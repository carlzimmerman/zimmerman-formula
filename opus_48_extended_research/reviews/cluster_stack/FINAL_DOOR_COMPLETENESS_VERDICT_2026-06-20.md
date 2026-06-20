# FINAL-DOOR completeness check — is there a genuine THIRD no-particle ingredient? — verdict 2026-06-20

**Workflow:** `finaldoor` (cluster_stack). After the banked round-2 stack — Route B (full
nonlinear AeST Y-Q field, +17-20% core phantom) + IGIMF stellar remnants + known baryons —
is there ANY remaining no-new-particle ingredient (not in the stack, not in the killed-list)
that could close the post-stack core residual? Four candidates tested both ways against the
four gates (G1 sufficiency, G2 galaxy-veto, G3 no-new-particle, G4 data), on the framework's
own footing (a0=9.36e-11), real eRASS1, sympy/numpy, cited 2024-2026 literature.

## HEADLINE (both ways)

**NO candidate adds a genuine THIRD no-particle channel. The stack (Route B field + IGIMF
remnants + known baryons) IS THE CEILING. Two of the four candidates are STRUCTURALLY DEAD
(lensing≡dynamics by construction; ICL already inside the IGIMF budget), and two are
WRONG-SIGNED (non-equilibrium biases the core X-ray mass LOW; the EFE suppresses the MOND
boost). Best-case honest no-particle CORE coverage is ~59-61% (gas-tracking) to ~80-83%
(galaxy-tracking); ~43% on conservative knobs. The residual ~17-39% (best-case) up to ~57%
(conservative) of the core stays UNCOVERED at full weight — the shared relativistic-MOND open
soft-spot. No third ingredient; no manufactured closure; no reflexive dismissal.**

| Candidate | Verdict | Gate that decides | Core mass added |
|---|---|---|---|
| **(i) AeST lensing-vs-dynamics split** | STRUCTURALLY DEAD | G1 (no split) + G4 (data) | ~0 (slip ≤3%, gap-shrink ~4%) |
| **(ii) non-equilibrium / merging core** | DEAD (wrong sign) | G1 + G4 | ~0 (HSE biases core mass LOW) |
| **(iii) ICL / 2nd remnant population** | SUBSUMED (anti-double-count) | G1 | ~0 fresh (ICL is in the IGIMF budget) |
| **(iv) EFE on the core** | DEAD (negligible / wrong sign) | G1 | ≤0 (EFE deepens the deficit) |

## CANDIDATE (i) — AeST/framework LENSING-vs-DYNAMICS split — STRUCTURALLY DEAD

The cleanest possible third ingredient: if light bent MORE than matter feels, the LENSING
residual would overstate the DYNAMICAL residual a no-DM theory must source, shrinking the
target. **It does not exist**, three independent ways:
- **AeST has NO slip by construction.** FPS (2410.02612) verbatim: *"a dynamical mass
  equivalent to the lensing mass BY CONSTRUCTION, in MONDian gravity"* (under Ψ=−Φ). This is
  a DESIGN requirement — a relativistic MOND theory with lensing≠dynamics fails Bullet /
  solar lensing / GW170817 (c_T=c). So s_AeST = 1.000 exactly.
- **The framework's own γ-slip is the SAME phantom counted once.** The banked predicted slip
  γ = 2√(1+a0/g_N)−1 gives lensing/dynamical ratio s = (1+γ)/2 / √(1+a0/g_N) = **1
  identically** (sympy-exact: γ is DEFINED as 2·μ_dyn−1, so (1+γ)/2 = μ_dyn). The slip is the
  enhancement in BOTH channels — there is no lensing-only mass to subtract.
- **The DATA caps any slip at 3%.** CLASH-lensing core / eRASS1-X-ray(HSE) core = **1.03**
  (two-probe agreement). X-ray (HSE) IS the dynamical probe; it sees the same residual.
- **Both ways:** even granting the FULL 3% slip, the dynamical target drops only 1.357e14 →
  1.317e14 (gap-shrink ~4%); the residual is still ~3.8× the framework's MI phantom. G1 fails,
  G4 is decisive against. **No split to exploit.**

## CANDIDATE (ii) — NON-EQUILIBRIUM / merging-core mass — DEAD (wrong sign)

