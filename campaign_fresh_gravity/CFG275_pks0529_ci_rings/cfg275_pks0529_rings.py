#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG275 -- implied-a0 rows for PKS 0529-549 (z = 2.5706) from the five-ring [CI](2-1) circular-velocity curve of Lin et al. (arXiv:2411.08958):
independent baryons, eight stellar x gas branches never pooled (SED 3e11 or the preliminary CIGALE range 0.4-1.2e11 for the stars; none / CO / [CI] / dust for the gas).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG275_pks0529_ci_rings/FROZEN_CRITERIA.md (4108d99e9).
  g_obs   V_c^2 / R, V_c = the authors' asymmetric-drift-corrected circular velocity (digitised from the vector figures), split-normal errors, inclination 53 +- 5 deg
  g_bar   stars: the authors' MaxDisk geometry (Freeman disc R_e 4.7 kpc + de Vaucouleurs bulge R_e 0.47 kpc, B/D = 0.9); gas: a razor-thin Sersic disc (n 0.52, R_e 2.57 kpc) by a Hankel transform
  STAGE=A   the blind pre-flight: no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A, the SELFTEST and this script are committed); STAGE=B SELFTEST=1; STAGE=B MUTATE=1 (V_c x 2).
Run: STAGE=A python3 .../cfg275_pks0529_rings.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, re
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import j0, j1, ive, gammainc, gammaln
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V_c x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V_c on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
LOADVEL = (STAGE == "B") and not SELFTEST                                   # the SELFTEST never loads the real velocity-bearing columns
CSVP = os.path.join(HERE, "lin2024_rings_digitised.csv")
TEXP = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src", "2411.08958", "aanda.tex")
MTP = os.path.join(REPO, "data_assembly", "multitracer_gas", "singles_multitracer_galaxies.csv")

# ---------------------------------------------------------------- constants frozen in the criteria (section 3)
Z0 = 2.5706
KPA = 8.22                                                                  # kpc / arcsec stated by Lin+
INC0, EINC = 53.0, 5.0
GAS_N, GAS_RE = 0.52, 2.57                                                  # the [CI](2-1) Sersic profile
DUST_N, DUST_RE = 1.3, 4.7
BULGE_N, BULGE_RE, DISC_RE, BD = 4.0, 0.47, 4.7, 0.9                        # MaxDisk: disc R_e = R_e,dust, bulge R_e = 0.1 R_e,dust, B/D = 0.9
FB = BD / (1.0 + BD)
SIGGAS = 0.213                                                              # CFG237's class S/L inner band half-width, dex
STELL = {"SED": dict(lm=math.log10(3e11), elm=0.30, role="literature stellar mass"), "CIG": dict(lm=math.log10(math.sqrt(0.4e11 * 1.2e11)), elm=0.24, role="preliminary stellar range")}
GASB = {"none": None, "CO": 7.3e10, "CI": 3.1e11, "dust": 2.2e11}
GCLASS = {"none": "D", "CO": "S", "CI": "S", "dust": "L"}
ROWS = [dict(label=f"PKS0529 [{st}; {gs}]", st=st, gs=gs, role=STELL[st]["role"]) for st in ("SED", "CIG") for gs in ("none", "CO", "CI", "dust")]
LAB2I = {r["label"]: i for i, r in enumerate(ROWS)}

# ---------------------------------------------------------------- loading (stage A: radius columns only)
cols = ["series", "ring", "R_arcsec", "R_kpc"] + (["V_kms", "err_lo_kms", "err_hi_kms"] if LOADVEL else [])
df = pd.read_csv(CSVP, usecols=cols)
SER = {"fit": "V_c (mass-model fit input)", "const": "V_c (constant sigma_v)", "var": "V_c (varying sigma_v)", "rot": "V_rot (3DFIT)"}
sub = {k: df[df["series"] == v].sort_values("ring").reset_index(drop=True) for k, v in SER.items()}
RING_R = sub["fit"]["R_kpc"].values.astype(float)
NR = len(RING_R)
P(f"digitised rings {os.path.basename(CSVP)} sha256 {H.sha(CSVP)}; multitracer row file {H.sha(MTP)}; velocity-bearing columns loaded: {LOADVEL}; rings R = {np.array2string(RING_R, precision=3)} kpc")

# ---------------------------------------------------------------- geometry (all in m s^-2 per Msun)
def b_proj(n):
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n ** 2)


def sigma_unit(R, n, Re):
    b = b_proj(n); Se = 1.0 / (2 * math.pi * n * math.exp(b) * b ** (-2 * n) * math.exp(gammaln(2 * n)) * Re ** 2)
    return Se * np.exp(-b * ((R / Re) ** (1.0 / n) - 1.0))


_HC = {}


