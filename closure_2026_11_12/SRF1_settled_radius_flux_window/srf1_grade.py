#!/usr/bin/env python3
"""SRF1 grading (FROZEN_CRITERIA.md fa73352ceb, AMENDMENT_A1 88144763e1). The gate is FRZ3R's grading set-up (frz3r_grade.py up to
its "parts" marker, executed read-only from FRZ3R's folder: the record's ss1_cosmo.forest_setup / forest_eval, DESI DR1 P1D, full
covariance). G2, G3, G4 are read from SRH1's committed srh1_grade.json. Usage: nice -n 19 python3 srf1_grade.py <footing>
-> srf1_grade_<footing>.json/.out and srf1_grade_<footing>_MUTATE.json/.out.  kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob, warnings
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ3R = os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade")
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
FOOT = sys.argv[1]; assert FOOT in ("canonical", "alt")
OUTD = os.environ.get("SRF1_OUT", HERE)          # test runs only; the graded outputs go next to this script
src = open(os.path.join(FRZ3R, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(FRZ3R, "frz3r_grade.py"), "__name__": "frz3r_grade_setup_srf1"}; _a = sys.argv; sys.argv = ["frz3r_grade.py", FOOT]
exec(compile(src[:cut], "frz3r_grade_setup", "exec"), g); sys.argv = _a
FD, forest_eval, BGB, amp, dchi2_sel, ZB, ALL, ASEL, bin_sel, md5ok = (g[k] for k in ("FD", "forest_eval", "BGB", "amp", "dchi2_sel", "ZB", "ALL", "ASEL", "bin_sel", "md5ok"))
sys.path.insert(0, HERE); import srf1_tables as TB
KT = TB.KT; ANCH = (2.2, 3.0, 4.4)
FG = [0.70, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 2.00, 3.00]
fk_ = TB.fkey
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132
SEL = lambda zs: np.isin(FD["zs"], zs)

# ------------------------------------------------------------------ parts
def load(stage, N=384):
    D = {}
    for f in sorted(glob.glob(os.path.join(os.environ.get("SRF1_PARTS", os.path.join(HERE, "parts")), f"{stage}_z*_s*_{FOOT}_N{N}.json"))):
        d = json.load(open(f)); D.setdefault(d["z"], {})[d["seed"]] = d
    return D
PR = load("primary", int(os.environ.get("SRF1_N", "384")))
missing = [z for z in ZB if z not in PR]
assert not missing, f"missing primary bins {missing}"

WMODE = {"m": "frozen"}
IK3 = int(np.searchsorted(TB.KT, 3.0)); _TT = {}
def wratio(d, gr, key):
    """AMENDMENT_A2 reading R: w_g = sum_b E_b s_b / sum_b n_b s_b, s_b the per-halo ta-scope 1h difference at k 3."""
    if d["z"] not in _TT: _TT[d["z"]] = TB.tables(d["z"])[FOOT]
    t = _TT[d["z"]]; b = np.array(gr["bins"]); E = np.array(gr["E"]); n = np.array(d["forced"][str(gr["g"])]["counts"])
    kk = key if key in t["Ub"] else "f1.00"
    UR = t["UbR"][b, IK3]; dU = t["Ub"][kk][b, IK3]; sb = (UR + dU) ** 2 - UR ** 2
    return float((E * sb).sum() / (n * sb).sum())
def est(d, key, spec="primary", what="p", poisson=False):
    """stratified estimate R = 1 + [dP_base + sum_g w_g dP_g] / P_R(base); what = 'p' (1D flux) or 'P3D'."""
    F = d["flux"][spec]; R = np.array(F["base"]["R"][what])
    if poisson: return np.array(F["base"]["BP|" + key][what]) / R
    dP = np.array(F["base"]["B|" + key][what]) - R
    for gr in d["groups"]:
        bx = F.get(f"g{gr['g']}")
        if bx is None: raise KeyError(f"forced box {gr['g']} missing")
        w = gr["w"] if WMODE["m"] == "frozen" else wratio(d, gr, key)
        dP = dP + w * (np.array(bx["B|" + key][what]) - np.array(bx["R"][what]))
    return 1.0 + dP / R

def r_at(kvz, Rz):
    r = np.ones(FD["NB"])
    for z in Rz:
        s_ = FD["zs"] == round(z, 2); r[s_] = np.interp(FD["ks"][s_], kvz[z][1:], Rz[z][1:])
    return r
def dchi(kvz, Rz, sel=ALL): return dchi2_sel(r_at(kvz, Rz), sel)

def flux_curves(key, parts=PR, seeds=None, poisson=False, spec="primary"):
    kvz, Rz = {}, {}
    for z, ps in parts.items():
        S = sorted(ps) if seeds is None else [s for s in sorted(ps) if s in seeds.get(z, ps)]
        kvz[z] = np.array(ps[S[0]]["kv"]); Rz[z] = np.mean([est(ps[s], key, spec, "p", poisson) for s in S], 0)
    return kvz, Rz
def mat_D(key, poisson=False):
    kp, Rp = {}, {}
    for z, ps in PR.items():
        k = np.array(ps[0]["k3d"]); R = np.mean([est(ps[s], key, "primary", "P3D", poisson) for s in sorted(ps)], 0)
        m = (k <= 10) & np.isfinite(R); kp[z], Rp[z] = k[m], R[m]
    return float(forest_eval(FD, BGB, amp(Rp, kp))["dchi2"]), kp, Rp

# ------------------------------------------------------------------ halo model per f (tables)
T = {z: TB.tables(z)[FOOT] for z in ZB}
KKF = np.geomspace(1e-3, 10.0, 260)        # FRZ1's KK (the grid SRH1's and FZS1's numbers were projected from)
def hm_D(key, q):
    Rz = {z: np.interp(np.log(KKF), np.log(KT[1:]), T[z]["spec"][key][q][1:]) for z in ZB}
    return float(forest_eval(FD, BGB, amp(Rz, KKF))["dchi2"])
HMF = sorted(set(TB.SRH1_GRID + FG))
Drec = {fk_(f): hm_D(fk_(f), "Rcold") for f in HMF + [math.inf]}
Dta = {fk_(f): hm_D(fk_(f), "Rta") for f in HMF + [math.inf]}

# ------------------------------------------------------------------ primary table
RES = dict(lane="SRF1", footing=FOOT, criteria="fa73352ceb", amendment="88144763e1", note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
rows = {}
for f in FG + [math.inf]:
    key = fk_(f); kvz, Rz = flux_curves(key); Df = dchi(kvz, Rz)
    Dm, kp, Rp = mat_D(key)
    rows[key] = dict(f=f, flux=Df, flux_anchor=dchi(kvz, Rz, ASEL), per_bin={f"{z:.1f}": dchi(kvz, Rz, bin_sel(z)) for z in ZB},
                     matter=Dm, ratio=Df / Dm if Dm > 0 else None, D_ta=Dta[key], D_rec=Drec[key], q=Dm / Drec[key] if Drec[key] > 0 else None,
                     R_F={f"{z:.1f}": [float(np.interp(x, kvz[z][1:], Rz[z][1:])) for x in (0.003, 0.005, 0.01, 0.02, 0.03)] for z in ZB},
                     R_mat={f"{z:.1f}": [float(np.exp(np.interp(math.log(x), np.log(kp[z]), np.log(Rp[z])))) for x in (1, 3, 5)] for z in ZB},
                     R_ta={f"{z:.1f}": [float(np.interp(math.log(x), np.log(KT[1:]), T[z]["spec"][key]["Rta"][1:])) for x in (1, 3, 5)] for z in ZB})
RES["rows"] = rows; RES["halo_model"] = dict(D_rec=Drec, D_ta=Dta)
P(f"[{FOOT}] SRF1: forest at flux level, R_set = f R_fold (settled-radius family, POST HOC). Gate Delta chi^2 <= 4 (755 DESI DR1 P1D points).")
P(f"[{FOOT}] f    | flux dchi2 | matter (realised) | ratio  | D_ta (halo model, ta scope) | D_rec (record convention = SRH1) | q = matter / D_rec")
for key, r in rows.items():
    P(f"[{FOOT}] {r['f']:<4} | {r['flux']:10.3f} | {r['matter']:10.2f}        | {r['ratio'] if r['ratio'] is None else round(r['ratio'], 4)!s:6} | {r['D_ta']:10.2f}                  | {r['D_rec']:10.2f}                         | {r['q'] if r['q'] is None else round(r['q'], 3)}")
P(f"[{FOOT}] halo-model only (no flux run), D_rec / D_ta: " + "; ".join(f"{f:.2f}: {Drec[fk_(f)]:.3f} / {Dta[fk_(f)]:.3f}" for f in HMF if f not in FG))
for key in ("f1.00", "f1.30", "f2.00"):
    r = rows[key]
    P(f"[{FOOT}] per bin f {r['f']}: " + " ".join(f"{z}:{v:.2f}" for z, v in r["per_bin"].items()))
    for z in ("2.2", "2.6", "3.0", "4.4"):
        P(f"[{FOOT}]   z {z}: R_F at 0.003/0.005/0.01/0.02/0.03 s/km " + "/".join(f"{v:.4f}" for v in r["R_F"][z]) + "; R_mat k1/3/5 "
          + "/".join(f"{v:.4f}" for v in r["R_mat"][z]) + " (halo model ta " + "/".join(f"{v:.4f}" for v in r["R_ta"][z]) + ")")

def edge(D):
    """first crossing of 4 on FG, log-linear in Delta chi^2 against f from the grid point below."""
    vals = [D[fk_(f)] for f in FG]
    cross = [i for i in range(1, len(FG)) if vals[i - 1] <= 4 < vals[i]]
    if vals[0] > 4: return dict(f_max=None, below_grid=True, crossings=[])
    if not cross: return dict(f_max=None, above_grid=True, crossings=[])
    i = cross[0]; a, b = math.log(max(vals[i - 1], 1e-12)), math.log(vals[i])
    return dict(f_max=FG[i - 1] + (FG[i] - FG[i - 1]) * (math.log(4) - a) / (b - a), crossings=[(FG[i - 1], FG[i]) for i in cross])
Dflux = {k: r["flux"] for k, r in rows.items()}
E0 = edge(Dflux); RES["edge"] = E0
P(f"[{FOOT}] G1 flux-level upper edge f_max: {E0}")

# ------------------------------------------------------------------ known answers
KA = {}
a_ok = True; a_rows = []
for z in ANCH:
    d = PR[z][0]; F = d["flux"]["primary"]
    for bx, v in F.items():
        if "B|f0.00" in v:
            same = bool(np.array_equal(np.array(v["B|f0.00"]["p"]), np.array(v["R"]["p"]))); a_ok &= same; a_rows.append((z, bx, same))
KA["a"] = dict(rows=a_rows, pass_=bool(a_ok and len(a_rows) > 0 and md5ok))
# (b) Poisson-only f = inf against FRZ3R's turn parts
bmax = 0.0; seeds_used = {}
for z, ps in PR.items():
    for s, d in ps.items():
        fr = json.load(open(os.path.join(FRZ3R, "parts", f"turn_z{z:.1f}_s{s}_{FOOT}_N384.json")))
        if len(fr["kv"]) != len(d["kv"]): bmax = float("inf"); seeds_used.setdefault(z, []).append(s); continue
        mine_R = np.array(d["flux"]["primary"]["base"]["R"]["p"]); mine_B = np.array(d["flux"]["primary"]["base"]["BP|finf"]["p"])
        bmax = max(bmax, float(np.max(np.abs(mine_R / np.array(fr["flux"]["primary"]["R"]["p"]) - 1))), float(np.max(np.abs(mine_B / np.array(fr["flux"]["primary"]["B"]["p"]) - 1))))
        seeds_used.setdefault(z, []).append(s)
kvz, Rz = flux_curves("finf", poisson=True); Dp_inf = dchi(kvz, Rz); Dm_p_inf = mat_D("finf", poisson=True)[0]
fkv, fR, fk3, fR3 = {}, {}, {}, {}
for z in ZB:
    arr, arr3 = [], []
    for s in seeds_used[z]:
        fr = json.load(open(os.path.join(FRZ3R, "parts", f"turn_z{z:.1f}_s{s}_{FOOT}_N384.json")))
        fkv[z] = np.array(fr["kv"]); arr.append(np.array(fr["flux"]["primary"]["B"]["p"]) / np.array(fr["flux"]["primary"]["R"]["p"]))
        k = np.array(fr["P3D"]["k"]); arr3.append(np.array(fr["P3D"]["B"]) / np.array(fr["P3D"]["R"]))
    fR[z] = np.mean(arr, 0); R3 = np.mean(arr3, 0); m = (k <= 10) & np.isfinite(R3); fk3[z], fR3[z] = k[m], R3[m]
if os.environ.get("SRF1_N", "384") != "384": fkv, fR = kvz, Rz
D_frz3r = dchi(fkv, fR); Dm_frz3r = float(forest_eval(FD, BGB, amp(fR3, fk3))["dchi2"])
KA["b"] = dict(max_rel_part=bmax, flux=[Dp_inf, D_frz3r], matter=[Dm_p_inf, Dm_frz3r],
               pass_=bool(bmax <= 1e-4 and abs(Dp_inf / D_frz3r - 1) <= 0.01 and abs(Dm_p_inf / Dm_frz3r - 1) <= 0.01))
# (c0) halo-model chain against SRH1
SF = json.load(open(os.path.join(SRH, f"srh1_forest_{FOOT}.json"))); SH = json.load(open(os.path.join(SRH, "srh1_hm.json")))
KKs = np.array(SH["k"]); m = (KKs >= 0.3) & (KKs <= 10); c0max = 0.0; c0d = {}
for f in TB.SRH1_GRID:
    key = fk_(f)
    for z in ZB:
        Rm = np.interp(np.log(KKs), np.log(KT[1:]), T[z]["spec"][key]["Rcold"][1:]); Rs = np.array(SH["cases"][f"{key}|{FOOT}"][f"{z}"]["R_cold"])
        c0max = max(c0max, float(np.max(np.abs(Rm - Rs)[m])))
    c0d[key] = (Drec[key], SF["cases"][key]["dchi2"])
c0ok = c0max <= 1e-4 and all(abs(a - b) <= 0.01 * max(b, 1e-3) + 1e-3 for a, b in c0d.values())
KA["c0"] = dict(max_abs_Rcold=c0max, dchi2_mine_vs_SRH1=c0d, pass_=bool(c0ok))
# (c1) realisation against the halo model's own ta-scope expectation
c1 = {}; ok = True
for key in ("f1.00", "f1.30", "f2.00"):
    a, b = rows[key]["matter"], rows[key]["D_ta"]
    good = (abs(a - b) <= 1.0) if (a < 1 and b < 1) else (0.67 <= a / b <= 1.5 if b > 0 else False)
    c1[key] = dict(realised=a, expected_ta=b, ratio=a / b if b > 0 else None, ok=bool(good)); ok &= good
KA["c1"] = dict(rows=c1, pass_=bool(ok))
# (d) mean flux
dmax = 0.0
for stg in ("primary", "bracket", "clustered"):
    for z, ps in (PR if stg == "primary" else load(stg, int(os.environ.get("SRF1_N", "384")))).items():
        for d in ps.values():
            for sp, boxes in d["flux"].items():
                sF = {"tau_x0.9": 0.9, "tau_x1.1": 1.1}.get(sp, 1.0)
                for bx in boxes.values():
                    for v in bx.values(): dmax = max(dmax, abs(v["meanF"] - math.exp(-sF * tau_eff(d["z"]))))
KA["d"] = dict(max_abs=dmax, pass_=bool(dmax <= 1e-4))
# (e) scatter at the edge
fe = E0.get("f_max") or (FG[-1] if E0.get("above_grid") else FG[0])
fnear = min(FG, key=lambda f: abs(f - fe)); key = fk_(fnear)
kvz, Rz = flux_curves(key)
half = {}
for z in ANCH:
    r0 = est(PR[z][0], key); r1 = est(PR[z][1], key); half[z] = 1.0 + 0.5 * (r0 - r1)
kvA = {z: kvz[z] for z in ANCH}
Dn_anch = dchi(kvA, half, ASEL); Dm_anch = dchi(kvz, Rz, ASEL); Dn12 = Dflux[key] * Dn_anch / Dm_anch if Dm_anch > 0 else float("inf")
fm_s = {}
for s in (0, 1):
    Ds = {}
    for f in FG:
        kv_, Rz_ = flux_curves(fk_(f), seeds={z: (s,) for z in ANCH}); Ds[fk_(f)] = dchi(kv_, Rz_)
    fm_s[s] = edge(Ds).get("f_max")
SE = abs(fm_s[0] - fm_s[1]) / 2 if (fm_s[0] is not None and fm_s[1] is not None) else None
KA["e"] = dict(f_near=fnear, noise_dchi2_12bin=Dn12, noise_anchor=Dn_anch, mean_anchor=Dm_anch, f_max_seed0=fm_s[0], f_max_seed1=fm_s[1], SE_f_max=SE, pass_=bool(Dn12 <= 1.0))
RES["known_answers"] = KA
for k, v in KA.items(): P(f"[{FOOT}] known answer ({k}): {'PASS' if v['pass_'] else 'FAIL'} " + json.dumps({kk: vv for kk, vv in v.items() if kk != 'pass_'}, default=str)[:900])
P(f"[{FOOT}] Poisson-only reading (FRZ3R's method, reported): f 1.00 flux {dchi(*flux_curves('f1.00', poisson=True)):.3f}, matter {mat_D('f1.00', poisson=True)[0]:.2f}; f inf flux {Dp_inf:.2f}, matter {Dm_p_inf:.1f}")
dr = {z: PR[z][0]["dropped_share"] for z in ZB}; RES["dropped_share"] = dr
P(f"[{FOOT}] rare-group share dropped by A1's 3 % cut (ta-scope 1h difference at k 3; f 1.00 / 1.30 / 2.00): " + "; ".join(f"z {z}: " + "/".join(f"{v:+.3f}" for v in dd.values()) for z, dd in dr.items()))
P(f"[{FOOT}] forced groups (log M, n_g, E_g) at z 2.2: {[(gg['lM'], gg['ng'], round(gg['Eg'], 4)) for gg in PR[2.2][0]['groups']]}")

# ------------------------------------------------------------------ AMENDMENT_A2 reading R (reported; never the label)
WMODE["m"] = "ratio"; rowsR = {}
for f in FG + [math.inf]:
    key = fk_(f); kvz, Rz = flux_curves(key); rowsR[key] = dict(flux=dchi(kvz, Rz), matter=mat_D(key)[0])
WMODE["m"] = "frozen"
ER = edge({k: v["flux"] for k, v in rowsR.items()})
RES["reading_R_A2"] = dict(rows=rowsR, edge=ER)
P(f"[{FOOT}] reading R (AMENDMENT_A2, ratio-weighted forced groups; REPORTED, not the label): " + "; ".join(f"{v and k}: flux {r['flux']:.3f} matter {r['matter']:.2f}" for k, r in rowsR.items() for v in [True]) + f"; f_max {ER}")

# ------------------------------------------------------------------ regime split (ADDED AFTER THE CRITERIA WERE FROZEN, on the lead's
# request; UNGRADED; no new compute: the stratified estimator is a sum over the base box and the forced groups, so the sum is split)
SN = TB.srh1(); RG = {}
for z in ZB:
    SN["set_z"](z); L_ = SN["L"]; LMg = L_["LM"]; out = {}
    for gr in PR[z][0]["groups"]:
        cl = [SN["regime"](hb, FOOT) == "cluster" for hb, lm in zip(L_["HB"], LMg) if gr["lM"] - 1e-9 <= lm < gr["lM"] + 0.5 - 1e-9]
        out[gr["g"]] = sum(cl) / max(len(cl), 1)
    RG[z] = out
def est_sub(d, key, which, what="p"):
    F = d["flux"]["primary"]; R = np.array(F["base"]["R"][what]); dP = np.zeros_like(R)
    if which == "galaxy": dP = dP + np.array(F["base"]["B|" + key][what]) - R
    for gr in d["groups"]:
        is_cl = RG[d["z"]][gr["g"]] >= 0.5
        if (which == "cluster") == is_cl:
            bx = F[f"g{gr['g']}"]; dP = dP + gr["w"] * (np.array(bx["B|" + key][what]) - np.array(bx["R"][what]))
    return 1.0 + dP / R
SPLIT = {}
for which in ("galaxy", "cluster"):
    kvz = {z: np.array(PR[z][0]["kv"]) for z in ZB}; Rz = {z: np.mean([est_sub(PR[z][s], "f1.00", which) for s in sorted(PR[z])], 0) for z in ZB}
    kp, Rp = {}, {}
    for z in ZB:
        k = np.array(PR[z][0]["k3d"]); R = np.mean([est_sub(PR[z][s], "f1.00", which, "P3D") for s in sorted(PR[z])], 0); mm = (k <= 10) & np.isfinite(R); kp[z], Rp[z] = k[mm], R[mm]
    SPLIT[which] = dict(flux=dchi(kvz, Rz), matter=float(forest_eval(FD, BGB, amp(Rp, kp))["dchi2"]))
RES["regime_split_f1_UNGRADED_added_after_freeze"] = dict(split=SPLIT, cluster_fraction_of_group_masses=RG,
    note="galaxy = base-box difference (common bins, galaxy regime, plus the two-halo term) + forced groups whose grid masses are mostly galaxy regime; cluster = forced groups mostly cluster regime (FRZ1's v_stiff boundary unchanged). A group straddling the boundary is assigned by majority.")
P(f"[{FOOT}] REGIME SPLIT at f 1.00 (added after the criteria were frozen; UNGRADED): galaxy-regime only: flux {SPLIT['galaxy']['flux']:.3f}, matter {SPLIT['galaxy']['matter']:.2f}; cluster-regime only: flux {SPLIT['cluster']['flux']:.3f}, matter {SPLIT['cluster']['matter']:.2f}; cluster fraction per forced group at z 2.2: {RG[2.2]}")

# ------------------------------------------------------------------ mutations
MU = {}
BR = load("bracket", int(os.environ.get("SRF1_N", "384"))); S23 = SEL((2.2, 3.0))
def br_D(tag, key, parts, sel):
    kz = {z: np.array(parts[z][0]["kv"]) for z in parts}; Rz = {z: est(parts[z][0], key, tag) for z in parts}; return dchi(kz, Rz, sel)
if all(z in BR for z in (2.2, 3.0)):
    m1 = br_D("M1_lin", "f1.30", BR, S23); p1 = br_D("primary", "f1.30", BR, S23)
    MU["M1_saturation_removed"] = dict(dchi2_z22_30=m1, primary=p1, factor=m1 / p1, bites=bool(max(m1 / p1, p1 / m1) >= 1.25),
                                       other_f={k: [br_D("M1_lin", k, BR, S23), br_D("primary", k, BR, S23)] for k in ("f1.00", "f2.00")})
A0 = {z: {0: PR[z][0]} for z in ANCH}
kz = {z: np.array(A0[z][0]["kv"]) for z in ANCH}
m2 = dchi(kz, {z: est(A0[z][0], "MU2") for z in ANCH}, ASEL); p2 = dchi(kz, {z: est(A0[z][0], "f1.00") for z in ANCH}, ASEL); q2 = dchi(kz, {z: est(A0[z][0], "f2.00") for z in ANCH}, ASEL)
MU["M2_Rset_doubled"] = dict(dchi2_anchor_seed0=m2, f1=p2, f2_grid=q2, factor=m2 / p2 if p2 > 0 else float("inf"), bites=bool(m2 >= 2 * p2))
RES["mutations"] = MU
for k, v in MU.items(): P(f"[{FOOT}] MUTATE {k}: " + json.dumps(v, default=str) + f" -> {'bites' if v['bites'] else 'DOES NOT BITE'}", m=True)

# ------------------------------------------------------------------ G2, G3, G4 from SRH1 and the label
G4E = {"canonical": 1.004, "alt": 1.050}[FOOT]; G2E = 0.391
RES["SRH1_edges_used"] = dict(G2=G2E, G4=G4E, G3="holds at every f", source="SRH1 RESULT.md and srh1_grade.out as committed (G4 edge: SRH1 RESULT.md interpolated table)")
f_lo = max(G2E, G4E)
def window(fmax, flo):
    if fmax is None: return None
    return (flo, fmax) if fmax > flo else None
def fmax_of(ed):
    if ed.get("above_grid"): return FG[-1]
    if ed.get("below_grid"): return FG[0] * 0.999
    return ed["f_max"]
fM = fmax_of(E0)
# brackets
BRK = {}
if all(z in BR for z in (2.2, 3.0)):
    for tag in ("lam_x0.5", "lam_x2", "lam_rec", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1"):
        est12 = {}
        for f in (1.00, 1.30, 2.00):
            k = fk_(f); est12[k] = Dflux[k] * br_D(tag, k, BR, S23) / max(br_D("primary", k, BR, S23), 1e-12)
        BRK[tag] = est12
for stg in ("clustered", "res"):
    PP = load(stg, 256 if stg == "res" else int(os.environ.get("SRF1_N", "384")))
    if 2.2 in PP:
        est12 = {}
        for f in (1.00, 1.30, 2.00):
            k = fk_(f); est12[k] = Dflux[k] * br_D("primary", k, PP, SEL((2.2,))) / max(dchi({2.2: np.array(PR[2.2][0]["kv"])}, {2.2: est(PR[2.2][0], k)}, SEL((2.2,))), 1e-12)
        BRK[stg] = est12
BRK["B-conv (record convention)"] = {fk_(f): Dflux[fk_(f)] * Drec[fk_(f)] / rows[fk_(f)]["matter"] for f in (1.00, 1.30, 2.00)}
def edge3(e):
    fs = [1.00, 1.30, 2.00]; v = [e[fk_(f)] for f in fs]
    if v[0] > 4: return ("< 1.00", None)
    for i in range(1, 3):
        if v[i] > 4:
            a, b = math.log(max(v[i - 1], 1e-12)), math.log(v[i]); return ("", fs[i - 1] + (fs[i] - fs[i - 1]) * (math.log(4) - a) / (b - a))
    return ("> 2.00", None)
frag = []
win0 = window(fM, f_lo)
for tag, e in BRK.items():
    pre, fm = edge3(e); e["_edge"] = pre + (f"{fm:.3f}" if fm is not None else "")
    f1_cross = (e["f1.00"] > 4) != (Dflux["f1.00"] > 4)
    fmv = fm if fm is not None else (0.99 if pre == "< 1.00" else 2.0)
    opens = (fmv > f_lo) != (win0 is not None)
    if f1_cross or opens: frag.append(tag)
RES["brackets"] = BRK
for tag, e in BRK.items(): P(f"[{FOOT}] bracket {tag}: 12-bin estimate at f 1.00 / 1.30 / 2.00: {e['f1.00']:.2f} / {e['f1.30']:.2f} / {e['f2.00']:.2f}; edge {e['_edge']}")
kaok = all(v["pass_"] for v in KA.values()); muok = all(v["bites"] for v in MU.values()) and len(MU) == 2
brok = len(BRK) >= 10
if not (kaok and muok): lab = "NO VERDICT"
elif win0 is None:
    lab = f"WINDOW EMPTY AT FLUX LEVEL (G1 flux edge {fM:.3f} vs lower edge {f_lo:.3f}; gap x {f_lo / fM:.2f})"
else:
    inside = win0[0] <= 1.0 <= win0[1]
    lab = f"WINDOW OPENS AT FLUX LEVEL [{win0[0]:.3f}, {win0[1]:.3f}{'+' if E0.get('above_grid') else ''}], f = 1 {'INSIDE' if inside else 'OUTSIDE'}"
    if SE is not None and (win0[1] - win0[0]) < 2 * SE: lab += ", MARGINAL"
    lab += "; a hit awaiting an independent blind re-grade, not a pass of form B"
if lab != "NO VERDICT" and frag: lab += ", FRAGILE (" + "; ".join(frag) + ")"
if not brok: lab += " [brackets incomplete]"
RES["label"] = lab
fR = fmax_of(ER); wR = window(fR, f_lo)
RES["reading_R_A2"]["window"] = wR; RES["reading_R_A2"]["moves"] = dict(f1_across_gate=bool((rowsR["f1.00"]["flux"] > 4) != (Dflux["f1.00"] > 4)), window_changes=bool((wR is None) != (win0 is None)))
P(f"[{FOOT}] reading R (A2, reported beside the label): f_max {fR}, window {wR}; moves f = 1 across the gate: {RES['reading_R_A2']['moves']['f1_across_gate']}; opens/closes the window: {RES['reading_R_A2']['moves']['window_changes']}")
w_r = window(fM, G2E)
RES["reported"] = dict(f_max=fM, edge=E0, window_with_SRH1R_reading=w_r, f_lo=f_lo)
P(f"[{FOOT}] reported: forest flux-level edge f_max {fM} (SRH1's matter-level edge 0.722 / 0.725); lower edge used {f_lo} (G2 0.391, G4 {G4E}: SRH1 RESULT.md, interpolated); "
  f"window with SRH1R's reading (lensing cannot see f, f_lo = 0.391): {w_r}")
P(f"[{FOOT}] LABEL (as amended by A1; the as-frozen grid could not be run): {lab}")
json.dump(RES, open(os.path.join(OUTD, f"srf1_grade_{FOOT}.json"), "w"), indent=1, default=float)
open(os.path.join(OUTD, f"srf1_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
json.dump(dict(lane="SRF1", footing=FOOT, mutations=MU, note=RES["note"]), open(os.path.join(OUTD, f"srf1_grade_{FOOT}_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(OUTD, f"srf1_grade_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
