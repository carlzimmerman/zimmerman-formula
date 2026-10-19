# CFG853: granular (fragment) dynamical-friction transport of the dSph cold core. EXCLUDED (Sextans-independent); the stellar receiver is not excluded

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in cbe934afe, before any script existed. The script is
`cfg853.py`: one core, `nice -n 19`, numpy/scipy/sympy, about 1 s, well under 1 GB. The running 1024³ jobs were not touched.

- Main run: `nice -n 19 python3 cfg853.py` writes `cfg853.out` and `cfg853_results.json` (deterministic). It exits 0 because
  every control passes.
- `CFG853_MUTATE=1` writes `cfg853_MUTATE.out` and `cfg853_results_MUTATE.json`. It exits 0 because the mutation bites.

κ = ½ is FITTED. Both footings are scored separately and never pooled. No dark-matter species is added: the cold energy's
mass is still required, and its amount (53.64 M★ = 5.364/0.1) is an input. This is not "theory closed", and nothing here
says the data favour the framework over ΛCDM.

## The question

The handoff (`sol61_push/HANDOFF_TO_CLAUDE_COLD_CORE_TRANSPORT_2026-10-19.txt`) asks for a physical way, inside the
framework, for cold mass to shed energy AND angular momentum and pile up in Draco and Sextans without over-boosting Fornax
and Leo I.

This lane tests one mechanism. The free cold energy is broken into self-bound lumps of mass m (ARGON11's low-density
branch). The lumps sink by Chandrasekhar dynamical friction against the light populations: diffuse cold energy, settled
cold, stars, and gas while it is present.

- Friction removes orbital energy and angular momentum together. It puts them into the light populations, so it is a
  reciprocal cold → light heat/torque transport.
- It needs no new interaction.
- It acts inside each dwarf, so it is host-, gas-loss- and age-independent from the start, as CFG843, CFG838/839, CFG852,
  CFG860 and CFG827 require.

**Not tested here:** the non-gravitational part of the fragment route (capture or fusion in the M100 action).

## Inputs

All inputs follow the handoff convention, which K1 reproduces:

- **Dwarf data.** LVD M_V, a, σ. Υ_V comes from the CFG827 SFH fits; Sextans has Υ = 2 assumed.
- **Aperture.** R = 4a/3.
- **Settled cold.** s = min[p(√(¼ + 1/y) − ½), 5.364].
- **Reservoir.** M_rem = (53.64 − s) M★, placed outside R.
- **Need.** M_x = M★[3Rσ²/(GM★) − p − s], and F = M_x/M_rem.
- **Allowance.** A is M_x evaluated at σ + 2σ_err.

| | M★ [M_⊙] | R [pc] | M_rem | needed M_x | F | allowed A |
|---|---|---|---|---|---|---|
| Draco | 5.74e5 | 258 | 2.77e7 | 1.30e7 | 0.469 | 1.48e7 |
| Sextans | 5.26e5 | 648 | 2.54e7 | 2.51e7 | 0.989 | 4.67e7 |
| Fornax | 1.98e7 | 927 | 9.90e8 | 1.29e7 | 0.0131 | 1.93e7 |
| Leo I | 3.70e6 | 305 | 1.88e8 | 6.50e6 | 0.0345 | 8.62e6 |

The model treats all four dwarfs with one law:

- **Reservoir shape.** ρ ∝ r⁻² from R out to the record's catchment radius r_ta (CFG822; geometry G1), or out to 5R
  (geometry G2, the handoff's compact cloud scale).
- **Fragment fraction.** One common lump fraction, φ = max(F_Dra, F_Sex) = 0.9885.
- **Friction.** Chandrasekhar friction against the light background, with B(1) on circular orbits.
- **Common clock.** One common product Q = G²m lnΛ t. lnΛ is common to all four; this is permissive for the guards (Fornax
  and Leo I), whose R·V_c² is 3.5–26× Draco's, so their true lnΛ is larger.

## Result. CLASS: **EXCLUDED (Sextans-independent), stellar receiver not excluded**, on both footings

**T2 (graded): the four-dwarf test with one law.** The table gives delivered/allowed for each dwarf, at the common clock
that delivers both the Draco and Sextans cores.

| footing, geometry | Draco | Sextans | Fornax | Leo I | T2 |
|---|---|---|---|---|---|
| canonical G1 (r_ta) | 1.69 | 0.54 | **5.98** | **5.77** | FAIL |
| canonical G2 (5R) | 1.86 | 0.54 | **18.2** | **21.6** | FAIL |
| alt G1 | 1.69 | 0.54 | **9.54** | **6.46** | FAIL |
| alt G2 | 1.86 | 0.54 | **29.6** | **24.6** | FAIL |

The Sextans-independent check (T2-D: φ = F_Dra, Draco's own clock, guards only) also fails:

| T2-D | Fornax | Leo I |
|---|---|---|
| canonical G1 | 2.24 | 2.92 |
| canonical G2 | 2.58 | 5.56 |
| alt G1 | 3.47 | 3.26 |
| alt G2 | 4.08 | 6.28 |

**Post-hoc φ envelope.** This was added after the primary result was seen; it is reported only and cannot change the class.
- No common fragment fraction rescues the mechanism.
- Over φ ∈ [F_Dra, 0.999], the smallest worst-case guard over-fill is ×2.8 (canonical G1), ×5.6 (canonical G2), ×3.2 (alt G1)
  and ×6.3 (alt G2).

**Why it fails, in plain terms.**
- How much friction delivers depends on size, velocity and the background, and the supply is proportional to the stars
  (53.64 M★).
- Leo I has the same size and σ as Draco but 6.4× the stars and 6.8× the reservoir. Fornax has 36× the reservoir.
- So the friction clock that fills Draco delivers a similar or larger fraction of a much larger reservoir into Fornax and
  Leo I. Yet Leo I needs *less* absolute extra mass than Draco (0.65e7 against 1.30e7).
- The MUTATE run shows the size of the problem. With friction-consistent dispersions injected at Draco's clock, the same law
  predicts:
  - Leo I: σ = 13.3 km/s (G1) or 17.7 km/s (G2), against 9.29 ± 0.26 observed;
  - Fornax: σ = 15.3 km/s (G1) or 15.2 km/s (G2), against 12.10 ± 0.20 observed.

**T1 (graded): the stars as heat receivers.** The Rosenbluth coefficients (K2) show that a light species is heated at a rate
that does not depend on its own mass. So stars and diffuse cold energy take the transit energy equally per unit mass.

Heating of the stars, Δε★, as a fraction of the permissive tolerance V_c,need² ln 10:

| | Draco | Sextans |
|---|---|---|
| G1 | 0.24 | 0.46 |
| G2 | 0.21 | 0.44 |

- T1 passes, because the settled (tethered) cold inside R, s M★, takes about 82% of the heat.
- Under the strict tolerance ln 2, Sextans fails (1.45–1.54) and Draco passes (0.70–0.81).
- Consequence, not graded: the settled tethered cold absorbs about 1.5–3 σ² per unit mass, so it would no longer sit at
  rest on the law profile (compare Codex's virial obstruction).

## Reported (not graded)

- **R1: persisting lumps are ruled out by stellar heating.**
  - If lumps survive as lumps inside R, they keep heating the stars. m cancels when delivery just finishes at t★.
  - Post-arrival heating relative to the tolerance:

    | | Draco | Sextans |
    |---|---|---|
    | G2 | 66× | 288× |
    | G1 | 1.4e4× | 1.0e4× |
    | G2, total-background variant | 1.3× | 4.0× |
    | G2, binary-corrected Sextans | 7.7× | 12.8× |

  - So any working version needs the lumps to merge into a smooth core on arrival. That is the non-gravitational capture
    question, which is still untested.
- **R2: the relaxation channel (lump–lump, gravothermal).**
  - The stars gain 1.205 σ² per lump relaxation time, independent of m. They pass the permissive tolerance after 5.7
    relaxation times, and the strict one after 1.7.
  - Energy growth needed, |E_f|/|E_i|, with the remainder dispersed to E = 0 and a uniform final core (an SIS final core in
    brackets):
    - G1: Draco 7.2 (11.9); Sextans 14.8 (24.7).
    - G2: Draco 0.99 (1.64); Sextans 3.5 (5.8).
  - Escapers from diffusive relaxation leave with E ≈ 0. For Sextans the escapers would need 124–163 × σ²/2, so the channel
    fails for Sextans at its central inputs.
  - Sextans variants: binary-corrected (CFG861) gives 1.66 in G2 (escapers at 1.55 × σ²/2); σ − 2σ_err gives 0.70 (passes).
  - Draco's G2 relaxation endpoint is energetically allowed. Here the stellar heating per relaxation time is the binding
    constraint.
- **R3: angular momentum is not the binding constraint.**
  - Suppose the angular momentum J is deposited with the same mass share as the energy.
  - Then the stars spin up to 0.5σ only if the delivered mass carries net rotation λ_crit = 0.37–0.47 (Draco) or 0.19–0.21
    (Sextans) of its circular specific angular momentum.
  - Isotropic lumps mostly cancel their J. Energy, and the four-dwarf supply mismatch, are what bind.
- **R4: variants.** None of these changes T2 or the class: Sextans binary-corrected or at σ − 2σ_err, strict tolerance,
  per-dwarf φ, total background, initial static potential, G0 receivers. The strict tolerance alone changes the T1 sub-label
  to "stars cannot be the receiver".
- **D1: diagnostic that applies to any mechanism.**
  - No single non-decreasing extra-mass profile M_x(r) fits all four dwarfs.
  - Draco needs at least 1.13e7 M_⊙ inside 258 pc even at σ − 2σ_err. Leo I is allowed at most 8.62e6 inside 305 pc at
    σ + 2σ_err. That is a 1.32× conflict (alt 1.50×).
  - So any successful mechanism must give a fainter dwarf more absolute extra mass at the same radius and σ. The delivered
    fraction must fall steeply with M★ or with g_bar (Draco 0.47 against Leo I 0.035 for 6.4× the stars). It must not
    follow supply or kinematics.

## What it leaves open

1. **Fragment coalescence or capture.** This is the handoff's priority A and needs the actual M100 action. R1 shows it is
   needed anyway. But any capture-assisted transport whose rate depends on size, velocity or supply meets the same
   four-dwarf mismatch unless its efficiency falls steeply with M★ or g_bar at fixed R and σ (D1).
2. **A selector tied to the internal baryonic acceleration** (CFG828), which friction does not see.
   - A coincidence was noticed post hoc: the settled-cold cap binds below log g_bar ≈ −12.1 (canonical) or −12.0 (alt),
     close to CFG828's −12 boundary.
   - Leo II is uncapped yet has Δ_SFH ≈ +0.36 (CFG861 table), so this is not a clean switch. It was not pursued.
3. **Reservoir geometries that differ from dwarf to dwarf.** This is the initial-condition route, and CFG844/845 already
   constrain it.
4. **The Sextans inputs** (Υ, σ, binaries). The verdict does not rest on them: T2-D uses only Draco, Fornax and Leo I.
5. **SPARC small dwarfs.** Not run, because the mechanism already fails on the dSph guards.

## Controls

- **K1: PASS.** The script reproduces CE-FM-084 and the handoff to 1e-9 against its saved values:
  - baseline σ: Draco 4.333888, Fornax 11.242388, Leo I 7.468185;
  - F: Draco 0.4693028, Sextans 0.9885403, Fornax 0.0130695, Leo I 0.0345131;
  - M_rem: 2.77236e7, 2.53958e7, 9.90289e8, 1.88437e8.
- **K2: PASS.**
  - sympy verifies the identity 2vh′ + 2h = (4/√π)X e^{−X²}/v.
  - Quadrature of the massless-test heating rate over the test Maxwellian matches the closed form
    8√(2π)σ_L²/(σ_L² + σ_s²)^{3/2} to ≤ 8e-10 relative, in four cases.
  - The equal-σ coefficient is 4√π.
- **K3: PASS.** The same machinery in a singular isothermal background gives 1.1693, against BT08 eq. 8.13's 1.17.
- **K4: PASS.** The Plummer fraction inside 4a/3 is 0.512.
- **MUTATE bites on both footings and in both geometries.** Injecting the dispersions that the friction law would produce
  (at Draco's clock, φ held fixed) makes T2 pass, with all ratios 0.32–0.93.

## Disclosures

- Two items were added after the primary result was seen; both are reported only and enter no graded cell:
  - the post-hoc φ envelope;
  - the R1 column in the variant lines.
- K1's σ check was first coded as |Δ| ≤ 5e-4 (the printed precision). Before the final run it was aligned to the frozen
  1e-4 relative rule. The values pass both rules, and match CE-FM-084's saved values to 1e-9.
- Model limits:
  - static initial potential for the friction step;
  - circular orbits;
  - local Chandrasekhar approximation;
  - no wake self-gravity (tethered self-gravity cancels in Codex's functional, which would weaken friction equally in all
    four dwarfs);
  - no core stalling.
  All of these are common to the four dwarfs, so the T2 ratios are insensitive to them to first order. That is a judgement,
  not a computation.

κ fitted; cold energy mass required; not theory closed.
