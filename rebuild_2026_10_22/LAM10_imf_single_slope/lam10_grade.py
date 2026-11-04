"""LAM10 grade (criteria e70770e272): LAM9's frozen grading text (Q1 KU2's absolute r_half residual, Q2 HX1's MaNGA need, Q3
LAM6's h4 lean; C1-C4, K1/K2 gates, K3, variant B, M1 MUTATE, rows, colour row) with LAM10's single-slope alpha and Gamma_best.
This file is LAM9's lam9_grade.py with only the data sources, names and the Gamma_b detail rows changed. Footings apart.
  python3 -I lam10_grade.py           -> lam10_grade.out/.json (variant A, labels) and lam10_grade_B.out/.json
  python3 -I lam10_grade.py MUTATE    -> lam10_grade_MUTATE.out/.json (alpha shuffled within groups; M1)
Minutes, single thread. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework."""
import os, sys, json, math, io, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); RB = os.path.dirname(HERE); L9DIR = os.path.join(RB, "LAM9_imf_from_spectra"); sys.path.insert(0, L9DIR)
import numpy as np
from scipy.stats import spearmanr
import lam9_core as L
MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"; NB = 2000; SEED = L.SEED
OUT = []; RES = {"lane": "LAM10", "mode": MODE, "note": "κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework."}
def P(s=""): print(s, flush=True); OUT.append(s)
def ci(x): return [float(v) for v in np.nanpercentile(x, [2.5, 97.5])]

# ---------------------------------------------------------------- data
S = L.sample(); K = S["K"]; n = len(S["pifu"]); idx = {p: i for i, p in enumerate(S["pifu"])}
FJ = json.load(open(os.path.join(HERE, "lam10_fits.json"))); F = {v: {r["plateifu"]: r for r in FJ[v]} for v in ("A", "B")}
PR = json.load(open(os.path.join(L9DIR, "lam9_prepare.json"))); s5 = [r["plateifu"] for r in PR["rows"] if r["step5"]]
gA = [p for p in s5 if F["A"].get(p, {}).get("status") == "ok"]
P(f"LAM10 grade, mode {MODE}. KU2 {n}; steps 1-4 {PR['counts']['fit_ok']}; step 5 {len(s5)}; variant-A fit ok {len(gA)} (failures {len(s5) - len(gA)}) = the graded sample")
TPLJ = json.load(open(os.path.join(L9DIR, "lam9_templates.json"))); KJ = json.load(open(os.path.join(HERE, "lam10_k.json"))) if os.path.exists(os.path.join(HERE, "lam10_k.json")) else None
h4 = np.full(n, np.nan);
for p, i in idx.items():
    if p in S["FIT"] and S["FIT"][p]["status"] == "ok": h4[i] = S["FIT"][p]["h4"]
def alpha_arr(v, key):
    a = np.full(n, np.nan)
    for p in gA:
        r = F[v].get(p)
        if r is not None and r.get("status") == "ok": a[idx[p]] = r[key]
    return a
G = np.zeros(n, bool); G[[idx[p] for p in gA]] = True
grp = K["cell"] * 2 + K["slow"].astype(int)
rng0 = np.random.default_rng(SEED)
def shuffle_within(a, sel, groups):
    b = a.copy()
    for g in np.unique(groups[sel]):
        j = np.flatnonzero(sel & (groups == g)); b[j] = b[j][rng0.permutation(len(j))]
    return b
AL = {v: dict(ku2=alpha_arr(v, "alpha_ku2"), tian=alpha_arr(v, "alpha_tian"), raw=alpha_arr(v, "alpha"), gamma=alpha_arr(v, "gamma_best")) for v in ("A", "B")}
if MODE == "MUTATE":
    for v in ("A", "B"):
        for k in ("ku2", "raw", "gamma"): AL[v][k] = shuffle_within(AL[v][k], G, grp)
        # Q2's shuffle (within HX1 sigma quartiles) is applied to the Tian rows below
for v in ("A", "B"):
    m = G & np.isfinite(AL[v]["ku2"]); P(f"variant {v}: alpha_KU2 finite on {int(m.sum())}; median Gamma_b {np.nanmedian(AL[v]['gamma'][m]):.3f}, alpha {np.nanmedian(AL[v]['raw'][m]):.3f}, "
                                         f"alpha_KU2 {np.nanmedian(AL[v]['ku2'][m]):.3f} (16-84 % {np.nanpercentile(AL[v]['ku2'][m], 16):.3f}-{np.nanpercentile(AL[v]['ku2'][m], 84):.3f})")

