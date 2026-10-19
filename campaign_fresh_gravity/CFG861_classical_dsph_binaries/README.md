# CFG861: do unresolved binaries make the classical dwarfs' excess?

**Label: PARTIAL (canonical, graded, by the frozen rule).** Binary cleaning moves the classical dwarfs very little
(mean δ −0.045 ± 0.030 dex). The class is PARTIAL, not BINARIES MINOR, because the five graded systems scatter widely
(s = 0.186), so m = +0.251 is not above 3s. Binaries do not remove the excess in Draco, Ursa Minor or Sextans.

- **Criteria:** `FROZEN_CRITERIA.md` (4bcf7ce28), committed alone before any script. Block CFG860–869.
- **Script:** `cfg861.py` → `cfg861.out`, `cfg861_results.json`. `CFG861_MUTATE=1` → `cfg861_MUTATE.out`, `cfg861_results_MUTATE.json`.
  One process, about 2 s, about 190 MB RSS, numpy/scipy only, nothing downloaded. The JSON is deterministic (two runs gave the same md5).
- **Reuse:** CFG51's `reduce_walker.py` is imported unchanged as a module, so its `main()` and file output never run. Its quality cut,
  membership v2, epoch pooling by Gaia id and `mle_sigma` are used as written. CFG852's `delta_ups2` is taken from its source with `ast`,
  as CFG860 did. The alt footing uses the same function with its module-level a0 swapped.
- **Settings:** κ = ½ FITTED; footings never pooled; Δ uses Υ_V = 2, Wolf at r_1/2 = 4/3 r_h, kernel ν_e; canonical a0 = 9.3603e-11
  (graded), alt 1.1312e-10 (reported).

## The question

CFG860 (NOT GAS) and CFG843 (SAME) leave two readings for the faint-dwarf excess (+0.3 to +0.5 dex in g at g_bar < 10⁻¹² m/s²).
It is either something real in every faint pressure-supported dwarf, or a measurement systematic they all share. Binary stars
inflate single-epoch dispersions. The ultra-faints were already checked (CFG29, 46, 51, 78, 93, 259): binaries trim their excess
but do not remove it. The classical dSphs were never cleaned. CFG51's reducer listed them but did not analyse them.

For each classical system, the test takes the members with ≥ 2 quality epochs (the set M). It compares the first-epoch dispersion
σ_single(M) with σ_clean(M), which drops stars whose epochs vary (χ² p < 0.01) and uses all-epoch means for the rest. The shift is
δ = 2 log10(σ_clean/σ_single), in dex of g. Both use the same stars and footprint, so δ isolates binaries. Δ_clean = Δ_LVD + δ.

## Result (canonical, graded)

The graded set is the informative classicals (|M| ≥ 30) at log g_bar < −11.9.

| system | \|M\| | δ | Δ_LVD | Δ_clean | log g_bar | σ_bin needed (km/s) |
|---|---|---|---|---|---|---|
| Crater II | 39 | +0.011 | −0.436 | −0.425 | −13.95 | 0 (below the law) |
| Sextans | 192 | −0.161 | +0.509 | +0.348 | −13.06 | 6.56 (above 4.5) |
| Ursa Minor | 135 | −0.015 | +0.573 | +0.558 | −12.43 | 7.58 (above 4.5) |
| Draco | 263 | −0.032 | +0.632 | +0.600 | −12.20 | 8.36 (above 4.5) |
| Carina | 396 | −0.028 | +0.199 | +0.171 | −12.19 | 4.00 (within 4.5) |

- **m = +0.251 ± 0.186** (mean Δ_clean, s = std(ddof 1)/√5). The mean Δ_LVD before cleaning is +0.295.
- **Mean δ = −0.045 ± 0.030 dex.**
- **CLASS: PARTIAL.** It is not BINARIES EXPLAIN, since m = +0.25 is above +0.10. It is not BINARIES MINOR either: |mean δ| < 0.05
  holds, but m = 1.35 s, short of 3 s. With ddof 0 (s = 0.166) the class is the same.
- σ_bin = σ_LVD √(1 − 10^(−Δ_LVD)) is the binary dispersion a system would need for binaries to make its whole excess. Draco, Ursa
  Minor and Sextans would need 6.6–8.4 km/s, above the ~4.5 km/s single-epoch bound (McConnachie & Côté 2010, as used in CFG29).
  Carina's smaller excess would need 4.0 km/s, within the bound. Crater II sits below the law.
- Post hoc (added after the graded run, labelled in the output, not graded): without Crater II, which is tidally disturbed and
  below the law, m = +0.419 ± 0.099 and mean δ = −0.059 ± 0.034. That is still PARTIAL, because Sextans' −0.16 takes |mean δ|
  past 0.05. The class does not hinge on Crater II.

