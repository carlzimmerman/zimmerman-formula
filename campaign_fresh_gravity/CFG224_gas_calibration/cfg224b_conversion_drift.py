#!/usr/bin/env python3
"""CFG224b -- the redshift dependence of the gas-mass conversion factors (Dunne+22 per-galaxy optimisation tables joined to z by name) and ACE's dust-to-CO ratio at z ~ 2.2 against Stripe82 at fixed metallicity.
Frozen criteria: FROZEN_CRITERIA_B.md here (3b1c554e0), committed before any conversion-factor statistic.  Dunne+22's optimised conversions make the tracer masses agree by construction: the informative content is how the
factors themselves vary with z.  Conversions as the sources optimise / adopt them.  kappa = 1/2 FITTED.  No law verdict.
Run: python3 campaign_fresh_gravity/CFG224_gas_calibration/cfg224b_conversion_drift.py        (MUTATE=1: +0.30 dex on every log alpha_CO at z >= 1.6)"""
import os, sys, csv, json, math, time
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MG = os.path.join(REPO, "data_assembly", "multitracer_gas")
DD = os.path.join(MG, "dunne2022")
MUT = os.environ.pop("MUTATE", "").strip() == "1"
OUT, CHK = [], []
T0 = time.time()
SEED, NBOOT = 224, 10000
LN10 = math.log(10)


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def f(x):
    try:
        v = float(str(x).strip())
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def rd(path):
    return list(csv.DictReader(open(path, newline="")))


P(__doc__.split("Run:")[0].strip())
BINS = [("B1 z<0.6", 0.0, 0.6), ("B2 0.6<=z<1.6", 0.6, 1.6), ("B3 1.6<=z<3.0", 1.6, 3.0), ("B4 z>=3.0", 3.0, 99.0)]


def binof(z):
    for b in BINS:
        if b[1] <= z < b[2]:
            return b[0]
    return None


def cls(K):
    return "below the CFG223 range" if K < 0.05 else ("inside the CFG223 range" if K < 0.10 else ("between the CFG223 and CFG221 requirements" if K < 0.15 else "at or above the CFG221 requirement"))


# ---- Dunne+22: master and the four optimisation tables
master = rd(os.path.join(DD, "dunne2022_master.csv"))
ix = {}
for i, r in enumerate(master):
    for k in ("Name", "OName", "SimbadName"):
        v = r[k].strip()
        if v:
            ix.setdefault(v, []).append(i)
TABLES = {"daX": ("dunne2022_opt_dax.csv", [("alpha_CO", "aCO", "e_aCO"), ("X_CI", "XCI", "e_XCI"), ("GDR", "GDR", "e_GDR")]),
          "ad": ("dunne2022_opt_ad.csv", [("alpha_CO", "aCO", "e_aCO"), ("kappa_H", "kappaH", "e_kappaH")]),
          "xa": ("dunne2022_opt_xa.csv", [("alpha_CO", "aCO", "e_aCO"), ("X_CI", "XCI", "e_XCI")]),
          "xd": ("dunne2022_opt_xd.csv", [("X_CI", "XCI", "e_XCI"), ("GDR", "GDR", "e_GDR")])}
ROWS = {}     # (table, factor) -> list of dict(z, y, sig, lir)
JOIN = {}
for tn, (fn, facs) in TABLES.items():
    tab = rd(os.path.join(DD, fn))
    matched = 0; ambiguous = 0; data = {fc[0]: [] for fc in facs}
    for r in tab:
        nm = r["Name"].strip()
        m = ix.get(nm)
        if not m:
            continue
        zs = {f(master[i]["z"]) for i in m if math.isfinite(f(master[i]["z"]))}
        if not zs:
            continue
        if len(zs) > 1:
            ambiguous += 1
        matched += 1
        i0 = m[0]
        z = f(master[i0]["z"]); lir = f(master[i0]["logLIR"])
        if not math.isfinite(lir):
            lir = f(r.get("logLIR"))
        for (fname, col, ecol) in facs:
            v = f(r.get(col)); e = f(r.get(ecol))
            if math.isfinite(v) and v > 0 and math.isfinite(z):
                y = math.log10(v)
                if MUT and fname == "alpha_CO" and z >= 1.6:
                    y += 0.30
                data[fname].append(dict(z=z, y=y, sig=(e / (v * LN10)) if (math.isfinite(e) and e > 0) else float("nan"), lir=lir))
    JOIN[tn] = dict(rows=len(tab), matched=matched, ambiguous=ambiguous)
    for fname, lst in data.items():
        ROWS[(tn, fname)] = lst
