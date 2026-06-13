#!/usr/bin/env python3
"""
CONFRONTATION: Chaudhary, Capozziello, Sharma, Gomez-Vargas, Mustafa (2025, arXiv:2508.10247?)
"Evidence for evolving dark energy from DESI DR2 BAO and Pantheon+, DES-Dovekie, and Union3"
=============================================================================================
Submitted 2025-08-14 (NOTE: 2025, OUTSIDE the prioritized 2026-03..06 window -- flagged).
Numbers banked from Table 4 (CMB+DESI DR2+SNe) and the Sec IV reconstruction text.

WHY THIS DATASET IS DIFFERENT FROM MUSE (and worth running):
  MUSE-DARK III measures a FITTED RAR a0 directly -> it is a measurement of the *observable*
  apparent a0, which the framework already showed is LCDM-degenerate (assembly-dominated).
  THIS paper instead constrains the DARK-ENERGY EQUATION OF STATE (w0,wa). The framework's
  CANONICAL a0(z) is a0 = (c/2) sqrt(G rho_DE), so a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).
  A w0-wa fit therefore reconstructs rho_DE(z) and feeds the framework's DECLINING branch
  DIRECTLY -- this is a test of the framework's *input* (the DE density history), not the
  contaminated RAR observable. The verdict here is about DIRECTION & magnitude of a0(z).

THE FRAMEWORK FOOTING (binding working rule):
  Judge on the framework's OWN terms: a0(0)=9.36e-11 (rho_DE footing), declining sqrt(rho_DE)
  branch, Upsilon~0.70. ALSO run the regular-MOND default a0(0)=1.2e-10, CONSTANT, as baseline.
  rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))   [CPL, identical to the banked
  efe_vs_z_recompute.py and project_a0_tracks_dark_energy.py reconstruction].

Pure numpy. C. Zimmerman confrontation harness, 2026-06-13.
"""
import numpy as np

# --- framework constants (locked conventions) --------------------------------
A0_FW   = 9.36e-11      # framework footing a0(0), rho_DE, m/s^2
A0_MOND = 1.20e-10      # regular-MOND default a0(0), m/s^2
c, G    = 2.99792458e8, 6.674e-11
Mpc     = 3.0857e22

# --- Table 4 (CMB + DESI DR2 + SNe), CPL w0,wa (banked verbatim) -------------
# label: (w0, w0_err, wa, wa_minus, wa_plus, Om, h)
CPL = {
    "+Pantheon+"        : (-0.876, 0.062, -0.410, 0.220, 0.270, 0.306, 0.680),
    "+DES-SN5Y"         : (-0.795, 0.063, -0.660, 0.240, 0.270, 0.308, 0.681),
    "+DES-SN5Y(z>0.01)" : (-0.850, 0.105, -0.490, 0.320, 0.390, 0.304, 0.677),
    "+Union3"           : (-0.716, 0.089, -0.860, 0.290, 0.320, 0.305, 0.682),
}
# DESI DR2 2025 reference values used by the banked repo files (for continuity)
W0_BANKED, WA_BANKED = -0.752, -0.86


