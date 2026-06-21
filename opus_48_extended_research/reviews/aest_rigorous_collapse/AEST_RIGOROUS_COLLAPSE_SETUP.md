# Rigorous AeST collapse — derivation + solver design (the three dropped caveats)

*Setup for workflow following `wxbnjxb64`. Goal: re-test phase-pinning of the AeST oscillation mode
after adding the THREE things the scalar-only 1+1D spherical collapse dropped: (1) self-consistency
(r''=-g_AeST), (2) the vector sector (K_B / E field), (3) violent relaxation / phase-mixing (multi-stream,
non-radial). Both-ways. Quarantine: a0/Z/kappa/I0 never derived.*

---

## 0. The prior, stated plainly (do not let it bias the calc)
The scalar-only spherical collapse (`wxbnjxb64`) found NO pin: the late-time AeST oscillation phase tracks
the IC phase ~1:1 (slope +1.00 to +1.20 three ways), because the shift-symmetric AeST scalar has a
FRICTIONLESS conservative free Helmholtz/KG mode at omega = mu*c that is exactly conserved (708 osc/Hubble,
Hubble damping per period 0.9979 ~ undamped). Collapse fixes only the DC part. The obstruction is
STRUCTURAL (conservative wave), not a numerical artifact. AeST is action-derived => strictly conservative
=> no true dissipation anywhere (confirmed below).

The genuine open question: do (1)+(2)+(3) — none of which is a true friction term, but each of which is
different physics the smooth scalar-only model missed — supply an EFFECTIVE phase-selection (mode-mixing
that fixes the macroscopic phase) and PIN a unique, universal, galaxy-safe boost? If ANY does, the cluster
door reopens predictively (strong result, follow-up paper). If none does, the no-go is airtight.

---

## 1. vector_sector_eqs — the AeST aether VECTOR mode, full action + weak-field role

### 1.1 The full AeST action (Skordis-Zlosnik 2021, arXiv:2007.00082; Hamiltonian form Blanchet-Skordis 2024 arXiv:2307.15126 Eq.1)
```
S = (1/16piG) ∫ d^4x sqrt(-g) [ R - 2Λ
                                 - (K_B/2) F^{μν} F_{μν}            <-- VECTOR kinetic (Maxwell-type)
                                 + (2 - K_B)(2 J^μ ∇_μ φ - Y)       <-- scalar-vector cross + scalar
                                 - F(Y, Q)                          <-- free function (gives MOND + mass μ)
                                 - λ (A^μ A_μ + 1) ]                <-- unit-timelike constraint
        + S_m[g]   (matter couples to the metric ONLY)
```
Building blocks (arXiv:2406.18225 Eqs.1-4; 2307.15126 Eqs.3-4):
- F_{μν} = 2 ∇_[μ A_ν]                  (vector field strength, ANTISYMMETRIC => Maxwell-like)
- J_μ   = A^ν ∇_ν A_μ                    (aether "acceleration", along the flow)
- Q     = A^μ ∇_μ φ                       (scalar gradient projected ALONG the aether — temporal part)
- Y     = q^{μν} ∇_μφ ∇_νφ,  q^{μν}=g^{μν}+A^μ A^ν   (scalar gradient projected ORTHOGONAL — spatial part)
- constraint A^μ A_μ = -1                 (unit timelike; λ is the Lagrange multiplier)

### 1.2 Mode content (linear stability, Skordis-Zlosnik 2022 arXiv:2109.13287; Hamiltonian 2307.15126)
6 physical dof, all action-derived (no friction):
- 2 tensor (massless graviton, c_T = c — passes GW170817)
- **2 VECTOR modes — MASSIVE** (mass scale set by K_B and the action params)
- 2 scalar (1 massive with mass gap μ ≲ 1 Mpc^{-1}; 1 with Jeans-like low-k behavior, the "healthy ghost")
The vector kinetic term is PURELY Maxwell F^2 = -(K_B/2) F_{μν}F^{μν}. F is antisymmetric in (μν), so it has
**no single-time-derivative (friction) structure** — F_{0i} = ∂_0 A_i - ∂_i A_0 enters QUADRATICALLY as
|E|^2 (Eq.25 of 2307.15126: K_B(|E|^2 - |B|^2), E_i = (1/N)F_{0i} the "electric" aether field). This is the
"E field / K_B sector" flagged as the place a friction could hide.

### 1.3 The decisive weak-field fact (where the vector CAN and CANNOT enter)
From the AeST weak-lensing paper (arXiv:2301.03499, App.B) and the quasistatic-spherical paper
(Durakovic-Skordis 2024, MNRAS 531 272 / arXiv:2304.05134, sec.4):

