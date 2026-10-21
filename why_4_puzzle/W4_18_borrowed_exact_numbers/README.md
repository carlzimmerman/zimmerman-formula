# W4-18: exact numbers borrowed from outside gravity

**Verdict: MENU ONLY.** No outside exact number fixes the 4. The one π-free ½ found in the record is a lattice-choice menu
of a dust lattice, not a derivation. **κ = ½ stays FITTED.** Not theory closed.

The owner asked for equations from the rest of physics that might bear on the 4. Most borrowings were already in the
register (see the criteria). This lane runs the ones that were not: nine exact results, each with one mapping declared
before the script existed (criteria 68d2adb12).

## Results

| item | exact result borrowed | κ by the declared mapping | class |
|---|---|---|---|
| B1 | Mathieu first tongue: a mode resonates at half the pump (δ = ¼, confirmed by Floquet at ε = 0.02: [0.240, 0.259]) | pump H_Λ → √(2π/3) = 1.447, π-odd, out of window | odd |
| B2 | Fisher–KPP pulled front v* = 2√(Dr) | the vacuum has no D. Secondary reading: front at c with r = H → 2cH, κ = Z = 5.789 | free |
| B3 | Hardy/BF ¼ (inverse-square double root); dS₄ complementary-series edge m = 3H/2 | deep-MOND perturbation exponents ±√(l(l+1)/2): no tunable inverse-square coupling, so no Hardy slot. Edge reading √(6π) = 4.342, π-odd | odd |
| B4 | Thomson/Eddington: σ_T's 8π/3 cancels the flux 4π (L_Edd = 3GMm_pc/(2r_e²)) | transfer ∝ ρ(1+w) = 0 at w = −1: a Lorentz-invariant vacuum pushes nothing | void (nk) |
| B5 | Newton–Hooke duality (a+3)(A+3) = 4 | deep MOND is the self-dual point, but the dual coupling k = 4h/s² carries a free time scale s, so it is exponent-only | nk |
| B6 | Landau χ₊/χ₋ = 2, GL 1/√2, critical damping γ = 2ω₀ | no order parameter shared by a₀ and ρ_Λ; the damping reading is B3's edge | nk |
| B7 | lattices of touching horizons (32π chat brief X5, light part) | P-cube (sc) **½ exactly**, bcc 3^(1/4)/3 = 0.439, P-dense (fcc/hcp) 2^(3/4)/4 = **0.420**; all π-free, all in W_data | **menu** |
| B8 | Λ thresholds × MOND (brief X4, static part) | zero-force (2ρ_Λ) and OSCO (8ρ_Λ) exact for Newton; every law's threshold acceleration scales as M^(1/4) or M^(1/3); none is M-independent, and with no c none could fix κ | nk |
| B9 | Maxwellian √π (mean speed 2√2σ/√π; effusion ¼ n v̄) | the w = −1 source has no velocity distribution | void (nk) |

## What this says

- **B7 is the only route in the record that gives a π-free ½.**
  - The pull of one neighbour in a cubic lattice of masses whose horizons touch (spacing 2r_s) is exactly (c/2)√(Gρ). The
    ½ is the touching 2 times Schwarzschild's 2.
  - The lattice is the knob. Densest packing (Kepler: fcc/hcp) gives 0.420 and bcc gives 0.439. Both lie inside the data
    window, as ½ does (measured κ_Λ 0.500 canonical, 0.603 alt).
  - It is a lattice of pressureless masses (w = 0), not the vacuum (w = −1).
  - MU3 shows the ½ is definitional: "touching" at d = r_s gives 0.707.
- **B8 restates wall 1 concretely.** Static Newton or MOND plus Λ contains no c, so no threshold of it can relate a₀ to
  c√(Gρ_Λ); the computed thresholds are not even M-independent.
- **The π-odd items (B1–B3) land at 1.4–5.8, outside the window.** Each has the size √(8π) × rational, the same
  dichotomy W4-05 found.
- **Pointer, not run here:** the heavy half of brief X5 (exact-GR critical compactness of a periodic black-hole lattice)
  needs an elliptic solve and a horizon finder. It waits for NC2x, and even an exact ¼ there would be a dust lattice.

## Controls and checks

- **K1–K7 and I1 pass** (8/8).
- **First run:** I1 flagged printed text "pi^(-1/2)" in B9's output line, which is not a κ input. That run is kept as
  `w4_18_firstrun.out` and the line was reworded.
- **MUTATE (`W4_18_MUTATE=1`) bites on all five controls** (exit 1 by design):
  - MU1: w = −0.9 makes B4 non-void.
  - MU2: s → 2s changes B5's coupling.
  - MU3: d = r_s moves sc to 0.707.
  - MU4: Λ → −Λ removes every threshold.
  - MU5: pump 2H doubles B1.

## Files and run

`FROZEN_CRITERIA.md`, `w4_18.py`, `w4_18.out`, `w4_18_firstrun.out`, `w4_18_MUTATE.out`, `w4_18_results*.json`.

```
OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_18_borrowed_exact_numbers/w4_18.py > why_4_puzzle/W4_18_borrowed_exact_numbers/w4_18.out
W4_18_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_18_borrowed_exact_numbers/w4_18.py > why_4_puzzle/W4_18_borrowed_exact_numbers/w4_18_MUTATE.out
```
