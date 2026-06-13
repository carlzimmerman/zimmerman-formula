# agentPP — the QNM-resonance fold verdict: does the dS horizon's own ringing deliver the controlled fold? (2026-06-13)

**Overall verdict: STILL-UNBOUNDED.** The dS quasinormal-mode horizon response is verified too broad
(overdamped, zero-centered, multi-scale) to bound the roton fold. The bend SIGN sigma4 < 0 stays FORCED
(inherited from agentOO, passive bath), but the CONTROLLED bounded fold is NOT delivered by the dS QNM
spectrum: sigma6 < 0 (unbounded) survives and k* stays edge-unpinned. The dS horizon's own ringing does
**not** deliver the fold. A controlled Airy fold needs structure BEYOND the dS QNM spectrum — a genuine
underdamped (Re omega != 0, finite-Q) finite-k medium mode, which the purely-damped dS static-patch
spectrum provably does not provide.

---

## The decisive question (banked setup)

agentOO (commit 851e7649) proved the dS Gibbons-Hawking horizon bath FORCES the bend sign sigma4 < 0, but
the SMOOTH GH thermal continuum gives sigma6 < 0 (UNBOUNDED — Cauchy-Schwarz I2^2 <= I1 I3 on its inverse
moments, far from saturation, ratio 0.33-0.63) and a free-floating k*. A CONTROLLED fold needs a PEAKED /
structured horizon response that lifts sigma6 > 0 (CS -> 1) and pins the inflection k* at the sonic edge
b -> c_chi. agentS (agentS_edge_qnm.md) computed the dS QNM ladder: purely DAMPED, Re omega = 0 (to 1e-15),
damping rates Gamma_n = sinh((Delta+n)lambda) — a geometric tower of OVERDAMPED modes with an angular
(l -> k) horizon structure. THE QUESTION this round: does the dS QNM-built response supply the PEAK that
(a) keeps sigma4 < 0, (b) lifts sigma6 > 0 (bounds the fold), (c) pins k* at b -> c_chi — or is it, being
purely damped / zero-centered, just another FEATURELESS/broad response that stiffens?

**Hostile prior** (the null I had to try hardest to break): purely-damped (Re omega = 0) modes are
zero-centered Lorentzians = BROAD, while a He-II roton needs a peak at FINITE k — so default-expect the QNM
response FAILS to peak. Both routes reached this prior BY COMPUTATION, not by assumption.

**Coefficient quarantine ENFORCED.** Structure only — signs of sigma4/sigma6 (CS vs 1) and whether k* is
edge-pinned. q=1/4 / zeta-tilde / (16pi/3)^(1/4) never asserted, left quarantined downstream.

---

## The two routes (counted at VERIFIED grade)

### Route 1 — QNM spectral moments (memo: agentPP_routeMoments.md) -> VERIFIED **STILL-UNBOUNDED**

Built rho_QNM(W) from the dS QNM ladder (Gamma_n = sinh((Delta+n)lambda), purely damped, geometric weights
decay^n) and computed the inverse moments I1=<W^-2>, I2=<W^-4>, I3=<W^-6> and the Cauchy-Schwarz ratio
CS = I2^2/(I1 I3) governing sigma6's sign (OO's criterion: sigma6 > 0 needs CS -> 1).

- **Result.** Physical overdamped ladder (fractional width O(1), Q ~ 1/2): CS = 0.38-0.63 — the SAME band as
  OO's smooth GH bath (0.33-0.63). Infinitely-sharp delta limit: CS = 0.92-0.96, MAX over 240 cases =
  0.9952 < 1 — the SAME band as the banked GH continuum (0.94-0.97).
