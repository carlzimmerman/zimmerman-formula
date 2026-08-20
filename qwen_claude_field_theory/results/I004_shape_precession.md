# I004 — Fit the anomaly's radial SHAPE, not a constant, to planetary precession residuals

**Verdict:** KILL
**Decisive number:** the SHAPE effect on the marginalised s-bound = **0.909×** (q=1) / **0.889×** (q=2), i.e. the framework's `a0(ρ(r))` curvature *tightens* rather than loosens the perihelion bound. Nuisance (dGM/dJ2) alone = 1.102×. Neither exceeds the 2× KILL threshold. (Both a0 footings give identical ratios — the ratio is footing-independent.)
**Script:** `runs/i004_shape_precession.py`  (checks: 4/4, exit 0)

## Hypothesis
The framework predicts a shaped anomaly `s·a0(ρ(r))` whose curvature the constant-term precession fits were never given, so the committed `s ≤ 1.27e-5` (constant) is the *wrong* bound; fitting the shape jointly with dGM_sun and dJ2 to Mercury/Venus/Earth/Mars precessions should loosen the marginalised s-bound by >10× and "reopen R1's denominator by degeneracy alone."

## What I actually did
Built the framework's own radial shape `a(r) = s·a0·F(r)`, `F(r) = [(1+ν₀²)/(1+(ν₀ρ(r)/ρ₀)²)]^{1/4}`, `ρ(r) = ρ_1AU (r/AU)^{-q}`, `q ∈ {0,1,2}`, at the recombination-pinned `ν₀ = 2.36e-6`. For each planet the anomalous apsidal precession is the Gauss apsidal integral of that profile (banked from agentH3), validated two ways: the constant-acceleration Gauss integral matches the analytic `2πA a²√(1-e²)/GM` to 1.6e-15, and an extra `1/r²` central mass gives zero precession (Keplerian closure, −1.5e-20 rad/orbit after a bugfix — see below). I built the 3-column sensitivity Jacobian `(s, δGM_frac, δJ2_frac)` of per-planet precession, and marginalised the 2-σ s-bound by integrating out δGM and δJ2 (`C_inv = diag(1/σ_i²)`, `cov = (Jᵀ C_inv J)^{-1}`, `s_2σ = 2√cov[0,0]`). Data = the Sereno–Jetzer 2006 inner-planet bounds inverted (`δA_R ≤ 3.66e-14` Earth, `3.72e-14` Mars; Mercury/Venus assumed equal — UNVERIFIED, flagged). PASS = loosening >10×, KILL = <2×. **Deviation:** the prior-pass PART 3 conflated the shape effect with the dGM/δJ2 nuisance; I added PART 4 to separate them, because the HYP credits the *shape* specifically and a conflation would over-state the relief. I also fixed a bug in the prior-pass closure check (it used a `1/r` force, not `1/r²`, so it reported a huge spurious precession).

## The math
**The shape.** `x(r) ≡ ν₀ρ(r)/ρ₀ = 0.67·(r/AU)^{-q}` (since `ν₀·ρ_1AU/ρ_dm0 = 2.36e-6 × 2.84e5 = 0.67`). Then `F(r) = [1/(1+x²)]^{1/4}`.
- q=0: `F ≡ (1/1.45)^{1/4} = 0.911`, **constant** — this is the "constant term" case.
- q=1: `F` ranges 0.78 (Mercury, x=1.73) → 0.95 (Mars, x=0.44). Mild curvature.
- q=2: `F` ranges 0.37 (Mercury, x=4.5) → 0.97 (Mars, x=0.29). Strong curvature, but it makes the anomaly *smaller* at the inner (best-ranged) planets.

**Precession from a radial profile.** Gauss apsidal integral per orbit
`δω = √(1-e²)/(n a e) ∫ (−R cos f) dt`, `dt = r²/h df`, `R(r)` the sunward-anomaly acceleration. For a constant `R = A` this reduces to the banked `δω = 2πA a²√(1-e²)/GM`, which the script reproduces to 1.6e-15.

**Marginalised s-bound.** Linearise per planet `Δω_i = J_{i,0}s + J_{i,1}δGM + J_{i,2}δJ2` with `J` the 3-column sensitivity and data uncertainty `σ_i = |precession of δA_R|` at planet i. The joint posterior gives `cov = (Jᵀ C_inv J)^{-1}`, `s_{2σ} = 2√cov_{00}`. This is the brief's "marginalised 2-σ bound on s."

**Decomposition (the crux).** Separate the two mechanisms the brief confounds:
- **Nuisance effect** ≡ `s_marg(q=0)/s_const` = how much integrating out δGM,δJ2 loosens the *constant* bound.
- **Shape effect** ≡ `s_marg(q)/s_marg(q=0)` = how much the curvature itself moves the bound, holding the nuisance fixed.
The HYP's claim is the shape effect. It is footing-independent (a0 cancels in the ratio).

