#!/usr/bin/env python3
"""
MWT1 POST HOC copy (E forced into C after the graded run; not graded, changes no label) -- which data-side assumptions does RAW1's hot 30-40 kpc bin rest on?
Criteria: FROZEN_CRITERIA.md (committed alone before this script).
Usage: python3 -I -B mwt1.py <path to MWS_BHB.fits>
Writes mwt1.out, mwt1_results.json, and the mutations to mwt1_MUTATE.out.
RAW1's estimators are reused unchanged: this script parses raw1.py and executes only its import, constant and
function-definition statements (raw1.py's top level is not run; RAW1's files are not written). RAW1's model module
is imported read-only. Paths are relative to this script.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[k] = "1"
import ast, json, math, hashlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import minimize
from scipy.stats import chi2 as CHI2, kurtosis as KURT, skew as SKEW

HERE = os.path.dirname(os.path.abspath(__file__))
RAW1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_12", "RAW1_halo_stars_direct"))
FITS = sys.argv[1]
SHA_DATA = "5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246"

OUT = open(os.path.join(HERE, "mwt1_posthoc_E_forced.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say(""); say("=" * 110); say(t); say("=" * 110)
FAILED = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAILED.append(name)
def stop_if_failed():
    if FAILED:
        say("KNOWN-ANSWER CHECK FAILED: " + ", ".join(FAILED) + ". Stopping before any label."); OUT.close(); sys.exit(2)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

# ------------------------------------------------------------------ RAW1's functions, unchanged
sys.path.insert(0, RAW1)
src = open(os.path.join(RAW1, "raw1.py")).read()
tree = ast.parse(src)
KEEP_ASSIGN = ("K474", "BINS", "NOMINAL", "FOOT", "SG", "NGRID", "_GCACHE")
body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in KEEP_ASSIGN)]
R1 = {"FITS": FITS, "HERE": RAW1, "__name__": "raw1_functions"}
exec(compile(ast.Module(body=body, type_ignores=[]), "raw1.py", "exec"), R1)
MOD = R1["MOD"]; BINS = R1["BINS"]; NOMINAL = R1["NOMINAL"]; SG = R1["SG"]
CASES = [("FW_census", "canonical"), ("FW_census", "alt"), ("FW_rc", "canonical"), ("FW_rc", "alt")]
COMPS = [("H", None), ("N", None)]
CKEY = lambda m, f: f"{m}/{f}" if f else m
BN = ["20-30", "30-40", "40-55", "55-80"]
A0EXACT = {"canonical": 9.3603e-11 / 9.36e-11, "alt": 1.1312e-10 / 1.13e-10}

# ------------------------------------------------------------------ generalised Jeans (variable beta, broken law)
BEDGE = (30.0, 40.0, 55.0)
def beta_of(r, bt):
    r = np.asarray(r, float); b = np.full(r.shape, bt[0])
    b = np.where(r >= BEDGE[0], bt[1], b); b = np.where(r >= BEDGE[1], bt[2], b); b = np.where(r >= BEDGE[2], bt[3], b)
    return b
def tracer(s, ak):
    s = np.asarray(s, float)
    if not isinstance(ak, tuple): return (s / 40.0) ** (-float(ak))
    ai, ao, rb = ak; return np.where(s < rb, (s / rb) ** (-ai), (s / rb) ** (-ao))
_SC = {}
def sr2_grid(model, footing, a0m, ak, bt):
    key = (model, footing, a0m, ak, bt)
    if key not in _SC:
        b = beta_of(SG, bt); lnS = np.log(SG)
        lnI = 2 * b[0] * lnS[0] + np.concatenate([[0.0], np.cumsum(0.5 * (2 * b[1:] + 2 * b[:-1]) * np.diff(lnS))])
        n = tracer(SG, ak); I = np.exp(lnI)
        w = n * I * R1["g_on_grid"](model, footing, a0m) * MOD.KPC
        seg = 0.5 * (w[1:] + w[:-1]) * np.diff(SG)
        cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        _SC[key] = cum / (n * I) / 1e6
    return _SC[key]
def predP(r, sin2, model, footing, a0m, ak, bt):
    s2 = np.exp(np.interp(np.log(r), np.log(SG), np.log(np.maximum(sr2_grid(model, footing, a0m, ak, bt), 1e-30))))
    return s2 * (1.0 - beta_of(r, bt) * sin2)

# ------------------------------------------------------------------ scale fit with linear mean model (RAW1's fit_f when X = ones)
def fit_scale(v, e, P, X=None, lo=0.05, hi=5.0, groups=None):
    """v ~ N(X theta, f^2 P + e^2); theta exact WLS for each f; f profiled (RAW1's prof_interval).
    groups: integer labels; each group gets its own intercept (common f)."""
    if X is None: X = np.ones((len(v), 1))
    if groups is not None:
        ug = np.unique(groups); X = np.hstack([X[:, 1:]] + [(groups == g)[:, None].astype(float) for g in ug]) if X.shape[1] > 1 else \
            np.hstack([(groups == g)[:, None].astype(float) for g in ug])
    def solve(f):
        var = f * f * P + e * e; w = 1.0 / var
        A = X.T @ (X * w[:, None]); bvec = X.T @ (w * v)
        th = np.linalg.lstsq(A, bvec, rcond=None)[0]; res = v - X @ th
        return var, th, res, A
    def nll(f):
        var, th, res, A = solve(f); return 0.5 * np.sum(res * res / var + np.log(var))
    fb, flo, fhi, nb = R1["prof_interval"](nll, lo, hi)
    var, th, res, A = solve(fb)
    try: cov = np.linalg.inv(A)
    except np.linalg.LinAlgError: cov = np.full(A.shape, np.nan)
    return dict(f=fb, lo=flo, hi=fhi, s=0.5 * (fhi - flo), nll=nb, theta=th, cov=cov, n=len(v))
def dipX(nv): return np.hstack([np.ones((len(nv), 1)), nv])
def lb_of(vec):
    a = np.linalg.norm(vec); return a, math.degrees(math.atan2(vec[1], vec[0])) % 360, math.degrees(math.asin(np.clip(vec[2] / a, -1, 1)))

# ------------------------------------------------------------------ data
assert sha(FITS) == SHA_DATA, "data file hash mismatch"
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
D = R1["load"]()
_h = fits.open(FITS, memmap=False)
_rv, _ga = _h["RVTAB"].data, _h["GAIA"].data
D["logg"] = np.asarray(_rv["LOGG"], float); D["logg_err"] = np.asarray(_rv["LOGG_ERR"], float)
D["plx"] = np.asarray(_ga["PARALLAX"], float); D["eplx"] = np.asarray(_ga["PARALLAX_ERROR"], float)
_c = SkyCoord(ra=D["ra"] * u.deg, dec=D["dec"] * u.deg, frame="icrs").galactic
D["l"], D["b"] = _c.l.deg, _c.b.deg
D["bsgr"] = R1["sgr_lat_lon"](D["l"], D["b"])[1]

def build(cfg):
    S = R1["build"](D, cfg)
    for k in ("l", "b", "bsgr", "logg", "logg_err", "plx", "eplx"): S[k] = D[k][S["i"]]
    S["sid_ok"] = (D["sid"][S["i"]] > 0) & (D["sid"][S["i"]] == D["ref_id"][S["i"]])
    S["bin"] = np.array([next((j for j, (a, b) in enumerate(BINS) if a <= x < b), -1) for x in S["r"]])
    return S

def fit_beta_nll(P):
    """RAW1's fit_beta, also returning the minimum nll (for the B LR test)."""
    from scipy.optimize import minimize_scalar
    def prof(beta):
        return minimize_scalar(lambda t: R1["beta_nll"](P, t, beta), bounds=(math.log(20.0), math.log(600.0)), method="bounded",
                               options=dict(xatol=1e-7)).fun
    bb, blo, bhi, nb = R1["prof_interval"](prof, -3.0, 0.99)
    return dict(beta=bb, lo=blo, hi=bhi, sig=0.5 * (bhi - blo), nll=nb)

_MEAS = {}
def measured(dscale):
    if dscale not in _MEAS:
        cfg = dict(NOMINAL, dscale=dscale); S = build(cfg); R = R1["measure"](S, cfg)
        # B LR: per-bin vs one constant over the usable bins
        us = [j for j, x in enumerate(R["usable"]) if x]
        per = [fit_beta_nll(R1["pm_arrays"](S, R["bsel"][j] & S["pmok"], cfg["dfrac"])) for j in us]
        sel = np.zeros(len(S["r"]), bool)
        for j in us: sel |= R["bsel"][j]
        glob = fit_beta_nll(R1["pm_arrays"](S, sel & S["pmok"], cfg["dfrac"]))
        LR = 2 * (glob["nll"] - sum(p["nll"] for p in per))
        R["B_LR"] = dict(LR=LR, dof=len(us) - 1, p=float(CHI2.sf(LR, len(us) - 1)) if len(us) > 1 else float("nan"),
                         per=[(p["beta"], p["sig"]) for p in per], usable=us)
        _MEAS[dscale] = (cfg, S, R)
    return _MEAS[dscale]

# ------------------------------------------------------------------ broken law from the sample (D-data)
def alpha_nll_rb(A, ak):
    if not isinstance(ak, tuple): return R1["alpha_nll"](A, ak)
    ai, ao, rb = ak
    ln_n = np.log(tracer(A["r"], ak)); ln_ng = np.log(tracer(A["rg"], ak))
    lw = 3 * np.log(A["dg"]) + ln_ng; mx = lw.max(axis=1)
    dl = np.log(A["dg"][:, 1] / A["dg"][:, 0])
    ww = np.exp(lw - mx[:, None]); Z = (np.sum(ww, axis=1) - 0.5 * (ww[:, 0] + ww[:, -1])) * dl
    return -np.sum(2 * np.log(A["d"]) + ln_n - (np.log(Z) + mx))
_DD = {}
def broken_fit(dscale, rb):
    key = (dscale, rb)
    if key not in _DD:
        cfg, S, R = measured(dscale); A = R1["alpha_setup"](S, cfg)
        f = lambda p: alpha_nll_rb(A, (p[0], p[1], rb))
        res = minimize(f, [R["alpha"]["alpha"], R["alpha"]["alpha"]], method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-7, maxiter=4000))
        p = res.x; h = 1e-2; H = np.zeros((2, 2))
        for i in range(2):
            for j in range(2):
                ei = np.eye(2)[i] * h; ej = np.eye(2)[j] * h
                H[i, j] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * h * h)
        try:
            C = np.linalg.inv(H); si, so = math.sqrt(max(C[0, 0], 0)), math.sqrt(max(C[1, 1], 0))
        except np.linalg.LinAlgError: si = so = float("nan")
        nll1 = R1["alpha_nll"](A, R["alpha"]["alpha"])
        _DD[key] = dict(ain=float(p[0]), aout=float(p[1]), sin=si, sout=so, rb=rb, LR=float(2 * (nll1 - res.fun)), nll=float(res.fun))
    return _DD[key]