**What this means for the record.** In the three classicals with the largest excess, the like-for-like cleaning removes 5%
(Draco), 3% (Ursa Minor) and 32% (Sextans) of Δ_LVD. They keep +0.35 to +0.60 dex over the bare law after cleaning. The
binaries those excesses would need are above the published single-epoch bound. Within what multi-epoch data can test, the
classical-dwarf excess is not a binary artefact. The rule still says PARTIAL, because Sextans moves by a measurable amount
and five systems are too few and too scattered for the stricter class.

## All classical systems (reported)

M is the set of members with ≥ 2 quality epochs. fM = |M|/N. "rm" is the number removed by the χ² test in M. σ is in km/s.

| system | \|M\|/N | fM | rm | σ_single(M) | σ_clean(M) | δ | Δ_LVD | Δ_clean | log g_bar | σ_bin needed | graded |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Antlia II | 24/68 | 0.35 | 2 | 5.35 | 5.52 | +0.026 | +0.069 | +0.095 | −14.03 | 2.30 | no (\|M\| < 30) |
| Crater II | 39/79 | 0.49 | 1 | 2.46 | 2.49 | +0.011 | −0.436 | −0.425 | −13.95 | 0 | yes |
| Sextans | 192/521 | 0.37 | 33 | 9.56 | 7.95 | −0.161 | +0.509 | +0.348 | −13.06 | 6.56 | yes |
| Canes Venatici I | 0/18 | 0 | – | – | – | – | +0.477 | – | −12.71 | 6.25 | no (no multi-epoch members) |
| Ursa Minor | 135/531 | 0.25 | 11 | 9.54 | 9.37 | −0.015 | +0.573 | +0.558 | −12.43 | 7.58 | yes |
| Draco | 263/505 | 0.52 | 15 | 9.41 | 9.07 | −0.032 | +0.632 | +0.600 | −12.20 | 8.36 | yes |
| Carina | 396/839 | 0.47 | 33 | 6.34 | 6.14 | −0.028 | +0.199 | +0.171 | −12.19 | 4.00 | yes |
| Leo II | 42/183 | 0.23 | 3 | 8.29 | 7.57 | −0.080 | +0.291 | +0.211 | −11.72 | 5.26 | no (g_bar) |
| Sculptor | 91/960 | 0.09 | 11 | 9.43 | 9.57 | +0.013 | +0.201 | +0.214 | −11.56 | 5.60 | no (g_bar) |
| Fornax | 157/861 | 0.18 | 8 | 13.33 | 13.24 | −0.006 | −0.088 | −0.094 | −11.50 | 0 | no (g_bar) |
| Leo I | 42/322 | 0.13 | 4 | 9.94 | 9.94 | −0.000 | −0.021 | −0.022 | −11.17 | 0 | no (g_bar) |

The output also lists CFG51's full-sample estimators for every system (single / all-epoch mean / clean / paper flag), the 1σ
errors on σ_single(M) and σ_clean(M), the median epoch baseline of M (64–1379 d) and the Υ_SFH Δ where CFG828 has a row.
Eight of the eleven systems have such a row; Sextans, Crater II and Antlia II do not.

## Reported variants (not graded)

| variant | N | m ± s | mean δ ± se | class |
|---|---|---|---|---|
| alt footing (a0 1.1312e-10) | 5 | +0.210 ± 0.186 | −0.045 ± 0.030 | PARTIAL |
| \|M\| ≥ 15 (adds Antlia II) | 6 | +0.225 ± 0.154 | −0.033 ± 0.027 | PARTIAL |
| alt footing, \|M\| ≥ 15 | 6 | +0.184 ± 0.154 | −0.033 ± 0.027 | PARTIAL |
| CFG51 paper-flag cleaning (f_Vlosvar) | 5 | +0.256 ± 0.189 | −0.039 ± 0.026 | PARTIAL |
| Υ_SFH (CFG828 rows and lgbar), canonical | 3 | +0.508 ± 0.094 | −0.025 ± 0.005 | NOT DIAGNOSTIC (N < 4) |
| Υ_SFH, alt | 3 | +0.468 ± 0.094 | −0.025 ± 0.005 | NOT DIAGNOSTIC (N < 4) |

Every variant with N ≥ 4 is PARTIAL. The paper's own variability flag gives nearly the same shifts (Sextans −0.139, Draco −0.041).

## Controls

