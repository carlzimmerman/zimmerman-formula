#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG66 -- DO THE TWO CFG51 ULTRA-FAINT OFFSETS SURVIVE A TWO-COMPONENT FIT (BOOTES I) AND A VELOCITY-GRADIENT FIT (TUCANA II)?

FROZEN QUESTIONS (verbatim).
'CFG51 found that after per-star binary cleaning the bare isolated law under-predicts the ultra-faint dispersions of Bootes I (+0.219 dex, 2.46 sigma) and Tucana II
(+0.465 dex, 3.63 sigma), and flagged two systematics: (Q1) Bootes I has a cold (~2.4 km/s) and a hot (~4.6 km/s) kinematic component in the literature (Koposov+2011)
and CFG51's velocity window keeps both; the cold component alone would give about +0.007 dex. (Q2) Tucana II is tidally disturbed in the literature (an extended halo
and a velocity gradient), and a gradient inflates a dispersion. Do the two offsets survive (a) a declared two-Gaussian mixture fit for Bootes I and (b) a declared
linear-velocity-gradient fit for Tucana II?'

DECLARED BEFORE THE FIRST RUN (nothing tuned afterwards; any result is valid; kappa = 1/2 is FITTED; nothing here closes or proves the theory).

DATA / SAMPLE.  CFG51's reduction, imported READ-ONLY (campaign_fresh_gravity/CFG51_walker_multiepoch/reduce_walker.py: parse, build_stars, membership; the repo
file is not edited and no bytecode is written).  Same membership (logg<4, Gaia PM, parallax, +-4 sigma_seed window, one recentring), same per-star binary cleaning
(stars with >= 2 quality epochs and epoch-chi2 p < 0.01 removed), same per-star inputs: the inverse-variance mean velocity v_i over quality epochs and its error e_i.
The only addition: field positions RA/Dec (ReadMe bytes 234-248, 250-264) are parsed for the same rows (COLS is extended in memory), averaged over a star's quality epochs.

Q1  BOOTES I.  Binary-cleaned members.  Likelihood: p(v_i) = (1-f) N(v_i; mu, s_c^2+e_i^2) + f N(v_i; mu, s_h^2+e_i^2), COMMON mean mu, s_c <= s_h, f = f_hot in [0,1].
    Maximum likelihood by multi-start L-BFGS-B (4 free parameters; s_h = s_c + d with d >= 0).  Profile-likelihood 1-sigma intervals (Delta(-2lnL) = 1, other
    parameters re-optimised at each value, linear interpolation on a fixed grid) for s_c, s_h, f, and the total sigma_tot = sqrt((1-f) s_c^2 + f s_h^2) (profiled by
    solving f from sigma_tot, s_c, s_h).  An interval end that the profile never reaches inside the grid is reported as open (>= / <=).  Improvement over the single
    Gaussian: LR = -2lnL_single - (-2lnL_mix); NOT a formal chi2 significance (boundary, unidentified parameters); a parametric-bootstrap calibration of the LR (fixed
    seed, 200 single-Gaussian datasets with the real errors and the fitted single-Gaussian mean and sigma; fit the mixture with a reduced multi-start) is reported
    as a diagnostic only.  'The galaxy' component is the open question, so BOTH offsets are reported: cold-only log10(s_c/sigma_law), total log10(sigma_tot/sigma_law).
