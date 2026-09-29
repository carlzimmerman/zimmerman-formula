# CFG173 — door 11, variant 11B′: a compressible directional flow of a massless Λ-medium

- **Criteria:** frozen in `FROZEN_CRITERIA.md` (3b68ed4ba), before any script, under the door-11 gates file (addenda 1–2, erratum 1: P2 primary).
- **Script:** `cfg173_directional_flow.py`, about 9 s.
  - Written by a background agent of this session to the frozen spec, and reviewed line by line before this run.
  - It imports CFG4_common and CFG7_common read-only.
- **Runs:**
  - The main run passes 27 of 27 checks (16 load-bearing) and exits 0.
  - MUTATE A, B, C and D each exit 1, each on exactly its targeted check:
    - A (w = −0.9): S1b and S1c fail.
    - B (achieved gravity × 10¹²): the three S2 checks fail.
    - C (isotropic flux): S3a fails.
    - D (deep-only flux law): S4-D fails.

## Bottom line

**A scoped no-go. None of the massless directional-flow readings written here (V1–V4 under T1–T3) passes G1 as a mechanism.** The extra gravity cannot come from:
- the flow's own gravity, which is at most 1.2 × 10⁻⁶ of the phantom;
- a push, which is Le Sage gravity: sign-changing, linear in mass, heating by 10⁵–10⁷ times the orbital energy, and saturated in stars and planets;
- the only flow law that reproduces the target. That law is a restatement: AQUAL written as a flux with a sink, the same object as door 11A (CFG171). It needs about 10⁷ times too much energy and has an imaginary sound speed.

The directional part itself adds a first-order dipole: a 12% side-to-side asymmetry at x = 30 for a galaxy moving at 600 km/s.

## The gate matrix

Canonical footing, P2, u = ρ_Λc². The reasons in the `.out` carry the alternatives.

| variant | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|
| V1 (w = −1) | FAIL | N/R | N/R | N/R | N/R | UNDEF | UNDEF | UNDEF |
| V1′ (w = −1 + ε), T1 | FAIL | UNDEC | N/R | FAIL | N/R | PASS* | PASS* | PASS* |
| V2 (null flux), T1 | FAIL | FAIL | N/R | PASS | N/R | PASS* | PASS* | PASS* |
| V2, T2 push | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL† | PASS† | FAIL |
| V3 (radiation fluid), T1 | FAIL | FAIL | N/R | PASS | N/R | PASS* | PASS* | PASS* |
| V3, T2 push | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS† | PASS† |
| V4 (granted law), T3 | FAIL | UNDEF | FAIL | FAIL | FAIL | PASS | PASS | FAIL |

- N/R = NOT REACHED; UNDEF = UNDEFINED; UNDEC = UNDECIDED.
- \* A trivial bound. The frozen text requires G6–G8 even when G1 fails structurally. The whole T1 force is ≤ 1.2 × 10⁻⁶ g_tot, so there is nothing to be anisotropic.
- † The agent's estimate, not in the frozen S3, labelled ESTIMATE in the output:
  - V2's Doppler drag 2k·u_F·v⊕/c = 2.8 × 10⁻¹⁴ m s⁻²;
  - V2's Doppler monopole change (1 + U/c)² − 1 = 4.0 × 10⁻³;
  - V3's monopole change (4/3)(U/c)² = 5.3 × 10⁻⁶;
  - V3's dipole bound 4U/c = 8.0 × 10⁻³.

## What each part found

- **S1 (V1; sympy). A w = −1 medium cannot flow. H-A holds exactly.**
  - T = −ρc²η is invariant under every boost.
  - T⁰¹ = (1 + w)ργ²cv, which is 0 for every v at w = −1.
  - The relativistic Euler coefficient ρc² + p vanishes, so there is no rest frame, no energy or momentum flux, and no compression.
