#!/usr/bin/env python3
"""
Clusters with THE ACTUAL FORMULA: a0 = (c/2) sqrt(G rho), rho = LOCAL density.
=============================================================================
I previously tested clusters with a0(z) = a0(0) E(z) -- i.e. a0 set by the COSMIC
mean density only, evolving with redshift. That is NOT the framework's content.
The formula is a0 = (c/2) sqrt(G rho): a0 is set by the DENSITY. A cluster is a
density ENHANCEMENT, so inside it a0 should be LARGER than cosmic -- by sqrt of the
overdensity. Blaksley & Bonamente (2009) find clusters need a0 ~10-13x the galaxy
value; sqrt(overdensity ~100-200) ~ 10-14x. That is the test I should have run.

THE CRUX is *which* rho. We check three readings honestly:
  (L) local CLUMPY density at the dynamical radius,
  (A) ambient density smoothed on a LARGE (~Mpc) scale,
  (C) cosmic mean (what I wrongly used everywhere).
The galaxy RAR (universal a0 = 1.2e-10) is the hard constraint any reading must pass.

Run: python <thisfile>  (numpy only).
"""
import numpy as np

c, G, Msun, kpc, Mpc, pc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22, 3.0857e16
H0 = 67.4e3/Mpc
rho_crit = 3*H0**2/(8*np.pi*G)                    # cosmic critical density today
a0 = lambda rho: 0.5*c*np.sqrt(G*rho)             # THE FORMULA
A0c = a0(rho_crit)                                 # a0 at cosmic density
nu  = lambda x: 0.5*(1+np.sqrt(1+4/x))            # MOND boost M_MOND/M_b


def line(env, rho):
    print(f"   {env:42s} rho/rho_crit={rho/rho_crit:10.3g}  a0={a0(rho):.2e}  "
          f"= {a0(rho)/A0c:8.2g} x cosmic")


