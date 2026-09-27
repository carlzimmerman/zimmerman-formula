# XR14 — the KiDS row on M*'s own carrier

Cross-thread review, 2026-09-26 (night). Read-only on every other file: two new scripts in this folder, controls that
reproduce committed numbers exactly, and a MUTATE run that must fail. Both a0 footings throughout (canonical 9.36e-11,
alt 1.13e-10 m s⁻²). Beyond this lane's own files, the only edits are the XR10 registry row and two signature regexes in
the XR10 validator.

**Why.** DE10 (dabce1b73) passed KiDS-1000 for the converged model: −37.0/−34.0 (hard) and −32.3/−29.3 (w = 0.25) at
600 km s⁻¹. But it re-ran L375's shell model with L375's own trigger, which reads the Newtonian matter density. XR10 flags
that row off M* on the carrier. M*'s carrier is L388's trigger (78fc5dd81), which reads the phantom-inclusive x~.

## Answer: KiDS passes on M*'s carrier, by less than DE10

Δχ² against L352's unswitched model, canonical/alt. Gated as the DE thread set for XR9: fs = 1 and A ≤ 2. The pass bar
is ≤ +4.

| kick (km/s) | M*'s carrier, w = 0.02 | M*'s carrier, w = 0.25 | L388 as written, w = 0.02 | L388 as written, w = 0.25 |
|---|---|---|---|---|
| 575 | −34.25/−31.36 | −29.70/−26.70 | −36.63/−33.61 | −31.91/−28.90 |
| 600 | −34.17/−31.28 | −29.61/−26.62 | −36.58/−33.46 | −31.82/−28.75 |
| 625 | −34.12/−30.94 | −29.57/−26.28 | −36.62/−33.63 | −31.90/−28.91 |
| 650 | −33.96/−30.94 | −29.40/−26.29 | −36.51/−33.50 | −31.80/−28.79 |

For comparison, at the same settings:

