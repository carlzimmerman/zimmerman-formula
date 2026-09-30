#!/usr/bin/env python3
"""CFG199 -- MUSE-DARK: is CFG198's against-interest a0 level real?  a0 at R_e from the model's own rotation profile
(true_Vrot.dat), which brackets the pressure term from below.  Frozen criteria: FROZEN_CRITERIA.md here (997e5047a),
committed before any number.  kappa = 1/2 FITTED, NOT DERIVED.  Nothing here is graded as support for the framework.

Two readings of the file's v, never pooled: (a) v_perp = v (deprojected, before the drift term; the papers' text),
(b) v_perp = v / sin i (projected).  g_perp = v_perp^2 / R_e is a lower bound on the model's total at R_e when the
pressure term is non-negative; route (i) a0 = (1 - fDM) g_perp / y*(1/(1 - fDM)) is then a lower bound on III's route.
Run:  python3 campaign_fresh_gravity/CFG199_musedark_level_pressure/cfg199_musedark_level.py        (MUTATE=1: v x 0.8)
"""
import os, sys, csv, math, hashlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import brentq
from scipy.stats import spearmanr

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "muse_dark", "numeric")
DA = os.path.join(REPO, "data_assembly", "musedark_catalogues")
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
R = C.Report("cfg199_musedark_level", MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

# ---- the formulas of CFG198 (copied verbatim; C4 below re-derives CFG198's committed primary slope with them)
G_KPC = 4.30091e-6
G2SI = 1e6 / 3.0856775814913673e19
XN = 1.678
DMIN = 1.05
NBOOT, SEED = 10000, 199
A0F = K.A0
OM = 0.315


def E(z):
    return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + 1 - OM)


def g_disc(M, Rd, Rr):
    y = np.asarray(Rr, float) / (2 * np.asarray(Rd, float))
    b = i0e(y) * k0e(y) - i1e(y) * k1e(y)
    return 2 * G_KPC * np.asarray(M, float) / np.asarray(Rd, float) * y ** 2 * b / np.asarray(Rr, float)


def g_hi(sig_pc2):
    return math.pi * G_KPC * np.asarray(sig_pc2, float) * 1e6


def mu_mol(z, logm):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + np.asarray(z, float)) - 0.65) ** 2 - 0.41 * (np.asarray(logm, float) - 10.7))


def ystar(D, nu=K.nu_mono):
    out = np.full(len(D), np.nan)
    for i, d in enumerate(D):
        if not np.isfinite(d) or d <= DMIN:
            continue
        out[i] = 10.0 ** brentq(lambda ly: float(nu(np.array([10.0 ** ly]))[0]) - d, -12, 14, xtol=1e-14, rtol=1e-14)
    return out


def theil_sen(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m])) if m.any() else np.nan


def ols_slope(x, y):
    return float(np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)[0])


def v_at_re(rad, v, target=1.0):
    """|v| at |rad| = target on each side (linear interpolation), averaged over the sides that reach it; NaN if none"""
    vals = []
    for sgn in (1, -1):
        m = (np.sign(rad) == sgn)
        if m.sum() < 2:
            continue
        rr, vv = np.abs(rad[m]), np.abs(v[m])
        o = np.argsort(rr)
        rr, vv = rr[o], vv[o]
        if rr[0] <= target <= rr[-1]:
            vals.append(float(np.interp(target, rr, vv)))
    return float(np.mean(vals)) if vals else np.nan, len(vals)


# ------------------------------------------------------------------------------------------------ controls C1, C2
R.banner("CONTROLS")
man = {}
for line in open(os.path.join(DA, "numeric_manifest_sha256.txt")):
    parts = line.split()
    if len(parts) == 2:
        man[parts[1]] = parts[0]
tv = sorted(k for k in man if k.endswith("_true_Vrot.dat"))
bad = []
for k in tv:
    p = os.path.join(EXT, k)
    if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != man[k]:
        bad.append(k)
check("C1 every true_Vrot.dat sha256 matches the data chat's manifest", f"{len(tv)} files in the manifest; mismatched or missing: {bad[:3]}",
      len(tv) == 126 and not bad)
if bad or len(tv) != 126:
    R.write(here=LANE)
    sys.exit("abort: hash check failed")