- **S2 (T1, the flow's own gravity). H-B holds.**
  - The largest ratio R = g_ach/a_ph over the G1 grid, all at M = 10¹², x = 30:
    - V1′ (at its most compressible corner, ε = 0.1, c_s² = 10⁻⁴c²): 1.2 × 10⁻⁶;
    - V3 (hydrostatic): 9.6 × 10⁻⁹;
    - V2 (lensing): 4.8 × 10⁻⁹.
  - With P_cap, R is 100× smaller still.
  - To supply the phantom, the medium's density excess would have to be 26 to 10⁷ times ρ_Λ.
  - Physically: the energy density of Λ gravitates about 10⁻⁶ as strongly as a₀ at galactic radii, and focusing or compression changes it only at the r_s/r level.
- **S3 (T2, push).**
  - **V2, a directional shadow push**, taken relative to the galaxy's own free fall:
    - it pushes inward upstream (because the galaxy shadows itself) and OUTWARD downstream outside the shadow (θ = 90°–154.5°), so it changes sign (S3a);
    - only 1.2% of the 500 grid points fall within 10% of the target;
    - at fixed x it scales ×1000 from 10⁹ to 10¹² M☉, where the target scales ×1;
    - the opacity needed is 0.26 m²/kg; the absorbed energy over a Hubble time is 3 × 10⁵–1 × 10⁷ times the orbital energy;
    - the Sun and the Earth are optically thick (kΣ ≈ 10¹⁰–10¹²), so the push is not proportional to mass and the equivalence principle is broken.
  - **V3, an isotropic Le Sage bath**, gives a Newtonian 1/r² force. It is universal in mass but has the wrong shape (max error ×82 over x = 0.1–30).
    - Its drag on the Earth is 5.7 × 10⁻¹⁴ m s⁻², above the α₁ scale.
    - As electromagnetic radiation, it would be a 29 K bath.
  - **G2:** a Λ-energy flow that redshifts like radiation outweighs matter at recombination by 24–2400×.
- **S4 (V4, the granted flux law, T3; a restatement by rule).**
  - **The stream's first-order dipole,** measured in the galaxy's free-falling frame, reaches D = 0.120 at x = 30 for U = 600 km/s: **G8b FAIL**.
    - D exceeds 0.02 from x ≈ 5.
    - It arises because the stiff Newtonian core shields the stream while the outskirts feel it: the flow version of MOND's external-field lopsidedness.
    - The simple kernel gives 0.118.
  - **G7 passes** (the monopole changes by 5.1 × 10⁻³), **G8a passes** (2.0 × 10⁻³ dex), and **G6 passes** (3.6 × 10⁻²¹ m s⁻² at 1 AU, where the core shields the stream).
  - **G3 fails:**
    - the sink absorbs σ_E = 0.705 W/kg, which is 6 × 10⁶–2 × 10⁸ times the orbital energy over a Hubble time;
    - the momentum it absorbs from the stream exceeds 0.1 g_law over 57% of x ∈ [0.3, 30];
    - no b satisfies both G3 (b ≥ 6 × 10⁶) and the stream (b ≤ 0.8–4.4), so the window is empty.
  - **G5 fails:**
    - the medium's Bernoulli sound speed is imaginary everywhere, c_s²/q² = −(1 − 2s);
    - it inherits P2's Solar-System tail: a₀/2 is 1258–1545× the planetary bound (CFG185).

## Against the frozen hypotheses

- **H-A, H-B and H-C hold,** with one correction to H-C. Its expectation that "a directional flux's T2 force vanishes upstream" was wrong in the galaxy's frame: self-shadowing makes the upstream push inward and the downstream push outward. G1 fails either way.
- **H-D was partly wrong.** At b = 1 the stream breaks G8b (the dipole), but not G7 or G8a. V4 fails G3, G4 and G5 independently of the stream.

## Reading

- **The owner's picture, "the extra gravity is a boosted effect of a flow from one direction", is excluded as a mechanism in these readings.**
  - A massless Λ-medium is too dilute to gravitate enough.
  - It can push only by being absorbed, which breaks the energy budget and the equivalence principle.
  - The one flow law that reproduces the target is the MOND field equation written as a flux with a sink, with its known instability. The directional stream then adds only a dipole.
- **What survives is the restatement, not a mechanism.** CFG171 (door 11A, the inflow) reached the same object.
- **Candidate B is untouched:** its law, its a₀ = κc√(Gρ_Λ) tie and its cold component are unchanged. This door, as written, does not supply B's missing mechanism.

## Disclosed judgement calls and departures

- **Numerics:**
  - C1 is evaluated with s in the algebraically identical, cancellation-free form. The literal form fails the 10⁻¹² line by float cancellation alone.
  - C4 adds an independent SI quadrature of the column, since the grid path is tautological by construction.
  - C5b is an added, load-bearing sympy control of the G7 angle average and the ℓ = 2 source; it passes.
- **Scoring conventions:**
  - G8b uses the total force (s + 1/x²) as the denominator, which is what a rotation-velocity asymmetry needs. The frozen formula's "/s" variant is reported: 0.124, also FAIL.
  - G6 for V4 uses the core value f̂′(0) = 0, because x_sun = 1.26 × 10⁻⁴ lies below the integration start. The literal reading gives 2.3 × 10⁻¹⁹; both PASS.
  - The frozen "B" (the 1/x coefficient) is not well defined, because f̂ → x + c₀ with a constant c₀ ≈ −1. No gate uses it.
  - The b-window is reported by the frozen test (max b_max < min b_min) and by the natural one (min b_max < max b_min). They agree in the main run.
- **Matrix entries:**
  - The T1 rows' G6–G8 are trivial-bound PASSes.
  - V2(T1) and V3(T1) pass G4, because they use no opacity.
  - The estimate rows are marked † above.
  - As the frozen spec wrote it, V2's push is scored against the full g_tot and V3's bath against a_ph.
  - ν_mono is not computed.
- **Process:** the writing agent ran one read-only git command (`check-ignore`), which its brief forbade. It changed nothing. No other git command was run, and no `__pycache__` was written.

κ = ½ and Ω_c h² stay fitted. Nothing here touches candidate B, says the theory is closed, or says the data favour any model.
