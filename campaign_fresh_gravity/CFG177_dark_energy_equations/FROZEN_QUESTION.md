# CFG177: the equations of the dark energy in the committed action. Frozen before any script (2026-09-29)

**The owner's directive:** "figure out the equations of the dark energy itself and how it works". His picture is that the dark-energy vacuum FLOWS, it is compacted as it pushes through matter, and the extra gravity is a boosted effect of the flow. The governing file is `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md` (gates G1–G8, Addenda 1–2). Also governing: `CFG174_door11_vacuum_column/README.md`.

**Seen before writing this:**
- CFG43's README, `A_common.py` and `A1_action_field_equations_dof.py`
- CFG44's README and `Bcommon.py`
- CFG171's and CFG176's frozen questions
- CFG174's README
- the ten-doors gates file

No CFG177 code has been run. The menu below was written knowing the target (CFG44's C(r); the P2 law) and knowing that every local route in the record failed. It is not a blind sample.

**The lead (from the record, to be derived, not assumed).** CFG43's committed action already contains a current for the dark energy:

    S = ∫d⁴x { √−g [(M_P²/2)R − M_P²Λ − ρ(n; Λ)] + M_P²Λ ∂ₘTᵐ + Jᵐ∂ₘθ },   ρ(n;Λ) = m n + P_cap x arctan x,  P_cap = ε M_P²Λ,  ε = κ²/8π

In the Henneaux–Teitelboim (HT) form, Λ comes with a vector density Tᵐ. Equivalently, Tᵐ is the dual of a 3-form A with Λ ∝ *dA. T⁰ is the unimodular (cosmic) clock. Read literally, tᵐ = Tᵐ/√−g is a flowing vacuum, and its divergence is changed wherever matter depends on Λ ("compacted as it pushes through matter"). This is the Addendum-1 11C reading: "the top" is the time direction, and compaction is the flow's divergence being changed by matter.

## Q1: the field equations and the gauge (sympy, explicit metrics)

1a. On an explicit static spherical metric (−e^{2α(r)}, e^{2β(r)}, r², r² sin²θ), with all fields functions of all four coordinates, derive the Euler–Lagrange equations of CFG43's action for Λ and Tᵐ. Expected:
- ∂ₘΛ = 0
- ∂ₘTᵐ = √−g (1 + ρ_Λ/M_P²) = √−g (1 − P/ρ_vac), with ρ_vac ≡ M_P²Λ. The −P/Λ comes from CFG43's EOS identity ρ_Λ|ₙ = −P/Λ, re-derived here.
- The fluid equation ∂ₘJᵐ = 0.

1b. The 3-form dual: Tᵐ = (1/3!) εᵐⁿᵖᵍ A_npq ⇒ ∂ₘTᵐ = (1/4!) εᵐⁿᵖᵍ F_mnpq, with F = dA.

1c. The gauge freedom. Tᵐ → Tᵐ + ∂ₙωᵐⁿ, with ω antisymmetric, leaves ∂ₘTᵐ, and hence the action, unchanged identically. This transformation is A → A + dλ. It is reducible: ω → ω + ε∂ξ leaves Tᵐ unchanged.

1d. The metric equations. Show whether the HT term contributes. It is metric-independent, so it should not. Show that Schwarzschild–de Sitter (SdS) solves the vacuum equations whatever Tᵐ is.

1e. Which part is physical, and which is gauge (the physical/gauge split). Construct explicit gauge-equivalent flows on the same solution:
- a "clock" gauge with no spatial flow;
- a radial "river" outflow;
- an inflow converging on the galaxy;
- a uniform stream "from the top" (the 11B′ picture).

Then show that the instantaneous flux through a sphere can be set to any function of time. Show that the gauge-invariant content is exactly two things:
- the local scalar ∇ₘtᵐ, which the matter fixes algebraically;
- the flux through closed 3-surfaces, i.e. the 4-volume. Its global zero mode is CFG43's one global pair.

## Q2: the flow around a static point mass and CFG44's exponential sphere

2a. Point mass (SdS): √−g = r² sinθ exactly. So the river-gauge current and its flux per unit Killing time through the areal sphere are expected to be (4π/3)r³, exactly independent of M.

2b. The exponential sphere (weak field, dust baryons, Λ-independent): the 4-volume deficit from GR's volume distortion. Expected fractional size ~GM/(Rc²) ~ 10⁻⁶, and not of the MOND form.

2c. With CFG43's cap fluid holding CFG44's target pressure, P = (a₀/4π)∫_r^∞ M_b(<r′) r′⁻³ dr′, the divergence deficit is (1/ρ_vac c²)∫P dV. Expected closed form: (4π/3)r³P(r) + (a₀/3)∫₀^r M_b(<r′)dr′. For a point mass this is a fraction 3ε/x² of the volume. The cap P ≤ P_cap bounds the deficit at ε ≈ 1%.

2d. Does anything in the metric respond, and is the flow observable? Expected: no, and no. Λ is constant, and Tᵐ appears in no other equation.

2e. How much "compaction" the picture would need (a cross-check of CFG176 Q1f, not a new result):
- ρ_phantom/ρ_Λ over x ∈ [0.1, 30], for M_b = 10⁹–10¹² M☉, point mass and exponential sphere (h = 0.5 r_M and h = 3 kpc), P2 primary, ν_mono reported;
- the active-mass sign of a compacted w = −1 medium, ρ + 3p = −2ρ (it repels);
- the HT action's actual compaction, which is none (Λ is constant).

## Q3: promote the flow to a dynamical dark energy (the minimum addition)

3a. Add the 3-form mass term. In dual variables this is U(t²) = −(σ/2) g_mn tᵐtⁿ, which makes tᵐ physical. The massive three-form of Koivisto & Nunes 2009 (Phys. Rev. D 80, 103509; from memory, unverified) has the same U, but W(Λ) quadratic instead of HT's linear W. Here CFG43's linear W is kept, and the dual identities are verified. The only way to add no dimensionful constant is σ = s M_P²Λ² with the HT field itself: a Λ-power of 2 is the only one that gives an O(1) pure number. **s is a new pure number.** Its one declared illustration, fixed now and not scanned, is s = κ² (λ = √s = ½). That value is a POSTULATE, not a tie, and the G1 verdict must not depend on s.

3b. Derive the equations (FRW minisuperspace by Euler–Lagrange, and the covariant form). Expected:
- tₘ = M_P²∂ₘΛ/σ: the vacuum flows along its own density gradient.
- ∇·t = 1 − P/ρ_vac + (Λ-dependence of σ).
- Together these are a canonical scalar φ = (M_P/√s) ln Λ with V(φ) = M_P²Λ ∝ e^{√s φ/M_P}.
- The flow's energy is σ(t⁰)²/2 = φ̇²/2 = (1 + w)ρ_DE/2.

3c. The Dirac count on a periodic 1-D lattice, re-implemented from CFG43's method. The HT mode must reproduce CFG43's D = 2N + 2. The HT + U mode is expected to give D = 4N, i.e. one local dof added.

3d. Ghost and gradient stability: the sign of the reduced Hamiltonian's quadratic part (healthy iff s > 0), and c_s = 1.

3e. Background cosmology. Thawing from rest at a = 10⁻⁶, flat, Ω_Λ-equivalent 0.6847 today, Ω_m = 0.3153, radiation included. Report:
- w(z) at z = 0, 0.5, 1, 2, and w₀, w_a = −dw/da at a = 1;
- the growth ratio D/D_ΛCDM at z = 0, at the same Ω_m;
- the quasi-static clustering ratio of δφ at k = 0.01–30/Mpc;
- that the background flow tᵘ is along the Hubble-flow 4-velocity;
- the s → 0 limit (must be ΛCDM).

3f. The static solution around baryons, and whether the MOND form arises.
- Linearised Klein–Gordon on a weak static metric: ∇²δφ = V″δφ + 2V′Φ/c².
- The scalar's active mass density in GR, 2(φ̇² − V). Static gradient energy drops out.
- (i) Dust baryons only: δg/(g_law − g_N) over x ∈ [0.1, 30], 10⁹–10¹² M☉, point mass and exponential sphere.
- (ii) With the cap fluid at the target pressure: the same ratio.
- The M- and r-scalings of δg against √(GMa₀)/r.
- The λ² that would be needed to reach the boost at x = 1, and whether any exponential slope that large still accelerates. The scaling-solution w = −1 + λ²/3 is to be verified symbolically.

3g. Scoping only: what the MOND form would require. The baryon masses coupled to Λ (m ∝ Λ^{β_b}) and U ∝ |t|^{3/2}.
- Derive the deep-MOND form and the coefficient needed for a₀ = κc√(Gρ_Λ).
- Count the constants.
- Lensing under a conformal coupling (the refractive index is independent of the conformal factor).
- Two items reported, not load-bearing: the cosmic time-current's external-field cut radius r_c/r_M, and the health of the timelike-branch continuation.

Expected: this is AQUAL in dual variables, a restatement.

## Q4: constants, and the verdict class

Count every constant beyond κ and Ω_c h². CFG43's ν* is inherited and is not counted again. The verdict is one of:
- "no new content" (pure gauge);
- "a dynamical dark energy with a flow but no MOND force";
- more.

## Gates (door 11; scored separately per construction, never pooled)

The three constructions:
- **HT**: the committed action.
- **DYN**: the minimal promotion (3a–3f).
- **DAQ**: the dual-AQUAL scoping (3g).

Pass lines are as in the gates file. Additional rules:
- G1: 10% over x ∈ [0.1, 30], 10⁹–10¹² M☉, the same constants at every mass. A restatement scores p* at most.
- G2 for DYN: the growth ratio within 5% of ΛCDM, and the background current along the Hubble flow. The CMB is not computed, so it is OPEN, not passed.
- G3, G6, G7: a sector that exerts no force on baryons scores "vacuous".
- G4: s and β_b are FAILs.
- G5: no ghost, no gradient instability, causal, and the Solar-System anomaly at 1 AU below Q₂-level (5.2 × 10⁻²⁷ s⁻², GATES 4.01).
- G8: not applicable (the 11C reading).

## Controls (each must change the headline; outputs named by mode; control failures kept)

- **E1 MUTATE=1:** add U to the HT action. Then ∂Λ = 0 must no longer follow, the gauge invariance of the action must fail, and Tᵐ must enter the metric equations.
- **E2 MUTATE=1:** make the baryons Λ-dependent (β_b = 1). Then the point-mass flux must stop being M-independent.
- **E3 MUTATE=1:** s < 0. The ghost check must fail.
- **E3 MUTATE=2:** s = 0. Then D = 2N + 2 and w ≡ −1, and the "one local dof" check must fail.
- **E4 MUTATE=1:** a positive control. The G1 scorer is fed the dual-AQUAL force with U built to reproduce P2. The "no MOND force" headline must flip.

## Honest expected outcome (declared now)

- **HT:** no new content. The flow is gauge apart from a divergence that the matter fixes, 0 in baryons and ≤ ε ≈ 1% in the cap fluid. There is no metric response and no local dof.
- **DYN:** a thawing quintessence whose "flow" is its time derivative. Its w(z) and growth are close to ΛCDM for s = κ². There is no MOND force: ≤ 10⁻¹⁴ of the boost, with the wrong M and r scaling. G4 fails on s.
- **DAQ:** reproduces the MOND form only by putting a₀ into U by hand. It needs a new constant β_b, and a conformal coupling does not lens.

A scoped no-go or "no new content" is a valid answer. κ = ½ stays FITTED. Nothing here says the theory is closed.

## Note (2026-09-29, before any script): the owner's Addendum 2 of the door-11 gates file, relayed by the coordinator

The flowing medium has no rest mass and is not a particle. The extra gravity is an effect of the flow, not of mass the flow carries. "No mass" is read as no rest mass or particle content, not as no energy. Therefore each construction must state its medium's stress-energy and whether and how it gravitates:
- HT: T_μν = −ρ_vac g_μν (w = −1). The current carries no stress.
- DYN: a canonical-scalar perfect fluid moving along tᵘ, with w ∈ [−1, 1] and active density 2(φ̇² − V).
- DAQ: as DYN, plus the conformal fifth force.

The CMB's cold mass (Ω_c h² ≈ 0.12) is not supplied by any construction here and stays as in candidate B / CFG43. None of the constructions removes it, so G2 is not asked to pass without it.

## Note 2 (2026-09-29): the orchestrator's priority note, added AFTER E1–E3 had run and BEFORE E4 was written (disclosed; the body above is unchanged and its pre-script hash is in FROZEN_QUESTION_SHA256.txt)

The owner wants the time-direction reading pushed: the flow is cosmic time, and matter changes its expansion rate. A sibling lane (CFG176) reports that a Λ cannot flow in GR, and that a time-direction flow reproduces ΛCDM's H(z) exactly. Two things are added to Q3, both to be computed in E4:

- **3h. The time-flow version, and a direct test of "compaction by matter".** In DYN the HT current is timelike, and its time component (the unimodular clock) is the canonical momentum of ρ_vac (E3-HEALTH). The time flow's divergence is sourced by matter through ∇·t = 1 − P/ρ_vac − sΛt². The added case lets the **baryons** source that divergence, m ∝ Λ^{β_b}, so matter compacts the time flow directly.
  - Derive the static force on baryons. Expected: G_eff = G(1 + 2β_b² s), Newtonian 1/r² in shape. Also derive the PPN γ − 1 for the conformal coupling, against Cassini (|γ − 1| ≲ 2.3 × 10⁻⁵, commonly quoted; from memory, not re-verified).
  - Question: does any consequence reach √(GMa₀)/r without new constants? Expected: no. The linear Gauss law gives M/r², and the MOND form needs DAQ's nonlinear U with a₀ put in by hand.
- **3i. The relation to a khronon.**
  - In DYN, t_μ = ∂_μτ with τ = −1/(sΛ). So the vacuum current is hypersurface-orthogonal, and the level sets of the unimodular clock (equivalently of ρ_vac) define a physical foliation with unit normal u_μ = ∂_μτ/√(−∂τ·∂τ), a khronon-type field.
  - In HT the same foliation is pure gauge (E1-SPLIT).
  - Unlike the Blas–Pujolàs–Sibiryakov khronon, DYN's action is not invariant under τ → f(τ): the clock's rate is physical, it is ρ_vac.
  - Neither matter nor gravity couples to u_μ, so there are no preferred-frame terms.
  - Adding the khronon couplings is door 11C's aether/khronon route (CFG172). There the record's FC-KH, KM1, KM3 and V0 exclusions apply; that route is not run here.

Pass lines are unchanged: G1 at 10%, G4 counts β_b and s, G5 is Cassini. A scoped no-go is valid.
