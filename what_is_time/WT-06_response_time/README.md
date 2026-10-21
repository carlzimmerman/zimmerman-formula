# WT-06: how long does the extra pull take to catch up after a sudden baryon change?

**Field part: INSTANT. Mass part: READING-DEPENDENT.** Under the frozen rules the five record readings split as follows:
- M-I is UNRESOLVED (K4) and does not settle;
- M-D(0.5), M-ID(0.5) and M-ID(1.186) are FLOW-LIMITED LAG;
- M-D(1.186) is MIXED (1.76–3.03 t_dyn).

No reading is INSTANT. Against CFG763 the response is INCONSISTENT-FASTER in every reading. Against CFG764 it is
INCONSISTENT-FASTER in four of five readings (M-D(0.5) PARTLY CONSISTENT, 2/16), so these are **different physics**. Observability
is OBSERVABLE (SOME READINGS: M-I only) and is robust to the A1 probes. K4 FAILS as frozen.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (**f11ca13c3**). Amendments A1–A4 are appended after the freeze and are
  uncommitted for review:
  - A1: report-only V3 fragility probe;
  - A2: the probe's T_max bug, K4's UNRESOLVED consequence coded, extra reporting;
  - A3: WT-02 cited;
  - A4: shell-crossing diagnostics.

  None changes a rule, cell, reading or threshold.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. Z = 5.7888. Cold energy is real gravitating mass;
  no particle species. Instantaneous MOND (MOND-I) appears only as a same-pipeline comparison. Not "theory closed". Nothing here
  says the data favour the framework.
- **Script:** `wt06.py` (sympy/numpy/scipy, one process).
  - `OMP_NUM_THREADS=1 nice -n 10 python3 wt06.py` → `wt06.out`, `wt06_results.json`. Exit 2 = K4 fails as frozen; every other
    K passes.
  - `WT06_MUTATE=1 …` → `wt06_MUTATE.out`, `wt06_results_MUTATE.json`. Exit 1 = all three teeth bite.
  - Main: 2172 s (about 36 min), peak RSS 0.40 GB (`/usr/bin/time -l`).
- **Inputs (read only):** CFG938 parent (7a0d41e8b / 92606e049); CFG638 drift and α bounds; CFG747/776 dynamics; CFG763/764
  windows; SPARC rotmod NGC 3198 and DDO 154 (999f94dfe); R_d and R_HI from `SPARC_Lelli2016c.mrt`; WT-02 (b85749d1c /
  9b3d77382). Nothing was downloaded. No other lane's file was edited, run or staged.
- **Earlier outputs kept:** `wt06_firstrun_A1trunc.*` (run 1, stopped; A2) and `wt06_run2.*` (run 2; A4). Run 2's classes and cell
  numbers equal the final run's. See the disclosures.

## (a) What responds, and how fast (sympy, all checks True)

In the CFG938 parent the extra pull on stars, gas and light is u = χ′ = G M_c(<r)/r²: the cold medium's own Newtonian pull.
- **S1:** χ is a constraint sourced by ρ_c alone. It has no baryon source. **At t = 0⁺ after a blowout, the extra pull is exactly
  what it was.** Only the medium's motion can change it.
- **The field part re-forms instantly.**
  - Φ re-forms at c: r/c = 2–116 kyr at the cells, ≤ 5.4e-4 t_dyn.
  - χ is instantaneous on the medium's slices (independently, WT-02: elliptic on static media).
  - The tether-stress (metric) share of the pull is ≤ 1.2e-7.
  - In an expanding medium WT-02 finds a smear τ_k = 3Hr²/c², which is 0.22 yr at 10 kpc. That is negligible here (A3).
- **The mass part moves** under f = R(u) − g_N, with R = u²/(a0 − u) (S2). The medium's self-gravity cancels, so the restoring
  force comes from the baryons only. Three clocks follow:
  - **M-I (ideal parent):** an oscillator, ω² = 2uR′(u)/r + dg_N/dr (S3).
    - Deep point mass: ω t_dyn = √(2 g_N/g) < 1 (S3), i.e. slower than the stars' orbits in the low-acceleration regime.
    - NGC 3198: ω t_dyn = 1.84 (2 R_d) and 1.04 (5 R_d).
    - With no dissipation it **does not settle**; it rings.
  - **M-D(α) (record drift, overdamped):** decay rate Γ = ατ·4πGρ_ph (S4). For NGC 3198, Γ t_dyn/α = 0.64 (2 R_d) and
    0.89 (5 R_d).
  - **M-ID(α) (parent + drift):** s² + Γs + ω² = 0 (S5), an underdamped oscillator at the record's α.
