# Maintaining Pitaka translations

For **maintainers** of `PLFIndia/pitaka-translations`. Contributors should read
[CONTRIBUTING.md](CONTRIBUTING.md) instead.

This repo is the staging area for translation contributions. Nothing here ships
to users automatically. "Approving" a translation means **you** decide it's good
and then copy the value into the Pitaka app repo. There is no bot, no backend,
no auto-merge into the app — by design (Pitaka has no developer-operated server).

---

## The two repos

| Repo | Role |
|---|---|
| `PLFIndia/pitaka` | The Android app. English source of truth: `app/src/main/res/values/strings.xml`. Shipped translations live in `app/src/main/res/values-hi/strings.xml` (Hindi) and `values-pa/strings.xml` (Punjabi). |
| `PLFIndia/pitaka-translations` (this repo) | Staging. Suggestion **issues** land here; bulk translators open **PRs** against `translations/values-<locale>/strings.xml`. |

A suggestion is a *proposal*. It becomes a shipped translation only when you put
the value into the app repo's `values-<locale>/strings.xml` and cut a release.

---

## Two intake channels

1. **Suggestion issues** — one string at a time, filed from inside the app
   (Settings → Help translate Pitaka → long-press text → Submit). Best for
   one-off corrections. Pre-filled with String ID, English source, target
   language, the suggestion, a context note, app version, and a ticked MIT
   license box.
2. **Pull requests** — many strings at once, against
   `translations/values-<locale>/strings.xml`. Best for bulk work. Review with
   GitHub's normal PR flow; an automated check (`scripts/validate_translations.py`,
   run by the `Validate translations` workflow) gates every PR: XML validity,
   key parity, placeholder integrity, invisible-character and homoglyph
   screening, and oversize flags. See [scripts/README.md](scripts/README.md).

---

## Reviewing a suggestion issue

### 1. Read it
Note the **String ID** (e.g. `library_empty_headline`), the **English source**,
the **target language**, and the **suggested translation**. The submitter has
already agreed to MIT (the checkbox) — that's your right to ship it.

### 2. Judge it against the style rules
Full rules: [docs/TONE.md](docs/TONE.md) and [docs/GLOSSARY.md](docs/GLOSSARY.md).
Quick checklist:

- [ ] Colloquial, not Sanskritized/textbook (how a bilingual urban friend would
      say it on WhatsApp).
- [ ] **Placeholders preserved exactly** — `%1$s`, `%1$d`, etc. must all be
      present. Re-ordering is fine (`%2$s ... %1$d`); dropping one is a bug.
- [ ] Length roughly matches the English so it fits the button/label.
- [ ] Proper nouns left English (Pitaka, GitHub, ISBN).
- [ ] Loanwords OK where already everyday (Backup, Scan, Settings, Wishlist).
- [ ] Western punctuation (`.` not `।`), Arabic numerals (0–9 not ०–९).

### 3. Decide

**Approve** → label `approved`, then ship it (see "Shipping" below). Close the
issue with a note like `shipped in v0.2.0` and credit the contributor.

**Needs work** → comment with the specific change you want, label `needs-changes`,
keep it open until revised.

**Reject** → comment why, label `declined`/`wontfix`, close. Closing is your
"disapprove".

> There is no approve/reject button that ships anything. The labels are just
> organization; the real approval is the edit you make in the app repo.

---

## Shipping an approved translation

Translations live in the **app repo**, not here. To ship one approved string:

1. In `PLFIndia/pitaka`, open (or create) the locale file:
   - Hindi → `app/src/main/res/values-hi/strings.xml`
   - Punjabi → `app/src/main/res/values-pa/strings.xml`

   If it's the first string for that language, create the folder + file with a
   standard resources wrapper:

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <resources>
   </resources>
   ```

2. Add the line — **same `name`**, translated value:

   ```xml
   <string name="library_empty_headline">कोई किताब नहीं है अभी</string>
   ```

3. Only add keys you've approved. Missing keys fall back to English
   automatically — partial locale files are correct and expected.

4. Build to confirm it compiles, commit, push, and the string ships in the next
   app release.

5. Back here, close the issue (or merge the PR) and note where it shipped.

> Keeping translations in the app repo (not mirrored here) is deliberate —
> single source of truth, no drift. This repo stages proposals; the app repo
> holds what actually ships.

---

## Reviewing a bulk PR

1. Check the diff only touches `translations/values-<locale>/strings.xml`.
2. Confirm the `Validate translations` check passed (green). It mechanically
   catches dropped/added placeholders, invisible bidi overrides, homoglyph
   (mixed-script) attacks, and translated repo slugs — so your review can focus
   on tone and meaning, not on spotting an invisible character by eye. If it's
   red, read the error lines; each names the offending key and reason.
3. Spot-check tone/glossary on a sample of strings.
4. Approve + merge using GitHub's PR review.
5. To ship: copy the merged values into the app repo's `values-<locale>/`
   file(s) as above, or cherry-pick the keys you want in this release.

---

## Labels

Suggestion issues filed via the app's prefilled URL do **not** arrive
pre-labeled (GitHub only auto-applies issue-form labels when submitted through
its own UI, not via a prefilled link). Apply labels by hand. Suggested set:

| Label | Meaning |
|---|---|
| `translation` | A translation suggestion (vs. a bug/question). |
| `needs-review` | Not yet looked at. |
| `approved` | Accepted; pending ship into the app repo. |
| `needs-changes` | Sent back to the contributor for a tweak. |
| `declined` | Rejected, with a reason in the comments. |
| `shipped` | Landed in an app release (optional; closing also works). |

---

## Credit

When a translation ships, credit the contributor in the app's release notes.
If they asked to stay anonymous (some note it in their issue/PR), honour that.
