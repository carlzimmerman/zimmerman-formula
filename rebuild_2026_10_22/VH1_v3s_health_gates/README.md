# VH1_v3s_health_gates: v3s PASSES Codex's three KT40/KT42 health gates on both footings

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not theory closed.
**Adopts nothing.** The 10-24 verdict (v3s fails as gravity and cosmology: clusters, growth/CMB, hosted dwarfs, the Milky
Way joint fit) and the owner's 11-04 FN1 decision (no action selected) stand.

Criteria: `FROZEN_CRITERIA.md`, commit 837119737f, plus amendment A1 (a check typo, no line changed).

## Question

KT40/KT42 (branch `codex/kt33-kt42-research-closeout`, c1ac71c574) showed that the fixed-length curvature response
(p = 9/8, ℓ = 3 kpc), which had passed the four Milky Way cuts and Cassini Q2, fails three physical-health checks:
outward vertical force in the outer disc, negative dwarf binding virials in an external field, and planets by ~1e4 on
AZ11/AZ12. v3s is the only form in the record that passes the Solar System (AX1, C6P), and it has its own fixed length
L★. These three checks had never been applied to it.

## Result

| gate | canonical | alt | the KT39/KT42 response, for comparison |
|---|---|---|---|
| **G1** MW vertical-force sign, 15 / 12 baryon models (P4's four + X5's passing cells) | **PASS**: 0 outward cells of 2,608 in every model; ∂Φ/∂z(12, 0.3) +18.6 to +28.1 M☉ pc⁻² | **PASS**: 0 outward; +21.2 to +29.7 | −843.8 / −936.1 (km/s)²/kpc at (12, 0.3): outward |
| **G2** dwarf scalar virial, 4 objects × 41 Υ × 9 η (1,476 per footing) | **PASS**: W > 0 in all 1,476; lowest σ_W 0.80 km/s (Draco, Υ 1, η 3) | **PASS**: W > 0 in all 1,476; lowest 0.80 km/s | 1,805 of 2,952 negative; canonical Draco Υ 2, η 0.01: σ² = −19.34 (km/s)² |
| **G3** planets, AZ11 radial / AZ12 precession, six planets | **PASS**: worst Mars, Z 0.052 / 0.053 (−7.95e-5 mas/yr) | **PASS**: worst Mars, Z 0.047 / 0.048 | 16/16 fail; Mars Z ≈ 16,500, Saturn ≈ 9,500 |

**Overall: PASS on both footings.**

