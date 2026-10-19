# Complete acceleration response of the original cold-energy particle model

**CHECKPOINT: CL-AR-2026-10-19-01** (19 October 2026).
Brief: `sol61_push/HANDOFF_TO_CLAUDE_2026-10-19.md`, "Next executable work"
item 1 only. Parent research checkpoint: CE-FM093 /
CE-NONLINEAR-ORIGIN-2026-10-19. The handoff bundle verified (411 files,
archive SHA-256 `734c315f010b888c5e7aae4e5eee77424b3c44442d1812e0e57474003fd4cca4`)
and was read from a scratch extraction. No existing file was modified.
Master action bytes used by the parent: SHA-256 `c81b4a31…0bbe43`.

**The theory is not closed. The original prediction target stays OPEN.**
This note derives the acceleration response that any spectrum or occupation
must feed into. It is not a derivation of the galaxy law.

---

## 0. Verdict

1. **Uniform acceleration (affine limit).** No source-carrying response
   survives in the original action. The result is exact in the Galilean
   (Newtonian/Bargmann) effective theory: it holds at every order in E, for
   every state (pure, thermal, entangled, prepared), for time-dependent
   E(t), and for every host, support and receiver body that belongs to the
   system. The complete response is a rigid translation of the total COM.
   Remove only that, and every internal observable and every COM-centred mass
   multipole is unchanged (§2). A nonzero uniform-field response needs either
   unequal passive/inertial mass ratios or an external anchor. The action
   contains neither.
2. **Finite wavelength.** The static responses that do exist are listed in §4.
   A centred closed object gives O(k⁴); a medium of free composites gives
   α = O(k²); a supported compressible medium gives a Jeans kernel with one
   marginal wavenumber; a supported *insulating* dielectric gives a
   k-independent α, but only with an incompressible static support. None of
   them supplies the target's linear term across a band of wavelengths. An
   exact positive-energy transport budget (§5) then excludes **every local
   displacement mechanism** as the origin of the law's medium mass, for
   positive-energy carriers in any microscopic phase.
3. **First missing selection equation (§6):** scale-free gravitational
   marginality of the low-field medium, h_med(k) = 4πG/k² (equivalently
   g_med/g → 1 as g → 0). In Gauss form it becomes
   4πG Σ_med(<r) = a0 g/(a0+g). The original action does not supply it.
   What is missing is a mechanism, not a parameter value. The only branch not
   excluded here is a non-static, non-local supply (assembly over ℓ ≳ r), and
   there the equation becomes a supply law that still has to be derived.

Not claimed: an all-phase no-go, a statement about strong-field GR, or any
comparison with data.

---

## 1. Contract: state, bodies, metric source, observable

**Action and material state.** The scalar sector is the matched daughter
EFT of the original action: field ψ of mass m, contact
g₂ = λ_rep/(2m²), Newtonian self-gravity, and X eliminated with no double
counting. Explicit X conversion with M ≠ 2m violates Bargmann mass
superselection at NR order. For that case the gravitating centre is the total
energy centre of the record (CE-FM-087 internal_polarization eqs. 8–9, valid
at linear order in E). The baryons are modelled as follows:

* stars are collisionless point bodies;
* disc gas is a barotropic fluid in near-rotational support;
* hot gas is hydrostatic;
* host cores use the record's ideal degenerate γ = 5/3 closure
  (EQUILIBRIUM.md) when a specific state is needed.

Supports (solids, walls, traps) and heat receivers are any further
Galilean-invariant positive-mass subsystems. All of them belong to the closed
system. No external non-gravitational agent exists in the action.

**Free versus supported.** "Supported" means a non-gravitational force density
f acts, so the body's acceleration relative to local free fall is
a_rel = ẍ − g = f/ρ ≠ 0.

| body | status in a disc galaxy | a_rel/g |
|---|---|---|
| stars | geodesic | 0 exactly |
| disc gas | rotation-supported, small pressure support | ≈ (c_s/v_c)²·\|dlnP/dlnr\| = 0.08 / 0.02 / 0.005 for v_c = 50/100/200 km s⁻¹, c_s = 10 km s⁻¹, \|dlnP/dlnr\| = 2 (illustration) |
| hot halo gas | pressure-supported | ≈ 1 |
| scalar clouds bound to hosts | share their host's a_rel | as host |
| diffuse scalar medium | geodesic if orbiting or collisionless; supported only if hydrostatic | 0 or ≈ 1 |
| supports, receivers | internal to the closed system | — |

