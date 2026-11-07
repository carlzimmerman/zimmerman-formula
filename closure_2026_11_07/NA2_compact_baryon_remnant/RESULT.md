# NA2 RESULT: late-formed compact baryonic objects (1e2-1e7 Msun) as the hot-system half, a SEPARATE cause. FAILS (rows) on both footings, and no single formation rule exists

**Label line:** canonical: FAILS (X-COP shape, groups shape, Bullet) | alt: FAILS (X-COP shape, groups shape, Bullet) |
overall: **FAILS (rows)**. Also: (b) NO ONE RULE (every key is S1 DEAD on both footings); (c) the M_c window shrinks to
1e2-1.8e2 Msun (not empty, so not DEAD); (a) the budget is not excluded (lower bound B1 0.054 / 0.050). MUTATE M1-M5 all
hold or bite.

Criteria: `FROZEN_CRITERIA.md`, b313324efd on origin (local bf4b0178aa), committed alone before any script or number.
Script `na2.py`. Outputs `na2.json` / `na2.out` (+ `run_main.txt`) and `na2_MUTATE.json` / `na2_MUTATE.out` (+ `run_mutate.txt`).
Every number below is read from those JSONs. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

**This door does not touch the CMB wall.** Compact baryons that form late do not exist at z 3400, and they are already
counted in the BBN baryons, so the CMB-lensing half stays a separate, open wall.

## Known answers (all PASS before anything was graded)

| KA | canonical | alt |
|---|---|---|
| KA1 DOORS gas-traced at F = f_cap R (iter_7) | +0.0189 / 0.1003, equal to iter_7 | -0.0055 / 0.0996, equal |
| KA1 DOORS baryon-traced (K2) | -0.0029 / 0.082 | -0.0269 / 0.087 |
| KA2 F = 0 (QX2) | +0.4675 | +0.4345 |
| KA3 DB1 | one survivor, "massive black holes (1e2 to ~1e7 Msun)"; M_cb/M_gas 4.36-5.44 | |
| KA4 KD1 amounts, PB3 intervals | PASS | PASS |
| KA5 Bullet R = 0 | M300 1.112e14 / 7.337e13, dkappa -0.0683 / -0.1106 | |

## Which PBH walls apply to late-formed objects

The walls that shut PBHs at 1e3-1e9 Msun do not apply here. Those are CMB accretion at z 300-1000 and Poisson
isocurvature / Ly-alpha, and late-formed objects do not exist that early. LVK primordial binaries, PTA and mu-distortion
also do not apply. What still applies:
- MW dynamics (D1-D4) and Galactic X-ray / radio (X1), which scale with how many objects the rule puts in discs.
- Cosmological millilensing (L3), conditional on the objects forming by z ~2.
- The dynamics of the dwarfs and UDGs that must carry the objects. These are graded in (c).

## (a) Amount and budget

| Class | F needed (canonical / alt) | progenitor baryons / today's |
|---|---|---|
| X-COP | 4.18 / 3.78 | 5.18 / 4.78 |
| groups (upper) | 3.46 / 2.86 | 4.46 / 3.86 |
| bright M31 dSphs | 1.64 / 1.50 | 2.64 / 2.50 |
| Coma UDGs | >= 23.6 / 20.2 | >= 24.6 / 21.2 |
| SPARC discs | <= 0.33 / 0.19 | |
| LG field dwarfs | 0 | 1 |

- **Budget B1, eRASS1 lower-bound census vs BBN D/H.** The sample is 0.02 <= z <= 0.10 and PCONT <= 0.5, which gives 467
  clusters and 590 groups in V 1.63e8 Mpc^3.
  - Host baryons are 0.0108 of rho_b(BBN). The CBOs they need are 0.0435 / 0.0387.
  - B1 = 0.0544 / 0.0496, and the worst bracket (13,116 deg^2) gives 0.0855 / 0.0779.
  - So the census does not exclude it. This is a lower bound, so it is not a budget pass.
  - X-COP's M_*/M_gas at R500 is 0.058.
- **BBN input.** Omega_b h^2 = 0.02166 from D/H (as in DB1 and PB3, PROVISIONAL). It is a measurement, not an LCDM fit, and
  rho_b needs no h.
- **PROVISIONAL reading, no label.** On DB1's census range (hot cluster gas is 4-10 % of cosmic baryons), the CBOs would be
  0.18-0.44 (canonical) or 0.16-0.40 (alt) of all baryons, dark and formed without stars or metals. No channel for that is
  known (DB1).

## (b) One formation rule: NONE, both footings

Each key and convention was graded with OQ1 S1 on SE2 95 % intervals (PB3 model U), in 0.2 dex bins. Every one is S1 DEAD,
so S3 was never reached.

