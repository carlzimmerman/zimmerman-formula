"""Cache-free, source-built f34 zero-field scalar audit.

Reads hunt_2026/f34_timedep_scalar_sector.py and executes its AST only through
the construction of L2dc. It omits SC/CACHE assignments, os.makedirs, the cache
read branch, both pickle.dump calls, and everything from the numpy import
onward. Before the selected build branch it sets w1=w2=w3=Q0=0 and the
transverse/tensor field expressions B2f=B3f=s22=s23=a2f=a3f=0. No source cache
is read or written; captured source progress text is not a cache provenance.

The source's Newton-gauge scalar fields obey a_i=-partial_i T. The invertible
change Psi=n+dot(T), with Fourier convention exp(i(k x-omega t)), gives the
clock-unitary lapse n and scalar shift variable T. Both are then eliminated
by their invertible algebraic block, only for k!=0,c14!=0,c2!=0. K=-K2.
Matrices use independent bra/ket amplitudes; their shared factor 2 is retained
in the full matrix and removed from the final reduced kernel.

This tests the constant-chi, Minkowski, clock-rest quadratic scalar sector.
It does not count nonlinear Dirac degrees of freedom, test k=0, or establish
health on finite-gradient, boosted, curved, or time-dependent backgrounds.
The outside-J variant is a different operator placement, not a validation of
the original inside-J candidate. All algebra is exact over SymPy rationals;
decimal roots are illustrative evaluations of exact quadratic roots.

An independent ADM quadratic expression is checked against the transformed
source action. In unitary clock gauge with gamma_ij=(1-2 Phi)delta_ij and
N_i=partial_i T, K_ij=-dot(Phi)delta_ij-partial_i partial_j T. Its lapse and
shift are both varied. The spatial scalar gauge E=0 leaves the E equation
redundant through spatial diffeomorphism invariance and the retained shift
equation at k!=0. Thus the reduction does not rely solely on counting a
Newton-gauge Hessian. This argument and the explicit ADM equality apply only
to this quadratic background; k=0 needs a fresh constraint analysis.
"""

import argparse
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import platform
import time

import sympy as sp


def _build_source():
    root = Path(__file__).resolve().parents[3]
    source = root / 'hunt_2026/f34_timedep_scalar_sector.py'
    raw = source.read_bytes()
    tree = ast.parse(raw.decode())
    body = []
    excluded = []
    selected = False
    for node in tree.body:
        if isinstance(node, ast.Import) and any(n.name == 'numpy' for n in node.names):
            excluded.append('numpy import and all subsequent source statements')
            break
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id in ('SC', 'CACHE') for t in node.targets
        ):
            excluded.append(ast.unparse(node))
            continue
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                and ast.unparse(node.value.func) == 'os.makedirs'):
            excluded.append(ast.unparse(node))
            continue
        if isinstance(node, ast.If) and 'os.path.exists(CACHE)' in ast.unparse(node.test):
            selected = True
            excluded.append('source cache existence test and entire cache-read branch')
            body.extend(ast.parse(
                'w1=w2=w3=Q0=sp.S(0)\nB2f=B3f=s22=s23=a2f=a3f=sp.S(0)'
            ).body)
            for inner in node.orelse:
                if (isinstance(inner, ast.Expr) and isinstance(inner.value, ast.Call)
                        and ast.unparse(inner.value.func) == 'pickle.dump'):
                    excluded.append(ast.unparse(inner))
                else:
                    body.append(inner)
        else:
            body.append(node)
    if not selected:
        raise RuntimeError('Expected source build branch not found')
    reduced_ast = ast.fix_missing_locations(ast.Module(body=body, type_ignores=[]))
    calls = [ast.unparse(n.func) for n in ast.walk(reduced_ast) if isinstance(n, ast.Call)]
    forbidden = {'open', 'pickle.load', 'pickle.dump', 'os.makedirs', 'os.path.exists'}
    if forbidden.intersection(calls):
        raise RuntimeError('Unexpected filesystem/cache operation in selected AST')
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(reduced_ast, str(source), 'exec'), namespace)
    return namespace, {
        'path': str(source.relative_to(root)), 'sha256': hashlib.sha256(raw).hexdigest(),
        'excluded_operations': excluded, 'cache_io': False,
        'early_substitutions': 'w1=w2=w3=Q0=B2f=B3f=s22=s23=a2f=a3f=0',
    }


def _strings(matrix):
    return [[str(v) for v in row] for row in matrix.tolist()]


