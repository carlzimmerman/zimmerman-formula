#!/usr/bin/env python3
"""FN1b T0 Milky Way at one universal Gaussian length L, one footing per process. Criteria e6e031a163.
SO rows: KT14's own functions (loaded from kt14.py without its run loop) at 0.024, 0.1, 0.25 kpc; 0.5-2 kpc carried by
fn1b_label.py from kt14.json. R rows: KT33's mw_reciprocal engine (vendored unchanged in vendor_kt33/, KT33 being uncommitted) at refine 1, cut 120 kpc, lmax at the
grid's full even rank. Known answers KA1 (KT14 at 0.25 kpc) and KA2 (KT33 at its own settings) first; V1 decides whether R
is evaluable. Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I -B fn1b_mw.py canonical|alt [--mutate].
kappa = 1/2 FITTED and held fixed; not theory closed."""
import ast, gc, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import warnings   # this machine's Accelerate BLAS raises false FP flags in matmul (KT14, CW1 note it); results are checked finite below
for _m in ("invalid value encountered in matmul", "divide by zero encountered in matmul", "overflow encountered in matmul"): warnings.filterwarnings("ignore", message=_m)
T00 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE))); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; FOOT = [a for a in sys.argv[1:] if a in ("canonical", "alt")][0]; OUT = []; RES = dict(footing=FOOT); FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok); P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
def rel(a, b): return abs(a / b - 1) if (a is not None and b) else float("inf")
def f6(x): return "None" if x is None else f"{x:.6f}"
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30
P(f"FN1b T0 Milky Way [{FOOT}] (criteria e6e031a163){'  [MUTATE: nu = 1]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
LS_NEW = [0.024, 0.1, 0.25]; LS = [0.024, 0.1, 0.25, 0.5, 1.0, 2.0]; KEYS = ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk"); GATE = ("L1", "L2a", "L2b", "L3")
# ---- engines: KT33 (import-safe module), KT14 (definitions only, its run blocks are not executed)
sys.path.insert(0, os.path.join(RB, "UX5_mw_stellar_mass")); import ux5_core   # loaded first, so the vendored module finds it
sys.path.insert(0, os.path.join(HERE, "vendor_kt33")); import mw_reciprocal as K33
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

# ================= KA2: KT33's engine at its own settings reproduces its stored grid run
st33 = json.load(open(os.path.join(HERE, "fn1b_ka_snapshot.json")))["grid_run_first25"][FOOT]; ka2 = 0.0
for row in st33:
    e = solve_both(sol, row["cell"], row["xi"], 24)
    for f_, k_ in (("so", "source_only"), ("r", "corrected")):
        for q_ in ("vc", "K0", "cO"): ka2 = max(ka2, rel(e[f_][q_], row[k_][q_]))
check("KA2", ka2 <= 1e-6, f"KT33 engine (lmax 24, KT25 widths) reproduces grid_run's first 25 cells, vc/K0/cO of source_only and corrected: max rel {ka2:.1e} (line 1e-6)")
sol.filters.clear()

# ================= KT14's C3 smoothing test at the new widths (verbatim lines), C2 mass check, SO rows, KA1
RIN, ROUT, ZIN, WIN = K14["RIN"], K14["ROUT"], K14["ZIN"], K14["WIN"]; radial_matrix, vsmooth = K14["radial_matrix"], K14["vsmooth"]
c3 = {}
for s in (0.024, 0.1):
    w = 1.3; M = radial_matrix(ROUT, RIN, WIN, s); f = np.exp(-RIN ** 2 / (2 * w * w)); ex = (w * w / (w * w + s * s)) * np.exp(-ROUT ** 2 / (2 * (w * w + s * s))); e = float(np.max(np.abs(M @ f - ex)) / ex.max())
    hz = vsmooth(np.exp(-ZIN ** 2 / (2 * 0.3 ** 2)), s); exz = (0.3 / math.hypot(0.3, s)) * np.exp(-ZIN ** 2 / (2 * (0.09 + s * s))); ez = float(np.max(np.abs(hz - exz)) / exz.max())
    c3[str(s)] = bool(e <= 1e-3 and ez <= 1e-3); P(f"  KT14 C3 xi {s}: radial max rel {e:.1e}, vertical {ez:.1e}: {'PASS' if c3[str(s)] else 'FAIL'}"); del M
check("KA1-C3", all(c3.values()), "KT14's C3 radial and vertical Gaussian tests at 0.024 and 0.1 kpc (line 1e-3)")
SO = {}; SOok = {}
for s in LS_NEW:
    K14["OPS"].clear(); c2ok = True
    for nm, c in (("first in-prior cell", IP[0]), ("shortest disc, heaviest bulge", max(IP, key=lambda t: (t["mbb"], -t["rd"])))):
        fx = K14["rho_xi"](c, s); rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        m1 = float(np.sum(g.rho_axisym(lambda R_, z_: fx(R_, z_) / Mu, nq=4) * g.vol)); m0 = float(np.sum(g.rho_axisym(lambda R_, z_: rf(R_, z_) / Mu, nq=4) * g.vol)); ob = K14["ops"](s)["mB"]
        ok = abs(m1 / m0 - 1) <= 1e-3 and abs(ob[1] / ob[0] - 1) <= 1e-3; c2ok &= ok; P(f"  KT14 C2 xi {s} {nm}: grid mass ratio - 1 {m1 / m0 - 1:+.1e}; bulge fine-grid {ob[1] / ob[0] - 1:+.1e}: {'PASS' if ok else 'FAIL'}")
    rows = []
    for c in IP:
        o = K14["solve"](c, s, a0, g, Mu, LU); o.update(c); rows.append(o)
    del fx; SO[str(s)] = summary(rows); SOok[str(s)] = bool(c2ok and (c3.get(str(s), True))); sm = SO[str(s)]
    P(f"  SO (KT14) L {s}: all four {sm['n_pass']}; L1 {sm['lines']['L1']} L2a {sm['lines']['L2a']} L2b {sm['lines']['L2b']} L3 {sm['lines']['L3']}; v_c max {sm['vc_max']:.1f}; "
      f"lowest K with v_c in line {sm['K_min_L1'] if sm['K_min_L1'] is None else round(sm['K_min_L1'], 2)}; best D {sm['best']['D']:.3f} (v_c {sm['best']['vc']:.1f}, K {sm['best']['K0']:.1f}, Ou {sm['best']['cO']:.0f}); RSS {rss():.2f} GB")
    del rows; K14["OPS"].clear(); gc.collect()
K14["OPS"].clear()
st14 = json.load(open(os.path.join(RB, "KT14_filtered_phantom_mw", "kt14.json")))[FOOT]["0.25"]; mine = SO["0.25"]
ka1 = (mine["n_pass"] == st14["n_pass"] and mine["strict"] == st14["strict"] and mine["lines"] == st14["lines"] and rel(mine["K_min_L1"], st14["K_min_L1"]) <= 1e-6
       and rel(mine["vc_max"], st14["vc_max"]) <= 1e-6 and rel(mine["best"]["D"], st14["best"]["D"]) <= 1e-6)
check("KA1", ka1, f"KT14's code at 0.25 kpc reproduces kt14.json: n_pass {mine['n_pass']}/{st14['n_pass']}, lines {mine['lines'] == st14['lines']}, "
      f"K_min_L1 {f6(mine['K_min_L1'])}/{f6(st14['K_min_L1'])}, vc_max {f6(mine['vc_max'])}/{f6(st14['vc_max'])}, best D {f6(mine['best']['D'])}/{f6(st14['best']['D'])}")
RES["SO"] = SO; RES["SO_evaluable"] = SOok; P(f"peak RSS so far {rss():.2f} GB")

# ================= V1: is KT33's S (full angular rank) accurate at fixed L? Newtonian observables of the disc + gas parts of VC1
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
V1 = {}
for L in LS:
    f0, fs = parts(VC1, L); rho0 = g.rho_axisym(lambda R, z: f0(R, z) / Mu, nq=4); rref = g.rho_axisym(lambda R, z: fs(R, z) / Mu, nq=4)
    F = sol.get_filter(L, LMAXF, 120); er = sol.evaluate(LU.newton(rref)); ea = sol.evaluate(LU.newton(F.forward(rho0))); eb = sol.evaluate(F.adjoint(LU.newton(rho0)))
    row = {}
    for nm, e in (("a", ea), ("b", eb)):
        dv = abs(e["vc"] - er["vc"]); do = float(np.max(np.abs(np.asarray(e["vc_Ou"]) - np.asarray(er["vc_Ou"])))); dk = abs(e["K0"] - er["K0"])
        row[nm] = dict(dvc=dv, dvOu=do, dK0=dk, ok=bool(dv <= 0.3 and do <= 0.5 and dk <= 0.3))
    # V1(c), reported: KT33-engine SO against KT14 SO on KT14's best-D cell at this L (computed above, or kt14.json for 0.5-2 kpc)
    b14 = SO[str(L)]["best"] if str(L) in SO else json.load(open(os.path.join(RB, "KT14_filtered_phantom_mw", "kt14.json")))[FOOT][str(L)]["best"]
    eso = solve_both(sol, cellkeys(b14), L, LMAXF)["so"]
    row["c"] = dict(dvc=abs(eso["vc"] - b14["vc"]), dK0=abs(eso["K0"] - b14["K0"]), dcO_rel=abs(eso["cO"] / b14["cO"] - 1), ok=bool(abs(eso["vc"] - b14["vc"]) <= 0.3 and abs(eso["K0"] - b14["K0"]) <= 0.3 and abs(eso["cO"] / b14["cO"] - 1) <= 0.05))
    row["evaluable"] = bool(row["a"]["ok"] and row["b"]["ok"]); V1[str(L)] = row; sol.filters.clear(); del f0, fs, rho0, rref; gc.collect()
    P(f"  V1 L {L}: (a) S.forward dvc {row['a']['dvc']:.3f} dvOu {row['a']['dvOu']:.3f} dK0 {row['a']['dK0']:.3f} {'PASS' if row['a']['ok'] else 'FAIL'}; "
      f"(b) S.adjoint dvc {row['b']['dvc']:.3f} dvOu {row['b']['dvOu']:.3f} dK0 {row['b']['dK0']:.3f} {'PASS' if row['b']['ok'] else 'FAIL'}; "
      f"(c) engines dvc {row['c']['dvc']:.3f} dK0 {row['c']['dK0']:.3f} dcO {row['c']['dcO_rel']:.3f} {'ok' if row['c']['ok'] else 'MISS [ENGINE-DEPENDENT]'}; RSS {rss():.2f} GB")
RES["V1"] = V1

# ================= R rows (and KT33-engine SO beside) at every L, all in-prior cells
RR, SO33 = {}, {}
for L in LS:
    rr, ss = [], []
    for c in IP:
        e = solve_both(sol, c, L, LMAXF); ck = cellkeys(c); rr.append(dict(Q=e["r"], Mstar=e["Mstar"], **ck)); ss.append(dict(Q=e["so"], Mstar=e["Mstar"], **ck))
    RR[str(L)] = summary(rr); SO33[str(L)] = summary(ss); sm = RR[str(L)]; sol.filters.clear()
    P(f"  R  (KT33) L {L}: all four {sm['n_pass']}; L1 {sm['lines']['L1']} L2a {sm['lines']['L2a']} L2b {sm['lines']['L2b']} L3 {sm['lines']['L3']}; v_c max {sm['vc_max']:.1f}; "
      f"lowest K with v_c in line {sm['K_min_L1'] if sm['K_min_L1'] is None else round(sm['K_min_L1'], 2)}; best D {sm['best']['D']:.3f} (v_c {sm['best']['vc']:.1f}, K {sm['best']['K0']:.1f}, Ou {sm['best']['cO']:.0f}) "
      f"| SO (KT33) all four {SO33[str(L)]['n_pass']}, best D {SO33[str(L)]['best']['D']:.3f}; RSS {rss():.2f} GB")
    del rr, ss
RES["R"] = RR; RES["SO_kt33"] = SO33

# ================= convergence, reported: refine 2, full lmax, best-D cell and up to 10 passing R cells per L
g2, mu2 = K33.make_grid(a0, 2, 1); sol2 = K33.Solver(g2, mu2, a0); LMAXF2 = 2 * (g2.Nt - 1); CONVG = {}
for L in LS:
    sm = RR[str(L)]; tests = [sm["best"]] + sm["passing"][:10]; out = []
    for t in tests:
        e2 = solve_both(sol2, cellkeys(t), L, LMAXF2)["r"]; out.append(dict(cell=cellkeys(t), dK0=e2["K0"] - t["K0"], dvc=e2["vc"] - t["vc"], all_four_r1=bool(t in sm["passing"]), all_four_r2=bool(e2["all_four"])))
    flips = [o for o in out[1:] if not o["all_four_r2"]] + ([out[0]] if (out[0]["all_four_r1"] != out[0]["all_four_r2"]) else []); big = [o for o in out if abs(o["dK0"]) > 1]
    CONVG[str(L)] = dict(rows=out, grid_dependent=bool(flips or big)); sol2.filters.clear()
    P(f"  refine 2 L {L}: best cell dK0 {out[0]['dK0']:+.3f} dvc {out[0]['dvc']:+.3f}; passing cells rechecked {len(out) - 1}, flips {len(flips)}{' [GRID-DEPENDENT]' if (flips or big) else ''}")
RES["convergence"] = CONVG; RES["lmax_full"] = [LMAXF, LMAXF2]
fin = all(math.isfinite(v) for blk in (SO, RR, SO33) for sm in blk.values() for v in (sm["vc_max"], sm["best"]["vc"], sm["best"]["K0"], sm["best"]["cO"], sm["best"]["D"]))
check("K-finite", fin, "every summary value (v_c max, best v_c, K0, cO, D) is finite")
RES["peak_rss_GB"] = rss(); RES["failed_checks"] = FAILS; RES["runtime_s"] = round(time.time() - T00, 1)
P(f"\npeak RSS {rss():.2f} GB; runtime {time.time() - T00:.0f} s; failed checks: {FAILS if FAILS else 0}")
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"fn1b_mw_{FOOT}{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"fn1b_mw_{FOOT}{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or FAILS) else 0)
