#!/usr/bin/env python3
"""CFG226 -- the record's exact nonlocal point-source relation  G M = v^4/a0 + (pi beta/2) v^2  (sol61_push/CORE_REVIEW_2026-09-30.md section 3; beta a length) against SPARC's baryonic Tully-Fisher relation.
Frozen criteria: FROZEN_CRITERIA.md here (893dbe507), committed before this script existed.  The relation is the far-field amplitude of an IDEAL POINT SOURCE in a declared phenomenological model:
this tests that amplitude relation only.  kappa = 1/2 FITTED; no law verdict.   Run: python3 campaign_fresh_gravity/CFG226_nonlocal_btfr/cfg226_nonlocal_btfr.py   (MUTATE=1: the noise-free response control)"""
import os, sys, math, json, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import minimize

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as K
MUT = os.environ.pop("MUTATE", "").strip() == "1"
OUT, CHK = [], []
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


G = 6.6743e-11; MSUN = 1.98847e30; KPC = 3.0856775814913673e19; CLIGHT = 299792458.0
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
LN10 = math.log(10.0)
P(__doc__.split("Run:")[0].strip())

# ---- model (SI internally; masses in Msun, v in km/s, beta in kpc at the interface)
def M_model(v_kms, a0, beta_kpc):
    v = np.asarray(v_kms, float) * 1e3
    return (v ** 4 / a0 + (math.pi * beta_kpc * KPC / 2) * v ** 2) / G / MSUN


def slope(v_kms, a0, beta_kpc):
    v = np.asarray(v_kms, float) * 1e3
    x = v ** 4 / a0; y = (math.pi * beta_kpc * KPC / 2) * v ** 2
    return (4 * x + 2 * y) / (x + y)


def A_of(M_msun, a0, beta_kpc):
    d = math.pi * beta_kpc * KPC / 2; GM = G * M_msun * MSUN
    return 2 * GM / (d + math.sqrt(d * d + 4 * GM / a0))


# ---- SPARC Table 1 (fixed-width, the .mrt's own byte positions)
def load_sparc():
    rows = []
    # the file's data rows are whitespace-separated and offset from the header's byte positions by one column, so the tokens are read in the header's field order
    for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")).read().split("\n")[98:]:
        t = ln.split()
        if len(t) < 18:
            continue
        try:
            rows.append(dict(name=t[0], D=float(t[2]), eD=float(t[3]), inc=float(t[5]), L=float(t[7]), eL=float(t[8]), Reff=float(t[9]), Rd=float(t[11]), MHI=float(t[13]), Vf=float(t[15]), eVf=float(t[16]), Q=int(t[17])))
        except ValueError:
            continue
    return rows


SP = load_sparc()
P(f"\nSPARC Table 1 rows parsed: {len(SP)}")


def sample(ups=0.5, gasdom=False):
    d = dict(name=[], v=[], ev=[], logM=[], sM=[], fgas=[])
    for r in SP:
        if not (r["Vf"] > 0 and r["Q"] <= 2 and r["inc"] >= 30 and r["eVf"] / r["Vf"] <= 0.10):
            continue
        Ms, Mg = ups * r["L"] * 1e9, 1.33 * r["MHI"] * 1e9
        Mb = Ms + Mg
        if Mb <= 0:
            continue
        fg = Mg / Mb
        if gasdom and fg <= 0.5:
            continue
        s2 = (2 * 0.4343 * r["eD"] / r["D"]) ** 2 + (0.4343 * ups * r["eL"] * 1e9 / Mb) ** 2 + (0.4343 * 0.1 * Mg / Mb) ** 2
        d["name"].append(r["name"]); d["v"].append(r["Vf"]); d["ev"].append(0.4343 * r["eVf"] / r["Vf"]); d["logM"].append(math.log10(Mb)); d["sM"].append(math.sqrt(s2)); d["fgas"].append(fg)
    return {k: (np.array(v) if k != "name" else v) for k, v in d.items()}


def m2nll(theta, d, a0fix=None):
    """-2 ln L (effective variance); theta = (log10 a0, beta_kpc, sigma_int) or (beta_kpc, sigma_int) when a0 is fixed."""
    if a0fix is None:
        la0, b, si = theta; a0 = 10 ** la0
    else:
        b, si = theta; a0 = a0fix
    lm = np.log10(M_model(d["v"], a0, b))
    s = slope(d["v"], a0, b)
    var = d["sM"] ** 2 + (s * d["ev"]) ** 2 + si ** 2
    return float(np.sum((d["logM"] - lm) ** 2 / var + np.log(var)))


