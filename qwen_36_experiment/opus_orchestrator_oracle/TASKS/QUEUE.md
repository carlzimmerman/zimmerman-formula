# QUEUE — work top-down. `CLOSED` is a success.

**37 tasks.** `M` modified-inertia physics · `D` data · `E` engineering · `W` unrelated.
**Always `import` from `../TOOLS/mi_constants.py`** — never retype a constant. Run
`python3 ../TOOLS/mi_constants.py` first; it must print 15/15.
Before committing: `python3 ../TOOLS/run_regression.py --quick`.

Status: `OPEN` `IN PROGRESS` `CLOSED` `CONFIRMED` `PARKED` `NEEDS_CARL`

## M — modified inertia (ranked; all are open items the 2026-08-07 sweep did NOT cover)

| # | task | file | cost | status |
|---|---|---|---|---|
| M01 | The α ≥ 1.260 kernel the joint DEMANDS — identify it, price it everywhere | `M01_alpha_1260_kernel.md` | S | OPEN |
| M02 | Theorem 4's escape kernel: μ≤1 saturated to 6.75e-05, what shape is it | `M02_theorem4_escape_kernel.md` | S | OPEN |
| M03 | a₀(z): two curves, no knobs, vs MUSE + MSA-3D | `M03_a0_of_z_two_curves.md` | S | OPEN |
| M04 | Ephemeris de/dt — the eccentricity drift nobody has computed | `M04_ephemeris_dedt.md` | M | OPEN |
| M05 | Non-quadratic-in-u — on the 2026-08-01 open list, never run | `M05_non_quadratic_in_u.md` | M | OPEN |
| M06 | ρ_m / T_μν coupling — also on that list, never run | `M06_Tmunu_coupling.md` | M | OPEN |
| M07 | All-orders rigidity of the (v/c)² suppression | `M07_all_orders_rigidity.md` | M | OPEN |
| M08 | The b-projector at third-derivative cost | `M08_b_projector.md` | M | OPEN |
| M09 | Finite-past initial-value problem (memory time 101 Gyr) | `M09_finite_past_ivp.md` | M | OPEN |
| M10 | The cluster 0.10 dex decider — what precision, which survey | `M10_cluster_decider.md` | S | OPEN |

## D — DATA. Nothing in this folder has ever loaded a dataset. Do D01 early; the rest build on it.

| # | task | file | cost | status |
|---|---|---|---|---|
| D01 | Actually load SPARC (reproduce 0.108 dex as the check) | `D01_sparc_loader.md` | M | OPEN |
| D02 | Confirm the RAR shape is a₀-blind on real data | `D02_rar_shape_blindness_on_data.md` | M | OPEN |
| D03 | Reproduce the fit-free a₀ ≤ 1.1606e-10 bound | `D03_fit_free_a0_bound.md` | S | OPEN |
| D04 | The cluster ladder on current weak-lensing data | `D04_cluster_ladder_on_data.md` | M | OPEN |

## E — ENGINEERING. Cheap, and each one prevents a whole class of error.

| # | task | file | cost | status |
|---|---|---|---|---|
| E01 | Fix the OOM (dense N×N → exact triangular solve) | `E01_fix_the_oom.md` | S | OPEN |
| E02 | Wire in the regression runner, record the baseline | `E02_regression_ci.md` | S | OPEN |
| E03 | A linter for the corpus's own rules | `E03_ledger_linter.md` | S | OPEN |

## W — unrelated and wacky. No framework rules. Do these when an M-task blocks, or for fun.

| # | task | file | cost | status |
|---|---|---|---|---|
| W01 | Benford forensics on this repo's own committed numbers | `W01_benford_forensics.md` | S | OPEN |
| W02 | Can you hear the shape of a drum? Build the isospectral pair | `W02_isospectral_drums.md` | M | OPEN |
| W03 | The figure-eight three-body orbit — integrate it, test stability | `W03_figure_eight_orbit.md` | M | OPEN |
| W04 | The hat monotile: substitution, inflation factor, tile counts | `W04_hat_monotile.md` | M | OPEN |
| W05 | Buffon's needle → π, and the bits-per-throw of Monte Carlo | `W05_buffon_bits.md` | S | OPEN |
| W06 | Collatz stopping times vs the log-normal prediction | `W06_collatz_stopping.md` | S | OPEN |
| W07 | Kolmogorov cost: how many bits IS the Standard Model? | `W07_bits_of_the_SM.md` | S | OPEN |
| W08 | Zipf's law on this repo's own commit messages | `W08_zipf_commits.md` | S | OPEN |
| W09 | Prime gaps: Cramér model vs the actual maximal gaps | `W09_prime_gaps.md` | S | OPEN |
| W10 | Arnold's cat map: exact recurrence times for integer matrices | `W10_arnold_cat.md` | S | OPEN |
| W11 | Ramanujan/Chudnovsky/BBP — the cost of a digit of π | `W11_ramanujan_pi.md` | S | OPEN |
| W12 | Langton's ant builds a highway at step ~10,000 | `W12_langtons_ant.md` | S | OPEN |
| W13 | Penney's game: non-transitive coin sequences | `W13_penney_game.md` | S | OPEN |
| W14 | The Kelly criterion, and why 2× Kelly grows nothing | `W14_kelly_criterion.md` | S | OPEN |
| W15 | The 15 convex pentagon tilings (list closed in 2017) | `W15_pentagon_tiling.md` | M | OPEN |
| W16 | Shannon's entropy of English, measured three ways | `W16_shannon_english.md` | S | OPEN |
| W17 | Six compactness metrics that disagree with each other | `W17_gerrymander_metric.md` | S | OPEN |
| W18 | The birthday problem's ugly cousins (near/triple/strong) | `W18_birthday_variants.md` | S | OPEN |
| W19 | How long is a chaotic prediction good for? | `W19_lorenz_shadowing.md` | M | OPEN |
| W20 | Arrow's theorem made concrete: six rules, one profile | `W20_voting_paradoxes.md` | S | OPEN |
