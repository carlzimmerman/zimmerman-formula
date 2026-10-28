import pathlib,io,contextlib,json,math,hashlib
import numpy as np
root=pathlib.Path(__file__).resolve().parents[3];p=root/'rebuild_2026_10_22/F2_outer_lensing/f2_outer_lensing.py';t=p.read_text();s=t[:t.index('# ============================================================================ 2. K0')]+t[t.index('# ============================================================================ 4. lens inventory'):t.index('# ============================================================================ 5. Track A')];n={'__file__':str(p),'__name__':'csm1_inventory'}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(s,str(p),'exec'),n)
h=.679;result={}
for b in range(4):
 inv=n['INV'][b];m=inv['logMs70']+2*np.log10(.7/h)+2*np.log10(inv['qDA']);m=m[inv['w']>0];g=n['LMG'];inds=set()
 for lm in m:
  if lm<=g[0]:inds.add(0)
  elif lm>=g[-1]:inds.add(len(g)-1)
  else:
   j=int(np.searchsorted(g,lm,side='left'))
   if lm==g[j]:inds.add(j)
   else:inds.update([j-1,j])
 result[str(b+1)]=dict(n_positive=int(len(m)),min_logMstar=float(m.min()),max_logMstar=float(m.max()),support_indices=sorted(inds),support_logMstar=[float(g[j]) for j in sorted(inds)])
result['h']=h;result['LMG']=g.tolist();result['source_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
path=pathlib.Path(__file__).with_name('lens_support.json');path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['LMG']},indent=2))
