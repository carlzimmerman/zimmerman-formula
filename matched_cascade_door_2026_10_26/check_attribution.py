"""Public source review only. No local research is uploaded; no source text retained."""
import concurrent.futures, hashlib, json, re, urllib.request
from pathlib import Path

REV='7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a'
tree=json.loads(Path('/tmp/oai-preprints-tree.json').read_text())
terms=['Penrose','Vlasov','Boltzmann','Bose','condensate','Quantum-Depletion','Local-smoothing','Anderson','Scale-and-conformal']
paths=[t['path'] for t in tree['tree'] if t['type']=='blob' and t['path'].endswith(('.tex','.bib','.md')) and any(s.lower() in t['path'].split('/')[0].lower() for s in terms)]
patterns={
 'author':r'zimmerman+n?|carl\s+zimmerman',
 'project':r'zimmerman.formula|zimmerman.programme|new_physics',
 'physics_topic':r'\bMOND\b|Milgrom|Skordis|Z[lł]o[sś]nik|Tully.{0,3}Fisher|radial.acceleration.relation|galactic.acceleration',
 'recent_dois':r'23601528|23585319|23579379|21937958',
 'distinctive_number':r'9[.]36(?:19)?|0[.]417|0[.]4607',
}
compiled={k:re.compile(v,re.I) for k,v in patterns.items()}
def read(path):
 u='https://raw.githubusercontent.com/openai/math/'+REV+'/preprints/'+path
 try:
  data=urllib.request.urlopen(u,timeout=30).read();s=data.decode('utf-8');hits=[]
  for kind,pat in compiled.items():
   for match in pat.finditer(s):
    hits.append({'kind':kind,'line':s.count('\n',0,match.start())+1,'excerpt':s[max(0,match.start()-90):match.end()+90]})
  return {'path':path,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'hits':hits}
 except Exception as e:return {'path':path,'error':str(e)}
rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(read,paths))
out={'revision':REV,'date_checked_client':'2026-10-26','selection_terms':terms,'patterns':patterns,'manuscript_count':len(set(p.split('/')[0] for p in paths)),'files_requested':len(paths),'files_read':sum('error' not in r for r in rows),'files':rows,'limits':'Scoped source/bibliography exact and synonym search, not entire collection, plagiarism determination, or proof of independent discovery. No original work transmitted. Equation equivalence requires manual comparison; no access to training data or private development history.'}
Path('matched_cascade_door_2026_10_26/attribution_scan.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='files'}));print(json.dumps([r for r in rows if r.get('hits') or r.get('error')],indent=2))
