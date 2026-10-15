# HANDOFF TO CONDUCTOR — from AG3 (argon interactive session, 2026-10-15)

Lane: `argon_push/AG3_sparc_annulus_widths/` — LANDED (K3 verdict **S**, stable under
all pre-registered robustness cuts; K2b FAILED its frozen tolerance and is kept failed
on record ⇒ lane marked CONDITIONAL-on-record with a quantitative explanation; M1–M3
as designed). Register rows below are PROPOSALS per LOOP_CONDUCTOR §2.9; this session
touched only `argon_push/`.

## Proposed register rows

1. **AG1 observational kill test — RESOLVED (branch S).** Measured A/r² phantom-annulus
   widths in SPARC (exact law identity ρ = √(M(r)/M_b)/(√(u+1)+√u), zero-import; corpus
   v7 / G071 conventions): median w = 1.843 [1.403–3.180], n = 78 eligible of 165
   cleaned; frac > w₁(DF) = 7.4403: 0.038; frac > w₁(DD) = 10.7491: 0. Robust:
   censored-excluded / isolated-subset / f∈{√2,3} / a₀_alt all give S (medians
   1.76–2.75). Conservative-fluid stability is NOT falsified at observed scales; the
   data-implied inner cutoff sits ~16× above AG1's r_crit = 0.083·r_M. Baryon-inclusive
   eigen-solve (general q-ODE, drift −GM_b/(2r²), symbolic assembly): 0/78 unstable,
   median ω₀²/(C/r_lo²) = +3.43. Verification: ag3_sparc_widths{,_MUTATE}_results.json.
2. **Static A/r² ball excluded as the realized galactic interior state (K4).**
   X_ball = median ρ(r ≤ 0.62·r_M) = 0.0025 over 128 galaxies vs static-ball
   prediction 1; >>10× every statistical (σ_ρ = 0.059) and systematic (20%-Υ proxy
   0.167) scale. GF2's static ball remains valid as the κ=½ CLOSURE DEVICE (algebra
   untouched) but is not the settled interior state of real galaxies; the realized
   structure is haze-interior + narrow outer A/r² annulus. Haze-vs-Newtonian interior
   NOT decidable at SPARC precision.
3. **Named follow-up candidates:** UGC 06787 (w=8.98), UGC 02953 (w=8.67), UGC 09133
   (w=7.63) — the three eligible galaxies above the DF rung. If the conservative reading
   holds with negligible dissipation, these should show non-settled/disturbed phantom
   kinematics. AG3b (spawn proposal): targeted disturbance check on exactly these three
   (non-circular motions, interaction signatures — literature + any on-disk H I data);
   pre-registered: pristine-and-settled would falsify branch S for those systems.
4. **Framework-facing flag (non-gated): law-line interior residual.** The quadratic
   law's interior prediction g_ph → a₀/2 is not visible in SPARC interiors (X_ball ≈ 0);
   the deficit is within Υ systematics, so this is NOT a law falsification — but a
   G071-followup re-audit of inner-point residuals (per-galaxy Υ vs law-interpolation
   degeneracy) is proposed as an evidence re-audit on a named pain point.
5. **Calibration lesson (process):** frozen tolerances for DIFFERENCE-quantity checks
   must be calibrated against the law's registered precision propagated through the
   estimator (here: 0.15 dex velocity-space ⇒ ~0.33+ in r_lo crossing space), not
   against exactness. K2b's 0.15 tolerance was miscalibrated pre-run; kept FAILED per
   discipline; post-hoc K2d/band-scatter analysis attached in-lane.

## Spawn proposals still open

