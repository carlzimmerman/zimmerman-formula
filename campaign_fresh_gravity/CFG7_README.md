# CFG7 — swinging the top five of IDEAS_100 (FG001, FG016, FG097, FG004, FG041)

Campaign fresh gravity, 2026-09-27.
- Five ideas from `IDEAS_100.md`, each turned into a committed, runnable lane.
- Every lane has controls that reproduce committed numbers, and a MUTATE run that fails (rc = 1).
- Hypotheses were declared before each first run. Failed checks are kept as they fell. Exploratory runs are disclosed.
- Both a₀ footings throughout (9.3603e-11 / 1.1312e-10 m s⁻²). κ = ½ stays fitted.
- The dark component is the framework's own cold field (CFG4's T5), not a particle species.

The shared engine is `CFG7_common.py`:
- **Background:** flat ΛCDM with Ω_m = 0.3153, plus the GR top-hat turnaround table, checked against CFG4's committed table.
- **Linear power:** CLASS. The record's T_EH98 is not used, because it carries a units error (CFG1 B03).
- **Shell code:** a spherical collisionless shell code with angular momentum at turnaround, as in XR28. Its splashback measure is the first-apocentre percentile.
- **The law's helpers.**

## Results

### FG041: tidal dwarf galaxies, the kill test FG001 wrote for itself

`CFG7_tdg_fg041.py`; data in `real_research/data/tidal_dwarfs/` (Lelli et al. 2015, Tables 1, 7, 8 and 9, transcribed with provenance).

**FG001 survives its own kill test.**

Under FG001 a tidal dwarf forms inside its host's bound region, from disc material with no cold component, so it must be
Newtonian.
- The six tidal dwarfs (around NGC 5291, NGC 7252 and NGC 4694) are Newtonian: χ² = 1.09 for 6 objects (p = 0.98). The
  inverse-variance mean of M_dyn/M_bar is 1.16 ± 0.26.