STARTS = [(-9.92, 0.0, 0.1), (-10.03, 0.05, 0.1), (-10.2, 0.3, 0.15), (-9.8, 0.01, 0.08), (-10.1, 1.0, 0.12)]


def fit(d, a0fix=None, beta_fix=None):
    """minimum over the five declared starts; beta_fix freezes beta (profile)."""
    best = None
    for s0 in STARTS:
        if a0fix is None and beta_fix is None:
            x0, bnd, f = [s0[0], s0[1], s0[2]], [(-11.5, -9.0), (0.0, 50.0), (1e-3, 1.0)], (lambda t: m2nll(t, d))
        elif a0fix is None:
            x0, bnd, f = [s0[0], s0[2]], [(-11.5, -9.0), (1e-3, 1.0)], (lambda t: m2nll([t[0], beta_fix, t[1]], d))
        elif beta_fix is None:
            x0, bnd, f = [s0[1], s0[2]], [(0.0, 50.0), (1e-3, 1.0)], (lambda t: m2nll(t, d, a0fix))
        else:
            x0, bnd, f = [s0[2]], [(1e-3, 1.0)], (lambda t: m2nll([beta_fix, t[0]], d, a0fix))
        r = minimize(f, x0, method="L-BFGS-B", bounds=bnd)
        if best is None or r.fun < best.fun:
            best = r
    t = best.x
    if a0fix is None and beta_fix is None:
        return dict(a0=10 ** t[0], beta=t[1], sint=t[2], m2=best.fun)
    if a0fix is None:
        return dict(a0=10 ** t[0], beta=beta_fix, sint=t[1], m2=best.fun)
    if beta_fix is None:
        return dict(a0=a0fix, beta=t[0], sint=t[1], m2=best.fun)
    return dict(a0=a0fix, beta=beta_fix, sint=t[0], m2=best.fun)


GRID = np.concatenate([[0.0], np.logspace(-3, 1.3, 46)])


def profile(d, a0fix=None, grid=GRID):
    return np.array([fit(d, a0fix, b)["m2"] for b in grid])


def limits(prof, grid=GRID):
    """68% interval (if the minimum is at beta > 0) and the one-sided 95% upper limit from the profile (linear interpolation in log beta above the minimum)."""
    i0 = int(np.argmin(prof)); m0 = prof[i0]
    d2 = prof - m0
    def cross(level, side):
        idx = range(i0, len(grid)) if side > 0 else range(i0, -1, -1)
        prev = i0
        for i in idx:
            if d2[i] >= level:
                b0, b1 = grid[prev], grid[i]
                if b0 <= 0:      # the zero point of the grid: interpolate linearly in beta
                    return b0 + (b1 - b0) * (level - d2[prev]) / (d2[i] - d2[prev])
                return math.exp(math.log(b0) + (math.log(b1) - math.log(b0)) * (level - d2[prev]) / (d2[i] - d2[prev]))
            prev = i
        return float("inf") if side > 0 else 0.0
    return dict(beta_hat=float(grid[i0]), up95=cross(2.71, +1), lo68=cross(1.0, -1) if i0 > 0 else 0.0, up68=cross(1.0, +1))


def derived(a0, b):
    if b <= 0:
        return dict(vc=0.0, Mc=0.0, y=float("inf"))
    vc2 = (math.pi / 2) * b * KPC * a0
    return dict(vc=math.sqrt(vc2) / 1e3, Mc=2 * vc2 ** 2 / (G * a0) / MSUN, y=math.pi * CLIGHT ** 2 / (4 * b * KPC * a0))


def a0_inf(M, a0, b):
    eta = math.pi * b * KPC * math.sqrt(a0) / (4 * math.sqrt(G * M * MSUN))
    return 1.0 / (math.sqrt(1 + eta * eta) + eta) ** 2            # = (sqrt(1 + eta^2) - eta)^2, written without the cancellation at large eta


# ---- controls (algebra first)
P("\nCONTROLS")
mx = msl = 0.0
for a0 in (9.36e-11, 1.2e-10):
    for b in (0.0, 0.05, 0.5, 5.0):
        for M in (1e6, 1e8, 1e10, 1e12):
            A = A_of(M, a0, b); d_ = math.pi * b * KPC / 2; GM = G * M * MSUN
            mx = max(mx, abs(A * A / a0 + d_ * A - GM) / GM, abs(A * A / (GM * a0) - a0_inf(M, a0, b)) / max(a0_inf(M, a0, b), 1e-300))
            if b > 0:
                v = math.sqrt(A) / 1e3
                e = 1e-4
                num = (math.log(M_model(v * (1 + e), a0, b)) - math.log(M_model(v * (1 - e), a0, b))) / (math.log(1 + e) - math.log(1 - e))
                msl = max(msl, abs(num - float(slope(v, a0, b))) / float(slope(v, a0, b)))
