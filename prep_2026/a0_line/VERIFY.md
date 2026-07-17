# VERIFY — Adversarial verification of the a0-line lane (2026-07-16)

Independent verifier. All six lane scripts re-run from scratch (`identity_uniqueness.py`,
`estimator_theory.py`, `bayes_setup.py`, `fire_slope.py`, `fire_linearity.py`,
`fire_lambda.py`, `fire_occam.py`): **all exit 0** and reproduce every headline number in
`DERIVATION.md` / `FIRE_RESULTS.md` / the `*_results.json` files (GLS gas slope 1.181e-10,
sigma 0.190e-10, 71% degeneracy kill, shape chi2 1860.4/1858.8/1867.5, B01 +0.60/+1.04
bans, Lambda 1.737e-52 at +1.45 sigma, bias demo 4.15e-11). No hard-coded checks found:
every assert is a live sympy simplification or a computed numeric comparison (the one
weak `or ... in (True, None)` assert in `identity_uniqueness.py` L92 is backed by a real
numeric positivity check on the next line). The closed-form B01, the footing likelihood
ratio (0.44 bans), and the Lambda inversion were additionally re-derived by hand and
match to the printed precision.

Independent machinery (own parser, own cuts, own estimators, own sympy solves) is in
`verify_independent.py` (exit 0; run it — nothing below is asserted from memory).

## Per-piece verdicts

### 1. Identity + uniqueness — **UPHELD**
Solved the functional equation independently, one generalization further: demanding an
*affine* excess y^2(nu^2-1) = alpha·y + beta gives nu^2 = 1 + alpha/y + beta/y^2; the
beta term is a nonzero floor g_obs^2 -> beta·a0^2 as g_bar->0, so "through the origin"
is forced by g_obs->0, and the surviving family sqrt(1+alpha/y) is pure a0-rescaling with
the deep-MOND normalization forcing alpha=1. **nu = sqrt(1+1/y) is the unique exactly
linear-excess interpolation, as claimed** — and, as the lane itself states, the claim is
definitionally tight: "excess exactly linear through origin" *is* the law restated.
Rival non-linearity confirmed by an independent route (d²E/dg² != 0 for McGaugh-nu).
SPARC census reproduced exactly: 153 gals / 3166 pts, 379 gas-dom (all at y<1),
N(y>30)=47, N(y>50)=16, N(y>100)=1.

**Conflation-trap check (one cosmetic finding):** the "x100 at y~100" separation is a
*matched-scale* number. At the rival's OWN conventions the same physical point
(g_bar = 100·a0_canon) gives R = 44 (g_dagger = 1.2e-10) and R = 11 (at McGaugh-nu's
SPARC-profiled optimum 1.95e-10). The superexponential tail *death* — the load-bearing
statement — survives any g_dagger, and all quantitative tests profile each rival's scale
separately (no conflation where it matters); the identity script flags the offset
("less than one row"). Cosmetic overstatement in the x100 slogan only, immaterial since
the tail is data-starved anyway.

### 2. Gas-dominated slope (E1) — **UPHELD, with one sub-claim sharpened**
Re-derived with independent code: own parser, three cuts (their point-level
g_gas > g_star; a stricter f_gas > 0.8; a galaxy-level median-f_gas > 0.5) and three
estimators none of which is their GLS (banked-P1-style log-space profile fit restricted
to the gas points; per-point median of E/g; per-galaxy median-of-medians). Results at
Ud = 0.70 on their cut: **0.93 / 0.97 / 0.92 e-10** — i.e. my independent estimators
side with the lane's *median* variant (0.973e-10), not with the GLS primary (1.181e-10).
Stricter cut f_gas>0.8 goes lower still (0.78–0.86e-10 at Ud 0.7–0.8, small N).
Upsilon swings 15–29% across my cuts — **the 71% degeneracy kill is confirmed**
(independent swing 19–29% vs 55–69% full-sample).

