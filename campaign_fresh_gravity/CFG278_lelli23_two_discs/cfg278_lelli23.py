#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG278 -- implied-a0 rows for the two ALMA CO discs of Lelli et al. 2023 (arXiv:2302.00030), zC-400569 (z = 2.240) and zC-488879 (z = 1.470), from the digitised multi-line rotation curves
with independent baryons (SED stars x CO-based gas): six rows = two galaxies x {stars, stars+CO a=0.4, stars+CO a=4.3}, never pooled.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG278_lelli23_two_discs/FROZEN_CRITERIA.md (9a45bbdae).
  g_obs   V_rot^2 / R at every digitised point (all lines pooled), no pressure term; inclination N(54.5, 5.0) / N(71.6, 4.1) deg common draw; V errors = the digitised bar half-widths
  g_bar   stars (SED, 0.30 dex): deprojected de Vaucouleurs bulge (fraction f_bul = 0.33 / 0.63) + exponential Freeman disc; gas (L'_CO x alpha_CO, 0.213 dex): exponential disc of the stellar disc's R_e
  STAGE=A   the blind pre-flight: only the radius column of the digitised CSV is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A, the SELFTEST and this script are committed); STAGE=B SELFTEST=1; STAGE=B MUTATE=1 (V x 2).
Run: STAGE=A python3 .../cfg278_lelli23.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math, time, zlib, re
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import j0, j1, ive, gammainc, gammaincinv, gammaln
from scipy.integrate import quad

TSTART = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUTATE or SELFTEST) and STAGE == "A") and not (MUTATE and SELFTEST), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}{'' if load_bearing else ' (not load-bearing)'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
LOADVEL = (STAGE == "B") and not SELFTEST                                   # the SELFTEST never loads the real velocity-bearing columns
CSVP = os.path.join(REPO, "data_assembly", "lelli2023_rotcur_digitised", "lelli2023_rotcur_digitised.csv")
TEXP = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src", "2302.00030", "ColdGasDiskCosmicNoon.tex")

# ---------------------------------------------------------------- constants frozen in the criteria (sections 0-3)
GAL = {"zC-400569": dict(z=2.23999, i0=54.5, ei=5.0, lm=math.log10(21.9e10), S=0.50, nu_rest=345.796, Rj=0.60, Re_bul_as=0.12, Re_disc_as=0.76, fbul=0.33, Mstar_dyn=7.8e10, alpha_dyn=2.1, mbul_mbar=0.2, vbar_table=254.0, nlines=[4, 5, 6], beams=None),
       "zC-488879": dict(z=1.46997, i0=71.6, ei=4.1, lm=math.log10(5.2e10), S=0.56, nu_rest=230.538, Rj=0.85, Re_bul_as=0.35, Re_disc_as=0.88, fbul=0.63, Mstar_dyn=21.1e10, alpha_dyn=2.9, mbul_mbar=0.5, vbar_table=336.0, nlines=[5, 5], beams=None)}
ALPHA = {"stars": 0.0, "stars+CO a=0.4": 0.4, "stars+CO a=4.3": 4.3}
SIGM, SIGGAS = 0.30, 0.213
SIG_CO, SIG_HA = 15.0, 37.0
ROWS = [dict(label=f"{g} [{b}]", gal=g, branch=b, alpha=ALPHA[b], role="branch") for g in GAL for b in ALPHA]
LAB2I = {r["label"]: i for i, r in enumerate(ROWS)}


def DL_mpc(z, H0=67.4, Om=H.OM):
    return 299792.458 / H0 * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0] * (1 + z)


def Lprime(S, nu_rest, z):                                                  # K km/s pc^2 (Solomon & Vanden Bout 2005), S in Jy km/s
    return 3.25e7 * S * (nu_rest / (1 + z)) ** -2 * DL_mpc(z) ** 2 * (1 + z) ** -3


for g, G in GAL.items():
    G["kpa"] = H.kpc_per_arcsec(G["z"]); G["Re_bul"] = G["Re_bul_as"] * G["kpa"]; G["Re_disc"] = G["Re_disc_as"] * G["kpa"]; G["L10"] = Lprime(G["S"], G["nu_rest"], G["z"]) / G["Rj"]; G["Ms"] = 10 ** G["lm"]

