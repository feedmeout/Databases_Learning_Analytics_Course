"""Review images for the lecturer: each slide next to its speaker notes as the presenter window (N) shows them, 4 slides per image.
Usage: python3 review.py /abs/path/out/N2P1.html ../review/N2P1/pilot.png 5,7,8
       more than 4 slides -> pilot_1.png, pilot_2.png, ...
Also checks every slide of the deck: the presenter must show each note's text unchanged, markup aside ("notes shown: all")."""
import sys, asyncio, io, os
from playwright.async_api import async_playwright
from PIL import Image

BG, PAD, SW, SH, NW = (11, 22, 40), 24, 960, 540, 900


def plain(t):
    """Text the presenter must show for a note with markup: backticks gone, ** gone outside code (written apart from the engine's regexes)."""
    seg = t.split('`')
    return ''.join(s if k % 2 else s.replace('**', '') for k, s in enumerate(seg))


async def main(src, dst, idxs):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1600, 'height': 900})
        await pg.goto('file://' + src); await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content='nav.ctl{display:none!important}')
        async with pg.expect_popup() as pi:
            await pg.keyboard.press('n')
        pres = await pi.value
        await pres.set_viewport_size({'width': NW, 'height': SH})
        await pres.add_style_tag(content='.bar,.nxt,.btns,aside{display:none!important}body{display:block!important;height:auto!important}main{overflow:visible!important}')
        deck = await pg.evaluate('window.DECK')
        n = len(deck['slides'])
        if not all(1 <= i <= n for i in idxs):
            raise SystemExit('slides must be between 1 and %d' % n)
        bad = []
        await pg.keyboard.press('Home')
        shots = {}
        for i in range(1, n + 1):
            if i > 1:
                await pg.keyboard.press('ArrowRight')
            await pg.wait_for_timeout(120)
            shown = await pres.evaluate("[...document.querySelectorAll('#notes li')].map(li => li.textContent)")
            want = [plain(t) if deck['meta'].get('notesMarkup') else t for t in deck['slides'][i - 1]['notes']]
            if shown != want:
                bad.append(i)
            if i in idxs:
                await pg.wait_for_timeout(400)
                slide = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB').resize((SW, SH), Image.LANCZOS)
                notes = Image.open(io.BytesIO(await (await pres.query_selector('main')).screenshot())).convert('RGB')
                shots[i] = (slide, notes)
        await b.close()
    print('notes shown:', 'all' if not bad else 'MISMATCH on slides %s' % bad)
    groups = [idxs[k:k + 4] for k in range(0, len(idxs), 4)]
    stem, ext = os.path.splitext(dst)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    for g, grp in enumerate(groups, 1):
        rows = [shots[i] for i in grp]
        hs = [max(SH, nt.height) for _, nt in rows]
        img = Image.new('RGB', (PAD * 3 + SW + NW, PAD + sum(h + PAD for h in hs)), BG)
        y = PAD
        for (sl, nt), h in zip(rows, hs):
            img.paste(sl, (PAD, y)); img.paste(nt, (PAD * 2 + SW, y)); y += h + PAD
        out = dst if len(groups) == 1 else '%s_%d%s' % (stem, g, ext)
        img.save(out, optimize=True)
        print('slides', ','.join(map(str, grp)), '->', out)
    if bad:
        sys.exit(1)

asyncio.run(main(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]))