# ---------------------------------------------------------------- checks
C1 = len(gA) >= 1000
ref = json.load(open(os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.json"))); C2 = {}
def r_of(a0, dlog=None, extra=0.0):
    lm = K["lm"] + extra + (0 if dlog is None else np.nan_to_num(dlog, nan=0.0))
    go, gb = K["accel"](K["mtm"], K["rhm"], lm); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    return np.where(ok, K["resid"](np.where(ok, go, 1), np.where(ok, gb, 1), a0), np.nan)
for foot, a0 in K["A0"].items():
    r = r_of(a0); g = np.isfinite(r); Dv, _ = K["Dstat"](r[g], K["slow"][g], K["cell"][g]); C2[foot] = bool(abs(Dv - ref[foot]["D"]) <= 1e-6)
    P(f"C2 [{foot}] KU2 D {Dv:+.6f} vs ku2.json {ref[foot]['D']:+.6f}: {'PASS' if C2[foot] else 'FAIL'}")
C4 = bool(TPLJ["C4_pass"]); P(f"C1 graded N {len(gA)} (>= 1000): {'PASS' if C1 else 'FAIL'}; C4 (templates): {'PASS' if C4 else 'FAIL'}")
iqr = float(np.subtract(*np.nanpercentile(h4[G], [75, 25])))
K1 = {v: (None if KJ is None else bool(KJ[f"K1_{v}"]["PASS"])) for v in ("A", "B")}
K2 = None if KJ is None else bool(0.69 * np.log(10) * abs(KJ["K2"]["b"]) * iqr <= 0.01 and KJ["K2"]["n"] == 100)
P(f"K1 A {K1['A']}, K1 B {K1['B']}; K2 with the graded IQR(h4) {iqr:.4f}: {K2}" + ("" if KJ is None else f" (b {KJ['K2']['b']:+.4f}, lean {0.69 * np.log(10) * abs(KJ['K2']['b']) * iqr:.4f} ln)"))
gm = G & np.isfinite(AL["A"]["gamma"]); k3 = spearmanr(AL["A"]["gamma"][gm], np.log10(K["sig"][gm]))
P(f"K3 (reported): Spearman(Gamma_b, log Sigma_Re) {k3.statistic:+.3f}, p {k3.pvalue:.2e}, n {int(gm.sum())}")
RES["checks"] = dict(C1=C1, C2=C2, C4=C4, K1=K1, K2=K2, iqr_h4=iqr, K3=dict(rho=float(k3.statistic), p=float(k3.pvalue)))

# ---------------------------------------------------------------- Q1
def q1(v, a0, extra=0.0, sel=None):
    sel = G if sel is None else sel; la = np.log10(AL[v]["ku2"]); r0 = r_of(a0, extra=extra); r1 = r_of(a0, la, extra=extra)
    m = sel & np.isfinite(r0) & np.isfinite(r1) & np.isfinite(la); i0 = np.flatnonzero(m); R0, R1 = float(np.median(r0[i0])), float(np.median(r1[i0]))
    rg = np.random.default_rng(SEED); b0, b1 = [], []
    for _ in range(NB):
        j = i0[rg.integers(0, len(i0), len(i0))]; b0.append(np.median(r0[j])); b1.append(np.median(r1[j]))
    b0, b1 = np.array(b0), np.array(b1); bf = (b0 - b1) / b0
    out = dict(N=int(m.sum()), R0=R0, R1=R1, f=(R0 - R1) / R0, R0_ci=ci(b0), R1_ci=ci(b1), f_ci=ci(bf))
    lo1, hi1 = out["R1_ci"]; flo, fhi = out["f_ci"]; lo0, hi0 = out["R0_ci"]
    if lo0 > -0.15 and hi0 < 0.15: lab = "NO VERDICT (nothing to absorb)"
    elif lo1 > -0.15 and hi1 < 0.15: lab = "IMF ABSORBS"
    elif hi1 < -0.15: lab = "IMF OVERSHOOTS"
    elif fhi < 0.5: lab = "IMF DOESN'T"
    elif flo > 0.5: lab = "IMF PARTLY"
    else: lab = "NO VERDICT"
    out["line_label"] = lab; return out, r0, r1

# ---------------------------------------------------------------- Q3
def demean(x, g):
    u, c = np.unique(g, return_inverse=True); cnt = np.bincount(c); mu = np.bincount(c, weights=x) / cnt
    return np.where(cnt[c] >= 3, x - mu[c], np.nan)
def eff(r, h, g):
    a, b = demean(r, g), demean(h, g); mm = np.isfinite(a) & np.isfinite(b)
    return float(np.sum(a[mm] * b[mm]) / np.sum(b[mm] ** 2) * iqr) if mm.sum() > 2 else float("nan")
def q3(v, a0, sel=None):
    sel = G if sel is None else sel; la = np.log10(AL[v]["ku2"]); r0 = r_of(a0); r1 = r_of(a0, la)
    m = sel & np.isfinite(r0) & np.isfinite(r1) & np.isfinite(h4) & np.isfinite(la); i0 = np.flatnonzero(m)
    E0, E1 = eff(r0[i0], h4[i0], grp[i0]), eff(r1[i0], h4[i0], grp[i0])
    rg = np.random.default_rng(SEED); b0, b1 = [], []
    for _ in range(NB):
        j = i0[rg.integers(0, len(i0), len(i0))]; b0.append(eff(r0[j], h4[j], grp[j])); b1.append(eff(r1[j], h4[j], grp[j]))
    b0, b1 = np.array(b0), np.array(b1)
    out = dict(N=int(m.sum()), E0=E0, E1=E1, dE=E1 - E0, E0_ci=ci(b0), E1_ci=ci(b1), dE_ci=ci(b1 - b0))
    (l0, h0), (l1, h1), (ld, hd) = out["E0_ci"], out["E1_ci"], out["dE_ci"]; s0 = np.sign(E0)
    if ld > -0.01 and hd < 0.01: lab = "IMF DOESN'T"
    elif (l0 > 0 or h0 < 0) and (l1 <= 0 <= h1) and (ld > 0 or hd < 0) and np.sign(E1 - E0) == -s0: lab = "IMF ABSORBS"
    elif (l1 > 0 and s0 > 0) or (h1 < 0 and s0 < 0): lab = "IMF DOESN'T"
    else: lab = "NO VERDICT"
    out["line_label"] = lab; return out
def q3_rows(v, a0):
    la = np.log10(AL[v]["ku2"]); r0 = r_of(a0); m = G & np.isfinite(r0) & np.isfinite(h4) & np.isfinite(la); i0 = np.flatnonzero(m)
    a, b, c = demean(r0[i0], grp[i0]), demean(h4[i0], grp[i0]), demean(la[i0], grp[i0]); mm = np.isfinite(a) & np.isfinite(b) & np.isfinite(c)
    X = np.c_[b[mm], c[mm]]; co = np.linalg.lstsq(X, a[mm], rcond=None)[0]
    out = dict(E_with_logalpha_covariate=float(co[0] * iqr), logalpha_coef=float(co[1]))
    for nm, s in (("slow", K["slow"]), ("fast", ~K["slow"])):
        q = q3(v, a0, sel=G & s); out[f"{nm}_E0"], out[f"{nm}_E1"] = q["E0"], q["E1"]
    sn = np.array([np.nan] * n); snp = {r["plateifu"]: r["sn_nai_scaled"] for r in PR["rows"]}
    for p in gA: sn[idx[p]] = snp[p]
    e = np.nanpercentile(sn[G], [100 / 3, 200 / 3])
    for t, (lo, hi) in enumerate(((-np.inf, e[0]), (e[0], e[1]), (e[1], np.inf))):
        q = q3(v, a0, sel=G & (sn >= lo) & (sn < hi)); out[f"sn_third{t + 1}_E0"], out[f"sn_third{t + 1}_E1"] = q["E0"], q["E1"]
    return out

# ---------------------------------------------------------------- Q2 (HX1's B1 integral, its code in memory; nothing written in HX1's folder)
HARN = ("old_gates.py", "tolerances.json", "row_marks.json")  # the harness's byte copies, as HX1 keeps them (A1 item 6)
def hx1():
    """RQ3's acceptance.py, unedited, with this folder as its working folder: byte copies of its three support files are put here for
    the run (sha256 checked against RQ3's) and removed afterwards, so nothing is written in HX1's or RQ3's folders."""
    import hashlib, shutil
    H = os.path.join(RB, "HX1_hot_ladder"); R3 = os.path.join(RB, "RQ3_acceptance_v2"); acc = os.path.join(R3, "acceptance.py")
    for f in HARN:
        shutil.copyfile(os.path.join(R3, f), os.path.join(HERE, f))
        assert hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() == hashlib.sha256(open(os.path.join(H, f), "rb").read()).hexdigest(), f
    N = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "rq3_in_lam10"}
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(acc).read(), acc, "exec"), N)
    src = open(os.path.join(H, "hx1_ladder.py")).read(); top = src.split("# ---------- SLUGGS through")[0]; stats = src.split("# ---------- statistics")[1].split("# ---------- run")[0]
    a1 = "n = hx1_acc.load();"; a2 = 'OUT = open(os.path.join(HERE, f"hx1_ladder{TAG}.out"), "w");'
    assert top.count(a1) == 1 and top.count(a2) == 1
    top = top.replace(a1, "n = _LAM9_N;").replace(a2, "import io as _io; OUT = _io.StringIO();")
    env = os.environ.pop("HX1_MUTATE", None); argv = sys.argv; sys.argv = ["hx1_ladder.py"]
    Hn = {"__file__": os.path.join(H, "hx1_ladder.py"), "__name__": "hx1_in_lam9", "_LAM9_N": N}
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(top + "\n" + stats, os.path.join(H, "hx1_ladder.py"), "exec"), Hn)
    sys.argv = argv
    if env is not None: os.environ["HX1_MUTATE"] = env
    return Hn
