# Runs every command of NoSQL Evening 2, Part 1 against a real MongoDB and stores the outputs.
# Needs: mongod running on localhost:27017 (MongoDB Community 8.0.32), mongosh 2.12.0 and Database Tools 100.19.0 on PATH.
#   python3 run_e2p1.py   -> e2p1_outputs.json (every output, keyed as in e2p1_cmds.py) and E2P1_output.txt (the full transcript)
import json, os, re, subprocess
from e2p1_cmds import CMDS, IMPORT, IMPORT_AGAIN
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, '..', 'sources_nosql')
OUT = {}

def sh(cmd, stdin=None, cwd=None):
    r = subprocess.run(cmd, shell=True, input=stdin, cwd=cwd, capture_output=True, text=True)
    return (r.stdout + r.stderr).replace('\r', '')

# 1. mongoimport, as in the colleague's slide (with --drop), then a second run without --drop
OUT['import'] = sh(IMPORT, cwd=SRC).rstrip('\n')
again = sh(IMPORT_AGAIN, cwd=SRC).rstrip('\n').split('\n')
OUT['import_again_first'] = again[0]
OUT['import_again_last'] = again[-1]
OUT['import_again_errors'] = sum(1 for l in again if 'E11000 duplicate key error' in l)
# 2. mongoimport typed inside mongosh
OUT['import_in_mongosh'] = sh('mongosh --quiet', stdin=IMPORT + '\n').rstrip('\n')

# 3. every statement of every pane, one mongosh session, each preceded by a marker
assert list(CMDS)[0] == 'book23'
lines = []
for key, stmts in CMDS.items():
    for i, s in enumerate(stmts):
        lines.append('print("@@%s#%d")' % (key, i))
        lines.append(' '.join(s.split()))
transcript = sh('mongosh --quiet', stdin='\n'.join(lines) + '\n')
chunks = re.split(r'\n(?:test|library)> ', '\n' + transcript)
res = {}
for k, c in enumerate(chunks):
    m = re.fullmatch(r'@@(\w+)#(\d+)\n?', c)
    if m:
        res.setdefault(m.group(1), {})[int(m.group(2))] = chunks[k + 1].rstrip('\n')
for key, stmts in CMDS.items():
    assert key in res and len(res[key]) == len(stmts), key
    OUT[key] = [res[key][i] for i in range(len(stmts))]
    for o in OUT[key]:
        assert 'Uncaught' not in o or key == 'projerr', (key, o)

json.dump(OUT, open(os.path.join(H, 'e2p1_outputs.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
with open(os.path.join(H, 'E2P1_output.txt'), 'w', encoding='utf8') as f:
    f.write('$ ' + IMPORT + '\n' + OUT['import'] + '\n\n$ ' + IMPORT_AGAIN + '   (first and last line)\n' + OUT['import_again_first'] + '\n...\n'
            + OUT['import_again_last'] + '\n\n# typed inside mongosh\n' + OUT['import_in_mongosh'] + '\n\n# mongosh session\n' + transcript)
print('panes', len(CMDS), 'statements', sum(len(v) for v in CMDS.values()), 'duplicate-key errors', OUT['import_again_errors'])
