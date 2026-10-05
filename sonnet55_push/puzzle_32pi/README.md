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
