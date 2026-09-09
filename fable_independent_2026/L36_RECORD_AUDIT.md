# L36 — adversarial audit of this lane's own standing record

`L36_record_audit.py` + `L36_record_audit.out` (6 checks FAIL of 13; **the FAILs are the finding**).

Target: `HANDOFF_CONTRACT.md` section A, entries A1–A23, and the long form in `FINDINGS.md`.
The job was to break the record, not to confirm it. It broke in twenty-two places.

**Nothing in `FINDINGS.md` or `HANDOFF_CONTRACT.md` was edited. Every correction below is a proposal
for the orchestrator.**

---

## The headline

**The computations are sound. The sentences are not.**

All 22 lane scripts were re-run for this audit and diffed against their committed `.out`. Every one
reproduces to the character; only wall-clock timing lines differ. Nothing in this record has drifted
from its script. The four algebraic keystones were re-derived here in exact symbolic arithmetic,
*independently of the lane's own code*, and all four are right:

| keystone | exact value | record |
|---|---|---|
| `S₄′(1)\|σ=1/3` | −11.140771125114798741 (40 digits) | −11.1407711251147987 ✓ |
| `S₄′(1)\|σ=1` | −20.194205022906776 | ✓ |
| `σ* = 4T/(4T−27) = 3/a_*` | 1.6793127321871131, exact identity | ✓ (29.588% superluminal) |
| `α₁ = −4c₁₄` on `c₁ = −c₃ = K_B` | exact in the field, `c₂* = c₁₄/(1−2c₁₄)` its exact α₂ zero | ✓ |
| split-degeneracy map | exact rational identity; `Z/β² = 2/κ² − 2b` | ✓ (7.9640 / 5.4756 / 9.3871) |

A8's `5.73 ± 0.68` and `f_bar = 0.149` were rebuilt from the raw X-COP audit JSON and reproduce to
three significant figures.

So every error found is an error of **description**. That is the good news and it is also the pattern:
**this record's failure mode is the sentence, not the solve.** Every fix is a rewrite, not a re-run.

**Counts: 25 verified · 4 wrong · 3 overclaimed · 8 footing-leaky · 3 statistics-only · 1 weak ·
8 unverified.**

---

## PASS/FAIL lines, verbatim

```
  [PASS] X0 [CONTROL] the exact-arithmetic machinery reproduces the record's boxed obstruction to 18 digits AND rejects a deliberately corrupted version of the same closed form
  [PASS] X1 [CONTROL] the split-degeneracy theorem holds as an exact rational identity and the machinery REJECTS the corrupted map with (1-mu) in place of (1-mu^2)
  [PASS] X2 [CONTROL] alpha_1 = -4 c_14 is exact on the c_1 = -c_3 = K_B locus, c_2* = c_14/(1-2c_14) is its exact alpha_2 zero, and a corrupted Foster-Jacobson numerator is REJECTED
  [PASS] X3 [CONTROL] the saturation point (s_sat, Delta_sat) = (2.540, 0.6476) shared by L6/L13/L21/L23 is the true argmax of the carried Delta, and the same machinery rejects a corrupted target
  [PASS] X4 [CONTROL] the currency probe finds a number that IS in the source .out and does NOT find a one-digit corruption of it
  [PASS] X5 [CONTROL] the cheap lane scripts re-run today reproduce their committed .out exactly, so the stored outputs are current and the F5 test is reading live numbers
  [FAIL] F1 [FAILURE MODE 1, footing leakage] no entry in section A quotes one number where the two a0 footings give different values
  [FAIL] F2 [FAILURE MODE 2, arithmetic in prose] every arithmetic statement in section A and FINDINGS recomputes correctly from its own stated inputs
  [FAIL] F3 [FAILURE MODE 3, correlated errors] every sigma and every error bar in section A either includes a coherent-systematic floor or is labelled statistics-only where it is quoted
  [FAIL] F4 [FAILURE MODE 4, overclaim] no section-A sentence is stronger, broader or more general than what its script's PASS/FAIL lines and printed numbers support
  [PASS] F5 [currency] every section-A number is present in the output its own entry names, and every lane script reproduces its committed .out today
  [FAIL] F6 [cross-entry] no two section-A entries disagree on a shared quantity
  [FAIL] F7 [VERDICT] the standing record in HANDOFF_CONTRACT section A is sound AS WRITTEN and can be relied on without amendment
```

