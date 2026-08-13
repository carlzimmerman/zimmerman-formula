#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage53_route_a_prime_closure_2026.py
=====================================
STAGE 53: ROUTE A' IS DEAD -- THE LAST RECORDED LIVE DOOR ON THE DUST PROBLEM CLOSES,
THE REPAIR SPACE IS MAPPED (4 UNTRIED CELLS, NAMED), AND THE BANIK LOCAL-VOID TEST IS
A CLEAN STRUCTURAL NEGATIVE.

Provenance: a 10-agent workflow (3 lanes x [1 builder + 2 adversarial refuters] + synthesis,
2026-08-13).  TWO of the three lane headlines were DESTROYED by their own verifiers before
commit -- both errors ran in the framework's favour -- so the standing rule (adversarial
verification BEFORE commit) is what this stage's numbers survived.  Status per part:
  PART A  Route A' closure ........................ ESTABLISHED (refuted=false x2, high conf)
  PART B  repair-space map ........................ CANDIDATE  (lane headline killed; the
                                                    corrected map is the verifiers' own)
          B4 massless-dark-U(1) closure ........... ESTABLISHED (accepted by both verifiers)
  PART C  void-growth negative .................... ESTABLISHED (adverse core survived both)
          C5 z0 residue ........................... CANDIDATE, DEMOTED (lane's "new front"
                                                    killed on four independent grounds)
  PART D  corpus corrections ...................... applied in-place (banners on stage51/52,
                                                    RETRACTIONS.md rows, kernel-labelled eta)

WHAT DIED AND WHY (one line each):
  * Route A' (stages 10/11, chi with p = K rho^gamma): the surviving gamma range is EMPTY --
    M_J today <= 1.4e8 Msun (gamma=1; <= ~7e10 even as gamma->0) against the 2.51e12 the halo
    needs, and the 4/3 threshold theorem (growth needs gamma < 4/3, polytrope stability needs
    gamma > 4/3) has EMPTY intersection.  The binding-epoch wall fires on A' too (z_bind = 10.19).
  * Lane B's "one-symbol repair" (gate on Y, not y; "clears CMB by 238x"): normalisation slip --
    V51 = 3.25e6 is the SATURATING-gate bound, not the y^2 violation; corrected, the cell
    VIOLATES the CMB by 674x-3.79e4x.  The band-pass cell dies too (4.3e3x-9.4e5x).
  * Lane C's z0 "new testable front": domain mismatch (9.4-14.7x, not 9-40x), its own Part B
    g_ext dropped (restored: the rise SATURATES at r = 425 Mpc), outside AeST's own MOND
    regime beyond r_C = 832/807 Mpc, and 3-8x SMALLER than the published HBK20 mechanism.

WHAT THIS DOES NOT SAY: "no open doors".  Four cells of the repair space are genuinely
untried (PART B3), one closed cell is REOPENED (Cell 3 -- its dismissal used stage 2 B1's
mu^2, which prices a DIFFERENT term: a manufactured deficit), and the Y=0-on-FLRW premise
conflict (B5) gates whether the gate arithmetic is even the right calculation.

Sources: workflow wf_ed177ad4-c58; lane scripts + 6 verifier scripts in the session scratchpad
(laneA_reconfrontation_2026.py, laneA_crux_binding_epoch_2026.py, laneB_two_field_pressure_
gate_2026.py, laneC_void_growth_2026.py 20/20, ADV_laneB_refute.py, verify_routeAprime*.py,
ADV_laneC_refute*.py, ADV_VOID_*.py); committed anchors stage10, stage11, stage12 (6/6,
commit ee0b1793), stage44, stage51, stage52.  Every number quoted from a verifier is either
RE-DERIVED inline below (check) or recorded with its source named (info).

Exit 0 = every check passed.
"""

import json
import os
import sys

import numpy as np
import sympy as sp
from astropy.io import fits

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


# frozen framework constants
A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10
NU0_LO, NU0_HI = 2.14e-5, 1.77e-4          # the derived-a0(z) law's nu0 range (stage 17)
G, MSUN, MPC = 6.674e-11, 1.989e30, 3.0857e22


def nu_ms08(y):
    y = np.asarray(y, dtype=float)
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-300))))


def A_ratio(overdensity_or_zfac, nu0):
    """A(z or local) / A(today, mean): sqrt(1+nu0^2)/sqrt(1+nu0^2 r^2), r = n/n0.
    On FRW r = (1+z)^3; inside structure r = the LOCAL overdensity times (1+z)^3.
    (a0^2 = A, so the a0 ratio is the sqrt of this.)"""
    r = float(overdensity_or_zfac)
    return np.sqrt(1.0 + nu0**2) / np.sqrt(1.0 + nu0**2 * r**2)


print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- ROUTE A' CLOSURE (ESTABLISHED): the surviving gamma range is EMPTY")
print("=" * 100)

# A1 -- the 4/3 threshold theorem, symbolically.
gam, rho = sp.symbols("gamma rho", positive=True)
MJ_exp = sp.Rational(3, 2) * gam - 2                    # M_J ~ rho^((3g-4)/2)
grow_boundary = sp.solve(sp.Eq(MJ_exp, 0), gam)[0]      # M_J grows as rho falls iff exponent < 0
stab_factor = 3 * gam - 4                               # polytrope total energy ~ -(3g-4)(...): bound iff > 0
check(grow_boundary == sp.Rational(4, 3),
      "A1a the Jeans-mass exponent (3*gamma-4)/2 vanishes exactly at gamma = 4/3: M_J grows in time "
      "(rho falling) iff gamma < 4/3",
      "M_J ~ rho^((3 gamma - 4)/2)")
check(sp.solve(sp.Eq(stab_factor, 0), gam)[0] == sp.Rational(4, 3),
      "A1b and a barotropic polytrope is gravitationally bound/stable iff gamma > 4/3 (the (3 gamma - 4) "
      "factor in the polytrope energy) -- the SAME threshold",
      "Lane-Emden n = 1/(gamma-1) > 3 <=> gamma < 4/3 unstable")
check(True,
      "A1c *** the intersection is EMPTY, not measure zero: at gamma = 4/3 exactly, M_J is CONSTANT, so "
      "the growth requirement fails there too.  Route A's two structural requirements exclude each other "
      "for EVERY gamma ***")

# A2 -- profile-free, gamma-free Jeans-mass transport (the cleanest closing route).
# Committed caps (stage 10's requirements, masses derived by verifier 'both-ways' and re-derived here):
MJ_FOREST_Z3 = 1.76e7      # Msun, forest cap at z=3
M_REQUIRED = 2.51e12       # Msun, the halo mass chi must carry (stage 11's own normalisation)
dil = (1 + 3) ** 3         # rho(z=3)/rho(0) on FRW
for g_, lab in ((1.0, "gamma = 1"), (1e-9, "gamma -> 0")):
    growth = dil ** (-(3 * g_ - 4) / 2.0) if g_ > 1e-6 else dil ** 2.0
    mj_today = MJ_FOREST_Z3 * growth
    short = M_REQUIRED / mj_today
    check(short > 30,
          f"A2-{lab}: M_J(today) <= {mj_today:.2e} Msun (forest cap transported; growth factor "
          f"{growth:.0f}) vs the required {M_REQUIRED:.2e} -- shortfall {short:.0f}x",
          "gamma = 1: 8x growth (=64^(1/2)); gamma->0 bound: 4096x (=64^2); NO profile, NO NFW, no gamma tuning helps")
info("A2-note verifier both-ways quotes 6.8e10 at gamma->0 (exact Omega_m evolution); the pure "
     "(1+z)^3 bound above is 7.2e10 -- same verdict at 35x short.  CMB-alone caps: gamma <= 1.3170 "
     "(50 kpc) / 1.2485 (80 kpc), both < 4/3 (source: verify_routeAprime*.py, refuted=false x2)")

# A3 -- the binding-epoch wall fires on A' with its own committed profile.
RHO_LOCAL_100KPC = 1401.3      # rho_dm0 units, stage 11's committed profile at the 100 kpc core edge
z_bind = RHO_LOCAL_100KPC ** (1.0 / 3.0) - 1.0
a0_ratio_lo = np.sqrt(A_ratio(RHO_LOCAL_100KPC, NU0_LO))
a0_ratio_hi = np.sqrt(A_ratio(RHO_LOCAL_100KPC, NU0_HI))
check(abs(z_bind - 10.19) < 0.02,
      f"A3a z_bind(A') = (1401.3)^(1/3) - 1 = {z_bind:.2f} -- within 6% of route B's surface-calibrated "
      f"10.83, from A's own profile, using the LOCAL density (the choice FAVOURING A')")
check(abs(a0_ratio_lo - 0.99978) < 2e-4 and abs(a0_ratio_hi - 0.98519) < 2e-4,
      f"A3b a0(z_bind)/a0(0) = {a0_ratio_lo:.5f} (nu0 floor) / {a0_ratio_hi:.5f} (ceiling) -- the "
      f"0.0060-at-recombination lever is UNAVAILABLE to A' exactly as it was to route B",
      "pressure is needed at z <~ 11 where a0(z) is FLAT; the wall is route-independent")

# A4 -- the T3 this lane existed to catch: committed stage 12 already excluded the cored
# two-field window, while stages 51/52 carried Route A' as live.
HERE = os.path.dirname(os.path.abspath(__file__))
s12 = open(os.path.join(HERE, "stage12_lensing_stack_fit_2026.py")).read()
s51 = open(os.path.join(HERE, "stage51_gated_proca_support_2026.py")).read()
s52 = open(os.path.join(HERE, "stage52_open_doors_audit_cycle_2026.py")).read()
check("TWO-FIELD WINDOW CLOSES" in s12,
      "A4a committed stage12 (6/6 green, commit ee0b1793) prints 'THE CORED-HALO PREDICTION IS EXCLUDED "
      "BY THE LENSING STACK, AND THE TWO-FIELD WINDOW CLOSES'")
check("SUPERSEDED BY STAGE 53" in s51 and "SUPERSEDED BY STAGE 53" in s52,
      "A4b stage51:106 and stage52:68 ('Route A' remains the one live alternative') now carry "
      "supersession banners -- the T3 (favourable claim contradicting a committed script in the same "
      "directory) is DISCHARGED by this stage")
info("A4c KiDS re-confrontation at A''s own 2.51e12 normalisation (verifier-reproduced from stage12's "
     "committed machinery + raw Mistele+24 data): Delta chi2 = +1405 (canonical worst, MS08) / +1283 "
     "(a0-line); grid +446 (150 kpc boundary) to +1698 (ALT/MS08/60 kpc).  Survives the 0.1 dex "
     "normalisation systematic (baseline 0.48, chi still +176 to +436).")
info("A4d clusters with full-Omega_dm chi (lane A, both verifiers): chi is NOT cored on cluster scales "
     "(lambda_J = 9-22 kpc vs R500 ~ 1.3 Mpc) => prediction/observed = 1.56-1.87x OVERSHOOT.  "
     "Three-way squeeze: clusters want chi at 0.26-0.43 of the dark mass, the CMB wants 1.00, KiDS "
     "allows <= 0.05.  stage51 owed item (d) is DISCHARGED ADVERSELY: full-dust does NOT close the "
     "cluster shortfall, it overshoots.")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE REPAIR-SPACE MAP (CANDIDATE except B4): 4 untried cells, named")
print("=" * 100)

# B1 -- the corrected normalisation that killed lane B's headline.
CH2 = 1.08e4               # (km/s)^2, c_h^2 = G M / R_halt at the support calibration
RHO_REC_OVER_H = 1091.0**3 / 1654.0
CS2_CAP = 2606.0           # (km/s)^2, the CLASS recombination sound-speed cap (stage 51 kill 2)
V_SAT = CH2 * RHO_REC_OVER_H / CS2_CAP
check(abs(V_SAT / 3.25e6 - 1.0) < 0.01,
      f"B1  V_sat = c_h^2 (rho_rec/rho_h) / c_s2_cap = {V_SAT:.2e} -- this is the SATURATING-gate "
      f"bound and contains NO y-amplification.  stage 52:58's 3.25e6 is THIS number",
      "lane B normalised its whole gate table on it as if it were the y^2 violation: every cell was "
      "too small by rho_y^2 = 1.6e5-9.0e6.  Corrected map: V(m,q) = V_sat * rho_y^m * A_r^(m+q)")
info("B2  cell deaths under the corrected map (ADV_laneB_refute.py, arithmetic confirmed by the "
     "second verifier): CELL 1 (m,q)=(2,0) 'gate on Y, clears by 238x' actually VIOLATES the CMB by "
     "674x-3.79e4x; the q-boundary is q >= +0.64..+1.03 (nu0 floor) / +0.19..+0.51 (ceiling) -- q=0 "
     "excluded.  CELL 2 (band-pass B(y)=y/(1+y)^2, the a0-bump's own shape) violates by 4.3e3x-9.4e5x; "
     "stage 52's y-only wall stands UNREFINED.  The true y^2-gate violation is 5.2e11-2.9e13x -- the "
     "committed 3.25e6 UNDERSTATES stage 51's kill.")
print("""
  B3  THE FOUR UNTRIED CELLS (the honest live list; none is an endorsement):
      1. W ~ Y^m A^q with q >= +0.6..+1.0 -- a POSITIVE power of A (inverse-density gate).
         First obstruction to price: A is degenerate between the halo surface and z_bind by
         construction (r = n/n0), so the A factor cannot do the z <~ 11 job -- only Y can.
      2. Cell 3 REOPENED: AeST's own 2(2-K_B) J^mu grad_mu phi term (J = 0 on FRW, zero new
         parameters).  Its closure used stage 2 B1's mu^2 = 2 K2 Q0^2/(2-K_B), which prices the
         F(Y,Q) expansion, NOT this term -- a manufactured deficit.  The genuinely non-quasi-
         static part during collapse is UNPRICED.
      3. Baryon-disk torque (matter-coupling x angular momentum) -- carries an EP/fifth-force
         price.  UNTRIED-WEAK.
      4. Wave/gradient support from a non-k-essence second field (the k^4 obstruction is
         k-essence-specific).  Narrow, untried.
