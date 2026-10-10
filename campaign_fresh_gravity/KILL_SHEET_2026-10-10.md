# Kill sheet, 2026-10-10: every live prediction, what tests it, when, and what kills it

Purpose: score each incoming result in an hour, from committed sources only. κ = ½ is FITTED (current estimate 0.42 ± 0.10,
CFG493). The two footings (9.36e-11 / 1.13e-10 m/s²) are never pooled. The cold energy's mass is still required. A survival is
never a confirmation, and nothing here may be cited as "the data favour the framework". Dates marked ~ are estimates.

## Gravity: the framework

| # | prediction | source | test, date | KILLS it | survives |
|---|---|---|---|---|---|
| G1 | Wide binaries, settling model: γ = 1.000 (Arm C) | PREREGISTRATION_DR4.md, Amdt 21 | Gaia DR4, **2 Dec 2026**; z_C = (γ̂ − 1)/√(σ_fit² + 0.02²) via `dr4_ready_1/arm_c_rows.py` | γ̂ in 1.084–1.23 with Arm C's stability requirements passing | \|z_C\| < 2. Cannot separate the model from Newton/ΛCDM |
| G2 | Wide binaries, law-as-force (Arm A) | prereg, Arm A | DR4 | scored by Arm A's frozen rows; its floors 1.1614 / 1.1917 sit 5.8 / 6.8 σ_tot above Arm C, so a Newtonian γ̂ disfavours Arm A | Arm A's rows |
| G3 | Milky Way outer slope, 15–27.5 kpc | STANDING_2026-10-09_law (CFG532b) | DR4 distance scale | the shape stays excluded (now Z −3.6 / −3.9) once DR4 distances are in | DR4 distances move the slope into the band |
| G4 | Milky Way K_z map, round cold energy vs phantom disc | CFG514, 516 (32/32 cells now) | DR4 | DR4 K_z reverses the cell preference | preference holds |
| G5 | a₀(z) tracks dark energy: a₀(z)/a₀ = √(ρ_DE(z)/ρ_DE,0); with DESI DR2 w0wa, a +6% bump near z ≈ 0.4, then ≈ 0.74 by z = 3. FLAT only if w = −1 | book/26; feedback rule 10-06 | DESI DR3 (~2026–27), then BTFR offsets: ALMA ~2028–30, ELT/HARMONI 2030s | a robust RISE of a₀ with z (e.g. ∝ H(z): ×3.8 at z = 2.5) at ≥ 3σ with measured gas | offsets consistent with the DE-tracking curve (or flat if DR3 gives w = −1) |
| G6 | a₀ at z ≈ 2.5 is power-limited | STANDING_2026-09-29 §a₀ high z | any new sample | — (the 0.25-dex mass floor caps it at 2.3σ vs a₀ ∝ H(z)) | needs measured gas plus outer dispersion: 3–5σ power, subject to the ~2.3σ correlated floor |
| G7 | KURVS-like z ≈ 1.5 discs need cold gas ≈ 4 M* under flat a₀ | CFG141 | measured CO / gas fractions | measured μ ≤ 1.5 disfavours flat a₀ at z ≈ 1.5 (under the constant-σ correction) | μ ≈ 4 measured |
| G8 | SME boost dipole s^TX = −8.68e-10 (canonical) / −1.048e-9 (alt), per-body reading. VOID as a falsifier under α = 2 (Amdt 4–5) | prereg §2 | ephemeris fits (INPOP/EPM updates) | NO VERDICT by construction under α = 2 (§2's DETECT / KILL / WRONG-SIGN-KILL bands are void, Amdt 5) | inside the bar (now 0.67σ, margin 1.50× / 1.24×) |
| G9 | The early-type failure (KiDS / SLUGGS, ≈ 30–40% mass short at 50–100 kpc) is physical, not a survey systematic | STANDING_2026-10-09_law | an independent lensing survey (DES Y3; owner declined the download 10-09) or old-population σ_z | an independent survey reproduces the shortfall → the law lacks spheroid physics (already the working reading) | the shortfall vanishes in an independent survey → KiDS/SLUGGS systematic |

## Atomos: the lepton sector (CONDITIONAL on TM1, Dirac neutrinos, m₁ = ρ_Λ^{1/4})

Certified in Lean: lean_2026/LEPTON_CHAIN{,_2,_3}.lean, MODULAR_S4_FIXED.lean. Numbers: atomos FS16 (local).

| # | prediction | test, date | KILLS it |
|---|---|---|---|
| A1 | TM1: sin²θ12 ∈ [0.3162, 0.3198] for s13² ∈ [0.020, 0.025] (LEPTON_CHAIN L2) | JUNO next releases, ~2027–28 (rough) | JUNO's whole 3σ range outside the window (central now 0.309) |
| A2 | TM1: sign(cos δ) = sign(s23² − ½) (L4); cos²δ ≤ 0.21, i.e. δ within 27.3° of 90° or 270° (L9); \|J\| ≥ 0.0277 (L10) | NOvA/T2K updates; DUNE/Hyper-K 2030s | δ near 0° or 180°; or the measured octant and the sign of cos δ disagree |
| A3 | m_ββ = 0 (Dirac) | LEGEND-1000 / nEXO, 2030s | any 0νββ signal (also kills FS11's window) |
| A4 | Σm_ν ≈ 0.0614 eV (m = 2.24 / 8.95 / 50.3 meV, NO) | DESI DR3 + Euclid + CMB-S4, ~2030 | a 95% bound below 0.0609 eV (L5's lower edge) |
| A5 | Normal ordering (IO is excluded at DESI's 95% ΛCDM bound, L11) | JUNO ordering, ~2030 | inverted ordering established |
| A6 | m₁ < 5.0 meV (DESI, 3σ splittings, L12) | cosmology | — (a data bound, not a framework prediction) |
| A7 | Under A3, DESI caps a₀ < 4.99 × canonical (L13) | — | already satisfied by both footings; weak |

Closed doors (do not re-open without a new mechanism): residual symmetries (FS01–03), textures (FS06/13c), modular A4 (FS07) and
modular S4 fixed points (FS17), swampland × evolving DE (FS18), Koide routes (KOIDE_*), torus generations.

## Release calendar
- **2 Dec 2026: Gaia DR4.** G1–G4. Run RELEASE_DAY_CHECKLIST.md, then `arm_c_rows.py`. Owner-side: a Gaia archive account.
- **~2026–27: DESI DR3.** G5 gate. If w → −1, a₀(z) is predicted flat, and the distinctive evolution goes silent.
- **~2027–28: JUNO θ12.** A1.
- **~2028–30: ALMA BTFR offsets.** G5 sign. **~2030: DESI + Euclid + CMB-S4.** A4. **2030s: DUNE/Hyper-K, LEGEND/nEXO, ELT.** A2, A3, G5 shape.
