# agentTT VERIFY — hostile referee of ROUTE 1 (SL(2,R) representation matching) — 2026-06-13

**Claim under review** (route `agentTT_routeRep.md`, parts 1–5):
`placement_constrained = center-favored-not-forced`; verdict word **CENTER-FAVORED-STRENGTHENED**.
The route says the static-patch SL(2,R) modular rep *selects* the center (center → discrete series
D⁺_Δ = GH QNM ladder; edge → continuum band-edge, not even principal series), but this is a
**CONSISTENCY/SHARPENING, not a FORCING**, for two stated reasons (chord algebra is one continuum
rep admitting both placements; the rep-class label is read off the same pole data as agentS's t^{−3/2}).

**CENTRAL MISSION:** distinguish FORCING (edge provably EXCLUDED by the modular/SL(2,R) structure)
from CONSISTENCY (center fits, edge not ruled out). Default prior: 'forced' is overclaimed; honest
likely outcome CENTER-FAVORED-STRENGTHENED.

**Method:** independent re-derivation (not re-running the route), three verifier scripts:
`agentTT_vp1_rep_from_scratch.py`, `agentTT_vp2_edge_survives.py`, `agentTT_vp3_circularity_forcing.py`.
All route parts 1–5 also re-run clean and reproduce their stated numbers.

---

## (1) INDEPENDENT RE-DERIVATION OF THE REP / MODULAR-WEIGHT CLAIM — CONFIRMED

Rebuilt from the banked primitive (agentS line 52: den-factor zeros `q^{Δ+k} e^{i(σθ−θ_v)}=1`):

- `E_pole = cos(θ_v − iu) = cos(θ_v)cosh(u) − i sin(θ_v)sinh(u)`, `u=(Δ+k)λ` — re-derived symbolically
  (sympy), matches agentS exactly (the apparent Im sign is the σ=±1 conjugate-pole branch).
- **CENTER θ_v=π/2:** `Re E_pole = cos(π/2)cosh(u) = 0` IDENTICALLY → boost spectrum purely imaginary
  `ω_k = −i sinh((Δ+k)λ)` → real, half-bounded, integer-spaced ladder `{Δ+k}` → **lowest-weight
  discrete series D⁺_Δ, Casimir Δ(Δ−1)**. Semiclassical `sinh((Δ+k)λ)→(Δ+k)λ` = the GH ladder. ✓
- **λ-independence of the discrete point:** `Re E_pole = cos(θ_v)cosh(u)`, and `cosh(u)>0` strictly,
  so `Re=0 ⟺ cos(θ_v)=0 ⟺ θ_v=π/2` for **any** λ, Δ, k. The route's "exact, λ-independent" claim
  is correct. ✓
- **Casimir is IDENTICAL at both placements** (Δ labels the operator O_Δ, not the vacuum). So any
  center/edge distinction is a **rep-class/weight** distinction, never a Casimir-label distinction.
  Confirmed — and this is load-bearing for what follows.

## (2) IS THE EDGE GENUINELY THE WRONG REP, OR DOES AN ADMISSIBLE EDGE SECTOR SURVIVE?

Tested three candidate surviving sectors (the FORCING-killers):

- **(S-A) Principal series in dS** (the route's own sharpest steelman B3 — dS *does* have
  principal-series QNMs for heavy fields). Tested the edge poles against all three principal-series
  signatures: **(P1)** constant ring freq `Re=±Hν` n-independent — **FAILS** (edge `Re/Re0` grows
  1.0→2.5 like cosh, re-confirmed at ε=1e-3, 0.05, 0.15); **(P3)** poles are bona-fide spectral lines
  on the support — **FAILS** (every edge pole sits BELOW the band floor `cos ε−1`). So the edge is
  **not** a principal-series tower; the surviving late-time object is the continuum band-edge (branch
  point, t^{−3/2}) = the analog of NO discrete irrep. Route CONFIRMED.
- **(S-B) Does the chord algebra ADMIT the edge?** YES — `θ_v=π−ε` is a genuine **interior** point of
  the continuous band `E=2cos θ/√(1−q)` for any ε>0 (only the exact endpoint θ=π is the boundary).
  The chord algebra U_q(su(1,1)) is one continuum rep that admits BOTH placements. **This is the
  forcing pivot:** the only placement-independent algebra does not exclude the edge. CONFIRMED.
- **(S-C) Any intermediate θ_v∈(π/2,π) carrying a discrete tower?** NO — `Re ω_k=cos(θ_v)cosh(u_k)=0`
  needs `cos θ_v=0` → **θ_v=π/2 UNIQUELY**. So the center is not merely *a* discrete option, it is the
  **unique** one. (This is the strongest pro-center fact and I verify it holds — but per S-B it is a
  unique TARGET-hit, not an algebra-internal exclusion of the others.)

**Net (2):** the edge is genuinely OFF the discrete-series target AND not rescuable as principal
series — but it **survives as an admissible chord-algebra sector**. A surviving admissible edge
sector ⇒ CENTER-FAVORED at best, **not FORCED**.

## (3) DERIVED, OR RESTATED? — THE CIRCULARITY LINCHPIN (CONSISTENCY vs FORCING)

This is the decisive test. The route's ATTACK-1 claims the rep-class exclusion is NOT independent of
agentS's t^{−3/2}. I verified this from both sides:

- **(D2, anti-forcing) Input-trace:** the rep-class label of *both* placements is a function of the
  matter-2pt **pole positions** `{ω_pole(θ_v,k)}` ONLY (discrete ⟺ `Re ω_pole=0` ⟺ `cos θ_v=0`;
  not-discrete ⟺ ring + band-exit). agentS's t^{−3/2} uses the SAME pole positions (sub-threshold the
  contour sweeps no poles → Watson sqrt-edge). The **same scalar** `Re ω_pole = cos(θ_v)cosh(u)` drives
  BOTH the rep-class test and agentS's band-exit test. The rep label is **informationally downstream**
  of the agentS discriminator — a strictly weaker-or-equal statement, never an independent forcing.
