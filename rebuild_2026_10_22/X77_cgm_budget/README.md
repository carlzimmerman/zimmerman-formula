# X77_cgm_budget

> **Lane-ID collision.** A peer session's `X77_direct_core_surface_density` (21f010353f, 21:05) took the X77 id first.
> This lane (d40d851943, 21:26) is a different lane. Cite it by its full name, `X77_cgm_budget`.

**Question (the owner's pick, 10-29).** X76 showed that the clusters' fair-share rule fits galaxy outskirts only if a
galaxy's baryon budget is ×10^0.85 (lensing) to ×10^1.25 (satellites) larger than its observed stars, cold gas and
0.5 M★ hot gas. Can an undetected hot CGM supply that?
- **Rule:** the CGM is counted out to the self-consistent turnaround radius, as the clusters count their measured gas.
- **Measured input:** Zhang et al. 2024 (eRASS:4 stacks of SDSS centrals), verified from the paper's TeX source.
  - MW-mass bin: f_b,hot+star(<R_vir) = 0.12 ± 0.06, so M_hot(<196 kpc) ≈ 1.0×10¹¹ M☉.
  - β = 0.43 (+0.10 / −0.06).
- Criteria were frozen first (d40d851943).

## Verdict

**Frozen rule:** CGM BUDGET SUPPLIES THE MASS.

**What it actually shows:** the budget is set by extrapolation, not by data. The measurement neither supplies nor
excludes the mass.

| MW-mass bin (log M★ 10.5–11.0) | central | generous (f_b + 1σ, β − 1σ) | tight (f_b − 1σ, β + 1σ) |
|---|---|---|---|
| M_hot inside R_vir (measured) | 1.0×10¹¹ | 1.8×10¹¹ | 2.3×10¹⁰ |
| uncut profile: self-consistent r_ta | 4.5 Mpc (23 R_vir) | 12.5 Mpc (64 R_vir) | 1.1 Mpc (5.7 R_vir) |
| uncut profile: M_hot(<r_ta) | 2.2×10¹³ | 4.6×10¹⁴ | 2.8×10¹¹ |
| **m_CGM** (need +0.85 lensing, +1.25 satellites) | **+2.37** | +3.70 | +0.57 |

- **The "supply" is a runaway.** A ρ ∝ r^−1.3 profile extrapolated without a cut keeps adding mass as r_ta grows, so
  the fixed point lands at 20–60 R_vir. Over 99 % of the "reservoir" lies beyond the measured R_vir, and it overshoots
  the need by more than a dex. Too much mass fails the satellites just as too little does.
- **The criteria guarded only the low side.** That gap is mine, and is disclosed here.
- **At the tight edge it falls short** (+0.57).

## Where the data would have to stop (AMENDMENT A1, post-result, reported only)

Cutting the measured profile at k R_vir, with no hot gas beyond:

| | k for lensing (+0.85) | k for satellites (+1.25) |
|---|---|---|
| MW-mass, central | **2.8 R_vir** (≈ 550 kpc) | **5.0 R_vir** (≈ 970 kpc) |
| MW-mass, generous | 1.9 | 3.2 |
| MW-mass, tight | never (m ≤ +0.57 at 8 R_vir) | never |
| M31-mass, central | 3.0 | 5.1 |

- **Lensing needs the measured hot-CGM profile to continue to about 3 R_vir.** That is where Zhang et al. themselves
  place baryon closure (R_c ≈ 3 R_vir). It is not a coincidence:
  - the fair share uses the cosmic baryon ratio;
  - a galaxy that holds its cosmic baryons within ~3 R_vir therefore gets about the halo mass lensing measures.
- **Satellites need the profile out to about 5 R_vir (~1 Mpc).** The extra 0.4 dex over lensing is X75's
  satellites-vs-lensing difference (environment, centrals vs isolated).
- **The cut is a free parameter.** Nothing measured past R_vir fixes it, and Zhang note that the profile beyond R_vir
  is unconstrained.

## Reading

- **The CGM route is not excluded. It is untested by present data.**
  - Route E's galaxy halos can match lensing if galaxies keep roughly their cosmic baryon share as hot gas out to
    ~3 R_vir, and satellites if out to ~5 R_vir.
  - The measured part, within R_vir, is 1–10 % of what is needed.
- **The decisive observation is the hot-gas profile from 1 to 5 R_vir around MW-mass centrals.** Deeper eROSITA/DESI
  stacks (Zhang et al.'s own stated next step) or tSZ cross-correlations at 0.2–1 Mpc can measure it.
  - A cutoff near R_vir would exclude this route.
  - Continuation to ~3–5 R_vir would keep it.
- **Not regraded.** X76/X75 were not rerun with the gas gravitating. Only the budget is tested here.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled (canonical budget; X76's alt needs are within 0.05); cold dark
  energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the
  framework.

## Checks

- **K1:** the β-mass quadrature matches the β = 2/3 closed form exactly.
- **K2:** the r_ta fixed point holds to 2e-16.
- **K3:** with M_hot ≡ 0.5 M★, m = 0 exactly.
- **MUTATE:** β = 0.25 raises m (+2.37 → +5.30).
- **Disclosed:** the first A1 printout had the two "k needed" labels swapped. The values were right; the labels are
  fixed.

## Files and data

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`
- `x77_cgm.py` with `x77_cgm.out` and `x77_cgm_results.json`
- `x77_cut_profile.py` with `x77_cut_profile.out` and `_results.json`
- Input: `_external_data/arxiv_src/2401.17308/` (FETCH_LOG.md, sha256 8e0a0305…).

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x77_cgm.py && python3 x77_cut_profile.py
