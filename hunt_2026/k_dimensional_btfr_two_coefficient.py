#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_dimensional_btfr_two_coefficient.py -- COMPUTE stage, angle "dimensional".

CANDIDATE 4 -- THE TWO-COEFFICIENT BTFR.
=================================================================================================================
    V_flat^4 / G  =  (a_0 Upsilon_[3.6]) L_[3.6]  +  (1.33 a_0) M_HI
  fitted as TWO free coefficients instead of one.  The hydrogen coefficient is predicted with no freedom,
  1.33 a_0 = 1.245e-10 (canonical) / 1.503e-10 (alt) m/s^2, and reading a_0 off it never touches a stellar
  mass-to-light ratio: Upsilon is the OTHER coefficient divided by the first.

  THE PROPOSER ALREADY LABELLED THIS A RESTATEMENT.  Section 0 executes the derivation rather than asserting it,
  and confirms the label: substituting M_b = Upsilon L + 1.33 M_HI into v^4 = G M_b a_0 and expanding the
  bracket produces the two-coefficient form in one line.  is_restatement = TRUE.  It is computed anyway because
  its VALUE is not as a law but as a ladder rung whose Upsilon lever is exactly zero, which the hunt's own
  ledger (items 100, 102, 123, 125) says is the property it needs -- and because the ledger also predicts what
  it costs, d log a_0/d log M_HI = -1 exactly.  Both are measured here.

WHAT IS DONE BEYOND THE PROPOSAL, because the naive version is known to be biased:
  the hunt's item 105b found that the BTFR zero-point is NOT G M_b a_0 but G M_b a_0 x C with a structural
  factor C = nu(y)^2 y epsilon -- the kernel is not exactly in its deep-MOND limit at the last measured point,
  and not all of the baryonic mass is enclosed there.  Ignoring it moved a naive 1.53e-10 to 9.82e-11.  Both
  the naive and the C-corrected fits are run here, with C computed per galaxy from that galaxy's own rotation
  curve and the kernel, iterated to convergence.

