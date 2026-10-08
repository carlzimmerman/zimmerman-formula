# CFG494: adiabatic initial conditions relabel the supply; they do not derive it. NOT DERIVED (RESTATEMENT, initial-condition relabel)

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in cbfc9b04b. The script is `cfg494_adiabatic.py` and runs in
about 8 minutes (five infall runs plus CFG485's lensing stack).
- Main run: exit 0, because controls K1–K5 pass.
- `CFG494_MUTATE=1` (coherent isocurvature labels): exit 1. The teeth were detected, as designed.

κ = ½ is FITTED. Both footings are scored separately and never pooled. No dark-matter particle is added: the cold fluid's mass
is still required, and its amount (Ω_c/Ω_b = S = 5.364) is an input. This is not "theory closed".

## The question

The growth fix (PAPER45 v2.1) assumes each galaxy settles S × its own baryons, which puts the edge at 5.85 r_M. CFG461, 462,
488 and 490 failed to derive this. New angle: adiabatic perturbations give cold/baryon = S in every Lagrangian element, so the
cold fluid born next to a galaxy's baryons (their "Lagrangian partner") is S × the original baryons by construction. Is that
enough?

Two readings were scored:
- **LP-G (galaxy partner):** the settled cold is the partner of the baryons that dissipated into the galaxy. LIVE: partners of
  expelled baryons unsettle (edge 5.85 r_M). SET: they stay settled (edge needs f_ret,gal).
- **LP-H (halo partner):** the settled cold is the partner of every baryon in the halo's collapsed patch, i.e. all
  turned-around cold. Two catchments: CFG118's infall catchment (LP-H/inf) and the law's own turnaround (LP-H/law).

Model: CFG118's point-core secondary infall (ΛCDM, N = 20,000, q = 0.05/0.1/0.2) via CFG488's worker, with Lagrangian partner
labels. Dissipation time t_d = 2 t_ta of the outermost partner shell (z = 3.51 in this self-similar set-up, for every mass).

## Verdict table

| reading | (a) G9 | (b) pairing | (c1) KiDS window | (c2) early-type levels | (d) clusters | DERIVES |
|---|---|---|---|---|---|---|
| LP-G/LIVE | FAIL | PASS (identity) | FAIL 0.038 / 0.033 | FAIL χ² 30.5 / 38.1 | FAIL | no |
| LP-G/SET | FAIL | PASS (identity) | no prediction | no prediction | FAIL | no |
| LP-H/inf | PASS | FAIL 1.57 (t_d), 4.41 (z = 0) | FAIL 0.156 / 0.135 | PASS χ² 1.7 / 1.9 | FAIL (u = 0) | no |
| LP-H/law | PASS | FAIL 20–96 | FAIL 0.849 / 0.848 | PASS χ² 2.6 / 2.9 | FAIL (u = 0) | no |

**Lane verdict: NOT DERIVED — RESTATEMENT (initial-condition relabel).** The reading that pairs (LP-G) needs the label; the
reading that is gravity-only (LP-H) does not pair.

## What was found

1. **(b) Pairing holds, but only as the composition identity.** The partner cold is exactly S M_b (to 1e-12) because the shells
   are built with ratio S, and 100% of it is inside the turnaround catchment at t_d (C = 1.0000, all q, all cells). That is mass
   conservation of bound orbits, not a selection: the same catchment holds 1.57 S M_b of cold at t_d and 4.41 S M_b at z = 0.

2. **(a) The partner identity is lost to every label-free sphere, CFG488's objection quantified.** Purity Π = partner / all cold:
   - R_ta (catchment): Π = 1.00 at the boundary shell's turnaround (z 6.2), 0.64 at t_d, 0.44 at z = 2, 0.32 at z = 1, 0.23 at z = 0.
   - R_200 at t_d: Π = 0.96–1.00 but C = 0.74–0.83; by z = 0 C ≈ 1, Π = 0.37–0.43.
   - No q passes C ≥ 0.9 and Π ≥ 0.9 at t_d: **G9-FAIL**. The selection must read which baryons cooled, i.e. baryon fate.
   - **Near-misses, reported honestly.** (i) Post-hoc epoch scan: R_ta passes both lines only at z 5.9–5.5, just after the
     outermost partner shell turns around; the best R_200 at any epoch reaches min(C, Π) = 0.83–0.85 (z 2.1–2.5). (ii) The
     most-bound S M_b of cold at t_d is 97–100% partner: binding energy preserves the Lagrangian order (also 0.985 at N = 5,000,
     0.99 in H-B). Both are real structure, but the epoch in (i) is set by the galaxy's baryon mass, and (ii) inserts S as the
     threshold. Either way the label (or S) re-enters, as in CFG462/488.

3. **LP-H is G9-clean but is the catchment supply, not the postulate.** Halo partner / (S × the galaxy's baryons) = 1.57 at t_d,
   4.41 at z = 0 (CFG118's 23.63 M_b catchment), and f_b ν(r_ta) = 20–96 for the law's turnaround (implied f_ret,halo 0.041 /
   0.036). Edges: 24.1 r_M (LP-H/inf) and 0.85 r_ta (LP-H/law).

4. **(c) Lensing: the two LP-H catchments bracket the KiDS window and miss it from both sides.**
   - KiDS median x_edge/r_ta: LP-G/LIVE 0.038 / 0.033 (CFG488), LP-H/inf 0.156 / 0.135, LP-H/law 0.849 / 0.848. Window [0.3, 0.5].
   - LP-H/law sits between CFG413's x = 0.7 and 1.0 rows, which KiDS accepts against x = 1 but the growth leg rejects (S < 0.6).
   - **Early-type absolute levels (CFG485 caveat 2) are fixed by any extended edge:** χ² 1.7–2.9 for LP-H and 2.6/2.8 for the
     census-SET edge (f_ret 0.10, reported), against 30.5 / 38.1 at 5.85 r_M (reproduced, K4). So the early-type failure is
     about the 5.85 r_M edge being too small, not about the supply mechanism.
   - LP-G/SET would land in the window at f_ret,gal 0.070–0.117 (CFG488), but the initial conditions do not supply f_ret,gal.

5. **(d) Clusters fail both ways.** LP-G (only dissipated baryons have settled partners): u = 0.79–0.97 for f_* = 0.05–0.20
   (RECALLED, not on disk) against [0.433, 0.628] canonical / [0.368, 0.584] alt; entering the range needs f_* ≥ 0.355 / 0.397.
   LP-H with free placement: u = 0 (CFG488). In-place LP-H (reported) gives 0.452 / 0.389, inside the range, but that placement
   does not carry the galaxy law (CFG488).

## MUTATE (coherent isocurvature: cold/baryon = S·2^(1/2 − m/M_ta), a factor 2 across the catchment)

- The partner becomes 1.277 S M_b and C(R_ta(t_d)) = 1.277 in every q: pairing broken. **TEETH DETECTED** (exit 1).
- Reported: a random per-shell ratio (factor 2, mean-preserving to 2%) gives 0.982. Small-scale isocurvature averages out;
  only coherent, galaxy-scale isocurvature breaks the pairing. The CMB's adiabatic constraint is what the postulate leans on.
- Under MUTATE the LP-G (a) row prints PASS (R_200 at the later t_d, z 2.5, has Π 0.96–1.00). Its C is normalised to S M_b
  while the partner is 1.28 S M_b, so that row is not meaningful; it shows again that R_200 at t_d tracks whatever patch t_d is
  keyed to.

## Controls

- K1 PASS: M_ta/M_b = 23.632, r_ta0 = 507.94 kpc, catchment 23.631 M_b (CFG118/488); partner = S M_b to 1e-12; the two-pass
  runs (turnaround pass, snapshot pass) are identical to 0.
- K2 PASS: purity inside the boundary shell's own radius at t_ta/2 = 0.9996.
- K3 PASS: KiDS LIVE medians 0.0377 / 0.0327 (CFG488).
- K4 PASS: early-type χ² at 5.85 r_M 30.46 / 38.11 (CFG485 R8 30.5 / 38.1).
- K5 PASS: x_e = 5.849761; ν_mono phantom there = S M_b to 4.5e-9.

## Disclosures

- The epoch scan (30 extra snapshots) was added after the first full output, print only. The integrator's results do not
  depend on snapshot times (two-pass identity 0), and every scored number is unchanged.
- Expectations were written in the criteria before the run. They held except: LP-H passes the early-type levels (not
  expected), and the energy rank keeps 97–100% purity (not anticipated).
- The CFG485 machinery is executed read-only up to its C6 banner (its C1–C5 pass inside this run).

## Caveats

- Spherical; settling's back-reaction on orbits is not modelled. The H-N galaxy is a point core present from z = 100, with its
  partners in the inner cold shells (CFG488's set-up), so t_d is the same for every mass. Real haloes have scattered formation
  times; that makes an epoch-based selector harder, not easier.
- The settling drive and energy sink are inherited and still NOT SUPPLIED (CFG462/490).
- The cluster stellar fraction f_* is recalled (U). The KiDS window rests on CFG413's free two-halo term.

## What this leaves

Adiabatic initial conditions do supply the AMOUNT, S × the original baryons, for any patch. They do not supply WHICH patch.
Gravity alone selects the halo's collapsed patch, which gives the catchment (4.4 × too much at z = 0) and edges at 0.14–0.16
or 0.85 r_ta. Selecting the galaxy's patch needs baryon fate, or an epoch or energy threshold that brings the label or S back.
The supply edge stays an input. The new physical clue is that binding energy keeps the partners almost perfectly ordered, so
any future selection rule that reads binding energy, with a threshold not set by S, is the one route left open here.

## Run

```
python3 campaign_fresh_gravity/CFG494_supply_from_adiabatic_ics/cfg494_adiabatic.py                    # exit 0
CFG494_MUTATE=1 python3 campaign_fresh_gravity/CFG494_supply_from_adiabatic_ics/cfg494_adiabatic.py    # exit 1 = teeth
```

Inputs, all read-only: `CFG488_cosettling_supply/cfg488_infall.py`, `CFG118_secondary_infall/shellcore.c`, `CFG4_common`,
`CFG100_kids_mass_rederivation/cfg100_lib.py`, `CFG485_kids_split_settling_completeness/cfg485_settling_split.py` (and its
CFG95/CFG61 inputs), `CFG453_t15_deficit_units/cfg453_results.json`, `real_research/data/lensing_rar/{lr_lenses,cfg110_perlens}.npz`.