> "In spherical symmetry, the curl term ∇×A vanishes and the A equation of motion and the φ equation of
>  motion are equivalent. Thus setting A to zero is justified."   **BUT** "outside spherical symmetry this
>  is inconsistent. The general A equation couples A to gradients of Φ and φ with derivatives controlled by K_B."

So the vector sector is **identically trivial in spherical symmetry** (the scalar-only solve lost NOTHING by
dropping it — that branch of the prior's caveat is closed by AeST's own structure). The vector can ONLY do
new work when the configuration is **NON-spherical** (the curl ∇×A ≠ 0). This ties caveat (2) directly to
caveat (3): the vector is a live channel ONLY in the multi-stream / non-radial / tidal collapse, never in
the onion-spherical one. THE SOLVER MUST BREAK SPHERICAL SYMMETRY to test the vector at all.

### 1.4 The weak-field vector equation to solve (non-spherical)
Linearize on Minkowski, quasistatic. With A_μ = (-1 + δA_0, A_i), constraint fixes δA_0 = (1/2)|A_i|^2 + δg.
The spatial vector A_i obeys (schematically, from varying the F^2 + (2-K_B)(2 J·∇φ) terms):
```
K_B [ ∇^2 A_i - ∂_i(∂_j A_j) ]  +  (2-K_B) ∂_i(∂_t φ · something)  =  (source from ∇φ × geometry)
```
The curl part (∇×A) is sourced ONLY by the TRANSVERSE / non-radial part of ∇φ and the tidal (off-diagonal)
metric shear. Key for the pin question: this equation is **elliptic in space, no ∂_t^2 friction on A** in the
quasistatic limit (the vector mass + Maxwell structure give |E|^2, conservative). The vector can REDISTRIBUTE
the scalar's oscillation energy across modes (mixing), but supplies no dissipative sink. **That is the crux:
mixing vs damping.**

---

## 2. self_consistent_eom — r'' = -g_AeST, the rigorous (non-proxy) collapse

The prior solve's MAIN weakness: matter radius was a prescribed cosine `r_phys(t)` (kinematic proxy);
r''=-g was never integrated. The rigorous version uses an N-SHELL (Lagrangian) integrator.

### 2.1 The N-shell self-consistent EOM (Lagrangian mass coordinate m)
Each shell i (enclosed baryon mass M_i fixed by Lagrangian labelling) obeys
```
d^2 r_i/dt^2  =  - g_AeST(r_i, t)
g_AeST(r, t)  =  g_N(r,t) + g_φ(r,t)
g_N(r,t)      =  G M_b(<r, t) / r^2                         (Newtonian, mass interior updated each step)
g_φ(r,t)      =  ∂_r φ(r, t)                                 (the AeST scalar force, from §2.2)
```
M_b(<r,t) = Σ_{j: r_j < r} M_j is RECOMPUTED from the live shell positions every timestep (this is the
self-consistency the proxy lacked — handles shell crossing: when shell j overtakes shell i, M_b(<r_i) jumps).
Shell crossing (the seed of multi-stream) is captured natively because shells are allowed to pass through
each other; M_b(<r) is evaluated on the instantaneous ordering.

### 2.2 The AeST scalar force solved AT each step (the real field, not a proxy)
At each timestep solve the AeST quasistatic scalar equation on the live density ρ_b(r,t)=ΔM/4πr^2Δr:
**Static (μ-domination) form** — Durakovic-Skordis Eq.2 / Eq.2.40:
```
(1/r^2) d/dr [ r^2 μ̃(|φ'|/a0) φ' ]  +  μ^2 Φ  =  4πG_N ρ_b ,    μ̃(x)=(√(1+4x)−1)/(√(1+4x)+1)
```
**Dynamical (KG wave) form** — to expose the oscillation phase honestly:
```
(1/c^2) ∂_t^2 χ  −  ∇·[ (dJ/dY) ∇χ ]  +  (μ c)^2 χ  =  4πG_N ρ_b(r,t)
```
with μ^{-1} = 1 Mpc (CMB-pinned), a0 = 9.36e-11 (INPUT, quarantined). The KG form is the one whose phase
we test; the static form is the validation gate (μ=0 must reproduce analytic MOND to ppm, as before).

