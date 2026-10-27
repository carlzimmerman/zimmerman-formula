# CFG361 FROZEN CRITERIA: CFG359's nonlinear PM growth test redone with B's own dark-mass bookkeeping

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle: the cold MASS is
still required and is kept ("cold fluid"). No knob scans. Never "theory closed".

**Why.** CFG359 (criteria ab965b387, Amendment 1 a3064af84) sources gravity ADDITIVELY in switched-ON cells:
baryons + cold fluid + f * phantom. Its T1 A0-FLAT sigma8 ratio to the Newtonian control is 1.58 (canonical) / 1.65 (alt)
at z = 0 (FAIL as frozen there). Additive double-counts relative to B's committed bookkeeping. Owner decision
(2026-10-06): "run the correct test with my bookkeeping".

## The bookkeeping, from the record (quoted)
- **CFG4 T5 (CFG4_README.md, target table):** "**identity**: in a bound region the cold component *is* the law's dark
  density. The dark mass is max(M_ph, (Omega_c/Omega_b) M_b)". Status: "the max rule is **DECLARED**. It adds no constant".
- **Spherical implementations (CFG336/CFG338, `sigma_read`, reading "M"):** `g = gN + max(g - gN, gc)`, i.e.
  g = g_N,b + max(g_ph, g_cold).
- **Reading S (CFG338 FROZEN_CRITERIA line 9):** "S = B's committed rule (CFG35, CFG45 S: f_ex switch); M = CFG4 T5 max
  bookkeeping written locally (CFG45 M); A = additive (diagnostic, NOT B)". CFG35: dark(<r) = M_ph(<r) + f_ex (1 - f_b) M_c
  with f_ex = max(0, 1 - M_ph,edge / [(1 - f_b) M_c]).
