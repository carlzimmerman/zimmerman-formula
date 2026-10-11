#!/usr/bin/env python3
"""CFG628: FRB foreground-halo gas partition vs the census placement R4 (FROZEN_CRITERIA.md, committed 2f6846261).

  sec. 2  rebuilt FLIMFLAM DR1 likelihood (Khrykin+24 Table 3 per-sightline inputs; flat priors; no HMF-based f_d prior)
  sec. 3  framework f_gas-equivalent interval: CFG515 census f_ret (cfg515_lib.fret_of, read-only), gas isothermal and
          hydrostatic in the law's potential g_N nu_mono(g_N/a0) out to the census edge; B-lo/B-hi x E1/E2 x M_ta in {1,2} M_h
  sec. 4  Z_near / Z_far, power gate sigma(f_halo) > 0.25, bins 2/3; f_IGM context
  sec. 5  MUTATE (CFG628_MUTATE=1): f_ret = 1 for every system
  sec. 6  C1 (partial identity), C2 (synthetic recovery), K1 (kernel), K2 (profile / edge)
Both footings, never pooled.  kappa = 1/2 FITTED.  One process, numpy only.
Run: nice -n 10 python3 -I cfg628_partition.py ; CFG628_MUTATE=1 nice -n 10 python3 -I cfg628_partition.py
"""
import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "CFG515_census_edge_resolution"))
import cfg515_lib as L515  # noqa: E402  (fret_of, ln_fac, FB, COLD_PER_B; read-only)

MUT = os.environ.get("CFG628_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


# ----------------------------------------------------------------------------------------------------------- constants
G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0856775814913673e19; MPC = 1e3 * KPC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FB16 = L515.FB16                      # 0.157, CFG416 census constant
H16 = L515.H16                        # 0.674
FB_TEMPLATE = 0.046 / 0.315           # Khrykin+24 mNFW normalisation Omega_b/Omega_m (INHERITED template)
H_FF, OM_FF, Z_FF = 0.673, 0.315, 0.20  # Khrykin+24 background and median redshift (INHERITED, r200 only)

# ---- nu_mono, copied verbatim from CFG596_lean_pm_1024/cfg596_pm.py
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


# ---- Moster+13 SHMR (parameters recalled, PROVISIONAL, INHERITED); M = M200c [Msun]
def moster_mstar(M, z):
    a = z / (1.0 + z)
    lM1 = 11.590 + 1.195 * a; N = 0.0351 - 0.0247 * a; b = 1.376 - 0.826 * a; g = 0.608 + 0.329 * a
    x = M / 10**lM1
    return M * 2 * N / (x**(-b) + x**g)


def r200c(M, z=Z_FF):
    Hz = 100 * H_FF * math.sqrt(OM_FF * (1 + z)**3 + 1 - OM_FF) * 1e3 / MPC
    rhoc = 3 * Hz**2 / (8 * math.pi * G)
    return (3 * M * MSUN / (4 * math.pi * 200 * rhoc))**(1 / 3)          # m


# ----------------------------------------------------------------------------------------------- framework gas profile
def gas_profile(Mb, a0, fret, sig2_fac=0.5, n=4000, inner="frozen"):
    """isothermal gas hydrostatic in g = g_N nu_mono(g_N/a0), point mass Mb [Msun]; returns (r [m], rho_shape, r_edge [m]).
    inner = "frozen": integrate from 1e-5 r_edge (as frozen).  DISCLOSED AFTER THE RUN: around a point mass the isothermal
    profile is degenerate (rho ~ exp(G Mb/(sigma^2 r)) in the Newtonian core), so essentially all gas piles up at the inner cut.
    inner = "rM" (post-freeze diagnostic, labelled, no verdict weight): the gas occupies r_M <= r <= r_edge only."""
    rM = math.sqrt(G * Mb * MSUN / a0)
    redge = rM / L515.ln_fac(fret)
    Vf2 = math.sqrt(G * Mb * MSUN * a0)
    sig2 = sig2_fac * Vf2
    r = np.geomspace(redge * 1e-5 if inner == "frozen" else min(rM, redge), redge, n)
    gN = G * Mb * MSUN / r**2
    g = gN * nu_mono(gN / a0)
    # ln rho = -(1/sig2) int g dr  (trapezoid in r)
    I = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))])
    lnrho = -I / sig2
    rho = np.exp(lnrho - lnrho.max())
    return r, rho, redge