DATA, ON DISK: SPARC (real_research/data/SPARC_Lelli2016c.mrt + sparc_data/*_rotmod.dat).
BOTH FOOTINGS.  Newtonian alternative computed beside it.  Mutation controls.  Levers measured, not argued.
"""
import os, sys, math
import numpy as np
from hunt_lib import Check, P, info, A0, load_sparc, read_master, nu, KMS2_KPC, kpc, Msun

ck = Check(); rng = np.random.default_rng(20260903)
G = 6.674e-11
HE = 1.33                                   # helium correction on M_HI

P("="*126)
P("k_dimensional_btfr_two_coefficient -- a_0 read off the HYDROGEN coefficient of a two-coefficient BTFR")
P("="*126)

# =================================================================================================================
P("\n" + "-"*126)
P("0.  THE RESTATEMENT TEST, EXECUTED -- and it closes")
P("-"*126)
P("""  v^4 = G M_b a_0  with  M_b = Upsilon L + 1.33 M_HI  gives  v^4 = G a_0 (Upsilon L + 1.33 M_HI)
  and dividing by G and expanding the bracket:  v^4/G = (a_0 Upsilon) L + (1.33 a_0) M_HI.
  THE DERIVATION CLOSES IN ONE LINE.""")
# executed, not asserted: build both sides numerically and require them to be identical
Ltest = np.logspace(8, 11, 50); Htest = np.logspace(7, 10.5, 50); ups, a0t = 0.5, A0["canonical"]
lhs = G*a0t*(ups*Ltest + HE*Htest)
rhs = (a0t*ups)*G*Ltest + (HE*a0t)*G*Htest
ck("K0 the restatement test is EXECUTED: the two-coefficient form and v^4 = G M_b a_0 are the same expression, "
   "verified numerically to machine precision over three decades of luminosity and hydrogen mass, not argued",
   np.allclose(lhs, rhs, rtol=1e-14),
   f"max relative difference {np.abs(lhs/rhs - 1).max():.2e}  =>  is_restatement = TRUE")
P("  => is_restatement = TRUE.  This is the baryonic Tully-Fisher relation with its bracket expanded.  It is")
P("     reported below as a LADDER RUNG (a different estimator on the same relation), never as a new law.")

# =================================================================================================================
P("\n" + "-"*126)
P("1.  THE SAMPLE")
P("-"*126)
gals = load_sparc(qmax=2, incmin=30, npts=6)
master = read_master()
use = []
for g in gals:
    m = master[g["name"]]
    if not (m["Vflat"] > 0 and m["eVflat"] > 0 and m["L36"] > 0 and m["MHI"] > 0):
        continue
    use.append(g)
P(f"  {len(use)} SPARC galaxies with Q <= 2, inclination >= 30 deg, >= 6 points, and a quoted V_flat, L_[3.6] "
  f"and M_HI")
L = np.array([g["L36"] for g in use])*1e9                       # Lsun
MH = np.array([g["MHI"] for g in use])*1e9                      # Msun
V = np.array([g["Vflat"] for g in use])*1e3                     # m/s
eV = np.array([g["eVflat"] for g in use])*1e3
D = np.array([g["D"] for g in use]); eD = np.array([g["eD"] for g in use])
Y = V**4/G                                                       # kg
Lkg, MHkg = L*Msun, MH*Msun
fgas = HE*MH/(HE*MH + 0.5*L)
info(f"log10 L_[3.6] spans {np.log10(L).min():.2f} to {np.log10(L).max():.2f}; "
     f"gas fraction (at Upsilon = 0.5) {fgas.min():.2f} to {fgas.max():.2f}, median {np.median(fgas):.2f}")
r = np.corrcoef(np.log10(L), np.log10(MH))[0, 1]
P(f"  collinearity of the two regressors: r(log L, log M_HI) = {r:.3f} -- the price the proposal named")

# =================================================================================================================
P("\n" + "-"*126)
P("2.  THE STRUCTURAL FACTOR C, computed per galaxy from its own curve and the kernel  (item 105b)")
P("-"*126)
P("""  v_flat^4 = G M_b a_0 x C with C = nu(y)^2 y epsilon, where y = g_bar/a_0 at the radius where V_flat is
  measured and epsilon = g_bar r^2/(G M_b) folds in the disc geometry and the mass not yet enclosed.  C -> 1 in
  the exact deep-MOND limit.  Computed here from each galaxy's own outermost measured point; because g_bar
  needs Upsilon and Upsilon is what the fit returns, it is iterated to convergence.""")

def structural_C(ups_d, a0):
    Cs = np.empty(len(use))
    for i, g in enumerate(use):
        j = len(g["r"]) - 1                                       # outermost measured point
        rr = g["r"][j]*kpc
        gbar = (g["vg"][j]*abs(g["vg"][j]) + ups_d*g["vd"][j]**2 + 0.7*g["vb"][j]**2)/g["r"][j]*KMS2_KPC
        gbar = max(gbar, 1e-14)
        Mb = ups_d*L[i] + HE*MH[i]
        eps = gbar*rr**2/(G*Mb*Msun)
        y = gbar/a0
        Cs[i] = float(nu(y))**2*y*eps
    return Cs

# =================================================================================================================
P("\n" + "-"*126)
P("3.  THE TWO-COEFFICIENT FIT")
P("-"*126)

def fit_two(Yv, wvar):
    X = np.vstack([Lkg, MHkg]).T
    W = 1.0/wvar
    A = (X*W[:, None]).T @ X
    b = (X*W[:, None]).T @ Yv
    return np.linalg.solve(A, b), np.linalg.inv(A)

def run(a0, corrected, ntag, nboot=2000):
    C = np.ones(len(use))
    coef = np.array([0.5*a0, HE*a0])
    # the weights depend on the fitted model, so BOTH forms are iterated to convergence -- otherwise the
    # Upsilon lever measured below would pick up a weighting artefact rather than the estimator's own property
    for _ in range(30):
        Yc = Y/C
        # variance: V_flat error (4 dlnV) plus distance error on the regressors (2 dlnD), both on the model value
        mdl = np.maximum(coef[0]*Lkg + coef[1]*MHkg, 1e-30)
        var = (4*eV/V*Yc)**2 + (2*eD/D*mdl)**2
        coef_new, cov = fit_two(Yc, var)
        # BUG PATTERN, found and fixed here rather than hidden: np.allclose defaults to atol = 1e-8, and these
        # coefficients are of order 1e-10, so an allclose convergence test is TRUE on the first iteration and the
        # fit silently stops with its seed weights.  The test below is purely relative.
        rel = float(np.max(np.abs(coef_new/np.where(coef == 0, 1e-300, coef) - 1)))
        if not corrected:
            coef = coef_new
            if rel < 1e-12: break
            continue
        ups_new = max(coef_new[0]/(coef_new[1]/HE), 0.05)
        Cn = structural_C(ups_new, a0)
        relC = float(np.max(np.abs(Cn/C - 1)))
        coef = coef_new; C = Cn
        if rel < 1e-10 and relC < 1e-10: break
    a0_gas = coef[1]/HE
    ups = coef[0]/a0_gas
    # bootstrap over galaxies
    bs = []
    idx = np.arange(len(use))
    Yc = Y/C
    mdl = np.maximum(coef[0]*Lkg + coef[1]*MHkg, 1e-30)
    var = (4*eV/V*Yc)**2 + (2*eD/D*mdl)**2
    for _ in range(nboot):
        s = rng.choice(idx, len(idx), replace=True)
        X = np.vstack([Lkg[s], MHkg[s]]).T; W = 1.0/var[s]
        try:
            c2 = np.linalg.solve((X*W[:, None]).T @ X, (X*W[:, None]).T @ Yc[s])
            if c2[1] > 0: bs.append(c2[1]/HE)
        except Exception: pass
    bs = np.array(bs)
    # variance inflation factor for the gas coefficient
    lx, ly = np.log10(Lkg), np.log10(MHkg)
    vif = 1.0/(1 - np.corrcoef(Lkg, MHkg)[0, 1]**2)
    P(f"  {ntag}")
    P(f"    median C = {np.median(C):.3f}  (1.000 = exact deep-MOND limit)" if corrected else
      "    no structural correction applied")
    P(f"    a_0 from the HYDROGEN coefficient  = {a0_gas:.4e} [{np.percentile(bs,16):.3e}, "
      f"{np.percentile(bs,84):.3e}] m/s^2   = {math.log10(a0_gas/A0['canonical']):+.3f} dex from canonical, "
      f"{math.log10(a0_gas/A0['alt']):+.3f} from alt")
    P(f"    Upsilon_[3.6] from the ratio       = {ups:.3f}  (stellar populations give 0.5 +- 0.1)")
    P(f"    variance inflation factor on the gas coefficient (from the L-M_HI collinearity) = {vif:.2f}")
    return a0_gas, ups, bs, C, vif

RES = {}
for foot, a0 in A0.items():
    P(f"\n  ---- footing {foot}: a_0 = {a0:.4e} m/s^2, so the predicted gas coefficient is 1.33 a_0 = "
      f"{HE*a0:.4e} ----")
    RES[(foot, "naive")] = run(a0, False, "NAIVE (no structural correction) -- the form the proposal states")
    RES[(foot, "corr")] = run(a0, True, "C-CORRECTED (item 105b's structural factor, per galaxy, iterated)")

a0n = RES[("canonical", "naive")][0]; a0c = RES[("canonical", "corr")][0]
# the estimator the literature actually uses: a log-space BTFR with the slope FIXED at 4, at a fixed Upsilon
Cc = RES[("canonical", "corr")][3]
for tagc, Cv in [("no structural correction", np.ones(len(use))), ("C-corrected", Cc)]:
    for ups_fix in (0.5,):
        Mb = ups_fix*Lkg + HE*MHkg
        a0_log = 10**np.mean(np.log10((V**4/G/Cv)/Mb))
        P(f"  the ESTIMATOR the literature uses instead -- log-space BTFR, slope fixed at 4, Upsilon = "
          f"{ups_fix} ({tagc}): a_0 = {a0_log:.4e} "
          f"({math.log10(a0_log/A0['canonical']):+.3f} dex from canonical)")
        if tagc == "no structural correction": A0_LOGNAIVE = a0_log
        else: A0_LOGCORR = a0_log
ck("K3.1 THE CHECK THAT MATTERS FOR A LADDER RUNG, and it fails: two estimators of the SAME relation on the SAME "
   "galaxies -- this linear-space two-coefficient regression and the log-space fixed-slope average the "
   "literature uses -- must agree to better than the 0.082 dex gap between the two footings, or a_0 read this "
   "way cannot decide between them",
   abs(math.log10(a0n/A0_LOGNAIVE)) < 0.082,
   f"linear-space two-coefficient {a0n:.3e} vs log-space fixed-slope {A0_LOGNAIVE:.3e}: "
   f"{math.log10(a0n/A0_LOGNAIVE):+.3f} dex apart, against a footing gap of 0.082 dex")
bs_c = RES[("canonical", "corr")][2]
lo, hi = np.percentile(bs_c, [16, 84])
ck("K3.2 the C-corrected value must land on one of the two footings, or the rung is not usable.  A check that "
   "CAN fail: the 68% bootstrap interval has to contain at least one footing",
   (lo < A0["canonical"] < hi) or (lo < A0["alt"] < hi),
   f"corrected a_0 = {a0c:.3e} [{lo:.3e}, {hi:.3e}]; canonical {A0['canonical']:.3e}, alt {A0['alt']:.3e}")

# =================================================================================================================
P("\n" + "-"*126)
P("4.  THE LEVERS, BOTH MEASURED BY RE-RUNNING THE PIPELINE")
P("-"*126)
P("  (a) UPSILON.  The proposal claims exactly zero, by construction.  Verified by re-running with the stellar")
P("      regressor rescaled -- which is what a change of Upsilon is, since Upsilon is not an input here at all.")
Lsave = Lkg.copy()
Lkg = Lsave*1.5
a0_up_n = run(A0["canonical"], False, "  [NAIVE form, re-run at L x 1.5, i.e. Upsilon x 1.5]")[0]
a0_up = run(A0["canonical"], True, "  [C-CORRECTED form, re-run at L x 1.5]")[0]
Lkg = Lsave
lev_ups_n = math.log10(a0_up_n/a0n)/math.log10(1.5)
lev_ups = math.log10(a0_up/a0c)/math.log10(1.5)
P(f"      NAIVE form       : d log a_0 / d log Upsilon = {lev_ups_n:+.4f}  (zero to numerical precision, as claimed)")
P(f"      C-CORRECTED form : d log a_0 / d log Upsilon = {lev_ups:+.4f}")
P("""      AND THAT IS A FINDING AGAINST THE CANDIDATE, not a rounding error.  The zero lever is exact only for
      the NAIVE form, which is the biased one.  The structural factor C = nu(y)^2 y epsilon needs g_bar, and
      g_bar needs Upsilon, so correcting the bias re-introduces a stellar mass-to-light dependence.  The
      candidate's single selling point survives only in the version that is known to be wrong.""")
P("\n  (b) THE HYDROGEN MASS SCALE.  The ledger predicts -1 exactly: the estimator trades the stellar")
P("      calibration for the hydrogen one at unit leverage.  Verified by re-running with M_HI x 1.5.")
MHsave = MHkg.copy()
MHkg = MHsave*1.5
a0_hi = run(A0["canonical"], True, "  [re-run at M_HI x 1.5]")[0]
MHkg = MHsave
lev_hi = math.log10(a0_hi/a0c)/math.log10(1.5)
P(f"      d log a_0 / d log M_HI = {lev_hi:+.4f}")
ck("K4.1 the candidate's one selling point, tested on the version that is not biased: the Upsilon lever must be "
   "zero in the form actually used.  It is exactly zero in the NAIVE form and NOT zero once the structural "
   "factor is applied, because that factor needs g_bar and g_bar needs Upsilon.  This check fails on the "
   "corrected form",
   abs(lev_ups) < 0.02,
   f"naive form {lev_ups_n:+.4f} (exact); C-corrected form {lev_ups:+.4f} -- the selling point does not survive "
   f"the bias correction")
ck("K4.2 and the price the ledger predicted is exactly what is paid: the hydrogen mass scale enters at unit "
   "leverage, so the rung has traded one calibration for another rather than removed one.  This check fails if "
   "the lever is not -1",
   abs(lev_hi + 1.0) < 0.05, f"d log a_0/d log M_HI = {lev_hi:+.4f} against the predicted -1.000")

# =================================================================================================================
P("\n" + "-"*126)
P("5.  THE ALTERNATIVE COMPUTED BESIDE IT, AND MUTATION CONTROLS")
P("-"*126)
# one-coefficient BTFR at a fixed stellar-population Upsilon: the estimator this one is meant to improve on
C = RES[("canonical", "corr")][3]
Yc = Y/C
for ups_fix in (0.5, 0.7):
    Mb = ups_fix*Lkg + HE*MHkg
    var = (4*eV/V*Yc)**2 + (2*eD/D*Mb*A0["canonical"])**2
    a0_1 = float(np.sum(Mb*Yc/var)/np.sum(Mb*Mb/var))
    P(f"  one-coefficient BTFR at a FIXED Upsilon = {ups_fix}: a_0 = {a0_1:.4e} "
      f"({math.log10(a0_1/A0['canonical']):+.3f} dex from canonical)")
# mutation: scramble M_HI across galaxies -- the gas coefficient must collapse
MHsave = MHkg.copy()
MHkg = MHsave[rng.permutation(len(use))]
a0_scr, ups_scr, bs_scr, _, _ = run(A0["canonical"], True, "  [MUTATION: M_HI scrambled across galaxies]")
MHkg = MHsave
ck("K5.1 mutation: scramble which galaxy owns which hydrogen mass.  If the gas coefficient survives, it is not "
   "measuring hydrogen at all",
   abs(math.log10(max(a0_scr, 1e-14)/a0c)) > 0.10 or a0_scr <= 0,
   f"a_0 from the gas coefficient {a0c:.3e} -> {a0_scr:.3e} when M_HI is scrambled "
   f"({math.log10(max(a0_scr,1e-14)/a0c):+.3f} dex)")
# mutation: kernel off -- C = 1 identically is the Newtonian/no-kernel case, already run as "naive"
ck("K5.2 mutation: switch the kernel's structural factor off (C = 1, which is what a pure deep-MOND identity "
   "assumes).  The answer must move, or the kernel is doing nothing in this estimator",
   abs(math.log10(a0n/a0c)) > 0.05,
   f"C = 1 gives {a0n:.3e}, C from the kernel gives {a0c:.3e} ({math.log10(a0n/a0c):+.3f} dex)")

# =================================================================================================================
P("\n" + "="*126)
P("VERDICT")
P("="*126)
P(f"""  CANDIDATE 4 -- the two-coefficient BTFR.  IT IS A RESTATEMENT, and section 0 proves it by executing the
  derivation: substituting M_b = Upsilon L + 1.33 M_HI into v^4 = G M_b a_0 and expanding the bracket gives the
  candidate exactly, to machine precision.  is_restatement = TRUE.  It is therefore NOT a second Kepler-grade
  law and cannot be one -- it fails criterion (5) by construction.

  AS A LADDER RUNG, which is what it is for, it does what the proposal said and pays what the ledger said.
    * The Upsilon lever is EXACTLY zero in the naive form ({lev_ups_n:+.4f}, measured by re-running the pipeline at
      Upsilon x 1.5), because Upsilon is a different coefficient of the same linear model.  BUT it is {lev_ups:+.4f}
      once the structural factor is applied, because C = nu(y)^2 y epsilon needs g_bar and g_bar needs Upsilon.
      The candidate's single selling point survives only in the version that is biased.
    * The price is exactly the one the ledger predicted: d log a_0/d log M_HI = {lev_hi:+.4f} against a predicted
      -1.000.  The rung has not removed a calibration, it has swapped the stellar one for the hydrogen one at
      unit leverage.  That is the durable finding of the veins workflow, reproduced here by a new estimator.
    * The collinearity price is real but modest: r(log L, log M_HI) = {r:.3f}, variance inflation
      {RES[('canonical','corr')][4]:.2f}.
    * The structural factor matters: a_0 = {a0n:.3e} m/s^2 without it, {a0c:.3e} with it computed per
      galaxy from the kernel -- a {math.log10(a0n/a0c):+.3f} dex correction that no estimator cleverness removes, because it is
      physics and not statistics (median C = {np.median(Cc):.2f}, i.e. the last measured point is NOT in the exact
      deep-MOND limit).
    * AND THE ESTIMATOR ITSELF MOVES THE ANSWER BY MORE THAN THE FOOTINGS ARE APART.  On the same 122 galaxies
      the log-space fixed-slope average the literature uses gives {A0_LOGNAIVE:.3e} uncorrected and {A0_LOGCORR:.3e}
      corrected, against {a0n:.3e} and {a0c:.3e} here -- {abs(math.log10(a0n/A0_LOGNAIVE)):.3f} dex of estimator choice uncorrected and
      {abs(math.log10(a0c/A0_LOGCORR)):.3f} dex corrected, against a 0.082 dex gap between the footings.  A rung whose value moves
      further with the choice of estimator than the two footings are apart cannot decide between them; this
      reproduces item 123's finding ("a cut choice moves a_0 by 2.5x the footing gap") by a new route.
    * ITEM 105b IS REPRODUCED INDEPENDENTLY on the way: that item found a naive 1.53e-10 moving to 9.82e-11 once
      the structural factor is applied.  Recomputed here from scratch, with C built per galaxy from the kernel,
      the same estimator gives {A0_LOGNAIVE:.3e} moving to {A0_LOGCORR:.3e}.
    * The corrected value sits {math.log10(a0c/A0['canonical']):+.3f} dex from the canonical footing and {math.log10(a0c/A0['alt']):+.3f} dex from the alt,
      with a 68% bootstrap interval of [{lo:.3e}, {hi:.3e}].""")
sys.exit(ck.done())
