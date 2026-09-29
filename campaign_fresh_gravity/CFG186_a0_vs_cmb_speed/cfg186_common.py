#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cfg186_common -- shared machinery for lane CFG186 (does SPARC's acceleration scale depend on a galaxy's speed through
the CMB frame?  door 11C, gate G7).  Nothing here is a result.  It holds:

  * the run harness (tee to this lane's own .out, named checks with a load-bearing flag, results JSON, outputs named by
    mode: MUTATE=1 writes *_MUTATE.*) -- adapted from CFG182's harness (copied, not imported);
  * the SPARC loader (CFG4_common.load_sparc, read-only import) and the kernel nu_mono (FP1's committed definition,
    exec'd read-only through CFG4_common);
  * sky positions (VizieR J/AJ/152/157 table 1 -> Galactic, astropy) and heliocentric velocities from four on-disk
    sources (NED via sparc_cosmicweb_match.csv, UNGC, Kourkchi & Tully 2017, 2MRS), matched by position;
  * the CMB-frame conversion and the line-of-sight peculiar velocity u(D) = c (z_CMB - z_cos(D)) / (1 + z_cos(D));
  * the per-galaxy 2D PROFILE likelihood C_i(x = log10 a0, t = (D - D_SPARC)/e_D): Upsilon_disk, Upsilon_bul and the
    inclination profiled at every cell (CFG182's nuisance model with the distance held on a grid instead of profiled);
  * the curve machinery and the global fit  F(L, beta, ...) = sum_i q_i min_t C_i(L + log10(1 + beta z_i(t)) + ..., t)/s_i.

kappa = 1/2 stays FITTED; a0 is fitted in this lane (a0_bar free).  Run nothing from here directly.
"""
import os
import sys
import json
import math
import time
import builtins

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.optimize import least_squares, minimize
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("MUTATE", "0") == "1"
sys.path.insert(0, CFGDIR)
import CFG4_common as C4                                     # read-only: loader + nu_mono (nothing written on import)

# ------------------------------------------------------------------------------------------------ declared constants
C_KMS = 299792.458
KPC_M = 3.0857e19
LN10 = math.log(10.0)
V_SUN, L_SUN, B_SUN = 369.8, 264.0, 48.3                     # solar motion w.r.t. the CMB (Planck 2018, rounded; declared)
V_LG, L_LG, B_LG = 627.0, 276.0, 30.0                        # LG motion w.r.t. the CMB (Kogut+1993; FROM MEMORY, UNVERIFIED)
V_SLG, L_SLG, B_SLG = 318.0, 106.0, -6.0                     # Sun w.r.t. the LG (Tully+2008; FROM MEMORY, consistency print only)
H0_PRIMARY, H0_VARIANT = 67.66, 73.0
OMEGA_M = 0.311
W_REF = 600.0                                                # km/s; beta = 0.10 is the G7 line
BETA_G7 = 0.10
BETA_MUT = 0.30                                              # MUTATE injection
A0_REF = 1.2e-10                                             # MUTATE injection reference only (declared)
UPS_D0, UPS_B0, UPS_SIG = 0.5, 0.7, 0.1                      # LML 2018 priors (log-normal, 0.1 dex)
XGRID = np.round(np.arange(-11.30, -8.9999, 0.02), 2)        # log10 a0 grid of the profile curves (116)
TGRID = np.round(np.arange(-4.0, 4.0001, 0.25), 2)           # (D - D_SPARC)/e_D coarse grid (33)
TFINE = np.round(np.arange(-4.0, 4.0001, 0.05), 2)           # fine grid for the fit (161)
D_FLOOR = 0.3                                                # D >= 0.3 D_SPARC
BIG = 1.0e6                                                  # value of masked (infeasible) cells
KM1_COEF = 2.0 * W_REF ** 2 / (3.0 * C_KMS ** 2)             # beta = KM1_COEF / eps  (KM1 C7, sphere average D/3)


# ------------------------------------------------------------------------------------------------ harness
class Run:
    def __init__(self, slug):
        self.slug = slug
        self.mutate = MUTATE
        suf = "_MUTATE" if MUTATE else ""
        self.suf = suf
        self.out_path = os.path.join(HERE, f"{slug}{suf}.out")
        self.json_path = os.path.join(HERE, f"{slug}_results{suf}.json")
        self._f = builtins.open(self.out_path, "w", encoding="utf-8")
        self._stdout = sys.stdout
        sys.stdout = self
        self.t0 = time.time()
        self.OUT = {"lane": "CFG186", "script": slug, "mutate": MUTATE, "checks": {}, "numbers": {}}
        self.CH = []

    def write(self, t):
        self._stdout.write(t)
        self._f.write(t)

    def flush(self):
        self._stdout.flush()
        self._f.flush()

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def check(self, name, measured, ok, load_bearing=True, reading=""):
        ok = bool(ok)
        key = name.split()[0]
        k2, j = key, 1
        while k2 in self.OUT["checks"]:
            j += 1
            k2 = f"{key}#{j}"
        self.CH.append((k2, ok, load_bearing))
        self.OUT["checks"][k2] = {"ok": ok, "load_bearing": load_bearing, "measured": str(measured), "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def num(self, key, value):
        self.OUT["numbers"][key] = jclean(value)
        return value

    def finish(self):
        npass = sum(1 for _, ok, _ in self.CH if ok)
        nlb = sum(1 for _, ok, lb in self.CH if (not ok) and lb)
        self.OUT["summary"] = {"n_checks": len(self.CH), "n_pass": npass, "load_bearing_failures": nlb,
                               "failed": [k for k, ok, _ in self.CH if not ok], "seconds": round(time.time() - self.t0, 1)}
        with builtins.open(self.json_path, "w", encoding="utf-8") as fh:
            json.dump(jclean(self.OUT), fh, indent=1)
        self.P(f"\n  {npass}/{len(self.CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(self.json_path)} "
               f"({time.time() - self.t0:.0f} s)")
        rc = 1 if nlb else 0
        self.P(f"rc = {rc}")
        sys.stdout = self._stdout
        self._f.close()
        return rc


def jclean(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else str(k)): jclean(v) for k, v in o.items()}
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


# ------------------------------------------------------------------------------------------------ geometry
def unitvec(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.stack([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)], axis=-1)


def lb_of(v):
    v = np.asarray(v, float)
    v = v / np.linalg.norm(v)
    return float(np.degrees(np.arctan2(v[1], v[0])) % 360.0), float(np.degrees(np.arcsin(np.clip(v[2], -1, 1))))


def angle_deg(u, v):
    u = np.asarray(u, float) / np.linalg.norm(u)
    v = np.asarray(v, float) / np.linalg.norm(v)
    return float(np.degrees(np.arccos(np.clip(u @ v, -1, 1))))


VEC_SUN = V_SUN * unitvec(L_SUN, B_SUN)
VEC_LG = V_LG * unitvec(L_LG, B_LG)


# ------------------------------------------------------------------------------------------------ data
def _vizier_rows(path):
    """generic VizieR ASU-TSV reader: header line, units line, dashes line, then rows (tab-separated)."""
    rows, header, seen_dash = [], None, False
    for line in builtins.open(path, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip():
            continue
        tok = line.rstrip("\n").split("\t")
        if header is None:
            header = [t.strip() for t in tok]
            continue
        if not seen_dash:
            if set(line.strip().replace("\t", "")) <= set("-"):
                seen_dash = True
            continue
        if tok[0].strip() == header[0]:                      # a further table in the same file: new header
            header, seen_dash = [t.strip() for t in tok], False
            continue
        rows.append({h: (tok[k].strip() if k < len(tok) else "") for k, h in enumerate(header)})
    return rows


def load_positions():
    """VizieR J/AJ/152/157 table 1 (J2000) -> name -> (ra, dec, l, b), Galactic with astropy."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    rows = {}
    for r in _vizier_rows(os.path.join(DATA, "sparc_lelli2016_table1_pos.tsv")):
        try:
            rows[r["Name"]] = (float(r["_RAJ2000"]), float(r["_DEJ2000"]))
        except (ValueError, KeyError):
            continue
    names = list(rows)
    ra = np.array([rows[n][0] for n in names])
    de = np.array([rows[n][1] for n in names])
    g = SkyCoord(ra=ra * u.deg, dec=de * u.deg, frame="fk5", equinox="J2000").galactic
    return {n: (ra[i], de[i], float(g.l.deg[i]), float(g.b.deg[i])) for i, n in enumerate(names)}


def _radec_vec(ra, de):
    ra, de = np.radians(np.asarray(ra, float)), np.radians(np.asarray(de, float))
    return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], axis=-1)