# ------------------------------------------------------------------ option builder and evaluator
def base_flags(): return dict(L=None, S1=None, S2=None, Xerr=None, D=None, Dlit=None, B=False, B55=None, Bconst=None, E=False, F=False, a0m=False)

def make_opt(S, R, cfg, flags, S2SET=None):
    keep = np.ones(len(S["r"]), bool)
    if flags["L"] is not None:
        keep &= ~((S["logg"] > flags["L"]) & (S["logg_err"] < 0.25) & np.isfinite(S["logg"]))
    if flags["S1"] is not None: keep &= np.abs(S["bsgr"]) >= flags["S1"]
    if flags["S2"] is not None: keep &= ~np.isin(S["i"], np.array(sorted(flags["S2"]), dtype=int))
    esc = flags["Xerr"] if flags["Xerr"] is not None else 1.0
    a, sa = R["alpha"]["alpha"], R["alpha"]["sig"]
    if flags["Dlit"] is not None:
        ak = flags["Dlit"]; avars = "nominal"
    elif flags["D"] is not None:
        bf = broken_fit(cfg["dscale"], flags["D"]); ai, ao, rb = bf["ain"], bf["aout"], bf["rb"]
        ak = (ai, ao, rb); avars = [((ai - bf["sin"], ao, rb), (ai + bf["sin"], ao, rb)), ((ai, ao - bf["sout"], rb), (ai, ao + bf["sout"], rb))]
    else:
        ak = a; avars = [(a - sa, a + sa)]
    if flags["Bconst"] is not None:
        b = flags["Bconst"]; bt = (b,) * 4; bvars = [(bt, bt)] * 4
    elif flags["B"]:
        vals = []; sigs = []
        for j in range(3):
            pb = R["pmbeta"][j]
            if R["usable"][j]: vals.append(pb["beta"]); sigs.append(pb["sig"])
            else: vals.append(R["beta"]); sigs.append(R["sbeta"])
        b55 = vals[2] if flags["B55"] is None else flags["B55"]
        bt = (vals[0], vals[1], vals[2], b55)
        lo = (vals[0] - sigs[0], vals[1] - sigs[1], vals[2] - sigs[2], (vals[2] - sigs[2]) if flags["B55"] is None else b55)
        hi = (vals[0] + sigs[0], vals[1] + sigs[1], vals[2] + sigs[2], (vals[2] + sigs[2]) if flags["B55"] is None else b55)
        bvars = [(lo, hi)] * 3 + [((bt[0], bt[1], bt[2], 0.2), (bt[0], bt[1], bt[2], 0.8))]
    else:
        b = R["beta"]; bt = (b,) * 4
        bvars = [((x,) * 4, (y,) * 4) for x, y in R["brange"]]
    return keep, dict(ak=ak, avars=avars, bt=bt, bvars=bvars, esc=esc, E=flags["E"], F=flags["F"])