**Metric source.** ∇²U = 4πGρ with ρ = m|ψ|² + ρ_b + ρ_support +
ρ_receiver, each counted once. At O(1/c²) the source is the total T⁰⁰,
including conversion and binding energy, through the record's energy-centre
theorem. For non-relativistic sources Φ = Ψ, so lensing sees the same mass as
dynamics.

**Measured observable.** The observable is the acceleration of free tracers
relative to the galaxy centre: g_obs = −∇U_int (rotation curves, RAR, and the
same Σ for lensing). In the medium language the law's "polarization" is
bookkeeping for the medium's mass profile. For spherical symmetry
p ≡ Σ_med(<r) = M_med(<r)/(4πr²), and the target reads

  4πG Σ_med(<r) = a0 g/(a0+g),  equivalently  M_med(<r) = r²(g − g_N)/G.

`transport_budget.py` C1 checks this identity numerically. The observable
is the medium's monopole (enclosed mass), not an internal dipole.

---

## 2. Affine limit: exact theorem

**Theorem 1.** Take a closed system of Galilean-invariant constituents. Each
constituent has passive gravitational mass equal to its inertial mass, and
the conserved Bargmann mass is M = Σm_a. Place it in U_ext = −E(t)·x. Then

  H(E) = [P²/2M − M E·R] + H_int(y, π),  [H_COM(E), H_int] = 0,

with y_a = x_a − R and π_a = p_a − (m_a/M)P. Consequently
e^{−iH(E)t} = e^{−iH_COM(E)t} e^{−iH_int t}, and every internal reduced state
evolves independently of E. At field level the nonlinear shared GP–Euler–
Poisson state obeys the Avron–Herbst map

  ψ_E = ψ₀(x−ξ,t) e^{i[mξ̇·x − S]/ħ},  S' = m|ξ̇|²/2,  ρ_bE = ρ_b0(x−ξ,t),
  v_E = v₀(x−ξ,t) + ξ̇,  U_E = U₀(x−ξ,t),  ξ̈ = E(t),

which sends solutions to solutions. Residuals map exactly, for any barotrope
P(ρ) and contact g_c.

The complete source response is therefore δρ(x,t) = ρ₀(x−ξ(t),t) − ρ₀(x,t).
Its only invariant content is the COM trajectory. Remove the total COM and
nothing remains for any body: no internal dipole, no change in any higher
multipole, no change in any population, gap or support stress.

Evidence: `affine_exact.py`.

* A1–A4: three bodies in 3D with arbitrary pair potentials.
* B1–B3: N = 4 commutator algebra, the kinetic split and −E Σm_a x_a = −M E·R.
* C1–C3: 3D field-level covariance with arbitrary E(t).
* D1, D6: closed chain, exact trajectory from a relaxed start.

These checks extend the record's classical-Lagrangian separation (CE-FM-087
eqs. 3–4) to the quantum many-body, thermal and nonlinear field level, with
supports and receivers included explicitly.

**Corollaries.**

* *The only source of a uniform-field response.* With passive charges γ_a,
  internal accelerations change by (γ_a/m_a − Σγ/M)E (A3). Minimal coupling
  gives zero (A4). This matches the record's eq. 19.
* *A heavy free host or support is not an anchor.* The internal extension is
  0 for every m_s, including m_s → ∞ (D2). Only an external anchor spring k₃
  gives the static sag m_c E/k₁ (cloud–host) and (m_c+m_h)E/k₂ (host–support),
  and that sag is independent of k₃ > 0 (D3). The limits do not commute (D4):

  lim_{ω→0} lim_{k₃→0} Δ = 0,  lim_{k₃→0} lim_{ω→0} Δ = m_c E/k₁.

  A closed system has no static uniform-field state; it falls. Any static sag
  belongs to an anchor, so a subsystem displacement measured relative to a
  supported host is cancelled by the support's own response inside the closed
  system. The source multipole about the total COM changes only when the
  chain is anchored (D5).
