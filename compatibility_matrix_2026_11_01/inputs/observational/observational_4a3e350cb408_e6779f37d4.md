# NR3_ur1_on_nr2: SIGN FLIP YES, AMPLITUDE FAILS [NOISE-LIMITED]. NR2's η doesn't rescue UR1. EM1 + response stays at Υ 0.35 / 0.36, and only NR2's low band reaches the line, where the tilt and LITTLE THINGS fail

Criteria: `FROZEN_CRITERIA.md` (645bdf801e), committed alone first. `nr3.py`, `nr3.out`, `nr3_results.json`, `nr3_{MEDIAN,LOW,HIGH}_results.json`. UR1's rule and tail, read only. κ = ½ FITTED, unused here. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** UR1, UR2, UR3 and NR2 were read. The first attempt stopped on a path bug in my driver before any number; no line moved.

## Canonical, f★ 0.034
| Input ρ₁₀, ρ₁₁ | Row | Υ A/B | rms A | tilt A | keys | Groups Z | X-COP mean, rms | LITTLE THINGS A |
|---|---|---|---|---|---|---|---|---|
| **MEDIAN** 1.241, 1.147 | EM1, off | 0.75/0.76 | 0.0690 | +0.59 | 12 | +1.47 | −0.160, 0.186 | +0.153 |
| | **EM1, Blumenthal** | **0.35/0.36** | **0.0670** | **+0.17** | **14** | **+1.50** | **−0.097, 0.146** | **+0.116** |
| | FAIRTA, Blumenthal (primary) | 0.84/0.84 | 0.1231 | +0.67 | 14 | +5.46 | −0.097, 0.146 | +0.525 |
| LOW 0.834, 0.683 | EM1, Blumenthal | 0.51/0.52 | 0.0658 | +0.55 | 14 | +1.50 | same | +0.173 |
| HIGH 1.864, 1.723 | EM1, Blumenthal | 0.30/0.30 | 0.0726 | −0.03 | 14 | +1.50 | same | +0.061 |

Υ by V_flat, EM1 + Blumenthal: MEDIAN 0.49, 0.53, 0.46, 0.30, 0.36, 0.47; LOW 0.85, 0.89, 0.63, 0.30, 0.36, 0.47; HIGH 0.30, 0.30, 0.31, 0.30, 0.36, 0.47. G-IN-Mall −2.05 throughout. Clusters don't depend on these inputs.

## Frozen label
Primary: **SIGN FLIP YES, AMPLITUDE FAILS** at all three inputs. EM1 line at MEDIAN: **no**. **[NOISE-LIMITED]** because the EM1 line differs at LOW; a band run reaching it isn't a pass, and at LOW the tilt, LITTLE THINGS, one key and X-COP all fail. At HIGH the tilt and LITTLE THINGS clear but Υ pins at the grid floor, 0.30.

My expectation held for MEDIAN (I wrote 0.36–0.38; A reads 0.35) and for LOW.

## How this reads
- **The 150–250 km/s bins don't move:** 0.30 and 0.36 at every input. Low-mass η only moves the low bins, so no low-mass η closes this. Those bins' floor is what UR1's row is really stuck on.
- **No input clears Υ and tilt together:** LOW lifts dwarfs away from spirals, HIGH brings them together at the floor.
- FAIRTA stays dead on every input.

## Checks
K1 EM1 off against NR2's same-named run 0, at all three. K2 7.2e-15. K4 0. K5 η(10¹²) 21.531. MUTATE R_nat × 2: Υ 0.84 → 0.52, bites. KiDS, Local Group and MW not run.

κ = ½ FITTED. Not theory closed.