Distance propagation re-derived independently (numeric + scaling): **g_bar ~ D^0 exactly
for gas AND stars, g_obs ~ 1/D — confirmed**; the lane's correction of its own
prospectus hint is right, and the per-point sensitivity -2a0(y+1) matches the data.

Sharpened caveat: the claim "a0 boxed to (1.13–1.36)e-10 regardless of M/L" is
**GLS-conditional**. Across estimator AND cut freedom the honest box is more like
(0.84–1.36)e-10; the quoted sigma_tot = 16% (which charges half the GLS–median spread)
nominally covers this, but the central value is estimator-owned, exactly as the lane's
own biggest budget line admits. Consequence, stated harder than the lane states it: the
"mild ~1-sigma lean toward ALT on the primary estimator" is an artifact of *choosing*
GLS as primary — the independent estimators lean canonical (+0.1 to −0.1 sigma from
9.355e-11). The footing fork is not merely "not decided"; **there is no usable lean in
either direction**. (The lane's tables do contain both leans and refuse the decision, so
nothing was hidden; only the word "primary" carries unearned weight.)

### 3. Linearity / high-g tail — **UPHELD**
The "undecided at <~1 sigma" tail verdict survives the adversarial stress it had not yet
been given: varying Upsilon_bulge ±30% (Ub/Ud = 0.98–1.82) and the intrinsic floor
x0.5–x1.6, the y>30 tail dchi2(McG−fw) ranges **−2.3 to +2.2 and flips sign** within the
stress range; the y>30 points are ~96% bulge/star-dominated (mean stellar share 0.96),
confirming the banked wall's "the tail rides on the points where M/L errors are
largest". Fixed-Ud global dchi2 (fw beats McG by ~7–99 depending on Ub and floor) vs
Ud-profiled wash reproduces the lane's disclosed Upsilon-dependence. Not a discriminator
today; neither a manufactured null (the wash comes from legitimate Upsilon profiling,
and the log-det/common-covariance bracket ±28 is reported) nor a suppressed win.

### 4. Lambda inversion (E2) — **UPHELD**
Algebra re-derived by hand (Lambda = 3Z²a0²/c⁴; 1.737e-52 GLS / 1.177e-52 median vs
Planck 1.089e-52; sigma_lnLambda = 2·0.161 = 0.322; +1.45/+0.24 sigma). Correctly
presented as the banked a0 ~ cH_Lambda/Z coincidence *reframed* — same information,
sharper falsification target — with the canonical-footing scope stated and the ALT
footing not blurred into it. Note both directions: on my independent estimators the
median-variant row (+0.24 sigma, ratio 1.08) is the better-supported one, which makes
the Lambda agreement *better* than the GLS headline, not worse.

### 5. Occam factor (E3) — **UPHELD, envelope floor noted**
Independent quadrature reproduces +0.60/+1.04 bans. Prior-rigging attack: the default
2-decade prior is **not rigged upward** — wider priors help M0 more (+0.90/+1.34 at 4
decades), so the default is mid-envelope, and the reported sensitivity list is honest.
The true adversarial floor is lower than the quoted envelope, though: a
"Milgrom-1983-informed" prior [0.6, 2.4]e-10 gives **+0.08 (canon) / +0.52 (ALT)** and a
hostile half-decade prior +0.00/+0.44 — i.e. a skeptic who conditions the prior on the
MOND literature (which is partly question-begging, since that literature is the same
kind of data) can drive the canonical bans to ~0 but not negative. "Positive but modest,
capped by systematics" is exactly right; the two-sided error-reduction lever (canonical
→ −2.45 bans if the GLS central value holds at x3 smaller error) is correctly stated
and is a genuine falsification exposure, not a win-forecast.

### 6. The information question (the core) — **UPHELD**
- **Full sample: REPACKAGED.** Banked P1 profile a0_best 1.761/1.359/1.095/0.883e-10 vs
  line-GLS 1.891/1.526/1.279/1.101e-10 over Ud 0.5→0.8: same ridge, same ~55–69%
  fractional spread, values offset +8–17% by metric choice (E-space GLS vs log scatter).
  The full-sample a0-line adds an estimator and elegance, zero information — exactly
  what the lane's own ledger says.