def mass_in(r, rho):
    w = 4 * np.pi * r**2 * rho
    return np.concatenate([[0.0], np.cumsum(0.5 * (w[1:] + w[:-1]) * np.diff(r))])


def cyl_fraction(r, rho, R):
    """fraction of the (truncated) sphere's mass projected inside a cylinder of radius R."""
    w = 4 * np.pi * r**2 * rho
    tot = np.trapz(w, r)
    if R >= r[-1]:
        return 1.0
    inner = r <= R
    m_in = np.trapz(w[inner], r[inner]) if inner.sum() > 1 else 0.0
    ro = r[~inner]; wo = w[~inner]
    m_out = np.trapz(wo * (1 - np.sqrt(np.clip(1 - (R / ro)**2, 0, 1))), ro)
    return (m_in + m_out) / tot


def fret_value(Mta):
    if MUT:
        return 1.0
    return L515.fret_of(math.log10(Mta * H16))


def f_eq_cells(Mh, foot, sig2_fac=0.5, inner="frozen"):
    """all frozen variants for one halo mass: dict[(mta_fac, B, E)] -> f_eq."""
    out = {}
    a0 = A0[foot]
    R200 = r200c(Mh)
    Ms = moster_mstar(Mh, Z_FF)
    for k in (1.0, 2.0):
        Mta = k * Mh
        fr = fret_value(Mta)
        Mb = fr * FB16 * Mta
        r, rho, redge = gas_profile(Mb, a0, fr, sig2_fac, inner=inner)
        fc = cyl_fraction(r, rho, R200)
        mi = mass_in(r, rho); core = float(np.interp(1e-3 * redge, r, mi) / mi[-1])
        for B, Mion in (("B-lo", max(0.0, Mb - Ms)), ("B-hi", Mb)):
            out[(k, B, "E1")] = Mion / (FB_TEMPLATE * Mh)
            out[(k, B, "E2")] = Mion * fc / (FB_TEMPLATE * Mh)
        out[("meta", k)] = dict(f_ret=fr, Mb=Mb, Mstar=Ms, r_edge_kpc=redge / KPC, r200_kpc=R200 / KPC, cyl_frac=fc, frac_core=core)
    return out


# --------------------------------------------------------------------------------------------- rebuilt measurement
def load_ff():
    with open(HERE / "flimflam_dr1_sightlines.csv") as f:
        rows = list(csv.DictReader(f))
    keys = ["z", "dm_argo", "s_argo", "dm_halos", "s_halos", "dm_hosthalo", "s_hosthalo", "dm_mw", "dm_frb"]
    return {k: np.array([float(r[k]) for r in rows]) for k in keys}, [r["frb"] for r in rows]


SIG_STAR = 1.23
SIG_MW = 15.0


def loglike_grid(D, fi, fg, lmu, with_norm=True, dm_obs=None):
    """ln L on the (fi, fg, lmu) grid (broadcast shapes)."""
    obs = D["dm_frb"] if dm_obs is None else dm_obs
    mu = np.exp(lmu)
    s2host = (math.exp(SIG_STAR**2) - 1) * np.exp(2 * lmu + SIG_STAR**2)
    ll = 0.0
    for i in range(len(obs)):
        z = D["z"][i]
        model = D["dm_mw"][i] + fi * D["dm_argo"][i] + fg * D["dm_halos"][i] + (fg * D["dm_hosthalo"][i] + mu) / (1 + z)
        s2 = (fi * D["s_argo"][i])**2 + (fg * D["s_halos"][i])**2 + (fg * D["s_hosthalo"][i])**2 + SIG_MW**2 + s2host
        ll = ll - 0.5 * (model - obs[i])**2 / s2
        if with_norm:
            ll = ll - 0.5 * np.log(s2)
    return ll


