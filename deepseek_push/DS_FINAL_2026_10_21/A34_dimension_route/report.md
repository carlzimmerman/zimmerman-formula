# A34 — THE DIMENSION / CODIMENSION ROUTE TO κ: a definition, an off-by-one, and a look-elsewhere artifact

Lane A34. `a34_checks.py` — 13 checks, **13/13 PASS**, exit 0, under 3 s. Deterministic, no network,
stdlib + sympy only. `a34.out` is the captured stdout; `a34_results.json` holds every number
quoted below (each value here is the corresponding entry, rounded to the digits shown).
Constants: BRIEF §4 only, plus the IAU nominal solar mass (declared). Measured κ = 0.417 ± 0.095
(CFG493 via A15). The question: is κ = 2/D (n = D−2, κ = 1/n) a derivation, or a coincidence?

## Claim

**It is numerology, and it fails at both links of the chain.** (i) **κ = 1/n is a definition.**
The framework defines n := 1/κ through `a0 = c√(Gρ_Λ)/n` and `Z = n√(8π/3)`; the identity
`a0 = cH_Λ/Z` and `κ_def = 1/n` both hold with residual **exactly 0 for symbolic n** (K5). No
derivation can live there. (ii) **n = D−2 is not supplied by the codimension argument.** The field
of a source with two transverse spatial directions *is* exactly 1/r, with coefficient 2G_Dλ in the
4π convention (4G_Dλ in 8π) — the exponent is right. But in D = 4 that source is a **string**
(p = 1), not a point: a point has transverse dimension m = 3 and falls as 1/r², and a "(D−2)-brane"
has m = 1 and gives a **constant** field (K2, K13). The task's premise "the codimension of a point
in D = 4 is 2" is false in every standard convention. The coefficient is a free parameter:
matching deep MOND requires λ = √(a0GM)/(2G) ∝ √M — not the baryonic mass, but a new dimensionful
source parameter per galaxy — and the flux topologies differ (MOND's grows ∝ r, the codim-2 flux is
constant), so no constant λ matches at more than one radius (K3, K4). The exponent the argument does
deliver is n_slope = m − 1 = **D−3**, which is 1 for a string and **D-independent**; the quantity
κ = 1/n uses is n_vac = 2, and the two are different symbols for different things (§5). So the
codimension route cannot produce any κ(D) at all.
(iii) **The D-formulas are not unique.** κ = 2/D and κ = 1/(D−2) agree only at D = 4, predicting
κ(5) = 0.4 vs 1/3; ten simple formulas give 2 at D = 4 and κ(5) spread over [0.167, 0.625] (K6, K12).
(iv) **The framework's own D-generalisation has no equation for κ**: the master identity
R = Λc⁴/(8πa0²) = 1/κ² is D-independent, with G_D cancelling identically and residual 0 (K7).
A D = 5 world predicts κ = 1/3 or 0.4 — both inside 1σ of the measured 0.417 — and declining
rotation curves v ∝ r^{−1/4}; only the slope decides, and it decides **D**, not κ (K8, K9).
(v) **Look-elsewhere**: a plain 90-formula pool contains 11 formulas equal to 4 at D = 4 and
**8 equal to 4 at D = 5**, so A19's "9 at D=4, 0 at D=5" is a selection artifact, not a D=4
discriminator (K11).

## Derivation

Symbols: D spacetime dimensions; p = number of spatial worldvolume dimensions of the source;
**m := D − 1 − p** transverse spatial dimensions; λ = source mass per unit p-volume; G_D the
D-dimensional Newton constant; Ω_{m−1} = 2π^{m/2}/Γ(m/2) the area of S^{m−1}; Φ the potential,
g = |∇Φ|; ρ_Λ = Λc²/(8πG_D); κ := a0/(c√(G_Dρ_Λ)); n := 1/κ; Z := cH_Λ/a0; L := c²/a0;
R := ρ_Λc²/(a0²/G_D).

**1. The field of a codimension-2 source.** Static p-brane, ∇²Φ = 4πG_Dρ, ρ = λδ^m(x). Gauss on
S^{m−1}:

    g(r) = 4πG_D λ / (Ω_{m−1} r^{m−1}),      ∮ g·dA = 4πG_D λ  for every m.        (1)

    m = 1: g = const (domain wall);   m = 2: g = 2G_Dλ/r exactly;   m = 3: g = 2G_Dλ/r².   (2)

The exponent is −(m−1) = −(D−2−p). **g ∝ 1/r ⟺ m = 2 ⟺ p = D−3.** In D = 4, p = 1: a string.
(The same derivation with ∇²Φ = 8πG_Dρ gives 4G_Dλ/r; the factor is convention, the 1/r is not.)
A finite string of length L has 1/r for r ≪ L and 1/r² for r ≫ L.