def q2(Hn, v, foot, a0, mutate=False):
    TI, s2, NEWT, LAW = Hn["TI"], Hn["s2"], Hn["NEWT"], Hn["LAW"]
    ma = [o for o in TI if o["cls"] == "MaNGA elliptical"]; q = np.percentile([10 ** o["ls"] for o in ma], [25, 50, 75])
    mid2i = {}
    for i in np.flatnonzero(G): mid2i.setdefault(S["mid"][i], i)
    objs = [l.rstrip("\n").split("\t")[2].strip() for l in open(os.path.join(Hn["CRG"], "inputs", "groups", "J_A_A_710_L39.tsv"))
            if len(l.split("\t")) >= 13 and l.split("\t")[0].strip().isdigit() and l.split("\t")[1].strip() == "MaNGA elliptical"]
    assert len(objs) == len(ma)
    rows = [(o, mid2i[ob]) for o, ob in zip(ma, objs) if ob in mid2i and np.isfinite(AL[v]["tian"][mid2i[ob]])]
    sig = np.array([10 ** o["ls"] for o, _ in rows]); qq = np.searchsorted(q, sig, side="left")  # HX1: (k > lo) & (k <= hi)
    al = np.array([AL[v]["tian"][i] for _, i in rows])
    if mutate:
        for k in range(4):
            j = np.flatnonzero(qq == k); al[j] = al[j][rng0.permutation(len(j))]
    def B(o, dl):
        sN, sL = s2(o, dl, NEWT, a0), s2(o, dl, LAW, a0); sO = (10 ** o["ls"] * 1e3) ** 2; return (sO - sN) / (sL - sN)
    def rung(sel, dls):
        J = np.flatnonzero(sel); Bv = np.array([B(rows[j][0], dls[j]) for j in J]); Bp = np.array([B(rows[j][0], dls[j] + 0.10) for j in J])
        Bm = np.array([B(rows[j][0], dls[j] - 0.10) for j in J]); y = Hn["ylog"](Bv)
        sy = abs(Hn["ylog"](Bp) - Hn["ylog"](Bm)) / 2; sb = Hn["boot"](Bv, np.random.default_rng(SEED)); return dict(n=int(sel.sum()), y=y, s=float(math.hypot(sb, sy)), Bmed=float(np.median(Bv)), key=float(np.median(sig[sel])))
    up = qq >= 1; d0 = np.zeros(len(rows)); d1 = np.log10(al); d1v = np.log10(0.08 + 0.92 * al)
    R0, R1, R1v = rung(up, d0), rung(up, d1), rung(up, d1v)
    if not (R0["y"] > 2 * R0["s"]): lab = "NO NEED ON THIS SUBSET"
    elif abs(R1["y"]) <= 2 * R1["s"] and abs(R1v["y"]) <= 2 * R1v["s"]: lab = "IMF ABSORBS"
    elif R1["y"] < -2 * R1["s"]: lab = "IMF OVERSHOOTS"
    elif R1["y"] > 2 * R1["s"] and R1["y"] >= 0.5 * R0["y"]: lab = "IMF DOESN'T"
    elif R1["y"] > 2 * R1["s"] and R1["y"] < 0.5 * R0["y"]: lab = "IMF PARTLY"
    else: lab = "NO VERDICT"
    quart = {f"Q{k + 1}": dict(before=rung(qq == k, d0), after=rung(qq == k, d1)) for k in range(4)}
    return dict(N_rows=int(up.sum()), before=R0, after=R1, after_092=R1v, line_label=lab, quartiles=quart, alpha_tian_median=float(np.median(al[up])))