def hankel_g_unit(n, Re, Rk, NRp=4000, Rmax_f=14.0, NK=24000, Kmax_f=60.0, chunk=2000):
    """radial acceleration (m s^-2) of a razor-thin Sersic disc of total mass 1 Msun at radii Rk (kpc): g = 2 pi G int k J1(kR) S~(k) dk, S~(k) = int Sigma J0(kR') R' dR'."""
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


def gauss_closed(s, R):                                                     # exact Gaussian thin disc, total mass 1 Msun, m s^-2
    x = R ** 2 / (4 * s ** 2)
    return H.G_KPC * math.sqrt(math.pi / 2) * R / (2 * s ** 3) * (ive(0, x) - ive(1, x)) * H.G2SI


def p_dep(n):
    return 1 - 0.6097 / n + 0.05563 / n ** 2


def b_dep(n):
    return 2 * n - 1 / 3 + 0.009876 / n


def fenc_sph(r, n, Re):                                                     # Terzic & Graham deprojected-Sersic enclosed fraction (as Lin+)
    return gammainc(n * (3 - p_dep(n)), b_dep(n) * (np.asarray(r, float) / Re) ** (1.0 / n))


def gsph_sersic(M, n, Re, R):
    R = np.asarray(R, float)
    return H.G_KPC * M * fenc_sph(R, n, Re) / R ** 2 * H.G2SI


def g_star_unit(R, kind="maxdisk"):
    R = np.asarray(R, float)
    if kind == "maxdisk": return (1 - FB) * np.asarray(H.gdisc(1.0, DISC_RE, R), float) + FB * gsph_sersic(1.0, BULGE_N, BULGE_RE, R)
    if kind == "sph4": return gsph_sersic(1.0, 4.0, 1.0, R)
    if kind == "sph56": return gsph_sersic(1.0, 5.6, 3.0, R)
    if kind == "disc47": return np.asarray(H.gdisc(1.0, DISC_RE, R), float)
    raise KeyError(kind)


def g_gas_unit(R, kind="sersic_thin"):
    R = np.asarray(R, float)
    if kind == "sersic_thin": return hankel_g_unit(GAS_N, GAS_RE, R)
    if kind == "exp": return np.asarray(H.gdisc(1.0, GAS_RE, R), float)
    if kind == "dust": return hankel_g_unit(DUST_N, DUST_RE, R)
    if kind == "pointmass": return H.G_KPC * gammainc(2 * GAS_N, b_proj(GAS_N) * (R / GAS_RE) ** (1.0 / GAS_N)) / R ** 2 * H.G2SI
    raise KeyError(kind)


for r_ in ROWS:
    r_["Ms"] = 10 ** STELL[r_["st"]]["lm"]; r_["Mg"] = GASB[r_["gs"]] or 0.0
    r_["gs_u"] = g_star_unit(RING_R); r_["gg_u"] = g_gas_unit(RING_R) if r_["gs"] != "none" else np.zeros(NR)
    r_["gb0"] = r_["Ms"] * r_["gs_u"] + r_["Mg"] * r_["gg_u"]; r_["y0"] = r_["gb0"] / A0C
P(f"PKS 0529-549: z {Z0}, {NR} rings, inclination {INC0:.0f} +- {EINC:.0f} deg, gas Sersic n {GAS_N} R_e {GAS_RE} kpc, MaxDisk stars (disc R_e {DISC_RE}, bulge n {BULGE_N} R_e {BULGE_RE}, B/D {BD}); stellar branches " + "; ".join(f"{k} log M* {v['lm']:.3f} +- {v['elm']}" for k, v in STELL.items()) + "; gas " + "; ".join(f"{k} {v:.3g}" for k, v in GASB.items() if v))


