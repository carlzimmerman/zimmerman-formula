#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
HZQ shared machinery for the owner-routed high-z implied-a0 lanes (CFG274 and later).  Nothing in this module is a result: it holds the programme's
estimator (CFG223's median-residual s*, imported read-only from CFG229's a0implied), CFG229's disc functions, CFG229's split-normal draw, the baryon-shift
bands, the distance-to-floor diagnostics and the writer of the chart-shaped points file.  kappa = 1/2 is FITTED; no verdict words.
"""
import os, sys, math, json, zlib, csv, hashlib, io, contextlib
import numpy as np
from scipy.integrate import quad
from scipy.special import i0e, i1e, k0e, k1e

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
for _p in (CFG, os.path.join(CFG, "CFG229_class_m_gold")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import a0implied as AI                                               # CFG223's estimator, verbatim (CFG229's copy)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as K4

NU, NUP2 = K4.nu_mono, K4.nu_p2
A0C, A0A = 9.3603e-11, 1.1312e-10
FLOOR = 0.001
LOG_FLOOR = -3.0
G_KPC = 4.30091e-6                                                   # kpc (km/s)^2 / Msun
XN = 1.678
OM = 0.315
G2SI = 1e6 / 3.0856775814913673e19                                   # (km/s)^2/kpc -> m s^-2
LOGHE = math.log10(1.36)
CHART_HEADER = ["lane", "object", "gas_class", "z", "z_shown", "no_root", "s_star", "a0_1e-10_m_s2", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi",
                "inner_lo", "inner_hi", "inner_noroot_corner", "outer_lo", "outer_hi", "outer_noroot_corner"]
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))["curves"]
LAWS = {"FLAT": lambda z: 1.0, "H(z)": lambda z: float(np.interp(z, J223["z"], J223["H(z)"])), "PROXY": lambda z: float(np.interp(z, J223["z"], J223["PROXY"]))}


def kpc_per_arcsec(z, H0=67.4, Om=OM):
    c = 299792.458
    dc = c / H0 * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0]            # Mpc
    return dc / (1 + z) * 1e3 * math.pi / 648000.0


def disc_v2(M, Re, Rr):                                              # thin exponential (Freeman) disc, (km/s)^2; Re, Rr in kpc  (CFG229)
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def gdisc(M, Re, Rr):                                                # m s^-2
    return disc_v2(M, Re, Rr) / Rr * G2SI


def gsph(M, Re, Rr):                                                 # m s^-2, the enclosed exponential-disc mass as a point mass
    x = Rr / (Re / XN)
    return G_KPC * M * (1 - (1 + x) * np.exp(-x)) / Rr ** 2 * G2SI


def split_normal(rng, v, ehi, elo, size):
    g = rng.normal(size=size)
    return v + np.where(g > 0, g * ehi, g * elo)


def seed_of(label):
    return zlib.crc32(label.encode()) % 100000


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest()[:16]


# ------------------------------------------------------------------ the estimator
def s_star(D, gb, nu=NU, a0=A0C):
    """(log10 s*, no_root) for one set of rows (n,): CFG223's median-residual root."""
    ls, unb = AI.implied(np.asarray(D, float), np.asarray(gb, float), nu, a0)
    return float(ls[0]), bool(unb[0])


def s_val(ls, unb):
    return FLOOR if unb else 10 ** ls


def s_status(D, gb, nu=NU, a0=A0C):
    """(log10 s*, status): 'root' (inside the solver bracket log10 s in [-3, +3]), 'floor' (no root, the median D <= 1: the baryons exceed the dynamics) or
    'ceiling' (no root because the median D > 1 puts s* above 1000: a vacuous upper bound).  Added after CFG273, where the bracket mislabelled two ceiling rows 'no root'."""
    ls, unb = s_star(D, gb, nu, a0)
    if not unb:
        return ls, "root"
    return ls, ("floor" if float(np.median(np.asarray(D, float))) <= 1.0 else "ceiling")


def s_val_status(ls, status):
    return {"root": 10 ** ls, "floor": FLOOR, "ceiling": 1000.0}[status]


def lever1(D, gb, nu=NU, a0=A0C):
    lv, fl = AI.lever(np.asarray(D, float), np.asarray(gb, float), nu, a0)
    return (float("nan") if bool(fl[0]) else float(lv[0])), bool(fl[0])


def band_solutions(D, gb, shifts=(-0.30, -0.15, 0.15, 0.30), nu=NU, a0=A0C):
    """all baryon masses x 10^shift at fixed g_obs (g_bar x 10^shift, D x 10^-shift): {shift: (log10 s*, no_root)}."""
    return {sh: s_star(np.asarray(D) * 10 ** (-sh), np.asarray(gb) * 10 ** sh, nu, a0) for sh in shifts}


def band_edges(bands, lo_key, hi_key):
    """(lo, hi, noroot_corner) in s units from the two shift solutions; a no-root corner is set to the floor (s = 0.001) for the lower edge of the band."""
    vals = [s_val(*bands[k]) for k in (lo_key, hi_key)]
    nr = int(bands[lo_key][1] or bands[hi_key][1])
    return min(vals), max(vals), nr


def delta_floor(D):
    """log10 median D of the set (> 0: the baryons could rise by that many dex before the root disappears; < 0: they would have to fall)."""
    return float(np.log10(np.median(np.asarray(D, float))))


def shift_to_s1(D, gb, lo=-3.0, hi=3.0, step=0.01, nu=NU, a0=A0C):
    """the baryon shift (dex) at which s* = 1, by a scan and linear interpolation; nan if there is none in [lo, hi]."""
    xs = np.arange(lo, hi + 1e-9, step)
    ys = []
    for x in xs:
        ls, unb = s_star(np.asarray(D) * 10 ** (-x), np.asarray(gb) * 10 ** x, nu, a0)
        ys.append(float("nan") if unb else ls)
    ys = np.array(ys)
    for i in range(len(xs) - 1):
        if np.isfinite(ys[i]) and np.isfinite(ys[i + 1]) and (ys[i] > 0) != (ys[i + 1] > 0):
            return float(xs[i] + (0 - ys[i]) * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i]))
    return float("nan")


def rooted_pct(ls, unb, q=(2.5, 16, 50, 84, 97.5)):
    ok = ~np.asarray(unb)
    if ok.sum() < 20:
        return [float("nan")] * len(q), float(np.mean(unb))
    return [float(v) for v in np.percentile(np.asarray(ls)[ok], q)], float(np.mean(unb))


def flags_for(z, lo95, hi95, band_in, band_out, has_root):
    """three letters per law: in the 95 % interval / in its hull with the inner band / with the outer band; 'na' when the row has no root."""
    out = {}
    for L, fn in LAWS.items():
        if not has_root:
            out[L] = "na"; continue
        sL = fn(z)
        out[L] = "".join("Y" if lo <= sL <= hi else "n" for lo, hi in ((lo95, hi95), (min(lo95, band_in[0]), max(hi95, band_in[1])), (min(lo95, band_out[0]), max(hi95, band_out[1]))))
    return out


def write_points(path, cols, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow(r)


def chart_header_check():
    ref = os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv")
    return open(ref).readline().strip().split(",") == CHART_HEADER


def jc(o):
    if isinstance(o, dict): return {(k if isinstance(k, str) else str(k)): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jc(v) for v in o]
    if isinstance(o, np.ndarray): return jc(o.tolist())
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
