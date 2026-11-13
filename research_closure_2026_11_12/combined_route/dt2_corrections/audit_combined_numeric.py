"""Independent arithmetic witnesses; consumes a completed combined_constraints output.

Usage: python3 audit_combined_numeric.py INPUT.json OUTPUT.json
This checks implementation arithmetic, not the physical assumptions or a general theorem.
"""
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq


def main():
    source = Path(sys.argv[1])
    observed = json.loads(source.read_text())
    enhancement = lambda x: math.atan((1+x)**(-.5))*(1+x)**1.5/x
    xlate = brentq(lambda x: enhancement(x)-60.5, .01, .02, xtol=1e-15)
    hubble = lambda z: math.sqrt(.315*(1+z)**3+.685)
    fold_coefficient = lambda z: float(np.interp(z, [0,1,2,4], [.52,.46,.435,.32]))
    # Algebraically equivalent positive root, independent expression from source.
    solve_x = lambda y: 2*y/(math.sqrt(y*y+4*y)-y)
    ylate = xlate*xlate/(1+xlate)
    xearly = solve_x(ylate*(3.5/1.3)**3)
    ratio = xlate/xearly*fold_coefficient(.3)/fold_coefficient(2.5)*(hubble(2.5)/hubble(.3))**(2/3)
    growth = (ratio/.56)**6
    independent = dict(x_early=xearly, Xc_early=enhancement(xearly)-1,
                       constant_mass_f_ratio=ratio,
                       minimum_baryon_growth_for_proxy_window=growth,
                       required_cold_growth_at_threshold=growth*59.5/(enhancement(xearly)-1),
                       maximum_early_Fc_if_late_Fc_le_1=(enhancement(xearly)-1)/(growth*59.5))
    comparisons = {k: abs(v/observed['exact_scalar_environment_history'][k]-1)
                   for k,v in independent.items()}
    assert max(comparisons.values()) < 1e-13
    eps = 1e-5
    finite_rate = (math.log(solve_x(ylate*math.exp(-3*eps)))-
                   math.log(solve_x(ylate*math.exp(3*eps))))/(2*eps)
    exact_rate = -3*(1+xlate)/(2+xlate)
    assert abs(finite_rate-exact_rate) < 1e-9
    identity_errors = []
    for u in np.geomspace(1e-6,1e6,1001):
        w = u*u
        gamma = 2*(1+2*w)/(1+w)
        eta = 2*w/((1+w)*(1+2*w))
        rational = (1+3*w+6*w*w)/((1+w)*(1+2*w))
        identity_errors.append(abs(gamma-1-eta-rational))
    assert max(identity_errors) < 3e-15
    result = dict(status='PASS; finite arithmetic witnesses only',
                  input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  independent_exact_history=independent,
                  history_relative_errors=comparisons,
                  log_x_rate_exact=exact_rate,
                  log_x_rate_finite_difference_error=abs(finite_rate-exact_rate),
                  convexity_identity_max_error=max(identity_errors),
                  source_runner_result=observed,
                  python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)
    Path(sys.argv[2]).write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_runner_result'}, indent=2))


if __name__ == '__main__':
    main()
