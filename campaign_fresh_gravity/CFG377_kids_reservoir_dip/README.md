# CFG377: KiDS-1000 isolated lenses vs CFG372's reservoir dip. CONSISTENT, but uninformative (λ ≈ 3e-4); the dip is out of reach

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (d03819f06). Script: `cfg377_run.py` (about 30 s, one niced process). Outputs: `cfg377_run.out`, `cfg377_results.json`; MUTATE: `cfg377_run_MUTATE.out`, `cfg377_results_MUTATE.json`. Both runs exit 0 with every check passing.

## Verdict (primary data, per footing, never pooled)

| footing | χ² BARE / 15 | χ² RES / 15 | Δχ² (RES − BARE) | λ | power at 2σ / 3σ | verdict |
|---|---|---|---|---|---|---|
| canonical 9.3603e-11 | 325.49 | 325.82 | **+0.33** | 3e-4 | 0.046 / 0.003 | **CONSISTENT (uninformative: λ < 1)** |
| alt 1.1312e-10 | 261.19 | 261.56 | **+0.37** | 4e-4 | 0.046 / 0.003 | **CONSISTENT (uninformative: λ < 1)** |

A power of 0.046 equals the false-alarm rate, so the test has no power. KiDS-1000 can neither see nor exclude the reservoir dip.

## Where the data reach and how big the dip is

- **Radial reach.** The 15 g_bar bins have pair-weighted mean radii from 0.046 to 2.17 Mpc (2.33 Mpc for the f30 subset); 4 bins lie beyond 1 Mpc. Brouwer+2021 Fig-3 reaches 2.60 Mpc. No data bin sits at 3 Mpc, where CFG372 quotes −6.5%.
- **The lensing dip is much smaller than the enclosed-mass dip.** Tangential shear measures ΔΣ = (mean Σ inside R) − Σ(R). A deficit spread over a 4.45 Mpc Gaussian is almost a uniform sheet near the lens, and a uniform sheet gives zero ΔΣ. So CFG372's −0.3% (1 Mpc) and −6.5% (3 Mpc) in enclosed mass become, in ΔΣ at z = 0.2, about −0.03% at 1 Mpc, −0.43% at 2 Mpc and −2.0% at 3 Mpc (M_b = 1e10.5–1e11, both footings).
- **In the stack.** The outermost bin's dip is −0.72% of the BARE model (−0.0015 Msun/pc²), about 1% of its jackknife error (0.14 Msun/pc²).

## Secondary results (reported; S1 and the guard enter the verdict only when it is decisive)

| | canonical Δχ² (λ) | alt Δχ² (λ) |
|---|---|---|
| S1: strict isolation f30 (57,265 lenses) | +0.009 (1e-4) | +0.008 (1e-4) |
| primary, two-halo nuisance profiled | +0.005 | +0.033 |
| S2: Brouwer+2021 Fig-3, 4 mass bins, B21 covariance, /60 | +0.33 (5e-4) | +0.36 (7e-4) |

## Required precision (forecast)

- **With KiDS-1000's bins.** An expected 2σ detection needs errors × 0.0080 (canonical) / × 0.0094 (alt). That is about 1.6e4 / 1.1e4 times KiDS-1000's lens–source pair count, if shape noise dominates. A 3σ detection needs 3.5e4 / 2.6e4 times.
- **At a single radius.** At R = 3 Mpc, a 2σ (3σ) detection needs ΔΣ measured to about 1.0% (0.7%) in fractional terms.
- **The two-halo term must be modelled to the same level.** Neither model has a two-halo or environment term. The data sit far above the truncated bare law at large radius: 0.98 against 0.21 Msun/pc² at 2.2 Mpc. That is the source of the large absolute χ² (325 / 261 over 15 bins), which falls to 9.7 / 11.9 once a free R^−0.8 two-halo amplitude is profiled. The dip is about 500 times smaller than this excess. A detection needs a two-halo model good to a few tenths of a percent of the signal at 2–3 Mpc.
- **Correction to CFG372's wording.** CFG372 called the dip a "sharp prediction for KiDS-Legacy / Euclid stacks". That is not supported. In ΔΣ the dip is 2% at 3 Mpc and below 0.5% inside 2 Mpc, and it is degenerate with the two-halo term. In practice it is not a near-term test.

## Controls (all pass)

- **C1:** the per-lens sums reproduce the June per-patch file (6e-13).
- **C2:** the closed-form Gaussian ΔΣ matches the shell projector (1e-4); point mass exact.
- **C3:** CFG372's own recipe reproduces its printed −0.28/−6.62, −0.27/−6.45, −0.28/−6.68, −0.27/−6.54% exactly. This lane's recipe (ν_mono, CFG100 r_ta at z = 0.2) gives −0.26 to −0.28% at 1 Mpc and −6.3 to −6.6% at 3 Mpc.
- **C4:** grouped and exact per-lens dips agree to 8e-4.
- **MUTATE (M_ex × 100):**
  - χ²_RES moves by 35.4 (canonical) and 40.3 (alt), above the required 4. PASS.
  - The verdict flips to "DISFAVOURED (NOT ROBUST: 2-halo / isolation)". f30 gives only +1.8 / +2.0, and the nuisance-profiled Δχ² turns to −4.8 / −4.5 on f30.
  - So the two-halo guard works as declared: a 100× dip is disfavoured only through the unmodelled two-halo excess.

## Caveats

- **Data.** The KiDS sums are the on-disk staged product `cfg110_perlens.npz` (it shares CFG100's independence limit). Brouwer+2021 restrict their isolated-lens RAR to R ≲ 0.3 Mpc/h. Every bin beyond that, which includes all the dip bins, carries two-halo and environment signal.
- **Models.**
  - The bare law is truncated at 0.4 r_ta and frozen beyond. Nothing models the matter beyond r_ta.
  - The reservoir is CFG366/372 bookkeeping (a Gaussian deficit), not a derived law. The cold fluid is still required (no dark-matter particle). κ = ½ is fitted.
- **Statistics.**
  - The jackknife has 50 patches and a Hartlap factor of 0.67.
  - S2 uses B21's covariance, taken in h70 units as given, with equal lens weights.
  - The large negative A-hat (−644 ± 62 in dip units) reflects the two-halo excess, not the dip.
- **numpy warnings.** numpy prints spurious matmul RuntimeWarnings (the Accelerate quirk CFG77/CFG100 saw). C2 and C4 confirm the numbers are unaffected.
- **What this does not say.** Nothing here says the data favour the framework. "Consistent" means only that the data cannot see the dip.
