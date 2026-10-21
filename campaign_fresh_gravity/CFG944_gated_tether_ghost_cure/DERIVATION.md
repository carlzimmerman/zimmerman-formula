# CFG944 DERIVATION: can the turnaround-gated tether (CFG941 R3θ) be made ghost-free?

Criteria: `FROZEN_CRITERIA.md` (2587be5c7, committed alone first). Every load-bearing step has a sympy or numeric check in
`cfg944.py`; check names are in brackets. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. Cold energy, no
particle species. Not "theory closed". K = 4πG, u = |Dχ|, W ≡ W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K (defined only for u < a₀),
D(u) = KW′ = u/(1 − u/a₀), S5(x) = 6x⁵ − 15x⁴ + 10x³, θ = ∇_μu^μ the medium's expansion, θ_s = H₀.

**Overall class (frozen rule): NO CURE.**
- Every declared cure is NOT CURABLE.
- Theorem G passes its checks: no local Lagrangian L(θ, u) of the medium's expansion and tether invariant can satisfy all four of
  - the static law (a),
  - growth at the actual linear amplitude (c-amp),
  - ghost freedom at all k (d),
  - the slip line (e).
- The one construction that removes the ghost globally (C4) does so only by switching the tether on in the linear regime at
  z ≳ 84. There the medium's own peculiar field exceeds u_c, and indeed a₀.
- The settled sector of every candidate is CFG938's P0, so (g) fails. Class A is not the non-relativistic limit, and the
  T1x/T2x/NC1x shear passes do not transfer.

The object (CFG941 R3θ):

  S = ∫√−g [c⁴R/16πG − mc²n − s(θ)(W(u) + (3γ/4K²)τ_μντ^μν) + λ(D_μD^μχ − Kmn)] + S_b,

with s = 1 − S5(θ/θ_s) on [0, θ_s], s = 1 for θ ≤ 0 and s = 0 for θ ≥ θ_s.

---

## 1. The ghost, re-derived exactly

### 1.1 Exact second variation [G1, K6]
Work in label (Lagrangian) coordinates, with J the Jacobian of the map from labels to positions. Continuity is kinematic and
θ = J̇/J exactly (θ = ∇·v = −d ln n/dτ). A medium term ∫√−g F(θ, u) becomes ∫d⁴q J F(J̇/J, u). Because J F(J̇/J) is homogeneous
of degree 1 in (J, J̇), its Hessian has rank one. sympy gives exactly

  δ²[J F(J̇/J)] = (F_θθ(θ₀)/2J₀)(δJ̇ − θ₀δJ)²   for ANY F(θ).

At θ₀ = 0 with F = −sW and δJ̇ = J₀∇·v, this is −½s″(0)W(∇·v)² per unit volume, which is CFG941's term (K6).

### 1.2 The kinetic coefficient [G2]
The second-order part of J = det(I + ∇ξ) is ½[(∇·ξ)² − ∂_iξ_j∂_jξ_i] = ½∇·(ξ∇·ξ − ξ·∇ξ), a divergence. For a single plane wave of
any polarization it vanishes identically (sympy). So in WKB the longitudinal kinetic coefficient is exactly

  ρ₀ + F_θθ k²   (transverse: ρ₀),

and for R3θ F_θθ = −s″(θ)W(u). Wherever s″ > 0 (the convex, upper half of the gate, θ ∈ (θ_s/2, θ_s)), the coefficient turns
negative for k > k_g = √(ρ₀/(s″W)). The quadratic action of (δρ, v, δχ) is CFG938's, with the tether multiplied by s(θ₀), plus
this single kinetic term. δχ is fixed by the constraint (δχ = −Kδρ/k²), δρ = −ρ₀ik·ξ, and v = ξ̇.

### 1.3 Frozen-coefficient dispersion and the degenerate surface [G3]
With A = F_θθk², the term ½A(ξ̇ − θ₀ξ)² gives

  (ρ₀ + F_θθk²)ω² = ρ₀Ω²_P0(k; s₀) − F_θθk²θ₀²,
  Ω²_P0 = γ_eff ρ₀k² + Kρ₀[s₀(D′cos²ϑ + (D/u)sin²ϑ) − 1].

