# U05 — THE ANALYTIC SLACK (J00/ND1): (D,ang) joint law, thin + asymptotic limits, and the ND1 kill verdict

**2026-09-25 · moment channel · files `U05_slack.py` · `U05_slack.out` · `U05_results.json` · this file**
Engine: `J02_moment_hierarchy.simulate` (exact optical-depth bisection, bit-identical kernels, no null-collision thinning). Every number carries a 24-block jackknife SE; every formula is engine-verified; no git commit (lane rule). Append-only: J00–J06/L01–N02 untouched. The final artifacts come from one coherent clean run (`python3 U05_slack.py all`, exit 0, 100/100 checks; a deterministic phase-3 re-derivation with the final code is appended to the log).

---

## 0. Bottom line up front

**1. The closure ratio R₁ and the J05 slack are NOT the same object.** R₁ = E[D·ang]/(E[D]E[ang]) = 1 + Cov(D,ang)/(E[D]E[ang]) is a *mean-normalized covariance* that **diverges as τ₀ → 0** (E[D·ang] = O(τ₀) against E[D]E[ang] = O(τ₀²): the L01 law R₁−1 = (7/5)/[(1+q/3)τ₀] − 1 re-verified here at τ₀ = 0.002 with R₁ = 703/348/164 at q = 0/3/10, and R₁τ₀(1+q/3)(5/7) = 1.0041/0.9936/1.0127 — within 1.7 SE of 1+g(q)τ₀ at τ₀ ≤ 0.02). The slack slack₁ = E[D²]E[ang²]/E[D·ang]² = 1/ρ0² is a *pure shape ratio* that stays **finite**. The exact link between the two objects (algebra; machine-exact round-trip on every cloud):
> **slack₁·R₁² = (1+CV_D²)(1+CV_ang²)**  (CV = mean-normalized std; both sides equal E[D²]E[ang²]/(E[D]E[ang])²).

**2. The thin-limit slack is a CLOSED rational curve in q** (N=1 sector, exact): on one-collision photons D = s₁(1−μ), ang = (1−μ) pointwise, so slack → E[s₁²|N=1]/E[s₁|N=1]² with s₁ collision-length-biased:
> **S_thin(q) = (1/3 + q/5)(1 + q/3)/(1/2 + q/4)²  =  4/3, 448/375, 91/81  at q = 0,3,10  → 16/15 (q→∞)**  (central source)
Engine: quadratic-in-τ₀ intercept fits over the deep points (τ₀ ≤ 0.02, n = 10⁷) land on S_thin at **z = 0.79 / 0.80 / 0.58** (q = 0/3/10); the N=1 slice ratio E[D|1]/E[ang|1] = (1/2+q/4)/(1+q/3) passes at z ≤ 1.8 at τ₀ = 0.002. Measured subtlety: at q ≠ 0 the full-cloud slack **rises** from the intercept with τ₀ (the N=2 sector enters the ratio at O(τ₀); its slice carries the exact extra factor 7/6 in the ang² term — D|N=2 = s₁(1−μ₂), ang|N=2 = (1−μ₁)+(1−μ₂) by the telescoping lemma), peaks, then falls to the thick values; slack(τ₀)|q is **non-monotone**.
**Volume-source analogue CLOSED in rationals** (chord geometry; new constants E[ch⁵] = 2, E[r₀²ch³] = 3/5, E[(r₀·u)ch⁴] = −4/5, E[∫s²r²ds] = 1/5 — Legendre 2048², agreement 1e-9, E[ch⁵] MC-checked at n = 3×10⁷, z = 0.05):
> **S_vol(q) = (1/3 + q/5)(3/4 + 5q/12)/(2/5 + 8q/35)²  =  25/16, 1715/1083, ≈ 1.59048  at q = 0/3/10  (→ 1225/768)**
with the denominator = N02's closed c₀ = 2/5 + 8q/35. Engine: volume intercept fits at z = **0.15 / 1.62** (q = 0/3). **N02's closed thin window R_v(0,q) = (3/4+5q/12)/(2/5+8q/35) is a different observable** — the thin limit of the *ratio of means* E[ang]/E[D] for the volume source — same N=1 machinery, different object (§2 table).

