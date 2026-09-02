# The framework-vs-ΛCDM test, run on the data in hand (2026-09-01)

Script: `a0z_lcdm_native_hypothesis_2026.py` (3 checks, 0 FAIL; output in `.out`). It loads the committed joint likelihood
`a0z_fork_likelihood_2026.py` (10 high-z constraints, exposure-weighted apparent-a₀ drift nuisance) and adds ΛCDM as a
**fourth zero-parameter hypothesis** instead of a nuisance. ΛCDM has no fundamental a₀: its RAR scale is emergent from
halo structure and rises with redshift (`real_research/crispy_2026/crispy_fabric_prediction_2026.py`):

    a_s(z)/a_s(0) = E(z)^{4/3} · [c²/f(c)](z) / [c²/f(c)](0),  f(c) = ln(1+c) − c/(1+c)

| law | z=1 | z=2 | z=2.5 | z=3.25 | meaning |
|---|---|---|---|---|---|
| M-FLAT (framework flat / standard MOND) | 1.000 | 1.000 | 1.000 | 1.000 | constant a₀ |
| M-DEC (framework, DESI-DR2 w₀wₐ) | 0.989 | 0.874 | 0.822 | 0.754 | a₀ ∝ √ρ_DE(z) |
| M-LCDM-DM14 (Dutton–Macciò 2014, M=10¹²) | 1.233 | 1.756 | 2.126 | 2.823 | structure-only rise |
| M-LCDM-D08 (Duffy 2008) | 1.427 | 2.284 | 2.802 | 3.667 | structure-only rise |
| M-LCDM-MAG (Magneticum (1+z)^0.92) | 1.892 | 2.748 | 3.166 | 3.785 | hydro apparent rise |

The contamination nuisance (beam smearing, pressure support, selection; exposure w_i per point) is kept **identically for
every model**. Those channels exist in a ΛCDM universe too, so keeping them for the ΛCDM laws is the conservative choice
against ΛCDM.

## Odds (log10 B, positive favours FLAT)

| drift ceiling | FLAT/DM14 | FLAT/D08 | FLAT/MAG | DEC/DM14 |
|---|---|---|---|---|
| face value (no drift) | −32.36 | −44.53 | −45.62 | −47.17 |
| Magneticum p<0.92 | −3.96 | −3.68 | −3.52 | −8.80 |
| MSA-3D measured p<1.22 | +0.19 | +0.48 | +0.64 | −1.59 |
| loose p<1.50 | +0.68 | +0.96 | +1.12 | +0.59 |

Worst case |log10 B| over the ladder = 0.19 (20:1 needs 1.30); the sign flips with the prior ceiling. **Undecided and
prior-dominated**, the same status the committed fork likelihood found among the framework's own laws.

Ciocan (MUSE-DARK III, a₁ = +1.59 ± 0.105, w = 1.00) carries every face-value verdict: its χ² is 229 under FLAT, 80 under
DM14, 17 under MAG. It is inconsistent with every law at face value and is absorbed only by the drift nuisance. With
Ciocan dropped, FLAT is mildly favoured at every ceiling (FLAT/DM14 +0.05 to +0.5; FLAT/MAG +0.5 to +1.2). Dropping the
two estimate-coded points ([9] McGaugh, [10] Milgrom) leaves the picture unchanged.

Per point at face value: [1] MSA-3D, [2] Ciocan favour the ΛCDM laws; [8] Big Wheel (z=3.25, +0.06 ± 0.22 dex, N=1),
[9] McGaugh+24, [10] Milgrom 2017 favour FLAT; the massive-disc BTFR points [4]–[6] are indifferent (σ ≥ 0.30 dex).

## The decisive measurement

The BTFR / deep-MOND zero-point of discs at z ≈ 2.5 where the lever L → 1 (g_bar ≲ a₀):

| z | FLAT | ΛCDM-native DM14 / D08 | σ for 20:1 (DM14) |
|---|---|---|---|
| 2.0 | 0.00 dex | +0.24 / +0.36 dex | 0.10 dex |
| 2.5 | 0.00 dex | +0.33 / +0.45 dex | 0.13 dex |
| 3.0 | 0.00 dex | +0.41 / +0.53 dex | 0.17 dex |

One clean deep-MOND point at z ≈ 2.5 with σ ≤ 0.13 dex decides FLAT vs ΛCDM-native at 20:1. That is a JWST/ALMA-scale
measurement of a handful of low-g_bar rotators (Big-Wheel-class objects, or the lensed low-mass MUSE-DARK class pushed to
z ≥ 2), not a survey. The existing clean points lean flat but are too coarse (±0.20–0.22 dex).

**Both ways.** A measured +0.3 dex rise on that arm kills the framework's flat law and standard MOND with it (and the
DEC law even harder). A measured constancy forces the ΛCDM halo dilution c_req/c_Nbody ≈ (H/H₀)^{−2/3} of
`crispy_fabric_prediction_2026.py` (0.61 at z=2, 0.40 at z=3), which N-body ΛCDM does not produce.

**Not claimed.** This does not show "the framework is right and ΛCDM is wrong" on present data; it shows the data cannot
yet tell them apart and names the measurement that will. a₀ ∝ √ρ_DE(z) (M-DEC) is the framework's distinctive prediction;
FLAT is shared with standard MOND. The framework-specific DEC-vs-FLAT separation at z=2.5 is only −0.09 dex and needs
σ ≈ 0.035 dex, a much harder measurement.
