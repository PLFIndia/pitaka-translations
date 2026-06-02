#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_translations.py — automated hygiene gate for Pitaka translations.

Addresses Pitaka security finding F-10 ("Translation supply chain has no
automated hygiene checks"). One merged malicious translation breaks *every*
install in that locale, and no human reviewer reliably catches a swapped
placeholder, an invisible bidi override, or a Cyrillic homoglyph. This script
catches them mechanically.

The SAME script runs in CI (.github/workflows/validate-translations.yml) and
locally (`python3 scripts/validate_translations.py --english <path>`), so the
rules CI enforces and the rules a contributor can self-check are, by
construction, identical — single source of truth.

No third-party dependencies: Python 3.8+ standard library only. This is
deliberate. The repo has no build system and CI should need nothing but
`python3`. (Mozilla's `compare-locales`, named in the original plan, targets
Mozilla l10n formats — .ftl/.properties/.dtd — and does not natively parse
Android strings.xml, so it would be the wrong borrow here.)

Checks performed against each translations/values-<locale>/strings.xml,
compared to the canonical English source (app repo's values/strings.xml):

  1. XML validity              — the file must parse as XML.
  2. Key sanity                — no duplicate keys; every translated key must
                                 exist in the English source; keys marked
                                 translatable="false" in English (repo slugs)
                                 must never be translated.
  3. printf-format parity      — the multiset of positional placeholders
                                 (%1$s, %2$d, %1$.1f, ...) must match the
                                 English source exactly. Re-ordering is fine;
                                 dropping or adding one is an error. A literal
                                 %% is correctly ignored.
  4. Dangerous invisible chars — bidi overrides (U+202A–202E, U+2066–2069),
                                 zero-width space, LTR/RTL marks, BOM, Arabic
                                 letter mark. ZWNJ (U+200C) / ZWJ (U+200D) are
                                 ALLOWED — Devanagari and Gurmukhi need them
                                 for correct conjunct rendering.
  5. Homoglyph / script mixing — per-locale script allow-list. A value may
                                 contain only its own script (Devanagari for
                                 hi, Gurmukhi for pa), Latin (loanwords: Backup,
                                 GitHub, ISBN, Pitaka), and script-neutral
                                 punctuation/digits/symbols. A letter from any
                                 other script (Cyrillic "С", Greek "Α", ...) is
                                 the classic homoglyph attack and is rejected.
  6. Oversized strings         — a translation more than 4x the English length
                                 (with a small floor for very short labels)
                                 won't fit its button/label and is flagged.

Prior art: Android lint's translation-consistency checks (placeholder parity),
the Unicode TR-39 "mixed-script / confusables" model (we implement the stronger
allow-list variant rather than a spot-confusables table).

Exit code 0 = clean, 1 = at least one ERROR (warnings alone do not fail).
"""

from __future__ import annotations

import argparse
import os
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Locale code -> the Unicode script-name prefix unicodedata.name() emits for
# that script's letters and combining marks. Latin and "Common" (punctuation,
# digits, symbols, whitespace) are allowed for *every* locale on top of this.
LOCALE_SCRIPT: Dict[str, str] = {
    "hi": "DEVANAGARI",
    "pa": "GURMUKHI",
}

# Format-category (Cf) code points that are ALWAYS allowed: needed by Indic
# scripts for correct shaping.
ALLOWED_FORMAT_CHARS = {
    0x200C,  # ZERO WIDTH NON-JOINER
    0x200D,  # ZERO WIDTH JOINER
}

# Invisible / bidi control characters that have no legitimate place in a UI
# string and are the vehicle for label-reordering attacks. Each maps to a
# human-readable reason for the report.
DANGEROUS_INVISIBLES = {
    0x200B: "ZERO WIDTH SPACE",
    0x200E: "LEFT-TO-RIGHT MARK",
    0x200F: "RIGHT-TO-LEFT MARK",
    0x202A: "LEFT-TO-RIGHT EMBEDDING",
    0x202B: "RIGHT-TO-LEFT EMBEDDING",
    0x202C: "POP DIRECTIONAL FORMATTING",
    0x202D: "LEFT-TO-RIGHT OVERRIDE",
    0x202E: "RIGHT-TO-LEFT OVERRIDE",
    0x2066: "LEFT-TO-RIGHT ISOLATE",
    0x2067: "RIGHT-TO-LEFT ISOLATE",
    0x2068: "FIRST STRONG ISOLATE",
    0x2069: "POP DIRECTIONAL ISOLATE",
    0x061C: "ARABIC LETTER MARK",
    0xFEFF: "ZERO WIDTH NO-BREAK SPACE (BOM)",
}

# Oversize rule: flag if len(translation) > max(LENGTH_RATIO * len(en),
# len(en) + SHORT_FLOOR). The floor stops tiny source strings ("OK", "Save")
# from tripping the ratio when their Indic equivalent is naturally a few code
# points longer.
LENGTH_RATIO = 4
SHORT_FLOOR = 20

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


# ---------------------------------------------------------------------------
# Placeholder parsing
# ---------------------------------------------------------------------------

import re

# java.util.Formatter conversion spec:
#   %[argument_index$][flags][width][.precision]conversion
# We also match a literal %% so we can discard it (it is NOT a placeholder).
_PLACEHOLDER_RE = re.compile(
    r"""
    %%                                  # literal percent -> discarded
    |
    %                                   # start of a real placeholder
    (?P<index>\d+\$)?                   # optional argument index, e.g. 1$
    (?P<flags>[-#+ 0,(]*)               # optional flags
    (?P<width>\d+)?                     # optional width
    (?P<prec>\.\d+)?                    # optional .precision
    (?P<conv>[a-zA-Z])                  # conversion char (s, d, f, ...)
    """,
    re.VERBOSE,
)


def extract_placeholders(text: str) -> Counter:
    """Return a multiset of normalized placeholder tokens (literal %% ignored).

    A token is the full placeholder string, e.g. '%1$s', '%2$d', '%1$.1f'.
    Comparing the full string (not just the conversion char) means a precision
    change like %1$f -> %1$.1f is also caught, which matters for correctness.
    """
    counts: Counter = Counter()
    for m in _PLACEHOLDER_RE.finditer(text):
        whole = m.group(0)
        if whole == "%%":
            continue
        counts[whole] += 1
    return counts


# ---------------------------------------------------------------------------
# XML loading
# ---------------------------------------------------------------------------

@dataclass
class StringEntry:
    name: str
    text: str
    translatable: bool


def load_strings(path: str) -> Tuple[Dict[str, StringEntry], List[str]]:
    """Parse an Android strings.xml. Returns (entries_by_name, duplicate_names).

    Uses itertext() so any inline markup is flattened to its text content.
    XML entities (&amp;) are decoded by the parser; Android escapes (\\' \\")
    remain literal, which is correct — they are not placeholders or letters.
    """
    tree = ET.parse(path)
    root = tree.getroot()
    entries: Dict[str, StringEntry] = {}
    duplicates: List[str] = []
    for el in root.findall("string"):
        name = el.get("name")
        if not name:
            continue
        translatable_attr = el.get("translatable")
        translatable = translatable_attr != "false"
        text = "".join(el.itertext())
        if name in entries:
            duplicates.append(name)
        entries[name] = StringEntry(name=name, text=text, translatable=translatable)
    return entries, duplicates


# ---------------------------------------------------------------------------
# Per-value checks
# ---------------------------------------------------------------------------

@dataclass
class Findings:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def extend(self, other: "Findings") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)


def script_of(ch: str) -> Optional[str]:
    """Return the script-name prefix for a letter/mark, else None.

    None means the character is script-neutral (punctuation, digit, symbol,
    whitespace, format control) and is allowed for any locale.
    """
    cat = unicodedata.category(ch)
    if not (cat.startswith("L") or cat.startswith("M")):
        return None  # not a letter or combining mark -> script-neutral
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return "UNNAMED"
    # Names look like "DEVANAGARI LETTER KA", "CYRILLIC SMALL LETTER ES",
    # "LATIN SMALL LETTER A". The leading word(s) identify the script.
    for prefix in (
        "DEVANAGARI", "GURMUKHI", "LATIN", "CYRILLIC", "GREEK", "ARABIC",
        "HEBREW", "BENGALI", "TAMIL", "TELUGU", "KANNADA", "MALAYALAM",
        "GUJARATI", "ORIYA", "HAN", "HANGUL", "HIRAGANA", "KATAKANA", "THAI",
    ):
        if name.startswith(prefix):
            return prefix
    return name.split()[0]


def check_value(
    key: str,
    en_text: str,
    tr_text: str,
    locale_script: Optional[str],
) -> Findings:
    f = Findings()

    # --- 3. printf-format parity -------------------------------------------
    en_ph = extract_placeholders(en_text)
    tr_ph = extract_placeholders(tr_text)
    if en_ph != tr_ph:
        missing = list((en_ph - tr_ph).elements())
        extra = list((tr_ph - en_ph).elements())
        parts = []
        if missing:
            parts.append(f"missing {missing}")
        if extra:
            parts.append(f"unexpected {extra}")
        f.error(
            f"[{key}] placeholder mismatch: {', '.join(parts)} "
            f"(English has {sorted(en_ph.elements())})"
        )

    # --- 4. dangerous invisibles -------------------------------------------
    for i, ch in enumerate(tr_text):
        cp = ord(ch)
        if cp in DANGEROUS_INVISIBLES:
            f.error(
                f"[{key}] contains disallowed invisible character "
                f"U+{cp:04X} {DANGEROUS_INVISIBLES[cp]} at index {i}"
            )

    # --- 5. homoglyph / script mixing --------------------------------------
    if locale_script is not None:
        allowed_scripts = {locale_script, "LATIN"}
        seen_foreign: Dict[str, str] = {}
        for ch in tr_text:
            cp = ord(ch)
            if cp in ALLOWED_FORMAT_CHARS:
                continue
            sc = script_of(ch)
            if sc is None:
                continue  # script-neutral
            if sc not in allowed_scripts:
                # Record one example per offending script for a concise report.
                if sc not in seen_foreign:
                    try:
                        nm = unicodedata.name(ch)
                    except ValueError:
                        nm = "?"
                    seen_foreign[sc] = f"U+{cp:04X} {nm} ({ch!r})"
        for sc, example in seen_foreign.items():
            f.error(
                f"[{key}] contains {sc}-script letter(s) not allowed for this "
                f"locale — possible homoglyph attack: {example}. "
                f"Allowed: {locale_script} + Latin + punctuation."
            )

    # --- 6. oversized string -----------------------------------------------
    en_len = len(en_text)
    tr_len = len(tr_text)
    limit = max(LENGTH_RATIO * en_len, en_len + SHORT_FLOOR)
    if tr_len > limit:
        f.warn(
            f"[{key}] translation is {tr_len} chars vs English {en_len} "
            f"(> {LENGTH_RATIO}x); may not fit its label."
        )

    return f


# ---------------------------------------------------------------------------
# Per-file orchestration
# ---------------------------------------------------------------------------

def locale_from_dirname(dirname: str) -> Optional[str]:
    """values-hi -> hi, values-b+sr+Latn -> None (unsupported here)."""
    base = os.path.basename(dirname)
    if not base.startswith("values-"):
        return None
    return base[len("values-"):]


def validate_locale_file(
    path: str,
    locale: str,
    english: Dict[str, StringEntry],
) -> Findings:
    f = Findings()
    rel = path

    try:
        tr_entries, duplicates = load_strings(path)
    except ET.ParseError as e:
        f.error(f"[{rel}] XML does not parse: {e}")
        return f

    for dup in duplicates:
        f.error(f"[{rel}] duplicate key defined more than once: '{dup}'")

    locale_script = LOCALE_SCRIPT.get(locale)
    if locale_script is None:
        f.warn(
            f"[{rel}] locale '{locale}' has no script mapping; "
            f"skipping homoglyph/script check (placeholder + invisibles + "
            f"length checks still apply). Add it to LOCALE_SCRIPT to enable."
        )

    for name, entry in tr_entries.items():
        en = english.get(name)
        if en is None:
            f.error(
                f"[{rel}][{name}] key does not exist in the English source — "
                f"typo or an injected key the app never reads."
            )
            continue
        if not en.translatable:
            f.error(
                f"[{rel}][{name}] key is translatable=\"false\" in the English "
                f"source (a fixed value such as a repo slug) and must not be "
                f"translated."
            )
            continue
        f.extend(check_value(name, en.text, entry.text, locale_script))

    return f


def discover_locale_files(translations_dir: str) -> List[Tuple[str, str]]:
    """Return [(path, locale), ...] for every values-*/strings.xml found."""
    out: List[Tuple[str, str]] = []
    if not os.path.isdir(translations_dir):
        return out
    for entry in sorted(os.listdir(translations_dir)):
        sub = os.path.join(translations_dir, entry)
        if not os.path.isdir(sub):
            continue
        locale = locale_from_dirname(sub)
        if locale is None:
            continue
        xml_path = os.path.join(sub, "strings.xml")
        if os.path.isfile(xml_path):
            out.append((xml_path, locale))
    return out


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Pitaka translation strings.xml files (F-10)."
    )
    parser.add_argument(
        "--english",
        required=True,
        help="Path to the canonical English strings.xml "
        "(app repo: app/src/main/res/values/strings.xml).",
    )
    parser.add_argument(
        "--translations",
        default="translations",
        help="Directory containing values-<locale>/strings.xml "
        "(default: ./translations).",
    )
    args = parser.parse_args(argv)

    if not os.path.isfile(args.english):
        print(f"ERROR: English source not found: {args.english}", file=sys.stderr)
        return 1

    try:
        english, en_dupes = load_strings(args.english)
    except ET.ParseError as e:
        print(f"ERROR: English source does not parse: {e}", file=sys.stderr)
        return 1

    if en_dupes:
        # The English source is upstream's, not a contributor's, but a dup
        # there would silently break parity for everyone — surface it.
        print(
            f"ERROR: English source has duplicate keys: {sorted(set(en_dupes))}",
            file=sys.stderr,
        )
        return 1

    files = discover_locale_files(args.translations)
    if not files:
        print(
            f"No values-*/strings.xml found under '{args.translations}'. "
            f"Nothing to validate."
        )
        return 0

    total = Findings()
    print(f"Validating {len(files)} locale file(s) against {args.english}\n")
    for path, locale in files:
        result = validate_locale_file(path, locale, english)
        n_keys = "?"
        try:
            entries, _ = load_strings(path)
            n_keys = str(len(entries))
        except Exception:
            pass
        status = "FAIL" if result.errors else ("WARN" if result.warnings else "OK")
        print(f"  [{status}] {path}  ({n_keys} keys, locale '{locale}')")
        total.extend(result)

    print()
    for w in total.warnings:
        print(f"  WARNING: {w}")
    for e in total.errors:
        print(f"  ERROR:   {e}")

    print()
    print(
        f"Summary: {len(total.errors)} error(s), "
        f"{len(total.warnings)} warning(s)."
    )
    return 1 if total.errors else 0


if __name__ == "__main__":
    sys.exit(main())