def hx1_c3(Hn, foot, a0):
    TI, s2, NEWT, LAW = Hn["TI"], Hn["s2"], Hn["NEWT"], Hn["LAW"]; ma = [o for o in TI if o["cls"] == "MaNGA elliptical"]
    q = np.percentile([10 ** o["ls"] for o in ma], [25, 50, 75]); k = np.array([10 ** o["ls"] for o in ma])
    Bv = np.array([(lambda sN, sL, sO: (sO - sN) / (sL - sN))(s2(o, 0, NEWT, a0), s2(o, 0, LAW, a0), (10 ** o["ls"] * 1e3) ** 2) for o in ma])
    J = json.load(open(os.path.join(RB, "HX1_hot_ladder", "hx1_ladder.json")))["footings"][foot]["rungs"]; ok = True; got = {}
    for j, (lo, hi) in enumerate(zip([0, *q], [*q, 1e9])):
        m = (k > lo) & (k <= hi); got[f"Q{j + 1}"] = float(np.median(Bv[m])); ok &= abs(got[f"Q{j + 1}"] - J[f"MaNGA Q{j + 1}"]["Bmed"]) <= 1e-6
    return bool(ok), got
def lorder(Hn, foot, quart):
    J = json.load(open(os.path.join(RB, "HX1_hot_ladder", "hx1_ladder.json")))["footings"][foot]["rungs"]
    names = list(J.keys()); y = np.array([J[r]["y"] for r in names]); s = np.array([J[r]["s"] for r in names]); keys = np.array([J[r]["key"] for r in names])
    for k in range(4):
        r = f"MaNGA Q{k + 1}"; i = names.index(r); y[i] = quart[f"Q{k + 1}"]["after"]["y"]; s[i] = quart[f"Q{k + 1}"]["after"]["s"]
    if not np.all(np.isfinite(y)): return dict(p=0.0, why="SUB-NEWTONIAN rung")
    o = Hn["order_p"](keys, y, s, np.random.default_rng(20261103)); return dict(p=float(o["p"]), chi2=float(o["chi2"]))

