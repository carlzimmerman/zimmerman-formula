import argparse,json,mpmath as m
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
R={'roots':[],'curvature':[],'scope':'External fixed A; no stiffness/metric/clock constraints. Not a physical instability verdict.'}
for bn,bd in [(1,3),(2,3),(9,10)]:
 roots=[]
 for prec in [40,80]:
  with m.workdps(prec):
   b=m.mpf(bn)/bd;xi=m.mpf('.5')/(1+b);K=4*m.pi
   F=lambda t:2*K/xi+2*m.log1p(t)-t-t/(1+t)
   lo=m.mpf('1e-6');hi=m.mpf('1e6');assert F(lo)>0>F(hi)
   for _ in range(prec*4):
    mid=(lo+hi)/2
    if F(mid)>0:lo=mid
    else:hi=mid
   roots.append((lo+hi)/2)
   if prec==80:R['roots'].append(dict(beta=float(b),A_over_a=float(roots[-1]),precision_error=float(abs(roots[-1]-roots[0])/(1+abs(roots[-1]))),Uaa_at_min=float(roots[-1]**3/(K*(1+roots[-1])**2))))
 for ys in ['.1','1','3']:
  for ss in [1,100,10000]:
   pair=[]
   for prec in [40,80]:
    with m.workdps(prec):
     b=m.mpf(bn)/bd;xi=m.mpf('.5')/(1+b);K=4*m.pi;q=(1-b)/b;B=2*m.sqrt(3*(1-b))/(3*b)
     phi=B*m.mpf(ys);V=lambda x:m.sinh(x/B)**(-2*q);a=lambda x:m.sqrt(xi*V(x))
     A=ss*a(phi);p=a(phi)*A/(a(phi)+A)
     W=lambda x,pp:a(x)**2/K*(-pp/a(x)-m.log1p(-pp/a(x)))
     U=lambda x:V(x)+a(x)**2/K*(m.log1p(A/a(x))-A/a(x))
     u=p/a(phi);sch=m.diff(V,phi,2)+m.diff(lambda x:W(x,p),phi,2)-(-u*u*m.diff(a,phi)/(K*(1-u)**2))**2/(1/(K*(1-u)**2))
     direct=m.diff(U,phi,2);pair.append(direct/V(phi))
     if prec==80:R['curvature'].append(dict(beta=float(b),y=float(m.mpf(ys)),s=ss,curvature_over_V=float(pair[-1]),identity_error=float(abs(sch-direct)/(1+abs(direct))),precision_error=float(abs(pair[1]-pair[0])/(1+abs(pair[1])))))
R['checks']={'root_precision':all(x['precision_error']<1e-25 for x in R['roots']),'positive_minimum':all(x['Uaa_at_min']>0 for x in R['roots']),'curvature_precision':all(x['precision_error']<1e-25 for x in R['curvature']),'schur_identity':all(x['identity_error']<1e-25 for x in R['curvature'])}
# With reversed source, derivative W_p+A/K is strictly positive on p>=0.
R['mutation']='Reversed source: W_p+A/K>0 for p>=0,A>0; no positive interior p stationary point.'
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(R,indent=2));print(json.dumps({'roots':R['roots'],'checks':R['checks'],'negative_curvatures':sum(x['curvature_over_V']<0 for x in R['curvature'])},indent=2))
assert all(R['checks'].values())