The six controls X0–X5 each reproduce a known-correct identity **and** reject a deliberately corrupted
version of it. The auditor is demonstrably capable of failing.

---

## Every error found, with its correction

### WRONG — the number in the record is not the number that is true

| # | where | as written | correct |
|---|---|---|---|
| E1 | `FINDINGS` §L2 | "J_Y ≈ 0.13–0.18 nearly constant, **i.e. g_obs ≈ 6.9 g_N**" | `J_Y = s/Δ_req`, so `1/J_Y = M_dark/M_bar` and `g_obs/g_N = 1 + 1/J_Y`. The 6.9 is the **dark-to-baryon ratio**, not the boost. **Correct: M_dark ≈ 6.9 M_bar, i.e. g_obs ≈ 7.9 g_N** (log-centre of the fitted law over s ∈ [0.09, 0.91]; at 1000 kpc the measured values are M_dark/M_bar = 5.73 and g_obs/g_N = 6.73). L2's own `.out` sentence, "G rescaled by 1/J_Y ~ 6.9", is correct — the FINDINGS restatement introduced the error. |
| E2 | A17 | "scale bounded at **<3.3e-13**, i.e. **3.4 dex** below a₀" | Two different statistics welded into one sentence. `3.29e-13` is the bootstrap 95% upper limit and is **2.45 dex** below a₀ (2.54 alt). The 3.47 dex figure belongs to the *point estimate*, which railed at the search floor `10^-13.5 = 3.2e-14`. **Quote one: "<3.3e-13 m/s², 2.5 dex below a₀" or "point estimate 3.2e-14, 3.5 dex below a₀."** |
| E3 | A9 / `FINDINGS` §L1 | "0.92–1.45 M_b, still **4–6×** the 0.25 the RAR tolerates" | `0.92/0.25 = 3.68`, `1.45/0.25 = 5.80`. **Correct: 3.7–5.8×.** Small, but it is an exceedance factor quoted in the handoff. *Also:* L1 produces a fourth run, `mp_cons60a = 0.96`, which the FINDINGS table omits. It lies inside 0.92–1.45 so nothing moves, but the table is an incomplete record of the runs. |
| E4 | `FINDINGS` lane headers | four of twenty-one miscount their own checks | L1: **3 FAIL of 11**, not "of 12". L4: **1 FAIL of 29**, not "of 24". L16: **5 FAIL of 12**, not "of 11". L18: **6 FAIL of 10**, not "7 FAIL of 10" — L18's own `RESULT:` line says 6. |
| E5 | `FINDINGS` §L2 | "exceeds the widest bounded-boost ceiling by **2.9×**" | L2-C4's own text says **3.0×** (max required Δ = 3.01 against C_max = 1.000); 2.94/2.9× is the stellar-7 subset. Quote the check's number or say which subset. |
| E6 | A20 | "**30.9 ± 1.6 within the pair separation** against 5.73 ± 0.68 at 0.80 R500 — 5.7×, **16σ**" | The 16.3σ L21-S1 computes is against the **cosmic 5.43**, not against L7's measured 5.73 ± 0.68. Against 5.73 ± 0.68 the combined figure is 14.5σ. The σ is attached to the wrong comparison. |

### OVERCLAIM — the prose is stronger than the script

