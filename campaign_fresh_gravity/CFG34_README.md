# CFG34 — the a₀ ladder under candidate B, and the X-ray groups under B's max rule

Script: `CFG34_groups_and_the_ladder_under_b.py`, under a second.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every hydrostatic mass is tripled, and the headline H1 fails (7.5 / 7.3σ, rc = 1).
- The main run exits 1: H2 (inside R2500) failed at 2.6σ. That is reported as run.

κ = ½ is fitted. Both footings are used.

## Question

The failures summary carried the a₀ ladder as liability B3. h20 asked every system class for its "implied a₀" on the phantom-only reading. The cluster rung came out at 1.81e-10, 6.3σ from the deep tail's 1.14e-10, and h20 concluded that the excess is missing *mass*, not a wrong constant.

Candidate B adds that mass. T5 sets the dark mass in a bound region to max(phantom, (Ω_c/Ω_b) M_b), and CFG4 reproduced X-COP's clusters with it (0.946 ± 0.080). But the rule had only been checked where baryons are nearly cosmic.

**The groups test it.** At 1–3 keV the baryon fraction inside R500 is about 0.10 (Lovisari+2015, 20 groups), against a cosmic 0.157. B's rule as written takes the cosmic share of the baryons present today.

## Method (declared before the first run)

- **Data:** h7's data and stellar-mass import, exec'd read-only (Lovisari+2015 hydrostatic and gas masses at R500 and R2500; stars from the Kravtsov+2018 SHMR, ×/1.5 bracket).
- **B's mass at each radius:** M_B = M_b + max(M_ph, 5.364 M_b), with M_ph = (ν_mono(g_N/a₀) − 1) M_b in the monopole reading, as CFG4.
- **Statistic:** the median over groups of log(M_HSE/M_B).
- **Error:** the group-to-group error, plus a floor for the stellar bracket and a 20% hydrostatic bias (0.079 dex). The bias is carried symmetrically, although hydrostatic masses usually run *low*, which would make the shortfall larger.

## Results

**Controls.**
- C1: h7's committed η at R500 is reproduced (1.800–2.108 canonical; 1.537–1.809 alt).
- C2: CFG4's X-COP identity ratios are recomputed exactly (max |d| 2e-16; median 0.9457). The cosmic share wins in 12 of 12 clusters.

| | canonical | alt | verdict |
|---|---|---|---|
| H1 (headline): groups at R500 | M_HSE/M_B = **1.41 → 1.80σ** | 1.33 → 1.49σ | PASS |
| H2: groups at R2500 | **1.88 → 2.57σ** | 1.88 → 2.63σ | **FAIL** |
| H3: the shortfall tracks the baryon fraction (groups + X-COP) | ρ = **−0.958**, p = 7e-18 over 32 systems | | PASS |

**What the numbers mean.**
- **At R500 the phantom wins the max in 18 of 20 groups** (canonical), so B equals the law there (the phantom-only law gives 1.45).
- **Inside R2500 the cosmic share wins but is short**, because the groups have lost baryons.
- **The error is mostly the allowance.** The group-to-group error is only 0.014 dex, so the R500 shortfall of 0.15 dex is carried by the hydrostatic allowance. If hydrostatic masses run low as usual, the shortfall grows.
- **R1:** for the rule to hold at R500, the groups would need a baryon fraction of 0.141 (observed 0.099; cosmic 0.157).

## The ladder under candidate B

Every rung is re-scored with B's own rule.

| rung | mass | residual under B | significance (canonical / alt) |
|---|---|---|---|
| MW ultra-faint dwarfs (CFG28) | ~1e3–1e5 | +0.325 dex in σ | **3.8 / 3.5** |
| MW classical + M31 dwarfs, infall gas (CFG18) | ~1e6–1e8 | +0.025 / +0.078 dex in σ | 0.4 / 1.6 |
| Coma UDGs (CFG31) | ~1e8 | +0.234 dex in g | 1.3 / 1.1 |
| SPARC rotation curves (CFG4) | 1e8–1e11 | the law's fit, rms 0.100 dex | fit |
| binary galaxies (CFG30) | ~1e11 | A = 1.12 with timing orbits (1.89 circular) | orbit-degenerate |
| X-ray ellipticals (CFG32) | ~3e11 | +0.280 dex in g | 1.7 / 1.6 |
| SLACS lensing vs ATLAS3D dynamics (CFG33) | ~2e11 | +0.159 dex in M_* | 1.6 / 1.5 (with its floor) |
| X-ray groups at R500 (this lane) | 2e13–1.4e14 | +0.150 dex in mass | 1.8 / 1.5 (with the allowance); R2500 2.6 |
| X-COP clusters (CFG4) | 3e14–9e14 | +0.024 dex in mass | 0.7 |

## Standing

**The a₀ ladder's "6.3σ" does not apply to candidate B.** B does not ask a₀ to supply cluster mass. Its cold component does, and the clusters close (0.7σ). Under B the ladder has one clean standing failure: the ultra-faint dwarfs at 3.5–3.8σ.

**But the groups expose where B's cluster rule is weak.** Its "cosmic share" is tied to the baryons a system has *today*:
- Groups have lost baryons (f_b ≈ 0.10 at R500).
- They come up 1.3–1.4× short at R500 (1.5–1.8σ, with a generous hydrostatic allowance) and 1.9× short inside R2500 (2.6σ).
- Across groups and clusters, the shortfall tracks the baryon fraction almost perfectly (ρ = −0.96).
- The X-ray ellipticals (CFG32) show the same thing.

**This is a design constraint, not a verdict.** A cold component should not follow baryons that feedback removes. If B tied the cosmic share to the baryons a system *collapsed with*, the groups and possibly the ellipticals would move toward closure. That is a change to T5, to be derived rather than fitted, and it is not done here.

Nothing here says the theory is closed.
