# CFG637 FROZEN CRITERIA: derive the unsettled cold-energy reservoir's profile from the framework, then re-score CFG634's static gates

Committed ALONE (with the derivation library `cfg637_lib.py`, which computes no gate number), before any gate number exists.
Date 2026-10-12.

κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻² (each reused gate keeps its own committed footing values) are
reported separately and NEVER pooled. "Cold energy" throughout. No dark-matter particle; the cold energy's mass is still required.
Not "theory closed". No ΛCDM halo shape (NFW, Einasto, c(M)) and no standard-MOND yardstick enters any verdict.

## 0. What was seen before freezing (disclosed)

- CFG634 (README, all three JSONs): groups need the reservoir outside the members (R0/RI), clusters need it inside (RI/RN), the
  Bullet main aperture is TENSION under RI/RN, and NO SINGLE RESERVOIR RULE passes T2, T3 and T4b (gate J), for H-CB and for B.
- CFG629 (RN closes most of the Bullet main core; the sub is input-mass-limited), CFG596 (canonical KiDS shear EXCLUDED),
  CFG636 (H-CB 1024³ running; its 256³ preview only), CFG118/CFG158 (secondary infall of ALL cold matter onto a static core in
  Newtonian gravity fails the law's C(r) target; cumulative mass converges, local bins noisy), CFG432 (X-COP unsettled mass is
  more concentrated than the gas), CFG527/530 (R5 shell draw), CFG557 (switch = turnaround ball; spherical collapse constants),
  CFG620/626 (maximum-entropy F(E,L) method), THEORY_v1, ASSESSMENT_2026-10-09.
- Engine smoke tests of `cfg637_lib.py` on a TOY cluster (β-model gas, r_c 300 kpc, 1.3e14 inside 2 Mpc; not a gate system):
  run time about 2–5 s; phase-mixed and time-averaged read-outs agree to about 10% at 0.03 r_ta; the edge falls beyond r_ta in
  clusters, and there the draw rule matters enormously (outer-first leaves 6.6e13 Msun of reservoir inside 250 kpc, uniform
  2.3e12). No gate number was computed.

## 1. Physics (declared)

**Which potential the reservoir feels.** Under G9 only real mass gravitates; the law's extra pull IS the settled cold energy (R1).
Unsettled cold energy is collisionless and moves in the TOTAL Newtonian potential of real mass: baryons (condensed core + diffuse
non-retained baryons) + settled cold energy (round, R6) + the reservoir itself + matter not yet turned around + the Λ term of the
framework's background. No additional phantom force acts on the reservoir (that would double-count the settled mass).

**Supply.** The turnaround catchment holds baryons and cold energy at the cosmic ratio (Ω_c/Ω_b = 5.364); its cold energy is
the supply. Reservoir = supply − settled.

**Method A (PRIMARY derivation): self-similar secondary infall** (`cfg637_lib.Infall`, `derive`):
- 1-D Lagrangian shells (N = 1600, log-spaced in enclosed mass from 1e-3 to 3 M_ta), physical coordinates, flat background with
  Ω_m = (ω_b + ω_c)/h², Ω_Λ = 1 − Ω_m (h 0.6736, ω_b 0.02237, ω_c 0.1200, as cfg557_lib; INHERITED context), start a = 0.02,
  growing mode, KDK leapfrog, softening 2e-3 r_ta.
- Each shell carries baryons + cold energy until it first turns around (candidate B's switch = the turnaround ball, CFG557 D1).
  At turnaround its RETAINED baryons (f_ret of its baryons) join the condensed core; non-retained baryons stay on the shell
  (gravitate, never drawn).
- Core: the system's OBSERVED retained-baryon cumulative profile at a_obs, grown self-similarly (amplitude = retained baryons
  turned around so far; radius ∝ r_ta(t)).
