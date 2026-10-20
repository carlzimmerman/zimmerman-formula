# W4-01: the gravity families the κ register never touched. NO FAMILY SELECTS κ

**Bottom line.** None of the seven families fixes the 4 in G ρ_DE = 4a₀²/c². No reading gives κ² = ¼:
- Every determinate value comes from the family's own 4D Friedmann relation, so it carries Einstein's 8π and is π-odd.
- Every other reading is a trade (a free constant), ħ-bearing, or an identity.

**κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078). Not theory closed.

Criteria were frozen first (5b09f2d51) under the CFG894 campaign rules, with no amendments. The normal run passes 13/13 checks.
In the MUTATE run, K4 fails on every reading the controls should move, and every bookkeeping check still passes (exit 1 by
design).

## Results (`w4_01.out`; κ on the family's own ρ_DE, the declared footing)

| family | readings | κ² | class |
|---|---|---|---|
| F1 DGP brane-induced gravity | self-accelerating: crossover c²/r_c; 5D product G₅ρ (action G₅); the same with the force-law G₅ᴺ = 4G₅/3π | 8π/3, 3/(2π), 8/(3π³) → κ 2.894, 0.691, 0.293 | **MENU**, all π-odd; 0.293 is a spurious in-window landing |
| | normal branch with a brane Λ | 1/(G r_c² ρ), 4G r_c² ρ | TRADE; a₀ ∝ ρ at fixed r_c breaks the LOCK |
| F2 Kaluza–Klein (circle, radius R) | R free | 4π²GR²ρ, 64GR²ρ/9, 1/(GR²ρ) | **TRADE** |
| | R tied to c/H_Λ | 3π/2, 8/(3π), 8π/3 → κ 2.171, 0.921, 2.894 | menu, all π-odd, all miss |
| | Casimir-stabilised R | ∝ ħ | HBAR |
| F3 dRGT / Hassan–Rosen | graviton Compton acceleration c²m on the self-accelerating branch | 8π/X, X free in the potential parameters | **TRADE**; π-odd at any algebraic X |
| F4 mimetic | no intrinsic acceleration; Λ an integration constant | — | **TRADE** |
| F5 Einstein–Cartan | spin–torsion energy, independent ρ_DE | (π/2)Għ²n²/ρ | **HBAR** |
| | spin energy as the dark energy | 1 by construction | IDENTITY (wrong sign; not scored) |
| F6 teleparallel f(T) = T + α(−T)ⁿ | scale of the correction | 16π(2n−1)^{1/(n−1)} (α cancels) | **TRADE** in n; π-odd at rational n |
| F7 Hořava–Lifshitz | Λ only | — | **TRADE** (detailed balance needs a free soft-breaking term) |

ρ_crit numbers (κ√Ω_Λ, report only) are in the .out. The footings are never pooled.

## The two structural points worth keeping

1. **Two Planck masses do cancel π, but the dark energy brings it back.**
   - DGP's crossover r_c = G₅/(2G) is π-free, because both actions carry the same 8π.
   - The 5D product G₅ρ is a π-free acceleration.
   - CFG891 says an exact ½ needs this kind of cross-sector cancellation. Here it fails at one step: on the self-accelerating
     branch the dark energy reaches the a₀ scale only through H² = 8πGρ/3, and the 8π returns (π-weights 1, −1, −3).
   - On the normal branch the dark energy is a free brane Λ, so the route is a TRADE.
2. **Kaluza–Klein with the 5D force-law constant gives a π-free tie, but with a free length.**
   - The circle's 2πR cancels the D = 5 Gauss factor, giving a₀ = (8/3) R G ρ_DE (κ² = 64GR²ρ/9).
   - R is unstabilised, so this is a TRADE.
   - The only π-free length built from ρ alone is R* = c/√(Gρ). That is the forbidden J = 1 premise (X7); it would give
     κ = 8/3, a miss.

So the minimal missing piece stated by CFG911 is unchanged: a bare-G portal a₀² = ξ G ε_DE with ξ fixed at ¼ by something named.

## Checks

- **K1–K3, the starting equations.**
  - DGP's vacuum root is H = 1/r_c.
  - The D = 5 force-law constant is 4G₅/(3π), with a flux of −4π² through S³.
  - f = T reproduces 6H² = 16πGρ, and f(T)'s de Sitter root is (6H²)^{1−n} = α(2n−1) at n = 2, 3/2 and 3.
- **K4.** Every frozen hand value is reproduced.
- **I1.** No forbidden input appears in the compute block.
- **I3.** κ² is dimensionless for every reading.
- **I4.** No route reads the law's κ.
- **I7.** ħ appears only in F2-R2 and F5-E1a, as declared.
- **I8.** Every declared π-odd value has odd weight. F3 and F6 carry π¹ structurally.

**MUTATE** (`w4_01_MUTATE.out`): M1 (8πG → 4πG) moves F1 to the frozen values 4π/3, 3/π and 16/(3π³). M2 (KK bulk 5 → 6) moves
F2-R1-B1 from 3π/2 to 6π³. F5-E1b stays at 1, as an identity should.

## Second predictions (stated, not scored)

- **DGP self-acceleration.** a₀ is flat while ρ_DE,eff drifts with H(z), which is not the framework's tracking law.
  Recalled, provisional: the branch has a ghost and expansion data disfavour it.
- **KK.** A radion drift moves G and a₀ together.
- **Massive gravity.** A graviton mass m ~ H₀.
- **f(T).** Its own w_eff(z).

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (5b09f2d51) |
| `w4_01.py` | sympy, one process, 0.45 s, 63 MB peak |
| `w4_01.out`, `w4_01_results.json` | normal run, 13/13 PASS, exit 0 |
| `w4_01_MUTATE.out`, `w4_01_results_MUTATE.json` | `W4_01_MUTATE=1`; K4 bites, exit 1 by design |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_01_untouched_gravity_families/w4_01.py > why_4_puzzle/W4_01_untouched_gravity_families/w4_01.out
    W4_01_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_01_untouched_gravity_families/w4_01.py > why_4_puzzle/W4_01_untouched_gravity_families/w4_01_MUTATE.out

Nothing was downloaded. Literature forms (DGP Friedmann equation, the Einstein–Cartan spin term, f(T) Friedmann, the
dRGT/HR structure) are quoted from memory and labelled provisional. The verdict rests on their structure (π-weight, free
constants, ħ). The printed values also depend on the recalled coefficients.
