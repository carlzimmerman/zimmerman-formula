#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g01_efe_sign_under_modified_inertia.py -- does the OTHER arm fix the framework's sharpest failure?  It does not.
=======================================================================================================================
THE FAILURE.  k_contrarian_dwarfefe measured, on 92 Local Group dwarfs with a MEASURED line-of-sight dispersion,
    d log sigma_los / d log(g_e/a_0)  at fixed (log M_*, log r_half) with a full quadratic surface  =  +0.0800 +- 0.0467
against a modified-GRAVITY prediction of -0.1006 through the identical design matrix (f01/f03 recomputed the
prediction side with the sphere-average and internal-field corrections and got -0.0929 analytically; the negative
survived both).  That is ~3.7-3.9 sigma AGAINST and it is a SIGN disagreement.  No amplitude correction fixes a sign.

THE HOPE, which is why this script exists.  f09 found that every system the framework fits is rotation-supported and
every system it misses is pressure-supported, and Milgrom proved modified INERTIA and modified GRAVITY coincide
exactly for circular orbits in the deep-MOND limit and differ for every other orbit.  The external-field effect in
modified gravity is a consequence of the AQUAL/QUMOND field equation's NONLINEARITY.  Modified inertia has no such
field equation, and a constant external acceleration is removable by going to the freely-falling frame -- so the
naive hope is that modified inertia predicts a WEAKER external-field effect, or one of the OPPOSITE sign, and the
framework's worst failure becomes the other arm's signature.

THIS SCRIPT ATTACKS THAT HOPE AND THE HOPE LOSES.  Three findings, in order of how much they cost:

  1. The hope's premise is FALSE at the local level.  The natural local ("algebraic") modified-inertia prescription --
     mu(|a|/a_0) a = -grad Phi_N, with a the body's TOTAL acceleration in the inertial frame -- gives a sphere-averaged
     external-field coupling that is NUMERICALLY IDENTICAL to QUMOND's, computed here by two independent code paths.
     The freely-falling frame does NOT remove the effect, because mu depends on the acceleration MAGNITUDE and a_0 is
     absolute: MOND of any kind breaks the strong equivalence principle (Milgrom 1986; Milgrom 2011 arXiv:1111.1611).
     So modified inertia's escape, if it has one, must come ENTIRELY from its time-NONLOCAL structure.

  2. That nonlocal structure is NOT fixed by the MOND limits.  Modified inertia is a CLASS, not a theory (Milgrom
     1994, Ann. Phys. 229, 384: the modification is a functional of the whole trajectory and must be nonlocal in time
     for momentum conservation).  Nothing in the class fixes how much a zero-frequency, constant external acceleration
     contributes relative to the system's own bound modes.  So this script does the only honest thing: it introduces
     ONE parameter w -- the external-field transparency, the weight the external field carries in the kernel's
     argument relative to the internal field -- and reports the whole range.  w = 1 is modified gravity / local
     modified inertia; w = 0 is the equivalence-principle limit, no external-field effect at all.

  3. Over the ENTIRE physically motivated range w in [0, 1] the predicted slope is never positive.  The best modified
     inertia can do is REMOVE the effect, landing on LambdaCDM's exact zero, which sits 1.7 sigma from the data.
     To MATCH +0.0800 the theory needs an ANTI-external-field effect at ~80% of full modified-gravity strength, and
     no modified-inertia theory in the literature has been shown to produce one.  Reported as a range, not a result.

WHAT IS ACTUALLY WORTH SOMETHING here is the theory-light statement (c): the measurement is 1.71 sigma from ZERO.
The Local Group dwarfs are CONSISTENT WITH NO EXTERNAL-FIELD EFFECT.  That is a clean statement that costs no theory
and is the only thing in this file I would quote.

AND THE TRAP.  "The other theory happens to fix my worst failure" is the classic wrong claim, so section 5 attacks
the +0.0800 itself: host fixed effects, dispersion-error weighting, the binary-inflation floor, the ultra-faint
discovery selection, jackknife influence, and the raw correlations between environment and every galaxy property in
the sample.  Reported whichever way they fall.  ONE OF THEM FIRES.

LITERATURE USED (stated from knowledge, NOT machine-verified against the paper text in this run -- flagged so):
  Milgrom 1994, Ann. Phys. 229, 384    -- the modified-inertia class; nonlocality forced by momentum conservation;
                                          circular orbits obey the algebraic mu(a/a_0) a = g_N exactly.
  Milgrom 2011, arXiv:1111.1611        -- "MOND particularly as modified inertia": MI and MG agree exactly for
                                          circular orbits in the deep-MOND limit and differ for every other orbit;
                                          the EFE follows from a_0 being an absolute constant and is present in MI.
  Milgrom 1986, ApJ 302, 617;
  Famaey & McGaugh 2012, LRR 15, 10 eq 59-60 -- the modified-gravity EFE coupling TENSOR nu[delta_ij + L n_i n_j].
  McGaugh & Milgrom 2013, ApJ 775, 139 -- MOND dispersion predictions for M31 dwarfs including the EFE.
  Chae et al. 2020, ApJ 904, 51; 2021, ApJ 921, 104 -- a CLAIMED EFE detection in SPARC rotation curves with the
                                          modified-gravity sign.  Opposite conclusion to this dwarf slope; noted as
                                          an unresolved literature conflict, not adjudicated here.
  Spencer et al. 2017, AJ 153, 254     -- unresolved binaries inflate dSph dispersions, worst below ~3 km/s.
  Pace 2024, Local Volume Database     -- the dwarf catalogue (real_research/data/dsph/lvd_dwarf_*.csv).

