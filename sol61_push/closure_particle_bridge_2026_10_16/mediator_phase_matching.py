"""Tree-level renormalizable two-scalar host completion; vacuum proof algebra
and exact finite-density matching. No loop or phase-response UV matching.
"""
import json,sys,math
from pathlib import Path
import sympy as s
import numpy as np
from scipy.optimize import brentq
out=Path(sys.argv[1]);assert out.is_dir();checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
M,x,I=s.symbols('M x I',positive=True);chi=s.symbols('chi',real=True)
L=2-1/M;a=2*M;mu=-3*M/8
U=M*M*chi*chi/2+mu*chi**3/3+chi**4/4
V=I+L*I*I+a*chi*I+U
check('positive-chi vacuum square',s.simplify(U-chi*chi*((chi-M/4)**2/4+s.Rational(31,64)*M*M))==0)
Ux=s.expand(U.subs(chi,-x))
reduced=s.expand(4*L*Ux-(2*M*x-1)**2)
proof=M*x*((L/2)*x*x-2*x+4)+L*x**4-1
check('negative-chi minimized potential identity',s.simplify(reduced-proof)==0)
check('vacuum bounding quadratic',s.simplify((L/2*x*x-2*x+4)-(L/2*(x-2/L)**2+4-2/L))==0)
# General expansion, evaluated for this family only after algebra verification.
z,mm,aa,nu,lc,lp=s.symbols('z m2 a mu lambda_chi lambda_Psi',real=True)
c1=-aa/mm;c2=-nu*aa*aa/mm**3
chiexp=c1*I+c2*I*I
Vgen=z*I+lp*I*I+aa*chi*I+mm*chi*chi/2+nu*chi**3/3+lc*chi**4/4
series=s.series(Vgen.subs(chi,chiexp),I,0,4).removeO()
expected=z*I+(lp-aa*aa/(2*mm))*I*I-nu*aa**3/(3*mm**3)*I**3
check('tree elimination sextic matching',s.simplify(series-expected)==0)
# Strictly increasing coexistence polynomial has one positive root for M>=1.
P=s.expand(L*(M*M+s.Rational(3,8)*M*x+x*x)**2-4*M*M*(M*M/2+M*x/8+x*x/4))
expectedP=L*x**4+3*L*M*x**3/4+(s.Rational(137,64)*L-1)*M*M*x*x+(3*L/4-s.Rational(1,2))*M**3*x-M**3
check('coexistence monotone polynomial',s.simplify(P-expectedP)==0)
rows=[]
for mass in (1.,10.,100.,1000.):
 ell=2-1/mass;aa=2*mass;nu=-3*mass/8
 def usea(xx):return .5*mass*mass*xx*xx+mass*xx**3/8+xx**4/4
 # Rescale polynomial by M^3 to avoid near-cancelling M^4 terms.
 def poly(xx):return ell*xx**4/mass**3+3*ell*xx**3/(4*mass**2)+(137*ell/64-1)*xx*xx/mass+(3*ell/4-.5)*xx-1
 xx=brentq(poly,0,4,xtol=1e-14,rtol=1e-14)
 density=math.sqrt(usea(xx)/ell)
 w2=1+2*ell*density-aa*xx
 # Independent minimized ratio evaluation; cancellation O(M) remains tolerable up to1000.
 ratio=1+ell*density-aa*xx+usea(xx)/density
 check('coexistence ratio '+str(mass),abs(ratio-w2)<2e-11)
 check('frequency interval '+str(mass),0<w2<1)
 check('mediator stationarity '+str(mass),abs((mass*mass*xx+3*mass*xx*xx/8+xx**3)/(aa*density)-1)<1e-12)
 # Canonically normalized real host-amplitude and real mediator mass matrix,
 # at fixed omega (phase fluctuations excluded).
 H=np.array([[4*ell*density,math.sqrt(2)*aa*math.sqrt(density)],
             [math.sqrt(2)*aa*math.sqrt(density),mass*mass+3*mass*xx/4+3*xx*xx]])
 eig=np.linalg.eigvalsh(H)
 check('fixed-frequency homogeneous amplitude curvature '+str(mass),float(eig[0])>0)
 # Exact constrained mediator branch is unique: U''=M²+2mu chi+3chi²>0 globally.
 expansion_rows=[]
 for fraction in (.01,.1,.5,1.):
  ii=density*fraction
  exact=brentq(lambda cc:mass*mass*cc+nu*cc*cc+cc**3+aa*ii,-4*ii/mass-1,0,xtol=1e-14,rtol=1e-14)
  exactV=ii+ell*ii*ii+aa*exact*ii+.5*mass*mass*exact**2+nu*exact**3/3+exact**4/4
  approxV=ii-ii*ii/mass+ii**3/mass**2
  expansion_rows.append({'I_fraction_of_exact_phase':fraction,'I':ii,'chi_exact':exact,
    'chi_over_M':exact/mass,'V_exact':exactV,'V_sextic':approxV,'relative_potential_error':(approxV-exactV)/exactV})
  # Compare derivatives independently against the series: shape is load-bearing.
  check('convex mediator branch '+str((mass,fraction)),mass*mass+2*nu*exact+3*exact*exact>0)
 rows.append({'M_over_m':mass,'lambda_Psi':ell,'a_over_M':2.,'mu_over_M':-.375,
   'lambda_eff_attractive':1/mass,'g6_matched':1/mass**2,'phase_negative_chi':xx,
   'phase_I_exact':density,'phase_I_sextic':mass/2,'phase_I_fractional_shift':density/(mass/2)-1,
   'omega_squared_exact':w2,'omega_squared_sextic':.75,'phase_frequency_squared_shift':w2-.75,
   'amplitude_masses_squared':eig.tolist(),'phase_chi_over_M':xx/mass,
   'amplitude_kinetic_factor_exact':1+2*density*aa*aa/(mass*mass+3*mass*xx/4+3*xx*xx)**2,
   'amplitude_kinetic_factor_leading':1+8*density/(mass*mass),
   'tree_quartic_cancellation_fraction':1/(2*mass),'expansion_rows':expansion_rows,
   'phase_EFT_potential_error_below_one_percent':bool(abs(expansion_rows[-1]['relative_potential_error'])<.01)})
result={'claim':'Classical globally stable vacuum for all M>=1 in selected two-scalar family; exact charge-carrying coexistence branch, tree sextic matching and finite EFT comparison','parameters':'m_h=1;lambda_Psi=2-1/M,a=2M,mu=-3M/8,lambda_chi=1; canonical complex Psi and real chi; I=|Psi|²','checks':checks,'rows':rows,
 'non_claims':['Tree-level renormalizability and bounded classical vacuum are not an all-energy UV completion or quantum vacuum certificate','No loops/beta functions, protected cancellation, portal abundance or mediator thermal history','No matching of the phase-switching W to this mediator or the nodal fermion medium','No inheritance of prior sextic droplet profiles, charge, full radial/metric stability or empirical gates']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'controls':len(checks),'rows':[{k:v for k,v in row.items() if k!='expansion_rows'} for row in rows]},indent=2))