**3. Asymptotic q → ∞: slack−1 is NOT linear in 1/N̄** (local exponents β_eff = −0.536/−0.436/−0.303/−0.081/−0.021 across the scan pairs 0→3→10→30→100→150; a single a/N̄ fit over the scan is killed at χ²/ndof ≫ 100). The data are consistent with a **floor + c/N̄** form on the large-q platform:
> slack − 1 = s∞ + c/N̄,  **s∞ = 0.03296 ± 0.00011, c = 0.866 ± 0.029**  (fit on q ∈ {30,100}, χ² = 0.00)
Honest disclosure: the full fit over q ∈ {10,30,100} has χ²/ndof = 38.7 — the q=10 excess lies ~20% *below* the large-q 1/N̄ line (the decay toward the floor steepens at q ≲ 30); the q=30 point bulges 5.7σ above the 3-point line. The coefficient c is **measured, not derived** — it encodes the per-collision conditional variance ratio of (s(1−u·u_f), (1−μ)), which the moment channel does not close. **Out-of-sample q=150 (new, n = 1.5×10⁵): slack(150) = 1.03321 ± 0.00019 vs forecast 1.03332 ± 0.00011 → z = 0.49.** The no-floor power law (β = −0.081 over {30,100}) forecasts 1.0317 — **excluded at 6.5 SE** (pred 1.03168 ± 0.00013, combined prediction SE). The large-q flattening level is **≈ 1.033**; N̄ grows as ≈ (1+q)^{1.9–2.0} (measured N̄ = 1.40/4.37/18.7/114.8/1082/2368 at q = 0/3/10/30/100/150). HONEST ENGINE LIMIT: the registered q = 300 target is **unreachable on the frozen engine** — the 5×10⁴-step transport cap trips even at n = 3×10³ (residence N is heavy-tailed: max/N̄ ≈ 9.2 at q=200, std/N̄ = 0.75 vs the Poisson 1/√N̄ scale — itself a structural reason the 1/N̄ asymptotics fails); q = 150 (max/N̄ = 7.2, max ≈ 2.0×10⁴, 2.5× cap margin) is the largest cap-safe extension and the registered large-q point here.

**4. THE ND1 KILL — restated and tested: the kill does NOT fire on either branch.**
> Pre-registered (J00 ND1): *"a proven positive lower bound on the slack above the measured 1.06 (the 'nearly tight' claim is then capped and must be weakened), or an n=10⁷ measurement showing the q-large limit flattening above 1.05."*
- **Branch A (lower bound above 1.06): refuted.** The reachable family attains slack = 1.03376 ± 0.00010 at (τ₀=1, q=100) and **1.03321 ± 0.00019 at (1, 150)**: the observed minimum sits **269 SE (q=100) and ~86 SE (q=150, vs 1.05)** below the kill thresholds. No positive lower bound above 1.06 exists over the reachable (τ₀,q) family — thin intercepts, asymptotic floor, and the measured grid together give an infimum ≈ 1.0332.
- **Branch B (q-large flattening above 1.05): refuted.** Flattening level = 1 + s∞ ≈ 1.0330 ± 0.0001, **≈ 153 SE below 1.05** (fit) with the q=150 point itself 86 SE below 1.05. The thin-corner limit 16/15 = 1.0667 is the *joint* τ₀→0, q→∞ corner, NOT the q-large limit at fixed τ₀ — the order of limits is registered explicitly.
- **Verdict: the kill condition fails on both branches; the converse registers — the J05 bound is tight-asymptotic on this family.** slack ≤ 1.0405 at q ≥ 30 and ≤ 1.034 at q ≥ 100 (measured); exact limit 1 remains not machine-provable (no q = ∞ run); the empirical floor ≈ 1.033 is the honest cap, so the "nearly tight" claim is *strengthened*, not capped.

