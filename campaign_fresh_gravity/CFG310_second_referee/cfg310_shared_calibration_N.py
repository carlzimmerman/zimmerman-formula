#!/usr/bin/env python3
"""CFG310: how many gated galaxies reach expected odds of 20:1 when a baryonic-mass calibration error delta_c is shared by the sample?
Re-implements the KL divergence of the MNRAS v3.2 design (Section 4.4, Table 12: per-galaxy variance s^2 I plus shared sigma_C^2 J,
sigma_C = A_bar delta_c, A_bar = 1.52 at y = 0.2; intrinsic 0.09 dex, halo-to-halo 0.13 dex; Delta = paper_numbers S4.laws[2].gate).
Validates against Table 12 (8 at 0.20 dex: 20:1 at delta_c = 0, 6.2:1 at 0.05, 2.5:1 at 0.10), then scans N.  Post hoc referee check;
kappa = 1/2 FITTED.  Writes cfg310_shared_calibration_N.out."""
import os, json, numpy as np
np.seterr(all='ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
PN = json.load(open(os.path.join(HERE, "..", "..", "qwen_claude_field_theory", "papers_2026", "mnras_submission_2026_v3", "paper_numbers.json")))
D = PN["S4"]["laws"][2]["gate"]; SI, SH, AB = 0.09, 0.13, 1.52


def kl(m0, C0, m1, C1):
    n = len(m0); dm = m1 - m0
    return 0.5 * (np.trace(np.linalg.solve(C1, C0)) + dm @ np.linalg.solve(C1, dm) - n + np.linalg.slogdet(C1)[1] - np.linalg.slogdet(C0)[1])


def odds(N, sm, dc, delta=D, sh=SH):
    I, J = np.eye(N), np.ones((N, N)); sc2 = (AB * dc) ** 2
    s0 = sm ** 2 + SI ** 2; s1 = s0 + sh ** 2
    C0 = s0 * I + sc2 * J; C1 = s1 * I + sc2 * J
    m0 = np.zeros(N); m1 = np.full(N, delta)
    return float(np.exp(min(min(kl(m0, C0, m1, C1), kl(m1, C1, m0, C0)), 700.0)))


out = [f"Delta = {D:.4f} (gated halo law), sigma_m = 0.20 dex, intrinsic {SI}, halo {SH}, A_bar {AB}"]
out.append("validation against Table 12 (8 galaxies at 0.20 dex): " + ", ".join(f"delta_c {dc:.2f} -> {odds(8, 0.20, dc):.1f}:1" for dc in (0.0, 0.05, 0.10)))
for dc in (0.0, 0.02, 0.03, 0.04, 0.05, 0.06):
    Ns = [n for n in range(2, 401) if odds(n, 0.20, dc) >= 20]
    out.append(f"delta_c {dc:.2f}: odds at N = 8, 20, 50, 200, 400: " + ", ".join(f"{odds(n, 0.20, dc):.1f}" for n in (8, 20, 50, 200, 400))
               + f"  | smallest scanned N reaching 20:1: {Ns[0] if Ns else '> 400'}")
out.append("dispersion alone (Delta = 0, delta_c = 0; the halo law differs only by its extra halo-to-halo scatter): odds at N = 8, 20, 50: "
           + ", ".join(f"{odds(n, 0.20, 0.0, delta=0.0):.1f}" for n in (8, 20, 50)))
out.append("dispersion alone if sigma_m were underestimated (true 0.25, assumed 0.20) is not computed here; the point is that part of the expected"
           " odds comes from the variance difference, which depends on knowing sigma_m and sigma_int.")
out.append("Reading: the abstract's 'about eight lensed discs ... and a common calibration good to 0.06 dex' are not jointly sufficient: eight discs reach"
           " 20:1 only at delta_c = 0 (8.4:1 at 0.04, 4.8:1 at 0.06); at delta_c = 0.05 and 0.06 about 21 and 36 discs are needed (smallest N above); the extra odds at large N come mainly from the dispersion term.")
open(os.path.join(HERE, "cfg310_shared_calibration_N.out"), "w").write("\n".join(out) + "\n"); print("\n".join(out))
