#!/usr/bin/env python3
"""CFG198 -- MUSE-DARK per galaxy: a0(z) at R_e from III's own DC14 products (route i), and whether III's rise survives
swapping the DC14-fitted disc mass for the SED stellar mass + main-sequence H2 (route ii, primary) or SED stars only
(route iii).  Frozen criteria: FROZEN_CRITERIA.md in this directory (d5a73127b), committed before any number.
kappa = 1/2 FITTED, NOT DERIVED.  Nothing here is graded as support for the framework.

Data: data_assembly/musedark_catalogues/musedark_numeric.csv (data chat, be78f2054 / f17dae96c); definitions as read, marked.
Run:  python3 campaign_fresh_gravity/CFG198_musedark_pergalaxy_a0z/cfg198_musedark_a0z.py            (MUTATE=1 for the control)
"""
import os, sys, csv, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import brentq
from scipy.stats import spearmanr

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
R = C.Report("cfg198_musedark_a0z", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G_KPC = 4.30091e-6                         # kpc (km/s)^2 / Msun
G2SI = 1e6 / 3.0856775814913673e19         # (km/s)^2/kpc -> m/s^2
XN = 1.678                                 # R_e / R_d for an exponential disc
DMIN = 1.05
NBOOT, SEED = 10000, 198
OM = 0.315
A0F = K.A0                                 # the two footings, from the chain's FP0 JSON
KER = {"nu_mono": K.nu_mono, "nu_RAR": K.nu_rar}


def E(z):
    return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + 1 - OM)


def g_disc(M, Rd, Rr):
    """thin exponential disc: g = v^2/R, v^2 = (2GM/Rd) y^2 [I0K0 - I1K1], y = R/(2Rd); (km/s)^2/kpc"""
    y = np.asarray(Rr, float) / (2 * np.asarray(Rd, float))
    b = i0e(y) * k0e(y) - i1e(y) * k1e(y)
    return 2 * G_KPC * np.asarray(M, float) / np.asarray(Rd, float) * y ** 2 * b / np.asarray(Rr, float)


def g_hi(sig_pc2):
    """A2: v^2 = pi G Sigma r  ->  g = pi G Sigma (constant with r); Sigma in Msun/pc^2 -> Msun/kpc^2"""
    return math.pi * G_KPC * np.asarray(sig_pc2, float) * 1e6


def mu_mol(z, logm):
    """the main-sequence molecular-gas scaling as coded in CFG90 (tacconi18_mu)"""
    return 10 ** (0.06 - 3.3 * (np.log10(1 + np.asarray(z, float)) - 0.65) ** 2 - 0.41 * (np.asarray(logm, float) - 10.7))


def ystar(D, nu):
    """y* with nu(y*) = D (nu decreasing from +inf to 1); NaN for D <= DMIN"""
    out = np.full(len(D), np.nan)
    for i, d in enumerate(D):
        if not np.isfinite(d) or d <= DMIN:
            continue
        f = lambda ly: float(nu(np.array([10.0 ** ly]))[0]) - d
        out[i] = 10.0 ** brentq(f, -12, 14, xtol=1e-14, rtol=1e-14)
    return out


def theil_sen(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m])) if m.any() else np.nan


def ols_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.polyfit(x, y, 1)[0])


# ------------------------------------------------------------------------------------------------ controls
R.banner("CONTROLS")
rr = np.linspace(0.05, 12, 200001)
v2n = 2 * (rr / 2) ** 2 * (i0e(rr / 2) * k0e(rr / 2) - i1e(rr / 2) * k1e(rr / 2))           # v^2 Rd/(GM) at R/Rd = rr
ipk = int(np.argmax(v2n))
kep = g_disc(1.0, 1.0, 50.0) * 50.0 ** 2 / G_KPC                                               # v^2 R/(GM) = g R^2/(GM) at 50 Rd
# (fixed after the first run, kept as *_firstrun*: that run computed g R/(GM) = v^2/(GM), missing a factor R = 50, and
#  reported 0.02004 = 1.002/50; the disc code itself was not changed)
check("C1 exponential disc: peak at R/Rd in [2.1, 2.3] with v^2max Rd/(GM) = 0.3877 +- 0.001; Keplerian at 50 Rd within 0.5%",
      f"peak R/Rd = {rr[ipk]:.4f}, v^2max Rd/GM = {v2n[ipk]:.5f}; v^2 R/GM at 50 Rd = {kep:.5f}",
      2.1 <= rr[ipk] <= 2.3 and abs(v2n[ipk] - 0.3877) <= 0.001 and abs(kep - 1) < 0.005)