- **The Israel–Stewart clock** τ_π = τ_ff/(2α) does not enter: the cold parent has p = 0. In the kinetic reading it would be
  1.00 / 0.42 t_dyn.
- **The stiffness term** (off) is ≤ 2e-6 of the tether term in ω² at L* = 24 pc. At L* = 1 kpc it is 0.06–1.4 in DDO 154, so a
  large L* would stiffen the dwarf's response. Report only.

## (b) Toy: instant gas loss, spherical SPARC baryons (Υ 0.61), baryons frozen after t = 0 (B-F)

**Residual.** D_V = ½ log10[g/g_law(g_N)], with g_N the baryons present at the same instant. The comparison has three phases:
- At t = 0⁺ instantaneous MOND drops at once to the new law, so D_V ≡ 0 always (an identity).
- The framework at first keeps the old pull, D_V(0⁺) > 0.
- It then recovers.

**Size of the jump, D_V(0⁺) in dex.**

| system | cell | gas share | f = 0.2 | f = 0.5 |
|---|---|---|---|---|
| DDO 154 | 2 R_d | 0.20 | 0.003 | 0.008 |
| DDO 154 | 5 R_d | 0.66 | 0.011 | 0.033 |
| DDO 154 | R_HI | 0.91 | 0.018 | 0.056–0.057 |
| NGC 3198 | 2 R_d | 0.008 | 1e-4 | 1e-4 |
| NGC 3198 | 5 R_d | 0.15 | 0.0015 | 0.0039 |
| NGC 3198 | R_HI | 0.42 | 0.007 | 0.019 |

**Lag times** (Myr; t_50 / t_90; the ranges cover both footings and both f). t_dyn(2 R_d, 5 R_d) is 27–28 and 48–50 Myr (DDO 154)
and 40–41 and 94–98 Myr (NGC 3198).

| reading | DDO 154, 2 R_d | DDO 154, 5 R_d | NGC 3198, 2 R_d | NGC 3198, 5 R_d | t_50, t_90 in t_dyn (all 16 cells) |
|---|---|---|---|---|---|
| M-I | 29–30 / > 3 Gyr (one 3.0 Gyr) | 62–66 / > 3 Gyr | 24 / > 5.9 Gyr | 98–101 / ≥ 5.85 Gyr | 0.57–1.38 / ≥ 59.9 (rings; swings to ≈ −D_V(0⁺)) |
| M-D(0.5) | 34–37 / 114–122 | 57–63 / 200–214 | 81–90 / 270–297 | 145–152 / 483–508 | 1.18–2.17 / 4.15–7.21 |
| M-D(1.186) | 15–16 / 48–51 | 24–27 / 85–91 | 35–38 / 114–125 | 61–64 / 204–215 | 0.50–0.92 / 1.76–3.03 |
| M-ID(0.5) | 19–20 / 200–210 | 38–39 / 307–482 | 21 / 515–574 | 72 / 952–972 | 0.51–0.79 / 6.36–13.92 |
| M-ID(1.186) | 12–13 / 107–111 | 22–23 / 213–239 | 17 / 225–227 | 48–49 / 382–393 | 0.42–0.51 / 3.88–5.64 |

**Classes (V1, frozen: L = t_90; INSTANT ≤ 1 t_dyn, FLOW-LIMITED LAG ≥ 2, in all 16 cells).**
- M-I is FLOW-LIMITED LAG before K4 and **UNRESOLVED** after it (frozen K4 consequence, below).
- M-D(0.5), M-ID(0.5) and M-ID(1.186) are **FLOW-LIMITED LAG**.
- M-D(1.186) is **MIXED**: DDO 154's cells sit at 1.76–1.84 t_dyn, NGC 3198's at 2.2–3.0.
- **Overall: READING-DEPENDENT.** The named physics is the baryon-only restoring force (M-I), the drift mobility ατ·4πGρ_ph
  (M-D), or both (M-ID).

**Shell crossing (A4, report only; final run).** Only M-I crosses; the dissipative readings never do.
- **DDO 154.** Crossing starts at 540–551 Myr at r = 0.49 kpc. That is the first SPARC radius, where the r³ inner extrapolation
  joins the PCHIP profile (a kink in dg_N/dr, plausibly an artefact). Near the cells it starts at 589–2044 Myr.
