"""Classical-limit scaling of actual mediator host; loop-sensitivity repair
at the cost of increased conserved inventory. No abundance/UV guarantee.
"""
import json,sys,math
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
p=json.loads((base/'four_gap_audit_run_003/results.json').read_text())
checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
I,J,x,X,eps,L,a,B,mu,l,m2=s.symbols('I J x X eps L a B mu l m2',positive=True)
V=m2*I+L*I**2+a*x*I+B*x*x/2+mu*x**3/3+l*x**4/4
Ve=m2*I+eps*L*I**2+s.sqrt(eps)*a*x*I+B*x*x/2+s.sqrt(eps)*mu*x**3/3+eps*l*x**4/4
check('exact rescaled potential',s.simplify(eps*Ve.subs({I:J/eps,x:X/s.sqrt(eps)})-V.subs({I:J,x:X}))==0)
net=L-a*a/(2*B)
nete=eps*L-(s.sqrt(eps)*a)**2/(2*B)
check('net quartic scales epsilon',s.simplify(nete-eps*net)==0)
beta=20*L*L-8*L*a*a/B+a*a*(2*a*a+6*B*l+4*mu*mu)/(2*B*B)
sub={L:eps*L,a:s.sqrt(eps)*a,mu:s.sqrt(eps)*mu,l:eps*l}
check('net beta scales epsilon squared',s.simplify(beta.subs(sub,simultaneous=True)-eps**2*beta)==0)
bm=8*L*m2+2*a*a
check('mass beta scales epsilon',s.simplify(bm.subs(sub,simultaneous=True)-eps*bm)==0)
rad=m2+6*L*I+a*x
check('same classical radial Hessian',s.simplify(rad.subs(sub,simultaneous=True).subs({I:J/eps,x:X/s.sqrt(eps)})-rad.subs({I:J,x:X}))==0)
source=next(r for r in p['quantum_rows'] if r['M_over_m']==100)
rows=[]
for e in (1.,1e-3,1e-6):
 b=source['beta_net_quartic_MS']*e*e;tree=-e/100
 rows.append({'M_over_m':100,'epsilon':e,'a_over_M':2*math.sqrt(e),'lambda_Psi':1.99*e,
  'net_quartic':tree,'beta_net_quartic_MS':b,'one_log_quartic_shift_relative_tree':abs(b/tree),
  'one_log_mass_squared_shift_relative_tree':source['beta_host_mass_squared_over_m2']*e,
  'charge_and_energy_factor_for_same_classical_shape':1/e,
  'field_amplitude_factor_for_same_classical_shape':1/math.sqrt(e),
  'one_log_diagnostic_both_below_one_percent':bool(abs(b/tree)<.01 and source['beta_host_mass_squared_over_m2']*e<.01)})
r={'checks':checks,'rows':rows,'non_claims':['One-log MS sensitivity estimates, not full finite matching or quantum vacuum proof','Classical inventory scaled not derived from neutral production; gravity/backreaction and cosmological abundance must be recomputed','Response W and all portals must be matched/scaled separately; no old empirical score inherited','Large classical field amplitudes require control of additional operators in any higher UV theory']}
(out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