rs = np.linspace(-3, 3, 25)
vs = 57.0 * rs
vt, ns = v_at_re(rs, vs)
check("C2 interpolation: a synthetic antisymmetric linear profile v = 57 R/R_e gives v(R_e) = 57 to 1e-12 (both sides)",
      f"v_f(R_e) = {vt!r} from {ns} sides", abs(vt - 57.0) < 1e-12 and ns == 2)

# ------------------------------------------------------------------------------------------------ data (CFG198's sample)
rows = list(csv.DictReader(open(os.path.join(DA, "musedark_numeric.csv"))))


def fl(r, k):
    try:
        v = float(r[k])
        return v if np.isfinite(v) else np.nan
    except (ValueError, TypeError):
        return np.nan


need = ("z", "logMstar_phot", "DC14_logMdisk", "fDM_at_Re", "Re_kpc", "gas_density_Msun_pc2")
S = [r for r in rows if all(np.isfinite(fl(r, k)) for k in need) and r["has_bulge"].strip() == "0" and 0 < fl(r, "fDM_at_Re") < 1]
ids = [int(r["muse_id"]) for r in S]
z = np.array([fl(r, "z") for r in S]); lms = np.array([fl(r, "logMstar_phot") for r in S])
lmf = np.array([fl(r, "DC14_logMdisk") for r in S]); fdm = np.array([fl(r, "fDM_at_Re") for r in S])
Re = np.array([fl(r, "Re_kpc") for r in S]); sig = np.array([fl(r, "gas_density_Msun_pc2") for r in S])
inc = np.array([fl(r, "incl_deg") for r in S]); sini = np.sin(np.radians(inc))
Rd = Re / XN
P(f"\n  sample S (CFG198's): {len(S)} galaxies")

# CFG198's quantities (its primary configuration), for the reproduction check and the ratios
gbi_mine = g_disc(10 ** lmf, Rd, Re) + g_hi(sig)
D = 1 / (1 - fdm)
GOBS198 = D * gbi_mine
a198_i = gbi_mine * G2SI / ystar(D)
d198 = np.isfinite(a198_i)
b198 = theil_sen(z[d198], np.log10(a198_i[d198]))
check("C4 the copied CFG198 formulas reproduce CFG198's committed primary route-(i) slope +0.789 (to the printed 3 decimals)",
      f"b_i = {b198:+.6f}", abs(b198 - 0.789) < 0.0005)
# CFG198's z-thirds of its route-(i) galaxies (the L1 set)
idx198 = np.where(d198)[0]
thirds198 = np.array_split(idx198[np.argsort(z[idx198])], 3)
low_third = thirds198[0]
P(f"  CFG198's lowest-z third of route (i): {len(low_third)} galaxies, median z {np.median(z[low_third]):.3f}")

# ------------------------------------------------------------------------------------------------ the file's v at R_e
vf = np.full(len(S), np.nan); sf = np.full(len(S), np.nan); nside = np.zeros(len(S), int)
for k, gid in enumerate(ids):
    p = os.path.join(EXT, f"ID{gid:04d}", f"DC14_{gid}_true_Vrot.dat")
    rws = [[c.strip() for c in l.strip().strip("|").split("|")] for l in open(p) if l.strip()]
    assert rws[0] == ["dx_arcsec", "rad_Re", "flux_slit", "v_kms", "sig_kms"], (gid, rws[0])
    arr = np.array([[float(x) for x in r_] for r_ in rws[1:]])
    vf[k], nside[k] = v_at_re(arr[:, 1], arr[:, 3])
    sf[k], _ = v_at_re(arr[:, 1], arr[:, 4] * np.sign(arr[:, 1]))
if MUT:
    vf = 0.8 * vf
    P("  MUTATE=1: v_f -> 0.8 v_f")
okv = np.isfinite(vf)
P(f"  v_f(R_e) available for {okv.sum()} of {len(S)} (both sides {int((nside == 2).sum())}, one side {int((nside == 1).sum())}, "
  f"none {int((nside == 0).sum())})")
R.num("v_at_Re_counts", dict(available=int(okv.sum()), both=int((nside == 2).sum()), one=int((nside == 1).sum()),
                             none=int((nside == 0).sum())))