Here s₀ = s(θ₀), and the frozen-coefficient ξξ̇ term is a total derivative. The F_θu terms are O(k) gyroscopic couplings,
subleading at large k.

**Example.** NGC 3198 at r = 7.1 kpc, θ₀ = 0.8θ_s, canonical:
- k_g r = 2.6e-3;
- ω²/(Kρ₀) = −3.88 / +3.51 at k = k_g(1 ∓ 0.1), and −3.7e7 / +3.7e7 at k_g(1 ∓ 1e-8).

ω² ∝ 1/(k − k_g), so it goes to −∞ as k → k_g from below: the inertia vanishes against the gated-off self-gravity. Above k_g there
is negative-energy oscillation. ω² is therefore **not bounded below independently of k**. The R3θ ghost is a degenerate kinetic
surface, not only a sign flip.

### 1.4 Reproduction of CFG941 and the galaxy-interior states [K4, G5]
CFG941's nine k_g R values are reproduced exactly (max relative deviation 0), with s″_max θ_s² = 5.77350 and k_g R = 0.227–2.185.

Transition states are also reached from settled galaxies. A perturbation with |∇·v| ≈ θ_s/2 ≈ 1e-18 s⁻¹, far below galactic
rates, puts a settled element into the convex half of the gate. On NGC 3198's 43 radii, with the medium density equal to the law's
phantom density:

| set | footing | k_g scale | u/a₀ |
|---|---|---|---|
| T3 (NGC 3198 interior) | canonical | k_g r = 5.0e-4 – 1.2e-2 | up to 0.774 |
| T3 (NGC 3198 interior) | alt | k_g r = 4.8e-4 – 1.2e-2 | up to 0.746 |
| T2 (CFG941 examples, edge field u = Kρ₀R/3) | both | k_g R = 0.077–1.09 | — |

The ghost band covers every galactic scale.

## 2. The linear amplitude the gate must tolerate (CFG654 native table)

U(z) is the 1σ medium field of linear perturbations, over k ∈ [0.01, 5] h/Mpc. P is CFG654's A1-primary CAMB table at z_i = 49,
scaled by the table's own D(a), with the medium's share f_c = 0.843; the D5 χ̄ boost is omitted, which lowers U.

| | U(0) | U(100) | U(1100) | U ≥ u_N,max for | U ≥ a₀ for |
|---|---|---|---|---|---|
| canonical | 0.0092 a₀ | 1.20 a₀ | 15.6 a₀ | z ≥ 65 | z ≥ 84 |
| alt | 0.0076 a₀ | 0.99 a₀ | 12.9 a₀ | z ≥ 75 | z ≥ 101 |

U rises as (1 + z): the physical peculiar acceleration of a constant comoving potential. U(0) = 8.6e-13 m s⁻² is a sane value
[AMP_native_table_sane]. The amplitude enters only (c-amp) and Theorem G. The margin is large: the conclusions need only U ≥ 0.77a₀
at some z ≤ 1100, which holds by a factor 20 at z = 1100.

**Side flag (estimate, not graded).**
- P0's always-on tether reads exactly this u, which reaches W's wall (u = a₀) at z ≥ 84 / 101 on typical points.
- CFG941's quadratic-action exponents for P0 (0.610 / 0.694) assume u ≪ a₀, so they are valid only at lower z.
- The gated theories avoid the wall only because s ≡ 0 exactly at θ ≥ θ_s.
- CFG938/941 files are not edited.

## 3. C1: an aether-like term (c_θ/2)θ², always on: NOT CURABLE

Action: R3θ plus +(c_θ/2)(∇_μu^μ)², with new constant c_θ [kg m⁻¹].

