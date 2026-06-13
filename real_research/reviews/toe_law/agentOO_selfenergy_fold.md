# agentOO — BANKING MEMO: the roton-fold self-energy verdict (does the dS bath FORCE sigma4 < 0?)

**The decisive question (NN, commit d2aff2f7).** The free khronon dispersion is STRICTLY CONVEX
(omega'' = ab/(a+bk^2)^{3/2} > 0 — re-verified by sympy this round, exact). MM/NN proved no free
2-derivative structure makes the Airy edge. The Link-5 generator needs the khronon's effective
dispersion to develop a ROTON FOLD: omega^2_eff(k) = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6 with a
NEGATIVE induced k^4 (bending, sigma4 < 0) AND a +k^6 stabilizer (sigma6 > 0, bounded). The only
admissible active source is the khronon's coupling to the de Sitter HORIZON BATH (Gibbons-Hawking
T_dS = H/2pi, occupation n(W) = 1/(e^{2pi W/H}-1); X2's pumped reservoir). **Does the one-loop
in-medium self-energy Sigma(k) FORCE sigma4 < 0 (roton -> Airy fold) or sigma4 >= 0 (convex -> MM
kill stands)?**

**Coefficient quarantine (enforced).** This round is the SIGN + STRUCTURE of the induced k^4/k^6
(bending vs stiffening, bounded vs unbounded) ONLY. zeta-tilde, (16pi/3)^{1/4}, q=1/4 stay
quarantined and DOWNSTREAM. q=1/4 is NOT asserted anywhere in this memo or either route.

**Both-ways honesty, maximum hostility** (framework-favorable = maximum stakes). The sign was
COMPUTED, never chosen; a convex/kill result IS the firewall outcome and would have been reported.

---

## The two routes, each counted at its VERIFIED grade

### Route 1 — DIRECT ONE-LOOP SELF-ENERGY (loop-direct). VERIFIED: CONFIRMED.
Concrete model: khronon chi (linear gapless omega = c_chi k, foliation Goldstone / EE STEP 1 / Lim)
coupled to the dS Gibbons-Hawking bath (Planck occupation, T_dS = H/2pi), one-loop thermal bubble
self-energy with TRUE Cauchy principal value (the load-bearing methodology fix: naive quadrature
mishandles the Landau pole and gave erratic signs — REJECTED runs c8/c9; scipy quad weight='cauchy'
is correct, c10+). On-shell omega = c_chi k, fit Re Sigma = s0 + s2 k^2 + s4 k^4 + s6 k^6.

- Relevant scalar trilinear g chi phi phi: **sigma4 > 0 (STIFFENING / CONVEX) at EVERY speed ratio
  r = c_chi/c_b in [0.5,3.0]** — the MM/NN FIREWALL reproduced from an explicit one-loop self-energy.
- Admissible DERIVATIVE bath couplings ((d phi)^2 chi: deriv2/timelike/grad2): **sigma4 < 0 (BEND)
  with +k^6 stabilizer (sigma6 > 0, bounded)**, but ONLY for c_chi > c_b (crossover r ~ 1.2-1.5);
  sub-luminal khronon stays convex. At deriv2, r=2: s4 = -2.0e-3, s6 = +1.1e-2 — exactly NN's
  bounded roton-fold pattern.
- The ONE spectrum-FORCED contribution is a POSITIVE thermal mass (m_th^2 > 0, a GAP) — the
  OPPOSITE of what a gapless roton fold wants; the forced piece works AGAINST the mechanism.

Hostile verify (different extractor R/k^4 plateau + exact 4-pt collocation; different regularization
Lorentzian i*eps; full contraction-angle cherry-pick scan): scalar convex is regularization-
independent; the derivative bend at c_chi>c_b is GENERIC (12/13 angles at r=2 — NOT a hand-tuned
single contraction), the s4<0 + s6>0 bounded pattern reproduced by exact collocation; the route's
own tiny-window s6 degradation honestly flagged. **REGRADE: CONFIRMED, FOLD-POSSIBLE-COUPLING-DEPENDENT.**

