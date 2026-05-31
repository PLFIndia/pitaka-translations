# Pitaka — Localization Glossary

Locked decisions for how brand terms, proper nouns, and recurring concepts get rendered across all Pitaka translations. **Do not deviate without changing this file first.**

Format: `English term → Decision → Notes for translator`

---

## Brand / app identity

| English | Decision | Notes |
|---|---|---|
| **Pitaka** | **Keep as `Pitaka`** | The app name. Do not translate to पिटक / ਪਿਟਕ — feels archaic and unbranded. Always use Latin script "Pitaka". |

## Proper nouns & external services

| English | Decision | Notes |
|---|---|---|
| GitHub | Keep English | Latin script. |
| Cloudflare | Keep English | Latin script. |
| Open Library | Keep English | Latin script. |
| Google Books | Keep English | Latin script. |
| Goodreads | Keep English | Latin script. |
| Android | Keep English | Latin script. |
| ISBN | Keep English | Standard identifier. |
| OAuth, PAT, Device Flow | Keep English | Technical terms users already know in English. |
| Drive, Dropbox, SD card | Keep English / loanword | Devanagari/Gurmukhi spelling of "ड्राइव" / "ਡਰਾਈਵ" is also fine. |

## Loanwords — keep English (in native script if natural)

These are loanwords bilingual urban users actually speak in English. Don't sanskritize.

| English | Hindi | Punjabi | Notes |
|---|---|---|---|
| Wishlist | विशलिस्ट | ਵਿਸ਼ਲਿਸਟ | Or keep "Wishlist" in Latin. Both fine. |
| Backup | बैकअप | ਬੈਕਅੱਪ | Never "प्रतिलिपि" / "ਪ੍ਰਤੀਲਿਪੀ". |
| Settings | सेटिंग्स | ਸੈਟਿੰਗਾਂ | "सेटिंग्स" is universal. |
| Scan | स्कैन | ਸਕੈਨ | Don't say "अवलोकन". |
| Import / Export | इंपोर्ट / एक्सपोर्ट | ਇੰਪੋਰਟ / ਐਕਸਪੋਰਟ | OK as English too. |
| Camera | कैमरा | ਕੈਮਰਾ | Always loanword. |
| Cancel | कैंसल | ਕੈਂਸਲ | Don't translate as "रद्द करें" unless the whole app's tone is formal. We're casual. |
| OK | ठीक है | ਠੀਕ ਹੈ | "OK" in Latin is also fine. Pick one and stick with it. |
| Share | शेयर | ਸ਼ੇਅਰ | Don't say "साझा करें". |

## Translate — but colloquial, not textbook

| English | Hindi (recommended) | Punjabi (recommended) | Reject |
|---|---|---|---|
| Library | लाइब्रेरी | ਲਾਇਬ੍ਰੇਰੀ | "पुस्तकालय" — too formal for this app. |
| Book | किताब | ਕਿਤਾਬ | "पुस्तक" — too formal. |
| Vault | तिजोरी | ਤਿਜੋਰੀ | "कोष" — wrong register. |
| Borrower | (no single word — phrase it) | (same) | "उधार लेने वाला" — too literal. Prefer "किसने ली" / "ਕਿਸਨੇ ਲਈ" phrasings in context, or just "Borrower" loanword. |
| Lend | उधार देना | ਉਧਾਰ ਦੇਣਾ | Standard, fine. |
| Loan | उधार | ਉਧਾਰ | Standard, fine. |
| Pending | (translate per context) | (same) | "Overdue" → "देरी से" / "ਦੇਰੀ ਨਾਲ"; "Due soon" → "जल्द लौटानी है" / "ਛੇਤੀ ਮੋੜਨੀ ਹੈ". Don't translate "Pending" as one word — describe what's pending. |
| Publish | पब्लिश | ਪਬਲਿਸ਼ | Or "प्रकाशित" — translator's choice. |
| Search | खोज / सर्च | ਖੋਜ / ਸਰਚ | Either. |
| Add a book | किताब जोड़ें | ਕਿਤਾਬ ਜੋੜੋ | |
| Save | सेव / सहेजें | ਸੇਵ / ਸਾਂਭੋ | Either. |
| Delete | डिलीट | ਡਿਲੀਟ | Or "हटाएँ" / "ਹਟਾਓ". |
| Edit | एडिट | ਐਡਿਟ | Or "बदलें" / "ਬਦਲੋ". |
| Notes | नोट्स | ਨੋਟਸ | Don't say "टिप्पणियाँ". |

## Words to be careful with

- **"Borrower"** — Hindi/Punjabi have no clean single-word equivalent that doesn't sound like a legal document. Prefer rephrasing: "Borrowers" list → "किसको दी" / "ਕਿਸ ਨੂੰ ਦਿੱਤੀ" (literally "who-given-to") or just keep "Borrowers" as loanword.
- **"Passphrase"** — "पासफ्रेज़" / "ਪਾਸਫ੍ਰੇਜ਼" is fine. "गुप्त वाक्य" is correct but feels textbook.
- **"Vault"** in the Pitaka sense (encrypted area) → "तिजोरी" / "ਤਿਜੋਰੀ" is the warmest fit; users get "a private locked place" from the metaphor.

## Numerics & dates

- **Dates** — let Android format per the user's locale. Do not bake date format into translations.
- **Numbers** — use Devanagari numerals (०१२३) for Hindi UI? **No** — keep Arabic numerals (0123). Devanagari numerals are now uncommon in modern Hindi UI and create OCR/parsing issues with ISBNs etc. Same for Punjabi: use Arabic numerals.
- **"%1$d day(s)"** — for Hindi/Punjabi, write `%1$d दिन` / `%1$d ਦਿਨ`. Both languages don't need a separate plural form for "1 day" vs "2 days" — same word.

## Punctuation

- **Sentence-final period** — Hindi traditionally uses "।" (purna viraam). For an app UI, **use Western period "."** — it matches the surrounding modern UI tone. Devanagari "।" feels textbook and adds visual noise.
- **Punjabi** — same: use Western period ".".
- **Question marks, commas, exclamation** — Western (?, !, ,).

## Capitalization

- Hindi and Punjabi don't have case. Don't try to mimic English Title Case. Just write naturally.
- For app titles where English says "Add Book", Hindi just says "किताब जोड़ें" — no special casing needed.

## When in doubt

Default to: **"how would a bilingual urban friend explain this on WhatsApp?"**
Not: **"how would a Hindi/Punjabi-medium textbook write this?"**

If a string genuinely has no comfortable native equivalent, **keep it in English (Latin script)**. Mixing scripts within Pitaka UI is fine and matches how users actually communicate.