- **K1 PASS.** The imported reducer reproduces CFG51's committed `walker_reduced_dispersions.tsv` for Boötes I (single 4.822, clean
  3.911) and Tucana II (single 7.477, clean 4.064). The all-epoch and paper-flag values and the counts N, n_multi and n_removed also match.
  The class, row and star counts for all 38 targets match CFG51's `run.log`. **Deviation, decided before the graded numbers:** the
  committed tsv is written with `'%.4g'`, so the frozen 1e-6 km/s tolerance cannot be checked against it. K1 therefore requires
  identical 4-significant-figure strings, which is agreement within 5e-4 km/s here. The unrounded values are in the JSON.
- **K2 PASS.** Draco's Δ_LVD is +0.632219040953, equal to CFG860's value (difference 0). The alt footing value also matches
  (+0.592688153471).
- **MUTATE bites (2/2).** Seed 861. In each graded system a random |M|//2 of the stars in M had an independent N(0, 10 km/s) offset
  added to every epoch. (a) The χ² test removed 413 of 511 injected stars, 0.808, against a requirement of ≥ 0.70. Among injected
  stars not already flagged it removed 375 of 470, 0.798. (b) Mean δ = −0.356, against a requirement of ≤ −0.10. Per system it was
  Carina −0.271, Crater II −0.769, Draco −0.181, Sextans −0.448 and Ursa Minor −0.108. White 10 km/s jitter is easier to catch than
  real binary orbits, so this shows the cleaning works at this cadence, not that it catches all binaries.

## Combined picture with the ultra-faints (quoted, not re-run)

- **CFG51 (LEDGER):** multi-epoch cleaning lowered the two informative ultra-faints' offsets without removing them. Boötes I went
  from +0.310 to +0.219 ± 0.089 and Tucana II from +0.730 to +0.465 ± 0.128. These offsets are log10(σ_obs/σ_law) with kernel
  ν_mono, so they are dex in σ. In g they double (the full-sample cleaning shifts are about −0.18 and −0.53 dex in g, not like-for-like on M).
- **CFG93 (LEDGER):** Tucana II's own testable multi-epoch stars alone give +0.22 ± 0.14 (1.55σ). At the real cadence the flagging
  catches only 9–13% of injected realistic binaries.
- **CFG29 (LEDGER):** the ultra-faint failure survives a binary audit at 3.5–3.8σ, using the same ~4.5 km/s single-epoch bound.
- **This lane:** for the classicals the like-for-like shift is small (mean −0.045 dex in g; largest Sextans −0.16). The three
  largest classical excesses stay +0.35 to +0.60 dex, and their σ_bin would exceed the bound.

Together, binaries trim the faint-dwarf excess more in the low-σ ultra-faints than in the classicals. Where multi-epoch data can
test it, they remove it in neither. This fits CFG860/CFG843: the excess is carried by faint pressure-supported dwarfs, host or no
host, gas or no gas. Binaries are not the shared systematic that would erase it. Other shared systematics (Υ, membership, the
small-sample Wolf estimator) are not tested here. Under the bare law the excess stands. In the framework this means bound cold
energy mass inside r_1/2, which no supply channel examined on the record provides for satellites (CFG842).

## Declared limitations

- **δ is a lower bound on the binary effect for M.** Binaries with periods much longer than the baselines, or with tiny amplitudes,
  escape the χ² test. The median baseline of M is 64–1379 d across the systems (278–1044 d in the graded five), and the median number of epochs is 2 (3 for Draco). CFG93 found that
  realistic binaries are caught far less often than the MUTATE jitter.
- **M is a subset.** It holds 9–52% of the members, and single-epoch stars are not used in δ. δ is applied as a relative shift to
  Δ_LVD, which uses the LVD literature σ, not the Walker+2023 σ.
- **No epoch zero-point offset is modelled** (CFG51's choice). Sextans pools three instrument files (Hectochelle, M2FS HiRes,
  M2FS MedRes). Any inter-instrument offset would show up as χ² variability and enlarge its |δ|.
- **Tidal systems.** Crater II and Antlia II are tidally disturbed. Tides are already on the record (CFG838/839: no signal) and
  are not re-tested. Canes Venatici I has no multi-epoch members. Antlia II has |M| = 24, below 30.
- **Small sample.** Five graded systems. The Υ_SFH variant has only three rows and is NOT DIAGNOSTIC.
- **Choices fixed before the graded numbers (in the script docstring):**
  - s uses ddof 1 (ddof 0 gives the same class).
  - The paper-flag variant is CFG51's own keep rule (fvar == 0) applied inside M. No member of M had a blank flag.
  - The Υ_SFH variant cuts on CFG828's lgbar.
  - MUTATE holds M fixed and does not re-run membership, so the test is the χ² cleaning alone.

κ = ½ fitted; cold energy mass required; not theory closed.
