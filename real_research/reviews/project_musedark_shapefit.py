#!/usr/bin/env python3
"""
MUSE-DARK III shape test: rising a0 SUPPORTED, but the specific a0 ∝ E(z) shape is mildly disfavored.
====================================================================================================
The framework's distinctive bet is really TWO claims: (1) a0 RISES with z (apparent, not event, horizon);
(2) a0 ∝ E(z)=sqrt(Om(1+z)^3+OL) exactly (= cH(z)/Z). MUSE-DARK III (A&A 2026) lets us test both. Fitting
their points: CONSTANT a0 is strongly rejected (chi2/dof~8) -> claim (1) SUPPORTED; but A*E(z) (chi2/dof~2.5)
fits worse than a LINEAR rise (chi2/dof~1.3) -> claim (2) mildly disfavored: the data rise more LINEARLY than
E(z). Honest split: the apparent-horizon DIRECTION is favored; the exact cH(z)/Z RATE is so-so. Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
# approx MUSE-DARK III points (z, a0[1e-10], sigma): local SPARC anchor + bins/global
PTS = [(0.0, 1.20, 0.26), (0.33, 1.99, 0.18), (1.0, 2.38, 0.11), (1.44, 2.71, 0.22)]


def main():
    print("#"*92); print("# MUSE-DARK III shape test -- rising YES, a0 ∝ E(z) shape so-so"); print("#"*92 + "\n")
    z = np.array([p[0] for p in PTS]); a = np.array([p[1] for p in PTS]); s = np.array([p[2] for p in PTS])
    fz = E(z); A = np.sum(a*fz/s**2)/np.sum(fz**2/s**2); chi_fw = np.sum(((a-A*fz)/s)**2)
    Ac = np.sum(a/s**2)/np.sum(1/s**2); chi_c = np.sum(((a-Ac)/s)**2)
    Xl = np.vstack([np.ones_like(z), z]).T; W = np.diag(1/s**2)
    cl = np.linalg.solve(Xl.T@W@Xl, Xl.T@W@a); chi_l = np.sum(((a-Xl@cl)/s)**2)
    print("="*92); print("THE FIT (approximate MUSE-DARK III points; honest within their error bars)"); print("="*92)
    print(f"  {'model':22}{'params':>8}{'chi2':>8}{'chi2/dof':>10}")
    print(f"  {'constant a0':22}{1:>8}{chi_c:>8.1f}{chi_c/(len(z)-1):>10.1f}   -> REJECTED (data rise)")
    print(f"  {'framework A*E(z)':22}{1:>8}{chi_fw:>8.1f}{chi_fw/(len(z)-1):>10.1f}   -> fits the rise, shape imperfect")
    print(f"  {'linear a0(0)+a1 z':22}{2:>8}{chi_l:>8.1f}{chi_l/(len(z)-2):>10.1f}   -> best (data rise ~linearly)")
    print(f"\n  framework E(z) prediction (A=1.2): {[f'{1.2*E(zz):.2f}' for zz in z]}  vs measured {list(a)}")
    print(f"  (matches at high z: 2.75 vs 2.71 @ z=1.44; too shallow at low z: 1.43 vs 1.99 @ z=0.33.)\n")
    print("="*92); print("VERDICT -- the two claims, separated"); print("="*92)
    print("""  CLAIM 1 (a0 RISES -- apparent vs event horizon): SUPPORTED. Constant a0 is rejected at chi2/dof~8 by
  MUSE-DARK III. The framework's core distinctive bet -- that a0 tracks the apparent horizon and increases with
  z -- is favored by the latest dedicated data.
  CLAIM 2 (a0 ∝ E(z) exactly -- the cH(z)/Z form): MILDLY DISFAVORED. A*E(z) (chi2/dof~2.5) fits worse than a
  linear rise (chi2/dof~1.3); the data rise more LINEARLY than E(z) (steep at low z, where a systematic in the
  MUSE-DARK low-z bins is also possible -- their own a0(0) fit is 1.0, below the adopted 1.2).
  NET: the apparent-horizon DIRECTION is observationally favored; the SPECIFIC cH(z)/Z rate is not yet the best
  description -- the real a0(z) law looks more linear in z than E(z). A concrete, falsifiable refinement target,
  and exactly the kind of thing the gas-clean z~3 measurement (project 17) pins down. Honest: a partial win
  (rising) plus a specific, testable tension (the E(z) shape).""")
    print("="*92)


if __name__ == "__main__":
    main()