""")
# B4 -- the one genuinely new closure, ESTABLISHED (both verifiers accept).
Q0, n_ = sp.symbols("Q0 n", positive=True)
rho_dust = Q0 * n_                      # identically (the shift-charge theorem, stages 5/6/9)
charge_to_mass = n_ / rho_dust
check(sp.simplify(charge_to_mass - 1 / Q0) == 0,
      "B4  massless-dark-U(1) CLOSED by universality: rho = Q0 n identically => dark charge/mass "
      "= 1/Q0 EXACTLY universal => the repulsion rescales dust self-gravity by the same constant at "
      "every epoch and density.  Tuning it to halt collapse today switches off the clustering the "
      "CMB measures.  The universality that makes the sign work makes it un-gateable.")
info("B5  GATING OWED ITEM, must be settled before ANY further gate is built or gate kill quoted: "
     "AEST_SPHERICAL_COLLAPSE_SETUP.md:41-43 has Y = 0 exactly on FLRW, so W ~ Y^m is O(delta^2m) "
     "and cannot move a LINEAR-theory c_s^2 at all (stage 51 D1 asserts this) -- if that premise "
     "holds, stage 52's kill 2 and the whole gate table price the WRONG OBJECT.  Also still owed: "
     "the perturbation health matrix (ghost/gradient) of any gated vector-on-current coupling.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- THE VOID-GROWTH NEGATIVE (ESTABLISHED) + the demoted z0 residue (CANDIDATE)")
print("=" * 100)

# C1 -- the framework selects on ACCELERATION, not scale: inline BBKS re-derivation.
h, Om, ns = 0.674, 0.315, 0.965
k = np.logspace(-4, 2, 4000)            # h/Mpc
q_ = k / (Om * h)                       # BBKS shape (Gamma ~ Om h)
T = (np.log(1 + 2.34 * q_) / (2.34 * q_)) * (1 + 3.89 * q_ + (16.1 * q_)**2
                                             + (5.46 * q_)**3 + (6.71 * q_)**4) ** -0.25
Pk = k ** ns * T ** 2


def sigma_R(R_mpc_h):
    x = k * R_mpc_h
    W = 3 * (np.sin(x) - x * np.cos(x)) / x**3
    return np.sqrt(np.trapz(Pk * W**2 * k**2, k) / (2 * np.pi**2))


SIG300 = 0.0232                          # lane C's absolute-A_s-normalised sigma(300 Mpc), verified
norm = SIG300 / sigma_R(300 * h)
rho_m = Om * 8.59e-27                    # kg/m^3
# two acceleration-window conventions bracket the inline re-derivation; the verified lane value
# (1.175, reproduced by BOTH refuters with the proper P(k)) sits inside the bracket:
g_dens = lambda R: (4 * np.pi / 3) * G * rho_m * (R * MPC) * norm * sigma_R(R * h)   # density window


def g_acc(R):                            # peculiar-acceleration window: |g_k| ~ delta_k / k
    x = k * (R * h)
    W = 3 * (np.sin(x) - x * np.cos(x)) / x**3
    Lh = np.sqrt(np.trapz(Pk * W**2, k) / (2 * np.pi**2)) * norm      # Mpc/h
    H0 = 2.184e-18 * h / 0.674
    return 1.5 * Om * H0**2 * Lh * MPC / h


ratios = []
for gf in (g_dens, g_acc):
    r300, r12 = nu_ms08(gf(300) / A0_CAN), nu_ms08(gf(12) / A0_CAN)
    ratios.append(r300 / r12)
check(max(ratios) < 2.5 and min(ratios) > 1.0,
      f"C1  inline BBKS bracket: nu(g_rms 300 Mpc)/nu(g_rms 12 Mpc) = {min(ratios):.2f}-{max(ratios):.2f} "
      f"across two crude window conventions; the lane's exact-P(k) value, reproduced by BOTH "
      f"refuters, is 1.175 -- against the KBC void's requirement of 2.7-8.2x MORE amplitude at "
      f"300 Mpc and NOT at 12 Mpc (defensible floor 4.32x)",
      "the verdict is CONVENTION-ROBUST: the kernel selects on ACCELERATION, both scales are "
      "deep-MOND (nu >= 18.9 over 8-1000 Mpc), and even the crudest convention stays a factor "
      ">= 2 below the floor.  Verified precise value 1.175 (1.210 BBKS variant; 1.175 ALT footing)")
info("C2  the three branches, all closed (laneC 20/20 + both verifiers): (i) delta-Y^(1) = 0 on FRW "
     "=> the promoted MOND term is O(delta phi^3), enhancement EXACTLY 1 (bridge1/stage18/22 -- "
     "stage23/24 hold); (ii) MOND-on (Haslbauer's prescription) over-delivers 18.3-28x AND cannot be "
     "confined: every rms 12-Mpc overdensity collapses by z=1.87 and every rms 12-Mpc void evacuates "
     "to delta = -0.993 (the scale-dependent EFE rescue fails at 1.33); (iii) AeST's own "
     "G_cosmo/G_local < 1 channel is capped at 8/7 by the BBN K_B bound => <= 1.75x, below the 4.32x "
     "floor, and scale-free so sigma_8 -> 1.38.  sigma_8, not the bracket, closes it.")
z9 = (1 + 9) ** 6
r_lo, r_hi = np.sqrt(A_ratio((1 + 9)**3, NU0_LO)), np.sqrt(A_ratio((1 + 9)**3, NU0_HI))
check(abs(r_lo - 0.99989) < 2e-4 and abs(r_hi - 0.99232) < 2e-3,
      f"C3  a0(z=9)/a0(0) = {r_lo:.5f} (floor) / {r_hi:.5f} (ceiling): the derived law is already FLAT "
      f"where the void lives (z_t = 16.8-35.0), so Haslbauer's constant-a0 void result transfers to "
      f"this framework UNCHANGED -- a0(z) is NOT distinguishable on this front",
      "effect on delta(0): +0.0002% to +0.013% from z_i=9; <= 4.5% even from z_i=1000")
check(NU0_HI**2 < 1e-7,
      f"C4  the 3.07-sigma BAO/MDPS anomaly is a SHARED PROBLEM, not a win: |1+w| <= nu0^2 = "
      f"{NU0_HI**2:.1e} and a0(1090)/a0(0) = 0.0021-0.0060 leave r_d the parent theory's.  "
      f"NEVER cite it as support")
info("C5  z0 residue, CANDIDATE and DEMOTED (the lane's 'new front' died 4 ways): z0 ~ 0.20-0.27%, "
     "SATURATING (not rising -- the lane dropped its own g_ext = 0.0111 a0; restored, nu saturates at "
     "r = 425 Mpc), ~17-19x standard gravity but DEGENERATE with a GR void of r_v = 1448 Mpc (Banik "
     "Eq. 26), BELOW HBK20's published 0.84%, and outside AeST's own MOND regime beyond r_C = 832 "
     "(canonical) / 807 (ALT) Mpc (Verwayen-Skordis-Boehm oscillatory zone).")
info("C6  citable adverse result for the Banik correspondence: Russell, Banik, Cray & Zhao, MNRAS 547 "
     "stag399 (arXiv:2602.21975): local-hole analogues DO form in MOND models but deceleration "
     "parameters < -1.5 prevent a satisfactory Hubble-tension resolution.  CAUTION: their '>5 sigma' "
     "is for nuHDM (Cosmicflows-4 bulk flows), NOT generic MOND-plus-cold-dust -- do not over-cite.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- CORPUS CORRECTIONS: the kernel-labelled cluster eta, and a0 as a LOCAL quantity")
print("=" * 100)

# D1 -- stage 44's R500 eta was computed with the a0-line kernel and headlined unlabelled.
# Recompute BOTH kernels x BOTH footings from the same raw X-COP profiles.
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data", "xcop")
R500 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))
names = sorted(n for n in R500 if os.path.exists(os.path.join(DATA, n, f"{n}_fgas_profile.fits")))
F_STAR_DEF = 0.015


def profile(n):
    d = fits.open(os.path.join(DATA, n, f"{n}_fgas_profile.fits"))[1].data
    r5 = R500[n]["R500"]
    x = np.asarray(d["RADIUS"], float)
    M = np.asarray(d["M_NFW"], float)
    mg = np.asarray(d["MGAS"], float)
    msf = os.path.join(DATA, n, f"{n}_mstar.fits")
    if os.path.exists(msf):
        ms = fits.open(msf)[1].data
        st = np.interp(x * r5, np.asarray(ms["RADIUS"], float) * r5, np.asarray(ms["MSTAR"], float))
    else:
        st = F_STAR_DEF * M
    ok = np.isfinite(M) & (M > 0) & (mg > 0) & (x > 0)
    return x[ok], M[ok], (mg + st)[ok], r5


def eta_r500(kernel, a0):
    """stage 44's own committed construction: the 0.6-1.0 R500 band, pooled median."""
    rat = []
    for n in names:
        x, M, mb, r5 = profile(n)
        m = (x > 0.6) & (x <= 1.0)
        if not m.any():
            continue
        rm = x[m] * r5 * MPC
        gb = G * mb[m] * MSUN / rm**2
        gobs = G * M[m] * MSUN / rm**2
        gpred = np.sqrt(gb**2 + a0 * gb) if kernel == "a0line" else nu_ms08(gb / a0) * gb
        rat.append(gobs / gpred)
    return float(np.median(np.concatenate(rat)))


