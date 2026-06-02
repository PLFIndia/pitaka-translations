# Translation hygiene checks

This directory holds the automated gate for translation contributions, built
to close Pitaka security finding **F-10** ("Translation supply chain has no
automated hygiene checks"). One merged malicious or malformed translation
breaks *every* install in that locale, and the defects involved — a swapped
placeholder, an invisible bidi override, a Cyrillic look-alike letter — are
exactly the things a human reviewer cannot reliably catch by eye. So a machine
catches them.

## Files

| File | Purpose |
|---|---|
| `validate_translations.py` | The checker. Pure Python 3.8+ stdlib, no dependencies. |
| `tests/test_validator.py` | Self-check: plants every defect class in a fixture and asserts each is caught (and that legitimate Indic shaping characters are *not* flagged). |
| `tests/fixtures/values-hi-clean/strings.xml` | A known-good Hindi file used as the positive control. |
| `run_tests.sh` | Convenience wrapper: runs the self-check, then validates the real `translations/` files if the English source is reachable. |

The **same** `validate_translations.py` runs in CI
(`.github/workflows/validate-translations.yml`) and locally, so what CI enforces
and what a contributor can self-check are identical by construction.

## What it checks

For each `translations/values-<locale>/strings.xml`, compared against the
canonical English source:

1. **XML validity** — the file must parse.
2. **Key sanity** — no duplicate keys; every key must exist in the English
   source; keys that are `translatable="false"` in English (the fixed repo-slug
   strings) must never be translated.
3. **printf-format parity** — the multiset of positional placeholders
   (`%1$s`, `%2$d`, `%1$.1f`, …) must match the English exactly. Re-ordering is
   allowed; dropping or adding one is an error. A literal `%%` is ignored.
4. **Dangerous invisible characters** — bidi overrides (U+202A–202E,
   U+2066–2069), zero-width space, LTR/RTL marks, BOM, Arabic letter mark are
   rejected. **ZWNJ (U+200C) and ZWJ (U+200D) are allowed** — Devanagari and
   Gurmukhi need them for correct conjunct rendering. (This is why a blanket
   "ban U+200B–U+200F" rule would be wrong for this repo.)
5. **Homoglyph / mixed-script** — each value may contain only its locale's own
   script (Devanagari for `hi`, Gurmukhi for `pa`), Latin (for loanwords like
   Backup / GitHub / ISBN / Pitaka), and script-neutral punctuation, digits,
   and symbols. A letter from any other script (Cyrillic, Greek, …) is the
   classic homoglyph attack and is rejected.
6. **Oversized strings** — a translation more than 4× the English length (with
   a small floor for very short labels) is **warned** about (does not fail the
   build) since it likely won't fit its button.

Errors fail the check (exit 1). Warnings alone do not.

## Running locally

```
# Full self-check + validate real files (against the vendored English mirror):
./scripts/run_tests.sh

# Just the self-check:
python3 scripts/tests/test_validator.py

# Validate against a specific English source:
python3 scripts/validate_translations.py \
  --english english/strings.xml \
  --translations translations
```

The English source-of-truth is in the **app repo** (`PLFIndia/pitaka`,
`app/src/main/res/values/strings.xml`), which is **private**. CI in this
(public) repo can't check it out without parking a credential here, so a
read-only mirror is vendored at `english/strings.xml` and kept current by a
one-way sync workflow in the app repo (see [../english/README.md](../english/README.md)).
Both CI and the local commands above validate against that mirror. To test
against a live app checkout instead, point `--english` at it (or set
`PITAKA_ENGLISH_STRINGS`).

## Adding a new locale

When you open a new language for contribution:

1. Add its Android locale code → Unicode script-name mapping to
   `LOCALE_SCRIPT` in `validate_translations.py`. The value is the prefix
   `unicodedata.name()` emits for that script's letters, e.g. `"BENGALI"`,
   `"TAMIL"`, `"GUJARATI"`. Without an entry, the script/homoglyph check is
   skipped for that locale (and a warning is emitted) — the other checks still
   run.
2. Add the language row to `README.md`'s "Currently supported languages" table.

## Prior art

- **Placeholder parity** mirrors Android lint's translation-consistency check.
- **Mixed-script / homoglyph** screening follows the Unicode TR-39 model; we
  implement the stronger per-locale allow-list variant rather than shipping a
  spot-confusables table, which catches the whole attack class without a
  database.
