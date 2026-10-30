# X76_galaxy_fair_share_halos

> **Superseded in part by GH1_matched_lensing_satellites (10-29).** KiDS lensing around these *same* G09 hosts wants Δ = +0.17 [+0.05, +0.28], not +0.78. The satellite number is a method systematic of this measurement (likely pair weighting toward rich hosts, interlopers, velocity bias), not a halo-mass need. Satellite-based needs/fails in this lane are overstated; the lensing lines stand.

**Question.** X74_smooth_core_lensing and X75 showed route E's galaxy halos are too light at 50–300 kpc when M200 comes
from EM1's SPARC relation. Does the clusters' own native rule fix that?

**The rule:** M_fair = R_nat · M_b,tot (R_nat = 5.27), placed inside the self-consistent turnaround radius, with the
smooth core and native normalisation.
- It is graded on the same KiDS lensing (X53 harness) and GAMA satellite (X75 frozen measurement) data. Nothing is
  fitted.
- Criteria were frozen first (5775b7d6b3), including the expectation that it would do *worse* than SPARC.

## Verdict: FAIR SHARE FALLS SHORT, both footings, as pre-registered

| | canonical | alt |
|---|---|---|
| lensing Δχ²(H2H − L2H), all radii: fair share / SPARC halos | **+750.3** / +423.7 | **+772.5** / +458.4 |
| satellites χ² (4 bins) at the observed baryon budget | **370.9** | 369.2 |
| predicted σ_sat at the observed budget, km/s (measured 72 / 114 / 151 / 188) | 28 / 42 / 53 / 63 | 28 / 42 / 53 / 63 |
| **budget multiplier needed, satellites** | **10^+1.24 (×17)** [+1.20, +1.27] | 10^+1.23 |
| **budget multiplier needed, lensing** (A1 profile, all radii / R ≤ 0.31 Mpc) | 10^+0.90 / 10^+0.75 | 10^+0.85 / 10^+0.70 |

- Every X75 systematic (β, γ, aperture, host weighting, Burkert, untruncated) gives +1.15 to +1.27 for the satellites.
- **The fair-share rule supplies less mass than SPARC, not more.** Galaxy halo masses come out 0.2–0.3 dex lighter
  than EM1's M200 (bin means 11.03 / 11.46 / 11.67 / 11.85), spread to r_ta ≈ 0.7 Mpc.
- **For the rule to work, a galaxy's baryon budget would have to be ~7–17× its observed stars + cold gas + hot CGM
  (0.5 M★).** Only an undetected baryon reservoir that size, counted into the budget, could do it. This lane does not
  test that. It is the size of the classic galaxy "missing baryons", now as a route E requirement.

## Reading

- **The clusters' rule does not carry down to galaxies on the observed budget.** Clusters pass because their gas is
  measured out to r_ta (GS1, X73). Galaxies have no such measured budget.
- **Route E now has no galaxy halo-mass rule that matches the outer data.**
  - SPARC's relation is 0.3–0.8 dex light (X74_smooth_core_lensing, X75).
  - The native fair share is 0.7–1.2 dex light (here).
  - The outer probes need about 10^12.6–10^12.9 at log M★ 10.9, i.e. a total-to-observed-baryon ratio near 50–100.
- **The isolated law, with no parameter,** has satellite χ² 29–39 against 369–371 here, and wins lensing (class LAW)
  throughout. That is not a pass, and nothing here says the data favour the framework.
- The open question for route E is where the galaxy outskirts' mass comes from. Each option is a new assumption, to be
  stated before it is tested:
  - a large undetected CGM counted into the budget;
  - a mass rule from collapse rather than from baryons;
  - conceding that galaxies need the law's phantom at 50–300 kpc.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
  not theory closed.

## Checks (all PASS)

- **K1:** with the fair switch off, the script reproduces X74_smooth_core_lensing's χ² exactly (max |d| = 0).
- **K2:** r_ta matches X30's r_ta_com at native parameters to 2e-15.
  - Disclosed: the first build used the rounded ρ_crit constant 2.775e11 and missed the frozen 1e-12 (3.4e-5).
  - It now uses X30's SI constants, and every run was redone. The graded numbers are unchanged at the printed
    precision.
- **K3:** the solved halo mass to r_ta equals M_fair to 2e-15 (test lens at log M★ 10.7: M_fair 4.45e11, r_ta 710 kpc).
- **MUTATE:** m = +1 raises ΔΣ near 100 kpc by ×3.2–4.7 in every bin, and raises σ_sat.
- `x76_satellites.py` exits 1 by construction. X75's pass count is taken before X76's K2 and K3 are appended, and all
  five checks pass. `x76_summary.py` applies the frozen rule and exits 0.
- One thread, peak RSS 0.50 GB.

## Files

- `FROZEN_CRITERIA.md`
- `x76_patch.py`: the shared smooth + fair-share patch
- `x76_lensing.py`: X53 harness; `X76_FAIR=0` gives K1
- `x76_satellites.py`: X75 harness
- `x76_lens_profile.py`: X53 A1 multiplier profile and MUTATE
- `x76_summary.py`: the frozen verdict
- outputs `*.out` and `*_results.json`

Run:

    X76_FAIR=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x76_lensing.py    # and X76_FAIR=0
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x76_satellites.py
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x76_lens_profile.py
    python3 -I x76_summary.py
