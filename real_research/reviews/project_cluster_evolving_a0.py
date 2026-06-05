#!/usr/bin/env python3
"""
Does EVOLVING a0 = cH(z)/Z make the MOND CLUSTER PROBLEM better, worse, or unchanged?
=====================================================================================
The MOND cluster problem (Sanders 2003; Pointecouteau & Silk 2005; The & White 1988;
Angus, Famaey & Buote 2008): even DEEP in the MOND regime, MOND under-predicts the
dynamical mass of relaxed clusters by ~2x. The "residual missing mass". Constant-a0
MOND does not fix it without extra mass (2 eV neutrinos / unseen baryons).

This framework's DISTINCTIVE claim: a0 EVOLVES as a0(z)=cH(z)/Z = a0(0) E(z), so a0
was LARGER at higher z by E(z)=sqrt(0.315(1+z)^3+0.685).

THE QUESTION (Carl): does evolving a0 make the cluster problem BETTER, WORSE, or
UNCHANGED? Carl's prior: larger a0 at high z => M_MOND ~ V^4/(G a0) is SMALLER for the
same velocity => predicted mass DOWN => discrepancy M_dyn/M_MOND UP => WORSE.

THE CRUX (why the repo currently contradicts itself). "The discrepancy" is not one
number -- a0(z) moves two different anchors in OPPOSITE directions:

  (A) FIX the OBSERVED kinematics (velocity dispersion / g_obs -- what you MEASURE in a
      cluster). MOND deep-regime: M_MOND = V^4/(G a0). Larger a0 => SMALLER predicted
      M_MOND => the mass you must explain away (M_dyn/M_MOND) gets BIGGER. WORSE.
      This is Carl's framing, and it is the one the cluster problem is actually posed in:
      the velocity dispersion / X-ray g_obs is the datum; M_MOND is the prediction from it.

  (B) FIX the BARYONS (M_b) and ask how much dynamical mass MOND MANUFACTURES.
      M_MOND = M_b * nu(g_bar/a0). Larger a0 => larger boost nu => MORE manufactured
      mass => residual (M_dyn/M_b)/nu gets SMALLER. BETTER.
      This is what cluster_residual_evolution.py / project16_clusters.py / the xray
      forecast compute (R ~ R0/sqrt(E)).

Both are correct algebra. They disagree because they hold different things fixed. So the
honest resolution is: WHICH anchor is "the cluster problem"? Answer below -- and it is (A).
Needs numpy only.
"""
import numpy as np

# --- constants & cosmology ---
G, Msun, kpc, Mpc = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
A0 = 1.2e-10
Om, OL = 0.315, 0.685
E  = lambda z: np.sqrt(Om*(1+z)**3 + OL)            # a0(z)/a0(0) = cH(z)/cH(0)
nu = lambda x: 0.5*(1.0 + np.sqrt(1.0 + 4.0/x))     # simple interpolation, M_MOND/M_b


def banner(s, ch="="):
    print(ch*86); print(s); print(ch*86)