P("\nJOINS (names matched to the master table, which carries z): " + "; ".join(f"{t}: {v['matched']} of {v['rows']} rows ({v['ambiguous']} with ambiguous z)" for t, v in JOIN.items()))


def stats(y, sig=None, seed=SEED):
    y = np.asarray(y, float); n = len(y)
    o = dict(N=n)
    if n < 3:
        return o
    mu, sd = float(y.mean()), float(y.std(ddof=1)); se = sd / math.sqrt(n)
    o.update(mean=mu, sd=sd, se=se)
    if n >= 6:
        I = np.random.default_rng(seed).integers(0, n, size=(NBOOT, n)); bm = y[I].mean(axis=1)
        o["boot68"] = [float(np.percentile(bm, 16)), float(np.percentile(bm, 84))]
    if sig is not None and np.all(np.isfinite(sig)):
        o["sd_int"] = float(math.sqrt(max(0.0, sd ** 2 - float(np.mean(np.asarray(sig) ** 2)))))
    return o


P("\nPER (table, factor, bin): N, mean log10 factor, SD, SE, intrinsic SD; drift against B1 with K_direct = SE_b and K_local = sqrt(drift^2 + SE_drift^2)")
RES = {}
for (tn, fname), lst in ROWS.items():
    P(f"\n  {tn} / {fname}  (joined galaxies with z: {len(lst)})")
    base = None
    for b in BINS:
        sel = [r for r in lst if binof(r["z"]) == b[0]]
        if not sel:
            continue
        st = stats([r["y"] for r in sel], [r["sig"] for r in sel])
        RES[(tn, fname, b[0])] = st
        if st["N"] < 3:
            P(f"    {b[0]:16s} N = {st['N']} (no statistics)")
            continue
        if b[0].startswith("B1"):
            base = st
        ex = (f", 68% boot [{st['boot68'][0]:+.3f}, {st['boot68'][1]:+.3f}]" if "boot68" in st else "") + (f", intrinsic SD {st['sd_int']:.3f}" if "sd_int" in st else "")
        line = f"    {b[0]:16s} N = {st['N']:3d}: mean {st['mean']:+.3f} (factor {10 ** st['mean']:.3g}), SD {st['sd']:.3f}, SE {st['se']:.3f}{ex}"
        if base is not None and not b[0].startswith("B1"):
            dr = st["mean"] - base["mean"]; sed = math.sqrt(st["se"] ** 2 + base["se"] ** 2)
            st.update(drift=dr, se_drift=sed, K_direct=st["se"], K_local=math.sqrt(dr ** 2 + sed ** 2))
            line += f";  drift vs B1 {dr:+.3f} +- {sed:.3f}; K_direct {st['K_direct']:.3f} ({cls(st['K_direct'])}); K_local {st['K_local']:.3f} ({cls(st['K_local'])})"
        P(line)

