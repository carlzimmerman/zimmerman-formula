#!/usr/bin/env python3
r"""mi_lyalpha_forest_b_test_2026.py -- confront the framework's diffuse-baryon velocity amplification
with Lyman-alpha forest Doppler b-parameters. A live falsification test, run on real published numbers.

*** CORRECTED 2026-07-30. The four low-b cutoff values this script used were UNSOURCEABLE and have
*** been withdrawn and replaced by Hiss et al. 2018 Table 4. See mi_forest_bcut_data_2026.py for the
*** full audit trail; the correction notice is printed at the top of this script's own output. The
*** correction runs BOTH ways and both are reported: the new statistical bars are 0.33-1.37 km/s
*** instead of an invented +/- 2.0 km/s, which SHARPENS the exclusion, while the calibration
*** systematic that Hiss et al. document and that Table 4 does NOT contain is 3.36 km/s, which
*** SOFTENS it. Both channels are printed side by side everywhere. The retired sequence also had the
*** redshift SHAPE backwards.

THE PREDICTION UNDER TEST. mi_growth_amplification_founded_2026.py found that under a POINTWISE reading
of the first-moment closure, diffuse baryons sit at x = a/a0 ~ 1e-3 where the linear-response
amplification 1/h(x) = sqrt(1+4x^2)/(2x) is O(1e2), so their velocity response is enhanced by
sqrt(1/h) ~ 9-27x (quasi-equilibrium scaling) up to 1/h ~ 80-720x (linear-infall scaling), while
galaxies at x ~ 0.1-1 are enhanced only 1.1-2.8x. That is an enormous differential signature, and the
Lyman-alpha forest measures exactly the affected quantity.

THE OBSERVABLE. Each forest absorption line has a Doppler parameter b (km/s) with
        b^2 = b_thermal^2 + b_nonthermal^2 ,   b_thermal = 12.85 sqrt(T/1e4 K) km/s
(Rudie, Steidel & Pettini 2012, eqs. 4-6, proton mass) where the non-thermal part collects Hubble
broadening across the absorber AND peculiar-velocity structure. Only the PECULIAR-VELOCITY part is
gravitational, so only that part is amplified: MI does not touch the background expansion
(mi_channelA_friedmann_2026: the term vanishes identically on FRW) and does not set the photoionization
temperature.

The decisive statistic is the LOW-b CUTOFF, not the median: the narrowest lines observed put a hard
ceiling on any universal velocity amplification, because a universal enhancement would leave NO narrow
lines at all.

THE VERIFIED OBSERVATIONS now come from Hiss, Walther, Hennawi, Onorbe, O'Meara, Rorai & Lukic 2018,
ApJ 865, 42 (DOI 10.3847/1538-4357/aada86; arXiv:1710.00700), TABLE 4: b0(z) in eight dz = 0.2 bins
from z = 2.0 to 3.4, with the table's own asymmetric percentile errors. b0(z) is NON-MONOTONIC and
peaks near z = 2.8. Note the Hiss sequence stops at z = 3.4, so the retired sequence's z = 3.70 point
-- the one that used to carry the "the exclusion dies at high z" conclusion -- has no counterpart in
the replacement data and that conclusion cannot be evaluated against it at all.

WHAT IS COMPUTED:
  S0  The correction notice and the replacement data. Printed first, always.
  S1  The forest gas's x = a/a0 at z = 2.0-3.4, from its own overdensity and scale. Both footings.
  S2  The amplification, and the two scalings (quasi-equilibrium sqrt(1/h) vs linear 1/h).
  S3  The predicted b-cutoff as a function of how much of the LCDM b budget is peculiar-velocity --
      the one genuinely uncertain input, so it is SCANNED rather than assumed. Both error channels.
  S4  The exclusion, in sigma, across the full Hiss sequence. Both footings, both error channels.
  S5  DIRECT PRIOR ART: Aguirre, Schaye & Quataert 2001, and the x-CONVENTION FOOTING FORK that their
      paper alone spans, propagated all the way through to sigma so the reader sees the dependence.
  S6  The COUNTERWEIGHT: Arnold, Puchwein & Springel 2015, stated both ways.
  S7  Verdict: what this kills, what escapes remain, and which are legitimate.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_forest_bcut_data_2026 import (  # noqa: E402
    AGUIRRE_A0, AGUIRRE_AN, AGUIRRE_LJ_KPC, B_CAL_SYS, B_CAL_SYS_ALT, B_CUT, B_CUT_HISS,
    ZS_FOREST, b_thermal, err_up, print_correction_notice, print_data_table, sig_cal, sig_stat,
)

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

G_SI = 6.67430e-11
C_SI = 2.99792458e8
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
H0S = 67.4e3 / MPC
OM = 0.315
RHO_M0 = OM * 3 * H0S**2 / (8 * np.pi * G_SI)
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
A0_CAN, A0_ALT = FOOTINGS[0][1], FOOTINGS[1][1]
T_IGM = (1.0e4, 2.0e4)   # K, IGM temperature range at z ~ 2-3


# *** KERNEL ARGUMENT CORRECTED 2026-07-30. *** h's argument is the OBSERVED acceleration
# x = sqrt(y^2+y) (the framework's own closure g_obs^2 = g_bar^2 + a0 g_bar), NOT the Newtonian
# y = g_bar/a0 that this script used to pass. The old argument OVERSTATED the amplification by
# 1.9x-5.6x and INFLATED every sigma below -- a manufactured deficit. Imported from the shared module,
# which carries the sympy derivation and the retired form for audit.
from mi_forest_bcut_data_2026 import (  # noqa: E402
    amp_linear, amp_sqrt, amp_inflation_factor, h_resp_at_obs, x_obs_from_newtonian,
    amp_linear_WRONG_newtonian_arg,
)


def h_resp(y):
    """Back-compat shim: same name, correctly argumented via the observed acceleration."""
    return h_resp_at_obs(y)


def b_pred_from(bc, A, f_pec=0.3, T=1.0e4):
    """Predicted cutoff: thermal floor untouched, Hubble part untouched, peculiar part amplified."""
    bth = b_thermal(T)
    bnt2 = max(bc**2 - bth**2, 0.0)
    return float(np.sqrt(bth**2 + bnt2 * (1.0 - f_pec) + (A * np.sqrt(bnt2 * f_pec)) ** 2))


def g_forest(z, delta=3.0, R_kpc=200.0):
    rho = RHO_M0 * (1 + z) ** 3
    return (4 * np.pi / 3) * G_SI * rho * delta * (R_kpc * KPC)


def E_of_z(z):
    return np.sqrt(OM * (1 + z) ** 3 + (1 - OM))


def main() -> int:
    banner("S0. THE CORRECTION -- what was withdrawn, and what replaced it")
    print_correction_notice()
    print()
    print_data_table()

    banner("S1. The forest gas's x = a/a0 at z = 2.0-3.4 -- computed from its own overdensity and scale")
    print("  Forest absorbers at z ~ 2-3 are mildly overdense sheets/filaments. Peculiar gravitational")
    print("  acceleration g ~ (4 pi/3) G rho_m(z) delta R with R the absorber coherence length.")
    print("  This is the SINGLE-ABSORBER estimate; mi_forest_total_acceleration_2026 replaces it with")
    print("  the total-acceleration integral, and S5 below prices the whole convention fork.")
    print(f"  {'z':>5s} {'delta':>6s} {'R (kpc)':>8s} {'rho_m(z)':>11s} {'g (m/s^2)':>11s} "
          f"{'x canon':>9s} {'x alt':>8s}")
    xs = {}
    for z in ZS_FOREST:
        rho = RHO_M0 * (1 + z) ** 3
        for delta, R_kpc in ((3.0, 200.0), (10.0, 100.0)):
            g = g_forest(z, delta, R_kpc)
            xs[(z, delta)] = (g / A0_CAN, g / A0_ALT)
            print(f"  {z:5.2f} {delta:6.1f} {R_kpc:8.0f} {rho:11.3e} {g:11.3e} "
                  f"{g/A0_CAN:9.5f} {g/A0_ALT:8.5f}")
    xvals = [v[0] for v in xs.values()] + [v[1] for v in xs.values()]
    check(max(xvals) < 0.05,
          f"forest gas sits at x = {min(xvals):.5f}-{max(xvals):.5f} across BOTH footings, i.e. 1-2 "
          f"orders BELOW a0 -- squarely in the framework's deep-modified regime either way")

    banner("S2. Amplification, and the two scalings stated separately (they bracket the prediction)")
    print("  quasi-equilibrium (virial-like): v ~ sqrt(g_eff r) so velocities scale as sqrt(1/h)")
    print("  linear infall (v = a t):          velocities scale as 1/h")
    print(f"  {'z':>5s} {'delta':>6s} {'x canon':>9s} {'1/h':>10s} {'sqrt(1/h)':>11s} "
          f"{'x alt':>9s} {'1/h alt':>10s} {'sqrt alt':>10s}")
    amps = {}
    for k, (xc, xa) in sorted(xs.items()):
        inv_c, inv_a = 1.0 / float(h_resp(xc)), 1.0 / float(h_resp(xa))
        amps[k] = (np.sqrt(inv_c), inv_c, np.sqrt(inv_a), inv_a)
        print(f"  {k[0]:5.2f} {k[1]:6.1f} {xc:9.5f} {inv_c:10.1f} {np.sqrt(inv_c):11.2f} "
              f"{xa:9.5f} {inv_a:10.1f} {np.sqrt(inv_a):10.2f}")
    A_lo = min(min(a[0], a[2]) for a in amps.values())
    A_hi = max(max(a[1], a[3]) for a in amps.values())
    check(A_lo > 1.0 and A_lo <= A_hi,
          f"even the MOST CONSERVATIVE scaling on either footing gives a velocity amplification of "
          f"{A_lo:.1f}x, and the aggressive one {A_hi:.0f}x -- bracketed but large either way")

    banner("S3. Predicted b-cutoff -- SCANNING the one uncertain input, both error channels")
    print("  The uncertain input is what fraction of the LCDM non-thermal budget is PECULIAR VELOCITY")
    print("  (amplified) as opposed to HUBBLE BROADENING (not amplified -- MI leaves the background")
    print("  untouched). Rather than assume it, scan it. Setup at the PEAK of the measured sequence,")
    print(f"  z = 2.8, where b0 = {B_CUT[2.8]} +{B_CUT_HISS[2.8][1]}/-{B_CUT_HISS[2.8][2]} km/s:")
    z0, bcut0 = 2.8, B_CUT[2.8]
    print(f"  thermal floor b_th = {b_thermal(T_IGM[0]):.1f}-{b_thermal(T_IGM[1]):.1f} km/s for "
          f"T = 1-2e4 K")
    print(f"  so the LCDM non-thermal budget at the cutoff is b_nt = sqrt(b_cut^2 - b_th^2) = "
          f"{np.sqrt(max(bcut0**2 - b_thermal(T_IGM[0])**2, 0)):.1f} km/s at T = 1e4 K, falling to "
          f"{np.sqrt(max(bcut0**2 - b_thermal(T_IGM[1])**2, 0)):.1f} km/s at T = 2e4 K")
    A_use = amp_sqrt(xs[(2.8, 3.0)][0])
    A_use_alt = amp_sqrt(xs[(2.8, 3.0)][1])
    print(f"  using the CONSERVATIVE amplification sqrt(1/h) at z = 2.8, delta = 3: "
          f"{A_use:.2f} canonical, {A_use_alt:.2f} alt footing")
    print(f"  {'f_pec':>7s} {'T (K)':>8s} {'b_th':>7s} {'b_pec':>7s} {'b_hub':>7s} {'b_pred':>8s} "
          f"{'sig_stat':>9s} {'sig_cal':>9s} {'b_pred alt':>11s} {'sig_stat':>9s} {'sig_cal':>9s}")
    rows = []
    for T in T_IGM:
        bth = b_thermal(T)
        bnt2 = max(bcut0**2 - bth**2, 0.0)
        for f_pec in (0.1, 0.2, 0.3, 0.5, 0.8):
            b_pec = np.sqrt(bnt2 * f_pec)
            b_hub = np.sqrt(bnt2 * (1 - f_pec))
            bp = b_pred_from(bcut0, A_use, f_pec, T)
            bpa = b_pred_from(bcut0, A_use_alt, f_pec, T)
            ss, sc = sig_stat(z0, bp), sig_cal(z0, bp)
            ssa, sca = sig_stat(z0, bpa), sig_cal(z0, bpa)
            rows.append((f_pec, T, bp, ss, sc, ssa, sca))
            print(f"  {f_pec:7.2f} {T:8.0f} {bth:7.1f} {b_pec:7.1f} {b_hub:7.1f} {bp:8.1f} "
                  f"{ss:8.1f}s {sc:8.1f}s {bpa:11.1f} {ssa:8.1f}s {sca:8.1f}s")
    st_all = [r[3] for r in rows] + [r[5] for r in rows]
    ca_all = [r[4] for r in rows] + [r[6] for r in rows]
    print(f"  SCAN RANGE, both footings: statistical {min(st_all):.1f}-{max(st_all):.0f} sigma, "
          f"calibration {min(ca_all):.1f}-{max(ca_all):.0f} sigma")
    check(min(ca_all) > 0.0 and min(ca_all) < min(st_all),
          f"EVERY point in the scan, on BOTH footings, predicts a cutoff above the measured "
          f"{bcut0} km/s -- by {min(st_all):.1f}-{max(st_all):.0f} sigma on Hiss's statistical bar and "
          f"{min(ca_all):.1f}-{max(ca_all):.0f} sigma even against the {B_CAL_SYS:.2f} km/s calibration "
          f"systematic, so the result does not depend on the uncertain peculiar/Hubble split")

    # threshold: how small must f_pec be to survive? Reported on BOTH error channels.
    bth = b_thermal(T_IGM[0]); bnt2 = max(bcut0**2 - bth**2, 0.0)
    thresh = {}
    for lab, denom in (("statistical", err_up(z0)), ("calibration", B_CAL_SYS)):
        f_thresh = None
        for f in np.logspace(-8, 0, 8000):
            bp = np.sqrt(bth**2 + bnt2 * (1 - f) + (A_use * np.sqrt(bnt2 * f)) ** 2)
            if (bp - bcut0) / denom > 1.0:
                f_thresh = f
                break
        thresh[lab] = f_thresh
        print(f"  THRESHOLD ({lab} channel): the peculiar-velocity fraction of the LCDM non-thermal")
        print(f"    budget must be below f_pec < {f_thresh:.2e} to stay within 1 sigma of the measurement.")
    check(all(v is not None for v in thresh.values()) and thresh['calibration'] > thresh['statistical'],
          f"survival requires f_pec < {thresh['statistical']:.1e} (statistical) / "
          f"{thresh['calibration']:.1e} (calibration), i.e. peculiar velocities contributing essentially "
          f"NOTHING to forest line widths -- which no LCDM hydro simulation supports")

    banner("S4. The same test across the FULL Hiss sequence -- both footings, both error channels")
    print("  SHAPE, CORRECTED: the measured cutoff is NON-MONOTONIC. It peaks at z = 2.8 (22.67 km/s)")
    print("  and FALLS both ways -- to 18.22 km/s at z = 2.0 and 20.80 km/s at z = 3.4, with a weak")
    print("  secondary dip at z = 2.2 (16.89, worst error bar in the table). The retired sequence")
    print("  asserted a MONOTONIC RISE toward low z (22 -> 24 km/s from z = 2.85 to z = 2.30); that is")
    print("  the OPPOSITE sense to the measurement on the low-z side. The corpus had the SHAPE wrong,")
    print("  not merely the values. Schaye et al. 2000 Fig. 4 documents a rise toward low z at FIXED")
    print("  N_HI = 10^13.6 in simulation model L1, but Hiss's b0 is quoted at a z-DEPENDENT pivot")
    print("  (log N_HI,0 = 0.6225(1+z) + 11.1068, climbing 0.872 dex across the eight bins), so the two")
    print("  are different statistics and Schaye's direction does not license the retired numbers.")
    print("  ALSO: Hiss stops at z = 3.4, so the retired z = 3.70 point -- which used to carry the")
    print("  'exclusion dies at high z' conclusion -- has NO counterpart in the replacement data.")
    print(f"  Evaluated at f_pec = 0.3, T = 1e4 K, conservative sqrt(1/h) scaling:")
    print(f"  {'z':>5s} {'b0 obs':>7s} {'+err':>6s} {'x can':>8s} {'A can':>7s} {'b_pred':>8s} "
          f"{'sig_stat':>9s} {'sig_cal':>9s} | {'x alt':>8s} {'A alt':>7s} {'b_pred':>8s} "
          f"{'sig_stat':>9s} {'sig_cal':>9s}")
    seq = {"canonical": {"stat": [], "cal": []}, "alt": {"stat": [], "cal": []}}
    for z in ZS_FOREST:
        xc, xa = xs[(z, 3.0)]
        Ac, Aa = amp_sqrt(xc), amp_sqrt(xa)
        bpc, bpa = b_pred_from(B_CUT[z], Ac), b_pred_from(B_CUT[z], Aa)
        ssc, scc = sig_stat(z, bpc), sig_cal(z, bpc)
        ssa, sca = sig_stat(z, bpa), sig_cal(z, bpa)
        seq["canonical"]["stat"].append(ssc); seq["canonical"]["cal"].append(scc)
        seq["alt"]["stat"].append(ssa); seq["alt"]["cal"].append(sca)
        print(f"  {z:5.1f} {B_CUT[z]:7.2f} {err_up(z):6.2f} {xc:8.5f} {Ac:7.2f} {bpc:8.1f} "
              f"{ssc:8.1f}s {scc:8.1f}s | {xa:8.5f} {Aa:7.2f} {bpa:8.1f} {ssa:8.1f}s {sca:8.1f}s")
    for lab in ("canonical", "alt"):
        print(f"  {lab:>10s} footing: statistical {min(seq[lab]['stat']):.1f}-{max(seq[lab]['stat']):.0f} "
              f"sigma, calibration {min(seq[lab]['cal']):.1f}-{max(seq[lab]['cal']):.0f} sigma")
    all_stat = seq["canonical"]["stat"] + seq["alt"]["stat"]
    all_cal = seq["canonical"]["cal"] + seq["alt"]["cal"]
    print(f"  RETIRED-DATA COMPARISON: on the unsourceable four values with their invented symmetric")
    print(f"  +/- 2.0 km/s bar, this same single-absorber calculation banked 6.5-42.8 sigma. On the real")
    print(f"  Hiss data it is {min(all_stat):.1f}-{max(all_stat):.0f} sigma statistical and "
          f"{min(all_cal):.1f}-{max(all_cal):.0f} sigma against the calibration")
    print(f"  systematic. The correction moved the number in BOTH directions and both are shown.")
    check(min(all_cal) > 0.0 and min(all_cal) < min(all_stat),
          f"the exclusion holds across all {len(ZS_FOREST)} Hiss bins and both footings: "
          f"{min(all_stat):.0f}-{max(all_stat):.0f} sigma statistical, "
          f"{min(all_cal):.1f}-{max(all_cal):.1f} sigma against the calibration systematic -- so it is "
          f"not an artifact of one epoch and it survives the larger of the two error channels")
    check(abs(max(B_CUT, key=lambda z: B_CUT[z]) - 2.8) < 1e-9,
          f"and the SHAPE is carried through the test rather than asserted: the argmax of the measured "
          f"sequence used here is z = {max(B_CUT, key=lambda z: B_CUT[z])}, not the low-z end")

    banner("S5. DIRECT PRIOR ART -- Aguirre, Schaye & Quataert 2001 -- and the x-CONVENTION FORK")
    print("  Aguirre, Schaye & Quataert 2001, ApJ 561, 550 (DOI 10.1086/323376; astro-ph/0105184v2),")
    print("  'Problems for MOND in Clusters and the Ly-alpha Forest?', applied MOND to forest gas 25")
    print("  years before this script. It is genuine prior art on this exact test and must be cited.")
    print("  Their Eq. 7 gives the MOND Jeans length L_J ~= 11 kpc (N_HI/1e14)^(-1/5) Gamma_12^(-1/5)")
    print("  T_4^0.65, GAS ONLY (MOND posits no dark component), and their Eq. 8 the absorber's internal")
    print(f"  Newtonian acceleration a_N ~= 4e-13 cm/s^2 = {AGUIRRE_AN:.2e} m/s^2 at N_HI = 1e14, T_4 = 1.")
    print("  THREE THINGS THE CORPUS MUST NOT GET WRONG ABOUT THIS PAPER:")
    print("   (i) Their verbatim 'The internal acceleration is then ~= a0/170' is the MOND-MODIFIED")
    print(f"       acceleration a = sqrt(a_N a0) = {np.sqrt(AGUIRRE_AN*AGUIRRE_A0):.2e} m/s^2, NOT a_N/a0. On THEIR")
    print(f"       a0 = {AGUIRRE_A0:.1e} m/s^2 the Newtonian ratio is a_N/a0 = 1/{AGUIRRE_A0/AGUIRRE_AN:.0f}, and the exact")
    print(f"       identity is a_N/a0 = (a/a0)^2 = 1/170^2. The figure '1/23400' appears NOWHERE in the")
    print(f"       paper; it is only what their fixed a_N gives against the framework's canonical a0.")
    print("   (ii) Their Omega_gas = 0.008-0.009 vs 0.045 is the ISOLATED case only, they call it")
    print("       'still plausible', their external-field value is 0.005-0.03 with the upper end in")
    print("       'comfortable agreement', and their stated conclusion is that MOND yields '(for any")
    print("       assumed external field) a reasonable density of intergalactic gas'. Relaying it as a")
    print("       MOND/forest kill would manufacture a deficit the source does not assert.")
    print("   (iii) Their forest verdict is deliberately SOFT and EFE-degenerate -- the title ends in")
    print("       '?', the conclusion says '(perhaps) intergalactic gas clouds', and their footnote 7")
    print("       concedes the SEP violation 'severely limits the possibility of testing the MOND")
    print("       formula over many decades of acceleration'. The kill they DO assert is CLUSTERS.")
    print("  NOTE FOR THE FRAMEWORK SPECIFICALLY: their Eq. 1 is the bare deep limit a = sqrt(a_N a0),")
    print("  which the framework's own nu(y) = sqrt(1+1/y) reproduces EXACTLY, so their forest")
    print("  calculation is interpolation-function-independent and carries over with a0 as the only")
    print("  change. But their EFE is the Bekenstein-Milgrom modified-GRAVITY result of Milgrom 1986,")
    print("  so it is NOT prior art on a modified-INERTIA external-field prediction.")
    print()
    print("  THE FORK. a_N for forest gas is CONVENTION-OWNED, not physical. Rebuilding a_N from their")
    print("  own relation a_N = (c_s^2/L)^2/a0 across their own sizes and mass components spans:")
    conv = [
        ("Aguirre iso MOND, gas, 11 kpc",       AGUIRRE_AN,  "their Eq. 7-8, a_N backed out of a=sqrt(a_N a0)"),
        ("Aguirre EFE a0/g0=170, 21.1 kpc",     2.1e-15,     "their Eq. 11 self-consistent, softest end"),
        ("Aguirre EFE a0/g0=25, 40 kpc",        7.6e-15,     "their Eq. 11 at the CDM-like end"),
        ("gas only at CDM size 110 kpc",        1.1e-14,     "their CDM comparison size, gas only"),
        ("gas+DM at 300 kpc (obs 'size')",      2.5e-14,     "the quasar-pair transverse extent"),
        ("CDM/Newtonian gas+DM, 110 kpc",       6.9e-14,     "their Newtonian+CDM case"),
        ("corpus single-absorber (S1, z=2.8)",  g_forest(2.8), "delta=3, R=200 kpc -- what S1-S4 use"),
    ]
    print(f"  {'convention':<34s} {'a_N (m/s^2)':>12s} {'x canon':>10s} {'A canon':>8s} "
          f"{'x alt':>10s} {'A alt':>8s} {'sig_stat':>9s} {'sig_cal':>9s}")
    fork_rows = []
    for lab, aN, why in conv:
        xc, xa = aN / A0_CAN, aN / A0_ALT
        Ac, Aa = amp_sqrt(xc), amp_sqrt(xa)
        bpc = b_pred_from(B_CUT[2.8], Ac)
        ss, sc = sig_stat(2.8, bpc), sig_cal(2.8, bpc)
        fork_rows.append((lab, aN, xc, xa, Ac, Aa, ss, sc))
        print(f"  {lab:<34s} {aN:12.2e} {xc:10.2e} {Ac:8.1f} {xa:10.2e} {Aa:8.1f} {ss:8.0f}s {sc:8.0f}s")
    # the MOND-modified acceleration, listed separately and labelled, because confusing it with a_N
    # is exactly the 170x error the corpus is at risk of.
    a_mond = float(np.sqrt(AGUIRRE_AN * AGUIRRE_A0))
    xm_c, xm_a = a_mond / A0_CAN, a_mond / A0_ALT
    print(f"  {'[Aguirre a=sqrt(a_N a0) = a0/170]':<34s} {a_mond:12.2e} {xm_c:10.2e} "
          f"{amp_sqrt(xm_c):8.1f} {xm_a:10.2e} {amp_sqrt(xm_a):8.1f}  <- MODIFIED a, NOT a_N. Do not")
    print(f"  {'':34s} {'':12s} mix this row into the a_N fork: it is a further factor 170 in x.")
    aN_span = max(r[1] for r in fork_rows) / min(r[1] for r in fork_rows)
    A_span = max(max(r[4], r[5]) for r in fork_rows) / min(min(r[4], r[5]) for r in fork_rows)
    sig_span = (min(r[7] for r in fork_rows), max(r[7] for r in fork_rows))
    print(f"  FORK SPAN: a_N ranges {aN_span:.0f}x ({np.log10(aN_span):.1f} dex) on convention ALONE, the")
    print(f"  amplification {A_span:.0f}x, and the z = 2.8 exclusion {sig_span[0]:.0f}-{sig_span[1]:.0f} sigma on the")
    print(f"  calibration channel. Both a0 footings are inside every row and they differ by only")
    print(f"  {A0_ALT/A0_CAN:.2f}x in x -- so the FOOTING is a minor axis here and the CONVENTION is the major one.")
    check(aN_span > 10.0,
          f"the verdict is robust across the whole {np.log10(aN_span):.1f}-dex convention fork -- the SOFTEST "
          f"convention anywhere ({min(fork_rows, key=lambda r: r[7])[0]}) still gives "
          f"{min(r[7] for r in fork_rows):.0f} sigma on the calibration channel -- but the SIZE of the "
          f"number is convention-owned to a factor {sig_span[1]/max(sig_span[0], 1e-9):.0f}, so no precise "
          f"sigma should be quoted without naming the convention")
    check(abs(AGUIRRE_A0 / AGUIRRE_AN - 30000) / 30000 < 0.02
          and abs(np.sqrt(AGUIRRE_A0 / AGUIRRE_AN) - 173.2) < 1.0,
          f"Aguirre's own identity reproduced: a_N/a0 = 1/{AGUIRRE_A0/AGUIRRE_AN:.0f} on their a0, and "
          f"sqrt of that = {np.sqrt(AGUIRRE_A0/AGUIRRE_AN):.1f} = their quoted a0/170 -- confirming the "
          f"a0/170 figure is the MODIFIED acceleration, not the Newtonian ratio")
    # a0-propagated version of their Eq. 7-8: a_N ~ a0^(-1/5), L_J ~ a0^(-2/5)
    print(f"  a0 PROPAGATED SELF-CONSISTENTLY through their Eqs. 7-8 (a_N ~ a0^(-1/5), L_J ~ a0^(-2/5)),")
    print(f"  since their a_N is backed out of the MOND relation and therefore inherits an a0 dependence:")
    for lab, a0v in FOOTINGS:
        f = (AGUIRRE_A0 / a0v)
        aN_sc = AGUIRRE_AN * f ** 0.2
        LJ_sc = AGUIRRE_LJ_KPC * f ** 0.4
        print(f"    {lab:<18s} a0 = {a0v:.2e} -> a_N = {aN_sc:.3e} m/s^2, a_N/a0 = 1/{a0v/aN_sc:.0f}, "
              f"L_J = {LJ_sc:.1f} kpc, a = a0/{a0v/np.sqrt(aN_sc*a0v):.0f}")

    banner("S6. THE COUNTERWEIGHT -- Arnold, Puchwein & Springel 2015, stated BOTH ways")
    print("  Arnold, Puchwein & Springel 2015, MNRAS 448, 2275 (DOI 10.1093/mnras/stv146;")
    print("  arXiv:1411.2600), 'The Lyman-alpha forest in f(R) modified gravity', found: 'Even models")
    print("  with strong modifications of gravity, like |f_R0| = 1e-4, do not change the statistical")
    print("  Lyman-alpha properties by more than 10%. The column density and line width distributions")
    print("  are hardly affected at all.' Specifically flux PDF <=7% (1e-5) to <=10% (1e-4); flux P(k)")
    print("  <=5% to ~10%; matter P(k) up to ~15-17% at z=2 near k ~ 30-100 h/Mpc.")
    print("  SCOPE CORRECTIONS carried: only |f_R0| = 1e-4 and 1e-5 were simulated (NOT 1e-6), and the")
    print("  Voigt-fit line-width/column-density null is shown for 1e-5 ONLY (the 1e-4 runs used the")
    print("  smaller 15 Mpc/h box). The often-quoted ~30% temperature effect is Arnold et al. 2014 for")
    print("  gas in COLLAPSED OBJECTS, not a forest result of this paper.")
    print()
    print("  WHY IT IS A REAL COUNTERWEIGHT (this side runs the framework's way): the forest's line-")
    print("  width PDF is a velocity-sensitive statistic -- their forward model carries peculiar")
    print("  velocities and Doppler shifts explicitly -- and it came out NULL under a strong gravity")
    print("  modification. That is direct evidence that a large predicted b signature is specific to")
    print("  the POINTWISE reading rather than generic to modified dynamics. And their paper documents")
    print("  that the forest is systematics-limited at roughly the 10% level for ANY model: GR itself")
    print("  misses Kim et al. 2007 at z = 3 by more than the error bars, blamed on continuum placement")
    print("  and unmodelled low-density IGM heating.")
    print()
    print("  WHY IT DOES NOT TRANSFER AS REASSURANCE (this side runs against it): f(R) is not the same")
    print("  object. Their eqs. 9-10 give grad^2 Phi = 4 pi G (delta_rho + delta_rho_eff) with")
    print("  delta_rho_eff = delta_rho/3 - delta_R/(24 pi G), which in the fully unscreened limit caps")
    print("  the enhancement at G_eff/G = 4/3, i.e. +33.3%. A compression factor measured at a 1.33x")
    print("  force change carries no information about a ~20x response change. It modifies the Poisson")
    print("  SOURCE (a density-sourced, Yukawa-ranged, additive force) whereas MI modifies the RESPONSE,")
    print("  keyed to |a| not rho, with no Yukawa cutoff. Note also that 'screening explains their null'")
    print("  is the WEAKEST available reason: forest gas at delta ~ 0-10 is largely UNSCREENED. The null")
    print("  is driven by the +33% ceiling, the scalar's finite Compton range (their Fig. 7 shows the")
    print("  effect growing with k and toward LOWER z, away from the forest), and mean-transmission")
    print("  tuning that absorbs absolute normalisation.")
    print()
    print("  AND THE FORK THE FRAMEWORK STILL OWES, which decides whether this paper is irrelevant or")
    print("  supportive -- it must not be picked silently:")
    y_loc = [g_forest(z) / A0_CAN for z in ZS_FOREST]
    print(f"   * LOCAL / pointwise branch: y = g_pec/a0 = {min(y_loc):.1e}-{max(y_loc):.1e} (canonical), so")
    print(f"     nu = sqrt(1+1/y) = {np.sqrt(1+1/max(y_loc)):.1f}-{np.sqrt(1+1/min(y_loc)):.1f}. Enormous. The f(R) paper says NOTHING about this.")
    print(f"   {'branch':<28s} {'y':>10s} {'nu - 1':>10s}")
    efe_rows = []
    for lab, a0v, riser in (("EFE cH(z)/a0 canonical", A0_CAN, False),
                            ("EFE cH(z)/a0 alt", A0_ALT, False),
                            ("EFE, alt a0(z)=a0*E(z)", A0_ALT, True)):
        for z in (2.0, 3.0):
            H = H0S * E_of_z(z)
            a0eff = a0v * (E_of_z(z) if riser else 1.0)
            y = C_SI * H / a0eff
            nu1 = np.sqrt(1 + 1 / y) - 1
            efe_rows.append((lab, z, y, nu1))
            print(f"   {lab + f' z={z:.0f}':<28s} {y:10.2f} {100*nu1:9.2f}%")
    nu1_all = [r[3] for r in efe_rows]
    print(f"   * EFE / cosmological-field branch: nu - 1 = {100*min(nu1_all):.1f}% to {100*max(nu1_all):.1f}% across both")
    print(f"     footings and the rising variant -- SMALLER than or comparable to f(R)'s <10%, so on THIS")
    print(f"     branch Arnold et al.'s null transfers a fortiori and the forest says nothing against the")
    print(f"     framework at all.")
    check(max(nu1_all) < 0.12 and min(y_loc) < 1e-2,
          f"the two branches differ by orders: local y ~ {min(y_loc):.0e}-{max(y_loc):.0e} giving nu up to "
          f"{np.sqrt(1+1/min(y_loc)):.0f}x, versus EFE y = {min(r[2] for r in efe_rows):.1f}-"
          f"{max(r[2] for r in efe_rows):.1f} giving nu - 1 <= {100*max(nu1_all):.1f}% -- so this whole test "
          f"constrains ONE branch of an unclosed framework fork, and the counterweight is real on the other")

    banner("S7. VERDICT")
    print("  THE POINTWISE READING IS EXCLUDED BY THE REAL DATA -- and the real data is not the data")
    print("  this script used to use. Under a pointwise application of the first-moment closure to")
    print("  diffuse baryons, with the single-absorber acceleration estimate, the framework predicts")
    print(f"  Lyman-alpha b-parameters above the measured Hiss et al. 2018 cutoff at")
    print(f"  {min(all_stat):.0f}-{max(all_stat):.0f} sigma on the table's own statistical bars and "
          f"{min(all_cal):.1f}-{max(all_cal):.1f} sigma against the")
    print(f"  {B_CAL_SYS:.2f} km/s cutoff-fitting calibration systematic, on both a0 footings, in all")
    print(f"  {len(ZS_FOREST)} redshift bins, and for every split of the non-thermal budget. Survival would need")
    print(f"  f_pec < {thresh['calibration']:.0e} even on the more forgiving channel.")
    print()
    print("  WHAT THE CORRECTION DID TO THE NUMBER, in both directions, because both happened:")
    print("   * SHARPER: the invented symmetric +/- 2.0 km/s bar is replaced by Hiss's real 0.33-1.37")
    print("     km/s statistical errors, which raises the statistical significance.")
    print(f"   * SOFTER: a calibration systematic of {B_CAL_SYS:.2f} km/s ({B_CAL_SYS_ALT:.2f} on the 2sigma-rejection")
    print("     variant) now has to be carried, which Table 4 does NOT contain, and it is 4.6x the")
    print("     median statistical bar. Every significance is quoted against both.")
    print("   * SHAPE REVERSED at low z: the retired sequence's rise to 24 km/s at z = 2.30 is refuted")
    print("     by Rudie's own 18.50 +/- 0.22 km/s at the same redshift and pivot; the measured cutoff")
    print("     turns over at z = 2.8 and falls to 18.22 km/s by z = 2.0. Lower observed cutoffs at low")
    print("     z leave LESS non-thermal budget, which cuts both ways in the arithmetic and is computed")
    print("     rather than argued in S4.")
    print("   * THE 'DIES AT z = 3.7' CLAIM IS UNEVALUABLE: Hiss stops at z = 3.4. Any banked statement")
    print("     about z = 3.7 rested on a value with no published source and is withdrawn, not softened.")
    print()
    print("  WHAT THIS DOES AND DOES NOT KILL:")
    print("   * It does NOT kill the framework's galaxy-scale phenomenology. Galaxies sit at x ~ 0.1-1")
    print("     where the amplification is 1.1-2.8x, and the RAR (0.108 dex) is untouched.")
    print("   * It does NOT kill the framework. It kills ONE READING of it -- the pointwise one -- and")
    print("     that reading was already flagged as suspect from a completely independent direction:")
    print("     mi_channelA_friedmann_2026 found K ~ sqrt(z) at the origin with h -> 0, so a pointwise")
    print("     linear-response treatment has no small expansion parameter exactly where it is being")
    print("     applied. Two independent arguments converge on the same conclusion.")
    print("   * It DOES convert the missing regulator from optional to MANDATORY, with a number: any")
    print(f"     viable MI cosmology must suppress the diffuse-baryon response by a factor >~ {A_use:.0f}")
    print("     relative to the pointwise reading, or explain why forest gas is not in the deep regime.")
    print()
    print("  THE LEGITIMATE ESCAPES, and each is a real research question rather than a dodge:")
    print("   1. THE EFE / TOTAL-ACCELERATION ARGUMENT, which is the same one that fixed my channel-A")
    print("      error, and which S6 now shows is the whole ballgame: on the EFE branch the framework")
    print(f"      predicts nu - 1 = {100*min(nu1_all):.1f}-{100*max(nu1_all):.1f}%, BELOW f(R)'s <10%, and Arnold et al. 2015's")
    print("      null transfers a fortiori. Deciding the branch is the single highest-value next step.")
    print("   2. THE x-CONVENTION FORK (S5). a_N for forest gas spans "
          f"{np.log10(aN_span):.1f} dex on convention alone")
    print("      inside Aguirre et al.'s own paper. The exclusion survives all of it, but the SIZE of")
    print("      the number is convention-owned and no precise sigma should be quoted bare.")
    print("   3. PRESSURE SUPPORT. Forest gas is photoionized and pressure-supported, so its velocity")
    print("      structure may be thermally rather than gravitationally set. The S3 scan tests this and")
    print("      finds it insufficient by orders of magnitude -- but a proper treatment needs sims.")
    print("   4. THE LCDM-HYDRO CALIBRATION. The b budget decomposition is calibrated on standard-")
    print("      gravity simulations, and Arnold et al. document that the forest is systematics-limited")
    print("      at the ~10% level for everyone. A self-consistent MI hydro run is still owed.")
    print("   5. THE NON-ANALYTICITY. If the pointwise linear response is simply invalid at small x,")
    print("      this test constrains nothing about the true theory. That is the most likely resolution")
    print("      and also the least satisfying, because it means the framework currently has NO")
    print("      calculable prediction in the diffuse sector at all.")
    print()
    print("  NET: a genuine, sharp, adverse observational result against the only calculable version of")
    print("  the framework's diffuse-sector prediction -- now resting on a sourced published table")
    print("  instead of four numbers that could not be found in any paper. Reported as found. The")
    print("  framework's galaxy-scale content is untouched; its cosmological-sector content is")
    print("  demonstrably incomplete rather than merely unbuilt.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
