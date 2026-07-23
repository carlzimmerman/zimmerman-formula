#!/usr/bin/env python3
"""
highz_systematics_floor.py -- THE IRREDUCIBLE PER-BIN SYSTEMATIC FLOOR ON a0(z) AT z>0,
AND THE HONEST GO / NO-GO FOR THE ZERO-PARAMETER CROSS-REDSHIFT a0-LINE TEST
========================================================================================
ROLE (one agent of the a0(z) cross-scale showdown): the "parameter-counting" side
(discriminating_power_a0z.py) fixed the REQUIRED per-bin measurement precision for the
framework's zero-parameter a0(z) = a0(0)*sqrt(rho_DE(z)/rho_DE0) prediction to reject
flat=1 (const-a0 MOND) and beat the fitted rivals. This script asks the complementary,
decisive question: is that precision REACHABLE, or is it floored by high-z kinematic
systematics that do NOT average down with sample size?

The framework under test (Zimmerman dS-Unruh MODIFIED INERTIA -- its OWN interpolation,
NOT standard MOND): nu = sqrt(1+1/y), a0 = c H_Lambda/Z, and the EXACT a0-line identity
    E := g_obs^2 - g_bar^2 = a0 * g_bar   at every acceleration.
The a0-line estimator reads a0 = E/g_bar. This is the estimator carried up in z.

WHAT MAKES z>0 QUALITATIVELY WORSE THAN z=0 (the four floors, each amplified by the
deep-MOND a0=g_obs^2/g_bar readout -- derived in S0):
  (i)   BEAM SMEARING: shrinking angular size at z>0 -> R_beam/R_d ~ O(1) -> the outer
        (deep-MOND) rotation velocity is suppressed; residual after 3D forward-modeling.
  (ii)  TURBULENT PRESSURE SUPPORT / ASYMMETRIC DRIFT: sigma_0 RISES with z while V_rot in
        the outer disk does not, so V/sigma collapses (~10-20 locally -> ~1.5-5 at z~1-2).
        The correction V_c^2 = V_rot^2 + 2(R/R_d) sigma_0^2 becomes O(30-130%) of V_rot^2;
        its RESIDUAL is the dominant high-z systematic and, being sigma_0(z)-driven, is a
        COHERENT z-trend that directly mimics / masks the predicted a0(z) evolution.
  (iii) GAS-MASS CALIBRATION DRIFT: at z>~0.5 HI is inaccessible; g_bar leans on CO(alpha_CO,
        metallicity-dependent, ~0.2-0.3 dex) or [CII] (~0.3-0.5 dex). The z-DEPENDENCE of this
        offset does NOT cancel in the a0(z)/a0(0) ratio.
  (iv)  UPSILON (stellar M/L): the z=0 floor, but stellar pops are younger/bluer/burstier
        + dustier at high z -> larger; suppressed on gas-dominated points, swamps
        star-dominated (HSB, rotation-selected) ones.
Added in quadrature per z bin, in two regimes (gas-rich DWARF = the clean a0-line sample;
massive HSB DISK = the rotation-selected sample) and two eras (TODAY warm-tracer / FUTURE
cold-tracer + high-res + corrected).

HONESTY RAILS (manufactured NO-GO penalized exactly as a manufactured GO):
 * Every systematic is a RESIDUAL after best-effort correction (3D forward modeling, nominal
   asymmetric-drift correction, metallicity-based alpha_CO), NOT the raw uncorrected bias.
   The residual fractions f_res are stated fiducials, sourced in comments, and swept.
 * The bottom-up floor is CROSS-CHECKED against the independent, real per-sample systematic
   bands already in the committed high-z TFR ledger (highz_tfr_fork/data_ledger.csv):
   Uebler+17 +/-0.35 dex, Jeanneau+26 +/-0.27 dex, Amvrosiadis+25 +/-0.30 dex -- and against
   the ledger's smoking gun that the two best z~1 bTFR points are 6 sigma MUTUALLY
   inconsistent on stat errors (systematics, not statistics, dominate). If my bottom-up
   number contradicted the empirical bands I would trust the data; it does not.
 * Both footings noted where absolute scale is load-bearing (ratio is footing-independent).
 * No "theory closed." Exit 0 = floor computed + GO/NO-GO rendered, NOT a verdict.

Fiducials (stated, not hidden), sourced in-line:
  sigma_0(z): warm ionized 15+15z km/s; cold (CO/[CII]/stellar) ~0.6x (Uebler+19 KMOS3D,
     Wisnioski+15/19). V_rot(outer,~2.2Rd): massive disk 150, gas-rich dwarf 70 km/s.
  Asymmetric-drift: V_c^2=V_rot^2+2(R/Rd)sigma_0^2, R/Rd=2.2 (Burkert+10, Uebler+18, Genzel+17).
  residual pressure fraction f_res: TODAY 0.50, FUTURE 0.30 (sigma_0 +/-20% -> dC/C=40%, plus
     prescription/anisotropy/sigma-gradient ~30%, in quadrature).
  beam residual after 3D modeling: 2%+5%*(R_beam/R_d) on V (Di Teodoro&Fraternali15, Uebler+18).
  gas-cal residual on g_bar: TODAY 0.12+0.06z dex, FUTURE 0.08+0.03z dex (Bolatto+13 alpha_CO;
     Tacconi+18/20 f_gas). Upsilon ln-scatter: TODAY 0.35 (0.15 dex), FUTURE 0.23 (0.10 dex).
  Required precision (from discriminating_power_a0z.py, Pantheon+ central, deep-MOND-penalized):
     z=2: 4.2% (3s)/2.5% (5s) on a0(z)/a0(0);  z=3: 7.5% (3s)/4.5% (5s).
"""
import numpy as np
import sympy as sp
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
DEX = np.log(10.0)
bar = "=" * 96
A0_CANON, A0_ALT = 9.36e-11, 1.13e-10          # canonical rho_DE/cH_Lambda ; alt rho_total/cH0

