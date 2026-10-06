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
  lie within 1σ of the SPARC a₀; the Nariai-shell 3√3 is at +3.1σ. On the ρ_Λ footing three of the four sit 2.4-3.7σ low; the Nariai-shell 3√3 sits at −0.57σ (audit M2; H0-dependent, statistical error only). So no measurement forces 32π over its neighbours.

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
> **CORRECTED (see section 12): the wall/membrane and 'no real horizon' conclusions of this section are WITHDRAWN. Only the flat-space-Schwarzschild statements (M_s/M_Nariai = 7.52, A_s/A_dS = 8 pi/3, i.e. a0 < cH/2) stand. 'kappa >= 1' below should read kappa >= sqrt(2 pi/3) = 1.447.**
Take the puzzle literally: a Schwarzschild horizon with surface gravity a₀ has r_s = ZL/2, mass M_s = ZL/4, area A_s = (8π/3)A_dS. Placed in the de Sitter universe with that Λ:
- **Schwarzschild-de Sitter has no horizon at all** (M_s/M_Nariai = 3√3 Z/4 = 7.52). The object is not a solution of that universe. Its entropy A_s/4 = (8π/3) S_dS exceeds the dS bound.
- **Embeddable iff Z ≤ 2** (r_s ≤ L), i.e. κ ≥ 1. The fitted κ = ½ (Z = 5.79), Milgrom's 2π and Verlinde's 6 all lie outside. So any a₀ on the data's scale is a *sub-Hubble* acceleration (a₀ ≈ H/6) that no real horizon of this universe carries.
- **Gravitating-wall route closed** (Israel junction, checked over 20,000 random cases): a real wall needs 1/R² ≥ max(H_in², H_out²), so any wall's acceleration is ≥ H for every tension. a₀ = H/Z would need σ² < 0. A Brown-Teitelboim membrane in the gravitating regime therefore cannot supply a₀; only the probe limit (a = eE/σ, a free ratio) is left.
Consequence for the search: a derivation cannot come from a real geometric object (horizon, wall, bubble) of the Λ-universe. It has to be a response coefficient (a normalisation of the medium/field, formulations 5-7 of section 6) or an analytic-continuation quantity. That narrows where the ½ can live; it does not supply it. κ = ½ stays FITTED.
Not a result: `p06` check D2 is bookkeeping (the static-patch angle tanθ₀ = 1/Z has no special value), and Z ≤ 2 embeddability is a sharp fact about the *puzzle's* object, not evidence about the field-theory a₀.

## 9. Membrane probe route: closed, and a correction to section 8 (`p07`, 6/6)
> **WITHDRAWN (section 12, H1): this section's 'correction' was itself wrong. The wall's proper acceleration in de Sitter is sqrt(1/R^2 - H^2), not 1/R; the membrane route is OPEN with one free ratio, exactly as section 8 originally said.**
Section 8 said a Brown-Teitelboim membrane "survives only in the probe limit, where the ratio is free". `p07` shows that was too generous.
In the probe limit the wall's acceleration is 1/R = ΔP/(3σ) (Schwinger radius R = 3σ/ΔP, recovered from the Israel solution), so κ = ½ would need a charge-to-tension ratio e/σ = 3/(2√2) = 1.061
(general κ: 3κ/√2), independent of E. But that formula is valid only when ΔP/(3σ) ≫ H, and at the target it equals H/Z ≪ H. The full junction solution at that ratio (σ → 0) gives 1/R = 2.077 vs H = 2.047 (E = 1):
the wall sits at the horizon and accelerates at ≈ H, not H/Z. So no membrane, probe or gravitating, has proper acceleration a₀; the route is closed, not merely under-determined.
The 1.061 is a convention-laden coupling ratio (Heaviside four-form, ρ = E²/2, ΔE = e) and matches none of 1, √(3/2), 3/2, √2; it is reported as a target only.

## 10. Gauss-law / four-form flux form of the puzzle (`p08`, 6/6): it exists and is the same identity
Raised by a peer session (the dark-energy field-equation lane) as a question for this lane. In Henneaux-Teitelboim / Brown-Teitelboim language F₄ = E vol₄ with E constant, ρ = E²/2 = Λ/8π, and the dual current obeys div T = √g (flux = 4-volume).
Result: A_{a₀} = π/a₀² = 4 Vol(S⁴_L)/L² = (4/3) Λ Vol(S⁴_L), equivalently A_{a₀}/S_dS = Z² and S_{a₀}/S_dS = 8π/3; the four-form flux through S⁴ is Φ = E·Vol = 4√3 π^{3/2} L³/3.
- This is the known reduction 32π² = 12 Vol(S⁴₁) = ∫R dV (section 1), rewritten with the flux. Check 5 shows it is an identity once a₀ := H/Z is defined; it restates Z² = 32π/3, it does not derive it.
- Flux quantisation Φ = n·e fixes L³ (that is, Λ) for given n, e. It contains no relation between a₀ and Λ: a₀ enters only through Z, the input.
- The a₀ "horizon" is a 2-surface whose radius exceeds L (`p06`); a 3-form flux needs a 3-volume, and the Gauss law counts 4-volume. So there is no flux *through the a₀-horizon*; the only Gauss-law statement is about Vol(S⁴).
- The one thing the form does show is the π-counting result again: with Z² ∝ π (framework, forced kernel) the coefficient of ΛVol₄ is rational (4/3, 1/3); with Milgrom's Z = 2π it is π/2 and with Verlinde's Z = 6 it is 9/(2π) (corrected from 27/(2π), audit M8). Rationality is a property of Z² ∝ π, not a selection of the ½.
So the answer to "is there a Gauss-law form of 32π?" is yes, and it carries no new content: the coefficient must still be supplied by the field's coupling. κ = ½ stays FITTED.

## 11. Vacuum self-consistency route (`p09`, 6/6): a scoped no-go, plus a correction to my own framing
> **CORRECTED (section 12, H3): the 'no-go' is unit-dependent. In units of a0^2/G the puzzle is W_v = 4, which a local algebraic potential can reach; only the reduction G rho = 4 a0^2 <=> U_v = 32 pi (U = 8 pi W) survives. Do not cite this as a no-go.**
Correction first: "V0" in the record is the name of the C-H/K action (CV1-CV4), not a vacuum potential; its "obstructed" status concerns the region gate, so it says nothing about this route. What the record does say (`campaign_fresh_gravity/closure_map/ACTIONS_AND_NOGOS.md`): in astra's CA4/CA5 action the a₀-vacuum relation is "an optional input, not a consequence of this action"; the chain action ties a₀ to Λ only by writing α(Λ) = κ√(Λ/8π) in by hand (XR20 T1).
The test: let Λ not be independent, i.e. the dark-energy density is the vacuum value of the a₀-sector's own potential, S = (1/16π)∫√-g [R − 2a₀²U(φ) + kinetic] (a₀²/8πG is the Poisson-normalised MOND scale). On shell, Λ_eff = a₀²U_v and Gρ = a₀²U_v/(8π). The puzzle Gρ = 4a₀² is then exactly **U_v = 32π**.
- A local potential with algebraic coefficients has an algebraic stationary value; 32π is not algebraic (Lindemann; an integer-relation search to degree 8 finds nothing, control passes). So a *local* algebraic self-consistency cannot reproduce the puzzle. The π must be put into the potential or the normalisation, which is again the inserted coefficient. (The algebraic-value check is close to trivial; the content is the reduction to U_v = 32π.)
- This agrees with the π-counting of section 3: a π appears only with a global integral (an area, a volume, a Gaussian) or with the 8πG dressing. In the record's filtered actions (S_h = e^{bΔ}) a Gaussian normalisation (4πb)^(-3/2) does bring a π, so the no-go is scoped to local potentials and does not exclude the nonlocal CA5 sector; that is the only part of this route I have not closed, and it would need the filtered action's vacuum energy computed, not assumed.
Net: self-consistency turns the puzzle into a sharper question -- why is the a₀-sector's own vacuum value 32π in Poisson units -- and shows a local action cannot answer it. κ = ½ stays FITTED.