- **So the record names S as B's committed rule, and T5 (M) as the target's bookkeeping. They differ** (S uses the
  system's edge phantom total, M compares locally). Additive is "NOT B".
- **Primary = T5-local**, because the owner's 10-06 decision names T5 explicitly. **S gets its own scored verdict**
  (separate, never pooled). The lane reports both; if they disagree, both are stated, neither is chosen post hoc.

## Model: everything identical to CFG359 except the source in ON cells
Engine copied (not imported) from cfg359_pm.py: GR + Lambda background (FP2), L352 parameters (f_b = 0.157), cold +
baryons one pressureless fluid with rho_b = f_b rho_m, nu_mono (L340), phantom sourced by baryons only, the T1 switch
(eps = 0.077, tau = (Delta_ta(z) - 1)/3, MS1 psi relaxation), EH no-wiggle ICs at z_i = 49 (the ONLY LCDM input, CFG324),
seed 359, L = 200 Mpc/h, 256^3 particles on a 256^3 mesh (Amendment 1), 150 KDK steps, same P(k) / sigma8 / FoF machinery.

In code units every density is a Poisson source s = (3/2) Om (rho / rho_bar_m) / a:
- s_ph = -div[(nu_mono(y) - 1) g_N,b] (CFG359's phantom source, unchanged);
- s_c = (3/2) Om (1 - f_b)(1 + delta) / a, the cosmic cold share = (Omega_c/Omega_b) x local baryons;
- the Newtonian part (3/2) Om delta / a is unchanged. Every extra term below has its k = 0 mode set to zero
  (the background is GR's, as in CFG359).

Source options (declared now):
- **T5 (T5-local, PRIMARY):** extra = f * max(s_ph - s_c, 0). In an ON cell (f = 1) the dark source is max(s_ph, s_c).
  - **Negative phantom density:** s_c >= 0, so where s_ph < 0 the max returns s_c and NO negative phantom is added.
    This differs from additive (which subtracts it), and it is disclosed.
- **S (S-region, own verdict):** the system-level rule on the mesh.
  - Regions R = connected components (6-connectivity, periodic) of cells with f > 0.
  - f_ex,R = max(0, 1 - sum_R s_ph / sum_R s_c).
  - extra = f * (s_ph - (1 - f_ex,R) s_c), so the ON-cell dark source is s_ph + f_ex,R s_c.
  - Note: a purely LOCAL f_ex equals T5-local identically, so the region totals are what make S distinct.
- **T5F (T5-force, REPORTED ONLY):** with all fields parallel to g_N in the monopole reading, g_ph = (nu - 1) g_N,b and
  g_c = (1 - f_b) g_N. Then g = g_N + f * max(|g_ph| - |g_c|, 0) g_hat = g_N + f f_b max(nu - 1/f_b, 0) g_N. It boosts only
  where nu > 1/f_b = 6.36. It is a non-conservative field-level analogue and is added as an acceleration.
- **ADD (reproduction control):** extra = f * s_ph, i.e. CFG359's T1.

Runs (256^3 unless stated; same seed, so all ratios are paired):
- T5 x {FLAT, CRIT, DE} x {canonical, alt}: verdict FLAT, separate CRIT, DE reported;
- S x {FLAT, CRIT} x 2;
- T5F FLAT x 2;
- ADD FLAT x 2;
- S1T5 (f = 1 everywhere, T5-local) FLAT x 2;
- MUTATE FLAT x 2;
- T5 FLAT canonical at amp 0.01 (linear test);
- 128^3: S0 and T5 FLAT canonical (resolution).
- **S0:** reuse CFG359's S0_FLAT_canonical_N256 JSON READ-ONLY. Its code path is identical, and the ADD control checks
  the engine copy. If that JSON is absent at analysis time, this engine's own S0 at 256^3 is used.
  The 128^3 S0 is run here.
- At most 4 processes x 2 FFT threads, os.nice(10). Work data goes to ../_external_data/cfg361_work/. No downloads.

## Measurements
- sigma8 ratio and P(k) ratio to S0 at z = 1, 0.5, 0.
- ON fractions (volume-weighted and mass-weighted <f>; ON = f > 0.5).
- The mass fraction of ON cells where s_ph > s_c ("phantom-dominated").
- For S: the number of regions and the mass-weighted mean f_ex.

## Decision (frozen; same cuts as CFG359; per a0 branch; both footings; never pooled)
For the option vs S0 at z = 0:
- **GROWTH OK:** |sigma8 ratio - 1| <= 5% on BOTH footings AND max over k <= 1 h/Mpc of |P ratio - 1| <= 10% on both.
- **TENSION:** the sigma8 shift is in (5%, 20%], or the P shift is > 10% with sigma8 within 20%.
- **FAIL:** the sigma8 shift is > 20% on either footing.

Lane verdict = T5 A0-FLAT. Separate verdicts: T5 A0-CRIT, S A0-FLAT, S A0-CRIT. Reported: T5 A0-DE, T5F, S1T5.

## Controls (frozen pass conditions)
- **K1 additive reproduction:** ADD reproduces CFG359's T1 A0-FLAT sigma8 ratios (1.58 / 1.65; read from CFG359's
  JSONs read-only if present) to |delta ratio| <= 0.01 on both footings.
- **K2 linear:** T5 at amp 0.01. For k <= 0.1 h/Mpc, sqrt(P(a)/P(a_i)) / (D(a)/D(a_i)) is within 1% at z = 1, 0.5, 0.
- **K3 MUTATE** (env CFG361_MUTATE=1, outputs *_MUTATE): T5 with s_c := 0 inside the max only. The extra source becomes
  f * max(s_ph, 0), i.e. additive MOND on baryons without its negative part. PASS if its sigma8 ratio exceeds T5's by
  > 0.01 on both footings (it moves away from T5, toward additive).
- **K4 resolution:** T5 FLAT canonical at 128^3 vs 256^3. PASS if the verdict category is unchanged.
- **K5 monotonicity (reported, with the Lean lemma):** sigma8(T5) <= sigma8(ADD) and sigma8(T5) <= sigma8(S1T5).
  The pointwise source inequality holds only where s_ph >= 0. Nonlinear sigma8 is not guaranteed monotone, so a K5
  failure is reported, not hidden.
- **K6:** the Delta_ta table reproduces CFG354 K4 (11.806 at z = 0, 6.412 at z = 1, to 1%).

## Lean (Lean 4 + Mathlib, no sorry)
- max(p, c) <= p + c for p, c >= 0;
- f max(p - c, 0) <= f p for p >= 0, c >= 0, 0 <= f <= 1 (T5 <= additive pointwise), with the converse inequality
  where p < 0;
- the force analogue: f_b max(nu - 1/f_b, 0) <= f_b (nu - 1) for nu >= 1;
- the measured sigma8 ratios inside stated rational intervals, each on the side of the 5% / 20% cuts the verdict reports.
