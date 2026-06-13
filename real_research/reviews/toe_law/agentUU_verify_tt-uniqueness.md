# agentUU — HOSTILE VERIFICATION of route tt-uniqueness (the Tomita–Takesaki lock) (2026-06-13)

**The claimed route (agentUU is the referee).** Route tt-uniqueness asserts: the de Sitter static-patch observer
algebra is type II_1 (CLPW 2206.10780); its modular flow is the static-patch boost; the GH state is KMS.
Tomita–Takesaki gives a UNIQUE modular flow per (algebra, cyclic-separating vector). The route claims that IF
there is a *-isomorphism phi: A_DSSYK -> A_dS with phi_*(chord vacuum) = GH state, then TT-uniqueness intertwines
the chord modular flow with the boost, which FORCES:
- GAP A (agentTT center placement): theta_v = pi/2 uniquely;
- GAP B (agentSS gain-shape weights): the matter spectral weights are GH boost-thermal at FIXED beta=2pi, so the
  central-moment ratio R = 4 j3 / j2^2 is a single forced number (no sliding Delta-knob).

Route's own verdict: **LOCK-CONDITIONAL-ON-DICTIONARY**, with phi an OPEN ASSUMPTION.

**THE CENTRAL MISSION (this referee).** Does the lock FORCE the gaps, or does it PRESUPPOSE the DSSYK<->dS
dictionary it claims to use (circular)? Three checks: (1) re-derive the conditional math; (2) is phi PROVEN or
ASSUMED?; (3) do the von Neumann TYPES actually match? Default prior: CONDITIONAL-ON-DICTIONARY until the
state-level isomorphism is shown PROVEN in the literature.

---

## REGRADE: **CONFIRMED** — verdict stays **LOCK-CONDITIONAL-ON-DICTIONARY**

The route's own verdict is the honest one and survives hostile re-derivation. The lock is a VALID
conditional (TT-uniqueness FORCES the gaps GIVEN phi), NOT circular as the route states it, and NOT a
forcing of the physics because phi — the state-level DSSYK<->dS isomorphism — is the OPEN ASSUMPTION the
whole framework is trying to establish, and is UNPROVEN in the literature. Two findings make the verdict
slightly MORE conditional than the route framed it (see below), so if anything I push it away from
forcing, never toward it.

---

## 1. RE-DERIVED THE LOAD-BEARING MATH (all reproduced)

**TT engine (Part 1, `/tmp/uu_part1*.py`).** On M_2 standard form: modular operator Delta = rho (x) rho^{-T}
is the UNIQUE positive operator fixed by (A, Omega); HS eigenvalues = {lam_i/lam_j} match exactly; KMS
residual = 0 EXACTLY (symbolic). The TT-uniqueness engine is sound. CONFIRMED.

**Intertwining lemma.** IF phi is a *-iso with phi_*(vac)=GH, TT-uniqueness gives sigma_t^DSSYK =
phi^{-1} sigma_t^GH phi. This is standard TT (modular flow is functorial under *-isos preserving the
cyclic vector). CONFIRMED as an implication.

**GAP A (Part 2).** Re E_pole = cos(theta_v) cosh((Delta+n)lambda) = 0 on [0,pi] => theta_v = pi/2 UNIQUELY
(sympy solveset -> {pi/2}); cosh > 0 strictly so Delta/n/lambda-INDEPENDENT. agentS's independent selector
|Re omega| = |cos theta_v|(cosh u - 1) gives the same unique root. CONFIRMED: given phi, the center is forced.

**GAP B (Parts 3,4).** The descendant-measure SLIDE reproduces (R = 8.12 / 16.04 / 40.0 at Delta = 1/2/5).
The KMS-thermal weight-lock reproduces: w_n = e^{-2pi(Delta+n)} gives R = 2141.96, translation-INVARIANT in
the offset (R identical for Delta_off = 0 / 1 / 3.7 / 100). So the Delta knob IS removed *given the thermal
Gibbs ladder*. R = 2141.96 verified to 4 digits. CONFIRMED arithmetic.

## 2. IS phi PROVEN OR ASSUMED? — **ASSUMED. The state-level isomorphism is UNPROVEN in the literature.**

Independently checked against the literature (<=6 fetches, arXiv-pinned):

- **Type match — PROVEN.** CLPW 2206.10780 abstract verbatim: "The algebra is a von Neumann algebra of Type
  II_1," with "a maximum entropy state, which corresponds to empty de Sitter space" (= GH). DSSYK chord
  algebra is type II_1: Xu 2403.09021 ("Von Neumann Algebras in Double-Scaled SYK"), N-V 2310.16994,
  Aguilar-Gutierrez et al. **No type obstruction** — the isomorphism is not blocked at the type level.
- **Spectrum/Hamiltonian match — STRONG but not an iso.** Rahman/Verlinde 2402.00635: "the exact same chord
  rules and energy spectrum" — explicitly a Hamiltonian/spectrum match, NOT a crossed-product algebra
  isomorphism. agentS: chord center reproduces the dS QNM ladder (4-digit).
