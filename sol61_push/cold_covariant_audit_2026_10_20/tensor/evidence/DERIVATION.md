# CFG938 DERIVATION: the cold-energy medium as a relativistic continuum

Criteria: `FROZEN_CRITERIA.md` (7a0d41e8b, committed alone first). Every load-bearing step below has a sympy or numeric
check in `cfg938.py`; check names are given in brackets, e.g. [S2c]. κ = ½ FITTED. Footings are never pooled.
Cold energy's mass is required. Not "theory closed". Signature (−+++), K = 4πG, x⁰ = ct unless stated.

**Class: CONDITIONAL.** A covariant parent of canonical S2 exists for the longitudinal (curl-free P) sector, which
includes every spherical system. Its static limit is the law exactly. It conserves energy-momentum, has an isotropic
FRW background with w = 0, and is linearly well-posed. Its slip is ≤ 1.5e-5.

These hold only under five conditions (§10). The parent also carries three flags, reported with equal prominence:
- C3 FAIL is inherited.
- The tethered medium has no linear self-gravity (D2 flag).
- Tethered medium does not feel the gravity of tethered medium anywhere (a universality violation, §7).

---

## 1. Kinematics: what P is

**Fields.** Comoving label fields φ^I(x), I = 1, 2, 3, with
- B^{IJ} = g^{μν}∂_μφ^I∂_νφ^J,
- n = √det B,
- J^μ = n u^μ, with u^μ = ε^{μαβγ}ε_{IJK}∂_αφ^I∂_βφ^J∂_γφ^K / (6n√−g).

J^μ is identically conserved, so continuity is kinematic, not dynamical.

**Internal symmetry.** It is declared to be a FLUID: volume-preserving relabellings plus internal shifts. Reason: S3
calls the medium collisionless rest mass, which has no shear rigidity. The solid is discussed only where it changes
an answer.

**P is a gauge potential of the current.** The current is the divergence of an antisymmetric 2-form [S2a]:

  J^μ = ∂_νQ^{μν},  Q^{μν} = (1/6) ε^{μνβγ} ε_{IJK} φ^I ∂_βφ^J ∂_γφ^K,  J⁰ = det(∂_iφ^I).

Define P^i = m(Q^{0i} − n̄ x^i/3). Then, exactly and nonlinearly:
- ∇·P = ρ − ρ̄;
- ∂ₜP + j is divergence-free, so ∂ₜP_L = −j_L [S2a].

So P is the "electric" part of the 2-form whose divergence is the medium's current. This is the bound-charge relation
of a polarization, which is why the record's S2/S3 language works.

Two properties follow:
- P is defined only up to a transverse (curl) part. Q → Q + ∂C changes P_T and leaves J alone. For a fluid, P_T is
  pure relabelling: only P_L is physical.
- Subtracting the background term n̄x/3 needs an origin, a choice the uniform medium does not make.

**Linear order.** With φ = x − ξ, P = −ρ̄ξ + (divergence-free) [S2a2]. The minus sign is required by ∇·P = +δρ. So
"P ≈ x − φ" holds up to the factor −ρ̄.

## 2. Background (Q1)

**Configuration.** Flat FRW with φ^I = x^I [K2, S1a, S1b]:
- B^{IJ} = δ^{IJ}/a², n = a⁻³, u^μ = (1, 0, 0, 0).

The medium's rest frame is the comoving (cosmic) frame exactly.

**Stress.** T^μ_ν is diagonal with T¹₁ = T²₂ = T³₃. This holds for F(n) and for a generic solid
F(tr B, tr B², tr B³). For F = −mc²n: ρ = mc²n, p = 0, so **w = 0 exactly**.

**Why there is no anisotropy during expansion.** Three separate reasons, all checked:
1. A perfect fluid's stress is −nF′ u_μu_ν + (F − nF′)g_μν, which is isotropic in the rest frame for any expansion,
   even an anisotropic one (Bianchi I check) [S1a2].
2. A solid can carry anisotropic stress only through anisotropic (shear) strain. Isotropic expansion makes B ∝ δ, so
   no shear invariant is excited. In Bianchi I the solid's stress is anisotropic only if a₁ ≠ a₂ [S1a2].