- The framework's own law applied to each tidal dwarf, with the host's external field, fits worse by Δχ² = +5.2 to +12.0.
  That holds on both footings and for both kernels, even at the most favourable host mass (2× the paper's). With a 10%
  equilibrium systematic the gap is +4.8 to +10.8.
- The isolated law is excluded (χ² 118–152).
- Controls: the paper's Table 8 is reproduced from its Table 7, and its MOND velocities (Table 9) come back from its own
  eq. 4 at a₀ = 1.25e-10, within 1.0 / 1.4 km/s.
- Caveat (the authors'): the H I discs have turned less than one orbit.

### FG001: hierarchical ownership of the phantom

`CFG7_hierarchy_fg001.py`.

**The principle.** The law acts on a system's own baryons only if that system is top-level. This follows from FG001 plus
CFG4's T5, and adds no constant. It splits systems into three classes:
- **Top-level:** the law, with no external-field effect.
- **Accreted** (satellites, cluster members, UDGs): they keep the cold component they owned at infall. Their internal
  dynamics is therefore the *isolated* law of their infall baryons, with no external-field effect.
- **Formed embedded** (tidal dwarfs, globular clusters, collision debris such as DF2/DF4, wide binaries, the Solar System):
  Newtonian.

**The headline passed.** FG001 passes 9 of the record's 14 population gates, against 6/14 for the law with the host's
external field (the chain/M* reading), on both footings. On the 13 physical gates alone it is 8 against 6.

The controls all pass exactly:
- h43's Local Group dwarf medians (0.0000 dex);
- f13's globular-cluster medians;
- XR27's significances;
- FG041's result.

| Gate | FG001 | Law + external field |
|---|---|---|
| Cassini without a screening constant (ξ retired) | pass, margin 2–3e4 | needs ξ |
| MW classical dSphs | 1.1 / 0.7σ | 3.5 / 3.3σ |
| LV dwarfs' host statistic | 1.7σ | 3.9σ |
| Cluster-infall BTFR slope | 0.1σ | 2.4σ |
| Cluster-infall BTFR zero point | 1.3σ | 0.8σ |
| NGC 1052-DF2 | 0.0σ | 3.0σ |
| NGC 1052-DF4 | 0.8σ | 1.5σ |
| Tidal dwarfs | pass | pass on χ², worse by Δχ² ≥ 5 |
| Globular clusters | M/L_V 1.70 (Newton) | needs M/L_V 1.0 |
| M31 dwarfs, LVD | 2.6 / 2.2σ | 6.0 / 5.7σ |
| M31 dwarfs, Collins | 2.5 / 2.3σ | 5.8 / 5.6σ |
| MW ultra-faints | 8.0 / 7.5σ | 13.2 / 12.8σ |
| Chae D1 / D2 (the cost) | 4.1 / 4.3σ | 0.8 / 0.0σ |

**Two pre-declared sub-hypotheses failed, kept as they fell:**
- **H2, globular clusters:** the gate does not discriminate. The law's required M/L_V is about 1.0, the bottom edge of the
  stellar range rather than below it.
- **H4, the M31 LVD dwarfs:** they sit at 2.2–2.6σ, just past the bar.

**The cost:** Chae's external-field fits, at 4.1–4.3σ against zero (CFG1 rates them contested).

**Exploratory: the fossil-gas account.** This was declared after seeing h43's offsets, and adds no constant. Under the max
rule a satellite keeps the cold component set by its gas-rich infall baryons. Taking the gas fraction from the isolated
Local Group dwarfs' own H I moves every satellite sample toward zero:

| Sample | Offset before | Offset after |
|---|---|---|
| MW classical dSphs | +0.067 | −0.018 dex |
| M31 LVD | +0.116 | +0.036 dex |
| M31 Collins | +0.226 | +0.140 dex |
| MW ultra-faints | +0.355 | +0.209 dex |

### FG004: is the max rule a ground state?

`CFG7_groundstate_fg004.py`.

**D1, derived.** Around a point baryonic mass in the deep regime, the law's phantom is exactly an isotropic isothermal
sphere in Jeans equilibrium in the total field, with **σ² = V_f²/2 and P = a₀ g_N / (8πG)**. That is the relaxed
(maximum-entropy) state.
- The identity is exact for P2 (to 1e-5).
- For ν_mono it is asymptotic, with a √y correction: 1.05% at g_N/a₀ = 1e-3, 3.3e-4 at 1e-6. The pre-declared 1% control
  C2 therefore failed for ν_mono at 1e-3 (kept as run). The √y scaling is confirmed by a clearly labelled check added
  afterwards.

**D2, derived.** No local equation of state P = Π(g_N) can hold where baryons sit.
- On SPARC the cross-galaxy scatter of log P at fixed ρ is 0.51–0.55 dex.
- So the ground state is not a universal barotropic fluid.

**H1, passed: the outer phantom is relaxed.**
- At SPARC points with g_bar < 0.1 a₀, σ²_Jeans/(V_flat²/2) = 0.92–1.01 (median over 84–98 galaxies).
- In the outer parts the max rule *is* the relaxed state of a collisionless cold component.

**H2, failed (pre-declared uncertain): the inner phantom is not the relaxed state.**
- A relaxed (isothermal) cold component carrying T5's amount would over-concentrate where the baryons dominate.
- With the max rule it exceeds the law by **+0.13 to +0.15 dex at g_bar > a₀** (median per galaxy; 84th percentile
  +0.38–0.41).
- The overshoot shrinks toward the deep regime: +0.02–0.03 dex at 0.1 < g_bar/a₀ < 1, and +0.005 dex at g_bar/a₀ < 0.1.

**What this leaves (the next target):**
- T5 holds by relaxation outside the baryons.
- Inside them, something must keep the cold component out where g_N ≳ a₀. This is the framework's analogue of the
  cusp–core problem, now located and sized.

### FG016: the edge derived as the splashback caustic — killed by its own test, and by KiDS

`CFG7_edge_fg016.py`.

**The idea.** Replace CFG4's declared edge x_e with the splashback caustic: the edge of the region where the infalling
matter has turned back.

**How it was computed:**
- **Collapse:** spherical collisionless infall in ΛCDM, with 2000 shells × 3 seeds and six accretion rates.
- **Two readings of the interior:**
  - N: the cold matter gravitates normally;
  - G: the law's shape is imposed inside the caustic.
- **T5 closure:** gives x_e = r(Δ_sp)/r(Δ_ta) from the galaxy's own law.
- **The accretion rate is the law's own.** With T5, the mass inside the edge must grow as the law demands:
  s_law = 0.97 + 0.75 β_b at z = 0.25, where β_b is the galaxy's baryonic growth (bracketed 0–1).

**Results:**
- **H1, the kill test as written, FAILED.** The derived edge is x_e = 0.175–0.242 (reading G) or 0.187–0.271 (reading N) at
  z = 0.25, below CFG4's window [0.31, 0.48]. It is the same at every galaxy mass from 10⁹ to 10^11.5 M☉.
- **H2, KiDS with the derived profile, FAILED.** The profile is the law inside the edge and the collapse's own infall
  outside, with no free amplitude. It costs Δχ² +50 to +95; even with CFG4's 2-halo template on top it costs +14 to +54.
  Only accretion below the law's own demand (s ≲ 0.8) would pass with the template.
- **H3, the lenient budget, passed.** Ω_ph is 0.10–0.12 against 0.265.

**Controls:**
- **Passed:**
  - the top-hat table and the KiDS machinery (CFG4's committed x-scan) are reproduced exactly;
  - the guard is ≤ 0.18% in every production run.
- **C1 failed as declared.** Bertschinger's radial caustic 0.364 is smeared by angular momentum: the instantaneous
  99th-percentile caustic reads +7.6% and the apocentre median −5.9%.
- **C4 failed narrowly.** Δ_sp moved 5.5% against the 5% bar, and x_sp moved 2.6%. That moves x_e by about 3%, far less
  than the gap to the window.
- **The first production run failed its guard.** A core-exclusion shortcut ejected shells: 25% in C1 and 9.5% at
  s = 0.6. The shortcut was removed and the lane re-run. Its physics numbers agreed.

**What it means.**
- **The conflict, sharpened.** The splashback edge is excluded. Around an isolated lens with M_b ≈ 1e11 M☉ the
  phase-mixed cold halo ends near 0.45 Mpc, while KiDS follows the law's lensing to about 1 Mpc. The collapse's infall
  between those radii carries only about 55–65% of the law's mass. So CFG4's minimal conflict becomes **KiDS against the
  collapse's own cold supply at the law's accretion rate**, not just KiDS against the budget.
- **The hybrid fails CMB lensing.** Making the phantom a *field* beyond the splashback adds lensing mass of about
  1.5 Ω_m on large scales.
- **A compensated field is the next lane.** Its monopole would switch off, so it adds no net mass. But it needs a
  response edge beyond 1.7–3.4 Mpc (h72's bounds), i.e. past the lenses' turnaround radii of 1.2–1.95 Mpc. The decisive
  test is a halo-model CMB-lensing computation for that compensated field.
- **x_e stays a declared constant.**

### FG097: the one-command gate harness

`CFG7_harness_fg097.py`.

**What it does.** It scores candidate laws on every committed gate in one run:
- SPARC and KiDS are recomputed, reproducing CFG4 to 1e-6;
- the cold budget, CMB lensing, the forest, X-COP, the Bullet, Cassini, FG001's population gates and FG041 are read from
  committed results.

It prints each candidate's constant ledger and a SHA-256 registration hash.

| Candidate | Gates passed |
|---|---|
| A: CFG4 as committed | 32/48 |
| **B: A + FG001** | **38/48** (ξ retired) |
| C: B + FG016's derived edge | 34/48 (fails KiDS) |
| D: the external-field rival | 32/48 |
| F: hybrid, the law's field out to r_ta | 36/48 (fails CMB lensing) |

**Checks:**
- **K2 failed, as intended.** It flags FG004's and FG016's failed controls: the harness reports a gate that rests on a
  lane with failed controls.
- **MUTATE failed, as it must.** The no-switch candidate is caught on CMB lensing (rc = 1).

## Where this leaves the framework (2026-09-27)

**Best candidate: B** — CFG4's target law plus FG001's hierarchical ownership.
- One constant is gone (ξ).
- Tidal dwarfs, MW classical dSphs, the LV host statistic, the cluster-member BTFR and DF2 all come out right.
- Its known costs:
  - Chae's external-field fits (contested);
  - the M31 dwarfs and the ultra-faints (the fossil-gas account is exploratory);
  - a still-declared edge x_e.

**The open problems are now located and sized:**
- keep cold matter out where g_N ≳ a₀ (FG004: +0.13–0.15 dex);
- supply KiDS's lensing beyond the splashback without adding cosmic lensing (FG016).

**Registered prediction:** wide binaries must be exactly Newtonian (γ = 1) under FG001. A DR4 amendment needs the
author's go.

## Files

| Lane | Script | Outputs |
|---|---|---|
| engine | `CFG7_common.py` | — |
| FG041 | `CFG7_tdg_fg041.py` | `CFG7_tdg_fg041{,_MUTATE}.out`, `_results{,_MUTATE}.json` |
| FG001 | `CFG7_hierarchy_fg001.py` | `CFG7_hierarchy_fg001{,_MUTATE}.out`, `_results{,_MUTATE}.json` |
| FG004 | `CFG7_groundstate_fg004.py` | `CFG7_groundstate_fg004{,_MUTATE}.out`, `_results{,_MUTATE}.json` |
| FG016 | `CFG7_edge_fg016.py` | `CFG7_edge_fg016{,_MUTATE}.out`, `_results{,_MUTATE}.json` |
| FG097 | `CFG7_harness_fg097.py` | `CFG7_harness_fg097{,_MUTATE}.out`, `_results{,_MUTATE}.json` |