# ---------------------------------------------------------------- loading (stage A: radius and notes only; no velocity-bearing column)
cols = ["galaxy", "line", "radius_arcsec"] + (["notes", "vrot_kms", "err_lo_kms", "err_hi_kms"] if LOADVEL else [])      # the notes column carries the error-bar cap pixel rows: loaded at stage B only
df = pd.read_csv(CSVP, usecols=cols)
if "notes" in df: df["notes"] = df["notes"].fillna("")
P(f"digitised curves {os.path.basename(CSVP)} sha256 {H.sha(CSVP)}; velocity-bearing columns loaded: {LOADVEL}; {len(df)} points; lines: " + "; ".join(f"{g}: " + ", ".join(f"{l} {int(((df.galaxy == g) & (df.line == l)).sum())}" for l in df[df.galaxy == g].line.unique()) for g in GAL))
PTS = {}
for g, G in GAL.items():
    d = df[df.galaxy == g].reset_index(drop=True)
    d["Rkpc"] = d["radius_arcsec"] * G["kpa"]
    d["is_ha"] = ~d["line"].str.upper().str.startswith("CO")
    d["first_of_line"] = False
    for l in d.line.unique():
        ix = d.index[d.line == l]; d.loc[ix[np.argmin(d.loc[ix, "radius_arcsec"].values)], "first_of_line"] = True
    d["flag"] = d["notes"].astype(str).str.startswith(("PARTLY HIDDEN", "overlapped")) if "notes" in d else False          # the three occluded markers (addendum 1)
    PTS[g] = d


# ---------------------------------------------------------------- geometry (m s^-2 per Msun)
def b_proj(n):
    return float(gammaincinv(2 * n, 0.5))


def sigma_unit(R, n, Re):
    b = b_proj(n); Se = 1.0 / (2 * math.pi * n * math.exp(b) * b ** (-2 * n) * math.exp(gammaln(2 * n)) * Re ** 2)
    return Se * np.exp(-b * ((R / Re) ** (1.0 / n) - 1.0))


_HC = {}


def hankel_g_unit(n, Re, Rk, NRp=4000, Rmax_f=14.0, NK=24000, Kmax_f=60.0, chunk=2000):
    key = (n, Re, tuple(np.round(np.atleast_1d(Rk), 9)))
    if key in _HC: return _HC[key]
    Rp = np.linspace(0, Rmax_f * Re, NRp + 1); dR = Rp[1] - Rp[0]; S = sigma_unit(Rp, n, Re) * Rp
    w = np.ones(NRp + 1); w[0] = w[-1] = 0.5
    ks = np.linspace(0, Kmax_f / Re, NK + 1); dk = ks[1] - ks[0]; St = np.empty(NK + 1)
    for a in range(0, NK + 1, chunk):
        kk = ks[a:a + chunk]; St[a:a + chunk] = (j0(np.outer(kk, Rp)) * (S * w * dR)).sum(axis=1)
    wk = np.ones(NK + 1); wk[0] = wk[-1] = 0.5
    Rk = np.atleast_1d(Rk).astype(float)
    g = np.array([(ks * j1(ks * R) * St * wk * dk).sum() for R in Rk]) * 2 * math.pi * H.G_KPC * H.G2SI
    _HC[key] = g
    return g


def gauss_closed(s, R):
    x = R ** 2 / (4 * s ** 2)
    return H.G_KPC * math.sqrt(math.pi / 2) * R / (2 * s ** 3) * (ive(0, x) - ive(1, x)) * H.G2SI


def p_dep(n):
    return 1 - 0.6097 / n + 0.05563 / n ** 2


def b_dep(n):
    return 2 * n - 1 / 3 + 0.009876 / n


def fenc_sph(r, n, Re):
    return gammainc(n * (3 - p_dep(n)), b_dep(n) * (np.asarray(r, float) / Re) ** (1.0 / n))


def gsph_sersic(M, n, Re, R):
    R = np.asarray(R, float)
    return H.G_KPC * M * fenc_sph(R, n, Re) / R ** 2 * H.G2SI


def gparts(G, R, fbul=None, gas="base", gre=1.0, scale=1.0):
    """(g_stars, g_gas) per Msun of stellar / gas mass at radii R (kpc); `scale` multiplies every length of the model (the kpc/arcsec knob)"""
    R = np.asarray(R, float); fb = G["fbul"] if fbul is None else fbul
    Rb, Rd = G["Re_bul"] * scale, G["Re_disc"] * scale
    gs = fb * gsph_sersic(1.0, 4.0, Rb, R) + (1 - fb) * np.asarray(H.gdisc(1.0, Rd, R), float)
    gg = np.asarray(H.gsph(1.0, Rd, R), float) if gas == "pointmass" else np.asarray(H.gdisc(1.0, Rd * gre, R), float)
    return gs, gg


def gb_row(G, R, Mg, fbul=None, gas="base", gre=1.0, scale=1.0, Ms=None):
    gs, gg = gparts(G, R, fbul, gas, gre, scale)
    return (G["Ms"] if Ms is None else Ms) * gs + Mg * gg


for r_ in ROWS:
    G = GAL[r_["gal"]]; d = PTS[r_["gal"]]; r_["R"] = d["Rkpc"].values.astype(float); r_["Mg"] = r_["alpha"] * G["L10"]
    r_["gs_u"], r_["gg_u"] = gparts(G, r_["R"]); r_["gb0"] = G["Ms"] * r_["gs_u"] + r_["Mg"] * r_["gg_u"]; r_["y0"] = r_["gb0"] / A0C