def derive():
    started = time.monotonic()
    ns, provenance = _build_source()
    (kb, c2, jy, xi2, k, omega) = [ns[n] for n in ('KB', 'C2', 'JY', 'XI2', 'kx', 'om')]
    c14, K = sp.symbols('c14 K', positive=True)
    Tk, Tb, nk, nb = sp.symbols('Tk Tb nk nb')
    phi, phib, chi, chib = [ns[n] for n in ('Phik', 'Phib', 'chik', 'chib')]
    sub = {ns['a1k']: -sp.I*k*Tk, ns['a1b']: sp.I*k*Tb,
           ns['Rk']: 0, ns['Rb']: 0, ns['XA']: 0, ns['XB']: 0,
           ns['XC']: 1, ns['LAM']: 0, ns['C4']: c14-kb, ns['K2']: -K}
    Lnewton = sp.expand(ns['L2dc'].subs(sub))
    Lunitary = sp.expand(Lnewton.subs({ns['Psik']: nk-sp.I*omega*Tk,
                                     ns['Psib']: nb+sp.I*omega*Tb}))
    kets, bras = [nk, Tk, phi, chi], [nb, Tb, phib, chib]
    M = sp.Matrix(4, 4, lambda i, j: sp.diff(Lunitary, bras[i], kets[j]))
    D = M[:2, :2]
    constraint_solutions = (-D.inv()*M[:2, 2:]*sp.Matrix([phi, chi])).applyfunc(sp.factor)
    R = ((M[2:, 2:]-M[2:, :2]*D.inv()*M[:2, 2:])/2).applyfunc(sp.factor)
    kinetic = R.applyfunc(lambda x: sp.expand(x).coeff(omega, 2)).applyfunc(sp.factor)
    A, B = 2-kb, 2-c14
    j0 = sp.factor(A/B-1)
    a, b, d, e = 2*(3+2/c2), 2*B/c14, 2*A/c14, 2*A**2/(B*c14)
    # Independent ADM expansion, including lapse and scalar shift before variation.
    Eplus, Eminus = sp.symbols('Eplus Eminus')
    def field(ket, bra):
        return ket*Eplus+bra*Eminus
    def dt(f):
        return -sp.I*omega*Eplus*sp.diff(f, Eplus)+sp.I*omega*Eminus*sp.diff(f, Eminus)
    def dx(f):
        return sp.I*k*Eplus*sp.diff(f, Eplus)-sp.I*k*Eminus*sp.diff(f, Eminus)
    fn, ft, fp, fc = [field(ket, bra) for ket, bra in zip(kets, bras)]
    ADM = (-6*dt(fp)**2+2*dx(fp)**2-4*dx(fn)*dx(fp)-4*dt(fp)*dx(dx(ft))
           -c2*(-3*dt(fp)-dx(dx(ft)))**2+c14*dx(fn)**2
           +2*A*dx(fn)*dx(fc)+K*dt(fc)**2-A*(1+jy)*dx(fc)**2
           -A*jy*xi2*dx(dx(fc))**2)
    ADM_dc = sp.expand(ADM).coeff(Eplus, 1).coeff(Eminus, 1)
    checks = {
        'independent_ADM_action_equals_source': sp.expand(ADM_dc-Lunitary) == 0,
        'source_projected_gradient_identity': ns['resDC'] == 0,
        'full_matrix_hermitian': (M-sp.conjugate(M.T)).applyfunc(sp.simplify).is_zero_matrix,
        'constraint_block_no_frequency': not D.has(omega),
        'deep_mond_stiffness_cancellation': sp.cancel(b*e-d*d) == 0,
    }
    values = {kb: sp.Rational(1, 5), c14: sp.Rational(1, 100000),
              c2: sp.Rational(1, 100), K: sp.Integer(10), k: sp.Integer(1), xi2: sp.Integer(1)}
    z = sp.symbols('z', real=True)
    variants = {}
    for name, h in [('inside', j0), ('outside', sp.Integer(1))]:
        # Change only the k^4 term; unlike xi2/JY substitution this is defined at JY=0.
        candidate = R.copy()
        if name == 'outside':
            candidate[1, 1] += A*(jy-1)*xi2*k**4
        candidate = candidate.subs(jy, j0).applyfunc(sp.factor)
        compact = sp.Matrix([[a*omega**2-b*k**2, d*k**2],
                             [d*k**2, K*omega**2-e*k**2-A*h*xi2*k**4]])
        checks[name+'_source_matches_compact_kernel'] = (
            candidate-compact).applyfunc(sp.cancel).is_zero_matrix
        determinant = sp.expand(compact[0, 0]*compact[1, 1]-compact[0, 1]*compact[1, 0])
        compact_det = a*K*omega**4-(a*(e*k**2+A*h*xi2*k**4)+b*K*k**2)*omega**2+b*A*h*xi2*k**6
        checks[name+'_determinant_identity'] = sp.cancel(determinant-compact_det) == 0
        # Numeric parameters are exact rationals, before polynomial/root construction.
        polynomial = sp.Poly(sp.factor(compact_det.subs(values)).subs(omega**2, z), z)
        roots = sorted(sp.solve(polynomial.as_expr(), z), key=lambda r: float(sp.N(r)))
        checks[name+'_root_residuals_zero'] = all(sp.simplify(polynomial.eval(r)) == 0 for r in roots)
        numeric_kernel = compact.subs(values)
        stiffness = -numeric_kernel.subs(omega, 0)
        variants[name] = {
            'h': str(h), 'kernel': _strings(compact),
            'determinant': str(compact_det),
            'constant_term': str(sp.factor(b*A*h*xi2*k**6)),
            'polynomial_at_witness': str(polynomial.as_expr()),
            'polynomial_degree_in_omega_squared': polynomial.degree(),
            'exact_omega_squared': [str(r) for r in roots],
            'numeric_omega_squared': [str(sp.N(r, 25)) for r in roots],
            'negative_omega_squared_count': sum(bool(r < 0) for r in roots),
            'positive_omega_squared_count': sum(bool(r > 0) for r in roots),
            'stiffness_leading_minor': str(stiffness[0, 0]),
            'stiffness_determinant': str(sp.factor(stiffness.det())),
        }
    numeric_kinetic = kinetic.subs(values)
    eigenvalues = list(numeric_kinetic.eigenvals().items())
    result = {
        'scope': 'Minkowski, clock rest, Q0=0, constant chi, scalar Fourier k!=0',
        'nonclaims': ['k=0 unanalyzed', 'nonlinear Dirac degree count unclaimed',
                      'finite-gradient/boosted/curved backgrounds unanalyzed',
                      'no tensor/vector analysis in this reduced build',
                      'outside-J is an alternative action'],
        'source': provenance, 'python': platform.python_version(), 'sympy': sp.__version__,
        'arithmetic': 'exact symbolic/rational; 25-digit display of exact roots',
        'assumptions': 'K=-K2>0, c2>0, 0<c14<KB<2, xi2>0, k!=0',
        'j0': str(j0), 'j0_at_witness': str(j0.subs(values)),
        'matrix_basis': ['n', 'T_shift', 'Phi', 'chi'], 'full_matrix': _strings(M),
        'constraint_block_determinant': str(sp.factor(D.det())),
        'constraint_solutions_n_T': [str(v) for v in constraint_solutions],
        'reduced_kernel_divided_by_2': _strings(R),
        'kinetic_matrix': _strings(kinetic), 'kinetic_rank': kinetic.rank(),
        'kinetic_determinant': str(sp.factor(kinetic.det())),
        'kinetic_eigenvalues_at_witness': {str(v): int(m) for v, m in eigenvalues},
        'kinetic_positive_count_at_witness': sum(int(m) for v, m in eigenvalues if v > 0),
        'witness_parameters': {str(key): str(value) for key, value in values.items()},
        'variants': variants, 'checks': checks,
    }
    result['internal_validity'] = all(checks.values())
    result['inside_rejected_at_witness'] = variants['inside']['negative_omega_squared_count'] > 0
    result['outside_positive_at_witness'] = (variants['outside']['negative_omega_squared_count'] == 0
        and variants['outside']['positive_omega_squared_count'] == variants['outside']['polynomial_degree_in_omega_squared'])
    result['runtime_seconds'] = round(time.monotonic()-started, 3)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-inside', action='store_true',
                        help='Exit 2 when the inside-J candidate has a negative omega squared')
    parser.add_argument('--output', type=Path,
                        help='Explicitly write JSON to this file; otherwise no file writes')
    args = parser.parse_args()
    result = derive()
    serialized = json.dumps(result, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(serialized+'\n')
    print(serialized)
    raise SystemExit(1 if not result['internal_validity'] else
                     2 if args.strict_inside and result['inside_rejected_at_witness'] else 0)
