# agentOO VERIFY — hostile referee of ROUTE 2 (SPECTRAL / KRAMERS-KRONIG)

**Target claim:** the dS / Gibbons-Hawking bath FORCES `sigma4 < 0` (negative-bending) in
`omega^2_eff(k) = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6`, via the exact secular dispersion
`omega^2 = c0^2 k^2 + k^2 ∫dW J(W)/(omega^2 - W^2)`, giving the rule
`sigma4 = -I2 c_chi^2`, `sigma6 = c_chi^2(I2^2 - I3 c_chi^2)`, with verdict
**FOLD-POSSIBLE-COUPLING-DEPENDENT** (sign forced, controlled bounded edge-pinned fold NOT supplied).

Default skepticism applied: a fold that closes the framework's deepest gap is assumed
cherry-picked until shown forced. Coefficient quarantine respected — only SIGN/STRUCTURE tested,
q=1/4 never asserted.

---

## (1) Independent re-derivation of the sigma4 SIGN — different method (exact numeric root, NO series)

`agentOO_verify_block1_numeric.py`. I distrust the analytic Taylor expansion (sign flips hide in
conventions), so I solved the secular equation as an **exact numeric root** (brentq on the lower
branch `w2 ∈ (0, W_min^2)`), then read sigma4 by a finite-difference fit in `u=k^2`. No kernel
choice, no expansion convention.

Result — **BEND (sigma4<0) in every case**, matching `-I2 c_chi^2`:

| bath | c_chi^2 (fit/pred) | sigma4 (fit) | pred -I2 c_chi^2 | sign |
|---|---|---|---|---|
| single W=1,g2=0.1 | 1.34000/1.34000 | -1.340e-1 | -1.340e-1 | BEND |
| single W=2,g2=0.5 | 2.12500/2.12500 | -6.640e-2 | -6.641e-2 | BEND |
| 3 modes 1,2,3     | 1.55389/1.55389 | -1.670e-1 | -1.670e-1 | BEND |
| broadband 1..10   | 3.95412/3.95412 | -1.237e-1 | -1.237e-1 | BEND |

The sign is reproduced by a method genuinely independent of the route's series algebra. **Confirmed.**

## Block2-vs-Block3 clash resolved AGAINST the inconvenient sign honestly

`agentOO_verify_block2vs3.py`. The route contained an internal contradiction: Block 2 (symmetric-KK
kernel `2W/(W^2-x^2)`) gave sigma4 **>0 (STIFFEN, kill-confirming)**; Block 3 (secular) gave
sigma4 **<0 (BEND)**. The route declared Block 3 "exact" and overruled Block 2. A hostile referee
must check this is not the route discarding the kill-confirming sign by fiat.

I re-derived the Kramers-Kronig reconstruction **in the physical `w2` dispersion variable with the
true passive `Im Pi(nu) < 0`**:
- `Im Pi(nu)/k^2 = -pi J(√nu)/(2√nu)`  (retarded, passive)
- `Re Pi(w2)/k^2 = (1/pi) P ∫dnu ImPi/(nu-w2) = P ∫dW J(W)/(w2-W^2) = S(w2)`  ← **reproduces Block 3 exactly**, with all-negative coefficients `S = -(I1 + w2 I2 + ...)`, hence `sigma4 = -I2 c_chi^2 < 0`.

Block 2's positive sign came from doing KK in the `omega` variable with `a(W)` treated as
`+Im Sigma` — a wrong-variable + wrong-passive-sign pair that flips the result. So the route's
overrule of its own Block 2 is **correct, not convenient**: the properly-done KK and the exact
numeric root BOTH land on BEND. The route did not bury the kill-confirming sign; that sign was a
genuine error.

## (2) Cherry-pick test — was sigma4<0 pre-shaped by the coupling/cutoff choice?

`agentOO_verify_couplings.py`. I scanned the admissible coupling space (passive bath `J>=0` +
shift-symmetric/gradient vertex), exact root each time:

