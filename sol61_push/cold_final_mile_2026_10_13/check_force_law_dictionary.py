"""CE-FM-057: exact force-law dictionary, false shell edge and sphere domain."""
import json,sys,math
from pathlib import Path
import sympy as s
u,x,z=s.symbols('u x z',positive=True)
checks=[]
def exact(name,e):
    assert s.simplify(e)==0,(name,e)
    checks.append(name)
# a0=1. u=g_b/a0. z=g_ph/a0. Exact canonical total g/a0=u+z.
zcan=2*u/(s.sqrt(u*u+4*u)+u)
zquad=s.sqrt(u*u+u)-u
exact('canonical simple-mu equation',(u+zcan)**2-u*(u+zcan)-u)
exact('quadratic comparison equation',(u+zquad)**2-u*u-u)
exact('canonical high baryon saturation',s.limit(zcan,u,s.oo)-1)
exact('quadratic high baryon saturation',s.limit(zquad,u,s.oo)-s.Rational(1,2))
# General spherical enclosed fraction f, point source f=1 gives u=1/x^2.
f=s.symbols('f',positive=True)
Rcan=s.sqrt(f)*2/(s.sqrt(u+4)+s.sqrt(u))
Rquad=s.sqrt(f)/(s.sqrt(u+1)+s.sqrt(u))
exact('canonical force proxy identity',s.sqrt(f/u)*zcan-Rcan)
exact('quadratic force proxy identity',s.sqrt(f/u)*zquad-Rquad)
mc=(s.sqrt(1+4*x*x)-1)/2
Rpoint=mc/x
Rother=(s.sqrt(1+x*x)-1)/x
exact('canonical half-amplitude crossing',Rpoint.subs(x,s.Rational(2,3))-s.Rational(1,2))
exact('quadratic half-amplitude crossing',Rother.subs(x,s.Rational(4,3))-s.Rational(1,2))
exact('canonical mass central limit',s.limit(mc/x**2,x,0)-1)
exact('mass deep constant term',s.limit(mc-x,x,s.oo)+s.Rational(1,2))
exact('canonical positive inner mass',mc.subs(x,s.Rational(1,2))-(s.sqrt(2)-1)/2)
# Canonical residual force relation u_b=z^2/(1-z) restricts 0<z<1.
exact('positive sub-saturation gap',1-zcan-2/(u+2+s.sqrt(u*u+4*u)))
G=6.67430e-11;a0=9.3603e-11;ratio=5.364
M=1000.;rM=math.sqrt(G*M/a0);Re=rM*math.sqrt(ratio+ratio*ratio)
ck=(lambda name,v:(checks.append(name) if v else (_ for _ in ()).throw(AssertionError(name))))
ck('tonne edge exceeds rM',Re>5*rM)
Mneed=9.8**2/(G*a0);gb=G*Mneed
# Stable expression avoids cancellation at huge gb/a0.
z_eval=2/(math.sqrt(1+4*a0/gb)+1)
actual=a0*z_eval
ck('requested 1g is outside exact phantom range',9.8/a0>1e10)
ck('exact phantom is saturated not deep1g',abs(actual/a0-1)<1e-12)
ck('deep mass lies at tiny r/rM',1/math.sqrt(G*Mneed/a0)<1e-10)
rows=[]
for xx in [.1,.3,.62,2/3,1,4/3,5.842644606682833]:
    m=(math.sqrt(1+4*xx*xx)-1)/2
    rows.append({'r_over_rM':xx,'M_c_over_Mb':m,'canonical_force_proxy':m/xx,'quadratic_force_proxy':xx/(math.sqrt(1+xx*xx)+1)})
# Raw AG3 summaries remain data/algorithm results; do not recompute or regrade.
b=Path('argon_push/AG3_sparc_annulus_widths');ag=json.loads((b/'ag3_sparc_widths_results.json').read_text())
res={'claim_id':'CE-FM-057','checks_passed':len(checks),'checks':checks,'canonical_point_crossing':2/3,'quadratic_point_crossing':4/3,'profile_controls':rows,'tonne_rM_m':rM,'tonne_supply_edge_m':Re,'reported_1g_mass_kg':Mneed,'exact_phantom_at_reported_mass_m_s2':actual,'r_over_rM_for_reported_1g_mass':1/math.sqrt(G*Mneed/a0),'AG3_preserved_K2b':ag['K2b'],'AG3_preserved_B2':ag['B2'],'scope':'Exact algebra/domain audit only; no SPARC/lensing rerun or new observed exclusion, sphere activation or halo existence proof.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