* *No external-field effect from a uniform external field.* A galaxy together
  with its medium, falling in an external field that is uniform across it, has
  exactly the internal dynamics it would have without that field. Only the
  external source's tides (∝ g_ext·size/distance) enter. If the target's p
  depends on |g_int + g_ext|, the original action cannot reproduce that
  dependence at uniform order.

---

## 3. Locality: how a medium can sense |g|

**Proposition 2 (Newton–Cartan).** Under x' = x − ξ(t) the field shifts,
g' = g − ξ̈. The tidal tensor ∂ᵢ∂ⱼU and the relative acceleration
a_rel = ẍ − g = f/ρ are invariant (`affine_exact.py` E1–E3). So a local
function of |g| can enter a Galilean-covariant constitutive law in only one
way: through matter whose a_rel equals −g, that is, matter held static by
non-gravitational stress. In a static galaxy such matter senses the
**internal** field only, never a uniform external one; this is consistent
with Theorem 1.

*Consequence for discs.* Host-anchored mechanisms (scalar clouds riding on
stars or gas) see a_rel = 0 for stars and 0.5–8 % of g for disc gas (table
in §1). Where rotation curves are measured, they would be suppressed by that
factor, and they would track gas pressure support rather than g. If the
response is local in |g|, the responding medium must itself be supported.
Otherwise the response is non-local.

---

## 4. Finite-wavelength static response by class, and the order of limits

Check labels in this section refer to `finite_wavelength.py`.

The target is written in kernel form first. The target's quadratic medium
energy is K|P|²/2 with K = 4πG. For a longitudinal P, δρ_k = −ikP_k, so this
energy is K|δρ_k|²/(2k²). It cancels the Newtonian self-energy at **every** k
(`finite_wavelength.py` E1). The target therefore needs a static proper
kernel

  h_target(k) ≡ −1/χ_p(k,0) = 4πG/k²,  ε(k) = 1 − 4πG/(k²h) ≡ 0,

which is exact gravitational marginality at all wavelengths. (The record
calls this "critical normalization"; this is its k-space form.)

**4.1 Centred closed object (COM-projected l = 1).** Consider a cloud m_c and
a host m_h with the total COM removed and host recoil kept. The odd probe has

  D_k = [m_c sin(kμ_h z) − m_h sin(kμ_c z)]/k = −(k²/6) q₃ z³ + O(k⁴),
  q₃ = μ_red(m_h−m_c)/M.

The k⁰ term vanishes identically (A1–A2). For equal masses D_k ≡ 0 at every
k (A3, A6), as the record states. In the harmonic ground state
χ_D = (11/18) k⁴ q₃² s⁶/(ħω) + O(k⁶) (A4). The exact all-k matrix-element sum
gives ratio 0.99996 at ks = 0.01 (A5). The record's n = 1 shared-state result
χ₁ = [20/(3π²) − 40/63] R⁷/G = 0.040554 R⁷/G was independently reproduced,
including the COM condition (F1). The plane-probe l = 1 part is
χ_k = (k⁴/100)χ₁ + O(k⁶) per centred object. The record's finite-GP plus
γ = 5/3 state shows the same k⁴ approach numerically (STATIC_RESPONSE.md,
χ_k/k⁴ → χ_{r³}/100); that calculation was cited, not rerun.

**4.2 Medium of free composites.** For objects at random positions,
ρ_k = e^{ikR}[M + 0·k − (k²/2)μ_red z² + …]. The internal O(k) term is
exactly zero (the equivalence principle, A7). The leading internal response
is the tidal quadrupole, χ_int = −n k⁴T/(2ω⁴) (classical harmonic), so
α_int = n k²T/(2ω⁴) → 0 (A8). The composites' COMs form a gas, which belongs
to class 4.3.

**4.3 Supported compressible medium (original-action scalar).** With contact
plus quantum pressure, h(k) = 2K + τk²/(2ρ̄). Then

* h − 4πG/k² is strictly increasing in k² (B2), so ε has exactly one positive
  root (B1).
* The Thomas–Fermi root is k*² = 2πG/K = 8πG m⁴/λ_rep (ħ = c = 1; in SI
  K = λ_rep ħ³/(4m⁴c)). At the benchmark,
  1/k* = 3.683472×10⁷ m, matching the record's L0 = 3.68347×10⁷ m (B6).
