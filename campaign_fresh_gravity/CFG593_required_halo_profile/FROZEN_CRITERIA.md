# CFG593 FROZEN CRITERIA: which total halo mass profile do cosmic shear and KiDS galaxy lensing require at once, and can a framework settling rule make it?

Date frozen: 2026-10-10. Committed alone, before any number of this lane is computed.

Settings: κ = ½ FITTED; footings canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s², never pooled; flat a0 = κ c √(G ρ_DE); kernel ν_mono; candidate B. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing is downloaded. Other lanes are read only.

**Nature of this lane: DIAGNOSTIC and DATA-DRIVEN.** It maps which profiles the data allow. A profile found here is what the data require, NOT a framework derivation. Only the comparison in section 6 (record rules) speaks to the framework's own predictions.

## 1. Question

- Cosmic shear (CFG590) excludes the framework's settled halos: they put too much mass at ~0.1–0.5 r_ta (A_eff 1.30 / 1.46 with feedback off; EXCLUDED both footings). Only variants that do not settle the turnaround catchment inside ~r200m survive (emergent edge, r200m scope).
- KiDS isolated-lens galaxy lensing (CFG529 / 531 / 557 / 559) wants the settled edge further out (x ≈ 0.45–0.50 r_ta) and more inner mass for massive early types.
- (1) Does ANY member of a small, declared profile family satisfy both data sets at once, per footing? (2) If so, what does that profile say in words, and does any rule already on the record produce it?

## 2. The profile family (declared before fitting)

Notation per halo: catchment mass M_ta, turnaround radius r_ta, retained baryons M_b = f_ret f_b M_ta with cumulative profile m_b(r), the law's phantom of those baryons S(r) = m_b(r) [ν_mono(G m_b / r² a0) − 1] (untruncated), the ΛCDM cumulative shape M_L(r) (NFW, normalised to M_L(r_ta) = M_ta), r_M = √(G M_b / a0), supply = (1 − f_b) M_ta.

Three parameters, the same for every halo (mass dependence only through r_ta(M_ta), r_M and f_ret):
- **x_e** — settled-edge radius r_e = x_e r_ta.
- **f** — fraction of the law's phantom actually settled between r_in and r_e.
- **y** — full-law core: r_in = y r_M; inside r_in the settled cold energy is the full law phantom.