def harness_cleanup():
    import shutil
    for f in HARN:
        if os.path.exists(os.path.join(HERE, f)): os.remove(os.path.join(HERE, f))
    if os.path.isdir(os.path.join(HERE, "cache_crg")): shutil.rmtree(os.path.join(HERE, "cache_crg"))

# ---------------------------------------------------------------- run
Hn = hx1(); LAB = {}; GR = {}
for v in ("A", "B"):
    GR[v] = {}
    for foot, a0 in K["A0"].items():
        c3ok, c3got = hx1_c3(Hn, foot, a0) if v == "A" else (True, None)
        Q1, r0, r1 = q1(v, a0); Q2 = q2(Hn, v, foot, a0, mutate=(MODE == "MUTATE")); Q3 = q3(v, a0)
        # C3: alpha = 1 reproduces R0, E0, y0
        c3a = abs(np.median(r0[G & np.isfinite(r0)]) - np.median(r_of(a0, np.zeros(n))[G & np.isfinite(r0)])) == 0.0
        R = dict(Q1=Q1, Q2=Q2, Q3=Q3, C3_hx1=c3ok, C3_hx1_got=c3got, C3_alpha1=bool(c3a))
        if MODE == "REAL" and v == "A":
            R["Q1_h70"] = q1(v, a0, extra=0.310)[0]; R["Q1_slow"] = q1(v, a0, sel=G & K["slow"])[0]; R["Q1_fast"] = q1(v, a0, sel=G & ~K["slow"])[0]
            la = np.log10(AL[v]["ku2"]); m = G & np.isfinite(r0) & np.isfinite(r1)
            R["D_slow_fast"] = dict(before=K["Dstat"](r0[m], K["slow"][m], K["cell"][m])[0], after=K["Dstat"](r1[m], K["slow"][m], K["cell"][m])[0])
            rich = S["rich"] & np.isfinite(r0); both = (G & np.isfinite(r1)) | rich; flag = G.copy()
            rr0 = np.where(both, r0, np.nan); rr1 = np.where(G, r1, r0); mm = both & np.isfinite(rr0) & np.isfinite(rr1)
            R["early_minus_late_D"] = dict(n_poor=int((mm & flag).sum()), n_rich=int((mm & ~flag).sum()),
                                           before=K["Dstat"](rr0[mm], flag[mm], K["cell"][mm])[0], after=K["Dstat"](rr1[mm], flag[mm], K["cell"][mm])[0])
            R["Q2_Lorder_after"] = lorder(Hn, foot, Q2["quartiles"]); R["Q3_rows"] = q3_rows(v, a0)
        if MODE == "REAL":
            red = S["ur"] > 2.0; col = {}
            for nm, s in (("red", G & red), ("blue", G & ~red & np.isfinite(S["ur"]))):
                a = AL[v]["ku2"][s & np.isfinite(AL[v]["ku2"])]; rg = np.random.default_rng(SEED)
                bs = [np.median(a[rg.integers(0, len(a), len(a))]) for _ in range(NB)] if len(a) > 1 else [np.nan]
                qq = q1(v, a0, sel=s)[0] if s.sum() > 5 else None
                col[nm] = dict(n=int(len(a)), alpha_ku2_median=float(np.median(a)) if len(a) else float("nan"), ci=ci(bs), R1_minus_R0=(qq["R1"] - qq["R0"]) if qq else float("nan"))
            R["colour_row"] = col
        GR[v][foot] = R
