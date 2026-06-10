# Agent N3 — the non-Huygens tail at scale: the unique bath-side escape is structurally REAL and numerically EMPTY (no (λ, m/H) window; four independent walls, margins 10⁵–10⁸⁶)

*agentN3, 2026-06-10. Task: scale the door agentF left open (`agentF_nonpert_detector.md` §5: "non-Huygens
fields — massive / minimally coupled in dS — retarded tails → trajectory-dependent dissipation; the unique
field-side escape" from the κ-only blindness lemma). Compute (1) the dS tail amplitude and its m/H scaling,
(2) the induced memory force on an accelerated worldline as a function of (λ, m/H, a/H), (3) the window
question against the banked solar budgets, (4) raw coefficients before comparison. Artifacts:
`agentN3_tail_scale.py` + `.out` (sympy exact pieces machine-verified; mpmath tail calibrated once and then
verified against four independent anchors). Both ways at full weight. arXiv ids for every external pin.
Motivation, stated and not claimed: the physically motivated bath candidate is the dark-energy field itself
(mass naturally ~H); since the framework ties a₀ to ρ_DE, a DE-field bath would make the kernel
a₀ ∝ √ρ_DE structurally natural. Nothing below assumes it; the calculation tests it.*

## 1. The exact pieces (raw numbers first — every one machine-verified in `.out` [N3-A1..A4])

**(1) Tail amplitude (massless minimal, exact).** For the minimally coupled massless scalar in dS₄ the
retarded Green function is `G_ret = δ(Δη−r)/(4π a a′ r) + (H²/4π)·θ(inside the cone)` — the tail is the
**constant H²/4π** on the entire interior of the light cone (derived in-script from the Bunch–Davies mode
sum: EOM + Wronskian + two Dirichlet integrals, all sympy-exact; the cone term reproduces the flat form
exactly). Cross-anchor: Burko–Harte–Poisson, PRD 65, 124006 (2002), **arXiv:gr-qc/0201020**, eq. (6.1):
G_smooth = 1/C² = H² in their 4π-Gaussian normalization (their eq. 2.10), ÷4π = ours; their eq. (6.8)
dm/dτ = −q²H² (Gaussian) is exactly this tail integrated along the comoving worldline — **the m=0 charge
loses ALL its mass in finite proper time** (their punchline; also Haas–Poisson **gr-qc/0411108**). So the
m→0 limit of this family is secular runaway — particle destruction, not MOND.

**(2) Massive tail (exact, four anchors).** From the BD hypergeometric two-point function (standard form,
e.g. Spradlin–Strominger–Volovich **hep-th/0110007**): W(P) = (H²/16π²)Γ(h₊)Γ(h₋)·₂F₁(h₊,h₋;2;(1+P)/2),
h± = 3/2±ν, ν = √(9/4−m²/H²); the retarded tail is V(P) = 2 Im W(P+iε). Calibration came out **exactly 1**
against the analytic normalization, then verified with no further freedom:
- m→0: V → H²/4π, P-independent (plateau ≈ 0.9995 at m/H = 0.01 over six decades of P) — anchor (1);
- cone value **V(P→1⁺) = (H²/4π)(1 − m²/2H²)** — matches the Hadamard transport value to 6 digits at five
  masses *including the sign flip past m² = 2H²*;
- **conformal point m² = 2H²: V ≡ 0 identically** (₂F₁(2,1;2;w) = 1/(1−w), pure pole, no discontinuity) —
  Door I's Huygens class sits inside this family as the zero-tail point, as it must;
- large-P falloff P^(−h₋), fitted = exact h₋ to 5 decimals. Small-m decay rate: h₋ → (1/3)(m/H)², i.e.
  Γ_tail = m²/3H in comoving time — the quasi-constant tail persists for ~3H/m².

**(3) The IR signature and its physical cap.** SY equilibrium variance **⟨φ²⟩ = 3H⁴/(8π²m²)**
(Starobinsky–Yokoyama, PRD 50, 6357 (1994), **arXiv:astro-ph/9407016**; sympy-verified from the
Fokker–Planck equilibrium and from the Langevin balance). BUT: relaxation time = 1.5(H/m)²/H, and our
Λ-phase is only t_dS ≈ 0.20–0.35 H⁻¹ old (z_Λ = 0.30, z_acc = 0.63) — **the 1/m² enhancement is NOT
available in this universe**: the usable variance is capped at H³t_dS/4π² ≈ 0.007 H², m-independent, and
the memory integral is capped at τ_eff ≤ t_dS ≈ 0.27/H. (Both eternal and capped versions computed; the
verdict is identical either way.)

**(4) Trajectory dependence (exact).** On the constant-proper-acceleration (Deser–Levin, **gr-qc/9706018**)
family, the dS invariant between two worldline points is **P(Δτ) = 1 + (2H²/κ²)sinh²(κΔτ/2)**,
κ = √(a²+H²) (sympy-verified from the static-patch embedding, including |a| and κ² = H²/(1−H²r²); flat and
geodesic limits check). The massive tail V(P(Δτ; a)) therefore *knows a and H separately* — the dissipation
kernel is **trajectory-dependent, exactly as agentF's lemma said only non-Huygens fields could be. The door
is structurally real.**

## 2. The memory force (the scale object)

Worldline coupling S = −∫m(φ)dτ, m(φ) = m(1+βφ/M_Pl,red) ⇒ scalar charge q = βm/M_red per particle (the
standard quintessence coupling; q dimensionless). The tail self-field dressing (Quinn **gr-qc/0005030** /
BHP lineage, m_eff = m₀ + qφ_self, φ_self = −q∫G_ret):

> **δm(a) = −q² (H²/4π) τ_eff(a/H; m/H)**, τ_eff = ∫v(P(Δτ;a))dΔτ, v = 4πV/H²

computed on a grid (m/H ∈ [0.01, 1.45], x = a/cH_Λ from 0 to Mars; steady-state AND t_dS-capped). Findings:
- **Sign: MOND-signed.** δm < 0 (inertia *deficit*), larger at low a, for all m² < 2H² — **the first
  MOND-signed object any bath channel has produced tonight** (Doors I and I-b found only anti-MOND
  dressing). Past the conformal point m² > 2H² the sign flips to anti-MOND.
- Comoving saturated value (small m, eternal): |δm| = (3/4π)q²H³/m² = 2π q²⟨φ²⟩/κ — the dressing IS the
  SY variance over the DL temperature scale.
- **Deep limit saturates**: g(x) = τ_eff(x)/τ_eff(0) → 1 as x → 0, so μ_induced → 1−ε = const — *not* the
  μ ~ x deep-MOND structure (a deficit plateau rescales G; it does not make BTFR). [Structure: N2's lane.]
- **Self-caught correction (bug-log discipline):** the pre-registered guess for the high-a falloff,
  x^−(1+2h₋), is **refuted by the computation**: the worldline integral is dominated by the near-cone
  plateau, giving the verified law **τ_eff(x≫1) ≈ (v_cone/κ)(2 ln κ + 1/h₋ + c₀)** — a **(ln x)/x tail at
  every mass**: the F1/Milgrom-99 linear-tail ephemeris class (`MI_BATH_TAIL_CONSTRAINT.md`, killed
  ×54,000), softened only by the log. There is no mass-tunable exponent: the dS-distinctive part of the
  cone amplitude that carries the high-a tail is H²/4π *exactly, mass-independent* (subtraction-robust).
- Capped (physical) profile is **flat across the entire galactic decade** (10% bend only at x ≳ 30–100):
  in the real, t_dS-old universe the a-dependence MOND needs at x ~ 0.02–2 is not there at all.

## 3. The window question — three channels, four walls, all closed (`.out` [N3-B2..B5])

**Required for the window:** ε ≡ |δm|/m ~ O(1) at x_gal = a₀/cH_Λ = 0.173 (both footings run; identical).

**Wall 1 — the coupling wall (decisive; channel i).** ε = β²(m_p/M_red)(H/M_red)·τ_eff H/4π, and
(m_p/M_red)(H/M_red) = **1.9×10⁻⁷⁹** — the bath carries energy scale H per coupling, the inertia to modify
is nucleon-scale. Numbers (capped, best m/H):
- at the Cassini-maximal universal coupling β = 3.4×10⁻³ (γ−1 = (2.1±2.3)×10⁻⁵, Will LRR
  **arXiv:1403.7377**): **ε = 4.7×10⁻⁸⁶** — short by 2×10⁸⁵;
- at β = 1 (gravitational strength): 4.1×10⁻⁸¹; at q = 1 per nucleon (a fifth force ~10³⁷ × gravity):
  2.8×10⁻⁴⁴ — *even that* is 43 orders short;
- required (quoted at the DE-motivated m = H; the m/H-grid spread is ×1.4): **β ≈ 2.2×10⁴⁰**, i.e.
  q ≈ 8.5×10²¹ per nucleon = scalar exchange **9.8×10⁸⁰ × gravity ≈ 8×10⁴⁴ × the Coulomb force** between
  two protons, on an unscreened Hubble-wavelength carrier. Excluded by Cassini by ×(2–4)×10⁸⁵;
  composition-dependent variants are bound harder still (MICROSCOPE final,
  η = [−1.5±2.3±1.5]×10⁻¹⁵, **arXiv:2209.15487**); this is Carroll's quintessence-coupling problem
  (**astro-ph/9806099**) at its maximal violence. Chameleon screening (**arXiv:1407.0059**) cannot rescue
  it: screening that hides the solar coupling raises m_φ in galaxies (ρ_gal ≫ ρ_cosmic) and kills the
  light-field tail there first — self-defeating. Coherent-body coupling (ε_body = N·ε₁) buys 10⁵⁷ for a
  star and still sits at 2.8×10⁻²⁹, while making δm/M ∝ M — a ~10-dex universality violation across the
  SPARC mass range. The eternal-dS m→0 "enhancement" is the BHP runaway (mass destruction) and is capped
  by t_dS anyway.

**Wall 2 — the shape wall (channel ii; coupling deliberately unconstrained).** With ε set to do the
galactic job, the (ln x)/x tail puts Saturn at 2×10⁵–3×10⁶ × the radial budget (2.3×10⁻¹⁵) and the solar
reflex at 2×10⁵–1.5×10⁶ × the agentE survival-line budget (s < 3.21×10⁻¹¹ ⇒ response < 2.45×10⁻¹⁵), at
EVERY mass. Reverse direction: the solar budgets cap the galactic magnitude-keyed tail term at
**4.2×10⁻⁶ a₀** (best case, lightest mass) — short of the job by 2.4×10⁵ *even with unlimited coupling*.
The only masses with a solar-softer profile sit past m² = 2H², where the sign is anti-MOND and the
amplitude has crossed zero. Two independent walls, each alone sufficient.

**Wall 3 — the frequency bracket (channel iii; N2 coordination, bracketed not blocked).** A term keyed as
s·(H/Ω)^p, p ∈ {1,2}: galactic Ω/H_Λ ∈ [28, 1.8×10³] (dwarf edge → massive edge), Saturn 3.7×10⁹, Mars
5.9×10¹⁰. Solar side: **safe** — exposures land 10²–10⁸ below the budgets (frequency suppression does open
solar room, as anticipated). Source side: the required raw amplitude is a₀·(Ω_gal/H)^p = **4.8–319 cH_Λ
(p=1), 132–5.9×10⁵ cH_Λ (p=2) per unit mass** — versus the bath ceiling at maximal allowed coupling of
~10⁻⁸⁵ a₀-equivalent: short by ≥ 87 orders. Structure flag for N2: Ω = a/v imprints a v-dependence at
fixed a (×15 spread across SPARC at p=1) — an RAR-universality liability independent of scale.

**Wall 4 — the equilibration cap.** The ⟨φ²⟩ = 3H⁴/8π²m² IR enhancement needs 1.5(H/m)² Hubble times; the
Λ-phase provides 0.2–0.35. For every m ≲ H the enhancement never materializes: the usable kernel is
m-independent (τ_eff ≈ t_dS ≈ 0.27/H), 6× below even the m = H eternal value and 10³–10⁵× below the
m ≪ H eternal values the IR-enhancement hope was built on. (Drag channel, for completeness:
≤ 7×10⁻⁸⁸ a₀ at Cassini coupling.)

## 4. Raw coefficients (Door-III discipline: in isolation, BEFORE comparison)

| raw object | value | status |
|---|---|---|
| tail amplitude coefficient (×H²) | 1/4π = 0.0796 | EXACT (A1 + BHP) |
| cone-value mass factor 1 − m²/2H² (at m=H) | 1/2 | EXACT (A2) |
| SY variance coefficient (×H⁴/m²) | 3/8π² = 0.0380 | EXACT (A3) |
| small-m decay-rate coefficient (h₋/(m/H)²) | 1/3 | EXACT |
| comoving saturated dressing (×q²H³/m²) | 3/4π = 0.2387 | EXACT-asym |
| dressing–variance identity (×q²⟨φ²⟩/κ) | 2π | EXACT-asym |
| P-space kernel exponent h₋ at m=H | 0.38197 | EXACT (≠ worldline-tail power; §2) |
| trajectory-invariant coefficient | 2 | EXACT (A4) |

**Post-hoc comparison (flagged as such):** nothing lands on Z = 5.789, 1/Z, 2, or 2π. Nearest accidents:
1/3 vs 2/Z (3.5% — the same 3.5% family as agentB's banked 1/6-vs-1/Z near-miss, doubled; structurally
meaningless, recorded so nobody "discovers" it later); 3/4π vs 1/Z misses by 38%. Consistent with the
banked verdict: **Z stays data-selected; no coefficient claim arises here.**

## 5. VERDICT (both ways, full weight)

- **The door is structurally REAL.** The non-Huygens tail delivers exactly the two features agentF's
  closure said only it could: a trajectory-dependent dissipation kernel (P(Δτ; a) enters the memory
  integral — a and H are known separately, the blindness lemma is escaped), and — new tonight — the
  **MOND sign** (an inertia *deficit*, growing toward low a), the first and only bath channel of the night
  with the right sign. That much is framework-favorable and is stated at full weight.
- **The window is EMPTY.** Four independent walls, each sufficient, two of them coupling-independent:
  (1) the coupling wall — the galactic job needs a per-nucleon scalar charge 10⁴²× the Cassini-allowed
  universal coupling (a fifth force ~10⁸¹ × gravity ≈ 10⁴⁵ × Coulomb); at allowed couplings the tail term
  is 10⁻⁸⁶ of the job; (2) the shape wall — the dressing's high-a tail is (ln x)/x at every mass (the
  banked F1 ephemeris class; pre-registered power-law hope refuted by own computation), capping the
  galactic term at 4×10⁻⁶ a₀ even at unlimited coupling; (3) the frequency-suppressed bracket is
  solar-safe but source-impossible (≥87 orders); (4) the equilibration cap — the light-field IR
  enhancement does not exist in a 0.3/H-old Λ-phase, and the m→0 limit is the BHP mass-loss runaway.
  Margins of 10⁵–10⁸⁶ are immune to every convention axis the working rule names (footing, a₀ vs cH,
  weighting, capped vs eternal — all run both ways in `.out`). **The unique bath-side escape narrows to
  nothing for any worldline coupling a light scalar is allowed to have.** This kill is
  coupling-strength-keyed, not perturbation-theory-keyed: a non-perturbative regime (λφ ~ m_p) needs the
  same impossible charge, so it dies on the same wall.
- **What this does NOT close (named, honest):** extended (non-point) detectors and the field-level hybrid
  (Door II's lane — after the 40.5σ lensing wall the missing object needed a metric partner anyway);
  the charity assumptions are explicit — the orbital acceleration was treated as the worldline's proper
  acceleration (most favorable reading; the banked constituent-incoherence problem rides along), and
  stationary-|a| coherence was granted (rotation of ê only suppresses further).
- **What survives, sharpened:** the *kinematic* half of the bath idea — κ = √(a²+H²) bends at a ~ cH, so
  any dS-bath object automatically knows *where* a₀ is — remains intact and is exactly why the family kept
  passing shape tests. What is now quantitatively dead is the *energetic* half: converting a bath whose
  energy scale per coupling is H (10⁻³³ eV) into an O(1) modification of nucleon-scale inertia costs the
  hierarchy (m_p/M_red)(H/M_red) ≈ 10⁻⁷⁹, and no allowed coupling crosses it. One line for the program:
  **the dS bath has the right length scale and the wrong energy scale; a₀ ∝ √ρ_DE can be a kernel of the
  law, but not the strength of a worldline force.** The missing object, if it exists, is not a
  weak-coupling worldline bath effect — it is field-level (Door II) or nothing.