* At k = 1/kpc, ε ≈ −7×10²³. The homogeneous benchmark medium is deeply
  Jeans-unstable at galactic scales. Its static states there are finite
  objects (T = 0 contact-supported n = 1 polytropes of mass-independent
  radius π/k* ≈ 1.16×10⁸ m), which puts it back in classes 4.1–4.2.
* Below k_J the gravity-dressed static response tends to +k²/(4πG) (B3).
  This is perfect screening on the unstable branch (δρ → −ρ_ext): the
  magnitude 1/(4πG) appears, but on the wrong side of marginality.

These results are consistent with the record's static-kernel monotonicity
theorem (CE-FM-087 §4). A collisionless medium supported by velocity
dispersion has constant h = σ²/ρ̄ and behaves the same way.

**4.4 Supported insulating dielectric.** A cloud sits in a uniform-density
host core of density ρ_h, and the host is held static (a_rel = −g).

* The polarizability is 4πGα = 3ρ_c/ρ_h, with ρ_c = n m_c (D1).
* A hard wall at the core radius gives saturation at g* = G M_core/R_c², the
  core surface gravity, with p_sat/g* = α (D2).
* The target would therefore need the state selections ρ_c = ρ_h/3 and
  a0 = G M_core/R_c².
* A finite site compressibility C_site > 0 makes 4πG(−χ)/k² diverge as k → 0
  (D3). Only an incompressible static support passes, and no such support is
  present.
* In the deep regime with a flat curve, the carrier displacement obeys
  |u|/r = ρ_dyn/ρ_carrier (D4). Locality would need a carrier density far
  above the total dynamical density. But the carriers' own mass is part of
  that density (on average ρ_carrier ≲ ρ_dyn by §5), so |u| ≳ r.

**4.5 Order of limits.**

| limit | result | meaning |
|---|---|---|
| k → 0 first (uniform), any ω, then ω → 0 | COM free fall, χ/k² = ρ̄/ω²; internal part ≡ 0 (Thm 1) | nothing selected at k = 0 |
| ω → 0 first, finite closed state, then k → 0 | χ_D = O(k⁴) (centred), α_med = O(k²) | → 0 |
| ω → 0 first, homogeneous supported medium, then k → 0 | proper χ/k² → −∞; crosses ε = 0 once at k_J; no stable static state below k_J | marginal at one k only |
| dressed homogeneous medium, k → 0 then ω → 0 | χ/k² → ρ̄/(ω²+4πGρ̄) → 1/(4πG) (B5) | swindle/collapse branch, not a static state |
| critical, soft mode of gap Ω and weight ∝ k^{2a} | α ∝ k^{2a−2}/Ω; internal modes have a ≥ 2. lim_k lim_Ω = ∞, lim_Ω lim_k = 0 (C2) | constant α needs Ω ∝ k^{2a−2}, i.e. a gap that closes at the probe scale; a = 1 with a finite gap is a pinned COM (anchor) (C1) |

---

## 5. Positive-energy transport budget (exact; closes the χ ∝ k² loophole)

Check labels in this section refer to `transport_budget.py`.

The record left one route open (STATIC_KERNEL.md §4): a gapped
conserved-density or insulating phase with χ(0,k) ∝ k². The following lemma
covers every such phase whose carriers have positive gravitating energy.

**Lemma.** Let ρ_ref, ρ_fin ≥ 0 have equal total energy, and set
ℓ = W_∞(ρ_ref, ρ_fin), the ∞-Wasserstein distance: the largest displacement
needed to turn one distribution into the other, minimised over all transport
plans. Then for every ball B_r(c),

  M_ref(B_{r−ℓ}) ≤ M_fin(B_r) ≤ M_ref(B_{r+ℓ}),
  ∫₀^R M_pol(<r) dr ≤ ℓ M_ref(B_{R+ℓ}).

Proof: a plan with displacement at most ℓ carries all the mass of B_{r−ℓ}
into B_r, and everything that ends in B_r started in B_{r+ℓ}. For the
integral, M_pol(<r) ≤ M_ref(shell r..r+ℓ), and each reference element lies
in that shell for a set of r of length at most ℓ.

