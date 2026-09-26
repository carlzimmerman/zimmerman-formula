# The clean path — what dark energy does in this theory, and what closure takes (2026-09-26)

**What this is.** A first-principles reading of the record as of 2026-09-26: what follows from the framework's one
principle, what dark energy is and does in the theory as built, where every gate stands, and the shortest route to a
closed theory. Every load-bearing statement cites a committed lane; the new results of this session are DE1 and DE2
(this directory) with their Lean certificates. It is a synthesis, not a new claim: nothing here is a derivation of κ,
and "closed" is not claimed. An independent audit of an earlier draft of this note (the lead track's
`real_research/closure_resume_2026_09_26/recipe_audit.md` and `dark_energy_audit.md`, uncommitted at the time of
writing) found five overclaims; they are
corrected here, and its stricter labels are adopted throughout.

---

## 1. One principle, and what follows from it

**The premise.** Gravity gets exactly one new scale, and the vacuum supplies it. This is a model-building premise until
an action enforces it: in the C-H action Λ and a₀ are independent inputs. What follows is what the premise implies.

| consequence | status | where |
|---|---|---|
| a₀² ∝ G · (vacuum energy), i.e. a₀ = κc√(Gρ_Λ): **given** that a₀ is built from the vacuum energy alone, the form is forced (exponent matrix, det = 2) | conditional: forced by the premise, not by an action | `qwen_claude_field_theory/closure_2026/a0_promotion_2026/a0_from_condensate_action_2026.py` |
| with a₀ tied to the vacuum's pressure, a₀² = κ²G(−p_vac) (the stage-17 promotion, a postulate), a w = −1 vacuum makes **a₀ flat in time** (< 1% to z = 5); ΛCDM's emergent scale rises (+0.33 dex at z ≈ 2.5) | postulate + exact consequence | L37, L273–L275 |
| κ, one pure number: measured 0.465 ± 0.076 (BTFR), 0.55 ± 0.17 (distance-free), consistent with ½; Z = cH_Λ/a₀ = √(32π/3) = 5.7888 is κ restated | measured, **not derivable** in the present action class | `kappa_closure/k01–k03` |
| the de Sitter vacuum has no invariant timelike vector; so the preferred frame the record's local constructions need can only be a *state* — one clock field (the khronon) | theorem (representation) + the record's scoped class exclusions | `opus_48_extended_research/reviews/gap2_rep_door/so41_no_invariant_timelike_vector.py` |
| strict two-DOF MOND with an external-field effect can signal instantaneously (conditional theorem); a moving source's phantom needs a momentum channel ⇒ **2 tensors + 1 extra scalar (the khronon)** — whether it qualifies as the spec's separately counted "genuine clock" needs the full canonical classification of the assembled action (open) | theorem (conditional) + open count | `qwen_claude_field_theory/theory_2026/york/elliptic_channel_signaling_theorem_2026.py`; L330; L340 |
| in L340's tested momentum channels the kernel must have a monotone phantom (243/243 negative-coefficient cells unhealthy — a bounded scan of the families tried, not a theorem for every channel), and GR then comes back through a filter, not the kernel's tail. The exact exponential law has longitudinal coefficient C_L = (1−x)/(eˣ + x − 1) < 0 for x > 1 (exact), so it cannot be imported into that branch; in the reduced C-H/K block both exact laws need α_c > 0.06 (RAR) / 0.27 (exponential) against the candidate's ceiling 3.2×10⁻⁹ (lead-track peer review); whether another constrained action can carry them is open | scoped | L340 H2/H3, S1; lead-track recipe audit and peer review |
| one metric, minimal coupling ⇒ any component the kernel cannot see feels Newtonian gravity only (reciprocity) | theorem | L353 N2 |

