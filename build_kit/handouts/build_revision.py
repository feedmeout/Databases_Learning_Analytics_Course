"""Two-page revision sheet from the «Να θυμάστε» slides of the nine parts -> out/LA_revision_sheet.html (rework of 20 Sept 2026: the Lab 1 and Lab 2
«Να θυμάστε» slides now sit in Part 3 of their week, after the reveal; they are still attributed to the lab, i.e. Part 2).  PDF: python3 lab1/topdf.py"""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(HERE, '..'); e = html.escape
CSS = re.search(r"CSS = '''(.*?)'''", open(f'{K}/lab1/build_pack.py', encoding='utf8').read(), re.S).group(1)
CSS += '.rv{break-inside:avoid;margin:0 0 4.2mm}.rv h3{font-size:11pt;color:var(--deep);margin-bottom:1mm}.rv ol{margin-left:5mm}.rv li{font-size:10pt;line-height:1.42;margin-bottom:.8mm}.wk{font-size:13pt;font-weight:800;color:var(--ink);border-bottom:1.2pt solid var(--amber);padding-bottom:1mm;margin:2mm 0 3mm}'
def doc(title, pages): return f'<!DOCTYPE html><html lang="el"><head><meta charset="UTF-8"><title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400;500;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
def page(n, N, kicker, title, body, left, right): return f'<section class="page"><header><span class="kick">{e(kicker)}</span><h1>{e(title)}</h1></header><div class="content">{body}</div><footer><span>{e(left)}</span><span>{e(right)} · σελίδα {n} από {N}</span></footer></section>'
mk = lambda t: re.sub(r'_(.+?)_', r'<i>\1</i>', re.sub(r'\*(.+?)\*', r'<b>\1</b>', e(t)))
PARTS = [('Εβδομάδα 1 · Από τα δεδομένα στη γνώση', ['w1p1_v2', 'w1p2', 'w1p3']), ('Εβδομάδα 2 · Από τα ίχνη στη γνώση', ['w2p1', 'w2p2', 'w2p3']), ('Εβδομάδα 3 · Από τη γνώση στη δράση', ['w3p1', 'w3p2', 'w3p3'])]
blocks = []
for wk, files in PARTS:
    titles = {k: json.load(open(f'{K}/content/{f}.json', encoding='utf8'))['meta']['deckTitle'] for k, f in enumerate(files, 1)}
    for k, f in enumerate(files, 1):
        d = json.load(open(f'{K}/content/{f}.json', encoding='utf8'))
        for rem in [s for s in d['slides'] if s['type'] == 'remember']:
            lab = re.search(r'Εργαστήριο (\d)', rem['title'])
            part = 2 if lab else k                                     # a lab's points belong to Part 2, even when shown in Part 3
            blocks.append((wk, f'Μέρος {part} · {titles[part]}', rem['items']))
assert len(blocks) == 9 and sum(len(b[2]) for b in blocks) == 27, (len(blocks), sum(len(b[2]) for b in blocks))
assert [b[1][:7] for b in blocks] == ['Μέρος 1', 'Μέρος 2', 'Μέρος 3'] * 3, [b[1] for b in blocks]
def render(bl):
    out, cur = [], None
    for wk, part, items in bl:
        if wk != cur: out.append(f'<p class="wk">{e(wk.split(" · ")[0])}</p>'); cur = wk
        out.append(f'<div class="rv"><h3>{e(part)}</h3><ol>' + ''.join(f'<li>{mk(i)}</li>' for i in items) + '</ol></div>')
    return ''.join(out)
n1 = 5
R = [page(1, 2, 'Μαθησιακή Αναλυτική · Φύλλο επανάληψης', 'Να θυμάστε: τα σημεία των τριών εβδομάδων', render(blocks[:n1]), 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης', 'Φύλλο επανάληψης'),
     page(2, 2, 'Μαθησιακή Αναλυτική · Φύλλο επανάληψης', 'Να θυμάστε: τα σημεία των τριών εβδομάδων (συνέχεια)', render(blocks[n1:]) + '<div class="note"><b>Τα τέσσερα ερωτήματα που διατρέχουν την ενότητα.</b> Τι; Ποιος; Γιατί; Πώς; Και πριν από κάθε χρήση ενός δείκτη: τι μετρά, για ποιον, και τι ακολουθεί.</div>', 'Βάσεις Δεδομένων & Ανάλυση Δεδομένων Μάθησης', 'Φύλλο επανάληψης')]
open(f'{K}/out/LA_revision_sheet.html', 'w', encoding='utf8').write(doc('Μαθησιακή Αναλυτική: φύλλο επανάληψης', R))
print('revision sheet:', len(R), 'pages |', sum(len(b[2]) for b in blocks), 'points from', len(blocks), 'parts |', [b[1] for b in blocks])
