# CFG694 — the three pieces together (frozen criteria, committed alone)

Block CFG690–699. Written before any CFG694 script or number. κ = ½ fitted; both footings, never pooled; the cold energy's
mass is required; no particle species; not theory closed.

## The construction (named before scoring)
One Newtonian-limit action plus one nonlocal reading:

- **Action:** L = −|∇Φ − 4πG P|²/8πG − ρ_bΦ − β|P|³/3 − (γ/2)|∇P|² + (I/2)|Ṗ|².
  - CFG692's critical medium, astra's stiff sector (with its scalar identified as the gravitational potential), and CFG691's
    stiffness are claimed to be this one action.
  - β ↔ a₀ (SI cubic); γ ↔ L* (CFG691).
- **Reading (CFG693):** each system's P is solved with its own baryons and isolated boundary conditions on its free-fall
  basin. Nodes superpose their bound charges ∇·P, which are the cold mass.

## Tests
- **G1 (sympy). Criticality is not a tuning.**
  - Show −|∇Φ|²/8πG + 4πG P·∇Φ/4πG − 2πG P² ≡ −|∇Φ − 4πG P|²/8πG (with the sign conventions of CFG692).
  - Show the P equation is astra's with a = 1/4πG, α = 1, so CFG691's universal profile applies unchanged.
  - **Reading rule (frozen):** if both hold, "W″(0) = 4πG" is restated as "P has no mass term of its own". A mass term
    m²P² would be a new constant and would break SI. R0's criticality item is then **removed**; the SI-cubic item remains.
- **G2 (reading). Solar System:** L*_min = 5.75 pc carries over from CFG691 iff G1 holds.
- **G3 (numbers). Stars do not carry halos.**
  - For M = 1 and 0.3 M☉ stars, at L* = L*_min, compute the star's own phantom mass inside r_b = min(r_J, 1.08 pc).
    - r_J is the free-fall basin radius in the local Galactic tide (CFG693).
    - 1.08 pc is half the mean separation at n = 0.1 star/pc³.
  - Compute it with CFG691's profile: M_ph = g_an r_b²/G.
  - **PASS iff M_ph/M ≤ 0.155 for both masses.** 0.155 is the local non-baryonic-to-baryonic density ratio
    0.013 / 0.084 M☉ pc⁻³ (McKee, Parravano & Hollenbach 2015), a declared external measurement.
- **G4 (numbers). Satellites stay unscreened.** Sifón/PAPER44 satellites, M_b = 10^9.5 and 10^11 M☉ (stellar mass as the
  floor), at their apertures r_bg = 36 and 149 kpc: PASS iff S(r_bg/ℓ_γ) ≥ 0.99 at L*_min. PAPER44's no-EFE fit then stands.
- **G5 (raw SPARC). C2.**
  - The combined interpolation is CFG690's g = g_N + √(a₀ g_N); stiffness is negligible in SPARC galaxies (CFG691). C2 is
    re-scored from CFG690/691: FAIL (Υ band) unless G5b changes it.
  - **G5b (diagnosis, reported).** The next term allowed in W is the SI-breaking quartic c₄(4πG)³P⁴/(4a₀²). The interpolation
    becomes w² + c₄w³ = y, g/a₀ = y + w.
    - Scan c₄ ∈ {0} ∪ [0.01, 100] (log, 0.05 dex) on the CFG4 statistic. Report the smallest c₄ that passes the H2 line
      (rms ≤ 0.110, Υ_disk 0.50–0.80) on both footings, if any, and its rms and Υ.
    - c₄ would be a **second** new constant (CFG679 R1 allows one). A passing c₄ is reported as **REQUIRES A SECOND CONSTANT**,
      never as a C2 pass.
- **G6 (reported). Predictions.**
  - wide binaries (2 M☉ at 10³–10⁴ AU): anomaly/Newton;
  - UFD ladder: ℓ_γ;
  - satellites: full boost.

## Verdict
- **COMBINED CONSTRUCTION CONSISTENT** iff G1, G3 and G4 pass. C2 is reported separately (inherited FAIL, plus the G5b
  diagnosis).
- Still open after any verdict:
  - M1a (attractor);
  - the basin reading as an action term (B1);
  - the relativistic completion (Φ = Ψ);
  - the SI postulate (R0).

## MUTATE (`CFG694_MUTATE=1`, exit 1 iff all bite)
- **M1:** a = 1/(2πG) in G1. The identity must fail.
- **M2:** no stiffness in G3. M_ph/M must be ≫ 0.155.
- **M3:** L* = 10⁴ pc in G4. The 10^9.5 M☉ satellite must be screened (S < 0.99).
