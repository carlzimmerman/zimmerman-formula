#!/usr/bin/env python3
"""v04_omega_lambda_prediction.py -- the framework's own prediction  Omega_Lambda = 32 pi a0^2 / (3 H0^2 c^2) = Z_F^2 (a0/(c H0))^2,
computed from each a0 determination, with propagated errors, against the measured 0.685 +- 0.007.  Reproduces the audit's 0.906 for the
record's SPARC a0 and explains the ~2.4 sigma.  NOTHING IS ADJUSTED: the shifts that would remove the tension are reported and compared with
the measured systematic budget (v02) and the published budgets (v01).
Exit 0 = every check held.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v_common import *

ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
r1, r2 = json.load(open("v01_results.json")), json.load(open("v02_results.json"))
U = 1e-10; c = c_si
OM_MEAS, S_OM = 0.685, 0.007
def omega_pred(a0, H0):           # Omega_Lambda = 32 pi a0^2 / (3 H0^2 c^2)
    return 32 * math.pi * a0 ** 2 / (3 * H_si(H0) ** 2 * c ** 2)

# ---------------------------------------------------------------- 0. algebra checks
print("0  algebra")
Zsq = 32 * math.pi / 3
check(abs(omega_pred(1e-10, 67.4) - Zsq * (1e-10 / (c * H_si(67.4))) ** 2) < 1e-12, "A1 Omega = 32 pi a0^2/(3 H0^2 c^2) = Z_F^2 (a0/cH0)^2 (Z_F^2 = 32 pi/3)")
a_can = c * H_si(67.4) * math.sqrt(OM_MEAS) / Z_F
check(abs(omega_pred(a_can, 67.4) - OM_MEAS) < 1e-12, f"A2 identity: a0 = c H0 sqrt(0.685)/Z_F = {a_can:.4e} returns Omega = 0.685 exactly")
check(abs(omega_pred(2 * a_can, 67.4) / OM_MEAS - 4) < 1e-9 and abs(omega_pred(a_can, 73.0) / OM_MEAS - (67.4 / 73.0) ** 2) < 1e-9, "A3 Omega ~ a0^2 and ~ H0^-2 (doubling a0 quadruples Omega; H0 67.4 -> 73 scales by (67.4/73)^2)")
check(abs(Z_M ** 2 / Zsq * OM_MEAS - 0.685 * 39.4784176 / 33.5103216) < 1e-9 and abs(Z_M ** 2 / Zsq - 1.17810) < 1e-4, "A4 (mutation) using Milgrom's Z = 2 pi in place of Z_F would multiply the prediction by (2 pi)^2/(32 pi/3) = 3 pi/8 = 1.178: the check separates the coefficients")

# ---------------------------------------------------------------- 1. the record's SPARC a0: 0.906 and the tension
print("\n1  the record's SPARC a0 = 1.0766e-10 (5.44% clustered-crude, 1.24% independent)")
a_rec, s_rec = 1.0766e-10, 0.0544
Om_rec = omega_pred(a_rec, 67.4)
print(f"   Omega_pred = {Om_rec:.4f}   (audit: 0.906);   measured 0.685 +- 0.007")
check(abs(Om_rec - 0.906) < 0.002, "R1 reproduces the audit's 0.906")
sOm = 2 * s_rec * Om_rec
t_om = (Om_rec - OM_MEAS) / math.hypot(sOm, S_OM)
t_a0_lin = (a_rec - a_can) / (s_rec * a_rec)                  # the record's own '2.40 sigma' (sigma taken as 5.44% of the FITTED a0)
t_ln = math.log(a_rec / a_can) / s_rec
d_chi = 63.9; defl = 3380 / 175
t_prof = math.sqrt(d_chi / defl)
print(f"   the same tension in different parametrisations / estimators:")
print(f"     a0 linear, sigma = 5.44% of the fit (the record's convention)   : {t_a0_lin:.2f} sigma")
print(f"     Omega linear, sigma_Omega = 2 x 5.44% x Omega_pred (+0.007)     : {t_om:.2f} sigma")
print(f"     ln a0, sigma = 5.44%                                             : {t_ln:.2f} sigma")
print(f"     profile d chi2 = 63.9 deflated by N_pts/N_gal = {defl:.1f}              : {t_prof:.2f} sigma   (the record's P3 table: 1.82)")
sig_b = r2["record_pl"]["sig_ln_bootstrap"]
print(f"     ln a0 with the galaxy-bootstrap sigma = {100*sig_b:.1f}% (v02)                : {math.log(r2['record_pl']['a0_hat']/a_can)/sig_b:.2f} sigma  (a0_hat = {r2['record_pl']['a0_hat']/U:.4f}e-10)")
check(abs(t_a0_lin - 2.40) < 0.02 and abs(t_prof - 1.82) < 0.02, "R2 reproduces the record's 2.40 sigma (a0-linear) and 1.82 sigma (deflated d chi2)")
print("   -> WHY THEY DIFFER: Omega ~ a0^2 doubles the fractional error and makes the mapping non-linear; the record divides by 5.44% of the FITTED value (not of the")
print("      prediction), and the profile is asymmetric.  The honest range is 1.7-2.6 sigma; none of them uses the systematic budget, which (below) is larger than the offset.")
res = dict(Om_rec=Om_rec, t_a0_lin=t_a0_lin, t_om=t_om, t_ln=t_ln, t_prof=t_prof)

# ---------------------------------------------------------------- 2. per determination and H0
print("\n2  Omega_Lambda predicted by the framework from each a0 (Z_F = sqrt(32pi/3)); error = 2 x fractional a0 error (+ 2 x H0 error), 0.685 +- 0.007 measured")
rows = {r["id"]: r for r in r1["rows"]}
sel = [("Rec", 0.0544), ("thisA1", r2["record_pl"]["sig_ln_bootstrap"]), ("MLS16", math.hypot(0.02, 0.24) / 1.2), ("Des23", math.hypot(0.04, 0.09) / 1.19), ("McG12", 0.3 / 1.3),
       ("thisR0", None), ("thisR1", None), ("thisR2", None), ("Rod18-RAR", None), ("CZ19-RAR", None), ("DBF23-RAR", None), ("DBF23-std", None)]
E = r1["E"]
print(f"   {'determination':<14}{'a0[1e-10]':>10}{'err':>7} | " + "".join(f"{'H0='+str(h):>20}" for h in (67.4, 70.2, 73.0)))
res["Om"] = {}
for k, s in sel + [("ENSEMBLE E", E["sd_ln"])]:
    a0 = (E["logmean"] if k == "ENSEMBLE E" else rows[k]["a0"]) * U
    line = f"   {k:<14}{a0/U:>10.4f}{('%5.1f%%' % (100*s)) if s else '   n/a':>7} | "
    for h in (67.4, 70.2, 73.0):
        Om = omega_pred(a0, h)
        if s:
            sh = 2.0 * (0.5 / 67.4 if h == 67.4 else (1.0 / 73.0 if h == 73.0 else 2.8 / 70.2))
            sO = Om * math.hypot(2 * s, 2 * (0.5 / 67.4 if h == 67.4 else (1.0 / 73.0 if h == 73.0 else 2.8 / 70.2)))
            t = (Om - OM_MEAS) / math.hypot(sO, S_OM)
            line += f"{Om:>8.3f} +-{sO:5.3f} ({t:+4.1f}s)"
            res["Om"][f"{k}|{h}"] = dict(Om=Om, sig=sO, t=t)
        else:
            line += f"{Om:>8.3f}{'':>12}"
            res["Om"][f"{k}|{h}"] = dict(Om=Om)
    print(line)
print("   (s = (Omega_pred - 0.685)/sqrt(sigma_pred^2 + 0.007^2); rows with no printed error: the papers give none, or it is the analysis-choice scatter of E.)")
check(abs(res["Om"]["Rec|67.4"]["Om"] - 0.906) < 0.002, "T1 the record's row is the audit's 0.906")
Oms = [v["Om"] for k, v in res["Om"].items() if k.endswith("|67.4") and not k.startswith("DBF23-std")]
print(f"   spread of Omega_pred at H0 = 67.4 over the galaxy-scale RAR-family analyses: {min(Oms):.2f} - {max(Oms):.2f}  (measured 0.685)")
check(min(Oms) < 0.685 < max(Oms), "T2 the measured 0.685 lies INSIDE the range of predictions from the different published/own a0 analyses (the prediction is analysis-choice-dependent, sign included)")

# ---------------------------------------------------------------- 3. kernel x Upsilon x H0 world
print("\n3  Omega_pred by fitting choice (this work, v02) and by H0 'world':  P = Planck H0 = 67.4 with SPARC Hubble-flow distances rescaled 73 -> 67.4;  S = SH0ES H0 = 73 with SPARC distances as published")
mat = r2["matrix"]; h0c = r2["H0_coupled"]
print(f"   {'IF (Upsilon free 0.05-3)':<26}{'a0 as published':>16}{'Om @67.4':>10}{'a0 (P, HF only)':>17}{'Om':>7}{'a0 (P, all dist.)':>19}{'Om':>7}{'Om (S: a0 as pub., 73)':>24}")
for nm in h0c:
    b0, hf, al = h0c[nm]["baseline"], h0c[nm]["HF only"], h0c[nm]["all distances"]
    print(f"   {nm:<26}{b0/U:>16.4f}{omega_pred(b0,67.4):>10.3f}{hf/U:>17.4f}{omega_pred(hf,67.4):>7.3f}{al/U:>19.4f}{omega_pred(al,67.4):>7.3f}{omega_pred(b0,73.0):>24.3f}")
res["worlds"] = {nm: dict(pub=omega_pred(v["baseline"], 67.4), P_HF=omega_pred(v["HF only"], 67.4), P_all=omega_pred(v["all distances"], 67.4), S=omega_pred(v["baseline"], 73.0)) for nm, v in h0c.items()}
o1 = res["worlds"]["alpha1 (record kernel)"]
print(f"   record kernel: the 0.906 becomes {o1['P_HF']:.3f} (Hubble-flow distances re-scaled) or {o1['P_all']:.3f} (all distances) in a self-consistent Planck-H0 world, and {o1['S']:.3f} at H0 = 73.")
check(o1["P_all"] < o1["P_HF"] < o1["pub"], "W1 in the Planck-H0 world the predicted Omega falls monotonically as more distances are rescaled")
check(res["worlds"]["RAR (MLS16)"]["pub"] < 0.685 < o1["pub"], "W2 the prediction flips sign with the interpolating function: RAR gives Omega_pred < 0.685, the record's alpha1 kernel gives > 0.685")
print("   CAUTION: the P-world rescaling assumes SPARC's distances were biased low by exactly 73/67.4; the S-world assumes Omega_Lambda = 0.685 (a Planck-fit number) is compared at a")
print("   non-Planck H0.  Both are sensitivity statements about how much H0-coupling matters, not corrections to the record.")

# ---------------------------------------------------------------- 4. what shift removes the tension, and is it inside the budget
print("\n4  the fractional shift of a0_obs that would remove the tension (record kernel, H0 = 67.4), and what the systematic budget offers")
need_center = a_can / a_rec - 1
need_1s = (a_can + s_rec * a_rec) / a_rec - 1
need_2s = (a_can + 2 * s_rec * a_rec) / a_rec - 1
print(f"   to Omega_pred = 0.685 exactly: a0_obs must fall by {100*need_center:+.1f}% (a0 = {a_can/U:.4f}e-10);  to within 1 sigma (5.44%): {100*need_1s:+.1f}%;  to within 2 sigma: {100*need_2s:+.1f}%")
pert = r2["perturbations"]
menu = [("Hubble-flow distances x 73/67.4 (H0 = 67.4 world)", "Hubble-flow (f_D=1) distances x 1.0831 (H0 73 -> 67.4)"),
        ("ALL distances x 73/67.4 (ladder biased if H0 = 67.4)", "ALL distances x 1.0831 (ladder biased if H0 = 67.4)"),
        ("all distances x 1.05", "all distances x 1.05"), ("gas mass x 1.10", "gas mass x 1.10"), ("gas mass x 1.20", "gas mass x 1.20"),
        ("coherent inclination + 1 sigma_i", "inclination + 1 sigma_i (coherent, per-galaxy e_Inc)")]
print(f"   {'systematic (v02, measured on the record kernel)':<58}{'d ln a0':>9}{'fraction of needed shift':>28}")
frac = {}
for lab, key in menu:
    d = pert[key]["dln"]; frac[lab] = d / math.log(1 + need_center)
    print(f"   {lab:<58}{100*d:>+8.1f}%{100*frac[lab]:>26.0f}%")
d_rar = math.log(mat["Upsilon free 0.05-3 (record)"]["RAR (MLS16)"]["a0"] / mat["Upsilon free 0.05-3 (record)"]["alpha1 (record kernel)"]["a0"])
print(f"   {'interpolating function alpha1 -> RAR (data-preferred, d chi2 = 168)':<58}{100*d_rar:>+8.1f}%{100*d_rar/math.log(1+need_center):>26.0f}%   (overshoots: Omega_pred = {res['worlds']['RAR (MLS16)']['pub']:.3f} < 0.685)")
bud = r2["budget"]
quad_ind = math.sqrt(bud["global distance scale +-5% (calibrator zero point)"] ** 2 + bud["gas mass +-10% (HI calibration, H2, helium)"] ** 2 + bud["coherent inclination bias +-1 sigma_i (upper bound)"] ** 2)
quad_all = math.sqrt(quad_ind ** 2 + bud["interpolating function, all four IFs (half-range, Upsilon free)"] ** 2 + bud["Upsilon treatment (free vs fixed 0.5, RAR IF; half-range)"] ** 2 + bud["galaxy-class heterogeneity (gas- vs star-dominated, cleanest fit; half-range)"] ** 2)
print(f"   measured 1-sigma-ish budget (v02, quadrature): distance+gas+inclination = {100*quad_ind:.1f}%;  adding IF + Upsilon treatment + class heterogeneity = {100*quad_all:.1f}%;  published: MLS16 20%, Desmond 2023 7.6% (sys)")
print(f"   needed shift {100*abs(need_center):.1f}% = {abs(math.log(1+need_center))/quad_ind:.2f} x the distance+gas+inclination budget, {abs(math.log(1+need_center))/quad_all:.2f} x the full budget, {abs(need_center)/0.20:.2f} x MLS16's quoted 20%")
check(abs(math.log(1 + need_center)) < quad_all and abs(math.log(1 + need_center)) < 0.20, "B1 the shift needed to remove the tension is INSIDE the systematic budget (measured full budget and MLS16's 20%); the tension is not evidence against Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2)")
check(pert["ALL distances x 1.0831 (ladder biased if H0 = 67.4)"]["dln"] < math.log(1 + need_center) * 0.95, "B2 a single systematic (rescaling all SPARC distances by the H0 ratio) is by itself as large as the needed shift (>= 95% of it)")
res["need"] = dict(center=need_center, one_sigma=need_1s, two_sigma=need_2s, budget_quad_ind=quad_ind, budget_quad_all=quad_all, frac=frac)
print("   The other side of the ledger: the same systematics, applied the other way, would push Omega_pred UP; and the IF choice alone spans "
      f"Omega_pred = {res['worlds']['RAR (MLS16)']['pub']:.2f}-{res['worlds']['standard']['pub']:.2f}.  The 'prediction' Omega_Lambda inherits twice the fractional error of a0.")
json.dump(res, open("v04_results.json", "w"), indent=1, default=float)
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
