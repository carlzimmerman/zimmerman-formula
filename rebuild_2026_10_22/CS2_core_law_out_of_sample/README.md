# CS2_core_law_out_of_sample: the CS1 law fixed on SPARC + MW does not beat OS1 out of sample (UNDECIDED: TRADES / NO BETTER)

Criteria and ledger: `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md`, committed alone in f8674a8eec before any script or
number.

Amendments: two post-result check-definition fixes, each committed alone before its rerun. Neither changed a class.
- `AMENDMENT_A1.md` (80584b85a7): OS1's literal a₀ in the dwarf comparator.
- `AMENDMENT_A2.md` (761674b6d3): each law carries its own σ pivot. SC1's run-time σ_ref is 70.49854608; the CS2 pivot is
  70.50.

Standing caveats:
- κ = ½ is FITTED.
- The two footings are scored separately and never pooled.
- Route E. Cold dark energy is a gravitating field component, never a particle.
- Not "theory closed". Nothing here says the data favour the framework or ΛCDM.

## Calibration (SPARC + MW only, printed before any other class)

CS1's per-system Burkert Σ₀: 165 two-sided SPARC galaxies plus the Milky Way, fitted with CS1's own fit code.

    log Σ₀ = 2.2254 ± 0.0217 + (0.8869 ± 0.0878) log(σ / 70.5 km/s),   s_int 0.249 dex

- That is Σ(70.5) = 168 M☉ pc⁻², i.e. 1.57 Σ_a₀ canonical and 1.30 alt.
- The slope equals OS1's canonical q_f (0.892).
- The amplitude is +0.20 dex above OS1 on canonical and +0.11 dex on alt.
- The native core-radius law fitted at the same step is log r₀ = 0.778 + 0.657 log(σ/70.5). Its scatter is 0.63 dex,
  so r₀ is not set by σ.

## Out-of-sample grades (no refit)

Record machinery, read-only: OS1/SC1 for the eRASS1 cells, GR1 for groups and SLUGGS, OS1/CD1 for dwarfs, and the
matched-clumping profiles for X-COP. Each cell reads CS2 (OS1 comparator in brackets), canonical; alt alongside where it
differs.

| class | canonical | alt | grade |
|---|---|---|---|
| eRASS1 cells | 11/15 (14/15) | same counts | FAILS, worse than OS1 |
| groups (63) | mean +0.064, Z +1.58 (+0.077, Z +1.94) | +0.064 (+0.074) | PASS, same as OS1 |
| SLUGGS (4) | mean +0.126, 1/4 cleared (+0.127) | same | FAILS, same |
| dwarfs (89) | EXCLUDE: 0.506 with z ≥ 2, median S 3.01 (0.652, 4.78) | 0.506 (0.483) | FAILS; better than OS1 on canonical, same on alt |
| X-COP (35 points, 0.1–0.7 R500) | mean Δ −0.151, rms 0.205 (−0.075, 0.124) | (−0.035, 0.092) | FAILS, worse than OS1 |

The eRASS1 failing keys under CS2:
- INNER M-all |Z| 3.90;
- INNER all |Z| 2.88;
- MID T3 |Z| 2.36;
- MID T1 |Z| 2.14.

All four are over-predictions.

**Lane class:**

| footing | class |
|---|---|
| canonical | **CS2 TRADES** (better on dwarfs; worse on eRASS1 and X-COP) |
| alt | **CS2 NO BETTER** |
| verdict | **UNDECIDED** (footings disagree) |

**Native r₀ variant (reported, no class).** Mass rules are replaced by the σ-law for r₀. It is far worse:
- eRASS1 6/15, MID and OUTER under-predicted (G-OUT-M3 |Z| 10.5);
- groups ABOVE LAW at Z +31.9;
- X-COP mean Δ +0.36.

A core-radius law in σ does not transfer from galaxies to clusters.

## Reading

**The slope transfers; the amplitude does not.** SPARC + MW alone reproduce OS1's slope (0.887 vs 0.892). But the
free-halo amplitude is 0.1–0.2 dex higher than the amplitude OS1 got by normalising halos to EM1's M200.

Carried into the record's mass-normalised machinery, that extra amplitude over-builds cluster cores:
- 4 eRASS1 inner and MID keys fail high;
- X-COP's inner profile is over-predicted by 0.15 dex.

It helps the dwarfs only partly: they stay EXCLUDE (0.51 with z ≥ 2 against OS1's 0.65 / 0.48).

The CS1 Σ₀ and the machinery's Σ are not the same quantity. A free Burkert fit and a mass-normalised Burkert with the
same Σ give different halos. So the measured law cannot simply be dropped into the record's graders without that
normalisation mismatch.

The groups pass under both laws, and SLUGGS fails under both. Neither class responds to the amplitude at this level.

**The graders' mass rules are borrowed.** This is disclosed in the ledger (L3, L4):
- the eRASS1 halos use Mfair = 5.364 M_b, a Planck baryon fraction;
- groups and SLUGGS use EM1's CLASS/Bullock M200 relation.

The request named OS1's machinery, and K0 needs it, so those are the graded rows. The only fully native row (the r₀ law)
fails badly, so there is not yet a native way to normalise a predicted halo. That gap is the open item.

## Checks 6/6

| check | what it confirms |
|---|---|
| K1 | 165 SPARC + 1 MW calibration points; CS1's fit code |
| K0b | GR1's own K0 checks pass inside this run |
| K2 | X-COP equals the matched-clumping lane exactly |
| K0 (each footing) | at OS1's law the machinery reproduces OS1 and GR1: eRASS1 cells ≤ 3e-7, dwarfs 0, groups ≤ 3e-14, SLUGGS ≤ 8e-16 |
| K3 | 0.74 GB, one thread |

**MUTATE** (`CS2_MUTATE=1`): σ is permuted across the 166 calibration systems. The recalibrated q is −0.05 ± 0.11
(−0.5σ). **The tooth bites; exit 1.** Under the mutated law (reported), X-COP saturates in all 7 clusters, mean Δ +0.56.

## Files and run

- `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md`
- `cs2_out_of_sample.py`
- `cs2_out_of_sample.out`, `cs2_out_of_sample_results.json`
- the `_MUTATE` twins of the output and results files
- `cs2_x30_machinery*.log` (local only, gitignored)

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs2_out_of_sample.py               # ~1 min, exit 0, 6/6
    CS2_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs2_out_of_sample.py  # exit 1 = tooth bites