- **AG2 — tether-medium mode analysis** (unchanged from AG1's handoff): does W_rem +
  stiffness change the corrected ladders? AG3's B2 (baryon-inclusive) already shows the
  baryon drift term STABILIZES (0/78 unstable) — AG2's stiffness question is the
  remaining medium-physics gap.
- **AG3b — the three named candidates** (row 3).
- **AG1-L — Lean certification** of AG1's exact identities (unchanged).

## CROSS-TRACK FLAG (added post-commit of main results; sibling ARGON07 ab94d5171)

**RESOLVED 2026-10-15 (same day, post-flag investigation — see RESOLUTION below; the
original flag text is kept unedited per append-only style).**

**Settled-halo inner edge: ARGON02/ARGON07 model vs AG3 rotation-curve measurement.**
ARGON07's commit states the settled halo: M_c = 5.364·M_b within 5.84·r_M, locked
amplitude g_ph = √(G M_b a₀)/r = C/r (ARGON02 ESD: ΔΣ → √(GM_b a₀)/(4GR), break
5.84 r_M). Under the A/r² shell reading, M_c/M_b = 5.84 − r_in/r_M ⇒ **r_in = 0.476
r_M**. But AG3's measurement: X_ball = median ρ(r ≤ 0.62 r_M) = **0.0025** (128
galaxies) excludes locked amplitude (ρ = 1) inside 0.62 r_M at >10× every statistical
and systematic scale; the ρ ≥ 1/2 band starts at median ~1.6 r_M (K2c offset +0.17 over
(4/3)r_M). **If the ARGON02 halo model extends locked amplitude down to 0.476 r_M, it is
in tension with rotation curves across the zone 0.48–1.5 r_M.** Possible resolutions for
the conductor: (i) the ESD fit's 1/R form is an outer-regime asymptote with no inner
leverage (lensing stacks have little constraining power inside ~r_M where baryons
dominate ΔΣ) — the halo may have an inner cutoff/transition near the r_M scale; (ii) the
interior "haze" (non-A/r² phantom, g_ph ≪ C/r) projects to part of the measured ESD and
the 1/R extrapolation inward is unwarranted; (iii) a real tension to adjudicate. Note the
benign direction: an inner cutoff near ~1–1.5 r_M makes the realized A/r² annulus NARROWER
than the model shell — strictly favorable for AG1 stability (AG3's S verdict already
measures the realized widths, median 1.84). This flag does NOT reopen AG1 or AG3; it
routes a model-vs-data reconciliation to the ARGON02/07 track owner via the conductor.

## RESOLUTION of the flag (post-investigation, same session)

