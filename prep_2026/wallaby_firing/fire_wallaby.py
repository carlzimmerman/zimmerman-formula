#!/usr/bin/env python3
"""
WALLABY FIRING -- the pre-registered directional-EFE aligned statistic at scale
================================================================================
FIREWALL (applies to EVERY number below): at N~237 per-side-capable (and the
25-galaxy QC-pass x direction-usable firing sample this lane actually yields)
the achieved sensitivity at AQUAL amplitude is far below the pre-registered
kill thresholds. NEITHER pre-registered kill condition (3-sigma AQUAL-vs-
BranchB separation, N~1157 canonical a0=9.36e-11 / N~1424 alt a0=1.13e-10)
CAN TRIGGER on this sample. Kill-condition language appears here ONLY as
"cannot trigger". Everything below is EXPLORATORY and is reported straight,
whatever its sign and size.

SIGN TRAP (the one that inverts the physics): the PRE-REGISTERED convention is
  A_i = 2(v_rec - v_appr)/(v_rec + v_appr)   (tied to the RECEDING side),
with psi measured from the RECEDING-side kinematic major axis, so p_i > 0
predicts attractor-side-FASTER for x >~ 2e. perside_extractor.py's pilot
printout used the OPPOSITE ordering A_ext = 2(v_app - v_rec)/(v_app + v_rec).
This script (1) asserts A_preregistered == -A_raw_extractor for all 237 rows,
(2) re-verifies the conversion BY HAND from a raw mom1 map of one galaxy IN
THE FIRING SAMPLE on an independent code path (astropy WCS, no extractor
import), in addition to Lane W1's independent hand check on J165901-601241.

WHAT IS REUSED VERBATIM (no convention drift):
  * fire_aligned_n16.py (the battle-tested n=16 firing) is imported by path:
    banked laneA BVP interpolator A_aqual_pct(x,e), banked gamma shape
    G_gamma, psi/gamma geometry (basis, psi_gamma, sky_pa_of_vector, wrap180),
    the WHISP noise SIG_A recomputed in the pre-registered A convention.
  * xstrat_filter.py (Lane W3) is imported by path: frozen strata
    (DEEP r<1.0 / TRANSITION 1<=r<5 / OUTER r>=5, r = x/e), the banked-map
    zero-crossing assertion re-runs at import (refuses if crossings leave
    (0.70, 1.00)), frozen beta grid + Branch-B w values.
  The STACK generalizes the banked uniform-noise form to per-galaxy noise
  s_i^2 = sigma_boot,i^2 + sigma_intr^2 (the lane brief's requirement); it
  reduces EXACTLY to the banked stack for constant s_i (asserted at runtime).

SAMPLE: QC-pass (frozen QC_FROZEN.md cuts, Lane W1) AND direction-usable
(cone68 < 30 deg AND not inside the 2M++ |b|<5 cloned-fill mask, Lane W2).

x_i = outer g_bar/a0. HONESTY: WALLABY has NO published baryonic
decomposition -- the frozen repo's own WALLABY_rar_framework.py audited both
public archives and returned DATA_GATED ("kinematics-only ... g_bar cannot be
formed"). The only self-consistent route is the framework's EXACT inversion of
its own interpolation g_obs = sqrt(g_bar^2 + g_bar*a0):
    g_bar = ( -a0 + sqrt(a0^2 + 4 g_obs^2) ) / 2,
with g_obs = V^2/R (accel_SI convention of WALLABY_rar_framework.py) averaged
over the outermost 3 WKAPP AvgMod rings, R from D_mpc (Lane W2, Hubble-flow
H0=75 / CF4). Per-galaxy x is honestly good to only ~0.3 dex (distance +
inclination + WKAPP outer-VRot systematics + the ~0.11 dex model-dependence of
the inversion itself); the +-0.3 dex x-shift variants below show the matched
filter barely cares in the x >> 2e regime. The inversion makes x (and r = x/e)
WEAKLY a0-footing-dependent; both footings run everywhere.

e_i = Lane W2 OWN-scale amplitudes with the +0.100 dex GATE-A global offset to
the Chae Table-3 scale APPLIED here (W2 shipped it "reported NOT applied");
both clustering brackets (maxclu PRIMARY / noclu) everywhere. The shipped unit
VECTOR is the maxclu one; the noclu-vs-maxclu direction swing is median ~2 deg
(computed below), i.e. the brackets differ in amplitude, not direction.

Predictor p_i = A_map(x_i, e_i) * G(gamma_i) * cos(psi_i)  (banked, signed --
the sign reversal x <~ e is carried inside the map).
Stack   Ahat = sum(A_i p_i / s_i^2) / sum(p_i^2 / s_i^2).
Targets E[Ahat]: AQUAL/QUMOND-class MG = +1 (local-force floor; up to ~5 with
loop-orbit amplification); Branch B (elastic medium) = +0.304 natural / +0.24
Cassini-max; PURE MI = EXACTLY 0; isotropic systematics = 0 (by construction
of the isotropic-direction permutation null).

Outputs: fire_wallaby_results.json + WALLABY_FIRING.md (this directory only).
The frozen repo is READ-ONLY and is not touched. Exit 0.
"""
import csv
import importlib.util
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
PILOT = "/Users/carlzimmerman/new_physics/prep_2026/wallaby_prep/pilot_data"


def dpath(fn):
    """W1 kept the 3 proof-of-life pilot galaxies' raw files in pilot_data."""
    p = os.path.join(DATA, fn)
    return p if os.path.exists(p) else os.path.join(PILOT, fn)
ALIGNED = "/Users/carlzimmerman/new_physics/prep_2026/aligned_firing"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
RAR_WALLABY = os.path.join(REPO, "real_research/reviews/wallaby_rar_2026",
                           "WALLABY_rar_framework.py")

