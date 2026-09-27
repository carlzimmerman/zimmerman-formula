#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
kappa_h0_convention_audit_2026.py
=================================
AUDIT: do the corpus's two committed kappa determinations handle the H0 convention consistently?

kappa is DEFINED as   kappa = a_0 / (c sqrt(G rho_Lambda)).
  * the DENOMINATOR is built from Planck's H0 (67.36-67.39 km/s/Mpc, Omega_L = 0.685);
  * the NUMERATOR is measured on SPARC, whose Hubble-flow distances assume H0 = 73 km/s/Mpc
    (master-table Note 2, distance method f_D = 1 -- 97 of 175 galaxies).
So one calculation carries TWO different values of the same parameter.  kappa_gas_dominated_2026.py
PART F (check F4) flagged this today and left the audit of the COMMITTED numbers owed.  This is it.

THE TWO COMMITTED NUMBERS AUDITED
  kappa = 0.551 +/- 0.043  "distance-free"  -- real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py
  kappa = 0.465 +/- 0.076  BTFR intercept   -- real_research/reviews/mi_btfr_intercept_kappa_door_2026.py

HEADLINE, AND IT IS NOT WHAT TODAY'S FLAG SAID
  1. The BTFR number IS exposed, but far LESS than the flagged ~8%: its Hubble-flow WEIGHT fraction is
     0.202 (not the 0.583 count fraction), so the Planck-consistent correction is only -3.2%
     (0.465 -> 0.450).  Its budget already carries a 5.07% "distance scale (H0=73/TRGB zp)" term, so the
     WIDTH is honestly charged; only the OFFSET was never applied.  Direction: AWAY from 1/2 (ADVERSE).
  2. *** The distance-free number is NOT clean, and its exposure is BIGGER than the BTFR's, not smaller.
     Its immunity theorem covers a COMMON distance rescaling.  The H0 convention is not common -- it moves
     ONLY the 97 Hubble-flow galaxies, and those sit preferentially at the NEWTONIAN end of the RAR
     (median g_bar = 0.33 a_0 vs 0.18 a_0), which is exactly the lever the shape-only estimator uses.
     Re-running it with Planck-consistent Hubble-flow distances moves a_0 by +7.3% / +6.5% (Ups = 0.5/0.7),
     six times its 1.15% statistical error and comparable to its ENTIRE 7.77% quoted budget.  Direction:
     AWAY from 1/2 (0.551 -> 0.591, 1.20 sigma -> 1.98 sigma).  ADVERSE. ***
  3. So today's PART F direction claim -- "the committed 0.551 may be biased high by ~8%" -- is NOT
     supported.  For the shape-only estimator the numerator responds with the OPPOSITE sign to the naive
     a_0 ~ D^-2 argument, and the committed value sits INSIDE the self-consistent range [0.492, 0.591]
     rather than at its top.  What IS wrong with 0.551 +/- 0.043 is the ERROR BAR: it charges 0% for the
     distance/H0 scale on the strength of a theorem that does not cover the operation.
  4. STRUCTURAL: kappa ~ h^(2 q_eff - p), so kappa is H0-invariant ONLY IF q_eff = p/2.  Neither
     estimator is there (q_eff = +0.202 BTFR, -0.414 distance-free; p = 1 or 1/Omega_L = 1.46).  There is
     no cancellation available in principle -- kappa carries an irreducible H0-convention dependence and
     must be quoted WITH the H0 it was computed at.

WHAT IS ASSUMED, LABELLED
  * SPARC's f_D = 1 distances are exactly D = v_flow(Virgo-corrected)/H0, so rescaling H0 rescales them
    linearly and exactly.  The Virgo-infall model is held fixed.  (Master-table Note 2.)
  * TRGB / Cepheid / UMa / SN distances (f_D = 2,3,4,5) are treated as H0-INDEPENDENT.  For f_D = 4
    (Ursa Major, 28 galaxies) that is only approximately true -- the UMa distance is itself tied to a
    ladder -- so the exposure computed here is a LOWER bound.  Named, not hidden.
  * "Planck-consistent" (R1) keeps rho_Lambda and rescales the flow distances.  "Local-consistent" (R2)
    keeps SPARC's distances and rebuilds rho_Lambda at H0 = 73.  Both are self-consistent; they disagree
    because kappa genuinely depends on H0.  R1 is designated OPERATIVE because the framework's REGISTERED
    a_0 = 9.3619e-11 is Planck-footed: R2 would move the framework's own prediction to 1.014-1.048e-10
    and every a_0-dependent result in the corpus with it.
  * No claim here about which H0 is right.  The H0 tension is unresolved; the honest output is a RANGE.

