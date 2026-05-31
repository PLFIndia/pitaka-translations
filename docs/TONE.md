# Pitaka — Translation Tone Guide

**One-line rule:** write like a friend explaining the app over WhatsApp, not like a school textbook explaining the app on a blackboard.

Pitaka's English copy is deliberately casual ("No books yet", "Just mark purchased", "Without a backup passphrase, you can't restore your vault on a new phone"). It is conversational, sometimes uses contractions, and trusts the reader. Translations should match this register, not flatten it into formal prose.

---

## Register guidance — what we want

✅ **Colloquial, conversational, lightly literary.** The way an educated bilingual person would write a casual text or a personal note.
✅ **Loanwords where they're already in everyday speech.** "Backup", "Scan", "Wishlist", "Settings" — these are how people actually talk.
✅ **Short over long.** Buttons especially: 1–2 words. UI real estate is limited.
✅ **Direct address.** Speak TO the user, not ABOUT the user. "अपनी किताब जोड़ें" not "उपयोगकर्ता अपनी पुस्तक जोड़ सकते हैं".
✅ **Western punctuation.** Period `.` not purna viraam `।`. Question mark `?`, comma `,`.
✅ **Arabic numerals.** 0123 not ०१२३.

## Register guidance — what we reject

❌ **Shuddh Hindi / pure Punjabi.** "पुस्तकालय में पुस्तक जोड़ें" reads like a 1970s textbook. We want "लाइब्रेरी में किताब जोड़ें".
❌ **Sanskritized translations of common English words.** "बैकअप" not "प्रतिलिपि"; "स्कैन" not "अवलोकन"; "नोट्स" not "टिप्पणियाँ".
❌ **Overly formal honorifics where the English is casual.** English: "Save". Don't translate as "कृपया सहेजें". Just "सेव" or "सहेजें".
❌ **Translating proper nouns.** Pitaka stays Pitaka. GitHub stays GitHub. ISBN stays ISBN.
❌ **Word-for-word literal translation.** Reorder, drop, or rephrase to make it sound natural.

---

## Worked examples

### Example 1 — empty state

**English:** "No books yet"

✅ Hindi: "कोई किताब नहीं है अभी"  *or*  "अभी कोई किताब नहीं"
✅ Punjabi: "ਅਜੇ ਕੋਈ ਕਿਤਾਬ ਨਹੀਂ"

❌ Reject Hindi: "अद्यतिथि पुस्तक उपलब्ध नहीं है" (formal, dead)
❌ Reject Punjabi: "ਹਾਲੇ ਤੱਕ ਕੋਈ ਪੁਸਤਕ ਉਪਲਬਧ ਨਹੀਂ ਹੈ" (formal, dead)

### Example 2 — action button

**English:** "Scan a book"

✅ Hindi: "किताब स्कैन करें"
✅ Punjabi: "ਕਿਤਾਬ ਸਕੈਨ ਕਰੋ"

❌ Reject: "पुस्तक का अवलोकन करें" / "ਪੁਸਤਕ ਦਾ ਅਵਲੋਕਨ ਕਰੋ"

### Example 3 — warning

**English:** "Without a backup passphrase, you can't restore your vault on a new phone."

✅ Hindi: "बैकअप पासफ्रेज़ के बिना, नए फ़ोन पर अपनी तिजोरी रिस्टोर नहीं कर पाएँगे।"
✅ Punjabi: "ਬੈਕਅੱਪ ਪਾਸਫ੍ਰੇਜ਼ ਤੋਂ ਬਿਨਾਂ, ਨਵੇਂ ਫ਼ੋਨ 'ਤੇ ਤੁਸੀਂ ਆਪਣੀ ਤਿਜੋਰੀ ਰੀਸਟੋਰ ਨਹੀਂ ਕਰ ਸਕੋਗੇ।"