# Gamma_b detail rows (variant A), reported
if MODE == "REAL":
    rA = [F["A"][p] for p in gA]; zz = np.array([r["z"] for r in rA]); gg = np.array([r["gamma_best"] for r in rA]); ii = np.array([idx[p] for p in gA])
    sg = np.array([r["sigma"] for r in rA], float); lb = np.array([r["lalpha_chi"] - np.log10(r["alpha"]) for r in rA])
    det = dict(spearman={}, by_z={}, edge_hits=int(sum(1 for r in rA if r["edge"])), edge_low=int(sum(1 for r in rA if r["edge"] == "low")), edge_high=int(sum(1 for r in rA if r["edge"] == "high")),
               sigma_median=float(np.nanmedian(sg)), sigma_undefined=int(np.sum(~np.isfinite(sg))), beside_minus_primary_lalpha_median=float(np.median(lb)),
               age_median_gyr=float(10 ** (np.median([r["lage"] for r in rA]) - 9)), mh_median=float(np.median([r["mh"] for r in rA])))
    for nm, x in (("log_sigma", np.log10(K["sig"][ii])), ("log_mstar", K["lm"][ii]), ("h4", h4[ii]), ("lage", np.array([r["lage"] for r in rA])), ("mh", np.array([r["mh"] for r in rA]))):
        t = spearmanr(gg, x); det["spearman"][nm] = [float(t.statistic), float(t.pvalue)]
    for nm, (lo, hi) in (("z<=0.037", (0, 0.037)), ("0.037-0.063", (0.037, 0.063)), ("z>0.063", (0.063, 1))):
        m = (zz > lo) & (zz <= hi) if lo > 0 else (zz <= hi)
        det["by_z"][nm] = dict(n=int(m.sum()), gamma=float(np.median(gg[m])), alpha_ku2=float(np.median([rA[j]["alpha_ku2"] for j in np.flatnonzero(m)])), sigma=float(np.nanmedian(sg[m])))
    RES["gamma_detail"] = det
    P("\nGamma_b detail (variant A, reported): Spearman of Gamma_best with " + json.dumps({k: (np.round(v, 3).tolist() if isinstance(v, list) else v) for k, v in det["spearman"].items()}))
    P(f"  edge hits {det['edge_hits']} (low {det['edge_low']}, high {det['edge_high']}); median sigma(Gamma_b) {det['sigma_median']:.3f} (undefined {det['sigma_undefined']}); "
      f"beside estimator minus primary, median log alpha {det['beside_minus_primary_lalpha_median']:+.4f}; light-weighted age {det['age_median_gyr']:.2f} Gyr, [M/H] {det['mh_median']:+.3f}")
    for k, v in det["by_z"].items(): P(f"  {k}: n {v['n']}, Gamma_best {v['gamma']:.3f}, alpha_KU2 {v['alpha_ku2']:.3f}, sigma {v['sigma']:.3f}")