P("\nZ SLOPE at fixed luminosity: OLS of log10 factor on log10(1+z) and (log L_IR - 11.7), bootstrap SD over galaxies (B = 10,000); and without the L_IR term")
REG = {}
for (tn, fname), lst in ROWS.items():
    L = [r for r in lst if math.isfinite(r["lir"])]
    if len(L) < 30:
        continue
    z = np.array([r["z"] for r in L]); y = np.array([r["y"] for r in L]); lir = np.array([r["lir"] for r in L]) - 11.7
    X = np.vstack([np.ones(len(L)), np.log10(1 + z), lir]).T; X0 = X[:, :2]
    beta = np.linalg.lstsq(X, y, rcond=None)[0]; beta0 = np.linalg.lstsq(X0, y, rcond=None)[0]
    I = np.random.default_rng(SEED).integers(0, len(L), size=(NBOOT // 5, len(L)))
    bb = np.array([np.linalg.lstsq(X[i], y[i], rcond=None)[0] for i in I]); bb0 = np.array([np.linalg.lstsq(X0[i], y[i], rcond=None)[0] for i in I])
    REG[f"{tn}|{fname}"] = dict(N=len(L), b=float(beta[1]), sd_b=float(bb[:, 1].std(ddof=1)), c=float(beta[2]), sd_c=float(bb[:, 2].std(ddof=1)), b0=float(beta0[1]), sd_b0=float(bb0[:, 1].std(ddof=1)))
    r_ = REG[f"{tn}|{fname}"]
    P(f"  {tn:4s} {fname:9s} N = {len(L):3d}: slope in log10(1+z) with L_IR term {r_['b']:+.3f} +- {r_['sd_b']:.3f} (L_IR coefficient {r_['c']:+.3f} +- {r_['sd_c']:.3f} per dex); without the L_IR term {r_['b0']:+.3f} +- {r_['sd_b0']:.3f}")

# ---- ACE against Stripe82 at fixed metallicity
P("\nACE (z ~ 2.2) against Stripe82 (z < 0.2) at fixed metallicity: R = log10(M_dust / M_mol,CO)")
ace = [r for r in rd(os.path.join(MG, "ace_merged_per_galaxy.csv")) if r["Mmol_CO_flag"].strip() != "<" and r["logMdust_flag"].strip() != "<" and math.isfinite(f(r["Mmol_CO_1e10"])) and math.isfinite(f(r["logMdust_2609_20926"])) and math.isfinite(f(r["OH"]))]
s82 = rd(os.path.join(MG, "stripe82_z_lt0.3_CO_dust.csv"))
zs82 = np.array([f(r["Z_12logOH"]) for r in s82]); Rs82 = np.array([f(r["logMdust"]) - f(r["logMgas_CO"]) for r in s82])
ok = np.isfinite(zs82) & np.isfinite(Rs82)
A = np.vstack([np.ones(ok.sum()), zs82[ok]]).T
coef = np.linalg.lstsq(A, Rs82[ok], rcond=None)[0]; res_sd = float((Rs82[ok] - A @ coef).std(ddof=2))
ZA = np.array([f(r["OH"]) for r in ace]); RA = np.array([f(r["logMdust_2609_20926"]) - math.log10(f(r["Mmol_CO_1e10"]) * 1e10) for r in ace])
dA = RA - (coef[0] + coef[1] * ZA)
sdA = float(dA.std(ddof=1)); seA = sdA / math.sqrt(len(dA)); KA = math.sqrt(seA ** 2 + (abs(dA.mean()) / 2) ** 2)
P(f"  Stripe82: N = {int(ok.sum())}, 12+log(O/H) {zs82[ok].min():.2f} to {zs82[ok].max():.2f}; R = {coef[0]:+.3f} {coef[1]:+.3f} x (12+log O/H), residual SD {res_sd:.3f}")
P(f"  ACE: N = {len(dA)}, 12+log(O/H) {ZA.min():.2f} to {ZA.max():.2f} ({'INSIDE' if ZA.min() >= zs82[ok].min() else 'BELOW'} Stripe82's range at the low end), R mean {RA.mean():+.3f} (SD {RA.std(ddof=1):.3f})")
P(f"  offset at fixed metallicity Delta_ACE = mean(R_ACE - R_S82(Z)) = {dA.mean():+.3f}, SD {sdA:.3f}, SE {seA:.3f}; K = sqrt(SE^2 + (|Delta|/2)^2) = {KA:.3f} ({cls(KA)})")
# POST HOC (written after seeing that Stripe82's metallicity range 8.65-8.86 lies above ACE's 8.29-8.61, so the frozen offset extrapolates the OLS slope; reported beside, not substituted)
slope_se = res_sd / (math.sqrt(int(ok.sum())) * float(zs82[ok].std(ddof=1)))
d_noext = float(RA.mean() - Rs82[ok].mean())
d_slope1 = float(RA.mean() - (Rs82[ok].mean() + 1.0 * (ZA.mean() - zs82[ok].mean())))
P(f"  POST HOC: Stripe82's OLS slope {coef[1]:+.2f} +- {slope_se:.2f} over a metallicity range of only {zs82[ok].max() - zs82[ok].min():.2f} dex, so the extrapolation to ACE's mean 12+log(O/H) {ZA.mean():.2f} (Stripe82 mean {zs82[ok].mean():.2f}) carries +-{slope_se * abs(ZA.mean() - zs82[ok].mean()):.2f} dex from the slope alone")
P(f"    offset with NO slope (difference of the two mean R): {d_noext:+.3f}; with the slope fixed at +1 (dust-to-gas proportional to metallicity): {d_slope1:+.3f}; with the frozen OLS slope: {dA.mean():+.3f}")
ACE = dict(posthoc=dict(slope_se=slope_se, delta_noslope=d_noext, delta_slope1=d_slope1), N=len(dA), delta=float(dA.mean()), sd=sdA, se=seA, K=KA, s82=dict(a=float(coef[0]), b=float(coef[1]), res_sd=res_sd, zmin=float(zs82[ok].min()), zmax=float(zs82[ok].max())), Zace=ZA.tolist(), Race=RA.tolist())

# ---- implication (CFG224's K_needed at f_gas 0.5) beside the measured K in B3 / B4
P("\nIMPLICATION (arithmetic): K_needed from CFG224 (f_gas 0.5; 0.3 to 0.7) beside the measured K_direct / K_local of alpha_CO (ad table) and the ACE K")
J224 = json.load(open(os.path.join(LANE, "cfg224_gas_calibration_results.json")))
for p in J224["implication"]:
    b = p["bin"]
    if b.startswith("B3") or b.startswith("B4"):
        st = RES.get(("ad", "alpha_CO", b), {})
        kd = st.get("K_direct"); kl = st.get("K_local")
        P(f"    {p['point']:14s} z {p['z']:.2f} ({b}): K_needed {p['K_needed']['0.5']:.3f} ({p['K_needed']['0.7']:.3f} to {p['K_needed']['0.3']:.3f}); alpha_CO (ad): K_direct " + (f"{kd:.3f}" if kd is not None else "n/a") + ", K_local " + (f"{kl:.3f}" if kl is not None else "n/a") + (f"; ACE K {KA:.3f}" if b.startswith("B3") else ""))

# ---- controls
P("\nCONTROLS")
exp = dict(daX=99, ad=318, xa=106, xd=137)
check("C1 the joins reproduce the counts seen before the freeze (daX 99, ad 318, xa 106, xd 137) and the ACE set is 15", f"{ {t: v['matched'] for t, v in JOIN.items()} }; ACE {len(ace)}", all(JOIN[t]["matched"] == exp[t] for t in exp) and len(ace) == 15 or MUT)
rng = np.random.default_rng(SEED)
x = rng.normal(0.10, 0.15, 500); sx = stats(x)
check("C2 estimator identity on synthetic factors (N = 500, mu = 0.10, SD = 0.15): mean, SD and SE to 3 SE", f"mean {sx['mean']:.3f}, SD {sx['sd']:.3f}, SE {sx['se']:.4f}", abs(sx["mean"] - 0.10) < 3 * sx["se"] and abs(sx["sd"] - 0.15) < 3 * sx["sd"] / math.sqrt(2 * 499))
L = [r for r in ROWS[("ad", "alpha_CO")] if math.isfinite(r["lir"])]
z = np.array([r["z"] for r in L]); lir = np.array([r["lir"] for r in L]) - 11.7
ytrue = 0.45 + 0.30 * np.log10(1 + z) - 0.10 * lir + rng.normal(0, 0.12, len(L))
X = np.vstack([np.ones(len(L)), np.log10(1 + z), lir]).T
bt = np.linalg.lstsq(X, ytrue, rcond=None)[0]
I = rng.integers(0, len(L), size=(2000, len(L))); bbs = np.array([np.linalg.lstsq(X[i], ytrue[i], rcond=None)[0] for i in I])
check("C3 regression recovery on the real (z, L_IR) of the ad table with known (b, c) = (0.30, -0.10): recovered to 3 bootstrap SD", f"b {bt[1]:.3f} +- {bbs[:, 1].std(ddof=1):.3f}, c {bt[2]:.3f} +- {bbs[:, 2].std(ddof=1):.3f}", abs(bt[1] - 0.30) < 3 * bbs[:, 1].std(ddof=1) and abs(bt[2] + 0.10) < 3 * bbs[:, 2].std(ddof=1))
cov = {}
for n_ in (9, 40):
    hit = 0
    for k in range(2000):
        xx = rng.normal(0.0, 0.15, n_); I = rng.integers(0, n_, size=(1000, n_)); b_ = xx[I].mean(axis=1)
        hit += int(np.percentile(b_, 16) <= 0 <= np.percentile(b_, 84))
    cov[n_] = hit / 2000
check("C4 bootstrap coverage of the 68% interval of a bin mean on Gaussian mocks (K = 2,000): in [0.60, 0.76] at N = 9 and 40", f"{cov}", all(0.60 <= v <= 0.76 for v in cov.values()))

if MUT:
    base = json.load(open(os.path.join(LANE, "cfg224b_conversion_drift_results.json")))
    ok = True
    for (tn, fname, b), st in RES.items():
        if fname != "alpha_CO" or st["N"] < 3:
            continue
        r0 = base["primary"].get(f"{tn}|{fname}|{b}")
        if r0 is None or "mean" not in r0:
            continue
        shift = st["mean"] - r0["mean"]
        want = 0.30 if (b.startswith("B3") or b.startswith("B4")) else 0.0
        ok &= abs(shift - want) < 1e-9
    kb3, kb3m = base["primary"].get("ad|alpha_CO|B3 1.6<=z<3.0", {}).get("K_local"), RES.get(("ad", "alpha_CO", "B3 1.6<=z<3.0"), {}).get("K_local")
    sb, sm = base["regression"].get("ad|alpha_CO", {}).get("b"), REG.get("ad|alpha_CO", {}).get("b")
    P(f"\nMUTATE: alpha_CO B3/B4 means shift by +0.300 and B1/B2 by 0: {ok}; ad alpha_CO K_local in B3 {kb3:.3f} -> {kmb3 if False else kb3m:.3f}; ad alpha_CO z slope {sb:+.3f} -> {sm:+.3f}")
    check("MUTATE the B3 and B4 alpha_CO means shift by +0.300 to 1e-9, B1 and B2 are unchanged, the z slope rises and K_local in B3 rises", f"{ok}", ok and sm > sb and kb3m > kb3)
    open(os.path.join(LANE, "cfg224b_conversion_drift_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
P("Reading rule: optimised conversions make the tracer masses agree by construction; the statistics describe how the conversion factors vary with z, at Dunne+22's priors and normalisation; a z-independent conversion is not a z-independent true gas mass; no law verdict.")
ser = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in RES.items()}
json.dump(dict(primary=ser, regression=REG, join=JOIN, ace=ACE, controls=dict(passed=sum(CHK), n=len(CHK)),
               points={f"{k[0]}|{k[1]}": [dict(z=r["z"], y=r["y"]) for r in v] for k, v in ROWS.items()}), open(os.path.join(LANE, "cfg224b_conversion_drift_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg224b_conversion_drift.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)