Q2  TUCANA II.  Binary-cleaned members.  Model: single Gaussian dispersion sigma with mean(x,y) = v0 + g_x xi + g_y eta.  Coordinates: gnomonic tangent-plane
    (xi east, eta north, degrees) about the LVD catalogue centre (RA 342.9796, Dec -58.5689); the gradient is reported in km/s/deg and km/s per half-light radius
    (LVD rhalf in arcmin, 12.89'), amplitude |g| = sqrt(gx^2+gy^2) and direction (position angle of increasing velocity, degrees east of north).  At each sigma the
    linear parameters are solved by weighted least squares (weights 1/(sigma^2+e_i^2)); sigma profiled on a fine grid.  Gradient significance = LR against g = 0 (2 dof;
    chi2 tail quoted with the caveat of 12 stars).  Dispersion with gradient removed: sigma_g, profile 1-sigma interval.  Diagnostic (reported, not load-bearing): a
    permutation null (2000 shuffles of positions among stars, fixed seed) for the LR and for sigma_g -- how much a gradient fit lowers sigma by chance with N ~ 12 stars.
LAW PREDICTION AND ERROR MODEL: exactly CFG51's.  FG001 slices exec'd read-only from CFG7_hierarchy_fg001.py (a_int, A0H, UPS_V=2, G, Msun), sigma_law^2 = g(r) r/3 at
    r = (4/3) r_half, half the baryons enclosed, stars only, both footings; error on the offset = sqrt(e_stat^2 + floor^2) with e_stat = 0.5 (log10(1+p/s) +
    |log10 max(1-m/s,1e-3)|) from the asymmetric 1-sigma interval (here the profile-likelihood one) and floor = half the range of the offset over Upsilon_V in {1,2,4}
    and the pure deep-MOND estimate.

PRE-DECLARED ACCEPTANCE (gates; ALL on the law of CFG51, both footings)
  C1 CONTROL  the single-Gaussian, gradient-free fits reproduce CFG51's cleaned dispersions, Bootes I 3.911 and Tucana II 4.064 km/s, to 5e-3 (and member counts 55/14,
              cleaned 53/12 as CFG51 reports 2 removed each).
  S1 [HEADLINE, MUTATE must fail]  Bootes I offset SURVIVES: the TOTAL-MIXTURE reading log10(sigma_tot/sigma_law) is positive at > 2 sigma on BOTH footings.
  S2 [HEADLINE, MUTATE must fail]  Tucana II offset SURVIVES: the gradient-removed dispersion offset is positive at > 2 sigma on BOTH footings.
  R1 (reported, separate)  whether the Bootes I COLD-ONLY reading survives (same > 2 sigma both-footing gate).
  R2 (reported)  every fitted number, LR statistics, diagnostics.
  READING (declared): S1 and S2 PASS -> the CFG51 offsets are not removed by these two systematics as modelled (two objects, a declared model each; not a population
      result).  A FAIL of either says that system's offset is not established once the systematic is modelled; it does not say the law is right or wrong.
MUTATE=1: every member velocity x 0.5 (errors unchanged) entering the Q1/Q2 fits -- S1 and S2 must FAIL (rc = 1).  C1 is evaluated on the unscaled data.
Run: python3 CFG66_bootes_tucana_systematics.py    (MUTATE=1 for the control; writes .out/.json next to itself)
"""
import os, sys, math, io, contextlib, csv, json, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import minimize, brentq, minimize_scalar
from scipy.stats import chi2 as chi2dist

MUTATE = os.environ.get("MUTATE", "0") == "1"
SCR = os.path.dirname(os.path.abspath(__file__))
SLUG = "CFG66_bootes_tucana_systematics" + ("_MUTATE" if MUTATE else "")
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
LINES, CHECKS, NUMS = [], [], {}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LINES.append(s)


def check(name, detail, ok, lb=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=lb))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}\n         {detail}")


P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every fitted member velocity x 0.5 -- S1 and S2 must FAIL ***")
SF = 0.5 if MUTATE else 1.0

# ---------------------------------------------------------------------------------------- CFG51 reduction (read-only import)
sys.path.insert(0, os.path.join(CFG, "CFG51_walker_multiepoch"))
import reduce_walker as RW
RW.COLS = dict(RW.COLS); RW.COLS["RA"] = (234, 248, float); RW.COLS["DE"] = (250, 264, float)

# ---------------------------------------------------------------------------------------- FG001 law (as CFG51)
sys.path.insert(0, CFG)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL
FGP = os.path.join(CFG, "CFG7_hierarchy_fg001.py")
ns = {"np": np, "math": math, "os": os, "csv": csv, "C": C, "HL": HL}
ns = C.C4.exec_slices(FGP, [("G, kpc, Msun, A0H = HL.G", "# ================================================================================================ K1 h43"),
                            ("MW_MB, M31_MB, UPS_V = 6.0e10", "REF43 = {")], ns=ns, name="fg001_slices")[0]
A0H, UPS_V, a_int, G, Msun, fnum = ns["A0H"], ns["UPS_V"], ns["a_int"], ns["G"], ns["Msun"], ns["fnum"]
LVD = {r["key"]: r for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_mw.csv")))}
FOOTS = ("canonical", "alt")


def galinfo(name):
    r = [r for r in LVD.values() if r["name"] == name][0]
    MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); MHI = fnum(r["mass_HI"])
    return dict(name=name, MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** MHI if MHI is not None else 0.0),
                ra=float(r["ra"]), dec=float(r["dec"]), rhalf_arcmin=float(r["rhalf"]))


def spred(g, foot, ups=None, deep=False):
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * g["LV"]; Mb = Ms + 1.33 * g["MHI"]
    if deep:
        return (4.0 / 81.0 * G * Mb * Msun * a0) ** 0.25 / 1e3
    rh = (4.0 / 3.0) * g["rh"] * 3.0857e16
    gg = a_int(G * 0.5 * Mb * Msun / rh ** 2, 0.0, a0)
    return math.sqrt(gg * rh / 3.0) / 1e3


def offset(g, s, foot, **kw):
    return math.log10(s / spred(g, foot, **kw)) if s > 0 else -math.inf


def score(g, s, plus, minus, foot):
    """CFG51's error model: asymmetric 1-sigma interval -> dex, plus the systematic floor in quadrature."""
    if s <= 0:
        return dict(off=-math.inf, tot=float("nan"), z=-math.inf, e=float("nan"), fl=float("nan"))
    e = 0.5 * (math.log10(1 + plus / s) + abs(math.log10(max(1 - minus / s, 1e-3))))
    ofs = [offset(g, s, foot, ups=u) for u in (1.0, 2.0, 4.0)] + [offset(g, s, foot, deep=True)]
    fl = 0.5 * (max(ofs) - min(ofs))
    tot = math.sqrt(e ** 2 + fl ** 2); o = offset(g, s, foot)
    return dict(off=o, tot=tot, z=o / tot, e=e, fl=fl)


