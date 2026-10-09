# CFG527 FROZEN CRITERIA: a law-respecting engine -- compensation drawn from the shell OUTSIDE the census edge, phantom sourced by UNFILTERED retained baryons

Committed alone, before any code change or run. Date 2026-10-09.

## Why (CFG526)

CFG526 (A) found the small-scale power deficit (CFG521/524) is an ENGINE ARTEFACT on both footings: candidate B's own halo inside the census edge, M_law = M_b,all + (nu - 1) M_b,ret built from the run's own baryons, is as massive in the core as the matched S0 halo, but the engine's gravitating core holds only 0.51-0.77 of it; the shortfall tracks the grid; no compensation sits within 0.05 dex of the law. Two engine ingredients cause it: (1) the MOND input is pressure-filtered (MIX-A: 54% of the baryons smoothed at k_J(1e6 K) ~ 0.45 h/Mpc), so the in-core phantom is far below the phantom of the real baryons; (2) the per-catchment draw comp = q s_c removes cold energy from the same cores. This lane builds the rule CFG526 implies and judges it on the framework's own terms (the CFG526 law-profile statistic, unchanged) and on growth.

Settings (unchanged): kappa = 1/2 FITTED; footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), never pooled; a0 FLAT; kernel nu_mono; T1 switch eps = 0.077; census fret_of (CFG416) painted per turnaround ball, largest host wins, f_ret = 1 outside catchments; census edge r_e = x_supply(r_ON) r_ON (capped at r_ON); expelled baryons kept as gravitating mass (CFG518 convention); LCDM background; EH ICs at z_i = 49 (the only LCDM input); step grid; seed 359, NSEED 256 at 256^3 (512 at 512^3); resolved r_ON >= 2 cells of the 256^3 mesh (RMIN = 2L/256; 1.56 Mpc/h at L = 200). The cold energy's MASS is still required. Not "theory closed".

## The rule (no new parameter)

Both radii already exist in the engine: the census edge (the switch mask IN(x_supply), CFG416/518) and the turnaround catchment (IN(x = 1) cover components, CFG424). Per force call, with the same arrays the engine already uses at that step:

- **Excess (unchanged):** e = f_sw max(s_ph - s_c, 0) x catch, where f_sw already carries the census-edge mask (so e = 0 outside the census edge).
- **Draw region (new):** D = catch AND NOT edge, i.e. cells inside a turnaround catchment and outside every census-edge ball (the unsettled shell around the host). Inside the census edge nothing is drawn.
- **Weight (new):** comp = q_C s_c on D_C, zero elsewhere; per catchment component C (CFG424 labels, unchanged): E_C = Sum_C e, R_C = Sum_{D_C} s_c, q_C = E_C / R_C.
- **Cap (existing, unchanged in form):** if q_C > 1 (including a catchment whose shell is empty, R_C = 0, with E_C > 0), e -> e / q_C in that catchment and q_C -> 1 (the whole shell reservoir is drawn, never more). How often it acts is reported (number of catchments, mass fraction, fraction of Sum e removed, number of catchments with an empty shell).
- **Conservation (unchanged):** source added = e - comp, so Sum_C (e - comp) = 0 on every catchment.

### Why the weight s_c on the shell is forced (no alternative is run)

1. s_c = 1.5 Om (1 - f_b)(1 + delta)/a is the engine's only cold-energy field (CFG524 choice 1).
2. CFG524's literal unsettled reservoir is R2 = s_c - f_sw clip(s_ph, 0, s_c). The switch weight f_sw carries the census-edge mask, so f_sw = 0 identically on the shell: there R2 = s_c exactly. The shell s_c weight is therefore the CFG524 R2 reservoir restricted to the region the law does not occupy, not a new choice. (CFG524's R1 reading, clip(s_ph, 0, s_c) settled regardless of the switch, would declare cold energy "settled" where the engine assigns no phantom; it is not the literal reading and is not run.)
3. Drawing in proportion to s_c takes the same fraction q_C of the cold energy present from every shell cell; any other weight (volume, radius, density power) would impose a profile that nothing in the model supplies.
4. The in-edge cells are excluded because B fixes the in-edge total at M_law (CFG516 RM); drawing there is what CFG526 identified as the artefact.

