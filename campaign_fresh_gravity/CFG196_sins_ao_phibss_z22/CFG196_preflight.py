#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG196 pre-flight -- can a0 at z ~ 2.2 be discriminated (flat a0 vs a0 * E(z)) with SINS/zC-SINF AO Halpha kinematics
and PHIBSS (Tacconi+2013) CO gas, BEFORE any kinematics is looked at?

Frozen in campaign_fresh_gravity/CFG196_FROZEN_CRITERIA.md (section 7) before this script existed.

Inputs (and ONLY these):
  * PHIBSS 2013 table values: M*, Mmol, rh_opt, rh_co, z_CO, comp, type, co_upper_limit
    (data_assembly/kmos3d_phibss/phibss13_joined.csv). The vrot column is NEVER loaded.
  * FS2009 (CDS J/ApJ/706/1364) Halpha r1/2, z_Halpha and SED M* for reported variants only
    (data_assembly/high_z_tf_tables/sins2009_dynamics.csv). No velocity/dispersion/Mdyn column is loaded.
  * SINS/zC-SINF AO release: cut-cube FITS HEADERS (dimensions, centre pixel, wavelength axis) and the PSF IMAGES
    (a star; no velocity information) for the FWHM. No cube spectrum is read.
  * The kernels and a0 footings from CFG4_common (read-only import; nu_mono is FP1's committed kernel).

What it computes: V_c(R) at 1, 2, 3 R_e for Newton, flat (a = a0) and the rival (a = a0 E(z)), P2 and nu_mono, both
footings, over the M* +/- 0.2 dex and alpha_CO x/ 1.5 bands; the separation rival - flat in km/s and in units of the
declared per-point error budget; the profiled separation Z_prof (masses free under Gaussian priors), the band worst
case Z_band, and the sample-level feasibility gate H0 (reported, not load-bearing).

MUTATE=1: the rival's E(z) is set to 1, so the two laws coincide; every separation must collapse to 0, the headline
check S1 fails and the run exits 1. Outputs: CFG196_preflight{_MUTATE}.out and CFG196_preflight{_MUTATE}_results.json.

POST-HOC block (added after the first run, which is kept verbatim as CFG196_preflight_firstrun.out / _results.json;
reported only; no frozen number or the H0 verdict changes): a near-perfect-kinematics limit, the masses-exact Z_nom,
and a one-term-at-a-time ablation of the declared error budget -- to say what limits the forecast.

kappa = 1/2 stays FITTED. Nothing here says the data favour either law; it is a forecast, not a test.
"""
import os
import sys
import csv
import json
import math
import glob
import time
import builtins

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import minimize, least_squares
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
sys.path.insert(0, CFGDIR)
import CFG4_common as C4  # noqa: E402  (read-only: constants, nu_p2, nu_mono)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUT_PATH = os.path.join(HERE, f"CFG196_preflight{SUF}.out")
JSON_PATH = os.path.join(HERE, f"CFG196_preflight{SUF}_results.json")

PHIBSS_CSV = os.path.join(REPO, "data_assembly", "kmos3d_phibss", "phibss13_joined.csv")
FS09_CSV = os.path.join(REPO, "data_assembly", "high_z_tf_tables", "sins2009_dynamics.csv")
SINS_DIR = os.path.expanduser("~/new_physics/_external_data/sins_ao/cubes/SINS-ZCSINF_AO_release")
PIX_ARCSEC = 0.05                                   # release README

# ---------------------------------------------------------------------------------------------- constants
G_KPC = C4.G_SI * C4.MSUN / C4.KPC / 1e6            # kpc (km/s)^2 / Msun  (4.30092e-6)
A0_KPC = {f: C4.A0[f] * C4.KPC / 1e6 for f in C4.FOOTS}   # (km/s)^2 / kpc
OMEGA_M_RIVAL = 0.315                               # CFG140's convention for E(z)
COSMO_ANG = FlatLambdaCDM(H0=70.0, Om0=0.3)         # SINS/FS2018-style cosmology for kpc per arcsec (declared)
LAM_HA_VAC_UM = 0.656461                            # Halpha vacuum rest wavelength (micron)
RE_TO_RD = 1.678                                    # R_e = 1.678 R_d for an exponential disc
DEX_MSTAR = 0.2                                     # M* band (dex), prior sigma for Z_prof
DEX_CO = math.log10(1.5)                            # alpha_CO band (Tacconi+13 50% systematic), prior sigma
ULIRG_FAC = 0.8 / 4.36                              # CFG164's ULIRG-like alpha_CO bracket (stress row)
# declared per-point error budget (criteria section 7)
STAT_KNOTS = ((1.0, 10.0), (2.0, 15.0), (3.0, 25.0))  # LOS stat error (km/s) for the two-side average vs R/R_e
DI_DEG = 5.0                                        # inclination error
SIG0, DSIG0 = 50.0, 10.0                            # declared sigma_0 and its measurement error (km/s)
BS_RESID = 5.0                                      # beam-smearing residual after forward modelling (km/s)
NC_FLOOR = 10.0                                     # non-circular / side-asymmetry floor (km/s)
INCS = (30.0, 45.0, 60.0)
I_CENTRAL = 45.0

EXPECTED_MATCH = {"ZC406690", "Q1623-BX599", "Q2343-BX389", "Q2343-BX513", "Q2343-BX610", "Q2346-BX482"}
FROZEN_PRIMARY = {"ZC406690", "Q2343-BX610"}
# R1: the paper attributes the CO to another source (Tacconi+2013 Fig. 5 caption, t13.txt ~line 2640)
ATTRIBUTED_ELSEWHERE = {"Q2346-BX482": "Tacconi+13 Fig.5 caption: CO mostly from the fainter source BX482se"}


# ---------------------------------------------------------------------------------------------- tee + checks
class Tee:
    def __init__(self, path):
        self.f = builtins.open(path, "w", encoding="utf-8")
        self.o = sys.stdout

    def write(self, t):
        self.o.write(t)
        self.f.write(t)

    def flush(self):
        self.o.flush()
        self.f.flush()


TEE = Tee(OUT_PATH)
sys.stdout = TEE
T0 = time.time()
CHECKS = []
OUT = {"lane": "CFG196", "script": "CFG196_preflight", "mutate": MUTATE, "checks": {}, "numbers": {}}


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, load_bearing=True, reading=""):
    ok = bool(ok)
    key = name.split()[0]
    CHECKS.append((key, ok, load_bearing))
    OUT["checks"][key] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured), "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, np.floating):
        o = float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return str(o)
    return o


# ---------------------------------------------------------------------------------------------- physics
def Ez(z):
    if MUTATE:
        return 1.0
    return math.sqrt(OMEGA_M_RIVAL * (1.0 + z) ** 3 + (1.0 - OMEGA_M_RIVAL))


def v2_freeman(R, M, Rd):
    """exact thin exponential disc (Freeman 1970): V^2 = 2 G M / R_d * y^2 [I0 K0 - I1 K1], y = R / (2 R_d)."""
    R = np.asarray(R, float)
    if M <= 0:
        return np.zeros_like(R)
    y = R / (2.0 * Rd)
    return 2.0 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def v2_sphere(R, M, Rd):
    """CFG140's spherical shortcut: G M(<R)/R with the thin exponential disc's enclosed mass."""
    R = np.asarray(R, float)
    if M <= 0:
        return np.zeros_like(R)
    y = R / Rd
    return G_KPC * M * (1.0 - np.exp(-y) * (1.0 + y)) / R


KER = {"P2": C4.nu_p2, "nu_mono": C4.nu_mono}


def gN_of(R, gal, dstar=0.0, dco=0.0, geom="freeman", hi=0.0, rstar_fac=1.0, gas_fac=1.0):
    """Newtonian midplane field (km/s)^2/kpc. dstar, dco may be arrays broadcast against R's leading axes."""
    f = v2_freeman if geom == "freeman" else v2_sphere
    ms = gal["mstar"] * 10.0 ** np.asarray(dstar, float)
    mg = gal["mgas"] * gas_fac * 10.0 ** np.asarray(dco, float)
    rds = gal["re"] / RE_TO_RD * rstar_fac
    rdg = gal["re_gas"] / RE_TO_RD
    R = np.asarray(R, float)
    v2s = f(R, 1.0, rds) * ms[..., None] if np.ndim(ms) else f(R, ms, rds)
    v2g = f(R, 1.0, rdg) * mg[..., None] if np.ndim(mg) else f(R, mg, rdg)
    v2 = v2s + v2g
    if hi > 0:
        mh = gal["mgas"] * gas_fac * hi
        v2 = v2 + f(R, mh, 2.0 * rdg)
    return v2 / R


def vpred(R, gal, law, kern="P2", foot="canonical", **kw):
    """V_c prediction (km/s) for law in {newton, flat, rival}."""
    gN = gN_of(R, gal, **kw)
    if law == "newton":
        g = gN
    else:
        a = A0_KPC[foot] * (Ez(gal["z"]) if law == "rival" else 1.0)
        g = KER[kern](gN / a) * gN
    return np.sqrt(g * np.asarray(R, float))


def alpha_psB(R, gal):
    return 2.0 * np.asarray(R, float) / (gal["re"] / RE_TO_RD)


def alpha_psK(R, gal):
    x = np.clip(np.asarray(R, float) / gal["re"] - 1.0, 0.0, 4.0)
    return -0.146 * x ** 2 + 1.204 * x + 1.475


def stat_err(r_over_re):
    xs = np.array([k[0] for k in STAT_KNOTS])
    ys = np.array([k[1] for k in STAT_KNOTS])
    return np.interp(np.asarray(r_over_re, float), xs, ys)


def covariance(R, per_side, gal, vref, inc_deg, presc="B"):
    """C = diag(stat^2 + bs^2 + nc^2) + u u^T (inclination, coherent) + p p^T (sigma_0, coherent)."""
    R = np.asarray(R, float)
    si = math.sin(math.radians(inc_deg))
    cot = 1.0 / math.tan(math.radians(inc_deg))
    st = stat_err(R / gal["re"]) / si * np.where(per_side, math.sqrt(2.0), 1.0)
    u = vref * cot * math.radians(DI_DEG)
    al = alpha_psB(R, gal) if presc == "B" else alpha_psK(R, gal)
    p = al * SIG0 * DSIG0 / vref
    Cm = np.diag(st ** 2 + BS_RESID ** 2 + NC_FLOOR ** 2) + np.outer(u, u) + np.outer(p, p)
    return Cm, np.sqrt(np.diag(Cm))


# ---------------------------------------------------------------------------------------------- data (no kinematics)
def load_phibss():
    keep = ("name", "comp", "type", "rh_opt_kpc", "rh_co_kpc", "mmol_msun", "mstar_msun", "z_co", "co_upper_limit")
    rows = []
    with builtins.open(PHIBSS_CSV, newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append({k: r[k] for k in keep})      # vrot_kms is never copied
    return rows


def load_fs09():
    keep = ("name", "z_halpha", "r_half_halpha_kpc", "mstar_1e10msun")
    out = {}
    with builtins.open(FS09_CSV, newline="") as fh:
        for r in csv.DictReader(fh):
            out[r["name"].upper()] = {k: r[k] for k in keep}   # no velocity / sigma / Mdyn column copied
    return out


def fnum(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return float("nan")
    return v


def psf_fwhm(path):
    """FWHM (arcsec) of the PSF image: circular 2-D Gaussian + constant fitted to the central 25x25 around the peak,
    and the half-maximum-area equivalent 2 sqrt(A/pi). The PSF is a star: no velocity information."""
    im = fits.getdata(path).astype(float)
    im = np.nan_to_num(im, nan=0.0)
    ny, nx = im.shape
    border = np.concatenate([im[:3].ravel(), im[-3:].ravel(), im[:, :3].ravel(), im[:, -3:].ravel()])
    im = im - np.median(border)
    jy, jx = np.unravel_index(np.argmax(im), im.shape)
    h = 12
    y0, y1, x0, x1 = max(jy - h, 0), min(jy + h + 1, ny), max(jx - h, 0), min(jx + h + 1, nx)
    sub = im[y0:y1, x0:x1]
    yy, xx = np.mgrid[y0:y1, x0:x1]

    def res(p):
        A, cx, cy, s, b = p
        return (A * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * s * s)) + b - sub).ravel()

    fit = least_squares(res, [im[jy, jx], jx, jy, 2.0, 0.0])
    fwhm_g = 2.3548 * abs(fit.x[3]) * PIX_ARCSEC
    area = np.count_nonzero(im >= 0.5 * im[jy, jx])
    fwhm_a = 2.0 * math.sqrt(area / math.pi) * PIX_ARCSEC
    return fwhm_g, fwhm_a


def header_geom(name):
    f = glob.glob(os.path.join(SINS_DIR, f"{name}_*_data_cut.fits"))
    assert len(f) == 1, (name, f)
    hd = fits.getheader(f[0])
    n1, n2, n3 = hd["NAXIS1"], hd["NAXIS2"], hd["NAXIS3"]
    c1, c2 = float(hd["CRPIX1"]), float(hd["CRPIX2"])
    lam = hd["CRVAL3"] + (np.array([1.0, float(n3)]) - hd["CRPIX3"]) * hd["CDELT3"]
    # distances from the centre pixel to the four edges (pixel centres 1..N, edges 0.5 and N+0.5)
    d_edge = min(c1 - 0.5, n1 + 0.5 - c1, c2 - 0.5, n2 + 0.5 - c2)
    corners = [(0.5, 0.5), (0.5, n2 + 0.5), (n1 + 0.5, 0.5), (n1 + 0.5, n2 + 0.5)]
    d_corner = max(math.hypot(x - c1, y - c2) for x, y in corners)
    pasinf = os.path.basename(f[0]).split("_PA")[1].split("_")[0]
    return {"file": os.path.basename(f[0]), "naxis": (n1, n2, n3), "crpix": (c1, c2), "lam_um": lam.tolist(),
            "r_inside_arcsec": d_edge * PIX_ARCSEC, "r_corner_arcsec": d_corner * PIX_ARCSEC, "pasinf": pasinf}


# ---------------------------------------------------------------------------------------------- separations
DS_GRID = np.linspace(-0.8, 0.8, 81)
DC_GRID = np.linspace(-0.7, 0.7, 71)


def chi2_surface(R, gal, truth, fitlaw, Cinv, kern, foot, **kw):
    """chi^2 (no prior) of V_truth(nominal) against V_fitlaw(dstar, dco) on the grid; shape (81, 71)."""
    vt = vpred(R, gal, truth, kern, foot, **kw)
    ds, dc = np.meshgrid(DS_GRID, DC_GRID, indexing="ij")
    vf = vpred(R, gal, fitlaw, kern, foot, dstar=ds, dco=dc, **kw)       # (81, 71, n)
    d = vt[None, None, :] - vf
    return np.einsum("...i,ij,...j->...", d, Cinv, d), ds, dc


def profile(surfs, has_gas):
    """min over the grid of sum(surfs) + priors, then a Nelder-Mead polish is not needed at 0.02-dex steps for a
    forecast; the grid minimum is reported (declared). Returns (chi2_min, dstar_at_min, dco_at_min)."""
    s = sum(surfs)
    ds, dc = np.meshgrid(DS_GRID, DC_GRID, indexing="ij")
    pri = (ds / DEX_MSTAR) ** 2 + ((dc / DEX_CO) ** 2 if has_gas else np.where(np.abs(dc) < 1e-12, 0.0, np.inf))
    tot = s + pri
    k = np.unravel_index(np.argmin(tot), tot.shape)
    return float(tot[k]), float(ds[k]), float(dc[k])


def band_min(surfs, has_gas):
    s = sum(surfs)
    ds, dc = np.meshgrid(DS_GRID, DC_GRID, indexing="ij")
    m = (np.abs(ds) <= DEX_MSTAR + 1e-9) & ((np.abs(dc) <= DEX_CO + 1e-9) if has_gas else (np.abs(dc) < 1e-12))
    return float(np.min(np.where(m, s, np.inf)))


def point_set(gal, kind, fwhm_kpc):
    """radii (kpc) and per-side flags: '3pt_all' (1, 2, 3 R_e), '3pt_reach' (those reachable), 'dense' (every FWHM
    from 1 FWHM to the inside radius, both sides as separate points)."""
    if kind.startswith("3pt"):
        R = np.array([1.0, 2.0, 3.0]) * gal["re"]
        if kind == "3pt_reach":
            R = R[(R <= gal["r_inside_kpc"]) & (R >= fwhm_kpc)]
        return R, np.zeros(R.size, bool)
    n = int(math.floor(gal["r_inside_kpc"] / fwhm_kpc + 1e-9))
    R1 = fwhm_kpc * np.arange(1, n + 1)
    return np.repeat(R1, 2), np.ones(2 * R1.size, bool)


def separations(gal, kind, kern, foot, inc, presc="B", **kw):
    R, side = point_set(gal, kind, gal["fwhm_kpc"])
    if R.size == 0:
        return None
    vF = vpred(R, gal, "flat", kern, foot, **kw)
    vH = vpred(R, gal, "rival", kern, foot, **kw)
    Cm, sd = covariance(R, side, gal, vF, inc, presc)
    Ci = np.linalg.inv(Cm)
    dV = vH - vF
    znom = float(math.sqrt(max(dV @ Ci @ dV, 0.0)))
    has_gas = gal["mgas"] > 0
    res = {"n": int(R.size), "znom": znom}
    for tag, truth, fl in (("HtruthFfit", "rival", "flat"), ("FtruthHfit", "flat", "rival")):
        s, _, _ = chi2_surface(R, gal, truth, fl, Ci, kern, foot, **kw)
        c2, dsm, dcm = profile([s], has_gas)
        res[tag] = {"surf": s, "chi2prof": c2, "dstar": dsm, "dco": dcm, "chi2band": band_min([s], has_gas)}
    res["zprof"] = math.sqrt(min(res["HtruthFfit"]["chi2prof"], res["FtruthHfit"]["chi2prof"]))
    res["zband"] = math.sqrt(min(res["HtruthFfit"]["chi2band"], res["FtruthHfit"]["chi2band"]))
    return res


def strip(res):
    if res is None:
        return None
    o = {k: v for k, v in res.items() if k not in ("HtruthFfit", "FtruthHfit")}
    for tag in ("HtruthFfit", "FtruthHfit"):
        o[tag] = {k: v for k, v in res[tag].items() if k != "surf"}
    return o


# ================================================================================================ run
banner("CFG196 pre-flight: a0 at z ~ 2.2, SINS/zC-SINF AO x PHIBSS 2013 -- a FORECAST from baryons only"
       + ("   [MUTATE=1: rival E(z) -> 1]" if MUTATE else ""))
P(f"  a0 canonical {C4.A0['canonical']:.4e}, alt {C4.A0['alt']:.4e} m/s^2 (kappa = 1/2 FITTED); "
  f"A0 = {A0_KPC['canonical']:.1f} / {A0_KPC['alt']:.1f} (km/s)^2/kpc; G = {G_KPC:.5e} kpc (km/s)^2/Msun")
P(f"  rival: a = a0 E(z), E = sqrt({OMEGA_M_RIVAL} (1+z)^3 + {1 - OMEGA_M_RIVAL:.3f}); E(2.2) = "
  f"{math.sqrt(OMEGA_M_RIVAL * 3.2 ** 3 + 1 - OMEGA_M_RIVAL):.3f} (Omega_m = 0.3 would give "
  f"{math.sqrt(0.3 * 3.2 ** 3 + 0.7):.3f})" + ("  -- MUTATE sets E = 1" if MUTATE else ""))
P(f"  error budget (declared): stat LOS {STAT_KNOTS} km/s at R/R_e (two-side avg; /sin i; x sqrt2 per side in 'dense'),"
  f" di = +/-{DI_DEG} deg (coherent), sigma0 = {SIG0} +/- {DSIG0} km/s (coherent, via alpha), bs {BS_RESID}, "
  f"non-circ {NC_FLOOR} km/s")

# ---- C7: no kinematic column is loaded
PH = load_phibss()
FS = load_fs09()
loaded_cols = set().union(*[set(r) for r in PH]) | set().union(*[set(r) for r in FS.values()])
kin_cols = sorted(c for c in loaded_cols if any(t in c.lower() for t in ("vrot", "vel", "sig", "mdyn", "v_over", "vobs")))
check("C7 no kinematic column loaded (PHIBSS vrot, FS2009 velocities/dispersions/Mdyn are never read)",
      f"loaded columns: {sorted(loaded_cols)}; kinematic-looking: {kin_cols}", len(kin_cols) == 0)

# ---- C0: name match
sins_names = sorted({os.path.basename(p).split("_")[0] for p in glob.glob(os.path.join(SINS_DIR, "*_data_cut.fits"))})
ph_by = {}
for r in PH:
    ph_by.setdefault(r["name"].upper(), []).append(r)
match = sorted(n for n in sins_names if n.upper() in ph_by)
rows_match = {n: ph_by[n.upper()] for n in match}
primary = set()
role = {}
for n in match:
    r = rows_match[n][0]
    r1 = (int(r["co_upper_limit"]) == 0) and (r["comp"].strip() == "") and (n not in ATTRIBUTED_ELSEWHERE)
    r2 = r["type"].strip() == "Disk(A)"
    role[n] = {"R1": r1, "R2": r2, "comp": r["comp"], "type": r["type"], "co_upper_limit": int(r["co_upper_limit"]),
               "attributed_elsewhere": ATTRIBUTED_ELSEWHERE.get(n, "")}
    if r1 and r2:
        primary.add(n)
P(f"\n  SINS AO galaxies: {len(sins_names)}; PHIBSS rows: {len(PH)}; name matches: {len(match)}")
for n in match:
    P(f"    {n:13s} comp='{role[n]['comp']}' type={role[n]['type']:15s} CO_UL={role[n]['co_upper_limit']} "
      f"R1={role[n]['R1']} R2={role[n]['R2']} {role[n]['attributed_elsewhere']}")
ok0 = (set(match) == EXPECTED_MATCH and all(len(rows_match[n]) == 1 for n in match) and primary == FROZEN_PRIMARY
       and len(sins_names) == 35)
check("C0 the name match reproduces the frozen table (6 matches; PRIMARY by R1 and R2 = {ZC406690, Q2343-BX610})",
      f"matches={match}; primary={sorted(primary)}", ok0)
OUT["numbers"]["name_match"] = {"sins_n": len(sins_names), "matches": match, "roles": role, "primary": sorted(primary)}

# ---- C1: kernel limits (P2 as frozen; nu_mono reported)
y = np.array([1e-12, 1e12])
p2 = C4.nu_p2(y) * y
e_lo = abs(p2[0] / math.sqrt(y[0]) - 1.0)
e_hi = abs(p2[1] / y[1] - 1.0)
check("C1 P2 limits: g_pred/sqrt(g a) - 1 < 1e-5 at y = 1e-12, g_pred/g - 1 < 1e-5 at y = 1e12",
      f"{e_lo:.2e}, {e_hi:.2e}", e_lo < 1e-5 and e_hi < 1e-5)
nm = C4.nu_mono(y) * y
P(f"         nu_mono (reported): {abs(nm[0] / math.sqrt(y[0]) - 1):.2e}, {abs(nm[1] / y[1] - 1):.2e}")

# ---- C2: Freeman disc
Rg = np.linspace(0.5, 6.0, 55001)
v2 = v2_freeman(Rg, 1.0, 1.0) / G_KPC
kpk = int(np.argmax(v2))
v2_50 = float(v2_freeman(np.array([50.0]), 1.0, 1.0)[0] * 50.0 / G_KPC)
check("C2 Freeman disc: V^2 peaks at R = 2.15 +/- 0.02 R_d with V^2 R_d/(GM) = 0.387 +/- 0.004; V^2 R/(GM) = 1 +/- 0.01 "
      "at 50 R_d", f"peak R = {Rg[kpk]:.4f} R_d, V^2 R_d/GM = {v2[kpk]:.5f}; at 50 R_d {v2_50:.5f}",
      abs(Rg[kpk] - 2.15) <= 0.02 and abs(v2[kpk] - 0.387) <= 0.004 and abs(v2_50 - 1.0) <= 0.01)

# ---- galaxies: PHIBSS values as tabulated (+ reported variants)
banner("Inputs per galaxy (PHIBSS table values; header geometry; PSF FWHM from the PSF image)")
GAL = []
lam_ok = []
for n in match:
    r = rows_match[n][0]
    fs = FS.get(n.upper())
    z = fnum(r["z_co"])
    zsrc = "z_CO"
    if not np.isfinite(z):
        z = fnum(fs["z_halpha"])
        zsrc = "FS2009 z_Halpha"
    geo = header_geom(n)
    psfp = glob.glob(os.path.join(SINS_DIR, f"{n}_*_psf.fits"))[0]
    fw_g, fw_a = psf_fwhm(psfp)
    kpc_as = float(COSMO_ANG.kpc_proper_per_arcmin(z).value) / 60.0
    lam_ha = LAM_HA_VAC_UM * (1 + z)
    lam_ok.append((n, lam_ha, geo["lam_um"], geo["lam_um"][0] < lam_ha < geo["lam_um"][1]))
    rho = fnum(r["rh_opt_kpc"])
    rco = fnum(r["rh_co_kpc"])
    base = {"name": n, "z": z, "zsrc": zsrc, "mstar": fnum(r["mstar_msun"]), "mgas": fnum(r["mmol_msun"]),
            "re": rho, "re_gas": rco if np.isfinite(rco) else rho, "gas_scale_src": "rh_co" if np.isfinite(rco) else "rh_opt",
            "kpc_per_arcsec": kpc_as, "fwhm_arcsec": fw_g, "fwhm_area_arcsec": fw_a, "fwhm_kpc": fw_g * kpc_as,
            "r_inside_kpc": geo["r_inside_arcsec"] * kpc_as, "r_corner_kpc": geo["r_corner_arcsec"] * kpc_as,
            "geom": geo, "role": "PRIMARY" if n in primary else "reported", "variant": "PHIBSS as tabulated"}
    if n == "Q2343-BX389":
        base["variant"] = "PHIBSS; gas = 3-sigma UPPER LIMIT"
        GAL.append(base)
        g0 = dict(base, mgas=0.0, variant="PHIBSS; gas = 0 (lower bracket)")
        GAL.append(g0)
    elif n == "Q2346-BX482":
        base["variant"] = "PHIBSS row 'se' as tabulated (component BX482se: NOT the main disc's baryons)"
        GAL.append(base)
        re9 = fnum(fs["r_half_halpha_kpc"])
        g1 = dict(base, mstar=fnum(fs["mstar_1e10msun"]) * 1e10, mgas=0.0, re=re9, re_gas=re9,
                  variant="main disc: FS2009 M*, r1/2(Halpha); gas = 0 (none measured)")
        GAL.append(g1)
    else:
        GAL.append(base)
        if fs is not None and np.isfinite(fnum(fs["r_half_halpha_kpc"])) and \
                abs(fnum(fs["r_half_halpha_kpc"]) - rho) > 0.05:
            re9 = fnum(fs["r_half_halpha_kpc"])
            GAL.append(dict(base, re=re9, re_gas=re9, variant=f"size variant: FS2009 r1/2(Halpha) = {re9} kpc"))

check("C6 Halpha at z lies inside every cut cube's wavelength range (header only)",
      "; ".join(f"{n} {l:.4f} in [{a[0]:.4f},{a[1]:.4f}]" for n, l, a, _ in lam_ok), all(t[3] for t in lam_ok))

P("\n  galaxy         role      z      zsrc   E(z)   M*/1e10 Mmol/1e10 R_e  R_e,gas(src)  kpc/\"  PSF FWHM \" (area) kpc"
  "   R_inside/R_corner kpc  PASINF")
for g in GAL:
    P(f"  {g['name']:13s} {g['role']:8s} {g['z']:.3f} {g['zsrc'][:6]:6s} {Ez(g['z']):.3f}  {g['mstar'] / 1e10:6.2f}  "
      f"{g['mgas'] / 1e10:7.2f}  {g['re']:4.1f}  {g['re_gas']:4.1f}({g['gas_scale_src']})  {g['kpc_per_arcsec']:.2f}  "
      f"{g['fwhm_arcsec']:.3f} ({g['fwhm_area_arcsec']:.3f}) {g['fwhm_kpc']:.2f}   {g['r_inside_kpc']:5.1f} / "
      f"{g['r_corner_kpc']:5.1f}   {g['geom']['pasinf']}")
    P(f"      variant: {g['variant']}")

# ================================================================================================ the table
banner("The requested table: V_c at 1, 2, 3 R_e -- P2 kernel, canonical footing, i = 45 deg, PS-B budget\n"
       "  bands = min..max over the 9 mass cells (M* +/- 0.2 dex x Mmol x/ 1.5); reach: in = inside the cut cube,"
       " corner = corner only, out = beyond; res = R >= 1 PSF FWHM")
TABLE = []
for g in GAL:
    R = np.array([1.0, 2.0, 3.0]) * g["re"]
    cells = [(ds, dc) for ds in (-DEX_MSTAR, 0.0, DEX_MSTAR) for dc in ((-DEX_CO, 0.0, DEX_CO) if g["mgas"] > 0 else (0.0,))]
    vN = vpred(R, g, "newton")
    vF = vpred(R, g, "flat")
    vH = vpred(R, g, "rival")
    vFc = np.array([vpred(R, g, "flat", dstar=a, dco=b) for a, b in cells])
    vHc = np.array([vpred(R, g, "rival", dstar=a, dco=b) for a, b in cells])
    gN = gN_of(R, g)
    Cm, sd = covariance(R, np.zeros(3, bool), g, vF, I_CENTRAL, "B")
    _, sdK = covariance(R, np.zeros(3, bool), g, vF, I_CENTRAL, "K")
    aB, aK = alpha_psB(R, g), alpha_psK(R, g)
    vrotB = np.sqrt(np.maximum(vF ** 2 - aB * SIG0 ** 2, 0.0))
    spread = vF - np.sqrt(vrotB ** 2 + aK * SIG0 ** 2)
    presdom = aB * SIG0 ** 2 >= vF ** 2
    P(f"\n  {g['name']} [{g['role']}] -- {g['variant']}")
    P("    R/R_e  R kpc  reach      gN/a0   V_N   V_flat [band]       V_rival [band]      dV    sig_V(B)  dV/sig  "
      "sig_V(K)  overlap  PS-B-PS-K")
    rows = []
    for k in range(3):
        reach = ("in" if R[k] <= g["r_inside_kpc"] else ("corner" if R[k] <= g["r_corner_kpc"] else "out")) + \
                ("/res" if R[k] >= g["fwhm_kpc"] else "/UNRES")
        ov = vFc[:, k].max() >= vHc[:, k].min()
        P(f"    {k + 1:3d}   {R[k]:5.1f}  {reach:10s} {gN[k] / A0_KPC['canonical']:6.2f}  {vN[k]:4.0f}  {vF[k]:4.0f} "
          f"[{vFc[:, k].min():4.0f}-{vFc[:, k].max():4.0f}]   {vH[k]:4.0f} [{vHc[:, k].min():4.0f}-{vHc[:, k].max():4.0f}]  "
          f"{vH[k] - vF[k]:5.1f}   {sd[k]:5.1f}   {(vH[k] - vF[k]) / sd[k]:5.2f}   {sdK[k]:5.1f}    "
          f"{'YES' if ov else 'no ':3s}     {spread[k]:5.1f}{'  [PS-B: V_rot->0 at sigma0=50]' if presdom[k] else ''}")
        rows.append({"R_over_Re": k + 1, "R_kpc": R[k], "reach": reach, "gN_over_a0": gN[k] / A0_KPC["canonical"],
                     "V_newton": vN[k], "V_flat": vF[k], "V_flat_band": [vFc[:, k].min(), vFc[:, k].max()],
                     "V_rival": vH[k], "V_rival_band": [vHc[:, k].min(), vHc[:, k].max()], "dV": vH[k] - vF[k],
                     "sigV_psB": sd[k], "sigV_psK": sdK[k], "dV_over_sig": (vH[k] - vF[k]) / sd[k], "bands_overlap": bool(ov),
                     "psB_minus_psK_kms": spread[k], "pressure_dominated_psB": bool(presdom[k])})
    # other kernels / footings (compact)
    for kern in ("P2", "nu_mono"):
        for foot in ("canonical", "alt"):
            if kern == "P2" and foot == "canonical":
                continue
            vf = vpred(R, g, "flat", kern, foot)
            vh = vpred(R, g, "rival", kern, foot)
            vfc = np.array([vpred(R, g, "flat", kern, foot, dstar=a, dco=b) for a, b in cells])
            vhc = np.array([vpred(R, g, "rival", kern, foot, dstar=a, dco=b) for a, b in cells])
            _, s2 = covariance(R, np.zeros(3, bool), g, vf, I_CENTRAL, "B")
            bf = [f"{vfc[:, k].min():.0f}-{vfc[:, k].max():.0f}" for k in range(3)]
            bh = [f"{vhc[:, k].min():.0f}-{vhc[:, k].max():.0f}" for k in range(3)]
            P(f"    {kern:7s} {foot:9s}: V_flat {np.round(vf).astype(int).tolist()} [{', '.join(bf)}]  V_rival "
              f"{np.round(vh).astype(int).tolist()} [{', '.join(bh)}]  dV {np.round(vh - vf, 1).tolist()}  dV/sig "
              f"{np.round((vh - vf) / s2, 2).tolist()}")
            rows.append({"kernel": kern, "footing": foot, "V_flat": vf, "V_rival": vh, "dV": vh - vf, "dV_over_sig": (vh - vf) / s2,
                         "V_flat_band": [[vfc[:, k].min(), vfc[:, k].max()] for k in range(3)],
                         "V_rival_band": [[vhc[:, k].min(), vhc[:, k].max()] for k in range(3)],
                         "bands_overlap": [bool(vfc[:, k].max() >= vhc[:, k].min()) for k in range(3)]})
    TABLE.append({"name": g["name"], "role": g["role"], "variant": g["variant"], "rows": rows})
OUT["numbers"]["table_1_2_3_Re"] = TABLE

# ================================================================================================ Z per galaxy
banner("Separations per galaxy: Z_nom (nominal masses), Z_prof (masses profiled under Gaussian priors 0.2 dex / "
       "log10 1.5), Z_band (worst case inside the bands)\n  point sets: 3pt_all (1,2,3 R_e, if reached), 3pt_reach, "
       "dense (every FWHM to the inside radius, both sides)")
ZG = {}
P("  galaxy          variant                                   set        n   " +
  "   ".join(f"i={int(i)}: Znom Zprof Zband" for i in INCS))
for g in GAL:
    key = f"{g['name']} | {g['variant']}"
    ZG[key] = {}
    for kind in ("3pt_all", "3pt_reach", "dense"):
        ZG[key][kind] = {}
        cols = []
        nn = 0
        for inc in INCS:
            s = separations(g, kind, "P2", "canonical", inc, "B")
            ZG[key][kind][f"i{int(inc)}"] = strip(s)
            if s is None:
                cols.append("  (no reachable point)  ")
            else:
                nn = s["n"]
                cols.append(f"  {s['znom']:5.2f} {s['zprof']:5.2f} {s['zband']:5.2f}   ")
        P(f"  {g['name']:13s}  {g['variant'][:40]:40s}  {kind:9s} {nn:3d} " + "  ".join(cols))
    # kernel / footing / prescription variants at i = 45, dense
    for kern, foot, presc in (("nu_mono", "canonical", "B"), ("P2", "alt", "B"), ("P2", "canonical", "K")):
        s = separations(g, "dense", kern, foot, I_CENTRAL, presc)
        ZG[key][f"dense_{kern}_{foot}_PS{presc}_i45"] = strip(s)
        if s is not None:
            P(f"      dense i=45 {kern:7s} {foot:9s} PS-{presc}: Znom {s['znom']:5.2f}  Zprof {s['zprof']:5.2f}  "
              f"Zband {s['zband']:5.2f}   (mimicry: flat needs dM* {s['HtruthFfit']['dstar']:+.2f} dex, "
              f"dMmol {s['HtruthFfit']['dco']:+.2f} dex to look like the nominal rival)")
OUT["numbers"]["Z_per_galaxy"] = ZG

# ================================================================================================ sample level: H0
banner("Sample level (PRIMARY = ZC406690 + Q2343-BX610, PHIBSS as tabulated): the feasibility gate H0")
PRIM = [g for g in GAL if g["role"] == "PRIMARY"]
assert {g["name"] for g in PRIM} == FROZEN_PRIMARY and len(PRIM) == 2


def sample_Z(kind, kern, foot, inc, presc, coherent=False, **kw):
    per = []
    for g in PRIM:
        s = separations(g, kind, kern, foot, inc, presc, **kw)
        if s is not None:
            per.append((g, s))
    if not per:
        return None
    res = {"n_gal": len(per), "znom": math.sqrt(sum(s["znom"] ** 2 for _, s in per))}
    best = []
    for tag in ("HtruthFfit", "FtruthHfit"):
        if coherent:
            c2, dsm, dcm = profile([s[tag]["surf"] for _, s in per], True)
            best.append(c2)
            res[tag] = {"chi2prof": c2, "dstar": dsm, "dco": dcm}
        else:
            c2 = sum(s[tag]["chi2prof"] for _, s in per)
            best.append(c2)
            res[tag] = {"chi2prof": c2}
    res["zprof"] = math.sqrt(min(best))
    return res


def h0_class(z):
    if z is None:
        return "NO REACHABLE POINT"
    return ("CAN be decisive (forecast, >= 3)" if z >= 3 else
            "CAN discriminate at 2 sigma (forecast)" if z >= 2 else "CANNOT discriminate (forecast, < 2)")


H0 = sample_Z("dense", "P2", "canonical", I_CENTRAL, "B")
P(f"  H0 (declared: dense, reachable, P2, canonical, PS-B budget, i = 45, independent nuisances): "
  f"Z_nom = {H0['znom']:.2f}, Z_prof = {H0['zprof']:.2f}  ->  {h0_class(H0['zprof'])}")
H0VAR = {}
for lab, args in (("i=30", ("dense", "P2", "canonical", 30.0, "B")), ("i=60", ("dense", "P2", "canonical", 60.0, "B")),
                  ("nu_mono", ("dense", "nu_mono", "canonical", 45.0, "B")), ("alt footing", ("dense", "P2", "alt", 45.0, "B")),
                  ("PS-K budget", ("dense", "P2", "canonical", 45.0, "K")),
                  ("3pt_reach", ("3pt_reach", "P2", "canonical", 45.0, "B")),
                  ("3pt_all (optimistic: if 1-3 R_e were all reached)", ("3pt_all", "P2", "canonical", 45.0, "B"))):
    s = sample_Z(*args)
    H0VAR[lab] = s
    P(f"    variant {lab:52s}: " + ("no reachable point" if s is None else
                                    f"Z_nom {s['znom']:5.2f}  Z_prof {s['zprof']:5.2f}  -> {h0_class(s['zprof'])}"))
sc = sample_Z("dense", "P2", "canonical", I_CENTRAL, "B", coherent=True)
H0VAR["coherent shared (dM*, dMmol)"] = sc
P(f"    variant {'coherent: one shared (dM*, dMmol) for both galaxies':52s}: Z_prof {sc['zprof']:5.2f} "
  f"(rival-truth mimicked by flat at dM* {sc['HtruthFfit']['dstar']:+.2f}, dMmol {sc['HtruthFfit']['dco']:+.2f} dex)"
  f" -> {h0_class(sc['zprof'])}")
OUT["numbers"]["H0"] = {"declared": H0, "class": h0_class(H0["zprof"]), "variants": H0VAR}

# ---- stress rows (reported; primary only; dense, P2, canonical, i=45, PS-B)
banner("Stress rows (reported, never in the verdict grid): primary galaxies, dense, P2, canonical, i = 45, PS-B")
STRESS = {}
for lab, kw in (("nominal", {}), ("alpha_CO ULIRG-like (Mmol x 0.8/4.36)", {"gas_fac": ULIRG_FAC}),
                ("stellar R_e = rh_opt/1.3", {"rstar_fac": 1 / 1.3}), ("HI h = 0.5 at 2x gas scale", {"hi": 0.5}),
                ("spherical shortcut geometry", {"geom": "sphere"})):
    s = sample_Z("dense", "P2", "canonical", I_CENTRAL, "B", **kw)
    one = {g["name"]: (float(vpred(np.array([g["re"]]), g, "rival", **kw)[0] - vpred(np.array([g["re"]]), g, "flat", **kw)[0]),
                       float(vpred(np.array([g["re"]]), g, "newton", **kw)[0])) for g in PRIM}
    STRESS[lab] = {"sample": s, "dV_at_1Re_and_VN": one}
    P(f"  {lab:40s}: sample Z_prof {s['zprof']:5.2f} | dV(1 R_e), V_N(1 R_e): " +
      "; ".join(f"{k} {v[0]:+.1f}, {v[1]:.0f} km/s" for k, v in one.items()))
OUT["numbers"]["stress"] = STRESS

# ---- POST-HOC diagnostic (added after the first run, which is kept as *_firstrun*; reported only; H0 unchanged):
#      what limits the forecast -- the kinematic budget or the mass calibration?
banner("POST-HOC diagnostic (added after the first run; reported only; H0 above is unchanged)\n"
       "  (i) near-perfect kinematics: C = (1 km/s)^2 I, no inclination or sigma0 term, mass priors as declared -- does the\n"
       "      rival/flat SHAPE difference survive the mass freedom? (1 km/s is unphysical; this is a limit, not a forecast)\n"
       "  (ii) masses known exactly: Z_nom with the declared kinematic budget\n"
       "  (iii) ablation: the declared-set sample Z_prof with ONE budget term changed at a time")
POSTHOC = {}
for kind in ("dense", "3pt_all"):
    per = {}
    tot = {"HtruthFfit": 0.0, "FtruthHfit": 0.0}
    for g in PRIM:
        R, side = point_set(g, kind, g["fwhm_kpc"])
        Ci = np.eye(R.size)
        best = []
        for tag, truth, fl in (("HtruthFfit", "rival", "flat"), ("FtruthHfit", "flat", "rival")):
            s, _, _ = chi2_surface(R, g, truth, fl, Ci, "P2", "canonical")
            c2, dsm, dcm = profile([s], True)
            tot[tag] += c2
            best.append((c2, dsm, dcm, tag))
        b = min(best)
        per[g["name"]] = {"zprof_perfect_kin": math.sqrt(b[0]), "dstar": b[1], "dco": b[2], "direction": b[3], "n": int(R.size)}
    zs = math.sqrt(min(tot.values()))
    POSTHOC[kind] = {"per_galaxy": per, "sample_zprof_perfect_kin": zs}
    P(f"  {kind:8s}: sample Z_prof (perfect kinematics, priors 0.2 dex / log10 1.5) = {zs:.2f}  -> {h0_class(zs)}; " +
      "; ".join(f"{k} {v['zprof_perfect_kin']:.2f} (n={v['n']}, masses shift dM* {v['dstar']:+.2f}, dMmol {v['dco']:+.2f})"
                for k, v in per.items()))
P(f"  (ii) masses known exactly, declared budget, dense: sample Z_nom = {H0['znom']:.2f}; 3pt_all: "
  f"{H0VAR['3pt_all (optimistic: if 1-3 R_e were all reached)']['znom']:.2f}")
ABL = {}
_ZERO_STAT = ((1.0, 0.0), (2.0, 0.0), (3.0, 0.0))
for lab, changes in (("declared (reference)", {}),
                     ("inclination error 0 (i known exactly)", {"DI_DEG": 0.0}),
                     ("inclination error 2 deg", {"DI_DEG": 2.0}),
                     ("sigma0 error 0 (sigma0 known exactly)", {"DSIG0": 0.0}),
                     ("statistical error 0", {"STAT_KNOTS": _ZERO_STAT}),
                     ("non-circular floor 0", {"NC_FLOOR": 0.0}),
                     ("beam-smearing residual 0", {"BS_RESID": 0.0}),
                     ("inclination AND sigma0 known exactly", {"DI_DEG": 0.0, "DSIG0": 0.0}),
                     ("mass priors halved (0.1 dex; x/1.22)", {"DEX_MSTAR": DEX_MSTAR / 2, "DEX_CO": DEX_CO / 2}),
                     ("i and sigma0 exact + mass priors halved", {"DI_DEG": 0.0, "DSIG0": 0.0, "DEX_MSTAR": DEX_MSTAR / 2,
                                                                  "DEX_CO": DEX_CO / 2})):
    old = {k: globals()[k] for k in changes}
    globals().update(changes)
    try:
        sd_ = sample_Z("dense", "P2", "canonical", I_CENTRAL, "B")
        s3_ = sample_Z("3pt_all", "P2", "canonical", I_CENTRAL, "B")
    finally:
        globals().update(old)
    ABL[lab] = {"dense": sd_, "3pt_all": s3_}
    P(f"  (iii) {lab:42s}: dense Z_nom {sd_['znom']:5.2f} Z_prof {sd_['zprof']:5.2f} | 3pt_all (if reached) "
      f"Z_nom {s3_['znom']:5.2f} Z_prof {s3_['zprof']:5.2f}")
POSTHOC["ablation"] = ABL
OUT["numbers"]["posthoc_limits"] = POSTHOC

# ================================================================================================ headline S1
banner("Headline S1 [MUTATE must change it]")
dvs = [r["dV"] for t in TABLE for r in t["rows"] if "R_over_Re" in r]
zn = [ZG[k]["3pt_all"]["i45"]["znom"] for k in ZG if ZG[k]["3pt_all"]["i45"] is not None]
check("S1 the rival and flat predictions differ: dV > 0 at every radius of every galaxy row, and Z_nom > 0",
      f"min dV = {min(dvs):.3e} km/s over {len(dvs)} points; min Z_nom (3pt_all, i=45) = {min(zn):.3e}",
      min(dvs) > 1e-6 and min(zn) > 1e-6)
check("H0 the test CAN discriminate at >= 2 sigma (forecast; declared set)", f"Z_prof = {H0['zprof']:.2f} -> "
      f"{h0_class(H0['zprof'])}", H0["zprof"] >= 2.0, load_bearing=False)

npass = sum(1 for _, ok, _ in CHECKS if ok)
nlb = sum(1 for _, ok, lb in CHECKS if (not ok) and lb)
OUT["summary"] = {"n_checks": len(CHECKS), "n_pass": npass, "load_bearing_failures": nlb,
                  "failed": [k for k, ok, _ in CHECKS if not ok], "seconds": round(time.time() - T0, 1)}
with builtins.open(JSON_PATH, "w", encoding="utf-8") as fh:
    json.dump(jclean(OUT), fh, indent=1)
P(f"\n  {npass}/{len(CHECKS)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(JSON_PATH)} "
  f"({time.time() - T0:.1f} s)")
rc = 1 if nlb else 0
P(f"rc = {rc}")
sys.stdout = TEE.o
TEE.f.close()
sys.exit(rc)