def _match(ra0, de0, ra, de, vals, rmax_arcmin=1.5):
    """nearest catalogue entry within rmax of each target; returns (value or nan, separation arcmin)."""
    t = _radec_vec(ra0, de0)
    c = _radec_vec(ra, de)
    out, sep = np.full(len(ra0), np.nan), np.full(len(ra0), np.nan)
    for i in range(len(ra0)):
        with np.errstate(all="ignore"):                      # numpy 1.26 + Accelerate: spurious FP flags in matmul
            d = c @ t[i]
        j = int(np.argmax(d))
        s = math.degrees(math.acos(min(1.0, float(d[j])))) * 60.0
        if s <= rmax_arcmin:
            out[i], sep[i] = vals[j], s
    return out, sep


def load_velocities(names, ra0, de0):
    """heliocentric velocities (km/s) from four on-disk sources, matched by name (NED table) or position (<= 1.5').
    Returns dict: name -> {'NED':v, 'UNGC':v, 'KT17':v, '2MRS':v}, plus a diagnostics dict."""
    import csv
    src = {n: {} for n in names}
    with builtins.open(os.path.join(DATA, "sparc_cosmicweb_match.csv")) as fh:
        for r in csv.DictReader(fh):
            if r["name"] in src and r["cz_kms"].strip():
                src[r["name"]]["NED"] = float(r["cz_kms"])
    diag = {}
    # UNGC (Karachentsev+2013): HRV heliocentric
    U = [r for r in _vizier_rows(os.path.join(DATA, "ungc_karachentsev2013.tsv")) if r.get("HRV", "").strip()]
    ura = np.array([float(r["_RAJ2000"]) for r in U])
    ude = np.array([float(r["_DEJ2000"]) for r in U])
    uv = np.array([float(r["HRV"]) for r in U])
    v, s = _match(ra0, de0, ura, ude, uv)
    for i, n in enumerate(names):
        if np.isfinite(v[i]):
            src[n]["UNGC"] = float(v[i])
    diag["UNGC_rows"] = len(U)
    # Kourkchi & Tully 2017: HRV (per galaxy only if group members carry distinct values)
    K = [r for r in _vizier_rows(os.path.join(DATA, "kt2017_galaxies.tsv")) if r.get("HRV", "").strip()]
    K = [r for r in K if float(r["HRV"]) > -999]
    kg = {}
    for r in K:
        kg.setdefault(r["PGC1"], []).append(float(r["HRV"]))
    multi = [vals for vals in kg.values() if len(vals) >= 2]
    distinct = sum(1 for vals in multi if len(set(vals)) > 1)
    frac = distinct / max(len(multi), 1)
    diag["KT17_groups_multi"] = len(multi)
    diag["KT17_groups_distinct_frac"] = frac
    diag["KT17_used"] = bool(frac > 0.5)
    if frac > 0.5:
        kra = np.array([float(r["RAJ2000"]) for r in K])
        kde = np.array([float(r["DEJ2000"]) for r in K])
        kv = np.array([float(r["HRV"]) for r in K])
        v, s = _match(ra0, de0, kra, kde, kv)
        for i, n in enumerate(names):
            if np.isfinite(v[i]):
                src[n]["KT17"] = float(v[i])
    # 2MRS (Huchra+2012): cz heliocentric
    M = _vizier_rows(os.path.join(DATA, "2mrs_huchra2012.tsv"))
    M = [r for r in M if r.get("cz", "").strip()]
    mra = np.array([float(r["RAJ2000"]) for r in M])
    mde = np.array([float(r["DEJ2000"]) for r in M])
    mv = np.array([float(r["cz"]) for r in M])
    v, s = _match(ra0, de0, mra, mde, mv)
    for i, n in enumerate(names):
        if np.isfinite(v[i]):
            src[n]["2MRS"] = float(v[i])
    return src, diag


