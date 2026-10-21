# CFG955 DERIVATION: a kinetic parent for the class-A engine? (relaxing cold dust)

Criteria `FROZEN_CRITERIA.md` (903cd8f1d, committed alone first). Every load-bearing statement has a sympy or numeric check in
`cfg955.py` (check names in brackets; numbers from `cfg955.out` / `cfg955_results.json`). κ = ½ FITTED. Footings 9.3603e-11 /
1.1312e-10 m/s², never pooled. Cold energy is the framework's own component; no particle species. Not "theory closed". Nothing
here says the data favour the framework.

## 1. The kinetic theory, written out

### 1.1 Equations (reading K-T, the one the hypothesis's conservation clause demands)

    ∂ₜf + v·∇ₓf − ∇Φ·∇ᵥf = − Σ_D 1[x ∈ D, |x − X_b,D| < r_e,D] · (f − M[ρ_d, u, T_J,D]) / τ          (K1)
    ∇²Φ = 4πG (ρ_b + ρ_d),   ρ_d = ∫f d³v,   ρ_d u = ∫v f d³v                                         (K2)
    M[ρ, u, T](v) = ρ (2πT)^(−3/2) exp(−|v − u|²/2T)                                                  (K3)
    T_J,D(r) = (1/ρ_ph,D(r)) ∫_r^{r_e,D} ρ_ph,D(r′) g_law,D(r′) dr′,   r = |x − X_b,D|                 (K4)
    M_ph,D(<r) = r² [g_law(ḡ) − ḡ]/G,   ḡ = G M_b,own,D(<r)/r²,   M_ph,D(<r_e,D) = M_d,D                (K5)
    ∂ₜ e_R = −Q,   Q = ∫ (v²/2) C[f] d³v  (= (3/2) ρ_d (T_J − T)/τ for a local Maxwellian)                 (K6)

- **Dust.** Cold energy is ordinary collisionless dust: no tether and no phantom field. Gravity is plain Poisson, sourced by
  baryons and dust (K2).
- **Domains.** A domain D is born at first turnaround from the Hubble flow (E3's criterion, with no RMIN), and its identity is
  latched. Systems formed inside a collapsed domain are not domains (CFG953 R1). Cells are shared among domains by M1.
- **Target.** The own-domain MONOPOLE phantom of the condensed baryons (M2), centred on the condensed-baryon centroid X_b,D, cut at
  the supply root r_e,D where it exhausts the domain's dust (M1, zero-sum). T_J is its isotropic Jeans temperature in the law
  field, with zero pressure at r_e.
- **Reservoir.** R takes the energy moment of the collision term. Covariantly, ∇_μT^{μν}_d = −(Q/c)U^ν and ∇_μT^{μν}_R = +(Q/c)U^ν,
  so the momentum handed to R is Q u/c², O(v²/c²) of the exchange. Rest mass is untouched.
- **Rate.** τ is the open item (§9). The record's kinetic rate is CFG638's pressure-relaxation time, τ_π = τ_ff/(2α) with α = 1
  (T1).

### 1.2 The literal "density = phantom" target (reading K-ρ)

f_eq = ρ_eq M[u, T_J], with ρ_eq = ρ_ph inside r_e and (1 − q)ρ_d in the shell. This is class A's E6–E8 written as a target. It is
kept as the reading whose τ → 0 limit relocates mass like E8.

### 1.3 Why the brief's sentence has to be read as K-T

The hypothesis asks for two things at once:
- "f_eq's density is the phantom";
- "the relaxation conserves mass locally".

∫(f − f_eq) d³v = ρ_d − ρ_eq vanishes only where ρ_d already equals the phantom, so the two cannot both hold pointwise. K-T keeps
local conservation and moves "density = phantom" to the stationary state (§5). K-ρ keeps the density target and gives up
conservation (§2).

## 2. H0: what each reading conserves [H0_collision_moments: PASS]

For a local Maxwellian f = M[ρ, u, T] (sympy, three components):
- K-T: ∫C d³v = 0, ∫v C d³v = 0, ∫(v²/2) C d³v = (3/2)ρ(T_J − T)/τ.
- K-ρ: ∫C d³v = −(ρ − ρ_eq)/τ.

**K-T** conserves mass and momentum at every point. Its only non-conservation is the energy moment, which goes to R.

**K-ρ** has a source in its continuity equation:

    ∂ₜρ_d + ∇·(ρ_d u) = −(ρ_d − ρ_eq)/τ.

The O(c²) part of ∇_μT^{μ0} = 0 is exactly the continuity equation, so K-ρ violates covariant conservation at leading order. The
alternative is that a separate conserved sector carries the relocated mass, with a current from shell to edge. Then that sector is
CFG947's 𝒮, and T-M applies verbatim: the relocated weights change in a non-concentric domain, so R = Σ(s̈x + 2ṡẋ) ≠ 0 (CFG947 §3.2;
reproduced in K1). The planar toy shows the same thing directly (§4).