| # | where | as written | what the script says |
|---|---|---|---|
| E7 | **A14** | "The lead's own 'galactic matching' open item is answered **POSITIVELY**." | L11 runs 22 checks and **three FAIL**, two of them on exactly this question: **B2b** (the kernel produced is the exponential carrier, not the programme's carried ν_RAR — 0.073 dex apart, ceiling exceeded 5.2× more often on bulgeless SPARC), **B3** (the IC kernel *is* disfavoured on that control), **B5** (the far-field boundary condition on `u` is **not determined** by the published files; if `u` must approach the cosmological value, 27%/38% of bulgeless SPARC points beyond 2 kpc sit below the implied universal external field). L11's own verdict line says the open items "are scored separately as B2b and B5 and are **not hidden inside this verdict**". A14 hides them; FINDINGS does not. **This is the entry the lead is told it may rely on.** |
| E8 | **A16** | "**clears** the cosmological gates (BBN, CMB, growth, expansion incl. absolute BAO) … predicting **σ₈ = 0.845–0.861**" | L9 annotates that same σ₈, in the same table row, as **6–8σ from Planck's 0.8111 ± 0.0060**. The RSD gate is `Δχ² ≤ 9` and the canonical band runs from `+5.28` right up to `+9.00`, i.e. to the boundary. Ω_Λ = 0.248–0.321 against a measured 0.685 is "not gated". "Clears" is doing work a ±10% σ₈ gate cannot support. FINDINGS carries "every survivor sits at the top of the growth gate"; A16 does not. **Add "already 6–8σ from Planck σ₈" to A16.** |
| E9 | **A1** | "c₇ is genuinely built from action derivatives alone." | True (L4-I6, checked symbolically). But L4-**I5**, in the same run, records what neither A1 nor FINDINGS carries anywhere: *"the central IC7 identity S₄ + 32Vc₇/B3⁴ = 0 holds identically on the isotropic plateau — **but it holds because c₇ IS −S₄/32 by definition: the repair is an exactly tuned counterterm, not an independent prediction of the action.**"* That is the single most important qualification on the IC7 repair, it is the lane's own finding, and it is missing from the record. |

### FOOTING LEAKAGE — one number quoted where two are needed

Ten leaks across eight entries. The `.out` files print both footings in every case; the record drops one.

| # | entry | as written | canonical | alt | impact |
|---|---|---|---|---|---|
| E10 | **A4** | "Cassini **3.7e4×** above the PPN threshold; coupling **e^(−5.8e5)**" — and FINDINGS adds "on both footings" | **6.96e5 a₀, 4.5e4×, e^(−7.0e5)** | 5.78e5 a₀, 3.7e4×, e^(−5.8e5) | **The quoted pair is the ALT column of L10's own two-footing table**, presented as universal. Conclusion unaffected (both are astronomically safe); the record quotes the *weaker* margin. |
| E11 | A5 | "\|a\|/a₀ = 8.8e38 … D_loss = 4.5 ℓ_M = **33 Hubble distances**" | 8.81e38, 33.2 D_H | **7.31e38, 27.6 D_H** | none on the verdict ("no bound at all" either way) |
| E12 | **A20** | "ν̄ = 7.99 vs 6.43, **11.5% apart in velocity** … below the stellar-M/L systematic" | ν̄ = 7.994, **+11.5%** | ν̄ = **8.733**, **+16.5%** | **Material.** The "exact degeneracy, below the M/L systematic" reading is a canonical-footing statement. 16.5% is the *same size* as the systematic the sentence invokes to dismiss it. |
| E13 | A20 | "kernel + cosmic share, **1.141 ± 0.028**" (5.0σ) | 1.141 ± 0.028, 5.0σ | 1.099 ± 0.025, 4.0σ | the entry gives both footings for its *first* row and one for this one |
| E14 | A19 | "c₁₄_eff/c₁₄ = **1.190** at Saturn" | 1.1898 | **1.2333** | L13:357 computes `jy = J_Y(s_can)` and never uses the `s_alt` column it prints. The alt drag is 23% larger. |
| E15 | A19 | "c_s ≥ **19c** at 1 AU / **2522c** at Cassini conjunction" | 18.8c / 2522c | 17.1c / 2298c | none; both hugely superluminal |
| E16 | A12 | "\|K2\| in **[5e4, 5e5]**" | [5e4, 5e5] | **[5e4, 3.16e5]** | the alt region is 37% narrower in \|K₂\| than stated |
| E17 | A16 | "H0 = **68–72**" | 68.9–72.0 | **67.4–72.2** | the stated lower edge is 1.5 km/s/Mpc too high once the alt footing is in. (The σ₈ union 0.845–0.861 *is* right, but it is a union: canonical alone is 0.853–0.861.) |
| E18 | A17 | "fixed-a₀ kernel **0.142 dex**" | **0.145 dex** | 0.142 dex | L16-A1 itself says "(best footing: alt)"; the record quotes the better footing without saying so |
| E19 | A18 | "the b … is negative (**−0.82**)" | −0.819 | **−0.681** | FINDINGS carries both; the handoff entry carries one |

### STATISTICS-ONLY σ — the L23 failure mode, reintroduced

`L23` corrected exactly this in `h9` (19.4σ → 4.9σ). Three entries in section A repeat it.

| # | entry | quoted | what is coherent across the sample | recomputed |
|---|---|---|---|---|
| E20 | **A20** | **19.6σ** (and 24.9, 22.4, 25.0, 5.0, 16.3, 3.9, 5.6) | one Υ_K = 0.6 for all 1900 pairs; one distance scale; one isolation criterion; one circular-orbit assumption; one interloper model. `A ∝ Υ^(−1/4)`, so a coherent M/L error moves every pair together — **L21's own systematics note says the shape axis "is immune to this", i.e. the amplitude axis is not.** | 0.10 dex coherent Υ_K → **7.2σ**; 0.15 dex → 5.0σ; adding the lane's *own* leading systematic (isolation depth, A falls 1.99 → 1.51 measured) → **3.0σ**. Same for the ladder: 30.9 ± 1.6 → **3.1σ** from the cosmic 5.43, factor 5.7 → 4.5–7.2. |
| E21 | **A8** | **13–15σ** residual | one HSE estimator, one XMM calibration, one gas-density deprojection, one stellar prescription, one kernel, one a₀ — none averages down. The quoted σ is `median / (scatter/√12)`. The residual is a **difference of two large numbers**, so a 10% coherent X-ray mass calibration moves it 22%. | 10% coherent M_HSE floor → **4.4σ**, not 15. |
| E22 | A7 | \|z\| = 13, 12.8σ | SPARC's frozen Υ_disc = 0.5 (coherent, ~0.11 dex in the literature) on the galaxy side; the HSE bias on the cluster side | not recomputed here — the SPARC-side term needs L2/L6 re-run with Υ profiled. **UNVERIFIED as a significance.** |

**In every one of these the direction of the conclusion survives and only the number falls.**
A > 1 for binary galaxies is robust; 19.6σ is not. The cluster residual ≠ 0 is robust — and here the
record is *helped* by the physics: L18 shows the one systematic that is actually measured (the
hydrostatic bias, b ∈ [0.00, 0.42]) moves the residual **away** from zero, 3.09 → 4.85 at b = 0.20.

**A22 is the counter-example and the template.** It quotes 4.9σ/4.7σ *after* a 0.227 dex coherent floor
built from a named line-item budget (M/L+IMF 0.148, aperture/anisotropy 0.120, cluster model 0.088,
instrument 0.052, estimator 0.047, **a₀ footing 0.047**, distance 0.021), and it names the stat-only
19.4σ as the thing being corrected. Recomputed here: `1.159/√(0.062² + 0.227²) = 4.93σ` ✓.
The lane knows how to do this. It did it once.

### WEAK — the record understates its own check

| # | entry | as written | achieved |
|---|---|---|---|
| E23 | A15 | "verified … numerically at six sigma **to <1.7e-40**" | `1.7e-40` is the **tolerance** in `L15_SIGMA_ONE.md`. The script's L15-G2 prints the achieved agreement: **4.867e-51**, eleven orders better. Not an overclaim — an understatement that reads as a measurement. |

### CROSS-ENTRY DISAGREEMENTS

| # | quantity | the conflict |
|---|---|---|
| E24 | the `± 0.68` on the cluster ratio | **A8** quotes it as the 12% cluster-to-cluster **scatter**; **A20** places it alongside "30.9 ± 1.6" where it reads as an uncertainty. The error on the median of 12 would be `0.68/√12 = 0.20`. A20's own 16.3σ in fact uses neither — it compares to 5.43 with only the 1.6. One symbol, three meanings. |
| E25 | the tensor cone `c_T²` | **A3**: "IC7 detunes the tensor cone: `c_T² = 1 − 4c₇R̄₀/c`". **A15**: "`c_T² = 1` … is a σ-**INDEPENDENT identity**". Both are true of different backgrounds (A15 means the IC6 sector on **flat** backgrounds) but as written the handoff asserts luminality as an identity in one row and its violation in another, with no qualifier. *Also unrecorded:* L15-R14 finds the detuning roughly **doubles** at σ = 1 (0.00857 → 0.02259); A3 carries only the σ = 1/3 number. |
| E26 | the α₂ closed form | **L10-K1** identifies a `3c₁₄²/4` term **omitted** by g03v — verified symbolically here: the correct expansion is `−c₁₄/2 + c₁₄²/(2c₂) + 3c₁₄²/4`. **A19 / L13-P2** then quote the *uncorrected* form. Numerically irrelevant at c₁₄ ~ 1e-5, but the record repeats an error one of its own lanes corrected. |
| E27 | Cassini \|a\|/a₀ | A4's number contradicts its own script's table (same as E10). |

### CROSS-CHECKS THAT PASSED

- **s_sat = 2.540, Δ_sat = 0.6476** — used identically in L6, L13, L21, L23, and re-derived here from
  scratch as the true argmax of `Δ(s) = s/(e^√s − 1)`: solving `e^u(2−u) = 2` gives `u = 1.5936243`,
  `s = 2.5396`, `Δ = 0.64761`. ✓
- **a₀ footings** — all 22 scripts use 9.3619e-11 / 1.1279e-10. No third value anywhere. ✓
- **cosmic ratio 5.43** — identical in A8 and A20. ✓
- **c₁₄ ceiling** — A6's 2.5e-5 (from α₁) contains A12's 1.18e-5 (sweep grid edge). Containment, and
  A12 correctly says "consistent", not "equal". ✓
- **2.2–5.1× cluster/galaxy contrast** — identical in A7, A16, A18; L18-H1 reproduces L2 exactly as a
  control. ✓
- **A7 vs A8 on the same clusters** — recomputed from the raw JSON: `M_dark/M_bar` at 1000 kpc = **5.730**,
  matching A8 exactly and lying inside L2's headline `1/J_Y = 5.44–7.91`. ✓ *One caveat neither entry
  states:* this agreement holds on L2's **stellar-7** headline subset only. L2's all-12 subset gives
  `J_Y` down to 0.100 (`1/J_Y = 10.0`), which does **not** contain 5.73.

---

## The ledger

25 VERIFIED · 4 WRONG · 3 OVERCLAIM · 8 LEAKY · 3 STAT-ONLY · 1 WEAK · 8 UNVERIFIED.
Full machine-readable form in `L36_record_audit.out` section G. Summary by entry:

| entry | verdict | note |
|---|---|---|
| A1 | OVERCLAIM | algebra reproduces exactly (obstruction re-derived to 40 digits independently); I5's "exactly tuned counterterm" qualification missing |
| A2 | VERIFIED | DOF = 3, A₀ = 0.4614531036, λ = 1, c_s² = 1/3 — L4-D2/D3/C1 verbatim |
| A3 | VERIFIED (with E25) | window 1.0736445, 4c₇/c = 0.008570513 — verbatim; conflicts with A15's phrasing |
| A4 | LEAKY | quotes the alt column as universal |
| A5/A6 | VERIFIED | model conditional: three tiers, deciding input named, region explicitly scoped to Y1 |
| A5 | LEAKY | 8.8e38 and 33 D_H are canonical-only |
| A7 | VERIFIED (ratios) / STAT-ONLY (z) / WRONG (FINDINGS' 6.9 g_N) | the ratio 2.2–5.1 carries the argument; the record leads with the z |
| A8 | VERIFIED (5.73, 12%, f_bar) / STAT-ONLY (13–15σ) | rebuilt from raw JSON; σ is scatter/√12 |
| A9 | VERIFIED (0.92–1.45) / WRONG (4–6×) | correct factor 3.7–5.8× |
| A10 | VERIFIED | 5.7e-03 vs 1.3e-09, unbinds within 1 Gyr at any timestep — L1-V5a/V5b verbatim |
| A11 | **VERIFIED, exemplary** | the one entry that names its own footing dependence. Theorem exact in rationals |
| A12 | VERIFIED (core) / LEAKY (\|K₂\|) | no admissible point on either footing; every minimal subset contains G2; all 10 gate controls PASS |
| A13 | VERIFIED | Ω_d,eff ≤ 2.6e-6 vs 0.266, short by 1.0e5× |
| A14 | OVERCLAIM | the reduction itself verifies exactly (coefficient 1.000000, no slip <1e-4, same G); B2b/B3/B5 dropped |
| A15 | VERIFIED / WEAK | σ* = 4T/(4T−27) exact; "<1.7e-40" is a tolerance, achieved 4.867e-51 |
| A16 | OVERCLAIM / LEAKY | gates as defined pass; σ₈ is 6–8σ from Planck in L9's own annotation; H0 union is 67.4–72.2 |
| A17 | WRONG (dex) / LEAKY (0.142) | 74.0% → −3.5% and the 11 halo rows verify |
| A18 | VERIFIED / LEAKY | the only entry that exists to attack this lane's own strongest claim. Self-correction of L7's "5%" is real |
| A19 | VERIFIED (α₁, Λ_sc, 7.3e-92) / LEAKY (c₁₄_eff, cone) / see E26 | α₁ = −4c₁₄ and c₂* verified exactly; Λ_sc = 1.5400e16 GeV and c₁₄ < 7.34e-92 reproduce from the reduced Planck mass |
| A20 | STAT-ONLY / LEAKY ×2 / WRONG (E6) | every measured number reproduces; the 1.9σ "closest slope of any law" is confirmed as the minimum of seven |
| A21 | **VERIFIED, exemplary** | both footings on both numbers; every clause maps to a named check |
| A22 | **VERIFIED, exemplary** | 4.93σ recomputed; the only defensible significance in section A |
| A23 | VERIFIED | all thirteen quoted numbers found; internal units, footing-free by construction |

### UNVERIFIED — recorded as such, **not** passed by default

1. **A9's convergence.** No run above N = 8000 exists. FINDINGS concludes "the converged value is at or
   above these"; L1's own line reads "numbers RISING with N are particle noise, not caustics", which is a
   *different* claim. Settling it needs N = 16000–32000.
2. **A9's carried-over caveats** that L1 declines to repair: angle-averaged QUMOND rather than a solved
   field equation, an isolated vacuole with no tides, z_i = 20 against the shell model's 50.
3. **A20's isolation depth.** Every amplitude is an upper limit and the lane says so; how much further a
   2-magnitude-deeper catalogue would take it is not computable from 2MRS. It is the single number the
   entry most needs.
4. **A7's SPARC-side Υ systematic** on \|z\| = 13 and 12.8σ.
5. **A16's region** — whether it is real or a boundary artefact of the ±10% σ₈ gate and the Δχ² ≤ 9 RSD
   gate, which the canonical band runs right up to.
6. **A12's grid resolution.** 1.2e8 points is ~22 per axis in six dimensions; "no admissible point" is a
   statement about a coarse log grid, and the surviving region is described in the `.out` itself as "a
   thin sheet" where the marginal boxes are not independent.
7. **A2/A3's lead-side inputs.** L4 rebuilds the lead's algebra independently and it reproduces, and the
   lead's `c₇ = 0.00235189114143216`, `S4₁₁ = −0.0642323935174161` and leftover `0.0151964888331` are
   present in its files today. What is **not** verified is the lead's anisotropic two-mode reduction
   itself, which neither L4 nor L15 reproduces (L15 names it as missing).
8. **A19's scalar cubic action.** L13-P9 FAILs because Δ′ = 0 on the saturated branch, so Σ_∥ = ∞.
   A19 records this correctly.

---

## What would formal verification actually buy here?

Asked concretely, per failure mode, with Mathlib's real coverage rather than its reputation.

### The short answer

**Lean 4 would have caught none of the twenty-two defects found today**, because none of them is a
false proof. They are a footing dropped in transcription, a ratio relabelled, four miscounted headers,
an error model that omits a term, and three sentences that summarise a script by leaving out its FAILs.
A proof assistant checks the argument you write down; every failure here is in an argument nobody wrote
down.

**But two results in this record are worth formalising anyway**, for a reason that has nothing to do
with the four failure modes: they are universally-quantified statements the programme currently
believes on the strength of one `sympy.solve` call.

### Per failure mode

**FM1 — footing leakage.** Lean *could* catch this: make every dimensional quantity a function of `a₀`
and quoting one instantiation becomes a type error. But that is dependency tracking, not theorem
proving, and Python's type system does it for a fraction of the cost.
→ **The right tool is a typed reporting harness.** A `report(name, {canonical: x, alt: y})` helper that
*refuses a scalar* for any quantity in a footing-sensitive unit class. Ten of ten leaks found today
originate in a print statement that accepted one float where the script had already computed two. L13
is the clearest case: it prints an `s (alt)` column and then never uses it (`L13:357`). ~1 day. **Not
Lean.**

**FM2 — arithmetic in prose.** The strongest case for machine checking, but it is a
literate-programming problem, not a proof problem. Every one of the ten slips is a number *retyped by
hand* into a markdown file from a `.out`.
→ **The right tool is transclusion.** Each lane script emits `results.json`; a linter asserts every
numeric literal in `FINDINGS.md` / `HANDOFF_CONTRACT.md` resolves to a key in some lane's JSON. That
catches E1, E2, E3, E5, E6, E23 **and all four miscounted headers** (E4), which are mechanically
derivable from the `.out`. ~1–2 days, and it is the single highest-value change available.
Lean *can* do the numeric subset — `dexBelow a b := Real.logb 10 (a/b)` with `norm_num` interval
extensions would reject "3.29e-13 is 3.4 dex below 9.3619e-11" — but at roughly fifty times the cost of
the linter, for the same catch.

**FM3 — correlated errors.** Mathlib has the machinery to state the lemma (`ProbabilityTheory.variance`,
covariance, and variance-of-a-sum for independent variables), and
`Var(mean of Xᵢ = Yᵢ + S) ≥ Var(S)` is a short, real theorem. **It would not have helped.** Neither h9
nor A20 believed a false lemma about variance; both simply never wrote a term for the shared systematic.
A proof assistant cannot tell you your model omits a variable — it can only check the model you gave it.
There *is* a version that helps — formalise the *estimator*, so that "the eleven objects are
independent" becomes an explicit hypothesis you cannot discharge without proving it — and Mathlib's
`gaussianReal` makes it reachable for a simple likelihood. It is a months-long project.
→ **The right tool is a required error-budget schema.** Every reported σ must carry a named line-item
budget in A22's shape, and the harness must **refuse** a σ whose budget contains only a "statistical"
line. That is a 30-line dataclass and it catches E20, E21 and E22 on the spot, and would have caught h9
in 2026-08. Do this first; consider the Lean estimator only if the programme ever publishes a headline σ.

**FM4 — overclaim.** Entirely outside a proof assistant. No formal system compares an English sentence
to a PASS line.
→ **The right tool is citation-linting.** Require every section-A sentence to name the check IDs it
rests on, then assert that every `[FAIL]` in a cited script is either mentioned in the entry or
explicitly waived. That catches **E7** (A14 cites L11 and omits three FAILs) and **E8** (A16 cites L9
and omits its own σ₈ annotation) mechanically. It does **not** catch **E9**, where the missing caveat
lives in the *detail text of a PASS* — for that the rule has to be "a cited check's detail text is
quoted in full or not at all". ~1 day.

### What is formalisable in Lean 4 / Mathlib today

**Formalisable now, and worth it:**

1. **A15's σ\* theorem — the highest-value target in the record.**
   `S₄′(1;σ) = e^{5/6}(p_R T − 9)(3p_R + 4)(3p_R − 44)/(216(4T − 27))` with `p_R = 8/3 + 4a_*σ` is a
   product of three affine functions of σ over a positive constant. The theorem — *exactly one zero, at
   `σ* = 4T/(4T−27) = 3/a_*`, and `σ* > 1` for every `T > 27/4`, hence `S₄′ < 0` on the whole of IC-4's
   design interval `(0,1]`* — reduces to three goals well inside `nlinarith`/`positivity`: the zero of
   the third factor, positivity of the other two for σ > 0, and `4T/(4T−27) > 1`. Mathlib coverage is
   complete (ordered fields, `Real.exp` positivity). **Effort: days.** Worth it because it is a
   ∀-statement over a design interval, and a ∀-statement is precisely what a numerical scan cannot
   establish and a proof assistant can. The programme is currently relying on one `sympy.solve`.

2. **A19's `α₁ = −4c₁₄` and `c₂* = c₁₄/(1−2c₁₄)`.**
   A rational-function identity after clearing `2c₁ − c₁² + c₃²`, with side condition `K_B ≠ 0`;
   `field_simp; ring` closes it. Mathlib coverage complete. **Effort: hours.** Worth it because this
   identity is what killed A3's design principle, and everything downstream — the c₁₄ ≤ 2.5e-5 ceiling,
   A6's whole target region, A12's cross-check — rests on it being *exact* rather than approximate.

3. **A11's split-degeneracy map.** `(Z + 2bβ²(1−μ²)) + 2b(μβ)² = Z + 2bβ²` is closed by `ring`
   outright; `κ → μκ` needs one `Real.sqrt` step. **Effort: an afternoon.** Cheap, and it is the
   load-bearing statement about κ.

4. **X3's saturation point** as a uniqueness theorem (`Δ(s) = s/(e^√s − 1)` has exactly one critical
   point on `s > 0`) — Mathlib has `Real.exp`, strict monotonicity and the IVT. The *18-digit numeric
   value* is a different matter: rigorous decimal bounds on `Real.log(9/5)` or `Real.exp` need interval
   arithmetic built on `Real.exp_bound`, which is feasible but is a week of work that buys nothing
   scientific. **Formalise the uniqueness and the sign; leave the digits to mpmath.**

5. **The FM3 variance lemma**, as documentation rather than as a check.

**Not formalisable today, and it is not close:**

6. **A2's degree-of-freedom count of 3.** This is Dirac constraint analysis on a field-theory phase
   space: primary and secondary constraints, first/second-class classification by the rank of the
   Poisson-bracket matrix, and the counting formula `(2N − n₂ − 2n₁)/2`. Mathlib has symplectic *linear
   algebra* and smooth manifolds; it has **no Poisson brackets on a constrained phase space, no ADM
   decomposition, no Dirac algorithm**, and PhysLean does not cover it either. What *is* formalisable is
   the finite-dimensional step where an error would actually hide: *"this 4×4 Dirac matrix has rank 4"*
   is `Matrix.rank` / `det ≠ 0`, and Mathlib does that today. **Formalise the rank claim, not the DOF
   theorem.**

7. **A3's `c_T² = 1 − 4c₇R̄₀/c` and A14's MOND reduction.** Variational calculations on a Lorentzian
   manifold: curvature-tensor identities, Euler–Lagrange for field Lagrangians, an ADM split. Mathlib
   has none of this at working strength. The realistic failure mode here is a *transcription* error in
   sympy, and the tool that catches transcription errors is **a second independent CAS** — xAct or
   Cadabra re-deriving the same variation. That is what L4 and L11 already do by hand; a second CAS
   would harden it far more cheaply than a proof assistant could.

8. **Everything with data in it** — A7, A8, A9, A16, A17, A18, A20, A22. No proof assistant reaches a
   claim about a measurement. The only defence is A22's: a named, propagated error budget.

### Recommendation

| failure mode | Lean would have caught it? | do this instead | cost |
|---|---|---|---|
| FM1 footing | in principle; not economically | typed two-footing reporting harness | ~1 day |
| FM2 arithmetic in prose | partially, expensively | `results.json` transclusion + numeric-literal linter | ~2 days |
| FM3 correlated σ | **no** — the omission is in the model | required error-budget schema in A22's shape | ~1 day |
| FM4 overclaim | **no** | citation-linting: cited FAILs must be mentioned or waived | ~1 day |

**Five days of harness work would have prevented seventeen of the twenty-two defects found today.**
Then formalise exactly two theorems — **A15's σ\* uniqueness** and **A19's α₁ = −4c₁₄** — not because
they are at risk of being wrong (both were re-derived exactly here) but because they are the two
∀-statements the whole clock sector rests on, and a machine-checked proof is the only thing that closes
a ∀ over a parameter interval. Do **not** attempt the constraint analysis, the variational reductions,
or anything with data in it. Mathlib is not there, and for the data-side claims nothing ever will be.

---

## Standing after L36

The record is **repairable in place**. Not one finding requires re-running a solve; every one is a
sentence. The three that must be fixed before the record is used:

1. **A20's significances are statistics-only** on a sample sharing one Υ_K, one distance scale and one
   isolation criterion — the identical failure L23 corrected in h9, reintroduced in the newest entry.
   19.6σ → ~7σ with a 0.10 dex M/L floor, ~3σ including the lane's own isolation band. **A > 1 survives;
   the number does not.**
2. **A14 tells the lead its galactic-matching item is "answered POSITIVELY"** while dropping the three
   FAILs L11's own verdict line insisted be kept visible.
3. **A4 quotes the alt column of L10's two-footing table as universal**, while FINDINGS says "on both
   footings". Canonical is 6.96e5 a₀ and 4.5e4×.

And one thing worth saying plainly in the record's favour, because this lane's rule cuts both ways:
**A11, A18, A21, A22 and A23 are clean as written.** A18 exists solely to attack this lane's own
strongest claim and does it correctly, including withdrawing L7's "5%" headline. A22 is the only
defensible significance in section A and is the template the rest should follow.