**G_cosmo [C1_G_cosmo].** Minisuperspace with lapse, ds² = −N²c²dt² + a²dx² (sympy):
- √−g R = −6aȧ²/(Nc) + a total derivative, and θ = 3ȧ/(Na);
- so L = −(3c³/8πG)aȧ²/N + (9/2)c_θc aȧ²/N − ρ₀c³N.

The Hamiltonian constraint gives

  H² = (8πGρ/3)/(1 − 12πGc_θ/c²),   i.e.   G_cosmo/G_N = 1/(1 − 12πGc_θ/c²).

This is Einstein-aether's 1/(1 + 3c₂/2) with c₂ = −8πGc_θ/c² (checked). The dust history a ∝ t^{2/3} solves the a-equation with the
same rescaling, so the cure is a pure G renormalisation, ε_θ = (9/2)c_θH². Static states have θ = 0, so G_N = G.
- The sign that gives the medium positive kinetic energy (c_θ > 0) raises G_cosmo.
- At 12πGc_θ/c² = 1 the scale factor's kinetic term vanishes.

**Ghost bound vs growth.**
- The ghost needs c_θ ≥ s″W on every transition state.
- Linear perturbations acquire extra inertia c_θk_phys² (δθ = −δ̇). The two-component EdS growth, with medium inertia ρ̄_c(1 + r),
  r = c_θk_phys²/ρ̄_c ∝ a, and the background with G_cosmo, gives |n − 1| < 1e-3 at every z ≤ 1100 and k ≤ 5 h/Mpc only for
  **c_θ ≤ 8.87e14 kg/m** (r(z = 0, k = 5) = 1.5e-3).

| set | footing | c_θ,g (kg/m) | × growth max | 12πGc_θ,g/c² | G_cosmo/G | n_min at c_θ,g (k = 5 / 0.01) |
|---|---|---|---|---|---|---|
| T1 | canonical | 1.75e24 | 2.0e9 | 0.049 | 1.05 | 0.00 / 0.16 |
| T2 | canonical | 1.54e25 | 1.7e10 | 0.430 | 1.75 | 0.00 / 0.01 |
| T3 | canonical | 9.00e24 | 1.0e10 | 0.252 | 1.34 | 0.00 / 0.03 |
| T1 | alt | 1.62e24 | 1.8e9 | 0.045 | 1.05 | 0.00 / 0.17 |
| T2 | alt | 1.05e25 | 1.2e10 | 0.293 | 1.41 | 0.00 / 0.03 |
| T3 | alt | 1.15e25 | 1.3e10 | 0.322 | 1.48 | 0.00 / 0.02 |

- For transition states with u ≥ 0.978a₀ (canonical) or 0.944a₀ (alt), the bound needs 12πGc_θ/c² ≥ 1: no Friedmann branch at all.
- Because W → ∞ as u → a₀, no finite c_θ is ghost-free globally. The exact region is W(u) ≤ c_θ/s″_max. At the growth maximum it
  covers u ≤ 1.2e-5a₀ (canonical) / 9.8e-6a₀ (alt), which is below every T1 state.
- The record has no BBN bound on G_cosmo, so none is graded. It is not needed: (c) already excludes C1 by about 9–10 decades.

**Tests:** (a) PASS; (b) PASS with the G_cosmo cost; (c) FAIL; (d) FAIL (region only); (e) PASS; (g) FAIL. **NOT CURABLE.**

## 4. C2: gates on non-derivative variables: NOT CURABLE

- **(i) Density, s(ρ_c) (= CFG941 R3n)** [C2i_density_gate_structure].
  - What differs from R3θ: the gate's curvature now multiplies a potential term, not a kinetic one, giving
    (s″W + sγ)δρ²/2 with δρ ∝ kξ. So c_eff² = ρ₀(s″W + sγ), and the θθ ghost becomes a gradient instability wherever s is concave
    and W > sγ/|s″|.
  - It is the same convexity obstruction in another variable: a bounded increasing gate that saturates at 1 is concave near the top.
  - Independently, CFG941 R3n fails (a), since the tether ends at r_* = 73 kpc and the BTFR limit is 0; and (c), since the gate is on
    for the cosmic mean at z > 18. Its min c_eff²/(sγρ) is −3.4e7.