Dt = np.geomspace(1.06, 100, 60)
rt = {k: float(np.max(np.abs(np.array([float(nu(np.array([y]))[0]) for y in ystar(Dt, nu)]) / Dt - 1))) for k, nu in KER.items()}
check("C2 kernel round trip nu(y*(D)) = D to 1e-9 for D in [1.06, 100] (nu_mono and nu_RAR)", f"max rel error {rt}",
      max(rt.values()) < 1e-9)

# ------------------------------------------------------------------------------------------------ data
R.banner("DATA AND SAMPLE")
rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "musedark_catalogues", "musedark_numeric.csv"))))


def fl(r, k):
    try:
        v = float(r[k])
        return v if np.isfinite(v) else np.nan
    except (ValueError, TypeError):
        return np.nan


need = ("z", "logMstar_phot", "DC14_logMdisk", "fDM_at_Re", "Re_kpc", "gas_density_Msun_pc2")
n0 = len(rows)
ok_cols = [r for r in rows if all(np.isfinite(fl(r, k)) for k in need)]
n_bulge = sum(1 for r in ok_cols if r["has_bulge"].strip() == "1")
disc = [r for r in ok_cols if r["has_bulge"].strip() == "0"]
S = [r for r in disc if 0 < fl(r, "fDM_at_Re") < 1]
P(f"  rows {n0}; with all needed columns {len(ok_cols)}; bulge galaxies set aside {n_bulge}; disc-only {len(disc)}; "
  f"0 < fDM_at_Re < 1: {len(S)}")
R.num("sample_counts", dict(rows=n0, with_columns=len(ok_cols), bulge_set_aside=n_bulge, disc_only=len(disc), S=len(S)))
ids = [r["muse_id"] for r in S]
z = np.array([fl(r, "z") for r in S])
lms = np.array([fl(r, "logMstar_phot") for r in S])
lmf = np.array([fl(r, "DC14_logMdisk") for r in S])
fdm = np.array([fl(r, "fDM_at_Re") for r in S])
Re = np.array([fl(r, "Re_kpc") for r in S])
sig = np.array([fl(r, "gas_density_Msun_pc2") for r in S])
v22 = np.array([fl(r, "v22") for r in S])
Rd = Re / XN
zmed = float(np.median(z))
# g_obs at R_e: the DC14 model's total, from ITS OWN fitted disc mass and fitted Sigma_HI, computed once and held fixed in
# every route, every robustness row and the MUTATE run (FROZEN_CRITERIA: "held fixed in every route").
# (fixed after the second run, kept as *_secondrun* and *_MUTATE_firstrun*: those runs recomputed g_obs inside each
#  configuration, so the Sigma_HI = 0 / 15 rows and the MUTATE run changed the total along with the baryons; the primary
#  numbers and the mu_mol / nu_RAR rows are unchanged by this fix)
GOBS_RE = (1 / (1 - fdm)) * (g_disc(10 ** lmf, Rd, Re) + g_hi(sig))
lmf_true = lmf.copy()
if MUT:
    lmf = lmf - 0.4 * (z - zmed)
    P(f"  MUTATE=1: log M_fit -> log M_fit - 0.4 (z - {zmed:.3f}) (an injected fitted-mass drift at fixed g_obs)")


def routes(lmf_, lms_, sig_, mu_scale=1.0, radius="Re", nu=K.nu_mono, identity=False):
    """per-galaxy a0 [m/s^2] for routes i, ii, iii at the frozen radius; returns dict route -> (a0, D, g_bar)"""
    Rr = Re if radius == "Re" else 2.2 * Rd
    gh = g_hi(sig_)
    Mi = 10 ** lmf_
    gbi = g_disc(Mi, Rd, Rr) + gh
    gobs = GOBS_RE if radius == "Re" else v22 ** 2 / Rr
    mu = 0.0 if identity else mu_scale * mu_mol(z, lms_)
    Mii = 10 ** lms_ * (1 + mu)
    gbii = g_disc(Mii, Rd, Rr) + gh
    gbiii = g_disc(10 ** lms_, Rd, Rr) + gh
    out = {}
    for name, gb in (("i", gbi), ("ii", gbii), ("iii", gbiii)):
        D = gobs / gb
        ys = ystar(D, nu)
        out[name] = (gb * G2SI / ys, D, gb * G2SI)
    return out, gobs * G2SI