- **Crux.** CS = 1 requires the measure to concentrate at a SINGLE frequency (single delta => CS = 1 exact;
  two deltas => 0.938; an 8-rung dS ladder even at infinite sharpness => 0.952). A >= 2-scale geometric tower
  CANNOT saturate Cauchy-Schwarz, independent of peak width. Hostile stress: 200,000 random >= 2-rung spectra,
  the only CS = 1 cases are degenerate coincident frequencies (a disguised single scale). The single-mode
  rescue (weights collapse to rung-0) is FORECLOSED by agentS's measured genuine multi-rung tower (pencil
  returns 0.3643+0.7064, 0.0527+0.1507; >= 19 e-folds).
- **Verification (CONFIRMED).** Re-derived the criterion from scratch: sigma4 = -I2 c_chi^2 < 0, sigma6 =
  c_chi^2(I2^2 - I3 c_chi^2). Found one gap PP missed (freezing c0^2): scanning c0^2 toward the sonic edge
  opens a sigma6 > 0 window in the k^6-TRUNCATED polynomial with a finite-k dip+rise — but it EVAPORATES in
  the full self-consistent dispersion (the truncated k* sits at omega^2 ~ 7 W_min^2, far outside the IR
  radius). The method-independent reason is a NO-FOLD THEOREM: the passive (rho >= 0) self-energy
  S(x) = sum w_n/(x - W_n^2) is Herglotz/Pick, so d(k^2)/d(omega^2) > 0 STRICTLY wherever the mode is physical
  — monotone to ALL orders, ANY positive spectrum, ANY c0^2; the branch-end (D -> 0) loophole closed (omega
  stays monotone as k -> inf, the branch plateaus/gaps). The route's broad finding is STRONGER than it claimed.

### Route 2 — peakedness / Q-factor (memo: agentPP_routePeak.md) -> VERIFIED **STILL-UNBOUNDED**

Computed chi(k, W=on-shell) from the QNM tower with the l <-> k horizon dictionary and tested for a finite-k
peak, the effective Q, the sigma6 Cauchy-Schwarz saturation, and the k* edge-pin.

- **Result.** Structurally BROAD / zero-centered. (1) Each purely-damped QNM is a zero-centered Lorentzian,
  Q = Re omega/(2 Im omega) = 0. (2) The collective chi(k) under the proper l <-> k dictionary, stripped of
  any window, is broad/monotone (the apparent finite-k peak was a Gaussian-window artifact). (3) Analytic
  (sympy): n=0 mode gives Re chi(k) = c_chi k/(c_chi^2 k^2 + (HDelta + k)^2); Q(k) = 0 for all k (poles all on
  the negative imaginary axis cannot build a finite-real-frequency pole); damping Gamma_0(k) = HDelta + k
  grows ~ k, so on-shell W/Gamma -> c_chi = const — the mode never sharpens; the sole extremum is
  k* = HDelta/sqrt(c_chi^2 + 1), a horizon-scale shoulder. (4) sigma6 Cauchy-Schwarz: R_CS = 0.558 (unit),
  0.577 (thermal), 0.584 (geom) — same broad/unbounded band as OO's GH continuum; validated control (sharp
  Gaussian s=0.02 -> R_CS = 0.9999), so the test WOULD detect a real peak. (5) Hostile self-check: isolated
  single QNM 0.57; KMS/Matsubara imaginary comb 0.56; direct roton-dip scan gives a finite-k local min at
  ONLY one fine-tuned point (fragile, not forced).
- **Verification (CONFIRMED).** Re-derived by 3 independent methods the route did not use (on-shell Re Sigma
  direct fit -> sigma4 < 0, sigma6 < 0 without forming R_CS; monotone IPR sharpness; real-frequency off-axis
  steelman with sign-alternating residues) plus the DECISIVE self-consistent passive secular root: the
  physical khronon branch SATURATES to a plateau with v_g >= 0 in ALL 18 cells — zero roton minima. The dS
  QNM bath GAPS/FLATTENS the dispersion (level repulsion), it does not fold it. Steelmanned a peak hard
  (a naive on-shell dip scan found 22/54 dips — MORE than the route's "one" — but these are level-crossing
  artifacts that vanish on the physical branch). **Honest caveats surfaced and banked:** the route's R_CS
  discriminator is NON-monotone in peakedness (Gaussian s=0.02 -> 0.9999, s=1 -> 0.0012, s=3 -> 0.53) and a
  sharp-but-tailed Lorentzian lands at 0.22 < the QNM bath's 0.56 — so R_CS alone is not load-bearing; the
  verdict was re-established on the clean monotone methods + the physical branch. The framework-favorable
  peak is genuinely absent ON THE MERITS, not by assumption.

