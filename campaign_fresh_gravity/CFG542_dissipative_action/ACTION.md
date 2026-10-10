# CFG542 ACTION: the dissipative principle for candidate B, written out

Status: **CONSISTENT WITH OPEN ITEMS** (section 6). Every claim here is a sympy result or a 1-D number written by `cfg542.py`
into `cfg542_results.json`. The criteria are in `FROZEN_CRITERIA.md` (3d435f032).

κ = ½ is fitted. The cold energy's mass is still required; its amount (Ω_c/Ω_b = 5.364) is an input. No dark-matter particle
species. This is not a closed theory.

---

## 1. The single statement (metriplectic / GENERIC form, Newtonian limit)

State z = (f_b, f_c, φ, π_φ): baryon and cold-energy phase-space densities, and a dark-energy scalar φ with momentum π_φ.

    dz/dt = L(z) · δE/δz  +  M(z) · δS/δz

- **Energy** E = E_N + E_φ, with E_N = Σ ∫ ½ f v² + W[ρ_b + ρ_c] (Newtonian, ∇²Φ = 4πG(ρ_b + ρ_c)) and
  E_φ = ∫ [½ π_φ² + ½ c²|∇φ|² + V(φ)].
- **Reversible part** L: Vlasov–Poisson for both species, plus the canonical bracket of φ. Only real mass gravitates (G9).
- **Dissipative functional** S = −F/Θ, with F = (1/8πG) ∫ |∇ψ|², ∇²ψ = 4πG d, d = 1_C max(ρ_ph − ρ_c, 0), ρ_ph the round
  per-region phantom (CFG541 E7) of each region's own baryons. Θ appears only in the product M/Θ; it is not a constant of the theory.
- **Dissipative operator** M, built pair by pair (in the continuum, element by element): for a transfer of cold-energy
  mass between two neighbouring points i → j, M = m (e_j − e_i, −ΔΦ)ᵀ ⊗ (e_j − e_i, −ΔΦ), acting on (ρ_c, ε_φ), with
  m/Θ = ρ_c α τ_ff 1_B 1_C, τ_ff = (4πGρ_m)^(−1/2).

sympy (3-cell model, any F, any symmetric gravity kernel, any baryon potential) verifies:
- M is symmetric and positive semi-definite; **M · δE = 0** (energy degeneracy), because δE/δρ_c = Φ and δE/δε_φ = 1;
- **dE/dt = 0 exactly**; **dS/dt = Σ m (Δψ/Θ)² ≥ 0**, so dF/dt ≤ 0;
- the mass flux is **J = −(m/Θ) Δψ**: the class-A drift, discretised;
- the partner gains **Q = (m/Θ) Δψ ΔΦ** per pair.

## 2. What follows from it

**(1) The settling flow.** ∂_t ρ_c + ∇·(ρ_c u_c) = ∇·(ρ_c α τ_ff 1_B 1_C ∇ψ): CFG541's class A, exactly (K1). Stationary states are
ρ_c ∇ψ = 0 on B∩C. They are α-free, and the inside-out fill to the exhaustion radius is the minimiser (CFG541 V4).

**(2) The energy sink.** The partner's energy rises at the local rate

    Q = ρ_c α τ_ff 1_B 1_C ∇ψ · ∇Φ        (≥ 0 in spherical symmetry, since ψ′, Φ′ ≥ 0)

This is the work gravity does on the slide. The φ equation that carries it (sympy energy identity):

    φ̈ + 3Hφ̇ − c²∇²φ + V′(φ) = Q/φ̇,    cosmically  ρ̇_DE + 3H(1 + w)ρ_DE = Q/c²

- The partner must be a **zero-entropy (coherent) field**, ∂S/∂ε_φ = 0. A thermal partner at a finite T_φ adds a drift
  −(m/T_φ)∇Φ, which moves the stationary state off ψ = const (sympy; MUTATE M3).
- An exact Λ cannot take the energy: φ̇ = 0 makes Q/φ̇ singular. That is the same condition CFG541 found.
- Rest mass is never converted (G9). Only binding energy leaves the matter sector.

**(3) "Bound".** The GENERIC conditions hold for **any** support function s(x) ≥ 0 multiplying m. The principle does not
select the region. **The switch is an INPUT.** What the principle does decide is where the switch may sit:
- If the gate sits **inside F** and reads the cold energy (CFG541 E8: the tidal tensor of the total density), the drive picks up a
  term ½ s′(u) d², a leak. The flow could then lower F by dissolving bound regions. This is the MS1 matter-door leak in
  dissipative form, so **CONFLICT with MS1**.
