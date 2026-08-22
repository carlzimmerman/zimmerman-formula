# The Candidate Action — CMC/York Relativistic MOND (minimal, EFE-as-input)

**Status: FROZEN MINIMAL CANDIDATE UNDER CLOSURE TESTING.** Not a validated theory.
The FIRST validation gate is the full Dirac count of THIS exact action (with η a_i a^i + Λ_CMC):
the result 2+0 is proven only for sub-formulations, NOT yet for this action — it could be 2+1.
This is the single frozen action from which every observable must be derived. No equation
enters a paper because it gives a desired limit; it enters because it follows from this action.

Distinctive novel content (scope honestly): **a₀ = κc√(Gρ_Λ)** (coefficient reframing; κ, Z
FITTED) and **a₀(z) = a₀,₀ H(z)/H₀** (derived, Z-independent — the one prediction, not a fit).
Everything else (MOND interpolation, AQUAL/QUMOND, the EFE, the screening) is standard
machinery being *used*. This is a modified-gravity effective field theory, not a TOE.

---

## §1. The frozen MINIMAL action (2026-08-22 — screening set aside; EFE = input)

Per Theorem 8 the EFE environment is NOT locally derivable while keeping 2+0, so the screening
sector (e, Ψ, L) is REMOVED from the core; the external field enters as a boundary datum, exactly
as in standard MOND. No screening field, no L, no vector E_i.

    S = S_grav + S_CMC + S_Φ + S_m

Gravitational sector (general spatially-covariant; coefficients λ, ξ, η FIXED by the constraint
analysis + c_T=1 + G_eff=G, NOT by phenomenology):

    S_grav = (c³/16πG) ∫ dt d³x N√h [ K_ij K^ij − λ K² + ξ ³R + η a_i a^i ],   a_i = D_i ln N

CMC sector (multiplier Λ_CMC):

    S_CMC  = (c³/16πG) ∫ dt d³x N√h Λ_CMC (K − q)     ⇒  K = q(t)

MOND scalar sector (μ_gal only — NO screening):

    y = D_iΦ D^iΦ / a₀²,   U_y = μ_gal(√y),   μ_gal(x) = x/√(1+x²)
    U(y) = √(y(1+y)) − arcsinh(√y)
    S_Φ = −(1/8πG) ∫ dt d³x N√h a₀² U(y)     ⇒  D_i[μ_gal(|DΦ|/a₀) D^iΦ] = 4πGρ

Matter (universal coupling to ONE physical metric; the map is DECLARED OPEN, not invented):

    S_m = S_m[g̃_μν, ψ_m],   g̃_μν = C(Φ,X) g_μν + D(Φ,X) ∇_μΦ ∇_νΦ
    weak-field ⇒ g̃_00 = g_00 − 2Φ/c² (leading PN); C, D UNSPECIFIED until lensing/PPN fixes
    them subject to c_T=1, G_eff=G.

EFE / Solar-System quadrupole: NOT a new field. Solve the SAME nonlinear Φ equation with
D_iΦ → g_{e,i} on the subsystem's outer boundary; Φ = Φ_e + φ linearises to
D_i(M^{ij} D_jφ)=4πGρ, M^{ij} = μ_e h^{ij} + 2μ_y D^iΦ_e D^jΦ_e/a₀², anisotropic part ∝ ê^iê^j
⇒ the quadrupole. The environment g_e is INPUT (Theorem 8).

**Set aside, NOT in core (tested):** Helmholtz screening (e,Ψ) [scalar-e is 2+0, but its EFE scale
L=r_M is a proven no-go, Thm 8]; curvature-adaptive selector ℓ = √a₀ √ℋ /(√6 𝒢^{3/4}), ℋ=|D_iD_jΦ|²,
𝒢=|DΦ|² [gives L=r_M locally — VERIFIED — but Dirac-untested, higher-derivative Ostrogradsky risk +
𝒢→0 singularity]. Optional extensions, revisited only if the input-EFE core proves insufficient.

Novel relations:

    a₀(q) = c q / Z ,   q_FLRW = 3H   ⇒   a₀(z) = a₀,₀ H(z)/H₀

Matter couples to ONE physical metric with weak-field g^phys_00 = −(1 + 2Φ/c²) (single
potential ⇒ G_eff = G; no additive second Newtonian source).

**Formulation note (honest):** the DOF proof in hand is for a scalar screening field e with its
own elliptic term S_e = −(1/8πG)∫N√h[½ D_ie D^ie + W]; the Helmholtz form above replaces that
with e ≡ |DΨ| and the λ_Ψ constraint. The scalar-e DOF is verified 2+0; the Ψ-formulation's
full constraint count is the open item in §5 step 3.

