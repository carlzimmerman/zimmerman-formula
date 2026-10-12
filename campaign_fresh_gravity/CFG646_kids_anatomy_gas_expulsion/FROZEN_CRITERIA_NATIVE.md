# CFG646 (iii) FROZEN CRITERIA + PM spec: a native CFG596 run WITH the framework's own census gas expulsion

Status: FROZEN, NOT RUN. Written 2026-10-12, after the CFG646 estimates (disclosed: the expected size is known, see
README.md); committed alone before any engine code for it. No PM >= 256^3 is run in this lane.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy MASS still required; no particle species;
not "theory closed". No LCDM or standard-MOND yardstick enters any verdict; the S0 arm is CFG596's frozen same-pipeline control.

## 1. Physics being added (framework-native, zero new constants)

- The census (CFG416/515 fret_of, verbatim; the engine's own uint8 f_ret code and table) retains M_b = f_ret f_b M_ta per
  catchment. CFG596's engine already feeds only the retained baryons, tab[code] (1 + delta), to the MOND input. But its
  Newtonian source is the FULL particle density, so the non-retained baryons f_b (1 - f_ret(x)) (1 + delta) still gravitate
  as collisionless mass inside every catchment. That is the omission.
- The framework places that gas outside the halo: CFG632 PRIMARY DIFF (the census gas the raw FRB DMs accepted). It has no
  one-halo profile, keeps its host's large-scale bias, and conserves mass.

## 2. Engine (cfg646_pm.py = a copy of cfg596_pm.py; one new switch EXPEL, default OFF)

- EXPEL=OFF: no new line executes. The code path is byte-identical in effect to cfg596_pm.py.
- EXPEL=ON, in forces() for switch RES, after the census / catchment refresh (same cadence: every 10th call, and the
  diagnostic snapshot call):
  1. e(x) = FB * (1 - tab[code(x)]) * (1 + delta(x)) on the catchment cells. Code 0 means tab = 1 and e = 0, so halos below
     the resolved catchment mass get no expulsion. That is disclosed: CFG646's halo model shows resolved-only and all-mass
     DIFF agree to <= 0.003 in P'/P at k <= 2.
  2. Placement, PRIMARY DIFF-S: for each catchment class kc (one catchment radius R_kc per code), e restricted to code == kc
     is convolved with a unit-normalised Gaussian of sigma = R_kc. The sum is renormalised to sum(e). Brackets, each a
     separate run: DIFF-U (uniform), SHELL (each connected catchment's e goes into its own shell cells, catchment AND NOT
     census edge, weighted by 1 + delta; a catchment with no shell cell keeps its e in place, and that fraction is
     reported).
  3. Newtonian source: delta -> delta - e + place(e) in _finish_phik's (-1.5 Om / a) delta_k / k^2 term ONLY. The MOND input
     (already retained-only), the switch f_sw, s_c, the edge, the shell draw, the cap and the time steps are unchanged.
  4. Particles carry no tag. The relocation acts on the gravitating weight: particle P(k) stays a diagnostic, and the scored
     spectrum is the gravitating P(k) (CFG555 definition, as in CFG596).
- Memory: e and place(e) are disk-backed DFields (SPILL), with at most one extra full mesh field alive. Gate V-M is
  peak RSS <= 50 GB at 1024^3, with CFG596's watchdog (RSS 50 GB, swap +4 GB, disk 3 GB) unchanged.

## 3. Gates (all before production; all at <= 256^3 except V-M)

- **G-R reproduction (EXPEL=OFF, bit for bit vs CFG596):**
  - exact mode RES L200 N256 must equal CFG596's VEa outputs: P, sigma8 at every snapshot, z = 0 positions, q_max,
    n_catch, e_sum, src_sum, all identical.
  - lean mode RES L100 N256 (NSEED 512) must equal CFG596's VLr outputs, identical.
  - Any difference -> STOP.
- **G-0 null tooth:** EXPEL=ON with tab forced to 1 (e = 0) must be bit for bit with EXPEL=OFF.
- **G-M mass:** |sum(place(e)) - sum(e)| <= 1e-6 sum(1 + delta) at every refresh; the sum of the Newtonian source is
  unchanged to <= 1e-6.
- **G-E estimate consistency (reported, no verdict role):** at 256^3 L100 (smoke), the z = 0 gravitating P'/P at k 0.3 / 0.5 / 1
  is compared with CFG646's post-process DIFF-S ratio of the same run's EXPEL=OFF fields. A difference > 0.03 is disclosed
  as back-reaction, not as an error.
- **V-M:** a 1024^3 three-step probe as in CFG596.

## 4. Production and scoring

- Run RES-EXPEL canonical, L100 N1024, NSEED 1024, SEED 359, RMIN 0.78125, lean mode, snapshots and extras exactly as CFG596
  P1. The alt footing is run only when CFG596 P2 exists (same seed).
- Score with cfg596_native.py UNCHANGED, with the new run in place of P1 (a path argument only), against CFG596 P0 (S0, the same
  realisation). Everything else is unchanged: statistic dchi2(F - S0), support cut f >= 0.9, nuisances, robustness set
  {widen2, noIA, held, DESI}, klass, and T-OWN taken from CFG596's MUTATE JSON. KiDS canonical passed T-OWN (16.4); DES
  failed it (2.4), so DES stays NOT DIAGNOSTIC.
- Verdict per survey x footing: CFG592/596 klass (EXCLUDED if dchi2 >= 9 and every robustness variant >= 9; TENSION if
  dchi2 >= 4; CONSISTENT if dchi2 < 4 and max robust < 9; else NOT DIAGNOSTIC). chi2(F) with its p on the raw data is reported
  beside it.
- Brackets (DIFF-U, SHELL) are reported, with no verdict role. If the PRIMARY and either bracket fall in different classes,
  the label is suffixed "(placement-sensitive)".
- Pre-registered expectation (CFG646 estimate, not a criterion): KiDS canonical dchi2 about +52 (DIFF-S), +36 to +62 over all
  placements. A result outside +30 to +70 is reported as a back-reaction finding and investigated before it is quoted.

## 5. MUTATE

- M-E0: tab = 1, which reproduces CFG596 P1 bit for bit (G-0 at production scale is NOT required; it is shown at 256^3).
- M-Eall: f_ret = 0.10 for every catchment (maximal expulsion within the engine). Its dchi2 must move further than the
  PRIMARY's, or the switch does not bite.

## 6. What this run can and cannot decide

- It decides whether CFG596's canonical KiDS exclusion survives the framework's own expulsion, including the PM
  back-reaction that the post-process estimate cannot see.
- It does not test the condensed-baryon source (CFG634 H-CB) or any change to the settling rule.
- Cold energy settles by candidate B's supply rule, not by following the gas.