- Settled cold energy: the law's phantom (the gate's own kernel and a₀) of the SOURCE baryons of the core (candidate B: all
  retained baryons; H-CB: condensed only), truncated at the supply edge (R2: where M_ph(<r) reaches the cold energy turned around
  so far), confined to the turnaround ball.
- Draw (R5): settled cold energy is drawn uniformly from the cold weight of turned-around shells located between the edge and
  r_ta; nothing inside the edge. If that shell is exhausted the draw is short (reported). If the edge lies at or beyond r_ta the
  R5 shell is empty; its continuous limit (r_e → r_ta) is **outer-first**: draw from the outermost turned-around shells inward
  (PRIMARY). Uniform draw over all turned-around cold weight is a BRACKET (it draws from the core, which R5 forbids).
- Angular momentum at turnaround: j² = 2 G M(<r) r q/(1 + q) (INHERITED bracket, as CFG118). Primary q = 0.1; brackets 0.05, 0.2.
- Seed: δ_i(M) = δ₀ (M/M_ta)^(−ε), capped at 0.3 (INHERITED context: the initial power-spectrum shape sets ε). Primary ε = 1
  (point-seed, Bertschinger/CFG118 benchmark); bracket ε = 0.5. δ₀ is iterated until the mass turned around at a_obs equals M_ta
  to 1%.
- a_obs = 1 for groups and X-COP; a_obs = 1/1.296 for the Bullet progenitors.
- Read-out (PRIMARY): phase-mixed M_res(<r) from each reservoir shell's (E, j) in the final potential (time fraction inside r).
  Bracket: the snapshot time-average over the last 1 Gyr.

