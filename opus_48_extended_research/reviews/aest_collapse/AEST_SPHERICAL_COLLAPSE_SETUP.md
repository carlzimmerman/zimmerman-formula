# Spherical-collapse-with-AeST: the formalism + setup

*Setup/derivation pass for the open door left by the static BVP (banked `wn6n716aa`,
AEST_NONLINEAR_PHI_CLUSTER_2026-06-20). The static spherical-boundary-value problem leaves the AeST
oscillation phase (equivalently χ∞ / the boundary constant Δ) FREE; the cluster boost is therefore
DESCRIPTIVE not predictive. THE QUESTION this setup targets: does **dynamical collapse from cosmological
ICs through turnaround + virialization** PIN that phase — and if so, to a boost, universally, galaxy-safely?
This file DERIVES + SETS UP the 1+1D (radius × time) spherical-collapse-with-AeST solve; it does not yet
run it. Both-ways, quarantine held (a0/Z/κ/I0 never derived here — a0=9.36e-11 is an INPUT throughout).*

---

## 0. What the static result established (the thing to dynamically test)

The exact static weak-field AeST equation (Durakovic–Skordis 2024 = "DS24" Eq 2.40; Blanchet–Skordis 2024
Eq 3.21; reduced from Verwayen–Skordis–Bœhm 2024 = "VSB24" Eqs 2-4) is the **modified Helmholtz equation**

  (1/r²) d/dr[ r² M(x) Φ′ ] + µ̃² Φ = 4πG_N ρ_b ,   x ≡ |Φ′|/a₀ ,   M(x) = (√(1+4x) − 1)/(√(1+4x) + 1)

with µ̃² ≡ (1+β₀) µ², β₀ ≡ 1/λ_s. In the large-gradient (Newtonian/strong) limit M→1 it becomes the pure
Helmholtz equation ∇²Φ + µ̃²Φ = 4πG_N ρ_b, whose **homogeneous solutions are oscillatory**:

  Φ_hom(r) = C₁ cos(µ̃ r)/r + C₂ sin(µ̃ r)/(2 µ̃ r)      (DS24, §2.3.5)

