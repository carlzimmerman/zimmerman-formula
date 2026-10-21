# W4-23: the Gauss-law (fixed-flux) rescue. DOES NOT ESCAPE FOR GRAVITY'S SIGN; ½ NOT REACHED

**Bottom line.**
- **New lemma (L1).** Every MOND law is *convex* in the field variable s = g² and *concave* in the flux variable t = g_N²,
  because dE/ds = μ/2 (μ rises) and dU/dt = ν/2 (ν falls).
  - So the record's concavity theorem (W4-08) is stronger than it looked. A stable medium that couples affinely to s can't
    produce **any** MOND interpolation, not just the deep cubic. It can only give "anti-MOND", μ non-increasing.
  - Read in the Gauss-law variable t, the same theorem permits every MOND law.
- **A minimal fixed-flux medium works on paper (L2).** It has one internal size x, energy a/xⁿ (one quantum per cell) and a
  flux coupling b·t·x^{n−2}. Minimising over x gives the deep-MOND power exactly in n = 3, 4, 5 spatial dimensions, with
  the exponents fixed by dimension, not tuned. At n = 3 it is **g = g_N + √(a₀g_N)**.
- **The catch (L3).** At fixed x, a flux-affine medium *is* a field-affine one: the Legendre transform of V + tF is
  s/(4F) − V. So rewriting the same mediator in Gauss-law form changes nothing physical. Stability is set by the sign the
  field sector has in the action:
  - **Electrostatic (Gauss-law) sign:** the MOND branch is a stable minimum for every perturbation direction.
  - **Gravity's attractive sign:** the same branch is a maximum, which is W4-08's tachyon. The energy is also unbounded below
    as x → 0, so there is no stable ground state.
- **So the only escape is a flux sector entering with the opposite sign** relative to the matter-coupled field. That is
  QUMOND's structure: an indefinite cross term 2∇Φ·∇Φ_N (eigenvalues ±1), with ν = Q′(t). That is the class the campaign
  already excludes unless stiffened (X15: Cassini p58 gives κ < 0.17 at 2σ).
- **The 4 is still free (L4).**
  - A vacuum from the same amplitude makes the law analytic at zero flux, so it is Newtonian in the infrared. This repeats
    W4-08's finding, now in the fixed-flux form.
  - A separate vacuum gives R = ε/(54ab³K³) and ξ = 192π·ab³K³/ε: a TRADE, never ¼ with π-free inputs.

**κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095). Not theory closed.

## In plain words

The "sign wall" from W4-22 says the MOND term comes out with the wrong sign in any stable medium. The hope was that writing
gravity in its Gauss-law form would flip that sign, and on paper it does. Every MOND law has the allowed curvature in the
flux variable, and a very simple medium (cells holding one quantum each, which cost energy when flux runs through them)
reproduces MOND exactly.

But the rewrite is only a change of variables. For a force that *attracts*, like gravity, the medium state that gives MOND
is still the unstable one. The flip only becomes real if the flux lives in a separate sector with the opposite sign. That is
exactly QUMOND's hidden structure, and the campaign has already excluded it unless the stiffness term is added. And the
number 4 is still unfixed.

## Results (`w4_23.out`)

| check | what | result |
|---|---|---|
| K1 | duality, for simple μ, standard (n = 2) μ and the additive law | E convex in s and U concave in t for all three |
| K2 | minimal medium a x⁻ⁿ + b t x^{n−2} | exponents 3/4, 2/3, 5/8 = n/(2(n−1)); n = 3 gives g = g_N + √(a₀g_N), a₀ = 4√3·K√a·b^{3/2} |
| K3 | electrostatic sign | x-stiffness U_xx (k ∥ D₀) and −W_xx (k ⊥ D₀), both positive and linear in sin²θ: stable |
| K4 | gravity sign | W_xx < 0 on the MOND branch (a maximum; Φ relaxation only lowers it); W → −∞ as x → 0 |
| K5 | sign structure | flux-affine = field-affine at fixed x; QUMOND cross term ±1; ν = Q′ |
| K6 | vacuum and the 4 | same-amplitude vacuum: U′(0⁺) finite (Newtonian IR); separate ε: R = ε/(54ab³K³), ξ = 192πab³K³/ε |
| I1, I3 | forbidden constants; common energy rescaling | pass |

## What is new against the record

- **W4-08 has:** the constrained branch with g = g_N + √(a₀g_N), its tachyon, and the same-sector vacuum failure.
- **W4-23 adds:**
  - the duality lemma (the wall forbids every interpolation, not just the cubic);
  - the minimal fixed-flux medium with dimension-fixed exponents;
  - the proof that stability is decided by the field sector's sign and not by Gauss-law versus field form. That answers
    W4-08's declared route R3 for the affine family;
  - the identification of the one escape as QUMOND's indefinite sector.

## What is still open

A coupling that is affine in **neither** s nor t, where the gradient enters the constraint's own definition (W4-08
NEUTRAL_CURRENT_TEST). This lane doesn't cover that, and the record's attempts at it (neutral currents, Jacobian charge, CS
flux attachment) have hit other walls.

## Disclosure: first run

The first normal run (`w4_23_firstrun_K5fail.out`, kept) scored K5 as FAIL. The QUMOND gradient symbols were declared real
rather than positive, so sympy returned ν wrapped in a Piecewise/Abs form that didn't match Q′ symbolically. For a positive
gradient it is identical. The fix changes only that symbol assumption, and every other output is unchanged.

## MUTATE (`w4_23_MUTATE.out`, exit 1 by design)

- **MU1, field-sector sign flip:** the electrostatic-stable and gravity-unstable verdicts swap (K3 and K4 both fail). Bites.
- **MU2, one quantum per (n+1)-cell:** the n = 3 exponent moves 3/4 → 4/5 and the additive law fails. Bites.
- K6 is not evaluated under MUTATE, by design. K1, K5, I1 and I3 still pass.

## Files

- `FROZEN_CRITERIA.md`: committed alone, f98069665.
- `w4_23.py`: sympy, single core.
- `w4_23.out` and `w4_23_results.json`: the fixed normal run.
- `w4_23_MUTATE.out` and `w4_23_results_MUTATE.json`: the control run.
- `w4_23_firstrun_K5fail.out`: the first run, kept.
