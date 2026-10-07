# CFG396 FROZEN CRITERIA: the "two-regime" rule in the CFG361/366/372 PM engine (does it close large-scale growth without CFG372's gas-temperature dependence?)

Committed alone, before any script or result. kappa = 1/2 FITTED and fixed. Both footings (9.3603e-11, 1.1312e-10 m/s^2),
never pooled. nu_mono. No dark-matter particle species: the cold fluid MASS is required and its amount is free. No knob
scans, no new constants. Never "theory closed"; never "data favour the framework over LCDM".

## The rule under test (declared exactly)
Motivation (X-COP, reported elsewhere): the mass beyond the law in clusters is more concentrated than the law's phantom.
Rule: where the local cold-fluid density already exceeds the law's phantom target, the fluid is ordinary collisionless
cold matter and the phantom adds nothing; where rho_cold < rho_ph the phantom acts as the settling target and the extra
source is capped at (rho_ph - rho_cold).

In the engine's code units (s = 1.5 Om rho/rho_bar_m / a; CIC-deposited cell densities, the engine's own smoothing):
- s_ph = -div[(nu_mono(y) - 1) g_N,b]   (baryon-only phantom, unfiltered: NO gas temperature, T = 0 path);
- s_c  = 1.5 Om (1 - f_b)(1 + delta) / a (the local cold density, as the engine already computes it);
- **two-regime extra source = f * max(0, s_ph - s_c)**, f = the engine's T1 bound-region switch ("bound/cell-local");
  the Newtonian term (cold + baryons) is unchanged; k = 0 mode dropped as in CFG361.
- Gravitating dark source in a bound cell is therefore s_c if s_c >= s_ph, and s_ph if s_c < s_ph.

## Step 0: identity gate (FIRST, before any PM run)
Read from the committed engines: CFG361's T5 is `extra = fsw * max(s_ph - s_c, 0)`; CFG366's RES is T5's
e = fsw * max(s_ph - s_c, 0) minus its Gaussian-catchment average; CFG372 = RES with a gas-filtered g_b. CFG366's
"literal local min rule" (dark <= cold present, added on top of the Newtonian cold) adds 0 = S0; it is NOT this rule.
- **G0 (algebra):** state whether the two-regime extra equals T5's extra term for term.
- **G1 (field-level, numeric):** on CFG361's T5 FLAT canonical z = 0 snapshot (read-only, deposited 128^3), compute the
  two-regime source from an independent implementation (explicit regime masks: zero where s_c >= s_ph, s_ph - s_c
  elsewhere, times f) and compare with the engine's T5 force path (CFG372 engine copy, TGAS = 0, imported read-only). PASS
  = max |force difference| <= 1e-5 x the T5 extra-force scale, on both footings. Non-vacuity: the phantom regime must hold
  > 0 ON mass and the cold regime must be reported (mass fractions).
- **Decision of Step 0:** if G0 and G1 both say identical, the two-regime rule IS CFG361's T5. Then **STOP: no PM rerun**
  (rerunning an identical source with the same engine, seed and resolution reproduces CFG361's JSONs). The verdict is
  inherited from CFG361's committed T5 A0-FLAT 256^3 numbers (read from its committed _results.json), scored with
  CFG361's cuts below, per footing. If not identical, the runs below are made.

## Runs (only if Step 0 says NOT identical)
TR (two-regime) A0-FLAT x {canonical, alt}, 256^3, seed 359, L = 200 Mpc/h, 150 KDK steps, T_gas = 0 (no filter).
S0 = CFG359's 256^3 JSON, read-only. If a 256^3 run would exceed ~3 h, use 128^3 and rerun CFG372's T = 1e6 K case at
128^3 as the like-for-like comparator (declared now).

## Decision (CFG361's cuts verbatim; ratios to S0 at z = 0; per footing; never pooled)
- **GROWTH OK:** |sigma8 ratio - 1| <= 5% on BOTH footings AND max over k <= 1 h/Mpc of |P ratio - 1| <= 10% on both.
- **TENSION:** the sigma8 shift is in (5%, 20%], or the P shift is > 10% with sigma8 within 20%.
- **FAIL:** the sigma8 shift is > 20% on either footing.

## Controls
- **C1 (reproduction):** the CFG361 T5 FLAT ratios used for the verdict are re-derived from CFG361's work JSONs and
  CFG359's S0 JSON (read-only) and must match CFG361's committed _results.json to 1e-6 (sigma8 ratio and max |P - 1|).
- **C2 (gate forced open, direction):** the rule with the regime gate disabled (no cold comparison: extra = f * s_ph =
  CFG359's ADD) must over-build MORE than the gated rule, from CFG361's committed numbers (ADD sigma8 ratio > T5's, both
  footings). The spatial gate forced open (f = 1 everywhere, CFG361's S1T5) is reported alongside.
- **MUTATE** (CFG396_MUTATE=1, writes _MUTATE outputs): the regime gate is disabled in the independent implementation
  (extra := f * s_ph). G1 must then FAIL (it is no longer T5) and the run must exit 1.

## Scope
Gravity-level bookkeeping on a collisionless PM run; cell-level comparison at the mesh scale (0.78 Mpc/h at 256^3); no
hydrodynamics; the cold fluid is not moved by the rule. The cold fluid is still required. kappa = 1/2 is fitted.
Local compute only. No downloads.