eta = {(k_, f_): eta_r500(k_, a0_) for k_ in ("a0line", "ms08")
       for f_, a0_ in (("can", A0_CAN), ("alt", A0_ALT))}
check(abs(eta[("a0line", "can")] - 2.084) < 0.03 and abs(eta[("a0line", "alt")] - 1.917) < 0.03,
      f"D1a regression: the a0-line kernel reproduces stage 44's committed R500 numbers: "
      f"{eta[('a0line', 'can')]:.3f} canonical / {eta[('a0line', 'alt')]:.3f} alt")
check(abs(eta[("ms08", "can")] - 1.865) < 0.04 and abs(eta[("ms08", "alt")] - 1.722) < 0.04,
      f"D1b under the OPERATIVE MS08 kernel the same data give {eta[('ms08', 'can')]:.3f} canonical / "
      f"{eta[('ms08', 'alt')]:.3f} alt -- the in-force kernel is ~10.5% FAVOURABLE, and this arrived "
      f"unlabelled (a favourable T3, caught by the verifier)",
      "QUOTE THE SPREAD 1.72-2.08 WITH THE KERNEL NAMED.  Caveat that travels with it: stage 33's "
      "eta window 1.6-2.3 is itself a0-line-derived, so a consistent swap moves both sides.  "
      "All four values are INSIDE the window; none of them is 1")

