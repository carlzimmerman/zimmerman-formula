#!/usr/bin/env python3
"""HO2_sluggs_milkyway_heldout: the frozen CL2 picture (switch T 12.3 or satellite; S9 / L 4 eta-floor Burkert cores;
law on baryons below) graded on GR1's four SLUGGS centrals and on GD1/GD2's Milky Way lines. Neither entered the
calibrating lanes. Frozen criteria: FROZEN_CRITERIA.md (8dc1536cfd, committed alone).

Machinery executed read-only as text copies (outputs suppressed): EM1 (backgrounds) + X43's EPS block (Sigma_coll),
GR1's head (SC1/X38/EM1/X30, P4 group estimator, CFG528b Jeans solver), GD2 (X5 box on P4's Newtonian path), GD1.
Each runs in its own forked process (RSS < 1 GB each, one thread).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ho2_heldout.py        (HO2_MUTATE=1 twin)
"""
import os, sys, io, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in ("X30_MUTATE", "X53_MUTATE", "CFG528_MUTATE", "CFG528_POSTFREEZE", "CFG528B_MUTATE", "CFG331_MUTATE"): os.environ.pop(_v, None)
import numpy as np

T0 = time.time(); MUTATE = os.environ.get("HO2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUTATE else ""
HERE='/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/CSM1_consistent_core_switch/heldout'; REB='/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22'; REPO='/Users/carlzimmerman/new_physics/zimmerman-formula'
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
FEET = ("canonical", "alt"); A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
TSW = 12.3
P(f"HO2_sluggs_milkyway_heldout  {'MUTATE (switch flag inverted; S0-CL2 targets x1.01)' if MUTATE else 'normal run'}   criteria 8dc1536cfd")
P("kappa = 1/2 FITTED; footings never pooled; CL2 picture: route E iff satellite or M200 > 10^12.3, else the law on baryons; not theory closed")

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def take_route_e(flag):
    return (not flag) if MUTATE else bool(flag)
SWITCH = {"n": 0, "viol": 0}
def branch(flag):
    t = take_route_e(flag); SWITCH["n"] += 1; SWITCH["viol"] += int(t != bool(flag)); return t

def run_copy(src_path, edits, fake_file, argv=None, cut=None, extra=None):
    src = open(src_path).read()
    if cut: src = src[:src.index(cut)]
    for old, new in edits:
        assert src.count(old) == 1, (src_path, old[:70]); src = src.replace(old, new)
    ns = {"__file__": fake_file, "__name__": os.path.basename(fake_file)[:-3]}
    if extra: ns.update(extra)
    argv0 = sys.argv; sys.argv = [fake_file] + list(argv or [])
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try: exec(compile(src, fake_file, "exec"), ns)
            except SystemExit: pass
    finally:
        sys.argv = argv0
    return ns

# ------------------------------------------------------------------ the CL2 core: c_f(M), eta(M), Sigma = max(Sigma_a0, eta Sigma_coll)
X48A2 = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48_A2.json")))
S9 = [X48A2["cf_by_mass"][k] for k in ("1e+12", "1e+13", "1e+14")]
CF_TAB = [4.0 * c / S9[2] for c in S9]                                  # CL2 cf_table("S9", 4.0)
B1 = 3 * math.log(2) - math.pi / 2
def eta(M_sun): return 4.0 / (3.0 * B1) * float(np.interp(math.log10(M_sun), [12.0, 13.0, 14.0], CF_TAB)) ** 1.25
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3J = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGR = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3J[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
TAB = {}                                                                 # filled from child 0
def sig_coll_pc(tag, M_sun): return 10 ** float(np.interp(math.log10(M_sun), TAB["lg"], TAB["lsc"][tag]))
def sigma_cl2_pc(foot, tag, M_sun, sig_a0_pc):
    return max(sig_a0_pc[foot], eta(M_sun) * sig_coll_pc(tag, M_sun))

# ================================================================== child 0: Sigma_coll table (EM1 CLASS backgrounds + X43 EPS)
def child_sigma():
    EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py")
    NE = run_copy(EM1SRC, [], EM1SRC, cut="# ---------------- halo profiles")
    X43SRC = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py"); TX = open(X43SRC).read()
    blk = TX[TX.index("# ------------------------------------------------------------------ EPS formation"):TX.index("k2 = all(abs(EPS[t][\"s8\"]")]
    NX = {"np": np, "math": math, "MUTATE": False, "BGSE": NE["BGS"]}
    exec(compile(blk, "x43_eps_block", "exec"), NX)
    lg = np.round(np.arange(9.0, 16.0 + 1e-9, 0.0005), 6)
    lsc = {t: np.array([math.log10(NX["sigma_coll"](t, 10.0 ** l)[0]) for l in lg]) for t in BGR}
    test = {}
    for l in (11.37, 12.0, 12.31, 12.777, 13.5):
        d = NX["sigma_coll"]("A_c2b_refit", 10.0 ** l)[0]; i = 10 ** float(np.interp(l, lg, lsc["A_c2b_refit"]))
        test[f"{l}"] = (d, i)
    return dict(lg=lg.tolist(), lsc={t: v.tolist() for t, v in lsc.items()}, s12=NX["sigma_coll"]("A_c2b_refit", 1e12)[0], test=test,
                A0={f: float(NE["A0"][f]) for f in FEET}, eta_x43=float(NX["ETA"]), rss=rss())

# ================================================================== child 1: SLUGGS (GR1 head) + S0-GR1 + S0-CL2 (groups)
GR1DIR = os.path.join(REB, "GR1_core_law_groups_ellipticals")
def child_sluggs():
    STAT = {}
    NS = run_copy(os.path.join(GR1DIR, "gr1_groups_ellipticals.py"),
                  [('f"gr1_x30_machinery{TAG}.log"', repr(f"ho2_x30_machinery_gr1copy{TAG}.log"))],
                  os.path.join(HERE, "ho2_gr1copy.py"), cut="# ------------------------------------------------------------------ graded runs")
    GR1J = json.load(open(os.path.join(GR1DIR, "gr1_groups_ellipticals_results.json")))
    sluggs, grade_groups, QF, CEN, BIN = NS["sluggs"], NS["grade_groups"], NS["QF"], NS["CEN"], NS["BIN"]
    SIGkg = NS["SIG"]; GE, MSUNE, MPCE = NS["GE"], NS["MSUNE"], NS["MPCE"]; PC2 = (3.0857e16) ** 2
    SIGPC = {f: SIGkg[f] * PC2 / MSUNE for f in FEET}
    out = dict(sig_a0_pc=SIGPC, K0c=bool(dict(NS["checks"]).get("K0c", False)))
    # ---- S0-GR1
    s0gr, dev = {}, 0.0
    for f in FEET:
        s0 = sluggs(f, 0.0); sq = sluggs(f, QF[f]); g0 = grade_groups(f, 0.0); R = GR1J["footings"][f]
        for st, ref in ((s0, R["sluggs"]["q0"]), (sq, R["sluggs"]["st"])):
            for k in ref["per"]: dev = max(dev, abs(st["per"][k] - ref["per"][k]))
            dev = max(dev, abs(st["mean"] - ref["mean"]))
        okg = abs(g0["mean"] - R["groups"]["q0"]["mean"]) < 1e-6 and abs(g0["Z"] - R["groups"]["q0"]["Z"]) < 1e-4
        s0gr[f] = dict(q0=dict(per=s0["per"], mean=s0["mean"], Z=s0["Z"], Z_class=s0["Z_class"], n_cleared=s0["n_cleared"]),
                       qf=dict(per=sq["per"], mean=sq["mean"]), groups_ok=okg, groups_q0=dict(mean=g0["mean"], Z=g0["Z"]))
    out["S0_GR1"] = dict(max_dev=dev, ok=bool(dev < 1e-6 and out["K0c"] and all(s0gr[f]["groups_ok"] for f in FEET)), rows=s0gr)
    # ---- S0-CL2: the picture on the 63 groups (P4 T3 estimator, X62's X43 copy reproduced)
    NSG, GROUPS, solve_r0, BURK = NS["NSG"], NS["GROUPS"], NS["solve_r0"], NS["BURK"]
    G540, MS540, KP540, HERN_RE, XG, LXG, RHO_H, M_H = (NSG[k] for k in ("G540", "MSUN540", "KPC540", "HERN_RE", "XG", "LXG", "RHO_H", "M_H"))
    bgA = BGR["A_c2b_refit"]
    def group_logsig(o, foot, dlM=0.0):
        lMb = o["lM"] + dlM; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE
        rc = 3 * (100 * bgA["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540)
        M200 = 10 ** (bgA["a"] + bgA["b"] * (lMb - 10)) * MS540; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        Msun = M200 / MSUNE; flag = Msun > 10 ** TSW
        sc = sigma_cl2_pc(foot, "A_c2b_refit", Msun, SIGPC) * MSUNE / PC2
        gN = M_H / XG ** 2; use_rE = branch(flag)
        if use_rE:
            r0 = solve_r0(M200, R200, sc); Mh = math.pi * sc * r0 ** 2 * BURK(np.minimum(XG * a, R200) / r0); gN = gN + Mh / Mb / XG ** 2
        else:
            a0u = A0SI[foot] / (G540 * Mb / a ** 2); gN = np.where(gN > 0, nu(np.where(gN > 0, gN, 1.0) / a0u) * gN, gN)
        s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a
        return 0.5 * math.log10(s2) - 3.0, flag
    CL2J = json.load(open(os.path.join(REB, "CL2_native_cf_slope", "x62_x43copy_on_shpS9_L4_T12.3_B_results.json")))["footings"]
    s0c = {}; okc = True
    for f in FEET:
        d, sl, na = [], [], 0
        for o in GROUPS:
            v, fl = group_logsig(o, f); na += int(fl)
            sp = (group_logsig(o, f, 0.01)[0] - group_logsig(o, f, -0.01)[0]) / 0.02
            d.append(o["ls"] - v); sl.append(sp)
        st = NSG["class_stats"](d, sl); ref = CL2J[f]["groups"]; m = 1.01 if MUTATE else 1.0
        ok = abs(st["mean"] - ref["mean"] * m) < 1e-4 and abs(st["Z"] - ref["Z"] * m) < 1e-3 and na == ref["n_active"]
        okc = okc and ok
        s0c[f] = dict(mean=st["mean"], Z=st["Z"], verdict=st["verdict"], n_active=na, ref=dict(mean=ref["mean"], Z=ref["Z"], n_active=ref["n_active"]), ok=bool(ok))
    out["S0_CL2"] = dict(ok=bool(okc), rows=s0c)
    # ---- SLUGGS under the CL2 picture
    route_e, off_pops, score, POPS, SIGOBS = NS["route_e"], NS["off_pops"], NS["score"], NS["POPS"], NS["SIGOBS"]
    Gs, KPC, MSUN, RG, LR = NS["Gs"], NS["KPC"], NS["MSUN"], NS["RG"], NS["LR"]
    gas_profile = NS["gas_profile"]
    src528 = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG528_sluggs_centrals_mechanism", "cfg528_mechanism.py")).read()
    assert "{4486: 700.0, 5846: 380.0}" in src528
    R500 = {4486: 700.0, 5846: 380.0}                                     # kpc, CFG528 template (PROVISIONAL)
    rcA = 3 * (100 * bgA["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)    # kg/m^3
    HOSTM = {n: 500 * rcA * 4 * math.pi / 3 * (R500[n] * MPCE / 1e3) ** 3 / MSUNE for n in R500}
    SATS = (4365, 4374)                                                   # CFG331: accreted systems
    CUR = {}
    def halo_M_cl2(n, foot, q, Mstar, sig, gas=None):
        Mb = Mstar + (0.0 if gas is None else float(gas[-1]))
        M200 = 10 ** (bgA["a"] + bgA["b"] * (math.log10(Mb) - 10)) * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rcA)) ** (1 / 3)
        sc = sigma_cl2_pc(foot, "A_c2b_refit", M200 / MSUNE, SIGPC) * MSUNE / PC2
        n0 = NS["SAT"]["n"]; r0 = solve_r0(M200, R200, sc); CUR["sat"] = NS["SAT"]["n"] > n0
        CUR["lgM200"] = math.log10(M200 / MSUNE); CUR["Sig_ratio"] = sc / SIGkg[foot]
        return math.pi * sc * r0 ** 2 * BURK(np.minimum(RG * KPC, R200) / r0) / MSUNE, sc
    def law_field(n, foot, gas=None):
        b = BIN[n]; Mg = None if gas is None else gas_profile(n, gas); r12 = b["r12"]; a0 = A0SI[foot]
        Mg12 = 0.0 if Mg is None else float(np.interp(math.log(r12), LR, Mg))
        lawM = lambda M: (0.5 * M + Mg12) * float(nu(Gs * (0.5 * M + Mg12) * MSUN / (r12 * KPC) ** 2 / a0))
        from scipy.optimize import brentq
        fn = lambda lm: math.log10(lawM(10 ** lm)) - math.log10(0.5 * b["Mjam"])
        lo, hi = math.log10(b["Mjam"]) - 4, math.log10(b["Mjam"])
        if fn(lo) * fn(hi) > 0: return None
        M = 10 ** brentq(fn, lo, hi, xtol=1e-13)
        gN = Gs * (M * RG ** 2 / (RG + b["ah"]) ** 2 + (0.0 if Mg is None else Mg)) * MSUN / (RG * KPC) ** 2
        return dict(g=nu(gN / a0) * gN, M=M, frac=M / b["Mjam"])
    def own_lgM200(M): return bgA["a"] + bgA["b"] * (math.log10(M) - 10)
    def sluggs_cl2(foot, gas=None, force=None):
        per, info = {}, {}
        for n in CEN:
            sat = n in SATS; host = n in HOSTM
            if force == "law": use_rE = False
            else:
                # own M200 from the route-E JAM analogue (route E) -- the flag needs it only for host centres / isolated centrals
                NS["halo_M"] = halo_M_cl2; rE = route_e(n, foot, 0.0, SIGOBS[n], "jam", gas)
                own = own_lgM200(rE["M"] + (0.0 if gas is None else float(gas_profile(n, gas)[-1]))) if rE else float("nan")
                flag = sat or (host and HOSTM[n] > 10 ** TSW) or (own > TSW)
                use_rE = branch(flag)
            if use_rE:
                r = rE
                if r is None: per[n] = None; info[f"NGC{n}"] = "not computable (no JAM-analogue root)"; continue
                per[n] = off_pops(n, r["g"], POPS[n])
                info[f"NGC{n}"] = dict(branch="route E", class_="accreted (satellite)" if sat else "host centre", host_M500=HOSTM.get(n),
                                       Mstar_over_Mjam=r["frac"], lgMstar=math.log10(r["M"]), lgM200=CUR["lgM200"], Sigma_over_Sigma_a0=CUR["Sig_ratio"], saturated=CUR["sat"])
            else:
                r = law_field(n, foot, gas)
                if r is None: per[n] = None; info[f"NGC{n}"] = "not computable (no law JAM-analogue root)"; continue
                per[n] = off_pops(n, r["g"], POPS[n])
                info[f"NGC{n}"] = dict(branch="law", Mstar_over_Mjam=r["frac"], lgMstar=math.log10(r["M"]), lgM200_own=own_lgM200(r["M"]))
        st = score(per, foot); st["info"] = info; return st
    def cls(st, st0):
        if st["closes"]: return "PASS"
        if np.isfinite(st["mean"]) and abs(st["mean"]) <= 0.5 * abs(st0["mean"]) and st["n_reversed"] == 0: return "IMPROVES ON X38"
        return "FAILS"
    NS["K2"]["max"] = 0.0
    out["sluggs"] = {}
    HALO_GR1 = NS["halo_M"]
    for f in FEET:
        NS["halo_M"] = HALO_GR1; s0 = sluggs(f, 0.0)                         # X38 baseline (GR1's own halo, q = 0)
        NS["halo_M"] = halo_M_cl2
        st = sluggs_cl2(f); c = cls(st, s0)
        bar = sluggs_cl2(f, gas="extrap"); law = sluggs_cl2(f, force="law")
        NS["halo_M"] = HALO_GR1
        def pk(s): return dict(per=s["per"], Z=s["Z"], mean=s["mean"], Z_class=s["Z_class"], n_cleared=s["n_cleared"], n_reversed=s["n_reversed"], closes=s["closes"], info=s.get("info"))
        out["sluggs"][f] = dict(cls=c, cl2=pk(st), x38_q0=pk(s0), rep_bar=pk(bar), rep_law_all=pk(law),
                                gr1_qf=GR1J["footings"][f]["sluggs"]["st"]["mean"])
    out["K4"] = NS["K2"]["max"]; out["host_M500"] = HOSTM; out["switch"] = dict(SWITCH); out["rss"] = rss()
    out["sigobs"] = SIGOBS
    return out

# ================================================================== child 2: Milky Way (GD2 + GD1 Step 0; CL2 picture on X5's box)
def child_mw():
    out = {}
    global CACHED_SETUP
    if CACHED_SETUP is None:
        GD2SRC = os.path.join(REB, "GD2_route_e_mw_x5_box", "gd2_x5_box.py")
        ed2 = [('json.dump(RES, open(os.path.join(HERE, f"gd2_x5_box_results{TAG}.json"), "w"), indent=1)', "pass"),
               ('open(os.path.join(HERE, f"gd2_x5_box{TAG}.out"), "w").write("\\n".join(OUT) + "\\n")', "pass"),
               ("sys.exit(0 if all(v for _, v in checks) else 1)", "pass")]
        N2 = run_copy(GD2SRC, ed2, GD2SRC)
        REF2 = json.load(open(os.path.join(REB, "GD2_route_e_mw_x5_box", "gd2_x5_box_results.json")))
        ok2 = set(N2["RES"]["classes"]) == set(REF2["classes"]) and all(
            N2["RES"]["classes"][k]["cls"] == REF2["classes"][k]["cls"] and N2["RES"]["classes"][k]["counts"] == REF2["classes"][k]["counts"]
            and abs(N2["RES"]["classes"][k]["best"]["vc_R0"] - REF2["classes"][k]["best"]["vc_R0"]) < 1e-6 for k in REF2["classes"])
        out["S0_GD2"] = dict(ok=bool(ok2), classes={k: (v["cls"], v["counts"]["all"]) for k, v in N2["RES"]["classes"].items()})
        GD1SRC = os.path.join(REB, "GD1_route_e_mw_dr4", "gd1_route_e_mw.py")
        ed1 = [('json.dump(RES, open(os.path.join(HERE, f"gd1_route_e_mw_results{TAG}.json"), "w"), indent=1)', "pass"),
               ('open(os.path.join(HERE, f"gd1_route_e_mw{TAG}.out"), "w").write("\\n".join(OUT) + "\\n")', "pass"),
               ("sys.exit(0 if all(v for _, v in checks) else 1)", "pass")]
        s1 = {}; ok1 = True
        for argv, fn in (([], "gd1_route_e_mw_results.json"), (["--os1", "172.98"], "gd1_route_e_mw_results_OS1_V173.json"), (["--os1", "229.05"], "gd1_route_e_mw_results_OS1_V229.json")):
            N1 = run_copy(GD1SRC, ed1, GD1SRC, argv=argv); R1 = json.load(open(os.path.join(REB, "GD1_route_e_mw_dr4", fn)))
            for f in FEET:
                k = f"{f}|A_c2b_refit"
                a, b = N1["RES"]["headline"][k], R1["headline"][k]
                ok = abs(a["V8"]["central"] - b["V8"]["central"]) < 1e-6 and abs(a["Kz_R0_1p1_over_2piG"]["central"] - b["Kz_R0_1p1_over_2piG"]["central"]) < 1e-6
                ok1 = ok1 and ok; s1[f"{fn}|{f}"] = dict(V8=a["V8"]["central"], Kz=a["Kz_R0_1p1_over_2piG"]["central"], ok=bool(ok))
            del N1
        out["S0_GD1"] = dict(ok=bool(ok1), rows=s1)
        CACHED_SETUP=(N2,dict(out))
    else:
        N2, oldout=CACHED_SETUP; out.update(oldout)
    FIELD_CURSOR[0]=0
    # ---- CL2 picture on the GD2 path
    ns, F, L, PS = N2["ns"], N2["F"], N2["L"], N2["PS"]
    G, KZU, R0, BR_R, BR_K, BR_E5 = N2["G"], N2["KZU"], N2["R0"], N2["BR_R"], N2["BR_K"], N2["BR_E5"]
    OR, OV, OE, vE, eE, A0C = N2["OR"], N2["OV"], N2["OE"], N2["vE"], N2["eE"], N2["A0C"]
    LINE_KZ, LINE_OU, KZ_BR, KZ_BR_E, solve_r0, Bk = N2["LINE_KZ"], N2["LINE_OU"], N2["KZ_BR"], N2["KZ_BR_E"], N2["solve_r0"], N2["B"]
    SIGU = ns["SIGU"]; conv = A0C / (2 * math.pi * PS.G_SI) / SIGU
    SIG_A0_PC = {f: N2["SIG_A0"][f] / 1e6 for f in FEET}
    Rg = np.arange(15.0, 27.51, 0.5)
    def field_uncached(rhof):
        Mu = PS.mass_unit(A0C); g = ns["mw_grid"](6.6e10 / Mu)
        rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol))
        pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Phi = pr.solve_newton()
        dr, dt = g.grad_cells(Phi)
        return g, np.sin(g.t2d) * dr + np.cos(g.t2d) * dt, np.cos(g.t2d) * dr - np.sin(g.t2d) * dt, Mt * Mu
    def obs_uncached(g, dR, dz, extraR=None):
        K = g.interp_cells(dz, BR_R, np.full_like(BR_R, 1.1)) * conv
        K0 = float(g.interp_cells(dz, np.array([R0]), np.array([1.1]))[0] * conv)
        vc = float(np.sqrt(max(g.interp_cells(dR, np.array([R0]), np.array([0.0]))[0], 0) * A0C * R0 * PS.KPC) / 1e3)
        vou = np.sqrt(np.maximum(g.interp_cells(dR, OR, np.zeros_like(OR)), 0) * A0C * OR * PS.KPC) / 1e3
        o = dict(K=K, K_R0=K0, vc_R0=vc, vou=vou)
        if extraR is not None:
            o["vx"] = np.sqrt(np.maximum(g.interp_cells(dR, extraR, np.zeros_like(extraR)), 0) * A0C * extraR * PS.KPC) / 1e3
        return o
    def field(rhof):
        idx=FIELD_CURSOR[0]; FIELD_CURSOR[0]+=1
        if idx in FIELD_MASSES: return ("cached",idx),None,None,FIELD_MASSES[idx]
        v=field_uncached(rhof); FIELD_IDS[id(v[0])]=idx; FIELD_MASSES[idx]=v[3]; return v
    def idx_of(g): return g[1] if isinstance(g,tuple) else FIELD_IDS[id(g)]
    def okey(g,extraR): return (idx_of(g),None if extraR is None else tuple(float(v) for v in extraR))
    def obs(g,dR,dz,extraR=None):
        key=okey(g,extraR)
        if key not in OBS_CACHE: OBS_CACHE[key]=obs_uncached(g,dR,dz,extraR)
        return OBS_CACHE[key]
    def law_obs(g,dR,dz,foot,extraR=None):
        key=(okey(g,extraR),foot)
        if key not in LAW_CACHE:
            fac=nu(np.hypot(dR,dz)*A0C/A0SI[foot]); LAW_CACHE[key]=obs_uncached(g,fac*dR,fac*dz,extraR)
        return LAW_CACHE[key]
    def lines(vc, K, K0, vo):
        cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cO = float(np.sum(((vo - OV) / OE) ** 2))
        l1 = abs(vc - L.VC_BRIEF) <= L.VC_BRIEF_LINE and abs(vc - vE) <= 2 * eE
        D = max(cK / LINE_KZ, abs(vc - vE) / (2 * eE), cO / LINE_OU, abs(K0 - KZ_BR) / (2 * KZ_BR_E))
        return dict(vc_R0=vc, K_R0=K0, chi2_Kz=cK, chi2_Ou=cO, L1=bool(l1), L2a=bool(cK <= LINE_KZ), L2b=bool(abs(K0 - KZ_BR) <= 2 * KZ_BR_E), L3=bool(cO <= LINE_OU), D=D)
    def grade(g, dR, dz, Mb, foot, tag, extraR=None):
        bg = BGR[tag]; lM = bg["a"] + bg["b"] * (math.log10(Mb) - 10); flag = CSM_FLAG(foot, tag, SIG_A0_PC)
        b = obs(g, dR, dz, extraR); law_b = law_obs(g, dR, dz, foot, extraR)
        if branch(flag):
            Sig = sigma_cl2_pc(foot, tag, 10 ** lM, SIG_A0_PC) * 1e6                       # Msun/kpc^2
            M200 = 10 ** lM; rc = 3 * (100 * bg["h"] / 1e3) ** 2 / (8 * math.pi * G); R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
            r0, sat = solve_r0(M200, R200, Sig)
            gh = lambda r: G * math.pi * Sig * r0 ** 2 * Bk(np.asarray(r, float) / r0) / np.asarray(r, float) ** 2
            b = obs(g, dR, dz, extraR); rk = np.hypot(BR_R, 1.1); r00 = math.hypot(R0, 1.1)
            K = b["K"] + gh(rk) * 1.1 / rk / KZU; K0 = b["K_R0"] + float(gh(r00)) * 1.1 / r00 / KZU
            vc = math.sqrt(b["vc_R0"] ** 2 + R0 * float(gh(R0))); vo = np.sqrt(b["vou"] ** 2 + OR * gh(OR))
            r = lines(vc, K, K0, vo); r.update(branch="route E", lgM200=lM, Sig_ratio=Sig / 1e6 / SIG_A0_PC[foot], saturated=bool(sat))
            if extraR is not None: r["vx"] = np.sqrt(b["vx"] ** 2 + extraR * gh(extraR)).tolist()
        else:
            o = law_b
            r = lines(o["vc_R0"], o["K"], o["K_R0"], o["vou"]); r.update(branch="law", lgM200=lM)
            if extraR is not None: r["vx"] = o["vx"].tolist()
        return r
    # K3: nu == 1 path reproduces GD2's newton() for McMillan
    g, dR, dz, Mb = field(ns["rho_mcm"]); o = obs(g, dR, dz); ref = N2["newton"](ns["rho_mcm"])
    k3 = max(abs(o["vc_R0"] / ref["vc_R0"] - 1), abs(o["K_R0"] / ref["K_R0"] - 1), float(np.max(np.abs(o["K"] / ref["K"] - 1))),
             float(np.max(np.abs(o["vou"] / ref["vou"] - 1))), abs(Mb / ref["Mb"] - 1))
    out["K3"] = k3
    # McMillan (GD1 point)
    mc = {}
    for f in FEET:
        for t in BGR:
            r = grade(g, dR, dz, Mb, f, t, extraR=np.concatenate([[20.0], Rg]))
            vx = np.array(r.pop("vx")); r["V20"] = float(vx[0]); r["slope_15_27p5"] = float(np.polyfit(np.log(Rg), np.log(vx[1:]), 1)[0])
            r["z_vc_Eilers"] = (r["vc_R0"] - 229.053) / 4.645; r["z_Kz_BR"] = (r["K_R0"] - 66.4) / 2.2; r["Vb_R0"] = o["vc_R0"]; r["Kb_R0"] = o["K_R0"]
            mc[f"{f}|{t}"] = r
    out["mcmillan"] = dict(Mb=Mb, rows=mc)
    # X5's box
    import itertools
    cells = []
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID):
        rhof, p = F.rho(sb, mbb, rd); g, dR, dz, Mb = field(rhof)
        c = dict(sig_b=sb, M_bb=mbb, R_d=rd, Mstar=p["Mstar"], tag_Rd_IN=bool(L.RD_TAG[0] <= rd <= L.RD_TAG[1]),
                 tag_Mstar_IN=bool(L.MSTAR_TAG[0] <= p["Mstar"] <= L.MSTAR_TAG[1]), Mb=Mb, rows={})
        for f in FEET:
            for t in BGR: c["rows"][f"{f}|{t}"] = grade(g, dR, dz, Mb, f, t)
        cells.append(c)
    def classify(key):
        allp = [c for c in cells if all(c["rows"][key][l] for l in ("L1", "L2a", "L2b", "L3"))]
        vk = [c for c in cells if all(c["rows"][key][l] for l in ("L1", "L2a", "L2b"))]
        if any(c["tag_Rd_IN"] and c["tag_Mstar_IN"] for c in allp): cl = "FEASIBLE IN PRIORS"
        elif allp: cl = "FEASIBLE (WIDE PRIORS ONLY)"
        elif vk: cl = "V+K ONLY"
        else: cl = "INFEASIBLE"
        best = min(cells, key=lambda c: c["rows"][key]["D"]); b = best["rows"][key]
        n = {l: sum(c["rows"][key][l] for c in cells) for l in ("L1", "L2a", "L2b", "L3")}
        n["L1&L2a&L2b"] = len(vk); n["all"] = len(allp); n["L1&L2b"] = sum(c["rows"][key]["L1"] and c["rows"][key]["L2b"] for c in cells)
        n["L1&L2a"] = sum(c["rows"][key]["L1"] and c["rows"][key]["L2a"] for c in cells)
        vmax = max(cells, key=lambda c: c["rows"][key]["vc_R0"])
        br = {k: sum(c["rows"][key]["branch"] == k for c in cells) for k in ("law", "route E")}
        lgm = [c["rows"][key]["lgM200"] for c in cells]
        return dict(cls=cl, counts=n, branches=br, lgM200_range=[min(lgm), max(lgm)],
                    best=dict(sig_b=best["sig_b"], M_bb=best["M_bb"], R_d=best["R_d"], Mstar=best["Mstar"], **{k: b[k] for k in ("vc_R0", "K_R0", "chi2_Kz", "chi2_Ou", "D", "L1", "L2a", "L2b", "L3")}),
                    max_vc=dict(vc=vmax["rows"][key]["vc_R0"], K_R0=vmax["rows"][key]["K_R0"], chi2_Kz=vmax["rows"][key]["chi2_Kz"], chi2_Ou=vmax["rows"][key]["chi2_Ou"], sig_b=vmax["sig_b"], M_bb=vmax["M_bb"], R_d=vmax["R_d"]),
                    min_K_R0=min(c["rows"][key]["K_R0"] for c in cells),
                    short_disc_best_vc=max(c["rows"][key]["vc_R0"] for c in cells if c["R_d"] <= 2.27),
                    passing=[dict(sig_b=c["sig_b"], M_bb=c["M_bb"], R_d=c["R_d"]) for c in allp])
    out["box"] = {f"{f}|{t}": classify(f"{f}|{t}") for f in FEET for t in BGR}
    out["cells"] = [dict(sig_b=c["sig_b"], M_bb=c["M_bb"], R_d=c["R_d"], Mb=c["Mb"], rows={k: {kk: vv for kk, vv in v.items()} for k, v in c["rows"].items()}) for c in cells]
    out["switch"] = dict(SWITCH); out["rss"] = rss()
    return out

