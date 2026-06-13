# agentPP VERIFY — hostile referee on the QNM peakedness route (Route 2)

**Charge.** Independently re-derive agentPP_routePeak.md's finding (the dS QNM horizon
response is BROAD / zero-centered, not peaked => σ6<0 STILL-UNBOUNDED, k* not edge-pinned)
by a DIFFERENT method. PRIMARY check: purely-damped (Re ω=0) modes are zero-centered
Lorentzians; if the route claims a finite-k PEAK was it real or assumed? If the route claims
σ6>0 / FOLD-DELIVERED, assume cherry-pick until shown forced. If the route found
broad/unbounded (it did), steelman a peak HARD before confirming. Then regrade.

Scripts: /tmp/agentPP_verify_v1..vN.py (deterministic, re-run clean). mpmath/sympy/numpy.

---

## 0. What the route actually claimed (so I verify the right thing)

The route's verdict is **BROAD-ZERO-CENTERED / STILL-UNBOUNDED**, NOT a fold-delivered claim.
So my burden is the REVERSE of the cherry-pick hunt: the route reached the framework-HOSTILE
outcome, so I must try hardest to BUILD a peak / lift σ6>0 and only confirm if every honest
attempt fails. (Per instruction (3) + the working rule: verify a "fails" claim as rigorously
as a "works" claim — do not let a framework-unfavorable verdict through on momentum either.)

Route's three sub-claims to test:
- (P) PEAK: Re χ(k) / the response has no finite-k roton peak; only a horizon-scale shoulder
  at k* = HΔ/√(c_χ²+1); Q(k)≡0 ∀k.
- (S) σ6: the Cauchy-Schwarz ratio R_CS = I2²/(I1 I3) ≈ 0.56 for the QNM bath, same band as
  the smooth GH continuum, far from saturation ⇒ σ6<0 unbounded.
- (E) EDGE-PIN: k* tracks H/Δ, no dependence on the sonic edge b→c_χ.

## 1. Independent method #1 — the ON-SHELL self-energy directly (no R_CS proxy)

`/tmp/agentPP_verify_v1.py`. Instead of the route's moment-ratio proxy R_CS, I build the
agentOO Route-2 self-energy object directly: place the bath modes at the QNM damping scales
Γ_N = H(2n+l+Δ), form the passive secular shift Σ(k,w) = k² Σ_N g_N/(w²−Γ_N²) on-shell
(w=c_χk), and fit Re Σ = s0 + s2 k² + s4 k⁴ + s6 k⁶ at small k. This NEVER forms I_p=∫J/W^{2p};
it reads σ4,σ6 straight off the dispersion, the object the fold actually needs.

RESULT (Δ=0.5, c_χ=1): for unit / thermal / geom residues,
σ4 = −10.8 / −21.2 / −10.6 (all <0, BEND) and σ6 = −148 / −297 / −148 (all <0, UNBOUNDED).
**Method-independent corroboration of the route's two key signs: σ4<0 forced, σ6<0 unbounded —
reached without ever forming the R_CS moment ratio.** (P)/(S) corroborated on the first
independent method.

## 2. A FLAW in the route's R_CS discriminator (caught, then routed around)

`/tmp/agentPP_p5.py` / `p6.py` reproduce. The route's discriminator R_CS = I2²/(I1 I3) is
**NOT monotone in peakedness** — the route's own p6 control shows a Gaussian at W0=5 going
s=0.02→0.9999, s=0.2→0.9935, s=1.0→**0.0012**, s=3.0→**0.5293** (re-run, exact). It crashes to
~0 at intermediate width and rises back. And the p5 SHARP Lorentzian (W0=5, γ=0.05) gives
R_CS=**0.2166** — *below* the broad QNM bath's 0.56, because its fat W⁻² tail pollutes the low
moment I1. So "QNM R_CS≈0.56 ⇒ broad" is, by R_CS ALONE, an unreliable read: the QNM bath could
in principle be sharp-but-tailed and land at 0.56 by coincidence. **This is a real weakness in
the route's stated discriminator.** It does NOT overturn the verdict, because the verdict is
re-established below on two CLEAN, monotone methods — but it means the R_CS argument is not
load-bearing on its own, and I down-weight it.

## 3. Independent method #2 — a MONOTONE sharpness measure (IPR width)

`/tmp/agentPP_verify_v2.py` (Attack 1). The IPR effective-width fraction
(∫J)²/(∫J²)/support IS monotone in peakedness (Gaussian: s=0.02→0.0012, s=1→0.059, s=3→0.162).
The QNM bath: 0.903 (unit), 0.553 (thermal), 0.048 (geom). The unit/thermal towers are **far
BROADER than even a very broad (s=3) Gaussian** — broad confirmed on a measure R_CS lacks. The
geom value 0.048 looks "sharp" but `/tmp/agentPP_verify_v3b.py` resolves it: **every** QNM bath
J(W) peaks at W→0 (weight below W=0.5 = 0.013/0.052/0.346 for unit/thermal/geom). The geom
"sharpness" is a W→0 SPIKE (the single lowest damped mode), the OPPOSITE of a roton (which needs
a peak at FINITE W). So all three baths are W=0-centered, none peaked at finite W. (P) confirmed.

