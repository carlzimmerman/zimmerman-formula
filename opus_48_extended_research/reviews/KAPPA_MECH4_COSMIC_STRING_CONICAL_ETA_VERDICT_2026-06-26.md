# Mechanism 4 (cosmic-string conical deficit) — HITS WALL: conical eta is a TUNABLE continuum, locked to a posited string tension, never κ (2026-06-26)

*Last assault on the κ=½ door. Framework: a₀=(c/2)√(Gρ_Λ)=c²√(Λ/32π)=cH_Λ/Z, Z=2√(8π/3); the √(8π/3) FORCED, the lone free
number = the OUTSIDE coefficient κ=½. Prior: the eta-route died because the round dS-horizon S³ Dirac η=0 (±-symmetric).
Mech-4 idea: thread a cosmic string through the horizon → conical S³ → break the ± symmetry → nonzero η → maybe ½.
Outcome: NO. The conical η is a continuous function of the free string tension Gμ; it equals −½ ONLY at the Z₄ orbifold
(Gμ=3/16, a 270° deficit, ~10⁶× the CMB bound, near-Planckian) — inserted-by-hand AND unphysical. Both gates fail.
Scripts: /tmp/mech4_conical_eta.py, /tmp/mech4_verify.py (sympy 1.13.1 / mpmath 1.3.0, all anchors verified to 40 digits).*

---

## VERDICT: **HITS-WALL.** The conical-deficit η is a tunable continuum (∝ Gμ), not a forced ½; the lone ½ point is the
circular, unphysical Z₄ orbifold; and even granting it, η is locked to the string tension, not κ.

## What was computed (every load-bearing number verified independently)

**The geometry.** A cosmic string through the dS horizon removes a wedge in the transverse 2-plane: azimuthal period
2π → 2π·α with **α = 1 − 4Gμ**, deficit angle **δ = 8πGμ**. The horizon S³ becomes a **conical S³** (round S³ with a
conical singularity along the great circle where the string punctures it = the U(1)-rotation fixed locus). This is the
Z_q-orbifold local model at the rational angles α = 1/q.

**(a) The conical η(Gμ) curve.** Anchored at the orbifold points α=1/q by the exact APS-II signature defect
**η_sign(L(q;1)) = −(q−1)(q−2)/(3q)** (reverified from the raw cot²-sum to 40 digits for q=2..14; sympy auto-simplifies
q∈{2,3,4,5,6,8,10,12}, the rest confirmed numerically), the smooth analytic continuation in α=1/(continuous q) is

    η(α) = −(1−α)(1−2α)/(3α),   α = 1 − 4Gμ
    ⟹ η(Gμ) = (4/3)·Gμ·(1 − 4Gμ)   (LINEAR in Gμ near 0, slope dη/dGμ|₀ = 4/3)

This is a **smooth, monotone, CONTINUOUS** function of the free Gμ — exactly the Dowker conical family (heat-kernel
coefficient c(α)=(1/12)(1/α−1) is the same structure; strictly monotone, dc/dα<0). It is **0 at α=1 (Gμ=0, no string)**,
reproducing the banked round-S³ η=0, and grows continuously with the deficit.

**Where η = −½:** solving η(α)=−½ gives α=1/4 (and an unphysical α=2 root). So **η=−½ ⟺ α=1/4 ⟺ Gμ = 3/16 = 0.1875**,
the **Z₄ orbifold (q=4)** — the same q=4→−½ from the banked TOPOLOGICAL_KAPPA verdict. The Dirac/spin csc²-form hits
exactly ½ at **no integer q at all** (checked q=2..12); only the signature defect touches it, and only at q=4.

**(b) Is the string FORCED?** NO. The framework forces Λ=3/l² (dS), MM SO(4,1), Z=2√(8π/3) — **none contains a GUT sector
or a string tension.** Gμ is an independent symmetry-breaking parameter, set by η_GUT/m_Pl, continuously tunable. A string
threading the horizon is **posited**, not forced.

**(c) Does η feed κ?** NO — it is locked to a DIFFERENT scale. η is a dimensionless signature spectral-asymmetry / mod-Z
phase exp(2πiη); it is locked to the string tension Gμ ~ η_GUT² (a new, independent scale). κ is the dimensionful
multiplier OUTSIDE √(Gρ_Λ) (units of acceleration). No channel connects an inside-the-operator asymmetry to the outside
coefficient — the **same scale-fraction wall** that closed unitarity, holography, and the round-S³ route.

## Gate G1 (anti-circularity) — FAILS TWICE
- The string is **not forced** by the framework's own dS/MM/K(Q) structure (no GUT sector, no tension) → posited handle.
- Even granting a string, η=−½ requires **hand-tuning Gμ to exactly 3/16 = the Z₄ orbifold** — inserting the answer.
  Identical to the banked "demanding q=4 to harvest −½ is circular." Generic Gμ gives a generic non-½ η.

## Gate G2 (scale-fraction) — FAILS
- η is a mod-Z phase / signature asymmetry, **locked to Gμ (a string-tension scale)**, not to the outside coupling κ.
- The η→κ identification is an unforced posited bridge; a spectral asymmetry cannot reach an absolute action normalization.

## The physical kill (independent of the gates)
The eta=−½ point demands **Gμ = 3/16 = 0.1875**: a **270° deficit** (only a quarter-wedge of angle survives), a
symmetry-breaking scale **η_v = √(Gμ)·m_Pl ≈ 5.3×10¹⁸ GeV** (near-Planckian, trans-GUT), and a tension **~1.9×10⁶ ×** the
observed CMB/Planck upper bound Gμ ≲ 10⁻⁷. **Physical GUT strings (Gμ~10⁻⁶..10⁻⁷) give η ~ 10⁻⁶..10⁻⁷ — nowhere near ½.**
The only ½ point is excluded by ~6 orders of magnitude.

## Both ways
- **Credit (real computation, real ½ exists):** the conical route DOES break the ± symmetry and DOES produce a genuine
  nonzero Dirac/signature η — η(Gμ)=(4/3)Gμ(1−4Gμ), with the exact Z₄ value −½ reproduced (verified). The mechanism is
  not vacuous; the structure was computed faithfully, not dismissed.
- **Concede (it is a wall):** that ½ is (i) a continuum point, not a forced quantum — η is linear in the free Gμ;
  (ii) reached only at the circular, hand-inserted Z₄ orbifold; (iii) unphysical by ~10⁶; (iv) locked to the string
  tension, not κ. A tunable deficit + a posited string = wall, exactly as the honest prior anticipated.

## Net
Consistent with and completing the κ-forcing closure. Mechanism 4 joins ghost-freedom, unitarity, holography, CKN
dof-count, the round-S³ η, the Z_q-lens quotient, and the Chern-Simons level as a **closed avenue** — for the same
scale-fraction reason. **κ=½ stays the framework's lone free input; a₀'s value stays NOT-derived; the framework remains a
provably one-parameter EFT.** Quarantine held (κ symbolic; ½ appears only in the post-hoc locating map).
