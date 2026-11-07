# SV2 iter_1: is AC18's outside-cone signal physical? FROZEN CRITERIA

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Frozen before any script or number of this lane exists.

## System (unchanged from AC18, read from origin/main)

AC18's weak-field v3s system, frozen local background (charge Pi, MOND ratio x, field direction e = z), retarded GR
for phi by hand, test source m = 1000 kg displaced as v_s t e_s (v_s = 1 m/s, e_s = (1,1,1)/sqrt 3), AC18's kernel
H = -x d_e^2 G_b and its monomial coefficients of g_hat (degree <= 3). Footings never pooled:
canonical (a0 9.3603e-11, Pi = 0.0447 Msun/pc^3, x = 1.15), alt (a0 1.1312e-10, Pi = 0.0514, x = 2.6) (AZ37
transcription, provisional, as in AC18). Graded rows: AC18's 18 outside-cone rows per footing,
(t, r) in {(1 s, 1e9 m), (1 s, 1e10 m), (10 s, 1e10 m)} x 6 directions.

## Q1: does it reach a detector made of matter? (test-matter observable)

Observable: the tidal tensor E_ij = c^2 R_0i0j along a free test-mass pair at rest in the khronon frame
(geodesic deviation d^2 xi^i/dt^2 = -E_ij xi^j). It is gauge invariant at linear order in h. Matter couples to the
metric only (S_m minimal).

Linear GR, harmonic gauge, retarded: Box hbar_mn = -16 pi G T_mn / c^4, with the khronon stress at AC18's order
(Pi u u, A22 D3): dT_00 = c^2 dq, dT_0i = -c Pi dv_i, dT_ij = 0 (background v = 0 in the khronon frame). Then
E_ij = d_i d_j phi + [d_t^2 phi delta_ij + 2 d_t(d_i A_j + d_j A_i)]/c^2 with Box phi = 4 pi G rho, Box A_i =
4 pi G rho v_i. At an observer outside the source's cone only the observer's own past ball (radius c(t - t'))
contributes. To leading order in ct/r:

    E_ij = 4 pi G (4 Q_ij - delta_ij dq),   Q_ij = -Pi Int_0^t (t - t') d_i d_j Xi dt',   tr Q = dq

(trace check: tr E = 4 pi G dq = c^2 R_00 for dust). Corrections are O((ct/r)^2); the verdict is read on the
ct/r = 0.03 rows, and the 0.3 rows are reported. Not included, stated now: 1PN stresses of the P / Xi sector
(they are O(Pi^1) times g_bg/c^2 and outside the cone too; they are a different order in Pi, so they cannot cancel
the computed O(Pi^2) term identically).

Lines (50-digit mpmath, floor = 2^-52 x the sum of |terms| of the evaluated component, as AC18):
- D1 (reaches matter): max |E_ij| > 1e6 x floor at one or more ct/r = 0.03 row, on both footings.
- D2 (carries information): the sender's choice is readable. |E(e_s) - E(-e_s)| > 1e6 x floor on the same rows,
  both footings (flipping the source direction at t = 0 changes the detector reading outside the cone).
- Reported, not graded: the strain of a 1 m pair after time t, |E|_max t^2 / 2; the local khronon energy-density
  change c^2 dq; the statement that energy delivered to a free test pair is second order in the source (work =
  force x displacement, both first order).
- KA: at x = 0 (KA1) and Pi = 0 (KA2) E_ij = 0 exactly (H off-origin vanishes; g vanishes).

## Q2: is the amplitude set by forced quantities?

- F1: the dipole coefficient C(x, n) = |dv_dip| r^5 / (K Pi G m c^2 v_s t^6), K = 4 pi G, must agree across the
  three (t, r) cells to 1e-20 relative (pure scaling, no hidden scale).
- F2: dv is exactly linear in Pi: rerun with Pi -> 2 Pi, ratio 2 to 1e-20.
- F3: gamma (Lstar, the only postulated constant in the leaf operator) does not enter the off-source response:
  sympy, the gamma part of the symbol (gamma k^2 g_hat) is a polynomial, so its kernel is supported on the source.
- FORCED if F1-F3 hold: the amplitude is K Pi G m c^2 v_s t^6 / r^5 times C(x, n), with G, c, the record's Pi and x
  only (Pi and x are law-forced given a0 and the baryons; their Galactic values are AC18's provisional ones).
- Reported: t_dyn = (4 pi G Pi)^(-1/2) per footing and the outside-cone bound, from r > c t:
  |dv| <= C_max (t / t_dyn)^2 G m v_s / (c^3 t). The leading-order expansion holds only for t << t_dyn.

## Q3: does tau-ordering exclude every closed signalling loop, for every observer?

- P1 (Lean, SV2_causality.lean): (a) if grad tau is future timelike (u0 > 0, u0^2 > |u|^2), every future causal
  displacement k (k0 > 0, k0^2 >= |k|^2) has d tau = u0 k0 - u.k > 0; (b) a chain of legs each with d tau >= 0 and
  one leg with d tau > 0 has total d tau > 0, so it cannot return to its start; (c) a luminal return leg to an
  emitter moving at |w| < c arrives at t* >= L/(c + |w|) > 0; (d) a boosted observer can see an instantaneous leg
  run backward in its own time (d t' = -gamma w L / c^2 < 0 for w L > 0), so (a)-(c) are the content, not (d).
- P2 (numeric sweep, a quantifier check, not a knob scan): emitter speeds |w|/c in {0, 0.5, 0.9, 0.99, 0.999999} x 26
  directions; relay offsets L n, 26 directions; loop = instantaneous leg on the leaf + luminal return. Min of
  t* c / L over the sweep must be > 0, and the sweep must find boosted frames where the instantaneous leg runs
  backward (d t' < 0), so the test can see what it excludes.
- P3: the leaves are spacelike on the graded background: 1 - v_rel^2/c^2 > 0 at v_rel = 220 km/s.
- PARADOX-FREE if P1 compiles (0 sorry, standard axioms), P2 min > 0 with backward legs found, P3 holds.

## Label (frozen)

- PHYSICAL if D1 and D2 hold on both footings: the outside-cone signal reaches test matter and carries the sender's
  choice. Qualifiers FORCED (Q2) and PARADOX-FREE (Q3) are attached yes / no.
- HARMLESS-BY-STRUCTURE if E_ij is below 1e6 x floor on every graded ct/r = 0.03 row on both footings (the failure
  stays inside the khronon's own variables), or D2 fails (no information).
- SPLIT if the footings disagree.

## MUTATE (must bite, separate outputs: SV2_MUTATE=1 -> *_MUTATE.json / .out)

AC18's hyperbolic leaf (add -(1/c^2) d_tt to L_Mt; speeds <= c / sqrt(1 + x)). Xi is then zero at every graded
observer at the sample time, so E_ij = 0 and the label must become HARMLESS-BY-STRUCTURE. If it stays PHYSICAL the
detector test cannot tell elliptic from hyperbolic and no label stands.

Kappa = 1/2 FITTED; not theory closed.
