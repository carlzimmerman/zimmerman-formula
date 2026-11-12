#!/usr/bin/env python3
"""FRZ3 grading (FROZEN_CRITERIA.md sections 2 to 5). Reads parts/z*_s*.json. The gate set-up is SHARED MACHINERY copied
from FRZ1R's frz1r_forest.py (the record's ss1_cosmo.forest_eval executed read-only on DESI DR1 P1D, reference = form B's
own CLASS spectrum, F1A B2 cold fit); the flux-level chi^2 uses the same data points and covariance with the ratio
R_F(k_par) applied directly. Usage: nice -n 19 python3 frz3_grade.py <foot>
-> frz3_<foot>.json/.out and frz3_<foot>_MUTATE.json/.out. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_factor, cho_solve
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion")
F1AD = os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit")
FRZ1 = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
OUT = []; OUTM = []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
os.environ["SS1_FOOT"] = FOOT; os.environ.pop("SS1_MUTATE", None)
sys.path.insert(0, SS1); src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_frz3"}; _a = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = _a
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
MB.compute(); BGB = class_bg(MB); HB = pr["h"]
ns["M"] = MB; ns["REFBG"] = BGB
ZB = [round(float(z), 1) for z in FD["ZB"]]; ANCH = [2.2, 3.0, 4.4]
cf, lower = FD["CF"]; Uc = np.tril(cf).T if lower else np.triu(cf); CFULL = Uc.T @ Uc

def sub_fd(zset):
    s_ = np.isin(np.round(FD["zs"], 1), zset)
    return dict(FD, ZB=np.array([z for z in FD["ZB"] if round(float(z), 1) in zset]), zs=FD["zs"][s_], ks=FD["ks"][s_], Pd=FD["Pd"][s_],
                NB=int(s_.sum()), CF=cho_factor(CFULL[np.ix_(s_, s_)]))
FDA = sub_fd(ANCH)
def chi2_ratio(fd, rfun):
    """rfun(z) -> (k grid s/km, ratio); r at each data point linear in k, flat below the first mode."""
    r = np.empty(fd["NB"])
    for z in fd["ZB"]:
        s_ = fd["zs"] == z; kk, rr = rfun(round(float(z), 1)); r[s_] = np.interp(fd["ks"][s_], kk, rr)
    d = (r - 1.0) * fd["Pd"]; return float(d @ cho_solve(fd["CF"], d))
def amp(Rz_by_bin, kh_grid, zbins):
    out = np.empty((len(KG), len(ZG))); kh = KG / HB
    for j, z in enumerate(ZG):
        zb = min(zbins, key=lambda q: abs(q - z)); R = np.interp(np.log(kh), np.log(kh_grid), np.asarray(Rz_by_bin[zb], float))
        out[:, j] = np.sqrt(np.maximum(R, 0.0))
    return out

# ------------------------------------------------------------------ load parts
PT = {}
for fn in sorted(glob.glob(os.path.join(HERE, "parts", "z*_s*.json"))):
    d = json.load(open(fn)); PT.setdefault(round(d["z"], 1), {})[d["seed"]] = d
ZDONE = sorted(PT); P(f"[{FOOT}] parts: " + " ".join(f"z{z}:{sorted(PT[z])}" for z in ZDONE))
RES = dict(lane="FRZ3", footing=FOOT, md5_ok=md5ok, criteria="FROZEN_CRITERIA.md", note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.",
           parts={str(z): sorted(PT[z]) for z in ZDONE})
def kpar(z): return np.array(PT[z][min(PT[z])]["kpar_skm"])
def kmaxz(z): return 0.5 * math.pi / (CLIGHT * 0.8 / ((1 + z) * 1215.67))
def ratio_seeds(z, getB, getR):
    rs = np.array([np.array(getB(PT[z][s]["foot"][FOOT])) / np.array(getR(PT[z][s]["foot"][FOOT])) for s in sorted(PT[z])])
    return rs.mean(0), (rs.std(0, ddof=1) if len(rs) > 1 else np.zeros(rs.shape[1])), rs
def zinterp(table):
    """fill missing bins linearly in z from computed neighbours (criteria section 2)"""
    out = {}
    for z in ZB:
        if z in table: out[z] = table[z]; continue
        lo = max(q for q in table if q < z); hi = min(q for q in table if q > z); w = (z - lo) / (hi - lo)
        out[z] = (table[lo][0], (1 - w) * np.asarray(table[lo][1]) + w * np.asarray(table[hi][1]))
    return out
FILLED = [z for z in ZB if z not in ZDONE]; RES["bins_interpolated_in_z"] = FILLED

# ------------------------------------------------------------------ primary R_F, gas ratio, matter ratio
RF, RG, SC, RFS = {}, {}, {}, {}
for z in ZDONE:
    m, sd, rs = ratio_seeds(z, lambda f: f["flux"]["L"]["P_F"], lambda f: f["flux"]["R"]["P_F"]); RF[z] = (kpar(z), m); SC[z] = sd; RFS[z] = rs
    mg, _, _ = ratio_seeds(z, lambda f: f["P_gas"]["L"], lambda f: f["P_gas"]["R"]); RG[z] = (kpar(z), mg)
RFf, RGf = zinterp(RF), zinterp(RG)
d_flux = chi2_ratio(FD, lambda z: RFf[z]); d_gas = chi2_ratio(FD, lambda z: RGf[z])
pb = {}
for z in ZB:
    fz = sub_fd([z]); pb[f"{z:.1f}"] = dict(flux=chi2_ratio(fz, lambda q: RFf[q]), gas=chi2_ratio(fz, lambda q: RGf[q]))
# matter level: painted 3D ratio, seed mean, record's forest_eval (FRZ1 convention: k <= 10 h/Mpc, flat outside)
pk0 = PT[ZDONE[0]][min(PT[ZDONE[0]])]["foot"][FOOT]; edges = np.array(pk0["Pm_kbins"]); kc = np.sqrt(edges[1:] * edges[:-1]); use = (kc <= 10.0) & (np.array(pk0["Pm_nmodes"]) > 0)   # empty shells (below the box fundamental) dropped
RM = {}
for z in ZDONE:
    m, _, _ = ratio_seeds(z, lambda f: f["Pm"]["L"], lambda f: f["Pm"]["R"]); RM[z] = m
RMf = {z: (RM[z] if z in RM else None) for z in ZB}
for z in FILLED:
    lo = max(q for q in RM if q < z); hi = min(q for q in RM if q > z); w = (z - lo) / (hi - lo); RMf[z] = (1 - w) * RM[lo] + w * RM[hi]
A_mat = amp({z: RMf[z][use] for z in ZB}, kc[use], ZB)
d_mat = float(forest_eval(FD, BGB, A_mat)["dchi2"])
for z in ZB:
    fz = sub_fd([z]); pb[f"{z:.1f}"]["matter"] = float(forest_eval(fz, BGB, A_mat)["dchi2"])
soft = d_flux / d_mat if d_mat > 0 else float("nan")
RES["primary"] = dict(dchi2_flux=d_flux, dchi2_matter_painted=d_mat, dchi2_gas_1d=d_gas, softening=soft, per_bin=pb)
P(f"[{FOOT}] PRIMARY: dchi2 flux {d_flux:.2f}; matter-level (painted, record projection) {d_mat:.2f}; gas 1D {d_gas:.2f}; softening factor {soft:.4f}")
for z in ZB:
    q = pb[f"{z:.1f}"]; P(f"[{FOOT}]   bin {z:.1f}{' (z-interp)' if z in FILLED else ''}: flux {q['flux']:.2f}  matter {q['matter']:.2f}  gas {q['gas']:.2f}")
KT = [0.002, 0.005, 0.01, 0.02, 0.03, 0.04]
tab = {}
for z in ZDONE:
    kk, m = RF[z]; tab[f"{z:.1f}"] = dict(k=[k for k in KT if k <= kmaxz(z)], R_F=[float(np.interp(k, kk, m)) for k in KT if k <= kmaxz(z)],
                                         sd=[float(np.interp(k, kk, SC[z])) for k in KT if k <= kmaxz(z)],
                                         R_gas=[float(np.interp(k, *RG[z])) for k in KT if k <= kmaxz(z)],
                                         R_paint_k135=[float(np.interp(math.log(k), np.log(kc[use]), RM[z][use])) for k in (1, 3, 5)])
    t = tab[f"{z:.1f}"]; P(f"[{FOOT}]   z {z:.1f} R_F at k " + " ".join(f"{k}:{r:.4f}+-{s:.4f}" for k, r, s in zip(t['k'], t['R_F'], t['sd'])) +
                           " | R_gas " + " ".join(f"{r:.4f}" for r in t['R_gas']) + " | R_paint k1/3/5 " + " ".join(f"{r:.4f}" for r in t['R_paint_k135']))
RES["table"] = tab

# ------------------------------------------------------------------ known answers
KA = {}
okA = True
for z in ZDONE:
    for s in PT[z]:
        f = PT[z][s]["foot"][FOOT]; r = np.array(f["KAa_zero_diff"]) / np.array(f["flux"]["R"]["P_F"]); okA &= bool(np.all(r == 1.0))
RA = {z: (kpar(z), ratio_seeds(z, lambda f: f["KAa_zero_diff"], lambda f: f["flux"]["R"]["P_F"])[0]) for z in ZDONE}; RAf = zinterp(RA)
dA = chi2_ratio(FD, lambda z: RAf[z]); okA = okA and dA == 0.0
KA["a_zero_diff"] = dict(exact_one=okA, dchi2=dA, pass_=okA)
fr1 = json.load(open(os.path.join(FRZ1, "frz1_hm.json"))); K1 = np.array(fr1["k"]); rows = []; okB = True
for z in ANCH:
    if z not in RM: okB = False; continue
    Rf = np.array(fr1["cases"]["primary|" + FOOT][f"{z:.1f}"]["R_cold"])
    for k in (1.0, 3.0, 5.0):
        a = float(np.interp(math.log(k), np.log(kc[use]), RM[z][use])); b = float(np.interp(k, K1, Rf)); tol = 0.01 + 0.25 * abs(b - 1); ok = abs(a - b) <= tol; okB &= ok
        rows.append(dict(z=z, k=k, R_paint=a, R_FRZ1=b, tol=tol, pass_=ok))
KA["b_painting"] = dict(rows=rows, pass_=okB)
rows = []; okC = True
for z in ANCH:
    if z not in PT: okC = False; continue
    mt, _, _ = ratio_seeds(z, lambda f: f["thin"]["L"]["P_F"], lambda f: f["thin"]["R"]["P_F"]); kk, mg = RG[z]; sel = kk <= kmaxz(z)
    dev = np.abs(mt - mg)[sel]; tol = (1e-3 + 0.01 * np.abs(mg - 1))[sel]; ok = bool(np.all(dev <= tol)); okC &= ok
    rows.append(dict(z=z, max_dev=float(dev.max()), max_dev_over_tol=float((dev / tol).max()), pass_=ok))
KA["c_thin"] = dict(rows=rows, pass_=okC)
mx = 0.0
for z in ZDONE:
    for s in PT[z]:
        f = PT[z][s]["foot"][FOOT]
        for key in [k for k in f if k.startswith("flux")]:
            for v in f[key].values(): mx = max(mx, abs(v["meanF"] - v["target"]))
KA["d_meanflux"] = dict(max_abs_dev=mx, pass_=bool(mx <= 1e-4))
KA["gate"] = dict(md5_ok=md5ok, R1=float(forest_eval(FD, BGB, np.ones((len(KG), len(ZG))))["dchi2"]))
KA["gate"]["pass_"] = bool(md5ok and KA["gate"]["R1"] == 0.0)
RES["known_answers"] = KA; ka_ok = all(v["pass_"] for v in KA.values())
P(f"[{FOOT}] KA a (diff off): exact 1 {okA}; KA b (painting vs FRZ1): " + " ".join(f"z{r['z']}k{r['k']:.0f} {r['R_paint']:.3f}/{r['R_FRZ1']:.3f}{'' if r['pass_'] else ' FAIL'}" for r in KA['b_painting']['rows'])
  + f" -> {'PASS' if okB else 'FAIL'}; KA c (thin): " + " ".join(f"z{r['z']} {r['max_dev_over_tol']:.3f}" for r in KA['c_thin']['rows']) + f" -> {'PASS' if okC else 'FAIL'}"
  + f"; KA d mean flux max dev {mx:.1e}; gate md5 {md5ok} R1 {KA['gate']['R1']}")

# ------------------------------------------------------------------ scatter
scat = {}; okS = True
for z in ANCH:
    if z not in RF: continue
    kk, m = RF[z]; sel = kk <= kmaxz(z); E = float(np.sqrt(np.mean((m[sel] - 1) ** 2))); S = float(np.sqrt(np.mean(SC[z][sel] ** 2)))
    scat[f"{z:.1f}"] = dict(E=E, S=S, nseeds=len(PT[z])); okS &= S <= E
RES["scatter"] = dict(rows=scat, pass_=okS)
P(f"[{FOOT}] scatter vs effect at anchors: " + " ".join(f"z{k} E {v['E']:.4f} S {v['S']:.4f}" for k, v in scat.items()) + f" -> {'ok' if okS else 'SCATTER > EFFECT'}")

# ------------------------------------------------------------------ anchors: mutations and brackets (3-bin joint block)
def anch(getB, getR):
    t = {}
    for z in ANCH: t[z] = (kpar(z), ratio_seeds(z, getB, getR)[0])
    return chi2_ratio(FDA, lambda z: t[z])
A_matA = float(forest_eval(FDA, BGB, A_mat)["dchi2"])
a_flux = anch(lambda f: f["flux"]["L"]["P_F"], lambda f: f["flux"]["R"]["P_F"])
m1 = anch(lambda f: f["flux"]["L"]["P_tau"], lambda f: f["flux"]["R"]["P_tau"])
m2 = anch(lambda f: f["flux"]["L2x"]["P_F"], lambda f: f["flux"]["R"]["P_F"])
b1 = abs(math.log(m1 / A_matA)) < abs(math.log(a_flux / A_matA)); b2 = m2 > a_flux
MUT = dict(anchor_dchi2_flux=a_flux, anchor_dchi2_matter=A_matA, M1_saturation_removed=dict(dchi2=m1, bites=b1), M2_difference_doubled=dict(dchi2=m2, bites=b2))
P(f"[{FOOT}] MUTATE (anchor bins): flux {a_flux:.2f}, matter {A_matA:.2f}; M1 saturation removed {m1:.2f} -> {'bites' if b1 else 'DOES NOT BITE'}; M2 doubled {m2:.2f} -> {'bites' if b2 else 'DOES NOT BITE'}", m=True)
BR = {}
spec = {"gamma_1.2": ("flux_glo", "L", "R"), "gamma_1.6": ("flux_ghi", "L", "R"), "lambdaP_x0.5": ("flux_lh", "L", "R"), "lambdaP_x2": ("flux_l2", "L", "R"),
        "mmin_1e10": ("flux", "Lmmin", "R"), "reading_V": ("flux", "V", "R"), "remainder_FRZ1R": ("flux", "remnfw", "R")}
for nm, (key, vb, vr) in spec.items():
    a = anch(lambda f, key=key, vb=vb: f[key][vb]["P_F"], lambda f, key=key, vr=vr: f[key][vr]["P_F"])
    est = d_flux * a / a_flux; BR[nm] = dict(anchor_dchi2=a, est_12bin=est, side="FAILS" if est > 4 else "HOLDS")
RES["brackets"] = BR
lab_primary = "FOREST ROW FAILS AT FLUX LEVEL" if d_flux > 4 else "FOREST ROW HOLDS AT FLUX LEVEL"
cross = [nm for nm, v in BR.items() if (v["est_12bin"] > 4) != (d_flux > 4)]
ok_all = ka_ok and okS and b1 and b2
label = (lab_primary + (" (FRAGILE: " + ", ".join(cross) + ")" if cross else "")) if ok_all else "NO VERDICT"
RES.update(label=label, primary_label_before_checks=lab_primary, crossing_brackets=cross, checks_ok=ok_all, mutations=MUT)
P(f"[{FOOT}] brackets (anchor dchi2 -> estimated 12-bin): " + "; ".join(f"{k} {v['anchor_dchi2']:.2f} -> {v['est_12bin']:.1f}" for k, v in BR.items()))
P(f"[{FOOT}] LABEL: {label}  (dchi2 flux {d_flux:.2f}, matter {d_mat:.2f}, softening {soft:.4f})")
json.dump(RES, open(os.path.join(HERE, f"frz3_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz3_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="FRZ3", footing=FOOT, **MUT, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing."), open(os.path.join(HERE, f"frz3_{FOOT}_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz3_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
