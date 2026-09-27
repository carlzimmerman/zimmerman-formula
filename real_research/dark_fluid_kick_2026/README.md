# dark_fluid_kick_2026: the kick as a phase change of the dark order parameter

FL1 (`real_research/dark_fluid_2026/`) identifies the dark carrier as a complex order parameter Φ. It is a superfluid:
new field content, classical at occupation N ≫ 1. FL1 leaves open the kick that clears it from galaxies: the triggered
carrier must leave at a universal v_k = 575–650 km/s (L388's window), a scale separate from the region cap (XR7). This
lane builds that kick inside Φ, as a first-order transition whose latent heat is fixed by the Lagrangian.

This is a construction, not closure:
- the splitting ε, the conversion coupling and its gate exponent q are declared;
- the carrier's mass is still required;
- the field content is FL1's, plus one U(1)-breaking constant.

## The result

**One component cannot do it.** Every homogeneous state of one non-relativistic component with density n has energy
V(n). So a first-order transition must change n, and what it releases per particle, (V − V_hull)/n, depends on where it
happens. On a concrete two-phase V it varies by 3.9× across the unstable range. Its products include the dense phase.
A relativistic field does no better in the NR regime: two homogeneous branches at one charge density coincide there.

**Φ's two real components can.**
- **The splitting.** A small U(1)-breaking mass term, V = m²|Φ|² + ε Re(Φ²) + V₄, splits Φ = (φ_H + iφ_L)/√2 into
  m_H² = m² + ε and m_L² = m² − ε.
- **The carrier.** The cold carrier is the heavy component.
- **Stability.** V is even in each component (Z₂ × Z₂), so a lone φ_H cannot decay.
- **The conversion.** Two φ_H convert to two φ_L, and the pair leaves back to back at exactly v_k = √(m_H² − m_L²)/m_H.
  That gives ε/m² = v_k²/(2c² − v_k²) = 1.84–2.35 × 10⁻⁶ for 575–650 km/s.
- **The latent heat.** It is v_k²/2 per unit mass, set by one constant: universal, isotropic, the same in every halo and
  at every redshift. This is astra's Δm/m ≈ 2 × 10⁻⁶, carried by one field's two components instead of two fields.
- **Bose stimulation.** At FL1's occupations the conversion is a parametric instability of the heavy condensate on the
  shell |v| = v_k. A mode swept through that shell grows by πG²/(4Hδ) e-folds.
- **A sharp trigger.** Converting needs 60–180 e-folds, and the exponent grows as n². So a region converts completely at
  the threshold density and negligibly 6% below it. The trigger is effectively sharp.

**The quartic must be the pure cross term, λ(Im Φ²)² = λφ_H²φ_L².**
- The generic λ|Φ|⁴ gives each component a self-coupling three times the conversion coupling. At the trigger that
  means a self-interaction pressure (sound speed ≈ 22 km/s for m = 2 × 10⁻¹⁹ eV), and products that relax where they
  are made.
- The pure cross term leaves each component a free field away from the conversion. The cold carrier has no pressure,
  and the products free-stream once the heavy pump is spent. Stream crossing is then FL1 F4's linear superposition.

**The vacuum gate stays, as the coupling's dependence on the khronon's expansion.**
- With a constant coupling, the cosmic background converts first, at z ≈ 0.9–4 for the record's threshold.
- The coupling must fall into the past: λ ∝ K^(−2q) with q > 3/4. q = 1.75 reproduces the linear gate's threshold
  scaling, E⁴.
- K = 3H is uniform on the khronon's CMC leaves in bound regions (CV4), so this dependence exerts no force.

## Lane

| Lane | Script | Checks | Result |
|---|---|---|---|
| FK1 | `FK1_kick_as_phase_change.py` | 8/8; MUTATE (ε = 0) fails K2 and K3 (the shell collapses to v ≈ 0.03 v_k or none), rc = 1 | **K1** one component can't (sympy identity; Δ varies 3.9×; NR branches coincide). **K2** the doublet: m_H² − m_L² = 2ε, Z₂ × Z₂ for both quartics (no odd vertices), the φ_H²φ_L² vertex λ/2 (in λ\|Φ\|⁴) or λ; the kick reproduced at 575–650 km/s. **K5** the slow couplings: λ\|Φ\|⁴ gives g_HH = g_LL = 3λ/4m² and G/n = λ/4m²; λ(Im Φ²)² gives g_HH = g_LL = 0 and G/n = λ/2m². **K3** growth √(G² − D²), peaking on the shell at v_res/v_k = 1.0005 / 0.9990 (G = 10⁻³δ). **K4** πG²/(4Hδ) e-folds. **N1** λ_dB(600 km/s) = 0.1 pc at 2 × 10⁻¹⁹ eV (the classical, Vlasov limit, so L388's ballistic kick applies); 61–178 e-folds; negligible below 0.942 n_t. **N2** (reported) a constant coupling converts the background by z = 0.86–1.48 (δ_t = 5) and 2.69–4.01 (δ_t = 25). The background exponent falls into the past iff q > 3/4; with q = 1.75 it peaks at z = 0.30, at 1.35× its z = 0 value, which is 0.054 of the trigger's. **N3** (reported) the λ\|Φ\|⁴ cost: sound speed 22/8.3/2.6/0.15 km/s at the trigger for m = 2 × 10⁻¹⁹ / 10⁻¹⁷ / 10⁻¹⁵ / 10⁻¹⁰ eV, and products relaxing ≈ 10³ C_k times per Hubble time (estimate). |

## Said plainly

- **Field content.** The new content is FL1's, plus ε. The two states are Φ's own real and imaginary parts, not a
  second field.
- **The initial condition is declared.** The misalignment must lie near the φ_H axis. An unconvertible cold φ_L share
  adds to the retained carrier, and MS2's flagship allows at most 0.059 at r_F, so the misalignment must be within about
  14°.
- **The trigger reads the carrier's own density**, not the MOND sector's baryons and phantom. In a virialised halo the
  growth rate also carries the local dispersion (≈ √σ in the threshold). That halo-regime rate is an estimate with O(1)
  factors. Whether L388/L375's trigger variable matches is for the particle-mesh owners to check.
- **Retention, Harvey, X-COP and the flagship are not re-scored here.** In the classical limit the products move exactly
  as L388's ballistic kick, so those results carry over only as far as the trigger variable matches.
- **The gate is not derived.** It is λ's K-dependence, with q = 1.75 chosen to match the linear cell. It would also add
  a source, λ′(K)(Im Φ²)², to the khronon's equation. That source is small, of order the conversion energy (G/mc² ~
  10⁻⁹), but it has not been computed.

## Hand-offs (the owners' calls; nothing outside this folder was edited)

1. **FL1 / V0 writer.** Give the dark slot the potential ε Re(Φ²) + λ(K)(Im Φ²)². Then check two things: the khronon's
   equation with the λ′(K) source, and that the pure cross coupling keeps FL1 F2's kernel invisibility (it has no
   metric derivatives).
2. **The particle-mesh track.** The fluid's trigger is sharp (6% in density) and reads the carrier's own density, with
   a √σ modulation in bound regions. Check the L388/L375 trigger against it.
3. **XR8.** Away from the conversion, each component is a free field under the pure cross term. So the stream-crossing
   question for this model reduces to linear superposition; XR8's self-interacting continua test the other choices.

## Reproduction

`python3 real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change.py` (~1 s). `MUTATE=1` runs its control. The lane
writes `.out`, `_MUTATE.out` and `_results[_MUTATE].json`.
