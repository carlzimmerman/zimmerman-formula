# cm12 FROZEN CRITERIA: predict the retention-step mass from the cooling criterion, with the framework's own virial relation
(owner 2026-10-06: "yeah run c"; committed before any script exists)

**Question.** cm08–cm10 found two retention levels for the cold fluid: about 0.13 in galaxy-scale hosts and about 0.6 in group and cluster centrals. The step sits between the Milky Way and the lowest group-level hosts.

Does the classical cooling criterion predict where that step falls, using only the framework's gravity?
- The criterion is t_cool = t_dyn at the virial shock (Rees & Ostriker 1977; Silk 1977; White & Rees 1978).
- The framework's gravity enters through V⁴ = G M_b a₀ (deep MOND, flat V).
- No ΛCDM halo mass is used.

**Inputs (frozen).**
- Baryonic host mass M_b on a grid from 1e9 to 1e14 Msun. V = (G M_b a₀)^{1/4}.
- Hot-gas temperature T = μ m_p V² / (2k), with μ = 0.6. This is isothermal support for a flat curve, with σ = V/√2.
- Hot gas f_hot · M_b is spread uniformly inside a radius R. Electron density n_e = 1.17 n_H, n = 2.3 n_H.
  - t_cool = 3 n k T / (2 n_e n_H Λ(T)).
  - t_dyn = R / V.
- Cooling function Λ(T): the Tozzi & Norman (2001) fit for Z = 0.3 Zsun, in units of 1e-23 erg cm³ s⁻¹.
  - Λ = 8.6e-3 (kT)^-1.7 + 5.8e-2 (kT)^0.5 + 6.3e-2, with kT in keV.
  - The fit is used over 0.01–20 keV. Values outside that range are flagged.
- **Two radii, both reported, verdict on both:**
  - R1 is the MOND radius r_M = √(G M_b / a₀).
  - R2 is the radius where the mean enclosed baryon density is 200 × the cosmic baryon density, ρ_b = Ω_b ρ_crit with Ω_b = 0.0493 and H₀ = 67.4. This uses baryons only.
- f_hot = 1.0 (the classical assumption) and 0.5.
- Both footings: a₀ = 9.3603e-11 and 1.1312e-10.
- That gives 8 cells in total.

**Predicted step.** M_b* is the mass where t_cool / t_dyn crosses 1, moving upward from below. Hosts above M_b* cannot cool, so they keep a hot atmosphere.

**Target bracket (from the record, in baryons, no ΛCDM conversion).**
- Lower edge: the highest galaxy-level host, the Milky Way, at M_b = 6e10 Msun (McGaugh 2016 order). Retention 0.14 (cm08).
- Upper edge: the lowest group-level hosts, the Lovisari groups, at M_b(R500) ≥ 2.2e12 Msun (cm02).
- The bracket is [6e10, 2.2e12] Msun. That corresponds to V ≈ 165–406 km/s on the canonical footing.

**Verdict.**
- PREDICTS: M_b* falls inside the bracket in all 8 cells.
- PARTIAL: M_b* falls inside the bracket in 1 to 7 cells.
- FAILS: M_b* falls inside the bracket in no cell, or no crossing exists.
- Separately, I report the slope question: does t_cool/t_dyn rise with mass, as a step requires?

**MUTATE.** Λ × 100. M_b* must move by more than 0.3 dex in the canonical R1, f_hot = 1 cell. MUTATE writes separate outputs.

**Scope.** A pass would explain only where the step is, not the two levels 0.13 and 0.6, and not why cooling should change cold-fluid retention. No mechanism is claimed. The cold fluid is still required. κ = ½ is fitted.