**1. The flag's premise was wrong; the ARGON02-vs-AG3 tension DISSOLVES.** ARGON02's
settled halo is explicitly CORED (their own P2: "exact cored transition curve, 13–54%
of r⁻¹ within r_M"): locked amplitude g_ph = C/r is the ASYMPTOTE (x ≳ 10), not the
interior. My "r_in = 0.476 r_M" was a shell-mass-equivalent misreading: M_c = 5.364 M_b
integrates the cored profile from 0 to 5.84 r_M; the 0.476 r_M mass deficit is spread
over the whole core, not a hard edge. ARGON02's canonical core amplitude over x ≤ 0.62
is ρ ∈ [0, 0.48] (median ~0.2–0.3), which AG3's X_ball = 0.0025 ± 0.003(stat) ± ~0.17
(correlated Υ systematics) cannot resolve from zero. **No contradiction between tracks.**
AG3 K4's load-bearing claim stands unchanged: ρ ≈ 1 (locked/static ball) is excluded
inside the cap; both tracks' cores survive.

**2. The investigation surfaced a sharper, real issue: the repo runs TWO law lines.**
- **Canonical (frozen):** THEORY_CANONICAL_2026-10-14 S2 line 21: g_N = g²/(g + a₀);
  PAPER49 (§line 37) numerics confirm: ν = g/g_N = 100.5 at g_N = 10⁻⁴a₀ matches
  standard-μ (x/(1+x)) to 3 digits (quadratic would give 100.005; "simple"
  x/√(1+x²) would give 100.00). ARGON02 script line 11 uses exactly this ("from
  g_N = g²/(g + a0)"). NB: S2/PAPER49 both LABEL it the "simple interpolating function
  (Famaey & Binney 2005)" — a misnomer; the algebra + numerics pin standard μ.
- **Quadratic "equipartition" a₀-line:** g² − ḡ² = a₀ḡ ⇔ ḡ = g²/(g + ḡ): the form in
  the user-profile statement of the program, G071's tested law (0.145 dex pooled,
  benchmark-validated), and AG3's K2 prediction bands. The two forms are the SAME
  expression with (g+a₀) vs (g+ḡ) in the denominator — a natural transcription trap.
- **What is NOT affected:** deep asymptote identical (g_ph → C/r; C, σ² = C/2, A/r²,
  M_b/(4πr_Mr²)) ⇒ the entire AG1/GF2/κ=½ algebraic chain, ARGON02 P1 deep-window ESD,
  and AG3's measured widths/verdict S (law-agnostic: ρ_meas is data over the shared C).
- **What IS law-form dependent:** ARGON02 P2 exact-curve ESD numbers (canonical runs
  6–27% above quadratic through their [1,5]r_M window: density ratio
  2√(1+x²)/√(1+4x²)); supply edge r_e = 5.843 r_M (canonical) vs 6.285 r_M (quadratic)
  at fixed M_c = 5.364 M_b — kill-test (b) targets shift accordingly; ρ = 1/2 crossing
  (2/3 vs 4/3)·r_M; AG3 K4 band predictions (core amplitude 2× higher in canonical).

**3. New empirical discriminator, measured today (ag3_lawform_diagnostic.py/.out,
identical 165-galaxy AG3 sample, both laws, verdict-free):** rotation data prefer the
QUADRATIC form, consistently:
- paired velocity-space rms: quadratic 0.178 dex vs canonical 0.220 dex (paired median
  difference −0.042; same sign and size in the deep subset);
- ρ = 1/2 crossings: measured/quadratic median +0.063 (consistent) vs measured/canonical
  +0.493 (1.6× outside — canonical crossings predicted far too deep);
- band-region ρ ratios: measured/quadratic −0.204 vs measured/canonical −0.466;
- stacked ρ_meas(x) tracks ~1.2× below quadratic and ~1.7–1.9× below canonical through
  x ∈ [0.1, 3]. A ~20% Υ-disk overestimation bias plausibly absorbs the quadratic gap;
  it cannot absorb the canonical gap.
This does NOT by itself overturn the frozen canonical doc (fit quality is not the
framework's arbiter — PAPER49's claim is that the law is the medium's unique rest state,
a theory-internal fact). It does mean: if standard μ stays canonical, its transition-
regime phantom over-predicts SPARC rotation by ~1.7× at the 0.2-dex level — a
kill-test-(c)-class embarrassment arriving BEFORE the lensing data; and G071's
benchmark-validated 0.145-dex result is validating the non-canonical form.

**4. Decisive route — proposed lane AG4 (theory-internal, no data needed):** derive the
static rest-state law from S2's own action (L = −|∇Φ−KP|²/(2K) − ρ_bΦ − W_rem(u) −
(γ/2)|∇P|², K W_rem′(u) = u²/(a₀−u), u = K|P|): solve the settled/tethered equilibrium
for a point baryon mass and read off which interpolation emerges. Pre-registered
readings: (a) rest state = standard μ ⇒ canonical stands; the quadratic's better SPARC
fit becomes an anomaly to explain (or weakens PAPER49's uniqueness claim); (b) rest
state = quadratic ⇒ THEORY_CANONICAL S2 line 21 + PAPER49 eq/numerics get a dated v2
erratum (never an edit), ARGON02 P2/P3 re-derive (r_e → 6.285 r_M, ESD inner bins
−6…−27%); (c) rest state = neither/both-in-limits ⇒ report as falls. Until adjudicated:
AG3 verdict S stands (law-agnostic); ARGON02 numbers stand AS canonical-form numbers
with this dependency recorded; no file outside argon_push/ touched.

## Housekeeping

- Frozen-first chain: FROZEN_CRITERIA (4560f945c) + AMENDMENT_A (7527066a6), both
  committed alone before the first data run.
- Exit codes: MAIN exit 1 (K2b frozen gate failed — honest CONDITIONAL, all other gates
  pass); MUTATE exit 1 (same shared gate + all M-checks True).
- No files outside argon_push/ modified; sibling processes untouched; G071/G081/G111/
  GF2 files read-only.
