# CFG657: a derived cold-energy capture rule for the NGC 1052 trail (DF2, DF4, DF9) and LEDA 4014647

Criteria: `FROZEN_CRITERIA.md` (commit 20d95b0d1, committed alone before the script). Script: `cfg657_capture.py`
(about 2 s, one process, no downloads). Outputs: `cfg657_capture.out`, `cfg657_capture_results.json`, and the `_MUTATE` pair.
Run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg657_capture.py`; `MUTATE=1` runs the two teeth only (exit 0 if both behave).

## Verdict: BRACKET-DEPENDENT; KNOB (alpha) (both footings). Not a pass.

At the primary inputs the derived rule does reproduce CFG655's four labels on both footings, without sigma and without
the vD+22 label. The outcome flips inside the frozen brackets, though, including inside the record's own O(1) bracket for
the drift coefficient alpha. By the frozen rule that is KNOB (alpha). CFG655's pass stays conditional on the external label.

| galaxy | f_cap primary (can / alt) | CFG655 bound or LEDA f_min (can / alt) | reproduces at primary? | f_cap range over bracket (can) |
|---|---|---|---|---|
| DF2 | 0.076 / 0.052 | <= 0.361 / 0.327 | yes | 0.013 - 1 |
| DF4 | 0.228 / 0.159 | <= 0.288 / 0.260 | yes (margin 0.03 on can vs the alt bound) | 0.067 - 1 |
| DF9 | 0.250 / 0.178 | <= 0.515 / 0.464 | yes | 0.052 - 1 |
| LEDA 4014647 | 0.335 / 0.242 | >= 0.226 / 0.202 | yes (just) | 0.092 - 1 |

- **Alpha window that reproduces all four** (other inputs primary): [0.67, 1.14] canonical and [0.84, 1.62] alt. The frozen
  alpha bracket is [0.5, 2]. At alpha = 0.5 LEDA drops below f_min; at alpha = 2 DF4 (both footings) and DF9 (canonical) exceed
  their bounds. The capture amplitude scales roughly as alpha^(4/3) times the ambient density, so one free amplitude decides it.
- **Other inputs that flip the outcome at a bracket end:** R (3-D distance to NGC 1052, R_proj/2), V_coll = 250, M_b,p = 1e10,
  the NGC 1035 mass, k = 3 (unsettled reservoir), and, on alt, t. Only X (local enhancement) and M_b,g leave it unchanged.
- **MUTATE:** M1 (V_coll -> 0) gives f_cap = 1 for all four on both footings (fallback: the gas stays with its own cold energy).
  M2 (cold energy -> 0) gives f_cap = 0 for all four. Both teeth behave.

## The derived rule (no new constant beyond the record's free alpha)

A dwarf that condensed from collision gas holds cold energy only through three channels, each an upper bound:

1. **S, separation.** The gas stalls and the collisionless cold energy moves on at V_coll/2. If V_coll/2 is below the
   progenitor's framework escape speed (settled isothermal halo out to the CFG541 exhaustion radius, then Kepler), the gas
   falls back and keeps full supply. Otherwise only cold-energy elements slower than the new dwarf's escape speed stay.
   At the primary inputs (V_coll = 358, M_b,p = 1e9) the gas escapes, and f_S ~ 3e-5 to 3e-4.
2. **F, sudden capture at formation.** Ambient cold energy (the settled halos of NGC 1052 and NGC 1035) inside the dwarf's
   Jacobi radius, slower than its escape speed: f_F ~ 1e-3.
3. **D, drift capture since formation.** This is Gould-type capture with the CFG541 settling drift as the only
   dissipation. Energy is removed at alpha tau_ff |grad psi| |g| per unit mass (CFG542 hand-off), with psi the full
   deficit field. D dominates everything: f_D ~ 0.05 to 0.33.

Under A6 strictly (no pooling: ambient cold energy belongs to the group's catchment) F = D = 0. Then f_cap ~ 3e-5 to 3e-4 for
all four. The E side is DERIVED at every bracket corner that keeps separation, but LEDA is NOT derived (needs >= 0.20).

## What separates LEDA 4014647 under the rule

Compactness. Its r_1/2 = 0.80 kpc against 1.5 to 2.7 kpc for the trail dwarfs, and its Sigma_e = 4.2e7 against 0.8 to
1.8e7 Msun/kpc^2. That gives:
- a deeper potential (v_esc,d(0) 36.6 against 28 to 33 km/s), so the drift does more work per crossing;
- a much smaller law target (nu(r_1/2) = 3.5 against 5 to 7.4), so the same captured mass is a larger fraction of it.

The ordering holds: f_cap(LEDA)/f_cap(DF4) = 1.47 / 1.52 at primary, and LEDA has the highest f_cap in every unsaturated one-at-a-time scan entry. The absolute level is not robust, because alpha times
the ambient density sets it. If LEDA is a pre-existing galaxy (vD+22 "interloper", or a progenitor remnant), it keeps its
own supply whatever the capture rate. The framework's own observables still cannot say which it is: CFG655 Rule A (age)
fails DF4/DF9, and Rule M (membership) fails LEDA.

## Read before citing (verified as hard as a pass)

1. **The LEDA side rests on favourable upper bounds.** Channel D uses the deepest (radial) chord, focusing with the central
   escape speed, the smaller host sigma, and an isothermal ambient continued past NGC 1052's exhaustion radius (72 / 65 kpc,
   while the dwarfs sit at 79 to 185 kpc projected). These are conservative for the E side and generous for LEDA. A
   realistic chord average lowers every f_D, and would take LEDA (only 1.5x / 1.2x above f_min) below its threshold first.
   "Reproduces at primary" is therefore not a derivation of LEDA's supply.
2. **Channel D runs the drift outside its validity.** CFG541 found the overdamped drift inconsistent in diffuse reservoirs
   (Pi = 10 to 1300; open item 3). Ambient cold energy streaming at 60 to 90 km/s through a dwarf is that regime.
3. **Separation itself is marginal in the framework.** Gas escapes its progenitor's cold energy only if M_b,p is below
   (1.7 to 3.0)e9 Msun at V_coll = 358 km/s, or V_coll exceeds 242 to 304 km/s at M_b,p = 1e9 (canonical; alt similar).
   The progenitor masses are not measured, so the framework does not establish separation; it is consistent with it only
   for progenitors at or below about 2e9 Msun of baryons.
4. **Correction 1 (sign, made before any verdict was read).** The frozen text wrote "Z >= -2" for LEDA's f_min and "Z = +2"
   for the E bounds. With Z = (obs - pred)/e the E upper bound is at Z = -2 and LEDA's lower bound at Z = +2. The script
   uses the corrected signs. It reproduces CFG655's R2 bounds (0.361/0.327, 0.288/0.260, 0.515/0.464), which confirms the
   intent. The frozen file is not edited.
5. **Implementation note.** The "all-upper corner" is taken as the maximum over all 512 bracket-endpoint combinations.
   That bound is at least as strict as the frozen one.

## Inputs (PROVISIONAL unless V)

Dwarf M_*, R_e, D and dispersions: CFG655 frozen table (V). Positions: vD+22 (2205.08552) Table 1 via ar5iv (V). V_coll:
"the relative radial velocity of the galaxies is high, 358 km s-1" and ">~300" (vD+22, V). Epoch: "around eight billion
years ago", minimum ~6 Gyr (vD+22, V). NGC 1052 / NGC 1035 positions, masses (1e11 / 5e9 Msun condensed), and progenitor
mass (1e9 each, bracket 3e8 to 1e10): PROVISIONAL, not measured in the cited abstracts.

## Prior record

CFG655 (label-conditional pass; R2 bounds), CFG541 (drift, exhaustion edge, alpha free O(1), diffuse-regime caveat), CFG542
(energy hand-off), CFG7 FG001 H6, CFG441, CFG392.

kappa = 1/2 fitted; cold energy mass required; no dark-matter particle; not theory closed.