- **(ii) χ itself** [C2ii_chi_gate].
  - s(χ) adds −s′(χ)W to χ's Euler–Lagrange equation. That changes the static law unless s′ = 0 on every static χ, and it breaks χ's
    shift symmetry.
  - It also cannot recognise collapse. The rms linear medium potential today (1.4e-5 c²) exceeds NGC 3198's entire well across its
    radii (8.1e-7 c²), and χ̄ drifts by Ω_c c²/2 = 0.13 c² per Hubble time. A χ threshold is a cosmic-epoch switch.
- **(iii) Latch or label enforced by a multiplier** [C2iii_latch_and_clock_density].
  - λ(u^μ∂_μσ − F(θ, σ)) puts −λ̄F_θθ(δθ)² back into the kinetic sector, with a sign set by the multiplier. The (δσ, δλ) Hamiltonian
    Hessian has det = −F_σ² < 0: it is linear in the multiplier momentum and unbounded below.
  - If F is linear in θ, ∫dσ/α + ln n is conserved along the flow, so σ is a density or label gate (R3n / R2).
  - The clock–density label Y = Kρ_cT² (T the proper time) equals 2/3 exactly on the EdS mean, a natural turnaround label. But it is a
    density gate: (a) fails as for R3n, and δρ ∝ k makes s_YY W K²T⁴ρ₀k² a gradient term.
  - Stability needs a transition width ΔY ≥ 5.5e6 (L* = 24 pc) or 1.3e5 (1 kpc), against the 1.2e3 available (NGC 3198's lowest Y
    minus 2/3).

## 5. C3: the gate profile alone: NOT CURABLE (theorem) [C3_concavity_theorem]

- **(i)** By §1.2, ρ₀ − s″Wk² > 0 for all k iff s″ ≤ 0 wherever W > 0, i.e. s is concave.
- **(ii)** (c) needs |s(3H(z))| ≤ c₂,max = 2.35e-3 at z = 0 and z = 1100. Take θ₂ = 3H(1100) ≥ 6.1e4 H₀; matter alone gives this lower
  bound. Concavity with s(0) = 1 then gives s(3H₀) ≥ 1 − (θ₁/θ₂)(1 + c₂,max) = 0.99995, which is not ≤ 2.35e-3. A contradiction:
  no concave gate exists.
- **(iii)** Bounded s″ only moves k_g.
  - Any C¹ gate falling from 1 to 0 on [0, θ_s] with s′(θ_s) = 0 has max s″ ≥ 2/θ_s², since s′ ≥ −B(θ_s − θ) ⇒ 1 ≤ Bθ_s²/2. The bound
    is attained by (1 − θ/θ_s)².
  - max s″θ_s² by family: cubic 6.00, quintic (CFG941) 5.77, septic 7.51, optimal 2.00. A logistic constrained to s(0) = 1 − 1e-6 and
    s(3H₀) = c₂,max gives 4.22 H₀⁻².
  - At θ_s = 3H₀ the optimal gate raises k_g by ×5.10: T1 k_g R = 1.16–11.1, and NGC 3198 interior k_g r ≤ 0.063. A ghost band
    remains in every case.

## 6. C4: u-saturated gate + a transition-localized convex θ-term: NOT CURABLE

**Construction** (one constant, u_c):
- s(θ, u) = ŝ(θ) + h(u)(1 − ŝ(θ)), with ŝ = R3θ's gate and h = S5(2u/u_c − 1) (0 for u ≤ u_c/2, 1 for u ≥ u_c);
- L₀″(θ) = W_g·60x(1 − x)/θ_s² on x = θ/θ_s ∈ (0, 1), L₀ = 0 for θ ≥ θ_s;
- W_g = max over u ≤ u_c of (1 − h)W;
- the stiffness is not gated.