A Monte Carlo check found no violation (3 centres × random/inward/outward
transports × 240 radii, A1–A2), and the bound is sharp (A3).

No dynamics is assumed. Conversion X ↔ ΦΦ cannot evade the lemma, because
the source gravitates with its full energy; the positive-square potential
makes T⁰⁰ ≥ 0 pointwise, up to O(v²/c²) gravitational binding.

**Corollary.** For a non-increasing reference density,
M_ref(B_r) ≥ M_pol(<r)/[(1+ℓ/r)³ − 1] = M_pol(<r)·[r/(3ℓ) − 1/3 + …] (B1).
So a local response (ℓ ≪ r) can change M_med(<r) by at most the mass of a
shell of width ℓ. The law counts the whole final medium mass inside r,
M_law = M_ref(B_r) + M_pol(<r). The fraction of it that a response can
*generate* is therefore bounded:

  f_gen = M_pol/M_law ≤ 1 − (1+ℓ/r)^{−3} ≈ 3ℓ/r   (B2).

At most 2.9 %, 25 % or 55 % can be generated for ℓ/r = 0.01, 0.1 or 0.3.
Generating 50 %, 90 % or 99 % needs ℓ/r ≥ 0.26, 1.15 or 3.64. Everything
else must already be present in the reference state, with the law's profile,
before the response acts.

Suppose instead that the whole law mass is generated from a cosmologically
subtracted uniform reservoir ρ̄, which the law does not count. Then
ℓ_min = (r³ + 3M_law/(4πρ̄))^{1/3} − r. Illustration (declared
inputs: point mass 10¹⁰ M☉, ρ̄ = Ω_m ρ_crit with H0 = 67.4, Ω_m = 0.315):

| a0 (m s⁻²) | r = 10 kpc | r = 30 kpc | r = 100 kpc |
|---|---|---|---|
| 9.36×10⁻¹¹ | ℓ_min = 495 kpc (49 r) | 730 kpc (24 r) | 1052 kpc (11 r) |
| 1.13×10⁻¹⁰ | 514 kpc (51 r) | 755 kpc (25 r) | 1089 kpc (11 r) |

At those radii ρ_dyn/ρ̄ ranges from 5×10² to 6×10⁴ (both footings). A local
linear response built from cosmic-mean carriers would need |u|/r of 5×10² to
5×10⁴, which is self-contradictory. So the law's medium mass cannot come from
a local response of any positive-energy medium: either it was already in place
from formation, or it was assembled non-locally over ℓ ≳ r. A local
dielectric with positive-mass carriers can only add a small correction
(≈ 3ℓ/r) on top of a pre-arranged profile; it cannot be the origin of the
law. This is why
gravitational-polarization models of MOND introduce opposite-sign
gravitational charges or a separate internal field; the original action has
neither.

---

## 6. Decision and the first missing selection equation

**Does any source-carrying response survive at uniform acceleration?** No.
It vanishes exactly, to all orders and for all states, once the host,
support, receiver and recoil are kept and only the total COM is removed
(Theorem 1). This is an action-level statement. No choice of occupation,
spectrum, temperature or inventory changes it.

**SE-1, the first missing selection equation.** Work on the galactic band
1/r ≲ k ≪ 1/(microscopic scale), in regions where g ≪ a0. There the medium's
static proper kernel must satisfy

  h_med(k) = (4πG/k²)·[1 + O(g/a0)]  uniformly in k,

that is, ε(k) = O(g/a0) at every wavelength. In Gauss form this is
g_med/g → 1, with g_med = 4πGΣ_med. Its nonlinear completion is

  4πG Σ_med(<r) = a0 g(r)/(a0 + g(r))  for every baryon profile.

The "universal normalization" p_sat/a0 = 1/(4πG) is then the statement that
the saturated medium's own field is a0: Σ_sat = a0/(4πG) = 53.4 or
64.5 M☉ pc⁻² for the two footings (`transport_budget.py` D1). It is not an
independent condition once SE-1 and a0 are given.

SE-1 comes first because it is the lowest-order (linear, field-free)
coefficient of the target response, needed before a0, the rational shape or
any occupied spectrum. The k = 0 response, which would otherwise come first,
is identically zero.