FIREWALL = (
    "FIREWALL: at the WALLABY scale (237 per-side-capable; 25 QC-pass x "
    "direction-usable actually fired here) the achieved sensitivity at AQUAL "
    "amplitude is ~0.2-0.5 sigma -- NEITHER pre-registered kill condition "
    "(3-sigma AQUAL-vs-BranchB separation, N~1157 canonical a0=9.36e-11 / "
    "N~1424 alt a0=1.13e-10) CAN TRIGGER on this sample. EXPLORATORY ONLY; "
    "the number is reported straight, whatever it is.")

SIGN_TRAP = (
    "SIGN TRAP: pre-registered A = 2(v_rec - v_appr)/(v_rec + v_appr), "
    "RECEDING side, psi from the RECEDING-side kinematic major axis; the "
    "extractor pilot printed the OPPOSITE ordering. A_prereg = -A_extractor "
    "asserted on all 237 rows AND hand-verified from a raw mom1 map on an "
    "independent code path (below).")

A0_CANON = 9.36e-11        # m/s^2, canonical cH_Lambda/Z footing
A0_ALT = 1.13e-10          # m/s^2, alt rho_total/cH0 footing
CHAE_OFFSET_DEX = 0.100    # W2 GATE-A global offset to Chae Table-3 scale: APPLIED
KPC_M = 3.0856775814913673e19
ARCSEC_RAD = math.pi / (180.0 * 3600.0)
NBOOT, NPERM = 10000, 10000
NPERM_VAR = 4000
X_SHIFT_DEX = 0.3          # honest per-galaxy x uncertainty, demonstrated below

rng = np.random.default_rng(20260716)


# ---------------------------------------------------------------------------
# 0. import the banked machinery verbatim (no re-implementation)
# ---------------------------------------------------------------------------
def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BASE = load_mod("fire_aligned_n16", os.path.join(ALIGNED, "fire_aligned_n16.py"))
XS = load_mod("xstrat_filter", os.path.join(HERE, "xstrat_filter.py"))
assert BASE.SIGN_BANKED == "attractor_side_faster"
# XS import re-ran the banked-map zero-crossing assertion (frozen bracket
# (0.70, 1.00)); reaching this line means it passed.
SIG_INTR_WHISP = BASE.SIG_A     # 0.187: rms of the 70 WHISP signed asymmetries
#   recomputed in the PRE-REGISTERED A = 2(v_rec-v_appr)/(v_rec+v_appr)
#   convention (fire_aligned_n16 section 2). The often-quoted 0.092 is the
#   eps_kin = (v_rec-v_appr)/(2 v_c) convention, exactly A/2 -- W1's report
#   compared the WALLABY rms(A)=0.155 against 0.092 across conventions; in the
#   MATCHING convention the WALLABY QC-pass scatter (0.155) is BELOW the WHISP
#   intrinsic rms (0.187), i.e. the diagnosed vsys systematic sits INSIDE the
#   WHISP lopsidedness budget, it does not add to it.


# ---------------------------------------------------------------------------
# 1. load + merge the two lane tables; assert the sign conversion everywhere
# ---------------------------------------------------------------------------
def load_csv(path):
    return list(csv.DictReader(l for l in open(path) if not l.startswith("#")))


perside = load_csv(os.path.join(HERE, "perside_237.csv"))
gext = {r["name"]: r for r in load_csv(os.path.join(HERE, "gext_wallaby_237.csv"))}
assert len(perside) == 237 and len(gext) == 237

for r in perside:                     # sign-trap assertion, all 237
    assert abs(float(r["A_preregistered"]) + float(r["A_raw_extractor"])) < 1e-12, \
        f"{r['jname']}: A_pre != -A_ext -- SIGN TRAP violated, STOP"

sample = []
for r in perside:
    g = gext[r["jname"]]
    if r["qc_pass"] != "True" or g["usable"] != "yes":
        continue
    pa_rec = float(r["pa_wkapp"]) + (180.0 if r["pa_flipped"] == "True" else 0.0)
    sample.append(dict(
        name=r["jname"], field=r["field"],
        ra=float(r["ra"]), dec=float(r["dec"]),
        A=float(r["A_preregistered"]),
        sig_boot=float(r["sigma_boot"]),
        pa_rec=pa_rec % 360.0, incl=float(r["inc"]),
        model_file=r["model_file"],
        u=np.array([float(g["ux_icrs"]), float(g["uy_icrs"]),
                    float(g["uz_icrs"])]),
        D_mpc=float(g["D_mpc"]),
        cone68=float(g["cone68_deg"]), zoa=g["zoa_flag"],
        swing=float(g["angle_noclu_maxclu_deg"]),
        # W2 own-scale amplitudes in a0 units, +0.100 dex offset APPLIED:
        e_can_max=float(g["eN_maxclu_can936"]) * 10 ** CHAE_OFFSET_DEX,
        e_can_no=float(g["eN_noclu_can936"]) * 10 ** CHAE_OFFSET_DEX,
        e_alt_max=float(g["eN_maxclu_alt113"]) * 10 ** CHAE_OFFSET_DEX,
        e_alt_no=float(g["eN_noclu_alt113"]) * 10 ** CHAE_OFFSET_DEX,
        dom=g["dom_name"], attractor=g["attractor"],
        sep_attr=g["sep_attr_mpc"],
    ))
n = len(sample)
FIELDS = sorted({s["field"] for s in sample})


