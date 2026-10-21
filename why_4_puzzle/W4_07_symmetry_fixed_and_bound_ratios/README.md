# W4-07: ratios fixed by a symmetry or a consistency bound. RIGID BUT π-ODD

**Bottom line.**
- **Two symmetries really do fix a mass to the dark energy with no free coupling.**
  - The partially massless spin-2 point (the Higuchi bound saturated, m² = 2H²).
  - The conformally coupled scalar in de Sitter (m² = R/6 = 2H²).
  - Both give **κ² = 16π/3, κ = 4.09**: π × algebraic, never ½, and about ten times the measured 0.42.
  - That extends W4-05's dichotomy from "theories that fix their own vacuum" to "ratios fixed by a symmetry": rigidity
    through H always carries Einstein's π.
- **The consistency bounds don't select κ.**
  - Weak-gravity and species-scale saturation carry ħ and a free coupling.
  - The de Sitter and trans-Planckian conjectures are inequalities.
  - Flat-space positivity cannot see a vacuum constant at all.
- **The microscopic seesaw (Berezhiani–Khoury superfluid) cancels ħ exactly** but leaves κ² = α⁶ or 8πα⁶. The free phonon
  coupling α stays free, and the π is set only by which Planck mass you write.

None of these fixes the 4. **κ = ½ is FITTED.** Not theory closed.

## Results (`w4_07.out`; footing ρ_DE, de Sitter background)

| id | principle | κ² | class |
|---|---|---|---|
| B1 | partially massless spin-2, m² = (d−2)H² | 16π/(d−1), so **16π/3 at d = 4 (κ 4.093)** | MISS, π × algebraic |
| B2 | conformally coupled scalar, m² = ξ_c R | 4πd/(d−1), so **16π/3 at d = 4 (κ 4.093)** | MISS, π × algebraic (differs from B1 at d = 5: 5π vs 4π) |
| B3 | weak-gravity conjecture saturated + seesaw | c⁵g⁴q⁴/(2πG²ħρ) | HBAR (ħ⁻¹) / TRADE |
| B4 | dS swampland conjecture | — | BOUND (inequality on the quintessence slope) |
| B5 | trans-Planckian censorship | — | BOUND |
| B6 | species scale M_P/√N + seesaw | c⁵/(8πG²N²ħρ) | HBAR (ħ⁻¹) / TRADE |
| B7 | Berezhiani–Khoury superfluid, a₀ = α³Λ²/M_P with Λ⁴ = ε_DE | **α⁶** (non-reduced M_Pl) or **8πα⁶** (reduced M_P); ħ cancels | TRADE. κ = ½ needs α = 0.794 or 0.457. |
| B8 | flat-space amplitude positivity | — | CLOSURE: no vertex depends on a vacuum constant |

## What it adds to "why 4"

- **Rigidity is not enough.** L32 asked for a ratio fixed by structural data rather than a coupling. The partially massless
  and conformal points are exactly that, the first such cases on record, and they still land on π × algebraic. A symmetry that
  ties a mass to Λ ties it to H, and H brings 8π.
- **The seesaw is the one ħ-free bridge from microphysics.** It turns the 4 into a statement about a coupling (α⁶ = ¼, or
  1/(32π)) plus a Planck-mass convention. Nothing on record fixes α.

## Checks

- **I1:** no forbidden input.
- **K1:** B1 = B2 at d = 4 and they differ at d = 5, so the 16π/3 coincidence is four-dimensional.
- **K2:** B7's ħ power is 0 in both conventions.
- **K3:** the hand values are reproduced.
- **I3:** the SI items are dimensionless.
- **I7:** ħ appears only in B3 and B6.
- **I8:** B1 and B2 are π × algebraic, and neither is ¼.

**MUTATE** (`w4_07_MUTATE.out`, exit 1 by design). Each control is run as its own variant, because M1 and M3 together cancel
exactly for B1 (16π/(d−2) at d = 5 is 16π/3). Each bites with its frozen value:
- M1 (d = 5): B1 4π, B2 5π.
- M2 (Planck-mass swap): B7 8πα⁶ ↔ α⁶.
- M3 (Higuchi coefficient (d−1)): B1 8π.

## Disclosure: first run

The first normal run (`w4_07_firstrun_I8fail.out`, kept) scored 6/7. B2's conformal coupling (d−2)/(4(d−1)) was evaluated in
Python float arithmetic at d = 4, so κ² printed as 5.333…π and failed the algebraic test (I8). Exact rationals fixed it, giving
16π/3, the same value. Nothing else changed.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (a8684c224); B2's general-d formula was corrected before that commit |
| `w4_07.py` | sympy, one process, 0.5 s, 63 MB |
| `w4_07.out`, `w4_07_results.json` | normal run, 7/7 PASS, exit 0 |
| `w4_07_MUTATE.out`, `w4_07_results_MUTATE.json` | `W4_07_MUTATE=1`, three variants bite, exit 1 by design |
| `w4_07_firstrun_I8fail.out` | first normal run, 6/7 (float bug, disclosed above) |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios/w4_07.py > why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios/w4_07.out
    W4_07_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios/w4_07.py > why_4_puzzle/W4_07_symmetry_fixed_and_bound_ratios/w4_07_MUTATE.out

The principles are quoted from memory and labelled provisional; nothing was downloaded. Ran beside the live NC2x (1024³):
one core, 63 MB, under a second.
