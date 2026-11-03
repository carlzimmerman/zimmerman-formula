"""DB1's rule: cluster baryonic dark matter (CBDM) as ordinary mass, sourcing the law like any baryon: g = law(g_b + g_cb).
Applied to hot-gas samples (cluster, group, xgroup); every other sample returns the law exactly. Arms P1, P1G, P2, P3, Z (lambda 0).
See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed. Reinstates nothing."""
import json, math, os
import numpy as np
from astropy.io import fits
G = 6.674e-11; MS = 1.989e30; KPC = 3.0857e19; PCm = 3.0857e16
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
XDIR = os.path.join(REPO, "real_research", "data", "xcop"); TDIR = os.path.join(REPO, "_external_data", "xcop_thermo_2026_11_02")
GROUPF = float(os.environ.get("DB1_GROUPF", "0.5")); TCOOL_GYR = float(os.environ.get("DB1_TCOOL_GYR", "13.97"))
HOT = ("cluster", "group", "xgroup")
LAM = None          # override for fitting: float or None (then read db1_lambda.json)
PERM = 0            # label control: cyclic shift of X-COP gas/star ratios (P1 only)
MP = 1.67262e-27; KEV = 1.602177e-16; KB = 1.380649e-23; YR = 3.15576e7
def law(g, a):
    g = np.asarray(g, float)
    with np.errstate(all="ignore"): return np.where(g > 0, 0.5 * g + np.sqrt(0.25 * g * g + a * g), g)
def I5(x, y): return x / -np.expm1(-np.sqrt(x / y))
def p3_gx(gb, gg, gs, a):
    """P3: the Newtonian CBDM field that makes law(g_b + g_cb) equal BK2's I5 row; floored at 0."""
    with np.errstate(all="ignore"):
        gi = I5(gb, a) * ((8 * math.pi / 3) * gg / np.sqrt(a * gb) + (gs / gb) ** 4)
        return np.maximum(gi * gi / (gi + a) - gb, 0.0)
def tcool_s(ne_cm3, kT_keV):
    """(3/2)(n_e + n_i) kT / (n_e n_H Lambda), Lambda = 3.0e-27 sqrt(T) erg cm^3/s, n_i 0.92 n_e, n_H 0.83 n_e (frozen)."""
    T = kT_keV * KEV / KB; kT_erg = kT_keV * KEV * 1e7
    return 1.5 * 1.92 * ne_cm3 * kT_erg / (0.83 * ne_cm3 ** 2 * 3.0e-27 * np.sqrt(T))
def rcool_from(r_kpc, ne, kT):
    """first radius from the centre outward where t_cool reaches TCOOL_GYR; 0 if the innermost point already exceeds it."""
    t = tcool_s(ne, kT) / YR / 1e9; over = t >= TCOOL_GYR
    if over[0]: return 0.0
    if not over.any(): return float(r_kpc[-1])
    i = int(np.argmax(over)); return float(np.exp(np.interp(math.log(TCOOL_GYR), [math.log(t[i - 1]), math.log(t[i])], [math.log(r_kpc[i - 1]), math.log(r_kpc[i])])))
_XT = {}
def xcop_table():
    """per X-COP cluster: r500 (m), M_gas, M_star at r500 (kg), M_gas(<r) profile, r_cool. Same files and interpolation as RQ3's rows_xcop."""
    if _XT: return _XT
    li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
    names = sorted(n for n in os.listdir(XDIR) if os.path.isdir(os.path.join(XDIR, n)))
    for name in names:
        p = os.path.join(XDIR, name)
        with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: r5 = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        rgas = np.asarray(ga["RADIUS"], float) * rg; mg = np.asarray(ga["MGAS"], float)
        ms5 = None
        if os.path.exists(os.path.join(p, f"{name}_mstar.fits")):
            with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
            ms5 = li(st["RADIUS"], st["MSTAR"], r5) * MS
        rc = np.nan
        tp = os.path.join(TDIR, name)
        if os.path.isdir(tp):
            with fits.open(os.path.join(tp, f"{name}_temperature.fits")) as h: X = h["XRAY"].data.copy(); R5T = float(h["XRAY"].header["R500"])
            with fits.open(os.path.join(tp, f"spectral_results_{name}.fits")) as h: Sp = h[1].data.copy()
            x = np.asarray(X["RW_X"], float); kT = np.asarray(Sp["KT"], float); o = np.argsort(x); x, kT = x[o], kT[o]
            rr = np.geomspace(max(rgas[0], 1.0), rgas[-1], 400); M = 10 ** np.interp(np.log10(rr), np.log10(rgas), np.log10(mg)); dM = np.gradient(M, rr)
            rho = dM * MS / (1e3 * PCm) / (4 * math.pi * (rr * 1e3 * PCm) ** 2); ne = rho / (1.17 * MP) / 1e6
            kTr = np.exp(np.interp(np.log(rr / R5T), np.log(x), np.log(kT)))
            rc = rcool_from(rr, ne, kTr)
        _XT[name] = dict(r5=r5 * 1e3 * PCm, mg5=li(rgas, mg, r5) * MS, ms5=ms5, rgas=rgas * 1e3 * PCm, mg=mg * MS, rcool=rc * 1e3 * PCm, rcool_x=rc / r5)
    return _XT