# =====================================================================================
# S0 -- THE DEEP-MOND AMPLIFICATION (sympy): how a per-point error on V, g_obs, g_bar
#       propagates into the a0-line readout a0 = (g_obs^2 - g_bar^2)/g_bar. Reproduces
#       estimator_theory.py S3 (framework's OWN sensitivities, not McGaugh's).
# =====================================================================================
print(bar); print("S0 -- DEEP-MOND AMPLIFICATION of per-point errors into a0 (sympy; framework-native)"); print(bar)
a0s, yv, phi = sp.symbols("a0 y phi", positive=True)
go, gbv = sp.symbols("g_obs g_bar", positive=True)          # INDEPENDENT observables
a0_read = (go**2 - gbv**2) / gbv                            # the a0-line readout
# framework relation on the model manifold, in terms of y: g_bar=a0*y, g_obs^2=a0^2*y(y+1)
onshell = {go: sp.sqrt(a0s**2 * yv * (yv + 1)), gbv: a0s * yv}
assert sp.simplify(a0_read.subs(onshell) - a0s) == 0        # readout == a0 (identity)
# d ln a0 / d ln g_obs, then put on-shell and express in y ; g_obs=V^2/R -> d ln g_obs=2 d ln V
amp_gobs = sp.simplify((sp.diff(sp.log(a0_read), go) * go).subs(onshell))
amp_V    = sp.simplify(2 * amp_gobs)
amp_gbar = sp.simplify((sp.diff(sp.log(a0_read), gbv) * gbv).subs(onshell))
print(f"  a0-line readout a0 = (g_obs^2-g_bar^2)/g_bar  verified == a0 (identity).")
print(f"  d ln a0 / d ln g_obs = {amp_gobs}   ( = 2(y+1) )")
assert sp.simplify(amp_gobs - 2 * (yv + 1)) == 0
print(f"  d ln a0 / d ln V     = {amp_V}      ( = 4(y+1) : the deep-MOND velocity penalty )")
assert sp.simplify(amp_V - 4 * (yv + 1)) == 0
print(f"  d ln a0 / d ln g_bar = {sp.factor(amp_gbar)}   ( = -(2y+1); gas part scales by (1-phi) )")
assert sp.simplify(amp_gbar + (2 * yv + 1)) == 0
print("  => a velocity error is amplified 4(y+1)x, a g_obs (pressure) error 2(y+1)x, a gas-mass")
print("     error (2y+1)(1-phi)x, an Upsilon error phi(2y+1)x. ALL grow with y: the high-g")
print("     (massive-disk) points where signal is smallest are where systematics blow up most.")

AMP_V    = lambda y: 4.0 * (y + 1.0)
AMP_GOBS = lambda y: 2.0 * (y + 1.0)
AMP_GBAR = lambda y: (2.0 * y + 1.0)

