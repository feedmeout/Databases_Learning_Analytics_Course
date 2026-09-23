# Runs every command of NoSQL Evening 2, Part 2 against a real MongoDB (same set-up as run_e2p1.py) -> e2p2_outputs.json, E2P2_output.txt
import json, os, re, subprocess
from e2p2_cmds import SHEET, CMDS
H = os.path.dirname(os.path.abspath(__file__))

def session(lines):
    r = subprocess.run('mongosh --quiet', shell=True, input='\n'.join(['use library'] + lines) + '\n', capture_output=True, text=True)
    return (r.stdout + r.stderr).replace('\r', '')

def run(stmts):
    """stmts: {key: [statements]} -> {key: [outputs]} in one session, with markers"""
    lines = []
    for key, st in stmts.items():
        for i, s in enumerate(st):
            lines += ['print("@@%s#%d")' % (key, i), ' '.join(s.split())]
    t = session(lines)
    chunks = re.split(r'\n(?:test|library)> ', '\n' + t)
    res = {}
    for k, c in enumerate(chunks):
        m = re.fullmatch(r'@@(\w+)#(\d+)\n?', c)
        if m:
            res.setdefault(m.group(1), {})[int(m.group(2))] = chunks[k + 1].rstrip('\n')
    out = {}
    for key, st in stmts.items():
        assert key in res and len(res[key]) == len(st), key
        out[key] = [res[key][i] for i in range(len(st))]
    return out, t

stmts = {}
for q in SHEET:
    stmts['q%d_find' % q['n']] = [q['find']]
    if q['count']: stmts['q%d_count' % q['n']] = [q['count']]
    if q['show']: stmts['q%d_show' % q['n']] = [q['show']]
for k in ('example', 'java', 'andor', 'sortcase', 'regex', 'javascript', 'count_old', 'java_lc', 'zeros_java'):
    stmts[k] = CMDS[k]
OUT, transcript = run(stmts)
for k, v in OUT.items():
    for o in v:
        assert 'Uncaught' not in o and 'Error' not in o, (k, o[:200])
# the two syntax errors of the old solutions, each in its own session (an unclosed string must not swallow later lines)
for k in ('curly', 'unclosed'):
    t = session([' '.join(CMDS[k][0].split())])
    OUT[k] = [l for l in t.split('\n') if 'SyntaxError' in l][0].strip()
    transcript += '\n# %s\n%s' % (k, t)
# item 1 typed without `use library`: mongosh starts in the database test
r = subprocess.run('mongosh --quiet', shell=True, input='db.books.countDocuments()\n', capture_output=True, text=True)
OUT['q1_in_test'] = [re.sub(r'^test> ', '', (r.stdout + r.stderr).replace('\r', '').strip().split('\n')[0]).strip()]
transcript += '\n# item 1 in the database test\n' + r.stdout
for q in SHEET:            # keep only the first lines of the big outputs
    OUT['q%d_find' % q['n']] = ['\n'.join(OUT['q%d_find' % q['n']][0].split('\n')[:12])]
json.dump(OUT, open(os.path.join(H, 'e2p2_outputs.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
open(os.path.join(H, 'E2P2_output.txt'), 'w', encoding='utf8').write(transcript)
print('statements', sum(len(v) for v in stmts.values()), '+ 2 syntax errors')
for q in SHEET:
    c = OUT.get('q%d_count' % q['n'], [''])[0]
    print(q['n'], 'count', c or '-', '| show', (OUT.get('q%d_show' % q['n'], [''])[0] or '')[:120].replace('\n', ' '))
for k in ('example', 'java', 'andor', 'sortcase', 'regex', 'javascript', 'count_old', 'java_lc', 'zeros_java', 'curly', 'unclosed'):
    print('==', k, OUT[k])
