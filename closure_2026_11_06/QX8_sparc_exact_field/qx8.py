#!/usr/bin/env python3
"""QX8: the flagship SPARC grade (PAPER67 / FG1 / EM1-P4 grader, line rms <= 0.110 and median U 0.50-0.80) on the
action's exact static field (AQUAL, mu = x/(1+x); QX4's solver imported read-only). Criteria: FROZEN_CRITERIA.md.
kappa = 1/2 FITTED; not theory closed. Footings never pooled.

Run (from the repo root):
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX8_sparc_exact_field/qx8.py solve [--workers 4]
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX8_sparc_exact_field/qx8.py grade            -> qx8.out/json
  OMP_NUM_THREADS=1 nice -n 15 python3 closure_2026_11_06/QX8_sparc_exact_field/qx8.py grade --mutate   -> qx8_MUTATE.*
"""
import os, sys, math, json, time, warnings
import numpy as np
import scipy.sparse.linalg as spla
from scipy.optimize import nnls

warnings.filterwarnings("ignore", category=RuntimeWarning)   # macOS Accelerate matmul FP-flag warnings; values are checked
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX4_udg"))
import aqual as A                                                    # noqa: E402  (read-only import)

DATA = os.path.join(REPO, "real_research", "data")
PARTS = os.path.join(HERE, "parts")
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
NODES = np.array([0.30, 0.42, 0.60, 0.85, 1.20])
HELD = np.array([0.50, 0.72])
GRID = (160, 48); LADDER = (240, 72)
ZG = 0.15
KPC_S = 3.0857e19
LN10 = math.log(10.0)


def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))