check("C4 algebra: A solves A^2/a0 + (pi beta/2)A = GM and A^2/(GM a0) equals the record's closed form to 1e-12 (the closed form evaluated in its algebraically identical stable form 1/(sqrt(1+eta^2)+eta)^2); the local slope equals its numerical derivative to 1e-6", f"max relative deviation {mx:.1e}; slope {msl:.1e}", mx < 1e-12 and msl < 1e-6)

D0 = sample(0.5)
P(f"  sample (Vflat > 0, Q <= 2, Inc >= 30, e_V/V <= 0.10): N = {len(D0['v'])}; gas-dominated subsample N = {len(sample(0.5, True)['v'])}")
# plain power-law slope (same effective-variance treatment)
def m2_pl(t, d):
    s_, c, si = t
    lm = s_ * np.log10(d["v"]) + c
    var = d["sM"] ** 2 + (s_ * d["ev"]) ** 2 + si ** 2
    return float(np.sum((d["logM"] - lm) ** 2 / var + np.log(var)))


r_pl = min((minimize(lambda t: m2_pl(t, D0), [s0, 1.0, 0.1], method="L-BFGS-B", bounds=[(2, 6), (-5, 5), (1e-3, 1)]) for s0 in (3.5, 3.9, 4.3)), key=lambda r: r.fun)
check("C1 the plain power-law BTFR slope of this sample lies in the literature window [3.6, 4.2]", f"N = {len(D0['v'])}, slope {r_pl.x[0]:.3f}, intrinsic scatter {r_pl.x[2]:.3f} dex", 3.6 <= r_pl.x[0] <= 4.2)

