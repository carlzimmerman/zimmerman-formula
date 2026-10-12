# CFG643: Door 1, baryon -> cold-energy heat exchange Q_c = C a0 v rho_b. Verdict: CLOSED

Baryons cannot supply the energy. Even the record's IC-C benchmark import needs 8 to 56 times the baryons' whole kinetic
energy. If every catchment baryon donated a full V_f^2, the import would still be 1.5 to 3.5 times larger. The framework's own
formation path (infall from turnaround, CFG541) needs energy taken OUT of the cold energy, so heating it has the wrong sign. No
fixed coupling gives the needed sigma proportional to 1/(n_c v^2). Getting it requires a new baryon vertex, which means a
particle with a free cross-section. This holds on both footings.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first in c7dad5f10. It discloses a mental order-of-magnitude estimate
  made before the freeze; the thresholds come from the task specification.
- **Script:** `cfg643.py`. It imports CFG541's `Model` read-only and reruns CFG541's alpha = 1 settling flow to get the target
  state.
  - Run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg643.py`. It takes about 3 s, uses one process and well under 300 MB, and
    exits 0.
  - `CFG643_MUTATE=1` writes the `_MUTATE` outputs.
  - No PM. Nothing was downloaded.
- **Settings:**
  - kappa = 1/2 is FITTED.
  - The footings, canonical 9.3603e-11 and alt 1.1312e-10, are never pooled.
  - "Cold energy" throughout; its mass is required. No particle species is added.
  - No LCDM or standard-MOND yardstick is used. Not "theory closed".
- **Numbers:** every number below comes from `cfg643_results.json`.
- **Heating law:** the law is posited. It is taken from astra's MECHANISM.md checkpoint, which quotes FKPS arXiv:1912.07626
  eqs 26-28. The paper itself was not re-read (no downloads).
- **Systems:** CFG541's MW-like disc and group-like system (CFG540 median), plus the 1.5e14 point-mass cluster, labelled as
  the X-COP-scale proxy.
- **Control V0:** the recomputed K_f and dW match `cfg541_results.json` exactly (relative difference 0) in all 6 cells: PASS.
- **Cross-check:** the C_min from collective_energy_lower's import fractions agrees with the CFG541-based value to 0.95-0.97.

## Statement used

- Heat flow: the cold energy gains Q_c = C a0 v rho_b and the baryons lose the same amount.
  - v = V_f/sqrt(2) is the primary choice (astra's); v = V_f is the variant.
  - System age: 10 Gyr for all three is primary; 12 / 8 / 5 Gyr is the variant.
- Transport, three versions:
  - **T0 (framework-native).** The cold energy is collisionless, so there is no irreversible heat flux and A = 0.
  - **T1 (FKPS closure, ASSUMED, not framework).** Ideal gas relaxing on a dynamical time:
    L = ∫ (3/2) rho_c sigma^2 (sigma/r) dV over the derived target.
  - **T2 (collisional, context).** Relaxation at astra's benchmark self-collision rate, S = 0.3 cm^2/g.
- Balance: L_heat = B C a0 M_b V_f and L_transport = A V_f^5/G give V^4 = (BC/A) G M_b a0. The law's normalisation therefore
  needs C_BTFR = A/B.

## C each system needs (G1a: IC-C import over the age, primary v and age)

| | MW-like | group | X-COP-scale cluster | spread |
|---|---|---|---|---|
| E_imp / (M_cat V_f^2) (can) | 0.526 | 0.294 | 0.660 | |
| C_min canonical | **0.223** | **0.075** | **0.220** | 2.96 |
| C_min alt | **0.193** | **0.064** | **0.191** | 3.04 |
| spread with the age variant | | | | 4.67 / 4.81 |

The MW and cluster values agree closely (0.22 vs 0.22). The group is the outlier: its K_f/M is low (0.30) and its M_cat/M_b is
18 instead of 54. Under the frozen factor-2 rule, one universal C fails. This is a mild failure on its own (spread about 3),
not a clean closure.

## Gate table (canonical / alt)

| gate | result | label |
|---|---|---|
| G1a one C supplies the IC-C import | C_min 0.22 / 0.075 / 0.22 (can), 0.19 / 0.064 / 0.19 (alt); spread 2.96 / 3.04 (variants 4.7-4.8) | **FAIL** (not universal; mild) |
| G1b native formation path | E_sink = +0.24 / +0.11 / +0.32 (can), +0.26 / +0.12 / +0.35 (alt) M_cat V_f^2. Infall from turnaround must LOSE energy | **FAIL BY SIGN**: heating imports energy where export is needed |
| G2 BTFR, T0 native | A = 0: no balance; the heat accumulates linearly | **FAIL** |
| G2 BTFR, T1 assumed | C_BTFR = 4.36 / 0.44 / 20.1 (can), 4.20 / 0.41 / 21.5 (alt); spread 45 / 52; 6-110x C_min | **FAIL** |
| G2 BTFR, T2 collisional | C_BTFR 2.0e-2 / 3.2e-4 / 4.1e-2; spread 130-150; A depends on S and r, so V^4 ∝ M_b is lost | **FAIL** |
| G3 baryon reservoir | E_imp/K_b = 57 / 11 / 7.9 (C-independent). t_b at C_min 0.18 / 0.92 / 1.27 Gyr; at C_BTFR(T1) 8-160 Myr; all against a 10 Gyr age | **FAIL** |
| G3 replenishment ceiling | every catchment baryon donates V_f^2: the import is still 2.8 / 1.6 / 3.5x larger | **FAIL** |
| G4(i) is there an interaction with sigma ∝ 1/(n_c v^2) | v^-2 is possible (s-wave unitarity saturation); 1/n_c needs a density-screened mediator, and astra's trial version has negative compressibility; both need a non-gravitational baryon vertex the action lacks | **FAIL**: needs a particle with a free cross-section |
| G4(ii) context (different channel) | required sigma_cb/m_b at C_min: cluster 1.0-1.2 (100 kpc), 30-34 (500 kpc) cm^2/g; MW 26-29 (8 kpc), 340-390 (30 kpc); unitarity puts m_c at or below 3-23 GeV | above 0.35 cm^2/g (context: Sagunski+ limit is for SELF-interaction) |
| G5a CFG541 S(i) | heat retained on the native path: K = +0.37 to +0.40 dex above the target Jeans K (rule 0.1) | **FAIL** |
| G5b CFG623 Bullet drag | a_d = C a0 rho_b/rho_c. If sigma ∝ 1/w^2 at merger speed: offset 1.3-14 kpc over 0.2 Gyr. If sigma is fixed at thermal v: 38-394 kpc | **PASS** as frozen (primary); FAIL in the variant |
| G5c CFG596 clumping | candidate B places settled mass by the law's deficit; heating can de-concentrate it only by moving it off the law's profile | REDUCES CLUMPING ONLY BY BREAKING THE LAW |
| MUTATE | M1 C -> 0: delivered/required 0, so IC-C cannot reach the profile (astra's bound reproduced). M2 C x 2: supply ratio exactly 2. M3 export-signed Q passes the native sign test | all bite |

## Verdict: CLOSED (both footings)

Three gates fail cleanly. Two of them are independent of how C is chosen.

1. **G1b sign.** The record's own route to the profile (infall from rest at turnaround) arrives with too much energy. CFG541
   already showed this: E_sink > 0 everywhere. Q_c >= 0 makes it worse.
   - The IC-C state (target density, cold velocities) needs an import, but it is a benchmark, not the framework's formation
     state.
   - Reconciliation with CFG541: baryon heating is a different SOURCE from settling, but it feeds the same cold kinetic
     energy. CFG541 S(i) already excludes extra heat there (G5a +0.4 dex).
2. **G3 budget.** E_imp/K_b = 2 (K_f/M_cat V_f^2)(M_cat/M_b), which is 8-57.
   - With the declared generous replenishment, the ratio becomes 5.364 x (K_f/M_cat V_f^2) = 1.5-3.5, independent of the
     catchment. The cold energy outweighs the baryons 5.364 : 1, so the baryons cannot raise it to virial energy even if each
     gives up a full V_f^2.
   - The only escape is to have all catchment baryons sink deep into the core and give up potential energy. That contradicts
     census f_ret (0.10 for the MW) and is not framework-supplied.
3. **G4 existence.** A fixed coupling cannot track 1/n_c. Any working version is a new non-gravitational baryon vertex, i.e. a
   dark particle with a free cross-section. The framework's rules exclude that.

The BTFR normalisation (G2) is not rescued either:
- Under the assumed FKPS closure, the C that makes BC/A = 1 varies 45-52x across systems.
- That C would drain the baryons in 8-160 Myr.

As a door to energy supply, this is closed. It is not a KNOB, because no choice of C passes G1b, G3 or G4(i).

## Disclosures

- The cluster is CFG541's point mass. Its T1 transport A is dominated by the Newtonian zone near the point. Its "local-sigma B"
  variant (sigma at r_in) is meaningless and is not used. The G2 universality failure holds without it: MW vs group alone
  differ about 10x.
- G2's rule (ii), "within 2x of C_min", fails in the oversupply direction. Oversupply alone would not be fatal under T1. The
  G2 label rests on (i), universality, and the G3 drain.
- The heating law, the T1 closure, the closure for the energy transferred per collision (O(1)), and the Bullet bracket
  rho_b/rho_c in [0.1, 1] are inherited or declared assumptions. Literature values come from the checkpoint files and were not
  re-verified here.
- kappa is fitted; the cold energy mass is required; no particle species; not theory closed.
