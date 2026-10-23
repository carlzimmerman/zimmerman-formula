#!/usr/bin/env python3
"""T1_efe_strength -- the external-field-effect strength measured with ONE diagnostic multiplier eps on the total host
field that enters v3's static (stiffened AQUAL, mu = x/(1+x)) solve: eps = 1 is v3, eps = 0 the isolated solve.
Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (0fbdb17c87, committed alone first).  A diagnostic, not a theory.

Stages (each its own process; one thread; < 1 GB RSS each):
  satcoma  S1's script prefix exec'd READ-ONLY (its data build, seeds, MC draws, bootstrap; D10's solver)
           -> SAT (tile 26: 45/46 satellites, 3x3 tables per eps) and COMA (tile 29: 9 UDGs) eps curves
  lens     F2's script sections 0, 1, 4 exec'd READ-ONLY (B21 Fig. 3 + covariance, inventory, stack_model; f2_aqual)
           -> Track A chi2_all(x_e), x_e = eps * x_e(noclu)
  gc       D10's clusters, MW field and likelihood tables (D10 JSON) with D10's solver (read-only)
           -> -2 lnL(eps) at the L* floor, L*_95(eps)
  wb       F2's point-mass AQUAL solver -> unscreened gamma_pm(eps) at 20 kAU (contrast only, not v3)
Assembly: per-dataset intervals, combinations, consistency (parameter goodness of fit), verdict, record classes, K1-K9.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 t1_efe_strength.py            (all stages, then the assembly)
      OMP_NUM_THREADS=1 nice -n 15 python3 t1_efe_strength.py --mutate   (check cells only; every solver gets
                                                                          eps * Newtonian y_e instead of eps * total x_e)
Deterministic, no network.  kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import contextlib, io, json, math, re, resource, subprocess, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""
STAGE = sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else None
QUICK = os.environ.get("T1_QUICK") == "1"                       # development only: tiny subsets, scratch output
OUTDIR = os.environ.get("T1_OUTDIR", HERE)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
T0 = time.time()
trapz = getattr(np, "trapezoid", None) or np.trapz


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)


def xtot(eps, xe):
    """total background field handed to a solver: eps * x_e (v3 diagnostic); MUTATE: eps * Newtonian y_e."""
    if eps <= 0 or xe <= 0:
        return 0.0
    return eps * (xe * xe / (1.0 + xe) if MUT else xe)


def y_of_x(x):
    return x * x / (1.0 + x)


def stage_path(name):
    return os.path.join(OUTDIR, f"t1_stage_{name}{SFX}.json")


def jdump(obj, fn):
    json.dump(obj, open(fn, "w"), indent=1, default=float)


def ols_slope(x, r):
    x = np.asarray(x, float); r = np.asarray(r, float)
    xm = x - x.mean()
    return float(np.sum(xm * (r - r.mean())) / np.sum(xm * xm))


def boot_slope(x, r, idx):
    x = np.asarray(x, float)[idx]; r = np.asarray(r, float)[idx]
    xm = x - x.mean(axis=1, keepdims=True)
    return np.sum(xm * (r - r.mean(axis=1, keepdims=True)), axis=1) / np.sum(xm * xm, axis=1)


# ======================================================================================== stage satcoma
EPS_SAT = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5]
EPS_COMA = [0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5]
EPS_COMA_DPROJ = [0.0, 0.1, 0.2, 0.5, 1.0]


def stage_satcoma():
    S1F = os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small", "s1_v3_hosted_small.py")
    src = open(S1F, encoding="utf-8").read()
    marker = "# ================================================================== SATELLITES: per-system native tables"
    cut = src.index(marker)
    ns = {"__file__": S1F, "__name__": "s1_prefix_readonly"}
    argv = sys.argv[:]; sys.argv = [S1F]                         # S1's own MUT stays False; this lane's MUTATE is xtot()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src[:cut], S1F, "exec"), ns)
    sys.argv = argv
    out = dict(stage="satcoma", mutate=MUT, s1_prefix_checks={k: v["ok"] for k, v in ns["CHK"].items()},
               s1_prefix_check_values={k: v["value"] for k, v in ns["CHK"].items()})
    print(f"[satcoma] S1 prefix exec'd read-only: checks {out['s1_prefix_checks']} ({time.time() - T0:.0f} s)", flush=True)
    G, MSUN, PC, KPC = ns["G"], ns["MSUN"], ns["PC"], ns["KPC"]
    logG, interp2, boot_median = ns["logG"], ns["interp2"], ns["boot_median"]
    DATASETS, BOOT, SAMP, LFLOOR = ns["DATASETS"], ns["BOOT"], ns["SAMP"], ns["LFLOOR"]
    g_host, host_mass, DY, DL, R12 = ns["g_host"], ns["host_mass"], ns["DY"], ns["DL"], ns["R12"]
    arr_free, med_free = ns["arr_free"], ns["med_free"]
    eps_sat = [0.0, 1.0] if MUT else EPS_SAT
    samp = {f: (SAMP[f][:3] if QUICK else SAMP[f]) for f in FOOTS}

    # ---------------- SAT tables
    SATT = {}
    for f in FOOTS:
        a0 = A0[f]
        for r in samp[f]:
            M0 = 10 ** r["logms"]; a = r["rh"] * PC; y0 = G * M0 * MSUN / (a * a * a0)
            Rh = (r["dhost"] if r["dhost"] else r["dist"]) * KPC
            xe = {ek: g_host(Rh, host_mass(r["host"], ek, a0), a0) / a0 for ek in ("E_lo", "E_mid", "E_hi")}
            ys = math.log10(y0) + np.array([-DY, 0.0, DY])
            Ls = math.log10(LFLOOR[f] / r["rh"]) + np.array([-DL, 0.0, DL])
            T, C90 = {}, {}
            for eps in eps_sat:
                fx = xtot(eps, xe["E_mid"])
                T[eps] = np.array([[logG(10 ** ly, fx, 10 ** lL) for lL in Ls] for ly in ys])      # (3, 3, 2) [E-W, E-V]
                if not MUT:
                    C90[eps] = np.array(logG(y0, fx, 90.0 / r["rh"]))
            SATT[(f, r["name"])] = dict(xe=xe, ys=ys, Ls=Ls, T=T, C90=C90, y0=y0, r=r)
        print(f"[satcoma] SAT {f}: {len(samp[f])} systems x {len(eps_sat)} eps tabulated ({ns['NSOLVE'][0]} solves, "
              f"worst {ns['WORST'][0]:.1e}, {time.time() - T0:.0f} s)", flush=True)

    def pred(f, X, eps, est, shift90=False):
        o = np.empty_like(X["lb"])
        for i, r in enumerate(X["rows"]):
            t = SATT[(f, r["name"])]
            lL = math.log10(LFLOOR[f]) - X["la"][i]
            v = interp2(X["ly"][i], lL, t["ys"], t["Ls"], t["T"][eps][:, :, est])
            if shift90:
                v = v + (t["C90"][eps][est] - t["T"][eps][1, 1, est])
            o[i] = v
        return o

    SAT = {}
    for f in FOOTS:
        cur = {k: dict(Delta=[], sd=[]) for k in ("primary_EW", "primary_EV", "W_EW", "primary_EW_L90")}
        for eps in eps_sat:
            for key, ds, est, s90 in (("primary_EW", "primary", 0, False), ("primary_EV", "primary", 1, False),
                                      ("W_EW", "W", 0, False), ("primary_EW_L90", "primary", 0, True)):
                if (MUT or QUICK) and key != "primary_EW":
                    continue
                X = DATASETS[(f, ds)]
                if QUICK:
                    keep = [i for i, r in enumerate(X["rows"]) if (f, r["name"]) in SATT]
                    X = dict(lb=X["lb"][keep], ly=X["ly"][keep], la=X["la"][keep], rows=[X["rows"][i] for i in keep])
                    ix = (np.random.default_rng(1).integers(0, len(keep), (200, len(keep))), np.random.default_rng(2).integers(0, X["lb"].shape[1], (200, len(keep))))
                else:
                    ix = BOOT[(f, ds)]
                m, s = boot_median(X["lb"] - pred(f, X, eps, est, s90), ix)
                cur[key]["Delta"].append(m); cur[key]["sd"].append(s)
        # tracking (central data, S1's per-system convention)
        names = [r["name"] for r in samp[f]]
        lb0, lx = [], []
        for r in samp[f]:
            b = arr_free.get(r["name"], med_free); sig = r["sigma"] * b * 1e3
            r12 = R12 * r["rh"] * PC; M = 10 ** r["logms"]
            lb0.append(math.log10(3 * sig ** 2 / r12 / (G * (M / 2) * MSUN / r12 ** 2)))
            lx.append(math.log10(SATT[(f, r["name"])]["xe"]["E_mid"]))
        lb0 = np.array(lb0); lx = np.array(lx)
        idx = np.random.default_rng(20261024).integers(0, len(names), (4000, len(names)))
        trk = dict(b=[], sd=[])
        for eps in eps_sat:
            pc = np.array([SATT[(f, n)]["T"][eps][1, 1, 0] for n in names])
            res = lb0 - pc
            trk["b"].append(ols_slope(lx, res)); trk["sd"].append(float(np.std(boot_slope(lx, res, idx))))
        xm = np.array([SATT[(f, n)]["xe"]["E_mid"] for n in names])
        scale = {ek: float(np.median(xm / np.array([SATT[(f, n)]["xe"][ek] for n in names]))) for ek in ("E_lo", "E_hi")}
        per = []
        for n in names:
            t = SATT[(f, n)]
            per.append(dict(name=n, host=t["r"]["host"], x_e_mid=t["xe"]["E_mid"], y0=t["y0"],
                            logG_EW_central={f"{e:g}": float(t["T"][e][1, 1, 0]) for e in eps_sat}))
        SAT[f] = dict(eps=eps_sat, curves=cur, tracking=dict(eps=eps_sat, **trk, n=len(names)),
                      host_scale_xmid_over=scale, median_x_e_mid=float(np.median(xm)), per_system=per,
                      lb0_central=lb0.tolist(), log_xe_mid=lx.tolist())
        print(f"[satcoma] SAT {f}: Delta(eps) " + ", ".join(f"{e:g}:{d:+.3f}" for e, d in zip(eps_sat, cur["primary_EW"]["Delta"]))
              + f"  | trk b " + ", ".join(f"{e:g}:{b:+.3f}" for e, b in zip(eps_sat, trk["b"])), flush=True)
    out["SAT"] = SAT

    # ---------------- COMA
    ADM, g_beta, se_conv = ns["ADM"], ns["g_beta"], ns["se_conv"]
    G_, MSUN_, PC_ = ns["G_"], ns["MSUN_"], ns["PC_"]
    solve = ns["solve"]

    def coma_pred(c, a0, eps, pos, Lst, mfac=1.0, dfac=1.0):
        Ms = c["Ms"] * mfac * dfac ** 2; Re = c["Re"] * dfac; a = Re * 1e3 * PC_
        y = G_ * Ms * MSUN_ / (a * a * a0)
        xe0 = g_beta(c[pos] * dfac) / a0
        d = solve(y, xtot(eps, xe0), Lst * PC_ / a if Lst else 0.0)
        return math.sqrt(d["wo"] * a0 * a) / 1e3, xe0

    def coma_stats(f, eps, pos):
        a0 = A0[f]; Lst = LFLOOR[f]
        def Es(mfac=1.0, dfac=1.0):
            o = []
            for c in ADM:
                sp_, xe0 = coma_pred(c, a0, eps, pos, Lst, mfac, dfac)
                o.append((2 * math.log(c["sig"] / sp_), 2 * c["esig"] / c["sig"], xe0))
            return o
        base = Es(); E = [x[0] for x in base]; sE = [x[1] for x in base]
        mE = float(np.mean(E)); se = se_conv(E, sE)
        mv = lambda **kw: float(np.mean([x[0] for x in Es(**kw)]))
        sM = abs(mv(mfac=10 ** 0.2) - mv(mfac=10 ** -0.2)) / 2
        sA = abs(2 * math.log(1.15) - 2 * math.log(1 / 1.15)) / 2      # sfac moves sigma_obs only (exact; S1's recipe)
        sD = abs(mv(dfac=1.05) - mv(dfac=0.95)) / 2
        ss = math.sqrt(sM ** 2 + sA ** 2 + sD ** 2)
        return dict(meanE=mE, se=se, s_M=sM, s_A=sA, s_D=sD, sigma_sys=ss, z_stat=mE / se, z_sys=mE / math.hypot(se, ss),
                    E=E, log_xe=[math.log10(x[2]) for x in base])
    eps_c = [0.0, 0.5, 1.0] if (MUT or QUICK) else EPS_COMA
    eps_p = [] if MUT else ([0.0] if QUICK else EPS_COMA_DPROJ)
    COMA = {}
    for f in FOOTS:
        cm = {"dmean": {}, "dproj": {}}
        for eps in eps_c:
            cm["dmean"][f"{eps:g}"] = coma_stats(f, eps, "dmean")
        for eps in eps_p:
            cm["dproj"][f"{eps:g}"] = coma_stats(f, eps, "dproj")
        idx = np.random.default_rng(20261025).integers(0, len(ADM), (4000, len(ADM)))
        trk = dict(eps=eps_c, b=[], sd=[])
        for eps in eps_c:
            v = cm["dmean"][f"{eps:g}"]
            trk["b"].append(ols_slope(v["log_xe"], v["E"])); trk["sd"].append(float(np.std(boot_slope(v["log_xe"], v["E"], idx))))
        COMA[f] = dict(eps_dmean=eps_c, eps_dproj=eps_p, stats=cm, tracking=trk)
        print(f"[satcoma] COMA {f}: z_sys(eps) " + ", ".join(f"{e:g}:{cm['dmean'][f'{e:g}']['z_sys']:+.2f}" for e in eps_c)
              + f" ({time.time() - T0:.0f} s)", flush=True)
    out["COMA"] = COMA
    out["worst_residual"] = ns["WORST"][0]; out["n_solves"] = ns["NSOLVE"][0]
    out["rss_gb"] = rss_gb(); out["runtime_s"] = time.time() - T0
    jdump(out, stage_path("satcoma"))


# ======================================================================================== stage lens
XG = [0.0, 0.001, 0.002, 0.003, 0.0045, 0.006, 0.008, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.025, 0.03, 0.035, 0.0425,
      0.05, 0.07, 0.085, 0.1, 0.125]


def stage_lens():
    F2F = os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing", "f2_outer_lensing.py")
    lines = open(F2F, encoding="utf-8").read().splitlines(keepends=True)
    idx = [i for i, l in enumerate(lines) if l.startswith("# ====")]
    sec = {}
    for j, i in enumerate(idx):
        m = re.match(r"# =+ (\d+)\.", lines[i])
        sec[int(m.group(1))] = "".join(lines[i:(idx[j + 1] if j + 1 < len(idx) else len(lines))])
    code = "".join(lines[:idx[0]]) + sec[1] + sec[4]
    ns = {"__file__": F2F, "__name__": "f2_prefix_readonly"}
    argv = sys.argv[:]; sys.argv = [F2F]                         # F2's own MUT (data x 1.10) stays False
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, F2F, "exec"), ns)
    sys.argv = argv
    ns["SOL"] = {}
    AQ, stack_model, data_native, C, H_NAT = ns["AQ"], ns["stack_model"], ns["data_native"], ns["C"], ns["H_NAT"]
    gls_amp, chi2_vec = ns["gls_amp"], ns["chi2_vec"]
    IDX = {k: ns[f"IDX_{k}"] for k in ("IN", "O1", "O2", "OUT", "ALL")}

    def amps(y, m, Cm):                                         # F2 section 5's amps(), same definitions
        o = {}
        for lab in ("IN", "O1", "O2", "OUT"):
            a, s = gls_amp(y, m, IDX[lab], Cm); o[f"A_{lab}"] = a; o[f"sA_{lab}"] = s
        o["chi2_all"] = chi2_vec(y, m, IDX["ALL"], Cm); o["chi2_out"] = chi2_vec(y, m, IDX["OUT"], Cm)
        o["chi2_in"] = chi2_vec(y, m, IDX["IN"], Cm)
        return o
    CENTRAL = dict(h=H_NAT["mid"], dMs=0.0, dcold=0.0, fhot=0.5, ye="zero", pz=1.0)
    ENV = dict(CENTRAL, fhot=1.0, dMs=0.2, dcold=0.2)
    Rn, Yn, fsc = data_native(H_NAT["mid"]); Cn = C * fsc * fsc
    YREF = {foot: {"noclu": 10 ** -3.215 * 1.2e-10 / A0[foot], "maxclu": 10 ** -2.30 * 1.2e-10 / A0[foot]} for foot in FOOTS}
    out = dict(stage="lens", mutate=MUT, y_ref=YREF, solves={})
    worst = [0.0]

    def put(key, y_solver, maxit):
        s = AQ.solve_efe(y_solver, maxit=maxit)
        worst[0] = max(worst[0], s["resid"])
        for foot in FOOTS:
            ns["SOL"][(foot, key)] = s
        out["solves"][key] = dict(y_solver=y_solver, x_e=s["x_e"], iters=s["iters"], resid=s["resid"])
        return s

    def evalcfg(foot, key, cfg):
        o = amps(Yn, stack_model(foot, Rn, dict(cfg, ye=key)), Cn)
        return {k: float(v) for k, v in o.items()}
    # check cells (K3): F2's own field values (the reference total field; MUTATE hands the solver eps * y_e instead)
    cells = {}
    for foot in FOOTS:
        for lab, yref, mx in (("noclu", YREF[foot]["noclu"], 300), ("maxclu", YREF[foot]["maxclu"], 300),
                              ("scan1e-05", 1e-5, 200), ("scan0.0001", 1e-4, 200)):
            xr = AQ.x_of_y(yref)
            ysol = y_of_x(xtot(1.0, xr))
            key = f"{foot}|{lab}"
            s = put(key, ysol, mx)
            cells[key] = dict(x_ref=xr, x_solved=s["x_e"], central=evalcfg(foot, key, CENTRAL))
        cells[f"{foot}|zero"] = dict(x_ref=0.0, x_solved=0.0, central=evalcfg(foot, "zero", CENTRAL))
        print(f"[lens] {foot} check cells: " + ", ".join(f"{k.split('|')[1]} chi2 {v['central']['chi2_all']:.2f}"
                                                         for k, v in cells.items() if k.startswith(foot)) + f" ({time.time() - T0:.0f} s)", flush=True)
    out["cells"] = cells
    if not MUT:
        grid = {foot: [] for foot in FOOTS}
        for x in (XG[:4] if QUICK else XG):
            if x == 0.0:
                key = "zero"
            else:
                key = f"x{x:g}"; put(key, y_of_x(x), 300)
            for foot in FOOTS:
                grid[foot].append(dict(x_e=x, central=evalcfg(foot, key, CENTRAL), envelope=evalcfg(foot, key, ENV)))
            print(f"[lens] x_e {x:g}: chi2_all canonical {grid['canonical'][-1]['central']['chi2_all']:.1f} / alt "
                  f"{grid['alt'][-1]['central']['chi2_all']:.1f}  envelope {grid['canonical'][-1]['envelope']['chi2_all']:.1f} "
                  f"({time.time() - T0:.0f} s)", flush=True)
        out["grid"] = grid
    out["worst_last_change"] = worst[0]
    out["rss_gb"] = rss_gb(); out["runtime_s"] = time.time() - T0
    jdump(out, stage_path("lens"))


# ======================================================================================== stage gc
EPS_GC = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]


def stage_gc():
    D10D = os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar")
    sys.path.insert(0, D10D)
    import d10_solver as S
    D10J = json.load(open(os.path.join(D10D, "d10_native_lstar_results.json")))
    G, Msun, kpc, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16      # D10's constants
    UPS_V, WID, A_H = 1.6, 0.15, 3.0 * kpc
    CL = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))
    GC = CL["clusters"]
    GCDIR = os.path.join(REPO, "real_research", "data", "globular_clusters")

    def rows(fn):
        o = {}
        for line in open(fn, encoding="utf-8"):
            if line.startswith("#") or line.startswith("ClusterName"):
                continue
            fl = line.rstrip("\n").split("\t"); o.setdefault(fl[0], []).append(fl)
        return o
    par, prof = rows(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv")), rows(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"))
    for g in GC:                                                   # D10's R_bin convention, verbatim
        D = float(par[g["name"]][0][3].split("+-")[0])
        pr = [p for p in prof[g["name"]] if p[6] == "RV"]
        g["Rbin_pc"] = float(pr[0][1]) / 206265.0 * D * 1e3 if len(pr) == 1 else g["rhl"]
        g["Rbin"] = g["Rbin_pc"] / g["rhl"]
        ref = D10J["clusters"][g["name"]]
        assert abs(g["Rbin"] - ref["Rbin"]) < 1e-12 and abs(g["LV"] - ref["LV"]) < 1e-6 * ref["LV"], g["name"]
    PRIMARY = ["NGC 2419", "Pal 4", "Pal 14"]

    def g_mw(R_kpc, Mb, a0):
        gN = G * Mb * Msun / (R_kpc * kpc + A_H) ** 2
        return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
    UPSG = np.geomspace(0.1, 8.0, 15); LG = np.geomspace(2.0, 500.0, 24)
    assert np.allclose(UPSG, D10J["Ups_grid"], rtol=1e-12) and np.allclose(LG, D10J["L_grid"], rtol=1e-12)
    UI = [i for i in range(15) if UPSG[i] >= 0.47]
    LI = [i for i in range(24) if 8.0 <= LG[i] <= 120.0]
    if QUICK:
        UI = UI[3:7]; LI = LI[2:6]
    GR = S.Grid2D(nper=24, Nt=16)
    eps_list = [1.0] if MUT else ([0.0, 1.0] if QUICK else EPS_GC)
    SIGT = {}; worst = 0.0; nsolve = 0
    for foot in FOOTS:
        a0 = A0[foot]
        for eps in eps_list:
            for g in GC:
                if g["name"] not in PRIMARY and eps not in (0.0, 1.0):
                    continue
                a = g["rhl"] * PC; xe = g_mw(g["RGC"], 6.0e10, a0) / a0; unit = math.sqrt(a0 * a) / 1e3
                fx = xtot(eps, xe); iso = fx <= 0
                tab = np.zeros((3, len(UI), len(LI) + 2))
                for k, iu in enumerate(UI):
                    y = G * UPSG[iu] * g["LV"] * Msun / (a * a * a0)
                    sv = S.Solver2D(GR, y, 0.0 if iso else fx, 0.0, isolated=iso); U, res, _ = sv.solve()
                    worst = max(worst, res); nsolve += 1
                    rf, gr = sv.field_monopole(); s2, vir, wo = S.jeans(rf, gr, [g["Rbin"]]); tab[:, k, 0] = [s2[0], vir, wo]
                    for j, il in enumerate(LI):
                        sv = S.Solver2D(GR, y, 0.0 if iso else fx, LG[il] * PC / a, isolated=iso); U, res, _ = sv.solve(U0=U)
                        worst = max(worst, res); nsolve += 1
                        rf, gr = sv.field_monopole(); s2, vir, wo = S.jeans(rf, gr, [g["Rbin"]]); tab[:, k, j + 1] = [s2[0], vir, wo]
                    s2, vir, wo = S.jeans(rf, S.plummer_gN(rf, y), [g["Rbin"]]); tab[:, k, -1] = [s2[0], vir, wo]
                SIGT[(foot, eps, g["name"])] = np.sqrt(tab) * unit
            print(f"[gc] {foot} eps {eps:g} done ({nsolve} solves, worst {worst:.1e}, {time.time() - T0:.0f} s)", flush=True)
    SIGI = np.array(D10J["sigma_int_grid"])
    LIK = {g["name"]: np.array(D10J["lik_tables"][f"{g['name']}|0.3"]) for g in GC}
    LU = np.linspace(math.log(UPSG[UI][0]), math.log(UPSG[UI][-1]), 600)

    def lnL(foot, eps, name, il):
        sig = SIGT[(foot, eps, name)][0, :, il]                    # E-P estimator (D10 primary)
        lsig = np.interp(LU, np.log(UPSG[UI]), np.log(sig))
        lp = np.interp(lsig, np.log(SIGI), LIK[name], left=-690.0, right=-690.0)
        z = (LU / math.log(10) - math.log10(UPS_V)) / WID; pr = np.exp(-0.5 * z * z); pr /= trapz(pr, LU)
        mx = lp.max(); return mx + math.log(max(trapz(pr * np.exp(lp - mx), LU), 1e-300))
    LGs = LG[LI]

    def curve(foot, eps, names):
        return np.array([-2 * sum(lnL(foot, eps, n, il) for n in names) for il in range(len(LI) + 2)])

    def L95(c):                                                    # D10's rule on this lane's L nodes
        d = c - c.min()
        if d[0] <= 3.84:
            return 0.0, "AQUAL allowed"
        inner = d[1:-1]; ok = np.where(inner <= 3.84)[0]
        if len(ok) == 0:
            return (float("inf"), "none") if d[-1] <= 3.84 else (float("nan"), "nan")
        i = ok[0]
        if i == 0:
            return float(LGs[0]), "at or below the lowest node"
        x1, x2 = math.log(LGs[i - 1]), math.log(LGs[i]); y1, y2 = inner[i - 1] - 3.84, inner[i] - 3.84
        return float(math.exp(x1 + (x2 - x1) * y1 / (y1 - y2))), "interpolated"

    def at_L(c, L):
        return float(np.interp(math.log(L), np.log(LGs), c[1:-1]))
    FLOOR = {"canonical": 21.68, "alt": 22.85}
    res = {}
    for foot in FOOTS:
        r = dict(eps=eps_list, chi2_floor=[], chi2_24=[], chi2_50=[], chi2_90=[], chi2_AQUAL=[], chi2_Newton=[], chi2_min=[],
                 L95=[], L95_note=[], per_cluster_floor={n: [] for n in PRIMARY}, pal3={})
        for eps in eps_list:
            c = curve(foot, eps, PRIMARY)
            r["chi2_floor"].append(at_L(c, FLOOR[foot])); r["chi2_24"].append(at_L(c, 24.0)); r["chi2_50"].append(at_L(c, 50.0))
            r["chi2_90"].append(at_L(c, 90.0)); r["chi2_AQUAL"].append(float(c[0])); r["chi2_Newton"].append(float(c[-1]))
            r["chi2_min"].append(float(c.min()))
            l, note = L95(c); r["L95"].append(l); r["L95_note"].append(note)
            for n in PRIMARY:
                r["per_cluster_floor"][n].append(at_L(curve(foot, eps, [n]), FLOOR[foot]))
            if (foot, eps, "Pal 3") in SIGT:
                cp = curve(foot, eps, ["Pal 3"]); r["pal3"][f"{eps:g}"] = dict(floor=at_L(cp, FLOOR[foot]), AQUAL=float(cp[0]), Newton=float(cp[-1]))
        print(f"[gc] {foot}: -2lnL at floor " + ", ".join(f"{e:g}:{v:.2f}" for e, v in zip(eps_list, r["chi2_floor"]))
              + " | L*_95 " + ", ".join(f"{e:g}:{v:.2f}" for e, v in zip(eps_list, r["L95"])), flush=True)
        res[foot] = r
    # K4: sigma tables at eps = 1 vs D10's committed tables at the shared nodes
    k4 = 0.0
    if (FOOTS[0], 1.0, PRIMARY[0]) in SIGT:
        cols = [0] + [1 + il for il in LI] + [25]
        for foot in FOOTS:
            for g in GC:
                ref = np.array(D10J["sigma_tables"][f"{foot}|E_mid|{g['name']}"])[:, UI][:, :, cols]
                k4 = max(k4, float(np.max(np.abs(SIGT[(foot, 1.0, g["name"])] / ref - 1))))
    # K5: eps -> 0 continuity of the embedded solve
    k5 = []
    for (y, Lam) in ((3e-3, 0.3), (0.03, 0.02)):
        sa = S.Solver2D(GR, y, 1e-8, Lam); sa.solve(); rf, gr = sa.field_monopole(); _, va, wa = S.jeans(rf, gr, [])
        sb = S.Solver2D(GR, y, 0.0, Lam, isolated=True); sb.solve(); rf, gr = sb.field_monopole(); _, vb, wb = S.jeans(rf, gr, [])
        k5.append(max(abs(math.sqrt(va / vb) - 1), abs(math.sqrt(wa / wb) - 1)))
    out = dict(stage="gc", mutate=MUT, UI=UI, LI=LI, L_nodes=LGs.tolist(), Ups_nodes=UPSG[UI].tolist(), res=res, K4=k4, K5=k5,
               x_e_mid={foot: {g["name"]: g_mw(g["RGC"], 6.0e10, A0[foot]) / A0[foot] for g in GC} for foot in FOOTS},
               worst_residual=worst, n_solves=nsolve, rss_gb=rss_gb(), runtime_s=time.time() - T0)
    jdump(out, stage_path("gc"))


# ======================================================================================== stage wb
EPS_WB = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.25, 1.5]


def stage_wb():
    sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing"))
    import f2_aqual as AQ
    G, MSUN, AU = 6.67430e-11, 1.989e30, 1.495978707e11
    GEXT = 1.778e-10                                               # PREREG primary g_ext (D2/E2)
    out = dict(stage="wb", mutate=MUT, g_ext=GEXT, r_kAU=20.0, M_Msun=2.0, curves={})
    worst = 0.0
    for foot in FOOTS:
        a0 = A0[foot]; rM = math.sqrt(G * 2.0 * MSUN / a0); s = 20e3 * AU / rM
        xe = GEXT / a0
        g = []
        for eps in ([1.0] if MUT else EPS_WB):
            x = xtot(eps, xe)
            if x <= 0:
                Me = float(AQ.M_iso(s))
            else:
                so = AQ.solve_efe(y_of_x(x)); worst = max(worst, so["resid"])
                Me = float(np.interp(math.log(s), np.log(so["r"]), so["M"]))
            g.append(math.sqrt(Me))
        out["curves"][foot] = dict(eps=[1.0] if MUT else EPS_WB, gamma_pm=g, s_over_rM=s, x_e=xe)
        print(f"[wb] {foot}: gamma_pm " + ", ".join(f"{e:g}:{v:.3f}" for e, v in zip(out['curves'][foot]['eps'], g)), flush=True)
    out["worst_last_change"] = worst; out["rss_gb"] = rss_gb(); out["runtime_s"] = time.time() - T0
    jdump(out, stage_path("wb"))


# ======================================================================================== assembly
def assemble():
    from scipy import stats
    OUT = []

    def P(s=""):
        print(s, flush=True); OUT.append(str(s))
    CHK = {}

    def check(k, ok, val, thr, what):
        CHK[k] = dict(ok=bool(ok), value=val, threshold=thr, what=what)
        P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")
    ST = {n: json.load(open(stage_path(n))) for n in ("satcoma", "lens", "gc", "wb")}
    S1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small", "s1_v3_hosted_small_results.json")))
    F2J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing", "f2_outer_lensing_results.json")))
    C6J = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini_results.json")))
    S2J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "S2_v3_lowg_lensing", "s2_v3_lowg_lensing_results.json")))
    WBJ = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG816_dr4_r_statistic_scoring", "cfg816_r_dr3_results.json")))
    N16 = json.load(open(os.path.join(REPO, "prep_2026", "aligned_firing", "fire_aligned_n16_results.json")))
    WAL = json.load(open(os.path.join(REPO, "prep_2026", "wallaby_firing", "fire_wallaby_results.json")))
    R = dict(lane="T1_efe_strength", mutate=MUT, frozen="0fbdb17c87", stages={n: dict(rss_gb=v["rss_gb"], runtime_s=v["runtime_s"]) for n, v in ST.items()})
    P("=" * 112)
    P("T1_efe_strength: EFE strength eps (eps x total host field in v3's AQUAL solve; 1 = v3, 0 = isolated)"
      + ("   *** MUTATE: eps x Newtonian y_e handed to every solver ***" if MUT else ""))
    P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled; diagnostic, not a theory")
    P("=" * 112)
    sc, ln, gc, wb = ST["satcoma"], ST["lens"], ST["gc"], ST["wb"]

    # ------------------------------------------------------------------ checks K1-K5, K8, K9 from the stages
    P("\n--- reproduction and solver checks ---")
    k1 = []
    for f in FOOTS:
        c = sc["SAT"][f]["curves"]["primary_EW"]; e = sc["SAT"][f]["eps"]
        r1 = S1J["satellites"][f"{f}|primary|S4 v3: AQUAL + EFE + screening L*floor E-W"]
        r0 = S1J["satellites"][f"{f}|primary|side: isolated native screening L*floor E-W"]
        i1, i0 = e.index(1.0), e.index(0.0)
        d = [abs(c["Delta"][i1] - r1["Delta"]), abs(c["sd"][i1] - r1["sd"]), abs(c["Delta"][i0] - r0["Delta"]), abs(c["sd"][i0] - r0["sd"])]
        k1 += d
        P(f"   K1 {f}: eps 1 Delta {c['Delta'][i1]:+.4f}+-{c['sd'][i1]:.4f} (S1 {r1['Delta']:+.4f}+-{r1['sd']:.4f}); "
          f"eps 0 {c['Delta'][i0]:+.4f}+-{c['sd'][i0]:.4f} (S1 {r0['Delta']:+.4f}+-{r0['sd']:.4f})")
    check("K1", max(k1) <= 0.005, f"{max(k1):.1e} dex", "<= 0.005", "SAT reproduces S1 at eps 1 (v3) and eps 0 (isolated native screening), L* floor, E-W")
    k2 = []
    for f in FOOTS:
        st = sc["COMA"][f]["stats"]["dmean"]
        lab0 = "floor"
        for e, key in (("1", f"{f}|S4 v3 dmean L*{lab0} E-W"), ("0.5", f"{f}|v3 dmean L*{lab0} field/2"), ("0", f"{f}|isolated bound (x_e = 0) L*{lab0}")):
            ref = S1J["coma"][key]; mine = st[e]
            k2.append(max(abs(mine["meanE"] - ref["meanE"]) / 2e-3, abs(mine["z_sys"] - ref["z_sys"]) / 1e-2))
            P(f"   K2 {f} eps {e}: <E> {mine['meanE']:+.4f} (S1 {ref['meanE']:+.4f}) z_sys {mine['z_sys']:+.3f} (S1 {ref['z_sys']:+.3f})")
    check("K2", max(k2) <= 1.0, f"max normalised diff {max(k2):.2f}", "<= 1 (|d<E>| <= 2e-3, |dz_sys| <= 0.01)", "COMA reproduces S1 at eps 1, 0.5 (field/2), 0 (isolated)")
    k3 = []
    refs = {}
    for f in FOOTS:
        refs[f"{f}|noclu"] = F2J["trackA"][f]["L5_plus_EFE_noclu=T_central"]["chi2_all"]
        refs[f"{f}|zero"] = F2J["trackA"][f]["OAT EFE y_e = 0"]["chi2_all"]
        refs[f"{f}|maxclu"] = F2J["trackA"][f]["OAT EFE y_e = maxclu"]["chi2_all"]
        refs[f"{f}|scan1e-05"] = F2J["posthoc"][f"ye_scan_{f}"]["1e-05"]["chi2_all"]
        refs[f"{f}|scan0.0001"] = F2J["posthoc"][f"ye_scan_{f}"]["0.0001"]["chi2_all"]
    for k, v in refs.items():
        mine = ln["cells"][k]["central"]["chi2_all"]; k3.append(abs(mine - v))
        P(f"   K3 {k}: chi2_all {mine:.3f} (F2 {v:.3f})")
    yref_ok = all(abs(ln["y_ref"][f][k] - F2J["y_e"][f][k]) < 1e-15 for f in FOOTS for k in ("noclu", "maxclu"))
    check("K3", max(k3) <= 1.0 and yref_ok, f"max |dchi2| {max(k3):.3f}; y_e refs {'==' if yref_ok else '!='} F2", "<= 1.0",
          "LENS reproduces F2 Track A (noclu, maxclu, y_e 0, scan 1e-5 / 1e-4)")
    # ---- A1: LENS-P2 read (P2's committed uniform-field scan) + K3b integrity
    sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing"))
    import f2_aqual as AQ
    P2J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "P2_spec_isolated_lensing", "p2_spec_isolated_lensing_results.json")))
    P2C, k3b = {}, []
    for f in FOOTS:
        scn = P2J["diagnostics"][f]["scan"]
        items = sorted(((float(k), v) for k, v in scn.items()), key=lambda t: t[0])
        ys_ = np.array([t[0] for t in items]); xs_ = np.array([AQ.x_of_y(y) for y in ys_])
        A_ = np.array([t[1]["A_out"] for t in items]); sA_ = np.array([t[1]["sA_out"] for t in items])
        a_ = P2J["amplitudes_S3"][f]["a"]
        k3b.append(max(abs(scn["0"]["A_out"] - a_["A_out"]), abs(scn["0"]["sA_out"] - a_["sA_out"])) / 1e-12)
        for k, v in P2J["efe_solves"].items():
            k3b.append(abs(AQ.x_of_y(float(k)) - v["x_e"]) / 1e-9)
        pr = P2J["verdict"][f]["profile"]; Rp = np.array(pr["R"]); d_ = np.array(pr["d"]); Cp = np.array(pr["cov"])
        io = [i for i in range(len(Rp)) if Rp[i] > 0.4]
        Ci = np.linalg.inv(Cp[np.ix_(io, io)])
        def gls(m):
            m = np.asarray(m)[io]; F = float(m @ Ci @ m); return float(m @ Ci @ d_[io]) / F, 1 / math.sqrt(F)
        def chi7(m):
            r_ = d_[io] - np.asarray(m)[io]; return float(r_ @ Ci @ r_)
        Aa, sa = gls(pr["m_a"]); k3b.append(max(abs(Aa - a_["A_out"]), abs(sa - a_["sA_out"])) / 1e-6)
        xref = AQ.x_of_y(P2J["ye_S3"][f]["c10"]["median"]); xbary = AQ.x_of_y(P2J["ye_S3"][f]["bary"]["median"])
        P2C[f] = dict(y=ys_.tolist(), x=xs_.tolist(), A_out=A_.tolist(), sA_out=sA_.tolist(), chi2=(((A_ - 1) / sA_) ** 2).tolist(),
                      x_ref=xref, x_bary=xbary, n_outer_bins=len(io),
                      chi2_7pt={k: chi7(pr[k]) for k in ("m_a", "m_b", "m_b_lo")}, gls_check=(Aa, sa),
                      A_out_b=(P2J["amplitudes_S3"][f]["b"]["A_out"], P2J["amplitudes_S3"][f]["b"]["sA_out"]),
                      A_out_b_lo=(P2J["amplitudes_S3"][f]["b_lo"]["A_out"], P2J["amplitudes_S3"][f]["b_lo"]["sA_out"]),
                      O1=[t[1]["A_O1"] for t in items], sO1=[t[1]["sA_O1"] for t in items], O2=[t[1]["A_O2"] for t in items], sO2=[t[1]["sA_O2"] for t in items])
        P(f"   K3b {f}: P2 scan nodes y_e {', '.join(f'{y:g}' for y in ys_)}; GLS A_out(a) from P2's profile {Aa:.6f}+-{sa:.6f} (P2 {a_['A_out']:.6f}+-{a_['sA_out']:.6f}); "
          f"outer bins {len(io)}; reference x_e catalogue {xref:.4f}, bary {xbary:.4f}")
    check("K3b", max(k3b) <= 1.0, f"max normalised diff {max(k3b):.2e}", "<= 1 (1e-12 scan/amplitudes; 1e-9 x_of_y; 1e-6 GLS)",
          "A1: P2's committed scan read consistently (scan node 0 = S3 (a); x_of_y = P2's solves; GLS from P2's profile)")
    R["P2_read"] = P2C
    # ---- A2 (post-hoc): K3c = P2's own estimator (w = m / jackknife var, diagonal; sigma propagated with P2's covariance)
    k3c = []
    for f in FOOTS:
        pr = P2J["verdict"][f]["profile"]; Rp = np.array(pr["R"]); d_ = np.array(pr["d"]); Cp = np.array(pr["cov"]); var = np.diag(Cp)
        for lab in ("a", "b", "b_lo"):
            m = np.array(pr["m_" + lab]); w = np.where(Rp > 0.4, m / var, 0.0); A = float(np.sum(w * d_) / np.sum(w * m))
            sp_ = float(math.sqrt(w @ Cp @ w) / np.sum(w * m)); ref = P2J["amplitudes_S3"][f][lab]
            k3c.append(max(abs(A - ref["A_out"]) / 1e-6, abs(sp_ / ref["sA_out"] - 1) / 1e-2))
            P(f"   K3c {f} ({lab}): P2 estimator A_out {A:.6f} (P2 {ref['A_out']:.6f}); propagated sigma {sp_:.4f} (P2 jackknife {ref['sA_out']:.4f})")
    check("K3c", max(k3c) <= 1.0, f"max normalised diff {max(k3c):.2e}", "<= 1 (A_out 1e-6; sigma 1 %)",
          "A2 post-hoc: P2's own diagonal-weighted amplitude reproduced from its committed profile (a, b, b_lo)")
    l95_1 = {f: gc["res"][f]["L95"][gc["res"][f]["eps"].index(1.0)] for f in FOOTS}
    k4b = max(abs(l95_1["canonical"] - 21.68), abs(l95_1["alt"] - 22.85))
    check("K4", gc["K4"] <= 1e-5 and k4b <= 0.3, f"sigma tables {gc['K4']:.1e}; L*_95(eps 1) {l95_1['canonical']:.2f}/{l95_1['alt']:.2f}",
          "<= 1e-5; within 0.3 pc of 21.68/22.85", "GC: D10's committed sigma tables and floor reproduced at eps = 1")
    check("K5", max(gc["K5"]) <= 2e-3, f"{max(gc['K5']):.1e}", "<= 2e-3", "eps -> 0 continuity: embedded x_e 1e-8 vs isolated solve")

    # ------------------------------------------------------------------ SS (C6) flatness
    P("\n--- SS: Cassini / planets (C6, read only) ---")
    Q = {}
    k6 = 0.0
    for f in FOOTS:
        a0c = C6J["inputs"]["a0"][f]
        xs = [C6J["inputs"]["E"][f][e]["ge"] / a0c for e in ("E0", "E1", "E2", "E3")]
        for L in ("24", "50", "90"):
            q = [C6J["R1_physical"][f"{f}|{L}|{e}"]["Q2"] for e in ("E0", "E1", "E2", "E3")]
            ob = [max(C6J["R1_physical"][f"{f}|{L}|{e}"]["over_Hees_upper"], C6J["R1_physical"][f"{f}|{L}|{e}"]["over_Park_upper"]) for e in ("E0", "E1", "E2", "E3")]
            p = np.polyfit(np.log(xs), np.log(q), 1)[0]
            ext = max(ob) * (1.5 * max(xs) / max(xs)) ** p            # eps = 1.5 at the strongest field (E3)
            Q[f"{f}|{L}"] = dict(x_e=xs, Q2=q, over_bound_max=max(ob), slope=p, over_bound_eps1p5=ext)
            k6 = max(k6, max(ob), ext)
            P(f"   [{f} L* {L}] Q2/bound max {max(ob):.2e} at E0-E3 (x_e {xs[0]:.2f}-{xs[-1]:.2f}); dlnQ2/dln x_e {p:.2f}; eps 1.5 -> {ext:.2e}; eps 0 -> 0 (isotropy)")
    pl = max(v["ratio"] for k, v in C6J["R2_planets"].items() if k.split("|")[1] == "24")
    P(f"   planets: hedgehog GM/L*^2 is field-independent; worst ratio to bound at 24 pc {pl:.3f} (C6 R2)")
    check("K6", k6 <= 1e-3, f"{k6:.1e}", "<= 1e-3", "SS flat premise: screened Q2/bound at E0-E3 and the eps 1.5 extrapolation")
    R["SS"] = dict(Q2=Q, planets_max_ratio_24pc=pl, reading="flat on [0, 1.5]: no eps information (screened); unscreened fails at every eps")

    # ------------------------------------------------------------------ WB
    P("\n--- WB: wide binaries ---")
    Rwb = WBJ["branches"]["primary"]["R"]; sRwb = WBJ["branches"]["primary"]["sigma_R"]
    gw = {f: wb["curves"][f]["gamma_pm"][wb["curves"][f]["eps"].index(1.0)] for f in FOOTS}
    e2 = {"canonical": 1.167, "alt": 1.199}
    check("K7", all(abs(gw[f] - e2[f]) <= 0.06 for f in FOOTS), f"gamma_pm(1) {gw['canonical']:.3f}/{gw['alt']:.3f} vs E2 1.167/1.199", "within 0.06",
          "WB unscreened contrast anchored to E2's binary AQUAL value")
    scr = {f: C6J["R3_wide_binary"][f"{f}|24"]["gamma_minus_1"] for f in FOOTS}
    P(f"   screened v3 (C6 R3, 24 pc): gamma_v - 1 = {scr['canonical'][0]:.2e}..{scr['canonical'][-1]:.2e} over E0-E3 (set by L*, not the field): flat, no eps information")
    WB = {}
    if not MUT:
        for f in FOOTS:
            e = np.array(wb["curves"][f]["eps"]); g = np.array(wb["curves"][f]["gamma_pm"])
            ch = ((g - Rwb) / sRwb) ** 2
            WB[f] = dict(eps=e.tolist(), gamma_pm=g.tolist(), chi2_vs_R=ch.tolist())
            P(f"   unscreened law-first [{f}] gamma_pm(eps): " + ", ".join(f"{a:g}:{b:.3f}" for a, b in zip(e, g))
              + f" | vs CFG825 R {Rwb:.3f}+-{sRwb:.3f}: z(eps 0) {(g[0] - Rwb) / sRwb:+.2f}, z(eps 1) {(g[list(e).index(1.0)] - Rwb) / sRwb:+.2f}, z(eps 1.5) {(g[-1] - Rwb) / sRwb:+.2f}")
    R["WB"] = dict(R_DR3=Rwb, sigma_R=sRwb, screened_gamma_minus_1_24pc=scr, unscreened=WB, E2=e2)

    # ------------------------------------------------------------------ K8, K9
    k8 = max(sc["worst_residual"], gc["worst_residual"])
    k8b = max(ln["worst_last_change"], wb["worst_last_change"])
    check("K8", k8 < 1e-8 and k8b < 1e-3, f"D10 solver {k8:.1e}; F2 solver last change {k8b:.1e}", "< 1e-8; < 1e-3 (A1)", "every production solve converged")
    rss = {n: v["rss_gb"] for n, v in ST.items()}; rss["assembly"] = rss_gb()
    check("K9", max(rss.values()) < 1.0, ", ".join(f"{k} {v:.2f}" for k, v in rss.items()) + " GB", "< 1 GB each", "peak RSS per process")
    if MUT:
        return finish(R, CHK, OUT, P)

    # ------------------------------------------------------------------ curves on a fine eps grid
    E = np.round(np.linspace(0.0, 1.5, 1501), 6)
    CURVES = {}
    for f in FOOTS:
        cv = {}
        s = sc["SAT"][f]; c = s["curves"]["primary_EW"]
        e = np.array(s["eps"]); D = np.array(c["Delta"]); sd = np.array(c["sd"])
        cv["SAT"] = dict(chi2=(np.interp(E, e, D) / np.interp(E, e, sd)) ** 2, nu=1, label="satellites (S1 tile 26), Delta/sd")
        t = s["tracking"]; b = np.interp(E, e, t["b"]); sb = np.interp(E, e, t["sd"])
        cv["SAT-TRK"] = dict(chi2=(b / sb) ** 2, nu=1, label="satellites tracking slope b/sd")
        cm = sc["COMA"][f]; ec = np.array(cm["eps_dmean"]); z = np.array([cm["stats"]["dmean"][f"{x:g}"]["z_sys"] for x in ec])
        cv["COMA"] = dict(chi2=np.interp(E, ec, z) ** 2, nu=1, label="Coma UDGs (S1 tile 29), z_sys at dmean")
        g = ln["grid"][f]; xg = np.array([q["x_e"] for q in g]); chi = np.array([q["central"]["chi2_all"] for q in g])
        xn = ln["cells"][f"{f}|noclu"]["x_solved"]
        cv["LENS-F2"] = dict(chi2=np.interp(E * xn, xg, chi), nu=59, label=f"KiDS photo-z isolated lensing (F2 Track A), x_e = eps x {xn:.4f} (noclu)")
        p2 = P2C[f]
        cv["LENS-P2"] = dict(chi2=np.interp(E * p2["x_ref"], p2["x"], p2["chi2"]), nu=1,
                             label=f"GAMA spec-isolated lensing (P2 S3 A_out), x_e = eps x {p2['x_ref']:.4f} (catalogue median)")
        cv["LENS-P2-bary"] = dict(chi2=np.interp(E * p2["x_bary"], p2["x"], p2["chi2"]), nu=1,
                                  label=f"P2 with the 'bary' reference field, x_e = eps x {p2['x_bary']:.4f} (reported)")
        r = gc["res"][f]; eg = np.array(r["eps"])
        cv["GC"] = dict(chi2=np.interp(E, eg, r["chi2_floor"]), nu=None, label="outer globulars (D10) at the L* floor, -2 lnL")
        A = {"canonical": (0.76, 0.16), "alt": (0.88, 0.15)}[f]
        cv["REC-Chae"] = dict(chi2=((E - A[0]) / A[1]) ** 2, nu=1, label="record: Chae amplitude A read as eps (CFG179; standard-MOND machinery)")
        CURVES[f] = cv

    def summarize(ch, nu):
        i = int(np.argmin(ch)); cmin = float(ch[i]); d = ch - cmin
        inside = d <= 3.84
        segs = []; j = 0
        while j < len(E):
            if inside[j]:
                k = j
                while k + 1 < len(E) and inside[k + 1]:
                    k += 1
                segs.append([float(E[j]), float(E[k])]); j = k + 1
            else:
                j += 1
        p = float(stats.chi2.sf(cmin, nu)) if nu else None
        return dict(eps_hat=float(E[i]), chi2_min=cmin, interval95=segs, dchi2_at_1=float(d[E.tolist().index(1.0)]), dchi2_at_0=float(d[0]),
                    p=p, failed=(p is not None and p < 0.01), S2=(cmin / nu if (p is not None and p < 0.01) else 1.0))

    def fmt_int(segs):
        return " U ".join(f"[{a:.3f}, {b:.3f}]" for a, b in segs) if segs else "empty"
    P("\n--- per-dataset eps constraints (fine grid 0..1.5, step 0.001; 95 % = dchi2 <= 3.84) ---")
    SUMM = {}
    for f in FOOTS:
        SUMM[f] = {}
        for d, v in CURVES[f].items():
            sm = summarize(v["chi2"], v["nu"]); SUMM[f][d] = sm
            P(f"   [{f:9s}] {d:9s} eps_hat {sm['eps_hat']:.3f}  95% {fmt_int(sm['interval95']):28s} dchi2(1) {sm['dchi2_at_1']:7.2f}  dchi2(0) {sm['dchi2_at_0']:7.2f}  "
              f"chi2_min {sm['chi2_min']:7.2f}" + (f" p {sm['p']:.1e}" if sm['p'] is not None else "") + ("  FAILED-AT-EVERY-eps (scaled S2 %.2f)" % sm["S2"] if sm["failed"] else "")
              + f"   [{v['label']}]")

    # ------------------------------------------------------------------ dataset detail
    P("\n--- dataset detail ---")
    for f in FOOTS:
        s = sc["SAT"][f]; e = s["eps"]
        for key in ("primary_EW", "primary_EV", "W_EW", "primary_EW_L90"):
            c = s["curves"][key]
            P(f"   SAT [{f}] {key:15s} Delta(eps): " + ", ".join(f"{a:g}:{b:+.3f}+-{c2:.3f}" for a, b, c2 in zip(e, c["Delta"], c["sd"])))
        t = s["tracking"]
        P(f"   SAT [{f}] tracking slope d r / d log x_e: " + ", ".join(f"{a:g}:{b:+.3f}+-{c2:.3f}" for a, b, c2 in zip(e, t["b"], t["sd"])) + f"  (n {t['n']})")
        P(f"   SAT [{f}] host-field scale: x_e(E_mid)/x_e(E_lo) median {s['host_scale_xmid_over']['E_lo']:.3f}, /x_e(E_hi) {s['host_scale_xmid_over']['E_hi']:.3f}; median x_e(E_mid) {s['median_x_e_mid']:.3f}")
        cm = sc["COMA"][f]
        P(f"   COMA [{f}] dmean <E> / z_sys: " + ", ".join(f"{a:g}:{cm['stats']['dmean'][f'{a:g}']['meanE']:+.2f}/{cm['stats']['dmean'][f'{a:g}']['z_sys']:+.2f}" for a in cm["eps_dmean"]))
        P(f"   COMA [{f}] dproj <E> / z_sys: " + ", ".join(f"{a:g}:{cm['stats']['dproj'][f'{a:g}']['meanE']:+.2f}/{cm['stats']['dproj'][f'{a:g}']['z_sys']:+.2f}" for a in cm["eps_dproj"]))
        P(f"   COMA [{f}] tracking dE/dlog x_e: " + ", ".join(f"{a:g}:{b:+.2f}+-{c2:.2f}" for a, b, c2 in zip(cm["tracking"]["eps"], cm["tracking"]["b"], cm["tracking"]["sd"])))
        g = ln["grid"][f]
        P(f"   LENS [{f}] x_e: chi2_all / chi2_in / A_O1 / A_O2 (central) | chi2_all envelope:")
        for q in g:
            c = q["central"]
            P(f"        x_e {q['x_e']:7.4f}: {c['chi2_all']:7.1f} / {c['chi2_in']:6.1f} / {c['A_O1']:.3f} / {c['A_O2']:.3f} | {q['envelope']['chi2_all']:7.1f}")
        r = gc["res"][f]
        P(f"   GC [{f}] -2lnL at floor / 24 / 50 / 90 pc / AQUAL / Newton, L*_95 (eps):")
        for i, a in enumerate(r["eps"]):
            P(f"        eps {a:4.2f}: {r['chi2_floor'][i]:6.2f} / {r['chi2_24'][i]:6.2f} / {r['chi2_50'][i]:6.2f} / {r['chi2_90'][i]:6.2f} / {r['chi2_AQUAL'][i]:6.2f} / {r['chi2_Newton'][i]:6.2f}   "
              f"L*_95 {r['L95'][i]:.2f} pc ({r['L95_note'][i]}); per cluster at floor " + ", ".join(f"{n} {r['per_cluster_floor'][n][i]:.2f}" for n in r["per_cluster_floor"]))
        P(f"   GC [{f}] Pal 3 (reported): " + ", ".join(f"eps {k}: floor {v['floor']:.2f} AQUAL {v['AQUAL']:.2f} Newton {v['Newton']:.2f}" for k, v in r["pal3"].items()))

    # LENS absolute bounds
    LB = {}
    for f in FOOTS:
        g = ln["grid"][f]; xg = np.array([q["x_e"] for q in g])
        xf = np.linspace(0, xg[-1], 12501)
        out = {}
        for cfg in ("central", "envelope"):
            ch = np.interp(xf, xg, [q[cfg]["chi2_all"] for q in g]); d = ch - ch.min()
            nu = 59; S2 = max(1.0, ch.min() / nu) if stats.chi2.sf(ch.min(), nu) < 0.01 else 1.0
            ok = np.where(d <= 3.84)[0]; oks = np.where(d / S2 <= 3.84)[0]
            out[cfg] = dict(x_hat=float(xf[np.argmin(ch)]), x95=float(xf[ok[-1]]), x95_scaled=float(xf[oks[-1]]), chi2_min=float(ch.min()), S2=S2)
        xn = ln["cells"][f"{f}|noclu"]["x_solved"]; xm = ln["cells"][f"{f}|maxclu"]["x_solved"]
        out["eps95_noclu"] = out["central"]["x95"] / xn; out["eps95_noclu_scaled"] = out["central"]["x95_scaled"] / xn
        out["eps95_maxclu"] = out["central"]["x95"] / xm; out["eps95_maxclu_scaled"] = out["central"]["x95_scaled"] / xm
        out["x_noclu"] = xn; out["x_maxclu"] = xm
        LB[f] = out
        P(f"   LENS [{f}] absolute bound: x_e,95 {out['central']['x95']:.4f} (scaled {out['central']['x95_scaled']:.4f}); envelope {out['envelope']['x95']:.4f} "
          f"(scaled {out['envelope']['x95_scaled']:.4f}) -> eps_95 {out['eps95_noclu']:.3f} (scaled {out['eps95_noclu_scaled']:.3f}) of noclu x_e {xn:.4f}; "
          f"{out['eps95_maxclu']:.3f} ({out['eps95_maxclu_scaled']:.3f}) of maxclu x_e {xm:.4f}")
    R["LENS_bounds"] = LB

    # ------------------------------------------------------------------ combinations
    P("\n--- one eps for all: combinations (Delta chi2 summed; FAILED-AT-EVERY-eps curves scaled by S2 = chi2_min/nu) ---")
    V = ["SAT", "COMA", "LENS-P2", "GC"]                                   # A1: LENS-P2 is the primary outer-lensing set
    COMBOS = {"V (primary)": (V, True), "C1 V unscaled": (V, False), "C2 V - GC": (["SAT", "COMA", "LENS-P2"], True),
              "C3 V - SAT": (["COMA", "LENS-P2", "GC"], True), "C4 V - LENS-P2": (["SAT", "COMA", "GC"], True),
              "C5 SAT -> SAT-TRK": (["SAT-TRK", "COMA", "LENS-P2", "GC"], True), "C6 V + REC-Chae": (V + ["REC-Chae"], True),
              "C7 LENS-P2 -> LENS-F2 (frozen primary)": (["SAT", "COMA", "LENS-F2", "GC"], True),
              "C8 SAT + COMA + LENS-P2": (["SAT", "COMA", "LENS-P2"], True), "C9 COMA + LENS-P2": (["COMA", "LENS-P2"], True),
              "C10 SAT + LENS-P2": (["SAT", "LENS-P2"], True),
              "C9b COMA + LENS-P2 (bary ref)": (["COMA", "LENS-P2-bary"], True), "C10b SAT + LENS-P2 (bary ref)": (["SAT", "LENS-P2-bary"], True),
              "Vb V with LENS-P2 (bary ref)": (["SAT", "COMA", "LENS-P2-bary", "GC"], True)}

    def dcurve(f, d, scaled):
        v = CURVES[f][d]; sm = SUMM[f][d]; dd = v["chi2"] - sm["chi2_min"]
        return dd / sm["S2"] if (scaled and sm["failed"]) else dd

    def classify(f, ds, scaled, res):
        ints = {d: summarize(dcurve(f, d, scaled), None)["interval95"] for d in ds}
        inside1 = all(any(a <= 1.0 <= b for a, b in ints[d]) for d in ds)
        if inside1 and res["p_PG"] >= 0.05:
            return "EFE CONSISTENT WITH v3", ints
        if res["p_PG"] >= 0.01 and res["eps_hat"] < 1 and res["dchi2_at_1"] >= 9:
            return f"DATA PREFER WEAK EFE (eps {res['eps_hat']:.2f}, 95% {fmt_int(res['interval95'])})", ints
        if res["p_PG"] < 0.01:
            return "INCONSISTENT", ints
        return "NOT DECIDED", ints
    COMB = {}
    for f in FOOTS:
        COMB[f] = {}
        for name, (ds, scaled) in COMBOS.items():
            tot = sum(dcurve(f, d, scaled) for d in ds)
            sm = summarize(tot, None); pg = sm["chi2_min"]; dof = len(ds) - 1
            res = dict(datasets=ds, scaled=scaled, eps_hat=sm["eps_hat"], interval95=sm["interval95"], dchi2_at_1=sm["dchi2_at_1"],
                       dchi2_at_0=sm["dchi2_at_0"], chi2_PG=pg, dof=dof, p_PG=float(stats.chi2.sf(pg, dof)))
            cls, ints = classify(f, ds, scaled, res)
            res["class"] = cls; res["intervals"] = ints
            conf = []
            for i in range(len(ds)):
                for j in range(i + 1, len(ds)):
                    A_, B_ = ints[ds[i]], ints[ds[j]]
                    if not any(max(a[0], b[0]) <= min(a[1], b[1]) for a in A_ for b in B_):
                        conf.append(f"{ds[i]} vs {ds[j]}")
            res["non_overlapping_pairs"] = conf
            drops = {}
            for d in ds:
                rest = [x for x in ds if x != d]
                if len(rest) >= 2:
                    drops[d] = float(min(sum(dcurve(f, x, scaled) for x in rest)))
            res["chi2_PG_without"] = drops
            res["largest_drop"] = (max(drops, key=lambda k: pg - drops[k]) if drops else None)
            COMB[f][name] = res
            P(f"   [{f:9s}] {name:20s} eps_hat {res['eps_hat']:.3f} 95% {fmt_int(res['interval95']):28s} dchi2(1) {res['dchi2_at_1']:7.2f} dchi2(0) {res['dchi2_at_0']:7.2f} "
              f"chi2_PG {pg:6.2f}/{dof} p {res['p_PG']:.1e} -> {cls}" + (f" | no-overlap: {', '.join(conf)}" if conf else "")
              + (f" | removing {res['largest_drop']} lowers chi2_PG most ({drops[res['largest_drop']]:.2f})" if drops else ""))
    R["curves_summary"] = SUMM; R["combinations"] = COMB

    # ------------------------------------------------------------------ A1: the two lensing readings on one absolute x_e axis
    P("\n--- A1: outer lensing, F2 (photo-z isolated) vs P2 (spectroscopic, hole-subtracted), absolute x_e ---")
    ABS = {}
    for f in FOOTS:
        p2 = P2C[f]; g = ln["grid"][f]
        xf2 = np.linspace(0.0, p2["x"][-1], 20001); c2 = np.interp(xf2, p2["x"], p2["chi2"]); d2 = c2 - c2.min()
        xfF = np.linspace(0.0, g[-1]["x_e"], 20001); cF = np.interp(xfF, [q["x_e"] for q in g], [q["central"]["chi2_all"] for q in g])
        SF = SUMM[f]["LENS-F2"]["S2"]; dF = (cF - cF.min()) / SF
        def rng(dd, xf):
            ok = np.where(dd <= 3.84)[0]; return [float(xf[ok[0]]), float(xf[ok[-1]])]
        xc = np.linspace(0.0, min(p2["x"][-1], g[-1]["x_e"]), 20001)
        tot = (np.interp(xc, xfF, cF) - cF.min()) / SF + (np.interp(xc, xf2, c2) - c2.min())
        ABS[f] = dict(P2_x_hat=float(xf2[np.argmin(c2)]), P2_x95=rng(d2, xf2), P2_dchi2_x0=float(d2[0]), F2_x_hat=float(xfF[np.argmin(cF)]), F2_x95_scaled=rng(dF, xfF),
                      F2_S2=SF, PG_chi2=float(tot.min()), PG_p=float(stats.chi2.sf(tot.min(), 1)), PG_x_hat=float(xc[np.argmin(tot)]),
                      P2_eps95_catalogue=[v / p2["x_ref"] for v in rng(d2, xf2)], P2_eps95_bary=[v / p2["x_bary"] for v in rng(d2, xf2)],
                      P2_chi2_7pt=p2["chi2_7pt"], P2_A_out_b=p2["A_out_b"], P2_A_out_b_lo=p2["A_out_b_lo"])
        a = ABS[f]
        P(f"   [{f}] P2: x_hat {a['P2_x_hat']:.4f}, 95% x_e [{a['P2_x95'][0]:.4f}, {a['P2_x95'][1]:.4f}] (= eps [{a['P2_eps95_catalogue'][0]:.2f}, {a['P2_eps95_catalogue'][1]:.2f}] "
          f"of the catalogue field, [{a['P2_eps95_bary'][0]:.3f}, {a['P2_eps95_bary'][1]:.3f}] of the 'bary' field); zero field at dchi2 {a['P2_dchi2_x0']:.2f}")
        P(f"   [{f}] F2: x_hat {a['F2_x_hat']:.4f}, 95% x_e (S2-scaled {SF:.2f}) [{a['F2_x95_scaled'][0]:.4f}, {a['F2_x95_scaled'][1]:.4f}]; "
          f"C11 F2 + P2 on one x_e axis: chi2_PG {a['PG_chi2']:.2f}/1, p {a['PG_p']:.1e} (joint x_hat {a['PG_x_hat']:.4f})")
        P(f"   [{f}] P2 7-point outer chi2 (a) {p2['chi2_7pt']['m_a']:.2f}, (b) {p2['chi2_7pt']['m_b']:.2f}, (b_lo) {p2['chi2_7pt']['m_b_lo']:.2f}; "
          f"A_out (b) {p2['A_out_b'][0]:.3f}+-{p2['A_out_b'][1]:.3f}, (b_lo) {p2['A_out_b_lo'][0]:.3f}+-{p2['A_out_b_lo'][1]:.3f}")
        P(f"   [{f}] P2 scan: " + ", ".join(f"y {y:g} (x {x:.4f}): A_out {A:.2f}+-{s:.2f}" for y, x, A, s in zip(p2["y"], p2["x"], p2["A_out"], p2["sA_out"])))
    R["lensing_absolute"] = ABS

    # ------------------------------------------------------------------ A3 (POST-RESULT, reported only; no verdict line)
    P("\n--- A3 post-result diagnostics (reported only) ---")
    A3 = {}
    for f in FOOTS:
        s = sc["SAT"][f]; lb0 = np.array(s["lb0_central"]); lx = np.array(s["log_xe_mid"])
        ly = np.log10([p["y0"] for p in s["per_system"]]); X = np.column_stack([np.ones_like(lx), lx, ly])
        idx = np.random.default_rng(20261026).integers(0, len(lx), (4000, len(lx)))
        part = []
        for e in s["eps"]:
            res = lb0 - np.array([p["logG_EW_central"][f"{e:g}"] for p in s["per_system"]])
            b = np.linalg.lstsq(X, res, rcond=None)[0]
            bs = np.array([np.linalg.lstsq(X[i], res[i], rcond=None)[0][1] for i in idx])
            part.append(dict(eps=e, b_xe=float(b[1]), sd=float(np.std(bs)), b_y=float(b[2])))
        cm = sc["COMA"][f]["stats"]["dmean"]["0"]; xm = float(np.median(10 ** np.array(cm["log_xe"])))
        e95 = SUMM[f]["COMA"]["interval95"][0][1]
        A3[f] = dict(SAT_partial_slope=part, corr_logxe_logy=float(np.corrcoef(lx, ly)[0, 1]), COMA_median_x_e=xm,
                     COMA_x_e_allowed_95=e95 * xm, P2_x_e_required_95=ABS[f]["P2_x95"][0], F2_x_e_allowed_95_scaled=ABS[f]["F2_x95_scaled"][1])
        P(f"   [{f}] SAT tracking slope controlled for log y0 (corr(log x_e, log y0) {A3[f]['corr_logxe_logy']:+.2f}): "
          + ", ".join(f"{q['eps']:g}:{q['b_xe']:+.2f}+-{q['sd']:.2f}" for q in part))
        P(f"   [{f}] absolute fields: Coma UDGs median x_e {xm:.3f} -> allowed x_e <= {e95 * xm:.3f} (eps_95 {e95:.3f}); "
          f"P2 lenses need x_e >= {ABS[f]['P2_x95'][0]:.4f}; F2 photo-z lenses allow x_e <= {ABS[f]['F2_x95_scaled'][1]:.4f} (S2-scaled)")
    R["A3_posthoc"] = A3

    # ------------------------------------------------------------------ verdict
    P("\n--- VERDICT (frozen rule; primary set V = {SAT, COMA, LENS-P2, GC@floor} per A1) ---")
    VER = {}
    for f in FOOTS:
        prim = COMB[f]["V (primary)"]["class"]
        if COMB[f]["V (primary)"]["non_overlapping_pairs"]:
            prim_pairs = "; non-overlapping 95% intervals: " + ", ".join(COMB[f]["V (primary)"]["non_overlapping_pairs"])
        else:
            prim_pairs = ""
        movers = [n for n, v in COMB[f].items() if n != "V (primary)" and v["class"].split(" (")[0] != prim.split(" (")[0]]
        VER[f] = dict(primary=prim, fragile=bool(movers), movers={n: COMB[f][n]["class"] for n in movers})
        mv_txt = "; ".join(n + " -> " + COMB[f][n]["class"] for n in movers)
        P(f"   [{f}] {prim}{prim_pairs}" + (f"  -- FRAGILE: {mv_txt}" if movers else ""))
    same = VER["canonical"]["primary"].split(" (")[0] == VER["alt"]["primary"].split(" (")[0]
    lane = VER["canonical"]["primary"].split(" (")[0] if same else "FOOTING SPLIT"
    P(f"   LANE VERDICT: {lane}" + ("" if same else f" (canonical {VER['canonical']['primary']}; alt {VER['alt']['primary']})"))
    R["verdict"] = dict(per_footing=VER, lane=lane)

    # ------------------------------------------------------------------ record EFE claims
    P("\n--- record EFE claims (classes per criteria Sec. 6) ---")
    REC = {}
    for f in FOOTS:
        A, sA = {"canonical": (0.76, 0.16), "alt": (0.88, 0.15)}[f]
        iv = COMB[f]["V (primary)"]["interval95"]; ivh = SUMM[f]["COMA"]["interval95"] + SUMM[f]["SAT"]["interval95"]
        ov = any(max(a, A - 2 * sA) <= min(b, A + 2 * sA) for a, b in iv)
        REC[f"Chae|{f}"] = dict(A=A, sA=sA, class_=("CONSISTENT, NOT A DETECTION (tracking not shown)" if ov else "CONTRADICTED BY THIS LANE (and NOT A DETECTION: tracking not shown)"),
                                primary_interval=iv)
        P(f"   (a) Chae SPARC [{f}] A = {A} +- {sA} (zero-intercept; tracking slope non-diagnostic) vs primary eps 95% {fmt_int(iv)}: {REC[f'Chae|{f}']['class_']}")
    a16 = N16["stacks"] if isinstance(N16.get("stacks"), dict) else {}
    A1, s1 = 2.95, 3.13; A2, s2b, s2a = -1.70, 2.12, 2.98
    w1, w2 = 1 / s1 ** 2, 1 / s2a ** 2; Ac = (A1 * w1 + A2 * w2) / (w1 + w2); sc_ = 1 / math.sqrt(w1 + w2)
    REC["directional"] = dict(n16=(A1, s1), wallaby=(A2, s2b, s2a), combined=(Ac, sc_), eps_range_k1=(Ac - 2 * sc_, Ac + 2 * sc_),
                              class_="NOT DIAGNOSTIC" if sc_ >= 1.0 else "DIAGNOSTIC")
    P(f"   (b) directional EFE: n16 Ahat {A1:+.2f}+-{s1:.2f}, WALLABY {A2:+.2f}+-{s2a:.2f} (analytic; boot {s2b:.2f}) -> combined {Ac:+.2f}+-{sc_:.2f} "
      f"(units of the QUMOND-class AQUAL floor; eps = Ahat/k, k in [1, 5]): {REC['directional']['class_']}")
    REC["WB"] = dict(CFG447="OTHER READING (unscreened law, no EFE; uses the non-scoring DR3 dry run 1.075 +- 0.055)",
                     CFG825=f"R {Rwb:.3f} +- {sRwb:.3f}: v3 screened gamma_v - 1 ~ 8e-6 at every eps -> NOT DIAGNOSTIC for eps in v3",
                     unscreened={f: WB[f] for f in FOOTS})
    for f in FOOTS:
        g = np.array(WB[f]["gamma_pm"]); e = np.array(WB[f]["eps"]); okk = e[np.abs(g - Rwb) <= 2 * sRwb]
        REC["WB"][f"unscreened_2sigma_eps|{f}"] = okk.tolist()
        P(f"   (c) wide binaries [{f}]: CFG447 -> OTHER READING; CFG825 R {Rwb:.3f}+-{sRwb:.3f} -> NOT DIAGNOSTIC for v3 (screened); "
          f"unscreened law-first gamma_pm within 2 sigma of R at eps in {okk.tolist()}")
    REC["CFG478"] = "OTHER READING (QUMOND force-with-EFE vs satellite lensing; ownership-era model)"
    P(f"   (d) CFG478: {REC['CFG478']}")
    for f in FOOTS:
        s = sc["SAT"][f]; e = s["eps"]; c = s["curves"]["primary_EW"]
        P(f"   (e) S1 [{f}]: EFE step at the floor Delta(1) - Delta(0) = {c['Delta'][e.index(1.0)] - c['Delta'][e.index(0.0)]:+.3f} dex "
          f"(S1's +0.58/+0.57 is the L* = 0 step S3 - S2); F2: data/model A_O2 at noclu = {F2J['trackA'][f]['L5_plus_EFE_noclu=T_central']['A_O2']:.2f} "
          f"-> the EFE prediction is too LOW (the brief's 'too high' is a sign slip); S2: chi2_in moves {min(q['central']['chi2_in'] for q in ln['grid'][f]):.1f}-{max(q['central']['chi2_in'] for q in ln['grid'][f][:16]):.1f} for x_e <= 0.0425")
    R["record"] = REC
    R["S2_committed_A"] = {k: v for k, v in S2J.items() if k.startswith("central") or k.startswith("cells")} if isinstance(S2J, dict) else None
    return finish(R, CHK, OUT, P)


def finish(R, CHK, OUT, P):
    npass = sum(v["ok"] for v in CHK.values())
    R["checks"] = CHK; R["runtime_s_assembly"] = time.time() - T0
    P(f"\nT1_EFE_STRENGTH COMPLETE: {npass}/{len(CHK)} checks PASS." + ("  (MUTATE: check cells only)" if MUT else ""))
    jdump(R, os.path.join(OUTDIR, f"t1_efe_strength_results{SFX}.json"))
    open(os.path.join(OUTDIR, f"t1_efe_strength{SFX}.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if npass == len(CHK) else 1


# ======================================================================================== main
if __name__ == "__main__":
    if STAGE:
        {"satcoma": stage_satcoma, "lens": stage_lens, "gc": stage_gc, "wb": stage_wb}[STAGE]()
        sys.exit(0)
    skip = os.environ.get("T1_SKIP_STAGES", "") == "1"            # development: reuse existing stage files
    for st in ("wb", "gc", "lens", "satcoma"):
        if skip and os.path.exists(stage_path(st)):
            continue
        cmd = [sys.executable, os.path.abspath(__file__), "--stage", st] + (["--mutate"] if MUT else [])
        rc = subprocess.run(cmd, env=dict(os.environ)).returncode
        if rc != 0:
            print(f"stage {st} failed (exit {rc})", flush=True); sys.exit(2)
    sys.exit(assemble())
