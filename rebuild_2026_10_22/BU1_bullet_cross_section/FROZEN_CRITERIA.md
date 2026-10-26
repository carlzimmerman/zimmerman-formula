# BU1_bullet_cross_section — FROZEN CRITERIA + ASSUMPTION LEDGER (committed alone, before any script or number)

Written 2026-10-25. κ = ½ FITTED. Footings canonical / alt, computed and graded separately, never pooled. Cold dark
energy: a collisionless, self-coupled field component, not matter and never a particle; "cross-section per mass" s is
the coupling's rate coefficient per unit cold-energy mass density, nothing more. Nothing here says the data favour the
framework or ΛCDM. Not "theory closed". No download; no knob scan; light compute (analytic, one thread).

## 0. Question

OS1's core law fixes the cold dark energy's self-interaction with no free number. Is the implied s(v) compatible with
merging-cluster bounds, and is it sane at dwarf speeds (including gravothermal collapse within a Hubble time)?

## 1. Derivation (fixed now; every step is a certified identity or a stated premise)

- Exponent: n = 2 q_f − 1 (LN2 `q_to_n`), q_f read from `OS1_core_law_out_of_sample/os1_out_of_sample_results.json`
  (canonical 0.892, alt 0.748 ⇒ n = 0.784 / 0.496; LN2 `os1_n_values`).
- Normalisation (LN1 T7 solved for K at the SC1 anchor): s·v = K σ^(1−n),
  K = 9 σ_ref^(1+n) / (4πG t Σ_a0²), σ_ref = 70.50 km/s, Σ_a0 = a₀/(2πG), t = 13.8 Gyr.
- a₀ per footing as in OS1/DW1: canonical 9.3603e-11, alt 1.1312e-10 m/s². G = 6.674e-11, yr = 3.156e7 s.
- Speed convention: v = (4/√π) σ (mean relative speed of a Maxwellian; LN2 `knudsen_closed_form` premise). Hence
  **s(v) = K (√π/4)^(1−n) v^(−n)**, reported in cm²/g (1 m²/kg = 10 cm²/g) at v = 10, 50, 200, 1000, 1900, 3000,
  4700 km/s.

## 2. Bounds (where found; values not in the repo are PROVISIONAL from memory)

Every bound below is a velocity-independent (constant s) bound applied at the stated evaluation speed. That is the
standard way such bounds are quoted; the transfer to a falling s(v) is a premise (ledger L6).

