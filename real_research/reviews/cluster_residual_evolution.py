#!/usr/bin/env python3
"""
The relaxed-cluster residual-mass problem -- does evolving a0 do anything?
=========================================================================
This is the DEEPER, less-contested MOND cluster weakness (separate from the
Bullet offset): even after the MOND boost, MOND under-predicts relaxed-cluster
dynamical masses by a factor ~2 (Sanders 2003; Angus, Famaey & Buote 2008;
Pointecouteau & Silk 2005). Standard fix: ~2 eV neutrinos / hot dark matter.

QUESTION (Carl): does a0(z) = a0(0) E(z) help, and is the prediction distinctive?

PHYSICS. For a system with baryonic mass M_b inside r, g_N = G M_b/r^2, the MOND
boost is nu(g_N/a0) and the MOND-predicted dynamical mass is M_MOND = M_b nu.
The observed discrepancy is the residual
        R(z) = M_dyn / M_MOND = (M_dyn/M_b) / nu(g_N / a0(z)).
Because nu INCREASES as a0 increases, R(z) DECREASES with redshift. In deep MOND
(nu -> sqrt(a0/g_N)) this is the clean scaling R(z) ~ R(0)/sqrt(E(z)).

  nu(x) = 1/2 [1 + sqrt(1 + 4/x)]   (simple interpolation; x = g_N/a0)

  => DISTINCTIVE: constant-a0 MOND predicts R ~ const with z; this framework
     predicts R falls as ~1/sqrt(E(z)). Run: python <thisfile>  (numpy only).
"""
import numpy as np

G, Msun, kpc, Mpc = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
A0 = 1.2e-10
E  = lambda z: np.sqrt(0.315*(1+z)**3 + 0.685)
nu = lambda x: 0.5*(1.0 + np.sqrt(1.0 + 4.0/x))          # boost M_MOND/M_b


def g_N(M_b, r):
    return G*M_b/r**2


def residual(Mdyn_over_Mb, M_b, r, z):
    x = g_N(M_b, r)/(A0*E(z))
    return Mdyn_over_Mb / nu(x)


# Two representative regions of a massive relaxed cluster (Coma-like).
# Numbers ~ Sanders 2003 / Angus+2008 scale: M_dyn/M_b ~ 6-7; residual ~2 at z=0.
REGIONS = [
    # name,                 r,        M_b,       Mdyn/Mb
    ("deep-MOND outskirt (r=1.5 Mpc)", 1.5*Mpc, 1.5e14*Msun, 6.5),
    ("transition core   (r=0.25 Mpc)", 0.25*Mpc, 2.0e13*Msun, 6.5),
]
ZS = [0.0, 0.3, 0.5, 1.0, 1.5, 2.0]


def confront_data():
    """Confront the prediction with Blaksley & Bonamente 2009 (38 clusters, Chandra)."""
    print("="*82)
    print("HARD DATA: Blaksley & Bonamente 2009 (38 clusters, z=0.14-0.89, Chandra)")
    print("="*82)
    a0_gal = 1.17e-8          # cm/s^2, galaxy/canonical value
    a0_req = 1.49e-7          # cm/s^2, mean a0 REQUIRED to fit clusters (no DM), at r2500
    ratio  = a0_req/a0_gal
    # what redshift would the framework need to supply that a0?
    Eneed  = ratio
    z_need = ((Eneed**2 - 0.685)/0.315)**(1/3) - 1
    print(f"  They solve for the a0 REQUIRED to make MOND fit each cluster (f_baryon=1):")
    print(f"     a0_required (mean, r2500) = {a0_req:.2e} cm/s^2")
    print(f"     a0_galaxy   (canonical)   = {a0_gal:.2e} cm/s^2")
    print(f"     => clusters need a0 about {ratio:.0f}x the galaxy value (one order of magnitude).")
    print(f"  This framework gives a0(z)=a0(0)E(z). To reach {ratio:.0f}x you need E(z)={Eneed:.0f},")
    print(f"     i.e. z ~ {z_need:.1f} -- where galaxy CLUSTERS DO NOT EXIST (structure unformed).")
    print(f"     At the highest real cluster redshifts the boost is tiny by comparison:")
    for z in (0.5, 0.89, 1.5, 2.0):
        print(f"        z={z:<4} E(z)={E(z):.2f}  -> a0 up x{E(z):.2f}  (need x{ratio:.0f}; gap x{ratio/E(z):.1f})")
    print(f"""
  TWO independent reasons evolving a0 CANNOT solve clusters:
   (1) NORMALISATION: clusters want a0 ~10x; evolution reaches that only at z~6,
       where there are no clusters. At z<=2 the gap is still ~3-4x.
   (2) SHAPE: B&B find the required a0 VARIES WITH RADIUS within a cluster and
       BETWEEN clusters -- so it is not a single missing normalisation at all. No
       a0(z), constant OR evolving, can fix a discrepancy whose 'needed a0' is not
       even constant inside one cluster. Clusters are a STRUCTURAL MOND failure.\n""")


