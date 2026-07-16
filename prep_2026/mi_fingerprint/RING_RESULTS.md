# RING-BY-RING SPARC CONFRONTATION — MI exactness vs QUMOND radius mixing under the framework ν (Lane CC, 2026-07-16)

**Script:** `ring_by_ring.py` (this directory; exit 0, 7/7 validation checks; output banked as `ring_by_ring.out`).
**Data (READ-ONLY):** 175 SPARC rotmod files + `SPARC_Lelli2016c.mrt` + `sparc_master_clean.csv` at `zimmerman-formula/real_research/data/`.
**Framework (NOT standard MOND):** dS-Unruh modified inertia; ν(y) = √(1+1/y), y = g_bar/a₀; a₀ FIXED (no fit): canonical 9.36e-11 m/s² (cH_Λ/Z) and alt 1.13e-10 m/s² (ρ_total/cH0) — both run everywhere. Zero fitted parameters in every statistic.
**Pre-flight (memory rule):** `real_research/rar_framework_a0_mlfit.py` re-run 2026-07-16 → 0.108 dex @ Υ=0.70 at canonical a₀, beats reg-MOND 0.122 @ Υ=0.5. Confirmed before any verdict below.

## 1. What was confronted

- **MI prediction (the framework's, derived — Lane RB Theorem A):** g_obs(R) = ν(g_bar/a₀)·g_bar(R) exactly ring-by-ring ⇒ E[δ_inner − δ_outer] = 0 to <3e-7 dex (i.e. zero), δ = log₁₀g_obs − log₁₀[ν g_bar].
- **MG prediction (same ν, no strawman):** QUMOND, lap Φ = div[ν(|∇Φ_N|/a₀)∇Φ_N], solved by the rb1-validated multipole phantom-density method (Plummer spherical control 1.3e-5) on 27 Miyamoto–Nagai disk configurations (B/A = 0.1/0.2/0.3 × 9 depths), mapped per galaxy by a profile-matched proxy (A_eff from the V-peak radius, depth anchored at the galaxy's own y(2.2R_d)), zone-averaged with **identical zones and weights** as the data. Stated systematic = thickness bracket + anchor-radius variants (a y-collapse mapping was tested, shown to fail — deviation is a function of (R/A, depth), not local y — and excluded, transparently, from the systematic).
- **Sample (pre-declared, Chae-2022-comparable):** Q∈{1,2}, i≥30°, UGC06787 removed → **152 galaxies** (matches Chae exactly). Υ_disk = 0.5 primary (Chae's value; Υ_bul = 1.4Υ_d), 0.7 variant (repo mlfit best fit), 0.4–0.8 scan. Zone splits: **A** = Chae's median transition 2.6R_d; **B** = slope-based rising/flat (all-inner fractions 7%/25% vs Chae's ~30%; his per-galaxy visual table is unpublished, so both proxies are reported). Galaxy statistic D = weighted-mean(δ_inner) − weighted-mean(δ_outer), ≥3 points per zone (N=114 both-zone galaxies), significance by 10⁴ galaxy bootstrap.

## 2. The QUMOND correction (computed, not asserted)

The same ν on a flattened disk produces a **signed inner/outer split**: inner rings suppressed (−1 to −2% at high y), outer rings enhanced (+2–3% at y≲0.5), zero in spherical symmetry. Zone-averaged over the real SPARC radii/weights this gives

**D_MG = −0.024 to −0.027 dex (±0.008 systematic)** in every configuration — same sign and same order as Chae's measured inner–outer offset (−0.021 ± 0.0045 dex). MI predicts **0**. The discriminant gap is therefore only ≈0.026 dex.

## 3. Ring-by-ring result (zero free parameters, both footings)

Main grid, D̄ = mean(δ_inner − δ_outer) [dex], plain-mean statistic (pre-declared):

| footing | Υd | split | N | D̄ ± σ_boot | D_MG | z_MI | z_MG | prefer |
|---|---|---|---|---|---|---|---|---|
| canonical | 0.5 | A | 114 | +0.0024 ± 0.0107 | −0.0262 | **+0.2** | +2.1 | **MI** |
| canonical | 0.5 | B | 65 | +0.0304 ± 0.0129 | −0.0253 | +2.4 | +3.7 | MI |
| canonical | 0.7 | A | 114 | −0.0269 ± 0.0106 | −0.0251 | −2.5 | **−0.1** | **MG** |
| canonical | 0.7 | B | 65 | +0.0033 ± 0.0132 | −0.0239 | +0.2 | +1.8 | MI |
| alt | 0.5 | A | 114 | +0.0091 ± 0.0105 | −0.0267 | +0.9 | +2.7 | MI |
| alt | 0.5 | B | 65 | +0.0372 ± 0.0124 | −0.0259 | +3.0 | +4.3 | MI |
| alt | 0.7 | A | 114 | −0.0194 ± 0.0103 | −0.0258 | −1.9 | +0.5 | MG |
| alt | 0.7 | B | 65 | +0.0107 ± 0.0128 | −0.0248 | +0.8 | +2.4 | MI |

Robustness at (Υ=0.5, split A), both footings: S/N≥10, bulgeless & L<1e11 (N=80; Chae's robust subsample), inner floors R>1 kpc and R>0.5R_d — **all ten variants keep D̄ ≥ 0 (MI-side); none reproduces the QUMOND-negative**.

Υ-scan (canonical, split A): D̄ slides ≈ −0.015 dex per +0.1 in Υ_d (+0.022 at 0.4 → −0.038 at 0.8), crossing the MI value near Υ=0.5 and the MG value near Υ=0.7.

## 4. Chae-style statistic recomputed with the framework ν at zero free parameters

Pooled error-weighted orthogonal residuals from the fixed-a₀ framework curve (Chae fitted a₀ per part and used the simple IF; only the inner−outer **difference** is comparable):

| config | inner | outer | diff | signif |
|---|---|---|---|---|
| canonical, 0.5, A | +0.051 | +0.091 | **−0.039 ± 0.015** | 2.6σ |
| alt, 0.5, A | +0.038 | +0.063 | **−0.025 ± 0.015** | 1.7σ |
| canonical, 0.7, A | −0.038 | +0.027 | −0.065 ± 0.016 | 4.2σ |
| alt, 0.7, A | −0.050 | +0.001 | −0.051 ± 0.015 | 3.4σ |
| (split B, any Υ/footing) | — | — | −0.021…+0.006 ± 0.024 | ≤0.8σ |

Chae 2022 published: inner −0.031±0.004, outer −0.010±0.002, diff −0.021±0.0045 (his v2 "5.1σ"; abstract "6.9σ taken at face value"). **Our pooled diff reproduces his sign and magnitude within errors** (−0.039±0.015 and −0.025±0.015 at his Υ=0.5 vs his −0.021±0.0045) but at 1.7–2.6σ, not 5–7σ: with a₀ fixed (no per-part fit) and the framework ν, the significance drops by ~3× — consistent with his own fixed-a₀ variant dropping 5.1σ→3.9σ, and with trap 6 (IF-reference leakage).

**Decisive diagnostic (the flip):** the pooled (point-precision-weighted) statistic and the equal-galaxy statistic **disagree in sign on the same residuals** (canonical, 0.5, A): pooled −0.039±0.015 vs per-galaxy equal-weight +0.001±0.009. Isolation shows the driver is **precision weighting alone** — not the all-inner galaxies (both-zone-only pooled: −0.043) and only mildly luminosity (high-L D̄ = −0.005±0.012, low-L +0.010±0.017, each null). The inverse-variance-weighted per-galaxy mean lands at −0.021±0.010 (canonical) — Chae's number — but at the **alt footing it is −0.006±0.010, null**: the precision-weighted MG-lean at canonical a₀ contains an a₀-level component (fixed-low a₀ biases outer residuals up more than inner), not pure disk geometry.

## 5. Verdict, straight

1. **Under Chae's own conventions (Υ=0.5), the pre-declared per-galaxy statistic prefers MI-exactness on both footings** (z_MI = 0.2/0.9 vs z_MG = 2.1/2.7), and all ten robustness variants hold that sign. This is the first run of this test with ν=√(1+1/y) and a fixed horizon a₀, and it does **not** reproduce Chae's anti-MI verdict at his M/L.
2. **The preference is not robust — it inverts within the plausible systematics.** At Υ_d=0.7 (the repo's own best-fit M/L for canonical a₀) the same statistic lands exactly on the QUMOND prediction (z_MG = −0.1) and 2.5σ from MI. Precision weighting alone flips the Υ=0.5 result to Chae's value on the canonical footing. Zone-split B flips it positive (+2–3σ *above* MI — a direction neither template predicts, flagging the split definition itself as a systematic).
3. **The honest bottom line:** the MI-vs-MG geometric discriminant on SPARC is |D_MI − D_MG| ≈ 0.026 dex, while the in-hand systematic sliders move the measured D̄ by more than that (Υ ±0.1 → ∓0.015; weighting scheme → −0.023; split definition → +0.028; footing → +0.007). **SPARC rotation curves at fixed Υ cannot presently decide between exact ring-by-ring MI and QUMOND-with-the-same-ν**; Chae's 5–7σ is not reproduced at zero free parameters (we get ≤2.6σ pooled, ~0σ per-galaxy at his Υ), and neither is an MI "win" claimable — the Υ=0.7/precision-weighted readings sit on the MG template. This lands between Chae 2022 (MG at 6.9σ) and Desmond+ 2024/Famaey–Durakovic 2025 ("slight preference for the straight algebraic relation... not with high significance"), and closer to the latter.
4. **What would decide it:** an independent per-galaxy Υ (population-synthesis priors at 3.6μm are ±0.1 — exactly the degeneracy width), or the statistic run on data whose inner points carry honest noncircular/beam error budgets (BIG-SPARC-class), or the frequency/eccentricity fingerprints (Lanes RB2/RB3) that MG cannot mimic at all.

**Caveats (named, no gloss):** the framework's own MI prediction for inner zones is the bare algebraic law only for circular tracers; the Lane-RB3 closure fork allows a signed non-circular correction (Milgrom-2023-type, same sign as Chae's signal) that is not computed per-galaxy here — the bare-algebraic MI verdict is what is scored, and it happens to be the *favored* template at Υ=0.5, so the correction is not needed to rescue anything. The MG template is a Miyamoto–Nagai proxy, not each galaxy's true baryon geometry (stated systematic ±0.008 dex; AQUAL differs from QUMOND by further ~0.1–1%). Chae's per-galaxy visual zone table is unpublished, so his split is approximated two ways. The EFE is not modeled (a mean-field EFE would push both zones, mostly outer, down — it cannot manufacture the D̄ ≈ 0 observed at Υ=0.5, but a per-galaxy EFE run via `sparc_efe_real_externalfield.py` remains open ground).
