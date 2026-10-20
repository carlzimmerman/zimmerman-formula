# CFG920: does the D-i route's post-formation baryon loss fit the dwarfs' own chemistry? CONDITION TEST. Class: UNDERDETERMINED (both footings)

**Label: CONDITION TEST** of the dwarf route D-i of CFG915 (inherited by CFG916's LR-c). Criteria: `FROZEN_CRITERIA.md`, committed
alone first (a229bb78c), block 920–929. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are kept apart and never pooled. Raw
data and framework-native quantities only. Cold energy is real gravitating mass; no particle species is added. Not "theory closed".
Nothing here says the data favour the framework.

## The question

D-i holds a faint dwarf's excess as cold energy bound at its formation and retained after the baryons left. In the deep regime each
dwarf then needs a post-formation loss factor L_req = M_b,form/M_b,now = exp(4E), with E = ln(σ_obs/σ_law) from CFG827. CFG915's median
is ×4.32 (about 77% of the formation baryons lost). CFG852 tested only a correlation. This lane tests the **amount**: can each dwarf's
mean stellar [Fe/H], present gas and SFH hold its own L_req?

**Bound (declared, never fitted per dwarf).** The bound is a one-zone homogeneous leaky box:
- instantaneous recycling and mixing, no inflow, primordial start;
- wind at the ISM metallicity;
- Fe yield log y ∈ {−0.5, −0.2, +0.1} (CFG317's bracket).

Two outflow forms are declared:
- **W1**, continuous wind (CFG317's estimator).
- **W2**, W1 plus terminal removal of the gas left at quench (gas-free dwarfs only).

Gas that never mixed into the star-forming gas can only raise L, so each corner allows [L_min, ∞). **"Cannot hold" means the chemistry
demands more post-formation loss than D-i allows**, so D-i would over-predict that dwarf's excess.

## Result

**Sample median** (tested N = 20; M_req 3.81 canonical / 3.18 alt; ratio = M_req / median L_min, bootstrap 16–84%):

| corner | median L_min | ratio, canonical | ratio, alt |
|---|---|---|---|
| −0.5, W2 (most favourable) | 3.34 | 1.14 [0.83–3.14] | 0.95 [0.69–2.63] |
| −0.5, W1 | 4.31 | 0.89 [0.62–3.14] | 0.74 [0.52–2.62] |
| −0.2, W2 | 6.40 | 0.60 [0.43–1.41] | 0.50 [0.36–1.18] |
| −0.2, W1 | 8.68 | 0.44 [0.31–1.40] | 0.37 [0.26–1.17] |
| +0.1, W2 | 12.52 | **0.31 [0.22–0.66]** | **0.25 [0.18–0.55]** |
| +0.1, W1 | 17.41 | **0.22 [0.16–0.65]** | **0.18 [0.13–0.54]** |

**SAMPLE-MEDIAN CLASS: UNDERDETERMINED on both footings, so the overall class is UNDERDETERMINED.**
- At the lowest yield the median ×4 loss is held.
- At the highest yield it is excluded: the chemistry then wants a median ×12–17 loss, and the 84th percentile of the ratio is below 1.
- The class therefore hinges on the Fe yield.
- CFG915's headline 4.32 (all 28) divided by M_k runs from 1.29 (−0.5, W2) to 0.25 (+0.1, W1).

**Per dwarf** (graded at 1σ in E and [Fe/H]; 8 of 28 NOT TESTED for lack of an LVD metallicity: And XIII, And XI, And VI, LGS 3,
NGC 185, NGC 147, NGC 205, M 32):

| footing | COMPATIBLE | UNDERDETERMINED | CONTRADICTED | central values (C / U / X) |
|---|---|---|---|---|
| canonical | 1 (NGC 6822) | 15 | **4: Hercules, Andromeda II, Cetus, IC 1613** | 4 / 7 / 9 |
| alt | 0 | 15 | **5: the same four plus Leo IV** | 4 / 6 / 10 |

| dwarf | gas | [Fe/H] | L_req can / alt | L_min (W2/W1) at −0.5 | at −0.2 | at +0.1 | graded can / alt |
|---|---|---|---|---|---|---|---|
| Andromeda VII | no | −1.37 | 1.70 / 1.42 | 2.99 / 4.16 | 5.70 / 8.30 | 11.1 / 16.6 | U / U |
| Hercules | no | −2.64 | 1.09 / 0.91 | 51.0 / 77.5 | 102 / 155 | 202 / 309 | **X / X** |
| Leo IV | no | −2.56 | 11.2 / 9.28 | 42.5 / 64.5 | 84.5 / 129 | 168 / 257 | U / **X** |
| Canes Venatici II | no | −2.85 | 61.4 / 51.0 | 82.6 / 126 | 165 / 251 | 328 / 500 | U / U |
| Andromeda V | no | −1.84 | 23.9 / 19.9 | 8.30 / 12.3 | 16.3 / 24.5 | 32.3 / 48.9 | U / U |
| Andromeda I | no | −1.51 | 3.29 / 2.74 | 4.03 / 5.75 | 7.77 / 11.5 | 15.2 / 22.9 | U / U |
| Tucana | no | −1.58 | 2.17 / 1.81 | 4.68 / 6.75 | 9.08 / 13.5 | 17.9 / 26.9 | U / U |
| Andromeda II | no | −1.47 | 0.84 / 0.70 | 3.70 / 5.24 | 7.11 / 10.5 | 13.9 / 20.9 | **X / X** |
| Andromeda III | no | −1.75 | 12.2 / 10.2 | 6.80 / 9.98 | 13.3 / 19.9 | 26.3 / 39.8 | U / U |
| Cetus | no | −1.74 | 1.80 / 1.50 | 6.65 / 9.76 | 13.0 / 19.5 | 25.7 / 38.8 | **X / X** |
| Sagittarius | no | −0.53 | 1.00 / 0.83 | 1.00* / 1.00* | 1.10 / 1.20 | 1.85 / 2.40 | U / U |
| Aquarius | HI | −1.44 | 3.34 / 2.78 | 1.00* | 1.87 | 4.13 | U / U |
| Phoenix | HI | −1.49 | 11.8 / 9.83 | 4.46 | 9.06 | 18.2 | U / U |
| Pegasus dIrr | HI | −1.39 | 7.28 / 6.06 | 1.21 | 2.73 | 5.83 | U / U |
| IC 1613 | HI | −1.19 | 0.28 / 0.23 | 1.00* | 1.97 | 4.26 | **X / X** |
| Leo T | HI | −1.74 | 15.1 / 12.5 | 1.35 | 3.07 | 6.61 | U / U |
| NGC 6822 | HI | −1.05 | 4.28 / 3.58 | 1.00* | 1.00* | 1.49 | C / U |
| Sagittarius dIrr | HI | −1.85 | 4.37 / 3.65 | 1.21 | 2.80 | 6.08 | U / U |
| WLM | HI | −1.28 | 5.26 / 4.40 | 1.00* | 1.00* | 2.14 | U / U |
| Leo A | HI | −1.60 | 3.35 / 2.79 | 1.00* | 1.62 | 3.64 | U / U |

\* The chemistry under-produces the observed [Fe/H] at that corner. As frozen, η = 0 and L_min = 1; pre-enrichment would be needed.
This convention favours D-i. Gas-bearing dwarfs have W2 = W1 (one value per yield).

## Reading: the sample splits into two populations

**Gas-free dSphs (11): the chemistry wants more loss than D-i can absorb.**
- At the nominal yield (−0.2, W1), the loss the chemistry implies would give each of the 11 a larger excess than it shows: E_pred = ln L_min/4 > E_obs,
  on both footings. At the most favourable corner (−0.5, W2) the count is 8 of 11 canonical and 9 of 11 alt (post-hoc summary line).
- In the homogeneous box, a metal-poor dSph either lost a large mass in its wind or kept most of its gas unprocessed until a terminal
  strip. Either way L lies between y/(e·Z_g) (closed box plus strip) and 0.56 y/Z_g (W1), with Z_g = 10^[Fe/H]. At the nominal yield
  that is ×5.7–165 for ten of the eleven; Sagittarius ([Fe/H] −0.53) needs only ×1.1.
- In 32 of 32 feasible gas-free cases the most favourable member is the pure closed box plus terminal strip (η = 0).
- Graded: 0 C / 8 U / 3 X canonical; 0 / 7 / 4 alt. Hercules (L_req 1.1 against L_min ≥ 51) is CONTRADICTED even at 2σ.

**Gas-bearing dIrrs (9): the chemistry needs little loss, and D-i's stars-only L_req then needs loss the chemistry cannot see.**
- L_min is 1.0–4.5 at −0.5 and 1.0–9.1 at −0.2. Several low-yield corners under-produce [Fe/H].
- Their stars-only L_req is 3.3–15 (IC 1613: 0.28, no excess). For the 8 with an excess, holding it needs unseen unprocessed loss of
  ×1.3–5.3 above the nominal-yield W1 value.
- V-NOUNSEEN: 4 of 9 need it even at yield +0.1 (central): Pegasus dIrr, Leo T, NGC 6822, WLM.
- **V-GAS** counts the HI in the law's baryons (CFG873's "all-gas" end). L_req then falls to 0.12–9.9: below 1 for Aquarius, IC 1613,
  NGC 6822, Sagittarius dIrr, WLM and Leo A.
  - Graded classes move NGC 6822 C → U and Leo A U → X. Sagittarius dIrr goes to X on the alt footing.
  - So for the gas-rich dwarfs, how much of the "excess" D-i must explain is set mostly by the gas bookkeeping CFG915 inherited from
    CFG827 (stars only).

## Timing map (reported; binding after a fraction F of the star formation, Weisz+14 clock)

D-i binds the cold energy at formation, so all chemistry-traced loss comes after binding. Results at yield −0.5, canonical:
- **AT FORMATION: 11.** Andromeda V, Andromeda III and Sagittarius among the gas-free dSphs, and 8 of the 9 gas-bearing dwarfs.
- **LATE: 7.** Andromeda VII, Hercules, Leo IV, CVn II, Andromeda I, Tucana and Cetus hold their L_req only if binding followed
  51–99.9% of their star formation (F_need 0.51–0.999).
- **NONE: 2.** Andromeda II and IC 1613 have no excess to hold.
- At −0.2: 9 at formation, 1 EARLY (Andromeda III, F 0.39), 8 LATE, 2 NONE. Alt: 10 / 0 / 6 / 4 at −0.5.

**So in the homogeneous box, the metal-poor gas-free dSphs fit D-i's amount only if their cold energy was bound after most of their
stars had formed.** That contradicts "bound at formation". The quench epochs themselves allow a post-formation loss of the needed size:
for gas-free dwarfs the terminal loss falls at τ90, after any binding at formation.

The t_need values for F_need ≳ 0.9 are resolution-limited. Weisz+14 gives cumulative fractions to 0.01, and Hercules has 91% of its
stars by 12.6 Gyr, so its F_need of 0.999 lands in the late tail at 0.64 Gyr.

## Escapes outside the declared bracket (reported, no class weight)

- **Metal-enhanced winds.** At yield −0.5, a wind ζ times the ISM metallicity holds the central L_req for:
  - 11 dwarfs at ζ = 1 (canonical);
  - CVn II 3.0, Andromeda I 3.0, Andromeda VII 7.5, Tucana 8.2, Leo IV 10.4, Cetus 19 (alt 3.8–31);
  - Hercules only above ζ = 1000; Andromeda II, IC 1613 (and alt Hercules, Sagittarius) never, because L_req ≤ 1.

  No ζ > 1 is declared standard here; these numbers are the price of the escape.
- **Pristine inflow after binding** (later lost) decouples [Fe/H] from L. The leaky box excludes it by definition, so it is not modelled.

## Variants (reported, not graded)

- **V-COL** adds Collins+13 [Fe/H] for And XIII, XI and VI (L_req 19.4, 88.6, 9.6). All three are UNDERDETERMINED, and the sample median
  over 23 stays UNDERDETERMINED (−0.5, W2 ratio 1.11 canonical / 0.93 alt).
- **V-TR**, the 8 MW training dwarfs: CVn I is CONTRADICTED on both footings (L_req 9.6 against L_min ≥ 25.7); Sculptor is CONTRADICTED
  on the alt footing; the rest are UNDERDETERMINED. Draco (19.4 against 18.7) and Ursa Minor (16.4 against 20.0) sit at the edge of the
  most favourable corner.
- **V-2σ**: 0 / 19 / 1 (Hercules) on both footings.

## Controls

| K | result |
|---|---|
| K1 CFG827/CFG915 | all 36 E_SFH reproduced exactly (max \|ΔE\| 0); alt ρ +0.078883 = stored; loss factor median 4.324714, p16 1.184758, p84 17.7686, n_le1 3, N 28 = CFG915 |
| K2 CFG852 | primary N 22, slope 0.507934, ρ −0.107849; secondary N 67, 0.344138, −0.023505: all equal to the stored values (≤ 1e-9) |
| K3 CFG317 | 318 stored estimator entries (3 yields) reproduced: max rel Δη 1.2e-13, max \|Δ log R_ind\| 4.1e-14 |
| K4 numerics | ζ > 1 closed form vs ODE 1.8e-13; ζ = 1 quadrature vs closed form 6.2e-15; W2 η = 0 endpoint vs closed-box formula 1.3e-15 |

**MUTATE BITES (exit 1).**
- L ≡ 1 gives per-dwarf 0 C / 9 U / 11 X and a CONTRADICTED median.
- L ≡ 20 gives 9 / 8 / 3 and an UNDERDETERMINED median.
- 17 of 20 dwarfs change class. The median machinery can therefore return CONTRADICTED.

## Disclosures and post-freeze items (2026-10-20)

- **Implementation fix before any result.** The first run crashed (NaN in CFG317's closed form at truncations u < 1e-17), so no number
  was printed. `elnx` now uses the exact power series for u < 1. K3/K4 confirm agreement with the closed form.
- **Reporting-line fix after the first run.** The W2-endpoint line now counts feasible cases (32 of 32, 1 under-produced) instead of
  "32 of 33". No number changed; diffed.
- **Post-hoc reporting summary**, labelled in the script, added after the first full run. It holds the gas-free / gas-bearing split
  counts and E_pred > E_obs counts, computed only from values already in the JSON. Every other output line and JSON value was unchanged
  (diffed).
- **Implementation check (not frozen).** The Gauss quadrature of the ζ > 1 term agrees with adaptive quadrature to 1.1e-5 in ln Z
  (5e-6 dex). It affects only the ζ_need map.
- **Not blind to inputs** (criteria §2). The CFG827 E values, the LVD metallicities and CFG317's R_ind were seen before freezing.
  CFG317 led the author to expect that the homogeneous box would demand more loss than L_req for metal-poor dSphs, and it does.
- **Approximations.**
  - D-i's amount relation is deep-regime, t-dominated and order of magnitude (CFG915).
  - Stars-only E is CFG915's definition.
  - Instantaneous recycling for Fe is carried by the yield bracket.
  - Number-weighted RGB [Fe/H] vs mass-weighted mean log Z is covered by the 0.1 dex allowance.
  - One zone; no MDF-shape fit.
- **Compute.** One core, nice 10, about 2 s per run, peak about 100 MB. One process at a time, beside the live 1024³ job; no other
  process was touched. Nothing was downloaded.
- **Not claimed:**
  - any measured formation-epoch baryon mass;
  - that D-i is excluded;
  - that metal-enhanced winds or inflow happened;
  - κ derived;
  - "theory closed".

## What this means for CFG915/916

The ×4.3 condition is **not excluded** by the dwarfs' chemistry at the sample-median level. It is **not established** either: it holds
at a low Fe yield and fails at a high one.

The per-dwarf map shows where it strains. For the metal-poor gas-free dSphs the standard leaky box demands more post-formation loss than
D-i can absorb. Binding at formation would then over-predict their excess. They are rescued only by:
- a low effective Fe yield;
- metal-enhanced winds (ζ ≈ 3–19); or
- cold energy bound after most of their star formation, which contradicts the route's own premise.

For the gas-rich dIrrs the loss must be mostly unprocessed, or their excess largely disappears once their gas is counted.

A decisive version needs one of:
- an Fe-yield / SN Ia-fraction constraint ([α/Fe] is not on disk);
- MDF shapes;
- a native formation epoch for dwarfs.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (a229bb78c) |
| `cfg920.py` | K1–K4; CFG827 code path (E on both footings); leaky-box W1/W2; classes; bootstrap median; timing map; ζ_need; variants; MUTATE |
| `cfg920.out`, `cfg920_results.json` | main run (exit 0: 4/4 K pass) |
| `cfg920_MUTATE.out`, `cfg920_results_MUTATE.json` | MUTATE run (exit 1 = tooth bites) |

Rerun from this directory with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg920.py`, then the same command with `CFG920_MUTATE=1`. Both
runs are deterministic (seed 920).

Read-only inputs: `real_research/data/dsph` (E-MILES SSPs, Weisz+14 tables 5/6, LVD MW/M31/field, Collins+13), and the result JSONs of
CFG824, 827, 828, 852, 915 and 317. No other lane was edited.
