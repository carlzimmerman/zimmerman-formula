# CFG921: can one new posit select the law's excesses? Constraint intersection of five candidates

**Bottom line.** No candidate survives. All five posits FAIL on both footings. The failures are robust to the trials factor and
not fragile under the declared variants.

| posit (one constant, fixed on the 83 LVD dwarfs) | canonical | alt | decisive failures | if the cluster excess goes away (VC, pending CFG922) |
|---|---|---|---|---|
| P1 stress coupling (c_*) | FAILS | FAILS | calibration impossible: no c_* gives the dwarf mean with every dwarf in equilibrium | FAILS |
| P2 velocity-space capture (v_2) | FAILS | FAILS | clusters (z −7.3 / −6.2), cluster slope (−5.3 / −5.4), red lenses (−4.4 / −3.0) | FAILS (red lenses; alt knife-edge 3.03, local) |
| P3 late binding + escape (v_w) | FAILS | FAILS | clusters, cluster slope, red lenses (−4.2 canonical), dwarf size split (+3.9 / +3.9) | FAILS |
| P4 phase-space-density capture (Q_*) | FAILS | FAILS | clusters (−7.3 / −6.2), cluster slope; red lenses canonical (−3.8, local) | canonical FAILS, alt UNDERDETERMINED → split |
| P5 QUMOND geometry (no constant) | FAILS | FAILS | dwarfs (−8.2 / −7.3), dwarf shape χ² p ~ 1e-18 / 1e-15, size split (+7.6), red lenses | FAILS |

**What it costs.** Each of P1–P4 adds one new constant and new physics, and none of them pays for itself:
- P1 adds a stress coupling.
- P2 and P4 add a capture-and-retain mechanism. The record's drift erodes retained clumps (CFG889), so a latch is also needed.
- P3 adds a latch plus an escape law.

P5 adds nothing, and it misses the dwarfs by a factor of ~40.