| Key, per | canonical widest conflict (f* 1) | alt |
|---|---|---|
| f_* per baryon / per star | bin [0, 0.2]: Coma UDGs need >= 10 vs SPARC <= 0.316; gap 1.50 dex; 7 empty bins | >= 7.08 vs <= 0.178; gap 1.60 |
| M_b per baryon | bin [7.6, 7.8]: UDGs vs SPARC dwarfs; gap 1.50 | gap 1.60 |
| M_b per star | bin [7.8, 8.0]: UDGs vs SPARC / LG field; gap 1.50; 11 empty bins | gap 1.60 |
| Sigma_b per baryon | bin [0.2, 0.4] Msun/pc^2: UDGs vs SPARC; gap 1.50 | gap 1.60 |
| Sigma_b per star | bin [1.2, 1.4]: X-COP >= 68.4 vs SPARC <= 0.316; gap 2.33 | 60.9 vs 0.178; gap 2.53 |
| v per baryon / per star | bin [1.2, 1.4] (16-25 km/s): UDGs vs SPARC dwarfs; gap 1.50 | gap 1.60 |

**Spread needed.** UDG over the SPARC cap is 72x (canonical) and 104x (alt). X-COP over the SPARC cap is 12.8x / 19.5x.
- The Coma UDGs sit at the same mass, velocity, surface density and stellar fraction as SPARC dwarfs, yet need 30-50x more.
  A rule keyed on any formation property of the system therefore has to be a class label.
- Under the per-star convention, the f* 0 group bracket has no stars, so its needs diverge (>= 398). That conflict comes
  from the bracket. The f* 1 rows above carry the reading.

## (c) Dynamics of the objects: window 1e2-1.8e2 Msun (both footings)

t / t_H, class median, with each class at its own need (dynamical friction (DF) graded at the shorter of Newtonian and /nu):

| M_c (Msun) | bright M31 t_heat, t_DF | Coma UDGs t_heat, t_DF | groups t_DF | X-COP t_DF, L_acc/L_brems (eps 0.1 bracket) |
|---|---|---|---|---|
| 1e2 | 16.9, 2.62 / 18.4, 2.35 | 171, 1052 / 200, 917 | 1.5e8 | 8.9e8, 5.7e-20 (3.4e-8) |
| 1.78e2 | 9.97, 1.56 / 10.9, 1.39 | 100, 615 / 117, 536 | | |
| 3.16e2 | 5.9, **0.93** / 6.45, **0.83** | 58.6, 360 | | |
| 1e4 | 0.27, 0.046 | 2.46, 15.1 / 2.88, 13.1 | 1.9e6 | 1.1e7, 5.7e-16 (3.4e-6) |
| 1e5 | 0.040, 0.007 | **0.32**, 1.92 / **0.37**, 1.68 | 2.1e5 | 1.2e6, 5.7e-14 |
| 1e7 | 0.002, 0.0003 | 0.007, 0.043 | 2.8e3 | 1.5e4, 5.7e-10 (3.4e-3) |

- Allowed range per class:
  - X-COP and groups: the whole grid.
  - Coma UDGs: 1e2-1.78e4 (canonical) or 1e2-3.16e4 (alt), set by heating of the stars.
  - Bright M31 dSphs: 1e2-1.78e2 only, set by dynamical friction.
- **The window over all needing classes is 1e2-1.78e2 on both footings: not empty, so not DEAD.** DB1's 1e2-1e7 window
  shrinks by about 4.7 of its 5 dex.
- Bondi X-rays in X-COP are negligible at every M_c, even at eps 0.1.
- Reported only, not window gates:
  - PB2 FW at the SPARC cap. If discs carried the cap, 1e2 would be closed by X1 (8.4e-4 at the 1e2 row) and 1e6-1e7 by D4.
    So the rule must put next to nothing into discs, which is what SPARC and the LG field ask anyway.
  - L3, if the objects form by z 2. At the lower-bound cosmic share 0.044 every decade is open. At the PROVISIONAL share
    0.44 / 0.40, 1e5-1e7 closes; the surviving 1e2 window is untouched (ceiling 2.1e5).
  - Cluster millilensing and caustic-transient stars: NOT EVALUABLE (no lensed-source data on disk).

## (d) Shape (DOORS construction, per bin): FAILS

X-COP, with the amount fitted on X-COP. Mean, rms and bin means are in dex, with bins in r/R500.

| shape | canonical F, mean / rms, bins 0-0.25, 0.25-0.5, 0.5-0.75 | alt | gate |
|---|---|---|---|
| **stars (graded)** | 1.723, +0.0185 / **0.1208**, -0.068, +0.089, +0.070 | 1.560, +0.0173 / **0.1138**, -0.059, +0.086, +0.059 | **FAIL** both |
| HSE-traced | 2.787, +0.0057 / 0.0892, +0.050, +0.023, -0.047 | 2.524, +0.0052 / 0.0869 | pass (bracket) |
| baryon-traced | 4.206, -0.0017 / 0.0818, +0.055, +0.031, -0.075 | 3.811, -0.0017 / 0.0835 | pass (bracket) |
| gas-traced | 4.564, -0.0001 / 0.0985, +0.080, +0.023, -0.092 | 4.130, -0.0000 / 0.0995 | pass on the line (bracket) |

