#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG4 (part 1 of 5) -- THE GALAXY LAW THE DATA FORCE: the total field of bound galaxies as a function of their baryons, read
off SPARC (175 galaxies) with a0 fixed by the framework on both footings; the functional form nu and its allowed range; the
scatter budget; the baryonic Tully-Fisher normalisation; the dark density the law implies,
rho_eff = div[(nu - 1) g_bar]/(4 pi G), and its integral properties (surface density, core radius); and a verdict on the
record's use of a halo surface density ~ a0/(2 pi G).

THE BASE.  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED (never derived; Z = 2 sqrt(8 pi/3) = 5.7888 is the same
statement), flat in z.  Footings: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (FP0's committed pair).  The law's form is the
framework's own: g_obs = nu(g_bar/a0) g_bar.  Two named kernels are carried: P2 = sqrt(1 + 1/y) (the framework's postulate,
FP0/FP1) and nu_mono (the chain's monotone repair of the exponential RAR shape, the 09-26 kernel decision; FP1's committed
definition exec'd read-only).  To say what the DATA allow, a one-parameter transition family is scanned:
nu_beta(y) = (1 + y^-beta)^(1/(2 beta)) (deep limit y^-1/2 for every beta; beta = 1 is P2).  This family is an effective
description of the transition sharpness, not a theory.

DATA.  real_research/data/sparc_data/*_rotmod.dat (175 rotation curves with their baryonic components) and
real_research/data/SPARC_Lelli2016c.mrt (distances, inclinations, 3.6 um luminosities, HI masses, Vflat, quality flags).
The record's statistic is kept exactly (real_research/rar_framework_a0_mlfit.py; FP1 C0/C2): the weighted rms of
log10(g_obs) - log10(nu g_bar), weights (V_obs/e_V)^2 with e_V, V_obs clipped at 1 km/s, Upsilon_bul = 1.4 Upsilon_disk,
one global Upsilon_disk profiled on the grid 0.30-1.20 (step 0.01).

PRE-DECLARED (written before any run of this script; expectations from FP1 and the record's RAR fit):
  H1 CONTROLS.  (a) The record's SPARC RAR fit, real_research/rar_framework_a0_mlfit.py, exec'd read-only, is reproduced
     exactly by this lane's vectorised statistic (its own a0 = 9.3614e-11, Upsilon = 0.70: 0.108 dex; its fine-grid optimum
     0.70); (b) FP1 C2's committed rms and Upsilon for P2 and nu_mono on both footings are reproduced to < 1e-9.
     EXPECT TRUE.
  H2 [HEADLINE] THE LAW FITS.  At the framework's a0 on both footings, with one global Upsilon profiled, P2 and nu_mono fit
     SPARC with a weighted rms <= 0.110 dex at a 3.6-um Upsilon_disk inside 0.50-0.80, while the Newtonian law (no phantom)
     cannot do better than 0.25 dex at any Upsilon.  EXPECT TRUE.
  H3 THE SHAPE.  SPARC at fixed a0 constrains the transition sharpness beta to a finite band.  Expected: the band sits
     ABOVE beta = 1 (the data prefer a sharper transition than P2, as nu_mono's lower rms suggests, FP1 C2), with P2 outside
     or at the edge of the galaxy-bootstrap 95% band.  UNCERTAIN; the measured band is the law's allowed range.
  H4 THE SCATTER BUDGET.  The observational error model (velocity errors per point; distance, inclination and Upsilon
     (0.10 dex population scatter) coherent per galaxy) accounts for most of the observed scatter, and the maximum-likelihood
     per-point intrinsic scatter is <= 0.06 dex at 95% on both footings for both kernels.  EXPECT TRUE.
  H5 THE BTFR.  On the clean Vflat sample (Q <= 2, e_Vflat/Vflat <= 0.1) the free slope lies in 3.5-4.5; at slope 4 the
     observed normalisation agrees within 0.10 dex with the law's own finite-radius prediction (the BTFR is the RAR's outer
     part), and differs from the deep-limit value 1/(G a0) by the finite-y offset.  UNCERTAIN on the deep-limit comparison.
  H6 THE DARK DENSITY AND ITS SURFACE DENSITY.  In spherical symmetry the phantom's enclosed surface density is exactly
     Sigma_ph(<r) = y (nu(y) - 1) a0/(pi G): for P2 it is bounded by Sigma_M = a0/(2 pi G) (reached only as y -> oo); nu_RAR's
     bound is 1.2952 Sigma_M (the record's h122); nu_mono has none (logarithmic growth).  On SPARC the median of each galaxy's
     largest Sigma_ph(<r) lies at 0.4-0.8 Sigma_M; the phantom's Burkert product rho0 r0 lies within 0.3 dex of Sigma_M.
     UNCERTAIN; the verdict on the record's 'halo surface density ~ a0/(2 pi G)' follows the numbers.
MUTATE=1 replaces the law by Newton (nu = 1) in every place the law is scored: the headline H2 must FAIL (rc = 1).

SCOPE.  The spherical (monopole) reading of the law on the measured baryonic curves, as the record's RAR statistic uses;
thin-disc curl-field corrections are not computed.  The error model's inputs are the SPARC table's errors plus a declared
0.10 dex Upsilon scatter.  Published comparison numbers (Donato et al. 2009 log rho0 r0 = 2.15 +- 0.2; Gentile et al. 2009
<Sigma>(<r0) = 72 +42/-27 Msun/pc^2) are quoted, not fitted.

Run from the repository root:  python3 campaign_fresh_gravity/CFG4_galaxy_law.py      (MUTATE=1 for the control run)
"""
import os
import re
import sys
import math
import json
import time
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG4_common as C
import numpy as np
from scipy.optimize import least_squares, minimize_scalar, minimize

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
R = C.Run("CFG4_galaxy_law")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("PRE-DECLARED")[0].strip())
P("\nPRE-DECLARED" + __doc__.split("PRE-DECLARED")[1].split("SCOPE.")[0].rstrip())
if C.MUTATE:
    P("\n  *** MUTATE=1: the law is replaced by Newton (nu = 1) wherever it is scored -- the headline H2 must FAIL ***")
A0 = C.A0
P(f"\n  a0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2 [FP0]; Sigma_M = a0/(2 pi G) = "
  f"{C.SIGMA_M['canonical']:.1f} / {C.SIGMA_M['alt']:.1f} Msun/pc^2; kappa = 1/2 fitted; Z = {C.Z_FRAME:.4f}")

# ================================================================================================ data
GAL = C.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
KPC_S = 3.0857e19                                                     # the record's kpc (rar_framework_a0_mlfit.py, FP1)
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL])
eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL])
Vd = np.concatenate([g["Vdisk"] for g in GAL])
Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WPT = (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)
WW = np.where(OK, WPT[:, None], 0.0)
ONEHOT = np.zeros((NG, len(Rm)))
ONEHOT[GI, np.arange(len(Rm))] = 1.0
P(f"\n  SPARC: {NG} galaxies, {len(Rm)} points; master table rows matched {sum(1 for g in GAL if g['meta'])}; Upsilon grid "
  f"{UPS[0]:.2f}-{UPS[-1]:.2f}")

NEWTON = lambda y: np.ones_like(np.asarray(y, float))


def law(kfun):
    return NEWTON if C.MUTATE else kfun


def sums(nuf, a0):
    """per-galaxy weighted SSR S[g, U] and weight W[g, U] of the record's statistic (vectorised over points and Upsilon)."""
    with np.errstate(all="ignore"):
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, nuf(np.where(OK, GB, 1.0) / a0) * np.where(OK, GB, 1.0), 1.0))
    return ONEHOT @ (WW * r_ ** 2), ONEHOT @ WW


def best(S, W, wg=None):
    wg = np.ones(NG) if wg is None else wg
    mse = (wg @ S) / (wg @ W)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i]), i


# ================================================================================================ K controls
banner("K  CONTROLS: the record's SPARC RAR fit (rar_framework_a0_mlfit.py) and FP1 C2, reproduced exactly")
MLFIT = os.path.join(C.REPO, "real_research", "rar_framework_a0_mlfit.py")
nsml, txt_ml = C.exec_slices(MLFIT, [(None, None)], name="rar_mlfit")
m_fine = re.search(r"fine grid: Upsilon_disk = ([0-9.]+), scatter = ([0-9.]+) dex", txt_ml)
ml_U, ml_s = float(m_fine.group(1)), float(m_fine.group(2))
a0_ml = float(nsml["a0_fw"])
s70_theirs, mo70_theirs = nsml["scatter"](0.70, 1.4 * 0.70, a0_ml)
S0, W0 = sums(C.nu_p2, a0_ml)
iu70 = int(np.argmin(np.abs(UPS - 0.70)))
s70_mine = math.sqrt(S0[:, iu70].sum() / W0[:, iu70].sum())
coarse = [(U, *nsml["scatter"](U, 1.4 * U, a0_ml)) for U in (0.5, 0.6, 0.7, 0.8, 1.0)]
P(f"    rar_framework_a0_mlfit.py (exec'd read-only): a0 = {a0_ml:.4e}; its fine-grid optimum Upsilon_disk = {ml_U:.2f}, scatter "
  f"{ml_s:.3f} dex; its scatter() at Upsilon 0.70 = {s70_theirs:.12f} (mean offset {mo70_theirs:+.4f}); this lane at the same "
  f"point {s70_mine:.12f}")
P("    its coarse table: " + ", ".join(f"U {u:.2f}: {s:.3f} ({m:+.2f})" for u, s, m in coarse)
  + "  [committed doc FRAMEWORK_A0_RAR_MLFIT_2026-06-06.md: 0.145/0.117/0.108/0.116/0.155]")
k1a = abs(s70_mine - s70_theirs) < 1e-12 and abs(ml_U - 0.70) < 1e-9 and abs(round(s70_theirs, 3) - 0.108) < 1e-12 and \
    [round(s, 3) for _, s, _ in coarse] == [0.145, 0.117, 0.108, 0.116, 0.155]
check("K1 CONTROL: the record's SPARC RAR fit (real_research/rar_framework_a0_mlfit.py, exec'd read-only) is reproduced "
      "exactly: at its own a0 = 9.3614e-11 and Upsilon_disk = 0.70 this lane's vectorised statistic equals its scatter() to "
      "< 1e-12, its fine-grid optimum is 0.70 at 0.108 dex, and its coarse table is the committed one",
      f"|mine - theirs| = {abs(s70_mine - s70_theirs):.1e}; optimum {ml_U:.2f} / {ml_s:.3f} dex; coarse "
      + "/".join(f"{s:.3f}" for _, s, _ in coarse), k1a)
fp1 = json.load(open(os.path.join(C.CHAIN, "FP1_static_sector_results.json")))["numbers"]["C2"]["sparc"]
k2 = {}
for f in C.FOOTS:
    Sp, Wp = sums(C.nu_p2, A0[f])
    Sm, Wm = sums(C.nu_mono, A0[f])
    rp, up, _ = best(Sp, Wp)
    rm, um, _ = best(Sm, Wm)
    k2[f] = (rp, up, rm, um)
dev2 = max(max(abs(k2[f][0] - fp1[f]["rms_P2"]), abs(k2[f][2] - fp1[f]["rms_mono"])) for f in C.FOOTS)
dup2 = max(max(abs(k2[f][1] - fp1[f]["ups_P2"]), abs(k2[f][3] - fp1[f]["ups_mono"])) for f in C.FOOTS)
check("K2 CONTROL: FP1 C2's committed SPARC numbers (P2 and nu_mono, both footings, Upsilon profiled) are reproduced",
      "; ".join(f"{f}: P2 {k2[f][0]:.6f} (U {k2[f][1]:.2f}) vs {fp1[f]['rms_P2']:.6f}, mono {k2[f][2]:.6f} (U {k2[f][3]:.2f}) vs "
                f"{fp1[f]['rms_mono']:.6f}" for f in C.FOOTS) + f"; max |d rms| {dev2:.1e}, max |d U| {dup2:.2f}",
      dev2 < 1e-9 and dup2 < 1e-9)
R.num("K", dict(mlfit=dict(a0=a0_ml, U=ml_U, scatter=ml_s, s70=s70_theirs, s70_mine=s70_mine), fp1_c2=k2))

# ================================================================================================ H2 the law fits
banner("H2  THE LAW ON SPARC: P2 and nu_mono at the framework's a0 (both footings), one global Upsilon profiled; Newton for contrast")
FITS = {}
for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        S_, W_ = sums(law(kf), A0[f])
        r_, u_, iu_ = best(S_, W_)
        FITS[(f, kn)] = dict(rms=r_, U=u_, iu=iu_, S=S_, W=W_)
    Sn, Wn = sums(NEWTON, A0[f])
    rn, un, _ = best(Sn, Wn)
    FITS[(f, "Newton")] = dict(rms=rn, U=un)
    P(f"    {f:9s}: P2 {FITS[(f, 'P2')]['rms']:.4f} dex (Upsilon_disk {FITS[(f, 'P2')]['U']:.2f}); nu_mono "
      f"{FITS[(f, 'nu_mono')]['rms']:.4f} dex (Upsilon {FITS[(f, 'nu_mono')]['U']:.2f}); Newton {rn:.4f} dex (Upsilon {un:.2f}, the "
      f"grid's edge)")
h2 = all(FITS[(f, k)]["rms"] <= 0.110 and 0.50 <= FITS[(f, k)]["U"] <= 0.80 for f in C.FOOTS for k in ("P2", "nu_mono")) and \
    all(FITS[(f, "Newton")]["rms"] >= 0.25 for f in C.FOOTS)
check("H2 [HEADLINE] THE LAW FITS SPARC: at the framework's a0 on both footings, with one global Upsilon profiled, P2 and nu_mono "
      "reach a weighted rms <= 0.110 dex at a 3.6-um Upsilon_disk inside 0.50-0.80, while Newton (no phantom) stays >= 0.25 dex",
      "; ".join(f"{f}: P2 {FITS[(f, 'P2')]['rms']:.4f}@{FITS[(f, 'P2')]['U']:.2f}, mono {FITS[(f, 'nu_mono')]['rms']:.4f}@"
                f"{FITS[(f, 'nu_mono')]['U']:.2f}, Newton {FITS[(f, 'Newton')]['rms']:.4f}" for f in C.FOOTS), h2)
R.num("H2", {f"{k[0]}|{k[1]}": dict(rms=v["rms"], U=v["U"]) for k, v in FITS.items()})

# ---- the a0-Upsilon degeneracy: a0 fitted at the population-synthesis prior Upsilon = 0.50, and kappa it implies
banner("H2b (reported) a0 AND Upsilon: the fitted a0 at the 3.6-um prior Upsilon_disk = 0.50, and the kappa each reading implies")
KAP_UNIT = C.C_SI * math.sqrt(C.G_SI * C.RHO_LAMBDA)                # a0 = kappa * this
iu50 = int(np.argmin(np.abs(UPS - 0.50)))
A0FIT = {}
for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
    lg = np.linspace(-10.5, -9.3, 241)
    rr = []
    for la in lg:
        S_, W_ = sums(law(kf), 10 ** la)
        rr.append(math.sqrt(S_[:, iu50].sum() / W_[:, iu50].sum()))
    rr = np.array(rr)
    i_ = int(np.argmin(rr))
    A0FIT[kn] = dict(a0=float(10 ** lg[i_]), rms=float(rr[i_]), kappa=float(10 ** lg[i_] / KAP_UNIT))
    P(f"    {kn:8s}: at Upsilon_disk = 0.50 the best a0 = {A0FIT[kn]['a0']:.3e} m/s^2 (rms {A0FIT[kn]['rms']:.4f}) -> kappa = "
      f"{A0FIT[kn]['kappa']:.3f} (the canonical footing is kappa = 0.5 with Upsilon {FITS[('canonical', kn)]['U']:.2f})")
check("H2b (reported) a0 and Upsilon are degenerate on SPARC: at the 3.6-um prior Upsilon_disk = 0.50 the fitted a0 is the "
      "printed value; the framework's kappa = 1/2 is the same fit at a higher Upsilon -- kappa stays FITTED",
      "; ".join(f"{k}: a0 {v['a0']:.3e} (kappa {v['kappa']:.3f})" for k, v in A0FIT.items()), True, load_bearing=False)
R.num("H2b", A0FIT)

# ================================================================================================ H3 the shape band
banner("H3  THE SHAPE THE DATA ALLOW: the transition family nu_beta = (1 + y^-beta)^(1/(2 beta)), galaxy bootstrap")
BETAS = np.round(np.geomspace(0.25, 6.0, 49), 4)
rng = np.random.default_rng(20260927)
NB = 1000
WB = rng.multinomial(NG, np.full(NG, 1.0 / NG), size=NB).astype(float)
SHAPE = {}
for f in C.FOOTS:
    SS = np.stack([sums(law(lambda y, b=b: C.nu_beta(y, b)), A0[f])[0] for b in BETAS])      # (nbeta, NG, NU)
    WS = np.stack([sums(law(lambda y, b=b: C.nu_beta(y, b)), A0[f])[1] for b in BETAS])
    full = np.array([best(SS[j], WS[j])[0] for j in range(len(BETAS))])
    jb = int(np.argmin(full))
    num = np.einsum("bg,kgu->bku", WB, SS)
    den = np.einsum("bg,kgu->bku", WB, WS)
    msb = (num / den).min(axis=2)                                                             # (NB, nbeta)
    bb = BETAS[np.argmin(msb, axis=1)]
    lo68, hi68 = np.percentile(bb, [16, 84])
    lo95, hi95 = np.percentile(bb, [2.5, 97.5])
    d1 = np.sqrt(msb[:, np.argmin(np.abs(BETAS - 1.0))]) - np.sqrt(msb.min(axis=1))
    SHAPE[f] = dict(best_beta=float(BETAS[jb]), best_rms=float(full[jb]), U_best=best(SS[jb], WS[jb])[1],
                    ci68=[float(lo68), float(hi68)], ci95=[float(lo95), float(hi95)], rms_beta1=float(full[np.argmin(np.abs(BETAS - 1.0))]),
                    P2_worse_frac=float(np.mean(d1 > 0)), d_rms_P2_median=float(np.median(d1)),
                    table={str(b): float(r_) for b, r_ in zip(BETAS[::4], full[::4])})
    P(f"    {f:9s}: best beta = {BETAS[jb]:.2f} (rms {full[jb]:.4f}, Upsilon {SHAPE[f]['U_best']:.2f}); bootstrap 68% "
      f"[{lo68:.2f}, {hi68:.2f}], 95% [{lo95:.2f}, {hi95:.2f}]; beta = 1 (P2) rms {SHAPE[f]['rms_beta1']:.4f}, worse than the "
      f"resample's best in {SHAPE[f]['P2_worse_frac']:.3f} of resamples (median excess {SHAPE[f]['d_rms_P2_median']:+.4f} dex)")
    P("               rms(beta): " + ", ".join(f"{b:.2f}: {r_:.4f}" for b, r_ in zip(BETAS[::6], full[::6])))
h3 = all(SHAPE[f]["ci95"][0] > 1.0 for f in C.FOOTS)
check("H3 (reported; pre-declared UNCERTAIN) the SPARC band on beta lies above beta = 1: the data prefer a sharper transition "
      "than P2, with P2 outside the galaxy-bootstrap 95% band",
      "; ".join(f"{f}: best {SHAPE[f]['best_beta']:.2f}, 95% [{SHAPE[f]['ci95'][0]:.2f}, {SHAPE[f]['ci95'][1]:.2f}]" for f in C.FOOTS),
      h3, load_bearing=False,
      reading="the band is the law's allowed transition sharpness at the framework's a0; the deep limit (y^-1/2, the BTFR's "
              "slope 4) and the Newtonian limit are common to every member and are not what the band measures")
R.num("H3", SHAPE)

# ================================================================================================ H4 scatter budget
banner("H4  THE SCATTER BUDGET: velocity errors per point; distance, inclination and Upsilon coherent per galaxy; ML intrinsic scatter")
SIG_UPS = 0.10                                                        # dex, declared population scatter of Upsilon_[3.6]
LN10 = math.log(10.0)
meta_ok = np.array([g["meta"] is not None for g in GAL])
DD = np.array([g["meta"]["D"] for g in GAL]); EDD = np.array([g["meta"]["eD"] for g in GAL])
INC = np.radians(np.array([g["meta"]["Inc"] for g in GAL])); EINC = np.radians(np.array([g["meta"]["eInc"] for g in GAL]))
sig_gal_const = np.sqrt((EDD / DD / LN10) ** 2 + (2.0 / np.tan(np.clip(INC, 0.05, None)) * EINC / LN10) ** 2)


def budget(kfun, f, sig_ups=SIG_UPS):
    """residuals at the kernel's best Upsilon; per-galaxy covariance diag(sv^2 + s_int^2) + c^2 11^T + (sig_ups u)(sig_ups u)^T,
    u_i = s_i f*_i (s = dlog(nu g)/dlog g, f* the stellar share of V_bar^2); returns the ML s_int, its 95% upper bound and the
    fraction of the observed variance the error model carries."""
    fit = FITS[(f, "P2" if kfun is C.nu_p2 else "nu_mono")]
    iu = fit["iu"]; U = UPS[iu]; a0 = A0[f]
    kf = law(kfun)
    gb = GB[:, iu]; go = GO[:, iu]; ok = OK[:, iu]
    y = gb / a0
    nu_ = kf(y)
    res = np.log10(go) - np.log10(nu_ * gb)
    e_ = 1e-4
    s_ = (np.log(kf(y * (1 + e_)) * (1 + e_)) - np.log(kf(y * (1 - e_)) * (1 - e_))) / (2 * e_)
    fstar = np.clip((U * Vd ** 2 + 1.4 * U * Vb ** 2) / np.maximum(VB2[:, iu], 1e-30), 0.0, 1.0)
    sv = 2.0 / LN10 * np.clip(eV, 1, None) / np.clip(Vo, 1, None)
    blocks = []
    for ig in range(NG):
        m = (GI == ig) & ok
        if m.sum() < 1:
            continue
        blocks.append((res[m], sv[m], sig_gal_const[ig], s_[m] * fstar[m]))

    def m2lnL(s_int, mu, sups):
        tot = 0.0
        for r_, v_, cg, u_ in blocks:
            n = len(r_)
            Cm = np.diag(v_ ** 2 + s_int ** 2) + cg ** 2 * np.ones((n, n)) + (sups ** 2) * np.outer(u_, u_)
            L = np.linalg.cholesky(Cm)
            z = np.linalg.solve(L, r_ - mu)
            tot += z @ z + 2.0 * np.sum(np.log(np.diag(L)))
        return tot

    mu0 = float(np.average(res[ok], weights=WPT[ok]))
    prof = lambda s: minimize_scalar(lambda mu: m2lnL(s, mu, sig_ups), bounds=(mu0 - 0.1, mu0 + 0.1), method="bounded",
                                     options={"xatol": 1e-4}).fun
    grid = np.array([0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.10, 0.12])
    vals = np.array([prof(s) for s in grid])
    j = int(np.argmin(vals))
    if 0 < j < len(grid) - 1:
        rr_ = minimize_scalar(prof, bounds=(grid[j - 1], grid[j + 1]), method="bounded", options={"xatol": 2e-4})
        s_ml, v_ml = float(rr_.x), float(rr_.fun)
    else:
        s_ml, v_ml = float(grid[j]), float(vals[j])
    up = [s for s, v in zip(grid, vals) if s > s_ml and v - v_ml >= 3.84]
    if up:
        k_ = list(grid).index(up[0])
        from scipy.optimize import brentq
        s95 = brentq(lambda s: prof(s) - v_ml - 3.84, grid[k_ - 1] if grid[k_ - 1] > s_ml else s_ml, up[0], xtol=5e-4)
    else:
        s95 = float("inf")
    obs_var = float(np.average((res[ok] - mu0) ** 2, weights=WPT[ok]))
    err_var = float(np.average(sv[ok] ** 2 + sig_gal_const[GI[ok]] ** 2 + (sig_ups * s_[ok] * fstar[ok]) ** 2, weights=WPT[ok]))
    unw = float(np.std(res[ok]))
    return dict(s_int=s_ml, s_int95=float(s95), mu=mu0, obs_rms_w=math.sqrt(obs_var), obs_rms_unw=unw,
                err_rms_w=math.sqrt(err_var), err_frac=err_var / obs_var, n=int(ok.sum()), U=float(U))


BUD = {}
t4 = time.time()
for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        BUD[(f, kn)] = budget(kf, f)
        b_ = BUD[(f, kn)]
        P(f"    {f:9s} {kn:8s}: observed rms {b_['obs_rms_w']:.4f} dex (weighted; unweighted {b_['obs_rms_unw']:.4f}), the error "
          f"model's rms {b_['err_rms_w']:.4f} ({100 * min(b_['err_frac'], 9.99):.0f}% of the variance); ML intrinsic scatter "
          f"{b_['s_int']:.4f} dex, 95% upper bound {b_['s_int95']:.4f} ({b_['n']} points, Upsilon {b_['U']:.2f})")
sens = {s: budget(C.nu_mono, "canonical", s)["s_int"] for s in (0.05, 0.15)}
P(f"    sensitivity (canonical, nu_mono) to the declared Upsilon scatter: 0.05 dex -> s_int {sens[0.05]:.4f}; 0.15 dex -> "
  f"{sens[0.15]:.4f} ({time.time() - t4:.0f} s)")
h4 = all(v["s_int95"] <= 0.06 for v in BUD.values())
check("H4 (reported) THE SCATTER BUDGET: the error model (per-point velocity errors; coherent distance, inclination and 0.10 dex "
      "Upsilon per galaxy) carries most of the observed variance, and the ML per-point intrinsic scatter is <= 0.06 dex at 95% "
      "for both kernels on both footings",
      "; ".join(f"{k[0][:3]}/{k[1]}: s_int {v['s_int']:.3f} (95% <= {v['s_int95']:.3f}), errors {100 * min(v['err_frac'], 9.99):.0f}%"
                for k, v in BUD.items()), h4, load_bearing=False,
      reading="the intrinsic scatter bounds any hidden second parameter of the galaxy law (an environment, a formation history, a "
              "variable a0): at fixed baryons the total field is deterministic to this level")
R.num("H4", {f"{k[0]}|{k[1]}": v for k, v in BUD.items()})
R.num("H4_sensitivity", sens)

# ================================================================================================ H5 BTFR
banner("H5  THE BARYONIC TULLY-FISHER RELATION: slope, normalisation, and the law's own finite-radius prediction")
sel = [i for i, g in enumerate(GAL) if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Vflat"] > 0
       and g["meta"]["eVflat"] / g["meta"]["Vflat"] <= 0.1]
BTF = {}


def btfr_fit(logV, sV, logM, sM, slope=None):
    def nll(p):
        s = slope if slope is not None else p[0]
        b = p[-2]; si = abs(p[-1])
        var = sM ** 2 + (s * sV) ** 2 + si ** 2
        return 0.5 * np.sum((logM - s * logV - b) ** 2 / var + np.log(var))
    x0 = ([4.0] if slope is None else []) + [2.0, 0.05]
    r_ = minimize(nll, x0, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 20000})
    return r_.x, r_.fun


for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        U = FITS[(f, kn)]["U"]
        Mst = np.array([U * GAL[i]["meta"]["L36"] * 1e9 for i in sel])
        Mg = np.array([1.33 * GAL[i]["meta"]["MHI"] * 1e9 for i in sel])
        Mb = Mst + Mg
        V = np.array([GAL[i]["meta"]["Vflat"] for i in sel]); eVf = np.array([GAL[i]["meta"]["eVflat"] for i in sel])
        Dg = np.array([GAL[i]["meta"]["D"] for i in sel]); eDg = np.array([GAL[i]["meta"]["eD"] for i in sel])
        logV, sV = np.log10(V), eVf / V / LN10
        logM = np.log10(Mb)
        sM = np.sqrt((2 * eDg / Dg / LN10) ** 2 + (SIG_UPS * Mst / Mb) ** 2)
        (sl, b_f, si_f), _ = btfr_fit(logV, sV, logM, sM)
        (b4, si4), _ = btfr_fit(logV, sV, logM, sM, slope=4.0)
        A_obs = 10 ** b4                                                  # Msun per (km/s)^4
        A_deep = 1.0 / (C.G_SI * A0[f]) * 1e12 / C.MSUN                  # 1/(G a0) in Msun (km/s)^-4
        # the law's own finite-radius velocity at the outer points, as V_flat is read: the mean over the outermost third
        Vlaw = []
        for i in sel:
            g = GAL[i]
            vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
            rr = g["R"] * KPC_S
            gb = vb2 * 1e6 / rr
            okp = gb > 0
            vl = np.where(okp, np.sqrt(np.maximum(law(kf)(np.where(okp, gb, 1) / A0[f]) * gb * rr, 0)) / 1e3, np.nan)
            n3 = max(3, len(rr) // 3)
            Vlaw.append(np.nanmean(vl[-n3:]) * g["meta"]["Vflat"] / np.nanmean(g["Vobs"][-n3:]) if np.isfinite(np.nanmean(vl[-n3:]))
                        else np.nan)
        Vlaw = np.array(Vlaw)
        mm = np.isfinite(Vlaw) & (Vlaw > 0)
        (b4l, _), _ = btfr_fit(np.log10(Vlaw[mm]), sV[mm], logM[mm], sM[mm], slope=4.0)
        kappa_deep = 1.0 / (C.G_SI * (A_obs * C.MSUN / 1e12)) / KAP_UNIT
        BTF[(f, kn)] = dict(n=len(sel), slope=float(sl), sig_int=float(abs(si_f)), b4=float(b4), A_obs=float(A_obs),
                            A_deep=float(A_deep), d_obs_deep=float(b4 - math.log10(A_deep)), A_law_finite=float(10 ** b4l),
                            d_obs_law=float(b4 - b4l), kappa_deep_reading=float(kappa_deep), U=U)
        P(f"    {f:9s} {kn:8s} (Upsilon {U:.2f}, {len(sel)} galaxies): free slope {sl:.3f} (intrinsic {abs(si_f):.3f} dex); at slope 4: "
          f"A_obs = {A_obs:.1f} Msun/(km/s)^4; deep limit 1/(G a0) = {A_deep:.1f} (obs - deep {b4 - math.log10(A_deep):+.3f} dex); the law's "
          f"own outer velocities give {10 ** b4l:.1f} (obs - law {b4 - b4l:+.3f} dex); kappa read from A_obs as a deep-limit "
          f"normalisation {kappa_deep:.3f}")
h5 = all(3.5 <= v["slope"] <= 4.5 and abs(v["d_obs_law"]) <= 0.10 for v in BTF.values())
check("H5 (reported) THE BTFR: the free slope lies in 3.5-4.5 and, at slope 4, the observed normalisation agrees within 0.10 dex "
      "with the law's own outer-radius prediction on both footings (the deep-limit 1/(G a0) differs by the printed finite-y offset)",
      "; ".join(f"{k[0][:3]}/{k[1]}: slope {v['slope']:.2f}, obs-law {v['d_obs_law']:+.3f}, obs-deep {v['d_obs_deep']:+.3f} dex"
                for k, v in BTF.items()), h5, load_bearing=False,
      reading="the BTFR normalisation is the deep-MOND 1/(G a0) only asymptotically; SPARC's V_flat sits at finite y, so reading "
              "kappa off A_obs as a deep-limit number biases it (the record's 0.465 +- 0.076 is that reading)")
R.num("H5", {f"{k[0]}|{k[1]}": v for k, v in BTF.items()})

# ================================================================================================ H6 rho_eff
banner("H6  THE DARK DENSITY THE LAW IMPLIES: rho_eff = div[(nu - 1) g_bar]/(4 pi G), its surface density and core radius")
yy = np.logspace(-6, 8, 2001)
fP2 = yy * (C.nu_p2(yy) - 1.0)
fRAR = yy * (C.nu_rar(yy) - 1.0)
fMONO = yy * (C.nu_mono(yy) - 1.0)
P(f"    analytic (spherical): Sigma_ph(<r) = y (nu(y) - 1) a0/(pi G) = 2 y (nu - 1) Sigma_M.  sup over y: P2 {2 * fP2.max():.4f} Sigma_M "
  f"(at y = {yy[np.argmax(fP2)]:.0e}, approached as y -> oo); nu_RAR {2 * fRAR.max():.4f} Sigma_M at y = {yy[np.argmax(fRAR)]:.3f} "
  f"(the record's h122: 1.2952); nu_mono {2 * fMONO[yy <= 1e2].max():.3f} at y <= 100, {2 * fMONO[yy <= 1e4].max():.3f} at y <= 1e4, "
  f"{2 * fMONO.max():.3f} at y <= 1e8 (no bound: logarithmic)")
P(f"    at the MOND radius of a point mass (y = 1): P2 {2 * (C.nu_p2(1.0) - 1):.4f} Sigma_M, nu_mono {2 * (C.nu_mono(1.0) - 1):.4f} Sigma_M")
ANA = dict(sup_P2=float(2 * fP2.max()), sup_RAR=float(2 * fRAR.max()), y_sup_RAR=float(yy[np.argmax(fRAR)]),
           mono_1e2=float(2 * fMONO[yy <= 1e2].max()), mono_1e4=float(2 * fMONO[yy <= 1e4].max()), mono_1e8=float(2 * fMONO.max()))


def burkert_M(r, rho0, r0):
    x = r / r0
    return math.pi * rho0 * r0 ** 3 * (np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x))


def piso_M(r, rho0, rc):
    x = r / rc
    return 4 * math.pi * rho0 * rc ** 3 * (x - np.arctan(x))


PHAN = {}
for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("nu_mono", C.nu_mono)):
        U = FITS[(f, kn)]["U"]; a0 = A0[f]
        rows = []
        for i, g in enumerate(GAL):
            if not g["meta"] or g["meta"]["Q"] > 2 or len(g["R"]) < 5:
                continue
            rr = g["R"] * C.KPC
            vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
            gb = vb2 * 1e6 / rr
            m = gb > 0
            if m.sum() < 5:
                continue
            rr, gb = rr[m], gb[m]
            y = gb / a0
            gph = (law(kf)(y) - 1.0) * gb
            Mph = gph * rr ** 2 / C.G_SI / C.MSUN
            Sig = Mph / (math.pi * (rr / C.PC) ** 2) / C.SIGMA_M[f]                  # Sigma_ph(<r) / Sigma_M
            Mb_last = gb[-1] * rr[-1] ** 2 / C.G_SI
            # central column: (1/pi G) Int g_ph dr/r, linear inside the first point, deep-MOND tail outside the last
            I = np.trapz(gph / rr, rr) + gph[0] + math.sqrt(C.G_SI * Mb_last * a0) / rr[-1]
            col = I / (math.pi * C.G_SI) / (C.MSUN / C.PC ** 2) / C.SIGMA_M[f]
            row = dict(name=g["name"], Sig_max=float(np.nanmax(Sig)), col0=float(col), Rdisk=g["meta"]["Rdisk"],
                       rM=math.sqrt(C.G_SI * Mb_last / a0) / C.KPC, y_last=float(y[-1]), y_max=float(y.max()))
            okm = Mph > 0
            if okm.sum() >= 5:
                lr, lM = np.log(rr[okm] / C.KPC), np.log(Mph[okm])
                for nm_, fun in (("bur", burkert_M), ("piso", piso_M)):
                    def resid(p, fun=fun):
                        return np.log(np.maximum(fun(np.exp(lr), 10 ** p[0], 10 ** p[1]), 1e-300)) - lM
                    best_ = None
                    for r0g in (0.5, 2.0, 8.0):
                        for rhog in (6.0, 7.5, 9.0):                    # log10 rho0 [Msun/kpc^3]
                            try:
                                sol = least_squares(resid, [rhog, math.log10(r0g)], method="lm", max_nfev=400)
                            except Exception:
                                continue
                            if best_ is None or sol.cost < best_.cost:
                                best_ = sol
                    rho0, r0 = 10 ** best_.x[0], 10 ** best_.x[1]              # Msun/kpc^3, kpc
                    row[nm_] = dict(rho0=rho0, r0=r0, rho0r0=rho0 * r0 / 1e6,
                                    rms=float(np.sqrt(np.mean(best_.fun ** 2)) / LN10))   # rho0 r0 in Msun/pc^2
            rows.append(row)
        PHAN[(f, kn)] = rows
        smax = np.array([r_["Sig_max"] for r_ in rows]); col = np.array([r_["col0"] for r_ in rows])
        bur = np.array([r_["bur"]["rho0r0"] for r_ in rows if "bur" in r_ and r_["bur"]["rms"] < 0.1])
        pis = np.array([r_["piso"]["rho0r0"] for r_ in rows if "piso" in r_ and r_["piso"]["rms"] < 0.1])
        r0 = np.array([r_["bur"]["r0"] for r_ in rows if "bur" in r_ and r_["bur"]["rms"] < 0.1])
        rd = np.array([r_["Rdisk"] for r_ in rows if "bur" in r_ and r_["bur"]["rms"] < 0.1])
        rM = np.array([r_["rM"] for r_ in rows if "bur" in r_ and r_["bur"]["rms"] < 0.1])
        mrd = rd > 0
        cor_rd = float(np.corrcoef(np.log10(r0[mrd]), np.log10(rd[mrd]))[0, 1]) if mrd.sum() > 5 else float("nan")
        cor_rM = float(np.corrcoef(np.log10(r0), np.log10(rM))[0, 1]) if len(r0) > 5 else float("nan")
        PHAN[(f, kn, "summary")] = dict(
            n=len(rows), Sig_max_median=float(np.median(smax)), Sig_max_p16_p84=[float(np.percentile(smax, 16)), float(np.percentile(smax, 84))],
            frac_above_SigM=float(np.mean(smax > 1.0)), col0_median=float(np.median(col)),
            bur_n=len(bur), bur_log_median=float(np.median(np.log10(bur))), bur_log_std=float(np.std(np.log10(bur))),
            bur_over_SigM_dex=float(np.median(np.log10(bur)) - math.log10(C.SIGMA_M[f])),
            piso_log_median=float(np.median(np.log10(pis))) if len(pis) else float("nan"),
            r0_over_Rdisk_median=float(np.median(r0[mrd] / rd[mrd])) if mrd.sum() else float("nan"),
            r0_over_rM_median=float(np.median(r0 / rM)), corr_r0_Rdisk=cor_rd, corr_r0_rM=cor_rM)
        s_ = PHAN[(f, kn, "summary")]
        P(f"    {f:9s} {kn:8s}: {s_['n']} galaxies (Q <= 2); max_r Sigma_ph(<r)/Sigma_M median {s_['Sig_max_median']:.3f} "
          f"[16-84%: {s_['Sig_max_p16_p84'][0]:.3f}-{s_['Sig_max_p16_p84'][1]:.3f}], above Sigma_M in {100 * s_['frac_above_SigM']:.0f}%; "
          f"central column Sigma_ph(0)/Sigma_M median {s_['col0_median']:.2f}")
        P(f"    {'':19s}  Burkert fit to M_ph(<r) ({s_['bur_n']} galaxies with fit rms < 0.1 dex): log10 rho0 r0 = "
          f"{s_['bur_log_median']:.3f} +- {s_['bur_log_std']:.3f} (Msun/pc^2; Sigma_M = {math.log10(C.SIGMA_M[f]):.3f}, offset "
          f"{s_['bur_over_SigM_dex']:+.3f} dex; Donato+09 2.15 +- 0.2); pISO {s_['piso_log_median']:.3f}; core radius r0 = "
          f"{s_['r0_over_Rdisk_median']:.2f} R_disk (corr {s_['corr_r0_Rdisk']:+.2f}) = {s_['r0_over_rM_median']:.2f} r_M (corr "
          f"{s_['corr_r0_rM']:+.2f})")
sP2c = PHAN[("canonical", "P2", "summary")]; sMc = PHAN[("canonical", "nu_mono", "summary")]
h6 = (abs(ANA["sup_P2"] - 1.0) < 1e-3 and abs(ANA["sup_RAR"] - 1.2952) < 2e-3 and ANA["mono_1e8"] > ANA["mono_1e2"]
      and all(0.4 <= PHAN[(f, k, "summary")]["Sig_max_median"] <= 0.8 for f in C.FOOTS for k in ("P2", "nu_mono"))
      and all(abs(PHAN[(f, k, "summary")]["bur_over_SigM_dex"]) <= 0.3 for f in C.FOOTS for k in ("P2", "nu_mono")))
check("H6 (reported; pre-declared UNCERTAIN) THE SURFACE DENSITY: analytically P2's phantom surface density is bounded by exactly "
      "Sigma_M = a0/(2 pi G) (nu_RAR 1.2952 Sigma_M, nu_mono unbounded); on SPARC each galaxy's largest Sigma_ph(<r) has a median "
      "in 0.4-0.8 Sigma_M, and the phantom's Burkert rho0 r0 lies within 0.3 dex of Sigma_M, on both footings for both kernels",
      f"sup: P2 {ANA['sup_P2']:.4f}, RAR {ANA['sup_RAR']:.4f}, mono(1e2/1e8) {ANA['mono_1e2']:.2f}/{ANA['mono_1e8']:.2f} Sigma_M; "
      + "; ".join(f"{f[:3]}/{k}: Sig_max {PHAN[(f, k, 'summary')]['Sig_max_median']:.2f}, Burkert {PHAN[(f, k, 'summary')]['bur_over_SigM_dex']:+.2f} dex"
                  for f in C.FOOTS for k in ("P2", "nu_mono")), h6, load_bearing=False)
R.num("H6", dict(analytic=ANA, summary={f"{k[0]}|{k[1]}": v for k, v in PHAN.items() if len(k) == 3}))
P("\n    VERDICT on the record's 'halo surface density ~ a0/(2 pi G)' (hunt_2026/WHAT_THE_HUNT_TAUGHT.md item 5; hy4_push/H033):")
P(f"      * as an IDENTITY it holds only as P2's analytic CEILING: Sigma_ph(<r) < Sigma_M for every spherical system, equality as "
  f"y -> oo; for nu_mono (the adopted kernel) there is no ceiling (Sigma_ph(<r) reaches {ANA['mono_1e4']:.2f} Sigma_M at y = 1e4).")
P(f"      * as a MEASUREMENT on SPARC the typical phantom sits BELOW it: median max Sigma_ph(<r) = {sP2c['Sig_max_median']:.2f} "
  f"(P2) / {sMc['Sig_max_median']:.2f} (nu_mono) Sigma_M (canonical); the Burkert product rho0 r0 = 10^{sP2c['bur_log_median']:.2f} "
  f"/ 10^{sMc['bur_log_median']:.2f} Msun/pc^2 vs Sigma_M = {C.SIGMA_M['canonical']:.0f} (canonical) -- a fit-convention number, not "
  f"an identity.")

# ================================================================================================ W ledger
banner("W  THE LEDGER: part 1 (the galaxy law)")
sh = SHAPE["canonical"]; sha = SHAPE["alt"]
R.ledger("G1", "FITTED", f"the galaxy law g = nu(g_bar/a0) g_bar at a0 = kappa c sqrt(G rho_L), kappa = 1/2: SPARC rms "
         f"{FITS[('canonical', 'nu_mono')]['rms']:.4f}/{FITS[('alt', 'nu_mono')]['rms']:.4f} (nu_mono), "
         f"{FITS[('canonical', 'P2')]['rms']:.4f}/{FITS[('alt', 'P2')]['rms']:.4f} (P2) at Upsilon "
         f"{FITS[('canonical', 'nu_mono')]['U']:.2f}/{FITS[('alt', 'nu_mono')]['U']:.2f} and {FITS[('canonical', 'P2')]['U']:.2f}/"
         f"{FITS[('alt', 'P2')]['U']:.2f}", "H2")
R.ledger("G2", "CONSTRAINT", f"transition sharpness beta (nu_beta family) 95%: [{sh['ci95'][0]:.2f}, {sh['ci95'][1]:.2f}] canonical, "
         f"[{sha['ci95'][0]:.2f}, {sha['ci95'][1]:.2f}] alt (P2 = 1)", "H3")
R.ledger("G3", "CONSTRAINT", "intrinsic scatter (per point, ML, 95%): " + ", ".join(f"{k[0][:3]}/{k[1]} <= {v['s_int95']:.3f}"
                                                                                       for k, v in BUD.items()), "H4")
R.ledger("G4", "MEASURED", "BTFR at slope 4: " + ", ".join(f"{k[0][:3]}/{k[1]} A_obs {v['A_obs']:.1f} vs law {v['A_law_finite']:.1f}"
                                                          f" vs 1/(G a0) {v['A_deep']:.1f}" for k, v in BTF.items()), "H5")
R.ledger("G5", "DERIVED", f"phantom surface density ceiling: P2 exactly a0/(2 pi G) (sup {ANA['sup_P2']:.4f}); nu_RAR 1.2952x; "
         f"nu_mono none", "H6")
check("W (reported) the ledger of part 1", f"{len(R.OUT['ledger'])} rows", True, load_bearing=False)
sys.exit(R.finish())