- **NGC 3198.** It starts at 1.6–2.5 Gyr, at 14–41 kpc.
- **Consequence.** M-I's t_50 values and the V3 hit (below) lie inside the single-stream regime. M-I's late settling (t_90 or
  censored) lies after crossing near the cell in 12 of 16 cells, which is beyond CFG938's single-stream condition 5.

## (c) Relation to CFG763 / CFG764 and to instantaneous MOND

- τ_resp ≡ t_50/ln 2 is 0.10–0.50 t_orb and 17–220 Myr, across readings, cells and footings.
- **Against CFG763** (0.72 / 0.83 to 3.47 Gyr): INCONSISTENT-FASTER in every reading.
- **Against CFG764** (0.457 / 0.525 to 1.196 t_orb): INCONSISTENT-FASTER in four readings. The exception is M-D(0.5), PARTLY
  CONSISTENT in 2 of 16 cells; its maximum is 0.499 t_orb, at NGC 3198 cells where ρ_ph/ρ_m is low.
- Frozen text rule: **DIFFERENT PHYSICS.** τ_resp is below CFG764's floor in 78 of 80 reading-cells (by up to ×4.8). It is
  below CFG763's floor in all 80 (by ×3–41). The medium re-settles faster than the formation clocks fitted to young tidal dwarfs
  allow. So if those clocks are real, a young tidal dwarf's missing cold mass cannot be a settling delay. It must be a supply
  or formation delay: no cold mass is there yet to settle.
- **Against instantaneous MOND** (same pipeline):
  - MOND's V_c drops to the new law at t = 0, with residual ≡ 0.
  - The framework's V_c first drops only by the Newtonian part, sits **above** the law by D_V(0⁺), and recovers half way in
    t_50.
  - In the ideal parent (M-I) it then **overshoots below** the law, with nearly the full amplitude (min D_V ≈ −D_V(0⁺)).

## (d) Observability (V3 frozen: |D_V| ≥ 0.05 dex continuously for ≥ 100 Myr)

**Overall: OBSERVABLE (SOME READINGS: M-I).**
- **The single hit:** DDO 154 at R_HI (4.96 kpc), f = 0.5, M-I.
  - It is not the initial excess, which stays above 0.05 for only 89–95 Myr.
  - It is the **overshoot**: from 432–437 Myr after the blowout, the rotation curve sits **0.050–0.057 dex below the law** for
    290 (canonical) / 311 (alt) Myr.
  - Robust (A1/A2): N_c × 2, dt / 2, outer × 2 and inner / 2 all give 290–311 Myr from 432–437 Myr.
  - It lies before shell crossing reaches R_HI (871–877 Myr), so it is inside the single-stream regime (A4).
- **Every dissipative reading: NOT OBSERVABLE.** |D_V| ≥ 0.05 lasts ≤ 23 Myr, and ≥ 0.02 lasts 73–195 Myr.
- **NGC 3198:** never above 0.02 dex (peak 0.0197).
- **Where it could show:** only at the HI edge of a gas-dominated dwarf, and only if it lost ≳ 46% of its gas quickly. f* = 0.462
  (canonical) / 0.457 (alt) is needed for D_V(0⁺) to reach 0.05 dex at DDO 154's R_HI.
  - The observable is a rotation curve that, given the gas still present, sits first above and then (ideal parent) below the law
    for a few hundred Myr.
  - Satellites just after pericentre are not modelled. Young tidal dwarfs are formation, which is CFG763/764's domain, not
    response.
- **Gradual loss (report only).** A loss spread over T cuts the drift reading's peak by (1 − e^(−ΓT))/(ΓT) (S7): ×0.78 / 0.51 /
  0.19 for T = 1 / 3 / 10 t_dyn(R_HI) at DDO 154.
  - **PROVISIONAL (WebFetch of the arXiv abstract, report only):** McQuinn et al. 2010 (arXiv:1009.2940) give dwarf starburst
    durations of 450–650 Myr, some up to 1.3 Gyr. That is ≈ 4.5–13 t_dyn(R_HI), so a real outflow is probably slower than the lag,
    and the signal shrinks to roughly ×0.2–0.5.
  - The undamped M-I ringing would also be excited less by a slow ramp. That is not computed here.
