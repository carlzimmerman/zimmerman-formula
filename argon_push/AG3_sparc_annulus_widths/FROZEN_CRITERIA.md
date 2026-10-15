# AG3 — SPARC phantom-annulus widths vs the AG1 ladders · FROZEN CRITERIA (pre-registered, 2026-10-15)

**Lane:** `argon_push/AG3_sparc_annulus_widths/` (argon track; sibling to AG1 =
`argon_push/AG1_g081_mode_adjudication/`, landed 77036c1ff).

**Question (AG1's queued observational kill test).** AG1 showed: a CONSERVATIVE isothermal
A/r² phantom annulus [r_in, r_out] is unstable on ~Myr timescales once its width exceeds
the BC ladders (DF-binding first rung w₁ = e^{(π−atan(√7/5))/ν₀} = 7.4403; DD/FF
e^{2π/√7} = 10.7491; ν₀ = √7/2), and stable below. Observed law-obeying galaxies persist
Gyr. So: how wide are the phantom annuli that REAL galaxies settle into? Two
pre-registered branches — either answer is a result:

- **S (survives):** the A/r² annuli are narrow (median w < 7.44) ⇒ the conservative
  reading is NOT falsified at observed scales; AG1's stability requirement is met by the
  data-implied inner cutoff; no dissipation needed for the outer annulus.
- **F (falsified at observed scales):** median w > 7.44 or a large tail above it ⇒
  wide settled annuli exist ⇒ the settling channel MUST be dissipative (S3) or the medium
  is not conservative-isothermal (AG2 tether analysis becomes load-bearing).

## Law algebra (zero-import, derived BEFORE touching the data)

The framework law line: g² − ḡ² = a₀ḡ (g = g_obs, ḡ = Newtonian baryonic). Phantom
acceleration g_ph ≡ g − ḡ = a₀ḡ/(g+ḡ). The A/r² medium reading demands g_ph = C/r with
C = √(a₀GM_b) (= 4πGA, the AG1/GF2 closure identity). With u ≡ ḡ/a₀ = (r_M/r)²,
r_M ≡ √(GM_b/a₀):

    r·g_ph/C = 1/(√(u+1) + √u)

⇒ the A/r² reading holds within a factor f ≥ 1 of C **iff** u ≤ ((f²−1)/(2f))², i.e.

    r ≥ r_lo(f) = r_M · 2f/(f²−1)      [f=2: r_lo = (4/3)·r_M EXACTLY]

and it can never hold inward of that on any law-obeying curve. At G081's static-ball cap
r = 0.62·r_M (u = 2.60): r·g_ph/C = 1/(√3.6+√2.6) = 0.285 — while the pure static-ball
reading (phantom A/r² filling (0, 0.62 r_M]) demands ≈ 1. **This is a sharp, pre-registered
DISCRIMINATOR between the two settled-state readings inside the cap.**

## Data and pipeline (precedent-frozen: G071/G044 corpus conventions, no new choices)

- Source: `glm53_push/data/rotation_curve_corpus_v7.json`, survey == SPARC (175).
- Per point: v_b² = sign(Vgas)·Vgas² + m2l_disk·(Vdisk² + Vbul²)  [G071 convention];
  g_obs = Vobs²/R, ḡ = v_b²/R, g_ph = g_obs − ḡ. Points with Vobs ≤ 0, errV ≥ Vobs, or
  v_b² ≤ 0 are dropped (counts recorded).
- M_b = max over valid points of R·v_b²/G (outermost enclosed baryonic mass — an
  UNDERESTIMATE if the curve truncates outside the baryons; bias direction recorded:
  smaller M_b ⇒ smaller r_lo ⇒ LARGER w ⇒ biases toward branch F. A verdict of S is
  therefore robust against this bias; a verdict of F carries it as a caveat).
- r_M = √(GM_b/a₀); C = √(a₀GM_b); a₀ = 9.3619e-11 m/s² read at runtime from
  deepseek_push/G081_results.json (robustness: a₀_alt = 1.1279e-10, G071's alternative
  footing — decision must not flip; if it does, CONDITIONAL and loud).
- Annulus extraction (primary band f=2): ρ(r) ≡ r·g_ph/C. Eligible run = maximal
  contiguous run of valid points (ascending R) with ρ ≥ 1/2, containing ≥ 2 points, and
  ending at the outermost or second-outermost valid point (pre-registered edge-noise
  allowance). r_lo = run start, r_hi = run end, w = r_hi/r_lo. Galaxies with no eligible
  run are excluded and counted (not silently dropped).
- Sample gates (pre-registered): n_points ≥ 6 after cleaning. PRIMARY = all surviving
  SPARC; ROBUSTNESS = the G071 isolated/low-EFE subset (env table
  `real_research/data/sparc_a0_environment_table.csv`, name match). Decision on PRIMARY;
  flip under robustness ⇒ CONDITIONAL.

## Checks and decision rules (frozen)

- **K1 pipeline sanity:** per-galaxy law diagnostic — rms of log10[(g²−ḡ²)/(a₀ḡ)] over
  valid points (should sit near the registered ~0.15 dex benchmark; reported, not gated).
- **K2 r_lo cross-check:** measured r_lo vs (4/3)r_M: median of ln(r_lo/((4/3)r_M)) and
  IQR. PASS iff |median| < 0.4 (factor ~1.5) — the run-start must track the law-algebra
  prediction; a gross mismatch means the band operationalization is measuring noise.
- **K3 width distribution (THE decision):** median w, IQR, frac(w > 7.4403),
  frac(w > 10.7491). Verdict S iff median < 7.4403 AND frac(>7.4403) ≤ 0.10.
  Verdict F iff median > 7.4403 OR frac(>7.4403) > 0.30. Else AMBIGUOUS (reported as is).
- **K4 interior discriminator (pre-registered, separate statement):**
  X_ball ≡ median over all galaxies of median{ρ(r) at valid r ≤ 0.62·r_M}.
  X_ball ≥ 0.8 ⇒ static-ball reading realized inside the cap; X_ball ≤ 0.4 ⇒ law-haze
  reading realized (g_ph ≈ a₀/2, phantom NOT A/r² inside the cap) ⇒ G081's violently
  unstable conservative A/r² ball was never the galactic interior state, and GF2's P1
  static-branch acceptance is re-scoped to the outer annulus. 0.4 < X_ball < 0.8 ⇒
  AMBIGUOUS. No gating — a measurement with frozen interpretation bands.
- **K5 band robustness:** verdicts recomputed at f ∈ {√2, 2, 3}: K3 branch must not flip
  across f (else CONDITIONAL, loud).
- **Part B (EXPLORATORY, non-gated, declared at freeze):** the observed outer annulus
  carries baryonic gravity too: at r ≥ (4/3)r_M the baryon/phantom force ratio is
  GM_b/(C r) = r_M/r ∈ [0.33, 0.75] — NOT negligible, so AG1's phantom-only threshold is
  an idealization. B1: report that ratio distribution. B2: for each galaxy solve the
  lowest eigenvalue of the GENERAL AG1/EB q-ODE (σ²q″ + (Φ₀′ − 2σ²/r)q′ + (4πGρ₀ + ω²)q
  = 0) with ρ₀ = A/r², Φ₀′ = GM_b/r² + C/r on [r_lo, r_hi], σ²(r) = (GM_b/r + C)/2
  (local-hydrostatic choice — documented deviation from the closure σ² = C/2, forced by
  the baryon term), D-BC at r_lo, F-BC (δP_L = 0) at r_hi. Report the fraction with
  Λ₀ < 0. No verdict attached; feeds AG2/G111.

## Mutations (must behave as designed; MUTATE=1)

- **M1:** shuffle M_b across galaxies (seed 20261015): K2 median |ln(r_lo/((4/3)r_M))|
  must degrade (> 0.4) — pipeline is sensitive to the mass scale.
- **M2:** run the band test on the BARYONIC product r·ḡ/C instead of r·g_ph/C: eligible
  runs must be structurally different (≥ 50% of galaxies flip eligibility or r_lo shifts
  by > ×1.5 at the median) — the test discriminates the phantom signal, not generic
  curve shape.
- **M3:** swap roles (ḡ ↔ g_obs in g_ph): g_ph ≤ 0 identically ⇒ zero eligible runs
  (pipeline must report empty, not manufacture runs).

## Kill conditions of THIS lane's conclusion

- A law-obeying galaxy population with eligible-run widths median > 7.44 and Gyr-stable
  kinematics would falsify branch S's conservative reading (that IS branch F).
- If a future re-analysis with a defensible alternative band (f ≠ 2) flips the K3 branch,
  the CONDITIONAL machinery above fires — the lane's verdict is band-robust or loud.
- If X_ball ≥ 0.8 (static ball realized inside the cap), AG1's ball instability says
  those interiors collapse in ≲ 33 Myr — contradicted by the settled curves themselves;
  that tension would land on the tether medium (AG2) as a hard constraint, not on AG1.

**Outputs:** `ag3_sparc_widths.py/.out/_results.json` (+ MUTATE .out/_results.json),
IDEA.md, README.md, handoff addendum. Numbers: a₀ from G081_results.json (runtime);
thresholds 7.4403/10.7491 and (4/3)r_M are AG1/law closed forms; f-band, edge allowance,
sample gates, and interpretation bands above are the ONLY choices — all frozen here,
before any data touched.