3. The vector P is a *displacement*. A comoving medium is not displaced, so P ≡ 0 on FRW, and no direction exists to
   pick. The tether sector built below depends only on two quantities:
   - h^{μν}∂_μχ∂_νχ, the medium-frame gradient;
   - the traceless medium-frame tidal tensor of an auxiliary χ.

   Both vanish identically on FRW. There, χ = χ̄(t) with D²χ̄ = −3Hχ̄̇ = Kρ̄, so a homogeneous solution exists and no
   ρ̄ subtraction is needed [S1d].

This differs from CFG897, which put a *timelike* homogeneous P⁰ on FRW. That is a different object, and its stiffness
had an H² background energy. The medium's P has no background at all.

## 3. Matching to S2 (Q2)

### 3.1 The tether is forced: it is the medium's gravity

For a static medium in the weak-field metric, √−g(−mc²n) = −ρc² − ρΦ + O(c⁻²), and Ψ drops out exactly [K3]. With
∇·P = δρ_c:

  −δρ_c Φ = P·∇Φ − ∇·(PΦ)  [S2b].

Also

  −|∇Φ − KP|²/(2K) − W_rem(K|P|) = −|∇Φ|²/(2K) + P·∇Φ − W_full(K|P|),  W_full = W_rem + u²/(2K)  [S2b, S2b2].

So canonical S2 + ID is: [GR + minimally coupled dust]_Newtonian − W_full(u) − (γ/2)|∇P|².

The tether P·∇Φ is not a new coupling. It is the equivalence principle for the medium's rest mass: **forced.** The only
new physics is W_full and the stiffness. Here K W_full′ = u/(1 − u/a₀) and K W_rem′ = u²/(a₀ − u) (astra's dictionary,
GRAVITY_ACTION_AUDIT §2).

### 3.2 W is not a strain function; an extra structure is forced

[S2c] gives two facts:
- **Not a strain function.** Uniform compression φ = x/λ has the same strain B = δ/λ² everywhere, but
  |P|² = (λ³ − 1)² r²/(9λ⁶) grows with position. So u = K|P| is not a function of B^{IJ}.
- **Not local.** Two density profiles identical near R but with different interiors give u(R) differing by
  πGΔR/6. So u is an *enclosed-mass* quantity, nonlocal in φ.

Hence no local, shift-symmetric function of φ's derivatives can be W(K|P|). Two ways remain to localise it:
- **(i) An anchor.** A background 2-form or reference lattice (a pinned solid), e.g. u = (4π/3)Gρ̄|φ|³/r². This needs
  a centre and breaks translations, so it cannot serve a universe with many centres. Rejected.
- **(ii) The medium's own potential.** An auxiliary scalar χ obeying a medium-frame Poisson constraint
  D_μD^μχ ≡ h^{μν}∇_μ∇_νχ = Kρ_c, imposed by a multiplier λ, with u² = h^{μν}∂_μχ∂_νχ.

  In a static metric, h^{μν}∇_μ∇_νχ is the spatial Laplacian of the medium's slices. In spherical symmetry
  χ′ = GM_c(<r)/r² = u = K|P_L| (Gauss) [S2c2].

  χ and λ carry no time derivatives in the medium frame, so they are constraints, not particles [S5d]. On FRW the
  homogeneous mode χ̄(t) absorbs ρ̄ automatically (§2).

**Covariantly, u = K|P| is |Dχ|:** the magnitude of the medium-rest-frame gradient of the potential sourced by the
medium alone. It is not a function of the strain, and it is not available from the metric, which carries only the
total potential. One extra non-propagating field (χ, plus its multiplier) is the price.

### 3.3 The stiffness

For longitudinal P, |∂_i∂_jχ|² = (∇²χ)² + divergence (exact, 3-D) [S2d]. So

  (γ/2)|∇P_L|² = (γ/2)δρ_c² + divergence.

