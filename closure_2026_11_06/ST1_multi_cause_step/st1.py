#!/usr/bin/env python3
"""ST1 (criteria 3622fad837): does the hot/cold step have several causes? GB1's battery (exec'd read-only), the plain
law throughout, each class's data side corrected by its frozen systematic.
    python3 st1.py           -> st1.json / st1.out
    python3 st1.py --mutate  -> st1_MUTATE.json / .out   (M1 Newton, M2 inverted IMF, M3 cut limits)
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.dirname(HERE); REPO = os.path.dirname(CL)
MUTATE = "--mutate" in sys.argv; TAG = "st1_MUTATE" if MUTATE else "st1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ GB1, read-only, up to its main block
GBP = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); src = open(GBP).read()
cut = src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GBP, "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "gb1_lib", "exec"), NS); sys.argv = _a
A0 = NS["A0"]; G = NS["G"]
for k in ("g_sparc", "g_xcop", "g_groups", "g_ell", "g_udg", "g_dsph", "g_kids", "g_ss", "L0", "L1", "NEWTON", "delta", "b_imf",
          "groups_pts", "build", "udgs", "dsphs", "kids", "R1", "X1R", "LW", "GRADED_D", "Missing", "filled", "dl", "STOT", "DX"):
    globals()[k] = NS[k]
GB = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
Q26 = json.load(open(os.path.join(CL, "QX26_imf_variation", "qx26.json")))
Q24 = json.load(open(os.path.join(CL, "QX24_environment_key", "iter_1", "qx24.json")))
HC = json.load(open(os.path.join(CL, "HC1_hot_fermion_all_gates", "hc1.json")))
Q12 = json.load(open(os.path.join(CL, "QX12_triangle", "iter_3_isothermal_sea", "qx12_i3.json")))
LN10 = math.log(10)
RES = dict(tag=TAG, criteria="3622fad837", note="kappa = 1/2 FITTED; not theory closed", footings={}, KA={})
P(f"ST1 multi-cause step {'MUTATE' if MUTATE else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ batteries (exactly as gb1 main builds them)
BATT = {}
for f, a0 in A0.items():
    S, E, X = build(f, a0); GRp = {0: groups_pts(a0, 0.0), 1: groups_pts(a0, 1.0)}
    st = R1[f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / LN10
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=udgs(f, a0), D=dsphs(f, a0), K=kids(a0), sigU=sigU, s1row=st)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S]))); BATT[f] = B

# ------------------------------------------------------------------ S-D tidal susceptibility (QX24 replay, verbatim)
GPC = 4.30091e-3; VC = {"MW": 200.0, "M31": 230.0}
SAT_CLASSES = ("MW classical", "bright M31", "M31 others", "M31 dE")
def taus(f):
    ps = LW["footings"][f]["per_system"]; x1 = {n: r for (ff, n), r in X1R.items() if ff == f}
    names = [n for n in ps if n in x1]; tau = {}
    for n in names:
        r = x1[n]; host = r["host"]
        if host not in VC: continue
        Re = float(r["rh_pc"]); sg = float(r["sigma"]); d = float(r["d_host_kpc"]) * 1e3
        MW_ = 4 * sg ** 2 * Re / GPC; Mh = VC[host] ** 2 * d / GPC
        tau[n] = Re / (d * (MW_ / (3 * Mh)) ** (1 / 3))
    sats = [n for n in names if (ps[n]["cls"] in SAT_CLASSES or ps[n]["cls"].startswith("indiv:")) and n in tau]
    return tau, sats
TAU_LINE = 0.375; PERI = 3 ** (2 / 3)
CUT_CLASSES = ("bright M31", "MW classical")
def cut_D(B, tau, line, scale=1.0):
    D = {c: list(v) for c, v in B["D"].items()}; info = {}
    for c in CUT_CLASSES:
        keep = [p for p in D[c] if (p["name"] not in tau) or tau[p["name"]] * scale < line]
        info[c] = dict(N_raw=len(D[c]), N_kept=len(keep), dropped=[p["name"] for p in D[c] if p not in keep],
                       no_tau=[p["name"] for p in D[c] if p["name"] not in tau]); D[c] = keep
    return D, info
def g6_cut(c, B, a0, tau, line, scale=1.0):
    D, info = cut_D(B, tau, line, scale); B2 = dict(B, D=D)
    if any(len(D[k]) < 5 for k in CUT_CLASSES):
        return "NO VERDICT", None, info
    ok, num = g_dsph(c, B2, a0); return ("PASS" if ok else "FAIL"), num, info

def st(ok): return "PASS" if ok else "FAIL"
def fnum(n, d=4): return f"{n:+.{d}f}"

# ------------------------------------------------------------------ inverted-IMF twin candidate (M2)
def L1INV(f, a0): return lambda ft: dict(b=1.0 / b_imf(ft), F=1.0, T=0.0)
def BF(fx): return lambda f, a0: (lambda ft: dict(b=1.0 + fx, F=1.0, T=0.0))

for f, a0 in A0.items():
    B = BATT[f]; R = {}; RES["footings"][f] = R
    base = NEWTON(f, a0) if MUTATE else L0(f, a0)
    P(f"\n================ [{f}] a0 {a0:.4e}  Lstar {NS['LSTAR'][f]} pc  ({'M1 Newton' if MUTATE else 'plain law L0'})")
    # ---------------- raw GB1 cells
    raw = {}
    raw["G1"] = g_sparc(base, B, a0); raw["G2"] = g_xcop(base, B, a0); raw["G3"] = g_groups(base, B, a0); raw["G4"] = g_ell(base, B, a0)
    raw["G5"] = g_udg(base, B, a0); raw["G6"] = g_dsph(base, B, a0); raw["G7"] = g_kids(base, B, a0); raw["G8"] = g_ss(base, B, a0)
    # ---------------- KA1: L0 reproduces gb1.json
    if not MUTATE:
        gl = GB["cands"]["L0"][f]; d = []
        mp = {"G1": "G1 SPARC", "G2": "G2 X-COP", "G3": "G3 groups", "G4": "G4 ellipticals", "G5": "G5 Coma UDGs", "G6": "G6 dSph classes", "G7": "G7 KiDS split", "G8": "G8 Solar System"}
        for k, gn in mp.items():
            a, b = raw[k][1], gl[gn]["num"]
            if k == "G1": d += [a["Z"] - b["Z"], a["rms"] - b["rms"]]
            if k == "G2": d += [a["mean"] - b["mean"], a["rms"] - b["rms"]]
            if k == "G3": d += [a[s]["n_pass"] - b[s]["n_pass"] for s in ("fst0", "fst1")] + [a[s]["median_res"] - b[s]["median_res"] for s in ("fst0", "fst1")]
            if k in ("G4",): d += [a["mean"] - b["mean"]]
            if k == "G5": d += [a["mean"] - b["mean"], a["z"] - b["z"]]
            if k == "G6": d += [a[c]["median_minus_anchor"] - b[c]["median_minus_anchor"] for c in GRADED_D] + [a[c]["ci"][i] - b[c]["ci"][i] for c in GRADED_D for i in (0, 1)]
            if k == "G7": d += [a["R"] - b["R"]]
            if k == "G8": d += [a["worst_planet_use"] - b["worst_planet_use"], a["cassini_use"] - b["cassini_use"]]
        m1 = float(max(abs(x) for x in d)); RES["KA"][f"KA1_{f}"] = dict(n=len(d), maxdiff=m1, ok=m1 <= 1e-9)
        P(f"KA1 L0 vs gb1.json ({len(d)} numbers): max|d| {m1:.1e} -> {st(m1 <= 1e-9)}")

    # ---------------- S-E ellipticals: IMF
    cE = (L1INV(f, a0) if MUTATE else L1(f, a0))
    okE, nE = g_ell(cE, B, a0)
    rob = {}
    if not MUTATE:
        for sc in (0.9, 1.1):
            pts = [dict(p, feat=dict(p["feat"], stars=[dict(s, sigma=s["sigma"] * sc) for s in p["feat"]["stars"]])) for p in B["E"]]
            rob[str(sc)] = g_ell(cE, dict(B, E=pts), a0)[1]["mean"]
        d2 = abs(nE["mean"] - Q26["foot"][f]["ellipticals"]["D_imf"]); RES["KA"][f"KA2_{f}"] = dict(diff=d2, ok=d2 <= 1e-6)
        P(f"KA2 S-E vs QX26 D_imf {Q26['foot'][f]['ellipticals']['D_imf']:+.6f}: |d| {d2:.1e} -> {st(d2 <= 1e-6)}")
    R["G4"] = dict(raw=raw["G4"][1]["mean"], corrected=nE["mean"], status=st(okE), sigma_x09_x11=rob, line=0.15,
                   systematic="IMF, Posacki+2015 via QX26" if not MUTATE else "M2: inverted IMF b = 1/f_IMF")
    P(f"G4 ellipticals: raw {raw['G4'][1]['mean']:+.4f} -> {'inverted IMF' if MUTATE else 'IMF'} {nE['mean']:+.4f} (line 0.15) {st(okE)}"
      + (f"; sigma x0.9 {rob['0.9']:+.4f}, x1.1 {rob['1.1']:+.4f}" if rob else ""))

    # ---------------- S-K KiDS: IMF bracket
    cK = base if MUTATE else L1(f, a0); kb = {}
    for s_e in (130, 170, 210):
        ok, n = g_kids(cK, B, a0, {"sig_early": s_e, "sig_late": 60}); kb[str(s_e)] = dict(ok=bool(ok), R=n["R"], z=n["z"])
    oks = [v["ok"] for v in kb.values()]; sK = "PASS" if all(oks) else ("FAIL" if not any(oks) else "MIXED")
    if not MUTATE:
        d3 = max(abs(kb[k]["R"] - Q26["foot"][f]["kids"]["bracket"][k]["R"]) for k in kb); RES["KA"][f"KA3_{f}"] = dict(diff=d3, ok=d3 <= 1e-4)
        P(f"KA3 S-K vs QX26 KiDS R bracket: max|d| {d3:.1e} -> {st(d3 <= 1e-4)} (as frozen)")
        # post-freeze, disclosed: QX26 linearises (slope dlog g_law/dlog g_N x log10 f_IMF, late at the Kroupa floor); replay that formula
        def slope_(g, h=1e-4): return (math.log(NS["glaw"](g * (1 + h), a0)) - math.log(NS["glaw"](g * (1 - h), a0))) / (math.log(1 + h) - math.log(1 - h))
        gk_ = NS["gk"]; K1_ = NS["K1"]; dlin = {}
        for s_e in (130, 170, 210):
            fk = NS["alpha"](s_e) / 0.63; dlin[str(s_e)] = float(np.mean([slope_(gk_[i]) * math.log10(fk) for i in K1_]))
        d3l = max(abs((Q26["foot"][f]["kids"]["DX"] - dlin[k]) - Q26["foot"][f]["kids"]["bracket"][k]["R"]) for k in dlin)
        d3x = max(abs(DX - Q26["foot"][f]["kids"]["DX"]), 0.0)
        RES["KA"][f"KA3_{f}"]["linear_replay_diff"] = d3l; RES["KA"][f"KA3_{f}"]["DX_diff"] = d3x
        RES["KA"][f"KA3_{f}"]["exact_minus_linear_R"] = {k: kb[k]["R"] - (DX - dlin[k]) for k in dlin}
        P(f"KA3' (post-freeze) QX26's linearised formula replayed: max|d| {d3l:.1e}, DX |d| {d3x:.1e} -> {st(d3l <= 1e-8 and d3x <= 1e-9)} (line 1e-8: finite-difference slope, h 1e-4); "
          f"exact - linear R: " + ", ".join(f"{k} {kb[k]['R'] - (DX - dlin[k]):+.1e}" for k in dlin))
    R["G7"] = dict(raw=raw["G7"][1]["R"], raw_z=raw["G7"][1]["z"], bracket=kb, status=sK, line_2sigma=2 * STOT)
    P(f"G7 KiDS: raw R {raw['G7'][1]['R']:+.4f} ({raw['G7'][1]['z']:+.2f} sigma) -> IMF " + ", ".join(f"{k}: R {v['R']:+.4f} ({v['z']:+.2f})" for k, v in kb.items()) + f" -> {sK}")

    # ---------------- S-D dSphs: equilibrium cut
    tau, sats = taus(f)
    if not MUTATE:
        tq = [float(x) for x in np.percentile([tau[n] for n in sats], [10, 50, 90])]; ref = Q24["foot"][f]["T3"]["tau_p10_p50_p90"]
        d4 = max(abs(a - b) for a, b in zip(tq, ref)); RES["KA"][f"KA4_{f}"] = dict(tau_p=tq, qx24=ref, diff=d4, ok=d4 <= 1e-9)
        P(f"KA4 tau p10/p50/p90 {tq[0]:.4f}/{tq[1]:.4f}/{tq[2]:.4f} vs QX24: max|d| {d4:.1e} -> {st(d4 <= 1e-9)}")
    sD, nD, iD = g6_cut(base, B, a0, tau, TAU_LINE)
    sP, nP, iP = g6_cut(base, B, a0, tau, TAU_LINE, PERI)
    sS, nS, iS = g6_cut(base, B, a0, tau, 0.05)
    # M3 limits
    m3a = g6_cut(base, B, a0, tau, 1e9); m3b = g6_cut(base, B, a0, tau, 0.0)
    m3_ok = (m3a[1] is not None and all(abs(m3a[1][c]["median_minus_anchor"] - raw["G6"][1][c]["median_minus_anchor"]) <= 1e-12 and
                                         max(abs(m3a[1][c]["ci"][i] - raw["G6"][1][c]["ci"][i]) for i in (0, 1)) <= 1e-12 for c in GRADED_D)
             and m3b[0] == "NO VERDICT")
    # T3b direction over the graded satellites
    gs = [(math.log10(tau[p["name"]]), p["D"]) for c in CUT_CLASSES for p in B["D"][c] if p["name"] in tau]
    lt, ov = np.array([a for a, _ in gs]), np.array([b for _, b in gs])
    from scipy.stats import spearmanr
    rho = spearmanr(lt, ov); sl, ic = np.polyfit(lt, ov, 1); anchor = raw["G6"][1]  # anchor via the class numbers
    spa = g_sparc(base, B, a0)[1]["Z"]
    kept_t = [tau[p["name"]] for c in CUT_CLASSES for p in B["D"][c] if p["name"] in tau and tau[p["name"]] < TAU_LINE]
    t3b = dict(N=len(gs), spearman=[float(rho[0]), float(rho[1])], slope_per_dex=float(sl), at_line=float(ic + sl * math.log10(TAU_LINE)) - spa,
               at_kept_median=float(ic + sl * math.log10(np.median(kept_t))) - spa)
    R["G6"] = dict(raw={c: raw["G6"][1][c] for c in GRADED_D}, raw_status=st(raw["G6"][0]),
                   cut=dict(status=sD, num=({c: nD[c] for c in GRADED_D} if nD else None), info=iD),
                   pericentre=dict(status=sP, num=({c: nP[c] for c in GRADED_D} if nP else None), info=iP),
                   strict_005=dict(status=sS, info=iS), T3b=t3b, M3_ok=bool(m3_ok), tau_line=TAU_LINE)
    P(f"G6 dSphs raw: " + "; ".join(f"{c} {raw['G6'][1][c]['median_minus_anchor']:+.3f} [{raw['G6'][1][c]['ci'][0]:+.3f},{raw['G6'][1][c]['ci'][1]:+.3f}]" for c in GRADED_D) + f" -> {st(raw['G6'][0])}")
    for lab, s_, n_, i_ in (("equilibrium cut tau<0.375 (GRADED)", sD, nD, iD), ("pericentre tau x 2.08 (reported)", sP, nP, iP), ("strict tau<0.05 (reported)", sS, nS, iS)):
        P(f"   {lab}: kept " + ", ".join(f"{c} {i_[c]['N_kept']}/{i_[c]['N_raw']}" for c in CUT_CLASSES) + " -> " + s_ +
          ("; " + "; ".join(f"{c} {n_[c]['median_minus_anchor']:+.3f} [{n_[c]['ci'][0]:+.3f},{n_[c]['ci'][1]:+.3f}]" for c in GRADED_D) if n_ else ""))
        P(f"      dropped: {', '.join(i_['bright M31']['dropped'] + i_['MW classical']['dropped']) or 'none'}; no tau: {', '.join(i_['bright M31']['no_tau'] + i_['MW classical']['no_tau']) or 'none'}")
    P(f"   T3b direction (graded satellites N {t3b['N']}): Spearman(offset, log tau) {rho[0]:+.3f} (p {rho[1]:.3f}); slope {sl:+.3f} dex/dex; "
      f"line at tau 0.375 {t3b['at_line']:+.3f}, at kept median {t3b['at_kept_median']:+.3f} (minus anchor)")
    P(f"   M3 (no cut reproduces raw; zero line -> NO VERDICT): {'PASS' if m3_ok else 'FAIL'}")

    # ---------------- S-U Coma UDGs
    row = B["s1row"]; se, ss = row["se"], row["sigma_sys"]; sM, sA, sDd = row["s_M"], row["s_A"], row["s_D"]
    d5 = abs(math.hypot(se, ss) / LN10 - B["sigU"]); RES["KA"][f"KA5_{f}"] = dict(diff=d5, ok=d5 <= 1e-12)
    m = raw["G5"][1]["mean"]; edge = (sM + sA + sDd) / LN10
    readQ = dict(mean=m, line=2 * B["sigU"], z=m / B["sigU"], ok=bool(abs(m) <= 2 * B["sigU"]))
    resL = m - edge; readL = dict(residual=resL, edge_dex=edge, line=2 * se / LN10, z=resL / (se / LN10), ok=bool(abs(resL) <= 2 * se / LN10))
    var = {k: COMA for k, COMA in R1.items() if k.startswith(f"{f}|") and (("field/2" in k or "dproj" in k) and "floor" in k or "isolated" in k)}
    R["G5"] = dict(raw=m, Q=readQ, L=readL, status="PASS" if (readQ["ok"] or readL["ok"]) else "FAIL",
                   components_ln=dict(se=se, s_M=sM, s_A=sA, s_D=sDd, sigma_sys=ss),
                   host_variants_reported={k: dict(meanE_dex=v["meanE"] / LN10, z_sys=v.get("z_sys")) for k, v in var.items()})
    P(f"KA5 sigma_U from S1 se/sigma_sys: |d| {d5:.1e} -> {st(d5 <= 1e-12)}")
    P(f"G5 UDGs raw {m:+.4f} dex. Q: {m / B['sigU']:+.2f} sigma_U (line 2) {st(readQ['ok'])}. L: edges M {sM / LN10:.3f} + sigma {sA / LN10:.3f} + D {sDd / LN10:.3f} = {edge:.3f} dex -> residual {resL:+.4f}, "
      f"{readL['z']:+.2f} sigma_stat (line 2, se {se / LN10:.3f}) {st(readL['ok'])} -> {R['G5']['status']}")
    for k, v in var.items(): P(f"   reported host variant {k.split('|', 1)[1]}: {v['meanE'] / LN10:+.3f} dex, z_sys {(v.get('z_sys') if v.get('z_sys') is not None else float('nan')):+.2f}")

    # ---------------- unchanged rows
    R["G1"] = dict(status=st(raw["G1"][0]), num=raw["G1"][1]); R["G2"] = dict(status=st(raw["G2"][0]), num=raw["G2"][1])
    R["G3"] = dict(status=st(raw["G3"][0]), num=raw["G3"][1]); R["G8"] = dict(status=st(raw["G8"][0]), num=raw["G8"][1])
    P(f"G1 SPARC Z {raw['G1'][1]['Z']:+.4f} rms {raw['G1'][1]['rms']:.4f} {R['G1']['status']}; G2 X-COP {raw['G2'][1]['mean']:+.4f} rms {raw['G2'][1]['rms']:.4f} {R['G2']['status']}; "
      f"G3 groups {raw['G3'][1]['fst0']['n_pass']}/{raw['G3'][1]['fst1']['n_pass']} of 20 (med {raw['G3'][1]['fst0']['median_res']:+.3f}/{raw['G3'][1]['fst1']['median_res']:+.3f}) {R['G3']['status']}; G8 {R['G8']['status']}")
    if not MUTATE:
        RES["footings"][f]["hot_IMF_reported"] = {g: GB["cands"]["L1"][f][g]["bracket"]["runs"] for g in ("G2 X-COP", "G3 groups")}
        P("   reported: IMF on hot (GB1 L1 bracket) X-COP " + ", ".join(f"{r['num']['mean']:+.3f}" for r in GB["cands"]["L1"][f]["G2 X-COP"]["bracket"]["runs"]) +
          "; groups pass " + ", ".join(f"{r['num']['fst0']['n_pass']}/{r['num']['fst1']['n_pass']}" for r in GB["cands"]["L1"][f]["G3 groups"]["bracket"]["runs"]))

    if MUTATE: continue
    # ---------------- section 2: remaining classes and f targets
    def solve_f(stat):
        lo, hi = 0.0, 1.0
        while stat(hi) > 0 and hi < 1e6: hi *= 2
        if stat(hi) > 0: return float("inf")
        for _ in range(80):
            mid = 0.5 * (lo + hi); (lo, hi) = (mid, hi) if stat(mid) > 0 else (lo, mid)
        return 0.5 * (lo + hi)
    def mres(pts, fx): return float(np.mean([p["D"] for p in pts] - dl(BF(fx)(f, a0), pts, a0)))
    def gres(fst, fx): return float(np.median([p["D"] - delta(BF(fx)(f, a0), p["feat"], a0) for g in B["GR"][fst] for p in g["pts"]]))
    def dres(cls, pts, fx): return float(np.median([p["D"] for p in pts] - dl(BF(fx)(f, a0), pts, a0)) - spa)
    Dcut, _ = cut_D(B, tau, TAU_LINE)
    remain = {}
    if R["G2"]["status"] == "FAIL": remain["X-COP"] = dict(residual=raw["G2"][1]["mean"], f=solve_f(lambda x: mres(B["X"], x)))
    if R["G3"]["status"] == "FAIL": remain["groups"] = dict(residual=[raw["G3"][1]["fst0"]["median_res"], raw["G3"][1]["fst1"]["median_res"]],
                                                           f=[solve_f(lambda x: gres(0, x)), solve_f(lambda x: gres(1, x))])
    if R["G4"]["status"] == "FAIL": remain["ellipticals"] = dict(residual=nE["mean"])
    if R["G5"]["status"] == "FAIL":
        # target applied on the linear-edge (most generous) residual: f such that mean(D - edge - Delta_f) = 0
        remain["Coma UDGs"] = dict(residual=resL, residual_Q=m, f_L=solve_f(lambda x: mres(B["U"], x) - edge), f_raw=solve_f(lambda x: mres(B["U"], x)))
    if sD == "FAIL":
        for c in GRADED_D:
            if nD[c]["ci"][0] > 0: remain[f"dSph {c}"] = dict(residual=nD[c]["median_minus_anchor"], ci=nD[c]["ci"], f=solve_f(lambda x, c=c: dres(c, Dcut[c], x)))
    if sK != "PASS": remain["KiDS early"] = dict(residual={k: v["R"] for k, v in kb.items()})
    R["remaining"] = remain
    P("REMAINING above the law after the systematics: " + ("; ".join(f"{k} {json.dumps(v, default=lambda o: round(o, 4))}" for k, v in remain.items()) or "none"))

if not MUTATE:
    # ------------------------------------------------------------------ KA6 + section 3: reduced battery, record test objects
    k6 = []
    for f, ref in (("canonical", 0.392), ("alt", 0.360)): k6.append(abs(HC["footings"][f]["HC1"]["G2 X-COP"]["num"]["mean"] - ref))
    for f, ref in (("canonical", -0.713), ("alt", -0.724)): k6.append(abs(Q12["foot"][f]["c_min"]["X_mean"] - ref))
    RES["KA"]["KA6"] = dict(maxdiff=float(max(k6)), ok=bool(max(k6) <= 5e-4)); P(f"\nKA6 HC1 / QX12 record cells read back: max|d| {max(k6):.1e} -> {st(max(k6) <= 5e-4)}")
    RED = {}
    for f, a0 in A0.items():
        R = RES["footings"][f]; h = HC["footings"][f]["HC1"]; rr = {}
        sh4 = R["G4"]["raw"] - R["G4"]["corrected"]; r4 = h["G4 ellipticals"]["num"]["mean"] - sh4; rr["G4"] = dict(v=r4, status=st(abs(r4) <= 0.15))
        r7 = {k: h["G7 KiDS split"]["num"]["R"] - (R["G7"]["raw"] - v["R"]) for k, v in R["G7"]["bracket"].items()}
        o7 = [abs(v) < 2 * STOT for v in r7.values()]; rr["G7"] = dict(v=r7, status="PASS" if all(o7) else ("FAIL" if not any(o7) else "MIXED"))
        if R["G6"]["cut"]["num"]:
            s6 = {c: R["G6"]["raw"][c]["median_minus_anchor"] - R["G6"]["cut"]["num"][c]["median_minus_anchor"] for c in GRADED_D}
            v6 = {c: dict(med=h["G6 dSph classes"]["num"][c]["median_minus_anchor"] - s6[c], ci=[x - s6[c] for x in h["G6 dSph classes"]["num"][c]["ci"]]) for c in GRADED_D}
            rr["G6"] = dict(v=v6, status=st(all(v["ci"][0] <= 0 <= v["ci"][1] for v in v6.values())))
        else: rr["G6"] = dict(v=None, status="NO VERDICT")
        hm = h["G5 Coma UDGs"]["num"]["mean"]; okQ = abs(hm) <= 2 * BATT[f]["sigU"]; okL = abs(hm - R["G5"]["L"]["edge_dex"]) <= R["G5"]["L"]["line"]
        rr["G5"] = dict(v=dict(Q=hm, L=hm - R["G5"]["L"]["edge_dex"]), status=st(okQ or okL))
        for g, gn in (("G1", "G1 SPARC"), ("G2", "G2 X-COP"), ("G3", "G3 groups"), ("G8", "G8 Solar System")): rr[g] = dict(v=h[gn]["num"], status=h[gn]["status"])
        fails = [g for g in sorted(rr) if rr[g]["status"] != "PASS"]
        cond = [g for g in fails if g not in ("G5", "G6")]
        # QX12 iter_3 scan
        scan = Q12["scan"][f]; xp = [s for s in scan if s["X_pass"]]; both = [s for s in xp if s["G_strict"]["fst0"] >= 16 and s["G_strict"]["fst1"] >= 16]
        best = min(scan, key=lambda s: s["X_rms"])
        RED[f] = dict(HC1=dict(rows=rr, fails=fails, label=("PASSES THE REDUCED BATTERY" if not fails else f"FAILS ({', '.join(fails)})"),
                               conditional_noG5G6=("PASSES" if not cond else f"FAILS ({', '.join(cond)})")),
                      QX12=dict(c_min=Q12["foot"][f]["c_min"], n_scan=len(scan), n_X_pass=len(xp), n_X_and_groups=len(both),
                                best_X_rms=dict(c=best["c"], X_mean=best["X_mean"], X_rms=best["X_rms"]),
                                label="FAILS (G2, G3: no c_s0 on the scan passes X-COP)" if not xp else ("FAILS (G3)" if not both else "X-COP and groups pass somewhere: grade galaxy rows")))
        P(f"[{f}] HC1 fermion, reduced battery: " + "; ".join(f"{g} {rr[g]['status']}" for g in sorted(rr)) + f" -> {RED[f]['HC1']['label']}; conditional (G5, G6 dropped): {RED[f]['HC1']['conditional_noG5G6']}")
        P(f"      G4 {r4:+.3f}; G7 " + ", ".join(f"{k} {v:+.3f}" for k, v in r7.items()) + f"; G5 Q {hm:+.3f} L {hm - R['G5']['L']['edge_dex']:+.3f}"
          + (("; G6 " + "; ".join(f"{c} {v['med']:+.3f} [{v['ci'][0]:+.3f},{v['ci'][1]:+.3f}]" for c, v in rr["G6"]["v"].items())) if rr["G6"]["v"] else ""))
        P(f"[{f}] QX12 iter_3 sea: scan {len(scan)} c_s0 values, X-COP pass at {len(xp)}, X-COP + groups at {len(both)}; best X rms {best['X_rms']:.3f} at c {best['c']:.0f} (mean {best['X_mean']:+.3f}) -> {RED[f]['QX12']['label']}")
    RES["reduced_battery"] = RED

    # ------------------------------------------------------------------ labels
    lab = {}
    for g, nm in (("G4", "ellipticals"), ("G7", "KiDS split"), ("G6", "dSph satellites"), ("G5", "Coma UDGs")):
        cells = []
        for f in A0:
            R = RES["footings"][f]
            if g == "G6": s_ = R["G6"]["cut"]["status"]; rawv = max(R["G6"]["raw"][c]["median_minus_anchor"] for c in ("bright M31",)); corv = R["G6"]["cut"]["num"]["bright M31"]["median_minus_anchor"] if R["G6"]["cut"]["num"] else None
            elif g == "G5": s_ = R["G5"]["status"]; rawv = R["G5"]["raw"]; corv = R["G5"]["L"]["residual"]
            elif g == "G4": s_ = R["G4"]["status"]; rawv = R["G4"]["raw"]; corv = R["G4"]["corrected"]
            else: s_ = R["G7"]["status"]; rawv = R["G7"]["raw"]; corv = max(v["R"] for v in R["G7"]["bracket"].values())
            cells.append((s_, rawv, corv))
        if all(c[0] == "PASS" for c in cells): L = "EXPLAINED"
        elif any(c[0] == "NO VERDICT" for c in cells): L = "NO VERDICT"
        elif any(c[2] is not None and c[2] > c[1] * (2 / 3) for c in cells): L = "NOT EXPLAINED"
        else: L = "PARTLY"
        lab[nm] = dict(label=L, cells=cells)
        P(f"CLASS {nm:16s}: {L}  (" + "; ".join(f"{s_} raw {r:+.3f} -> {c:+.3f}" if c is not None else f"{s_}" for s_, r, c in cells) + ")")
    expl = [k for k, v in lab.items() if v["label"] == "EXPLAINED"]
    remaining_all = sorted({k for f in A0 for k in RES["footings"][f]["remaining"]})
    if set(remaining_all) <= {"X-COP", "groups"}: LL = "MULTI-CAUSE, CLUSTERS AND GROUPS ONLY"
    elif expl: LL = f"MULTI-CAUSE IN PART (remaining: {', '.join(remaining_all)})"
    else: LL = "ONE STEP STANDS"
    RES["class_labels"] = lab; RES["label"] = LL; RES["remaining_union"] = remaining_all
    P(f"\nLANE LABEL: {LL}")
    kaok_frozen = all(v["ok"] for v in RES["KA"].values()) and all(RES["footings"][f]["G6"]["M3_ok"] for f in A0)
    kaok = all(v["ok"] for k, v in RES["KA"].items() if not k.startswith("KA3_")) and all(RES["footings"][f]["G6"]["M3_ok"] for f in A0) \
        and all(RES["KA"][f"KA3_{f}"]["linear_replay_diff"] <= 1e-8 and RES["KA"][f"KA3_{f}"]["DX_diff"] <= 1e-9 for f in A0)
    RES["KA_all_as_frozen"] = bool(kaok_frozen); RES["KA_all"] = bool(kaok)
    P(f"KNOWN ANSWERS + M3: as frozen {'ALL PASS' if kaok_frozen else 'KA3 FAILS its 1e-4 line (linear vs exact convention)'}; with KA3' replay {'ALL PASS' if kaok else 'SOME FAIL'}")
else:
    m1 = all(RES["footings"][f]["G1"]["status"] == "FAIL" for f in A0); m2 = all(RES["footings"][f]["G4"]["status"] == "FAIL" for f in A0)
    m3 = all(RES["footings"][f]["G6"]["M3_ok"] for f in A0)
    RES["MUTATE"] = dict(M1_newton_fails_G1=m1, M2_inverted_IMF_fails_G4=m2, M3_cut_limits=m3, bites=bool(m1 and m2 and m3))
    P(f"\nMUTATE: M1 Newton fails G1 both footings {m1}; M2 inverted IMF fails G4 both footings {m2}; M3 cut limits {m3} -> {'BITES' if (m1 and m2 and m3) else 'NO POWER'}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (RES.get("KA_all", True) and RES.get("MUTATE", {}).get("bites", True)) else 1)