**Why no single posit can work.** The facts pull in incompatible directions:
1. **Dwarfs vs red lenses.** At the same g_bar, dwarfs (σ ~ 10 km/s) carry the excess and red lenses (σ ~ 100 km/s) carry
   1/3 to 1/5 of it.
   - Every selector with a velocity scale (P2, P3, P4) suppresses the hotter system by ≳ 100×: s ∝ σ⁻³ or L − 1 ∝ v_c⁻².
   - Scale-free selectors (CFG919's F1) suppress it by only 1.25×.
   - Neither gives the observed 3–5×.
2. **Clusters.** The cluster excess (σ ~ 600 km/s, E rising with g_bar) is reproduced by none of P2–P5. P1 is the only posit
   that grows with σ, and it has no equilibrium at the dwarf amplitude.
3. **Dwarf shape.** Within the dwarfs, the excess falls with g_bar and with size at fixed g_bar: d = −1.36 ± 0.18 per dex of
   r12. P2 and P4 follow this shape: P2 is best on the g_bar slope and the cell χ²; P4 is best on size, with a slope of
   −0.30, z +2.2. P3 does not (d −0.66, z +3.9). P5 has no shape.

So even if CFG922 shows the cluster-core excess to be a baryon-accounting artefact, the dwarf/red-lens pair still excludes P2
and P3. P4 is then the only candidate not excluded on the alt footing, while the canonical footing still excludes it at 3.8σ
(local, below the trials-factor bar).

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. The
extra mass is cold energy, not a particle. No knob scans: one constant per posit, fixed once on the calibrator. Not "theory
closed". Nothing here says the data favour the framework.

- **Kind:** CONSTRAINT INTERSECTION (pre-registered). Block 920–929.
- **Criteria:** `FROZEN_CRITERIA.md`, 0abd82098, committed alone before any script or number.
- **Amendment:** `AMENDMENT_A1.md`, 9585600db, POST HOC. Written after the K-stage and a calibrator-only debug, before MUTATE,
  before the main run, before any class.
- **Not blind:** CFG919's cells and the other lanes' headline numbers were seen before freezing. The expectations formed then
  (P1 off by orders of magnitude; P2/P3 under the red lenses; P2–P5 failing clusters) are disclosed in the criteria.

## The five posits

The cold surplus gravitates in the Newtonian way (class A, CFG888). A surplus s per unit settled cold energy gives
E = ln(1 + sφ), with φ = 1 − g_bar/g_law. Each dwarf is solved self-consistently: the posit sets σ_*, and σ_* feeds back into
the posit.

| | minimal form | constant (canonical / alt) |
|---|---|---|
| P1 | ρ_x = 3P_b/c_*² (trace of the baryons' random stress) ⇒ X = 3Σm_kσ_k²/c_*², E = ln(1 + X/ν) | none: calibration impossible |
| P2 | s = Σ m_k (v_2/σ_k)³ exp(−v_rot,k²/2σ_k²): velocity-space density at the cold energy's velocity, unsaturated limit | v_2 = 6.95 / 6.46 km/s |
| P3 | latched phantom of the baryons at binding, L = 1 + (M*/M_b)(v_w/v_c)², g = g_bar + g_L(Lg_bar) − Lg_bar | v_w = 27.6 / 23.9 km/s (lower root, A1-3) |
| P4 | s = (ρ̄_b/Q_*) Σ m_k (2πσ_k²)^−3/2 exp(−v_rot,k²/2σ_k²): phase-space density, a second variable at fixed f_P | Q_* = 5.04e-7 / 6.30e-7 M_⊙ pc⁻³ (km/s)⁻³ |
| P5 | the record's settled field is QUMOND; discs depart from the algebraic RAR by δ_disc, absorbed in κ ⇒ spheres and lensing at E = −⟨δ⟩ | ⟨δ⟩ = −0.0214, so E_P5 = +0.021 |

Inputs and brackets (lens central masses and sizes, f_P proxies, SPARC and dwarf-gas dispersions) are as frozen in criteria
section 3.

**A coincidence flag.** P2's calibrated v_2 ≈ 6.5–7 km/s lies close to the record's clump velocity scale (CFG877 7.53 km/s;
CFG878's hydrogen-cooling 7.4–8.2 km/s). It is the same dwarf data seen through a σ⁻³ selector. It is a coincidence, not a
derivation.

## Facts and results (V0; E in ln units, dex = E/ln 10)

Observed values and nominal predictions (canonical / alt):

| fact | observed | P2 pred | P3 pred | P4 pred | P5 pred |
|---|---|---|---|---|---|
| F0 dwarfs (calibrator; graded for P5) | +0.856 ± 0.102 / +0.765 ± 0.102 | = | = | = | +0.021 |
| F1 red/sph lenses | +0.293 ± 0.067 / +0.203 ± 0.067 | +0.000 | +0.007 / +0.005 | +0.005 / +0.003 | +0.021 |
| F2 blue/disc lenses | +0.008 ± 0.091 / −0.083 ± 0.091 | 0.000 | +0.010 | 0.000 | +0.021 |
| F3 SPARC small | +0.137 ± 0.084 / +0.057 ± 0.084 | +0.001 | +0.022 | +0.005 | 0 |
| F4 SPARC large | +0.002 ± 0.050 / −0.053 ± 0.050 | 0.000 | +0.003 | 0.000 | 0 |
| F5 clusters | +0.560 ± 0.077 / +0.476 ± 0.077 | 0.000 | 0.000 | 0.000 | +0.021 |
| F6 cluster slope dE/dlog g_bar | +0.831 ± 0.157 / +0.841 ± 0.156 | 0 | 0 | 0 | 0 |
| F7 DW − LS at matched g_bar | +0.628 ± 0.130 / +0.627 ± 0.130 | +0.887 / +0.794 | +0.871 / +0.781 | +0.900 / +0.808 | 0 |
| F8a dwarf cells χ²/5 (p) | — | 1.9 (0.87) | 3.6 (0.61) | 5.7 (0.33) | 92 (2e-18) |
| F8b dwarf slope dE/dlog g_bar | −0.659 ± 0.164 / −0.656 ± 0.164 | −0.773 | −0.549 | −0.304 | 0 |
| F9 gas split (HI − gas-free) | −0.156 ± 0.277 / −0.152 ± 0.277 | −0.069 | −0.121 | −0.159 | 0 |
| F10 size split dE/dlog r12 | −1.356 ± 0.179 / −1.355 ± 0.179 | −1.083 | −0.657 | −1.504 | 0 |

"=" means fixed by the calibration.

**Grading.**
- FAIL rule: min |z| ≥ 3 at EVERY bracket corner, or a sign wrong at every corner.
- Trials factor: N_T = 5 posits; Bonferroni z_TF = 4.06 over 5 × 11 facts.
- Nominal z values, canonical:

| posit | F1 | F3 | F5 | F6 | F7 | F8b | F10 | dwarf χ² p |
|---|---|---|---|---|---|---|---|---|
| P2 | −4.4 | −1.6 | −7.3 | −5.3 | +1.6 | −0.7 | +1.5 | 0.87 |
| P3 | −4.3 | −1.4 | −7.3 | −5.3 | +1.5 | +0.7 | +3.9 | 0.61 |
| P4 | −4.3 | −1.6 | −7.3 | −5.3 | +1.7 | +2.2 | −0.8 | 0.33 |
| P5 | −4.1 | −1.6 | −7.0 | −5.3 | −4.8 | +4.0 | +7.6 | 2e-18 (F0 −8.2) |

**Lenient-corner minima (min |z| over corners)** for the red lenses:
- P2: 4.38 / 3.03;
- P3: 4.19 / 2.90;
- P4: 3.79 / 2.59.

For P2–P4, the clusters' minima are 7.28 / 6.19 (F5) and 5.31 / 5.38 (F6).

**Globulars** (stiffness-conditional, no class weight). Without screening, every cold-energy posit would put a large excess in
globulars:
- P2: median s 44, E 3.5;
- P3: median L 80, E 2.2;
- P4: median s 1e4, E 9.

So all of them need the L* ≥ 24 pc stiffness screening (CFG820) to remove it.

**Variants.**
- **V6 (floor 0.10 dex)** keeps every class. The red-lens failure of P2–P4 disappears under V6, so that failure is
  floor-sensitive, like CFG919's. The cluster failures remain (min |z| 3.3–4.0).
- **V7 (no +0.123 dex on the n > 2 lenses)** keeps every class and deepens the red-lens failures.
- No posit is FRAGILE.

**VC (cluster facts withheld, a conditional class pending CFG922):**
- P2 FAILS: canonical F1 4.38, robust to the trials factor; alt F1 3.03, local.
- P3 FAILS: F1 4.19, robust; F10 3.88 / 3.94.
- P4: canonical FAILS (F1 3.79, local); alt UNDERDETERMINED (F1 min |z| 2.59; F8b 2.01). Split → UNDERDETERMINED.
- P1 and P5 FAIL.

## A1 diagnostics (post-freeze, no class weight)

- **P1 equilibrium domain.** Inside the frozen domain the runaway threshold is c_crit = 49.6 km/s, set by NGC 205
  (log g_bar −9.88, outside the graded cells). P1's largest dwarf class mean there is 0.006, against 0.856 observed.
- **P1 "relaxed"** (equilibrium required only inside the graded cells):
  - The threshold becomes 9.49 km/s, set by Fornax, and NGC 147, NGC 185 and NGC 205 then run away.
  - The class mean is 0.73 at c_* = threshold × (1 + 1e-7) and 1.17 at × (1 + 1e-12). The dwarf mean is reachable only by
    fine-tuning c_* to within ~1e-9 of Fornax's runaway, with the whole class mean carried by one dwarf at the edge of
    instability.
  - Physically, P1's self-consistent excess is E = −ln(1 − w r12 g_bar/c_*²). It feeds back on itself and diverges only
    logarithmically, so a stress coupling cannot give a uniform +0.37 dex.
- **P3 upper root** (v_w 1185 / 1582 km/s). It over-predicts every lens class by z +16 to +21 and fails the dwarf shape
  (χ² 49 / 62 on 5 dof). It is not a rescue.
- **P5 disc correction δ(R)** (QUMOND minus the in-plane RAR):
  - from −0.43 / −0.33 / −0.14 at R = 0.5 R_d to about +0.02 beyond 4 R_d, for central g_N/a0 = 0.1 / 1 / 10;
  - mean over 1–6 R_d: −0.030 / −0.024 / −0.010, so ⟨δ⟩ = −0.0214;
  - with the simple ν it is −0.0209.

  The sign is right: spheres sit above the disc-calibrated law. The size is about 40× too small. This closes CFG919's theory
  note item 3: geometry is not the selector.

## Controls

| control | result |
|---|---|
| K1 | CFG919 input/cell code exec'd read-only: 7/7 of its checks pass, including CFG914's 9 |
| K2 | CFG919 V0 cells reproduced exactly (37 × 2, max diff 0) |
| K3 | CFG919 class means and F1 (A, sA, χ²) reproduced to 1.1e-16 by this lane's GLS |
| K4 | 33/33 quoted source numbers match the source files: CFG687 A_MID 1.910 ± 0.119 / 1.754 ± 0.109; CFG829 blue A 1.016 ± 0.086; CFG850; CFG845 D −0.273 ± 0.026; CFG820 L95 23.96 / 24.72 pc; CFG876; CFG860 c0 −0.150 / cG −0.064; CFG920 M_req 3.815 / 3.185, UNDERDETERMINED |
| K5 | zero surplus gives E = 0 everywhere (3e-16); P1 closed form equals bisection (1e-16); root residuals 2e-14 |
| K6 | dwarf inputs equal CFG919's f_sph exactly; σ_law reproduced to 9e-16 |
| K7 | P5 numerics: (a) Freeman 1.3e-4; (b) Plummer 2.9e-3; (c) QUMOND Plummer 2.7e-3; (d, A1) Kuzmin exact QUMOND 1.3e-3 |
| K8 | interpolated vs exact calibration: 6e-16 |
| MUTATE sign | **BITES**: all 16 cases FAIL. M1a: reversed-surplus P1–P4 cannot be calibrated. M1b: sign-flipped predictions FAIL (decisive F10) |
| MUTATE inject | **RECOVERED** on both footings. 200 realizations each from the posit's own predictions: P2 FAILS 3.0% / SURVIVES 61.5%; P3 4.5% / 62.0% (alt 61.5%); P4 3.0% / 61.0%; P5 6.0% / 55.0%. P1 is not injectable (A1-4) |

## No sealed prediction

No posit survives on any footing, so no sealed prediction is written (criteria section 8). P4 is UNDERDETERMINED only under
VC on the alt footing. That is not a survival, and no prediction was sealed for it.

## What this means for the cold sector

- Within the declared class (one new constant on top of CFG638, fixed on the dwarfs), the excess selector is not found.
- The dwarf excess has the shape of a velocity-scale selector: P2 and P4 reproduce the dwarf g_bar trend, size trend and
  shape. But that same scale kills the red-lens excess.
- The red lenses (+0.13 dex at 30–300 kpc, around galaxies with σ ~ 100 km/s) and the cluster cores (rising with g_bar) need
  something else.
- Candidates left outside this lane:
  - a second constant (a two-component selector);
  - a non-local or history selector beyond CFG915/916;
  - a baryon-accounting resolution for one or both of the hot classes (CFG922 for clusters; CFG580–582 left the early-type
    shortfall standing).

## Limitations

- Lens kinematics, masses and sizes are proxies: B21 colour medians, CFG919's f_P proxy, Shen+03 sizes. They are bracketed,
  and FAILS requires failure at every corner.
- SPARC random σ is a declared 10 km/s for all baryons (bracket 6–20). Bulges are not treated separately.
- Clusters: ΔΣ excess ≈ g excess per band, stacked with the cell's own weights. σ_ICM² = v_c²/3.
- P3's loss uses present radii and an energy-driven escape law. Real loss histories and SFHs are CFG923's domain; CFG923
  found the framework clock binds too early for 4 of 7 dSphs (canonical).
- P5 uses a razor-thin exponential disc. Thick discs and bulges are not modelled.
- The dwarf excess is taken at Υ_V = 2 with CFG880's gas, as in CFG919. The lens excess is taken with CFG850's +0.123 dex
  (V7 drops it).
- Early-type galaxies with stellar dynamics: NOT TESTED.

## Reproduce

One core, < 0.5 GB, seconds to a minute each, nothing downloaded:
- `CFG921_KONLY=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg921.py` → `cfg921_K.out`, `cfg921_results_K.json` (exit 0)
- `CFG921_MUTATE=sign ...` → `cfg921_MUTATE_sign.out`, `cfg921_results_MUTATE_sign.json` (exit 1 = bites)
- `CFG921_MUTATE=inject ...` → `cfg921_MUTATE_inject.out`, `cfg921_results_MUTATE_inject.json` (exit 0 = recovered)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg921.py` → `cfg921.out`, `cfg921_results.json` (exit 0)

No other lane's files were edited. CFG919 code is exec'd read-only (with writes refused), and through it CFG914/880/883/687.
The other lanes' JSON/out files were only read.