---

## §2. Field content and constraints

| Canonical pair            | Role                          | Time deriv? |
|---------------------------|-------------------------------|-------------|
| (h_ij, π^ij)              | metric — the ONLY propagating | yes (2 TT)  |
| q (global) ↔ York time    | CMC clock, sets a₀(t)          | global only |
| (Φ, P_Φ)                  | MOND potential (elliptic)      | no ⇒ P_Φ≈0  |
| (Ψ, P_Ψ), (λ_Ψ, P_λ)      | outer-field filter (elliptic)  | no          |
| L (+ its constraint)      | scale selector — see §5        | no          |

Auxiliary constraints C_Φ, C_Ψ, … are all intended second-class (0 propagating DOF each).
The final deliverable is **rank(C) on the physical branch ⇒ N_local = 2**, checked on the
dangerous surfaces y→0, y→∞, ε→0, ε→∞, A′→0, L→0.

---

## §3. Ingredient ledger (structural / derived / phenomenological / conjecture)

| Ingredient                    | Status                          | Backed by (committed) |
|-------------------------------|---------------------------------|-----------------------|
| CMC/York, q(t)                | STRUCTURAL candidate            | dof_deformed_cmc_2026.py |
| a₀ = cq/Z                     | DERIVED relation (Z fitted)     | cosmology_flrw_2026.py |
| a₀(z) = a₀,₀ H(z)/H₀          | DERIVED prediction, Z-indep     | cosmology_flrw_2026.py |
| N_tensor = 2, c_T = 1         | PROVEN (scalar-e formulation)   | stability_taskG_2026.py |
| G_eff = G (single potential)  | REPAIRED/verified               | referee_gateE_doublecount_2026.py |
| Modified LY elliptic + lapse  | PROVEN                          | modified_LY_verify.py, york_step2_closure_2026.py |
| H_⊥ Dirac–DeWitt algebra      | CLOSES                          | york_step2_closure_2026.py |
| U(y,ε) constitutive law       | EXPLICIT construction           | escreen_Q2_map_2026.py |
| Scalar elliptic e             | 2+0 candidate PROVEN            | york_efield_dof_2026.py (+crosscheck) |
| Helmholtz outer filter        | scale-separation VERIFIED       | cassini_widebinary_lock_2026.py (hand-checked) |
| L = r_M as a LOCAL field      | 🔴 PROVEN NO-GO (breaks 2+0)     | york_Lclosure_global_2026.py, york_Lclosure_dirac_2026.py |
| L = r_M as per-system input   | works, but NOT a closed theory  | (same status as MOND's g_ext input) |
| ε_s, m                        | PHENOMENOLOGICAL parameters     | need independent calibrator |
| γ_PPN = 1 / lensing           | 🔴 engineered, NOT derived       | OPEN |
| wide-binary γ_v               | branch-dependent PREDICTION     | escreen_widebinary_fork_2026.py |
| cosmological evolution a₀(z)  | genuine PREDICTION              | — |

---

## §4. Theorem / Proposition / Prediction structure

Statements are labeled DERIVATION (math, script-backed) or PREDICTION (empirical) or OPEN.

- **Theorem 1 (CMC acceleration scale).** K = q(t) ⇒ a₀ = cq/Z.  DERIVATION ✅
- **Theorem 2 (cosmological scaling).** q_FLRW = 3H ⇒ a₀(z) = a₀,₀ H(z)/H₀, Z-independent.
  DERIVATION ✅ (cosmology_flrw_2026.py)
- **Theorem 3 (constraint count).** The auxiliary sector is second-class ⇒ 0 propagating DOF;
  N_local = 2.  PROVEN for the scalar-e formulation; OPEN for the full (Φ,Ψ,λ,L) system.
- **Proposition 4 (isolated MOND limit).** e→0 ⇒ A→1 ⇒ μ_eff→μ_gal ⇒ g² = a₀ g_N.
  DERIVATION ✅
- **Proposition 5 (screened Solar-System branch).** ∃ (ε_s,m) with Q₂ < Q₂,Cassini.
  DERIVATION ✅ *as a parameter window* (escreen_Q2_map_2026.py) — NOT yet from a solved (e,Ψ,L).
- **Prediction 6 (stellar-scale screening).** γ_v = γ_v(r/L_⋆) — SEPARATION-DEPENDENT, not a
  single value.  PREDICTION (conditional on the screened-bubble picture; OPEN).
- **Prediction 7 (cosmological evolution).** a₀(z) ∝ H(z).  PREDICTION — the falsifiable
  centerpiece; distinguishes this from constant-a₀ MOND and ΛCDM.
- **Theorem 8 (EFE-scale no-go).** The internal/external separation scale L = r_M CANNOT be a
  single-valued local functional of ρ fixed by the action while preserving 2+0.  DERIVATION ✅
  (york_Lclosure_dirac_2026.py, york_Lclosure_global_2026.py). Three legs: (i) global M[ρ]=∫ρ
  grows ∝R^{3/2} with no stopping scale → L≈r_M(MW) → filters the external field as internal →
  Q₂ = 1.8e-26 > Cassini by 3.5×; (ii) the local self-consistent root L²a₀=GM(<L;x) is
  multivalued (3 roots at the Sun in the Sun⊂dwarf⊂MW test; ×200 swing from ρ's coarse-graining
  which the action does not fix) because r_M needs a *segmentation* of ρ into objects, not a
  field functional; (iii) exact Dirac: det H ∝ (2La₀−GM_L)², so the entry f′(L) enters squared
  and vanishes on a codim-1 tangency locus (shell Σ crosses a₀/G) → (L,P_L) turns first-class →
  +1 scalar DOF; the nonlocal ball-integral form factor F(kL) has infinitely many zeros (not
  ghost-free). Only the global L keeps 2+0, and it is Cassini-dead. **Consequence:** the EFE
  environment is an *input* (as in all MOND), not derivable locally within this class.

---

## §5. The closure sequence (locked order — do NOT run all at once)

Rule: once the action is frozen, ALL observables are computed from it. Do not re-optimize the
action against a failed test; record failures in the ledger, don't patch them invisibly.

1. **Write one complete action** — ✅ this document.
2. **Derive every constraint** — mostly done (scalar-e); redo for the frozen (Φ,Ψ,λ,L) form.
3. **Prove 2+0 globally** — on the FULL system, on the dangerous surfaces (§2). PARTIAL.
4. **Derive the scale-selector L** — ✅ RESOLVED as **Outcome C: NO-GO** (Theorem 8). L=r_M
   cannot be a local action-determined field while keeping 2+0. The EFE environment is an input,
   not locally derivable. Remaining alternatives are (B) a covariant *nonlocal* selector (hard —
   the natural ball-integral form is not ghost-free) or accepting L as a per-system boundary
   datum (then Cassini is a parameter window / DR4-arbitrated tension, NOT a closed local fix).
   ⇒ steps 5–6 (local Q₂/homogenization closure) are moot for a LOCAL theory; skip to the
   derived-core paper.
5. **Solve the full Solar-System Q₂** with (e,Ψ,L) SOLVED, not assigned.
6. **Homogenize the stellar bubbles** — derive μ_coarse(g) from the microscopic screened
   bubbles (a homogenization problem, not just Gauss's law); check the RAR survives.
7. **Fit the galaxy RAR** — one universal (Z, ε_s, m); compare the residual distribution to
   SPARC, not just the mean.
8. **Predict wide binaries** — the full γ_v(r) curve over 10²–10⁵ AU; fit the whole
   distribution ONCE, never tune to a preferred analysis.
9. **Derive lensing** — g^phys potentials Φ_N + Ψ_N (light deflection) with NO implicit dark
   matter.  Likely the hardest relativistic gate.
10. **Derive cosmological perturbations** — the SAME action must give w_eff(z), H(z),
    G_eff(z), Σ(z); no borrowing GR cosmology on top of a phenomenological a₀(z).
11. **Adversarial suite** — ghost, gradient, strong coupling, PPN, binary pulsars, GW,
    lensing, clusters, cosmological perturbations, RAR, Q₂, wide binaries, and every prior
    no-go route.
12. **Freeze and let independent data decide.**

---

## §6. Non-claims and live gates (state up front, always)

- κ = ½ and Z ≈ 21 are **fitted**, not derived. Only a₀ ∝ H(z) is predicted.
- L = r_M is **proven NOT locally derivable while keeping 2+0** (Theorem 8). The EFE
  environment is an input, exactly as in standard MOND — not worse, but not derived. A local
  screening field cannot close Cassini; that route is a proven dead end, not a pending calc.
- γ_PPN = 1 / lensing = dynamics is currently an **engineered coupling**, not an output.
- ε_s, m are **phenomenological** until each has an independent (non-Cassini) calibrator.
- Cassini is passable **as a parameter window**; the wide-binary casualty is real but is now a
  *prediction* (separation-dependent γ_v), consistent with QC-clean Newtonian samples.
- The CMC sector (→ a₀(H)) and the elliptic screening sector (→ local hierarchy) are kept
  **conceptually separate**; CMC does NOT cancel the EFE (δK=0 no-go).

Until steps 4, 9, 10 close, this is a **candidate theory under closure testing.**