# =====================================================================================
# S1 -- sigma_0(z), V/sigma(z), and the asymmetric-drift correction magnitude
# =====================================================================================
print("\n" + bar); print("S1 -- PRESSURE SUPPORT: sigma_0(z), V/sigma, and the asymmetric-drift correction C"); print(bar)
R_OVER_RD = 2.2                                 # outer measurement radius, ~ V2.2 (RC peak)
K_AD = 2.0 * R_OVER_RD                           # V_c^2 = V_rot^2 + K_AD*sigma_0^2 (exp disk)
def sigma0(z, cold):                             # km/s ; Uebler+19, Wisnioski+15/19
    return (10.0 + 7.0 * z) if cold else (15.0 + 15.0 * z)
def C_AD(z, Vrot, cold):                          # dimensionless AD correction fraction
    return K_AD * sigma0(z, cold) ** 2 / Vrot ** 2
REG = {"dwarf (gas-dom, y=0.5)": dict(y=0.5, phi=0.15, Vrot=70.0),
       "intermediate gas-rich (y=0.5)": dict(y=0.5, phi=0.30, Vrot=110.0),
       "massive disk (HSB, y=2.5)": dict(y=2.5, phi=0.60, Vrot=150.0)}
ZS = [0.5, 1.0, 2.0, 3.0]
print(f"  V_c^2 = V_rot^2 + {K_AD:.1f}*sigma_0^2  (R/Rd={R_OVER_RD}); C = correction/V_rot^2.")
for rlab, rp in REG.items():
    print(f"\n  [{rlab}]  V_rot={rp['Vrot']:.0f} km/s")
    print(f"    {'z':>4} | {'sig0_warm':>9} {'V/sig_w':>8} {'C_warm':>7} | {'sig0_cold':>9} {'V/sig_c':>8} {'C_cold':>7}")
    for z in ZS:
        sw, sc = sigma0(z, False), sigma0(z, True)
        Cw, Cc = C_AD(z, rp["Vrot"], False), C_AD(z, rp["Vrot"], True)
        print(f"    {z:>4.1f} | {sw:>9.0f} {rp['Vrot']/sw:>8.2f} {Cw:>7.2f} | "
              f"{sc:>9.0f} {rp['Vrot']/sc:>8.2f} {Cc:>7.2f}")
print("\n  READING: for the gas-rich DWARF (the CLEAN a0-line sample) the warm-tracer AD")
print("  correction reaches C~1.8 at z=2 (V/sigma~1.6 -- barely a disk): the pressure term")
print("  is LARGER than the rotation term. Massive disks keep V/sigma~3-5 (C~0.4) but are")
print("  star-dominated (see phi). A dynamically COLD tracer (CO/[CII]/stellar) roughly halves")
print("  sigma_0 and is the ONLY lever that tames C. This is the crux of the go/no-go.")

# =====================================================================================
# S2 -- BEAM SMEARING: angular size vs beam, residual after 3D forward modeling
# =====================================================================================
print("\n" + bar); print("S2 -- BEAM SMEARING: R_beam/R_d vs z, residual dV/V after 3D forward-modeling"); print(bar)
def d_A(z, Om=0.3, H0=70.0):                     # angular-diameter distance, flat LCDM (Mpc)
    c = 299792.458
    zz = np.linspace(0, z, 2000)
    Ez = np.sqrt(Om * (1 + zz) ** 3 + (1 - Om))
    Dc = (c / H0) * np.trapz(1.0 / Ez, zz)
    return Dc / (1 + z)
RD_PHYS = 3.0                                     # kpc, massive disk; *(1+z)^-0.75 compactness
def theta_Rd(z):                                  # arcsec subtended by R_d(z)
    Rd = RD_PHYS * (1 + z) ** (-0.75)             # van der Wel+14 size evolution
    return (Rd / 1e3) / d_A(z) * 206265.0
BEAMS = {"seeing IFU (KMOS/SINFONI 0.6\")": 0.60,
         "JWST NIRSpec-IFU / ALMA (0.15\")": 0.15,
         "ELT/ALMA-hi-res (0.05\")": 0.05}
def dV_beam(ratio):                               # residual dV/V after 3D modeling (Barolo/DYSMAL)
    return 0.02 + 0.05 * ratio                    # Di Teodoro&Fraternali15, Uebler+18 calibration
