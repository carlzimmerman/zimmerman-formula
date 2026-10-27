#!/usr/bin/env python3
"""Small arithmetic receipt for explicitly conditional analytic receiver bounds."""
import hashlib
import json
import math
import pathlib
import resource
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
G = 4.30091e-3  # pc (km/s)^2 / Msun; conventional benchmark conversion
M = 2.53958e7
q = .9885403
Rc = 25.21
Ra = 647.853
Ri = 5 * Ra
Mc, Me = q * M, (1 - q) * M
Ei = -.3 * G * M * M / Ri
Ec = -.3 * G * Mc * Mc / Rc
Q = Ei - Ec
Jscale = math.sqrt(G * M**3 * Ri)
Jcmax = math.sqrt(6 / 25 * G * Mc**3 * Rc)


def launch_min(dj, energy=Q):
    if dj <= 0:
        return 0.0
    b = G * Mc * Me * Me
    if energy == 0:
        return dj * dj / (2 * b)
    # Rationalized positive root of 2Me Q R^2+2b R-dj^2=0.
    return dj * dj / (math.sqrt(b * b + 2 * Me * energy * dj * dj) + b)


start = time.monotonic()
assert Q > 0 and 0 < q < 1
assert launch_min(0) == 0
assert math.isclose(launch_min(Jcmax, 0), Jcmax**2/(2*G*Mc*Me**2), rel_tol=1e-14)
rows = []
for lam in (.01, .03, .05):
    Ji = math.sqrt(10 / 3) * lam * Jscale
    for eta in (0.0, .5, 1.0):
        dj = max(0.0, Ji - math.sqrt(eta) * Jcmax)
        rl = launch_min(dj)
        if rl:
            cap = 2 * Me * Q * rl**2 + 2 * G * Mc * Me**2 * rl
            assert math.isclose(cap, dj**2, rel_tol=2e-14)
        rows.append(dict(initial_lambda=lam, core_ordered_kinetic_fraction_eta=eta,
                         delta_J_Msun_pc_kms=dj, receiver_sphere_min_pc=rl,
                         min_pc_if_sphere_must_enclose_core=max(Rc, rl),
                         bound_envelope_Rout_over_Ri=dj**2/(2*G*M*Me**2*Ri)))

result = dict(
    hypotheses="Conditional spherical Newtonian uniform endpoints and negligible-self-gravity particle receiver; no physical trajectory computed",
    assertion_tested="Displayed benchmark arithmetic, positive-root flux equality, zero-J and zero-energy limits only",
    input=dict(G_pc_kms2_per_Msun=G, M_Msun=M, q=q, Rc_pc=Rc, aperture_pc=Ra, Ri_pc=Ri),
    core_fraction_max_closed_shell_bound=math.sqrt(1.2*Rc/Ri),
    aperture_fraction_max_closed_Ri_5R=math.sqrt(1.2/5),
    max_Ri_over_Rc_closed_shell=1.2/q**2,
    max_Ri_over_Rc_uniform_core=1/q**2,
    export_uniform_Msun_kms2=Q,
    export_shell_min_Msun_kms2=max(0.0,Ei+G*Mc**2/(4*Rc)),
    export_uniform_J=Q*1.98892e36,
    ejecta_vinf_rms_kms=math.sqrt(2*Q/Me),
    core_Jmax_Msun_pc_kms=Jcmax,
    zero_core_J_bound_envelope_Rout_over_Ri={str(lam):(5/3)*(lam/(1-q))**2 for lam in (.01,.03,.05)},
    approximate_CFG848_P1=dict(Ei=-.117, rg=7, assumed_free_core_mass=4.9,
                              free_mass_max_B0=math.sqrt(-4*7*(-.117)),
                              B_min_for_assumed_mass=2*(-.117)+4.9**2/(2*7)),
    rows=rows,
    runtime_seconds=time.monotonic()-start,
    max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    python=sys.version,
)
out = pathlib.Path(sys.argv[1])
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