**2. Premise audit (the off-by-one).** With m = D−1−p at D = 4: point (p=0) → m = 3 (1/r²);
string (p=1) → m = 2 (1/r); (D−2)-brane (p=2) → m = 1 (constant). The number "D−2" equals 2 at
D=4 and it *is* the transverse dimension of a **string**; it is not the transverse dimension of a
point (that is 3), and it is not the exponent of the field (that is 1). The codimension of a point
in D=4 is 3, not 2 (K13).

**3. Coefficient matching.** The framework's deep limit for a point mass is g = √(a0GM)/r. Setting
this equal to (2):

    λ = √(a0 G M)/(2G)  ∝ M^{1/2},  not M.                                        (3)

For an MW-like M = 1e11 M_⊙: λ = 2.6407e20 kg/m, r_M = √(GM/a0) = 12.20 kpc. A string carrying
the same M has λ = M/L, hence

    L = 2GM/√(a0GM) = 2 r_M = 24.41 kpc,                                          (4)

giving 1/r inside L and 1/r² outside — the **inverse** of MOND's ordering (1/r² for r ≪ r_M,
1/r for r ≫ r_M). The 1/r regime is near the source, not far from it.

A logical point that applies to any such match: the coefficient **1** in g = √(a0g_N) is not a
prediction, because a0 is *defined* as the acceleration at which g = g_N = a0; any 1/r field can be
written with coefficient 1 by choosing a0. The only content is the **value** of a0, i.e. κ, and the
codimension field does not supply it — it supplies a free tension instead.

**4. Flux.** ∮_{S²} g_MOND dA = 4π√(a0GM)·r, log slope **+1**; the codim-2 flux through its
transverse circle is **constant**, slope 0. Different topology. Equivalently, the phantom mass the
MOND field implies, M_ph = A r²/G = √(a0GM)·r/G, grows **∝ r** (log slope +1): the deep-MOND
field is sourced by an extended medium, not by a localized object of any codimension. The two
fields can agree at exactly one radius by construction; they are not the same law (K4).

**5. Three different "n"s.** The framework uses the same symbol for three quantities, and the
chain needs the coincidence of all three:

    n_vac   := 1/κ = 2          a0 = c√(Gρ_Λ)/n_vac ,  Z = n_vac√(8π/3)     (definition)
    n_gate  = 1                 the canonical Langmuir law has capacity a0 = A_max
    n_slope = 1                 g ∝ r^{−1} in the deep limit

n_vac = 2 and n_gate = n_slope = 1. FINAL_THEORY §2 labels the canonical law n = 1 (one gate per
site); BRIEF §1 labels the same canonical law n = 1/κ = 2. Whatever is intended, the symbol is not
one quantity. **The codimension argument, correctly counted, delivers the exponent
n_slope = m − 1 = D − 2 − p (= D−3 = 1 for a string at D=4), not D − 2.** "n = D−2" matches n_vac
(=m only if the source is a string), and matching it to n_slope is off by exactly one unit. So the
chain is: κ = 1/n_vac (definition) → n_vac = m (new premise) → m = 2 (the source is a string in
D=4: false for a point). Two premises, one of them false.

**6. The tautology.** ρ_Λ = Λc²/(8πG), so

    a0 = κ c√(Gρ_Λ) = κ c²√(Λ/8π) = c²√(Λ/8π)/n,    cH_Λ = c²√(Λ/3),             (5)

    a0/(cH_Λ) = √(3/8π)/n = 1/(n√(8π/3)) = 1/Z,   Z = n√(8π/3).                  (6)

Both residuals are exactly 0 for symbolic n (K5). So **κ = 1/n is the definition of n**, and
"κ = 1/(D−2)" is precisely the statement "n = D−2". Link (i) of the chain carries zero content;
everything must be carried by n = D−2, which §2–§4 do not supply.

**7. The framework in D dimensions.** From the metric (flat FRW, D = 3,4,5):

    G_00 = (D−1)(D−2)/2 · H²  = 1, 3, 6   →   H² = 16πG_Dρ/((D−1)(D−2));          (7)

    ρ_Λ = Λ/(8πG_D)  →  H_Λ² = 2Λ/((D−1)(D−2));   a0 = κc²√(Λ/8π) is D-free;      (8)

    Z_D = cH_Λ/a0 = 4√π/(κ√((D−1)(D−2))) = n√(16π/((D−1)(D−2)));                 (9)

    Z_3 = 10.02651,  Z_4 = 5.78881 = 2√(8π/3),  Z_5 = 4.09331.                    (10)

The master identity is D-free:

    R = Λc⁴/(8πa0²) = 1/κ²,  G_D and D cancel identically, residual 0.           (11)

