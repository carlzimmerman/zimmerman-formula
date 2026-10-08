# CFG461: what sets the cold fluid's temperature? FROZEN before any script exists

The theory question behind the newest result. κ = ½ is FITTED. Both footings (a₀ = 9.3603e-11 and 1.1312e-10 m/s²) are scored separately and never pooled. No dark-matter particle is added: the cold fluid's mass is still required, and its amount (Ω_c/Ω_b = 5.364) is an input. This is not "theory closed".

## The question

PAPER45 v2 (CFG424–427, CFG439) fixes growth by treating the phantom as conserved cold fluid drawn from each halo's turnaround sphere and cut at r_edge = r_M/ln(1/(1−f_b)) ≈ 5.85 r_M. The settling there is bookkeeping: it is imposed, not derived.

What the record has already established (cited, not re-derived):
- T13 / CFG472 K-A: the deep phantom is exactly a singular isothermal sphere (SIS) with σ² = V_f²/2.
- T10: a JKO settling toward the deep target is pure heat flow in μ = r²ρ, and the uniform-μ state is deep MOND.
- So settling reduces to one number per galaxy, the AMPLITUDE: **σ⁴ = G M_b a₀/4**.
- CFG60 (54 rows): no committed construction derives the cold fluid's stress (D = 0).
- CFG130: the target's f(E, L) exists, but it is not a Lynden-Bell extremum (for CFG44's point-mass target).
- CFG472/473: no Newtonian pressure equilibrium has the target's transition shape, and the holding force is nonlocal.
- CFG381: the khronon alone gives no settling force (the coupling is +1 constant).
- CFG264: c-free principles cannot fix c-carrying coefficients (there, k2).

This lane asks only about the amplitude (the temperature), not the transition shape. CFG472 already failed the shape.

## Candidate mechanism classes (all tested, none dropped after the run)

- **C1 Lynden-Bell / maximum entropy** of the cold fluid in Newtonian gravity of all real mass (the working model: the law is a target, not a force). Constraints: mass M_c, energy E, box R, and the maximum phase-space density η.
  - C1a: does the max-entropy state fix σ⁴ = G M_b a₀/4, or leave σ as the multiplier set by E? Tested by the c-scaling test below.
  - C1b: self-gravitating, no baryons, in a box at the truncated SIS's own energy E = −GM²/(4R). Is the SIS the entropy maximum, or is a cored isothermal state? This is the Emden spiral (Antonov; Lynden-Bell & Wood 1968).
- **C2 gradient flows (JKO / Wasserstein).**
  - C2a: T10's μ-heat flow with conserved cold mass in a no-flux box R. The equilibrium amplitude is computed and tested against the box radii that cosmology supplies (C4).
  - C2b: the free energy built from the law's own action applied to all real mass (AQUAL/QUMOND field energy of ρ_b + ρ_c, with ν_mono) plus isothermal entropy. Numeric isothermal spheres:
    - Hernquist baryons, a = 0.3 and 1 r_M;
    - cold mass fixed at 5.364 M_b;
    - central density scanned, σ solved.
  - C2c: the mismatch functional F = (1/8πG)∫|g_N[ρ_b + ρ_c] − g_law[ρ_b]|² dV (sympy minimiser).
  - C2d: the fluid as a tracer of the law's baryon field plus its own Newtonian self-gravity (the A11 class), sympy.
- **C3 an a₀-scale thermal bath.**
  - C3a: Unruh temperature at a₀, and Gibbons–Hawking at H_Λ, with particle mass m. Computed: the m each galaxy needs, the spread, and the c-scaling.
  - C3b: a vacuum stress boundary P_edge = a₀²/(8πG) on an SIS (sympy).
- **C4 cosmological virialisation**, gravity only and energy conserving.
  - A uniform sphere at rest at turnaround (spherical collapse, Einstein–de Sitter timing, Ω_m = 0.315, H₀ = 67.4) relaxes to a truncated SIS of the same energy, so R = (5/12) R_ta.
  - Collapse redshift z_c = 0, 1, 3; M_tot = M_b/f_b. The r₂₀₀(z_c) radius is reported as a bracket.
