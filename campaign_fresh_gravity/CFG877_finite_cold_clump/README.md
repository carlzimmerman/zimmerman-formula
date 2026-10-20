# CFG877 — a finite cold clump, with no new parameter, across every dwarf sample

Criteria: `FROZEN_CRITERIA.md` (37fd77c59, committed alone before the script; owner block 870–879). Run: `python3 cfg877.py`
(`CFG877_MUTATE=inf|tenth` → separate outputs). Seconds, numpy only. κ = ½ fitted; ν_e; footings never pooled.
**Post-hoc (disclosed in the criteria):** chosen after CFG876 broke the extended form, and CFG876's 33 dwarfs were already seen.
No number in the model was tuned here.

## Model
One self-gravitating cold-energy clump per dwarf, fixed by one number from earlier lanes:
- σ = V_x/√2 = 7.53 km/s (CFG870);
- total mass M_cl = 81σ⁴/(4 G a0) = **5.3e6 M_⊙** canonical / 4.2e6 alt (CFG871's deep-regime relation);
- CFG870's cored shape (r_c 104 pc), capped at M_cl, so the clump's mass stops growing at r_t = G M_cl/V_x² ≈ **200 pc** (163 alt).

## Result — CLASS: **PARTIAL** (canonical: M31 + field at 2.2 se; alt: FINITE CLUMP HOLDS)
| sample (each scored as in its source lane) | N | canonical E = ⟨ln σ_obs/σ_pred⟩ | alt E |
|---|---|---|---|
| MW classical dSphs (CFG870 calibration) | 10 / 9 | +0.085 ± 0.069 | +0.100 ± 0.079 |
| M31 + field (CFG870 T2) | 17 | **+0.121 ± 0.055 (2.2 se)** | +0.112 ± 0.057 (2.0 se) |
| literature-σ UFDs (CFG870 T3) | 21 | −0.064 ± 0.101 | −0.058 ± 0.099 |
| large out-of-sample (CFG876 B) | 18 | **+0.021 ± 0.095**; 1 individual failure (Crater II −3.9σ) | +0.021 ± 0.096; 1 |
| small out-of-sample (CFG876) | 15 | +0.005 ± 0.134 | +0.019 ± 0.133 |
| SPARC small rotating dwarfs (D) | 56 | +0.029 ± 0.022 | −0.006 ± 0.022 |

**Reading.**
- **Every sample sits within ~2σ.** The finite clump does what neither earlier form did. CFG876's large dwarfs go from
  −0.20 ± 0.10 (extended form, BROKEN) to +0.02 ± 0.10, and the calibration and in-sample groups stay put.
- **The one individual failure is Crater II.** The law alone already over-predicts it (3.9 against 2.3 km/s). No external
  field or tides are modelled, so it is a limit of the law, not of the clump.
- **The remaining tension is the M31 + field group at +0.12 (2.2 se),** where the clump is slightly too small. This matches
  CFG872's strike: a few extreme compact dwarfs (Andromeda V, VI, XI) need more than one universal clump supplies.

**What it says about cold energy:**
- **Each faint dwarf carries one bound cold-energy clump.** Its velocity is σ ≈ 7.5 km/s, its mass ≈ 5e6 M_⊙ and its extent
  ≈ 100–200 pc.
- **Its mass and size follow from σ through the law,** as a self-gravitating deep-regime isothermal: M = 81σ⁴/(4Ga0),
  r_c ≈ (9/2)σ²/a0. That works only if cold energy's own gravity follows the law, which this fit supports but does not prove.
- **One number remains underived:** σ ≈ 7.5 km/s, equivalently M_cl ≈ 5e6 M_⊙. CFG876 rules out reading it as a universal
  bath temperature (an extended atmosphere).

## Controls
- **K1 PASS:** with M_cl → ∞ the script reproduces CFG870 T2 (|diff| 2e-17) and CFG876's primary (0).
- **MUTATE:** M_cl → ∞ → FAILS-OVER (CFG876's result); M_cl × 0.1 → FAILS-UNDER. The test bites on both sides.

## Disclosed limits
Post-hoc model choice. No per-dwarf scatter in M_cl (CFG872 found 0.52 dex). No EFE or tides. Υ as in each source lane.
