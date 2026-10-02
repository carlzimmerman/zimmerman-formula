#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG288 POST-HOC (written AFTER the first seeding run, after C-FLUID and C-EARLY FAILED) -- WHERE THE CAMB-FLUID SYSTEMATIC LIVES, AND
A DIFFERENTIAL COMPARISON THAT CANCELS IT.  NOTHING HERE CHANGES A FROZEN VERDICT.

The frozen seeding run (cfg288_seeding_camb.py) found that CAMB's DarkEnergyFluid carrying "Lambda + dust at all times" (cs2 = 0) does not
reproduce real CDM to the frozen 0.1% in the LENSED spectra (TT 0.40%, EE 0.56% over 2 <= l <= 2500), so by the frozen rule no seeding
row may be rated INDISTINGUISHABLE and z_req is undefined.  This script, labelled POST-HOC throughout:
  D1  locates the systematic: unlensed TT/EE, lensed TT/EE and the lensing potential C_L^phiphi, fluid vs CDM, in l bands, at the frozen
      settings; plus the lensing-potential deviation at AccuracyBoost 1 and 2 (does it move with numerical accuracy?).
  D2  a differential comparison for every z_seed (H0 fixed, comparison (a)):
        (i)  UNLENSED seeded vs UNLENSED CDM reference (valid if the fluid passes 0.1% unlensed: check PH1);
        (ii) LENSED seeded vs LENSED fluid baseline (the same CAMB fluid with dust at all times: the late-time behaviour is identical, so
             the fluid's late-time systematic cancels).
      The frozen thresholds (1% / 0.1% on S_TT over 30 <= l <= 1000) are applied to these statistics only as a POST-HOC READING.
The frozen verdicts stand as frozen.  kappa = 1/2 FITTED.  The cold mass is still required.  Not a likelihood fit.
Run: python3 campaign_fresh_gravity/CFG288_one_field_dark_sector/cfg288_seeding_posthoc_instrument.py
"""
import sys
sys.dont_write_bytecode = True
import os, io, math, json, time, hashlib, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C

SLUG = "cfg288_seeding_posthoc_instrument_POSTHOC"
R = C.Report(SLUG, False)
P, check, num = R.P, R.check, R.num
T0 = time.time()
P(__doc__.split("Run: python3")[0].strip())
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(os.path.join(HERE, 'FROZEN_CRITERIA.md'), 'rb').read()).hexdigest()}")

# the frozen seeding script's model machinery, exec'd read-only (everything before its reference section)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
SRC = os.path.join(HERE, "cfg288_seeding_camb.py")
_src = open(SRC).read()
g = {"__file__": SRC, "__name__": "cfg288_seeding_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index("# ================================================================================================ reference + controls")],
                 "cfg288_seeding_camb.py", "exec"), g)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
camb, make_params, maxdev, H0REF, LMAX = g["camb"], g["make_params"], g["maxdev"], g["H0REF"], g["LMAX"]
P(f"  machinery: exec'd read-only from cfg288_seeding_camb.py (whole-file sha256 {hashlib.sha256(open(SRC, 'rb').read()).hexdigest()})")


def spectra(p):
    res = camb.get_results(p)
    s = res.get_cmb_power_spectra(p, CMB_unit="muK", spectra=["lensed_scalar", "unlensed_scalar", "lens_potential"])
    return dict(TT=s["lensed_scalar"][:LMAX + 1, 0], EE=s["lensed_scalar"][:LMAX + 1, 1], TTu=s["unlensed_scalar"][:LMAX + 1, 0],
                EEu=s["unlensed_scalar"][:LMAX + 1, 1], PP=s["lens_potential"][:LMAX + 1, 0])


# ================================================================================================ D1
R.banner("D1  WHERE THE CAMB-FLUID SYSTEMATIC LIVES (fluid with dust at all times vs real CDM, frozen settings)")
pr, _ = make_params(H0REF, "ref"); REF = spectra(pr)
pf, _ = make_params(H0REF, "fluid"); FL = spectra(pf)
BANDS = ((2, 29), (30, 300), (301, 1000), (1001, 1600), (1601, 2500))
D1 = {}
for key, lab in (("TTu", "unlensed TT"), ("EEu", "unlensed EE"), ("TT", "lensed TT"), ("EE", "lensed EE"), ("PP", "C_L^phiphi")):
    D1[lab] = {f"{a}-{b}": maxdev(FL[key], REF[key], a, b) for a, b in BANDS}
    P(f"    {lab:12s} max |d/ref| per band: " + "; ".join(f"{k} {v:.2e}" for k, v in D1[lab].items()))
num("D1_bands", D1)
u_tt = maxdev(FL["TTu"], REF["TTu"], 2, LMAX); u_ee = maxdev(FL["EEu"], REF["EEu"], 2, LMAX)
check("PH1 [post-hoc diagnostic] the fluid reproduces CDM in the UNLENSED TT and EE to <= 0.1% over 2 <= l <= 2500 (the unlensed comparison "
      "is then a valid instrument)", f"unlensed TT {u_tt:.2e}, EE {u_ee:.2e}", u_tt <= 1e-3 and u_ee <= 1e-3, load_bearing=True)
pp500 = FL["PP"][500] / REF["PP"][500] - 1
check("PH2 [post-hoc diagnostic] the failure is in the late-time clustering: C_L^phiphi of the fluid deviates by >= 1% at L = 500",
      f"C_500^phiphi fluid/CDM - 1 = {pp500:+.3e}", abs(pp500) >= 1e-2, load_bearing=False)
# accuracy dependence of the lensing-potential deviation
ACC = {}
for acc in (1.0, 2.0):
    out = []
    for kind in ("ref", "fluid"):
        p, _ = make_params(H0REF, kind)
        p.Accuracy.AccuracyBoost = acc; p.Accuracy.lSampleBoost = acc; p.Accuracy.lAccuracyBoost = acc
        out.append(spectra(p))
    ACC[str(acc)] = {f"L{L}": float(out[1]["PP"][L] / out[0]["PP"][L] - 1) for L in (100, 500, 1500)}
    P(f"    AccuracyBoost {acc}: C_L^phiphi fluid/CDM - 1 at L = 100 / 500 / 1500: " + " / ".join(f"{v:+.3e}" for v in ACC[str(acc)].values()))
num("D1_accuracy_dependence", ACC)
P(f"    {R.el()}")

# ================================================================================================ D2
R.banner("D2  DIFFERENTIAL COMPARISON (H0 fixed): unlensed seeded vs unlensed CDM; lensed seeded vs lensed fluid baseline")
ROWS = {}
for zs in (1100.0, 3400.0, 1e4, 1e5, 1e6, 1e7):
    p, info = make_params(H0REF, "seed", zs)
    S = spectra(p)
    r = dict(
        S_TT_unl_vs_CDM=maxdev(S["TTu"], REF["TTu"], 30, 1000), S_EE_unl_vs_CDM=maxdev(S["EEu"], REF["EEu"], 30, 1000),
        S_TT_unl_vs_CDM_2_2500=maxdev(S["TTu"], REF["TTu"], 2, LMAX),
        S_TT_len_vs_fluid=maxdev(S["TT"], FL["TT"], 30, 1000), S_EE_len_vs_fluid=maxdev(S["EE"], FL["EE"], 30, 1000),
        S_TT_len_vs_fluid_2_2500=maxdev(S["TT"], FL["TT"], 2, LMAX), S_EE_len_vs_fluid_2_2500=maxdev(S["EE"], FL["EE"], 2, LMAX),
        S_TT_unl_vs_fluid=maxdev(S["TTu"], FL["TTu"], 30, 1000))
    def reading(x):
        return "EXCLUDED" if x > 1e-2 else ("INDISTINGUISHABLE" if x <= 1e-3 else "UNDECIDED")
    r["posthoc_reading_unl_vs_CDM"] = reading(r["S_TT_unl_vs_CDM"])
    r["posthoc_reading_len_vs_fluid"] = reading(r["S_TT_len_vs_fluid"])
    ROWS[f"{zs:g}"] = r
    P(f"    z_seed {zs:>8g}: unlensed vs CDM S_TT {r['S_TT_unl_vs_CDM']:.3e} (S_EE {r['S_EE_unl_vs_CDM']:.2e}; 2-2500 {r['S_TT_unl_vs_CDM_2_2500']:.2e}) "
          f"-> {r['posthoc_reading_unl_vs_CDM']};  lensed vs fluid baseline S_TT {r['S_TT_len_vs_fluid']:.3e} (S_EE {r['S_EE_len_vs_fluid']:.2e}; "
          f"2-2500 TT {r['S_TT_len_vs_fluid_2_2500']:.2e}, EE {r['S_EE_len_vs_fluid_2_2500']:.2e}) -> {r['posthoc_reading_len_vs_fluid']}   {R.el()}")
num("D2_rows", ROWS)
c7 = ROWS["1e+07"]
check("PH3 [post-hoc instrument] the 1e7 control is clean in the differential statistics: unlensed vs CDM and lensed vs fluid baseline both "
      "<= 0.1% over 2 <= l <= 2500", f"unlensed TT vs CDM {c7['S_TT_unl_vs_CDM_2_2500']:.2e}; lensed TT/EE vs fluid {c7['S_TT_len_vs_fluid_2_2500']:.2e} / "
      f"{c7['S_EE_len_vs_fluid_2_2500']:.2e}",
      c7["S_TT_unl_vs_CDM_2_2500"] <= 1e-3 and c7["S_TT_len_vs_fluid_2_2500"] <= 1e-3 and c7["S_EE_len_vs_fluid_2_2500"] <= 1e-3, load_bearing=True)
# the smallest grid z_seed whose post-hoc readings (both statistics) are INDISTINGUISHABLE, with every larger z too
zq = None
for zs in (1100.0, 3400.0, 1e4, 1e5, 1e6):
    later = [ROWS[f"{z:g}"] for z in (1100.0, 3400.0, 1e4, 1e5, 1e6) if z >= zs]
    if all(x["posthoc_reading_unl_vs_CDM"] == "INDISTINGUISHABLE" and x["posthoc_reading_len_vs_fluid"] == "INDISTINGUISHABLE" for x in later):
        zq = zs; break
P(f"\n    POST-HOC z_req analogue (smallest grid z_seed with both differential readings INDISTINGUISHABLE, and every larger one too): {zq}")
P("    This is a post-hoc reading only.  The frozen rule leaves z_req undefined (the frozen lensed controls failed).")
num("posthoc_zreq", zq)
P(f"\n  run time {time.time() - T0:.0f} s.  POST-HOC; no frozen verdict changed.  kappa = 1/2 FITTED; the cold mass is still required.")
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
