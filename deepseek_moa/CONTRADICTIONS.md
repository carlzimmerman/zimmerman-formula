# CONTRADICTIONS — the live ledger, ranked by attack order

Every entry cites the committed lanes it came from. No new numbers invented.
One contradiction is CLOSED (by the commit named); the rest are open with a
closing condition and an owning lane.

## 1. The deep-limit staircase (the theory's one free parameter misbehaving)

- State: SPARC 0.69 < HI 1.08 < MIGHTEE 1.87 (x1e-10), 2.95x spread AT the deep
  limit; pooled eta = 0.722, 4.6 sigma below the seesaw line.
- What is already closed: the MIGHTEE top step is a registered M/L convention
  (G133/G167: fixed Upsilon 0.6 refit -> a0 ~ 1.08e-10 = 1.005x the HI step;
  the 55 dwarfs never adopt the big a0 at all).
- What remains OPEN: the z0 residual 2.15x (HI 1.075 vs SPARC 0.50 at the SAME
  mass window [8.5,9.5], same z, comparable M/L) — not closable by any
  registered systematic (G208 C5/C9, G133 max 1.25x).
- Closing condition: a per-galaxy a0_eff-deep vs f_dark at fixed (M, z); if the
  trend survives in-sample it is a NEW law (a0_eff = 0.229 a0_DE D^1.47
  candidate, G208 V2), if not it is a sample-selection split.
- Owner: M01-adjacent lane (staircase verdict) — reuse G208's committed arrays,
  do NOT re-ingest.

## 2. The beta envelope (-4.4 sigma) vs the radial map

- State: window mean beta(2-5 R500) = 0.438 +- 0.014 by TWO estimators
  (G203/G206), static null dead at 31 sigma, ideal-infall 0.5 rule EXCLUDED at
  -4.4 sigma; but G209's per-bin profile rises monotonically
  0.033 -> 0.093 -> 0.173 -> 0.305 -> 0.560, WITH the 0.5-class reached at the
  outermost bin (3-5 R500).
- Reading: the window-average was never the right comparison; the envelope
  amplitude needs the realistic NON-SELF-SIMILAR infall with the measured
  beta(r) as boundary condition.
- Closing condition: beta(r) closed form from the two-regime model
  (core-static + streaming envelope) fit to G209's five bins, not a polynomial.
- Owner: M02-adjacent lane (beta closed form).

## 3. The ontology contradiction: Noether charge vs Gauss-map charge; charge vs relic

- State: J^0 = f' phidot = 0 identically on the static branch — "dark mass =
  Noether charge" is EMPTY there (H045/G154); the committed fix assigns
  M_ph(<r) = M_b r/r_M as the GAUSS-map charge of the mu2-flux (G154).
- AND: charge vs relic is a live cross-track contradiction — hy4 H047 says
  lambda_fs = 0 (coherent charge, R(k)=1); deepseek G093/G115 says
  lambda_fs = 0.50 Mpc (warm relic, cutoff ~1e6 Msun).
- Closing condition (registered, G156): subhalo mass function inversion below
  ~1e6 Msun decides; the census scorer (G215, 19 at the 1e5 class, 3.2-4.1
  sigma leaning CHARGE) is executed, the full Drlica-Wagner sample not yet.
- Owner: M03 (the gauss_deep_mond Lean lemma + the one-page ontology).

## 4. The mass triangle

- CLOSED by G212 (commit ec7cae782): the three lines (cosmic-noon m(z*) =
  5.0-5.2 keV; Lyman-alpha forest 3.3-5.7 keV; free-streaming ~4.7 keV) jointly
  marginalized -> m = 5.09 +- 0.10 keV, kill band 4-6 keV (G168). DO NOT redo.

## 5. The D1 integrity item (L258's claim)

- State: a hostile audit claimed one committed certificate fails on standard
  axioms. The claim predates the G055 taint fix (d0f3d645f) and the G047
  salvage (d21aee425); the file it flagged was mid-edit race state.
- Closing condition: per-certificate `lake env lean` compile + axiom prints on
  the CURRENT tree. This gates every Lean-chain claim in the fork.
- Owner: fork sweep (foreground per-file; do not background without consent).

---

## The ruled-out list (never re-attempt — see also DEAD.md)

k^4/local higher-derivative completions (G030/G034 + H053 IR argument),
biharmonic screening (G204), sourced-equation fifth-force reading (G155),
neutrino relic window (f04/f06, structurally empty), photocount shot-noise
(G009), Newtonian attractor (G035), mimetic routes (G043/G048), Horn-A grid
(G032 verdict: fixed congruence is PPN-clean by architecture), strict
bound-cloud wide binaries (G006), n=2.000 as universal deep exponent (G183),
Wang+ 13-sigma vertical (G042), the mass triangle (G212, CLOSED).