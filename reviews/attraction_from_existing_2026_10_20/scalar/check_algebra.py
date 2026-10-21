"""Exact identities and fixed-input arithmetic; no parameter search or dynamics."""
import json
import math
import resource
import sys
from pathlib import Path

import sympy as s

OUT = Path(sys.argv[1])
k, d = s.symbols("k d", positive=True)
e = s.symbols("e", real=True)
c2 = (2*k-e)*(d-e)/2
A, C = 12*k-2*e, 2*d-2*e
schur = d+2*k-2*e-12*c2/A-4*c2/C
assert s.factor(schur-2*e*(d-e)/(6*k-e)) == 0
assert s.factor(A*C*schur-8*e*(d-e)**2) == 0
H4 = s.Matrix([[12*k-2*e, s.sqrt(12), 0],
                [s.sqrt(12)*c2, d+2*k-2*e, 2],
                [0, 2*c2, 2*d-2*e]])
# Similarity-scaled tridiagonal matrix preserves characteristic polynomial;
# avoids introducing square roots of the symbol c2.
assert s.factor(H4.det()-8*e*(d-e)**2) == 0
assert s.expand(2*d-2*(2*k+d)+12*k) == 8*k

beta, ad, r = s.symbols("beta ad r", positive=True)
ab = ad/beta
overlap = 4*s.pi*s.integrate(
    r*r*s.exp(-r/ab-2*r/ad)/(s.pi**s.Rational(3,2)*ab**s.Rational(3,2)*ad**3),
    (r, 0, s.oo))
I4 = 1/(8*s.pi*ad**3)
rho = s.factor(overlap**2/I4)
assert s.factor(rho-512*beta**3/(beta+2)**6) == 0

# Frozen scalar benchmark from MASTER + RESONANCE_FOLLOWUP. Host mass,
# temperature and receiver geometry are deliberately not selected.
m = 1.0e6
u = 0.02
r_lambda = 2.0
g = 2168.0  # published rounded source-coupling benchmark, not refitted
M = 2*m*math.sqrt(1+u*u)
delta = M-2*m
Delta_c = 4*m*m*u*u
lambda_min = g*g/Delta_c
lambda_rep = r_lambda*lambda_min
c3 = g/(2*m*math.sqrt(2*M))
kc = (lambda_min+lambda_rep)/(4*m*m)
delta_k = -g*g/(8*m*m*M*(M+2*m))
kR = kc+delta_k
assert math.isclose(kR-c3*c3/delta, lambda_rep/(4*m*m), rel_tol=1e-10)
ratio = kR*delta/(c3*c3)
beta_value = (M/m)**2
rho_value = 512*beta_value**3/(beta_value+2)**6
zc = delta-c3*c3/kR
# Conditional Coulomb-host inequality endpoints, computed algebraically.
# These are derived boundaries, not chosen or scanned host configurations.
Dalpha = m*((M/m)**3-2)/2
alpha_attraction_lower = math.sqrt((delta-rho_value*c3*c3/kR)/Dalpha)
alpha_source_closed_upper = math.sqrt(delta/Dalpha)
results = {
    "assertion_tested": [
        "exact Q=4 Schur identity after Q=2 characteristic substitution",
        "exact determinant identity det(H4-2e)=8e(delta-e)^2",
        "fixed-Q=4 bare source-count curvature is 8k",
        "exact Coulomb 1s overlap ratio 512 beta^3/(beta+2)^6",
        "fully matched contact coefficient identity at fixed published benchmark"
    ],
    "symbolic_domain": "rational functions; positivity inferred analytically in RESULT.md",
    "numerical_inputs": {"m_eV": m, "u_star": u, "r_lambda": r_lambda, "g_rounded_eV": g},
    "derived": {"M_eV": M, "delta_eV": delta, "kR_eV_minus2": kR,
                "matched_repulsive_remainder_eV_minus2": kR-c3*c3/delta,
                "kR_delta_over_c3_squared": ratio,
                "positive_energy_schur_contact_zero_eV": zc,
                "coulomb_overlap_ratio": rho_value,
                "conditional_alpha_attraction_lower": alpha_attraction_lower,
                "conditional_alpha_closed_source_upper": alpha_source_closed_upper},
    "non_claims": ["No host is selected", "No memory occupation dictionary or state count is derived",
                   "No dynamics, physical lifetime, continuum renormalization or phenomenology is computed",
                   "Threshold-matched NR truncation is not full relativistic quantum theory"]
}
rss_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # macOS bytes
assert sys.platform == "darwin"
assert rss_bytes < 1_000_000_000
results["observed_peak_rss_bytes"] = rss_bytes
OUT.write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps(results, indent=2))
