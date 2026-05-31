# Contributing translations to Pitaka

Thanks for helping translate Pitaka. This file explains the mechanics. For style / register guidance, see [docs/TONE.md](docs/TONE.md). For locked decisions on brand terms and loanwords, see [docs/GLOSSARY.md](docs/GLOSSARY.md).

---

## The easy path — in-app suggestion

If you have Pitaka installed:

1. **Settings → Help translate Pitaka → toggle ON.**
2. **Long-press any UI text in the app.** The screen briefly highlights every other long-pressable text (5-second hint), and a suggestion sheet opens for the text you pressed.
3. Pick **Hindi** or **Punjabi**, type your suggestion, optionally add a context note, tap **Submit on GitHub**.
4. Your browser opens a pre-filled GitHub Issue. Review and submit.

A maintainer reviews the issue, applies the right label, and either folds the suggestion in or asks a clarifying question.

---

## The manual path — direct edits

If you want to translate many strings at once:

### 1. Find the canonical English source

The English source-of-truth for every Pitaka string lives in the main Pitaka repo:

  https://github.com/plfindia/pitaka/blob/main/app/src/main/res/values/strings.xml

Each `<string name="...">value</string>` line is one translatable string. The `name` is the string ID we use everywhere.

### 2. Pick or create a target file

In this repo, translations go in `translations/values-<locale>/strings.xml`:

  - Hindi: `translations/values-hi/strings.xml`
  - Punjabi: `translations/values-pa/strings.xml`

Don't translate every string at once — partial files are fine. Android automatically falls back to the English source for any missing key.

### 3. Translate

Copy the English `<string>` line, then change the value (NOT the `name`). Examples:

```xml
<!-- English (canonical) -->
<string name="library_empty_headline">No books yet</string>

<!-- Hindi -->
<string name="library_empty_headline">कोई किताब नहीं है अभी</string>

<!-- Punjabi -->
<string name="library_empty_headline">ਅਜੇ ਕੋਈ ਕਿਤਾਬ ਨਹੀਂ</string>
```

**Keep placeholders intact.** `%1$s`, `%1$d`, etc. must appear exactly as in the English source — the app substitutes runtime values into them. Re-ordering is OK: `%1$d days for %2$s` in English can become `%2$s के लिए %1$d दिन` in Hindi.

**Escape correctly.** Apostrophes go as `\'` (e.g. `Couldn\'t reach`). Quotes go as `\"`. Newlines as `\n`.

### 4. Open a PR

Branch from `main`, commit your changes, push to your fork, open a PR. CI will verify the XML parses and that no placeholder went missing.

---

## Style guidance summary

Full doc: [docs/TONE.md](docs/TONE.md). The short version:

  ✅ Colloquial, conversational ("किताब डिलीट करें?" not "क्या आप पुस्तक को हटाना चाहते हैं?")
  ✅ Loanwords where they're already in everyday speech (Backup, Scan, Settings, Wishlist)
  ✅ Western punctuation (`.` not `।`)
  ✅ Arabic numerals (0–9 not ०–९)
  ✅ Short — match the button/label size of the English

  ❌ Sanskritized formal Hindi/Punjabi
  ❌ "उपयोगकर्ता" / "पुस्तक" / "प्रतिलिपि" — too textbook
  ❌ Word-for-word literal translation
  ❌ Translating proper nouns (Pitaka, GitHub, ISBN stay English)

When in doubt: **how would a bilingual urban friend explain this on WhatsApp?**

---

## What gets credited

When a translation ships in a Pitaka release, the contributor is credited in the release notes. If you'd prefer to remain anonymous, mention it in your issue/PR.

---

## Questions

Open a regular GitHub Issue (not the suggest-translation form) and a maintainer will respond.