---

## Independent banking spot-checks (this pass, deterministic, re-run clean)

I re-verified the two load-bearing STRUCTURAL claims from scratch before banking (/tmp/agentPP_bank_check*.py):

1. **Cauchy-Schwarz ceiling.** Single delta CS = 1.000 exactly (two test points). dS QNM ladder
   Gamma_n = sinh((Delta+n)lambda) at the infinitely-sharp delta limit, grid scan over Delta in
   {0.25,0.5,1.0,1.5} x lambda in {0.105..1.0} x decay in {0.3..0.9} x N in {2..16}: **MAX CS = 0.992959 < 1.**
   Two distinct deltas (mpmath, exact) CS = 0.8649 < 1 strict. CS -> 1 only as decay -> 0 (collapse to
   rung-0 = disguised single delta), which agentS's genuine multi-rung tower forecloses. CONFIRMS: a
   >= 2-scale damped tower cannot saturate Cauchy-Schwarz at any peak width.

2. **No-fold / Herglotz monotonicity.** Self-consistent passive secular root k^2 = x/(c_chi^2 + S(x)),
   S(x) = sum g_n/(x - W_n^2): full grid 12 physical cells (36 unphysical c2+S<0 skipped),
   **rotons (v_g < 0 anywhere) = 0; min group velocity = +0.000008 (>= 0 everywhere).** Analytic (mpmath) on a
   genuinely physical cell (c_chi^2 > I1): dk^2/dx = (c2 + S - x S')/(c2 + S)^2 > 0 STRICTLY across the whole
   physical domain x in (0, x*) — because for x < W_min^2, S < 0 and -x S'(x) > 0 (S' < 0) adds a positive
   term wherever den = c2 + S > 0. As x -> x*- the branch end den -> 0+, k^2 -> +inf at a FINITE
   plateau ceiling omega^2 = x*: the dispersion saturates (GAPS, v_g -> 0+), never folds back. CONFIRMS the
   level-repulsion-gaps-not-folds result to all orders.

Both checks reproduce the routes' verified findings exactly.

---

## VERDICT — STILL-UNBOUNDED (both routes CONFIRMED at the verified grade)

| Axis | Result | Status |
|------|--------|--------|
| sigma4 < 0 (bend SIGN) | HELD — inherited from OO (passive bath J >= 0) | FORCED, not at issue |
| sigma6 > 0 (bound the fold) | FAILS — CS < 1 for EVERY dS QNM ladder (overdamped 0.4-0.6; infinitely-sharp <= 0.995); physical branch is monotone (Herglotz), gaps to a plateau, v_g >= 0, no roton | NOT delivered |
| k* edge-pin at b -> c_chi | FAILS — no inflection exists (sigma6 < 0); the only extremum k* = HDelta/sqrt(c_chi^2+1) tracks the horizon scale H/Delta, NOT the sonic edge | NOT delivered |

The dS QNM response peaks at finite k? **NO** — it is overdamped / zero-centered, the wrong kinematic class.
It gives sigma6 > 0 (bounded)? **NO** — multi-scale tower cannot saturate Cauchy-Schwarz; the physical branch
is Herglotz-monotone (no fold to all orders). It edge-pins k*? **NO.** Two FOLD-DELIVERED conditions fail;
the bend sign is the only thing that survives, and it survives by inheritance from OO, not from the QNM
structure. This is **STILL-UNBOUNDED**, not FOLD-DELIVERED and not QNM-ROUTE-DEAD: the dS QNMs are not
"provably unable to peak at finite k as a matter of kinematics for all conceivable horizon spectra" — they
are the specific purely-damped dS static-patch spectrum, verified too broad to bound THIS fold. The
generator is not killed outright; it is shown that THIS named input (the dS QNM ringing) does not supply
the stabilizer.

