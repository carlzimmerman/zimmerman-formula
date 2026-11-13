#!/usr/bin/env python3
"""FRZ3R grading (READING.md sections 3 to 8). Reads parts/*.json; the gate is SHARED MACHINERY: the record's
ss1_cosmo.forest_setup / forest_eval executed read-only (set-up as FRZ1R's frz1r_forest.py: form B's own CLASS reference,
F1A B2 cold fit). Usage: nice -n 19 python3 frz3r_grade.py <footing>  -> frz3r_grade_<footing>.json/.out and
frz3r_grade_<footing>_MUTATE.json/.out.   kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, glob, contextlib, signal, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_factor, cho_solve
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion")
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit")
FRZ1J = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z", "frz1_hm.json")
OUT = []; OUTM = []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
# ------------------------------------------------------------------ shared gate (as FRZ1R)
os.environ["SS1_FOOT"] = FOOT; os.environ.pop("SS1_MUTATE", None)
sys.path.insert(0, SS1); src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_frz3r"}; _a = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = _a
signal.signal(signal.SIGTERM, lambda s, f: sys.exit(143))
Class, KG, ZG, forest_setup, forest_eval = (ns[k] for k in ("Class", "KG", "ZG", "forest_setup", "forest_eval"))
CLIGHT = 299792.458
FD = forest_setup(); md5ok = FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433"
def class_bg(Mx):
    b = Mx.get_background(); z = b['z'][::-1]; Hh = b['H [1/Mpc]'][::-1] * CLIGHT; DM = b['comov. dist.'][::-1]; m = z <= 3600
    return dict(z=z[m], H=Hh[m], DM=DM[m])
pr = json.load(open(os.path.join(F1AD, "parts", f"fit_B2_{FOOT}_cold.json")))["pars"]
MB = Class()
MB.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': ns["LMAX"] + 100, 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
        'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 210.0, 'z_max_pk': ns["ZPK"]})
MB.compute(); BGB = class_bg(MB); HB = pr["h"]; ns["M"] = MB; ns["REFBG"] = BGB
ZB = [float(z) for z in FD["ZB"]]
def amp(Rz_by_bin, kh_grid):
    out = np.empty((len(KG), len(ZG))); kh = KG / HB
    for j, z in enumerate(ZG):
        zb = min(ZB, key=lambda q: abs(q - z)); R = np.interp(np.log(kh), np.log(kh_grid[zb] if isinstance(kh_grid, dict) else kh_grid), np.asarray(Rz_by_bin[zb], float))
        out[:, j] = np.sqrt(np.maximum(R, 0.0))
    return out
cf, lower = FD["CF"]; Uc = np.tril(cf).T if lower else np.triu(cf); COV = Uc.T @ Uc
def dchi2_sel(r, sel):
    d = ((r - 1.0) * FD["Pd"])[sel]; return float(d @ np.linalg.solve(COV[np.ix_(sel, sel)], d))
ALL = np.ones(FD["NB"], bool)
ANCH = (2.2, 3.0, 4.4)
ASEL = np.isin(FD["zs"], ANCH)
def bin_sel(z): return FD["zs"] == round(z, 2)
# ------------------------------------------------------------------ parts
def load(stage, z, N=384):
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "parts", f"{stage}_z{z:.1f}_s*_{FOOT}_N{N}.json"))):
        d = json.load(open(f)); out[d["seed"]] = d
    return out
PARTS = {z: load("anchor", z) for z in ANCH}
for z in ZB:
    if z not in ANCH: PARTS[z] = load("other", z)
RES_ = {z: load("res", z, 256) for z in ANCH}; CLU = {z: load("clustered", z) for z in ANCH}
def RF(parts, tag, wB="BM", wR="R", tagR=None, seeds=None):
    """seed mean of per-seed flux ratios; returns kv, mean, per-seed array."""
    tagR = tagR or tag; S = sorted(parts) if seeds is None else [s for s in seeds if s in parts]
    arr = np.array([np.array(parts[s]["flux"][tag][wB]["p"]) / np.array(parts[s]["flux"][tagR][wR]["p"]) for s in S])
    return np.array(parts[S[0]]["kv"]), arr.mean(0), arr
def r_at_points(kv_by_z, R_by_z, zsel=None):
    r = np.ones(FD["NB"])
    for z in ZB:
        if z not in R_by_z: continue
        s_ = FD["zs"] == round(z, 2); kv = kv_by_z[z][1:]; R = R_by_z[z][1:]
        r[s_] = np.interp(FD["ks"][s_], kv, R)                      # flat at the first mode below the fundamental
    return r
def dchi(kvz, Rz, sel=ALL): return dchi2_sel(r_at_points(kvz, Rz), sel)
RESJ = dict(lane="FRZ3R", footing=FOOT, md5_ok=md5ok, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
# ------------------------------------------------------------------ gate validation
RESJ["gate_R1"] = float(forest_eval(FD, BGB, np.ones((len(KG), len(ZG))))["dchi2"])
F1 = json.load(open(FRZ1J)); KF1 = np.array(F1["k"])
f1R = {z: F1["cases"][f"primary|{FOOT}"][f"{z:.1f}"]["R_cold"] for z in ZB}
RESJ["FRZ1_through_gate"] = float(forest_eval(FD, BGB, amp(f1R, KF1))["dchi2"])
P(f"[{FOOT}] gate: R = 1 -> {RESJ['gate_R1']:.3e}; md5 ok {md5ok}; FRZ1's stored R_cold through the gate -> {RESJ['FRZ1_through_gate']:.1f} (FRZ1 reported 9916.2 / 9008.7)")
# ------------------------------------------------------------------ primary flux level
kvz, RFz, per_seed, nseed = {}, {}, {}, {}
for z in ZB:
    kv, m, arr = RF(PARTS[z], "primary"); kvz[z], RFz[z], per_seed[z], nseed[z] = kv, m, arr, len(arr)
D_flux = dchi(kvz, RFz); D_flux_anch = dchi(kvz, RFz, ASEL)
perbin = {f"{z:.1f}": dchi(kvz, RFz, bin_sel(z)) for z in ZB}
RESJ["flux"] = dict(dchi2=D_flux, dchi2_anchor_bins=D_flux_anch, per_bin=perbin, seeds=nseed)
# matter level of the same fields
def Rpaint(parts, wB="BM"):
    S = sorted(parts); k = np.array(parts[S[0]]["P3D"]["k"])
    arr = np.array([np.array(parts[s]["P3D"][wB]) / np.array(parts[s]["P3D"]["R"]) for s in S]); return k, arr.mean(0)
kp, Rp = {}, {}
for z in ZB:
    k, R = Rpaint(PARTS[z]); m = (k <= 10.0) & np.isfinite(R); kp[z], Rp[z] = k[m], R[m]   # empty low-k bins dropped
D_mat = float(forest_eval(FD, BGB, amp(Rp, kp))["dchi2"])
RESJ["matter_same_fields"] = dict(dchi2=D_mat, softening=D_flux / D_mat if D_mat > 0 else None)
P(f"[{FOOT}] FLUX LEVEL Delta chi^2 (12 bins, 755 points) = {D_flux:.2f} (anchor bins {D_flux_anch:.2f}); matter level, same fields, record projection = {D_mat:.1f}; ratio {D_flux / D_mat:.4g}")
P(f"[{FOOT}] per bin (own block): " + " ".join(f"{k}:{v:.2f}" for k, v in perbin.items()))
# per-z table
tab = {}
for z in ZB:
    kv = kvz[z]; zs = round(z, 2); kmax = 0.5 * math.pi / (CLIGHT * 0.8 / ((1 + z) * 1215.67))
    sel = (kv > 0) & (kv <= kmax)
    def at(x): return float(np.interp(x, kv[1:], RFz[z][1:]))
    tab[f"{z:.1f}"] = dict(R_F_at=dict((f"{x}", at(x)) for x in (0.003, 0.005, 0.01, 0.02, 0.03)), R_F_min=float(RFz[z][sel].min()), R_F_max=float(RFz[z][sel].max()),
                           R_paint_k135=[float(np.exp(np.interp(np.log(x), np.log(kp[z]), np.log(Rp[z])))) for x in (1, 3, 5)],
                           R_FRZ1_k135=[float(np.interp(x, KF1, f1R[z])) for x in (1, 3, 5)], dchi2_bin=perbin[f"{z:.1f}"])
    P(f"[{FOOT}] z {z:.1f}: R_F at k_v 0.003/0.005/0.01/0.02/0.03 s/km " + "/".join(f"{v:.4f}" for v in tab[f'{z:.1f}']['R_F_at'].values())
      + f"; R_paint k 1/3/5 " + "/".join(f"{v:.4f}" for v in tab[f'{z:.1f}']['R_paint_k135']) + " (FRZ1 " + "/".join(f"{v:.4f}" for v in tab[f'{z:.1f}']['R_FRZ1_k135']) + f"); seeds {nseed[z]}")
RESJ["table"] = tab
# per-seed Delta chi^2 on anchor bins
ps = []
for i in range(4):
    Rz = {z: per_seed[z][i] for z in ANCH if per_seed[z].shape[0] > i}
    if len(Rz) == 3: ps.append(dchi(kvz, Rz, ASEL))
RESJ["per_seed_anchor_dchi2"] = ps
P(f"[{FOOT}] per-seed anchor-bin Delta chi^2: " + " ".join(f"{x:.2f}" for x in ps) + f" (seed-mean field {D_flux_anch:.2f})")
# ------------------------------------------------------------------ known answers
KA = {}
# (a)
a_ok = True; a_max = 0.0
for z in ANCH:
    for s, d in PARTS[z].items():
        r = np.array(d["flux"]["KA_a_zero"]["BM0"]["p"]) / np.array(d["flux"]["primary"]["R"]["p"])
        a_max = max(a_max, float(np.max(np.abs(r - 1)))); a_ok &= bool(np.all(r == 1.0))
KA["a"] = dict(max_dev=a_max, exact=a_ok, gate_R1=RESJ["gate_R1"], pass_=bool(a_ok and RESJ["gate_R1"] == 0.0 and md5ok))
# (b)
b_rows = {}; b_ok = True
for z in ANCH:
    for i, x in enumerate((1, 3, 5)):
        rp = tab[f"{z:.1f}"]["R_paint_k135"][i]; rf = tab[f"{z:.1f}"]["R_FRZ1_k135"][i]; tol = 0.01 + 0.25 * abs(rf - 1)
        b_rows[f"z{z} k{x}"] = dict(R_paint=rp, R_FRZ1=rf, diff=rp - rf, tol=tol, ok=bool(abs(rp - rf) <= tol)); b_ok &= abs(rp - rf) <= tol
KA["b"] = dict(rows=b_rows, pass_=bool(b_ok))
# (c)
c_rows = {}; c_ok = True
for z in ANCH:
    d = PARTS[z][0]; kv = np.array(d["kv"]); kmax = 0.5 * math.pi / (CLIGHT * 0.8 / ((1 + z) * 1215.67)); sel = (kv > 0) & (kv <= kmax)
    rf = np.array(d["flux"]["KA_c_thin"]["BM"]["p"]) / np.array(d["flux"]["KA_c_thin"]["R"]["p"])
    rm = np.array(d["gas1d"]["matter_los"]["BM"]) / np.array(d["gas1d"]["matter_los"]["R"])
    dev = np.abs(rf - rm)[sel]; tol = (1e-3 + 0.01 * np.abs(rm - 1))[sel]
    c_rows[f"{z}"] = dict(max_dev=float(dev.max()), worst_margin=float((dev - tol).max()), ok=bool(np.all(dev <= tol)),
                          R_matter_1D_at_0p01=float(np.interp(0.01, kv[1:], rm[1:])), R_thin_at_0p01=float(np.interp(0.01, kv[1:], rf[1:]))); c_ok &= bool(np.all(dev <= tol))
KA["c"] = dict(rows=c_rows, pass_=bool(c_ok))
# (d)
d_max = 0.0
from math import exp
def Fbar(z, s=1.0): return exp(-s * (0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132))
sF = {"Fbar_tau_x0.9": 0.9, "Fbar_tau_x1.1": 1.1}
for coll in (PARTS, RES_, CLU):
    for z, pz in coll.items():
        for s, d in pz.items():
            for tag, fl in d["flux"].items():
                if tag == "KA_c_thin": continue
                for w, v in fl.items():
                    d_max = max(d_max, abs(v["meanF"] - Fbar(z, sF.get(tag, 1.0))))
KA["d"] = dict(max_abs=d_max, pass_=bool(d_max <= 1e-4))
# (e)
e_rows = {}; e_ok = True
for z in ANCH:
    kv = kvz[z]; kmax = 0.5 * math.pi / (CLIGHT * 0.8 / ((1 + z) * 1215.67)); sel = (kv > 0) & (kv <= kmax)
    E = float(np.sqrt(np.mean((RFz[z][sel] - 1) ** 2))); Sm = float(np.sqrt(np.mean((per_seed[z][:, sel].std(0, ddof=1) / math.sqrt(nseed[z])) ** 2)))
    e_rows[f"{z}"] = dict(E=E, S_mean=Sm, ok=bool(Sm <= E / 3)); e_ok &= Sm <= E / 3
KA["e"] = dict(rows=e_rows, pass_=bool(e_ok))
RESJ["known_answers"] = KA
for k, v in KA.items():
    P(f"[{FOOT}] known answer ({k}): {'PASS' if v['pass_'] else 'FAIL'} " + json.dumps({kk: vv for kk, vv in v.items() if kk != 'pass_'})[:600])
# ------------------------------------------------------------------ mutations (anchor bins)
MU = {}
kv1, Rl, _ = RF({z: None for z in []}, "x") if False else (None, None, None)
def anch_dchi(tagB, wB, tagR, wR, coll=PARTS, seeds=None):
    kz, Rz = {}, {}
    for z in ANCH:
        kv, m, _ = RF(coll[z], tagB, wB=wB, wR=wR, tagR=tagR, seeds=seeds); kz[z], Rz[z] = kv, m
    return dchi(kz, Rz, ASEL), Rz
d_m1, _ = anch_dchi("M1_lin", "BM", "M1_lin", "R")
d_m2, _ = anch_dchi("M2_doubled", "BM2", "primary", "R")
MU["M1_saturation_removed"] = dict(dchi2_anchor=d_m1, primary=D_flux_anch, factor=d_m1 / D_flux_anch, bites=bool(max(d_m1 / D_flux_anch, D_flux_anch / d_m1) >= 1.25))
MU["M2_doubled"] = dict(dchi2_anchor=d_m2, primary=D_flux_anch, factor=d_m2 / D_flux_anch, bites=bool(d_m2 / D_flux_anch >= 2.0))
# matter-level anchor value for M1 direction
kz, Rz = {}, {}
RESJ["mutations"] = MU
for k, v in MU.items():
    P(f"[{FOOT}] MUTATE {k}: anchor-bin Delta chi^2 {v['dchi2_anchor']:.2f} vs primary {v['primary']:.2f} (x {v['factor']:.3f}) -> {'bites' if v['bites'] else 'DOES NOT BITE'}", m=True)
# ------------------------------------------------------------------ brackets
BR = {}
def bracket(name, tag, coll=PARTS, tagprim="primary", seeds=None, collprim=PARTS):
    db, _ = anch_dchi(tag, "BM", tag, "R", coll=coll, seeds=seeds)
    dp, _ = anch_dchi(tagprim, "BM", tagprim, "R", coll=collprim, seeds=seeds)
    BR[name] = dict(dchi2_anchor=db, primary_anchor_same_seeds=dp, est_12bin=D_flux * db / dp, seeds=seeds or "all")
for nm, tg in (("lambda_P x 0.5", "lam_x0.5"), ("lambda_P x 2", "lam_x2"), ("lambda_P = 100 proper kpc (record)", "lam_rec"),
               ("gamma 1.2", "gam_1.2"), ("gamma 1.6", "gam_1.6"), ("mean flux tau_eff x 0.9", "Fbar_tau_x0.9"), ("mean flux tau_eff x 1.1", "Fbar_tau_x1.1")):
    bracket(nm, tg)
bracket("peculiar velocities (linear)", "vel", seeds=(0, 1))
if all(len(RES_[z]) for z in ANCH):
    db, _ = anch_dchi("primary", "BM", "primary", "R", coll=RES_, seeds=(0, 1)); dp, _ = anch_dchi("primary", "BM", "primary", "R", seeds=(0, 1))
    BR["resolution N 256"] = dict(dchi2_anchor=db, primary_anchor_same_seeds=dp, est_12bin=D_flux * db / dp, seeds=(0, 1))
else: BR["resolution N 256"] = "NOT COMPUTED"
if all(len(CLU[z]) for z in ANCH):
    db, _ = anch_dchi("primary", "BM", "primary", "R", coll=CLU, seeds=(0, 1)); dp, _ = anch_dchi("primary", "BM", "primary", "R", seeds=(0, 1))
    rpc = {}
    for z in ANCH:
        kc_, rc_ = Rpaint(CLU[z]); mm = np.isfinite(rc_); rpc[f"{z}"] = [float(np.exp(np.interp(np.log(x), np.log(kc_[mm]), np.log(rc_[mm])))) for x in (1, 3, 5)]
    BR["clustered halo placement"] = dict(dchi2_anchor=db, primary_anchor_same_seeds=dp, est_12bin=D_flux * db / dp, seeds=(0, 1), R_paint_k135=rpc)
else: BR["clustered halo placement"] = "NOT COMPUTED"
RESJ["brackets"] = BR
for k, v in BR.items():
    if isinstance(v, str): P(f"[{FOOT}] bracket {k}: {v}"); continue
    P(f"[{FOOT}] bracket {k}: anchor {v['dchi2_anchor']:.2f} (primary same seeds {v['primary_anchor_same_seeds']:.2f}) -> 12-bin estimate {v['est_12bin']:.2f}")
# ------------------------------------------------------------------ plain painting (reported only)
d_p_anch, RzP = anch_dchi("primary", "BP", "primary", "R")
kpp, Rpp = {}, {}
for z in ANCH:
    k, R = Rpaint(PARTS[z], "BP"); m = (k <= 10) & np.isfinite(R); kpp[z], Rpp[z] = k[m], R[m]
mat_p = {z: Rpp[z] for z in ANCH}
# matter level anchor-only comparisons through the record projection need all bins: use anchor-bin selection on r from forest_eval is not exposed; report flux only
RESJ["plain_painting_reported"] = dict(flux_dchi2_anchor=d_p_anch, R_paint_k135={f"{z}": [float(np.exp(np.interp(np.log(x), np.log(kpp[z]), np.log(Rpp[z])))) for x in (1, 3, 5)] for z in ANCH})
P(f"[{FOOT}] plain painting (reported, never graded): anchor-bin flux Delta chi^2 {d_p_anch:.2f}; R_paint k 1/3/5 " + json.dumps(RESJ['plain_painting_reported']['R_paint_k135']))
# gas level (reported)
kz, Rz = {}, {}
for z in ZB:
    S = sorted(PARTS[z]); arr = np.array([np.array(PARTS[z][s]["gas1d"]["gas_primary"]["BM"]) / np.array(PARTS[z][s]["gas1d"]["gas_primary"]["R"]) for s in S])
    kz[z], Rz[z] = kvz[z], arr.mean(0)
RESJ["gas_level_reported"] = dict(dchi2=dchi(kz, Rz))
P(f"[{FOOT}] gas level (1D power of the smoothed gas skewers; reported): Delta chi^2 {RESJ['gas_level_reported']['dchi2']:.2f}")
# floors
fl = []
for z in ZB:
    for s, d in PARTS[z].items():
        for k, v in d.get("floored", {}).items():
            if k.startswith("primary|"): fl.append(v)
RESJ["floored_primary_max_fraction"] = max(fl) if fl else 0.0
P(f"[{FOOT}] floored pixel fraction, primary fields: max {RESJ['floored_primary_max_fraction']:.2e}")
# ------------------------------------------------------------------ label
ka_ok = all(v["pass_"] for v in KA.values()); mu_ok = all(v["bites"] for v in MU.values())
vals = [v["est_12bin"] for v in BR.values() if not isinstance(v, str)]
if not (ka_ok and mu_ok):
    lab = "NO VERDICT"
elif D_flux > 4:
    cross = [k for k, v in BR.items() if not isinstance(v, str) and v["est_12bin"] <= 4]
    lab = "FOREST ROW FAILS AT FLUX LEVEL" + (", FRAGILE (" + "; ".join(cross) + ")" if cross else "")
else:
    cross = [k for k, v in BR.items() if not isinstance(v, str) and v["est_12bin"] > 4]
    lab = "FOREST ROW HOLDS AT FLUX LEVEL (not a pass; a hit awaiting a further independent check)" + (", FRAGILE (" + "; ".join(cross) + ")" if cross else "")
RESJ["label"] = lab; RESJ["known_answers_ok"] = ka_ok; RESJ["mutations_bite"] = mu_ok
P(f"[{FOOT}] LABEL: {lab}; flux {D_flux:.2f}, matter (same fields) {D_mat:.1f}, ratio {D_flux / D_mat:.4g}")
json.dump(RESJ, open(os.path.join(HERE, f"frz3r_grade_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz3r_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(lane="FRZ3R", footing=FOOT, mutations=MU, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing."), open(os.path.join(HERE, f"frz3r_grade_{FOOT}_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz3r_grade_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\n")