## 12. Corrections after the independent audit (`agents/I_adversarial_audit/`, 2026-09-29) -- read before citing anything above
Two of my negative claims were wrong, one was unit-dependent, and several were overstated. The identities, curvature numbers, `p01`-`p10` outputs and the Lean file reproduce; nothing here derives or excludes κ = ½.
- **H1 (withdrawn: sections 8 bullet 3, 8 'consequence for the search', 9, `p06` A, `p07` 6).** A wall's proper acceleration in de Sitter is √(1/R² − H²) (embedding acceleration 1/R minus the normal piece 1/L; checked against the static observer a = (c/L²)/√(1−c²/L²)). For a pure-tension wall it is 2πGσ for every H; the Israel quantities A, B = ΔP/(3σ) ± 2πσ are the two sides' accelerations. So a₀ = H/Z IS reachable (σ = a₀/2π), the probe formula needs no 'a ≫ H', and the '1/R = 2.077 vs H = 2.047' number is an S³ radius, not an acceleration. The membrane route is open, with the single free ratio e/σ = 3/(2√2) (Heaviside convention). `p06` A3 was a sum-of-squares test that cannot fail. What survives: the Unruh-effective acceleration √(a²+H²) = 1/R is ≥ H for every worldline, which is not the MOND a₀ (an acceleration relative to free fall).
- **H2 (scope).** 'No real horizon carries a₀' is normalisation-dependent: in the f-normalisation of the Killing vector an SdS horizon has κ = a₀ exactly (M = 0.98695 M_Nariai), in the Bousso-Hawking normalisation every SdS horizon has κ ≥ H. What `p06` B proves is about the flat-space Schwarzschild mass and the formula A = π/a₀² (equivalent to a₀ < cH/2), not about which surface gravities occur. The claim that 'a derivation cannot come from a real horizon/wall/bubble' is unsupported.
- **H3 (unit-dependence).** π-counting arguments ('local algebraic relations cannot give a π') depend on which variable is called natural. In G ρ_Λ = 4 a₀² there is no π; the π lives in Λ = 8πGρ_Λ and A = 4πr². In units of a₀²/G the vacuum condition is W_v = 4, reachable by an explicit local algebraic potential. Sections 3, 4 and 11, and the sibling agent lanes that use π-class arguments (`agents/B`, `agents/G`), are therefore conditional on treating a₀/H (not Gρ_Λ/a₀²) as the quantity fixed. The reduction itself (Gρ = 4a₀² ⇔ U_v = 32π) is fine.
- **M1.** 'Gauss-Bonnet is scale-free' is for smooth closed or asymptotically flat geometries. For two-horizon Euclidean SdS regular at one horizon and conical at the other, the smooth-part integral is 64π²(1 + κ_c/κ_b), a ratio of surface gravities (audit `a08`); no Z-specific value comes out of it.
- **M3.** 'Embeddable iff Z ≤ 2, i.e. κ ≥ 1' should read κ ≥ √(2π/3) = 1.447 (at κ = 1, r_s = 1.447 L, also not embeddable).
- **M4.** 'Ten formulations are the same statement; deriving any one derives all' overstates: rows 1-4, 9, 10 are algebraic rewritings; rows 5-8 are premise-conditional (p′(0) = 1 fixes N = 2 by the convention μ = 1 − (1−p)^N; M₁ is defined from a₀; the four-form row has three free numbers; the mode count needs a non-integer n).
- **M5.** The 'exactly 2π ⇒ classical, no thermal 2π' inference in section 4 is a non sequitur (32π² = 8(2π)² = 2(4π)² = 12 Vol S⁴, so π-count is not an invariant of origin); thermal readings are not excluded.
- **Also:** `p02`'s 'one of 34' is effectively one of two admissible pairs (a decoy target is hit 9-18% of the time), so it is uninformative; the SPARC a₀ is 15% above the framework's cH_Λ/Z (2.4σ), so the coincidence being explained is itself approximate on the ρ_Λ footing; `p10` claims are true but two of its four checks were tautological (repaired in the audit's `a06`, 12/12). The record errors flagged by other lanes (PD11 Tolman count) are their claims, not verified here.

## 13. The agent campaign (2026-09-29): twelve lanes, no derivation (`agents/`, read `agents/BRIEF.md` first)
Every lane below wrote its own scripts, controls and README; I re-ran the scripts of B, D, F, G, A, H (Lean build), K, L, J myself (all exit 0, counts match). None derives κ = ½; κ = ½ stays FITTED.
| lane | question | verdict | what it leaves |
|---|---|---|---|
| A instanton/gauge-gravity | does anything with a scale enter the S⁴ instanton/MacDowell-Mansouri structure? | no-go | S_dS = 2 × instanton action (ħ-free ratio χ = 2); a₀² = c⁴Λ/(32π) has no G or ħ, so quantisation fixes Λ, never a₀: the factor must be a classical ħ-free coefficient |
| B gravitational waves | is 32π a GW/graviton quantity that ties to Λ? | no-go (scoped) | 32π = graviton normalisation (Isaacson 8π×4; κ_g² = 32πG), unrelated to Λ; puzzle ⇔ ω h₀ = √(Gρ_Λ) with coefficient 1 unexplained |
| C census | where else is 32π used, and why? | nothing new | 41 instances of different origins (topological / Einstein-Hilbert normalisation / angle integral / accident); no classical instance ties a rate to Gρ with a π-free coefficient |
| D filtered vacuum | can the nonlocal (heat-kernel) sector supply the π? | no-go (scoped) | homogeneous vacuum is exactly GR + constant, filter-blind; solved-for filter widths are meaningless (20/20 decoys hit) |
| E literature | any published derivation of the coefficient? | no-go | ~35 works, all insert it; horizon-first routes give rational Z; only a₀²-linear-in-density forms allow exactly ½ |
| F dimension | does d select one of the five readings? | no-go | seven κ(d), all ½ at d = 3 by construction; record's 'Tolman lock' contains an error (claimed by F; not independently verified here) |
| G symmetry | can a symmetry fix a₀/√(Gρ_Λ)? | no-go | algebraic vs π dichotomy: only the π-free form Gρ_Λ = 4a₀² is symmetry-accessible; no symmetry contains it |
| H Lean | certify the bridges | certified bridges | 110 theorems in 8 files, 41 false variants rejected, default axioms; certifies premises ⇒ conclusions only; π's transcendence is not in Mathlib |
| I audit | are my README claims right? | corrections | section 12: walls (H1) and the p09 no-go (H3) withdrawn, horizons scoped (H2) |
| J membrane extremality | does BPS/no-force/threshold fix e/σ? | no-go on declared principles | target e²/(Gσ²) = 9/8 (π-free); gravitational principles vanish in the probe limit; the near-hit n = 16 is noise (58% of decoys do as well) |
| K density-linear family | is the AQUAL/potential offset the vacuum energy, and does it fix 4? | no-go (conditional discriminator) | c = ∫(1−μ)dy is set by the far tail (x ≳ 10 to 10⁶), untestable by SPARC/Solar System; the offset reading forces flat a₀(z) |
| L SdS two-horizon | does a principle pick the near-Nariai point where κ_b = a₀? | no-go | monotone family, only the endpoints are special; 19 functionals have no interior extremum; integer quantisation gives only μ = 1/√2 |
**Net.** The 32π at the a₀ scale is not explained by any of: graviton/GW normalisation, instanton or Gauss-Bonnet topology, the S⁴ spin connection, a symmetry, a nonlocal filter, dimension, membranes/walls, the MOND-offset constant or the SdS family. What survives as the open target: the rational coefficient 4 in Gρ_Λ = 4a₀² (equivalently the ½), in a model where a₀² is linear in a density, or a principle that fixes a dimensionless ratio entering exactly there. Not investigated: a larger algebra with a₀ and Λ as two deformation parameters (G); dilaton/scalar sectors of the membrane (J); whether a wall's acceleration is the MOND a₀ at all (J).

## 14. Wave 3 (2026-09-29): eight more lanes, still no derivation (`agents/M,N,Q,R,S,T,U,V`)
Scripts of every lane re-run by me (all exit 0, counts match the agents'). κ = ½ stays FITTED; the open target remains the rational 4 in Gρ_Λ = 4a₀².
| lane | question | verdict | what it leaves |
|---|---|---|---|
| M two-parameter algebra | can Jacobi/central-charge/cohomology fix a₀/H? | no-go | Newton-Hooke admits no a₀ deformation; the only 1/acceleration structure constant (c3 in [K,K] = c3 P) lives on Galilei, parity-odd, Jacobi forces c3/c² = 0; central charges are the mass only; algebra-forced rationals (½, 2:1, N = 4) share one origin, a bilinear bracket, and reach κ only by assumption |
| N Jacobson thermodynamics in dS | does the exact dS Unruh temperature give a crossover? | no-go (scoped) | heat and T carry the same Killing factor, so G_eff = G for every a/H; a crossover needs a hand-inserted mismatch (4 inserted premises); the resulting a₀ is H or 2H (Z or 2Z times the framework's), never 1/Z |
| Q Yang-Mills scale | anomaly, dimensional transmutation, condensate | no-go (scoped) | every scale-carrying 32π² is the one instanton unit; ε_vac = θ/4 (the 1/4 is 1/D); a₀²/(Gρ) has no ħ or YM datum; same-S⁴-instanton self-consistency gives ½ per chirality (1 for the pair) by construction of 1/g² = L²/(16πħG), not 4; the magnitude route is a two-parameter fit |
| R entanglement equilibrium | does the exact finite-ball condition mark an acceleration? | no-go | the Einstein equation holds exactly for a ball of any radius, in every d (180 cases to 1e-30); Λ is an integration constant; ball accelerations are trig × H, decoys hit as often; my brief's ball volume lacked a factor 2 (V = 2πL³(x − sin2x/2)) |
| S quasi-local field energy | Brown-York / field-energy budget principles | no-go (scoped) | the gravitational field-energy density is not covariant (coefficient +1, −1 or −7 by localisation), so ρ_Λ = 32π u_g(a₀) is a Poisson-coefficient statement only; 341 principles declared beforehand, none gives 1/4; every ρ-dependent root carries one π |
| T Weyl/conformal gravity | does the Mannheim-Kazanas invariant tie a₀ to Λ? | no-go | only γ² + 4k = 4κ_h² is conformally invariant, so a₀ (= γ/2) is a gauge parameter and a₀²/k is not invariant; G_eff ρ/a₀² = (3/8π)(1 + k/a₀²) is a free ratio (needs k/a₀² = 32π/3 − 1); the theory's own γ₀c²/2 is 7.8× below SPARC a₀ |
| U RG-improved gravity | does an IR fixed point fix Gρ/a₀²? | no-go (scoped) | Gρ_Λ/a₀² = λ_X ζ²/(8π) with ζ a cutoff-identification constant (ζ = 8√π to 25.6 across schemes); the fixed-point coupling carries ħ (~10⁻¹²²), a₀ does not |
| V evidence for the coefficient | do the data establish 32π? | evidence table | supported: a₀ = cH₀/(6.0 +0.8/−0.7) (ρ_total footing, H₀ = 67.4, a₀ = 1.10e-10 ± 12%); cH_Λ/(4.9 ± 0.6) on the ρ_Λ footing. Bayes factors F:V = 0.97, F:M = 1.06; only κ = 1 (Z = 2.894) is excluded (5.7σ). Ω_Λ prediction 0.906 reproduces; 1.7–2.6σ by estimator; removing it needs a₀ −13%, inside the systematic budget (rescaling SPARC distances by 73/67.4 gives −13.8%); the record's SPARC a₀ = 1.0766e-10 is conditional on its α = 1 kernel (RAR 0.873, simple 0.881, standard 1.117 with the same data); precision needed: 1.8% for 5.789 vs 6 at 2σ, 4.1% vs 2π; best published 8.3% |
**Net after 20 lanes.** Gravity, gauge theory, topology, thermodynamics, symmetry, algebra, quantum-gravity RG, membranes, the MOND offset and Weyl gravity each fail to supply the ½ (or the 4); every route that produces a coefficient inserts it. The data support 'a₀ ≈ cH/6 within ~13%', not '32π' specifically: 5.79, 6 and 2π are not separable until the total error on a₀ is below about 2–4%.

## 15. Wave 4 (2026-09-29): brainstorm lanes, the Sciama relocation, a Lean chain (`agents/W,X1,X2,X3,Y,Z1,Z6,H2` + `p11`)
All scripts re-run by me (exit 0). Still no derivation; κ = ½ stays FITTED.
| lane | question | verdict | what it leaves |
|---|---|---|---|
| W fresh ideas | 18 untried mechanisms, top 5 ranked | nothing new | derivation chance ≤ 2% each; W03 (SdS: κ²/\|P\| = 2π(1−x)²/x) and W11 (k-essence: Gρ/a₀² = c/8π) closed by script |
| X1 one generator | one D-formula behind the 4's? Noether/Euler origin? | no-go (scoped) | 28 rows, 20 verified atoms; the puzzle's 4 is the only factor with no derivation; TT–Euler 1/(64πG) match is a D = 4 accident; Aκ² ≤ π (Kerr-Newman) |
| X2 collective frequencies | Jeans/plasma-type scales of the vacuum | no-go (scoped) | vacuum Jeans frequency is exactly 0 (gravity enters through 1+w); 22-entry declared menu, no hit; my brief's 4πG(ρ+3p) = −Λ, not −2Λ |
| X3 extended thermodynamics + Mach | P = −Λ/8πG enthalpy; Sciama coefficient | no-go (scoped) | every condition gives (rational)×π for a₀²/Gρ; Sciama 2π (3/4 at the Hubble cutoff); the record's M₁ premise maps to a cutoff 2R* |
| Z6 referee of X3 | is the record's memory kernel Sciama's? | TRUE ONLY FOR THE MOMENT | the record's kernel is a free-weight proper-time memory with no G or ρ; cutoff is 2, 8/3, 4/3 or 2/3 × R* by shape, ∝ 1/M₀; long-memory branch violates the ephemeris by ~10¹² |
| `p11` | which horizon cutoff would c²/R_c = a₀? | table (uninformative) | particle-horizon diameter 92.3 Gly gives 0.96 × SPARC a₀ and 6.36 c/H₀ ≈ 2π; an 8% match among ~6 candidates happens ~55% of the time; corrected after Z6 |
| Z1 cutoff laws vs a₀(z) | test each cutoff as an a₀(z) law | discriminating test | particle-horizon law ×6.05 at z = 2.5 (+0.78 dex) vs H(z) ×3.77, ΛCDM-native ×2.16, flat ×1; data neither exclude nor confirm; 0.1 dex at z = 2.5 separates flat from the rest at 3.3–7.8σ, but H(z) vs particle-horizon only 2.1σ; R*/R_p = 1.0995, H₀-independent |
| Y maximal force | does F_max = c⁴/4G, a string or the dS C-metric fix a₀/cH rationally? | no-go (scoped) | 6·F_max is the Friedmann relation as a force; C-metric acceleration parameter is free; only interior fixed point q = 2.448; Z = 6 would mean Λ = 108a₀², Ω_Λ 7.4% higher |
| H2 Lean wave 2-4 | certify the later exact results and the chain | certified | 203 theorems in 9 files, standard axioms, 103 mutation pairs, cross-check 85/85; sixteen forms TFAE with one `OpenPremise`, none a theorem of the definitions (a₀ = H witness falsifies all); correction: at a root of f, κ_b = (1 − 3r²/L²)/(2r), unique root of κ_b = H/Z is (√(1+3Z²) − 1)/(3Z) = 0.5226; in the Bousso-Hawking normalisation no SdS horizon has κ = H/Z (Z ≥ 1) |
**Net.** Twenty-eight lanes now: every route either inserts the coefficient or leaves it as the single open premise; Lean certifies that all sixteen readings are one statement. What can move the case is a₀ at z ≈ 2.5 (flat vs rising) and total error on a₀ below 2–4%.

## 16. Wave 5 (2026-09-30): three structurally new tests (`agents/N1,N2,N3`)
Scripts re-run by me (exit 0, counts match). Nothing derived; κ = ½ stays FITTED.
| lane | question | verdict | what it leaves |
|---|---|---|---|
| N1 algebraic-in-Λ Z | does a π-free vacuum-geometry scale fit the flat-a₀(z) (ρ_Λ) footing better than 32π? | nothing new | only a₀ = GM_N/L² (Z = 3√3 = 5.196) fits, and it pairs the Nariai hole's mass with r = L, a radius outside that geometry's static patch (every radius belonging to the Nariai geometry gives Z = √3, excluded at > 7σ); ρ_Λ footing, ensemble E: N at +0.4σ, 5.789 at +1.3σ (LR 2.1); under the Υ-free RAR/simple kernels N is −2.1σ, 5.789 −0.85σ, 2π +0.15σ (LR N:F = 0.14); no candidate within 2σ under all four kernels; false-match probability for 8 menu values 28%; menu fixed after seeing N fit, so not an independent prediction; Ω_Λ from the record a₀: 0.73 ± 0.08 (N) vs 0.906 ± 0.10 (32π) vs 0.685 observed |
| N2 nonlinear eigenvalue | does the MOND field equation in the dS patch have an existence threshold fixing a₀/H? | no-go | regular global solution for every M and a₀/H in all standard families incl. DBI; only thresholds are cubic-Galileon folds (rational, π-free, a₀ ≥ 4H, a polynomial-coefficient convention; exclude that family, do not select Z); dS attractor exists for every a₀/H; decoys hit 56% |
| N3 MOND cosmology | fixed points of the MOND-modified expansion with Λ | no-go (scoped to the boundary-shell closure) | one fixed point, always a saddle (λ²/H² between 2 and 3), a₀, H, M independent; homogeneous closure gives ν(x*) = 2/f, needs an inserted f = 1.705 for Z = 5.789 (decoys 4.5, 7.3, 8.1 equally reachable); a total-density closure has no fixed point for z > 0.296 |

## 17. The bridge cannot be a local static-horizon statement (`p12`, 7/7)
For a static spherical metric f = 1 − 2Gm(r)/r with energy density ρ(r) (G^t_t = −2m'/r², verified from the Ricci tensor), a horizon f(r_h) = 0 with f-normalised κ = f'(r_h)/2 obeys **1 − 2κr_h = 8πGρ(r_h)r_h²**. Hence: (A) the puzzle's Schwarzschild relation κ = 1/(2r_h) holds iff ρ(r_h) = 0 (the sympy solve over positive ρ returns no solution, i.e. only ρ = 0); (B) r_h²Λ = 8π with constant vacuum density needs κr_h = (1 − 8π)/2 = −12.07, not ½; (C) the ordinary de Sitter horizon (r_h²Λ = 3) has κr_h = −1; (D) so κr_h = ½ and r_h²Λ = 8π cannot hold at one static horizon of one metric. Scope: f-normalised Killing vector (audit H2), static spherical symmetry, GR. What it rules out: a bridge that is a statement about the same horizon's local geometry. What it leaves: a global or nonlocal tie (boundary condition, average, a dynamical/FRW apparent horizon r_A = c/H with Λr_A² = 3), a different gravity theory, or a MOND-sector object with its own horizon. κ = ½ stays FITTED.

## 18. Wave 6 (2026-09-30): the three bridge options after p12 (`agents/B1,B3,B4`)
Scripts re-run by me (exit 0). Nothing derived; κ = ½ stays FITTED.
| lane | option | verdict | what it leaves |
|---|---|---|---|
| B1 global boundary tie | global conditions on {r_s, r_b, r_c, r_N, r_ZF, r_J, r_ES} | sharp no-go | every pair coincidence is algebraic (r²Λ = 1, 3/2 or 3), never 8π; SdS horizons obey r_b²Λ ≤ 1, r_c²Λ ≤ 3, 1 − 2κr = Λr²; horizons exist only for r_s²Λ < 4/9 (the puzzle's 8π is 56× above); the outer boundary only fixes M; κr = ½ holds only in a Λ-free vacuole where r²Λ = 8π is a choice of M = 1.447L = 7.52 M_N (1.6e23 M☉, not a meaningful object, decoy rate 41%); Einstein-Straus is an inequality ρ_m/ρ_Λ ≤ 3/8π, true only after a = 1.57; standard E-S radius 3M/(4πρ_m) has no Λ |
| B3 modified horizon equations | f(R), Horndeski stealth, Rastall, Lovelock, 4D EGB | nothing new + one structural no-go | any theory with an SdS-form static vacuum has exactly 1 − 2κr_h = Λ_e r_h², so (κr_h, Λr_h²) = (½, 8π) is excluded for every coupling; only 4D Glavan-Lin/EGB with α = −(8π/3)r_h² reaches it, with G_eff < 0, a solution ending at 1.24 r_h, and the coupling tied to a₀ by hand (re-inserts the coefficient); the factor 4 is rigid (8π/2π from the first law); Einstein-aether, Horava, AeST, TeVeS, BIMOND and the record's CA5/V0 not computed |
| B4 MOND-sector object | phantom-density radius, zero-force, hydrostatic cap, wall/slab | sharp no-go | every object leaves one free scale; 0/18 phantom roots, 0/18 zero-force roots, 0/3 energy roots within 1% of 1/√(32π) (decoy rate 2.6%); masses with r* = r_M or r_a0/2 are defined by a₀ (tautological); stress cap gives P_c = 3P_Λ for every ρ so ρ_Λ/P_Λ = 32π cannot be an equilibrium output; a φ⁴ kink gives R*/δ = Z² but δ is free |
**Net.** After p12 the 'physical bridge' options are closed as far as the declared principles reach: a local one is impossible (p12), a global one gives only algebraic coincidences (B1), a modified horizon equation re-inserts the coefficient (B3), and a MOND-sector object leaves a free scale (B4).

## 19. Is the "actual" horizon the wrong one? Real LambdaCDM horizons (`p14`, 4/4; MUTATE 3/4, exit 1) -- 2026-10-04
Pure de Sitter gives Lambda A = 12 pi exactly; that is a metric identity, not an error. But our universe is not pure de Sitter, so `p14` puts
its three real horizons (Planck 2018) against 32 pi^2. Needed radius: sqrt(8 pi/Lambda) = 50.4 Gly.
- Hubble (14.4 Gly) and event (16.6 Gly) horizons miss by a factor 9-12.
- **The particle horizon (46.2 Gly) gets within 16%: ratio 0.84, implied a0 = c^2/(2 R_p) = 1.03e-10, between the two footings.**
- But it is not a law of Lambda: R_p grows with time, so this a0 changes with redshift: a0(2.5)/a0(0) = 6.0, steeper than the a0 ~ H(z) rival (3.75),
  and the opposite of FLAT. It is an epoch coincidence (we live when R_p ~ 2.7 R_dS). As a hypothesis it is falsifiable by the same a0(z) data;
  the framework's FLAT law and this one cannot both hold. **kappa = 1/2 stays FITTED.**

## 20. The particle-horizon reading against the a0(z) record (`p15`, 5/5; MUTATE 2/5, exit 1) -- 2026-10-04, POST-HOC
Law PH: a0(z) = c^2/(2 R_p(z)), no free parameter (s* 1.10 today, 2.5 at z 0.8, 6.0 at z 2.3, 16 at z 5.3; always above a0 ~ H(z)).
- **Native (LCDM-free, CFG303) points: PH inside the 95% interval for 1 of 5 (RC100 Q1 only); FLAT 4 of 5, H(z) 2 of 5.**
  RC100 Q2 needs baryons 0.19 dex lower to reach PH; Q3 about 0.30 dex, CRISTAL more than 0.30 dex; Q4 has no root (baryons alone suffice).
- Committed chart points (LCDM-halo inputs where the record says so): PH 6 of 15, FLAT 11, H(z) 11.
- KiDS lens-z halves cannot separate anything (PH +0.7 sigma, FLAT +1.6 sigma). PH sits above the KMOS3D PT1 bound (5.9 vs <= 2.44).
- **Reading:** on the record's own calibration-limited data the particle-horizon law does worse than both FLAT and H(z); it survives only if
  every high-z baryon mass is overestimated by >= 0.2-0.3 dex in the same direction. Not a kill (post-hoc, calibration-limited), but the
  p14 match is best read as an epoch coincidence. The 32 pi^2 remains the fitted kappa = 1/2.

## 21. Why gas- and star-dominated SPARC galaxies want different a0 (`p16`, 3/3; MUTATE shuffles labels, fails A) -- 2026-10-04, diagnostic
Baseline (lane V's cleanest: RAR, Upsilon 0.5/0.7, Q<=2, i>=30): late types 0.856, early types 1.247 (e-10), ratio 1.46 +- 0.05.
- Not distances (TRGB/Cepheid only: 1.63), not inclination (i>=50: 1.53), not inner beam smearing (outer half: 1.47).
- Pressure support helps but does not close it (sigma_HI 10 km/s: 1.23). A gas-mass rescaling would need x0.6 (implausible).
- **A star-class Upsilon_disk of 0.6 (instead of 0.5) closes it (ratio 1.05)**: the one plausible single cause. The common a0 is then ~0.86-0.90e-10.
- At matched acceleration the split survives in the low window (g_bar < 2e-11: 1.37) and closes in the mid window (1.06, only 10 gas galaxies).
Reading: the split is most simply a stellar mass-to-light zero point (0.6 vs 0.5 at 3.6 um, within SPS uncertainty); with it, a0 ~ 0.86-0.90e-10,
8% below the framework's 9.36e-11. Independent-point errors understate the true error. Not a derivation; kappa = 1/2 stays FITTED.

## 22. Try to derive G rho_Lambda r_s^2 = c^2 from standard black-hole/vacuum conditions (`p17`, 2/2; MUTATE fails A) -- 2026-10-04, post-hoc menu
Thirteen conditions solved by sympy for rho r^2 (target 1). **None hits.** Seven independent ones (escape speed, energy inside r, potential, Hubble radius,
equal horizon areas/entropies, tidal fields, BH mean density) all give the SAME value 3/(8 pi) = 0.119, i.e. r_s = c/H_Lambda; the others give 3/(16 pi), 1/(16 pi),
1/(32 pi), 1/(8 pi), 3 pi/32. Every row carries one net power of pi (G enters as 4 pi G / 8 pi G), so none can be the pi-free 1.
Reading: the natural condition is r_s = c/H_Lambda (a0 = cH_Lambda/2, Z = 2, excluded by the data); the puzzle is that condition with H = sqrt(8 pi G rho/3)
replaced by the bare sqrt(G rho), a factor sqrt(8 pi/3) = 2.894 that no standard condition supplies. kappa = 1/2 stays FITTED.

## 23. The same conditions in Heaviside-Lorentz gravity units (`p18`, 2/2; MUTATE corrupts a p17 value, fails B) -- 2026-10-04
With G_H = 4 pi G (Poisson lap Phi = G_H rho), the p17 conditions become pi-free rationals (seven rows: G_H rho r_s^2 = 3/2 c^2; others 3/4, 1/4, 1/8, 1/2)
and the puzzle becomes G_H rho_Lambda r_s^2 = 4 pi c^2: the pi moves to the target. The physical gap target/natural = 8 pi/3 is unit-invariant.
Units relabel; they cannot derive. In these units the open question reads: why a full solid angle 4 pi in place of 3/2. kappa = 1/2 stays FITTED.
(First MUTATE choice changed G_H/G, which cancels in check B by construction and could not fail; replaced.)

## 24. Flux through the horizon (`p19`, 5/5; MUTATE K = 2/r^2 fails A, B, C) -- 2026-10-04
- Gauss-Bonnet on the horizon sphere: oint K dA = 4 pi for every radius (computed from the metric). This is the natural source of a full 4 pi.
- GR's own horizon flux balance (the Hawking-Gibbons-Woolgar area bound): oint Lambda dA <= oint K dA, i.e. Lambda A <= 4 pi, equality exactly at Nariai
  (checked: f = f' = 0 at r = 1/sqrt(Lambda); SdS scan never exceeds 4 pi).
- **The puzzle is the same balance with the vacuum entering as G rho instead of 8 pi G rho:** A Lambda = 32 pi^2 <=> oint G rho_Lambda dA = oint K dA <=> rho r^2 = 1.
  So 32 pi^2 = 8 pi (Einstein) x 4 pi (Gauss-Bonnet of the horizon), and the puzzle's horizon lies 8 pi beyond GR's maximum: no GR horizon satisfies it.
- Newtonian Gauss flux and the Smarr formula reduce to point conditions (3/(16 pi)), as p17.
Reading: the flux form gives the cleanest statement yet -- the vacuum "fills" the horizon's Euler number with coupling G, not 8 pi G -- but supplies no reason for
the coupling G. kappa = 1/2 stays FITTED. (Check B first failed on a 1e-2 tolerance near Nariai, where r_b approaches as sqrt(eps); fixed with the exact Nariai point.)

## 25. Acoustic horizon of the a0 sector (`p20_acoustic_horizon/`, SETUP.md = frozen criteria) -- 2026-10-04, in progress
Setup: QUMOND's auxiliary fields are constrained (FP4/FP5), so they have NO acoustic horizon; branches A (k-essence form of the kernel on a rolling background)
and B (khronon universal horizon). Pass needs kappa = a0 AND Lambda A = 32 pi^2, no tuned parameter, mass-independent radius, subluminal.
- `p20a` (5/5; MUTATE drops the 2 in c_s^2, fails M2/M3): machinery verified (canonical, X^n, DBI). **A1, the cosmological sound horizon, FAILS:** r_h = c_s/H,
  so Lambda r_h^2 = 8 pi needs c_s = sqrt(8 pi/3) = 2.894 c (superluminal), and kappa r_h = c_s or 1 (by normalisation), never 1/2.
- Open: A2 (sonic horizon around a mass: radius scales with M, so criterion 3 is the hurdle), B (khronon universal horizon). kappa = 1/2 stays FITTED.
- `p20b` (5/5; MUTATE u^r = 2Hr fails S1, S3): **branch B, the khronon universal horizon, FAILS.** Test khronon on SdS (core: beta = 0, alpha_c <= 3.2e-9),
  infinite-speed (CMC, K = 3H) foliation matched to cosmic time. Exact: F = f + (u^r)^2 = 1 - 2(M - HC)/r + C^2/r^4 -- Lambda cancels, the foliation sees a
  Schwarzschild hole of mass M_eff. Schwarzschild limit reproduces r_UH = 3M/2, kappa_UH = sqrt(2/27)/M (kappa r = 1/sqrt 6 = 0.408). Over the SdS family up to
  Nariai: kappa_UH r_UH in [0.013, 0.408] (never 1/2), Lambda r_UH^2 <= 0.94 (the UH lies inside r_b), so Lambda r^2 = 8 pi is unreachable.
  Not covered: finite khronon speed (the CMC limit is the framework's small-alpha regime only in that limit), branch A2. kappa = 1/2 stays FITTED.
- `p20c` (6/6; MUTATE drops P_XX in G^rr and flips f, fails 3): **A2 and finite-speed B both FAIL.**
  A2 (sonic horizon around a mass, P = s^n on a rolling background): horizon where the a0-field flow equals c_s; kappa r_h = p sqrt(2n-1)/(2(n-1)) (p = profile slope),
  independent of M; kappa r_h = 1/2 in deep MOND needs a tuned exponent n = 2 + sqrt 2, and Lambda r_h^2 = 8 pi needs the one mass M a0 = 8 pi c_s^2 q^2/Lambda
  (radius ~ sqrt M; q free): INSERTION on both halves. (POST-HOC: the pre-written A2-1 guessed kappa r_h = 1/2 for all n; the run refuted it; replaced by the formula.)
  B at ANY khronon speed: a universal horizon needs d_t spacelike (f < 0); on the black-hole side Lambda r^2 <= 0.997 < 1 for every SdS mass, and beyond r_c a khronon
  matched to cosmic time has u.chi = -1. Lambda r^2 = 8 pi is unreachable whatever the speed.
**Branch verdicts (p20): A1 FAIL, A2 INSERTION, B FAIL (CMC and any finite speed).** No effective-metric horizon of the a0 sector gives the puzzle. kappa = 1/2 stays FITTED.

## 26. BIMOND (Milgrom 2009, arXiv:0912.0790v2, PDF read; sha256 067e8560...) (`p21`, 3/3; MUTATE halves the RAR integrand, fails B) -- 2026-10-04
Vacuum term eq (24) at kappa = 1: Lambda = -(1/2)(1 + f'(1)) a0^2 M(0); NR limit eq (3): M'(z) = nu(sqrt z) - 1. With M(inf) = 0, M(0) = -int 2y(nu - 1)dy < 0, so
BIMOND gives Lambda > 0 and rho_DE proportional to a0^2 automatically -- the framework's STRUCTURE (a0 ~ sqrt(rho_DE)). The coefficient:
- framework kernel nu = sqrt(1 + 1/y): the integral DIVERGES linearly; 32 pi needs a strong-field cutoff at g_N = 203 a0 (free).
- RAR kernel: finite, 25.976 (= lane K's AQUAL c), so Lambda = 12.99 a0^2 with the minimal f = 1: 7.74x short; 32 pi needs f'(1) = 6.74 (f is free beyond f(1) = 1).
Verdict: BIMOND reproduces the form rho_DE ~ a0^2 with the right sign but INSERTS the coefficient. kappa = 1/2 stays FITTED.

## 27. Minimal BIMOND (f = 1) with a sharpened tail: which tail gives 32 pi? (`p22`, 5/5; MUTATE doubles the tail coefficient, fails T) -- 2026-10-04
The record keeps nu = sqrt(1+1/y) exactly (alpha = 1, planets handled by the spatial filter, FP1/FP7); the exact law forces that tail. A one-parameter family that
contains it, nu_a = (1 + y^-a)^(1/(2a)), and Milgrom's nu_n were scanned (SPARC cannot tell tails apart: <= 0.0084 dex). I_nu is finite only for tail exponent > 2,
and behaves as ~1/(a(a-2)) near the edge (checked: (a* - 2) 64 pi a* = 1.002).
- **Lambda = 32 pi a0^2 needs alpha* = 2.0025 (F1) or n* = 2.0050 (F2): a tail tuned to within 0.25-0.5% of the divergence, and a different exponent per family.**
- Every steep (ephemeris-comfortable) tail gives Lambda/a0^2 ~ 0.2-5, i.e. 20-500x short; RAR's exponential tail gives 13 (p21).
Verdict: minimal BIMOND makes 32 pi a near-divergent fine tuning of an unmeasured tail. Not a derivation. kappa = 1/2 stays FITTED.
(Numerics: nu - 1 computed with expm1/log1p after floating-point cancellation zeroed the 1e6-1e7 decade in the first brute-force check; the first MUTATE could not fail; both replaced.)

## 28. Horizons of BIMOND's auxiliary metric g-hat (the a0 sector's own metric) (`p23`, 3/3; MUTATE removes the sector sign difference, fails A) -- 2026-10-04
From Milgrom 2009 eq (24): Lambda = -(1/2)(1 + f'(1)) a0^2 M(0), Lambdahat = -(1/2)(f'(1) - 1) a0^2 M(0). A g-hat horizon with kappa r = 1/2 needs Lambdahat = 0, i.e. f'(1) = 1.
- One structural gain: then g-hat is Lambda-free, so the puzzle's Schwarzschild hole (kappa = a0, A = pi/a0^2) EXISTS there as an exact solution, unlike in our de Sitter
  metric where it is 8 pi past the Nariai bound (p06, p19).
- But nothing selects that hole: requiring kappa = a0 and Lambda r^2 = 8 pi on one hole IS Lambda = 32 pi a0^2 (restatement), and with f'(1) = 1, Lambda = a0^2 I_nu,
  so 32 pi needs I_nu = 32 pi -- the p22 tail tuning. Not a derivation. kappa = 1/2 stays FITTED.

## 29. What pins f'(1) in BIMOND? (`p24`, 3/3; MUTATE drops lambda^-2 in qhat, fails 2) -- 2026-10-04
Milgrom eqs (84)-(85): with g-hat = lambda g the vacuum must satisfy both field equations, q/beta = qhat/alpha.
1. Milgrom's main class (alpha + beta = 0, the clean QUMOND limit): a g-hat = g de Sitter vacuum is inconsistent for EVERY f'(1) unless M(0) = 0 -- the a0^2 vacuum
   term needs lambda != 1 or twin matter. Nothing pinned.
2. Ghost-free (determinant-only) potential f = A kappa + B/kappa: the vacuum gives f'(1) = (lambda+1)/(lambda-1), Lambda = lambda/(lambda-1) a0^2 I_nu: f'(1) traded for
   the free cosmological scale ratio lambda.
3. alpha = beta with g <-> g-hat exchange symmetry: f(kappa) = f(1/kappa) PINS f'(1) = 0, and the g-hat = g vacuum is consistent, Lambda = (1/2) a0^2 I_nu. So symmetry does pin
   f'(1) -- but then 32 pi needs I_nu = 64 pi, the p22 tail tuning; and this class lacks Milgrom's clean NR limit (its nu <-> M' map not derived here).
Verdict: f'(1) can be pinned (exchange symmetry), but pinning it moves the whole coefficient into the unmeasured kernel tail. kappa = 1/2 stays FITTED.

## 30. The nu <-> M' map for exchange-symmetric BIMOND (alpha = beta = 1) and its vacuum (`p25`, 6/6; MUTATE uses the main-class map, fails ID) -- 2026-10-05
Derived by varying Milgrom's NR Lagrangian (eq 1) with sympy: alpha phihat' = -M' phi*', mu* = beta - (alpha+beta)M'/alpha, g = (1 - M'/alpha) g* (his eq 2).
For alpha = beta = 1: **M'(z) = (nu - 1)/(2nu - 1) at z = [y(2nu - 1)]^2** (main class: M' = nu - 1 at z = y^2).
**Exact identity:** J - I_nu = int d[2 y^2 (nu - 1)^2], a boundary term that vanishes, so the vacuum integral is the SAME in both classes. Lambda/a0^2 = (1/2) int (nu-1) d(y^2)
depends on the force law nu alone, not on how BIMOND is set up. Consequences: framework kernel diverges in both; RAR gives 12.99 a0^2 (x7.74 short); 32 pi needs the same tail
alpha* = 2.00249. A class-independent, kernel-only statement of the coefficient -- still not a derivation. kappa = 1/2 stays FITTED.

## 31. What could pin the strong-field tail of nu (`p26`, 5/5; MUTATE corrupts the Planck acceleration, fails C1) -- 2026-10-05
- **Data:** no. The tuned tail (alpha* = 2.0025) gives 3.5e-19 m/s^2 at the Earth, 3e4 below ephemeris sensitivity; SPARC stops at y ~ 1e2. Worse, the tuned value is collected
  out to y ~ e^400 ~ 5e173 (accelerations 1e164 m/s^2), far beyond the Planck acceleration (y_P ~ 6e61): unphysical as stated.
- **Theory:** Milgrom 1999 (the framework's kernel) is the one derivation that fixes the tail, and its integral diverges; 64 pi needs a cutoff at 203 a0, a scale with no marker.
- **A physical cutoff:** with the 'standard' mu tail (nu - 1 ~ 1/(2y^2)), I_nu = ln y_max + 0.193. Cut at the Planck acceleration: Lambda/a0^2 = 71.2 (both footings),
  1.41x short of 32 pi; the 10^61 of the cosmological-constant problem enters only as a logarithm, so the ORDER is natural. Reaching 32 pi needs y_max = 1.7e87, 3e25 x past Planck.
  This is a menu result (kernel and cutoff chosen) and it puts hbar into a0 logarithmically, against lane A. The ratio 0.708 is not read as 1/sqrt 2 (post-hoc menu).
Verdict: nothing pins the tail; the closest natural construction (standard tail + Planck cutoff) gives the right order but not 32 pi. kappa = 1/2 stays FITTED.

## 32. Planck cutoff with the framework kernel (`p27`, 2/2; MUTATE uses an alpha = 2 kernel, fails both) -- 2026-10-05
Exact: int_0^Y 2y(sqrt(1+1/y) - 1) dy = [2Y^(5/2) + 3Y^(3/2) + sqrt Y - sqrt(Y+1)(2Y^2 + asinh sqrt Y)]/(2 sqrt(Y+1)) ~ Y (evaluated at 200 digits: the closed form cancels Y^2 terms).
Cut at the Planck acceleration: Lambda = (1/2) a0 a_P/c^4, the geometric mean of a0 and the Planck acceleration: **3e59 x too large** (both footings). The slow alpha = 1 tail
makes the vacuum term track the cutoff linearly, so the framework kernel turns BIMOND's vacuum into the cosmological-constant problem (softened from 1e122 to 1e59).
kappa = 1/2 stays FITTED.

## 33. Planck cutoff with the steeper-tail families (`p28`, 4/4; MUTATE doubles F1's tail coefficient, fails T, B) -- 2026-10-05
Cut at a_P (ln(a_P/a0) = 142.2): at tail exponent exactly 2, Lambda/a0^2 = 35.7 (F1, the family containing the framework kernel) and 71.2 (F2 = standard mu).
**32 pi needs F1 a* = 1.98735, F2 n* = 1.99543** (alt footing 1.98732 / 1.99540): a tail falling slightly SLOWER than 1/y^2, different per family, invisible to planets
(4.7e-19 m/s^2 at the Earth) and to SPARC. Not a natural value; a fit. (POST-HOC: check A's band was pre-written as 1.99 < a* < 2; F1 gave 1.98735; widened to 1.98.)
kappa = 1/2 stays FITTED.

## 34. Tail exponent exactly 2 with different cutoffs (`p29`, 3/3; MUTATE halves the standard amplitude, fails C) -- 2026-10-05
nu - 1 ~ A/y^2 makes the vacuum log-divergent: Lambda/a0^2 = A ln(a_cut/a0) + const. Cutoffs a_cut = E c/hbar:
electron 22.9 / 45.5, proton 24.8 / 49.2, electroweak 26.1 / 52.0, GUT 34.1 / 68.0, Planck 35.8 / 71.2 (F1 a=2 / standard), target 100.5.
No physical cutoff reaches 32 pi: the standard kernel needs a_cut = 1.6e77 m/s^2 (2.9e25 x Planck), F1 needs 3.5e112 x Planck. At the Planck cutoff exponent 2 needs tail
amplitude A = 0.706 (standard 1/2, F1 1/4). The log makes the order natural (20-70 for any cutoff from the electron to Planck) but never 100.5. kappa = 1/2 stays FITTED.

## 35. Tail amplitude 1/sqrt 2 (exponent 2) with the Planck cutoff (`p30`, 5/5; MUTATE amplitude 1/2, fails A) -- 2026-10-05, POST-HOC
The amplitude was suggested by p29's SOLVED value 0.706. Three kernels with the deep-MOND limit and tail (1/sqrt 2)/y^2: Lambda/a0^2 = 100.41 / 100.53 / 100.47 vs 32 pi = 100.53
on the framework footing (K2 hits to 0.002%); the transition shape moves it by 0.3%.
**But this matches only where a0 is DEFINED from Lambda.** Against measured a0 (the observed ratio is 32 pi (9.36e-11/a0)^2): predicted ~100.4 vs observed 76 +- 8 (record SPARC,
+3.0 sigma), 73 +- 18 (lane V ensemble, +1.5), 61 +- 25 (MLS16, +1.6), 80 +- 19 (MIGHTEE, +1.1). The log makes the prediction insensitive to a0, so the test is really
'is Lambda/a0^2 ~ 100?', and measured a0 values say ~60-80. (The 'alt footing within 0.25%' line in check A compares against 32 pi, which is not the observed ratio there;
the honest comparison is check D, added after the first run.) Rough look-elsewhere for the amplitude: ~50% given the choices (cutoff, normalisation, 14 nice numbers).
Verdict: a striking-looking post-hoc match on the self-defined footing; 1-3 sigma high against measured a0; not significant. kappa = 1/2 stays FITTED.

## 36. Amplitude 1/sqrt 2 with the GUT cutoff (`p31`, 2/2; MUTATE uses Planck, fails A) -- 2026-10-05, POST-HOC
a_cut = (2e16 GeV) c/hbar = 9.1e48 m/s^2. Framework footing: Lambda/a0^2 = 95.9-96.0 (K1-K3), 4.5% short of 32 pi (ln(a_GUT/a_P) = -6.4, x 1/sqrt 2).
Against measured a0: predicted ~95.9 vs observed 76 +- 8 (+2.4 sigma), 73 +- 18 (+1.3), 80 +- 19 (+0.8). Closer to the data than Planck, still high, not a match. kappa = 1/2 stays FITTED.

## 37. Amplitude 1/sqrt 2, all five cutoffs (`p32`, 2/2; MUTATE amplitude 1/2, fails A) -- 2026-10-05, POST-HOC SWEEP
| cutoff | framework footing (vs 32 pi) | vs measured a0: SPARC record / lane V ensemble / MIGHTEE (pull) |
|---|---|---|
| electron | 64.1 (-36%) | -1.45 / -0.52 / -0.83 |
| proton | 69.4 (-31%) | -0.81 / -0.22 / -0.55 |
| electroweak | 73.4 (-27%) | -0.33 / +0.00 / -0.35 |
| GUT | 96.0 (-4.5%) | +2.41 / +1.27 / +0.84 |
| Planck | 100.5 (-0.0%) | +2.96 / +1.52 / +1.07 |
The framework footing (a0 defined from Lambda) prefers Planck; measured a0 prefer electron-to-electroweak (the electroweak row's 0.00 against the ensemble is a sweep pick).
Three of five cutoffs fit the measured ratios within 1.5 sigma: the data cannot choose a cutoff, and a sweep that finds a match is a menu pick. kappa = 1/2 stays FITTED.

## 38. Lean certification of the 2026-10-04/05 chain (`fable_independent_2026/lean_2026/PUZZLE_32pi_chain_2026_10_05.lean`) -- 2026-10-05
Ten theorems, repo Mathlib pin, `#print axioms` = [propext, Classical.choice, Quot.sound] for each; no `axiom` declarations; premises are named hypotheses.
sds_horizon_identity + no_sds_horizon_is_puzzle (no f-normalised SdS-type horizon has kappa r = 1/2 and Lambda r^2 = 8 pi); escape_condition_value (3/(8 pi) < 1);
heaviside_form; flux_form (Lambda A = 32 pi^2 <-> the horizon Gauss-Bonnet balance with G rho); acoustic_ds_superluminal (c_s^2 = 8 pi/3 > 1);
bimond_vacuum_condition ((1 + f'(1)) I = 64 pi); exchange_symmetry_pins_fprime (f(k) = f(1/k) -> f'(1) = 0, via HasDerivAt); symmetric_map; class_identity_integrand.
MUTATE copy (Lambda r^2 = 0 in place of 8 pi, 32 pi in place of 64 pi, a wrong map): exit 1, 5 errors, as required.
Certifies premises => conclusions only. The open premise is unchanged: kappa = 1/2 stays FITTED.

## 39. Field-energy-additive Verlinde gives the framework law outside matter (`p33`, 3/3; MUTATE uses Verlinde's mass additivity, fails P and X) -- 2026-10-05
Verlinde's elastic response (1611.02269, CFG117 form) M_D^2 = (a_V r^2/G) d(M_B r)/dr gives exactly g_D^2 = a_V (g_N + 4 pi G rho_B r). Verlinde ADDS MASSES (g = g_N + g_D: wrong shape).
**Adding FIELD ENERGIES instead (g^2 = g_N^2 + g_D^2) gives g^2 = g_N^2 + a_V g_N -- the framework law -- exactly for a point mass at every radius, and to 2.5e-4 beyond
15 scale lengths of exponential spheres**, with a_V = c H_Lambda/6 = 0.965 x the framework's a0 (Z = 6 vs 5.789; ratio 1.036, inside the 12% a0 systematic).
Inside the matter the local term 4 pi G rho_B r raises g by up to x2 at x = 0.1 (x1.2-2.0 by mass): a prediction that differs from the framework's local law and is testable on
SPARC (the RAR's tightness, 0.1 dex, is the obvious threat). This is a MECHANISM for the shape (quadrature = energy additivity of an elastic dark field) with Verlinde's
coefficient, not a derivation of kappa = 1/2: it gives a0 = c H/6, so Lambda A = 108 pi (not 32 pi^2). kappa = 1/2 stays FITTED.

## 40. SPARC test of field-energy-additive Verlinde (`p34`, 2/2; MUTATE sets s = -2, models coincide, verdict check fails) -- 2026-10-05
Model energy-V: g^2 = g_N^2 + a g_N (3 + s), s = dln g_N/dln r (spherical-equivalent local term; = framework where s = -2). Lane V machinery.
- Upsilon fixed 0.5, MLS16 cuts (153 galaxies): chi2 framework 4597.0 vs energy-V 5985.6, **Delta chi2 = +1389** (~+77 after lane V's crude x18 clustering deflation).
- Upsilon free (175): 3140.4 vs 5356.7, **Delta chi2 = +2216** (~+123). Energy-V's best a drops to 0.6-0.8e-10 to compensate.
- Framework residuals vs log10(3 + s): r = -0.13 (energy-V predicts a positive trend).
**Verdict: SPARC rules out the local-density term; field-energy-additive Verlinde FAILS inside galaxies.** The framework's purely local law g(g_N) is strongly preferred.
The p33 mechanism survives only as an exterior statement. kappa = 1/2 stays FITTED.

## 41. The kernel-tail fix (`p35`, 4/4; MUTATE k = 0 = the exact law, fails P, V, W) -- 2026-10-05
nu_fix(y) = 1 + (sqrt(1+1/y) - 1)/(1 + (y/y_t)^2): the framework law below y_t, nu - 1 ~ y^-3 above.
- **SPARC:** indistinguishable from the exact law for y_t >= 100 (|Delta chi2| <= 1.06 on ~3000 points, both Upsilon treatments).
- **Planets (record's bare bounds, no EFE credit):** all pass for y_t <= 7.7e5 (Mars binds; Earth 1.8e6); at y_t = 128 the worst planet is 2.8e-8 of its bound.
  The 1279x Earth liability of the exact law is gone.
- **Vacuum:** QUMOND/BIMOND's vacuum integral becomes finite: Lambda/a0^2 = 77.9 / 99.8 / 784 at y_t = 100 / 128 / 1000 (leading order (pi/4) y_t).
- **If** the a0 sector's vacuum is the dark energy (an input, lane K), 32 pi needs y_t = 128.9 (1.21e-8 m/s^2) for this k = 2 shape -- inside both windows; k = 3, 4 give
  167.5, 182.4. So the turn-off scale is shape-dependent; y_t is a free parameter in [~100, 7.7e5] unless that input is adopted.
Verdict: the tail is FIXED (planets pass, vacuum finite, galaxies unchanged) at the cost of one new constant y_t. It does not derive kappa = 1/2.

## 42. SPARC fit of the turn-off y_t (`p36`, 3/3; MUTATE puts the turn-off in the deep regime, fails A-C) -- 2026-10-05
Profile over (a0, y_t) for nu_fix (k = 2). The offset reading's signature is tiny: y_t = 100 changes log g by -0.0002 / -0.0006 / -0.0011 dex at y = 10 / 30 / 100.
- MLS16 cuts, Upsilon 0.5 (153): no preference; Delta chi2 < 4 for y_t >= 20; y_t = 94 / 128: +0.08 / +0.04.
- Upsilon free (175): best y_t = 5, Delta chi2 = -53 (~ -3 after lane V's crude x18 deflation); y_t = 94 / 128: -1.19 / -0.67. Bulge-bearing (32): best 5, -14.4.
  Reading: the y_t ~ 5 preference is the known preference for a SHARPER TRANSITION than the alpha = 1 kernel (lane V: RAR shape preferred by d chi2 168), not a
  detection of a strong-field turn-off; it vanishes at fixed Upsilon.
**Verdict: SPARC bounds y_t from below (>= 2-20 by treatment) and cannot see the offset reading's y_t ~ 94-129. Allowed, not detected.** Testing it needs data at
10 <~ y <~ 1e3 with ~0.001 dex precision on g -- not available. kappa = 1/2 stays FITTED.

## 43. The transition shape on SPARC (`p37`, `p37b`, `p37c`) -- 2026-10-05
- **p37 (pre-written checks FAILED, 1/4, kept):** in nu_n = (1 + y^-n)^(1/(2n)) (n = 1 the framework kernel) the data do NOT want a sharper transition; at Upsilon 0.5
  they want n ~ 0.7 (a LARGER boost at y ~ 1: nu(1) = 2^(1/(2n)), RAR-like), Delta chi2 -61 (Upsilon free) / -121 (fixed 0.5); gas-dominated galaxies barely care (-1.5).
  RAR beats n = 1 by 168 / 141 / 11.
- **p37b (post hoc, 2/2):** the preference is mostly the stellar mass-to-light zero point: RAR's advantage falls 141 -> 51 -> 12 for Upsilon_disk 0.5 -> 0.6 -> 0.7, and the
  best n moves 0.7 -> 1.0 -> 1.25.
- **p37c (fine scan, 1/3; pre-written K and G FAILED, kept):** chi2 is minimal at Upsilon_disk = 0.56 (4499.9; 0.58: 4504.1), where a0(n = 1) = 1.248e-10, the best n = 0.85,
  RAR is still better by 80 (~4 after crude x18 deflation), and the gas/star split stays open (1.43 +- 0.04). The framework kernel is the best family member only at
  Upsilon 0.58-0.60 (a0 1.20-1.15e-10). The kernel shape and Upsilon are degenerate; SPARC alone does not separate them.
Reading: the transition-shape signal is largely Upsilon, not a clean verdict on the kernel; at the data's preferred Upsilon the RAR shape still edges the framework's. kappa = 1/2 stays FITTED.

## 44. Lean: the leftover postulate r* = c/sqrt(G rho_Lambda) is INDEPENDENT of the ingredients (`fable_independent_2026/lean_2026/PUZZLE_32pi_postulate_status_2026_10_05.lean`)
Premises as a structure: Lambda = 8 pi G rho/c^2; a0 = c^2/(2r) (Schwarzschild surface gravity); BIMOND vacuum Lambda = (1/2)(1+f'(1)) a0^2 I/c^4 (any fp > -1, I > 0).
Proved (standard axioms only): postulate_iff_kappa_half (P <-> a0^2 = G rho c^2/4); a model with all premises AND P; a model with all premises and NOT P; hence
**postulate_independent**: P is neither implied nor excluded; scale_family: every kappa > 0 has a model. The premises carry a free modulus kappa; only a NEW premise that
breaks the kappa-family (fixes I, f'(1) or the tail) can derive P. MUTATE (the not-P model's radius changed so the horizon premise fails): exit 1.

## 45. Can high-acceleration data see PAPER42's turn-off? (`p38`, 2/2; MUTATE y_t = 1 flips both) -- 2026-10-05
ATLAS3D early types (187 with JAM quality >= 1; y = g_N(r_1/2)/a0: median 4.2, 90th percentile 9.8, max 38): the turn-off at y_t = 94 (71-117) shifts the predicted
dynamical mass by a median -0.00009 dex (max 0.0008); the sample mean -0.0001 dex is 60x below its statistical reach (0.007) and ~900x below the 0.10 dex IMF floor.
SLACS lenses (y ~ 5-20 at the Einstein radius): -0.0001 to -0.0005 dex. **Undetectable.** Structural reason: at y ~ y_t the MOND boost itself is nu - 1 ~ 1/(2 y_t) ~ 0.5%,
so no galaxy-scale probe can see more than ~0.002 dex of it; the Solar System (y ~ 1e7-1e8) sees only that SOME turn-off exists (y_t <= 7.7e5). The 'measure g_t,
predict Lambda' route is closed for foreseeable data. kappa = 1/2 stays FITTED.

## 46. Classical UV completion of the MOND field (`p39`, 2/2; MUTATE halves the requirement, fails R) -- 2026-10-05
Dimensional fact: G, c, a0 form no dimensionless number, so a classical parameter-free completion can only fix Lambda c^4/a0^2 = I/2 as a pure number set by its kernel
(with hbar, a0/a_Planck ~ 1e-62 enters and gives the log / 1e59 results of p26-p29). Required I = 146.4 (measured a0) to 201.1 (kappa = 1/2 footing).
Catalog: framework, simple, standard: infinite; RAR 25.98 (Lambda c^4/a0^2 = 13.0); Milgrom nu_n n = 2.5/3/4/6: 1.90/1.00/0.60/0.43. **Every principled kernel with a finite
vacuum term falls short by x5.6-7.7 or more.** The requirement is equivalent to the framework kernel's 1/(2y) tail persisting unchanged to y_t = 94-129 and then stopping;
RAR's tail behaves like a cut at y ~ 17. So a completion that predicts Lambda must explain why the quadrature law's slow tail survives to ~100 a0 and no further.
No known kernel does. kappa = 1/2 stays FITTED.

## 47. Capacity principle and 'nice' turn-off numbers (`p40`, 2/2; MUTATE a0 error 1%, fails N) -- 2026-10-05
(S) 'The MOND field's extra energy a0 g_N/(8 pi G) saturates at the vacuum energy' (y_t = s L) combined with the vacuum condition: no solution for s = 1, 1.2, 4/pi, 2
(L(y_t) ~ 0.78 y_t never meets y_t/s), one tiny solution (L = 3.2) at s = 1.4. The principle does not fix L. 
(N) If y_t is a pure number N: of 20 declared simple numbers in [30, 400], FIVE (8 pi^2, 25 pi, 100, 32 pi, 36 pi) predict a0 within 1 sigma of the measured ensemble
(1.097e-10 +- 12%); y_t = 32 pi gives a0 = 1.061e-10 (pull -0.27). A one-in-four menu hit rate: no single 'nice' turn-off is evidence. kappa = 1/2 stays FITTED.

## 48. Pinning the mass-to-light ratio (`p41`, `p41b`; pre-written checks FAILED in both, kept) -- 2026-10-05
- **p41 (0/2):** galaxy-level 'gas-dominated' samples (last-point gas fraction > 0.6) are NOT Upsilon-insensitive (a0 spread 63% over Upsilon 0.3-0.7): their inner regions
  are star-dominated and a0 ~ g_obs^2/g_bar in the MOND regime. Calibrated Upsilon* = 0.65 (0.56-0.72), a0(all) = 1.055e-10 +- 16%: too loose to decide anything.
- **p41b (0/2; MUTATE fcut = 0 spread 138%, fails G):** calibrating on POINTS where gas supplies > 80% of g_bar (124 points, 19 galaxies): spread 11.2% over Upsilon 0.3-0.7
  (> 0.9: 5.7%, only 5 galaxies; > 0.7: 17%). **Upsilon-insensitive a0 = 9.00e-11 +- 11% (stat), framework kernel**: -3.9% from the kappa = 1/2 footing 9.36e-11,
  -20.5% from the alt footing, -15.2% from p40's 32 pi turn-off value 1.061e-10. RAR kernel: 7.60e-11 (kernel systematic 15.6%). Matching the star-dominated points
  needs Upsilon* = 0.73 (0.66-0.77), ABOVE the 3.6 um population prior (0.40-0.63) -- the star/gas tension persists as either a heavier M/L or a kernel effect.
Reading: the cleanest Upsilon-free measurement in SPARC sits on the kappa = 1/2 footing (as the July population-split note found, 9.8e-11 there), but at 11% stat +
16% kernel it cannot decide between footings or 'nice' turn-off numbers. kappa = 1/2 stays FITTED.

## 49. Kernel preference on the Upsilon-free gas points (`p42`, 2/2; MUTATE fcut 0 fails both) -- 2026-10-05
The 124 gas-dominated points (19 galaxies) are all deep-MOND (y = 0.015-0.066), so they test the kernel's next-order term, Upsilon-independently (same verdict at 0.3/0.5/0.7).
RAR is disfavoured by Delta chi2 = +5.0 to +5.4 vs the framework kernel; within nu_n the allowed range is n = 0.9-1.6 (best 1.6, -1.9: not significant); n = 1 inside.
a0 across the allowed kernels: 8.82 (n 0.9), 9.00 (n 1), 9.24 (1.3), 9.31e-11 (1.6) -> **a0 = (9.0 +- 0.25 kernel) e-11, +- 11% stat**, i.e. the kernel systematic on
the gas points shrinks from 16% (RAR included) to ~3% once RAR's next-order term is disfavoured. Still 19 galaxies; clustering not deflated. kappa = 1/2 stays FITTED.

## 50. Sample-size theorem and Bayes factors from the Upsilon-free gas points (`p44`, 3/4; pre-written N check FAILED, kept; MUTATE data 1.13e-10 fails B) -- 2026-10-05
(1) Per-galaxy a0 on SPARC's gas points (19 galaxies): scatter s = 0.60 in ln a0 (robust 0.51); N = (z s/Delta)^2. vs the kappa = 1/2 rho_Lambda value: alt footing N = 41 (2 sigma)
/ 92 (3 sigma); 32 pi turn-off 93 / 210; Milgrom 2pi (rho_total) 127 / 286, (rho_Lambda) 217 / 489; Verlinde 6 (rho_Lambda) 1137 / 2558. The pre-written check 'every
rival needs > 100 at 3 sigma' FAILED (alt needs 92). **The binding limit is the shared systematic floor (kernel 3% + distance 8.5% = 9%): at 2 sigma only the alt footing is
separable at any N; everything closer needs distances better than ~5%.**
(3) Data a0 = 9.00e-11, sigma_ln 0.142 (stat 0.11 + floor 0.09). Pulls: Verlinde 6 rho_L -0.03, kappa = 1/2 rho_L -0.28, Milgrom 2pi rho_L +0.30 (BF ~1 among them);
Milgrom 2pi rho_tot -1.03 (BF 1.6), 32 pi turn-off -1.16 (1.9), Verlinde 6 rho_tot -1.36 (2.4), kappa = 1/2 rho_tot (alt) -1.61 (BF 3.5).
**The Upsilon-free data favour the rho_Lambda FOOTING (a0 tied to dark energy, not total density) by BF ~2-3.5, but cannot tell kappa = 1/2 from Verlinde's 6 or Milgrom's 2pi
on that footing.** kappa = 1/2 stays FITTED.

## 51. Closed form for the MOND field's vacuum term (`p45`, 4/4; MUTATE constant 1/16 -> 1/8 fails N, P, R) -- 2026-10-05
For the framework kernel with the k = 2 turn-off: **Lambda c^4/a0^2 = (pi/4) y_t - (1/8) ln(4 y_t) + 1/16 + O(1/y_t)**.
Derivation: 2y(sqrt(1+1/y) - 1) = 1 - h, int_0^Y h dy = (1/4) ln(4Y) - 1/8 exactly at large Y (sympy); the Lorentzian gives pi y_t/2 and converts ln Y to ln y_t.
Matches the exact integral to 1e-3 at y_t = 100-128 and 1e-5 at 1e4; reproduces p35's 77.85 / 99.81 / 784.4. Each term has a source: pi/4 from the turn-off's shape,
-(1/8) ln(4 y_t) from the exact law's a0/2 tail (h ~ 1/(4y)), +1/16 from the kernel's interior. Corollary on the kappa = 1/2 footing:
**y_t = 128 + (ln(4 y_t) - 1/2)/(2 pi) = 128.91** (numeric root 128.92): '128 = 4 x 32' plus a logarithmic correction from the law's own tail. kappa = 1/2 stays FITTED.

## 52. WALLABY DR2 gas points (`p43`, 3/3; MUTATE gas x2 fails W) -- 2026-10-05
Data: WALLABY DR2 kinematic models (CADC, 303 models / 236 galaxies; fetch log data_assembly/wallaby_dr2/), AllWISE W1 (IRSA; 229/236 matched after two failed
fetch versions -- v1 ADQL DISTANCE() error, v2 invalid column ba_2mass, both silently empty; v3 now aborts on < 50% matches). Thin-disc gas by ring summation
(Freeman control 0.9%); stars: W1, Upsilon_W1 0.6, exponential disc. QFlag 0, i >= 30, flux scale corrected to log_m_hi_corr. Gas points (> 80% of g_bar): 218 in 46 galaxies, y ~ 0.04.
- **a0 = 7.28e-11 +- 23% (stat)** (H0 73 Hubble distances): -19% from SPARC's gas points (9.00e-11; agrees within the combined 26%), -22% from the kappa = 1/2 footing.
- Upsilon 0.3/0.9: 7.59 / 7.00 (8% spread: Upsilon-free as intended). R_d x0.5 / x2: 8.13 / 6.79.
- **Data-collector assumptions:** framework EFE cubic with per-galaxy g_ext: +1% (noclu) / +8.5% (maxclu); flux scale uncorrected: 8.35 (+15%); asymmetric drift 8 km/s:
  7.68 (+5%); **CMB-frame distances (median 9% larger, up to 21%): 4.88e-11 (-33%)**; near a cluster/group (< 15 Mpc 3D, 27 galaxies) 8.91 vs field (19) 5.63.
Reading: WALLABY confirms the gas-point a0 is low (7-9e-11, below the alt footing) but cannot pin it: its Hubble-flow distances move a0 by ~33% for a ~10% distance
change (a0 ~ D^-3 to -4 in the deep regime with gas-dominated baryons), the dominant systematic exactly as p44 predicted. A precise a0 from WALLABY needs redshift-independent
distances. kappa = 1/2 stays FITTED.

## 53. Gas points by distance method (`p46`, 2/2; MUTATE TRGB distances x0.8 -> a0 rises, check D fails; a first x1.1 control could not fail and was replaced) -- 2026-10-05 -- REVISES the p41b/p44 reading
SPARC's Upsilon-free gas points split by f_D: **TRGB/Cepheid (8 galaxies: D631-7, DDO154, ESO444-G084, NGC3109, NGC3741, UGC04483, UGCA442, UGCA444; e_D/D median 5%):
a0 = 1.158e-10 +- 20%**; Hubble flow (11 galaxies): 6.97e-11 +- 18%; all (19): 9.00e-11. The 9.0e-11 of p41b/p44 was an average of a high redshift-independent set
and a low Hubble-flow set (ratio 1.66, ~2 sigma).
On the TRGB/Cepheid set: alt footing (rho_crit, the ORIGINAL a0 = c sqrt(G rho_c)/2) +2.4% (0.1 sigma); 32 pi turn-off +9%; kappa = 1/2 rho_Lambda +24% (1.1 sigma);
Verlinde 6 rho_L +28%; Milgrom 2pi rho_L +34% (1.5 sigma). **p44's 'data favour the rho_Lambda footing' rested on the mixed sample; the best-distance subset leans the
other way.** 8 galaxies at 20% cannot decide; WALLABY (p43, all Hubble flow) is in the low group, consistent with a Hubble-flow distance bias. kappa = 1/2 stays FITTED.

## 54. LITTLE THINGS (Oh+2015) a0 (`p47`, 1/2; pre-written overlap check FAILED, kept; MUTATE no DM subtraction fails A) -- 2026-10-05
VizieR J/AJ/149/180 (fetch: first attempt saved 404 pages for un-gzipped names, discarded; .gz versions match the ReadMe row counts). Baryons = V_tot^2 - V_DM^2 with the
AUTHORS' stellar M/L (not Upsilon-free); distances Hunter+2012 (mostly TRGB, not re-verified). 22 galaxies, 720 points, y ~ 0.03.
**a0 = 7.80e-11 +- 41% (stat)**; outer half 6.95e-11. vs kappa = 1/2 rho_L -17% (0.45 sigma), alt -31%, SPARC TRGB gas points -33%.
Overlap with SPARC (DDO 154, DDO 168, NGC 2366): per-galaxy a0 LITTLE THINGS / SPARC = 1.58, 2.42, 1.60 (median 1.60) -- the two pipelines (different baryon
decompositions, inclinations, distances) disagree by ~60% on the SAME galaxies. Reading: per-galaxy baryon modelling, not just distances, moves a0 by tens of percent;
LITTLE THINGS adds no precision. Across p41b/p43/p46/p47 the cleanest estimates span 0.70-1.16e-10 by method. kappa = 1/2 stays FITTED.

## 55. Random-effects meta-analysis of the Upsilon-robust a0 estimates (`p48`, 1/2; pre-written P FAILED, kept; MUTATE TRGB 2e-10 fails H) -- 2026-10-05
Inputs (independent sets): SPARC gas TRGB/Cepheid 1.158e-10 (20%), SPARC gas Hubble flow 6.97e-11 (18%), WALLABY gas 7.28e-11 (23%), LITTLE THINGS 7.80e-11 (41%).
Q = 3.97 (3 dof), I^2 = 24%, tau = 0.13. **Pooled a0 = 8.32e-11 +- 13%** (7.28-9.51e-11). Pulls: Milgrom 2pi rho_L +0.27, Verlinde 6 rho_L +0.62, kappa = 1/2 rho_L +0.88,
Milgrom 2pi rho_tot +1.69, 32 pi turn-off +1.82, alt rho_tot (original c sqrt(G rho_c)/2) +2.30, conventional 1.2e-10 +2.74. The pre-written 'every candidate within 2 sigma'
FAILED: the alt footing and 1.2e-10 sit beyond 2 sigma. CAVEAT, load-bearing: three of four inputs rest on Hubble-flow distances or the authors' baryon models, which p46
and p47 show bias a0 low; the TRGB-only value (1.16e-10) alone favours the alt footing. The pooled verdict is distance-conditional. kappa = 1/2 stays FITTED.

## 56. Independent check of Sol's orbital sum rule (`p49`, 3/3; MUTATE wrong kappa^2/Omega^2 fails S, N) -- 2026-10-05
Sol (sol61_push/*/breakthrough_2026_10_05/, read-only) found Lambda c^4/a0^2 = (1/4) int y nu [kappa^2/Omega^2 - 1] dy for an isolated point mass. Own derivation:
kappa^2/Omega^2 = 3 + dln g/dln r (sympy from the definition), = 1 - 2y nu'/nu outside a point mass; integration by parts gives int y(nu - 1) dy - (1/2)[y^2(nu - 1)]_0^inf,
i.e. our p21/p25 vacuum integral when the boundary term vanishes. Numerically identical for nu_fix (y_t = 128): 99.812920 both sides; RAR: 12.987879 both sides.
For the exact framework kernel the boundary term grows like y/2 (the a0/2 tail): the rule needs PAPER41's turn-off. Correct and physical (the coefficient as an orbital
observable) but an identity, not a principle; the integrand is dominated by high y where kappa^2/Omega^2 - 1 is tiny, so data give only a lower bound. kappa = 1/2 stays FITTED.

## 57. Cosmicflows-4 rotation-free distances for the gas-point galaxies (`p50`, 1/2; pre-written G FAILED, kept; MUTATE CF4 x1.2 fails C) -- 2026-10-05
CF4 (Tully+2023, VizieR J/ApJ/944/94, 55,877 galaxies; 446 with TRGB) + CDS Sesame positions for all 175 SPARC names (175/175 resolved). Rotation-free distances only
(TRGB > Cepheid > SBF > SN Ia > SN II); Tully-Fisher, FP and the combined DM excluded (TF is built from rotation: circular for a0). Match within 60".
- **Control:** 32 SPARC TRGB/Cepheid galaxies: D_CF4/D_SPARC median 0.980 (16-84%: 0.976-0.986). Pass.
- 17 more SPARC galaxies gain a rotation-free distance, but **none has >= 2 points above the strict 80% gas cut**: the rotation-free gas-point set stays at 8 (pre-written
  'grows beyond 8' FAILED). POST-HOC at a 70% cut (17% Upsilon-sensitive, less clean): original 10 galaxies 1.20e-10 (+-17%); the 2 upgraded (UGC 8550, UGC 12632, TRGB) give
  7.08e-11 -- LOW even with TRGB distances; union 12 galaxies 1.175e-10 (+-16%).
- WALLABY: 9 kinematic galaxies have a CF4 rotation-free distance; only 1 has gas points. No usable upgrade.
Reading: the existing catalogues cannot grow the rotation-free gas-point sample; and the two new TRGB dwarfs sit low, so the TRGB-vs-Hubble-flow split is not purely a
distance effect (galaxy-to-galaxy scatter, s ~ 0.6 in ln a0, is large). The coefficient question stays open at the 15-20% level. kappa = 1/2 stays FITTED.

## 58. Holographic equipartition (Padmanabhan) as the missing premise (`p51`, 2/2; MUTATE drops hbar from T, fails H, T) -- 2026-10-05
Premise: the a0 horizon (r = c^2/2a0, T = hbar a0/2 pi c k) is in equilibrium, N_sur = A/l_P^2 = N_bulk = 2|E_Komar|/kT with E_Komar = 2 rho c^2 V for vacuum.
hbar cancels (a classical relation, as a0 requires) -- the first horizon-thermodynamic premise in the record with that property -- but it gives G rho r^2 = 3/(16 pi) c^2
(standard), 3/(8 pi) (no Komar factor), 3/(64 pi) (entropy normalisation): p17's one-pi values again, never 1. Not the missing premise. kappa = 1/2 stays FITTED.

## 59. The one-pi obstruction, certified (`fable_independent_2026/lean_2026/PUZZLE_32pi_one_pi_obstruction_2026_10_05.lean`) -- 2026-10-05
Why ~60 horizon/vacuum principles (p17, p19, p51 and the agent lanes) never give G rho r*^2 = c^2: each yields q * pi^(+-1) with q rational (G enters as 4 pi G / 8 pi G,
geometry adds rational volume factors). Lean (standard axioms; Mathlib `irrational_pi`): `one_pi_obstruction` q pi != 1 and q/pi != 1 for every rational q;
`p17_values_never_one` for the seven computed values; `gauss_shape_is_pi_free`: a whole-sphere flux balance g (4 pi r^2) = 4 pi G S cancels its pis exactly.
Consequence -- the SHAPE of the missing principle: a Gauss-law-type balance (flux of some field over the full horizon sphere = 4 pi G x a pi-free source) in which the
source is NOT a volume integral of rho (that re-introduces 4 pi/3). Not proved: the general net-pi statement (needs pi transcendental; not in Mathlib). MUTATE
(a pi-cancelling value inserted as '!= 1'): fails. kappa = 1/2 stays FITTED.

## 60. Which field has the flux? (`p52`, 2/2; MUTATE target c^2/2 fails U) -- 2026-10-05
Gauss balance g (4 pi r*^2) = 4 pi G S over the a0 horizon, for natural fields (kappa = c^2/2r* = the hole's own Newtonian field; 2 kappa = c^2/r*, the centripetal
acceleration of light circling at r*; the vacuum's own field (8 pi G/3) rho r; the hole's deep-MOND field) and sources (rho r^3, rho x ball volume, the hole mass).
**Exactly one of twelve combinations gives G rho r*^2 = c^2: field c^2/r* with the source rho_Lambda r*^3** -- equivalently **G rho_Lambda = (c/r*)^2 = Omega_light^2 = 2 Omega_Kepler^2(r*)**:
the vacuum's gravitational rate equals the angular frequency of light circling at r*. The hole's own field with the same source gives 1/2 (i.e. Lambda = 16 pi a0^2); ball-volume
sources give 3/(8 pi), 3/(4 pi). Neither ingredient is physical as it stands: light cannot orbit at a Schwarzschild horizon (the photon sphere is 1.5 r_s), and rho r^3 is the
vacuum energy of a cube, not a sphere. The puzzle's exact content is now 'light frequency on the a0 horizon = vacuum free-fall rate'; no known field supplies it. kappa = 1/2 stays FITTED.

## 61. PREMISE A and the conditional theorem (`fable_independent_2026/lean_2026/PUZZLE_32pi_premise_A_2026_10_05.lean`) -- 2026-10-05
PREMISE A (a hypothesis, new physics): the a0 horizon (r = c^2/2a0) obeys GR's horizon balance (vacuum source over the horizon = Gauss-Bonnet total 4 pi), with the MOND
sector coupling to the vacuum through G instead of 8 pi G: G rho (4 pi r^2) = 4 pi. Lean (standard axioms): `premise_A_implies_32pi` -- A + Lambda = 8 pi G rho + r = 1/2a0
=> Lambda = 32 pi a0^2; `premise_A_is_not_the_target` -- with coupling kG it gives Lambda = (32 pi/k) a0^2 (a different sector coupling gives a different number: screen 1 passes);
`gr_coupling_gives_nariai_side` -- GR's 8 pi G in the same balance gives Lambda = 4 a0^2. MUTATE (claims 16 pi): fails.
Status: a CONDITIONAL derivation with one clearly labelled new assumption. Its support must come from (i) a theory with a separately coupled MOND sector (the bimetric
auxiliary sector is the natural home) and (ii) its second prediction, a0 ~ sqrt(rho_DE) over cosmic time (PAPER42). kappa = 1/2 is DERIVED FROM PREMISE A; without A it stays FITTED.

## 62. p53: BIMOND with a general auxiliary coupling alpha (the natural home of PREMISE A)
`p53_bimond_general_alpha.py` (3/3; MUTATE q = 1/(2+alpha) fails F). Weighting the auxiliary metric's Einstein-Hilbert term by alpha (beta = 1):
the map is m = (nu-1)/(nu + (nu-1)/alpha); class independence holds for EVERY alpha (J - I_nu = d[(1+alpha)/alpha · y^2 (nu-1)^2], boundary term 0);
the vacuum conditions force f'(1) = (1-alpha)/(1+alpha), so **Lambda c^4/a0^2 = I_nu/(1+alpha)**. 32 pi needs I_nu = 32 pi (1+alpha).
Verdict: alpha is a real "own coupling of the MOND sector", but it is degenerate with the kernel's vacuum integral I_nu (i.e. with the turn-off y_t, p35/p45):
any alpha can be matched by a y_t. No value of alpha is forced (alpha = 8 pi - 1 needs I_nu = 256 pi^2; the exponential RAR's finite I = 25.98 needs alpha = -0.742).
alpha = -1 (Milgrom's main class) has no consistent vacuum solution of this form. So PREMISE A is EXPRESSIBLE in BIMOND but NOT derived: it relabels kappa as (alpha, y_t).

## 63. p54: what fixes alpha and y_t
`p54_what_fixes_alpha_yt.py` (4/4; MUTATE alpha = 1/3 fails A). v1 output kept as `p54_what_fixes_alpha_yt_v1criteria.out` (2/4): checks B and D were mis-specified
(B demanded exact agreement from an asymptotic form, off by 7.5e-6 relative; D tested "any integer" and 1/(1-p) = 29.3 sat 0.9% from 29); both restated in the open.
- **alpha is FIXED:** p53 gives f'(1) = (1-alpha)/(1+alpha); the g <-> ghat exchange symmetry (f'(1) = 0) forces alpha = 1 uniquely, ghost-free.
- **Crisp form (alpha = 1):** Lambda c^4 = int_0^inf (g - g_N) dg_N -- the cosmological constant is the phantom acceleration integrated over all field strengths.
  The exact law's plateau a0/2 diverges; a turn-off at g_t gives Lambda c^4 ~ (pi/4) a0 g_t, i.e. g_t = (4/pi) Lambda c^4/a0 = 128.9 a0 = 1.21e-8 m/s^2 on the kappa = 1/2 footing.
- **y_t is NOT fixed:** without hbar a0 is the only acceleration, so y_t must be a pure number of the UV kernel (and depends on its shape k); with hbar, g_t = a0^p a_P^(1-p) needs 1-p = 1/29.3 (unnatural); sqrt(a0 a_P) breaks the planets.
- **y_t is dynamically ~invisible:** at y = y_t the kernels differ by 0.19% in g/g_N (the Sun's field at 701 AU; a 1 M_sun binary at 700 AU separation).
Net: the puzzle is now exactly ONE pure number -- why int_0^inf (g - g_N) dg_N = 32 pi a0^2.

## 64. p55: natural principles for the turn-off -- all fail
`p55_turnoff_principles.py` (2/2; MUTATE wrong slope fails both). Leading slope L(y_t) ~ c_k y_t, c_k = (pi/2k)/sin(pi/k) (pi/4 at k = 2), checked numerically.
- P1 self-reflection (turn-off energy = vacuum energy, y_t = L(y_t)): needs c_k >= 1, i.e. k < 1.657 -- no root for any planet-safe smooth shape tried.
- P2 Unruh wavelength = dS radius / a0 horizon: y_t = 5.8 / 2 -> kappa 2.4 / 4.3, and both break SPARC (y_t >= 20).
- P3 the self-consistent version: y_t = 0.14, kappa = 21. Fails.
No principle built from a0, c, Lambda fixes y_t; the needed number (~129 = 32 pi / (pi/4) + log) still has to come from a UV theory of the strong-field end.
Forecast if a turn-off exists: the Sun's anomalous acceleration is 2e-14 at 100 AU, 1.5e-12 at 300 AU, 2.3e-11 at 700 AU, 4.5e-11 at 1500 AU (exact law: 4.7e-11 everywhere).
The turn-off lives in the extreme-TNO / inner-Oort region (300-1500 AU) -- the one place it is not invisible.
