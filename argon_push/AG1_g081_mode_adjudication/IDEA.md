# AG1 — Adjudicating the flagged G081 boundary of the only live κ = ½ candidate

**Open item addressed:** (2) the rational κ = ½ — via its least-bad candidate's flagged,
unadjudicated boundary (GF2_closure_half README boundary 4). **Answer to "(b) does your
algebra produce the target number with zero inserted constants?": NO — and this lane does
not claim it.** What it does: adjudicates the flagged discrepancy exactly, REVERSES the
stability certification the static branch was committed under, derives the corrected
spectral structure in zero-import closed form, anchors the machinery on the classical
Ebert–Bonnor point to 4 digits, and converts the κ-candidate's cost ledger from a vague
"static branch accepted" into a quantified stability requirement.

## Idea

The only surviving κ = ½ derivation (GF2 self-source closure: static log branch Φ = C ln r
+ Poisson + hydrostatics ⇒ σ² = C/2, zero-number-import ledger) rests on the committed
static branch, whose physical-admissibility certification is G081's stability verdict:
"ω₀² = 0 EXACT, cap-invariant neutral continuum, well-posed linear relaxation, CRITICAL
(marginal)". GF2 itself flagged (unadjudicated): re-deriving G081's linearized momentum
equation could not reproduce its [SELF-CONSISTENT] mode equation — G081's Euler line (L31)
omits the standard force of the perturbed density in the equilibrium field, −δρ∇Φ₀. This
lane adjudicates that flag from first principles. Either outcome is a result: flag
rejected ⇒ κ candidate's boundary cleared; flag upheld ⇒ the branch's stability leg is
reversed and must be re-earned.

## Algebra (sympy + mpmath + scipy; FROZEN_CRITERIA.md committed before any run)

Linearizing continuity + Euler (ALL force terms) + Poisson + isothermal EOS about
ρ₀ = A/r², Φ₀ = C ln r, P₀ = σ²ρ₀, with δρ = −ρ₀ξ′ and φ₁′ = −Cξ/r² (inner mass frozen):

    σ²ξ″ + (C − 2σ²)ξ′/r + (C/r² + ω²)ξ = 0                      (E-corr, general σ²)
    σ² = C/2  ⇒  ξ″ + (ω²/σ² + 2/r²)ξ = 0                        (E-corr*, drift cancels EXACTLY)

- **C1/M2:** deleting −δρ∇Φ₀ from the SAME symbolic machinery reproduces G081's committed
  equation coefficient-by-coefficient (under its exp(ωt) sign convention) and revives its
  {r, r²} zero modes (residuals 0). The discrepancy is exactly the omitted term.
- **C2:** corrected residuals: ξ=r → 2/r, ξ=r² → 4. The double homology zero mode is dead.
- **C3:** G081's premise "homology of the isothermal family at fixed σ²" is not a family of
  equilibria: the ε-rescaled profile has hydrostatic residual −2εC/r + O(ε²) at fixed σ².
- **C4:** exact solutions ξ = √r·J_{±i√7/2}(ωr/σ) (imaginary Bessel order ν₀ = √7/2;
  mpmath pointwise residual < 1e-27); at ω = 0 the basis is √r{cos,sin}(ν₀ ln r) —
  log-periodic, no algebraic mode. On an annulus [r_in, r_b] the ω² = 0 BC ladders are
  zero-import closed forms (F-BC phase atan(√7/5) from (5/2)sinθ + ν₀cosθ = 0):
  DD/FF: w_n = e^{2nπ/√7}, w₁ = 10.7491; DF: w₁ = e^{(π−atan(√7/5))/ν₀} = 7.4403;
  FD: w₁ = 1.4447 (n = 0). One more unstable mode per width factor e^{π/ν₀} = 10.749.
  Numerical shooting reproduces all four first rungs to < 1e-8 in ln w; Sturm counts match
  the ladder. (Frozen-text slip recorded: '~5.4 per rung' → exact 10.7491; closed form
  binding; frozen C4(iv) integer tuple superseded by its own governing clause, matched.)
- **C7:** G081's own domain, the ball (0, r_break], is ill-posed: both branches ~ √r e^{±iν₀ln r}
  → 0 and are L²(A dr) (limit-circle); "ξ(0) = 0" selects nothing; the DD eigenvalue
  diverges as Λ₀ ≈ −0.0245/x_in² (measured slope −2.15 → −2): fall to the center.
  G081's "cap-invariant ω₀² = 0 EXACT" verdict cannot be well-defined.
- **C6 (machinery anchor):** the SAME primitive-equation machinery, generated symbolically
  for general ρ₀ (q = r²ρ₀ξ form: σ²q″ + (Φ₀′ − 2σ²/r)q′ + (4πGρ₀ + ω²)q = 0), reproduces
  the classical Ebert–Bonnor–Antonov critical point on the non-singular isothermal sphere:
  ξ_crit = 6.4508 (lit. 6.451), contrast ρ_c/ρ_edge = 14.0420 (lit. 14.04), stability
  direction λ₀(ξ_R=5.5) = +0.0399, λ₀(8.0) = −0.0274, and the independent turning-point
  criterion peaks at ξ = 6.4500. **M3:** delete the adjudicated term ⇒ NO marginal point
  anywhere on [2,12] — the classical instability is driven ENTIRELY by the term G081 omitted.

