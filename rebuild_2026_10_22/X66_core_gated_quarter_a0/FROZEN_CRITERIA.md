# X66_core_gated_quarter_a0: FROZEN CRITERIA (committed alone, before any script or number)

Source: the external model's second proposal, relayed by the owner in chat (10-29), written after the X65 result.
The owner said "run X66".

Standing: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m s⁻², never pooled. Σ_a₀ ≡ a₀/(2πG).
Cold dark energy is not matter and not a particle. No ΛCDM input. Not "theory closed". Lane id X66.

**By-construction warning (stated before any number).** The threshold a₀/4 is chosen so that an isotropic Burkert core
saturates at R = 1 (0.2545 ≈ ½ sphere-vs-slab × 0.5086 Burkert geometry). A pass shows that this feedback rule can be
realized dynamically and is robust. It is NOT a derivation of a₀/(2πG), and NOT an action: the law is velocity-dependent
and non-conservative. Any write-up must say this.

## The law (as proposed)

g_tot = g_N + W · max(0, (a₀/4)/g_σ − 1) · g_N, inward. Here:
- W = Q · Θ(T), with T = 4πGρ_c − 2g_N/r (that is, dg_N/dr > 0).
- Q is X65's stream-sign order parameter (same code).
- g_σ = √((π/3) G ρ_c σ_tot²), with σ_tot² = ⟨v_r² + L²/r²⟩ − ⟨v_r⟩².

Chunk estimates, all from X65's harness (`x65_shells.py`, imported unchanged):
- Shells are sorted by r and grouped in consecutive chunks of K = 32.
- ρ_c is chunk mass over chunk shell volume. σ_tot² is the chunk variance. g_N = G M(<r)/r² at the chunk's mass-weighted r.
- ρ_c and σ_tot² are smoothed by a 3-chunk running mean.
- The boost factor is capped at 100 (numerical; reported if it is ever hit).

Velocity-dependent force in KDK: the acceleration is evaluated with the post-drift positions and the half-step velocities
(stated).

## Runs (X65 numerics otherwise unchanged: N = 2000, ε, dt rule, T = 12 Gyr, averaging over 10–12 Gyr, Burkert fit, R, P)

- **N (Newtonian):** j = 0.1 at all six masses (1e9–1e14 M☉); j = 0.05 and 0.2 at 1e9, 1e10, 1e11, 1e13.
- **G (this law):**
  - canonical, j = 0.1, all masses;
  - alt, j = 0.1, all masses;
  - canonical, j = 0.05 and 0.2, at 1e9, 1e10, 1e11, 1e13;
  - canonical, N = 1000, j = 0.1, at 1e9 and 1e10.
- **MUTATE** (threshold a₀/2 instead of a₀/4): canonical, j = 0.1, all masses. Separate outputs (`X66_MUTATE=1`).

## Pre-checks (fail ⇒ UNDECIDED, exit 1)

- **E1:** N runs |ΔE/E| ≤ 2 %.
- **S1:** Q = 0 whenever r is monotonic in q.

## Verdict

**Per footing, primary j = 0.1, N = 2000.** S = masses with N fit OK and R_N < 0.7. If S is empty ⇒ UNDECIDED.
- **FLOOR EMERGES:** every R_G in S lies in [0.67, 1.5], with spread ≤ 0.2 dex.
- **RAISES, NO FLOOR:** the median lift over S is > 0.1 dex but FLOOR fails.
- **NO EFFECT:** |median lift| ≤ 0.1 dex.

**max() rule.** For masses with R_N > 1.5: REPRODUCED if |log₁₀(R_G/R_N)| ≤ 0.1 for all; otherwise BROKEN.

**j-robustness (canonical; a pass condition).** For each (M, j) with M in {1e9, 1e10, 1e11} and j in {0.05, 0.2}:
- if R_N < 0.7 at that j, require R_G in [0.67, 1.5];
- if R_N > 1.5, require |log₁₀(R_G/R_N)| ≤ 0.1;
- at 1e13, require the max() condition at both j.

ROBUST if every case holds; otherwise j-DEPENDENT.

**Resolution.** N = 1000 within 0.1 dex of N = 2000 at 1e9 and 1e10; otherwise UNRESOLVED.

**Threshold sensitivity (MUTATE).** The median log₁₀ R over S must rise by ≥ 0.2 dex at a₀/2 compared with a₀/4. Otherwise
flag THRESHOLD-INSENSITIVE (the floor would then not be set by the a₀ term).

**OVERALL PASS** = FLOOR EMERGES on both footings + max() REPRODUCED on both + ROBUST + not UNRESOLVED + not
THRESHOLD-INSENSITIVE. Anything else is FAIL, with the failing conditions listed.

**Reported:**
- the final mass fraction with W·boost > 0;
- the maximum boost factor;
- whether the cap was hit;
- g_σ(0)/(a₀/4) at the end in each G run.

**Out of scope:** the cosmic web, the Bullet Cluster, baryons, and any action.