print(f"  R_d(z)=3 kpc*(1+z)^-0.75; theta_Rd in arcsec; residual dV/V = 2% + 5%*(R_beam/R_d).")
print(f"    {'z':>4} {'theta_Rd(\")':>11} | " + " | ".join(f"{b:>32}" for b in BEAMS))
for z in ZS:
    th = theta_Rd(z)
    cells = []
    for blab, bfw in BEAMS.items():
        ratio = bfw / th
        cells.append(f"r={ratio:>4.2f} dV={100*dV_beam(ratio):>4.1f}%")
    print(f"    {z:>4.1f} {th:>11.3f} | " + " | ".join(f"{c:>32}" for c in cells))
print("\n  READING: seeing-limited IFU is R_beam/R_d~1-2 at z>1 (dV/V~7-12% residual EVEN after")
print("  3D modeling); JWST/ALMA at 0.15\" gets R_beam/R_d~0.4-0.7 (dV/V~4-5%); only ELT-class")
print("  0.05\" reaches R_beam/R_d<0.3 (dV/V~3%). Every % of dV is x4(y+1) in a0.")

# =====================================================================================
# S3 -- ASSEMBLE THE PER-BIN a0(z) SYSTEMATIC FLOOR (quadrature), by regime x era x z
# =====================================================================================
print("\n" + bar); print("S3 -- PER-BIN a0(z) FRACTIONAL SYSTEMATIC FLOOR  (residuals, in quadrature)"); print(bar)
def gascal_dex(z, era):   return (0.12 + 0.06 * z) if era == "TODAY" else (0.08 + 0.03 * z)
def ups_ln(era):          return 0.35 if era == "TODAY" else 0.23
def fres(era):            return 0.50 if era == "TODAY" else 0.30
def beam_ratio(z, era):   # today = JWST/ALMA 0.15" (best routine); future = ELT 0.05"
    return (0.15 if era == "TODAY" else 0.05) / theta_Rd(z)

def floor(z, rp, era, cold):
    y, phi = rp["y"], rp["phi"]
    # (i) beam -> velocity
    s_beam = AMP_V(y) * dV_beam(beam_ratio(z, era))
    # (ii) pressure support -> g_obs (residual of the AD correction)
    C = C_AD(z, rp["Vrot"], cold)
    dgobs_press = fres(era) * C / (1.0 + C)
    s_press = AMP_GOBS(y) * dgobs_press
    # (iii) gas-mass calibration -> gas part of g_bar
    s_gas = AMP_GBAR(y) * (1.0 - phi) * gascal_dex(z, era) * DEX
    # (iv) Upsilon -> stellar part of g_bar
    s_ups = AMP_GBAR(y) * phi * ups_ln(era)
    tot = np.sqrt(s_beam**2 + s_press**2 + s_gas**2 + s_ups**2)
    # GLOBAL (does NOT average down over N_gal) vs AVERAGEABLE (random per-galaxy) split:
    #  gas-cal 100% global (one alpha_CO/tracer calibration for all); Upsilon 70% global (SPS-model
    #  systematic common, some random color/dust); pressure ~50% global (AD prescription/anisotropy/
    #  R-Rd coeff common) + 50% random (per-galaxy sigma_0 noise); beam 30% global (PSF-model) + 70%.
    fG = dict(beam=0.30, press=0.50, gas=1.00, ups=0.70)
    s_glob = np.sqrt((fG["beam"]*s_beam)**2 + (fG["press"]*s_press)**2
                     + (fG["gas"]*s_gas)**2 + (fG["ups"]*s_ups)**2)   # survives N -> infinity
    return dict(beam=s_beam, press=s_press, gas=s_gas, ups=s_ups, tot=tot, C=C, glob=s_glob)

SCEN = [("TODAY", "warm", False), ("FUTURE", "cold", True)]
results = {}
for rlab, rp in REG.items():
    for era, tname, cold in SCEN:
        print(f"\n  [{rlab}]  era={era} tracer={tname}")
        print(f"    {'z':>4} | {'beam':>7} {'PRESS':>7} {'gas':>7} {'Upsil':>7} | {'C_AD':>6} | "
              f"{'TOTAL a0 floor':>14} | {'dex':>6}")
        for z in ZS:
            f = floor(z, rp, era, cold)
            results[(rlab, era, z)] = f
            print(f"    {z:>4.1f} | {100*f['beam']:>6.1f}% {100*f['press']:>6.1f}% {100*f['gas']:>6.1f}% "
                  f"{100*f['ups']:>6.1f}% | {f['C']:>6.2f} | {100*f['tot']:>13.1f}% | {f['tot']/DEX:>6.3f}")