# M1 (Q3 null) from the MUTATE run
mp = os.path.join(HERE, "lam10_grade_MUTATE.json"); M1 = None
if MODE == "REAL" and os.path.exists(mp):
    MJ = json.load(open(mp)); M1 = {f: bool(MJ["A"][f]["Q3"]["dE_ci"][0] <= 0 <= MJ["A"][f]["Q3"]["dE_ci"][1]) for f in K["A0"]}
def label(v, foot, q):
    R = GR[v][foot]; c3 = R["C3_alpha1"] and GR["A"][foot]["C3_hx1"]
    if not (C4 and all(C2.values()) and c3): return "NO VERDICT (code check failed)"
    k1 = K1[v]
    if k1 is False: return "NOT MEASURABLE (K1 fails)"
    if q in ("Q1", "Q3") and not C1: return "NOT MEASURABLE (C1)"
    if q == "Q2" and R["Q2"]["N_rows"] < 150: return "NOT MEASURABLE (C1)"
    if q == "Q3" and K2 is False: return "NOT MEASURABLE (K2 fails)"
    if q == "Q3" and M1 is not None and M1[foot] is False: return "NO VERDICT (M1 fails)"
    lab = R[q]["line_label"]; prov = [x for x, y in (("K1", k1), ("K2", K2 if q == "Q3" else True), ("M1", M1 if q == "Q3" else True)) if y is None]
    return lab + (f" (PROVISIONAL: {', '.join(prov)} not run)" if prov else "")
for foot in K["A0"]:
    LAB[foot] = {}
    for q in ("Q1", "Q2", "Q3"):
        a, b = label("A", foot, q), label("B", foot, q)
        if K1["B"] is False: a += " (Na I robustness not tested)"
        elif a.split(" (")[0] != b.split(" (")[0]: a += " (NOT ROBUST TO Na I)"
        LAB[foot][q] = dict(A=a, B=b)
RES.update(graded_N=len(gA), A=GR["A"], B=GR["B"], labels=LAB, M1=M1)

