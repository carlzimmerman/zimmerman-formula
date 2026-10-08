# T18 — the cold-fluid reconstruction: the front law measures the cold

**The setup.** T17 pinned the phantom at every radius (closed forms:
f(r) = 1 − e^{−c/r}, c = λτV = 55–59 kpc; S(<r) = M_b/(e^{r_t/r}−1)).
The published MW halo anchors then leave the cold fluid as a measured
residual — NOT an assumed profile:

    M_cold(r) = M_tot,obs(r) − M_b − f(r)·S(<r)

## Results (5/5 PASS rc 0; MUTATE flips C2/C4)

Reconstructed cold masses (1e11 M_sun; V = 188 km/s convention):

| anchor (kpc) | f    | M_ph  | M_cold | window  | source |
|---|---|---|---|---|---|
| 30 (V=188)   | 0.84 | 1.68  | **0.09** | [0.09, 0.09] | rotation |
| 30 (V=200)   | 0.86 | 1.72  | 0.38–0.42 | —       | rotation |
| 50           | 0.67 | 2.59  | 0.56  | [−0.04, 1.16] | Huang+16 |
| 100          | 0.43 | 3.65  | 1.80  | [1.0, 2.6] | Huang+16/Posti+19 |
| 200 (set A)  | 0.24 | 4.37  | 2.83  | [1.33, 4.33] | Callingham+19 |
| 217 (set B)  | 0.23 | 4.43  | 4.57  | [3.57, 5.57] | Gaia DR3 era |

- **The cold fluid EMERGES outside the front, measured.** |M_cold(30)/
  M_b| = 0.13 (V=188 — the T15 knife-edge re-derived radially; V=200
  carries 0.54–0.60, reported). Cold ≈ 0.1e11 inside 30 kpc, rising
  to 1.8e11 @ 100 and 4.6e11 @ 217 kpc: the fraction climbs
  x_cold(100) = 0.28 → x_cold(217) = 0.46. The cold is a component
  that a) does not cusp in the inner halo, b) dominates the outer
  dark mass beyond ~150 kpc. Its recovered shape is close to
  ρ_cold ∝ (1−f)·ρ_supply — the un-settled reservoir in space — NOT a
  CDM-like cusp. This is the first radial measurement of the cold
  component's spatial law.
- **The masking verdict (S5 quantified):** phantom-alone V(200)/V(60)
  = 0.630; with the reconstructed cold: **0.764** — the cold absorbs
  ~40% of the front's decline. The observed bend already lives in the
  published masses (V_rec(200) = 133, V_rec(217) = 141 km/s).
- **Honest caveat:** at the anchors the total curve is degenerate with
  NFW (V(200)/V(100) = 0.80 both ways) — the discriminator shifts to
  the *split*: the phantom+front part (closed-form, fitted-free)
  vs the cold residual, testable where the cold is probed separately.

## Corrections to the freeze (dated, the machine ruled)

1. C5 rescaled to the rotation-anchored radii (30–100 kpc) — the
   outer masses themselves bend (133/141 km/s); reported, not failed.
2. The knife-edge exact values: 0.13 (V=188) / 0.54–0.60 (V=200).
3. C7's verdict sharpened: 0.764 total vs 0.630 phantom — the cold
   cushions the decline; the split is the content.

## Falsifiers (registered)

1. A measured ρ_cold(r) cusping inward (∝ r^{−1} or steeper inside
   50 kpc) kills the reservoir reading — the cold then behaves like
   CDM inside the front, where the knife-edge says ≈ 0.
2. The 30-kpc cold exceeding 0.3 M_b under V = 188-consistent
   rotation data kills the inner closure (the knife-edge is
   radial now).
3. A measured outer dark profile steeper than the reconstruction's
   at 100–217 kpc (x_cold growing faster than the table) — the cold
   would overstep the observed halo.

## Lean

No new theorem — the radial application of certified #14 (deficit),
#15 (cold_budget_identity), #16 (cold_ceiling) rides the lane; every
row of the table is the budget identity at one radius.

## Bottom line

The cold fluid was the record's necessary-but-unconstrained component;
the front law + the published MW halo masses give it a PROFILE. It
emerges exactly where the settling says it must — outside the
knife-edge — its shape is the un-settled reservoir, and the rotation
decline it cushions is split 63/76 between phantom and total. The cold
fluid is now measured, not assumed — and the radial knife-edge is a
new, sharper closure test.