SRC_ORDER = ("NED", "UNGC", "KT17", "2MRS")


def pick_velocity(s):
    for k in SRC_ORDER:
        if k in s:
            return s[k], k
    return float("nan"), ""


def load_galaxies():
    """SPARC curves + master table + positions + velocities; usable points and flags (no selection applied)."""
    gal = C4.load_sparc()
    pos = load_positions()
    out = []
    for g in gal:
        m = g["meta"]
        if m is None or g["name"] not in pos:
            continue
        R, V, eV, Vg, Vd, Vb = g["R"], g["Vobs"], g["eV"], g["Vgas"], g["Vdisk"], g["Vbul"]
        Vbar2_fid = Vg * np.abs(Vg) + UPS_D0 * Vd ** 2 + UPS_B0 * Vb ** 2
        ok = (V > 0) & (eV > 0) & (R > 0) & (Vbar2_fid > 0) & np.isfinite(V + eV + Vbar2_fid)
        ra, de, l, b = pos[g["name"]]
        out.append(dict(name=g["name"], R=R[ok], V=V[ok], eV=eV[ok], Vg=Vg[ok], Vd=Vd[ok], Vb=Vb[ok], npt=int(ok.sum()),
                        D=m["D"], eD=m["eD"], fD=m["fD"], Inc=m["Inc"], eInc=m["eInc"], Q=m["Q"], ra=ra, dec=de, l=l, b=b,
                        n=unitvec(l, b), clean=bool(m["Q"] <= 2 and m["Inc"] >= 30.0 and ok.sum() >= 5),
                        has_bul=bool(np.any(Vb[ok] > 0))))
    names = [g["name"] for g in out]
    src, diag = load_velocities(names, np.array([g["ra"] for g in out]), np.array([g["dec"] for g in out]))
    for g in out:
        g["vsrc"] = src[g["name"]]
        g["cz_hel"], g["cz_src"] = pick_velocity(src[g["name"]])
    return out, diag


# ------------------------------------------------------------------------------------------------ velocities
_ZTAB = np.linspace(0.0, 0.25, 25001)


def _dl_table(H0):
    E = np.sqrt(OMEGA_M * (1 + _ZTAB) ** 3 + 1 - OMEGA_M)
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(_ZTAB))])
    return (1 + _ZTAB) * (C_KMS / H0) * integ


_DL = {}


def z_cos(D, H0):
    """cosmological redshift for luminosity distance D (Mpc), flat LCDM (Omega_m = 0.311), low-z table."""
    if H0 not in _DL:
        _DL[H0] = _dl_table(H0)
    return np.interp(np.asarray(D, float), _DL[H0], _ZTAB)