# ---------------------------------------------------------------------------------------- CFG51 sample reproduction
rows = []
for f in ("hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"):
    rows += RW.parse(os.path.join(RW.IN, f))
stars_all = RW.build_stars(rows)
pos = {}
for r in rows:
    if r["Gaia"] and r["Goodobs"] > 0 and r["RRL"] == 0 and r["AGN"] == 0 and r["eVlos"] > 0 and np.isfinite(r["Vlos"]):
        pos.setdefault((r["Target"], r["Gaia"]), []).append((r["RA"], r["DE"]))
lvd_rw = RW.load_lvd()


def sample(target):
    stars = {k: s for k, s in stars_all.items() if s["target"] == target}
    mem, nvrej, vs, sw = RW.membership(stars, lvd_rw[target.lower()])
    clean = [s for s in mem if not (s["n"] >= 2 and s["p"] < 0.01)]
    for s in clean:
        p = np.array(pos[(s["target"], s["gaia"])]); s["ra"], s["dec"] = p[:, 0].mean(), p[:, 1].mean()
    return mem, clean, vs


mem_b, cln_b, vs_b = sample("Bootes_1")
mem_t, cln_t, vs_t = sample("Tucana_2")
P(f"\n  samples: Bootes I members {len(mem_b)}, cleaned {len(cln_b)} (v_c {vs_b:.1f}); Tucana II members {len(mem_t)}, cleaned {len(cln_t)} (v_c {vs_t:.1f})")


# ---------------------------------------------------------------------------------------- Q1 mixture machinery
def m2ll_mix(mu, sc, sh, f, v, e):
    vc, vh = sc * sc + e * e, sh * sh + e * e
    d = v - mu
    a = (1 - f) * np.exp(-0.5 * d * d / vc) / np.sqrt(2 * np.pi * vc) + f * np.exp(-0.5 * d * d / vh) / np.sqrt(2 * np.pi * vh)
    return -2.0 * np.sum(np.log(np.maximum(a, 1e-300)))


def m2ll_single(v, e, s):
    w = 1.0 / (s * s + e * e); mu = np.sum(w * v) / np.sum(w)
    return np.sum(np.log(1 / w) + w * (v - mu) ** 2) + len(v) * math.log(2 * math.pi), mu   # + N ln(2 pi): same normalisation as m2ll_mix


def fit_single(v, e):
    return RW.mle_sigma(v, e)


def starts(v, nst):
    vm = float(np.mean(v)); out = []
    for sc in (0.3, 1.0, 2.0, 3.0):
        for dd in (0.5, 2.0, 5.0, 10.0):
            for f in (0.1, 0.3, 0.5, 0.8):
                out.append((vm, sc, dd, f))
    rng = np.random.default_rng(1)
    if nst < len(out):
        out = [out[i] for i in rng.choice(len(out), nst, replace=False)]
    return out


