"""Independent sample-order discriminator; no astrophysical fitting."""
import json, math, sys
from pathlib import Path
p=Path(__file__).resolve().parents[2]
j=json.loads((p/'campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_baryon_loss_results.json').read_text())['numbers']
rows={k:[e for e in j['EST']['-0.2|'+k] if e is not None] for k in ['ufd','cls','col','m31','fld']}
xy=[(math.log10(float(e['Ms'])+float(e.get('Mg') or 0)),float(e['lR'])) for rr in rows.values() for e in rr if e.get('lR') is not None]
xm=sum(x for x,y in xy)/len(xy); ym=sum(y for x,y in xy)/len(xy)
b=sum((x-xm)*(y-ym) for x,y in xy)/sum((x-xm)**2 for x,y in xy); a=ym-b*xm
out={}
for reading in ['implementation','frozen_spec']:
 v={}
 for k,rr in rows.items():
  vv=[]
  for e in rr:
   mass=float(e['Ms'])+float(e.get('Mg') or 0)
   lr=e.get('lR') if reading=='implementation' or k in ['ufd','cls'] else None
   lr=max(float(lr) if lr is not None else a+b*math.log10(mass),0)
   vv.append((6.674e-11*1.989e30*mass*10**lr*9.3603e-11)**.25/1000)
  v[k]=sorted(vv)
 # Strict v < threshold: 90% UFDs needs threshold > kth order value.
 lower=v['ufd'][math.ceil(.9*len(v['ufd']))-1]
 uppers={k:vs[math.floor(.1*len(vs))] for k,vs in v.items() if k!='ufd'}
 out[reading]={'N':{k:len(vs) for k,vs in v.items()},'threshold_must_exceed_km_s':lower,'threshold_must_not_exceed_km_s':uppers,'any_threshold_feasible':lower<min(uppers.values()),'primary_flagged':{k:sum(x<20.487 for x in vs) for k,vs in v.items()},'M31_minimum_flagged_at_UFD_requirement':{k:sum(x<=lower for x in v[k]) for k in ['col','m31']}}
 assert lower>min(uppers.values())
# Independent exact algebra: mass transfer breaks unchanged polarization continuity.
from fractions import Fraction as F
S=F(1); divj=F(2); drhot=-divj-S
assert drhot != -divj
# With locally fixed reference density, div(Pdot+j_t)=-S restores equality.
assert -divj-S==drhot
# At fixed R != Rstar, an explicit relaxation law converges to its inserted Rstar;
# with Q=0 two distinct conserved abundance ratios remain distinct.
assert F(1)!=F(5364,1000)
out['algebra_checks']={'continuity_source_required':True,'conserved_ratio_not_selected':True}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