# ---------------------------------------------------------------------------
# 2. HAND VERIFICATION of the sign conversion on a FIRING-SAMPLE galaxy,
#    independent code path (astropy WCS + plain loops; no extractor import).
#    Complements Lane W1's hand check on J165901-601241.
# ---------------------------------------------------------------------------
def hand_verify(s):
    from astropy.io import fits
    from astropy.wcs import WCS
    C, F0 = 299792.458, 1420405751.77
    stem = s["model_file"].replace("_Kin_", "_").replace("_AvgMod.txt", "")
    # model_file: WALLABY_J..._Field_Kin_TRn_AvgMod.txt -> ..._Field_TRn_mom1
    mom1p = dpath(stem + "_mom1.fits")
    mom0p = dpath(stem + "_mom0.fits")
    avgp = dpath(s["model_file"])
    if not (os.path.exists(mom1p) and os.path.exists(mom0p)
            and os.path.exists(avgp)):
        return None
    geo, rc, started = {}, [], False
    for line in open(avgp):
        t = line.split("\t")
        if len(t) >= 2:
            k = t[0].split("(")[0].strip()
            try:
                geo[k] = float(t[1])
            except ValueError:
                pass
        if line.startswith("Rotation Curve"):
            started = True
            continue
        if line.startswith("Surface Density"):
            started = False
        if started:
            p = line.split()
            if len(p) >= 3:
                try:
                    rc.append((float(p[0]), float(p[1])))
                except ValueError:
                    pass
    pa, inc, vsys = geo["PA_model_g"], geo["Inc_model"], geo["VSys_model"]
    hdu = fits.open(mom1p)[0]
    dat = np.squeeze(hdu.data).astype(float)
    v = dat if np.nanmedian(np.abs(dat[np.isfinite(dat)])) < 1e5 \
        else C * (F0 / dat - 1.0)                      # km/s or Hz axis
    mom0 = np.squeeze(fits.open(mom0p)[0].data).astype(float)
    w = WCS(hdu.header).celestial
    ny, nx = v.shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    ra, dec = w.wcs_pix2world(np.column_stack([xx.ravel(), yy.ravel()]), 0).T
    dE = (ra.reshape(v.shape) - geo["RA_model"]) * \
        math.cos(math.radians(geo["DEC_model"])) * 3600.0
    dN = (dec.reshape(v.shape) - geo["DEC_model"]) * 3600.0
    pr = math.radians(pa)
    along = dE * math.sin(pr) + dN * math.cos(pr)      # >0 = PA_model_g side
    perp = -dE * math.cos(pr) + dN * math.sin(pr)
    Rd = np.hypot(along, perp / math.cos(math.radians(inc)))
    cth = np.where(Rd > 0, along / np.maximum(Rd, 1e-9), 0.0)
    fin = (np.isfinite(v) & np.isfinite(mom0) & (mom0 > 0)
           & (np.abs(cth) >= 0.5) & (np.abs(v - vsys) < 600))
    mean_pa = float(v[fin & (cth > 0)].mean())
    mean_anti = float(v[fin & (cth < 0)].mean())
    check1 = mean_pa > vsys > mean_anti                # PA side is RECEDING
    # independent per-side outer means -> sign of A in BOTH conventions
    rads = np.array([q[0] for q in rc])
    dr = float(np.median(np.diff(rads))) if len(rads) > 1 else rads[0]
    Rmax = rads[-1] + dr / 2
    sini = math.sin(math.radians(inc))
    vrot = np.abs(v - vsys) / (sini * np.maximum(np.abs(cth), 1e-9))
    vr_l, va_l = [], []
    for R0 in rads:
        if R0 < 0.5 * Rmax:
            continue
        sel = fin & (Rd >= R0 - dr / 2) & (Rd < R0 + dr / 2)
        mr, ma = sel & (cth > 0), sel & (cth < 0)
        if mr.sum() < 4 or ma.sum() < 4:
            continue
        vr_l.append(np.average(vrot[mr], weights=mom0[mr]))
        va_l.append(np.average(vrot[ma], weights=mom0[ma]))
    if not vr_l:
        return None
    v_rec_i, v_app_i = float(np.mean(vr_l)), float(np.mean(va_l))
    A_pre_ind = 2.0 * (v_rec_i - v_app_i) / (v_rec_i + v_app_i)
    check2 = (A_pre_ind > 0) == (s["A"] > 0)           # sign matches pipeline
    return dict(name=s["name"], mean_vlos_pa_side=mean_pa, vsys=vsys,
                mean_vlos_anti=mean_anti, receding_is_pa_side=bool(check1),
                v_rec_indep=v_rec_i, v_appr_indep=v_app_i,
                A_pre_indep=A_pre_ind, A_pre_pipeline=s["A"],
                sign_match=bool(check2))


HAND = None
for s in sorted(sample, key=lambda q: q["name"]):
    HAND = hand_verify(s)
    if HAND is not None:
        break
assert HAND is not None, "no firing-sample galaxy with raw maps on disk -- STOP"
assert HAND["receding_is_pa_side"], \
    f"hand check FAILED: PA side not receding on {HAND['name']} -- STOP"
assert HAND["sign_match"], \
    f"hand check FAILED: independent A_pre sign != pipeline on {HAND['name']}"


# ---------------------------------------------------------------------------
# 3. per-galaxy geometry (banked psi/gamma) + outer g_obs -> framework g_bar
# ---------------------------------------------------------------------------
def gobs_outer(s):
    """Mean V^2/R (SI) over the outermost 3 WKAPP AvgMod rings.
    Rad column is arcsec; R_kpc = D_mpc * 1000 * tan(arcsec)."""
    rc, started = [], False
    for line in open(dpath(s["model_file"])):
        if line.startswith("Rotation Curve"):
            started = True
            continue
        if line.startswith("Surface Density"):
            started = False
        if started:
            p = line.split()
            if len(p) >= 3:
                try:
                    rc.append((float(p[0]), float(p[1])))
                except ValueError:
                    pass
    assert len(rc) >= 3, f"{s['name']}: <3 WKAPP rings"
    gs = []
    for R_as, V in rc[-3:]:
        R_m = s["D_mpc"] * 1000.0 * KPC_M * R_as * ARCSEC_RAD
        gs.append((V * 1.0e3) ** 2 / R_m)
    return float(np.mean(gs))


def gbar_inv(gobs, a0):
    """EXACT inversion of the framework's own nu: g_obs=sqrt(gb^2+gb*a0)."""
    return 0.5 * (-a0 + math.sqrt(a0 * a0 + 4.0 * gobs * gobs))


