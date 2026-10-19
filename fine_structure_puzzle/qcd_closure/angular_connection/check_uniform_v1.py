#!/usr/bin/env python3
"""Exact angular-operator crosscheck; bounded by the pre-execution contract."""
import json
from pathlib import Path
import sympy as s

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
OUT = BASE / 'runs/exact-001/results.json'
checks = []


def check(name, expr):
    if isinstance(expr, s.MatrixBase):
        ok = all(s.simplify(x) == 0 for x in expr)
    else:
        ok = bool(expr)
    if not ok:
        raise AssertionError(name)
    checks.append(name)


def crossmat(v):
    return s.Matrix([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])


nx, ny, nz, r, k, h = s.symbols('nx ny nz r k h')
n = s.Matrix([nx, ny, nz])
p = s.Matrix([0, 0, 1])
coords = [nx, ny, nz]
eye3 = s.eye(3)
Cn = crossmat(n)
Cadj = [crossmat(eye3[:, a]) for a in range(3)]
Imat = []
for a in range(3):
    mat = s.zeros(4)
    for i in range(3):
        for j in range(3):
            mat[i, j] = s.LeviCivita(i, j, a)
        mat[i, 3] = -s.KroneckerDelta(i, a)
        mat[3, i] = s.KroneckerDelta(a, i)
    Imat.append(mat)

# Check signs/algebra separately from the imported Cartesian potential.
sigma4 = [-s.I * x for x in Imat]
T3 = [s.I * x for x in Cadj]
for a in range(3):
    for bidx in range(3):
        pauli = s.KroneckerDelta(a, bidx) * s.eye(4)
        pauli += s.I * sum((s.LeviCivita(a, bidx, c) * sigma4[c]
                          for c in range(3)), s.zeros(4))
        check('Pauli_%d_%d' % (a, bidx), sigma4[a] * sigma4[bidx] - pauli)
        comm = s.I * sum((s.LeviCivita(a, bidx, c) * T3[c]
                         for c in range(3)), s.zeros(3))
        check('isospin_%d_%d' % (a, bidx), T3[a] * T3[bidx] - T3[bidx] * T3[a] - comm)

# Curvature characteristic polynomial in the active spin space (spectator omitted).
pauli2 = [s.Matrix([[0, 1], [1, 0]]), s.Matrix([[0, -s.I], [s.I, 0]]), s.diag(1, -1)]
b, c, z = s.symbols('b c z')
curv = 2 * (c * (s.kronecker_product(pauli2[0], T3[0])
                  + s.kronecker_product(pauli2[1], T3[1]))
            + b * s.kronecker_product(pauli2[2], T3[2]))
target_charpoly = (z - 2*b)**2 * (z**2 + 2*b*z - 8*c**2)**2
check('active_curvature_characteristic', s.expand(curv.charpoly(z).as_expr() - target_charpoly) == 0)

# Original Cartesian J1 tensors, in spatial rows and adjoint columns.
basis = []
def spatial(mat):
    out = s.zeros(4, 3)
    out[:3, :] = mat
    return out

def fourth(v):
    out = s.zeros(4, 3)
    out[3, :] = v.T
    return out

basis.append(spatial(eye3 * nz))
basis.append(spatial(n * p.T))
basis.append(spatial(p * n.T))
basis.append(spatial(n * n.T * nz))
basis.append(spatial(s.Matrix(3, 3, lambda i, a: s.LeviCivita(i, a, 2))))
basis.append(spatial(n * n.cross(p).T))
basis.append(spatial(n.cross(p) * n.T))
basis.append(fourth(p))
basis.append(fourth(n * nz))
basis.append(fourth(n.cross(p)))

def Lsquare(expr):
    # -Delta_S for an arbitrary polynomial extension from n.n=1.
    value = -sum(s.diff(expr, x, 2) for x in coords)
    value += sum(coords[i]*coords[j]*s.diff(expr, coords[i], coords[j])
                 for i in range(3) for j in range(3))
    value += 2*sum(coords[i]*s.diff(expr, coords[i]) for i in range(3))
    return s.expand(value)

def LdotT(vec):
    out = s.zeros(3, 1)
    for a in range(3):
        for ib in range(3):
            for ic in range(3):
                if s.LeviCivita(a, ib, ic):
                    out += s.LeviCivita(a, ib, ic)*coords[ib]*Cadj[a]*vec.diff(coords[ic])
    return s.expand(out)

