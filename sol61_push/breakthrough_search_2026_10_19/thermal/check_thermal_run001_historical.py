"""Bounded finite-T quadratures; these do not prove the general claims."""
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import zeta

OUT = Path(__file__).parent / "run_001" / "results.json"
rows = []


def record(name, condition, **data):
    if not condition:
        raise AssertionError((name, data))
    rows.append({"name": name, **{k: float(v) for k, v in data.items()}})


def thermal_tail(v):
    q = math.exp(-2 * v)
    return 2 * q / (1 + q)


def deficit(theta):
    return theta * quad(
        lambda v: thermal_tail(v) / (1 + theta**2 * v**2)**1.5,
        0, 45, epsabs=2e-13, epsrel=2e-12,
    )[0]


def source(e, theta):
    lo = e / theta
    thermal = 0.0 if lo > 45 else e * theta * quad(
        lambda v: thermal_tail(v) / (1 + theta**2 * v**2 - e**2)**1.5,
        lo, 45, epsabs=2e-13, epsrel=2e-12,
    )[0]
    return e**2 / (1 + e) + thermal


for theta in [1e-4, 1e-3, 1e-2, 0.1, 1, 10, 100]:
    value = deficit(theta)
    # Independent compact-interval change of variables in chi_T itself.
    chi = quad(
        lambda s: math.tanh(s / (theta * math.sqrt(1 - s*s))),
        0, 1, epsabs=2e-12, epsrel=2e-12,
    )[0]
    record("two susceptibility quadratures", abs(value - (1 - chi)) < 2e-10,
           theta=theta, delta=value, discrepancy=abs(value - (1 - chi)))
    record("strict deficit and analytic bound", 0 < value < 1 and value <= theta * math.log(2),
           theta=theta, delta=value)

values = [deficit(t) for t in [1e-4, 1e-3, 1e-2, 0.1, 1, 10, 100]]
record("temperature monotonicity on declared grid", all(a < b for a, b in zip(values, values[1:])))

for theta in [1e-2, 3e-3, 1e-3]:
    val = deficit(theta)
    approx = theta * math.log(2) - 9 * float(zeta(3)) * theta**3 / 16
    record("low temperature cubic coefficient", abs(val - approx) < 5 * theta**5,
           theta=theta, error=abs(val-approx))

for theta in [1e-2, 1e-3, 1e-4]:
    for ratio in [0.01, 0.1, 1, 10]:
        e = ratio * theta
        val = source(e, theta)
        scaling = e * theta * float(np.logaddexp(ratio, -ratio))
        # Explicit bound: |(1+q)^(-3/2)-1|<=3q/2 for q>=0.
        # Here q=theta^2 v^2-e^2, and dropping its negative term enlarges it.
        moment = quad(lambda v: v*v*thermal_tail(v), ratio, 45)[0]
        bound = e**3 / (1 + e) + 1.5 * e * theta**3 * moment
        record("infrared logcosh scaling bound", abs(val - scaling) <= bound * (1+2e-6) + 1e-20,
               theta=theta, field_over_thermal=ratio, absolute_error=abs(val-scaling), bound=bound)

for theta in [1e-2, 1e-3, 1e-4]:
    e = theta * 1e-5
    ratio = source(e, theta) / e
    delta = deficit(theta)
    record("linear source floor", abs(ratio-delta) < delta * 2e-6,
           theta=theta, source_slope=ratio, delta=delta)

for theta in [1e-2, 1e-3, 1e-4]:
    # Units hbar=kB=d=a=1: tau0=pi/4 and theta=T.
    normalized = deficit(theta) / (theta * math.pi/4)
    expected = 4*math.log(2)/math.pi
    record("thermal to zero-T absorption relation", abs(normalized/expected-1) < 2*theta**2,
           theta=theta, ratio=normalized, limit=expected)

# A mutation with the zero-T response at T>0 misses the finite susceptibility
# deficit. This checks that the asserted thermal effect is resolved numerically.
mutation_residual = deficit(0.01)
record("zero-T substitution mutation detected", mutation_residual > 0.006,
       mutation_residual=mutation_residual)

OUT.write_text(json.dumps({
    "assertion_tested": "Declared finite quadrature grids and asymptotic/bound controls",
    "checks_count": len(rows), "checks": rows,
    "limitations": "Float quadrature with stated tolerances; no interval certification or physical source matching."
}, indent=2) + "\n")
print(json.dumps({"checks_count": len(rows), "theta_0.01_deficit": deficit(0.01),
                  "dimensionless_ratio_limit": 4*math.log(2)/math.pi}))