The minimal generalisation of the law keeps the algebra and uses the D-dimensional Newtonian field:

    g_N = K_D M/r^{D−2},  K_D = 4πG_D/Ω_{D−2};   deep: g = √(a0K_DM) r^{−(D−2)/2}; (12)

    v² = g r ∝ r^{(4−D)/2}   →   flat ⟺ D = 4 (D=5: v ∝ r^{−1/4}; D=3: v ∝ r^{+1/4}). (13)

The vacuum integral does **not** generalise. The cell identity AΛ = Ω_{D−2}ℓ^{D−2}Λ has length
dimension L^{D−4}: dimensionless only at D = 4. The Gauss–Bonnet density is identically zero at
D = 3, a total derivative at D = 4 (`24ȧ²ä = d/dt(8ȧ³)`, residual 0), and dynamical at D = 5:
on de Sitter GB = 120H⁴ and its Euler–Lagrange derivative is 480H⁴a³ ≠ 0 (K10). The length-fixing
part of A19's route (candidate (i), the Euler cell) is a D = 4 object.

**8. The two candidate laws.** 2/D = 1/(D−2) ⟺ **D = 4** (the only intersection); κ(5) = 2/5 vs
1/3 (ratio 1.2); κ(3) = 2/3 vs 1. Ten simple formulas with f(4) = 2 (D/2, D−2, D(D−1)/6, √D,
log₂D, 2^D/8, (D−1)(D−2)/3, C(D,2)−4, D²/8, 8/D) give κ(5) ∈ {0.167, …, 0.625}, 9 distinct
values, spread 3.75× (K6, K12).

**9. What a D-world predicts.**

| D | κ=1/(D−2) | κ=2/D | tension vs 0.417±0.095 | Z_D | a0 (Λ fixed) | v(r) deep | GB route |
|---|---|---|---|---|---|---|---|
| 3 | 1.000 | 0.667 | 6.14σ , 2.63σ | 10.02651 | 9.36e-11 | r^{+1/4} | identically 0 |
| 4 | 0.500 | 0.500 | 0.87σ , 0.87σ | 5.78881 | 9.36e-11 | flat | total derivative |
| 5 | 0.333 | 0.400 | 0.88σ , 0.18σ | 4.09331 | 9.36e-11 | r^{−1/4} | dynamical |

Implied D from κ_meas: 4.398 (1/(D−2)) and 4.796 (2/D); 1σ ranges [3.953, 5.106] and
[3.906, 6.211]. **The κ measurement cannot exclude D = 5; under κ = 2/D it prefers it (0.18σ)
over D = 4 (0.87σ).** If instead ρ_Λ is held fixed with G_5 = G_4·(c/H₀) (V₁ = 1.3725e26 m), then
a0 scales by √V₁ = 1.1715e13 and becomes 1096.56 m/s² — so the D-generalisation is not defined
until one states whether Λ or ρ_Λ is held fixed. That choice is another free input (K7).

**10. Look-elsewhere.** A pool of 90 simple expressions built from the same ingredients as A19's
list (C(D,k)+m, k=1..6, m=−3..3; (D−a)(D−b)/c, a,b=0..3, c=1..3) has hits equal to 4 at
D = 3,4,5,6,7 of **4, 11, 8, 5, 2**; hit fraction at D=4 is 0.122. A19's "9" is **8 nontrivial
formulas plus the identity "D"**. And `(D−4)(D−5)+4` equals 4 at both D = 4 and D = 5, so
"0 at D=5" is a property of the chosen list, not of the space (K11).

## Status

**`NUMEROLOGY`.**

- **Link (i) is a definition** (exact, K5). κ = 1/n cannot be a derivation in either direction.
- **Link (ii) is false as stated and does not generalise.** The codimension-2 field is 1/r, but
  its source in D=4 is a string (m=2), not a point (m=3); the coefficient is a free tension, and
  the required tension scales as √M. The exponent is D-independent, so this route predicts no
  κ(D). A "(D−2)-brane" is a wall with a constant field. In the task's own terms, this is a
  **redefinition**: n is renamed "the codimension", and the codimension is then *chosen* to be 2
  by positing a string.
- **The D-formulas are degenerate.** 2/D and 1/(D−2) coincide only at D=4; ten formulas give
  n=2 at D=4 and κ(5) over a factor 3.75.
- **The framework supplies no κ(D).** R = 1/κ² is D-free; a0 is D-free at fixed Λ; the cell
  identity and the Euler charge exist only at D=4.
- **The D=5 prediction is unfalsifiable where it matters**: κ(5) ∈ {1/3, 0.4} is inside 1σ of the
  measurement, and 8 of the 10 simple-formula κ(5) values lie inside 2σ (K6). Only the
  rotation-curve slope (v ∝ r^{−1/4}) excludes D=5, and that is a measurement of D, not of κ.