The cleanest action-level statement of the premise on the record is the **four-form promotion** — a distinct action
proposal, not part of C-H/K (`kappa_closure/k04`): one conserved, non-propagating flux q sets both ρ_Λ and a₀ = β√G|q|. It makes a₀ ∝ √(Gρ_Λ)
structural and a₀(z) exactly flat, and leaves one ratio free: κ = ½ ⟺ Z/β² = 7.96. It also predicts an environmental
a₀ that switches off above 155 a₀, invisible in galaxies (< 0.002 dex) and a ~1σ shift of wide-binary γ_v for Gaia DR4.
Once the MOND term depends on q, the conserved object is ∂L/∂q, not q itself, so "exactly flat" holds for the vacuum,
not unqualified inside coupled environments. A related identity (XC1 A7, the peer track): with a₀ = κc√(Gρ_Λ)
substituted, the unfiltered MOND sector's strong-coupling scale √(M_P a₀/c²) = (κ²/8π)^{1/4} ρ_Λ^{1/4} ≈ 0.7 meV is
the dark-energy scale — a conditional algebraic consequence of the premise, not an independent derivation of it.

## 2. What dark energy is, and how it works

**What it is (as built).** The ground state of the vacuum's own field, with w = −1 exactly for a constant vacuum term
(T_μν = −V g_μν, ρ + 3p = −2V < 0: the acceleration mechanism). Two readings are
on the record: the ghost-condensate ground state of the clock field (AeST's K(Q) = μ²(Q−1)², Blanchet–Skordis 2024
eq. 7), or a non-propagating four-form flux (k04). Either way it is not a particle and it does not evolve: a DESI-type
w(z) ≠ −1 would be the excitation, not the vacuum. That is a prediction. (Homogeneity alone does not force the field to
its vacuum: the lead track's exact homogeneous check shows the same action admits a charged state with a dust term
Q₀I/a³ and a stiff term I²/(2Aa⁶) — the dark-mass amount is initial data.)

**How it works — three jobs.**
1. **Its energy accelerates the expansion** (Λ).
2. **Its pressure sets gravity's low-acceleration scale**, a₀ = κc√(Gρ_Λ) = c²√(Λ/32π) at κ = ½. Because the vacuum
   does not evolve, neither does a₀: the flat-a₀(z) prediction (the flagship).
3. **Its share of the expansion decides where that response can act** — in the construction as prescribed, not yet as
   a varied action (see §5). In the assembled construction MOND acts only
   in bound regions where u = x̃ [Ω_Λ(z)/Ω_Λ,0]^p ≥ x_c0 (L359), with x̃ = 9(R⁽³⁾ + σ²)/(4K²) the leaf's curvature
   against its expansion and Ω_Λ = 3Λc²/K², a local scalar of the clock's foliation. For p = 1 the gate is simply
   x̃Ω_Λ = 27Λc²(R⁽³⁾+σ²)/(4K⁴): local curvature times vacuum curvature against the expansion rate to the fourth power.
   This third job is what lets one theory have MOND galaxies now and ΛCDM-like growth, forest and CMB earlier:
   a constant threshold cannot (KiDS needs x_c ≲ 3 at z = 0.25, the forest ≳ 5.4 at z = 2 — L352/L358/L362), and the
   vacuum's share, rising toward today, supplies exactly the time dependence the two need.

**What it does not do.** It does not supply the dark *mass*: the amount of cold dust any shift-symmetric vacuum field
carries is a free modulus (the I₀ theorem, `opus_48_extended_research/reviews/GHOST_CONDENSATE_2026-06-19.md`), and the CMB and clusters still require that mass.
It does not fix κ.

## 3. How tightly the data pin dark energy's third job (DE1, DE2 — new)

**DE1** (`DE1_vacuum_gate_flagship.py`, 5/6 with the pre-declared F1 failure recorded; MUTATE rc = 0). Beyond the switch
edge a galaxy weighs its baryons (Gauss, L352), and the edge sits at r_e = v_f/(√x_c,eff H(z)). So the deepest MOND
acceleration visible at redshift z is

  **y_edge = x_c0 (H₀²/a₀^{3/2}) √(GM_b) E(z)^{2+2p}**   (Lean: `y_edge_formula`)