For a fluid this is all of it, because P_T is relabelling. Two covariant realisations exist:
- **(a) Local equation of state:** ε_int = (γ/2)ρ², i.e. p = πGL*²ρ². This is the pressure CFG847 and CFG888 used.
  Covariant and local, it is a Γ = 2 stiff fluid on the background:
  - w(0) = 2.9e-18 (24 pc) to 5.0e-15 (1 kpc);
  - w(z = 1100) = 3.9e-9 to 6.7e-6;
  - ε_stiff/ε_rad at z = 4e8 is 1.3e3 to 2.3e6, reaching 10% of radiation at z = 3.5e6 / 8.3e4 [S2d3].

  **Excluded at BBN for the whole L* window if the medium exists then.**
- **(b) Background-free:** −(3γ/4K²) τ_μν τ^μν, with τ_μν = D_μD_νχ − ⅓h_μν D²χ. This equals (γ/2)δρ_c² for
  longitudinal perturbations and vanishes on FRW, since the tidal tensor there is pure trace. It is the form adopted
  here. Cost: the χ constraint becomes fourth order in *space* (no higher time derivatives).

The static equation including stiffness is R(u) = g_N + γ dρ_c/dr [S2d2]. With ρ_c′ < 0 it pushes u below the law,
which is the screening.

*Solid alternative:* a pure shear modulus μ ∝ ρ² vanishes on FRW, but its energy for nonlinear radial collapse depends
on λ_r and λ_t separately, so it does not reproduce S2's exact spherical (γ/2)δρ². Not adopted.

### 3.4 The derived action

  S = ∫d⁴x √−g [ c⁴R/(16πG) − mc²n − W_full(u) − (3γ/4K²) τ_μν τ^μν + λ(D_μD^μχ − K m n) ] + S_b[g, ψ_b],

with
- n = √det B^{IJ};
- u² = h^{μν}∂_μχ∂_νχ, h^{μν} = g^{μν} + u^μu^ν;
- W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K;
- γ = KL*²/2, L* ∈ [24 pc, ≳ 1 kpc] (CFG820);
- a₀ = κc√(Gρ_DE), κ = ½ FITTED.

**Static weak-field limit.** With Φ and χ on shell:

  L = −|∇Φ|²/(2K) − (ρ_b + ρ_c)Φ − W_full(|∇χ|) − (γ/2)δρ_c² + λ(∇²χ − Kρ_c),

which equals canonical S2 with ∇·P = δρ_c on the longitudinal sector. In spherical symmetry the energy is a
functional of the medium's enclosed mass M_c(r):

  E[M_c] = ∫dr [ −G(M_b + M_c)²/(2r²) + 4πr² W_full(GM_c/r²) + (γ/2)(M_c′)²/(4πr²) ].

**Euler–Lagrange (sympy).** D_full(u) = g + γρ_c′, i.e. R(u) = g_N + γρ_c′. At γ → 0 this is the law
g_N = g²/(g + a₀). [K1] solves it at all 43 radii of NGC 3198 (Υ = 0.61) from the lambdified sympy expression:
max |g/g_law − 1| = 2.2e-16 on both footings (line 1e-6).

### 3.5 Forced vs chosen