Total profile M(<r) = baryons + settled cold energy + unsettled cold energy:
- Settled: S_set(r) = S(min(r, r_in)) + f [S(min(r, r_e)) − S(min(r, r_in))] (if r_in ≥ r_e: S(min(r, r_e))).
- **Supply cap:** settled cold energy cannot exceed the supply. If S_set(r_e) > supply, the edge is pulled in to the radius where S_set reaches the supply (as CFG556's emergent edge does).
- Unsettled: density ∝ ρ_L(r) h(r) with h = 0 inside min(r_in, r_e), h = 1 − f between r_in and r_e, h = 1 beyond r_e; normalised by **mass conservation**, M(<r_ta) = M_ta. If the cumulative of h dM_L vanishes (f = 1 with r_e ≥ r_ta), the remainder is spread as M_L / M_ta (CFG556's capped rule).
- The **outer drained-shell depth** q = 1 − (unsettled density / ΛCDM density) beyond r_e is therefore NOT free: conservation fixes it. It is reported at every allowed point.
- Limits: f = 1, y = 0 is the framework's settled halo with edge x_e (CFG556's construction exactly, for a constant x_e). x_e = 1, f = 0 is baryons + ΛCDM-shaped rest (the family's NFW member).

**Grid:** x_e ∈ {0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.85, 1.00}; f ∈ {0, 0.1, …, 1.0}; y ∈ {0, 1, 3, 10} (at f = 1, y is irrelevant and only y = 0 is run). 14 × 41 = 574 points per footing. The overlap is judged on grid points only (no interpolation).

**Per data set (each lane's own machinery, read-only, with the family profile substituted):**
- **Halo model (shear):** CFG556 (masses, bias, concentration, Δ_ta, f_ret census, the declared extended baryon shape). PRIMARY baryon convention: retained baryons inside r_e (CFG556 `cen`). Declared variant: baryons to r_ta (CFG556 `emg` convention). R(k) = 1 + (P_F − P_L,ta)/P_L,std (CFG556 PRIMARY scope).
- **KiDS:** CFG529 lens groups, census f_ret and M_ta, law r_ta(M_g, a0, z), point-mass baryons M_g; M_L shape from CFG556's NFW at the census M_ta (z = 0 shape). PRIMARY convention: the own profile is the total family M(<r) to r_ta (unsettled cold energy included), flat beyond. Declared variant ("lane convention", as CFG529 / 557 / 559): the unsettled cold energy is not in the own profile (M_g + S_set, flat beyond r_e).
- **Groups:** CFG543 P2 (stellar Hernquist baryons, f_cond 0.10 catchment); r_ta from CFG556's halo_basics at the group M_ta. PRIMARY: total family profile; variant: lane convention (flat beyond the edge).
- **MW:** CFG513 / 515 `Prof` baryons (6.0e10), census f_ret and M_ta; r_ta from CFG556's halo_basics.

## 3. Constraints (each judged per footing, per grid point)

- **(a) Cosmic shear (CFG590's mapping M1, machinery exec'd read-only):** ALLOWED iff some log T_AGN ∈ {7.6, 7.7, 7.8, 7.9, 8.0} (the fiducial band) gives |Z_KiDS| < 2 AND |Z_DES| < 2. Data recalled and PROVISIONAL (KiDS-1000 A_mod 0.858 ± 0.052; DES Y3 0.82 ± 0.04). Reported variant: the full band 7.3–8.3. R is taken at z = 0 (CFG590's disclosed assumption; CFG591 is the parallel z lane; CFG592 the real likelihood).
- **(b) KiDS f30 galaxy lensing (CFG529's f30 sample, measured W30 leakage, SHMR term propagated by CFG529's `score_vecs`):** ALLOWED iff p > 0.01 in construction A AND in construction B.
- **(c) Side constraints:** groups, CFG543 P2 |Z| < 2; MW, |ΔV_c| ≤ 5.4 km/s at r = 8.2, 16, 20, 30 kpc and |ΔΣ_dark(R0, |z| ≤ 1.1 kpc)| ≤ 5.8 M_⊙/pc² relative to the law profile (CFG553 band half-widths, as CFG559 used them).

## 4. Overlap verdict per footing

- **OVERLAP** iff at least one grid point is allowed by (a) and (b). Also reported: the overlap with (c) added (O_abc), and the allowed regions of (a) and (b) separately (projected on (x_e, f) for each y).
- **NO OVERLAP** otherwise.
- **CONVENTION-SENSITIVE** (flag): the OVERLAP / NO OVERLAP answer changes under the halo-model baryon variant, the KiDS lane convention, or the full feedback band.

## 5. Reading the result (fixed in advance)

- **If OVERLAP:** describe the overlap profile in words using its (x_e, f, y) and the derived q (e.g. "only a fraction f of the law's phantom is settled beyond r_in", "the law holds only inside y r_M"); report M(<r)/M_L(<r) at r/r_ta = 0.05, 0.1, 0.2, 0.3, 0.5 for log M_ta 12–15.
- **If NO OVERLAP:** say plainly that the framework's settled-halo concept, within this family, conflicts with the combination of cosmic shear and KiDS galaxy lensing, pending the real shear likelihood (CFG592); name which data assumption (KiDS environment model, recalled A_mod, z = 0 R, KiDS profile convention) would have to fail to rescue it, and by how much the closest point misses each constraint.
- Either way, the closest-to-both point is reported (minimum over the grid of max(Zmax_shear(best T in band) / 2, χ²_KiDS-excess measure)), with its margins read from JSON.

## 6. Record rules (does the record predict the overlap?)

Each record rule's own profile is judged by the same (a) and (b), per footing:
- CFG556 census edge (`census|cen`, f = 1, mass-dependent x_e) and emergent edge (`census|emg`): computed through this lane's family code (control K1 requires an exact match to CFG556's R).
- CFG557 finite-age supply (`TESTED`) and CFG559 kinetic (`PRIMARY_kin`, `VARIANT_full_kin`): shear from their stored R through CFG590's code; KiDS from their stored χ² (CFG557 / CFG559 results JSON).
- CFG541 edge = the census edge's analytic form (same profile as `census|cen`); CFG542 leaves the switch an INPUT (no profile; it is reported as making no profile prediction).
- A record rule **predicts the overlap** iff its own profile is allowed by both (a) and (b) on that footing. Also reported: whether the overlap contains any f = 1 point (a framework-type fully settled law profile at some constant x_e).

## 7. Controls (load-bearing)

- **K1:** the family code with f = 1, y = 0, the census edge (mass-dependent, no supply cap) reproduces CFG556's `census|cen` R(k) (both footings) to max |ΔR| ≤ 1e-10; with baryons to r_ta and the emergent edge, CFG556's `census|emg` to ≤ 1e-10.
- **K2:** CFG590's code, exec'd here, reproduces CFG590's stored A_M1 for ΛCDM and for CFG559 PRIMARY (T 7.8, both surveys, both footings) to ≤ 1e-9.
- **K3:** KiDS linear-response path: (i) for 5 random groups the operator applied to a test profile equals CFG504's `kids_fin` / `truncate` / `window` on the same grid to ≤ 1e-8 relative; (ii) the lane-convention census edge (f = 1, census edge, unsettled excluded) reproduces CFG529's stored census χ² (A and B, both footings) to |Δχ²| ≤ 0.5 (grid-resolution tolerance; the actual difference is reported); (iii) CFG529's native ΛCDM f30 χ² (A 22.47, B 22.51) reproduced to ≤ 0.01.
- **K4:** the group code in lane convention with the supply-reached edge and f = 1 reproduces CFG543's stored P2 mean (both footings) to ≤ 1e-4.
- **K5:** mass conservation M(<r_ta) = M_ta to ≤ 1e-6 for every family point and halo in the halo model.

## 8. MUTATE (`CFG593_MUTATE=1`, separate `_MUTATE` outputs; exit 1 = all teeth bite)

- **MU1:** the framework's current profile (CFG559 PRIMARY stored R, and CFG556 `census|cen` through the family code) must land OUTSIDE the shear-allowed region on both footings, reproducing CFG590's EXCLUDED class.
- **MU2:** ΛCDM (R ≡ 1 for shear; CFG529's native ΛCDM rows for KiDS) must land INSIDE both (a) and (b). The family's NFW member (x_e = 1, f = 0) is also evaluated; if it fails either constraint, that is reported as a limitation of the family construction, not hidden.

## 9. Outputs and rules

- Scripts in this folder; `.out` and `_MUTATE.out`; results JSON (`cfg593_*_results.json`, `_MUTATE`); README. All numbers in the README come from the JSON. Large intermediate tables go to `_external_data/cfg593_work/` (not committed).
- Compute: `nice -n 10`, ≤ 4 processes / threads.
- Disclosures dated 2026-10-10. Frozen text is never edited; any departure is disclosed in the README.
- Results commit message starts "CFG593 results:". Not pushed.
