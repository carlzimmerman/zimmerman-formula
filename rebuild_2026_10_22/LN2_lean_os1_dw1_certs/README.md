# LN2_lean_os1_dw1_certs — Lean 4 + Mathlib certificates for OS1 and DW1

`CoreLawCerts.lean` compiles with **no `sorry`**. All 7 theorems depend only on Lean's standard axioms (propext,
Classical.choice, Quot.sound), printed in `CoreLawCerts.out`. `CoreLawCerts_MUTATE.lean` changes three statements:
- the Knudsen coefficient 4/(3√π) → 4/(3π);
- Γt = 1 → 2;
- q < 2 → q ≤ 2.

It fails to compile at each (exit 1, `CoreLawCerts_MUTATE.out`).

**Lean certifies mathematics from stated premises only.** It does not certify the physical premises (isothermal cores,
rate × age = 1 at the core, Burkert halos, the Σ_a0 anchor) or any measured number. κ = ½ FITTED; not "theory closed";
nothing here says the data favour the framework or ΛCDM.

Compile: `cd fable_independent_2026/lean_2026 && lake env lean ../../rebuild_2026_10_22/LN2_lean_os1_dw1_certs/CoreLawCerts.lean`

| theorem | statement | lane |
|---|---|---|
| `q_to_n` | q = (1+n)/2 ⇔ n = 2q − 1 | LN1 T7, OS1 |
| `os1_n_values` | OS1's q_f = 0.892 / 0.748 give n = 0.784 / 0.496 > 0, so the cross-section per mass falls with velocity | OS1 |
| `sigma_ratio` | under Σ_i = Σ_a0 (σ_i/σ_ref)^q, Σ₁/Σ₂ = (σ₁/σ₂)^q, independent of the anchor σ_ref | OS1 |
| `gamma_t_one` | with ρ₀ = 1/(K σ^(1−n) t) and Γ = ρ₀ K σ^(1−n): **Γ t = 1 for every σ, K, n, t > 0** | DW1 M2 |
| `no_collapse` | no collapse threshold N_c > 1 is reached by any system under this core law | DW1 M2 |
| `knudsen_closed_form` | from λ = 1/(ρ₀ s), H = σ/√(4πGρ₀), ρ₀(sv)t = 1, v = (4/√π)σ, sv = Kσ^(1−n), K = 9σ_ref^(1+n)/(4πG t Σ²), Σ = a₀/(2πG): **Kn = (4/(3√π)) · (2 a₀ t/σ_ref) · (σ/σ_ref)^((n−1)/2)**, i.e. (σ/σ_ref)^(q−1) | DW1 M1 |
| `sigma_h_unique` | for C > 0 and **q < 2**, σ_h² = C σ_h^q has exactly one positive solution, σ_h = C^(1/(2−q)) | DW1 M3 |

## Reading

- **M1** is now a certified identity, not a numeric claim. With the coupling anchored by a₀ at galaxy scale, Kn depends
  on σ only through (σ/σ_ref)^(q−1). Evaluated in DW1 at the stated premises, it gives Kn = 653–1158 (canonical) and 539–2048 (alt) from 5 to 1000 km/s, deep in the long-mean-free-path regime.
- **M2** is structural. Under this core condition every core has rate × age exactly 1, so collapse cannot distinguish
  dwarfs from anything else.
- **M3**'s halo-dispersion solve is well posed (unique) for every q < 2, which covers OS1's q_f. DW1's M3 FAILS is
  therefore a statement about the data, not a solver artefact.
- Together with LN1 (the ceiling (9/32) a₀, the core law Σ₀² = 9σ^(1+n)/(4πGKt), and the q window), the core-law chain
  CD1 → SC1 → OS1 → DW1 now has its mathematics certified end to end.
