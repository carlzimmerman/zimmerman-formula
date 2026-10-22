# D8_Lstar_value: what fixes the value of the stiffness length L*?

## Verdict: CRISP FINDING

There are three findings.

1. **A76's L* = σ_c²/a0 and AG6D's stiffness are not the same object.** A76's sound speed *is* AG6D's
   free-medium equation of state, but A76's σ_c is not that equation of state. AG6D's C1 bound rules out
   the 10⁴ K value in the free medium. The identification can survive only in the tethered state.
2. **The record is wrong to say that no datum excludes L* = 23.43 pc** (A76). The 24 pc floor is
   CFG820's globular χ² bound. It was not made by rounding the thermal width. At the thermal L*,
   Δχ² = 3.91 on the canonical footing (a marginal 95 % exclusion) and 5.99 on the alt footing.
3. **On disk, the only per-galaxy HI dispersions at z ≈ 0 are those of 6 tidal dwarfs.** With the frozen
   rule they give a median L* of 42 / 35 pc, which is inside the window. But the 84/16 spread is 4.45×,
   so the values do not form one constant. This is a first look, not the measurement A76 asks for.

- Criteria: `FROZEN_CRITERIA.md`, committed alone (3327019734). AMENDMENT A1 was added before any
  result (ce9340ccbc).
- Script: `d8_lstar_value.py`, 5/5 checks PASS, exit 0, 0.5 s, 49 MB.
- `D8_MUTATE=1` sets K = 8πG. K1 then fails and the run exits 1.
- Rules: κ = ½ is FITTED. The two footings are never pooled. No particle is added. The theory is not closed.

## 1. Adjudication: two relations, one length, and different objects

- **K1: the same formula.** A76 (and A16) take γ = 2πG L*² and c_s² = γρ_c, evaluated at the
  **cosmic mean** ρ_c. That is AG6D Part A's free-medium Γ = 2 relation, c_s² = 2πG L*² ρ̄. At 24 pc it
  gives 0.720398 m/s, a relative difference of 0 from A76.
- **So AG6D C1 applies to it directly.**
  - C1 says the free medium must have L* ≤ 1 pc (frozen scan) or ≤ 0.247 pc (post hoc).
  - Read as L* = σ_c²/a0, that caps σ_c at:

| footing | cap on σ_c (frozen / post hoc) | T cap at μ = 1.22 | σ_th(10⁴ K) / cap |
|---|---|---|---|
| canonical | 1.70 / 0.845 km/s | 427 / 106 K | 4.84 / 9.73 |
| alt | 1.87 / 0.928 km/s | 515 / 127 K | 4.41 / 8.86 |

- **K3: σ_c is not the medium's sound speed.**
  - At L*_th, σ_th / c_s(ρ_c) is 1.17×10⁴ (canonical) and 1.41×10⁴ (alt).
  - The Γ = 2 sound speed equals σ_c only at ρ_eq = a0/(2πG L*) = Σ_M/L*.
  - That density is 4.56 M☉/pc³ (canonical) or 6.65 M☉/pc³ (alt), which is 1.4–2.0 × 10⁸ ρ_c.
  - Here Σ_M = a0/(2πG) is 106.8 / 129.0 M☉/pc².
- **Which reading survives.** "L* = σ_c²/a0 as the EOS stiffness of the free medium" is excluded. "L* = σ_c²/a0
  as a property of the tethered (bound) state" is not excluded. That second reading requires three things:
  - the Γ = 2 stiffness is absent from the free medium until z ≈ 3.7×10³ (AG6D P4, at 24 pc);
  - σ_c belongs to the bound state, i.e. it is inherited from the local gas, so it is not a property of
    the medium;
  - L* is either environment-dependent, or σ_c is a universal floor. CFG820 applies one universal L* to
    gas-free globulars, and CFG821 does the same for gas-poor dSphs. That is legitimate only if σ_c is a
    universal constant and not the local gas dispersion.
- None of these is written into the action. A switch for the tethered state does not exist yet.

## 2. Record check: the 24 pc floor is a globular measurement, and it bites the thermal value