R.banner("C3 ROUTE IDENTITY")
idr, _ = routes(lmf, lmf, sig, identity=True)
rat = idr["ii"][0] / idr["i"][0]
fin = np.isfinite(rat)
check("C3 route identity: with M*_SED := M_fit and mu_mol := 0, route (ii) equals route (i) (every a0 ratio 1 to 1e-12)",
      f"max |ratio - 1| = {np.nanmax(np.abs(rat[fin] - 1)):.2e} over {fin.sum()} galaxies", fin.sum() > 0 and np.nanmax(np.abs(rat[fin] - 1)) < 1e-12)

# ------------------------------------------------------------------------------------------------ bootstrap machinery
rng = np.random.default_rng(SEED)
BOOT = rng.integers(0, len(S), size=(NBOOT, len(S)))
LAWS = {"flat": lambda zz: np.zeros_like(zz), "E(z)": lambda zz: np.log10(E(zz)), "III law": lambda zz: np.log10(1 + 1.59 * zz)}


def slope_ci(x, y, defined):
    """Theil-Sen slope over the defined galaxies and its bootstrap CI (resampling the full sample S, keeping defined ones)"""
    b = theil_sen(x[defined], y[defined])
    bs = np.empty(NBOOT)
    for k in range(NBOOT):
        idx = BOOT[k]
        idx = idx[defined[idx]]
        bs[k] = theil_sen(x[idx], y[idx]) if len(idx) > 2 else np.nan
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return b, float(lo), float(hi), bs


def evaluate(tag, rt, verbose=True):
    """slopes, CIs, reference slopes, R0/R1/R2 for one configuration"""
    res = {}
    la = {k: np.log10(v[0]) for k, v in rt.items()}
    dfn = {k: np.isfinite(la[k]) for k in rt}
    for k in ("i", "ii", "iii"):
        n = int(dfn[k].sum())
        lo_half = int((~dfn[k] & (z <= zmed)).sum()); hi_half = int((~dfn[k] & (z > zmed)).sum())
        if n < 3:
            res[k] = dict(n=n, b=np.nan, ci=[np.nan, np.nan], undefined_low_z=lo_half, undefined_high_z=hi_half)
            continue
        b, lo, hi, bs = slope_ci(z, la[k], dfn[k])
        refs = {L: ols_slope(z[dfn[k]], f(z[dfn[k]])) for L, f in LAWS.items()}
        inside = {L: bool(lo <= s <= hi) for L, s in refs.items()}
        rho = spearmanr(z, np.where(dfn[k], la[k], -99.0)).correlation
        thirds = np.array_split(np.argsort(z[dfn[k]]), 3)
        med3 = [float(np.median(la[k][dfn[k]][t])) for t in thirds]
        zmed3 = [float(np.median(z[dfn[k]][t])) for t in thirds]
        res[k] = dict(n=n, b=b, ci=[lo, hi], refs=refs, inside=inside, spearman_rho_with_undefined_at_bottom=float(rho),
                      undefined_low_z=lo_half, undefined_high_z=hi_half, median_log_a0_by_z_third=med3, median_z_by_third=zmed3,
                      _bs=bs)
    both = dfn["i"] & dfn["ii"]
    db = theil_sen(z[both], la["ii"][both]) - theil_sen(z[both], la["i"][both]) if both.sum() > 2 else np.nan
    dbs = np.empty(NBOOT)
    for kk in range(NBOOT):
        idx = BOOT[kk]; idx = idx[both[idx]]
        dbs[kk] = theil_sen(z[idx], la["ii"][idx]) - theil_sen(z[idx], la["i"][idx]) if len(idx) > 2 else np.nan
    dlo, dhi = np.nanpercentile(dbs, [2.5, 97.5])
    res["db"] = dict(n=int(both.sum()), db=float(db), ci=[float(dlo), float(dhi)], excludes_zero=bool(dlo > 0 or dhi < 0))
    # the same paired difference for route iii (reported)
    both3 = dfn["i"] & dfn["iii"]
    res["db_iii"] = float(theil_sen(z[both3], la["iii"][both3]) - theil_sen(z[both3], la["i"][both3])) if both3.sum() > 2 else np.nan
    if verbose:
        P(f"\n  [{tag}]")
        for k in ("i", "ii", "iii"):
            r_ = res[k]
            if not np.isfinite(r_["b"]):
                P(f"    route {k:3s}: n = {r_['n']} (too few); undefined low-z/high-z {r_['undefined_low_z']}/{r_['undefined_high_z']}")
                continue
            P(f"    route {k:3s}: n = {r_['n']:3d}  b = {r_['b']:+.3f} dex/z  95% CI [{r_['ci'][0]:+.3f}, {r_['ci'][1]:+.3f}]  "
              f"refs flat {r_['refs']['flat']:+.3f} E(z) {r_['refs']['E(z)']:+.3f} III {r_['refs']['III law']:+.3f}  "
              f"inside {[L for L, v in r_['inside'].items() if v]}  undefined (D<=1.05) low/high z {r_['undefined_low_z']}/"
              f"{r_['undefined_high_z']}  rho {r_['spearman_rho_with_undefined_at_bottom']:+.2f}")
            P(f"               median log10 a0 by z-third (z~{', '.join(f'{v:.2f}' for v in r_['median_z_by_third'])}): "
              f"{', '.join(f'{v:.3f}' for v in r_['median_log_a0_by_z_third'])}   "
              f"[footings log10 {math.log10(A0F['canonical']):.3f} / {math.log10(A0F['alt']):.3f}]")
        P(f"    paired db = b_ii - b_i = {res['db']['db']:+.3f}  95% CI [{res['db']['ci'][0]:+.3f}, {res['db']['ci'][1]:+.3f}]  "
          f"(n = {res['db']['n']}); excludes 0: {res['db']['excludes_zero']};  b_iii - b_i = {res['db_iii']:+.3f}")
    return res


