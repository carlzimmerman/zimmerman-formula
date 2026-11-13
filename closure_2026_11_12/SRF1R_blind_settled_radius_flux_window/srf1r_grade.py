#!/usr/bin/env python3
"""SRF1R (READING.md, cc3d45432d): grading per footing. FRZ1's frz1_forest.py is executed unchanged from its own path
(read-only) up to the line that reads frz1_hm.json (the record's pipeline, form B's CLASS reference, DESI DR1 P1D).
  record's matter level Delta chi^2_SRH1(f) (SRH1's R_cold, recomputed in stage 0) and check c0 against SRH1's stored values;
  matter level of this construction Delta chi^2_matter,real(f); flux level Delta chi^2_flux,real(f) (own gate, full covariance);
  K(f), graded Delta chi^2_G(f), f_max, window, label; known answers (a)-(f); mutations M1, M2; brackets B0-B10.
  SRF1R_FOOT=canonical|alt nice -n 19 python3 srf1r_grade.py -> srf1r_grade_<foot>.json / .out, srf1r_grade_<foot>_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, glob
FOOT = os.environ.get("SRF1R_FOOT", "canonical"); assert FOOT in ("canonical", "alt")
os.environ["HLF1_FOOT"] = FOOT; os.environ.pop("HLF1_MUTATE", None)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_solve, cho_factor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
SRC = os.path.join(FRZ, "frz1_forest.py"); code = open(SRC).read()
cut = code.index('FZ = json.load(open(os.path.join(HERE, "frz1_hm.json")))')
NS = {"__file__": SRC, "__name__": "frz1_forest_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), NS)
forest_eval, Rkz_z, FD, BGB, CFULL = (NS[k] for k in ("forest_eval", "Rkz_z", "FD", "BGB", "CFULL"))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]; ANCH = [2.2, 3.0, 4.4]; SEEDS = [0, 1, 2]
TAB = {z: np.load(os.path.join(HERE, "tables", f"tab_{FOOT}_z{z:.1f}.npz")) for z in ZB}
FG = list(TAB[2.2]["FGRID"]); ALLF = list(TAB[2.2]["ALLF"]); KK = TAB[2.2]["KK"]
fl = lambda f: "inf" if math.isinf(f) else f"{f:.2f}"
def part(var, z, s):
    p = os.path.join(HERE, "parts", f"{var}_{FOOT}_z{z:.1f}_s{s}.json")
    return json.load(open(p)) if os.path.exists(p) else None
RES = dict(lane="SRF1R", footing=FOOT, reading="cc3d45432d", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, MUTATE={}, brackets={})

# ---------------------------------------------------------------- the record's matter level (SRH1's path) and check c0
def dchi_rows(rows): return forest_eval(FD, BGB, Rkz_z({f"{z:.1f}": rows[z] for z in rows}))["dchi2"]
SRHM = {}
for q, f in enumerate(ALLF):
    SRHM[fl(f)] = dchi_rows({z: TAB[z]["Rcold"][q] for z in ZB})
SRS = json.load(open(os.path.join(SRH, f"srh1_forest_{FOOT}.json")))["cases"]
c0rows = {}
for f in ALLF:
    key = "KA_T" if math.isinf(f) else ("KA_0" if f == 0 else f"f{f:.2f}")
    if key in SRS: c0rows[fl(f)] = (SRHM[fl(f)], SRS[key]["dchi2"])
c0 = all(abs(a - b) <= 0.01 for a, b in c0rows.values())
# light-halo share: heavy one-halo change only, over the record's denominator
heavy_only = {}
for f in (1.0, 2.0):
    q = ALLF.index(f); heavy_only[fl(f)] = dchi_rows({z: 1 + TAB[z]["dP3"][q] / TAB[z]["PstdRbar"] for z in ZB})
RES["KA"]["c0"] = dict(rows=c0rows, heavy_one_halo_only=heavy_only, pass_=bool(c0))
P(f"[{FOOT}] c0 SRH1's path recomputed vs stored: " + ", ".join(f"{k} {a:.3f}/{b:.3f}" for k, (a, b) in c0rows.items()) + f" -> {'PASS' if c0 else 'FAIL'}")
P(f"[{FOOT}] heavy (>= 10^10.8) one-halo change only, record's denominator: f 1 {heavy_only['1.00']:.2f} (all haloes {SRHM['1.00']:.2f}); f 2 {heavy_only['2.00']:.2f} ({SRHM['2.00']:.2f})")

# ---------------------------------------------------------------- matter level of the construction (AMENDMENT A3)
RHOM = float(json.load(open(os.path.join(HERE, "tables", "cosmo.json")))["RHO_M"])
def expected_bg(z):
    T = TAB[z]; li = T["light_idx"]; U = T["URt_light"].astype(float); Wl = T["W"][li]
    E = T["P2h"] + np.sum(Wl[:, None] * U ** 2, 0) / RHOM ** 2
    return np.interp(np.log(KK), np.log(np.maximum(T["KTAB"], 1e-6)), E)
P3B = {}; Q = {}
for z in ANCH:
    x = part("P", z, 0)
    if x is None: P(f"[{FOOT}] MISSING primary part z {z}"); sys.exit(1)
    P3B[z] = np.interp(np.log(KK), np.log(np.array(x["k3"])), np.array(x["P3_B"])); Q[z] = P3B[z] / expected_bg(z)
for z in ZB:                                   # A3: bins without a part: measured/expected ratio interpolated in z
    if z in P3B: continue
    za = max(a for a in ANCH if a < z); zb = min(a for a in ANCH if a > z); t = (z - za) / (zb - za)
    P3B[z] = expected_bg(z) * ((1 - t) * Q[za] + t * Q[zb])
def Rpaint(z, q):
    T = TAB[z]; R = 1 + T["dP3"][q] / (P3B[z] + T["P1hH"])
    R[KK < 0.3] = np.interp(0.3, KK, R); R[KK > 10.0] = np.interp(10.0, KK, R); return R
def sub_eval(rows, zsel):
    s_ = np.isin(np.round(FD["zs"], 1), zsel)
    sub = dict(FD, ZB=np.array([z for z in FD["ZB"] if round(float(z), 1) in zsel]), zs=FD["zs"][s_], ks=FD["ks"][s_], Pd=FD["Pd"][s_],
               NB=int(s_.sum()), CF=cho_factor(CFULL[np.ix_(s_, s_)]))
    return forest_eval(sub, BGB, Rkz_z({f"{z:.1f}": rows[z] for z in rows}))["dchi2"]
MATR, MATR_AB, MATR_22 = {}, {}, {}
for f in FG:
    q = ALLF.index(f); rows = {z: Rpaint(z, q) for z in ZB}
    MATR[fl(f)] = dchi_rows(rows); MATR_AB[fl(f)] = sub_eval(rows, ANCH); MATR_22[fl(f)] = sub_eval(rows, [2.2])
carry = {}
for z in ANCH:
    q = ALLF.index(1.0); rp = Rpaint(z, q); rc = TAB[z]["Rcold"][q]
    carry[f"{z:.1f}"] = [float((np.interp(k, KK, rp) - 1) / (np.interp(k, KK, rc) - 1)) if abs(np.interp(k, KK, rc) - 1) > 1e-7 else None for k in (3.0, 5.0, 10.0)]

# ---------------------------------------------------------------- flux level (A3: anchor bins, seed 0)
zs, ks, Pd = FD["zs"], FD["ks"], FD["Pd"]; ZR = np.round(zs, 1)
def r_at(kv, R, kd): return np.interp(kd, kv[1:], R[1:], left=R[1], right=R[-1])
def gate_sel(rvec, zsel):
    sel = np.where(np.isin(ZR, zsel))[0]; d = ((rvec - 1.0) * Pd)[sel]
    return float(d @ cho_solve(cho_factor(CFULL[np.ix_(sel, sel)]), d))
def fidx_of(x, f):
    for j, v in enumerate(x["f"]):
        if isinstance(f, str):
            if v == f: return j
        elif isinstance(v, (int, float)) and ((math.isinf(f) and math.isinf(v)) or (not math.isinf(f) and not math.isinf(v) and abs(v - f) < 1e-9)): return j
    return None
def rvec_for(var, f, zsel, seeds=(0,)):
    r = np.ones(len(Pd))
    for z in zsel:
        Rs = []
        for s in seeds:
            x = part(var, z, s)
            if x is None: return None
            j = fidx_of(x, f)
            if j is None: return None
            Rs.append(np.array(x["R_F"])[j]); kv = np.array(x["kv"])
        s_ = ZR == z; r[s_] = r_at(kv, np.mean(Rs, 0), ks[s_])
    return r
FLUX_AB, FLUX_22, FLUX, ESTH = {}, {}, {}, []
for f in FG:
    k_ = fl(f); r22 = rvec_for("P", f, [2.2]); FLUX_22[k_] = gate_sel(r22, [2.2])
    rab = rvec_for("P", f, ANCH)
    if rab is not None:
        FLUX_AB[k_] = gate_sel(rab, ANCH); FLUX[k_] = FLUX_AB[k_] * (MATR[k_] / MATR_AB[k_] if MATR_AB[k_] > 0 else 1.0)
    else:
        FLUX_AB[k_] = None; FLUX[k_] = FLUX_22[k_] * (MATR[k_] / MATR_22[k_] if MATR_22[k_] > 0 else 1.0); ESTH.append(k_)
PERBIN = {}
for f in (1.0, 2.0):
    r = rvec_for("P", f, ANCH); PERBIN[fl(f)] = {f"{z:.1f}": gate_sel(r, [z]) for z in ANCH}
K = {}; GR = {}
for f in FG:
    k_ = fl(f); K[k_] = (SRHM[k_] / MATR[k_]) if MATR[k_] >= 0.01 else (SRHM["0.70"] / MATR["0.70"])
    GR[k_] = FLUX[k_] * K[k_]
def edge(fs, vals):
    last = None
    for f, v in zip(fs, vals):
        if v <= 4: last = (f, v); continue
        if last is None: return 0.0, "fails at the first grid f"
        fa, va = last
        if math.isinf(f): return fa, f"passes to {fa:g}; fails only at inf"
        if va <= 0: return fa, "interpolation from zero"
        return fa + (math.log(4) - math.log(va)) / (math.log(v) - math.log(va)) * (f - fa), "interpolated"
    return math.inf, "passes at every grid f including inf"
fmax, how = edge(FG, [GR[fl(f)] for f in FG])
G4E = {"canonical": 1.004, "alt": 1.050}[FOOT]; G2E = 0.391; flo = max(G2E, G4E)
RES.update(f_grid=[fl(f) for f in FG], dchi2_SRH1=SRHM, dchi2_matter_real_12bin=MATR, dchi2_matter_real_anchor_block=MATR_AB,
           dchi2_matter_real_z22=MATR_22, dchi2_flux_anchor_block=FLUX_AB, dchi2_flux_z22=FLUX_22, dchi2_flux_12bin_estimate=FLUX,
           flux_from_z22_only=ESTH, K=K, dchi2_G=GR, per_bin_flux=PERBIN, carry_f1=carry, f_max=fmax, f_max_how=how, f_lo=flo)

# ---------------------------------------------------------------- known answers
ka = {}
q0 = 0; a_ok = True
for p in glob.glob(os.path.join(HERE, "parts", f"P_{FOOT}_*.json")):
    x = json.load(open(p)); j = fidx_of(x, 0.0); a_ok = a_ok and bool(np.max(np.abs(np.array(x["R_F"])[j] - 1)) == 0.0)
md5ok = bool(FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433")
ka["a"] = dict(dchi2_f0=FLUX_AB["0.00"], RF_exactly_1=a_ok, md5_ok=md5ok, pass_=bool(a_ok and abs(FLUX_AB["0.00"]) <= 1e-12 and md5ok))
TREF = {"canonical": (5035.0, 363.0), "alt": (4377.0, 425.0)}[FOOT]
mi, fi_ = MATR["inf"], FLUX["inf"]
ka["b"] = dict(matter_real=mi, frz3r_T_matter=TREF[0], flux_real_estimate=fi_, flux_z22_bin=FLUX_22["inf"], frz3r_T_flux=TREF[1],
               ratio=fi_ / mi if mi else None, frz3r_T_ratio=TREF[1] / TREF[0], graded_inf=GR["inf"], frz1_x_frz3r_ratio={"canonical": 715, "alt": 874}[FOOT],
               flux_is_estimate_A3=True, pass_=bool(TREF[0] / 2 <= mi <= TREF[0] * 2 and TREF[1] / 3 <= fi_ <= TREF[1] * 3))
SR1 = {"canonical": 38.741, "alt": 36.658}[FOOT]; c1v = MATR["1.00"] / SR1; K1 = K["1.00"]
c2 = {fl(f): K[fl(f)] / K1 for f in FG if 0.7 <= f <= 6 and SRHM[fl(f)] >= 1}
ka["c"] = dict(c0=RES["KA"]["c0"]["pass_"], c1=c1v, c1_pass=bool(0.25 <= c1v <= 1.5), c2=c2, c2_pass=bool(all(0.5 <= v <= 2 for v in c2.values())))
ka["c"]["pass_"] = bool(ka["c"]["c0"] and ka["c"]["c1_pass"] and ka["c"]["c2_pass"])
mf = []; epsmax = 0.0
for p in glob.glob(os.path.join(HERE, "parts", f"*_{FOOT}_*.json")):
    x = json.load(open(p)); mf.append(x["meanF_relerr"])
    for f, e in zip(x["f"], x["eps"]):
        ff = 2.0 if isinstance(f, str) else float(f)
        if ff <= 6: epsmax = max(epsmax, abs(e))
ka["d"] = dict(max_meanF_relerr=max(mf), max_abs_eps_f_le_6=epsmax, pass_=bool(max(mf) <= 1e-4 and epsmax <= 0.01))
e_rows = {}; e_ok = True; e_avail = part("P", 2.2, 1) is not None
EF = [1.0] + ([f for f in (0.70, 1.00, 1.25, 1.60, 2.00, 3.00) if f <= fmax][-1:] + [f for f in (0.70, 1.00, 1.25, 1.60, 2.00, 3.00) if f > fmax][:1] if fmax <= 3 else [2.0, 3.0])
for f in sorted(set(EF)):
    if not e_avail: break
    xs = [part("P", 2.2, s) for s in (0, 1)]; R = np.array([np.array(x["R_F"])[fidx_of(x, f)] for x in xs]); kv = np.array(xs[0]["kv"])
    m = (kv > 0) & (kv <= float(np.max(ks[ZR == 2.2])))
    E = float(np.sqrt(np.mean((R.mean(0)[m] - 1) ** 2))); S = float(np.sqrt(np.mean((R.std(0, ddof=1)[m] / math.sqrt(2)) ** 2)))
    ok = S <= E / 3; e_ok = e_ok and ok
    e_rows[fl(f)] = dict(E=E, S=S, ok=bool(ok), dchi2_z22_s0=gate_sel(rvec_for("P", f, [2.2], (0,)), [2.2]), dchi2_z22_s1=gate_sel(rvec_for("P", f, [2.2], (1,)), [2.2]))
ka["e"] = dict(rows=e_rows, computed=e_avail, pass_=bool(e_avail and e_ok))
z3 = TAB[3.0]; ka["f"] = dict(conf=float(z3["conf"]), mass_check=float(z3["mass_check"]), pass_=bool(float(z3["conf"]) <= 1e-6 and float(z3["mass_check"]) <= 1e-9))
RES["KA"].update(ka); KA_OK = all(ka[k]["pass_"] for k in "abcdef")
per_seed = {k: (v["dchi2_z22_s0"], v["dchi2_z22_s1"]) for k, v in e_rows.items()}

# ---------------------------------------------------------------- mutations and brackets (A3: z 2.2 bin, seed 0)
def z22(var, f):
    r = rvec_for(var, f, [2.2]); return None if r is None else gate_sel(r, [2.2])
MU = {}
p1, p2 = FLUX_22["1.00"], FLUX_22["2.00"]; m1a, m1b = z22("M1", 1.0), z22("M1", 2.0)
if None not in (m1a, m1b):
    fac = lambda a, b: max(a / b, b / a) if a > 0 and b > 0 else math.inf
    MU["M1"] = dict(primary_f1=p1, mutate_f1=m1a, primary_f2=p2, mutate_f2=m1b, bites=bool(fac(m1a, p1) >= 1.25 or fac(m1b, p2) >= 1.25),
                    direction="up" if m1a > p1 else "down")
m2 = z22("M2", "Rset_x2_at_f1")
if m2 is not None: MU["M2"] = dict(primary_f1=p1, mutate=m2, bites=bool(m2 >= 2 * p1))
MU_OK = bool(MU.get("M1", {}).get("bites") and MU.get("M2", {}).get("bites"))
RES["MUTATE"] = MU
BRF = [0.70, 1.00, 1.25, 1.60, 2.00, 3.00]
BR = {"B0": dict(values={fl(f): FLUX[fl(f)] for f in BRF}, note="unscaled flux (twelve-bin estimate), carry convention")}
for b in ["B2", "B3", "B8", "B1", "B4", "B5", "B6", "B7", "B9", "B10"]:
    vals = {}
    for f in BRF:
        ab = z22(b, f); ap = FLUX_22[fl(f)]
        if ab is None: vals = None; break
        vals[fl(f)] = GR[fl(f)] * (ab / ap) if ap > 0 else (0.0 if ab == 0 else math.inf)
    BR[b] = dict(values=vals) if vals else dict(values=None, note="not computed")
cross = []
for b, v in BR.items():
    if not v["values"]: continue
    vv = v["values"]; e_, _ = edge(BRF, [vv[fl(f)] for f in BRF]); v["f_max"] = e_
    f1_flip = (vv["1.00"] <= 4) != (GR["1.00"] <= 4); win_p = fmax >= flo; win_b = e_ >= flo
    v["f1_flips"] = bool(f1_flip); v["window_flips"] = bool(win_p != win_b)
    if b != "B10" and (f1_flip or win_p != win_b): cross.append(b)
RES["brackets"] = BR; RES["brackets_not_computed"] = [b for b, v in BR.items() if not v["values"]]


# ---------------------------------------------------------------- label
if not (KA_OK and MU_OK):
    why = [k for k in "abcdef" if not ka[k]["pass_"]] + [m for m in ("M1", "M2") if not MU.get(m, {}).get("bites")]
    label = f"NO VERDICT (fails: {', '.join(why)})"
elif fmax >= flo:
    label = f"WINDOW OPENS AT FLUX LEVEL [{flo:.3f}, {fmax:.3f}], f = 1 OUTSIDE (G4 fails at f = 1)" + (f", FRAGILE ({', '.join(cross)})" if cross else "") + " (a hit on a post hoc family, not a pass of form B)"
else:
    label = f"WINDOW EMPTY AT FLUX LEVEL (f_max {fmax:.3f} < f_lo {flo:.3f}, gap x {flo / fmax:.2f})" + (f", FRAGILE ({', '.join(cross)})" if cross else "") if fmax > 0 else "WINDOW EMPTY AT FLUX LEVEL (fails at every grid f)"
RES.update(label=label, KA_ok=bool(KA_OK), MUTATE_ok=MU_OK, fragile_by=cross,
           window_with_srh1r_reading=(f"[{G2E}, {fmax:.3f}]" if fmax >= G2E else "empty"), f1_forest_flux_pass=bool(GR["1.00"] <= 4))
P(f"[{FOOT}] LABEL: {label}")
P(f"[{FOOT}] f_max (flux-level forest edge) {fmax:.4g} ({how}); f_lo {flo}; forest at f = 1: Delta chi^2_G {GR['1.00']:.3f} -> {'PASS' if GR['1.00'] <= 4 else 'FAIL'}")
P(f"[{FOOT}] window read with SRH1R (lensing cannot see f; lower edge G2's 0.391): {RES['window_with_srh1r_reading']}")
P(f"[{FOOT}]    f | SRH1 matter | matter real |   K   | flux real | softening | graded G | gate")
for f in FG:
    k_ = fl(f); soft = FLUX[k_] / MATR[k_] if MATR[k_] > 0 else float('nan')
    P(f"[{FOOT}] {k_:>5} | {SRHM[k_]:11.3f} | {MATR[k_]:11.3f} | {K[k_]:5.3f} | {FLUX[k_]:9.4f} | {soft:9.2e} | {GR[k_]:8.4f} | {'P' if GR[k_] <= 4 else 'F'}")
P(f"[{FOOT}] SRH1 matter at the SRH1-only grid points (flux not computed): " + ", ".join(f"{fl(f)} {SRHM[fl(f)]:.3f}" for f in ALLF if f not in FG))
P(f"[{FOOT}] per-bin flux Delta chi^2 (own blocks) at f 1 / 2: {PERBIN}")
P(f"[{FOOT}] flux twelve-bin values are ESTIMATES (A3): anchor block x matter twelve-bin / anchor block; from the z 2.2 bin alone at {ESTH}")
P(f"[{FOOT}] anchor-block flux (direct): " + ", ".join(f"{k} {v:.4f}" for k, v in FLUX_AB.items() if v is not None))
P(f"[{FOOT}] z 2.2-bin flux (direct): " + ", ".join(f"{k} {v:.4f}" for k, v in FLUX_22.items()))
P(f"[{FOOT}] brackets not computed: {RES['brackets_not_computed']}")
P(f"[{FOOT}] carry at f 1 ((R_paint-1)/(R_cold-1) at k 3/5/10): {carry}")
P(f"[{FOOT}] KA: " + "; ".join(f"({k}) {'PASS' if ka[k]['pass_'] else 'FAIL'}" for k in "abcdef"))
P(f"[{FOOT}]   (b) matter real {mi:.1f} vs T {TREF[0]}, flux real (estimate) {fi_:.2f} vs T {TREF[1]}, ratio {ka['b']['ratio']:.4f} vs {TREF[1]/TREF[0]:.4f}; graded inf {GR['inf']:.1f}")
P(f"[{FOOT}]   (c) c1 {c1v:.3f}; c2 {c2}")
P(f"[{FOOT}]   (d) {ka['d']}")
P(f"[{FOOT}]   (e) {e_rows}; per seed {per_seed}")
P(f"[{FOOT}] MUTATE: {MU}")
for b, v in BR.items():
    P(f"[{FOOT}] bracket {b}: " + (", ".join(f"{k} {x:.3f}" for k, x in v['values'].items()) + f"; f_max {v['f_max']:.3g}; f1 flips {v['f1_flips']}; window flips {v['window_flips']}" if v["values"] else "not computed"))
P(f"[{FOOT}] FRAGILE rule applied to the computed brackets only (A3 item 5)")
json.dump(RES, open(os.path.join(HERE, f"srf1r_grade_{FOOT}.json"), "w"), indent=1, default=lambda o: None)
json.dump(dict(lane="SRF1R", footing=FOOT, MUTATE=MU, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, f"srf1r_grade_{FOOT}_MUTATE.json"), "w"), indent=1, default=lambda o: None)
open(os.path.join(HERE, f"srf1r_grade_{FOOT}.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
