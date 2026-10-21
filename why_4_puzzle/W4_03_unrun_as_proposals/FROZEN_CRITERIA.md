# W4-02: execute the eight κ proposals the register lists as never run (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-02 script exists.** Append-only after this commit. Rules followed:
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md`. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ±
0.095, κ_crit = 0.345 ± 0.078). Not theory closed.

## Question

Register row K547 lists nine deepseek proposals as "NOT EXECUTED (proposals only)": AS025 AS119 AS562 AS654 AS655 AS672 AS698
AS725 AS1923.
- **AS025 was in fact executed.** Its claim is "completed" (results/AS025/run_20260928T000953: dimensional uniqueness of
  the exponents (1, ½, ½), κ-blind). It gets a correction row only.
- **The other eight have no run.** AS1923 has a stale hermes reservation from 2026-09-29 and no worker; the rest have no claim.

W4-02 executes the eight as written, here, and reads each against the campaign walls. The proposal files are astra/deepseek's
and are read only; nothing is written into `deepseek_push/`.

Overlap note: AS654, AS655, AS672 and AS1923 use k04's four-form P(q). p63 (the 32π chat; registered, unrun) tests
identifications and quantisations of Z/β², not P(q)'s form. AS1923 is the closest: it repeats FL1/K144's question
(quantisation and the split), not p63-C2's lattice reading (a₀ tied to one quantum). It is executed as written and flagged.

## Items, starting equations (from each proposal's "Mathematics and principal test") and hand expectations

Sources at their pinned SHA-256, verified 2026-10-20: G228 cb82a65c…, G230 a80516a5…, G235 0483ca38…, k04 15c0a7e1…,
k01 8df5a3ab…, k02 c4fbd387….

| item | statement | hand expectation (disclosed) | class |
|---|---|---|---|
| **AS119** | Max-entropy with {∫f = 1, E[ln(1+u)] = c} gives the Lomax family f = (λ−1)(1+u)^{−λ}, so n = λ−1 = 1/c. Then κ = 1/n holds **only** under the response identification that the kernel's scale is s = c√(Gρ). | κ = c exactly, conditional. The identification is premise A (a forbidden premise unless derived), so this is a **reparametrisation (S5)**: c carries the measured κ's uncertainty, giving n = 2.40 ± 0.55 from CFG493. Truncated moments on [0, u_max], u_max = 10, 100, 1000 with 128/256/512 cells, converge to 1/n with an analytic tail bound. | free |
| **AS562** | Π_quant = ħ/(M_b v R). | Dimensionless. At the fixture M_b = 10¹⁰ M_⊙, v = 100 km/s, R = 10 kpc it is ~10⁻¹⁰⁰. Any κ carrying ħ^p, p ≠ 0, is excluded. The law a₀ = κc√(Gρ) has p = 0. | audit |
| **AS654** | P(q) = Zq²/2 + C₀; ε = qP_q − P; a₀ = β√G q. | κ²(q) = 2β²/(Z − 2C₀/q²): the amplitude no longer cancels, so the LOCK holds only if C₀ = 0, and nothing names C₀ = 0. a₀² = (2β²G/Z)(ε + C₀). | free (CONDITION) |
| **AS655** | P(q) = Zq²/2 + λq⁴/Q₀². | κ²(q) = 2β²/(Z + 6λq²/Q₀²), a running κ. d ln a₀/d ln ε = (Z + 6x)/(2(Z + 12x)) with x = λq²/Q₀², so the LOCK slope ½ is broken at O(x). | free (TRADE) |
| **AS672** | a₀(q)² = κ²G[qP_q − P] for all q in an interval. | The ODE solves for every κ: P = q[C + ∫a₀²/(κ²G s²)ds], with a free homogeneous mode Cq (zero energy, linear in the flux). For a₀ = β√G q it reproduces k04's Z/2 + bβ² = β²/κ². No rigidity. | free (CLOSURE) |
| **AS698** | A_t = ∫a³L dt/∫a³dt versus A_a = ∫a³L da/∫a³da. | A_t is the covariant 4-volume average (√−g = a³ in cosmic time); A_a is not. Fixture a = t^{2/3} on [1, T], L = H²: the ratio A_a/A_t ≠ 1 and depends on T. Control: L constant gives equality. A prescription ambiguity inside the already-excluded global-average class (T3, k02). | free |
| **AS725** | μ(g) = K′(g)/(2g) after matching G_N (Newtonian K = g²). | K = ∫2gμ dg + K₀: integrable for any μ, and K₀ stays free (k01's zero mode). The K₀-independent Newtonian offset K − g² diverges for both declared branches: Q (g² = g_N² + a₀g_N) linearly, MU2 (μ = 1 − (1 + g/2a₀)^{−2}) logarithmically. | free (CLOSURE) |
| **AS1923** | ∮F = 2πnf on a closed four-cycle, so q = 2πnf/Vol, with P = Zq²/2 (+bβ²q²) and a₀ = β√G q. | κ² = 2β²/(Z + 2bβ²), independent of n, f and Vol. Quantisation fixes only the flux magnitude (Λ), never β²/Z. Duplicates FL1/K144. | free (TRADE) |

## Inputs and footing

Symbols only, plus pure numbers forced by each item. AS562's fixture uses SI constants (ħ, M_⊙, kpc), which carry no κ. AS119's
interval uses CFG493's κ_Λ = 0.417 ± 0.095 **only to propagate an uncertainty**, after the symbolic result, and labelled as such.
No a₀ value, Z or footing number appears upstream of any κ. Footing: ρ_DE wherever κ appears. Items are dimensionless and apply
to both footings identically; nothing is pooled.

## π / ħ declarations

- AS654, AS655, AS672, AS1923: κ² = 2β²/(…) with β, Z free, so π enters only through the couplings' normalisation (free).
- AS119: κ = c, π-free as a number, because the π lives in premise A's s = c√(Gρ).
- AS725, AS698: no κ number.
- ħ enters only AS562 (p = 1 for Π_quant, p = 0 for the law).

## Checks (printed in the .out)

- **I1:** the compute block contains no forbidden constant.
- **I2:** every κ² is symbolic, with its free symbols printed.
- **I3:** Π_quant is dimensionless.
- **I4:** the law's κ is never read by AS654/655/672/1923/725/698. AS119's κ = c follows the identification by construction,
  so it is flagged as a consistency relation.
- **I7:** ħ power printed (AS562).
- **K1–K8:** one per item, each comparing the symbolic result with the hand expectation above.
  - AS119 adds the max-ent Euler–Lagrange solution and the truncated-moment convergence.
  - AS725 adds the two divergence orders.
  - AS698 adds the dS / constant-L equality control.
- **Negative controls (from each proposal; each must be *rejected* by its check):**
  - AS119: declare κ exact while c is inferred with σ > 0.
  - AS562: call a ħ = 1 normalisation classical. Example: an entropy count A/(4ℓ_P²) restored has p = −1.
  - AS654: claim the amplitude cancellation removes all offsets.
  - AS655: keep the quadratic κ formula after adding q⁴.
  - AS672: treat satisfying the equation as deriving κ. It holds at κ = 0.3, 0.5 and 0.7 alike.
  - AS698: call A_t and A_a the same covariant average.
  - AS725: solve only K′ and claim vacuum closure.
  - AS1923: set f = 1 by convention and read ½ from it.

## Outcome classes (CFG894 §7) and lane verdict

- Per item: EXACT CANDIDATE / CONSISTENT / MISS / MENU / TRADE / CONDITION / CLOSURE / audit / VOID.
- **Lane verdict (frozen):**
  - **BACKLOG CLEARED, NO SELECTION:** every item TRADE/CONDITION/CLOSURE/audit.
  - **CANDIDATE:** any EXACT CANDIDATE (then an audit lane plus §8).
  - **DEFECT IN THE RECORD:** an item contradicts a committed record result. Report it; never fix another lane.
- Hand expectation: **BACKLOG CLEARED, NO SELECTION.**

## Mutation control (`W4_02_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when it bites)

