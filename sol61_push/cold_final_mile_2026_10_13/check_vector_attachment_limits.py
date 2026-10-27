"""CE-FM-074: local cone identity versus vacuum and isolated-energy limits."""
import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
E,a,kp,kt=s.symbols('E a k_parallel k_perp',positive=True)
D=E**2/(E+a);Le=E**2/2-a*E+a*a*s.log(1+E/a)
checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
ck('vector L derivative gives declared D',s.simplify(s.diff(Le,E)-D)==0)
A=D/E;B=s.diff(D,E);c2=s.simplify(B/A);v2=s.simplify(A/B)
ck('reported special-mode reciprocal',s.simplify(c2*v2)==1)
ck('reported law slopes',s.simplify(c2-(E+2*a)/(E+a))==0)
scalar=kt**2+c2*kp**2;vector=kp**2+v2*kt**2
ck('angular dispersion relation differs by scale',s.simplify(scalar-c2*vector)==0)
ck('same-direction phase speeds not reciprocal in general',s.simplify((scalar*vector/(kp**2+kt**2)**2)-1)!=0)
ck('electric quadratic coefficient vanishes in vacuum',s.limit(B,E,0,dir='+')==0)
ck('magnetic/transverse coefficient vanishes in vacuum',s.limit(A,E,0,dir='+')==0)
ck('cubic rather than quadratic vacuum L',s.limit(Le/E**3,E,0,dir='+')==1/(3*a))
ck('finite speed ratio does not supply vacuum kinetic term',s.limit(v2,E,0,dir='+')==s.Rational(1,2))
H=s.simplify(E*D-Le);ck('positive-energy electric Hamiltonian derivative',s.simplify(s.diff(H,E)-E*B)==0)
ck('Hamiltonian cubic at small field',s.limit(H/E**3,E,0,dir='+')==2/(3*a))
# Gauss D=Q/(4pi r²); exact exterior field at nonzero net charge.
r,Q=s.symbols('r Q',positive=True);d=Q/(4*s.pi*r*r);er=(d+s.sqrt(d*d+4*a*d))/2
# Leading term avoids cancellation in symbolic H(E) near infinity.
ck('Gauss tail E~sqrt(aQ/4pi)/r',s.simplify(s.limit(r*er,r,s.oo)-s.sqrt(a*Q/(4*s.pi)))==0)
coef=s.simplify(4*s.pi*2/(3*a)*(a*Q/(4*s.pi))**s.Rational(3,2))
ck('positive energy per logarithmic radius',s.simplify(coef-s.sqrt(a)*Q**s.Rational(3,2)/(3*s.sqrt(s.pi)))==0)
# Stable numerical tail check in units a=1, Q=4pi: D=1/r² and H~2/(3r³).
def energyH(ee):
 # E D - L = E^3/(1+E) + E - E²/2 - ln(1+E).
 if ee<.01:return sum(((-1)**(n+1))*(n-1)/n*ee**n for n in range(3,15))
 return ee**3/(1+ee)+ee-ee*ee/2-math.log1p(ee)
def perlog(rr):
 dd=1/rr**2;ee=(dd+math.sqrt(dd*dd+4*dd))/2
 return 4*math.pi*rr**3*energyH(ee)
# Taylor sign: H=sum_{n>=3} (-1)^(n+1)(n-1)/n E^n.
for rr in [100,1000,10000]:ck('positive tail approaches8pi/3 at r'+str(rr),abs(perlog(rr)/(8*math.pi/3)-1)<.02)
# A Maxwell regulator epsilon>0 repairs quadratic vacuum energy, changes weak static law.
eps=s.symbols('epsilon',positive=True);Dr=eps*E+D;Lr=eps*E**2/2+Le
ck('Maxwell regulator restores vacuum Hessian',s.limit(s.diff(Dr,E),E,0,dir='+')==eps)
ck('Maxwell regulator changes zero-field D/E',s.limit(Dr/E,E,0,dir='+')==eps)
# At epsilon<1, equality of the two displacement terms is E=epsilon a/(1-epsilon).
xc=eps*a/(1-eps)
ck('exact positive-regulator crossover',s.simplify((eps*E-D).subs(E,xc))==0)
# Lab dt for scalar cone diag(-1,1,1,c²), boosted along its axis.
v=s.symbols('v',real=True);gtt=(-1+c2*v*v)/(1-v*v)
ck('boosted time covector condition',s.simplify(gtt*(1-v*v)-(-1+c2*v*v))==0)
margin=299792.458/(math.sqrt(2)*4700)
old=json.loads(Path('argon_push/ARGON10_four_gaps_2026-10-16/argon10_gravity_results.json').read_text())
ck('source local criterionB margin reproduced',abs(margin-old['margin_bullet'])<1e-12)
result={'claim_id':'CE-FM-074','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'source_criterionB_margin':margin,'isolated_tail_energy_per_ln_r_units_a1_Q4pi':{'r100':perlog(100),'r1000':perlog(1000),'r10000':perlog(10000),'limit':8*math.pi/3},'scope':'Classical source-side Lorentz L(F) with exact D(E)=E²/(E+a), positive electric branch, nonzero net Gauss charge, flat asymptotic exterior. Not a proof of ill-posedness of all degenerate nonlinear equations or rejection of phase/composite/compensated constructions; no full scalar/quantum or GR completion derived.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
