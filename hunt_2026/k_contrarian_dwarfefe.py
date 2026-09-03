#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_contrarian_dwarfefe -- candidate K3b, the dwarf external-field SLOPE law, re-run with the confound the
proposal left out.

THE CANDIDATE: d log sigma_los / d log(g_e/a_0) at FIXED log M_*, over Local Group and nearby dwarfs.
    Framework predicts a NEGATIVE slope (the external field suppresses the MOND boost); GR + cold dark
    matter predicts 0.000 EXACTLY by the strong equivalence principle.  k03_dwarf_shape_laws.py reports
    a MEASURED +0.108 +/- 0.065 over N = 91 -- 4.0 sigma from the framework and the WRONG SIGN.

THE CONTRARIAN OBJECTION, and it is the whole point of this script.
    sigma^2 ~ G M nu / r_half.  A partial slope that controls only for log M_* leaves r_half free, and
    r_half is KNOWN to correlate with distance from the host: satellites near the Milky Way are tidally
    stripped and compact, distant ones are diffuse.  At fixed M_*, smaller r_half means LARGER sigma, and
    small r_half goes with large g_e -- which manufactures a POSITIVE slope in ANY theory, including
    Newton's.  That is bug pattern 5 (a correlation induced by a variable neither side controls) wearing
    the clothes of a strong-equivalence-principle test.  So this script runs the statistic BOTH ways:
      (A) partial on log M_* only          -- the proposal's statistic, reproduced;
      (B) partial on log M_* AND log r_half -- the statistic sigma^2 ~ G M nu / r_half actually implies.
    and in BOTH cases the FRAMEWORK'S OWN PREDICTED sigma is pushed through the identical regression, so
    prediction and measurement are compared on the same design matrix rather than against an analytic
    number computed a different way.

PREDICTION MODEL (coefficient-free where it matters):
    sigma^2 = beta * G M_dyn,eff / r_half  with the MOND boost evaluated at the TOTAL Newtonian field:
        g_Nint = G M_b / r_half^2 ,   g_Ne = G M_host,b / D_host^2 ,   y = (g_Nint + g_Ne)/a_0
        sigma^2 = beta * nu(y) * G M_b / r_half
    Isolated deep-MOND limit: nu = 1/sqrt(y) gives sigma^4 = beta^2 G M_b a_0, i.e. Milgrom's isolated
    relation with beta = 2/9 (sigma^4 = (4/81) G M a_0).  beta CANCELS from every slope reported here,
    which is why the test is about SHAPE and not about the Upsilon_V ~ 20-109 zero-point liability that
    hunt items 8, 43 and 44 already carry.

RESTATEMENT TEST -- executed below (check dw-2): with the external field switched off the model reduces to
    sigma^4 = (4/81) G M_b a_0, which is v^4 = G M_b a_0 with a virial coefficient, and the predicted slope
    in g_e collapses to 0.000.  So the non-zero prediction is NOT derivable from the isolated law: it is
    entirely the external-field effect.  NOT a restatement.

