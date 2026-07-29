#!/usr/bin/env python3
r"""mi_cmb_acoustic_shift_2026.py -- turn "the rising a0 footing spoils the CMB peaks" into a
NUMBER: the fractional shift in the acoustic scale, and its exclusion in sigma against Planck.

BACKGROUND. mi_cmb_a0_horizon_2026 showed, at order of magnitude, that under the RISING footing
(a0 = cH(z)/Z, tied to total density) the recombination plasma sits at g/a0 ~ few, i.e. partly in
the modified-inertia regime, whereas under the CANONICAL footing (a0 = cH_Lambda/Z, constant) it
sits at g/a0 ~ 1e5 and the CMB is untouched. This script makes the rising-footing case quantitative
via the sound horizon.

THE MECHANISM. The CMB acoustic-peak angular scale is theta_star = r_s / D_A, with the comoving
sound horizon
        r_s = INT_{z_rec}^{inf} c_s(z) / H(z) dz ,     c_s^2 = c^2 / [3(1+R)] ,
        R(z) = (3/4) rho_b/rho_gamma = (3 Omega_b)/(4 Omega_gamma) / (1+z).
Modified INERTIA changes the inertial mass of the baryons when their proper acceleration is below
a0, which rescales the baryon loading R -> R/nu(y) (inertia reduced by 1/nu) or R*nu(y) depending
on convention. Either way c_s and hence r_s change, and the peaks move.

THE CLEAN ANALYTIC POINT. The plasma's acoustic acceleration is a_ac(z) ~ c_s(z) H(z) (sound speed
times oscillation rate near horizon crossing). Under the RISING footing a0(z) = cH(z)/Z, so
        y_rising(z) = a_ac/a0 = c_s(z) H(z) / (cH(z)/Z) = Z c_s(z)/c = Z / sqrt(3(1+R(z))).
The H(z) CANCELS. So under the rising footing y is ORDER UNITY at EVERY redshift in the plasma
(y ~ 2.6 at recombination, ~3.3 deep in radiation), and nu(y) deviates from 1 by ~15% throughout
the ENTIRE acoustic history -- not a small late correction. That is why the rising footing is not
marginally excluded but structurally incompatible with standard acoustic physics.

DISCIPLINE. This is a TIGHT-COUPLING / sound-horizon estimate, not a full Boltzmann solve. The
modeling choice is a_ac = c_s H; the sign convention of the inertia rescaling affects the DIRECTION
of the peak shift, not its magnitude. A full CAMB/CLASS run would refine the exact number but
cannot close a ~1.5% effect against Planck's 0.03% measurement of theta_star (the ~15% modification
is to the baryon loading R; because R < 1 it propagates to a ~1.5% shift in r_s). Both footings and
both sign conventions are carried. Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

C = 2.99792458e8
H0 = 2.184e-18                         # s^-1 (67.4 km/s/Mpc)
OM, OL, OR = 0.315, 0.685, 9.1e-5      # Omega_r includes 3 neutrino species
OB = 0.0493
OG = 5.38e-5                           # photons only
Z = math.sqrt(32 * math.pi / 3)
A0_CANON = 9.36e-11
MPC = 3.0857e22
Z_REC = 1089.9
# Planck 2018: 100 theta_star = 1.04109 +/- 0.00030  -> fractional precision:
THETA_STAR_FRAC_ERR = 0.00030 / 1.04109      # = 2.88e-4

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)


def H(z):
    return H0 * math.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)

def R_of(z):
    return (3.0 * OB) / (4.0 * OG) / (1.0 + z)

def nu(y):
    return math.sqrt(1.0 + 1.0 / y)


def sound_horizon(inertia=None, n=200000, zmax=1.0e7):
    """comoving r_s = INT c_s/H dz from z_rec to zmax. `inertia`: None=standard;
    'reduce' -> R/nu ; 'enhance' -> R*nu, with y = Z/sqrt(3(1+R))."""
    # log-spaced in (1+z) for accuracy across radiation+matter
    lo, hi = math.log(1 + Z_REC), math.log(1 + zmax)
    tot = 0.0
    prev_z = None; prev_int = None
    for i in range(n + 1):
        lz = lo + (hi - lo) * i / n
        z = math.exp(lz) - 1.0
        R = R_of(z)
        if inertia:
            y = Z / math.sqrt(3.0 * (1.0 + R))
            f = nu(y)
            R = R / f if inertia == "reduce" else R * f
        cs = C / math.sqrt(3.0 * (1.0 + R))
        integrand = cs / H(z) * (1 + z)          # d z = (1+z) d ln(1+z)
        if prev_int is not None:
            tot += 0.5 * (integrand + prev_int) * (lz - prev_lz)
        prev_int, prev_lz = integrand, lz
    return tot

def comoving_distance_to_rec(n=200000):
    lo, hi = 0.0, math.log(1 + Z_REC)
    tot = 0.0; prev = None
    for i in range(n + 1):
        lz = lo + (hi - lo) * i / n
        z = math.exp(lz) - 1.0
        integrand = C / H(z) * (1 + z)
        if prev is not None:
            tot += 0.5 * (integrand + prev) * (lz - prev_lz)
        prev, prev_lz = integrand, lz
    return tot


def main() -> int:
    banner("mi_cmb_acoustic_shift_2026 -- the acoustic-scale shift, in sigma")

    # ---------------------------------------------------------------------------------
    banner("1. Validate the machinery against the known standard values")
    r_s = sound_horizon()
    D_A = comoving_distance_to_rec()
    theta = r_s / D_A
    ell_A = math.pi / theta
    print(f"  r_s (standard)        = {r_s/MPC:.2f} Mpc      (known ~144-147)")
    print(f"  D_A to last scatter   = {D_A/MPC/1e3:.2f} Gpc  (known ~13.9)")
    print(f"  100*theta_star        = {100*theta:.4f}       (Planck 1.04109)")
    print(f"  ell_A = pi/theta      = {ell_A:.0f}            (first peak ~220 ~ 0.75 ell_A)")
    check(140 < r_s / MPC < 152, "r_s within a few % of the known sound horizon")
    check(1.00 < 100 * theta < 1.08, "theta_star within a few % of Planck")

    # ---------------------------------------------------------------------------------
    banner("2. The H(z) cancellation -- why the rising footing is uniformly modified")
    print(f"  y_rising(z) = Z / sqrt(3(1+R(z)))   (H cancels):")
    print(f"    {'z':>10}{'R':>10}{'y_rising':>12}{'nu(y)-1':>12}{'y_canon':>14}")
    for z in (Z_REC, 1e4, 1e5, 1e6):
        R = R_of(z); y = Z / math.sqrt(3 * (1 + R))
        a_ac = (C / math.sqrt(3 * (1 + R))) * H(z)
        yc = a_ac / A0_CANON
        print(f"    {z:>10.0f}{R:>10.4f}{y:>12.3f}{nu(y)-1:>12.4f}{yc:>14.2e}")
    print("  -> under RISING, y ~ 2.6-3.3 at EVERY epoch, so nu-1 ~ 14-18% THROUGHOUT the")
    print("     acoustic history. Under CANONICAL, y ~ 1e5+, so nu-1 ~ 1e-5 (no effect).")
    check(abs(Z / math.sqrt(3 * (1 + R_of(Z_REC))) - 2.63) < 0.1,
          "y_rising at recombination ~ 2.6 (order unity, from H-cancellation)")

    # ---------------------------------------------------------------------------------
    banner("3. The acoustic-scale shift under the RISING footing, both conventions")
    r_s_red = sound_horizon(inertia="reduce")
    r_s_enh = sound_horizon(inertia="enhance")
    for label, r_s_mod in (("inertia reduced R/nu", r_s_red),
                           ("inertia enhanced R*nu", r_s_enh)):
        d = (r_s_mod - r_s) / r_s
        dtheta = d                                   # theta_star ~ r_s/D_A, D_A ~ unchanged
        sigma = abs(dtheta) / THETA_STAR_FRAC_ERR
        dell = -d * ell_A
        print(f"  {label:<24}: r_s = {r_s_mod/MPC:6.2f} Mpc  "
              f"Delta r_s/r_s = {100*d:+6.2f}%  Delta ell_A = {dell:+6.0f}  "
              f"-> {sigma:6.0f} sigma")
    worst = max(abs((r_s_red - r_s) / r_s), abs((r_s_enh - r_s) / r_s))
    print(f"\n  NOTE: the baryon loading R is modified by ~15% (nu-1), but R enters")
    print(f"  c_s^2 = c^2/[3(1+R)] and R < 1 at recombination, so the ~15% R-shift propagates")
    print(f"  to only a ~1.5% shift in r_s. Both numbers are real; do not conflate them.")
    print(f"  Planck measures 100*theta_star = 1.04109 +/- 0.00030 (fractional {THETA_STAR_FRAC_ERR:.1e}).")
    print(f"  The rising footing shifts theta_star by ~{100*worst:.1f}% = "
          f"~{worst/THETA_STAR_FRAC_ERR:.0f} sigma. EXCLUDED.")
    check(worst / THETA_STAR_FRAC_ERR > 30,
          "the rising footing is excluded at tens of sigma by the acoustic scale alone")

    # ---------------------------------------------------------------------------------
    banner("4. The CANONICAL footing -- the framework's actual claim")
    # y_canonical is enormous, so nu-1 ~ 1e-5; the r_s shift is far below measurement.
    def r_s_canonical():
        lo, hi = math.log(1 + Z_REC), math.log(1 + 1e7)
        tot = 0.0; prev = None; n = 200000
        for i in range(n + 1):
            lz = lo + (hi - lo) * i / n
            z = math.exp(lz) - 1.0
            R = R_of(z)
            cs0 = C / math.sqrt(3 * (1 + R))
            a_ac = cs0 * H(z)
            y = a_ac / A0_CANON
            R_eff = R / nu(y)                         # same convention as 'reduce'
            cs = C / math.sqrt(3 * (1 + R_eff))
            integrand = cs / H(z) * (1 + z)
            if prev is not None:
                tot += 0.5 * (integrand + prev) * (lz - prev_lz)
            prev, prev_lz = integrand, lz
        return tot
    r_s_can = r_s_canonical()
    d_can = (r_s_can - r_s) / r_s
    print(f"  r_s (canonical, a0 const) = {r_s_can/MPC:.4f} Mpc")
    print(f"  Delta r_s/r_s             = {d_can:.2e}  -> {abs(d_can)/THETA_STAR_FRAC_ERR:.3f} sigma")
    check(abs(d_can) / THETA_STAR_FRAC_ERR < 1.0,
          "the CANONICAL footing shifts theta_star by << 1 sigma -- consistent with Planck")

    banner("VERDICT")
    print(f"  Machinery validated: r_s = {r_s/MPC:.1f} Mpc, 100 theta_star = {100*theta:.4f},")
    print(f"  ell_A = {ell_A:.0f} -- all within a few % of the standard/Planck values.")
    print(f"  RISING footing (a0 = cH(z)/Z): y ~ 2.6-3.3 at EVERY epoch (H cancels), so the")
    print(f"  baryon loading R is modified ~15% throughout -> theta_star shifts ~{100*worst:.1f}% ->")
    print(f"  ~{worst/THETA_STAR_FRAC_ERR:.0f} sigma against Planck. EXCLUDED, and no Boltzmann")
    print(f"  refinement can close ~1.5% vs 0.03%.")
    print(f"  CANONICAL footing (a0 const): y ~ 1e5, theta_star shift ~{abs(d_can):.0e} = "
          f"{abs(d_can)/THETA_STAR_FRAC_ERR:.2f} sigma -- CONSISTENT.")
    print(f"  So the CMB acoustic scale, computed not just estimated, DECISIVELY selects the")
    print(f"  framework's canonical constant-a0 footing over the rising one.")
    print(f"  CAVEATS: tight-coupling estimate; a_ac = c_s H is the modeling choice; sign")
    print(f"  convention sets direction not magnitude; a0's VALUE remains postulated.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