| | w = 0.02 | w = 0.25 |
|---|---|---|
| DE10 committed, 600 (L375's carrier) | −37.03/−34.01 | −32.27/−29.29 |
| DE10 committed, 650 | −36.82/−33.74 | −32.08/−29.02 |
| the switch alone (fs = 0) | −28.64/−25.57 | −24.63/−20.71 |

- **H1 passes (pre-declared).** M*'s carrier passes at every kick, both widths, both footings. The worst case is −26.28
  (alt, w = 0.25).
- **Against DE10.** M*'s carrier costs 2.7–2.9 in Δχ² at matched kick, width and footing.
- **H1b passes (pre-declared).** L388's carrier as written lands within 0.6 of DE10 (0.23–0.55 weaker).
- **What the carrier adds.**
  - M*'s carrier improves the score by 4.8–6.0 over the switch alone (w = 0.25); L388 as written by 7.2–8.2.
  - Fitting the amplitude as a diagnostic gives fs = 1.0 at the edge of [0, 1]. On [0, 3], which is unphysical above 1,
    it reaches fs = 3.0 at −33.5/−32.1.
  - KiDS would take more carrier at these radii, not less.
- **The 2-halo amplitude never reaches the cap.** A ≤ 1.69 in every bin for M*'s carrier, and ≤ 1.70 over every fit
  (A per bin is in the `.out` and the results JSON). So the A ≤ 2 and A ≤ 20 (DE10's) scores are identical.
- **The κ cap does not bind (K1).** l_cap(0.25) = 2.35 Mpc. The largest v_f on the fit's mass grid is 298/312 km s⁻¹, below
  v_cap = 325. The κ, uncapped and withdrawn-local scores are identical, and Δf = 0 on the whole grid.
- **MUTATE fails, as it must.** v_k = 0 (triggered, nothing kicked) keeps the no-decay retention and gives
  +133.2…+136.3 on M*'s carrier and +132.6…+133.9 for L388 as written. H1 and H1b fail, rc = 1; DE10's MUTATE gave
  +133/+137.

**What moved.** The trigger reads M*'s phantom, which in the MOND-sector reading reaches ~1–2 Mpc around these hosts.
So the trigger clears carrier far beyond L375's reach. At 600 km s⁻¹ (canonical; alt within 0.005 in S):

| | L375 (DE10) | L388 as written | M*'s carrier |
|---|---|---|---|
| retention S (< 0.5 Mpc/h), bins 0–3 | 0.262, 0.254, 0.237, 0.360 | 0.273, 0.263, 0.240, 0.362 | 0.183, 0.185, 0.184, 0.291 |
| decayed fraction | 0.82–0.84 | 0.81–0.84 | 0.905–0.907 |
| decays the phantom term alone caused | 0 | 1.2–1.6% | 26–39% |
| trigger reach at z_l (kpc) | 188, 246, 322, 496 | 209, 274, 359, 552 | 898, 1114, 1310, 1716 |

- **Monte-Carlo noise is small.** S changes smoothly and monotonically with the kick across four independently seeded runs.
- **L388 as written keeps slightly more carrier than L375.** This comes from L377's Gauss-compensated switch edge.
  - At z > 0.61 its switch threshold 2.5E(z)² exceeds the trigger's 5, so the edge lies inside the Newtonian trigger
    region.
  - The negative compensation there leaves a thin non-triggering band. The mesh has the same negative edge cells, so
    this is L388's construction, not an artefact of the sphere.

## M*'s carrier, read from the code

`XR14_carrier_halos.py` parses L388's cell, rate, mode and kicks from L388's source and asserts eleven defining lines of
L377's `run()` and `phantom()` verbatim (check T0). The rule L388 runs is:

- a cold carrier element decays at Γ = 10 H where x~ = 1.5 Ω_m(a)(δ_m + δ_ph) > 5;
- the daughter gets an isotropic kick v_k, 575–650 km/s;
- δ_ph is the baryons' QUMOND phantom wherever the switch is on, with the vacuum gate [Ω_Λ(a)/Ω_Λ0]^p at p = 1,
  x_c0 = 2.5;
- L388 ran the canonical a0 only.

The rule reads "the phantom", so it needs a switch, and here the code forces a choice:

| label | the phantom the trigger reads | status |
|---|---|---|
| **M\*'s carrier** (`MSPH`) | the phantom of M*'s own gate: MS2's MOND-sector reading, MS5's κ cap, hard, connected to the centre. This is what the same-model PM run L396 feeds its trigger. | the XR10 row |
| **L388 as written** (`L388`) | the phantom switched by L388's own matter-only reading (carrier + baryons), as L377's `phantom()` does at L388's cell | inside M* this mixes switch branches; scored beside it |
| L375 (`L375`) | none: the Newtonian matter density only | DE10's carrier; the C1 control |
| FK1 (`FK1`) | none: FK1's n² trigger on the cold carrier's own density, gate E⁴ (q = 1.75), δ_t0 = 5, sharp | a labelled variant |

Each carrier is run on each footing's a0 and scored on that footing. L388's canonical carrier on the alt footing is
reported as "as run": worst −28.73.

## The shell model and the score

- **The halos.** L375's `halo()` is copied line for line: secondary infall on the fiducial accretion history, the bins'
  baryons (Hernquist + CGM), L390's refitted masses, DE10's seeds, N = 60000, 1 Myr steps. Only the trigger block is a
  choice.
  - N = 60000 took 19–51 s per halo single-threaded, so no reduced-N convergence run was needed.
  - XR9's MOND-sector refit at this cell differs from L390's masses by 0.1 dex in two bins. It moved the L375-carrier score
    by ≤ 0.03.
- **The gate.** DE10's fit on DE8's operator A: σ = 1, 1/m = 0.1 Mpc, MS2's MOND-sector reading, p = 1, x_c0 = 2.5,
  w = 0.02 and 0.25.
- **The cap.** MS5's κ form, U = min(x, (v_cap/(rH))²). It binds only where v_f > v_cap = 325 km s⁻¹; K1 above shows it
  does not bind here.
- **The anti-fake rules.**
  - The carrier's amplitude is fixed at fs = 1.
  - The 2-halo amplitude is capped at A ≤ 2 and scored against the unswitched baseline with the same bound. That baseline
    equals the A ≤ 20 one: the unswitched fit never exceeds A = 0.47.
  - A and log M_b are reported per bin, and DE10's A ≤ 20 is shown beside every score.

## Controls (all exact unless stated)

| check | what it shows | result |
|---|---|---|
| T0 | L388's trigger definition read from source; 11/11 lines verbatim | pass |
| C3 | the shell model's spherical phantom against L377's own `phantom()` on an 80³ mesh at L388's cell: switch edge 1.099 vs 1.096 Mpc/h (cell 0.1); enclosed phantom within 0.6–1.4%; both compensated beyond the edge | pass |
| C0 | the fit loop's baseline equals L352's (0e+00) | pass |
| C1 | with L375's trigger restored: histograms identical to XR9's cache of L375's own `halo()`; S equals L390's committed S (0e+00); DE10's full committed table and preferred amplitudes reproduced (0e+00) | pass |
| C2 | the no-decay (CDM-like) carrier on M*'s gate: +128.7/+131.5 | rejected, as it must be |
| C3b | the gate M*'s carrier's trigger reads is the scored gate: hard edges within 0.18% at z = 0.25 and 1, M_b = 1e11 and 1e12, including where the κ cap binds | pass |
| K1 | the κ cap is non-binding on KiDS lenses | pass |
| MUTATE | v_k = 0 in every scored carrier: +133.2…+136.3 (M*), +132.6…+133.9 (L388 as written); every control above still passes | H1 and H1b fail, rc = 1 |

## FK1's conversion (variant)

FK1's pair instability grows as n² on the heavy (cold) component's own density. Its gated coupling puts the threshold at
n_t(z) = 5 n̄_c0 E(z)⁴, sharp.

- **It can be expressed in the shell model.** Every cold element in a bin above n_t converts in that step and is kicked
  at v_k.
- **It retains the least carrier.** S = 0.164–0.166 in bins 0–2 and 0.269 in bin 3, with 93% converted and the conversion
  front at 260–686 kpc at z_l.
- **KiDS still passes:** −31.4/−28.4 (hard) and −26.7/−23.7 (w = 0.25) at 575; worst −23.50.
- **Not modelled:** the √σ halo modulation FK1 flags, an O(1) estimate.

## The XR10 row (`XR14.kids`)

`XR10_answer_validator.py` classifies the row **ON-M\*~**. It traces two stages from code:
- `kids_gate`: this lane's fit on DE8's operator;
- `carrier_trigger`: the shell model's trigger, with its own switch, cap, width, kernel and operator.

| axis | status |
|---|---|
| switch, both stages | MATCH (MOND-sector reading) |
| cap, both stages | MATCH (MS5's κ form) |
| p, x_c0 (the gate's, and L388's cell via the trigger) | MATCH |
| w: kids_gate 0.02/0.25 | MATCH |
| w: the trigger's hard switch | COMPAT `[HARDW_FOR_SMOOTH]` |
| kernel (ν_mono), σ = 1 | MATCH |
| operator: kids_gate A | MATCH |
| operator: the trigger's phantom (L377's form, B) | COMPAT `[OP_B_FOR_A]` |
| carrier (`L388_density_trigger`, from `XC_TRIG = L77.XC_TRIG`) | MATCH |
| kicks 575–650, both footings, epoch 0.25 | MATCH |

Two regexes were added to the validator's signature table, for the MOND-sector reading and the κ cap as the shell model
writes them in its own units. No other row's classification changed; rc = 0, and the validator's own MUTATE still fails
on check D.

The claim is `pending` because nothing here is committed. Re-evaluated in memory with the claim set to `M*`, the row
fails only on "[not committed]": set the claim to `M*` once the lane is committed.

As a row, L388 as written would be OFF-M*: a matter-only switch inside the carrier's trigger stage.

## Scope

- The lenses are spherical and isolated. There is one accretion history, and the baryons are static.
- The shell model has no cosmic background beyond the halo's own infall, so x~_m falls below zero past ~1 Mpc and the
  trigger's reach there comes from the phantom alone.
- The trigger's phantom is sourced by the shell model's baryons (galaxy + CGM). The lens gate reads L352's point-mass lens
  (M_b only).
- The trigger's phantom uses L377's spherical QUMOND form with a hard switch; the lensing uses operator A with the smooth
  gate.
- The gate's phantom is read ungated (the on-branch convention), and the heat filter is omitted.
- The trigger and the cap are posited: neither has an action for the trigger.

## Files (only these)

| file | what it is |
|---|---|
| `XR14_carrier_halos.py` | the halos (T0, C3 and H1 inside), resumable cache |
| `XR14_carrier_halos.out` | two chunked calls: 68 halos, then the M* carrier at 600 and 625 km s⁻¹ |
| `XR14_carrier_halos_results.json` | the halo cache: 84 halos |
| `XR14_carrier_halos_MUTATE.out` | the MUTATE halos' log |
| `XR14_carrier_halos_results_MUTATE.json` | the MUTATE halo cache: 24 halos, v_k = 0 |
| `XR14_kids_mstar_carrier.py` | the score |
| `XR14_kids_mstar_carrier.out` | 13/13, rc = 0 |
| `XR14_kids_mstar_carrier_results.json` | the score's results |
| `XR14_kids_mstar_carrier_MUTATE.out` | 11/13: H1 and H1b fail, rc = 1 |
| `XR14_kids_mstar_carrier_results_MUTATE.json` | the MUTATE score's results |

Plus the `XR14.kids` row in `XR10_answer_rows.json` and two regexes in `XR10_answer_validator.py`.

Run from the repository root, in order:

1. `XR14_MAXN=200 python3 real_research/cross_thread_review_2026_09_26/XR14_carrier_halos.py`: about 65 min
   single-threaded; resumable. Add `MUTATE=1` for its v_k = 0 cache (about 20 min).
2. `python3 real_research/cross_thread_review_2026_09_26/XR14_kids_mstar_carrier.py`: about 6 s. Add `MUTATE=1` for the
   control.
3. `python3 real_research/cross_thread_review_2026_09_26/XR10_answer_validator.py`
