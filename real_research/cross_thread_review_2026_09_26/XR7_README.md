# XR7 — one number for the kick and the cap?

**The claim tested** (a parallel synthesis, 2026-09-26, not committed): the carrier's kick (~600 km/s; L388's window
575–650) empties every system whose escape speed is too low, and deeper wells keep most of their carrier. Cosmic shear
(MS3 K1) needs MOND regions capped near 1.75 Mpc at z = 0.5, i.e. v_cap ≈ 325 km/s (M_b ≈ 9e11 M☉). The claim says the
cap is about half the kick speed and equals the escape speed of the systems the kick empties, so one number sets both.

**Verdict: the two scales do not coincide.** The retention transition sits 2.2–2.6× above the cap. The arithmetic
v_cap ≈ v_k/2 holds (0.50–0.57), but that is not where the committed retention changes, and v_cap is a circular speed,
not an escape speed.

Script: `XR7_kick_escape_vs_cap.py`. It reads committed JSON and source text only; no lane is imported or run, and
nothing outside this folder was touched.

## What the committed retention says

The data are L388's per-halo retention: 120 peaks in 3 boxes, 118 of them at ≥ 6e13 M☉/h, where
eps = carrier within 1 Mpc/h over LCDM's, at z = 0.

| Kick (km/s) | 50% retention: v_c(1 Mpc/h) | v200 | escape speed at 1 Mpc/h (Φ(∞) = 0) | ÷ v_cap | canonical X-COP floor (0.286): v_c |
|---|---|---|---|---|---|
| 575 | 702 | 737 | 1306 | 2.16 | 588 (below the lowest bin centre, inside the data) |
| 600 | 768 | 795 | 1445 | 2.36 | 621 |
| 625 | 817 | 838 | 1549 | 2.51 | 662 |
| 650 | 849 | 866 | 1619 | 2.61 | 714 |