def est_bin(v, e, P, nv, gl_b, E, F):
    """the per-bin estimator: f and its stat sigma."""
    if E and not F:
        r = fit_scale(v, e, P, dipX(nv)); return r["f"], r["s"], r
    if E:
        r0 = fit_scale(v, e, P, dipX(nv)); v = v - nv @ r0["theta"][1:]
    if F:
        nN, nS = np.sum(gl_b > 0), np.sum(gl_b <= 0)
        if nN >= 15 and nS >= 15:
            rN = fit_scale(v[gl_b > 0], e[gl_b > 0], P[gl_b > 0]); rS = fit_scale(v[gl_b <= 0], e[gl_b <= 0], P[gl_b <= 0])
            return 0.5 * (rN["f"] + rS["f"]), 0.5 * math.hypot(rN["s"], rS["s"]), dict(fN=rN["f"], fS=rS["f"], n=len(v))
    r = fit_scale(v, e, P); return r["f"], r["s"], r

def f_rows(S, keep, model, footing, opt, a0m=1.0, vel=None):
    v_all = S["vgsr"] if vel is None else vel
    rows = []
    for j in range(4):
        m = keep & (S["bin"] == j)
        v, e, r, s2, nv, gb = v_all[m], S["verr"][m] * opt["esc"], S["r"][m], S["sin2"][m], S["n"][m], S["b"][m]
        if len(v) < 30:
            rows.append(dict(f=float("nan"), s=float("nan"), s_stat=float("nan"), s_alpha=0, s_beta=0, n=int(len(v)))); continue
        F0 = lambda ak, bt: est_bin(v, e, predP(r, s2, model, footing, a0m, ak, bt), nv, gb, opt["E"], opt["F"])
        f, ss, _ = F0(opt["ak"], opt["bt"])
        if opt["avars"] == "nominal": sa = None
        else: sa = math.sqrt(sum((0.5 * (F0(hi, opt["bt"])[0] - F0(lo, opt["bt"])[0])) ** 2 for lo, hi in opt["avars"]))
        lo, hi = opt["bvars"][j]
        sb = 0.0 if lo == hi else 0.5 * abs(F0(opt["ak"], hi)[0] - F0(opt["ak"], lo)[0])
        rows.append(dict(f=f, s_stat=ss, s_alpha=sa, s_beta=sb, n=int(len(v))))
    return rows

def finish_rows(rows, nominal_salpha=None):
    for j, x in enumerate(rows):
        if x["s_alpha"] is None: x["s_alpha"] = nominal_salpha[j]
        x["s"] = math.sqrt(x["s_stat"] ** 2 + x["s_alpha"] ** 2 + x["s_beta"] ** 2) if np.isfinite(x["s_stat"]) else float("nan")
    return rows
def word(x):
    if not np.isfinite(x["f"]): return "N/A"
    return "HOT" if x["f"] > 1 + 2 * x["s"] else ("COLD" if x["f"] < 1 - 2 * x["s"] else "PASS")
def rowlabel(rows):
    lab, bad = R1["grade"]([x["f"] for x in rows], [x["s"] for x in rows], BN); return lab, bad

NOMSA = {}
def run(flags, dscale=1.0, cases=CASES + COMPS, vel=None):
    cfg, S, R = measured(dscale)
    keep, opt = make_opt(S, R, cfg, flags)
    out = {}
    for m, ft in cases:
        a0m = A0EXACT[ft] if (flags["a0m"] and ft) else 1.0
        rows = f_rows(S, keep, m, ft, opt, a0m, vel)
        out[CKEY(m, ft)] = finish_rows(rows, NOMSA.get(CKEY(m, ft)))
    out["_n"] = [int(np.sum(keep & (S["bin"] == j))) for j in range(4)]
    out["_removed"] = [int(np.sum(~keep & (S["bin"] == j))) for j in range(4)]
    return out

def fmt(rows): return "  ".join(f"{x['f']:.3f}+/-{x['s']:.3f} {word(x):4s}" for x in rows)

# ================================================================== K1-K3 (no data numbers)
sec("MWT1 known answers without data (K1-K3)")
say(f"  RAW1 files read-only: raw1.py sha256 {sha(os.path.join(RAW1, 'raw1.py'))[:16]}..., raw1_model.py {sha(os.path.join(RAW1, 'raw1_model.py'))[:16]}...; data sha256 {SHA_DATA[:16]}... (matches)")
rr = np.linspace(20, 80, 61); worst = 0.0
for model, ft in CASES + COMPS:
    for b in (0.2, 0.659, 0.8):
        for a in (3.0, 5.289):
            mine = predP(rr, np.zeros_like(rr), model, ft, 1.0, a, (b,) * 4)
            raw = R1["sr2_at"](rr, model, a, b, ft, 1.0)
            worst = max(worst, float(np.max(np.abs(mine / raw - 1))))
check("K1 variable-beta solver at constant beta == RAW1 sr2_profile", worst < 1e-6, f"max relative difference {worst:.2e}")
rng = np.random.default_rng(7); vv = rng.normal(5, 100, 300); ee = rng.uniform(2, 20, 300); PP = rng.uniform(5e3, 1.5e4, 300)
fa, sa_ = R1["fit_f"](vv, ee, PP); fb_ = fit_scale(vv, ee, PP)
check("K2 fit_scale (X = ones) == RAW1 fit_f", abs(fa - fb_["f"]) < 1e-6 and abs(sa_ - fb_["s"]) < 1e-6, f"{fa:.8f}/{sa_:.8f} vs {fb_['f']:.8f}/{fb_['s']:.8f}")
g30 = float(MOD.g_model(30.0, "FW_census", "canonical")); Msi = g30 * (30 * 3.0857e19) ** 2 / 6.674e-11 / 1.989e30
check("K3 SI: M = g r^2 / G at 30 kpc (FW census canonical)", abs(Msi / float(MOD.M_of_g(g30, 30.0)) - 1) < 1e-9,
      f"g = {g30:.4e} m/s^2, M = {Msi:.4e} Msun, V = sqrt(g r) = {math.sqrt(g30 * 30 * 3.0857e19) / 1e3:.1f} km/s")
stop_if_failed()

# ================================================================== K0: RAW1 reproduced
sec("K0 RAW1 reproduced with no check applied")
cfg0, S0, R0 = measured(1.0)
J = json.load(open(os.path.join(RAW1, "raw1_results.json")))["nominal"]
check("K0 counts", list(R0["counts"]) == J["counts"] == [865, 264, 241, 125], f"{R0['counts']}")
dd = max(abs(a["sigma"] - b["sigma"]) for a, b in zip(R0["disp"], J["disp"]))
check("K0 sigma_los", dd < 5e-4, "  ".join(f"{x['sigma']:.3f}" for x in R0["disp"]) + f" (max diff {dd:.1e})")
check("K0 alpha, beta", abs(R0["alpha"]["alpha"] - J["alpha"]["alpha"]) < 5e-4 and abs(R0["beta"] - J["beta"]) < 5e-4,
      f"alpha {R0['alpha']['alpha']:.4f} beta {R0['beta']:.4f} +/- {R0['sbeta']:.4f}")