# ---------------------------------------------------------------- print
for v in (("A",) if MODE == "MUTATE" else ("A", "B")):
    for foot in K["A0"]:
        R = GR[v][foot]; q1r, q2r, q3r = R["Q1"], R["Q2"], R["Q3"]
        P(f"\n[{v} {foot}] Q1: N {q1r['N']}; R0 {q1r['R0']:+.3f} {np.round(q1r['R0_ci'], 3).tolist()}, R1 {q1r['R1']:+.3f} {np.round(q1r['R1_ci'], 3).tolist()} ln; "
          f"removed f {q1r['f']:+.3f} {np.round(q1r['f_ci'], 3).tolist()}" + (f" -> {LAB[foot]['Q1'][v]}" if MODE == "REAL" else ""))
        P(f"[{v} {foot}] Q2: rows {q2r['N_rows']}; y0 {q2r['before']['y']:+.3f} +- {q2r['before']['s']:.3f} (B {q2r['before']['Bmed']:.2f}), y1 {q2r['after']['y']:+.3f} +- {q2r['after']['s']:.3f} "
          f"(B {q2r['after']['Bmed']:.2f}); 0.92-Mbar variant y1 {q2r['after_092']['y']:+.3f}; median alpha_Tian {q2r['alpha_tian_median']:.3f}" + (f" -> {LAB[foot]['Q2'][v]}" if MODE == "REAL" else ""))
        P(f"[{v} {foot}] Q3: N {q3r['N']}; E0 {q3r['E0']:+.4f} {np.round(q3r['E0_ci'], 4).tolist()}, E1 {q3r['E1']:+.4f} {np.round(q3r['E1_ci'], 4).tolist()}, "
          f"dE {q3r['dE']:+.4f} {np.round(q3r['dE_ci'], 4).tolist()}" + (f" -> {LAB[foot]['Q3'][v]}" if MODE == "REAL" else ""))
        if MODE == "REAL" and v == "A":
            P(f"[{v} {foot}] C3: HX1 MaNGA Bmed reproduced {R['C3_hx1']}; alpha = 1 reproduces R0 {R['C3_alpha1']}")
            h = R["Q1_h70"]; P(f"[{v} {foot}] row Q1 with h70 masses: R0 {h['R0']:+.3f}, R1 {h['R1']:+.3f}, f {h['f']:+.3f} {np.round(h['f_ci'], 3).tolist()} -> lines read {h['line_label']}")
            P(f"[{v} {foot}] row Q1 slow: R0 {R['Q1_slow']['R0']:+.3f} R1 {R['Q1_slow']['R1']:+.3f}; fast: R0 {R['Q1_fast']['R0']:+.3f} R1 {R['Q1_fast']['R1']:+.3f}; "
              f"KU2 D slow-fast before {R['D_slow_fast']['before']:+.4f} after {R['D_slow_fast']['after']:+.4f}")
            e = R["early_minus_late_D"]; P(f"[{v} {foot}] row early-minus-late D (gas-poor {e['n_poor']} vs gas-bearing {e['n_rich']}): before {e['before']:+.4f}, after {e['after']:+.4f}")
            P(f"[{v} {foot}] row Q2 quartiles y before/after: " + ", ".join(f"{k} {q2r['quartiles'][k]['before']['y']:+.3f}/{q2r['quartiles'][k]['after']['y']:+.3f} (n {q2r['quartiles'][k]['after']['n']})" for k in q2r["quartiles"])
              + f"; HX1 L-ORDER with these MaNGA rungs: p {R['Q2_Lorder_after'].get('p')}")
            qr = R["Q3_rows"]; P(f"[{v} {foot}] row Q3: E with log alpha as covariate {qr['E_with_logalpha_covariate']:+.4f}; slow E0/E1 {qr['slow_E0']:+.4f}/{qr['slow_E1']:+.4f}; fast {qr['fast_E0']:+.4f}/{qr['fast_E1']:+.4f}")
        if MODE == "REAL":
            c = R["colour_row"]; P(f"[{v} {foot}] colour row (ungraded): red (u-r > 2.0) n {c['red']['n']}, alpha_KU2 {c['red']['alpha_ku2_median']:.3f} {np.round(c['red']['ci'], 3).tolist()}, "
                                   f"R1-R0 {c['red']['R1_minus_R0']:+.3f}; blue n {c['blue']['n']}, alpha_KU2 {c['blue']['alpha_ku2_median']:.3f} {np.round(c['blue']['ci'], 3).tolist()}, R1-R0 {c['blue']['R1_minus_R0']:+.3f}")
if MODE == "MUTATE":
    for foot in K["A0"]:
        d = GR["A"][foot]["Q3"]["dE_ci"]; P(f"M1 [{foot}] dE interval {np.round(d, 4).tolist()} includes 0: {'PASS' if d[0] <= 0 <= d[1] else 'FAIL'}")
else:
    P("\nLABELS (variant A; B in brackets):")
    for foot in K["A0"]:
        for q in ("Q1", "Q2", "Q3"): P(f"  {foot} {q}: {LAB[foot][q]['A']}   [B: {LAB[foot][q]['B']}]")
harness_cleanup()
sfx = "" if MODE == "REAL" else f"_{MODE}"
open(os.path.join(HERE, f"lam10_grade{sfx}.out"), "w", encoding="utf-8").write("\n".join(OUT) + "\nκ = ½ FITTED; not theory closed.\n")
json.dump(RES, open(os.path.join(HERE, f"lam10_grade{sfx}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
if MODE == "REAL":
    B = {k: RES[k] for k in ("lane", "mode", "note", "graded_N")}; B["B"] = GR["B"]; B["labels_B"] = {f: {q: LAB[f][q]["B"] for q in LAB[f]} for f in LAB}
    json.dump(B, open(os.path.join(HERE, "lam10_grade_B.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
    open(os.path.join(HERE, "lam10_grade_B.out"), "w", encoding="utf-8").write("\n".join(l for l in OUT if l.startswith("[B") or l.startswith("  ")) + "\nκ = ½ FITTED; not theory closed.\n")
