# CFG695 — a vacuum whose polarization saturates at a₀ (frozen criteria, committed alone)

Block CFG690–699. Written before any CFG695 script or number. κ = ½ fitted; both footings, never pooled; the cold energy's mass
is required; no particle species; not theory closed.

## Disclosure: how this candidate was found
CFG694's G5b scan (a diagnosis frozen at 08c12aea1) found that the smallest SI-breaking quartic passing the SPARC H2 line is
c₄ = 1. After that run I noticed that, in the frozen normalisation, c₄ = 1 is the third term of the series
W′(u) = u + u²/a₀ + u³/a₀² + … = u/(1 − u/a₀) (u = 4πG P). That is a medium whose polarization **saturates** at u = a₀. This lane
is therefore post-hoc in its origin. It is frozen here before the resummed form is scored on anything.

## The candidate
CFG694's action with W(P) = −(1/4πG)[a₀u + a₀² ln(1 − u/a₀)], u = 4πG|P|. Equivalently W′(u) = u/(1 − u/a₀).
- No new constant: the saturation scale is a₀ itself.
- Unscreened static law: g = g_N + u with W′(u) = g, which gives **g_N = g²/(g + a₀)** (the "simple μ").
- Stiffness, the free-fall basins and the no-mass-term identity are as in CFG694.

## Tests
- **S1 (sympy). Structure.**
  - (a) W's expansion has the critical quadratic (no mass term), the SI cubic of CFG690/692 and the c₄ = 1 quartic.
  - (b) The resummed static law is g_N = g²/(g + a₀): deep g_N = g²/a₀, high-field u → a₀.
  - (c) Stability margins are positive for every u ∈ (0, a₀): longitudinal W″ − 4πG, and the PD condition in every k direction.
  - PASS iff (a)–(c) hold.
- **S2 (raw SPARC, data, decisive).** ν = (1 + √(1 + 4/y))/2 on the CFG4 statistic (CFG690 copy; controls reproduce CFG4's
  ν_mono and CFG690's T3). **PASS iff rms ≤ 0.110 with Υ_disk 0.50–0.80 on both footings** (CFG4 H2).
- **S3 (numbers). Solar System carry-over.** At L* = 5.75 pc the Sun's screened inner anomaly GM/L*² must satisfy u/a₀ ≪ 1, so
  the saturation terms are negligible and CFG691's bound applies unchanged. PASS iff u/a₀ ≤ 1e-3 at 1 AU (both footings).
- **S4 (reported). Surface density.** With u ≤ a₀, a node's phantom mass obeys M_ph(<r) ≤ a₀r²/G, so its mean phantom surface
  density is ≤ a₀/(πG). Report it next to the record's Σ_M = a₀/(2πG).

## Verdict
- **SATURATING VACUUM PASSES C2** iff S1, S2 and S3 pass. Combined with CFG694 (G1, G3, G4) and CFG693, the construction would
  then be consistent on every gate scored in this block.
- **R0 (frozen reading):** saturation at a₀ is one postulate replacing the SI-cubic postulate (the cubic follows from it). It
  scores **R0-SHAPED (saturation)**, never PASS: it was chosen because it reproduces a law shape.
- Unchanged by any verdict here:
  - M1a (attractor), B1 (the basin reading as an action), the relativistic completion, and κ fitted;
  - the wide-binary prediction (Newtonian), which Gaia DR4 tests.

## MUTATE (`CFG695_MUTATE=1`, exit 1 iff both bite)
- **M1:** saturation at 2a₀. S1(b) must fail: the deep coefficient is no longer a₀.
- **M2:** ν = 1. S2 must fail (rms ≥ 0.25).
