# CFG474: what can the cold mass be? The light end closes. If it is the record's wave field, its mass is ≥ 3e-19 eV, and in every surviving window it behaves like cold dark matter on all scales the record tests

Criteria 50e0265b4 (committed before the script). Script `cfg474_window.py` (< 1 s). κ = ½ fitted; both footings. **The cold mass is still required, and its amount (Ω_c/Ω_b = 5.36) is still underived.** This lane bounds its nature; it does not explain it.

**Step 1: the MW ultra-faints are cold-fluid-dominated** (31 resolved; f_cold = (M_dyn − M_law)/M_dyn inside r_½).

| footing | median f_cold | share with f_cold ≥ 0.5 | Segue 1 (M_dyn / M_law / f_cold) | verdict |
|---|---|---|---|---|
| canonical | 0.805 | 0.94 | 2.86e5 / 1.15e4 / **0.960** | COLD-DOMINATED |
| alt | 0.786 | 0.94 | 2.86e5 / 1.26e4 / **0.956** | COLD-DOMINATED |

Segue 2, the bound's other anchor, has only an upper-limit σ (2.06 km/s) in the LVD.

**Step 2: the UFD heating bound applies.** Dalal & Kravtsov 2022 bound a wave field that dominates a UFD as a virialized, granular halo at m > 3e-19 eV (99%). The ground-state escape is closed by CFG440 s02 (soliton scaling rejected). It is conditional on:
- (c1) the UFD fluid being the cosmological cold component;
- (c2) it being granular, not a coherent ground state;
- (c3) the published bound itself.

**Step 3: surviving mass windows** (CFG367's committed survivors ∩ m > 3e-19 eV).

| window | λ_dB at 10 km/s | λ_dB at 200 km/s |
|---|---|---|
| 3.0–3.9e-19 eV (a sliver CFG367 already called "probably not real": it sits between measured holes) | 3–4 pc | 0.15–0.20 pc |
| 5.3e-17 – 37 eV | ≤ 0.02 pc | ≤ 0.001 pc |

**The light end (2.0–4.4e-20 eV) is CLOSED**, conditionally. The working model's open piece 6 listed it as open, and CFG394/444 kept it open on black-hole spins alone. Ultra-faint heating closes it independently.

**Step 4: what that means.** In every surviving window the field's de Broglie length is ≤ 0.2 pc at galactic speeds. So it behaves as **collisionless cold matter on every scale the record tests**: discs, dwarfs, lensing, clusters. That matches CFG440 session05 (X-COP excess NFW-like), CFG443 (halos more concentrated than the target with or without settling) and CFG472 (no pressure gives the target). Plainly: the record's cold fluid is, operationally, **cold dark matter**, a classical field whose quanta would be bosons of mass ≥ 3e-19 eV. Its wave nature is invisible at tested scales. The framework's distinctive content then lies entirely in how galaxies arrange that mass (the law, a₀ tied to ρ_DE). As CFG472/473 show, the mechanism for that arrangement is supply-limited, needs an outward force and is nonlocal.

**Controls.**
- K1 PASS (Segue 1 reproduces CFG440 s03).
- K2 PASS (CFG367's light end read from its JSON: 2.013–4.345e-20 eV).
- MUTATE (M_law ×20): NOT COLD-DOMINATED, so the bound is not applied: detected, exit 1.
