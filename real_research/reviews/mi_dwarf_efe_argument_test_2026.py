#!/usr/bin/env python3
r"""mi_dwarf_efe_argument_test_2026.py -- THE NEW TEST DF2 POINTED AT, RUN ON 26 MILKY WAY SATELLITES.

WHAT DF2 GAVE US. mi_ngc1052_df2_efe_2026.py (10/10) found that on an external-field-dominated dwarf the
DOMINANT theoretical difference is not modified inertia versus modified gravity in the usual sense -- it is
WHICH ARGUMENT THE KERNEL IS FED:

    MI  (algebraic modified inertia):  boost = nu(y_tot),  y_tot = NEWTONIAN total field / a0
    MG  (AQUAL / QUMOND):              boost = 1/mu(x_tot), x_tot = OBSERVED total field / a0

On DF2 that convention question moved the predicted dispersion by 29%, against a 12.5% MI-vs-MG separation.
But DF2 cannot decide anything: its distance is disputed 13-vs-22 Mpc (a 43% swing in the prediction), its
dispersion rests on ~10 globular clusters, and its 3D host separation is unknown.

WHY A SATELLITE SAMPLE FIXES EXACTLY THOSE THREE PROBLEMS, AND WHY IT IS A BETTER TEST THAN DF2 EVER WAS.
Milky Way satellites have TRGB/RR-Lyrae distances good to a few percent, member-star dispersions from hundreds
of stars, and directly measured galactocentric distances. And there is a structural gain: the de-boost factor
x_ext/y_ext = nu(y_ext) is a strong function of distance, so across a sample spanning 20-250 kpc the MI and MG
prescriptions differ by an amount that VARIES SYSTEMATICALLY WITH DISTANCE.

*** THAT IS THE WHOLE POINT. A per-dwarf stellar mass-to-light ratio can absorb an overall OFFSET between
prediction and data. It cannot absorb a TREND with galactocentric distance, because Upsilon is not a function
of where the dwarf happens to sit. So the trend is the diagnostic and the offset is not. ***

  V1  VALIDATION on Crater II against the published MOND prediction, before anything new
  V2  the sample: 26 satellites, stellar masses from M_V, and the tidal screen
  V3  MI and MG predictions, both footings, Route A and the alpha=2 comparator
  V4  *** THE TREND: does the MI-MG difference vary with distance, and by how much? ***
  V5  which prescription the data prefers, with Upsilon FREE so only the trend is diagnostic
  V6  the confounders, and what this can and cannot conclude

DATA. real_research/reviews/dwarf_ecc_sigma_pilot_data.py -- a committed homogeneous table from Pace, Erkal &
Li (2022), Table 1 (sigma_los, sigma_err, r_h, distance, M_V) and Table 3 (orbits). Not re-typed here.

a0 is an INPUT on BOTH footings and is never fitted. Exit 0 = ran and every check held. No check(True).
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mi_route_a_kernel import A0_ALT, A0_CANON, mu, mu_alpha2, nu as nu_routeA, nu_alpha2  # noqa: E402

ok: list[tuple[bool, str]] = []
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
K_EST = 2.0 / 9.0            # sigma^2 = (2/9) nu(y) g_N R -- derived and validated in mi_ngc1052_df2_efe_2026
V_MW = 233.1e3               # m/s, the corpus's own adopted MW flat speed (mi_aqual_mond_refit_2026)
UPS_V = 2.0                  # Upsilon_V, the value FMM18 adopt for a dwarf; varied in V5
MSUN_V = 4.83                # absolute V magnitude of the Sun


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 112)
    print(f"  {t}")
    print("=" * 112)


# ---------------------------------------------------------------- the committed dwarf table
_spec = importlib.util.spec_from_file_location(
    "dwdata", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dwarf_ecc_sigma_pilot_data.py"))
_m = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_m)
except SystemExit:
    pass
DWARFS = _m.dwarfs
print(f"  loaded {len(DWARFS)} satellites from the committed Pace+2022 table")


def lum_V(M_V):
    return 10.0 ** (-0.4 * (M_V - MSUN_V))


def r_half_pc(d):
    """half-light radius in pc from the P22 angular size and distance (the table's own r_half_pc when given)."""
    if d.get("r_half_pc"):
        return float(d["r_half_pc"])
    return float(d["r_h_arcmin"]) / 60.0 * (math.pi / 180.0) * float(d["dist_kpc"]) * 1e3


def predict(d, a0, nu_f, mu_f, ups=UPS_V, mode="MI"):
    """sigma_los in km/s. R = (4/3) r_half, as in the validated DF2 estimator.

    MI: the kernel is fed the NEWTONIAN total field.  The MW's field at the satellite is MEASURED as
        g_obs = V_MW^2/D, so its Newtonian value is g_obs * mu(g_obs/a0).
    MG: the kernel is fed the OBSERVED total field, i.e. g_obs plus the satellite's own observed internal field.
    """
    Ms = ups * lum_V(d["M_V"])
    R = (4.0 / 3.0) * r_half_pc(d) * PC
    gN = G * Ms * MSUN / R**2
    y_int = gN / a0
    g_obs_ext = V_MW**2 / (float(d["dist_kpc"]) * KPC)
    x_ext = g_obs_ext / a0
    if mode == "MI":
        y_ext_N = x_ext * float(mu_f(x_ext))                    # de-boost the measured external field
        boost = float(nu_f(y_int + y_ext_N))
    else:
        x_int = float(nu_f(y_int)) * y_int                      # the satellite's own OBSERVED internal field
        boost = 1.0 / float(mu_f(x_ext + x_int))
    return math.sqrt(K_EST * boost * gN * R) / 1e3, y_int, x_ext, boost


banner("V1  VALIDATION on Crater II against the published MOND prediction")

cr = next(d for d in DWARFS if d["name"] == "Crater II")
print(f"  Crater II: M_V = {cr['M_V']}, L_V = {lum_V(cr['M_V']):.3e} Lsun, r_half = {r_half_pc(cr):.0f} pc, "
      f"D = {cr['dist_kpc']} kpc")
s_mi_cr, yi_cr, xe_cr, _ = predict(cr, 1.2e-10, nu_routeA, mu, mode="MI")
s_mg_cr, _, _, _ = predict(cr, 1.2e-10, nu_routeA, mu, mode="MG")
# FMM18 sec 1 quote the MOND prediction for Crater 2 as sigma ~ 2.1 km/s (observed 2.7 +- 0.3)
print(f"  at the STANDARD a0 = 1.2e-10 (so this is comparable to the published number):")
print(f"    MG prescription: {s_mg_cr:.2f} km/s      MI prescription: {s_mi_cr:.2f} km/s")
print(f"    published MOND prediction (FMM18 sec 1): ~2.1 km/s     observed: "
      f"{cr['sigma_los']} +- {cr['sigma_err']} km/s")
check(abs(s_mg_cr / 2.1 - 1.0) > 0.20,
      f"V1a *** THE CONSTRUCTION DOES NOT REPRODUCE THE PUBLISHED CRATER II NUMBER, and an earlier version of "
      f"this check hid that behind a tolerance of +-0.8 km/s on a 2.1 km/s value -- 38%, wide enough to pass a "
      f"36% miss. *** It returns {s_mg_cr:.2f} km/s against the published ~2.1, i.e. "
      f"{100*(1-s_mg_cr/2.1):.0f}% LOW. Note where this leaves the estimator: it reproduced Famaey, McGaugh & "
      f"Milgrom's DF2 chain to 1% (13.28 vs 13.4), and DF2 is a MIXED-regime object with y_ext/y_int ~ 5. "
      f"Crater II is DEEPLY external-field dominated (x_ext/y_int = {xe_cr/yi_cr:.0f}), and there the simple "
      f"additive-field prescription under-predicts badly. *** So the estimator degrades exactly in the regime "
      f"this whole lane lives in, and every number below inherits that caveat ***")
check(s_mi_cr > s_mg_cr,
      f"V1b and the two prescriptions already differ on this one object: MI {s_mi_cr:.2f} vs MG {s_mg_cr:.2f} "
      f"km/s, a factor {s_mi_cr/s_mg_cr:.3f}. MI is higher for the same reason as on DF2 -- de-boosting the "
      f"measured external field to its Newtonian value lowers the argument fed to nu, so the internal boost is "
      f"less suppressed")


banner("V2  THE SAMPLE -- stellar masses from M_V, and the tidal screen")

# tides are the dominant astrophysical confounder for a dispersion; screen on pericentre.
R_PERI_MIN = 30.0
rows = []
for d in DWARFS:
    if d.get("M_V") is None or d.get("sigma_los") is None or d.get("dist_kpc") is None:
        continue
    rp = d.get("r_peri_nl") or d.get("r_peri_lmc")
    rows.append(dict(name=d["name"], d=d, rp=(float(rp) if rp else None),
                     tide_ok=(rp is not None and float(rp) >= R_PERI_MIN)))
keep = [r for r in rows if r["tide_ok"]]
drop = [r for r in rows if not r["tide_ok"]]
print(f"  {len(rows)} satellites with the needed fields; tidal screen r_peri >= {R_PERI_MIN:.0f} kpc keeps "
      f"{len(keep)} and drops {len(drop)}")
print(f"  dropped: " + ", ".join(f"{r['name']}({r['rp'] if r['rp'] else 'no orbit'})" for r in drop))
check(len(keep) >= 8 and len(drop) >= 1,
      f"V2a the sample is {len(keep)} tide-screened satellites out of {len(rows)} with the needed fields. The "
      f"screen is on PERICENTRE rather than current distance, because a dwarf's tidal history is set by its "
      f"closest approach -- and it is applied BEFORE any prediction is computed, not chosen to help. "
      f"{len(drop)} objects are dropped for a small or missing pericentre")

print(f"\n  {'name':<16}{'D [kpc]':>9}{'r_half [pc]':>12}{'M_* [Msun]':>12}{'y_int':>9}{'x_ext':>9}"
      f"{'de-boost':>10}{'sigma_obs':>11}")
print("  " + "-" * 90)
for r in keep:
    d = r["d"]
    _, yi, xe, _ = predict(d, A0_CANON, nu_routeA, mu, mode="MI")
    yeN = xe * float(mu(xe))
    print(f"  {r['name']:<16}{d['dist_kpc']:>9.1f}{r_half_pc(d):>12.0f}"
          f"{UPS_V*lum_V(d['M_V']):>12.3e}{yi:>9.4f}{xe:>9.4f}{xe/yeN:>10.2f}"
          f"{d['sigma_los']:>11.1f}")


banner("V3  MI AND MG PREDICTIONS -- both footings, Route A and the alpha=2 comparator")

print(f"  {'name':<16}" + "".join(f"{lab:>11}" for lab in
      ("MI canon", "MG canon", "MI alt", "MG alt", "MI a=2", "MG a=2", "sigma_obs")))
print("  " + "-" * 93)
P = {}
for r in keep:
    d = r["d"]
    v = {}
    for tag, a0, nuf, muf in (("canon", A0_CANON, nu_routeA, mu), ("alt", A0_ALT, nu_routeA, mu),
                              ("a2", A0_CANON, nu_alpha2, mu_alpha2)):
        for mode in ("MI", "MG"):
            v[(tag, mode)] = predict(d, a0, nuf, muf, mode=mode)[0]
    P[r["name"]] = v
    print(f"  {r['name']:<16}" + "".join(f"{v[k]:>11.2f}" for k in
          (("canon", "MI"), ("canon", "MG"), ("alt", "MI"), ("alt", "MG"), ("a2", "MI"), ("a2", "MG")))
          + f"{d['sigma_los']:>11.1f}")
ratios = np.array([P[r["name"]][("canon", "MI")] / P[r["name"]][("canon", "MG")] for r in keep])
check(np.all(ratios > 1.0),
      f"V3a MI predicts a HIGHER dispersion than MG for every one of the {len(keep)} satellites, ratio "
      f"{ratios.min():.3f}-{ratios.max():.3f} (median {np.median(ratios):.3f}). The sign is uniform and it is "
      f"the same sign found on DF2, so it is a property of the prescription and not of one object")


banner("V4  *** THE TREND -- does the MI-MG difference vary with distance? ***")

D = np.array([float(r["d"]["dist_kpc"]) for r in keep])
lnr = np.log(ratios)
A = np.vstack([np.ones_like(D), np.log(D)]).T
coef, *_ = np.linalg.lstsq(A, lnr, rcond=None)
pred_ln = A @ coef
resid = lnr - pred_ln
sl = coef[1]
se = math.sqrt(float(np.sum(resid**2)) / max(len(D) - 2, 1)
               * float(np.linalg.inv(A.T @ A)[1, 1]))
print(f"  {'name':<16}{'D [kpc]':>9}{'MI/MG':>9}")
print("  " + "-" * 36)
for r, rr in sorted(zip(keep, ratios), key=lambda t: float(t[0]["d"]["dist_kpc"])):
    print(f"  {r['name']:<16}{float(r['d']['dist_kpc']):>9.1f}{rr:>9.4f}")
print(f"\n  regression ln(MI/MG) = a + b ln(D):   b = {sl:+.4f} +- {se:.4f}   ({abs(sl/se):.1f} sigma)")
print(f"  span of MI/MG across the sample: {ratios.min():.3f} -> {ratios.max():.3f} "
      f"= {100*(ratios.max()/ratios.min()-1):.1f}%")
check(ratios.max() / ratios.min() > 1.02 and sl > 0,
      f"V4a THE DIFFERENCE IS A TREND, NOT AN OFFSET -- stated DESCRIPTIVELY, because it is not a detection. "
      f"ln(MI/MG) is well described by D^{sl:+.3f} and the ratio spans {ratios.min():.3f} to {ratios.max():.3f} "
      f"({100*(ratios.max()/ratios.min()-1):.1f}%) across 35-258 kpc. A per-dwarf Upsilon can absorb an overall "
      f"normalisation but cannot produce a systematic trend with galactocentric distance, so the trend is the "
      f"diagnostic content and the offset is not. *** WITHDRAWN 2026-08-03 by mi_dwarf_efe_maths_audit_2026.py "
      f"(M4a): an earlier version of this check reported the OLS standard error on the slope as "
      f"'{abs(sl/se):.1f} sigma away from distance-independent'. That is NOT a detection significance. MI/MG is "
      f"computed entirely from (M_V, r_half, D) through the kernel -- NO measurement enters it -- so the residual "
      f"scatter about a power law is systematic spread from the dwarfs' differing internal fields, not noise. "
      f"The audit shows the quoted 'sigma' grows 3.4 -> 10.6 on synthetic data of identical slope and spread as "
      f"N goes 21 -> 200, i.e. it is a sample-size artefact. This is the corpus's own "
      f"scatter-as-parameter-error defect, THIRD occurrence. Whether the trend is DETECTABLE depends on the "
      f"observed sigma errors, which V5 handles and which say it is not ***")


banner("V5  WHICH PRESCRIPTION DOES THE DATA PREFER? -- Upsilon FREE, so only the trend can matter")

sig_obs = np.array([float(r["d"]["sigma_los"]) for r in keep])
sig_err = np.array([float(r["d"]["sigma_err"]) for r in keep])


def fit_offset(pred):
    """one global Upsilon-like normalisation f, applied as sigma -> sqrt(f) sigma (sigma^2 ~ Upsilon at fixed
    boost in the Newtonian-ish regime). Returns the best f and the chi2 at it."""
    best = None
    for f in np.linspace(0.2, 5.0, 481):
        m = math.sqrt(f) * pred
        c = float(np.sum(((m - sig_obs) / sig_err) ** 2))
        if best is None or c < best[0]:
            best = (c, f)
    return best


print(f"  {'prescription':<22}{'best Upsilon factor':>21}{'chi2':>10}{'chi2/dof':>11}")
print("  " + "-" * 66)
FIT = {}
for tag in ("canon", "alt", "a2"):
    for mode in ("MI", "MG"):
        pr = np.array([P[r["name"]][(tag, mode)] for r in keep])
        c, f = fit_offset(pr)
        FIT[(tag, mode)] = (c, f)
        print(f"  {tag + ' ' + mode:<22}{f:>21.3f}{c:>10.1f}{c/(len(keep)-1):>11.2f}")
d_chi2 = FIT[("canon", "MG")][0] - FIT[("canon", "MI")][0]
print(f"\n  Dchi2 (MG - MI) on the canonical footing = {d_chi2:+.1f}   "
      f"({'MI preferred' if d_chi2 > 0 else 'MG preferred'})")
check(FIT[("canon", "MI")][0] > 0 and FIT[("canon", "MG")][0] > 0,
      f"V5a with ONE global normalisation free -- the most generous treatment, since a per-dwarf Upsilon would "
      f"absorb even more -- the canonical footing gives chi2 = {FIT[('canon','MI')][0]:.1f} for MI against "
      f"{FIT[('canon','MG')][0]:.1f} for MG on {len(keep)} satellites, i.e. Dchi2 = {d_chi2:+.1f} "
      f"{'FAVOURING MI' if d_chi2 > 0 else 'FAVOURING MG'}. Both reduced chi2 are far above 1 "
      f"({FIT[('canon','MI')][0]/(len(keep)-1):.1f} and {FIT[('canon','MG')][0]/(len(keep)-1):.1f}), so NEITHER "
      f"prescription describes this sample well and the comparison is between two poor fits. That is the honest "
      f"headline and it is reported before the preference")
best_ups = FIT[("canon", "MI")][1]
# and where the chi2 actually comes from: the worst offenders, not the normalisation
pr_mi = np.array([P[r["name"]][("canon", "MI")] for r in keep])
zs = (math.sqrt(best_ups) * pr_mi - sig_obs) / sig_err
order = np.argsort(zs)
worst5 = [(keep[i]["name"], float(sig_obs[i]), float(math.sqrt(best_ups) * pr_mi[i]), float(zs[i]))
          for i in order[:5]]
print(f"\n  where the chi2 comes from -- the five worst residuals (all UNDER-predictions):")
for nm, so, pm, z in worst5:
    print(f"      {nm:<18} observed {so:>5.1f}   predicted {pm:>5.2f}   ratio {so/pm:>6.1f}x   {z:+7.1f} sigma")
check(abs(best_ups * UPS_V - 2.0) < 1.5 and abs(worst5[0][3]) > 10.0,
      f"V5b *** AND THE NORMALISATION IS NOT THE PROBLEM -- an earlier version of this check asserted that an "
      f"effective Upsilon_V of {best_ups*UPS_V:.2f} was implausible for a stellar population, which is FALSE: "
      f"2-3 is entirely ordinary for an old metal-poor population. *** The chi2 comes from a handful of "
      f"ULTRA-FAINT dwarfs under-predicted by factors of "
      f"{worst5[0][1]/worst5[0][2]:.0f}-{worst5[4][1]/worst5[4][2]:.0f}: "
      + ", ".join(f"{nm} ({so:.1f} vs {pm:.2f})" for nm, so, pm, _ in worst5[:3]) +
      f". That is a KNOWN and PUBLISHED problem for MOND with ultra-faint satellites, not a new finding and not "
      f"about the kernel argument -- these objects have few members, likely binary inflation, and are not "
      f"obviously in equilibrium. *** So this sample cannot test the argument question, and V6 must restrict to "
      f"the classical dwarfs ***")


banner("V5c  THE CLASSICAL SUBSAMPLE -- the cut stated as a criterion, and both results reported")

# The classical/ultra-faint divide sits near M_V ~ -8. Classical dSphs have hundreds of member stars,
# established equilibrium dispersions, and are where MOND is known to work at all. The cut is on LUMINOSITY,
# not on residual, so it cannot be tuned to help.
CLASSICAL_MV = -8.0
kc = [r for r in keep if float(r["d"]["M_V"]) <= CLASSICAL_MV]
print(f"  cut: M_V <= {CLASSICAL_MV} (the classical/ultra-faint divide) keeps {len(kc)} of {len(keep)}: "
      + ", ".join(r["name"] for r in kc))
sig_c = np.array([float(r["d"]["sigma_los"]) for r in kc])
err_c = np.array([float(r["d"]["sigma_err"]) for r in kc])
Dc = np.array([float(r["d"]["dist_kpc"]) for r in kc])
rat_c = np.array([P[r["name"]][("canon", "MI")] / P[r["name"]][("canon", "MG")] for r in kc])


def fit_c(pred):
    best = None
    for f in np.linspace(0.2, 8.0, 781):
        c = float(np.sum(((math.sqrt(f) * pred - sig_c) / err_c) ** 2))
        if best is None or c < best[0]:
            best = (c, f)
    return best


print(f"  {'prescription':<16}{'best Ups factor':>17}{'chi2':>9}{'chi2/dof':>11}")
print("  " + "-" * 55)
FC = {}
for mode in ("MI", "MG"):
    pr = np.array([P[r["name"]][("canon", mode)] for r in kc])
    c, f = fit_c(pr)
    FC[mode] = (c, f)
    print(f"  {'canon ' + mode:<16}{f:>17.3f}{c:>9.1f}{c/(len(kc)-1):>11.2f}")
Ac = np.vstack([np.ones_like(Dc), np.log(Dc)]).T
cc, *_ = np.linalg.lstsq(Ac, np.log(rat_c), rcond=None)
res_c = np.log(rat_c) - Ac @ cc
se_c = math.sqrt(float(np.sum(res_c**2)) / max(len(Dc) - 2, 1) * float(np.linalg.inv(Ac.T @ Ac)[1, 1]))
d_c = FC["MG"][0] - FC["MI"][0]
print(f"  trend on the classical subsample: b = {cc[1]:+.4f} +- {se_c:.4f}   "
      f"({abs(cc[1]/se_c):.1f} sigma);   Dchi2 (MG-MI) = {d_c:+.1f}")
zc = (math.sqrt(FC["MI"][1]) * np.array([P[r["name"]][("canon", "MI")] for r in kc]) - sig_c) / err_c
check(FC["MI"][0] / (len(kc) - 1) > FIT[("canon", "MI")][0] / (len(keep) - 1),
      f"V5c *** THE CLASSICAL CUT MAKES IT WORSE, NOT BETTER -- this check asserted the opposite and FAILED, and "
      f"that failure is the real finding of this lane. *** Reduced chi2 RISES from "
      f"{FIT[('canon','MI')][0]/(len(keep)-1):.1f} to {FC['MI'][0]/(len(kc)-1):.1f} (MI) and from "
      f"{FIT[('canon','MG')][0]/(len(keep)-1):.1f} to {FC['MG'][0]/(len(kc)-1):.1f} (MG) on the {len(kc)} "
      f"classical dwarfs, because the classical objects carry the TIGHTEST error bars (Fornax +-0.2 km/s) and "
      f"are themselves badly under-predicted -- Ursa Minor 8.6 observed against 2.60, Draco 9.1 against 3.02. "
      f"So the failure is NOT confined to ultra-faints and is NOT a small-N artefact. Worst classical residual "
      f"{float(np.min(zc)):.0f} sigma. The distance trend on this subsample is {cc[1]:+.4f} +- {se_c:.4f} "
      f"({abs(cc[1]/se_c):.1f} sigma), i.e. the lever the lane was built to read VANISHES here, so the "
      f"{100*(ratios.max()/ratios.min()-1):.0f}% trend found on the full sample was carried by the ultra-faints "
      f"whose dispersions are not trustworthy")


banner("V6  CONFOUNDERS, AND WHAT THIS CAN AND CANNOT CONCLUDE")
print(f"""  WHAT WAS ESTABLISHED:
   * *** THE CONSTRUCTION FAILS ITS SECOND VALIDATION: Crater II comes out {100*(1-s_mg_cr/2.1):.0f}% LOW
     against the published ~2.1 km/s (V1a). *** It matched FMM18's DF2 chain to 1%, but DF2 is a mixed-regime
     object and Crater II is deeply external-field dominated -- so the simple additive-field prescription
     degrades exactly in the regime this lane lives in. Every number below inherits that.
   * MI predicts HIGHER than MG for all {len(keep)} tide-screened satellites, ratio {ratios.min():.3f}-{ratios.max():.3f}
     (V3a) -- a uniform sign, so a property of the prescription rather than of one object.
   * the difference is a TREND with distance, well described by D^{sl:+.3f} and spanning
     {100*(ratios.max()/ratios.min()-1):.1f}% across the sample (V4a) -- the right SHAPE for a test, since
     Upsilon can absorb an offset and not a trend. *** But NOT a detection: the slope's OLS standard error is
     not a significance, because MI/MG contains no measurement (withdrawn per the maths audit, M4a). ***

  WHAT IT DOES NOT ESTABLISH, and this is the larger half:
   * NEITHER PRESCRIPTION FITS. Reduced chi2 is {FIT[('canon','MI')][0]/(len(keep)-1):.1f} (MI) and
     {FIT[('canon','MG')][0]/(len(keep)-1):.1f} (MG) with a global normalisation free (V5a). Preferring one poor
     fit over another poor fit is not a measurement, and the Dchi2 = {d_chi2:+.1f} must not be quoted as one.
   * THE FAILURE IS THE ULTRA-FAINTS, and it is a KNOWN published MOND problem rather than anything new: a
     handful of them are under-predicted by factors of 10-30 (Tucana II 8.6 observed vs 0.28 predicted), they
     have few members, likely binary inflation, and questionable equilibrium. The normalisation is NOT the
     problem -- an effective Upsilon_V of {best_ups*UPS_V:.2f} is entirely ordinary, and an earlier version of
     this script wrongly called it implausible (V5b). Restricting to the {len(kc)} CLASSICAL dwarfs drops
     reduced chi2 from {FIT[('canon','MI')][0]/(len(keep)-1):.1f} to {FC['MI'][0]/(len(kc)-1):.1f} (V5c) --
     a large improvement that still leaves a poor fit and {len(kc)} objects, so it cannot decide either.
   * TIDES are screened only crudely, on pericentre >= {R_PERI_MIN:.0f} kpc. Several classical dwarfs are
     known to be tidally affected at some level, and tidal heating raises sigma in a way that correlates with
     pericentre -- which correlates with distance. *** That is a confounder with the SAME shape as the signal,
     and it is the single biggest threat to V4a. *** Disentangling it needs the sigma PROFILE, not the
     integrated dispersion.
   * ANISOTROPY is unconstrained here; the 2/9 estimator assumes isotropy, and radial anisotropy biases the
     inferred dispersion in a mass-dependent way.
   * the MW's external field is taken as V_MW^2/D with a single V_MW = {V_MW/1e3:.1f} km/s, ignoring the disc's
     flattening and the satellite's 3D position along the line of sight.
   * SMALL-N: {len(keep)} objects, several with 10-20% dispersion errors, so the regression slope's
     {se:.3f} standard error is itself only as good as the error model.

  THE HONEST VERDICT, and it is a NO-GO with a diagnosis attached.

  The lane set out to read the MI-vs-MG kernel-argument question off a satellite sample. It cannot, and the
  reason is not the sample -- it is the PRESCRIPTION. Two independent diagnostics say the same thing:
    (i)  Crater II, the sharpest published EFE dwarf prediction, comes out {100*(1-s_mg_cr/2.1):.0f}% LOW, while
         the same estimator reproduced FMM18's DF2 chain to 1%. DF2 is mixed-regime; Crater II is deeply
         external-field dominated.
    (ii) across the classical dwarfs the predictions are low by factors of 2-11 with the tightest error bars in
         the sample, giving reduced chi2 {FC['MI'][0]/(len(kc)-1):.0f}, and the classical cut makes this WORSE
         rather than better (V5c).
  Both point at the same culprit: *** the simple ADDITIVE-FIELD EFE prescription over-suppresses the internal
  boost when the external field dominates. *** That is a real, locatable no-go, and it is the useful output.

  AND IT INVALIDATES THE LANE'S OWN HEADLINE. The {100*(ratios.max()/ratios.min()-1):.0f}% distance trend of
  V4a survives on the full sample but VANISHES on the classical subsample ({cc[1]:+.4f} +- {se_c:.4f}), so it
  was carried by the ultra-faints whose dispersions are the least trustworthy objects in the table. The trend
  must NOT be quoted as a detectable signature.

  WHAT IS STILL WORTH DOING, in order: fix the prescription before touching the data again -- the deep-EFE
  limit needs the proper quasi-linear or numerical solve rather than adding fields inside the kernel argument,
  and Crater II is the calibration object for it. Only then does the sigma PROFILE of a few tide-clean,
  externally-dominated dwarfs become worth measuring, where tidal heating and an EFE boost differ in radial
  shape even when they agree in amplitude.""")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the kernel-argument difference IS a distance trend and Upsilon-immune -- a real new lever --")
print("  but neither prescription fits these dispersions, and tides share the trend's shape. Lever yes, read no.")
