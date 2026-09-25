#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D04 -- DOES FALSIFIER ROW 11 TEST THE FRAMEWORK'S LAW?  G158's slope channel, run on the law itself.

Row 11 of deepseek_push/FALSIFIER_MATRIX.md ("the n-kill", lane G158) is registered FIRED: the deep-window slope beta of
the radial acceleration relation, mapped to an exponent by the task-declared rule n = 2*beta, reads n = 1.20 +/- 0.06,
"12.7 sigma from 2.000" (ring level: 24.6 sigma).  2.000 is the seesaw value n = s_Lambda/a0 at the canonical footing.

The seesaw n is an AMPLITUDE.  In the programme's family mu_n(u) = 1 - (1+u)^(-n), u = g/s, the deep law is
g = sqrt((s/n) g_N): a0 = s/n, and the deep slope is 1/2 for EVERY n (G158's own docstring and its own check C1).  The
rule n = 2*beta therefore assigns the canonical footing a deep slope beta = 1, which is the Newtonian slope.

This script asks the question in a form that can fail:
  (M) the deep slope of the law itself at each footing                                              [identity]
  (I) G158's own estimator and pooling, run on data that obey the law EXACTLY at the canonical footing   [injection]
      (seesaw n = 2), at the three samples' own deep points with the data's own scatter: does row 11 fire on the law
      it is meant to test?  Can the slope channel tell the two footings apart?
  (D) does the measured deep slope agree with the law's own slope at the same points?                  [data]
      Power control: the same data must exclude slopes the law does not have (0.75 and 1).
  (A) the amplitude channel, where the seesaw n lives: the lane's alpha=1 fit on law-exact data         [injection]
      and the in-force kernel's deep a0 per sample, both footings, and the n <= 2.01 kill line          [data]
The law under test is the in-force kernel nu_RAR(y) = 1/(1 - exp(-sqrt y)), y = g_N/a0.  The programme's mu_n family
and the committed alpha=1 quadratic are reported alongside.
Samples are G158's: MIGHTEE-HI (digitised Fig. 3; the 'galaxies' are 18 marker-colour groups), SPARC through G071 (the
committed corpus and D02's four corrected corpora, rebuilt in the sandbox), LITTLE THINGS dwarfs through G114.

LOAD-BEARING (they set the exit code): B1, M1, I1, I2, D1, P1, A1.  REPORTED data checks (printed PASS/FAIL, stated in
the verdict whichever way they go, not in the exit code because they answer different questions): D2 (the ring-pooled
slope) and A2 (whether the three deep samples share one amplitude).  All criteria were fixed before the first run.
MUTATE=1: the law under test is replaced by the task-declared curve g = a0 (g_N/a0)^(n/2) (beta = n/2 exactly,
n = s_Lambda/a0).  Then M1, I1, I2, D1, D2 and A1 must FAIL (rc = 1); B1, P1 and A2 do not depend on the law under test.
FIRST RUN, KEPT AS IT CAME OUT: I1 and P1 FAILED as pre-stated.  I1: on law-exact data row 11 fires in 88 per cent of draws
(per-galaxy reading) and 100 per cent (ring level), under the 95 per cent bar set for the per-galaxy reading.  P1: the data
reject beta = 1 at 6-7 sigma but a slope of 0.75 only at 2.2-2.8 sigma.  Both stay FAIL, so the main run exits 1.  The
DIAGNOSIS section was added after that run.  It changes no pre-stated criterion, seed or result, and not the exit code.
Both footings: canonical a0 = 9.3619e-11 (seesaw n = 2.000), alternative a0 = 1.1279e-10 (n = 1.660).
Run from the repository root:  python3 real_research/reviews/deep_a0eff_audit_2026_09_25/D04_g158_slope_channel.py
(about 4 minutes).  Writes D04_results[_MUTATE].json next to this file.
"""
import os, sys, csv, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sandbox as sb

MUTATE = os.environ.get("MUTATE", "0") == "1"
DS = sb.DS
ARCH = os.path.join(HERE, "D02_rerun_outputs")
A0_DE, A0_ALT = 9.3619e-11, 1.1279e-10
S_LAMBDA = 2.0 * A0_DE
N_DE, N_ALT = S_LAMBDA / A0_DE, S_LAMBDA / A0_ALT
FOOT = {"DE": A0_DE, "ALT": A0_ALT}
DEEP = 0.2
GN, MSUN, KPC = 6.674e-11, 1.98892e30, 3.0856775814913673e19
VARIANTS = {"std05_cut": dict(ud=0.5, ub=0.7, qcut=0.10), "std06_cut": dict(ud=0.6, ub=0.7, qcut=0.10),
            "std07_cut": dict(ud=0.7, ub=0.7, qcut=0.10), "std05_nocut": dict(ud=0.5, ub=0.7, qcut=None)}
CORRECTED = list(VARIANTS)
N_INJ = 400
# MIGHTEE-HI's own all-radii refits of the same kernel (Varasteanu et al. 2025, Table 3), as transcribed in the committed
# deepseek_push/G167_pipeline_split.py (A0_PAPER, A0_147, A0_06, A0_206).  Used only in DIAGNOSIS item 5.
MIGHTEE_TABLE3 = {"fiducial varying SED Ystar (median 0.36)": 1.69e-10, "radial-average Ystar": 1.47e-10,
                  "fixed Ystar_K = 0.6 (SPARC-class)": 1.08e-10, "no molecular gas": 2.06e-10}

LINES, CH = [], []
def out(s=""):
    print(s, flush=True)
    LINES.append(s)
def check(cid, claim, ok, measured, reading="", lb=True):
    CH.append(dict(id=cid, claim=claim, ok=bool(ok), load_bearing=lb, measured=measured, reading=reading))
    out(f"  [{'PASS' if ok else 'FAIL'}] {cid} {claim}" + ("" if lb else "   (reported, not load-bearing)"))
    out(f"         measured: {measured}")
    if reading:
        out(f"         reading:  {reading}")
def rule(t):
    out("")
    out("=" * 118)
    out(t)
    out("=" * 118)

# ------------------------------------------------------------------------------------------------------------------
# G158's estimators, verbatim (deepseek_push/G158_n_discriminator.py)
# ------------------------------------------------------------------------------------------------------------------
def ols_slope(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    A = np.vstack([x, np.ones(len(x))]).T
    coef, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    sig = np.sqrt((resid @ resid) / (len(x) - 2))
    se = float(np.sqrt(sig ** 2 * np.linalg.inv(A.T @ A)[0, 0]))
    return float(coef[0]), se

def fit_a0(gN, gO, lo=-10.6, hi=-9.3, npts=601):
    best = None
    for a0 in np.logspace(lo, hi, npts):
        r = np.log10(np.sqrt(gN ** 2 + a0 * gN) / gO)
        rms = np.sqrt(np.mean(r ** 2))
        if best is None or rms < best[0]:
            best = (rms, a0, np.median(r))
    return best

def boot(fn, groups, draws=2000, seed=11):
    rng = np.random.default_rng(seed)
    vals = []
    gkeys = list(groups.keys())
    for _ in range(draws):
        pick = rng.integers(0, len(gkeys), size=len(gkeys))
        idx = [i for k in pick for i in groups[gkeys[k]]]
        try:
            vals.append(fn(idx))
        except Exception:
            pass
    return float(np.mean(vals)), float(np.std(vals))

# ------------------------------------------------------------------------------------------------------------------
# G158's samples, same construction
# ------------------------------------------------------------------------------------------------------------------
def load_mightee():
    rows = list(csv.DictReader(open(os.path.join(DS, "data2", "mightee2025_rar_digitized_points.csv"))))
    gN = np.array([10.0 ** float(r["log10_gbar"]) for r in rows])
    gO = np.array([10.0 ** float(r["log10_gobs"]) for r in rows])
    grp = {}
    for i, r in enumerate(rows):
        grp.setdefault((r["color_r"], r["color_g"], r["color_b"]), []).append(i)
    return dict(name="MIGHTEE", gN=gN, gO=gO, grp=grp)

def load_sparc(g071):
    sN, sO, sgal = [], [], []
    for pg in g071["per_galaxy"]:
        for rg in pg["rings"]:
            R = rg["R_kpc"] * KPC
            gN = (rg["v_b"] * 1e3) ** 2 / R
            gO = (rg["v_obs"] * 1e3) ** 2 / R
            if gN > 0:
                sN.append(gN); sO.append(gO); sgal.append(pg["name"])
    sgal = np.array(sgal)
    grp = {}
    for i in range(len(sgal)):
        grp.setdefault(sgal[i], []).append(i)
    return dict(name="SPARC", gN=np.array(sN), gO=np.array(sO), grp=grp)

def load_hi():
    g114 = json.load(open(os.path.join(DS, "G114_results.json")))
    hN, hO, hgal = [], [], []
    for p in g114["per_galaxy"]:
        if p["sample"] != "LT" or p["gN_a0"] is None:
            continue
        V = p["V_obs_kms"] * 1e3
        R = V ** 2 / (p["gN_a0"] * A0_DE)
        hN.append(GN * p["M_b_Msun"] * MSUN / R ** 2); hO.append(V ** 2 / R); hgal.append(p["name"])
    grp = {n: [i] for i, n in enumerate(hgal)}
    return dict(name="HI", gN=np.array(hN), gO=np.array(hO), grp=grp)

def deepmask(S):
    return S["gN"] < DEEP * A0_DE

def g158_measure(S, gO=None):
    """G158's measure(): pooled OLS slope and the median per-galaxy slope over galaxies with >= 3 deep rings."""
    gN, grp = S["gN"], S["grp"]
    gO = S["gO"] if gO is None else gO
    deep = deepmask(S)
    b_pool, se_pool = ols_slope(np.log10(gN[deep]), np.log10(gO[deep]))
    pgs = []
    for g, idx in grp.items():
        idx = np.array(idx); dm = deep[idx]
        if dm.sum() >= 3:
            pgs.append(ols_slope(np.log10(gN[idx][dm]), np.log10(gO[idx][dm]))[0])
    return dict(beta_pool=b_pool, se_pool=se_pool, beta_pg=float(np.median(pgs)) if pgs else float("nan"),
                n_pg=len(pgs), n_deep=int(deep.sum()))

def g158_full(S):
    """G158's measure() including its two bootstraps (500 slope draws, 250 amplitude draws, seed 11) and beta_law."""
    gN, gO, grp = S["gN"], S["gO"], S["grp"]
    deep = deepmask(S)
    m = g158_measure(S)
    bg = {g: np.array(v) for g, v in grp.items()}
    _, se_bs = boot(lambda idx: ols_slope(np.log10(gN[idx]), np.log10(gO[idx]))[0], bg, draws=500)
    _, a0f, _ = fit_a0(gN[deep], gO[deep])
    _, a0_se = boot(lambda idx: fit_a0(gN[idx], gO[idx])[1], bg, draws=250)
    b_law, _ = ols_slope(np.log10(gN[deep]), np.log10(np.sqrt(gN ** 2 + A0_DE * gN)[deep]))
    m.update(se_pg=se_bs, a0_fit=float(a0f), a0_se=float(a0_se), beta_law=b_law)
    return m

def readings(samples, gOs):
    """G158's two slope-channel readings from three samples [MIGHTEE, SPARC, HI]:
    per-galaxy reading n = 2*mean(beta_pg MIGHTEE, beta_pg SPARC, beta_pool HI), sigma = 2*std(three)/sqrt(3);
    ring-level reading n = 2*(OLS slope over all deep rings).  'Fires' = G158's C2: > 3 sigma from 2.000 AND 1.660."""
    ms = [g158_measure(S, gO) for S, gO in zip(samples, gOs)]
    bp = [ms[0]["beta_pg"], ms[1]["beta_pg"], ms[2]["beta_pool"]]
    n_pg, s_pg = 2 * float(np.mean(bp)), 2 * float(np.std(bp) / math.sqrt(3))
    xs = [np.log10(S["gN"][deepmask(S)]) for S in samples]
    ys = [np.log10(gO[deepmask(S)]) for S, gO in zip(samples, gOs)]
    br, sr = ols_slope(np.concatenate(xs), np.concatenate(ys))
    n_r, s_r = 2 * br, 2 * sr
    fire = lambda n, s: abs(n - N_DE) / s > 3 and abs(n - N_ALT) / s > 3
    return dict(beta=bp, n_pg=n_pg, s_pg=s_pg, z2_pg=(N_DE - n_pg) / s_pg, n_ring=n_r, s_ring=s_r,
                z2_ring=(N_DE - n_r) / s_r, fire_pg=fire(n_pg, s_pg), fire_ring=fire(n_r, s_r), beta_ring=br, se_ring=sr)

# ------------------------------------------------------------------------------------------------------------------
# the laws
# ------------------------------------------------------------------------------------------------------------------
def nu_rar_curve(gN, a0):
    return gN / (1.0 - np.exp(-np.sqrt(gN / a0)))
def alpha1_curve(gN, a0):
    return np.sqrt(gN ** 2 + a0 * gN)
def mun_curve(gN, n, s=S_LAMBDA):
    """the programme's family: g_N = mu_n(g/s) g, mu_n(u) = 1 - (1+u)^(-n); bisection in log u."""
    v = np.atleast_1d(np.asarray(gN, float)) / s
    lo = np.log(v)
    hi = np.log(np.maximum(v, np.sqrt(v / n)) * 10.0 + 10.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi); u = np.exp(mid)
        f = u * (1.0 - (1.0 + u) ** (-n)) - v
        lo = np.where(f < 0, mid, lo); hi = np.where(f < 0, hi, mid)
    return s * np.exp(0.5 * (lo + hi))
def task_curve(gN, a0):
    n = S_LAMBDA / a0
    return a0 * (gN / a0) ** (n / 2.0)
def law(gN, foot):
    """the law under test: the in-force kernel; under MUTATE the task-declared curve beta = n/2."""
    a0 = FOOT[foot]
    return task_curve(gN, a0) if MUTATE else nu_rar_curve(gN, a0)
def local_slope(fn, gN, h=1e-4):
    gN = np.atleast_1d(np.asarray(gN, float))
    return (np.log(fn(gN * (1 + h))) - np.log(fn(gN * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))

# ------------------------------------------------------------------------------------------------------------------
# noise model (from the data; does not depend on the law under test)
# ------------------------------------------------------------------------------------------------------------------
def noise_model(S):
    gN, gO, grp = S["gN"], S["gO"], S["grp"]
    deep = deepmask(S)
    ss, dof, offs, wn = 0.0, 0, [], []
    for g, idx in grp.items():
        idx = np.array(idx); m = deep[idx]
        if m.sum() >= 3:
            x = np.log10(gN[idx][m]); y = np.log10(gO[idx][m])
            A = np.vstack([x, np.ones_like(x)]).T
            r = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
            ss += float(r @ r); dof += len(x) - 2
            offs.append(float(np.mean(y - np.log10(nu_rar_curve(gN[idx][m], A0_DE))))); wn.append(int(m.sum()))
    if dof > 0:
        sw = math.sqrt(ss / dof)
        sg = math.sqrt(max(float(np.var(offs)) - float(np.mean([sw ** 2 / k for k in wn])), 0.0))
        return dict(sig_ring=sw, sig_gal=sg)
    x = np.log10(gN[deep]); y = np.log10(gO[deep])
    A = np.vstack([x, np.ones_like(x)]).T
    r = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    return dict(sig_ring=math.sqrt(float(r @ r) / (len(x) - 2)), sig_gal=0.0)

def inject(S, foot, rng, nm, sig_x=0.0, curve=None):
    """law-exact g_obs at the sample's own g_N; per-galaxy offsets in log g_obs (sig_gal: distance, inclination) and
    in log g_N (sig_x: the stellar mass-to-light ratio moves where a galaxy's rings sit on the law while the estimator
    still reads the tabulated g_N), plus per-ring noise sig_ring."""
    gN = S["gN"]
    y = np.empty(len(gN))
    for g, idx in S["grp"].items():
        idx = np.array(idx)
        dx = rng.normal(0.0, sig_x) if sig_x > 0 else 0.0
        gt = gN[idx] * 10 ** dx
        y[idx] = np.log10(law(gt, foot) if curve is None else curve(gt)) + rng.normal(0.0, nm["sig_gal"])
    return 10 ** (y + rng.normal(0.0, nm["sig_ring"], size=len(y)))

# ------------------------------------------------------------------------------------------------------------------
# per-galaxy slopes and the paired bootstrap
# ------------------------------------------------------------------------------------------------------------------
def pg_slopes(S, gO):
    deep = deepmask(S)
    out_ = {}
    for g, idx in S["grp"].items():
        idx = np.array(idx); m = deep[idx]
        if m.sum() >= 3:
            out_[g] = ols_slope(np.log10(S["gN"][idx][m]), np.log10(gO[idx][m]))[0]
    return out_

def slope_vs_ref(S, ref_gO, draws=2000, seed=2026):
    """data slope minus the reference law's slope at the same points, with a paired bootstrap.
    Multi-ring samples: median per-galaxy slope, galaxies resampled.  Single-point samples (HI): pooled OLS, points resampled."""
    rng = np.random.default_rng(seed)
    deep = deepmask(S)
    bd = pg_slopes(S, S["gO"])
    if bd:
        br = pg_slopes(S, ref_gO)
        keys = list(bd)
        d_arr = np.array([bd[k] for k in keys]); r_arr = np.array([br[k] for k in keys])
        delta = float(np.median(d_arr) - np.median(r_arr))
        ds, bs = [], []
        for _ in range(draws):
            p = rng.integers(0, len(keys), size=len(keys))
            ds.append(np.median(d_arr[p]) - np.median(r_arr[p])); bs.append(np.median(d_arr[p]))
        return dict(beta=float(np.median(d_arr)), beta_ref=float(np.median(r_arr)), delta=delta,
                    se=float(np.std(ds)), se_beta=float(np.std(bs)), n=len(keys))
    x = np.log10(S["gN"][deep]); yd = np.log10(S["gO"][deep]); yr = np.log10(ref_gO[deep])
    bd0, br0 = ols_slope(x, yd)[0], ols_slope(x, yr)[0]
    ds, bs = [], []
    for _ in range(draws):
        p = rng.integers(0, len(x), size=len(x))
        b1 = ols_slope(x[p], yd[p])[0]; b2 = ols_slope(x[p], yr[p])[0]
        ds.append(b1 - b2); bs.append(b1)
    return dict(beta=bd0, beta_ref=br0, delta=bd0 - br0, se=float(np.std(ds)), se_beta=float(np.std(bs)), n=len(x))

# ------------------------------------------------------------------------------------------------------------------
# the in-force kernel's amplitude on the deep window
# ------------------------------------------------------------------------------------------------------------------
def fit_a0_nu(gN, gO, lo=-10.8, hi=-9.3, npts=601):
    grid = np.logspace(lo, hi, npts)
    rms = [np.sqrt(np.mean(np.log10(nu_rar_curve(gN, a) / gO) ** 2)) for a in grid]
    k = int(np.argmin(rms))
    return float(grid[k]), k in (0, npts - 1)

def amp_nu(S, draws=300, seed=7):
    deep = deepmask(S)
    a0, edge = fit_a0_nu(S["gN"][deep], S["gO"][deep])
    groups = [np.array([i for i in idx if deep[i]]) for idx in S["grp"].values()]
    groups = [g for g in groups if len(g)]
    rng = np.random.default_rng(seed)
    la = []
    for _ in range(draws):
        p = rng.integers(0, len(groups), size=len(groups))
        idx = np.concatenate([groups[k] for k in p])
        la.append(math.log(fit_a0_nu(S["gN"][idx], S["gO"][idx])[0]))
    se_ln = float(np.std(la))
    n = S_LAMBDA / a0
    return dict(a0=a0, edge=edge, se_ln=se_ln, n=n, sig_n=n * se_ln)

# ==================================================================================================================
def main():
    t0 = time.time()
    out("D04 -- DOES FALSIFIER ROW 11 TEST THE FRAMEWORK'S LAW?  G158's slope channel, run on the law itself.")
    out("=" * 104)
    out("Row 11 ('the n-kill', G158) is registered FIRED: the deep slope beta, mapped by the task-declared rule n = 2*beta,")
    out("reads n = 1.20 +/- 0.06, '12.7 sigma from 2.000'.  In the programme's own family the seesaw n is an AMPLITUDE")
    out("(a0 = s/n) and the deep slope is 1/2 for every n; the rule n = 2*beta gives the canonical footing beta = 1, the")
    out("Newtonian slope.  Here the lane's own estimator is run on data that obey the law exactly.")
    out(f"Law under test: {'the TASK-DECLARED curve g = a0 (g_N/a0)^(n/2)  [MUTATE control]' if MUTATE else 'the in-force kernel nu_RAR(y) = 1/(1 - exp(-sqrt y))'}.")
    out(f"Footings: canonical a0 = {A0_DE:.4e} (seesaw n = {N_DE:.3f}), alternative a0 = {A0_ALT:.4e} (n = {N_ALT:.3f}).")
    out("Run from the repository root:  python3 real_research/reviews/deep_a0eff_audit_2026_09_25/D04_g158_slope_channel.py")

    # ---------------- samples ----------------
    MIG, HI = load_mightee(), load_hi()
    corp = {"committed": load_sparc(json.load(open(os.path.join(DS, "G071_results.json"))))}
    for tag, kw in VARIANTS.items():
        S = sb.build(sb.corpus_variant(**kw), tag="D04" + tag)
        try:
            r = sb.run(S, "G071_sparc_fullcurve.py")
            if r["rc"] != 0:
                raise RuntimeError(f"G071 failed in the {tag} sandbox: {r['stderr'][-400:]}")
            corp[tag] = load_sparc(sb.load(S, "G071_results.json"))
        finally:
            sb.destroy(S)
    ALL = ["committed"] + CORRECTED
    NM = {"MIGHTEE": noise_model(MIG), "HI": noise_model(HI)}
    for k in ALL:
        NM["SPARC_" + k] = noise_model(corp[k])

    # ---------------- B: faithfulness ----------------
    rule("B  FAITHFULNESS: this script's copy of G158's estimators reproduces G158's committed and D02-archived results")
    worst, nf, fails = 0.0, 0, []
    REPRO = {}
    for k in ALL:
        ref = json.load(open(os.path.join(DS, "G158_results.json") if k == "committed" else os.path.join(ARCH, k, "G158_results.json")))
        mine = {"MIGHTEE": g158_full(MIG), "SPARC": g158_full(corp[k]), "HI": g158_full(HI)}
        REPRO[k] = mine
        rd = readings([MIG, corp[k], HI], [MIG["gO"], corp[k]["gO"], HI["gO"]])
        pairs = []
        for smp in ("MIGHTEE", "SPARC", "HI"):
            R = ref["measurements"][smp]; M = mine[smp]
            pairs += [(R["beta_pooled"], M["beta_pool"]), (R["beta_pooled_se"], M["se_pool"]), (R["beta_per_galaxy"], M["beta_pg"]),
                      (R["beta_per_galaxy_se"], M["se_pg"]), (R["beta_law_window"], M["beta_law"]), (R["a0_fit_deep"], M["a0_fit"]),
                      (R["a0_se"], M["a0_se"]), (R["n_deep"], M["n_deep"])]
        P = ref["pooled"]
        pairs += [(P["beta_ring_pooled"], rd["beta_ring"]), (P["se_ring"], rd["se_ring"]),
                  (P["n_per_galaxy_reading"], rd["n_pg"]), (P["n_per_galaxy_se"], rd["s_pg"]),
                  (ref["discriminator"]["slope_channel"]["sep_from_2_000_sigma"], abs(rd["z2_pg"]))]
        for a, b in pairs:
            nf += 1
            if isinstance(a, float) and math.isnan(a) and math.isnan(b):
                continue
            d = abs(a - b) / max(abs(a), 1e-30)
            worst = max(worst, d)
            if d > 1e-9:
                fails.append((k, a, b))
    check("B1", "the copy of G158's estimators reproduces its committed results and D02's four archived corrected results",
          not fails, f"{nf} numbers over 5 corpora; worst relative difference {worst:.1e}" + (f"; mismatches {fails[:3]}" if fails else ""),
          "the injections below go through exactly the estimator that produced row 11's numbers")
    out("")
    out(f"  {'corpus':12s} {'SPARC Ndeep':>11s} {'beta_pg SPARC':>13s} {'MIGHTEE':>8s} {'HI':>6s} {'n = 2*mean':>10s} {'sigma':>6s} {'from 2.000':>10s} {'ring n':>7s} {'from 2.000':>10s}")
    for k in ALL:
        rd = readings([MIG, corp[k], HI], [MIG["gO"], corp[k]["gO"], HI["gO"]])
        out(f"  {k:12s} {int(deepmask(corp[k]).sum()):11d} {rd['beta'][1]:13.3f} {rd['beta'][0]:8.3f} {rd['beta'][2]:6.3f} {rd['n_pg']:10.3f} {rd['s_pg']:6.3f} {rd['z2_pg']:9.1f}s {rd['n_ring']:7.3f} {rd['z2_ring']:9.1f}s")

    # ---------------- M: what the law's deep slope is ----------------
    rule("M  THE LAW'S OWN DEEP SLOPE (d log g_obs / d log g_N at y = g_N/a0)")
    ys = [1e-4, 0.01, 0.05, 0.1, 0.2]
    out(f"  {'curve':44s} " + " ".join(f"y={y:<7g}" for y in ys))
    tab = [("in-force kernel nu_RAR, canonical footing", lambda q: nu_rar_curve(q, A0_DE), A0_DE),
           ("in-force kernel nu_RAR, alternative footing", lambda q: nu_rar_curve(q, A0_ALT), A0_ALT),
           ("alpha=1 quadratic, canonical", lambda q: alpha1_curve(q, A0_DE), A0_DE),
           ("programme family mu_n, n = 2.000 (a0 = s/2)", lambda q: mun_curve(q, N_DE), A0_DE),
           ("programme family mu_n, n = 1.660 (a0 = s/1.66)", lambda q: mun_curve(q, N_ALT), A0_ALT),
           ("task-declared beta = n/2, n = 2.000", lambda q: task_curve(q, A0_DE), A0_DE),
           ("task-declared beta = n/2, n = 1.660", lambda q: task_curve(q, A0_ALT), A0_ALT)]
    for lab, fn, a0 in tab:
        out(f"  {lab:44s} " + " ".join(f"{float(local_slope(fn, y * a0)[0]):<9.4f}" for y in ys))
    m1 = {f: float(local_slope(lambda q, f=f: law(q, f), 1e-4 * FOOT[f])[0]) for f in FOOT}
    check("M1", "[identity] the law under test has deep slope 1/2 at BOTH footings (|beta - 0.5| < 0.01 at y = 1e-4): the slope carries no n",
          all(abs(v - 0.5) < 0.01 for v in m1.values()),
          f"beta(y = 1e-4) = {m1['DE']:.4f} (canonical, n = 2.000), {m1['ALT']:.4f} (alternative, n = 1.660)",
          "an identity, carries no evidence: the seesaw n sets the amplitude a0 = s/n, and beta = n/2 = 1 is the Newtonian slope")

    # ---------------- I: the lane's estimator on the law itself ----------------
    rule("I  INJECTION: G158's slope channel run on data that obey the law EXACTLY at the canonical footing (seesaw n = 2)")
    out("  noise model from the data (dex): within-galaxy ring scatter / per-galaxy offset")
    for k, v in NM.items():
        out(f"    {k:22s} {v['sig_ring']:.3f} / {v['sig_gal']:.3f}")
    I1, DRAWS = {}, {}
    for k in ALL:
        rng = np.random.default_rng(20260925)
        fp, fr, npg, z2 = 0, 0, [], []
        dr = dict(n_pg=[], n_ring=[], s_pg=[], fire_pg=[], beta_hi=[], spread=[])
        for _ in range(N_INJ):
            gOs = [inject(MIG, "DE", rng, NM["MIGHTEE"]), inject(corp[k], "DE", rng, NM["SPARC_" + k]), inject(HI, "DE", rng, NM["HI"])]
            rd = readings([MIG, corp[k], HI], gOs)
            fp += rd["fire_pg"]; fr += rd["fire_ring"]; npg.append(rd["n_pg"]); z2.append(rd["z2_pg"])
            dr["n_pg"].append(rd["n_pg"]); dr["n_ring"].append(rd["n_ring"]); dr["s_pg"].append(rd["s_pg"])
            dr["fire_pg"].append(rd["fire_pg"]); dr["beta_hi"].append(rd["beta"][2]); dr["spread"].append(max(rd["beta"]) - min(rd["beta"]))
        DRAWS[k] = {kk: np.array(v) for kk, v in dr.items()}
        I1[k] = dict(frac_fire_pg=fp / N_INJ, frac_fire_ring=fr / N_INJ, n_pg_median=float(np.median(npg)), z2_median=float(np.median(z2)))
    for k in ALL:
        v = I1[k]
        out(f"    {k:12s} law-exact data: slope-channel reading n = {v['n_pg_median']:.3f} (median), {v['z2_median']:.1f} sigma from 2.000; "
            f"row 11 fires in {100 * v['frac_fire_pg']:.1f}% (per-galaxy) / {100 * v['frac_fire_ring']:.1f}% (ring level) of {N_INJ} draws")
    check("I1", "[injection] row 11's criterion (G158 C2: > 3 sigma from 2.000 and 1.660) FIRES on law-exact canonical-footing data in >= 95% of draws, for every corpus",
          all(I1[k]["frac_fire_pg"] >= 0.95 and I1[k]["frac_fire_ring"] >= 0.95 for k in ALL),
          "; ".join(f"{k} {100 * I1[k]['frac_fire_pg']:.0f}%/{100 * I1[k]['frac_fire_ring']:.0f}%" for k in ALL),
          "the falsifier fires on the law it is registered to test: its firing carries no information about the law")
    I2 = {}
    for k in ALL:
        rDE = readings([MIG, corp[k], HI], [law(S["gN"], "DE") for S in (MIG, corp[k], HI)])
        rAL = readings([MIG, corp[k], HI], [law(S["gN"], "ALT") for S in (MIG, corp[k], HI)])
        mDE = readings([MIG, corp[k], HI], [mun_curve(S["gN"], N_DE) for S in (MIG, corp[k], HI)])
        mAL = readings([MIG, corp[k], HI], [mun_curve(S["gN"], N_ALT) for S in (MIG, corp[k], HI)])
        I2[k] = dict(n_DE=rDE["n_pg"], n_ALT=rAL["n_pg"], diff=abs(rDE["n_pg"] - rAL["n_pg"]),
                     ring_DE=rDE["n_ring"], ring_ALT=rAL["n_ring"], mun_DE=mDE["n_pg"], mun_ALT=mAL["n_pg"])
    for k in ALL:
        v = I2[k]
        out(f"    {k:12s} noise-free: reading n = {v['n_DE']:.3f} (law at n = 2.000) vs {v['n_ALT']:.3f} (law at n = 1.660); ring level {v['ring_DE']:.3f} vs {v['ring_ALT']:.3f}; "
            f"programme family mu_n: {v['mun_DE']:.3f} vs {v['mun_ALT']:.3f}")
    check("I2", f"[injection] the slope channel cannot tell the footings apart: its reading on law-exact data moves by < 0.10 between n = 2.000 and n = 1.660 (the gap it claims to resolve is {N_DE - N_ALT:.3f})",
          all(I2[k]["diff"] < 0.10 for k in ALL),
          "; ".join(f"{k} {I2[k]['diff']:.3f}" for k in ALL),
          "the footing lives in the amplitude; a slope reading of about 1.1-1.2 is what the law itself returns at either footing")

    # ---------------- D: the data against the law's own slope ----------------
    rule("D  DATA: the measured deep slope against the law's own slope at the same points (paired bootstrap, 2000 draws)")
    D1, P1 = {}, {}
    out(f"  {'corpus':12s} {'sample':8s} {'beta data':>9s} {'beta law':>8s} {'delta':>7s} {'se':>6s} {'z':>6s} | {'law at alternative':>18s}")
    for k in ALL:
        rows = {}
        for S in (MIG, corp[k], HI):
            a = slope_vs_ref(S, law(S["gN"], "DE")); b = slope_vs_ref(S, law(S["gN"], "ALT"))
            rows[S["name"]] = dict(DE=a, ALT=b)
            out(f"  {k:12s} {S['name']:8s} {a['beta']:9.3f} {a['beta_ref']:8.3f} {a['delta']:+7.3f} {a['se']:6.3f} {a['delta'] / a['se']:+6.2f} | "
                f"law {b['beta_ref']:.3f}, z {b['delta'] / b['se']:+.2f}")
        w = np.array([1 / rows[s]["DE"]["se"] ** 2 for s in rows]); dl = np.array([rows[s]["DE"]["delta"] for s in rows])
        pd, ps = float(np.sum(w * dl) / np.sum(w)), float(1 / math.sqrt(np.sum(w)))
        wb = np.array([1 / rows[s]["DE"]["se_beta"] ** 2 for s in rows]); bb = np.array([rows[s]["DE"]["beta"] for s in rows])
        pb, pbs = float(np.sum(wb * bb) / np.sum(wb)), float(1 / math.sqrt(np.sum(wb)))
        D1[k] = dict(rows={s: {f: {kk: vv for kk, vv in rows[s][f].items()} for f in rows[s]} for s in rows},
                     pooled_delta=pd, pooled_se=ps, pooled_z=pd / ps, zs=[rows[s]["DE"]["delta"] / rows[s]["DE"]["se"] for s in rows])
        P1[k] = dict(beta=pb, se=pbs, z075=(0.75 - pb) / pbs, z1=(1.0 - pb) / pbs)
        out(f"  {k:12s} {'POOLED':8s} {'':9s} {'':8s} {pd:+7.3f} {ps:6.3f} {pd / ps:+6.2f}   (inverse-variance over the three samples)")
    check("D1", "[data] the measured per-galaxy deep slope agrees with the law's own slope at the same points: |z| < 3 for every sample and the pooled difference, in every corrected corpus",
          all(max(abs(z) for z in D1[k]["zs"] + [D1[k]["pooled_z"]]) < 3 for k in CORRECTED),
          "; ".join(f"{k}: pooled {D1[k]['pooled_delta']:+.3f} +/- {D1[k]['pooled_se']:.3f} (z {D1[k]['pooled_z']:+.2f}), max |z| {max(abs(z) for z in D1[k]['zs'] + [D1[k]['pooled_z']]):.2f}" for k in CORRECTED)
          + f"; committed corpus (kinematic ratios, reported only): pooled z {D1['committed']['pooled_z']:+.2f}",
          "the deep slope row 11 measured is the slope the framework's law predicts")
    check("P1", "[data, power] the same data and bootstrap EXCLUDE the slopes the law does not have: beta = 0.75 and the Newtonian beta = 1 at > 3 sigma, in every corrected corpus",
          all(P1[k]["z075"] > 3 and P1[k]["z1"] > 3 for k in CORRECTED),
          "; ".join(f"{k}: beta {P1[k]['beta']:.3f} +/- {P1[k]['se']:.3f}, {P1[k]['z075']:.1f} sigma from 0.75, {P1[k]['z1']:.1f} sigma from 1" for k in CORRECTED),
          "D1's agreement is not for lack of power; what row 11 excluded at 12.7 sigma is beta = 1")
    D2 = {}
    for k in ALL:
        dat = readings([MIG, corp[k], HI], [MIG["gO"], corp[k]["gO"], HI["gO"]])
        res = {}
        for sx in (0.0, 0.1):
            rng = np.random.default_rng(777)
            br = [readings([MIG, corp[k], HI], [inject(MIG, "DE", rng, NM["MIGHTEE"], sx), inject(corp[k], "DE", rng, NM["SPARC_" + k], sx),
                                               inject(HI, "DE", rng, NM["HI"], sx)])["beta_ring"] for _ in range(N_INJ)]
            res[sx] = (float(np.mean(br)), float(np.std(br)))
        D2[k] = dict(beta_data=dat["beta_ring"], inj0=res[0.0], inj1=res[0.1], z0=(dat["beta_ring"] - res[0.0][0]) / res[0.0][1],
                     z1=(dat["beta_ring"] - res[0.1][0]) / res[0.1][1])
    out("")
    out("  ring-pooled slope (row 11's 'ring level'), data vs law-exact injections with the data's scatter, and with 0.1 dex per-galaxy mass-to-light scatter:")
    for k in ALL:
        v = D2[k]
        out(f"    {k:12s} data {v['beta_data']:.3f} | law, no M/L scatter {v['inj0'][0]:.3f} +/- {v['inj0'][1]:.3f} (z {v['z0']:+.2f}) | "
            f"law, 0.1 dex M/L scatter {v['inj1'][0]:.3f} +/- {v['inj1'][1]:.3f} (z {v['z1']:+.2f})")
    check("D2", "[data] the ring-pooled deep slope agrees with law-exact injections carrying 0.1 dex per-galaxy mass-to-light scatter (|z| < 3), in every corrected corpus",
          all(abs(D2[k]["z1"]) < 3 for k in CORRECTED),
          "; ".join(f"{k} z {D2[k]['z1']:+.2f} (without the scatter {D2[k]['z0']:+.2f})" for k in CORRECTED)
          + f"; committed corpus z {D2['committed']['z1']:+.2f}", lb=False)

    # ---------------- A: the amplitude channel ----------------
    rule("A  THE AMPLITUDE CHANNEL: where the seesaw n actually lives (n = s_Lambda/a0 = 2 a0_DE/a0)")
    A1 = {}
    for k in ALL:
        A1[k] = {S["name"]: fit_a0(S["gN"][deepmask(S)], law(S["gN"][deepmask(S)], "DE"))[1] / A0_DE for S in (MIG, corp[k], HI)}
    out("  G158's amplitude fit (the alpha=1 quadratic) on noise-free law-exact data at the canonical footing, a0_fit/a0:")
    for k in ALL:
        out(f"    {k:12s} " + ", ".join(f"{s} {v:.3f}" for s, v in A1[k].items()) + "  -> its n_amp on exact n = 2 data: "
            + ", ".join(f"{N_DE / v:.2f}" for v in A1[k].values()))
    check("A1", "[injection] G158's alpha=1 amplitude fit returns a0 x (1.05-1.35) on law-exact canonical-footing data, for every sample and corpus: its n_amp reads LOW on exact n = 2 data",
          all(1.05 <= v <= 1.35 for k in ALL for v in A1[k].values()),
          "; ".join(f"{k} {min(A1[k].values()):.3f}-{max(A1[k].values()):.3f}" for k in ALL),
          "the lane's amplitude channel carries the alpha=1 form's bias (D01 D5); the kernel's own fit is below")
    A2 = {}
    AMP_FIXED = {"MIGHTEE": amp_nu(MIG), "HI": amp_nu(HI)}
    out("")
    out("  the in-force kernel's deep amplitude (deep rings only; galaxy bootstrap, 300 draws), both footings and the kill line n = 2.01:")
    out(f"    {'corpus':12s} {'sample':8s} {'a0 [1e-11]':>10s} {'a0/a0_DE':>8s} {'n':>6s} {'sigma_n':>7s} {'vs 2.000':>9s} {'vs 1.660':>9s} {'(2.01-n)/s':>10s} | G158 alpha=1 a0, n")
    for k in ALL:
        am = {"MIGHTEE": AMP_FIXED["MIGHTEE"], "SPARC": amp_nu(corp[k]), "HI": AMP_FIXED["HI"]}
        la = np.array([math.log(am[s]["a0"]) for s in am]); se = np.array([am[s]["se_ln"] for s in am])
        w = 1 / se ** 2; mean = float(np.sum(w * la) / np.sum(w)); chi2 = float(np.sum(w * (la - mean) ** 2))
        A2[k] = dict(per_sample=am, chi2=chi2, a0_joint=math.exp(mean), se_ln_joint=float(1 / math.sqrt(np.sum(w))))
        for s in am:
            v = am[s]
            g = REPRO[k][s]
            out(f"    {k:12s} {s:8s} {v['a0'] / 1e-11:10.2f} {v['a0'] / A0_DE:8.3f} {v['n']:6.3f} {v['sig_n']:7.3f} {(v['n'] - N_DE) / v['sig_n']:+8.1f}s "
                f"{(v['n'] - N_ALT) / v['sig_n']:+8.1f}s {(2.01 - v['n']) / v['sig_n']:+10.1f} | {g['a0_fit'] / 1e-11:.2f}, {N_DE * A0_DE / g['a0_fit']:.2f}"
                + ("  [GRID EDGE]" if v["edge"] else ""))
        nj = S_LAMBDA / A2[k]["a0_joint"]; snj = nj * A2[k]["se_ln_joint"]
        out(f"    {k:12s} {'JOINT':8s} {A2[k]['a0_joint'] / 1e-11:10.2f} {A2[k]['a0_joint'] / A0_DE:8.3f} {nj:6.3f} {snj:7.3f} {(nj - N_DE) / snj:+8.1f}s "
            f"{(nj - N_ALT) / snj:+8.1f}s {(2.01 - nj) / snj:+10.1f} | chi2 (df 2) = {chi2:.2f}")
        A2[k]["n_joint"], A2[k]["sig_n_joint"] = nj, snj
    check("A2", "[data] the three deep samples share ONE amplitude under the in-force kernel (chi2 < 9.21, df 2, p > 0.01), in every corrected corpus",
          all(A2[k]["chi2"] < 9.21 for k in CORRECTED),
          "; ".join(f"{k} chi2 {A2[k]['chi2']:.2f}" for k in CORRECTED) + f"; committed corpus chi2 {A2['committed']['chi2']:.2f}", lb=False)

    # ---------------- diagnosis (added after the first run) ----------------
    rule("DIAGNOSIS  (added after the first run, in which I1 and P1 failed as pre-stated; changes no pre-stated result and not the exit code)")
    def p_t2(t):                        # two-sided p of a t statistic with 2 degrees of freedom (closed form)
        return 1.0 - t / math.sqrt(t * t + 2.0)
    def gauss_eq(p):                    # two-sided p -> Gaussian-equivalent sigma
        lo, hi = 0.0, 40.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if math.erfc(mid / math.sqrt(2.0)) > p else (lo, mid)
        return 0.5 * (lo + hi)
    rd0 = {k: readings([MIG, corp[k], HI], [MIG["gO"], corp[k]["gO"], HI["gO"]]) for k in ALL}
    tl = abs(rd0["committed"]["z2_pg"]); tstd = tl * math.sqrt(2.0 / 3.0); t3 = 3.0 * math.sqrt(2.0 / 3.0)
    DG = dict(t_lane=tl, t_standard=tstd, p_committed=p_t2(tstd), gauss_committed=gauss_eq(p_t2(tstd)), p_line=p_t2(t3))
    out("  (1) G158's per-galaxy error is the spread of THREE sample values (numpy std, which divides by 3, then /sqrt 3).  Read as the")
    out(f"      lane's own error model, its 'sigma' is a t statistic with 2 degrees of freedom, inflated by sqrt(3/2): the committed {tl:.1f}")
    out(f"      is t = {tstd:.2f}, two-sided p = {DG['p_committed']:.4f}, {DG['gauss_committed']:.2f} sigma Gaussian-equivalent; its firing line '3 sigma' has a")
    out(f"      false-alarm rate of {100 * DG['p_line']:.1f} per cent, not 0.27.  (Against beta = 1 the paired bootstrap of D gives 6.0-6.9 sigma: P1.)")
    CAL = {}
    for k in ALL:
        rng = np.random.default_rng(424242)
        fp = fr = 0
        for _ in range(N_INJ):
            gOs = [inject(S, "DE", rng, NM[key], curve=lambda q: task_curve(q, A0_DE))
                   for S, key in ((MIG, "MIGHTEE"), (corp[k], "SPARC_" + k), (HI, "HI"))]
            rd = readings([MIG, corp[k], HI], gOs)
            fp += rd["fire_pg"]; fr += rd["fire_ring"]
        CAL[k] = dict(frac_fire_pg=fp / N_INJ, frac_fire_ring=fr / N_INJ)
    DG["calibration"] = CAL
    out("  (2) the same injections with G158's OWN mapped null exactly true (beta = n/2 = 1 at n = 2) against the framework's law exactly true:")
    for k in ALL:
        out(f"      {k:12s} fires {100 * CAL[k]['frac_fire_pg']:5.1f}% / {100 * CAL[k]['frac_fire_ring']:5.1f}% (per-galaxy / ring level) when beta = 1 is true;"
            f"  {100 * I1[k]['frac_fire_pg']:5.1f}% / {100 * I1[k]['frac_fire_ring']:5.1f}% when the law is true")
    out("      the firing separates beta = 1 from beta = 1/2.  It says nothing about n = 2.000 against n = 1.660, and its rate on its own null")
    out("      is the lane's real false-alarm rate.")
    out("  (3) where the REAL data's readings sit among the law-exact draws of I1 (percentile; 50 = typical of the law):")
    PCT = {}
    for k in ALL:
        dr = DRAWS[k]
        PCT[k] = dict(pg=float(100 * np.mean(dr["n_pg"] < rd0[k]["n_pg"])), ring=float(100 * np.mean(dr["n_ring"] < rd0[k]["n_ring"])))
        out(f"      {k:12s} per-galaxy reading n = {rd0[k]['n_pg']:.3f}: percentile {PCT[k]['pg']:5.1f} | ring level n = {rd0[k]['n_ring']:.3f}: percentile {PCT[k]['ring']:5.1f}"
            "  (I1 draws carry no mass-to-light scatter)")
    DG["percentiles"] = PCT
    out("  (4) why the per-galaxy reading misses some law-exact draws: the three-number error swells when one sample strays")
    for k in ALL:
        dr = DRAWS[k]; f = dr["fire_pg"].astype(bool)
        if (~f).any():
            out(f"      {k:12s} error 2*std/sqrt3: median {np.median(dr['s_pg'][f]):.3f} when firing, {np.median(dr['s_pg'][~f]):.3f} when not; spread of the three"
                f" slopes {np.median(dr['spread'][f]):.3f} vs {np.median(dr['spread'][~f]):.3f}; the HI slope's draw-to-draw std {np.std(dr['beta_hi']):.3f}")
    out("  (5) MIGHTEE's amplitude and its stellar mass-to-light convention (the survey's own refits, Table 3, via G167):")
    for lab, v in MIGHTEE_TABLE3.items():
        out(f"      {lab:42s} a0 = {v / 1e-11:6.2f}e-11 = {v / A0_DE:.3f} a0_DE  (n = {S_LAMBDA / v:.2f})")
    mg0 = AMP_FIXED["MIGHTEE"]
    fid = MIGHTEE_TABLE3["fiducial varying SED Ystar (median 0.36)"]; y06 = MIGHTEE_TABLE3["fixed Ystar_K = 0.6 (SPARC-class)"]
    out(f"      this script's kernel fit to the digitised deep rings: a0 = {mg0['a0'] / 1e-11:.2f}e-11, {100 * (mg0['a0'] / fid - 1):+.1f} per cent from the fiducial refit:")
    out("      the digitised deep rings carry the survey's fiducial convention.")
    WI = {}
    for k in CORRECTED:
        am = dict(A2[k]["per_sample"])
        am["MIGHTEE"] = dict(am["MIGHTEE"], a0=mg0["a0"] * y06 / fid)
        la = np.array([math.log(am[s_]["a0"]) for s_ in am]); se = np.array([am[s_]["se_ln"] for s_ in am])
        w = 1 / se ** 2; mean = float(np.sum(w * la) / np.sum(w)); chi2 = float(np.sum(w * (la - mean) ** 2))
        nj = S_LAMBDA / math.exp(mean); snj = nj / math.sqrt(np.sum(w))
        WI[k] = dict(n_joint=nj, sig_n=snj, z_DE=(nj - N_DE) / snj, z_ALT=(nj - N_ALT) / snj, chi2=chi2, a0_joint=math.exp(mean))
        out(f"      what-if {k:12s}: MIGHTEE rescaled by the survey's own Ystar_K = 0.6 refit ({y06 / fid:.3f}x) -> joint n = {nj:.2f} +/- {snj:.2f}"
            f" ({(nj - N_DE) / snj:+.1f} sigma from 2.000, {(nj - N_ALT) / snj:+.1f} from 1.660; a0 = {math.exp(mean) / A0_DE:.2f} a0_DE; chi2 {chi2:.2f})")
    out("      (a what-if: the survey refits all radii, and the digitised points carry no per-ring stellar mass to redo it on the deep window)")
    DG["mightee_ml"] = dict(table3=MIGHTEE_TABLE3, kernel_fit_digitised=mg0["a0"], what_if=WI)

    # ---------------- verdict ----------------
    rule("VERDICT")
    lbfail = [c["id"] for c in CH if c["load_bearing"] and not c["ok"]]
    rep = {c["id"]: c["ok"] for c in CH}
    rg = lambda xs, f="{:.1f}": (f.format(min(xs)) + "-" + f.format(max(xs))) if f.format(min(xs)) != f.format(max(xs)) else f.format(min(xs))
    if not MUTATE:
        c = CORRECTED
        spx = {k: A2[k]["per_sample"]["SPARC"] for k in c}
        mg = A2[c[0]]["per_sample"]["MIGHTEE"]
        vt = [
            "1. Row 11 does not test the framework's law.  The law's deep slope is 1/2 at both footings (M1); the rule n = 2*beta",
            "   assigns the canonical footing beta = 1, the Newtonian slope, which neither footing predicts.",
            f"   On data that obey the law exactly, row 11 fires in {rg([100 * I1[k]['frac_fire_pg'] for k in ALL], '{:.0f}')} per cent of draws (per-galaxy reading) and "
            f"{rg([100 * I1[k]['frac_fire_ring'] for k in ALL], '{:.0f}')} per cent (ring level).",
            "   " + ("I1 passed its pre-stated 95 per cent bar." if rep["I1"] else "I1 FAILED its pre-stated 95 per cent bar on the per-galaxy reading and stays FAIL."),
            f"   With its own mapped null true (beta = 1) it fires in {rg([100 * CAL[k]['frac_fire_pg'] for k in ALL])} / {rg([100 * CAL[k]['frac_fire_ring'] for k in ALL])} per cent,"
            " and between the two footings its reading moves",
            f"   {rg([I2[k]['diff'] for k in ALL], '{:.3f}')} against the 0.340 gap it claims to resolve (I2).  What fired is beta = 1, not n = 2.",
            f"2. The measured deep slope agrees with the law's own slope at the same points (D1 {'PASS' if rep['D1'] else 'FAIL'}: pooled z "
            + ", ".join(f"{D1[k]['pooled_z']:+.2f}" for k in c) + ").",
            f"   The data reject beta = 1 at {rg([P1[k]['z1'] for k in c])} sigma but a slope of 0.75 only at {rg([P1[k]['z075'] for k in c])} sigma"
            + (": P1 passed." if rep["P1"] else ": P1 FAILED as pre-stated."),
            "   The deep slope is consistent with the law; it is not yet a sharp confirmation of it.",
            f"3. The ring-pooled slope sits {rg([abs(D2[k]['z1']) for k in c])} sigma "
            + ("BELOW" if all(D2[k]["z1"] < 0 for k in c) else ("ABOVE" if all(D2[k]["z1"] > 0 for k in c) else "from"))
            + f" the law's own expectation, {'inside' if rep['D2'] else 'OUTSIDE'} the pre-stated 3 sigma (D2)"
            + (": a lean, not a failure." if rep["D2"] else ": a failure."),
            f"   Allowing 0.1 dex mass-to-light scatter moves z by at most {max(abs(D2[k]['z1'] - D2[k]['z0']) for k in c):.2f}.  On the committed corpus "
            f"it sat {abs(D2['committed']['z1']):.1f} sigma below, the kinematic mass-to-light artefact of D01-D02.",
            "4. The footing question lives in the amplitude.  With the in-force kernel the three deep samples "
            + ("share one amplitude" if rep["A2"] else "do NOT share one amplitude") + f" (A2: chi2 {rg([A2[k]['chi2'] for k in c])}, df 2).",
            f"   Jointly n = {rg([A2[k]['n_joint'] for k in c], '{:.2f}')} +/- {rg([A2[k]['sig_n_joint'] for k in c], '{:.2f}')}: "
            f"{rg([abs(A2[k]['n_joint'] - N_DE) / A2[k]['sig_n_joint'] for k in c])} sigma below the canonical n = 2.000 and "
            f"{rg([abs(A2[k]['n_joint'] - N_ALT) / A2[k]['sig_n_joint'] for k in c])} sigma below the alternative 1.660.",
            f"   SPARC alone (population ratios): n = {rg([spx[k]['n'] for k in c], '{:.2f}')}, within {rg([abs(spx[k]['n'] - N_DE) / spx[k]['sig_n'] for k in c])} sigma of 2.000.",
            f"   MIGHTEE alone (the survey's own baryonic masses): n = {mg['n']:.2f} +/- {mg['sig_n']:.2f}, {abs(mg['n'] - N_DE) / mg['sig_n']:.1f} sigma from 2.000 and "
            f"{abs(mg['n'] - N_ALT) / mg['sig_n']:.1f} from 1.660, statistical errors only.",
            f"   MIGHTEE's own refit at a SPARC-class Ystar_K = 0.6 gives a0 = 1.08e-10 = {1.08e-10 / A0_DE:.2f} a0_DE (Table 3 via G167); with MIGHTEE put there,",
            f"   the joint becomes n = {rg([DG['mightee_ml']['what_if'][k]['n_joint'] for k in c], '{:.2f}')}: {rg([abs(DG['mightee_ml']['what_if'][k]['z_DE']) for k in c])} sigma from 2.000 and "
            f"{rg([abs(DG['mightee_ml']['what_if'][k]['z_ALT']) for k in c])} from 1.660 (DIAGNOSIS 5, a what-if).",
            "   The deep amplitude sits between the two footings and is set by the stellar mass-to-light convention.  No sample sits above the n = 2.01 subluminality line.",
            f"5. G158's '12.7 sigma' is a t statistic with 2 degrees of freedom: p = {DG['p_committed']:.4f}, {DG['gauss_committed']:.1f} sigma Gaussian-equivalent (DIAGNOSIS 1).",
        ]
    else:
        vt = ["MUTATE control: the law under test was replaced by the task-declared curve beta = n/2.  The checks that say row 11",
              "does not test the law must fail: " + ", ".join(f"{i} {'PASS' if rep[i] else 'FAIL'}" for i in ("M1", "I1", "I2", "D1", "D2", "A1")) + "."]
    for s in vt:
        out("  " + s)
    npass = sum(c["ok"] for c in CH)
    out("")
    out(f"  {npass}/{len(CH)} checks pass; load-bearing failures: {len(lbfail)}" + ("  (MUTATE: M1, I1, I2, D1, A1 must fail)" if MUTATE else ""))
    out(f"  runtime {time.time() - t0:.0f} s")
    res = dict(script="D04_g158_slope_channel.py", mutate=MUTATE, footings=dict(canonical=A0_DE, alternative=A0_ALT, n_canonical=N_DE, n_alternative=N_ALT),
               noise_model=NM, I1=I1, I2=I2, D1=D1, P1=P1, D2=D2, A1=A1, diagnosis=DG,
               A2={k: dict(chi2=v["chi2"], a0_joint=v["a0_joint"], n_joint=v["n_joint"], sig_n_joint=v["sig_n_joint"],
                           per_sample={s: {kk: vv for kk, vv in d.items()} for s, d in v["per_sample"].items()}) for k, v in A2.items()},
               checks=[{kk: c[kk] for kk in ("id", "claim", "ok", "load_bearing", "measured")} for c in CH],
               load_bearing_failures=lbfail, verdict=vt)
    fn = "D04_results_MUTATE.json" if MUTATE else "D04_results.json"
    json.dump(res, open(os.path.join(HERE, fn), "w"), indent=1, default=float)
    return 0 if not lbfail else 1

if __name__ == "__main__":
    sys.exit(main())
