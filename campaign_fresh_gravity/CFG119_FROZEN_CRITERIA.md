# CFG119 — Door 7: a fuzzy-dark-matter soliton plus baryons (Schrödinger–Poisson) against the CFG44 target. FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. The menu of ten doors (closure_map/TEN_DOORS_GATES_2026-09-29.md, 5ef77ea09) was written knowing the target. The shared gates G1–G5 there are binding; this file adds lines but weakens none. A scoped no-go is a valid result.

## The question

Take an ultralight scalar of boson mass m. Its spherically symmetric Schrödinger–Poisson ground state (n = 0, l = 0) sits in the combined potential of the baryons and its own self-gravity:

−(ħ²/2m)∇²ψ + m(Φ_b + Φ_ψ)ψ = Eψ, ∇²Φ_ψ = 4πG m|ψ|², ∫ m|ψ|² dV = M_sol.

Can this state reproduce CFG44's target C(r) ≡ ρ_c r³ g_tot = (a₀/4π) M_b(<r)?
- The pass line (G1) is within 10% over x = r/r_M in [0.1, 30].
- It is checked for M_b = 10⁹, 10¹⁰, 10¹¹ and 10¹² M☉, for a point mass and CFG44's exponential spheres (h = 2, 3, 4, 5 kpc), with ONE m at every mass.

## Declared procedure

- **The ground state** is solved by a shooting or imaginary-time relaxation method on a log grid from 10⁻³ r_M to 10³ r_M, and converges to 1e-8 in E.
- **The boson mass:** m ∈ {10⁻²³, 10⁻²², 10⁻²¹, 10⁻²⁰} eV, the declared literature range.
  - This is FDM's own new constant. The grid reports which m comes closest; it does not tune m to pass.
  - G4 fails for any m that is not tied to Λ or κ in the same action. No such tie is declared.
- **The soliton mass M_sol at each M_b, two declared rules:**
  - (i) the Schive et al. (2014) core–halo relation, M_sol ∝ M_h^(1/3), with M_h from the target's own cold mass at 30 r_M;
  - (ii) free per galaxy: the M_sol that minimises the largest |log ratio| over x in [0.1, 30]. That is the most generous reading, and it breaks G4's "same constants" rule, but it bounds the shape test.

## Checks

- **C1 CONTROL:** with no baryons, the ground state reproduces Schive et al.'s empirical soliton, ρ ∝ (1 + 0.091 (r/r_c)²)^(−8), within 3% out to 3 r_c. The fit's own accuracy is quoted as about 2%.
- **C2 CONTROL:** with self-gravity off and a point-mass potential, the ground state reproduces the hydrogen-like ψ ∝ e^(−r/a_B), a_B = ħ²/(G M_b m²), to 1e-6.
- **H1 [HEADLINE; MUTATE must change it]:** G1 holds: with one m at every mass, the ratio C_SP/C_target lies in [0.9, 1.1] over x in [0.1, 30], for every mass and both geometries, under rule (i) or rule (ii).

## Reported rows

- **R1:** for each m, M_b and rule, the largest |log10 ratio| over x in [0.1, 30] and where it occurs. The shape expectations are declared: the soliton is cored (ρ → constant as r → 0), unlike the target's ρ ∝ 1/r inside r_M, and it falls steeply beyond its core, unlike the target's ρ ∝ r⁻² outside.
- **R2:** the best m per mass under rule (ii). A single m could fit only if these agree.
- **R3, G2–G5 as statements:**
  - G2: FDM suppresses linear growth below its Jeans scale. Report the half-mode wavenumber from the Hu, Barkana and Gruzinov (2000) scaling and whether growth stays within 5% to k = 30 Mpc⁻¹ for each m.
  - G3: ordinary gravity, so reciprocity holds.
  - G4: m is a new constant, a FAIL unless tied.
  - G5: a Klein–Gordon field is well posed.

## MUTATE

MUTATE=1 evaluates G1 on the target's own ρ_c in place of the SP ground state. H1 must then pass, so the MUTATE changes the headline. This checks that the evaluator can pass. The physics is validated by C1 and C2.

## Readings (declared)

- **H1 PASS:** the soliton lands on the target. G4 still fails unless m is tied to Λ.
- **H1 FAIL:** a scoped no-go on G1. R1 says whether the failure is the inner core, the outer envelope, or both, and R2 whether a single m could serve every mass.
- **Untested (declared):**
  - the FDM envelope of excited states and granules (the NFW-like outer halo in simulations), since only the ground state is tested;
  - self-interactions;
  - non-spherical and time-dependent solutions;
  - baryonic feedback.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
