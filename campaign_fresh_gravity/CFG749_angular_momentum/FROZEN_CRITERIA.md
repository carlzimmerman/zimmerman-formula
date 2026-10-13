# CFG749 — does orbital motion of the cold energy spoil the law? (frozen criteria, committed alone; last ID of 740–749)

Written 2026-10-13, before any CFG749 number. κ = ½ fitted; the cold energy's mass is required; no particle species; not
theory closed.

## Why
CFG747/748: radial cold-energy shells settle onto the law (m = r, the zero-force state) inside ~20 r_M. With angular momentum
L, a shell's force balance becomes −1/r² + m²/r⁴ + L²/r³ = 0. For circular support the expected profile is

m/r = √(1 − v_t²/v_c²) (with v_c² = r/r² + 1 ≈ the law's circular speed²),

i.e. **below** the law by an amount set by rotation. Infalling cold energy carries orbital motion. This decides whether the
mechanism yields the law for realistic cold energy.

## Runs (CFG748 code + a centrifugal term L_i²/r³ per shell; L conserved)
- R₀ = 200, t_end = 6000, N = 4000, dt = 0.005, radial shells otherwise unchanged.
- Initial: a uniform cold sphere with the law's mass. Each shell gets L_i = λ r_i v_c,law(r_i), with
  v_c,law² = r(1/r² + 1/r) in code units, for **λ ∈ {0, 0.3, 0.6}**. λ = 0 reproduces CFG748's uniform run (control).

## Tests
- **A1.** Time-averaged m/r over [5000, 6000] at r = 2, 5, 10, 20. Also the mass-weighted ⟨v_t²/v_c,law²⟩ in each radial bin
  ±20%, and the predicted √(1 − ⟨v_t²/v_c²⟩).
- **Verdict per λ:**
  - **LAW HOLDS** iff |m/r − 1| ≤ 0.05 at r = 2–20;
  - **ROTATION DEFICIT** iff m/r lies below 1 by more than 0.05 and within 0.05 of the predicted √(1 − ⟨v_t²/v_c²⟩) at three or
    more of the four radii;
  - **OTHER** otherwise.

## Reading rule (frozen)
- If λ = 0.3 or 0.6 gives a ROTATION DEFICIT, the mechanism reproduces the law only for **low-angular-momentum cold energy**.
  The size of the deficit then becomes a prediction tied to the cold energy's orbital support, and rotation-supported systems
  fall below the law.
- If LAW HOLDS at λ = 0.6, the mechanism is robust to orbital motion.

## Controls
- **K1.** λ = 0 reproduces CFG748's uniform last-window values within 0.02 at r = 2–20 (shorter run, same dynamics).
- **K2.** Energy conserved to 1e-2. Loosened from CFG748's 1e-3, given its uniform-run failure; declared here before any run.
