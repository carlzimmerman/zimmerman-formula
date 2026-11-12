# KR2 RESULT: no present-day mu_K window. FAIL on both footings: X-COP's core cannot be formed at any mu_K(0) in 0.1-79.43 Mpc^-1

TEST lane under the owner's 11-04 rule (owner 2026-11-08: "launch lanes, solve clusters and CMB based on this framework or
something compatible with the action equations"). The component is the action's own K(Q) sector: cold dark energy, never
dark matter, no particle. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

- Criteria: `FROZEN_CRITERIA.md`, 92c1ced823, committed alone and pushed before any script or number.
- Scripts:
  - `kr2.py`, with subcommands `battery`, `sparc`, `kids` and `lens`; each ran in its own process and wrote to `parts/`.
  - `kr2_grade.py` writes `kr2.json` / `kr2.out` and the MUTATE readout `kr2_MUTATE.json` / `kr2_MUTATE.out`.
  - `kr2_local.py` writes `kr2_local.json` / `kr2_local.out`. This is the post-freeze section, which is not part of the label.
  - Run logs: `run_battery.txt`, `run_sparc.txt`, `run_kids.txt`, `run_lens.txt`.
- Compute: one thread, nice 12. Peak RSS was 0.31 GB (battery), 0.70 GB (SPARC), 0.33 GB (KiDS) and 0.27 GB (lens).
  Run times were 397 s, 325 s, 51 s and 92 s. Nothing was downloaded.
- Every number in this file is read from those outputs.

## Labels

| | canonical | alt |
|---|---|---|
| **Frozen label** | **FAIL (empty at C2)** | **FAIL (empty at C1)** |
| Reading under it | C2 (X-COP) is empty on its own at every mu_K(0). C3 (groups) and C6 (hosts) are disjoint as well | C1 is empty only through the frozen T = 0 clause (disclosure 1). Under the T-carried rule alone, C1 reads [0.1, 6.31] as on canonical, and the window empties at C2 as on canonical |
| Today window (C1-C3, C5, C6), handed to KR1 | **empty** (first emptied at C2) | **empty** (C1 by the frozen clause; C2 otherwise) |

The window is the set of grid mu_K(0) values where a column passes. The label reading is B (no extra dust inside
r_J = 1/mu_K) at amount R. Windows are in Mpc^-1 (physical, today).

| Column | canonical window | alt window | reading A (uncapped) can / alt | f_cap R bracket can / alt |
|---|---|---|---|---|
| C1 SPARC clean (QX8 per-galaxy rule + every galaxy under the SPARC cap) | [0.1, 6.31] | **empty** (NOT EVALUABLE <= 15.85, FAIL above) | [0.1, 1.585] / empty | [0.1, 6.31] / empty |
| C2 X-COP core (KQ1 lines, NA2 per-bin) | **empty** | **empty** | empty / empty | empty / empty |
| C3 groups (UA1 95 % interval, both f*) | [1.585, 3.98] (edges 1.53, 4.76) | [1.585, 3.98] (edges 1.33, 4.65) | [0.631, 2.51] / [0.251, 1.585] | [2.51, 3.98] / [1.585, 3.98] |
| C4 Bullet | NOT EVALUABLE (RSS) | NOT EVALUABLE | | |
| C5 KiDS G6 with kSZ gas (KX1, two-sided) | [0.1, 3.98] (edge 5.73) | [0.1, 3.98] (edge 4.55) | [0.1, 1.585] / same | [0.1, 3.98] / same |
| C6 hosts inside R500 (NC4) | [0.1, 0.631] (edge 0.84) | [0.1, 0.631] (edge 0.76) | same | same |
| C7 CMB lensing, corrected kernel, static mu | **empty** (Delta chi^2 309-1315) | **empty** (309-1315) | | |

Edges are 12-step log bisections, reported only. Running intersection in the frozen order (canonical): after C1
[0.1, 6.31], after C2 empty. Empty on their own: C2 and C7 (canonical); C1, C2 and C7 (alt). Disjoint pair on both
footings: C3 [1.585, 3.98] and C6 [0.1, 0.631]. So even with X-COP set aside, groups and hosts cannot be met at one mu_K(0).

## What the columns say