- **M1:** AS119 constraint value c = ½ → ⅓. Expected: n 2 → 3, κ → ⅓.
- **M2:** AS654 C₀ → 0. Expected: q-dependence vanishes, κ² = 2β²/Z.
- **M3:** AS655 λ → 0. Expected: the quadratic formula is recovered.
- **M4:** AS698 a = t^{2/3} → t^{1/2}. Expected: the ratio moves.
- **M5:** AS1923 b = 0 versus symbolic b. Expected: κ² → 2β²/Z.
- The K checks against the normal-run hand values must FAIL for M1, M2, M3 and M5. The bookkeeping checks (I1, I3) must still
  pass.

## Second predictions (stated, not scored)

- **AS654:** a₀² ∝ ε + C₀, an offset tracking law. a₀(z) departs from √ρ_DE(z) if w ≠ −1.
- **AS655:** a tracking slope below ½.
- The others give no number.

## Files

`w4_02.py`, `w4_02.out`, `w4_02_results.json`, `w4_02_MUTATE.out`, `w4_02_results_MUTATE.json`, `README.md`. Register rows (one
per item, plus a K547 correction row for AS025), then `kappa_campaign_lee.py` rerun. Nothing downloaded; no file in
`deepseek_push/` is edited.

## Erratum (appended 2026-10-20, after the run; no criterion changed)

**Lane id W4-02 → W4-03.** A parallel session froze a different lane as W4-02 at 15:12:56
(`why_4_puzzle/W4_02_independent_portal_audit/`, criteria 72a3b470d), four minutes before this file (4708fd74c, 15:17:05). This
lane is renumbered **W4-03**: folder `why_4_puzzle/W4_03_unrun_as_proposals/`, files `w4_03.*`, env `W4_03_MUTATE`. Everything
above, including the hand expectations, controls and verdict rules, is unchanged; read "W4-02" in this file as W4-03.
