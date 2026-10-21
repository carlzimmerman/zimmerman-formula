# CFG932 DERIVATION: the energy equation of the record's settling dynamics, and the cost of reaching the law

κ = ½ FITTED. Footings never pooled (nothing in this file uses a footing). Cold energy's mass is required; no particle species.
Not "theory closed". This is a derivation from the record's own equations (CFG541 E1–E9, CFG544 FIX-1/FIX-2, CFG638, CFG542 Pb);
nothing new is posited except where marked **H-ELS** (the post-hoc hypothesis under test).

## 1. The system (CFG638, inside B∩C; outside γ = v_s = 0)

- Cold energy: ∂ₜf + ∇ₓ·[(v + v_s)f] − ∇Φ·∇ᵥf = γ∇ᵥ·[(v − u)f + σ_J²∇ᵥf], γ = α/τ, τ = (4πGρ_m)^(−1/2).
- Drift: v_s = −α 1_B 1_C τ∇ψ, with
  - one-sided (CFG541 E5): ∇²ψ = 4πG d, d = 1_B 1_C max(ρ_ph − ρ_c, 0), ψ ≤ 0;
  - two-sided (CFG544 FIX-1, CFG638): ∇²ψ = 4πG(ρ_ph − ρ_c) on B∩C;
  - gated (CFG639): mobility (drift and OU) only where d = ρ_ph − ρ_c > 0.
- Baryons: Vlasov (E1) (gas hydrodynamics without feedback is energy-conserving and changes nothing below).
- Gravity: ∇²Φ = 4πG(ρ_b + ρ_c) (E2, G9: only real mass gravitates).

## 2. Energy equation (3-D, self-gravity)

Moments of the cold-energy equation with ½|v|²:

- ∂ₜk_c + ∇·(F_k + v_s k_c) = −ρ_c u·∇Φ + γ(3ρ_cσ_J² − tr Π), with k_c = ½ρ_c u² + ½ tr Π.
  - The streaming term integrates by parts to ∫ f v·∇Φ = ρ_c u·∇Φ.
  - The OU term: γ∫½v²∇ᵥ·[(v − u)f + σ_J²∇ᵥf] d³v = −γ[∫v·(v − u)f − 3σ_J²ρ_c] = γ(3ρ_cσ_J² − tr Π).
  - The drift advects k_c in position only (each element keeps its velocity).