- **C5 Jeans marginality** (T13's λ_J² = 2π² r²): does marginal stability pick σ? Sympy.
- **C6 the direct dark–baryon phonon coupling** (Berezhiani–Khoury; arm (a) of the fork). NOT computed. It is listed so that the table is complete: it fails G-d by construction.
- **R0 RESTATEMENT (control, not a candidate).** The conserved cosmic share relaxed to the uniform-μ state inside the law's r_edge. It must pass G-b's numbers (this shows the gate can pass). By construction it fails G-c, because r_edge is the law's own output.

## Test galaxies

M_b = 1e9, 10^10.5 and 10^11.5 M_sun, on both footings.

Target: σ_t⁴ = G M_b a₀/4 (σ_t² = V_f²/2, V_f⁴ = G M_b a₀). f_b = 1/(1 + 5.364).

## Gates (a class PASSES only if every one passes)

- **G-a mass conservation.** The mechanism conserves cold mass (continuity), and it uses at most the cosmic share 5.364 M_b inside r_edge.
- **G-b the equilibrium is the right SIS.** All four parts must hold:
  1. σ is an OUTPUT. It is not chosen, and it is not fixed by a boundary radius or energy taken from the law.
  2. The equilibrium is an SIS: the log-slope of ρ_c is within [−2.15, −1.85] over r ∈ [2, 5] r_M for the numeric classes, or exactly −2 for the analytic ones.
  3. |log₁₀(σ⁴/σ_t⁴)| ≤ 0.10 for all 3 galaxies × 2 footings. (0.1 dex is the BTFR intrinsic scatter in mass.)
  4. Scaling: d ln σ⁴/d ln M_b ∈ [0.9, 1.1] across the three galaxies, AND the **c-test** d ln σ⁴/d ln c ∈ [0.9, 1.1] at fixed G, ρ_Λ, M_b. In the framework a₀ = κc√(Gρ_Λ), so the target is linear in c. The c-test is evaluated by changing c by ×1.2 inside the mechanism.
- **G-c no constant beyond κ.** Allowed inputs: G, c, ρ_Λ (a₀), Ω_c/Ω_b, the cosmological background (H₀, Ω_m, z_c), and the baryon profile. Not allowed:
  - a new constant (a particle mass, a coupling, a threshold);
  - a hand-inserted ρ_ph, g_law, σ, or a radius keyed to r_M.
- **G-d G9.** There is no non-gravitational baryon–cold coupling.
- **G-e timescale and locality.**
  - The relaxation time at r_edge must be ≤ t_H = 13.8 Gyr for all 3 galaxies.
  - The mechanism must be inert outside bound halos, so that growth stays as in CFG424.
  - A mechanism acting on the whole cosmic fluid (a universal bath, or the law applied to all mass) fails.
- **G-f MUTATE control** (`CFG461_MUTATE=1`). Inside every mechanism, and in R0's r_edge:
  - a₀ → 2a₀;
  - the baryon dependence is dropped (M_b → 10^10.5 M_sun inside the mechanism).

  Scoring is against the TRUE target. Every class and R0 must then fail G-b (parts 3/4). R0 failing under MUTATE is the teeth check. Exit code 1 when detected.

## Controls (load-bearing; the main run exits 0 only if all pass)

- **K1 (sympy).** σ⁴ = GMa₀/4 ⇔ σ² = V_f²/2 for the deep SIS; the truncated-SIS energy E = −GM²/(4R); λ_J² = 2π² r² for any σ.
- **K2.** The Emden spiral reproduces Antonov's limit: min λ = RE/(GM²) = −0.335 ± 1% at density contrast 709 ± 3%. Its centre (the SIS) is at λ = −1/4.
- **K3.** A pure deep-MOND isothermal sphere (ν = y^−½, no baryons) gives σ⁴/(G M a₀) = 4/81 within 2% (Milgrom's deep virial relation).
- **K4.** R0 passes G-b parts 2–4. (Part 1 is excluded, because R0 is a restatement by construction.)

## Verdicts

- **MECHANISM FOUND:** a class passes every gate.
- **NO CLASS PASSES:** otherwise. The table then states which gate each class fails and the missing ingredient.

"No class passes" is an acceptable outcome. A class that reproduces the SIS only by choosing σ, or by inserting ρ_ph or r_edge, FAILS G-b (part 1) or G-c.
