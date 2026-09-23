# J00 — THE MOMENT CHANNEL LEDGER (RH08-STYLE)
**2026-09-23 · the authoritative register of the JWST moment-channel campaign (J01–J05), self-contained**

## Scope (shared by every entry below)
Every statement lives inside the frozen conservative Thomson-sphere transport model of
`real_research/reviews/bhstar_scattering_clock_2026_09_21/density_free/THEOREM.md` and the target
`ai_slop/research_orchestrator/JWST_EQUATION_TARGET_2026_09_22.md`: stationary sphere R = 1 (dimensionless),
central isotropic point source (or volume-uniform where stated), conservative unpolarized Thomson
scattering (E[u′|u] = 0), all photons counted, no absorption, escape at first outward crossing,
D = t_exit − r_exit·u_exit with c = 1. Model identities are **proven statements inside this model** —
not observational JWST confirmations, not new laws of nature.
Frozen-lane anchors: Theorem 1 (E[D] = ∫₀¹ rκ(r) dr, all scattering orders), Theorem 2 (lag–width band,
uniform + isothermal), Theorem 3 (|H(2π/P)| bound). Uniform τ₀ = 1 benchmark: E[D] = 1/2.
Verification census: **35/35 checks across three independent stochastic engines** (frozen `transport.py`,
J01 engine, J02 engine; exact optical-depth bisection, own geometry/seeds, no null-collision thinning)
**and both source geometries** (J01 20/20 + J02 15/15). MC numbers below carry their reported standard
errors; the identities themselves are exact (closed arguments), the numbers are evidence.

## PROVEN (closed arguments; machine-verified)

| # | line | content and evidence | falsifier |
|---|---|---|---|
| P1 | **Conditional-Gaussian lemma / even-moment hierarchy** | Conditional on the trajectory, v is Gaussian with variance exactly 2·ang, ang = Σ_j T(r_j)(1−u_j·u′_j) (per-kick Var = 2T(1−μ), kicks conditionally independent). Hence **E[D v^{2m}] = (2m−1)!!·2^m·E[D·ang^m]** for every m, every scattering order, any bounded κ ≥ 0, T > 0, central or volume source. Engine evidence (n = 10⁶): central m=1,2,3: 3.7254 vs 3.7142 (0.30%), 122.04 vs 121.57 (0.38%), 8502 vs 8762 (3.1%); volume: 2.2634 vs 2.2598 (0.16%), 68.60 vs 68.24 (0.53%), 4834 vs 4672 (3.5%); ratios 1.003/1.004/0.970 and 1.002/1.005/1.035 (m=3 spread = MC tail of v⁶, within pre-registered tolerance). m=1 at J01 n = 5×10⁵: 3.7316 vs 2E[D·ang] = 3.7237 (Δ 0.2%); q=10: 192.67 vs 192.38 (Δ 0.15%); τ₀=2,q=3,h=2: 234.16 vs 234.04 (Δ 0.05%); E[v⁴] = 12E[ang²]: 67.05 vs 67.34. | A valid model configuration whose v|trajectory is not Gaussian with variance 2·ang — i.e. an independent engine violating the m = 1 **and** m = 2 identities jointly at ≥ 3 SE (kicks conditionally independent, Maxwellian e). The identity is not hostage to the m = 3 tail. |
| P2 | **Volume-source Dynkin compensation / the Q coupling** | E[τ]_vol = ∫₀¹ rκ dr + E[μ_exit] − ½·E[F(r₀)] exactly (R = c = 1; r₀ ~ 3r² volume-uniform; F(r) = 2∫₀^r sκ(s)ds; Dynkin on f = F(r)+2x·u, Lf = 2c). E[D]_vol = E[τ]_vol − E[Q], Q = Σⱼ ℓⱼ(uⱼ·u_final) — a retained path functional (residence–direction coupling). Uniform τ₀ = 1: E[F(r₀)] = 3/5, so E[τ]_vol = ½ + E[μ_exit] − 3/10. B1 central re-benchmark 0.4989 vs ½ ✓; B3: 0.93465 vs ½ + 0.73527 − 0.3 = 0.93527 ✓; B4 bookkeeping exact to 7e-16 (0.59715 vs τ−D = 0.59706). **Theorem 1 does not port off-centre** — the reason is itemized (½E[F(r₀)] injection + Q coupling), and the mixed hierarchy P1 is untouched. | An engine with a dedicated escape-face estimator violating E[τ]_vol = ∫rκ dr + E[μ_exit] − ½E[F(r₀)] at > 3 SE (E[μ_exit] = 0.73527 ± 0.00052, n = 1.5×10⁵). |
| P3 | **Density-free transfer-function width bound** | Cauchy–Schwarz on (D, ang) + the P1 moment relations give **E[D²] ≥ 3·E[Dv²]²/E[v⁴]** — no κ, no n_e, no geometry parameter appears; all three inputs are velocity-resolved reverberation observables (E[D²] = ∫τ²Ψ dτdv, E[Dv²] = ∫τv²Ψ dτdv, E[v⁴] = line kurtosis moment). Verified on 4 clouds (table M5); slack 1.06–1.25. | Within-model violation is a Cauchy–Schwarz contradiction (theorem-rigid). Operative falsifier is data-side (J05 §5): for an LRD judged Thomson-scattered with model conditions verified, any ≥ 3σ violation of (a) the joint hierarchy ratios R = 2.64/3.57/4.56 (q = 0) or (b) E[D²] ≥ 3E[Dv²]²/E[v⁴] kills the Thomson-scattering interpretation **for any density**. |

