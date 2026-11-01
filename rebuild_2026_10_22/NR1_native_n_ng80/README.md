# NR1_native_n_ng80: N PASSES AT NG 80 [ANCHOR-DEPENDENT]. The pass holds with η(10¹²) 21.53 if the low masses stay as measured at ng 64. If they fall by the same factor, it fails on the high side, Υ 0.88

Criteria: `FROZEN_CRITERIA.md` (38237437b0), `AMENDMENT_A1.md`, `AMENDMENT_A2.md`. `nr1.py`, `nr1_bins.py`, `nr1.out`, `nr1_results.json`, `nr1_bins.out`. κ = ½ FITTED; no a₀ in the cold sector; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework.

**Not blind.** Two earlier runs ended NOT DECIDED on check failures of mine, and I saw their Υ values. Both amendments record them. No pass line moved.

| Run | η(10¹²) | ρ₁₀, ρ₁₁ | Υ A / B | rms A / B | line |
|---|---|---|---|---|---|
| ng 64 (X80, NF1) | 25.94 | 1.128, 0.938 | 0.70 / 0.72 | 0.0682 / 0.0694 | pass |
| **PRIMARY** | **21.53** | **1.359, 1.131** | **0.72 / 0.75** | **0.0686 / 0.0697** | **PASS** |
| **ALT, ratios held** | 21.53 | 1.128, 0.938 | **0.88 / 0.89** | 0.0710 / 0.0721 | **FAIL, Υ high** |
| Band low | 14.55 | 2.011, 1.673 | 0.78 / 0.80 | 0.0737 / 0.0747 | pass, at the ceiling |
| Band high | 24.89 | 1.176, 0.978 | 0.70 / 0.72 | 0.0682 / 0.0694 | pass |

Groups Z +1.45 to +1.51. Failing keys in every run are the same as before: G-IN-all, G-MID-T3, G-IN-Mall, all OVER. The expected PRIMARY range on record, 0.70–0.78, held; its "band low may leave the line" didn't.

## How this reads
- **The anchor at 10¹² barely decides the line.** Even 14.55 passes while η(10¹⁰) and η(10¹¹) are held.
- **The low masses decide it.** SPARC's median galaxy sits below 10¹². ALT asks: what if ng 80 lowers η at 10¹⁰ and 10¹¹ by the same 0.83? Then Υ goes to 0.88 and the line fails.
- **Nobody has measured that.** No ng 80 run exists at 10¹⁰ or 10¹¹. The 0.83 itself has a 68 % band of 0.55–1.12, so it isn't established at 10¹² either.

## By V_flat, PRIMARY (reported, A background)
| V_flat | n | Υ | ΔV at Υ 0.50 | S rule | ET1 [CI] | |
|---|---|---|---|---|---|---|
| 20–60 | 13 | 1.20 | −4.3 | 53 | 69 [52, 85] | inside |
| 60–100 | 35 | 1.19 | −6.6 | 69 | 103 [81, 124] | outside |
| 100–150 | 23 | 0.91 | −12.5 | 86 | 143 [118, 200] | outside |
| 150–200 | 25 | 0.57 | −8.9 | 115 | 150 [98, 190] | inside |
| 200–250 | 18 | 0.62 | −21.6 | 140 | 215 [137, 272] | inside |
| 250–400 | 10 | 0.77 | −58.4 | 155 | 412 [182, 596] | outside |

The median passes, but Υ still runs from the 1.20 cap down to 0.57 with V_flat, as in ZN2's read. Those are mostly dwarfs at or above the 0.80 line, balanced by massive galaxies below it.

## Limits
One background pair, f★ 0.034, A4's η at 10¹³ and 10¹⁴. Band varies the anchor only. Core shape by hand, no contraction: LC1 and OP3 say contraction is strong, and it isn't in this rule.

## Checks
K1 formula at CE1's median returns 8.05034; grader's η against intended, every run, max |d| 7e-4. K2 A3 table against `NF1_N0`, |d| 0. K3 A4 table against `NF1_NATIVE`, |d| 0. MUTATE η × 0.5 moves Υ by 0.48, BITES.
