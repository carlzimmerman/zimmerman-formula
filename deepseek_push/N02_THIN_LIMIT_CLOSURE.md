# N02 — CLOSURE OF THE THIN-LIMIT VOLUME WINDOW (DEEP PRECISION)

**2026-09-23 · moment channel · volume source · CLOSED**
Files: `N02_thin_closure.py` (engine: `J02_moment_hierarchy`, instrumented thin
simulator + exact N=1-sector integrand by weighted MC, Legendre quadrature) ·
`N02_thin_closure.out` (exit 0 · **27/27 checks PASS**) · `N02_results.json`
(every number ± SE). No git commit (per lane rules).

---

## Bottom line

The thin-limit volume window is a **closed rational curve, gently decreasing in q**:

```
R_v(0,q) = (3/4 + 5q/12) / (2/5 + 8q/35)
         = 1.8750 / 1.8421 / 1.8307            at q = 0 / 3 / 10
```

and **every piece is now derived and machine-verified at deep precision**:

1. **c₀(q) = E[D]_vol/tau0 → 2/5 + 8q/35 is EXACT** (not "≈0.396…≈1.089…≈2.677").
   The closed form is confirmed by the deep grid over 18 points
   (τ₀ ∈ {1e-4 … 5e-3}, n = 1e7 at the two smallest τ₀, 4e6 else): per-point
   z against the form |z| ≤ 1.9 at *every* point; per-q weighted fits
   c₀(fit) = 0.4058 ± 0.0071 / 1.1024 ± 0.0119 / 2.6866 ± 0.0185, z =
   0.83 / 1.40 / 0.05. **No curvature**: at q=10 the √τ₀-term fits to
   d = −0.065 ± 0.459 (z = 0.007) and the three-deepest-point z = −0.26;
   the task's curvature branch (q=10 z>4) is NOT triggered.
2. **Derivation (N=1 sector, exact in τ₀):** D telescopes, D|N=1 = s₀(1−μ) with
   E[1−μ|N=1] = 1 + O(τ₀) (Thomson symmetry), and the first-collision
   length-bias — P(N=1) ≈ τ₀·E[ch], E[s₀|N=1] → E[ch²]/(2E[ch]) = 8/15 —
   gives c₀(q) = E[ch²]/2 + q·E[∫ s r²(s) ds] = 2/5 + 8q/35, with the
   geometry closed **exactly**: E[ch] = 3/4, E[ch²] = 4/5, E[ch³] = 1,
   E[ch⁴] = 48/35, E[r₀²ch²] = 16/35, E[(p·u)ch³] = −18/35, hence
   E[∫₀^{ch} s r²(s) ds] = 16/70 − 12/35 + 12/35 = 8/35 (quadrature
   agreement 1e-13; MC 0.228561 ± 4e-5). The exact N=1 integrand matches the
   engine masked at N==1 at z ≤ 0.9 (4 points), and its τ₀→0 extrapolation
   reproduces 2/5 + 8q/35 at c₀(sec) = 0.40008 ± 0.00023 / 1.08657 ± 0.00066
   / 2.68513 ± 0.00170 (z = 0.36 / 1.29 / −0.35).
3. **E[Q] thin (q=0) — the premised -6/25 is CORRECTED:**
   E[Q] = E[ch e^{−Λ₁}] + τ₀·B(τ₀) + O(τ₀²) with the N=0 piece exact
   (3/4 − (4/5)τ₀ + τ₀²/2 + O(τ₀³), E[ch³]=1) and B₀ := lim E[s₁·1{N=1}]/τ₀
   = **0.58092 ± 0.00013** (exact-sector value, no clean rational at 1e-4).
   Tangent slope dE[Q]/dτ₀ → −E[ch²] + B₀ = **−0.2191 ± 0.0001**, not −6/25
   (−0.24): the premised value would require B₀ = 14/25, excluded at z = 164
   of the sector value; L02's "−0.24" was the chord slope across τ₀ ≈
   0.05–0.1 (0.7378 at τ₀=0.05 reproduces the thin law at z ≈ 0.6), not the
   τ₀→0 tangent. The grid-fit slope −0.249 ± 0.053 is consistent with both
   (z = 0.6 / −0.2) — the discrimination is carried by the exact sector
   value — and the **full per-point thin law** E[ch e^{−Λ₁}] + τ₀·B(τ₀)
   reproduces all six grid values of E[Q] at |z| ≤ 1.2. E[Q] → 3/4 as τ₀→0
   (intercept fit 0.75010 ± 0.00010, z = 1.0). E[Q](q) slopes per q
   (measured-only): −0.249 ± 0.053 / −0.505 / −1.245.