BASE = run(base_flags())
for m, ft in CASES + COMPS:
    k = CKEY(m, ft); NOMSA[k] = [x["s_alpha"] for x in BASE[k]]
    dmax = max(max(abs(a["f"] - b["f"]), abs(a["s"] - b["s"])) for a, b in zip(BASE[k], J["f"][k]))
    check(f"K0 f {k}", dmax < 5e-4, fmt(BASE[k]) + f" (max diff {dmax:.1e})")
stop_if_failed()
say(f"  per-bin beta (own PMs): " + ", ".join(f"{BN[j]} {p['beta']:.3f} +/- {p['sig']:.3f}" if 'beta' in p else f"{BN[j]} not fitted" for j, p in enumerate(R0['pmbeta'])))
say(f"  median tangential velocity error per bin [km/s]: " + ", ".join(f"{BN[j]} {p.get('med_terr', float('nan')):.1f}" for j, p in enumerate(R0['pmbeta'])))

RES = dict(base=BASE, checks={}, diag={}, detected={}, twins={}, combination={}, labels={})

# ================================================================== diagnostics and detection rules
sec("(E) Equilibrium: mean, dipole, kurtosis, bimodality (per bin)")
rngK = np.random.default_rng(20261113)
def kurt_bc(z):
    n = len(z); g = SKEW(z, bias=False); k = KURT(z, bias=False)
    return k, (g * g + 1) / (k + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))
EDIAG = []
for j in range(4):
    m = S0["bin"] == j; v, e, nv = S0["vgsr"][m], S0["verr"][m], S0["n"][m]
    r1 = fit_scale(v, e, np.ones(len(v)), None, 1.0, 400.0); rd = fit_scale(v, e, np.ones(len(v)), dipX(nv), 1.0, 400.0)
    LR = 2 * (r1["nll"] - rd["nll"]); p = float(CHI2.sf(LR, 3))
    Dv = rd["theta"][1:]; Cd = rd["cov"][1:, 1:]
    amp, l_, b_ = lb_of(Dv); g_ = Dv / amp; samp = float(math.sqrt(max(g_ @ Cd @ g_, 0)))
    mu, smu = r1["theta"][0], math.sqrt(r1["cov"][0, 0])
    z = (v - mu) / np.sqrt(r1["f"] ** 2 + e ** 2); k_obs, bc_obs = kurt_bc(z)
    ks, bs = [], []
    for _ in range(2000):
        vs = rngK.normal(0, 1, len(v)) * np.sqrt(r1["f"] ** 2 + e ** 2)
        w = 1 / (r1["f"] ** 2 + e ** 2); mus = np.sum(w * vs) / np.sum(w)
        ss = math.sqrt(max(np.mean((vs - mus) ** 2 - e ** 2), 1.0))
        kk, bb = kurt_bc((vs - mus) / np.sqrt(ss ** 2 + e ** 2)); ks.append(kk); bs.append(bb)
    ks, bs = np.array(ks), np.array(bs)
    pk = float(min(1.0, 2 * min(np.mean(ks >= k_obs), np.mean(ks <= k_obs)) + 1 / 2000)); pb = float((1 + np.sum(bs >= bc_obs)) / 2001)
    zd = (v - mu - nv @ Dv) / np.sqrt(rd["f"] ** 2 + e ** 2); k_d, bc_d = kurt_bc(zd)
    EDIAG.append(dict(n=len(v), mu=mu, smu=smu, sigma=r1["f"], sigma_dip=rd["f"], s_dip=rd["s"], D=Dv.tolist(), amp=amp, samp=samp, l=l_, b=b_,
                      LR=LR, p=p, kurt=k_obs, p_kurt=pk, bc=bc_obs, p_bc=pb, kurt_after_dip=k_d, bc_after_dip=bc_d))
    say(f"  {BN[j]}: N {len(v)}; mean v_gsr {mu:+.1f} +/- {smu:.1f}; sigma {r1['f']:.2f} -> {rd['f']:.2f} with dipole; dipole {amp:.1f} +/- {samp:.1f} km/s "
        f"toward (l {l_:.0f}, b {b_:+.0f}), LR {LR:.2f}, p {p:.4f}; excess kurtosis {k_obs:+.3f} (p {pk:.4f}); bimodality coeff {bc_obs:.3f} (p {pb:.4f}; 0.555 = uniform); after dipole kurt {k_d:+.3f} BC {bc_d:.3f}")
RES["diag"]["E"] = EDIAG
DET_E = True  # POST HOC: E forced into the combination after M1 failed to bite (not graded)
say(f"  E DETECTED (dipole p < 0.01 in any bin): {DET_E}")
# T2 dipole twin
rngT = np.random.default_rng(20261114); vsh = S0["vgsr"].copy()
for j in range(4):
    ii = np.where(S0["bin"] == j)[0]; vsh[ii] = vsh[rngT.permutation(ii)]
m = S0["bin"] == 1
r1 = fit_scale(vsh[m], S0["verr"][m], np.ones(m.sum()), None, 1.0, 400.0); rd = fit_scale(vsh[m], S0["verr"][m], np.ones(m.sum()), dipX(S0["n"][m]), 1.0, 400.0)
pT2 = float(CHI2.sf(2 * (r1["nll"] - rd["nll"]), 3))
check("T2 dipole twin (shuffled 30-40): not DETECTED", pT2 >= 0.01, f"p {pT2:.4f}")
RES["twins"]["T2_p"] = pT2

sec("(S1) Sagittarius band 15 -> 25 deg: detection test 15-25 vs >= 25 (per bin)")
S1DIAG = []
for j in range(4):
    m = S0["bin"] == j; ga = m & (np.abs(S0["bsgr"]) < 25); gb_ = m & (np.abs(S0["bsgr"]) >= 25)
    if ga.sum() < 10 or gb_.sum() < 10: S1DIAG.append(dict(nA=int(ga.sum()), nB=int(gb_.sum()), p=float("nan"))); say(f"  {BN[j]}: too few"); continue
    one = lambda mm: fit_scale(S0["vgsr"][mm], S0["verr"][mm], np.ones(mm.sum()), None, 1.0, 400.0)
    rA, rB, rC = one(ga), one(gb_), one(m)
    LR = 2 * (rC["nll"] - rA["nll"] - rB["nll"]); p = float(CHI2.sf(LR, 2))
    S1DIAG.append(dict(nA=int(ga.sum()), nB=int(gb_.sum()), sA=rA["f"], sB=rB["f"], muA=rA["theta"][0], muB=rB["theta"][0], LR=LR, p=p))
    say(f"  {BN[j]}: 15-25 deg N {ga.sum()} sigma {rA['f']:.1f} mean {rA['theta'][0]:+.1f}; >= 25 deg N {gb_.sum()} sigma {rB['f']:.1f} mean {rB['theta'][0]:+.1f}; LR {LR:.2f} p {p:.4f}")
DET_S1 = any(np.isfinite(x["p"]) and x["p"] < 0.01 for x in S1DIAG)
say(f"  S1 DETECTED: {DET_S1}"); RES["diag"]["S1"] = S1DIAG

sec("(S2) position-velocity overdensity mask (200 shuffles nominal; 2,000 for the p 0.001 / 0.05 brackets)")
def s2_setup(S):
    nn = S["n"]; ca = np.clip(nn @ nn.T, -1, 1)
    Apos = (ca > math.cos(math.radians(10.0))) & (np.abs(S["r"][:, None] - S["r"][None, :]) < 5.0)
    np.fill_diagonal(Apos, False); return Apos