The cured action reads:

  S = ∫√−g [c⁴R/16πG − mc²n − s(θ, u)W(u) − (3γ/4K²)τ_μντ^μν + L₀(θ) + λ(D_μD^μχ − Kmn)] + S_b.

- **(d) is GLOBAL** [C4_construction, C4_d_bounded_dispersion].
  - F_θθθ_s² = 60x(1 − x)[W_g − (2x − 1)(1 − h)W] > 0 on 0 < x < 1 for every u < a₀ (sympy; grid minimum 4e-10 a₀²/K ≥ 0). Outside
    the transition there is no θ-dependence.
  - With F_θθ ≥ 0, ω² ≥ −max(Kρ₀, θ₀²) at every k, a weighted mean; the sampled minimum is −0.9965 in those units.
  - So the kinetic matrix is positive definite everywhere and ω² is bounded below: the ghost is cured.
- **(a) PASS.** s(0, u) = 1 for all u, and L₀ is linear for θ ≤ 0: a total derivative plus the bag constant B₀ = L₀(0) = 5W_g.
- **(b) PASS.** θ = 3H > θ_s and u = 0 on FRW give s = h(0) = 0 and L₀ = 0.
- **(c) literal PASS.** At u = 0 the medium is pure dust, n = 1.
- **(e)** caps u_c, through the bag's slip on CFG847's systems.
  - The slip-allowed bag is B_e = 0.0476 a₀²/K (canonical) and 0.0247 a₀²/K (alt).
  - So u_c ≤ 0.22 / 0.16 a₀ with the frozen profile (B₀ = 5W_g), ≤ 0.38 / 0.28 a₀ with the minimal profile (1.4375W_g), and
    ≤ 0.46 / 0.34 a₀ even at the absolute minimum B₀ = W_g (§7).
- **(c-amp) FAIL.**
  - On typical linear points U(z) exceeds u_c/2 (and a₀) at z ≳ 84. There the saturation switches the tether on: the effective
    c₂ = h(U/u_c) goes to 1, D-T returns, and the argument lies beyond W's wall.
  - (c-amp) needs u_c ≥ 2U_max/(1 + x_ε) = 29.3a₀ (canonical) / 24.3a₀ (alt). A finite bag needs u_c < a₀.
- **Window: empty. NOT CURABLE.** M5 shows that with U ≡ 0 the window would open (u_c ≤ 0.22a₀), so (c-amp) is the test that closes it.

## 7. Theorem G: no local L(θ, u) works [TheoremG]

**Statement.** Let the medium's dependence on its expansion and tether invariant be any C² local L(θ, u). Suppose:
- **(d)** ghost freedom at all k, i.e. L_θθ ≥ 0 (§1.2);
- **(a)** L(0, u) = −W(u) + L(0, 0) on NGC 3198's static states. The static EL depends only on L(0, ·): the variation
  ∫L_θ(0, u(x))∇·δξ̇ integrates by parts in time to zero on a static background;
- **(c-amp)** L(θ, u) = L(θ, 0) near some cosmic θ_T where linear states with u = u* occur (U(z) ≥ u* for z ≥ 65 / 75);
- **(c)** L(·, 0) linear on the cosmic range, so that there is no inertia.

Let T be that linear function. Then

  B ≡ L(0, 0) − T(0) ≥ W(u*),   u* = min(u_N,max, U_max).

**Proof.** f(θ) = L(θ, u*) is convex, so f(0) ≥ f(θ_T) − θ_T f′(θ_T) = T(0). Since f(0) = −W(u*) + L(0, 0), the bound follows. ∎

**Physical meaning of B.**
- T(θ) = α + βθ contributes a cosmological constant α everywhere plus a total derivative βθ.
- So, relative to the cosmic regime, every static region carries a vacuum term T_μν = Bg_μν, which shifts p_r and p_t in CFG938's slip
  formulas.
- The identity (d/dx)(xf′ − f) = xf″ gives ∫₀¹ x s″ dx = 1 for every gate falling from 1 to 0 with s′(1) = 0. So the bag is ≥ W
  whatever the profile; this is why C4's bag cannot be shrunk below W_g.

