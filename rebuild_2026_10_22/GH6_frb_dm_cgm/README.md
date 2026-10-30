# GH6_frb_dm_cgm

**Question.** tSZ (GH3–GH5) measures pressure and misses cool gas; route E needs mass. Can the localized FRBs on disk
measure the electron column around MW-mass centrals, and tell gas ending at R_vir from gas reaching 1.8 R_vir?
Criteria were frozen before any FRB was matched to a galaxy (545e09b5a4).

## Verdict: NON-DIAGNOSTIC

The power gate fails both tests, so the FRB dispersion measures were **never read** and nothing was measured. This says
nothing for or against the gas. It says these FRBs and this catalogue cannot answer the question.

| forecast (92 arcsec FRBs, 19 in the DESI footprint) | mean m(k = 1 / 1.8 / 3), pc cm⁻³ | crossings < 3 R_vir per FRB | S(k=1), gate ≥ 3 | S(1.8 − 1), gate ≥ 3 | S(3) |
|---|---|---|---|---|---|
| **PRIMARY:** centrals log M★ 10.6–11.0 | 0.0 / 2.0 / 4.2 | 0.21 | **0.00** | **0.18** | 0.26 |
| wide: log M★ 10–11.5, Zhang extrapolated | 1.5 / 5.7 / 13.0 | 1.16 | 0.14 | 0.29 | 0.67 |
| 114 FRBs (23 in footprint), primary lenses | 2.0 / 4.1 / 6.3 | 0.22 | 0.35 | 0.19 | 0.55 |
| 114 FRBs, wide lenses | 3.3 / 7.2 / 13.6 | 1.00 | 0.37 | 0.30 | 0.81 |

Median noise per FRB is about 129 pc cm⁻³ (the authors' cosmic scatter plus a fixed host term).

## What it shows

1. **The signal is far below the noise.** A typical sightline here gets a few pc cm⁻³ from MW-mass centrals, against about
   129 of scatter.
2. **No PRIMARY sightline passes within R_vir of a primary lens,** so S(k=1) is exactly 0.
3. **The footprint is not the main problem.** Only 19 of 92 FRBs pass the frozen 90 % coverage rule. Scaling the best case
   (wide lenses, gas to 3 R_vir) to all 92 gives S ≈ 1.5, still under 3.
4. **Rough sample size needed:** about 1,500–8,000 FRBs in the footprint for detection, and about 2,000–5,500 for extent.
   These scale S ∝ √N from a handful of crossings, so they are order-of-magnitude only; the 92-FRB primary detection case
   has no estimate at all, because S is zero.

**For the theory.** Route E's gas is still neither detected nor excluded by a mass-weighted probe. The KiDS lensing need
(GH2, k* ≈ 1.8) stays open. The remaining on-sky mass-weighted route is kSZ, which needs data not on disk. κ = ½ FITTED;
c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the
data favour the framework.

## Disclosures

- **K3, K4 and MUTATE vector changed from the frozen text.** They were frozen on the primary m(1), which turned out to be
  identically zero. They ran on the wide m(3) instead (recorded in `gh6_gate.json`).
- **Failed first runs.** The first run stopped on a formatting error, after printing only the footprint count, because N for
  G1 is undefined at S = 0. Its RSS was 12.5 GB, mostly mapped catalogue pages, above the frozen 3 GB. The script now caches
  the needed columns and restarts. The committed run peaked at 0.69 GB. K1 and K2 print twice in `gh6_gate.out` because of
  that restart.
- **The noise is fixed, not measured.** It includes the authors' host-term choice at the centre of their box. A plausibly
  smaller value would not lift S by the 10× or more needed.
- **Prior results.** The FRB z-scatter lane CFG632 and the FLIMFLAM lane CFG628 (also non-diagnostic) read DMs for other
  questions; neither is a sightline-by-lens match.

## Checks (all PASS)

- **K1:** β = 2/3 projection closed form (−6.5e-5).
- **K2:** area integral of the column gives 1.84 M★ (−1.6e-4).
- **K3:** Fisher S vs mock scatter, ratio 0.972.
- **K4:** injected A = 1 gives mean 0.991 (−0.28 se).
- **MUTATE:** S(10 m)/S(m) = 10.000000; rotated positions S 0.48 ± 0.16 vs true 0.67, ratio 0.71.

## Files

- `FROZEN_CRITERIA.md`, `gh6_gate.py`, `gh6_gate.out`, `gh6_gate.json`
- Column cache: `_external_data/gh6_work/gh6_bgs.npz` (not committed)

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh6_gate.py`