- **G1.** The smallest ∂Φ/∂z/|∇Φ| in the region (R ≤ 25 kpc, 0.02 ≤ z ≤ 5 kpc) is +0.0096 to +0.0118, at the region's
  outer, lowest corner (R 23.8, z 0.024 kpc). It is positive everywhere. The L★ = 0 (AQUAL) twin is the same: 0 outward
  in every model. The reason is the one written in the criteria: v3s's static field has no Hessian stress. KT40's
  outward force came from its B term (−1,445 against Newton's +350 at (12, 0.3)).
- **G2.** The external field lowers the virial, as it should (1,312 of 1,312 nonzero-field configurations sit below their
  isolated value), but it never crosses zero. At Υ 2 and η = 0.01, canonical Draco has σ_W 2.87 km/s (isolated 4.26).
  KT40's response gives a negative virial there. The grid ladder (24/decade, Nt 48, Υ 1/2/3) agrees in sign everywhere,
  with a largest relative change of 0.29 %. Including L★ moves σ_W² by at most 11 % / 12 % from AQUAL, at the dwarf
  centres; the sign never changes.
- **G3.** The v3s anomaly inside L★ is the hedgehog GM☉/L★², 2.96e-16 m/s² (canonical, L★ 21.7 pc) and
  2.66e-16 (alt, 22.9 pc). It is about 3.2e5 times smaller than the constant ≈ a₀ tail that KT42's response kept. At L★ 24 / 50 /
  90 pc Mars falls to Z 0.043 / 0.010 / 0.003. Against C6's tighter dg_tight, Mars is 0.21 / 0.19 of its bound at the
  lower-bound L★.

Context, not graded: σ_W against the observed σ★ (|σ − obs| ≤ 2 err). Draco is never within 2σ at any η. Sculptor is
within 2σ up to η 0.03, Leo II up to 0.01 and Fornax up to 0.1. This is the hosted-dwarf shortfall that the 10-24 verdict
already counts as a FAIL (U1/X1). It is not revisited here.

## What this means

On these three gates, v3s's AQUAL-type static sector, screened by L★ near masses, is healthy where Codex's curvature
filter is not. KT40's failure modes come from Hessian (curvature) stress. v3s screens with a stiffness on the auxiliary
field's divergence instead, and that leaves the galaxy-scale field free of the stress. So v3s, option (a) in AX1, is now the
only route in the record that passes Cassini Q2, the planets (radial and precession), the MW force sign and dwarf virial
positivity, on both footings. Option (b), a smoothed-QUMOND action with a fixed length, is the family KT33–KT42 tested,
and it fails.

This does **not** fix anything v3s already fails. The MW joint fit still misses: K_z(R₀, 1.1) here is 76.7–80.9 in X5's
corner and 90–110 on P4's models, against 66.4 ± 2.2. The other failures also stand: hosted dwarfs, clusters, growth/CMB and
the radiation era. The owner's FN1 call is unchanged.

## Checks: 40/40 (MW), 8/8 (dwarfs), 1/1 (planets) PASS

| check | result |
|---|---|
| K1 Newtonian Plummer virial | 1.07665 vs 1.08196 (km/s)², 0.49 % (both footings) |
| K2 deep-MOND AQUAL virial (2/9)√(GMa₀) | 0.31 % (canonical), 0.31 % (alt) |
| K3 momentum, external-field solves | max \|F_z\|/∫ρ\|∇φ\| 1.1e-3 (line 2e-2) |
| K4 P4 reproduction, B1 canonical L★ = 0 | K_z(R₀) 92.283 vs 92.3 |
| K5 X5 best canonical cell at L★ 24 pc | K_z 76.656 (76.66), v_c 229.710 (229.71), after A1 |
| K6 AZ12 orbit oracles | max err 8.1e-13 |
| K7 residuals | MW ≤ 8.8e-11, dwarfs ≤ 1.0e-10 (line 1e-8) |

**MUTATE twins bite.** Non-Newtonian part reversed and tripled: G1 FAIL (575–793 outward cells, ∂Φ/∂z(12, 0.3)
−13.4 to −22.9); G2 FAIL (328/328 configurations W ≤ 0 per footing). Planet anomaly × 1e3: G3 FAIL (Mars Z 52 / 47).
**Reruns are byte-identical** (planets JSON `cmp`; MW B1 rows identical apart from wall time).

## Limits

- **G3 is carried, not re-solved.** The hedgehog is C6/C6P's result: it agrees with C6's Route F monopole to four digits,
  and C6P checks it at high precision. Only the monopole is orbit-averaged. There is no ephemeris refit and no
  multipoles, as in AZ12 and KT42.
- **G1 is the isolated Milky Way** on P4's half grid (equatorial symmetry). There is no external field or LMC, and no
  hydrostatic gas model beyond the sign requirement.
- **G2 uses fixed, centred Plummer spheres in a uniform field,** with the field axis as the grid axis. There are no tides,
  orbits or anisotropic line-of-sight predictions. The η → g_e map assumes a uniform background (g_e = η ν(η) a₀), as
  KT40 states.
- **The μ_K² term is dropped,** as in P4 and X5. v3s's khronon dust (U1) is not part of these gravity-only gates.
- **A1:** the first MW run's K5 rebuilt the wrong X5 cell (R_d 2.1 instead of 1.933). That output is kept as
  `vh1_mw_FIRSTRUN_K5BUG.*`. Its G1 rows are identical to the rerun's.

## Files

`vh1_gates.py` (P4's solver and X5's loader imported read-only; AZ12's rate re-implemented). Outputs:
`vh1_{planets,mw,dwarfs}.json/.out`, `_MUTATE`, `_RERUN`, `_runtime.json`. Single thread, peak RSS 0.62 GB, total
≈ 25 min.

```bash
python3 vh1_gates.py --part all      # exits non-zero on any failed check
```