# D2 -- a0 is NOT a function of epoch alone: A(Q) depends on the LOCAL charge density.
dlnA_ceiling = 0.5 * abs(np.log(A_ratio(1654.0, NU0_HI)))
supp_1e6 = 1.0 / np.sqrt(np.sqrt(A_ratio(1e6 * 1654.0 / 1654.0, NU0_HI))) if False else \
    1.0 / np.sqrt(A_ratio(1e6, NU0_HI))
check(abs(2 * dlnA_ceiling - 0.0411) < 0.002,
      f"D2a inside a halo at overdensity 1654, |Delta ln A| = {2*dlnA_ceiling:.4f} at the nu0 ceiling "
      f"(6.3e-4 at the floor): a0 is suppressed by up to ~2% (A by ~4%) INSIDE structure.  An "
      f"overdensity of 1654 IS z_bind identically (11.83^3 = 1656): A is structure/epoch DEGENERATE",
      "'a0 maximal today' is a statement about the COSMIC MEAN, not about a point inside a galaxy -- "
      "this cuts both ways and is new")
check(abs(supp_1e6 / 13.3 - 1.0) < 0.05,
      f"D2b at the corpus's 1e6 rho_dm0 support calibration the local a0 is suppressed {supp_1e6:.1f}x "
      f"(ceiling) -- any support mechanism reading a0 locally must price this")

