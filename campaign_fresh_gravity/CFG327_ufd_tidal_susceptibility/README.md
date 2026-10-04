# CFG327: MW ultra-faint offsets vs tidal susceptibility (McGaugh & Wolf 2010-type test)

**Verdict: NOT SUPPORTED** (frozen criteria 219e0a0b9).
- **Data:** 31 resolved UFDs from the LVD.
- **Orbits:** integrated back 6 Gyr in the MW's own MOND field (6e10 M☉ baryons, exponential/ν_mono kernel).
- **Susceptibility metric:** r_half / r_t at the pericentre.

| footing | Spearman ρ(Δ, log A) | one-sided p | least-susceptible third | most-susceptible third |
|---|---|---|---|---|
| canonical | −0.166 | 0.81 | +0.363 ± 0.128 dex (2.8σ) | +0.374 |
| alt | −0.166 | 0.81 | +0.342 ± 0.129 dex (2.7σ) | +0.354 |

- **The test result:** the least tidally susceptible dwarfs sit as far above the law as the most susceptible ones. Tides do not explain the UFD offset.
- **Reported rows agree:** the present-distance metric gives ρ ≈ 0. Dropping LMC/SMC-hosted dwarfs gives ρ ≈ −0.04.
- **C1, reported:** the measured-only median offset is +0.354 (canonical), against AUDIT_UFD's Kaplan–Meier median of +0.3245, which includes the upper limits.

## Controls
- **C3 passes:** a circular orbit at 50 kpc keeps its pericentre to 1e-4.
- **MUTATE passes:** with the metric shuffled, T1 fails, as required.
- **C2 fails, and the failure is kept** (max |dE/E| 1.7e-2).
  - Post-hoc diagnostic (`cfg327_dt_diag.py`, `cfg327_dt_diag_POSTHOC.out`): the failure is a single orbit, Pisces II. It is unbound in this potential (|E|/|φ| = 1.67) and leaves the 3 Mpc potential grid, where the energy bookkeeping clamps.
  - Every other orbit conserves energy to ≤ 5e-6.
  - Halving dt moves every pericentre by ≤ 7e-6, so the pericentres and the verdict are unaffected.

## Run
```
python3 campaign_fresh_gravity/CFG327_ufd_tidal_susceptibility/cfg327_tidal.py
CFG327_MUTATE=1 python3 campaign_fresh_gravity/CFG327_ufd_tidal_susceptibility/cfg327_tidal.py
```
(~5 s each)