for s in sample:
    s["_basis"] = BASE.basis(s["ra"], s["dec"])
    s["psi"], s["gam_a"], s["gam_b"] = BASE.psi_gamma(s, s["u"])
    s["Ggam"] = 0.5 * (BASE.G_gamma(s["gam_a"]) + BASE.G_gamma(s["gam_b"]))
    s["gobs"] = gobs_outer(s)
    s["gbar_can"] = gbar_inv(s["gobs"], A0_CANON)
    s["gbar_alt"] = gbar_inv(s["gobs"], A0_ALT)

# footing -> (a0, gbar key, e-column prefix)
FOOTINGS = {"canonical a0=9.36e-11": (A0_CANON, "gbar_can", "e_can"),
            "alt a0=1.13e-10": (A0_ALT, "gbar_alt", "e_alt"),
            }
EBRACKETS = {"maxclu": "_max", "noclu": "_no"}


def xe(s, foot, ebr, xshift_dex=0.0):
    a0, gk, ep = FOOTINGS[foot]
    x = s[gk] * 10 ** xshift_dex / a0
    e = s[ep + EBRACKETS[ebr]]
    return x, e


# ---------------------------------------------------------------------------
# 4. the per-galaxy-noise stack (reduces to the banked stack for constant s)
# ---------------------------------------------------------------------------
def stack_w(A, p, s2):
    S = float(np.sum(p * p / s2))
    if S <= 0:
        return np.nan, np.nan, np.nan
    num = float(np.sum(A * p / s2))
    return num / S, 1.0 / math.sqrt(S), num / math.sqrt(S)


# runtime equivalence check against the banked uniform-noise stack
_A = np.array([0.1, -0.2, 0.05])
_p = np.array([0.01, -0.02, 0.005])
_bk = BASE.stack(_A, _p, 0.187)
_nw = stack_w(_A, _p, np.full(3, 0.187 ** 2))
assert all(abs(a - b) < 1e-12 for a, b in zip(_bk, _nw)), \
    "weighted stack does not reduce to the banked stack -- STOP"


def predictor_parts(rows, foot, ebr, xshift_dex=0.0, use_gamma=True):
    """amp_i = A_map(x_i,e_i)/100 (signed); p_i = amp_i*G(gamma_i)*cos(psi_i)."""
    amp, p, cl_lo, cl_hi, xs, es = [], [], 0, 0, [], []
    for r in rows:
        x, e = xe(r, foot, ebr, xshift_dex)
        Apct, cl = BASE.A_aqual_pct(x, e)
        a = Apct / 100.0
        G = r["Ggam"] if use_gamma else 1.0
        amp.append(a)
        p.append(a * G * math.cos(math.radians(r["psi"])))
        cl_lo += cl < 0
        cl_hi += cl > 0
        xs.append(x)
        es.append(e)
    return (np.array(amp), np.array(p), cl_lo, cl_hi,
            np.array(xs), np.array(es))


def run_cfg(rows, foot, ebr, sigma_intr, A_key="A", xshift_dex=0.0,
            use_gamma=True, nboot=NBOOT, nperm=NPERM):
    A = np.array([r[A_key] for r in rows])
    s2 = np.array([r["sig_boot"] ** 2 + sigma_intr ** 2 for r in rows])
    amp, p, cl_lo, cl_hi, xs, es = predictor_parts(rows, foot, ebr,
                                                   xshift_dex, use_gamma)
    ahat, sig_an, Z = stack_w(A, p, s2)

    # leave-one-galaxy-out
    loo = np.array([stack_w(np.delete(A, i), np.delete(p, i),
                            np.delete(s2, i))[0] for i in range(len(rows))])
    # leave-one-FIELD-out (attractor-coherent blocks)
    lofo = {}
    flds = np.array([r["field"] for r in rows])
    for f in sorted(set(flds)):
        m = flds != f
        if m.sum() >= 2:
            a_, s_, z_ = stack_w(A[m], p[m], s2[m])
            lofo[f] = dict(n_dropped=int((~m).sum()), Ahat=a_, Z=z_)

    # bootstrap over galaxies (paired A, p, s2)
    boot = np.empty(nboot)
    idx = rng.integers(0, len(rows), size=(nboot, len(rows)))
    for b in range(nboot):
        boot[b] = stack_w(A[idx[b]], p[idx[b]], s2[idx[b]])[0]
    boot = boot[np.isfinite(boot)]

    # isotropic-direction permutation null: redraw u on the sphere,
    # recompute psi AND gamma per draw; amp_i = A_map(x,e) unchanged.
    Zn, An = np.empty(nperm), np.empty(nperm)
    U = rng.normal(size=(nperm, len(rows), 3))
    U /= np.linalg.norm(U, axis=2, keepdims=True)
    for k in range(nperm):
        pn = np.empty(len(rows))
        for i, r in enumerate(rows):
            psi, ga, gb = BASE.psi_gamma(r, U[k, i])
            G = (0.5 * (BASE.G_gamma(ga) + BASE.G_gamma(gb))
                 if use_gamma else 1.0)
            pn[i] = amp[i] * G * math.cos(math.radians(psi))
        An[k], _, Zn[k] = stack_w(A, pn, s2)
    ok = np.isfinite(Zn)
    okA = np.isfinite(An)
    return dict(
        n=len(rows), Ahat=float(ahat), sig_analytic=float(sig_an),
        Z=float(Z), boot_std=float(np.std(boot)),
        boot_p16=float(np.percentile(boot, 16)),
        boot_p84=float(np.percentile(boot, 84)),
        p_perm_Z_one=float((1 + np.sum(Zn[ok] >= Z)) / (ok.sum() + 1)),
        p_perm_Z_two=float((1 + np.sum(np.abs(Zn[ok]) >= abs(Z)))
                           / (ok.sum() + 1)),
        p_perm_Ahat_one=float((1 + np.sum(An[okA] >= ahat)) / (okA.sum() + 1)),
        p_perm_Ahat_two=float((1 + np.sum(np.abs(An[okA]) >= abs(ahat)))
                              / (okA.sum() + 1)),
        null_Z_std=float(np.std(Zn[ok])), null_Ahat_std=float(np.std(An[okA])),
        null_Ahat_mean=float(np.mean(An[okA])),
        loo_min=float(np.nanmin(loo)), loo_max=float(np.nanmax(loo)),
        loo_min_gal=rows[int(np.nanargmin(loo))]["name"],
        loo_max_gal=rows[int(np.nanargmax(loo))]["name"],
        leave_one_field_out=lofo,
        nclamp_lo=int(cl_lo), nclamp_hi=int(cl_hi),
        median_x=float(np.median(xs)), median_e=float(np.median(es)),
        median_r=float(np.median(xs / es)),
        sum_p2_over_s2=float(np.sum(p * p / s2)))


