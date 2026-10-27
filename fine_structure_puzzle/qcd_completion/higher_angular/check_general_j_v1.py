#!/usr/bin/env python3
"""Exact bounded checks of the general-J hand argument; no fitting or ODEs."""
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'runs/general-j-001/results.json'
checks = []

def check(name, value):
    if isinstance(value, s.MatrixBase):
        ok = all(s.simplify(v) == 0 for v in value)
    else:
        ok = bool(value)
    if not ok:
        raise AssertionError(name)
    checks.append(name)

def eps(i, j, k):
    return s.LeviCivita(i, j, k)

# The actual four-vector curvature matrices, not guessed scalar copies.
Imat = []
for a in range(3):
    m = s.zeros(4)
    for i in range(3):
        for j in range(3):
            m[i,j] = eps(i,j,a)
        m[i,3] = -s.KroneckerDelta(i,a)
        m[3,i] = s.KroneckerDelta(a,i)
    Imat.append(m)
sigma = [-s.I*m for m in Imat]
for a in range(3):
    for b in range(3):
        rhs = s.KroneckerDelta(a,b)*s.eye(4)
        rhs += s.I*sum((eps(a,b,c)*sigma[c] for c in range(3)),s.zeros(4))
        check(f'quaternion_Pauli_{a}_{b}', sigma[a]*sigma[b]-rhs)

lam = s.symbols('lam', positive=True)
mu = s.symbols('mu')
kap = s.diag(lam,-lam)
for q in (-1,1):
    w = s.Matrix([[-q/lam,s.sqrt(lam**2-1)/lam],
                  [s.sqrt(lam**2-1)/lam,q/lam]])
    check(f'w_square_q{q}', w*w-s.eye(2))
    check(f'anticommutator_q{q}', kap*w+w*kap+2*q*s.eye(2))
    b = kap+2*q*w
    check(f'Biedenharn_square_q{q}',b*b-lam**2*s.eye(2))
    A = lam**2*s.eye(2)-b
    expected=(mu-lam*(lam-1))*(mu-lam*(lam+1))
    check(f'charged_charpoly_q{q}',s.simplify(A.charpoly(mu).as_expr()-expected)==0)
    # Lowest active k=1/2 space has only kappa=-1,w=q.
    check(f'lowest_branch_q{q}',1-(-1)-2*q*q == 0)

J,x,c = s.symbols('J x c',positive=True)
C=J*(J+1)
charged_c=[(J-1)*J,C,C,(J+1)*(J+2)]*2
neutral_c=[(J-1)*J,C,C,(J+1)*(J+2)]
a1=(2-c)/2
a2=(6-c)*a1/4
# Direct differential residual: the coefficients through x^-3 vanish.
f=1+a1/x+a2/x**2
g=s.exp(x)*f/x
res=s.expand((s.diff(g,x,2)-(1-2/x+c/x**2)*g)*x/s.exp(x))
check('charged_recurrence_through_xminus3',s.simplify(res.coeff(x,-2))==0 and s.simplify(res.coeff(x,-3))==0)
robin=s.expand((s.diff(g,x)+g/x)*x/s.exp(x))
check('charged_Robin_same_a1',s.simplify(robin.coeff(x,-1)-a1)==0)
sum_a1=s.simplify(sum(a1.subs(c,v) for v in charged_c))
check('charged_Casimir_sum',s.simplify(sum(charged_c)-(8*C+4))==0)
check('charged_a1_sum',s.simplify(sum_a1-(6-4*C))==0)

# Neutral mixed trace in the actual radial/electric basis.
d=s.sqrt(2*J+1)
e_minus=s.Matrix([s.sqrt(J),s.sqrt(J+1)])/d
e_plus=s.Matrix([-s.sqrt(J+1),s.sqrt(J)])/d
wall=s.Matrix([[e_minus[1],e_plus[1]],
               [(J+1)*e_minus[0],(J+3)*e_plus[0]]])
wall_det=s.factor(wall.det())
check('neutral_mixed_wall_nonzero_formula',s.simplify(wall_det+(J+1)*(2*J+3)/(2*J+1))==0)
neutral_power=J+(J+1)+(J+1)+(J+2)-1
ref_power=12*(J+1)-3
vec_log_power=s.expand(neutral_power-8-ref_power)
gh_log_power=s.expand((J+1)-2-(3*J+3))
check('vector_log_power',vec_log_power == -8*J-14)
check('ghost_log_power',gh_log_power == -2*J-4)
gaussian_a1=s.simplify((2-C)-sum_a1/2)
check('Gaussian_coefficient',s.simplify(gaussian_a1-(C-1))==0)