### Route 2 — SPECTRAL / KRAMERS-KRONIG. VERIFIED: CONFIRMED.
Exact secular dispersion from integrating out the passive linear Gibbons-Hawking bath:
omega^2 = c0^2 k^2 + k^2 int dW J(W)/(omega^2 - W^2), J(W) = W^p coth(piW/H) >= 0 (passivity forced;
coth = the T_dS = H/2pi KMS factor). Convention-free result, reproduced 3 ways (exact secular series,
single-mode exact quadratic root to 1e-7, per-mode moment rule):

   c_chi^2 = c0^2 - I1,   **sigma4 = -I2 c_chi^2 < 0 (BEND, forced)**,   sigma6 = c_chi^2(I2^2 - I3 c_chi^2)

- **The bend SIGN is FORCED**, not a coupling choice: integrating out ANY passive (J>=0) bath gives
  the level-repulsion sign sigma4 = -I2 c_chi^2 < 0 (I2 > 0, c_chi^2 > 0). The IR khronon
  (w2 = c_chi^2 k^2 -> 0) sits below any gapped horizon bath, so the secular root stays on the lower
  branch and bends. Robust across model, the entire shift-symmetric coupling family, and cutoff.
- **But the controlled-fold STRUCTURE is NOT supplied** by the bare GH spectrum: (i) featureless /
  scale-free — no convergent curvature-moment window, monotone peakless response (the stiffening CM
  class, NOT the He-II structured/peaked class); (ii) sigma6 = c_chi^2(I2^2 - I3 c_chi^2) < 0 because
  the Cauchy-Schwarz ratio I2^2/(I1 I3) sits FAR below its ceiling 1 (this round's spot-check:
  0.33-0.63 for the GH coth bath; the route's wider scan went to 1e-8) — the fold is UNBOUNDED, not
  a bounded roton minimum; (iii) the fold location k* is cutoff-set, NOT pinned to the sonic edge.

Hostile verify (exact numeric brentq root, no series; correct w2-variable KK with true passive
Im Pi<0; admissible-coupling scan): every shift-symmetric vertex bends; the route's Block-2 STIFFEN
was a genuine wrong-variable/wrong-passive-sign KK error correctly overruled (it did NOT bury its own
kill-confirming sign by fiat); sigma6<0 unbounded confirmed via Cauchy-Schwarz + exact GH cases.
**REGRADE: CONFIRMED, FOLD-POSSIBLE-COUPLING-DEPENDENT.**

### This memo's independent spot-checks (compute-first, before banking)
- SPECTRAL bend sign reproduced: 3-mode passive bath, exact brentq secular root, fit sigma4(fit) =
  -1.750e-1 vs -I2 c_chi^2 = -1.760e-1 — BEND, matching the rule to ~1%.
- GH Cauchy-Schwarz ratio I2^2/(I1 I3) = 0.63 (p=0.5), 0.57 (p=1), 0.48 (p=2), 0.33 (Lam=20) — all
  < 1, so sigma6 < 0 (UNBOUNDED) on the bare GH bath, reproduced.
- FREE convexity firewall reproduced exactly: omega'' = a*b/(a+b k^2)^{3/2} > 0 (sympy).

---

## OVERALL VERDICT — FOLD-POSSIBLE-COUPLING-DEPENDENT

Both routes are CONFIRMED at FOLD-POSSIBLE-COUPLING-DEPENDENT. Neither was downgraded; neither was
upgraded to FOLD-GENERATED. The mechanism candidate SURVIVES its decisive test as a candidate — the
dS bath genuinely pushes in the roton (bending) direction — but the dS Gibbons-Hawking spectrum does
NOT FORCE a controlled fold, so this is honest partial progress, not a derivation.

**WHICH WAY THE DECISIVE FORK FELL — stated plainly.** The fork is NOT a single yes/no; the two
routes split it cleanly and the split is the result:

- **The bend SIGN sigma4 < 0 is REAL and, for a passive bath, FORCED** (Route 2: -I2 c_chi^2 < 0 for
  any J>=0; Route 1: reachable, generic for a super-luminal derivative coupling). **MM/NN's
  free-convex kill is DOWNGRADED on the sign axis — the active dS pump does bend.** CONVEX-NO-FOLD is
  REFUTED: this is not "no fold."
- **But FOLD-GENERATED is NOT reached.** A controlled, edge-pinned, bounded Airy fold needs three
  more ingredients the bare Gibbons-Hawking spectrum does NOT supply: (1) a +k^6 stabilizer (sigma6 > 0)
  — the featureless GH continuum gives sigma6 < 0 (unbounded runaway), a bounded floor needs a SHARP
  spectral peak the smooth thermal bath lacks; (2) edge-coincidence (k* pinned to b->c_chi) — k* is
  cutoff/coupling-set and free-floating; (3) in Route 1, the bend is a SELECTED choice (derivative
  operator AND c_chi > c_b), not compelled by T_dS = H/2pi. The one thing the GH spectrum genuinely
  FORCES — a positive thermal mass / gap — works AGAINST a gapless fold.

So: **bend sign forced YES; controlled bounded edge-pinned fold forced NO.** The mechanism remains a
MECHANISM-CANDIDATE, now sharpened to a falsifiable target: it needs an internal-scale / sharply-
peaked horizon response (the named next input: the dS-horizon QUASINORMAL-MODE resonance, which IS
peaked, as opposed to the smooth Gibbons-Hawking thermal continuum) to simultaneously lift sigma6 > 0
and pin k* to the sonic edge.

**ONE-SENTENCE LINK-5 UPDATE.** Link 5's named roton operator is no longer free-floating on the SIGN
axis — the dS horizon bath forces the bending direction sigma4 < 0 the Airy fold requires — but it
is NOT yet delivered: the bare Gibbons-Hawking thermal spectrum supplies neither the +k^6 stabilizer
(it gives an unbounded sigma6 < 0) nor the edge-coincidence, so the controlled bounded edge-pinned
fold now hinges on a single NAMED UNBANKED input, a peaked/internal-scale horizon response (the dS
QNM resonance), not on any further computation with the smooth thermal continuum.

**NEXT CALC (named, downstream of this verdict).** Test whether the dS-horizon QUASINORMAL-MODE
spectrum (peaked/resonant, carrying an internal scale, vs the smooth GH continuum) can
simultaneously (a) keep sigma4 < 0, (b) lift sigma6 > 0 by pushing I2^2 toward its Cauchy-Schwarz
ceiling I1 I3 (requires the sharp peak), and (c) pin the inflection k* (omega''(k*)=0) to the sonic
edge b->c_chi (NN tuning condition 2). Only if all three hold does one then check the Ai(-w)
oscillatory-side selection (condition 3) and, finally and still-quarantined, derive rho(b) and test
q=1/4. If only the smooth GH continuum couples, the fold stays unbounded (sigma6 < 0) and free-
floating, and NN's named roton operator still needs the unbanked internal-scale input.

---

## Smuggle guards (held)
- q=1/4 left OPEN, never asserted; zeta-tilde / (16pi/3)^{1/4} quarantined; the round computed
  ONLY the sign+structure of sigma4/sigma6.
- The decisive fork was NOT manufactured: Route 1's most-relevant operator (scalar) is the CONVEX
  firewall; Route 2's one forced piece (the gap) works against the fold; both verifies confirmed the
  routes did not bury their own kill-confirming results (Route 1 reported scalar-convex up front;
  Route 2's Block-2 stiffen was a real KK error, correctly overruled, not discarded by fiat).
- Framework-favorable reading recorded honestly (EE STEP 1 c_chi^2 = O(gamma/alpha) >> 1 lands the
  khronon naturally super-luminal, the bending regime) AND labeled REACHABLE, not FORCED.

## Scripts / memos (all under real_research/reviews/toe_law/)
- Route 1 compute: agentOO_routeLoop.md (c10_cauchy, c11_converge, c12_scaling, c13_deriv, c14-c17).
- Route 1 verify: agentOO_verify_loop-direct.md (v1 plateau, v2 collocation, v3 reg+cherry-pick).
- Route 2 compute: agentOO_routeSpectral.md (block1-7: moment rule, sign audit, exact secular, GH
  moments, peakedness, cutoff, sigma6 floor + Cauchy-Schwarz).
- Route 2 verify: agentOO_verify_spectral.md (block1_numeric exact root, block2vs3 KK, couplings, GHcoth).
- This memo's spot-checks: /tmp/agentOO_bank_spotcheck.py (spectral bend, GH CS ratio, free convexity).
