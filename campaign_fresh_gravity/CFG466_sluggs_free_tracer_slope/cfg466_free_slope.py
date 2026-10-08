#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG466 -- the four SLUGGS group/cluster centrals (M87 = NGC 4486, NGC 4365, NGC 4374, NGC 5846) with the GC tracer density slope FREE.
Frozen criteria: FROZEN_CRITERIA.md (commit 03b9e83e1), written and committed before any CFG466 number.

Law and baryons are EXACTLY CFG330 K0 / CFG331: CFG331's source is exec'd read-only up to its "run" block (raw Forbes+17 GC velocities,
global 3-sigma clip, equal-number bins, ML sigma, outer bins R > max(R_e, 2 kpc), ATLAS3D JAM calibration, Hernquist a = R_e/1.8153,
nu_mono, kappa = 1/2 FITTED, footings 9.36e-11 | 1.13e-10, CFG331 host gas / members / g_e).  Changed: only the tracer density and the error model.
  M87: measured Agnello+14 three-population Sersic sum (CFG323's script-parsed values), Abel-deprojected; MC over the published errors.
  NGC 4365 / 4374 / 5846: no GC density profile on disk -> declared prior gamma ~ U[2, 4] (single power law), marginalised.
  Anisotropy as in the record: isotropic primary; beta = +-0.5 reported.
  Per-galaxy error: bootstrap over the GCs through the full CFG331 binning pipeline.
CFG466_MUTATE=1: M1 gamma = 3 forced (reproduces CFG330 K0 / CFG331), M2 gamma = 1.5 forced (must move the headline class). Separate outputs.
Run: python3 campaign_fresh_gravity/CFG466_sluggs_free_tracer_slope/cfg466_free_slope.py   (main first; then CFG466_MUTATE=1)
"""
import os, sys, math, json, io, contextlib, time
import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG466_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
FROZEN = "03b9e83e1"
NB, NMC, SEED = 4000, 300, 466
P2 = 0.02275                                                    # one-sided 2 sigma
NB_C5, NREAL_C5 = 1000, 300
OUT = []
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


# ------------------------------------------------------------------ 0. CFG331's machinery, read-only (law + baryons unchanged)
os.environ.pop("CFG331_MUTATE", None)
C331 = os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment.py")
_src = open(C331).read()
_cut = _src.index("\n# ------------------------------------------------------------------ run")
NS = {"__file__": C331, "__name__": "cfg331_ns"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg331_environment", "exec"), NS)
B, GAL, GCS, A0, RG, LR = NS["B"], NS["GAL"], NS["GCS"], NS["A0"], NS["RG"], NS["LR"]
G, KPC, MSUN, ARCSEC = NS["G"], NS["KPC"], NS["MSUN"], NS["ARCSEC"]
sig_los, jam_mass, calib, gN_of, nu, g_efe = NS["sig_los"], NS["jam_mass"], NS["calib"], NS["gN_of"], NS["nu"], NS["g_efe"]
ml_sigma, clipped = NS["ml_sigma"], NS["clipped"]
GAS, MEM, GE = NS["GAS"], NS["MEM"], NS["GE"]
CENTRALS = (4486, 4365, 4374, 5846)
PRIOR3 = (4365, 4374, 5846)
READ = ("K0", "own", "bar", "barN", "efe")
DECIDE = ("K0", "own")
FEET = ("canonical", "alt")

K0J = json.load(open(os.path.join(LANES, "CFG330_sluggs_icgc_clip", "cfg330_summary_K0.json")))["CFG330"]
C331J = json.load(open(os.path.join(LANES, "CFG331_sluggs_centrals_environment", "cfg331_environment_results.json")))["summary"]
C323J = json.load(open(os.path.join(LANES, "CFG323_sluggs_measured_tracers", "cfg323_measured_tracers_results.json")))


def committed(n, rd, ft):
    if rd == "K0":
        return K0J[ft]["per_galaxy"][f"NGC{n}"]
    return C331J[f"{ft}|{rd}"]["per"][f"NGC{n}"]


# ------------------------------------------------------------------ 1. fields: CFG331's run() up to off_g, returning g(r)
def field(n, a0, reading, x=1.0):
    b = B[n]
    if reading == "K0":                                          # = CFG331 run(n, a0, 0.0, "bar") = CFG330 K0
        M = jam_mass(b["Mjam"], b["r12"], a0, "nu_mono"); gN = gN_of(n, M, np.zeros_like(RG))
        return nu(gN / a0) * gN
    Mg = GAS[n][0]
    Mg = None if (Mg is None or x == 0) else Mg * x
    if reading == "efe":
        M = jam_mass(b["Mjam"], b["r12"], a0, "nu_mono"); gN = gN_of(n, M, 0.0)
        return g_efe(gN, GE[(n, a0)] * (x > 0), a0)
    M = calib(n, a0, Mg) if Mg is not None else jam_mass(b["Mjam"], b["r12"], a0, "nu_mono")
    Mx = np.zeros_like(RG) if Mg is None else Mg.copy()
    if reading == "own" and n in (4486, 5846) and x > 0:
        mb = MEM[n]
        for rp, dk in zip(mb["Rp"], mb["dK"]):
            Mx = Mx + x * M * 10 ** (-0.4 * dk) * (RG >= rp)
    if reading == "barN":
        gN0 = gN_of(n, M, 0.0)
        return nu(gN0 / a0) * gN0 + G * Mx * MSUN / (RG * KPC) ** 2
    gN = gN_of(n, M, Mx)
    return nu(gN / a0) * gN


FIELD = {(n, rd, ft): field(n, A0[ft], rd) for n in CENTRALS for rd in READ for ft in FEET}

# ------------------------------------------------------------------ 2. general-profile Jeans, Abel deprojection, Sersic
UP = np.linspace(0, 14, 4000); CHP = np.cosh(UP)


def sig_los_rho(Rb, g, rho, beta=0.0):
    """isotropic/constant-beta Jeans for a tabulated rho(r) on RG; same projection as CFG331's sig_los"""
    lnf = 2 * beta * LR
    w = rho * np.exp(lnf) * g * RG * KPC
    cum = np.concatenate([np.cumsum((0.5 * (w[1:] + w[:-1]) * np.diff(LR))[::-1])[::-1], [0.0]])
    lP = np.log(np.maximum(cum / np.exp(lnf), 1e-300)); lrho = np.log(np.maximum(rho, 1e-300))
    out = []
    for R in Rb:
        r = R * CHP; lr_ = np.log(r)
        num = np.trapz((1 - beta / CHP ** 2) * np.exp(np.interp(lr_, LR, lP)) * r, UP)
        den = np.trapz(np.exp(np.interp(lr_, LR, lrho)) * r, UP)
        out.append(math.sqrt(num / den) / 1e3)
    return np.array(out)


def sig_pred(Rb, g, spec, beta=0.0):
    kind, val = spec
    return sig_los(Rb, g, val, beta) if kind == "pl" else sig_los_rho(Rb, g, val, beta)


def delta(n, g, spec, beta=0.0):
    b = B[n]; s = sig_pred(b["Rb"], g, spec, beta); o = b["outer"]
    return float(np.mean(np.log10(b["Sb"][o] / s[o])))


UU = np.linspace(0.0, 12.0, 6001); CHU = np.cosh(UU)
RLO, RHI = 0.3, 1.0e6                                            # every GC bin lies inside; the Sersic tail beyond RHI is < 1e-12 of the bins'
MRANGE = (RG >= RLO) & (RG <= RHI)


def abel_rho(dSigma, r):
    """rho(r) = -(1/pi) int_0^inf Sigma'(r cosh u) du"""
    out = np.empty_like(r)
    for i0 in range(0, len(r), 500):
        rr = r[i0:i0 + 500, None] * CHU[None, :]
        out[i0:i0 + 500] = -np.trapz(dSigma(rr), UU, axis=1) / math.pi
    return out


def bn_cb(n):                                                    # Ciotti & Bertin 1999 (Agnello+14's kappa_n; as CFG323)
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n ** 2)


