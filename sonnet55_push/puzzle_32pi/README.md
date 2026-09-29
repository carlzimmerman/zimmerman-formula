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
  not at 32π²/Λ. The 4D Einstein-Gauss-Bonnet black hole was then checked (`p03`): its maximal Hawking temperature gives κ_max² = 0.0164/α, no 32
  (a first version of that check used a wrongly remembered temperature and failed; the corrected one is committed and the 'lead' is retracted). Junction conditions were not developed.
- Anything about why κ = ½. kappa = 1/2 stays FITTED.

## 6. Piecing it together with the rest of the repo (2026-09-29)
What the repo already established, and how this folder fits:
- **The 2026-06-15 "derive Z" verdict** (`opus_48_extended_research/reviews/DERIVE_Z_FRESH_RUN_VERDICT_2026-06-15.md`, five routes, every step in sympy): Z is an
  UNFORCED POSIT. The form (a0 ~ c²√Λ), the √-law, the 8π (Einstein) and the 3 (Friedmann) are forced, giving the forced kernel **Z = √(8π/3) = 2.894 (κ = 1)**; the
  entire remaining content is κ = ½, "the lone factor of 2". Its "32π = 8π × 4 as Einstein × entropy-quarter" lead was killed as numerology (a literal second Bekenstein-Hawking
  quarter gives Z = 11.58). The scan and the Gauss-Bonnet no-go in this folder agree, and add: exactly one of 34 pre-declared matchings reproduces 32π/3 (K_Σ = ρ_Λ), and a
  topological invariant is scale-free.
- **`deepseek_push/GEOMETRIC_EQUATIONS_SYNTHESIS_2026-09-22.md` Part 1** already states the relation as a₀ = (c/2)√(Gρ) = "the surface gravity of the free-fall horizon at R* = c/√(Gρ)".
  That is my K_Σ = ρ_Λ, i.e. r_s = R*, with the Schwarzschild κ = c²/(2r_s) supplying the ½. It also gives the dimension lock Z_d = 8√(π/(d(d-1))).
- **`p04_equivalence_web.py` (13/13)** proves that TEN formulations the repo uses are the same statement, each with the unique positive root κ = ½:
  Λ = 32πa₀²; AΛ = 32π² (Schwarzschild κ = a₀); horizon Gauss curvature = ρ_Λ; Rindler length = 2R*; unit response p'(0) = 1; memory moment M₁ = (4/3)t_Λ;
  four-form Z_q + 2bβ² = 8β²; the Unruh mode count n = Z; Z = 2√(8π/3); Ω_Λ = 32πa₀²/(3H₀²c²). Deriving any one derives all; the repo has not derived any.
- **The repo's "Z² = 8 × Vol(unit 3-ball)" reading is a d = 3 coincidence.** The dimension-covariant Friedmann form is Z_d² = 64π/(d(d-1)) = 32π/dim SO(d);
  it equals 8 Vol(B^d) only at d = 3 (`p04` part B). So the structural content of the "3" is dim SO(3), the number of independent 2-planes of the spatial slice
  (H² = 8πGρ/dim SO(d)), not a ball volume. This weakens the "bulk-boundary conversion" gloss and leaves the Friedmann origin of 8π/3 intact.
- **The data do not decide the coefficient** (`p03`): on the ρ_total footing three of four natural candidates (Milgrom 2π at -0.59σ, Verlinde 6 at +0.25σ, √(32π/3) at +0.93σ)
  lie within 1σ of the SPARC a₀; the Nariai-shell 3√3 is at +3.1σ. On the ρ_Λ footing all sit 2.4-3.7σ low. So no measurement forces 32π over its neighbours.