### 2.3 Why self-consistency MIGHT pin (the honest pro-pin case)
With r''=-g_AeST, the matter density history ρ_b(r,t) is no longer an externally prescribed smooth cosine —
it has its OWN bounce/ringing at the collapse frequency ω_dyn ~ √(Gρ). If ω_dyn happens to lock to ω=μc
(resonance), the forced response could select a preferred phase. **Test:** sweep IC phase AND check whether
the self-consistent ρ_b(r,t) forcing spectrum overlaps ω=μc. Prior intuition: ω_dyn(cluster) ~ 1/(few Gyr)
vs μc/2π ~ 708/Hubble => μc ~ 4448 H0 >> ω_dyn, so the forcing is far off-resonance and the free mode rings
on its own — but the SELF-CONSISTENT bounce spectrum is broadband (not a single cosine), so this must be
re-checked numerically, not assumed.

---

## 3. phasemix_reduction — violent relaxation / Lynden-Bell, reduced past spherical

### 3.1 The physics (Lynden-Bell 1967; Kandrup 1998 arXiv:astro-ph/9708026)
Violent relaxation = collisionless rapid relaxation via the TIME-DEPENDENT collective potential, completing
in **~2-3 dynamical times** (Sylos Labini 2012, MNRAS 423 1610). It is **nonlinear Landau damping** = PHASE
MIXING (destructive interference of a CONTINUUM of frequencies), NOT true energy dissipation. THE LOAD-BEARING
THEOREM (Kandrup 1998, confirmed): phase mixing damps a coherent oscillation **only if there is a CONTINUUM /
SPREAD of frequencies** to interfere. **A single sharp discrete normal mode at one frequency, with no
neighboring continuum, does NOT phase-mix — it persists undamped.**

### 3.2 The reduction (how to break spherical symmetry tractably)
Three escalating reductions, each adds a frequency spread the spherical-onion lacked:
- **(A) Multi-stream onion (radial only):** N shells allowed to cross (§2.1). After shell crossing each
  Lagrangian shell oscillates at its OWN radial frequency ω_i ~ √(G M(<r_i)/r_i^3). This gives a SPREAD of
  MATTER frequencies {ω_i} — the question is whether that spread couples into the AeST field's ω=μc mode.
- **(B) Axisymmetric / non-radial (2D r,θ or low-ℓ multipoles):** seed ℓ=2 (and ℓ=4) density perturbations;
  evolve r''=-∇Φ_AeST with the non-radial force. Now ∇×A ≠ 0 => the VECTOR sector (§1.3) turns on. The
  scalar φ acquires transverse gradients => Y vs Q mixing => the free function couples the modes.
- **(C) Triaxial / tidal:** external tidal field (cluster forms in a filament) => the collapse axes have
  DIFFERENT ω => maximal frequency spread + maximal ∇×A. This is the closest tractable proxy to full 3D
  violent relaxation.

### 3.3 The reduced field-mixing model (the actual computable test)
Represent the AeST scalar oscillation as a set of modes χ_n(t) e^{i k_n·x} with the matter providing a
TIME-DEPENDENT source S(x,t) from the violently-relaxing ρ_b(x,t). The mode equation:
```
χ_n'' + (ω_n^2) χ_n  =  S_n(t) + Σ_m C_{nm}(t) χ_m ,   ω_n^2 = c^2 k_n^2 + (μc)^2
```
- Diagonal term ω_n: each mode is a sharp oscillator (mass gap μc + k_n).
- C_{nm}(t): mode-MIXING from the non-radial/vector coupling (∇×A, Y-Q cross terms) — TIME-DEPENDENT because
  the collapse potential is. **This is the only candidate phase-selection mechanism.** If C_{nm}(t) from
  violent relaxation transfers the coherent χ-energy into a continuum of k-modes that destructively
  interfere, the macroscopic (spatially-averaged, observable) phase could settle to a universal value even
  though no single mode is damped. **That would be the pin.**

### 3.4 The decisive test (both-ways, robust)
For each reduction (A,B,C): sweep IC phase θ_IC over [0,2π) AND mass (1e14-1e15) AND profile AND seed
amplitude. Measure d(θ_obs)/d(θ_IC) of the OBSERVABLE boost η(R500) at a=1.
- **PIN** iff: slope → 0 (universal), η lands GALAXY-SAFE (RAR shift < 0.05 dex) and CASSINI-SAFE, AND the
  result is ROBUST to halving every numerical damping/viscosity/grid parameter (NOT a damping artifact).