def main():
    banner("# Evolving a0 vs the MOND cluster problem -- direction & magnitude", "#")
    print()

    # ---------------------------------------------------------------- (1) E(z)
    banner("(1) E(z) = a0(z)/a0(0): a0 was LARGER at higher z")
    ZS = [0.2, 0.5, 1.0, 1.5]
    for z in ZS:
        print(f"   z={z:<4} E(z)={E(z):.4f}  ->  a0(z) = {E(z):.3f} x a0(today)")
    print()

    # --------------------------------------- (2A) FIXED-VELOCITY anchor (the real problem)
    banner("(2A) THE CLUSTER PROBLEM AS ACTUALLY POSED: fix the kinematics, M_MOND ~ V^4/(G a0)")
    print("""  Deep-MOND, isothermal/flat regime: the OBSERVED quantity is the velocity dispersion
  (X-ray: g_obs from kT and the density+temperature gradients). MOND PREDICTS the enclosed
  mass from it:  g_obs = sqrt(a0 g_bar)  =>  g_bar = g_obs^2/a0  =>  M_MOND(<r)=g_bar r^2/G
  = (g_obs r)^2 /(G a0) = V^4/(G a0). The 'missing mass' the cluster problem reports is
       D(z) = M_dyn / M_MOND ,  with M_dyn FIXED by the (z-independent) kinematics.
  Since M_MOND ~ 1/a0 and a0(z)=a0(0)E(z):   D(z) = D(0) * E(z).   Larger a0 -> WORSE.\n""")
    D0 = 1.9    # z~0 residual missing-mass factor (the classic ~2x; Sanders/Pointecouteau-Silk)
    print(f"   anchoring D(0) = {D0} (the classic factor ~2):")
    print(f"   {'z':>5}{'E(z)':>8}{'M_MOND(z)/M_MOND(0)':>22}{'D(z)=D0*E(z)':>16}{'vs const-a0 D=1.9':>20}")
    for z in [0.0]+ZS:
        Mfac = 1.0/E(z)                 # M_MOND shrinks as 1/a0
        D = D0*E(z)
        print(f"   {z:>5.1f}{E(z):>8.3f}{Mfac:>22.3f}{D:>16.2f}{D/D0:>18.2f}x")
    print(f"\n   => the discrepancy GROWS by exactly E(z): x{E(0.5):.2f} at z=0.5, x{E(1.0):.2f} at z=1.0.")
    print(f"      At z=0.5 you must hide {D0*E(0.5):.1f}x the baryons (vs {D0:.1f}); at z=1.0, {D0*E(1.0):.1f}x. WORSE.\n")

    # --------------------------------------- (2B) FIXED-BARYON anchor (what the repo computed)
    banner("(2B) THE OTHER ANCHOR (what cluster_residual_evolution.py used): fix baryons, M_MOND=M_b*nu")
    print("""  If instead you FIX the baryons and ask how much mass MOND manufactures, the boost nu
  grows with a0, so the residual R=(M_dyn/M_b)/nu(g_bar/a0) SHRINKS as ~1/sqrt(E(z)). This
  is real algebra too -- but it answers a DIFFERENT question ('does MOND make more mass from
  the same gas at high z', yes) than the cluster problem ('given the kinematics, how much is
  still unexplained', which is 2A). Shown for completeness / to reconcile the two scripts:\n""")
    # representative deep-MOND cluster region: g_bar/a0(0) = 0.05 (eRASS1 R500 median ~ 0.03-0.06)
    gx = 0.05
    R0 = 6.5/nu(gx)                     # (M_dyn/M_b)=6.5, boost at z=0
    print(f"   region g_bar/a0(0)={gx}, M_dyn/M_b=6.5:")
    print(f"   {'z':>5}{'E(z)':>8}{'boost nu(z)':>13}{'residual R(z)':>15}{'R0/sqrt(E)':>13}")
    for z in [0.0]+ZS:
        x = gx/E(z)
        R = 6.5/nu(x)
        print(f"   {z:>5.1f}{E(z):>8.3f}{nu(x):>13.2f}{R:>15.2f}{R0/np.sqrt(E(z)):>13.2f}")
    print(f"\n   => residual FALLS ~1/sqrt(E): x{1/np.sqrt(E(0.5)):.2f} at z=0.5, x{1/np.sqrt(E(1.0)):.2f} at z=1.0. 'BETTER' on THIS anchor.\n")

    # --------------------------------------- (3) which anchor IS the cluster problem
    banner("(3) WHICH ANCHOR IS 'THE CLUSTER PROBLEM'?  -> (2A), the fixed-kinematics one")
    print("""  The literature factor-2 (Sanders 2003; The & White 1988; Pointecouteau & Silk 2005;
  Angus+2008; Blaksley & Bonamente 2009) is derived by taking the cluster's MEASURED
  kinematics (X-ray temperature/velocity dispersion = M_dyn) and comparing to what MOND
  predicts FROM THE BARYONS. The deficit is reported as 'a0 you would NEED to fit it':
  B&B find a0_required ~ 10-13x the galaxy a0. That 'needed a0' is exactly anchor (2A):
       M_MOND ~ a0  must be raised ~10x to match M_dyn  <=>  D = M_dyn/M_MOND ~ 10 at the
       galaxy a0.  Evolving a0 RAISING a0 by E(z) helps in the SAME direction as 'needed a0'
       only if E(z) is the thing being raised at FIXED kinematics. BUT the catch:
  - The clusters where D~2-10 is measured sit at z<0.3 (Coma, X-COP) to z~0.9 (B&B). At
    those z, E(z) is 1.0-1.45 -- it raises a0 by at most ~45%, against a needed ~10x. The
    EXISTING low-z discrepancy is NOT reduced (a0(0) is the z=0 value, unchanged).
  - For a cluster OBSERVED at z=0.5 or 1.0, the relevant a0 is the LARGER a0(z). With the
    kinematics fixed by observation, that larger a0 makes M_MOND SMALLER, so the SAME
    cluster has a LARGER inferred missing-mass factor than if you (wrongly) used a0(0).\n""")

    # --------------------------------------- (4) net effect on the problem as a whole
    banner("(4) NET DIRECTION: WORSE (modestly), and a NEW z-trend the problem did not have")
    print(f"""  * At FIXED kinematics (the way the cluster problem is posed), evolving a0 multiplies the
    missing-mass factor by E(z): x{E(0.5):.2f} at z=0.5, x{E(1.0):.2f} at z=1.0. So a z=1 cluster's residual
    is ~1.8x WORSE than the z~0 factor-2, i.e. you must now hide ~{1.9*E(1.0):.1f}x the baryons.
  * The famous LOW-z factor-2 itself is UNCHANGED (it is set by a0(0), which the framework
    keeps at 1.2e-10). Evolving a0 does not touch the canonical Coma/X-COP discrepancy.
  * NEW exposure: evolving a0 PREDICTS a rising missing-mass trend D(z)=D0 E(z) at fixed
    kinematics -- a falsifiable z-trend that constant-a0 MOND does NOT predict (flat D).
    A homogeneous cluster sample would test it; the direction of the prediction is 'worse
    at high z', so high-z cluster data can only hurt, never help, the framework here.\n""")

    # --------------------------------------- (5) reconcile the repo's two readings
    banner("(5) RECONCILING THE REPO (the apparent contradiction is anchor choice, not a bug)")
    print("""  cluster_residual_evolution.py / project16 / the xray forecast got R ~ R0/sqrt(E) FALLING
  -- because they FIXED THE BARYONS (M_MOND=M_b*nu) and let MOND manufacture more mass. That
  answers 'does MOND make more dark mass from the same gas at high z?' (yes, sqrt(E)). It does
  NOT answer 'is the cluster MORE under-massed given its kinematics?' which is the cluster
  problem -- and there the answer is the OPPOSITE: D ~ E(z), WORSE. Both are in this repo; the
  honest statement is that the cluster PROBLEM (kinematics-anchored) gets WORSE with z.

  Note the magnitudes are different (E vs sqrt(E)) because the fixed-baryon reading sits in the
  deep-MOND nu~sqrt regime (nu ~ sqrt(a0/g_bar) ~ sqrt(E)), while the fixed-kinematics reading
  is the full M_MOND ~ 1/a0 ~ 1/E. The deep-MOND M_dyn ~ sqrt(M_b a0) 'half-helps' the baryon
  view precisely because it 'double-hurts' the kinematic view -- same physics, two ledgers.\n""")

    banner("HONEST VERDICT")
    print(f"""  DIRECTION: WORSE (modestly), at the redshifts clusters actually exist.
  - Fixed-kinematics (the cluster problem as posed): D(z) = D(0) * E(z).
       z=0.5 -> x{E(0.5):.2f} WORSE ; z=1.0 -> x{E(1.0):.2f} WORSE. A z=1 cluster's residual goes
       ~factor-2 -> ~factor-{1.9*E(1.0):.1f}.
  - The canonical low-z factor-2 is UNCHANGED (set by a0(0)).
  - Fixed-baryon reading (different question) 'improves' ~1/sqrt(E) (x{1/np.sqrt(E(0.5)):.2f}, x{1/np.sqrt(E(1.0)):.2f}),
       but that is NOT the cluster problem and should not be sold as a fix.

  IS IT A NEW TENSION OR A WORSENING OF AN EXISTING ONE?  A WORSENING + a new z-trend:
  evolving a0 inherits the full constant-a0 cluster failure (unchanged at z~0) AND adds a
  rising-with-z missing-mass prediction (D ~ E(z)) that constant-a0 MOND does not carry. So
  the distinctive claim takes an EXTRA strike here: it cannot help clusters (the ~10x 'needed
  a0' is reached only at z~6, where clusters don't exist -- B&B), and at the high-z end it makes
  the deficit larger. Carl's prior is CONFIRMED by the arithmetic: larger a0 at high z makes the
  MOND-predicted mass smaller at fixed kinematics, so the cluster discrepancy gets WORSE.""")
    print("="*86)


if __name__ == "__main__":
    main()