## MEASURED (MC, with SEs where reported; three-engine agreement)

| # | line | value ± SE (engine, n) | source | exit / upgrade |
|---|---|---|---|---|
| M1 | E[D], central uniform τ₀ = 1 | 0.5008 ± 0.0007 (J02, n=10⁶); 0.5012 ± 0.0011 (J01, n=5×10⁵); frozen transport.py 0.4985 (engine Δ ≤ 0.8%); MC reference 0.5008 (J04) | J02 A_central / J01 / J04 | re-measurement beyond 3 SE, or replacement by the deterministic P_N leg once S2/S3 land (S1 already 1.2%) |
| M2 | E[v²], central uniform | 2.8061 (J01 2.806104, n=5×10⁵; J04 MC reference 2.8061; frozen 2.833, Δ 0.6%); exposure identity E[v²] = 2E[ang] verified; E[v²] = 2E[N] isothermal to 0.02%; E[ang] = E[v²]/2, E[ang²] = E[v⁴]/12 (J02 S4b) | J01 / J02 / J04 | joint-consistency family (J05 §1); re-measure at n = 10⁷ or deterministic S2 |
| M3 | E[Dv²], central uniform | 3.7316 ± 0.027 (J01 3.731638, sDv2 0.02735, n=5×10⁵; J04 MC reference 3.7316); identity checks: 3.7316 vs 2E[D·ang] = 3.7237 (Δ 0.2%); q=10: 192.67 vs 192.38 (Δ 0.15%); τ₀=2,q=3,h=2: 234.16 vs 234.04 (Δ 0.05%) | J01 / J04 | as M2 |
| M4 | Closure ratios R = E[Dv²]/(2E[D]·E[ang]) — the shape-pure conspiracy | q=0: **2.6446 ± 0.018**; q=3: 2.0235 ± 0.012; q=10: 1.6971 ± 0.009 (n = 5×10⁵; 5σ+ separations). Even-moment ratios R_m (q = 0, n = 10⁶): m=1 **2.635**, m=2 **3.574**, m=3 **4.563** — the ledger's canonical 2.64/3.57/4.56 | J01 closure table / J02 C / J05 | only a profile with R → 1 within SE could have resurrected the closure (it did not); extension to larger q is registered under ND1 |
| M5 | J05 width-bound table (n = 10⁶, SE on every mean) | (τ₀=1,q=0): E[D²] = 0.7651, bound 0.6141, slack 1.25, σ_D = 0.717; (1,3): 3.3615 / 2.9666 / 1.13 / 1.342; (1,10): 16.213 / 15.235 / 1.06 / 2.683; (2,3): 11.222 / 10.497 / 1.07 / 2.231 | J05 table | bound holds on all; measured tightness is MC-grade until ND1 closes |
| M6 | Volume corrections (τ₀ = 1, volume-uniform) | E[D]_vol = **0.3376** ± 0.0006 (J02 0.337548, sD 0.000640; vs central 0.4989–0.5008; ≠ ½, > 8 SE); E[τ]_vol = 0.93465 vs Dynkin 0.93527 (B3 ✓); E[Q] = 0.59715 vs 0.59706 (bookkeeping exact to 7e-16, B4 ✓); E[μ_exit] = 0.73527 ± 0.00052 (n = 1.5×10⁵, escape-face estimator); observer using the frozen identity on a shell emitter is wrong by exactly E[Q] + ½E[F(r₀)] | J02 B3/B4 / J05 §3 | as P2 |

## KILLED (records preserved; no number adjusted to pass)