def verdicts(res):
    r0 = res["i"].get("inside", {}).get("III law") if np.isfinite(res["i"]["b"]) else None
    if res["ii"]["n"] < 30 or not np.isfinite(res["ii"]["b"]):
        r1 = "NON-DIAGNOSTIC (baryon overshoot: fewer than 30 galaxies with D > 1.05)"
    else:
        ins = [L for L, v in res["ii"]["inside"].items() if v]
        exc = [L for L, v in res["ii"]["inside"].items() if not v]
        r1 = f"not excluded: {ins}; excluded: {exc}"
    r2 = (("changes the slope: db " + ("> 0" if res["db"]["ci"][0] > 0 else "< 0")) if res["db"]["excludes_zero"]
          else "no significant change (db CI contains 0)")
    return dict(R0=("reproduces III's rise" if r0 else "does not reproduce III's rise") if r0 is not None else "undefined",
                R1=r1, R2=r2)


# ------------------------------------------------------------------------------------------------ P1
R.banner("P1 -- the fitted disc mass against the SED mass, in z")
dstar = lmf - lms
dh2 = dstar - np.log10(1 + mu_mol(z, lms))
allS = np.ones(len(S), bool)
p1 = {}
for nm, q in (("delta_star = log M_fit - log M*_SED", dstar), ("delta_star - log(1 + mu_mol) (fitted disc vs SED + H2)", dh2)):
    b, lo, hi, _ = slope_ci(z, q, allS)
    p1[nm] = dict(b=b, ci=[lo, hi], median=float(np.median(q)))
    P(f"  {nm}: Theil-Sen slope {b:+.3f} dex/z, 95% CI [{lo:+.3f}, {hi:+.3f}]; median {np.median(q):+.3f} dex (n = {len(q)})")
R.num("P1", p1)

# ------------------------------------------------------------------------------------------------ primary
R.banner("PRIMARY -- a0 at R_e per route (nu_mono; Sigma_HI fitted; mu_mol x1)")
rt0, gobs0 = routes(lmf, lms, sig)
res0 = evaluate("primary", rt0)
v0 = verdicts(res0)
P(f"\n  R0 (closure, route i): {v0['R0']}\n  R1 (route ii): {v0['R1']}\n  R2 (circularity): {v0['R2']}")
R.num("primary", {k: ({kk: vv for kk, vv in v.items() if kk != "_bs"} if isinstance(v, dict) else v) for k, v in res0.items()})
R.num("primary_verdicts", v0)

# ------------------------------------------------------------------------------------------------ robustness
R.banner("ROBUSTNESS (reported): R0-R2 repeated")
cfgs = {"Sigma_HI = 0": dict(sig_=np.zeros_like(sig)), "Sigma_HI = 15": dict(sig_=np.full_like(sig, 15.0)),
        "mu_mol x 0.5": dict(mu_scale=0.5), "mu_mol x 2": dict(mu_scale=2.0), "nu_RAR": dict(nu=K.nu_rar)}
