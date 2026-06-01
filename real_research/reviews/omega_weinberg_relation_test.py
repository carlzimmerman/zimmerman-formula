#!/usr/bin/env python3
"""
Putting the one good strand to the test:  Omega_m / Omega_Lambda  =?  2 sin^2(theta_W)
=====================================================================================

This is the single relation in the Zimmerman web that ties two INDEPENDENTLY
measured numbers (Planck cosmology and collider electroweak). It deserves a real,
honest test rather than a quoted central-value "0.5% match". Three questions:

  (1) Does it hold in the MEASURED values, with error bars, across every standard
      sin^2(theta_W) scheme?  (kills or confirms "scheme-dependence")
  (2) What energy scale does it secretly pick (sin^2 runs; Omega_m/Omega_Lambda
      does not)?  Is that scale physically motivated or arbitrary?
  (3) Look-elsewhere: among simple (rational x particle-observable) relations, how
      special is "2 sin^2(theta_W)" for hitting Omega_m/Omega_Lambda?

No answer is assumed; we report whatever the numbers say.
Pure stdlib + numpy.  Run:  python reviews/omega_weinberg_relation_test.py
"""

import math
import numpy as np

# ---- measured inputs (PDG 2023 / Planck 2018) ---------------------------------
OMEGA_M = 0.3153;  OMEGA_M_ERR = 0.0073      # Planck 2018 TT,TE,EE+lowE+lensing
# flat LCDM: Omega_Lambda = 1 - Omega_m (anti-correlated), so the ratio error
# comes from Omega_m alone:  R = Om/(1-Om),  sigma_R = sigma_Om/(1-Om)^2
R = OMEGA_M / (1 - OMEGA_M)
R_ERR = OMEGA_M_ERR / (1 - OMEGA_M) ** 2

# sin^2(theta_W) in every standard convention (value, error, label)
SCHEMES = [
    (0.23122, 0.00004, "MS-bar at M_Z          "),
    (0.23155, 0.00004, "effective leptonic     "),
    (0.22305, 0.00023, "on-shell 1-M_W^2/M_Z^2 "),
    (0.23867, 0.00016, "low-energy s^2(Q->0)   "),
]


def part1_scheme_test():
    print("=" * 80)
    print("(1) Does Om/OL = 2 sin^2(theta_W) hold in MEASURED values, with errors?")
    print("=" * 80)
    print(f"   Omega_m/Omega_Lambda = {R:.5f} +/- {R_ERR:.5f}   (+/- {R_ERR/R*100:.1f}% ; Planck)")
    print(f"   target for sin^2 = R/2 = {R/2:.5f} +/- {R_ERR/2:.5f}\n")
    print(f"   {'scheme':<24} {'2 sin^2':>9} {'diff':>9} {'sigma':>7}  verdict")
    for s, serr, label in SCHEMES:
        two_s = 2 * s
        diff = two_s - R
        sigma = abs(diff) / math.sqrt(R_ERR**2 + (2*serr)**2)
        verdict = "CONSISTENT" if sigma < 2 else "TENSION"
        print(f"   {label} {two_s:>9.5f} {diff:>+9.5f} {sigma:>6.2f}s  {verdict}")
    print()
    print("   Note: the cosmological error (+/-3.4% on the ratio) is far larger than")
    print("   the spread BETWEEN schemes, so the relation cannot currently")
    print("   distinguish them -- every standard scheme sits within ~1 sigma.")
    print("   The quoted '0.5%' is a central-value coincidence inside a ~3.4% window.\n")