- **Look-elsewhere**: 11 vs 8 formulas in a 90-formula pool single out D=4 vs D=5; the count is at
  chance level.

**The one CONDITIONAL reading, and why it fails.** If one adds the premise *"the gravitating
source is a 2D sheet (spatial codimension 2) and D = 4 is fixed independently"*, then the exponent
is 1 and κ = 1/2 follows — but only because n was defined as the codimension, and because D=4 is
an input. The framework's cold sector is a 4D collisionless medium (FINAL_THEORY §0, §5), not a
sheet; its only flattened structure is the A13 saddle pancake, which is not a gravitational source
and carries negative density. The premise is therefore not merely unproven, it is contradicted by
the framework. That is why the status is NUMEROLOGY and not CONDITIONAL.

**What DERIVED would have required**: an argument that fixes the transverse dimension of the
*actual* source (m = 3 for a galaxy in D=4) to 2 without positing a new object, and that fixes the
coefficient with no new dimensionful parameter. Neither exists in the class tested.

## Checks

| id | what it measures | value | verdict |
|---|---|---|---|
| K1 | codim-2 field: exponent, coefficient, flux | g = 2G_Dλ/r; flux 4πG_Dλ | PASS |
| K2 | general m: exponent −(m−1); point/wall bookkeeping | m=1 const, 2 1/r, 3 1/r²; point D=4 m=3 | PASS |
| K3 | coefficient matching; finite-string geometry | λ ∝ M^{0.5}; L = 2r_M = 24.41 kpc; regimes inverted | PASS |
| K4 | flux topology | MOND slope +1, codim-2 slope 0 | PASS |
| K5 | κ = 1/n tautology | both residuals exactly 0 | PASS |
| K6 | over-determination of "2" at D=4 | 10/10 hit; κ(5) 9 values in [0.167, 0.625] | PASS |
| K7 | D-Friedmann, a0, Z_D, master identity | G00/H² = 1,3,6; Z = 10.0265/5.7888/4.0933; R = 1/κ² | PASS |
| K8 | deep slope and v(r) in D dims | g ∝ r^{−(D−2)/2}; v² ∝ r^{(4−D)/2}; flat iff D=4 | PASS |
| K9 | κ tensions across D | D=5: 0.88σ / 0.18σ; D=4: 0.87σ | PASS |
| K10 | vacuum integral: dimension and Euler charge | [AΛ] = L^{D−4}; GB 0 / total deriv / EL=480H⁴a³ | PASS |
| K11 | look-elsewhere calibration | pool 90: 11 at D=4, 8 at D=5, 5 at D=6; A19's 9 = 8 + identity | PASS |
| K12 | 2/D vs 1/(D−2) | intersection {4}; κ(5) = 0.4 vs 0.333 | PASS |
| K13 | codimension audit | point 3, string 2, (D−2)-brane 1 | PASS |

## What this does not do

- It does not prove that no brane-world or extra-dimensional construction can produce MOND. DGP,
  cascading gravity and the dark-dimension literature are different frameworks with their own
  crossovers; this lane tests the **counting** argument only, and shows the count does not fix n.
- It does not test the framework's cold sector for a 2D substructure. It notes that the framework's
  stated ontology is a 4D collisionless medium, and that no codim-2 source is postulated anywhere
  in FINAL_THEORY.
- It does not re-derive A19's K11; it recounts it (8 nontrivial formulas + the identity "D") and
  calibrates it against a plain pool. The pool is one choice of "equal simplicity"; a different
  pool moves the number, which is itself the point — the denominator is undefined.
- It does not use the alt footing or any fitted constant. κ_meas is CFG493 as quoted by A15, and
  the canonical a0 enters only through BRIEF §4.
- It does not claim the D = 5 world is physically sensible: with ρ_Λ fixed and a Hubble-sized
  extra dimension, a0 = 1096.56 m/s², which is immediately excluded. That exclusion is about
  compactification, not about κ.

## Next

1. **The only measurement that would matter for this route** is a 1% κ (σ = 0.005): it separates
   κ = 1/2 from 1/3 at 33.3σ and would kill D = 5 under either D-formula. It still would not be a
   derivation — it would only remove the D = 5 degeneracy.
2. **Kill the ambiguity first.** A successor should state which quantity is held fixed across D
   (Λ or ρ_Λ) and what fixes D. Without that, "κ(D)" is not a function.
3. **The real target is unchanged from A19**: L = 2ℓ₁, i.e. a₀ = c²√(Λ/32π). The D-route does not
   touch it: R = 1/κ² is D-free, so no dimensional argument can supply the missing factor 2.
4. If the codimension idea is to be taken seriously, it must name the 2D object and show it carries
   the baryonic mass with λ = M/L, which §3 shows is not the case for a galaxy (λ ∝ √M).