def inc_factor(i_deg):
    return math.sin(math.radians(INC0)) / np.sin(np.radians(i_deg))


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity-bearing column is loaded; no g_obs, D, delta or s* is formed)")
    tex = open(TEXP, encoding="utf-8", errors="ignore").read(); comp = re.sub(r"\s+", "", tex)
    TXT = ["Gas&$0.52\\pm0.01$&$0.313\\pm0.003$&$2.57\\pm0.02$", "Dust&$1.3\\pm0.2$&$0.57\\pm0.04$&$4.7\\pm0.3$", "&$53\\pm5$", "1arcseccorrespondsto8.22kpc", "widthofeachringis0.09arcsec", "Starsonly&$53.0_{-4.9}^{+4.8}$&...&$10.5_{-4.2}^{+3.4}$", "$5.6_{-2.0}^{+2.3}$&$3.0_{-1.5}^{+1.4}$",
           "Gasonly&$53.0_{-4.9}^{+4.8}$&$8.5_{-1.6}^{+1.7}$", "$0.4\\times10^{11}$to$1.2\\times10^{11}$", "$7.3\\pm0.9\\times10^{10}$"]
    found = [t in comp for t in TXT]
    d_ = pd.read_csv(CSVP, usecols=["series", "ring", "R_arcsec", "R_kpc"])
    ok_rows = len(d_) == 20 and all((d_["series"] == v).sum() == 5 for v in SER.values())
    ok_R = all(np.allclose(sub[k]["R_arcsec"].values, 0.045 + 0.09 * np.arange(5), atol=1e-4) for k in SER) and np.allclose(sub["fit"]["R_kpc"].values, (0.045 + 0.09 * np.arange(5)) * KPA, atol=2e-3)
    kpa = H.kpc_per_arcsec(Z0)
    check("C1 CONTROL (loader): the digitised CSV has 20 rows = 4 series x 5 rings; radii equal 0.045 + 0.09 k arcsec (1e-4) and x 8.22 kpc (2e-3) in every series; the cosmology gives 8.22 kpc/arcsec at z = 2.5706 to 0.01",
          f"rows {len(d_)}, per-series counts ok {ok_rows}; radii ok {ok_R}; kpc/arcsec {kpa:.4f}", ok_rows and ok_R and abs(kpa - 8.22) < 0.01)
    check("C1b CONTROL: the paper's constants are found verbatim in the TeX (gas / dust Sersic rows, i = 53 +- 5, 8.22 kpc per arcsec, the 0.09-arcsec rings, the stars-only and gas-only table rows, the 0.4-1.2e11 CIGALE range, the CO gas mass)", f"found {sum(found)} of {len(TXT)}: {found}", all(found))
    mt = pd.read_csv(MTP); mr = mt[mt["galaxy"] == "PKS 0529-549"]
    mstr = str(mr["stated_gas_masses_and_conversions"].iloc[0]) if len(mr) else ""
    need = ["[CI] 3.1+-0.6e11", "CO 0.73+-0.09e11", "dust 2.2+-0.2e11", "M* ~3+-2e11"]
    check("C1c CONTROL: the on-disk multitracer row (arXiv:2411.04290 Table 5) holds the frozen constants (CI 3.1 +- 0.6, CO 0.73 +- 0.09, dust 2.2 +- 0.2, M* ~ 3 +- 2, all 1e11) and z = 2.5725; the frozen CO mass (7.3e10) equals 0.73e11", f"row found {len(mr)}; strings {[s in mstr for s in need]}; z {float(mr['z'].iloc[0]) if len(mr) else float('nan')}", len(mr) == 1 and all(s in mstr for s in need) and abs(float(mr["z"].iloc[0]) - 2.5725) < 1e-9 and abs(GASB["CO"] - 0.73e11) < 1)
    g_h1 = hankel_g_unit(1.0, 2.57, RING_R); g_f = np.array([float(H.gdisc(1.0, 2.57, r)) for r in RING_R]); d1 = float(np.max(np.abs(g_h1 / g_f - 1)))
    s_g = 2.57 / math.sqrt(2 * b_proj(0.5)); g_h5 = hankel_g_unit(0.5, 2.57, RING_R); g_c = np.array([gauss_closed(s_g, r) for r in RING_R]); d5 = float(np.max(np.abs(g_h5 / g_c - 1)))
    d_half = {}
    for n_ in (4.0, 5.6):
        p_, b_ = p_dep(n_), b_dep(n_); a_ = n_ * (3 - p_)
        rho = lambda r: (r) ** (-p_) * np.exp(-b_ * r ** (1.0 / n_))
        Sg = lambda Rp: 2.0 * quad(lambda t: rho(math.sqrt(Rp ** 2 + t ** 2)), 0, np.inf, limit=200)[0]
        norm = math.exp(gammaln(a_)) * n_ * b_ ** (-a_) * 4 * math.pi
        d_half[n_] = quad(lambda Rp: 2 * math.pi * Rp * Sg(Rp), 0, 1.0, limit=200)[0] / norm
    d_inf = float(abs(fenc_sph(1e4, 4.0, 1.0) - 1) + abs(fenc_sph(1e4, 5.6, 3.0) - 1))
    check("C2 CONTROL (geometry): the Hankel thin disc equals Freeman's exact exponential disc (n = 1) to 2e-3 and the exact Gaussian-disc closed form (n = 0.5, R_e = 2.57) to 2e-3 at the five radii; the deprojected-Sersic profile's projected half-mass radius equals R_e to 1 % for n = 4 and 5.6 (numerical projection); the enclosed fraction tends to 1; the stellar B/D partition sums to 1",
          f"Hankel vs Freeman {d1:.1e}; Hankel vs Gaussian {d5:.1e}; projected fraction within R_e: n=4 {d_half[4.0]:.4f}, n=5.6 {d_half[5.6]:.4f}; |f(inf) - 1| {d_inf:.1e}; partition {(1 - FB) + FB}",
          d1 < 2e-3 and d5 < 2e-3 and all(abs(v - 0.5) < 0.005 for v in d_half.values()) and d_inf < 1e-6 and abs((1 - FB) + FB - 1) < 1e-12)
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
        P(f"    {r_['label']:24s} g_bar {np.array2string(r_['gb0'], precision=3)} m/s^2; y {np.array2string(r_['y0'], precision=3)}; lever {lv:+.2f}{' (not computable)' if fl else ''}  {'ILL-CONDITIONED' if r_['ill'] else 'conditioned'}")
    ymin = min(float(r_["y0"].min()) for r_ in ROWS); ymax = max(float(r_["y0"].max()) for r_ in ROWS)
    P(f"    CFG240: y(B) spans {ymin:.1f} to {ymax:.1f} over all rows and rings (the break-even design needs y >~ 8 with deep points, y < 0.3: none here); T4 floor 3 sigma / sqrt(N) at sigma = 0.2 dex is {3 * 0.2 / math.sqrt(5):.2f} dex for N = 5 and {3 * 0.2 / math.sqrt(2.75):.2f} dex for N_eff = 2.75 (calibration free)")
    P("\nA3  KNOB EFFECTS ON g_bar BY RING (dex relative to the baseline; stars at unit mass, gas at unit mass)")
    for nm, f_ in (("stars: sph n=4 R_e=1", lambda: g_star_unit(RING_R, "sph4") / g_star_unit(RING_R)), ("stars: sph n=5.6 R_e=3.0", lambda: g_star_unit(RING_R, "sph56") / g_star_unit(RING_R)), ("stars: exp disc R_e=4.7", lambda: g_star_unit(RING_R, "disc47") / g_star_unit(RING_R)),
                   ("gas: exp disc R_e=2.57", lambda: g_gas_unit(RING_R, "exp") / g_gas_unit(RING_R)), ("gas: dust profile", lambda: g_gas_unit(RING_R, "dust") / g_gas_unit(RING_R)), ("gas: point mass", lambda: g_gas_unit(RING_R, "pointmass") / g_gas_unit(RING_R))):
        P(f"    {nm}: {np.array2string(np.log10(f_()), precision=3)} dex")
    HWHM = 0.5 * 0.18 * KPA
    P(f"\nA4  THE BEAM ([CI](2-1) beam 0.18 arcsec = {0.18 * KPA:.2f} kpc FWHM, HWHM {HWHM:.2f} kpc; ring width 0.09 arcsec = half the beam): R/HWHM = {np.array2string(RING_R / HWHM, precision=2)}; rings inside the HWHM: {int((RING_R < HWHM).sum())} of {NR}; N_eff of the correlated rings ~ 2.5-3")
    f_gas = gammainc(2 * GAS_N, b_proj(GAS_N) * (RING_R / GAS_RE) ** (1.0 / GAS_N)); f_bul = fenc_sph(RING_R, BULGE_N, BULGE_RE); x_ = RING_R / (DISC_RE / H.XN); f_disc = 1 - (1 + x_) * np.exp(-x_)
    P(f"A5  ENCLOSED FRACTIONS at the rings: gas (projected Sersic) {np.array2string(f_gas, precision=3)}; bulge {np.array2string(f_bul, precision=3)}; stellar disc {np.array2string(f_disc, precision=3)}")

    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C4)")
    P("  PF-D2 ILL-CONDITIONED rows: " + (", ".join(r_["label"] for r_ in ROWS if r_["ill"]) or "none"))
    P("  PF-D3 DRAWABLE as an upper bound: " + (", ".join(r_["label"] for r_ in ROWS if pfd1 and not r_["ill"]) or "none") + " (every drawable row is an upper bound on s*, never a measurement)")
    pfd4 = bool(RING_R[0] < HWHM)
    P(f"  PF-D4 BEAM-LIMITED: {pfd4} (the innermost ring at {RING_R[0]:.2f} kpc against the beam HWHM {HWHM:.2f} kpc; reported, not blocking)")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE4-HE8 are scored at stage B):")
    rA, rB = ROWS[LAB2I["PKS0529 [SED; CO]"]], ROWS[LAB2I["PKS0529 [CIG; none]"]]
    gg3 = float(hankel_g_unit(GAS_N, GAS_RE, np.array([RING_R[-1]]))[0]) * 1e11
    he = {"HE1": bool(15 <= rA["y0"][-1] <= 50 and 3 <= rB["y0"][-1] <= 9), "HE2": bool(all(r_["ill"] for r_ in ROWS)), "HE3": bool(7.5e-10 <= gg3 <= 1.1e-9)}
    P(f"    HE1: y at the outer ring: [SED; CO] {rA['y0'][-1]:.1f} (needs 15-50), [CIG; none] {rB['y0'][-1]:.2f} (needs 3-9): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}")
    P(f"    HE2: all eight rows ILL-CONDITIONED ({sum(r_['ill'] for r_ in ROWS)} of 8): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
    P(f"    HE3: thin-disc Sersic gas g at R = {RING_R[-1]:.2f} kpc for 1e11 Msun = {gg3:.3e} m/s^2 (needs 7.5e-10 to 1.1e-9): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(z=Z0, rings_R=RING_R.tolist(), inc=[INC0, EINC], kpc_per_arcsec=KPA, gas=[GAS_N, GAS_RE], dust=[DUST_N, DUST_RE], maxdisk=dict(disc_Re=DISC_RE, bulge_n=BULGE_N, bulge_Re=BULGE_RE, BD=BD), stellar=STELL, gas_masses=GASB, sig_gas_dex=SIGGAS, hwhm_kpc=HWHM),
               rows={r_["label"]: dict(gb0=r_["gb0"].tolist(), y0=r_["y0"].tolist(), lever=r_["lever"], ill=r_["ill"]) for r_ in ROWS}, enclosed=dict(gas=f_gas.tolist(), bulge=f_bul.tolist(), disc=f_disc.tolist()), hand_estimates=he, pf=dict(PF_D1=bool(pfd1), PF_D4=pfd4),
               controls_numbers=dict(hankel_vs_freeman=d1, hankel_vs_gaussian=d5, half_mass_n4=d_half[4.0], half_mass_n56=d_half[5.6]))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_c x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2750)
    if SELFTEST:
        gt = {r_["label"]: r_["gb0"] * NU(r_["gb0"] / (2.0 * A0C)) * 10 ** rngS.normal(0, 0.15, NR) for r_ in ROWS}
        KV = {r_["label"]: dict(V=np.sqrt(gt[r_["label"]] * RING_R / H.G2SI)) for r_ in ROWS}
        for k_ in KV.values(): k_["elo"] = k_["ehi"] = 0.10 * k_["V"]
        P("SELFTEST: V_c fabricated from the law at s_true = 2 on each row's own baryons (+0.15 dex scatter), 10 % errors; the real velocity-bearing columns are not even loaded")
    else:
        V_fit, ELO, EHI = sub["fit"]["V_kms"].values.astype(float), sub["fit"]["err_lo_kms"].values.astype(float), sub["fit"]["err_hi_kms"].values.astype(float)
        V_con, V_var = sub["const"]["V_kms"].values.astype(float), sub["var"]["V_kms"].values.astype(float)
        V_rot, ER_lo, ER_hi = sub["rot"]["V_kms"].values.astype(float), sub["rot"]["err_lo_kms"].values.astype(float), sub["rot"]["err_hi_kms"].values.astype(float)
        if MUTATE: V_fit, ELO, EHI, V_con, V_var, V_rot = 2.0 * V_fit, 2.0 * ELO, 2.0 * EHI, 2.0 * V_con, 2.0 * V_var, 2.0 * V_rot
        KV = {r_["label"]: dict(V=V_fit, elo=ELO, ehi=EHI) for r_ in ROWS}
    g_of = lambda V, R=RING_R: (np.asarray(V, float) ** 2 / R * H.G2SI)
    KN_LIST = ["g_obs: V_c varying sigma", "g_obs: V_rot (no ADC)", "inclination 48 deg", "inclination 58 deg", "stars: sph n=4 R_e=1", "stars: sph n=5.6 R_e=3.0", "stars: exp disc R_e=4.7", "gas: exp disc R_e=2.57", "gas: dust profile", "gas: point mass", "rings 3-5 only", "kernel P2"]
    KGR = {"g_obs: V_c varying sigma": "kinematics", "g_obs: V_rot (no ADC)": "kinematics", "inclination 48 deg": "inclination", "inclination 58 deg": "inclination", "stars: sph n=4 R_e=1": "stellar geometry", "stars: sph n=5.6 R_e=3.0": "stellar geometry", "stars: exp disc R_e=4.7": "stellar geometry",
           "gas: exp disc R_e=2.57": "gas geometry", "gas: dust profile": "gas geometry", "gas: point mass": "gas geometry", "rings 3-5 only": "rings", "kernel P2": "kernel"}

    def mc_row(r_, kv, B, rng):
        n = NR
        i_d = np.clip(rng.normal(INC0, EINC, B), 20, 85); finc = (np.sin(math.radians(INC0)) / np.sin(np.radians(i_d)))[:, None]
        Vd = H.split_normal(rng, kv["V"][None, :], kv["ehi"][None, :], kv["elo"][None, :], (B, n)); god = (Vd * finc) ** 2 / RING_R[None, :] * H.G2SI
        Ms_d = (r_["Ms"] * 10 ** rng.normal(0, STELL[r_["st"]]["elm"], B))[:, None]; gbd = Ms_d * r_["gs_u"][None, :]
        if r_["gs"] != "none": gbd = gbd + (r_["Mg"] * 10 ** rng.normal(0, SIGGAS, B))[:, None] * r_["gg_u"][None, :]
        Dd = god / gbd; lsd, ud = H.AI.implied(Dd, gbd, NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (np.median(Dd, axis=1) > 1.0)))
        dFd = np.median(np.log10(god / (gbd * NU(gbd / A0C))), axis=1); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    RES = {}
    for r_ in ROWS:
        lab = r_["label"]; kv = KV[lab]; gb0 = r_["gb0"]; has_gas = r_["gs"] != "none"
        GO = g_of(kv["V"]); D0 = GO / gb0; ls0, st0 = H.s_status(D0, gb0)
        rng = np.random.default_rng(zlib.crc32(("275|" + lab).encode()) % 100000)
        q, frn, frc, dq = mc_row(r_, kv, B_MC, rng)
        dF0 = float(np.median(np.log10(GO / (gb0 * NU(gb0 / A0C))))); bands = H.band_solutions(D0, gb0)

        def variant(nm):
            go, gb, nu, idx = GO, gb0, NU, slice(None)
            if nm == "g_obs: V_c varying sigma":
                if SELFTEST: return None
                go = g_of(V_var)
            elif nm == "g_obs: V_rot (no ADC)":
                if SELFTEST: return None
                go = g_of(V_rot)
            elif nm in ("inclination 48 deg", "inclination 58 deg"): go = GO * inc_factor(float(nm.split()[1])) ** 2
            elif nm.startswith("stars:"):
                kind = {"stars: sph n=4 R_e=1": "sph4", "stars: sph n=5.6 R_e=3.0": "sph56", "stars: exp disc R_e=4.7": "disc47"}[nm]; gb = r_["Ms"] * g_star_unit(RING_R, kind) + r_["Mg"] * r_["gg_u"]
            elif nm.startswith("gas:"):
                if not has_gas: return None
                kind = {"gas: exp disc R_e=2.57": "exp", "gas: dust profile": "dust", "gas: point mass": "pointmass"}[nm]; gb = r_["Ms"] * r_["gs_u"] + r_["Mg"] * g_gas_unit(RING_R, kind)
            elif nm == "rings 3-5 only": idx = slice(2, None)
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
        kin_shift = {}
        if not SELFTEST:
            for nm_, Vx in (("V_c constant", V_con), ("V_c varying", V_var), ("V_rot", V_rot)): kin_shift[nm_] = float(np.median(np.log10(g_of(Vx) / GO)))
        RES[lab] = dict(label=lab, stellar=r_["st"], gas=r_["gs"], role=r_["role"], z=Z0, R=RING_R.tolist(), GO=GO.tolist(), GB=gb0.tolist(), D=D0.tolist(), D_med=float(np.median(D0)), y=r_["y0"].tolist(), ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc,
                        delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, n_knobs=n_k, lever=lv_nl,
                        ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(D0), delta_to_s1=d1, kin_median_shift_dex=kin_shift)
        R_ = RES[lab]
        b0 = (f"s* <= {10 ** ls0:.3g}" if st0 == "root" else ("FLOOR (D <= 1)" if st0 == "floor" else "CEILING (s* > 1000)"))
        qs = f"68 % [{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] 95 % [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "no draw interval (< 20 rooted draws)"
        P(f"  {lab:24s} D {np.array2string(D0, precision=3)}  D_med {np.median(D0):.3f}  dF {dF0:+.3f}  y {np.array2string(r_['y0'], precision=3)}  {b0}; MC {qs} (no root {frn:.2f}, ceiling {frc:.2f}); to s*=1 {d1:+.2f} dex; recipe half-width {half:.3f} ({n_root}/{n_k} knobs rooted){' ILL' if R_['ill'] else ''}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg275_stageB_results.json")))["numbers"]["rows"]
        bad = 0.0; nroot = 0; n_gt1_m = 0; n_gt1_0 = 0
        for r_ in ROWS:
            R_ = RES[r_["label"]]; D0 = np.array(R_["D"]); gb = np.array(R_["GB"]); n_gt1_m += int(np.median(D0) > 1); n_gt1_0 += int(np.median(main[r_["label"]]["D"]) > 1)
            if R_["status"] == "root": nroot += 1; bad = max(bad, abs(float(np.median(np.log10(D0 / NU(gb / (A0C * 10 ** R_["ls"])))))))
        check("M2 MUTATE=1 (reactivity; the count is of rows with median D > 1, not of roots): V_c x 2 (g_obs x 4); rows with status ROOT satisfy the median-residual equation at their own s* to 1e-6 and the number of rows with median D > 1 is at least the main run's",
              f"rows with median D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max |median residual| {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for r_ in ROWS:
            R_ = RES[r_["label"]]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array(R_["D"])[None, :], np.array(R_["GB"])[None, :], NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r_ in ROWS if RES[r_['label']]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        roles = [RES[r_["label"]]["role"] for r_ in ROWS]
        check("M3 the eight rows are present with their roles (four literature stellar mass, four preliminary stellar range) and five radii each", f"{roles}; ring counts {[len(RES[r_['label']]['R']) for r_ in ROWS]}", roles == ["literature stellar mass"] * 4 + ["preliminary stellar range"] * 4 and all(len(RES[r_['label']]['R']) == 5 for r_ in ROWS))
        if not SELFTEST:
            ok5 = bool(all(np.all(np.abs(Vx - V_rot) <= np.maximum(ER_lo, ER_hi)) for Vx in (V_con, V_var)))
            check("M5 the digitised V_rot, V_c (constant sigma_v) and V_c (varying sigma_v) agree pointwise within the digitised V_rot error bars (the paper: 'consistent within the errors')", f"max |V_c - V_rot| / error: constant {float(np.max(np.abs(V_con - V_rot) / np.maximum(ER_lo, ER_hi))):.2f}, varying {float(np.max(np.abs(V_var - V_rot) / np.maximum(ER_lo, ER_hi))):.2f}", ok5)
            Vg = np.sqrt(8.5e10 * g_gas_unit(RING_R) * RING_R / H.G2SI); mg = float(np.median(np.abs(Vg[2:] / V_fit[2:] - 1)))
            check("M6 (validates my gas geometry against the authors' own fit): the thin-disc Sersic gas with the gas-only M_gas = 8.5e10 reproduces V_c at rings 3-5 with median |V_gas/V_c - 1| <= 0.25", f"V_gas/V_c at rings 3-5: {np.array2string(Vg[2:] / V_fit[2:], precision=3)}; median |ratio - 1| {mg:.3f}", mg <= 0.25)
            Vs = np.sqrt(1.05e11 * gsph_sersic(1.0, 5.6, 3.0, RING_R) * RING_R / H.G2SI); ms = float(np.median(np.abs(Vs[2:] / V_fit[2:] - 1)))
            check("M7 (validates my stellar function against the authors' own fit): the spherical Sersic with the stars-only best fit (M = 1.05e11, n = 5.6, R_e = 3.0 kpc) reproduces V_c at rings 3-5 with median |V_*/V_c - 1| <= 0.25", f"V_*/V_c at rings 3-5: {np.array2string(Vs[2:] / V_fit[2:], precision=3)}; median |ratio - 1| {ms:.3f}", ms <= 0.25)
        else:
            tested = [r_["label"] for r_ in ROWS if RES[r_["label"]]["status"] == "root" and not RES[r_["label"]]["ill"]]
            inside = [t for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4]]
            if tested:
                check("SELFTEST: the conditioned rooted rows return the fabricated truth (s = 2) inside their 95 % interval for at least min(4, number of such rows) of them", f"{len(inside)} of {len(tested)} inside; rows {[(t, 't' if t in inside else 'OUT') for t in tested]}", len(inside) >= min(4, len(tested)))
            else:
                check("SELFTEST: no row is both rooted and conditioned in the fabricated world (every row is ILL-CONDITIONED or has no root): the coverage statement is not evaluated; the 100-world repeat below is the reported evidence", f"rooted rows {[r_['label'] for r_ in ROWS if RES[r_['label']]['status'] == 'root']}; ill rows {sum(RES[r_['label']]['ill'] for r_ in ROWS)} of 8", True, load_bearing=False)
            rep = {}
            for r_ in ROWS:
                inn = 0; nroot_w = 0; nfloor = 0
                for w in range(100):
                    rw = np.random.default_rng(100000 + 1000 * LAB2I[r_["label"]] + w); gtw = r_["gb0"] * NU(r_["gb0"] / (2.0 * A0C)) * 10 ** rw.normal(0, 0.15, NR); Vw = np.sqrt(gtw * RING_R / H.G2SI)
                    lsw, stw = H.s_status(gtw / r_["gb0"], r_["gb0"]); nfloor += int(stw == "floor")
                    qw, _, _, _ = mc_row(r_, dict(V=Vw, elo=0.10 * Vw, ehi=0.10 * Vw), 1000, rw)
                    if stw == "root" and np.isfinite(qw[0]): nroot_w += 1; inn += int(qw[0] <= math.log10(2.0) <= qw[4])
                rep[r_["label"]] = (inn, nroot_w, nfloor); P(f"  SELFTEST repeat (reported): {r_['label']}: the 95 % interval contains s = 2 in {inn} of {nroot_w} fabricated worlds with a root ({nfloor} of 100 worlds at the floor)")
            NUM["selftest_repeat"] = rep
    # ---------------------------------------------------------------- hand estimates
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE1-HE3 were scored at stage A) scored:")
        g = lambda lab: RES[f"PKS0529 [{lab}]"]
        sed = [g(f"SED; {x}") for x in ("none", "CO", "CI", "dust")]
        m567 = [ok for n_, ok, lb in CHK if n_.startswith(("M5", "M6", "M7"))]
        he = {"HE4": bool(all(r["status"] == "floor" for r in sed) and 0.12 <= g("SED; CO")["D_med"] <= 0.35),
              "HE5": bool(g("CIG; CO")["status"] == "floor" and 0.45 <= g("CIG; CO")["D_med"] <= 0.80 and g("CIG; CI")["status"] == "floor" and 0.12 <= g("CIG; CI")["D_med"] <= 0.35 and g("CIG; dust")["status"] == "floor" and 0.15 <= g("CIG; dust")["D_med"] <= 0.45),
              "HE6": bool(0.9 <= g("CIG; none")["D_med"] <= 1.4 and ((g("CIG; none")["status"] == "root" and g("CIG; none")["s"] >= 3) or g("CIG; none")["status"] == "ceiling")),
              "HE7": bool(all(abs(v) <= 0.04 for v in g("SED; CO")["kin_median_shift_dex"].values())),
              "HE8": bool(len(m567) == 3 and all(m567))}
        P(f"    HE4: SED rows' statuses {[r['status'] for r in sed]} (all floor needed); D_med [SED; CO] {g('SED; CO')['D_med']:.3f} (needs 0.12-0.35): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: [CIG; CO] {g('CIG; CO')['status']} D_med {g('CIG; CO')['D_med']:.3f} (0.45-0.80); [CIG; CI] {g('CIG; CI')['status']} {g('CIG; CI')['D_med']:.3f} (0.12-0.35); [CIG; dust] {g('CIG; dust')['status']} {g('CIG; dust')['D_med']:.3f} (0.15-0.45): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: [CIG; none] D_med {g('CIG; none')['D_med']:.3f} (0.9-1.4), status {g('CIG; none')['status']}, s* {g('CIG; none')['s']:.3g}: {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE7: the kinematic readings move the median g_obs by {g('SED; CO')['kin_median_shift_dex']} dex (needs |.| <= 0.04): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
        P(f"    HE8: M5, M6 and M7 {'hold' if he['HE8'] else 'do not all hold'}: {'hit' if he['HE8'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    pcols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling", "delta_floor", "delta_to_s1", "status", "stellar", "gas", "role", "R_kpc", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r_ in ROWS:
        R_ = RES[r_["label"]]; st = R_["status"]; q = R_["q"]
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(Z0, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]
        extra = [float(np.median(R_["y"])), R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D_med"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], R_["delta_floor"], R_["delta_to_s1"], st, R_["stellar"], R_["gas"], R_["role"], "/".join(f"{v:.3f}" for v in R_["R"])]
        q_ = ("ILL-CONDITIONED (y 5-120, near-Newtonian); " if R_["ill"] else "") + {"root": "has a root: an UPPER bound on s* (vacuous if far above 1)", "floor": "FLOOR: no root, median D <= 1 (the baryons exceed the dynamics at the median ring): robust against any higher baryon set",
                                                                                    "ceiling": f"CEILING: median D = {R_['D_med']:.2f} > 1 but s* > 1000: vacuous upper bound, NOT a floor"}[st] \
            + "; five correlated rings (width = half the beam); disc possibly out of equilibrium; stellar size and B/D unmeasured; gas tracers disagree x4; stellar branch " + R_["stellar"] + (" (RECOMMENDED CHART ROW by the frozen rule)" if R_["label"] == "PKS0529 [CIG; CO]" else "")
        sstar = R_["s"]
        lim = "baryons are a lower limit (no gas): s* is an upper bound" if R_["gas"] == "none" else f"class {GCLASS[R_['gas']]} {R_['gas']} gas with a standard conversion and a {R_['stellar']} stellar mass: not a measurement"
        rows.append(["CFG275", R_["label"], f"{GCLASS[R_['gas']]} ({R_['gas']} gas; {R_['stellar']} stars)", f"{Z0:.4f}", f"{Z0:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], lim, fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg275_points{SFX}.csv"), pcols, rows)
    P(f"\n  points written: cfg275_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg275{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg275{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