**5. Composite closed form — killed.** The task's candidate slack(τ₀,q) = 1 + s0(q)/(τ₀-scaled N-score) fails in every reading: (i) the naive 1 + s0/N̄ over the q-scan has χ²/ndof ≫ 100 (thin intercept finite, floor nonzero); (ii) the thin-anchored pure interpolation (S_thin−1)·N₀/(N₀+N̄) fails at the thick ends of the q-chains ((τ₀=2,q=3) at 58 SE; q=100 under-predicted by ~10² SE); (iii) the anchored two-parameter composite slack−1 = s∞ + (S_thin−1−s∞)·N₀/(N₀+N̄) is **killed by the measured grid**: best fits per chain have worst-point z = 18.8 (q=0), 59.1 (q=3), 165.2 (q=10) and χ²/ndof = 105/1038/11108. Structural reasons (measured): (a) the surface is **not a function of N̄ alone** — (τ₀=2,q=3) has slack = 1.0689 at N̄ = 13.97 while (τ₀=1,q=10) has 1.0701 at N̄ = 18.69, an ordering reversal vs N̄-monotonicity at 6.2 combined SE; (b) the q=0 chain is flat at 4/3−1 out to N̄ ≈ 0.2 then declines — one transition scale cannot do flat-then-cliff. The only composite that survives is the **floor-only large-q form** (slack−1 = s∞ + c/N̄, q ≥ 30: z = 0.00/0.00/0.49 at q = 30/100/150).

---

## 1. The taxonomy: R₁ vs the J05 slack — same object? (algebra, then engine)

**Definitions (all on the same sample).**
```
R_1   = E[D·ang]/(E[D]·E[ang])                    (m=1 closure ratio, J00 M4/L01)
      = 1 + Cov(D,ang)/(E[D]E[ang])               (definition form)
slack = E[D²]·E[ang²]/E[D·ang]² = 1/ρ0²           (J06 §3: EXACT, origin correlation)
CV_D² = E[D²]/E[D]² − 1,  CV_ang² = E[ang²]/E[ang]² − 1
```

**The exact link (one line of algebra):** ρ0² = (R₁E[D]E[ang])²/(E[D²]E[ang²]) = R₁²/[(1+CV_D²)(1+CV_ang²)], so
> **slack·R₁² = (1+CV_D²)(1+CV_ang²)** — machine-exact on every cloud (same ratio of the four estimators; registered as an algebraic identity, not a physics gate).

**Are they the same object? No — different limits, different status.**
- As τ₀ → 0: E[D·ang] = r₁(q)τ₀ + O(τ₀²) (L01, r₁ = (7/5)(1/2+q/4)), E[D] = τ₀(1/2+q/4) exact (Theorem 1), E[ang] = τ₀(1+q/3)+O(τ₀²) (K04): R₁−1 = (7/5)/[(1+q/3)τ₀] − 1 + O(1) — **diverges**; R₁ is the thin-channel pairing of the first moments.
- slack mixes only O(τ₀) moments → **finite** thin limit (§2).
- In the attainability toy (D = c·ang pointwise, J06 §4a): slack = 1 exactly while R₁ = E[ang²]/E[ang]² = 1+CV² > 1 — the two objects disagree qualitatively in the sharpness limit.

**Engine taxonomy** (z_ident = machine round-trip of the identity; z_Rforms = the two definitional forms of R₁; z_Rvel = R₁ via the velocity path E[Dv²]/(2E[D]E[ang]), hierarchy m=1 — all three at z < 5 on every cloud):

| cloud (τ₀,q) | R₁ ± SE | slack ± SE | z_ident / z_Rforms / z_Rvel | R₁τ₀(1+q/3)(5/7) |
|---|---|---|---|---|
| (0.02, 0) | 70.872 ± 0.193 | 1.33503 ± 0.00190 | 0.26 / ≪5 / ≪5 | 1.0125 |
| (0.02, 3) | 36.26 ± 0.26 | 1.20728 ± 0.00088 | ≪5 / ≪5 / ≪5 | 1.0359 |
| (0.02, 10) | 17.380 ± 0.029 | 1.16094 ± 0.00055 | ≪5 / ≪5 / ≪5 | 1.0759 |
| (0.05, 3) | 15.228 ± 0.020 | 1.21742 ± 0.00066 | ≪5 / ≪5 / ≪5 | 1.0877 |
| (0.5, 0) | 4.030 ± 0.005 | 1.30273 ± 0.00077 | ≪5 / ≪5 / ≪5 | 1.439 |
| (1, 0) | 2.646 ± 0.004 | 1.24296 ± 0.00061 | ≪5 / ≪5 / ≪5 | 1.890 |
| (1, 3) | 2.017 ± 0.002 | 1.13220 ± 0.00022 | ≪5 / ≪5 / ≪5 | 2.881 |
| (1, 10) | 1.711 ± 0.001 | 1.07014 ± 0.00012 | ≪5 / ≪5 / ≪5 | 5.295 |
| (2, 3) | 1.709 ± 0.001 | 1.06894 ± 0.00015 | ≪5 / ≪5 / ≪5 | 4.883 |

