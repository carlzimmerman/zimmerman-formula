# W4-23: the Gauss-law (fixed-flux) rescue of the sign wall (frozen criteria, committed alone)

**Status: FROZEN 2026-10-21, before any W4-23 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Model and audit lane, continuing W4-22's "what would rescue it". It also answers W4-08's declared route R3: does a Gauss-law
constraint evade stable-auxiliary concavity? **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095; not used). Not theory
closed.

## Inherited (paths)

- **I-a.** The concavity obstruction (`W4_08_positive_mond_amplitudes/formal/NEUTRAL_CURRENT_TEST.md`):
  - if E(s) = inf_x[V(x) + sF(x)], with s = h² and an s-independent admissible set, then E is concave in s;
  - so E = E(0) + C₂s + C₃s^{3/2} with C₃ > 0 is impossible.
- **I-b.** W4-08's constrained branch (`W4_08_positive_mond_amplitudes/PROOF.md` §constrained):
  - exact g = g_N + √(a₀g_N), with the auxiliary at a **maximum** of U;
  - a kinetic regulator gives the auxiliary mass² = −A_c/η < 0;
  - a vacuum from the same auxiliary restores a quadratic infrared response; R = 8ε₀/(9γb³) with ε₀ free.
- **I-c.** The A1 dictionary (W4-04).
- **I-d.** The excluded class X15: the unstiffened QUMOND/BIMOND vacuum class, where Cassini gives κ < 0.17 at 2σ (p58,
  K064).

## Claims (hand expectations)

- **L1. Duality.** For any static law g = ν(g_N/a₀)·g_N, with μ(g/a₀) = 1/ν at corresponding points:
  - the fixed-potential functional E(s), s = g², has dE/ds = μ/2;
  - the fixed-flux functional U(t), t = g_N², has dU/dt = ν/2.

  So MOND (μ increasing, ν decreasing) ⇔ E strictly convex in s ⇔ U strictly concave in t.

  **Corollary:** I-a forbids **every** MOND interpolation for a stable s-affine medium, not just the deep cubic; such media
  give μ non-increasing ("anti-MOND"). Checked for simple μ, the n = 2 standard μ and the additive law.
- **L2. Minimal fixed-flux medium.** U(t) = ε + t/(2K) + inf_{x>0}[a x^{−n} + b t x^{n−2}]. One quantum per n-cell plus a
  flux coupling ∝ x^{n−2} gives the deep-MOND power t^{n/(2(n−1))} exactly for n = 3, 4, 5. At n = 3 this is t^{3/4}, the law
  g = g_N + √(a₀g_N). No exponent is tuned; the dimension fixes p = n and q = n − 2.
- **L3. Stability is set by the sign of the field sector, not by the picture.**
  - At fixed x, U = V + |D|²F is Legendre-dual to W = |h|²/(4F) − V. **Flux-affine is field-affine.**
  - **(a) Electrostatic (Gauss-law) sign:** the fixed-charge energy ∫U(D, x) is minimized. L2's MOND branch (min over x of
    U) is stable for every perturbation direction. The x-stiffness after minimizing δD under Gauss and curl-free conditions
    is ½[U_xx − 2(F′²/F)|D₀⊥|²], with ends U_xx (k ∥ D₀) and −W_xx (k ⊥ D₀), both > 0.
  - **(b) Gravity's (attractive) sign:** the potential energy ∫[W(∇Φ, x) + ρΦ] is minimized over Φ and x. The same branch is
    a maximum of W (W_xx < 0), which is I-b's tachyon. W is unbounded below as x → 0, so there is no stable ground state.
  - **Conclusion:** a Gauss-law rewriting of the same attractive mediator does not escape. An escape needs a flux sector
    entering with the opposite sign relative to the matter-coupled field. That is QUMOND's indefinite cross term
    2∇Φ·∇Φ_N (eigenvalues ±1), whose medium function obeys ν = Q′ and must be concave. This is the X15 class.
- **L4. The vacuum and the 4.**
  - With the vacuum from the same amplitude, e.g. V = a/x³ + Bx with B > 0, U(t) is analytic at t = 0: Newtonian in the
    infrared (this extends I-b's finding to the fixed-flux form).
  - With a separate ε: R = ε/(54ab³K³) and ξ = 192π·ab³K³/ε. This is a TRADE (S6 fails); with π-free parameters ξ has
    weight 1 and is never ¼.

## Checks (`w4_23.out`; light single-core sympy)

- **K1:** L1 symbolic for the three laws: dE/ds = μ/2 and dU/dt = ν/2, with sign(E_ss) > 0 and sign(U_tt) < 0 on t > 0.
- **K2:** L2. The infimum exponent for n = 3, 4, 5 equals n/(2(n−1)). At n = 3 the reconstructed law is g = g_N + √(a₀g_N).
- **K3:** L3(a). The x-stiffness at θ = 0 and θ = π/2 equals U_xx and −W_xx and is positive. It is linear in sin²θ, so it
  is positive for all θ.
- **K4:** L3(b). W_xx < 0 on the branch, and W → −∞ as x → 0.
- **K5:** L3 conclusion. Flux-affine ⇔ field-affine at fixed x (Legendre). QUMOND: the cross-term matrix [[0,1],[1,0]] has
  eigenvalues ±1, and ν = Q′.
- **K6:** L4. Taylor-analyticity of U at t = 0 when B > 0; R = ε/(54ab³K³); ξ = 192πab³K³/ε (weight 1).
- **I-checks:**
  - I1: grep for forbidden constants.
  - I2: symbolic.
  - I3: R is invariant under (ε, a, b⁻¹K⁻¹…) common rescalings and reported as such.
  - I4: no law κ read.
  - I5: no Friedmann.
  - I6: footing ρ_DE.
  - I7: classical, ħ-free.
  - I8: weights printed.

## Screen

- **S1:** static constitutive lane; no κ is output from c. Not cleared.
- **S6:** fails (ε separate).
- **S7:** the only escape found is X15 (QUMOND class).
- **Class:** `free` for the model; `audit` for the lemma.

## MUTATE (`W4_23_MUTATE=1`, separate outputs, exit 1 when the controls bite)

- **MU1. Flip the field-sector sign in K3/K4.** Expected: the stable/unstable verdicts swap. The electrostatic-stability
  check fails and the gravity-instability check fails.
- **MU2. One quantum per (n+1)-cell (p = n + 1).** Expected: the n = 3 exponent moves 3/4 → 4/5, and the additive-law check
  fails.
- Both must bite.

## Verdict (frozen)

- **GAUSS-LAW REWRITE DOES NOT ESCAPE FOR GRAVITY'S SIGN; THE ESCAPE IS THE OPPOSITE-SIGN FLUX SECTOR (X15); ½ NOT
  REACHED** if K1–K6 hold.
- **ESCAPE FOUND** only if K4 fails, i.e. the MOND branch is stable for the attractive sign. Not expected.
- Any failing K is reported as is.

**Hand expectation:** the first verdict.
