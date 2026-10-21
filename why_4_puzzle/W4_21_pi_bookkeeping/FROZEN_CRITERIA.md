# W4-20: π bookkeeping for the medium ratio R = εC₃²/C₂³ (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-20 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
**Screen lane:** it states a necessary condition and outputs no κ. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095 on
ρ_DE, κ_crit = 0.345 ± 0.078 on ρ_crit; neither value enters). Not theory closed.

## Question

W4-04's single-mediator dictionary turns ξ = ¼ into one target: R ≡ εC₃²/C₂³ = 128π/9 at n = 3. Can π content alone show
which media can never reach it? Are the record's explicit misses one failure or several? The explicit misses are W4-04's
thermal ratios 16/5 and 16/15, and the H-type κ² of W4-05, W4-07 and W4-19.

## Inherited from the record (paths; scope unchanged)

- **A1** (`W4_04_microscopic_normalization/PROOF.md` §A):
  - Static energy E(h) with E′(h) ~ 2C₂h at high h and ~ 3C₃h² at low h, h = |∇φ|.
  - Flux law Ω_n r^{n−1} E′(h) = qM.
  - G_n = q²/(2Ω_n C₂), a₀ = 2qC₂/(3C₃), ξ = a₀²/(G_n ε) = 8Ω_n C₂³/(9εC₃²).
  - Single mediator only. A tensor-plus-mediator theory must redo G.
- **A2** (same file, §C): free bosonic thermal coefficients
  - F = N[−π²θ⁴/90 + γθ²X/24 − γ^{3/2}θX^{3/2}/(12π) + …], with ε_rad = 3|F(0)|.
  - C₂ = Nγθ²/24 and C₃ = −Nγ^{3/2}θ/(12π).
- **A3**: the H-type values, transcribed exactly. These are record values, not recomputed:
  - W4-05 EiBI κ² = 8π; f(R) κ² = 32π/√3; DGP (via W4-01) κ² = 8π/3.
  - W4-07 B1/B2 κ² = 16π/3.
  - W4-19 L1 (Zhao) κ² = 8π.

## Added definitions and hypotheses (named)

- **D1. π-weight.** A number r·π^w, with r algebraic and nonzero and w an integer, has wt = w. wt is used only on that class.
  This is W4-02 Claim C's restricted grammar. No unrestricted parity theorem is invoked.
- **D2. Glued π.** A medium is *glued* if each of ε, C₂, C₃ equals r_i · Q · ∏_j (π^{g_j} s_j)^{p_ij}, where:
  - r_i is algebraic;
  - Q is a factor common to all three (species count, ħ, loop factor), of any weight;
  - each scale s_j carries the **same** π-weight g_j per unit power in all three coefficients.

  Examples: Matsubara πθ, or a Friedmann H used consistently. A route that attaches π to one scale differently in different
  coefficients is not glued. One example is a₀ = cH/2π, with H's 8π/3 in ε but 1/2π in a₀.
- **H1. One scale.** R is a pure number, with no free ratio of scales surviving. Otherwise the route is a TRADE before π is
  considered.

## Claims to check

- **L1.** Every glued one-scale medium has wt(R) = wt(Q)·(1 + 2 − 3) + Σ_j g_j·(p_εj + 2p_3j − 3p_2j) = 0. The second sum
  vanishes because R is dimensionless in each scale (H1). So R is algebraic.
- **L2.** With R algebraic, ξ = 8Ω_n/(9R) has wt(ξ) = wt(Ω_n) ≥ 1 for every n ≥ 2, since Ω_n = 2π^{n/2}/Γ(n/2). So ξ ≠ ¼
  in every dimension (S3). The theorem leaf is the transcendence of π.
- **L3.** A necessary condition for ξ = ¼ at n = 3, within D1: wt(ε) + 2·wt(C₃) − 3·wt(C₂) = 1. List every solution with all
  |w| ≤ 1. This is the solution set of one linear equation, not a scan. Hand expectation: (1, 0, 0), (−1, 1, 0), (0, −1, −1).
- **Correction, disclosed now.** The chat summary that led to this lane said "a Chern–Simons-type k/(4π) gives one free π".
  That holds only for where it sits:
  - on C₃ alone, wt(R) = −2;
  - on both stiffnesses, (0, −1, −1), wt(R) = +1.

  L3's table replaces that wording.

## Checks (all printed in `w4_20.out`; light single-core sympy plus mpmath)

- **K1.** sympy re-derives A1's G_n, a₀ and ξ from the two asymptotes and the flux law. At n = 3: R* = 128π/9 and
  wt(R*) = 1.