- **Gas subsample: genuinely new within this ledger.** Banked band [0.776, 2.005]e-10 is
  1.37 bits wide (log); the gas Upsilon-interval [1.13, 1.36]e-10 is 0.27 bits — ~1.1
  bits removed in the log metric, ~x3.8 in linear width. (The lane's "~2.6 bits" uses
  the linear-interval metric loosely; the shrinkage itself is real either way.) With
  estimator freedom added the box widens to ~(0.84–1.36)e-10 — still a real kill of the
  Upsilon direction, now systematics/estimator-owned instead. Historical scope note:
  gas-dominated galaxies as M/L-insensitive a0 probes are standard since McGaugh 2011;
  "new" here means new relative to this repo's banked walls, not new to the literature.
- **Tail shape: <~1 sigma today** (verified under harder stress than the lane applied).
- **Occam/Lambda: formalizations, no new data** — and both scripts say so themselves.

### 7. Honesty rails / manufactured-verdict hunt — **CLEAN, both directions**
- Hunted a manufactured *confirmation*: the GLS-primary choice is the one lever that
  pushes the result toward ALT/RAR-fit values; independent estimators pull back toward
  canonical. Since the lane prints both, charges the spread, and refuses the footing
  call, this is a disclosed sensitivity, not a manufactured win. The Lambda "52 orders
  of magnitude" rhetoric is flagged in-text as a reframed coincidence.
- Hunted a manufactured *null*: the shape-test wash could have been engineered via the
  f_int = 0.64 floor + Upsilon profiling; stress tests show the wash is the honest
  Ud-profiled answer (fixed-Ud wins for fw are reported, the invalid −147 cross-Ud
  statistic was correctly quarantined, the log-det bracket is symmetric). Not
  manufactured.
- The three in-script artifact diagnoses (weight-noise x3 bias, cross-Ud covariance,
  the corrected "+1.5–2 bans" forecast) check out; the bias demo reproduces (4.15e-11).
  One narrative nit: an early draft's "3.3e-11" for the bias demo appears in the lane's
  hand-off summary; the committed scripts/outputs consistently say 4.15e-11/"x3".
- Banned word: the string "proof" occurs **only in negations/disclaimers** ("not a
  proof", "no 'proof' language") in docstrings and the two .md headers; no affirmative
  proof-claim anywhere in code, output, or JSON. Pedantic nit: FIRE_RESULTS.md L81 says
  "the word proof appears nowhere" while its own L3 uses it in a negation.
- Frozen repo untouched (all reads; outputs confined to prep_2026/a0_line/). Both
  footings carried in every table I checked. "Not a TOE", "no rival kill", "no footing
  resolution" all present.

## Bottom line
**UPHELD overall.** Every load-bearing claim reproduces and survives independent
re-derivation and adversarial stress; the lane's honest bottom line ("beautiful
reframing; full sample as degenerate as the RAR; the gas cut kills ~71% of the Upsilon
degeneracy; tail <~1 sigma; Occam +0.6–1.0 bans modest") is exactly what independent
code finds. Two sub-claims are sharpened, not refuted: (i) the gas box
"(1.13–1.36)e-10 regardless of M/L" and the "mild lean toward ALT" are
GLS-estimator-conditional — independent estimators land at 0.92–0.97e-10 (leaning
canonical), so the correct statement is *no usable footing lean at all*; (ii) the Occam
envelope floor under literature-informed (question-begging) priors is ~0.0 bans
canonical, slightly below the quoted +0.30 floor. One cosmetic finding: the "x100 at
y~100" separation is matched-scale; at the rival's own scale it is x10–x45 (the tail
death itself survives any scale, and no quantitative test conflates conventions).
Nothing flips a verdict; the banked wall (RAR non-diagnostic of a0's exact value)
stands untouched, exactly as the deliverable says.
