#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG193_b_curves -- the 2D profile curves chi2(x = log10 a0, t = distance pull) with Upsilon_disk, Upsilon_bul, inclination
profiled (own batch Levenberg-Marquardt), for the clean SPARC sample, plus checks C1-C4.
MUTATE modes (env MUTATE=k; outputs named ..._MUTATE<k>.*; exit 1 = the control BITES, 3 = it did NOT, 2 = own checks failed):
  1  inject beta = 0.30 at the point level (V -> V sqrt(nu(y')/nu(y)), y = g_bar,fid/a0,ref, y' = y/(1 + 0.30 z_i(0)), a0,ref = 1.2e-10)
  3  drop the profiling: Upsilon = 0.5/0.7, i = catalogue, D = D_SPARC (t frozen at 0)
  5  kernel swap: my own exponential-RAR kernel instead of nu_mono
Rerun: ZF_REPO=<repo> python3 CFG193_b_curves.py [MUTATE=k]  (needs CFG193_a_velocities first; < 10 min)."""
import os, sys, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG193_common import *

MODE = int(os.environ.get("MUTATE", "0"))
SUF = ("" if MODE == 0 else "_MUTATE%d" % MODE) + ("_" + VARIANT if VARIANT else "")
T = Tee(os.path.join(HERE, "CFG193_b_curves%s.out" % SUF))
P = T.p
P("CFG193_b_curves  mode MUTATE=%d  (repo = <repo>)" % MODE)
gal = load_sparc()
clean = clean_sample(gal, "U1")
ut = np.load(os.path.join(HERE, "CFG193_utable.npz"))
uname = list(ut["names"])
u0 = dict(zip(uname, ut["u"]))
if MODE in (1, 3, 5):
    clean = [g for g in clean if g["name"] in uname and g["meta"]["fD"] in (2, 3, 4, 5)]
kernel = "RAR" if MODE == 5 else "mono"
nu = get_kernel(kernel)
P("galaxies:", len(clean), " kernel:", kernel)
GL = [Gal(g) for g in clean]
RAW = {g["name"]: g for g in clean}

A0_REF = 1.2e-10


def inject(G, g):
    """MU1: point-level beta = 0.30 injection with the frozen recipe (my own z)"""
    z0 = (u0[G.name] / W_REF) ** 2
    gb = (G.Sg + UPS_D0 * G.Sd + UPS_B0 * G.Sb) / G.R * CONV
    gb = np.maximum(gb, 1e-16)
    y = gb / A0_REF
    yp = y / (1.0 + 0.30 * z0)
    return G.V * np.sqrt(nu(yp) / nu(y))


def work(i):
    G = GL[i]
    if MODE == 3:
        C0 = profile_grid(G, nu, xg=XG, tg=np.array([0.0]), nstart=1, free=(False, False, False), prior=False)[0]
        C = np.tile(C0[None, :], (len(TG), 1)) + 1e4 * (TG ** 2)[:, None]
        return i, C, None
    Vo = inject(G, RAW[G.name]) if MODE == 1 else None
    C, allc = profile_grid(G, nu, Vobs=Vo, nstart=3, return_all=True)
    return i, C, allc


t0 = time.time()
with mp.get_context("fork").Pool(min(14, os.cpu_count() or 4)) as pool:
    out = pool.map(work, range(len(GL)), chunksize=1)
out.sort(key=lambda o: o[0])
C = np.array([o[1] for o in out])
P("profiled %d galaxies x %d x %d cells in %.0f s" % (len(GL), len(TG), len(XG), time.time() - t0))
meta = dict(N=[G.N for G in GL], fD=[G.fD for G in GL], D=[G.D for G in GL], eD=[G.eD for G in GL])
np.savez(os.path.join(HERE, "CFG193_curves%s.npz" % SUF), names=np.array([G.name for G in GL]), C=C, N=np.array(meta["N"]), fD=np.array(meta["fD"]),
         D=np.array(meta["D"]), eD=np.array(meta["eD"]))

# ---------------- checks
feas = np.array([(G.D + G.eD * TG) >= 0.3 * G.D for G in GL])
fin = np.isfinite(C)
T.check("C2 zero non-finite cells among feasible cells", int(np.sum(feas[:, :, None] & ~fin)) == 0, "count=%d" % int(np.sum(feas[:, :, None] & ~fin)))
if MODE != 3:
    # C1: the three starts agree within dchi2 <= 25 of each galaxy's minimum
    worst, nbad, ncell = 0.0, 0, 0
    for i, o in enumerate(out):
        allc = o[2]
        cm = np.nanmin(allc, axis=0)
        gmin = np.nanmin(cm)
        sel = np.isfinite(cm) & (cm - gmin <= 25.0)
        for k in range(allc.shape[0]):
            d = (allc[k] - cm)[sel]
            worst = max(worst, float(np.max(d)))
            nbad += int(np.sum(d > 0.01)); ncell += int(d.size)
    T.check("C1 three starts (prior centre and two perturbed) agree to 0.01 within dchi2<=25 of the minimum", worst <= 0.01,
            "worst |dchi2| = %.4f; cells above 0.01: %d of %d" % (worst, nbad, ncell))

    # C3: spline vs direct profile at off-grid t, near each minimum
    rng = np.random.RandomState(193501)
    errs = []
    Cf = None
    idxs = rng.choice(len(GL), size=min(12, len(GL)), replace=False)
    for i in idxs:
        G = GL[i]
        cm = C[i] + (TG ** 2)[:, None]
        jt, jx = np.unravel_index(np.nanargmin(cm), cm.shape)
        for _ in range(3):
            tt = float(np.clip(TG[jt] + rng.uniform(-1.0, 1.0), -3.9, 3.9))
            if G.D + G.eD * tt < 0.3 * G.D:
                continue
            xj = int(np.clip(jx + rng.randint(-8, 9), 0, len(XG) - 1))
            Vo_ = inject(G, RAW[G.name]) if MODE == 1 else None
            Cd = profile_grid(G, nu, xg=XG[xj:xj + 1], tg=np.array([tt]), nstart=2, Vobs=Vo_)[0, 0]
            sp = spline_t(C[i] + (TG ** 2)[:, None])
            k = int(np.argmin(np.abs(TF - tt)))
            # spline on the 0.05 fine grid: evaluate at the nearest fine t; compare with a direct profile at that same t
            tt_f = float(TF[k])
            Cd = profile_grid(G, nu, xg=XG[xj:xj + 1], tg=np.array([tt_f]), nstart=2, Vobs=Vo_)[0, 0] + tt_f ** 2
            near = (np.nanmin(cm) + 25.0) >= Cd
            if near:
                errs.append(abs(sp[k, xj] - Cd))
    T.check("C3 spline in t vs direct profile within dchi2<=25 of the minimum <= 0.1", (max(errs) if errs else 0.0) <= 0.1,
            "n=%d, max |d| = %.4f, median %.4f" % (len(errs), max(errs) if errs else float("nan"), float(np.median(errs)) if errs else float("nan")))

    # C4: min_t of the 2D curve (spline, fine t) vs an independent 1D distance-profiled curve (scipy least_squares, t a 4th parameter)
    from scipy.optimize import least_squares
    d4 = []
    for i in idxs[:6]:
        G = GL[i]
        Vo4 = inject(G, RAW[G.name]) if MODE == 1 else None
        Ct = spline_t(C[i] + (TG ** 2)[:, None])
        prof = np.min(Ct, axis=0)
        jm = int(np.argmin(prof))
        for xj in (jm - 6, jm, jm + 6):
            if xj < 0 or xj >= len(XG):
                continue
            a0 = 10.0 ** XG[xj]
            def rf(p):
                th = np.array([[p[0], p[1], p[2]]])
                sc = np.array([math.sqrt(max(G.D + G.eD * p[3], 0.31 * G.D) / G.D)])
                r = resid(G, th, np.array([a0]), sc, nu, True, Vo4)[0]
                return np.concatenate([r, [p[3]]])
            best = None
            for t0_ in (-1.0, 0.0, 1.0):
                sol = least_squares(rf, [math.log10(UPS_D0), math.log10(UPS_B0), G.inc, t0_], bounds=([-1.6, -1.6, 5, -4.0], [0.8, 0.8, 89, 4.0]))
                if best is None or sol.cost < best:
                    best = sol.cost
            d4.append(abs(2 * best - prof[xj]))
    T.check("C4 min_t of the 2D curve reproduces a direct 1D distance-profiled curve (<= 0.1)", (max(d4) if d4 else 0.0) <= 0.1,
            "n=%d, max |d| = %.4f, median %.4f" % (len(d4), max(d4) if d4 else float("nan"), float(np.median(d4)) if d4 else float("nan")))

# widths summary
cv = Curves([G.name for G in GL], C, meta=meta)
sig, xhat, p = cv.sigma_i()
P("median Birge s = %.2f;  median sigma_i (distance-profiled, Birge-scaled) = %.3f dex" % (float(np.median(cv.s)), float(np.median(sig))))
res = dict(mode=MODE, n=len(GL), median_s=float(np.median(cv.s)), median_sigma_i=float(np.median(sig)), checks=[(n_, ok, ld) for n_, ok, ld in T.checks])
jdump(res, os.path.join(HERE, "CFG193_b_curves%s_results.json" % SUF))

bad = T.failed_load()
P("verdict: %d/%d checks pass; load-bearing failures: %d" % (sum(1 for c in T.checks if c[1]), len(T.checks), len(bad)))
if MODE != 0:
    P("(MUTATE=%d curves built; the biting condition is evaluated by CFG193_c_fit_power.py with the same MUTATE)" % MODE)
sys.exit(2 if bad else 0)