### Unfiltered source (exact code meaning)

In the engine the MOND input is g_b = f_b (-grad phi_b), phi_b from the retained baryons f_ret(x)(1 + delta), multiplied in Fourier space by the MIX-A filter W(k) = 0.28/(1 + k^2/k_J(1e4 K)^2) + 0.54/(1 + k^2/k_J(1e6 K)^2) + 0.18 (cfg521_pm.py line `gb = [FB * (-mesh.inv(1j * kv * phik_b * Wk)) ...]`). **Unfiltered = W(k) = 1 for all k** (implemented as the mix (f_cool, f_hot, f_coll) = (0, 0, 1), tag `NOFILT`), so g_b is the CIC/PM field of the retained baryons with no other smoothing. Nothing else changes: the Newtonian force, the CIC deposit, the switch and the census are untouched. The filter enters the engine only here.

**Numerical stability.** The filter was introduced (CFG372) as a gas-pressure model, not as a numerical regulator; the pre-CFG372 engines (CFG359/361, T1/T5) sourced the phantom from unfiltered baryons and ran at 256^3. It is still tested here:
- **Declared stability check (each NOFILT run):** STABLE if every snapshot's sigma8, P(k), e_sum and src_sum are finite AND P_run/P_S0 at the bin nearest k_Nyq/2 at z = 0 is <= 2 (no grid-scale runaway). UNSTABLE otherwise (the lane is then INVALID for that run, and the filter is stated to protect stability).
- **Attribution / stability control SHF:** shell draw WITH the MIX-A filter (canonical, L = 50 and L = 25), reported: it separates the two ingredients and shows whether dropping the filter changes grid-scale power beyond the law-consistency change.

## Engine (cfg527_pm.py = cfg524_pm.py copied; changes listed in full)

1. CFG527_DRAW = `SHELL` (default) | `SC`. SC is the old core-weighted draw comp = q s_c over the whole catchment, i.e. cfg521_pm.py exactly (with the MIX-A filter).
2. Mix argument `NOFILT` = (0, 0, 1) added to MIXES (W = 1). MIXA unchanged.
3. The census-edge mask used for f_sw at that call is also used to define D (the cached mask in non-diag calls, the recomputed one in diag calls, exactly as f_sw).
4. Diagnostics only: shell fraction Sum_D s_c / Sum_catch s_c; catchments with an empty shell and their share of Sum e; cap use as CFG524; draw-weighted vs s_c-weighted mean density; in-edge net source sum; finiteness flag.
5. Bookkeeping: environment CFG527_*, outputs in ../_external_data/cfg527_work/, tags carry _<MIX>_ and _draw<SHELL|SC>.

## Runs (256^3, nice 10, 4 threads each, up to 4 at once, claim-based queue, detached with nohup)

| job | draw | source | f_ret | foot | boxes |
|---|---|---|---|---|---|
| LR-can | SHELL | NOFILT | census | canonical | L200, L100, L50, L25 |
| LR-alt | SHELL | NOFILT | census | alt | L200, L100, L50, L25 |
| K1 | SHELL | NOFILT | 1 | canonical | L50, L25 (reported) |
| MUTATE A | SC | MIXA | census | canonical | L50, L25 (= CFG521 DC-can) |
| MUTATE B | none (NOCOMP) | NOFILT | census | canonical | L200 |
| SHF | SHELL | MIXA | census | canonical | L50, L25 (reported) |

Matched S0 controls are reused, not rerun (the S0 path is untouched): CFG521 S0 L50 / L25 / L100 (256^3), CFG359 S0 N256 (L200), CFG411 S0 N512 (L200 512^3). sha256 recorded.