## 4. Independent method #3 — real-frequency response, off-axis steelman

`/tmp/agentPP_verify_v2.py` (Attack 2). The genuine steelman for "the angular ladder builds a
collective resonance": compute Im χ(k,w) on the REAL-w axis from the tower, and try
sign-ALTERNATING residues — the only mechanism that could move collective weight off the
imaginary axis. RESULT: |Im χ(k,w)| peaks at **w→0 in every case** (unit/geom × normal/alternating).
The angular tower cannot build a finite-w peak. This is the structural heart of the route's
claim, confirmed by direct real-frequency construction: a sum of poles on the negative-imaginary
axis stays zero-centered, and even sign-alternation does not move the response peak off w=0. (P)
confirmed by a third method.

## 5. The PRIMARY check — was the route's "no peak" assumed, or computed? + a dip the route
## under-counted, fully resolved

The referee charge asks specifically whether the route ASSUMED the overdamped modes can't peak.
It did not — but I found a place the route's hostile self-check (p7) UNDER-reported, and chased it
to ground.

- p7 claimed the direct roton-dip scan gives a dip at "ONLY one fine-tuned point." My
  `/tmp/agentPP_verify_v3b.py` scan of the NAIVE on-shell ω²_eff = c_χ²k² + κ·Re Σ(k) found dips
  in **22/54 cells** — far more than "one." So the route under-counted the naive-construction dips.
- BUT: these dips are an artifact of the NAIVE on-shell construction, not physical.
  `/tmp/agentPP_verify_v4.py`: the dip at k0=0.792 is regulator-stable (good), so it is not an
  eps artifact — but the naive ω²_eff = c_χ²k² + κ Re Σ(k,w=c_χk) is NOT the physical dispersion;
  it evaluates Σ at the BARE on-shell point and crosses the bath modes (w=Γ_N), producing
  level-crossing kinks. The PHYSICAL dispersion is the self-consistent secular root
  ω² = c_χ²k² + k² Σ_N g_N/(ω²−Γ_N²).

- `/tmp/agentPP_verify_v5.py` + `v6.py` + `v7.py` — the decisive method (different from the route's
  entirely): solve the self-consistent passive secular root for the lowest (khronon) branch, with
  the agentOO renormalization c_χ²=c0²−I1 holding c_χ²>0. RESULT, across all 18 cells
  (residue×Δ×c_χ²):
  - the physical branch **SATURATES to a plateau** ω²→const (below the first mode Γ_min²) and
    never comes back down;
  - **min group velocity v_g ≥ 0 EVERYWHERE** (≈+0.00004 to +0.0012, →0⁺ at the plateau, never
    negative) — a roton REQUIRES v_g<0 on a descending side; there is NONE;
  - **zero roton minima in 18/18 cells.**
  So the 22/54 naive "dips" are level-crossing artifacts of evaluating Σ off the physical branch.
  On the physical branch the QNM bath FLATTENS/GAPS the khronon (level repulsion eats the
  dispersion into a plateau) — it does NOT fold it into a roton. **(P) PEAK — confirmed by the
  cleanest method; no roton.**

## 6. The σ6 framings reconciled — both say FOLD-NOT-DELIVERED

`/tmp/agentPP_verify_v6.py`. There IS a subtlety the route's flat "σ6<0 unbounded" wording glosses:
the self-consistent branch has a small-k σ6 that fits POSITIVE (s6 = +108 at kmax=0.2 → +0.04 at
kmax=1.5, sign-stable, magnitude collapsing). But this σ6>0 is merely the local curvature of a
SATURATING plateau — there is no dip for it to bound. So the two constructions give:
  (i) route's naive on-shell Re Σ fit → σ6<0 (unbounded runaway, no stabilizer);
  (ii) self-consistent physical branch → local σ6>0 but a plateau with NO fold to stabilize.
**Neither delivers a controlled bounded roton fold.** The verdict STILL-UNBOUNDED /
FOLD-NOT-DELIVERED is robust to this framing difference — confirmed by two independent
constructions. (The route would have been more precise to say "no bounded fold delivered" rather
than leaning on "σ6<0"; the physical content is the same and is confirmed.)

## 7. Edge-pin (E) — confirmed

`/tmp/agentPP_verify_v3b.py` (sympy). With the on-shell speed carried as a free sonic-edge
parameter b, the only extremum is k* = HΔ/√(b²+1): tracks the horizon scale HΔ, no divergence or
pinning to a sonic-edge scale as b→c_χ. Edge-pin FAILS, confirming route claim (E). The physical
branch (§5) reinforces this: its only scale is the horizon (Γ_min=HΔ), where it gaps — nothing
ties the bend to b→c_χ.

---

## VERDICT — CONFIRMED (broad / FOLD-NOT-DELIVERED / STILL-UNBOUNDED), regrade below

