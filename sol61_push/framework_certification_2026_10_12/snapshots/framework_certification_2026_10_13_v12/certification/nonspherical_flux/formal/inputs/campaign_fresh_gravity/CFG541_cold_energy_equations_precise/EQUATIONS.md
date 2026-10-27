# CFG541 EQUATIONS: the cold-energy equations of motion, class A, Newtonian limit

Status: **SPECIFIED WITH OPEN ITEMS** (the list is in section 8). Every number quoted here is in `cfg541_results.json`, written by
`cfg541.py`. The criteria are in `FROZEN_CRITERIA.md` (09e5d0a18).

κ = ½ is fitted. The cold energy's mass is still required: its amount, Ω_c/Ω_b = 5.364, is an input. No dark-matter particle
species is added. This is not a closed theory.

This file writes CFG539's surviving class A as one complete system. It changes one thing in CFG539's committed form: the census
edge is taken out of the deficit (section 4 gives the reason).

---

## 0. Conventions

- Newtonian limit, physical coordinates, SI units.
- For a cosmological box, use comoving x with the usual a(t) factors, and put ρ − ρ̄ in the Φ equation. The ψ equation keeps an
  isolated (free-space) Green's function per catchment, as described in (E6).
- Units: [M] kg, [L] m, [T] s.

## 1. Constants and their origin

| symbol | value / definition | origin | status |
|---|---|---|---|
| G, c | Newton's constant, speed of light | physics | — |
| ρ_DE | dark-energy density | cosmology input | input |
| κ | ½ | fitted (A2) | **FITTED** |
| a₀ | κ c √(G ρ_DE): 9.3603e-11 (can) or 1.1312e-10 (alt) m s⁻² | A2; two footings, never pooled | follows from κ, ρ_DE |
| ν(y) | 1/(1 − e^(−√y)) | A1 (ν_mono) | the kernel is an experimental variable |
| f_b | Ω_b/(Ω_b + Ω_c) = 0.02237/0.14237, so (1 − f_b)/f_b = 5.364 | A4 | input |
| Δ_ta(z) | mean overdensity at turnaround from the spherical-collapse ODE (11.816 at z = 0) | LCDM background (Ω_m, h) only | derived from the background |
| α | prefactor of the mobility time, α = 1 by convention | V5: **O(1) FREE**; the variational structure does not fix it | open, robustness required |
| β | ψ damping time τ_ψ = β τ (causal completion only) | stability needs β < ρ_m/ρ_c; β = 1 is admissible in every state | O(1), bounded by stability |
| ε | width of the switch smoothing, 0.077 | inherited (CFG539/527 engine T1 switch) | numerical regularisation of an indicator; the continuum system uses ε → 0 |
| f_ret(M) | census retained fraction (CFG416 `fret_of`, CFG515 `fret_census`) | inherited | only (i) to emulate ejected baryons in a feedback-free PM, and (ii) to infer M_ta for observed systems. Not part of the dynamics |
| RMIN | smallest resolved host | numerical (CFG530) | numerical |

**Audit D1 (sympy): PASS.** Every equation below is dimensionally consistent, and every timescale is built from G and a local
density only (τ uses {G, ρ_m}). **MUTATE M3:** a hidden constant time is flagged.

## 2. Fields