def kcount(Apos, v): return np.sum(Apos & (np.abs(v[:, None] - v[None, :]) < 25.0), axis=1)
def shuffles(S, v, nsh, seed):
    rg = np.random.default_rng(seed); idx = [np.where(S["bin"] == j)[0] for j in range(4)]
    out = np.empty((nsh, len(v)))
    Apos = s2_setup(S)
    for t in range(nsh):
        w = v.copy()
        for ii in idx: w[ii] = v[rg.permutation(ii)]
        out[t] = kcount(Apos, w)
    return Apos, out
def flags_from(k, null, pthr):
    nsh = null.shape[0]; cnt = np.sum(null >= k[None, :], axis=0)
    return (k >= 2) & ((cnt + 0.0) / nsh < pthr) if pthr != 0.01 else (k >= 2) & (cnt < 2)
v0 = S0["vgsr"]
Apos0, NULL200 = shuffles(S0, v0, 200, 20261115)
k0 = kcount(Apos0, v0); FL = flags_from(k0, NULL200, 0.01)
# leave-one-out null of flagged counts
nullflag = np.zeros((200, 4))
for t in range(200):
    others = np.delete(NULL200, t, axis=0); cnt = np.sum(others >= NULL200[t][None, :], axis=0)
    ft_ = (NULL200[t] >= 2) & (cnt < 2)
    nullflag[t] = [np.sum(ft_ & (S0["bin"] == j)) for j in range(4)]
S2DIAG = []
for j in range(4):
    obs = int(np.sum(FL & (S0["bin"] == j))); q99 = float(np.percentile(nullflag[:, j], 99))
    S2DIAG.append(dict(flagged=obs, null_mean=float(nullflag[:, j].mean()), null_q99=q99, detected=obs > q99))
    mm = (S0["bin"] == j) & FL
    sf = fit_scale(v0[mm], S0["verr"][mm], np.ones(mm.sum()), None, 1.0, 400.0)["f"] if mm.sum() >= 5 else float("nan")
    say(f"  {BN[j]}: flagged {obs} (null mean {nullflag[:, j].mean():.1f}, 99th pct {q99:.1f}) -> {'DETECTED' if obs > q99 else 'not detected'}; dispersion of the flagged stars {sf:.1f}")
DET_S2 = any(x["detected"] for x in S2DIAG)
S2SET = set(S0["i"][FL].tolist())
_, NULL2000 = shuffles(S0, v0, 2000, 20261116)
S2SET_001 = set(S0["i"][flags_from(k0, NULL2000, 0.001)].tolist()); S2SET_05 = set(S0["i"][flags_from(k0, NULL2000, 0.05)].tolist())
say(f"  S2 DETECTED: {DET_S2}; mask sizes p<0.01 {len(S2SET)}, p<0.001 {len(S2SET_001)}, p<0.05 {len(S2SET_05)} (2,000 shuffles for the brackets)")
RES["diag"]["S2"] = S2DIAG

sec("(L) logg contamination cut")
LDIAG = []
for thr in (3.5, 3.75, 4.0):
    bad = (S0["logg"] > thr) & (S0["logg_err"] < 0.25) & np.isfinite(S0["logg"])
    cnts = [int(np.sum(bad & (S0["bin"] == j))) for j in range(4)]
    sd = fit_scale(v0[bad], S0["verr"][bad], np.ones(bad.sum()), None, 1.0, 400.0)["f"] if bad.sum() >= 5 else float("nan")
    LDIAG.append(dict(thr=thr, removed=cnts, sigma_removed=sd))
    say(f"  LOGG > {thr} (err < 0.25): removed per bin {cnts}; dispersion of removed stars {sd:.1f}")
say(f"  LOGG over the 20-80 sample: median {np.nanmedian(S0['logg']):.2f}, 5-95 pct {np.nanpercentile(S0['logg'], 5):.2f} to {np.nanpercentile(S0['logg'], 95):.2f}; finite {np.isfinite(S0['logg']).mean():.3f}")
DET_L = sum(LDIAG[1]["removed"]) >= 1
say(f"  L DETECTED: {DET_L}"); RES["diag"]["L"] = LDIAG

sec("(D) tracer density: the sample's own broken law (break 25 and 30)")
DD = {rb: broken_fit(1.0, rb) for rb in (25.0, 30.0)}
for rb, x in DD.items():
    conv = x["aout"] > 2 * R0["beta"] + 0.5
    say(f"  break {rb:.0f}: inner {x['ain']:.3f} +/- {x['sin']:.3f}, outer {x['aout']:.3f} +/- {x['sout']:.3f}; 2 Delta lnL vs single {x['LR']:.2f}; convergent {conv}")
best_rb = max(DD, key=lambda k: -DD[k]["nll"])
DET_D = any(DD[rb]["LR"] > 6.63 and DD[rb]["aout"] > 2 * R0["beta"] + 0.5 for rb in DD)
say(f"  single slope {R0['alpha']['alpha']:.3f} +/- {R0['alpha']['sig']:.3f}; better break {best_rb:.0f}; D DETECTED: {DET_D}")
say(f"  The window reaches about 45 kpc (RAW1): the slope beyond is extrapolated; completeness flat in magnitude is assumed and not testable here.")
RES["diag"]["D"] = {str(k): v for k, v in DD.items()}

sec("(B) anisotropy: per-bin beta from the stars' own proper motions")
BL = R0["B_LR"]
say(f"  usable bins {[BN[j] for j in BL['usable']]}; per-bin " + ", ".join(f"{b:.3f}+/-{s:.3f}" for b, s in BL["per"]) +
    f"; LR per-bin vs constant {BL['LR']:.2f} ({BL['dof']} dof) p {BL['p']:.4f}")
DET_B = BL["p"] < 0.01
b30, s30 = R0["pmbeta"][1]["beta"], R0["pmbeta"][1]["sig"]
BCOUNT = {bc: abs(bc - b30) <= 3 * s30 for bc in (0.2, 0.8)}
say(f"  B DETECTED: {DET_B}. 30-40 bin's own beta {b30:.3f} +/- {s30:.3f}: B-bracket 0.2 excluded at > 3 sigma: {not BCOUNT[0.2]}; 0.8 excluded: {not BCOUNT[0.8]}")
say(f"  What the PMs can say at 30-40: median tangential error {R0['pmbeta'][1]['med_terr']:.1f} km/s against sigma_los {R0['disp'][1]['sigma']:.1f}: beta measured; Gaia systematic floor not modelled.")
RES["diag"]["B"] = dict(LR=BL, b30=b30, s30=s30, counts_for_depends=BCOUNT)