- Potential energy W = ½∫ρ_tot Φ dV (symmetric Green's function, Φ linear in ρ_tot):
  dW/dt = ∫(∂ₜρ_tot)Φ dV = ∫ρ_c(u + v_s)·∇Φ dV + ∫ρ_b u_b·∇Φ dV.
- Baryon kinetic energy: dK_b/dt = −∫ρ_b u_b·∇Φ dV.

Summing, with boundary fluxes zero:

**d(K_c + K_b + W)/dt = P_drift + P_bath,  P_drift = ∫ρ_c v_s·∇Φ dV,  P_bath = ∫(α/τ)(3ρ_cσ_J² − tr Π) dV.**

Neither source is a divergence. This reproduces CFG541 §5 (drift sub-flow) and CFG638 K3 (1-D, external Φ), now with self-gravity
and the bath together. **The matter sector's energy is not conserved by the record's settling.**

## 3. The drift power in closed form

**Two-sided (FIX-1).** On B∩C, ψ = Φ_law − Φ with ∇²Φ_law = 4πG(ρ_b + ρ_ph) (CFG544). With g = −∇Φ, g_law = −∇Φ_law:

v_s = −ατ∇ψ = ατ(g_law − g),  so  **P_drift = α∫ρ_c τ g·(g − g_law) dV.**

In spherical symmetry (magnitudes g = GM_tot(<r)/r², g_law = GM_law(<r)/r²):
P_drift = α∫ρ_c τ g (g − g_law) dV, and g − g_law = G[M_c(<r) − M_ph(<r)]/r².
- Where the cumulative cold mass exceeds the law's (a central surplus), v_s points outward and P_drift > 0: **energy is injected**.
- Where it falls short (deficit), v_s points inward and P_drift < 0: energy is released.

**One-sided (E5).** ψ' = G M_d(<r)/r² ≥ 0, so v_s points inward everywhere on B∩C and P_drift ≤ 0. The drift never moves cold energy
outward. A surplus is never removed; it can only grow by inflow (CFG541 V4 minimiser: ρ_c = max(ρ_ph, ρ_c,initial) inside r_*).

**Gated (CFG639).** The drift acts only in deficit cells. With the FIX-1 ψ its direction there is set by the cumulative balance, so
the outward branch survives at the skin of a surplus. That is the erosion CFG889 found with orbits (gated t_50 = 105–148 Myr/α).
The energy for that outward transport is again P_drift > 0.

## 4. Who holds the other side of the books

- **G9 excludes the baryons.** The drift force is not gravitational, so no term couples P_drift to baryonic energy (CFG541 S(iv)).
- **CFG542 Pb's dark-energy partner φ** carries Q = ρ_c α τ 1_B 1_C ∇ψ·∇Φ = −ρ_c v_s·∇Φ, and the closed system (matter + φ) conserves
  energy exactly (CFG542 K2). Removing a central surplus under FIX-1 means Q < 0: **the energy is drawn from the dark-energy
  partner**, not from baryons.
  - An exact Λ cannot exchange energy (∇_μ(Λg^{μν}) = 0, CFG541 S(ii)). Under exact Λ, two-sided settling violates energy
    conservation outright.
  - A canonical partner is singular at DESI's w = −1 crossing (CFG542 K10).
- **The bath** P_bath has no named partner. CFG544 found that the books close only if the dark-energy exchange runs both ways:
  out during settling, back in during reheating.
- **CFG747 tether dynamics (canonical v2 S2).** This is a different, conservative system: r̈ = −GM_b/r² + G²m(<r)²/(a₀r⁴), with
  K2 PASS (ΔE/E ≤ 1.6e-4). A surplus is expelled by the cubic push, whose potential energy grows as m². The energy that unbinds a
  tethered surplus is stored in the tether field itself, so no baryonic energy is needed, and it is expelled in 50–100 t₀ (CFG776).

**Consequence for H-ELS.** In no reading of the record (one-sided, two-sided, gated, tether) does baryonic feedback enter the
cold energy's energy budget. H-ELS therefore requires a new constitutive rule, not present in the record. One minimal form:
the outward branch of the drift is throttled by a feedback budget,

∫ P_drift⁺ dt ≤ ε E_fb,  e.g.  α_eff = α min(1, ε Ė_fb / P_drift⁺) in surplus zones.

It must also replace the dark-energy partner on that branch, and switch off the tether push on surplus cold energy (CFG776: a
tethered surplus does not wait for an energy supply). Neither is derived.

## 5. The cost of reaching the law (Q2): identities used

Let a primordial (p) and a settled (s) equilibrium agree outside R and have M_p(<R) = M_s(<R). The construction is the
intermediate state "settled inside R_x, primordial outside", so the outside is unchanged by construction.

- **(a) Self-consistent.** For a steady self-gravitating system with zero surface pressure, 2K + W = 0, so E = W/2. In
  W = −∫GM(<r)dM/r the shells beyond R contribute identically to both states. Hence
  **ΔE_a = ½[W_s(<R) − W_p(<R)]**, with W(<R) the self-energy of the mass inside R.
- **(b) In the law's potential (primary).** For cold mass in a fixed potential, the virial theorem gives
  E = ∫ρ_c(Φ_law + ½v_c,law²)dV. At equal enclosed mass the zero point cancels, and by parts
  **ΔE_b = ∫_0^R (M_p − M_s)(r) · ½[g_law(r) + 4πGρ_law(r) r] dr.** The integrand is positive in a cumulative-surplus zone.
- **(c) Gross local transport.** The drift is a radial flux, so shells keep their order. With the monotone map
  r_p(m) → r_s(m) and E_law = Φ_law + ½v_c,law², **ΔE_c = ∫dm max(0, E_law(r_s(m)) − E_law(r_p(m)))**. This is the cost when the energy
  released by infalling shells cannot pay for lifting the surplus (as in the record's drift, where each element's work is booked
  locally to the partner). It satisfies ΔE_c ≥ ΔE_b, with ΔE_b equal to the net of the same integrand.
- **Region.** R_x = the outermost radius below r_* at which M_p − M_s changes sign from + to −, i.e. the end of the outermost
  surplus zone.

## 6. Drift work and virial energy

In the drift-only sub-flow, K is untouched. So ∫P_drift dt = ΔW, the full change of potential energy (§2). The bath then moves K
to the Jeans value, ΔK = −½ΔW, and the net matches ΔE_a = ½ΔW. Even when the end state's energy budget is net zero, the drift
alone passes ΔW through the partner and the bath passes −½ΔW back.