## Gate 1: law consistency (CFG526 statistic reused unchanged)

`cfg527_profiles.py` = cfg526_profiles.py with only the run table changed (pointing at the cfg527 runs and engine; S0 at L200 = CFG359 N256): the engine's own `forces` on the saved z = 0 positions, total potential captured exactly, rho_grav = particles + (e - comp); integrity K1 (state reproduction), K2 (S0 null), K3 (conservation) as CFG526; halo sample, discrete-ball profiles R in {1, 1.5, 2, 3, 4, 6, 8} cells, scored radii r_eff <= r_e, 100 densest scored hosts; **R = M_grav / M_law**, M_law = M_b,all + (nu - 1) M_b,ret (PRIMARY, unfiltered retained baryons -- which is now exactly the engine's MOND input), with R_noexp and R_in reported; D_law, D_eng, D_part vs the matched S0. Tolerance: CFG526's |log10 R| <= 0.1 dex.

Per footing (canonical = LR-can, alt = LR-alt), applied in order:
1. **NOT DIAGNOSTIC** if any of K1-K3 fails for the footing's L50 or L25 run or the S0s, or fewer than 20 scored halos in either L50 or L25, or no shared physical radius is evaluable in the convergence test below.
2. **LAW-CONSISTENT** if ALL of:
   - (a) median R within 0.1 dex of 1 at every scored radius (n >= 1) in L50 and in L25, and median core R (scored, <= 2 cells) within 0.1 dex in both;
   - (b) **physical-radius convergence:** CFG526's conv_stat (median log10 R at shared physical radii, L50 R = 1, 2, 3, 4 cells = L25 R = 2, 4, 6, 8 cells, scored halos with log M_ta in [12.7, 14.3], >= 10 halos in both) gives |Delta| <= 0.1 at every evaluable radius; the same test is applied to L100 vs L50 (L100 R = 1, 2, 4 cells = L50 R = 2, 4, 8 cells) where evaluable;
   - (c) **cell-unit convergence:** median core R within 0.1 dex of 1 in every box with >= 20 scored halos among L200, L100, L50, L25 (the spread across boxes is reported).
3. Otherwise **NOT LAW-CONSISTENT**, labelled SHORTFALL (core R < 10^-0.1 in both L50 and L25), EXCESS (core R > 10^0.1 in both), or DEPARTS (anything else), with every failing item named.

K1 (f_ret = 1) and SHF are put through the same pipeline and reported. MUTATE A must come out NOT LAW-CONSISTENT (see controls).

## Gate 2: growth

- **L = 200 (CFG361 cuts, gating):** each LR run vs CFG359 S0 N256 at z = 0, k <= 1 h/Mpc: GROWTH OK if |sigma8 ratio - 1| <= 0.05 and max|P/P_S0 - 1| <= 0.10; FAIL if |sigma8 ratio - 1| > 0.2; TENSION otherwise. Must be GROWTH OK.
- **L = 100:** CFG361 cuts reported.
- **Small boxes (L = 50, 25), reported:** CFG521's gate vs the matched S0 (|sigma8 ratio - 1| <= 0.05, |sigma(4) ratio - 1| <= 0.05, max|P/P_S0 - 1| <= 0.10 for k <= k_Nyq/4 -> GROWTH OK; FAIL if a sigma ratio is off by > 0.2; TENSION otherwise). In this lane S0 is information, not the yardstick at k >~ 2: S0 is the cold energy evolved as ordinary cold matter, whose halos are not B's halos.
- **Small boxes, framework-native pass (gating):** the small-scale power is the framework's if it is produced by law-consistent halos and is a converged prediction. Per footing: (i) Gate 1 = LAW-CONSISTENT, AND (ii) r(k) = P_run/P_S0 (particles, z = 0, nearest bin) is converged at k = 2 and 4 h/Mpc by CFG526's rule: |r_L50 - r_L25| <= 0.05 and |r_L100 - r_L50| <= 0.05. The converged r(k) is then the framework's small-scale prediction (reported; its confrontation with cosmic-shear data is a later lane, nothing downloaded).

