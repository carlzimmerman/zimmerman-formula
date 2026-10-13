# CFG725 FROZEN CRITERIA: the condensate carrier's self-interaction window against the record's merger and core data

Committed alone, before any CFG725 script or number. Frozen text is never edited; later changes are dated disclosures in the
README.

## Question
CFG723 left one viable carrier: a cold collisionless medium of quanta (mass m) whose displacement is P (∇·P = ρ_c − ρ̄_c), with
a condensate branch that needs σ/m ≥ 0.146–0.82 cm²/g (thermalisation at r_M within 13.8 Gyr for M_b = 1e9–1e12 M☉;
`cfg723_results.json` → B.rows, per footing) and m ≤ 16–143 eV. What does σ/m do in this theory, and is that window allowed by
the self-interaction data already on disk?

## Settings
- κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) / 1.1312e-10 (alt) m s⁻², never pooled. Capacity Σ_cap = a₀/(πG) =
  213.8 / 258.3 M☉ pc⁻² (CFG722 B8).
- "Cold energy". Its mass is required. Not "theory closed". No ΛCDM or standard-MOND yardstick in any verdict. 1 cm²/g =
  0.1 m²/kg (CFG428 correction), asserted in the script.
- Light compute: one process, ≤ 1 GB, nice -n 10. No downloads. Literature numbers PROVISIONAL.

## Inputs (declared)
- I1 Bullet lensing M_proj(<250 kpc): main 2.5e14, sub 2.0e14 M☉ (Paraficz+16, recalled, PROVISIONAL; as CFG724). Baryons inside
  250 kpc (CFG625 static, projected): main 4.85e13, sub 1.50e13. Dark Σ̄ = (M_lens − M_b)/(π R²). Declared error on the dark Σ̄:
  ±15% (PROVISIONAL).
- I2 Merger history: CFG623's VALID α = 0 (collisionless) runs, `runs/a0_{can,alt}_v2666.7_eta1.132.json` (primary); seeds
  603–605 reported as scatter. CFG623's own estimator code (`cfg623_main.py`: beta_of, window, stable, S.epoch) imported read-only.
