"""Independent exact algebra; no finite component-model rerun or Git mutation."""
import sys
sys.dont_write_bytecode = True
import json, resource
from pathlib import Path
import sympy as s

z, k = s.symbols('z k', real=True)

def block(r, broken=False):
    m, q, beta = (1+r)*z, r*s.sqrt(2), 1+r
    hp = s.Matrix([[m*m+q*q+beta, -m*q], [-m*q, q*q]])
    hm = s.Matrix([[m*m+q*q-beta, m*q], [m*q, q*q]])
    mf = s.Matrix([[m, q], [q, 0]])
    v = 0
    if broken:
        L, R = 5*k*s.sqrt(2), 5*k*z
        hp += s.Matrix([L, -R])*s.Matrix([[L, -R]])
        mf = s.Matrix([[m, q, L], [q, 0, R], [L, R, 0]])
        v = L*L+R*R
    st2 = s.simplify(s.trace(hp)+s.trace(hm)-2*s.trace(mf*mf)+3*v)
    st4 = s.factor(s.trace(hp*hp)+s.trace(hm*hm)-2*s.trace(mf**4)+3*v*v)
    return st2, st4

invariants, total = {}, 0
for name, r, mult, broken in [('SU3', s.Integer(2), 8, False),
                               ('SU2', s.Integer(-3), 3, False),
                               ('broken', -s.Rational(1, 2), 12, True)]:
    st2, st4 = block(r, broken)
    invariants[name] = {'STr_M2_over_c': str(st2), 'STr_M4_over_c2': str(st4),
                        'multiplicity': mult}
    assert st2 == 0
    assert s.diff(st4, z) == 0
    total += mult*st4
total = s.factor(total)
assert s.simplify(total.subs(k*k, s.Rational(29,200))) == 0

h, lam, aa = s.symbols('h lambda a', positive=True)
D = 30*h*h+lam*lam
Rratio = lam**s.Rational(5,2)*s.sqrt(h)/D**s.Rational(1,4)
dh = s.factor(h*s.diff(s.log(Rratio), h))
dl = s.factor(lam*s.diff(s.log(Rratio), lam))
assert s.simplify(dh-lam*lam/(2*D)) == 0
assert s.simplify(dl-(75*h*h+2*lam*lam)/D) == 0
F_X, F_B = lam*lam/D, s.sqrt(30)*h*lam/D
B_AA = s.simplify(h*F_X-lam*F_B/s.sqrt(30))
assert B_AA == 0
Msing = s.Matrix([[0,s.I*s.sqrt(30)*h*aa,0],
                  [s.I*s.sqrt(30)*h*aa,0,-s.I*lam*aa],
                  [0,-s.I*lam*aa,0]])
t=s.symbols('t')
char = s.factor((Msing.H*Msing).charpoly(t).as_expr().subs(aa*aa,2*h/D))
assert s.simplify(char-t*(t-2*h)**2) == 0

# Fundamental D/sqrt(30), commutator representation includes 1/sqrt(2).
# Each adjoint has six roots of each sign and twelve neutral generators.
fundD=[2,2,2,-3,-3]
charges=[s.Rational(fundD[i]-fundD[j],1)/s.sqrt(60)
         for i in range(5) for j in range(5) if i!=j]
charged=[q for q in charges if q!=0]
assert len(charged)==12
assert all(s.simplify(q*q-s.Rational(5,12))==0 for q in charged)
assert sum(q*q for q in charged)==5

# Canonical complex-to-real scalar completeness annihilates the common
# B0 scale logarithm multiplying two conjugated scalar-gaugino vertices.
E=s.Matrix([[1,s.I]])/s.sqrt(2)
assert E.conjugate()*E.conjugate().T==s.zeros(1)

result={'claim_id':'TP06_HIERARCHY_INDEPENDENT_AUDIT',
        'exact_block_invariants':invariants,'total_STr_M4_over_c2':str(total),
        'critical_kappa_squared':'29/200','dlog_ratio_dlogh':str(dh),
        'dlog_ratio_dloglambda':str(dl),
        'singlet_B_AA':str(B_AA),'singlet_MdaggerM_characteristic':str(char),
        'charged_roots_per_adjoint':len(charged),'charged_root_square':'5/12',
        'adjoint_U1_trace_charge_squared':'5','complex_real_log_moment':'0',
        'checks':'passed','maxrss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'Exact symbolic block identities, singlet cancellation, U1 charge normalization, scalar completeness and positive-coupling monotonicity. No numerical minimum isolation, full component rerun, or all-SUSY no-go.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
