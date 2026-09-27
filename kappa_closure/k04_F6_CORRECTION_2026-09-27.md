# Correction to k04 (2fb80ca12): check F6 does not establish stability

Verified independently by review lane XR31
(`real_research/cross_thread_review_2026_09_26/XR31_k04_f6_stability.py`, with its README; first flagged by XR20 T2f).
k04's own files are left unchanged; this note fixes the record forward.

**What F6 tests.** F6's Z_eff = Z + (2 − K_B)β²(sΔ − j)/(8π) is the flux's secant stiffness Π/q. For every kernel
that is convex in Y it is ≥ Z, because F = sΔ − j = YJ_Y − J ≥ 0. F6 therefore cannot fail, and so it does not test
stability. The test is the slaved scalar's longitudinal coefficient, C_L,eff = dg_N/dg_φ at fixed Π.

**The result, on k04's own kernel and couplings** (F3's Z = 8β²):
- The slaved scalar force peaks at g_N = 2.385 a0 (2.403 at K_B = 0.25; 2.323 with κ tied on the alt footing).
- It then falls linearly to zero at the switch-off, 155.2 a0 (177.4; 106.3).
- So C_L,eff < 0 on the whole band (−238.6 at 20 a0), and the static scalar equation is not elliptic there.
- Longitudinal perturbations grow at a rate proportional to k: ω² = −0.86 (ck)² in the chain root's quadratic form at
  λ = 1.
- Three independent routes agree on the fold to about 1e-12.

**What the band covers:**
- 17% / 15% of SPARC points (Υ = 0.7, canonical / alt);
- a shell from about 639 to 5154 AU around every solar-mass star;
- wide binaries at 2–5 kAU.

**Corrected reading.** "stable (F6)" should read: "UNSTABLE for 2.39 < g_N/a0 < 155: the four-form's feedback tilts
the saturated kernel's flat branch downward."

**What stands and what doesn't:**
- F1–F2 are unaffected.
- F3's RAR shift (< 0.002 dex) stands below 2.39 a0. Its rows above that are an unstable static solution.
- F4: the planets sit in the switched-off core. "Inside 205 AU" should read about 639 AU, where g_N = 155 a0 around
  1 M☉ with k04's own a0.
- F5: the 2 kAU wide-binary shift (δγ_v = −0.019 / −0.015) is computed on an unstable solution and is not a
  prediction.
- What F6 does establish: the flux equation has exactly one root, with 0 < a0_loc ≤ a0, at every g_N.

**Where this also appears.**
- PAPER6 (`qwen_claude_field_theory/papers_2026/PAPER6_kappa_no_go_2026.tex`, DOI 10.5281/zenodo.22559892)
  states "the effective flux stiffness stays positive (F6)", "Inside 205 AU", and the F5 wide-binary shift.
- The same variant is recorded (not registered) in Amendment 11 of the Gaia DR4 pre-registration.
- Any erratum or new version of the paper, and any pre-registration amendment, is the author's decision. Neither file
  has been edited.