The route's central finding is **CONFIRMED by three independent methods** the route did not use
(on-shell Re Σ direct fit; monotone IPR sharpness; real-frequency off-axis steelman) and by the
**self-consistent physical secular root** (the cleanest, decisive construction):

1. **PEAK — the QNM response is BROAD / not peaked at finite k. CONFIRMED.** Every QNM bath J(W)
   peaks at W→0 (zero-centered), the unit/thermal towers are broader than a very-broad Gaussian on
   a monotone measure, and even sign-alternating residues cannot build a finite-w real-frequency
   peak. The "peak" the framework needs is genuinely ABSENT — it was not smuggled; the route did
   not assume it, it computed its absence, and so did I, four ways.
2. **σ6 / FOLD — NOT DELIVERED. CONFIRMED (with a framing correction).** The physical khronon
   branch SATURATES to a plateau (v_g≥0 in all 18 cells, no descending side, no finite-k minimum):
   the QNM bath gaps/flattens the dispersion, it does not fold it. No roton. The route's "σ6<0
   unbounded" and my "saturating plateau, local σ6>0 but no dip" are two faces of the same
   FOLD-NOT-DELIVERED result.
3. **σ4<0 (bend sign) — held, inherited (passive bath). Not at issue, confirmed not threatened.**
4. **EDGE-PIN — FAILS. CONFIRMED.** k* = HΔ/√(b²+1) tracks the horizon, never the sonic edge.

**The peak finding is ROBUST — the route did NOT assume the peak it wanted; if anything it
assumed the framework-favorable peak might exist and disproved it.** The hostile prior (purely-
damped ⇒ zero-centered ⇒ broad) is REALIZED by computation. I steelmanned a peak HARD (monotone
sharpness, alternating-residue real-frequency response, full physical-branch roton scan across 18
cells) and every attempt failed on the merits. The one place I beat the route — the naive on-shell
dip count (22/54, not "one") — turned out to be level-crossing ARTIFACTS that vanish on the
physical branch, which strengthens, not weakens, the FOLD-NOT-DELIVERED verdict.

### Both-ways honesty
- Framework-FAVORABLE corrections I owed and made: (a) the route's R_CS discriminator is
  non-monotone and not trustworthy alone — flagged and down-weighted; (b) the naive scan has many
  more dips (22/54) than the route's "one." Neither rescues the fold: both dissolve on the physical
  branch. (c) The self-consistent branch's small-k σ6 actually fits POSITIVE — reported, but it
  bounds nothing (no dip).
- Framework-UNFAVORABLE truth held: no finite-k peak, no roton minimum, v_g≥0 everywhere, k* not
  edge-pinned — on four methods. The dS QNM static-patch spectrum is the wrong kinematic class
  (overdamped, Re ω=0) to supply a roton, exactly as the route concluded.

### REGRADE: **CONFIRMED.** Verdict STILL-UNBOUNDED (FOLD-NOT-DELIVERED) stands. The named
"peaked dS QNM horizon resonance" is refuted as the stabilizer source; a controlled Airy fold
still needs a DIFFERENT named input — a genuine underdamped (Re ω≠0, finite-Q) finite-k medium
mode the purely-damped dS spectrum does not provide. σ4<0 remains forced (agentOO, passive bath).

## Smuggle guards (held)
- q=1/4 NEVER asserted; ζ-tilde / (16π/3)^(1/4) quarantined. This round computed ONLY structure:
  peaked-vs-broad, the physical-branch shape, v_g sign, σ4/σ6 signs, k* location.
- The framework-favorable outcome (a peak / bounded fold) was given its strongest shot (monotone
  sharpness, alternating residues, 22/54 naive dips chased to the physical branch) and failed on
  the merits — not dismissed reflexively. Conversely the route's own weak spots (non-monotone
  R_CS, undercounted naive dips) were surfaced, not buried.

## Scripts (all /tmp/, deterministic, re-run clean)
- agentPP_verify_v1.py — on-shell Re Σ direct fit (σ4<0, σ6<0), method #1.
- agentPP_verify_v2.py — Attack 1 (monotone IPR sharpness) + Attack 2 (real-frequency off-axis
  steelman); both broad.
- agentPP_verify_v3b.py — J(W) peak location (all W→0) + naive roton-dip scan (22/54) + edge-pin
  sympy (k*=HΔ/√(b²+1)).
- agentPP_verify_v4.py — regulator-independence of the naive dip (stable ⇒ not eps artifact, but
  off the physical branch).
- agentPP_verify_v5.py — renormalized self-consistent secular root; small-k σ4<0, σ6>0-but-plateau.
- agentPP_verify_v6.py — full branch shape (saturates), window-dependence of σ6, group velocity.
- agentPP_verify_v7.py — physical-branch roton scan across 18 cells: 0 rotons, v_g≥0 everywhere.
- (route's own p4/p5/p6 re-run to confirm its numbers + expose the R_CS non-monotonicity.)