- **C2 X-COP (binding, kernel-free).** Under the brief's rule (reading B), the extra dust starts at r_J = 1/mu_K.
  - **mu_K <= 6.3:** r_J >= 158 kpc, so the core line fails (a hollow beyond 100 kpc). The inner bin (0-0.25 R500) stays
    at the law's under-prediction of +0.54 / +0.51 dex.
  - **mu_K >= 10:** KQ1's equilibrium puts all of R x M_last inside 0.25 R500 (c = 0.99-1.00), and R = 5.41 is above the
    need. The inner bin over-fills by -0.89 to -1.23 dex.
  - The best per-bin rms is 0.439 / 0.425 at mu_K 2.5 / 1.6. Under reading A the best is 0.248 / 0.237, and with the
    f_cap R amount 0.225 / 0.231. That is KQ1's 0.226 again, against a line of 0.10.
  - No mu_K in the window gives a 50-100 kpc core holding X-COP's need.
- **C6 hosts.** With R x baryons retained inside R500, every cluster's M_d(<R500)/M_b(<R500) reaches 8.9, against
  F_X 4.18 / 3.78. The hosts' held share is H = 0.019, against NC4's most generous capacity of 0.0248 / 0.0222.
  - H itself passes; the per-cluster amount line fails.
  - C6 passes only while r_J > R500 (mu_K <= 0.63, edges 0.84 / 0.76), which keeps the dust out of every cluster.
- **C3 groups.** A step inside UA1's interval (+0.052 to +0.459 canonical, +0.009 to +0.415 alt) appears only when r_J
  falls inside the groups' graded radii and the dust is still extended: mu_K 1.6-4.0, steps +0.06 / +0.22 / +0.35. Below
  that range there is no step (0.000); above it the step is +0.57 to +0.66.
- **C5 KiDS.** Under reading B the lenses keep no extra dust inside 300 kpc while r_J > 300 kpc, so KX1's budget passes up
  to mu_K 3.98. At mu_K >= 6.3 the dust is held at 100-300 kpc: z +3.1 to +3.8 in bin 1 and >= 2 bins over, so it fails.
  - Reading A (uncapped) passes only up to 1.585. This is the iter_5 / QX10 kill, moved by KX1's wider budget.
- **C1 SPARC.** Under reading B no galaxy carries extra dust inside r_last for mu_K <= 6.3 (r_J >= 158 kpc).
  - At 10 and 15.85, 1 and 7 galaxies exceed the cap.
  - From 25 up, the rule fails: rms 0.136-0.303 canonical, with 22-81 galaxies over the cap.
  - Reading A fails from 2.5 up, where 1-160 galaxies are over the cap.
- **C7 CMB lensing.** With mu held at mu_K(0) at all z, Delta chi^2 is 309-1315 across the window. That reproduces GL1's
  wall: the line is 631. See the hand-off below.

### Hand-off to KR1 (C7-run, reported): z_run,max(mu_K(0))

The table gives the largest z_run with Delta chi^2 <= 4 when mu = mu_K(0) for z < z_run and there is no suppression above.
It is the same on both footings.

| mu_K(0) | 0.1-0.16 | 0.25-0.40 | 0.63-1.0 | 1.585 | >= 2.5 |
|---|---|---|---|---|---|
| z_run,max | 2 | 3 | 5 | 10 | >= 20 (grid top) |

Reading: CMB lensing tolerates a low today-mass if the mass has grown past the lensing line by z of about 2-20. That is the
part KR1's DBI members satisfy on the background (M(z 3) = 631). The window it would apply to is empty.

## Known answers (all PASS, 20/20; nothing was graded until they did)

| KA | result |
|---|---|
| KQ1's own KA1-KA5, run inside its prefix | all PASS (law X-COP 0.467499 / 0.434523; KD1 G2 cusp; iter_5 lambda_0 3.162 row; calculators) |
| KA2 SPARC law only through C1 = QX8 exact | rms 0.05604651 @ U 0.58 / 0.05582588 @ 0.52, abs(d) 0 |
| KA3 X-COP law only through C2 | 0.467499 / 0.434523, abs(d) 4.9e-8 / 5.6e-8 |
| KA4 KiDS law through C5 = KX1 E_b, sigma | max abs(d) 0, W = 0 |
| KA5 groups law only | step 0 / 0 |
| KA6a KQ1's recorded closest row (mu 19.05, F_X) through my C2 path | rms 0.78373 / 0.75796, inner bin -1.0772 / -1.0417, abs(d) 0 |
| KA6b KX1's C2 cell through my C5 wrapper | W per bin, abs(d) 0 |
| KA6c the two solvers, M_d(200 kpc), 10^10.7 host, mu 1 | QX10 3.847e10 vs iter_5 3.846e10 Msun, relative 1.9e-4 |
| KA7 vectorised solver = iter_5 `profile` (X-COP, groups, SPARC) | max relative 0 |
| KA8 C7: growth copy = QX3; static Delta chi^2 = GL1 converse | abs(d) 0; 667.4606 / 309.0285 (can), 667.3448 / 308.9734 (alt) |