Pure AQUAL/MOND (µ=0) is shift-invariant — only ∇Φ appears, so the absolute level of Φ is unphysical. The
**+µ̃²Φ term breaks that shift symmetry**, so the asymptotic level χ∞ (≡ the boundary constant on the
oscillatory branch) becomes physical and feeds a phantom source ρ_eff = −µ̃²Φ/4πG. The static BVP fixes
Φ only up to the **one-parameter family** {C₁,C₂} (equivalently DS24's boundary parameter Δ / χ̂_out): a
GIVEN cosmological χ∞ is reached at MANY oscillation phases → η(R500) from −3.12 to +3.97. **The phase is
the free knob the static problem cannot close.** Dynamical collapse is the only physics that can fix it.

KEY: µ̃ is CMB-pinned to µ⁻¹ ≳ 1 Mpc (SZ2021; Mistele et al. 2023 lower bound from flat-RC extent). So
(µr)² ≪ 1 in galaxies (kpc) but O(1) at cluster R500 (Mpc) — the boost is GEOMETRIC, protecting galaxies.

---

## 1. The AeST cosmological background + the origin of χ∞ (the physical boundary)

From Skordis–Zlosnik 2021 (= "SZ2021", arXiv:2007.00082) the action is
  S = ∫d⁴x √−g/(16πG̃) [ R − (K_B/2)F^{µν}F_{µν} + 2(2−K_B)J^µ∇_µφ − (2−K_B)Y − F(Y,Q) − λ(A²+1) ] + S_m
with Q ≡ A^µ∇_µφ, Y ≡ q^{µν}∇_µφ∇_νφ, q^{µν}=g^{µν}+A^µA^ν, F^{µν}=2∇^[µA^ν], J^µ=A^α∇_αA^µ.

**Background (FLRW, A^µ=(1,0,0,0), φ=φ̄(t), Y=0, Q=Q̄=φ̄̇):** define K(Q̄) ≡ −½F(0,Q̄). Shift-symmetric
k-essence requires K to have a minimum at Q̄=Q₀≠0:  K = −2Λ + K₂(Q̄−Q₀)² + …  (SZ2021 Eq 4). The scalar
EOM integrates once to dK/dQ = I₀/a³, giving

  **Q̄(a) = Q₀ + I₀/a³ + …**,    ρ̄_AeST = ρ̄₀/a³ + …,   8πG̃ρ̄₀ = Q₀ I₀.       (SZ2021 "Cosmological observables")

So the AeST scalar is **dust-like**: φ̄ ≈ Q₀ t at late times, displaced by the decaying I₀/a³ piece set by
the initial condition I₀ (= Ω_AeST, the framework's I₀ knob — quarantined, never derived). The Helmholtz
mass is set by the SAME background:

  **µ² = (2K₂/(2−K_B)) Q₀²**       (SZ2021 weak-field reduction; DS24 §2.3).

**This is the crux of the whole door:** χ∞ is NOT an arbitrary integration constant — physically it is the
**value of the cosmological scalar perturbation χ(t) (SZ2021 Eq 7, χ ≡ ϕ + φ̄̇ α) evaluated at the cluster's
location and epoch**, i.e. the large-scale environment into which the cluster's quasistatic solution must
asymptote. The static BVP treats χ∞ as free precisely because it discards the time-dependence that the
COSMOLOGICAL χ(t) evolution would supply. The question "does collapse pin the phase?" = "does the
time-dependent χ field, sourced by the evolving collapse density on top of the cosmological χ(t)
background, converge to a unique oscillation phase at virialization?"

---

## 2. (1) Collapse equations — the onion-shell fluid with MOND-boosted infall + Hubble drag

Standard spherical-collapse reduction (Malekjani–Rahvar–Haghi 2008 arXiv:0811.1833, building on Sanders
2001, Nusser 2002): divide the top-hat overdensity into N co-centric shells ("onion model"); each shell
i has comoving-anchored Lagrangian radius r_i(t) enclosing fixed baryon mass M_i. No shell crossing (inner
shells collapse first), so M_i is conserved per shell.

**Background (the embedding cosmology):** flat ΛCDM-like AeST FLRW (the AeST dust replaces CDM in the
background), H(a)² = H₀²[Ω_b a⁻³ + Ω_AeST a⁻³ + Ω_Λ], with Ω_AeST set by I₀ (≈Ω_dm to match CMB; SZ2021).
The cluster forms inside this expanding background.

**Per-shell equation of motion (physical radius r_i, cosmic time t):**

  r̈_i = − g(r_i, t)        [no explicit 2H ṙ drag term — Hubble drag enters through the EXPANSION-set
                             initial velocity v_ent = H_ent r_ent (1−δ_ent), the standard onion convention,
                             eqn (10)–(11) of MRH08; the shell decelerates relative to background as it
                             turns around]

where g is the AeST/MOND gravitational acceleration sourced by the enclosed baryons **and the AeST phantom
mass** (this is the new ingredient vs pure-MOND collapse). In the pure-MOND deep regime MRH08 use the
closed form r̈_i = −√(G M_i a₀)/r_i (their Eq 10). For AeST we must instead read g off the field solve at
each step (§3): g(r_i,t) = +Φ′(r_i,t) from the AeST Eq-2.40 solution on the instantaneous density profile.

**MOND/AeST acceleration, general regime:**
  g_N(r) = G M_baryon(<r)/r² ;   g = g_N · ν(g_N/a₀)  in the algebraic limit, with the framework's OWN
  dS–Unruh interpolation g = √(g_N² + g_N·a₀)  (MEMORY rule — use the framework's ν, NOT McGaugh's, when
  judging the framework). For the FIELD solve we do not use the algebraic ν; we solve Eq 2.40 directly,
  which contains M(x) and the +µ̃²Φ phantom term self-consistently. The algebraic ν is the µ=0 check.

**Critical (MOND-entry) radius** separating Newtonian (r>r_c) from MOND (r<r_c) domains, MRH08 Eq 8–9:
  r_c = 3a₀ / [4πG(ρ+3p)]  →  r_c = 2a₀ / [H₀²|Ω_b a⁻³ + 2Ω_r a⁻⁴ − 2Ω_Λ|].
  A shell switches dynamics from linear-Newtonian growth to MOND/AeST when its size λ_i drops below r_c
  (equivalently when its internal g falls below a₀). Entry time t_ent^i, radius r_ent^i, velocity
  v_ent^i = H_ent r_ent^i (1 − δ_ent^i) are the per-shell initial data for the nonlinear phase.

**Turnaround:** r_max^i where ṙ_i = 0. Deep-MOND closed form (MRH08 Eq 11):
  r_max^i = r_ent^i · e^{α_i},   α_i = (v_ent^i)² / (2√(G M_i a₀)).
**Virialization:** energy conservation E = ½(v_ent^i)² + √(GM_i a₀) ln r_ent^i set equal to the virial
condition ½ r dV/dr + V = E with MOND potential V(r) = √(GM_i a₀) ln r (MRH08 Eqs 12–14):
  r_vir^i = r_ent^i · e^{α_i − ½}   (MOND branch; valid when α_i>½, i.e. 2T_ent/W_ent>1, which MRH08 find
  holds for all shells → all virialize in the MOND regime). The cluster "appears" (virializes) over a
  spread of redshifts, inner shells first.

**In AeST (the modification):** V(r) and g(r) are NOT the closed MOND forms — they include the +µ̃²Φ
phantom contribution, which is exactly the term whose oscillation phase we are tracking. So r_max, r_vir
must be obtained by integrating r̈_i = −g_AeST(r_i,t) with g_AeST from the field solve, NOT the closed
formulae. The closed MOND formulae are the **µ=0 validation limit** (solver must reproduce them to ~1e-6,
as the static solver already does).

---

## 3. (2) The AeST field equation solved at each time step + how χ∞ is set dynamically

At each time t the collapse provides an instantaneous spherical baryon profile ρ_b(r,t) (from the shell
positions r_i(t) and masses M_i, via mass conservation / Jacobian — MRH08 Eq 15ff). We must solve the AeST
field for Φ(r,t), χ(r,t) on top of the EVOLVING cosmological background. Two solve modes:

**(3a) QUASISTATIC-at-each-step (leading approximation, the tractable load-bearing version):**
At each t, solve the static DS24 Eq 2.40 BVP on ρ_b(r,t):
  (1/r²) d/dr[ r² M(x) Φ′ ] + µ̃²(t) Φ = 4πG_N ρ_b(r,t),   x=|Φ′|/a₀,
with µ̃²(t) frozen at its (essentially constant, late-time) value µ̃² = (1+β₀)(2K₂/(2−K_B))Q₀². The OUTER
boundary at the cluster's turnaround/infall radius r_ta(t) is set NOT freely but by **matching Φ(r_ta,t) and
Φ′(r_ta,t) to the cosmological χ-field** χ_cosmo(t) evolved from SZ2021's linear perturbation equations
(§3c). This is the change from the static BVP: the outer boundary is an OUTPUT of the cosmological χ(t)
evolution + the collapse history, not a free input. The Hamiltonian reformulation (DS24 §3, VSB24) is
needed numerically because oscillating Φ makes |Φ′|=0 points singular in the 2nd-order form — recast
Eq 2.40 as first-order Hamilton equations for (Φ, P_Φ).

**(3b) FULLY TIME-DEPENDENT field (the rigorous version, harder):**
Restore the time derivatives dropped in the quasistatic limit. The weak-field AeST action (SZ2021 Eq 6)
before dropping φ̇:
  S = −∫d⁴x (2−K_B)/(16πG̃) [ |∇Φ|² − 2∇Φ·∇ϕ + |∇ϕ|² − µ²Φ² + J(Y) ] + Φρ
gives, restoring ∂_t (the χ mode obeys a wave equation with mass µ — Klein–Gordon-like), a hyperbolic
system whose homogeneous solutions oscillate in BOTH space (Helmholtz, wavelength 2π/µ̃) AND time
(frequency ~µ̃ c). The collapse density acts as a moving source. This is the regime VSB24 / "price of
abandoning dark matter is nonlocality" (Blanchet–Marleau–Skordis 2024) flag: the time-dependent oscillatory
field has memory — its phase at virialization depends on the whole collapse trajectory, not just the
instantaneous density. THIS is where dynamical phase-pinning would (or would not) happen.

**(3c) The cosmological χ(t) outer boundary (where χ∞ comes from):**
SZ2021 linear perturbations give the evolution of the scalar perturbation χ ≡ ϕ + φ̄̇ α (SZ2021 Eq 7) and
the vector mode E with (SZ2021 Eq 12):
  K_B(Ė + HE) = (dK/dQ)χ − (2−K_B)[ (φ̄̇/(1+w))Π + (H+φ̄̇)χ − 3c_ad²Hφ̄̇α ].
Together with the fluid eqs (SZ2021 Eqs 9–11, nonstandard pressure Π). On large scales this χ_cosmo(t,k→0)
is the value the cluster's local Φ must asymptote to — i.e. χ∞(t) = χ_cosmo evaluated at the cluster
environment. The collapse perturbs χ locally; the question is whether the local solve relaxes to a
phase locked to χ_cosmo (pinned) or retains a free oscillation phase (not pinned).

---

## 4. (3) The phase diagnostic — how χ∞ / the phase is read off the dynamical solution

Define the diagnostic the solver must track as the system virializes:

**(i) Oscillation phase θ(t).** On the oscillatory branch r>r_C, fit Φ(r,t) to A(t) cos(µ̃ r + θ(t))/r over
the µ-dominated region. θ(t) (equivalently the boundary constant Δ(t) via DS24 Eq 20, χ̂_out = χ̂_out^max
+ Δ) is the free phase. **Pinned ⟺ θ(t) → θ* converges to a unique value as the shells virialize,
INDEPENDENT of how the collapse was seeded.**

**(ii) χ∞(t) = the matched asymptotic level** Φ(r→r_ta, t) on the oscillatory branch, normalized
χ̂_out = χ(r̂_M)/√(G M a₀) (DS24 §2.2.2). Track χ̂_out(t) vs the cosmologically-evolved χ_cosmo(t).

**(iii) The boost η(R500, t) ≡ M_total^AeST(R500)/M_baryon(R500) − 1** (the phantom-mass enhancement, DS24
Eq 3.48–3.50), the observable the door turns on. η>0 boost, η<0 deficit. Static result: η∈[−3.12,+3.97]
across phases; natural untuned Δ=0 gives η=−1.54 (deficit).

**Convergence tests (the actual yes/no):**
- **(C1) Phase convergence:** does θ(t)→θ* as t→t_vir, with dθ/dt→0? Plot θ(t) and Δ(t) through turnaround
  and virialization. A late-time plateau = pinned; persistent drift / sensitivity = unpinned.
- **(C2) IC-independence (the decisive test):** run an ensemble of ICs — vary the initial overdensity
  amplitude δ_ent (cluster mass 1e14–1e15 M☉), the profile shape (top-hat vs NFW-progenitor vs Hernquist),
  the random infall realization, and the I₀/Ω_AeST background within CMB-allowed range. If θ* is the SAME
  across the ensemble → universally pinned. If θ* tracks δ_ent / mass / profile → IC-dependent = NOT pinned
  (the static no-go holds dynamically). **MEMORY rule: a "pinned" claim must be as rigorously verified as an
  "unpinned" claim — robustness to ICs is the load-bearing check.**
- **(C3) Boost-vs-deficit sign:** is θ* a BOOST phase (η(R500,θ*)>0, ideally η~+2 to close clusters) or the
  deficit branch (η<0)? Report the sign and magnitude the dynamics actually select.
- **(C4) Galaxy veto:** run the SAME collapse machinery on a GALAXY-mass progenitor (1e11 M☉, kpc scale).
  If the dynamics pin a boost phase for galaxies too, it leaks into the RAR (>0.05 dex breaks). The door
  reopens ONLY if collapse pins a boost at clusters AND leaves galaxies MOND-clean (the (µr)²≪1 geometric
  protection must survive the dynamical phase selection). Static check: universal χ∞ that fixes clusters
  gives +0.275 dex at galaxies = breaks 5.5×. The dynamical question is whether the SELECTED phase is
  scale-dependent in exactly the protective way.
- **(C5) Cassini:** the selected phase must keep the solar-system anomaly < PPN |γ−1|<2.3e-5 (static solve:
  margin ~2.3e4×, geometric (µr)²~1e-30 at 10 AU — essentially automatic, but verify the dynamical phase
  doesn't pathologically amplify near the source).

---

## 5. (4) Initial conditions

**Background cosmology:** AeST FLRW with H₀=67–75, Ω_b≈0.05, Ω_AeST≈0.25 (set by I₀ to match CMB dust;
quarantined), Ω_Λ≈0.69, a₀=9.36e-11 m/s² (framework INPUT, c²√(Λ/32π)). µ⁻¹ = 1 Mpc (CMB/flat-RC pinned;
also run µ⁻¹∈[0.5,2] Mpc as a robustness band). λ_s→∞ (β₀=0, totally-screened "simple" interpolation, the
DS24 default) and a finite-λ_s robustness run.

**Cosmological perturbation seed:** top-hat (or NFW-progenitor) overdensity δ_i(z_dec) drawn at last
scattering from CMB-amplitude fluctuations (MRH08 use the LSS CMB anisotropy amplitude). Linear-Newtonian
growth δ∝a from z_dec until each shell enters the MOND/AeST regime (r_c-crossing). This sets the per-shell
entry data (t_ent, r_ent, v_ent, δ_ent) — Table-1 style in MRH08.

**AeST scalar IC:** χ_cosmo(z_dec) and its evolution from SZ2021's adiabatic initial conditions for the
scalar/vector modes (ϕ, α, E), evolved by the linearized SZ2021 equations to provide χ∞(t) = the outer
boundary the cluster solve matches to. The decaying displacement I₀/a³ sets ρ̄_AeST and µ (quarantined).

**Cluster masses for the ensemble (C2):** M ∈ {1e14, 3e14, 1e15} M☉ (cluster) + 1e11 M☉ (galaxy veto, C4).
Profiles: top-hat, Hernquist (baryon), NFW-shaped progenitor. Several random infall realizations each.

**Numerical:** 1+1D grid (radius r ∈ [r_core, ~3–7 R500], time/scale-factor a ∈ [a_dec, 1]); N≈10–50 onion
shells; field solve via the DS24/VSB24 Hamiltonian first-order recast (Φ, P_Φ) to avoid the |Φ′|=0
oscillation singularity; adaptive time-stepping through turnaround. Validation: µ=0 must reproduce the
analytic MOND collapse (MRH08 Eqs 10–14, r_max/r_vir closed forms) to ~1e-6, and the static (frozen-ρ)
limit must reproduce the banked aest_phi_cluster_solve.py η(R500) curve.

---

## 6. (5) Key facts / what this setup commits to (and the honest scope)

See `key_facts` in the structured return. Headline: this is the standard spherical-collapse (onion-shell)
reduction PLUS the AeST field solved at each step, with the outer boundary supplied by the cosmological
χ(t) instead of being free — the minimal honest test of the phase-pinning question. A full 3D cosmological
AeST N-body (which would settle it definitively) is research-group-scale and NOT producible here; the 1+1D
solve is the tractable load-bearing version. The quasistatic-per-step mode (3a) is the first build; the
fully time-dependent field (3b) is the rigorous follow-up where genuine dynamical phase memory lives.

## Sources
- Skordis & Zlosnik 2021, "New Relativistic Theory for MOND", PRL 127 161302, arXiv:2007.00082 (action Eq 5;
  background K(Q) Eq 4; Q=Q₀+I₀/a³; weak-field+µ² Eq 6; cosmological perturbations Eqs 7–12).
- Verwayen, Skordis & Bœhm 2024, MNRAS 531 272, arXiv:2304.05134 (static weak-field Eqs 2–4; M(x); rC, χ̂_out,
  Δ boundary parameter Eqs 19–21; three regimes Newton/MOND/µ-domination).
- Durakovic & Skordis 2024, JCAP 04 040, arXiv:2312.00889 (reduced single-field Eq 2.40; M(x) Eq 2.39;
  oscillatory homogeneous solution §2.3.5; phantom mass Eqs 3.48–3.50; RAR peak vs deficit; isothermal cluster).
- Blanchet & Skordis 2024, arXiv:2404.06584 (covariant matter action, Eq 3.21 mass term).
- Blanchet, Marleau & Skordis 2024 ("price of abandoning dark matter is nonlocality") — time-dependent
  oscillatory field / nonlocality of the boundary.
- Malekjani, Rahvar & Haghi 2008, arXiv:0811.1833 (onion-shell MOND spherical collapse: Eqs 5–15, r_c,
  r_max, r_vir, virialization in MOND regime) — building on Sanders 2001 & Nusser 2002 (peculiar-accel MOND
  collapse, Jeans-swindle 1D hydro). MEMORY rule: use the framework's OWN dS–Unruh ν, a₀=9.36e-11.