def rho_de_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE(0) for CPL w(a)=w0+wa(1-a). a=1/(1+z)."""
    z = np.asarray(z, float)
    a = 1.0 / (1.0 + z)
    return (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))


def a0_decl(z, w0, wa, A0):
    """Framework DECLINING branch: a0(z) = A0 * sqrt(rho_DE(z)/rho_DE0)."""
    return A0 * np.sqrt(rho_de_ratio(z, w0, wa))


def E(z, Om):
    OL = 1.0 - Om
    return np.sqrt(Om * (1.0 + z) ** 3 + OL)


def a0_rho_total(z, Om, A0):
    """Footing-bug rho_total branch (contrast only): a0(z) = A0 * E(z)."""
    return A0 * E(z, Om)


def main():
    print("#" * 100)
    print("# Chaudhary+ (2025) DESI DR2 evolving-DE  vs  the framework's a0(z) DECLINING sqrt(rho_DE) branch")
    print("#" * 100 + "\n")

    zs = [0.0, 0.5, 1.0, 2.0, 3.0]

    # ---------------------------------------------------------------- (0) reconstructed rho_DE(z) direction
    print("=" * 100)
    print("(0) RECONSTRUCT rho_DE(z)/rho_DE0 from each Table-4 (w0,wa).  Quintom-B => RISES into the past?")
    print("=" * 100)
    print(f"  {'SNe combo':<20}{'w0':>8}{'wa':>8}{'w0+wa':>8}  | rho_DE(z)/rho_DE0 at z=" +
          "  ".join(f"{z:>4}" for z in zs[1:]))
    for lab, (w0, w0e, wa, wam, wap, Om, h) in CPL.items():
        rr = [rho_de_ratio(z, w0, wa) for z in zs[1:]]
        print(f"  {lab:<20}{w0:>8.3f}{wa:>8.3f}{w0+wa:>8.3f}  |  " +
              "   ".join(f"{r:>5.2f}" for r in rr))
    rrb = [rho_de_ratio(z, W0_BANKED, WA_BANKED) for z in zs[1:]]
    print(f"  {'(repo-banked DR2)':<20}{W0_BANKED:>8.3f}{WA_BANKED:>8.3f}{W0_BANKED+WA_BANKED:>8.3f}  |  " +
          "   ".join(f"{r:>5.2f}" for r in rrb))
    print("\n  Quintom-B has w0>-1, wa<0, w0+wa<-1. Two opposing effects on rho_DE(z):")
    print("    - the (1+z)^{3(1+w0+wa)} term: w0+wa<-1 => exponent<0 => FALLS into the past;")
    print("    - the exp(-3 wa z/(1+z)) term: wa<0 => RISES into the past.")
    print("  Net behaviour (printed above) decides which way the framework's a0(z) actually moves.\n")

    # ---------------------------------------------------------------- (1) direction test
    print("=" * 100)
    print("(1) DIRECTION of the framework a0(z) DECLINING branch under each fit (rises or declines with z?)")
    print("=" * 100)
    print(f"  {'SNe combo':<20}  a0(z)/a0(0) at z=" + "  ".join(f"{z:>5}" for z in zs[1:]) +
          "   trend over 0->3")
    for lab, (w0, w0e, wa, wam, wap, Om, h) in CPL.items():
        ratios = [np.sqrt(rho_de_ratio(z, w0, wa)) for z in zs[1:]]
        trend = "RISES" if ratios[-1] > 1.0 else "DECLINES"
        print(f"  {lab:<20}  " + "   ".join(f"{r:>5.2f}" for r in ratios) +
              f"     {trend} ({100*(ratios[-1]-1):+.0f}% at z=3)")
    print("\n  Framework's BANKED prescription: a0(z) DECLINES with z (the 'only reading below 1').")
    print("  AGREEMENT requires a0(z)/a0(0) < 1 at high z.\n")

    # ---------------------------------------------------------------- (2) error-bar robustness on the DIRECTION
    print("=" * 100)
    print("(2) IS THE DIRECTION ROBUST to the (w0,wa) errors?  vary w0,wa at +/-1sigma corners")
    print("=" * 100)
    print(f"  {'SNe combo':<20}{'a0(z=3)/a0(0) range over 1sigma (w0,wa) box':>55}")
    for lab, (w0, w0e, wa, wam, wap, Om, h) in CPL.items():
        corner_vals = []
        for dw0 in (-w0e, 0, +w0e):
            for dwa in (-wam, 0, +wap):
                corner_vals.append(np.sqrt(rho_de_ratio(3.0, w0 + dw0, wa + dwa)))
        lo, hi = min(corner_vals), max(corner_vals)
        always_below = hi < 1.0
        always_above = lo > 1.0
        verdict = ("ALWAYS declines (<1)" if always_below else
                   "ALWAYS rises (>1)" if always_above else "SIGN AMBIGUOUS (straddles 1)")
        print(f"  {lab:<20}   z=3 ratio in [{lo:.2f}, {hi:.2f}]   -> {verdict}")
    print()

    # ---------------------------------------------------------------- (3) a0(0) normalization check
    print("=" * 100)
    print("(3) a0(0) NORMALIZATION: does Omega_DE0~0.69-0.70, h~0.68 reproduce 9.36e-11 (rho_DE footing)?")
    print("=" * 100)
    # rho_DE0 = Omega_DE0 * rho_crit ; rho_crit = 3 H0^2 / (8 pi G)
    # framework geometric core: a0 = (c/2) sqrt(G rho_DE)  (the sqrt(rho_DE) footing)
    print(f"  {'SNe combo':<20}{'h':>6}{'Om':>7}{'Om_DE0':>9}{'rho_DE0 [kg/m^3]':>20}{'(c/2)sqrt(G rho_DE0)':>24}")
    for lab, (w0, w0e, wa, wam, wap, Om, h) in CPL.items():
        H0 = h * 100.0 * 1e3 / Mpc
        rho_crit = 3.0 * H0**2 / (8.0 * np.pi * G)
        Om_DE0 = 1.0 - Om
        rho_DE0 = Om_DE0 * rho_crit
        a0_geom = (c / 2.0) * np.sqrt(G * rho_DE0)
        print(f"  {lab:<20}{h:>6.3f}{Om:>7.3f}{Om_DE0:>9.3f}{rho_DE0:>20.3e}{a0_geom:>24.3e}")
    print(f"  framework footing target a0(0) = {A0_FW:.3e} m/s^2 (rho_DE);  regular-MOND default = {A0_MOND:.3e}.")
    print("  NOTE: the (c/2)sqrt(G rho_DE) geometric core carries the SAME route coefficient as the banked")
    print("  9.36e-11 derivation; this row checks the rho_DE0 normalization moves with (h,Om), not the coeff.\n")

    # ---------------------------------------------------------------- (4) both-footings magnitude table
    print("=" * 100)
    print("(4) BOTH FOOTINGS, absolute a0(z) [x1e-10 m/s^2], using the +DES-SN5Y fit (steepest wa)")
    print("=" * 100)
    w0, w0e, wa, wam, wap, Om, h = CPL["+DES-SN5Y"]
    print(f"  {'z':>5}{'FW decl 9.36e-11':>20}{'MOND-default 1.2e-10 (const)':>30}{'FW rho_total E(z)':>20}")
    for z in zs:
        fw = a0_decl(z, w0, wa, A0_FW) * 1e10
        mo = A0_MOND * 1e10                       # regular MOND default is CONSTANT
        rt = a0_rho_total(z, Om, A0_FW) * 1e10
        print(f"  {z:>5.1f}{fw:>20.3f}{mo:>30.3f}{rt:>20.3f}")
    print()

    # ---------------------------------------------------------------- (5) verdict
    print("=" * 100)
    print("(5) VERDICT")
    print("=" * 100)
    # compute the headline numbers for the verdict
    ratios_z3 = {lab: np.sqrt(rho_de_ratio(3.0, p[0], p[2])) for lab, p in CPL.items()}
    print(f"  a0(z=3)/a0(0) by fit:  " +
          ",  ".join(f"{lab.strip('+')}={r:.2f}" for lab, r in ratios_z3.items()))


if __name__ == "__main__":
    main()