**Status in the original action.** Every static class constructed fails SE-1
on a band:

* free composites: 4πG/(k²h) = O(k²), from the equivalence principle (4.1–4.2);
* supported compressible media: one Jeans root at most (4.3, and the record's
  theorem);
* supported insulating media, the only class with k-independent α: they need
  C_site = 0 and 3ρ_c/ρ_h = 1. Even then the budget lets a local response
  generate only about 3ℓ/r of the law mass, so the profile must be
  pre-arranged by formation or assembled over ℓ ≳ r (4.4, §5).

The open branch is a non-static, non-local supply. There SE-1 becomes a
supply equation for Σ_med(r), which must be derived from formation dynamics
under three constraints:

* no uniform-field external-field effect (Theorem 1);
* any local |g| keying happens only where the deposited medium is supported
  (Proposition 2);
* a catchment of at least ℓ_min (§5), with the reservoir correspondingly
  depleted.

That derivation is the next executable step for this line. It belongs to
brief items 2–4, and it has not been done here.

---

## 7. Proved versus conditional

| statement | status |
|---|---|
| Theorem 1 (affine, all orders, all states, supports/receivers) | proved in the Galilean/Bargmann EFT; at O(1/c²) relies on the record's energy-centre theorem; strong-field GR not addressed |
| EP-violation/anchor characterization, non-commuting limits, heavy-host ≠ anchor | proved (symbolic) |
| No uniform-field EFE | proved at uniform order; tides of the external source not computed |
| Newton–Cartan locality (only tides and a_rel are local) | proved |
| Disc a_rel fractions | illustrative inputs (c_s, v_c, dlnP/dlnr) |
| 4.1 composite formulas; record χ₁ reproduction | proved for the stated harmonic and n = 1 models |
| 4.2 α_int = O(k²) | proved (EP) at leading order; coefficient model-specific |
| 4.3 single Jeans root, benchmark 1/k*, perfect-screening limit | proved for the TF+quantum-pressure kernel; general compressible class rests on the record's theorem and its hypotheses |
| 4.4 supported-dielectric normalization | conditional on a uniform core, hard wall and rigid support |
| Transport lemma and corollary | proved (positivity, conservation, W∞ ≤ ℓ; corollary needs a monotone reference) |
| ℓ_min and ρ_dyn/ρ̄ numbers | illustrative (point mass, declared cosmology, both footings) |
| SE-1 unsatisfied by every static class constructed | proved for those classes; **not** an all-phase no-go: unconstructed non-local/critical phases and the non-static supply branch remain open |

---

## 8. Evidence and reproduction

Run each script into a new directory (1 core, a few seconds, < 110 MB RSS):

```bash
nice -n 19 python3 sol61_push/claude_continuation_2026_10_19/acceleration_response/affine_exact.py      <outdir>
nice -n 19 python3 sol61_push/claude_continuation_2026_10_19/acceleration_response/finite_wavelength.py <outdir>
nice -n 19 python3 sol61_push/claude_continuation_2026_10_19/acceleration_response/transport_budget.py  <outdir>
```

The recorded outputs are the JSON files in `run_001/` (Python 3.13.9,
sympy 1.13.1, numpy 1.26.4, mpmath; seed 20261019): 19 + 22 + 7 = 48 checks,
all passing. Stdout logs are git-ignored; the JSON files carry every check and
number.
Two of them are records rather than tests: `affine_exact` C3 (a trivial
translation identity) and `transport_budget` D1 (arithmetic). The zero
results come with positive controls in the same scripts: EP-violating charges
(A3) and an external anchor (D3, D5) do produce a nonzero response, so the
zeros are not artefacts of the method.

Two corrections were made during the work. First, `transport_budget` B1
initially stated the expansion's constant term as −1 instead of −1/3; the
check failed and the statement was corrected. Second, the corollary was
first framed as "the reference monopole is extra mass the law cannot hold",
with thresholds (1+1/δ)^{1/3} − 1. That framing was wrong, because the law
counts the whole final medium mass. It was replaced by the generated-fraction
bound f_gen ≤ 1 − (1+ℓ/r)^{−3} (B2), which supports the same conclusion
with different numbers. File hashes are in `CHECKPOINT.json`.
