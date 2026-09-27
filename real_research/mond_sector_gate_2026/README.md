# mond_sector_gate_2026: which quantity the MOND switch reads, and the one number cosmic shear sets

These lanes are a construction-level result, not closure. κ = ½ stays a declared input. The dark carrier is a state
of the framework's own field, not a new particle species, and its mass is still required. The trigger is still
posited.

## The direct path, in four steps

**1. The switch must read the baryons (with their phantom), never the carrier and never the metric curvature.**

Every switch on the record reads the carrier:
- the particle-mesh runs read matter (baryons + carrier);
- DE1/DE2 and V0's curvature variable read the total dynamical density.

The gate has always been a prescribed mask. Once it is varied as an action term, two independent calculations rule
out reading the carrier or the curvature:
- **MS1 (here, sympy on CV1's Lagrangian).** A switch that reads the carrier, directly or through the curvature it
  sources, gives the carrier an edge force. That force is 0.06–60× its own gravity around an L* lens, and up to
  150–2300× around a z = 2.5 flagship host.
- **DE7 (the dark-energy thread, committed 095ab610a).** A curvature-reading gate needs a repair term against a
  wrong-sign k⁴ term. It also makes lensing differ from dynamics in transition layers: ~6% at z = 0.25, ~100% at z = 4.

Two readings keep the carrier exactly Newtonian with the gate varied:
- ∇²(Φ − v): the baryons and their phantom (L353's pair field v removes the carrier's own potential);
- the baryon density alone.

**2. On that reading the flagship no longer needs circumgalactic gas.**
- The switch is carrier-blind, so there is no bistability and no self-limiting clearing.
- At the linear cell (p = 1, x_c0 = 2.5) the flat-a₀ flagship holds at z = 2.5 with no CGM at all. The matter-only
  reading needs ≥ 30% (MS2).
- The unbound web needs 1/f_b = 6.4× the overdensity to switch on.

**3. Cosmic shear, scored resolution-free, sets one number: MOND regions must stop growing near 1.75 Mpc (z = 0.5),
a velocity scale v_cap ≈ 325 km/s** (MS3).
- The record's mock-based "shear ok" (DE3/DE5 → L388, AT3) rests on a 100 Mpc mock with two defects:
  - it cannot grow a region from an isolated galaxy's seed cell;
  - it holds too few clusters.
- On L363's own resolution-free halo model, the region kernel's lensing power at k = 1 is ≥ 73% clusters. Uncapped,
  it fails for every carrier history: worst R 2.5–4.3 against 1.2.
- **With the cap and L388's density-trigger retention it passes: 1.05 / 1.12.** Every KiDS lens (v_f ≤ 250 km/s)
  keeps its full region.

**4. What is left.**
- A same-model particle-mesh run at this switch and cap.
- Mechanisms for the cap and the trigger. The cap can be written as an action term (MS5):
  U_cap = C·min(∇²Φ_X, v_cap²κ_X²), where κ_X = ½∇·(∇Φ_X/|∇Φ_X|) is the mean curvature of the MOND field's
  equipotentials. κ_X = 1/r for every spherical profile, so every region stops at ℓ_cap(z) = v_cap/(H√x_c): 1.75 Mpc at
  z = 0.5, 2.99 Mpc at z = 0.023. **An earlier version of this step proposed v_loc² = |∇Φ|²/∇²Φ, and L395 implements
  that form. It is withdrawn.** It equals (1 + β_b/2)/r, so cluster regions grow with their gas, and cosmic shear
  fails (MS5 S1).
- The dark state (L374).
- The Local Group and EFE liabilities. XR6 scored the converged model: none flips, and two get worse (see "Said plainly").

## Lanes

| Lane | Script | Checks | Result |
|---|---|---|---|
| MS1 | `MS1_gate_variation_reciprocity.py` | 5/5; MUTATE (the carrier added to the MOND-sector reading) fails A3, rc = 1 | **Reciprocity decides the doors.** CV1's Lagrangian is used term for term, with f = W(U) varied and M² = m²(1 − f); CV1's six field equations are reproduced (A1). sympy derives the varied Euler–Lagrange equations for four readings in closed form, zero residual (A2). The dark component's potential minus the Newtonian potential of all matter (A3) is:<br>• **0 identically** for U = C∇²(Φ − v) and for U = Cρ_b;<br>• −½CW′(U)B for U = C∇²Φ (curvature);<br>• −CW′(U)B/(8πG) for U = C(ρ_b + ρ_d) (matter).<br>Both carrier-blind readings have off-plateau homogeneous backgrounds (A4, CV1 A6's requirement). **N1, the leak's size** (kernel term of B, gate widths Δ = 0.1–1, curvature / matter door): 0.06–6× / 0.6–60× the carrier's gravity around an L* lens at z = 0.25, and 1.5–150× / 23–2300× around a z = 2.5 flagship host. |
| MS2 | `MS2_mond_sector_door_flagship_web.py` | 7/7; MUTATE (the door reads the carrier too) fails D1, 98 state changes, rc = 1 | **The MOND-sector door's own cell, on DE4's galaxy (loaded unedited).** DE4's F1 shifts, DE1's z_max and DE6's 264-entry table are all reproduced exactly (C1–C3).<br>**Carrier-blind:** 0 of 3696 switch states change with the retained carrier (D1).<br>**Flagship:** at the linear cell, z = 2.5, carrier cleared, the switch is on at r_F for M_b = 1e10–1e11 on both footings at every CGM share including 0. It then needs only S ≤ 0.059 retained at r_F. The matter door loses r_F at f_CGM = 0 and 0.1 (F1).<br>**z_max** at the linear cell: 4.26/4.52 with no CGM, against 1.95/2.15 on the matter door. Ten of DE6's eleven cells keep the flagship radius to z ≥ 2.5 with no CGM (Z1).<br>**The web:** the activation contrast is exactly f_b × the matter door's: δ ≥ 29–34 at z ≤ 0.5 and 105–228 at z = 2–3 at the linear cell. XR4's filament range (3.7–6.3) maps to 23–40 (W1). |
| MS3 | `MS3_cosmic_shear_bound_mond_sector.py` | 5/5; MUTATE (no cap) fails K1, rc = 1 | **Cosmic shear, resolution-free.** L363's committed halo-model R(k) is reproduced exactly (C1).<br>**U1, the mock can't score the door:** L363's region builder never grows from an isolated seed cell. Hosts of 1e12 / 1e13 / 1e14 M☉ stay at 1 cell (0.24 Mpc) against analytic phantom edges of 1.26 / 2.26 / 4.61 Mpc: the one-cell Dirichlet phantom vanishes.<br>**M1:** the 100 Mpc mock holds 4 systems at ≥ 1e14 M☉ (7.4 expected) and 0 at ≥ 1e14.5 (0.8 expected).<br>**D1:** the phantom's power at k = 1 is 0.80/1.07 of P_NL at the linear cell, ≥ 73% of it from ≥ 1e14 M☉ halos; halos below 1e13 give ≤ 0.004.<br>**X1:** uncapped, worst R is 2.47–4.32 against 1.2, for every carrier history (intact, cleared < 1e13, < 1e14, L388's retention), both edge conventions and both footings.<br>**K1:** capping every region at r_cap (z = 0.5) with L388's retention gives, canonical/alt: 1.24/1.36 at 2.0 Mpc, **1.05/1.12 at 1.75 Mpc**, 0.99/0.99 at 1.5 Mpc. With the carrier intact, only a 1.0 Mpc cap passes (1.16/1.18), so the density trigger's group/cluster clearing is needed too. The largest passing cap is 1.75 Mpc: **v_cap = 325 km/s, M_b,cap = 9e11 M☉**. At a fixed v_cap it caps regions at 2.35 Mpc at z = 0.25, above every KiDS lens's own edge (0.91–1.79 Mpc for M_b = 3e10–3e11). |
| MS4 | `MS4_smooth_gate_shear.py` | 4/4; MUTATE (no cap) fails S1, rc = 1 | **The smooth, action-ready gate keeps MS3's pass, at DE9's in-window cells.** DE7/DE9's C-infinity gate on the MOND-sector reading, p = 1, with L388's retention. DE9 (fix aa5705194) allows x_c0 in [2.0, 3.35] at w = 0.25 and [3.0, 3.09] at w = 0.5, so the scored cells are (w, x_c0) = (0.25, 2.5) and (0.5, 3.0). A near-sharp gate reproduces MS3 to 0.2% (C1). With the 1.75 Mpc cap, worst R is 1.049/1.124 at (0.25, 2.5) and 1.025/1.096 at (0.5, 3.0), against the sharp gate's 1.047/1.121 (S1). Uncapped it fails: 2.72/3.18 and 2.48/2.91 (S2). The 1.75 Mpc cap is the largest that passes in every cell (S3), including w = 0.5 at x_c0 = 2.5, outside the window, at 1.050/1.126. Quote it as: w ≤ 0.25 at x_c0 = 2.5, or x_c0 ≈ 3.0 at w = 0.5. The gate's width does not matter for cosmic shear; the cap does. |
| MS5 | `MS5_cap_as_action_term.py` | 5/5; MUTATE (the carrier added to the reading, and L395's form scored in place of κ) fails A1 and S1, rc = 1 | **The cap as an action term.**<br>**A1 (sympy, MS1's chassis):** the gate is varied on a generic reading U = C·F(Φ_X′, Φ_X″). Its term enters the Φ and v equations with opposite signs, and V_d = u_N exactly. So any cap built from Φ − v keeps the carrier Newtonian.<br>**A2 (sympy, 3-D):** κ_X = ½∇·(∇Φ_X/\|∇Φ_X\|) = 1/r for every spherical profile. L395's form ∇²Φ/\|∇Φ\| = (1 + β_b/2)/r in deep MOND.<br>**N1:** on MS3's point-mass baryons L395's form stays at ℓ_cap (0.86–0.99×). On baryons that keep tracing the host's NFW past r200 it sits 1.21–1.32× further out at z = 0.5. A Coma-like host at z = 0.023 has its edge at 3.77 Mpc, against XR6's 3.5–3.7 Mpc; the κ form's ℓ_cap is 2.99 Mpc.<br>**S1 (pre-declared, MS3's machinery):**<br>• the κ form reproduces MS3's K1 exactly and passes, 1.047/1.121;<br>• L395's form on extended baryons fails, 1.418/1.567 (point mass: 0.991/1.063).<br>**P1 (sympy):** the gate's fourth-order term:<br>• uncapped: C²W″Bk⁴;<br>• κ form: (Cv_cap²k_⊥⁴/\|g\|²)·B·[W″U + W′/2], transverse only;<br>• L395's form: 4Cv_cap²k⁴/\|g\|²·B·[W″U + W′/2].<br>The capped bracket still changes sign inside DE9's layer (t > 0.53/0.55 at w = 0.25/0.5, against 0.50 uncapped), so DE7's repair is still needed. |

Lean: `fable_independent_2026/lean_2026/MS1_MS2_mond_sector_door_certificates.lean`, 8 theorems, zero `sorry`,
standard axioms (propext, Classical.choice, Quot.sound). It certifies:
- the algebra that decides the doors;
- the "Newtonian iff the edge term vanishes" statements for the curvature and matter doors;
- the web's f_b scaling.

## Said plainly

- **The mock's cosmic-shear passes are not established, and not refuted either.** The halo model is the other
  extreme: it treats every halo as isolated and over-counts phantoms in crowded places. The truth lies between the two
  estimates. So the cap found on the halo model is a **sufficient** target, and a larger cap may pass. The decisive
  run is a cluster-bearing volume (≥ 500 Mpc) with regions grown from the phantom itself.
- **A first mock-based version of MS3 returned T_max(k = 1) ≈ 1.06 on this door.** U1 shows why that number is not
  physics. It is withdrawn and superseded by the halo-model lane above.
- **The MOND-sector reading ∇²(Φ − v) reads the lapse's Laplacian** in the covariant action. Its constraint structure,
  and whether DE7's k⁴ issue carries over, are CV3's to compute. The baryon-density reading avoids both, because it has
  no metric derivatives. But its regions follow the gas profile, so its KiDS fit is open.
- **The cap is a design target, not a mechanism.** MS5's action term is a construction with one new constant,
  (v_cap/c)² = 1.18e-6, separate from the kick (XR7). Its lower limit is the KiDS lenses (v_f ≤ 247 km/s); the grid's
  largest pass is 325 km/s.
- **What fails in the converged model (XR6, cross_thread_review_2026_09_26). ⚠️ These numbers use the withdrawn
  cap form (edges at 3.5–3.7 Mpc).** They stand until XR9 re-scores EFE with the κ form (2.9–3.0 Mpc).
  - Cluster-infall BTFR: worse. The cap screens members beyond its edge, so the EFE becomes a step: 3.00–3.07σ
    (scalar) and 4.87–5.52σ (subtract), against XR4's 2.66/3.83. Both EFE samples in quadrature give 4.4–8.0σ.
  - Local Volume dwarfs: unchanged at 3.87–4.48σ.
  - Local Group R₀: worse, 1.413/1.480 Mpc (+0.168/+0.188 dex).
  - Coma UDGs: 4.35/4.20σ.
  - The κ form moves the cap in from 3.5–3.7 to 2.9–3.0 Mpc at z = 0.02–0.06, so more infall members are screened and
    the cluster-infall EFE is expected to get worse again. It needs a re-score; nothing here has scored it.
- **Not touched here:**
  - the Local Group zero-velocity radius (+0.13–0.23 dex, XR4);
  - the 09-03 EFE liabilities;
  - the baryons' own edge layer (on every door; CV1's σ);
  - the trigger's action and the dark state.

## Hand-offs (the owners' calls; nothing outside this folder was edited)

1. **CV3 (`real_research/chk_v0_2026/`).** Take ∇²(Φ − v) or ρ_b as the gate functional. Then CV1's "the dark
   component feels Newtonian only" survives the variation exactly (MS1 A3). On the curvature reading it does not.
2. **The dark-energy thread (DE5–DE7).** For DE7's slip and k⁴ analysis, the baryon-density door is the one reading
   with no metric derivatives. DE5's mock bounds should carry MS3's U1/M1 caveat.
3. **The particle-mesh track (L388+).** Re-run with:
   - the switch and trigger both on the baryon (or baryon + phantom) density;
   - regions capped at v_cap ≈ 300–325 km/s;
   - the cosmic-shear score taken resolution-free, or in a box that holds clusters.
   The flagship then no longer depends on the CGM convention.
4. **AT3.** Its trigger clears galaxies' inner regions only (close to "cleared < 1e13"). On the halo model that fails
   even with the cap (1.64/1.74 at 1.75 Mpc). The density trigger's group/cluster clearing is what the cap needs
   alongside it.
5. **L395 and XR6.** Read the cap through κ_X, not ∇²Φ/|∇Φ| (MS5). In a box whose gas keeps tracing clusters past
   r200, the ∇²Φ/|∇Φ| form's edge runs 1.2–1.3× beyond the cap that the halo-model shear score assumes, so the PM
   dynamics and the shear score are not the same model.
6. **XR1's registry.** Add two labels, the switch reading (matter / curvature / MOND sector / baryons) and the cap,
   so that pooling across them is flagged.

## Files and reproduction

Each lane runs from the repository root; `MUTATE=1` runs its control:
- `python3 real_research/mond_sector_gate_2026/MS1_gate_variation_reciprocity.py` (~3 s)
- `python3 real_research/mond_sector_gate_2026/MS2_mond_sector_door_flagship_web.py` (~30 s)
- `python3 real_research/mond_sector_gate_2026/MS3_cosmic_shear_bound_mond_sector.py` (~2 min)
- `python3 real_research/mond_sector_gate_2026/MS4_smooth_gate_shear.py` (~1 min)
- `python3 real_research/mond_sector_gate_2026/MS5_cap_as_action_term.py` (~30 s)

Each lane writes a `.out` log, a `_MUTATE.out` log and a `_results.json` file. The Lean file compiles with
`lake env lean MS1_MS2_mond_sector_door_certificates.lean` in `fable_independent_2026/lean_2026/`.