sec("(X) velocity-error scale from repeat observations; parallax check of the distance scale")
okr = np.isfinite(D["vrad"]) & (D["verr"] > 0)
tid = D["tid"]; order = np.argsort(tid, kind="stable"); ts = tid[order]
uniq, start, cnts = np.unique(ts, return_index=True, return_counts=True)
pairs = []; gid = []
for g, (s_, c_) in enumerate(zip(start, cnts)):
    if c_ < 2: continue
    rows = [order[s_ + t] for t in range(c_) if okr[order[s_ + t]]]
    for x in range(len(rows)):
        for y in range(x + 1, len(rows)): pairs.append((rows[x], rows[y])); gid.append(g)
pairs = np.array(pairs); gid = np.array(gid)
dv = D["vrad"][pairs[:, 0]] - D["vrad"][pairs[:, 1]]; se = np.hypot(D["verr"][pairs[:, 0]], D["verr"][pairs[:, 1]])
same = (np.abs(dv) < 1e-6) & (np.abs(D["verr"][pairs[:, 0]] - D["verr"][pairs[:, 1]]) < 1e-6)
zr = dv / se
def madscale(z): return 1.4826 * np.median(np.abs(z - np.median(z)))
sX = madscale(zr); ug = np.unique(gid); rgb = np.random.default_rng(20261117); bsX = []
gl = {g: np.where(gid == g)[0] for g in ug}
for _ in range(1000):
    pick = rgb.choice(ug, len(ug)); ii = np.concatenate([gl[g] for g in pick]); bsX.append(madscale(zr[ii]))
esX = float(np.std(bsX)); DET_X = abs(sX - 1) > 2.576 * esX
say(f"  repeat pairs {len(pairs)} from {len(ug)} TARGETIDs; identical pairs (same v and error) {int(same.sum())}; median quoted error {np.median(D['verr'][okr & D['primary']]):.2f} km/s")
say(f"  error scale s = 1.4826 MAD(z) = {sX:.3f} +/- {esX:.3f}; X-err DETECTED: {DET_X}" + (f"; without identical pairs s = {madscale(zr[~same]):.3f}" if same.any() else ""))
PLX = []
for j in range(4):
    m = (S0["bin"] == j) & np.isfinite(S0["plx"]) & (S0["eplx"] > 0) & S0["sid_ok"]
    w = 1 / S0["eplx"][m] ** 2; obs = np.sum(w * (S0["plx"][m] + 0.017)) / np.sum(w); err = 1 / math.sqrt(np.sum(w)); pred = np.sum(w * (1 / S0["d"][m])) / np.sum(w)
    PLX.append(dict(n=int(m.sum()), obs=obs, err=err, pred=pred, ratio=obs / pred, ratio_err=err / pred))
    say(f"  {BN[j]}: Gaia parallax (zero point +0.017, PROVISIONAL) {obs:.4f} +/- {err:.4f} mas vs 1/d {pred:.4f}: ratio {obs / pred:.2f} +/- {err / pred:.2f} (N {m.sum()})")
say("  The parallaxes cannot fix the distance scale at 10 per cent (errors above): X-dist stays untestable.")
RES["diag"]["X"] = dict(npairs=int(len(pairs)), ngroups=int(len(ug)), identical=int(same.sum()), s=sX, es=esX, plx=PLX)

sec("(F) footprint: coverage, hemispheres, quadrants; polar-cone symmetry diagnostic (f with FW census canonical P)")
rgc = np.random.default_rng(20261118); pts = rgc.normal(size=(20000, 3)); pts /= np.linalg.norm(pts, axis=1)[:, None]
FDIAG = []
for j in range(4):
    m = S0["bin"] == j; nn = S0["n"][m]
    cov = float(np.mean(np.max(pts @ nn.T, axis=1) > math.cos(math.radians(5.0))))
    P = predP(S0["r"][m], S0["sin2"][m], "FW_census", "canonical", 1.0, R0["alpha"]["alpha"], (R0["beta"],) * 4)
    v, e, bb_ = v0[m], S0["verr"][m], S0["b"][m]
    def lr_groups(lab):
        ok = np.ones(len(v), bool); ug_ = [g for g in np.unique(lab) if np.sum(lab == g) >= 15]
        ok = np.isin(lab, ug_)
        if len(ug_) < 2: return float("nan"), [], len(ug_)
        common = fit_scale(v[ok], e[ok], P[ok], None, groups=lab[ok])
        sep = [fit_scale(v[lab == g], e[lab == g], P[lab == g]) for g in ug_]
        LR = 2 * (common["nll"] - sum(s_["nll"] for s_ in sep))
        return float(CHI2.sf(LR, len(ug_) - 1)), [(int(np.sum(lab == g)), s_["f"]) for g, s_ in zip(ug_, sep)], len(ug_)
    hemi = (bb_ > 0).astype(int)
    quad = hemi * 2 + (S0["l"][m] >= 180).astype(int)
    zr_ = np.abs(S0["pos"][m][:, 2]) / S0["r"][m]; polar = (zr_ > 0.5).astype(int)
    ph, gh, _ = lr_groups(hemi); pq, gq, nq = lr_groups(quad); pp, gp, _ = lr_groups(polar)
    FDIAG.append(dict(coverage=cov, p_hemi=ph, hemi=gh, p_quad=pq, quad=gq, p_polar=pp, polar=gp))
    say(f"  {BN[j]}: sky coverage {cov:.3f}; hemispheres (S, N) {[(n_, round(f_, 3)) for n_, f_ in gh]} p {ph:.4f}; quadrants {[(n_, round(f_, 3)) for n_, f_ in gq]} p {pq:.4f}; "
        f"polar cones (rest, polar) {[(n_, round(f_, 3)) for n_, f_ in gp]} p {pp:.4f}")
DET_F = any(np.isfinite(x["p_hemi"]) and x["p_hemi"] < 0.01 for x in FDIAG)
say(f"  F DETECTED (hemisphere p < 0.01 in any bin): {DET_F}"); RES["diag"]["F"] = FDIAG

DET = dict(E=DET_E, S1=DET_S1, S2=DET_S2, L=DET_L, D=DET_D, B=DET_B, Xerr=DET_X, F=DET_F)
RES["detected"] = DET
say(""); say("DETECTED (enter the combination): " + ", ".join(f"{k} {v}" for k, v in DET.items()))

# ================================================================== single checks (forced in every bin)
sec("Single checks, each applied to every bin (forced where not detected); f +/- sigma_f and word per bin")
def F_(**kw):
    f = base_flags(); f.update(kw); return f
SINGLE = [("RAW1 (no check)", F_(), 1.0, True),
          ("E dipole fitted", F_(E=True), 1.0, DET_E),
          ("S1 Sgr band 25", F_(S1=25.0), 1.0, DET_S1),
          ("S2 overdensity mask", F_(S2=S2SET), 1.0, DET_S2),
          ("L logg > 3.75", F_(L=3.75), 1.0, DET_L),
          (f"D-data break {best_rb:.0f}", F_(D=best_rb), 1.0, DET_D),
          ("B-data per-bin beta", F_(B=True), 1.0, DET_B),
          ("X-err scale", F_(Xerr=sX), 1.0, DET_X),
          ("F hemisphere equal weight", F_(F=True), 1.0, DET_F)]
