#!/usr/bin/env python3
"""CFG433 - T13 phantom dispersion vs Milky Way satellites (spherical Jeans, beta from 3D motions).

Data: Fritz et al. 2018, A&A 619, A103, Table 2 (arXiv:1805.00908 source), read from
../_external_data/cfg433_work/src/UFDsmot_arx_final.tex (not committed; see FETCH_LOG.md there).
Prediction: V_pred^2 = r g_N nu(g_N/a0), nu = 1/(1-exp(-sqrt y)), point-mass MW baryons.
Estimator: V_c^2 = <v_t^2> + (gamma-2)<v_r^2>  (alpha=0 3D tracer / Jeans estimator).
Criteria: FROZEN_CRITERIA.md (committed before this script).  CFG433_MUTATE=1 -> MUTATE run.
"""
import json, math, os, re, sys
import numpy as np
from scipy.integrate import quad

MUT = os.environ.get("CFG433_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(REPO, "..", "_external_data", "cfg433_work", "src", "UFDsmot_arx_final.tex")

G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MB_PRIMARY, MB_HI, MB_T13 = 6.0e10, 7.3e10, 1.0e11
LMC_CAND = {"CarII", "CarIII", "HorI", "HyiI", "RetII", "TucII"}
NBOOT = 10000
RNG = np.random.default_rng(433)


# ---------------------------------------------------------------- data
def parse_table():
    txt = open(TEX).read()
    i0 = txt.index(r"\label{KapSou2}")
    i1 = txt.index(r"\end{table*}", i0)
    block = txt[i0:i1]
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line or "&" not in line or line.startswith("satellite") or line.startswith("&"):
            continue
        c = [x.strip() for x in line.rstrip("\\").split("&")]
        if len(c) < 9:
            continue
        name = c[0]
        d = float(c[1])
        def asym(s):
            m = re.match(r"([-\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}", s.replace(" ", ""))
            return float(m.group(1)), float(m.group(2)), float(m.group(3))
        def sym(s):
            a, b = s.replace(" ", "").split(r"\pm")
            return float(a), float(b)
        v3, v3p, v3m = asym(c[6])
        vr, er = sym(c[7])
        vt, etp, etm = asym(c[8].rstrip("\\").strip())
        rows.append(dict(name=name, d=d, v3=v3, e3=0.5 * (v3p + v3m), vr=vr, er=er, vt=vt, et=0.5 * (etp + etm)))
    return rows


# ---------------------------------------------------------------- prediction
def nu(y):
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def vpred(r_kpc, mb, a0):
    r = np.asarray(r_kpc, float) * KPC
    gN = G * mb * MSUN / r ** 2
    return np.sqrt(r * gN * nu(gN / a0)) / 1e3


# ---------------------------------------------------------------- estimator
def gamma_ml(r, lo, hi):
    """ML index of n ~ r^-g truncated to [lo, hi] (3D): p(r) ~ r^(2-g)."""
    s = np.mean(np.log(np.asarray(r, float)))
    k = 3.0 - _GS
    with np.errstate(divide="ignore", invalid="ignore"):
        norm = np.where(np.abs(k) < 1e-9, math.log(hi / lo), (hi ** k - lo ** k) / k)
    ll = (2.0 - _GS) * s - np.log(norm)
    return float(_GS[np.argmax(ll)])


_GS = np.linspace(0.05, 6.0, 1191)  # step 0.005


def vc_est(vr, er, vt, et, gam):
    mr = np.mean(vr ** 2 - er ** 2)
    mt = np.mean(vt ** 2 - et ** 2)
    v2 = mt + (gam - 2.0) * mr
    beta = 1.0 - mt / (2.0 * mr) if mr > 0 else np.nan
    return (math.sqrt(v2) if v2 > 0 else float("nan")), beta, mr, mt


def analyse(S, lo, hi, gamma_fixed=None, qcut=None, nboot=NBOOT, rng=None):
    """S: list of dict rows already window-selected. gamma from all S; quality cut after."""
    rng = RNG if rng is None else rng
    r_all = np.array([s["d"] for s in S])
    q = np.array([(qcut is None) or (s["et"] <= qcut) for s in S])
    vr = np.array([s["vr"] for s in S]); er = np.array([s["er"] for s in S])
    vt = np.array([s["vt"] for s in S]); et = np.array([s["et"] for s in S])
    gam = gamma_fixed if gamma_fixed is not None else gamma_ml(r_all, lo, hi)
    V, beta, mr, mt = vc_est(vr[q], er[q], vt[q], et[q], gam)
    n = len(S)
    boots = []
    for _ in range(nboot):
        idx = rng.integers(0, n, n)
        g_b = gamma_fixed if gamma_fixed is not None else gamma_ml(r_all[idx], lo, hi)
        qi = idx[q[idx]]
        if len(qi) < 3:
            continue
        Vb = vc_est(vr[qi], er[qi], vt[qi], et[qi], g_b)[0]
        boots.append(Vb)
    boots = np.array(boots)
    nbad = int(np.sum(~np.isfinite(boots)))
    bf = boots[np.isfinite(boots)]
    lo16, hi84 = np.percentile(bf, [16, 84]) if len(bf) else (np.nan, np.nan)
    return dict(V=V, beta=beta, gamma=gam, mr=mr, mt=mt, n_sel=int(q.sum()), n_win=n,
                sig=0.5 * (hi84 - lo16), p16=lo16, p84=hi84, nbad=nbad,
                r_med=float(np.median(r_all[q])), r_q=r_all[q])


# ---------------------------------------------------------------- mocks
def jeans_sigr2(r_kpc, gam, beta, mb, a0, vfac=1.0):
    """sigma_r^2(r) = r^(gam-2beta) int_r^inf r'^(2beta-gam-1) V^2(r') dr'  (km/s)^2."""
    f = lambda x: x ** (2 * beta - gam - 1.0) * (vfac * vpred(x, mb, a0)) ** 2
    out = []
    for r in np.atleast_1d(r_kpc):
        I = quad(f, r, np.inf, limit=400)[0]
        out.append(r ** (gam - 2 * beta) * I)
    return np.array(out)


def make_mock(n, lo, hi, gam, beta, errs, mb, a0, rng, vfac=1.0, n_kin=None):
    k = 3.0 - gam
    u = rng.random(n)
    r = (lo ** k + u * (hi ** k - lo ** k)) ** (1.0 / k) if abs(k) > 1e-9 else lo * (hi / lo) ** u
    s2 = jeans_sigr2(r, gam, beta, mb, a0, vfac)
    sr = np.sqrt(s2); st1 = sr * math.sqrt(max(1.0 - beta, 0.0))
    ei = rng.integers(0, len(errs), n)
    er = errs[ei, 0]; et = errs[ei, 1].copy()
    if n_kin is not None and n_kin < n:
        # mimic the primary: all n radii feed gamma, only n_kin objects pass the e_t <= 50 cut
        drop = rng.choice(n, n - n_kin, replace=False)
        et[drop] = 999.0
    vr = rng.normal(0, sr) + rng.normal(0, er)
    vth = rng.normal(0, st1) + rng.normal(0, et / math.sqrt(2))
    vph = rng.normal(0, st1) + rng.normal(0, et / math.sqrt(2))
    vt = np.hypot(vth, vph)
    rows = [dict(name=f"m{i}", d=r[i], vr=vr[i], er=er[i], vt=vt[i], et=et[i]) for i in range(n)]
    kin = et < 999.0
    vtrue = float(np.mean(vfac * vpred(r[kin], mb, a0)))
    return rows, vtrue


def verdict(D, Dvars):
    if abs(D) <= 2:
        return "PASS"
    if abs(D) <= 3:
        return "TENSION"
    sgn = np.sign(D)
    if all(abs(x) > 2 and np.sign(x) == sgn for x in Dvars):
        return "FAIL"
    return "TENSION"


# ================================================================= main
out = {}
P = print
rows = parse_table()
P(f"CFG433 T13 phantom dispersion vs MW satellites   MUTATE={MUT}")
P(f"Fritz+2018 Table 2 rows parsed: {len(rows)}")
# C1
ok = 0
for s in rows:
    comb = math.sqrt(s["e3"] ** 2 + s["er"] ** 2 + s["et"] ** 2)
    v3c = math.sqrt(s["vr"] ** 2 + s["vt"] ** 2)
    ok += abs(s["v3"] - v3c) <= 2 * comb * 1.0 + 1e-9
c1 = (len(rows) == 39) and ok >= 37
P(f"C1 parse: 39 rows = {len(rows) == 39}; V3D vs sqrt(Vrad^2+Vtan^2) within 2 sigma: {ok}/39  PASS={c1}")

# C3
rr = np.linspace(30, 300, 200)
c3 = True
for f, a0 in A0.items():
    vp = vpred(rr, MB_PRIMARY, a0)
    deep = (G * MB_PRIMARY * MSUN * a0) ** 0.25 / 1e3
    var = vp.max() / vp.min() - 1
    c3 &= var < 0.10
    P(f"C3 {f:9s}: V_pred 30-300 kpc = {vp.max():.1f} -> {vp.min():.1f} km/s (spread {100*var:.1f} %); (G M_b a0)^1/4 = {deep:.1f} km/s; "
      f"V_pred(300)/deep = {vp[-1]/deep:.4f}")
P(f"C3 flat-potential appropriate (<10 %)  PASS={c3}")

LO, HI = 30.0, 300.0
win = [s for s in rows if LO <= s["d"] <= HI]
P(f"\nwindow 30-300 kpc: {len(win)} objects: {', '.join(s['name'] for s in win)}")


def run_variants(win_rows, label=""):
    res = {}
    res["PRIMARY"] = analyse(win_rows, LO, HI, qcut=50)
    res["V1 no quality cut"] = analyse(win_rows, LO, HI, qcut=None)
    res["V2 e_t<=100"] = analyse(win_rows, LO, HI, qcut=100)
    res["V3 no LMC candidates"] = analyse([s for s in win_rows if s["name"] not in LMC_CAND], LO, HI, qcut=50)
    res["V4 no Leo I"] = analyse([s for s in win_rows if s["name"] != "LeoI"], LO, HI, qcut=50)
    res["V5 inner 30-100"] = analyse([s for s in win_rows if s["d"] <= 100], LO, 100.0, qcut=50)
    res["V6 outer 100-300"] = analyse([s for s in win_rows if s["d"] > 100], 100.0, HI, qcut=50)
    res["V7 gamma=2"] = analyse(win_rows, LO, HI, gamma_fixed=2.0, qcut=50)
    res["V8 gamma=3"] = analyse(win_rows, LO, HI, gamma_fixed=3.0, qcut=50)
    return res


def score(res, label):
    table = {}
    for f, a0 in A0.items():
        P(f"\n  --- footing {f} (a0 = {a0:.4e}) {label}")
        P(f"  {'case':22s} {'n':>3s} {'gamma':>6s} {'beta':>6s} {'V_obs':>7s} {'sig':>6s} {'r_med':>6s} {'V_pred':>7s} {'D':>6s}   V_pred range over radii")
        Ds = {}
        for k, R in res.items():
            vp = float(vpred(R["r_med"], MB_PRIMARY, a0))
            rng_ = vpred(R["r_q"], MB_PRIMARY, a0)
            D = (R["V"] - vp) / R["sig"]
            Ds[k] = D
            P(f"  {k:22s} {R['n_sel']:3d} {R['gamma']:6.2f} {R['beta']:6.2f} {R['V']:7.1f} {R['sig']:6.1f} {R['r_med']:6.0f} {vp:7.1f} {D:+6.2f}   "
              f"[{rng_.min():.1f}, {rng_.max():.1f}]  (bad boots {R['nbad']})")
        Rp = res["PRIMARY"]
        vp9 = float(vpred(Rp["r_med"], MB_HI, a0))
        D9 = (Rp["V"] - vp9) / Rp["sig"]
        Ds["V9 M_b=7.3e10"] = D9
        vpt = float(vpred(Rp["r_med"], MB_T13, a0))
        P(f"  {'V9 M_b=7.3e10':22s} {'':3s} {'':6s} {'':6s} {Rp['V']:7.1f} {Rp['sig']:6.1f} {Rp['r_med']:6.0f} {vp9:7.1f} {D9:+6.2f}")
        P(f"  (ref) M_b=1e11 (T13's value): V_pred = {vpt:.1f}, D = {(Rp['V']-vpt)/Rp['sig']:+.2f}")
        V_ = verdict(Ds["PRIMARY"], [v for k, v in Ds.items() if k != "PRIMARY"])
        P(f"  isotropic-equivalent sigma = V_obs/sqrt2 = {Rp['V']/math.sqrt(2):.1f} km/s vs T13-style sigma_ph(M_b=6e10) = {vp/math.sqrt(2) if False else float(vpred(Rp['r_med'], MB_PRIMARY, a0))/math.sqrt(2):.1f}")
        P(f"  VERDICT ({f}): {V_}   D_primary = {Ds['PRIMARY']:+.2f}")
        table[f] = dict(D=Ds, verdict=V_, V_obs=Rp["V"], sig=Rp["sig"], V_pred=float(vpred(Rp["r_med"], MB_PRIMARY, a0)))
    return table


def naive(win_rows):
    S = [s for s in win_rows if s["et"] <= 50]
    r_all = np.array([s["d"] for s in win_rows])
    gam = gamma_ml(r_all, LO, HI)
    v3sq = np.mean([s["vr"] ** 2 - s["er"] ** 2 + s["vt"] ** 2 - s["et"] ** 2 for s in S])
    return math.sqrt(gam * v3sq / 3.0), gam


if not MUT:
    res = run_variants(win)
    Rp = res["PRIMARY"]
    P(f"\nPRIMARY sample (e_t<=50): {Rp['n_sel']} objects; gamma_ML = {Rp['gamma']:.3f} (from {Rp['n_win']} in window); "
      f"<v_r^2>^1/2 = {math.sqrt(Rp['mr']):.1f}, <v_t^2>^1/2 = {math.sqrt(Rp['mt']):.1f} km/s; beta = {Rp['beta']:.3f}")
    P(f"  V_c,obs = {Rp['V']:.1f} km/s  (16-84: {Rp['p16']:.1f} - {Rp['p84']:.1f})")
    vn, gn = naive(win)
    s1d = math.sqrt((Rp['mr'] + Rp['mt']) / 3.0)
    P(f"  naive 1D rms sigma = sqrt(<v3D^2>/3) = {s1d:.1f} km/s vs T13 sigma_ph = (G M_b a0)^1/4/sqrt2: "
      + ", ".join(f"{f} {(G*mb*MSUN*a0)**0.25/1e3/math.sqrt(2):.1f} (M_b {mb:.1e})" for f, a0 in A0.items() for mb in (MB_PRIMARY, MB_T13)))
    P(f"  M3-style naive (beta forced 0): V = sqrt(gamma <v3D^2>/3) = {vn:.1f} km/s (difference {abs(vn-Rp['V'])/Rp['sig']:.2f} sigma)")
    tab = score(res, "")
    out["main"] = {f: dict(verdict=t["verdict"], D={k: float(v) for k, v in t["D"].items()}, V_obs=t["V_obs"], sig=t["sig"], V_pred=t["V_pred"]) for f, t in tab.items()}
    out["primary"] = dict(n=Rp["n_sel"], gamma=Rp["gamma"], beta=Rp["beta"], V=Rp["V"], sig=Rp["sig"], r_med=Rp["r_med"])

    # C2 mock recovery
    P("\nC2 mock recovery (300 mocks, exact kernel potential, canonical, M_b primary, beta = beta_obs)")
    errs = np.array([[s["er"], s["et"]] for s in win if s["et"] <= 50])
    rngm = np.random.default_rng(4331)
    rec, cov, nm = [], 0, 300
    for i in range(nm):
        mrows, vt = make_mock(Rp["n_win"], LO, HI, Rp["gamma"], Rp["beta"], errs, MB_PRIMARY, A0["canonical"], rngm, n_kin=Rp["n_sel"])
        R = analyse(mrows, LO, HI, qcut=50, nboot=300, rng=rngm)
        rec.append(R["V"] / vt)
        cov += (R["p16"] <= vt <= R["p84"])
    rec = np.array(rec); rf = rec[np.isfinite(rec)]
    bias = np.mean(rf) - 1
    covf = cov / nm
    c2 = abs(bias) <= 0.03 and 0.50 <= covf <= 0.85
    P(f"  mean V_rec/V_true = {np.mean(rf):.4f} (bias {100*bias:+.2f} %), median {np.median(rf):.4f}, scatter {np.std(rf):.3f}; "
      f"1-sigma coverage {covf:.2f}; non-finite {nm-len(rf)}  PASS={c2}")
    P(f"  (each mock: {Rp['n_win']} radii feed gamma, {Rp['n_sel']} random objects carry the primary sample's errors and pass the e_t<=50 cut, as in the data)")
    out["controls"] = dict(C1=bool(c1), C2=bool(c2), C3=bool(c3), C2_bias=float(bias), C2_cov=float(covf))
    allc = c1 and c2 and c3
    P(f"\nCONTROLS C1 {c1}  C2 {c2}  C3 {c3}  -> all pass: {allc}")
    P("\nHEADLINE: " + "; ".join(f"{f}: {t['verdict']} (V_obs {t['V_obs']:.1f} +- {t['sig']:.1f} vs V_pred {t['V_pred']:.1f}, D {t['D']['PRIMARY']:+.2f})" for f, t in tab.items()))
    P("(Diagnosticity is set by the MUTATE run, cfg433_satellite_jeans_MUTATE.out.)")
else:
    # M1 planted mocks
    res0 = run_variants(win)
    Rp = res0["PRIMARY"]
    errs = np.array([[s["er"], s["et"]] for s in win if s["et"] <= 50])
    rngm = np.random.default_rng(4332)
    a0 = A0["canonical"]
    P(f"M1 planted mocks (n = {Rp['n_win']} radii / {Rp['n_sel']} kinematic, gamma {Rp['gamma']:.2f}, beta {Rp['beta']:.2f}, canonical, 100 each)")
    m1 = {}
    for vf in (1.0, 1.35):
        nfail = npass = 0
        for i in range(100):
            mrows, vt = make_mock(Rp["n_win"], LO, HI, Rp["gamma"], Rp["beta"], errs, MB_PRIMARY, a0, rngm, vfac=vf, n_kin=Rp["n_sel"])
            R = analyse(mrows, LO, HI, qcut=50, nboot=300, rng=rngm)
            D = (R["V"] - float(vpred(R["r_med"], MB_PRIMARY, a0))) / R["sig"]
            nfail += D > 3
            npass += abs(D) <= 2
        m1[vf] = (npass, nfail)
        P(f"  V_c x {vf:.2f}: PASS(|D|<=2) {npass}/100, D>3 {nfail}/100")
    m1ok = m1[1.0][0] >= 80 and m1[1.35][1] >= 80
    P(f"M1 power check (unmodified PASS >= 80, x1.35 FAIL >= 80): {m1ok}")
    # M2 scaled real data
    main = json.load(open(os.path.join(HERE, "cfg433_results.json")))["main"]
    m2 = {}
    for sc in (1.35, 1 / 1.35):
        w2 = [dict(s, vr=s["vr"] * sc, er=s["er"] * sc, vt=s["vt"] * sc, et=s["et"] * sc) for s in win]
        # quality cut is applied in the scaled units as frozen (e_t <= 50 km/s on the scaled errors)
        res = run_variants(w2)
        P(f"\nM2 real velocities x {sc:.4f}")
        tab = score(res, f"[x{sc:.3f}]")
        m2[sc] = {f: t["verdict"] for f, t in tab.items()}
    flips = {f: any(m2[sc][f] != main[f]["verdict"] for sc in m2) for f in A0}
    P(f"\nM2 flip vs main run: {flips}  (main: { {f: main[f]['verdict'] for f in A0} })")
    vn, gn = naive(win)
    m3 = abs(vn - Rp["V"]) / Rp["sig"]
    P(f"M3 anisotropy-blind V = {vn:.1f} vs primary {Rp['V']:.1f}: {m3:.2f} sigma apart (informational; >1 means anisotropy matters: {m3 > 1})")
    diag = m1ok and all(flips.values())
    P(f"\nMUTATE SUMMARY: M1 {m1ok}; M2 flips {flips}; test DIAGNOSTIC = {diag}")
    out["mutate"] = dict(M1={str(k): v for k, v in m1.items()}, M1_ok=bool(m1ok), M2=m2 and {str(k): v for k, v in m2.items()},
                         M2_flips=flips, M3_sigma=float(m3), diagnostic=bool(diag))

json.dump(out, open(os.path.join(HERE, f"cfg433_results{TAG}.json"), "w"), indent=1, default=float)
