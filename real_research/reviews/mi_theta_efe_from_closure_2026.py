#!/usr/bin/env python3
r"""mi_theta_efe_from_closure_2026.py -- DERIVE the EFE phase function theta(y) from the framework's
OWN inertia closure, instead of importing Milgrom's postulated theta forms.

WHY THIS MATTERS. The non-adiabatic relational sigma-spread is the ONE observable the corpus lists as
genuinely MG-IMPOSSIBLE: MI predicts a 6-13% spread across infall phase at matched external field,
while any modified-gravity realization (one shared field, responding only to the momentary a_ext)
predicts EXACTLY ZERO for any a0.  prep_2026/sigma_spread/GAP_STATEMENT.md freezes the estimator and
reports 6.2-14.1% over both footings -- but flags the magnitude as **theta-form UNVERIFIED**: the band
is produced by evaluating THREE POSTULATED forms
    theta = 2/(1+y^2),   e^{1-|y|},   e^{(1-|y|)/2}
with only theta(1)=1, "decreasing", theta(0)~few fixed (Milgrom 2022 arXiv:2208.07073v3 Eq 34).
Because the required carrier count scales as N ~ 1/s^4, the entire feasibility question -- an ELT
programme in 2032 versus never -- is set by a function nobody has derived. The framework's MI
completion has a UNIQUE inertia kernel, so it should not need to borrow theta at all. That is the door.

WHAT IS COMPUTED (no verdict hard-coded; the script exits 1 if any internal check fails):
  S1  The kernel on the oscillatory branch is UNIMODULAR (sympy-exact) -- the FREQUENCY channel
      carries zero amplitude modification and cannot source theta's y-dependence.
  S2  Theorem B (prep_2026/mi_fingerprint/KERNEL_THEORY.md) forces the inertia argument to be built
      from |a|^2, so the external field adds in QUADRATURE. Milgrom's Eq 34 adds it LINEARLY with a
      multiplying theta. The two differ even at theta == 1.
  S3  Under quadrature the whole y-dependence sits in the cross term 2 a_in.a_ex, whose coherence
      over the framework's own averaging window is DERIVED -- and with no free input, because
      Q = omega_in*T_w and y = omega_ex/omega_in combine to Q = (omega_ex*T_w)/y.
  S4  The y range real LSB cluster carriers actually span, computed from carrier physics.
  S5  The sigma-spread re-derived under the framework's own closure, on BOTH the max-min convention
      (how the banked band was quoted) and the population-RMS convention (what the frozen
      variance-excess estimator actually measures). Both footings.
  S6  The carrier-count consequence, and the SHAPE finding: the derived signal is non-monotonic in
      infall phase, which the frozen E4 sign statistic is not built to detect.

BOTH FOOTINGS (Carl's rule 4): canonical a0 = 9.36e-11 (rho_DE, cH_Lambda/Z), alt a0 = 1.13e-10
(rho_total, cH0). Physical accelerations held fixed in m/s^2; a0 is what varies.

Framework's OWN premises only -- nu(y)=sqrt(1+1/y), mu_fw(x)=(sqrt(1+4x^2)-1)/(2x). Never McGaugh's nu.
"""
from __future__ import annotations
import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

C_LIGHT = 2.99792458e8
KPC     = 3.0856775814913673e19
GYR     = 3.1556952e16
T_AGE   = 13.797 * GYR
FOOTINGS = [("canonical rho_DE cH_Lambda/Z", 9.36e-11), ("alt rho_total cH0", 1.13e-10)]

# frozen fiducial from prep_2026/sigma_spread (physical, m/s^2, defined against the canonical a0)
A0_REF   = 9.36e-11
A_IN_FID = 0.3 * A0_REF
A_EX_FID = 2.0 * A0_REF
Y_SPEC   = [0.05, 0.5, 1.0, 1.5]

THETAS_POSTULATED = [("rational 2/(1+y^2)", lambda y: 2.0 / (1.0 + y * y)),
                     ("exp e^{1-|y|}",      lambda y: np.exp(1.0 - np.abs(y))),
                     ("exp e^{(1-|y|)/2}",  lambda y: np.exp((1.0 - np.abs(y)) / 2.0))]


