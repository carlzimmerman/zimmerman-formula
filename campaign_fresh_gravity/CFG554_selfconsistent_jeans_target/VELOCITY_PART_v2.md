# CFG554 VELOCITY PART v2: the self-consistent Jeans target, the equations

Criteria `FROZEN_CRITERIA.md` (01ad75492). Every claim is a sympy result in `cfg554_results.json` (key `sympy`) or a bench
number there; the README gives the verdicts. κ = ½ is fitted. The cold energy's mass is still required. No dark-matter
particle. Not a closed theory. Supersedes nothing in CFG550's `VELOCITY_PART.md`; it replaces only the choice of target.

## 1. The statement (CFG542 Pb with CFG550's velocity block)

State z = (f_b, f_c, φ, π_φ), dz/dt = L·δE + M·δS, E = E_N + E_φ. The velocity block of M is built from transfers at fixed x,
compensated by the coherent zero-entropy partner φ (M·δE = 0). CFG550 showed that this block is symmetric PSD, energy
conserving and has dS/dt ≥ 0 for **any** reference measure p(v|x): the structure does not choose the target. CFG554 asks
what does.

## 2. Route (a): maximum entropy at fixed density under the kinetic stationarity constraint

The velocity block acts at fixed x, so ρ_c(x) is fixed on its orbit. Among those states, take the one of maximum
Boltzmann entropy that leaves the reversible flow momentarily stationary at the moment level:

    maximise  S_B = −∫ f ln f   subject to   ∫ f d³v = ρ_c(x),
                                              J_i ≡ ∂_j Π_ij + ρ_c ∂_i Φ = 0  (= −∂_t(ρu_i)|_Vlasov at u = 0),

with Φ the current Newtonian potential of baryons + cold energy (G9: no phantom in Φ). Multipliers μ(x), λ_i(x).

- **S1a.** After integrating the constraint by parts, δ/δf gives f = exp(−1 − μ + v_i v_j ∂_jλ_i): a Gaussian with inverse
  covariance −2 sym(∇λ). No temperature is inserted.
- **S1b.** Spherical, λ = λ(r) r̂: v_i v_j ∂_jλ_i = λ′ v_r² + (λ/r) v_t², so

      σ_r² = −1/(2λ′),     σ_t² = −r/(2λ)   (per tangential component).

  It is isotropic iff λ′ = λ/r, i.e. λ = C r, i.e. **iff the state is isothermal**.
- **S1c.** SIS: λ = −r/V_f² solves the constraint, σ_r² = σ_t² = V_f²/2 (Jeans residual 0). In the deep regime route (a)
  returns the law's temperature, as it must.
- **S1d.** −∫(δf)²/f < 0 on a linear constraint set: the maximiser is unique where it exists.
- **S1e.** ∫ r·J dV = 0 is the virial theorem 2K = ∫ρ_c r·∇Φ dV, so a total-energy constraint is implied, not added.
- **The multiplier field is fixed by the constraint.** With Λ = −λ > 0 and P = ρ_c σ_r²:

      Λ′ = ρ_c/(2P),     P′ = −ρ_c g − 2P/r + ρ_c/Λ,

  with an isotropic start Λ = c r_in, P = ρ_c/(2c), and P = 0 at the outer face of the occupied region. The single number c
  is found by shooting. The temperature profile is a Lagrange-multiplier field of the current density, not an input.
- **Shape (bench, `final_target` in the JSON).** In the bulk the maximiser is close to isotropic (MW shell β −0.19 to −0.21),
  approaching V_f²/2 where the state is SIS-like.
  - At a compact edge (MW) it turns tangential (edge β −0.68 to −0.92).
  - In a dilute tail it turns radially HOT. σ_t² = r/(2Λ) falls only logarithmically. Wherever σ_t² > V_c²/2, the
    constraint P′ = −ρ(g − 2σ_t²/r) − 2P/r makes P fall more slowly than ρ, so σ_r² = P/ρ rises outward.
  - In the cluster cells this gives σ_r² = 2.7 to 7.1 V_f² at 2 r_*, against an isotropic Jeans value of 0.02 to 0.07
    (edge β +0.15 to +0.55). That is the route-(a) failure mode (README).

**S1f: what FIX-2's isotropy needs.** Add an isotropy constraint Π_rr = (Π_θθ + Π_φφ)/2, with multiplier
ν = 2(λ − rλ′)/(3r). Or replace the tensor constraint by the scalar (Euler-fluid) one, ∇(tr Π/3) + ρ∇Φ = 0. Either way the
maximiser is the isotropic Maxwellian at the isotropic Jeans σ_J² of the current density, which is exactly FIX-2's target,
and it is solvable for any σ_J²(r). The exact Vlasov moment is the tensor one, so isotropy is an extra assumption: route (b)'s
target is POSITED.

**S4.** The route-(a) maximiser is not an exact Vlasov steady state. The v_r³ coefficient of the Vlasov operator acting on
ln f forces σ_r² = const, and the v_r v_t² coefficient then forces ln f = −E/σ_r² − γL². So ρ and ρu are stationary at the
instant, third moments are generated, and the relaxation keeps acting.

## 3. The relaxation (routes a, b, c): metriplectic with a state-dependent reference

Velocity transfers at fixed x, with the partner (CFG550 A2) and reference p*[ρ] (route a: the S1 Gaussian; route b: N(0, σ_J²);
route c: N(0, T_v), T_v = ∫ρ_c r g / 3M).

- **S2.** M is symmetric PSD; M·δE = 0; dS/dt is a sum of squares; mass is conserved.
- The ρ-dependence of p* adds a **v-independent** term to δS/δf, of value T₀/Θ at p_c = p*. So it does not move the velocity
  equilibrium, which stays p_c = p*.
- ∂KL/∂σ² = 0 at the match, so the **position drift is unchanged on the velocity-equilibrium manifold**.
- Continuum (OU, as CFG550): ∂_t f = (α/τ) ∇_v·[(v − ū) f + C[ρ](x) ∇_v f], with C = diag(σ_r², σ_t², σ_t²).
- Energy into matter: (α/τ) ∫ρ_c (tr C − tr Cov)/2. It runs two-way, allowed by M.

**S3: angular momentum.** The radial component relaxes about zero, by single moves (r × r̂ = 0, so Δj = 0). The tangential
components relax about the local mean, by pair transfers that conserve Σv_t, with the partner taking ΔK (M·δE = 0 is kept).

- d⟨v_t⟩/dt = 0, d⟨v_r⟩/dt = −γ⟨v_r⟩, and dVar_t/dt = −2γ(Var_t − σ_t²).
- Stationarity on the pair manifold forces δS/δf to be affine in v_t: a Gaussian with the target covariance and a free
  rotation.
- **Total j is conserved.** Numerically: a rotating shell (20 points × 500 particles, 2000 steps) keeps J to ~1e-15 relative,
  while CFG544's FIX-2 operator decays J by 98%. (The spherical bench stores |v_t| with isotropic orientation, so its J ≡ 0 by
  construction.)

**MK.** Without the partner component, w·δE = (v_j² − v_i²)/2 ≠ 0: energy is not conserved.

## 4. Lyapunov: NOT ESTABLISHED

Every candidate built from F, or from the KL to a ρ-dependent target, has a Vlasov rate first order in the bulk velocity λ,
while all dissipation is O(α):

    dL/dt = λA − α(B + λ²C),   max = A²/(4Cα) − Bα > 0   for α < A/(2√(BC)).

E_N − T S_B is not a candidate, because the self-consistent target is not isothermal (S1b). The sub-flow H-theorem
(drift + relaxation at fixed Vlasov) holds.