def opt_mix(v, e, fixed=None, nst=64, extra=None):
    """minimise -2lnL over (mu, sc, d, f), sh = sc + d.  fixed: dict name->value among sc, sh, f, stot (profile constraint)."""
    fixed = fixed or {}
    best = (np.inf, None)
    vm = float(np.mean(v))

    def unpack(x):
        mu, sc, d, f = x
        return mu, sc, d, f

    for st in starts(v, nst) + ([extra] if extra is not None else []):
        mu0, sc0, d0, f0 = st
        if "sc" in fixed: sc0 = fixed["sc"]
        if "f" in fixed: f0 = fixed["f"]
        if "sh" in fixed: d0 = max(fixed["sh"] - sc0, 0.0)
        if "stot" in fixed:
            S = fixed["stot"]; sc0 = min(sc0, S); d0 = max(d0, 0.1)
        # free variable vector by case
        if "sc" in fixed:
            fun = lambda y: m2ll_mix(y[0], fixed["sc"], fixed["sc"] + y[1], y[2], v, e)
            x0 = [mu0, d0, f0]; bnd = [(vm - 30, vm + 30), (0, 60), (0, 1)]
            r = minimize(fun, x0, method="L-BFGS-B", bounds=bnd)
            val, par = r.fun, (r.x[0], fixed["sc"], fixed["sc"] + r.x[1], r.x[2])
        elif "f" in fixed:
            fun = lambda y: m2ll_mix(y[0], y[1], y[1] + y[2], fixed["f"], v, e)
            x0 = [mu0, sc0, d0]; bnd = [(vm - 30, vm + 30), (0, 30), (0, 60)]
            r = minimize(fun, x0, method="L-BFGS-B", bounds=bnd)
            val, par = r.fun, (r.x[0], r.x[1], r.x[1] + r.x[2], fixed["f"])
        elif "sh" in fixed:
            sh = fixed["sh"]
            fun = lambda y: m2ll_mix(y[0], y[1], sh, y[2], v, e)
            x0 = [mu0, min(sc0, sh), f0]; bnd = [(vm - 30, vm + 30), (0, sh), (0, 1)]
            r = minimize(fun, x0, method="L-BFGS-B", bounds=bnd)
            val, par = r.fun, (r.x[0], r.x[1], sh, r.x[2])
        elif "stot" in fixed:
            S = fixed["stot"]

            def fun(y):
                mu, sc, sh = y
                if sh * sh - sc * sc < 1e-12:
                    return 1e12
                f = (S * S - sc * sc) / (sh * sh - sc * sc)
                if f < 0 or f > 1:
                    return 1e12
                return m2ll_mix(mu, sc, sh, f, v, e)
            # feasible starts: sc in [0,S], sh in [S, .]
            best_l = (np.inf, None)
            for sc_ in (0.0, 0.3 * S, 0.7 * S, 0.95 * S):
                for sh_ in (1.05 * S, 1.5 * S, 2.5 * S, 5 * S):
                    r = minimize(fun, [mu0, sc_, sh_], method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-8, maxiter=4000))
                    if r.fun < best_l[0]:
                        best_l = (r.fun, r.x)
            mu, sc, sh = best_l[1]
            f = (S * S - sc * sc) / (sh * sh - sc * sc) if sh * sh - sc * sc > 1e-12 else 0.0
            val, par = best_l[0], (mu, sc, sh, f)
            if val < best[0]:
                best = (val, par)
            break                                                        # the stot case does its own multi-start
        else:
            fun = lambda y: m2ll_mix(y[0], y[1], y[1] + y[2], y[3], v, e)
            x0 = [mu0, sc0, d0, f0]; bnd = [(vm - 30, vm + 30), (0, 30), (0, 60), (0, 1)]
            r = minimize(fun, x0, method="L-BFGS-B", bounds=bnd)
            val, par = r.fun, (r.x[0], r.x[1], r.x[1] + r.x[2], r.x[3])
        if val < best[0]:
            best = (val, par)
    return best


