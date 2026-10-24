# X25_floor_from_action — FROZEN CRITERIA (committed alone, before any script; estimate disclosed in §5)

**Question.** X24 (19d31a99d9) found that a velocity floor σ² = σ_iso² + c₀² reproduces three of four dwarf classes, with
c₀ = 4.59 [4.01, 5.14] / 4.05 [3.41, 4.66] km/s calibrated on LG field dwarfs. The MW ultra-faints want less (in-sample
H fit 3.64 / 3.46). Is c₀ the v3s held medium's own sound speed? ZT11 derived it from X3's PN Lagrangian:
c_s² = γ_L ρ₀ = 2π G ρ₀ L★², where ρ₀ = D·P is the held (phantom) density. If it is, does its density dependence also cure
the ultra-faint overshoot?

Standing rules: κ = ½ FITTED. Footings never pooled. No new constant: L★ is the action's own, with the record's lower
bounds 21.68 / 22.85 pc (floor), 24 pc, and 90 pc as the upper value X1 and ZT11 carry. Not "theory closed". Nothing here
may say the data favour the framework.

## 1. The derived sound speed per dwarf

- Per system: X1 `x1_per_system.csv` and X24's σ_iso and class definitions (X24's loader, copied).
- r₁₂ = (4/3) rh. g_N = G (M★/2)/r₁₂². g_iso = 3 σ_iso²/r₁₂ (E-W).
- ρ₀ (PRIMARY) = the mean enclosed phantom density inside r₁₂: ρ̄_ph = 3 (g_iso − g_N)/(4π G r₁₂).
- Reported: the local deep-MOND point-mass phantom density g_iso/(4πG r₁₂), which is ρ̄_ph/3 in the deep limit.
- c_s(L★) = √(2π G ρ₀) L★ at L★ ∈ {floor, 24, 90} pc, per footing.
- **L★,need** = the L★ at which the class median c_s equals the X24 field c₀.

## 2. Tests

- **D1 magnitude.** Per graded class (MW ultra-faint, bright M31, M31 others, MW classical): the median c_s at each L★
  against X24's field c₀ interval. D1 passes at an L★ if every graded class's median c_s lies in the interval.
- **D2 sign (verdict-bearing).** Does the action's own small-scale physics raise the prediction (a floor) or lower it
  (screening)? This is read from X1's full v3 predictions, which already contain that physics:
  ΔE_v3 = `Delta[AQUAL + EFE L*0]` − `Delta[v3 L*24]` per system. That is the change in log g_pred from switching on L★ at
  24 pc, on the same EFE baseline. A positive median means L★ raises g_pred (floor-like, the right sign). A negative
  median means it lowers g_pred (screening, the wrong sign). Also reported at L★ floor and 90 pc.
- **D3 ultra-faint direction.** The ratio of median c_s (MW ultra-faint) to median c_s (the other three classes pooled).
  The UFDs want a smaller c₀ (3.5 vs 4.6): ratio < 1 is the right direction. Reported at every L★.

## 3. Verdict (both footings must agree)

- **FLOOR DERIVED** — D2 has the right sign AND D1 passes at some L★ in [floor, 90] pc. D3 is reported as the
  ultra-faint qualifier.
- **WRONG SIGN** — D2 has the wrong sign. The held medium's pressure screens rather than adds, at any magnitude.
- **TOO SMALL** — D2 has the right sign but D1 fails at every L★ ≤ 90 pc. L★,need is reported.
- **UNDECIDED** — the footings disagree.

## 4. Checks (all must pass; `--mutate` must fail K0)

- **K0:** X24's field c₀ (from its JSON) and X19's H plain medians are reproduced (as X24's K0).
- **K1:** c_s formula vs ZT11 at R₀. With ZT11's ρ₀ = 0.059 / 0.068 M☉ pc⁻³ and L★ = 24 / 90 pc, it gives 0.96 / 3.6
  (canonical) and 1.0 / 3.8 (alt) km/s, to 3 % (ZT11's printed rounding).
- **K2:** deep-MOND identity: for a point mass in the deep limit, the local phantom density is exactly 1/3 of the mean
  enclosed (analytic, to 1e-12).
- **K3:** peak RSS < 1 GB.
- **MUTATE:** c_s² → 2 γ_L ρ₀ (ZT11's mutation); K1 must fail.

## 5. Disclosure

Before freezing, one back-of-envelope number was computed in this session: c_s ≈ 0.8 km/s (24 pc) and ≈ 3 km/s (90 pc)
for a typical ultra-faint, using ρ̄ = 3 g_iso/(4πG r₁₂) with σ_iso 1.6 km/s and r₁₂ 100 pc. No D2 or D3 number had been
computed. X1's v3 L★ rows are known in outline: X1 reports the v3 prediction leaves the UFDs at +1.56 dex.
