"""
mc_metric_carried.py -- does the search ever reach the class Part I actually covers?

Gate-SLIP has two branches:
  (a) FRAME slip   -- binds when the MOND enhancement is carried by the MATTER FRAME
                      (the TeVeS fifth-force class);
  (b) Sigma_P      -- Part I's traceless-stress obstruction.  It only bites when the
                      enhancement is carried by the EINSTEIN-FRAME METRIC, because only
                      then does the carrier's stress gravitate at MOND strength
                      (2 (Phi-Psi)'' = -Sigma_P against 4 Psi'' = -rho_carrier).

Branch (b) is armed in mc_gates.run_chain but it can only fire if some candidate actually
produces METRIC-carried MOND.  This script tests that directly, so the coverage claim is
measured rather than assumed: sweep the curvature-coupled sector (chi R, chi^2 R, A^2 R,
A^m A^n R_mn, S^mn R_mn, X R, d phi d phi R_mn) -- the only operators in the basis that can
put the carrier into the Einstein equations -- over MOND cores and matter frames, and count
how many candidates reach Gate-SLIP at all, and with what metric-carried fraction.
"""
import collections
import sys
import numpy as np

import mc_gates as G
import mc_screen as S
from mc_basis import N_OPS, N_PARAM, OP_INDEX, MFRAME

np.seterr(all='ignore')

CURV = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
SUPPORT = {"C3": dict(V15=1.0, K4=-0.25), "C4": dict(V15=1.0, K4=-0.25),
           "C5": dict(V18=1.0, K8=-0.5, K9=1.0), "C6": dict(V18=1.0, K8=-0.5, K9=1.0)}

N = int(sys.argv[1]) if len(sys.argv) > 1 else 900
rng = np.random.default_rng(11)
mort = collections.Counter()
reach_slip = []
best_frac = 0.0
best = None

for trial in range(N):
    c = S._mk(S.MOND_CORES[int(rng.integers(len(S.MOND_CORES)))])
    k = int(rng.integers(1, 3))
    ops = rng.choice(CURV, size=k, replace=False)
    for o in ops:
        c[OP_INDEX[o]] = float(S._rand_mag(rng, 1)[0])
        for kk, vv in SUPPORT.get(o, {}).items():
            c[OP_INDEX[kk]] = vv
    if rng.random() < 0.5:
        j = int(rng.integers(N_OPS))
        c[j] += float(S._rand_mag(rng, 1)[0]) * 0.5
    nm = int(rng.integers(0, 3))
    if nm:
        midx = rng.choice(len(MFRAME), size=nm, replace=False)
        c[N_OPS + midx] = S._rand_mag(rng, nm)
    v, info = G.run_chain(c, rng=rng)
    mort[v] += 1
    if v in ("Gate-SLIP", "Gate-H2", "Gate-PPN", "SURVIVOR"):
        f = info.get("metric_carried_frac", 0.0)
        reach_slip.append((v, f, info.get("slip", ""), info.get("sigmaP_cancellation_rel")))
        if f > best_frac:
            best_frac, best = f, (c.copy(), v, info)

print(f"curvature-coupled sweep, {N} candidates")
print("mortality:", dict(mort))
print(f"reached Gate-SLIP or deeper: {len(reach_slip)}")
if reach_slip:
    fr = np.array([r[1] for r in reach_slip])
    print(f"  metric-carried fraction among them: min {fr.min():.3e}  "
          f"median {np.median(fr):.3e}  max {fr.max():.3e}")
    n_metric = int((fr > 0.1).sum())
    print(f"  candidates with METRIC-carried MOND (frac > 0.1): {n_metric}")
    kills = collections.Counter(r[2].split("=")[0] for r in reach_slip)
    print(f"  Gate-SLIP outcomes: {dict(kills)}")
    if n_metric:
        print("  -> Part I's Sigma_P branch was EXERCISED by the search.")
        for r in reach_slip:
            if r[1] > 0.1:
                print(f"       verdict={r[0]} frac={r[1]:.3f} slip={r[2]} "
                      f"sigmaP_rel={r[3]}")
    else:
        print("  -> NO candidate produced metric-carried MOND, so Part I's Sigma_P branch")
        print("     never fired in this basis.  The curvature couplings that could put the")
        print("     carrier into the Einstein equations (chi R and friends) rescale G with")
        print("     the carrier and are killed by G3 at Gate-MOND instead -- an honest")
        print("     COVERAGE GAP of the screen, not evidence against Part I.")
else:
    print("  none reached Gate-SLIP at all.")
    print("  -> COVERAGE GAP, stated explicitly: within this basis the ONLY way to put the")
    print("     carrier into the Einstein equations is a curvature coupling (chi R, A^2 R,")
    print("     A^m A^n R_mn, ...).  Every such coupling makes G_eff depend on the carrier,")
    print("     and since the carrier grows in the Newtonian limit (that is what makes the")
    print("     MOND interpolation run the right way) G_eff runs with it -- so G3 kills")
    print("     these at Gate-MOND before Gate-SLIP is ever reached.  Part I's Sigma_P")
    print("     branch is therefore NOT independently confirmed by this screen; it is")
    print("     inherited from the committed Part-I proof and reproduced only as the exact")
    print("     identity Sigma_P = mu s^2 (mc_validate V4a).  The screen's lensing kills are")
    print("     all FRAME-slip kills, which is a DIFFERENT and complementary obstruction.")