## Framework verdict (G081's registered constants, read at runtime; Λ = ω²r_break²/σ²)

| r_in (kpc) | width w | Λ₀(DD) | Λ₀(DF) | conservative verdict | growth |
|---|---|---|---|---|---|
| 0.05 | 126.6 | −392.6 (2 modes) | −392.6 | UNSTABLE | 2.6 Myr |
| 0.10 | 63.3 | −98.1 | −98.1 | UNSTABLE | 5.1 Myr |
| 0.40 | 15.8 | −5.00 | −6.17 | UNSTABLE | 20.5 Myr |
| 0.589 | 10.75 | −0.002 (critical) | −2.41 | UNSTABLE | 32.8 Myr |
| 0.850 | 7.45 | +3.84 | −0.005 (critical) | UNSTABLE (DF) | 691 Myr |
| 1.00 | 6.33 | +5.54 | +0.94 | stable | — |
| 2.00 | 3.17 | +15.83 | +5.77 | stable | — |

Critical inner radii: r_crit(DF) = r_break·e^{−(π−atan(√7/5))/ν₀} = **0.851 kpc** (binding),
r_crit(DD) = 0.589 kpc. Timescale unit r_break/σ = 50.97 Myr. G081's ball (r_in → 0):
violently unstable and ill-posed.

## Consequences

1. **G081 V2/V3/V4 REVERSED** as committed (marginal/critical, neutral continuum,
   well-posed relaxation, formation-gate language). The corrected operator, ladders, and
   ill-posedness theorem replace them. G081 V1 (closure identity) independently
   re-verified exact (C0c) — GF2's algebraic base is untouched.
2. **GF2 boundary 4: FLAG UPHELD — resolved.** GF2's κ = ½ chain stands or falls on its
   remaining boundaries (P1 acceptance, vacuum-coupling ladder), but P1's stability leg
   SHARPENS: the static branch as a CONSERVATIVE isothermal fluid is physically
   admissible only with a stabilizing inner cutoff (r_in > r_crit, MW: > 0.85 kpc) or a
   dissipative channel. The framework HAS the dissipative channel (S3 settling, two-sided
   attractor CFG747/748/776) — but G081's certification of it as "well-posed relaxation
   with neutral family" was the wrong mathematics. κ stays FITTED; this lane derives no κ.
3. **G111 reading-(c) INVALID as written** — it gates the relaxation N-body on preserving
   G081's neutral family and fixed-well scan (F(0) = 4.9998, no sign changes). Corrected
   inputs handed to the conductor: fixed-well ball spectrum is discrete and stable,
   z·cot z + 2 = 0 ⇒ z = 2.2889, 5.0870, 8.0962 (no neutral continuum, no ω = 0 gauge
   mode under the regular center); self-consistent structure = (E-corr*) + ladders.
4. **G081 JSON anomaly recorded:** neutral_families_w2 = {0: 0, ±1: 0} cannot be raw ODE
   residuals on {r, r²} under G081's own printed ODE (would be ∓ω²ξ ≠ 0).

## Kill test

Internal: M1–M4 all fail as designed (pre-registered); EB control within pre-registered
windows. Observational: the corrected CONSERVATIVE reading predicts any settled phantom
annulus wider than w₁ (7.44–10.75 in radius ratio, BC-dependent) collapses in ≲ 50 Myr —
yet SPARC/MW/X-COP show law-obeying settled profiles persisting Gyr across wider annuli.
So the conservative-fluid reading of the settled branch is falsified on observed scales
UNLESS per-halo effective inner cutoffs satisfy r_in > r_crit OR the settling is genuinely
dissipative. Falsifier of this adjudication: a conservative (non-dissipative) certified
N-body run showing wide settled A/r² annuli stable over ≫ 50 Myr. Operational follow-up
(queued, not run here): AG3 — extract effective phantom-annulus widths from SPARC fits,
compare against w₁(DF) = 7.4403.

## Two strongest objections

1. **"The isothermal fluid is not the framework's medium."** Correct — the phantom is the
   tether medium (W_rem + stiffness). The adjudication is INTERNAL to G081's own declared
   model, constants, and domain: that model's verdict was the branch's committed stability
   certification, and it is reversed on its own terms. Whether the full tether medium
   changes the ladders is registered as AG2 (scale separation suggests stiffness at
   L* ~ 10–15 pc cannot cure kpc-wide annulus instability; W_rem's nonlinear response is
   unanalyzed). Not answered here — honestly open.
2. **"Inner BCs are arbitrary, so the verdict is arbitrary."** The verdict is tabled for
   all four BC pairs; wide-annulus instability holds for ALL of them (first rungs 1.44 to
   10.75 — every pair destabilizes by width ~15 at the latest); the ball ill-posedness is
   extension-independent. What the corrected analysis converts G081's "arbitrary-cap
   invariance" into is a sharp requirement: pick your inner data (cutoff ≥ r_crit) or pick
   dissipation. Both are falsifiable; neither was visible under the omitted term.

**Files:** FROZEN_CRITERIA.md (pre-run commit c902d2cdd) · ag1_adjudicate.py/.out/_results.json
(7/7 gates PASS) · ag1_eb_control.py/.out/_results.json (C6 PASS, M3 as designed) ·
ag1_eb_diagnostic.py/.out (the Robin-BC Sturm-counting debug that fixed the C6 direction
check — preserved per house rule) · HANDOFF_TO_CONDUCTOR.md.
