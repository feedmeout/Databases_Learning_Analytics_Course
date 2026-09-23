import json, re, os, hashlib
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
os.makedirs('media', exist_ok=True)
import sys
DECKS = [int(x) for x in (sys.argv[1] if len(sys.argv)>1 else '1,2,3,4,5').split(',')]
OUT = sys.argv[2] if len(sys.argv)>2 else 'inventory.json'
inv = {}
def walk(shapes, acc):
    for sh in shapes:
        st = sh.shape_type
        if st == T.GROUP:
            acc['groups'] += 1; walk(sh.shapes, acc); continue
        if st == T.PICTURE:
            try:
                im = sh.image; h = hashlib.md5(im.blob).hexdigest()[:8]
                fn = f"{acc['deck']}_{acc['n']:02d}_{h}.{im.ext}"
                p = os.path.join('media', fn)
                if not os.path.exists(p): open(p,'wb').write(im.blob)
                acc['pics'].append({'file': fn, 'px': im.size, 'kb': round(len(im.blob)/1024), 'w_in': round(Emu(sh.width).inches,1), 'h_in': round(Emu(sh.height).inches,1)})
            except Exception as e:
                acc['pics'].append({'file': None, 'err': str(e)[:40]})
            continue
        if sh.has_text_frame:
            t = ' '.join(p.text for p in sh.text_frame.paragraphs).strip()
            if t: acc['texts'].append(t)
        if getattr(sh, 'has_table', False) and sh.has_table:
            acc['tables'] += 1
            for r in sh.table.rows:
                for c in r.cells:
                    if c.text.strip(): acc['texts'].append(c.text.strip())
        if getattr(sh, 'has_chart', False) and sh.has_chart: acc['charts'] += 1
        if st is None or 'graphicFrame' in sh._element.tag:
            x = sh._element.xml
            if 'dgm' in x or 'diagram' in x: acc['smartart'] += 1
        if 'video' in sh._element.xml.lower()[:3000] or st == T.MEDIA: acc['media'] += 1
for d in DECKS:
    prs = Presentation(f'd{d}.pptx')
    W, H = Emu(prs.slide_width).inches, Emu(prs.slide_height).inches
    for n, s in enumerate(prs.slides, 1):
        acc = {'deck': d, 'n': n, 'texts': [], 'pics': [], 'tables': 0, 'charts': 0, 'smartart': 0, 'groups': 0, 'media': 0}
        walk(s.shapes, acc)
        acc['layout'] = s.slide_layout.name
        acc['notes'] = (s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide and s.notes_slide.notes_text_frame is not None else '')
        words = sum(len(re.findall(r'\w+', t)) for t in acc['texts'])
        acc['words'] = words
        inv[f'{d}.{n}'] = acc
    print(f'deck {d}: {len(prs.slides)} slides, {W:.2f}x{H:.2f} in, layouts used: {sorted(set(inv[k]["layout"] for k in inv if k.startswith(str(d)+".")))}')
json.dump(inv, open(OUT,'w',encoding='utf8'), ensure_ascii=False, indent=0)
# SmartArt text is not in shape text frames: pull it from the diagram data parts
import zipfile
for d in DECKS:
    z = zipfile.ZipFile(f'd{d}.pptx'); names = z.namelist()
    dg = [n for n in names if n.startswith('ppt/diagrams/data')]
    print(f'deck {d}: diagram data parts = {len(dg)}, media files = {len([n for n in names if n.startswith("ppt/media/")])}, notes slides = {len([n for n in names if n.startswith("ppt/notesSlides/notesSlide")])}')
print()
print('deck.slide | words | pics | smartart | tables | notes? | first text')
for k, a in inv.items():
    first = (a['texts'][0] if a['texts'] else '')[:58].replace('\n',' ')
    flag = 'OVER' if a['words'] > 70 else ('thin' if a['words'] < 12 and not a['pics'] and not a['smartart'] else '')
    print(f"{k:>5} | {a['words']:>4} | {len(a['pics']):>2} | {a['smartart']:>2} | {a['tables']:>2} | {'Y' if a['notes'] else '-'} | {flag:4} | {first}")