def grids(nf=201, nm=121):
    f = (np.arange(nf) + 0.5) / nf            # cell centres in (0, 1]
    lm = np.linspace(0.0, 6.0, nm)
    return f, lm


def marg_stats(post, axis_vals, axis):
    other = tuple(a for a in range(post.ndim) if a != axis)
    p = post.sum(axis=other)
    p = p / p.sum()
    c = np.cumsum(p)
    q = lambda t: float(np.interp(t, c, axis_vals))
    return dict(p16=q(0.16), median=q(0.5), p84=q(0.84), pdf=p)


def fit(D, with_norm=True, fd_prior=False, nf=201, nm=121, dm_obs=None, chunk=16):
    """grid posterior, evaluated in f_igm chunks (memory < 100 MB)."""
    f, lm = grids(nf, nm)
    ll = np.empty((nf, nf, nm), np.float32)
    FG, LM = np.meshgrid(f, lm, indexing="ij")
    for i0 in range(0, nf, chunk):
        fi = f[i0:i0 + chunk][:, None, None]
        part = loglike_grid(D, fi, FG[None], LM[None], with_norm, dm_obs)
        if fd_prior:
            fd = fi + (0.20 / 0.55) * FG[None]
            part = np.where((fd >= 0.75) & (fd <= 0.95), part, -np.inf)
        ll[i0:i0 + chunk] = part
    post = np.exp(ll - ll.max())
    del ll
    sfi = marg_stats(post, f, 0); sfg = marg_stats(post, f, 1); smu = marg_stats(post, lm, 2)
    return dict(f_igm=sfi, f_gas=sfg, lnmu=smu, grid=f)


def zscore(m, sm, sp, lo, hi):
    """signed Z (prediction edge minus measurement) to the nearest and far edges of [lo, hi]."""
    if lo <= m <= hi:
        far = max((hi - m) / sp, (m - lo) / sm)
        return 0.0, far
    if hi < m:
        return (hi - m) / sm, (lo - m) / sm
    return (lo - m) / sp, (hi - m) / sp


def binlab(z_near, z_far):
    a = abs(z_near)
    if a >= 3: return "EXCLUDED"
    if a >= 2: return "TENSION"
    return "CONSISTENT (interval-limited)" if abs(z_far) >= 2 else "CONSISTENT"


