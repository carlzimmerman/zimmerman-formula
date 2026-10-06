# CFG346: is CFG337's stable (smeared) switch edge acceptable to the data?

Criteria: `FROZEN_CRITERIA.md` (188df575b, committed alone first). κ = ½ FITTED; ν_mono; both footings. The cold mass is
still required; no dark-matter particle. Nothing here closes the theory.

**Frozen verdict: PARTIAL.** The best stable configuration passes KiDS and growth, and fails SPARC. That configuration is
C2 (baryon-density door), R = 4, local E_c, ℓ = ℓ_min = 378.5 kpc. The unit-level diagnostic (f_in = 1, smearing only)
gives the same 2 of 3.

The model: f = f_in φ², where φ is the screened-Poisson smoothing of B's sharp edge Θ(r_ta − r), with range ℓ/√(2 f_in).
The declared interior level is f_in = 1 + 2/R. The phantom density is multiplied by f.

| configuration (ℓ_min = max over 1e5/1e6 K) | ℓ | KiDS Δχ² can / alt (≤ 9) | SPARC | growth |
|---|---|---|---|---|
| C2 R4 local, declared (f_in 1.5) | 378.5 kpc | **−46.4 / −41.7 P** | **F**: A3 spirals 0.03/0.00, dwarfs 0.31/0.27; Δrms +0.026/+0.047 | P |
| same, ×1.5 | 568 kpc | −37.5 / −35.1 P | F (Δrms +0.025/+0.040) | P |
| C2 R4 local, unit (f_in 1) | 378.5 kpc | −10.7 / −10.9 P | **F**: spirals 1.00, dwarfs 0.13/0.16; Δrms +0.012/+0.006 | P |
| C2 R40 local, declared (1.05) | 738 kpc / 1.11 Mpc | +23.9 / +16.7 F; +110 / +87 F | F | P |
| C1 local R4 / R40 | 2.9–6.0 Mpc | +408 to +1030 F | F (A3 0) | P |
| any universal E_c (one constant: C1 293/928 Mpc, C2 29/92 Mpc) | ≥ 29 Mpc | ≈ +1070 F (the switch never turns on: Newtonian) | F (Δrms +0.296) | P |

Reported only, not stable for 1e5 K gas: C2 R4 local at the 1e6 K ℓ_min of 183 kpc. Declared level: S fails. Unit level:
spirals 1.00, dwarfs 0.84 (just under 0.90), Δrms +0.0005, KiDS −12. Even this unstable corner misses on the dwarfs.

**Why SPARC fails:**
- **Declared level.** R = 4's overshoot (f_in = 1.5) adds 50% to the phantom, and that breaks every disc.
- **Unit level (smearing alone).** The dwarfs' own turnaround radii (a few hundred kpc; the SPARC median is 990 kpc) are
  comparable to ℓ_min. A light switch cannot fill a region smaller than its own length, so the dwarfs lose their phantom.
- **R = 40.** It removes the overshoot but doubles ℓ_min, and then KiDS fails too.
- **The single-constant versions** (universal E_c) never switch on at all.

**Growth:** G1 holds for every ℓ. On FRW with |δ| ≪ 1 the trigger is OFF (U ≤ 0.09), so f = 0 identically. The largest
tail at 20 h⁻¹ Mpc is 4e-8, against CFG324's limit of 1.2e-3. Smearing does not leak onto linear scales.

**Declared constants.** These are beyond κ = ½; the owner's rule is zero, so they are a cost, not a pass.
- The best configuration adds ℓ (μ0), R (E_c) and Δ_e. Its E_c is set per system, which is a free function, not a
  constant, so that configuration is not a single-constant action.
- The legal single-constant versions add 3 (C2) or 4 (C1, which also inherits DE12's w and Umax). They fail everything.

X-COP (reported only): r_ta ≈ 12 Mpc, so local configurations keep f ≈ f_in at 1–2 Mpc, while universal ones give f ≈ 0–0.03.

## Controls
- **C0a.** ℓ = 0 reproduces CFG4_switch K3's law χ² 162.605 / 154.758 (|Δ| 0), its sharp turnaround edge at −9.1767 / −9.2959,
  and CFG39's rms0 of 0.100328994.
- **C0b.** ℓ = 5 kpc lands within 0.09 of sharp.
- **C0c.** A sharp edge at r_ta leaves SPARC unchanged.
- **C1.** The H4 ratio at 0.5 ℓ_min is 2 for every configuration, so the instability returns below ℓ_min.
- **MUTATE** (ℓ = 10 ℓ_min). Every configuration fails K and S; the best one has KiDS at +700 / +642. The test is sensitive.

## Lean
`CFG346_smeared_certificates.lean`: 13 theorems, Mathlib, no sorry, standard axioms. The output is in the `.out` file.

## Run
```
python3 campaign_fresh_gravity/CFG346_smeared_switch_vs_data/cfg346_smeared_switch.py                  # rc 0, ~7 s
CFG346_MUTATE=1 python3 campaign_fresh_gravity/CFG346_smeared_switch_vs_data/cfg346_smeared_switch.py  # rc 0, *_MUTATE outputs
cd fable_independent_2026/lean_2026 && lake env lean <abs path>/CFG346_smeared_certificates.lean
```
Harnesses are exec'd read-only, as in CFG340: the FP1 KiDS slice with the FP20 projector, the CFG45 prefix, the
CFG4_galaxy_law prefix, and the CFG337/CFG4_switch JSONs. Nothing was downloaded.

**Scope:**
- The trigger is saturated inside r_e (the T = 1 − 1/U taper is dropped).
- The interior Compton length is also used outside.
- Systems are spherical, static and isolated, with point-mass baryons for r_ta.
