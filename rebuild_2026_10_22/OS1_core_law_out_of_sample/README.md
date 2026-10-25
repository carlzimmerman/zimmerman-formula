# OS1_core_law_out_of_sample — RESULT: OS FAILS OUT OF SAMPLE (frozen class); clusters nearly pass, dwarfs break

Frozen criteria 71873e76d3 (committed alone; no amendment). κ = ½ FITTED; footings calibrated and scored separately,
never pooled; cold dark energy, not matter; nothing here says the data favour the framework or ΛCDM; not "theory closed".

**Law.** X38's route-E Burkert halos with Σ_i = Σ_a0 (σ_i/σ_ref)^q, σ_ref = 70.50 km/s (the median SPARC galaxy keeps
a₀/(2πG)). This is LN1's T7 core law (Lean-certified) with q = (1+n)/2. q was calibrated **once, on SPARC alone**, then
clusters and dwarfs were graded at that q with no further freedom.

## Result (`os1_out_of_sample.out`)

| | canonical | alt |
|---|---|---|
| **q_f (SPARC only)** | **0.892** | **0.748** |
| SPARC A rms @ Υ, at q_f (at q = 0) | 0.0605 @ 0.79 (0.0795) | 0.0591 @ 0.63 (0.0729) |
| SPARC B at q_f | 0.0609 @ 0.78 | 0.0599 @ 0.62 |
| **clusters out of sample** | **14 / 15 cells pass**; failing \|Z\| 17.61 → **5.31**; one new fail, INNER M-all Z −2.41 (over-predicts) | **14 / 15**; 14.26 → **4.40**; INNER M-all −2.06 (over) |
| cluster grade (frozen) | FAIL (because of the one new failure) | FAIL |
| dwarfs out of sample | **EXCLUDE**: 65% at z ≥ 2, median S 4.78 | **EXCLUDE**: 48%, median S 2.74 |
| dwarfs stay CONSISTENT only for q ≤ | 0.13 | 0.22 |
| **lane class** | **OS FAILS OUT OF SAMPLE** | **OS FAILS OUT OF SAMPLE** |

Checks 5/5 (K0: q = 0 reproduces X38 and CD1 exactly; K1: q = 1/3 reproduces SC1). **MUTATE** permutes σ across the
SPARC galaxies before calibrating. The SPARC gain collapses from 0.0190 / 0.0138 dex to 0.0003 / 0.0002, so the gain comes
from the real σ ordering, not from a free parameter. Exit 1, as frozen.

## What it means

1. **A single constant fixed on galaxies predicts the clusters.** Galaxies alone want core surface density rising as
   Σ ∝ σ^0.75–0.89. Carried unchanged to 326 eRASS1 clusters, that law turns X38's five failing cluster cells into passes:
   - MID T3 Z +4.26 → −1.29;
   - the MID KT slope +3.07 → +0.85;
   - OUTER M3 +5.36 → +1.81.

   The only miss is a mild over-prediction in the innermost band (Z −2.4 / −2.1), and q_f − 0.05 keeps that same single
   miss. This is the first route-E model in the record that gets the heavy cluster cores without a cluster-tuned number.
2. **Dwarfs break.** With Σ falling as σ^0.8 toward dwarf dispersions (≈ 5–10 km/s), the dwarf cores become too shallow:
   the median dwarf needs 3–5× the cap.

   This is the old dwarf blank again: X24's ~4 km/s floor and DF1's Γ ≈ 0.88, now seen from the halo side. The galaxy–
   cluster law and the dwarfs want different things below σ ≈ 20 km/s.
3. **Physics reading (not derived).** q = (1+n)/2 ⇒ n ≈ 0.78 (canonical) / 0.50 (alt): a self-interaction cross-section
   per mass falling with velocity, σ/m ∝ v^(−0.5 to −0.8). That is the conventional direction for velocity-dependent
   self-interacting dark sectors.

   LN1's window premise ("galaxies flat within ×2") was the wrong assumption. SPARC itself prefers Σ rising with σ, so
   that window evaluation is superseded. T7 and T8 are unaffected: they are theorems, and only the premise values change.

**Status of the cold sector after OS1.** A self-coupled cold dark energy with a₀ setting the core surface density of a
typical galaxy, Σ ∝ σ^~0.8, and one constant calibrated on galaxies:
- passes SPARC (rms 0.06);
- passes nearly all cluster cells out of sample;
- fails the dwarfs.

The dwarfs need either a separate small-scale ingredient (the record's floor) or a law that flattens below about 20 km/s.
That flattening is a new shape, not yet motivated by anything here.
