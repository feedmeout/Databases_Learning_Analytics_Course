# Runs NoSQL Evening 2, Part 3 against a real MongoDB (set-up as run_e2p1.py) -> e2p3_outputs.json, E2P3_output.txt
import json, os, re, subprocess
from e2p3_cmds import PANES
H = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(H, '..', 'sources_nosql')
def sh(cmd, stdin=None, cwd=None):
    r = subprocess.run(cmd, shell=True, input=stdin, cwd=cwd, capture_output=True, text=True)
    return (r.stdout + r.stderr).replace('\r', '')
# starting state: books re-imported, Evening 1's world.country, persons pasted from persons.txt (corrected copy)
sh('mongoimport books.json -d library -c books --drop', cwd=SRC)
sh('mongosh --quiet', stdin='use world\ndb.dropDatabase()\ndb.country.insertOne({ name: "Greece", euSince: 1981, population: 10400000 })\n'
   'db.country.insertMany([ { name: "France", euSince: 1958, population: 68600000, capital: { name: "Paris", timezone: "Europe/Paris" } },'
   ' { name: "Germany", euSince: 1958, population: 83600000, capital: { name: "Berlin", timezone: "Europe/Berlin" } } ])\n'
   'use book-filtered-top-subset\ndb.dropDatabase()\n')
OUT = {}
paste = sh('mongosh --quiet', stdin=open(os.path.join(SRC, 'persons_corrected.txt'), encoding='utf8').read() + '\n')
m = re.search(r"\{\n  acknowledged: true,\n  insertedIds: \{.*?\n  \}\n\}", paste, re.S)
OUT['persons_load'] = [m.group(0)]
lines = []
for key, st in PANES:
    for i, s in enumerate(st):
        lines += ['print("@@%s#%d")' % (key, i), ' '.join(s.split())]
t = sh('mongosh --quiet', stdin='\n'.join(lines) + '\n')
chunks = re.split(r'\n[^\s>]+> ', '\n' + t)
res = {}
for k, c in enumerate(chunks):
    mm = re.fullmatch(r'@@(\w+)#(\d+)\n?', c)
    if mm: res.setdefault(mm.group(1), {})[int(mm.group(2))] = chunks[k + 1].rstrip('\n')
for key, st in PANES:
    assert key in res and len(res[key]) == len(st), key
    OUT[key] = [res[key][i] for i in range(len(st))]
    for o in OUT[key]:
        assert ('Uncaught' not in o and 'Error' not in o) or key == 'poll', (key, o)
assert OUT['persons_pipeline'][2] == OUT['persons_project'][0] == OUT['persons_find'][0]
json.dump(OUT, open(os.path.join(H, 'e2p3_outputs.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
open(os.path.join(H, 'E2P3_output.txt'), 'w', encoding='utf8').write('# persons.txt pasted\n' + paste + '\n# Part 3 session\n' + t)
for key, _ in PANES: print('==', key, json.dumps(OUT[key], ensure_ascii=False)[:400])
print('== persons_load', OUT['persons_load'][0][:120].replace('\n', ' '))
