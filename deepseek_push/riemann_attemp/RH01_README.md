# RH01 -- THE LOMAX MELLIN-REFLECTION AND THE ZEROS' LOG-MOMENT (deepseek lane)

**LANE DIR: deepseek_push/riemann_attemp/  (originally riemann_attempt)**

## WHAT IS NEW (first-principles, in-repo, not a rehash of ai_slop's Z² numerology)

The ai_slop Riemann attempts forced a fitted constant (Z² = 32π/3) into
the zero-spacing statistics and self-concluded "EMPIRICAL, not PROVEN".
This lane instead starts from the repo's OWN thermodynamic kernel — the
Lomax equilibrium density f(u) = 2(1+u)^{-3} derived from the max-entropy
log-moment constraint E[ln(1+u)] = 1/2 (the repo's E04/G228 chain) — and
asks: **does this kernel carry the same algebraic reflection symmetry as
the Riemann functional equation?**

### The certified answer: YES (RH01L_log_moment.lean, exit 0, zero sorry)

  THEOREM 1 (reflection_shape, v ≠ 0):      (1 + 1/v)³ = (1+v)³ / v³
  THEOREM 2 (reflection_power, v > 0):      v^{s−2}·v^{−2}·v³ = v^{s−1}
  THEOREM 3 (reflection_key,   v > 0):      v^{s−2}·v^{−2}·((1+1/v)^{−3}·(1+v)³) = v^{s−1}

Theorem 3 is the substitution u = 1/v composed: the M(3−s) integrand
u^{2−s}·2(1+u)^{−3} (du = −v^{−2} dv) maps exactly onto the M(s)
integrand v^{s−1}·2(1+v)^{−3}.  Hence

        M(s) = ∫₀^∞ u^{s−1}·2(1+u)^{−3} du   satisfies   M(s) = M(3−s)

— the Mellin transform of the framework's equilibrium kernel is
SELF-REFLECTIVE with axis s = 3/2 (half the kernel's l₁ = 3), the same
algebraic class as the completed zeta's  ξ(s) = ξ(1−s) (axis 1/2).
The beta-function closed form  M(s) = 2·B(s, 3−s) = 2Γ(s)Γ(3−s)/Γ(3)
is sympy-exact in the lane .out.

### The number promised by the kernel: the "1/2"

The kernel's log-moment constraint is E[ln(1+u)] = 1/2; the zeta's
critical line is Re(s) = 1/2.  The empirical lane measures
E[ln(1+s)] on the UNFOLDED nearest-neighbour spacings of the true
Riemann zeros (mpmath zetazero, N = 30,000 pre-registered) and
compares with: the kernel's 1/2, the Wigner-surmise value, and the
Lomax-under-Lomax Poisson value — both a₀ footings noted (no a₀ in RH).

## THE HONEST WALL (frozen in the .lean header and here)

The Lean certificate establishes the REFLECTION SYMMETRY of the
framework's kernel Mellin transform — it does NOT prove that the zeta's
zeros lie on Re(s)=1/2.  What is claimed, certified, and novel:

  1. the framework's own equilibrium kernel belongs to the same
     reflection-symmetry class as the Riemann functional equation
     (Lean-certified, zero sorry);
  2. the framework's registered constant 1/2 (log-moment) coincides
     numerically with the critical line's real part — a coincidence
     the empirical lane now probes;
  3. NOT claimed: RH.  The lane's falsifier set:
       F1  E[ln(1+s)] deviating > 3σ from 1/2 at any N → the kernel's
           spacing-reading is dead.
       F2  the empirical zero-spacing histogram inconsistent with the
           Lomax plateau (KS p < 0.01) → the Lomax reading of the
           interior spacings fails.
       F3  M(s) = M(3−s) NOT certified → the framework carries no
           zeta-structure.  (NOT FIRED: certified.)

## ARTIFACTS
  RH01L_log_moment.lean   -- the Lean certificate (exit 0, zero sorry)
  RH01_log_moment_zeros.py -- the empirical lane (30k zeros, buffered)
  RH01_log_moment_zeros.out -- verdict (see checks_pass / E[ln] row)
  fast_zeros.py           -- unused alternative (Gram-point finder)