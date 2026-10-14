import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
b,c,d,eta,J,a=s.symbols('b c D eta J a',positive=True)
B=b-d/(1+eta);C=c-eta*d/(1+eta)
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
ze('total pressureless mass independent of source partition',B+C-(b+c-d))
ze('partitioned matter-to-vacuum transfer cancels',-J/(1+eta)-eta*J/(1+eta)+J)
ze('fixed primordial ratio iff proportional transfer',(C/B-c/b).subs(eta,c/b))
ze('same fractional survival for proportional transfer',(B/b-C/c).subs(eta,c/b))
ze('proportional survival', (B/b).subs(eta,c/b)-(1-d/(b+c)))
ze('total Friedmann density unchanged',((B+C)/a**3)-((b+c-d)/a**3))
src=json.loads(Path('sol61_push/claude_bh_followthrough_2026_10_14/run_v1/results.json').read_text())
rows=[]
for zcase in [src['primary']]+src['zstart_sensitivity']:
 b0=zcase['Omega_b_projected'];c0=zcase['Omega_c_projected'];loss=b0-zcase['Omega_b_today'];R=c0/b0
 for tag,ee in [('baryons only',0),('proportional cold and baryons',R),('cold only',None)]:
  fb=0 if ee is None else 1/(1+ee)
  bb=b0-fb*loss;cc=c0-(1-fb)*loss
  ck('positive stocks '+str((zcase['z_start'],tag)),bb>0 and cc>0)
  ck('same background '+str((zcase['z_start'],tag)),abs(bb+cc-(b0+c0-loss))<1e-14)
  if tag.startswith('proportional'):ck('ratio retained '+str(zcase['z_start']),abs(cc/bb-R)<1e-12)
  rows.append({'z_start':zcase['z_start'],'transfer':tag,'fraction_of_converted_mass_from_baryons':fb,'baryon_survival':bb/b0,'cold_survival':cc/c0,'cold_over_baryon_today':cc/bb,'Xi_baryonic_share':fb*zcase['Xi_shot'],'Xi_cold_share':(1-fb)*zcase['Xi_shot'],'H_and_DE_history':'identical to corresponding conserved background; only source partition changes'})
j={'passed':len(checks),'checks':checks,'rows':rows,'interpretation':'Background degeneracy and necessary source/abundance accounting. Proportional co-conversion is an additional physical hypothesis, not a BH capture or vacuum-production mechanism. CMB ratio is assumed, not derived. Baryon-only published model is not silently replaced.'}
(out/'results.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
