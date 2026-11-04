"""Inclusive-channel and external-leg audit for the ordinary decay matching."""
import os,sys,json,math,time,resource
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np
from matching import model,parent,coefficients,amplitude,ROOT
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import B0

def selfenergy(data,ext,xi=1.,uv=0.):
 d=data['d'];U=data['U'];m=d['mF'];ms=d['mS2'].copy();ms[data['gold']]=xi*max(d['mV2']);ms=np.maximum(ms,0)
 Y=np.einsum('Ia,JK,IJs->aKs',ext,U,data['dy'],optimize=True)
 G=d['g']*np.einsum('rv,Ia,rIJ,JK->vaK',d['Ov'],ext.conj(),data['RF'],U,optimize=True)
 bs=np.array([[B0(float(mf*mf),float(ma),1.)+uv for ma in ms] for mf in m])
 bv=np.array([[3*(B0(float(mf*mf),float(mv),1.)+uv)+xi*(B0(float(mf*mf),float(xi*mv),1.)+uv) for mf in m] for mv in d['mV2']])
 s=-np.einsum('aIs,bIs,Is,I->ab',Y,Y,bs,m,optimize=True)/(16*math.pi**2)
 v=-np.einsum('vaI,vbI,vI,I->ab',G.conj(),G.conj(),bv,m,optimize=True)/(16*math.pi**2)
 return s+v,Y,G

def main(out):
 start=time.monotonic();data=model();d=data['d'];gold=np.r_[d['F'].conj(),np.zeros(24)];gold/=np.linalg.norm(gold)
 ex=np.column_stack([data['ext'],data['U'],gold]);sg,Yg,Gg=selfenergy(data,ex,1.);sg2,_,_=selfenergy(data,ex,2.);uv,_,_=selfenergy(data,ex,1.,uv=1.)
 # Endpoint index 12+73 is the normalized tree Goldstino.
 gold_index=85;rows=[]
 eta=np.einsum('aij,aji->a',__import__('matching').T.transpose(0,2,1),__import__('matching').T).real
 cc=np.r_[1.,eta,eta];cf=np.r_[cc,-eta];cs=np.r_[cc,cc]
 sym=dict(background=float(np.max(abs(cc*d['z']-d['z']))),
  superpotential_tensor=float(np.max(abs(d['Y']*(cc[:,None,None]*cc[None,:,None]*cc[None,None,:]-1)))),
  fermion_mass=float(np.max(abs(cf[:,None]*d['MF']*cf[None,:]-d['MF']))),
  scalar_hessian=float(np.max(abs(cs[:,None]*d['H']*cs[None,:]-d['H']))),
  Goldstino_even=float(np.max(abs(cf*gold-gold))))
 for r,R in enumerate(d['R']):
  err=float(np.max(abs(cc[:,None]*R*cc[None,:]+eta[r]*R)))
  sym['gauge_intertwining']=max(sym.get('gauge_intertwining',0),err)
 for name in ('S8_0','S3_0'):
  p=parent(data,name);b=p['b'];ypold=np.einsum('IJs,s->IJ',data['dy'],p['weights'])
  tree_fixed_chi=np.linalg.norm(ypold@data['ext'][:,11]);tree_gold=float(abs(data['ext'][:,b].T@ypold@gold))
  nz=d['mF']>1e-10;mix=sg[b,12:85];mix2=sg2[b,12:85]
  y_to_gold=data['U'].T@ypold@gold;y_to_lambda=data['U'].T@ypold@data['ext'][:,b]
  # Leading massless-external eigenvector perturbation; chirality-preserving
  # mixing multiplies slash(p) u=0 and drops out at this order.
  leg_lambda=-np.sum(mix[nz]/d['mF'][nz]*y_to_gold[nz])
  leg_gold=-np.sum(sg[gold_index,12:85][nz]/d['mF'][nz]*y_to_lambda[nz])
  datum=dict(data);datum['Y']=Yg;datum['G']=Gg
  terms=coefficients(datum,p,a=b,b=gold_index,charged_only=False)
  direct=[]
  for xi in (1.,2.):
   parts=amplitude(datum,p,terms,xi);z=sum(parts.values());legs=leg_lambda+leg_gold if xi==1 else -np.sum(mix2[nz]/d['mF'][nz]*y_to_gold[nz])-np.sum(sg2[gold_index,12:85][nz]/d['mF'][nz]*y_to_lambda[nz])
   direct.append(dict(xi=xi,triangle_parts={k:[v.real,v.imag] for k,v in parts.items()},triangle=[z.real,z.imag],external_legs=[legs.real,legs.imag],total=[(z+legs).real,(z+legs).imag],width=p['mass']/(8*math.pi)*abs(z+legs)**2))
  extra=None
  if name=='S8_0':
   tt=coefficients(data,p,a=0,b=0,charged_only=False);z=sum(amplitude(data,p,tt).values());alt=sum(amplitude(data,p,tt,xi=2).values())
   pattern=[]
   from matching import fundamental_basis
   ts=fundamental_basis()
   d0=4*np.trace(ts[7]@ts[0]@ts[0]).real
   for pair in (2,6,7):
    zz=sum(amplitude(data,p,coefficients(data,p,a=pair,b=pair,charged_only=False)).values());dd=4*np.trace(ts[7]@ts[pair]@ts[pair]).real
    pattern.append(dict(index=pair,amplitude=[zz.real,zz.imag],d_ratio=dd/d0,relative_error=abs(zz/z-dd/d0)))
   extra=dict(y_11=[z.real,z.imag],inclusive_SU3_SU3_width=5*p['mass']/(16*math.pi)*abs(z)**2,gauge_relative_error=abs(alt/z-1),color_pattern=pattern)
  rows.append(dict(id=name,tree_fixed_chi_all_fermion_norm=float(tree_fixed_chi),tree_lambda_gold=tree_gold,
   lambda_to_massive_mixing_norm=float(np.linalg.norm(mix[nz])),lambda_to_massive_mixing_UV_norm=float(np.linalg.norm((uv-sg)[b,12:85][nz])),
   Goldstino_selfenergy_mass=[sg[gold_index,gold_index].real,sg[gold_index,gold_index].imag],
   lambda_leg=[leg_lambda.real,leg_lambda.imag],Goldstino_leg=[leg_gold.real,leg_gold.imag],Goldstino_cases=direct,other_gaugino=extra))
  print(name,'mix',rows[-1]['lambda_to_massive_mixing_norm'],'Gold total',direct,flush=True)
 checks=dict(charge_conjugation_symmetry=max(sym.values())<1e-12,Goldstino_selection_remainder=max(abs(complex(*c['total'])) for s in rows for c in s['Goldstino_cases'])<1e-20,
  unbroken_lambda_chiral_mass_mixing=max(s['lambda_to_massive_mixing_norm'] for s in rows)<1e-18,
  octet_extra_gauge=rows[0]['other_gaugino']['gauge_relative_error']<1e-8,
  octet_color_tensor=max(t['relative_error'] for t in rows[0]['other_gaugino']['color_pattern'])<1e-8)
 checks={k:bool(v) for k,v in checks.items()}
 result=dict(claim_id='CC11_DECAY_GOLDSTINO_AND_LEG_AUDIT',states=rows,checks=checks,unitary_charge_conjugation_controls=sym,Goldstino_tree_null_error=float(np.max(abs(d['MF']@gold))),runtime_seconds=time.monotonic()-start,
  peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Ordinary massless-external one-loop triangle plus chirality-flipping external-leg audit; Goldstino/background/gravity conditions must be reviewed before inclusive branching.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