Run: python3 real_research/reviews/kappa_h0_convention_audit_2026.py    (exit 0 iff every check holds)
"""
from __future__ import annotations

import glob
import math
import os
import re
import sys
from collections import Counter

import numpy as np
import sympy as sp
from scipy.optimize import minimize

# ----------------------------------------------------------------------------------- check harness
FAIL: list[str] = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def banner(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # .../real_research
MRT = os.path.join(HERE, "data", "SPARC_Lelli2016c.mrt")
ROTMOD = sorted(glob.glob(os.path.join(HERE, "data", "sparc_data", "*_rotmod.dat")))

# ------------------------------------------------------------------- the framework's own constants
C_L, G_N = 2.998e8, 6.674e-11
MPC = 3.0856775814913673e22
KPC_M = 3.0857e19                       # as used by the BTFR script
K_UNIT = 3.2408e-14                     # (km/s)^2/kpc -> m/s^2, as used by the distance-free script
MSUN = 1.989e30

H0_PLANCK_KMS = 67.36                   # Planck 2018 TT,TE,EE+lowE+lensing
OM_L_PLANCK = 0.6847
OM_M_H2 = 0.1430                        # omega_m = Omega_m h^2, what the CMB actually measures
H0_SPARC_KMS = 73.0                     # SPARC master-table Note 2 (asserted here, PARSED in A1)

A0_CANON_REG = 9.3619e-11               # the framework's REGISTERED canonical a_0
A0_ALT_REG = 1.1279e-10                 # the alt footing (rho_total / cH0)
DEN_DF = 1.87094e-10                    # hard-coded denominator in mi_distance_free_gbar_estimator_sparc
DEN_ALT_DF = DEN_DF * (A0_ALT_REG / A0_CANON_REG)

# the BTFR script's denominator, rebuilt from its own imported module constants
H0_KERNEL, OM_L_KERNEL = 2.184e-18, 0.685
RHO_L_KERNEL = OM_L_KERNEL * 3 * H0_KERNEL ** 2 / (8 * math.pi * G_N)
A0_CANON_KERNEL = (C_L / 2) * math.sqrt(G_N * RHO_L_KERNEL)
DEN_BT = 2.0 * A0_CANON_KERNEL

K_DF_PUB, S_DF_PUB = 0.551, 0.043
K_BT_PUB, S_BT_PUB = 0.465, 0.076
A0_BT_PUB = 8.7091e-11

F_R1 = H0_SPARC_KMS / H0_PLANCK_KMS     # Hubble-flow distances grow by this under R1

print(__doc__)


def den_of_h(h_kms, mode="fixed_OmL"):
    """c sqrt(G rho_Lambda) as a function of H0, on the canonical (rho_DE) footing.

    mode 'fixed_OmL' : Omega_Lambda held at Planck's 0.6847  -> rho_L ~ h^2   -> DEN ~ h^1
    mode 'fixed_wm'  : omega_m = Omega_m h^2 held at 0.1430  -> rho_L ~ h^2 - omega_m -> DEN ~ h^(1/Om_L)
    """
    h = h_kms * 1e3 / MPC
    rho_c = 3 * h ** 2 / (8 * math.pi * G_N)
    if mode == "fixed_OmL":
        om_l = OM_L_PLANCK
    else:
        om_l = 1.0 - OM_M_H2 / (h_kms / 100.0) ** 2
    return C_L * math.sqrt(G_N * om_l * rho_c), om_l


def den_alt_of_h(h_kms):
    """the ALT footing: c sqrt(G rho_total) = c H0 sqrt(3/8pi).  No Omega_Lambda -> exponent 1 exactly."""
    h = h_kms * 1e3 / MPC
    return C_L * h * math.sqrt(3.0 / (8.0 * math.pi))


# =================================================================================================
banner("PART A -- PROVENANCE: which H0 sits where, parsed rather than asserted")

note2 = ""
nrow = 0
TBL: dict[str, dict] = {}
for ln in open(MRT):
    if "Hubble-Flow" in ln:
        note2 = ln.strip()
    t = ln.split()
    if len(t) != 19:
        continue
    try:
        TBL[t[0]] = dict(D=float(t[2]), eD=float(t[3]), fD=int(t[4]), inc=float(t[5]), einc=float(t[6]),
                         L36=float(t[7]), Rd=float(t[11]), MHI=float(t[13]), Vf=float(t[15]),
                         eVf=float(t[16]), Qf=int(t[17]))
        nrow += 1
    except ValueError:
        continue
hist = Counter(v["fD"] for v in TBL.values())
m73 = re.search(r"H0\s*=\s*([\d.]+)\s*km/s/Mpc", note2)
print(f"\n   master-table Note 2, verbatim: {note2}")
print(f"   f_D histogram over {nrow} rows: " + "  ".join(f"{k}:{hist[k]}" for k in sorted(hist)))
check(nrow == 175 and m73 is not None and abs(float(m73.group(1)) - 73.0) < 1e-9 and hist[1] == 97,
      "A1  SPARC's Hubble-flow distances DO assume H0 = 73 km/s/Mpc, parsed from the master table, and "
      f"{hist[1]} of {nrow} galaxies ({100*hist[1]/nrow:.0f}%) use that method (f_D = 1)",
      f"the other {nrow-hist[1]} use TRGB (45), Ursa Major (28), Cepheids (3), SNe (2) -- treated here as "
      "H0-independent, which for the 28 Ursa Major objects is only approximate (LOWER bound on exposure)")

den_p, _ = den_of_h(H0_PLANCK_KMS, "fixed_OmL")
r_df = den_p / DEN_DF
r_bt = den_p / DEN_BT
print(f"\n   c sqrt(G rho_L) rebuilt at (H0, Om_L) = ({H0_PLANCK_KMS}, {OM_L_PLANCK}) : {den_p:.5e}")
print(f"   distance-free script's hard-coded denominator            : {DEN_DF:.5e}  (ratio {r_df:.5f})")
print(f"   BTFR script's denominator = 2 x A0_CANON (mi_route_a_kernel): {DEN_BT:.5e}  (ratio {r_bt:.5f})")
check(abs(r_df - 1) < 2e-3 and abs(r_bt - 1) < 2e-3,
      "A2  BOTH committed determinations divide by a PLANCK-H0 quantity -- the denominators reproduce "
      f"c sqrt(G rho_Lambda) at H0 ~ 67.4 to {100*abs(r_df-1):.3f}% and {100*abs(r_bt-1):.3f}%",
      "so the mismatch is real and structural: numerator at H0 = 73, denominator at H0 = 67.4")

check(abs(DEN_BT / DEN_DF - 1) < 5e-3,
      f"A3  HYGIENE (labelled, not physics): the two committed denominators differ from each other by "
      f"{100*abs(DEN_BT/DEN_DF-1):.3f}% -- 1.87094e-10 hard-coded vs 1.87250e-10 rebuilt from H0 = 67.39, "
      "Om_L = 0.685.  The two kappas are therefore on very slightly different footings",
      "negligible against every error bar here, but it should be one constant in one place")

alt_strict = den_alt_of_h(H0_PLANCK_KMS)
check(abs(alt_strict / DEN_ALT_DF - 1) < 0.01,
      f"A4  the ALT footing denominator is c H0 sqrt(3/8pi) = {alt_strict:.5e} against the corpus's "
      f"{DEN_ALT_DF:.5e} ({100*abs(alt_strict/DEN_ALT_DF-1):.2f}%); it carries NO Omega_Lambda, so on the "
      "alt footing the H0 exponent is EXACTLY 1 and there is no omega_m sub-fork",
      "useful: the alt footing is the cleaner one for this particular question")


# =================================================================================================
banner("PART B -- THE SCALING ALGEBRA: where H0 enters, and why nothing cancels")

D_s, F_s, th_s, v_s, G_s = sp.symbols("D F theta v G", positive=True)
g_bar_sym = sp.simplify(G_s * (F_s * D_s ** 2) / (th_s * D_s) ** 2)
g_obs_sym = sp.simplify(v_s ** 2 / (th_s * D_s))
a0_btfr_sym = sp.simplify(v_s ** 4 / (G_s * F_s * D_s ** 2))
check(D_s not in g_bar_sym.free_symbols and D_s in g_obs_sym.free_symbols
      and sp.simplify(sp.diff(sp.log(a0_btfr_sym), sp.log(D_s)) if False else
                      sp.simplify(D_s * sp.diff(a0_btfr_sym, D_s) / a0_btfr_sym)) == -2,
      f"B1  the two axes, symbolically: g_bar = {g_bar_sym} is DISTANCE-FREE, g_obs = {g_obs_sym} ~ 1/D, "
      f"and the BTFR estimator V^4/(G M_bar) ~ D^-2 exactly (d ln a0/d ln D = -2)",
      "so the BTFR intercept inherits the distance scale twice over, the g_bar axis not at all")

h_s, wm_s, oml_s = sp.symbols("h omega_m Omega_L", positive=True)
rho_fixed_oml = oml_s * h_s ** 2
rho_fixed_wm = h_s ** 2 - wm_s
e_fixed_oml = sp.simplify(h_s * sp.diff(sp.sqrt(rho_fixed_oml), h_s) / sp.sqrt(rho_fixed_oml))
e_fixed_wm = sp.simplify(h_s * sp.diff(sp.sqrt(rho_fixed_wm), h_s) / sp.sqrt(rho_fixed_wm))
e_wm_num = float(e_fixed_wm.subs({h_s: H0_PLANCK_KMS / 100.0, wm_s: OM_M_H2}))
P_OML, P_WM = 1.0, e_wm_num
check(e_fixed_oml == 1 and abs(P_WM - 1.0 / OM_L_PLANCK) < 5e-3,
      f"B2  the DENOMINATOR exponent p = d ln[c sqrt(G rho_L)]/d ln h is p = {e_fixed_oml} at fixed "
      f"Omega_Lambda, but p = {P_WM:.4f} = 1/Omega_Lambda at fixed omega_m = Omega_m h^2 (derived: "
      f"{sp.simplify(e_fixed_wm)}), because rho_L ~ h^2 - omega_m",
      "the CMB measures omega_m, not Omega_Lambda, so p = 1.46 is the more faithful fork; both carried")

q_s, p_s = sp.symbols("q p", real=True)
kappa_exp = 2 * q_s - p_s
q_inv = sp.solve(sp.Eq(kappa_exp, 0), q_s)[0]
check(q_inv == p_s / 2,
      f"B3  *** kappa ~ h^(2 q_eff - p) with q_eff := (1/2) d ln a0/d ln h.  kappa is H0-INVARIANT if and "
      f"only if q_eff = p/2 = {float(P_OML/2):.3f} (fixed Om_L) or {P_WM/2:.3f} (fixed omega_m).  PART C and "
      "PART D measure q_eff for the two committed estimators; neither is at the invariant point, so kappa "
      "carries an IRREDUCIBLE H0-convention dependence and must always be quoted with its H0 ***",
      "this is a structural statement about the definition of kappa, not about either script")


# =================================================================================================
banner("PART C -- THE BTFR DETERMINATION (kappa = 0.465 +/- 0.076): reproduced, then corrected")

UD_FID, UB_OVER_UD, HE_FID = 0.70, 1.4, 1.33
SIG_UPS_RAND, SIG_GAS_RAND = 0.230, 0.050
Y_CUT = 0.05                       # the committed script's quadrature-optimal rung of its frozen ladder


def nu_kernel(y):
    """the in-force Route A kernel nu(y) = 1/(1 - e^-sqrt(y))."""
    return 1.0 / -np.expm1(-np.sqrt(np.asarray(y, float)))


def Qy(y):
    y = np.asarray(y, float)
    return nu_kernel(y) ** 2 * y


def btfr_sample(fscale_hf=1.0):
    """rebuild the committed BTFR deep sample.  fscale_hf multiplies the DISTANCE of every f_D = 1 galaxy;
    R ~ D, V_bar^2 ~ D, L ~ D^2 and M_HI ~ D^2 are all propagated, so g_bar, y_out and Gamma stay invariant
    by construction and only M_bar moves -- which is the whole content of the H0 operation."""
    out = []
    for fn in ROTMOD:
        nm = os.path.basename(fn).replace("_rotmod.dat", "")
        if nm not in TBL:
            continue
        T = TBL[nm]
        if T["Qf"] > 2 or T["inc"] < 30.0 or T["Vf"] <= 0.0:
            continue
        d = np.genfromtxt(fn, comments="#")
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        m = (R > 0) & (Vo > 0)
        R, Vo, eV, Vg, Vd, Vb = R[m], Vo[m], eV[m], Vg[m], Vd[m], Vb[m]
        if len(R) < 4:
            continue
        f = fscale_hf if T["fD"] == 1 else 1.0
        R = R * f                                       # R = theta D
        Vg, Vd, Vb = Vg * math.sqrt(f), Vd * math.sqrt(f), Vb * math.sqrt(f)   # V_bar^2 ~ GM/R ~ D
        L36, MHI, Rd = T["L36"] * f ** 2, T["MHI"] * f ** 2, T["Rd"] * f
        V2 = np.sign(Vg) * Vg ** 2 + UD_FID * Vd ** 2 + UB_OVER_UD * UD_FID * Vb ** 2
        if V2[-1] <= 0:
            continue
        k = max(3, int(math.ceil(0.3 * len(R))))
        slope = float(np.polyfit(np.log(R[-k:]), np.log(Vo[-k:]), 1)[0])
        if abs(slope) >= 0.15 or R[-1] / max(Rd, 1e-9) <= 2.0:
            continue
        gbl = V2[-1] * 1e6 / (R[-1] * KPC_M)
        Mst, Mgs = UD_FID * L36 * 1e9, HE_FID * MHI * 1e9
        if Mst + Mgs <= 0:
            continue
        Mb = (Mst + Mgs) * MSUN
        fst = Mst / (Mst + Mgs)
        inc = math.radians(T["inc"])
        sig = math.sqrt((4.0 * T["eVf"] / T["Vf"]) ** 2
                        + (4.0 * math.radians(T["einc"]) / math.tan(inc)) ** 2
                        + (2.0 * T["eD"] / T["D"]) ** 2
                        + (fst * SIG_UPS_RAND) ** 2 + ((1.0 - fst) * SIG_GAS_RAND) ** 2)
        out.append(dict(nm=nm, gbl=gbl, Gam=gbl * (R[-1] * KPC_M) ** 2 / (G_N * Mb), Mb=Mb,
                        Vf=T["Vf"], fD=T["fD"], w=1.0 / sig ** 2))
    return out


def btfr_a0(sample):
    y = np.array([g["gbl"] / A0_CANON_KERNEL for g in sample])
    keep = y < Y_CUT
    sub = [g for g, k in zip(sample, keep) if k]
    yy = y[keep]
    lna = np.array([4.0 * math.log(g["Vf"] * 1e3) - math.log(G_N * g["Mb"]) for g in sub])
    lna = lna - np.log(np.asarray(Qy(yy)) * np.array([g["Gam"] for g in sub]))
    w = np.array([g["w"] for g in sub])
    a0 = math.exp(float(np.sum(w * lna) / np.sum(w)))
    qhf = float(np.sum(w * np.array([1.0 if g["fD"] == 1 else 0.0 for g in sub])) / np.sum(w))
    neff = float(w.sum() ** 2 / (w ** 2).sum())
    return a0, qhf, neff, sub, w


S0 = btfr_sample(1.0)
a0_bt, qhf, neff_bt, sub0, w0 = btfr_a0(S0)
nhf = sum(1 for g in sub0 if g["fD"] == 1)
k_bt = a0_bt / DEN_BT
print(f"\n   deep sample at y_cut = {Y_CUT}: N = {len(sub0)}, N_eff = {neff_bt:.1f}")
print(f"   a0_hat = {a0_bt:.5e} = {a0_bt/A0_CANON_KERNEL:.4f}x canonical   ->  kappa = {k_bt:.4f}")
print(f"   Hubble-flow objects: {nhf}/{len(sub0)} by COUNT = {nhf/len(sub0):.3f}, "
      f"but only {qhf:.3f} by WEIGHT")
check(abs(a0_bt / A0_BT_PUB - 1) < 0.01 and abs(k_bt - K_BT_PUB) < 0.005 and len(sub0) == 24,
      f"C1  the committed BTFR pipeline is REPRODUCED independently here: a0_hat = {a0_bt:.4e} vs the "
      f"published {A0_BT_PUB:.4e} ({100*abs(a0_bt/A0_BT_PUB-1):.2f}%), kappa = {k_bt:.4f} vs {K_BT_PUB}, "
      f"N = {len(sub0)}, N_eff = {neff_bt:.1f}",
      "so the correction below is applied to the real committed estimator, not to a lookalike")

check(abs(qhf - 0.202) < 0.01 and qhf < 0.5 * nhf / len(sub0),
      f"C2  *** THE EXPOSURE IS THE WEIGHT FRACTION, NOT THE COUNT: q_HF = {qhf:.3f}, against "
      f"{nhf/len(sub0):.3f} by count -- a factor {(nhf/len(sub0))/qhf:.2f} smaller, because the Hubble-flow "
      f"galaxies have the worst e_D/D and are down-weighted.  q_eff = +{qhf:.3f} ***",
      "the naive '8% because a0 ~ H0^2 / H0 ~ H0' assumes q_eff = 1; the committed estimator is at 0.20")

S1 = btfr_sample(F_R1)
a0_bt_r1, qhf1, _, sub1, _ = btfr_a0(S1)
pred = a0_bt * (1.0 / F_R1) ** (2.0 * qhf)
same_sample = [g["nm"] for g in sub0] == [g["nm"] for g in sub1]
print(f"\n   R1 (Planck-consistent: f_D = 1 distances x {F_R1:.5f}):")
print(f"     a0_hat -> {a0_bt_r1:.5e} ({100*(a0_bt_r1/a0_bt-1):+.2f}%)   analytic (1/f)^(2 q_HF) predicts "
      f"{pred:.5e} ({100*(pred/a0_bt-1):+.2f}%)")
check(same_sample and abs(a0_bt_r1 / pred - 1) < 2e-4,
      f"C3  the correction is EXACTLY multiplicative and the sample is unchanged ({len(sub1)} galaxies, "
      f"identical list): y_out, Gamma, the flatness cut and R_last/R_disk are all distance-invariant, so "
      f"re-running the full pipeline on rescaled distances agrees with (1/f)^(2 q_HF) to "
      f"{1e4*abs(a0_bt_r1/pred-1):.2f} parts in 10^4",
      "the H0 operation touches M_bar only -- verified, not assumed")

k_bt_r1 = a0_bt_r1 / DEN_BT
den73_oml, _ = den_of_h(H0_SPARC_KMS, "fixed_OmL")
den73_wm, oml73 = den_of_h(H0_SPARC_KMS, "fixed_wm")
k_bt_r2a = a0_bt / den73_oml
k_bt_r2b = a0_bt / den73_wm
sig_bt_r1 = S_BT_PUB * k_bt_r1 / K_BT_PUB
print(f"\n   BTFR kappa, one H0 at a time:")
print(f"     committed (MIXED: numerator 73, denominator 67.36)  kappa = {k_bt:.4f}")
print(f"     R1  h = 67.36 everywhere                            kappa = {k_bt_r1:.4f}  "
      f"({100*(k_bt_r1/k_bt-1):+.2f}%)")
print(f"     R2a h = 73 everywhere, Omega_L fixed                kappa = {k_bt_r2a:.4f}  "
      f"({100*(k_bt_r2a/k_bt-1):+.2f}%)")
print(f"     R2b h = 73 everywhere, omega_m fixed (Om_L={oml73:.4f}) kappa = {k_bt_r2b:.4f}  "
      f"({100*(k_bt_r2b/k_bt-1):+.2f}%)")
check(k_bt_r1 < k_bt and k_bt_r2a < k_bt and k_bt_r2b < k_bt and abs(k_bt_r1 - 0.450) < 0.004,
      f"C4  every self-consistent choice LOWERS the BTFR kappa, so the committed 0.465 IS biased high -- "
      f"the mixed convention is the MAXIMUM of the 2x2 (h_num, h_den) box because a0 and the denominator "
      f"both increase with h.  OPERATIVE (R1) value: kappa = {k_bt_r1:.3f} +/- {sig_bt_r1:.3f}, a "
      f"{100*(k_bt_r1/k_bt-1):.1f}% shift = {abs(k_bt_r1-k_bt)/sig_bt_r1:.2f} sigma",
      f"DIRECTION: AWAY from 1/2 ({abs(k_bt-0.5)/S_BT_PUB:.2f} sigma -> "
      f"{abs(k_bt_r1-0.5)/sig_bt_r1:.2f} sigma).  ADVERSE to the framework, and far too small to flip "
      "anything -- the door was already 5.9x too coarse")

# what the committed budget already charges for this
wf = w0 / w0.sum()
SIG_D_HF, SIG_D_OTH = 0.041, 0.030
charged = 2.0 * math.hypot(qhf * SIG_D_HF, (1 - qhf) * SIG_D_OTH)
shift = abs(math.log(k_bt_r1 / k_bt))
check(charged > shift,
      f"C5  the committed budget's 'distance scale (H0=73 / TRGB zp)' term is {100*charged:.2f}%, which is "
      f"LARGER than the {100*shift:.2f}% offset R1 actually applies -- so the ERROR BAR is honestly "
      "charged; what was missing is only the OFFSET.  Verdict on the BTFR number: PARTIALLY HANDLED "
      "(width yes, central value no)",
      "and because the term is already in the budget, the corrected number must NOT also inflate sigma -- "
      "that would double-count")


# =================================================================================================
banner("PART D -- THE DISTANCE-FREE DETERMINATION (kappa = 0.551 +/- 0.043): the theorem vs the operation")

SIG0 = 0.034


def load_df(UD=0.5, UB=0.7, qcut=0.1):
    """the committed distance-free loader, plus per-point bookkeeping of f_D and g_bar."""
    gb, go, ew, hf = [], [], [], []
    for fn in ROTMOD:
        nm = os.path.basename(fn).replace("_rotmod.dat", "")
        try:
            d = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
        m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < qcut)
        R, V, eV, Vg, Vd, Vb = R[m], V[m], eV[m], Vg[m], Vd[m], Vb[m]
        v2 = np.sign(Vg) * Vg ** 2 + UD * Vd ** 2 + UB * Vb ** 2
        ok = v2 > 0
        n = int(ok.sum())
        gb.append(v2[ok] / R[ok] * K_UNIT)
        go.append(V[ok] ** 2 / R[ok] * K_UNIT)
        ew.append(2 * eV[ok] / V[ok] / math.log(10))
        is_hf = 1.0 if (nm in TBL and TBL[nm]["fD"] == 1) else 0.0
        hf.append(np.full(n, is_hf))
    return (np.concatenate(gb), np.concatenate(go), np.concatenate(ew), np.concatenate(hf))


def chi2_df(la, C, gb, go, ew, SIG=SIG0):
    s = np.sqrt(ew ** 2 + SIG ** 2)
    return float(np.sum(((np.log10(go) - (np.log10(gb * nu_kernel(gb / 10 ** la)) + C)) / s) ** 2))


def fit_shape(gb, go, ew, SIG=SIG0):
    """the committed SHAPE-ONLY (free vertical offset) estimator."""
    def prof(la):
        r = minimize(lambda c: chi2_df(la, c[0], gb, go, ew, SIG), [0.0], method="Nelder-Mead")
        return r.fun
    r = minimize(lambda p: prof(p[0]), [math.log10(A0_CANON_REG)], method="Nelder-Mead")
    return 10 ** float(r.x[0])


def fit_std(gb, go, ew, SIG=SIG0):
    r = minimize(lambda p: chi2_df(p[0], 0.0, gb, go, ew, SIG), [math.log10(A0_CANON_REG)],
                 method="Nelder-Mead")
    return 10 ** float(r.x[0])


def stat_err_shape(gb, go, ew, a0):
    """Delta chi2 = 1 half-width on ln a0, by scan."""
    def prof(la):
        r = minimize(lambda c: chi2_df(la, c[0], gb, go, ew), [0.0], method="Nelder-Mead")
        return r.fun
    la0 = math.log10(a0)
    c0 = prof(la0)
    lo, hi = la0, la0
    while prof(lo) - c0 < 1.0 and la0 - lo < 0.5:
        lo -= 2e-3
    while prof(hi) - c0 < 1.0 and hi - la0 < 0.5:
        hi += 2e-3
    return (hi - lo) / 2 * math.log(10)


res_df = {}
for UD in (0.5, 0.7):
    gb, go, ew, hf = load_df(UD=UD)
    a_base = fit_shape(gb, go, ew)
    go_hf = go.copy()
    go_hf[hf == 1] /= F_R1                       # R -> R f for f_D=1 only => g_obs -> g_obs/f, g_bar fixed
    a_r1 = fit_shape(gb, go_hf, ew)
    a_common = fit_shape(gb, go / F_R1, ew)      # the theorem's operation: COMMON rescale
    res_df[UD] = dict(base=a_base, r1=a_r1, common=a_common, gb=gb, go=go, ew=ew, hf=hf)

gb, go, ew, hf = res_df[0.5]["gb"], res_df[0.5]["go"], res_df[0.5]["ew"], res_df[0.5]["hf"]
k05, k07 = res_df[0.5]["base"] / DEN_DF, res_df[0.7]["base"] / DEN_DF
k_cen = 0.5 * (k05 + k07)
print(f"\n   reproduced: kappa(Ups_d = 0.5) = {k05:.4f}, kappa(Ups_d = 0.7) = {k07:.4f}  ->  "
      f"k_cen = {k_cen:.4f}  (committed {K_DF_PUB})")
check(abs(k_cen - K_DF_PUB) < 0.003 and abs(k05 - 0.5287) < 0.002,
      f"D1  the committed distance-free estimator is REPRODUCED independently: k_cen = {k_cen:.4f} vs the "
      f"published {K_DF_PUB}",
      "same loader, same kernel, same Upsilon bracket, same denominator")

ppm = max(abs(res_df[u]["common"] / res_df[u]["base"] - 1) for u in (0.5, 0.7)) * 1e6
check(ppm < 10.0,
      f"D2  its THEOREM holds exactly as published: a COMMON distance rescaling of {100*(F_R1-1):.2f}% moves "
      f"a_0 by {ppm:.2f} ppm, because the free vertical offset C absorbs a common g_obs rescaling entirely",
      "nothing here disputes the theorem -- the question is whether the H0 convention IS a common rescaling")

sh05 = res_df[0.5]["r1"] / res_df[0.5]["base"] - 1
sh07 = res_df[0.7]["r1"] / res_df[0.7]["base"] - 1
stat05 = stat_err_shape(gb, go, ew, res_df[0.5]["base"])
print(f"\n   *** the H0 operation is NOT common -- it moves ONLY the {hist[1]} f_D = 1 galaxies: ***")
print(f"     Ups_d = 0.5 : a_0 {res_df[0.5]['base']:.5e} -> {res_df[0.5]['r1']:.5e}  ({100*sh05:+.2f}%)")
print(f"     Ups_d = 0.7 : a_0 {res_df[0.7]['base']:.5e} -> {res_df[0.7]['r1']:.5e}  ({100*sh07:+.2f}%)")
print(f"     statistical error on the same quantity: {100*stat05:.2f}%   (quoted total budget 7.77%)")
check(min(sh05, sh07) > 0.04 and min(sh05, sh07) > 3 * stat05,
      f"D3  *** THE DISTANCE-FREE NUMBER IS NOT H0-CLEAN.  A Hubble-flow-ONLY rescale to Planck's H0 moves "
      f"its a_0 by {100*sh05:+.2f}% / {100*sh07:+.2f}% (Ups = 0.5/0.7) -- {sh05/stat05:.1f}x its "
      f"{100*stat05:.2f}% statistical error and comparable to its ENTIRE 7.77% quoted budget, which charges "
      f"0.0% for distance. ***",
      "the immunity theorem is true and irrelevant here: it covers common rescalings, and H0 is not one")

std_b = fit_std(gb, go, ew)
go_hf5 = go.copy()
go_hf5[hf == 1] /= F_R1
std_r1 = fit_std(gb, go_hf5, ew)
sh_std = std_r1 / std_b - 1
print(f"\n   AND THE SIGN IS ESTIMATOR-DEPENDENT, which is why 'the direction of the H0 bias' is not one "
      f"number:\n     STANDARD (C = 0) estimator on the same data: a_0 {std_b:.5e} -> {std_r1:.5e} "
      f"({100*sh_std:+.2f}%)  [the naive a_0 ~ D^-2 sign]\n     SHAPE-ONLY (C free), which is what the "
      f"committed 0.551 uses: {100*sh05:+.2f}%  [opposite sign]")
check(sh_std < 0.0 < sh05,
      f"D3b the two estimators respond with OPPOSITE SIGNS to the identical Planck-consistent distance "
      f"correction: the standard C = 0 fit moves {100*sh_std:+.2f}% (down, as a_0 ~ D^-2 demands) while the "
      f"shape-only fit moves {100*sh05:+.2f}% (up, because its lever is the deep-to-Newtonian separation). "
      f"So 'the H0 convention biases kappa high' is TRUE of a standard-estimator kappa and FALSE of a "
      f"shape-only kappa -- the direction cannot be stated without naming the estimator",
      "this is the single most important correction to today's PART F flag, and it is a computed sign, not "
      "an argued one")

wpt = 1.0 / (ew ** 2 + SIG0 ** 2)
med_hf = float(np.median(gb[hf == 1]) / A0_CANON_REG)
med_no = float(np.median(gb[hf == 0]) / A0_CANON_REG)
wfrac_hf = float(wpt[hf == 1].sum() / wpt.sum())
lg = np.array([1e-4, 1e-2, 1.0, 1e2, 1e4])
dlog = []
for yv in lg:
    e = 1e-4
    m1 = math.log10(nu_kernel(yv / 10 ** e)) - math.log10(nu_kernel(yv / 10 ** (-e)))
    dlog.append(m1 / (2 * e))
print(f"\n   MECHANISM, measured: median g_bar = {med_hf:.3f} a_0 (Hubble-flow) vs {med_no:.3f} a_0 "
      f"(direct-distance); Hubble-flow points carry {100*wfrac_hf:.1f}% of the fit weight")
print(f"   d log(model)/d log(a_0) at y = 1e-4, 1e-2, 1, 1e2, 1e4 : " +
      "  ".join(f"{v:+.3f}" for v in dlog))
check(med_hf > 1.5 * med_no and dlog[0] > 0.49 and abs(dlog[-1]) < 0.02,
      f"D4  and the mechanism is exactly the estimator's own lever: d log(model)/d log a_0 = +0.5 in the "
      f"deep-MOND limit and -> 0 in the Newtonian limit, so with C free the ONLY information about a_0 is "
      f"the VERTICAL SEPARATION between the two ends.  The Hubble-flow galaxies sit at {med_hf/med_no:.2f}x "
      f"higher g_bar -- i.e. on the Newtonian end -- so an H0 shift of that subset acts directly on the "
      f"lever and RAISES a_0 (opposite in sign to the naive a_0 ~ D^-2 argument)",
      "which is why the direction of this one could not be guessed and had to be computed")

# CONTROL: is the shift specific to the f_D = 1 subset, or would any subset of that weight do it?
rng = np.random.default_rng(20260817)
names = []
for fn in ROTMOD:
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    names.append(nm)
gal_id = []
for fn in ROTMOD:
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    d = np.genfromtxt(fn, comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < 0.1)
    v2 = np.sign(Vg[m]) * Vg[m] ** 2 + 0.5 * Vd[m] ** 2 + 0.7 * Vb[m] ** 2
    gal_id.append(np.full(int((v2 > 0).sum()), nm))
gal_id = np.concatenate(gal_id)
uniq = np.array(sorted(set(gal_id)))
target = float((hf == 1).mean())
null = []
for _ in range(120):
    pick = rng.permutation(uniq)
    sel = np.zeros(len(gb), bool)
    for nm in pick:
        if sel.mean() >= target:
            break
        sel |= (gal_id == nm)
    g2 = go.copy()
    g2[sel] /= F_R1
    null.append(fit_shape(gb, g2, ew) / res_df[0.5]["base"] - 1)
null = np.array(null)
z_null = (sh05 - null.mean()) / null.std(ddof=1)
pct = 100.0 * float((null < sh05).mean())
# the complement test: rescale the DIRECT-distance galaxies instead
go_dir = go.copy()
go_dir[hf == 0] /= F_R1
sh_dir = fit_shape(gb, go_dir, ew) / res_df[0.5]["base"] - 1
print(f"\n   CONTROL -- 120 RANDOM galaxy subsets matched to the same {100*target:.0f}% point fraction: "
      f"induced shift = {100*null.mean():+.2f}% +/- {100*null.std(ddof=1):.2f}% (sd), range "
      f"[{100*null.min():+.2f}%, {100*null.max():+.2f}%]")
print(f"   the f_D = 1 subset's {100*sh05:+.2f}% sits at the {pct:.0f}th percentile of that null "
      f"({z_null:+.1f} sd from its centre)")
print(f"   COMPLEMENT: rescaling the DIRECT-distance galaxies instead gives {100*sh_dir:+.2f}% -- opposite "
      f"sign, as the g_bar split predicts")
p_perm = (100.0 - pct) / 100.0
check(pct >= 90.0 and null.std(ddof=1) > stat05 and sh_dir < 0.0,
      f"D5  CONTROL, TWO CONCLUSIONS AND BOTH ARE ADVERSE TO THE 'ZERO DISTANCE CHARGE'.  (i) the f_D = 1 "
      f"selection IS a tail case of the null: {100*sh05:+.2f}% sits at the {pct:.0f}th percentile of 120 "
      f"random matched subsets, one-sided permutation p = {p_perm:.3f}, and the COMPLEMENT subset moves a_0 "
      f"the other way ({100*sh_dir:+.2f}%) -- so the distance-method/g_bar correlation is a real channel.  "
      f"(ii) but the null's own WIDTH, {100*null.std(ddof=1):.2f}% sd, already exceeds the estimator's "
      f"{100*stat05:.2f}% statistical error by {null.std(ddof=1)/stat05:.1f}x, so ANY subset-selective "
      f"distance error of this size moves a_0 by more than its stat error -- the exposure is partly generic",
      f"AGAINST INTEREST, recorded rather than tuned: I first set this check at 'null sd > 2x stat error' "
      f"and it FAILED ({null.std(ddof=1)/stat05:.2f}x, just under), so the generic component is real but "
      f"NOT as dominant as my first pass asserted; the tail statement (p = {p_perm:.3f}) is the stronger of "
      f"the two and is what carries the finding")

q_eff_df = 0.5 * (0.5 * (math.log1p(sh05) + math.log1p(sh07))) / math.log(1.0 / F_R1)
k_df_r1 = k_cen * math.exp(0.5 * (math.log1p(sh05) + math.log1p(sh07)))
k_df_r2a = k_cen * DEN_DF / den73_oml
k_df_r2b = k_cen * DEN_DF / den73_wm
sig_df_r1 = S_DF_PUB * k_df_r1 / K_DF_PUB
print(f"\n   distance-free kappa, one H0 at a time  (q_eff = {q_eff_df:+.3f}, vs the invariant point "
      f"p/2 = {P_OML/2:.3f}):")
print(f"     committed (MIXED)                    kappa = {k_cen:.4f}")
print(f"     R1  h = 67.36 everywhere             kappa = {k_df_r1:.4f}  ({100*(k_df_r1/k_cen-1):+.2f}%)")
print(f"     R2a h = 73 everywhere, Om_L fixed    kappa = {k_df_r2a:.4f}  ({100*(k_df_r2a/k_cen-1):+.2f}%)")
print(f"     R2b h = 73 everywhere, omega_m fixed kappa = {k_df_r2b:.4f}  ({100*(k_df_r2b/k_cen-1):+.2f}%)")
lo_df, hi_df = min(k_df_r1, k_df_r2a, k_df_r2b), max(k_df_r1, k_df_r2a, k_df_r2b)
check(lo_df < k_cen < hi_df,
      f"D6  *** TODAY'S DIRECTION CLAIM IS NOT SUPPORTED FOR THIS NUMBER.  The self-consistent range is "
      f"[{lo_df:.3f}, {hi_df:.3f}] and the committed {k_cen:.3f} sits INSIDE it, not at the top: the two "
      f"resolutions push in OPPOSITE directions because q_eff = {q_eff_df:+.3f} is NEGATIVE.  So 0.551 is "
      f"not '~8% biased high'. ***",
      f"what IS wrong is the ERROR BAR: half-range {0.5*(hi_df-lo_df)/k_cen*100:.2f}% is not in the quoted "
      f"7.77%, so sigma(kappa) = 0.043 should be at least "
      f"{math.hypot(S_DF_PUB, 0.5*(hi_df-lo_df)):.3f}")

check(k_df_r1 > k_cen and abs(k_df_r1 - 0.5) / sig_df_r1 > abs(k_cen - 0.5) / S_DF_PUB,
      f"D7  and under the OPERATIVE resolution R1 the move is ADVERSE: kappa = {k_df_r1:.3f} +/- "
      f"{sig_df_r1:.3f}, which is {abs(k_df_r1-0.5)/sig_df_r1:.2f} sigma from 1/2 against "
      f"{abs(k_cen-0.5)/S_DF_PUB:.2f} sigma before",
      "R1 is operative because the framework's REGISTERED a_0 = 9.3619e-11 is built from Planck's "
      "rho_Lambda; R1 leaves that prediction untouched and rescales the data instead")


# =================================================================================================
banner("PART E -- THE CORRECTED TABLE, BOTH FOOTINGS, AND THE DIRECTION LEDGER")

ALT = DEN_DF / DEN_ALT_DF
rows = [
    ("distance-free  committed (MIXED 73/67.36)", k_cen, S_DF_PUB),
    ("distance-free  R1  h=67.36 everywhere  *OPERATIVE*", k_df_r1, sig_df_r1),
    ("distance-free  R2a h=73, Omega_L fixed", k_df_r2a, S_DF_PUB * k_df_r2a / K_DF_PUB),
    ("distance-free  R2b h=73, omega_m fixed", k_df_r2b, S_DF_PUB * k_df_r2b / K_DF_PUB),
    ("BTFR           committed (MIXED 73/67.36)", k_bt, S_BT_PUB),
    ("BTFR           R1  h=67.36 everywhere  *OPERATIVE*", k_bt_r1, sig_bt_r1),
    ("BTFR           R2a h=73, Omega_L fixed", k_bt_r2a, S_BT_PUB * k_bt_r2a / K_BT_PUB),
    ("BTFR           R2b h=73, omega_m fixed", k_bt_r2b, S_BT_PUB * k_bt_r2b / K_BT_PUB),
]
print(f"\n   {'determination':<52}{'kappa (canon)':>16}{'kappa (alt)':>16}{'n_sigma from 1/2':>18}")
for lbl, kv, sv in rows:
    print(f"   {lbl:<52}{kv:>9.3f} +/-{sv:5.3f}{kv*ALT:>10.3f} +/-{sv*ALT:5.3f}"
          f"{abs(kv-0.5)/sv:>16.2f}")

z_mixed = abs(k_cen - k_bt) / math.hypot(S_DF_PUB, S_BT_PUB)
z_r1 = abs(k_df_r1 - k_bt_r1) / math.hypot(sig_df_r1, sig_bt_r1)
z_r2a = abs(k_df_r2a - k_bt_r2a) / math.hypot(S_DF_PUB * k_df_r2a / K_DF_PUB, S_BT_PUB * k_bt_r2a / K_BT_PUB)
print(f"\n   mutual consistency of the two determinations: MIXED {z_mixed:.2f} sigma  ->  "
      f"R1 {z_r1:.2f} sigma  ->  R2a {z_r2a:.2f} sigma")
check(z_r1 > z_mixed and z_r1 < 3.0,
      f"E1  the H0 convention also changes the two determinations' AGREEMENT WITH EACH OTHER, because their "
      f"q_eff have opposite SIGNS: {z_mixed:.2f} sigma apart on the mixed convention, {z_r1:.2f} sigma under "
      f"R1.  Still not a contradiction, but the mixed convention flatters the internal consistency too",
      "no cascade: nothing in the corpus turns on the difference between 1.0 and 1.6 sigma here")

a0_half_r2a = 0.5 * den73_oml
a0_half_r2b = 0.5 * den73_wm
print(f"\n   AND THE PRICE OF R2, which is why it is not the operative resolution: rebuilding rho_Lambda at "
      f"H0 = 73 moves\n   the framework's OWN prediction from a_0(kappa=1/2) = {A0_CANON_REG:.4e} to "
      f"{a0_half_r2a:.4e} (Om_L fixed) or {a0_half_r2b:.4e} (omega_m fixed),\n   i.e. +"
      f"{100*(a0_half_r2a/A0_CANON_REG-1):.1f}% to +{100*(a0_half_r2b/A0_CANON_REG-1):.1f}% -- which would "
      f"have to be propagated through the RAR fit, the kernel, the DR4 target and every a_0-dependent "
      f"result.")
best_toward = min([(abs(k - 0.5), lbl) for lbl, k, s in rows if lbl.startswith("distance-free")])
check(abs(k_df_r2b - 0.5) < abs(k_cen - 0.5) and a0_half_r2b > 1.04 * A0_CANON_REG,
      f"E2  *** AND THE ONE MOVE THAT LOOKS LIKE A WIN IS THE ONE TO REFUSE.  R2b brings the distance-free "
      f"kappa from {k_cen:.3f} ({abs(k_cen-0.5)/S_DF_PUB:.2f} sigma from 1/2) to {k_df_r2b:.3f} "
      f"({abs(k_df_r2b-0.5)/(S_DF_PUB*k_df_r2b/K_DF_PUB):.2f} sigma) -- but it buys that ONLY by growing the "
      f"DENOMINATOR, which simultaneously moves the framework's predicted a_0 to {a0_half_r2b:.3e}.  kappa "
      f"landing on 1/2 because rho_Lambda was rebuilt at a different H0 is not evidence for kappa = 1/2, "
      f"and it is not free. ***",
      "recorded explicitly so that no later run can quote R2b's 0.49 as a confirmation")


# =================================================================================================
banner("PART F -- SECONDARY FINDINGS AND WHAT REMAINS OWED")

# F1: a third H0 appearance, inside the distance-free script's own a0(z) check.
z_at_67 = H0_PLANCK_KMS * 100.0 / 2.99792458e5
z_at_73 = H0_SPARC_KMS * 100.0 / 2.99792458e5


def a0z(z, w0, wa):
    return (1 + z) ** (1.5 * (1 + w0 + wa)) * math.exp(-1.5 * wa * z / (1 + z))


Ds = np.array([TBL[n]["D"] for n in TBL])
dev_67 = max(abs(a0z(H0_PLANCK_KMS * D / 2.99792458e5, -0.9, -0.4) - 1) for D in Ds)
dev_73 = max(abs(a0z(H0_SPARC_KMS * D / 2.99792458e5, -0.9, -0.4) - 1) for D in Ds)
print(f"\n   the distance-free script converts SPARC distances to redshift with z = 67.36 D/c, but those "
      f"distances were\n   BUILT at H0 = 73 -- so for the f_D = 1 galaxies it understates z by "
      f"{100*(H0_SPARC_KMS/H0_PLANCK_KMS-1):.1f}%.  Effect on its\n   a_0(z) check: worst-case DESI-like "
      f"deviation {100*dev_67:.3f}% -> {100*dev_73:.3f}%.")
check(dev_73 < 0.01,
      f"F1  a THIRD H0 appearance, in the opposite direction, and it is genuinely negligible: the a_0(z) "
      f"correction over SPARC goes from {100*dev_67:.3f}% to {100*dev_73:.3f}% on a DESI-like fork -- still "
      f"far below any error bar in this lane",
      "labelled for completeness; nothing to correct beyond a comment")

OWED = [
    "the a_0 used by rar_framework_a0_mlfit.py (0.108 dex at Ups = 0.70) is HELD FIXED at the Planck-footed "
    "9.36e-11 while the data carry H0 = 73 distances: that mismatch does not move a kappa, it moves the "
    "best-fit Upsilon and the scatter.  Re-running that fit with R1 distances is OWED (it is the one number "
    "the memory rule says to re-run before relaying any deficit).",
    "the 28 Ursa Major (f_D = 4) distances are treated here as H0-free; they are tied to their own ladder, "
    "so the exposure computed in PART C/D is a LOWER bound.  Pricing them needs the UMa distance provenance.",
    "the a0-line determination (0.84-1.36e-10, +/-16%) and the gas-dominated TLS number were NOT audited "
    "here; the a0-line is a g_obs^2 - g_bar^2 = a0 g_bar slope, so its D-exposure is a THIRD exponent and "
    "has to be computed separately, not inherited from either number audited here.",
    "one constant in one place: 1.87094e-10 (hard-coded) vs 1.87250e-10 (rebuilt from H0 = 67.39) differ by "
    "0.08%, and the alt denominator is 0.3% off c H0 sqrt(3/8pi) at H0 = 67.36.",
    "whether to quote kappa at R1 or marginalised over [R1, R2b] is a CONVENTION DECISION for Carl, not a "
    "calculation: this script supplies both and refuses to pick silently.",
]
print("\n   OWED:")
for o in OWED:
    print(f"     - {o}")
check(len(OWED) == 5, "F2  five owed items named, none hidden", "")


# =================================================================================================
banner("SUMMARY")
print(f"""
  1.  THE INCONSISTENCY IS REAL AND STRUCTURAL, and it is not a bug in either script: kappa = a_0 /
      (c sqrt(G rho_Lambda)) divides a SPARC-calibrated numerator (Hubble-flow distances at H0 = 73,
      {hist[1]}/{nrow} galaxies, parsed) by a Planck-calibrated denominator (H0 ~ 67.4).  kappa ~ h^(2 q_eff - p)
      is H0-invariant ONLY at q_eff = p/2, and neither estimator is there.  kappa must be quoted with an H0.

  2.  BTFR, kappa = 0.465 +/- 0.076 -> {k_bt_r1:.3f} +/- {sig_bt_r1:.3f} under the operative Planck-consistent
      resolution.  q_eff = +{qhf:.3f} (the WEIGHT fraction on Hubble-flow distances, not the {nhf}/{len(sub0)} count),
      so the shift is {100*(k_bt_r1/k_bt-1):+.1f}% -- NOT the flagged 8%.  Its budget already charges {100*charged:.2f}% for the
      distance scale, so the WIDTH was honest and only the OFFSET was missing.  PARTIALLY HANDLED.
      Direction: AWAY from 1/2.  ADVERSE, and {abs(k_bt_r1-k_bt)/sig_bt_r1:.2f} sigma -- flips nothing.

  3.  *** DISTANCE-FREE, kappa = 0.551 +/- 0.043: NOT HANDLED, and the exposure is BIGGER than the BTFR's.
      Its distance-immunity theorem is true ({ppm:.1f} ppm under a common rescale, reproduced) and does not
      cover the H0 operation, which moves ONLY the {hist[1]} Hubble-flow galaxies -- and those sit at
      {med_hf/med_no:.2f}x higher g_bar, i.e. on the Newtonian end, which is precisely the lever a shape-only
      estimator uses.  Planck-consistent distances move a_0 by {100*sh05:+.2f}%/{100*sh07:+.2f}%, {sh05/stat05:.0f}x its
      {100*stat05:.2f}% statistical error, against a budget that charges ZERO for distance.  Controlled two ways:
      the f_D = 1 selection is at the {pct:.0f}th percentile of 120 random matched subsets (permutation
      p = {p_perm:.3f}) and the complement subset moves a_0 the other way ({100*sh_dir:+.2f}%), so the channel is
      real; but that null's own sd is already {100*null.std(ddof=1):.2f}%, so part of the sensitivity is generic
      to ANY subset-selective distance error. ***

  4.  DIRECTION, both ways, since that is the rule.  Under R1 (operative) BOTH numbers move AWAY from
      1/2: {k_cen:.3f} -> {k_df_r1:.3f} ({abs(k_cen-0.5)/S_DF_PUB:.2f} -> {abs(k_df_r1-0.5)/sig_df_r1:.2f} sigma) and {k_bt:.3f} -> {k_bt_r1:.3f}.  ADVERSE.
      Under R2 both move TOWARD 1/2 ({k_df_r2b:.3f} at best, {abs(k_df_r2b-0.5)/(S_DF_PUB*k_df_r2b/K_DF_PUB):.2f} sigma) -- and that is REFUSED as a win,
      because it is bought by rebuilding rho_Lambda at H0 = 73, which moves the framework's OWN predicted
      a_0 to {a0_half_r2b:.3e} (+{100*(a0_half_r2b/A0_CANON_REG-1):.0f}%) and would have to be propagated everywhere.

  5.  TODAY'S FLAG, GRADED.  "kappa ~ H0 for the Hubble-flow subset" -- CORRECT as algebra.  "~8% bias" --
      TOO BIG for both committed numbers ({100*(k_bt_r1/k_bt-1):+.1f}% BTFR under R1); it is the q_eff = 1 limit.
      "in the direction of OVERSTATING kappa" -- TRUE for the BTFR number and for ANY standard-estimator
      kappa (the same operation moves the C = 0 fit {100*sh_std:+.1f}%), but FALSE for the shape-only
      estimator the committed 0.551 actually uses, whose q_eff is NEGATIVE ({q_eff_df:+.3f}): its two
      resolutions STRADDLE the committed value.  The direction cannot be stated without naming the
      estimator.  The real defect in 0.551 +/- 0.043 is the error bar: sigma should be at least
      {math.hypot(S_DF_PUB, 0.5*(hi_df-lo_df)):.3f}, not 0.043.

  6.  NET EFFECT ON THE STANDING POSITION: none of the four verdicts move.  kappa remains FITTED not
      derived, consistent with 1/2 on every convention, and the data still do not single out 1/2 --
      the audit widens the distance-free error bar and lowers the BTFR central value, both adverse,
      both far too small to change a conclusion.
""")

print("=" * 100)
print(f"H0-CONVENTION AUDIT: {NCHK[0] - len(FAIL)}/{NCHK[0]} checks passed"
      + ("" if not FAIL else f";  FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