def profile_interval(v, e, key, best, grid, nst=24, tolerance=1.0):
    """profile -2lnL over grid values of `key`; return (lo, hi, lo_open, hi_open, curve)."""
    ref = best[0]
    x0 = best[1]
    est = dict(sc=x0[1], sh=x0[2], f=x0[3], stot=math.sqrt((1 - x0[3]) * x0[1] ** 2 + x0[3] * x0[2] ** 2))[key]
    curve = []
    for gv in grid:
        val, _ = opt_mix(v, e, fixed={key: gv}, nst=nst, extra=(x0[0], x0[1], max(x0[2] - x0[1], 0.0), x0[3]))
        curve.append(val)
    curve = np.array(curve) - min(ref, np.min(curve))
    grid = np.asarray(grid)
    # walk outward from the estimate
    def crossing(direction):
        idx = np.argmin(np.abs(grid - est))
        rng = range(idx, len(grid)) if direction > 0 else range(idx, -1, -1)
        prev = None
        for i in rng:
            if curve[i] >= tolerance:
                if prev is None:
                    return grid[i], False
                j = prev
                return grid[j] + (grid[i] - grid[j]) * (tolerance - curve[j]) / (curve[i] - curve[j]), False
            prev = i
        return grid[-1] if direction > 0 else grid[0], True
    lo, lo_open = crossing(-1); hi, hi_open = crossing(+1)
    return est, lo, hi, lo_open, hi_open, curve


# ---------------------------------------------------------------------------------------- Q2 gradient machinery
def tangent(ra, dec, ra0, dec0):
    a, d, a0, d0 = map(np.radians, (ra, dec, ra0, dec0))
    cosc = np.sin(d0) * np.sin(d) + np.cos(d0) * np.cos(d) * np.cos(a - a0)
    xi = np.cos(d) * np.sin(a - a0) / cosc
    eta = (np.cos(d0) * np.sin(d) - np.sin(d0) * np.cos(d) * np.cos(a - a0)) / cosc
    return np.degrees(xi), np.degrees(eta)


def m2ll_grad(v, e, X, s):
    w = 1.0 / (s * s + e * e)
    A = X.T @ (w[:, None] * X); b = X.T @ (w * v)
    beta = np.linalg.solve(A, b)
    r = v - X @ beta
    return np.sum(np.log(1 / w) + w * r * r), beta, np.linalg.inv(A)


def fit_grad(v, e, X):
    """returns dict sigma (MLE, 0 if < 1e-3), 1-sigma interval, beta, cov, nll."""
    f = lambda s: m2ll_grad(v, e, X, s)[0]
    top = max(3 * np.std(v), 5 * np.max(e), 1.0) * 3
    grid = np.linspace(0, top, 800)
    vals = np.array([f(s) for s in grid])
    i = int(np.argmin(vals))
    if i == 0:
        r = minimize_scalar(f, bounds=(0, grid[1]), method="bounded"); s0 = r.x if r.fun < vals[0] else 0.0
    else:
        r = minimize_scalar(f, bounds=(grid[i - 1], grid[min(i + 1, len(grid) - 1)]), method="bounded"); s0 = r.x if r.fun <= vals[i] else grid[i]
    if s0 < 1e-3: s0 = 0.0
    fmin = f(s0)
    g = lambda s, d: f(s) - fmin - d
    def upper(d):
        hi = top
        while g(hi, d) < 0:
            hi *= 2
            if hi > 1e6: return float("nan")
        return brentq(lambda x: g(x, d), s0, hi) if g(s0, d) < 0 else s0
    up = upper(1.0); ul95 = upper(2.706)
    lo = brentq(lambda x: g(x, 1.0), 0.0, s0) if (s0 > 0 and g(0.0, 1.0) > 0) else 0.0
    _, beta, cov = m2ll_grad(v, e, X, s0)
    return dict(sig=s0, ep=up - s0, em=s0 - lo, ul95=ul95, beta=beta, cov=cov, nll=fmin)


# ---------------------------------------------------------------------------------------- control C1
P("\n" + "=" * 118 + "\nC1  CONTROL  (unscaled data)\n" + "=" * 118)
vb0 = np.array([s["vm"] for s in cln_b]); eb = np.array([s["em"] for s in cln_b])
vt0 = np.array([s["vm"] for s in cln_t]); et = np.array([s["em"] for s in cln_t])
sb0 = fit_single(vb0, eb); st0 = fit_single(vt0, et)
Xt_plain = np.ones((len(vt0), 1))
st0_own = fit_grad(vt0, et, Xt_plain)
check("C1 CONTROL: single-Gaussian gradient-free cleaned dispersions reproduce CFG51 (Bootes I 3.911, Tucana II 4.064 km/s, tol 5e-3) and member counts 55/14, cleaned 53/12",
      f"Bootes I {sb0['sig']:.4f} (+{sb0['ep']:.3f} -{sb0['em']:.3f}); Tucana II {st0['sig']:.4f} (+{st0['ep']:.3f} -{st0['em']:.3f}) [own WLS engine, g=0: {st0_own['sig']:.4f}]; "
      f"members {len(mem_b)}/{len(mem_t)}, cleaned {len(cln_b)}/{len(cln_t)}",
      abs(sb0["sig"] - 3.911) < 5e-3 and abs(st0["sig"] - 4.064) < 5e-3 and abs(st0_own["sig"] - 4.064) < 5e-3 and (len(mem_b), len(mem_t), len(cln_b), len(cln_t)) == (55, 14, 53, 12))