## 3. L1: the fast-relaxation limit, and why E8 is not it

**K-T as τ → 0** (Chapman–Enskog). The zeroth order is f = M[ρ, u, T_J], with stress ρT_J δ_ij and zero heat flux (sympy). The
dust then obeys Euler flow with a pressure p = ρT_J(x) held by the bath:

    ∂ₜρ_d + ∇·(ρ_d u) = 0,   ∂ₜ(ρ_d u) + ∇·(ρ_d u⊗u) + ∇(ρ_d T_J) = −ρ_d ∇Φ.

At first order the standard BGK results are η = ρT_Jτ and q ≈ −(5/2)ρT_Jτ∇T_J. At the record's rate (T1) the Knudsen number is
Kn ≈ 0.35 (CFG638 K7), so the hydrodynamic expansion is marginal there. The toy is kinetic and does not rely on it.

**Flow bound (theorem; follows from H0).** In any kinetic theory whose collision operator conserves mass locally, the gravitating
density ρ_b + ρ_d obeys continuity. After a catchment event, E8 fills the deficit ΔM inside r_e within one force evaluation, drawing it
from the shell r_e < r < r_ON. In the kinetic theory the mass inside r_e changes only by flux through r = r_e:

    |dM(<r_e)/dt| ≤ 4π r_e² ρ_d(r_e) v_max,

so for t − t₀ < ΔM / (4π r_e² ρ_d v_max), ‖ρ_KT(t) − S_E8‖₁ ≥ 2[ΔM − 4π r_e² ρ_d v_max (t − t₀)] > 0.

τ does not enter v_max: relaxation keeps u, a collision invariant, and the τ → 0 limit is Euler flow, whose signal speed at r_e is
at most |u| + √T_J, with T_J(r_e) = 0. So E8 is not the τ → 0 limit of K-T in any norm that sees where the mass is at fixed time
(L1, Wasserstein). At most it can be K-T's late-time attractor, for isolated hosts that relax and stay relaxed (relation ATTRACTOR,
§7). The toy measures this (§5.3, L1).

**K-ρ as τ → 0** sets ρ_d = ρ_eq inside r_e at once. That is E6–E8 with two differences:
- the clip is gone (K-ρ also removes native surplus; E6 keeps it);
- the relocation is of real mass rather than of active mass only.

## 4. L2: T-M is resolved by K-T (and only by K-T)

In K-T the gravitating weights are the dust masses themselves. They are constant and carried by the matter (s_j = m_j), so CFG947's
identity gives R = Σ(s̈x + 2ṡẋ) ≡ 0. The relaxation exchanges no momentum between cells, and Poisson gravity obeys Newton's third
law, so total momentum is conserved exactly. "Zero-sum" is no longer a prescription: it is mass conservation inside the domain.

## 5. (a) The law for isolated relaxed hosts

### 5.1 The stationary state is the law (a1, a2), and it has company (L5)

