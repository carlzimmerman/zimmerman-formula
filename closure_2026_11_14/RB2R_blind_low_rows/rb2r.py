"""RB2R blind re-grade: rows below form B's isolated law, and whether tidal stripping can reach them.

Usage (from anywhere; paths are built from this file's location):
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 19 python3 -I -B rb2r.py

Writes rb2r.out, rb2r.json (graded run) and rb2r_MUTATE.out, rb2r_MUTATE.json (known answers, twins, sensitivities)
next to this file. Criteria: FROZEN_CRITERIA.md in the same folder.
"""
import csv
import json
import math
import os
import sys
import zlib

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "real_research", "data", "dsph")

G = 6.67430e-11
GMSUN = 1.32712440018e20
MSUN = GMSUN / G
PC = 3.0856775814913673e16
KPC = 1e3 * PC
KMS = 1e3
FOOTINGS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
VC = {"mw": 200.0, "m31": 230.0}
N_DRAW = 2000
N_ORBIT = 500
MV_CUT = -7.7
LOGM_CUT = 5.4
M31_RADEC = (10.6847, 41.2690)
EXCLUDE = {"LMC", "SMC", "M 32"}
OUT_LINES = []
MUT_LINES = []


def jdef(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return float(o)


def say(line, mut=False):
    (MUT_LINES if mut else OUT_LINES).append(line)
    print(line)


# ---------------------------------------------------------------- the law and form B
def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def g_law(gN, a0):
    return nu(gN / a0) * gN


def plummer_frac(r, a):
    return r ** 3 / (r * r + a * a) ** 1.5


def mb_enc(r, mstar, a, rhalf):
    """Baryon mass (kg) inside r: Plummer shape, normalised to M*/2 at r_1/2 (FROZEN_CRITERIA C4)."""
    return 0.5 * mstar * plummer_frac(r, a) / plummer_frac(rhalf, a)


def g_iso_at(r, mstar, a, rhalf, a0):
    gN = G * mb_enc(r, mstar, a, rhalf) / r ** 2
    return g_law(gN, a0)


def g_B(r, mstar, a, rhalf, rJ, a0):
    """Form B at radius r (arrays broadcast)."""
    mb = mb_enc(r, mstar, a, rhalf)
    gN = G * mb / r ** 2
    giso = g_law(gN, a0)
    mbJ = mb_enc(rJ, mstar, a, rhalf)
    gNJ = G * mbJ / rJ ** 2
    mph = (nu(gNJ / a0) - 1.0) * mbJ
    gtr = gN + G * mph / r ** 2
    return np.where(r <= rJ, giso, gtr)


def solve_rJ_vec(gfun, target, lo=1e-4 * PC, hi=1e9 * PC, iters=90):
    """Vectorised bisection on ln r for ln(g(r)/r) = ln(target); g(r)/r decreasing in r."""
    target = np.asarray(target, dtype=float)
    llo = np.full(np.shape(target), math.log(lo))
    lhi = np.full(np.shape(target), math.log(hi))
    lt = np.log(target)
    for _ in range(iters):
        mid = 0.5 * (llo + lhi)
        r = np.exp(mid)
        f = np.log(gfun(r) / r) - lt
        pos = f > 0  # still above the target: root is further out
        llo = np.where(pos, mid, llo)
        lhi = np.where(pos, lhi, mid)
    return np.exp(0.5 * (llo + lhi))


def solve_rJ_scalar(gfun, target, lo=1e-4 * PC, hi=1e9 * PC):
    f = lambda lr: math.log(float(gfun(math.exp(lr))) / math.exp(lr)) - math.log(target)
    if f(math.log(lo)) <= 0:
        return lo
    if f(math.log(hi)) >= 0:
        return hi
    return math.exp(brentq(f, math.log(lo), math.log(hi), xtol=1e-14, rtol=1e-14, maxiter=500))


def check_monotone(gfun):
    r = np.exp(np.linspace(math.log(1e-4 * PC), math.log(1e9 * PC), 400))
    v = np.log(gfun(r) / r)
    return bool(np.all(np.diff(v) < 0))


# ---------------------------------------------------------------- catalogue
def fnum(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n)
    return np.where(z > 0, c + z * ep, c + z * em)


def load_rows():
    rows, left_out, skipped = [], [], []
    for fname, host in (("lvd_dwarf_mw.csv", "mw"), ("lvd_dwarf_m31.csv", "m31"), ("lvd_dwarf_local_field.csv", "field")):
        for x in csv.DictReader(open(os.path.join(DATA, fname))):
            name = x["name"]
            sig = fnum(x["vlos_sigma"])
            ul = fnum(x["vlos_sigma_ul"]) if x["vlos_sigma_ul"].strip() else None
            is_ul = x["vlos_sigma_ul"].strip() != ""
            if name in EXCLUDE:
                if sig is not None:
                    skipped.append((name, host, "excluded by name"))
                continue
            if sig is None and is_ul and ul is not None:
                sig = ul  # graded and marked (FROZEN_CRITERIA A, lead's restriction)
            if sig is None or sig <= 0:
                continue
            rcol = "rhalf_sph_physical" if fnum(x["rhalf_sph_physical"]) else "rhalf_physical"
            R = fnum(x[rcol])
            if R is None or R <= 0:
                skipped.append((name, host, "no half-light radius"))
                continue
            MV = fnum(x["M_V"])
            logm = fnum(x["mass_stellar"])
            mfrom = "mass_stellar"
            if logm is None:
                logm = 0.4 * (4.83 - MV) + 0.301
                mfrom = "M_V"
            bright = (MV <= MV_CUT) if MV is not None else (logm >= LOGM_CUT)
            if not bright:
                left_out.append((name, host, MV))
                continue
            sem = fnum(x["vlos_sigma_em"]) or 0.1 * sig
            sep = fnum(x["vlos_sigma_ep"]) or 0.1 * sig
            rem = fnum(x[rcol + "_em"]) or 0.1 * R
            rep = fnum(x[rcol + "_ep"]) or 0.1 * R
            dem = fnum(x["distance_modulus_em"]) or 0.1
            dep = fnum(x["distance_modulus_ep"]) or 0.1
            d = None
            if host in ("mw", "m31"):
                d = fnum(x["distance_host"])
                if d is None and host == "m31":
                    d = fnum(x["distance_m31"])
                if d is None:
                    d = fnum(x["distance"])
            alt_R = fnum(x["rhalf_physical"])
            rows.append(dict(key=x["key"], name=name, host=host, cat_host=x["host"], MV=MV, logm=logm, mfrom=mfrom,
                             sig=sig, sem=sem, sep=sep, R=R, rem=rem, rep=rep, rcol=rcol,
                             R_major=alt_R, R_major_em=fnum(x["rhalf_physical_em"]), R_major_ep=fnum(x["rhalf_physical_ep"]),
                             DM=fnum(x["distance_modulus"]), dem=dem, dep=dep, d_kpc=d,
                             ra=fnum(x["ra"]), dec=fnum(x["dec"]), dist=fnum(x["distance"]),
                             pmra=fnum(x["pmra"]), pmra_em=fnum(x["pmra_em"]), pmra_ep=fnum(x["pmra_ep"]),
                             pmdec=fnum(x["pmdec"]), pmdec_em=fnum(x["pmdec_em"]), pmdec_ep=fnum(x["pmdec_ep"]),
                             vlos=fnum(x["vlos_systemic"]), vlos_em=fnum(x["vlos_systemic_em"]),
                             vlos_ep=fnum(x["vlos_systemic_ep"]), ul=is_ul))
    return rows, left_out, skipped


def ang_sep(ra1, dec1, ra2, dec2):
    r1, d1, r2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.acos(max(-1.0, min(1.0, c)))


def m31_distance():
    plus, minus = [], []
    for x in csv.DictReader(open(os.path.join(DATA, "lvd_dwarf_m31.csv"))):
        D, dm, ra, dec = fnum(x["distance"]), fnum(x["distance_m31"]), fnum(x["ra"]), fnum(x["dec"])
        if None in (D, dm, ra, dec):
            continue
        th = ang_sep(ra, dec, *M31_RADEC)
        disc = dm * dm - (D * math.sin(th)) ** 2
        if disc < 0:
            continue
        plus.append(D * math.cos(th) + math.sqrt(disc))
        minus.append(D * math.cos(th) - math.sqrt(disc))
    return float(np.median(plus)), float(np.median(minus)), len(plus)


# ---------------------------------------------------------------- orbits
KMS_KPC_MYR = 1.0227121650537077e-3  # 1 km/s in kpc/Myr


def galcen(ra, dec, D_kpc, pmra, pmdec, vlos, cosdec_reading=True):
    import astropy.units as u
    from astropy.coordinates import SkyCoord, Galactocentric
    if not cosdec_reading:
        pmra = pmra * np.cos(np.radians(dec))
    c = SkyCoord(ra=np.full(np.shape(D_kpc), ra) * u.deg, dec=np.full(np.shape(D_kpc), dec) * u.deg,
                 distance=D_kpc * u.kpc, pm_ra_cosdec=pmra * u.mas / u.yr, pm_dec=pmdec * u.mas / u.yr,
                 radial_velocity=vlos * u.km / u.s, frame="icrs")
    gc = c.transform_to(Galactocentric())
    pos = np.stack([gc.x.to_value(u.kpc), gc.y.to_value(u.kpc), gc.z.to_value(u.kpc)], axis=-1)
    vel = np.stack([gc.v_x.to_value(u.km / u.s), gc.v_y.to_value(u.km / u.s), gc.v_z.to_value(u.km / u.s)], axis=-1)
    return pos, vel


def peri_analytic(pos, vel, vc):
    r = np.linalg.norm(pos, axis=-1)
    v2 = np.sum(vel ** 2, axis=-1)
    L = np.linalg.norm(np.cross(pos, vel), axis=-1)
    E = 0.5 * v2 + vc ** 2 * np.log(r)
    out = np.empty_like(r)
    for i in range(len(r)):
        h = lambda x: 2.0 * (E[i] - vc ** 2 * math.log(x)) * x * x - L[i] ** 2
        if h(r[i]) <= 0:
            out[i] = r[i]
        else:
            out[i] = brentq(h, 1e-9 * r[i], r[i], xtol=1e-12, rtol=1e-13)
    return out


def peri_leapfrog(pos, vel, vc, dt=0.25, tmax=10000.0):
    """KDK leapfrog in Phi = vc^2 ln r; kpc, kpc/Myr; forward and backward; returns min r and max |dE/E|."""
    v_c = vc * KMS_KPC_MYR
    nstep = int(round(tmax / dt))
    rmin = np.linalg.norm(pos, axis=-1)
    edrift = np.zeros(len(rmin))
    hit_end = np.zeros(len(rmin), dtype=bool)
    for sgn in (1.0, -1.0):
        x = pos.copy()
        v = vel * KMS_KPC_MYR
        h = sgn * dt
        E0 = 0.5 * np.sum(v * v, axis=1) + v_c ** 2 * np.log(np.linalg.norm(x, axis=1))
        acc = lambda q: -v_c ** 2 * q / np.sum(q * q, axis=1)[:, None]
        a = acc(x)
        rmin_dir = np.linalg.norm(x, axis=1)
        last_r = rmin_dir.copy()
        for _ in range(nstep):
            v += 0.5 * h * a
            x += h * v
            a = acc(x)
            v += 0.5 * h * a
            r = np.linalg.norm(x, axis=1)
            rmin_dir = np.minimum(rmin_dir, r)
            last_r = r
        E1 = 0.5 * np.sum(v * v, axis=1) + v_c ** 2 * np.log(last_r)
        edrift = np.maximum(edrift, np.abs((E1 - E0) / E0))
        hit_end |= (rmin_dir >= last_r - 1e-9)
        rmin = np.minimum(rmin, rmin_dir)
    return rmin, edrift, hit_end


def pericentre_draws(row, rng, vc=200.0, cosdec_reading=True):
    n = N_ORBIT
    DM = split_normal(rng, row["DM"], row["dem"], row["dep"], n)
    D = 10 ** (DM / 5 + 1) / 1e3
    pmra = split_normal(rng, row["pmra"], row["pmra_em"] or 0.0, row["pmra_ep"] or 0.0, n)
    pmdec = split_normal(rng, row["pmdec"], row["pmdec_em"] or 0.0, row["pmdec_ep"] or 0.0, n)
    vlos = split_normal(rng, row["vlos"], row["vlos_em"] or 1.0, row["vlos_ep"] or 1.0, n)
    pos, vel = galcen(row["ra"], row["dec"], D, pmra, pmdec, vlos, cosdec_reading)
    pa = peri_analytic(pos, vel, vc)
    pl, ed, hit = peri_leapfrog(pos, vel, vc)
    bad = np.abs(pl / pa - 1) > 0.01
    peri = np.where(bad, pa, pl)
    # central values
    posc, velc = galcen(row["ra"], row["dec"], np.array([10 ** (row["DM"] / 5 + 1) / 1e3]), np.array([row["pmra"]]),
                        np.array([row["pmdec"]]), np.array([row["vlos"]]), cosdec_reading)
    pac = peri_analytic(posc, velc, vc)[0]
    plc, edc, _ = peri_leapfrog(posc, velc, vc)
    return dict(p16=float(np.percentile(peri, 16)), p50=float(np.median(peri)), n_analytic_used=int(bad.sum()),
                central_leapfrog=float(plc[0]), central_analytic=float(pac), central_Edrift=float(edc[0]),
                r_now_central=float(np.linalg.norm(posc[0])))


# ---------------------------------------------------------------- dwarf grading
def draws_for(row, seed, use_major=False):
    rng = np.random.default_rng(seed)
    n = N_DRAW
    if use_major:
        R, rem, rep = row["R_major"], row["R_major_em"] or 0.1 * row["R_major"], row["R_major_ep"] or 0.1 * row["R_major"]
    else:
        R, rem, rep = row["R"], row["rem"], row["rep"]
    sig = split_normal(rng, row["sig"], row["sem"], row["sep"], n)
    Rd = split_normal(rng, R, rem, rep, n)
    dDM = split_normal(rng, 0.0, row["dem"], row["dep"], n)
    nclip = int(np.sum(sig <= 0) + np.sum(Rd <= 0))
    sig = np.where(sig <= 0, 1e-3 * row["sig"], sig)
    Rd = np.where(Rd <= 0, 1e-3 * R, Rd)
    fD = 10 ** (dDM / 5)
    Rh = Rd * fD * PC
    mstar = 10 ** row["logm"] * MSUN * fD ** 2
    rhalf = 4.0 / 3.0 * Rh
    gobs = 3 * (sig * KMS) ** 2 / rhalf
    c = dict(Rh=R * PC, mstar=10 ** row["logm"] * MSUN, sig=row["sig"])
    c["rhalf"] = 4.0 / 3.0 * c["Rh"]
    c["gobs"] = 3 * (row["sig"] * KMS) ** 2 / c["rhalf"]
    return dict(Rh=Rh, mstar=mstar, rhalf=rhalf, gobs=gobs, nclip=nclip), c


def logg_iso_c(c, a0, f=1.0):
    return math.log10(float(g_iso_at(c["rhalf"], f * c["mstar"], c["Rh"], c["rhalf"], a0)))


def k_iso(c, a0, f=1.0):
    h = 0.01
    return (logg_iso_c(c, a0, f * 10 ** h) - logg_iso_c(c, a0, f * 10 ** -h)) / (2 * h)


def rJ_central(c, a0, target_fn, f=1.0):
    m = f * c["mstar"]
    gf = lambda r: g_iso_at(r, m, c["Rh"], c["rhalf"], a0)
    return solve_rJ_scalar(gf, target_fn(m))


def edge_eval(D, c, a0, tidal, k, strong_mode=None):
    """tidal = G M_host(<d)/d^3 (s^-2). strong_mode: None, or ('div', tidal_primary) for r_J(primary)/3^(2/3)."""
    def rJ_draws(mstar, Rh, rhalf):
        gf = lambda r: g_iso_at(r, mstar, Rh, rhalf, a0)
        if strong_mode == "div":
            return solve_rJ_vec(gf, np.full(np.shape(mstar), 3 * tidal)) / 3 ** (2 / 3)
        return solve_rJ_vec(gf, np.full(np.shape(mstar), k * tidal))

    rJ = rJ_draws(D["mstar"], D["Rh"], D["rhalf"])
    gb = g_B(D["rhalf"], D["mstar"], D["Rh"], D["rhalf"], rJ, a0)
    res = np.log10(D["gobs"] / gb)

    def logg_c(f):
        m = f * c["mstar"]
        rj = rJ_draws(np.array([m]), np.array([c["Rh"]]), np.array([c["rhalf"]]))[0]
        return math.log10(float(g_B(c["rhalf"], m, c["Rh"], c["rhalf"], rj, a0))), rj

    lg0, rj0 = logg_c(1.0)
    h = 0.01
    kk = (logg_c(10 ** h)[0] - logg_c(10 ** -h)[0]) / (2 * h)
    med, sd = float(np.median(res)), float(np.std(res))
    s = math.sqrt(sd ** 2 + (0.15 * kk) ** 2)
    return dict(rJ_pc=rj0 / PC, rJ_over_rhalf=rj0 / c["rhalf"], resid=med, sd=sd, k=kk, s=s,
                resid_plus_2s=med + 2 * s, rJ_draw_median_over_rhalf=float(np.median(rJ / D["rhalf"])))


def ml_needed(Di, sdi, c, a0):
    def F(f, two=True):
        dl = Di - (logg_iso_c(c, a0, f) - logg_iso_c(c, a0, 1.0))
        if not two:
            return dl
        return dl + 2 * math.sqrt(sdi ** 2 + (0.15 * k_iso(c, a0, f)) ** 2)
    out = {}
    for key, two in (("ups_V_not_low", True), ("ups_V_delta_zero", False)):
        try:
            lf = brentq(lambda q: F(10 ** q, two), -8, 0, xtol=1e-10)
            out[key] = 2.0 * 10 ** lf
        except ValueError:
            out[key] = None
    return out


def grade_dwarf(row, a0, m31_dist, peri=None, use_major=False):
    seed = 20261114 + zlib.crc32(row["key"].encode()) % (2 ** 31)
    D, c = draws_for(row, seed, use_major)
    giso = g_iso_at(D["rhalf"], D["mstar"], D["Rh"], D["rhalf"], a0)
    dl = np.log10(D["gobs"] / giso)
    Di, sdi = float(np.median(dl)), float(np.std(dl))
    ki = k_iso(c, a0)
    si = math.sqrt(sdi ** 2 + (0.15 * ki) ** 2)
    low = Di + 2 * si < 0
    out = dict(name=row["name"], host=row["host"], cat_host=row["cat_host"], M_V=row["MV"], logM=row["logm"],
               sigma=row["sig"], R_h_pc=c["Rh"] / PC, r_half_pc=c["rhalf"] / PC, upper_limit=row["ul"],
               Delta_iso=Di, sd=sdi, k_iso=ki, s=si, Delta_plus_2s=Di + 2 * si, LOW=bool(low), nclip=D["nclip"])
    gf = lambda r: g_iso_at(r, c["mstar"], c["Rh"], c["rhalf"], a0)
    out["monotone"] = check_monotone(gf)
    if row["host"] == "field":
        out["edges"] = None
    else:
        vc = VC[row["host"]] * KMS
        d = row["d_kpc"] * KPC
        tidal = vc ** 2 / d ** 2
        e = {"d_kpc": row["d_kpc"]}
        e["primary"] = edge_eval(D, c, a0, tidal, 3)
        e["weak"] = edge_eval(D, c, a0, tidal, 2)
        if row["host"] == "mw":
            if peri is not None:
                e["strong_mode"] = "pericentre p16 = %.2f kpc" % peri["p16"]
                e["strong"] = edge_eval(D, c, a0, vc ** 2 / (peri["p16"] * KPC) ** 2, 3)
            else:
                e["strong_mode"] = "r_J(primary)/3^(2/3)"
                e["strong"] = edge_eval(D, c, a0, tidal, 3, strong_mode="div")
        else:
            th = ang_sep(row["ra"], row["dec"], *M31_RADEC)
            Rp = m31_dist * math.sin(th)
            e_proj = edge_eval(D, c, a0, vc ** 2 / (Rp * KPC) ** 2, 3)
            e_div = edge_eval(D, c, a0, tidal, 3, strong_mode="div")
            if e_proj["rJ_pc"] <= e_div["rJ_pc"]:
                e["strong_mode"] = "projected distance %.1f kpc" % Rp
                e["strong"] = e_proj
            else:
                e["strong_mode"] = "r_J(primary)/3^(2/3) (projected %.1f kpc gives larger r_J)" % Rp
                e["strong"] = e_div
        out["edges"] = e
    if low:
        out["ml_needed"] = ml_needed(Di, sdi, c, a0)
        if out["edges"] is None:
            out["word"] = "TIDES CANNOT REACH"
            out["word_note"] = "field row: no tidal edge"
        else:
            st = out["edges"]["strong"]
            out["word"] = "TIDES CAN REACH" if st["resid_plus_2s"] >= 0 else "TIDES CANNOT REACH"
            out["reach_needs_rJ_inside_rhalf"] = bool(out["word"] == "TIDES CAN REACH" and st["rJ_over_rhalf"] < 1)
    return out


# ---------------------------------------------------------------- DF2 / DF4
DFS = {"DF2": dict(M=2.0e8, Re=2.0, sig=8.5, ep=2.3, em=3.1, ra=40.4451, dec=-8.4028),
       "DF4": dict(M=1.5e8, Re=1.6, sig=6.3, ep=2.5, em=1.6, ra=39.8128, dec=-8.1160)}
NGC1052 = (40.2700, -8.2558)
D_DF = 20e3  # kpc


def df_resid(p, gpred, rhalf):
    sp = math.sqrt(rhalf * gpred / 3) / KMS
    E = 2 * math.log(p["sig"] / sp)
    e = p["em"] if p["sig"] > sp else p["ep"]
    u = 2 * e / p["sig"]
    return E, u, sp


def grade_df(name, a0, host_mass_override=None):
    p = DFS[name]
    rhalf = 4.0 / 3.0 * p["Re"] * KPC
    a = rhalf / 1.30477
    m = p["M"] * MSUN
    giso = float(g_iso_at(rhalf, m, a, rhalf, a0))
    E, u, sp = df_resid(p, giso, rhalf)
    Rp = D_DF * ang_sep(p["ra"], p["dec"], *NGC1052) * KPC
    gN_host = G * 1e11 * MSUN / Rp ** 2
    Mhost = Rp ** 2 * float(g_law(gN_host, a0)) / G
    out = dict(name=name, r_half_kpc=rhalf / KPC, R_proj_kpc=Rp / KPC, M_host_law_Msun=Mhost / MSUN,
               sigma_pred_iso=sp, E_iso=E, u_iso=u, E_plus_2u=E + 2 * u, LOW=bool(E + 2 * u < 0))
    gf = lambda r: g_iso_at(r, m, a, rhalf, a0)

    def at(Mh, k):
        rJ = solve_rJ_scalar(gf, k * G * Mh / Rp ** 3)
        gb = float(g_B(rhalf, m, a, rhalf, rJ, a0))
        E2, u2, sp2 = df_resid(p, gb, rhalf)
        return dict(rJ_kpc=rJ / KPC, rJ_over_rhalf=rJ / rhalf, E=E2, u=u2, sigma_pred=sp2, E_plus_2u=E2 + 2 * u2)

    out["primary_strong_k3"] = at(Mhost, 3)
    out["weak_k2"] = at(Mhost, 2)
    if out["LOW"]:
        st = out["primary_strong_k3"]
        out["word"] = "TIDES CAN REACH" if st["E_plus_2u"] >= 0 else "TIDES CANNOT REACH"
        try:
            lm = brentq(lambda l: at(10 ** l * MSUN, 3)["E_plus_2u"], math.log10(Mhost / MSUN), 20, xtol=1e-8)
            out["M_host_needed_Msun"] = 10 ** lm
            out["M_host_needed_over_law"] = 10 ** lm / (Mhost / MSUN)
            out["at_needed"] = at(10 ** lm * MSUN, 3)
        except ValueError:
            out["M_host_needed_Msun"] = None
    return out


# ---------------------------------------------------------------- known answers and twins
def known_answers():
    res = {}
    a0 = FOOTINGS["canonical"]
    m, Rh = 1e7 * MSUN, 400 * PC
    rh = 4 / 3 * Rh
    gi = float(g_iso_at(rh, m, Rh, rh, a0))
    gb_inf = float(g_B(rh, m, Rh, rh, 1e12 * PC, a0))
    gN = G * 0.5 * m / rh ** 2
    gb_0 = float(g_B(rh, m, Rh, rh, 1e-6 * PC, a0))
    res["KA1_inf"] = abs(gb_inf / gi - 1)
    res["KA1_zero"] = abs(gb_0 / gN - 1)
    res["KA1_pass"] = res["KA1_inf"] < 1e-12 and res["KA1_zero"] < 1e-6
    msat, Mh, d = 1e6 * MSUN, 1e12 * MSUN, 50 * KPC
    rj = solve_rJ_scalar(lambda r: G * msat / r ** 2, G * 3 * Mh / d ** 3)  # g/r = 3 G M/d^3 with k folded as 3M
    exact = d * (msat / (3 * Mh)) ** (1 / 3)
    rjv = solve_rJ_vec(lambda r: G * msat / r ** 2, np.array([G * 3 * Mh / d ** 3]))[0]
    res["KA2_rel"] = abs(rj / exact - 1)
    res["KA2_vec_rel"] = abs(rjv / exact - 1)
    res["KA2_pass"] = res["KA2_rel"] < 1e-8 and res["KA2_vec_rel"] < 1e-8
    y = 1e-13
    gNd = y * a0
    res["KA3_rel"] = abs(float(g_law(gNd, a0)) / math.sqrt(gNd * a0) - 1)
    res["KA3_pass"] = res["KA3_rel"] < 1e-6
    return res


def twin_row(kind, host, d_kpc=None, R=500.0):
    m = 1e6
    rhalf = 4 / 3 * R * PC
    gN = G * 0.5 * m * MSUN / rhalf ** 2
    g = gN if kind == "newton" else float(g_law(gN, FOOTINGS["canonical"]))
    sig = math.sqrt(g * rhalf / 3) / KMS
    return dict(key="twin_%s_%s_%d" % (kind, host, R), name="TWIN %s %s R_h %d" % (kind, host, R), host=host, cat_host="", MV=-9.0,
                logm=6.0, mfrom="set", sig=sig, sem=0.05 * sig, sep=0.05 * sig, R=R, rem=0.05 * R, rep=0.05 * R,
                rcol="set", R_major=R, R_major_em=None, R_major_ep=None, DM=20.0, dem=0.05, dep=0.05, d_kpc=d_kpc,
                ra=None, dec=None, dist=None, pmra=None, vlos=None, ul=False)


# ---------------------------------------------------------------- main
def fmt_edge(tag, e):
    return ("    %-8s r_J/r_1/2 %8.3f  r_J %10.1f pc  resid %+7.3f  s %.3f  resid+2s %+7.3f"
            % (tag, e["rJ_over_rhalf"], e["rJ_pc"], e["resid"], e["s"], e["resid_plus_2s"]))


def main():
    import astropy
    rows, left_out, skipped = load_rows()
    m31p, m31m, nm31 = m31_distance()
    from astropy.coordinates import Galactocentric
    gcf = Galactocentric()
    say("RB2R blind re-grade. astropy %s; numpy %s" % (astropy.__version__, np.__version__))
    say("Galactocentric defaults: galcen_distance %s, z_sun %s, galcen_v_sun %s"
        % (gcf.galcen_distance, gcf.z_sun, gcf.galcen_v_sun))
    say("M31 distance (median of %d rows): + root %.1f kpc (used), - root %.1f kpc" % (nm31, m31p, m31m))
    say("Graded rows: %d. Left out by M_V <= %.1f cut: %d. Excluded / skipped among rows with sigma: %s"
        % (len(rows), MV_CUT, len(left_out), skipped))
    say("Upper-limit rows in the graded sample: %s" % [r["name"] for r in rows if r["ul"]])
    ka = known_answers()
    say("Known answers: %s" % json.dumps(ka, default=jdef))
    # pericentres for MW rows with proper motions
    peris = {}
    for r in rows:
        if r["host"] == "mw" and r["pmra"] is not None and r["pmdec"] is not None:
            rng = np.random.default_rng(20261114 + 1 + zlib.crc32(r["key"].encode()) % (2 ** 31))
            peris[r["name"]] = pericentre_draws(r, rng)
            p = peris[r["name"]]
            say("  orbit %-22s r_now %.1f  peri leapfrog %.2f analytic %.2f  dE %.1e  p16 %.2f p50 %.2f  analytic used %d/%d"
                % (r["name"], p["r_now_central"], p["central_leapfrog"], p["central_analytic"], p["central_Edrift"],
                   p["p16"], p["p50"], p["n_analytic_used"], N_ORBIT))
    ka4 = all(abs(p["central_leapfrog"] / p["central_analytic"] - 1) < 0.01 and p["central_Edrift"] < 1e-4
              for p in peris.values())
    ka["KA4_pass"] = bool(ka4)
    say("KA4 (integrator vs analytic pericentre to 1 %%, dE < 1e-4): %s" % ka4)
    result = dict(known_answers=ka, m31_distance_plus=m31p, m31_distance_minus=m31m, n_graded=len(rows),
                  left_out=[dict(name=a, host=b, M_V=c) for a, b, c in left_out], skipped=skipped,
                  pericentres=peris, footings={})
    for fk, a0 in FOOTINGS.items():
        say("")
        say("===== footing %s (a0 = %.4e) =====" % (fk, a0))
        graded = []
        for r in rows:
            g = grade_dwarf(r, a0, m31p, peris.get(r["name"]))
            graded.append(g)
            say("%-22s %-5s M_V %6.2f  Delta_iso %+7.3f  s %.3f  Delta+2s %+7.3f  %s%s"
                % (g["name"], g["host"], g["M_V"], g["Delta_iso"], g["s"], g["Delta_plus_2s"],
                   "LOW" if g["LOW"] else "not low", " [UL]" if g["upper_limit"] else ""))
            if g["LOW"]:
                if g["edges"]:
                    for tag in ("primary", "weak", "strong"):
                        say(fmt_edge(tag, g["edges"][tag]))
                    say("    strong edge: %s" % g["edges"]["strong_mode"])
                say("    WORD: %s%s   (Upsilon_V to stop being LOW %s; for Delta = 0 %s)"
                    % (g["word"], " (reach needs r_J < r_1/2)" if g.get("reach_needs_rJ_inside_rhalf") else "",
                       g["ml_needed"]["ups_V_not_low"], g["ml_needed"]["ups_V_delta_zero"]))
        inside = [(g["name"], g["edges"]["primary"]["rJ_over_rhalf"]) for g in graded
                  if g["edges"] and g["edges"]["primary"]["rJ_over_rhalf"] < 1]
        say("Rows with primary r_J < r_1/2: %s" % inside)
        say("Non-monotone g/r rows: %s" % [g["name"] for g in graded if not g["monotone"]])
        dfs = []
        for nm in DFS:
            dg = grade_df(nm, a0)
            dfs.append(dg)
            say("%s  R_proj %.1f kpc  M_host(<d) %.3e  sigma_pred_iso %.2f  E_iso %+.3f  u %.3f  E+2u %+.3f  %s"
                % (nm, dg["R_proj_kpc"], dg["M_host_law_Msun"], dg["sigma_pred_iso"], dg["E_iso"], dg["u_iso"],
                   dg["E_plus_2u"], "LOW" if dg["LOW"] else "not low"))
            for tag in ("primary_strong_k3", "weak_k2"):
                e = dg[tag]
                say("    %-17s r_J %.3f kpc r_J/r_1/2 %.3f  E %+.3f u %.3f E+2u %+.3f"
                    % (tag, e["rJ_kpc"], e["rJ_over_rhalf"], e["E"], e["u"], e["E_plus_2u"]))
            if dg["LOW"]:
                say("    WORD: %s; host mass inside d needed: %s Msun (x%s of the law's)"
                    % (dg["word"], "%.3e" % dg["M_host_needed_Msun"] if dg.get("M_host_needed_Msun") else None,
                       "%.1f" % dg["M_host_needed_over_law"] if dg.get("M_host_needed_Msun") else None))
        lows = [g for g in graded if g["LOW"]] + [d for d in dfs if d["LOW"]]
        cannot = [x["name"] for x in lows if x["word"] == "TIDES CANNOT REACH"]
        cannot_noul = [x["name"] for x in lows if x["word"] == "TIDES CANNOT REACH" and not x.get("upper_limit")]
        word = "LOW ROWS COUNT AGAINST B" if cannot else "NO LOW ROW COUNTS AGAINST B"
        word_noul = "LOW ROWS COUNT AGAINST B" if cannot_noul else "NO LOW ROW COUNTS AGAINST B"
        if not all(ka[k] for k in ("KA1_pass", "KA2_pass", "KA3_pass", "KA4_pass")):
            word = "NO VERDICT (known answer failed)"
        say("WORD (%s): %s; without upper-limit rows: %s; CANNOT REACH rows: %s" % (fk, word, word_noul, cannot))
        result["footings"][fk] = dict(a0=a0, word=word, word_without_ul=word_noul, cannot_reach=cannot,
                                      low_rows=[x["name"] for x in lows], dwarfs=graded, df=dfs,
                                      primary_rJ_inside_rhalf=inside)
    both = sorted(set(result["footings"]["canonical"]["cannot_reach"]) & set(result["footings"]["alt"]["cannot_reach"]))
    result["cannot_reach_both_footings"] = both
    say("")
    say("ACROSS FOOTINGS: rows reading TIDES CANNOT REACH on both footings: %s -> %s"
        % (both, "the part counts against B" if both else "the part does not count against B"))
    with open(os.path.join(HERE, "rb2r.out"), "w") as f:
        f.write("\n".join(OUT_LINES) + "\n")
    with open(os.path.join(HERE, "rb2r.json"), "w") as f:
        json.dump(result, f, indent=1, default=jdef)

    # ------------------------------------------------ MUTATE: twins and sensitivities
    mut = dict(twins={}, sensitivity={})
    for fk, a0 in FOOTINGS.items():
        t1 = grade_dwarf(twin_row("newton", "field"), a0, m31p)
        t2 = grade_dwarf(twin_row("law", "field"), a0, m31p)
        t3 = grade_dwarf(twin_row("newton", "mw", 20.0), a0, m31p)
        t4 = grade_dwarf(twin_row("newton", "field"), a0, m31p)
        t3b = grade_dwarf(twin_row("newton", "mw", 20.0, R=2000.0), a0, m31p)  # AMENDMENT_A1
        t4b = grade_dwarf(twin_row("newton", "field", R=2000.0), a0, m31p)  # AMENDMENT_A1
        bites = dict(T1_LOW=t1["LOW"], T2_not_LOW=not t2["LOW"],
                     A1_T3b_LOW=t3b["LOW"], A1_T3b_CAN_REACH=t3b.get("word") == "TIDES CAN REACH",
                     A1_T3b_rJ_inside=t3b["edges"]["primary"]["rJ_over_rhalf"],
                     A1_T3b_strong_rJ_inside=t3b["edges"]["strong"]["rJ_over_rhalf"],
                     A1_T3b_strong_resid_plus_2s=t3b["edges"]["strong"]["resid_plus_2s"],
                     A1_T4b_CANNOT=t4b.get("word") == "TIDES CANNOT REACH",
                     T3_CAN_REACH=t3.get("word") == "TIDES CAN REACH",
                     T3_rJ_inside=t3["edges"]["primary"]["rJ_over_rhalf"] if t3["edges"] else None,
                     T4_CANNOT=t4.get("word") == "TIDES CANNOT REACH")
        mut["twins"][fk] = dict(T1=t1, T2=t2, T3=t3, T4=t4, T3b=t3b, T4b=t4b, bites=bites)
        say("TWINS %s: %s" % (fk, json.dumps(bites, default=jdef)), mut=True)
        say("  T1 Delta %+.3f s %.3f; T2 Delta %+.3f s %.3f; T3 strong resid+2s %+.3f (r_J/r_1/2 strong %.3f)"
            % (t1["Delta_iso"], t1["s"], t2["Delta_iso"], t2["s"], t3["edges"]["strong"]["resid_plus_2s"],
               t3["edges"]["strong"]["rJ_over_rhalf"]), mut=True)
    # sensitivities for LOW rows: major-axis radius; pmra without cos(dec); M31 '-' root
    for fk, a0 in FOOTINGS.items():
        sens = []
        lows = [g["name"] for g in result["footings"][fk]["dwarfs"] if g["LOW"]]
        for r in rows:
            if r["name"] not in lows:
                continue
            gm = grade_dwarf(r, a0, m31p, peris.get(r["name"]), use_major=True)
            ent = dict(name=r["name"], major_axis=dict(Delta_iso=gm["Delta_iso"], s=gm["s"], LOW=gm["LOW"],
                                                         word=gm.get("word")))
            if r["name"] in peris:
                rng = np.random.default_rng(20261114 + 1 + zlib.crc32(r["key"].encode()) % (2 ** 31))
                pn = pericentre_draws(r, rng, cosdec_reading=False)
                gp = grade_dwarf(r, a0, m31p, pn)
                ent["pmra_no_cos"] = dict(p16=pn["p16"], word=gp.get("word"),
                                          strong_resid_plus_2s=gp["edges"]["strong"]["resid_plus_2s"])
            if r["host"] == "m31":
                gq = grade_dwarf(r, a0, m31m)
                ent["m31_minus_root"] = dict(word=gq.get("word"), strong_mode=gq["edges"]["strong_mode"],
                                             strong_resid_plus_2s=gq["edges"]["strong"]["resid_plus_2s"])
            sens.append(ent)
            say("SENS %s %s: %s" % (fk, r["name"], json.dumps(ent, default=jdef)), mut=True)
        mut["sensitivity"][fk] = sens
    with open(os.path.join(HERE, "rb2r_MUTATE.out"), "w") as f:
        f.write("\n".join(MUT_LINES) + "\n")
    with open(os.path.join(HERE, "rb2r_MUTATE.json"), "w") as f:
        json.dump(mut, f, indent=1, default=jdef)


if __name__ == "__main__":
    sys.exit(main())