Where a derivation could still hide (each is a statement of the ONE number; none is a proof):
1. formulations 3 and 4 compare two geometric objects (a horizon's curvature or length, and a density-derived length): a variational or junction-condition principle setting r_s = c/√(Gρ_Λ) would do it;
2. formulations 5-7 are normalisations or response coefficients inside an action (unit susceptibility, the four-form ratio, the memory moment 4/3 = the enthalpy ratio (ρ+p)/ρ of a
   p = ρ/3 component): the repo's action-route audit shows the checked actions leave Z_q/β² free, so the missing object is a principle or symmetry that fixes it;
3. the mode-count form (8) needs n = Z, a non-integer: an integer count cannot give it, so if it is a count it must be a measure (a weight or a volume ratio), not a number of channels.
Not established: that any of these can be derived; nothing here shows κ = ½ is anything but fitted.

## 7. The ½ as a slope, and five structural origins that all say ½ at d = 3 (`p05`, 7/7)
With s = c√(Gρ_Λ) and p = g/s, the interpolation function μ = 1 - (1-p)^N has μ'(0) = N, so a₀ = s/N. The natural, no-free-factor crossover is the Rindler distance
c²/g = R* = c/√(Gρ_Λ): κ = 1, Z = √(8π/3) = 2.894 (the repo's "forced kernel"). The framework's ½ is N = 2. Read this way the literature coefficients are all "the forced kernel
times about two": Milgrom 2π is N = 2.17, Verlinde 6 is N = 2.07, √(32π/3) is exactly N = 2, and the Nariai-shell 3√3 is N = 1.80. So the robust content is a factor of about 2,
with the fine value (5.79, 6, 6.28) inside the data's 10%.
Five natural structural origins of that 2 all give exactly ½ at d = 3 and different values elsewhere: two static response channels (½ for every d), the Tolman count d-1
(1/(d-1)), the D-dimensional Schwarzschild surface gravity ((d-2)/2), the enthalpy premise ((2/3)d/(d+1)), and the fixed-Z rigidity form (√(3/(2d(d-1)))). At d = 4 they range
from 0.33 to 1.00. So d = 3 alone cannot tell which, if any, is the real origin, and agreement of several rational functions at one point is weak evidence (many functions equal ½ at 3).
That is the sharpest statement of the open problem I can make: find a principle for the 2 (a channel count, a horizon count, an enthalpy, a normalisation), and check it in a second dimension.

## 8. The puzzle's horizon cannot exist inside its own universe (`p06`, 14/14) -- a no-go, not a derivation
Take the puzzle literally: a Schwarzschild horizon with surface gravity a₀ has r_s = ZL/2, mass M_s = ZL/4, area A_s = (8π/3)A_dS. Placed in the de Sitter universe with that Λ:
- **Schwarzschild-de Sitter has no horizon at all** (M_s/M_Nariai = 3√3 Z/4 = 7.52). The object is not a solution of that universe. Its entropy A_s/4 = (8π/3) S_dS exceeds the dS bound.
- **Embeddable iff Z ≤ 2** (r_s ≤ L), i.e. κ ≥ 1. The fitted κ = ½ (Z = 5.79), Milgrom's 2π and Verlinde's 6 all lie outside. So any a₀ on the data's scale is a *sub-Hubble* acceleration (a₀ ≈ H/6) that no real horizon of this universe carries.
- **Gravitating-wall route closed** (Israel junction, checked over 20,000 random cases): a real wall needs 1/R² ≥ max(H_in², H_out²), so any wall's acceleration is ≥ H for every tension. a₀ = H/Z would need σ² < 0. A Brown-Teitelboim membrane in the gravitating regime therefore cannot supply a₀; only the probe limit (a = eE/σ, a free ratio) is left.
Consequence for the search: a derivation cannot come from a real geometric object (horizon, wall, bubble) of the Λ-universe. It has to be a response coefficient (a normalisation of the medium/field, formulations 5-7 of section 6) or an analytic-continuation quantity. That narrows where the ½ can live; it does not supply it. κ = ½ stays FITTED.
Not a result: `p06` check D2 is bookkeeping (the static-patch angle tanθ₀ = 1/Z has no special value), and Z ≤ 2 embeddability is a sharp fact about the *puzzle's* object, not evidence about the field-theory a₀.

## 9. Membrane probe route: closed, and a correction to section 8 (`p07`, 6/6)
Section 8 said a Brown-Teitelboim membrane "survives only in the probe limit, where the ratio is free". `p07` shows that was too generous.
In the probe limit the wall's acceleration is 1/R = ΔP/(3σ) (Schwinger radius R = 3σ/ΔP, recovered from the Israel solution), so κ = ½ would need a charge-to-tension ratio e/σ = 3/(2√2) = 1.061
(general κ: 3κ/√2), independent of E. But that formula is valid only when ΔP/(3σ) ≫ H, and at the target it equals H/Z ≪ H. The full junction solution at that ratio (σ → 0) gives 1/R = 2.077 vs H = 2.047 (E = 1):
the wall sits at the horizon and accelerates at ≈ H, not H/Z. So no membrane, probe or gravitating, has proper acceleration a₀; the route is closed, not merely under-determined.
The 1.061 is a convention-laden coupling ratio (Heaviside four-form, ρ = E²/2, ΔE = e) and matches none of 1, √(3/2), 3/2, √2; it is reported as a target only.
