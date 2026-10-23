# P2_spec_isolated_lensing: lensing at 0.4–3 Mpc around spectroscopically isolated GAMA galaxies, and v3's external field

## Verdict: UNDECIDABLE (N too small), on both footings

The primary sample has **N = 2,251** spectroscopically isolated lenses. Separating v3 with zero external field (a) from
v3 with the field the catalogue implies (b) at 3σ needs about **N ≈ 26,500 (canonical) / 22,000 (alt)**, roughly
10× the sample. That is about 10× GAMA's 180 deg² at GAMA depth and completeness.

Two results hold on either reading:
1. **The F2 "EFE tension" does not come back in clean data.**
   - F2's photo-z isolated sample allowed only y_e ≲ 3e-5, because the data sat above every EFE prediction.
   - Here the data are never above v3 for any field on the grid: y_allow reaches the top of the grid.
   - Beyond 1.1 Mpc the stack sits *below* the zero-field prediction: A_O2 = −0.16 ± 0.42 (canonical, 2.8σ) /
     −0.15 ± 0.38 (alt, 3.0σ). It is consistent with the catalogue-field prediction (b): −0.22 ± 0.65 / −0.20 ± 0.59.
   - Smallest grid field the data accept (A1, post-result): y_e = 1e-4. The catalogue implies a median 6.6e-5 / 5.4e-5.
2. **The catalogue's own baryons imply a field about 2× F2's tolerance.**
   - Median y_e for the S3 lenses: 6.6e-5 canonical (16–84 %: 1.7e-5 to 2.0e-4).
   - Brackets: 2.6e-5 with no completeness correction, 1.1e-4 summing to 20 Mpc.
   - If all cosmic baryons traced the galaxies, the field would be 1.4e-3, and 8.8e-3 if the dust traced them too
     (ΛCDM-processed ratio, flagged, not used).
   - In 1.1–2.6 Mpc, (b)'s model is 0.63 of (a)'s.

The larger secondary sample S1 is reported only, not graded. It has 10,620 lenses with a host veto inside 1 Mpc, hosts
beyond 1 Mpc modelled.
- It sits 3.5σ (canonical) / 4.0σ (alt) below the zero-field prediction at 1.1–2.6 Mpc.
- It is consistent with (b).
- Its own decisiveness is S = 2.6σ / 2.9σ, just short of the frozen 3σ.

κ = ½ FITTED. Footings are never pooled. No dark-matter particle. Not theory closed. Nothing here says the data favour the
framework.

## The numbers (S3, primary; A = data / model, F2's estimator; data vector Δ = L − I3)

| | A_in (≤ 0.31 Mpc) | A_O1 (0.4–1.1) | A_O2 (1.1–2.6) | classes (O1, O2) |
|---|---|---|---|---|
| canonical (a) y_e = 0 | 1.83 ± 0.30 | 0.57 ± 0.38 | −0.16 ± 0.42 | consistent, between (−2.8σ) |
| canonical (b) catalogue y_e | 1.83 ± 0.30 | 0.62 ± 0.40 | −0.22 ± 0.65 | consistent, consistent |
| alt (a) | 1.68 ± 0.28 | 0.52 ± 0.35 | −0.15 ± 0.38 | consistent, over (−3.0σ) |
| alt (b) | 1.68 ± 0.28 | 0.56 ± 0.37 | −0.20 ± 0.59 | consistent, between |

- **Decisiveness.** Model (b)/(a) with (a)'s weights is 0.95 (O1) and 0.63 (O2), so S = 0.87σ (canonical) / 0.96σ (alt).
  The frozen line needs 3σ, so the verdict is UNDECIDABLE (N too small).
- **Profile in Msun/pc², canonical.**
  - Δ at 0.41, 0.55, 0.75, 1.02, 1.39, 1.89, 2.57 Mpc: 8.0, 0.3, 1.9, 0.4, 0.4, −0.8, 0.1.
  - σ at the same radii: 4.4, 2.9, 2.3, 1.9, 1.2, 0.8, 0.9.
  - Model (a): 5.3, 4.0, 3.0, 2.3, 1.7, 1.3, 1.0. Model (b): 5.2, 3.9, 2.8, 2.0, 1.3, 0.8, 0.5.
  - The full 15 × 15 jackknife covariance is in the JSON.