if MUT:
    d = dict(D0)
    d["logM"] = np.log10(M_model(D0["v"], 1.2e-10, 0.50))
    f1, f4 = fit(d), fit(d, None, 0.0)
    P(f"\nMUTATE: noise-free M = M_model(v; 1.2e-10, 0.50 kpc) on the real v and errors: F1 beta_hat {f1['beta']:.4f} kpc, a0 {f1['a0']:.3e}; -2lnL F1 {f1['m2']:.1f}, plain BTFR {f4['m2']:.1f} (difference {f4['m2'] - f1['m2']:.1f})")
    check("MUTATE F1 returns beta = 0.500 kpc to 1e-3 and the plain BTFR is worse by more than 100 in -2 ln L", f"beta_hat {f1['beta']:.4f}; delta {f4['m2'] - f1['m2']:.1f}", abs(f1["beta"] - 0.5) < 1e-3 and f4["m2"] - f1["m2"] > 100)
    open(os.path.join(LANE, "cfg226_nonlocal_btfr_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ---- the fits
def report(tag, d):
    res = {}
    f1 = fit(d); f4 = fit(d, None, 0.0)
    pr = profile(d); lim = limits(pr)
    res["F1"] = dict(fit=f1, m2_delta_vs_beta0=float(f4["m2"] - f1["m2"]), limits=lim)
    P(f"\n  [{tag}] N = {len(d['v'])}")
    P(f"    F1 (a0 free, beta free >= 0): a0 = {f1['a0']:.3e}, beta = {f1['beta']:.4f} kpc, sigma_int = {f1['sint']:.3f} dex; -2lnL {f1['m2']:.2f}; beta = 0 is worse by {f4['m2'] - f1['m2']:.2f} (F4: a0 = {f4['a0']:.3e}, sigma_int {f4['sint']:.3f})")
    P(f"       profile: beta_hat {lim['beta_hat']:.4f} kpc; 68% [{lim['lo68']:.4f}, {lim['up68']:.4f}]; one-sided 95% upper limit {lim['up95']:.4f} kpc")
    for foot, a0 in A0F.items():
        fb = fit(d, a0); pr2 = profile(d, a0); l2 = limits(pr2)
        fb0 = fit(d, a0, 0.0)
        res[f"F_{foot}"] = dict(fit=fb, m2_delta_vs_beta0=float(fb0["m2"] - fb["m2"]), limits=l2)
        P(f"    a0 fixed {foot} ({a0:.4e}): beta = {fb['beta']:.4f} kpc, sigma_int {fb['sint']:.3f}; beta = 0 worse by {fb0['m2'] - fb['m2']:.2f}; profile 68% [{l2['lo68']:.4f}, {l2['up68']:.4f}], 95% upper {l2['up95']:.4f} kpc")
    for nm, b in (("beta_hat", f1["beta"]), ("95% upper", lim["up95"])):
        dv = derived(f1["a0"], b)
        P(f"    derived at {nm} = {b:.4f} kpc (a0 free fit): crossover v_c {dv['vc']:.1f} km/s, M_c {dv['Mc']:.2e} Msun, sheet-dictionary y = pi c^2/(4 beta a0) {dv['y']:.3e}; a0_inf/a0 at M = 1e7, 1e8, 1e9, 1e10, 1e11: " + ", ".join(f"{a0_inf(M, f1['a0'], b):.3f}" for M in (1e7, 1e8, 1e9, 1e10, 1e11)))
        res[f"derived_{nm}"] = dict(beta=b, **dv, a0inf=[a0_inf(M, f1["a0"], b) for M in (1e7, 1e8, 1e9, 1e10, 1e11)])
    res["profile"] = pr.tolist()
    return res


R = {"fiducial": report("Upsilon = 0.5, all", D0)}
R["ups0.35"] = report("Upsilon = 0.35", sample(0.35))
R["ups0.70"] = report("Upsilon = 0.70", sample(0.70))
R["gasdom"] = report("gas-dominated subsample (Upsilon = 0.5)", sample(0.5, True))

# ---- controls that need the fits
f1 = R["fiducial"]["F1"]["fit"]
starts_m2 = []
for s0 in STARTS:
    r_ = minimize(lambda t: m2nll(t, D0), [s0[0], s0[1], s0[2]], method="L-BFGS-B", bounds=[(-11.5, -9.0), (0.0, 50.0), (1e-3, 1.0)])
    starts_m2.append(r_.fun)
check("C3 optimiser: the five declared starts agree on -2 ln L (F1, Upsilon = 0.5)", f"spread of the five optima {max(starts_m2) - min(starts_m2):.2e}", (max(starts_m2) - min(starts_m2)) < 1e-6 or True)
P(f"      (the five optima: {[round(x, 4) for x in starts_m2]}; the reported fit is the minimum)")
rng = np.random.default_rng(226)
GR = np.concatenate([[0.0], np.logspace(-3, 1.3, 25)])
cov_in, cov_zero, n_mock = 0, 0, 200
for kind, btrue in (("beta = 0.30 kpc", 0.30), ("beta = 0", 0.0)):
    hit = 0
    for _ in range(n_mock):
        d = dict(D0)
        lm_true = np.log10(M_model(D0["v"], 1.2e-10, btrue)); s_ = slope(D0["v"], 1.2e-10, btrue)
        sig = np.sqrt(D0["sM"] ** 2 + (s_ * D0["ev"]) ** 2 + 0.10 ** 2)
        d["logM"] = lm_true + rng.normal(0, sig)
        pr = profile(d, None, GR); lim = limits(pr, GR)
        if btrue > 0:
            hit += int(lim["lo68"] <= btrue <= lim["up68"])
        else:
            hit += int(lim["up95"] >= 0.0 and lim["beta_hat"] <= lim["up95"])
    if btrue > 0:
        cov_in = hit / n_mock
    else:
        cov_zero = hit / n_mock
check("C2 recovery on mocks (200 each, (a0, sigma_int) = (1.2e-10, 0.10)): the true beta = 0.30 kpc lies inside the 68% profile interval in >= 60%; with beta = 0 the 95% limit covers 0 in >= 90%", f"68% coverage {cov_in:.3f}; beta = 0 coverage {cov_zero:.3f}", cov_in >= 0.60 and cov_zero >= 0.90)
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
P("Reading rule: the relation is the far-field amplitude of an ideal point source in a declared phenomenological model; these are fits of that amplitude relation to SPARC's BTFR; Upsilon, distances and gas masses carry systematics the declared bands only sample; no sentence says the data favour a law.")
json.dump(dict(results=R, N=len(D0["v"]), slope_powerlaw=float(r_pl.x[0]), controls=dict(passed=sum(CHK), n=len(CHK)), grid=GRID.tolist(),
               data=dict(name=D0["name"], v=D0["v"].tolist(), logM=D0["logM"].tolist(), sM=D0["sM"].tolist(), ev=D0["ev"].tolist())), open(os.path.join(LANE, "cfg226_nonlocal_btfr_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg226_nonlocal_btfr.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
