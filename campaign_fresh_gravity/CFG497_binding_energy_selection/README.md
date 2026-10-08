# CFG497: no binding-energy threshold that leaves S out selects S × M_b. NOT DERIVED (0 of 10 candidates)

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in e8ec321b0. The script is `cfg497_binding.py` and runs in
about 12 minutes: four infall runs, then CFG485's lensing stack.
- Main run: exit 1, because control K6 (self-similarity) failed. The failure is kept and diagnosed below; it moves no verdict.
  K1–K5 pass.
- `CFG497_MUTATE=1` (Ω_c/Ω_b = 2 × 5.364 in the initial conditions): exit 1. The teeth were detected, as designed.
- `cfg497_k6_diag.py` / `.out` is the K6 diagnostic. It was added after the main run (post hoc) and is not a verdict input.

κ = ½ is FITTED. Both footings are scored separately and never pooled. No dark-matter particle is added: the cold energy's
mass is still required, and its amount (S = Ω_c/Ω_b = 5.364) is an input. This is not "theory closed".

## The question

PAPER45 v2.1's growth fix assumes each galaxy settles S × its original baryons of cold energy (edge 5.85 r_M). CFG461, 462,
488, 490 and 494 did not derive this. CFG494 left one route open. In CFG118's infall model, the most-bound S M_b of cold at the
dissipation time t_d is 97–100% Lagrangian-partner material, but S was inserted as the cut.

Is there a binding-energy cut E < E_thr whose threshold is set by something other than S, and which selects S M_b anyway?

## Model

- **Infall:** CFG118's point-core secondary infall (H-N, Planck18 ΛCDM), N = 20,000 shells, q = 0.05 / 0.1 / 0.2. The worker
  `cfg497_infall.py` is a copy of CFG488's; the only change is the MUTATE switch name.
- **Energy:** E = v²/2 + j²/2r² + Φ at t_d (z = 3.51). Φ includes the core, the shells, the smooth baryons and Λ.
- **Selection:** s_sel = (cold with E < E_thr) / M_b,orig. "E < Φ(r_x)" means the apocentre lies inside r_x.
- **Mass scaling:** a₀-free thresholds give the same s_sel at every mass, because H-N is self-similar. a₀-carrying thresholds
  are rescaled per mass (r ∝ M^⅓).

## Candidate table (selected cold / M_b,orig at t_d)

Each range is over 3 masses (10⁹, 10^10.5, 10^11.5 M☉) × 2 footings × 3 q. The (M) window is [4.83, 5.90]; the (T) window
under 2S is [9.66, 11.80].

| candidate | threshold | s_sel (true S) | purity | s_sel (2S MUTATE) | (M) | (T) | (iii) G9 | new constants |
|---|---|---|---|---|---|---|---|---|
| A1 VIR200 | apocentre < R_200(t_d) | 3.28–3.48 | 1.00 | 5.49–5.74 | FAIL | FAIL | PASS | 1 conventional (200) |
| A2 VIRTH | apocentre < R_ta(t_d)/2 | 6.48–6.96 | 0.77–0.83 | 9.00–9.28 | FAIL | FAIL | PASS | 1 structural (½) |
| A3 CATCH | apocentre < R_ta(t_d) | 13.2–14.3 | 0.38–0.41 | 12.8–13.7 | FAIL | FAIL | PASS | 0 |
| A4 CORE-BOUND | bound to the baryon core alone | 2.27–6.99 (by q) | 0.42–1.00 | 2.34–9.31 | FAIL (0/18 cells) | FAIL | FAIL (species split) | 0 |
| B1 Y1-FIELD | total field = ν(1) a₀ | 0.12–1.51 (rises with M) | 1.00 | 0.13–1.43 | FAIL | FAIL | PASS | 0 |
| B2 A0-FIELD | total field = a₀ | 0.24–2.12 | 1.00 | 0.21–2.04 | FAIL | FAIL | PASS | 0 |
| B3 Y1-RM | apocentre < r_M | 0.13–1.01 | 1.00 | 0.16–0.91 | FAIL | FAIL | FAIL (needs M_b) | 0 |
| B4 LAW-TA | apocentre < the law's turnaround | 15.6–22.6 | 0.24–0.34 | 15.6–27.0 | FAIL | FAIL | FAIL (needs M_b) | 0 |
| B5 VF-SPEED | V_c = V_f radius | 0.58–38.1 (jumps at 10^11.5) | 0.14–1.00 | 0.54–41.6 | FAIL | FAIL | FAIL (needs M_b) | 0 |
| B6 LYNDEN-BELL | degeneracy | not formulable | – | – | FAIL | FAIL | FAIL | needs a quantum mass (no particle) |
| *R1 BARYON-E (control)* | E < E(outermost dissipated baryon shell) | 5.11–5.36 | 1.00 | 10.57–10.73 | restatement | tracks | reads the label | – |
| *R2 TOP-S (control)* | most-bound S M_b | 5.36 | 0.97–1.00 | 10.73 | restatement | tracks | S inserted | – |