The R₁·τ₀-column shows the thin divergence law (→ 1+g(q)τ₀, g = 0.88/1.61/3.59 at q = 0/3/10, L01) crossing over to the thick regime (grows with τ₀).

## 2. The thin limit — sector structure, closed intercepts, N02 comparison

**Sector decomposition (T = 1 isothermal).** D = Σⱼ sⱼ(1 − uⱼ·u_f) telescopes (L01 lemma). N = 0: (D,ang) = (0,0) (atom spike: zero lag, zero width, contributes nothing); N = 1: D = s₁(1−μ), ang = (1−μ) — **D = s₁·ang pointwise on the slice**; N ≥ 2 enters all three slack moments at O(τ₀²). Hence E[D²], E[ang²], E[D·ang] are each O(τ₀) and the ratio is O(1):
```
slack(0⁺,q) = [P₁·E[s₁²]·(7/5)]·[P₁·(7/5)] / [P₁·E[s₁]·(7/5)]² = E[s₁²|N=1] / E[s₁|N=1]²
```
with s₁ collision-length-biased: P(ds₁) ∝ κ̃(s₁)ds₁, κ̃(s) = 1 + qs² (central: s ∈ [0,1]; P₁ = P(N=1)); E[(1−μ)²] = 7/5 cancels.

> **S_thin(q) = (1/3 + q/5)(1 + q/3)/(1/2 + q/4)²**   (q=0: 4/3; q=3: 448/375; q=10: 91/81; q→∞: 16/15)

**The N=2 correction is exact and positive** (why the approach is from above at q ≠ 0): on N=2 the last flight's (1−u₂·u_f) = 0 term drops, so D = s₁(1−μ₂), ang = (1−μ₁)+(1−μ₂), giving
```
E[ang²|2] = 2·(7/5) + 2 = 24/5,  E[D·ang|2] = E[s₁|2]·(1+7/5) = (12/5)E[s₁|2],  E[D²|2] = (7/5)E[s₁²|2]
⇒  slice slack|N=2 = (7/6)·E[s₁²|2]/E[s₁|2]²
```
so slack(τ₀) = S_thin(1 + εδ + …) with ε = P(N≥2)/P(N=1) ≈ τ₀(1+q/3)/2 — a **rise** (measured small-τ₀ slopes +2.2 at q=10, ≈ +0.6 at q=3, ≈ 0 at q=0), then higher sectors pull slack back down (1.0701 at (1,10); 1.0689 at (2,3)): **slack(τ₀)|q is non-monotone**. The q=0 chain is a flat shelf — 4/3 within ±0.2% out to τ₀ = 0.2 (N̄ ≈ 0.2) — with the decline beginning between N̄ ≈ 0.2 and 0.6.

**Engine table (central + volume thin grid, n = 3–10×10⁶ per point, jackknife SEs):**

| τ₀ | q=0 slack | q=3 slack | q=10 slack | R₁(q=0) |
|---|---|---|---|---|
| 0.002 | 1.33006 ± 0.00339 | 1.19616 ± 0.00233 | 1.12870 ± 0.00116 | 702.9 |
| 0.005 | 1.33364 ± 0.00333 | 1.19850 ± 0.00140 | 1.13504 ± 0.00096 | 278.8 |
| 0.01 | 1.33279 ± 0.00213 | 1.19962 ± 0.00117 | 1.14461 ± 0.00087 | 141.2 |
| 0.02 | 1.33503 ± 0.00190 | 1.20728 ± 0.00088 | 1.16094 ± 0.00055 | 70.9 |
| 0.05 | 1.33556 ± 0.00113 | 1.21742 ± 0.00066 | 1.19191 ± 0.00042 | 29.1 |
| 0.1 | 1.33089 ± 0.00132 | 1.23147 ± 0.00071 | 1.21099 ± 0.00060 | 15.3 |
| 0.2 | 1.33122 ± 0.00076 | — | — | 8.20 |
| 0.5 | 1.30273 ± 0.00077 | — | — | 4.03 |
| 1 | 1.24296 ± 0.00061 | 1.13220 ± 0.00022 | 1.07014 ± 0.00012 | 2.65 |
| 2 | — | 1.06894 ± 0.00015 | — | — |