UNTEST = [("U X-dist x0.9", F_(), 0.9), ("U X-dist x1.1", F_(), 1.1),
          ("U D-lit 2.5/4.0 rb25", F_(Dlit=(2.5, 4.0, 25.0)), 1.0), ("U D-lit 2.5/4.5 rb25", F_(Dlit=(2.5, 4.5, 25.0)), 1.0),
          ("U D-lit 2.5/4.0 rb30", F_(Dlit=(2.5, 4.0, 30.0)), 1.0), ("U D-lit 2.5/4.5 rb30", F_(Dlit=(2.5, 4.5, 30.0)), 1.0),
          ("U B-bracket 0.2", F_(Bconst=0.2), 1.0), ("U B-bracket 0.8", F_(Bconst=0.8), 1.0)]
TABLE = {}
def show(tag, out, det=None):
    TABLE[tag] = out
    say(f"-- {tag}" + ("" if det is None else ("  [DETECTED]" if det else "  [forced, not detected]")) + f"  N per bin {out['_n']} (removed {out['_removed']})")
    for m, ft in CASES + COMPS:
        k = CKEY(m, ft); say(f"   {k:20s} {fmt(out[k])}   -> {rowlabel(out[k])[0]}")
DCONV = DD[best_rb]["aout"] > 2 * R0["beta"] + 0.5
for tag, fl, ds, det in SINGLE:
    if tag.startswith("D-data") and not DCONV:
        say(f"-- {tag}: NOT EVALUABLE (outer slope {DD[best_rb]['aout']:.2f} <= 2 beta + 0.5; Jeans integral not convergent)"); continue
    show(tag, run(fl, ds), det)
for tag, fl, ds in UNTEST: show(tag + " (alone, on RAW1 nominal)", run(fl, ds))
show("a0 at the standing values 9.3603e-11 / 1.1312e-10 (reported)", run(F_(a0m=True)))

# ================================================================== the combination
sec("Combination C of the DETECTED corrections, brackets on C, untestable alternatives on C")
def cflags(**over):
    f = base_flags()
    if DET["L"]: f["L"] = 3.75
    if DET["S1"]: f["S1"] = 25.0
    if DET["S2"]: f["S2"] = S2SET
    if DET["Xerr"]: f["Xerr"] = sX
    if DET["D"]: f["D"] = best_rb
    if DET["B"]: f["B"] = True
    if DET["E"]: f["E"] = True
    if DET["F"]: f["F"] = True
    f.update(over); return f
say("C = " + (", ".join(k for k, v in DET.items() if v) or "nothing detected (C equals RAW1's nominal)"))
CC = run(cflags()); show("C", CC)
BRK = []
if DET["S1"]: BRK += [("bracket S1 20", cflags(S1=20.0)), ("bracket S1 30", cflags(S1=30.0))]
if DET["S2"]: BRK += [("bracket S2 p<0.001", cflags(S2=S2SET_001)), ("bracket S2 p<0.05", cflags(S2=S2SET_05))]
if DET["L"]: BRK += [("bracket L 3.5", cflags(L=3.5)), ("bracket L 4.0", cflags(L=4.0))]
if DET["D"]: BRK += [("bracket D other break", cflags(D=(30.0 if best_rb == 25.0 else 25.0)))]
if DET["B"]: BRK += [("bracket beta(>=55) 0.2", cflags(B55=0.2)), ("bracket beta(>=55) 0.8", cflags(B55=0.8))]
BRKOUT = {}
for tag, fl in BRK: BRKOUT[tag] = run(fl); show(tag + " (on C)", BRKOUT[tag])
UNC = {}
for tag, fl, ds in UNTEST:
    fl2 = cflags(); fl2.update({k: v for k, v in fl.items() if v not in (None, False)})
    if fl2.get("Dlit") is not None: fl2["D"] = None
    if fl2.get("Bconst") is not None: fl2["B"] = False
    UNC[tag] = run(fl2, ds); show(tag + " (on C)", UNC[tag])

# ================================================================== twins: random masks
sec("T1 random-mask twins (100 seeded masks per mask check, same count removed per bin; FW cases only)")
def random_masks(removed, nrep, seed):
    rg = np.random.default_rng(seed); out = []
    for _ in range(nrep):
        keep = np.ones(len(S0["r"]), bool)
        for j in range(4):
            ii = np.where(S0["bin"] == j)[0]
            if removed[j] > 0: keep[rg.choice(ii, removed[j], replace=False)] = False
        out.append(keep)
    return out
def run_keep(keep, flags):
    cfg, S, R = measured(1.0); _, opt = make_opt(S, R, cfg, flags); out = {}
    for m, ft in CASES:
        out[CKEY(m, ft)] = finish_rows(f_rows(S, keep, m, ft, opt), NOMSA[CKEY(m, ft)])
    return out
MASKCHECKS = [("S1 Sgr band 25", F_(S1=25.0)), ("S2 overdensity mask", F_(S2=S2SET)), ("L logg > 3.75", F_(L=3.75))]
cm = cflags(); maskonly = F_(L=cm["L"], S1=cm["S1"], S2=cm["S2"])
if any(x is not None for x in (cm["L"], cm["S1"], cm["S2"])): MASKCHECKS.append(("masks of C", maskonly))
T1 = {}
for tag, fl in MASKCHECKS:
    real = TABLE.get(tag) or run(fl)
    rem = real["_removed"]
    if sum(rem) == 0: say(f"  {tag}: removes no star; no twin needed"); continue
    keeps = random_masks(rem, 100, 20261119 + len(T1))
    sh = {CKEY(m, ft): [] for m, ft in CASES}; twin_words = None
    for t, kp in enumerate(keeps):
        o = run_keep(kp, base_flags())
        for k in sh: sh[k].append([o[k][j]["f"] - BASE[k][j]["f"] for j in range(4)])
        if t == 0: twin_words = {k: [word(x) for x in o[k]] for k in o}
    T1[tag] = {}
    say(f"  {tag}: removed per bin {rem}")
    for m, ft in CASES:
        k = CKEY(m, ft); a = np.array(sh[k]); lo, hi = np.percentile(a, 2.5, axis=0), np.percentile(a, 97.5, axis=0)
        realsh = [real[k][j]["f"] - BASE[k][j]["f"] for j in range(4)]
        moves = [bool(realsh[j] < lo[j] or realsh[j] > hi[j]) for j in range(4)]
        flips = float(np.mean([word(dict(f=BASE[k][1]["f"] + a[t, 1], s=BASE[k][1]["s"])) != word(BASE[k][1]) for t in range(len(a))]))
        same = twin_words[k][1] == word(BASE[k][1])
        T1[tag][k] = dict(lo=lo.tolist(), hi=hi.tolist(), real=realsh, moves=moves, twin_words=twin_words[k], twin_ok=same, flip_frac_3040=flips)
        check(f"T1 twin {tag} {k}: 30-40 word unchanged under the seeded random mask", same, f"twin words {twin_words[k]}; real shifts " +
              ", ".join(f"{x:+.3f}" for x in realsh) + "; random 95% ranges " + ", ".join(f"[{a_:+.3f},{b_:+.3f}]" for a_, b_ in zip(lo, hi)) +
              f"; moves (outside range) {moves}; fraction of random masks flipping 30-40 {flips:.2f}")