The flagship (y = 0.1, M_b ≤ 10¹¹ at z = 2.5) therefore caps the exponent: **p ≤ 1.97** (x_c0 = 2, canonical; 2.07
alt). The cell the best-standing construction uses for cosmic shear (p = 2, x_c0 = 2) fails at M_b = 10¹¹ canonical:
edge 36.8 kpc inside the flagship radius 38.6 kpc, zero point −1.13 dex (Newtonian) instead of 0. The same law is a
distinctive prediction for any gate: **the MOND region of every galaxy shrinks as E(z)^−(1+p)**, so resolved kinematics at
z ≳ 3–5 should show Newtonian outer discs beyond r_e — below today's reach at z ≈ 2.5–3, where even the p = 2 edge
stays at ≥ 1.7 r(y = 1) for the flagship masses.

**DE2** (`DE2_vacuum_gate_joint_window.py`, 8/8; MUTATE — constant thresholds only — closes the window, rc = 1). Each
gate reads the gate at one epoch: KiDS-1000 caps x_c,eff(0.25) at 3.867; cosmic shear needs x_c,eff(0.5) ≥ 3.50 / 2.93 /
2.49 at v_k = 600 / 650 / 700 km/s; the flagship caps x_c,eff(2.5) at 364.5; the forest is certified by dominance over a
committed passing cell. Because the vacuum's share Ω_Λ(z) falls into the past, a single gate can sit low enough for
KiDS at z = 0.25, high enough for cosmic shear at z = 0.5, and still below the flagship's cap at z = 2.5. **A window
exists: p ∈ [0.5, 2.07], and it contains the linear gate p = 1** with x_c0 ∈ [2.005, 2.975] (600 km/s). With p = 1 the
gate is the simplest local form, u = x̃Ω_Λ/Ω_Λ,0 = 27Λc²(R⁽³⁾+σ²)/(4Ω_Λ,0K⁴) ≥ x_c0, and the flagship then survives to
z ≈ 4.2–5.0. This pins how dark energy does its third job to a window; it does not derive it. The construction's
particle-mesh gates (clusters, clearing, Harvey; L380/L381) were run at p = 2 and must be re-run at (p = 1, x_c0 = 2.5)
before the assembled construction can claim that cell (never pool passes across cells). Lean:
`window_iff`, `window_p_interval`, `dominance`, `ungated_pincer`, `linear_gate_cell_in_window`.

## 4. The theory as it stands, sector by sector

| sector | what is built | standing | open |
|---|---|---|---|
| gravity + clock | **C-H/K**: GR + khronon (BPS terms α_c a² − c₂K², leaf-average λ-term) | linear frozen-coefficient health in the scanned channels; moving-source tracking; static β = γ = 1 derived in the reduced khronometric sector (KM3; other PPN terms and the filtered remainder documentary); c_T = 1 in the tested TT sector; c₂ under the Planck cap; G8 bounded pass at frozen-background, decoupling-limit scope including the filter/foliation vertices (XC1 + XC3, peer lanes); conditional at full-action scope | full canonical classification (is the khronon the spec's "genuine clock"?); nonlinear well-posedness scoped by XC2 (peer, f3b848273) — but the lead track's peer review (`real_research/peer_review_2026_09_26/`, uncommitted) finds XC2's all-kernel convexity step applies an unweighted heat contraction to a lapse-weighted norm (sound for a genuinely monotone kernel, not for the exact non-monotone ones without extra lapse restrictions), its zero-field modulus fails at a homogeneous U = 0 leaf (a √ε response), and mixed heat-operator variations escape XC1/XC3's per-leg suppression — so the principal-symbol reduction to GR + BPS khronon is unproved and G4/G7/G8 stay conditional; the UV khronon is superluminal on the metric cone (4.4×10²–7.9×10⁵ c): requirement 7 must say which causality criterion it means (see the R2 proposal) |
| MOND kernel | ν_mono (≤ 0.01 dex from ν_RAR) + heat filter ξ — a different constitutive law from the spec's exact μ_exp | SPARC RAR 0.108 dex at Υ = 0.70 (`rar_framework_a0_mlfit.py`); Solar-System floors 0.031/0.045 pc | κ's value (input); whether the exact law can be carried by another constrained action |
| where MOND acts | bound-region kernel (L361, nonrelativistic, gate prescribed) + vacuum gate (L359, prescribed mask) | KiDS at the realizable profile, growth, forest; the Sun keeps the Galaxy's field | the gate's parameters are data-pinned (DE2), not derived; the gate is not yet varied in an action (its W′(U)δU terms feed the clock and metric equations); relativistic embedding |
| dark mass | kernel-invisible carrier, cold early, shed from galaxy halos at virialization with v_k ≈ 600–675 km/s (L365–L380) | S₈, forest, clearing, two-sided X-COP, cosmic shear (with the p = 2 gate), KiDS — pooled on fixed-cell clearing; Harvey: L381's merger check uses an active p = 1, x_c0 = 1.5 gate with p = 2, x_c0 = 2 retentions (lead-track peer review), so no same-cell Harvey verdict exists yet | no action for the trigger; the no-particle field (L374: condensate dust breaks at shell crossing; only a wave field passes, m ≳ 2–5×10⁻¹⁹ eV) |

## 5. The path to closure — four steps, in order

1. **Pin what the data can pin, from the framework's own gates** — done today for the vacuum gate (DE1/DE2: the linear
   gate p = 1, x_c0 ≈ 2.0–2.97, passes the four epochs). Next in the same spirit: re-run L380's pooled particle-mesh
   construction at (p = 1, x_c0 = 2.5) — its cluster, clearing and Harvey gates see the gate through the phantom the
   baryons feel.