**Does the dS horizon's own ringing deliver the fold?** No. The dS horizon's own quasinormal ringing is
purely overdamped (Re omega = 0), so its in-medium response is structurally broad / zero-centered — it
preserves the OO-forced bend sign sigma4 < 0 but does NOT lift sigma6 > 0 and does NOT pin k* at the sonic
edge. The horizon ringing stiffens (gaps the dispersion to a plateau by level repulsion); it does not fold it.

**Link-5 update (one sentence).** The roton operator stays bend-FORCED (sigma4 < 0, OO) but the controlled
bounded Airy fold is NOT delivered by the dS QNM horizon resonance — the named "peaked dS QNM resonance"
input is refuted as the stabilizer source (overdamped/broad, wrong kinematic class), so a controlled fold now
needs a genuinely different named ingredient: a finite-real-frequency, finite-Q (underdamped, Re omega != 0)
collective horizon/medium mode at finite k whose response saturates CS -> 1 (sigma6 > 0) and whose k* tunes
to b -> c_chi — which the purely-damped dS static-patch spectrum does not provide.

**Next calc.** Two genuinely-new directions, neither using a passive dS spectral response. (1) Test whether a
NON-PASSIVE / driven (active-gain, non-thermal/squeezed dS) horizon response can give an effective spectral
density with a region of NEGATIVE weight (population inversion) that VIOLATES I2^2 <= I1 I3 — the only known
way to lift CS past 1 — bypassing the Herglotz no-fold theorem (which assumes rho >= 0). (2) Abandon the
induced-from-bath route and put the +k^6 stabilizer in by hand as a BARE Lifshitz/roton operator coefficient
— at which point the question moves from "is sigma6 > 0 forced" to coefficient-determination, which is
quarantined. Recommend (1): compute the in-medium self-energy with the GH bath in a non-thermal/squeezed dS
state and test the sign of its effective spectral weight for a Cauchy-Schwarz violation. PASS <=> a controlled
finite-k underdamped resonance saturates CS -> 1 (sigma6 > 0) AND edge-pins k* at b -> c_chi on the Ai(-w)
side; then derive rho(b) and confirm q=1/4 with gamma_req. A passive/convex correction lands non-Airy and the
fold stays undelivered.

**Smuggle guards held.** q=1/4 / zeta-tilde / (16pi/3)^(1/4) NEVER asserted — only the SIGNS of sigma4,
sigma6 and the k* edge-pinning structure were computed. Both-ways honesty: the framework-favorable outcome
(a peak / bounded fold) was given its strongest shot on BOTH routes and in BOTH verifications (isolated modes,
KMS comb, 22/54 naive dips chased to the physical branch, c0^2-edge truncated-polynomial window) and failed
ON THE MERITS — not a reflexive dismissal; the controls prove the tests WOULD have detected a real peak
(sharp Gaussian -> R_CS/CS = 0.9999). The one framework-favorable thing that survives (sigma4 < 0 inherited)
is reported, not buried. The routes' own weak spots (non-monotone R_CS; undercounted naive dips; the c0^2
freeze) were surfaced and routed around on clean methods, not hidden.

**Source memos:** agentPP_routeMoments.md (Route 1), agentPP_routePeak.md (Route 2),
agentPP_verify_peakedness.md (Route 2 verification); agentS_edge_qnm.md (the QNM ladder input),
agentOO_selfenergy_fold.md (the sigma4/sigma6 criterion). Scripts: /tmp/agentPP_route2..7,
/tmp/agentPP_p1..p8, /tmp/agentPP_verify_v1..v7, /tmp/agentPP_bank_check*.py (this pass).