def main():
    confront_data()
    print("="*82)
    print("RELAXED-CLUSTER MOND RESIDUAL vs REDSHIFT  (R = (M_dyn/M_b)/nu(g_N/a0(z)))")
    print("="*82)
    for name, r, M_b, ratio in REGIONS:
        x0 = g_N(M_b, r)/A0
        print(f"\n  {name}")
        print(f"    g_N = {g_N(M_b,r):.2e} m/s^2 = {x0:.3f} a0(0)   (M_dyn/M_b = {ratio})")
        print(f"    {'z':>5}{'E(z)':>7}{'a0(z)/a0':>9}{'boost nu':>10}{'residual R(z)':>15}"
              f"{'1/sqrt(E) law':>15}")
        R0 = residual(ratio, M_b, r, 0.0)
        for z in ZS:
            x = g_N(M_b, r)/(A0*E(z))
            R = residual(ratio, M_b, r, z)
            print(f"    {z:>5.1f}{E(z):>7.2f}{E(z):>9.2f}{nu(x):>10.2f}{R:>15.2f}"
                  f"{R0/np.sqrt(E(z)):>15.2f}")
    print("\n"+"="*82); print("WHAT THIS MEANS -- honestly (after confronting the data)"); print("="*82)
    print("""  [DISTINCTIVE, but small] The framework predicts the MOND cluster residual
    FALLS with z as ~1/sqrt(E(z)) (deep-MOND). Across the B&B sample (z=0.14-0.89)
    that is only ~20% -- WITHIN the cluster-to-cluster scatter in the required a0,
    and confounded by selection (high-z X-ray clusters are hotter -> less deep-MOND
    -> LARGER residual, which masks or reverses the predicted decline). So this
    sample neither confirms nor refutes it. A re-analysis of required-a0 vs z at
    FIXED temperature would be the real test; the predicted signal is marginal.

  [LIMIT -- the honest headline] Evolving a0 does NOT solve clusters, and the data
    make this sharper than the Bullet:
    - clusters need a0 ~10x the galaxy value (B&B 2009; Angus+08; Pointecouteau &
      Silk 05). The framework reaches 10x only at z~6, where clusters don't exist.
    - the required a0 varies WITH RADIUS and BETWEEN CLUSTERS -- a structural/shape
      failure, not a missing normalisation. No a0(z) can fix a 'needed a0' that is
      not even constant within one cluster.
    - so the relaxed-cluster residual is a GENUINE, inherited, structural MOND
      failure that a0-evolution reframes ('a0 was larger then') but cannot cure.

  NET: unlike the Bullet (contested, possibly OK), the relaxed-cluster residual is
  a real and fairly decisive MOND shortfall, and evolving a0 buys only a marginal,
  currently-untestable improvement. Honest -- this is a place the framework, and
  MOND generally, still fails.

  CORRECTION (do not soft-pedal this): the residual-vs-z IS a genuine test of the
  DISTINCTIVE evolving-a0 claim -- so it is wrong to wave clusters away as 'only
  the foundational MOND risk, not a wound to the novelty'. They test the novelty.
  And the dominant confound runs the WRONG way for us: flux-limited high-z samples
  select the hottest, most massive clusters (higher g_N/a0 -> less boost -> LARGER
  residual / higher required-a0 with z), an effect ~20-30%, comparable to or bigger
  than our predicted ~20% DECLINE. So the raw cluster trend, if anything, leans
  AGAINST evolving a0. It is not a free pass -- it is an open test currently tilted
  against the distinctive claim, pending a fixed-temperature re-analysis.""")
    print("="*82)


if __name__ == "__main__":
    main()