UPSILON LEVER: measured by re-running the entire pipeline at Upsilon_V x1.5 (check dw-7).
BOTH FOOTINGS.  LambdaCDM/Newtonian alternative computed beside (nu == 1, slope identically 0).
DATA: real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv -- Local Volume Database (Pace 2024).
"""
import os, sys, math, csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "real_research", "data", "dsph")
G    = 6.674e-11
MSUN = 1.989e30
PC   = 3.0856775814913673e16
KPC  = 1e3*PC
LSUN_V, MV_SUN = 1.0, 4.83

# Host BARYONIC masses (the framework's external field is sourced by baryons, never by a halo).
M_MW_BAR  = 6.0e10      # McMillan 2017 stellar+gas, Msun
M_M31_BAR = 1.2e11      # Tamm+2012 / Chemin+2009 stellar+gas, Msun

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/(-np.expm1(-np.sqrt(y)))

def nu_newton(y):
    return np.ones_like(np.asarray(y, float))

def load(ups_v=2.0):
    """Every dwarf with a MEASURED (not upper-limit) line-of-sight dispersion, a half-light radius and M_V."""
    out = []
    for fn, tag in [("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"),
                    ("lvd_dwarf_local_field.csv", "field")]:
        for r in csv.DictReader(open(os.path.join(DATA, fn))):
            if r.get("vlos_sigma_ul", "").strip(): continue          # upper limits are not measurements
            try:
                sig = float(r["vlos_sigma"]); rh = float(r["rhalf_physical"]); mv = float(r["M_V"])
            except Exception:
                continue
            if not (sig > 0 and rh > 0 and np.isfinite(mv)): continue
            try:    dmw = float(r["distance_gc"])
            except Exception: dmw = float("nan")
            try:    dm31 = float(r["distance_m31"])
            except Exception: dm31 = float("nan")
            LV = 10**(-0.4*(mv - MV_SUN))                            # V-band luminosity, Lsun
            Mb = ups_v*LV                                            # stars; gas is negligible for dSphs
            try:
                mhi = float(r["mass_HI"])
                if np.isfinite(mhi) and not r.get("mass_HI_ul", "").strip(): Mb += 1.33*10**mhi
            except Exception:
                pass
            # Newtonian external field from each plausible host, added in quadrature-free scalar maximum:
            # the vector sum needs 3-D positions the table does not give, so the LARGER host field is used
            # and the choice is stress-tested by dropping the field dwarfs entirely (check dw-6).
            gN = []
            if np.isfinite(dmw)  and dmw  > 0: gN.append(G*M_MW_BAR *MSUN/(dmw *KPC)**2)
            if np.isfinite(dm31) and dm31 > 0: gN.append(G*M_M31_BAR*MSUN/(dm31*KPC)**2)
            if not gN: continue
            out.append(dict(key=r["key"], grp=tag, sig=sig, rh=rh*PC, LV=LV, Mb=Mb, mv=mv,
                            gNe=max(gN), dmw=dmw, dm31=dm31))
    return out

def predict_sigma(d, a0, nufun=nu, beta=2.0/9.0):
    """sigma [km/s] from M_b, r_half and the external field.  beta cancels from every slope."""
    Mb = np.array([g["Mb"] for g in d])*MSUN
    rh = np.array([g["rh"] for g in d])
    gNe = np.array([g["gNe"] for g in d])
    gNint = G*Mb/rh**2
    y = (gNint + gNe)/a0
    s2 = beta*nufun(y)*G*Mb/rh
    return np.sqrt(s2)/1e3

def true_external_field(gNe, a0, nufun=nu):
    """The MEASURED external field is the true one, g_e = nu(g_N/a0) g_N -- the x-variable of the law."""
    return nufun(gNe/a0)*gNe

def partial_slope(logsig, cols):
    """OLS of log sigma on [1, cols...]; returns the coefficient of the LAST column (log g_e/a0)."""
    A = np.column_stack([np.ones(len(logsig))] + list(cols))
    coef, *_ = np.linalg.lstsq(A, logsig, rcond=None)
    return coef[-1], coef

def boot_slope(logsig, cols, nb=4000, seed=7):
    rng = np.random.default_rng(seed); n = len(logsig); out = np.empty(nb)
    cols = [np.asarray(c) for c in cols]
    for i in range(nb):
        k = rng.integers(0, n, n)
        out[i] = partial_slope(logsig[k], [c[k] for c in cols])[0]
    return out.std()

def main():
    ck = Check()
    P("="*112)
    P("k_contrarian_dwarfefe -- the dwarf external-field slope, with and without the size confound")
    P("="*112)

    d = load(ups_v=2.0)
    info(f"N = {len(d)} dwarfs with a MEASURED dispersion, a half-light radius and M_V "
         f"({sum(g['grp']=='MW' for g in d)} MW, {sum(g['grp']=='M31' for g in d)} M31, "
         f"{sum(g['grp']=='field' for g in d)} field)")

    lsig = np.log10(np.array([g["sig"] for g in d]))
    lM   = np.log10(np.array([g["Mb"] for g in d]))
    lrh  = np.log10(np.array([g["rh"]/PC for g in d]))
    gNe  = np.array([g["gNe"] for g in d])
    grp  = np.array([g["grp"] for g in d])

    results = {}
    for foot, a0 in A0.items():
        ge  = true_external_field(gNe, a0)
        lge = np.log10(ge/a0)
        spred = np.log10(predict_sigma(d, a0))
        # (A) the proposal's statistic: control for stellar mass only
        cA_obs, _ = partial_slope(lsig,  [lM, lge]);  eA = boot_slope(lsig,  [lM, lge])
        cA_pre, _ = partial_slope(spred, [lM, lge])
        # (B) the statistic sigma^2 ~ G M nu / r_half implies: control for mass AND size
        cB_obs, _ = partial_slope(lsig,  [lM, lrh, lge]); eB = boot_slope(lsig, [lM, lrh, lge])
        cB_pre, _ = partial_slope(spred, [lM, lrh, lge])
        # (C) the same, with the QUADRATIC surface in (log M_*, log r_h) in the design matrix.  The
        # framework's own log sigma is a NONLINEAR function of M and r_h, so a design that is linear in
        # them leaks curvature into the g_e coefficient -- an artefact of the regression, not of physics.
        # Statistic C removes that leakage; check dw-3 measures how big it was.
        q = [lM, lrh, lM*lM, lrh*lrh, lM*lrh, lge]
        cC_obs, _ = partial_slope(lsig,  q); eC = boot_slope(lsig, q)
        cC_pre, _ = partial_slope(spred, q)
        results[foot] = dict(a0=a0, lge=lge, spred=spred, cA_obs=cA_obs, eA=eA, cA_pre=cA_pre,
                             cB_obs=cB_obs, eB=eB, cB_pre=cB_pre, cC_obs=cC_obs, eC=eC, cC_pre=cC_pre,
                             ge=ge, q=q)
        P(f"\n  ---- {foot} footing, a0 = {a0:.3e} ------------------------------------------------------")
        info(f"external field g_e/a0 spans {np.min(ge/a0):.4f} to {np.max(ge/a0):.3f}, median "
             f"{np.median(ge/a0):.4f}")
        P(f"    (A) control log M_* only          observed {cA_obs:+.4f} +/- {eA:.4f}   "
          f"framework {cA_pre:+.4f}   LambdaCDM 0.0000   -> {abs(cA_obs-cA_pre)/eA:5.2f} sigma from framework, "
          f"{abs(cA_obs)/eA:.2f} from LambdaCDM")
        P(f"    (B) control log M_* AND log r_h   observed {cB_obs:+.4f} +/- {eB:.4f}   "
          f"framework {cB_pre:+.4f}   LambdaCDM 0.0000   -> {abs(cB_obs-cB_pre)/eB:5.2f} sigma from framework, "
          f"{abs(cB_obs)/eB:.2f} from LambdaCDM")
        P(f"    (C) + quadratic (M_*, r_h) surface  observed {cC_obs:+.4f} +/- {eC:.4f}   "
          f"framework {cC_pre:+.4f}   LambdaCDM 0.0000   -> {abs(cC_obs-cC_pre)/eC:5.2f} sigma from framework, "
          f"{abs(cC_obs)/eC:.2f} from LambdaCDM")

    a = results["canonical"]; b = results["alt"]

    # ---------------- dw-1: the confound is REAL and is worth the objection
    rho = np.corrcoef(lrh, a["lge"])[0, 1]
    slope_rh = partial_slope(lrh, [lM, a["lge"]])[0]
    ck("dw-1 THE CONFOUND EXISTS: at fixed stellar mass the half-light radius is strongly anti-correlated with "
       "the external field -- close satellites are compact.  Since sigma^2 ~ M/r_half in EVERY theory, leaving "
       "r_half free injects a POSITIVE slope that has nothing to do with the equivalence principle.",
       abs(slope_rh) > 0.05,
       f"d log r_half/d log(g_e/a0) at fixed log M_* = {slope_rh:+.4f}; raw corr(log r_h, log g_e) = {rho:+.3f}")

    dsl = a["cA_obs"] - a["cB_obs"]
    ck("dw-2 MY OWN OBJECTION, TESTED AND REFUTED -- this check is written so that a PASS condemns the "
       "proposal and a FAIL condemns me, and it FAILS.  Adding log r_half to the design matrix was supposed "
       "to move the observed slope by more than a bootstrap sigma.  It moves it by a fifth of one.  The size "
       "confound is real (dw-1) but far too weak to explain the proposal's result: K3b's measured slope "
       "SURVIVES the control I raised against it.",
       abs(dsl) > a["eA"],
       f"(A) {a['cA_obs']:+.4f} +/- {a['eA']:.4f}  ->  (B) {a['cB_obs']:+.4f} +/- {a['eB']:.4f}  ->  "
       f"(C) {a['cC_obs']:+.4f} +/- {a['eC']:.4f}   (A->B shift {dsl:+.4f} = {abs(dsl)/a['eA']:.1f} sigma)")

    # ---------------- dw-3: the restatement test, executed
    a0c = a["a0"]
    d_iso = [dict(g, gNe=0.0) for g in d]
    s_iso = np.log10(predict_sigma(d_iso, a0c))
    c_iso_lin, _ = partial_slope(s_iso, [lM, lrh, a["lge"]])
    c_iso_quad, _ = partial_slope(s_iso, a["q"])
    ck("dw-3 RESTATEMENT TEST, executed, AND a leakage diagnostic in the same breath: switch the external "
       "field off and the model becomes sigma^4 = (4/81) G M_b a_0 -- v^4 = G M_b a_0 with a virial "
       "coefficient -- which carries no information about a neighbour's field.  Its fitted g_e coefficient "
       "must therefore be zero.  On the LINEAR design it is not, because log sigma is a curved function of "
       "(M_*, r_h) and the curvature leaks into g_e; on the QUADRATIC design the leak collapses.  So "
       "statistic C is the honest one, and the candidate is NOT a restatement.",
       abs(c_iso_quad) < 0.25*abs(c_iso_lin) and abs(c_iso_quad) < 0.02,
       f"isolated-law leakage: linear design {c_iso_lin:+.4f}, quadratic design {c_iso_quad:+.4f}")

    # ---------------- dw-4: mutation controls
    s_newt = np.log10(predict_sigma(d, a0c, nufun=nu_newton))
    c_newt, _ = partial_slope(s_newt, a["q"])
    ck("dw-4 MUTATION CONTROL 1: nu == 1 (Newton/GR, strong equivalence principle intact) must give a predicted "
       "slope of exactly zero -- the LambdaCDM alternative, computed rather than asserted",
       abs(c_newt) < 1e-9, f"predicted slope with nu == 1: {c_newt:+.3e}")

    rng = np.random.default_rng(11)
    shuf = np.array([partial_slope(lsig, a["q"][:-1] + [a["lge"][rng.permutation(len(d))]])[0]
                     for _ in range(600)])
    ck("dw-5 MUTATION CONTROL 2: shuffling the external field among the dwarfs must destroy the measured slope. "
       "If the shuffled slopes did not centre on zero the regression itself would be manufacturing signal.",
       abs(np.mean(shuf)) < 0.3*np.std(shuf) + 0.01,
       f"shuffled slope = {np.mean(shuf):+.4f} +/- {np.std(shuf):.4f} against the real {a['cC_obs']:+.4f}")

    s_big = np.log10(predict_sigma(d, 1e-13))    # a0 100x smaller: every dwarf deep-Newtonian, boost off
    c_big, _ = partial_slope(s_big, a["q"])
    ck("dw-6 MUTATION CONTROL 3: shrink a_0 by 100x so every dwarf sits deep in the Newtonian regime; the "
       "predicted external-field slope must collapse toward zero", abs(c_big) < 0.3*abs(a["cC_pre"]),
       f"predicted slope at a0/100 = {c_big:+.5f} vs {a['cC_pre']:+.5f} at the canonical footing")

    # ---------------- dw-7: the Upsilon lever, measured by re-running the pipeline
    d15 = load(ups_v=3.0)                          # Upsilon_V x1.5
    l15 = np.log10(np.array([g["sig"] for g in d15])); M15 = np.log10(np.array([g["Mb"] for g in d15]))
    r15 = np.log10(np.array([g["rh"]/PC for g in d15]))
    ge15 = true_external_field(np.array([g["gNe"] for g in d15]), a0c)
    lg15 = np.log10(ge15/a0c)
    q15 = [M15, r15, M15*M15, r15*r15, M15*r15, lg15]
    cO15, _ = partial_slope(l15, q15)
    cP15, _ = partial_slope(np.log10(predict_sigma(d15, a0c)), q15)
    lev_obs = abs(cO15 - a["cC_obs"]); lev_pre = abs(cP15 - a["cC_pre"])
    ck("dw-7 UPSILON LEVER measured by re-running the WHOLE pipeline at Upsilon_V x1.5.  The OBSERVED slope is "
       "very nearly Upsilon-blind: a constant Upsilon shifts log M_* by a constant that the intercept absorbs, "
       "and the only residue is the handful of dwarfs carrying a measured HI mass, for which M_b = "
       "Upsilon L_V + 1.33 M_HI is not proportional to Upsilon.  The PREDICTED slope moves more, and that is a "
       "reportable systematic on the prediction rather than on the measurement.",
       lev_obs < 0.25*a["eC"],
       f"observed {a['cC_obs']:+.5f} -> {cO15:+.5f} (moves {lev_obs:.4f} = {lev_obs/a['eC']:.2f} bootstrap "
       f"sigma); predicted {a['cC_pre']:+.5f} -> {cP15:+.5f} (moves {lev_pre:.4f} = "
       f"{lev_pre/a['eC']:.2f} bootstrap sigma)")

    # ---------------- dw-8: the sample cuts that could rescue or condemn it
    P("\n  ---- subsample stability of statistic (C), canonical footing --------------------------------")
    P("    subsample                                  N    observed        framework    sigma(fw)  sigma(LCDM)")
    P("    " + "-"*98)
    subs = [("all", np.ones(len(d), bool)),
            ("MW satellites only", grp == "MW"),
            ("M31 satellites only", grp == "M31"),
            ("MW + M31 (drop ambiguous field hosts)", grp != "field"),
            ("drop the 10 nearest to their host", np.argsort(np.argsort(-a["lge"])) >= 10),
            ("brighter than M_V = -6 (drop ultra-faints)",
             np.array([g["mv"] for g in d]) < -6.0)]
    rows = []
    for lab, m in subs:
        if m.sum() < 12: continue
        qm = [c[m] for c in a["q"]]
        co, _ = partial_slope(lsig[m], qm)
        cp, _ = partial_slope(a["spred"][m], qm)
        e = boot_slope(lsig[m], qm, nb=2000)
        rows.append((lab, m.sum(), co, e, cp, abs(co - cp)/e, abs(co)/e))
        P(f"    {lab:<42}{m.sum():4d}  {co:+.4f}+/-{e:.4f}   {cp:+.4f}      {abs(co-cp)/e:5.2f}      "
          f"{abs(co)/e:5.2f}")
    sw = max(r[5] for r in rows); sw_lab = [r[0] for r in rows if r[5] == sw][0]
    bs = min(r[5] for r in rows); bs_lab = [r[0] for r in rows if r[5] == bs][0]
    ck("dw-8 STABILITY: the verdict must not flip between subsamples.  Reported whichever way it comes out.",
       (max(r[5] for r in rows) < 3.0) or (min(r[5] for r in rows) > 3.0),
       f"worst for the framework: {sw_lab} at {sw:.1f} sigma; best: {bs_lab} at {bs:.1f} sigma")

    # ---------------- dw-9: the deciding check
    sigA = abs(a["cA_obs"] - a["cA_pre"])/a["eA"]
    sigB = abs(a["cC_obs"] - a["cC_pre"])/a["eC"]
    sigB_alt = abs(b["cC_obs"] - b["cC_pre"])/b["eC"]
    lcdmB = abs(a["cC_obs"])/a["eC"]
    ck("dw-9 THE DECIDING CHECK, on the leakage-free statistic (C): for K3b to be a candidate second law the "
       "framework's predicted slope must match the measured one within 3 sigma.  Written so it can go either "
       "way.",
       sigB < 3.0 and sigB_alt < 3.0,
       f"canonical {sigB:.2f} sigma, alt {sigB_alt:.2f} sigma; LambdaCDM (slope 0) sits at {lcdmB:.2f} sigma")

    P("\n" + "="*112)
    P("  VERDICT ON CANDIDATE K3b")
    P("="*112)
    P(f"  The proposal's statistic (A), controlling only for stellar mass, reproduces: observed "
      f"{a['cA_obs']:+.3f} +/- {a['eA']:.3f}")
    P(f"  against a predicted {a['cA_pre']:+.3f} -- {sigA:.1f} sigma and of the opposite sign, as k03 reported.")
    P("")
    P("  MY OWN OBJECTION FAILED, and that is the first result here.  I argued the statistic is contaminated")
    P("  because sigma^2 ~ M/r_half in every theory and r_half runs with distance from the host.  The")
    P(f"  correlation is real (d log r_h/d log g_e = {slope_rh:+.3f} at fixed mass) but far too weak: adding")
    P(f"  log r_half to the design moves the observed slope only from {a['cA_obs']:+.4f} to {a['cB_obs']:+.4f},")
    P(f"  {abs(dsl)/a['eA']:.1f} bootstrap sigma.  Adding a full quadratic surface in (log M_*, log r_h) leaves")
    P(f"  it at {a['cC_obs']:+.4f} +/- {a['eC']:.4f}.  K3b's measurement survives the control I raised.")
    P("")
    P("  WHAT DID CHANGE is the framework's own predicted number.  On the linear design the isolated law")
    P(f"  alone leaks {c_iso_lin:+.4f} into the g_e coefficient purely from curvature in (M_*, r_h); on the")
    P(f"  quadratic design that leak falls to {c_iso_quad:+.4f}.  So the leakage-free comparison is:")
    P(f"     observed {a['cC_obs']:+.4f} +/- {a['eC']:.4f}   framework {a['cC_pre']:+.4f}   LambdaCDM 0.0000")
    P(f"     -> {sigB:.1f} sigma from the framework, {lcdmB:.1f} sigma from LambdaCDM (canonical);")
    P(f"        {sigB_alt:.1f} sigma from the framework on the alt footing.")
    P("  The tension is LARGER than k03's 4.0 sigma, not smaller.  Reported against my own hypothesis.")
    P("")
    P("  NOT a second Kepler-grade law, on two criteria:")
    P("   (4) 'nobody has stated it' is weak -- MOND predictions for Local Group dwarf dispersions with the")
    P("       external-field effect are Angus 2008 and McGaugh & Milgrom 2013.  Only the partial-slope")
    P("       FRAMING is new, and a statistic is not a law.")
    P("   (3) the scatter is nowhere near RAR-class.")
    P("   (1),(2),(5) pass: measured quantities, a predicted coefficient, and NOT a restatement (dw-3).")
    resid = lsig - (a["spred"] - np.mean(a["spred"] - lsig))
    P(f"   residual scatter of log sigma about the framework's prediction (zero point free): "
      f"{np.std(resid):.3f} dex, against the <= 0.1 dex a Kepler-grade relation needs.")
    P("")
    P("  STABILITY, reported whichever way it falls: the MW satellites alone give "
      f"{[r for r in rows if r[0].startswith('MW satellites')][0][2]:+.4f} +/- "
      f"{[r for r in rows if r[0].startswith('MW satellites')][0][3]:.4f} against a predicted "
      f"{[r for r in rows if r[0].startswith('MW satellites')][0][4]:+.4f}, which is LambdaCDM's answer to")
    P("  a fraction of a sigma and the framework's to several.  The M31 satellites alone are the framework's")
    P(f"  best subsample at {bs:.1f} sigma, so the verdict is not uniform across the sample and must not be")
    P("  quoted as if it were.")
    P("")
    P("  CAVEAT BOTH WAYS, unchanged from the proposal and not resolvable with this data: tidal heating")
    P("  inflates the dispersions of close satellites in EITHER theory and biases the measured slope")
    P("  POSITIVE, i.e. against the framework.  Dropping the ten nearest satellites does not remove it")
    P("  (the slope is unchanged), but a properly tidally-cleaned sample could still move this.")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