## MUTATE (`kr2_MUTATE.out`; every twin bites or holds)

- **M1, mu_K -> mu_B = 8.890e6 / 8.889e6.** This reproduces KD1 / KQ1:
  - At KD1's capture amount, X-COP gives KD1's cusp, -0.702864 / 0.802677 and -0.714392 / 0.809485, with abs(d) 0. The
    largest r_1/2 is 2.1e-4 kpc, so L1 fails.
  - At R: C1 FAILS (rms 0.730 / 0.740, U at the 0.30 floor, all 175 galaxies over the cap). C2 FAILS (rms 0.897 / 0.904).
    C5 FAILS (z +2.4 to +3.8 in all 4 bins). At f_cap R it equals HY1's point-mass KiDS z to 9e-16.
  - **Bites.** C7 static is 0.000 there (reported).
- **M2, f -> 0.** The law's record numbers come back to 0: SPARC QX8, X-COP 0.467499 / 0.434523, KX1 E_b, and a UA1 step
  of 0. C2 FAILS at f = 0, so C2 has power. **Bites.**
- **M3, planted NC4 cored isothermal at r_c 100 kpc and the need amount.** C2's L3 and L4 PASS (rms 0.0908 / 0.0907,
  c 0.2485-0.2663). The lines can pass. **Holds.**

## Disclosures

1. **The alt C1 label is set by the frozen T = 0 clause, not by the dust.**
   - The frozen C1 needs the QX8 line to give the same PASS/FAIL with T carried and with T = 0. Otherwise the cell is NOT
     EVALUABLE.
   - On alt, the law ALONE fails the line at T = 0: U median 0.44 < 0.50, as in QX8's own record (law rms 0.05372 @ 0.44).
     So every alt cell where reading B keeps the dust out of the discs (mu_K <= 15.85, 12 cells) reads NOT EVALUABLE. The
     cells above that FAIL.
   - With T carried (the QX8 / HY1 primary), alt C1 reads [0.1, 6.31], the same as canonical. Under that reading alt
     empties at C2, as canonical does.
   - The label stays as frozen. The conclusion does not depend on it, because C2 is empty on both footings regardless.
2. **The C1 dust host is fixed at U 0.5 (bulge 0.7).** The per-galaxy U refit does not move the dust. This is disclosed in
   criteria section 4.
3. **C2's core line under reading B is L1B (r_J <= 100.5 kpc).** KQ1's density lines L1/L2 are defined for the uncapped
   profile and are graded in reading A. L3 and L4 decide C2 in both readings; L1B never rescues it.
4. **C4 (Bullet) was not run.** The only machinery on disk (DB1/UX6 via NA2's child) measured 1.19-1.48 GB. The window is
   empty without it, and C4 could only shrink it.
5. **C5 retention.** KX1's own solver retains what fits inside r_ta (closed boundary). C1, C2, C3 and C6 use iter_5's
   all-or-nothing rule. The two solvers agree to 2e-4 where both bind (KA6c).
6. **C6 has two parts, and the per-cluster one binds.** H = 0.0133 x median q500 / R peaks at 0.019, under NC4's 0.0248 /
   0.0222. The per-cluster line q500 <= F_X fails as soon as the dust sits inside R500.
7. **Worktree.** The run used a detached worktree at origin/main (../kr2_wt). It had an untracked symlink to the shared
   checkout's gitignored `real_research/data/lensing_rar/brouwer2021_rar`, as HY1 and KR1 did. The symlink is not
   committed.
8. **The battery process was launched from a shell `&` (not a tracked background task).** Its log `run_battery.txt` is
   complete.

## POST-FREEZE (requested by the orchestrator after KR1 landed, 38b8f7749f; graded separately, NOT the frozen label)

KR1 found that for any convex K(Q), the mass M^2 = Q^2 K''/2 is a function of the sector's own local density, not of the
background's mu_K(0).

`kr2_local.py` takes the following read-only: KR1's DBI members D0-D3 (mu 1e-3, 0.1, 9.998, 79.43, each with lambda fixed
by M(z 3) = 631) and KR1's exact inverse `M_at_density`. With them it evaluates M at each column's local dust density,
relative to today's mean.
- Known answer: KR1's M_ta at 149.85 x mean is reproduced, abs(d) 0, for 4 members x 2 footings.