def actual_angular_action(B):
    out = s.zeros(4, 3)
    for mu in range(4):
        v = B[mu, :].T
        qv = v - n * (n.dot(v))
        angular = v.applyfunc(Lsquare) + 2*(1-k)*LdotT(v)
        angular += (1-k)**2*(2*v-qv)
        out[mu, :] = (angular/r**2+h**2*qv).T
    br = (1-k**2)/r**2
    cr = k*h/r
    for aa in range(3):
        field = cr*Cadj[aa] + (br-cr)*n[aa]*Cn
        for mu in range(4):
            for nu in range(4):
                if Imat[aa][mu, nu]:
                    out[mu, :] += (2*Imat[aa][mu, nu]*field*B[nu, :].T).T
    return out.applyfunc(s.expand)

data_path = ROOT / 'fine_structure_puzzle/qcd_completion/higher_angular/inputs_v1/j1_operator.json'
data = json.loads(data_path.read_text())
t0, k0, h0, kp0, hp0 = s.symbols('t k h kp hp')
local = {'t': t0, 'k': k0, 'h': h0, 'kp': kp0, 'hp': hp0}
Vin = s.Matrix([[s.sympify(x, locals=local) for x in row] for row in data['V_raw']])
Vin = Vin.subs({kp0: -k0*h0, hp0: (1-k0**2)/t0**2})
Vin = Vin.subs({t0: r, k0: k, h0: h}).applyfunc(s.cancel)
for j in range(10):
    action = actual_angular_action(basis[j])
    frozen = sum((Vin[i, j]*basis[i] for i in range(10)), s.zeros(4, 3))
    residual = (action-frozen).applyfunc(lambda x: s.cancel(x*r**2))
    for mu in range(4):
        for aa in range(3):
            poly = s.Poly(residual[mu, aa], nz)
            remainder = poly.rem(s.Poly(nz**2+nx**2+ny**2-1, nz)).as_expr()
            check('Cartesian_J1_column_%d_component_%d_%d' % (j, mu, aa), s.expand(remainder) == 0)

# Generic identities used by the hand proof, rather than more finite-J cases.
J, K = s.symbols('J K')
brace = (J-1)*(J-2*K)-5*(1-K**2)
aJ = (J-1)*(J-2)
check('large_J_lower_factorization', s.expand(brace-aJ-(1-K)*(2*(J-1)-5*(1+K))) == 0)
check('small_J_minimum_quadratic', s.expand(brace-(5*(K-(J-1)/5)**2+J*(J-1)-5-(J-1)**2/5)) == 0)
check('angular_convex_rewrite', s.expand(K*s.Symbol('LL')+(1-K)*(s.Symbol('LL')+2+2*s.Symbol('LT'))-2*K*(1-K)-(1-K)**2*s.Symbol('Q')-(s.Symbol('LL')+2*(1-K)*s.Symbol('LT')+(1-K)**2*(2-s.Symbol('Q')))) == 0)
ell = s.symbols('ell')
check('Coulomb_lower_barrier', s.expand(r**2-2*r+ell*(ell+1)-ell*(ell-1)-((r-1)**2+2*ell-1)) == 0)
check('beta_upper_barrier', s.expand((J+4)*(J+3)-((J+2)*(J+3)+2)-(2*J+4)) == 0)
num = 12*(13*J+120)
den = 7*(2*J-3)
check('connection_constant_decreases', s.simplify(s.diff(num/den, J)+s.Rational(3348, 7)/(2*J-3)**2) == 0)
check('connection_constant_max_below_38', num.subs(J, 6)/den.subs(J, 6) < 38)

result = {
    'checks_passed': len(checks),
    'checks': checks,
    'curvature_characteristic_polynomial': str(s.factor(target_charpoly)),
    'Cartesian_J1_columns': 10,
    'Cartesian_component_residuals': 120,
    'universal_claim_status': 'hand proof in RAW_DERIVATION_v1.md, not inferred from finite checks',
    'physical_coefficient_computed': False,
    'software': {'Python_arithmetic': 'exact symbolic', 'SymPy': s.__version__}
}
OUT.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'checks_passed': len(checks), 'Cartesian_component_residuals': 120}))