(Notice "बैकअप", "पासफ्रेज़", "रिस्टोर", "तिजोरी" — three loanwords, one translated. That's the right mix.)

### Example 4 — short status

**English:** "Saved."

✅ Hindi: "हो गया।" *or* "सेव हो गया।"
✅ Punjabi: "ਹੋ ਗਿਆ।" *or* "ਸੇਵ ਹੋ ਗਿਆ।"

❌ Reject: "सहेजा गया।" / "ਸੰਭਾਲਿਆ ਗਿਆ।" (correct, but dead)

### Example 5 — confirmation question

**English:** "Delete this book?"

✅ Hindi: "इस किताब को डिलीट करें?" *or* "किताब डिलीट कर दें?"
✅ Punjabi: "ਇਹ ਕਿਤਾਬ ਡਿਲੀਟ ਕਰਨੀ ਹੈ?"

❌ Reject: "क्या आप इस पुस्तक को हटाना चाहते हैं?" / "ਕੀ ਤੁਸੀਂ ਇਸ ਪੁਸਤਕ ਨੂੰ ਹਟਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ?" (verbose, formal)

### Example 6 — informational copy with technical terms

**English:** "Pitaka uses your own GitHub OAuth App for sign-in (§1.1 — no developer infrastructure). Register one at github.com/settings/applications/new with the Device Flow option checked and paste the Client ID below."

This kind of string mixes technical terms (GitHub, OAuth App, Device Flow, Client ID) with instructional copy. Keep technical terms in English. Translate the connective tissue.

✅ Hindi: "साइन-इन के लिए Pitaka आपकी अपनी GitHub OAuth App इस्तेमाल करता है (§1.1 — कोई डेवलपर इन्फ़्रास्ट्रक्चर नहीं)। github.com/settings/applications/new पर एक रजिस्टर करें, Device Flow option टिक करें, और नीचे Client ID पेस्ट करें।"

(URLs, "OAuth App", "Device Flow", "Client ID", "GitHub" all stay English. Result: a Hindi sentence that an actual dev-curious user will understand instantly.)

---

## Length budget

| UI element | Target max | Notes |
|---|---|---|
| Bottom nav label | 1 short word | "Library" → "लाइब्रेरी" works; "पुस्तकालय" overflows. |
| Button label | 1–3 words | "Save", "Cancel", "Lend". Keep tight. |
| Dialog title | ≤ 4 words | "Delete this book?" |
| Dialog body | 1–2 sentences | OK to be slightly longer in Hindi/Punjabi than English if needed for clarity. |
| Section heading | 1–3 words | "Vault & security" → don't pad it. |
| Empty-state body | 1 sentence | Be brief. |

If your translation is twice as long as the English, you're probably over-formalizing. Try again.

---

## Code-mixing is allowed

Pitaka is a personal library app. Real bilingual users mix scripts naturally. The following is *fine*:

- "Pitaka में आपकी किताबें"
- "GitHub पर पब्लिश करें"
- "अपना Backup पासफ्रेज़ सेट करें"
- "ਆਪਣੀ Vault ਅਨਲੌਕ ਕਰੋ"

What's NOT fine:

- Forcing a Latin-script-only word into Devanagari/Gurmukhi when it would look weird ("गिथब", "ਗਿਥਬ" — no).
- Forcing a native word into Latin where the native script is more natural ("kitaab" — Devanagari "किताब" is better in a Hindi locale UI).

Default to: **brand/protocol words in Latin script. Native verbs/nouns in native script. Mix where natural.**

---

## Voice & person

Pitaka talks TO the user in second person, friendly. Match it.

- English: "Your library." → Hindi: "आपकी लाइब्रेरी।" → Punjabi: "ਤੁਹਾਡੀ ਲਾਇਬ੍ਰੇਰੀ।"
- English: "Lock vault" (imperative) → Hindi: "तिजोरी लॉक करें।" → Punjabi: "ਤਿਜੋਰੀ ਲਾਕ ਕਰੋ।"
- Never refer to the user in third person ("उपयोगकर्ता", "ਯੂਜ਼ਰ") in UI copy.

---

## Final checklist for translators

Before submitting any translation, check:

- [ ] Does it sound like something a bilingual urban friend would say casually?
- [ ] Are technical/brand terms (Pitaka, GitHub, ISBN, OAuth, Backup, Vault) per the GLOSSARY?
- [ ] Is the punctuation Western (`.` `?` `,`)?
- [ ] Are the numerals Arabic (0–9)?
- [ ] Is it short enough to fit in the UI element it goes into?
- [ ] Did you check the placeholders (`%1$s`, `%1$d`) are preserved exactly?
- [ ] Does it feel WARM rather than FORMAL?

If all checked, ship it.
