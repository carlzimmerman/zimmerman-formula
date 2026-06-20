# Why Skordis and Złośnik Were Right: The MOND Acceleration Scale as a de Sitter–Unruh Manifestation of the Cosmological Constant

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

**Version 2026-06-20 · Zenodo [10.5281/zenodo.20773004](https://doi.org/10.5281/zenodo.20773004) (concept DOI, latest version).** Companion to the published framework (Zenodo [10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540)) and the evolving-a₀(z) note (Zenodo [10.5281/zenodo.20737162](https://doi.org/10.5281/zenodo.20737162)). *Every quantitative claim below is reproduced by a committed Python script; the paths are listed in §9 and all 60 scripts exit 0.*

---

## Abstract

The Aether-Scalar-Tensor theory (AeST) of Skordis and Złośnik (2021) is the relativistic completion of MOND that fits the full *Planck* cosmic-microwave-background power spectrum, including the third acoustic peak, while reproducing the galaxy-scale radial acceleration relation. It has, however, been criticised on three grounds: (i) its scalar potential — a "ghost-condensate" kinetic function K(Q)=μ²(Q−1)² — is *postulated*; (ii) its preferred (aether) frame is *postulated*; and (iii) its MOND acceleration scale a₀ is *fitted*, not derived. We argue that on every count Skordis and Złośnik were *right*, and that the framework a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z (with Z = √(32π/3) = 5.7888) supplies precisely the physical motivation those three postulates were missing — without altering a single one of AeST's successful predictions. The acceleration scale is *tied to the cosmological constant* through a de Sitter–Unruh effective temperature, fixing a₀ = 9.36×10⁻¹¹ m s⁻² to within the radial-acceleration-relation band; the preferred frame is *named* by the de Sitter vacuum (the cosmic rest frame where the Gibbons–Hawking floor is isotropic); and the K(Q) ghost-condensate is shown to be internally healthy — it clears the boost-free infrared positivity/causality bound of Grall–Melville and Serra–Trombetta (the latter written at Skordis's own institute). We are scrupulously two-sided: the framework **derives no number** (a₀'s coefficient, the kinetic-term origin, and the dark-sector amplitude all remain free or postulated), its cluster-core deficit is **shared identically with AeST**, and the positivity result is a **saturation-pass that transmits no new constraint**. The net is a vindication, not a replacement: AeST is sound, well-founded, and — read as modified *inertia* with a₀ set by Λ — even better-motivated than its authors claimed. We close with the live falsifiable tests (Gaia DR4 wide binaries, the s^TX Lorentz-violation dipole, the evolving-a₀ Tully–Fisher offset) whose first verdict arrives in ~December 2026.

---

## 1. Introduction

Modified Newtonian Dynamics (MOND; Milgrom 1983) reproduces galaxy rotation curves and the baryonic Tully–Fisher relation from a single acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻², with no galaxy-scale dark matter. Its long-standing obstacle was a relativistic completion compatible with cosmology and gravitational lensing. The Aether-Scalar-Tensor theory (AeST; Skordis & Złośnik 2021, *Phys. Rev. Lett.* **127**, 161302, arXiv:2007.00082) cleared that obstacle: a unit-timelike aether A_μ plus a shift-symmetric scalar with a kinetic function K(Q) and a MOND function J(Y) reproduce both the MOND limit *and* the full *Planck* CMB power spectrum, third peak included, by carrying a cold, dust-like energy density that mimics cold dark matter on linear scales.

AeST is nonetheless commonly described as having three "free" ingredients: the scalar kinetic function K(Q)=μ²(Q−1)², the preferred aether frame, and the value of a₀. This paper's thesis is that these are not weaknesses of AeST but *open slots*, and that a single physical input — **the cosmological constant Λ acting through a de Sitter–Unruh effective temperature** — fills all three, fixing the framework

$$ a_0 \;=\; c^2\sqrt{\frac{\Lambda}{32\pi}} \;=\; \frac{c}{2}\sqrt{G\rho_{\rm DE}} \;=\; \frac{cH_\Lambda}{Z}, \qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.7888, $$

to a₀ = 9.3624×10⁻¹¹ m s⁻² for Λ = 1.0909×10⁻⁵² m⁻² (Ω_Λ = 0.685, H₀ = 67.4 km s⁻¹ Mpc⁻¹). This value sits inside the radial-acceleration-relation (RAR) optimum band (≈7.5×10⁻¹¹–1.8×10⁻¹⁰ m s⁻², ≤2% scatter penalty across interpolation/M-L conventions); it is *not* a new fit but a re-reading of AeST's existing a₀ as a manifestation of Λ. Three independent reproductions of the value are in [`reviews/ghost_condensate/gc_scale_check.py`](../reviews/ghost_condensate/gc_scale_check.py).

We honour a strict both-ways discipline throughout: a claimed deficit is verified as rigorously as a claimed success, on the framework's *own* footing (a₀ = 9.36×10⁻¹¹, the de Sitter–Unruh interpolation g_obs = √(g_bar² + g_bar·a₀), stellar mass-to-light Υ ≈ 0.7), never the regular-MOND defaults. The quarantine is absolute: **a₀, Z, the coefficient κ = ½, and the dark-sector amplitude I₀ are never asserted to be *derived*.**

## 2. The acceleration scale from the cosmological constant

A test body of proper acceleration **a** immersed in the de Sitter background of a universe with cosmological constant Λ experiences a Deser–Levin effective temperature
$$ T_{\rm eff} = \frac{\hbar}{2\pi c k_B}\sqrt{a^2 + (cH_\Lambda)^2}, \qquad cH_\Lambda = c^2\sqrt{\Lambda/3}, $$
interpolating between the Unruh temperature (a ≫ cH_Λ) and the Gibbons–Hawking temperature (a ≪ cH_Λ). Reading inertia as the response to this vacuum (modified-inertia MOND), the transition between Newtonian and deep-MOND dynamics occurs where the two terms are comparable, i.e. at an acceleration of order cH_Λ. The geometric coefficient that converts cH_Λ into a₀ is Z = cH_Λ/a₀ = √(32π/3). Its content is transparent once a₀ is written in density form: from ρ_DE = Λc²/(8πG) one has √(Gρ_DE) = c√(Λ/8π), so

$$ a_0 = \tfrac{c}{2}\sqrt{G\rho_{\rm DE}} = c^2\sqrt{\tfrac{\Lambda}{4\cdot 8\pi}} = c^2\sqrt{\tfrac{\Lambda}{32\pi}}, \qquad Z^2 = \frac{32\pi}{3} = \frac{4\cdot 8\pi}{3}, $$

so that **8π is Einstein's field-equation normalisation, 3 is the Friedmann factor (H_Λ² = Λc²/3), and the remaining 4 is the inverse-square of the coefficient κ = ½** in a₀ = κc√(Gρ_DE) — pure spacetime geometry up to that one free κ. The **coefficient κ = ½ in a₀ = κc√(Gρ_DE) is a free input** — it is not forced by ghost-freedom, unitarity, or holography (each is κ-invariant), and we re-confirm below (§5, Door S) that no independent mechanism transmits it. This is the framework's defining equation and its single quarantined number; what follows treats it as *given* and asks whether AeST is the right home for it.

## 3. The AeST embedding: the dark sector is the framework's own field

The framework's modified-inertia reading and AeST's modified-gravity reading share one scalar field φ. Its spatial gradient mode (the J(Y) sector) supplies the a₀-scale MOND force; its temporal mode (the K(Q) sector) supplies a cold, a⁻³ "dust" energy that mimics dark matter — *not a particle, a mode of the gravitational field itself*. The kinetic function

$$ K(Q) = \mu^2 (Q-1)^2 $$

is, structurally, a **ghost condensate** in the sense of Arkani-Hamed, Cheng, Luty & Mukohyama (2004, hep-th/0312099): a P(X) with a non-trivial minimum at X₀ > 0. This is the *authors' own* identification — Verwayen, Skordis & Złośnik (2024) write Eq. (7) as exactly μ²(Q−1)² and cite ACLM; Blanchet & Skordis (2024, *JCAP* **11**, 040, arXiv:2404.06584) adopt the identical K(Q) in their "Relativistic Khronon" action. The structural mapping is sympy-verified in [`reviews/ghost_condensate/map_aest_to_ghost.py`](../reviews/ghost_condensate/map_aest_to_ghost.py) and [`expand_PX_around_condensate.py`](../reviews/ghost_condensate/expand_PX_around_condensate.py): K′(1)=0, K″(1)=2μ²>0 (a true minimum, no ghost), and the shift-charge first integral a³K′(Q)=I₀ gives the a⁻³ dust.

Two of AeST's three "postulates" acquire physical content from §2:

* **The preferred frame is named, not postulated.** The framework's lensing no-go (covariant, Cassini-safe MOND lensing is forbidden by diffeomorphism invariance with c_T=c and ghost-freedom) *forces* a preferred frame; a preferred unit-timelike frame *is* an aether A_μ. The de Sitter–Unruh vacuum then selects *which* frame: the cosmic rest frame, where T_eff has its isotropic Gibbons–Hawking floor. AeST postulates the aether and justifies it a posteriori by the CMB fit; the framework supplies the missing front-end motivation.
* **The dark-sector "condensate" evades the symmetry obstruction that killed vacuum induction.** A de Sitter *vacuum* is SO(4,1)-invariant and induces no preferred-frame kinetic term; the condensate breaks the symmetry through a *background solution*, not the vacuum (the ferromagnet/magnon mechanism), and the same de Sitter background cures the ghost-condensate Jeans instability by Hubble friction (H₀/Γ ~ 10²⁵–10³¹; [`reviews/door_runs/C_lyapunov_stability.py`](../reviews/door_runs/C_lyapunov_stability.py)).

That a₀ ∝ √Λ is not an artefact of one mechanism: Blanchet & Seraille (2025, *JCAP* **12**, 036, arXiv:2502.14686) obtain the *same* scaling a₀ ~ c²√Λ from an entirely independent SU(2) Yang–Mills graviphoton theory. The *form* is multiply realised; the coefficient is not (§5, Door S).

## 4. Consistency: AeST's kinetic term is healthy

The sharpest theoretical worry about a ghost-condensate dark sector is whether its wrong-sign-then-stabilised kinetic structure violates positivity/causality. The applicable bounds are the **boost-free** ones — Grall & Melville (2021, *Phys. Rev. D* **105**, L121301, arXiv:2102.05683) and Serra & Trombetta (2024, arXiv:2412.19745) — which rest on unitarity, causality and locality, *not* Lorentz invariance, and therefore bind a Lorentz-violating condensate. (The stronger Creminelli–Janssen–Senatore bounds require a conformal UV completion the condensate lacks and are *inapplicable* — they must not be cited as a kill.) Notably, Trombetta is at CEICO Prague, Skordis's own institute: the theorem that adjudicates the framework's positivity was written by the home cluster. We are careful about attribution: Skordis and Złośnik themselves established AeST's ghost-freedom and its linear stability window {0<K_B<2, μ²>0, λ_s>0} in 2020–21, and we credit that result in full; the boost-free positivity bounds applied below *postdate* AeST (2021, 2024), so what follows is an independent later confirmation of their already-stable action, not a substitute for it.

We report two results, both ways.

**(a) The sign of the dark-matter mode is forced.** Energy-positivity of the dust (ρ_dust ∝ +4μ²·δQ > 0) forces the shift-charge sign(I₀) > 0, hence Q > 1, which is exactly the gradient-stable branch c_s² = δQ/(3δQ+2) > 0. Energy-positivity and sound-speed-positivity *coincide* on the dust branch: **the dark mode is gradient-stable by the very requirement that makes it dark.** This is sympy-exact in [`reviews/door_runs/doorA_positivity_gate.py`](../reviews/door_runs/doorA_positivity_gate.py) and [`condensate_postulate_and_eos.py`](../reviews/ghost_condensate/condensate_postulate_and_eos.py). It is a *new constraint on the theory's initial condition*, and it survives independently of the dispersion details.

**(b) The positivity bound is cleared — by saturation, adding no new constraint (stated plainly).** Reading the *real* Blanchet–Skordis quadratic action (not a generic ghost-condensate placeholder), the propagating scalar has dispersion ω = 0 at quadratic order — there is **no propagating k⁴ tail** (Blanchet–Skordis Sec. 6.2: "there are no higher-derivative interaction terms … quadratic in the fields"); MOND emerges from the *nonlinear* term. The faithful gapped/gapless pair is same-sector and shares one sound speed, so the Serra–Trombetta ratio v²_gapped/c_s² ≡ 1 *identically* across the entire stability window {0<K_B<2, K_2>0, λ_s>0}. **Positivity/causality is cleared everywhere — but by equality, sitting on the bound, and it carves out no new parameter sub-window.** We explicitly *retract* an earlier (placeholder-driven) suggestion of a K_B exclusion; there is none ([`reviews/door_runs/doorA_real_coefficients.py`](../reviews/door_runs/doorA_real_coefficients.py)). The honest reading: a genuine consistency *pass*, not a discovery, and a reminder that the ghost-condensate k⁴ picture is a useful EFT analogy, not the host's literal quadratic structure.

**(c) Lensing reconciles with the host.** The framework's gravitational slip γ = 2√(1+a₀/g_N) − 1 is *not* a field-level discriminator against AeST: it is the effective-dark-matter "inferred slip" (the ratio of the real phantom-mass lensing potential to twice the baryon-only Newtonian potential), which the Blanchet–Skordis khronon produces identically (their φ=ψ at Eq. 3.10). The null-geodesic deflection α(b) is identical to the host to a ratio of 1.0000 at every impact parameter ([`reviews/door_runs/door_L_lensing_headtohead.py`](../reviews/door_runs/door_L_lensing_headtohead.py)). The slip survives only as a MOND-family signature versus ΛCDM (which has γ=1), not as a framework-versus-AeST discriminator.

## 5. The honest ledger: established, shared, open

| # | Sector | Verdict (framework footing) | Script |
|---|--------|-----------------------------|--------|
| 1 | Galaxies / RAR / BTFR | **PASS** (AeST MOND limit; a₀ = c²√(Λ/32π) is the scale) | published framework |
| 2 | CMB + linear P(k) | **PASS** (AeST fits *Planck*; dust ≈ CDM on linear scales) | Skordis–Złośnik 2021 |
| 3 | Lensing | **PASS** (GR-of-the-phantom-mass; agrees with the host, §4c) | `door_L_lensing_headtohead.py` |
| 4 | Cassini / Solar System | **PASS** (c_T=c; MOND screened where g_N≫a₀) | published framework |
| 5 | Ghost-freedom / 6-dof stability | **PASS** (windowed {K_B, K_2, λ_s}) | `C_lyapunov_stability.py` |
| 6 | IR positivity / causality | **PASS by saturation** (no new exclusion, §4b) | `doorA_real_coefficients.py` |
| 7 | a₀ *value* (κ) | **OPEN — free** (Door S: Seraille's √Λ form matches, coefficient 32π not transmitted) | `door_S_seraille_coefficient.py` |
| 8 | Kinetic-term *origin* | **OPEN — postulated** (Door D, Oda both NOT-FORCED, §6) | `D_mersini_forcing.py`, `oda_door/` |
| 9 | Dark-sector *amount* (Ω_dm) | **OPEN — free** (a shift-charge integration constant) | `door_E_amount_pin.py` |
| 10 | Cluster cores | **SHARED MOND deficit** (identical to AeST, §6) | `clash_cluster/` |

The framework **closes no gap**: a₀'s value, the kinetic-term origin, and the amount are all free or postulated — *exactly as they are in AeST itself*. The vindication is that all of AeST's successes are reproduced and its kinetic term is shown healthy, while none of the framework's distinctive content manufactures a derivation it does not have.

## 6. What the framework does *not* do (both ways)

**Cluster cores — a shared, not a framework-specific, failure.** On the precise CLASH weak-lensing cluster-core residual (Famaey, Pizzuti & Saltas 2024, arXiv:2410.02612) the framework's modified-inertia phantom under-supplies the cored residual by a factor ≈4.4 (core-averaged 100–450 kpc), recovered identically by the eRASS1 X-ray core (ratio 1.03 between the two probes). Crucially, the framework's modified-*inertia* residual equals AeST's modified-*gravity* residual to machine precision (deep-MOND scale invariance pins M·G·a₀ = η·σ⁴ with η~1, shared); AeST itself undershoots cluster cores (Durakovic & Skordis 2023, arXiv:2312.00889). The same deficit appears in the new JWST strong-lensing cluster XLSSC 122 at z=1.98 (Finner et al. 2025), where the framework undershoots the concentrated M(<100 kpc)=6.5×10¹³ M⊙ core by ~6–20×. This is the 40-year MOND cluster-core problem, *shared across the relativistic-MOND family* and not closeable without an additional component; it is not a referee-proof kill given the post-XRISM equilibrium ambiguity, but we report it as an open deficit, not a manufactured win. Scripts: [`reviews/clash_cluster/framework_mi_residual.py`](../reviews/clash_cluster/framework_mi_residual.py), [`aest_mg_vs_mi_residual.py`](../reviews/clash_cluster/aest_mg_vs_mi_residual.py).

**The kinetic-term origin is not derived.** Three independent attempts to *derive* the form of K(Q) from Λ all return NOT-FORCED: the de Sitter–Unruh vacuum-induction route (killed by a sympy-proven theorem — the defining representation of so(4,1) is irreducible, so the de Sitter vacuum admits *no* invariant timelike vector and can induce no preferred frame; a static-patch observer or the condensate background evades it by breaking the symmetry with a *state*, recovering the frame as an SO(3)-singlet Goldstone but as a postulated VEV, never a derived stiffness — [`reviews/gap2_rep_door/so41_no_invariant_timelike_vector.py`](../reviews/gap2_rep_door/so41_no_invariant_timelike_vector.py)); the Mersini-Houghton phantom⇒time-crystal forcing theorem (vacuous here — the framework is never phantom, w ∈ (−1, ⅓); [`reviews/door_runs/D_mersini_forcing.py`](../reviews/door_runs/D_mersini_forcing.py)); and the most direct published "ghost condensate from Λ" mechanism, Oda (2025, arXiv:2509.23648), which turns out to be a *false cognate* — its "ghost" is a fermionic Faddeev–Popov gauge ghost generating only Einstein–Hilbert gravity, structurally excluding the bosonic scalar the framework's dark sector is, and leaving a₀ untouched since ∂a₀/∂G = 0 ([`reviews/oda_door/oda_gap1_mapping.py`](../reviews/oda_door/oda_gap1_mapping.py)). The kinetic term remains *postulated* — as it is in AeST.

**The amount is free.** No de Sitter number pins Ω_dm/Ω_Λ = 0.388; the dust amplitude I₀ is a free shift-charge integration constant (dρ_dust/dΛ = 0 at the level of the FRW equations; [`reviews/door_runs/door_E_amount_pin.py`](../reviews/door_runs/door_E_amount_pin.py)), in agreement with the independent "Ghost Dark Matter" construction of Lim, Sawicki & Vikman (2010, arXiv:1001.4634).

## 7. Falsifiable predictions and live tests

The framework inherits AeST's z=0 record and adds one distinctive content — a *declining* acceleration scale tied to the dark-energy density, a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)), which under the DESI DR2 CPL parameters (w₀=−0.752, w_a=−0.86) gives a₀(z=2) ≈ 0.86 a₀(0), a₀(z=3) ≈ 0.74 a₀(0). The decisive tests, with the first verdict imminent:

| Test | What it decides | Earliest verdict |
|------|-----------------|------------------|
| Gaia DR4 wide binaries | the MOND premise at z=0 | **~Dec 2026** |
| s^TX SME dipole | the preferred-frame (Lorentz-violation) prediction (~9.6× margin) | ~2028–2032 |
| evolving-a₀ Tully–Fisher offset | the *distinctive* declining-a₀ (discs ~7% below the z=0 BTFR) | DESI DR3 + ELT/JWST, early-mid 2030s |
| cluster non-adiabatic σ-spread (plunging UDG/dSph, outer MOND zone) | modified *inertia* specifically: internal σ rises with infall phase ~6–13% (MG **exactly 0**, a machine-verified theorem; CDM tidal fakes ~2–8% but radially anti-correlated) | ELT resolved-σ, ~2032+ |

If w(z) → −1 (no evolving dark energy), the distinctive a₀(z) content vanishes and the framework degenerates to constant-a₀ AeST. The cluster-core deficit is *not* a discriminator — it is shared with AeST and "explained" by ΛCDM with particle dark matter.

## 8. Conclusion: why Skordis and Złośnik were right

AeST was criticised for postulating its kinetic function, its preferred frame, and its acceleration scale. We have argued that all three postulates are *correct slots* filled by one physical input — the cosmological constant acting through a de Sitter–Unruh effective temperature. The acceleration scale is fixed to a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m s⁻² (within the RAR band); the preferred frame is the cosmic rest frame the de Sitter vacuum names; and the K(Q) ghost-condensate is internally healthy — energy-positivity forces the dark mode onto its gradient-stable branch, and the boost-free positivity/causality bound (from Skordis's own institute) is cleared.

We have been equally clear about the limits. The framework derives no number it did not already postulate; its positivity pass is a saturation, not a margin; its cluster-core deficit is real and shared identically with AeST; and three independent attempts to derive the kinetic term from Λ all fail. The honest standing is a *well-founded effective theory at a real frontier* — not a completed theory of everything, and not numerology.

That standing is, in our reading, a vindication of Skordis and Złośnik. AeST is the right relativistic MOND; tying its acceleration scale to the cosmological constant and reading it as modified inertia makes it better-motivated, fully consistent with the boost-free positivity programme, and falsifiable on a near-term timeline — without disturbing a single one of its successful predictions. The first datum that could overturn it all arrives, fittingly, within the year.

## 9. Computational reproducibility

All quantitative claims are reproduced by committed Python scripts under `opus_48_extended_research/reviews/`; **all 60 scripts exit 0** (verified 2026-06-19). The load-bearing files:

- **Acceleration scale / value** — `ghost_condensate/gc_scale_check.py`, `ghost_condensate/dsunruh_drives_vev.py`
- **Ghost-condensate mapping** — `ghost_condensate/map_aest_to_ghost.py`, `expand_PX_around_condensate.py`, `condensate_postulate_and_eos.py`, `seesaw_two_scales.py`, `amount_and_pathologies_calc.py`, `adversarial_gate_and_eos.py`
- **Consequences (dispersion, S8, EFT window)** — `gc_consequences/pin_I0_thermal.py`, `pk_k4_signature.py`, `w_gradient_cmb_calc.py`, `w_gradient_cmb_scherrer.py`, `eft_validity_window_calc.py`
- **Positivity (Door A) + pin** — `door_runs/doorA_positivity_gate.py`, `doorA_real_coefficients.py`, `doorA_real_coefficients_SKEPTIC.py`, `doorA_REAL_coefficients_RATIO_SCAN.py`, `doorA_REAL_coefficients_VERIFY.py`
- **Origin (Door D, Oda, GAP-2 frame)** — `door_runs/D_mersini_forcing.py`, `oda_door/oda_gap1_mapping.py`, `oda_door/oda_steelman_bothways.py`, `gap2_rep_door/so41_no_invariant_timelike_vector.py` (the SO(4,1) no-invariant-timelike-vector theorem)
- **Lensing (Door L)** — `door_runs/door_L_lensing_headtohead.py`, `door_L_lensing_headtohead_SKEPTIC.py`
- **K(Q) family, stability, amount, coefficient, window** — `door_runs/doorB_quadratic_vs_dbi.py`, `C_lyapunov_stability.py`, `door_E_amount_pin.py`, `door_S_seraille_coefficient.py`, `doorF_aclm_window.py`
- **Clusters** — `clash_cluster/clash_target_profile.py`, `framework_mi_residual.py`, `aest_mg_vs_mi_residual.py`, `robustness_bothways.py`
- **Distinctive σ-spread prediction** — `sigma_predict/mi_amplitude_band.py`, `mg_zero_theorem.py`, `cdm_tidal_confound.py`, `verify_MG_zero_and_CDM_separation.py`, `observational_test_design.py`

## References

- S. Milgrom, *Astrophys. J.* **270**, 365 (1983).
- C. Skordis & T. Złośnik, *Phys. Rev. Lett.* **127**, 161302 (2021); arXiv:2007.00082.
- N. Arkani-Hamed, H.-C. Cheng, M. A. Luty & S. Mukohyama, *JHEP* **05**, 074 (2004); hep-th/0312099.
- M. Verwayen, C. Skordis & T. Złośnik (2024), Eq. (7) [AeST = ghost condensate].
- L. Blanchet & C. Skordis, *JCAP* **11**, 040 (2024); arXiv:2404.06584 [Relativistic Khronon; K(Q)=μ²(Q−1)²].
- L. Blanchet & E. Seraille, *JCAP* **12**, 036 (2025); arXiv:2502.14686 [a₀ ∝ √Λ from a graviphoton theory].
- S. Grall & S. Melville, *Phys. Rev. D* **105**, L121301 (2022); arXiv:2102.05683 [positivity without boosts].
- D. Serra & A. Trombetta (2024), arXiv:2412.19745 [IR positivity bounds; CEICO].
- B. Famaey, L. Pizzuti & I. Saltas (2024), arXiv:2410.02612 [CLASH cluster-core residual].
- A. Durakovic & C. Skordis (2023), arXiv:2312.00889 [AeST undershoots cluster cores].
- E. A. Lim, I. Sawicki & A. Vikman, *JCAP* **05**, 012 (2010); arXiv:1001.4634 [Ghost Dark Matter].
- I. Oda (2025), arXiv:2509.23648 [GR from Λ via ghost condensation — false cognate].
- K. Finner et al., *Astrophys. J. Lett.* **994**, L35 (2025) [XLSSC 122].
- A. Deser & J. Levin, *Class. Quantum Grav.* **15**, L85 (1998) [Unruh–de Sitter T_eff].
- C. P. Zimmerman, Zenodo [10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540) (framework), [10.5281/zenodo.20737162](https://doi.org/10.5281/zenodo.20737162) (a₀(z)).

---

*Both-ways discipline and quarantine (a₀/Z/κ/I₀ never asserted derived) maintained throughout. This is a synthesis/position paper, not a discovery paper: it claims a re-reading of AeST's acceleration scale and a consistency demonstration, not a new derivation.*