def sersic_rho(Re, n, b, S0=1.0):
    def dS(R):
        x = np.maximum(R / Re, 1e-300); e = np.exp(-b * x ** (1.0 / n))
        return -S0 * e * b / (n * Re) * x ** (1.0 / n - 1.0)
    rho = np.zeros_like(RG)
    rho[MRANGE] = np.maximum(abel_rho(dS, RG[MRANGE]), 0.0)
    rho[RG < RLO] = rho[MRANGE][0]                               # below every GC bin: unused
    return rho


def am2kpc(a, D):
    return a * math.pi / 180 / 60 * D * 1e3


TR = {}
for l in open(os.path.join(LANES, "CFG323_sluggs_measured_tracers", "cfg323_transcribed_values.tsv")):
    p = l.rstrip("\n").split("\t")
    if len(p) == 3 and not l.startswith("#"):
        try:
            TR[p[0]] = json.loads(p[2])
        except Exception:
            pass
D87 = GAL[4486]["D"]


def a14_rho(nv, rev, sib, srb):
    S0 = [1.0, sib, srb]; rho = np.zeros_like(RG)
    for j in range(3):
        rho = rho + sersic_rho(am2kpc(rev[j] / 60.0, D87), nv[j], bn_cb(nv[j]), S0[j])
    return rho


A14C = dict(n=[TR["A14_n"][j][0] for j in range(3)], Re=[TR["A14_Re_as"][j][0] for j in range(3)], sib=TR["A14_Sib"][0], srb=TR["A14_Srb"][0])
RHO_C = a14_rho(A14C["n"], A14C["Re"], A14C["sib"], A14C["srb"])
RHO_Z = sersic_rho(am2kpc(TR["Z14"]["R0_as"][0] / 60, D87), TR["Z14"]["n"][0], TR["Z14"]["bn_log10"] * math.log(10))
lslope_c = -np.gradient(np.log(np.maximum(RHO_C, 1e-300)), LR)
G_LOC87 = np.interp(np.log(B[4486]["Rb"][B[4486]["outer"]]), LR, lslope_c)
GMIN87 = float(G_LOC87.min())
P(f"[{time.time() - T0:.0f}s] fields + M87 central profile ready; M87 local slope at the outer bins {np.round(G_LOC87, 3).tolist()} -> gamma_min {GMIN87:.3f}")

GAM = np.round(np.linspace(1.0, 4.0, 151), 10)                  # step 0.02; the prior grid is the 101 points in [2, 4]
IPRI = np.where((GAM >= 2.0 - 1e-9) & (GAM <= 4.0 + 1e-9))[0]
assert len(IPRI) == 101


def trap_w(x):
    w = np.zeros_like(x)
    if len(x) > 1:
        d = np.diff(x); w[:-1] += d / 2; w[1:] += d / 2
    else:
        w[:] = 1.0
    return w / w.sum()


W_PRI = np.zeros(len(GAM)); W_PRI[IPRI] = trap_w(GAM[IPRI])
_iw = np.where(GAM >= GMIN87 - 1e-12)[0]
W_WIDE = np.zeros(len(GAM)); W_WIDE[_iw] = trap_w(GAM[_iw])
A16 = {}
for l in open(os.path.join(LANES, "CFG326_sluggs_alabi16", "cfg326_alabi16_transcribed.tsv")):
    p = l.rstrip("\n").split("\t")
    if len(p) == 3 and p[0].isdigit():
        A16[int(p[0])] = float(p[2])
GREL = {n: A16[n] for n in CENTRALS}


def w_rel(n):
    w = np.zeros(len(GAM)); w[IPRI] = trap_w(GAM[IPRI]) * np.exp(-0.5 * ((GAM[IPRI] - GREL[n]) / 0.29) ** 2)
    return w / w.sum()


