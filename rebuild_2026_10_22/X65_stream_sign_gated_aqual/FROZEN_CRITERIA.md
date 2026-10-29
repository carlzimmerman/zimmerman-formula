# X65_stream_sign_gated_aqual: FROZEN CRITERIA (committed alone, before any script or number)

Source: an external model's proposal, relayed by the owner in chat (10-29). Its mechanism: AQUAL gravity acting on the cold
dark energy only, switched on by a stream-sign order parameter Q. It claims Q enforces the core floor ρ₀r₀ = a₀/(2πG).
The owner's question: run a small 1D spherical-shell collapse and report the core surface density against a₀/(2πG).

Standing: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m s⁻², never pooled. Σ_a₀ ≡ a₀/(2πG)
(107 / 129 M☉ pc⁻²). Cold dark energy is not matter and not a particle. Route E: baryons are absent here; this is a test of
the cold sector's own core. No ΛCDM input. Not "theory closed". Lane id X65 (X60–X64 are taken).

## The model (as proposed, one reduction stated)

Q at a point = 1 − |Σ_s sgn_s m_s| / Σ_s m_s over the streams there. sgn = sign(∂r/∂q) of the Lagrangian map (q = initial radius).
Q = 0 exactly while the map is single-valued.

Field equation as proposed: ∇·[μ(|∇φ|/a₀)∇φ] = 4πG Q ρ_c, with simple μ(x) = x/(1+x). In spherical symmetry
g_φ = g_NQ/2 + √(g_NQ²/4 + g_NQ a₀), where g_NQ = G M_Q(<r)/r² and M_Q = ∫Qρ_c dV.

Force on a cold shell: a = −G M(<r)/r² + L²/r³ − Q (g_φ − g_NQ). The extra term is inward and active only where Q > 0.
**Stated reduction:** the proposal's Lagrangian Qρ_c(φ − Φ_N) also implies a term −(φ − Φ_N)∇Q. It is ill-defined with a
discrete Q and is DROPPED. The verdict applies to the gated-AQUAL pull, which is the mechanism the proposal invokes.

## Numerics (fixed)

- **Units:** kpc, M☉, Gyr; G = 4.4985e-6.
- **Shells:** N = 2000 equal-mass shells. Initial profile at rest ρ_i ∝ (r² + r_c²)^(−1/2), r_c = 0.1 R. R is set so the outer
  shell's free-fall time is 5 Gyr. This is the same collapse epoch for every mass, so Σ_coll ∝ M^(1/3); that is a stated
  simplification, not the EPS scaling.
- **Angular momentum:** L_i = j √(G M(<q_i) q_i), with j = 0.1 primary.
- **Softening:** ε = 1e-3 R.
- **Integrator:** KDK leapfrog, dt = min(0.01 Gyr, 0.02 min_i √(r_i/|a_i|)), floor 1e-7 Gyr, run to T = 12 Gyr.
- **Q evaluation:** sort shells by r and group them in consecutive chunks of K = 32; sgn from np.gradient of r over q-order.
- **Masses:** M = 1e9, 1e10, 1e11, 1e12, 1e13, 1e14 M☉.
- **Runs:**
  - N (Newtonian, gate off; this run does not depend on a₀).
  - G (gated), for each footing.
  - MUTATE (Q ≡ 1 always, ungated AQUAL on the cold sector), canonical footing; outputs written separately.
  - Robustness: j = 0.05 and 0.2 at 1e10 and 1e11 (G canonical, plus the matching N runs); N = 1000 at 1e10 and 1e11 (G canonical).

## Measurement (fixed)

- Time-average ρ(r) over snapshots every 0.1 Gyr in t ∈ [10, 12] Gyr.
- Use log bins between the radii enclosing 1 % and 60 % of the mass (time-averaged), 25 bins.
- Fit Burkert (ρ₀, r₀) by least squares in log ρ, with r₀ bounded to [r_in/3, 3 r_out]. Fit is OK if rms ≤ 0.15 dex.
- **Primary statistic:** R ≡ ρ₀r₀ / Σ_a₀.
- **Secondary statistic (model-free):** P ≡ g_pk / a₀, where g_pk is the peak Newtonian self-pull G M(<r)/r² of the final
  profile for r ≥ r_in.
- Reference values for a Burkert halo: P = 0.2545 R. "Floor" means R ≈ 1 (P ≈ 0.25); "slab reading" means P ≈ 1 (R ≈ 3.9).

## Pre-checks (fail ⇒ verdict UNDECIDED, exit 1)

- **E1:** N runs conserve energy, |ΔE/E| ≤ 2 % over 0–12 Gyr.
- **S1:** whenever r is monotonic in q, max Q = 0 exactly.
- **S2:** in every G run, the mass-weighted Q between r_in and r₀ at the end is ≥ 0.7. Otherwise the gate never switches on,
  and the result is reported as GATE INACTIVE, not UNDECIDED.

## Verdict (per footing, primary j = 0.1, N = 2000)

S = masses whose N run fits OK and has R_N < 0.7 (below the floor). S empty ⇒ UNDECIDED.

- **FLOOR EMERGES:** every R_G in S lies in [0.67, 1.5] and their spread is ≤ 0.2 dex.
- **SLAB READING:** every R_G in S lies in [2.6, 5.9].
- **RAISES, NO FLOOR:** median log₁₀(R_G/R_N) over S > 0.1, but neither of the above.
- **NO EFFECT:** |median log₁₀(R_G/R_N)| ≤ 0.1.

Above-floor masses (R_N > 1.5): max() is REPRODUCED if |log₁₀(R_G/R_N)| ≤ 0.1 for all of them; otherwise BROKEN. Reported
alongside the verdict.

**Flags (attached to the verdict, never change its class):**
- j-DEPENDENT if a j = 0.05 or 0.2 R_G differs from j = 0.1 by > 0.15 dex.
- UNRESOLVED if N = 1000 differs from N = 2000 by > 0.1 dex.
- HARNESS INSENSITIVE if MUTATE equals G within 0.01 dex at every mass.

Also reported: the final mass fraction with Q > 0.5, and the radius where Q first exceeds 0.5 relative to r₀.

**Out of scope (cannot be tested in 1D spherical symmetry):** whether Q fires in cosmic walls and filaments, and the
Bullet Cluster. A pass here is necessary, not sufficient.