rob = {}
for tag, kw in cfgs.items():
    kw2 = dict(sig_=sig); kw2.update(kw)
    rt_, _ = routes(lmf, lms, **kw2)
    r_ = evaluate(tag, rt_)
    vv = verdicts(r_)
    P(f"    -> R0 {vv['R0']}; R1 {vv['R1']}; R2 {vv['R2']}")
    rob[tag] = dict(verdicts=vv, b={k: r_[k]["b"] for k in ("i", "ii", "iii")}, ci={k: r_[k]["ci"] for k in ("i", "ii", "iii")},
                    db=r_["db"], n={k: r_[k]["n"] for k in ("i", "ii", "iii")})
# route (iii) in place of (ii) for R1/R2
r3 = dict(res0)
r3 = {"i": res0["i"], "ii": res0["iii"], "iii": res0["iii"], "db": None}
la_i, la_3 = np.log10(rt0["i"][0]), np.log10(rt0["iii"][0])
both3 = np.isfinite(la_i) & np.isfinite(la_3)
dbs3 = np.empty(NBOOT)
for kk in range(NBOOT):
    idx = BOOT[kk]; idx = idx[both3[idx]]
    dbs3[kk] = theil_sen(z[idx], la_3[idx]) - theil_sen(z[idx], la_i[idx])
d3 = float(theil_sen(z[both3], la_3[both3]) - theil_sen(z[both3], la_i[both3]))
lo3, hi3 = np.nanpercentile(dbs3, [2.5, 97.5])
r3["db"] = dict(n=int(both3.sum()), db=d3, ci=[float(lo3), float(hi3)], excludes_zero=bool(lo3 > 0 or hi3 < 0))
v3 = verdicts(r3)
P(f"\n  [route (iii) SED stars only, in place of (ii)] -> R1 {v3['R1']}; R2 {v3['R2']} (db {d3:+.3f}, CI [{lo3:+.3f}, {hi3:+.3f}])")
rob["route (iii) in place of (ii)"] = dict(verdicts=v3, db=r3["db"])
same = {k: len({rob[t]["verdicts"][k] for t in rob} | {v0[k]}) == 1 for k in ("R0", "R1", "R2")}
P("\n  robust (same verdict in the primary and every robustness row): " + ", ".join(f"{k} {'ROBUST' if v else 'NOT robust'}"
                                                                                 for k, v in same.items()))
R.num("robustness", rob)
R.num("robust", same)

# ------------------------------------------------------------------------------------------------ v22 variant
R.banner("VARIANT (reported): the v22 route at 2.2 R_d (v22 read as v_c there; A3, unverified)")
rtv, gobsv = routes(lmf, lms, sig, radius="v22")
okv = np.isfinite(gobsv) & (gobsv > 0)
ratio = gobsv[okv] / gobs0[okv]
P(f"  g_obs(v22 at 2.2 Rd) / g_obs(R_e, from fDM): median {np.median(ratio):.3f}, 16-84% {np.percentile(ratio, 16):.3f}-"
  f"{np.percentile(ratio, 84):.3f} (n = {okv.sum()}); a flat curve between the radii would give R_e/(2.2 Rd) = {XN / 2.2:.3f}")
resv = evaluate("v22 variant", rtv)
vv = verdicts(resv)
P(f"    -> R0 {vv['R0']}; R1 {vv['R1']}; R2 {vv['R2']}")
R.num("v22_variant", dict(verdicts=vv, gobs_ratio_median=float(np.median(ratio)),
                          gobs_ratio_16_84=[float(np.percentile(ratio, 16)), float(np.percentile(ratio, 84))],
                          b={k: resv[k]["b"] for k in ("i", "ii", "iii")}, ci={k: resv[k]["ci"] for k in ("i", "ii", "iii")}))

# ------------------------------------------------------------------------------------------------ MUTATE response
if MUT:
    R.banner("MUTATE RESPONSE")
    rtt, _ = routes(lmf_true, lms, sig)
    rt_true = evaluate("unmutated (for the response check)", rtt, verbose=False)
    dbi = res0["i"]["b"] - rt_true["i"]["b"]
    ddb = res0["db"]["db"] - rt_true["db"]["db"]
    check("MUTATE: the injected fitted-mass drift raises b_i by >= 0.1 dex/z and lowers db by >= 0.1",
          f"b_i {rt_true['i']['b']:+.3f} -> {res0['i']['b']:+.3f} (change {dbi:+.3f}); db {rt_true['db']['db']:+.3f} -> "
          f"{res0['db']['db']:+.3f} (change {ddb:+.3f})", dbi >= 0.1 and ddb <= -0.1)
R.write(here=LANE)