# ------------------------------------------------------------------------------------------------ C3 route identity
rng = np.random.default_rng(SEED)
BOOT = rng.integers(0, len(S), size=(NBOOT, len(S)))


def routes(vperp, lms_=lms, mu_on=True):
    g_perp = vperp ** 2 / Re                                     # (km/s)^2/kpc
    gbi = (1 - fdm) * g_perp
    out = {"i": (gbi * G2SI / ystar(D), D)}
    base = g_disc(10 ** lmf, Rd, Re) + g_hi(sig)
    for name, M in (("ii", 10 ** lms_ * (1 + (mu_mol(z, lms_) if mu_on else 0.0))), ("iii", 10 ** lms_)):
        gb = gbi * (g_disc(M, Rd, Re) + g_hi(sig)) / base
        Dr = g_perp / gb
        out[name] = (gb * G2SI / ystar(Dr), Dr)
    return out, g_perp


idt, _ = routes(vf, lms_=lmf, mu_on=False)
rat = idt["ii"][0] / idt["i"][0]; rat3 = idt["iii"][0] / idt["i"][0]
fin = np.isfinite(rat) & np.isfinite(rat3)
check("C3 route identity: with M*_SED := M_fit and mu_mol := 0, routes (ii) and (iii) equal route (i) to 1e-12",
      f"max |ratio - 1| = {max(np.nanmax(np.abs(rat[fin] - 1)), np.nanmax(np.abs(rat3[fin] - 1))):.2e} over {fin.sum()}",
      fin.sum() > 0 and max(np.nanmax(np.abs(rat[fin] - 1)), np.nanmax(np.abs(rat3[fin] - 1))) < 1e-12)


def slope_ci(x, y, defined):
    b = theil_sen(x[defined], y[defined])
    bs = np.empty(NBOOT)
    for k in range(NBOOT):
        idx = BOOT[k]; idx = idx[defined[idx]]
        bs[k] = theil_sen(x[idx], y[idx]) if len(idx) > 2 else np.nan
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return b, float(lo), float(hi)