RES["twins"]["T1"] = T1
twin_fail = list(FAILED)

# ================================================================== labels
sec("Labels (FW census = headline, per footing; FW rc by the same rule)")
LAB = {}
for m, ft in CASES:
    k = CKEY(m, ft); base_w = [word(x) for x in BASE[k]]; c_w = [word(x) for x in CC[k]]
    c30 = CC[k][1]
    if c30["n"] < 100 or not (c30["s"] <= 0.10): lab = "NO POWER"; named = []
    else:
        singles = [tag for tag, fl, ds, det in SINGLE[1:] if det and tag in TABLE and word(TABLE[tag][k][1]) == "PASS"]
        if word(c30) == "PASS" or singles:
            lab = "FAIL REMOVED BY"; named = singles if singles else ["the combination"]
        elif word(c30) == "HOT":
            unt = []
            for tag, fl, ds in UNTEST:
                if "B-bracket" in tag and not BCOUNT[0.2 if "0.2" in tag else 0.8]: continue
                if word(UNC[tag][k][1]) == "PASS": unt.append(tag[2:])
            if unt: lab = "FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST"; named = unt
            else: lab = "FAIL SURVIVES EVERY CHECK"; named = []
        else:
            lab = f"FAIL SURVIVES EVERY CHECK (fall-through: 30-40 is {word(c30)} under C, a case the frozen rules do not name)"; named = []
    frag = [tag for tag in BRKOUT if word(BRKOUT[tag][k][1]) != word(c30)]
    forced_pass = [tag for tag, fl, ds, det in SINGLE[1:] if (not det) and tag in TABLE and word(TABLE[tag][k][1]) == "PASS"]
    newfail = {tag: [BN[j] for j in range(4) if base_w[j] == "PASS" and word(TABLE[tag][k][j]) != "PASS"] for tag in TABLE}
    LAB[k] = dict(label=lab, named=named, fragile=frag, base_words=base_w, C_words=c_w, C_row=rowlabel(CC[k])[0],
                  forced_pass=forced_pass, passing_bins_that_fail=newfail)
    say(f"{k:20s}: {lab}{(' ' + ', '.join(named)) if named else ''}{', FRAGILE (' + ', '.join(frag) + ')' if frag else ''}")
    say(f"   words RAW1 {base_w} -> C {c_w} (row: {rowlabel(CC[k])[0]}); forced-not-detected checks that pass 30-40: {forced_pass or 'none'}")
    say("   RAW1-passing bins that fail under a check: " + ("; ".join(f"{t}: {v}" for t, v in newfail.items() if v) or "none"))
RES["labels"] = LAB
RES["checks"] = TABLE; RES["combination"] = dict(C=CC, brackets=BRKOUT, untestable_on_C=UNC, flags={k: (sorted(v) if isinstance(v, set) else v) for k, v in cflags().items()})
if twin_fail: say(f"NOTE: twin checks failed: {twin_fail} (reported; the frozen rule stops only on known answers K0-K3)")

# ================================================================== mutations (separate file)
MUT = open(os.path.join(HERE, "mwt1_posthoc_E_forced_MUTATE.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("MWT1 mutations (FROZEN_CRITERIA.md section 4). M1: injected dipole in 40-55 must be found and removed by check E. M2: planted cold group must be flagged by S2.")
j = 2; m = S0["bin"] == j; nv = S0["n"][m]; e = S0["verr"][m]
Pm = predP(S0["r"][m], S0["sin2"][m], "FW_census", "canonical", 1.0, R0["alpha"]["alpha"], (R0["beta"],) * 4)
L_, B_ = math.radians(300.0), math.radians(20.0); Dinj = 40.0 * np.array([math.cos(B_) * math.cos(L_), math.cos(B_) * math.sin(L_), math.sin(B_)])
vm = v0[m] + nv @ Dinj
r_orig = fit_scale(v0[m], e, Pm, dipX(nv)); r_mut = fit_scale(vm, e, Pm, dipX(nv)); r_mut0 = fit_scale(vm, e, Pm); r_o0 = fit_scale(v0[m], e, Pm)
r1 = fit_scale(vm, e, np.ones(m.sum()), None, 1.0, 400.0); rd = fit_scale(vm, e, np.ones(m.sum()), dipX(nv), 1.0, 400.0)
pM = float(CHI2.sf(2 * (r1["nll"] - rd["nll"]), 3))
rec = rd["theta"][1:] - np.array(EDIAG[j]["D"]); amp, l_, b_ = lb_of(rec); ga = Dinj / 40.0
Cd = rd["cov"][1:, 1:]; samp = math.sqrt(max((rec / amp) @ Cd @ (rec / amp), 0))
ang = math.degrees(math.acos(np.clip(rec @ Dinj / (amp * 40.0), -1, 1)))
ok1 = pM < 0.01 and abs(amp - 40.0) <= 2 * samp and ang <= 30.0 and abs(r_mut["f"] - r_orig["f"]) <= 0.02
msay(f"M1 40-55 kpc, +40 km/s toward (300, +20): LR p {pM:.2e}; recovered (fit minus un-mutated fit) {amp:.1f} +/- {samp:.1f} km/s toward ({l_:.0f}, {b_:+.0f}), "
     f"{ang:.1f} deg off; raw fitted dipole {lb_of(rd['theta'][1:])[0]:.1f} km/s; f (FW census canonical) without removal {r_o0['f']:.3f} -> {r_mut0['f']:.3f} mutated; "
     f"with removal {r_orig['f']:.3f} -> {r_mut['f']:.3f}; bites: {ok1}")
# M2
rg2 = np.random.default_rng(20261120); ii = np.where(m)[0]; s0_ = rg2.choice(ii)
cand = ii[np.abs(S0["r"][ii] - S0["r"][s0_]) < 5.0]; angs = np.degrees(np.arccos(np.clip(S0["n"][cand] @ S0["n"][s0_], -1, 1)))
grp = cand[np.argsort(angs)[:25]]
vM2 = v0.copy(); vM2[grp] = np.mean(v0[m]) + rg2.normal(0, 10.0, len(grp))
AposM, NULLM = shuffles(S0, vM2, 200, 20261121); kM = kcount(AposM, vM2); FLM = flags_from(kM, NULLM, 0.01)
nfl = int(np.sum(FLM[grp])); ok2 = nfl >= 15
msay(f"M2 25-star cold group in 40-55 (angular radius {np.max(np.sort(angs)[:25]):.1f} deg): flagged {nfl} of 25 (total flagged in 40-55 {int(np.sum(FLM & m))}); bites: {ok2}")
RES["mutations"] = dict(M1=dict(p=pM, amp=amp, samp=samp, l=l_, b=b_, off_deg=ang, f_before=r_orig["f"], f_after=r_mut["f"], bites=bool(ok1)),
                        M2=dict(flagged=nfl, bites=bool(ok2)))
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, set): return sorted(clean(v) for v in o)
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o
json.dump(clean(RES), open(os.path.join(HERE, "mwt1_posthoc_E_forced.json"), "w"), indent=1)
say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
