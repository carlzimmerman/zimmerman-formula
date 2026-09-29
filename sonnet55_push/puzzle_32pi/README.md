# Is AΛ = 32π² a coincidence? (c = G = 1) -- working notes and results

**Question.** Λ = 32π a₀² (equivalently the Rindler length 1/a₀ = √(32π/3) × the de Sitter radius √(3/Λ)). A Schwarzschild horizon with
surface gravity a₀ has area A = π/a₀², so AΛ = 32π² -- the Chern-Gauss-Bonnet constant in four dimensions. Is there a natural
geometric reason for 32π here? Scripts: `p01_exact_reductions.py` (23/23, sympy curvature computations), `p02_matching_scan.py`
(pre-declared scan, 3 controls); Lean: `fable_independent_2026/lean_2026/PUZZLE_32pi_reductions.lean` (11 theorems, standard axioms, MUTATE rejected).

## Bottom line
I found no Gauss-Bonnet (or other topological) reason, and I can show that none *can* exist in the form asked. What the coincidence
reduces to exactly is a statement about the horizon's Gauss curvature and the vacuum energy density:

    A Λ = 32π²  <=>  Λ = 32π a₀²  <=>  a₀ = ½ √ρ_Λ  <=>  ρ_Λ r_s² = 1  <=>  K_Σ = ρ_Λ        (ρ_Λ = Λ/8π, r_s = 1/(2a₀), K_Σ = 1/r_s²)

i.e. the Schwarzschild black hole with κ = a₀ is the one whose horizon 2-sphere has Gauss curvature equal to the vacuum energy density.
The 32π² and the "32π" are then bookkeeping: 32π² = (8π)(4π), Einstein's 8π times a solid angle. Nothing beyond the ½ (the fitted κ) is explained.

## 1. Why the numbers match: 32π² = (8π)(4π) = 2(4π)²
- AΛ = (4π r_s²)(8π ρ_Λ) = 32π² ρ_Λ r_s². So AΛ = 32π² is EXACTLY ρ_Λ r_s² = 1, an O(1) relation between a density and a length.
  Any relation "Gρ_Λ r² = 1" for a sphere would give 32π². This is not Gauss-Bonnet.
- Gauss-Bonnet's constant is 32π² for the same reason: E₄ = 2R₁R₂ on S²×S² (computed, p01 G4) and ∫_{S²}R = 8π, so ∫E₄ = 32π²χ.
  Also 32π² = 12 Vol(S⁴_unit) = ∫_{S⁴(1)} R dV. Two different uses of "8π × 4π".
- Where 32π really appears with Λ: the on-shell Euclidean action of de Sitter, S_dS = (1/32π)∫_{S⁴}R dV = πL² (the 32π is 16π from Einstein-Hilbert times 2
  from the on-shell Λ term); and the Euler charge per unit Killing time, ∫_{static slice}E₄ dV₃ = 32π κ (see 2).

## 2. Gauss-Bonnet cannot fix a scale
Computed from the Riemann tensor (p01), all independent of the size:
- Euclidean de Sitter S⁴(L): E₄ = 24/L⁴, ∫E₄ = 64π² for every L (χ = 2).
- Euclidean Schwarzschild: E₄ = 48M²/r⁶, ∫E₄ = 64π² for every M (χ = 2).
- Euclidean Nariai S²×S²: E₄ = 8Λ², ∫E₄ = 128π² (χ = 4).
- The Euler charge per unit Killing time is 32π κ for BOTH Schwarzschild (8π/M, κ = 1/4M) and de Sitter (32π/L, κ = 1/L): the Hamiltonian form of ∫E₄ = (2π/κ)(32πκ) = 64π².
So the Euclidean black hole and Euclidean de Sitter carry the SAME Gauss-Bonnet number at every size. A scale-free integer cannot say how large one is
relative to the other. To turn a topological invariant into a length ratio you need a dimensionful coupling (e.g. an Einstein-Gauss-Bonnet coefficient) or flux
quantisation; none is present in the puzzle as posed.

## 3. Why a pure-geometry matching cannot give 32π/3, and what does
Z² = (1/(a₀L))² = 32π/3 contains one π (transcendental, Lindemann). Any equation between LOCAL metric invariants of Schwarzschild (algebraic in M) and de Sitter
(algebraic in L) gives M/L algebraic, so it can never equal 32π/3. A π needs (a) Einstein's coupling, ρ_Λ = Λ/8πG, or (b) a horizon area/volume (4π, 8π²/3).
`p02` tests a menu I fixed in advance (12 Schwarzschild quantities x 14 de Sitter quantities, every same-dimension pair, 34 pairs): 8 of the 34 contain a π (a π
on exactly one side, as the argument requires) and EXACTLY ONE gives 32π/3: **K_Σ = ρ_Λ**. Its near sibling κ² = ρ_Λ gives 8π/3 (the Friedmann coefficient), a factor 4 smaller.
The factor 4 is r_s = 1/(2κ) squared: K_Σ = 4κ². So the fitted κ = ½ is exactly the difference between "κ² = ρ_Λ" and "K_Σ = ρ_Λ".
Caveat, stated plainly: I wrote the menu knowing the target, and it contains the quantity that hits; this characterises the hit, it does not measure a false-positive rate.

## 4. The Milgrom comparison (a real structural difference)
With Milgrom's a₀ = cH/2π: Λ = 12π² a₀², so AΛ = 12π³ -- one more π, from the thermal period 2π in the Unruh temperature. The framework's 32π² has exactly two,
the count expected for classical GR (one from Einstein's 8π, one from the horizon area). So the relation is a classical statement, with no thermal 2π: consistent with
it having no ħ, and a reason not to look for its origin in Unruh/Hawking matching.

## 5. What would count as an explanation
The relation says r_s√(Gρ_Λ) = c: the light-crossing time of the black hole's horizon equals the vacuum's gravitational dynamical time 1/√(Gρ_Λ). A derivation
would have to (a) say why the acceleration scale is the surface gravity of a Schwarzschild horizon (κ = g_N(r_s) = c²/(2r_s) exactly, a special property of the
Schwarzschild solution), and (b) supply the dynamical reason for r_s = c/√(Gρ_Λ). I found neither. This is the record's κ = ½, restated, not derived.

## Not established
- That no principle exists: I searched exact curvature integrals, the Euler charge, the on-shell action and 34 matching conditions, not every possibility.
  One further route was checked by hand and gives nothing new: a Gauss-Bonnet term with the Kounterterm coefficient that makes the renormalised on-shell action
  of S⁴ vanish has α = -L²/4; the Wald/Jacobson-Myers entropy is then S = A/4 + 4πα = A/4 - πL², which vanishes at A = 4πL², the de Sitter horizon's own area,
  not at 32π²/Λ. Junction conditions and the 4D Einstein-Gauss-Bonnet black holes were not developed.
- Anything about why κ = ½. kappa = 1/2 stays FITTED.