| Column, local density (canonical; alt within 0.5 %) | rho / mean | local M (Mpc^-1), D0-D3 | 2 pi / M |
|---|---|---|---|
| C1 SPARC: captured galaxy at turnaround (KR1 GC) | 149.8 | 2173-2261 | <= 2.9 kpc |
| C3 groups: turnaround (same convention) | 149.8 | 2173-2261 | <= 2.9 kpc |
| C5 KiDS: R x M* mean inside 100 kpc, lm 9.4 to 10.9 | 97-3057 | 1140 to 2.1e5 | <= 5.5 kpc |
| C5 KiDS: R x M* mean inside 300 kpc, lm 9.4 / 10.45 / 10.7 / 10.9 | 3.6 / 40 / 71 / 113 | 8.3-82 / 314-336 / 737-744 / 1436-1484 | <= 753 / 20 / 8.5 / 4.4 kpc |
| C2 X-COP: the need profile (cored r_c 100 at F_X), mean inside 100 kpc / 0.25 R500 | 3.9e4 / 1.0e4 | 8.9e6 / 1.2e6 | <= 0.005 kpc |
| C6 hosts: mean inside R500 (500 rho_crit) | 1585 | 7.4e4-7.8e4 | <= 0.08 kpc |

**Does the window survive once M is local? NO, on both footings, for every column.**
- C1's window tops out at 6.31; local M >= 2173.
- C3's tops out at 3.98; local M >= 2173.
- C5's tops out at 3.98. The lowest local M anywhere in the KiDS stack is 8.3, in the lightest bin's 300 kpc mean, and the
  heavier bins carry >= 314.
- C6's tops out at 0.63; local M >= 7.4e4.
- C2 and the today window were already empty.

The local masses sit 2-5 decades above every column's window. In the record's dynamics the dust is then a compact, Jeans-
unsupported cusp (KD1's model P, KR1's G1-G8), which is MUTATE M1 here: SPARC rms 0.73, X-COP rms 0.90, KiDS z +2.4 to +3.8.

One caveat makes the section generous. The densities assume the dust sits at R x the baryons in each system. A lower
density would lower M only as rho^1.5, and even the lightest KiDS bin at 300 kpc (3.6 x mean) carries M >= 8.3, which is
above C5's top of 3.98.

## In plain words

The question was whether the action's own cold dark-energy sector, carrying the CMB's amount (5.41 times the baryons), could
be given one present-day mass scale mu_K(0) that keeps galaxies clean and still fills clusters. With the brief's rule (no
extra dust inside 1/mu_K, self-bound dust beyond), the answer is no, on both footings.
- The X-COP clusters decide it. Wherever the dust can start inside 100 kpc, the record's own equilibrium piles the whole
  amount into the inner quarter of R500 and over-fills it by about a factor of ten. Wherever it does not, the core is
  hollow and the inner clusters stay as short as the law alone leaves them.
- The best per-bin scatter is 0.43, or 0.23 without the brief's cap (KQ1's 0.23 again), against a line of 0.10.
- Even without clusters, group masses need mu_K 1.6-4, while the hosts' measured capacity needs mu_K <= 0.6. Those two
  never meet.
- Galaxies and KiDS lensing are happy below about 4-6 per Mpc. CMB lensing at a constant mass fails everywhere in the
  window; it would pass if the mass had grown back past the lensing line by z ~ 2-20, which is KR1's running.

KR1 has since shown that the mass is not set by the calendar but by the dust's own local density. At the densities of a
galaxy, a group, a lensing halo or a cluster core, that mass is thousands to millions per Mpc. So even the partial windows
above do not survive: the dust collapses into the KD1 cusp, and the K(Q) door closes from both lanes.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
