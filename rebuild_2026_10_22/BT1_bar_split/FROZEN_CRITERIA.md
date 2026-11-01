# BT1_bar_split: FROZEN CRITERIA, committed alone before any script or per-galaxy Υ

**Question.** Under EM1 + Blumenthal the spirals at 150–250 km/s sit at Υ 0.30–0.36. Is that miss carried by barred galaxies, where a bar could have torqued the inner halo? No model of a bar enters.

**Data, no download.** Bar family: Buta et al. 2015 S4G mean family ⟨F⟩ (`real_research/data/s4g_morph_buta2015_cvrhs.tsv`), 0 = SA, 0.5 = SAB, 1 = SB. SPARC has no bar field. Names matched after removing spaces and leading zeros.

**Υ per galaxy.** `_gals_U` on RM1's path, NR2 MEDIAN, EM1, δ 0, Blumenthal, background A; B must agree or the split is reported on both. The off row is reported as a control.

**Sample.** SPARC Q ≤ 2, i ≥ 30°, 150 ≤ V_flat < 250 km/s.
**Seen before freezing, no Υ.** 43 galaxies by the mrt: F < 0.5 n 10, F = 0.5 n 6, F > 0.5 n 7, no class 20. S4G's coverage selects, so the 20 unclassified are reported, not imputed.

**Split.** Unbarred F < 0.5; barred F ≥ 0.5. The stricter split, F > 0.5 against F < 0.5, is reported. Statistic: median Υ per side, and a two-sided permutation p on the difference, 20 000 draws, seed 20261101.

**Labels.**
| Label | Condition |
|---|---|
| **BAR-CARRIED MISS** | unbarred median ≥ 0.50, barred median < 0.40, p < 0.05 |
| **UNBARRED SHARE THE MISS** | unbarred median < 0.40. Bars aren't what makes the miss, on this classification |
| **NOT SEPARATED** | anything else |

**Disclosed.** The Υ grid has a floor at 0.30, so medians there are censored; the count at the floor is reported per side. Low n: the label can't exclude a small bar effect. V_obs enters Υ, as it must, and doesn't enter F. Bars today aren't bars over the disc's history. Reported, not graded: the same split at 100–150 km/s, and at 250–400 only if n allows.

**Expectation on record.** UNBARRED SHARE THE MISS, held loosely: NR3's bins are tight at the floor.

**Checks.** K1 the sample's Q and i cut with `_TB` gives median Υ in 150–200 and 200–250 equal to NR3 MEDIAN's bins, within 10⁻⁶. K2 the galaxy count in the band is 43 and the classified count 23. K3 F is read as a number in [0, 1]. Rerun byte-identical. MUTATE: F shuffled with a fixed seed, K2's classification sum check against the unshuffled per-galaxy F fails, exit 1, separate outputs.

One thread, nice 15. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