**Numbers.**
- canonical: u* = 0.774a₀, so B ≥ 0.712 a₀²/K, against B_e = 0.0476: ×15.0.
- alt: u* = 0.746a₀, so B ≥ 0.624 a₀²/K, against B_e = 0.0247: ×25.3.

No local L(θ, u) passes (a), (c-amp), (d) and (e) together. Static states with u → a₀ (the Solar System) would make the bound
infinite.

**Scope.** L is a function of (θ, u). Adding ρ-dependence brings in the R3n failures (§4(i)). New fields (latches, clocks) bring in
the multiplier sector (§4(iii)). Higher time derivatives of θ are Ostrogradsky-unstable. None of these is claimed to be closed beyond
what §4 shows.

## 8. (g): class A is not the non-relativistic limit

Class A was read from the CFG650 engine: `forces()`, `_finish_phik()`, `cover_peaks()`, `cover_balls()`, `own_host_labels()`. The
code was read only, never run or imported.

| item | class A (engine code) | gated theory (any cure) | match |
|---|---|---|---|
| g1 coupling | every PM particle (cold + baryon tracers) is kicked by −∇φ, with φ_k = −(1.5Ω_m/a)δ_k/k² − src_k/k² | settled medium feels −∇Φ_b + R(\|∇χ\|)∇̂χ (CFG941 D2b) | no |
| g2 phantom input | s_ph = −∇·[(ν(\|g_b\|) − 1)g_b], g_b = f_b × field of the retained (or condensed) fraction of the particle density over the box; src never feeds back | R(u) = g_N with u the total tethered field (host and neighbour media enter; hover lemma) | no |
| g3 linear regime | no catchments before turnaround: Newtonian cold matter | θ = 3H > θ_s: s = 0, pure dust | yes |
| g4 switch | union of balls (radius x·r_ON) around resolved peaks with enclosed mean ≥ Δ_ta(z), × tidal f_sw, × edge mask: non-local | local θ ≤ 0 (C4 also u ≥ u_c): pointwise, with no ball, peak or cosmic mean | no |
| g5 source | src = e − q s_c(1 + δ), demand e = f_sw max(s_ph − s_c(1 + δ), 0), filled by an instantaneous shell draw, zero-sum per catchment/host; particles are not moved | no extra source, ∇²Φ = K(ρ_b + ρ_c); the medium itself must move (continuity; settling needs dissipation, CFG938 §4) | no |

**(g) FAIL** (only g3 matches). The T1x/T2x/NC1x shear passes remain results of the class-A engine. They do not transfer to R3θ or
to any cure here.

## 9. What the cures imply for F2 (CFG945's lane; not duplicated)