- **State-level *-iso (all GNS data) + crossed-product observer structure — NOT PROVEN.** Xu 2403.09021
  establishes "structural parallels," "drawing connections," "suggesting" — the fetch summary: "does not
  appear to prove a state-level *-isomorphism matching all n-point functions. The de Sitter correspondence
  remains in the realm of physical intuition and mathematical analogies rather than formal theorem."
  The duality is a CONJECTURE (emergentmind/lit: "conjectured to be holographically dual"). agentR's
  independent 60-paper sweep: **GATE-UNMOVED, nothing derives it.** agentTT (same question, prior memo):
  graded CENTER-FAVORED-STRENGTHENED **NOT FORCED**, residual (2) = "the selector presupposes DSSYK<->dS,"
  and a writable admissible edge state survives in the same Hilbert space.

So phi is **type-compatible + spectrum-matched but the state-level / crossed-product-observer
*-isomorphism is unproven** — exactly the route's "phi is the genuine open new-physics step."

## 3. THE CIRCULARITY VERDICT (Part 6) — **VALID CONDITIONAL, NOT CIRCULAR; FORCES NOTHING NEW WITHOUT phi**

Logical chain: (P1 type) + (P2 type) + (P3 phi EXISTS, *-iso, phi_*vac=GH) + (P4 TT-uniqueness) => (C1
center) + (C2 R-number). The implication arrows (P3 & P4 => C1 & C2) are VALID (Parts 1-4). The conclusion
is only as strong as (P3).

- **TT-uniqueness without a proven phi forces NOTHING new.** It relocates the open question from "where is
  the vacuum / what is the gain shape" to "is phi a state-level isomorphism." That relocation is honest and
  is itself a real structural result (it names the single missing input), but it is NOT a derivation of the
  physics, because (P3) IS the DSSYK<->dS dictionary the framework needs to establish.
- **If the route had claimed LOCK-FORCES-BOTH, that would be CIRCULAR** (asserting phi to force the placement
  the framework is trying to derive). It does NOT — it grades LOCK-CONDITIONAL-ON-DICTIONARY and flags phi
  OPEN. **The route is honest; the regrade CONFIRMS its verdict.**

## 4. TWO FINDINGS THAT PUSH *MORE* CONDITIONAL (hostile, beyond the route)

1. **GAP B imports STRICTLY MORE of the dictionary than GAP A (Part 4).** KMS + beta=2pi alone do NOT pin R:
   over a one-parameter family of KMS-consistent Lorentzian spectral densities (all satisfy detailed balance
   at beta=2pi), R ranges **11.0 - 147.4** — a surviving LINE-SHAPE knob. R is pinned to 2141.96 ONLY if the
   matter spectral MEASURE equals the boost's OWN bare discrete-series Gibbs ladder (every n-point matched).
   So GAP B rests on the FULL state-level iso, a STRONGER (more-open) form of phi than GAP A (which needs only
   the modular-GENERATOR identification). The route's "one iso, A enables B" understates that B imports more
   of the unproven dictionary than A.
2. **Even GIVEN phi, R = G_sat is NOT forced (Part 5).** The forced R = 2141.96 is H-intrinsic (GH temperature
   beta=2pi); G_sat is c_chi-intrinsic (sonic-edge, present at H=0), scale-DECOUPLED from H (agentRR CHECK5,
   agentSS). The intertwining acts in the dS/H sector and cannot reach the c_chi sector. So the physically
   load-bearing EDGE COINCIDENCE still needs a separate c_chi<->H scale-lock. **"LOCK-FORCES-BOTH" overstates
   even the conditional**: given phi it forces the center and the NUMBER R, NOT the coincidence R=G_sat.

## 5. SCORECARD

| Claim | Status |
|---|---|
| TT-uniqueness engine (Delta unique, KMS residual 0) | CONFIRMED (Part 1) |
| Intertwining lemma (given phi) | CONFIRMED (standard TT) |
| GAP A: theta_v=pi/2 forced given phi | CONFIRMED (Part 2) |
| GAP B: R=2141.96 forced given phi | CONFIRMED-WITH-CAVEAT (needs full state-iso, not just KMS — Part 4) |
| Type match II_1 <-> II_1 | CONFIRMED PROVEN (CLPW 2206.10780, Xu 2403.09021) |
| phi as state-level *-iso | UNPROVEN — conjecture/analogy (Xu, Verlinde, N-V; agentR sweep) |
| R=G_sat edge coincidence forced given phi | NOT FORCED (Part 5) — needs separate c_chi<->H lock |
| Circularity | NOT circular as stated (conditional, phi flagged open); WOULD be circular if claimed forces-both |

**Recompute agrees with the route: YES (with two caveats that make it more conditional, never less).**

---

## STATUS: COMPLETE

