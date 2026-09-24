# CLAUDE.md

## What this repository is
Course material for «Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης» (co-taught, online over Zoom, in Greek). The lecturer, Thanos, teaches:
- Learning Analytics: 3 weeks × 3 parts (W1P1 … W3P3), with lab sheets and answer keys.
- NoSQL/MongoDB: 2 evenings × 3 parts (N1P1–N1P3, N2P1–N2P3), following his colleague's decks in `build_kit/sources_nosql/`.

Everything is built from sources in `build_kit/`. `build_kit/README.txt` is the full history and the rules: read it before any change (latest sections v13 to v14, and the list «Αλλαγές από το παλαιότερο υλικό» at its end).

## How it is built
- Sources: `build_kit/content/*.json`, one per deck. The NoSQL JSON files are written by `build_kit/nosql/make_*.py`; their mongosh outputs come from real runs, stored in `nosql/e2p*_outputs.json` (`run_e2p*.py`).
- Engine: `build_kit/build_html2.js` + `deck2.css` + `deck.client.js` → one self-contained HTML per deck in `build_kit/out/`.
- Build (inside `build_kit/`): `node build_html2.js content/n2p1.json out/N2P1.html`
- Checks, all must pass before showing anything:
  - `python3 shot2.py "$PWD/out/N2P1.html" /tmp/s_ ""` → `problems: 0 | JS errors: none`
  - `python3 nosql/check_pre.py "$PWD/out/N2P1.html"` → `clipped code: none`
  - `python3 topdf_deck.py "$PWD/out/N2P1.html" "$PWD/out/N2P1_student.pdf"` (student PDF, one slide per page)
  - A4 documents: `python3 lab1/topdf.py <html> <pdf>` → `pages overflowing: none`
  - Notes rules: `python3 check_notes.py "$PWD/out/N2P1.html"` → `notes rules: ok` (read every warning; errors must be zero)
  - Notes and review images: `python3 review.py "$PWD/out/N2P1.html" ../review/N2P1/pilot.png 5,7,8` → `notes shown: all`
- Never hand-edit HTML in `out/`: change the JSON or its generator and rebuild.
- Engine changes are opt-in (a new flag or markup). After any engine change, every earlier deck must rebuild with identical slide HTML: compare the part between `<div id="stage">` and `<nav class="ctl"` before and after. Check a new CSS class name with grep before using it (`.wkc` already exists).
- Legacy one-off scripts with absolute paths from an old sandbox (`audit/`, `lab1/check.py`, `workbook/make_wb.py`): ignore unless asked.

## Rules for all content (the lecturer's standing preferences)
- Formal, natural Greek; never literal translation (he rejected «κοόρτη» as laughable).
- No GenAI style: no qualifiers that vouch for the material («…, με την πραγματική έξοδο», «με διορθωμένη διατύπωση»), no background facts students do not need, no filler.
- Anything students must download or open gets a direct clickable link: `[κείμενο](https://…)` in slide text.
- Theory parts: 30–35 slides, one idea per slide, minutes summing to exactly 45, two skippable slides, one timed question (its label is the timer), labels «Να θυμάστε», «Ερώτημα», «Προσοχή» (and «Δοκιμάστε»). No clock times and no calendar dates on slides, no placeholders, no slide that presupposes students' answers.
- Every fact verified at the source; every mongosh output from a real run (README v12).
- NoSQL follows the colleague's approach (his decks in `sources_nosql/`): update and correct, do not redesign.
- NoSQL Evening 1 (N1P1–N1P3) is final: change it only if he asks.

## Speaker notes (Σημειώσεις): the current task
The notes are what he reads while the slide is on screen.
1. Follow the slide from top to bottom; every item that carries the slide's message gets a note.
2. Each note starts with the item to point at, written exactly as on the slide and shown in bold, then one or two short spoken sentences.
3. Nothing that is not on the slide, except at most one line «Αν ρωτήσουν: …».
4. No meta: nothing about skipping (the «Αν είστε πίσω» tag already shows it), sources, versions, how outputs were produced, or the colleague's old slides. Keep those in a list «Αλλαγές από το παλαιότερο υλικό» in README.txt.
5. 2 to 4 notes per slide, short sentences.
6. If a slide line is not worth a note, or a key item is hard to see, propose the slide change and wait.

Notes take markup when the deck opts in with `'notesMarkup': True` in its meta (set in the deck's generator, as in `nosql/make_n2p1.py`): `**item**` → bold, `` `code` `` → code (README v14). Decks without the flag keep plain-text notes, exactly as before. The optional "spotlight" (clicking a note lights up its item on the shared slide) is not built; it needs its own opt-in change.

## Working with the lecturer
- He reads short messages only: English in chat, Greek in the material.
- He approves by looking at images: for every changed deck, save PNG review images (each slide next to its notes, 4 slides per image) in `review/<deck>/` with `build_kit/review.py`, and commit them.
- One branch per deck (`notes/<deck>`). Never rewrite history or delete files unless he asks.
- Decide sensible details yourself; ask at most one short question when something is truly his call.
- Order of work: N2P1, N2P2, N2P3 (taught next), then W1P1 to W3P3.

## Environment
Run `./setup.sh` once per session (Playwright Chromium, poppler-utils, Pillow, the Node package `docx`, the deck font Commissioner). If the browser cannot be installed, the cloud environment needs network access set to Full; otherwise stop and tell him.
