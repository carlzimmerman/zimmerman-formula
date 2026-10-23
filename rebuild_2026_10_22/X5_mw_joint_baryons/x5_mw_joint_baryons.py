#!/usr/bin/env python3
"""X5_mw_joint_baryons: lane script (criteria FROZEN_CRITERIA.md, commit 8e5b65bca5; ledger ASSUMPTION_LEDGER.md).

Step 0  reproductions with the record's own code, read-only: P4's B1 (and the B3 identity) with P4's solver; S3 Part A's
        AQ_iso / AQ_gamma0 / AQ_gamma0_2x combined slope statistics with S3's code (census solved fresh in this lane's
        untracked _cache_s3/; off-census s-grid solves are byte copies of S3's cache).
(i)     reads x5_grid_<foot>.json (x5_grid.py), applies the frozen pass line, FEASIBLE / AQUAL-STRUCTURAL per footing, the
        best cell and its robustness re-solves (L* 90 pc; g_e 0.03 a0 along the axis).
(ii)    S3 Part A under CFG532's S2 error budget: SHAPE EXCLUDED ROBUST / ERROR-MODEL-DEPENDENT per footing.
Run:  OMP_NUM_THREADS=1 nice -n 15 python3 x5_mw_joint_baryons.py            (after x5_grid.py for both footings)
      OMP_NUM_THREADS=1 nice -n 15 python3 x5_mw_joint_baryons.py --mutate   (P4 mu -> x/sqrt(1+x^2), S3 mu == 1; exit 1)
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys
import json
import math
import time
import shutil
import hashlib
import itertools
import numpy as np
from scipy.stats import chi2 as chi2dist
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x5_lib as L  # noqa: E402  (sets PYTHONDONTWRITEBYTECODE)

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
CACHE_S3 = os.path.join(L.HERE, "_cache_s3")                      # untracked; never committed
os.makedirs(CACHE_S3, exist_ok=True)
os.environ["S3_CACHE_DIR"] = CACHE_S3
T0 = time.time()
OUT, CHECKS = [], []
RES = dict(lane="X5_mw_joint_baryons", criteria=L.CRITERIA, mutate=MUT, checks={})


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(cid, ok, value, thr, detail=""):
    ok = bool(ok)
    CHECKS.append((cid, ok))
    RES["checks"][cid] = dict(ok=ok, value=value, threshold=thr, detail=detail)
    P(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr}" + (f"   [{detail}]" if detail else ""))
    return ok


def jdefault(o):
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


P("=" * 118)
P(f"X5_mw_joint_baryons {'*** MUTATE: P4 mu -> x/sqrt(1+x^2) (L* 0), S3 mu == 1 ***' if MUT else ''}")
P("kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; no dark-matter particle; not theory closed")
P("=" * 118)

# =================================================================================================== Step 0: P4
P("\n--- Step 0a: P4's B1 (McMillan17) F0 L* 24 pc with P4's solver (read-only)")
ns = L.load_p4()
F = L.Family(ns)
P4J = json.load(open(os.path.join(L.P4DIR, "p4_v3_galaxy_tiles_results.json")))["tiles"]["T4"]["models"]
RES["step0_P4"] = {}
dmax = [0.0, 0.0, 0.0]
for foot in L.FOOTS:
    o0, oL, info = L.solve_cell(ns, ns["rho_mcm"], foot, mutate=MUT)
    ref = P4J["B1_McMillan17"][foot]["F0|L24"]
    d = [abs(oL["K_R0"] - ref["K_R0"]), abs(oL["chi2_kz"] - ref["chi2_kz"]), abs(oL["vc_R0"] - ref["vc_R0"])]
    dmax = [max(a, b) for a, b in zip(dmax, d)]
    RES["step0_P4"][foot] = dict(mine=L.slim(oL), record=dict(K_R0=ref["K_R0"], chi2_kz=ref["chi2_kz"], vc_R0=ref["vc_R0"]), info=info)
    P(f"  {foot:<9} K_z(R0) {oL['K_R0']:.3f} (P4 {ref['K_R0']:.3f}); chi2_Kz {oL['chi2_kz']:.3f} (P4 {ref['chi2_kz']:.3f}); "
      f"v_c(R0) {oL['vc_R0']:.3f} (P4 {ref['vc_R0']:.3f}); h {oL['h']:.3f}")
check("C0a", dmax[0] <= 0.05 and dmax[1] <= 0.1 and dmax[2] <= 0.05, f"dK={dmax[0]:.2e};dchi2={dmax[1]:.2e};dvc={dmax[2]:.2e}",
      "<=0.05;<=0.1;<=0.05", "P4 B1 F0 L*24 pc reproduced on both footings")

P("\n--- Step 0b: the family at McMillan17's column and bulge with R_d = 2.15 is P4's B3")
rhoB3, pB3 = F.rho(F.sig_b_mcm, F.M_bulge_mcm, 2.15)
rng = np.random.default_rng(5)
Rq, zq = rng.uniform(0.0, 40.0, 2000), rng.uniform(-5.0, 5.0, 2000)
a, b = rhoB3(Rq, zq), ns["rho_b3"](Rq, zq)
eid = float(np.max(np.abs(a - b) / np.maximum(np.abs(b), 1e-300)))
db3 = [0.0, 0.0, 0.0]
RES["step0_B3"] = dict(identity_max_rel=eid)
for foot in L.FOOTS:
    o0, oL, info = L.solve_cell(ns, rhoB3, foot, mutate=MUT)
    ref = P4J["B3_short_disc_2.15"][foot]["F0|L24"]
    d = [abs(oL["K_R0"] - ref["K_R0"]), abs(oL["chi2_kz"] - ref["chi2_kz"]), abs(oL["vc_R0"] - ref["vc_R0"])]
    db3 = [max(x, y) for x, y in zip(db3, d)]
    RES["step0_B3"][foot] = dict(mine=L.slim(oL), record=dict(K_R0=ref["K_R0"], chi2_kz=ref["chi2_kz"], vc_R0=ref["vc_R0"]))
    P(f"  {foot:<9} K_z(R0) {oL['K_R0']:.3f} (P4 B3 {ref['K_R0']:.3f}); chi2_Kz {oL['chi2_kz']:.3f} ({ref['chi2_kz']:.3f}); v_c {oL['vc_R0']:.3f} ({ref['vc_R0']:.3f})")
check("C0b", eid <= 1e-12 and db3[0] <= 0.05 and db3[1] <= 0.1 and db3[2] <= 0.05,
      f"identity={eid:.1e};dK={db3[0]:.2e};dchi2={db3[1]:.2e};dvc={db3[2]:.2e}", "<=1e-12;<=0.05;<=0.1;<=0.05",
      "family(Sigma_McM, M_bulge_McM, 2.15) == P4 rho_b3 at 2000 points, and its solve == P4's B3 cell")

vE, eE = L.eilers_target(ns)
U1J = json.load(open(os.path.join(L.U1DIR, "u1_v3_dust_content_results.json")))["numbers"]["N6"]["canonical"]
dE = max(abs(vE - U1J["vc_Eilers_R0"]), abs(eE - U1J["e_vc_Eilers"]))
check("C2", dE <= 1e-6, f"{vE:.4f}+-{eE:.4f} (U1 {U1J['vc_Eilers_R0']:.4f}+-{U1J['e_vc_Eilers']:.4f})", "<=1e-6", "Eilers v_c(R0) target")
RES["vc_target"] = dict(v=vE, e=eE, line_unrounded=2 * eE, brief=[L.VC_BRIEF, L.VC_BRIEF_LINE])

# =================================================================================================== Step 0: S3 machinery
P("\n--- Step 0c: S3 Part A with S3's code (read-only; census solved fresh in this lane's cache)")
sys.path.insert(0, L.S3DIR)
import s3_aqual as S3S  # noqa: E402
import s3_mw as MWm  # noqa: E402
assert os.path.abspath(S3S.CACHE) == os.path.abspath(CACHE_S3)
assert S3S.MUTATE == MUT
S3CACHE = os.path.join(L.S3DIR, "_cache_final")
TAG_MW = "main" + S3S.TAG


def cache_name(foot, s, eN):
    key = f"{TAG_MW}|{foot}|s{s:.6f}|eN{eN:.6f}|"
    return "mw_" + hashlib.sha1(key.encode()).hexdigest()[:16] + ".npz"


ncopy, nmiss = 0, 0
for foot in L.FOOTS:
    for s in MWm.S_GRID:
        if abs(s - 1.0) < 1e-12:
            continue
        for eN in (0.0, MWm.EN_H81[foot]):
            fn = cache_name(foot, s, eN)
            src, dst = os.path.join(S3CACHE, fn), os.path.join(CACHE_S3, fn)
            if os.path.exists(dst):
                continue
            if os.path.exists(src):
                shutil.copyfile(src, dst); ncopy += 1
            else:
                nmiss += 1
census = [(f, 1.0, e) for f in L.FOOTS for e in (0.0, MWm.EN_H81[f], 2 * MWm.EN_H81[f])]
fresh_before = [os.path.exists(os.path.join(CACHE_S3, cache_name(*c))) for c in census]
mw = MWm.MW()
g = mw.g
nrun, cpeak = MWm.presolve(mw, MWm.GRID_MAIN, "main", census, batch=3)
P(f"  off-census S3 cache files copied {ncopy} (missing in S3's cache, solved here: {nmiss}); census cells solved now {nrun} "
  f"(already solved by this lane earlier: {sum(fresh_before)}); child peak RSS {cpeak:.0f} MB")
nrun2, cpeak2 = MWm.presolve(mw, MWm.GRID_MAIN, "main", [(f, s, e) for f in L.FOOTS for s in MWm.S_GRID for e in (0.0, MWm.EN_H81[f])], batch=4)
RES["s3_cache"] = dict(copied=ncopy, missing_in_S3=nmiss, census_solved_now=nrun, census_preexisting_in_lane=sum(fresh_before),
                       offcensus_solved_now=nrun2, child_peak_MB=max(cpeak, cpeak2))

# C0d: fresh census solves vs S3's cached census solves
Rcmp = np.linspace(5.0, 27.5, 46)
d0d, nref = 0.0, 0
for c in census:
    fn = cache_name(*c)
    mine = np.load(os.path.join(CACHE_S3, fn))["Phi"]
    srcf = os.path.join(S3CACHE, fn)
    if not os.path.exists(srcf):
        d0d = float("inf"); continue
    theirs = np.load(srcf)["Phi"]; nref += 1
    gm, gt = g.gR_plane(mine, Rcmp), g.gR_plane(theirs, Rcmp)
    d0d = max(d0d, float(np.max(np.abs(gm / gt - 1))))
check("C0d", d0d <= 1e-6, f"{d0d:.1e} ({nref}/6 S3 census files)", "<=1e-6", "this lane's census AQUAL solves vs S3's cached ones, g_R 5-27.5 kpc")

# exec S3 Part A's data / C-table / scoring segments (read-only)
S3CHK = []
srcA = open(os.path.join(L.S3DIR, "s3_partA_mw.py")).read()
MK = "# ------------------------------------------------------------------ "
segA = MK + "data (my loader" + srcA.split(MK + "data (my loader", 1)[1].split(MK + "MW model and solves", 1)[0]
segB = "def gAQ(foot, s, eN, R):" + srcA.split("\ndef gAQ(foot, s, eN, R):", 1)[1].split(MK + "3-D EFE ratios", 1)[0]
segC = MK + "models along the path" + srcA.split(MK + "models along the path", 1)[1].split("\nRES = dict(lane=", 1)[0]
nsS = dict(os=os, np=np, math=math, json=json, itertools=itertools, chi2dist=chi2dist, minimize_scalar=minimize_scalar,
           S=S3S, MWm=MWm, mw=mw, g=g, DATA=L.DATA, CFGD=L.CFGD, SRCDIR=os.path.join(os.path.abspath(os.path.join(L.REPO, "..", "_external_data")), "cfg532_work", "src"),
           P=lambda *a: None, check=lambda name, ok, detail="": S3CHK.append((name, bool(ok), detail)), FOOTS=L.FOOTS)
for nm, seg in (("s3_partA_data", segA), ("s3_partA_ctable", segB), ("s3_partA_scoring", segC)):
    exec(compile(seg, nm, "exec"), nsS)
P("  S3's own data controls inside the executed segment: " + ", ".join(n + (" PASS" if o else " FAIL") for n, o, _ in S3CHK))
CUR, run_combined, delta, score, slope, window, class_verdict = (nsS[k] for k in ("CUR", "run_combined", "delta", "score", "slope", "window", "class_verdict"))
S3J = json.load(open(os.path.join(L.S3DIR, "s3_partA_mw_results.json")))["steps"]
STEPS3 = ("AQ_iso", "AQ_gamma0", "AQ_gamma0_2x")
RES["step0_S3"] = {}
dz, dbl = 0.0, 0.0
for step in STEPS3:
    for foot in L.FOOTS:
        cm = run_combined(step, foot)
        rf = S3J[step][foot]["combined"]
        dz = max(dz, abs(cm["primary"]["Z"] - rf["primary"]["Z"]), abs(cm["primary_rho05"]["Z"] - rf["primary_rho05"]["Z"]))
        if step == "AQ_gamma0":
            for k in ("Ou24", "Jiao23"):
                dbl = max(dbl, abs(cm["per_curve"][k]["b_law"] - rf["per_curve"][k]["b_law"]))
        RES["step0_S3"][f"{step}|{foot}"] = dict(Z=cm["primary"]["Z"], Z_rho05=cm["primary_rho05"]["Z"], label=cm["primary"]["verdict"],
                                                 Z_record=rf["primary"]["Z"], Z_range=cm["Z_range"],
                                                 b_law_Ou=cm["per_curve"]["Ou24"]["b_law"], b_law_Jiao=cm["per_curve"]["Jiao23"]["b_law"])
        P(f"  {step:<13} {foot:<9} primary Z {cm['primary']['Z']:+.4f} (S3 {rf['primary']['Z']:+.4f}) {cm['primary']['verdict']}; "
          f"rho0.5 {cm['primary_rho05']['Z']:+.4f} (S3 {rf['primary_rho05']['Z']:+.4f}); law slope Ou {cm['per_curve']['Ou24']['b_law']:+.5f}")
check("C0c", dz <= 0.01 and dbl <= 1e-4, f"dZ={dz:.1e};db_law={dbl:.1e}", "<=0.01;<=1e-4",
      "S3 Part A AQ_iso / AQ_gamma0 / AQ_gamma0_2x primary and rho 0.5 Z, and Ou / Jiao law slopes, both footings")

# =================================================================================================== (ii) S2 error budget
P("\n=== (ii) S3 Part A under CFG532's S2 error budget (Ou 5 % inner / 15 % beyond; Eilers 5 %; Wang, Zhou, Feng stat + 5 %; Jiao, SL23 as published)")
ou, el, TEX, parse_tex = nsS["ou"], nsS["el"], nsS["TEX"], nsS["parse_tex"]
CUR2 = {}
for k, c in CUR.items():
    c2 = dict(c)
    if k == "Ou24":
        s_ = 0.5 * (ou["sig_plus"] + ou["sig_minus"]); E = np.hypot(s_, np.where(c["R"] <= 22.0, 0.05, 0.15) * c["V"]); rule = "stat + 5% (R<=22) / 15%"
    elif k == "Eilers19":
        s_ = 0.5 * (el["sig_plus"] + el["sig_minus"]); E = np.hypot(s_, 0.05 * c["V"]); rule = "stat + 5%"
    else:
        f_, l0, l1, et, grp, nexp = TEX[k]
        R_, V_, Sg = parse_tex(f_, l0, l1)
        assert np.array_equal(R_, c["R"]) and np.array_equal(V_, c["V"])
        E = np.hypot(Sg, 0.05 * V_) if et == "stat" else Sg.copy(); rule = "table + 5%" if et == "stat" else "as published"
    c2["E"] = E
    lo, hi = window(c2)
    c2["b_data"], c2["b_err"], c2["n_win"] = slope(c2["R"], c2["V"], c2["E"], lo, hi)
    c2["S2_rule"] = rule
    CUR2[k] = c2
    P(f"  {k:<16} {rule:<26} data slope {c2['b_data']:+.4f} +- {c2['b_err']:.4f} (primary {c['b_data']:+.4f} +- {c['b_err']:.4f}; n {c2['n_win']})")
J532 = json.load(open(os.path.join(L.CFGD, "CFG532_mw_gaia_rotation_curves", "cfg532_results.json")))["systematics"]
J532b = json.load(open(os.path.join(L.CFGD, "CFG532_mw_gaia_rotation_curves", "cfg532b_results.json")))["systematics"]
refs = {"Ou24": J532["C1_Ou24|canonical|RMv"]["S2_5pct_inner"], "Eilers19": J532["C2_Eilers19|canonical|RMv"]["S2_5pct"],
        "Wang23": J532b["Wang23|canonical|RMv"]["S2_5pct"], "Zhou23": J532b["Zhou23|canonical|RMv"]["S2_5pct"],
        "Feng26_Cepheids": J532b["Feng26_Cepheids|canonical|RMv"]["S2_5pct"]}
d1 = max(max(abs(CUR2[k]["b_data"] - r["slope_data"]), abs(CUR2[k]["b_err"] - r["slope_err"])) for k, r in refs.items())
d1j = max(abs(CUR2[k]["b_err"] - CUR[k]["b_err"]) for k in ("Jiao23", "SL23_DR3plus"))
check("C1", d1 <= 1e-9 and d1j == 0.0, f"{d1:.1e};Jiao/SL23 unchanged {d1j:.1e}", "<=1e-9;0",
      "S2 data slopes and errors vs CFG532 (Ou S2_5pct_inner, Eilers S2_5pct) and CFG532b (Wang, Zhou, Feng S2_5pct)")
RES["S2_data"] = {k: dict(rule=c["S2_rule"], b_data=c["b_data"], b_err=c["b_err"], n=c["n_win"], b_data_primary=CUR[k]["b_data"],
                          b_err_primary=CUR[k]["b_err"]) for k, c in CUR2.items()}

RES["ii"] = {}
for foot in L.FOOTS:
    cm = run_combined("AQ_gamma0", foot, CUR2)
    ci = run_combined("AQ_iso", foot, CUR2)
    cx = run_combined("AQ_gamma0_2x", foot, CUR2)
    prim = cm["primary"]
    mem = {"rho0.5": cm["primary_rho05"]["verdict"], "e_N 0 (AQ_iso)": ci["primary"]["verdict"], "e_N 2 x h81 (AQ_gamma0_2x)": cx["primary"]["verdict"]}
    memZ = {"rho0.5": cm["primary_rho05"]["Z"], "e_N 0 (AQ_iso)": ci["primary"]["Z"], "e_N 2 x h81 (AQ_gamma0_2x)": cx["primary"]["Z"]}
    robust = prim["verdict"] == "SHAPE EXCLUDED" and all(v == "SHAPE EXCLUDED" for v in mem.values())
    verdict = "SHAPE EXCLUDED ROBUST" if robust else "ERROR-MODEL-DEPENDENT"
    cep = delta("AQ_gamma0", foot, CUR2["Feng26_Cepheids"])
    Zc = cep[0] / cep[1]
    per = {k: score("AQ_gamma0", foot, c) for k, c in CUR2.items()}
    RES["ii"][foot] = dict(verdict=verdict, primary=prim, members=mem, members_Z=memZ, pairs=cm["pairs"], Z_range=cm["Z_range"],
                           per_curve_delta=cm["per_curve"], cepheid=dict(delta=cep[0], sig=cep[1], b_law=cep[2], Z=Zc,
                           label=class_verdict(Zc, cep[1], cep[2])), per_curve_labels={k: v["verdict"] for k, v in per.items()},
                           per_curve=per, Z_primary_errors=S3J["AQ_gamma0"][foot]["combined"]["primary"]["Z"])
    P(f"\n  {foot}: v3 cell AQ_gamma0, Ou+Jiao rho 0 under S2: Delta {prim['mean']:+.4f} +- {prim['sig']:.4f}, Z {prim['Z']:+.3f} -> {prim['verdict']}"
      f"   (primary errors: Z {S3J['AQ_gamma0'][foot]['combined']['primary']['Z']:+.3f})")
    P(f"    robustness set: " + "; ".join(f"{k} Z {memZ[k]:+.3f} {mem[k]}" for k in mem))
    P(f"    all one-per-group pairs: Z {cm['Z_range'][0]:+.3f} .. {cm['Z_range'][1]:+.3f}; " +
      ", ".join(f"{k} {v['Z']:+.2f}" for k, v in cm["pairs"].items() if k.endswith("rho0.0")))
    P(f"    Cepheids (Feng): Z {Zc:+.3f} {class_verdict(Zc, cep[1], cep[2])}")
    P("    per-curve CFG532 s4 labels at the v3 cell under S2: " + "; ".join(
        f"{k} {v['verdict']} (chi2 {v['chi2_census']:.1f}/{v['N']}, slope {v['dslope_census_sig']:+.2f} sig)" for k, v in per.items()))
    P(f"    -> (ii) {foot}: {verdict}")

# =================================================================================================== (i) the prior box
RES["i"] = {}
if not MUT:
    P("\n=== (i) the prior box (x5_grid.py outputs): pass = chi2_Kz <= %.3f AND |v_c - 229.1| <= 9.2 AND |v_c - %.3f| <= %.3f" % (L.LINE_CHI2, vE, 2 * eE))
    GR = {f: json.load(open(os.path.join(L.HERE, f"x5_grid_{f}.json"))) for f in L.FOOTS}
    ncell = {f: GR[f]["n_cells"] for f in L.FOOTS}
    resmax = max(max(c["info"]["res_L0"], c["info"]["res_L"]) for f in L.FOOTS for c in GR[f]["cells"])
    check("C3", all(n == 175 for n in ncell.values()) and resmax <= 1e-8, f"cells={ncell};res_max={resmax:.1e}", "175 each;<=1e-8",
          "grid complete; P4 scaled Newton residuals")
    mrel = max(abs(c["mass_rel_err"]) for f in L.FOOTS for c in GR[f]["cells"])
    check("C4", mrel <= 0.01, f"{mrel:.2e}", "<=0.01", "grid mass vs analytic (discs 2 pi Sigma0 Rd^2 + M_bb + gas quadrature)")
    for foot in L.FOOTS:
        cells = GR[foot]["cells"]
        # recompute the pass from the stored observables with the frozen lines (guards against any drift)
        for c in cells:
            c["passes"], c["D"] = L.cell_pass(c["L24"]["chi2_kz"], c["L24"]["vc_R0"], vE, eE)
        passing = [c for c in cells if c["passes"]]
        best = min(cells, key=lambda c: c["D"])
        invc = [c for c in cells if abs(c["L24"]["vc_R0"] - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(c["L24"]["vc_R0"] - vE) <= 2 * eE]
        inkz = [c for c in cells if c["L24"]["chi2_kz"] <= L.LINE_CHI2]
        mn_kz = min(invc, key=lambda c: c["L24"]["chi2_kz"]) if invc else None
        mx_vc = max(inkz, key=lambda c: c["L24"]["vc_R0"]) if inkz else None
        # robustness re-solves for the best cell and every passing cell
        rob = {}
        for c in ([best] + [c for c in passing if c is not best]):
            rhof, p = F.rho(c["sig_b"], c["M_bb"], c["R_d"])
            _, o90, _ = L.solve_cell(ns, rhof, foot, Lam_kpc=0.090, keep_L0=False)
            oge, _, _ = L.solve_cell(ns, rhof, foot, Lam_kpc=0.0, full=True, ge=0.03)
            p90 = L.cell_pass(o90["chi2_kz"], o90["vc_R0"], vE, eE)
            pge = L.cell_pass(oge["chi2_kz"], oge["vc_R0"], vE, eE)
            key = f"{c['sig_b']}|{c['M_bb']:.3g}|{c['R_d']:.4f}"
            rob[key] = dict(L90=dict(chi2_kz=o90["chi2_kz"], vc_R0=o90["vc_R0"], K_R0=o90["K_R0"], passes=p90[0], D=p90[1]),
                            ge003=dict(chi2_kz=oge["chi2_kz"], vc_R0=oge["vc_R0"], K_R0=oge["K_R0"], passes=pge[0], D=pge[1]),
                            fragile=bool(c["passes"] and not (p90[0] and pge[0])))
        if passing:
            tight = [c for c in passing if c["tag_Mstar_IN"] and c["tag_Rd_IN"]]
            verdict = "FEASIBLE (tight priors)" if tight else "FEASIBLE (wide priors only)"
        else:
            verdict = "AQUAL-STRUCTURAL"

        def cd(c):
            if c is None:
                return None
            return dict(sig_b=c["sig_b"], M_bb=c["M_bb"], R_d=c["R_d"], Mstar=c["params"]["Mstar"], Sigma_11=c["Sigma_11_R0_quad"],
                        chi2_kz=c["L24"]["chi2_kz"], vc_R0=c["L24"]["vc_R0"], K_R0=c["L24"]["K_R0"], h=c["L24"]["h"], chi2_rc=c["L24"]["chi2_rc"],
                        D=c["D"], tag_Mstar_IN=c["tag_Mstar_IN"], tag_Rd_IN=c["tag_Rd_IN"], chi2_kz_L0=c["L0"]["chi2_kz"], vc_L0=c["L0"]["vc_R0"])
        allc = [cd(c) for c in cells]
        RES["i"][foot] = dict(verdict=verdict, n_pass=len(passing), passing=[cd(c) for c in passing], best=cd(best),
                              min_chi2_with_vc_in_line=cd(mn_kz), max_vc_with_chi2_in_line=cd(mx_vc), n_vc_in_line=len(invc),
                              n_chi2_in_line=len(inkz), robustness=rob, cells=allc,
                              chi2_range=[min(c["chi2_kz"] for c in allc), max(c["chi2_kz"] for c in allc)],
                              vc_range=[min(c["vc_R0"] for c in allc), max(c["vc_R0"] for c in allc)],
                              grid_runtime_s=GR[foot]["runtime_s"], grid_peak_rss_MB=GR[foot]["peak_rss_MB"])
        b = RES["i"][foot]["best"]
        P(f"\n  {foot}: {len(passing)} of {len(cells)} cells pass -> (i) {verdict}")
        P(f"    best cell: Sigma_b {b['sig_b']}, M_bb {b['M_bb'] / 1e10:.2f}e10, R_d {b['R_d']:.3f} | M* {b['Mstar'] / 1e10:.2f}e10 "
          f"(M*-IN {b['tag_Mstar_IN']}, R_d-IN {b['tag_Rd_IN']}) | chi2_Kz {b['chi2_kz']:.2f}, v_c(R0) {b['vc_R0']:.2f}, K_z(R0) {b['K_R0']:.2f}, "
          f"h {b['h']:.2f}, D {b['D']:.3f}")
        rb = rob[f"{best['sig_b']}|{best['M_bb']:.3g}|{best['R_d']:.4f}"]
        P(f"    best cell at L* 90 pc: chi2_Kz {rb['L90']['chi2_kz']:.2f}, v_c {rb['L90']['vc_R0']:.2f}; with g_e 0.03 a0: chi2_Kz {rb['ge003']['chi2_kz']:.2f}, v_c {rb['ge003']['vc_R0']:.2f}")
        P(f"    cells with v_c inside the line: {len(invc)}; lowest chi2_Kz among them: " +
          (f"{mn_kz['L24']['chi2_kz']:.2f} (Sigma_b {mn_kz['sig_b']}, M_bb {mn_kz['M_bb'] / 1e10:.2f}, R_d {mn_kz['R_d']:.3f}, v_c {mn_kz['L24']['vc_R0']:.2f})" if mn_kz else "none"))
        P(f"    cells with chi2_Kz inside the line: {len(inkz)}; highest v_c among them: " +
          (f"{mx_vc['L24']['vc_R0']:.2f} (Sigma_b {mx_vc['sig_b']}, M_bb {mx_vc['M_bb'] / 1e10:.2f}, R_d {mx_vc['R_d']:.3f}, chi2 {mx_vc['L24']['chi2_kz']:.2f})" if mx_vc else "none"))
        P(f"    ranges over the box: chi2_Kz {RES['i'][foot]['chi2_range'][0]:.1f} .. {RES['i'][foot]['chi2_range'][1]:.1f}; "
          f"v_c(R0) {RES['i'][foot]['vc_range'][0]:.1f} .. {RES['i'][foot]['vc_range'][1]:.1f} km/s")
        for c in passing:
            k = f"{c['sig_b']}|{c['M_bb']:.3g}|{c['R_d']:.4f}"
            P(f"    PASS cell {k}: chi2 {c['L24']['chi2_kz']:.2f}, v_c {c['L24']['vc_R0']:.2f}, M* {c['params']['Mstar'] / 1e10:.2f}e10, "
              f"tags M*-IN {c['tag_Mstar_IN']} R_d-IN {c['tag_Rd_IN']}, {'FRAGILE' if rob[k]['fragile'] else 'robust to L* 90 and g_e 0.03'}")
    rss_runs = [GR[f]["peak_rss_MB"] for f in L.FOOTS]
    rt_runs = [GR[f]["runtime_s"] for f in L.FOOTS]
else:
    P("\n=== (i) MUTATE: the grid is not run; the central cell once with P4's mutate mu (reported)")
    rhof, p = F.rho(47.1, 1.88e10, 2.6)
    for foot in L.FOOTS:
        o0, oL, info = L.solve_cell(ns, rhof, foot, mutate=True)
        RES["i"][foot] = dict(central_cell_mutate=L.slim(oL))
        P(f"  {foot}: central cell (47.1, 1.88e10, 2.6) mutate: chi2_Kz {oL['chi2_kz']:.2f}, v_c {oL['vc_R0']:.2f}")
    rss_runs, rt_runs = [], []
    for cid in ("C3", "C4"):
        RES["checks"][cid] = dict(ok=None, value="not evaluated (mutate)")
        P(f"{cid} not evaluated (mutate)")

RES["runtime_s"] = round(time.time() - T0, 1)
RES["peak_rss_MB"] = round(L.rss_mb(), 1)
allrss = rss_runs + [RES["peak_rss_MB"], RES["s3_cache"]["child_peak_MB"]]
allrt = rt_runs + [RES["runtime_s"]]
if not MUT:
    check("C5", max(allrss) < 1000.0 and max(allrt) <= 1800.0, f"rss_max={max(allrss):.0f}MB;runtime_max={max(allrt):.0f}s", "<1000;<=1800",
          "grid runs, this run and S3 child processes")
else:
    RES["checks"]["C5"] = dict(ok=None, value=f"not evaluated (mutate); rss {max(allrss):.0f} MB")
    P("C5 not evaluated (mutate)")

npass = sum(ok for _, ok in CHECKS)
RES["n_checks"], RES["n_pass"] = len(CHECKS), npass
P("\n--- verdicts (per footing, never pooled)")
for foot in L.FOOTS:
    P(f"  {foot:<9} (i) {RES['i'][foot].get('verdict', 'n/a (mutate)')}; (ii) {RES['ii'][foot]['verdict']}")
json.dump(RES, open(os.path.join(L.HERE, f"x5_mw_joint_baryons_results{TAG}.json"), "w"), indent=1, default=jdefault)
P(f"\nX5_MW_JOINT_BARYONS COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {RES['runtime_s']} s, peak RSS {RES['peak_rss_MB']} MB")
open(os.path.join(L.HERE, f"x5_mw_joint_baryons{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