4. **Verdict — gently DECREASING, closed form; "universal ≈ 1.86" is
   superseded.** The three curve values differ by construction (1.8% and
   2.4% drops) and every measured ingredient agrees with the closed form to
   ≤ 1.9σ; K07's own thin limits 1.893 ± 0.013 / 1.837 ± 0.006 / 1.837 ±
   0.008 are each within z ≤ 1.4 of the curve — "universal ~1.86" was a
   within-2σ summary of K07's c₀ values, and the deep grid now excludes the
   c₀ deviations it would require.

---

## 1. Deep-thin grid (P1)

All engine runs: volume source, κ(r) = τ₀(1+qr²), exact optical-depth
bisection (bit-identical kernels to J02; cross-checked thin-simulator vs
engine at (5e-3,10): z_D = −0.16, z_N = −1.71; Q ≡ (x−x₀)·u_f per-photon to
1e-15). c := E[D]_vol/τ₀, z := (c − c_form)/SE, c_form = 2/5+8q/35.

| τ₀ | q | n | c ± SE | z | E[Q] ± SE |
|---|---|---|---|---|---|
| 1e-4 | 0 | 1e7 | 0.42002 ± 0.0221 | +0.91 | 0.75015 ± 0.00015 |
| 1e-4 | 3 | 1e7 | 1.10055 ± 0.0369 | +0.40 | 0.74996 ± 0.00015 |
| 1e-4 | 10 | 1e7 | 2.74456 ± 0.0573 | +1.03 | 0.74972 ± 0.00015 |
| 2e-4 | 0 | 1e7 | 0.40785 ± 0.0155 | +0.51 | 0.74995 ± 0.00015 |
| 2e-4 | 3 | 1e7 | 1.13450 ± 0.0262 | +1.86 | 0.75014 ± 0.00015 |
| 2e-4 | 10 | 1e7 | 2.63870 ± 0.0397 | −1.19 | 0.74971 ± 0.00015 |
| 5e-4 | 0 | 4e6 | 0.40489 ± 0.0154 | +0.32 | 0.75001 ± 0.00024 |
| 5e-4 | 3 | 4e6 | 1.07640 ± 0.0254 | −0.37 | 0.74950 ± 0.00024 |
| 5e-4 | 10 | 4e6 | 2.64686 ± 0.0403 | −0.96 | 0.74916 ± 0.00024 |
| 1e-3 | 0 | 4e6 | 0.40460 ± 0.0109 | +0.42 | 0.74999 ± 0.00024 |
| 1e-3 | 3 | 4e6 | 1.09488 ± 0.0183 | +0.50 | 0.74910 ± 0.00024 |
| 1e-3 | 10 | 4e6 | 2.70362 ± 0.0286 | +0.63 | 0.74889 ± 0.00024 |
| 2e-3 | 0 | 4e6 | 0.39723 ± 0.0077 | −0.36 | 0.74944 ± 0.00024 |
| 2e-3 | 3 | 4e6 | 1.09317 ± 0.0129 | +0.58 | 0.74852 ± 0.00024 |
| 2e-3 | 10 | 4e6 | 2.69475 ± 0.0203 | +0.45 | 0.74745 ± 0.00024 |
| 5e-3 | 0 | 4e6 | 0.39592 ± 0.0048 | −0.85 | 0.74889 ± 0.00024 |
| 5e-3 | 3 | 4e6 | 1.08234 ± 0.0081 | −0.42 | 0.74768 ± 0.00024 |
| 5e-3 | 10 | 4e6 | 2.67831 ± 0.0128 | −0.58 | 0.74365 ± 0.00024 |

**No point deviates by more than 1.9 SE.** Weighted fits c = c₀ + c₁τ₀ over
the six depths per q:

| q | c₀(fit) ± SE | c₁ ± SE | z vs 2/5+8q/35 | χ² |
|---|---|---|---|---|
| 0 | 0.40585 ± 0.00708 | −2.11 ± 1.85 | **0.83** | 0.80 |
| 3 | 1.10238 ± 0.01187 | −4.09 ± 3.10 | **1.40** | 2.51 |
| 10 | 2.68663 ± 0.01850 | −1.28 ± 4.86 | **0.05** | 4.12 |

q=10 curvature probes: √τ₀-term d = −0.065 ± 0.459 (z = 0.007); mean z of the
three deepest points = −0.26. **The c₀(q) = 2/5 + 8q/35 form stands with no
curvature.** K07's fit-based c₀ (0.3962 ± 0.0028 / 1.089 ± 0.004 / 2.677 ±
0.011) and L01's (0.4030 / 1.0915 / 2.6976) are all consistent with the
closed form; the deep grid pins them to it at per-point ≤ 1.9σ.

## 2. Derivation of c₀(q) from the N=1 sector (P2)

