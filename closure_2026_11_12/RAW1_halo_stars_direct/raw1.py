#!/usr/bin/env python3
"""
RAW1 -- the halo stars direct. DESI DR1 BHB stars, spherical Jeans, velocity-space comparison.
Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt), written before any data value was read; AMENDMENT_A1.md (alpha-fit window in observed r) after run 1 failed K6b; AMENDMENT_A2.md (exact re-maximisation of nuisance means) after run 2.
Usage: python3 -I raw1.py <path to MWS_BHB.fits>
Writes raw1.out (main), raw1_results.json, raw1_mut.out (mutations, separate).
Known-answer checks run first; the script stops before any label if one fails.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math
import numpy as np
from scipy.optimize import minimize, minimize_scalar, brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import raw1_model as MOD
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianRepresentation, CartesianDifferential
from astropy.coordinates.matrix_utilities import rotation_matrix

FITS = sys.argv[1]
K474 = 4.740470463
OUT = open(os.path.join(HERE, "raw1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 100); say(t); say("=" * 100)
FAIL = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAIL.append(name)
def stop_if_failed():
    if FAIL:
        say("\nKNOWN-ANSWER CHECK FAILED: " + ", ".join(FAIL) + ". Stopping before any label."); OUT.close(); sys.exit(2)

BINS = [(20.0, 30.0), (30.0, 40.0), (40.0, 55.0), (55.0, 80.0)]
NOMINAL = dict(clip=400.0, rfaint=18.9, rbright=16.2, R0=8.122, zsun=20.8, vsun=(12.9, 245.6, 7.78), sgr=15.0,
               dscale=1.0, dfrac=0.10)
FOOT = ("canonical", "alt")

# ------------------------------------------------------------------ Jeans machinery
SG = np.logspace(0.0, math.log10(2.0e4), 4000)  # kpc
def tracer_n(s, alpha):
    s = np.asarray(s, float)
    if np.isscalar(alpha) or np.ndim(alpha) == 0: return (s / 40.0) ** (-float(alpha))
    ai, ao = alpha; return np.where(s < 40.0, (s / 40.0) ** (-ai), (s / 40.0) ** (-ao))
_GCACHE = {}
def g_on_grid(model, footing=None, a0_mult=1.0):
    k = (model, footing, a0_mult)
    if k not in _GCACHE: _GCACHE[k] = MOD.g_model(SG, model, footing, a0_mult)
    return _GCACHE[k]
def sr2_profile(model, alpha, beta, footing=None, a0_mult=1.0):
    """sigma_r^2 (km/s)^2 on SG."""
    n = tracer_n(SG, alpha); w = n * SG ** (2 * beta) * g_on_grid(model, footing, a0_mult) * MOD.KPC  # g ds in m^2/s^2 per kpc
    seg = 0.5 * (w[1:] + w[:-1]) * np.diff(SG)
    cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    return cum / (n * SG ** (2 * beta)) / 1e6
def sr2_at(r, model, alpha, beta, footing=None, a0_mult=1.0):
    return np.exp(np.interp(np.log(r), np.log(SG), np.log(np.maximum(sr2_profile(model, alpha, beta, footing, a0_mult), 1e-30))))
def proj(sin2eta, beta): return 1.0 - beta * sin2eta

# ------------------------------------------------------------------ generic profile likelihood
def prof_interval(nll, lo, hi, x0=None):
    """nll(x) profiled negative log-likelihood; returns best, lower, upper (Delta = 0.5)."""
    res = minimize_scalar(nll, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6))
    xb, nb = res.x, res.fun
    def side(direction):
        step = max(abs(xb) * 0.02, 1e-3); x = xb
        for _ in range(200):
            xn = x + direction * step
            if (direction < 0 and xn < lo) or (direction > 0 and xn > hi): return (lo if direction < 0 else hi)
            if nll(xn) - nb > 0.5:
                return brentq(lambda t: nll(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-6)
            x = xn; step *= 1.3
        return lo if direction < 0 else hi
    return xb, side(-1), side(+1), nb

def fit_disp(v, e):
    def nll_s(s):
        var = s * s + e * e
        mu = np.sum(v / var) / np.sum(1 / var)
        return 0.5 * np.sum((v - mu) ** 2 / var + np.log(var))
    sb, slo, shi, _ = prof_interval(nll_s, 1.0, 400.0)
    var = sb * sb + e * e; mu = np.sum(v / var) / np.sum(1 / var)
    return dict(sigma=sb, lo=slo, hi=shi, mu=mu, n=int(len(v)))

def fit_f(v, e, P):
    def nll_f(f):
        var = f * f * P + e * e
        mu = np.sum(v / var) / np.sum(1 / var)   # one Newton step is exact for fixed var
        return 0.5 * np.sum((v - mu) ** 2 / var + np.log(var))
    fb, flo, fhi, _ = prof_interval(nll_f, 0.05, 5.0)
    return fb, 0.5 * (fhi - flo)

# ------------------------------------------------------------------ geometry
def sgr_matrix():
    D = rotation_matrix((180 + 3.75) * u.deg, "z"); C = rotation_matrix((90 - 13.46) * u.deg, "x")
    B = rotation_matrix((180 + 14.111534) * u.deg, "z"); A = np.diag([1., 1., -1.])
    return A @ B @ C @ D
def sgr_lat_lon(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    x = np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])
    xs = sgr_matrix() @ x
    return np.degrees(np.arctan2(xs[1], xs[0])) % 360.0, np.degrees(np.arcsin(np.clip(xs[2], -1, 1)))

def frame_affine(R0, zsun):
    gc = Galactocentric(galcen_distance=R0 * u.kpc, z_sun=zsun * u.pc, galcen_v_sun=CartesianDifferential([0, 0, 0] * u.km / u.s))
    def tr(xyz):
        c = SkyCoord(CartesianRepresentation(np.asarray(xyz, float).T * u.kpc), frame="icrs").transform_to(gc)
        return np.vstack([c.x.to_value(u.kpc), c.y.to_value(u.kpc), c.z.to_value(u.kpc)]).T
    p0 = tr(np.zeros((1, 3)))[0]
    Rm = (tr(np.eye(3)) - p0).T   # columns: images of ICRS unit vectors
    return p0, Rm

# ------------------------------------------------------------------ data
def load():
    h = fits.open(FITS, memmap=False)
    rv, fm, ga = h["RVTAB"].data, h["FIBERMAP"].data, h["GAIA"].data
    D = dict(tid=np.asarray(rv["TARGETID"]), tid_fm=np.asarray(fm["TARGETID"]), primary=np.asarray(rv["PRIMARY"]).astype(bool),
             vrad=np.asarray(rv["VRAD"], float), verr=np.asarray(rv["VRAD_ERR"], float),
             ra=np.asarray(rv["TARGET_RA"], float), dec=np.asarray(rv["TARGET_DEC"], float),
             dist=np.asarray(fm["DIST"], float), g=np.asarray(fm["MAG_DERED_G"], float), Mg=np.asarray(fm["ABS_MAG_G"], float),
             ref_id=np.asarray(fm["REF_ID"]), mwst=np.asarray(fm["MWS_TARGET"]), survey=np.char.strip(np.asarray(rv["SURVEY"]).astype(str)),
             robs=22.5 - 2.5 * np.log10(np.clip(np.asarray(fm["FLUX_R"], float), 1e-12, None)), sid=np.asarray(ga["SOURCE_ID"]),
             pmra=np.asarray(ga["PMRA"], float), pmdec=np.asarray(ga["PMDEC"], float),
             epmra=np.asarray(ga["PMRA_ERROR"], float), epmdec=np.asarray(ga["PMDEC_ERROR"], float),
             rho=np.asarray(ga["PMRA_PMDEC_CORR"], float), ruwe=np.asarray(ga["RUWE"], float))
    return D

def build(D, cfg, override=None):
    """Apply S1-S6; return dict of per-star arrays. override: dict of replacement arrays (synthetic)."""
    m = D["primary"] & np.isfinite(D["vrad"]) & (D["verr"] > 0) & (D["dist"] > 0) & np.isfinite(D["g"]) & np.isfinite(D["Mg"])
    idx = np.where(m)[0]
    ra, dec = np.radians(D["ra"][idx]), np.radians(D["dec"][idx])
    d = D["dist"][idx] * cfg["dscale"]
    if override is not None and "dist" in override: d = override["dist"]
    p0, Rm = frame_affine(cfg["R0"], cfg["zsun"])
    n = np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T
    ea = np.vstack([-np.sin(ra), np.cos(ra), np.zeros_like(ra)]).T
    no = np.vstack([-np.sin(dec) * np.cos(ra), -np.sin(dec) * np.sin(ra), np.cos(dec)]).T
    n, ea, no = n @ Rm.T, ea @ Rm.T, no @ Rm.T
    pos = p0 + d[:, None] * n; r = np.linalg.norm(pos, axis=1); rh = pos / r[:, None]
    vs = np.array(cfg["vsun"])
    vrad = D["vrad"][idx] if override is None or "vrad" not in override else override["vrad"]
    vgsr = vrad + n @ vs
    c = SkyCoord(ra=D["ra"][idx] * u.deg, dec=D["dec"][idx] * u.deg, frame="icrs").galactic
    lam, bet = sgr_lat_lon(c.l.deg, c.b.deg)
    keep = (np.abs(bet) >= cfg["sgr"]) & (r >= 20.0) & (r < 80.0)
    if cfg["clip"] is not None: keep &= np.abs(vgsr) <= cfg["clip"]
    k = np.where(keep)[0]
    cos_eta = np.sum(n * rh, axis=1)
    S = dict(i=idx[k], d=d[k], r=r[k], pos=pos[k], n=n[k], ea=ea[k], no=no[k], rh=rh[k], vgsr=vgsr[k], verr=D["verr"][idx][k],
             sin2=1 - cos_eta[k] ** 2, cos_eta=cos_eta[k], g=D["g"][idx][k], p0=p0, vs=vs)
    # proper motions
    pmra = D["pmra"][idx]; pmdec = D["pmdec"][idx]
    if override is not None and "pmra" in override: pmra, pmdec = override["pmra"], override["pmdec"]
    okpm = (D["sid"][idx] > 0) & np.isfinite(pmra) & np.isfinite(pmdec) & np.isfinite(D["epmra"][idx]) & np.isfinite(D["epmdec"][idx]) \
           & (D["ruwe"][idx] < 1.4) & (D["sid"][idx] == D["ref_id"][idx])
    S.update(pmok=okpm[k], pmra=pmra[k], pmdec=pmdec[k], epmra=D["epmra"][idx][k], epmdec=D["epmdec"][idx][k],
             rho=np.nan_to_num(D["rho"][idx][k]))
    # magnitude windows for the alpha fit
    S["robs"] = D["robs"][idx][k]   # amendment A1.1: observed r, MWS-targeted main-survey stars only
    S["win_ok"] = (D["survey"][idx][k] == "main") & (D["mwst"][idx][k] != 0) & (S["robs"] >= cfg["rbright"]) & (S["robs"] <= cfg["rfaint"])
    return S

def windows(S, cfg):
    d = S["d"]; ro = S["robs"]
    dlo = d * 10 ** ((cfg["rbright"] - ro) / 5); dhi = d * 10 ** ((cfg["rfaint"] - ro) / 5)
    p0 = S["p0"]; pn = S["n"] @ p0; p2 = p0 @ p0
    root = lambda R: -pn + np.sqrt(pn ** 2 - p2 + R * R)   # positive root of |p0 + d n| = R (|p0| < R)
    return np.maximum(dlo, root(20.0)), np.minimum(dhi, root(80.0))

# ------------------------------------------------------------------ alpha
NGRID = 400
def alpha_setup(S, cfg):
    w = S["win_ok"]; a, b = windows(S, cfg); a, b = a[w], b[w]
    t = np.linspace(0, 1, NGRID)
    dg = np.exp(np.log(a)[:, None] + (np.log(b) - np.log(a))[:, None] * t[None, :])
    n = S["n"][w]; p0 = S["p0"]
    rg = np.sqrt(np.sum((p0[None, None, :] + dg[:, :, None] * n[:, None, :]) ** 2, axis=2))
    return dict(dg=dg, rg=rg, r=S["r"][w], d=S["d"][w], N=int(w.sum()))
def alpha_nll(A, alpha):
    lnr = np.log(A["r"] / 40.0); lnrg = np.log(A["rg"] / 40.0)
    if np.ndim(alpha) == 0:
        ln_n, ln_ng = -alpha * lnr, -alpha * lnrg
    else:
        ai, ao = alpha
        ln_n = np.where(A["r"] < 40, -ai * lnr, -ao * lnr); ln_ng = np.where(A["rg"] < 40, -ai * lnrg, -ao * lnrg)
    # integrand d^2 n(r) dd = d^3 n d(ln d)
    lw = 3 * np.log(A["dg"]) + ln_ng; mx = lw.max(axis=1)
    dl = np.log(A["dg"][:, 1] / A["dg"][:, 0])
    ww = np.exp(lw - mx[:, None]); Z = (np.sum(ww, axis=1) - 0.5 * (ww[:, 0] + ww[:, -1])) * dl
    return -np.sum(2 * np.log(A["d"]) + ln_n - (np.log(Z) + mx))
def fit_alpha(A):
    ab, alo, ahi, _ = prof_interval(lambda a: alpha_nll(A, a), -2.0, 12.0)
    return dict(alpha=ab, lo=alo, hi=ahi, sig=0.5 * (ahi - alo), N=A["N"])
def fit_alpha2(A):
    f = lambda p: alpha_nll(A, (p[0], p[1]))
    res = minimize(f, [3.5, 4.5], method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-6, maxiter=4000))
    p = res.x; h = 1e-2; H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            ei = np.eye(2)[i] * h; ej = np.eye(2)[j] * h
            H[i, j] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * h * h)
    C = np.linalg.inv(H)
    return dict(ain=p[0], aout=p[1], sin=math.sqrt(C[0, 0]), sout=math.sqrt(C[1, 1]), corr=C[0, 1] / math.sqrt(C[0, 0] * C[1, 1]))

# ------------------------------------------------------------------ beta from proper motions
def pm_arrays(S, sel, dfrac):
    d = S["d"][sel]; vs = S["vs"]
    w = np.vstack([S["vgsr"][sel], K474 * d * S["pmra"][sel] + S["ea"][sel] @ vs, K474 * d * S["pmdec"][sel] + S["no"][sel] @ vs]).T
    E = np.zeros((len(d), 3, 3)); E[:, 0, 0] = S["verr"][sel] ** 2
    sa, sd = K474 * d * S["epmra"][sel], K474 * d * S["epmdec"][sel]
    vta, vtd = K474 * d * S["pmra"][sel], K474 * d * S["pmdec"][sel]
    E[:, 1, 1] = sa ** 2 + (dfrac * vta) ** 2; E[:, 2, 2] = sd ** 2 + (dfrac * vtd) ** 2
    E[:, 1, 2] = E[:, 2, 1] = S["rho"][sel] * sa * sd
    rh = S["rh"][sel]; pos = S["pos"][sel]
    Rc = np.hypot(pos[:, 0], pos[:, 1]); ph = np.vstack([-pos[:, 1] / Rc, pos[:, 0] / Rc, np.zeros(len(d))]).T
    Q = np.stack([S["n"][sel], S["ea"][sel], S["no"][sel]], axis=1)
    q = np.einsum("nij,nj->ni", Q, rh); qp = np.einsum("nij,nj->ni", Q, ph)
    return dict(w=w, E=E, q=q, qp=qp, terr=np.sqrt(0.5 * (sa ** 2 + sd ** 2)))
def beta_nll(P, ln_sr, beta, vphi=None):
    """vphi=None: vphi_bar re-maximised exactly (the mean is linear in vphi; amendment A2 bug fix)."""
    sr2 = math.exp(2 * ln_sr); st2 = (1 - beta) * sr2
    C = P["E"] + st2 * np.eye(3)[None] + (sr2 - st2) * P["q"][:, :, None] * P["q"][:, None, :]
    sign, ld = np.linalg.slogdet(C)
    if np.any(sign <= 0): return 1e30
    Cw = np.linalg.solve(C, P["w"][:, :, None])[:, :, 0]; Cq = np.linalg.solve(C, P["qp"][:, :, None])[:, :, 0]
    if vphi is None: vphi = np.sum(P["qp"] * Cw) / np.sum(P["qp"] * Cq)
    x = P["w"] - vphi * P["qp"]; sol = Cw - vphi * Cq
    return 0.5 * np.sum(np.sum(x * sol, axis=1) + ld)
def fit_beta(P):
    def prof(beta):
        r = minimize_scalar(lambda t: beta_nll(P, t, beta), bounds=(math.log(20.0), math.log(600.0)), method="bounded",
                            options=dict(xatol=1e-7))
        return r.fun
    bb, blo, bhi, _ = prof_interval(prof, -3.0, 0.99)
    return dict(beta=bb, lo=blo, hi=bhi, sig=0.5 * (bhi - blo), N=int(len(P["w"])))

# ------------------------------------------------------------------ one full measurement
def bin_index(r):
    return np.array([next((j for j, (a, b) in enumerate(BINS) if a <= x < b), -1) for x in r])
def merged_bins(S):
    edges = [BINS[0][0]] + [b for a, b in BINS]
    while True:
        cnt = [int(np.sum((S["r"] >= edges[j]) & (S["r"] < edges[j + 1]))) for j in range(len(edges) - 1)]
        small = [j for j, c in enumerate(cnt) if c < 30]
        if not small or len(edges) == 2: return [(edges[j], edges[j + 1]) for j in range(len(edges) - 1)], cnt
        j = small[0]; edges.pop(j if j > 0 else 1)

def measure(S, cfg, beta_fixed=None, quiet=False):
    bins, cnt = merged_bins(S)
    bsel = [(S["r"] >= a) & (S["r"] < b) for a, b in bins]
    disp = [fit_disp(S["vgsr"][m], S["verr"][m]) for m in bsel]
    A = alpha_setup(S, cfg); al = fit_alpha(A); al2 = fit_alpha2(A)
    # beta
    pmb = []
    for m, dp in zip(bsel, disp):
        sel = m & S["pmok"]
        if sel.sum() < 30: pmb.append(dict(N=int(sel.sum()), usable=False, why="fewer than 30 with PM")); continue
        P = pm_arrays(S, sel, cfg["dfrac"]); med = float(np.median(P["terr"]))
        if med > dp["sigma"]: pmb.append(dict(N=int(sel.sum()), usable=False, med_terr=med, why="PM error > LOS dispersion")); continue
        fb = fit_beta(P); fb.update(med_terr=med, usable=fb["sig"] <= 0.3, why="" if fb["sig"] <= 0.3 else "beta error > 0.3")
        pmb.append(fb)
    usable = [p.get("usable", False) for p in pmb]
    if beta_fixed is not None:
        beta, sbeta, glob = beta_fixed, 0.0, None
    elif any(usable):
        sel = np.zeros(len(S["r"]), bool)
        for m, us in zip(bsel, usable):
            if us: sel |= m
        glob = fit_beta(pm_arrays(S, sel & S["pmok"], cfg["dfrac"])); beta, sbeta = glob["beta"], glob["sig"]
    else:
        beta, sbeta, glob = 0.5, 0.3, None
    brange = []
    for us in usable:
        if beta_fixed is not None: brange.append((beta, beta))
        elif us: brange.append((beta - sbeta, beta + sbeta))
        else: brange.append((0.2, 0.8))
    return dict(bins=bins, counts=cnt, bsel=bsel, disp=disp, alpha=al, alpha2=al2, pmbeta=pmb, usable=usable,
                beta=beta, sbeta=sbeta, beta_glob=glob, brange=brange)

def f_bins(S, R, model, alpha, beta, footing=None, a0_mult=1.0):
    out = []
    for m in R["bsel"]:
        P = sr2_at(S["r"][m], model, alpha, beta, footing, a0_mult) * proj(S["sin2"][m], beta)
        out.append(fit_f(S["vgsr"][m], S["verr"][m], P))
    return out
def f_full(S, R, model, footing=None, a0_mult=1.0):
    """nominal f, stat sigma, propagated sigma, and the variant f values for fragility."""
    a, sa = R["alpha"]["alpha"], R["alpha"]["sig"]; b = R["beta"]
    nom = f_bins(S, R, model, a, b, footing, a0_mult)
    fa_lo = f_bins(S, R, model, a - sa, b, footing, a0_mult); fa_hi = f_bins(S, R, model, a + sa, b, footing, a0_mult)
    bvals = sorted({x for br in R["brange"] for x in br})
    fb = {bv: f_bins(S, R, model, a, bv, footing, a0_mult) for bv in bvals}
    rows = []
    for j, (f, s) in enumerate(nom):
        blo, bhi = R["brange"][j]
        da = 0.5 * abs(fa_hi[j][0] - fa_lo[j][0]); db = 0.5 * abs(fb[bhi][j][0] - fb[blo][j][0])
        rows.append(dict(f=f, s_stat=s, s_alpha=da, s_beta=db, s=math.sqrt(s * s + da * da + db * db),
                         f_alo=fa_lo[j][0], f_ahi=fa_hi[j][0], f_blo=fb[blo][j][0], f_bhi=fb[bhi][j][0]))
    a2 = (R["alpha2"]["ain"], R["alpha2"]["aout"])
    f2 = f_bins(S, R, model, a2, b, footing, a0_mult)
    for j in range(len(rows)): rows[j]["f_two"] = f2[j][0]
    return rows

def grade(fs, ss, names):
    cold = [nm for f, s, nm in zip(fs, ss, names) if f < 1 - 2 * s]
    hot = [nm for f, s, nm in zip(fs, ss, names) if f > 1 + 2 * s]
    if not cold and not hot: return "PASSES", []
    if cold and hot: return "FAILS COLD AND HOT", cold + hot
    return ("FAILS COLD", cold) if cold else ("FAILS HOT", hot)

# ------------------------------------------------------------------ direct Jeans mass
def fit_sr_law(S, beta):
    v, e, r, s2 = S["vgsr"], S["verr"], S["r"], S["sin2"]; pj = proj(s2, beta)
    def nll(q):   # mu re-maximised exactly (amendment A2 bug fix)
        ls0, gam = q; var = math.exp(ls0) * (r / 40.0) ** (-gam) * pj + e * e
        mu = np.sum(v / var) / np.sum(1 / var)
        return 0.5 * np.sum((v - mu) ** 2 / var + np.log(var))
    x0 = np.array([math.log(100.0 ** 2), 0.3])
    res = minimize(nll, x0, method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-8, maxiter=4000,
                   initial_simplex=np.array([x0, x0 + [0.3, 0.0], x0 + [0.0, 0.3]])))
    ls0, gam = res.x; var = math.exp(ls0) * (r / 40.0) ** (-gam) * pj + e * e
    return np.array([np.sum(v / var) / np.sum(1 / var), ls0, gam])
def jeans_mass(alpha, beta, p, r):
    sr2 = math.exp(p[1]) * (r / 40.0) ** (-p[2]) * 1e6
    return r * MOD.KPC * sr2 * (alpha + p[2] - 2 * beta) / MOD.G / MOD.MSUN / 1e11
def direct_mass(S, R, cfg, nboot=300, seed=20261112):
    a = R["alpha"]["alpha"]; b = R["beta"]; p = fit_sr_law(S, b)
    M = {r: jeans_mass(a, b, p, r) for r in (30.0, 50.0)}
    rng = np.random.default_rng(seed); N = len(S["r"]); boot = {30.0: [], 50.0: []}
    for _ in range(nboot):
        ii = rng.integers(0, N, N); Sb = {k: (v[ii] if isinstance(v, np.ndarray) and v.ndim >= 1 and len(v) == N else v) for k, v in S.items()}
        ab = fit_alpha(alpha_setup(Sb, cfg))["alpha"]; pb = fit_sr_law(Sb, b)
        for r in boot: boot[r].append(jeans_mass(ab, b, pb, r))
    out = {}
    for r in M:
        lo, hi = np.percentile(boot[r], [16, 84])
        if R["sbeta"] > 0:
            pl = fit_sr_law(S, b - R["sbeta"]); ph = fit_sr_law(S, b + R["sbeta"])
            db = 0.5 * abs(jeans_mass(a, b + R["sbeta"], ph, r) - jeans_mass(a, b - R["sbeta"], pl, r))
        else: db = 0.0
        out[r] = dict(M=M[r], boot_lo=M[r] - lo, boot_hi=hi - M[r], dbeta=db,
                      lo=math.hypot(M[r] - lo, db), hi=math.hypot(hi - M[r], db))
    return dict(p=list(map(float, p)), M=out)

# ================================================================== K2-K5: no data
sec("RAW1 known-answer checks without data (K2-K5)")
eta = math.radians(60.0)
check("K2a beta=0", abs(proj(math.sin(eta) ** 2, 0.0) - 1.0) < 1e-12, "P/sr^2 = 1 at any eta")
check("K2b beta=1", abs(proj(math.sin(eta) ** 2, 1.0) - math.cos(eta) ** 2) < 1e-12, "P/sr^2 = cos^2 eta")
rng = np.random.default_rng(1); NMC = 10 ** 6; sr = 1.0; st = math.sqrt(0.5)
vlos = rng.normal(0, sr, NMC) * math.cos(eta) + rng.normal(0, st, NMC) * math.sin(eta)
check("K2c Monte Carlo", abs(np.var(vlos) / proj(math.sin(eta) ** 2, 0.5) - 1) < 0.01, f"var {np.var(vlos):.4f} vs {proj(math.sin(eta)**2, 0.5):.4f}")
for (a, b) in ((4.5, 0.5), (3.5, 0.0), (4.0, 0.8)):
    vals = sr2_at(np.array([20.0, 40.0, 80.0]), "flat200", a, b); exact = 200.0 ** 2 / (a - 2 * b)
    check(f"K3 flat Jeans a={a} b={b}", np.all(np.abs(vals / exact - 1) < 0.005), f"{np.round(vals, 1)} vs {exact:.1f}")
for f, ref in (("canonical", 5.691), ("alt", 6.219)):
    Mb = MOD.M_sph(80.0); gb = MOD.G * Mb / (80 * MOD.KPC) ** 2; Ml = float(MOD.nu_fw(gb / MOD.A0[f])) * Mb / MOD.MSUN / 1e11
    check(f"K4 FW census 80 kpc {f}", abs(Ml / ref - 1) < 1e-3, f"{Ml:.4f} vs {ref}")
Msi = 50 * 3.0857e19 * (2.0e5) ** 2 / 6.674e-11 / 1.989e30
check("K4 SI r V^2/G", abs(Msi / 4.65e11 - 1) < 0.005, f"{Msi:.4e} Msun")
lam, bet = sgr_lat_lon(np.array([5.569]), np.array([-14.166]))
check("K5 Sgr core", (min(lam[0], 360 - lam[0]) < 2) and abs(bet[0]) < 2, f"Lambda {lam[0]:.2f} B {bet[0]:.2f}")
stop_if_failed()

# ================================================================== data, K6
sec("Data and K6 (magnitudes and identifiers only)")
D = load()
check("K6a TARGETID RVTAB == FIBERMAP", bool(np.all(D["tid"] == D["tid_fm"])), f"{len(D['tid'])} rows")
m12 = D["primary"] & np.isfinite(D["vrad"]) & (D["verr"] > 0) & (D["dist"] > 0) & np.isfinite(D["g"]) & np.isfinite(D["Mg"])
outside = np.mean((D["g"][m12] < 15.9) | (D["g"][m12] > 20.1))
say(f"  [INFO] frozen K6b (failed in run 1, superseded by A1.3): fraction of S1-S2 stars with dereddened g outside [15.9, 20.1] = {outside:.4f}")
mw = m12 & (D["survey"] == "main") & (D["mwst"] != 0)
lo_frac = np.mean(D["robs"][mw & (D["robs"] < 19.0)] < 15.95); hi_frac = np.mean(D["robs"][mw] > 20.3)
check("K6b' (A1.3) r window", lo_frac < 0.01 and hi_frac < 0.01, f"{mw.sum()} MWS-targeted main stars; below 15.95: {lo_frac:.4f}; above 20.3: {hi_frac:.4f}")
dcalc = 10 ** ((D["g"][m12] - D["Mg"][m12] + 5) / 5) / 1000
agree = np.mean(np.abs(dcalc / D["dist"][m12] - 1) < 0.01)
say(f"  [INFO] K6c DIST vs 10^((g - M_g + 5)/5): fraction within 1 per cent = {agree:.4f} (median ratio {np.median(dcalc / D['dist'][m12]):.4f})")
gaia_match = np.mean(D["sid"][m12 & (D["sid"] > 0)] == D["ref_id"][m12 & (D["sid"] > 0)])
say(f"  [INFO] GAIA SOURCE_ID == FIBERMAP REF_ID for {gaia_match:.4f} of rows with a Gaia match (mismatches dropped from the PM fit)")
stop_if_failed()

# ================================================================== K1 synthetic
sec("K1 synthetic sample at the real positions (flat 200 km/s, alpha 4.5, beta 0.5)")
cfg = dict(NOMINAL)
S0 = build(D, cfg)
rng = np.random.default_rng(12345)
m12i = np.where(m12)[0]; pos_in_m12 = {ix: j for j, ix in enumerate(m12i)}
sr_true = math.sqrt(200.0 ** 2 / 3.5); st_true = math.sqrt(0.5) * sr_true
# velocities for every S1-S2 star (positions real), then re-run S3-S6
ra, dec = np.radians(D["ra"][m12i]), np.radians(D["dec"][m12i]); dd = D["dist"][m12i]
p0, Rm = frame_affine(cfg["R0"], cfg["zsun"])
nn = np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T @ Rm.T
ee = np.vstack([-np.sin(ra), np.cos(ra), np.zeros_like(ra)]).T @ Rm.T
no_ = np.vstack([-np.sin(dec) * np.cos(ra), -np.sin(dec) * np.sin(ra), np.cos(dec)]).T @ Rm.T
pos = p0 + dd[:, None] * nn; rr = np.linalg.norm(pos, axis=1); rh = pos / rr[:, None]
Rc = np.hypot(pos[:, 0], pos[:, 1]); ph = np.vstack([-pos[:, 1] / Rc, pos[:, 0] / Rc, np.zeros(len(rr))]).T
th = np.cross(ph, rh)
vgc = rng.normal(0, sr_true, len(rr))[:, None] * rh + rng.normal(0, st_true, len(rr))[:, None] * th + rng.normal(0, st_true, len(rr))[:, None] * ph
vs = np.array(cfg["vsun"]); vh = vgc - vs
syn_vrad = np.sum(vh * nn, axis=1) + rng.normal(0, 1, len(rr)) * D["verr"][m12i]
dist_err = 1 + cfg["dfrac"] * rng.normal(0, 1, len(rr))
vta = np.sum(vh * ee, axis=1) * dist_err; vtd = np.sum(vh * no_, axis=1) * dist_err
epa = np.nan_to_num(D["epmra"][m12i], nan=1.0); epd = np.nan_to_num(D["epmdec"][m12i], nan=1.0); rho = np.nan_to_num(D["rho"][m12i])
z1 = rng.normal(0, 1, len(rr)); z2 = rng.normal(0, 1, len(rr))
syn_pmra = vta / (K474 * dd) + epa * z1; syn_pmdec = vtd / (K474 * dd) + epd * (rho * z1 + np.sqrt(1 - rho ** 2) * z2)
Ssyn = build(D, cfg, override=dict(vrad=syn_vrad, pmra=syn_pmra, pmdec=syn_pmdec))
# synthetic distances for the alpha fit: draw d from p(d|dir) with alpha 4.5 inside each window-star's window
Asyn = alpha_setup(Ssyn, cfg)
lw = 3 * np.log(Asyn["dg"]) - 4.5 * np.log(Asyn["rg"] / 40.0); wts = np.exp(lw - lw.max(axis=1)[:, None])
cdf = np.cumsum(wts, axis=1); cdf /= cdf[:, -1:]
uu = rng.random(len(cdf)); jj = np.array([np.searchsorted(c, x) for c, x in zip(cdf, uu)]).clip(0, NGRID - 1)
Asyn_d = dict(Asyn); Asyn_d["d"] = Asyn["dg"][np.arange(len(jj)), jj]; Asyn_d["r"] = Asyn["rg"][np.arange(len(jj)), jj]
asyn = fit_alpha(Asyn_d)
check("K1 alpha recovered", abs(asyn["alpha"] - 4.5) <= 2 * asyn["sig"], f"alpha = {asyn['alpha']:.3f} +/- {asyn['sig']:.3f} (N {asyn['N']})")
Rsyn = measure(Ssyn, cfg)
Rsyn["alpha"] = asyn   # end to end: the recovered alpha
if Rsyn["beta_glob"] is not None:
    check("K1 beta recovered", abs(Rsyn["beta"] - 0.5) <= 2 * Rsyn["sbeta"], f"beta = {Rsyn['beta']:.3f} +/- {Rsyn['sbeta']:.3f}; usable bins {Rsyn['usable']}")
else:
    say(f"  [INFO] K1: no usable PM bin in the synthetic sample; beta bracket used")
fsyn = f_full(Ssyn, Rsyn, "flat200")
for (a, b), row in zip(Rsyn["bins"], fsyn):
    check(f"K1 f bin {a:.0f}-{b:.0f}", abs(row["f"] - 1) <= 2 * row["s"], f"f = {row['f']:.3f} +/- {row['s']:.3f} (stat {row['s_stat']:.3f}, alpha {row['s_alpha']:.3f}, beta {row['s_beta']:.3f})")
stop_if_failed()

# ================================================================== the measurement
def full_run(cfg, tag, beta_fixed=None, do_mass=True, quiet=False):
    S = build(D, cfg); R = measure(S, cfg, beta_fixed=beta_fixed)
    res = dict(tag=tag, N=int(len(S["r"])), bins=R["bins"], counts=R["counts"], alpha=R["alpha"], alpha2=R["alpha2"],
               beta=R["beta"], sbeta=R["sbeta"], usable=R["usable"], brange=R["brange"], disp=R["disp"], pmbeta=R["pmbeta"],
               npm=int(S["pmok"].sum()), f={})
    for model in ("FW_census", "FW_rc"):
        for ft in FOOT: res["f"][f"{model}/{ft}"] = f_full(S, R, model, ft)
    res["f"]["N"] = f_full(S, R, "N"); res["f"]["H"] = f_full(S, R, "H")
    if do_mass: res["mass"] = direct_mass(S, R, cfg, nboot=300 if tag == "nominal" else 60)
    return S, R, res

sec("Nominal measurement")
S, R, NOM = full_run(dict(NOMINAL), "nominal")
names = [f"{a:.0f}-{b:.0f}" for a, b in NOM["bins"]]
say(f"Stars after S1-S6: {NOM['N']}; per bin {NOM['counts']} (bins {NOM['bins']}); with usable PM {NOM['npm']}")
say(f"alpha (single, 20-80): {NOM['alpha']['alpha']:.3f} [{NOM['alpha']['lo']:.3f}, {NOM['alpha']['hi']:.3f}] from {NOM['alpha']['N']} stars in the g window")
say(f"alpha two-slope: in {NOM['alpha2']['ain']:.3f} +/- {NOM['alpha2']['sin']:.3f}, out {NOM['alpha2']['aout']:.3f} +/- {NOM['alpha2']['sout']:.3f} (corr {NOM['alpha2']['corr']:.2f})")
for nm, dp, pb in zip(names, NOM["disp"], NOM["pmbeta"]):
    bt = f"beta {pb['beta']:.3f} [{pb['lo']:.3f}, {pb['hi']:.3f}]" if "beta" in pb else "beta not fitted"
    say(f"  bin {nm}: N {dp['n']}, sigma_los {dp['sigma']:.2f} [{dp['lo']:.2f}, {dp['hi']:.2f}] km/s, mean {dp['mu']:.1f}; PM N {pb['N']}, "
        f"median t-err {pb.get('med_terr', float('nan')):.1f}; {bt}; usable {pb.get('usable', False)} {pb.get('why', '')}")
say(f"beta nominal {NOM['beta']:.3f} +/- {NOM['sbeta']:.3f}; per-bin ranges {[(round(a, 3), round(b, 3)) for a, b in NOM['brange']]}")

sec("Scale factors f = observed / predicted dispersion (nominal), and labels")
LABELS = {}
for key, rows in NOM["f"].items():
    fs = [x["f"] for x in rows]; ss = [x["s"] for x in rows]
    lab, bad = grade(fs, ss, names)
    say(f"{key:16s} " + "  ".join(f"{nm}: {x['f']:.3f}+/-{x['s']:.3f}" for nm, x in zip(names, rows)) + f"   -> {lab} {bad}")
    LABELS[key] = dict(label=lab, bins=bad)

sec("Fragility variants (graded with the nominal sigma_f)")
_, _, WIN2 = full_run(dict(NOMINAL, rfaint=19.9), "r window 19.9", do_mass=True)
say(f"  A1.2 window r [16.2, 19.9]: alpha {WIN2['alpha']['alpha']:.3f} +/- {WIN2['alpha']['sig']:.3f} (N {WIN2['alpha']['N']}); two-slope in {WIN2['alpha2']['ain']:.3f}+/-{WIN2['alpha2']['sin']:.3f} out {WIN2['alpha2']['aout']:.3f}+/-{WIN2['alpha2']['sout']:.3f}; M30 {WIN2['mass']['M'][30.0]['M']:.3f} M50 {WIN2['mass']['M'][50.0]['M']:.3f}")
CLIPV = {}
for cv in (350.0, 500.0, None):
    _, _, CLIPV[str(cv)] = full_run(dict(NOMINAL, clip=cv), f"clip {cv}", do_mass=False)
for key in [k for k in NOM["f"] if k.startswith("FW")]:
    rows = NOM["f"][key]; ss = [x["s"] for x in rows]; base = LABELS[key]["label"]; vlabs = {}
    vlabs["alpha lo"] = grade([x["f_alo"] for x in rows], ss, names)[0]
    vlabs["alpha hi"] = grade([x["f_ahi"] for x in rows], ss, names)[0]
    vlabs["beta lo"] = grade([x["f_blo"] for x in rows], ss, names)[0]
    vlabs["beta hi"] = grade([x["f_bhi"] for x in rows], ss, names)[0]
    vlabs["two-slope"] = grade([x["f_two"] for x in rows], ss, names)[0]
    vlabs["r window 19.9 (A1.2)"] = grade([x["f"] for x in WIN2["f"][key]], ss, names)[0]
    for cv, rr_ in CLIPV.items():
        if rr_["bins"] == NOM["bins"]: vlabs[f"clip {cv}"] = grade([x["f"] for x in rr_["f"][key]], ss, names)[0]
        else: vlabs[f"clip {cv}"] = grade([x["f"] for x in rr_["f"][key]], [x["s"] for x in rr_["f"][key]], [f"{a:.0f}-{b:.0f}" for a, b in rr_["bins"]])[0]
    changed = {k: v for k, v in vlabs.items() if v != base}
    LABELS[key]["fragile"] = bool(changed); LABELS[key]["variants"] = vlabs
    say(f"{key:16s} base {base}; " + "; ".join(f"{k}: {v}" for k, v in vlabs.items()) + ("  -> FRAGILE" if changed else "  -> robust"))
for cv, rr_ in CLIPV.items():
    say(f"  clip {cv}: N {rr_['N']}, alpha {rr_['alpha']['alpha']:.3f}, beta {rr_['beta']:.3f}, sigma_los " + ", ".join(f"{d['sigma']:.1f}" for d in rr_["disp"]))

sec("Direct Jeans enclosed mass (no calibration), 1e11 Msun")
p = NOM["mass"]["p"]
say(f"sr^2 law: s0 = {math.exp(p[1]):.0f} (km/s)^2 at 40 kpc (sr {math.sqrt(math.exp(p[1])):.1f} km/s), gamma_s = {p[2]:.3f}, mean {p[0]:.1f} km/s; alpha {NOM['alpha']['alpha']:.3f}, beta {NOM['beta']:.3f}")
DESI = {30.0: (2.65, 0.13, 0.14), 50.0: (4.51, 0.26, 0.27)}
for r, mm in NOM["mass"]["M"].items():
    fw = {f"{mdl}/{ft}": float(MOD.M_of_g(MOD.g_model(r, mdl, ft), r)) / 1e11 for mdl in ("FW_census", "FW_rc") for ft in FOOT}
    say(f"  r = {r:.0f} kpc: M = {mm['M']:.3f} -{mm['lo']:.3f} +{mm['hi']:.3f} (bootstrap -{mm['boot_lo']:.3f} +{mm['boot_hi']:.3f}, beta +-{mm['dbeta']:.3f});"
        f" DESI joint {DESI[r][0]} -{DESI[r][1]} +{DESI[r][2]}; FW " + ", ".join(f"{k} {v:.3f}" for k, v in fw.items()))

# ================================================================== reported variations (assumption list)
sec("Reported variations (section 10; not part of any label)")
VARS = {}
vlist = [("faint r 18.5 (A1.4)", dict(rfaint=18.5), None), ("R0 8.275, vsun (11.1, 251.5, 8.59)", dict(R0=8.275, vsun=(11.1, 251.5, 8.59)), None),
         ("Sgr band 10", dict(sgr=10.0), None), ("Sgr band 20", dict(sgr=20.0), None), ("no Sgr cut", dict(sgr=-1.0), None),
         ("distances x0.95", dict(dscale=0.95), None), ("distances x1.05", dict(dscale=1.05), None),
         ("beta fixed 0.2", {}, 0.2), ("beta fixed 0.8", {}, 0.8), ("dist-err term 0", dict(dfrac=0.0), None), ("dist-err term 0.2", dict(dfrac=0.2), None)]
for tag, ch, bf in vlist:
    _, _, rv = full_run(dict(NOMINAL, **ch), tag, beta_fixed=bf, do_mass=True)
    VARS[tag] = rv
    say(f"{tag}: N {rv['N']}, alpha {rv['alpha']['alpha']:.3f}+/-{rv['alpha']['sig']:.3f}, beta {rv['beta']:.3f}+/-{rv['sbeta']:.3f}, "
        f"M30 {rv['mass']['M'][30.0]['M']:.3f}, M50 {rv['mass']['M'][50.0]['M']:.3f}")
    for key in ("FW_census/canonical", "FW_census/alt", "FW_rc/canonical", "FW_rc/alt"):
        rows = rv["f"][key]; nm_ = [f"{a:.0f}-{b:.0f}" for a, b in rv["bins"]]
        say(f"    {key:20s} " + "  ".join(f"{n}: {x['f']:.3f}+/-{x['s']:.3f}" for n, x in zip(nm_, rows)) + f"  -> {grade([x['f'] for x in rows], [x['s'] for x in rows], nm_)[0]}")

# ================================================================== mutations (separate file)
MUT = open(os.path.join(HERE, "raw1_mut.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("RAW1 mutations (criteria FROZEN_CRITERIA.md). M1: comparator N must FAIL HOT. M2: a0 x 16 must FAIL COLD.")
rows = NOM["f"]["N"]; labN = grade([x["f"] for x in rows], [x["s"] for x in rows], names)
msay("M1 N: " + "  ".join(f"{n}: {x['f']:.3f}+/-{x['s']:.3f}" for n, x in zip(names, rows)) + f" -> {labN[0]} {labN[1]}  bites: {labN[0] == 'FAILS HOT'}")
MUTRES = {"M1": dict(label=labN[0], bins=labN[1], f=[x["f"] for x in rows])}
for ft in FOOT:
    rows = f_full(S, R, "FW_census", ft, a0_mult=16.0); lab = grade([x["f"] for x in rows], [x["s"] for x in rows], names)
    msay(f"M2 a0x16 {ft}: " + "  ".join(f"{n}: {x['f']:.3f}+/-{x['s']:.3f}" for n, x in zip(names, rows)) + f" -> {lab[0]} {lab[1]}  bites: {lab[0] == 'FAILS COLD'}")
    MUTRES[f"M2/{ft}"] = dict(label=lab[0], bins=lab[1], f=[x["f"] for x in rows])
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(dict(nominal=NOM, labels=LABELS, clip_variants=CLIPV, window_19_9=WIN2, variations=VARS, mutations=MUTRES,
                     synthetic=dict(alpha=asyn, beta=Rsyn["beta"], sbeta=Rsyn["sbeta"], f=fsyn))),
          open(os.path.join(HERE, "raw1_results.json"), "w"), indent=1)
say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
