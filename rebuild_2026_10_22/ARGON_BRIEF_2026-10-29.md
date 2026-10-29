# Brief for Argon: the most important open puzzle, and every attempt so far (2026-10-29)

**Rules (the record's).**
- κ = ½ FITTED.
- Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled.
- "Cold dark energy" is a gravitating w ≈ 0 field component, never "cold dark matter" or a particle.
- No ΛCDM inputs.
- Frozen criteria are committed alone before any number.
- Not "theory closed".

**Published state:** PAPER64 v1.2, DOI 10.5281/zenodo.23771199 (concept 10.5281/zenodo.23750179).

## THE PUZZLE (highest priority): what physically switches cold dark energy on?

**What works, with a data-located switch (BS1, 979363d820).**
- A system carries a cored cold dark energy halo iff the gravitational **basin** it belongs to is above T ≈ 10^12.3 M☉.
  The basin is the region inside its zero-velocity surface.
- Otherwise the law g = ν(g_N/a₀) g_N acts on baryons alone.
- This passes every canonical calibration line and the Milky Way (Local Group basin 10^12.39).

**Why it is not yet a mechanism.**
1. **T is located, not derived.** The one derivation that looked native was "the switch is the core-floor crossover",
   η(L) Σ_coll(M) = a₀/2πG (CL3). It was **inconsistent**: the switch used a constant coefficient while the cores used
   c_f(M).
   - Made consistent (CSM1), the crossover drops to 10^11.22, many isolated lenses switch on, and lensing fails
     (Δχ² +415).
   - The one allowed refit, L = 2.51, passes lensing but fails groups (Z +2.62).
   - **No single L passes every line with a consistent switch and core.**
2. **The basin is a posit.** The candidate field equation keys condensation on the matter-flow expansion θ < 0, inside
   turned-around regions (`BASIN_FIELD_EQUATION_CANDIDATE_2026-10-28.md`). The step function and the smoothing scale
   are posited, and the threshold still needs T.

**The precise question for Argon:**
> Find a condensation criterion with **no new fitted constant** that is the **same** inequality for the switch and the
> core, and that puts the switch near 10^12.3 M☉ on the basin mass, not 10^11.2.
>
> It must keep KiDS isolated lenses (log M200 ≲ 12.05) on the law, and put the Local Group (10^12.39), groups
> (12.0–13.7) and clusters on halos. It must not be keyed on potential depth, σ or acceleration: those are killed,
> because satellites sit in shallower potentials than the Sun (J1, X19).

**Hard constraints any answer must meet:**
- the Bullet Cluster (no pressure fluid);
- the CMB and transfer-function windows (no hot particles);
- Cassini (screening);
- satellites switched (they sit inside their host's basin);
- the SP2 sealed prediction (sha256 75b5fcdb…8b3d). At fixed M★, basin members lens about half as strongly at 0.3 Mpc
  as isolated galaxies.

## Every attempt on the hardest problems (lane, commit or doc, verdict)

### A. The switch / selector (what turns halos on)

| attempt | verdict |
|---|---|
| X58: mass-keyed switch | the need is non-monotone in mass (dwarfs need halos, L* lenses the law, clusters halos) |
| X59: formation-epoch key | fails |
| X60: acceleration key | fails |
| X19: selector rank test | no single variable or pair separates EXTRA from NONE; the σ/Φ trapping door is killed (Bullet for a fluid; CMB/TG for hot particles) |
| J1: a₀(Φ) potential selector | FAILS: satellites are shallower than the Sun; not in the action |
| X22 / X23: late heating window | fails |
| X62: environment switch (satellite OR above crossover) | the working base |
| CF1: T = core crossover with one c_f | no single c_f |
| CF2: decoupled T | window 12.2–12.5 (canonical) |
| CL1 / CL2: combined budget + native slope | CL2 passes at L = 4 (fragile) |
| DT1: threshold tournament (formation epoch, self-similar, mass-function knee, fair-share) | every native candidate misses |
| CL3: T from L | WITHDRAWN (CSM1 inconsistency) |
| HO1–HO3: held-out tests of CL2 | all failed (MW contradiction, dwarfs, SLUGGS, X-COP, group sign) |
| **BS1: basin switch** | **works** (data-located T); MW fixed |
| TH1: flow-defined basins | reproduces BS1 in the Local Volume (weak test) |
| DS1: hot gas displaces halo | fails |
| CSM1 (other agent): consistent switch/core | no joint pass for any single L |
| basin field-equation candidate (θ < 0 condensation) | written, not derived or graded |

### B. The cluster halo shape (X-COP cores against lensing outskirts)

| attempt | verdict |
|---|---|
| X38 / X43: cored halos, core floor | 14/15 keys; groups Z 2.05 |
| GC1: two-halo term | ≤ 1.3 % effect |
| GC2: turnaround budget | overshoots |
| GC3: self-similar infall shape | fixes centres; outskirts short |
| GS1: measured gas to r_ta | all 15 keys pass (Burkert) |
| IB1: gas-HSE core | fixes inner/mid, trades the outskirts |
| PS1 / PS2: phase-space cap | trades; family closed |
| GT1: gas-temperature core | 14/15; G-OUT-M3 fails |
| BC1: explicit BCG | the BCG is already counted; does not help |
| GX1: infall + measured budget | fixes X-COP **or** lensing, not both |
| SM1: sample comparison | eRASS1 Mgas is 0.11 dex below X-COP; X-COP at the 95th mass percentile; different radii |
| GX2: corrected gas | breaks lensing |
| **Open** | a mass-dependent halo shape is the natural next idea |

### C. κ = ½ (why the 1/2)

| attempt | verdict |
|---|---|
| DSF-21 "κ = Z/4π" | Milgrom's cH/2π, a posit |
| GF2 | the SIS ratio, not a derivation |
| why_4_puzzle W4-01…W4-18 | no selection; the only π-free ½ is a touching-horizon lattice (a menu) |
| 32π campaign | no derivation |
| footing audit | κ = ½ versus 1/2π is footing-conditional |

### D. L, the halo concentration level

| attempt | verdict |
|---|---|
| X48 zooms ng 38 / ng 48 / ng 64 | native c falls with mass, but the level is too high |
| NL1 | L_nat = 4.86 [3.83, 5.81]: fails three cluster keys; not converged |
| CSM2 (other agent) | the first-crossing estimator is binning-sensitive (seed c_f 3 → 17) |

### E. Dwarfs and single-galaxy failures

| attempt | verdict |
|---|---|
| X20 | the hosted-dwarf extra is not tides or binaries |
| X24 | a mass trend; floor c₀ ≈ 4 km/s fixes 3 of 4 classes |
| X25 / X28 | the floor is not in v3s; not a₀-scaled |
| X51 | cooling-floor halos center the classes |
| HO3 | 0.2–0.3 dex per-object scatter |
| IC 1613 (HO3, FD1, RT1, EF1, IN1, IN2) | a failure on two tracers; external field no help; the inclination rescue failed (MUSE i 32–36°) |

### F. The covariant parent (an action)

| attempt | verdict |
|---|---|
| v3 / v3s (Khronon + switched stiffness) | frozen: passes as a galaxy law, fails gravity + cosmology |
| AeST + one operator (PAPER58/59) | Cassini OK; clusters fail |
| P-medium (CFG938) | conditional; ill-posed on FRW |
| MV28 microscopic vacuum (other agent) | building blocks; no full model |

## What a winning answer looks like

A short derivation, with a frozen lane, that:
1. gives the switch and the core from **one** inequality, with no new constant;
2. lands the switch near 10^12.3 on basin mass;
3. passes CL2/BS1's full line set and the MW on the canonical footing;
4. keeps the SP2 sign.

Second priority: a halo shape that passes X-COP (≤ 0.7 R500) and eRASS1 × KiDS lensing (0.7–3 R500) together.