- **The DOORS clue, refined.** Objects that trace the stars are too concentrated. They overfill the core (-0.07) and leave
  0.25-0.75 R500 short (+0.07 to +0.09). The extra mass lies between the gas and the stars, and its shape is closest to the
  HSE mass profile.
- **Groups** (graded on the all-inside-R2500 shape) pass 11 / 9 of 20 (canonical) and 10 / 8 (alt), against the 16 needed:
  **FAIL**.
  - The medians are fine: R2500 +0.017, R500 -0.010 (canonical, f* 0).
  - So the miss is scatter between groups at one F per class, not a radial shape miss.
  - Gas-traced groups repeat DOORS: 4 / 3 of 20, with R2500 short by +0.12 and R500 over by -0.15.
- **Bullet**, with the objects on the galaxies at eta_X 29.7 / 26.9 times the stars (the X-COP stellar fit): **FAIL** on both
  footings.
  - M300 is 2.55 / 1.91 e14 (Z -1.81 / -1.13), and dkappa turns positive (+0.064 / +0.049).
  - But the subcluster's lens peak stays nearer its gas: d_gal 114 kpc against d_gas 45 kpc.
  - This is the same failure as DB1 P3 and PB3.

## MUTATE (`na2_MUTATE.json`): all hold or bite, both footings

| Twin | canonical | alt | |
|---|---|---|---|
| M1 planted star-traced truth F = 3 | fit 3.0000, gate PASS | 3.0000, PASS | HOLDS |
| M2 planted gas-traced truth | star fit 1.484, rms 0.170, bins -0.124, +0.081, +0.171: FAIL | 1.486, 0.167: FAIL | BITES |
| M3 planted rule (key M_b) | 0 / 0 empty bins | 0 / 0 | HOLDS |
| M4 planted x10 on hot classes | 3 / 3 empty bins | 3 / 3 | BITES |
| M5 M_c 1e9 | UDG t_heat 2.6e-4, M31 t_DF 2.9e-6 | 3.0e-4, 2.6e-6 | BITES |

## Compute

- Main process peak RSS is 262 MB and MUTATE is 204 MB. Each run takes about 16 s on one thread at nice 15.
- **The Bullet child, which runs DB1/UX6 read-only, peaks at 1188 MB.** That is over the 1 GB line (see disclosure 1).

## Post-freeze disclosures

1. **RSS.** The first main run did the Bullet in-process and peaked at 1341 MB. I moved it into a child process
   (`--bullet-child`) and added RSS logging by stage. The child alone still peaks at 1188 MB, because DB1/UX6's Bullet maps
   are fixed read-only code. The line was exceeded three times, about 10 s each. No graded number changed between the runs.
2. **The X-COP points stop at 0.7 R500,** so only three r/R500 bins are graded. The 0.75-1.0 and 1.0-2.0 bins are empty.
3. In (c), nu uses g_N from (1 + F) M_b/2 for dwarfs and UDGs, and from the enclosed (1 + F) M_b for X-COP and groups. The
   criteria did not say which. rho_cbo = F M_b / 2 over the sphere of radius r for every class, as frozen.
4. In (b), KiDS is left out (its interval covers the whole F grid, so it adds no constraint). In the per-star convention,
   f_* = 0 (f* 0 groups) is clamped at 1e-3.
5. **The bright M31 need (1.64 / 1.50, ST1) closes the window.** SE2's 95 % interval for bright M31 contains 0. Without that
   class the window would be 1e2-1.78e4 (canonical) or 1e2-3.16e4 (alt), limited by the UDGs. This is reported, not graded,
   and it does not change the label: the rows fail at every M_c.
6. **Push method.** The temp-worktree checkout filled the disk ("No space left on device"). I aborted it and removed it.
   Instead I replayed each commit onto origin/main through a temporary index file (git read-tree / update-index /
   commit-tree, no checkout), then ran `git push origin <sha>:main`. The content is the same as a cherry-pick. No rebase,
   force or history rewrite.
7. The literature inputs are PROVISIONAL and recalled, as in DB1/PB2/PB3: Omega_b h^2, the area brackets, t_H, and the DB1
   census range.

## What this door says

- A late-formed compact baryonic population is not killed by the budget or by X-rays, and the PBH walls do not apply to it.
- It still fails as the hot-system cause, for three reasons:
  1. Shape. Objects tracing the stars overshoot X-COP's centre; the needed profile is HSE-like, between the gas and the stars.
  2. Group scatter at one F per class.
  3. The Bullet, where the subcluster peak stays on the gas.
- No single formation rule gives the 72-104x spread, because the UDGs and the SPARC dwarfs share every formation-native key.
- The bright M31 dSphs' dynamics leave only 1e2-1.8e2 Msun of DB1's black-hole window, and no channel is known that makes
  that many 100 Msun dark objects without stars or metals.
- The CMB wall is untouched and stays separate.

Kappa = 1/2 FITTED; not theory closed.