def z_cmb(cz_hel, nvec):
    """heliocentric -> CMB frame: 1 + z_CMB = (1 + z_hel) / (1 - v_sun.n/c)."""
    return (1 + np.asarray(cz_hel, float) / C_KMS) / (1 - (np.asarray(nvec) @ VEC_SUN) / C_KMS) - 1


def u_los(cz_hel, nvec, D, H0):
    """line-of-sight CMB-frame peculiar velocity (km/s) of ONE galaxy at distance(s) D (Mpc): c (z_CMB - z_cos)/(1 + z_cos)."""
    zc = z_cos(np.maximum(D, 1e-3), H0)
    return C_KMS * (float(z_cmb(cz_hel, nvec)) - zc) / (1 + zc)


def u_matrix(gals, H0, tgrid=TFINE):
    """U[i, k] = u_i(D_i + e_D,i t_k) for a list of galaxies (km/s)."""
    return np.array([u_los(g["cz_hel"], g["n"], g["D"] + g["eD"] * np.asarray(tgrid), H0) for g in gals])


def vperp2_lg(nvec):
    """|V_LG|^2 - (V_LG.n)^2: the transverse part of the LG's motion seen along n (W2 proxy)."""
    nvec = np.asarray(nvec, float)
    return V_LG ** 2 - (nvec @ VEC_LG) ** 2


# ------------------------------------------------------------------------------------------------ the per-galaxy 2D profile
def dlnnu_dlny(nuf, y, h=1e-4):
    return (np.log(nuf(y * math.exp(h))) - np.log(nuf(y * math.exp(-h)))) / (2 * h)


def _model(p, g, a0, nuf, rD):
    ud, ub, ti = p
    Yd = UPS_D0 * 10 ** (UPS_SIG * ud)
    Yb = UPS_B0 * 10 ** (UPS_SIG * ub)
    S = g["Vg"] * np.abs(g["Vg"]) + Yd * g["Vd"] ** 2 + Yb * g["Vb"] ** 2
    S = np.maximum(S, 1e-6)
    k = 1e6 / (g["R"] * KPC_M)
    y = S * k / a0
    nu = nuf(y)
    F = nu * S
    inc0 = math.radians(g["Inc"])
    inc1 = math.radians(g["Inc"] + g["eInc"] * ti)
    si = math.sin(inc1) / math.sin(inc0)
    V = np.sqrt(F * rD) * si
    return V, S, y, nu, F, inc1, Yd, Yb


def _resid(p, g, a0, nuf, V_obs, rD):
    V = _model(p, g, a0, nuf, rD)[0]
    return np.concatenate([(V_obs - V) / g["eV"], p])


def _jac(p, g, a0, nuf, V_obs, rD):
    V, S, y, nu, F, inc1, Yd, Yb = _model(p, g, a0, nuf, rD)
    dlog = dlnnu_dlny(nuf, y)
    dFdS = nu * (1.0 + dlog)
    fac = V / (2.0 * F) * dFdS
    J = np.zeros((len(V) + 3, 3))
    J[:len(V), 0] = -fac * g["Vd"] ** 2 * Yd * UPS_SIG * LN10 / g["eV"]
    J[:len(V), 1] = -fac * g["Vb"] ** 2 * Yb * UPS_SIG * LN10 / g["eV"]
    J[:len(V), 2] = -V * (math.cos(inc1) / math.sin(inc1)) * math.radians(g["eInc"]) / g["eV"]
    J[len(V):, :] = np.eye(3)
    return J


def _bounds(g):
    ilo = max(g["Inc"] - 8 * g["eInc"], 5.0)
    ihi = min(g["Inc"] + 8 * g["eInc"], 90.0)
    if g["eInc"] > 0:
        tilo, tihi = (ilo - g["Inc"]) / g["eInc"], (ihi - g["Inc"]) / g["eInc"]
    else:
        tilo, tihi = -1e-9, 1e-9
    return np.array([-10.0, -10.0, min(tilo, -1e-9)]), np.array([10.0, 10.0, max(tihi, 1e-9)])


def feasible_t(g, tgrid=TGRID):
    return g["D"] + g["eD"] * np.asarray(tgrid) >= D_FLOOR * g["D"]


def _ls(p0, g, a0, nuf, V_obs, rD, lo, hi):
    return least_squares(_resid, np.clip(p0, lo + 1e-9, hi - 1e-9), jac=_jac, bounds=(lo, hi),
                         args=(g, a0, nuf, V_obs, rD), method="trf", xtol=1e-10, ftol=1e-10, gtol=1e-10, max_nfev=200)