**Method B (SECONDARY derivation): maximum entropy.** Non-degenerate Lynden-Bell = lowered Maxwell–Boltzmann (Woolley) F(E) of
the reservoir in the same final total potential, bounded at r_ta (E < Φ(r_ta)), mass = Method A's reservoir mass, temperature
fixed by the energy the infall delivered (Method A's reservoir energy in the final potential), self-consistent with its own
gravity. Isotropic (the CFG620/626 anisotropy is not used: its constraint is the law's settled density, not the reservoir's).

**System inputs (CFG634's conventions, unchanged):**

| system | catchment baryons | f_ret | retained-core profile | source (B / H-CB) | gate kernel, a₀ |
|---|---|---|---|---|---|
| T2 Tian+26 groups (63, per group) | M_bar / 0.10 | 0.10 | M_bar Hernquist (a = Re/HERN_RE) | M_bar / 0.92 M_bar (hot 0.08) | C540.nu, C540.FOOT |
| T3 X-COP (12, per cluster) | M_b(<R200)/0.90 | 0.90 | audit gas + stars (log-extrapolated to R200 as CFG634; flat beyond) | gas+stars / stars | C4.nu_mono, C4.A0 |
| T4 Bullet (B1 primary; BASE, B2, B3) | p.Mb | 1.0 | p.Mbar | p.Mbar / p.Ms | cfg597 phantom_mass kernel (exp), A0 |

M_ta = catchment baryons / f_b (f_b = 0.02237/0.14237).

**Reservoir input to the gates (RD).** M_res,gate(<r) = M_res,A(<r) × (supply_gate / supply_A), where supply_A is the cold energy
the derivation turned around (≈ supply_gate to 1%) and supply_gate is CFG634's supply for that system. The gates' settled
phantom, baryons, statistics, thresholds and data are CFG634's, unchanged (`cfg637_gates.py` copies CFG634's functions verbatim
and adds only the `RD` reservoir branch). Method B enters the same way (RB).

## 2. Gates and pass/fail (= CFG634's, unchanged)

- **T2 groups:** CLOSES (|Z| < 2) = PASS, else FAIL (ABOVE / BELOW). Primary hot 0.08, Hernquist hot shape.
- **T3 X-COP:** η = M_HSE/M_model at the headline radius, median over 12, σ = SD/√12. PASS |η − 1| ≤ 0.20 on both footings; FAIL if
  η ≥ 1.30 or ≤ 0.77 with ≥ 3σ on both; else TENSION. Inner band 200–420 kpc: same thresholds; in CFG634 reported only — here it
  enters the stricter joint gate J+ (below).
- **T4 Bullet (b):** aperture Δκ (galaxies − plasma), PASS if |Δκ_model − Δκ_obs| ≤ 2σ and Δκ_model > 0 for main AND sub; FAIL if
  either misses by ≥ 3σ; else TENSION. B1 primary; BASE/B2/B3 reported. (c) main M(<250)/Paraficz+16 PROVISIONAL reported.
- **Joint gate J (CFG634's):** a derived rule passes iff T2 PASS, T3 headline PASS and T4b (B1) PASS, each on both footings.
  **J+** additionally needs the T3 inner band PASS on both footings.
- Evaluated separately for each source variant (candidate B, H-CB) and each derivation method (A primary, B secondary).
  Never pooled across footings or sources.

## 3. Verdict rule

- **SINGLE DERIVED RULE PASSES** (for a source variant) if Method A primary passes J; reported with J+ and with every bracket that
  flips it (label DERIVATION-BRACKET-DEPENDENT if any of ε 0.5, q 0.05/0.2, uniform draw, time-averaged read-out flips J).
- **DERIVED RESERVOIR FAILS <gate(s)>** if Method A primary fails J; the failing gate(s) named. If Method B passes where A fails
  (or vice versa), the label is METHOD-DEPENDENT. A fail is a valid result and is verified as hard as a pass (brackets,
  resolution, MUTATE).

## 4. Controls and MUTATE (all must hold, or the dependent result is VOID)

- **M-R (exact reproduction):** with the reservoir set to CFG634's R0 / RI / RN brackets, `cfg637_gates.py` must reproduce
  CFG634's JSON numbers: T2 means (all CELLS present in both), T3 η medians, T4 Δκ and M(<250)/P16 — to 1e-9 absolute.
- **M-G (reservoir gravity has teeth):** turning the reservoir's self-gravity off (selfgrav = False) must change M_res(<0.1 r_ta)
  by > 5% for a representative group and X-COP cluster on both footings.
- **M-D (draw rule teeth, reported):** the uniform draw must change the cluster M_res(<0.05 r_ta) by > 5%.
- **C1 mass conservation:** supply_A = drawn + reservoir to 1e-9 relative; turned-around mass within 1% of M_ta.
- **C2 resolution:** N 1600 vs 3200, M_res(<r) at 0.02, 0.05, 0.1, 0.3 r_ta within 10% for one group and one cluster (reported;
  a failure is reported and limits precision, as CFG118 C3).
- **C3 Bertschinger benchmark (reported):** no core, no settling, ε = 1, q = 0.02 — log-slope of ρ over 0.03–0.15 r_ta reported
  against −9/4 (Λ background, so not exact).
- **C4 read-out agreement (reported):** phase-mixed vs time-averaged M_res(<r) at 0.05 and 0.1 r_ta.

## 5. Inherited ingredients (flagged as CONTEXT; none is a framework prediction)

Seed slope ε (initial power-spectrum shape), angular-momentum bracket q (tidal torques), Planck-like background constants, the
spherical/self-similar approximation, the self-similar growth of the observed core, X-COP hydrostatic masses (published
reconstruction), Paraficz+16 masses (recalled, PROVISIONAL), Bullet progenitor M200 (simulation line; sub input-limited per
CFG629), the 8% group hot fraction, and CFG634's per-scale supply conventions (groups /0.10, X-COP /0.90, Bullet ×1).

## 6. Machine

One process, < 1.5 GB, nice -n 10, OMP 1 thread; the running cfg636_pm.py and cfg625 jobs are not touched. No downloads.
Outputs: `cfg637_*.out`, `cfg637_*_results.json`.
