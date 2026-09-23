import sys, asyncio
from playwright.async_api import async_playwright
async def main(path, prefix, idxs):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1600,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://'+path); await pg.wait_for_timeout(1500)
        res = await pg.evaluate("""() => [...document.querySelectorAll('.slide')].map((s,i)=>{
          document.querySelectorAll('.slide').forEach(x=>x.classList.remove('on')); s.classList.add('on');
          const r=s.getBoundingClientRect(); let out=0, who='';
          s.querySelectorAll('*').forEach(e=>{ if(e.closest('svg')) return; const b=e.getBoundingClientRect(); if(!b.width||!b.height) return;
            const o=Math.max(b.right-r.right, b.bottom-r.bottom, r.left-b.left, r.top-b.top); if(o>out){out=o; who=(e.className||e.tagName)+''}});
          const body=s.querySelector('.body'); let clip=0, free=0;
          if(body){ clip=body.scrollHeight-body.clientHeight; const kids=[...body.children]; if(kids.length){const top=Math.min(...kids.map(k=>k.getBoundingClientRect().top)), bot=Math.max(...kids.map(k=>k.getBoundingClientRect().bottom)); free=Math.round(body.clientHeight-(bot-top));} }
          // inner text overflow of fixed-height boxes
          let inner=0, iw='';
          s.querySelectorAll('.node,.tile,.step,.cell,.qf,.item,.fbig,.cc,.vrow').forEach(e=>{const d=Math.max(e.scrollHeight-e.clientHeight, e.scrollWidth-e.clientWidth); if(d>inner){inner=d; iw=e.className}});
          return {i:i+1, type:s.className.match(/t-(\\w+)/)[1], out:Math.round(out), who, clip, inner, iw, free}})""")
        bad=0
        for r in res:
            flag = 'OK ' if r['out']<=0 and r['clip']<=1 and r['inner']<=1 else '!! '
            if flag!='OK ': bad+=1
            print(flag, f"{r['i']:>2} {r['type']:<11} out={r['out']:<4} clip={r['clip']:<4} inner={r['inner']:<4} free={r['free']:<4} {r['who'] if r['out']>0 else ''} {r['iw'] if r['inner']>1 else ''}")
        print('problems:', bad, '| JS errors:', errs or 'none')
        for i in idxs:
            await pg.evaluate(f"location.hash='#{i}'"); await pg.reload(); await pg.wait_for_timeout(450); await pg.screenshot(path=f'{prefix}{i:02d}.png')
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 and sys.argv[3] else []))