- **(D1, pro-forcing) Is there an independent gravity-side theorem** (Tomita–Takesaki uniqueness) that
  forces matter-modular = GH-boost only at center? **No.** T–T gives a unique modular flow PER STATE;
  each placement is a different cyclic vector with its own flow. Singling out the center requires
  *demanding* matter-modular = GH-boost — which **is** agentS's "reproduce dS relaxation," now stated
  operator-wise. T–T does not supply that demand. The boost is **diagonal on the placement** (energy
  `E_v=cos θ_v` is its conserved charge) → it cannot dynamically rotate edge→center (witnessed
  numerically). No algebra-internal superselection forces the GH boost onto one vacuum (S-B).

**Net (3):** the modular argument is a **CONSISTENCY** (center fits exactly AND uniquely; edge
off-target) **SHARPENED** to a clean rep-class label — it is **NOT a FORCING**. Nothing new is
*derived* that excludes the edge; agentS's conditional is *restated* in rep language. This respects
agentR's "CONTESTED-TERMINAL at the algebra level": the algebra (chord U_q(su(1,1))) still cannot
pick — exactly as agentR found.

## (4) REGRADE — **CONFIRMED**, regraded verdict **CENTER-FAVORED-STRENGTHENED**

The route's verdict is **correct and honestly stated** in both directions; it does not overclaim
toward FORCED, nor does it under-report the genuine sharpening.

- The claim word in the route header ("CENTER-FAVORED-STRENGTHENED") and the body verdict
  ("center-favored-not-forced") are the SAME grade — favored, strengthened beyond agnostic, NOT forced.
- **Is the modular argument a FORCING or a CONSISTENCY?** A **CONSISTENCY** (with a genuine
  sharpening). The edge is NOT excluded by representation theory acting alone — it survives as an
  admissible interior point of the chord continuum band (S-B), is not rescuable as principal series
  (S-A, a real negative result the route adds), and the "only at center" comes from re-imposing
  agentS's reproduce-dS-relaxation demand (D1/D2), not from an algebra-internal forbidden weight.
- **Added value (so "strengthened" is earned, not empty):** (i) the failure is upgraded from a
  dynamical t^{−3/2} fit to a clean **rep-class** statement (center = discrete series D⁺_Δ; edge =
  continuum branch-cut); (ii) a NEW negative result — the edge is **not** principal series (P1 ring
  grows like cosh, P3 poles below floor), closing the sharpest steelman; (iii) the center is the
  **UNIQUE** discrete placement (S-C). None of these EXCLUDES the edge algebraically, so "strengthened"
  is the right word and "forced" would be the overclaim the mission warned about.

**One honest caveat on the word "strengthened":** the sharpening is real but the EXCLUSION content is
strictly **informationally equal** to agentS (same pole data). So "strengthened" should be read as
*better-characterized* (rep-class clarity + principal-series kill), NOT as *more-excluded*. The route
states exactly this (its own ATTACK 1 lands), so I confirm rather than downgrade — but I flag that a
reader must not mistake "strengthened" for "an independent second forcing." It is not.

### Comparison to Route 2 (modular/KMS) — consistency of the verdict
Route 2 reaches the same `center-favored-not-forced` via a *stronger-input* path (the GH boost-KMS
identification as a theorem: Gibbons–Hawking + Bisognano–Wichmann + Allen), but stops short of FORCED
for the SAME two honest residuals I confirm here: (i) the boost is inner/diagonal on θ_v (cannot
rotate edge→center), (ii) DSSYK↔dS is presupposed. Both routes are mutually consistent and neither
forces. This cross-check raises confidence the FAVORED-NOT-FORCED grade is convention-robust, not an
artifact of one route's framing.

## (5) QUARANTINE — held
Only computed: rep-class labels (discrete/principal/continuum), Casimir Δ(Δ−1), boost-eigenvalue
Re/Im and ring/decay ratios, band-exit thresholds, band-interior membership, the unique discrete root
θ_v=π/2, principal-series signature tests (P1/P3), input-trace of the discriminator. `q=1/4`, Z, a0
NEVER asserted.

---

## BOTTOM LINE
**regrade = CONFIRMED. regraded_verdict = CENTER-FAVORED-STRENGTHENED.** The route's recompute is
independently reproduced (recompute_agrees = yes). The modular/SL(2,R) argument is a **CONSISTENCY**
(center fits the discrete series exactly and uniquely; edge off-target) **sharpened** to a rep-class
statement and augmented by a genuine new negative result (edge ≠ principal series) — but it is **NOT a
FORCING**: the edge survives as an admissible interior point of the single chord continuum rep, and
the exclusion is agentS's reproduce-dS-relaxation conditional restated in rep language (same pole
data, no independent algebra-internal exclusion). Link 8 stays **EDGE-WOUNDED with the wound
sharpened** (center = discrete series D⁺_Δ; edge = continuum branch-cut, not principal series), not
closed. The honest mission-default outcome (favored-strengthened, not forced) is borne out.
