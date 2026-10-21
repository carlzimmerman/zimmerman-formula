# W4-03: the eight κ proposals the register listed as never run. BACKLOG CLEARED, NO SELECTION

**Bottom line.** None of the eight fixes κ.
- **AS119** gives the only exact ½. It is the committed MU2 kernel's exponent n = 2 read back through premise A, so the ½ went
  in with the kernel.
- **The four-form items** (AS654, AS655, AS1923) move the 4 into another free number: C₀, λ or β²/Z.
- **AS672 and AS725** show the defining equations hold for every κ.
- **AS698** adds a prescription ambiguity to a class that is already excluded.
- **AS562** confirms the ħ wall.

Register row K547 had nine names. AS025 was in fact run on 2026-09-28 (results/AS025/run_20260928T000953: dimensional uniqueness
of the exponents (1, ½, ½), κ-blind), so only eight were outstanding.

**κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095). Not theory closed.

Criteria were frozen first (4708fd74c), with no amendments. The lane was frozen as "W4-02" and renumbered W4-03 after the run, because a parallel session had frozen a different W4-02 four minutes earlier (`../W4_02_independent_portal_audit/`). The erratum is appended to `FROZEN_CRITERIA.md`. The normal run passes 19/19 checks. In MUTATE, M1, M2, M3 and M5 make
their K checks fail, M4 moves the AS698 ratio, and the bookkeeping checks still pass (exit 1 by design).

## Results (`w4_03.out`)

| item | result | class |
|---|---|---|
| **AS119**, max-ent log moment | The Euler–Lagrange equation gives the Lomax family (λ−1)(1+u)^{−λ}, with E[ln(1+u)] = 1/(λ−1), so n = 1/c exactly. Truncated moments converge to 1/n: the exact truncated value plus the analytic tail equals 1/n to 0, and the quadrature converges at second order. κ = 1/n = c **only** if the kernel's scale is s = c√(Gρ), which is premise A. So c = ½ ⟺ the committed MU2 (n = 2) ⟺ κ = ½: one number in three costumes. Taken from data, c = 0.417 ± 0.095 gives n = 2.40 ± 0.55. | reparametrisation (S5); conditional |
| **AS562**, hidden ħ | Π_quant = ħ/(M_b v R) is dimensionless and equals 1.7 × 10⁻¹⁰⁰ for a 10¹⁰ M_⊙, 100 km/s, 10 kpc galaxy. The law a₀ = κc√(Gρ) has ħ⁰. An entropy count written "classically" with ℓ_P = 1 carries ħ⁻¹ once units are restored. | audit |
| **AS654**, additive C₀ in P(q) | κ²(q) = 2β²/(Z − 2C₀/q²). The flux amplitude no longer cancels, so the LOCK (a₀ ∝ √ε) holds only if C₀ = 0, and nothing names C₀ = 0. Exact consequence: a₀² = (2β²G/Z)(ε + C₀), an offset tracking law. | CONDITION |
| **AS655**, quartic flux term | κ²(q) = 2β²/(Z + 6λq²/Q₀²), so κ runs. The tracking slope is d ln a₀/d ln ε = (Z + 6x)/(2(Z + 12x)) < ½, with x = λq²/Q₀². | TRADE |
| **AS672**, rigidity as a functional equation | q P′ − P = a₀²/(κ²G) solves for every κ (checked at 0.3, 0.5 and 0.7, and for a general a₀(q)). Its homogeneous mode Cq is linear in the flux and carries zero energy. A linear a₀ reproduces k04's κ² = 2β²/(Z + 2bβ²). | CLOSURE (no rigidity) |
| **AS698**, two averages | A_t (cosmic time, weight √−g = a³) is the covariant 4-volume average; A_a (scale-factor measure) is not. For a = t^{2/3}, L = H²: A_a/A_t = 1.164, 1.284 and 1.321 at T = 10, 100 and 1000. For constant L the two agree, in both fixtures. | prescription ambiguity inside the global-average class T3/k02 already excludes |
| **AS725**, μ = K′(g)/2g | Integrable for any μ, and the constant K₀ stays free (k01's zero mode). The K₀-independent Newtonian offset K − g² diverges for both declared branches: Q as −a₀g, MU2 as −8a₀² ln g. So no finite vacuum functional comes free. | CLOSURE |
| **AS1923**, compact three-form | With q = 2πnf/Vol, κ² = 2β²/(Z + 2bβ²), independent of n, f and Vol. Quantisation fixes Λ, never β²/Z. Setting f = 1 changes nothing. This is the same as FL1/K144. | TRADE |

## What it adds

- **The register's backlog of unrun κ proposals is empty,** apart from p62, p63 and KAPPA_LOGIC, which belong to the
  "32pi squared puzzle" chat.
- **AS654 and AS655 give the four-form sector its own second predictions,** independent of κ:
  - an additive C₀ makes a₀² track ε + C₀;
  - a quartic correction makes a₀ track ε with a slope below ½.
  Both are visible only if w ≠ −1.
- **AS119 is a clean example of the S5 rule.** The max-ent "derivation" of the kernel is exact, and the ½ is its input.

## Disclosure: first run

The first normal run (`w4_03_firstrun_K1bfail.out`, kept unedited, so it still prints the old id W4-02) gave 18/19. K1b used an unfrozen 1e-5 threshold on the raw midpoint
residual and failed at u_max = 1000 with 512 cells (1.52e-5). That is a quadrature error, not a tail error. K1b now tests the
frozen wording: the exact truncated moment plus the analytic tail equals 1/n, and the quadrature converges at second order
(error ratio 4.00 per cell doubling at every u_max). No result changed.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (4708fd74c) |
| `w4_03.py` | sympy + stdlib, one process, 1.4 s, 71 MB peak |
| `w4_03.out`, `w4_03_results.json` | normal run, 19/19 PASS, exit 0 |
| `w4_03_MUTATE.out`, `w4_03_results_MUTATE.json` | `W4_03_MUTATE=1`; controls bite, exit 1 by design |
| `w4_03_firstrun_K1bfail.out` | first normal run, 18/19 (see the disclosure above) |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_03_unrun_as_proposals/w4_03.py > why_4_puzzle/W4_03_unrun_as_proposals/w4_03.out
    W4_03_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_03_unrun_as_proposals/w4_03.py > why_4_puzzle/W4_03_unrun_as_proposals/w4_03_MUTATE.out

Proposal files and pinned sources were read only. Their SHA-256 hashes match the pins: G228 cb82a65c, G230 a80516a5, G235
0483ca38, k04 15c0a7e1, k01 8df5a3ab, k02 c4fbd387. Nothing was written into `deepseek_push/`; AS1923's stale hermes reservation
was left as it is. Nothing was downloaded.