# ---------------------------------------------------------------------------------------- Q1
P("\n" + "=" * 118 + "\nQ1  BOOTES I: TWO-GAUSSIAN MIXTURE (common mean)" + ("  [velocities x 0.5]" if MUTATE else "") + "\n" + "=" * 118)
vb = SF * vb0
gb = galinfo("Bootes I")
nll1, mu1 = m2ll_single(vb, eb, fit_single(vb, eb)["sig"])
best = opt_mix(vb, eb, nst=64)
best2 = opt_mix(vb, eb, nst=64, extra=(best[1][0], best[1][1], best[1][2] - best[1][1], best[1][3]))
best = min(best, best2, key=lambda t: t[0])
mu, sc, sh, fh = best[1]
stot = math.sqrt((1 - fh) * sc ** 2 + fh * sh ** 2)
LR = nll1 - best[0]
P(f"    single Gaussian: sigma {fit_single(vb, eb)['sig']:.3f}, mean {mu1:.2f}, -2lnL {nll1:.3f}")
P(f"    mixture MLE: mu {mu:.2f}, s_cold {sc:.3f}, s_hot {sh:.3f}, f_hot {fh:.3f}; sigma_tot {stot:.3f}; -2lnL {best[0]:.3f}")
P(f"    LR (single vs mixture) = {LR:.3f}  (2 extra parameters; NOT a formal significance: boundary and unidentified parameters at f->0 or s_c=s_h)")
# repeat fit from a different multi-start seed to show stability
alt = opt_mix(vb, eb, nst=40)
P(f"    stability: independent 40-start refit gives -2lnL {alt[0]:.4f} (delta {alt[0] - best[0]:+.4f})")
PR = {}
grids = dict(sc=np.linspace(0.0, 6.0, 61), sh=np.linspace(0.5, 15.0, 59), f=np.linspace(0.0, 1.0, 41), stot=np.linspace(0.5, 8.0, 61))
for key in ("sc", "sh", "f", "stot"):
    est, lo, hi, lop, hop, curve = profile_interval(vb, eb, key, best, grids[key], nst=16)
    PR[key] = dict(est=est, lo=lo, hi=hi, lo_open=lop, hi_open=hop)
    P(f"    profile 1-sigma {key:5s}: {est:.3f}  [{lo:.3f}{' (open)' if lop else ''}, {hi:.3f}{' (open)' if hop else ''}]")
# diagnostic: parametric bootstrap of LR (single-Gaussian null)
rng = np.random.default_rng(66)
s_null = fit_single(vb, eb)["sig"]; nb = 0; lrs = []
NBOOT = 200
for _ in range(NBOOT):
    vs_ = mu1 + rng.normal(size=len(vb)) * np.sqrt(s_null ** 2 + eb ** 2)
    n1 = m2ll_single(vs_, eb, fit_single(vs_, eb)["sig"])[0]
    bm = opt_mix(vs_, eb, nst=10)[0]
    lrs.append(max(n1 - bm, 0.0))
lrs = np.array(lrs)
pboot = float(np.mean(lrs >= LR))
P(f"    diagnostic (reported, not load-bearing): parametric bootstrap under the single-Gaussian null, {NBOOT} sets: P(LR >= {LR:.2f}) = {pboot:.3f}; null LR median {np.median(lrs):.2f}, 95th pct {np.percentile(lrs, 95):.2f}")

Q1 = {}
for foot in FOOTS:
    # cold-only: profile interval on s_c ; total: profile interval on sigma_tot
    c = PR["sc"]; t = PR["stot"]
    cold = score(gb, sc, max(c["hi"] - c["est"], 0.0), max(c["est"] - c["lo"], 0.0), foot)
    tot = score(gb, stot, max(t["hi"] - t["est"], 0.0), max(t["est"] - t["lo"], 0.0), foot)
    Q1[foot] = dict(cold=cold, total=tot)
    P(f"    {foot:9s} sigma_law {spred(gb, foot):.3f}:  COLD-ONLY  {cold['off']:+.3f} +- {cold['tot']:.3f} ({cold['z']:+.2f} sigma) [e_stat {cold['e']:.3f}, floor {cold['fl']:.3f}]"
      f";  TOTAL-MIXTURE {tot['off']:+.3f} +- {tot['tot']:.3f} ({tot['z']:+.2f} sigma) [e_stat {tot['e']:.3f}, floor {tot['fl']:.3f}]")

