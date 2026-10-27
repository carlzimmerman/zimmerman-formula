"""Independent finite identities; stdlib only, no target implementation imports."""
from fractions import Fraction as F
from functools import reduce
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def polynomial_with_roots(roots):
    p = [F(1)]
    for x in roots:
        q = [F(0)] * (len(p) + 1)
        for i, a in enumerate(p):
            q[i] -= x * a
            q[i + 1] += a
        p = q
    return p


def eval_poly(p, x):
    return sum(a * x**i for i, a in enumerate(p))


n = [10, 13, 20, 34, 50, 65]
ys = [F(x) for x in ['.688', '.596', '.208', '.080', '.136', '.135']]
errs = [F(x) for x in ['.071', '.087', '.073', '.069', '.075', '.065']]
segments = [F(n[i+1] - n[i], 2) * (ys[i] + ys[i+1]) for i in range(5)]
momentum_weights = [F(3, 2), F(5), F(21, 2), F(15), F(31, 2), F(15, 2)]
assert sum(segments) == F(21033, 2000)
coefficient = -F(3, 16 * 48**2) / F('.3860')**2
kp = coefficient * sum(segments)
assert kp == -F(876375, 152571904)
sigma = abs(coefficient) * sum(w * e for w, e in zip(momentum_weights, errs))
assert sigma == F(166375, 76285952)
assert 2 * max(w * e for w, e in zip(momentum_weights, errs)) <= sum(w * e for w, e in zip(momentum_weights, errs))

# Spectral expansion is independent of the target's linear-system implementation.
stress = polynomial_with_roots([F(1), F(4), F(16)])
assert stress == [-64, 84, -21, 1]
assert eval_poly(stress, F(2)) == 28
assert all(eval_poly(stress, F(2)**i) == 0 for i in (0, 2, 4))
assert eval_poly(stress, F(2)**6) / 28 == 6480
w = [64 * x for x in polynomial_with_roots([F(1), F(1), F(1, 4), F(1, 16)])]
assert w == [1, -22, 105, -148, 64]
assert eval_poly(w, F(1, 8)) == -F(49, 128)
assert sum(w) == 0 and sum(i * a for i, a in enumerate(w)) == 0
assert all(eval_poly(w, F(2)**i) == 0 for i in (-4, -2, 0))
# A metric rho=A H has W=(4/3)Omega A H^-3.
assert -F(96, 49) * eval_poly(w, F(1, 8)) * F(4, 3) == 1

# Concrete flat baseline with dimensionless toy constants all equal to one:
# m=Lambda+u/L, Lambda=1-u/L, E0=Lambda^4, E_L=E0.
# Cross-theory subtraction has a linear 1/L term; same-theory subtraction is 0.
u, Linv = F(1, 100), F(1, 10)
lam = 1-u*Linv
E0 = lam**4
assert E0-E0 == 0
assert E0-1 != 0
# Evaluate stress first: baseline coefficient A. Compose first: coefficient 3A/4.
A = F(7, 3)
metric_coefficient = A
composed_coefficient = A-F(1, 4)*A
assert composed_coefficient == F(3, 4)*metric_coefficient

result = {
    'scope': 'Exact finite rational identities and one concrete flat toy matching family; no QCD data or limits inferred.',
    'self_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'K_exact': str(kp), 'sigma_ceiling_exact_fixed_aM': str(sigma),
    'stress_weights': list(map(str, stress)), 'stress_H_normalization': '28',
    'partition_weights': list(map(str, w)),
    'partition_H_minus3_moment': str(eval_poly(w, F(1, 8))),
    'stress_from_W_conversion': '3/4',
    'flat_model_same_theory_difference': '0',
    'flat_model_cross_theory_difference': str(E0-1),
    'status': 'all assertions passed'
}
(HERE/'independent_checks_result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