def main():
    print("="*84)
    print(f"THE FORMULA a0=(c/2)sqrt(G rho):  a0(cosmic rho_crit) = {A0c:.2e} m/s^2  (=> 1.2e-10 OK)")
    print("="*84)

    print("\n  (C) COSMIC reading -- what I wrongly used for clusters:")
    line("cosmic mean (any system, this reading)", rho_crit)
    print("      -> clusters get NO boost. This is the strawman I tested. WRONG per the formula.\n")

    print("  (L) LOCAL CLUMPY density at the dynamical radius:")
    # galaxy disk at the MOND transition: Sigma_dagger = a0/(2 pi G) ~137 Msun/pc^2, h~300 pc
    Sig = A0c/(2*np.pi*G); rho_disk = Sig/(2*300*pc)
    line("galaxy disk @ MOND radius (Freeman/h~300pc)", rho_disk)
    # cluster gas at r2500: n_e ~ 1e-3 cm^-3
    rho_gas = 1e-3*1e6 * 1.17*1.67e-27
    line("cluster gas @ r2500 (n_e~1e-3 cm^-3)", rho_gas)
    print("      -> KILLS the local reading: a galaxy DISK is ~1e6x cosmic, giving a0 ~1e3x too")
    print("         big -- MOND would never switch on in galaxies. So a0 does NOT track the")
    print("         local clumpy density. (The cluster gas, being DIFFUSE, is only ~1e2x cosmic.)\n")

    print("  (A) AMBIENT density smoothed on a LARGE (~Mpc) scale -- the only reading that")
    print("      survives galaxies AND helps clusters:")
    # field galaxy: ~1e12 Msun halo smoothed over ~ (1.5 Mpc)^3
    Mgal, Rsm = 1.5e12*Msun, 1.5*Mpc
    rho_field = Mgal/((4/3)*np.pi*Rsm**3)
    line("FIELD galaxy, Mpc-smoothed ambient", rho_field)
    # cluster: ~1e15 Msun within ~2 Mpc  (Mpc-scale overdensity)
    for Mc, Rc, tag in [(1.0e15*Msun, 2.0*Mpc, "cluster <2 Mpc"),
                        (6e14*Msun, 1.0*Mpc, "cluster <1 Mpc"),
                        (2e14*Msun, 0.5*Mpc, "cluster core <0.5 Mpc")]:
        line(f"CLUSTER ambient: {tag}", Mc/((4/3)*np.pi*Rc**3))
    print(f"""      -> FIELD galaxies sit at ~cosmic ambient density (Mpc-smoothed) -> a0 ~ 1.2e-10,
         universal RAR preserved. CLUSTERS are Mpc-scale OVERDENSITIES -> a0 ~10-50x cosmic.
      -> B&B (2009) require a0 ~ 1.5e-7 cgs = {1.5e-7*1e-2:.1e} m/s^2 = {1.5e-9/A0c:.0f}x cosmic at r2500.
         The formula's Mpc-ambient a0 lands in EXACTLY this range. Standard MOND has NO such
         prediction -- it just declares a0 universal and absorbs the cluster gap as 'needs DM'.\n""")

    # Does the residual close with the formula's cluster a0?
    print("  RESIDUAL CLOSURE with the formula's cluster a0 (Mpc-ambient ~14x cosmic):")
    a0_cl = 14*A0c
    gN = 0.37*A0c                                  # representative cluster-core g_N (~0.37 a0_cosmic)
    for tag, a in [("standard MOND (a0=1.2e-10)", A0c), ("THE FORMULA (a0~14x in-cluster)", a0_cl)]:
        boost = nu(gN/a); resid = 6.5/boost
        print(f"     {tag:36s}: boost nu={boost:4.1f}  residual={resid:4.2f}  "
              f"{'(closes!)' if resid<1.3 else '(fails ~2x)'}")
    print("     i.e. the SAME cluster that leaves standard MOND a factor ~2-3 short is fit by the")
    print("     formula -- because the cluster's own density RAISES a0 there. And a0 ~ sqrt(rho(r))")
    print("     RISES toward the dense core, matching B&B's finding that required a0 grows inward.\n")

    print("="*84); print("HONEST VERDICT -- I owe you this both ways"); print("="*84)
    print("""  YOU WERE RIGHT, I tested a strawman. a0=(c/2)sqrt(G rho) is a DENSITY law; clusters
  are overdense, so the formula predicts a LARGER in-cluster a0 -- and sqrt(cluster
  overdensity) ~10-14x lands right on the a0 that Blaksley & Bonamente say clusters
  need. Standard MOND CANNOT do this (universal a0). So the cluster residual that I
  called a 'decisive failure' may instead be a genuine, distinctive SUCCESS of THIS
  formula -- including the radial trend (a0 ~ sqrt(rho(r)) rises inward, as observed).

  THE CATCH (equally honest): it works only if rho is the AMBIENT density on ~Mpc
  scales. The LOCAL clumpy reading is dead -- a galaxy disk is ~1e6x cosmic and would
  give a0 ~1e3x too large, erasing MOND in galaxies. So the framework MUST specify
  'rho = density coarse-grained on a large scale' (a Machian/free-fall-clock reading,
  consistent with a0 ~ sqrt(G rho_cosmic) in the smooth limit). The smoothing scale
  (~Mpc) is currently an INPUT, not derived -- that is the open theoretical question.

  TESTABLE CONSEQUENCE: a0 then depends on the Mpc-scale ENVIRONMENT -- galaxies inside
  clusters/overdensities should show a LARGER a0 than identical field galaxies. That is
  a sharp, falsifiable, DISTINCTIVE prediction (and it is in tension with strict RAR
  universality -- the very a0-universality debate, Rodrigues vs McGaugh). THIS is where
  the formula lives or dies -- not the cosmic-only test I ran before.""")
    print("="*84)


if __name__ == "__main__":
    main()