BOTH FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL AND FOUR OF THEM DO.
"""
import os, sys, math, csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0

HERE = os.path.dirname(os.path.abspath(__file__))
DDIR = os.path.join(HERE, "..", "real_research", "data", "dsph")
G, MSUN = 6.674e-11, 1.989e30
PC = 3.0856775814913673e16; KPC = 1e3*PC
MV_SUN = 4.83
M_MW_BAR, M_M31_BAR = 6.0e10, 1.2e11          # McMillan 2017; Tamm+2012/Chemin+2009 -- baryons only

# --------------------------------------------------------------------------------------------------- kernel
def nu_a(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/(-np.expm1(-np.sqrt(y)))
def nu1(x):
    x = max(float(x), 1e-300); return 1.0/(-math.expm1(-math.sqrt(x)))
def Lx(x, d=1e-5):
    return (math.log(nu1(x*(1+d))) - math.log(nu1(x*(1-d))))/(2*d)
def nu_sphere_a(y):
    """f01's sphere-averaged coupling nu(x)(1 + L/3): the angle average an ISOTROPIC dispersion measures."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.array([nu1(v)*(1.0 + Lx(v)/3.0) for v in np.atleast_1d(y)]).reshape(np.shape(y))

# --------------------------------------------------------------------------------------------------- data
def load(ups_v=2.0):
    """LVD dwarfs with a MEASURED (not upper-limit) dispersion, a half-light radius and M_V.  Loader lifted
    verbatim from k_contrarian_dwarfefe.py so the measurement side is reproduced, not re-derived."""
    out = []
    for fn, tag in [("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"),
                    ("lvd_dwarf_local_field.csv", "field")]:
        for r in csv.DictReader(open(os.path.join(DDIR, fn))):
            if r.get("vlos_sigma_ul", "").strip(): continue
            try:
                sig = float(r["vlos_sigma"]); rh = float(r["rhalf_physical"]); mv = float(r["M_V"])
            except Exception: continue
            if not (sig > 0 and rh > 0 and np.isfinite(mv)): continue
            def g(k):
                try: return float(r[k])
                except Exception: return float("nan")
            dmw, dm31, dhel = g("distance_gc"), g("distance_m31"), g("distance")
            em, ep = g("vlos_sigma_em"), g("vlos_sigma_ep")
            esig = np.nanmean([v for v in (em, ep) if np.isfinite(v)]) if np.isfinite(em) or np.isfinite(ep) else np.nan
            LV = 10**(-0.4*(mv - MV_SUN)); Mb = ups_v*LV
            try:
                mhi = float(r["mass_HI"])
                if np.isfinite(mhi) and not r.get("mass_HI_ul", "").strip(): Mb += 1.33*10**mhi
            except Exception: pass
            gN = []
            if np.isfinite(dmw) and dmw > 0:  gN.append(G*M_MW_BAR*MSUN/(dmw*KPC)**2)
            if np.isfinite(dm31) and dm31 > 0: gN.append(G*M_M31_BAR*MSUN/(dm31*KPC)**2)
            if not gN: continue
            out.append(dict(key=r["key"], grp=tag, sig=sig, esig=esig, rh=rh*PC, LV=LV, Mb=Mb, mv=mv,
                            gNe=max(gN), dhel=dhel))
    return out

# --------------------------------------------------------------------------------------------------- regression
def partial_slope(y, cols, wts=None):
    A = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in cols])
    if wts is None:
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    else:
        W = np.asarray(wts, float)
        coef = np.linalg.solve(A.T @ (A*W[:, None]), A.T @ (y*W))
    return coef[-1]

def boot_err(y, cols, nb=3000, seed=7, wts=None):
    rng = np.random.default_rng(seed); n = len(y); cols = [np.asarray(c, float) for c in cols]
    o = np.empty(nb)
    for i in range(nb):
        k = rng.integers(0, n, n)
        o[i] = partial_slope(y[k], [c[k] for c in cols], None if wts is None else np.asarray(wts)[k])
    return float(np.std(o))

def design(lM, lrh, lge):
    """Statistic (C) of k_contrarian_dwarfefe: full quadratic surface in (log M_*, log r_h), then log g_e last."""
    return [lM, lrh, lM*lM, lrh*lrh, lM*lrh, lge]

def predict_logsigma(d, a0, w, coupling=nu_sphere_a, beta=2.0/9.0):
    r"""sigma from sigma^2 = beta * C(w) * G M_b / r_h, with the external-field TRANSPARENCY w applied in the LOG
    of the coupling rather than inside the kernel's argument:

        log C(w) = log C_isolated + w * [ log C_full - log C_isolated ],
        C_isolated = coupling(x_int),   C_full = coupling(x_int + x_e).

    w = 1 recovers the full modified-gravity / local-modified-inertia coupling EXACTLY; w = 0 recovers the isolated
    law EXACTLY, i.e. no external-field effect at all.  This form is used INSTEAD of coupling(x_int + w x_e) for a
    reason that is a bug I hit and fixed: putting w inside the argument sends x_int + w x_e NEGATIVE for w < 0 and
    the kernel is undefined there, which produced nonsense slopes of order +30.  The log form is well defined on the
    whole real line, is monotone in w, and makes the predicted slope EXACTLY linear in w (the regression coefficient
    is a linear functional of the response vector), which is what section 2 then inverts.  beta cancels everywhere."""
    Mb = np.array([g["Mb"] for g in d])*MSUN; rh = np.array([g["rh"] for g in d])
    gNe = np.array([g["gNe"] for g in d])
    x_int = G*Mb/rh**2/a0; x_e = gNe/a0
    lC = np.log(coupling(x_int)) + w*(np.log(coupling(x_int + x_e)) - np.log(coupling(x_int)))
    s2 = beta*np.exp(lC)*G*Mb/rh
    return np.log10(np.sqrt(s2)/1e3)