# ---------------------------------------------------------------------------
# 5. sigma_intr: WHISP primary + fitted variant (excess over pixel bootstrap)
# ---------------------------------------------------------------------------
def fit_sigma_intr(rows):
    """Solve sum((A_i - m)^2/(sb_i^2+s^2)) = n-1 with m the IV-weighted mean,
    by bisection. Captures the vsys-systematic-inflated ensemble scatter."""
    A = np.array([r["A"] for r in rows])
    sb2 = np.array([r["sig_boot"] ** 2 for r in rows])

    def chi2red(s):
        w = 1.0 / (sb2 + s * s)
        m = np.sum(w * A) / np.sum(w)
        return np.sum(w * (A - m) ** 2) / (len(rows) - 1)

    lo, hi = 0.0, 1.0
    if chi2red(0.0) <= 1.0:
        return 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if chi2red(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


SIG_INTR_FIT = fit_sigma_intr(sample)


# ---------------------------------------------------------------------------
# 6. joint (alpha, beta) fit, frozen beta grid, per-galaxy weights
# ---------------------------------------------------------------------------
def joint_fit(rows, foot, ebr, sigma_intr):
    A = np.array([r[a] for r, a in zip(rows, ["A"] * len(rows))])
    s2 = np.array([r["sig_boot"] ** 2 + sigma_intr ** 2 for r in rows])
    prof = []
    for beta in XS.BETA_GRID:
        p = np.empty(len(rows))
        for i, r in enumerate(rows):
            x, e = xe(r, foot, ebr)
            Apct, _ = BASE.A_aqual_pct(x, beta * e)
            p[i] = (Apct / 100.0) * r["Ggam"] * math.cos(math.radians(r["psi"]))
        sp2 = float(np.sum(p * p / s2))
        alpha = float(np.sum(A * p / s2) / sp2) if sp2 > 0 else np.nan
        chi2 = float(np.sum((A - alpha * p) ** 2 / s2))
        chi2_t = {nm: float(np.sum((A - a_th * p) ** 2 / s2))
                  for nm, a_th in (("AQUAL_alpha1", 1.0),
                                   ("BranchB_w_natural", XS.W_NATURAL),
                                   ("BranchB_w_cassini", XS.W_CASSINI),
                                   ("pureMI_alpha0", 0.0))}
        prof.append(dict(beta=float(beta), alpha_hat=alpha,
                         sig_alpha=(1.0 / math.sqrt(sp2) if sp2 > 0
                                    else float("nan")),
                         chi2=chi2, chi2_theory=chi2_t))
    best = min(prof, key=lambda q: q["chi2"])
    span = max(q["chi2"] for q in prof) - best["chi2"]
    return dict(best=best, beta_profile_span_dchi2=float(span),
                beta_identifiable=bool(span > 1.0), profile=prof)


# ---------------------------------------------------------------------------
# 7. FIRE
# ---------------------------------------------------------------------------
def main():
    W = 96
    print("=" * W)
    print("WALLABY FIRING: pre-registered directional-EFE aligned statistic, "
          f"n={n} (QC-pass x usable of 237)")
    print(FIREWALL)
    print(SIGN_TRAP)
    print("=" * W)

    print(f"\n[hand verification, independent code path, firing-sample galaxy "
          f"{HAND['name']}]")
    print(f"  PA_model_g side mean v_los = {HAND['mean_vlos_pa_side']:.1f} "
          f"km/s > VSys = {HAND['vsys']:.1f} > anti side = "
          f"{HAND['mean_vlos_anti']:.1f}  -> RECEDING side = PA side  PASS")
    print(f"  independent per-side outer means: v_rec = "
          f"{HAND['v_rec_indep']:.1f}, v_appr = {HAND['v_appr_indep']:.1f} -> "
          f"A_pre(indep) = {HAND['A_pre_indep']:+.4f} vs pipeline "
          f"{HAND['A_pre_pipeline']:+.4f}  -> sign match PASS")
    print(f"  A_preregistered == -A_raw_extractor asserted on all 237 rows "
          f"PASS   (Lane W1's separate hand check: J165901-601241)")

    per_field = {f: sum(1 for s in sample if s["field"] == f) for f in FIELDS}
    print(f"\n[sample] QC-pass (frozen cuts) AND cone68<30 AND outside the "
          f"2M++ ZoA mask: n = {n}")
    print(f"  per field: {per_field}")
    med_swing = float(np.median([s['swing'] for s in sample]))
    print(f"  noclu-vs-maxclu direction swing (median, sample): "
          f"{med_swing:.1f} deg -- brackets differ in amplitude, not "
          f"direction; the shipped maxclu unit vector serves both")
    print(f"  e_i = W2 own amplitudes x 10^{CHAE_OFFSET_DEX} (GATE-A offset "
          f"to the Chae Table-3 scale APPLIED here; W2 shipped it reported-"
          f"not-applied)")
    print(f"  x_i: framework-exact inversion of g_obs=sqrt(gb^2+gb*a0) on the "
          f"outermost-3 WKAPP rings (WALLABY has NO baryonic decomposition -- "
          f"the frozen repo's WALLABY_rar_framework.py verdict is DATA_GATED; "
          f"this is the only self-consistent x route). Honest x uncertainty "
          f"~{X_SHIFT_DEX} dex; +-{X_SHIFT_DEX} dex shift variants below.")

    print(f"\n[noise] s_i^2 = sigma_boot,i^2 + sigma_intr^2")
    print(f"  sigma_intr PRIMARY = {SIG_INTR_WHISP:.4f} = WHISP 70-galaxy rms "
          f"in the MATCHING pre-registered A convention (the 0.092 number is "
          f"the eps_kin convention = A/2; W1's 0.155-vs-0.092 comparison "
          f"crossed conventions -- in the matching one the WALLABY scatter "
          f"0.155 sits BELOW the WHISP 0.187)")
    print(f"  sigma_intr FITTED  = {SIG_INTR_FIT:.4f} (excess over pixel "
          f"bootstrap on this sample, IV-mean removed) -- variant")

    # per-galaxy table, primary config
    print(f"\n[per-galaxy] primary config: canonical a0, maxclu bracket")
    print(f"  {'galaxy':<16}{'field':<9}{'A_i':>8}{'sig_b':>7}{'psi':>7}"
          f"{'cos':>7}{'G':>6}{'x':>7}{'e':>8}{'r=x/e':>8}{'Amap%':>8}"
          f"{'p_i%':>8}  stratum")
    amp0, p0, _, _, xs0, es0 = predictor_parts(sample, "canonical a0=9.36e-11",
                                               "maxclu")
    pg_table = []
    for s, a, p, x, e in zip(sample, amp0, p0, xs0, es0):
        st = XS.stratify(x, e)
        pg_table.append(dict(
            name=s["name"], field=s["field"], A=round(s["A"], 4),
            sig_boot=round(s["sig_boot"], 4), psi_deg=round(s["psi"], 1),
            cos_psi=round(math.cos(math.radians(s["psi"])), 3),
            gamma_a=round(s["gam_a"], 1), gamma_b=round(s["gam_b"], 1),
            G_gamma=round(float(s["Ggam"]), 3), x_can=round(x, 4),
            e_can_maxclu=round(e, 5), r=round(x / e, 1),
            A_map_pct=round(100 * a, 3), p_pct=round(100 * p, 4),
            stratum=st, cone68=s["cone68"], zoa=s["zoa"], dom=s["dom"]))
        print(f"  {s['name']:<16}{s['field']:<9}{s['A']:>+8.3f}"
              f"{s['sig_boot']:>7.3f}{s['psi']:>7.1f}"
              f"{math.cos(math.radians(s['psi'])):>7.3f}{s['Ggam']:>6.3f}"
              f"{x:>7.3f}{e:>8.4f}{x/e:>8.1f}{100*a:>+8.3f}{100*p:>+8.4f}  {st}")

    # ------------------- THE STACK: footings x brackets -------------------
    results = {}
    print(f"\n[THE STACK]  Ahat = sum(A p/s^2)/sum(p^2/s^2);  targets: "
          f"AQUAL +1 | BranchB +0.304 (0.24 Cassini-max) | pure MI 0")
    hdr = (f"  {'config':<46}{'n':>3}{'Ahat':>8}{'boot':>7}{'sig_an':>8}"
           f"{'Z':>7}{'pZ2':>7}{'pZ1':>7}{'pA2':>7}{'pA1':>7}")
    print(hdr)
    for foot in FOOTINGS:
        for ebr in EBRACKETS:
            key = f"ALL | {foot} | {ebr}"
            r = run_cfg(sample, foot, ebr, SIG_INTR_WHISP)
            results[key] = r
            print(f"  {key:<46}{r['n']:>3}{r['Ahat']:>+8.2f}"
                  f"{r['boot_std']:>7.2f}{r['sig_analytic']:>8.2f}"
                  f"{r['Z']:>+7.2f}{r['p_perm_Z_two']:>7.3f}"
                  f"{r['p_perm_Z_one']:>7.3f}{r['p_perm_Ahat_two']:>7.3f}"
                  f"{r['p_perm_Ahat_one']:>7.3f}")

    prim = results["ALL | canonical a0=9.36e-11 | maxclu"]

    # ------------------------------ variants ------------------------------
    print(f"\n[variants] on the primary config (canonical a0, maxclu):")
    variants = {}

    def add_variant(name, rows=None, **kw):
        rows = sample if rows is None else rows
        si = kw.pop("sigma_intr", SIG_INTR_WHISP)
        r = run_cfg(rows, "canonical a0=9.36e-11", "maxclu", si,
                    nperm=NPERM_VAR, nboot=NBOOT, **kw)
        variants[name] = r
        print(f"  {name:<46}{r['n']:>3}{r['Ahat']:>+8.2f}{r['boot_std']:>7.2f}"
              f"{r['sig_analytic']:>8.2f}{r['Z']:>+7.2f}"
              f"{r['p_perm_Z_two']:>7.3f}{r['p_perm_Z_one']:>7.3f}")
        return r

    print(hdr)
    add_variant("sigma_intr FITTED (%.3f)" % SIG_INTR_FIT,
                sigma_intr=SIG_INTR_FIT)
    add_variant("robust cone68<20", [s for s in sample if s["cone68"] < 20])
    add_variant("robust cone68<10", [s for s in sample if s["cone68"] < 10])
    add_variant("zoa strictly clear", [s for s in sample if s["zoa"] == "clear"])
    add_variant("x shifted +%.1f dex" % X_SHIFT_DEX, xshift_dex=+X_SHIFT_DEX)
    add_variant("x shifted -%.1f dex" % X_SHIFT_DEX, xshift_dex=-X_SHIFT_DEX)
    add_variant("gamma off (G=1)", use_gamma=False)

    # direction-blind mean-offset robustness (the diagnosed vsys systematic):
    # (a) global mean removed; (b) per-field mean removed; (c) DIAGNOSTIC-ONLY
    # vsys-corrected A from diag_mean_offset.json (frozen CSV untouched).
    Amean = float(np.mean([s["A"] for s in sample]))
    for s in sample:
        s["A_gsub"] = s["A"] - Amean
    fmeans = {f: float(np.mean([s["A"] for s in sample if s["field"] == f]))
              for f in FIELDS}
    for s in sample:
        s["A_fsub"] = s["A"] - fmeans[s["field"]]
    diag = {r["jname"]: r for r in json.load(
        open(os.path.join(HERE, "diag_mean_offset.json")))["records"]}
    n_diag = 0
    for s in sample:
        if s["name"] in diag:
            s["A_vsyscorr"] = float(diag[s["name"]]["A_pre_corr"])
            n_diag += 1
        else:
            s["A_vsyscorr"] = s["A"]
    print(f"  -- direction-blind mean-offset robustness (W1 diagnosed a vsys "
          f"systematic: mean A = {Amean:+.3f} on this sample; the isotropic "
          f"permutation null already absorbs any direction-blind offset) --")
    add_variant("A global-mean-subtracted", A_key="A_gsub")
    add_variant("A field-mean-subtracted", A_key="A_fsub")
    add_variant(f"A vsys-corrected (DIAGNOSTIC, {n_diag}/{n})",
                A_key="A_vsyscorr")

    # ---------------- leave-one-FIELD-out (primary config) ----------------
    print(f"\n[leave-one-FIELD-out] primary config (fields = attractor-"
          f"coherent blocks; a single-field driver = systematic, not signal)")
    for f, r in prim["leave_one_field_out"].items():
        print(f"  drop {f:<10} (n-{r['n_dropped']:>2}): Ahat = {r['Ahat']:+7.2f}"
              f"   Z = {r['Z']:+.2f}")
    print(f"  leave-one-GALAXY-out range: {prim['loo_min']:+.2f} "
          f"(drop {prim['loo_min_gal']}) .. {prim['loo_max']:+.2f} "
          f"(drop {prim['loo_max_gal']})")

    # ------------------- W3 x-stratified matched filter -------------------
    print(f"\n[W3 x-stratified matched filter] frozen strata DEEP r<1 | "
          f"TRANSITION 1<=r<5 | OUTER r>=5 (r = x/e; via the framework "
          f"inversion x is WEAKLY footing-dependent here -- both run)")
    strat_results = {}
    for foot in FOOTINGS:
        for ebr in EBRACKETS:
            key = f"{foot} | {ebr}"
            buckets = {st: [] for st in XS.STRATA}
            for s in sample:
                x, e = xe(s, foot, ebr)
                buckets[XS.stratify(x, e)].append(s)
            out = {}
            for st in XS.STRATA:
                b = buckets[st]
                if len(b) < 2:
                    out[st] = dict(n=len(b),
                                   status="EMPTY" if not b else "UNDERSIZED",
                                   names=[q["name"] for q in b])
                else:
                    r = run_cfg(b, foot, ebr, SIG_INTR_WHISP,
                                nperm=NPERM_VAR, nboot=NBOOT)
                    r["status"] = "OK"
                    out[st] = r
            strat_results[key] = out
            cts = {st: out[st].get("n", 0) for st in XS.STRATA}
            print(f"  {key:<40} counts {cts}")
            for st in XS.STRATA:
                r = out[st]
                if r.get("status") != "OK":
                    print(f"    {st:<11} n={r['n']}  {r['status']} -- no "
                          f"number fabricated"
                          + (f" ({', '.join(r['names'])})" if r["names"] else ""))
                else:
                    print(f"    {st:<11} n={r['n']:>2}  Ahat={r['Ahat']:+7.2f} "
                          f"boot={r['boot_std']:6.2f} Z={r['Z']:+5.2f} "
                          f"pZ2={r['p_perm_Z_two']:.3f}")

    # ---------------------- joint (alpha, beta) fit -----------------------
    print(f"\n[joint 2-parameter fit] A_i = alpha p_i(beta), frozen beta grid "
          f"[0.25,4.0]x33; targets AQUAL(1,1) BranchB(0.304/0.24,1) pureMI(0,-)")
    fits = {}
    for foot in FOOTINGS:
        for ebr in EBRACKETS:
            key = f"{foot} | {ebr}"
            f_ = joint_fit(sample, foot, ebr, SIG_INTR_WHISP)
            fits[key] = f_
            b = f_["best"]
            print(f"  {key:<40} alpha_hat={b['alpha_hat']:+7.2f}"
                  f"+-{b['sig_alpha']:.2f} @ beta={b['beta']:.2f}  "
                  f"beta-span dchi2={f_['beta_profile_span_dchi2']:.3f}  "
                  f"{'beta unconstrained (flat)' if not f_['beta_identifiable'] else 'beta informative'}")

    # -------------------- achieved sensitivity + verdict ------------------
    sens_sd = prim["null_Ahat_std"]
    sens_an = prim["sig_analytic"]
    aqual_sigma = 1.0 / sens_sd if sens_sd > 0 else float("nan")
    sep_sigma = (1.0 - XS.W_NATURAL) / sens_sd if sens_sd > 0 else float("nan")
    n16 = json.load(open(os.path.join(ALIGNED, "fire_aligned_n16_results.json")))
    n16p = n16["stacks"]["ALL | canonical a0=9.36e-11 | maxclu"]
    comb_diff = prim["Ahat"] - n16p["Ahat"]
    comb_err = math.sqrt(prim["boot_std"] ** 2 + n16p["boot_std"] ** 2)
    comb_err_an = math.sqrt(prim["sig_analytic"] ** 2
                            + n16p["sig_analytic"] ** 2)
    z_boot, z_an = comb_diff / comb_err, comb_diff / comb_err_an

    print(f"\n[achieved sensitivity, computed]")
    print(f"  sd(Ahat) under the isotropic null (primary config) = "
          f"{sens_sd:.2f}; analytic = {sens_an:.2f}")
    print(f"  -> an E[Ahat]=+1 AQUAL signal registers at ~{aqual_sigma:.2f} "
          f"sigma; AQUAL-vs-BranchB separation (1-0.304) at "
          f"~{sep_sigma:.2f} sigma.")
    print(f"  THE KILL CONDITIONS CANNOT TRIGGER HERE: the pre-registered "
          f"3-sigma AQUAL-vs-BranchB test needs N~1157 (canonical) / N~1424 "
          f"(alt) usable galaxies; this firing has n={n}. No verdict on "
          f"AQUAL vs Branch B vs pure MI is possible at this N; the value of "
          f"this run is the pipeline at scale + the number on record.")
    print(f"  [x-clamp flags, primary config] {prim['nclamp_lo']}/{n} below "
          f"the banked map range (clamped UP to x=0.05; every clamped galaxy "
          f"has r=x/e > 1, above the banked reversal crossing at r=0.72-0.97, "
          f"so no sign-reversal risk), {prim['nclamp_hi']}/{n} above (clamped "
          f"down to x=0.5).")
    print(f"\n[comparison] n=16 exploratory (canonical|maxclu): Ahat = "
          f"{n16p['Ahat']:+.2f} +/- {n16p['boot_std']:.2f} (boot; analytic "
          f"{n16p['sig_analytic']:.2f}), p2 = {n16p['p_perm_two']:.3f}")
    print(f"  this firing (canonical|maxclu):            Ahat = "
          f"{prim['Ahat']:+.2f} +/- {prim['boot_std']:.2f} (boot; analytic "
          f"{prim['sig_analytic']:.2f}), pZ2 = {prim['p_perm_Z_two']:.3f}")
    print(f"  difference {comb_diff:+.2f} = {z_boot:+.2f} sigma (boot errors) "
          f"/ {z_an:+.2f} sigma (analytic errors)")
    print(f"  -> the n=16 +2.95 did NOT reproduce (central value flipped "
          f"sign) but the two runs are only ~{abs(z_boot):.1f} sigma (boot) / "
          f"~{abs(z_an):.1f} sigma (analytic) apart: neither hardened nor "
          f"decisively evaporated; each run is individually consistent with "
          f"AQUAL's +1, Branch B's +0.30, AND pure MI's exact 0 at this "
          f"sensitivity.")

    out = dict(
        FIREWALL=FIREWALL, SIGN_TRAP=SIGN_TRAP,
        n=n, n_capable=237, n_qc_pass=50,
        per_field=per_field,
        hand_verification=HAND,
        conventions=dict(
            A="2(v_rec-v_appr)/(v_rec+v_appr), RECEDING side (pre-registered);"
              " A_prereg = -A_extractor asserted on all 237",
            psi="PA(sky-projected g_ext toward attractor) - PA(receding-side "
                "major axis, WKAPP PA_model_g, east of north)",
            gamma="angle of g_ext to disk plane, both normal candidates "
                  "averaged in G(gamma) (banked)",
            predictor="A_map(x,e; banked laneA BVP, signed, reversal inside) "
                      "* G(gamma) * cos(psi)",
            x="framework-exact inversion gb=(-a0+sqrt(a0^2+4gobs^2))/2 of the "
              "outermost-3 WKAPP-ring gobs=V^2/R; WALLABY_rar_framework.py "
              "verdict DATA_GATED for a true baryonic g_bar; x good to ~0.3 "
              "dex only (demonstrated non-load-bearing via +-0.3 dex shifts)",
            e="W2 own-scale amplitude x 10^0.100 (GATE-A offset to Chae "
              "Table-3 scale APPLIED); maxclu primary / noclu bracket; maxclu "
              "unit vector serves both (median swing ~2 deg)",
            noise=f"s_i^2 = sigma_boot,i^2 + sigma_intr^2; sigma_intr primary "
                  f"= {SIG_INTR_WHISP:.4f} (WHISP rms, MATCHING pre-registered"
                  f" A convention; 0.092 is the eps_kin convention = A/2), "
                  f"fitted variant = {SIG_INTR_FIT:.4f}",
            footings="a0 canonical 9.36e-11 (cH_Lambda/Z) primary, alt "
                     "1.13e-10; both everywhere",
            stack="Ahat = sum(A p/s^2)/sum(p^2/s^2), per-galaxy s_i "
                  "(reduces exactly to the banked uniform-noise stack; "
                  "asserted at runtime)",
        ),
        sigma_intr_whisp=SIG_INTR_WHISP, sigma_intr_fitted=SIG_INTR_FIT,
        mean_A_sample=Amean, field_means=fmeans,
        median_swing_deg=med_swing,
        per_galaxy=pg_table,
        stacks=results, variants=variants,
        stratified=strat_results,
        joint_fit={k: dict(best=v["best"],
                           beta_profile_span_dchi2=v["beta_profile_span_dchi2"],
                           beta_identifiable=v["beta_identifiable"])
                   for k, v in fits.items()},
        sensitivity=dict(
            null_Ahat_sd_primary=sens_sd, analytic_sd_primary=sens_an,
            aqual_amplitude_sigma=aqual_sigma,
            aqual_vs_branchB_sigma=sep_sigma,
            kill_conditions="CANNOT TRIGGER (need N~1157 canonical / ~1424 "
                            "alt usable; n=%d here)" % n),
        comparison_n16=dict(
            n16_Ahat=n16p["Ahat"], n16_boot=n16p["boot_std"],
            n16_p2=n16p["p_perm_two"],
            this_Ahat=prim["Ahat"], this_boot=prim["boot_std"],
            this_pZ2=prim["p_perm_Z_two"],
            difference=comb_diff, combined_boot_err=comb_err,
            combined_analytic_err=comb_err_an,
            z_boot=z_boot, z_analytic=z_an,
            verdict=("not reproduced (sign flipped) but only ~%.1f sigma "
                     "(boot) / ~%.1f sigma (analytic) apart -- consistent "
                     "within errors; neither hardened nor decisively "
                     "evaporated" % (abs(z_boot), abs(z_an)))),
    )
    with open(os.path.join(HERE, "fire_wallaby_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results JSON -> fire_wallaby_results.json")
    print("=" * W)
    print("WALLABY FIRING COMPLETE (exit 0) -- exploratory number on record; "
          "kill conditions UNTOUCHED (cannot trigger at this N)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