# ------------------------------------------------------------------ 3. exact Delta_obs(gamma) at the observed bins
DOBS = {}                                                         # (n, rd, ft) -> array over GAM (power law, beta 0)
DOBS_B = {}                                                       # (n, rd, ft, beta) -> array over GAM (power law)
DC, DZ, DC_B = {}, {}, {}                                         # M87 central Agnello / Zhu / central with beta
for n in CENTRALS:
    for rd in READ:
        for ft in FEET:
            g = FIELD[(n, rd, ft)]
            DOBS[(n, rd, ft)] = np.array([delta(n, g, ("pl", gm)) for gm in GAM])
            if not MUTATE:
                for bt in (0.5, -0.5):
                    DOBS_B[(n, rd, ft, bt)] = np.array([delta(n, g, ("pl", gm), bt) if W_PRI[i] > 0 else np.nan for i, gm in enumerate(GAM)])
            if n == 4486:
                DC[(rd, ft)] = delta(n, g, ("rho", RHO_C)); DZ[(rd, ft)] = delta(n, g, ("rho", RHO_Z))
                for bt in (0.5, -0.5):
                    DC_B[(rd, ft, bt)] = delta(n, g, ("rho", RHO_C), bt)
P(f"[{time.time() - T0:.0f}s] exact Delta_obs(gamma) on the grid done")


