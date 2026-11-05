#!/usr/bin/env python3
"""FN6_powerlaw_screening T0 Milky Way (criteria 5f0f4a5d99), form R, one footing per process. Each in-prior cell gets
its own length L = L_MW (M / 6e10 Msun)^p, M the cell's stars + gas (KT25's width mass). Engine: KT33's mw_reciprocal
imported read-only from FN1b's vendor_kt33/, with FN1b's fn1b_mw.py pieces copied verbatim in marked blocks (SHA-256
below). Points: KA1's (p 0, L_MW 2) and every grid point that passes T1-T4 on this footing in fn6_small_part*.jsonl.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I -B fn6_mw.py canonical|alt [--all] [--points p:L,...] [--mutate SEED]
kappa = 1/2 FITTED and held fixed; not theory closed."""
import ast, gc, glob, hashlib, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import warnings   # this machine's Accelerate BLAS raises false FP flags in matmul (KT14, CW1, FN1b note it); results are checked finite
for _m in ("invalid value encountered in matmul", "divide by zero encountered in matmul", "overflow encountered in matmul"): warnings.filterwarnings("ignore", message=_m)
T00 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
FN1B = os.path.join(REPO, "finish_2026_11_04", "FN1_action_call", "FN1b_fixed_length_static")
SRC_SHA = {"fn1b_mw.py": "dc4a6673289cc64063001c33d681790f922ce245275141142718f182ff5ea27e", "vendor_kt33/mw_reciprocal.py": "a6c3980eac47d27830c8c30aee9001fc54be484bb6c4caa202b47c90d3b446b5"}
def _arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
MUT = False   # FN1b's nu = 1 twin switch, off: FN6's MUTATE is the mass shuffle (--mutate SEED)
SEED = _arg("--mutate"); PTS = _arg("--points"); ODIR = _arg("--outdir", HERE)
FOOT = [a for a in sys.argv[1:] if a in ("canonical", "alt")][0]; OUT = []; RES = dict(footing=FOOT); FAILS = []
TAG = f"{FOOT}_mutate_s{SEED}" if SEED else FOOT
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
def rel(a, b): return abs(a / b - 1) if (a is not None and b) else float("inf")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30
for k_, h_ in SRC_SHA.items():
    got = hashlib.sha256(open(os.path.join(FN1B, k_), "rb").read()).hexdigest(); check(f"K-src {k_}", got == h_, f"FN1b source SHA-256 {got[:16]}... (copied from {h_[:16]}...)")
M0 = 6.0e10
def Lof(LMW, p, M): return LMW * (M / M0) ** p   # kpc; M in Msun (FN6's frozen form)
P(f"FN6 T0 Milky Way [{TAG}] (criteria 5f0f4a5d99); form R; kappa = 1/2 FITTED; not theory closed")
sys.path.insert(0, os.path.join(RB, "UX5_mw_stellar_mass")); import ux5_core   # loaded first, so the vendored module finds it (as FN1b)
sys.path.insert(0, os.path.join(FN1B, "vendor_kt33")); import mw_reciprocal as K33   # read-only import from FN1b's folder (no bytecode written)

# ---- verbatim from FN1b's fn1b_mw.py lines 25-25 (keys and KT14's four lines); source SHA-256 in SRC_SHA
LS_NEW = [0.024, 0.1, 0.25]; LS = [0.024, 0.1, 0.25, 0.5, 1.0, 2.0]; KEYS = ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk"); GATE = ("L1", "L2a", "L2b", "L3")
# ---- end of verbatim lines 25-25

# ---- verbatim from FN1b's fn1b_mw.py lines 29-52 (KT14 definitions, grid, in-prior cells, summary, solve_both); source SHA-256 in SRC_SHA
C = K33.C
def kt14_defs():
    p = os.path.join(RB, "KT14_filtered_phantom_mw", "kt14.py"); tree = ast.parse(open(p).read(), filename=p)
    keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign))]
    ns = {"__file__": p, "__name__": "kt14_definitions"}; exec(compile(ast.Module(body=keep, type_ignores=[]), p, "exec"), ns); ns["MUT"] = MUT; return ns
