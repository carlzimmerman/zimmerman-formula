# D5_kappa_four: why κ (the 4 in ρ_DE c²/(a₀²/G)). **SCOPED NO-GO**, plus one record error

κ = ½ stays FITTED. Z/4π = 0.460659 stays a POSTULATE (Milgrom's relation). Nothing here derives κ. Not theory closed.

- Criteria: `FROZEN_CRITERIA.md`, committed alone first (91ec2c9d07).
- Run: `OMP_NUM_THREADS=1 nice -n 10 python3 d5_kappa_four.py` takes under 1 s, about 60 MB, exit 0, **8/8**.
  `D5_MUTATE=1` (Friedmann 8π/3 → 1) exits 1 at **6/8**. K2 and K3 flip, as frozen.
- Every number below is in `d5_kappa_four_results.json`.

## The exact statement
a₀ = κc√(Gρ_Λ) gives **ρ_Λc²/(a₀²/G) = 1/κ² ≡ R**. So κ = ½ ⇔ R = 4 ⇔ Gρ_Λ = 4a₀²/c² ⇔ Λ = 32πa₀²/c⁴ ⇔ a₀ = cH_Λ/Z.
Check K0 verifies this chain symbolically.

## Angle T: a no-go for the horizon-thermodynamic class
**The class H_D.** a₀ is any monomial in the de Sitter horizon quantities, each with its textbook coefficient:
r_H, A, V, T_GH, S_BH, the Misner–Sharp energy, u_Λ = ρ_Λc², E_Λ, the Komar energy and the surface gravity.
Any powers of c, G, ħ and k_B may be added. The result must be ħ-free and k_B-free. Exponents are in ℤ/D, with D = 1
(products only) or D = 2 (square roots allowed).

**Theorem (T1, checked on all 3,900 enumerated monomials to 1e-15).** Every member equals a₀ = q·π^m·cH_Λ, with q² rational
and m ∈ ℤ/D. Dimensional analysis forces G's power to zero once ħ and k_B drop out. Hence **κ² = (8/3)·q²·π^(2m+1)**.

- **T2, D = 1: ½ ∉ S₁.** κ² is a rational number times an odd power of π, which can never equal ¼ because π is
  transcendental. **Z/4π ∈ S₁**, and it is the simplest member: a single block, a₀ = c·k_B·T_GH/ħ = cH_Λ/2π.
  The class's most natural output is Milgrom's value, not ½.
- **T3, D = 2: ½ ∈ S₂, but only one way.** All 16 enumerated hits have m = −½ and q² = 3/32. Each takes the square root of
  a π-odd block, which is the law's own √(Gρ_Λ) (κ = 1). That is then multiplied by one of three rational halves:
  - the 2 in the Misner–Sharp/Schwarzschild relation (E_MS/r_H = c⁴/2G);
  - the Komar ratio E_Λ/E_Komar = ½ (from ρ + 3p = −2ρ);
  - √ of Bekenstein's ¼ (S/A).

  So ½ is reachable only as "κ = 1 times a half picked from a menu". That fails D1 (no insertion).
- **LEE (D2).** P_cover = **1.0000** for S₁ and S₂ under both data bands. It is also 1.0000 for the 11-value minimal
  subclass (at most two blocks, Σ|e| ≤ 2), whose in-band members are 0.2303, 0.3455 and 0.4607.
  The share of class values inside the band (p_elem) is:

  | class | CFG493 band [0.227, 0.607] | A81 band [0.165, 0.749] |
  |---|---|---|
  | S₁ | 10 of 48 (0.208) | 16 of 48 (0.333) |
  | S₂ | 47 of 228 (0.206) | 71 of 228 (0.311) |

  A landing in the band therefore carries no weight for this class, as the record already says (P_LEE(data) = 1).
  Within ±1% of ½ there is no other value in S₁ or S₂.
- **Second prediction (D3).** A member either reads H_Λ, in which case a₀ is constant for w = −1, exactly as the framework
  already predicts, or it reads H(z), giving a₀(2.5)/a₀(0) = 3.7687, the record's Z1 rival law. No member fixes a second
  number that depends on the coefficient. D3 fails for the whole class.
- **Footings, not pooled** (Planck ρ_Λ):

  | footing | κ | nearest S₁ | nearest S₂ |
  |---|---|---|---|
  | canonical | 0.50000 | 0.51824 (+0.016 dex) | ½ exactly, by the T3 menu |
  | alt | 0.60425 | 0.61421 (+0.007 dex) | 0.60021 (−0.003 dex) |

  The class sits that close to both footings, which is the LEE point again.

**Scoped statement.** No principle built only from H_Λ, G, c and horizon-thermodynamic geometric factors gives ½.
- Without square roots, ½ is impossible. The first thing such a principle reaches is Z/4π.
- With square roots, ½ appears only as √(Gρ_Λ) times a hand-picked rational half.
- In both cases the class lands in the data band with probability 1 and has no coefficient-dependent second prediction.

**What is new.** The core parity fact is the record's wall 2 (`why_4_puzzle/README.md`; W4-02, W4-21). The new parts are:
- the class stated with exact coefficients and enumerated;
- the full list of ways ½ arises (only √(Gρ_Λ) times one of three named halves: Misner–Sharp, Komar, √Bekenstein);
- P_cover = 1 even for the 11-value minimal subclass.

## Angle A: the record's "data select 4 among the natural caps" is wrong
`FINAL_THEORY.md` says: "the saturation cap admits only R ∈ {1, 2, 4} … 4 is the only natural value the data admit". It
takes A19's three caps. But A19's **own** natural grid (`a19_checks.py` K6: β ∈ {1, 2}, χ ∈ {1…4}) is
R ∈ {1, 2, 3, 4, 8, 12, 16}.
- Reproduced A19 K10: 6.14 / 3.05 / 0.87σ (K6).
- **CFG493 (κ 0.417 ± 0.095):** 5 of 7 grid values lie within 2σ: R = 3 (+1.69), 4 (+0.87), 8 (−0.67), 12 (−1.35) and
  16 (−1.76). **R = 8 (κ = 0.354) is closer to the data than R = 4.** A19's own repair value R = 4π sits at −1.42σ, and the
  plain caps R = 3…8 all lie inside 2σ.
- **A81 joint** (κ_DE 0.457 ± 0.146, A81's κ_P3 scaled by its own ½-equivalence factor): 6 of 7 lie within 2σ. R = 2 is
  only +1.71σ, so "the data exclude R = 2" holds only on the CFG493 band.
- The data do not select 4. A19 itself said so ("the data pick the quarter, but the data measure κ itself"). The upgrade to
  "the only natural value the data admit" happened downstream.

**Where the claim is repeated (read-only; not edited):**
- `deepseek_push/DS_FINAL_2026_10_21/FINAL_THEORY.md:152–155`
- `deepseek_push/DS_FINAL_2026_10_21/A31_referee/report.md:236` (C20)
- `deepseek_push/DS_FINAL_2026_10_21/A33_master_action/MASTER_ACTION.md:291`
- `deepseek_push/DS_FINAL_2026_10_21/A75_thermal_premise/report.md:160`

## What this does not show
- It says nothing about classes outside H_D, such as bare-G portals (CFG911's ξ), media, or quantised couplings. The door
  stays open there.
- It does not rank ½ against Z/4π; the data cannot (≤ 2.8% on a₀ is needed).
- The A81 conversion is A81's linear ½-equivalence factor. Its thermal-equivalence factor differs by 0.1%.
- The enumeration bound (≤ 3 blocks, |e| ≤ 2) is a declared grammar. T1 and T2 hold for every exponent; the counts and
  p_elem do not.

## Record checked
- `doors_push_2026_10_22/BRIEF.md`;
- DS_FINAL BRIEF §2: the closed κ doors;
- DSF-21 A19 (code and report), A72 VERDICT and the A75 claim line;
- `why_4_puzzle/README.md` (W4-01…W4-23);
- `argon_push/AG6A_vacuum_capacity_factor/README.md`;
- CFG894 register and LEE output (737 rows; K170 and K458 Komar rows);
- CFG493 output;
- A81 results JSON;
- the κ memory notes.

No register row was added: this lane writes only inside its own folder.
