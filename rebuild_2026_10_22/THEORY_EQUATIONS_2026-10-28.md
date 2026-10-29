# The theory in equations (2026-10-28)

**Standing rules.**
- κ = ½ FITTED.
- Canonical footing a₀ = 9.3603e-11 m s⁻². The alt footing (1.1312e-10) fails SPARC and the Milky Way faint dwarfs at
  every setting.
- Cold dark energy is a gravitating w ≈ 0 field component paired with dark energy, not matter and not a particle.
- Not "theory closed". Nothing here says the data favour the framework.

**Every equation below is graded in a committed lane** (cited). Nothing here is new physics written for this page.

## The four equations

**(1) Dark energy sets the acceleration scale.**

    a₀ = κ c √(G ρ_DE),      κ = ½  (fitted)

**(2) The galaxy law.** Gravity from baryons in a system without a cold dark energy halo:

    g = ν(g_N / a₀) g_N,      ν(y) = ½ + √(¼ + 1/y)

**(3) Cold dark energy: one surface-density rule.** Its two branches are the switch and the core. For a halo, the core
surface density is

    Σ_core = max( a₀ / 2πG ,  η(L) Σ_coll(M) ),      η(L) = (4 / 3B(1)) L^{5/4},  B(1) = 3 ln 2 − π/2

A halo exists only where the **second** term wins, evaluated on the mass of the gravitational basin, i.e. the region
inside the zero-velocity surface the system belongs to:

    cold dark energy halo   ⇔   η(L) Σ_coll(M_basin) > a₀ / 2πG
    otherwise                    the law (2) acts on baryons alone

- **Reading:** where the collapse column cannot beat the floor a₀/2πG that the law already supplies, cold dark energy
  stays unclumped and the law is the whole story. Where it can, cold dark energy condenses into a cored halo.
- **The threshold mass** T is the root of η(L) Σ_coll(T) = a₀/2πG. It is **not a separate number**: T = 10^12.236 at
  L = 3.75 (canonical).
- **The concentration** falls with mass along the framework's own zoom slope (X48 nine-seed): c_f(M) = L c_nat(M) /
  c_nat(10^14).

**(4) The halo's mass budget.** The native fair share of the measured baryons, counted out to the turnaround radius
(GS1):

    M_halo = (Ω_c/Ω_b)_native × M_b(< r_ta),      Ω_c/Ω_b = 5.2715  (BAO + BBN background, no CMB)

## What (1)–(4) pass (canonical)

The evidence is BS1 (979363d820), variant CL3_L3.75, using CL2's harness with the S9 slope.

- **Every calibration line:**
  - SPARC on two backgrounds;
  - 63 groups;
  - 15 eRASS1 × KiDS cluster lensing keys in two h cells;
  - five LG dwarf classes;
  - KiDS isolated-lens lensing.
- **The Milky Way:** it sits in the Local Group basin (log M_basin 12.39 > 12.236), so it carries a halo. The X5 box is
  feasible on velocity and vertical force (V + K).
- **The pass is a region, not a point:** LEE1 (199a94cd21) found 10 of 24 random settings pass. The band is
  L ≈ 3.6–4.2.

## The numbers that remain

| number | status |
|---|---|
| κ = ½ | **fitted** (every derivation in the record reduced to a posit or a fit) |
| L ≈ 3.75–4 | **located by data**; NL1 (7493e2902a) tests whether the native ng 64 zooms give it. Pending. |
| T | **derived from L** through (3); no longer independent |
| Ω_c/Ω_b | native background (BAO + BBN) |

If NL1 passes, the galaxy-to-cluster picture carries **one** fitted number, κ.

## Known failures (counterexamples, not hidden)

- **IC 1613: consistent if near face-on (IN1).** Both tracers (stellar σ, HI rotation) match the law at one
  inclination, i ≈ 19–27° (Oh+15 fixed 48°; their own rings span 15–85°), with LITTLE THINGS' stellar mass and a
  disc estimator. **Prediction:** an independent inclination ≥ 30° keeps it a failure.
- **X-COP cluster profiles:** the right mean but the wrong shape (HO1). It is not missing BCG stars (BC1: the profiles
  already carry the BCG, and ×2 moves the core miss only from +0.19 to +0.17), so the halo shape is wrong for clusters.
  The gas-temperature core (GT1) fixes 14 of 15 lensing keys but fails G-OUT-M3.
- **X-ray-bright groups (HG2 sign): WITHDRAWN as a failure (FM1).** HG2 bins on σ, the observed pull. Forward-
  modelled the same way, the base picture gives D ≈ −0.49 (measured −0.36), and the statistic cannot see even a
  +0.4 dex hot-gas excess. NOT DIAGNOSTIC as measured.
- **SLUGGS ellipticals:** the IMF is at its bound (SG1). Gas extrapolated beyond the measured X-ray edges passes
  (−0.002, 3/4). **Partly confirmed (XG1):** Chandra Atlas gas around NGC 4374 out to 65 kpc meets the extrapolation
  (f 1.19). NGC 5846 (atlas stops at 28.6 kpc) and NGC 4365 (not in the atlas) are untested.

## What is still a posit

- **The basin** as the unit the switch acts on. Equation (3) says *what* is compared, but no field equation yet
  *produces* the condensation.
- **The covariant parent.** The attempts (v3s, AeST + operator) were frozen after failing gravity or cosmology tests.
  (1)–(4) are a phenomenological theory, not yet an action.