def part2_scale_test():
    print("=" * 80)
    print("(2) What energy scale does the relation pick?  (sin^2 runs; Om/OL doesn't)")
    print("=" * 80)
    # measured running of sin^2(theta_W) (MS-bar), a few real anchor points:
    #   Q->0 : 0.23867 ;  M_Z(91 GeV): 0.23122 ;  ~1 TeV: ~0.23085 (slow decrease)
    anchors_Q = np.array([1e-3, 91.19, 1000.0])          # GeV
    anchors_s = np.array([0.23867, 0.23122, 0.23085])
    target = R / 2
    print(f"   need sin^2(mu) = R/2 = {target:.5f}")
    # interpolate in log Q
    lo, hi = target - R_ERR/2, target + R_ERR/2
    def s_of_logQ(lnq):
        return np.interp(lnq, np.log(anchors_Q), anchors_s)
    # scan for crossing
    lnqs = np.linspace(math.log(1e-3), math.log(1e4), 2000)
    svals = s_of_logQ(lnqs)
    hit = np.where(np.abs(svals - target) == np.abs(svals - target).min())[0][0]
    Q_central = math.exp(lnqs[hit])
    print(f"   central value sin^2 = {target:.5f} is reached near Q ~ {Q_central:.0f} GeV")
    print(f"   but with the cosmo error, the allowed sin^2 band [{lo:.4f},{hi:.4f}]")
    print(f"   spans from Q ~ M_Z all the way to Q -> 0 -- i.e. the scale is NOT")
    print(f"   pinned at all. No privileged scale is selected; current precision")
    print(f"   admits essentially the whole SM running curve.\n")


def part3_look_elsewhere():
    print("=" * 80)
    print("(3) Look-elsewhere: how special is '2 sin^2' for hitting Om/OL = 0.4605?")
    print("=" * 80)
    # particle-physics observables nature hands us independently
    particles = {
        "sin^2_W": 0.23122, "cos^2_W": 0.76878, "tan^2_W": 0.30077,
        "alpha":   1/137.036, "alpha_s": 0.1179, "alpha_s^.5": 0.1179**0.5,
    }
    target = R
    tol = 0.005   # 0.5%, the quoted precision
    hits = []
    for pname, pval in particles.items():
        for a in range(1, 7):
            for b in range(1, 7):
                val = (a / b) * pval
                if val > 0 and abs(val - target) / target <= tol:
                    hits.append((f"({a}/{b})*{pname}", val))
    print(f"   target Om/OL = {target:.5f}; counting simple (a/b)*observable within 0.5%:")
    for expr, val in sorted(hits, key=lambda x: abs(x[1]-target)):
        print(f"     {expr:<22} = {val:.5f}   ({(val-target)/target*100:+.2f}%)")
    print(f"\n   => {len(hits)} simple relations hit within 0.5%.  '2*sin^2_W' is one")
    print( "      of several (e.g. (3/5)*cos^2_W lands equally well). It is the most")
    print( "      'meaningful'-looking, but it is not numerically unique.\n")


def main():
    print(f"\n  Omega_m = {OMEGA_M} +/- {OMEGA_M_ERR}  (Planck 2018)\n")
    part1_scheme_test()
    part2_scale_test()
    part3_look_elsewhere()
    print("=" * 80)
    print("HONEST VERDICT")
    print("=" * 80)
    print("  Om/OL = 2 sin^2(theta_W) is CONSISTENT with the measured values -- but")
    print("  consistent in the weak sense: the cosmological ratio is only known to")
    print("  +/-3.4%, so 2 sin^2 matches for EVERY standard scheme (0.1-1 sigma) and")
    print("  for any scale from M_Z to Q->0, and several other simple relations match")
    print("  too. The '0.5%' is a central-value accident inside a 3.4% window.")
    print()
    print("  Correction to an earlier overstatement: it does NOT cleanly 'fail for")
    print("  on-shell' -- on-shell is 0.9 sigma, still consistent. The relation simply")
    print("  is not yet precisely TESTED, in any scheme.")
    print()
    print("  What would turn it from coincidence into evidence (concrete + forward):")
    print("   * Omega_m to <1% (DESI Y5 / Euclid) shrinks the window ~4x. Then 2 sin^2")
    print("     either nails it (scheme-resolving, genuinely interesting) or breaks.")
    print("   * A MECHANISM predicting WHICH scheme/scale sin^2 is evaluated at --")
    print("     without that, 'sin^2' is ambiguous at the 3% level and the relation")
    print("     has no defined left-hand side.")
    print("  Until both: the best strand in the web is a consistent, mechanism-free")
    print("  coincidence -- promising enough to keep, not yet evidence.")


if __name__ == "__main__":
    main()
