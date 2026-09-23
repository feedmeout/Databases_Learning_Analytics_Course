"""Student PDF of a deck, one slide per page, no speaker notes.
Usage: python3 topdf_deck.py /abs/path/out/W3P1.html /abs/path/out/W3P1_student.pdf
Recipe used for every delivered student PDF: Chromium print media, CSS page size (1600 x 900 px), backgrounds on, fonts given time to load."""
import sys, asyncio
from playwright.async_api import async_playwright
async def main(src, dst):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1600, 'height': 900})
        await pg.goto('file://' + src); await pg.wait_for_timeout(2500)
        await pg.emulate_media(media='print'); await pg.wait_for_timeout(800)
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        await pg.pdf(path=dst, prefer_css_page_size=True, print_background=True)
        await b.close(); print('slides:', n, '->', dst)
asyncio.run(main(sys.argv[1], sys.argv[2]))
