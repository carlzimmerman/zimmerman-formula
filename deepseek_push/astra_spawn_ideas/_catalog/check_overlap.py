"""Lexical candidate triage only; human/agent semantic review is still required."""
import json,math,re,collections,heapq
from pathlib import Path
B=Path(__file__).resolve().parent.parent
rows=json.loads((B/'manifest.json').read_text())['tasks']
texts=[]
for t in rows:
 texts.append(t['title']+' '+t['title']+' '+t['math']+' '+' '.join(t['steps']))
tokens=[collections.Counter(re.findall(r'[a-z][a-z0-9_]{2,}',s.lower())) for s in texts]
df=collections.Counter(w for x in tokens for w in x)
vecs=[]; inv=collections.defaultdict(list)
for i,ts in enumerate(tokens):
 v={w:(1+math.log(c))*math.log(len(rows)/df[w]) for w,c in ts.items() if 1<df[w]<180}
 norm=math.sqrt(sum(x*x for x in v.values()))
 v={w:x/norm for w,x in v.items()} if norm else {}
 vecs.append(v)
 for w,x in v.items():inv[w].append((i,x))
scores=collections.defaultdict(float)
for postings in inv.values():
 for p,(i,a) in enumerate(postings):
  for j,b in postings[p+1:]:scores[i,j]+=a*b
pairs=heapq.nlargest(160,scores.items(),key=lambda x:x[1])
result=[{'a':rows[i]['id'],'b':rows[j]['id'],'score':round(s,4),'a_title':rows[i]['title'],'b_title':rows[j]['title']} for (i,j),s in pairs]
(B/'_catalog/overlap_candidates.json').write_text(json.dumps(result,indent=2)+'\n')
for r in result[:65]:print(f"{r['score']:.3f} {r['a']} / {r['b']}: {r['a_title']} | {r['b_title']}")
