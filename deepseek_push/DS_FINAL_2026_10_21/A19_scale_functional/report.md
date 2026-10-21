# A19 — THE REMAINING HOLE FOR κ: four scale-setting functionals, exact outcomes

Lane A19. `a19_checks.py` — 17 checks, **17/17 PASS**, exit 0. Deterministic, no network,
stdlib + sympy only, under one second. `a19.out` is the captured stdout;
`a19_results.json` holds every number quoted below — each computed value here is the
corresponding entry of that file, rounded to the digits shown;
`MUTATE.md` records three mutations, each breaking exactly one check.
Constants used: BRIEF §4 only (c, G, Λ, a₀, and the rounded ρ_Λ = 5.831e-27 for the A15
cross-check), plus κ = 0.417 ± 0.095 (CFG493, via a15's report). No fitted constant is introduced.

## Claim

**No candidate in the tested class returns 4 without a free parameter.** All four reduce to the
same single dimensionless equation, ΛL² = 32π with L := c²/a₀, and each supplies at most one of
the two numbers that equation needs. Exactly:

- **(i) Euler balance — a definition, and not even a dynamical one.** The Gauss–Bonnet density is
  a total derivative in 4D (K4: the Euler–Lagrange derivative vanishes identically for arbitrary
  a(t); 24ȧ²ä = d/dt(8ȧ³)): a total derivative cannot supply a stationarity condition at all.
  The balance is a₀-blind (K5: ∂(AΛ)/∂a₀ = 0 while ∂R/∂a₀ = −Λc⁴/(4πa₀³) ≠ 0), so it
  fixes the *geometric* length ℓ_χ = √(8πχ/Λ) and says nothing about a₀. The coincidence with the
  record's 32π² is arithmetic: 32π² = π·8π·4 (K15), i.e. sphere × Einstein × (1/κ)².
- **(ii) Channel count — no honest count is 4.** Massless covector: 2 physical; massive: 3; the 4
  is the off-shell component count including the constrained mode (K7). The per-channel split is
  foliation-dependent (K8: time-component fraction 0 → 0.694 under a boost of rapidity 2) while
  the invariant count stays 2.
- **(iii) One quantum per cell — a tautology in a₀.** P_max·A = a₀²/G · 4π(c²/a₀)² = 4πc⁴/G for
  every a₀ (K9), ∂/∂a₀ = 0. The balance is also dimensionally inhomogeneous by an *area*, and its
  unique repair returns R = 4π (K9).
- **(iv) Saturation cap — three natural values, no principle.** R ∈ {1,2,4} ⇒ κ ∈ {1, 0.707107,
  0.5}; measured κ excludes the first two at 6.14σ and 3.05σ and accepts the third at 0.87σ
  (K10), but nothing in the class selects among them, and R = 4's only geometric content is (i)'s.

**Falsifiable beyond κ: none of the four.** (i) only relabels ℓ₁; its one new content, the discrete
family κ = 1/(2√χ), is unresolvable by present data. (ii) is scale-free and slicing-dependent.
(iii) is an identity in a₀, hence unfalsifiable. (iv) *is* κ (R = 1 at 6.14σ, R = 2 at 3.05σ).
The only genuinely predictive member, (v) Unruh–dS, is already excluded at 33.5×.

The two parameter-free entries are **the same functional in two dresses** — a₀ = c²/r_H, the
Unruh–de Sitter / horizon-radius statement — and both return **R = 3/(8π) = 0.119366**, off by
32π/3 = 33.510 (K12). Over the class as tested, *"returns exactly 4" and "has no free parameter"
are mutually exclusive* (K13). The exact ledger is

    κ = ℓ₁/L ,   ℓ₁ := √(8π/Λ) ,   L := c²/a₀ ,   1/κ = L/ℓ₁ = β√χ ,

so **1/κ is a length ratio**: 2 in cell units (χ = 1, β = 2) and Z = 2√(8π/3) = 5.788810 in
horizon units (K16). κ = ½ ⟺ the MOND length is twice the vacuum's χ = 1 cell radius.
**Status: `NO-GO(obstruction)`** — κ is a modulus, and the missing premise is one geometric
identification (L = 2ℓ₁), not a count.

## Derivation

Signature (−+++); c = 1 in the algebra, restored in every number. Symbols: Λ > 0;
ρ_DE := Λc²/(8πG) (mass density); u := ρ_DE c² = Λc⁴/(8πG) (energy density);
s_DE := c√(Gρ_DE); a₀ the law's scale; κ := a₀/s_DE; L := c²/a₀; r_H := √(3/Λ);
ℓ_χ := √(8πχ/Λ) (the Euler cell radius); β := L/ℓ_χ; R := u/(a₀²/G) = 1/κ².

**1. Master identity (K1, all residuals exactly 0).**

    (1)  R = u/(a₀²/G) = Λc⁴/(8πa₀²) = ΛL²/(8π) = Λℓ²/(2π) ,   ℓ := L/2 .

    (2)  R = 4  ⟺  ΛL² = 32π  ⟺  Λℓ² = 8π  ⟺  AΛ = 32π² (A = 4πℓ²)  ⟺  a₀² = Gu/4 .

Footing (K2): R = 3.99502, κ = 0.500311, 1/κ = 1.99876, L = 9.602085e26 m, r_H = 1.659765e26 m,
ℓ₁ = 4.804033e26 m, s_DE = 1.870835e-10 m/s², cH_Λ = 5.414953e-10 m/s², Z = 5.788810,
a₀(32π) = 9.354173e-11 (6.22e-4 from the footing). With a15's rounded ρ_Λ = 5.831e-27 the same
arithmetic gives κ = 0.500473 — the verified lane reproduced at its quoted precision. The alt footing
a₀ = 1.13e-10 gives R = 2.74103, κ = 0.60401. **R ≈ 4 is a property of the canonical footing, not
a measurement**: the footing was built as κ = ½.

**2. Candidate (i): the Euler-density balance.**

    (3)  ε := (1/32π²)(R²_abcd − 4R²_ab + R²) ,   ∫_M ε = χ(M) .
    (4)  maximally symmetric: R²_abcd = 24/ℓ⁴, R²_ab = 36/ℓ⁴, R² = 144/ℓ⁴ ⇒ ε = 24/ℓ⁴ (K3).
    (5)  ∫_{S⁴} ε = (24/ℓ⁴)(8π²ℓ⁴/3) = 64π² = 32π²·2 = 32π²χ(S⁴)  (exact).
         For B⁴, χ = 1 ⇒ charge 32π², and since the ball is flat the charge is entirely boundary.
    (6)  balance: AΛ = 32π²χ with A = 4πℓ_χ²  ⇒  Λℓ_χ² = 8πχ  ⇒  ℓ_χ = √(8πχ/Λ) .

What the balance *is*. It is a **definition** of ℓ_χ, and not a dynamical statement:

    (7)  δ/δa(t) ∫ 24ȧ²ä dt ≡ 0 ,   24ȧ²ä = d/dt(8ȧ³)      (K4, exact for arbitrary a(t))
    (8)  ∂(AΛ)/∂a₀ = 0 ,   ∂R/∂a₀ = −Λc⁴/(4πa₀³) ≠ 0        (K5, exact)

(7) is structural: the GB density has no bulk equation of motion, so "stationary on de Sitter"
cannot select anything through it — the balance can only be a constraint on the field space, i.e.
a definition of the cell. (8) is the sharper statement: the balance has *zero* sensitivity to the
cold sector, so it cannot fix a₀. What it *does* fix, with no free parameter, is ℓ_χ — that is
real content: it is where the Λ-scaling a₀ ∝ c²√Λ comes from. What it cannot fix is the
coefficient. With β := L/ℓ_χ,

    (9)  R = β²χ ,   κ = 1/(β√χ) ,   R = 4 ⟺ β√χ = 2                    (K6)

K6: eight exact (β,χ) pairs satisfy β√χ = 2; the natural grid β ∈ {1,2} (radius/diameter) ×
χ ∈ {1,2,3,4} (B⁴, S⁴, CP², S²×S²) realises **seven distinct κ** — 1, 0.707107, 0.577350, 0.5,
0.353553, 0.288675, 0.25 — and κ = ½ is realised **twice**: (β,χ) = (2,1) [diameter, 4-ball] and
(1,4) [radius, S²×S²]. The value 4 does not pin down the structure.

The arithmetic of the match, exactly:

    (10) AΛ = 8π²n²  (n := 1/κ)  and  32π² = π · 8π · 4                 (K15)

so the "32π²" carries no topology: it is π × 8π × n², and 8 × 4 = 32. Equating it to a
Gauss–Bonnet charge asserts an identity between two monomials that merely share a symbol.

Locality — a premise of the problem — fails on both readings. A *local* balance ε = F(T) would
force the cold sector's stress to be constant (ε is constant on dS); that stress falls as r⁻², a
factor 1.0e4 over 0.3–30 kpc (K17). The integral reading is a boundary charge, i.e. non-local.
Either way candidate (i) is outside the stated class.

**3. Candidate (ii): the zero-mode / channel count.**

    (11) covector, D = 4: 4 − 1 (first-class constraint) − 1 (gauge) = 2 physical (massless);
         4 − 1 = 3 (massive Proca, ghost-free); 4 = off-shell components = 3 + 1 constrained.
         General D: D−2 = 4 only at D = 6.                              (K7)
    (12) basis dependence: A = (0,a,0,0) with n = (1,0,0,0) has zero time component; after a
         boost of rapidity η along x the time-component fraction is
         sinh η/√(sinh²η + cosh²η) = 0.419 (η=0.5), 0.606 (η=1), 0.694 (η=2); the invariant
         physical count stays 2.                                        (K8)

The "ghost" does not supply a 4: for Proca the fourth component is removed by a constraint, not
canceled by a ghost; in a Stückelberg description the count is again 3. opus_48 found the same
basis dependence for dust (invariant engaged-response rank 1, not 2) — cited, per BRIEF §2, not
re-run. A count is moreover a pure integer independent of Λ: with amplitude ratio x free,
R = c·x is one equation in two unknowns (dof 1). A count can multiply a ratio; it cannot create
one.

**4. Candidate (iii): one quantum per cell.**

    (13) A = 4π(c²/a₀)² ,  P_max = a₀²/G  ⇒  P_max·A = 4πc⁴/G = 1.5209e45 N ,  ∂/∂a₀ = 0   (K9)

The balance holds identically for every a₀ — a tautology, not a constraint: because the cell area
is defined *with* a₀, the product is a₀-free. (14) Dimensionally [P_max·A] = force while
[u] = stress, so the gap is an **area** (L²), not zero; the unique repair with the one available
length, P_max·A = u·ℓ₀², gives P_max = u/4π, i.e. **R = 4π = 12.566** — one of the values a15
lists as excluded. So (iii) is not the same statement as (i): (i) fixes a length, (iii) fixes
nothing at all.

**5. Candidate (iv): the saturation cap.**

    (15) P_max = a₀²/G = u/R ,  R ∈ {1,2,4}  ⇒  κ = 1/√R = 1, 0.707107, 0.5
    (16) AΛ = 8π²R = 8π², 16π², 32π²
    (17) κ_meas = 0.417 ± 0.095: tensions 6.14σ, 3.05σ, 0.87σ                      (K10)

The three caps are "cold stress = vacuum", "= half" (equipartition) and "= a quarter". Nothing in
the class picks one; the data pick the quarter, but the data measure κ itself. By (16) the three
are AΛ = 8π², 16π², 32π², and only R = 4 lands on the Euler monomial — arithmetically, by (10).

**6. The parameter-free members.**

    (18) T_Unruh = ħa/(2πck_B) = T_dS = ħH/(2πk_B) ,  H = c√(Λ/3)  ⇒  a = c²/r_H   (ħ, k_B cancel)
    (19) κ_U = ℓ₁/r_H = √(8π/3) = 2.894405 ,  R_U = 3/(8π) = 0.119366 ,  4/R_U = 32π/3 = 33.510
    (20) κ_can = κ_U/Z ,  Z = 2√(8π/3) = 5.788810                                  (K12)

The de Sitter geodesic ball (radius r_H) is the same statement: the only parameter-free length is
r_H. These are the only members of the class with zero free parameters, and they miss by 33.5×.
Equivalently: **the canonical value is the unique dynamical answer divided by Z**, and Z is exactly
the Einstein 8π/3 bookkeeping — which is the BRIEF's warning made quantitative.

**7. The ledger.**

    (21) κ = ℓ₁/L  exactly (K16); hence 1/κ = L/ℓ₁ = β√χ: 2 in cell units, Z in horizon units.
    (22) κ = ½ ⟺ L = 2ℓ₁ ⟺ a₀ = c²√(Λ/32π) = 9.354173e-11 m/s².

## Status

**`NO-GO(obstruction)`**, with one `CONDITIONAL` sub-result.

**Theorem A19-T1 (non-identifiability of 4).** In the class 𝔉 of local functionals of
(g, T^φ) built from G and c with no further dimensionful parameter and no dimensionless constant:

- (a) every vacuum-sector member fixes at most one length, through Λℓ_F² = N_F with N_F a pure
  number (a topological charge or a group count);
- (b) the required ratio is R = β²N_F/(8π) with β = L/ℓ_F, so such a functional fixes R only if
  it fixes β — the comparison of a functional of g with a property of the cold sector's response,
  which is not in its argument list;
- (c) 𝔉 realises seven distinct exact κ on premises of equal simplicity (K6), and nine independent
  structural formulas equal 4 at D = 4 while none does at D = 5 (K11);
- (d) the parameter-free members give κ = 2.894, not ½.

Hence 4 is not identifiable in 𝔉: it requires β√χ = 2, which *is* the content of κ.
**The hypothesis that carries (b)**, stated so it can be attacked: that a stationary functional of
(g, T^φ) outputs a single pure number rather than a length built jointly from Λ and T^φ. That is
the one shape that would break the theorem, and it is where a successor should aim.

**Conditional sub-result — the unique identification that works.** Premises: **P1** the cell is a
4-ball (χ = 1, Euler charge 32π²); **P2** AΛ = Euler charge ⇒ ℓ₁ = √(8π/Λ); **P3** L = 2ℓ₁ (the
MOND length is the cell's diameter). Then R = 4 and κ = ½ exactly. P3 is load-bearing, and by (21)
P3 *is* 1/κ: the derivation returns its premise. That is why the status is NO-GO and not DERIVED.

Register wording this lane supports: *"κ = ½ is a length ratio, L/ℓ₁ = 2 with ℓ₁ = √(8π/Λ); it is
FITTED (CFG493). The 32π² spelling is π·8π·4 — sphere × Einstein × (1/κ)² — not a topological
charge. The Euler route fixes ℓ₁ and cannot fix L."*

Relation to GF1: GF1's R1 certified that every target is π-bookkeeping × n² and left the single
integer n = 2 open. This lane refines that: **n = β√χ, and the class fixes neither factor** —
χ is a topology and β a length convention, and (2,1) and (1,4) both give n = 2. The "one open
integer" is one open *product*.

## Checks

| id | what it measures | value | verdict |
|---|---|---|---|
| K1 | master identity and the four spellings of R = 4 | max residual 0.0e+00 | PASS |
| K2 | footing: R, κ, 1/κ, L, ℓ₁; A15 cross-check | R = 3.99502, κ = 0.500311 (0.500473 at A15's ρ_Λ) | PASS |
| K3 | GB bulk coefficient, Euler charges | 24/ℓ⁴; 64π² (χ=2); 32π² (χ=1) | PASS |
| K4 | GB density is a total derivative | EL = 0, 24ȧ²ä − d/dt(8ȧ³) = 0 | PASS |
| K5 | a₀-blindness of the Euler balance | ∂(AΛ)/∂a₀ = 0; ∂R/∂a₀ ≠ 0 | PASS |
| K6 | R = β²χ; exact-4 family and natural grid | 8/8 exact; 7 distinct κ; κ=½ twice | PASS |
| K7 | covector counts | 2 massless, 3 massive; 4 = off-shell | PASS |
| K8 | foliation dependence of the channel split | 0 → 0.694; invariant count 2 | PASS |
| K9 | one quantum per cell | P_max·A = 4πc⁴/G; ∂/∂a₀ = 0; repair R = 4π | PASS |
| K10 | cap family vs measured κ | 6.14σ / 3.05σ / 0.87σ | PASS |
| K11 | D = 4 degeneracy of the value 4 | 9 formulas = 4 at D=4, 0 at D=5 | PASS |
| K12 | Unruh–de Sitter | κ = 2.894405, R = 3/(8π), off by 32π/3 | PASS |
| K13 | free-parameter audit | 0 parameter-free candidates return 4 | PASS |
| K14 | size of the Euler cell | ℓ₁/r_H = 2.894405; 0.04124 cells per Hubble volume | PASS |
| K15 | 32π² = π·8π·4 | residuals 0 | PASS |
| K16 | κ = ℓ₁/L; 1/κ as a length ratio | 0; 2 (cells); Z (horizons) | PASS |
| K17 | local Euler balance vs the sector's profile | stress varies 1.0e4 over 1.5 dex | PASS |

## What this does not do

- It does not prove that no local functional of any kind can fix κ. It proves the four named
  candidates do not, and states (T1b) as a theorem hypothesis with its single escape route named.
- It does not re-audit opus_48's dust count; cited per BRIEF §2.
- It does not test data beyond the one measured κ; the σ-tensions in K10 are κ's own evidence.
- It does not claim the Euler cell is physical: ℓ₁/r_H = 2.894 > 1, so there are 0.041 cells in a
  Hubble volume (K14). "One quantum per cell" is not a description of the observable universe —
  the cell is super-horizon, which is a second, independent reason (iii) is not a picture.
- It does not derive 8π/3 or Einstein's 8π. Both are bookkeeping, as GF1's R1 already certified.
- The S⁴ charge is integrated exactly (K3); the B⁴ charge is quoted as 32π²χ with χ = 1
  (topology), not integrated term by term.

## Next

The single missing premise, in its sharpest form: **L = 2ℓ₁**, i.e. a₀ = c²√(Λ/32π), i.e.
a₀ = c²/(2√(8π/Λ)). Equivalently: a principle that ties the cold sector's response length to Λ
with coefficient exactly 2. Three things would settle it:

1. **Break T1b.** A functional whose stationarity outputs a length built jointly from Λ and T^φ
   rather than from Λ alone. That is the only shape not excluded here.
2. **Derive the product, not the factors.** β√χ = 2 has eight exact realisations; a derivation
   must single one out. A principle that fixes the cell topology (χ) independently of the length
   convention (β) would do it — the Euler route fixes neither.
3. **Precision.** κ = 0.417 ± 0.095 today. The χ-family predicts κ = 1/(2√χ), so a 1% κ
   measurement (σ_κ = 0.005) separates χ = 1 (0.5) from χ = 2 (0.3536) at 29.3σ (K10). The
   testable part of this lane is the *topology*, not the number: κ = ½ with a different χ is
   already excluded at that precision, and nothing in the class prefers χ = 1.
