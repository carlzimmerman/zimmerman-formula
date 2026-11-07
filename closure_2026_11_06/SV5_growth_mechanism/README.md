# SV5: the growth / CMB-lensing constraint, mapped, and three escape classes. All three FAIL; the wall is the a0 law acting on the linear web

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: any sector here is cold dark energy carried by the action's own
fields; no particle; no LCDM input (QX3's framework-native corner background, raw PR4 lensing, KiDS RAR, SPARC). Footings
canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. QX31 was read, not redone (its "no failure is a data-product
artefact" is taken as given).

- Criteria: FROZEN_CRITERIA.md + iter_*/FROZEN_CRITERIA.md, committed and pushed alone before any script or number
  (local 247d2eaa2f, origin ca352ccb7f).
- Amendment A1 (technical, before any graded number): iter_1_law_on_web/AMENDMENT_A1.md (z = 50 slice uses EdS growth from
  CLASS's z_max_pk = 20).
- Scripts: sv5_common.py (read-only loaders of QX3 iter3, QX7 iter_3's g2gen, QX10 iter_2), sv5_t0_iter3.py, sv5_web.py.
  One thread, nice 15, about 4 + 6 min. Logs run_*.txt; outputs sv5_t0.json/.out, sv5_web(.out, _MUTATE.out), iter_k/*.json/.out.
- Lean: fable_independent_2026/lean_2026/SV5_growth_nogo.lean (15 theorems) and SV5_growth_nogo_MUTATE.lean (4 false claims).
  **NOT COMPILED** in this run: the checkout has no Mathlib build, and unpacking it (`lake exe cache get`, local cache) was refused
  by the session's permission check. No .out is saved; the algebra is stated but uncertified until the owner runs
  `lake exe cache get && lake env lean SV5_growth_nogo.lean` (and the twin).

## 1. The target function (T0, sv5_t0.out)

What a growth mechanism must deliver, from the record's own machinery:

| Piece | Requirement | Source / number |
|---|---|---|
| Lensing source | The Newtonian potential of a cold (dust) component, omega_d 0.112-0.124, on k 0.003-0.6 Mpc^-1, z 0-20 | QX3 iter2 G1 (chi^2 8.2-8.6 vs 18.5) |
| Size of the missing source | R_req = delta_m(dust)/delta_m(sector smooth) ~ 1.4e3 (z 0.5), 1.1e3 (z 1), 760 (z 2), 380 (z 5), 210 (z 10), flat in k for k 0.04-0.6 | solver baryons start at 0 at decoupling, so this is an upper envelope |
| Amplitude precision | sigma_A,rel = 0.024 (PR4, CMB-marginalised covariance). The shape gate alone cannot see a uniform deficit (smooth sector: shape dchi^2 0.3 with a 3e6 power refit); the amplitude is pinned by the primary CMB's A_s (QX15) | T0.4 |
| Gain of the law on the web | must be 1 within 3 sigma_A = 7 % in lensing power | iter_1 |
| Late stiffening tolerated (physical Jeans length lambda_s switched on below z_s) | 1 Mpc only below z 0.75; 3 Mpc below 0.25; 10 Mpc below 0.1; 30 Mpc and up: never | T0.2 (dchi^2 <= 4) |
| Hosts must not retain it | n = 1 end state passes G5/G6/G7 only for lambda_J >= 20 Mpc (both footings; 15.8 Mpc gives KiDS -0.057 / -0.062) | T0.3 via QX10 |
| Primary CMB | cold at z >= 10 (QX15 cold component, omega_d 0.121) | in the solver from z 3400 |

The time-only reading is already a contradiction: hosts need lambda_J >= 20 Mpc at z <= 0.5 (SPARC at z ~ 0, KiDS lenses to
0.5), and growth tolerates nothing above 10 Mpc before z 0.1.

## 2. The three classes

| Iteration | Class | Key numbers (canonical / alt) | MUTATE | Label |
|---|---|---|---|---|
| iter_1 | W: ANY sector delivering the target, with the a0 law on on the linear web (QUMOND on the peculiar field, the action's static equation) | web |g_N|/a0 median 0.013-0.60 (z 0.25-50); lensing amplitude r = **74.7 / 89.4** vs line 1 +- 0.072; B(k) almost flat in k (shape dchi^2 0.0); rigorous floor nu(y_max)^2 = 15.2 / 17.9 at z 1, >= 1.75 at every z | nu == 1 gives r = 1, dchi^2 0: bites | **NO-GO FOR CLASS W** (Lean bound not yet compiled) |
| iter_2 | C: K(Q) Jeans scale switched (any antitone mu_K) by the AC2q charge Sigma = D.P + 2X | Sigma_* (least-charged host at r_ta, UGC02487) = 8.0 / 6.0 rho_DE; web cells above it (mass-weighted) 25 % (z 0.25) to 54 % (z 3), 51 % at z 50, vs line 3.6 %. Median positive web charge 4-836 rho_DE (z 0.25-50). Sun 7.5e4 / 5.8e4 rho_DE (stiff, Cassini inherited) | M1 switch off: G5 4.23 (bites); M2 web charge 0: C2 PASS (bites) | **NO-GO FOR CLASS C** (inside the action) |
| iter_3 | T: lambda_J = F(a0(z)/a0(0)), any F, a0 ~ sqrt(rho_DE) | lambda_host 20 Mpc. H-flat: F constant, dchi^2 544. H-native (CFG689): a0 bump to 1.12 at z 0.7, host image [1.000, 1.054], so M* is stiff on z 0-0.88: dchi^2 877; best power law (q +3) 301. H-CPL (reported): 781; best 109 | M1 F == dust: G5 4.23, KiDS -0.37 (bites); M2 F == 20 Mpc: 544 (bites) | **H-flat NO-GO FOR CLASS; H-native FAIL** (K-mono failed: extra stiffness at z 1-2 LOWERS dchi^2 to 542, the amplitude-refit non-monotonicity QX27 noted, so no class claim); CPL FAIL (reported) |

Checks: iter_1 K1 realisation power 0.987, PASS; K2 (a0 x 1e-8) |B-1| 7e-7, PASS; K3 seed 6 at z 1 B 41.2-43.7 (seed 5:
41.3-44.2). iter_2 K1 deep-MOND point-mass phantom ratio 1.0000, PASS; C1 host charge monotone in r on every host.

## 3. What the map says

1. **The wall is not the sector. It is the law on the web.** The action's static equation is the a0 law everywhere g < a0, and the
   linear web sits at 0.01-0.2 a0 in the lensing epoch. A sector that supplies exactly the needed Newtonian source is boosted 75-89x
   in lensing power. The Lean statement (Cauchy-Schwarz through QUMOND's projection) is that the integrated gradient power is at
   least nu(y_max)^2 times Newton's, so no member of W can sit within 7 %. WG2's 11-14x (baryons only) is the same effect at a
   lower source.
2. **A charge switch cannot separate hosts from the web inside the action.** The same law-on phantom that boosts the web also makes
   its charge large: a quarter to half of the web's mass sits above the least-charged host's turnaround charge, and the early web's
   median positive charge (z >= 8) is 10-100x the least-charged host's charge at r_ta. That is QX3's density ordering again, now for the khronon charge.
   Conditional only (A-web: law off on the web, which is NOT in the action): Sigma_web = 2X <= 2 rho_DE < Sigma_* = 6-8 rho_DE, so
   C2 would pass. That is reported, not a pass.
3. **Tying the coupling to a0(z) cannot work.** a0 hardly moves at z <= 1 (and on the native and CPL histories returns to today's
   value near z 0.9, Lean `ivt_crossing`), so whatever stiffness hosts need today is also on through the lensing peak. The time-only
   tolerance (<= 10 Mpc, only below z 0.1) and the host need (>= 20 Mpc by z 0.5) do not overlap for any clock switch.
4. **So the escape now needs two switches, and the first is the law's.** The law's phantom must be off on the linear web (gain <= 1.07
   in lensing power) while staying on in galaxies out to the KiDS 3 Mpc. Only then does a sector switch have room: in that branch
   the charge (6-8 rho_DE at host turnaround vs <= 2 rho_DE on a law-off web) separates hosts from the web. No such law switch is
   in the action, and none was tested here. WG6's by-hand Yukawa screening of the phantom is the record's only try.

## Not done / not evaluable

- Lean files not compiled (see above).
- iter_2 expulsion dynamics (does the stiffened sector actually leave r_ta, and on what time scale): NOT EVALUABLE, not run. C3
  (G5/G6/G7) passes only by QX10's convention.
- The web is a 128^3 / 2000 Mpc Gaussian linear field. Finer cells raise the web's charge peaks, so iter_2's F is a floor.
- c_T for iter_2 and Cassini beyond the stiff-Sun check are ARGUED, not graded.
- The iter_2 MUTATE print shows F_0 = 1 and NaN medians when the web charge is zeroed: cosmetic, no label uses them.
- The `.lake/packages` sources (677 MB, git-ignored) that the first `lake env lean` cloned are left in the checkout for the
  owner's compile.