P("galaxies: " + "; ".join(f"{g}: z {G['z']}, {G['kpa']:.3f} kpc/arcsec, L'_CO(1-0) {G['L10']:.3e} K km/s pc2, M_gas(a=0.4) {0.4 * G['L10']:.2e}, (a=4.3) {4.3 * G['L10']:.2e}, M* {G['Ms']:.2e}, R_e,bul {G['Re_bul']:.2f}, R_e,disc {G['Re_disc']:.2f} kpc, f_bul {G['fbul']}, i {G['i0']} +- {G['ei']}" for g, G in GAL.items()))


def has(tex_compact, pat):
    return re.sub(r"\s+", "", pat) in tex_compact


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (only the radius column loaded; no g_obs, D, delta or s* is formed)")
    tex = re.sub(r"\s+", "", open(TEXP, encoding="utf-8", errors="ignore").read())
    TX = ["zC-400569&2.23999&CO(3-2)&$0.41\\times0.34$&$3.5\\times2.9$", "0.50$^{+0.09}_{-0.08}$", "0.56$^{+0.04}_{-0.05}$", "zC-488879&1.46997&CO(2-1)", "$i$($^{\\circ}$)&54.5$\\pm$5.0&71.6$\\pm$4.1", "$\\langle V_{\\rm rot}\\rangle$(\\kms)&254$\\pm$41&336$\\pm$29", "$R_{\\rm e,\\,disk}$(arcsec)&0.76$\\pm$0.01&0.88$\\pm$0.05", "$R_{\\rm e,\\,bul}$(arcsec)&0.12$\\pm$0.13&0.35$\\pm$1.1",
          "(21.9\\pm6.5)\\times10^{10}", "(5.2\\pm1.2)\\times10^{10}", "$M_\\star=(7.8^{+2.3}_{-2.8})\\times10^{10}$", "$M_\\star=(21.1^{+3.6}_{-4.2})\\times10^{10}$", "$\\alpha_{\\rm CO}\\simeq0.4$", "$\\alpha_{\\rm CO}\\simeq4.3$", "$R_{21}=L_{\\rm CO(2-1)}/L_{\\rm CO(1-0)}\\simeq0.85$", "$R_{31}=L_{\\rm CO(3-2)}/L_{\\rm CO(1-0)}\\simeq0.60$",
          "$M_{\\rm bul}/M_{\\rm bar}\\simeq0.2$", "$M_{\\rm bul}/M_{\\rm bar}\\simeq0.5$", "$\\alpha_{\\rm CO}=2.1^{+0.7}_{-0.8}$", "$\\alpha_{\\rm CO}=2.9^{+0.7}_{-0.9}$"]
    found = [has(tex, p) for p in TX]
    n_per = {g: sorted(int(((PTS[g].line == l)).sum()) for l in PTS[g].line.unique()) for g in GAL}
    mono = all(all(np.all(np.diff(PTS[g].loc[PTS[g].line == l, "radius_arcsec"].values) > 0) or np.all(np.diff(np.sort(PTS[g].loc[PTS[g].line == l, "radius_arcsec"].values)) > 0) for l in PTS[g].line.unique()) for g in GAL)
    check("C1 CONTROL (loader): the CSV has 25 rows; per-line counts equal 4/5/6 (zC-400569: CO(4-3), CO(3-2), Halpha) and 5/5 (zC-488879); radii positive and distinct within each line; the paper's constants of the criteria section 0.1 are found in the TeX",
          f"rows {len(df)}; counts {n_per}; radii ok {mono and bool((df.radius_arcsec > 0).all())}; TeX {sum(found)} of {len(TX)}: {[i for i, f in enumerate(found) if not f] or 'all found'}", len(df) == 25 and n_per["zC-400569"] == [4, 5, 6] and n_per["zC-488879"] == [5, 5] and mono and bool((df.radius_arcsec > 0).all()) and all(found))
    exp_ = {"zC-400569": (9.4e9, 1.0e11), "zC-488879": (7.8e9, 8.4e10)}
    errs = [abs(0.4 * GAL[g]["L10"] / exp_[g][0] - 1) for g in GAL] + [abs(4.3 * GAL[g]["L10"] / exp_[g][1] - 1) for g in GAL]
    check("C1b CONTROL: my CO luminosity code reproduces the hand arithmetic of the criteria (gas masses 9.4e9 / 1.0e11 for zC-400569, 7.8e9 / 8.4e10 for zC-488879 at alpha 0.4 / 4.3) within 5 %; the kpc/arcsec scales equal 8.45 and 8.69 (the paper's rounded 8.5) within 1 %",
          f"relative differences {np.array2string(np.array(errs), precision=4)}; kpc/arcsec {GAL['zC-400569']['kpa']:.3f}, {GAL['zC-488879']['kpa']:.3f}; the authors' dynamical gas masses alpha 2.1 / 2.9 x L'10 = {2.1 * GAL['zC-400569']['L10']:.2e} / {2.9 * GAL['zC-488879']['L10']:.2e}",
          max(errs) < 0.05 and abs(GAL["zC-400569"]["kpa"] / 8.45 - 1) < 0.01 and abs(GAL["zC-488879"]["kpa"] / 8.69 - 1) < 0.01)
    g_h1 = hankel_g_unit(1.0, 2.57, np.array([1.0, 3.6, 7.2])); g_f = np.array([float(H.gdisc(1.0, 2.57, r)) for r in (1.0, 3.6, 7.2)]); d1 = float(np.max(np.abs(g_h1 / g_f - 1)))
    s_g = 2.57 / math.sqrt(2 * b_proj(0.5)); g_h5 = hankel_g_unit(0.5, 2.57, np.array([1.0, 3.6, 7.2])); g_c = np.array([gauss_closed(s_g, r) for r in (1.0, 3.6, 7.2)]); d5 = float(np.max(np.abs(g_h5 / g_c - 1)))
    p_, b_ = p_dep(4.0), b_dep(4.0); a_ = 4.0 * (3 - p_); rho = lambda r: r ** (-p_) * np.exp(-b_ * r ** 0.25)
    Sg = lambda Rp: 2.0 * quad(lambda t: rho(math.sqrt(Rp ** 2 + t ** 2)), 0, np.inf, limit=200)[0]
    half4 = quad(lambda Rp: 2 * math.pi * Rp * Sg(Rp), 0, 1.0, limit=200)[0] / (math.exp(gammaln(a_)) * 4.0 * b_ ** (-a_) * 4 * math.pi)
    check("C2 CONTROL (geometry): the Hankel thin disc equals Freeman's exact exponential disc and the exact Gaussian closed form to 2e-3; the deprojected n = 4 profile's projected half-mass radius equals R_e to 1 %; the enclosed fraction tends to 1", f"Hankel vs Freeman {d1:.1e}; vs Gaussian {d5:.1e}; n=4 projected fraction within R_e {half4:.4f}; |f(inf) - 1| {abs(float(fenc_sph(1e4, 4.0, 1.0)) - 1):.1e}",
          d1 < 2e-3 and d5 < 2e-3 and abs(half4 - 0.5) < 0.005 and abs(float(fenc_sph(1e4, 4.0, 1.0)) - 1) < 1e-6)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C); same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C3 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    dn = 0.0
    for r_ in ROWS:
        for st in (0.5, 1.0, 2.5):
            ls, unb = H.s_star(NU(r_["gb0"] / (A0C * st)), r_["gb0"]); dn = max(dn, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C4 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every row's baryon side", f"max |d log10 s| {dn:.1e}", dn < 1e-6)

    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    for r_ in ROWS:
        lv, fl = H.lever1(NU(r_["y0"]), r_["gb0"]); r_["lever"], r_["ill"] = lv, bool(fl or abs(lv) >= 10)
        P(f"    {r_['label']:30s} N {len(r_['R'])}: R {r_['R'].min():.2f}-{r_['R'].max():.2f} kpc (median {np.median(r_['R']):.2f}); y {r_['y0'].min():.2f}-{r_['y0'].max():.2f} (median {np.median(r_['y0']):.2f}); lever {lv:+.2f}{' (not computable)' if fl else ''}  {'ILL-CONDITIONED' if r_['ill'] else 'conditioned'}")
    P(f"    CFG240: T4 floor 3 sigma / sqrt(N_eff) at sigma = 0.2 dex: {3 * 0.2 / math.sqrt(6):.2f} dex (N_eff ~ 6, zC-400569) and {3 * 0.2 / math.sqrt(4):.2f} dex (N_eff ~ 4, zC-488879); y(B) spans {min(r_['y0'].min() for r_ in ROWS):.2f} to {max(r_['y0'].max() for r_ in ROWS):.1f}; the break-even design needs y >~ 8 with deep points (y < 0.3)")
    P("\nA3  KNOB EFFECTS ON g_bar BY POINT (median over the points, dex relative to the baseline; stars at unit mass / gas at unit mass)")
    for g, G in GAL.items():
        R = PTS[g]["Rkpc"].values; s0, g0 = gparts(G, R)
        for nm, (s1, g1) in (("no bulge", (gparts(G, R, 0.0)[0], g0)), ("f_bul x2", (gparts(G, R, min(0.9, 2 * G["fbul"]))[0], g0)), ("gas R_e x0.6", (s0, gparts(G, R, gre=0.6)[1])), ("gas R_e x1.5", (s0, gparts(G, R, gre=1.5)[1])), ("gas point mass", (s0, gparts(G, R, gas="pointmass")[1])), ("8.5 kpc/arcsec", (gparts(G, R * 8.5 / G["kpa"], scale=8.5 / G["kpa"])[0], gparts(G, R * 8.5 / G["kpa"], scale=8.5 / G["kpa"])[1]))):
            P(f"    {g} {nm}: stars {float(np.median(np.log10(s1 / s0))):+.3f}, gas {float(np.median(np.log10(g1 / g0))):+.3f} dex")
    P("\nA4  THE BEAM (CO beams from Table tab:cubes; major axis in arcsec; HWHM = half of it): " + "; ".join(f"{g}: {', '.join(f'{l} {int((PTS[g][PTS[g].line == l].radius_arcsec < 0.5 * bm).sum())}/{int((PTS[g].line == l).sum())} points inside the HWHM' for l, bm in bl)}" for g, bl in (("zC-400569", [("CO(3-2)", 0.41), ("CO(4-3)", 0.54)]), ("zC-488879", [("CO(2-1)", 0.48), ("CO(3-2)", 0.46)])) if all(l in set(PTS[g].line.unique()) for l, _ in bl)))
    P(f"A5  innermost-of-line points (knob): {int(sum(PTS[g]['first_of_line'].sum() for g in GAL))}; the digitiser-flagged (occluded) points are identified from the notes column at stage B only")
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C4)")
    P("  PF-D2 ILL-CONDITIONED rows: " + (", ".join(r_["label"] for r_ in ROWS if r_["ill"]) or "none"))
    P("  PF-D3 DRAWABLE as an upper bound or floor: " + (", ".join(r_["label"] for r_ in ROWS if pfd1 and not r_["ill"]) or "none"))
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 7) scored (HE4-HE7 are scored at stage B):")
    def y_at(lab, R0=4.0):
        r_ = ROWS[LAB2I[lab]]; G = GAL[r_["gal"]]; gb = G["Ms"] * gparts(G, np.array([R0]))[0] + r_["Mg"] * gparts(G, np.array([R0]))[1]; return float(gb[0] / A0C)
    ya, yb = y_at("zC-400569 [stars]"), y_at("zC-488879 [stars]")
    he = {"HE1": bool(5 <= ya <= 15 and 0.8 <= yb <= 4), "HE2": bool(all(not ROWS[LAB2I[f"zC-488879 [{b}]"]]["ill"] for b in ALPHA) and any(ROWS[LAB2I[f"zC-400569 [{b}]"]]["ill"] for b in ALPHA)), "HE3": bool(max(errs) < 0.05)}
    P(f"    HE1: y at R = 4 kpc, stars only: zC-400569 {ya:.2f} (needs 5-15), zC-488879 {yb:.2f} (needs 0.8-4): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}")
    P(f"    HE2: zC-488879 rows conditioned {[not ROWS[LAB2I[f'zC-488879 [{b}]']]['ill'] for b in ALPHA]}; zC-400569 rows ILL {[ROWS[LAB2I[f'zC-400569 [{b}]']]['ill'] for b in ALPHA]}: {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
    P(f"    HE3: CO-based gas masses within 5 % of the hand arithmetic (max {max(errs):.4f}): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
    NUM.update(inputs={g: {k: v for k, v in G.items() if k not in ("beams",)} for g, G in GAL.items()}, rows={r_["label"]: dict(R=r_["R"].tolist(), gb0=r_["gb0"].tolist(), y0=r_["y0"].tolist(), lever=r_["lever"], ill=r_["ill"], Mg=r_["Mg"]) for r_ in ROWS}, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)),
               controls_numbers=dict(hankel_vs_freeman=d1, hankel_vs_gaussian=d5, half_mass_n4=half4, gas_mass_errors=errs))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2780)
    KIN = {}
    for g, G in GAL.items():
        d = PTS[g]; n = len(d)
        if SELFTEST:
            KIN[g] = None
        else:
            V = d["vrot_kms"].values.astype(float); E = 0.5 * (d["err_lo_kms"].values.astype(float) + d["err_hi_kms"].values.astype(float))
            if MUTATE: V, E = 2.0 * V, 2.0 * E
            KIN[g] = dict(V=V, E=E)
    if SELFTEST:
        for r_ in ROWS:
            gt = r_["gb0"] * NU(r_["gb0"] / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15, len(r_["R"])); V = np.sqrt(gt * r_["R"] / H.G2SI); r_["kin"] = dict(V=V, E=0.10 * V)
        P("SELFTEST: V fabricated from the law at s_true = 2 on each row's own baryons (+0.15 dex scatter), 10 % errors; the real velocity-bearing columns are not even loaded")
    else:
        for r_ in ROWS: r_["kin"] = KIN[r_["gal"]]
    KN_LIST = ["inclination -1 sigma", "inclination +1 sigma", "pressure (CO 15, Halpha 37 km/s)", "stars: no bulge", "stars: f_bul x2", "gas: R_e x0.6", "gas: R_e x1.5", "gas: point mass", "kpc/arcsec = 8.5", "rings: drop innermost of each line", "points: drop occluded", "kernel P2"]
    KGR = {"inclination -1 sigma": "inclination", "inclination +1 sigma": "inclination", "pressure (CO 15, Halpha 37 km/s)": "pressure", "stars: no bulge": "stellar geometry", "stars: f_bul x2": "stellar geometry", "gas: R_e x0.6": "gas geometry", "gas: R_e x1.5": "gas geometry", "gas: point mass": "gas geometry",
           "kpc/arcsec = 8.5": "scale", "rings: drop innermost of each line": "rings", "points: drop occluded": "rings", "kernel P2": "kernel"}
    gobs_of = lambda V, R: V ** 2 / R * H.G2SI

    def mc_row(r_, kin, B, rng):
        G = GAL[r_["gal"]]; n = len(r_["R"])
        i_d = np.clip(rng.normal(G["i0"], G["ei"], B), 20, 85); finc = (np.sin(math.radians(G["i0"])) / np.sin(np.radians(i_d)))[:, None]
        Vd = kin["V"][None, :] + kin["E"][None, :] * rng.normal(size=(B, n)); god = (Vd * finc) ** 2 / r_["R"][None, :] * H.G2SI
        Ms_d = (G["Ms"] * 10 ** rng.normal(0, SIGM, B))[:, None]; gbd = Ms_d * r_["gs_u"][None, :]
        if r_["Mg"] > 0: gbd = gbd + (r_["Mg"] * 10 ** rng.normal(0, SIGGAS, B))[:, None] * r_["gg_u"][None, :]
        Dd = god / gbd; lsd, ud = H.AI.implied(Dd, gbd, NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (np.median(Dd, axis=1) > 1.0)))
        dFd = np.median(np.log10(god / (gbd * NU(gbd / A0C))), axis=1); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    RES = {}
    for r_ in ROWS:
        lab = r_["label"]; G = GAL[r_["gal"]]; d = PTS[r_["gal"]]; kin = r_["kin"]; R = r_["R"]; gb0 = r_["gb0"]
        GO = gobs_of(kin["V"], R); D0 = GO / gb0; ls0, st0 = H.s_status(D0, gb0)
        rng = np.random.default_rng(zlib.crc32(("278|" + lab).encode()) % 100000)
        q, frn, frc, dq = mc_row(r_, kin, B_MC, rng)
        dF0 = float(np.median(np.log10(GO / (gb0 * NU(gb0 / A0C))))); bands = H.band_solutions(D0, gb0)
        sig_pt = np.where(d["is_ha"].values, SIG_HA, SIG_CO)

        def variant(nm):
            go, gb, nu, idx = GO, gb0, NU, np.ones(len(R), bool); Rv = R
            if nm == "inclination -1 sigma": go = GO * (math.sin(math.radians(G["i0"])) / math.sin(math.radians(G["i0"] - G["ei"]))) ** 2
            elif nm == "inclination +1 sigma": go = GO * (math.sin(math.radians(G["i0"])) / math.sin(math.radians(G["i0"] + G["ei"]))) ** 2
            elif nm == "pressure (CO 15, Halpha 37 km/s)": go = (kin["V"] ** 2 + 3.36 * sig_pt ** 2 * R / G["Re_disc"]) / R * H.G2SI
            elif nm == "stars: no bulge": gb = gb_row(G, R, r_["Mg"], fbul=0.0)
            elif nm == "stars: f_bul x2": gb = gb_row(G, R, r_["Mg"], fbul=min(0.9, 2 * G["fbul"]))
            elif nm == "gas: R_e x0.6":
                if r_["Mg"] <= 0: return None
                gb = gb_row(G, R, r_["Mg"], gre=0.6)
            elif nm == "gas: R_e x1.5":
                if r_["Mg"] <= 0: return None
                gb = gb_row(G, R, r_["Mg"], gre=1.5)
            elif nm == "gas: point mass":
                if r_["Mg"] <= 0: return None
                gb = gb_row(G, R, r_["Mg"], gas="pointmass")
            elif nm == "kpc/arcsec = 8.5":
                s_ = 8.5 / G["kpa"]; Rv = R * s_; go = gobs_of(kin["V"], Rv); gb = gb_row(G, Rv, r_["Mg"], scale=s_)
            elif nm == "rings: drop innermost of each line": idx = ~d["first_of_line"].values
            elif nm == "points: drop occluded":
                if not d["flag"].any(): return None
                idx = ~d["flag"].values
            elif nm == "kernel P2": nu = NUP2
            return go[idx], gb[idx], nu

        kn = {}
        for nm in KN_LIST:
            v = variant(nm)
            if v is None: continue
            go_, gb_, nu_ = v; lk, uk = H.s_star(go_ / gb_, gb_, nu_)
            kn[nm] = None if (st0 != "root" or uk) else lk - ls0; kn[nm + "|root"] = (not uk)
        grp = {}
        for nm in KN_LIST:
            if kn.get(nm) is not None: grp.setdefault(KGR[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm in KN_LIST if kn.get(nm + "|root")); n_k = sum(1 for nm in KN_LIST if nm + "|root" in kn)
        lv_nl, lf_nl = H.lever1(NU(gb0 / A0C), gb0); d1 = H.shift_to_s1(D0, gb0)
        pres_shift = float("nan") if SELFTEST else float(np.median(np.log10(((kin["V"] ** 2 + 3.36 * sig_pt ** 2 * R / G["Re_disc"]) / R * H.G2SI) / GO)))
        RES[lab] = dict(label=lab, gal=r_["gal"], branch=r_["branch"], role=r_["role"], z=G["z"], R=R.tolist(), GO=GO.tolist(), GB=gb0.tolist(), D=D0.tolist(), D_med=float(np.median(D0)), y=r_["y0"].tolist(), ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc,
                        delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, n_knobs=n_k, lever=lv_nl,
                        ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(D0), delta_to_s1=d1, pressure_median_shift_dex=pres_shift)
        R_ = RES[lab]
        b0 = (f"s* <= {10 ** ls0:.3g}" if st0 == "root" else ("FLOOR (D <= 1)" if st0 == "floor" else "CEILING (s* > 1000)"))
        qs = f"68 % [{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] 95 % [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "no draw interval (< 20 rooted draws)"
        P(f"  {lab:30s} N {len(R)} D_med {np.median(D0):.3f} (range {D0.min():.2f}-{D0.max():.2f}) dF {dF0:+.3f} y_med {np.median(r_['y0']):.2f}  {b0}; MC {qs} (no root {frn:.2f}, ceiling {frc:.2f}); to s*=1 {d1:+.2f} dex; recipe half-width {half:.3f} ({n_root}/{n_k} knobs rooted){' ILL' if R_['ill'] else ''}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg278_stageB_results.json")))["numbers"]["rows"]
        bad = 0.0; nroot = 0; n_gt1_m = 0; n_gt1_0 = 0
        for r_ in ROWS:
            R_ = RES[r_["label"]]; D0 = np.array(R_["D"]); gb = np.array(R_["GB"]); n_gt1_m += int(np.median(D0) > 1); n_gt1_0 += int(np.median(main[r_["label"]]["D"]) > 1)
            if R_["status"] == "root": nroot += 1; bad = max(bad, abs(float(np.median(np.log10(D0 / NU(gb / (A0C * 10 ** R_["ls"])))))))
        check("M2 MUTATE=1 (reactivity; the count is of rows with median D > 1, not of roots): V x 2 (g_obs x 4); rows with status ROOT satisfy the median-residual equation at their own s* to 1e-6 and the number of rows with median D > 1 is at least the main run's",
              f"rows with median D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max |median residual| {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for r_ in ROWS:
            R_ = RES[r_["label"]]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array(R_["D"])[None, :], np.array(R_["GB"])[None, :], NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r_ in ROWS if RES[r_['label']]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        check("M3 the six rows are present (two galaxies x three branches), with 15 and 10 points", f"{[(RES[r_['label']]['gal'], len(RES[r_['label']]['R'])) for r_ in ROWS]}", [len(RES[r_["label"]]["R"]) for r_ in ROWS] == [15] * 3 + [10] * 3)
        if not SELFTEST:
            means = {g: float(KIN[g]["V"].mean()) for g in GAL}; sds = {g: float(KIN[g]["V"].std(ddof=1)) for g in GAL}
            cnt = {g: sorted(int((PTS[g].line == l).sum()) for l in PTS[g].line.unique()) for g in GAL}
            check("M5 the digitised mean V_rot equals the paper's table value (254 and 336 km/s) within 1 km/s and the per-line counts equal 4/5/6 and 5/5", f"means {means}; SD {sds}; counts {cnt}",
                  all(abs(means[g] - GAL[g]["vbar_table"]) < 1.0 for g in GAL) and cnt["zC-400569"] == [4, 5, 6] and cnt["zC-488879"] == [5, 5])
            med6 = {}
            for g, G in GAL.items():
                Mg_dyn = G["alpha_dyn"] * G["L10"]; Mbar = G["Mstar_dyn"] + Mg_dyn; Mbul = G["mbul_mbar"] * Mbar; Mdisc = G["Mstar_dyn"] - Mbul; R = PTS[g]["Rkpc"].values
                gbm = Mbul * gsph_sersic(1.0, 4.0, G["Re_bul"], R) + Mdisc * np.asarray(H.gdisc(1.0, G["Re_disc"], R), float) + Mg_dyn * np.asarray(H.gdisc(1.0, G["Re_disc"], R), float); Vb = np.sqrt(gbm * R / H.G2SI)
                med6[g] = (float(np.median(np.abs(Vb / KIN[g]["V"] - 1))), float(np.median(Vb / KIN[g]["V"])), Mbul, Mdisc, Mg_dyn)
            check("M6 (validates my geometry against the authors' own baryon-only fits): with their fitted masses and my geometry the baryonic V at the digitised radii reproduces V_rot with median |V_bar/V_rot - 1| <= 0.25 in each galaxy", "; ".join(f"{g}: median |ratio - 1| {v[0]:.3f} (median ratio {v[1]:.3f}; M_bul {v[2]:.2e}, M_disc {v[3]:.2e}, M_gas {v[4]:.2e})" for g, v in med6.items()), all(v[0] <= 0.25 for v in med6.values()))
        else:
            tested = [r_["label"] for r_ in ROWS if RES[r_["label"]]["status"] == "root" and not RES[r_["label"]]["ill"]]
            inside = [t for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4]]
            if tested: check("SELFTEST: the conditioned rooted rows return the fabricated truth (s = 2) inside their 95 % interval", f"{len(inside)} of {len(tested)} inside; rows {[(t, 't' if t in inside else 'OUT') for t in tested]}", len(inside) == len(tested))
            else: check("SELFTEST: no row is both rooted and conditioned in the fabricated world: the coverage statement is not evaluated; the 100-world repeat below is the reported evidence", f"ill rows {sum(RES[r_['label']]['ill'] for r_ in ROWS)} of 6", True, load_bearing=False)
            rep = {}
            for r_ in ROWS:
                inn = 0; nroot_w = 0; nfloor = 0
                for w in range(100):
                    rw = np.random.default_rng(100000 + 1000 * LAB2I[r_["label"]] + w); gtw = r_["gb0"] * NU(r_["gb0"] / (2.0 * A0C)) * 10 ** rw.normal(0, 0.15, len(r_["R"])); Vw = np.sqrt(gtw * r_["R"] / H.G2SI)
                    lsw, stw = H.s_status(gtw / r_["gb0"], r_["gb0"]); nfloor += int(stw == "floor")
                    qw, _, _, _ = mc_row(r_, dict(V=Vw, E=0.10 * Vw), 1000, rw)
                    if stw == "root" and np.isfinite(qw[0]): nroot_w += 1; inn += int(qw[0] <= math.log10(2.0) <= qw[4])
                rep[r_["label"]] = (inn, nroot_w, nfloor); P(f"  SELFTEST repeat (reported): {r_['label']}: the 95 % interval contains s = 2 in {inn} of {nroot_w} fabricated worlds with a root ({nfloor} of 100 worlds at the floor)")
            NUM["selftest_repeat"] = rep
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 7; HE1-HE3 were scored at stage A) scored:")
        a = [RES[f"zC-400569 [{b}]"] for b in ALPHA]; b_ = [RES[f"zC-488879 [{b}]"] for b in ALPHA]; m567 = [ok for n_, ok, lb in CHK if n_.startswith(("M5", "M6"))]
        he = {"HE4": bool(all(r["status"] == "floor" and 0.3 <= r["D_med"] <= 0.8 for r in a)), "HE5": bool(all(r["status"] == "root" and 2 <= r["D_med"] <= 8 and 5 <= r["s"] <= 150 for r in b_)),
              "HE6": bool(all(abs(r["pressure_median_shift_dex"]) <= 0.02 for r in a + b_)), "HE7": bool(len(m567) == 2 and all(m567))}
        P(f"    HE4: zC-400569 statuses {[r['status'] for r in a]} D_med {[round(r['D_med'], 3) for r in a]} (all floor, 0.3-0.8): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: zC-488879 statuses {[r['status'] for r in b_]} D_med {[round(r['D_med'], 3) for r in b_]} (2-8), s* {[round(r['s'], 3) for r in b_]} (5-150): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: the pressure knob moves the median g_obs by {[round(r['pressure_median_shift_dex'], 4) for r in a + b_]} dex (needs <= 0.02): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE7: M5 and M6 {'hold' if he['HE7'] else 'do not both hold'}: {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    pcols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling", "delta_floor", "delta_to_s1", "status", "galaxy", "branch", "role", "R_kpc", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r_ in ROWS:
        R_ = RES[r_["label"]]; st = R_["status"]; q = R_["q"]; G = GAL[r_["gal"]]; z_ = G["z"]
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(z_, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]
        extra = [float(np.median(R_["y"])), R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D_med"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], R_["delta_floor"], R_["delta_to_s1"], st, R_["gal"], R_["branch"], R_["role"], "/".join(f"{v:.2f}" for v in R_["R"])]
        q_ = ("ILL-CONDITIONED; " if R_["ill"] else "") + {"root": "has a root: an UPPER bound on s* (vacuous if far above 1)", "floor": "FLOOR: no root, median D <= 1 (the baryons exceed the dynamics at the median point): robust against any higher baryon set",
                                                         "ceiling": f"CEILING: median D = {R_['D_med']:.2f} > 1 but s* > 1000: vacuous upper bound, NOT a floor"}[st] \
            + "; SED stellar mass vs the authors' dynamical value differs by x2.8 (zC-400569, SED higher) and x4 (zC-488879, SED lower); CO conversion factor 0.4-4.3; bulge fraction from the authors' dynamical fit; correlated multi-line points" + ("; RECOMMENDED CHART ROW by the frozen rule" if r_["branch"] == "stars+CO a=0.4" else "")
        sstar = R_["s"]
        lim = "baryons are a lower limit (no gas): s* is an upper bound" if r_["branch"] == "stars" else "class S gas with a bracketing conversion factor: not a measurement"
        rows.append(["CFG278", R_["label"], ("D (no gas; stars-only lower limit)" if r_["branch"] == "stars" else f"S (CO gas, alpha_CO {r_['alpha']}; SED stars)"), f"{z_:.4f}", f"{z_:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], lim, fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg278_points{SFX}.csv"), pcols, rows)
    P(f"\n  points written: cfg278_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg278{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg278{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