- If the gate reads baryons only, or sits **only in the mobility**, there is no leak for any reading.
- The region segmentation of the round phantom must therefore read baryons. This agrees with MS1 (owner, 09-26).
- A local covariant candidate, the expansion of the baryon congruence θ_b ≤ 0, is zero at turnaround for a top-hat. But it already
  fires in a one-axis (Zel'dovich sheet) collapse at λ₁a = 3/4, where E8 does not. It is a different switch, reported and not
  adopted.

## 3. The inertial completion Pb* (CFG541 open item 3): INCONSISTENT

Tried and failed. It is recorded here so that it is not re-proposed without a repair.


Give the slide a velocity w with flux relaxation at the same mobility time (no new constant):

    ∂_t w + (w·∇)w = −∇ψ − w/(α τ_ff),     ∂_t ρ_c + ∇·[ρ_c(u_c + w)] = 0

- **Extended Lyapunov** (sympy local identity): d/dt [F + ∫ ½ ρ_c w²] = −∫ ρ_c w²/(α τ_ff) ≤ 0. Here F + K_w plays the role of
  the extended entropy (extended irreversible thermodynamics). It is not an energy, so E is still E_N + E_φ, with
  Q = −ρ_c w·∇Φ.
- The overdamped limit (α τ_ff ≪ the ψ crossing time) returns class A. The stationary set is the same.
- **Speed bound** (sympy, along an element, ψ static, starting at rest): |w| ≤ √(2 max|ψ|).
- Linear stability with the damped ψ wave: q α (α + β) < 1. That gives α < 0.618 at β = 1, q → 1. With instantaneous ψ it is
  stable for every α.
- **Why it fails.**
  - The identity needs dF/dρ_c = ψ. At overfilled points (d = 0) the derivative for adding mass is 0.
  - Material accelerated by −∇ψ therefore coasts into the filled core, F + K_w rises, and the one-sided deficit never removes the
    overfill.
  - In the 1-D runs the edge collapses to 0.61–0.67 r_* (α = 0.5) and to ≤ 0.11 r_* (α ≥ 1); see the README.

## 4. Angular momentum

- A radial slide w r̂ in the region's baryon-centre frame, plus the velocity-space term **a_s = −(w/r) v_⊥** (minimal: no change
  of radial velocity), conserves **each element's j = x × v** (sympy).
- The slide is radial only if ψ is round, i.e. if the deficit uses the shell-averaged ρ_c. That keeps the gradient-flow
  symmetry (sympy).
- The energy rate per element is then w(Φ′ − v_⊥²/r). The settling releases energy only from the pressure-supported part:
  Q = 0 for circular orbits, and spin-up heats the tangential motion.
- A non-radial slide cannot conserve j element by element: the solvability condition (v × v_s)·x = 0 fails.

## 5. Constants

G, c, ρ_DE (through a₀), κ (fitted), 5.364 (input), the DE background w(z). α is **O(1) FREE**:
- energy balance is homogeneous of degree 1 in α;
- KMS/FDR fix the noise given the mobility, not the mobility (Onsager–Machlup relation and the Fokker–Planck equilibrium are both
  M-independent, sympy);
- a microscopic bath gives α ∝ g² (a new coupling).

Stability only **bounds** α: Pb gives αβq < 1, Pb* gives qα(α + β) < 1.

## 6. Open items

1. α FREE (bounded above by causality).
2. The GENERIC degeneracy L·δS = 0 fails. Orbital (Vlasov) transport changes F (dF/dt|orb = ∫ρ_c u·∇ψ, positive for outward
   motion). So F is not a true entropy of the full kinetic system; it decreases only under the drift sub-flow.
3. Kinetic consistency (CFG541 item 5) is not supplied: the slide leaves the cold energy sub-virial, and Q takes the whole ΔW.
4. The switch and the catchment are inputs. The principle fixes only their admissible placement (mobility, or a baryon reading).
5. A canonical partner is singular where w = −1. See K10 in the README for the DESI crossing fraction.
6. The diffuse-reservoir drift speeds (CFG541 item 3) are unresolved. Pb* is INCONSISTENT; a two-sided deficit, or a slip
   confined to d > 0, is the untested repair.
7. C1: overdamped cluster drift speeds reach 0.19 c at α = 2.