LAWS = {"flat": lambda zz: np.zeros_like(zz), "E(z)": lambda zz: np.log10(E(zz)), "III law": lambda zz: np.log10(1 + 1.59 * zz)}
FOOT = (math.log10(A0F["canonical"]), math.log10(A0F["alt"]))
out_all = {}
for reading, vperp in (("a: v_perp = v_file", vf), ("b: v_perp = v_file / sin i", vf / sini)):
    R.banner(f"READING {reading}")
    rt, g_perp = routes(vperp)
    la = {k: np.log10(v[0]) for k, v in rt.items()}
    dfn = {k: np.isfinite(la[k]) for k in rt}
    # L1: the level on CFG198's lowest-z third of route (i)
    lt = np.array([i for i in low_third if dfn["i"][i]])
    med = float(np.median(la["i"][lt]))
    r2 = np.random.default_rng(SEED)
    bm = np.array([np.median(la["i"][lt][r2.integers(0, len(lt), len(lt))]) for _ in range(NBOOT)])
    lo, hi = (float(x) for x in np.percentile(bm, [2.5, 97.5]))
    if lo > FOOT[1]:
        L1 = "the level excess SURVIVES the no-pressure lower bound (CI above both footings): against interest, robust"
    elif hi < FOOT[0]:
        L1 = "BELOW both footings at the lower bound"
    else:
        L1 = "consistent with the footings at the lower bound (CFG198's excess depends on the pressure term / geometry)"
    shift = float(np.median(np.log10(g_perp[lt] / GOBS198[lt])))
    P(f"  L1 route (i) lowest-z third (n = {len(lt)}, median z {np.median(z[lt]):.3f}): median log10 a0 = {med:.3f}, 95% CI "
      f"[{lo:.3f}, {hi:.3f}]; footings {FOOT[0]:.3f} / {FOOT[1]:.3f}; CFG198's value there -9.646; median log10(g_perp / "
      f"g_obs,CFG198) = {shift:+.3f}\n  -> L1: {L1}")
    # the other routes' levels (reported)
    lev = {}
    for k in ("ii", "iii"):
        ltk = np.array([i for i in low_third if dfn[k][i]])
        lev[k] = float(np.median(la[k][ltk])) if len(ltk) else np.nan
    P(f"  lowest-third medians, routes ii / iii (reported): {lev['ii']:.3f} / {lev['iii']:.3f}")
    # L2 slopes
    res = {}
    for k in ("i", "ii", "iii"):
        if dfn[k].sum() < 3:
            res[k] = dict(n=int(dfn[k].sum()), b=np.nan, ci=[np.nan, np.nan]); continue
        b, blo, bhi = slope_ci(z, la[k], dfn[k])
        refs = {L: ols_slope(z[dfn[k]], f(z[dfn[k]])) for L, f in LAWS.items()}
        res[k] = dict(n=int(dfn[k].sum()), b=b, ci=[blo, bhi], refs=refs, inside={L: bool(blo <= s <= bhi) for L, s in refs.items()},
                      undefined_low_high=[int((~dfn[k] & (z <= np.median(z))).sum()), int((~dfn[k] & (z > np.median(z))).sum())])
        P(f"  L2 route {k:3s}: n = {res[k]['n']:3d}  b = {b:+.3f} [{blo:+.3f}, {bhi:+.3f}]  inside {[L for L, v in res[k]['inside'].items() if v]}"
          f"  undefined low/high z {res[k]['undefined_low_high']}")
    both = dfn["i"] & dfn["ii"]
    dbs = np.empty(NBOOT)
    for kk in range(NBOOT):
        idx = BOOT[kk]; idx = idx[both[idx]]
        dbs[kk] = theil_sen(z[idx], la["ii"][idx]) - theil_sen(z[idx], la["i"][idx]) if len(idx) > 2 else np.nan
    db = theil_sen(z[both], la["ii"][both]) - theil_sen(z[both], la["i"][both])
    dlo, dhi = (float(x) for x in np.nanpercentile(dbs, [2.5, 97.5]))
    P(f"  L2 paired db = b_ii - b_i = {db:+.3f} [{dlo:+.3f}, {dhi:+.3f}] (n = {both.sum()})")
    survive = (res["i"]["ci"][0] > 0) and not (res["ii"]["ci"][0] > 0) and (dhi < 0)
    P(f"  -> CFG198's slope finding (route i rises; route ii not significantly rising; db < 0) "
      f"{'SURVIVES' if survive else 'does NOT fully survive'} under this reading")
    # L3
    vc198 = np.sqrt(GOBS198 * Re)
    m3 = np.isfinite(vperp)
    rho = spearmanr(vperp[m3] / vc198[m3], sini[m3]).correlation
    s_share = 1 - g_perp[m3] / GOBS198[m3]
    P(f"  L3 (reported): Spearman rho(v_perp / v_c,CFG198, sin i) = {rho:+.3f}; share s = 1 - g_perp/g_obs,CFG198: median "
      f"{np.median(s_share):.3f}, 16-84% {np.percentile(s_share, 16):.3f} to {np.percentile(s_share, 84):.3f}")
    out_all[reading] = dict(L1=dict(n=len(lt), median=med, ci=[lo, hi], verdict=L1, shift_vs_CFG198=shift),
                            levels_ii_iii=lev, L2={k: {kk: vv for kk, vv in v.items()} for k, v in res.items()},
                            db=dict(db=float(db), ci=[dlo, dhi], n=int(both.sum())), slope_finding_survives=bool(survive),
                            L3=dict(rho_sin_i=float(rho), s_median=float(np.median(s_share)),
                                    s_16_84=[float(np.percentile(s_share, 16)), float(np.percentile(s_share, 84))]))
R.num("readings", out_all)
if MUT:
    R.banner("MUTATE RESPONSE")
    # the unmutated level is recomputed in-process for the comparison
    vf0 = vf / 0.8
    rt0, _ = routes(vf0)
    la0 = np.log10(rt0["i"][0])
    lt0 = np.array([i for i in low_third if np.isfinite(la0[i])])
    shiftm = out_all["a: v_perp = v_file"]["L1"]["median"] - float(np.median(la0[lt0]))
    check("MUTATE: v_f x 0.8 shifts the route-(i) level by 2 log10 0.8 = -0.1938 +- 0.001 dex", f"shift {shiftm:+.4f}",
          abs(shiftm - 2 * math.log10(0.8)) < 0.001)
R.write(here=LANE)