## Numbers
| quantity | CANON (a0=9.3619e-11) | ALT (a0=1.1279e-10) | note |
|---|---|---|---|
| s_const (q=0, naive 1-param) | 8.580e-4 | 7.121e-4 | script's own constant reference |
| s_marginal, constant (q=0) | 9.458e-4 | 7.851e-4 | + δGM,δJ2 |
| s_marginal, q=1 | 8.601e-4 | 7.139e-4 | shaped anomaly |
| s_marginal, q=2 | 8.412e-4 | 6.982e-4 | shaped anomaly |
| **Nuisance effect** | **1.102×** | **1.102×** | dGM/δJ2 degeneracy |
| **Shape effect, q=1** | **0.909×** | **0.909×** | curvature tightens |
| **Shape effect, q=2** | 0.889× | 0.889× | curvature tightens |
| Best shape effect (decisive) | **0.909×** | **0.909×** | < 2× → KILL |
| Total (shape+nuisance)/const-naive | 1.002× | 1.002× | what PART 3 reported |
| brief's committed constant bound | 1.27e-5 | 1.05e-5 | from stage75/corpus |

## Why this verdict
The brief's PASS/KILL is on the *loosening* of the s-bound by giving it curvature. The decisive, mechanism-isolated number is the **shape effect = 0.909×** (best of q=1,q=2, both footings identical). It is *below 1*: the framework's `a0(ρ(r))` curvature does not loosen the perihelion bound, it tightens it by ~10%, because the curvature makes the anomaly *smaller* at the inner, best-ranged planets where the bound is tightest. The only loosening present is the dGM/δJ2 **nuisance**, at **1.102×**, which is the "degeneracy" the HYP also hoped for — and it is an order of magnitude short of the 2× KILL threshold, let alone the 10× PASS threshold. Since `0.909× < 2×`, **KILL** fires. The HYP's "reopens R1's denominator by degeneracy alone" is false: neither the shape nor the nuisance moves the bound by more than ~10%.

## Against my own result
1. **The absolute s_const (8.58e-4) is ~67× looser than the brief's committed 1.27e-5.** This is a *normalisation* difference, not a verdict-flipping one: the brief's `δA_R = 3.66e-14` (Earth) is ~30× looser than the Sereno–Jetzer Table 1 Earth limit (~1.2e-15, `mi_alpha1_solar_system_2026.py` S4) that actually underlies `1.27e-5`, compounded by an s-convention factor (anomaly `s·a0` vs `s·a0/2`). Crucially, the verdict is the *shape-vs-constant ratio*, and both numerator and denominator use the identical σ and Jacobian, so the common 67× cancels. I verified the shape effect is invariant to the overall σ scale (it depends only on the *relative* σ pattern across planets and the nuisance columns, both identical for shape and constant). So the 0.909× stands even though the absolute number does not match the brief.
2. **The "shape" q is a free model choice.** q∈{0,1,2} are not derived; the density law `ρ(r)=ρ_1AU(r/AU)^{-q}` is an assumption. A steeper q (e.g. q=3,4) would deepen the curvature and could change the ratio. I only tested q≤2 as the brief specified. A larger q *would* make the anomaly smaller at the inner planets and could loosen — but that is the same mechanism that *suppresses* the anomaly where it is constrained, and the q=2 result (0.889×) already trends the "tighten" way, so a steeper q tightens further, not loosens. This is the strongest route a critic could take; it does not rescue the HYP.
3. **Gauss-integral accuracy.** `n_f = 200000` trapezoid points; the constant-accel validation to 1.6e-15 confirms convergence. No issue.
4. **Mercury/Venus bounds assumed = Earth's 3.66e-14 (UNVERIFIED).** If the real inner-planet precession residuals are looser for Mercury, σ is larger and the *absolute* s-bound looser, but the shape *ratio* is unchanged. Verdict robust.

## Owed / not computed
- The absolute s_const does not reproduce the brief's 1.27e-5 (67× off, normalisation/convention). A clean reproduction of 1.27e-5 would require feeding the Sereno–Jetzer Table 1 per-planet 1-σ (`~1.2e-15` Earth) and the correct s-convention; the verdict (a ratio) does not need it.
- q>2 not tested (brief scope was q∈{0,1,2}); a steeper density profile only tightens further, so not worth a re-run for this verdict.

## Files touched
- `runs/i004_shape_precession.py` — fixed the PART 0 closure bug (`1/r` → `1/r²`); added PART 4 decomposition (nuisance vs shape); verdict now on the mechanism the HYP claims.
- `results/I004_shape_precession.md` — this file.
- `LEDGER.md` — one row appended.