def rcool_ratio():
    v = [t["rcool_x"] for t in xcop_table().values() if np.isfinite(t["rcool_x"])]; return float(np.median(v))
def mgas_interp(t, r):
    r = np.maximum(np.asarray(r, float), t["rgas"][0]); return 10 ** np.interp(np.log10(r), np.log10(t["rgas"]), np.log10(t["mg"]))
def lookup(r5):
    T = xcop_table(); best = min(T, key=lambda n: abs(T[n]["r5"] / r5 - 1))
    if abs(T[best]["r5"] / r5 - 1) > 1e-6: raise KeyError("no X-COP cluster at this r500")
    return best
def nfw_shape(r, r500, c=2.9):
    R200 = 1.5 * r500; x = c * r / R200; x5 = c * r500 / R200; f = lambda u: np.log1p(u) - u / (1 + u)
    return f(x) / f(x5)
def lam(arm, a):
    if arm == "Z": return 0.0
    if LAM is not None: return float(LAM)
    if arm == "P3": return 1.0
    return json.load(open(os.path.join(HERE, "db1_lambda.json")))[arm]["canonical" if a < 1e-10 else "alt"]
def mcb_cluster(arm, L, r, gg, gs, r5, keys, a):
    """M_cb(<r) in kg for one cluster, r increasing."""
    Mg = gg * r * r / G
    if arm == "P1G": return L * Mg
    if keys:
        Mg5 = float(np.exp(np.interp(np.log(r5), np.log(r), np.log(np.maximum(Mg, 1e-300)))))
        if arm == "P1": return L * Mg5 * nfw_shape(r, r5)
        if arm == "P2":
            rc = rcool_ratio() * r5; Mgc = float(np.exp(np.interp(np.log(rc), np.log(r), np.log(np.maximum(Mg, 1e-300))))) if rc > 0 else 0.0
            return L * np.where(r < rc, Mg, Mgc)
    else:
        T = xcop_table(); names = sorted(n for n in T if T[n]["ms5"] is not None); n = lookup(r5)
        if arm == "P1":
            src = names[(names.index(n) + PERM) % len(names)] if PERM else n; ratio = T[src]["mg5"] / T[src]["ms5"]
            return L * ratio * T[n]["ms5"] * (gs * r * r / G) / T[n]["ms5"]
        if arm == "P2":
            rc = T[n]["rcool"]; Mgc = float(mgas_interp(T[n], rc)) if rc > 0 else 0.0
            return L * np.where(r < rc, Mg, Mgc)
    raise ValueError(arm)
def g(Q, arm):
    gb = np.asarray(dict.__getitem__(Q, "gb"), float); a = Q["a0"]; s = Q["sample"]
    if s not in HOT or arm == "Z": return law(gb, a)
    L = lam(arm, a); r = np.asarray(Q["r"], float) * np.ones_like(gb)
    if s == "group":
        gg, gs = GROUPF * gb, (1 - GROUPF) * gb
        if arm == "P2": return law(gb, a)
        gx = p3_gx(gb, gg, gs, a) if arm == "P3" else L * gg
        return law(gb + gx, a)
    gg = np.asarray(Q["gg"], float) * np.ones_like(gb); gs = np.asarray(Q["gs"], float) * np.ones_like(gb)
    if arm == "P3": return law(gb + p3_gx(gb, gg, gs, a), a)
    if s == "xgroup":
        return law(gb, a) if arm == "P2" else law(gb + L * gg, a)
    r5 = np.asarray(Q["r500"], float) * np.ones_like(gb); out = np.empty_like(gb); keys = dict.__contains__(Q, "S")
    for u in np.unique(r5):
        i = np.where(r5 == u)[0]; i = i[np.argsort(r[i], kind="stable")]
        Mcb = mcb_cluster(arm, L, r[i], gg[i], gs[i], float(u), keys, a)
        out[i] = law(gb[i] + G * Mcb / r[i] ** 2, a)
    return out
