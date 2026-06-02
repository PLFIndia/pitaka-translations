#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-check for validate_translations.py (F-10).

Generates fixtures in a system temp directory (no repo pollution, no cleanup
needed) and asserts the validator catches every planted defect while leaving
legitimate Indic shaping characters alone. Run by run_tests.sh and by CI.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# English source-of-truth lives in the app repo; a read-only mirror is vendored
# at english/strings.xml (see english/README.md). Default to that mirror; allow
# an override via PITAKA_ENGLISH_STRINGS (e.g. to test against a live app
# checkout locally).
ENGLISH = os.environ.get(
    "PITAKA_ENGLISH_STRINGS",
    os.path.abspath(os.path.join(HERE, "..", "..", "english", "strings.xml")),
)
VALIDATOR = os.path.abspath(os.path.join(HERE, "..", "validate_translations.py"))
CLEAN_FIXTURE = os.path.join(HERE, "fixtures", "values-hi-clean", "strings.xml")

# Planted defects, one per <string>:
#   1. dropped placeholder       -> loan_lent_date has no %1$s
#   2. added placeholder         -> common_ok gains a stray %1$s
#   3. RTL override (U+202E)      -> bidi attack (here over Arabic text, so it
#                                    also trips the script allow-list)
#   4. zero width space (U+200B)  -> invisible
#   5. Cyrillic homoglyph         -> "Сancel" with Cyrillic С (U+0421)
#   6. unknown key                -> not in English source
#   7. translatable="false" key   -> attempt to translate a repo slug
#   8. wrong float precision      -> %1$.2f instead of %1$.1f
#   9. ZWNJ (U+200C) legit        -> must NOT be flagged (control)
MALICIOUS = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="loan_lent_date">दिया गया</string>
    <string name="common_ok">ठीक है %1$s</string>
    <string name="add_book_save">\u202eسेव</string>
    <string name="library_empty_headline">कोई\u200bकिताब नहीं</string>
    <string name="add_book_cancel">\u0421ancel</string>
    <string name="totally_made_up_key">कुछ भी</string>
    <string name="contribute_repo_owner">हैकर</string>
    <string name="borrower_avg_return">औसत: %1$.2f दिन</string>
    <string name="nav_library">लाइब्रे\u200cरी</string>
</resources>
"""

EXPECTED_ERROR_KEYS = {
    "loan_lent_date",          # missing %1$s
    "common_ok",               # unexpected %1$s
    "add_book_save",           # RTL override (+ Arabic script)
    "library_empty_headline",  # ZWSP
    "add_book_cancel",         # Cyrillic homoglyph
    "totally_made_up_key",     # unknown key
    "contribute_repo_owner",   # translatable=false
    "borrower_avg_return",     # %1$.1f -> %1$.2f mismatch
}
MUST_NOT_ERROR = {"nav_library"}  # legitimate ZWNJ


def _run(translations_dir: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, VALIDATOR, "--english", ENGLISH, "--translations", translations_dir],
        capture_output=True, text=True,
    )


def main() -> int:
    failures = []

    with tempfile.TemporaryDirectory() as tmp:
        # --- dirty fixture: expect exit 1 + specific keys -------------------
        dirty_dir = os.path.join(tmp, "dirty", "values-hi")
        os.makedirs(dirty_dir)
        with open(os.path.join(dirty_dir, "strings.xml"), "w", encoding="utf-8") as fh:
            fh.write(MALICIOUS)
        proc = _run(os.path.join(tmp, "dirty"))
        dirty_out = proc.stdout + proc.stderr
        if proc.returncode != 1:
            failures.append(f"dirty fixture: expected exit 1, got {proc.returncode}")
        for key in EXPECTED_ERROR_KEYS:
            if f"[{key}]" not in dirty_out:
                failures.append(f"dirty: expected an ERROR mentioning [{key}], none found")
        for key in MUST_NOT_ERROR:
            for line in dirty_out.splitlines():
                if line.strip().startswith("ERROR:") and f"[{key}]" in line:
                    failures.append(f"dirty: [{key}] flagged but should be clean: {line.strip()}")

        # --- clean fixture: expect exit 0, no errors ------------------------
        clean_dir = os.path.join(tmp, "clean", "values-hi")
        os.makedirs(clean_dir)
        with open(CLEAN_FIXTURE, "r", encoding="utf-8") as fh:
            clean_content = fh.read()
        with open(os.path.join(clean_dir, "strings.xml"), "w", encoding="utf-8") as fh:
            fh.write(clean_content)
        proc = _run(os.path.join(tmp, "clean"))
        clean_out = proc.stdout + proc.stderr
        if proc.returncode != 0:
            failures.append(f"clean fixture: expected exit 0, got {proc.returncode}\n{clean_out}")

    if failures:
        print("SELF-CHECK FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("SELF-CHECK PASSED: all planted defects caught, clean fixture clean,")
    print("legitimate ZWNJ not flagged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