- **NO-GO holds** iff: slope stays O(1) (IC-tracking) as in the spherical case.
GUARDRAIL (Carl's rule): if a pin appears ONLY when an artificial viscosity ν_num is on, halve ν_num — a
real pin survives, an artifact scales with ν_num. A pin from a reflecting boundary is killed by an outgoing
Sommerfeld BC (as in the prior clean-room check). Report the spread both ways; do not manufacture, do not
high-priest.

---

## 4. where_a_pin_could_come_from (ranked — the skeptic's map)
1. **VECTOR mode-mixing in non-radial collapse (caveat 2 ∩ 3, the top candidate).** ∇×A ≠ 0 only off-spherical;
   it couples scalar modes via C_{nm}(t). IF the violently-relaxing potential drives a broadband C_{nm}(t)
   that phase-mixes the χ continuum into a universal mean phase — pin. AGAINST: the coupling is conservative
   (Maxwell |E|^2, no friction), so it REDISTRIBUTES but cannot DISSIPATE; and the observable boost is set by
   the mass-term DC + the μc mode, which is a sharp discrete frequency (Kandrup: no continuum => no
   phase-mix). Likely mixing-not-damping.
2. **Resonant lock of the self-consistent bounce (caveat 1).** If ω_dyn(t) sweeps through μc during collapse
   (parametric resonance), the phase could lock. AGAINST: μc ~ 4448 H0 >> ω_dyn ~ few/Gyr; far off-resonance;
   the self-consistent bounce is broadband but weak at μc.
3. **True violent-relaxation continuum (caveat 3, multi-stream).** The {ω_i} spread of crossing shells is a
   genuine continuum — IF the AeST field's observable couples to the MATTER frequency continuum (not just its
   own sharp μc mode), it phase-mixes. AGAINST: the field's free mode is at the fixed μc, decoupled from the
   matter ω_i spread except through the (weak, off-resonant) source.
4. **A numerical-damping FALSE pin (the artifact to rule out).** Any grid viscosity, reflecting wall, or
   coarse Δt that bleeds the χ oscillation will FAKE a pin. Must be excluded by the ν_num-halving + Sommerfeld
   guardrails before crediting ANY pin.

**Net prior expectation (stated, not assumed):** the no-go likely holds HARDER — the vector is trivial in
spherical symmetry and conservative off it (mixing not damping), the observable rides a sharp discrete μc
mode that Kandrup's theorem says cannot phase-mix, and AeST is strictly action-conservative. BUT (1) and (3)
in the genuinely non-radial/tidal case are real, untested couplings — a true swing. If the broadband
violently-relaxing C_{nm}(t) DOES settle the observable phase universally and galaxy-safely and robustly,
credit it at full weight and reopen the door.

---

## 5. key_facts (see StructuredOutput)

## 6. Solver files (built under aest_rigorous_collapse/)
- `aest_rig_core.py` — constants, AeST static scalar (DS24 Eq 2.40, canonical-momentum form),
   scipy-free RK4 field solver (safe to nest inside the collapse), phase diagnostics
   (`fit_oscillation_phase`, `pin_metric` = slope + circ_std + |IC-response|). GATES: (1) μ=0
   deep-MOND r_vir/r_max=exp(-1/2) to 1e-9; (2) static μ=0 → analytic MOND to 0 ppm; (3) vector
   trivial-in-spherical (curl A_r e_r ≡ 0); (4) RK4 vs DOP853 field solver to 652 ppm.
- `aest_rig_selfconsistent.py` — CAVEAT 1 + 3A: N-shell velocity-Verlet r''=-g_AeST with the
   cosmological background + virialization closure, live M_b(<r) each step, native shell crossing
   (multi-stream); time-dependent KG χ wave driven by the self-consistent density history; the
   IC-seeded FREE mode isolated by (seeded−forced) differencing + temporal demod vs μc.
- `aest_rig_nonradial_vector.py` — CAVEATS 2 + 3B/C: the off-spherical VECTOR sector as a
   conservative (antisymmetric, energy-preserving) time-dependent mode-mixing matrix C_{nm}(t)
   from the violently-relaxing potential; both-ways CONTROLS = a dissipative sink + an indefinite
   coupling (so a real pin is distinguishable from a sink). E_drift diagnostic separates
   mixing (≈0) from dissipation (<0).
- `aest_rig_ADVERSARIAL.py` — analytic free-mode demod (slope vs γ → pin threshold), ν_num
   halving + Sommerfeld/reflecting BC flip (artifact ruling), galaxy-safety (worst-case RAR dex).
- `aest_rig_run.py` — MASTER runner: the 3 caveats + adversarial → consolidated verdict numbers.

## 7. Sources (see StructuredOutput)