Cluster cores are not perfectly relaxed; does a dynamical-state correction REDUCE the
equilibrium residual? **No — it is wrong-signed and the target is lensing-anchored:**
- **The SIGN is wrong.** Non-thermal pressure makes the THERMAL HSE mass an UNDER-estimate
  (b = 1−M_HSE/M_true > 0). Lebeau+2026 (A&A aa56598-25) major-merger sims: CORE bias
  b ≈ −0.15 (X-ray reads 15% LOW), and the core relaxes EARLIEST. So disequilibrium makes the
  TRUE core residual ~15% LARGER, not smaller.
- **The target is LENSING-anchored** (CLASH), which is disequilibrium-insensitive. The 1.03
  lensing/X-ray agreement IS the measurement that the core is effectively relaxed for mass
  purposes — a merger that disturbed the mass would break this 3% agreement; it doesn't.
- **Real eRASS1:** rich-bin f_gas500 = 0.095 [0.071, 0.115]; higher f_gas (disturbed gas-rich
  cores) → higher g_bar → SMALLER MOND boost → HARDER target. No escape in the spread.
- **Both ways:** even a GENEROUS granted 15% core deflation (wrong sign, granted as a
  best-case) leaves a ~3.3× undershoot. **No real gap-shrink.**

## CANDIDATE (iii) — ICL / SECOND remnant population — SUBSUMED (anti-double-count)

Is there a separate, not-double-counted reservoir from the intracluster light (ICL) or a
second remnant population the BCG-only count misses?
- **ICL is REAL core mass** (~1.8e12 Msun inside 420 kpc, canonical IMF; total ICL ~30-50% of
  the ~1.3-1.5e13 cluster stellar mass) — but it is **ALREADY INSIDE Route D's IGIMF stellar
  budget.** Route D applies the ~6-8× M/L boost to the TOTAL cluster stellar mass, which
  includes BCG + ICL + satellites. Adding ICL again = DOUBLE COUNT. **The honest fresh
  increment on top of (B+IGIMF) is ~0.**
- **No separate BBN-safe remnant population:** halo white dwarfs are the SAME IMF's low-mass
  tail (double-count) + MACHO-capped (<few %); primordial black holes are NOT stellar baryons
  → if invoked as the dark mass they are a new non-baryonic species (G3 FAILS); cold gas
  clouds are the same BBN-capped baryon census as the gas channel.
- **Both ways:** ICL credited as real core mass, but refused as a fresh stack increment
  (anti-double-count rule honored). **Not a third ingredient.**

## CANDIDATE (iv) — EFE / external-field correction on the core — DEAD (negligible / wrong sign)

Does the external-field effect ADD core phantom?
- **The core is internal-field-dominated.** Across the whole core the baryonic self-field
  (g_int/a0 ~ 0.22-0.34) exceeds a generous external field (0.1 a0) by ~2-3.4×. EFE is
  negligible at the center where the residual is steepest.
- **Where it acts, the SIGN is wrong.** Including the EFE DECREASES the MOND boost → MORE
  missing mass required (Kelleher-Lelli, A&A aa49968-24, verbatim: *"the MOND boost is
  decreased, so more missing mass is required"*). Quantified here: g_ext = 0.1 a0 cuts the core
  phantom by ~21% (DEEPENS the gap).
- **The framework's MI reading agrees:** MI uses the TRUE internal self-field (solitary-MSP
  pulsar reductio forces it), unchanged by the external field at the core; the dS-Unruh
  environmental term was already banked WRONG-SIGNED (hot core a≫a0 → more Newtonian → less
  MOND). **No EFE core enhancement.**

## THE HONEST BEST-CASE STACK (no double-counting), both shape readings

Three DISJOINT no-particle channels (no overlap): Route B AeST Y-Q **field** (+20% on the
phantom) + Route D IGIMF **remnants** (on baryons) + Route A extra **gas** (ICM census).
Candidate (i) applied as a 3%-capped target reduction; (ii)/(iii)/(iv) add 0.

| reading | Route B field | IGIMF remnants (core) | extra gas | TOTAL supplied | CORE coverage | residual (full weight) |
|---|---|---|---|---|---|---|
| **GAS-tracking (FPS)** | 4.21e13 | 3.47e13 | 3.69e12 | 8.04e13 | **~59-61%** | ~5.1e13 (~39%) |
| **GALAXY-tracking (Bullet)** | 4.21e13 | 6.30e13 | 3.69e12 | 1.09e14 | **~80-83%** | ~2.3e13 (~17%) |
| **CONSERVATIVE (ML=6, 50%, +0% gas)** | 4.10e13 | gas-eff | — | — | **~43%** | ~57% |

