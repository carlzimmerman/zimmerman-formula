"""Read-only structural checks of this task package, not a physics validator."""
import collections, hashlib, json, re, sys
from pathlib import Path
base=Path(__file__).resolve().parent
root=base.parents[1]
errors=[]
def check(ok,msg):
    if not ok: errors.append(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((base/'manifest.json').read_text()); tasks=m['tasks']
s=json.loads((base/'SOURCE_MANIFEST.json').read_text())['sources']
ids=[t['id'] for t in tasks]; expected=[f'AS{i:03d}' for i in range(1,2001)]
check(ids==expected,'IDs are not exactly ordered AS001..AS2000')
check(len(set(t['title'] for t in tasks))==2000,'Duplicate title')
check(collections.Counter(t['group'] for t in tasks)=={f'A{i:02d}':100 for i in range(1,21)},'Group counts differ from 100')
files=[p for p in base.glob('AS*_*.md') if re.fullmatch(r'AS[0-9]{3,4}_[a-z0-9_]+[.]md',p.name)]
check(len(files)==2000,'Individual Markdown task count differs from 2000')
check({p.name for p in files}=={t['file'] for t in tasks},'Manifest/file-set mismatch')
check(len({t.get('claim_key') for t in tasks})==2000,'Duplicate claim key')
check(m['task_count']==2000,'Manifest count mismatch')
lookup={t['id']:t for t in tasks}
words=[]
sections=['## Assignment and principle','## Framework base','## Sources to inspect','## Mathematics and principal test','## Inputs, domain','## Execute in order','## Controls','## Completion criterion','## Return package','## First-principles obligation','## Contribution to common-theory closure','## Authorized continuation and branching']
for t in tasks:
    p=base/t['file']
    if not p.is_file():check(False,f'Missing file {p.name}');continue
    text=p.read_text();words.append(len(text.split()))
    check(sha(p)==t['task_sha256'],f'{t["id"]}: task hash differs')
    for sec in sections:check(sec in text,f'{t["id"]}: missing {sec}')
    for field in ['title','principle','math','inputs','completion','branch','claim_key','first_principles','closure_bridge']:
        check(isinstance(t.get(field),str) and len(t[field].strip())>8,f'{t["id"]}: thin {field}')
    check(4<=len(t['steps'])<=6,f'{t["id"]}: step count')
    check(len(t.get('continuation',[]))==3,f'{t["id"]}: three distinct continuation directions required')
    check(len(t['checks'])>=2,f'{t["id"]}: needs controls')
    check(t['priority'] in ('P0','P1','P2'),f'{t["id"]}: priority')
    check(t['kind'] in ('derivation','computation','audit','construction'),f'{t["id"]}: kind')
    check(t['execution_state']=='proposed',f'{t["id"]}: false execution state')
    for d in t['depends_on']:
        check(d in lookup and d!=t['id'],f'{t["id"]}: invalid dependency {d}')
    for src in t['sources']:
        check(src in s,f'{t["id"]}: source unpinned {src}')
        check((root/src).is_file(),f'{t["id"]}: source missing {src}')
    link_text=re.sub(r'```.*?```','',text,flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)',link_text):
        check((p.parent/target).resolve().exists(),f'{t["id"]}: broken local link {target}')
visited=set();active=set()
def dfs(i):
    if i in active:check(False,f'Dependency cycle at {i}');return
    if i in visited:return
    active.add(i)
    for d in lookup[i]['depends_on']:
        if d in lookup:dfs(d)
    active.remove(i);visited.add(i)
for i in ids:dfs(i)
stale=[]
for path,h in s.items():
    p=root/path
    if not p.is_file() or sha(p)!=h:stale.append(path)
index=(base/'INDEX.md').read_text()
for t in tasks:check(f']({t["file"]})' in index,f'{t["id"]}: index link absent')
check(not stale,'Pinned sources changed: '+', '.join(stale))
report={'validation_scope':'Task structure, links, hashes, counts and acyclic explicit dependencies only; not scientific validity',
 'task_count':len(tasks),'individual_markdown_files':len(files),'group_count':len(m['groups']),
 'pinned_source_count':len(s),'min_words_per_task':min(words) if words else 0,
 'median_words_per_task':sorted(words)[len(words)//2] if words else 0,
 'max_words_per_task':max(words) if words else 0,'stale_sources':stale,'errors':errors,'passed':not errors}
print(json.dumps(report,indent=2))
sys.exit(bool(errors))