K14 = kt14_defs()
a0 = C.A0[FOOT]; g, Mu = C.grid(a0); sol = K33.Solver(g, Mu, a0); LU = sol.LU; LMAXF = 2 * (g.Nt - 1)
P(f"grid: Nr {g.Nr}, Nt {g.Nt}; full even angular rank lmax {LMAXF}; peak RSS so far {rss():.2f} GB")
IP = [c for c in K33.cells() if C.L.RD_TAG[0] <= c["rd"] <= C.L.RD_TAG[1] and C.L.MSTAR_TAG[0] <= K33.rho_cell(c)[1] <= C.L.MSTAR_TAG[1]]
check("K-cells", len(IP) == 1375, f"in-prior cells {len(IP)} (KT13/KT14: 1375)")
def cellkeys(c): return {k: c[k] for k in KEYS if c.get(k) is not None}
def summary(rows):
    """KT14's per-width summary, verbatim logic. rows: dicts with 'Q' (line dict), cell keys and 'Mstar'."""
    q = [o["Q"] for o in rows]; n4 = [o for o in rows if all(o["Q"][l] for l in GATE)]; cnt = {l: sum(x[l] for x in q) for l in ("L1", "L2a", "L2b", "L3", "Lh")}
    b = min(rows, key=lambda o: o["Q"]["D"]); bq = b["Q"]; kl1 = min((x["K0"] for x in q if x["L1"]), default=None)
    return dict(n_pass=len(n4), strict=sum(o["Q"]["Lh"] for o in n4), lines=cnt, K_min_L1=kl1, vc_max=max(x["vc"] for x in q),
                best={k: b.get(k) for k in KEYS + ("Mstar",)} | {k: bq[k] for k in ("vc", "K0", "cK", "cO", "h", "D")},
                passing=[{k: o.get(k) for k in KEYS + ("Mstar",)} | {k: o["Q"][k] for k in ("vc", "K0", "cK", "cO", "h", "D")} for o in sorted(n4, key=lambda o: o["Q"]["D"])][:30])
def slim(e): return {k: e[k] for k in ("vc", "K0", "cK", "cO", "h", "D", "L1", "L2a", "L2b", "L3", "Lh", "all_four")}
def solve_both(S_, c, sigma, lmax):
    """KT33's Solver.solve, copied, with the twin's nu = 1 switch: R = pn + S* ph, SO = pn + ph (discrete-energy phantom)."""
    rf, ms = K33.rho_cell(c); rho = S_.g.rho_axisym(lambda R, z: rf(R, z) / S_.mu, nq=4); pn = S_.LU.newton(rho)
    F = S_.get_filter(sigma, lmax, 120); rx = F.forward(rho); px = S_.LU.newton(rx); ph = S_.phantom(px, mut=MUT)
    return dict(Mstar=ms, so=S_.evaluate(pn + ph), r=S_.evaluate(pn + F.adjoint(ph)))
# ---- end of verbatim lines 29-52

# ---- verbatim from FN1b's fn1b_mw.py lines 64-64 (KT14's smoothing operators for V1); source SHA-256 in SRC_SHA
RIN, ROUT, ZIN, WIN = K14["RIN"], K14["ROUT"], K14["ZIN"], K14["WIN"]; radial_matrix, vsmooth = K14["radial_matrix"], K14["vsmooth"]
# ---- end of verbatim lines 64-64

# ---- verbatim from FN1b's fn1b_mw.py lines 94-114 (V1's fixed cell VC1 and its parts); source SHA-256 in SRC_SHA
VC1 = dict(box="BV2", sb=53.9, mbb=2.12e10, rd=2.6, ht=0.35, hk=1.08, fk=0.35, rdk=2.0)
check("K-VC1", any(cellkeys(c) == VC1 for c in IP), "VC1 is an in-prior cell")
HI, H2, HIr, H2r, HIz, H2z = K14["HI"], K14["H2"], K14["HIr"], K14["H2r"], K14["HIz"], K14["H2z"]; amps = K14["amps"]
def interp_f(rt, zt):
    def f(R, z):
        R = np.asarray(R, float); z = np.asarray(z, float); sh = np.broadcast(R, z).shape; Rf = np.broadcast_to(R, sh).ravel(); zf = np.broadcast_to(z, sh).ravel()
        return (np.interp(Rf, ROUT, rt, right=0.0) * np.interp(zf, ZIN, zt, right=0.0)).reshape(sh)   # KT14's I(): right=0.0
    return f