| id | bound | eval speed (fixed now) | source / status |
|---|---|---|---|
| B1 | Bullet Cluster, Randall+2008: s < 1.25 cm²/g | 3000 km/s (lower end of the 3000–4700 km/s collision range, so the larger s; also reported at 4700) | NOT in `citations/REFERENCES.bib` (only Markevitch2004 on the Bullet, no number in the record). Value from memory: **PROVISIONAL** |
| B2 | Harvey+2015, 72 mergers: s < 0.47 cm²/g | 1000 km/s (conservative low end for the merger sample) | bib `Harvey2015`; value in record CFG1 A09d (CONTESTED there) |
| B3 | record's own merger bound (CFG725, framework-native merger model): s ≤ 0.708 cm²/g | 3000 km/s | `campaign_fresh_gravity/CFG725_sidm_window/README.md`; its Bullet masses are PROVISIONAL there |
| W | Wittman+2018 re-analysis of the Harvey offsets: ~2 cm²/g (looser) | 1000 km/s | bib `Wittman2018`; value in record CFG1 A09d |
| C1 | cluster halo cores (Jeans), Sagunski+2021: s < 0.35 cm²/g (95%) | 1900 km/s (their cluster mean relative speed) | record `sol61_push/.../EVIDENCE.md` (WebFetch read ⇒ **PROVISIONAL** per the record's rule); not in bib |
| C2 | cluster cores, Andrade+2022: s ≲ 0.13 cm²/g (95%) | 1900 km/s | memory only: **PROVISIONAL**, reported only |
| C3 | cluster halo shapes, Peter+2013: s ≲ 1 cm²/g | 1900 km/s | memory only: **PROVISIONAL**, reported only |
| C4 | Kaplinghat+2016 core fit: s ≈ 0.1 cm²/g near ~1500 km/s, ≈ 2 cm²/g near ~50 km/s (a fit, not a bound) | 1000 and 50 km/s | memory only: **PROVISIONAL**, comparison only |

## 3. Merger class (per footing; graded on B1, B2, B3 with W as the tension ceiling)

| class | rule |
|---|---|
| **PASSES BOUNDS** | s ≤ B1, B2 and B3 at their eval speeds |
| **TENSION** | exceeds at least one of B1/B2/B3, but s(3000) ≤ 1.25 and s(1000) ≤ 2 (W) |
| **EXCLUDED** | s(3000) > 1.25 (B1) or s(1000) > 2 (W) |

The lane verdict needs both footings in the same class, else UNDECIDED. Qualifier (graded, does not change the merger
class): **C1 PASS / C1 FAIL** on s(1900) ≤ 0.35. C2–C4 reported only.

## 4. Dwarf sanity (per footing)

- Report s(10), s(50).
- **Gravothermal collapse.** Premise: the SIDM collapse time t_c ≈ (150/C) / (s ρ_s r_s √(4πG ρ_s)), C = 0.75
  (Essig+2019 / Pollack+2015 form; memory, **PROVISIONAL**), with the core (ρ₀, r₀) standing in for (ρ_s, r_s)
  (ledger L8). With the core law's ρ₀ s v t = 1 and the isothermal ρ₀ r₀² = 9σ²/(4πG), this is a closed form
  t_c / t = (150/C) · v / (3σ), independent of σ, K and n. Computed, not assumed.
- Dwarf classes: **SANE** if s(10) ≤ 100 cm²/g (literature scale above which dwarf/subhalo collapse becomes generic;
  memory, PROVISIONAL) and t_c/t > 1 at every σ; **COLLAPSE RISK** if t_c/t ≤ 1 anywhere; **EXTREME** if s(10) > 100.
- **How DW1's Γt = 1 interacts (to be stated in the README):** Γt = 1 is the core-*formation* condition and is imposed
  by the law, so it fixes ρ₀ for given s; it cannot by itself say whether a halo is collapsed. The t_c/t ratio is the
  independent statement, and the premise "cores are cored, not collapsed" is only self-consistent if t_c/t > 1.

## 5. Checks (all must pass; else the lane stops and reports)

- K0: n from the JSON equals 0.784 / 0.496 to 3 decimals (LN2).
- K1: the Knudsen number rebuilt from s (λ = 1/(ρ₀ s), H = σ/√(4πGρ₀), ρ₀ = 4πGΣ²/(9σ²)) matches LN2's closed form
  Kn_ref = (4/(3√π)) · 2a₀t/σ_ref and DW1's printed Kn at 5 and 1000 km/s to < 1%.
- K2: dimensional check s·v·ρ₀·t = 1 at σ_ref to 1e-9.

## 6. MUTATE (separate outputs, `_MUTATE` suffix)

n → −n (cross-section rising with velocity, LN1's original window direction). Expected: the merger class worsens to at
least TENSION on at least one footing, showing the grade is driven by the derived exponent. If MUTATE stays PASSES
BOUNDS on both footings, the grade is reported as INSENSITIVE TO n and the lane says so.

## 7. Assumption ledger

- L1 Isothermal core ρ₀ r₀² = 9σ²/(4πG) (LN1 T7 premise).
- L2 Core condition ρ₀ s v t = 1 at t = 13.8 Gyr for every system (LN1 T7, LN2 `gamma_t_one`); clusters are younger,
  which is not modelled (it would raise their implied ρ₀, not s).
- L3 Anchor Σ(σ_ref) = Σ_a0 = a₀/(2πG) (SC1/OS1); σ_ref = 70.50 km/s.
- L4 Power law s ∝ v^(−n) holds from 10 to 4700 km/s (extrapolation beyond SPARC's σ range toward mergers).
- L5 v = (4/√π) σ; merger collision speeds are taken directly as v.
- L6 Constant-s bounds transfer to a velocity-dependent s at one eval speed (no momentum-transfer or angular
  weighting; Bullet-type bounds for frequent forward scattering differ, not modelled).
- L7 The cold dark energy is the whole halo mass in the merger (the bound applies to the full component).
- L8 Burkert core (ρ₀, r₀) stands in for the NFW scale (ρ_s, r_s) in the collapse-time formula.
- L9 PROVISIONAL bound values (B1, C1–C4, the collapse formula, the 100 cm²/g scale) are from memory or a WebFetch
  read; a later look-up can change them and the grade must be redone if it does.