| volume τ₀ | q=0 slack | q=3 slack |
|---|---|---|
| 0.002 | 1.57144 ± 0.01055 | 1.58609 ± 0.00586 |
| 0.005 | 1.56081 ± 0.00619 | 1.58381 ± 0.00289 |
| 0.02 | 1.56019 ± 0.00327 | 1.58352 ± 0.00239 |
| 0.05 | 1.56052 ± 0.00216 | 1.57167 ± 0.00167 |
| intercept S_vol | **1.5625 (25/16)** | **1.58356 (1715/1083)** |

(The q=0 volume chain sits on 25/16 from τ₀ = 0.005 with |z| ≤ 0.9; the volume q=3 chain approaches from *below* (slope −0.3/τ₀-unit) — the N=2 mixture flips sign by geometry.)

**Intercept fits** (weighted quadratic slack = I + aτ₀ + bτ₀² over τ₀ ≤ 0.02, q=0 also the flat shelf to 0.2; the quadratic absorbs the measured saturation of the O(τ₀) N≥2 mixture; the linear reference is reported too):

| q | I ± SE (quadratic) | S_thin | z (gate < 3) | linear I ± SE, z | a, b | χ²/ndof |
|---|---|---|---|---|---|---|
| 0 | 1.33450 ± 0.00147 | 1.33333 (4/3) | **0.79** | 1.33451 ± 0.00094, 1.25 | −0.016, ~0 | 7.5/5 |
| 3 | 1.19687 ± 0.00275 | 1.19467 (448/375) | **0.80** | 1.19446 ± 0.00133, 0.16 | +0.085, +21.8 | 0.5/1 |
| 10 | 1.12436 ± 0.00156 | 1.12346 (91/81) | **0.58** | 1.12624 ± 0.00083, 3.33 | +2.23, −19.8 | 0.0/1 |

**N=1 slice (engine-masked):** E[D|1]/E[ang|1] (≡ E[s₁|N=1], pointwise D = s₁·ang on the slice) vs (1/2+q/4)/(1+q/3) at τ₀ = 0.002: 0.4997 ± 0.0020 (z = 0.15), 0.6236 ± 0.0017 (z = 0.80), 0.6907 ± 0.0009 (z = 1.83) at q = 0/3/10; slice slack 1.3314/1.1953/1.1249 vs S_thin (z ≤ 1.3). The τ₀ = 0.02 rows show the measured O(τ₀) e^{−Λ} escape-bias shift (up to 1.5%, z up to 30 — the expected escape suppression of deep collisions; reported, not gated).

**Volume source — CLOSED rational intercept.** Same N=1 structure with chord geometry r(s)² = r₀² + 2s(r₀·u) + s² under volume-uniform × isotropic emission:
```
B1(q) = E[∫₀^{ch} s κ̃ ds] = E[ch²]/2 + q·(E[r₀²ch²]/2 + (2/3)E[(r₀·u)ch³] + E[ch⁴]/4)
                          = 2/5 + q·(8/35 − 12/35 + 12/35) = 2/5 + 8q/35        (= N02 c₀)
B2(q) = E[∫₀^{ch} s² κ̃ ds] = E[ch³]/3 + q·(E[r₀²ch³]/3 + E[(r₀·u)ch⁴]/2 + E[ch⁵]/5)
                          = 1/3 + q·(1/5 − 2/5 + 2/5) = 1/3 + q/5              (NEW constants)
P1(q) = E[∫₀^{ch} κ̃ ds]  = 3/4 + 5q/12                                        (N02 numerator)
```
with the exact quadrature constants (Legendre 2048², agreement 1e-9; N02 rows re-verified E[ch] = 3/4, E[ch²] = 4/5, E[ch³] = 1, E[ch⁴] = 48/35, E[r₀²ch²] = 16/35, E[(r₀·u)ch³] = −18/35, E[∫r²ds] = 5/12; **NEW: E[ch⁵] = 2, E[r₀²ch³] = 3/5, E[(r₀·u)ch⁴] = −4/5, E[∫s²r²ds] = 1/5**; E[ch⁵] MC-checked at n = 3×10⁷, z = 0.05):