- I3 Data: D1 Bullet f_obs = 0.045 ± 0.125; D2 Harvey+15 β = −0.04 ± 0.07 (PROVISIONAL, as CFG623). Wittman+18 contest D2 (the
  record's A09d row: offsets consistent with zero, weaker bound ~2 cm²/g); no table on disk → context only.
- I4 LITTLE THINGS (Oh+15) `rotdm.dat` (DM-only rotation curves after their baryon model; near-raw, M/L-dependent), read from the
  external data folder, checksum per its SHA256SUMS.
- I5 Context only (never a verdict input): Sagunski+21 cluster limit 0.35 cm²/g (ΛCDM-halo Jeans modelling; astra EVIDENCE.md).

## (a) Merger offset vs σ/m
- **Populations.** Branch ALL (primary): every quantum scatters, tethered and free alike, because superfluidity breaks at merger
  speed (CFG723 B5, Landau ratio ~1e6) and the tether is a velocity-independent mean-field force. Branch FREE (alternative, the
  brief's framing): only the free fractions scatter, f_free = 1 − Σ_cap/Σ̄_dark (main and sub, per footing).
- **Kinematics (derived in the script).** Equal-mass, isotropic (contact, s-wave, velocity-independent) scattering at relative
  speed V: a scattered quantum of the sub gets Δv = (V/2)(n̂ − ẑ) relative to the sub; it stays bound iff |Δv| < v_esc. With
  x = min(v_esc/V, 1), the mean momentum per scattering retained by the bound remnant is (V/2)x⁴, so the drag on the bound carrier
  is a_d = η (σ/m) ρ_tgt V², η = x⁴/2. Escaping quanta leave without shifting the remnant's centroid (mass loss only).
  Drag-limit variant η_D = 1/2 (all momentum retained) is reported as the tight-side bound, not used in the verdict.
- **Offset.** Galaxy–carrier relative coordinate: δ̈ = a_d(t) − ω²δ, δ(0) = δ̇(0) = 0, ω² = (4π/3)Gρ₀,sub (sub total profile).
  The sub's lensing peak moves by w·δ along −v̂_rel (trailing, toward the gas), w = dark/total of the sub inside 250 kpc (ALL) or
  w·f_free,sub (FREE). ρ_tgt = main dark profile at the sub's position (ALL) or × f_free,main (FREE).
- **Profiles.** Pseudo-isothermal ρ₀/(1 + r²/r_c²) truncated at r_t (main 1200, sub 990.9 kpc: CFG623 run values), normalised
  to I1's projected masses inside 250 kpc (main dark; sub total for ω and v_esc). r_c ∈ {50, 100, 150} kpc, primary 100.
  v_esc = √(2|Φ(0)|). Separation and V(t) from the CFG623 run (sub galaxies vs main cold peak; |v_gal,sub − v_gal,main|).
- **Scores.** f and β̄ recomputed with CFG623's estimator on lens positions shifted by the SI displacement: same 720-kpc epoch
  interpolation, same Harvey window (t − t_peri ∈ [0.1, 0.6] Gyr, d_SG ≥ 200 kpc), same as-run stability flags (not
  re-evaluated). Z_B = (f − 0.045)/0.125, Z_H = (β̄ + 0.04)/0.07; allowed iff |Z_B| < 2 and |Z_H| < 2.
- **Grid.** σ/m = 0 plus 81 log-spaced values 0.01–100 cm²/g. σ/m_max,merger = the largest grid value below the first excluded
  one (any re-entry reported).

## (b) Cores vs σ/m
- **Tethered population (derived from CFG722 B4/B5):** its static minimum is the law's profile for a cold carrier; a quiescent
  condensate has no relative motion to scatter. Its core is σ/m-independent. Dwarf cores therefore carry σ/m information only
  if dwarfs hold a free population, i.e. dark Σ above capacity.
- **DW1 (LITTLE THINGS):** Σ_dark(<R) = V_DM²/(πGR) on the "Data" rows vs Σ_cap. "Dwarfs below capacity → dwarf cores
  σ/m-blind (NOT DIAGNOSTIC)" iff ≤ 5% of points exceed Σ_cap AND ≤ 3 galaxies have a point > 2σ above it (σ from e_V); else
  "a free population in dwarfs is possible; dwarf cores σ/m-diagnostic (not evaluated here)".
- **Free population (cluster cores):** isothermal sphere of dispersion σ_v in the potential of itself plus an external component
  (baryons + tethered at capacity: pseudo-isothermal, r_e, truncated at r_t, projected mass inside 250 kpc = M_b + Σ_cap π R²).
  Central density ρ₀ = A/((σ/m)⟨v_rel⟩t_age), ⟨v_rel⟩ = (4/√π)σ_v. Derived relations reported: r_c,free(σ/m), Σ₀,free(σ/m),
  Σ̄_free(<250 kpc; σ/m). Brackets A ∈ {1, 4}, t_age ∈ {5, 10} Gyr, σ_v ∈ {1000, 1300} km/s, r_e ∈ {50, 100, 200} kpc.
  Allowed iff Σ̄_pred ≥ (1 − 2 × 0.15) Σ̄_obs,free for both main and sub (Σ̄_obs,free = Σ̄_dark − Σ_cap). σ/m_max,core per
  bracket corner on the same grid. The thermalisation threshold σ_th = 1/(ρ̄⟨v_rel⟩t_age), ρ̄ = M_proj,free/((4/3)πR³) and
  0.5× that, is reported.

## (c) Combined window and (d) verdict, per footing
- s_lo,min / s_lo,max = min / max of CFG723's σ/m_min over M_b = 1e9–1e12 for that footing.
- The merger bound is DIAGNOSTIC as computed in the primary configuration (ALL, η = x⁴/2, r_c = 100, seed 599). The core bound is
  DIAGNOSTIC only if its minimum and maximum over the bracket corners fall on the same side of s_lo,min and on the same side of
  s_lo,max; otherwise it is NOT DIAGNOSTIC, excluded from the combination, and its range is reported.
- S_max = minimum over DIAGNOSTIC upper bounds (∞ if none bounds σ/m inside the grid).
- **CLOSED** iff S_max < s_lo,min. **OPEN** iff S_max ≥ s_lo,max. **OPEN-PARTIAL** iff s_lo,min ≤ S_max < s_lo,max (state
  which halo masses can still condense). **NOT DIAGNOSTIC** iff S_max = ∞.
- The single cleanest deciding measurement is named from whichever test's bracket straddles the window.

## Controls (script exit 0 iff all pass)
- K1: oscillator integrator vs the analytic constant-drag solution (a/ω²)(1 − cos ωt): max relative error ≤ 1e-6.
- K2: isothermal solver: projected mass to r_t equals the 3D mass within 1e-3; pure self-gravitating solution within 10% of the
  singular asymptote σ²/(2πGr²) at r = 300 r₀ (r₀ = 3σ/√(4πGρ₀)).
- K3: Monte Carlo isotropic scattering (1e6 samples) reproduces the retained mean Δv_z/V = −x⁴/2 within 1% at x = 0.3, 0.6, 0.9.
- K4: unit check 1 cm²/g = 0.1 m²/kg.

## MUTATE (`CFG725_MUTATE=1`, separate `_MUTATE` outputs; exit 0 iff every tooth bites)
- M1: σ/m = 0 reproduces CFG623's α = 0 scored f and β̄ to ≤ 1e-9 (both footings), and the core model gives no bound at
  σ/m = 1e-6.
- M2: σ/m × 10 (0.3 → 3, primary configuration): f and β̄ both increase (toward the gas), and Σ̄_free,pred decreases.
- M3: drag sign flipped at σ/m = 3: β̄ falls below its σ/m = 0 value.

## Pre-freeze disclosures (orders of magnitude seen while planning; not verdict inputs)
- CFG623 α = 0 baseline known: f 0.181 / 0.178, β̄ 0.063 / 0.061 (can / alt).
- Back-of-envelope: Bullet-sub free core thermalises within 250 kpc in 10 Gyr for σ/m ≳ 0.16 cm²/g; isotropic η ~ 0.03 at
  x ~ 0.5; impulsive drag-limit offset ~30 kpc at σ/m = 1 cm²/g. These guided the bracket choices, which are declared above.
- The merger model's progenitors underweight the Bullet (CFG625 M-RAW not met); the SI layer is a post-processing of CFG623's
  collisionless run, not a self-consistent N-body run with scattering (galaxies' back-reaction enters only through ω).
