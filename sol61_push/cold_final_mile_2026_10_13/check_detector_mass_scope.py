"""CE-FM-054: dimensions, rate scaling, and conditional detector scope."""
import json,sys,math
from pathlib import Path
import sympy as s
b=Path('argon_push/ARGON03_haloscope_audit_2026-10-15')
a=json.loads((b/'haloscope_audit_results.json').read_text())
checks=[]
def exact(label,v):
    assert s.simplify(v)==0,(label,v)
    checks.append(label)
g,h=s.symbols('g h',real=True)
# Rows M,L,T; columns a0,G,c,hbar,rho_mass.
D=s.Matrix([[0,-1,0,1,1],[1,3,1,2,-3],[-2,-2,-1,-1,0]])
old=s.Matrix([4*g+4*h-3,g,6-10*g-9*h,h,1-g-h])
new=s.Matrix([-3-2*g+4*h,g,6+2*g-9*h,h,1+g-h])
for i,expected in enumerate([1-2*g,0,0]):exact('old exponent dimension '+str(i),(D*old)[i]-expected)
for i,expected in enumerate([1,0,0]):exact('correct exponent dimension '+str(i),(D*new)[i]-expected)
native=s.Matrix([0,0,-s.Rational(3,4),s.Rational(3,4),s.Rational(1,4)])
for i,expected in enumerate([1,0,0]):exact('native dimensional scale '+str(i),(D*native)[i]-expected)
pi=s.Matrix([1,s.Rational(1,2),-s.Rational(7,2),s.Rational(1,2),0])
for i in range(3):exact('dimensionless acceleration group '+str(i),(D*pi)[i])
# Rate scales as coupling squared for any fixed fraction/response/mass.
e=s.symbols('e',positive=True)
N0=s.Integer(44)*10**6
correct_low=N0*(s.Rational(1,10**14)/s.Rational(1,10**12))**2
exact('1e-14 photon rate normalized',correct_low-4400)
rate_hi=a['native_rate_eps1e-12_per_day']; reported_low=a['native_rate_eps1e-14_per_day']
assert math.isclose(reported_low/(rate_hi*1e-4),100,rel_tol=1e-13);checks.append('stored lower-coupling rate overestimated by100')
# Conditional null bound is on e^2*f*C at assigned mass, not e alone.
f,C,Pmax,K=s.symbols('f C Pmax K',positive=True)
ebound=s.sqrt(Pmax/(K*f*C))
exact('null bound with stock and response',K*f*C*ebound**2-Pmax)
G=6.67430e-11;c=2.99792458e8;hb=1.054571817e-34;a0=9.3603e-11;EV=1.602176634e-19
rho=4*a0*a0/(G*c*c)
m=(rho*hb**3/c**3)**.25
energy=m*c*c/EV
assert math.isclose(energy,a['m_native_eV'],rel_tol=1e-6);checks.append('vacuum dimensional energy agrees')
# No carrier equation fixes the coefficient; valid algebraic alternatives.
scales=[{'coefficient':v,'energy_eV':v*energy} for v in [.1,1,10]]
res={'claim_id':'CE-FM-054','checks_passed':len(checks),'checks':checks,'old_dimension_vector':['1-2*g','0','0'],'correct_exponents':{'a0':'-3-2*g+4*h','G':'g','c':'6+2*g-9*h','hbar':'h','rho':'1+g-h'},'vacuum_scale_eV':energy,'stored_rate_at_eps1e_12':rate_hi,'stored_rate_at_eps1e_14':reported_low,'correct_rate_at_eps1e_14':rate_hi*1e-4,'coefficient_control':scales,'scope':'Conditional dimensional/rate audit; no astrophysical bounds authenticated, no physical carrier identification or framework kill.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