def parts(c, s):
    """Disc + gas parts of cell c: unsmoothed (analytic, rho_struct's forms) and KT14's separable 3D Gaussian smoothing (radial_matrix x vsmooth)."""
    a = amps(c)
    def f0(R, z):
        R = np.asarray(R, float); zz = np.abs(np.asarray(z, float)); Rs = np.maximum(R, 1e-6)
        return ((a["st"] / (2 * a["ZT"])) * np.exp(-zz / a["ZT"] - R / a["rd"]) + (a["sk"] / (2 * a["ZK"])) * np.exp(-zz / a["ZK"] - R / a["rk"])
                + (HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(zz / 0.17, 300)) ** 2 + (H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(zz / 0.09, 300)) ** 2)
    M = radial_matrix(ROUT, RIN, WIN, s)
    terms = [(a["st"] * (M @ np.exp(-RIN / a["rd"])), vsmooth(np.exp(-np.abs(ZIN) / a["ZT"]) / (2 * a["ZT"]), s)),
             (a["sk"] * (M @ np.exp(-RIN / a["rk"])), vsmooth(np.exp(-np.abs(ZIN) / a["ZK"]) / (2 * a["ZK"]), s)),
             (M @ HIr, vsmooth(HIz, s)), (M @ H2r, vsmooth(H2z, s))]
    del M; fs_ = [interp_f(rt, zt) for rt, zt in terms]
    return f0, (lambda R, z: sum(fi(R, z) for fi in fs_))
# ---- end of verbatim lines 94-114

def v1row(L):   # FN1b's V1 (a) and (b), lines 117-122 of fn1b_mw.py, at one length; (c) is not run (it needs KT14's SO rows; reported only in FN1b)
    f0, fs = parts(VC1, L); rho0 = g.rho_axisym(lambda R, z: f0(R, z) / Mu, nq=4); rref = g.rho_axisym(lambda R, z: fs(R, z) / Mu, nq=4)
    F = sol.get_filter(L, LMAXF, 120); er = sol.evaluate(LU.newton(rref)); ea = sol.evaluate(LU.newton(F.forward(rho0))); eb = sol.evaluate(F.adjoint(LU.newton(rho0)))
    row = {}
    for nm, e in (("a", ea), ("b", eb)):
        dv = abs(e["vc"] - er["vc"]); do = float(np.max(np.abs(np.asarray(e["vc_Ou"]) - np.asarray(er["vc_Ou"])))); dk = abs(e["K0"] - er["K0"])
        row[nm] = dict(dvc=dv, dvOu=do, dK0=dk, ok=bool(dv <= 0.3 and do <= 0.5 and dk <= 0.3))
    row["evaluable"] = bool(row["a"]["ok"] and row["b"]["ok"]); sol.filters.clear(); del f0, fs, rho0, rref; gc.collect(); return row

# ======================================================================= FN6: each cell at its own length
gm = K33.gas_mass(); MC = [K33.rho_cell(c)[1] + gm for c in IP]; IDX = {tuple(sorted(cellkeys(c).items())): i for i, c in enumerate(IP)}
FAC_MW = 1.0
if SEED:
    mu_ = json.load(open(os.path.join(HERE, f"fn6_small_mutate_s{SEED}.json")))["mutate"]; FAC_MW = mu_["factors"]["MW"]
    P(f"  MUTATE seed {SEED}: the Milky Way gets {mu_['MW_gets']} ({mu_['MW_mass']:.3g} Msun), every cell's mass x {FAC_MW:.4g}")
P(f"  cells {len(IP)}: mass (stars + gas {gm:.4g}) {min(MC):.4g} to {max(MC):.4g} Msun, median {float(np.median(MC)):.4g}")
def small_pass(tag):   # grid points where T1-T4 all pass and are evaluable on this footing
    out = []
    for fn in sorted(glob.glob(os.path.join(HERE, f"fn6_small_{tag}.jsonl"))):
        for ln in open(fn):
            o = json.loads(ln)
            if all(o[t][FOOT]["ok"] and o[t][FOOT]["evaluable"] for t in ("T1", "T2", "T3", "T4")): out.append((o["p"], o["L_MW"]))
    return out
if PTS: todo = [tuple(float(x) for x in s.split(":")) for s in PTS.split(",")]
elif SEED: todo = small_pass(f"mutate_s{SEED}")
else:   # KA1's point, then the points passing T1-T4; with --all, then every other grid point (T0 mapped across the plane)
    sp_ = [pt for pt in sorted(set(small_pass("part*"))) if pt != (0.0, 2.0)]; todo = [(0.0, 2.0)] + sp_
    if "--all" in sys.argv: todo += [(p, L) for p in (-0.5, -0.25, 0.0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.75) for L in (1.0, 1.5, 2.0, 3.0) if (p, L) not in todo]
