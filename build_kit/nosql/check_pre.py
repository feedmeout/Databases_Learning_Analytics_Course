# Code panes use white-space:pre with overflow hidden, so shot2.py cannot see clipped code.
# This check opens every slide and reports any <pre> or code block whose content is wider or taller than its box.
#   python3 check_pre.py /abs/path/out/N2P1.html      -> must end "clipped code: none"
import sys, asyncio
from playwright.async_api import async_playwright
async def main(path):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1600, 'height': 900})
        await pg.goto('file://' + path); await pg.wait_for_timeout(1500)
        bad = await pg.evaluate("""() => { const out = [];
          document.querySelectorAll('.slide').forEach((s, i) => {
            document.querySelectorAll('.slide').forEach(x => x.classList.remove('on')); s.classList.add('on');
            s.querySelectorAll('pre, code.n2code').forEach(e => {
              const dw = e.scrollWidth - e.clientWidth, dh = e.scrollHeight - e.clientHeight;
              if (dw > 1 || dh > 1) out.push(`slide ${i + 1}: ${e.className || e.tagName} wider by ${dw}px, taller by ${dh}px`); }); });
          return out; }""")
        for x in bad: print(x)
        print('clipped code:', 'none' if not bad else len(bad))
        await b.close()
asyncio.run(main(sys.argv[1]))