**Lane verdict: NOT DERIVED.** No candidate passes (M). None tracks under MUTATE. Only the two restatement controls land on S
and track 2S, because they read the partner label or insert S.

## What was found

1. **The a₀-free thresholds give fixed pure numbers, and none is S.**
   - The VIR200, VIRTH and CATCH cuts select 3.4, 6.7 and 13.9 M_b, the same at every mass and on both footings.
   - The nearest miss is VIRTH (the top-hat virial radius). It is 21–30% high, and its purity is 0.77–0.83, so it is not the
     partner set either.
   - These numbers come from the infall model's own time structure (t_d = 2 t_ta), not from the baryon content.

2. **The a₀-carrying thresholds cannot be constant across mass.**
   - Infall energies scale as M^⅔. The law's scales scale as M^½ (r_M, V_f², a₀).
   - So the field-crossing cuts B1–B3 select cold rising roughly as M^0.4: 0.15 → 1.4 M_b from 10⁹ to 10^11.5 M☉.
   - They sit 4–40× below S, because the law's a₀ radius lies at 2–13% of the turnaround radius at z = 3.5.
   - The law's turnaround (B4) selects 16–23 M_b, which is close to the whole catchment.
   - This is CFG461's scaling objection in energy space. A cut built on a₀ inherits M^½; the infall's binding order runs on M^⅓.

3. **Binding order is real, but only S or the label picks the right cut along it.**
   - The partner set is still almost exactly the most-bound part of the cold (R2 purity 0.97–1.00, as in CFG494).
   - Cutting at the outermost dissipated baryon shell's energy (R1) gives 5.1–5.4 and tracks 2S. But that is the label.
   - Every label-free cut lands somewhere else along the same order.

4. **MUTATE: nothing tracks, and the partial movement comes through the epoch.**
   - Under 2S, VIR200 moves ×1.65 and VIRTH ×1.36. CATCH (×0.96) and B1–B3 (×1.0) do not move.
   - A1 and A2 move because t_d is keyed to the partner boundary shell, which moves from z 3.51 to z 1.59 under 2S. Their
     movement is S leaking in through the label-keyed epoch, not binding order.
   - The criteria required TRACK. A derivation of "the cosmic share" must give (Ω_c/Ω_b) M_b for any Ω_c/Ω_b, and a cut that
     hits 5.364 but not 10.728 would be a number coincidence. No candidate came close enough for that distinction to bite.