> **S_vol(q) = B2·P1/B1² = (1/3 + q/5)(3/4 + 5q/12)/(2/5 + 8q/35)²**  (q=0: 25/16; q=3: 1715/1083 ≈ 1.58356; q=10: ≈ 1.59048; q→∞: 1225/768 ≈ 1.59505)

Engine intercept fits: q=0: 1.56190 ± 0.00407 (z = 0.15); q=3: 1.58738 ± 0.00236 (z = 1.62). (The naive r(s)² ≈ s² reading — denominator 2/5 + 12q/35 — is excluded at 33 SE by the q=3 point; the exact chord geometry with its r₀²/(p·u) terms is mandatory.)

**Comparison with N02's closed thin window** (all three closed thin objects, same sector machinery):

| object | what it is | q=0 | q=3 | q=10 | q→∞ | trend |
|---|---|---|---|---|---|---|
| N02 R_v(0,q) | ratio of *means* E[ang]/E[D] (volume) | 1.8750 | 1.8421 | 1.8307 | ~1.75 | decreasing |
| S_vol(q) (U05, NEW) | slack shape ratio (volume) | 1.5625 | 1.5836 | 1.5905 | 1225/768 | increasing |
| S_thin(q) (U05, NEW) | slack shape ratio (central) | 1.3333 | 1.1947 | 1.1235 | 16/15 | decreasing |
| measured thick slack (τ₀=1) | q-scan | 1.2430 | 1.1322 | 1.0701 | ≈ 1.033 | decreasing |

The window and the slacks are different observables with different q-trends; thick scattering always *tightens* the slack relative to its thin intercept.

## 3. The q → ∞ asymptotics

**q-scan (τ₀ = 1, central; q=0/3/10 at n = 1.2×10⁶, bit-identical to J06; q=30/100 re-run at the J06 seeds 8007/9007 — harness Δ = 2.3e-9 / 4.0e-9, 0.00 SE units; q=150 new at n = 1.5×10⁵ in three pooled 5×10⁴ chunks, seeds 10007/11007/12007):**

| q | N̄ | slack ± SE | slack−1 | ρ0 | std(N)/N̄ |
|---|---|---|---|---|---|
| 0 | 1.404 | 1.24296 ± 0.00061 | 0.24296 | 0.89696 | — |
| 3 | 4.373 | 1.13220 ± 0.00022 | 0.13220 | 0.93981 | — |
| 10 | 18.69 | 1.07014 ± 0.00012 | 0.07014 | 0.96667 | — |
| 30 | 114.8 | 1.04050 ± 0.00020 | 0.04050 | 0.98035 | — |
| 100 | 1082.5 | 1.03376 ± 0.00010 | 0.03376 | 0.98354 | — |
| 150 | 2368 | **1.03321 ± 0.00019** | 0.03321 | 0.98380 | 0.74 |

**Is slack − 1 linear in 1/N̄? No.** Local exponents β_eff = Δ ln(slack−1)/Δ ln N̄ between consecutive q's: −0.536 ± 0.003, −0.436 ± 0.002, −0.303 ± 0.003, −0.081 ± 0.003, **−0.021 ± 0.008** — the approach flattens decisively; a global slack−1 = a/N̄ fit over the scan is killed (χ²/ndof ≫ 100). A *derivable* 1/N̄ coefficient would require the per-collision conditional variance of (s(1−u·u_f), (1−μ)) — the moment channel's closed factors do not determine it (honest edge). The residence distribution is itself heavy-tailed (std/N̄ = 0.74 at q = 150, max/N̄ ≈ 7–9 at q = 150–200 vs the Poisson 1/√N̄ scale) — the structural crux: Var(N) ~ N̄^{α}, α > 1, spoils any naive CLT 1/N̄ reading of the correlation approach.

