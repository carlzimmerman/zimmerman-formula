# W4-05: theories that fix their own vacuum. DICHOTOMY HOLDS

**Bottom line.** A theory can tie its dark energy to its own scale with no free constant only by fixing its own vacuum. Every
such theory in the census gives κ² = 8π × (an algebraic number). That is transcendental, so it is never ¼, and its natural size
is √(8π) ≈ 5:
- **EiBI gravity** with no separate cosmological term: κ = 5.01.
- **f(R) = R − μ⁴/R**: κ = 7.62.
- **DGP** (from W4-01): κ = 2.89.

The measured κ_Λ = 0.417 ± 0.095 sits about ten times below that natural size. Every family that does not fix its own vacuum
(Brans–Dicke, Deser–Woodard nonlocal MOND, running vacuum, TeVeS, EiBI with a free λ) leaves either Λ or a₀ free: a TRADE.
Maggiore's nonlocal RR model fixes ρ_DE only through the whole expansion history and does not track. So the census splits
cleanly. **Self-determined means π-odd and too large; π-free means free.** Neither half selects the 4.

**κ = ½ is FITTED.** Not theory closed.

## Results (`w4_05.out`; footing ρ_DE; ρ_crit = κ√Ω_Λ, report only)

| family | vacuum | reading | κ² | κ | class |
|---|---|---|---|---|---|
| V1a EiBI, λ = 0, κ_E < 0 | Λ_eff = 1/ℓ² (fixed by the action) | a = c²/ℓ | 8π | 5.013 | MISS (π × algebraic) |
| V1b EiBI, λ free | Λ_eff = (λ−1)/κ_E | a = c²/ℓ | 8π/(Λℓ²) | — | TRADE |
| V2 f(R) = R − μ⁴/R (metric or Palatini) | R = √3 μ² (vacuum trace equation) | a = μc² | 32π/√3 | 7.619 | MISS (π × algebraic) |
| V3 Brans–Dicke / scalar–tensor | Λ free | none intrinsic | 8πa²/Λ | — | TRADE |
| V4 Maggiore RR nonlocal | ρ_DE from m through the expansion history | a = mc | needs the measured matter history upstream (forbidden); ρ_DE,RR(z) drifts while m is constant | — | CONDITION |
| V5 Deser–Woodard nonlocal MOND | Λ free | a₀ a parameter | 8πa²/Λ | — | TRADE |
| V6 running vacuum | ρ₀ + 3νH²/8πG | a = cH | 8πH²/(8πGρ₀ + 3νH²) | — | TRADE |
| V7 TeVeS | Λ free | a₀ = √(3k)c²/(4πℓ) | 3k/(2πΛℓ²) | — | TRADE |

Re-tabulated from W4-01, not recomputed: DGP crossover 8π/3 (κ 2.894); dRGT 8π/X and f(T) 16π(2n−1)^{1/(n−1)}, both π¹ ×
algebraic at algebraic parameters.

## Why this matters for "why 4"

- **The clean form of the obstruction.** If a theory's vacuum curvature and its a₀ scale are both algebraic multiples of one
  length, κ² = 8π × algebraic, by Lindemann never ¼. This is W4-02's coefficient-domain theorem made concrete on seven more
  families.
- **A size statement as well as a parity one.** Self-determined vacua put a₀ near cH, with Z = cH_Λ/a₀ about 1–3. The data
  put Z near 6. So the 4 is also the statement that a₀ sits several times below the natural curvature acceleration. Any
  future route has to explain that factor, not just a π.

## Checks

- **K1.** √det(1 + κ_E M) = 1 + κ_E tr M/2 + O(κ_E²), so EiBI reduces to Einstein + Λ with Λ = (λ−1)/κ_E; λ = 1 gives 0.
- **K2.** f(R): R f′ − 2f = 0 gives R = √3μ², and the control f = R − 2Λ₀ gives R = 4Λ₀.
- **K3.** The hand values 8π and 32π/√3 are reproduced.
- **I1.** No forbidden input.
- **I3.** κ² is dimensionless under rescaling.
- **I4.** No κ symbol is read.
- **I8.** κ²/π is algebraic and κ² ≠ ¼ for both self-determined readings.
- **K4.** The dichotomy holds.

**MUTATE** (`w4_05_MUTATE.out`; exit 1 by design). Each control is evaluated separately and each makes K3 fail with its
frozen value:
- M1 (8πG → 4πG): EiBI 4π, f(R) 16π/√3.
- M2 (μ⁴/R → μ⁶/R²): f(R) 16·2^{1/3}π.
- M3 (EiBI λ = ½): 16π.

## Disclosures (implementation, before the MUTATE run; no value changed)

1. **M1 and M3 are run as separate variants.** Applied together they cancel exactly for EiBI (8π → 4π → 8π), and the frozen
   text requires each to make K3 fail.
2. **I3 and I4 were literal True in the first normal run (8/8).** They were replaced by a real rescaling test and a check that
   no κ symbol appears in any κ². The normal run was redone with the same 8/8 and the same values. The first output was
   overwritten, not kept.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (af2a69b13) |
| `w4_05.py` | sympy, one process, 0.45 s, 62 MB peak |
| `w4_05.out`, `w4_05_results.json` | normal run, 8/8 PASS, exit 0 |
| `w4_05_MUTATE.out`, `w4_05_results_MUTATE.json` | `W4_05_MUTATE=1`; the three controls bite, exit 1 by design |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_05_self_determined_vacua/w4_05.py > why_4_puzzle/W4_05_self_determined_vacua/w4_05.out
    W4_05_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_05_self_determined_vacua/w4_05.py > why_4_puzzle/W4_05_self_determined_vacua/w4_05_MUTATE.out

Family actions are quoted from memory and labelled provisional; nothing was downloaded. The parallel W4-04 lane (microscopic
SUSY, D3-brane DBI, heat-kernel induction) is not repeated here.