- **K2.** A2 reproduces R_th = 16/5 (with ε_rad) and 16/15 (with |F(0)|) exactly, both wt 0.
  - **K2b.** Each A2 coefficient factors as r·π⁻²·(πθ)^p, with a common Q = π⁻² and glue g = 1. sympy confirms.
  - **K2c.** The three A2 high-T coefficients are checked numerically against the bosonic thermal integral
    J(y) = ∫₀^∞ x² ln(1 − e^{−√(x²+y²)}) dx = −π⁴/45 + π²y²/12 − πy³/6 + O(y⁴ ln y). mpmath, 30 digits.
    - Pass: at y = 0.01, the residual after the three terms is below 5% of the cubic term.
    - Pass: the residual ratio falls from y = 0.02 to y = 0.01.
- **K3.** L1 symbolic: generic glued coefficients (symbols r_i, Q, s, g) give an R free of Q, s and π. A two-scale control
  (θ and an independent mass M) leaves R dependent on θ/M, which shows that H1 is needed.
- **K4.** L1 applied to A3. Each R = 32π/(9κ²) must be algebraic with wt 0. Hand values:
  - EiBI and Zhao: 4/9;
  - f(R): √3/9;
  - DGP: 4/3;
  - B1/B2: 2/3.

  This shows the H-type misses and the thermal miss are the same failure.
- **K5.** L2 table for n = 2–5: wt(Ω_n) = 1, 1, 2, 2. ξ ≠ ¼ for algebraic R in each.
- **K6.** L3's solution set with |w| ≤ 1 must equal the hand list.

## Identity checks

- **I1.** Grep the script for the §2 constants: 5.7888, 0.1727, 9.36e-11, 9.3603e-11, 1.13e-10, 1.1312e-10, 1.2e-10, 0.417,
  0.465, 0.551. Fail on any hit. 128π/9 appears only as W4-04's tested target, never as a premise.
- **I2.** Every R and ξ is symbolic.
- **I3.** R is invariant under (ε, C₂, C₃) → Z·(ε, C₂, C₃) and under φ → sφ (q, C₂, C₃ → q/s, C₂/s², C₃/s³).
- **I4.** Not applicable: no κ is read or output.
- **I5.** No Friedmann matching is performed. A3 values are transcribed.
- **I6.** Footing is ρ_DE only, with ε = ρ_DE c².
- **I7.** ħ enters only through the common Q and cancels. No Bekenstein–Hawking ¼.
- **I8.** The π-weight of every number is printed.

## Entry screen

- **S1.** c enters only through ε = ρ_DE c² (inherited from W4-04). This lane does not claim to clear S1 for any medium.
- **S2.** Counterfactual. The condition depends on the target. For example, κ² = 2/(3π) (κ 0.461) needs wt(R) = 2, not 1.
- **S4.** Not applicable: screen lane. Any medium that passes the screen still owes S2–S8 and a second prediction.
- **Option space / class:** no κ output. Register class `audit` (family AU).

## Mutation control (`W4_20_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when a control bites)

- **MU1. Un-glue one coefficient.** Replace A2's π²θ⁴/90 by πθ⁴/90 in ε. Expected: wt(R_th) moves 0 → −1, and the L1 check
  on the thermal medium FAILS.
- **MU2. Dimension n = 3 → 4.** Expected: wt(R*) moves 1 → 2 (Ω₄ = 2π²), and L3's right-hand side becomes 2. The thermal
  R stays wt 0, which is still a miss.
- Both are expected to bite. A control that does not move voids the lane.

## Verdict (frozen)

- **FILTER HOLDS** if K1–K6 and I1 pass. Then register one AU row: *SCREEN: glued one-scale media give algebraic R, so
  ξ ∈ ℚ̄·π^{wt Ω_n} and is never ¼ in any n; necessary condition wt ε + 2 wt C₃ − 3 wt C₂ = 1 at n = 3.*
- **FILTER FAILS** if any of K1–K6 fails. Report it; no screen row.

**Hand expectation:** FILTER HOLDS. A screen is not a selection: it fixes nothing, and passing it is not evidence for ½.

## Appendix (appended 2026-10-20 after the run, before any result commit): renumbered W4-20 → W4-21

Two sessions took W4-20 within 34 s of each other. This file was committed at 21:17:29 (a67f9ed9c); the lattice lane's
criteria followed at 21:18:03 (5d7db2b16) and that lane finished and was registered first (K744–K746). This lane therefore
moves to **W4-21** (folder `W4_21_pi_bookkeeping`, script `w4_21.py`, outputs `w4_21*.out/json`, mutation switch
`W4_21_MUTATE=1`). Every criterion above is unchanged; read "W4-20" and `w4_20` above as W4-21 and `w4_21`. The first run
(under the W4-20 names) gave FILTER HOLDS and CONTROLS BITE; it is rerun under the new names with no code change other than
the names.