**Floor model** (slack−1 = s∞ + c/N̄):
- **large-q fit q ∈ {30, 100}: s∞ = 0.03296 ± 0.00011, c = 0.866 ± 0.029, χ² = 0.00**;
- full fit q ∈ {10, 30, 100}: s∞ = 0.03335 ± 0.00009, c = 0.689 ± 0.003, χ²/ndof = 38.7 — disclosed structure: the q=10 excess sits ~20% *below* the large-q 1/N̄ line (the decay toward the floor steepens at q ≲ 30); q=30 bulges 5.7σ above the 3-point line — the c coefficient only stabilizes at q ≳ 30;
- physical reading: ρ0 → 1/√((1+σ_D²/(a²κ))(1+σ_A²/(c²κ))) < 1 — a positive floor from the residual per-collision variance ratio in the (heavily) Poissonized walk: **slack∞ = 1 + s∞ ≈ 1.033**;
- **OUT-OF-SAMPLE q=150**: forecast (large-q fit) slack = **1.03332 ± 0.00011**; measured **1.03321 ± 0.00019** → **z = 0.49 ✓**; the no-floor power law (β = −0.081 over {30,100}) forecasts 1.03168 ± 0.00013 → excluded at 6.5 SE. **The flattening is real and it is at ≈ 1.033, far below 1.05.**
- N̄(q): 1.40/4.37/18.7/114.8/1082/2368 — ≈ (1+q)^{1.9–2.0} (the naive τ₀(1+q/3) N-score is unusable at τ₀ = 1; L01/K04 high-order terms dominate — the composite uses measured N̄ = E[N] = E[ang]).

## 4. THE ND1 KILL — restated, tested, honest verdict

Kill (J00 ND1, verbatim): *"a proven positive lower bound on the slack above the measured 1.06 (the 'nearly tight' claim is then capped and must be weakened), or an n=10⁷ measurement showing the q-large limit flattening above 1.05."*

| branch | test | result |
|---|---|---|
| A | 5-SE lower bound above 1.06 provable from the reachable (τ₀,q) family (thin intercepts + asymptotic floor + measured grid)? | **NO — refuted.** Family minimum = 1.03376 ± 0.00010 at (1,100); the new (1,150) point = 1.03321 ± 0.00019 (z = −269 vs 1.06 at q=100; the family minimum sits ≈ 138 SE below 1.06 even at n = 1.5×10⁵). The family's infimum over everything reachable is ≈ 1.0332. |
| B | q-large flattening above 1.05? | **NO — refuted.** Flattening level = 1 + s∞ ≈ 1.0330 ± 0.0001 (≈ 153 SE below 1.05); the q=150 point itself sits 86 SE below 1.05. The 16/15 thin-corner (τ₀→0, q→∞ jointly) is not the q-large limit — order of limits registered. |

**Kill verdict: the kill condition fails on both branches; the converse registers — the J05 bound is tight-asymptotic** (slack ≤ 1.0405 at q ≥ 30; ≤ 1.034 at q ≥ 100, with the q=150 platform at 1.0332; exact limit 1 not machine-provable; empirical floor ≈ 1.033 documented as the honest cap). No reachable configuration resurrects slack ≥ 1.06; the "nearly tight" claim is *strengthened*, not capped.

## 5. The composite closed-form candidate — killed (registered)

Candidate (task): slack(τ₀,q) = 1 + s0(q)/(τ₀-scaled N-score) + …, tested against the full measured grid (J06 clouds + the 35-point U05 grid incl. q=150):
1. **Naive 1 + s0/N̄** (single s0 over the q-scan): χ²/ndof ≫ 100 — killed (thin intercept finite; floor nonzero).
2. **Pure interpolation** (S_thin−1)·N₀/(N₀+N̄), thin-anchored, no floor: fails at the thick ends ((2,3) at 58 SE; q=100 under-predicted by ~10² SE) — **the floor term is mandatory** ("from (1)+(2)" in one sentence).
3. **Anchored two-parameter composite** slack−1 = s∞ + (S_thin−1−s∞)·N₀/(N₀+N̄), per-q (s∞, N₀) fitted on the chains (thin + mid + thick; s∞ clipped to [0, S_thin−1]):