## Gate 3: controls

- **MUTATE A (SC draw + MIX-A filter = CFG521 DC-can):** must reproduce CFG521's DC-can JSONs at L = 50 and 25: |d sigma8|/sigma8 <= 1e-8 and max|dP/P| <= 1e-8 at every snapshot; otherwise the lane is **INVALID**. It must also come out NOT LAW-CONSISTENT in Gate 1 (core R < 10^-0.1 as in CFG526); if it passes, the statistic has no teeth and the lane is **NOT DIAGNOSTIC**.
- **MUTATE B (no compensation, NOFILT, L = 200 canonical):** must NOT be GROWTH OK at k <= 1 (CFG518's filtered NOCOMP was TENSION, max|P - 1| = 0.139); if it is GROWTH OK, a growth pass of LR cannot be credited to the conservation and Gate 2 at L = 200 is **INCONCLUSIVE**.
- **K1 (f_ret = 1):** reported (law consistency and growth), not gating.
- **Stability:** every NOFILT run must be STABLE (definition above).

## Decision (per footing)

- **INVALID:** MUTATE A reproduction fails, or a gating NOFILT run is UNSTABLE.
- **NOT DIAGNOSTIC:** Gate 1 rule 1, or MUTATE A comes out LAW-CONSISTENT.
- **PASS (256^3):** Gate 1 LAW-CONSISTENT, L200 GROWTH OK (with MUTATE B not GROWTH OK), and the small-box framework-native pass.
- **FAIL:** Gate 1 NOT LAW-CONSISTENT (the engine still departs from the law), with the direction named.
- **PARTIAL:** anything else (each failing item named; e.g. law-consistent but L200 not GROWTH OK, or small-box r not converged).

The CFG521 small-box gate vs S0 is stated for every run, whichever way it falls.

## 512^3

Only if BOTH footings PASS at 256^3: ONE L = 200 canonical LR run at 512^3 (NSEED 512, 8 threads, nice 10), only when no other 512^3 job runs on the machine. Gated by the CFG361 cuts at k <= 1 vs CFG411 S0 N512: CONFIRMED if GROWTH OK, else NOT CONFIRMED; PENDING if it has not finished in the session (the 256^3 verdict then stands as 256^3 only).

## Reported (not gating)

- P/P_S0 at k = 0.3 / 1 / 2 / 3 / 4 / 8 by box; trend at k = 4 across L = 200 / 100 / 50 / 25 next to CFG521/518 (0.89 / 0.80 / 0.63 / 0.59) and CFG524 R2; z-growth of P/P_S0 at k = 4 (L50).
- Halo concentration ratio c/c_S0 as CFG524's post-hoc (M(<2 cells)/M(<8 cells), 100 highest peaks).
- q_max, cap use (snapshots, catchments, mass fraction, Sum e removed), empty-shell catchments, shell fraction, draw-weighted vs s_c-weighted mean density, Sum e vs K1.

## Caveats (declared before running)

- One seed at 256^3. PM forces are softened below about one cell; halo cores are 1-2 cells.
- The draw is bookkeeping of the cold share s_c, not a separate cold fluid moved particle by particle; the cold energy's MASS is still required.
- B's law here is CFG516's round enclosed-mass rule; the law check is the CFG526 statistic and inherits its caveats (baryons = the f_b share of the particles; no cooling).
- The census rule still paints group f_ret over galaxies inside group turnaround balls (CFG521 "NOT ACHIEVED"); unchanged here.
- kappa = 1/2 is fitted; f_b and rho_Lambda are not derived. A pass is not "theory closed".