**Stationary state.** With T_J from (K4), ρ_d = ρ_ph inside r_e solves the Jeans equation d(ρT_J)/dr = −ρ g_law exactly, by
construction. The hydrostatic + Poisson ODE, integrated from 0.1 kpc with C = 1, reproduces the law on NGC 3198 (fixed-step RK4 on a
2 × 100001-point ln-r table; Υ = 0.61; supply-root edge 453.9 / 412.9 kpc, equal to E7's 454.0 / 413.0 to 0.03%):

| footing, kernel | a1: max \|g/g_law − 1\| at 43 radii | a2: y = 1e-2 / 1e-3 | V⁴/(G M_b a₀) at y = 1e-2 / 1e-3 |
|---|---|---|---|
| canonical, simple | **1.64e-6** | 3.1e-7 / 4.4e-8 | 1.105 / 1.032 |
| canonical, ν_mono | 2.87e-7 | 2.7e-7 / 2.1e-7 | 1.104 / 1.032 |
| alt, simple | **2.80e-6** | 1.6e-7 / 4.5e-7 | 1.105 / 1.032 |
| alt, ν_mono | 4.84e-7 | 2.6e-7 / 1.9e-7 | 1.104 / 1.032 |

- **a1 FAILS as frozen for the simple kernel** (line 1e-6). The phantom density is positive everywhere inside r_e (min ρ_ph/⟨ρ⟩ =
  0.336).
- PH1 (post hoc, A1.3) puts the largest deviation at the first data radius (0.32 kpc), the kink between the r³ interior and the
  PCHIP interpolant. Doubling N cuts it 7.6× (§12). So it is discretisation, not physics. The frozen grade stands.
- a2 passes. The BTFR holds, as the law's own V⁴/(G M_b a₀) shows.

**L5: NOT UNIQUE (NGC 3198, both footings and kernels; toy).** With T_J and the domain's dust mass fixed, the solutions are labelled
by their central normalisation C. Each case has a second root besides C = 1:

| | second root C₂ | root near 1 | F(C) on [1e-2, 1e2] |
|---|---|---|---|
| NGC 3198 canonical simple / mono | 0.467 / 0.534 | 1.00025 / 1.00025 | −0.001 … +0.169, not monotone |
| NGC 3198 alt simple / mono | 0.457 / 0.514 | 1.00026 / 1.00025 | −0.001 … +0.169 |
| toy (Plummer, r_* = 10) | 0.087 | 0.99998 | −0.407 … +0.051 |

F(C) ≡ M_d(<r_e; C)/M_c − 1. For NGC 3198 it stays within 0.1% of zero all the way from C₂ to 1. The enclosed dust mass therefore
selects the central normalisation only weakly. This is CFG946 O2d2's "nothing selects the law", now with a law-fixed temperature.

### 5.2 Dynamics: the law is not reached, and a settled start does not stay (a3)

Spherical shell toy (CFG935 harness; N = 10000; T1 = τ_ff/(2α), α = 1). Runs are capped at 30 min under A1.1.

| run | capped at t (t_e = 61.5) | dust inside r < 0.5 (law 0.0118) | D(W2) | ΔD | X_m | ON THE LAW |
|---|---|---|---|---|---|---|
| IC-L (settled law) | 27.5 | **0.690** | −0.585 | −0.304 | 0.656 | **no** |
| IC-I (cold infall) | 36.2 | **0.813** | −0.725 | −0.697 | 0.729 | **no** |
| IC-S (cold ×1.5 surplus) | 14.9 | **0.909** | −1.032 | −0.336 | 0.797 | **no** |
| fast probe τ/10, IC-I | 34.7 | **0.777** | −0.554 | −0.407 | 0.657 | no |
| MUTATE Mu5: relaxation off, IC-I (t = 650) | — | — | −0.117 | −0.037 | 0.462 | no |
| MUTATE Mu4: self-consistent target, IC-I (t = 650) | — | f_esc 0.80 | −1.121 | −0.228 | 0.866 | no |

**What happens.** Every K-T start collapses centrally: 69–91% of the dust falls inside r < 0.5, where the law holds 1.2%.
- The onset is at t ≈ 12–18, about 0.2 t_e.
- The relaxation sends 1042–1824 toy energy units to R, against a starting |E| of order 10, almost all of it on the cooling branch:
  cool / heat = 1042 / 0.95 (IC-L), 1454 / 2.6 (IC-I), 1824 / 3.7 (IC-S).

**Why the energy books are poor.** ε_E = 0.31 – 1.6 at the cap. Once the core has formed, it is integrated inside the softening at
dt ≈ 1e-5. This affects the late states, not the onset: PH3 (§12) shows the collapse beginning while the books still close.

**Robustness (PH3).**
- Present at N = 40000.
- Present with softening ×5.
- Present at τ/10.
- Present with relaxation forbidden inside r = 0.24.
- Absent with relaxation off: the law state is kept (0.0136 inside r < 0.5 at t = 40).

**a3: FAIL.**

**Grade (a): FAIL.** a1 fails (simple kernel, numerically), a3 fails, L5 is NOT UNIQUE. Under A1.2 the (a) FAIL is generic through
L5: the hydrostatic family does not select the law, and the dynamics do not reach or keep it.

### 5.3 L1 and the engine relation

- **Fast probe.** τ/10 never brings ‖ρ_d − ρ_ph‖₁/M_c below 0.1 (line: by 0.1 t_e = 6.15). It collapses like T1. **L1: NOT a τ → 0
  limit.**
- **Attractor.** The T1 runs do not end ON THE LAW, so E6–E8's source is not K-T's late-time state either.
- **Engine relation: NONE** (frozen §7).

### 5.4 Interpretation (post hoc, A1.3 PH4; no class weight)

In the fluid limit K-T is dust held at the fixed temperature profile T_J by the bath. Radial perturbations obey a Sturm–Liouville
problem whose self-gravity term is negative. For the deep-law SIS phantom (T_J = v_c²/2, ρ ∝ r⁻²; the GF2 audit's SIS, v_c⁴ = G M_b a₀)
it reduces to

    −y″ − 2y/r² = (2ω²/v_c²) y.

- Its zero-frequency solutions are r^((1 ± i√7)/2) (sympy). They oscillate in ln r with spacing 2π/√7 = 2.375.
- By Sturm's theorem, a mode with ω² < 0 exists once the deep SIS region spans r_out/r_in > e^(2π/√7) = 10.75.

This is the Bonnor–Ebert / Antonov instability of a thermostatted singular isothermal sphere. In the toy and NGC 3198 the deep region
runs from about r_M to r_e = 6–54 r_M, which crosses that threshold. The eigenvalues computed in PH4 are listed in §12.

A heat bath is what K-T needs to close its energy books (§8), and a heat bath at T_J is exactly what destabilises the law's own SIS
profile. Mu4 shows the other side: without the law's T_J (a self-consistent target) the dust is not held at all (f_esc 0.80).

## 6. (b) Satellites: no hover, no EFE, and the multi-stream drag [L4, L6: PASS]

**b1 (hover).** The uniform-field operator drops out of Vlasov + BGK in the falling frame (sympy residual 0; local-Maxwellian shift
covariance 0), because f_eq uses the local u and a T_J that moves with its own baryons. Planar toy, satellite in g = 1 for t = 50:
fitted ε = 3.9e-4 (line 1e-2); |ΔP + Mgt|/(M v_ref) = 1.9e-12. **PASS.**

**b2 (EFE).** 0 dex at monopole order: the target is the own-domain monopole, so there is no global phantom. The M1 radius of each
satellite's own domain covers its Plummer radius in all 18 cases (s_M1 = 0.28–17 kpc against a = 0.03–0.7 kpc). It cuts below the
satellite's own edge only for H2 and H3 at 50 kpc (0.86 vs 1.14 kpc; 3.5 vs 9.3 kpc). **PASS.**

**b3 (drag; L6).** Relaxation to the local mean velocity drags a satellite's dust toward the host's dust stream:

    ε_drag = [ρ_h/(ρ_s + ρ_h)] V/(τ g_host).

| τ | worst ε_drag(a), can / alt (line 0.344 / 0.317) | H3 at 50 kpc: ε(2a); r_s/a | \|δ\| at a |
|---|---|---|---|
| T1 τ_ff/2 | 0.211 / 0.210 | 0.381; 2.43 | 0 |
| T2 k = 0.46 / 0.52 | 0.028 / 0.024 | 0.058; 7.5 | 0 |
| T2 k = 1.20 | 0.011 / 0.011 | 0.022; 59 | 0 |
| T3 0.72 / 0.83 Gyr | 0.0042 / 0.0035 | 0.015; 7.9 | 0 |
| T3 3.47 Gyr | 0.0009 / 0.0008 | 0.003; 19 | 0 |

- Every candidate passes at a. T1 is the closest, at 61% / 66% of the line.
- At 2a, T1 reaches 0.38, beyond ε_B (reported, no grade).
- **Grade (b): PASS** (b3 passes with the τ-P candidates T1, T2-fast and T3-fast on both footings).

**b4 Bullet (reported).** Fraction of the sub's dust relative momentum removed in one core crossing:
- T1: 0.43 / 0.45 (canonical / alt);
- T2 and T3: 0.007–0.063.

At T1 the dust of colliding clusters is partly collisional. This is CFG623's "mergers want α = 0" tension, reappearing in kinetic
form. The planar merger E-M sends 7472 toy units of the colliding streams' relative kinetic energy to R.

## 7. (c) slip, (d) growth, (e) conservation, (f) causality

**(c) Slip.** The isotropic dust pressure p = ρ_ph T_J of each CFG847 system's relaxed state (exact T_J, own edge):
- worst s_grad = 6.8e-6; worst s_847 = 1.355e-5 (line 1.9e-5);
- T_J/v_c² at the systems' radii is 0.37–0.47, the SIS value ½ being reached only in the deep regime.

**PASS.**

**(d) Growth.**
- Dust exponent n = 1.000000000000 (CFG941 machinery, c₂ = 0).
- C[f] ≡ 0 for a cold stream when T_J = 0 (no condensed baryons before collapse).
- The top-hat reaches turnaround (9π²/16 = 5.5517) at δ_lin = 1.0624, so no domain exists in the linear regime.

**PASS.**

**(e) Conservation** (planar toy; exact pairwise sheet gravity; per-cell, subset-mean momentum-preserving relaxation):

| run | sheets | \|ΔP\|/(M v_ref) | booked \|ΔE\|/\|E\| vs integrator (relaxation off) | E_R | M1 switches; max T_J jump |
|---|---|---|---|---|---|
| E-R asymmetric host | 12000 | 8.4e-12 | 1.04e-4 vs 1.10e-4 | +32.7 | 0 |
| E-S satellite infall | 13200 | 1.1e-12 | 1.34e-4 vs 1.06e-4 | +476 | 5270; 0.95 T₀ |
| E-M merger | 24000 | **1.04e-10** | 3.33e-4 vs 3.69e-4 | +7472 | 41846; 0.76 T₀ |

- Mass is exact in every run (integer counts).
- **(e) FAILS as frozen**: E-M's momentum line is 1e-10, and it reaches 1.04e-10.
- The relaxation-off E-M run reaches 8.6e-11 by itself. The miss is the floating-point round-off of O(N) cumulative force sums with
  24000 sheets over 5000 steps, not the relaxation. Under the frozen class text it has no generic statement (A1.2).

**(f) Causality.**
- f1: the operator ∂ₜ + v·∇ₓ − ∇Φ·∇ᵥ has characteristics dx/dt = v (speed ≪ c), and the collision term is local in x with finite τ.
- f2: T_J is a domain-wide functional (the monopole of the domain's condensed baryons, the supply root of its dust mass, and the M1
  partition). It is causal only with retarded domain fields (C-ret; CFG947's N1 / N2-B construction).
- f3: the relaxation is dissipative, so there is no action principle and CFG678's one-action rule cannot be met.

**Grade (f): CONDITIONAL (C-ret).**

## 8. The reservoir R: what it has to be [L7_second_law: PASS]

From the local-Maxwellian moments (sympy), with s = ρ[(3/2) ln T − ln ρ] and Q = (3/2)ρ(T_J − T)/τ:

    dS_d/dt − Q/T_J = (3/2)(ρ/τ)(T_J − T)²/(T T_J) ≥ 0.

This is the Clausius inequality for dust in contact with a heat bath at temperature T_J(x). Two consequences:
- **On the cooling branch (T > T_J)** the dust's entropy falls, dS_d/dt = (3/2)ρ(T_J − T)/(Tτ) < 0. The second law then requires R
  to absorb entropy at a rate of at least −Q/T_J > 0.
- **CFG542 Pb** requires the record's dark-energy partner to be coherent (zero entropy). A zero-entropy reservoir can absorb work
  but not entropy, so **it cannot be K-T's R on the cooling branch**.

Hence R must be a genuine heat reservoir whose local temperature equals the law's Jeans temperature of the host's own baryons. That is
CFG935's post-hoc reservoir (ii), "a heat bath at the local Jeans temperature σ_J²(x)".

**The drift partner is not needed.** CFG935's reservoir (i) took the drift's work. K-T has no drift: mass moves by flow, and
momentum is conserved.

**What R must also do.**
- Its temperature field is set non-locally, by the monopole phantom of each domain's condensed baryons and that domain's dust mass.
  It carries the law's own scale a₀, since T_J ≈ v_c²/2 = √(G M_b a₀)/2 deep in the law.
- It must exchange energy in both directions at large gross rates (§10).
- No such field is in the record. CFG544 found no named partner for P_bath. This is the theory's principal new-physics cost.

## 9. What sets τ (§3 of the criteria)

### 9.1 Class rows

CFG939's N5 systems, canonical footing (alt within 5%): r½ (kpc), age (Gyr), local τ_ff = (4πGρ_m)^(−1/2) (Gyr), t_orb (Gyr), and
the fraction of the law-state Maxwellian below V_esc,b (T5).

| system | r½ | age | τ_ff | t_orb | T5 fraction |
|---|---|---|---|---|---|
| UFD-c / UFD-e | 0.039 / 0.31 | 13 | 0.013 / 0.066 | 0.10 / 0.52 | 0.041 / 0.008 |
| Draco-like / Fornax-like | 0.29 / 0.93 | 12 | 0.030 / 0.031 | 0.23 / 0.24 | 0.062 / 0.218 |
| SPARC dwarf | 5.0 | 10 | 0.096 | 0.68 | 0.108 |
| MW-like | 8.0 | 10 | 0.045 | 0.27 | 0.617 |
| slowest SPARC last-point orbit (CFG764) | — | 8 | 0.46 | 2.91 | — |
| cluster core | 500 | 6 | 0.42 | 3.41 | 0.819 |

Two-body relaxation with stars as scatterers (T4) takes τ_2b = 2e3 Gyr (UFD-c) to 5e15 Gyr (cluster), and it is infinite for the dust
continuum.

### 9.2 Relaxed fraction R = 1 − e^(−age/τ)

States: ON LAW if R ≥ 0.9, NATIVE if R ≤ 0.1, MIXED otherwise. Canonical footing:

| candidate | SPARC dwarf | MW-like | slowest SPARC | cluster core | Draco / UFD-c | τ-P | τ-F |
|---|---|---|---|---|---|---|---|
| T1 τ_ff/2 | ON | ON | ON | ON (1.000) | ON | **yes** | no |
| T2 k = 0.46 | ON | ON | ON (0.997) | ON (0.978) | ON | **yes** | no |
| T2 k = 1.20 | ON | ON | MIXED (0.899) | MIXED (0.770) | ON | no | no |
| T3 0.72 Gyr | ON | ON | ON | ON (1.000) | ON | **yes** | no |
| T3 3.47 Gyr | ON (0.944) | ON | ON (0.900) | MIXED (0.823) | ON | no | no |
| T4 two-body | NATIVE | NATIVE | NATIVE | NATIVE | NATIVE | no | no |
| T5 capture gate | 0.108 < ½ | 0.617 | — | 0.819 | 0.04–0.06 | no | no |

Alt footing: the same pattern, with T2 at k = 0.52 and T3 at 0.83 Gyr.
- T5 shows that a per-element capture gate cannot hold the deep law. Only 1–22% of the law-state dust lies below V_esc,b in the
  dwarfs and the SPARC dwarf, because V_esc,b/v_c ≈ √2 y^(1/4) ≪ 1 deep in the law.
- The capture criterion in its CFG939 sense (a system moving through ambient dust faster than its own baryonic escape speed captures
  none) is kept by L6 for every τ: relaxation preserves a stream's mean velocity in a domain with no own dust. So tidal dwarfs and
  DF2/DF4 stay Newtonian in K-T, as in situ or no-capture systems. They are not domains (CFG953 R1), and the host dust at their
  location adds CFG953 A1's +0.02 to +0.11 dex.

### 9.3 The ordering obstruction (any proportionality constant)

A local clock τ = c·t(r) can give τ-F only if min over rotators of (age/t), divided by the cluster core's age/t, is at least
ln 10 / ln(10/9) = 21.85. Computed:

| clock | canonical | alt |
|---|---|---|
| t = τ_ff | 1.21 | 1.17 |
| t = t_orb | 1.56 | 1.50 |

These are short of the line by a factor of about 14–19.
- **Universal clock.** τ-F needs τ ≤ 3.5 Gyr (rotators ON LAW) and τ ≥ 57 Gyr (cluster core NATIVE, age 6 Gyr) at once.
- **Verdict: NO RECORD-DERIVED τ WORKS.** No candidate makes cluster cores native while keeping rotators on the law. CFG949's
  "clusters untethered" therefore gets no derived selector from finite τ, and the selector remains a choice (as CFG954 found inside
  SCT).
- **Cluster bands** (reported, approximate harmonic mixture of CFG687's law and CFG949's B0) at each candidate's cluster R:
  - canonical: MID 1.59–1.91 (Z +5.9 to +7.7), OUTER 1.01–1.02;
  - alt: MID 1.51–1.75 (Z +5.4 to +6.9), OUTER 0.93–0.95.

  The core deficit survives every record τ.

### 9.4 T-EX: the excess family is out of reach at any τ [T-EX_excess_unreachable: PASS]

- K-T's relaxed state is the law. Its unrelaxed state is native dust, and CFG930 D4 puts native dust below the settled phantom inside
  every dwarf aperture. Median Q_ap:
  - canonical: U 0.153, C 0.320, M31 Collins 0.284, M31 LVD 0.297, I 0.261;
  - alt: 0.139 / 0.290 / 0.257 / 0.270 / 0.237.
- Every mixture of the two therefore sits at or below the law. No τ produces the dSph excess (+0.37 dex stars-only, CFG860 / CFG873)
  or the Coma UDGs' +0.76 / +0.67 ln (CFG948).
- Extra dust in a domain only moves the supply edge outward. It does not raise the law inside it.

## 10. Energy (task 4)

**E1: net exchange per host = E_start − E_end.**
- E_end is the Jeans-supported truncated law, the same state as CFG935's N-type law. So K-T's net exchange is CFG935's E_x (PHYS
  table, read exactly), and the sign is dust → R for native-debris starts.
- Canonical: UFD-c 1.63e49 erg (3.4e-11 M_cat c²); UFD-e 1.60e50; Draco-like 1.57e52; Fornax-like 1.06e55; SPARC dwarf 2.82e56;
  MW-like 2.38e59 (4.1e-8 M_cat c²); cluster core 7.34e63 erg (3.0e-6 M_cat c²).
- Alt: 1.78e49 … 9.15e63 erg.

**Power E_x/τ** (canonical):
- MW-like: 3.3e44 (T1) down to 2.2e42 (T3, 3.47 Gyr) erg/s, i.e. 8.7e10 – 5.7e8 L⊙;
- cluster core: 1.1e48 – 6.7e46 erg/s.

R must take this out of sight. As radiation it would be a new massless field with Ω ≤ 5.5–7.5e-7 (CFG935). As vacuum energy it is
Δρ_DE/ρ_DE ≈ 0.8–1.1e-6 since z = 1, which a coherent partner cannot take (L7).

**E2: gross flows in the toy.** Every K-T start sends far more energy to R than it receives:

| start | cool (dust → R) | heat (R → dust) |
|---|---|---|
| IC-L | 1042 | 0.95 |
| IC-I | 1454 | 2.6 |
| IC-S | 1824 | 3.7 |

These cooling flows are the collapse (§5.2). The toy's start-minus-law energies are only +0.90 (IC-I) and −8.6 (IC-S): the
relaxation does not stop at the law's energy, it keeps extracting binding energy from the collapsing core.

**E3: CFG930/932's ordering.** It is **NOT APPLICABLE**: R is not baryonic feedback, and its capacity is not tied to E_SN. The
ordering therefore **DOES NOT KILL** K-T. Separately, T-EX holds: the excess family stays out of reach at any τ.

## 11. Classes

### 11.1 Per reading

| reading | conservative | (a) | (b) | (c) | (d) | (e) | (f) | engine relation |
|---|---|---|---|---|---|---|---|---|
| K-ρ | **no** (H0; toy CM slip 7.5e-3 x_e, \|ΔP\| 8.2e-3) | — | — | — | — | — | — | (τ → 0 = E6–E8 minus the clip, but not conservable) |
| K-T | yes (H0, L2) | **FAIL** | PASS | PASS | PASS | **FAIL** | CONDITIONAL | **NONE** |

### 11.2 Overall (frozen §7 with A1.2)

- **CONDITIONAL is excluded:** K-T has FAILs and relation NONE.
- **NO KINETIC PARENT** needs every FAIL to be covered by a listed structural statement:
  - the (a) FAIL is covered by L5 (a3 fails, NOT UNIQUE);
  - the (e) FAIL, the merger toy's momentum at 1.04e-10 against 1e-10, has no listed statement.
- **Frozen-rule outcome: NOT CLASSIFIED BY THE FROZEN RULE.**

### 11.3 Post-hoc reading (no class weight)

(e)'s miss is the integrator's round-off: relaxation-off gives 8.6e-11, and E-R / E-S stay at 1e-12 – 1e-11. Read that way, the only
physics FAIL is (a). It is generic three times over:
- L5: the hydrostatic family does not select the law;
- a3: every start collapses;
- PH4: the thermostatted SIS is linearly unstable.

So the substantive class is **NO KINETIC PARENT** for the hypothesis as stated. The obstruction rests on three proven pieces:
1. **H0:** the density-target reading K-ρ, the only one whose fast limit relocates mass like E8, is not locally conservative.
2. **L1:** no locally mass-conserving kinetic theory has E8 as its τ → 0 limit (flow bound).
3. **L5 + a3 (+ PH4):** the conservative reading K-T, which resolves T-M, T-R and T-X, does not hold the law. The heat bath its
   energy books require (L7) is the thing that destabilises the law's own SIS profile.

### 11.4 What is not excluded

- **Kinetic theories with a relocation drift** (CFG638's v_s, CFG935's post-hoc PH-OU). These held the law in CFG935, but their drift
  is a non-conservable relocation (T-M) and needs a dark-energy partner.
- **A collision operator whose target temperature is not the law's** (for example the self-consistent CFG554 target, which Mu4 shows
  does not reach the law).
- **Kinetic theories with additional degrees of freedom.**

None of these is the brief's hypothesis.

## 12. Post hoc (A1.3; reported, no class weight)

**PH1, a1 convergence** (simple kernel; max |g/g_law − 1|):

| nodes | canonical | alt |
|---|---|---|
| 100001 (frozen) | 1.64e-6 | 2.80e-6 |
| 200001 | 2.15e-7 | 5.27e-7 |
| 400001 | 4.95e-7 | 1.85e-7 |

- The largest deviation sits at 0.32 kpc, the first data radius, where the r³ interior meets the PCHIP interpolant.
- Convergence is non-monotone at that kink, but every finer table passes 1e-6.

**PH2, the second equilibrium** (same T_J; total dust mass equal to 1e-3):
- On NGC 3198 the law deviation is 0.195 / 0.168 / 0.207 / 0.182 at C₂ (canonical simple / mono, alt simple / mono), and
  0.137–0.144 / 0.080–0.084 / 0.030–0.031 at C = 0.6 / 0.75 / 0.9. The maximum sits at 1.9–2.9 kpc.
- In the toy, C₂ = 0.087 holds M_d/M_ph = 0.23 / 0.52 / 0.81 at r = 2 / 5 / 8.

**PH3, collapse diagnostics** (IC-L, 200 s caps). Onset is the first time more than 1% of the shells lie inside r < 0.05.

| variant | onset t | inside r < 0.5 at the cap (law 0.0118) |
|---|---|---|
| frozen | 13.0 | 0.24 (t = 14.6) |
| N = 40000 | 13.0 | 0.13 (t = 13.45) |
| softening 0.1 | 13.5 | 0.60 (t = 22.8) |
| τ/10 | 17.0 | 0.22 (t = 19.1) |
| no relaxation inside r = 0.24 | 15.0 | 0.54 (t = 20.9) |
| relaxation off | none to t = 40 | 0.0136 |

The onset times are deterministic. The fractions at the cap depend on how far each capped run got (the committed `cfg955_posthoc.out`
comes from the second post-hoc run, which added PH5; its fractions agree with the first run to the digits shown).

**PH4, thermostatted linear stability.**
- SIS exponents s = ½ ± i√7/2 (sympy); zero spacing 2π/√7 = 2.3748 in ln r; instability threshold r_out/r_in > 10.749.
- Lowest ω² by finite differences (4000 points, Dirichlet at r_in and 0.999 r_e):
  - toy: −0.038 (one negative mode; e-folding time 5.13, against an onset at about 13);
  - NGC 3198: two negative modes in every footing/kernel; fastest ω² from −1.6e-32 to −2.3e-32 s⁻², i.e. e-folding times of
    0.24 / 0.25 Gyr (canonical simple / mono) and 0.21 / 0.22 Gyr (alt).

**PH5, energy books through the onset** (frozen K-T, IC-L):

| t | ε_E | E_R | inside r < 0.05 |
|---|---|---|---|
| 5 | 2.8e-7 | −0.03 | 0 |
| 10 | 1.0e-6 | +0.46 | 0 |
| 12 | 1.4e-6 | +1.32 | 0.0004 |
| 13 | 5.5e-5 | +6.4 | 0.056 |
| 13.5 | 1.9e-6 | +28.3 | 0.120 |
| 14 | 6.0e-4 | +57.4 | 0.165 |

The collapse starts and runs to 17% of the shells inside r < 0.05 with the books closed to ≤ 6e-4. The large ε_E of the capped MAIN
runs comes later, from integrating the formed core inside the softening.

## 13. Controls

**K (8/8 PASS; identical in the K stage, in MAIN, and in the final-script rerun):**
- K1: CFG947 T-M (identity 0; E8 R form; π²ε/4 = 0.0247 / 0.2467 / 0.7402).
- K2: T-R (4.8154e10; NGC 3198 r_ON 0.7761 Mpc/h, unresolved; 128 / 175).
- K3: T-X (36 values, −0.7298 … −0.1019 dex).
- K4: CFG938 NGC 3198 law (2.22e-16 / 2.22e-16).
- K5: CFG952 node 1.0471 Mpc/h → 2.185e11 M⊙.
- K6: CFG941 0.609545 / 0.694330 / 1.000000000000.
- K7: CFG935 PHYS read; toy T_J against CFG935's σ_J², 2.8e-4.
- K8: SPARC 0.10033 @ 0.61 / 0.09910 @ 0.57; Newton 0.2755.

**MUTATE (5/5 bite; exit 1 by design):**
- Mu1: tether n = 0.694330, against relaxation-only n = 1.
- Mu2: global phantom EFE −0.7298 … −0.1019 dex, against own-domain 0.
- Mu3: K-ρ CM slip 7.5e-3 x_e (velocities kept) and |ΔP|/(M v_ref) 8.2e-3 (local velocities).
- Mu4: self-consistent target D(W2) −1.121, f_esc 0.80.
- Mu5: relaxation off D(W2) −0.117, X_m 0.462.

## 14. Disclosures

1. **Criteria and expectations.** The criteria were frozen before any script (903cd8f1d). The coordinator's note that CFG953's
   pointwise phantom fails was adopted before the commit. Expectations 1–6 and 8 held. Expectation 7 resolved as FAIL. The collapse
   was not foreseen.
2. **Implementation fixes before any graded number:**
   - quadrature atol scaled to the pressure (the first attempt failed at step 1);
   - a vectorized fixed-step RK4 replaced an adaptive solver (52 s per integration, too slow for the frozen 401-point scan);
   - the toy relaxation cadence is 0.05.

   Smoke tests on very short runs, crash-only, were made in a scratch directory.
3. **A1** (d11d47794; dated 2026-10-21) covers:
   - the wall cap;
   - the literal class rule (the first code fell back to NO KINETIC PARENT on any FAIL, which does not implement the frozen clause);
   - PH1–PH5.

   It was written after MAIN attempt 1 had printed the static lines (a1, L5) and after the scratch collapse diagnostics, and before
   any graded toy number.
4. **MAIN attempt 1** was stopped by hand (verified PID; my own process only). Its partial output is kept as
   `cfg955_firstrun_stopped_toycollapse.out`; its static lines are identical to the final run's.
5. **(e)'s 1e-10 momentum line** was set without a round-off estimate for 24000 sheets. The relaxation-off control shows the
   integrator alone reaches 8.6e-11. The frozen grade is kept.
6. **Inherited inputs:**
   - the census f_ret and the engine's M_ta constants;
   - CFG939's representative systems and nominal ages;
   - CFG930's Q_ap and CFG935's E_x (both read from their JSON);
   - CFG949 / CFG687 band amplitudes for the reported cluster mixture, which assumes similar shapes within a band (an approximation).
7. **Two-body estimate (T4).** All baryons are counted as 1 M⊙ scatterers. This favours relaxation and still gives ≥ 2e3 Gyr.
8. **Compute.** One process at a time, one core, nice 10, peak RSS ≤ 0.35 GB, no downloads. No other lane, LEDGER,
   THEORY_CANONICAL file, sol61_push/ or campaign_fresh_gravity_astra/ was edited.