# ---------------------------------------------------------------------------------------- Q2
P("\n" + "=" * 118 + "\nQ2  TUCANA II: LINEAR VELOCITY GRADIENT" + ("  [velocities x 0.5]" if MUTATE else "") + "\n" + "=" * 118)
gt = galinfo("Tucana II")
vt = SF * vt0
xi, eta = tangent(np.array([s["ra"] for s in cln_t]), np.array([s["dec"] for s in cln_t]), gt["ra"], gt["dec"])
rh_deg = gt["rhalf_arcmin"] / 60.0
P(f"    members {len(vt)}; projected offsets xi (E) [{xi.min():.3f}, {xi.max():.3f}] deg, eta (N) [{eta.min():.3f}, {eta.max():.3f}] deg; rhalf {gt['rhalf_arcmin']:.2f}' = {rh_deg:.4f} deg;"
  f" radii in r_half: median {np.median(np.hypot(xi, eta)) / rh_deg:.2f}, max {np.max(np.hypot(xi, eta)) / rh_deg:.2f}")
Xg = np.column_stack([np.ones_like(xi), xi, eta])
fg = fit_grad(vt, et, Xg); f0 = fit_grad(vt, et, np.ones((len(vt), 1)))
LRg = f0["nll"] - fg["nll"]
gx, gy = fg["beta"][1], fg["beta"][2]
amp = math.hypot(gx, gy); pa = math.degrees(math.atan2(gx, gy)) % 360
# amplitude uncertainty by propagation from the (gx, gy) covariance
cv = fg["cov"][1:, 1:]; u = np.array([gx, gy]) / amp if amp > 0 else np.array([1.0, 0.0])
amp_err = math.sqrt(u @ cv @ u)
P(f"    no gradient : sigma {f0['sig']:.3f} (+{f0['ep']:.3f} -{f0['em']:.3f}), mean {f0['beta'][0]:.2f}, -2lnL {f0['nll']:.3f}")
P(f"    with gradient: sigma_g {fg['sig']:.3f} (+{fg['ep']:.3f} -{fg['em']:.3f}) [UL95 {fg['ul95']:.3f}], v0 {fg['beta'][0]:.2f}, g_x(E) {gx:+.2f}+-{math.sqrt(cv[0, 0]):.2f}, g_y(N) {gy:+.2f}+-{math.sqrt(cv[1, 1]):.2f} km/s/deg,"
  f" -2lnL {fg['nll']:.3f}")
P(f"    gradient amplitude {amp:.2f} +- {amp_err:.2f} km/s/deg = {amp * rh_deg:.2f} km/s per r_half, direction (velocity increases toward) PA {pa:.0f} deg E of N;"
  f" LR vs g=0: {LRg:.3f} (2 dof; chi2 tail p = {chi2dist.sf(max(LRg, 0), 2):.4f}, nominal)")
# permutation null
rng = np.random.default_rng(67); NP = 2000; sg_null = []; lr_null = []
for _ in range(NP):
    ix = rng.permutation(len(vt)); Xp = Xg[ix]
    fp = fit_grad(vt, et, Xp); lr_null.append(f0["nll"] - fp["nll"]); sg_null.append(fp["sig"])
lr_null = np.array(lr_null); sg_null = np.array(sg_null)
P(f"    diagnostic (reported, not load-bearing): position-permutation null ({NP} shuffles): P(LR >= {LRg:.2f}) = {np.mean(lr_null >= LRg):.4f}; "
  f"null sigma_g median {np.median(sg_null):.2f} (5-95%: {np.percentile(sg_null, 5):.2f}-{np.percentile(sg_null, 95):.2f}) vs no-gradient {f0['sig']:.2f} -- i.e. chance alone lowers sigma by that much with N={len(vt)}")