**Telescoping (engine definitional D = τ − Q, Q = (x−x₀)·u_f):**
D = Σⱼ sⱼ(1 − uⱼ·u_f), so D = 0 on N=0, **D|N=1 = s₀(1−μ)** with μ = u₀·u₁
(per-photon check: E[D|N=1] ≡ E[s₀(1−μ)|N=1] to 0.2%). E[(1−μ)|N=1] = 1
exactly at leading order: the Thomson kick is symmetric (E[μ] = 0 and μ ⊥ all
first-flight geometry; the μ↔escape coupling enters only through e^{−Λ₂} at
O(τ₀)). The N=1 sector is exact in τ₀:

```
E[D 1{N=1}] = ∫ ρ du₀ ∫₀^{ch} s₀(1−μ) κ(y) e^{−Λ₁−Λ₂} ch ds₀ p(μ) dμ
```

The first-collision length-bias: the N=1 event is weighted by ∝ κ(y)·ds₀, so
the conditional first-flight mean is **E[s₀|N=1] → E[ch²]/(2E[ch]) = 8/15**
(not ch/2 = 3/8 — the naive "uniform-s₀" reading is the classic error), giving

```
c₀(q) = lim E[D]_vol/τ₀ = E[ch²]/2 + q·E[∫₀^{ch} s r²(s) ds] = 2/5 + 8q/35
```

Closed geometric constants (Legendre 512-pt, agreement 1e-13; MC cross-checks
at n = 3e7):

| object | value | rational |
|---|---|---|
| E[ch] | 0.750000000006 | **3/4** |
| E[ch²] | 0.800000000000 | **4/5** |
| E[ch³] | 1.000000000000 | **1** |
| E[ch⁴] | 1.371428571429 | **48/35** |
| E[r₀²ch] | 0.416666666672 | **5/12** |
| E[r₀²ch²] | 0.457142857143 | **16/35** |
| E[(p·u)ch³] | −0.514285714286 | **−18/35** |
| E[∫₀^{ch} r² ds] | 0.416666666672 | **5/12** (M05 re-verified) |
| **E[∫₀^{ch} s r²(s) ds]** | **0.228571428571** | **8/35** |

The q-geometry: ½·16/35 + (2/3)(−18/35) + ¼·48/35 = 8/35 − 12/35 + 12/35 =
**8/35**. (The (p·u)ch³ term is *not* zero — it is −18/35; dropping it, as a
naive μ-odd-symmetry argument would, leaves 0.5714 and falsifies the law.)

**Verification of the derivation:**
- Engine masked at N==1 vs the exact sector integrand (independent MC of the
  same quantity): |z| ≤ 0.9 at (0.02, 0/3/10) and (0.05, 10).
- Sector-integrand τ₀→0 extrapolation (weighted linear-in-τ over
  τ₀ = 1e-4 … 1e-3): c₀(sec) = 0.40008 ± 0.00023 / 1.08657 ± 0.00066 /
  2.68513 ± 0.00170 (z = 0.36 / 1.29 / −0.35) — the analytic limit at
  1e-3–2e-3 precision, confirming 2/5 + 8q/35 also at the "transition-free"
  sector level.
- Thin-simulator vs engine z_D = −0.16 / z_N = −1.71 at (5e-3, 10).

## 3. E[Q] thin expansion (P3) — correction registered

Sector decomposition (each term exact in τ₀, q=0):

```
E[Q] = E[Q 1{N=0}] + E[Q 1{N=1}] + O(τ₀²)
E[Q 1{N=0}] = E[ch e^{−Λ₁}] = 3/4 − (4/5)τ₀ + ½τ₀² + O(τ₀³)   [E[ch³]=1]
E[Q 1{N=1}] = τ₀·B(τ₀),  B(τ₀) = E[s₁ e^{−Λ₁−Λ₂} ch κ/τ₀]-sector,
B(τ₀) = 0.58070 / 0.58064 / 0.58072 / 0.57998 / 0.57914 / 0.57639
         at τ₀ = 1e-4 / 2e-4 / 5e-4 / 1e-3 / 2e-3 / 5e-3   (sector MC, s ≈ 2.4e-4)
B₀ := B(0) = 0.58092 ± 0.00013   (weighted linear-in-τ extrapolation)
```

(E[s₀μ·1{N=1}] = O(τ₀²): the μ-kick couples to the escape only through
e^{−Λ₂}.) The engine's own N=1 sector (E[Q·1{N=1}]/τ₀ per grid row) agrees
with B(τ₀) at z ≤ 1.7 per point. **Hence the thin tangent slope:**

```
dE[Q]/dτ₀ → −E[ch²] + B₀ = −0.8 + 0.58092 = −0.21908 ± 0.00013
```

