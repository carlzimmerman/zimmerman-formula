# W4-09: do the dark-energy models themselves fix the 4? NO MODEL FIXES THE 4

(Frozen as W4-08 at 89d2a43c5. Renumbered W4-09 before any script, because a parallel session's W4-08 was frozen ten minutes
earlier; the erratum is appended to `FROZEN_CRITERIA.md`.)

**Bottom line.** This lane comes at the 4 from the dark-energy side. Every model gives κ² = (number) × (its own free
amplitude):

| id | model | κ² | class |
|---|---|---|---|
| E1 | holographic dark energy (Li), L = future horizon, a = c²/L | 8π/(3c_H²) | TRADE (c_H) |
| E2 | agegraphic, T = cosmic age, a = c/T | 8π/(3n²) | TRADE (n) |
| E3 | generalized Chaplygin | a²/(G A^{1/(1+α)}) | TRADE |
| E4 | Cardassian | a²/(GB) | TRADE |
| E5 | exponential scaling attractor, a = cH | 8πλ²/(9(1+w_b)) | TRADE (λ) |
| E6 | LQC bounce density | — (3.5×10¹²² × a dark-energy density) | HBAR: a Planck-scale density |
| E7 | causal-set everpresent Λ, a = cH | 8π/α_s, ħ cancels | TRADE (α_s, a random O(1) amplitude) |
| E8 | Dirac large numbers | — | CLOSURE: G ∝ 1/t is excluded (recalled) and a₀ ~ cH is H-type |
| E9 | interacting dark energy | a²/(Gξ) | TRADE |

At the saturated horizon value (c_H = 1, n = 1) the holographic and agegraphic models both give **8π/3 (κ = 2.89)**. That is
the same H-type number as W4-01's DGP crossover and the CKN bound. So the dark-energy side shows the same structure as the
gravity side: either a free amplitude, or H-type π × algebraic of order √(8π).

**κ = ½ is FITTED.** Not theory closed.

## Checks

- **I1:** no forbidden input.
- **K1:** the saturated E1 and E2 equal 8π/3.
- **K2:** ħ cancels in the causal-set Λ.
- **K3:** the hand values are reproduced.
- **K4:** LQC's density is 10¹²² above the dark-energy scale. This uses a declared order-of-magnitude placeholder, not a κ input.
- **I3:** E7 is dimensionless in SI.

The normal run passes 6/6 (exit 0). MUTATE runs two separate variants, and both bite (exit 1 by design):
- M1, non-reduced Planck mass: E1, E2 and E5 lose their 8π.
- M2, causal-set exponent ½ → ⅓: ħ stops cancelling, with power ⅓.

The criteria also record why the reduced-Planck-length swap was rejected as a control: Sorkin's Λ ~ ℓ_P⁻²N^{−1/2} = V₄^{−1/2}
does not depend on ℓ_P's normalisation.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | 89d2a43c5, plus the rename erratum 8acbd3280 |
| `w4_09.py` | sympy, one process, about 1 s |
| `w4_09.out`, `w4_09_results.json` | normal run, 6/6 PASS |
| `w4_09_MUTATE.out`, `w4_09_results_MUTATE.json` | `W4_09_MUTATE=1`, exit 1 by design |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_09_dark_energy_models/w4_09.py > why_4_puzzle/W4_09_dark_energy_models/w4_09.out

The model relations are quoted from memory and labelled provisional; nothing was downloaded.