Q2 = {}
for foot in FOOTS:
    sc_ = score(gt, fg["sig"], fg["ep"], fg["em"], foot)
    s0_ = score(gt, f0["sig"], f0["ep"], f0["em"], foot)
    Q2[foot] = dict(grad=sc_, nograd=s0_)
    P(f"    {foot:9s} sigma_law {spred(gt, foot):.3f}: no-gradient {s0_['off']:+.3f} +- {s0_['tot']:.3f} ({s0_['z']:+.2f});  GRADIENT-REMOVED {sc_['off']:+.3f} +- {sc_['tot']:.3f} ({sc_['z']:+.2f} sigma) [e_stat {sc_['e']:.3f}, floor {sc_['fl']:.3f}]")

# ---------------------------------------------------------------------------------------- gates
P("\n" + "=" * 118 + "\nS1 / S2 / R1  SURVIVAL GATES\n" + "=" * 118)
s1 = all(Q1[f]["total"]["z"] > 2 for f in FOOTS)
s2 = all(Q2[f]["grad"]["z"] > 2 for f in FOOTS)
r1 = all(Q1[f]["cold"]["z"] > 2 for f in FOOTS)
fz = lambda d: f"{d['off']:+.3f} +- {d['tot']:.3f} ({d['z']:+.2f})"
check("S1 [HEADLINE] BOOTES I OFFSET SURVIVES the two-Gaussian fit: total-mixture offset > 0 at > 2 sigma on both footings" + ("  [MUTATE: v x 0.5]" if MUTATE else ""),
      "; ".join(f"{f[:3]}: {fz(Q1[f]['total'])}" for f in FOOTS), s1)
check("S2 [HEADLINE] TUCANA II OFFSET SURVIVES the gradient fit: gradient-removed offset > 0 at > 2 sigma on both footings" + ("  [MUTATE: v x 0.5]" if MUTATE else ""),
      "; ".join(f"{f[:3]}: {fz(Q2[f]['grad'])}" for f in FOOTS), s2)
check("R1 (reported) Bootes I COLD-ONLY reading survives (> 2 sigma, both footings)",
      "; ".join(f"{f[:3]}: {fz(Q1[f]['cold'])}" for f in FOOTS), r1, lb=False)
reading = ("S1 " + ("PASS" if s1 else "FAIL") + ", S2 " + ("PASS" if s2 else "FAIL") + "; Bootes I cold-only reading " + ("survives" if r1 else "does not survive"))
P(f"\n    READING (declared form): {reading}.  Two objects, one declared model each; nothing here is a population result and nothing closes or proves the theory.")

NUMS.update(dict(
    samples=dict(bootes_members=len(mem_b), bootes_clean=len(cln_b), tucana_members=len(mem_t), tucana_clean=len(cln_t)),
    control=dict(bootes_clean_sigma=sb0["sig"], tucana_clean_sigma=st0["sig"]),
    Q1_mixture=dict(mu=mu, s_cold=sc, s_hot=sh, f_hot=fh, sigma_tot=stot, m2lnL_mix=best[0], m2lnL_single=nll1, LR=LR, profile=PR, boot_P_LR=pboot, boot_null_median=float(np.median(lrs))),
    Q1_offsets=Q1,
    Q2_gradient=dict(sigma_nograd=f0["sig"], sigma_nograd_ep=f0["ep"], sigma_nograd_em=f0["em"], sigma_grad=fg["sig"], sigma_grad_ep=fg["ep"], sigma_grad_em=fg["em"], ul95_grad=fg["ul95"],
                     gx_per_deg=gx, gy_per_deg=gy, amp_per_deg=amp, amp_err=amp_err, amp_per_rh=amp * rh_deg, PA_deg=pa, LR=LRg, p_chi2_nominal=float(chi2dist.sf(max(LRg, 0), 2)),
                     perm_p=float(np.mean(lr_null >= LRg)), perm_sigma_median=float(np.median(sg_null)), rh_deg=rh_deg),
    Q2_offsets=Q2, S1=s1, S2=s2, R1=r1, reading=reading))


def jc(o):
    if isinstance(o, dict): return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jc(x) for x in o]
    if isinstance(o, (np.floating, float)):
        x = float(o); return x if math.isfinite(x) else str(x)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


lb = [c for c in CHECKS if c["load_bearing"]]; nf = sum(not c["ok"] for c in lb)
P(f"\n  {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
json.dump(jc(dict(slug=SLUG, mutate=MUTATE, checks=CHECKS, numbers=NUMS)), open(os.path.join(SCR, SLUG + "_results.json"), "w"), indent=1)
open(os.path.join(SCR, SLUG + ".out"), "w").write("\n".join(LINES) + "\n")
sys.exit(1 if nf else 0)