| element | status | why |
|---|---|---|
| dust background, w = 0 | forced | F = −mc²n (rest mass) [K2] |
| rest frame = cosmic frame | forced | φ^I = x^I is comoving [S1b] |
| ∇·P = δρ, ∂ₜP_L = −j_L | forced | 2-form identity of the conserved current [S2a] |
| tether P·∇Φ | forced | the medium's minimal gravitational coupling (EP) [K3, S2b] |
| P_T | chosen (fluid ⇒ unphysical) | relabelling; a solid would make it physical |
| background subtraction for P | avoided | the χ route absorbs ρ̄ in χ̄(t) |
| W_full(u) itself | chosen (S2's input) | not derived; κ fitted |
| some extra structure for u | forced | u is nonlocal (enclosed mass) [S2c] |
| that structure = χ + λ, medium-frame constraint | chosen | the anchor alternative needs a centre |
| stiffness as (γ/2)δρ² | forced (fluid, longitudinal) | [S2d] |
| stiffness realisation (EoS vs χ-tidal) | chosen | EoS fails BBN if the medium is present then; χ-tidal is background-free |
| γ > 0 | forced by well-posedness | M2 |

## 4. Conservation and settling (Q3)

**Momentum balance.** The action is diffeomorphism invariant, so ∇_μT^{μν} = 0 on shell. The tether sector's static
stress, by metric variation [S3a], is

  T_ij = (W′/u)∂_iχ∂_jχ − δ_ij W + 2∂_(iλ∂_j)χ − δ_ij ∇λ·∇χ.

For generic fields the identity is

  ∂_jT_ij = ∂_iχ[∇·(W′∇̂χ) + ∇²λ] + ∂_iλ ∇²χ  [S3b].

On the χ shell this equals ρ_c∂_i(Kλ), the reaction to the tether force on the medium (−ρ_c∇(Kλ) = ρ_c(D_full û)_L).
So medium + tether + gravity conserve momentum.

**Result: CFG660's stress is this action's stress.** On the law [S3c]:
- p_r = −W_full(u), p_t = p_r + D(u)u/K;
- dP∥/dg = (g/K)(dg_N/dg − 1), P⊥ − P∥ = g(g − g_N)/K;
- deep limit P∥ = −g²/8πG + g³/(6πGa₀);
- p_r′ + 2(p_r − p_t)/r = −ρ_c g.

This is exactly CFG660's field-aligned stress, now derived rather than posited. Why CFG660 was ill-posed and this is
not: CFG660 treated the stress as a fixed function of g, applied to an independent density. Here the stress responds
through the χ/λ constraints, and the dynamics follow from an action (§6).

**The settling drift.** The ideal action has **no first-order drift**. The medium obeys Euler's equation with the force

  f = −∇Φ − ∇p + (D_full û)_L = −∇Φ_b + R(u)û − ∇p.

Near the law, f ≈ R′(u_L)(g − g_law) [S3d]. This is the direction of the record's two-sided drift
v_s = ατ(g − g_law) (CFG544 FIX-1, CFG638). So the drift is the *overdamped* version of this force, with mobility
ατ = τ_d R′(u_L).

The ideal medium does not settle; it oscillates about the law (§6, ω² ≥ 0). Settling needs a dissipative extension.
- **Drag (∝ v).** Needs a frame to drag against, so it is not Galilean-invariant by itself. It is a choice.
- **Covariant viscosity.** Israel–Stewart, the form of CFG638's moments. Entropy production ησ_μνσ^μν + ζθ² ≥ 0;
  total energy is conserved with heat.

Either way the books close as

  d(K + E_grav + E_W + E_stiff)/dt = −(dissipation) = −dU_heat/dt.

**Comparison with CFG932 Q1** (non-conserving drift). CFG932's books contain K_c + K_b + W_grav only. They omit
E_W = ∫W_full(u)dV, the tether-field energy, which is a term of S2 itself.

[S3e] runs the overdamped gradient flow of this action's energy: 300 Lagrangian shells, Hernquist baryons, a central
surplus, code units G = a₀ = M_b = 1. Results:
- E_grav rises by +5.30e-3 (CFG932's "injection");
- E_W falls by −6.57e-3;
- E_total falls monotonically; the difference, 1.26e-3, is heat.

This is by construction for a gradient flow. The content is that **the surplus is expelled by tether energy already in
the action, so no dark-energy partner is needed. The energy is conserved once E_W and the dissipated heat are
booked.** The same conclusion is CFG747's conservative tether system, cited in CFG932 §4. CFG935 had no LEDGER row at
freeze time and is not compared.

## 5. Lensing and slip (Q4)

**Sources.** T₀₀ = ρ_c c²(1 + O(v²/c²)), so the medium lenses like mass. The tether sector does carry anisotropic stress:
p_r − p_t = −D(u)u/K = −gu/K on the law.

**Slip.** For a static sphere, Φ′ − Ψ′ = 4πG r p_r/c² at leading order (the TOV pressure term). With p_r = −W:

  s_∇ = |Φ′ − Ψ′|/Φ′ = 4πG r |p_r|/(c² g).

Measured on CFG847's own systems (both footings):

| system | v_c (km/s, can/alt) | s_∇ (can / alt) | s_847 (can / alt) |
|---|---|---|---|
| dwarf 1e7, 0.3 kpc | 20.8 / 21.6 | 1.4e-9 / 1.6e-9 (7e-9 / 8e-9 with stiffness at 1 kpc) | 3.6e-9 / 4.0e-9 (2.1e-8 / 2.3e-8) |
| MW disc 10 kpc | 208 / 214 | 6.8e-8 / 8.0e-8 | 2.5e-7 / 2.8e-7 |
| MW outer 100 kpc | 169 / 177 | 1.4e-7 / 1.6e-7 | 3.0e-7 / 3.3e-7 |
| group 1e12, 300 kpc | 345 / 360 | 5.6e-7 / 6.2e-7 | 1.2e-6 / 1.3e-6 |
| cluster 1.5e14, 1 Mpc | 1314 / 1363 | 5.1e-6 / 5.8e-6 | 1.4e-5 / 1.5e-5 |

Worst values: s_∇ = 5.8e-6 and s_847 = 1.54e-5. Both are below CFG847's largest (1.9e-5) and three orders below the
class line 1e-2 [S4]. The lensing–dynamics mass mismatch is s_∇/2.

*Caveat:* the medium here is cold, so CFG847's dispersion term is absent. If a multistream dispersion were added *on
top of* the tether stress, the cluster value would be ~3e-5. That is above 1.9e-5 but still far below 1e-2.

## 6. Well-posedness (Q5)

**Quadratic action** about a static medium, in WKB, in the rest frame, with background gradients dropped.
- Potential per mode: self-gravity −(K/2)|δρ|²/k², plus the tether ½∇δχ·Hess W·∇δχ with δχ = −Kδρ/k², plus the
  stiffness (γ/2)|δρ|².
- Kinetic: the rest mass, plus W(u) with u² = |∇χ|² + (v·∇χ)²/c².

Result [S5a]:

  ω² = c_s²k² + Kρ₀[R′(u₀)cos²θ + (R(u₀)/u₀) sin²θ]  (c → ∞),  c_s² = γρ₀,

with R′ = u(2a₀ − u)/(a₀ − u)² ≥ 0 and R/u = u/(a₀ − u) ≥ 0. The two transverse (vortical) roots are ω² = 0.

- The self-gravity −Kρ₀ is cancelled exactly, and over-cancelled, by the tether.
- Over kL* ∈ [1e-2, 1e5], all angles and u₀/a₀ ∈ {0.09, 0.5, 0.9, 0.99}: min ω²/(Kρ₀) = 0.100, 1.00, 9.0, 99.0. The
  maximum Im ω is 0 [S5b].
- **There is no growth at all, against CFG660's growth ∝ √k.** CFG678's B3/A2 failure is cured at the linear level.

**Inertia.** The inertia matrix is ρ₀δ_ij − (D(u₀)u₀/Kc²) ẑ_iẑ_j. It is positive iff **ρ_c c² > D(u)u/K**, i.e. the
rest energy exceeds the tether stress.
- On CFG847's systems the margin is 5.9e4 (cluster) to 2.5e8 (dwarf) [S5c].
- In screened regions (u ≈ Kρ_c r/3) the condition reduces to r < 3c/√(Kρ_c), which is always true below L*.
- This is a condition, not automatic.

**MUTATE M2** (γ → −γ): ω² < 0 at large k with Im ω = kL*/√2, a gradient instability (slope 1.0000).

**Degrees of freedom:** the medium (one longitudinal mode at c_s, two vortical modes at zero frequency) and the
graviton (two). χ and λ are constraints: elliptic, instantaneous in the medium frame [S5d].

**Not shown:**
- nonlinear well-posedness (A3);
- background-gradient (tidal) terms, which are order k⁰ and can give bounded growth, as for any self-gravitating fluid;
- behaviour after shell crossing, where the single-stream EFT ends (CFG939's domain);
- regions with no medium, where the medium frame does not exist (CONDITION: ρ_c > 0 everywhere, true at cosmic mean
  density).

## 7. Two structural consequences (found, not sought)

**(a) No linear self-gravity of the tethered medium: a D2 flag [S6].** In linear cosmology u ≪ a₀, so R ~ u²/a₀ is
second order. The medium then feels baryon gravity only (CFG888's "no self-gravity", now on FRW). Post-recombination,
matter era, Ω_c/Ω_b = 5.364:
- growth eigenvalue μ = 0.451, giving δ ∝ t^0.406 ∝ a^0.61;
- the record's class-A engine (Newtonian cold gravity; used by CFG650/T2x) gives a¹.

Before recombination the tethered medium follows photon-locked baryons only. So **the T2x shear pass does not transfer
to this parent.** It was computed with a different dynamical system, as astra's audit warns. D2 for this parent is
UNTESTED against its frozen line, and the flag is severe.

**(b) No gravity between tethered components [S8].** The 1-D mode average is

  ⟨L⟩_ID = πGB(B + 2C₁ + 2C₂)/k²,

against the Newtonian πG(B + C₁ + C₂)²/k². The C₁C₂ cross term vanishes. This is astra's C² cancellation (audit §4)
extended to two sources.

Tethered medium feels baryons (plus the residual R) but not the gravity of *any* tethered medium. Baryons and light feel
all of it. So CL-AR's premise (universal coupling) holds for fields sourced by baryons: uniform baryonic fields
free-fall out, with no EFE. It fails for fields sourced by tethered medium.

Consequence: a satellite's stars and its tethered medium fall differently in a host's medium field. For a 6e10 M☉ host
at 50–250 kpc that field is 0.03–0.17 a₀ (both footings). This is not one of CFG678's 20 gates. Its tension with
CFG925 R3 (no satellite EFE) is **UNTESTED and needs its own lane.**

## 8. Scorecard (CFG678's 20 gates; rules as frozen there)

| gate | status | source |
|---|---|---|
| A1 ghost / 2nd order | CONDITIONAL | positive inertia iff ρ_c c² > D(u)u/K (S5c); medium eqs 2nd order; χ/λ auxiliary; χ-tidal stiffness 4th order in space only |
| A2 hyperbolicity | CONDITIONAL | Euler with c_s² = γρ > 0 is symmetric hyperbolic; tether/gravity are order-0 elliptic terms; ω² ≥ 0 (S5b); needs γ > 0 + A1 inequality (CFG292's khronon line does not apply) |
| A3 nonlinear WP | UNTESTED | not proved; shell crossing ends the EFT |
| A4 strong coupling | UNTESTED | not computed |
| A5 GW at c | PASS | Einstein–Hilbert unmodified; no curvature couplings of the medium or χ: c_T = c (structural) |
| A6 BH exteriors | UNTESTED | no computation |
| A7 radiative | DECLARED | CFG320 |
| B1 switch from variation | UNTESTED | no switch term; S4 untethering not derived |
| B2 a₀–Λ tie | UNTESTED | a₀ constant in W; κ = ½ FITTED |
| B3 cold sector | CONDITIONAL | linear well-posed (S5); lenses like mass, slip ≤ 1.5e-5 (S4); one metric; CFG660 stress derived (S3c); conditions §10 |
| C1 Cassini | CONDITIONAL | spherical sector = S2 (CFG770); quadrupole sector differs (no P_T); baryonic uniform fields free-fall out; tethered-medium fields do not (S8) |
| C2 SPARC | PASS | static limit is the law (K1, 2.2e-16); CFG4 rms 0.1003/0.0991 ≤ 0.110 |
| C3 early types | FAIL | inherits CFG529 |
| C4 cluster lensing | NOT DECIDED | as CFG678 (CFG680 amplitude not frozen) |
| D1 zero field | UNTESTED | not run; tether sector ≡ 0 on FRW (S1d) |
| D2 growth | UNTESTED (flag) | CFG596 line not run; δ ∝ a^0.61 vs class A a¹ (S6) |
| D3 flat a₀(z) | PENDING | constant a₀; sealed tests 2026-11-06 / 2026-11-28 |
| E1–E3 | DECLARED | κ = ½ FITTED |

Relative to CFG678's "next action" specification:
- **B3/A2 move from FAIL to CONDITIONAL.**
- B1 stays unpassed.
- C3 stays FAIL.
- D2 is newly flagged against this parent.

## 9. Particle in disguise? (CFG723)

**Yes, for the mass.** F = −mc²n is the energy of a conserved number with rest mass m per element. Its gravitating and
inertial content is that of a cold matter component in the single-stream limit, and multistream flow needs a phase-space
(particle) description.
- The continuum EFT does not need quanta, because only ρ = mn is observable classically.
- But no gravitational observable distinguishes it from a cold species, exactly as CFG723 found.
- What is not a particle is the tether sector (χ, λ, W): it has no propagating mode.

Plainly: this is cold matter plus a non-propagating, long-range self-interaction whose equilibrium around baryons is the
law. This lane adds no particle species; it reports what the medium already is.

## 10. Class, conditions, and what is not claimed

**CONDITIONAL.** P1–P5 hold (law to 2.2e-16; conservation identities; ω² ≥ 0; isotropic w = 0 background; slip
1.5e-5), under these conditions:
1. Extra non-propagating fields χ (the medium's own potential, medium-frame constraint) and λ.
2. γ > 0, and ρ_c c² > D(u)u/K.
3. Stiffness realised on χ's traceless tidal tensor. The local-EoS realisation is BBN-excluded if the medium exists at
   BBN.
4. Matching to S2 only in the longitudinal sector: exact for spherical systems; non-spherical sectors differ from S2
   with an independent P.
5. Single-stream flow, with ρ_c > 0 everywhere.

**Not claimed:**
- κ, a₀, Ω_c/Ω_b or L* derived;
- nonlinear well-posedness;
- the non-spherical equivalence to S2;
- any data pass beyond C2;
- "theory closed".

## 11. Disclosures

- **A1 (post hoc, 2026-10-20, numerical; script only).** In the first full run the [S3e] flow used an explicit Euler
  step limited only by relative displacement. On the stiff shells near the u → a₀ wall it went unstable, and E_total
  rose by up to 7e-8 per record, so S3e FAILED. The step is now also limited by each shell's own curvature dF_k/dr_k,
  and E is monotone. The heat is unchanged to 4 digits (1.2613e-3). ΔE_grav and ΔE_W individually differ
  (run 1: +7.56e-3 / −8.82e-3) because the unstable integrator took a different path. The sign pattern
  (E_grav up, E_W down by more) is the same in both runs.

  The fix was made before the class was recorded as a result. The run-1 outputs are kept:
  `cfg938_firstrun_S3efail.out`, `cfg938_results_firstrun_S3efail.json`. Run 1 also printed CONDITIONAL, with
  "all checks pass: False".
- **A2 (post hoc, 2026-10-20, analysis added; script only).** [S8] was added after the first full main run. While
  scoring C1 I found that my own draft scorecard text ("uniform fields free-fall out: no EFE") was too generous: it
  ignored fields sourced by tethered medium. S8 corrects it. It is a result and a flag; it does not touch P1–P5 or the
  class rule.

  The S8 flag text was first written as "0.1–0.6 a₀" before the numbers existed. It was corrected to the computed
  0.03–0.17 a₀ before the final run.
- K, MUTATE and main were rerun in that order from the final script bytes. All outputs come from one version.
- M2's footing loop is redundant: the dispersion in units of √(Kρ₀) and kL* is footing-independent.
- The frozen Q4 "largest magnitude stress component" is p_t in every W-only row (|p_t|/|p_r| = 1.06–1.84, checked
  separately). The script takes the max in every row, including the stiffness rows.
- The WKB treats the background χ gradient as locally uniform (standard, as in CFG660 S5). Order-k⁰ tidal terms are
  dropped.
- Compute: one process, peak RSS 0.15 GB, ~7 s, run beside NC2x.