P(f"  points to run: {todo}")
g2 = mu2 = sol2 = None
def t0_point(p, LMW):
    global g2, mu2, sol2
    t0 = time.time(); Lc = [Lof(LMW, p, m * FAC_MW) for m in MC]; res = [None] * len(IP)
    for i in sorted(range(len(IP)), key=lambda i: Lc[i]):   # sorted, so each distinct length builds one filter; summary sees FN1b's cell order
        e = solve_both(sol, IP[i], Lc[i], LMAXF); res[i] = dict(Q=e["r"], Mstar=e["Mstar"], **cellkeys(IP[i]))
    sm = summary(res); sol.filters.clear(); del res; gc.collect()
    V1 = {f"{L:.6g}": v1row(L) for L in sorted({min(Lc), max(Lc)})}
    if g2 is None: g2, mu2 = K33.make_grid(a0, 2, 1); sol2 = K33.Solver(g2, mu2, a0)
    LMAXF2 = 2 * (g2.Nt - 1); tests = [sm["best"]] + sm["passing"][:10]; cv = []
    for t in tests:   # FN1b's convergence check (refine 2, full lmax), each cell at its own length
        ck = {k: t[k] for k in KEYS if t.get(k) is not None}; L = Lc[IDX[tuple(sorted(ck.items()))]]; e2 = solve_both(sol2, ck, L, LMAXF2)["r"]
        cv.append(dict(cell=ck, L=L, dK0=e2["K0"] - t["K0"], dvc=e2["vc"] - t["vc"], all_four_r1=bool(t in sm["passing"]), all_four_r2=bool(e2["all_four"]))); sol2.filters.clear()
    flips = [o for o in cv[1:] if not o["all_four_r2"]] + ([cv[0]] if (cv[0]["all_four_r1"] != cv[0]["all_four_r2"]) else []); big = [o for o in cv if abs(o["dK0"]) > 1]
    ev = all(v["evaluable"] for v in V1.values()); gc.collect()
    return dict(p=p, L_MW=LMW, L_cells=dict(min=min(Lc), median=float(np.median(Lc)), max=max(Lc)), summary=sm, ok=bool(sm["n_pass"] >= 1), evaluable=ev, V1=V1,
                convergence=dict(rows=cv, n_flips=len(flips), grid_dependent=bool(flips or big)), runtime_s=round(time.time() - t0, 1), rss_GB=rss())
CK = os.path.join(ODIR, f"fn6_mw_{TAG}.jsonl"); done = {}
if os.path.exists(CK):
    for ln in open(CK): o = json.loads(ln); done[(o["p"], o["L_MW"])] = o
ALL = {}
for p, LMW in todo:
    o = done.get((p, LMW))
    if o is None: o = t0_point(p, LMW); open(CK, "a").write(json.dumps(o, default=float) + "\n")
    ALL[(p, LMW)] = o; sm = o["summary"]
    P(f"  T0 p {p:+.2f} L_MW {LMW:.1f} (cells {o['L_cells']['min']:.3f}-{o['L_cells']['max']:.3f} kpc): all four {sm['n_pass']}; L1 {sm['lines']['L1']} L2a {sm['lines']['L2a']} L2b {sm['lines']['L2b']} L3 {sm['lines']['L3']}; "
      f"v_c max {sm['vc_max']:.1f}; best D {sm['best']['D']:.3f}; V1 {'PASS' if o['evaluable'] else 'FAIL'}; refine 2 flips {o['convergence']['n_flips']}{' [GRID-DEPENDENT]' if o['convergence']['grid_dependent'] else ''}; {o['runtime_s']:.0f} s, RSS {o['rss_GB']:.2f} GB")
fin = all(math.isfinite(v) for o in ALL.values() for v in (o["summary"]["vc_max"], o["summary"]["best"]["vc"], o["summary"]["best"]["K0"], o["summary"]["best"]["cO"], o["summary"]["best"]["D"]))
check("K-finite", fin, "every summary value (v_c max, best v_c, K0, cO, D) is finite")
RES["points"] = {f"{p}|{L}": o for (p, L), o in ALL.items()}; RES["peak_rss_GB"] = rss(); RES["failed_checks"] = FAILS; RES["runtime_s"] = round(time.time() - T00, 1)
P(f"\npeak RSS {rss():.2f} GB; runtime {time.time() - T00:.0f} s; failed checks: {FAILS if FAILS else 0}")
open(os.path.join(ODIR, f"fn6_mw_{TAG}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(ODIR, f"fn6_mw_{TAG}.json"), "w"), indent=1, default=float)
sys.exit(1 if FAILS else 0)