- **Uncertainties.**
  - Three estimators (the lanes' L371-bin medians, a logistic, isotonic regression): 702–895 km/s.
  - Halo bootstrap (95%) and per-box values: 660–934 km/s.
  - Including the two peaks below 6e13 changes the logistic by < 3%.
  - L380's p = 2 cell gives the same to 1–3%.
- **Most favourable case for the claim: 602 km/s.** This is the lowest plausible 50% crossing over every kick,
  estimator, bootstrap tail, box and circular convention, including both footings' baryonic flat speed
  (G M_b a0)^¼. It is still 1.67× the top of the cap band (247–361 km/s: from the largest KiDS lens's v_f up to MS3's
  interpolated edge).
- **Against the kick.** v_c,50 ≈ 1.22–1.31 v_k. It grows faster than the kick: v_c,50 ∝ v_k^1.6 (L388; 1.1–1.8
  across L380 and L366). So even the ratio to the kick is not fixed.
- **In escape speed.** The transition's escape speed is 4.5–5.0× v_k/2 at 1 Mpc/h and 3.8–3.9× at the trigger
  radius.
- **In baryonic mass.** The half-retention hosts hold 14–25× M_b,cap in observed bound baryons on the canonical
  footing (M_b,cap 9.0e11 M☉), and 17–31× on the alt footing (M_b,cap 7.5e11).

## The kick physics

- **The exact relation.** For an isotropic kick,
  f_unbound = clip(((v_o + v_k)² − v_esc²) / (4 v_o v_k), 0, 1). C3 checks it against Monte Carlo to 0.001.
- **I27 is correct, but it is the f = 1 edge.** Its v_k > |v_o| + v_esc means every kick direction unbinds the
  daughter. It is not the transition.
- **Half the daughters leave when v_k² = v_esc² − v_o²,** i.e. when the kick supplies the binding energy.
- **Where v_esc = v_k/2 comes from.** It is the every-direction edge only for daughters that already move at the
  escape speed (marginally bound infall), and there the unbound fraction never drops below ½.
- **L321's criterion is right.** L321's `retained()` (L371's S2 shape) keeps a daughter iff E < 0 in the post-decay
  potential. That is the correct energy criterion.
- **A static single halo reproduces "half the kick".** Take an NFW halo with isotropic Jeans velocities and let all
  of its carrier decay at once. Half-retention then falls at v200 = 0.46 v_k (Φ(∞)) or 0.62 v_k (Φ(2 r200)), i.e.
  264–404 km/s, which overlaps the cap band. The construction's own runs, which include assembly, put it 1.8–3.3×
  higher.

## The emptied end, and MS3's own rows

- **What the resolved runs empty.** L375 and L376 empty hosts up to v200 ≈ 264 km/s: they keep 8–17% of decayed
  daughters within 0.5 Mpc/h, and essentially none inside galaxies. Before decay, these hosts' escape speeds reach
  494 km/s at r200 and 886 km/s at the centre, well above v_k/2.
- **The cap sits in an unmeasured gap.** Where emptying stops lies somewhere between v200 ≈ 264 and v_c ≈ 531 km/s,
  and the cap falls in that gap. The only two committed peaks there (v_c 390–401 km/s) keep 0.69–1.30. So the cap
  can at most mark where emptying ends. It is not where "deeper wells keep most".
- **MS3's own K1 rules out a transition at the cap.** Its committed `cleared<1e13` row is a retention step at
  v200(z = 0.5) = 337 km/s, which is the one-number scenario. It fails the 1.75 Mpc cap (worst R 1.64/1.74 against
  1.2), and passes only up to about 1.1 Mpc (about 206 km/s, 0.61× the step). **The shear pass needs the carrier
  cleared in groups and clusters above the cap, so the separation between the two scales is load-bearing.**

## What this means for "one number"

No single number sets both. An action with one velocity parameter would also have to produce the ratio
v_50/v_cap ≈ 2.2–2.6, and that ratio drifts with the kick. That makes it a second number, and it is not derived.

## Limits

- **Mesh and footing.** The retention comes from a 0.39 Mpc/h mesh, at z = 0 and on the canonical footing only.
  L375 found the mesh under-retains in small halos.
- **The cap was scored at one kick.** MS3 computed it with v600's retention only, so how the allowed cap moves with
  the kick is not computed.
- **MS3's group-scale retention is interpolated.** For 1e13–6e13 it is interpolated, and the shear pass is
  sensitive to it: worst R is 1.05 with L388's retention against 1.64 with the step.
- **The cap edges are interpolated.** The 341/361 km/s edges are linear interpolations of MS3's grid, not runs.

## Hand-offs (the owners' calls)

1. **A resolved group/cluster retention.** Run L375/L376's shell model at M200 = 1e13–3e14 to see how much of the
   separation is the mesh.
2. **MS3's K1 at other kicks.** Re-score it with the 575 and 650 retention.
3. **Per-halo group retention.** Measure it at 1e13–6e13 M☉/h.

## Checks

- **C1:** 69 committed L388/L380/L366 retention numbers reproduced exactly.
- **C2:** MS3's v_cap, M_b,cap, the KiDS v_f values and GP0's bound baryons reproduced (relative difference 0).
- **C3:** the unbinding formula matches Monte Carlo, and I27 is its f = 1 edge.
- **T0 (load-bearing):** a mass transition exists at every kick, with Spearman ρ = +0.60 to +0.65 at p < 1e-12.
- **V1:** the claim, reported either way.
- **Result:** main run 5/5 (rc = 0). MUTATE=1 scrambles the pairing between retention and mass: ρ becomes −0.04 to
  −0.06 (p ≈ 0.6), T0 FAILS, and rc = 1.

## Files and reproduction

- `XR7_kick_escape_vs_cap.py`
- `XR7_kick_escape_vs_cap.out` and `XR7_kick_escape_vs_cap_MUTATE.out`
- `XR7_kick_escape_vs_cap_results.json` and `XR7_kick_escape_vs_cap_results_MUTATE.json`

Run from the repository root:

```
python3 real_research/cross_thread_review_2026_09_26/XR7_kick_escape_vs_cap.py
```

Add `MUTATE=1` for the control. It is single-threaded and takes about 15–25 s.
