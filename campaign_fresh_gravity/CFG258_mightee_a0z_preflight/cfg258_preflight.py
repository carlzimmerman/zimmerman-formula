#!/usr/bin/env python3
"""CFG258 -- a BLIND pre-flight (mocks only, nothing downloaded) of what the public MIGHTEE-HI / LADUMA RAR sample (arXiv:2608.03576; 130 resolved HI galaxies to z ~ 0.09) could say about
FLAT a0, the rival a0 ~ H(z) and the anchored slope a1 = (5.23 +- 1.05)e-10 per unit z.   Criteria frozen and committed before this script existed: FROZEN_CRITERIA.md (a88864716).
kappa = 1/2 is FITTED.  Kernel nu_mono (FP1's, through CFG4_common); both footings.  SPARC-resampled mocks; E1 = the anchored (fixed-anchor) slope, E2 = the within-sample slope; the statistic is the TOTAL scatter over
mocks with the shared systematics of the declared budget included (the CFG219 lesson).  Every MIGHTEE-like number is a declared scenario (UNVERIFIED); no MIGHTEE number except the quoted a1 is used.
Run: python3 campaign_fresh_gravity/CFG258_mightee_a0z_preflight/cfg258_preflight.py            [MUTATE=1: a planted shared offset equal to (iii); MUTATE=2: shared draws removed (C4 must FAIL)]
     CFG258_QUICK=1 runs a small smoke version (not a result; outputs named *_QUICK)."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG4_common as C4

MUT = os.environ.get("MUTATE", "").strip()
QUICK = os.environ.get("CFG258_QUICK", "") == "1"
SFX = ("_QUICK" if QUICK else "") + (f"_MUTATE{MUT}" if MUT else "")
T0 = time.time()
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


LN10 = math.log(10.0)
KMS2KPC = 1e6 / 3.0856775814913673e19                         # g [m s^-2] = KMS2KPC * V|V| [km^2 s^-2] / R [kpc]
C_KMS = 299792.458
FOOTS = ("canonical", "alt")
A0 = C4.A0
nu = C4.nu_mono
A1, A1E = 5.23e-10, 1.05e-10
B3 = {f: A1 / A0[f] for f in FOOTS}
UPS, BUL, SIG_INT = 0.6, 1.4, 0.06
Efun = lambda z: np.sqrt(0.315 * (1 + np.asarray(z, float)) ** 3 + 0.685)
SEED = 258


def law(truth, foot):
    if truth == "FLAT":
        return lambda z: np.ones_like(np.asarray(z, float))
    if truth == "RIVAL":
        return Efun
    b3 = {"ANCH": A1, "ANCH_LO": A1 - A1E, "ANCH_HI": A1 + A1E}[truth] / A0[foot]
    return lambda z: 1.0 + b3 * np.asarray(z, float)


# ================================================================================================ the template pool (SPARC)
class Pool:
    pass


def build_pool(custom=None):
    p = Pool()
    if custom is not None:
        for k, v in custom.items():
            setattr(p, k, v)
        return p
    gal = C4.load_sparc()
    keep = [g for g in gal if g["meta"] and g["meta"]["Q"] <= 2 and 30 <= g["meta"]["Inc"] <= 85]
    cols = {k: [] for k in ("R", "vobs", "ev", "g_gas", "g_dsk", "g_blg", "gal")}
    gstart, gn, meta = [], [], []
    for gi, g in enumerate(keep):
        R, Vo, eV = np.asarray(g["R"], float), np.asarray(g["Vobs"], float), np.asarray(g["eV"], float)
        gg = KMS2KPC * g["Vgas"] * np.abs(g["Vgas"]) / R
        gd = KMS2KPC * g["Vdisk"] * np.abs(g["Vdisk"]) / R
        gb = KMS2KPC * g["Vbul"] * np.abs(g["Vbul"]) / R
        gbar = gg + UPS * (gd + BUL * gb)
        ok = (R > 0) & np.isfinite(Vo) & (Vo > 0) & np.isfinite(eV) & np.isfinite(gbar) & (gbar > 0)
        if ok.sum() < 3:
            continue
        gstart.append(sum(len(c) for c in cols["R"])); gn.append(int(ok.sum()))
        cols["R"].append(R[ok]); cols["vobs"].append(Vo[ok]); cols["ev"].append(eV[ok])
        cols["g_gas"].append(gg[ok]); cols["g_dsk"].append(gd[ok]); cols["g_blg"].append(gb[ok]); cols["gal"].append(np.full(int(ok.sum()), len(gstart) - 1))
        m = g["meta"]
        meta.append(dict(name=g["name"], Inc=m["Inc"], eInc=m["eInc"], D=m["D"], eD=m["eD"], T=m["T"], Vflat=m["Vflat"], L36=m["L36"], MHI=m["MHI"], Q=m["Q"]))
    for k in cols:
        setattr(p, k if k != "gal" else "gal_of_pt", np.concatenate(cols[k]))
    p.rel = np.clip(p.ev / p.vobs, 0.01, 0.5)
    p.gstart, p.gn = np.array(gstart), np.array(gn)
    p.ngal, p.npts = len(gn), int(sum(gn))
    p.cot_i = np.array([1.0 / math.tan(math.radians(m["Inc"])) for m in meta])
    p.einc = np.array([math.radians(m["eInc"]) for m in meta])
    p.eD_frac = np.array([m["eD"] / m["D"] if m["D"] > 0 else 0.1 for m in meta])
    p.meta = meta
    return p


# ================================================================================================ the sample generator and the analyst's fit
def zdraw(rng, n, spec):
    kind, lo, hi = spec
    if kind == "U":
        return rng.uniform(lo, hi, n)
    return (lo ** 3 + rng.random(n) * (hi ** 3 - lo ** 3)) ** (1 / 3)          # density ~ z^2


KNOBS = ("tauML", "taugas", "tauD", "tauV", "tausel", "kapV", "kapsel", "kapML")
BUDGET = {"A": dict(tauML=0.05, taugas=0.02, tauD=0.015, tauV=0.01, tausel=0.02, kapV=0.01, kapsel=0.02, kapML=0.03),
          "B": dict(tauML=0.15, taugas=0.06, tauD=0.04, tauV=0.03, tausel=0.08, kapV=0.03, kapsel=0.06, kapML=0.08)}
ZERO = {k: 0.0 for k in KNOBS}


def draw_shared(rng, level):
    if level is None or MUT == "2":
        return dict(ZERO)
    return {k: float(rng.normal(0, BUDGET[level][k] / 2)) for k in KNOBS}


def gen(pool, rng, kind, foot, truth, cell, sh=ZERO, noiseless=False, lam=1.0):
    """one sample as the ANALYST sees it: (logg, gbar, z, w, inst) -- for kind 'S' (the anchor, z = 0) or 'M' (the MIGHTEE-like sample)"""
    if kind == "S":
        pt = np.arange(pool.npts); inst = pool.gal_of_pt; z_inst = np.zeros(pool.ngal); t_of_inst = np.arange(pool.ngal)
        rel = pool.rel.copy(); n_inst = pool.ngal
        sd_ups, sd_inc, sd_D = 0.10, pool.einc, pool.eD_frac
        u_pt = np.zeros(pt.size); a0_truth_scale = np.ones(pt.size); sh = ZERO
    else:
        n_inst = cell["N"]
        t_of_inst = rng.integers(0, pool.ngal, n_inst)
        z_inst = zdraw(rng, n_inst, cell["z"])
        sel = []
        for j, t in enumerate(t_of_inst):
            s, n = pool.gstart[t], pool.gn[t]
            if cell["pts"] == "all" or n <= 6:
                idx = np.arange(s, s + n)
            elif cell["pts"] == "rand6":
                idx = s + np.sort(rng.choice(n, 6, replace=False))
            else:                                                               # the 6 outermost
                idx = np.arange(s + n - 6, s + n)
            sel.append(idx)
        pt = np.concatenate(sel); inst = np.repeat(np.arange(n_inst), [len(i) for i in sel])
        rel = np.full(pt.size, cell["sv"])
        sd_ups = 0.15 * lam; sd_inc = np.full(n_inst, math.radians(5.0) * lam)
        sd_D = np.sqrt((250.0 / (C_KMS * z_inst)) ** 2 + (0.03 * lam) ** 2)
        zlo, zhi = cell["z"][1], cell["z"][2]
        z_pt = z_inst[inst]
        u_pt = (z_pt - 0.5 * (zlo + zhi)) / (zhi - zlo)
        f_T = law(truth, foot)
        a0_truth_scale = f_T(z_pt) * 10.0 ** (sh["tausel"] + sh["kapsel"] * u_pt)
    z_pt = z_inst[inst]
    if kind == "S":
        rel = pool.rel[pt]
    gs = pool.g_gas[pt]; gstar = pool.g_dsk[pt] + BUL * pool.g_blg[pt]
    gbar_true = gs + UPS * gstar
    a0z = A0[foot] * a0_truth_scale
    logg = np.log10(gbar_true * nu(gbar_true / a0z))
    if not noiseless:
        eps_ups = rng.normal(0, sd_ups, n_inst)
        dinc = rng.normal(0, 1, n_inst) * sd_inc
        eps_D = rng.normal(0, 1, n_inst) * sd_D
        logg = logg + rng.normal(0, SIG_INT, pt.size) + 2 * np.log10(np.clip(1 + rng.normal(0, 1, pt.size) * rel, 0.3, None)) \
            + 2 * np.log10(np.clip(1 + pool.cot_i[t_of_inst][inst] * dinc[inst], 0.3, None)) - np.log10(np.clip(1 + eps_D[inst], 0.3, None))
        tauML_pt = sh["tauML"] + sh["kapML"] * u_pt + eps_ups[inst]
    else:
        tauML_pt = sh["tauML"] + sh["kapML"] * u_pt
    logg = logg + 2 * (sh["tauV"] + sh["kapV"] * u_pt) - sh["tauD"]
    gbar_an = gs * 10.0 ** sh["taugas"] + UPS * gstar * 10.0 ** tauML_pt
    ok = gbar_an > 0
    w = 1.0 / ((2 * rel / LN10) ** 2 + SIG_INT ** 2)
    return dict(logg=logg[ok], gbar=gbar_an[ok], z=z_pt[ok], w=w[ok], inst=inst[ok], n_inst=n_inst)


H_DER = 1e-3


def fit(s, theta0, mode, theta_fixed=None, b0=0.0, cnt=None, iters=8):
    """Gauss-Newton on log10 a0(z) = theta + log10(1 + b z): modes 'E2' (theta, b), 'E1' (b only, theta fixed), 'th' (theta only, b = 0); returns (theta, b, sigma_b_formal)"""
    logg, gbar, z, w = s["logg"], s["gbar"], s["z"], s["w"]
    if cnt is not None:
        w = w * cnt[s["inst"]]
    lgb = np.log10(gbar)
    th = theta0 if theta_fixed is None else theta_fixed
    b = b0 if mode != "th" else 0.0
    sig_b = np.nan
    for _ in range(iters):
        a0z = 10.0 ** th * (1 + b * z)
        ly = lgb - np.log10(a0z)
        mod = lgb + np.log10(nu(10.0 ** ly))
        r = logg - mod
        L = -(np.log10(nu(10.0 ** (ly + H_DER))) - np.log10(nu(10.0 ** (ly - H_DER)))) / (2 * H_DER)
        Jb = L * z / ((1 + b * z) * LN10)
        if mode == "E2":
            JtWJ = np.array([[np.sum(w * L * L), np.sum(w * L * Jb)], [np.sum(w * L * Jb), np.sum(w * Jb * Jb)]])
            JtWr = np.array([np.sum(w * L * r), np.sum(w * Jb * r)])
            try:
                d = np.linalg.solve(JtWJ, JtWr)
                cov = np.linalg.inv(JtWJ); sig_b = math.sqrt(max(cov[1, 1], 0.0))
            except np.linalg.LinAlgError:
                return np.nan, np.nan, np.nan
            d = np.clip(d, [-0.3, -5.0], [0.3, 5.0])
            th += d[0]; b += d[1]
        elif mode == "E1":
            den = np.sum(w * Jb * Jb)
            if den <= 0:
                return th, np.nan, np.nan
            d = np.clip(np.sum(w * Jb * r) / den, -5.0, 5.0); b += d; sig_b = 1.0 / math.sqrt(den)
        else:
            den = np.sum(w * L * L); d = np.clip(np.sum(w * L * r) / den, -0.3, 0.3); th += d; sig_b = np.nan
        if abs(d if np.isscalar(d) else d[0]) < 1e-11 and (mode != "E2" or abs(d[1]) < 1e-11):
            break
    return th, b, sig_b


# ================================================================================================ pool, anchor library, cells
POOL = build_pool()
CELLS = {
    "C0": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=130, lam=1.0),
    "C1": dict(foot="alt", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=130, lam=1.0),
    "C2": dict(foot="canonical", z=("V", 0.02, 0.09), pts="rand6", sv=0.07, N=130, lam=1.0),
    "C3": dict(foot="canonical", z=("U", 0.005, 0.09), pts="rand6", sv=0.07, N=130, lam=1.0),
    "C4": dict(foot="canonical", z=("U", 0.02, 0.09), pts="all", sv=0.07, N=130, lam=1.0),
    "C5": dict(foot="canonical", z=("U", 0.02, 0.09), pts="out6", sv=0.07, N=130, lam=1.0),
    "C6": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.04, N=130, lam=1.0),
    "C7": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.12, N=130, lam=1.0),
    "C8": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=260, lam=1.0),
    "C9": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=520, lam=1.0),
    "C10": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=1040, lam=1.0),
    "C11": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=130, lam=None),             # AM: lambda solved (the anchor library)
    "C11b": dict(foot="canonical", z=("U", 0.02, 0.09), pts="rand6", sv=0.07, N=130, lam=None, anchor="canonical_formal"),   # POST HOC: AM with the anchor's FORMAL error (0.0072 dex)
    "C12": dict(foot="canonical", z=("U", 0.02, 0.30), pts="rand6", sv=0.07, N=130, lam=1.0),
}
NS_LIB = 150 if QUICK else 1500
M_MAIN, M_OTHER = (300, 150) if QUICK else (10000, 4000)


def anchor_library(foot, ns):
    rng = np.random.default_rng(np.random.SeedSequence([SEED, 7, FOOTS.index(foot)]))
    out = np.empty(ns)
    for i in range(ns):
        s = gen(POOL, rng, "S", foot, "FLAT", None)
        out[i] = fit(s, math.log10(A0[foot]), "th")[0] - math.log10(A0[foot])
    return out


ANCHOR = {}


# ================================================================================================ the Monte-Carlo run (one task = one cell, one truth, one budget level)
def mc_task(args):
    cname, foot, truth, level, M, seed, plant, lam = args
    cell = CELLS[cname]
    rng = np.random.default_rng(seed)
    th0 = math.log10(A0[foot])
    lib = ANCHOR[cell.get("anchor", foot)]
    b1, b2, f1, f2, th2 = (np.empty(M) for _ in range(5))
    for m_ in range(M):
        sh = draw_shared(rng, level)
        if plant:
            sh = dict(sh); sh["tauML"] += plant
        s = gen(POOL, rng, "M", foot, truth, cell, sh=sh, lam=lam)
        thS = th0 + lib[rng.integers(len(lib))]
        r2 = fit(s, th0, "E2"); r1 = fit(s, th0, "E1", theta_fixed=thS)
        b1[m_], f1[m_], b2[m_], f2[m_], th2[m_] = r1[1], r1[2], r2[1], r2[2], r2[0] - th0
    return dict(b1=b1, f1=f1, b2=b2, f2=f2, th2=th2)


def summ(a):
    a = a[np.isfinite(a)]
    return dict(mean=float(a.mean()), sd=float(a.std(ddof=1)), p5=float(np.percentile(a, 5)), p95=float(np.percentile(a, 95)), n=int(a.size))


# ================================================================================================ noiseless responses (levers, S_joint, mimic offsets)
def design_cell(cell):
    return dict(cell, N=1000)


def nl_fit(cell, foot, truth, sh, mode, seed=2581, pool=None, design=True):
    m = gen(pool or POOL, np.random.default_rng(seed), "M", foot, truth, design_cell(cell) if design else cell, sh=sh, noiseless=True)
    th0 = math.log10(A0[foot])
    if mode == "E1":
        return fit(m, th0, "E1", theta_fixed=th0)[1]
    if mode == "E2":
        return fit(m, th0, "E2")[1]
    return fit(m, th0, "th")[0] - th0


def levers(cell, foot, pool=None, design=True):
    out = {}
    for k in KNOBS[:5]:
        h = 0.02
        sp = dict(ZERO); sp[k] = h; sm = dict(ZERO); sm[k] = -h
        out[k] = (nl_fit(cell, foot, "FLAT", sp, "th", pool=pool, design=design) - nl_fit(cell, foot, "FLAT", sm, "th", pool=pool, design=design)) / (2 * h)
    return out


def s_joint(cell, foot, level):
    """the aligned worst case: sum over the 8 knobs, each at its half-range, of |b_hat(knob) - b_hat(0)| for E1 and E2 (noiseless, FLAT truth)"""
    b0 = {m: nl_fit(cell, foot, "FLAT", dict(ZERO), m) for m in ("E1", "E2")}
    tot, per = {"E1": 0.0, "E2": 0.0}, {}
    for k in KNOBS:
        sh = dict(ZERO); sh[k] = BUDGET[level][k]
        per[k] = {m: nl_fit(cell, foot, "FLAT", sh, m) - b0[m] for m in ("E1", "E2")}
        for m in ("E1", "E2"):
            tot[m] += abs(per[k][m])
    return tot, per


def mimic(cell, foot, zbar):
    from scipy.optimize import brentq
    target = math.log10(1 + B3[foot] * zbar)
    out = {}
    for k in KNOBS[:5]:
        def f(t):
            sh = dict(ZERO); sh[k] = t
            return nl_fit(cell, foot, "FLAT", sh, "th") - target
        try:
            out[k] = brentq(f, -0.9, 0.9, xtol=1e-6)
        except ValueError:
            out[k] = None
    return out, target


def plant_offset(cell, foot):
    """the shared stellar-mass-scale offset whose noiseless E1 slope equals b3 (MUTATE=1's plant)"""
    from scipy.optimize import brentq
    f = lambda t: nl_fit(cell, foot, "FLAT", dict(ZERO, tauML=t), "E1") - B3[foot]
    return brentq(f, -0.9, 0.05, xtol=1e-7)                                     # the offset is NEGATIVE (assumed stellar masses too low); +-1.5 dex breaks the fit (NaN) in the first MUTATE=1 attempt, which crashed before writing anything


# ================================================================================================ decisions
def decide(stats, SJ, M_note=""):
    """R1 / R2 per estimator, level and law; stats[run] = {'b1': summ, 'b2': summ} for run keys FLAT_off, RIVAL_off, ANCH_off, FLAT_A, ..."""
    res = {}
    for est, key in (("E1", "b1"), ("E2", "b2")):
        sd_stat = stats["FLAT_off"][key]["sd"]
        for law in ("RIVAL", "ANCH"):
            delta = stats[f"{law}_off"][key]["mean"] - stats["FLAT_off"][key]["mean"]
            for lv in ("A", "B"):
                r1 = stats[f"{law}_{lv}"][key]["p5"] > stats[f"FLAT_{lv}"][key]["p95"]
                sj = SJ[lv][est]
                r2 = delta > sj + 2 * sd_stat
                sd_tot = stats[f"FLAT_{lv}"][key]["sd"]
                sd_sys = math.sqrt(max(sd_tot ** 2 - sd_stat ** 2, 0.0))
                sig_req = delta / 3.29
                if sd_sys >= sig_req:
                    n_req = None
                else:
                    n_req = None  # filled by the caller (needs N)
                res[(est, law, lv)] = dict(delta=delta, sd_stat=sd_stat, sd_tot=sd_tot, sd_sys=sd_sys, S_joint=sj, R1=bool(r1), R2=bool(r2), possible=bool(r1 and r2),
                                           why="" if (r1 and r2) else ("R1" if not r1 else "") + ("+" if (not r1 and not r2) else "") + ("R2" if not r2 else ""),
                                           sig_req=sig_req, unreachable=bool(sd_sys >= sig_req), min_detectable=max(3.29 * sd_tot, sj + 2 * sd_stat))
    return res


# ================================================================================================ the controls' helpers
def synthetic_pool(kind):
    """a one-galaxy deep-regime template (y = 1e-8): 'gas' (gas only) or 'star' (stellar disc only)"""
    n = 40
    a0 = A0["canonical"]
    g = 1e-8 * a0 * np.ones(n)
    z = np.zeros(n)
    custom = dict(npts=n, ngal=1, gal_of_pt=np.zeros(n, int), g_gas=g if kind == "gas" else z, g_dsk=(g / UPS) if kind == "star" else z, g_blg=z, rel=np.full(n, 0.05), cot_i=np.array([0.5]),
                  einc=np.array([0.05]), eD_frac=np.array([0.1]), gstart=np.array([0]), gn=np.array([n]), R=np.linspace(1, 10, n), vobs=np.full(n, 100.0), ev=np.full(n, 5.0), meta=[dict(T=5, Vflat=100.0)])
    return build_pool(custom)


def blind_and_tot(level, foot, M_b=150, B=60, seed=4242):
    """the CFG219 reactivity control: Z_tot = signal / total scatter (supplied by the caller) is NOT computed here; this returns the BLIND statistic = the median over mocks of b_A / (the within-mock galaxy-bootstrap sd of b_A)"""
    cell = CELLS["C0"]
    rng = np.random.default_rng(seed)
    th0 = math.log10(A0[foot]); lib = ANCHOR[foot]
    ratios = []
    for _ in range(M_b):
        sh = draw_shared(rng, level)
        s = gen(POOL, rng, "M", foot, "ANCH", cell, sh=sh)
        thS = th0 + lib[rng.integers(len(lib))]
        b = fit(s, th0, "E1", theta_fixed=thS)[1]
        bs = []
        for _b in range(B):
            cnt = np.bincount(rng.integers(0, s["n_inst"], s["n_inst"]), minlength=s["n_inst"])
            bs.append(fit(s, th0, "E1", theta_fixed=thS, cnt=cnt)[1])
        ratios.append(b / np.std(bs, ddof=1))
    return float(np.median(ratios))


def solve_lambda(anchor_key, target=A1E, M=2000, seed=9999):
    """lambda such that SD(E1 b | FLAT, shared OFF) * a0(canonical) = target (the authors' formal sigma(a1)); None if unreachable even at lambda = 0"""
    CELLS["CAM"] = dict(CELLS["C0"], anchor=anchor_key)

    def sd1(lam):
        r = mc_task(("CAM", "canonical", "FLAT", None, M, seed, None, lam))
        return float(np.std(r["b1"], ddof=1)) * A0["canonical"]
    lo, hi = 0.0, 8.0
    f0 = sd1(lo)
    if f0 > target:
        return None, f0
    if sd1(hi) < target:
        return float("inf"), f0
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        v = sd1(mid)
        if abs(v / target - 1) < 0.02:
            return mid, v
        lo, hi = (mid, hi) if v < target else (lo, mid)
    return 0.5 * (lo + hi), sd1(0.5 * (lo + hi))


def real_sparc_theta(gal_idx, foot="canonical", boot=200, seed=77):
    """C8 (post hoc): the fitted log10 a0 of the REAL SPARC points of the template galaxies `gal_idx` (b = 0, the analyst's weights, Upsilon fixed at the mock truth), with a galaxy-bootstrap sd"""
    mask = np.isin(POOL.gal_of_pt, gal_idx)
    lgo = np.log10(KMS2KPC * POOL.vobs[mask] ** 2 / POOL.R[mask])
    gbar = POOL.g_gas[mask] + UPS * (POOL.g_dsk[mask] + BUL * POOL.g_blg[mask])
    w = 1.0 / ((2 * POOL.rel[mask] / LN10) ** 2 + SIG_INT ** 2)
    base = dict(logg=lgo, gbar=gbar, z=np.zeros(mask.sum()), w=w, inst=POOL.gal_of_pt[mask])
    th0 = math.log10(A0[foot])
    th = fit(base, th0, "th")[0]
    rng = np.random.default_rng(seed)
    gl = np.array(sorted(set(gal_idx.tolist())))
    ths = []
    for _ in range(boot):
        cnt = np.zeros(POOL.ngal); np.add.at(cnt, rng.choice(gl, gl.size), 1)
        ths.append(fit(dict(base), th0, "th", cnt=cnt)[0])
    return th - th0, float(np.std(ths, ddof=1)), int(gl.size)


# ================================================================================================ the run
CELL_ORDER = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C11b", "C12"]


def runs_for(cname):
    if MUT == "1":
        return [("FLAT", None), ("ANCH", None), ("PLANT", None), ("FLAT", "B"), ("ANCH", "B"), ("PLANT", "B")]
    base = [("FLAT", None), ("RIVAL", None), ("ANCH", None), ("FLAT", "A"), ("FLAT", "B"), ("RIVAL", "A"), ("RIVAL", "B"), ("ANCH", "A"), ("ANCH", "B")]
    if cname == "C0":
        base += [("ANCH_LO", "B"), ("ANCH_HI", "B")]
    return base


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def main():
    CK = {}

    def check(name, ok, detail=""):
        CK[name.split()[0]] = bool(ok)
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))

    RES = {}
    P("CFG258 -- a BLIND pre-flight of the MIGHTEE-HI / LADUMA RAR sample: FLAT a0 against a0 ~ H(z) and against the anchored slope (mocks only; nothing downloaded; criteria frozen in a88864716)"
      + (f"   *** MUTATE={MUT}: " + {"1": "a planted shared offset equal to (iii): it must be detected by E1 and attributed to an offset by E2", "2": "the shared draws removed (a statistic blind to shared systematics): C4 must FAIL"}[MUT] + " ***" if MUT else "")
      + ("   [QUICK smoke version: not a result]" if QUICK else ""))
    P(f"pool: {POOL.ngal} SPARC template galaxies, {POOL.npts} points; mock truth Upsilon_disc {UPS}, bulge {BUL * UPS}; sigma_int {SIG_INT} dex; kernel nu_mono; footings {A0}")
    t = time.time()
    for foot in FOOTS:
        ANCHOR[foot] = anchor_library(foot, NS_LIB)
        P(f"anchor library {foot}: {NS_LIB} realizations, theta_S - truth: mean {ANCHOR[foot].mean():+.4f} dex, sd {ANCHOR[foot].std(ddof=1):.4f} dex  ({time.time() - t:.0f} s)")
    ANCHOR["canonical_formal"] = ANCHOR["canonical"].mean() + 0.0072 * np.random.default_rng(SEED + 99).normal(size=NS_LIB)
    RES["anchor"] = {f: dict(mean=float(ANCHOR[f].mean()), sd=float(ANCHOR[f].std(ddof=1))) for f in FOOTS}

    # ------------------------------------------------------------------ Part A and C1: the laws and what (iii) implies
    P("\nPART A  WHAT THE ANCHORED CLAIM IMPLIES (arithmetic; a1 = 5.23e-10 +- 1.05e-10 m/s2 per unit z, quoted, not verified)")
    zs = (0.02, 0.03, 0.05, 0.055, 0.07, 0.09)
    PA = {}
    for foot in FOOTS:
        b3 = B3[foot]
        PA[foot] = {z: dict(f_iii=1 + b3 * z, dex_iii=math.log10(1 + b3 * z), f_rival=float(Efun(z)), dex_rival=math.log10(float(Efun(z)))) for z in zs}
        P(f"  {foot:9s} b3 = a1/a0 = {b3:.4f} (+-{A1E / A0[foot]:.4f}); " + "; ".join(f"z={z}: x{PA[foot][z]['f_iii']:.3f} ({PA[foot][z]['dex_iii']:+.3f} dex) vs rival x{PA[foot][z]['f_rival']:.3f}" for z in (0.02, 0.055, 0.09)))
    off = {foot: {zb: math.log10(1 + B3[foot] * zb) for zb in (0.04, 0.055, 0.07)} for foot in FOOTS}
    P("  sample-minus-anchor a0 offset implied at mean z 0.04 / 0.055 / 0.07: " + "; ".join(f"{f}: " + " / ".join(f"{v:+.4f}" for v in off[f].values()) + " dex" for f in FOOTS))
    ok1 = (abs(B3["canonical"] - 5.5874) < 1e-3 and abs(B3["alt"] - 4.6234) < 1e-3 and abs(float(Efun(0.09)) - 1.0454) < 1e-3 and abs(PA["canonical"][0.09]["f_iii"] - 1.5029) < 1e-3
           and abs(PA["alt"][0.09]["f_iii"] - 1.4161) < 1e-3 and abs(off["canonical"][0.055] - 0.1164) < 1e-3 and abs(off["alt"][0.055] - 0.0984) < 1e-3 and abs(off["canonical"][0.04] - 0.0876) < 1e-3)
    check("C1 CONTROL: the script's b3, E(z) and the implied changes equal the frozen arithmetic (section 0) to 1e-3", ok1, f"b3 {B3['canonical']:.4f} / {B3['alt']:.4f}; E(0.09) {float(Efun(0.09)):.4f}; x{PA['canonical'][0.09]['f_iii']:.4f}")
    RES["part_a"] = {f: {str(z): v for z, v in PA[f].items()} for f in FOOTS}; RES["offsets"] = {f: {str(k): v for k, v in off[f].items()} for f in FOOTS}

    # ------------------------------------------------------------------ C2 noiseless consistency, C3 deep-limit levers
    P("\nCONTROLS (noiseless)")
    from scipy.optimize import least_squares
    c2 = []
    for foot in FOOTS:
        th0 = math.log10(A0[foot]); cell = CELLS["C0"]
        s_ = gen(POOL, np.random.default_rng(1), "S", foot, "FLAT", None, noiseless=True)
        c2.append(abs(fit(s_, th0 + 0.1, "th")[0] - th0))
        for truth in ("FLAT", "ANCH"):
            m = gen(POOL, np.random.default_rng(5), "M", foot, truth, design_cell(cell), noiseless=True)
            r2, r1 = fit(m, th0 + 0.05, "E2"), fit(m, th0, "E1", theta_fixed=th0)
            tb = 0.0 if truth == "FLAT" else B3[foot]
            c2 += [abs(r2[0] - th0), abs(r2[1] - tb) / max(abs(tb), 1.0), abs(r1[1] - tb) / max(abs(tb), 1.0)]
        m = gen(POOL, np.random.default_rng(5), "M", foot, "RIVAL", design_cell(cell), noiseless=True)
        r2 = fit(m, th0, "E2")
        def resid(p_):
            a0z = 10.0 ** p_[0] * (1 + p_[1] * m["z"])
            return np.sqrt(m["w"]) * (m["logg"] - (np.log10(m["gbar"]) + np.log10(nu(m["gbar"] / a0z))))
        ls = least_squares(resid, [th0, 0.0], xtol=1e-14, ftol=1e-14, gtol=1e-14)
        c2.append(abs(r2[1] - ls.x[1]) / abs(ls.x[1]))
    check("C2 CONTROL: with every random and shared term OFF, FLAT gives theta = log10 a0 and b = 0 (1e-8), ANCH gives b = b3 (1e-6), and RIVAL's E2 slope equals an independent scipy least-squares fit (1e-3), both footings",
          max(c2) < 1e-3 and sorted(c2)[-2] < 1e-3, f"largest deviation {max(c2):.2e} (the RIVAL comparison); the others <= {sorted(c2)[-2]:.1e}")
    deep = {}
    for kind, knobs in (("gas", ("taugas", "tauD", "tauV", "tausel")), ("star", ("tauML",))):
        sp_ = synthetic_pool(kind)
        cdeep = dict(CELLS["C0"], N=40, pts="all")
        for k in knobs:
            h = 0.01
            sp1, sm1 = dict(ZERO, **{k: h}), dict(ZERO, **{k: -h})
            deep[k] = (nl_fit(cdeep, "canonical", "FLAT", sp1, "th", pool=sp_, design=False) - nl_fit(cdeep, "canonical", "FLAT", sm1, "th", pool=sp_, design=False)) / (2 * h)
    want = dict(tauML=-1.0, taugas=-1.0, tauD=-2.0, tauV=4.0, tausel=1.0)
    check("C3 CONTROL: on a synthetic deep-regime sample (y = 1e-8) the finite-difference levers are -1 (tauML, stars only), -1 (taugas), -2 (tauD), +4 (tauV), +1 (tausel) to 1e-3",
          all(abs(deep[k] - want[k]) < 1e-3 for k in want), "; ".join(f"{k} {deep[k]:+.5f}" for k in want))
    RES["deep_levers"] = deep

    # ------------------------------------------------------------------ the noiseless responses: levers, S_joint, mimic
    P("\nPART B  LEVERS AND THE OFFSETS THAT MIMIC (iii) (noiseless fits on a 1,000-galaxy design; dex of log10 a0 per dex of knob)")
    SJ, LEV, MIM = {}, {}, {}
    for cname in CELL_ORDER:
        cell = CELLS[cname]
        if cname in ("C11", "C11b"):
            continue
        SJ[cname] = {}
        for lv in ("A", "B"):
            tot, per = s_joint(cell, cell["foot"], lv)
            SJ[cname][lv] = tot
            if cname == "C0":
                RES.setdefault("S_joint_detail", {})[lv] = per
    SJ["C11"], SJ["C11b"] = SJ["C0"], SJ["C0"]
    for cname in ("C0", "C1", "C5"):
        LEV[cname] = levers(CELLS[cname], CELLS[cname]["foot"])
    for foot, cname in (("canonical", "C0"), ("alt", "C1")):
        MIM[foot] = {str(zb): mimic(CELLS[cname], foot, zb)[0] for zb in (0.04, 0.055, 0.07)}
    for cname in ("C0", "C1", "C5"):
        P(f"  levers {cname} ({CELLS[cname]['foot']}, {CELLS[cname]['pts']}): " + "; ".join(f"R_{k[3:] if k.startswith('tau') else k} {v:+.3f}" for k, v in LEV[cname].items()))
    for foot in FOOTS:
        P(f"  mimic offsets {foot} (the knob value at which the noiseless sample-level shift equals log10(1 + b3 zbar)); level-B half-ranges: " + ", ".join(f"{k} {BUDGET['B'][k]}" for k in KNOBS[:5]))
        for zb in ("0.04", "0.055", "0.07"):
            P(f"     zbar {zb}: " + "; ".join(f"{k} {v:+.3f}" if v is not None else f"{k} none" for k, v in MIM[foot][zb].items()))
    RES["levers"], RES["mimic"] = LEV, MIM
    RES["S_joint"] = {c: SJ[c] for c in SJ}
    P("  S_joint (aligned worst case, per unit z) at C0: " + "; ".join(f"level {lv}: E1 {SJ['C0'][lv]['E1']:.2f}, E2 {SJ['C0'][lv]['E2']:.2f}" for lv in ("A", "B")))

    plant_tau = {}
    if MUT == "1":
        for cname in CELL_ORDER:
            if cname in ("C11", "C11b"):
                continue
            plant_tau[cname] = plant_offset(CELLS[cname], CELLS[cname]["foot"])
        plant_tau["C11"], plant_tau["C11b"] = plant_tau["C0"], plant_tau["C0"]
        P("  planted shared stellar-mass-scale offset tau_ML* (noiseless E1 slope = b3): " + ", ".join(f"{c} {plant_tau[c]:+.3f}" for c in ("C0", "C1", "C5", "C12")))
        RES["plant"] = plant_tau

    # ------------------------------------------------------------------ AM: the authors-matched scatter factor
    lam_for = {c: 1.0 for c in CELL_ORDER}
    am = {}
    if MUT != "1" and not QUICK:
        for key, anch, cn in (("C11", "canonical", "C11"), ("C11b", "canonical_formal", "C11b")):
            lam, v = solve_lambda(anch, M=2000)
            am[key] = dict(lam=lam, sd_at_solution_a1=v)
            P(f"  AM {key} (anchor {anch}): " + ("UNREACHABLE: even with every M-side per-galaxy term at zero, SD(E1 b)*a0 = %.3e exceeds the authors' formal 1.05e-10" % v if lam is None
                                                else f"lambda = {lam:.3f}, SD(E1 b)*a0 = {v:.3e} (target 1.05e-10)"))
            lam_for[cn] = lam
        RES["AM"] = am
    skip_cells = {c for c in ("C11", "C11b") if lam_for.get(c) is None or MUT == "1" or QUICK}
    check("C7 CONTROL: the solved lambda reproduces the authors' formal sigma(a1) = 1.05e-10 within 2 %, or its unreachability is reported", all((v["lam"] is None) or abs(v["sd_at_solution_a1"] / A1E - 1) < 0.03 for v in am.values()) if am else True,
          "; ".join(f"{k}: " + ("unreachable" if v["lam"] is None else f"{v['sd_at_solution_a1']:.3e}") for k, v in am.items()) or "not run in this mode")

    # ------------------------------------------------------------------ the Monte-Carlo grid
    tasks, meta = [], []
    for ci, cname in enumerate(CELL_ORDER):
        if cname in skip_cells:
            continue
        cell = CELLS[cname]; foot = cell["foot"]
        M = M_MAIN if cname == "C0" else M_OTHER
        for ri, (truth, level) in enumerate(runs_for(cname)):
            seed = int(np.random.SeedSequence([SEED, ci, ri, 0]).generate_state(1)[0])
            tasks.append(((cname, foot, "FLAT" if truth == "PLANT" else truth, level, M, seed, plant_tau.get(cname) if truth == "PLANT" else None, lam_for.get(cname) if cell.get("lam", 1.0) is None else cell["lam"]), (cname, f"{truth}_{level or 'off'}")))
    cost = lambda tk: tk[0][4] * CELLS[tk[0][0]]["N"]
    tasks.sort(key=cost, reverse=True)
    nproc = min(12, os.cpu_count() or 4)
    P(f"\nMONTE CARLO: {len(tasks)} runs ({sum(tk[0][4] for tk in tasks):,d} mocks) on {nproc} processes  ({time.time() - T0:.0f} s so far)")
    t = time.time()
    ctx = mp.get_context("fork")
    OUT = {}
    with ctx.Pool(nproc) as pool:
        for (res, key) in zip(pool.imap(mc_task, [tk[0] for tk in tasks], chunksize=1), [tk[1] for tk in tasks]):
            OUT[key] = res
    P(f"  done in {time.time() - t:.0f} s")
    STATS = {}
    for (cname, run), r in OUT.items():
        STATS.setdefault(cname, {})[run] = dict(b1=summ(r["b1"]), b2=summ(r["b2"]), th2=summ(r["th2"]))
    RES["stats"] = STATS

    # ------------------------------------------------------------------ attribution / detection rates (any mode)
    def rates(cname, run, foot):
        r = OUT[(cname, run)]
        ok1, ok2 = np.isfinite(r["b1"]) & np.isfinite(r["f1"]) & (r["f1"] > 0), np.isfinite(r["b2"])               # a fit that did not converge is counted as a failure, not averaged (the first MUTATE=1 run returned NaN for C12)
        det = float(np.mean(r["b1"][ok1] / r["f1"][ok1] > 3)); phys = float(np.mean(r["b2"][ok2] > B3[foot] / 2))
        return dict(det=det, phys=phys, e2_mean=float(np.mean(r["b2"][ok2])), e2_sd=float(np.std(r["b2"][ok2], ddof=1)), e1_mean=float(np.mean(r["b1"][ok1])), n=int(ok2.sum()), n_fail=int((~ok1).sum() + (~ok2).sum()))

    if MUT == "1":
        P("\nMUTATE=1: THE PLANTED OFFSET EQUAL TO (iii)")
        RES["mutate1"] = {}
        ok6 = True
        for cname in CELL_ORDER:
            if cname in skip_cells:
                continue
            foot = CELLS[cname]["foot"]; b3 = B3[foot]
            rp, rpB, ra, raB, rf = rates(cname, "PLANT_off", foot), rates(cname, "PLANT_B", foot), rates(cname, "ANCH_off", foot), rates(cname, "ANCH_B", foot), rates(cname, "FLAT_B", foot)
            pred_off_phys = 1 - ncdf((b3 / 2 - rpB["e2_mean"]) / rpB["e2_sd"])                  # Gaussian prediction: P(classified PHYS | planted offset, level B)
            pred_phys_phys = 1 - ncdf((b3 / 2 - raB["e2_mean"]) / raB["e2_sd"])
            se = lambda p_, n: math.sqrt(max(p_ * (1 - p_), 1e-6) / n)
            cond_det = rp["det"] >= 0.95 and rpB["det"] >= 0.80
            cond_e2 = abs(rp["e2_mean"] - STATS[cname]["FLAT_off"]["b2"]["mean"]) < 0.15 * b3 and abs(ra["e2_mean"] - STATS[cname]["FLAT_off"]["b2"]["mean"] - b3) < 0.05 * b3
            cond_rate = abs(rpB["phys"] - pred_off_phys) < 3 * se(pred_off_phys, rpB["n"]) + 0.01 and abs(raB["phys"] - pred_phys_phys) < 3 * se(pred_phys_phys, raB["n"]) + 0.01
            RES["mutate1"][cname] = dict(plant=plant_tau[cname], planted_off=rp, planted_B=rpB, anch_off=ra, anch_B=raB, flat_B=rf, pred_phys_given_offset=pred_off_phys, pred_phys_given_phys=pred_phys_phys, ok=bool(cond_det and cond_e2 and cond_rate))
            ok6 &= cond_det and cond_e2 and cond_rate
            P(f"  {cname}: tau_ML* {plant_tau[cname]:+.3f}; E1 detects (formal z > 3): planted {rp['det']:.3f} (clean) / {rpB['det']:.3f} (level B), physical (iii) {ra['det']:.3f} / {raB['det']:.3f}, FLAT level B {rf['det']:.3f}; "
              f"E2 mean slope: planted {rp['e2_mean']:+.2f} / {rpB['e2_mean']:+.2f}, physical {ra['e2_mean']:+.2f} (b3 {b3:.2f}); classified PHYS: planted {rpB['phys']:.3f} (Gaussian prediction {pred_off_phys:.3f}), physical {raB['phys']:.3f} (prediction {pred_phys_phys:.3f}); control {'ok' if cond_det and cond_e2 and cond_rate else 'FAILS'}")
        check("C6 CONTROL (MUTATE=1): the planted offset equal to (iii) is DETECTED by E1 (>= 95 % clean, >= 80 % at level B), E2 reads it as no slope (within 0.15 b3 of FLAT's, physical (iii) within 5 % of b3) and the PHYS / OFFSET classification rates equal the Gaussian prediction within 3 MC errors, in every cell", ok6)
        return finish(CK, RES, STATS, OUT, SJ, plant_tau)

    # ------------------------------------------------------------------ decisions
    P("\nDECISIONS (R1 total scatter, R2 worst case; POSSIBLE iff both; E2 decisive; per unit z; Delta = signal, sd_stat, sd_tot(B), S_joint(B))")
    DEC = {}
    for cname in CELL_ORDER:
        if cname in skip_cells:
            continue
        DEC[cname] = decide(STATS[cname], SJ[cname])
    RES["decisions"] = {c: {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in d.items()} for c, d in DEC.items()}
    P(f"  {'cell':5s} {'law':6s} {'est':3s} {'Delta':>7s} {'sd_stat':>7s} | level A: {'sd_tot':>6s} {'S_joint':>7s} R1 R2 | level B: {'sd_tot':>6s} {'S_joint':>7s} R1 R2 | decision")
    final = {}
    for cname in CELL_ORDER:
        if cname in skip_cells:
            continue
        for law in ("RIVAL", "ANCH"):
            for est in ("E1", "E2"):
                a, b = DEC[cname][(est, law, "A")], DEC[cname][(est, law, "B")]
                dword = "POSSIBLE" if b["possible"] else ("POSSIBLE IF OPTIMISTIC" if a["possible"] else "NOT POSSIBLE")
                final[(cname, law, est)] = dword
                P(f"  {cname:5s} {law:6s} {est:3s} {a['delta']:7.2f} {a['sd_stat']:7.2f} | {a['sd_tot']:6.2f} {a['S_joint']:7.2f} {'Y' if a['R1'] else 'n'}  {'Y' if a['R2'] else 'n'}  | {b['sd_tot']:6.2f} {b['S_joint']:7.2f} {'Y' if b['R1'] else 'n'}  {'Y' if b['R2'] else 'n'}  | {dword}")
    RES["final"] = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in final.items()}
    P("\nPRIMARY DECISIONS (cell C0, level B decides; E2 is decisive, E1 detects but cannot attribute):")
    for law, nm in (("ANCH", "(i) FLAT vs (iii) the anchored slope"), ("RIVAL", "(i) FLAT vs (ii) the rival a0 ~ H(z)")):
        P(f"  {nm}: {final[('C0', law, 'E2')]}   [E1, reported only: {final[('C0', law, 'E1')]}]")
    for law in ("ANCH", "RIVAL"):
        cnt = {w: sum(1 for (c, l, e), v in final.items() if l == law and e == "E2" and v == w) for w in ("POSSIBLE", "POSSIBLE IF OPTIMISTIC", "NOT POSSIBLE")}
        P(f"  cells ({sum(cnt.values())}) by E2 outcome for {law}: {cnt}")
    # required precision, N, drift ceiling, minimum detectable (E2 and E1, C0)
    P("\nREQUIRED PRECISION (C0, per unit z): E2 / E1")
    REQ = {}
    for est in ("E2", "E1"):
        d = DEC["C0"][(est, "ANCH", "B")]; da = DEC["C0"][(est, "ANCH", "A")]
        sig_req = d["sig_req"]
        n_req = None if d["sd_sys"] >= sig_req else 130 * (d["sd_stat"] / math.sqrt(sig_req ** 2 - d["sd_sys"] ** 2)) ** 2
        sjA = SJ["C0"]["A"][est]
        r1k = math.sqrt(max((da["delta"] / 3.29) ** 2 - da["sd_stat"] ** 2, 0.0)) / max(da["sd_sys"], 1e-9)
        r2k = max((da["delta"] - 2 * da["sd_stat"]) / max(sjA, 1e-9), 0.0)
        kap = max(min(r1k, r2k), 0.0)
        REQ[est] = dict(sig_req=sig_req, N_req_levelB=n_req, unreachable_B=bool(d["sd_sys"] >= sig_req), drift_ceiling_kappa=kap, min_detectable_B=d["min_detectable"], min_detectable_A=da["min_detectable"])
        P(f"  {est}: sigma_req (Delta/3.29) {sig_req:.2f}; level-B sd_sys {d['sd_sys']:.2f} -> N_req {'UNREACHABLE at any N' if n_req is None else f'{n_req:,.0f}'}; level-A budget scale kappa_max {kap:.2f} (1 = level A); minimum detectable slope {da['min_detectable']:.2f} (A) / {d['min_detectable']:.2f} (B)")
    RES["required"] = REQ

    # ------------------------------------------------------------------ C4 reactivity, C5 MC margin
    P("\nCONTROLS (Monte Carlo)")
    foot = "canonical"
    d_off = DEC["C0"][("E1", "ANCH", "A")]["delta"]
    z_off = d_off / STATS["C0"]["FLAT_off"]["b1"]["sd"]
    z_B = d_off / STATS["C0"]["FLAT_B"]["b1"]["sd"]
    zbl_off, zbl_B = blind_and_tot(None, foot, M_b=40 if QUICK else 150, B=20 if QUICK else 60), blind_and_tot("B", foot, M_b=40 if QUICK else 150, B=20 if QUICK else 60)
    check("C4 CONTROL (reactivity; the CFG219 lesson): under ANCH the total-scatter statistic Z_tot (E1) falls below 50 % of its no-systematics value at level B while the blind within-mock-bootstrap statistic changes by less than 10 %",
          (z_B < 0.5 * z_off) and abs(zbl_B / zbl_off - 1) < 0.10, f"Z_tot {z_off:.2f} -> {z_B:.2f} (ratio {z_B / z_off:.2f}); blind {zbl_off:.2f} -> {zbl_B:.2f} (change {100 * (zbl_B / zbl_off - 1):+.1f} %)")
    RES["C4"] = dict(z_tot_off=z_off, z_tot_B=z_B, blind_off=zbl_off, blind_B=zbl_B)
    # C5: a reseeded rerun of C0 FLAT_B / ANCH_B and bootstrap errors of the percentile margin
    rr = {}
    for truth in ("FLAT", "ANCH"):
        rr[truth] = mc_task(("C0", "canonical", truth, "B", M_MAIN, int(np.random.SeedSequence([SEED, 31, 1]).generate_state(1)[0]) + (1 if truth == "ANCH" else 0), None, 1.0))
    bs = np.random.default_rng(555)
    marg = {}
    for est, key in (("E2", "b2"), ("E1", "b1")):
        m0 = np.percentile(OUT[("C0", "ANCH_B")][key], 5) - np.percentile(OUT[("C0", "FLAT_B")][key], 95)
        m1 = np.percentile(rr["ANCH"][key], 5) - np.percentile(rr["FLAT"][key], 95)
        ms = []
        for _ in range(100 if not QUICK else 20):
            a_ = OUT[("C0", "ANCH_B")][key]; f_ = OUT[("C0", "FLAT_B")][key]
            ms.append(np.percentile(a_[bs.integers(0, a_.size, a_.size)], 5) - np.percentile(f_[bs.integers(0, f_.size, f_.size)], 95))
        marg[est] = dict(margin=float(m0), margin_rerun=float(m1), se=float(np.std(ms, ddof=1)), mc_limited=bool(abs(m0) < 3 * np.std(ms, ddof=1)))
    check("C5 CONTROL (Monte Carlo margin): the level-B R1 margin P5(ANCH) - P95(FLAT) of the decisive estimator E2 and its reseeded rerun agree in sign, and the decision is not MC-LIMITED (|margin| >= 3 bootstrap errors)",
          np.sign(marg["E2"]["margin"]) == np.sign(marg["E2"]["margin_rerun"]) and not marg["E2"]["mc_limited"], "; ".join(f"{k}: margin {v['margin']:+.2f}, rerun {v['margin_rerun']:+.2f}, se {v['se']:.2f}" for k, v in marg.items()))
    RES["C5"] = marg

    # ------------------------------------------------------------------ C8 (post hoc): the SPARC sub-sample cross-check of the selection budget
    P("\nC8 (POST HOC, reported): the fitted a0 of REAL SPARC sub-samples (the analyst's weights, Upsilon fixed at the mock truth); the spread is the empirical size of a selection offset")
    order_v = np.argsort([m["Vflat"] for m in POOL.meta]); terc = np.array_split(order_v, 3)
    groups = {"Vflat tercile 1 (low)": terc[0], "Vflat tercile 2": terc[1], "Vflat tercile 3 (high)": terc[2],
              "T <= 4 (S0-Sbc)": np.array([i for i, m in enumerate(POOL.meta) if m["T"] <= 4]), "T 5-7 (Sc-Sd)": np.array([i for i, m in enumerate(POOL.meta) if 5 <= m["T"] <= 7]),
              "T >= 8 (Sdm-Im)": np.array([i for i, m in enumerate(POOL.meta) if m["T"] >= 8])}
    c8 = {}
    for nm, idx in groups.items():
        if idx.size < 20:
            continue
        d, e, n = real_sparc_theta(idx, boot=40 if QUICK else 200)
        c8[nm] = dict(dtheta=d, err=e, n=n)
        P(f"  {nm:26s} N = {n:3d}: log10(a0_fit / a0_canonical) = {d:+.4f} +- {e:.4f}")
    allg = real_sparc_theta(np.arange(POOL.ngal), boot=40 if QUICK else 200)
    P(f"  whole pool                  N = {allg[2]:3d}: {allg[0]:+.4f} +- {allg[1]:.4f}")
    rng_c8 = max(v["dtheta"] for v in c8.values()) - min(v["dtheta"] for v in c8.values())
    P(f"  range of the sub-sample fits: {rng_c8:.3f} dex (the level-B T5 band is 0.16 dex wide): " + ("budget ADEQUATE" if rng_c8 <= 0.16 else "SELECTION BUDGET TOO SMALL (decisions would only get worse if T5 and T7 were widened)"))
    RES["C8"] = dict(groups=c8, whole=dict(dtheta=allg[0], err=allg[1]), range=float(rng_c8))

    # ------------------------------------------------------------------ POST HOC level C (only if C8 says the selection budget is too small)
    if rng_c8 > 0.16 and not QUICK:
        BUDGET["C"] = dict(BUDGET["B"], tausel=round(rng_c8 / 2, 3), kapsel=round(rng_c8 / 2, 3))
        cells_c = ["C0"] + [c for c in CELL_ORDER if c not in skip_cells and c != "C0" and any(final[(c, l, "E2")] != "NOT POSSIBLE" for l in ("ANCH", "RIVAL"))]
        P(f"\nPOST HOC LEVEL C (T5 and T7 widened to half the C8 range = {BUDGET['C']['tausel']} dex, everything else as level B), cells {cells_c}")
        tasks_c = []
        for ci, cname in enumerate(CELL_ORDER):
            if cname not in cells_c:
                continue
            for ri, truth in enumerate(("FLAT", "RIVAL", "ANCH")):
                seed = int(np.random.SeedSequence([SEED, ci, 50 + ri, 0]).generate_state(1)[0])
                tasks_c.append(((cname, CELLS[cname]["foot"], truth, "C", M_MAIN if cname == "C0" else M_OTHER, seed, None, 1.0), (cname, f"{truth}_C")))
        tasks_c.sort(key=cost, reverse=True)
        with ctx.Pool(nproc) as pool:
            for (res, key) in zip(pool.imap(mc_task, [tk[0] for tk in tasks_c], chunksize=1), [tk[1] for tk in tasks_c]):
                STATS[key[0]][key[1]] = dict(b1=summ(res["b1"]), b2=summ(res["b2"]), th2=summ(res["th2"]))
        RES["posthoc_C"] = {}
        for cname in cells_c:
            cell = CELLS[cname]
            totC, _ = s_joint(cell, cell["foot"], "C")
            st_ = dict(STATS[cname]); st_["FLAT_B"], st_["RIVAL_B"], st_["ANCH_B"] = st_["FLAT_C"], st_["RIVAL_C"], st_["ANCH_C"]
            dC = decide(st_, {"A": SJ[cname]["A"], "B": totC})
            RES["posthoc_C"][cname] = {f"{k[0]}|{k[1]}": dict(possible=v["possible"], R1=v["R1"], R2=v["R2"], sd_tot=v["sd_tot"], S_joint=v["S_joint"]) for k, v in dC.items() if k[2] == "B"}
            for law in ("ANCH", "RIVAL"):
                P(f"  {cname} {law}: E2 level C: sd_tot {dC[('E2', law, 'B')]['sd_tot']:.2f}, S_joint {totC['E2']:.2f}, R1 {dC[('E2', law, 'B')]['R1']}, R2 {dC[('E2', law, 'B')]['R2']} -> {'POSSIBLE' if dC[('E2', law, 'B')]['possible'] else 'NOT POSSIBLE'};  E1: {'POSSIBLE' if dC[('E1', law, 'B')]['possible'] else 'NOT POSSIBLE'}")

    # ------------------------------------------------------------------ the hand estimates
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 6; scored by code)")
    H = {}
    H["H1"] = (ok1, "the frozen arithmetic (C1)")
    lc = LEV["C0"]
    H["H2"] = (-1.6 <= lc["tauML"] <= -0.3 and -1.3 <= lc["taugas"] <= -0.2 and -4 <= lc["tauD"] <= -1.2 and 3 <= lc["tauV"] <= 8 and abs(lc["tausel"] - 1) < 1e-3,
               "levers C0: " + ", ".join(f"{k} {v:+.2f}" for k, v in lc.items()))
    mm = MIM["canonical"]["0.055"]
    H["H3"] = (mm["tauML"] is not None and -0.40 <= mm["tauML"] <= -0.07 and -0.10 <= mm["tauD"] <= -0.03 and 0.015 <= mm["tauV"] <= 0.04 and abs(mm["tausel"] - 0.1164) < 2e-3,
               "mimic at zbar 0.055 canonical: " + ", ".join(f"{k} {v:+.3f}" for k, v in mm.items() if v is not None))
    s1, s2 = STATS["C0"]["FLAT_off"]["b1"]["sd"], STATS["C0"]["FLAT_off"]["b2"]["sd"]
    am_ok = bool(am) and am.get("C11", {}).get("lam") is not None and 1.0 <= am["C11"]["lam"] <= 4.0
    H["H4"] = (0.5 <= s1 <= 2.0 and 1.2 <= s2 <= 4.0 and am_ok, f"sd_stat E1 {s1:.2f} (0.5-2.0), E2 {s2:.2f} (1.2-4.0); AM lambda " + ("; ".join(f"{k}: {'unreachable' if v['lam'] is None else round(v['lam'], 2)}" for k, v in am.items()) if am else "n/a"))
    nrow = lambda law, est, cells=None: [final[(c, law, est)] for c in CELL_ORDER if c not in skip_cells and (cells is None or c in cells)]
    cond5a = all(v == "NOT POSSIBLE" for e in ("E1", "E2") for v in nrow("RIVAL", e))
    optim = {"C4", "C6", "C8", "C9", "C10", "C12"}
    cond5b = STATS["C0"]["ANCH_off"]["b1"]["p5"] > STATS["C0"]["FLAT_off"]["b1"]["p95"]                       # E1 at C0: R1 passes statistics-only
    cond5c = (not DEC["C0"][("E1", "ANCH", "B")]["R1"]) and (not DEC["C0"][("E1", "ANCH", "A")]["R2"]) and (not DEC["C0"][("E1", "ANCH", "B")]["R2"])      # E1 at C0: R1 fails at B, R2 fails at both levels
    cond5d = final[("C0", "ANCH", "E2")] == "NOT POSSIBLE"
    cond5e = all((v == "NOT POSSIBLE") or (c in optim and v == "POSSIBLE IF OPTIMISTIC") for (c, l, e), v in final.items() if l == "ANCH" and e == "E2")
    H["H5"] = (cond5a and cond5b and cond5c and cond5d and cond5e,
               f"(a) (i) vs (ii) NOT POSSIBLE in every cell, E1 and E2: {cond5a}; (b) E1 at C0: R1 passes statistics-only: {cond5b}; (c) E1 at C0: R1 fails at B and R2 fails at A and B: {cond5c}; (d) E2 (iii) NOT POSSIBLE in C0: {cond5d}; "
               f"(e) E2 (iii) is POSSIBLE at most at level A and only in the optimistic cells: {cond5e}  [scope of the E1 clauses: the primary cell C0, fixed in the code before the main run]")
    H["H6"] = (None, "scored in the MUTATE=1 run")
    H["H7"] = (CK.get("C4", False), f"Z_tot {z_off:.2f} -> {z_B:.2f}; blind {zbl_off:.2f} -> {zbl_B:.2f}")
    H["H8"] = (0.04 <= rng_c8 <= 0.20, f"SPARC sub-sample range {rng_c8:.3f} dex (0.04-0.20)")
    sn = {}
    for est, key in (("E1", "b1"), ("E2", "b2")):
        sn[est] = [STATS[c]["FLAT_off"][key]["sd"] * math.sqrt(CELLS[c]["N"]) for c in ("C0", "C8", "C9", "C10")]
    H["H9"] = (all(max(v) / min(v) < 1.05 for v in sn.values()), "sd_stat * sqrt(N): " + "; ".join(f"{k} " + "/".join(f"{x:.1f}" for x in v) for k, v in sn.items()))
    for k, (ok_, txt) in H.items():
        P(f"  {k}: {'PASS' if ok_ else ('(MUTATE run)' if ok_ is None else 'MISS')}  {txt}")
    RES["hand"] = {k: dict(ok=v[0], text=v[1]) for k, v in H.items()}
    return finish(CK, RES, STATS, OUT, SJ, plant_tau)


def finish(CK, RES, STATS, OUT, SJ, plant_tau):
    ok = all(CK.values())
    if MUT == "2":
        bit = not CK.get("C4", True)
        P(f"\n[MUTATE CONTROL] MUTATE=2: C4 {'FAILED as designed' if bit else 'did NOT fail: the control does not bite'}; controls: {CK}")
        ok = bit
    elif MUT == "1":
        P(f"\n[MUTATE CONTROL] MUTATE=1: C6 {'passes' if CK.get('C6') else 'FAILS'}; controls: {CK}")
    else:
        P(f"\n{sum(CK.values())}/{len(CK)} controls pass -> {'ALL PASS' if ok else 'CONTROL FAILURES'}  ({time.time() - T0:.0f} s)")
    RES["controls"] = CK; RES["seconds"] = round(time.time() - T0, 1)
    open(os.path.join(HERE, f"cfg258_preflight{SFX}.out"), "w").write("\n".join(LOG) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"cfg258_preflight{SFX}_results.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else (o.tolist() if hasattr(o, "tolist") else str(o)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
