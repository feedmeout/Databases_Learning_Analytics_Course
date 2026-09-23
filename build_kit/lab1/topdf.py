import asyncio, sys
from playwright.async_api import async_playwright
async def main(src, dst):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.goto('file://' + src); await pg.wait_for_timeout(1200)
        over = await pg.evaluate("[...document.querySelectorAll('.page')].map((s,i)=>{const c=s.querySelector('.content')||s;return [i+1, c.scrollHeight-c.clientHeight, s.scrollHeight-s.clientHeight]}).filter(x=>x[1]>1||x[2]>1)")
        print('pages overflowing (page, content px, page px):', over or 'none')
        await pg.pdf(path=dst, prefer_css_page_size=True, print_background=True); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