def profile_galaxy_2d(args):
    """C(t, x) = min over (Upsilon_d, Upsilon_b, inclination) of chi2_vel + priors, plus the distance prior t^2.
    Warm starts: along x outward from log a0 = -9.92, and across t from the neighbouring t's anchor solution."""
    g, V_obs = args
    nuf = C4.nu_mono
    V_obs = g["V"] if V_obs is None else V_obs
    lo, hi = _bounds(g)
    T, G = len(TGRID), len(XGRID)
    chi = np.full((T, G), np.nan)
    par = np.full((T, G, 3), np.nan)
    feas = feasible_t(g)
    j0 = int(np.argmin(np.abs(XGRID - (-9.92))))
    k0 = int(np.argmin(np.abs(TGRID)))
    anchor = {}
    for kseq in (list(range(k0, T)), list(range(k0 - 1, -1, -1))):
        prev = None if kseq[0] == k0 else anchor.get(k0)
        for k in kseq:
            if not feas[k]:
                continue
            rD = 1.0 + (g["eD"] / g["D"]) * TGRID[k]
            a0 = 10 ** XGRID[j0]
            best = None
            for p0 in ([np.zeros(3)] if prev is None else [prev, np.zeros(3)]):
                r = _ls(p0, g, a0, nuf, V_obs, rD, lo, hi)
                if best is None or r.cost < best.cost:
                    best = r
            chi[k, j0] = 2.0 * best.cost + TGRID[k] ** 2
            par[k, j0] = best.x
            anchor[k] = best.x.copy()
            prev = best.x.copy()
            for jseq in (range(j0 + 1, G), range(j0 - 1, -1, -1)):
                p = best.x.copy()
                for j in jseq:
                    r = _ls(p, g, 10 ** XGRID[j], nuf, V_obs, rD, lo, hi)
                    chi[k, j] = 2.0 * r.cost + TGRID[k] ** 2
                    par[k, j] = r.x
                    p = r.x
    return chi, par


def cell_cold(g, k, j, V_obs=None, n_starts=6, seed=0):
    """best of n random cold starts at one (t, x) cell (optimizer check)."""
    rng = np.random.default_rng(seed)
    lo, hi = _bounds(g)
    V_obs = g["V"] if V_obs is None else V_obs
    rD = 1.0 + (g["eD"] / g["D"]) * TGRID[k]
    best = np.inf
    for s in range(n_starts):
        p0 = np.zeros(3) if s == 0 else rng.uniform(-2.5, 2.5, 3)
        r = _ls(p0, g, 10 ** XGRID[j], C4.nu_mono, V_obs, rD, lo, hi)
        best = min(best, 2.0 * r.cost + TGRID[k] ** 2)
    return best


def compute_profiles(gals, V_override=None, nproc=14):
    import multiprocessing as mp
    args = [(g, None if V_override is None else V_override[i]) for i, g in enumerate(gals)]
    ctx = mp.get_context("fork")
    with ctx.Pool(nproc) as pool:
        res = pool.map(profile_galaxy_2d, args, chunksize=1)
    return np.array([r[0] for r in res]), np.array([r[1] for r in res])


def mutate_velocities(g, z0):
    """MUTATE: V_obs -> V_obs sqrt(nu(y')/nu(y)), y = g_bar,fid/a0_ref, y' = y/(1 + BETA_MUT z0)."""
    S = g["Vg"] * np.abs(g["Vg"]) + UPS_D0 * g["Vd"] ** 2 + UPS_B0 * g["Vb"] ** 2
    y = S * 1e6 / (g["R"] * KPC_M) / A0_REF
    y2 = y / (1.0 + BETA_MUT * z0)
    return g["V"] * np.sqrt(C4.nu_mono(y2) / C4.nu_mono(y))


# ------------------------------------------------------------------------------------------------ curve machinery
def fine_curves(chi, feas):
    """cubic spline along t from TGRID onto TFINE, for each x; infeasible fine cells -> BIG."""
    N = chi.shape[0]
    out = np.full((N, len(TFINE), len(XGRID)), BIG)
    for i in range(N):
        kk = np.where(feas[i])[0]
        cs = CubicSpline(TGRID[kk], chi[i, kk, :], axis=0)
        m = (TFINE >= TGRID[kk[0]] - 1e-9) & (TFINE <= TGRID[kk[-1]] + 1e-9)
        out[i, m, :] = cs(TFINE[m])
    return out


def halfwidth(p, h):
    """Delta chi2 = 1 half-width of a 1D curve (mean of the two sides, capped at 1 dex); p already min-subtracted."""
    G = len(p)
    j = int(np.argmin(p))
    ws = []
    for step in (1, -1):
        k = j
        while 0 <= k + step < G and p[k + step] < 1.0:
            k += step
        if 0 <= k + step < G:
            c1, c2 = p[k], p[k + step]
            f = (1.0 - c1) / (c2 - c1) if c2 != c1 else 0.0
            ws.append(abs((k + f * step) - j) * h)
    return min(float(np.mean(ws)), 1.0) if ws else 1.0


def parabola_min(y, x0, h):
    j = int(np.clip(np.argmin(y), 1, len(y) - 2))
    y0, y1, y2 = y[j - 1], y[j], y[j + 1]
    den = y0 - 2 * y1 + y2
    off = 0.5 * (y0 - y2) / den if den > 0 else 0.0
    off = float(np.clip(off, -1, 1))
    return x0 + (j + off) * h, float(y1 - 0.125 * (y0 - y2) ** 2 / den) if den > 0 else float(y1)