# ------------------------------------------------------------------ 4. bootstrap over the GCs (full CFG331 binning pipeline)
def bins_from(a_raw, n):
    """exact copy of CFG331's bins_for, on a given GC array"""
    g = GAL[n]; a = np.asarray(a_raw, float)
    if len(a) < 8:
        return None
    a = clipped(a, g["vsys"])
    if len(a) < 30:
        return None
    kpc_am = math.pi / 180 / 60 * g["D"] * 1e3
    R = a[:, 0] * kpc_am
    o = np.argsort(R); a, R = a[o], R[o]
    nb = max(2, min(6, len(a) // 25))
    idx = np.array_split(np.arange(len(a)), nb)
    out = []
    for ii in idx:
        if len(ii) < 12:
            continue
        mu, s = ml_sigma(a[ii, 1], a[ii, 2])
        out.append((float(np.median(R[ii])), s, len(ii)))
    if len(out) < 2:
        return None
    Re = g["Re_as"] * ARCSEC * g["D"] * 1e3
    Rb = np.array([b[0] for b in out]); Sb = np.array([b[1] for b in out])
    outer = Rb > max(Re, 2.0)
    if not outer.any():
        outer = np.ones(len(Rb), bool)
    return Rb, Sb, outer


ARAW = {n: np.array(GCS[n], float) for n in CENTRALS}
RTAB, LTAB = {}, {}
for n in CENTRALS:
    kpc_am = math.pi / 180 / 60 * GAL[n]["D"] * 1e3
    rr = ARAW[n][:, 0] * kpc_am
    RTAB[n] = np.geomspace(rr.min() * 0.99, rr.max() * 1.01, 60)
TAB = {}                                                          # (n, rd, ft, kind) -> log10 sigma_pred on (gamma, Rtab)
for n in CENTRALS:
    for rd in READ:
        for ft in FEET:
            g = FIELD[(n, rd, ft)]
            TAB[(n, rd, ft, "pl")] = np.array([np.log10(sig_los(RTAB[n], g, gm, 0.0)) for gm in GAM])
            if n == 4486:
                TAB[(n, rd, ft, "c")] = np.log10(sig_los_rho(RTAB[n], g, RHO_C, 0.0))[None, :]
P(f"[{time.time() - T0:.0f}s] prediction tables done")


def d_from_tab(T, lRt, Rb, Sb, outer):
    lr_ = np.log(Rb[outer]); i1 = np.clip(np.searchsorted(lRt, lr_), 1, len(lRt) - 1); i0 = i1 - 1
    w = (lr_ - lRt[i0]) / (lRt[i1] - lRt[i0])
    ls = T[:, i0] * (1 - w) + T[:, i1] * w
    return np.mean(np.log10(Sb[outer])[None, :] - ls, axis=1)


DSTAR = {}
NFAIL_BOOT = {}
for n in CENTRALS:
    rng = np.random.default_rng([SEED, n]); A = ARAW[n]; N = len(A); lRt = np.log(RTAB[n])
    keys = [k for k in TAB if k[0] == n]
    acc = {k: [] for k in keys}; nf = 0
    for _ in range(NB):
        res = bins_from(A[rng.integers(0, N, N)], n)
        if res is None:
            nf += 1; continue
        for k in keys:
            acc[k].append(d_from_tab(TAB[k], lRt, *res))
    for k in keys:
        DSTAR[k] = np.array(acc[k])
    NFAIL_BOOT[n] = nf
    P(f"[{time.time() - T0:.0f}s] bootstrap NGC{n}: {NB - nf}/{NB} usable resamples")
SIG = {k: DSTAR[k].std(axis=0, ddof=1) for k in DSTAR}          # sigma_Delta per gamma (or per profile)
# table-interpolation accuracy at the observed bins
TABERR = 0.0
for n in CENTRALS:
    b = B[n]; lRt = np.log(RTAB[n])
    for rd in READ:
        for ft in FEET:
            TABERR = max(TABERR, float(np.max(np.abs(d_from_tab(TAB[(n, rd, ft, "pl")], lRt, b["Rb"], b["Sb"], b["outer"]) - DOBS[(n, rd, ft)]))))


def zf(p):
    return float(-ndtri(min(max(p, 1e-300), 1 - 1e-16)))


def fz(z):
    return f"{z:+.2f}" if abs(z) < 8 else (">+8" if z > 0 else "<-8")


def outcome(pG, pE):
    if pG >= 1 - P2:
        return "REVERSED"
    fG, fE = pG <= P2, pE <= P2
    if fG and fE:
        return "FAIL"
    if (not fG) and (not fE):
        return "CLEARED"
    return "FRAGILE"


def prior_stats(n, rd, ft, W, beta=None):
    """prior-marginalised Gaussian and empirical p for a power-law tracer (beta None = 0, else shift)"""
    d = DOBS[(n, rd, ft)] if beta is None else DOBS_B[(n, rd, ft, beta)]
    ds = DSTAR[(n, rd, ft, "pl")]; s = SIG[(n, rd, ft, "pl")]
    m = W > 0
    if beta is not None:
        ds = ds[:, m] - DOBS[(n, rd, ft)][m][None, :] + d[m][None, :]
    else:
        ds = ds[:, m]
    pg = ndtr(-d[m] / s[m]); pe = (ds <= 0).mean(axis=0)
    PG, PE = float(np.sum(W[m] * pg)), float(np.sum(W[m] * pe))
    return dict(pG=PG, pE=PE, Z=zf(PG), outcome=outcome(PG, PE))


def gamma_null(n, rd, ft):
    g = FIELD[(n, rd, ft)]; fn = lambda gm: delta(n, g, ("pl", gm))
    a, b_ = fn(1.0), fn(4.0)
    return brentq(fn, 1.0, 4.0, xtol=1e-4) if a * b_ < 0 else None


def at_gamma(n, rd, ft, gm):
    d = delta(n, FIELD[(n, rd, ft)], ("pl", gm)); s = float(np.interp(gm, GAM, SIG[(n, rd, ft, "pl")]))
    return d, s, d / s


RESULTS = {}
# ------------------------------------------------------------------ 5. main run
if not MUTATE:
    # ---- M87 Monte Carlo over Agnello+14's published errors
    rng = np.random.default_rng([SEED, 87])

    def draw(v, ep, em, lo):
        while True:
            z = rng.standard_normal(); x = v + (ep * z if z > 0 else em * z)
            if x > lo:
                return x
    DMC = {(rd, ft): [] for rd in READ for ft in FEET}
    DMC_P = []
    for k in range(NMC):
        nv = [draw(*TR["A14_n"][j], 0.5) for j in range(3)]
        rev = [draw(*TR["A14_Re_as"][j], 5.0) for j in range(3)]
        sib = draw(*TR["A14_Sib"], 0.0); srb = draw(*TR["A14_Srb"], 0.0)
        rho = a14_rho(nv, rev, sib, srb)
        DMC_P.append(dict(n=nv, Re=rev, sib=sib, srb=srb))
        for rd in READ:
            for ft in FEET:
                DMC[(rd, ft)].append(delta(4486, FIELD[(4486, rd, ft)], ("rho", rho)))
        if (k + 1) % 50 == 0:
            P(f"[{time.time() - T0:.0f}s] M87 MC {k + 1}/{NMC}")
    DMC = {k: np.array(v) for k, v in DMC.items()}

    def m87_stats(rd, ft, shift=0.0):
        d = DMC[(rd, ft)] + shift; s = float(SIG[(4486, rd, ft, "c")][0]); ds = DSTAR[(4486, rd, ft, "c")][:, 0]; dc = DC[(rd, ft)]
        PG = float(np.mean(ndtr(-d / s)))
        PE = float(np.mean([(ds - dc + x <= 0).mean() for x in d]))
        return dict(pG=PG, pE=PE, Z=zf(PG), outcome=outcome(PG, PE), sigma=s, Dc=dc + shift,
                    Dmc_q=np.percentile(d, [2.275, 15.87, 50, 84.13, 97.725]).tolist(), Zc=(dc + shift) / s)

    PRIM, AUX = {}, {}
    for rd in READ:
        for ft in FEET:
            for n in CENTRALS:
                if n == 4486:
                    r = m87_stats(rd, ft)
                    r.update(slope="measured Agnello+14 (MC %d)" % NMC, Z_lit=r["Zc"], lit="measured profile")
                else:
                    r = prior_stats(n, rd, ft, W_PRI)
                    dl, sl, zl = at_gamma(n, rd, ft, GREL[n])
                    r.update(slope="prior U[2,4]", Z_lit=zl, lit=f"Alabi+16 relation gamma {GREL[n]:.2f}", D_lit=dl)
                PRIM[(n, rd, ft)] = r
                a = {}
                for gm in (2.0, 2.5, 3.0, 3.5, 4.0):
                    i = int(np.argmin(np.abs(GAM - gm))); a[f"D_g{gm}"] = float(DOBS[(n, rd, ft)][i]); a[f"sig_g{gm}"] = float(SIG[(n, rd, ft, "pl")][i])
                a["Z_edge_g2"] = a["D_g2.0"] / a["sig_g2.0"]
                a["gamma_null"] = gamma_null(n, rd, ft)
                a["rel_prior"] = prior_stats(n, rd, ft, w_rel(n))
                a["wide_prior"] = prior_stats(n, rd, ft, W_WIDE)
                a["U24_power_law"] = prior_stats(n, rd, ft, W_PRI)
                if n == 4486:
                    for bt in (0.5, -0.5):
                        a[f"beta{bt:+.1f}"] = m87_stats(rd, ft, shift=DC_B[(rd, ft, bt)] - DC[(rd, ft)])
                    a["zhu_single_sersic"] = dict(D=DZ[(rd, ft)], Z=DZ[(rd, ft)] / float(SIG[(4486, rd, ft, "c")][0]))
                else:
                    for bt in (0.5, -0.5):
                        a[f"beta{bt:+.1f}"] = prior_stats(n, rd, ft, W_PRI, beta=bt)
                AUX[(n, rd, ft)] = a

    def classify(rows):
        nF = sum(r["outcome"] == "FAIL" for r in rows); nC = sum(r["outcome"] == "CLEARED" for r in rows)
        lit_ok = all(r["Z_lit"] < 2 for r in rows if r["outcome"] == "CLEARED")
        if nF >= 3:
            return "ROBUST FAIL", nF, nC
        if nC >= 3 and lit_ok:
            return "SLOPE ARTEFACT", nF, nC
        return "NOT DIAGNOSTIC", nF, nC

    CLS = {(rd, ft): classify([PRIM[(n, rd, ft)] for n in CENTRALS]) for rd in READ for ft in FEET}
    cells = [CLS[(rd, ft)][0] for rd in DECIDE for ft in FEET]
    HEAD = "ROBUST FAIL" if all(c == "ROBUST FAIL" for c in cells) else ("SLOPE ARTEFACT" if all(c == "SLOPE ARTEFACT" for c in cells) else "NOT DIAGNOSTIC")

    # centrals' mean with independent gamma draws (reported)
    rngm = np.random.default_rng([SEED, 4])
    MEAN = {}
    for rd in READ:
        for ft in FEET:
            K = 20000; tot = np.zeros(K); var = np.zeros(K)
            for n in PRIOR3:
                gd = rngm.uniform(2.0, 4.0, K)
                tot += np.interp(gd, GAM, DOBS[(n, rd, ft)]); var += np.interp(gd, GAM, SIG[(n, rd, ft, "pl")]) ** 2
            tot += rngm.choice(DMC[(rd, ft)], K); var += float(SIG[(4486, rd, ft, "c")][0]) ** 2
            mm, ss = tot / 4, np.sqrt(var) / 4
            pg = float(np.mean(ndtr(-mm / ss)))
            MEAN[(rd, ft)] = dict(mean_median=float(np.median(mm)), sigma_median=float(np.median(ss)), pG=pg, Z=zf(pg))

    # ---- print
    P("=" * 124)
    P("CFG466 -- the four SLUGGS centrals with the GC tracer slope FREE (law + baryons exactly CFG330 K0 / CFG331)")
    P("=" * 124)
    P(f"Frozen criteria {FROZEN}. Bootstrap N_B = {NB} (seed {SEED}); M87 MC N = {NMC}; prior U[2,4] on 101 points; FAIL = p_G and p_E <= {P2}")
    P("Tracers: M87 measured (Agnello+14 three-population Sersic, Abel-deprojected; local slope at its outer bins "
      f"{', '.join(f'{x:.2f}' for x in G_LOC87)}); NGC 4365/4374/5846 prior U[2,4] (no GC density profile on disk).")
    P(f"Alabi+16 relation slopes (literature check): " + ", ".join(f"NGC{n} {GREL[n]:.2f}" for n in CENTRALS))
    P("Bins per central: " + "; ".join(f"NGC{n} {len(B[n]['Rb'])} bins, {int(B[n]['outer'].sum())} outer ({', '.join(f'{r:.1f}' for r in B[n]['Rb'][B[n]['outer']])} kpc), N_GC {B[n]['N']}" for n in CENTRALS))
    for rd in READ:
        for ft in FEET:
            P("\n" + "-" * 124)
            P(f"[{ft} | {rd}{'  (DECISION)' if rd in DECIDE else '  (reported)'}]   class: {CLS[(rd, ft)][0]}  (FAIL {CLS[(rd, ft)][1]}/4, CLEARED {CLS[(rd, ft)][2]}/4)")
            for n in CENTRALS:
                r = PRIM[(n, rd, ft)]; a = AUX[(n, rd, ft)]
                gnull = "none in [1,4]" if a["gamma_null"] is None else f"{a['gamma_null']:.2f}"
                if n == 4486:
                    q = r["Dmc_q"]
                    P(f"  NGC4486 measured: Delta_c {r['Dc']:+.3f} +- {r['sigma']:.3f} (Z_c {r['Zc']:+.1f}); MC Delta median {q[2]:+.3f} [2.3%..97.7%: {q[0]:+.3f}..{q[4]:+.3f}]"
                      f" | p_G {r['pG']:.2e} p_E {r['pE']:.2e} Z_free {fz(r['Z'])} -> {r['outcome']}")
                    P(f"           gamma=3 {a['D_g3.0']:+.3f}; power law: Delta(2) {a['D_g2.0']:+.3f} Delta(4) {a['D_g4.0']:+.3f}; gamma_null {gnull}; "
                      f"U[2,4] instead: Z {fz(a['U24_power_law']['Z'])} ({a['U24_power_law']['outcome']}); Zhu/Peng single Sersic Delta {a['zhu_single_sersic']['D']:+.3f} Z {fz(a['zhu_single_sersic']['Z'])}")
                else:
                    P(f"  NGC{n} U[2,4]: Delta(2) {a['D_g2.0']:+.3f} Delta(3) {a['D_g3.0']:+.3f} Delta(4) {a['D_g4.0']:+.3f}; sigma_Delta(3) {a['sig_g3.0']:.3f}"
                      f" | p_G {r['pG']:.2e} p_E {r['pE']:.2e} Z_free {fz(r['Z'])} -> {r['outcome']}")
                    P(f"           Z at gamma=2 edge {a['Z_edge_g2']:+.2f}; Z at Alabi gamma {GREL[n]:.2f}: {r['Z_lit']:+.2f}; gamma_null {gnull}; "
                      f"rel prior Z {fz(a['rel_prior']['Z'])}; wide U[{GMIN87:.2f},4] Z {fz(a['wide_prior']['Z'])} ({a['wide_prior']['outcome']})")
                P(f"           beta +0.5: Z {fz(a['beta+0.5']['Z'])} ({a['beta+0.5']['outcome']}); beta -0.5: Z {fz(a['beta-0.5']['Z'])} ({a['beta-0.5']['outcome']})")
            mn = MEAN[(rd, ft)]
            P(f"  centrals' mean (independent gamma draws, reported): median {mn['mean_median']:+.3f} +- {mn['sigma_median']:.3f}; Z {fz(mn['Z'])}")

    P("\n" + "-" * 124); P("CLASS TABLE (decision readings K0 and R-own; R-bar/R-barN/R-efe reported)"); P("-" * 124)
    for rd in READ:
        P(f"  {rd:5}: " + "  |  ".join(f"{ft}: {CLS[(rd, ft)][0]} (FAIL {CLS[(rd, ft)][1]}/4)" for ft in FEET)
          + "   per central: " + "; ".join(f"NGC{n} " + "/".join(PRIM[(n, rd, ft)]["outcome"] for ft in FEET) for n in CENTRALS))
    P(f"\n  HEADLINE: {HEAD}")

    # ---- reported-row classes (same class rule; not decision rows). M87 stays measured; its beta rows shift the MC by Delta_c(beta) - Delta_c.
    ALTCLS = {}
    for lab in ("beta+0.5", "beta-0.5", "rel_prior", "wide_prior"):
        for rd in DECIDE:
            for ft in FEET:
                rows = []
                for n in CENTRALS:
                    if n == 4486 and lab in ("rel_prior", "wide_prior"):
                        r = dict(PRIM[(n, rd, ft)])
                    else:
                        r = dict(AUX[(n, rd, ft)][lab]); r["Z_lit"] = PRIM[(n, rd, ft)]["Z_lit"]
                    rows.append(r)
                ALTCLS[(lab, rd, ft)] = classify(rows) + ("/".join(r["outcome"] for r in rows),)
    P("  reported-row classes (decision readings; order NGC4486/4365/4374/5846):")
    for lab in ("beta+0.5", "beta-0.5", "rel_prior", "wide_prior"):
        P(f"    {lab:10}: " + "  |  ".join(f"{rd} {ft}: {ALTCLS[(lab, rd, ft)][0]} ({ALTCLS[(lab, rd, ft)][3]})" for rd in DECIDE for ft in FEET))

    # ---- post-freeze diagnostic: R-own with the host gas truncated at its measured edge (no extrapolation beyond the X-ray field)
    def field_own_trunc(n, a0):
        b = B[n]; Mg0 = GAS[n][0]; rm = GAS[n][1]["r_meas"]
        Mg = np.where(RG <= rm, Mg0, float(np.interp(math.log(rm), LR, Mg0)))
        M = calib(n, a0, Mg); Mx = Mg.copy()
        if n in (4486, 5846):
            for rp, dk in zip(MEM[n]["Rp"], MEM[n]["dK"]):
                Mx = Mx + M * 10 ** (-0.4 * dk) * (RG >= rp)
        gN = gN_of(n, M, Mx)
        return nu(gN / a0) * gN
    TRUNC = {}
    P("\n" + "-" * 124)
    P("POST-FREEZE DIAGNOSTIC (not in the frozen text): R-own with host gas truncated at the measured X-ray edge (sigma_Delta and bootstrap from R-own)")
    P("-" * 124)
    for ft in FEET:
        gt = {n: field_own_trunc(n, A0[ft]) for n in CENTRALS}
        for bt in (0.0, 0.5):
            rows = []
            for n in CENTRALS:
                if n == 4486:
                    dct = delta(n, gt[n], ("rho", RHO_C), bt)
                    r = m87_stats("own", ft, shift=dct - DC[("own", ft)])
                else:
                    dt = np.array([delta(n, gt[n], ("pl", gm), bt) if W_PRI[i] > 0 else np.nan for i, gm in enumerate(GAM)])
                    m = W_PRI > 0; s_ = SIG[(n, "own", ft, "pl")]
                    ds = DSTAR[(n, "own", ft, "pl")][:, m] - DOBS[(n, "own", ft)][m][None, :] + dt[m][None, :]
                    pg = float(np.sum(W_PRI[m] * ndtr(-dt[m] / s_[m]))); pe = float(np.sum(W_PRI[m] * (ds <= 0).mean(axis=0)))
                    r = dict(pG=pg, pE=pe, Z=zf(pg), outcome=outcome(pg, pe), D_g2=float(dt[IPRI[0]]))
                r["Z_lit"] = PRIM[(n, "own", ft)]["Z_lit"]; rows.append(r)
            c = classify(rows); TRUNC[(ft, bt)] = dict(cls=c[0], rows=rows)
            P(f"  [{ft} | own-trunc | beta {bt:+.1f}] " + "; ".join(f"NGC{n} Z {fz(r['Z'])} ({r['outcome']})" for n, r in zip(CENTRALS, rows)) + f" -> {c[0]}")

    P("\n" + "-" * 124)
    P("POST-FREEZE DIAGNOSTIC (not in the frozen text): extra per-galaxy error that would clear each central at its most favourable admissible slope")
    P("-" * 124)
    P("  sigma_sys = sqrt((Delta_fav/2)^2 - sigma_Delta^2) dex in sigma_los, i.e. what would bring Z to 2; Delta_fav = Delta at gamma = 2 (prior galaxies)"
      " or the M87 MC 2.275% quantile (measured profile).")
    HEADROOM = {}
    for rd in DECIDE:
        for ft in FEET:
            row = []
            for n in CENTRALS:
                if n == 4486:
                    dfav = PRIM[(n, rd, ft)]["Dmc_q"][0]; s_ = PRIM[(n, rd, ft)]["sigma"]
                else:
                    dfav = AUX[(n, rd, ft)]["D_g2.0"]; s_ = AUX[(n, rd, ft)]["sig_g2.0"]
                ss = math.sqrt(max((dfav / 2) ** 2 - s_ ** 2, 0.0)); HEADROOM[(n, rd, ft)] = dict(D_fav=dfav, sigma=s_, sigma_sys=ss)
                row.append(f"NGC{n} {ss:.3f} (Delta_fav {dfav:+.3f}, sigma {s_:.3f})")
            P(f"  [{ft} | {rd}] " + "; ".join(row))

    # ---- controls
    P("\n" + "-" * 124); P("CHECKS"); P("-" * 124)
    ok = []

    def check(lbl, cond, det):
        ok.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")
    i3 = int(np.argmin(np.abs(GAM - 3.0)))
    d1 = max(abs(DOBS[(n, rd, ft)][i3] - committed(n, rd, ft)) for n in CENTRALS for rd in READ for ft in FEET)
    check("C1 power-law path at gamma = 3, beta = 0 reproduces committed CFG330 K0 and CFG331 own/bar/barN/efe per central, both footings, to 1e-9 dex",
          d1 < 1e-9, f"max |diff| {d1:.2e} (40 values)")
    d2 = 0.0
    for n in CENTRALS:
        g = FIELD[(n, "K0", "canonical")]
        for gm in (2.0, 3.0, 4.0):
            d2 = max(d2, abs(delta(n, g, ("rho", RG ** -gm)) - delta(n, g, ("pl", gm))))
    check("C2 general-rho Jeans with rho = r^-gamma reproduces the power-law path at gamma 2, 3, 4 per central to 1e-5 dex", d2 < 1e-5, f"max |diff| {d2:.2e}")
    rp = np.zeros_like(RG); rp_ = abel_rho(lambda R: -4 * R * (1 + R ** 2) ** -3, RG)
    msk = (RG > 0.1) & (RG < 30)
    c3 = float(np.max(np.abs(-np.gradient(np.log(np.maximum(rp_, 1e-300)), LR)[msk] - (5 * RG ** 2 / (1 + RG ** 2))[msk])))
    check("C3 Abel deprojection: Plummer Sigma ~ (1+R^2)^-2 -> rho log-slope within 0.01 over 0.1-30 a", c3 < 0.01, f"max |slope error| {c3:.2e}")
    c4 = {ft: DC[("K0", ft)] - C323J["reported"][ft]["M87 no gas"]["4486"] for ft in FEET}
    check("C4 central Agnello profile + K0 field reproduces CFG323 'M87 no gas' (+0.21780 / +0.20620) to 0.005 dex",
          all(abs(v) < 0.005 for v in c4.values()), "; ".join(f"{ft} {DC[('K0', ft)]:+.5f} (diff {v:+.1e})" for ft, v in c4.items()))
    # C5 synthetic bootstrap calibration on NGC 5846's radii and errors
    n5 = 5846; A5 = ARAW[n5].copy(); vs = GAL[n5]["vsys"]; sig0 = float(np.mean(B[n5]["Sb"][B[n5]["outer"]]))
    T5 = TAB[(n5, "K0", "canonical", "pl")][[i3]]; lR5 = np.log(RTAB[n5]); r5 = np.random.default_rng([SEED, 5])

    def syn():
        a = A5.copy(); a[:, 1] = vs + r5.normal(0.0, np.sqrt(sig0 ** 2 + a[:, 2] ** 2)); return a
    reals = []
    first = None
    for k in range(NREAL_C5):
        a = syn(); res = bins_from(a, n5)
        if first is None:
            first = a
        if res is not None:
            reals.append(float(d_from_tab(T5, lR5, *res)[0]))
    sd_true = float(np.std(reals, ddof=1))
    bs = []
    for k in range(NB_C5):
        res = bins_from(first[r5.integers(0, len(first), len(first))], n5)
        if res is not None:
            bs.append(float(d_from_tab(T5, lR5, *res)[0]))
    sd_boot = float(np.std(bs, ddof=1))
    check("C5 bootstrap SD of Delta on one synthetic NGC 5846 realisation within +-25% of the SD over 300 independent realisations",
          0.75 <= sd_boot / sd_true <= 1.25, f"sd_boot {sd_boot:.4f} vs sd_true {sd_true:.4f} (ratio {sd_boot / sd_true:.3f}); sigma_true {sig0:.1f} km/s")
    c6 = 0.0; c6o = True
    for n in CENTRALS:
        Rb, Sb, o = bins_from(ARAW[n], n)
        c6 = max(c6, float(np.max(np.abs(Rb - B[n]["Rb"]))), float(np.max(np.abs(Sb - B[n]["Sb"])))); c6o &= bool(np.array_equal(o, B[n]["outer"]))
    check("C6 bootstrap binning code on the unresampled data reproduces CFG331's bins exactly", c6 == 0.0 and c6o, f"max |diff| {c6:.1e}; outer masks equal {c6o}")
    P(f"  (diagnostic) table interpolation error at the observed bins: max {TABERR:.1e} dex; unusable bootstrap resamples "
      + ", ".join(f"NGC{n} {NFAIL_BOOT[n]}" for n in CENTRALS))
    P(f"\n  {sum(ok)}/{len(ok)} checks pass   [{time.time() - T0:.0f}s]")

    def jk(d):
        return {f"NGC{k[0]}|{k[1]}|{k[2]}": v for k, v in d.items()}
    RESULTS = dict(lane="CFG466", frozen_commit=FROZEN, mutate=False, kernel="nu_mono", kappa="1/2 FITTED", a0=A0, NB=NB, NMC=NMC, seed=SEED,
                   headline=HEAD, classes={f"{rd}|{ft}": dict(cls=CLS[(rd, ft)][0], n_fail=CLS[(rd, ft)][1], n_cleared=CLS[(rd, ft)][2]) for rd in READ for ft in FEET},
                   primary=jk(PRIM), reported=jk(AUX), post_freeze_headroom=jk(HEADROOM), reported_classes={f"{k[0]}|{k[1]}|{k[2]}": dict(cls=v[0], n_fail=v[1], n_cleared=v[2], outcomes=v[3]) for k, v in ALTCLS.items()}, post_freeze_own_trunc={f"{ft}|beta{bt:+.1f}": v for (ft, bt), v in TRUNC.items()}, centrals_mean={f"{rd}|{ft}": v for (rd, ft), v in MEAN.items()},
                   m87=dict(local_slope_outer_bins=G_LOC87.tolist(), gamma_min=GMIN87, mc_params_first5=DMC_P[:5]),
                   gamma_rel=GREL, gamma_grid=GAM.tolist(),
                   delta_obs={f"NGC{n}|{rd}|{ft}": DOBS[(n, rd, ft)].tolist() for n in CENTRALS for rd in READ for ft in FEET},
                   sigma_delta={f"NGC{k[0]}|{k[1]}|{k[2]}|{k[3]}": SIG[k].tolist() for k in SIG},
                   checks=dict(C1=d1, C2=d2, C3=c3, C4=c4, C5=dict(sd_boot=sd_boot, sd_true=sd_true), C6=c6, table_err=TABERR),
                   n_pass=sum(ok), n_checks=len(ok), unusable_resamples={f"NGC{n}": NFAIL_BOOT[n] for n in CENTRALS})

# ------------------------------------------------------------------ 6. MUTATE
else:
    P("=" * 124); P("CFG466 MUTATE -- M1 gamma = 3 forced (reproduction), M2 gamma = 1.5 forced (sensitivity)"); P("=" * 124)
    ok = []

    def check(lbl, cond, det):
        ok.append(bool(cond)); P(f"  [{'PASS' if cond else 'FAIL'}] {lbl}\n         {det}")
    # M1: every central (M87's measured profile replaced by r^-3) through the same delta() path
    m1 = {}
    for n in CENTRALS:
        for rd in READ:
            for ft in FEET:
                m1[(n, rd, ft)] = delta(n, FIELD[(n, rd, ft)], ("pl", 3.0))
    d1 = max(abs(m1[k] - committed(*k)) for k in m1)
    P("  M1 per central (canonical): " + "; ".join(f"{rd}: " + " ".join(f"NGC{n} {m1[(n, rd, 'canonical')]:+.4f}" for n in CENTRALS) for rd in READ))
    check("M1 gamma = 3 forced for all four reproduces committed CFG330 K0 and CFG331 R-own/R-bar/R-barN/R-efe to 1e-9 dex, both footings",
          d1 < 1e-9, f"max |diff| {d1:.2e} (40 values)")
    # M2: gamma = 1.5 forced; the forced slope counts as measured
    i15 = int(np.argmin(np.abs(GAM - 1.5))); assert abs(GAM[i15] - 1.5) < 1e-9
    main = json.load(open(os.path.join(HERE, "cfg466_free_slope_results.json")))
    M2 = {}; CLS2 = {}
    for rd in READ:
        for ft in FEET:
            rows = []
            for n in CENTRALS:
                d = float(DOBS[(n, rd, ft)][i15]); s = float(SIG[(n, rd, ft, "pl")][i15])
                pG = float(ndtr(-d / s)); pE = float((DSTAR[(n, rd, ft, "pl")][:, i15] <= 0).mean())
                r = dict(D=d, sigma=s, Zg=d / s, pG=pG, pE=pE, outcome=outcome(pG, pE), Z_lit=d / s,
                         Z_main=main["primary"][f"NGC{n}|{rd}|{ft}"]["Z"])
                M2[(n, rd, ft)] = r; rows.append(r)
            nF = sum(r["outcome"] == "FAIL" for r in rows); nC = sum(r["outcome"] == "CLEARED" for r in rows)
            lit_ok = all(r["Z_lit"] < 2 for r in rows if r["outcome"] == "CLEARED")
            CLS2[(rd, ft)] = ("ROBUST FAIL" if nF >= 3 else ("SLOPE ARTEFACT" if (nC >= 3 and lit_ok) else "NOT DIAGNOSTIC"), nF, nC)
            P(f"  [{ft} | {rd}] gamma 1.5: " + "; ".join(f"NGC{n} {M2[(n, rd, ft)]['D']:+.3f} (Z {M2[(n, rd, ft)]['Zg']:+.1f}, {M2[(n, rd, ft)]['outcome']})" for n in CENTRALS)
              + f" -> {CLS2[(rd, ft)][0]}")
    cells = [CLS2[(rd, ft)][0] for rd in DECIDE for ft in FEET]
    HEAD2 = "ROBUST FAIL" if all(c == "ROBUST FAIL" for c in cells) else ("SLOPE ARTEFACT" if all(c == "SLOPE ARTEFACT" for c in cells) else "NOT DIAGNOSTIC")
    P(f"\n  M2 headline at gamma = 1.5: {HEAD2}   (main run headline: {main['headline']})")
    check("M2 gamma = 1.5 forced moves the headline class away from the main run's", HEAD2 != main["headline"], f"{main['headline']} -> {HEAD2}")
    lower = all(M2[(n, rd, ft)]["Zg"] < M2[(n, rd, ft)]["Z_main"] for n in CENTRALS for rd in DECIDE for ft in FEET)
    P(f"  (reported) every central's Gaussian Z at gamma 1.5 below its main-run Z_free (decision readings): {lower}")
    P(f"\n  {sum(ok)}/{len(ok)} checks pass   [{time.time() - T0:.0f}s]")
    RESULTS = dict(lane="CFG466", frozen_commit=FROZEN, mutate=True, M1_max_diff=d1, M1={f"NGC{k[0]}|{k[1]}|{k[2]}": v for k, v in m1.items()},
                   M2={f"NGC{k[0]}|{k[1]}|{k[2]}": v for k, v in M2.items()},
                   M2_classes={f"{rd}|{ft}": dict(cls=c[0], n_fail=c[1], n_cleared=c[2]) for (rd, ft), c in CLS2.items()},
                   M2_headline=HEAD2, main_headline=main["headline"], M2_Z_all_lower=lower, n_pass=sum(ok), n_checks=len(ok))

json.dump(RESULTS, open(os.path.join(HERE, f"cfg466_free_slope{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg466_free_slope{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(ok) else 1)
