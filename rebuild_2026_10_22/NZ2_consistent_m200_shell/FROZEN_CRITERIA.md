# NZ2_consistent_m200_shell: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Argon's proposal, relayed 10-31. NZ1 keeps the zoom's core, M(<r_f) = M₂₀₀/2 with r_f about 0.89 R₂₀₀, then spreads the rest to r_ta, so its profile holds only about half of M₂₀₀ inside R₂₀₀. Argon calls that the bug behind NZ1's outer-shear miss (G-OUT-M3 UNDER), and proposes enforcing M(<R₂₀₀) = M₂₀₀ and M(<r_ta) = M_fair with the zoom's r₀ kept. It predicts, on the ng 64 tables: X-COP mean about +0.005, rms about 0.07; G-IN-Mall −1.15 to −1.65; G-MID about −0.10 to +0.10; groups back to +1.62. Those are scored as written. Part of its derivation arrived scrambled, so its other numbers aren't recorded.

**Disclosed, against this lane before it runs.**
- ZN1's zooms measure this directly. At z = 0, 10¹⁴: M₂₀₀/M nominal 0.683, and M(<r_f, z = 0) = 1.185 × M/2, so M(<r_f) is about 0.87 M₂₀₀, not 0.50. NZ1's mislabel is treating nominal M as M₂₀₀. ZN1 already enforces M(<R₂₀₀) = M₂₀₀ with the measured shape, and it reads X-COP −0.070, 0.116, keys 15 of 15. So NZ2's half-mass shell just inside R₂₀₀ isn't what the zooms do. A pass here would be an empirical two-piece profile that the zooms contradict inside R₂₀₀.
- Groups sit at r far below r_f, so NZ2 can't change them on the "all" path. I expect Z +3.84, as NZ1 at ng 64, not +1.62. The "clusters only" path keeps budget r₀ for groups, Z +1.45.
- I've seen NZ1 at ng 64: X-COP −0.025, 0.083; G-OUT-M3 +4.90 as graded.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Rule (cluster and X-COP paths; M is MA1's M₂₀₀, as NZ1)
- r ≤ r_f: NZ1's zoom core, S = f_c η(M) Σ_coll(M), r₀ = r_f/a, on CE1's ng 64 table.
- r_f to R₂₀₀: uniform density, reaching M_c(<R₂₀₀) = f_c M₂₀₀.
- R₂₀₀ to r_ta: ρ ∝ r^(−γ_o), M_c(<r_ta) = M_fair, with γ_o = 2.65, ZN1's measured slope past R₂₀₀. Density may jump at R₂₀₀. If f_c M₂₀₀ already exceeds M_fair, M_c stays constant past R₂₀₀, counted.
- The uniform shell and the γ_o choice are mine, since the readable part of the proposal doesn't fix them. Reported line 2 shows how much γ_o matters.

## Grade
One template, 15 keys, both h, |Z| ≤ 2; X-COP |mean| ≤ 0.05, rms ≤ 0.10; f★ 0.034 and 0.0615. X-COP's gas scale primary, as ZN1's A1, eRASS1's own gas beside it. SPARC and groups in both NZ1 modes, "clusters" and "all".

## Verdict
**NZ2 PASSES BOTH** (keys and X-COP at both f★), **F★-DEPENDENT**, **X-COP ONLY**, **KEYS ONLY**, **FAILS BOTH**, or **NEITHER AT ONE f★**, with **[GAS-SCALE-DEPENDENT]** if eRASS1's own gas differs. Whatever the class, the README states that this interior contradicts the measured native profile.

## Reported, not graded
1. With each cluster's own z_obs, as NZ1's reading.
2. γ_o 2.25 and 3.0.
3. BA1's joint χ² on each job.

## Checks
- **K1:** with NZ2 off, this path reproduces NZ1's ng 64 predictions: |d| ≤ 1e-9.
- **K2:** M_c(<R₂₀₀) = f_c M₂₀₀ and M_c(<r_ta) = M_fair on every cell with a shell: ≤ 1e-9.
- **MUTATE** (`--mutate`, separate outputs): r₀ × 1.5 must move X-COP's rms by more than 0.01.
- Any K failure: no verdict, exit 1.