population=[]
for j in range(2,21):
    ls=[]
    for k in (0,1,2):
        ls += list(range(abs(j-k),j+k+1))
    ls += list(range(j-1,j+2))
    mult=[ls.count(l) for l in range(j-2,j+3)]
    check(f'origin_counts_J{j}',len(ls)==12 and mult==[1,3,4,3,1])
    check(f'reference_power_J{j}',sum(l+1 for l in ls)-3==12*j+9)
    direct=sum((2*i+1)*(i*(i+1)-1) for i in range(2,j+1))
    closed=s.Rational(1,2)*((j+1)**4-3*(j+1)**2)-2
    check(f'finite_angular_sum_J{j}',direct==closed)
    population.append({'J':j,'origin_l_multiplicity':mult,'coefficient':(2*j+1)*(j*(j+1)-1),'cutoff_sum':int(closed)})

# Independently supplied J1 Cartesian operator: verify its far-field spectrum
# and charge/normal wall commutation against the generic lowest-spin exception.
data=json.loads((ROOT/'inputs_v1/j1_operator.json').read_text())
t,k,h,kp,hp=s.symbols('t k h kp hp')
local={'t':t,'k':k,'h':h,'kp':kp,'hp':hp}
V=s.Matrix([[s.sympify(v,locals=local) for v in row] for row in data['V_raw']])
Vinf=V.subs({k:0,kp:0,h:1-1/t,hp:1/t**2}).applyfunc(s.expand)
M0=Vinf.applyfunc(lambda e:e.coeff(t,0))
M1=Vinf.applyfunc(lambda e:e.coeff(t,-1))
M2=Vinf.applyfunc(lambda e:e.coeff(t,-2))
check('J1_charge_projector',M0*M0-M0)
check('J1_Coulomb_coefficient',M1+2*M0)
check('J1_charge_centrifugal_commute',M0*M2-M2*M0)
N=s.Matrix([[s.sympify(v) for v in row] for row in data['normal_N']])
Z=s.zeros(10,3)
for a,b in ((1,0),(3,1),(5,2)):
    Z[a,b]=1
PN=Z*N
check('J1_normal_projector',PN*PN-PN)
check('J1_charge_normal_commute',M0*PN-PN*M0)
check('J1_charged_count',s.trace(M0)==6)
check('J1_neutral_count',s.trace(s.eye(10)-M0)==4)
check('J1_charged_charpoly',s.factor((M0*M2).charpoly(mu).as_expr()-mu**6*(mu-2)**2*(mu-6)**2)==0)
check('J1_neutral_charpoly',s.factor(((s.eye(10)-M0)*M2).charpoly(mu).as_expr()-mu**7*(mu-2)**2*(mu-6))==0)
check('J1_charged_a1',s.simplify(s.trace(M0)-s.trace(M0*M2)/2)==-2)

# Euler-Maclaurin coefficient calculation for the ANGULAR COEFFICIENT SUM.
# This does not exchange the full determinant's x and angular limits.
e,y=s.symbols('e y')
fy=(2*y+1)*s.exp(-e*y*(y+1))
heat=1/e+s.Rational(1,2)
for m in range(1,5):
    term=s.diff(fy,y,2*m-1).subs(y,0)
    heat-=s.bernoulli(2*m)*term/s.factorial(2*m)
heat=s.series(heat,e,0,3).removeO().expand()
check('angular_heat_coefficients',s.simplify(heat-(1/e+s.Rational(1,3)+e/s.Integer(15)+4*e**2/s.Integer(315)))==0)
ab=s.series(-s.diff(heat,e)-heat+1-3*s.exp(-2*e),e,0,1).removeO().expand()
check('angular_Abel_divergences',s.simplify(ab-(1/e**2-1/e-s.Rational(12,5)))==0)

OUT.parent.mkdir(parents=True,exist_ok=True)
result={'status':'all-exact-checks-passed','checks':checks,'number_checks':len(checks),
        'generic_charged_centrifugals_per_charge':[str(v) for v in charged_c[:4]],
        'generic_neutral_centrifugals':[str(v) for v in neutral_c],
        'charged_a1_sum':str(sum_a1),'neutral_wall_determinant':str(wall_det),
        'vector_log_power':str(vec_log_power),'ghost_log_power':str(gh_log_power),
        'Gaussian_a1_per_m':str(gaussian_a1),'explicit_population':population,
        'angular_heat_series':str(heat),'angular_Abel_series':str(ab),
        'non_claim':'No numeric fit, no ODE, no proof of J-uniform determinant summability or physical matching.'}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'number_checks':len(checks),'finite_J_range':[2,20],
                  'vector_a1':str(sum_a1),'Gaussian_a1_per_m':str(gaussian_a1),'output':str(OUT)}))