| field | definition | units |
|---|---|---|
| f_b(x, v, t), f_c(x, v, t) | phase-space density of baryons and of cold energy | kg m⁻⁶ s³ |
| ρ_b, ρ_c | ∫ f d³v | kg m⁻³ |
| ρ_m | ρ_b + ρ_c | kg m⁻³ |
| u_c | ∫ v f_c d³v / ρ_c (mean orbital velocity) | m s⁻¹ |
| Φ | Newtonian potential of the real mass | m² s⁻² |
| g_b | −∇Φ_b, with ∇²Φ_b = 4πG ρ_b (the baryons' own Newtonian field) | m s⁻² |
| ρ_ph | phantom density of the law (E7) | kg m⁻³ |
| 1_B | bound region (the switch f_sw, E8) | 1 |
| 1_C | catchment (E9) | 1 |
| d | deficit, 1_B 1_C max(ρ_ph − ρ_c, 0) | kg m⁻³ |
| ψ | deficit potential, ∇²ψ = 4πG d, ψ ≤ 0 | m² s⁻² |
| τ | (4πG ρ_m)^(−1/2) (local free-fall time) | s |
| v_s | settling drift (E4) | m s⁻¹ |
| Γ | 4πG ρ_c α τ = α (ρ_c/ρ_m) √(4πG ρ_m) (linear relaxation rate) | s⁻¹ |

## 3. The system

**(E1) Baryons (collisionless part).** ∂_t f_b + v·∇_x f_b − ∇Φ·∇_v f_b = 0. Gas hydrodynamics and feedback are not part of this
lane (open item 7).

**(E2) Gravity.** ∇²Φ = 4πG (ρ_b + ρ_c), with Φ → 0 at infinity. Only real mass gravitates: there is no extra source term, and
G9 holds.

**(E3) Cold energy, kinetic form.** ∂_t f_c + ∇_x·[(v + v_s(x, t)) f_c] − ∇Φ·∇_v f_c = 0.

The drift v_s is a velocity-independent advection in position space. Each element keeps its velocity while it slides. Taking
moments:
- ∂_t ρ_c + ∇·[ρ_c (u_c + v_s)] = 0, so mass is conserved exactly;
- ∂_t(ρ_c u_c) + ∇·[ρ_c (u_c + v_s) ⊗ u_c + Π_c] = −ρ_c ∇Φ, where Π_c is the velocity-dispersion tensor.

**(E4) Drift.** v_s = −α 1_B 1_C τ ∇ψ. This is the gradient-flow drift v_s = −α τ ∇μ with mobility ρ_c α τ on B∩C. Here μ is a
selection of the first variation ∂F/∂ρ_c (section 4), and ψ is a valid selection everywhere on B∩C. Outside B∩C the mobility is
zero, so cold energy there is ordinary cold matter (T6).

**(E5) Deficit.** d = 1_B 1_C max(ρ_ph − ρ_c, 0). It is one-sided: the deficit counts missing settled cold energy, never an
excess.

**(E6) Deficit potential.** ∇²ψ = 4πG d, with ψ → 0 at infinity. This uses the isolated Green's function per connected catchment.
Overlapping catchments share one ψ, which is the record's shared supply (R8). In a periodic box the mean-subtracted Poisson
solve is only an approximation, because it breaks ψ ≤ 0, and ψ ≤ 0 is the sign the Lyapunov argument uses.

**(E7) Phantom.**
- **Round rule (primary, R6).** For each bound region B_i, take its baryon centre x_i and let M_b,i(<r) be the region's own
  baryon mass within r of x_i. Then
  ρ_ph,i(r) = (1/4πr²) d/dr [(ν(G M_b,i(<r)/(r² a₀)) − 1) M_b,i(<r)].
  Only the region's own baryons enter, so there is no external-field effect (R7).
- **QUMOND variant.** ρ_ph^Q = −∇·[(ν(|g_b|/a₀) − 1) g_b]/(4πG), with g_b from all baryons. External fields enter |g_b|, which
  reintroduces an EFE-like dependence. It can also be negative (−66.5 M_b on the deep annulus, T3 lane). The CFG527/539 PM
  engines use this global form, as an approximation (open item 4).
- **"Retained baryons"** are the baryons actually present, ρ_b. The census factor f_ret multiplies ρ_b only in a feedback-free PM.
- In the 1-D runs the round-rule phantom of a Hernquist or point mass has **0 negative cells** (JSON `rhoph_neg_cells`).

**(E8) Bound region (f_sw).** Let λ₁ ≥ λ₂ ≥ λ₃ be the eigenvalues of the tidal tensor T_ij = ∂_i∂_j φ, where ∇²φ = δ (the trace is
δ). Then B = {x : λ₂(x) ≥ τ_ta(z)} with τ_ta = (Δ_ta(z) − 1)/3: the region has collapsed along at least two axes. The engines
smooth it as f_sw = clip(½ + (λ₂ − τ_ta)/(2ε), 0, 1) with ε = 0.077 (inherited).

**(E9) Catchment.** C = ∪_h {|x − x_h| ≤ r_ta,h}. Here x_h are density peaks, and r_ta,h is the largest R whose mean total
overdensity is at least Δ_ta(z) (the turnaround radius). Hosts below RMIN are not resolved (numerical). For a host that formed
adiabatically, the catchment holds the cosmic ratio of cold energy:
M_cat = (1 − f_b) M_ta = 5.364 M_b,now/f_ret, with M_b,now = f_ret f_b M_ta.

**Nothing in (E1)–(E9) is set by hand per system.** B and C are functionals of the density field. ρ_ph is a functional of the
baryons. τ is local.

## 4. Free energy, gradient-flow structure, what is fixed

- **Free energy.** F[ρ_c] = (1/8πG) ∫ |∇ψ|² dV = −½ ∫ ψ d dV = (G/2) ∬ d(x) d(y)/|x − y|. It is ≥ 0 and convex in ρ_c, because d
  is a convex function of ρ_c and the kernel is positive.
- **First variation (V1, sympy, PASS).**
  - ∂F/∂ρ_c = 1_B 1_C ψ where d > 0;
  - the interval [ψ, 0] on filled points (d = 0 inside B∩C). The left derivative there is ψ (sympy), and the right one is 0;
  - {0} outside B∩C.
- **Onsager form.** The Rayleigh dissipation is R = ∫ ρ_c |v_s|²/(2ατ) dV. Minimising R + dF/dt over v_s gives (E4).
  - Lyapunov (V3): dF/dt = −α ∫_{B∩C} ρ_c τ |∇ψ|² dV ≤ 0. The sympy by-parts identity PASSES, with no boundary term, because the
    mobility region coincides with the region where d is defined.
  - In the 1-D runs the largest per-step increase of F/F₀ is ≤ −9e-15 (JSON `V3_max_step_dF_over_F0`): **PASS**.
- **Not a gradient flow: CFG539's committed form (V2).** That form confines the deficit by the census edge but gives the drift
  mobility over the whole catchment. Its response matrix ∂μ_i/∂ρ_j is not symmetric (sympy: the shell row is nonzero, the shell
  column is zero), so it **IS NOT a gradient flow of any functional**. The shell moves in the deficit field without entering F.
  The variational form (census edge removed, mobility = deficit region = B∩C) **IS** a gradient flow.
- **Stationary states and the minimiser (V4: PASS).**
  - Stationary ⇔ ρ_c ∇ψ = 0 on B∩C. That holds where d = 0 locally, or where no cold energy is left.
  - The minimiser of F at a fixed catchment mass is the **inside-out fill**: ρ_c = max(ρ_ph, ρ_c,initial) inside r_*, and 0 in the
    shell r_* < r < r_ta, with M_ph(<r_*) + (pre-existing overfill) = M_cat.
  - KKT holds with Lagrange multiplier ψ(r_*). Numerically the violation is 0 in every run.
  - The 1-D flow's steady state reproduces r_* to ≤ 0.01% (sub-cell) and ≤ 0.9% (literal face) in every run.
- **What the principle fixes, and what it leaves.**
  - It fixes the form v_s = −τ∇μ and the selection μ = ψ. It also fixes every stationary state, independently of the mobility:
    the sympy stationary condition is ψ' = 0, with no α, and the steady profiles at α = 0.5, 1 and 2 agree to ≤ 8e-7 of M_cat.
  - It does **not** fix the mobility prefactor. Any α φ(ρ_c/ρ_m, g/a₀, …) > 0 gives a gradient flow with the same minimisers.
  - The "λ = 1 convention" is therefore replaced by a statement: **the coefficient is O(1) FREE.**
  - Robustness requirement: z = 0 observables must not move when α changes by a factor of 2.
  - In the idealised 1-D drift-only model this requirement **fails**: t₉₀ ∝ 1/α exactly, and t₉₀(α = 0.5) = 16–20 Gyr against
    the 10 Gyr bar. The label is **RATE-SENSITIVE (idealised)**. The PM (CFG539 Stage 2: mobility ×0.5 and ×2, with orbital
    motion) is the real test.

## 5. Conservation and energy

- **Mass:** exact. The drift is a flux. The 1-D |ΔM|/M is ≤ 8e-16.
- **Linear momentum:** the drift leaves every element's velocity unchanged, so the total momentum is untouched by the drift and
  conserved by the self-gravity.
- **Angular momentum:** not conserved. A radial slide at fixed v changes r × v (open item 6).
- **Energy:** not conserved. E_N = ∫ ½ ρ v² + W changes at the rate dE_N/dt = ∫ ρ_c v_s·∇Φ dV, which is ≤ 0 for inward settling.
- **Released energy per unit settled mass** (top-hat at rest → steady state; Hernquist; can / alt):

| system | ΔW/M_cat | K_f/M_cat (Jeans, needed) | E_sink/M_cat | in km² s⁻² |
|---|---|---|---|---|
| MW-like (6e10, a = 2.5 kpc) | 0.770 / 0.791 V_f² | 0.529 / 0.528 V_f² | **0.241 / 0.263 V_f²** | 6.6e3 / 7.9e3 |
| group-like (CFG540 median) | 0.410 / 0.411 V_f² | 0.298 / 0.290 V_f² | **0.112 / 0.121 V_f²** | 9.5e3 / 1.1e4 |
| cluster-like (1.5e14, point) | 0.986 / 1.012 V_f² | 0.664 / 0.664 V_f² | **0.322 / 0.348 V_f²** | 4.4e5 / 5.2e5 |

  E_sink > 0 everywhere: the settled state is more bound than the infall can supply, so energy must leave. The deficit field
  energy behaves similarly: ΔF/ΔW = 0.71–1.23.
- **Where the energy can go (S):**
  - (i) **Heat in the cold energy: EXCLUDED.** It would raise σ² above the phantom's Jeans value by 0.14–0.18 dex (rule 0.1 dex).
  - (ii) **Exchange with dark energy: ALLOWED, conditionally.**
    - Cosmic upper bound: Δρ_DE/ρ_DE = 2.2e-6, i.e. Δlog a₀ = 4.9e-7 dex, against DESI's ±0.04 dex.
    - Locally, if the energy leaves at c: Δa₀/a₀ ≤ 7e-9.
    - It needs dynamical dark energy. An exact Λ cannot exchange energy, since ∇_μ(Λ g^{μν}) = 0.
    - It is excluded for clustering dark energy: Δa₀/a₀ = 2e-3 at r_M in the MW-like case.
    - The coupling Q is **not derived**.
  - (iii) **Radiation: EXCLUDED.** There is no EM coupling, and the GW power is ≤ 1e-15 of what is needed.
  - (iv) **Baryons: EXCLUDED by G9.** The drift force is not gravitational. The energy would also be 17–19 times the MW baryons'
    virial kinetic energy, and about 3 times the group's.

## 6. Causal completion

- **As written** (A0, instantaneous ψ), the linear operator is of order zero: s = −Γ for every k. There is no k² diffusion, and
  nothing propagates. Support moves with v_orb + v_s. The only instantaneous element is the elliptic ψ, of the same kind as
  Newtonian Poisson.
- **Retarded ψ, undamped** (c⁻² ∂_t²ψ − ∇²ψ = −4πG d): **UNSTABLE.**
  - The cubic is s³ + c²k² s + Γ c²k² = 0, whose s² coefficient is 0, so Routh–Hurwitz fails.
  - Growth rate → Γ/2 at all large k (scan max Re s = 0.500 Γ).
- **Retarded ψ, damped** (c⁻² ∂_t²ψ + (c² τ_ψ)⁻¹ ∂_tψ − ∇²ψ = −4πG d):
  - The cubic is s³ + s²/τ_ψ + c²k² s + Γ c²k² = 0.
  - Hurwitz gives stability iff Γ τ_ψ < 1, i.e. β < ρ_m/ρ_c.
  - With τ_ψ = τ (β = 1) this holds in every admissible state, because ρ_c < ρ_m whenever baryons are present. The front speed is
    c, and the static limit is (E6).
  - **Label: CAUSAL-WITH-τ.**
  - Stability also selects the timescale: the alternatives c/a₀ and 1/H₀ give Γ τ_ψ ≫ 1 inside galaxies and are unstable.
- **Cattaneo drift** (τ ∂_t v_s + v_s = −τ∇ψ):
  - With instantaneous ψ: stable.
  - With an undamped wave: unstable.
  - With a damped wave: Hurwitz requires (β + 1)(1 − q(β + 1)) + K² β q² > 0, with q = ρ_c/ρ_m and K = ck/Γ.
    - It fails only for ck ≲ 1.4 Γ when q > ½. That means wavelengths ≳ 100 Mpc for Γ⁻¹ ≥ 0.1 Gyr, beyond any bound system.
    - By the frozen "every state" rule it is **UNSTABLE**.
- **Nonlinear drift speeds (C1).**
  - At t = 0 the maximum |v_s|/c is 4.8e-3 / 5.3e-3 (MW-like), 2.2e-3 / 2.5e-3 (group-like) and **4.3e-2 / 5.2e-2 (cluster-like)**.
  - The frozen 1e-2 margin **FAILS** for clusters. During the run, cells with ρ_c ≥ 1e-3 ρ_c0 reach 2.4e4 / 2.9e4 km/s.
  - The cause: v_s ∝ ρ_m^(−1/2) grows without bound in diffuse reservoirs (open item 3).

## 7. What emerges and what is inherited

- **Edge location (T2a): emergent.**
  - With the census edge removed (variational form), the drift fills inside-out and stops where the catchment runs out.
  - For a point mass that radius is r_M/ln(1 + M_b/M_cat) = r_M/ln(1 + f_ret f_b/(1 − f_b)), the census formula, with no census
    rule inserted.
  - The 1-D flows reproduce it to ≤ 0.85% (literal face, N = 400) and ≤ 0.33% (N = 1600) in all four point cells (two masses, two footings).
- **Frozen label: NOT EMERGENT BY THE FROZEN RULE.**
  - The frozen inside-out clause uses the q ≥ 0.5 front. That front first runs into the undrained reservoir, which already has
    ρ_c0 ≥ ρ_ph/2 beyond 1.6–3.0 r_*. It peaks at 1.25–1.51 r_* and then recedes as the reservoir drains.
  - The filled front (q ≥ 0.999, post-freeze diagnostic) never recedes in any run.
  - The label is reported as frozen. The substance: the location is emergent, and the fill is inside-out by the filled-front test.
- **Inherited inputs** that the emergent edge still needs:
  - the catchment = turnaround sphere at the cosmic ratio (adiabatic start; CFG424);
  - for observed systems, M_ta inferred through the census f_ret.
- **Groups (T2b): PROBLEM PERSISTS.**
  - The class-A edge is the exhaustion radius of the Hernquist phantom, at median r_*/Re = 1.51 / 1.40 (range 0.92–3.26).
  - Class mean Δ = +0.118 / +0.106 ± 0.021, against the census point-mass edge +0.153 / +0.145 and no edge +0.010 / −0.010.
  - Reaching |Δ| < 0.042 would take 5× / 3× the census supply (report only).

## 8. Open items (why "with open items")

1. **α (mobility prefactor) is O(1) FREE.** In the idealised drift-only model the z = 0 state is RATE-SENSITIVE: t₉₀ = 8–10 Gyr at
   α = 1. The PM robustness runs (CFG539 Stage 2) decide this.
2. **Energy sink.** Only dark-energy exchange is allowed. It requires w ≠ −1 dynamics with sound speed ~c, and its coupling Q is
   not derived.
3. **The overdamped reading is self-inconsistent in diffuse reservoirs** (post-freeze diagnostic).
   - Π = |v_s| τ/r reaches 10–540 at t = 0 and up to 1300 during the run. |v_s| exceeds the circular speed by up to ×9.
   - A drift-speed bound is needed. An inertia-limited (Cattaneo) drift is the natural candidate; there the dynamics approaches
     CFG539's class C.
   - It is stable at all sub-100-Mpc scales, but unstable by the frozen every-state rule.
4. **The PM uses the global QUMOND phantom.** The round per-region phantom (E7) is what R6/R7 require.
5. **Kinetic consistency.**
   - d = 0 is stationary under (E3) only if the settled cold energy's velocity distribution is a collisionless equilibrium of ρ_ph
     in Φ (for the SIS, σ² = V_f²/2: CFG461's temperature).
   - Class A does not supply this. Settling at fixed velocity leaves it sub-virial, and the one-sided deficit never removes an
     overfill. So T1 equality (ρ_c = ρ_ph) is not guaranteed in the full kinetic system; only ρ_c ≥ ρ_ph is restored where the
     supply lasts.
   - F is a Lyapunov function of the drift sub-flow only. The orbital term ∇·(ρ_c u_c) is not sign-definite in dF/dt.
6. **Angular momentum is not conserved by the drift.**
7. **Gas and feedback**, and the switch width ε (inherited), are not derived.
8. **The edge's supply amount** (A6) reduces to the catchment definition (turnaround sphere at the cosmic ratio, adiabatic start),
   which is inherited, not derived.