- A11's script cites `LS_LO = 24 pc # [EXT] CFG820` (`a11_checks.py:49`). CFG820 is a χ² fit to NGC 2419,
  Pal 4 and Pal 14. The script reproduces it on CFG820's own grid exactly (K4).
- CFG820's quoted L*_95 values (23.957 / 24.721 pc) are limited by its grid. The fine-grid roots are
  **23.641 pc** (canonical) and **24.476 pc** (alt).

| footing | thermal L* (10⁴ K, μ = 1.22) | Δχ²_CFG820 | μ = 0.60 | μ = 1.40 |
|---|---|---|---|---|
| canonical | 23.43 pc | **3.913** (excluded at 95 %, by 0.07) | 47.6 pc, 0.40 | 20.4 pc, 5.03 |
| alt | 19.38 pc | **5.992** (excluded) | 39.4 pc, 0.94 | 16.9 pc, 7.47 |

- **The globular floor expressed as a velocity.**
  - Canonical: σ_c ≥ 8.263 km/s. At 10⁴ K that means μ ≤ 1.209.
  - Alt: σ_c ≥ 9.243 km/s. At 10⁴ K that means μ ≤ 0.966.
- Neutral 10⁴ K gas therefore sits just below the floor on the canonical footing and clearly below it
  on the alt footing. Partly ionised gas is allowed.
- On the canonical footing the thermal width and the globular floor agree to 0.46 % in σ. That agreement
  is a coincidence between a premise and a 95 % bound, and it carries no evidential weight. AG6D B7 had
  already graded it MISS.

## 3. Is σ_c measurable on disk? (frozen rule L*_pred = σ²/a0, coefficient 1)

- **Primary: Lelli+2015 tidal dwarfs.** The file is `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`.
  The values are σ_HI = 20, 20, 12, 10, 10 and 7 km/s, from 3D models of the HI cubes.

| footing | median L*_pred | 16–84 % range | 84/16 | class |
|---|---|---|---|---|
| canonical | 42.2 pc | 31.1–138.5 pc | 4.45 | CONSISTENT, but not one constant |
| alt | 35.0 pc | 25.8–114.7 pc | 4.45 | CONSISTENT, but not one constant |

- **Secondary: ionised σ0 at z ≈ 0.5–3** (695 discs, frozen rule as written, no verdict weight). These give
  450–1050 pc, above the 90 pc ceiling. If σ_c were whatever gas dispersion is present, then L* would
  not be one constant.
- **The window in velocity terms.**
  - Canonical: σ_c ∈ [8.26, 16.1] km/s.
  - Alt: σ_c ∈ [9.24, 17.7] km/s.
  - The often-quoted HI floor of about 7–10 km/s overlaps the bottom of this window. That floor is an
    external input from the literature and is not on disk.
- **Excluded data.** By the frozen protocol the lane excludes ALFALFA, FASHI, xGASS and MIGHTEE widths,
  SPARC and LITTLE THINGS, McQuinn+22, DiskMass `sigMod`, GMC CO widths, and all stellar dispersions
  (AMENDMENT A1).

## What this does not show

- It does not derive σ_c, and it does not write the tethered-state switch.
- The canonical exclusion of the thermal value has a margin of only 0.07 in Δχ². CFG820's Υ_V = 1.6 and its
  0.15 dex width were not varied (no knob scans). The alt exclusion is firmer.
- The tidal dwarfs are less than one orbit old, are seen through kpc beams, and carry turbulent σ. They are
  not the face-on dwarf maps at 30–100 pc that A76 §9 specifies.
- The rule uses the total σ, as frozen. It makes no split into thermal and turbulent parts.
- CFG821's dSph ceiling (22 pc) is conditional and was not re-run.

## Record checked

- DSF-21: A11, A16, A20, A37, A56, A65, A76, and BRIEF §2 (the closed stiffness mechanisms were not re-run).
- AG6D: README and all outputs.
- CFG820, CFG821, CFG575, CFG828, CFG940.
- Register door 4 (`CANDIDATE_LAWS_REGISTER.md:711`).
- A11's "c_s = 0.72c" unit slip was already caught by A16, A31 C108 and FINAL #2. It is not re-reported here.
