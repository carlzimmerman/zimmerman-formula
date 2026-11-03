# DB1_cluster_dark_baryons: NO CBDM READING PASSES. Every arm FAILS on both footings: the gas-shaped one passes X-COP and fails keys (3/15) and groups; the tracer and cooling-flow ones fail X-COP's shape; the requirement reading (BK2's I5 amount, placed on the galaxies) gets 14/15 keys and still fails the Bullet. Physically, cold clouds have no window (closed by a factor 3.7); only massive black holes pass my five order-of-magnitude gates, with no known way to make them

Criteria `FROZEN_CRITERIA.md` (9869ad8323), committed alone before any script or number. Scripts `db1_core.py` (the rule), `candidates/` (one module per arm), `db1_acc.py` (runs RQ3's `acceptance.py` unedited), `db1_fast.py` (checks, lambda fit, X-COP, groups, own Bullet, MG1 rows, label control, MUTATE), `db1_phys.py` (physical gates), `db1_k1keys.py`, `run_db1.sh`. RQ3's `tolerances.json`, `row_marks.json`, `old_gates.py` are byte copies.

**Not blind.** kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 are reported apart, never pooled. No LCDM input. Ordinary baryons only; no new particle. The cold sector (cold dark energy) stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

**Source.** Milgrom's CBDM paper is arXiv:0712.4203, not 0801.3133 as the brief had it (that is a different Milgrom paper). Abstract only, PROVISIONAL: CBDM "similar to that in hot gas", more concentrated than the gas, form open from "very massive black holes to cool, compact gas clouds". The forms are my fixed readings. In all of them, CBDM is ordinary mass that the law acts on: g = law(g_b + g_cb).

## Verdict table, per arm and footing (canonical / alt)
The law alone, for reference: X-COP +0.467 / 0.476, keys 10/15, B1 PASS, B2 FAIL +3.71 / +3.32, Bullet FAIL (M300 1.11, 0.73; dkappa -0.068, -0.111).

| | P1 tracer | P1G gas-shaped | P2 cooling core | P3 requirement |
|---|---|---|---|---|
| lambda (FITTED, X-COP mean 0) | 2.06 / 1.86 | 4.82 / 4.36 | 14.9 / 13.4 | none |
| M_cb/M_gas at 300 kpc (X-COP median) | 5.1 / 4.6 | 4.8 / 4.4 | 7.2 / 6.5 | 5.4 / 4.8 |
| X-COP B23 mean | 0 (fit) | 0 (fit) | 0 (fit) | -0.013 / -0.005 PASS |
| X-COP B24 rms, line 0.10 | **0.117 / 0.109 FAIL** | 0.099 / 0.100 PASS (on the line) | **0.178 / 0.164 FAIL** | 0.093 / 0.092 PASS |
| X-COP B25 | **FAIL +2.40 / +2.05** | PASS +1.85 / +0.82 | **FAIL +3.10 / +2.68** | PASS +1.25 / +0.59 |
| Keys B4-B18, of 15 | **5 / 4** | **3 / 3** | **10 / 8** | **14 / 14** (G-OUT-all -2.37 / -2.62) |
| B19, B20 | FAIL, FAIL | FAIL -8.3, p 1e-53 | FAIL (B19 passes alt) | PASS, PASS (p 0.59 / 0.41) |
| Groups B1 | **FAIL +2.08 / +2.53** | **FAIL +3.82 / +4.21** (over) | PASS (= law, not computable) | PASS -0.31 / +0.31 |
| Lovisari B2 | FAIL +2.04 / PASS +1.78 | FAIL -2.80 / -2.99 (over) | FAIL (= law) | FAIL +3.66 / +3.39 (law's own fail, unchanged) |
| Own Bullet | **FAIL**: M300 2.77, 1.34; sub dkappa -0.042 | **FAIL**: M300 3.55, 1.77; sub dkappa +0.007 / -0.002 | **FAIL**: M300 2.53, 1.62; sub dkappa +0.004 / -0.008 | **FAIL**: main M300 4.84, Z +2.54 (over); sub dkappa -0.004 / -0.017 |
| MG1 primary GAL rows, dkappa > 0 | 8 of 8 | 8 of 8 | not computable (no T) | 8 of 8 |
| Label | **FAILS** | **FAILS** | **FAILS** | **REQUIREMENT MISSES** |

Overall RQ3 reads REJECTED for every arm, as expected: the law's own failures elsewhere (planets, dwarfs, IC 1613, lensing A30) stay exactly as they were.

**SPARC and everything outside hot gas is untouched.** Every non-cluster row (A1-A30, C1, the elliptical, TDG, UDG and globular rows) is identical in the harness output to the lambda = 0 run for all four arms. That holds by construction: CBDM attaches to hot X-ray gas, and SPARC's gas is cold HI. Hot coronae of spirals are a real exception the rule ignores. NGC 891 is in SPARC and has a detected hot halo, and the Milky Way's corona of a few 1e9 Msun inside 50 kpc (PROVISIONAL, from memory) would add about 2e10 Msun of CBDM at lambda 4.8. That raises V(50 kpc) by roughly 5-7 %, at the edge of what the Milky Way's curve allows. This is a hand estimate, not graded.

## What it says, plainly
- **Shape.** Mass that follows the gas radially (P1G) fits X-COP, on the line. The same shape over-masses the outer shear keys hard (G-OUT -5 to -15 sigma) and the groups. Mass that follows the galaxies (P1) is too concentrated for X-COP and still over-masses the outer keys. A core deposit (P2) can't make X-COP's outer rows without overshooting its inner ones. Every fixed form tried here repeats MB1's split.
- **Amount.** Clusters need CBDM about 4.4-5.4 times the hot gas inside 300 kpc on this law, against Milgrom's "similar to the hot gas". The expectation on record was lambda 3.5-4.5 for P1G; it came out 4.4-4.8.
- **P3 is the instructive row.** Give the CBDM exactly the amount and radial shape BK2's I5 row needs, and keys go to 14/15, X-COP and groups pass. But **the Bullet fails anyway.** The main subcluster gets too much mass (4.8e14 against 3.5e14). The bullet subcluster, which has little gas for its stars (5.8 times the stars against 16.7 for the main), gets too little CBDM to pull its lens peak off its gas. So no gas-proportional amount fits both subclusters. Placement on the galaxies fixes the sign in MG1's pair model (8 of 8, as MG1 said any galaxy-tied mass does), but the full UX6 map is what decides, and it reads FAIL.
- **Label control.** P1 with the X-COP clusters' gas/star ratios shifted by one gives rms 0.1170 against real 0.1167: **AMOUNT NOT INFORMATIVE.** Larger shifts give 0.124-0.134. In the Bullet, swapping the main and sub ratios also FAILS (sub dkappa +0.094, main -0.011).

## Physical existence (`db1_phys.out`). Order of magnitude; literature inputs PROVISIONAL, most from memory
Governing case P1G canonical: M_cb(<300 kpc) 4.9e13 Msun, mean column at least 0.036 g/cm^2 (N_H 1.6e22), rho_cb 2.9e-26 g/cm^3.
| Gate | Need on cloud column Sigma_c | Basis |
|---|---|---|
| (a) X-ray absorption | diffuse excluded (1.6e22 against 2e20); grey clumps with f_c <= 0.1 need >= 0.36 g/cm^2 | N_H limit about 2e20, PROVISIONAL |
| (b) Bullet, swept column x 3; self-gravity against rho v^2 at 4700 km/s | >= 0.17; >= 0.24 | UX6's central gas, n_e 9e-3 |
| (c) conduction, saturated over 1/H0 | >= 0.66 (0.0066 if suppressed 100x) | Cowie and McKee 1977 form |
| (c) cloud-cloud collisions over 1/H0 | **>= 1.30** (sigma/m <= 0.77 cm^2/g) | rho_cb, sigma_v 1000 km/s |
| (d) not a microlens: Sigma_c < Sigma_cr | **< 0.35** | D_eff 1 Gpc |

**The cloud window is closed by a factor 3.7.** Collisions alone close it; suppressing conduction changes nothing. P1, P2 and P3 give 4.0, 5.4 and 4.2. A cloud at the lower edge at 2.7 K is a 8e-4 Msun, 42 AU object with a free-fall time of 1.7e3 yr, so it would make brown dwarfs or stars unless something holds it up.

| Class | a | b | c | d | e | Result |
|---|---|---|---|---|---|---|
| Sub-critical cold H2 clouds | fail | fail | fail | pass | pass | does not survive (window closed) |
| Super-critical clouds | pass | pass | pass | **fail** | pass | caustic-crossing microlensing, 1e-5 to 1e2 Msun (Oguri+2018, arXiv:1710.00148, qualitative, PROVISIONAL); CBDM is 50 % of the core mass against a 10 % reading |
| Sub-Earth H/He bodies | pass | pass | untested | pass | pass | NOT ESTABLISHED: sublimation not computed |
| Jupiters, brown dwarfs | pass | pass | pass | **fail** | pass | microlensing range |
| Stellar remnants | pass | pass | pass | **fail** | pass | microlensing, and progenitors' metals about 25x the ICM's (PROVISIONAL) |
| **Massive black holes, 1e2 to about 1e7 Msun** | pass | pass | pass | pass | pass | **passes my gates.** Above the caustic range. Galaxy heating is reached only at 1.4e9 (sigma 200 km/s) and 8.7e7 (50 km/s). Bondi-Hoyle L about 3e42 erg/s at 1e6 against core L_X 1e44-45. **No known channel turns about 5 times the hot gas into black holes without stars or metals. Millilensing and dynamical effects at the high end are not computed.** |

(e) Budget, raw data only: BBN with D/H, Omega_b h^2 0.02166 (Cooke+2018, PROVISIONAL, from memory, no Planck). If hot cluster gas holds 4-10 % of cosmic baryons (PROVISIONAL census range), CBDM in clusters alone is 19-54 %. FRB dispersion measures check the ionized total only to about +-40 % (Macquart+2020, from memory), so this reads pass within errors only, which is weak. Groups, if they carried the same lambda, would add more; B1 already fails there.

**The physical answer:** no cold-baryon class Milgrom's abstract names (clouds, dim compact objects) survives. Only the other end he named, very massive black holes, passes these gates, and nothing in hand makes them.

## Checks (`db1_checks.out`, `db1_k1keys.out`, rerun after the fix below)
- **K1 PASS.** At lambda 0: X-COP equals the law to 0 (canonical +0.4675, 0.4763); B1 the same; Bullet M300 1.112e14, 7.34e13, dkappa -0.068, -0.111; key Z's against RQ3's cached law keys to 3.1e-15. Every non-cluster harness row matches the lambda 0 run.
- **K2 PASS** 2.2e-16. **K3 PASS:** replica mean equals the harness's to 1e-12, planted lambda 3.0 recovered at 3.0000. **K4 PASS:** onBCG PASS, onGas FAIL. **K5 PASS:** grade rerun byte-identical (`cmp`).
- **MUTATE bites.** P1G's CBDM on the gas: Bullet FAIL, dkappa -0.186, -0.350 (canonical), exit 1. MG1 rows: 0 of 8 positive, exit 1.

## Disclosures, read as hard as a pass
1. **Bug found after the first harness read.** In `db1_core.py`'s key path for P1 and P2, an interpolation in natural log was raised to base 10. The key rows came out -inf/nan and P2's harness crashed (OverflowError). The fix was to change `10 **` to `np.exp(...)` in two places. The X-COP, groups, Bullet and MG1 paths don't use those lines, and their numbers predate the fix and stand. P1 and P2 harness runs were redone with keys caches cleared. The broken outputs are kept in `results/buggy_keys_path/` (stdout only).
2. **Gate (e) wording.** Before `db1_phys.py` first ran, I changed its class flag from "marginal" to "pass within errors" and said so in the output. The criteria's text for (e) didn't say how to grade "inside errors".
3. P1G's X-COP rms of 0.099 / 0.100 sits on the 0.10 line, so its pass is thin.
4. P2's cooling time uses the frozen Lambda = 3.0e-27 sqrt(T) on n_e n_H. That reads about 2x shorter than Sarazin's textbook t_cool, so r_cool (median 0.14 r500) is on the large side, which favours P2. P2 fails anyway.
5. Physical-gate literature numbers are PROVISIONAL. Oguri+2018 was read as an abstract only; the 10 % reading is mine. The N_H limit, Cooke's Omega_b h^2, the census shares, Macquart's errors, the Bullet temperatures and the metal yield are from memory, not looked up.
6. Harness runs, two at a time with keys, ran under a machine load near 23. Peak RSS of a keys driver was 0.71 GB.

## Limits
Static and spherical in relaxed clusters, Plummer maps in mergers. The CBDM's velocity structure and equilibrium aren't modelled. X-COP is DISPUTED HSE, keys use HSC 1.7, and the Bullet sigma is PROVISIONAL. The physical gates are order-of-magnitude and use one governing core. Spiral coronae aren't in the rule.

## Unfinished
- Millilensing and dynamical limits on 1e2-1e7 Msun black holes as about 50 % of cluster cores.
- H/He snowball survival.
- Spiral-corona rows graded, not hand-estimated.
- A literature check of the PROVISIONAL inputs.

None of these can rescue a form: every arm already fails a cluster gate.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired; nothing here reinstates it.