(Coverage = total no-particle source / core target; the dynamical target with the 3% slip is
1.317e14, the raw lensing target 1.357e14. IGIMF-alone gap-fill = 34% gas / 63% galaxy,
matching the banked ~40-65% core-budget. No gas+galaxy stacking; ICL not added on top of
IGIMF; IGIMF-BCG not added on top of IGIMF-remnants.)

## CEILING TEST — is the stack (B+IGIMF+baryons) the ceiling?

**YES.** No FINAL-DOOR candidate adds a genuine third no-particle channel:
- (i) lensing-vs-dyn slip: a TARGET reduction capped at 3% (data), ~4% gap-shrink — not mass.
- (ii) non-equilibrium: wrong sign (+15% target if anything) — 0 added.
- (iii) ICL / 2nd remnants: subsumed by IGIMF (anti-double-count) — 0 fresh mass.
- (iv) EFE: negligible/wrong-signed — 0 added.

The two contested arms of the existing stack (Route B field-boost galaxy-safety, IGIMF
core-shape gas-vs-galaxy-tracking) remain the only levers; the FINAL-DOOR adds none.

## STANDING (both ways, quarantine held)

- **Credited at full weight:** candidate (i) confirms — both ways — that the dynamical residual
  EQUALS the lensing residual (lensing≡dynamics is a CONSTRUCTION feature of relativistic MOND
  / AeST + a 1.03 data fact), so the framework cannot be accused of facing an inflated
  lensing-only target; the honest no-particle stack reaches ~59-83% of the core (best-case),
  closing 45-73% of the bare gap with ZERO new particles.
- **Conceded at full weight:** no third no-particle ingredient exists; the residual ~17-39%
  (best-case) to ~57% (conservative) of the core stays UNCOVERED. The core is the shared
  relativistic-MOND open soft-spot (MI≡AeST-MG to machine precision → generic, not
  framework-specific; post-XRISM η bracket keeps the equilibrium magnitude ambiguous; NOT a
  referee-proof kill).
- **The sharpest no-particle lead is UNCHANGED** by this check: settle the core-residual SHAPE
  observationally (a resolved deprojected total-to-baryon profile of one rich relaxed core,
  CLASH+XRISM). Galaxy-tracking → the stack reaches ~80% with zero new particles; gas-tracking
  → ~60% and the residual stays the irreducible open gap. This is an OBSERVATION, not a
  calculation, and the FINAL-DOOR confirms it is the cleanest live path left.
- **Kills re-confirmed (do not re-stack):** density-a0 (breaks galaxies), MI mean-mass
  (apocenter singularity), dS-Unruh environmental / EFE (wrong sign), keV/eV sterile (killed
  harder), condensate accumulation (shift symmetry). Quarantine held: a0/Z/κ/I0 never asserted
  derived.

## Files (absolute, all in opus_48_extended_research/reviews/cluster_stack/)
- `cand_i_lensing_vs_dynamics_split.py` — sympy-exact s=1 proof + 1.03 data cap
- `cand_ii_nonequilibrium_core.py` — wrong-sign HSE bias + lensing anchor + real eRASS1
- `cand_iii_icl_second_remnant_pop.py` — ICL subsumed by IGIMF (anti-double-count)
- `cand_iv_efe_core.py` — EFE negligible/wrong-signed on the core (framework footing)
- `final_door_master_stack.py` — honest best-case stack, both shape readings, no double-count
- `self_audit_no_inflation.py` — adversarial inflation check (total-vs-gap framings, conservative knobs)

## Papers cited
- Famaey-Pizzuti-Saltas 2410.02612 (PRD 111, 123042, 2025) — CLASH lensing core target; lensing≡dynamics by construction
- Durakovic-Skordis 2312.00889 — AeST Y-Q cluster cores (Route B)
- Zhang-Zonoozi-Kroupa 2602.06082 (PRD, Feb 2026) — IGIMF stellar remnants (Route D)
- Bullet residual 2605.10022 — galaxy-tracking shape reading
- Lebeau+2026 (A&A aa56598-25) — major-merger HSE bias, core b≈−0.15 (X-ray reads LOW)
- Kelleher-Lelli (A&A aa49968-24, 2024) — cluster MOND + EFE: EFE deepens the deficit
- ICL masses: Contini+2020 (2005.13763), Kluge/Zhang ICL census; Kravtsov+2018 (stellar-halo mass)