print("\n  READING: PRESSURE support (PRESS) is the dominant term at z>=1 in the warm-tracer TODAY")
print("  rows -- for the gas-rich dwarf it alone exceeds 50-100% of a0 at z=2-3. Switching to a COLD")
print("  tracer (FUTURE) roughly halves it, at which point GAS-MASS CALIBRATION becomes the leader")
print("  (e.g. intermediate FUTURE z=2: gas 45%, press 16%). The massive-disk rows are Upsilon-")
print("  swamped (star-dominated, high y): total >100% regardless -- confirming the a0-line signal")
print("  is NOT in massive HSB disks. No row's TOTAL comes near the ~4-8% requirement.")

# =====================================================================================
# S4 -- CROSS-CHECK vs the REAL per-sample systematic bands in the committed TFR ledger
# =====================================================================================
print("\n" + bar); print("S4 -- CROSS-CHECK: bottom-up floor vs REAL high-z TFR per-sample sys bands (ledger)"); print(bar)
# highz_tfr_fork/data_ledger.csv total per-sample systematic (dex, bTFR zero-point = -dlog a0
# in the deep-MOND limit, diluted by gbar/a0 otherwise). These are INDEPENDENT, published.
LEDGER = [("Jeanneau+26 (z~0.9, OII, lensed dwarf)", 0.9, 0.27),
          ("Uebler+17 (z~0.9, Halpha, KMOS3D)",       0.9, 0.35),
          ("Uebler+17 (z~2.3, Halpha, KMOS3D)",       2.3, 0.35),
          ("Amvrosiadis+25 (z~2.4, CO, ALMA DSFG)",   2.4, 0.30)]
print("  Real published total-systematic bands on the bTFR zero-point (~ dex on a0 in deep-MOND):")
for lab, z, sysdex in LEDGER:
    print(f"    {lab:44} z={z:.1f}  sys ~ {sysdex:.2f} dex  (~{100*(10**sysdex-1):.0f}% on a0 in deep-MOND)")
# my bottom-up dwarf/massive TODAY floors, in dex, at the matching z's, for comparison
b_dwarf_z1 = results[("dwarf (gas-dom, y=0.5)", "TODAY", 1.0)]["tot"] / DEX
b_dwarf_z2 = results[("dwarf (gas-dom, y=0.5)", "TODAY", 2.0)]["tot"] / DEX
b_mass_z2  = results[("massive disk (HSB, y=2.5)", "TODAY", 2.0)]["tot"] / DEX
print(f"\n  bottom-up TODAY floor (this script): dwarf z=1 ~ {b_dwarf_z1:.2f} dex, dwarf z=2 ~ "
      f"{b_dwarf_z2:.2f} dex, massive z=2 ~ {b_mass_z2:.2f} dex.")
print("  RECONCILIATION (honest): my bottom-up (0.6-1.0 dex) runs ~2x ABOVE the empirical ledger")
print("  bands (0.27-0.35 dex). The gap is real and I do NOT claim they coincide: I weight the")
print("  PRESSURE residual at f_res=0.5, whereas the best published samples (Uebler sigma0-corr,")
print("  Jeanneau Dalcanton-Stilp AD) correct pressure harder and are instead GAS/local-reference")
print("  dominated -- landing at ~0.30 dex. So the DATA-ANCHORED floor is ~0.30 dex (the number")
print("  MOST favorable to the test); my physics-based 0.6-1.0 dex is what you get if pressure")
print("  cannot be corrected as well as the best case. The go/no-go below uses BOTH and is the")
print("  SAME either way. SMOKING GUN (ledger, model-independent): the two best z~1 bTFR points")
print("  (Jeanneau 0.00 vs Uebler -0.44) are 6 SIGMA mutually inconsistent on STAT errors alone")
print("  -- direct proof the a0(z) zero-point scatter TODAY is systematics-dominated, full stop.")
EMPIRICAL_FLOOR_DEX = 0.30                        # data-anchored, most-favorable-to-test floor