- **Robustness tags** (reported only; canonical (a) / (b) classes for O1, O2):
  - Raw L − R, with no hole subtraction: consistent/over and consistent/between. A_O2 is −0.61 ± 0.47.
  - Without the neighbour term: consistent/between and consistent/consistent.
  - Lower-bracket field: consistent/between.
  - S1: consistent/over (3.5σ) and consistent/consistent.
- **One at a time** (T_own only; A_O1 / A_O2 at (a), canonical):
  - f_hot 0 / 1: 0.66 / 0.51 and −0.18 / −0.15.
  - M★ −0.2 / +0.2 dex: 0.64 / 0.51 and −0.18 / −0.14.
  - h 0.672 / 0.686 and Σ_crit ± 3 %: each moves A_O1 by ≤ 0.02.
- **Uniform-field scan** (canonical, A_O2): 0 → −0.16 ± 0.42; 3e-5 → −0.19 ± 0.50; 1e-4 → −0.23 ± 0.72;
  1e-3 → −0.63 ± 2.0. The error grows as the model shrinks, which is why the sample cannot reach 3σ.
- **Inner range (not this lane's question).** Inside 0.31 Mpc the data sit at 1.83 ± 0.30 / 1.68 ± 0.28 of v3's
  baryons-only profile. v3 has no dust term (F3).
  - The lens/iso-random source-weight ratio is 1.29–1.38 at 35–65 kpc and 1.05 at 2.6 Mpc. Part of that is
    lens-associated dilution, which is uncorrected and would raise the data. Part is footprint: iso-randoms fall more
    often in masked areas.
- **Environment-only stack** I3 − R at 0.4–2.6 Mpc: 2.3, −3.9, −0.2, −0.1, −1.5, −0.1, −0.2 ± (2.6, 1.4, 1.3, 0.8, 0.6,
  0.4, 0.4). The model predicts −0.01 to −0.34 (a) and −0.003 to −0.05 (b). Both are consistent and noisy.
- **Lens properties.**
  - Median z 0.234; median log M★ 10.78.
  - 4.5 % are G3C non-central group members (G3C's FoF is ΛCDM-mock-tuned, so this is reported only).
  - GKV minus LePhare(+0.15) in G09: +0.05 dex, NMAD 0.16 (736 lenses).

## What was done

The criteria and ledger were committed alone first (a1bc996fa8). AMENDMENT_A1 is post-result and changes no line.

**Inventory.** The table is in `FROZEN_CRITERIA.md` §1. Only GAMA DR4 G3C can define a complete spectroscopic
environment over KiDS-1000: 184,081 redshifts at r < 19.8 in G09, G12 and G15. The other catalogues fail:
- DESI DR1 BGS is fibre-incomplete. CFG316 found a median of 70 unobserved targets within 3 Mpc of a lens.
- 2MRS has only 1,030 galaxies in the KiDS footprint.
- 6dFGS FP and ALFALFA–SDSS are selected subsets.
- No SDSS or BOSS spectroscopic catalogue is on disk.

GAMA's completeness against KiDS-bright at r < 19.5 is 0.970 (K5).

**Isolation rule (frozen).**
- Lenses: 0.05 < z < 0.5; 8.5 ≤ log M★ < 11; KiDS-bright LePhare M★ + 0.15, rescaled to the spec-z distance.
- Completeness: the lens's own mass must be at or above the catalogue's 95 % completeness mass at its redshift.
- Host veto: no G3C galaxy at least as massive within R_iso (projected) and |Δv| < 1000 km/s. Proxy-mass neighbours
  carry a 0.30 dex margin.
- Edge: the lens lies at least R_iso from every box edge.
- S3 has R_iso = 3 Mpc and 2,251 lenses. S1 has R_iso = 1 Mpc and 10,620.
- A B21-style complete veto at 0.1 M★ is possible for only 29 GAMA lenses. A 0.1 M★ neighbour is fainter than
  r = 19.8 at almost every lens redshift. By this 95 % mass-completeness test, a 0.1 M★ spectroscopic veto (B21's
  rule) cannot be made complete on GAMA.

**Measurement.**
- Own vectorised estimator over F1's KiDS-1000 reader cache: Z_B > z_l + 0.2, inverse-Σ_crit² weights, native
  distances (flat Ω_m 0.3085, h 0.679), 15 bins over 0.03–3 Mpc, 1+K = 0.9853.
- 36 patches with a paired delete-one jackknife.
- K0a reproduces F1's per-cluster stack to 3e-12. K0b reproduces the record's CFG110 per-lens sums exactly
  (ΣWW ratio 1.0000000). So this is the same shear data read the same way.

**How the hole is handled.**
- Data: 9,004 iso-random points carry the same veto, z and M★ draws and edge margin as S3. Their stack (I3) is the
  lensing of the vetoed environment with no galaxy at the centre. The data vector is Δ = L − I3.
- Model: m = T_own + [T_nbr(L) − T_nbr(I3)].
  - T_nbr is every catalogued neighbour's own v3 profile within 6 Mpc and 1000 km/s. It is computed exactly from the
    azimuthal identity ⟨ΔΣ_t⟩ = M(<R)/πR² − Σ_ring and summed linearly.
  - Linear summation is exact in the EFE-linearised regime and an upper estimate at y_e → 0.
  - The term raises the model by about 20 % (O1) to 30 % (O2).
- No halo model, bias or fitted amplitude enters.

**Model (v3).**
- Field equation: AQUAL with μ = x/(1+x), solved with F2's point-mass-in-a-uniform-field solver (imported read-only)
  on a 10-node y_e grid.
- Baryons: F2's T_central inventory (M★, cold gas from B21's relation, hot CGM at 0.5 M★).
- No dust term. BS24's μ_K²ψ term is not included (as in S2).
- (a) y_e = 0 for every galaxy.
- (b) Every galaxy's own Newtonian field from the catalogue's baryons at 1–10 Mpc (3D, redshift space). Each galaxy is
  weighted by 1/C_b(z) from the catalogue's own 1/V_max baryonic mass function: C_b = 0.78 / 0.50 / 0.22 at
  z = 0.1 / 0.2 / 0.3. Galaxies hold 0.048 of Ω_b ρ_crit. Then μ(x_e) x_e = y_e.

**Checks.** 8/8 PASS: K0a, K0b, K1 (two), K2, K3, K4 (cross shear p = 0.09) and K5.
`--mutate` uses cross shear everywhere; K0a, K0b and K4 then fail (5/8) and the run exits 1 (`*_MUTATE.*`).

**Compute.** Run as `OMP_NUM_THREADS=1 nice -n 15 python3 p2_spec_isolated_lensing.py <F1 reader cache> <scratch dir> [--mutate]`
(the cache is `f1_extract.py`'s output). Single thread, nice 15. The run has two sequential processes, A (sources, K0, shear measurement) and
B (model, scoring). Peak RSS is 0.84 GB in A and 0.83 GB in B; the run takes 47 s + 181 s. No downloads.

## What this does not show

- It does not solve the AQUAL many-body problem. The neighbour term is a linear sum of single-galaxy profiles, and the
  external field is a uniform-field boundary condition set by the catalogue's Newtonian vector field.
- The catalogue field holds only catalogued galaxies' baryons, corrected for galaxies below the flux limit. The
  diffuse baryons (95 % of Ω_b) and v3's BS dust are not in the central field. If they traced the galaxies, the field
  would be 20–130× larger, and (b)'s outer prediction would be far below (a)'s.
- No boost correction is applied. The lens/iso-random weight ratio at 1.1–2.6 Mpc is 1.05–1.07, small next to the
  errors.
- B21's own GAMA lens list and masses are not on disk. Its "spectroscopically isolated" sample uses a 0.1 M★ veto that
  GAMA cannot complete.

## Next step

An outer-lensing test of the EFE needs about 25,000 host-free, completeness-limited spectroscopic lenses over KiDS-like
shear. That is GAMA's depth and redshift completeness over roughly 10× its area: WAVES, or DESI BGS once its fibre
completeness supports a 3 Mpc veto (DR2 or later), crossed with KiDS-Legacy, DES Y6 or HSC.

On the data on disk, S1 is the strongest hint: 10,620 lenses, 3.5–4.0σ below zero field, consistent with the
catalogue field, S = 2.6–2.9σ. Promoting it would need a frozen re-specification with its own hole control.
