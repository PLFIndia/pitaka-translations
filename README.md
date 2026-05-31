# pitaka-translations

Community-contributed translations for the Pitaka Android app — a local-first personal library tracker.

This repo lives alongside [Pitaka itself](https://github.com/plfindia/pitaka). Translation suggestions flow in via GitHub Issues (filed directly from inside the app by users who opt in to "Localization Contributor mode"); approved suggestions become PRs that ship in the next Pitaka release.

## Contributing

Two paths:

### 1. From inside the app (recommended)

Pitaka v0.x+ has a built-in contributor mode:

1. Open Pitaka → Settings → **Help translate Pitaka** → toggle ON
2. Long-press any UI text in the app
3. Pick the target language, type your suggestion, tap **Submit on GitHub**
4. A pre-filled issue opens in your browser. Review and submit.

You don't need to clone this repo or know anything about Android. The issue you file contains the string ID, the English source, and your suggested translation.

### 2. By hand

If you want to contribute many strings at once, or your phone can't open the browser, you can also:

1. Fork this repo.
2. Find or create `translations/values-xx/strings.xml` (where `xx` is the [Android locale code](https://developer.android.com/reference/java/util/Locale)).
3. Translate strings, following the [glossary](docs/GLOSSARY.md) and [tone guide](docs/TONE.md).
4. Open a PR.

## Currently supported languages

| Locale | Language       | Status              |
|--------|----------------|---------------------|
| `hi`   | Hindi          | Open for contribution |
| `pa`   | Punjabi        | Open for contribution |

Want to add another language? Open an issue with the locale code and we'll wire it in.

## Style

Pitaka's English copy is deliberately casual ("No books yet" / "Just mark purchased" / "Lend"). Translations should match that register — like a bilingual friend explaining the app on WhatsApp, not like a school textbook. See [docs/TONE.md](docs/TONE.md) for examples and [docs/GLOSSARY.md](docs/GLOSSARY.md) for the locked decisions on brand terms (`Pitaka`, `GitHub`, `ISBN` stay English; `Library`, `Vault`, `Borrower` get translated).

## How approved suggestions ship

1. A maintainer triages incoming `suggest_translation.yml` issues, applies a `language/xx` label, and either approves or comments.
2. Approved suggestions get folded into `translations/values-xx/strings.xml` (in this repo).
3. Periodically those `strings.xml` files get copied into the main Pitaka app repo at `app/src/main/res/values-xx/strings.xml` and ship in the next release.

Contributions are credited in the Pitaka release notes.

## License

Translations are licensed [MIT](LICENSE) — same as the main Pitaka app.