| # | line | verdict | falsifier that fired / exit |
|---|---|---|---|
| K1 | **Two-moment closure E[Dv²] = 2·E[D]·E[ang]** | **Dead** — the target's demanded counterexample, quantified: R = 2.64 / 2.02 / 1.70 for q = 0/3/10 (≥ 5σ from 1, shape-separated), and R_m = 2.64/3.57/4.56 grows with m: no finite set of marginal moments {E[D], E[v²], E[N], …} closes the mixed moment; Cov(D, ang^m) is load-bearing at every order. The matched pair matches only two moments — that warning is now a theorem-level negative. | survives iff some assignment of {E[D], E[v²], E[N]} reproduces E[Dv²] = 3.7316; it cannot (J01/J02) |
| K2 | **J03 central-difference grid** | **Failed its own benchmarks, kept as a bona fide negative** (exit 1): E[D] = −0.035 (64×32) / 0.059 (128×64) vs MC 0.501; E[v²] = 0.060 / 0.034 vs 2.806; E[Dv²] = 194 / 9.98 vs 3.73 — non-convergent, sign-flipping. Diagnosis: (1−μ²)/r·∂_μ singular at r → 0 (coupling coefficient 1/r ≈ 60–125 on the innermost row; the iso-μ regularity is invisible to a plain 2D difference), and central differencing of a first-order hyperbolic operator. Sanity anchor passes: the continuous operator is right (L(rμ) = 1 exactly at κ = 0, S4 ✓) — the failure is in the discretization, not the derivation. | resurrection only as a P_N or characteristic solver with an explicit regularity/boundary model — i.e. exactly J04's path (K3) |
| K3 | **J04 pre-fix boundary treatment (the Marshak-blame reading)** | **Superseded on the record**: the failure was a source-basis bug (hierarchy sources live in the l = 0 mode only; `src[:,l] = 1` injected spurious l ≥ 1 sources; fix `src[:,0] = 1.0`). Pre-fix: cond 2.5e9 (L=4) → 1e11 (L=5) → 4e18 (L=9) vs 8e3 exact-Dirichlet; constant level −3.8 vs −0.5; reconstruction battery: exact mode-Dirichlet 1e-15 / 4e-15 (incl. an l=0-carrying field — the boundary-exoneration control) vs Marshak 5e-2 (L=4) / 7e-3 (L=5). Post-fix **S1 LANDED deterministically**: E[D] = 0.4895 (L=5) → **0.4946 (L=9) vs 0.5008** (1.2%, converging from below) — Theorem 1 is now reproduced by an independent discretized transport equation. Two real bugs (kernel 3/8 normalization; collision sign) found, fixed, recorded. | the pre-fix reading survives iff the level stayed wrong after the source-basis fix — it did not; the corrected record is MID (S1 landed; S2/S3 open → N1) |

## NOT PROVEN / OPEN (registered, not hidden)

| # | line | why open | exit condition |
|---|---|---|---|
| N1 | **Deterministic S2/S3 P_N convergence** | E[v²] = 2.414 (14% low) and E[Dv²] = 1.717 (54% low) at L = 9 vs MC 2.8061 / 3.7316; both converge monotonically from below like E[D] did, but the mixed moment needs the most angular content (the G-kernel connects modes up to l±3). L = 13–17 (default grid) is the registered continuation. | L = 13–17 closes to the same class S1 achieved (1.2%); **kill**: the truncation series stalls below the MC reference at the largest affordable L — the deterministic cross-check stays open with the obstruction re-named |
| N2 | **Sharpness of the J05 slack** | Measured slack falls 1.25 → 1.06 from q = 0 → q = 10; no theorem fixes the limit. “Nearly tight” is an MC statement, not a certified one. | analytic slack analysis (ND1): proven slack → 1 certifies tightness; a proven positive lower bound above the measured 1.06 caps it |
| N3 | **Literature novelty re Bal/Jollivet/Patat** | The lane never resolved the overlap for adjacent scattering-order statistics (J01 honest edge). The mixed moment on a sphere is a transport calculation in a standard model; no novelty certificate exists. | primary-literature comparison per the target's promotion requirements — silent until then |
| N4 | **JWST observational application** | No LRD data touched; every entry is a model statement. The armed instrument is J05 §5's falsifier (joint hierarchy ratios 2.64/3.57/4.56 + E[D²] ≥ 3E[Dv²]²/E[v⁴], any ≥ 3σ violation with model conditions verified), not a measurement. | velocity-resolved RM data on a Thomson-candidate LRD; ND2 ships the pre-registered joint test |

## NEXT-DOOR (3 attacks, ranked by expected value; each machine-checkable)