def true_external_field(gNe, a0):
    """The x-variable of the law: the TRUE (MONDian) external field, g_e = nu(g_N/a_0) g_N.  Same as k_contrarian."""
    return nu_a(gNe/a0)*gNe

# ======================================================================================================
def main():
    ck = Check()
    P("="*116)
    P("g01 -- does modified INERTIA predict a different SIGN for the external-field slope?  Short answer: no.")
    P("="*116)

    d = load(); n = len(d)
    lsig = np.log10(np.array([g["sig"] for g in d]))
    lM   = np.log10(np.array([g["Mb"] for g in d]))
    lrh  = np.log10(np.array([g["rh"]/PC for g in d]))
    gNe  = np.array([g["gNe"] for g in d])
    grp  = np.array([g["grp"] for g in d])
    mv   = np.array([g["mv"] for g in d])
    sig  = np.array([g["sig"] for g in d])
    esig = np.array([g["esig"] for g in d])
    dhel = np.array([g["dhel"] for g in d])
    info(f"N = {n} Local Group dwarfs with a MEASURED dispersion ({(grp=='MW').sum()} MW, "
         f"{(grp=='M31').sum()} M31, {(grp=='field').sum()} field).  Local Volume Database (Pace 2024).")

    # ==================================================================================================
    P(""); P("="*116)
    P("1.  THE HOPE'S PREMISE, TESTED: does going to the freely-falling frame remove the effect in modified inertia?")
    P("="*116)
    info("Local ('algebraic') modified inertia: the body's TOTAL acceleration a in the inertial frame obeys")
    info("    mu(|a|/a_0) a = -grad Phi_N   ==>   a = nu(|g_N|/a_0) g_N   pointwise  (Milgrom 1994; 2011).")
    info("The dwarf's centre of mass obeys the SAME law with the host's field, A_cm = nu(g_Ne/a_0) g_Ne, so the")
    info("relative acceleration a_rel = a - A_cm is what an internal observer measures.  If the equivalence principle")
    info("were intact, a_rel would not know g_Ne at all.  Sphere-average -<a_rel . r_hat>/h and compare with QUMOND's")
    info("flux-theorem answer <g_r> = <S_r>, S = nu(|g_N|/a_0) g_N (f01).  TWO INDEPENDENT CODE PATHS.")

    def sphere_MI(xe, h, nth=6001):
        """Local modified inertia: angle-average of the radial part of a_rel = nu(|g_N|)g_N - A_cm."""
        th = np.linspace(0.0, math.pi, nth); wq = np.sin(th)/2.0
        st, ct = np.sin(th), np.cos(th)
        gx, gz = -h*st, xe - h*ct                                     # total Newtonian field, units a_0
        mag = np.hypot(gx, gz)
        nuv = nu_a(mag)
        ax, az = nuv*gx, nuv*gz                                       # total acceleration, units a_0
        Acm = nu1(xe)*xe                                              # CM acceleration, along +z
        arx, arz = ax, az - Acm
        ar = arx*st + arz*ct
        return -np.trapz(ar*wq, th)/np.trapz(wq, th)/h

    def sphere_QUMOND(xe, h, nth=6001):
        """QUMOND flux theorem: <g_r>_sphere = <S_r>_sphere, S = nu(|g_N|/a_0) g_N (f01, verbatim structure)."""
        th = np.linspace(0.0, math.pi, nth); wq = np.sin(th)/2.0
        st, ct = np.sin(th), np.cos(th)
        gx, gz = -h*st, xe - h*ct
        nuv = nu_a(np.hypot(gx, gz))
        Sr = nuv*(gx*st + gz*ct)
        return -np.trapz(Sr*wq, th)/np.trapz(wq, th)/h

    def sphere_Acm_radial(xe, nth=6001):
        """<A_cm . r_hat> over a sphere -- computed, NOT asserted to vanish."""
        th = np.linspace(0.0, math.pi, nth); wq = np.sin(th)/2.0
        return float(np.trapz(nu1(xe)*xe*np.cos(th)*wq, th)/np.trapz(wq, th))

    P("")
    info(f"{'x_e':>9} {'h/a_0':>10} {'MI  -<a_rel.r>/h':>19} {'QUMOND  -<S_r>/h':>19} {'frac diff':>12} "
        f"{'nu(x_e)(1+L/3)':>16}")
    worst = 0.0; acm_worst = 0.0
    for xe in (1e-3, 1e-2, 0.1, 0.5, 1.0):
        for hf in (1e-3, 1e-2):
            h = hf*max(xe, 1e-3)
            a, b = sphere_MI(xe, h), sphere_QUMOND(xe, h)
            worst = max(worst, abs(a/b - 1)); acm_worst = max(acm_worst, abs(sphere_Acm_radial(xe)))
            info(f"{xe:9.4f} {h:10.2e} {a:19.6f} {b:19.6f} {100*(a/b-1):11.4f}% "
                 f"{nu1(xe)*(1+Lx(xe)/3):16.6f}")
    ck("G1 (AGAINST THE HOPE, AND IT IS THE WHOLE POINT OF SECTION 1) local modified inertia gives the SAME "
       "sphere-averaged external-field coupling as QUMOND, to quadrature precision, by two independent code paths. "
       "Going to the freely-falling frame does NOT remove the external-field effect, because mu depends on the "
       "acceleration MAGNITUDE and a_0 is absolute: MOND of every kind breaks the strong equivalence principle. "
       "The centre-of-mass term drops out only because its radial sphere-average vanishes, which is computed here "
       "and not assumed.",
       worst < 1e-3 and acm_worst < 1e-9,
       f"worst fractional MI-vs-QUMOND difference over 10 (x_e, h) pairs = {100*worst:.5f}%; "
       f"|<A_cm . r_hat>| <= {acm_worst:.2e}")

    # ==================================================================================================
    P(""); P("="*116)
    P("2.  SO THE ESCAPE MUST BE NONLOCAL.  One parameter: the external-field transparency w.")
    P("="*116)
    info("Modified inertia is a CLASS, not a theory.  Milgrom 1994 shows the modification must be a NONLOCAL")
    info("functional of the whole trajectory (a local one cannot conserve momentum), and nothing in the class fixes")
    info("how much a zero-frequency, constant external acceleration weighs against the system's own bound modes.")
    info("So parameterise it honestly with ONE number and report the RANGE:")
    info("    log C(w) = log nu_sphere(x_int) + w * [ log nu_sphere(x_int + x_e) - log nu_sphere(x_int) ],  x = g_N/a_0")
    info("    w = 1  local MI == modified gravity (section 1); w = 0  full equivalence-principle restoration, no EFE.")
    info("w is NOT derived here and MUST NOT be quoted as a prediction.  It is a dial spanning the class's freedom.")
    info("(The transparency is applied in the LOG of the coupling, not inside the kernel's argument.  Putting it in the")
    info(" argument sends x_int + w x_e negative for w < 0 where the kernel is undefined -- a bug that produced slopes")
    info(" of order +30 in the first run of this script, and is recorded here rather than quietly fixed.)")

    lge_by_foot = {}; res = {}
    for foot, a0 in A0.items():
        ge = true_external_field(gNe, a0); lge = np.log10(ge/a0); lge_by_foot[foot] = lge
        q = design(lM, lrh, lge)
        obs = partial_slope(lsig, q); err = boot_err(lsig, q)
        pred = {w: partial_slope(predict_logsigma(d, a0, w), q) for w in
                (-1.0, -0.8, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0)}
        res[foot] = dict(a0=a0, obs=obs, err=err, pred=pred, lge=lge, q=q)
        P(f"\n  ---- {foot} footing, a_0 = {a0:.3e} ------------------------------------------------------------")
        info(f"g_e/a_0 spans {np.min(ge/a0):.4f} to {np.max(ge/a0):.3f}, median {np.median(ge/a0):.4f}")
        info(f"MEASURED slope, statistic (C), identical design matrix: {obs:+.4f} +/- {err:.4f}")
        P(f"      {'w':>6}  {'arm':<44} {'predicted slope':>16} {'EFE part':>10} {'sigma from data':>17}")
        for w in sorted(pred):
            lab = ("modified gravity == local modified inertia" if w == 1.0 else
                   "no EFE (equivalence principle intact)" if w == 0.0 else
                   "nonlocal modified inertia, transparency w" if w > 0 else
                   "hypothetical ANTI-EFE (no theory supplies it)")
            P(f"      {w:+6.2f}  {lab:<44} {pred[w]:+16.4f} {pred[w]-pred[0.0]:+10.4f} {abs(obs-pred[w])/err:16.2f}")

    a, b = res["canonical"], res["alt"]
    OBS, ERR = a["obs"], a["err"]
    ck("G2 REPRODUCTION: this script's independent regression must recover k_contrarian_dwarfefe's measured "
       "+0.0800 +/- 0.0467 on statistic (C).  If it does not, nothing downstream means anything.",
       abs(OBS - 0.0800) < 0.004 and abs(ERR - 0.0467) < 0.008,
       f"this run {OBS:+.4f} +/- {ERR:.4f} vs committed +0.0800 +/- 0.0467 (alt footing {b['obs']:+.4f} +/- {b['err']:.4f})")

    neg_all = all(v - res[foot]["pred"][0.0] <= 1e-12 for foot in res
                  for w, v in res[foot]["pred"].items() if w > 0)
    ck("G3 THE HOPE FAILS, STATED AS A RANGE, AND STATED ON THE RIGHT QUANTITY: the EXTERNAL-FIELD PART of the "
       "predicted slope, slope(w) - slope(0), is NON-POSITIVE for every w in (0, 1] on both footings.  Modified "
       "inertia cannot flip the sign by weakening the external-field effect; weakening it only walks the prediction "
       "toward the no-EFE limit.  The other arm does NOT rescue the framework's sharpest failure -- it can only make "
       "the failure smaller.  (Stated as the DIFFERENCE and not as the raw slope because the design matrix leaks a "
       "small positive constant into every arm alike -- see G4.)",
       neg_all,
       "; ".join(f"{foot} EFE part: w=1 {res[foot]['pred'][1.0]-res[foot]['pred'][0.0]:+.4f}, "
                 f"w=0.5 {res[foot]['pred'][0.5]-res[foot]['pred'][0.0]:+.4f}, "
                 f"w=0.25 {res[foot]['pred'][0.25]-res[foot]['pred'][0.0]:+.4f}" for foot in res))

    # leakage: what does the pipeline return for a model with NO external-field dependence at all?
    leak = a["pred"][0.0]
    ck("G4 PIPELINE LEAKAGE, reported because it moves the answer TOWARD the framework's rival and must not be "
       "hidden: a model with w = 0 has no external-field dependence whatsoever, so the honest zero-EFE prediction "
       "through this design matrix is NOT 0.0000 but the residual curvature leakage.  It is small but non-zero, and "
       "it means the raw predicted slope is faintly POSITIVE for w below about 0.13 -- from the regression, not from "
       "any physics.",
       abs(leak) < 0.05, f"w=0 predicted slope through the pipeline = {leak:+.4f} (canonical), "
                         f"{b['pred'][0.0]:+.4f} (alt); pure analytic zero-EFE answer is exactly 0")

    # invert: what w do the data require?  slope(w) is EXACTLY linear in w by construction of the log-interpolation.
    ws = np.array(sorted(a["pred"])); ss = np.array([a["pred"][w] for w in ws])
    m_, c_ = a["pred"][1.0] - a["pred"][0.0], a["pred"][0.0]
    lin_res = float(np.max(np.abs(ss - (m_*ws + c_))))
    w_star = (OBS - c_)/m_; w_err = ERR/abs(m_)
    P("")
    info(f"slope_pred(w) = {m_:+.5f} w {c_:+.5f} EXACTLY (max deviation over the 9-point grid {lin_res:.2e}), because")
    info("a least-squares coefficient is a linear functional of the response and log C is linear in w by construction.")
    info(f"INVERTING: the data require w = {w_star:+.3f} +/- {w_err:.3f}.")
    ck("G5 WHAT THE DATA PREFER, and it is not merely 'a weaker EFE': the central value asks a modified-inertia "
       "theory for an ANTI-external-field effect -- the external field ENHANCING the MOND boost rather than "
       "suppressing it.  No modified-inertia theory in the literature has been shown to do that and this script does "
       "not construct one.  The check passes only if the preferred w is negative AND the modified-gravity value w = 1 "
       "is excluded at more than 2 sigma.  REPORTED AGAINST THE CLAIM: w = 0 is NOT excluded, so the data do not "
       "DEMAND an anti-EFE, they merely lean that way.",
       w_star < 0 and (1.0 - w_star)/w_err > 2.0,
       f"preferred w = {w_star:+.3f} +/- {w_err:.3f}; w = 1 (modified gravity) is {(1.0-w_star)/w_err:.2f} sigma away, "
       f"w = 0 (no EFE) only {abs(0.0-w_star)/w_err:.2f} sigma away and therefore fully allowed "
       f"(alt footing: w = {(b['obs']-b['pred'][0.0])/(b['pred'][1.0]-b['pred'][0.0]):+.3f})")

    # ==================================================================================================
    P(""); P("="*116)
    P("3.  THE THEORY-LIGHT STATEMENT (c): how far are the data from ZERO external-field effect?")
    P("="*116)
    for foot in res:
        r = res[foot]
        info(f"{foot:10} measured {r['obs']:+.4f} +/- {r['err']:.4f}  ->  {abs(r['obs'])/r['err']:.2f} sigma from an "
             f"exact zero;  {abs(r['obs']-r['pred'][0.0])/r['err']:.2f} sigma from the leakage-corrected zero-EFE model;  "
             f"{abs(r['obs']-r['pred'][1.0])/r['err']:.2f} sigma from modified gravity")
    z_can = abs(a["obs"])/a["err"]; z_alt = abs(b["obs"])/b["err"]
    ck("G6 THE ONLY STATEMENT HERE WORTH QUOTING, and it costs no theory: the Local Group dwarf dispersions are "
       "CONSISTENT WITH NO EXTERNAL-FIELD EFFECT AT ALL on both footings.  That is what GR plus dark matter predicts "
       "exactly, by the strong equivalence principle, and it is what any modified-inertia theory whose nonlocal "
       "kernel screens a constant external acceleration would predict.  It does not distinguish the two.",
       z_can < 3.0 and z_alt < 3.0,
       f"canonical {z_can:.2f} sigma from zero, alt {z_alt:.2f} sigma from zero "
       f"(modified gravity sits at {abs(a['obs']-a['pred'][1.0])/a['err']:.2f} and "
       f"{abs(b['obs']-b['pred'][1.0])/b['err']:.2f} sigma)")

    # ==================================================================================================
    P(""); P("="*116)
    P("4.  MUTATION CONTROLS")
    P("="*116)
    rng = np.random.default_rng(2026)
    shuf = np.array([partial_slope(lsig, design(lM, lrh, a["lge"][rng.permutation(n)])) for _ in range(1500)])
    ck("M1 (d) SHUFFLE THE ENVIRONMENT LABELS: permuting log(g_e/a_0) among the dwarfs must destroy the measured "
       "slope.  If it did not, the regression itself would be manufacturing the signal.",
       abs(np.mean(shuf)) < 0.25*np.std(shuf) and abs(OBS) > 1.5*np.std(shuf),
       f"shuffled {np.mean(shuf):+.4f} +/- {np.std(shuf):.4f} against the real {OBS:+.4f} "
       f"({abs(OBS)/np.std(shuf):.2f} shuffle-sigma)")

    newt = partial_slope(predict_logsigma(d, a["a0"], 1.0, coupling=lambda y: np.ones_like(np.asarray(y, float))),
                         a["q"])
    ck("M2 nu == 1 (Newton, strong equivalence principle intact) must predict a slope of exactly zero in BOTH arms "
       "-- the LambdaCDM alternative, computed rather than asserted",
       abs(newt) < 1e-12, f"predicted slope with nu == 1: {newt:+.3e}")

    # x = g_N/a_0, so a_0 x 100 pushes every dwarf DEEP-MOND and a_0 / 100 pushes it deep-NEWTONIAN.  I had this
    # backwards in the first run of this script and the check failed for that reason; recorded, not quietly fixed.
    # The lever is taken on the EFE PART slope(w=1) - slope(w=0), which removes the design-matrix leakage of G4.
    def efe_part(a0v):
        return (partial_slope(predict_logsigma(d, a0v, 1.0), a["q"])
                - partial_slope(predict_logsigma(d, a0v, 0.0), a["q"]))
    dm, base_efe, nw = efe_part(a["a0"]*100), efe_part(a["a0"]), efe_part(a["a0"]/100)
    xr = np.array([g["gNe"] for g in d])/(G*np.array([g["Mb"] for g in d])*MSUN/np.array([g["rh"] for g in d])**2)
    fbar = float(np.mean(xr/(1.0 + xr)))
    ck("M3 a_0 LEVER, both directions, on the leakage-free EFE part of the slope: at a_0 / 100 every dwarf is "
       "deep-NEWTONIAN and the external-field effect must collapse toward zero; at a_0 x 100 every dwarf is "
       "deep-MOND and it must saturate near the analytic deep value -(1/4)<x_e/(x_int+x_e)>, which is diluted well "
       "below -1/4 because these dwarfs' own internal fields dominate their external ones.",
       abs(nw) < 0.3*abs(base_efe) and abs(dm) > abs(base_efe) and abs(dm - (-0.25*fbar)) < 0.05,
       f"deep-Newtonian (a_0/100) {nw:+.5f}; canonical {base_efe:+.5f}; deep-MOND (a_0 x100) {dm:+.5f} against the "
       f"analytic deep-MOND target {-0.25*fbar:+.5f} (mean x_e/(x_int+x_e) = {fbar:.3f})")

    # ==================================================================================================
    P(""); P("="*116)
    P("5.  ATTACKING THE +0.0800 ITSELF.  Is the measurement robust, or is it a selection effect?")
    P("="*116)
    info("raw correlations of log(g_e/a_0) with everything that could confound it, canonical footing:")
    lge = a["lge"]
    fin_e = np.isfinite(esig) & (esig > 0)
    for lab, v, msk in [("log M_b (stellar mass)", lM, np.ones(n, bool)),
                        ("log r_half", lrh, np.ones(n, bool)),
                        ("M_V (fainter = larger)", mv, np.ones(n, bool)),
                        ("log sigma_los", lsig, np.ones(n, bool)),
                        ("log heliocentric distance", np.log10(np.where(dhel > 0, dhel, np.nan)),
                         np.isfinite(dhel) & (dhel > 0)),
                        ("fractional error on sigma", esig/sig, fin_e)]:
        info(f"    corr(log g_e, {lab:<28}) = {np.corrcoef(lge[msk], np.asarray(v)[msk])[0,1]:+.3f}   (N={msk.sum()})")

    P("")
    P(f"    {'variant of the measurement':<58} {'N':>4} {'slope':>18} {'sigma from 0':>13} {'sigma from MG':>14}")
    P("    " + "-"*112)
    variants = []
    def add(lab, y, cols, wts=None, npts=None, predw=None):
        e = boot_err(y, cols, nb=1500, wts=wts)
        s = partial_slope(y, cols, wts)
        pm = a["pred"][1.0] if predw is None else predw
        variants.append((lab, npts if npts else len(y), s, e, abs(s)/e, abs(s-pm)/e))
        P(f"    {lab:<58} {variants[-1][1]:4d} {s:+9.4f}+/-{e:.4f} {abs(s)/e:13.2f} {abs(s-pm)/e:14.2f}")

    add("baseline, statistic (C)", lsig, a["q"])
    # host fixed effects: does the pooled slope survive removing between-host offsets?
    dmw = (grp == "MW").astype(float); dm31 = (grp == "M31").astype(float)
    qh = design(lM, lrh, lge); qh = qh[:-1] + [dmw, dm31, qh[-1]]
    pred_h = partial_slope(predict_logsigma(d, a["a0"], 1.0), qh)
    add("+ host fixed effects (MW / M31 dummies)", lsig, qh, predw=pred_h)
    # inverse-variance weighting on the dispersion
    wts = np.zeros(n); wts[fin_e] = 1.0/( (esig[fin_e]/sig[fin_e]/math.log(10))**2 )
    m_e = fin_e
    qe = [c[m_e] for c in a["q"]]
    add("inverse-variance weighted by the sigma error", lsig[m_e], qe, wts=wts[m_e],
        predw=partial_slope(predict_logsigma(d, a["a0"], 1.0)[m_e], qe, wts[m_e]))
    # binary-inflation floor
    for cut in (2.0, 3.0, 4.0):
        m = sig > cut; qm = [c[m] for c in a["q"]]
        add(f"drop sigma <= {cut:.0f} km/s (unresolved-binary inflation)", lsig[m], qm,
            predw=partial_slope(predict_logsigma(d, a["a0"], 1.0)[m], qm))
    # ultra-faint discovery selection
    for cut in (-6.0, -8.0):
        m = mv < cut; qm = [c[m] for c in a["q"]]
        add(f"drop M_V > {cut:.0f} (ultra-faint discovery selection)", lsig[m], qm,
            predw=partial_slope(predict_logsigma(d, a["a0"], 1.0)[m], qm))
    # host subsets
    for lab, m in [("MW satellites only", grp == "MW"), ("M31 satellites only", grp == "M31"),
                   ("MW + M31 (drop ambiguous field hosts)", grp != "field")]:
        qm = [c[m] for c in a["q"]]
        add(lab, lsig[m], qm, predw=partial_slope(predict_logsigma(d, a["a0"], 1.0)[m], qm))

    base = variants[0]; hostfe = variants[1]
    ck("R1 HOST FIXED EFFECTS -- THE TEST THAT MATTERS AND THE ONE NOBODY RAN.  The pooled slope (+0.08) is LARGER "
       "than either host's slope taken alone (MW +0.01, M31 +0.03 in the committed run).  That is the signature of a "
       "between-host OFFSET being read as a within-host trend: the Milky Way and M31 satellite populations differ in "
       "mean environment AND in mean dispersion at fixed mass, and pooling them converts the offset into a slope.  "
       "This check PASSES only if the slope survives host dummies.",
       abs(hostfe[2]) > base[3],
       f"baseline {base[2]:+.4f} +/- {base[3]:.4f}  ->  with host dummies {hostfe[2]:+.4f} +/- {hostfe[3]:.4f} "
       f"(shift {hostfe[2]-base[2]:+.4f} = {abs(hostfe[2]-base[2])/base[3]:.2f} baseline sigma)")

    signs = [v[2] for v in variants]
    ck("R2 SIGN STABILITY across every variant.  The measured slope's SIGN is the entire content of the disagreement "
       "with modified gravity, so if the sign is not stable the disagreement is not either.",
       all(s > 0 for s in signs),
       f"{sum(s>0 for s in signs)}/{len(signs)} variants positive; range {min(signs):+.4f} to {max(signs):+.4f}")

    worst_mg = min(v[5] for v in variants); wl = [v[0] for v in variants if v[5] == worst_mg][0]
    best_mg = max(v[5] for v in variants); bl = [v[0] for v in variants if v[5] == best_mg][0]
    ck("R3 THE MODIFIED-GRAVITY NEGATIVE MUST NOT EVAPORATE UNDER ANY REASONABLE ANALYSIS CHOICE.  It does not "
       "survive every one: reported whichever way it falls.",
       worst_mg > 3.0,
       f"weakest variant for the negative: '{wl}' at {worst_mg:.2f} sigma; strongest: '{bl}' at {best_mg:.2f} sigma")

    # jackknife influence
    jk = np.array([partial_slope(np.delete(lsig, i), [np.delete(c, i) for c in a["q"]]) for i in range(n)])
    imax = int(np.argmax(np.abs(jk - OBS)))
    ck("R4 NO SINGLE DWARF DRIVES THE RESULT: leave-one-out must not move the slope by more than half a bootstrap "
       "sigma.  With only 92 objects and a 6-term design this is a real risk.",
       np.max(np.abs(jk - OBS)) < 0.5*ERR,
       f"largest leave-one-out shift {jk[imax]-OBS:+.4f} = {abs(jk[imax]-OBS)/ERR:.2f} bootstrap sigma "
       f"(dropping '{d[imax]['key']}')")

    ck("R5 SELECTION AUDIT, reported not asserted: does environment correlate with a galaxy property strongly enough "
       "to fake the slope?  The dangerous one is the ultra-faint discovery selection -- faint, compact dwarfs are "
       "found preferentially close to the Milky Way, i.e. at HIGH g_e, and their dispersions are the ones unresolved "
       "binaries inflate (Spencer+2017).  That would manufacture a POSITIVE slope in ANY theory.  The check passes "
       "only if BOTH the luminosity cut and the dispersion floor leave the slope intact.",
       all(v[2] > 0 and abs(v[2]) > 0.5*v[3] for v in variants if "drop sigma" in v[0] or "drop M_V" in v[0]),
       "; ".join(f"{v[0]}: {v[2]:+.4f} +/- {v[3]:.4f}" for v in variants if "drop sigma" in v[0] or "drop M_V" in v[0]))

    # ==================================================================================================
    P(""); P("="*116)
    P("VERDICT")
    P("="*116)
    P("  THE ANSWER TO THE QUESTION ASKED -- does modified inertia predict a different SIGN? -- IS NO.")
    P("  What it CAN do is delete the prediction, and that is worth 3.8 sigma -> 1.4 sigma.  That is not nothing, but")
    P("  it is not a signature either: it is the same answer GR gives, so it buys agreement by predicting nothing.")
    P("")
    P(f"  (a) Modified inertia does NOT uniquely predict a sign, because it is a class and not a theory (Milgrom 1994).")
    P(f"      But the premise the hope rested on is wrong.  The freely-falling frame does not remove the external-field")
    P(f"      effect: the LOCAL modified-inertia prescription mu(|a|/a_0) a = -grad Phi_N gives a sphere-averaged")
    P(f"      coupling numerically IDENTICAL to QUMOND's, to {100*worst:.4f}%, by two independent code paths.  MOND breaks")
    P(f"      the strong equivalence principle in every formulation because a_0 is an absolute constant.  Any escape is")
    P(f"      purely nonlocal, and the class does not fix its size -- so the honest output is a RANGE, not a number.")
    P("")
    P(f"  (b) Through the identical regression pipeline, on the identical 92 dwarfs, both footings:")
    for foot in res:
        r = res[foot]
        P(f"        {foot:10} measured {r['obs']:+.4f} +/- {r['err']:.4f}  |  modified gravity (w=1) {r['pred'][1.0]:+.4f} "
          f"-> {abs(r['obs']-r['pred'][1.0])/r['err']:.2f} sigma  |  no-EFE modified inertia (w=0) {r['pred'][0.0]:+.4f} "
          f"-> {abs(r['obs']-r['pred'][0.0])/r['err']:.2f} sigma")
    P(f"      Over the whole range w in (0, 1] the EXTERNAL-FIELD PART of the prediction is NEGATIVE.  Modified")
    P(f"      inertia can only shrink the failure toward the no-EFE limit; it cannot flip it.  To MATCH the data it")
    P(f"      prefers w = {w_star:+.2f} +/- {w_err:.2f} -- an ANTI-external-field effect at most of full strength.  Nothing in the")
    P(f"      literature supplies one and this script does not construct one, and w = 0 is only {abs(w_star)/w_err:.1f} sigma away, so the")
    P(f"      data lean toward an anti-EFE without demanding one.  DO NOT quote 'modified inertia fixes the EFE")
    P(f"      failure'.  It does not.  The most it buys is 3.8 sigma -> {abs(a['obs']-a['pred'][0.0])/a['err']:.1f} sigma, by deleting the prediction.")
    P("")
    P(f"  (c) The clean, theory-light statement, and the only thing here I would put in the liability table:")
    P(f"      the Local Group dwarfs are {z_can:.2f} sigma (canonical) / {z_alt:.2f} sigma (alt) from ZERO external-field")
    P(f"      effect.  They are CONSISTENT WITH NO EFE.  Modified gravity's {abs(a['obs']-a['pred'][1.0])/a['err']:.1f} sigma stands; the honest")
    P(f"      alternative it loses to is 'no external-field effect', which is GR's answer and is also what a")
    P(f"      screening nonlocal modified inertia would give.  This measurement does not separate those two.")
    P("")
    P(f"  (d) The environment labels shuffle to {np.mean(shuf):+.4f} +/- {np.std(shuf):.4f}: the slope is in the data, not the design.")
    P("")
    P("  THE TRAP, ATTACKED, AND ONE CHARGE STICKS.")
    P(f"      The +0.0800 is NOT uniformly robust.  With host fixed effects it moves to {hostfe[2]:+.4f} +/- {hostfe[3]:.4f}, and")
    P(f"      the pooled slope is larger than EITHER host's slope alone -- the pooled number is carrying a")
    P(f"      between-host offset, not only a within-host trend.  Across all {len(variants)} variants the sign is")
    P(f"      {'stable' if all(s>0 for s in signs) else 'NOT stable'} and the modified-gravity tension ranges {worst_mg:.1f} to {best_mg:.1f} sigma.")
    P(f"      With host dummies the measurement is {abs(hostfe[2])/hostfe[3]:.2f} sigma from zero -- not significant at all.")
    P(f"      The ultra-faint / binary-inflation selection is real and biases POSITIVE in any theory, but cutting on")
    P(f"      luminosity and on a dispersion floor does not remove the slope; it strengthens it, which is the opposite")
    P(f"      of what that selection would do, so that particular charge does not stick.")
    P(f"      Two variants take the modified-gravity negative below 2 sigma: M31 satellites alone ({[v[5] for v in variants if v[0]=='M31 satellites only'][0]:.2f}) and the")
    P(f"      inverse-variance-weighted fit ({[v[5] for v in variants if v[0].startswith('inverse-variance')][0]:.2f}), and R3 FAILS on that.  Net: the modified-gravity negative")
    P(f"      survives as a 3-4 sigma result on the pooled sample but must keep TWO qualifiers -- it is a POOLED slope")
    P(f"      over two host systems, neither of which shows it strongly alone, and it weakens under error weighting.")
    P("")
    P("  LITERATURE ATTRIBUTIONS IN THE HEADER ARE FROM KNOWLEDGE AND WERE NOT MACHINE-VERIFIED AGAINST THE PAPER")
    P("  TEXT IN THIS RUN.  The Chae et al. 2020/2021 SPARC claim of an EFE detection with the modified-gravity SIGN")
    P("  is in direct conflict with this dwarf slope and is NOT adjudicated here -- that conflict is itself an open item.")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