# --------------------------------------------------------------------------------------------------------------- main
def main():
    say("CFG628 FRB foreground-halo partition vs census R4%s  (criteria 2f6846261)" % ("  [MUTATE: f_ret = 1 everywhere]" if MUT else ""))
    say("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    res = dict(mutate=MUT)

    # ---- K1 kernel
    yy = np.geomspace(1e-8, 1.0, 400)
    nuex = 1 / (1 - np.exp(-np.sqrt(yy)))
    k1 = float(np.max(np.abs(nu_mono(yy) - nuex)))
    k1r = float(np.max(np.abs(nu_mono(yy) / nuex - 1)))
    say("K1 nu_mono vs exponential for y < 1: max |d| = %.2e  %s at the frozen 1e-6 (absolute) tolerance; max relative |d| = %.2e"
        " (the engine's own table/trapezoid resolution; reported, tolerance not changed)" % (k1, "PASS" if k1 < 1e-6 else "FAIL", k1r))
    res["K1"] = dict(abs=k1, rel=k1r, pass_frozen=bool(k1 < 1e-6))

    # ---- K2 profile / edge
    k2 = {}
    for foot in A0:
        a0 = A0[foot]
        for Mh in (1e11, 1e12, 1e13):
            fr = fret_value(Mh); Mb = fr * FB16 * Mh
            r, rho, redge = gas_profile(Mb, a0, fr)
            m = mass_in(r, rho); norm_err = abs(m[-1] / np.trapz(4 * np.pi * r**2 * rho, r) - 1)
            Mcold = L515.COLD_PER_B * Mb / fr
            rM = math.sqrt(G * Mb * MSUN / a0)
            root = brentq(lambda x: Mb * (float(nu_mono(G * Mb * MSUN / (x * rM)**2 / a0)) - 1) - Mcold, 1e-3, 1e5) * rM
            k2[(foot, Mh)] = (norm_err, abs(root / redge - 1))
    k2max_n = max(v[0] for v in k2.values()); k2max_e = max(v[1] for v in k2.values())
    say("K2 profile normalisation max err %.1e; numeric phantom root vs closed-form edge max rel diff %.1e  %s"
        % (k2max_n, k2max_e, "PASS" if (k2max_n < 1e-6 and k2max_e < 1e-3) else "FAIL"))
    res["K2"] = dict(norm=k2max_n, edge=k2max_e)

    # ---- sec. 2 rebuilt measurement
    D, names = load_ff()
    F = fit(D)
    fg = F["f_gas"]; fi = F["f_igm"]; lmu = F["lnmu"]
    sm = fg["median"] - fg["p16"]; sp = fg["p84"] - fg["median"]; sig = 0.5 * (fg["p84"] - fg["p16"])
    say("")
    say("sec.2 REBUILT MEASUREMENT (Khrykin+24 Table 3, flat priors, ln-sigma term included; no HMF f_d prior)")
    say("  f_gas (= f_halo) median %.3f  p16 %.3f  p84 %.3f  -> sigma(f_halo) = %.3f  (-%.3f / +%.3f)"
        % (fg["median"], fg["p16"], fg["p84"], sig, sm, sp))
    say("  f_igm median %.3f  p16 %.3f  p84 %.3f" % (fi["median"], fi["p16"], fi["p84"]))
    say("  <DM_host^unk> median %.1f  (p16 %.1f, p84 %.1f)" % (math.exp(lmu["median"]), math.exp(lmu["p16"]), math.exp(lmu["p84"])))
    say("  published (fiducial, with the HMF-based f_d prior): f_igm 0.59 +0.11/-0.10, f_gas 0.55 +0.26/-0.29, mu 69 +28/-19;"
        " published sigma(f_gas) = 0.275")
    res["measurement"] = dict(f_gas=dict((k, fg[k]) for k in ("p16", "median", "p84")), sigma=sig, sigma_minus=sm, sigma_plus=sp,
                              f_igm=dict((k, fi[k]) for k in ("p16", "median", "p84")),
                              mu=dict((k, math.exp(lmu[k])) for k in ("p16", "median", "p84")), published_sigma=0.275)

    # ---- C1 partial identity
    say("")
    say("C1 partial identity vs Khrykin+24 fiducial (f_igm 0.59, f_gas 0.55, mu 69):")
    c1 = {}
    for lab, kw in (("C1-a flat, ln-sigma", {}), ("C1-b flat, no ln-sigma", dict(with_norm=False)),
                    ("C1-c approx f_d prior", dict(fd_prior=True))):
        Fx = F if lab.startswith("C1-a") else fit(D, **kw)
        a, b_, mu_ = Fx["f_igm"]["median"], Fx["f_gas"]["median"], math.exp(Fx["lnmu"]["median"])
        ok = abs(a - 0.59) <= 0.10 and abs(b_ - 0.55) <= 0.10
        c1[lab] = dict(f_igm=a, f_gas=b_, mu=mu_, f_gas_p16=Fx["f_gas"]["p16"], f_gas_p84=Fx["f_gas"]["p84"],
                       label="reproduced" if ok else "not reproduced")
        say("  %-24s f_igm %.3f  f_gas %.3f (p16 %.3f p84 %.3f)  mu %.1f  -> %s"
            % (lab, a, b_, Fx["f_gas"]["p16"], Fx["f_gas"]["p84"], mu_, c1[lab]["label"]))
    say("  NOTE: the frozen C1 rule tests only the f medians. <DM_host^unk> is NOT reproduced (rebuilt %.0f / %.0f / %.0f vs 69):"
        " the paper's exact likelihood normalisation and its HMF-based f_d prior are not recoverable from the text." %
        (c1["C1-a flat, ln-sigma"]["mu"], c1["C1-b flat, no ln-sigma"]["mu"], c1["C1-c approx f_d prior"]["mu"]))
    res["C1"] = c1

    # ---- C2 synthetic recovery (coarse grid 101 x 101 x 61, declared here)
    rng = np.random.default_rng(628)
    truth = (0.6, 0.5, math.log(69.0))
    s2host = (math.exp(SIG_STAR**2) - 1) * math.exp(2 * truth[2] + SIG_STAR**2)
    mod = D["dm_mw"] + truth[0] * D["dm_argo"] + truth[1] * D["dm_halos"] + (truth[1] * D["dm_hosthalo"] + 69.0) / (1 + D["z"])
    s = np.sqrt((truth[0] * D["s_argo"])**2 + (truth[1] * D["s_halos"])**2 + (truth[1] * D["s_hosthalo"])**2 + SIG_MW**2 + s2host)
    cover = 0; sigs = []; meds = []
    NM = 300
    for _ in range(NM):
        obs = mod + rng.normal(0, s)
        Fm = fit(D, nf=101, nm=61, dm_obs=obs)
        g = Fm["f_gas"]
        cover += int(g["p16"] <= truth[1] <= g["p84"]); sigs.append(0.5 * (g["p84"] - g["p16"])); meds.append(g["median"])
    cov = cover / NM
    say("")
    say("C2 synthetic recovery (truth f_igm 0.6, f_gas 0.5, mu 69; %d mocks, grid 101x101x61): 68%% coverage %.3f  %s;"
        " median mock sigma(f_gas) %.3f" % (NM, cov, "PASS" if 0.55 <= cov <= 0.81 else "FAIL", float(np.median(sigs))))
    res["C2"] = dict(coverage=cov, median_sigma=float(np.median(sigs)), n=NM, std_of_medians=float(np.std(meds)), mean_median=float(np.mean(meds)))
    say("   reading: scatter of recovered medians %.3f (mean %.3f) vs quoted sigma %.3f -> the f_gas posterior is wider than the"
        " estimator scatter, i.e. prior-dominated (bounded flat prior); over-coverage, not bias" % (np.std(meds), np.mean(meds), np.median(sigs)))

    # ---- sec. 3 framework prediction interval, per footing
    say("")
    say("sec.3 FRAMEWORK f_gas-EQUIVALENT (%s)" % ("MUTATE f_ret = 1" if MUT else "census f_ret, CFG416 fret_of"))
    lMs = np.round(np.arange(11.0, 13.0 + 1e-9, 0.05), 2)
    lMs_rep = np.round(np.concatenate([np.arange(10.0, 11.0, 0.05), np.arange(13.05, 13.5 + 1e-9, 0.05)]), 2)
    pred = {}
    for foot in A0:
        cells = {lm: f_eq_cells(10**lm, foot) for lm in lMs}
        vals = [v for c in cells.values() for kk, v in c.items() if kk[0] != "meta"]
        lo, hi = min(vals), max(vals)
        # temperature bracket (reported only, E2)
        tb = {}
        for fac in (2 / 9, 1.0):
            cc = [f_eq_cells(10**lm, foot, fac) for lm in lMs]
            v2 = [c[kk] for c in cc for kk in c if kk[0] != "meta" and kk[2] == "E2"]
            tb["%.3f" % fac] = (min(v2), max(v2))
        rep = [v for lm in lMs_rep for kk, v in f_eq_cells(10**lm, foot).items() if kk[0] != "meta"]
        say("  [%s a0 = %.4e]" % (foot, A0[foot]))
        say("    logM_h  f_ret(M_ta=M_h)  M*/(f_bT M_h)  r_edge/r200   E1:B-lo  E1:B-hi  E2:B-lo  E2:B-hi   (M_ta = M_h)")
        for lm in (11.0, 11.5, 12.0, 12.5, 13.0):
            c = cells[lm]; me = c[("meta", 1.0)]
            say("    %5.2f   %6.3f          %6.3f         %6.2f      %6.3f   %6.3f   %6.3f   %6.3f"
                % (lm, me["f_ret"], me["Mstar"] / (FB_TEMPLATE * 10**lm), me["r_edge_kpc"] / me["r200_kpc"],
                   c[(1.0, "B-lo", "E1")], c[(1.0, "B-hi", "E1")], c[(1.0, "B-lo", "E2")], c[(1.0, "B-hi", "E2")]))
        for lm in (11.0, 12.0, 13.0):
            c = cells[lm]; me = c[("meta", 2.0)]
            say("    M_ta = 2 M_h, logM_h %.1f: f_ret %.3f  E1:B-lo %.3f  E1:B-hi %.3f  E2:B-lo %.3f  E2:B-hi %.3f"
                % (lm, me["f_ret"], c[(2.0, "B-lo", "E1")], c[(2.0, "B-hi", "E1")], c[(2.0, "B-lo", "E2")], c[(2.0, "B-hi", "E2")]))
        say("    PREDICTION INTERVAL P = [%.3f, %.3f]  (grid 11.0-13.0; all variants)" % (lo, hi))
        say("    reported only: 10.0-11.0 & 13.05-13.5 extension -> [%.3f, %.3f]; E2 temperature bracket sigma^2 = 2/9 Vf^2: "
            "[%.3f, %.3f], = Vf^2: [%.3f, %.3f]" % (min(rep), max(rep), *tb["0.222"], *tb["1.000"]))
        dg = cells[12.0][("meta", 1.0)]
        say("    DISCLOSED (post-run): frozen point-mass isothermal profile is degenerate: at logM_h 12, M_ta = M_h, %.4f of the gas"
            " lies inside 1e-3 r_edge, so E2 = E1 wherever r_edge > r200 would matter. P does not depend on the profile"
            " (its edges are B-lo min and E1:B-hi max)." % dg["frac_core"])
        cp = {lm: f_eq_cells(10**lm, foot, inner="rM") for lm in lMs}
        v2p = [c[kk] for c in cp.values() for kk in c if kk[0] != "meta" and kk[2] == "E2"]
        say("    post-freeze diagnostic E2' (gas in r_M..r_edge, sigma^2 = Vf^2/2): cylinder fraction at logM_h 11/12/13 (M_ta = M_h)"
            " %.3f / %.3f / %.3f; E2' range [%.3f, %.3f] (no verdict weight)"
            % (cp[11.0][("meta", 1.0)]["cyl_frac"], cp[12.0][("meta", 1.0)]["cyl_frac"], cp[13.0][("meta", 1.0)]["cyl_frac"],
               min(v2p), max(v2p)))
        lo1 = min(v for c in cells.values() for kk, v in c.items() if kk[0] == 1.0)
        hi1 = max(v for c in cells.values() for kk, v in c.items() if kk[0] == 1.0)
        say("    reported only (post-freeze subset, M_ta = M_h only): P1 = [%.3f, %.3f]" % (lo1, hi1))
        pred[foot] = dict(lo=lo, hi=hi, P1=(lo1, hi1), ext=(min(rep), max(rep)), temp_bracket=tb,
                          table={str(lm): {"%s|%s|%s" % kk if kk[0] != "meta" else "meta|%g" % kk[1]: v
                                           for kk, v in cells[lm].items()} for lm in (11.0, 11.5, 12.0, 12.5, 13.0)})
    res["prediction"] = pred

    # ---- sec. 4 / 5 verdict
    say("")
    gate = sig > 0.25
    say("POWER GATE: sigma(f_halo) rebuilt = %.3f %s 0.25 -> %s (published 0.275 -> %s)"
        % (sig, ">" if gate else "<=", "NON-DIAGNOSTIC" if gate else "passes", "NON-DIAGNOSTIC" if 0.275 > 0.25 else "passes"))
    res["power_gate"] = dict(sigma=sig, non_diagnostic=bool(gate))
    m = fg["median"]
    pdf, grid = fg["pdf"], F["grid"]
    verdicts = {}
    for foot in A0:
        lo, hi = pred[foot]["lo"], pred[foot]["hi"]
        zn, zf = zscore(m, sm, sp, lo, hi)
        lab = binlab(zn, zf)
        pr = float(pdf[grid >= lo].sum())
        need_gate = 8 * (sig / 0.25)**2
        side = sm if hi < m else sp
        dist = 0.0 if lo <= m <= hi else (m - hi if hi < m else lo - m)
        need3 = 8 * (side / (dist / 3))**2 if dist > 0 else float("inf")
        verdicts[foot] = dict(Z_near=zn, Z_far=zf, bin=lab, verdict=("NON-DIAGNOSTIC" if gate else lab),
                              pr_fgas_ge_lo=pr, N_for_gate=need_gate, N_for_3sigma=need3)
        say("  [%s] P = [%.3f, %.3f] vs f_halo %.3f (-%.3f/+%.3f): Z_near %+.2f, Z_far %+.2f -> bin %s; VERDICT %s"
            % (foot, lo, hi, m, sm, sp, zn, zf, lab, verdicts[foot]["verdict"]))
        say("        Pr(f_gas >= %.3f) = %.3f; forecast N for sigma <= 0.25: %.0f sightlines; N for |Z_near| = 3: %s"
            % (lo, pr, need_gate, ("%.0f" % need3) if math.isfinite(need3) else "never (inside P)"))
        say("        (forecast scales sigma as N^-1/2 from a prior-bounded posterior: optimistic; no verdict weight)")
    res["verdict"] = verdicts

    # f_IGM context
    PI = (0.60, 0.95)
    smi = fi["median"] - fi["p16"]; spi = fi["p84"] - fi["median"]
    zni, zfi = zscore(fi["median"], smi, spi, *PI)
    say("  f_IGM CONTEXT: P_IGM = [0.60, 0.95] vs f_igm %.3f (-%.3f/+%.3f): Z_near %+.2f, Z_far %+.2f -> %s (CONTEXT; %s)"
        % (fi["median"], smi, spi, zni, zfi, binlab(zni, zfi),
           "MUTATE: f_IGM,pred under f_ret = 1 needs a halo mass function -> NOT EVALUABLE" if MUT else "no verdict weight"))
    res["f_IGM_context"] = dict(P=PI, Z_near=zni, Z_far=zfi, bin=binlab(zni, zfi))

    if MUT:
        teeth = all(abs(v["Z_near"]) >= 3 for v in verdicts.values())
        say("")
        say("MUTATE TOOTH: f_ret = 1 must come out EXCLUDED (|Z_near| >= 3): %s"
            % ("DETECTED -> the test has teeth" if teeth else "NOT DETECTED -> THE TEST HAS NO TEETH at this sample's power"))
        res["mutate_tooth"] = bool(teeth)

    with open(HERE / ("cfg628_partition%s.json" % TAG), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    with open(HERE / ("cfg628_partition%s.out" % TAG), "w") as f:
        f.write("\n".join(OUT) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
