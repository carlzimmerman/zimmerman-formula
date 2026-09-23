"""Exact bounded audit, no edits to existing research artifacts.

Run from repository root. Geometry is flat FRW; determinant is the exported
L287 frozen-background 5x5 matrix, with a independently reconstructed healing
replacement, not a derivation of full cosmological dynamics.
"""
import itertools
import json
from pathlib import Path
import runpy
from fractions import Fraction
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = {}

runpy.run_path(str(HERE/'geometric_linear_check.py'),run_name='__main__')
runpy.run_path(str(HERE/'independent_matrix_check.py'),run_name='__main__')

def check(name, ok, result):
    assert bool(ok), name
    OUT[name] = str(result)
    print('PASS', name, ':', result, flush=True)

# Flat FRW, calculated from the metric and the connection.
t,x,y,z = s.symbols('t x y z', real=True)
coords = [t,x,y,z]
a = s.Function('a')(t)
phi = s.Function('phi')(t)
g = s.diag(-1,a*a,a*a,a*a)
gi = g.inv()
gam = [[[sum(gi[l,r]*(s.diff(g[r,m],coords[n]) +
             s.diff(g[r,n],coords[m])-s.diff(g[m,n],coords[r]))
             for r in range(4))/2 for n in range(4)]
             for m in range(4)] for l in range(4)]
h = s.diag(0,1/a**2,1/a**2,1/a**2)
Hess = s.Matrix(4,4,lambda i,j:s.diff(phi,coords[i],coords[j])-
                gam[0][i][j]*s.diff(phi,t))
proj = s.simplify(sum(h[i,j]*Hess[i,j] for i in range(4) for j in range(4)))
check('projected_hessian_on_FRW', s.simplify(proj+3*s.diff(a,t)/a*s.diff(phi,t))==0, proj)
Kij = s.Matrix(3,3,lambda i,j:gam[0][i+1][j+1])
Aij = Hess.extract([1,2,3],[1,2,3])+s.diff(phi,t)*Kij
check('written_spatial_hessian_on_FRW', Aij==s.zeros(3), Aij)

# Reconstruct exact exported Fourier matrix. Explicit symbol dictionary avoids
# interpreting beta as SymPy's beta function.
ns='omega k Q_0 F_1 F_2 c_2 c14 K_B beta xi'
v=s.symbols(ns,real=True)
loc=dict(zip(ns.split(),v))
w,k,Q,F1,F2,c2,c14,KB,b,xi=v
data=json.loads((ROOT/'real_research/clock_2026/L287_dirac_count_clock_lapse_results.json').read_text())
M=s.Matrix(5,5,lambda i,j:s.sympify(data['M_entries'][str(i)+str(j)],locals=loc))
gauge=s.Matrix([s.I*w,s.I*k,0,-1,-Q])
check('correct_gauge_vector', all(s.simplify(x)==0 for x in M*gauge), 'M*(i w, i k, 0, -1, -Q)=0')
check('matrix_hermitian', all(s.simplify(x)==0 for x in M-s.conjugate(M.T)), True)

# In the flat quadratic sector the written Hessian norm and intrinsic
# Laplacian square have the same integrated Fourier symbol. This equivalence
# is NOT asserted on a curved nonlinear leaf.
old=s.Matrix([[0,s.I*k*Q,-3*s.I*w*Q,0,-k*k]])
new=s.Matrix([[0,0,0,k*k*Q,-k*k]])
Mc=M+2*(2-KB)*xi**2*s.conjugate(old.T)*old-2*(2-KB)*xi**2*s.conjugate(new.T)*new
check('corrected_gauge_vector', all(s.simplify(x)==0 for x in Mc*gauge), True)
check('corrected_healing_relative_scalar', s.expand((new*gauge)[0])==0, '-k^2 (P-Q T)')

# Extract only the needed determinant coefficient, avoiding an expensive
# general rational-function determinant. All 24 permutations are included;
# truncating powers above k^4 cannot change this coefficient.
def k4_coefficient(mat):
    coef=0
    for perm in itertools.permutations(range(4)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        poly=s.Poly(1,k)
        for i in range(4):
            poly=poly*s.Poly(mat[i,perm[i]],k)
            poly=s.Poly.from_dict({m:c for m,c in poly.terms() if m[0]<=4},k)
        coef+=sign*poly.nth(4)
    return s.factor(coef)

M4=Mc.extract([0,2,3,4],[0,2,3,4]).subs(b,(2-KB)/(2-c14))
coef=k4_coefficient(M4)
clock_factor=F1*Q*(2-c14)+2*(2-KB)**2*Q**2-2*c14*(2-c14)*w**2
expected=-3*F1*Q*(3*F1**2-2*F2*(3*c2+2)*w**2)*clock_factor/(c14-2)
check('exact_k4_factorization',s.factor(coef-expected)==0,expected)
check('k4_coefficient_independent_of_healing',s.diff(coef,xi)==0,True)
gap=((2-KB)**2*Q**2/(2-c14)+F1*Q/2)/c14
check('clock_gap_root',s.factor(clock_factor.subs(w**2,gap))==0,gap)
check('gap_independent_of_well_curvature',s.diff(gap,F2)==0,True)

# Finite numerical illustrations of the exact diagnostic, not growth histories.
corner={Q:1,KB:s.Rational(1,5),c14:s.Rational(1,40000)}
threshold=2*(2-s.Rational(1,5))**2/(2-s.Rational(1,40000))
OUT['density_loading_threshold']=str(threshold)
for av in (s.Integer(1),s.Rational(1,2),s.Rational(1,100)):
    slope=-s.Rational(156,100)/av**3
    val=gap.subs(corner).subs(F1,slope)
    OUT['gap_a_'+str(av)]=str(val)
    print('DIAGNOSTIC', 'a=',av,'gap/H0^2=',float(val),flush=True)

# Independent exact small-state YM07 counterexample using its own definitions.
e=Fraction(1,100)
ell=e*e/(1+e*e)
db=-e/(4*(1+e*e))  # x=8,N=2: (2/x)*[-(1/N)*2e/(1+e^2)]
bound=Fraction(13,2)*ell
check('YM07_magnetic_bound_counterexample',abs(db)>bound,
      {'ell':ell,'DB':db,'bound':bound,'ratio':abs(db)/bound})
check('YM07_electric_vacuum_not_ground',12*ell+db<0,12*ell+db)

# Separate Euler--Poisson linearization and exact variational witness.
runpy.run_path(str(HERE/'equilibrium_check.py'),run_name='__main__')
OUT['equilibrium_check']='exact missing term, zero-mode residuals, annulus integral verified'

result=HERE/'run_symbolic'/'results.json'
result.parent.mkdir(exist_ok=True)
result.write_text(json.dumps(OUT,indent=2)+'\n')
print('All exact audit assertions passed.',flush=True)
