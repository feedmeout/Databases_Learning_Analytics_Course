"""Checks the speaker notes of a deck against the notes rules of CLAUDE.md, on the built HTML.
Usage: python3 check_notes.py /abs/path/out/N2P1.html      -> must end "notes rules: ok"
Errors (the deck is not done): not 2-4 notes; a note that does not start with **item** (except one «Αν ρωτήσουν: …» line);
  a bold item that is not on the slide (compared without spaces and backticks); unbalanced ** or backticks; words that belong to meta.
Warnings (read the slide again): items out of top-to-bottom order; more than two sentences after the item."""
import sys, re, asyncio
from playwright.async_api import async_playwright

META = ['παλαιότερο υλικό', 'παλιό υλικό', 'παλαιότερες διαφάνειες', 'παλιές διαφάνειες', 'συνάδελφ', 'παραλείπεται', 'αν ο χρόνος πιέζει',
        'πραγματική έξοδο', 'πραγματική εκτέλεση', 'πραγματικό τρέξιμο', 'ελέγχθηκε', 'επαληθεύτηκε', 'έκδοση του υλικού', 'version']
ASK = 'Αν ρωτήσουν: '
squash = lambda t: re.sub(r'\s+', '', t.replace('`', '').replace(' ', ' '))


def sentences(t):
    t = re.sub(r'`[^`]*`', 'X', t)
    return [s for s in re.split(r'(?<=[.;!])\s+', t.strip()) if s]


async def main(path):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1600, 'height': 900})
        await pg.goto('file://' + path); await pg.wait_for_timeout(1200)
        deck = await pg.evaluate('window.DECK')
        texts = await pg.evaluate("[...document.querySelectorAll('.slide')].map(s => s.textContent)")
        await b.close()
    if not deck['meta'].get('notesMarkup'):
        print("meta.notesMarkup is not set: bold items would show as ** in the presenter"); print('notes rules: 1 errors'); return 1
    errs = warns = 0
    for i, (s, txt) in enumerate(zip(deck['slides'], texts), 1):
        notes, flat, out = s['notes'], squash(txt), []
        if not 2 <= len(notes) <= 4:
            out.append(('E', f'{len(notes)} notes (2 to 4)'))
        asks, pos = 0, []
        for k, n in enumerate(notes, 1):
            if n.count('**') % 2 or n.count('`') % 2:
                out.append(('E', f'note {k}: unbalanced ** or `'))
            low = n.lower()
            for m in META:
                if m in low:
                    out.append(('E', f'note {k}: meta word «{m}»'))
            if n.startswith(ASK):
                asks += 1
                continue
            if not n.startswith('**'):
                out.append(('E', f'note {k}: does not start with **item**: {n[:60]}'))
                continue
            items = re.findall(r'\*\*(.+?)\*\*', n)
            for it in items:
                if squash(it) not in flat:
                    out.append(('E', f'note {k}: item not on the slide: {it}'))
            if items and squash(items[0]) in flat:
                pos.append((k, squash(items[0])))
            rest = n.split('**', 2)[-1].lstrip(':').strip() if items else n
            if len(sentences(rest)) > 2:
                out.append(('W', f'note {k}: {len(sentences(rest))} sentences after the item'))
        if asks > 1:
            out.append(('E', f'{asks} «Αν ρωτήσουν» lines (at most one)'))
        cur = 0
        for k, it in pos:  # each item must occur at or after the previous one (first match from there on)
            at = flat.find(it, cur)
            if at < 0:
                out.append(('W', f'note {k} points above the note before it (top-to-bottom order?)'))
            else:
                cur = at
        for kind, msg in out:
            errs += kind == 'E'; warns += kind == 'W'
            print(f"{'!!' if kind == 'E' else ' w'} slide {i:>2} ({s['title'][:40]}): {msg}")
    print(f'notes rules: {"ok" if not errs else f"{errs} errors"}' + (f' ({warns} warnings)' if warns else ''))
    return 1 if errs else 0

sys.exit(asyncio.run(main(sys.argv[1])))
