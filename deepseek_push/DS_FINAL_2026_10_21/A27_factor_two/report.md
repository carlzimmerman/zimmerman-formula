# A27 — THE FACTOR TWO: why is the MOND length twice the cell length?

Lane A27. `a27_checks.py` — 16 checks, **16/16 PASS**, exit 0, 0.4 s, deterministic, no network,
sympy only. `a27.out` is the captured stdout; `a27_results.json` holds every number quoted below
(each value here is that file's entry, rounded); `MUTATE.md` records three mutations, each breaking
exactly one check. Constants: BRIEF §4 (c, G, Λ, a₀ canonical and alt), plus the one external
measurement κ = 0.417 ± 0.095 (CFG493, via A19/a15). No fitted constant introduced.

## Claim

**The factor 2 has no geometric origin, and the question is mis-posed twice over.** Exactly:
(i) with β := L/ℓ₁, the master identity is *algebraically* R ≡ β² and κ ≡ 1/β, so "L = 2ℓ₁",
"κ = ½" and "R = 4" are not three equivalent statements but **one equation written three ways**
(K1) — deriving 2 is deriving κ, with no residue. (ii) κ = ½ is not a point but the curve
β√χ = 2, so both (β,χ) = (2,1) ("the length is the diameter of a 4-ball") and (1,4) ("the length
is the radius of S²×S²") give exactly κ = ½ and R = 4 (K2): "why the diameter rather than the
radius" presumes a uniqueness the ledger does not have. (iii) The cell ball has **six** natural
lengths; the diameter is one, and two of them — the bulk diameter β = 2 and the antipodal arc on
the boundary 2-sphere β = π — sit at 0.874σ and 1.039σ from the measured κ (K7, K8). Of the five
candidate mechanisms, the two that return exactly 2 do so by naming it (a Dirichlet wall, a
diameter); the three in which the 2 is a substantive premise — two legs, two cells, exponent 2 —
return 0.690988, 1.259921 and nothing, and the first two are excluded at 10.84σ and 3.97σ
(K4, K10–K12).

**Status: `NO-GO(obstruction)`.** The obstruction is not the integer; it is the *link* — every
argument in the class needs a premise "the law's length is this functional of the cell", and that
premise, written in the base symbols, *is* a₀ = c²√(Λ/32π).

## Derivation

Signature (−+++). Symbols: Λ > 0; a₀ the law's scale; c; L := c²/a₀ (MOND length);
ℓ_χ := √(8πχ/Λ) (Euler cell radius, charge χ; A19); ℓ₁ := ℓ_{χ=1} = √(8π/Λ);
β := L/ℓ₁; κ := a₀√(8π/Λ)/c²; R := Λc⁴/(8πa₀²) = u/(a₀²/G).

**1. The three statements are one equation (K1, exact).**

    (1)  β = (c²/a₀)·√(Λ/8π)  ⇒  β² = Λc⁴/(8πa₀²) = R          [identically]
    (2)  1/β = a₀√(8π/Λ)/c²   = κ                                [identically]
    (3)  β ↦ β² and β ↦ 1/β are injective on β > 0, hence
         {L = 2ℓ₁} = {β = 2} = {κ = ½} = {R = 4},  one set, one equation.

Sympy returns residual exactly 0 for both identities and the same a₀* from all three spellings:

    (4)  a₀* = c²√(Λ/32π) = √2√Λ c²/(8√π) = 9.354173e-11 m/s².

This is the whole content of "the factor 2". There is no independent statement "R = 4" to prove
separately, and no information is gained by renaming β. A derivation of 2 *is* a derivation of κ;
conversely a no-go for κ is a no-go for 2. The lane therefore cannot succeed where A19 failed
unless it supplies something A19's class did not contain — and it does not.

**2. The factor is a coordinate on a curve, not a number (K2, exact).** For general cell topology χ,

    (5)  κ = 1/(β√χ) ,   R = β²χ ,   so  κ = ½  ⇔  β√χ = 2 .
    (6)  (β,χ) = (2,1): κ = 1/2, R = 4.      (β,χ) = (1,4): κ = 1/2, R = 4.

Two different sentences — "the MOND length is the diameter of the 4-ball" and "the MOND length is
the radius of S²×S²" — produce the identical theory. So the target is not "why 2" but "why the
pair (2,1)"; the integer 2 is the χ = 1 slice of a curve. This is A19's K6 restated as a
statement about the *question*, and it is what makes "why the diameter?" ill-posed as asked.

**3. The link lemma (K15).** Every candidate has the same shape: a geometric theorem Σ about a
ball of radius ℓ₁, plus a link premise "L is the length g(ℓ₁)". Substituting the definitions
L = c²/a₀, ℓ₁ = √(8π/Λ) into the link "L = 2ℓ₁" gives

    (7)  c²/a₀ = 2√(8π/Λ)   ⇔   a₀ = c²√(Λ/32π),

which is (4) — the answer. The check is mechanical: eliminate the abbreviations from each link and
ask what the result says about a₀. For all four links that carry a factor (diameter, standing
wave, two-cells, radius) the eliminated premise is a nontrivial equation fixing a₀ — **4/4** (K15):
the value of β enters through the link and never through the geometry. For the slope candidate the
eliminated premise does not mention a₀ at all, i.e. it constrains nothing. Defining L := 2ℓ₁ makes
the conclusion identically 0 (K15) — the formal signature of "true by construction".

**4. Criterion D — derivation vs redefinition.** A premise set Σ concluding β = β₀ is a
*derivation* iff:

- **D1 (independence).** No premise of Σ, after L, κ and R are eliminated by their definitions,
  *is* the target equation a₀ = c²√(Λ/32π). A link naming a length that gives a different a₀
  passes D1 — it is a substantive, checkable claim rather than a restatement.
- **D2 (discriminating image).** Σ determines a map to β whose image over the admissible variants
  of Σ has ≥ 2 values. *A derivation must be able to have been wrong*: if no variation of the
  premises returns anything but 2, the 2 was inserted, not derived.
- **D3 (no dimensionless input).** After (Λ, χ) are fixed, Σ carries no free dimensionless number;
  every number in the output must be an integer that is itself derived (a count, a topological
  charge, an exponent fixed by a law).
- **D4 (surplus).** Σ entails at least one further checkable statement not used in producing β₀.

D2 is the operational form of "produces 2 by construction", and it is the criterion the five
candidates are scored against below. Its force: a geometric identity such as "the diameter of a
ball of radius ℓ₁ is 2ℓ₁" is *true*, has image {2}, and therefore derives nothing about a₀.

## The five candidates, each to a number

| # | mechanism | β returned | κ | R | vs κ_meas | D-failures | verdict |
|---|---|---|---|---|---|---|---|
| i | round trip, literal base r_H | 0.690988 | 1.447203 | 0.477465 | 10.84σ | D3 | **excluded** |
| i' | round trip, each side "contributes ℓ₁" | 2 | 0.5 | 4 | 0.87σ | D1,D2 | circular |
| ii | standing wave, Dirichlet ball | 2 | 0.5 | 4 | 0.87σ | D1,D2,D3 | circular |
| ii' | standing wave, Neumann ball | ∞ | — | — | — | D2 | no scale |
| iii | diameter, bulk (2ℓ₁) | 2 | 0.5 | 4 | 0.87σ | D1,D2,D3,D4 | renaming |
| iii' | diameter, boundary arc (πℓ₁) | 3.141593 | 0.318310 | 9.869604 | 1.04σ | D1,D2,D3 | not excluded |
| iv | deep-MOND slope n = 2 | — | — | — | — | D2,D3 | no output |
| v | two cells per correlation volume | 1.259921 | 0.793701 | 1.587401 | 3.97σ | D2,D3 | **excluded** |

**(i) Round trip.** The only horizon available is r_H = √(3/Λ) = 1.659765e26 m. Counting both legs
gives β = 2r_H/ℓ₁ = 4/Z = 0.690988, κ = Z/4 = 1.447203, R = 0.477465, a₀ = c²/(2r_H) =
2.707477e-10 m/s² — **10.84σ** from the measured κ; the one-leg version is β = 2/Z = 0.345494,
κ = Z/2 = 2.894405, which is A19's parameter-free Unruh–de Sitter value (already 33.5× in R).
Image {0.345494, 0.690988}: the argument can return either, so the 2 is a choice of leg count.
*Surplus:* the round trip predicts a₀ = c/(2t_H), a pure horizon statement with no 8π anywhere —
that is exactly why it misses by Z/2 = 2.894405. **Survives? No: the one non-circular reading is
falsified at 10.84σ.** The charitable reading ("each boundary contributes ℓ₁") has β = 2 by
construction (D1) and no surplus at all.

**(ii) Standing wave.** For a Dirichlet ball, j₀(kr) = sin(kr)/(kr) vanishes at kℓ₁ = π, so
λ_max = 2π/k = 2ℓ₁ **exactly** (K5; the s-mode is a half-wave in the radial direction, antinode at
the centre, node at the wall — the "two nodes per wavelength" phrasing is the 1-D interval, and it
gives the same number). β = 2, κ = ½, R = 4 — it hits the target. But the same ball with Neumann
conditions has the constant mode at k = 0, so λ_max = ∞ and there is no scale at all (K5). Image
{2, ∞}: the 2 is a property of the wall, not of the cell, and the horizon is not a wall.
*Surplus:* a cavity fundamental predicts the harmonic tower λ_n = 2ℓ₁/n, i.e. features at
a = n a₀. At the first three tower points the canonical isotherm sits 61.803%, 93.185% and
118.890% above the deep asymptote (K6) — an O(1) modulation, not a correction. But the canonical
law is a function of g_N/a₀ alone, so a tower is inconsistent with the law's *form* (A2); and if
the tower is already summed into the isotherm, the candidate predicts nothing beyond the number
(D4). **Survives? No — either its surplus contradicts a premise of the theory, or it has none.**

**(iii) Diameter vs radius.** The maximum separation is metric-dependent: through the bulk it is
2ℓ₁ (antipodal points), along the boundary 2-sphere it is πℓ₁, and as an area ratio it is
A/(2πℓ₁) = 2ℓ₁ again (sphere area over hemisphere area) — the diameter in a third dress. The ball
has six natural lengths
(K7, exact): radius 1, mean radius 3/4, mean chord 4/3, RMS chord √2, diameter 2, antipodal arc π
— giving R = 1, 0.5625, 1.777778, 2, 4, 9.869604, six distinct values of which **exactly one** is
4. Tensions against κ_meas: 6.137σ, 9.646σ, 3.505σ, 3.054σ, **0.874σ**, **1.039σ**. So the data do
not select the diameter even among lengths of one ball: the boundary arc fits at 1.04σ. *Surplus:*
"maximum separation" makes the two-point function have compact support at r = 2ℓ₁ =
9.608066e26 m = 31.138 Gpc = 5.789 r_H — super-horizon, hence unobservable (K9). **Survives? No:
it is a renaming (D1), not unique (D2), and its one distinctive consequence is outside the
observable universe (D4).**

**(iv) Deep-MOND slope.** n = 2 is a statement about the *shape* of the RAR. Exactly:
d ln g/d ln g_N = 1/2 for every a₀, and a₀ → λa₀ rescales g by √λ while leaving the exponent at
1/2 (K10). So n is invariant under precisely the rescaling that β measures — the identification
β = n has sensitivity zero by construction. Numerically: the two footings both have n = 2 and give
R = 3.995022 and 2.741031 (ratio 1.457489). Stronger, inside the theory: the canonical law and the
half-capacity variant share n = 2 *and* the same deep limit, and differ in saturation offset by
exactly 2 (a₀ vs a₀/2, K11) — the slope does not even fix the capacity. **Survives? No: image ∅
(D2); it is a category error between an exponent and a length ratio, not an alternative mechanism.**

**(v) Two cells.** A count is dimensionless; a length ratio needs an exponent fixed by dimension.
Two cells per correlation volume gives the linear factor 2^{1/3} = 1.259921 (κ = 0.793701,
R = 1.587401, **3.97σ**); a linear factor 2 needs 2³ = 8 cells (K12). The 2 in the premise is a
count and cannot appear as a length ratio without the cube root. *Surplus:* state density 2/V_c
predicts κ = 0.794, excluded at 3.97σ. **Survives? No — dimensionally wrong and numerically
excluded.**

**The dichotomy.** Two candidates return exactly 2 (ii-Dirichlet, iii-diameter) and in both the 2
is a naming convention: the wall sits at ℓ₁, the diameter is 2ℓ₁. In the three where the 2 is a
substantive premise — two legs (i), two cells (v), exponent (iv) — the answer is 0.690988,
1.259921, and nothing; the first two are excluded at 10.84σ and 3.97σ and the third has no
output. Over this class: *the 2 is either a convention or a premise, and when it is a premise it
is wrong.* That is the sharp form of the no-go.

Only one candidate returns exactly 2 **and nothing else**: (iii), the bulk diameter. It has no
surplus content whatever — no extra number, no extra observable — which is precisely the diagnostic
of a redefinition rather than a derivation. (ii) also returns 2 but carries a surplus, and that
surplus contradicts the law's form.

## What the data actually select

A19 §5 and FINAL_THEORY §1.4 read the cap family R ∈ {1,2,4} as three dynamical options. By K13
they are exactly three **geometric functionals of the same ball**: R = 1 is the radius, R = 2 the
RMS chord (√2ℓ₁), R = 4 the diameter. So "the data select 4 at 0.87σ over 2 at 3.05σ" is a
statement that nature uses the *maximum* separation rather than the *typical* one — a choice among
lengths, not among dynamics. And it is not yet decided: the boundary antipodal arc (β = π) fits at
1.04σ. At σ_κ = 0.005 the diameter separates from the RMS chord at 41.421σ and from the radius at
100σ, but that would still only rank geometric functionals of one ball; it would not turn the
winner into a derivation.

## Status

**`NO-GO(obstruction)`.**

**Theorem A27-T1.** In the class of arguments 𝔏 = {(Σ, link)} where Σ is a statement about Λ and
the geometry of a cell of radius ℓ_χ and link is "L is a length functional of the cell":

- (a) the conclusion of every member, written in (a₀, Λ, c), is a₀ = c²/(β g(ℓ_χ)) — i.e. the
  argument *defines* a₀ and outputs no constraint on β (link lemma, K15: 4/4);
- (b) β is a free label: the natural functionals of one ball realise six distinct β and six
  distinct R (K7), and the topological index χ shifts β along the curve β√χ = 2 (K2);
- (c) the sub-class whose β can be checked against κ without naming it — horizon round trip,
  two-cells, slope — returns 0.690988 (10.84σ), 1.259921 (3.97σ) and no number at all (K4, K12,
  K10);
- (d) the sub-class that returns 2 does so with image {2} (D2 failure) in every member.

Hence no member of 𝔏 derives β = 2, and by T1(a) any member that did would derive κ = ½.
**The missing premise**, stated so it can be attacked: *a dynamical statement that fixes which
functional of the cell the law's length is, without naming it* — i.e. Σ must contain a variational
or spectral problem whose output is a length built jointly from Λ and the cold sector, not a pure
number. That is A19's T1b escape route, now localized to the link rather than to the count.

Register wording this lane supports: *"L = 2ℓ₁ is not a geometric fact; it is κ = ½ spelled in
lengths. The cell ball has six natural lengths; the diameter is one, the boundary arc πℓ₁ fits the
data as well, and the three non-circular readings of 'twice' are excluded at 10.84σ, 3.97σ and by
having no output. The factor 2 is a normalisation, FITTED with κ (CFG493)."*

## Checks

| id | what it measures | value | verdict |
|---|---|---|---|
| K1 | R ≡ β², κ ≡ 1/β; three spellings give one a₀* | max residual 0; a₀* = 9.354173e-11 | PASS |
| K2 | κ = 1/(β√χ); (2,1) and (1,4) both exact | κ = 1/2, R = 4 both; tested pair 0.5 | PASS |
| K3 | footing: R, κ, β, L, ℓ₁, 2ℓ₁, a₀(2ℓ₁) | \|R−4\| = 4.977e-03; 2ℓ₁ = 9.608066e26 | PASS |
| K4 | (i) literal round trip | β = 0.690988, κ = 1.447203, 10.84σ | PASS |
| K5 | (ii) Dirichlet λ_max = 2ℓ₁ exactly; Neumann ∞ | 2.0 vs ∞ | PASS |
| K6 | (ii) surplus: tower modulation size | 1.618034, 1.931852, 2.188901 | PASS |
| K7 | (iii) six natural lengths, six R, one = 4 | 6 distinct; 1 equals 4 | PASS |
| K8 | (iii) tensions; arc vs diameter | 1.039σ vs 0.874σ | PASS |
| K9 | (iii) compact-support edge vs horizon | 5.789 r_H = 31.138 Gpc | PASS |
| K10 | (iv) slope invariant under a₀ → λa₀ | 1/2 → 1/2; R ratio 1.457489 | PASS |
| K11 | (iv) same n = 2, offset ratio | a₀ vs a₀/2, ratio 2 | PASS |
| K12 | (v) 2^{1/3} ≠ 2; needs 8 cells | 1.259921, 3.97σ | PASS |
| K13 | caps {1,2,4} ↔ {radius, RMS chord, diameter} | max residual 0 | PASS |
| K14 | β invariant under unit rescaling | residual 0 | PASS |
| K15 | elimination test on every link premise | 4/4 fix a₀; tautology 0 | PASS |
| K16 | no candidate's image is {2} | 0 candidates; min size 2 | PASS |

## What this does not do

- It does not prove no dynamics can fix β. It proves the five named mechanisms do not, and that
  the *class* 𝔏 cannot, because β enters 𝔏 only as a label.
- The six-length table is not exhaustive: any smooth functional of the ball yields a length, and
  the argument only needs *two* to break uniqueness.
- It does not re-derive κ's measurement; the σ-tensions are κ's own evidence (CFG493).
- It does not test "2 = two polarisations / two pieces of Cauchy data": those 2s count components
  and cannot appear as a length ratio without a frequency — the same failure as (v).
- It does not claim the boundary-arc reading is physics. It claims the data cannot tell it from
  the diameter, which is enough to deny that the data select the diameter.

## Next

1. **The link is the target, not the 2.** A successor should try to produce a functional whose
   stationarity outputs a *length* (not a pure number) built from Λ and T^φ jointly — the one shape
   A19's T1b left open.
2. The only mechanism shapes that could satisfy D2 are (a) a two-boundary variational principle
   whose boundary coefficients are fixed by well-posedness rather than chosen (so the 2 is a
   coefficient), and (b) a spectral problem whose *gap*, not its fundamental, is the scale — a gap
   ratio can be a pure number fixed by the spectrum.
3. Pre-registered: at σ_κ = 0.005 the diameter separates from the RMS chord at 41.421σ, from the
   radius at 100σ, from the boundary arc at 36.338σ. That decides *which functional*, not *why*.