5. **(iii) G9, argued precisely.**
   - A1–A3, B1 and B2 read only the total potential or field and the parcel's own (E, j), with a₀ and the committed kernel as
     the only constants. They are G9-clean, and they fail on the number.
   - A4, B3 and B5 need the baryon mass or the baryon field apart from the total. That is a species split, CFG462's F-H class.
   - B4 evaluates the law's ν(g_N[baryons]) before anything has settled.
   - R1 reads which shells' baryons dissipated (baryon fate), the CFG488 coupling.
   - The epoch t_d itself is keyed to the label (CFG494's choice). So even a G9-clean threshold evaluated at t_d would have
     been DERIVES-COND at best.
   - Epoch robustness (q = 0.1, at t_ta(k_b) / t_d / z = 2): VIR200 2.9 / 3.5 / 4.2, VIRTH 8.3 / 6.8 / 6.9, A4 5.3 / 6.2 / 6.6.
     The selected amount drifts with epoch, so an epoch choice would be a second hidden threshold.

6. **(iv) Constant count.** CATCH, B1 and B2 add no constants; VIR200 adds one conventional number (200) and VIRTH one
   structural number (½). None contains S or f_b. None works, so the count is moot.

7. **Bonus (i) clusters: FAIL for every candidate, by a small margin.**
   - Every candidate except B3 supplies at least ν_cl − 1 = 2.94 / 3.28 M_b. Free inside-out fill then gives
     u = 1 − (ν − 1)/x_T15 = 0.426 / 0.620 canonical and 0.360 / 0.577 alt (b = 0 / 0.3).
   - The b = 0 ends fall 0.007 / 0.008 below the record range [0.433, 0.628] / [0.368, 0.584].
   - B3 gives 0.514 / 0.679 and 0.557 / 0.707, failing at the b = 0.3 end.
   - Class-B cluster masses (1e14 M☉) are RECALLED (U).

8. **Bonus (ii) lensing: KiDS FAILs everywhere; the early-type levels split.**
   - KiDS medians x_edge/r_ta run 0.007–0.18 against the window [0.3, 0.5]. B4 is the largest at 0.12 / 0.11, and B5's 0.18 is
     canonical only.
   - Early-type χ² (≤ 12.59 to pass) passes for A3, B1, B2, B3, B4 and B5 (2.8–10.2). It fails for A1, A2 and A4 (24–39) and
     for 5.85 r_M itself (30.5 / 38.1, K5).
   - So the early-type levels reject the supply range of 3–7 M_b around S. They accept both much smaller and much larger
     settled amounts.
   - This extends CFG494's finding: any supply that reproduces S inherits the early-type miss, as the criteria anticipated.

## Controls

- K1 PASS: M_ta/M_b = 23.632, r_ta0 = 507.94 kpc, partner = S M_b to 1e-12, z_d = 3.509, two-pass identity 0.
- K2 PASS: CFG494's energy-rank purity reproduced: 0.9714 / 0.9779 / 0.9989 (CFG494: 0.9721 / 0.9779 / 0.9996).
- K3 PASS: x_e = 5.849761, and the point phantom there equals S M_b to 4.5e-9.
- K4 PASS: KiDS median 0.0377 / 0.0327.
- K5 PASS: early-type χ² 30.46 / 38.11.
- **K6 FAIL (kept).** The direct 10⁹ run against the rescaled 10¹⁰ run gives A1 3.23 vs 3.48 (−7%) and B2 0.32 vs 0.42 (−23%).
  The post-hoc diagnostic (`cfg497_k6_diag.out`) finds two causes:
  - **Softening.** The softening scales as M^½ while lengths scale as M^⅓. With the softening rescaled to M^⅓, the 10⁹ run
    reproduces the rescaled values: A1 3.46, B2 0.436 / 0.350, R1 5.36.
  - **Instantaneous stream noise in the few innermost shells.** Removing one shell (N − 1) moves B1 by up to 26% and B2 by up
    to 13%.

  Neither moves a verdict. The B-class cuts sit 2.5–40× below the window, and A1/A2 move by ≤ 2% under the noise probe.

## Disclosures

- The K6 diagnostic, and the observation that A1/A2's MUTATE movement runs through the epoch, came after the first output.
- The bonus uses the geometric mean of s_sel over q. That choice was made in the script before the bonus was computed, but it
  was not written in the criteria.
- My written expectation (S-free cuts barely move under MUTATE) held for A3 and B1–B3. A1 and A2 moved more, through the epoch.
- A `CFG497_TESTN` smoke-test switch exists in the script. It is used for development only, and its outputs are not committed.

## Caveats

- Everything is spherical: a point core present from z = 100, and no settling back-reaction. The epoch t_d is inherited from
  CFG494.
- Energies are instantaneous, in a time-dependent potential, with v taken by a 1e-6 finite difference.
- Clusters use the closed-box CFG453 medians. The KiDS window rests on CFG413's free two-halo term.

## What this leaves

Binding energy orders the partners, but no G9-clean scale (virial overdensity, top-hat radius, turnaround, the a₀ field
crossing, the law's y = 1, the law's turnaround) cuts that order at S M_b. The a₀-free cuts land on fixed numbers (3.4, 6.7,
13.9) that do not track the cosmic ratio. The a₀ cuts scale as M^½ against the infall's M^⅓. The cut at S is reached only by
reading the partner label or inserting S, as in CFG462, 488 and 494.

**The supply postulate stays an input.** The open record now reads: amount from adiabatic initial conditions (CFG494); which
cold, by binding order (this lane); where to cut, still S.

## Run

```
nice -n 15 python3 campaign_fresh_gravity/CFG497_binding_energy_selection/cfg497_binding.py                    # exit 1 (K6, kept)
CFG497_MUTATE=1 nice -n 15 python3 campaign_fresh_gravity/CFG497_binding_energy_selection/cfg497_binding.py    # exit 1 = teeth
nice -n 15 python3 campaign_fresh_gravity/CFG497_binding_energy_selection/cfg497_k6_diag.py                    # post-hoc K6 diagnostic
```

Each run reads the other's JSON for the joint verdict, so run main and MUTATE, then re-run whichever ran first. Inputs, all
read-only:
- `CFG118_secondary_infall/shellcore.c`
- `CFG4_common`
- `CFG100_kids_mass_rederivation/cfg100_lib.py`
- `CFG485_kids_split_settling_completeness/cfg485_settling_split.py` (and its inputs)
- `CFG453_t15_deficit_units/cfg453_results.json`
- `real_research/data/lensing_rar/{lr_lenses,cfg110_perlens}.npz`