- **The premised E[Q] = 3/4 − (6/25)τ₀ + O(τ₀²) is CORRECTED**: it requires
  B₀ = 14/25 = 0.56, excluded at z = 164 of the sector value. The "−0.24"
  (L02) was the effective chord slope between τ₀ = 0.05 and 0.1 — where the
  thin law gives E[Q](0.05) = 0.7368 vs L02's 0.7378 ± 0.0013 (z ≈ 0.6) —
  not the τ₀→0 tangent.
- The grid-fit slope −0.249 ± 0.053 is too weak to discriminate (−0.24: z =
  −0.18; −0.2191: z = 0.57) — the correction is carried by the exact sector
  value. The **full per-point thin law** E[Q] = E[ch e^{−Λ₁}] + τ₀·B(τ₀)
  reproduces all six grid values of E[Q] at |z| ≤ 1.2, and E[Q] → 3/4
  (0.75010 ± 0.00010, z = 1.0). No clean rational for B₀ at 1e-4 (a
  two-point chord-correlation object; candidates cluster ~0.5809 but nothing
  locks).
- Measured (only) per-q slopes of E[Q]: −0.249 / −0.505 / −1.245 at q = 0 /
  3 / 10.

## 4. The closed thin-window curve and the verdict (P4)

| q | numerator ⟨T⟩_q (exact, quadrature 1e-12; M05) | c₀(q) (closed) | **R_v(0,q)** | ± SE |
|---|---|---|---|---|
| 0 | 3/4 = 0.75 | 2/5 = 0.4 | **1.8750** | 0.0332 |
| 3 | 2 = 3/4 + 5·3/12 | 2/5 + 24/35 = 38/35 | **35/19 = 1.8421** | 0.0201 |
| 10 | 59/12 = 4.9167 | 2/5 + 80/35 = 94/35 | **2065/1128 = 1.8307** | 0.0126 |

(SEs by delta-method on the deep-grid c₀ fits: sR = R·s(c₀)/c₀; the numerator
has no SE.)

**Verdict: the thin-limit volume window is the closed rational curve
(3/4+5q/12)/(2/5+8q/35), GENTLY DECREASING in q (1.875 → 1.8421 → 1.8307, a
1.8%/2.4% drop over q = 0→3→10) — "universal ≈ 1.86" (K07) is superseded as a
within-2σ summary.** Evidence: (i) every measured ingredient agrees with the
closed form at ≤ 1.9σ (18/18 deep-grid points) and the c₀ fits at
z = 0.05–1.40; (ii) the denominator is now *derived* (length-biased first
collision, exact geometry, sector-verified to 1e-3), so the curve's q-slope
is exact; (iii) K07's own thin limits (1.893 ± 0.013 / 1.837 ± 0.006 / 1.837
± 0.008) sit within z ≤ 1.4 of the curve — the "universal" reading required
c₀ deviations (c₀(0) below 2/5, c₀(10) below 2/5+80/35) that the deep grid
now excludes; (iv) the numerator/slope of the window at τ₀→0 (3/4+5q/12) was
already exact (M05). The thin end of the volume window is a strictly
decreasing rational curve with endpoints 1.8750 (q=0) and 1.8307 (q=10);
both stay below K07's high-side bound 2 and above the central window's low
edge 4/3.

## 5. Registration

- **c₀(q) = 2/5 + 8q/35: CLOSED (derived + deep-verified).** Supersedes the
  measured K07/L01 c₀ tables; the K07 fit values remain consistent.
- **E[D]_vol thin = τ₀(2/5 + 8q/35)(1 + O(τ₀)) with no √τ₀ or τ₀-curvature
  detected on [1e-4, 5e-3].**
- **E[Q] thin: E[ch e^{−Λ₁}] + τ₀·B(τ₀), B₀ = 0.58092 ± 0.00013, tangent
  slope −0.2191(1); 3/4 − (6/25)τ₀ CORRECTED** (z = 164). The L02 kill
  condition (3-SE reproduction of its 18-point table) is unaffected for the
  values themselves — the thin law reproduces its small-τ₀ rows — but any
  "−6/25" use must be replaced by −(4/5 − B₀).
- **Thin window: R_v(0,q) = (3/4+5q/12)/(2/5+8q/35), DECREASING, closed
  form; K07 "universal ~1.86" downgraded to a within-2σ summary.**

All checks: 27/27 PASS (deep z's ≤ 1.9; sector-engine mask z ≤ 0.9; sector
limits z ≤ 1.3; E[Q] per-point full law |z| ≤ 1.2; slope-correction recorded;
thin-sim ⇔ engine cross-check z = −0.16; Q ≡ X per-photon 1e-15).