class Curves:
    """per-galaxy 2D curves C_i(t, x) on (TFINE, XGRID) for the global fit (Addendum 2 weighting):
        C_eff(x, t) = t^2 + m(t) + q_i(t) [d(x, t) - m(t)],   d = (C - t^2)/s_i,   m(t) = min_x d,
        q_i(t) = sx(t)^2/(sx(t)^2 + tau^2),  sx(t) the Delta = 1 half-width of d(., t) - m(t) along x (fixed distance);
    the distance prior t^2 is never scaled.  s_i = max(1, chi2_min/(N_i - 1)) (Birge) or 1.  x_hat_i and sig_i (the
    distance-profiled preferred value and half-width) come from min_t [t^2 + d] (tau = 0).  Catmull-Rom along x (one
    linear ghost point at each end), a NON-DECREASING outward continuation beyond the grid (Addendum 1); min over t with a
    parabolic refinement (value and x-derivative Lagrange-interpolated at the refined t)."""

    def __init__(self, Cfine, npt, birge=True, tau=0.0):
        self.x0, self.h, self.G = float(XGRID[0]), float(XGRID[1] - XGRID[0]), len(XGRID)
        self.T = len(TFINE)
        self.k0 = int(np.argmin(np.abs(TFINE)))
        Cfine = np.asarray(Cfine, float)
        self.feas = Cfine[:, :, 0] < BIG / 2
        self.N = len(Cfine)
        self.rows = np.arange(self.N)
        t2 = (TFINE ** 2)[None, :, None]
        cmin_all = np.array([Cfine[i][self.feas[i]].min() for i in range(self.N)])
        dof = np.maximum(np.asarray(npt) - 1, 1)
        self.s = np.maximum(1.0, cmin_all / dof) if birge else np.ones(self.N)
        d = (Cfine - t2) / self.s[:, None, None]
        d[~self.feas] = BIG
        self.d = d
        self.m = d.min(axis=2)                                   # (N, T)
        self.sx = np.full((self.N, self.T), 1.0)
        for i in range(self.N):
            for k in np.where(self.feas[i])[0]:
                self.sx[i, k] = halfwidth(d[i, k] - self.m[i, k], self.h)
        base = t2 + d                                            # tau = 0 curve (Birge-scaled data + unscaled prior)
        base[~self.feas] = BIG
        self.prof = base.min(axis=1) - np.min(base.min(axis=1), axis=1)[:, None]
        self.xhat = np.array([parabola_min(self.prof[i], self.x0, self.h)[0] for i in range(self.N)])
        self.sig = np.array([halfwidth(self.prof[i], self.h) for i in range(self.N)])
        jx = np.clip(np.round((self.xhat - self.x0) / self.h).astype(int), 0, self.G - 1)
        self.tstar = TFINE[np.argmin(base[np.arange(self.N), :, jx], axis=1)]
        self.q = np.ones(self.N)                                 # kept for interface compatibility (weights are inside C)
        self.set_tau(tau)

    def set_tau(self, tau):
        self.tau = float(tau)
        qt = self.sx ** 2 / (self.sx ** 2 + self.tau ** 2)       # (N, T)
        t2 = (TFINE ** 2)[None, :, None]
        C = t2 + self.m[:, :, None] + qt[:, :, None] * (self.d - self.m[:, :, None])
        C[~self.feas] = BIG
        cmin = np.array([C[i][self.feas[i]].min() for i in range(self.N)])
        C = C - cmin[:, None, None]
        C[~self.feas] = BIG
        self.C = C
        self.Cp = np.concatenate([2 * C[:, :, :1] - C[:, :, 1:2], C, 2 * C[:, :, -1:] - C[:, :, -2:-1]], axis=2)
        self.Cp[~self.feas] = BIG
        self.qt = qt
        return self

    def with_tau(self, tau):
        """a copy of this (full) object with another tau."""
        if getattr(self, "_is_subset", False):
            raise RuntimeError("with_tau on a subset")
        c = Curves.__new__(Curves)
        c.__dict__.update(self.__dict__)
        return c.set_tau(tau)

    def subset(self, idx):
        c = Curves.__new__(Curves)
        c.__dict__.update(self.__dict__)
        c._is_subset = True
        idx = np.asarray(idx)
        for k in ("s", "q", "prof", "xhat", "sig", "tstar", "rows"):
            setattr(c, k, getattr(self, k)[idx])
        c.N = len(idx)
        return c

    def ev(self, X, idx=None):
        """values and x-derivatives of C_i(t_k, X_ik) for X (N, T); idx selects (with repeats) among this object's rows."""
        rows = self.rows if idx is None else self.rows[np.asarray(idx)]
        Cp = self.Cp
        t = (X - self.x0) / self.h
        tc = np.clip(t, 0.0, self.G - 1.0 - 1e-9)
        j = np.floor(tc).astype(int)
        f = tc - j
        N, T = X.shape
        ii = rows[:, None]
        kk = np.arange(T)[None, :]
        p0, p1, p2, p3 = Cp[ii, kk, j], Cp[ii, kk, j + 1], Cp[ii, kk, j + 2], Cp[ii, kk, j + 3]
        a = 3 * (p1 - p2) + p3 - p0
        bq = 2 * p0 - 5 * p1 + 4 * p2 - p3
        val = p1 + 0.5 * f * (p2 - p0 + f * (bq + f * a))
        der = (0.5 * (p2 - p0) + f * bq + 1.5 * f * f * a) / self.h
        out = t - tc
        slope = np.where(out > 0, np.maximum(der, 0.0), np.where(out < 0, np.minimum(der, 0.0), der))
        val = val + slope * out * self.h
        return val, slope


