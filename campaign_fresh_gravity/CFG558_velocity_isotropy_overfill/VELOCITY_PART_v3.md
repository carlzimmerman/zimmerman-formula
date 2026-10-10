# CFG558 VELOCITY PART v3: isotropy, overfill, α

Criteria: `FROZEN_CRITERIA.md` (f6b7ced5d). Every claim below is either a sympy result in `cfg558_results.json` (key `sympy`)
or a bench number there. The README gives the verdicts. κ = ½ is fitted. The cold energy's mass is still required. No
dark-matter particle. Not a closed theory. This file builds on CFG554's `VELOCITY_PART_v2.md`. It changes only the velocity
target, which now caps the density at the law's T1 value, and it adds the isotropy audit.

## 1. The statement (unchanged from v2)

State z = (f_b, f_c, φ, π_φ), dz/dt = L·δE + M·δS, with E = E_N + E_φ.
- **Position block of M (Pb, CFG542):** pair transfers driven by the round ψ, with ∇²ψ = 4πG d. The deficit d is two-sided
  (FIX-1).
- **Velocity block of M (CFG550/554):** transfers at fixed x. The zero-entropy partner φ takes Δ(v²/2), so M·δE = 0.
  Radial moves relax about zero, and tangential moves are momentum-conserving pairs (S3).
- Continuum: ∂_t f = (α/τ) ∇_v·[(v − ū) f + σ_*²(x) ∇_v f], with τ = (4πGρ_m)^(−1/2).

## 2. Q1: what the dissipative bracket can and cannot impose

- **I1 (equivariance).** δE/δf = v²/2 + Φ is invariant under v → Rv for every rotation R (checked with sympy using a general
  Cayley rotation).
  - The pair weight Δ(v²/2) equals ½ Δ tr(v vᵀ), so the velocity block reaches the second moment only through the trace.
  - The position block's drive is δ(−F/Θ)/δf = −ψ(x)/Θ, which does not depend on v. So M is SO(3)_v-equivariant at each x.
- **I2.** If a symmetric A commutes with all three rotation generators, then A = a·I. So every rotation-invariant linear
  constraint on Π_ij is a constraint on tr Π.
- **I3.** At fixed tr C, the Gaussian entropy ½ ln det C is maximised at C = (tr C/3)·I. Invariant constraints therefore
  give an isotropic maximiser.
- **I4.** Maximise S_B at fixed ρ(x) and fixed tangential momentum, which are the quantities the velocity block conserves.
  There is no energy multiplier, because the zero-entropy partner takes the energy.
  - The stationary point is f ∝ exp(−η·v_t), which is not normalisable (one half-line integral is ∞).
  - **So the bracket alone fixes no temperature profile.** The profile has to come from the reversible part L.
- **I5.** The tensor (route-a) multiplier term ∂_jλ_i Π_ij is rotation-invariant iff sym ∇λ ∝ I, i.e. iff λ = C r. That is
  the isothermal case, which re-derives CFG554 S1b.

**Reading.** The dissipative structure is isotropic and cannot supply a temperature. The temperature has to be imported from
L's stationarity, and that stationarity is the tensor moment ∂_t(ρu)|_Vlasov = −J. There are two ways to import it:
- the full tensor, which is route (a);
- its rotation average ⟨RΠRᵀ⟩ = (tr Π/3)·I, which is the scalar constraint and gives FIX-2's isotropic target.

The scalar target follows from one principle: an equivariant bracket uses only invariant constraints. Nothing in Pb's GENERIC
conditions implies that principle:
- the velocity block is valid for any reference measure (CFG550/554 S2);
- the round rule acts on the position block, and in spherical symmetry the tensor constraint is itself a single radial
  condition built from shell quantities;
- G9 holds for both options.

So isotropy is a **choice**, now reduced to that single stated principle. The bench (MUTATE MI) selects it.

## 3. Q2: the overfill rule (V3)

    ρ̂ = min(ρ_c, ρ_ph)                 the T1-admissible part of the current density
    P̂(r) = ∫_r^R ρ̂ g dr'              g = field of the current real mass (baryons + all cold energy; G9)
    σ_*²(r) = P̂ / ρ̂                    the isotropic target

- **Where nothing is overfilled at or outside r**, σ_*² equals FIX-2's σ_J² exactly (control C8).
- **In an overfilled region**, set q = ρ_c/ρ̂ > 1. The relaxed pressure is q P̂, and the net force density on the cold energy is
  −∇(ρ_cσ_*²) − ρ_c g = −P̂ ∇q.
  - The overfill therefore spreads under its own excess pressure.
  - The energy comes from the sink (two-way exchange, which Pb's M allows).
- **No new constant.** ρ_ph is the law's own density, and it enters only as the T1 comparison, never in Φ.
- **S2′ (sympy).** Take a reference p*[ρ] that depends nonlocally on the state (two sites).
  - The extra term in δS/δf is independent of v, off equilibrium as well as on it.
  - It equals T₀/Θ at p_c = p*.
  - So CFG554's S2 carries over: the equilibrium stays p_c = p*, and the position drift is unchanged on the
    velocity-equilibrium manifold.
- **Status of the cap.** T1 (ρ_c ≤ ρ_ph inside bound regions) is the law's inequality (CFG541). Taking the hydrostatic
  temperature of the T1 projection of the current density, rather than of the current density itself, is a declared choice.
  The README states how it is counted.
- **Bench outcome (README).** V3 fails.
  - In MW, P stays at 0.38–0.40: −P̂∇q smooths q but does not move a uniform overfill out of r_*.
  - In the clusters it blows up: σ_*² = P̂/ρ̂ is unbounded where ρ_ph ≪ ρ_c, which happens in the point-mass core.
  - So this rule is not the overfill fix.

## 4. Q3 and Lyapunov

- α enters only through rates, so the end states should not depend on α if they are reached. What α sets is the settling
  time t90(α), given in the README from the JSON.
- **Full-system Lyapunov: NOT ESTABLISHED.** V3 changes only the reference. Every candidate still has a Vlasov rate first
  order in the bulk velocity, against O(α) dissipation: dL/dt has a maximum A²/(4Cα) − Bα, which is positive for
  α < A/(2√(BC)).
- The sub-flow H-theorem (relaxation at fixed x toward a fixed target) holds by S2/S2′. Its numerical check (the moment KL
  before and after each relaxation step) is in the JSON.