**ND1 — the analytic slack of the J05 bound (highest expected value).** In the Gaussian-lemma variables the bound
is a correlation statement about the pair (D, ang) alone; the measured 1.25 → 1.06 slack (q = 0 → 10) is MC evidence
that the bound is nearly tight, but nothing proves the limit. Plan: re-express slack = E[D²]·E[v⁴]/(3E[Dv²]²) through
the closed factors (2m−1)!!·2^m, i.e. as E[D²]·E[ang²]/E[D·ang]², reducing tightness to the joint law of (D, ang);
compute E[D²], E[D·ang], E[D·ang²] on the J02 engine at n = 10⁷, extend the q-scan beyond q = 10, and cross-check on
the deterministic P_N leg once N1 lands; attempt the closed slack for the uniform cloud from the F-hierarchy's next
orders (L F¹²-order sources are already derived). **Kill condition:** a proven positive lower bound on the slack above
the measured 1.06 (the “nearly tight” claim is then capped and must be weakened), or an n = 10⁷ measurement showing
the q-large limit flattening above 1.05. Converse success: proven slack → 1 along steep profiles certifies the bound
tight-asymptotic, which becomes the channel's observational headline.

**ND2 — the transfer-function covariance E[Dv⁴] as the sharpest observable.** The m = 2 identity
E[Dv⁴] = 12·E[D·ang²] with R_2 = 3.574 compounds the correlation that killed the closure: a model matching the
matched pair (E[D], E[v²]) still fails R_2 five-fold harder than R_1 (2.64 → 3.57), with the joint moment's SE small
relative to that separation. Plan: turn J05 §5's falsifier into a pre-registered six-moment battery
(E[D], E[v²], E[Dv²], E[v⁴], E[Dv⁴], E[D²]) for velocity-resolved transfer-function data, with the within-model engine
audit at n = 10⁷ establishing the SE floor and the required joint 3σ thresholds before any data is opened; the hierarchy
requires all members simultaneously, whatever the density profile. **Kill condition:** any within-model cloud at
n = 10⁷ violating the m = 2 identity at ≥ 3σ refutes the Gaussian lemma itself (this is the sharpest falsifier the
channel can fire); any real LRD dataset violating any member at ≥ 3σ with model conditions verified kills the
Thomson-scattering interpretation for any density — and the m = 2 member is the one the matched pair cannot mimic.

**ND3 — the P_N characteristic-solver for S2/S3 (closes the target's deterministic leg).** The target's
“independent discretized transport equation” currently exists for the mean only (S1, 1.2%). Plan: implement J04's
registered remedies (b)/(c) — characteristic/ray integration of u·∇ψ = S − κ(P−I)ψ from the boundary, or the
integral (Feynman–Kac) form with deterministic ray quadrature on the already-verified Pmat/Gmat — with the explicit
constant-pinning row (a) as fallback if ray integration meets the same near-null constant mode; run the registered
L = 13–17 grid and target E[v²] → 2.8061 and E[Dv²] → 3.7316 at the same monotone-from-below rate E[D] showed.
**Kill condition:** S2/S3 level off below the MC reference at the largest affordable L — the deterministic leg is then
capped at S1 and N1 stays open with the obstruction re-named; converse success: all three moments land
deterministically, N1 exits, and the ledger's deterministic demand is fully satisfied.

## Register line
The moment channel closes in the RH08 structure: **PROVEN** = the conditional-Gaussian hierarchy
E[D v^{2m}] = (2m−1)!!·2^m·E[D·ang^m] (P1, all orders both sources), the volume Dynkin compensation with the Q coupling
(P2), the density-free width bound E[D²] ≥ 3E[Dv²]²/E[v⁴] (P3); **MEASURED** = E[D] = 0.5008, E[v²] = 2.8061,
E[Dv²] = 3.7316, R = 2.6446 ± 0.018 / 2.0235 ± 0.012 / 1.6971 ± 0.009, R_m = 2.64/3.57/4.56, the volume corrections
(E[D]_vol = 0.3376, E[τ]_vol = 0.93465, E[Q] = 0.59715 — 35/35 across three engines); **KILLED** = the two-moment
closure (5σ+, all q, all m), the J03 central-difference grid (failed its own benchmarks), the J04 pre-fix boundary
reading (exonerated by the source-basis-bug fix; S1 landed); **NOT PROVEN / OPEN** = deterministic S2/S3 convergence,
the slack's sharpness, Bal/Jollivet/Patat novelty, the JWST application (N1–N4, each with a named exit).
KEEP: the proof + independent-engine evidence standard, failing-output preservation, the falsifier-first format, and
the density-free observables (E[Dv²], E[v⁴], E[D²]) as the only things an observer can touch. BURN: any presentation
of model identities as JWST confirmation, any “closer to closure” spin, any resurrection of K1/K2/K3 or the frozen
identity on volume emitters without the P2 correction.