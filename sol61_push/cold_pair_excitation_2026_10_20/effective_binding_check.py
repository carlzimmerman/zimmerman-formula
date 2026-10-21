"""Tiny algebra/arithmetic audit of the explicit alternative-action binding clue.
No stationary/PDE/eigenvalue solve and no theory-completion claim.
"""
from pathlib import Path
import json,math,resource,sys
import numpy as np
import sympy as s
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1]);checks=[]
def ck(name,value): checks.append({'name':name,'pass':bool(value)})
P=json.loads((ROOT/'sol61_push/cold_completion_2026_10_20/run_001/results.json').read_text())['parameters']
t,z,I,M,a,c2,c3=s.symbols('t z I M a c2 c3',positive=True)
ansatz=-t+c2*t**2+c3*t**3
eq=s.series(ansatz-s.Rational(3,8)*ansatz**2+ansatz**3+t,t,0,4).removeO().expand()
sol=s.solve([eq.coeff(t,2),eq.coeff(t,3)],[c2,c3]);zs=s.expand(ansatz.subs(sol))
w=s.series(zs**2/2-zs**3/8+zs**4/4+t*zs,t,0,5).removeO().expand()
expected=-t**2/2+t**3/8+s.Rational(23,128)*t**4
ck('exact chi series coefficients',s.expand(w-expected)==0)
ck('chi root series satisfies equation to cubic',s.expand(eq.subs(sol))==0)
chi=s.symbols('chi',real=True)
U=M**2*chi**2/2-M*chi**3/8+chi**4/4
ck('strict convex chi square identity',s.expand(s.diff(U,chi,2)-3*(chi-M/8)**2-s.Rational(61,64)*M**2)==0)
g=s.Rational(271,125000);mx2=s.Rational(2501,625);lam=s.Rational(199,100)+g*g/mx2
physical=s.expand(M**4*w.subs(t,a*I/M**3)).subs({M:100,a:200})
static=s.expand(I+(lam-g*g/mx2)*I**2+physical)
want=I-I**2/100+I**3/10000+s.Rational(23,800000000)*I**4
ck('static X cancellation and all four potential coefficients exact',s.expand(static-want)==0)
ck('pinned parameters agree',abs(P['lambda']-float(lam))<1e-14 and P['MX2']==float(mx2) and P['g']==float(g) and P['M_chi']==100 and P['a']==200)
# Independent local finite point: exact cubic root via bracket, not its Taylor approximation.
M0=100.;a0=200.;I0=50.
fun=lambda h:M0*M0*h-3*M0*h*h/8+h**3+a0*I0
h=brentq(fun,-a0*I0/(M0*M0),0.,xtol=1e-14)
x=-float(g)*I0/float(mx2)
u=.5*M0*M0*h*h-M0*h**3/8+.25*h**4
v=I0+float(mx2)*x*x+2*float(g)*x*I0+float(lam)*I0**2+a0*h*I0+u
vseries=float(static.subs(I,I0));res=fun(h)
ck('I50 exact cubic root residual',abs(res)<1e-8)
ck('I50 sub-rest local potential ratio',0<v/I0<1)
ck('I50 series within one part per thousand of exact value',abs(vseries/v-1)<1e-3)
# Rotating stationary functional, not the physical V: X quadratic changes.
omega,b=s.symbols('omega b',real=True)
r=(1-omega**2)*I+(mx2-4*omega**2)*b*b+2*g*b*I+lam*I**2
bsol=-g*I/(mx2-4*omega**2)
rred=(1-omega**2)*I+(lam-g*g/(mx2-4*omega**2))*I**2
ck('rotating X algebra exact',s.factor(r.subs(b,bsol)-rred)==0)
ck('rotating stationary X derivative zero',s.factor(s.diff(r,b).subs(b,bsol))==0)
channels=[]
for Q in [136000,140000]:
 path=ROOT/f'sol61_push/cold_pair_excitation_2026_10_20/matched_refs_run_004/Q{Q}_L60_N1199.npz'
 with np.load(path) as cache: om=float(cache['omega']);Om=float(cache['Omega'])
 row={'reference_Q':Q,'omega':om,'Omega':Om,'twice_Omega':2*Om,'Psi_reduced_threshold':1-om,'Psi_plus_lab_frequency':om+2*Om,'Psi_plus_k2':(om+2*Om)**2-1,'Psi_minus_k2':(om-2*Om)**2-1,'X_plus_k2':(2*om+2*Om)**2-float(mx2),'chi_k2':(2*Om)**2-M0*M0}
 ck(f'Q{Q} quadratic positive Psi channel open',row['Psi_plus_k2']>0 and 2*Om>1-om)
 ck(f'Q{Q} other displayed matter channels closed',row['Psi_minus_k2']<0 and row['X_plus_k2']<0 and row['chi_k2']<0)
 channels.append(row)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below 1GB',rss<1000000000)
d={'scope':'Exact formal algebra and two local arithmetic/channel checks only; not continuum soliton existence, dynamical formation or radiative rate.','parameters':P,'dimensionless_chi_series':str(zs),'dimensionless_minimum_series':str(w),'static_potential_series':str(static),'local_I50':{'I':I0,'chi':h,'X_real':x,'chi_stationarity_residual':res,'V_effective_exact':v,'V_effective_over_I':v/I0,'V_series':vseries,'relative_series_error':abs(vseries/v-1)},'rotating_stationary_reduction':str(rred),'channels':channels,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),'peak_rss_bytes_macos':rss}
(out/'results.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(d['local_I50']));print(json.dumps({'checks':len(checks),'pass':d['all_checks_pass']}))
raise SystemExit(0 if d['all_checks_pass'] else 1)