| q | s∞ (best) | N₀ | χ²/ndof | worst point z |
|---|---|---|---|---|
| 0 | 0.000 | 4.18 | 734/7 = 105 | **18.8** |
| 3 | 0.000 | 8.15 | 6225/6 = 1038 | **59.1** |
| 10 | 0.000 | 25.0 | 55539/5 = 11108 | **165.2** |

**Killed at 19–165 SE per chain** — no two-parameter per-q closed composite represents the grid. Structural reasons (both measured): (a) the surface is **not a function of N̄ alone** — (2,3) [slack 1.0689, N̄ 13.97] vs (1,10) [1.0701, N̄ 18.69] reverse the N̄-order at 6.2 combined SE; (b) the q=0 chain is flat at 4/3−1 to N̄ ≈ 0.2 then declines — a single transition scale cannot do flat-then-cliff.
4. **What survives:** the **floor-only large-q composite** slack−1 = s∞ + c/N̄ (q ≥ 30): z = 0.00 / 0.00 / 0.49 at q = 30/100/150.

## 6. Honest edges

- Thin intercepts S_thin, S_vol: **derived** (N=1 sector, exact integrand at O(τ₀); e^{−Λ} corrections measured and understood). The *approach* structure (N=2 slice factor 7/6, slopes, peak, volume sign flip) is measured, not theorem-level.
- The new chord constants (E[ch⁵] = 2, E[r₀²ch³] = 3/5, E[(r₀·u)ch⁴] = −4/5, D₂ = 1/5) are pinned at 1e-9 by quadrature and MC-checked — not closed-form-proven.
- s∞ ≈ 0.033 and c ≈ 0.87 are **empirical** (the moment channel cannot close the per-collision conditional variance); the floor's existence is measured (flattening + OOS q=150); pinning s∞ to 1e-4 would need a q = 10⁴-class run.
- Non-monotone slack(τ₀)|q (bump) is real: any "slack decreases with τ₀" shorthand is wrong in the thin regime at q ≠ 0.
- **q=300 was NOT runnable on the frozen engine** (5×10⁴-step transport cap trips even at n = 3×10³; heavy-tailed residence max/N̄ ≈ 9.2 at q = 200, std/N̄ = 0.75). The large-q extension point is q = 150 at n = 1.5×10⁵ (SE ≈ 1.9×10⁻⁴ — decisive for every registered test; the n = 3×10⁵ spec was honored at q = 30/100). Registered as an engine limitation, not a physics claim.
- Not claimed: observational content, new laws of nature, novelty certificates. All statements live inside the frozen conservative Thomson-sphere model (J00 scope).

## 7. Registration

- **R₁ ≠ slack; exact link slack₁·R₁² = (1+CV_D²)(1+CV_ang²); R₁−1 diverges as (7/5)/[(1+q/3)τ₀] − 1 (re-verified), slack finite.** CLOSED here.
- **Thin slack intercepts — CLOSED rational curves, engine-verified at z ≤ 1.6:** central S_thin(q) = (1/3+q/5)(1+q/3)/(1/2+q/4)² (4/3, 448/375, 91/81 → 16/15); volume S_vol(q) = (1/3+q/5)(3/4+5q/12)/(2/5+8q/35)² (25/16, 1715/1083 → 1225/768). N02's window is a ratio-of-means object, not a slack (comparison registered).
- **q-large: slack−1 = s∞ + c/N̄ with s∞ = 0.03296 ± 0.00011, c = 0.866 ± 0.029 (q ∈ {30,100}; stabilized only for q ≳ 30); NOT linear in 1/N̄ with a derivable coefficient; q=150 out-of-sample z = 0.49; no-floor power law excluded at 6.5 SE.** N̄ ≈ (1+q)^{1.9–2.0} (measured). q=300 unreachable on the frozen engine (cap; heavy-tailed N) — registered.
- **ND1: kill fails both branches; slack ≤ 1.034 for q ≥ 100 (measured); tight-asymptotic registration; family infimum ≈ 1.0332; exact limit 1 not machine-provable.**
- Composite: naive 1+s0/N̄ killed; anchored per-q two-parameter composite killed (worst z = 19/59/165 per chain); N̄-alone dependence excluded (6.2 SE); floor-only large-q form survives at z ≤ 0.49.
- No git commit. J00–J06/L01–N02 untouched (append-only).