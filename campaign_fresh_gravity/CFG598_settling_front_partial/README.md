# CFG598: the settling front with the transport-clock correction. Frozen verdict: ONE α DOES NOT give partial settling that works, under both placements

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dd49c4124). Date: 2026-10-10.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled (the CFG543 group path uses CFG543's own 9.36e-11 / 1.13e-10). Flat a0, ν_mono, candidate B, G9, no EFE. The cold energy's MASS is still required; no particle species. This is not "theory closed", and nothing here says the data favour the framework.
- **Accretion history is INHERITED** from CFG557's `cfg557_lib` (EPS main progenitor, q = 2.2, recalled, PROVISIONAL; ΛCDM-background spherical collapse). It is not derived from the framework alone.
- **Numbers:** all come from `cfg598_results.json` / `cfg598_results_MUTATE.json`. Pairs are canonical / alt.

## Scripts

| file | what it does |
|---|---|
| `cfg598_lib.py` | Host accretion history (CFG557, read-only import). The CFG541 class-A radial drift PDE with infall sources (CFG541's donor-cell scheme, re-implemented). The exact α → ∞ minimiser. Diagnostics. |
| `cfg598_front.py` | Main run: 40 jobs × 6 α, 4 processes × 1 thread, `nice -n 10`, about 10 min. Writes `cfg598_front.out` and `cfg598_results.json`. `CFG598_MUTATE=1` writes the `_MUTATE` files and exits 1 when every tooth bites. |

Read-only reuse:
- CFG557 lib;
- CFG543 `cfg543_group_supply` (imported; `sigma_log` copied with one change);
- CFG555's 512³ spectrum caches in `_external_data/cfg555_work`, and its `stat`, copied.

`sol61_push/transport_clock_2026_10_10/check.py` was re-run read-only, with its output written outside the repo: **PASS 87/87**.

## Controls (all PASS)

- **K1:** t0 = 13.8196 Gyr and Δ_ta = 11.8056, matching CFG557.
- **K2:** largest mass error 3.4e-15.
- **K3, the transport-clock benchmark on our PDE flux:** a filled core plus uniform f = 0.2 / 0.5 / 0.8 reproduces ∂_t f = αV_f√f(1−f) r_i/r² to −0.12% at r/r_i = 2, 5 and 10. The single clock is larger by exactly r/r_i (2.004, 5.000, 10.000).
- **K4:** no run hit the step cap.
- **Convergence:** N = 600 against 300 changes F_set by at most 0.003 (P0) and 0.001 (P2).
- **G0:** CFG543 P2 reproduced exactly (+0.059613 / +0.043489).
- **CFG555:** λ = 1 and λ = 0 reproduce the gravitating (0.163060 / 0.192528) and particle values to all printed digits.

## MUTATE (all teeth bite)

- **M1, α = 64 against the exact α → ∞ trajectory** (log M_ta 14, canonical): max |ΔF_set| is 0.0008 (P0) and 0.0014 (P2), and the S ratio is 1.0000 / 1.0018.
- **M1b, the minimiser's infinite-age edge against CFG541's r_M/ln(1 + M_b/M_cat):** agreement to +0.02% (log 12 and 14, both footings).
- **M2, no transport-clock correction:** the single-clock path matches the analytic tanh² to 1e-14, and it differs from the PDE by the factor r/r_i (K3).

## 1. The settling front (task 1)

F_set(<r) is the fraction of the law's phantom that is settled inside r at t0. r_f is the q < 0.9 front.

**P0 (at rest at turnaround: the drift alone delivers), canonical:**

| log M_ta | α | F_set at 0.1 / 0.2 / 0.3 / 0.5 r_ta | r_f/r_ta | S/S_∞(<0.5) |
|---|---|---|---|---|
| 13 | 0.25 / 0.5 / 1 / 2 / ∞ | 0.91/0.73/0.62/0.48 · 0.98/0.90/0.78/0.54 · 0.99/0.98/0.90/0.56 · 1.00/0.99/0.94/0.57 · 1.00/1.00/0.97/0.57 | 0.064 / 0.125 / 0.216 / 0.264 / 0.288 | 0.83 / 0.95 / 0.99 / 0.99 / 1 |
| 14 | same | 0.88/0.68/0.57/0.45 · 0.97/0.87/0.74/0.53 · 0.99/0.97/0.88/0.57 · 1.00/0.99/0.95/0.58 · 1.00/1.00/0.99/0.58 | 0.058 / 0.112 / 0.200 / 0.268 / 0.297 | 0.77 / 0.90 / 0.98 / 0.99 / 1 |
| 15 | same | 0.81/0.62/0.54/0.47 · 0.95/0.81/0.70/0.56 · 0.98/0.94/0.87/0.67 · 0.99/0.98/0.96/0.74 · 1.00/1.00/1.00/0.77 | 0.049 / 0.089 / 0.165 / 0.284 / 0.392 | 0.61 / 0.73 / 0.87 / 0.96 / 1 |
| MW | same | 0.91/0.79/0.72/0.62 · 0.98/0.91/0.84/0.70 · 0.99/0.98/0.94/0.78 · 1.00/0.99/0.98/0.81 · 1/1/1/0.82 | 0.060 / 0.119 / 0.236 / 0.351 / 0.406 | 0.75 / 0.85 / 0.95 / 0.99 / 1 |

All masses (11–15) and the alt footing are in `cfg598_front.out`. Alt is lower by 0.01–0.05.

- **The front is inside-out and α-paced.** r_f roughly doubles with each doubling of α up to α ≈ 1. Above that it saturates at the α → ∞ front, which is the finite-age supply edge (0.24–0.41 r_ta).
- At α ≥ 1 the hosts are within 1–13% of the α → ∞ state at 0.5 r_ta. At α = 0.25 they hold 61–95% of it.
- **The transport-clock correction matters.** The single clock (homogeneous relaxation, no r_i/r factor) overstates F_set(<0.5 r_ta) by 0.13–0.39 (log 12–15, α 0.5 and 1), for example 0.77 against 0.53 at log 14, α = 0.5.

**P2 (deposited after first collapse with radial-orbit weights).** It is dominated by the placement, not by α:
- the orbit-averaged reservoir already fills the inner region at α = 0 (F_set(<0.1) ≈ 0.88–1.0);
- shells that have not collapsed by t0 (22–54% of the catchment, rising with mass) are not yet delivered;
- F_set(<0.5) is 0.29–0.44 at every α (log 11–15), and S/S_∞ is above 1 because of the overfill (one-sided deficit).

**Supply bound α_sup = G S/(T V_f³ · 2/(3√3))** with T = t0 − t_ta(X = 0.5):

| log M_ta | 11 | 12 | 13 | 14 | 15 | MW |
|---|---|---|---|---|---|---|
| α_sup (can / alt) | 0.34 / 0.29 | 0.64 / 0.56 | 0.51 / 0.45 | 0.58 / 0.50 | 1.02 / 0.89 | 0.84 / 0.73 |

With T = t0 − t_s the bound is 0.23–0.63. For α ≳ 0.5–1 the drift can carry the whole catchment within the host's age, and the PDE confirms it: the hosts reach their finite-age supply edge. The rate-limited, unexhausted regime is α ≲ 0.5. **That is the same range where the MW interior stops being fully settled.**

## 2. Comparisons (task 2)

**(a) CFG593, context only (it used ΛCDM-SHMR masses).**
- At α = 0.25 (P0) the numbers land in CFG593's window. F_set(<0.5 r_ta) is 0.45–0.48 (log 13–15), and it holds 0.61–0.83 of the α → ∞ supply.
- **But the shape is the opposite.** CFG593's family is a *uniform* partial fill with inner mass below the full law (M/M_L 0.35–0.8 at 0.05–0.2 r_ta). The PDE fills the inside first: F_set(<0.1 r_ta) is 0.81–0.91 even at α = 0.25, and 0.95–0.99 at α ≥ 0.5.
- Matching the fraction does not mean matching the profile.

**(b) Framework-native constraints.**
- **MW inside 30 kpc (CFG553).**
  - P0: SETTLED for α ≥ 0.5 on both footings (min q 0.993 / 0.993 at α = 0.5), with M_c/M_ph(<30 kpc) = 1.002 / 1.001. α = 0.25 just misses: q = 0.984 / 0.985 at 21–29 kpc, which is the tail of the front.
  - P2: OVERFILLED at every α including α = 0. M_c/M_ph(<30 kpc) is 1.89 / 1.69, so the overfill is placement-driven. Radial orbits from rest put every shell through the centre, and class A cannot remove an overfill (CFG541 open item 5).
- **Groups (CFG543 P2, cold mass × R(r)).**
  - P0: PASS for α ≥ 0.5 on both footings. α = 0.25 gives Z +2.03 (FAIL) on canonical and +1.93 on alt. α = 0 fails hard (+5.37 / +6.09).
  - P2: PASS at every α (Z 0.94–1.93).
  - Less settled mass at group radii raises Δ̄. Groups pull toward MORE settling, against the growth direction.
- **Growth / excess (CFG555 512³, scalar λ = mean S_α/S_cen(<0.5 r_ta) over log 13–15).**
  - P0: λ is 0.75 / 0.77 at α = 0.25 and 0.87 / 0.89 at 0.5, giving max|P − 1| 0.124 / 0.153 and 0.142 / 0.174 against CFG555's 0.163 / 0.193. **NOT REDUCED** by the frozen ≥ 25% rule: α = 0.25 is a 24% / 21% reduction. Only α = 0 (no settling drift at all) passes canonical (0.089).
  - P2: λ ≈ 0.52–0.55 at every α, from the uncollapsed transit mass (a finite-age effect, α-independent). max|P − 1| is 0.088–0.095 (PASS) on canonical and 0.111–0.116 (REDUCED) on alt.
  - Approximation (declared): one global amplitude. Because the PDE keeps the inner region full, a per-host radial treatment would most likely reduce the excess *less* than the global λ does. So this approximation flatters the result, and the P0 fail is not an artefact of it.

## 3. Verdict (frozen section 3)

| | (i) MW | (ii) partial 0.2–0.5 r_ta | (iii) excess | groups |
|---|---|---|---|---|
| P0 α = 0.25 | fails (q 0.984) | **holds** | NOT REDUCED (−24% / −21%) | fails on canonical (Z 2.03) |
| P0 α = 0.5, 1, 2 | holds | fails (S/S_∞ > 0.9, inner F_set(<0.2) > 0.8) | NOT REDUCED | pass |
| P2, any α | fails (overfill ×1.7–1.9) | fails (S/S_∞ > 1) | REDUCED (alt) / PASS (can) | pass |

**P0: DOES NOT. P2: DOES NOT. OVERALL: ONE-α PARTIAL SETTLING DOES NOT WORK.** It is not placement-sensitive.

**Mechanism.**
1. The transport-clock geometry is real: it slows the outer fill by r/r_i, and the PDE confirms it.
2. One α still splits into two regimes, separated by the supply bound α_sup ≈ 0.3–1.0:
   - **α ≳ 0.5:** the catchment is delivered within the age. Everything settles to the finite-age supply edge. The MW and groups pass; there is no rate-limited partial state, and the excess stays at 87–99% of its source.
   - **α ≈ 0.25:** the fill is rate-limited out at 0.2–0.5 r_ta, as asked. But the front is then still crossing 20–30 kpc in the MW, the canonical groups slip to Z 2.03, and the excess falls by only about a fifth, because the inner region (≤ 0.1 r_ta), which drives the concentration, is still filled first.
3. **The deeper obstruction is the profile shape.** The drift fills inside-out at any α, while the growth excess needs less mass at 0.05–0.2 r_ta (CFG557, CFG593). No α turns an inside-out front into a reduced inner mass.
4. The near-misses at α = 0.25 are within a factor of about 1.5 of every bar. They are reported, not rounded up. No α between grid nodes was scanned (owner rule: no knob scans).

## Disclosures (dated 2026-10-10)

- **Drift speeds.** max |v_s|/V_f reaches 45–137 in sparse reservoir cells (only cells with ρ_c ≥ 1e-3 ρ_ph counted). This is the overdamped inconsistency of CFG541 open item 3. No limiter was added, as frozen. An inertia-limited drift would slow delivery and push every α toward the less-settled side.
- **P2 placement.** Purely radial orbits from rest overconcentrate the centre, which causes the MW overfill. "Collapse" = reaching 0.003 r_ta, so P2 holds back 22–54% of the catchment as in transit. Both are bracket properties, not α effects. P0 is the cleaner test of the drift itself.
- **Baryon growth.** M_b(t) = M_b,0 X_ta(t) and point-mass baryons for the grid hosts, both declared. The group ratio R comes from point-mass hosts and is applied to Hernquist groups.
- **MW P0 inner cells** show q up to 104 inside 30 kpc. This is the Newtonian core, where ρ_ph is tiny and the initial ρ ∝ r^−2 placement of the first 2% overfills it in relative terms. The mass ratio M_c/M_ph(<30 kpc) stays ≤ 1.006, below the 1% rule.
- **CFG543 footings.** The group path uses CFG543's rounded footings (9.36e-11 / 1.13e-10) so that G0 reproduces CFG543 exactly.

Commits: criteria dd49c4124; results in the commit that adds this README.

**ID note (dated 2026-10-10).** After this lane's criteria were committed (dd49c4124), a parallel session committed its own CFG598 criteria (93abcbeb6, `CFG598_anisotropic_velocity_target/`, anisotropic velocity-relaxation target). It is not part of this lane and was not touched. The two lanes share the number CFG598; the ledger owner should renumber one of them.