Every candidate leaves the settled sector (θ = 0, s = 1) exactly P0, plus at most a constant (C4's bag). The hover lemma and
CFG941's Δa/g_host = 1.02–1.11 are untouched. C4's u-saturation would keep a strong-field satellite medium tethered whatever its flow.
No cure here touches the satellite problem.

## 10. Classes, and what is not claimed

| cure | (a) | (b) | (c) | (c-amp) | (d) | (e) | (g) | class |
|---|---|---|---|---|---|---|---|---|
| C1 aether θ² | PASS | PASS (G_cosmo cost) | FAIL (×2e9–2e10) | = (c) | FAIL (region u ≤ 1e-5 a₀) | PASS | FAIL | **NOT CURABLE** |
| C2 ρ / χ / latch | FAIL (ρ, Y), changed (χ) | — | FAIL (ρ) | — | FAIL (ρ, Y), ghost (latch) | — | FAIL | **NOT CURABLE** |
| C3 any s(θ) | PASS | PASS | PASS | = (c) | FAIL (theorem) | PASS | FAIL | **NOT CURABLE** |
| C4 u-saturated + convex θ-term | PASS | PASS | PASS (literal) | FAIL (needs u_c ≥ 24a₀) | **PASS (global)** | PASS for u_c ≤ 0.16–0.22a₀ | FAIL | **NOT CURABLE** |

**Overall: NO CURE** (all NOT CURABLE; Theorem G passes).

Open (not tested, not claimed):
- a non-variational switch (a dynamical latch not derived from an action), which would give up the action principle;
- a theory whose settled medium is held up by dispersion rather than a tether (CFG941 open item 2), which is a different theory;
- ρ-dependent extensions of Theorem G.

Not claimed:
- that any cure is a candidate;
- that κ, a₀, Ω_c/Ω_b or L* are derived;
- any data verdict.

Not "theory closed".

## 11. Controls and disclosures

- **K: all pass.**
  - K1: NGC 3198 law 2.22e-16 on both footings.
  - K2: BTFR limit 1; +1.00e-7 at y = 1e-14.
  - K3: n = 0.609545 / 0.694330 / 1.000000000000; c₂,max = 2.3458e-3.
  - K4: CFG941's nine k_g R values to 0, with s″_max θ_s² = 5.77350.
  - K5: s_847 = 1.5398e-5.
  - K6: the G1 identity reproduces CFG941's kinetic term.
- **MUTATE: all seven teeth bite (exit 1 by design).**
  - M1: removing C4's cure brings the ghost back (min F_θθθ_s² = −114 a₀²/K).
  - M1b: c_θ = 0 does the same.
  - M2: c_θ = c_θ,g/2 leaves a ghost on T1.
  - M3: half the bag gives F_θθ < 0 at x = 0.88, u = 0.20a₀.
  - M4: removing the saturation gives F_θθ < 0 as u → a₀.
  - M5: U ≡ 0 opens C4's window (u_c ≤ 0.22a₀).
  - M6: without (a), B_min = 0.
- **Text-only edits after the first full run.** After the first full set of runs (K, MUTATE, main), three output strings were changed:
  - G3's wording "diverges like −1/(k − k_g)" had the sign wrong; it now reads ω² ∝ 1/(k − k_g), → −∞ from below.
  - C1's class line used a hand value "u ~ 0.9 a₀". It now prints the computed u_flip = 0.978a₀ / 0.944a₀.
  - The g2 description of class A's phantom input was made precise: the retained fraction of the particle density, with src never
    fed back.

  No check, test, number or class changed. All three stages were then rerun from the final script (sha256 9978ec65…).
- **Hand expectations that missed (kept).**
  - Criteria §6 expected 12πGc_θ/c² to reach 1 "near u ~ 0.94a₀". Computed: 0.978a₀ (canonical), 0.944a₀ (alt).
  - It expected the C1 inertia c_θk²/ρ̄ to be ~1e2–1e8. Computed at c_θ,g(T1): ~1e1 (k = 0.01) to ~3e6 (k = 5).
  - It expected (e) to cap u_c near 0.3a₀. Computed: 0.22 / 0.16a₀ (frozen profile), 0.46 / 0.34a₀ (absolute minimum).
  - The other expectations held.
- **Implementation choices (not frozen; disclosed).**
  - C1's ρ̄_c is the EdS-consistent background (f_c × 3H₀²/8πG_cosmo), which favours C1. The declared Ω_c would tighten the growth
    window ×3.2.
  - U omits the D5 boost and uses the medium share f_c, both of which lower U. It is the 1σ rms over the (c) k-range.
  - G3's example state: mid radius, θ₀ = 0.8θ_s, L* = 24 pc and 1 kpc.
  - C4's dispersion sample uses s₀ only. The h′(u) terms add bounded k⁰ terms and do not affect the bound's k-independence.
  - T2 is capped at u = 0.999a₀.
  - The Y gate uses T = 2/(3H₀) and s ≈ 0.9 at the S5″ minimum.
- **Compute.** One process, ~1.5 s, peak RSS 0.31 GB, run beside NC2x with OMP_NUM_THREADS = 1 and nice 10. Nothing downloaded. No
  other lane's file edited. CFG654's table and CFG941's JSON were read only.