2. **Give the dark mass a field and an action.** It is the open problem no construction has yet met at the action level
   (it is not the only one: see step 3). The field has to survive stream
   crossing (L374): the minimal ghost-condensate dust does not; a linear wave field does, but its quanta are light
   bosons (m ≳ 2–5×10⁻¹⁹ eV even with the clearing, L383), and whether such a field can be an excitation of the vacuum's
   own field rather than a new species is exactly what is open. Its shedding at virialization also needs a Lagrangian
   trigger (the record's is posited). The acceleration-triggered variant
   is being built in parallel (`acceleration_trigger_2026`, AT lanes).
3. **Assemble one action and run every gate on it** (recipe §12): C-H/K + kernel + filter + bound-region kernel +
   vacuum gate + the dark-mass field, one action ID, every proof package on that ID. The cheapest deciding piece, named
   by the lead track's audit: write the gate as a smooth factor W(U) on the MOND term, vary it (the extra
   L_M W′(U)δU terms enter the clock and metric equations; ∂U/∂K = −(2+2p)U/K at fixed curvature), and check the
   constraint structure and principal symbol on FRW and in one transition patch. The full list still open there:
   canonical classification, nonlinear well-posedness, full PPN of the assembled action, the filter's vertices, and the
   relativistic embedding of the region kernel. Never pool passes from different gate cells or action revisions.
4. **Let the data decide what no calculation can:** the z ≈ 2.5 deep-MOND rotator (flat vs ΛCDM's +0.33 vs a
   too-steep gate's Newtonian outer disc), Gaia DR4 wide binaries (γ_v; k04's environmental a₀ shifts it ~1σ), lensing
   edges r_e(z) ∝ E(z)^−(1+p) in stacked weak lensing at z = 0.2–1, and a DESI-type w(z) (the framework says the vacuum
   stays at −1).

## 6. What closure will and will not mean

A closed theory here is one action passing every gate with its inputs listed — not a theory with no inputs. The
inputs, as of today: κ (measured, provably not derivable in this action class), the dark mass's amount (an initial
condition, provably free), the filter length ξ, the clock couplings α_c and c₂ (bounded windows), the screening mass m,
the gate (p, x_c0) (pinned to a window by DE2), and the carrier's trigger and kick. What follows once those are fixed,
within the scopes stated above: the form of a₀ and its flatness in time (given the premise), c_T = 1 in the tested
tensor sector, static β = γ = 1 in the reduced khronometric sector, the MOND phenomenology in galaxies, and lensing =
dynamics in the static block. None of these is yet a property of one assembled, varied action.
