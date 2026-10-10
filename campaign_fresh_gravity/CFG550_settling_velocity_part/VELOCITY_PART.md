# CFG550 VELOCITY PART: the equations

Criteria `FROZEN_CRITERIA.md` (2717e0197). Every claim is a sympy result or a number in `cfg550_results.json`; the README
gives the verdicts. κ = ½ is fitted. The cold energy's mass is still required. No dark-matter particle. Not a closed theory.

## 1. The statement (CFG542 Pb, lifted to phase space)

State z = (f_b, f_c, φ, π_φ). dz/dt = L·δE + M·δS, with E = E_N + E_φ (unchanged), and

    S = −(F + F_v)/Θ,
    F   = (1/8πG) ∫ |∇ψ|²,  ∇²ψ = 4πG (ρ_target − ρ_c)        (position part; two-sided deficit)
    F_v = ∫ ρ_c T_ph KL( p_c(·|x) ‖ p_ph(·|x) ) d³x          (velocity part)

- p_ph(v|x) = f_ph(E_law)/ρ_ph is the law's phase-space phantom: the isotropic (Eddington) distribution of the untruncated
  phantom ρ_ph in Φ_law. T_ph(x) is its second moment, which equals the isotropic Jeans dispersion of the untruncated phantom:

      T_ph(r) = (1/ρ_ph(r)) ∫_r^∞ ρ_ph g_law dr',   g_law = G (M_b + M_ph)(<r)/r²

- M has two blocks. Both are built pair by pair, and both satisfy M·δE = 0 through the partner:
  - Position transfers (CFG542): M = m (e_j − e_i, −ΔΦ) ⊗ (same), with m/Θ = ρ_c α τ 1_B 1_C.
  - Velocity transfers at fixed x: M = m (e_v' − e_v, −(v'² − v²)/2) ⊗ (same), with rate α/τ, τ = (4πGρ_m)^(−1/2).
- No constant beyond G, α (O(1) FREE) and the law's inputs (ρ_ph and the baryons) that class A already takes.

## 2. What follows

**Kinetic equation.**

    ∂_t f_c + ∇_x·[(v + v_s) f_c] − ∇Φ·∇_v f_c = (α/τ) ∇_v·[ v f_c + T_ph(x) ∇_v f_c ]
    v_s = −α τ ∇ψ

The right-hand side is a Fokker–Planck (OU) operator in the Maxwellian closure of p_ph. sympy shows that the flux of the
velocity pairs is −γ(T f′ + v f).

**Target temperature.** It comes from the law's own (ρ_ph, Φ_law), not from an insertion. For the SIS (Φ_law = V_f² ln r):
- f_ph ∝ exp(−E/T) reproduces ρ_ph = V_f²/(4πG r²) iff T = V_f²/2 (sympy);
- the amplitude is fixed as well;
- the Jeans integral gives V_f²/2.

**Energy exchange.** The energy delivered to matter by the velocity block is γ ∫ρ_c (3T_ph − ⟨v²⟩)/2. Its sign is set by the
state:
- cold matter is heated by φ;
- hot matter gives energy to φ.

M is symmetric PSD with M·δE = 0, and dS/dt is a sum of squares in both cases (sympy). So **two-way exchange is allowed**.
The partner must still be coherent (zero entropy, CFG542).

**Moments.** d⟨v⟩/dt = −γ⟨v⟩ and d⟨v²⟩/dt = −2γ(⟨v²⟩ − T) per degree of freedom (sympy). The mean velocity is pulled to zero
in the region's baryon frame, so **angular momentum is NOT conserved** (open).

## 3. Route (c): phase-space inside-out fill (the β → ∞ limit of Lynden-Bell with occupation cap f_ph)

The phase-space deficit is one-sided, f_c ≤ f_ph, with chemical potential E_law. At fixed supply M_cat:

    f_t = f_ph(E) Θ(E_t − E),   E_t fixed by ∫ f_t = M_cat   (no constant)
    ρ_t(r) = ρ_ph(r) · P₃(v_t/√T_ph),   v_t² = 2(E_t − Φ_law(r)),   P₃(x) = [√(π/2) erf(x/√2) − x e^(−x²/2)]/√(π/2)
    T_t(r) = T_ph · [3 I₂(x) − x³ e^(−x²/2)] / (3 I₂(x))

In route (c):
- ρ_t replaces ρ_ph in the position deficit (the density marginal of the same phase-space deficit);
- the OU proposal is rejected outside |v| < v_t (a Gaussian-reversible kernel restricted to the cap);
- the edge is softened by the energy cap itself. That softening is a prediction (see the README for the numbers).

## 4. Routes that fail by construction

- **(a0) Casimir entropy** (strict GENERIC, L·δS = 0). With the partner, stationarity is C′(f) equal in every velocity
  cell, so f is uniform in v: not normalisable, and T → ∞. Without the partner (Landau pairs), a cold element is already
  stationary and σ stays 0.
- **(b) Lynden-Bell with T as a Lagrange multiplier.** A zero-entropy partner gives β = 0 (sympy), so the temperature is
  undetermined. Closed (no sink), T is fixed but too hot (CFG541's ΔW goes into heat). With the cap f_ph, β = 0 gives a
  uniform fraction of f_ph (spread to r_ta), and β = ∞ is route (c).

## 5. Lyapunov

NOT ESTABLISHED (sympy).
- **The phase-space KL to f_ph:** under Vlasov it changes at the rate −∫ f (F′/F) v·∇(Φ_law − Φ). That is zero only where
  the real potential equals the law's.
- **The family L_c = c T H − F (isothermal):**
  - c = 1 is Vlasov-invariant (it equals E_N − T S_B + const). But on a mode about ρ_ph the drift changes it at the rate
    −2πGαε²ρ₀²τ(k²σ² − 4πGρ₀)/k², which is > 0 for k < k_J (super-Jeans scales).
  - For c ≠ 1, the Vlasov term is first order in the bulk velocity while all dissipation is O(α). So dL/dt > 0 for some state
    whenever α < A/(2√(BC)).
- **E_N + Casimirs:** the drift changes them with an indefinite sign, and the relaxation heats cold matter.

The sub-flow H-theorem (drift + velocity relaxation) holds: dS/dt ≥ 0.