def _u_safe(u):
    """log10(u) with a linear continuation below u = 0.05 and a quadratic penalty (keeps 1 + beta z > 0)."""
    u0 = 0.05
    ok = u >= u0
    lg = np.where(ok, np.log10(np.maximum(u, u0)), math.log10(u0) + (u - u0) / (u0 * LN10))
    dlg = np.where(ok, 1.0 / (np.maximum(u, u0) * LN10), 1.0 / (u0 * LN10))
    pen = np.where(ok, 0.0, 1e4 * (u0 - u) ** 2)
    dpen = np.where(ok, 0.0, -2e4 * (u0 - u))
    return lg, dlg, pen, dpen


def _tmin(val, grads):
    """min over t (axis 1) with parabolic refinement; grads: list of (N, T) arrays interpolated at the refined t."""
    N, T = val.shape
    k = np.argmin(val, axis=1)
    kc = np.clip(k, 1, T - 2)
    r = np.arange(N)
    y0, y1, y2 = val[r, kc - 1], val[r, kc], val[r, kc + 1]
    den = y0 - 2 * y1 + y2
    good = (den > 1e-12) & (k == kc) & (y0 < BIG / 4) & (y2 < BIG / 4)
    s = np.where(good, 0.5 * (y0 - y2) / np.where(good, den, 1.0), 0.0)
    s = np.clip(s, -0.5, 0.5)
    w0, w1, w2 = 0.5 * s * (s - 1), 1 - s * s, 0.5 * s * (s + 1)
    v = np.where(good, w0 * y0 + w1 * y1 + w2 * y2, val[r, k])
    out = []
    for gA in grads:
        out.append(np.where(good, w0 * gA[r, kc - 1] + w1 * gA[r, kc] + w2 * gA[r, kc + 1], gA[r, k]))
    return v, out, np.where(good, TFINE[kc] + s * (TFINE[1] - TFINE[0]), TFINE[k])


class Fitter:
    """F(q) = sum_i w_i min_t C_i(L + lg(1 + beta Z_it) + lg(1 + n_i.theta) + G_i.gamma - delta_i, t_k).
    q = (L, beta, theta (if dipole), gamma (if G))."""

    def __init__(self, cv, Z, nvec=None, G=None, delta=None, idx=None, use_q=True, offset=None):
        self.cv = cv
        self.idx = None if idx is None else np.asarray(idx)
        sel = (lambda a: a) if idx is None else (lambda a: a[self.idx])
        self.Z = sel(np.asarray(Z, float))
        self.N = self.Z.shape[0]
        self.nvec = None if nvec is None else sel(np.asarray(nvec, float))
        self.G = None if G is None else sel(np.asarray(G, float))
        self.delta = np.zeros(self.N) if delta is None else sel(np.asarray(delta, float))
        self.offset = None if offset is None else sel(np.asarray(offset, float))   # fixed (N, T) addition to x
        self.w = np.ones(self.N)                                 # weights live inside the curves (Addendum 2)
        self.kd = 0 if nvec is None else 3
        self.m = 0 if G is None else self.G.shape[1]

    def fun(self, q):
        L, beta = q[0], q[1]
        th = q[2:2 + self.kd]
        ga = q[2 + self.kd:]
        u = 1.0 + beta * self.Z
        lg, dlg, pen, dpen = _u_safe(u)
        X = L + lg - self.delta[:, None]
        if self.offset is not None:
            X = X + self.offset
        if self.kd:
            ud = 1.0 + self.nvec @ th
            lgd, dlgd, pend, dpend = _u_safe(ud)
            X = X + lgd[:, None]
        if self.m:
            X = X + (self.G @ ga)[:, None]
        val, der = self.cv.ev(X, self.idx)
        val = val + pen
        gb = der * dlg * self.Z + dpen * self.Z
        grads = [der, gb]
        v, gg, _ = _tmin(val, grads)
        dI, gbI = gg
        w = self.w
        F = float(np.sum(w * v))
        g = [np.sum(w * dI), np.sum(w * gbI)]
        if self.kd:
            F += float(np.sum(w * pend))
            g += list(self.nvec.T @ (w * (dI * dlgd + dpend)))
        if self.m:
            g += list(self.G.T @ (w * dI))
        return F, np.array(g)

    def fit(self, beta_starts=(0.0,), fix_beta=None, L0=None):
        Lg = float(np.median(self.cv.xhat if self.idx is None else self.cv.xhat[self.idx])) if L0 is None else L0
        nq = 2 + self.kd + self.m
        bnds = [(-12.0, -8.0), (-5.0, 20.0)] + [(-0.95, 0.95)] * self.kd + [(-5.0, 5.0)] * self.m
        if fix_beta is not None:
            bnds[1] = (fix_beta, fix_beta)
            beta_starts = (fix_beta,)
        best = None
        for b0 in beta_starts:
            q0 = np.zeros(nq)
            q0[0], q0[1] = Lg, b0
            r = minimize(self.fun, q0, jac=True, method="L-BFGS-B", bounds=bnds,
                         options=dict(maxiter=500, ftol=1e-13, gtol=1e-9))
            if best is None or r.fun < best.fun:
                best = r
        q = best.x
        return dict(F=float(best.fun), L=float(q[0]), beta=float(q[1]), theta=q[2:2 + self.kd].copy(),
                    gamma=q[2 + self.kd:].copy(), ok=bool(best.success), q=q.copy())

    def tstar(self, q):
        """the profiled t of each galaxy at parameters q."""
        L, beta = q[0], q[1]
        lg = _u_safe(1.0 + beta * self.Z)[0]
        X = L + lg - self.delta[:, None]
        if self.kd:
            X = X + _u_safe(1.0 + self.nvec @ q[2:5])[0][:, None]
        if self.m:
            X = X + (self.G @ q[2 + self.kd:])[:, None]
        val, der = self.cv.ev(X, self.idx)
        return _tmin(val, [der])[2]