# =====================================================================================
# S5 -- GO / NO-GO: floor vs REQUIRED precision (from discriminating_power_a0z.py)
# =====================================================================================
print("\n" + bar); print("S5 -- GO / NO-GO: per-bin systematic FLOOR vs REQUIRED precision to reject flat"); print(bar)
# required sigma_meas on a0(z)/a0(0), Pantheon+ central effect sizes, deep-MOND-penalized
# (these ARE the discriminating_power_a0z.py part-(b) numbers: |R_bar-1|/N_sigma)
REQ = {0.35: dict(eff=0.036, s3=0.012, s5=0.007),
       1.0:  dict(eff=0.011, s3=0.004, s5=0.002),
       2.0:  dict(eff=0.126, s3=0.042, s5=0.025),
       3.0:  dict(eff=0.225, s3=0.075, s5=0.045)}
print("  required sigma_meas(a0(z)/a0(0)) to reject flat (Pantheon+ central, deep-MOND-penalized):")
print(f"    z=2: {100*REQ[2.0]['s3']:.1f}% (3s) / {100*REQ[2.0]['s5']:.1f}% (5s);  "
      f"z=3: {100*REQ[3.0]['s3']:.1f}% (3s) / {100*REQ[3.0]['s5']:.1f}% (5s)")
print(f"\n  {'regime':26} {'era':>7} {'z':>4} {'floor':>8} {'req(3s)':>8} {'floor/req':>10}  verdict")
print(f"  {'-'*26} {'-'*7} {'-'*4} {'-'*8} {'-'*8} {'-'*10}  {'-'*7}")
gono = {}
for rlab, rp in REG.items():
    for era, tname, cold in SCEN:
        for z in (2.0, 3.0):
            fl = results[(rlab, era, z)]["tot"]
            req = REQ[z]["s3"]
            ratio = fl / req
            verdict = "GO" if ratio <= 1.0 else ("MARGINAL" if ratio <= 2.0 else "NO-GO")
            gono[(rlab, era, z)] = (fl, req, ratio, verdict)
            print(f"  {rlab:26} {era:>7} {z:>4.1f} {100*fl:>7.1f}% {100*req:>7.1f}% {ratio:>10.1f}x  {verdict}")
# CONSERVATIVE data-anchored anchor: the empirical ledger floor (0.30 dex), MOST favorable to
# the test (assumes pressure corrected as well as the best published samples). Even this is NO-GO.
emp = 10**EMPIRICAL_FLOOR_DEX - 1.0               # 0.30 dex -> fractional on a0(z)/a0(0)
print(f"\n  {'CONSERVATIVE data-anchored (ledger 0.30 dex)':40} {'':>2} "
      f"z=2 {100*emp:>5.0f}% vs {100*REQ[2.0]['s3']:.1f}% (3s) -> {emp/REQ[2.0]['s3']:>4.0f}x  NO-GO")
print(f"  {'':40} {'':>2} z=3 {100*emp:>5.0f}% vs {100*REQ[3.0]['s3']:.1f}% (3s) -> "
      f"{emp/REQ[3.0]['s3']:>4.0f}x  NO-GO")
print("\n  READING: the floor exceeds the 3-sigma requirement by ~13-24x even at the MOST GENEROUS")
print("  data-anchored floor (0.30 dex, ~100% on a0), and ~9-55x on the physics bottom-up -- a")
print("  decisive NO-GO in EVERY regime, era, and z (best single-disk case = intermediate gas-rich")
print("  FUTURE cold-tracer at z=3, still 8.7x short). The floor is a COHERENT z-dependent BIAS")
print("  (pressure support tracks sigma_0(z)), so it does NOT average down with N: no attainable")
print("  single-disk precision fixes it. Reaching the requirement needs a SEPARATE lever -- the")
print("  N->infinity (global) floor decomposition and the decisive era are in S6.")

