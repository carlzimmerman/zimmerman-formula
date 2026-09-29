#!/usr/bin/env python3
"""CFG95 -- DOES B'S OWN STELLAR-MASS CALIBRATION ACCOUNT FOR THE KiDS EARLY/LATE SPLIT?  B's colour-blind law, with each lens's TRUE
stellar mass set by B's own dynamical calibrations (early types: CFG33's ATLAS3D alpha_dyn(sigma); discs: SPARC's Upsilon), scored on
the KiDS early/late split in CFG61's seven 1-halo bins (K1), against the released covariance and CFG88's jackknife covariance.

Criteria frozen and committed before any number: campaign_fresh_gravity/CFG95_FROZEN_CRITERIA.md (32abb6e12 as CFG90; renumbered 05a819f04).
  early    true M* = alpha_dyn,foot(sigma) M_Salp; alpha_dyn,foot = 10^(a + b (log sigma - 2.3)), the CFG33 / CFG55-C2 fit of log(M_law/M_Salp)
           on log sigma_e over ATLAS3D qual >= 1 (N = 187), recomputed per footing with CFG55's own law_mass; sigma from an OLS fit of
           log sigma_e on log M_Salp over the same set; M_Salp = 10^0.25 M*_Chabrier (KiDS LePhare masses read as Chabrier).
           delta_early(M*) = log10 alpha_dyn(sigma(M*)) + 0.25.
  late     delta_late = log10(Upsilon_SPARC / 0.5): Upsilon_SPARC = 0.61 canonical / 0.57 alt (CFG4_galaxy_law, nu_mono), 0.5 = SPARC's
           population-synthesis reference; +0.086 / +0.057 dex.
  model    M_b,true = 10^delta M* + M_gas (M_gas = f_cold(M*) M*, CFG61); each lens keeps its measured-mass R for its g_bar bin; the law's
           Delta Sigma at the true M_b interpolated linearly in log M_b between CFG61's profile nodes, plus the true point-mass term.
  data     released: Brouwer+2021 Fig. 8 colour bins, 30x30 covariance, C_D = C_ee + C_ll - C_el - C_le on K1 (CFG61).
           re-measured: the June 2026 re-measurement (lr_esd_jackknife.npz), CFG88's 50-patch jackknife covariance on K1 (Hartlap 41/49).
PRE-DECLARED (from the frozen file)
  C1  CONTROL  delta = 0 reproduces CFG61's committed law stacks (ml, me, canonical) to 1e-9 relative and the released chi2_L = 28.07.
  C2  CONTROL  the canonical alpha_dyn fit reproduces CFG33's committed calibration (slope +0.204; x0.72 / x0.83 / x0.90).
  C3  CONTROL  the log-M_b interpolation of the law's Delta Sigma matches directly computed profiles at three off-node masses to 1%.
  H1  [HEADLINE; MUTATE must fail] with B's own calibration, the law fits the RELEASED split on K1: p > 0.01, both footings.
  H2  the same for the RE-MEASURED split under the jackknife covariance: p > 0.01, both footings.
  R1-R6 (reported): delta(M*); the late-type bracket (delta_late = 0; reference 0.6); Salpeter/Chabrier 0.20 / 0.30; constant alpha;
               chi2 against a uniform differential offset Delta (0-0.5 dex); the absolute per-class profiles on K1.
MUTATE=1: delta_early = delta_late = 0 (B's calibration removed) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG95_kids_split_own_calibration.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG95_kids_split_own_calibration", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: delta_early = delta_late = 0 (B's calibration removed) -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")
SC = 0.25


def lane_prefix(fname, marker):
    """exec a committed lane read-only up to marker, with its own MUTATE forced off."""
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(HERE, fname)).read()
    g = {"__file__": os.path.join(HERE, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(marker)], fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


g61 = lane_prefix("CFG61_kids_colour_split.py", "\nRES = {}\n")
g55 = lane_prefix("CFG55_sluggs_dynamical_masses.py", "\nRES = {}\n")
PROF, LMG, ZG, RG, EDGES, SUB = g61["PROF"], g61["LMG"], g61["ZG"], g61["RG"], g61["EDGES"], g61["SUB"]
weights, stack61, fcold, G_SI, MSUN, MPC = g61["weights"], g61["stack"], g61["fcold"], g61["G_SI"], g61["MSUN"], g61["MPC"]
d_late, d_early, C30, K1, profiles = g61["d_late"], g61["d_early"], g61["C30"], g61["K1"], g61["profiles"]
ET, law_mass, A0SI, ARCSEC = g55["ET"], g55["law_mass"], g55["A0SI"], g55["ARCSEC"]
PK = len(K1)
idx = np.array(K1)

# ------------------------------------------------------------------ B's own calibrations
q = np.array([e["qual"] >= 1 for e in ET])
ls_ = np.array([e["lsig"] for e in ET])
lmsalp = np.array([e["lmlsalp"] + e["lL"] for e in ET])
ALPHA = {}
for foot in FOOTS:
    al = np.array([law_mass(10 ** (e["lmljam"] + e["lL"]), 10 ** e["lr12"] * ARCSEC * e["D"] * 1e3, A0SI[foot]) / 10 ** (e["lmlsalp"] + e["lL"])
                   for e in ET])
    b_, a_ = np.polyfit(ls_[q] - 2.3, np.log10(al[q]), 1)
    ALPHA[foot] = (float(a_), float(b_))
s1, s0 = np.polyfit(lmsalp[q] - 11.0, ls_[q], 1)
sig_scatter = float(np.std(ls_[q] - (s0 + s1 * (lmsalp[q] - 11.0))))
U4 = json.load(open(os.path.join(HERE, "CFG4_galaxy_law_results.json")))["numbers"]["H2"]
UPS = {"canonical": float(U4["canonical|nu_mono"]["U"]), "alt": float(U4["alt|nu_mono"]["U"])}


def delta_early(lm, foot, sc=SC, const_logsig=None):
    lsig = const_logsig if const_logsig is not None else s0 + s1 * (lm + sc - 11.0)
    a_, b_ = ALPHA[foot]
    return a_ + b_ * (lsig - 2.3) + sc


def delta_late(foot, ref=0.5):
    return math.log10(UPS[foot] / ref)


# ------------------------------------------------------------------ the stack with per-lens true masses (interpolated in log M_b)
LOGMB = np.log10(10 ** LMG * (1 + np.array([fcold(lm) for lm in LMG])))
LRG = np.log(RG)
DSL = {(foot, b): np.array([PROF[(foot, "red", lm, z)]["dsL"] for lm in LMG]) for foot in FOOTS for b, z in enumerate(ZG)}
CLAMP = {"n": 0}


def stack_true(cls, foot, dfun):
    """dfun(lm) -> delta (dex) for this class; returns the model Delta Sigma per g_bar bin [Msun/pc^2] (CFG61's stack, true masses)."""
    w = weights(cls)
    out = np.zeros(15)
    fc = np.array([fcold(lm) for lm in LMG])
    dl = np.array([dfun(lm) for lm in LMG])
    lmbt = np.log10(10 ** LMG * (10 ** dl + fc))
    ii = np.clip(np.searchsorted(LOGMB, lmbt, side="right") - 1, 0, len(LMG) - 2)
    tt = (lmbt - LOGMB[ii]) / (LOGMB[ii + 1] - LOGMB[ii])
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            for b in range(len(ZG)):
                if w[a, b] <= 0:
                    continue
                if k == 0 and (tt[a] > 1 or tt[a] < 0):
                    CLAMP["n"] += 1
                t = min(max(tt[a], 0.0), 1.0)
                Mtab = 10 ** LMG[a] * (1 + fc[a])
                Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
                xr = np.log(Rj)
                prof = DSL[(foot, b)]
                dsl = (1 - t) * np.interp(xr, LRG, prof[ii[a]]) + t * np.interp(xr, LRG, prof[ii[a] + 1])
                ds = dsl + 10 ** lmbt[a] / (math.pi * Rj ** 2)
                wj = w[a, b] / gs
                num += float(np.sum(wj * ds)); den += float(np.sum(wj))
        out[k] = num / den / 1e12
    return out


# ------------------------------------------------------------------ the two data sets on K1
Cll, Cee = C30[:15, :15][np.ix_(idx, idx)], C30[15:, 15:][np.ix_(idx, idx)]
Cel, Cle = C30[15:, :15][np.ix_(idx, idx)], C30[:15, 15:][np.ix_(idx, idx)]
CD = Cee + Cll - Cel - Cle
DOBS = (d_early - d_late)[idx]
LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
wgE, W = J["wgE"].astype(float), J["W"].astype(float)
NP = wgE.shape[0]
tg, tw = wgE.sum(0), W.sum(0)
esd = tg / tw / KG
loo = (tg[None] - wgE) / (tw[None] - W) / KG
DREM = (esd[1] - esd[0])[idx]
Dp = loo[:, 1, idx] - loo[:, 0, idx]
Rd = Dp - Dp.mean(0)
CK = (NP - 1) / NP * (Rd.T @ Rd)
HART = (NP - PK - 2) / (NP - 1)


def x2(Dmod, which):
    if which == "released":
        r = DOBS - Dmod
        return float(r @ np.linalg.solve(CD, r))
    r = DREM - Dmod
    return float(r @ np.linalg.solve(CK, r)) * HART


def pv(x):
    return float(CHI2.sf(x, PK))


def zs(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


# ================================================================== C1-C3
R.banner("C1-C3  CONTROLS")
c61 = json.load(open(os.path.join(HERE, "CFG61_kids_colour_split_results.json")))["numbers"]["RES"]["canonical"]
ml0, me0 = stack_true(0, "canonical", lambda lm: 0.0), stack_true(1, "canonical", lambda lm: 0.0)
dev = max(float(np.max(np.abs(ml0 / np.array(c61["ml"]) - 1))), float(np.max(np.abs(me0 / np.array(c61["me"]) - 1))))
x0 = x2((me0 - ml0)[idx], "released")
check("C1 CONTROL: delta = 0 reproduces CFG61's committed law stacks (ml, me, canonical) to 1e-9 and the released chi2_L = 28.07",
      f"max relative deviation {dev:.1e}; released chi2 {x0:.4f} (CFG61 {c61['chi2L']:.4f})", dev < 1e-9 and abs(x0 - c61["chi2L"]) < 1e-6)
a_c, b_c = ALPHA["canonical"]
at = [10 ** (a_c + b_c * (math.log10(s) - 2.3)) for s in (100, 200, 300)]
check("C2 CONTROL: the canonical alpha_dyn fit reproduces CFG33's committed calibration (slope +0.204; x0.72 / x0.83 / x0.90)",
      f"slope {b_c:+.3f}; alpha at 100 / 200 / 300 km/s x{at[0]:.2f} / x{at[1]:.2f} / x{at[2]:.2f} (N = {int(q.sum())}); alt: a {ALPHA['alt'][0]:+.3f}, "
      f"b {ALPHA['alt'][1]:+.3f}; sigma(M_Salp): log sigma = {s0:.3f} + {s1:.3f} (log M_Salp - 11), scatter {sig_scatter:.3f} dex",
      round(b_c, 3) == 0.204 and [round(x, 2) for x in at] == [0.72, 0.83, 0.90])
gc = np.sqrt(EDGES[1:] * EDGES[:-1])
c3 = []
for lm in (10.325, 10.775, 11.125):
    pr = profiles(lm, ZG[2], "canonical", "red")
    lmb = math.log10(pr["Mb"])
    i = int(np.clip(np.searchsorted(LOGMB, lmb, side="right") - 1, 0, len(LMG) - 2))
    t = (lmb - LOGMB[i]) / (LOGMB[i + 1] - LOGMB[i])
    Rk = np.sqrt(G_SI * pr["Mb"] * MSUN / gc[idx]) / MPC
    direct = np.interp(np.log(Rk), LRG, pr["dsL"]) + pr["Mb"] / (math.pi * Rk ** 2)
    prof = DSL[("canonical", 2)]
    interp = (1 - t) * np.interp(np.log(Rk), LRG, prof[i]) + t * np.interp(np.log(Rk), LRG, prof[i + 1]) + pr["Mb"] / (math.pi * Rk ** 2)
    c3.append(float(np.max(np.abs(interp / direct - 1))))
check("C3 CONTROL: the log-M_b interpolation of the law's Delta Sigma (plus point mass) matches directly computed profiles at three off-node masses to 1%",
      f"max relative deviations at log M* 10.325 / 10.775 / 11.125 (z = 0.25, K1 radii): {', '.join(f'{x:.1e}' for x in c3)}", max(c3) < 0.01)

# ================================================================== H1 / H2
R.banner("H1 / H2  B's LAW WITH B's OWN STELLAR-MASS CALIBRATION")
RES = {}
for foot in FOOTS:
    fe = (lambda lm: 0.0) if MUTATE else (lambda lm, f=foot: delta_early(lm, f))
    fl = (lambda lm: 0.0) if MUTATE else (lambda lm, f=foot: delta_late(f))
    ml, me = stack_true(0, foot, fl), stack_true(1, foot, fe)
    Dm = (me - ml)[idx]
    RES[foot] = dict(ml=ml, me=me, D=Dm, rel=x2(Dm, "released"), rem=x2(Dm, "remeasured"))
w_e = weights(1).sum(1)
de_grid = np.array([delta_early(lm, "canonical") for lm in LMG])
de_mean = float(np.sum(w_e * de_grid) / np.sum(w_e))
P(f"  early-class delta (canonical), M_gal-weighted mean {de_mean:+.3f} dex; late delta {delta_late('canonical'):+.3f} (alt {delta_late('alt'):+.3f}); "
  f"differential {de_mean - delta_late('canonical'):+.3f} dex; clamped lens-grid nodes {CLAMP['n']}")
for foot in FOOTS:
    v = RES[foot]
    P(f"    {foot:9s}: model early-late on K1 {np.round(v['D'], 2).tolist()}")
P(f"    data (released):     {np.round(DOBS, 2).tolist()}\n    data (re-measured):  {np.round(DREM, 2).tolist()}")
check("H1 [HEADLINE] WITH B's OWN CALIBRATION, B's LAW FITS THE RELEASED SPLIT ON K1: p > 0.01, both footings"
      + ("  [MUTATE: calibration removed]" if MUTATE else ""),
      "; ".join(f"{f}: chi2 {RES[f]['rel']:.2f}/7, p {pv(RES[f]['rel']):.2e} ({zs(pv(RES[f]['rel'])):.2f} sigma)" for f in FOOTS)
      + f"  [no calibration: 28.07/7, p 2.1e-4]", all(pv(RES[f]["rel"]) > 0.01 for f in FOOTS))
check("H2 THE SAME FOR THE RE-MEASURED SPLIT UNDER THE JACKKNIFE COVARIANCE: p > 0.01, both footings",
      "; ".join(f"{f}: chi2 {RES[f]['rem']:.2f}/7, p {pv(RES[f]['rem']):.2e} ({zs(pv(RES[f]['rem'])):.2f} sigma)" for f in FOOTS)
      + "  [no calibration (CFG88): 35.04/7, p 1.1e-5]", all(pv(RES[f]["rem"]) > 0.01 for f in FOOTS))

# ================================================================== reported rows (canonical unless stated)
R.banner("REPORTED ROWS (canonical unless stated)")
lm_show = [9.5, 10.0, 10.5, 11.0, 11.5]
check("R1 (reported) delta(M*) per class: early = log10 alpha_dyn(sigma(M*)) + 0.25, late = log10(Upsilon_SPARC/0.5)",
      "early " + ", ".join(f"logM* {lm}: {delta_early(lm, 'canonical'):+.3f} (sigma {10 ** (s0 + s1 * (lm + SC - 11)):.0f} km/s)" for lm in lm_show)
      + f"; late {delta_late('canonical'):+.3f}; M_gal-weighted early mean {de_mean:+.3f}", True, load_bearing=False)


def run_variant(fe, fl, foot="canonical"):
    ml, me = stack_true(0, foot, fl), stack_true(1, foot, fe)
    Dm = (me - ml)[idx]
    return x2(Dm, "released"), x2(Dm, "remeasured")


v0 = run_variant(lambda lm: delta_early(lm, "canonical"), lambda lm: 0.0)
v6 = run_variant(lambda lm: delta_early(lm, "canonical"), lambda lm: delta_late("canonical", 0.6))
check("R2 (reported) the late-type bracket: delta_late = 0 (discs at catalogue mass); reference Upsilon_3.6 = 0.6",
      f"delta_late 0: released {v0[0]:.2f} (p {pv(v0[0]):.2e}), re-measured {v0[1]:.2f} (p {pv(v0[1]):.2e}); "
      f"ref 0.6 (delta_late {delta_late('canonical', 0.6):+.3f}): released {v6[0]:.2f} (p {pv(v6[0]):.2e}), re-measured {v6[1]:.2f} (p {pv(v6[1]):.2e})",
      True, load_bearing=False)
r3 = {sc: run_variant(lambda lm, s=sc: delta_early(lm, "canonical", sc=s), lambda lm: delta_late("canonical")) for sc in (0.20, 0.30)}
check("R3 (reported) the Salpeter/Chabrier offset at 0.20 and 0.30 dex",
      "; ".join(f"{sc:.2f}: released {r3[sc][0]:.2f} (p {pv(r3[sc][0]):.2e}), re-measured {r3[sc][1]:.2f} (p {pv(r3[sc][1]):.2e})" for sc in (0.20, 0.30)),
      True, load_bearing=False)
lsig_e = s0 + s1 * (np.array(LMG) + SC - 11.0)
med_lsig = float(np.interp(0.5, np.cumsum(w_e[np.argsort(lsig_e)]) / np.sum(w_e), np.sort(lsig_e)))
r4 = run_variant(lambda lm: delta_early(lm, "canonical", const_logsig=med_lsig), lambda lm: delta_late("canonical"))
check("R4 (reported) constant alpha at the early class's M_gal-weighted median sigma (no sigma-slope)",
      f"median sigma {10 ** med_lsig:.0f} km/s (alpha {10 ** (a_c + b_c * (med_lsig - 2.3)):.3f}): released {r4[0]:.2f} (p {pv(r4[0]):.2e}), "
      f"re-measured {r4[1]:.2f} (p {pv(r4[1]):.2e})", True, load_bearing=False)
DG = np.round(np.arange(0.0, 0.5001, 0.025), 3)
prof5 = {Dv: run_variant(lambda lm, d=Dv: d, lambda lm: 0.0) for Dv in DG}
ok3 = [Dv for Dv in DG if pv(prof5[Dv][0]) > 0.0027]
ok5 = [Dv for Dv in DG if pv(prof5[Dv][0]) > 0.05]
okr3 = [Dv for Dv in DG if pv(prof5[Dv][1]) > 0.0027]
okr5 = [Dv for Dv in DG if pv(prof5[Dv][1]) > 0.05]
rng = lambda L: f"{min(L):.3f}-{max(L):.3f}" if L else "none"
check("R5 (reported) chi2 against a uniform differential offset Delta = delta_early - delta_late (0-0.5 dex; a diagnostic, not a fit)",
      "released: " + ", ".join(f"{Dv:g}: {prof5[Dv][0]:.1f}" for Dv in DG[::2]) + f" | p > 0.0027 for Delta {rng(ok3)}, p > 0.05 for {rng(ok5)}; "
      "re-measured: " + ", ".join(f"{Dv:g}: {prof5[Dv][1]:.1f}" for Dv in DG[::2]) + f" | p > 0.0027 for {rng(okr3)}, p > 0.05 for {rng(okr5)}",
      True, load_bearing=False)
c = RES["canonical"]
ce = float(((d_early - c["me"])[idx]) @ np.linalg.solve(Cee, (d_early - c["me"])[idx]))
cl = float(((d_late - c["ml"])[idx]) @ np.linalg.solve(Cll, (d_late - c["ml"])[idx]))
check("R6 (reported) the absolute per-class profiles on K1 with B's calibration (released per-class blocks)",
      f"early {ce:.1f}/7, late {cl:.1f}/7  [CFG61 without calibration: early 51.9, late 12.6]", True, load_bearing=False)

h1 = all(pv(RES[f]["rel"]) > 0.01 for f in FOOTS)
h2 = all(pv(RES[f]["rem"]) > 0.01 for f in FOOTS)
if h1 and h2:
    reading = "B's own stellar-mass calibrations account for the KiDS split, with no new constant"
elif h1 or h2:
    reading = "B's own calibration accounts for the split on one data set only"
else:
    reading = "the split survives B's own stellar-mass calibration"
P(f"\n    READING (declared): {reading}; conditional on the Salpeter/Chabrier offset, the SPARC reference Upsilon and the LePhare-Chabrier "
  "reading of the KiDS masses (R2, R3)")
R.num("alpha", {f: dict(a=v[0], b=v[1]) for f, v in ALPHA.items()}); R.num("sigma_fit", dict(s0=float(s0), s1=float(s1), scatter=sig_scatter))
R.num("Upsilon", UPS); R.num("delta_early_mean", de_mean)
R.num("H", {f: dict(released=RES[f]["rel"], remeasured=RES[f]["rem"], D=RES[f]["D"].tolist()) for f in FOOTS})
R.num("R2", dict(late0=v0, ref06=v6)); R.num("R3", {str(k): v for k, v in r3.items()}); R.num("R4", r4)
R.num("R5", {str(k): v for k, v in prof5.items()}); R.num("R6", dict(early=ce, late=cl)); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
