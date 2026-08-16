REFINE round 1 of interp_0027 (seed_0027) -- graded NEAR-MISS, refine-once only
(trials = 2; faces its OWN blind referee; failed revision = DEAD-FINAL)

Read ONLY ref_0027.md + interp_0027.md. No catalog search -> no FDR surface.
All quantities dimensionless -> dual footings 9.3619e-11 / 1.1279e-10 are N/A here.
kappa = 1/2 is a FIT (0.551 +/- 0.043), NOT derived; neither 29->206.77 nor the
Yukawa bound is claimed DERIVED. CONVENTION-grade matches are not hits.

========================================================================
THE FIX  (each sub-fix justified by FOOTING/STRUCTURE, NOT "make 206.77 come out")
========================================================================

FIX alpha -- the Yukawa leg is read at the m_t footing, not m_Z.
  Justification (footing/physics, value-independent): the top Yukawa y_t(m_t)
  is the on-shell saturation value at the scale where m_t >> m_Z forces the
  coupling to its maximal, scheme-independent, self-consistent value; the
  MSbar value at m_Z (~0.94) is a running, off-shell quantity that is not the
  saturation point. The kernel enters as y_t,sat = sqrt(kappa*), evaluated at
  the footing where the coupling saturates (m_t). This chooses the footing on
  physical grounds (saturation = maximal, on-shell, scheme-independent), NOT on
  "which footing matches the measured number."
  HONEST FLAG: at m_t, y_t(m_t)^2 = 0.74^2 = 0.5476 ~= the FIT 0.551. Reading the
  saturation at m_t therefore RESURFACES the fit at a different footing; it does
  NOT constitute a derivation. It is recorded as the pre-registered ALTERNATE
  kappa* = 0.551 (a FIT), not as a value obtained from structure.

FIX beta -- the 29 -> 206.77 leg is GIVEN a specified fixed-point RG structure,
  not a free function. We take the MINIMAL fixed-point RG: a single relevant
  eigenvalue kappa* governing one beta function,
        dC/dln(mu) = kappa* * C            (one-loop; fixed point C* = 0,
                                            eigenvalue = kappa*)
  Solution C(mu_ell) = C(mu_grav) * (mu_ell/mu_grav)^kappa*, so
        206.77 / 29 = r^kappa*    with r = mu_ell/mu_grav the footing ratio,
        => kappa*_flow = ln(206.77/29)/ln(r) = 1.9645 / ln(r).
  Justification (structural, value-independent): the one-loop single-eigenvalue
  running is the minimal fixed-point structure -- parameter-free beyond the
  eigenvalue kappa* and the footing ratio r. Choosing it is a STRUCTURAL
  minimalism (the simplest RG that carries a fixed point between two footings),
  NOT a choice tuned to land 206.77. r is a framework/footing-invariant input
  (the ratio of the two footing definitions), NOT a free parameter fit to 206.77.
  If r has no footing-defined value, the leg is UNDERDETERMINED and the idea
  routes to DISCARD (no specified flow connects 29 to 206.77 without a free r).

========================================================================
THE "SAME kappa*" REQUIREMENT  (the crux the near-miss did not meet)
========================================================================
The wildcard holds ONLY if the eigenvalue of this one beta function is the SAME
number on both legs. Two legs, one beta, one eigenvalue:
  kappa*_flow = 1.9645 / ln(r)                     (from 29 -> 206.77)
  kappa*_yuk  = y_t(m_t)^2 = 0.5476 ~ 0.551(fit)   (from y_t,sat = sqrt(kappa*)
                                                 at the m_t footing, FIX alpha)
PASS iff kappa*_flow == kappa*_yuk (within the tolerance below). This is the
proof that kappa* is ONE number, not two fits.

========================================================================
FRESH PRE-REGISTERED TEST + TOLERANCE
========================================================================
1. Fix the structure a priori: one-loop B above; footprint r a footing input
   (do NOT refit r or kappa* per bullet).
2. Compute kappa*_flow = 1.9645/ln(r) from the 29 -> 206.77 leg.
3. Compute kappa*_yuk  = y_t(m_t)^2 from the m_t-footing Yukawa leg (FIX alpha).
4. PASS  iff |kappa*_flow - kappa*_yuk| / kappa*_yuk <= 0.10  (10% tol;
   the idea's pre-registered "within 2x tol" = 20% is the NEAR-MISS band only --
   a 10%-20% miss is NOT a pass, it is a recorded near-miss).
5. If r has no footing value -> the 29->206.77 leg is underdetermined ->
   DISCARD (no parameter-free flow). This is a SUCCESS outcome, not a failure.

HONEST EXPECTATION (not a test, just a pre-registered note): to pass, r must be
~35.6 (ln r = 1.9645/0.55 = 3.57). No footing ratio of ~35.6 is known in the
framework, so the "same kappa*" is very likely NOT established -> the revision
fails its own blind referee -> DEAD-FINAL. That null is the disciplined result.

========================================================================
KILLS (carried from ref_0027, reaffirmed)
========================================================================
-- kappa*_flow != kappa*_yuk (two distinct numbers) => wildcard fails => REFUTED.
-- r has no footing value (needs a 2nd free parameter) => overfit => DISCARD.
-- kappa*_yuk = 0.55 is the FIT resurfaced, not derived => if the only "match"
   is the fit, the idea adds no derivation => NULL/DISCARD.
-- any footing-dependence of C(mu_ell)/C(mu_grav) => "invariant" false => REFUTED.
-- counting a CONVENTION-grade match as a hit is not allowed.

trials = 2 (refined once; Bonferroni applies)

NOTE: this is a dimensional/structural conjecture pending its OWN blind referee.
No value here is claimed DERIVED; kappa = 1/2 (0.551 +/- 0.043) stays a FIT.