# =====================================================================================
# S6 -- THE SINGLE MOST REALISTIC (z-bin, sample, era) THAT MAKES IT DECISIVE
# =====================================================================================
print("\n" + bar); print("S6 -- SINGLE MOST REALISTIC DECISIVE CONFIGURATION  +  the N->infinity (global) floor"); print(bar)
# The a0-line SIGNAL lives at LOW y (deep-MOND); high-y massive disks are signal-free (a0 is a
# tiny difference of large numbers, amplification (2y+1) blows up). So the decisive target is the
# INTERMEDIATE gas-rich disk: y<~1 outer points (signal) with V high enough that a COLD tracer
# keeps V/sigma>~4 (pressure correctable). Report its floor AND the part that survives N->infinity.
tgt = results[("intermediate gas-rich (y=0.5)", "FUTURE", 2.0)]
print(f"""  TARGET: z ~ 1.5-2, INTERMEDIATE gas-rich disk (V_flat ~ 100-130 km/s, f_gas high but not
  dwarf), measured to OUTER radii where g_bar < a0 (y<~1: the deep-MOND regime that carries the
  a0-line SIGNAL -- high-y massive disks are signal-free, amplification (2y+1) explodes). Cold
  tracer (CO(J)/[CII] ALMA, or stellar absorption ELT/HARMONI) at R_beam/Rd<0.3 (0.05\"), with
  sigma_0 MEASURED per-galaxy (f_res~0.3) and metallicity-calibrated alpha_CO (~0.14 dex).
    single-disk FUTURE floor at z=2: ~{100*tgt['tot']:.0f}% on a0(z)/a0(0)
      (beam {100*tgt['beam']:.0f}% + press {100*tgt['press']:.0f}% + gas {100*tgt['gas']:.0f}% + Upsilon {100*tgt['ups']:.0f}%, quadrature)
    of which GLOBAL (does NOT average down with N): ~{100*tgt['glob']:.0f}%  vs the ~4.2% (3s) requirement.""")
print(f"  THE N->INFINITY FLOOR (the decisive number): even with unlimited galaxies, only the")
print(f"  random per-galaxy part averages down; the GLOBAL part -- dominated by GAS-MASS CALIBRATION")
print(f"  (no HI at z~2; one alpha_CO/[CII] prescription for all) -- stays at ~{100*tgt['glob']:.0f}% (~{tgt['glob']/DEX:.2f} dex),")
print(f"  still ~{tgt['glob']/REQ[2.0]['s3']:.0f}x the 3-sigma requirement. Collecting more curves CANNOT cross it.")
print("\n  => DECISIVE ERA: the gas-calibration wall is only broken by DIRECT HI 21cm gas masses")
print("     (calibration <0.05 dex, no alpha_CO) -- an SKA2 / ngVLA capability at z~1.5-2 (~2035+),")
print("     combined with ELT/ALMA cold-tracer per-galaxy dynamics + per-galaxy pressure correction.")
print("     Only THEN does the global floor fall to ~0.05-0.08 dex and a ~20-40 disk campaign reach")
print("     ~4-5% aggregate -> a ~3-sigma model-independent detection of the ~13% a0 decline at z~2.")
print("  WHY NOT TODAY, AND WHY NOT EVEN THE EARLY-2030s COLD-TRACER CAMPAIGN:")
print("   (1) gas-rich DWARFS (clean a0-line) have V/sigma~1.5 at z=2 -> pressure UNCORRECTABLE;")
print("   (2) massive HSB disks are star-dominated (Upsilon-swamped) AND high-y (signal-free);")
print("   (3) the intermediate target tames pressure with a cold tracer but is then GAS-CALIBRATION")
print("       floored (~0.2 dex global) until direct HI exists. No z~1-2 sample today is at once")
print("       gas-dominated, dynamically cold, AND HI-calibrated. That triple is the >2035 target.")

