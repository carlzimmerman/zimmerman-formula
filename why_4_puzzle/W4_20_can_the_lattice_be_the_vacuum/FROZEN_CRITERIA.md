# W4-20: can the touching-horizon lattice — the record's only π-free ½ — be the vacuum? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-21, before any W4-20 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Theory lane. **κ = ½ is FITTED.** Not theory closed.

## Why

W4-18 B7 found the only route in the record that gives a π-free ½.
- In a simple-cubic lattice of masses m with spacing d = 2r_s, the pull of one neighbour is exactly (c/2)√(Gρ).
- Its caveat was "a dust lattice, not the vacuum".
- This lane tests that caveat with two classical results: von Laue's theorem and frozen brane networks ("solid dark
  energy", Bucher & Spergel 1999, w = −p/3).
- If some lattice of elements can carry w = −1 and keep a π-free single-element pull and a touching condition, the ½
  survives as a vacuum route. Otherwise the record's only π-free ½ is closed as a ρ_DE route.
- The register has no row on either result.

## Items (declared now)

- **V1 von Laue.**
  - For a static, isolated, self-bound element, ∂_jT^{ij} = 0 implies ∫T^{ij}dV = 0, so its weak-field active (Tolman)
    mass ∫(T⁰⁰ + T^{ii})dV/c² equals its rest energy over c².
  - Explicit model: a ball of vacuum (T⁰⁰ = ρc², P = −ρc², radius R) held static by a thin shell with surface stress −γ.
    Fix γ by the Laplace balance and verify ∫T^{ii}dV = 0 symbolically.
  - Report the sign of the shell's required tension and the element's active mass.
  - Consequence to state: a lattice of such elements has ⟨T^{ii}⟩ = 0, so w_eff = 0 whatever is inside.
- **V2 assigned-w reading (von Laue ignored).**
  - Give each element an isotropic w, so the active mass is m(1+3w).
  - Pull G m_act/d²; touching d = 2r_s(m_act) = 4Gm_act/c²; ρ = m/d³ (simple cubic).
  - Derive κ²(w) symbolically. At w = −1 the active mass is negative, and a negative-mass Schwarzschild exterior has no
    horizon, so the touching condition is undefined.
- **V3 frozen p-brane networks** (w = −p/3; p = 3 is the homogeneous vacuum).
  - Single-element active density (T⁰⁰ + ΣT^{ii})/c² for a relativistic element of each p: a point (dust), a string with
    T^{zz} = −μc², a wall with T^{xx} = T^{yy} = −σc².
  - Its weak-field field from Gauss's law: point GM/r², line 2Gλ/r, sheet 2πGΣ, each multiplied by the active density.
  - The string's conical deficit 8πGμ/c² is reported.
  - Question: does any w < 0 element give a nonzero π-free bare-G pull?

## Checks (must pass)

- **K1:** the von Laue trace ∫T^{ii}dV = 0 for the ball and shell at the Laplace-balanced γ (sympy, exact).
- **K2:** a bare vacuum ball (no shell) has Komar active mass −2ρc²V/c², i.e. it is not self-bound.
- **K3:** Gauss-law fields of a point, a line and a sheet from 4πG × enclosed / area.
- **K4:** the V2 formula at w = 0 reproduces W4-18's simple-cubic κ.
- **I1:** a forbidden-token scan of the compute block. No literal 0.5, 1/2, 0.25, 1/4, Rational(1, 2), Rational(1, 4) or
  S.Half may be used as a κ input.

## Verdict (frozen)

- **THE LATTICE ½ CANNOT BE THE VACUUM:** all three hold.
  - V1 gives w_eff = 0 for every static self-bound lattice.
  - V2 has no touching condition at w = −1.
  - V3 has no w < 0 element with a π-free nonzero pull.
- **A VACUUM LATTICE KEEPS ½:** any item yields a w < 0 lattice (and at w = −1 for the full claim) with a π-free
  single-element pull and a defined touching condition.
- **PARTIAL:** otherwise, with the failing item named.

**Hand expectation (disclosed):** THE LATTICE ½ CANNOT BE THE VACUUM.
- V1: the shell must be compressive (γ < 0) and the active mass is positive.
- V2: κ² = (1+3w)/4, undefined below w = −1/3.
- V3: the string has zero active density (deficit angle 8πGμ/c², π-odd); the wall has active −σ and field 2πGσ (π-odd).

## Controls (`W4_20_MUTATE=1`, separate outputs, exit 1 when all bite)

- **MU1:** remove the shell. ∫T^{ii} ≠ 0 and the active mass turns negative, so V1's dust conclusion no longer follows.
- **MU2:** a non-relativistic string (T^{zz} = 0). The π-free pull 2Gλ/r returns, at w = 0.
- **MU3:** set w = 0 in V2. The touching condition is defined again, and V2 returns W4-18's simple-cubic value.

## Register

Three rows (V1–V3), with live ids, then a `kappa_campaign_lee.py` rerun. Light: sympy only.