# ------------------------------------------------------------------ SPARC: P4/EM1 loader, mask and weights (verbatim logic)
def load_sparc():
    d_ = os.path.join(DATA, "sparc_data"); gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        try:
            d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        gal.append(dict(name=f.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4],
                        Vbul=d[:, 5], SBd=d[:, 6] if d.shape[1] > 6 else np.zeros(len(d)), SBb=d[:, 7] if d.shape[1] > 7 else np.zeros(len(d))))
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            tab[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError:
            continue
    for g_ in gal:
        g_["meta"] = tab[g_["name"]]
        R = g_["R"] * KPC_S
        VB2 = np.sign(g_["Vgas"])[:, None] * g_["Vgas"][:, None] ** 2 + UPS[None, :] * g_["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * g_["Vbul"][:, None] ** 2
        GB = VB2 * 1e6 / R[:, None]
        GO = (g_["Vobs"] * 1e3) ** 2 / R
        OK = (GB > 0) & (GO > 0)[:, None] & np.isfinite(GB) & (g_["Vobs"] > 0)[:, None]
        g_.update(Rm=R, GB=GB, GO=GO, OK=OK, W=1.0 / (np.clip(g_["eV"], 1, None) / np.clip(g_["Vobs"], 1, None)) ** 2)
    return gal


def fit_one(q, lgp):
    OK, W = q["OK"], q["W"]
    r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0)
    Wm = np.where(OK, W[:, None], 0.0)
    wr2 = (Wm * r * r).sum(-2); ws = np.broadcast_to(Wm.sum(-2), wr2.shape)
    i = np.argmin(wr2 / np.maximum(ws, 1e-300), axis=-1)
    take = lambda a: np.take_along_axis(a, i[..., None], -1)[..., 0]
    return take(wr2), take(ws), i


def pooled(rows):
    wr2 = [r[0] for r in rows]; ws = [r[1] for r in rows]; iu = [r[2] for r in rows]
    return dict(rms=float(math.sqrt(np.sum(wr2) / np.sum(ws))), U_median=float(np.median(UPS[np.asarray(iu)])))


def line(st):
    return bool(st["rms"] <= 0.110 and 0.50 <= st["U_median"] <= 0.80)


# ------------------------------------------------------------------ fast deposit (same quadrature as aqual.Grid.deposit)
class Dep:
    def __init__(self, g, nsub=6):
        u = (np.arange(nsub) + 0.5) / nsub
        x = g.xf[:-1, None] + u[None, :] * g.dx                                    # (nr, ns)
        r = np.exp(x)
        dt = (g.tf[1:] - g.tf[:-1]) / nsub                                          # (nt,)
        t = g.tf[:-1, None] + u[None, :] * (g.tf[1:] - g.tf[:-1])[:, None]          # (nt, ns)
        self.R = r[:, None, :, None] * np.sin(t)[None, :, None, :]                  # (nr, nt, ns_r, ns_t)
        self.z = r[:, None, :, None] * np.cos(t)[None, :, None, :]
        self.w = 2 * np.pi * (r ** 3)[:, None, :, None] * np.sin(t)[None, :, None, :] * (g.dx / nsub) * dt[None, :, None, None]

    def __call__(self, rho_fn):
        return np.sum(rho_fn(self.R, self.z) * self.w, axis=(2, 3))


def vc2(g, Phi, R):
    """Signed V^2 = dPhi/dln r on the plane-adjacent row (same as aqual.midplane_vc without the clip)."""
    d = np.gradient(Phi[:, -1], g.xc)
    return np.interp(np.log(R), g.xc, d)


# ------------------------------------------------------------------ one galaxy's components and exact solves
def components(q, g, dep):
    R = q["R"]; Rd = max(q["meta"]["Rdisk"], 0.05); zd = 0.196 * Rd ** 0.633; Rl = R[-1]
    SB = np.asarray(q["SBd"], float) * 1e6                                         # Msun/kpc^2 at U = 1
    pos = SB > 0
    if pos.sum() >= 2:
        lR, lS = R[pos], np.log(SB[pos])
        def Sig(Rx):
            inner = np.interp(Rx, lR, lS, left=lS[0], right=lS[-1])
            out = lS[-1] - (Rx - lR[-1]) / Rd
            v = np.where(Rx <= lR[-1], inner, out)
            return np.where(Rx <= lR[-1] + 6 * Rd, np.exp(v), 0.0)
        Md = dep(lambda Rx, z: Sig(Rx) * np.exp(-np.abs(z) / zd) / (2 * zd))
    else:
        Md = np.zeros((g.nr, g.nt))
    # bulge (U = 1)
    Vb = np.asarray(q["Vbul"], float)
    if np.any(Vb > 0):
        Mr = np.maximum.accumulate(np.maximum(Vb ** 2 * R / A.G, 0.0))
        rr = np.concatenate([[0.0], R]); MM = np.concatenate([[0.0], Mr])
        rho_s = np.zeros(len(R) + 1)
        rho_s[1:] = np.diff(MM) / (4 / 3 * np.pi * np.diff(rr ** 3))               # shell-average density
        def rho_b(Rx, z):
            r = np.sqrt(Rx * Rx + z * z)
            k = np.searchsorted(rr, r, side="right")
            out = np.where(k < len(rr), rho_s[np.minimum(k, len(rr) - 1)], 0.0)
            return np.where(r <= rr[-1], out, 0.0)
        Mb = dep(rho_b)
    else:
        Mb = np.zeros((g.nr, g.nt))
    # gas: NNLS on sech^2 annuli, basis from the solver in Newton mode
    edges = np.concatenate([[0.0], np.sqrt(R[:-1] * R[1:]), [1.1 * Rl]])
    An = A.assemble(g, np.zeros((g.nr, g.nt)), 1.0, True).tocsc(); lu = spla.splu(An)
    nsolve = lambda M: lu.solve(4 * np.pi * A.G * M.ravel()).reshape(g.nr, g.nt)
    basis = []; Mann = []
    for k in range(len(edges) - 1):
        a, b = edges[k], edges[k + 1]
        Mk = dep(lambda Rx, z, a=a, b=b: ((Rx >= a) & (Rx < b)) / (np.pi * (b * b - a * a)) / (2 * ZG * np.cosh(np.clip(z / ZG, -50, 50)) ** 2))
        Mann.append(Mk); basis.append(vc2(g, nsolve(Mk), R))
    B = np.array(basis).T
    y = np.sign(q["Vgas"]) * q["Vgas"] ** 2
    if np.any(y > 0):                                                  # columns scaled to unit norm (conditioning);
        cn = np.maximum(np.linalg.norm(B, axis=0), 1e-300)              # NNLS, with bounded least squares as fallback
        try:
            ws_, _ = nnls(B / cn, y, maxiter=200 * B.shape[1])
        except RuntimeError:
            from scipy.optimize import lsq_linear
            ws_ = lsq_linear(B / cn, y, bounds=(0, np.inf), lsmr_tol="auto", max_iter=10000).x
        wts = ws_ / cn
    else:
        wts = np.zeros(B.shape[1])
    Mg = np.tensordot(wts, np.array(Mann), axes=1) if len(Mann) else np.zeros((g.nr, g.nt))
    v2 = {k: vc2(g, nsolve(M), R) for k, M in (("gas", Mg), ("disk", Md), ("bul", Mb))}
    return dict(Mg=Mg, Md=Md, Mb=Mb, v2=v2, zd=zd)


def exact_T(q, g, comp, a0, U_list, mu_one=False):
    R = q["R"]; Ts, res_l, it_l, nneg = [], [], [], 0; Phi0 = None
    for U in U_list:
        M = comp["Mg"] + U * comp["Md"] + 1.4 * U * comp["Mb"]
        Phi, res, it = A.solve(g, M, a0, mu_one=mu_one, tol=1e-7, maxit=400, Phi0=Phi0)
        Phi0 = Phi
        gx = vc2(g, Phi, R) / R
        gN = (comp["v2"]["gas"] + U * comp["v2"]["disk"] + 1.4 * U * comp["v2"]["bul"]) / R
        ok = (gx > 0) & (gN > 0)
        T = np.where(ok, np.log10(np.where(ok, gx, 1.0) / np.where(ok, nu(gN / a0) * gN, 1.0)), 0.0)
        nneg += int((~ok).sum()); Ts.append(T); res_l.append(float(res)); it_l.append(int(it))
    return np.array(Ts), res_l, it_l, nneg


def grid_for(q, nrnt):
    return A.Grid(0.02 * q["R"][0], 300.0 * q["R"][-1], *nrnt, p=2.0)


def solve_task(task):
    foot, gi, extra = task
    out = os.path.join(PARTS, foot, f"{gi:03d}.npz")
    if os.path.exists(out):
        return out
    while os.getloadavg()[0] > 45:
        time.sleep(30)
    GALS = load_sparc(); q = GALS[gi]; a0 = A.a0_kpc(FOOT[foot]); t0 = time.time()
    g = grid_for(q, GRID); dep = Dep(g); comp = components(q, g, dep)
    T, res, its, nneg = exact_T(q, g, comp, a0, NODES)
    # K4 reconstruction at U = 0.5
    v2s = comp["v2"]["gas"] + 0.5 * comp["v2"]["disk"] + 0.7 * comp["v2"]["bul"]
    v2d = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
    m = (np.abs(v2d) > 1.0) & (q["Vobs"] > 0)
    W = q["W"]
    k4 = float(np.sqrt(np.sum(W[m] * ((v2s[m] - v2d[m]) / np.abs(v2d[m])) ** 2) / max(np.sum(W[m]), 1e-300))) if m.any() else float("nan")
    rec = dict(name=q["name"], T=T, res=np.array(res), its=np.array(its), nneg=nneg, k4=k4, dt=time.time() - t0)
    if extra:
        Th, resh, _, _ = exact_T(q, g, comp, a0, HELD)
        gL = grid_for(q, LADDER); depL = Dep(gL); compL = components(q, gL, depL)
        TL, resL, _, _ = exact_T(q, gL, compL, a0, NODES)
        rec.update(T_held=Th, res_held=np.array(resh), T_ladder=TL, res_ladder=np.array(resL))
        if foot == "canonical":                                       # sensitivity, reported only, U = 0.60
            global ZG
            zg0 = ZG
            ZG = 2 * zg0; compg = components(q, g, dep); ZG = zg0
            Tg, _, _, _ = exact_T(q, g, compg, a0, [0.60])
            compd = components_zd2(q, g, dep)
            Td, _, _, _ = exact_T(q, g, compd, a0, [0.60])
            rec.update(T_zg2=Tg[0], T_zd2=Td[0])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    np.savez(out + ".tmp.npz", **{k: (np.asarray(v) if not isinstance(v, str) else np.array(v)) for k, v in rec.items()})
    os.replace(out + ".tmp.npz", out)
    return out


def components_zd2(q, g, dep):
    """Same as components() with the stellar z_d doubled (sensitivity only)."""
    c = components(q, g, dep)
    R = q["R"]; Rd = max(q["meta"]["Rdisk"], 0.05); zd = 2 * 0.196 * Rd ** 0.633
    SB = np.asarray(q["SBd"], float) * 1e6; pos = SB > 0
    if pos.sum() >= 2:
        lR, lS = R[pos], np.log(SB[pos])
        def Sig(Rx):
            inner = np.interp(Rx, lR, lS, left=lS[0], right=lS[-1]); out = lS[-1] - (Rx - lR[-1]) / Rd
            v = np.where(Rx <= lR[-1], inner, out)
            return np.where(Rx <= lR[-1] + 6 * Rd, np.exp(v), 0.0)
        Md = dep(lambda Rx, z: Sig(Rx) * np.exp(-np.abs(z) / zd) / (2 * zd))
        An = A.assemble(g, np.zeros((g.nr, g.nt)), 1.0, True).tocsc(); lu = spla.splu(An)
        c["Md"] = Md; c["v2"]["disk"] = vc2(g, lu.solve(4 * np.pi * A.G * Md.ravel()).reshape(g.nr, g.nt), R)
    return c


def subset_idx(n):
    return list(range(0, n, 15))


def run_solve(workers):
    from multiprocessing import Pool
    GALS = load_sparc(); n = len(GALS); sub = set(subset_idx(n))
    tasks = [(f, i, i in sub) for f in FOOT for i in range(n)]
    tasks.sort(key=lambda t: -len(GALS[t[1]]["R"]))                                 # long galaxies first
    t0 = time.time(); done = 0
    with Pool(workers) as pool:
        for _ in pool.imap_unordered(solve_task, tasks):
            done += 1
            if done % 10 == 0 or done == len(tasks):
                print(f"{done}/{len(tasks)} parts [{time.time() - t0:.0f} s]", flush=True)
    print("ALLDONE", flush=True)


# ------------------------------------------------------------------ known answers on the solver (KA2, KA3)
def solver_checks():
    a0c = A.a0_kpc(FOOT["canonical"])
    g = A.Grid(0.01, 3000.0, *GRID, p=2.0)
    Mp, bp = 1e9, 1.0
    rho_pl = lambda R, z: 3 * Mp / (4 * np.pi * bp ** 3) * (1 + (R * R + z * z) / bp ** 2) ** -2.5
    dep_slow = g.deposit(rho_pl); dep_fast = Dep(g)(rho_pl)
    ddep = float(np.max(np.abs(dep_fast - dep_slow)) / np.max(np.abs(dep_slow)))
    Phi, res, it = A.solve(g, dep_slow, a0c)
    r = np.array([1.0, 3.0, 10.0, 30.0]); gN = A.G * Mp * r / (r * r + bp * bp) ** 1.5
    k1 = float(np.max(np.abs(A.radial_g(g, Phi, r, g.nt // 2) / (nu(gN / a0c) * gN) - 1)))
    Mk, ak = 1e9, 2.0; hk = 0.02 * ak
    rho_kz = lambda R, z: Mk * ak / (2 * np.pi * (R * R + ak * ak) ** 1.5) * np.exp(-0.5 * (z / hk) ** 2) / (np.sqrt(2 * np.pi) * hk)
    Phi, res2, it2 = A.solve(g, g.deposit(rho_kz), a0c)
    r2 = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
    gR = A.G * Mk * r2 / (r2 * r2 + ak * ak) ** 1.5; gmag = A.G * Mk / (r2 * r2 + ak * ak)
    vex = A.midplane_vc(g, Phi, r2)
    k2 = float(np.max(np.abs(vex / np.sqrt(nu(gmag / a0c) * gR * r2) - 1)))
    return dict(KA2=k1, KA2_res=float(res), KA3=k2, KA3_res=float(res2), deposit_fast_vs_slow=ddep)


# ------------------------------------------------------------------ grade
def run_grade(mutate):
    tag = "_MUTATE" if mutate else ""
    OUT = []
    P = lambda s="": (print(s, flush=True), OUT.append(str(s)))
    GALS = load_sparc(); n = len(GALS); sub = subset_idx(n)
    P(f"QX8 SPARC on the action's exact AQUAL field{' -- MUTATE' if mutate else ''}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
    RES = dict(lane="QX8", criteria="8ad4e65ea3", mutate=mutate, footings={})
    if not mutate:
        sc = solver_checks(); RES["solver_checks"] = sc
        P(f"KA2 Plummer max rel {sc['KA2']:.2e} (line 1e-3) -> {'PASS' if sc['KA2'] <= 1e-3 else 'FAIL'}  [res {sc['KA2_res']:.1e}]")
        P(f"KA3 Kuzmin vs BM95 max rel {sc['KA3']:.4f} (line 0.02) -> {'PASS' if sc['KA3'] <= 0.02 else 'FAIL'}  [res {sc['KA3_res']:.1e}]")
        P(f"    fast deposit vs aqual.Grid.deposit: max rel {sc['deposit_fast_vs_slow']:.1e}")
    i50 = int(np.where(UPS == 0.50)[0][0]); lU = np.log(UPS); lN = np.log(NODES)
    allok = True
    for foot in FOOT:
        a0 = FOOT[foot]; F = {}
        parts = [dict(np.load(os.path.join(PARTS, foot, f"{i:03d}.npz"), allow_pickle=False)) for i in range(n)]
        law_rows, ex_rows, newt_rows, plant_rows, fix_law, fix_ex, fix_pl = [], [], [], [], [], [], []
        Tfine_all = []; percal = []
        for q, pt in zip(GALS, parts):
            lgl = np.log10(np.maximum(nu(q["GB"] / a0) * q["GB"], 1e-300))
            Tn = pt["T"]                                                              # (nodes, npts)
            Tf = np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])])  # (npts, nups)
            Tfine_all.append(Tf)
            lge = lgl + Tf
            for rows, fix, lg in ((law_rows, fix_law, lgl), (ex_rows, fix_ex, lge), (plant_rows, fix_pl, lge - 0.100)):
                rows.append(fit_one(q, lg))
                OK = q["OK"][:, i50]; r = np.log10(q["GO"]) - lg[:, i50]
                fix.append((np.sum(q["W"][OK] * r[OK]), np.sum(q["W"][OK] * r[OK] ** 2), np.sum(q["W"][OK])))
            newt_rows.append(fit_one(q, np.log10(np.maximum(q["GB"], 1e-300))))
            i_b = ex_rows[-1][2]; OK = q["OK"][:, i_b]; r = np.log10(q["GO"]) - lge[:, i_b]
            i_l = law_rows[-1][2]; OKl = q["OK"][:, i_l]; rl = np.log10(q["GO"]) - lgl[:, i_l]
            percal.append(dict(name=q["name"], mres_ex=float(np.sum(q["W"][OK] * r[OK]) / max(np.sum(q["W"][OK]), 1e-300)),
                               mres_law=float(np.sum(q["W"][OKl] * rl[OKl]) / max(np.sum(q["W"][OKl]), 1e-300)),
                               U_law=float(UPS[i_l]), U_ex=float(UPS[i_b]), SBeff=q["meta"]["SBeff"], Vflat=q["meta"]["Vflat"],
                               SB0=float(q["SBd"][0]), k4=float(pt["k4"])))
        st_law, st_ex, st_N, st_pl = pooled(law_rows), pooled(ex_rows), pooled(newt_rows), pooled(plant_rows)
        fx = lambda L: dict(mean=float(sum(a for a, _, _ in L) / sum(c for _, _, c in L)), rms=float(math.sqrt(sum(b for _, b, _ in L) / sum(c for _, _, c in L))))
        f_law, f_ex, f_pl = fx(fix_law), fx(fix_ex), fx(fix_pl)
        P(f"\n=== {foot} (a0 {a0:.4e})")
        if mutate:
            m1 = not line(st_N)
            dshift = f_pl["mean"] - f_ex["mean"]; m2 = abs(dshift - 0.100) <= 0.005 and st_pl["U_median"] > st_ex["U_median"]
            P(f"M1 mu = 1 (Newton): rms {st_N['rms']:.4f} @ U {st_N['U_median']:.2f} -> line {'PASS' if line(st_N) else 'FAIL'}; M1 {'BITES' if m1 else 'DOES NOT BITE'}")
            P(f"M2 planted T - 0.100: fixed-U mean residual shift {dshift:+.4f} (line +0.100 +- 0.005); median U {st_ex['U_median']:.2f} -> {st_pl['U_median']:.2f}; M2 {'BITES' if m2 else 'DOES NOT BITE'}")
            F.update(M1=dict(st=st_N, bites=m1), M2=dict(shift=dshift, U=(st_ex["U_median"], st_pl["U_median"]), bites=m2))
            allok &= m1 and m2
            RES["footings"][foot] = F
            continue
        # KA1
        P4R = {"canonical": (0.054087447879939264, 0.52), "alt": (0.05371798965550355, 0.44)}[foot]
        ka1 = abs(st_law["rms"] - P4R[0]) <= 1e-4 and st_law["U_median"] == P4R[1]
        P(f"KA1 algebraic mode: rms {st_law['rms']:.6f} @ {st_law['U_median']:.2f} (P4 {P4R[0]:.6f} @ {P4R[1]:.2f}) -> {'PASS' if ka1 else 'FAIL'}")
        # K4
        k4 = np.array([p["k4"] for p in percal]); k4m = float(np.nanmedian(k4)); tagged = [p["name"] for p in percal if not (p["k4"] <= 0.10)]
        P(f"K4 baryon reconstruction (weighted rms frac. diff of V_bar^2 at U 0.5): median {k4m:.4f} (line 0.05) -> {'PASS' if k4m <= 0.05 else 'FAIL'}; tagged > 10 %: {len(tagged)}")
        # K5, K6, K7
        k5 = []; k6 = []
        for i in sub:
            pt = parts[i]
            k5.append(float(np.max(np.abs(pt["T_ladder"] - pt["T"]))))
            Th = pt["T_held"]; Tn = pt["T"]
            for h, U in enumerate(HELD):
                Ti = np.array([np.interp(np.log(U), lN, Tn[:, j]) for j in range(Tn.shape[1])])
                k6.append(float(np.max(np.abs(Ti - Th[h]))))
        k5m, k6m = max(k5), max(k6)
        P(f"K5 ladder 160x48 vs 240x72 on {len(sub)} galaxies: max |dT| {k5m:.4f} dex (line 0.005) -> {'PASS' if k5m <= 0.005 else 'FAIL'}")
        P(f"K6 U interpolation (held-out 0.50, 0.72): max |dT| {k6m:.4f} dex (line 0.005) -> {'PASS' if k6m <= 0.005 else 'FAIL'}")
        resall = np.concatenate([p["res"] for p in parts]); ncap = int(np.sum(resall > 1e-7)); capg = [GALS[i]["name"] for i, p in enumerate(parts) if np.any(p["res"] > 1e-7)]
        cap_in_sub = [GALS[i]["name"] for i in sub if np.any(parts[i]["res"] > 1e-7)]
        P(f"K7 solves above residual 1e-7: {ncap} of {len(resall)} (galaxies: {capg[:12]}{' ...' if len(capg) > 12 else ''}); max residual {resall.max():.1e}")
        nneg = int(sum(int(p["nneg"]) for p in parts)); P(f"    points with g_N,solver <= 0 or g_exact <= 0 (T = 0): {nneg}")
        # the grade
        lab_ok = ka1 and k4m <= 0.05 and k5m <= 0.005 and k6m <= 0.005
        P(f"LAW   : rms {st_law['rms']:.4f} @ median U {st_law['U_median']:.2f} -> line {'PASS' if line(st_law) else 'FAIL'}")
        P(f"EXACT : rms {st_ex['rms']:.4f} @ median U {st_ex['U_median']:.2f} -> line {'PASS' if line(st_ex) else 'FAIL'}")
        dU = np.array([p["U_ex"] - p["U_law"] for p in percal])
        P(f"  per-galaxy refit U shift (exact - law): median {np.median(dU):+.3f}, mean {dU.mean():+.3f}, 90th pct {np.percentile(dU, 90):+.3f}")
        P(f"  fixed U = 0.50: law rms {f_law['rms']:.4f} mean {f_law['mean']:+.4f}; exact rms {f_ex['rms']:.4f} mean {f_ex['mean']:+.4f}")
        # without tagged
        keep = [k for k, p in enumerate(percal) if p["k4"] <= 0.10]
        st_ex_k = pooled([ex_rows[k] for k in keep]); st_law_k = pooled([law_rows[k] for k in keep])
        P(f"  without K4-tagged ({len(keep)} galaxies): law {st_law_k['rms']:.4f} @ {st_law_k['U_median']:.2f}, exact {st_ex_k['rms']:.4f} @ {st_ex_k['U_median']:.2f} -> line {'PASS' if line(st_ex_k) else 'FAIL'}")
        # T statistics
        Tall, ybar = [], []
        for q, Tf in zip(GALS, Tfine_all):
            OK = q["OK"][:, i50]; Tall.append(Tf[OK, i50]); ybar.append(q["GB"][OK, i50] / a0)
        Tall = np.concatenate(Tall); ybar = np.concatenate(ybar)
        bins = [0.01, 0.1, 0.3, 1.0, 3.0, 30.0, 1e9]; tb = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            s = (ybar >= lo) & (ybar < hi)
            if s.any():
                tb.append(dict(lo=lo, hi=hi, n=int(s.sum()), median=float(np.median(Tall[s])), p10=float(np.percentile(Tall[s], 10))))
                P(f"  T at U 0.50, g_bar/a0 [{lo:g}, {hi:g}): n {s.sum():4d} median {np.median(Tall[s]):+.4f} 10th pct {np.percentile(Tall[s], 10):+.4f}")
        P(f"  T overall: median {np.median(Tall):+.4f}, min {Tall.min():+.4f}")
        sbc = []
        for lo, hi in ((0, 50), (50, 200), (200, 1000), (1000, 1e9)):
            s = [k for k, p in enumerate(percal) if lo <= p["SB0"] < hi]
            if s:
                mins = [float(np.min(Tfine_all[k][GALS[k]["OK"][:, i50], i50])) if GALS[k]["OK"][:, i50].any() else 0.0 for k in s]
                dUs = [percal[k]["U_ex"] - percal[k]["U_law"] for k in s]
                sbc.append(dict(lo=lo, hi=hi, n=len(s), median_minT=float(np.median(mins)), median_dU=float(np.median(dUs))))
                P(f"  SBdisk(R_1) [{lo:g}, {hi:g}) L/pc^2: {len(s):3d} galaxies, median of per-galaxy min T {np.median(mins):+.4f}, median U shift {np.median(dUs):+.3f}")
        # SB trend at fixed speed
        rng = np.random.default_rng(20261106)
        tr = {}
        for key in ("mres_law", "mres_ex"):
            rows = [p for p in percal if p["Vflat"] > 0 and p["SBeff"] > 0]
            X = np.column_stack([np.ones(len(rows)), np.log10([p["SBeff"] for p in rows]), np.log10([p["Vflat"] for p in rows])])
            y = np.array([p[key] for p in rows])
            b = np.linalg.lstsq(X, y, rcond=None)[0]
            bs = []
            for _ in range(2000):
                ii = rng.integers(0, len(rows), len(rows)); bs.append(np.linalg.lstsq(X[ii], y[ii], rcond=None)[0][1])
            sd = float(np.std(bs)); tr[key] = dict(slope_SB=float(b[1]), sigma=sd, slope_V=float(b[2]), n=len(rows), no_trend=bool(abs(b[1]) < 2 * sd))
            P(f"  SB trend at fixed Vflat ({'law' if key == 'mres_law' else 'exact'}): slope d(res)/dlog SBeff {b[1]:+.4f} +- {sd:.4f} ({abs(b[1]) / sd:.1f} sigma; n {len(rows)}) -> {'no trend' if abs(b[1]) < 2 * sd else 'TREND'}; slope vs log Vflat {b[2]:+.4f}")
        # sensitivity
        if foot == "canonical":
            dg = [float(np.median(np.abs(parts[i]["T_zg2"] - np.array([np.interp(np.log(0.60), lN, parts[i]["T"][:, j]) for j in range(parts[i]["T"].shape[1])])))) for i in sub]
            dd = [float(np.median(np.abs(parts[i]["T_zd2"] - np.array([np.interp(np.log(0.60), lN, parts[i]["T"][:, j]) for j in range(parts[i]["T"].shape[1])])))) for i in sub]
            mg = [float(np.max(np.abs(parts[i]["T_zg2"] - parts[i]["T"][2]))) for i in sub]
            md = [float(np.max(np.abs(parts[i]["T_zd2"] - parts[i]["T"][2]))) for i in sub]
            P(f"  sensitivity (reported, U 0.60, {len(sub)} galaxies): z_g x 2 median |dT| {np.median(dg):.4f} max {max(mg):.4f}; z_d x 2 median |dT| {np.median(dd):.4f} max {max(md):.4f}")
            F["sensitivity"] = dict(zg2_median=float(np.median(dg)), zg2_max=max(mg), zd2_median=float(np.median(dd)), zd2_max=max(md))
        if not lab_ok:
            label = "NO VERDICT"
        elif line(st_ex):
            label = "EXACT FIELD PASSES" + (" (U refits upward)" if st_ex["U_median"] > st_law["U_median"] else "")
        else:
            label = "EXACT FIELD FAILS"
        P(f"LABEL {foot}: {label}")
        F.update(KA1=dict(ok=ka1, rms=st_law["rms"], U=st_law["U_median"]), K4=dict(median=k4m, tagged=tagged), K5=k5m, K6=k6m,
                 K7=dict(n_above=ncap, galaxies=capg, in_subset=cap_in_sub, max=float(resall.max())), nneg=nneg,
                 law=st_law, exact=st_ex, newton=st_N, fixedU50=dict(law=f_law, exact=f_ex), without_tagged=dict(law=st_law_k, exact=st_ex_k, n=len(keep)),
                 dU=dict(median=float(np.median(dU)), mean=float(dU.mean())), T_bins=tb, T_overall=dict(median=float(np.median(Tall)), min=float(Tall.min())),
                 SB_classes=sbc, SB_trend=tr, label=label, per_galaxy=percal)
        RES["footings"][foot] = F
    if mutate:
        P(f"\nMUTATE overall: {'BOTH BITE' if allok else 'A CONTROL DOES NOT BITE'}")
    open(os.path.join(HERE, f"qx8{tag}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"qx8{tag}.json"), "w"), indent=1, default=float)
    return 0 if (allok if mutate else True) else 1


if __name__ == "__main__":
    if sys.argv[1] == "solve":
        w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
        run_solve(w)
    elif sys.argv[1] == "grade":
        sys.exit(run_grade("--mutate" in sys.argv))
