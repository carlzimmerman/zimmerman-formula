# CFG648 native PM specification: phase-mixed settling (H-SP). Written, NOT run

Scope: how a particle-mesh run of the CFG596 lineage (candidate B with R2 supply edge, R3 per-catchment conservation, R5 outer draw,
R6 round settled profile, G9) would apply H-SP natively, with no new constant. Nothing here has been executed. κ = ½ fitted; footings
never pooled; cold energy's mass required; not theory closed.

## 1. Tagging phase-mixed vs first-infall material (per catchment, per step)

Per catchment (the host's turnaround ball, as the engine already defines it), with host centre x_h(t) and bulk velocity v_h(t):
- For each cold-energy and baryon particle inside the catchment keep two bits and two scalars:
  `turned` (radial velocity about the host v_r = (v − v_h)·r̂ has been ≤ 0 once since the particle entered the catchment),
  `peri` (after `turned`, v_r has changed sign from < 0 to ≥ 0 at least once), r_ta,i (its radius at the `turned` step), and
  r_apo1,i, a_apo1,i (radius and scale factor at the first v_r sign change > 0 → ≤ 0 after `peri`).
- Sign changes are detected between consecutive kicks (the same KDK step the engine uses). Particles that change host (catchment
  re-assignment) reset all four entries; this is the PM analogue of the merger statement (a merging region is not phase-mixed).
- Scattering guard (as in the 1-D solver, disclosed there): a `peri` particle with r > r_ta,i is excluded from the caustic statistic.

## 2. The splashback radius per host

- PRIMARY: r_sp(t) = the radius enclosing all but the outermost 1% (by mass) of `peri` particles of that host (the 1-D solver uses
  the maximum; in 3-D the maximum is dominated by single particles, so the 99th mass percentile is the declared PM analogue;
  report the 95th and 100th as brackets). Running maximum r_sp,eff(t) = max over t' ≤ t (settled cold energy is never taken back).
- Bracket "apo": the median r_apo1 of particles whose first apocentre fell within the last Δln a = 0.1.
- r_sp is measured per host on the particle field, before the settling step, every step (or every N_sp steps with N_sp ≤ the
  engine's catchment-refresh cadence).

## 3. Settling step under H-SP

- The settled target is unchanged in form: the law's round phantom of the host's source baryons (all baryons for B, condensed
  baryons for H-CB), but truncated at r_set = min(r_edge,SP, r_sp,eff), where r_edge,SP is R2's supply edge computed with the
  supply AVAILABLE FOR SETTLING: the cold energy carried by `peri` particles of that catchment (already settled + still orbiting).
- The settled increment is drawn outer-first (by current radius) from `peri` cold-energy particles of the catchment (R5's continuous
  limit with the edge at r_sp). First-infall (`turned` but not `peri`) and not-yet-turned particles are never drawn.
- Everything not drawn stays as ordinary collisionless cold-energy particles; R3 conservation per catchment is unchanged
  (supply = drawn + remaining, checked to 1e-9 as in CFG647's audit).

## 4. Required diagnostics (to compare with the 1-D derivation in cfg648_derive)

- Per host at z = 0, 0.5, 1: r_sp/r_ta, r_set/r_ta, Γ (turnaround-mass growth over Δln a = 0.4), fraction of catchment cold energy
  that is `peri`, settled mass / candidate-B settled mass, and the settled and unsettled mass inside 0.2–0.5 r_ta.
- The 1-D solver predicts (eps = 1, cfg648_derive_results.json): the binding limit is the phase-mixed supply, not r_sp itself. A PM
  run must reproduce that ordering (r_edge,SP < r_sp) in isolated hosts, or the 1-D reading is wrong.
- Raw-data scoring exactly as CFG596 (KiDS-1000 raw ESD/shear, framework-native projection); no ΛCDM template enters a verdict.

## 5. Cost and controls

- Memory: two bits plus three float32 per particle (≈ 13 bytes/particle; 1024³ ≈ 14 GB extra), so the native test needs a 512³ pilot
  (≈ 1.7 GB extra) before any 1024³ attempt.
- MUTATE: r_sp → r_ta (H-SP off) must reproduce the CFG596 engine bit-for-bit; host relabelling (shuffled host IDs for the r_sp
  lookup) must remove any correlation of r_set/r_ta with the host's own Γ.