| coupling | sigma4 | sign |
|---|---|---|
| deriv/momentum `Pi=k^2 S` (route's) | -7.13e-2 | BEND |
| time-deriv `Pi=(w2/c0^2)k^2 S` | -4.72e-2 | BEND |
| mixed `Pi=(k^2+w2/c0^2)S` | -1.35e-1 | BEND |
| higher-grad `Pi=k^4 S` | -4.72e-2 | BEND |

**The sign does NOT flip with the admissible coupling.** Every shift-symmetric vertex gives BEND.
This is the cherry-pick refutation: the route did not select a coupling pre-shaped to bend — the
whole admissible family bends.

**Mechanistic reason (and the only way to flip):** the bend sign `-I2 c_chi^2 < 0` is forced
whenever the on-shell mode sits BELOW the bath band. The IR khronon `w2 = c_chi^2 k^2 → 0` as
`k→0` is below ANY gapped positive bath, so the secular root stays on the lower branch and bends.
The ONLY way to get STIFFEN is genuine bath weight at exactly `W=0` (a second degenerate gapless
sound mode) overlapping the khronon — which is not a horizon bath and not admissible. I tested
pushing `W_min → 0` (0.3, 0.05, 0.01): the sign stayed BEND until the mode destabilized. **The
bending sign is FORCED by passivity + the gapped horizon bath, not cherry-picked.**

## (3) Steelman both the fold and the kill on the ACTUAL Gibbons-Hawking coth bath

`agentOO_verify_GHcoth_struct.py`. I ran the real `J(W) = W^p coth(piW/H)` spectrum with an
IR+UV band `[Wir,Lam]` (Block-6 cutoff regularization), exact secular root:

| p, band | c_chi^2 | sigma4 | sigma6 (pred) | CS ratio I2^2/(I1 I3) |
|---|---|---|---|---|
| 0.5 [1,5]   | +7.87 | -1.58 BEND | -12.6 runaway | 0.629 |
| 0.5 [1,20]  | +7.43 | -1.85 BEND | -11.2 runaway | 0.463 |
| 1.0 [1,5]   | +7.37 | -2.53 BEND | -11.9 runaway | 0.574 |
| 1.0 [1,20]  | +6.00 | -2.62 BEND | -7.53 runaway | 0.332 |
| 2.0 [1,5]   | +5.00 | -3.92 BEND | -5.07 runaway | 0.484 |

Every stable GH case: **sigma4 < 0 (BEND), sigma6 < 0 (unbounded), CS ratio well below the ceiling 1.**

**Steelman the kill (sigma6 floor):** sigma6 > 0 needs `I2^2 > I3 c_chi^2`. By Cauchy–Schwarz
`I2^2 <= I1 I3`, with equality only for a delta-like sharp mode. I confirmed numerically that as a
bath peak narrows, `I2^2/(I1 I3) → 1` (width 2.0 → 0.013; width 0.02 → 0.99998). The monotone GH
coth continuum sits at 0.33–0.63, far below the ceiling, so **sigma6 < 0 — the fold is unbounded,
not a controlled roton minimum.** A +k^6 floor requires a SHARP spectral peak the featureless GH
bath lacks. This reproduces the route's structural caveat independently.

**Steelman the fold:** I could NOT find an admissible bare-GH coupling that delivers a controlled
bounded edge-pinned fold. The fold location `k*^2 ~ |sigma4|/sigma6` is a bath moment ratio,
cutoff-controlled and untied to the sonic edge `b→c_chi`. Both the +k^6 floor and the
edge-coincidence require an internal-scale / sharp-peaked response (e.g. a horizon QNM resonance)
that the smooth thermal continuum does not carry — exactly the route's "next calc."

---

## (4) REGRADE — CONFIRMED. Verdict stands: FOLD-POSSIBLE-COUPLING-DEPENDENT.

The route's verdict is reproduced by independent methods and survives maximum hostility:

- **sigma4 SIGN (negative-bending): FORCED, not cherry-picked.** Reproduced by (a) exact numeric
  secular root, (b) correct w2-variable KK reconstruction, (c) the route's moment rule — all agree.
  Robust across the entire admissible shift-symmetric coupling family and on the actual GH coth
  bath. The route did NOT assume the bending it wanted; the bend is the generic level-repulsion
  sign of integrating out any gapped passive bath, forced by the IR khronon sitting below the band.
- **The route did NOT bury the kill-confirming sign.** Its Block 2 stiffen result was a genuine
  wrong-variable/wrong-sign KK error; the properly done KK bends. Honest internal overrule.
- **The STRUCTURE (sigma6 floor + edge-pinning) is genuinely NOT supplied** by the featureless GH
  continuum: sigma6 < 0 (unbounded) confirmed via Cauchy–Schwarz and exact GH cases; the fold is
  not edge-pinned. This is the honest both-ways brake that keeps it from FOLD-GENERATED.

**Why NOT FOLD-GENERATED:** the bare Gibbons-Hawking spectrum supplies the bend SIGN but neither
the +k^6 stabilizer nor the edge-coincidence — the induced fold is unbounded and free-floating.
A controlled Airy fold remains contingent on an unbanked internal-scale (peaked/QNM) input.

**Why NOT CONVEX-NO-FOLD:** the bend sign is real and forced; the dS bath genuinely pushes in the
roton direction. MM/NN's free-convex kill does NOT survive on the sign axis — the active pump does
bend. The kill is downgraded to "structure not yet supplied," not "no bend."

**sign_robust:** YES — the sigma4<0 sign is robust to model (single-mode/multi-mode/broadband/GH-coth),
coupling (all shift-symmetric vertices), and regularization (cutoff-independent in sign). NOT
cherry-picked. The route did not assume the bending it wanted.

**REGRADE: CONFIRMED. Regraded verdict: FOLD-POSSIBLE-COUPLING-DEPENDENT.**
