import sys, asyncio
from playwright.async_api import async_playwright
async def main(path, outprefix, idxs):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1600,'height':900})
        errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
        await pg.goto('file://'+path)
        await pg.wait_for_timeout(1200)
        for i in idxs:
            await pg.evaluate(f"location.hash='#{i}'"); await pg.reload(); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{outprefix}{i:02d}.png')
        # overflow check on every slide
        res = await pg.evaluate("""() => [...document.querySelectorAll('.slide')].map((s,i)=>{s.classList.add('on');
            const r=s.getBoundingClientRect(); let worst=0, who='';
            s.querySelectorAll('*').forEach(e=>{ if(e.closest('svg')||e.hidden) return; const b=e.getBoundingClientRect(); if(!b.width) return;
               const rail=s.querySelector('.rail').getBoundingClientRect();
               const over=Math.max(b.right-r.right, b.bottom-r.bottom); if(over>worst){worst=over;who=e.className||e.tagName}});
            const src=s.querySelector('.src'), rail=s.querySelector('.rail');
            // does main content collide with the source line?
            let coll=0; if(src){const sb=src.getBoundingClientRect(); [...s.children].forEach(c=>{ if(c===src||c===rail) return; const cb=c.getBoundingClientRect(); if(cb.bottom>sb.top+2) coll=Math.max(coll,cb.bottom-sb.top)})}
            else {const rb=rail.getBoundingClientRect(); [...s.children].forEach(c=>{ if(c===rail) return; const cb=c.getBoundingClientRect(); if(cb.bottom>rb.top+2) coll=Math.max(coll,cb.bottom-rb.top)})}
            s.classList.toggle('on', i===0); return {i:i+1, overflow:Math.round(worst), who, collide:Math.round(coll)} })""")
        for r in res:
            flag = 'OK ' if r['overflow']<=0 and r['collide']<=0 else '!! '
            print(flag, r)
        print('JS errors:', errs or 'none')
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]))