def mu_fw(x):
    """Framework's forward interpolation; inverse of nu(y)=sqrt(1+1/y)."""
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def sigma_of(C, a_in, a_ex, a0):
    """sigma ~ sqrt(boost) with the framework's QUADRATURE argument and cross-term coherence C."""
    x = np.sqrt(a_in**2 + a_ex**2 + 2.0 * a_in * a_ex * np.asarray(C, float)) / a0
    return np.sqrt(1.0 / mu_fw(x)), x


def main() -> int:
    banner("S1. The kernel's FREQUENCY channel cannot source theta -- unimodular on the live branch")
    # On the oscillatory branch z = -w^2 + i0 with w = omega c/a0 >= 1/2, the retarded boundary value
    # of K(z) = (sqrt(1+4z)-1)/(2 sqrt z) is (sqrt(4w^2-1) + i)/(2w).  Give sympy the radical as a
    # positive symbol W with W^2 = 4w^2 - 1, so it never has to branch-resolve atan2 on 4w^2-1.
    w, W = sp.symbols('w W', positive=True)
    Kb = (W + sp.I) / (2 * w)
    mod2 = sp.simplify(sp.expand((sp.Abs(Kb) ** 2).rewrite(sp.re)).subs(W**2, 4 * w**2 - 1))
    mod2 = sp.simplify(((W**2 + 1) / (4 * w**2)).subs(W**2, 4 * w**2 - 1))
    print(f"  K(-w^2+i0) = (sqrt(4w^2-1) + i)/(2w)      [retarded branch]")
    print(f"    Re K = sqrt(4w^2-1)/(2w) = sqrt(1 - 1/(4w^2)),   Im K = 1/(2w)")
    print(f"    |K|^2 = (W^2+1)/(4w^2) with W^2 = 4w^2-1  ->  {mod2}   (sympy-exact)")
    check(sp.simplify(mod2 - 1) == 0, "the kernel is EXACTLY unimodular on the oscillatory branch")
    # and it is exactly exp(i phi) with sin phi = 1/(2w)
    phi = sp.asin(1 / (2 * w))
    lhs_re = sp.simplify(sp.cos(phi) - sp.sqrt(1 - 1 / (4 * w**2)))
    lhs_im = sp.simplify(sp.sin(phi) - 1 / (2 * w))
    check(lhs_re == 0 and lhs_im == 0,
          "K = exp[i*arcsin(a0/2c omega)] -- a PURE PHASE LAG, zero amplitude modification")
    print("  So an amplitude-channel theta(y) would need |K| to vary with frequency. It cannot.")
    for fname, a0 in FOOTINGS:
        om_b = a0 / (2 * C_LIGHT)
        print(f"    {fname:30s}: branch point omega_b = a0/2c = {om_b:.3e} 1/s "
              f"-> period {2*np.pi/om_b/GYR:7.1f} Gyr")
    print("  Every bound orbit therefore sits at w >> 1/2, deep inside the unimodular regime. The")
    print("  only frequency-dependent amplitude effect is second order in the phase lag:")
    print(f"  {'carrier':<26s} {'omega (1/s)':>12s} {'w=omega c/a0':>13s} {'phi (rad)':>11s} {'1-cos phi':>11s}")
    amp = []
    for nm, v, R in [("cluster member orbit", 1000e3, 1.0e3 * KPC),
                     ("LSB dwarf internal", 20e3, 1.5 * KPC)]:
        om = v / R
        ww = om * C_LIGHT / A0_REF
        ph = np.arcsin(min(1.0, 1.0 / (2 * ww)))
        amp.append(1 - np.cos(ph))
        print(f"  {nm:<26s} {om:12.3e} {ww:13.3e} {ph:11.3e} {1-np.cos(ph):11.3e}")
    worst = max(amp)
    check(worst < 1e-4, f"frequency channel bounds any theta y-dependence at <= {worst:.1e}, ~4-5 "
                        f"orders below the banked 6-13% spread")

    banner("S2. Theorem B forces QUADRATURE addition, not Milgrom's linear Eq-34 ansatz")
    print("  KERNEL_THEORY.md Theorem B (exact for any timelike worldline, curved space included):")
    print("      u_mu Box_u u^mu = -|a|^2   =>   <Box_u>_u = +|a|^2   exactly")
    print("  so the inertia argument is built from |a|^2, and the total field enters as")
    print("      |a_in + a_ex|^2 = a_in^2 + a_ex^2 + 2 a_in.a_ex        (QUADRATURE + cross term)")
    print("  Milgrom's EFE ansatz (arXiv:2208.07073v3 Eq 34) instead posits")
    print("      A = a_in + a_ex * theta(omega_ex/omega_in)              (LINEAR in a_ex)")
    print("  They differ even at theta == 1. Size of that structural gap at the frozen fiducial:")
    a_lin, a_quad = A_IN_FID + A_EX_FID, np.hypot(A_IN_FID, A_EX_FID)
    for fname, a0 in FOOTINGS:
        b_lin, b_quad = 1.0 / mu_fw(a_lin / a0), 1.0 / mu_fw(a_quad / a0)
        print(f"    {fname:30s} linear x={a_lin/a0:5.2f} boost={b_lin:6.3f} | "
              f"quadrature x={a_quad/a0:5.2f} boost={b_quad:6.3f} | "
              f"sigma differs {100*(np.sqrt(b_quad/b_lin)-1):+6.2f}%")
    check(a_quad < a_lin, "quadrature gives a strictly SMALLER argument than linear addition")
    print("  This is the load-bearing difference. The LINEAR form is what lets theta multiply a_ex")
    print("  and swing the argument by ~3x across infall phase. Under quadrature nothing multiplies")
    print("  a_ex at all, and the y-dependence is forced into the cross term -- computed next.")

    banner("S3. The cross-term coherence, DERIVED with no free input")
    print("  a_in oscillates at omega_in, a_ex varies at omega_ex (the member's cluster orbit); their")
    print("  dot product beats at omega_in -/+ omega_ex. Averaged over the closure window T_w the")
    print("  difference beat carries the standard coherence factor")
    print("      C(y) = sinc[ Q (1-y)/2 ],   Q = omega_in * T_w,   y = omega_ex/omega_in")
    print("  T_w is supplied by the framework itself: the kernel memory tau_mem = 2c/a0, capped by")
    print("  the age of the universe. AND Q NEEDS NO SEPARATE INPUT -- since omega_in = omega_ex/y,")
    print("      Q(y) = (omega_ex * T_w) / y,   so C depends only on the DIMENSIONLESS  P = omega_ex*T_w")
    print("      C(y) = sinc[ P (1-y) / (2y) ]      (P = cluster orbits per memory window, x 2pi)")
    Pvals = {}
    for fname, a0 in FOOTINGS:
        tau_mem = 2 * C_LIGHT / a0
        T_w = min(tau_mem, T_AGE)
        om_ex = 1000e3 / (1.0e3 * KPC)
        P = om_ex * T_w
        Pvals[fname] = P
        print(f"    {fname:30s} tau_mem={tau_mem/GYR:7.1f} Gyr, T_w={T_w/GYR:6.2f} Gyr (age-capped)"
              f"  ->  P = {P:6.2f}")
    check(all(2 * C_LIGHT / a0 > T_AGE for _, a0 in FOOTINGS),
          "tau_mem exceeds the age of the universe on both footings, so T_w = t_age")

    def coherence(y, P):
        y = np.asarray(y, float)
        u = P * (1.0 - y) / (2.0 * y)
        return np.where(np.abs(u) < 1e-12, 1.0, np.sin(u) / np.where(u == 0.0, 1.0, u))

    Pc = Pvals["canonical rho_DE cH_Lambda/Z"]
    print(f"\n  Coherence across infall phase (canonical, P = {Pc:.2f}):")
    print(f"  {'y':>6s} {'Q(y)':>9s} {'C(y)':>9s}")
    for y in [0.05, 0.1, 0.25, 0.5, 0.8, 1.0, 1.2, 1.5]:
        print(f"  {y:6.2f} {Pc/y:9.1f} {float(coherence(y, Pc)):9.4f}")
    print("  C is NOT the monotone-decreasing theta Milgrom posits: it is small at low y, PEAKS AT")
    print("  y = 1, and falls again above it. The peak is where the internal and orbital frequencies")
    print("  lock, so the cross term stops averaging away. That is a qualitatively different shape.")
    c_at_1 = float(coherence(1.0, Pc))
    c_low = float(coherence(0.05, Pc))
    check(c_at_1 > abs(c_low), "coherence peaks at y=1 rather than at y->0 (opposite of theta's shape)")

    banner("S4. The y range real LSB cluster carriers actually span -- computed")
    print("  y = omega_ex/omega_in, omega_ex = v_cl/R_cl (orbit about cluster), omega_in = sigma_in/R_e.")
    print("  Carriers per frozen spec E1: mu_0,r fainter than 24 mag/arcsec^2, R_e >= 1 kpc.")
    ys = []
    for sig, Re in [(30e3, 1.0 * KPC), (20e3, 1.5 * KPC), (10e3, 3.0 * KPC), (8e3, 5.0 * KPC)]:
        for vcl, Rcl in [(1200e3, 0.5e3 * KPC), (1000e3, 1.0e3 * KPC), (700e3, 2.0e3 * KPC)]:
            ys.append((vcl / Rcl) / (sig / Re))
    y_lo, y_hi = min(ys), max(ys)
    print(f"  y spans {y_lo:.4f} to {y_hi:.4f} across that carrier x cluster grid")
    print(f"  frozen spec assumes y in [{min(Y_SPEC)}, {max(Y_SPEC)}]")
    check(y_lo < min(Y_SPEC) and y_hi >= max(Y_SPEC) * 0.99,
          "real carriers DO span the spec's phase range (it reaches y~1.5 for the most diffuse "
          "carriers at small cluster radii, and extends BELOW the spec floor) -- the phase lever "
          "is real, so the spread question is settled by amplitude, not by range")

    banner("S5. The sigma-spread re-derived under the framework's own closure, both footings")
    print("  (i) BANKED route -- Milgrom's LINEAR ansatz with the three postulated theta forms over")
    print("      the spec's four y values, reproduced as the like-for-like baseline.")
    banked = []
    for fname, a0 in FOOTINGS:
        sp_f = []
        for tname, th in THETAS_POSTULATED:
            b = np.array([1.0 / mu_fw((A_IN_FID + A_EX_FID * th(y)) / a0) for y in Y_SPEC])
            s = np.sqrt(b)
            sp_f.append((s.max() - s.min()) / s.mean())
        banked.append((min(sp_f), max(sp_f)))
        print(f"      {fname:30s} spread {min(sp_f)*100:5.1f}% - {max(sp_f)*100:5.1f}%")
    b_lo = min(v[0] for v in banked); b_hi = max(v[1] for v in banked)
    print(f"      both-footing band {b_lo*100:.1f}% - {b_hi*100:.1f}%   (GAP_STATEMENT: 6.2-14.1%)")
    check(0.055 < b_lo < 0.075 and 0.11 < b_hi < 0.15, "the banked band reproduces from its own inputs")

    print("\n  (ii) DERIVED route, max-min convention (same convention as the banked band above),")
    print("       evaluated on the spec's y range so the comparison is not a range artifact.")
    y_dense = np.linspace(min(Y_SPEC), max(Y_SPEC), 2000)
    der_mm = []
    for fname, a0 in FOOTINGS:
        s, x = sigma_of(coherence(y_dense, Pvals[fname]), A_IN_FID, A_EX_FID, a0)
        der_mm.append((s.max() - s.min()) / s.mean())
        print(f"      {fname:30s} x in [{x.min():.4f},{x.max():.4f}] -> spread {der_mm[-1]*100:.3f}%")
    d_mm = max(der_mm)

    print("\n  (iii) DERIVED route, POPULATION-RMS convention -- what the frozen estimator actually")
    print("        measures (E4: excess VARIANCE of FJ residuals). Monte Carlo over the carrier")
    print("        population; two priors on y, reported both ways, neither tuned.")
    rng = np.random.default_rng(20260730)
    NMC = 200000
    der_rms = {}
    for prior in ("log-uniform in y", "uniform in y"):
        for fname, a0 in FOOTINGS:
            if prior.startswith("log"):
                ysamp = np.exp(rng.uniform(np.log(y_lo), np.log(y_hi), NMC))
            else:
                ysamp = rng.uniform(y_lo, y_hi, NMC)
            s, _ = sigma_of(coherence(ysamp, Pvals[fname]), A_IN_FID, A_EX_FID, a0)
            der_rms[(prior, fname)] = s.std() / s.mean()
            print(f"      {prior:18s} {fname:30s} RMS spread = {der_rms[(prior,fname)]*100:.4f}%")
    d_rms = max(der_rms.values())
    print(f"\n  DERIVED spread: {d_mm*100:.3f}% (max-min)   {d_rms*100:.4f}% (population RMS, worst prior)")
    print(f"  BANKED  band  : {b_lo*100:.1f}% - {b_hi*100:.1f}%")
    print(f"  Suppression factor vs banked low end: {b_lo/d_mm:.1f}x (max-min), {b_lo/d_rms:.0f}x (RMS)")
    check(d_mm < b_lo, f"derived max-min spread ({d_mm*100:.2f}%) is below the banked band's low end "
                       f"({b_lo*100:.1f}%)")
    check(d_rms < d_mm, "the population-RMS spread is smaller than max-min, as it must be -- the "
                        "coherent enhancement lives near y=1, not across the whole population")

    print("\n  (iv) ROBUSTNESS TO THE WINDOW SHAPE -- honesty check on my own modelling choice.")
    print("       The sinc above comes from a BOXCAR average over T_w. That is MY choice, not the")
    print("       framework's: the kernel's memory carries a Herglotz weight, and I capped it at")
    print("       t_age by hand. So re-do it with an EXPONENTIAL memory (Lorentzian coherence,")
    print("       C = 1/(1+(P(1-y)/y)^2)) and with a Gaussian window, and see what actually moves.")
    windows = {
        "boxcar  -> sinc": lambda yy, P: coherence(yy, P),
        "exponential -> Lorentzian": lambda yy, P: 1.0 / (1.0 + (P * (1.0 - yy) / yy) ** 2),
        "Gaussian -> Gaussian": lambda yy, P: np.exp(-0.5 * (P * (1.0 - yy) / (2.0 * yy)) ** 2),
    }
    print(f"       {'window':<28s} {'max-min':>9s} {'pop-RMS':>9s} {'peak y':>7s}")
    rob = {}
    for wname, wfun in windows.items():
        P = Pvals["canonical rho_DE cH_Lambda/Z"]
        s_d, _ = sigma_of(wfun(y_dense, P), A_IN_FID, A_EX_FID, A0_REF)
        ysamp = np.exp(rng.uniform(np.log(y_lo), np.log(y_hi), NMC))
        s_p, _ = sigma_of(wfun(ysamp, P), A_IN_FID, A_EX_FID, A0_REF)
        mm = (s_d.max() - s_d.min()) / s_d.mean()
        rms = s_p.std() / s_p.mean()
        rob[wname] = (mm, rms)
        print(f"       {wname:<28s} {mm*100:8.3f}% {rms*100:8.4f}% {y_dense[np.argmax(wfun(y_dense,P))]:7.3f}")
    mm_all = [v[0] for v in rob.values()]
    check(max(mm_all) < b_lo,
          f"EVERY window shape gives a max-min spread ({min(mm_all)*100:.2f}-{max(mm_all)*100:.2f}%) below "
          f"the banked low end ({b_lo*100:.1f}%) -- the suppression is not a boxcar artifact")
    check(max(mm_all) / min(mm_all) < 3.0,
          f"window choice moves the amplitude by only {max(mm_all)/min(mm_all):.2f}x, so the ORDER of the "
          f"result is robust even though the exact shape is not derived")
    print("       WHAT IS ROBUST: quadrature-vs-linear (Theorem B, exact); the cross term being the")
    print("       only y-channel (algebraic); suppression ~1/Q for incommensurate frequencies and a")
    print("       peak at commensurability (generic for ANY averaging window). WHAT IS NOT DERIVED:")
    print("       the precise line shape, and hence the exact peak width. Quoted accordingly.")

    banner("S6. Consequences -- carrier count, and the SHAPE the frozen estimator is not built for")
    print("  Estimator (frozen, GAP_STATEMENT S3): z ~ (s p)^2 / (eps_eff^2 sqrt(2/N))")
    print("  => N(3sigma) = 2 (3 eps_eff^2 / (s p)^2)^2,  so N scales as s^-4.")
    p = 0.6
    print(f"  {'spread s':>22s} {'eps_meas':>9s} {'eps_FJ':>7s} {'N(3 sigma)':>13s}")
    N = {}
    for label, s in [("banked hi", b_hi), ("banked lo", b_lo),
                     ("DERIVED max-min", d_mm), ("DERIVED pop-RMS", d_rms)]:
        for eps_m, eps_fj in ((0.25, 0.15), (0.10, 0.10)):
            eps = np.hypot(eps_m, eps_fj)
            n3 = 2.0 * (3.0 * eps**2 / (s * p) ** 2) ** 2
            N[(label, eps_m)] = n3
            print(f"  {label:>22s} {s*100:6.3f}% {eps_m:9.2f} {eps_fj:7.2f} {n3:13.3e}")
    infl_mm = N[("DERIVED max-min", 0.10)] / N[("banked lo", 0.10)]
    infl_rms = N[("DERIVED pop-RMS", 0.10)] / N[("banked lo", 0.10)]
    print(f"\n  At the ELT tier (eps_meas=eps_FJ=0.10) the carrier requirement inflates by")
    print(f"    {infl_mm:.3e}x on the max-min reading   -> N ~ {N[('DERIVED max-min',0.10)]:.2e}")
    print(f"    {infl_rms:.3e}x on the pop-RMS reading   -> N ~ {N[('DERIVED pop-RMS',0.10)]:.2e}")
    print(f"  against ~{N[('banked lo',0.10)]:.0f} carriers on the banked band. For scale, 4MOST-CHANCES")
    print( "  delivers ~300k spectra total across 150 clusters, and only a small LSB subset of those")
    print( "  would ever have resolved internal dispersions at the 10% tier.")
    check(N[("DERIVED pop-RMS", 0.10)] > 3.0e5,
          f"on the estimator's own (RMS) convention the requirement exceeds the FULL CHANCES spectrum "
          f"budget (~3e5) even before the LSB/resolved-sigma cut")

    print("\n  SHAPE FINDING (independent of the amplitude, and arguably the more useful half).")
    print("  The frozen E4 SIGN statistic contrasts first-infall against settled members and expects")
    print("  a MONOTONE trend in infall phase. The derived coherence is NOT monotone: it peaks at")
    print("  y = 1 and declines on both sides. A monotone two-class contrast integrates across that")
    print("  peak and partially cancels. Quantified -- two-class difference vs the full range:")
    for fname, a0 in FOOTINGS:
        P = Pvals[fname]
        lowy = np.linspace(y_lo, 0.5, 800)
        hiy = np.linspace(0.5, y_hi, 800)
        s_lo, _ = sigma_of(coherence(lowy, P), A_IN_FID, A_EX_FID, a0)
        s_hi, _ = sigma_of(coherence(hiy, P), A_IN_FID, A_EX_FID, a0)
        two_class = abs(s_hi.mean() - s_lo.mean()) / np.r_[s_lo, s_hi].mean()
        print(f"    {fname:30s} two-class |diff| = {two_class*100:.4f}%  vs max-min "
              f"{der_mm[FOOTINGS.index((fname, a0))]*100:.3f}%")
    print("  So the pre-registered sign statistic is testing for a shape the framework's own closure")
    print("  does not produce. A y-RESOLVED statistic (bin carriers by omega_ex/omega_in and look for")
    print("  a peak at 1) is strictly better matched, and is free to adopt -- it needs no new data,")
    print("  only a different binning of the same carriers.")

    banner("VERDICT")
    print(f"  1. theta need not be borrowed, and the kernel cannot supply it: |K| = 1 exactly on the")
    print(f"     oscillatory branch, so the frequency channel offers <= {worst:.0e} of amplitude change.")
    print( "  2. Theorem B forces the external field in through |a|^2 -- QUADRATURE. Milgrom's Eq 34")
    print( "     adds it linearly with a multiplying theta. Under this framework's own closure there")
    print( "     is no slot for a multiplying phase function at all.")
    print(f"  3. The surviving y-dependence is the cross-term coherence C(y) = sinc[P(1-y)/2y] with")
    print(f"     P = omega_ex*t_age ~ {Pc:.1f}, and it needs NO free input.")
    print(f"  4. Re-derived spread: {d_mm*100:.2f}% (max-min) / {d_rms*100:.3f}% (population RMS) against the")
    print(f"     banked {b_lo*100:.1f}-{b_hi*100:.1f}%. Suppression {b_lo/d_mm:.0f}x to {b_lo/d_rms:.0f}x.")
    print(f"  5. Carrier requirement at the ELT tier: ~{N[('DERIVED pop-RMS',0.10)]:.1e} rather than "
          f"~{N[('banked lo',0.10)]:.0f}.")
    print( "     The GAP_STATEMENT reopen conditions (ELT ~2032, or an FJ floor <= 0.15) were priced")
    print( "     against a spread the framework's own closure does not deliver, so the 2032 window is")
    print( "     NOT the real gate. This narrows on THEORY grounds, before any data argument.")
    print( "  6. The frozen E4 sign statistic tests a monotone trend; the derived signal peaks at y=1.")
    print( "     Re-binning by omega_ex/omega_in is a free improvement to the pre-registration.")
    print()
    print( "  WHAT IS *NOT* CLAIMED. This does not say the channel is impossible in principle -- the")
    print( "  MG contrast is untouched (MG remains exactly zero, the framework remains nonzero, so the")
    print( "  signature is still MG-impossible in principle). Nor is it 'unreachable at any tier': the")
    print( "  requirement is large but finite. An earlier draft of this script asserted it exceeded the")
    print( "  number of galaxies in the observable universe; that was wrong by many orders and its own")
    print( "  check caught it. The defensible statement is narrower: at the derived amplitude the")
    print( "  observable is out of reach of every survey now on the books, including the ELT programme")
    print( "  the gap statement was written to justify.")
    print()
    print( "  WHAT WOULD OVERTURN THIS (falsifiable, not defended):")
    print( "   (a) A different closure. Theorem B fixes the first MOMENT exactly, but KERNEL_THEORY.md")
    print( "       Finding C records the off-circular TIME-WEIGHTING as a free O(1) choice. A weighting")
    print( "       that both reproduces the RAR and restores a LINEAR a_ex channel would bring the")
    print( "       banked band back. None is known, and the RAR constraint is severe.")
    print( "   (b) Carriers piled up near y = 1. The coherence peak is real; a population concentrated")
    print( "       there gets the full cross term. That is a checkable claim about cluster orbital")
    print( "       structure, not a free parameter -- and it is what the re-binned statistic tests.")
    print( "   (c) A much longer effective averaging window than t_age, which would raise P and")
    print( "       sharpen the peak; or a much shorter one, which would broaden it toward full")
    print( "       coherence. T_w = min(2c/a0, t_age) is the framework's own choice, not a knob.")
    print()
    print( "  PROVENANCE. Milgrom's theta is itself a modified-inertia construction and was the right")
    print( "  thing to try first; this is not a criticism of it. The finding is that THIS framework's")
    print( "  completion makes a stricter choice than Eq 34, and the corpus had been quoting Eq 34's")
    print( "  consequences as its own.")
    print()
    print( "  ONE CITATION CAVEAT, STATED RATHER THAN PAPERED OVER. The LINEAR form 'A = a_in +")
    print( "  a_ex*theta(y)' is taken from how this repo's own files record Milgrom 2022 Eq 34")
    print( "  (prep_2026/sigma_spread/rederive_spread_and_power.py and GAP_STATEMENT.md S1). The")
    print( "  primary source was NOT re-read while producing this script. If Eq 34 is in fact a vector")
    print( "  or quadrature statement, then S2's structural gap narrows or vanishes -- but the load-")
    print( "  bearing result does not depend on it: S1 (no amplitude in the frequency channel), S3")
    print( "  (the cross term is the only y-channel, suppressed ~1/Q and peaked at commensurability),")
    print( "  and S5 (the repriced spread) are all internal to THIS framework's closure and stand on")
    print( "  Theorem B alone. Verifying Eq 34 against the primary source is a cheap open item.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