# =====================================================================================
# JSON + honest caveats
# =====================================================================================
out = dict(
    amplification=dict(dlnA0_dlnV="4(y+1)", dlnA0_dlnGobs="2(y+1)", dlnA0_dlnGbar="-(2y+1)"),
    required_reject_flat=REQ,
    floors={f"{rlab}|{era}|z{z}": {k: float(v) for k, v in results[(rlab, era, z)].items()}
            for rlab in REG for era, _, _ in SCEN for z in ZS},
    global_floor_intermediate_future_z2=dict(
        total=float(tgt["tot"]), global_nonaveraging=float(tgt["glob"]),
        global_dex=float(tgt["glob"] / DEX),
        global_over_req3s=float(tgt["glob"] / REQ[2.0]["s3"])),
    empirical_floor_dex=EMPIRICAL_FLOOR_DEX,
    ledger_crosscheck_dex=dict(Jeanneau26=0.27, Uebler17=0.35, Amvrosiadis25=0.30,
                               bottom_up_dwarf_z2_dex=float(b_dwarf_z2),
                               bottom_up_massive_z2_dex=float(b_mass_z2),
                               smoking_gun="z~1 best two bTFR points 6-sigma inconsistent on stat"),
    go_no_go={f"{r}|{e}|z{z}": dict(floor=float(v[0]), req3s=float(v[1]),
                                    floor_over_req=float(v[2]), verdict=v[3])
              for (r, e, z), v in gono.items()},
    footings=dict(canonical=A0_CANON, alt=A0_ALT,
                  note="ratio a0(z)/a0(0) footing-independent; floor is on the ratio"),
    verdict="NO-GO with today's samples: the per-bin a0(z) systematic floor is ~0.3 dex (data-"
            "anchored, ~100% on a0) to ~0.6-1.0 dex (physics bottom-up), i.e. ~9-55x the ~4-8% "
            "precision needed to reject flat -- and it is a COHERENT z-dependent BIAS (pressure "
            "support tracks sigma_0(z)) that does NOT average down with N. Even a >2030 ELT/ALMA "
            "cold-tracer campaign at z~2 hits a ~0.2 dex GLOBAL (N->infinity) floor set by gas-mass "
            "calibration (~11x the requirement). Decisive only ~2035+ when DIRECT HI 21cm gas masses "
            "(SKA2/ngVLA, <0.05 dex, no alpha_CO) join ELT/ALMA cold-tracer per-galaxy dynamics + "
            "per-galaxy pressure correction on ~20-40 intermediate gas-rich disks at z~1.5-2. z=3 "
            "has the biggest signal but is data-starved; z=1 sits on the crossover null.")
json.dump(out, open(os.path.join(HERE, "highz_systematics_floor_results.json"), "w"),
          indent=1, default=float)
print("\n" + bar)
print("HONEST CAVEATS (each load-bearing; a manufactured NO-GO is penalized like a manufactured GO):")
for i, c in enumerate([
  "The floor is a RESIDUAL after best-effort correction (3D forward-modeling, nominal AD "
  "correction, metallicity alpha_CO); it is NOT the raw uncorrected bias. f_res, gas-cal dex, "
  "and beam residuals are stated fiducials and were swept TODAY(0.50)/FUTURE(0.30).",
  "The dominant term (pressure support) is a COHERENT z-dependent BIAS driven by sigma_0(z); it "
  "does NOT average down with N and directly mimics (under-correct -> false decline/'win') or "
  "masks (over-correct -> false null) the predicted a0(z) evolution. This is the deepest reason "
  "the test is not a matter of collecting more curves.",
  "The DATA-ANCHORED floor is the committed TFR ledger's real per-sample systematic bands "
  "(0.27-0.35 dex, ~100% on a0) -- the number MOST favorable to the test. My physics bottom-up "
  "runs ~2x higher (0.6-1.0 dex) because I under-correct pressure vs the best published samples; "
  "I do NOT claim they coincide. The go/no-go is NO-GO on BOTH, and the ledger's 6-sigma z~1 "
  "inter-sample inconsistency proves the scatter is systematics-dominated today regardless.",
  "The a0-line's z=0 CLEANLINESS (gas dominance kills Upsilon) INVERTS at high z: gas dominance "
  "means gas-mass calibration (no HI, alpha_CO/[CII]) becomes the floor, and gas-rich = low-mass "
  "= low V/sigma = pressure-support-destroyed. The clean sample is the worst pressure case.",
  "Ratio a0(z)/a0(0) is footing-independent (canonical 9.36e-11 vs alt 1.13e-10 cancel); the "
  "FLOOR is likewise on the ratio. Only the z=0 absolute anchor (Step A) separates footings.",
  "GO/NO-GO is CONDITIONAL on DE evolving (if w->-1 the prediction is flat and untestable). This "
  "script floors the MEASUREMENT; it does not adjudicate whether the effect exists.",
  "No 'theory closed'. The zero-parameter structure is genuinely powerful IN PRINCIPLE (0 params "
  "vs 1-2 for rivals); it is the high-z KINEMATIC DATA, not the theory, that is not ready. A "
  "weak-testability finding is stated as plainly as a win would be.",
], 1):
    print(f"  {i}. {c}")
print(bar)
print("EXIT 0: floor computed, cross-checked, go/no-go rendered. Exit code is not a verdict.")
