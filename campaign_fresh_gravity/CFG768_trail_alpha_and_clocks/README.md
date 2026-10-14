# CFG768: the NGC 1052 trail with alpha from the record's own physics — the framework's assembly does NOT reproduce it

**Label: A = OTHER as frozen (alpha_P = 0 derived under one c_P; no bracket point splits debris from LEDA); B = EXCLUDED for
both clocks, both footings (the old debris are overfilled). MUTATE bites (exit 1).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (35f781ce3), 2026-10-14. Block CFG760–769.
- **Script:** `python3 cfg768.py` (seconds) → `cfg768.out`, `cfg768_results.json`. `CFG768_MUTATE=1` → `*_MUTATE.*`, exit 1.
  CFG657's capture code is exec'd from its file text (no edits); CFG762's SPARC c_P,min read from its json.
- **Settings:** κ = ½ FITTED; no-EFE ν_mono (CFG655 frame); L* = 5.754 pc; the cold energy's mass is required; no particle species;
  not "theory closed".

## Part A: alpha from P-wave dissipation
- Every trail galaxy has its **own** P-export window (c_P ≈ 57–535 m/s), as CFG761 hinted for dwarfs.
- **One c_P closes it:** SPARC needs c_P ≥ 7674 m/s (CFG762); the best trail c_P,max is 487 / 535 m/s (can / alt). With one
  c_P for every system, P waves cannot dissipate drift energy in the trail ⇒ **alpha_P = 0** (conditional on one c_P).
- With alpha_P = 0 the drift channel D (which carried > 99% of CFG657's capture) vanishes. At primary inputs S + F gives
  4e-4–1.6e-3 for all four: debris pass, **LEDA unsupplied** (needs ≥ 0.23 / 0.20).
- **As frozen the label is OTHER, not LEDA UNSUPPLIED:** at two bracket ends (progenitor M_b,p = 1e10, and V_coll = 250 km/s
  for DF4/DF9/LEDA) the separation channel falls back to full supply (f = 1) for every galaxy, debris included. Debris and LEDA
  switch **together**; no bracket point gives the observed split.

## Part B: formation at rest (CFG763 universal, CFG764 orbital clocks)
Lenient for the debris (age 6 Gyr, slowest clock, longest orbit), lenient for LEDA (fastest clock, oldest age):

| | DF2 | DF4 | DF9 | LEDA |
|---|---|---|---|---|
| universal f (bound) | 0.82 (≤ 0.36 / 0.33) | 0.82 (≤ 0.29 / 0.26) | 0.82 (≤ 0.52 / 0.46) | 1.00 (≥ 0.23 / 0.20) |
| orbital f | 0.94 | 0.96 | 0.88 | 1.00 |
| Z at that f, can / alt (universal) | −3.97 / −4.27 | −3.93 / −4.18 | −2.66 / −2.83 | −0.74 / −1.07 |
| Z (orbital) | −4.39 / −4.71 | −4.30 / −4.56 | −2.77 / −2.94 | — |

Both clocks fill the debris in ≲ 3.5 Gyr (universal) or ~2 orbits (t_orb 1.6–2.4 Gyr); the debris are ≥ 6 Gyr old, so they should
sit near the law. They are Newtonian. **EXCLUDED at 2.7–4.7σ**, both clocks, both footings. LEDA is fine under both.

## Reading
1. **The framework's own assembly physics does not explain the trail.** Capture (Part A) cannot separate debris from LEDA once
   alpha is tied to P-wave dissipation; formation at rest (Part B) separates them in the wrong direction (everything old fills).
2. **What it teaches.** The old debris are the first available test of CFG763's "every old system fills" prediction, the
   discriminator CFG763 hoped to get from NGC 5557-E1. On the record's clocks the trail says **no**: some ≥ 6 Gyr-old systems hold
   ≤ 26–52% of the law's cold energy. Either formation needs a condition the debris lack (not fitted here; FG001's ownership/
   hierarchy reading is the record's candidate, not scored here), or the label/inputs are wrong (EFE frame, distances, DF4 σ).
3. CFG655's pass therefore stays **conditional on the external label**, and now the label conflicts with the framework's own
   clocks unless a formation condition is added.

## Hand estimates (in the criteria, before the run)
A: LEDA UNSUPPLIED — right at primary, but the frozen bracket rule gives OTHER (fallback ends). B: both clocks overfill the
debris (DF2 universal ≈ 0.83) — confirmed (0.823).

## Not tested
EFE variants (would raise the debris bounds), non-first-order formation, FG001 ownership, formation microphysics (astra F1/F5).