def fit_tau(xhat, sig):
    """ML (L, tau) of x_hat_i ~ N(L, sig_i^2 + tau^2)."""
    def nll(p):
        L, lt = p
        v = sig ** 2 + math.exp(2 * lt)
        return 0.5 * np.sum((xhat - L) ** 2 / v + np.log(v))
    best = None
    for lt0 in (-4.0, -2.5, -1.5):
        r = minimize(nll, [np.median(xhat), lt0], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9, maxiter=4000))
        if best is None or r.fun < best.fun:
            best = r
    L, lt = best.x
    tau = math.exp(lt)
    return float(L), (tau if tau > 1e-3 else 0.0)


def fisher_sigma_beta(z, sig, tau):
    v = 1.0 / (sig ** 2 + tau ** 2)
    zb = np.sum(v * z) / np.sum(v)
    return LN10 / math.sqrt(np.sum(v * (z - zb) ** 2))


# ------------------------------------------------------------------------------------------------ pooled ensembles
_POOL_STATE = {}


def _pool_init(state):
    _POOL_STATE.clear()
    _POOL_STATE.update(state)


def run_pool(func, tasks, state, nproc=14, chunksize=8):
    import multiprocessing as mp
    ctx = mp.get_context("fork")
    _pool_init(state)                                        # fork copies the module global into the workers
    with ctx.Pool(nproc) as pool:
        return pool.map(func, tasks, chunksize=chunksize)


# ------------------------------------------------------------------------------------------------ ensemble tasks (pool)
def zmat(U, VP2):
    """z = (u^2 + v_perp^2)/w_ref^2 (VP2 = 0 for W1)."""
    return (U ** 2 + np.asarray(VP2)[:, None]) / W_REF ** 2


def task_noise(seed):
    """curve-level mock: preferred value at L0 + eps_i (+ injected log10(1 + beta_inj z_i(0))), real speeds; returns beta_hat."""
    S = _POOL_STATE
    rng = np.random.default_rng(int(seed))
    cv = S["cv"]
    eps = rng.normal(0.0, np.sqrt(cv.sig ** 2 + S["tau"] ** 2))
    shift = S["L0"] + eps - cv.xhat
    if S.get("beta_inj", 0.0) != 0.0:
        shift = shift + np.log10(np.maximum(1.0 + S["beta_inj"] * S["Z"][:, S["k0"]], 1e-3))
    r = Fitter(cv, S["Z"], delta=shift, use_q=S.get("use_q", True)).fit(beta_starts=(0.0,), L0=S["L0"])
    return r["beta"]


def task_perm(seed):
    """speed shuffle: galaxy i gets u_pi(i)(0) (+ v_perp of pi(i)) and keeps its own distance lever."""
    S = _POOL_STATE
    rng = np.random.default_rng(int(seed))
    U, k0, VP2, groups = S["U"], S["k0"], S["VP2"], S.get("groups")
    N = U.shape[0]
    if groups is None:
        pi = rng.permutation(N)
    else:
        pi = np.arange(N)
        for gidx in groups:
            pi[gidx] = gidx[rng.permutation(len(gidx))]
    Up = U[pi, k0][:, None] + (U - U[:, k0][:, None])
    Z = zmat(Up, VP2[pi])
    r = Fitter(S["cv"], Z, use_q=S.get("use_q", True)).fit(beta_starts=(0.0,), L0=S["L0"])
    return r["beta"]


def task_boot(seed):
    """galaxy bootstrap: resample with replacement; returns (beta_hat, L_hat)."""
    S = _POOL_STATE
    rng = np.random.default_rng(int(seed))
    N = S["Z"].shape[0]
    idx = rng.integers(0, N, N)
    r = Fitter(S["cv"], S["Z"], idx=idx, use_q=S.get("use_q", True)).fit(beta_starts=(0.0,), L0=S["L0"])
    return r["beta"], r["L"]
