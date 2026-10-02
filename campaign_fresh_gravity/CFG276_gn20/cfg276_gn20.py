#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG276 -- implied-a0 rows for GN20 (z = 4.055) from the JWST/NIRSpec DysmalPy circular velocity of Uebler+24 (arXiv:2403.03192) with independent baryons
(Tan+14 stars 1.1e11; Hodge+12 gas 1.3e11 or the Boogaard+25 resolved radiative-transfer gas 2.87e11): six rows = three baryon branches x R_e / 2 R_e, never pooled.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG276_gn20/FROZEN_CRITERIA.md (bc2ed906d).
  g_obs   R_e: v_circ(R_e)^2 / R_e with v_circ = 496 km/s (the model's circular velocity: the pressure term 3.36 sigma0^2 is in it once); 2 R_e: G M_dyn(<2 R_e) / (2 R_e)^2, log M_dyn = 11.68; 0.10 dex declared
  g_bar   stars: Sersic n = 0.42 disc (R_e 3.6 kpc, Hankel thin disc) + nuclear component (n = 4, R_e 0.8 kpc, 2.5e10); gas: exponential disc R_e = 4.0 kpc (Freeman)
  STAGE=A the baryon side (no g_obs-based quantity); STAGE=B the measurement (once, after stage A, the SELFTEST and this script are committed); STAGE=B SELFTEST=1; STAGE=B MUTATE=1 (g_obs x 4).
Run: STAGE=A python3 .../cfg276_gn20.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math, time, zlib, re
sys.dont_write_bytecode = True
import numpy as np
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: g_obs x 4 ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED g_obs on the law at s_true = 2 (+0.10 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
B_MC = 10000
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src")
UBP = os.path.join(EXT, "2403.03192", "GN20_accepted.tex")
BOP = os.path.join(EXT, "2510.17804", "boogaard-gn20-noema-hires.tex")

# ---------------------------------------------------------------- constants frozen in the criteria (section 1-3)
Z0 = 4.055
RE = 3.6                                                                    # kpc, Colina+23 via Uebler+24 (fixed in the model)
V_FID, V_INFL, V_ROT_FID = 496.0, 472.0, 469.0                              # v_circ(R_e) fiducial, inflow model; v_rot(R_e) fiducial
SIG0 = 89.0
V_150 = math.sqrt(551.0 ** 2 + 3.36 * SIG0 ** 2)                            # the i = 150 deg reading: v_rot(R_e) = 551 plus the 3.36 sigma0^2 relation
LMD2_FID, LMD2_INFL, MD2_150 = 11.68, 11.51, 7.0e11                         # M_dyn(<2R_e)
SIGG = 0.10                                                                 # declared dex on g_obs
SIGM, SIGGAS = 0.30, 0.213
M_STAR, M_BULGE = 1.1e11, 2.5e10
FB = M_BULGE / M_STAR
GASM = {"none": 0.0, "H12": 1.3e11, "RT": 2.87e11}
GAS_RE, GAS_RE_TED, GAS_RE_COMPACT = 4.0, 1.678 * 2.914, 2.5
ROWS = [dict(label=f"GN20 [{b}; {r}]", branch=b, rad=r, role="headline" if r == "Re" else "sensitivity") for r in ("Re", "2Re") for b in ("stars", "stars+H12", "stars+RT")]
for r_ in ROWS:
    r_["R"] = RE if r_["rad"] == "Re" else 2 * RE; r_["Mg"] = {"stars": 0.0, "stars+H12": GASM["H12"], "stars+RT": GASM["RT"]}[r_["branch"]]
LAB2I = {r["label"]: i for i, r in enumerate(ROWS)}

# ---------------------------------------------------------------- geometry (m s^-2 per Msun); the CFG275 functions with the exact Sersic b_n
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


def g_star_unit(R, kind="base"):
    """per Msun of TOTAL stellar mass: base = (1 - FB) in a Sersic n = 0.42 disc of R_e 3.6 (Hankel) + FB in a nuclear n = 4, R_e = 0.8 kpc component"""
    R = np.atleast_1d(np.asarray(R, float))
    if kind == "base": return (1 - FB) * hankel_g_unit(0.42, RE, R) + FB * gsph_sersic(1.0, 4.0, 0.8, R)
    if kind == "disc": return hankel_g_unit(0.42, RE, R)
    if kind == "exp4": return np.asarray(H.gdisc(1.0, 4.0, R), float)
    raise KeyError(kind)


def g_gas_unit(R, kind="base"):
    R = np.atleast_1d(np.asarray(R, float))
    if kind == "base": return np.asarray(H.gdisc(1.0, GAS_RE, R), float)
    if kind == "ted": return np.asarray(H.gdisc(1.0, GAS_RE_TED, R), float)
    if kind == "compact": return np.asarray(H.gdisc(1.0, GAS_RE_COMPACT, R), float)
    if kind == "pointmass": return np.asarray(H.gsph(1.0, GAS_RE, R), float)
    raise KeyError(kind)


for r_ in ROWS:
    r_["gs_u"] = float(g_star_unit(r_["R"])[0]); r_["gg_u"] = float(g_gas_unit(r_["R"])[0]) if r_["Mg"] > 0 else 0.0
    r_["gb0"] = M_STAR * r_["gs_u"] + r_["Mg"] * r_["gg_u"]; r_["y0"] = r_["gb0"] / A0C
GR = lambda V, R: V ** 2 / R * H.G2SI                                      # g_obs (m s^-2) from a velocity (km/s) at R (kpc)
GM = lambda lM, R: H.G_KPC * 10 ** lM / R ** 2 * H.G2SI                     # g_obs from an enclosed mass at R
GOBS_V = {("Re", "fid"): GR(V_FID, RE), ("Re", "inflow"): GR(V_INFL, RE), ("Re", "i150"): GR(V_150, RE), ("Re", "rot"): GR(V_ROT_FID, RE),
          ("2Re", "fid"): GM(LMD2_FID, 2 * RE), ("2Re", "inflow"): GM(LMD2_INFL, 2 * RE), ("2Re", "i150"): H.G_KPC * MD2_150 / (2 * RE) ** 2 * H.G2SI}
P(f"GN20: z {Z0}, R_e {RE} kpc (2 R_e {2 * RE}); stars {M_STAR:.2e} (nuclear fraction {FB:.3f}); gas H12 {GASM['H12']:.2e}, RT {GASM['RT']:.2e}; g_obs(R_e) fiducial {GOBS_V[('Re', 'fid')]:.3e}, (2 R_e) {GOBS_V[('2Re', 'fid')]:.3e} m/s^2; sigma_g {SIGG} dex, sigma_M* {SIGM}, sigma_gas {SIGGAS}")


def has(tex_compact, pat):
    return re.sub(r"\s+", "", pat) in tex_compact


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BARYON SIDE (g_obs of the rows is printed as A6; no D, delta or s* is formed)")
    ub = re.sub(r"\s+", "", open(UBP, encoding="utf-8", errors="ignore").read()); bo = re.sub(r"\s+", "", open(BOP, encoding="utf-8", errors="ignore").read())
    UB = ["11.42^{+0.05}_{-0.06}", "\\sigma_0$ [km/s] & $89\\pm10$", "v_{\\rm circ}(R_e)$ [km/s] & 496", "v_{\\rm rot}(R_e)$ [km/s] & 469", "v_{\\rm rot,max}$ [km/s] & 531", "(<2R_e)/M_\\odot)$ & 11.68", "v_{\\rm circ}(R_e)$ [km/s] & 472", "v_{\\rm rot}(R_e)$ [km/s] & 443", "(<2R_e)/M_\\odot)$ & 11.51",
          "R_{e,\\rm disc}=3.6", "n_{\\rm S,disc}=0.42", "2.5\\times10^{10}", "=11.4$, with a standard deviation of 0.3", "M_\\star=1.1\\times10^{11}", "M_{\\rm H2}=1.3\\times10^{11}", "v_{\\rm rot}(R_e=3.6{\\rm kpc})=551", "M_{\\rm dyn}(r<R_e)=2.6\\times10^{11}", "M_{\\rm dyn}(r<2R_e)=7.0\\times10^{11}", "f_{\\rm DM}(<R_e)$ & $0.30\\pm0.07$"]
    BO = ["$2.87^{+0.39}_{-0.30}$", "$2914^{+1245}_{-965}$", "$0.98^{+0.18}_{-0.30}$", "$2.76^{+0.52}_{-0.34}$", "$3.46^{+5.91}_{-1.81}$", "r_{\\rm eff, mol} \\approx 4", "\\Mmol = 2.9_{-0.3}^{+0.4} \\times 10^{11}"]
    fu = [has(ub, p) for p in UB]; fb = [has(bo, p) for p in BO]
    check("C1 CONTROL (loader): every frozen number is found in the two TeX files (Uebler+24: the fiducial and inflow model tables, R_e 3.6, n 0.42, the 2.5e10 nuclear mass, the 11.4 +- 0.3 prior, Tan+14 1.1e11, Hodge+12 1.3e11, the i = 150 deg numbers; Boogaard+25: the TED and TUNER gas masses, r_exp, n, alpha_CO, r_eff 4 kpc)",
          f"Uebler {sum(fu)} of {len(UB)} {fu}; Boogaard {sum(fb)} of {len(BO)} {fb}", all(fu) and all(fb))
    d_f = abs(math.hypot(V_ROT_FID, math.sqrt(3.36) * SIG0) / V_FID - 1); d_i = abs(math.hypot(443.0, math.sqrt(3.36) * SIG0) / V_INFL - 1)
    check("C1b CONTROL: v_circ^2 = v_rot^2 + 3.36 sigma_0^2 at R_e to 0.5 % for the fiducial and the inflow model (the pressure term is in the published v_circ once)", f"fiducial: sqrt(469^2 + 3.36 x 89^2) = {math.hypot(V_ROT_FID, math.sqrt(3.36) * SIG0):.2f} against 496 (diff {d_f:.4f}); inflow: {math.hypot(443.0, math.sqrt(3.36) * SIG0):.2f} against 472 (diff {d_i:.4f}); i = 150 deg v_circ = {V_150:.1f}", d_f < 5e-3 and d_i < 5e-3)
    g_h1 = hankel_g_unit(1.0, 2.57, np.array([1.0, 3.6, 7.2])); g_f = np.array([float(H.gdisc(1.0, 2.57, r)) for r in (1.0, 3.6, 7.2)]); d1 = float(np.max(np.abs(g_h1 / g_f - 1)))
    s_g = 2.57 / math.sqrt(2 * b_proj(0.5)); g_h5 = hankel_g_unit(0.5, 2.57, np.array([1.0, 3.6, 7.2])); g_c = np.array([gauss_closed(s_g, r) for r in (1.0, 3.6, 7.2)]); d5 = float(np.max(np.abs(g_h5 / g_c - 1)))
    d_half = {}
    for n_ in (4.0,):
        p_, b_ = p_dep(n_), b_dep(n_); a_ = n_ * (3 - p_)
        rho = lambda r: (r) ** (-p_) * np.exp(-b_ * r ** (1.0 / n_))
        Sg = lambda Rp: 2.0 * quad(lambda t: rho(math.sqrt(Rp ** 2 + t ** 2)), 0, np.inf, limit=200)[0]
        norm = math.exp(gammaln(a_)) * n_ * b_ ** (-a_) * 4 * math.pi
        d_half[n_] = quad(lambda Rp: 2 * math.pi * Rp * Sg(Rp), 0, 1.0, limit=200)[0] / norm
    from scipy.special import gammainc as gi
    bn_chk = max(abs(gi(2 * n_, b_proj(n_)) - 0.5) for n_ in (0.42, 0.5, 1.0))
    check("C2 CONTROL (geometry): the Hankel thin disc equals Freeman's exact exponential disc (n = 1) and the exact Gaussian-disc closed form (n = 0.5) to 2e-3 at 1, 3.6 and 7.2 kpc; the exact Sersic b_n puts half the mass inside R_e (1e-12) for n = 0.42, 0.5, 1; the deprojected n = 4 profile's projected half-mass radius equals R_e to 1 %",
          f"Hankel vs Freeman {d1:.1e}; vs Gaussian {d5:.1e}; |P(2n, b_n) - 1/2| {bn_chk:.1e}; n=4 projected fraction within R_e {d_half[4.0]:.4f}", d1 < 2e-3 and d5 < 2e-3 and bn_chk < 1e-12 and abs(d_half[4.0] - 0.5) < 0.005)
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
            ls, unb = H.s_star(NU(np.array([r_["gb0"]]) / (A0C * st)), np.array([r_["gb0"]])); dn = max(dn, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C4 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every row's baryon side", f"max |d log10 s| {dn:.1e}", dn < 1e-6)

    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    for r_ in ROWS:
        lv, fl = H.lever1(NU(np.array([r_["y0"]])), np.array([r_["gb0"]])); r_["lever"], r_["ill"] = lv, bool(fl or abs(lv) >= 10)
        P(f"    {r_['label']:24s} R {r_['R']:.1f} kpc: g_bar {r_['gb0']:.3e} m/s^2, y {r_['y0']:.2f}, lever {lv:+.2f}{' (not computable)' if fl else ''}  {'ILL-CONDITIONED' if r_['ill'] else 'conditioned'}")
    P(f"    CFG240: T4 floor 3 sigma / sqrt(N) at sigma = 0.2 dex is {3 * 0.2:.2f} dex for N = 1 (calibration free); y(B) spans {min(r_['y0'] for r_ in ROWS):.1f} to {max(r_['y0'] for r_ in ROWS):.1f}; the break-even design needs y >~ 8 with deep points (y < 0.3): none here")
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to the baseline; stars at unit mass, gas at unit mass) at R_e and 2 R_e")
    for nm, f_ in (("stars: all in the disc", lambda R: g_star_unit(R, "disc") / g_star_unit(R)), ("stars: exp disc R_e=4.0", lambda R: g_star_unit(R, "exp4") / g_star_unit(R)), ("gas: TED input scale R_e=4.89", lambda R: g_gas_unit(R, "ted") / g_gas_unit(R)),
                   ("gas: compact R_e=2.5", lambda R: g_gas_unit(R, "compact") / g_gas_unit(R)), ("gas: point mass", lambda R: g_gas_unit(R, "pointmass") / g_gas_unit(R))):
        P(f"    {nm}: R_e {float(np.log10(f_(RE))[0]):+.3f}, 2 R_e {float(np.log10(f_(2 * RE))[0]):+.3f} dex")
    P("A5  ENCLOSED FRACTIONS at R_e and 2 R_e: gas (exponential R_e 4.0, projected) " + ", ".join(f"{1 - (1 + R / (GAS_RE / H.XN)) * math.exp(-R / (GAS_RE / H.XN)):.3f}" for R in (RE, 2 * RE)) + "; nuclear n=4 R_e 0.8 " + ", ".join(f"{float(fenc_sph(R, 4.0, 0.8)):.3f}" for R in (RE, 2 * RE))
      + "; Sersic n=0.42 disc projected " + ", ".join(f"{float(gammainc(0.84, b_proj(0.42) * (R / RE) ** (1 / 0.42))):.3f}" for R in (RE, 2 * RE)))
    P("\nA6  g_obs OF THE ROWS AND VARIANTS (numbers from the papers' tables; m s^-2): " + "; ".join(f"{k[0]} {k[1]}: {v:.3e} ({v / A0C:.1f} a0)" for k, v in GOBS_V.items()))
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C4)")
    P("  PF-D2 ILL-CONDITIONED rows: " + (", ".join(r_["label"] for r_ in ROWS if r_["ill"]) or "none"))
    P("\nM5 (a control that needs only the baryon side) -- Uebler's baryonic circular velocity at R_e against my geometry")
    Mb = 10 ** 11.42; gb_mine = Mb * 0.1 * float(gsph_sersic(1.0, 4.0, 0.8, RE)) + Mb * 0.9 * float(hankel_g_unit(0.42, RE, np.array([RE]))[0]); v_mine = math.sqrt(gb_mine * RE / H.G2SI); v_mod = V_FID * math.sqrt(1 - 0.30)
    check("M5 (validates my geometry against Uebler's own model): the baryonic circular velocity at R_e of the total baryons log M_bar = 11.42 split as in Uebler's model (B/T = 0.1 nuclear n = 4 R_e 0.8; 0.9 in the n = 0.42 R_e = 3.6 disc, thin) is within 25 % of the model's v_bar = v_circ sqrt(1 - f_DM) with f_DM(<R_e) = 0.30",
          f"v_bar (mine, thin disc) {v_mine:.1f} km/s; model {v_mod:.1f} km/s (496 x sqrt(0.70)); ratio {v_mod / v_mine:.3f}", abs(v_mod / v_mine - 1) <= 0.25)
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 7) scored (HE4-HE7 are scored at stage B; HE7 = M5 is scored here):")
    y_ = {r_["label"]: r_["y0"] for r_ in ROWS}
    he = {"HE1": bool(5 <= y_["GN20 [stars; Re]"] <= 12 and 10 <= y_["GN20 [stars+H12; Re]"] <= 20 and 15 <= y_["GN20 [stars+RT; Re]"] <= 35), "HE2": bool(all(r_["ill"] for r_ in ROWS)),
          "HE3": bool(2.1e-9 <= GOBS_V[("Re", "fid")] <= 2.3e-9 and 1.2e-9 <= GOBS_V[("2Re", "fid")] <= 1.4e-9), "HE7": bool(abs(v_mod / v_mine - 1) <= 0.25)}
    P(f"    HE1: y at R_e: stars {y_['GN20 [stars; Re]']:.1f} (5-12), +H12 {y_['GN20 [stars+H12; Re]']:.1f} (10-20), +RT {y_['GN20 [stars+RT; Re]']:.1f} (15-35): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}")
    P(f"    HE2: all six rows ILL-CONDITIONED ({sum(r_['ill'] for r_ in ROWS)} of 6): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}")
    P(f"    HE3: g_obs(R_e) {GOBS_V[('Re', 'fid')]:.3e} (2.1-2.3e-9), g_obs(2R_e) {GOBS_V[('2Re', 'fid')]:.3e} (1.2-1.4e-9): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}")
    P(f"    HE7: M5 {'holds' if he['HE7'] else 'does not hold'} (ratio {v_mod / v_mine:.3f}): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(z=Z0, R_e=RE, M_star=M_STAR, nuclear_frac=FB, gas=GASM, sig=[SIGG, SIGM, SIGGAS], gobs=[[k[0], k[1], v] for k, v in GOBS_V.items()]), rows={r_["label"]: dict(R=r_["R"], gb0=r_["gb0"], y0=r_["y0"], lever=r_["lever"], ill=r_["ill"]) for r_ in ROWS}, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)),
               controls_numbers=dict(hankel_vs_freeman=d1, hankel_vs_gaussian=d5, half_mass_n4=d_half[4.0], v_bar_mine=v_mine, v_bar_model=v_mod))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: g_obs x 4)" if MUTATE else ""))
    rngS = np.random.default_rng(2760)
    FAC = 4.0 if MUTATE else 1.0
    if SELFTEST:
        gt = {r_["label"]: r_["gb0"] * float(NU(np.array([r_["gb0"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, SIGG) for r_ in ROWS}
        GO0 = {r_["label"]: gt[r_["label"]] for r_ in ROWS}
        P("SELFTEST: g_obs fabricated from the law at s_true = 2 on each row's own baryons (+0.10 dex scatter); the tabulated velocities are not used")
    else:
        GO0 = {r_["label"]: FAC * GOBS_V[(r_["rad"], "fid")] for r_ in ROWS}
    KN_LIST = ["g_obs: inflow model", "g_obs: i=150 deg", "g_obs: rotation only", "stars: all in the disc", "stars: exp disc R_e=4.0", "gas: TED input scale R_e=4.89", "gas: compact R_e=2.5", "gas: point mass", "kernel P2"]
    KGR = {"g_obs: inflow model": "kinematics", "g_obs: i=150 deg": "kinematics", "g_obs: rotation only": "kinematics", "stars: all in the disc": "stellar geometry", "stars: exp disc R_e=4.0": "stellar geometry", "gas: TED input scale R_e=4.89": "gas geometry", "gas: compact R_e=2.5": "gas geometry", "gas: point mass": "gas geometry", "kernel P2": "kernel"}

    def mc_row(r_, go0, B, rng):
        god = (go0 * 10 ** rng.normal(0, SIGG, B))[:, None]
        Ms_d = (M_STAR * 10 ** rng.normal(0, SIGM, B))[:, None]; gbd = Ms_d * r_["gs_u"]
        if r_["Mg"] > 0: gbd = gbd + (r_["Mg"] * 10 ** rng.normal(0, SIGGAS, B))[:, None] * r_["gg_u"]
        Dd = god / gbd; lsd, ud = H.AI.implied(Dd, gbd, NU, A0C); q, frn = H.rooted_pct(lsd, ud); frc = float(np.mean(ud & (np.median(Dd, axis=1) > 1.0)))
        dFd = np.median(np.log10(god / (gbd * NU(gbd / A0C))), axis=1); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        return q, frn, frc, dq

    RES = {}
    for r_ in ROWS:
        lab = r_["label"]; go0 = GO0[lab]; gb0 = np.array([r_["gb0"]]); GO = np.array([go0]); D0 = GO / gb0; ls0, st0 = H.s_status(D0, gb0)
        rng = np.random.default_rng(zlib.crc32(("276|" + lab).encode()) % 100000)
        q, frn, frc, dq = mc_row(r_, go0, B_MC, rng)
        dF0 = float(np.median(np.log10(GO / (gb0 * NU(gb0 / A0C))))); bands = H.band_solutions(D0, gb0)

        def variant(nm):
            go, gb, nu = go0, r_["gb0"], NU
            if nm == "g_obs: inflow model": go = None if SELFTEST else FAC * GOBS_V[(r_["rad"], "inflow")]
            elif nm == "g_obs: i=150 deg": go = None if SELFTEST else FAC * GOBS_V[(r_["rad"], "i150")]
            elif nm == "g_obs: rotation only":
                if SELFTEST or r_["rad"] != "Re": return None
                go = FAC * GOBS_V[("Re", "rot")]
            elif nm == "stars: all in the disc": gb = M_STAR * float(g_star_unit(r_["R"], "disc")[0]) + r_["Mg"] * r_["gg_u"]
            elif nm == "stars: exp disc R_e=4.0": gb = M_STAR * float(g_star_unit(r_["R"], "exp4")[0]) + r_["Mg"] * r_["gg_u"]
            elif nm.startswith("gas:"):
                if r_["Mg"] <= 0: return None
                kind = {"gas: TED input scale R_e=4.89": "ted", "gas: compact R_e=2.5": "compact", "gas: point mass": "pointmass"}[nm]; gb = M_STAR * r_["gs_u"] + r_["Mg"] * float(g_gas_unit(r_["R"], kind)[0])
            elif nm == "kernel P2": nu = NUP2
            if go is None: return None
            return np.array([go]), np.array([gb]), nu

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
        kin_shift = {} if SELFTEST else {nm: float(np.log10(v / go0)) for nm, v in (("inflow", FAC * GOBS_V[(r_["rad"], "inflow")]), ("i150", FAC * GOBS_V[(r_["rad"], "i150")]))}
        RES[lab] = dict(label=lab, branch=r_["branch"], rad=r_["rad"], role=r_["role"], z=Z0, R=[r_["R"]], GO=GO.tolist(), GB=gb0.tolist(), D=D0.tolist(), D_med=float(np.median(D0)), y=[r_["y0"]], ls=ls0, status=st0, s=H.s_val_status(ls0, st0), q=q, frac_mc_noroot=frn, frac_mc_ceiling=frc,
                        delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1], bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, n_knobs=n_k, lever=lv_nl,
                        ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=H.delta_floor(D0), delta_to_s1=d1, kin_shift_dex=kin_shift)
        R_ = RES[lab]
        b0 = (f"s* <= {10 ** ls0:.3g}" if st0 == "root" else ("FLOOR (D <= 1)" if st0 == "floor" else "CEILING (s* > 1000)"))
        qs = f"68 % [{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] 95 % [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "no draw interval (< 20 rooted draws)"
        P(f"  {lab:24s} g_obs {go0:.3e} D {D0[0]:.3f} dF {dF0:+.3f} y {r_['y0']:.2f}  {b0}; MC {qs} (no root {frn:.2f}, ceiling {frc:.2f}); to s*=1 {d1:+.2f} dex; recipe half-width {half:.3f} ({n_root}/{n_k} knobs rooted){' ILL' if R_['ill'] else ''}")
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg276_stageB_results.json")))["numbers"]["rows"]
        bad = 0.0; nroot = 0; n_gt1_m = 0; n_gt1_0 = 0
        for r_ in ROWS:
            R_ = RES[r_["label"]]; D0 = np.array(R_["D"]); gb = np.array(R_["GB"]); n_gt1_m += int(np.median(D0) > 1); n_gt1_0 += int(np.median(main[r_["label"]]["D"]) > 1)
            if R_["status"] == "root": nroot += 1; bad = max(bad, abs(float(np.median(np.log10(D0 / NU(gb / (A0C * 10 ** R_["ls"])))))))
        check("M2 MUTATE=1 (reactivity; the count is of rows with median D > 1, not of roots): g_obs x 4; rows with status ROOT satisfy the median-residual equation at their own s* to 1e-6 and the number of rows with median D > 1 is at least the main run's",
              f"rows with median D > 1: mutated {n_gt1_m}, main {n_gt1_0}; rows with a root {nroot}; max |median residual| {bad:.1e}", bad < 1e-6 and n_gt1_m >= n_gt1_0)
    else:
        d1m = 0.0
        for r_ in ROWS:
            R_ = RES[r_["label"]]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array(R_["D"])[None, :], np.array(R_["GB"])[None, :], NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r_ in ROWS if RES[r_['label']]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        check("M3 the six rows are present with their roles (three headline at R_e, three sensitivity at 2 R_e)", f"{[(RES[r_['label']]['role'], RES[r_['label']]['R']) for r_ in ROWS]}", [RES[r_["label"]]["role"] for r_ in ROWS] == ["headline"] * 3 + ["sensitivity"] * 3)
        if SELFTEST:
            tested = [r_["label"] for r_ in ROWS if RES[r_["label"]]["status"] == "root" and not RES[r_["label"]]["ill"]]
            inside = [t for t in tested if np.isfinite(RES[t]["q"][0]) and RES[t]["q"][0] <= math.log10(2.0) <= RES[t]["q"][4]]
            if tested: check("SELFTEST: the conditioned rooted rows return the fabricated truth (s = 2) inside their 95 % interval", f"{len(inside)} of {len(tested)} inside", len(inside) == len(tested))
            else: check("SELFTEST: no row is both rooted and conditioned in the fabricated world (every row is ILL-CONDITIONED or has no root): the coverage statement is not evaluated; the 100-world repeat below is the reported evidence", f"rooted rows {[r_['label'] for r_ in ROWS if RES[r_['label']]['status'] == 'root']}; ill rows {sum(RES[r_['label']]['ill'] for r_ in ROWS)} of 6", True, load_bearing=False)
            rep = {}
            for r_ in ROWS:
                inn = 0; nroot_w = 0; nfloor = 0
                for w in range(100):
                    rw = np.random.default_rng(100000 + 1000 * LAB2I[r_["label"]] + w); gtw = r_["gb0"] * float(NU(np.array([r_["gb0"] / (2.0 * A0C)]))[0]) * 10 ** rw.normal(0, SIGG)
                    lsw, stw = H.s_status(np.array([gtw / r_["gb0"]]), np.array([r_["gb0"]])); nfloor += int(stw == "floor")
                    qw, _, _, _ = mc_row(r_, gtw, 1000, rw)
                    if stw == "root" and np.isfinite(qw[0]): nroot_w += 1; inn += int(qw[0] <= math.log10(2.0) <= qw[4])
                rep[r_["label"]] = (inn, nroot_w, nfloor); P(f"  SELFTEST repeat (reported): {r_['label']}: the 95 % interval contains s = 2 in {inn} of {nroot_w} fabricated worlds with a root ({nfloor} of 100 worlds at the floor)")
            NUM["selftest_repeat"] = rep
    if not (MUTATE or SELFTEST):
        P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 7; HE1-HE3 and HE7 were scored at stage A) scored:")
        g = lambda lab: RES[f"GN20 [{lab}; Re]"]
        he = {"HE4": bool(2.0 <= g("stars")["D_med"] <= 3.5 and 1.1 <= g("stars+H12")["D_med"] <= 1.7 and 0.7 <= g("stars+RT")["D_med"] <= 1.0 and g("stars")["status"] == "root" and g("stars+H12")["status"] == "root" and g("stars+RT")["status"] == "floor"),
              "HE5": bool(g("stars")["status"] == "root" and 15 <= g("stars")["s"] <= 120 and g("stars+H12")["status"] == "root" and 4 <= g("stars+H12")["s"] <= 40),
              "HE6": bool(abs(g("stars")["kin_shift_dex"]["inflow"] - (-0.043)) <= 0.01 and abs(g("stars")["kin_shift_dex"]["i150"] - 0.127) <= 0.01)}
        P(f"    HE4: D(R_e) stars {g('stars')['D_med']:.3f} (2.0-3.5), +H12 {g('stars+H12')['D_med']:.3f} (1.1-1.7), +RT {g('stars+RT')['D_med']:.3f} (0.7-1.0); statuses {g('stars')['status']} / {g('stars+H12')['status']} / {g('stars+RT')['status']}: {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5: s* (R_e) stars {g('stars')['s']:.3g} (15-120), +H12 {g('stars+H12')['s']:.3g} (4-40): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6: kinematic knobs move g_obs(R_e) by {g('stars')['kin_shift_dex']} dex (needs -0.043 and +0.127 within 0.01): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        NUM["hand_estimates_B"] = he
    pcols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling", "delta_floor", "delta_to_s1", "status", "branch", "radius", "role", "R_kpc", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    GCL = {"stars": "D (no gas; stars-only lower limit)", "stars+H12": "S (CO gas, alpha_CO 0.8 (Hodge+12); Tan+14 stars)", "stars+RT": "S/L (resolved radiative-transfer gas, Boogaard+25; Tan+14 stars)"}
    for r_ in ROWS:
        R_ = RES[r_["label"]]; st = R_["status"]; q = R_["q"]
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(Z0, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]
        extra = [R_["y"][0], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D_med"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], R_["delta_floor"], R_["delta_to_s1"], st, R_["branch"], R_["rad"], R_["role"], f"{R_['R'][0]:.2f}"]
        q_ = ("ILL-CONDITIONED (near-Newtonian); " if R_["ill"] else "") + {"root": "has a root: an UPPER bound on s* (vacuous if far above 1)", "floor": "FLOOR: no root, D <= 1 (the baryons exceed the dynamics): robust against any higher baryon set",
                                                                           "ceiling": f"CEILING: D = {R_['D_med']:.2f} > 1 but s* > 1000: vacuous upper bound, NOT a floor"}[st] \
            + "; g_obs is a DysmalPy model output (halo + baryon prior; inclination fixed at 142 deg, the 30 deg reading raises it by 0.13 dex); " + ("R = 2 R_e is a model extrapolation (sensitivity row)" if R_["rad"] == "2Re" else "R = R_e") + ("; RECOMMENDED CHART ROW by the frozen rule" if R_["label"] == "GN20 [stars+RT; Re]" else "")
        sstar = R_["s"]
        lim = "baryons are a lower limit (no gas): s* is an upper bound" if R_["branch"] == "stars" else "class S/L gas with a standard conversion: not a measurement"
        rows.append(["CFG276", R_["label"], GCL[R_["branch"]], f"{Z0:.4f}", f"{Z0:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], lim, fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg276_points{SFX}.csv"), pcols, rows)
    P(f"\n  points written: cfg276_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - TSTART:.0f} s)")
open(os.path.join(HERE, f"cfg276{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg276{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
