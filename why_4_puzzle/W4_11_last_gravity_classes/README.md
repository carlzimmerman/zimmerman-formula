# W4-11: the last gravity classes with no register row. NO CLASS FIXES THE 4

**Bottom line.** The four gravity classes the κ register still lacked all leave κ free:

| id | class | result | class |
|---|---|---|---|
| Q1 | f(Q) = Q + αQⁿ (symmetric teleparallel) | Its flat-FRW background maps onto f(T) (recalled, provisional), so κ² = 16π(2n−1)^{1/(n−1)}, the same as W4-01's f(T) | TRADE in n (π¹ at rational n) |
| Q2 | f(R,T) = R + 2λT | In vacuum (T = 0) it is GR: R = 4Λ for any Λ | TRADE |
| Q3 | bumblebee vector, V(B² ∓ b²) | κ² = c²/(G b² ρ_vac); the vacuum constant is independent of b | TRADE |
| Q4 | Weyl conformal geometry (Ghilencea) | κ² = 8πc³q²/(Għξ²), with ħ⁻¹ from M_P | HBAR / TRADE (q, ξ) |

With W4-01, W4-05, W4-07 and W4-09, every standard modified-gravity and dark-energy class now has a register row. None fixes
the 4. **κ = ½ is FITTED.** Not theory closed.

## Checks

- **I1:** no forbidden input.
- **K1:** Q1 equals W4-01's f(T) value.
- **K2:** f(R,T)'s vacuum leaves Λ free.
- **K3:** the hand value is reproduced.

The normal run passes 4/4 (exit 0). MUTATE runs two separate variants, and both bite (exit 1 by design):
- M1, Friedmann normalisation 2·8πG → 2·4πG: Q1 halves.
- M2, a nonzero vacuum trace: R gains a λ term.

**Disclosure.** The first run (`w4_11_firstrun_K1K3fail.out`, kept) scored 2/4. sympy could not prove that
16π/(1/(2n−1))^{1/(n−1)} equals 16π(2n−1)^{1/(n−1)} without knowing 2n − 1 > 0. A numeric fallback at four values of
n > ½, the same device W4-01 uses, fixed it. No value changed.

## Files

`FROZEN_CRITERIA.md` (6d88f570f), `w4_11.py` (sympy, about 1 s), `w4_11.out` / `_results.json` (4/4),
`w4_11_MUTATE.out` / `_results_MUTATE.json` (exit 1 by design), `w4_11_firstrun_K1K3fail.out`.

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_11_last_gravity_classes/w4_11.py > why_4_puzzle/W4_11_last_gravity_classes/w4_11.out

The forms are quoted from memory and labelled provisional; only their structure (free couplings, π, ħ) enters the verdict.
Nothing was downloaded.
