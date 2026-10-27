import json,sys,math
from fractions import Fraction as F
d=json.load(open('campaign_fresh_gravity/CFG779_frb_baryon_survival/cfg779_results.json'));checks=0
for foot in ['canonical','alt']:
 r=d[foot]
 for key in ['P0 (no conversion)','P1 (MD14 conserved, s_b0 0.43)','P2 (Croker-like, s_b0 0.70)']:
  v=r[key];den=r['lnB']-r['p16'] if r['lnB']>v['lnB_pred'] else r['p84']-r['lnB']
  zz=(r['lnB']-v['lnB_pred'])/den
  assert abs(zz-v['Z'])<1e-10;checks+=1
  cl='EXCLUDED' if abs(zz)>=3 else 'TENSION' if abs(zz)>=2 else 'CONSISTENT'
  assert cl==v['cls'];checks+=1
# Exact Gaussian two-sightline surrogate. Full candidate means y_i=a_i B_i.
a=[F(1),F(100)];b=[F(45,100),F(70,100)];y=[aa*bb for aa,bb in zip(a,b)]
proj=sum(aa*yy for aa,yy in zip(a,y))/sum(aa*aa for aa in a)
median=(b[0]+b[1])/2
assert proj!=median;checks+=1
# True model has zero residual; median amplitude has positive residual.
chi=sum((yy-aa*median)**2 for aa,yy in zip(a,y))
assert chi>0;checks+=1
json.dump(dict(checks=checks,gaussian_surrogate=dict(projected_B=str(proj),median_B=str(median),true_model_chi2=0,median_surrogate_chi2=str(chi)),scope='Stored classifier arithmetic and exact counterexample to median being a general likelihood projection; no corrected FRB fit or new observational class'),open(sys.argv[1],'w'),indent=2)