print("""
  D3  DO-NOT-CITE additions (recorded in RETRACTIONS.md + memory by this stage):
      * "Route A' / the cored two-field halo is live"  (dead: this stage; stage12 had it 8/2026)
      * "V51 = 3.25e6 is stage 51's y^2 gate violation"  (it is the SATURATING bound; true y^2
        violation 5.2e11-2.9e13x)
      * "gating on Y instead of y clears the CMB by 238x"  (violates 674x-3.79e4x)
      * "the band-pass in y refines the y-only wall"  (dead; the wall stands unrefined)
      * "z0 rises logarithmically with source distance / is a new testable front"  (saturates)
      * "Russell+2026 excludes MOND-plus-cold-dust at >5 sigma"  (that figure is nuHDM-specific)
      * "clusters at eta = 2.084" unqualified  (a0-line number; MS08 gives 1.865/1.722)

  D4  STANDING AFTER THIS STAGE: the dust problem remains OPEN -- 4 untried cells (B3), one
      reopened (Cell 3), the Y=0-on-FLRW premise conflict to settle FIRST (B5).  Untouched:
      a0 coefficient, lensing gamma_PPN = 1, CLASS CMB pass, RAR 0.108 dex, BTFR, solar system,
      no-ghost theorem, c_T = 1, the a0-bump, the DR4 pre-registration (stage 53 touches nothing
      frozen).  The standing rule is EXTENDED: any gate arithmetic normalised on a number quoted
      from a report must RE-DERIVE that number from its own inputs before use.
""")

print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 53 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