- **B-L variant (baryons as cold rotating shells; report only, no class weight).**
  - The stars' own response amplifies the M-I ringing at DDO 154 R_HI: peak 0.069–0.070 dex, ≥ 0.05 for 546–551 Myr.
  - M-ID(0.5): 21–22 Myr.
  - NGC 3198 stays < 0.02 dex.
  - NGC 3198's inner gas "hole" (V_gas² < 0 inside about 2 kpc) makes the spherical-equivalent gas mass negative there. Removing
    gas then raises M_b(<r) locally (2496 marker-mass increases across its 12 perturbed B-L rows). This is a spherical-equivalent
    artefact, disclosed.

## Controls

| check | result |
|---|---|
| K1a static limit = law (identity: R is built from the law) | max \|g/g_law − 1\| = 4.4e-16 (line 1e-12): PASS |
| K1b unperturbed runs stationary (all readings, B-F and B-L) | max \|D\| = 9.6e-17 dex (line 1e-8): PASS |
| K2 Newtonian textbook mass loss | impulsive apocentre 5/3 to 1.6e-15, radial period to 3.7e-13, δ = 0.5 energy 0, adiabatic ⟨r⟩ = 1.25 to 1.5e-8: PASS |
| K3 clocks vs sympy (single marker) | M-I period, M-D rate, M-ID roots: rel. err ≤ 6.7e-6 (lines 0.5% / 0.5% / 1%): PASS |
| K4 convergence (NGC 3198 canonical f = 0.5; M-I, M-ID(0.5)) | **FAIL as frozen.** M-ID(0.5) and every t_50 converge. M-I's t_90 at 5 R_d is 5851 Myr (59.9 t_dyn) in the base run but censored (> T_max = 60.0 t_dyn) under dt / 2 and inner / 2, so M-I → **UNRESOLVED** by the frozen rule. Post hoc, no class weight: either way M-I settles no sooner than ~60 t_dyn, far above the 2 t_dyn line |
| MUTATE (exit 1, 17 s, 0.19 GB) | **All teeth bite.** MU1 (medium → MOND-I): LAG_DETECTED fails and every class reads INSTANT. MU2 (R → u²/a0): K1a fails, 2.5e-1. MU3 (drift sign flipped): K3's M-D clock fails |

## Strongest caveat

The response clock is set by the medium's dissipation law, and the record does not fix that law.
- The parent's ideal dynamics (M-I) never settle.
- The record's drift (α between 0.5 and 1.186) gives t_90 from 1.8 to 14 local dynamical times.

The toy is spherical, with frozen baryons, an instantaneous and radially uniform gas loss, and stiffness off. The one observable hit
is in the dissipationless reading only, at the HI edge of a gas-dominated dwarf, at ≈ 0.05 dex. Realistic multi-hundred-Myr
outflows would shrink it.

## Plain answer

In this framework the extra pull is the cold medium's own mass, and the field that carries it updates instantly. That mass then
has to flow:
- it is half-way back to the law in about 0.4–2 local dynamical times (12–150 Myr in these galaxies);
- it settles in 2–14 dynamical times (0.05–1 Gyr) if the record's drift damps it;
- in the parent's ideal dynamics it never settles and rings around the law for Gyr.

That lag is a time signature instantaneous MOND does not have. It is small: ≤ 0.057 dex in V_c, and only for large, fast gas loss
in gas-dominated dwarfs.

## Disclosures

- **Code tests (scratchpad, not kept):**
  - a smoke run at T_max = 6 t_dyn(5 R_d) (A1 records what it showed);
  - a one-row unit test of the crossing bookkeeping before the final run.
- **Run 1** was stopped during B-L after A1's truncated probe printed a void "FRAGILE" (A2). Kept as `wt06_firstrun_A1trunc.*`.
- **Run 2** lacked the crossing diagnostics (A4). Kept as `wt06_run2.*`; the final run reproduces its classes and cell numbers.
- **The V1 class is printed twice,** before and after K4's frozen consequence. The first run printed only the former.
- **Approximations:**
  - the toy's τ uses the law-state matter density of the current baryons (declared in §3);
  - B-L's drift uses the t = 0⁺ profile.
- **A3:** the medium's own settling motion generates a uniform field u_v (WT-02). It is ≲ 3e-3 of the residual it rides on; this is
  a one-line estimate, not computed.
