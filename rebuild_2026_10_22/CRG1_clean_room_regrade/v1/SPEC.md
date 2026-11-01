# CRG1 SPEC: scorecard definitions for a clean-room rebuild

Governing documents: `FROZEN_CRITERIA.md` of this lane (you have it), and FG1's criteria as restated in section 1. Build from this file and `inputs/` only. Read no repo code, result, README or output. Import nothing from the repo.

No result number of any candidate appears here. Numbers below are constants, inputs, sample sizes and thresholds.

κ = ½ is FITTED. T is LOCATED, not derived. Cold dark energy is a gravitating field component, never a particle. Nothing here says the data favour the framework.

Run: one thread, nice 15, under 1 GB. Python with numpy, scipy, astropy is assumed. Use `np.trapz`-equivalent trapezoid rules where a rule is named. Bootstraps use numpy's `default_rng` (PCG64) with the stated seeds and draw order.

---

## 0. Notation and constants

**Each path keeps its own constants, as in the record.** They differ in the fourth digit, and rebuilding with one set would be a small departure, so use the set named per path.

| Set | G (SI) | M☉ (kg) | Mpc (m) | pc (m) | Used by |
|---|---|---|---|---|---|
| **E** | 6.67430e-11 | 1.98847e30 | 3.0857e22 | 3.0857e16 (`PC2 = pc²`) | SPARC, LITTLE THINGS, Σ_core unit conversion |
| **F** | 6.674e-11 | 1.989e30 | 3.0857e22 | 3.0857e16 | cluster lensing grid and prediction, `KG_PC2 = M☉/pc²` |
| **T** | 6.67430e-11 | 1.98847e30 | 3.0856775814913673e22 | | turnaround radius r_ta only |
| **P** | 6.674e-11 | 1.989e30 | | kpc = 3.0857e19 | groups |
| **D** | 6.67430e-11 | 1.98847e30 | 3.0856775814913673e22 | 3.0856775814913673e16 | dwarfs (Dw) |
| **L** | Gpc = 4.30091e-3 pc (km/s)²/M☉ | | | a0 in (km/s)²/pc = a0·3.0857e16/1e6 | KiDS lensing |
| **Z** | 4.30091e-9 Mpc (km/s)²/M☉ | | | | zoom measurement |

SPARC's conversion from kpc to m is `KPC = 3.0857e19`. LITTLE THINGS' `R[m] = R[kpc]·3.0857e22/1e3`.

**Footings.** a0 canonical = 9.3603e-11, alt = 1.1312e-10 m/s². Canonical is primary, alt is reported, never pooled.

**Backgrounds.** `A_c2b_refit`, `B_cfg886_bg`. Parameters in `inputs/scalars.json → backgrounds.<tag>.params`. Linear P(k), D(z) in `inputs/background/class_<tag>.npz`, from CLASS at those parameters [INPUT AS GIVEN]; `sigma8` in the JSON is a check (K-S below).

**Native values for the cluster path.** Ω_m = 0.2976016, h = 0.6856427, ω_b = 0.0223081. Ω_b = ω_b/h². `R_nat = (Ω_m − Ω_b)/Ω_b`. Cold share `f_c = R_nat/(1 + R_nat)`.

**The a0 law.** `ν(y) = ½ + √(¼ + 1/y)`, `g = ν(g_N/a0) g_N` where g_N > 0, else `g = g_N`.

**Core mass functions.**
- Burkert: `B_B(x) = ln(1+x²) + 2 ln(1+x) − 2 arctan x`. `B1 = B_B(1) = 3 ln 2 − π/2`.
- Smooth core: `B_S(x) = 4 (arcsinh x − x/√(1+x²))`.
- In either case `M(<r) = π S r0² B(r/r0)`, where S = ρ0 r0 is the core surface density.

**`solve_r0(M, R, S, B)`.** Let `lm(l) = ln[π S e^{2l} B(R/e^l)]`. Maximise lm over l in [ln(R·1e-6), ln(R·1e3)] by bounded scalar minimisation, x tolerance 1e-10, giving l_pk. If lm(l_pk) < ln M, return e^{l_pk} (saturated: count it). Otherwise return the compact root: solve lm(l) = ln M by Brent on [ln(R·1e-7), l_pk], x tolerance 1e-14.

**R200.** `R200 = (3 M200 / (4π·200 ρ_c))^{1/3}`, `ρ_c = 3 (100 h·1e3/Mpc)² / (8πG)` at z = 0, with h of the background in hand.

**Halo mass map, "EM1 map".** `lg M200[M☉] = a + b (lg M_b − 10)`, with a, b per background from `scalars.json` (`em1_map_a`, `em1_map_b`) [INPUT AS GIVEN].

### 0.1 Σ_coll, the collapse surface density

On a background tag, from `class_<tag>.npz`:
- `Ω_m = Omega_m_class`, `ρ_m0 = Ω_m · 2.775e11 h²` (M☉/Mpc³).
- `σ²(M)`: `R = (3M/(4π ρ_m,σ))^{1/3}·h` (Mpc/h), where `ρ_m,σ = Ω_σ·2.775e11 h²`, `Ω_σ = (ω_b + ω_cdm)/h² + Omega_nu`. `σ² = ∫ k³ P(k) W(kR)²/(2π²) d ln k` by the trapezoid rule over the file's k grid (h/Mpc), with W the top hat.
- Tabulate `σ²` at `lg M = linspace(7.0, 16.5, 191)`. Interpolate linearly in lg M, clamped at the ends.
- `S_q(M) = √max(σ²(M/2) − σ²(M), 0)`. `D_f = 1.686 / (1.686 + 0.974 S_q)`.
- If D_f ≥ 1, `z_f = 0`. Otherwise `z_f` is the linear interpolation of −D_f in (−Dg, zg).
- `ρ = 18π² ρ_m0 (1+z_f)³`. `r_f = (3 (M/2)/(4πρ))^{1/3}`. `Σ_coll(M) = ρ r_f / 1e12` in M☉/pc².

### 0.2 η tables

Interpolation of c_f is linear in lg M over nodes [12, 13, 14], flat outside. Call it cf(M).

| Rule | Definition | Where |
|---|---|---|
| **η_N(M)** native | `(4/(3 B_S(1))) cf(M)^{5/4}`, cf from the NR2 table | C1, C2, on S, Tl, LT, G, and C2's K, X |
| **η_C3(M)** | `(4/(3 B1)) cf(M)^{5/4}`, `cf` nodes `L·c_i/c_14`, c_i = `x48_A2_cf`, L = 7.082 | C3, on S, G, Ln |
| **η_A2(M)** | `(4/(3 B1)) cf(M)^{5/4}`, cf nodes `x48_A2_cf` | C4's Ln reference, H2H only |
| **A3 table** | `(4/(3 B_S(1))) cf^{5/4}`, cf nodes `ce1_a3_cf.<fs>` | C1's cluster fallback only (section 4.4) |

**NR2's table.** c_f(1e13), c_f(1e14) in `scalars.json → nr2.cf_table` [INPUT AS GIVEN, ng 64 stacks not supplied]. For 1e12: `c_f = 4 (η12/10.82)^{0.8}`. Low-mass ratios: `ρ10 = median η(1e10)/η12`, `ρ11 = median η(1e11)/η12`. η12 is the anchor, see AMBIGUITY A1.

**Native S, no floor.** `M_t` is the total mass:
`S_N(M_t) = f_c η_N(M_t) Σ_coll(M_t) · 10^{interp(lg M_t; [10,11,12]; [lg ρ10, lg ρ11, 0])}` (M☉/pc², clamped interp), then × M☉/PC2 with set E for kg/m². Σ_coll on the background in hand. On SPARC, LT and groups, `M_t = M200/f_c`, and in clusters `M_t = (M_fair + M_bt)/M☉`.

**Harness S, with floor.** `S_H(M) = max(a0/(2πG_E), η(M) Σ_coll(M)·M☉/PC2)`, set E. Halo-branch flag `above = M > 10^T`, T = 12.3 for C3. C3's floor is a disclosed departure (FG1's criteria).

### 0.3 Zoom re-estimates

Snapshots: `inputs/zooms/`, with `x` in physical Mpc as **float32** [reduced from float64, INPUT AS GIVEN], `m` (M☉), `meta`. Velocities are dropped.

**Centre.** `c = mean(x)`, `r = max|x−c|`. Loop: select |x−c| < r; if under 100 selected, return c; `c = mean(selected)`; `r ← 0.8 r`.

**Measure at z_f**, for the η files. `ρ_m = Mf/((4/3)π qM³)·(1+zf)³`. Sorted radii r, `Menc = n·m`, `dens = Menc/((4/3)π r³)`. `r_vir = r[max i: dens ≥ 18π²ρ_m]`; none means flagged. `r_conv = max(3 eps, r[199])`; flagged if r_conv ≥ r_vir/2. Bins: 24 log bins r_conv to r_vir; flagged if fewer than 8 non-empty. NFW fit: over c in `linspace(1, 30, 581)`, minimise `Σ [ln(μ(c r/r_vir)/μ(c)) − ln(Menc/Menc_last)]²` over particles with r_conv ≤ r ≤ r_vir, where `μ(y) = ln(1+y) − y/(1+y)`. This gives c.

**η from c.** `xs = geomspace(0.001, 1, 20001)`, `Ms = μ(c xs)` (unnormalised). `q = linspace(Ms[0], Ms[-1], 2000)`, `u = interp(q, Ms, xs)`, `y = ln(q/Ms[-1])`. Over a in `geomspace(0.5, 60, 2001)`, minimise `Σ [ln(B_S(a u)/B_S(a)) − y]²`. `η = (4/3) a²/B_S(a)`.

Median over seeds per mass. The per-seed values on record are `scalars.json → nr2.per_seed_eta`: use them as a known-answer check, and report the largest difference (float32 storage may move them slightly).

**Shape stack**, for `zooms/shape`. Grid `X = geomspace(1e-3, 40, 500)`. Per snapshot, at z (the file's z; for a `_zf_as_z0.50` file, `meta.zf`): `ρ_c(z) = 3 H0² (Ω_m(1+z)³ + 1 − Ω_m)/(8π G_Z)`, native Ω_m, `H0 = 100 h`, native h. `thr = 200 ρ_c(z)`. With r, Menc, dens as above, `i = max{dens ≥ thr}`. If i is the last particle, `R200 = r[i](dens[i]/thr)^{1/3}`; otherwise interpolate ln r linearly in ln dens between i and i+1 at ln thr. `M200 = thr (4/3)π R200³`. `x_conv = 3 eps/R200`. `x_edge = r[⌊0.9N⌋−1]/R200`.
`lnm(X) = interp(ln(X R200), ln r, ln Menc) − ln M200`. For `X < x_conv`, replace by `lnm(x_conv) + 2 ln(X/x_conv)`.

Stack per (mass tag, z tag): pointwise median of lnm, median lg M200, minimum x_edge. Mass tags 1e13 (ng 64, 9 seeds), 1e14, 1e15 (ng 80, 6 seeds each). z tags 0.00, 0.25, 0.50.

---

## 1. Candidates and lines

| | Architecture | SPARC-type rows | Cluster rows |
|---|---|---|---|
| **C1** | Native N, no response | Section 2.2, `S_N`, smooth core | Section 4.4, the zoom profile, gas +0.005 |
| **C2** | N + Blumenthal response | Section 2.3 | Section 4.5, smooth core + response, gas +0 |
| **C3** | Basin split: law below T 12.3, halos above | Section 2.4; Tl, LT = C4's law values | Same as C1 |
| **C4** | The law alone | Section 2.5 | Section 4.6 |

C1 and C2 are graded at canonical only ("footings coincide": no a0 enters except in the C* normaliser, see A9). C3 and C4 are graded at both footings.

**Pass rules.**
| Line | Pass |
|---|---|
| **S** | on both backgrounds, `rms ≤ 0.110` and `0.50 ≤ Υ_med ≤ 0.80` |
| **Tl** | on both, `|Υ(V<100) − Υ(V>150)| ≤ 0.15` |
| **LT** | on both, `|median E| ≤ 0.10` |
| **G** | class CONSISTENT |
| **K** | all 15 keys `|Z| ≤ 2` in both h cells |
| **X** | `|mean| ≤ 0.05` and `rms ≤ 0.10`, or NOT GRADED |
| **Ln** | C3, C4: `Δχ²(ENV2H − L2H) ≤ 9` and `Δχ²(ENV2H − H2H) < 0`. C1: class is not LAW |
| **Dw** | every class `|Z| < 2` |

**Per-candidate verdict.** FAILS with failed lines listed, or PASSES EVERY GRADED LINE with NOT GRADED lines listed. Tier C lines enter the verdict from the traced value in COMPARE. Overall: ROUTE E SURVIVES if C1 or C2 passes every graded line, otherwise ROUTE E DOES NOT SURVIVE ON MEASURED DATA. Tag [GAS-CONDITIONAL] if C1's K at f* 0.034 and at f* 0.0615 is 15 of 15 at gas +0.111. The implementer computes K and X only, and leaves the verdict to COMPARE.

### Tiers after tracing

| Line | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| S, Tl, LT | A | A | A | A |
| K | A | A | A (= C1's row) | A |
| X | A | A | A (= C1's row) | NOT GRADED: the harness has no X-COP row. Older value traced |
| G | B | C (B's scope excludes it; the equations are in 3.3 if wanted) | B | B |
| Ln | B (section 5.4) | C (FG1 reads C1's value) | B | B |
| Dw | B (section 6.3) | NOT GRADED | B | B |
| MW, DM, IC | C | C | C | C |

C2 closes for Tier A: its response is fully specified in section 2.3.

---

## 2. SPARC: S and Tl

### 2.1 Data and fit

`inputs/sparc/rotmod/*_rotmod.dat`: 175 files. Columns R (kpc), Vobs, eV, Vgas, Vdisk, Vbul. `inputs/sparc/SPARC_Lelli2016c.mrt`: split a line on whitespace; lines with exactly 19 tokens are data rows. Name = token 0. Fields in order, tokens 1 to 17: T, D, eD, fD, Inc, eInc, L36, eL36, Reff, SBeff, Rdisk, SBdisk, MHI, RHI, Vflat, eVflat, Q. (`L36`, `MHI` in 1e9 units.) Expect 175.

Set E. Υ grid: 0.30 to 1.20, step 0.01, rounded to 2 decimals. Per point and Υ:
- `V_B² = sign(Vgas) Vgas² + Υ Vdisk² + 1.4 Υ Vbul²` (km/s)². `g_B = V_B²·1e6/R`. `g_O = (Vobs·1e3)²/R`, R in m.
- Mask `OK`: g_B > 0, g_O > 0, finite g_B, Vobs > 0. The mask depends on Υ.
- Weight `W = 1/(max(eV,1)/max(Vobs,1))²`.
- `lg M_b = log10[(0.5 L36 + 1.33 MHI)·1e9]`.

**Fit.** For a model `g_p(point, Υ)`: `r = log10 g_O − log10 max(g_p, 1e-300)`; `wr2(Υ) = Σ_OK W r²`, `ws(Υ) = Σ_OK W`. Best Υ = argmin of wr2/ws (first minimum on the ascending grid). Keep wr2, ws, Υ at the best.

**Statistics.** `rms = √(Σ_gal wr2 / Σ_gal ws)`. `Υ_med` = median over galaxies of best Υ.

**Tilt.** Tokens as above: `Inc`, `Vflat`, `Q`. A row counts as parsed for tilt if it has at least 18 tokens and these three convert. Quality set: `Q ≤ 2` and `Inc ≥ 30`. `lo`: quality and `0 < Vflat < 100`. `hi`: quality and `Vflat > 150`. `tilt = median Υ(lo) − median Υ(hi)`. Expected: 153 in quality, 47 in lo, 53 in hi.

Per-galaxy Υ for tilt in C1, C2 uses halo pull with `B(min(R, R200)/r0)`, and the S statistic with `B(R/r0)`; see A4.

### 2.2 C1, both backgrounds, canonical

`M200` from the EM1 map. R200 at the background's h, set E. `S = S_N(M200/f_c)`. `r0 = solve_r0(M200 M☉, R200, S, B_S)`. `g_p = g_B + G π S r0² B_S(R/r0)/R²`.

### 2.3 C2: Blumenthal response

The **contraction operator** `contract(r, M_b, M_0, F)`, with r ascending and M cumulative on r. `Mb(x)`, `M0(x)` are linear interpolation in ln x, x floored at r[0], constant outside. `rf = r` initially. Repeat exactly 100 times:
`rf_new = r · M_0(r) (1 + F) / max(Mb(rf) + M_0(r), 1e-300)`, `rf ← ½ rf + ½ rf_new`.
Then `order = cumulative max(rf)`, and `M_f(r) = interp(ln r; ln order; M_0)`, with left value 0, right value `M_0[-1]`.

**SPARC.** Halo as 2.2 gives S, r0. `rg = geomspace(0.05 R[0], R200, 300)`. `M0g = π S r0² B_S(rg/r0)`. For each Υ:
- `M_k = cumulative max(max(g_B R²/G, 0))` on the data radii (g_B at this Υ, with all points).
- `M_tot = max(M_k[-1], (Υ L36 + 1.33 MHI)·1e9 M☉)`.
- `M_b(rg)`: for rg < R[0], `M_k[0](rg/R[0])²`; within the data, interp in ln r; for rg > R[-1], `exp[(1−t) ln max(M_k[-1], 1e-300) + t ln M_tot]`, `t = clip(ln(rg/R[-1])/ln 3, 0, 1)`. Then cumulative max.
- `M_f = contract(rg, M_b, M0g, M_tot/M200)`. `g_h = G interp(ln R; ln rg; M_f)/R²`. `g_p = g_B + g_h`.

### 2.4 C3

Per footing, background. `M200` from the map, R200, `S = S_H(M200)` with η_C3. Flag `above = M200 > 10^12.3`. If above: `g_p = g_B + G π S r0² B_B(R/r0)/R²`, Burkert, `r0 = solve_r0(M200, R200, S, B_B)`. If not above: `g_p = ν(g_B/a0) g_B` where g_B > 0, g_B elsewhere. Tl and LT read the law's values on all systems: FG1's stated approximation, to be stated beside the cell with the share of SPARC galaxies above T (compute it on background A).

### 2.5 C4

`g_p = ν(g_B/a0) g_B`, as the law branch above, per footing. Per-galaxy Υ for tilt from the same fit. C4's rows are the same on both background tags (no background enters); report both.

---

## 3. LT and G

### 3.1 LITTLE THINGS

`inputs/little_things/oh2015_table2.csv`, values as parsed from Oh+2015 Table 2. Keep rows where R, V, M_gas, M_SED are all present: expected 20 of 26. `M_b = (M_gas + M_SED)·1e7`, `lg M_b`. Set E. `E = log10(V²/R) − log10(g_model)`, with V in m/s, R in m. **LT = median E.** Pass as section 1.

- **C4, C3 law:** `g_N = G M_b/R²`, `g_model = ν(g_N/a0) g_N`.
- **C1:** `M200` from the map at lg M_b, R200, `S = S_N(M200/f_c)`, `r0 = solve_r0(M200, R200, S, B_S)`. `rg = geomspace(1e-3 R, R200, 600)`. `M0g = π S r0² B_S(rg/r0)`. `M_c` = interpolation of M0g in ln r at R. `g_model = G M_b/R² + G M_c/R²`.
- **C2:** the same, with `M_bg = M_b min(rg/R, 1)²`, `M_c` from `contract(rg, M_bg, M0g, M_b/M200)` at R.

Both backgrounds through the map; law rows have no dependence.

### 3.2 Groups: data

`inputs/groups/J_A_A_710_L39.tsv`: skip `#` lines, tab-separated, need ≥ 13 fields, field 0 an integer, field 1 stripped = "Galaxy group". Then `ls = f[5]`, `lM = f[7]`, `Re = f[10]` (kpc). Expect 63.

### 3.3 Groups: estimator, set P

Hernquist tracer: `XG = logspace(-5, 5, 3000)`, `ρ_H = 1/(2π XG (1+XG)³)`, `M_H = XG²/(1+XG)²`. `a = Re·kpc/1.8153`. `M_b = 10^{lM+δ} M☉`. All on background A.

`s² = [∫ 4π XG² ρ_H XG g̃ XG d ln XG / 3] · G M_b/a`, trapezoid on ln XG, with `g̃` the pull in units of G M_b/a². `log σ = ½ log10 s² − 3`.

- **No-halo:** `g̃_N = M_H/XG²`.
- **Halo mass, C1:** `ρ_c` from background A's h, with G of set P and Mpc of set E. `M200 = 10^{a + b(lg M_b − 10)}` with `lg M_b = lM + δ`, as kg with set P's M☉. R200 uses that. `S = S_N((M200/M☉_E)/f_c)`. `r0 = solve_r0(M200, R200, S, B_S)`. `M_h(rr) = π S r0² B_S(min(rr, R200)/r0)`, `rr = XG a`. `g̃ = M_H/XG² + M_h/(M_b XG²)`.
- **C2:** `rg = geomspace(min(rr[0], 1e-4 R200), R200, 800)`. `M0g = π S r0² B_S(rg/r0)`. `M_bg` = interp in ln r of `M_b M_H` at rg. `M_c` from `contract(rg, M_bg, M0g, M_bg[-1]/M0g[-1])`, interpolated back in ln r. `g̃ = M_H/XG² + M_c/(M_b XG²)`.
- **C3:** `M = M200/M☉_E`, `S = S_H(M)` at η_C3, flag `M > 10^12.3`. Burkert. `M_h = π S r0² B_B(min(rr, R200)/r0)`. If above: `g̃ = M_H/XG² + M_h/(M_b XG²)`. If not: `g̃ = ν(g̃_N/y0) g̃_N`, `y0 = a0/(G M_b/a²)`.
- **C4:** the same law form, always.

**Statistic.** `d_i = ls_i − log σ(δ=0)`. `sl_i = [log σ(δ=+0.01) − log σ(δ=−0.01)]/0.02`, evaluating the halo and its flag afresh at each δ. `mean = mean d`, `se = std(d, ddof=1)/√n`, `sys = 0.10·mean(sl)`, `tot = √(se² + sys²)`, `Z = mean/tot`. Class: NOT DIAGNOSTIC if tot > 0.045; else CONSISTENT if |Z| < 2; else ABOVE LAW if Z ≥ 2; else BELOW LAW.

---

## 4. Clusters: K and X

### 4.1 Data

- `clusters/x7_measure_percluster.npz`: arrays with N = 326. h index: `h0672 → 1`, `h0686 → 2` on the second axis of D, E, den, den_r, DRR, Dx, m3to8; `leakP` has h index `h0672 → 0`, `h0686 → 1`, and use its third-axis index 0.
- `clusters/x2_catalogue_columns.npz`: name, ra, dec, z, Mgas500 (M☉), R500 (Mpc), off_deg. Same order as the npz above.
- `clusters/erass1_kt.csv`: KT by name.
- `clusters/x7_outer_mgas_cal.json`: `A_CAL`, `s_CAL` per `foot|h` for Mall, M1, M2, M3 [INPUT AS GIVEN].
- `clusters/bcg_per_cluster.csv`: BCG mass or nan [INPUT AS GIVEN].
- `clusters/chae21_env.csv`: column `log_eN_noclu`.

**Selection.** `I` = clusters with finite KT > 0: expected 106. `xkt = log10(KT/median KT)` over I. KT terciles: quantiles 1/3, 2/3 of xkt, label `digitize`. `X1 = [1, xkt]`. Mgas terciles: over all 326, on `Mgas500`, quantiles 1/3, 2/3 and `digitize`, labelled by the npz's Mgas500. Patches: `order = argsort(ra)`, `PATCH[order] = arange(N)·30//N`.

**Weights.** `W = 1/E²` where E < 1e8, else 0. `Bst = Σ_i den_i / Σ_i den_r_i`, per radial bin. 8 radial bins. Bands: INNER {0,1,2}, MID {3,4,5}, OUTER {6,7}.

### 4.2 Forward model, set F

**Distances.** `PCHIP` through z nodes [0, 0.295, 0.510, 0.706, 0.934, 1.321, 1.484, 2.330] and values [0, DM_b, 13.588, 17.351, 21.576, 27.601, 30.512, 38.988], where `DH_b = 21.863 + (21.863 − 19.455)/(0.706 − 0.510)·(0.510 − 0.295)` and `DM_b = √(7.942³/(0.295 DH_b))`. `D_M(z, h) = PCHIP(min(z, 2.33))·101.54/h` Mpc. `DA_cat(z) = trapz over 600 points of 1/√(0.3(1+z')³+0.7) · c/(1e3·70)/(1+z)` with c = 2.998e8. `h` per cell: 0.672, 0.686. `q = (D_M/(1+z))/DA_cat`.

**Grids.** `RG = logspace(-3, log10 30, 3000)` Mpc, `RM = RG·Mpc`. `RF = logspace(log10 2e-3, log10 3.5, 90)`. `EDGES = logspace(log10 0.15, log10 3, 9)`, `RC = √(EDGES_i EDGES_{i+1})`. `UU = linspace(0, 1, 2001)`.

**Gas and baryons, measured chain.** Let g be the gas factor (`10^0.005`, `1`, or `10^0.111` per row) and f* the star share. `Mg500 = Mgas500 q^{2.5} g`. `R500' = R500 q`.
`sh(r) = (1 + (r/rc)²)^{−1}`, `rc = 0.15 R500'`. Beyond R500', `sh = sh(R500')(r/R500')^{−s}`, s = `gs1_s_meas`. `M(<r)` = cumulative trapezoid of `4π(r·Mpc)² sh` on RG, starting at 0. `M_bx = (1+f*) M(<r) Mg500 M☉/M(<R500')`, M at R500' by linear interpolation in r.

**Turnaround.** Set T. `H0 = h_nat·1e5/Mpc`, `ρ_c`, `Ω_b`, `Ω_c = R_nat Ω_b`, `Ω_m' = Ω_b + Ω_c`, `ρ_m = Ω_m' ρ_c`. `r_ta,com(M_b) = (3(Ω_m'/Ω_b) M_b/(4π·5.55 ρ_m))^{1/3}`. Iterate, at most 199 times: `r_ta = r_ta,com(M_bt)/(1+z)`, `M_bt = M_bx(r_ta)` by interpolation on RM, stop when the relative change is under 1e-6. Seed: `M_bt` from the 3 Mpc-cut gas profile:
`sh_P`: `sh(r)`, with r^{-3} beyond 2.2 R500', zero beyond 3 Mpc, normalised to Mg500 at R500', × (1+f*), last value.
`M_b(r) = M_bx(r)` for `r ≤ r_ta`, else M_bt. `M_fair = R_nat M_bt`.

**Projection.** For a density on RG:
- `ρ = gradient(M_src, RM)/(4π RM²)`. Non-positive values are floored: `ln ρ → ln 1e-300`.
- `Σ(RF) = 2 ∫ exp(interp(ln rr; ln RG; ln ρ)) rr Mpc du`, `rr = RF cosh u`, `u = UU·arccosh(RG[-1]/RF)`, trapezoid.
- **Offset**, `d = radians(off_deg)·D_M/(1+z)`, Mpc. If d ≤ 1e-4 unchanged. Else `Σ_o(RF) = (1/π) ∫_0^π exp(interp(ln R'; ln RF; ln max(Σ,1e-300))) dφ`, `R' = √(RF² + d² + 2 RF d cos φ)`, 181 points.
- `ΔΣ`: `cum = [½Σ_0 RF_0², ½Σ_0 RF_0² + cumtrapz(Σ RF, RF)]`, `ΔΣ = 2 cum/RF² − Σ`.
- `P(RC) = exp(interp(ln RC; ln RF; ln max(ΔΣ, 1e-30)))/KG_PC2`. `Σ_b(RC) = exp(interp(ln RC; ln RF; ln max(Σ_o, 1e-300)))`.
- **Reduced shear.** For bins with den > 0: `f_red = 1 + Σ_{p=0}^{5} Σ_b^{p+1} m_p/den`, m_p = `m3to8[i, h, p]`. Otherwise 1.
- **Vector.** `V_i = W_i · P · f_red`, 8 bins.

**C\* normaliser.** `v^C_i = V_i` for `M_src = g_C r²/G`, with `g_C = (½ g_N + √(¼ g_N² + g_N a0)) · C(s)`, `g_N = G M_b/RM²`, and `s = RG/(√(G M_b(3 Mpc)/a0)/Mpc)`.

**External-field factor C(s).** On a footing: `y_e = 10^{median log_eN_noclu}·1.2e-10/a0`. Solve AQUAL for a point mass in a uniform field, units G = M = a0 = 1, `μ(x) = x/(1+x)`, `div[μ(|∇Φ|)∇Φ] = 4πρ`, axisymmetric, `Φ → x_e z`, `x_e = ½(y_e + √(y_e² + 4 y_e))`.
Finite volume on (ln r, θ): `r_min = 0.05`, `r_max = 60/x_e`, 60 radial cells per decade, 64 θ cells. Radial faces `r_f`, geometric-mean centres. Kačanov iteration, one sparse direct solve per step, tolerance 1e-9 on the max relative change, maxit 3000. μ at a face from the normal difference and the average tangential derivative. Inner face: flux `1/r_min²` per unit area. Outer: Dirichlet at a ghost centre `r_f[-1] e^{½Δu}`, `Φ = x_e r cos θ − 1/(μ_e √(1+L_e) r')`, `r' = r √(sin²θ + cos²θ/(1+L_e))`, `L_e = 1/(1+x_e)`, `μ_e = μ(x_e)`.
`M(r_f) = r_f² Σ_θ w_θ (∂Φ/∂r)/2`, w_θ the exact solid-angle weights summing to 2. `M_iso(s) = ν(1/s²)`. `C = M/M_iso`.
Off the table: `C = 1` for s below the first s; interpolate C in ln s (clamped); beyond the last, `C = M_last/M_iso(s)`.
`clusters/efe_table_<foot>.npz` has (s, M) from the record's solver [INPUT AS GIVEN]. Solve it yourself, compare with this file and report the max relative difference; grade on your own solve (see A10).

### 4.3 Measurement side and keys

**Per cell (foot, h):** `n_i = W_i Bst (D_i − leakP_i)`, `n^raw = W Bst D`, `n^x = W Bst Dx`, `n^RR = W Bst DRR`, `d_i = v^C_i`. Band sums per cluster give arrays over clusters.

**A over set Ix, band b.** `A = Σ n/Σ d`. `A_x = Σ n^x/Σ d`. `A_RR = Σ n^RR/Σ d`.

**σ_STAT (key).** Bootstrap: `idx = default_rng([20261024, key]).integers(0, nsel, size=(2000, nsel))`, one call. Counts per replicate, by cluster. Replicate ratio `(Wt·n^raw)/(Wt·d)`. `σ_b = std(ddof=1)`. Jackknife: for q in 0..29 where any `PATCH[Ix] == q`, weights `(PATCH[Ix] != q)`, ratio; `σ_j = √((n−1)/n Σ(v − mean v)²)`. `σ_STAT = max(σ_b, σ_j)`. `σ_IN = √(σ_STAT² + A_x² + A_RR²)`.

**Slope.** `wls(n, d, X)`: solve `(Σ d_i X_i X_iᵀ) β = Σ n_i X_i`. `b = β_1`, with n = the leak-subtracted `n` (not `n^raw`). `σ_b` by the same bootstrap and jackknife on β_1, over I, with `key = 5010`, again on `n`; replicate weights Wt multiply each term of both sums. Ratio σ's use `n^raw`, as above.

**Keys.** `T` = KT tercile within I; `Mt` = Mgas tercile. Keys for band sums, with stat keys in brackets.

| Key | Measured A (σ) | Predicted |
|---|---|---|
| G-IN-all | I, INNER [0], σ_IN | Σ_I V / Σ_I v^C, INNER |
| G-MID-T1,2,3 | T = 0,1,2, MID [20100+t], σ_STAT | ratio on that T, MID |
| G-MID-b | slope I, MID [5010], σ_b | `wls(V, v^C, X1)` β_1, MID |
| G-OUT-all | I, OUTER [0], σ_STAT | Σ_I ratio, OUTER |
| G-OUT-T1,2,3 | T, OUTER [20100+t], σ_STAT | ratio on T, OUTER |
| G-OUT-b | slope I, OUTER [5010], σ_b | β_1, OUTER |
| G-OUT-Mall | all, OUTER [0]; see below | Σ_all ratio, OUTER |
| G-OUT-M1,2,3 | Mt, OUTER [200+t]; see below | ratio on Mt, OUTER |
| G-IN-Mall | all, INNER [0], σ_IN | Σ_all ratio, INNER |

**The four outer mass keys, "one template" (C1, C2).** `A` = this run's own A on the set above. `σ = s_CAL · A/A_CAL`, from `x7_outer_mgas_cal.json`. For C4 see 4.6 and A8.

`Z = (A − pred)/σ`. Fail if `|Z| > 2` in either h. Report all 15 for both h.

### 4.4 C1, and C3's K, X: the zoom profile. f* 0.034, g = 10^0.005, canonical

Reported beside it: f* 0.0615; and g = 10^0.111 at both f* for the tag.

Per cluster, per h: `M_b`, `r_ta`, `M_fair`, as 4.2.

**M200 at fair share.** Background A's h, set E: `ρ_c`. `thr = 200 ρ_c (Ω_m(1+z)³ + 1 − Ω_m)`, native Ω_m. `dens(r) = (1 + R_nat) M_b/((4/3)π RM³)`. `i = max{dens ≥ thr}`. Interpolate ln R in ln dens between i, i+1, at ln thr. `M2 = thr (4/3)π R2³`.

If no i exists, fall back: iterate from `M_ta = (M_fair + M_b[-1])/M☉`. `S = max(a0/(2πG), f_c η_A3(M)Σ_coll(M)·M☉/PC2)`, A3 table at this f*, background A. `r0 = solve_r0(M_fair, r_ta, S, B_S)`. `m(r) = M_b(r) + π S r0² B_S(r/r0)`. `R2`: root of `ln[m(r)/(thr0 (4/3)π r³)]`, r in [1e-3 r_ta, r_ta], x tolerance 1e-12, `thr0 = 200 ρ_c` (z = 0). `M_new = thr0 (4/3)π R2³/M☉`. Stop at `|ln(M_new/M)| ≤ 1e-8`, at most 100. Then `M2 = M` in kg, `R2 = (3 M2/(4π thr))^{1/3}`. Count these cases.

**Shape.** z tag: "0.00" if z < 0.125, "0.25" if z < 0.375, else "0.50". Tags in order 1e13, 1e14, 1e15. Choose the segment: start at the first, move on while there's a next segment and lg M2 > lg M of the next node (the middle node decides). `w = clip((lg M2 − lgM_a)/(lgM_b − lgM_a), 0, 1)`. `lnm = (1−w) lnm_a + w lnm_b`. `x_e = min(x_edge)`.
`lnm(x)` for `x ≥ X[0]` interpolates in ln X; below, `lnm[0] + 2 ln(x/X[0])`.

**Cold mass.** `M_c(r) = f_c M2 exp(lnm(r/R2))`. `r_e = x_e R2`.
- If `r_e ≥ r_ta`: `M_h(r) = M_c(min(r, r_ta))`.
- Otherwise `M_e = M_c(r_e)`. `k` = first index with `ln X[k] ≥ ln x_e` (left search). `dln = (lnm[k] − lnm[k−8])/(ln X[k] − ln X[k−8])`. `ρ_e = M_e dln/(4π r_e³)`.
  - If `M_e ≥ M_fair`: `M_h = M_c(r)` for r ≤ r_e, M_e beyond (count it).
  - Otherwise `L = ln(r_ta/r_e)`, `tgt = (M_fair − M_e)/(4π ρ_e r_e³)`, `I(γ) = L` if |3−γ| < 1e-9, else `expm1((3−γ)L)/(3−γ)`, the exponent capped at 700. Bracket from (−40, 60), widening as `lo → 3 − 2(3−lo)` and `hi → 3 + 2(hi−3)` until bracketed. Brent, x tolerance 1e-9, for `I(γ) = tgt`. For r ≤ r_e, M_c. Beyond, with r capped at r_ta and `y = max(r/r_e, 1)`, `M_h = M_e + 4π ρ_e r_e³ (y^{3−γ} − 1)/(3−γ)`, or `ln y` at γ ≈ 3.

**Prediction.** `M_src = M_b + M_h`; `V_i` from 4.2; key predictions from 4.3. The eta-free zoom shape is used, and S isn't, except in the fallback.

**X-COP (all h-free), canonical, set E except as noted.** `inputs/xcop/<name>/`: `hydro_mass` (HDU 1: RADIUS kpc, M_FORW; header R500 kpc, REDSHIFT), `fgas_profile` (HDU 1: RADIUS in units of its header R500, MGAS), `mstar` (HDU 2: RADIUS kpc, MSTAR). Seven clusters.
`li(r, m, t)`: log-log interp, nan outside the range.
Per cluster: `Mg500 = li(RADIUS·R500_g, MGAS, R500)`; g is **not** applied to X-COP's own gas (A6). The chain of 4.2 with `R500' = R500/1e3` Mpc and f* gives `M_bx`, `M_bt`, `r_ta`, seed `M_bt0 = 3·1.2·Mg500·M☉`, `M_fair = R_nat M_bt`.
Rows x in (0.1, 0.2, 0.3, 0.5, 0.7), `r = x R500`, `m_h = li(hydro)`, `m_b = li(gas) + li(stars)`; keep a row if all three are finite. Expected 35 rows. `r_m = r·1e3·3.0857e16`. `M_h(min(r_m, r_ta))` from the profile above, with `M_b = M_bx` capped at r_ta, z its own. `d = log10[m_h M☉/(m_b M☉ + M_h)]`. **X: mean d, rms = √mean d².** The cell is at f* 0.034, with f* 0.0615 reported. Since g isn't applied to X-COP's gas, X has one value per f* across the gas rows.

### 4.5 C2: smooth core + response. f* 0.034, g = 1, canonical

Per cluster, per h: `M_b`, `r_ta`, `M_fair` as 4.2. `M_t = (M_fair + M_b[-1])/M☉`. `S = S_N(M_t)`, background A. `r0 = solve_r0(M_fair, r_ta, S, B_S)`. `M_0 = π S r0² B_S(min(RM, r_ta)/r0)`.
**BCG.** Raw per cluster; where nan, the median of the non-nan values in its Mgas tercile. `M_bf = M_b + BCG·M☉_E·RM²/(RM + 10·3.0857e19)²`. `F = M_bf(r_ta)/M_fair`. `M_f = contract(RM, M_bf, M_0, F)`. `M_src = M_bf + M_f`.

**X-COP.** `M_0` on RM as above with that cluster's `S_N`, `M_c = contract(RM, M_bx, M_0, M_bt/M_fair)`. `M_h(r_m)` = linear interp of M_c on RM. Rows, mean, rms as 4.4.

### 4.6 C4: the law. f* 0.20, no tail, per footing

`M_b = 1.2 × gas(P)`: the `sh_P` profile of 4.2 (r^-3 beyond 2.2 R500', zero beyond 3 Mpc), normalised to Mg500 at R500', g = 1. `M_src = M_b ν(G M_b/RM²/a0)`, where `M_b > 0`, else M_b. Set F.

C* uses this same M_b. `V`, keys, A, σ as 4.3, except for the four mass keys: FG1's row uses A = `A_CAL`, σ = `s_CAL` of `x7_outer_mgas_cal.json` as given (A8).

X: NOT GRADED.

---

## 5. Ln: KiDS isolated lensing, set L

### 5.1 Data

`inputs/lensing/Fig-3_...Massbin-{1..4}.txt`: columns 0 = R (h70⁻¹ Mpc), 1 and 4 used: `Y = c1/c4`. `R`, `Y`: 4×15. Cov file: for each row, `m = index of c0 in sorted unique c0`, `n` likewise for c1; `i = argmin|R[0] − c2|`, `j = argmin|R[0] − c3|`; `C[15m+i, 15n+j] = c4/c6`. `IDX_ALL` = all 15; `IDX_PRIM`: `R[0] ≤ 0.31`. `sel` applies an index set to all four bins.

`lens_inventory.npz`: `logM`, `z`, `WLENS`. Bins by logM edges [8.5, 10.3, 10.6, 10.8, 11.0001], `digitize − 1`, keep 0..3. Per bin: `w`, `logMs70`, z, `qDA = χ(z; 0.3085)/χ(z; 0.3)`, `zeff = Σwz/Σw`. `χ(z; Ω) `: cumulative trapezoid of `1/√(Ω(1+z)³+1−Ω)` on `linspace(0,1,4001)`, interpolated.

**Native conversion**, `h_N = 0.679`, `Ω_N = 0.3085`, `T = 1.0128`: `R^n_b = R_b (0.70/h_N) χ(zeff_b; Ω_N)/χ(zeff_b; 0.2793)`. `F = (h_N/0.70) T`. `Y^n = Y F`. `C^n = C F²`. These are F2's and CFG885's committed values.

### 5.2 Models

`LMG = 6.8..11.8, step 0.02`. `RGRID = logspace(1, 10, 3601)` pc. For lm in LMG: `lm70 = lm − 2 log10(0.70/h_N)`, `lmc = lm + (−0.69 lm70 + 6.63)`. `M_s = 10^lm`, `M_cg = 10^lmc`, `M_B(r) = M_s + M_cg + 0.5 M_s min(1, (r/1e5)³)`.

**Halo.** Background A. `lg M200 = a + b(log10(M_s + M_cg) − 10)`. `ρ_c = 2.775e11 h²/1e18` M☉/pc³. R200 pc. Σ_coll(M) = log-log interp of the five nodes of 0.1 at M = 1e11, 1e12, 1e13, 1e14, 1e15, with linear extrapolation outside from the end segments (A11). `S = max(a0_L/(2π Gpc), η(M200) Σ_coll(M200))`. `r0 = solve_r0(M200, R200, S, B)`. `M_h = π S r0² B(min(r, R200)/r0)`.

**Mass models.**
- **L:** `M_B ν(Gpc M_B/r²/a0_L)`, tail "linear".
- **H (route E):** `M_B + M_h`, Burkert, η per candidate below, tail "const".
- **ENV, C3:** `M200 > 10^12.3`: `M_B + M_h`, tail "const". Otherwise L's profile, tail "linear".
- **ENV, C4:** L everywhere (ENV and L are one function in this mode).

**ΔΣ.** `t = linspace(0, 12, 2401)`. `dM/dr = gradient(M, ln r)/r`; tail value `dM/dr[-1]` if "linear", 0 if "const". For R, `f = interp(ln(R cosh t); ln r; dM/dr)`, with left value dM/dr[0], right value the tail. Endpoint weights ½·Δt. `M_cyl = interp(ln R; ln r; M) + Σ f (1 − tanh t) R sinh t w`. `Σ̄ = Σ (f/cosh t) w/(2πR)`. `ΔΣ = M_cyl/(πR²) − Σ̄`.

**Stack.** Per bin b, table over LMG at `R^n_b·1e6`. `lm_i = logMs70_i + 2 log10(0.70/h_N) + 2 log10 qDA_i`. `model_b(R_j) = Σ_i w_i interp(lm_i; LMG; table_j)/Σ w`. M200 for the flag is that of the grid mass.

**Two-halo.** `t1x_pgrav_x0.2562.json` [INPUT AS GIVEN]. Keep k > 0 with finite P > 0. `h_t = 0.6736`, `Ω_t = (0.02237 + 0.1200)/h_t²`, `a = 1/(1+z)` (see Disclosures). `rs = 0.05`, `rg = logspace(-2.5, 2, 900)` comoving Mpc/h. `ξ(r) = ∫ k² P sinc(kr/π) e^{−(k rs)²} dk/(2π²)`, trapz, np.sinc convention. `ξ(r)` by interp in ln r, left ξ[0], right 0. `ρ = Ω_t·2.775e11`.
`esd2h(R, r_ex)`: `R_c = R h_t/a`, `r_c = r_ex h_t/a`. `R_g = logspace(-3, log10(1.01 max R_c), 220)`. `Σ(R_v) = 2ρ ∫_0^80 ξ(√(R_v²+t²)) [only where √ > r_c] dt`, adaptive quadrature, limit 400. `M_cyl` = cumulative trapz of 2πR Σ. `ΔΣ = interp(R_c; R_g; M_cyl/(πR_g²) − Σ)·h_t/1e12/a²`.
Template: `T_b = esd2h(R_b, r_ex,b)·F`, with `r_ex = [0.343, 0.442, 0.433, 0.429]`.

### 5.3 Fit and statistic

`fit(m, idx, use2h, T, bmax)`: `s = sel(idx)`, `C_s = C^n[s,s]`, Cholesky `L`. `r0 = L⁻¹ (Y^n − m)[s]`. With 2h: design A with `T_b` in bin b, column b, `A ← L⁻¹A[s]`, `b = lsq_linear(A, r0, bounds=(0, bmax)).x`. `m_f = m + b T`. `χ² = r C_s⁻¹ r`, `r = (Y^n − m_f)[s]`.

**C3, C4 (footing by footing).** `L2H`, `ENV2H` = fit with 2h on IDX_ALL, of L and ENV. `H2H` = with 2h on IDX_ALL of H.
- C3: H's η = η_C3.
- C4: H's η = η_A2.
- Pass: `Δχ²(ENV2H − L2H) ≤ 9`, `Δχ²(ENV2H − H2H) < 0`.

Report the primary range as well (`IDX_PRIM`).

### 5.4 C1: the class on FC1's rule. Tagged not on NR2

Smooth core B_S. `η(M) = f_c · interp(lg M; [12,13,14]; ce1_a3_eta_med)`, flat outside; M is M200. `S = max(a0/(2πGpc), η Σ_coll(M200))`, as X79's text: the floor is in this rule and the mass isn't divided by f_c (A12). Tail const.

`D0 = χ²(H2H) − χ²(L2H)`, IDX_ALL. `cls(d)`: LAW if d ≥ 9; HALOS if d ≤ −9; NOT DIAGNOSTIC otherwise.
S1: T from `esd2h(R_b, median R200_b)`, median weighted: sort lenses by R200 (interp of R200 table at lm_i), first with cumulative w ≥ half total. `D1`, both models.
S2: `bmax = 1`. `D2`.
`verdict`: NOT DIAGNOSTIC if `cls(D0)` is NOT DIAGNOSTIC or cls(D1) or cls(D2) differs from cls(D0); otherwise cls(D0). **Pass iff verdict is not LAW.** Both footings reported, canonical graded.

---

## 6. Dw: Local Group dwarfs, set D

### 6.1 Rows

`dwarfs/x1_per_system_inputs.csv`, per footing row. Classes: MW ultra-faint 31, bright M31 25, M31 others 5, MW classical 8, LG field 13.

`dwarfs/arroyo_polonio2026_tableA1.csv`: `arr[lvd_name] = sig_free/sig_f0`, `med = median`. `b = arr[name]` if present, else `med` if `M_V` is present and > −7.7, else 1. `σ_c = sigma·b`. `r12 = (4/3) rh_pc·pc`. `M_* = 10^logMstar`. `g_obs = 3(σ_c·1e3)²/r12`. `g_N = G (M_*/2) M☉/r12²`. `s = sdMC[Newton]`.

### 6.2 C3, C4: harness rows

ρ_c from background A's h. `E = log10(g_obs/g_p)`.
- **C4:** `g_p = ν(g_N/a0) g_N`, no external-field term.
- **C3:** satellites (`host` in MW, M31) on the halo branch; others on the law (A13). Halo: `M_cool`: `T_vir(M,z) = μ m_p G M/(r_v·2 k_B)`, `r_v = (3M/(4π·18π²ρ_m0(1+z)³))^{1/3}`, `ρ_m0 = ((ω_b+ω_cdm)/h²)ρ_c`, background A, `μ = 0.59`, `T = 1e4`, `z = 8`, `m_p = 1.67262192e-27`, `k_B = 1.380649e-23`. `M200 = max(10^{a+b(lg M_*−10)} M☉, M_cool)`. R200. `S = a0/(2πG)`. Burkert. `M_h = π S r0² B_B(min(r12, R200)/r0)`. `g_p = g_N + G M_h/r12²`.

**Statistic per footing.** Fresh `rng = default_rng(20261026)` per footing, classes in the order MW ultra-faint, bright M31, M31 others, MW classical, LG field. For each, with its E, s in CSV order: `ix = rng.integers(0, N, (10000, N))`, then `rng.standard_normal((10000, N))`. `median = median E`. `sd = std(median over axis 1 of E[ix] + s[ix] z)`, ddof 0. `Z = median/sd`. Pass: all |Z| < 2.

### 6.3 C1: the ceiling over M200. Tagged [READ ND1]'s rule, not on NR2's table

`LMG = arange(4, 14, 0.02)`, inclusive. Per M: `M_t = M/f_c`, `lg = lg M_t`. `S = f_c · interp(lg; [12,13,14]; ce1_a4_eta_med) · 10^{interp(lg; [10,11,12]; [lg r10, lg r11, 0])} · Σ_coll(max(M_t, 10^{7+log10 2}))`, with `r10, r11` from `scalars.json → x80`. R200 at background A's h. `r0 = solve_r0` with B_S. `C_i = max over the grid of π S r0² B_S(min(r12_i, R200)/r0)`.
`E = log10(g_obs/(g_N + G C/r12²))`. Footing canonical. Same bootstrap, with one `default_rng(20261026)`.

---

## 7. Tier C trace

Not recomputed. **NOT RECOMPUTED is never agreement.** The implementer doesn't open these; the COMPARE stage does K4. "fg1_read" means `rebuild_2026_10_22/FG1_final_grade/fg1_read.py`.

| Candidate, line | File | Key or locator |
|---|---|---|
| C1 MW | `UR3_direct_weighing/ur3_mw.json` | `rows["A_c2b_refit|d0|off"].cls`, `.n_all` |
| C2 MW | same | `rows["A_c2b_refit|d0|blum"]`, `rows["A_c2b_refit|d0|gnedin"]`, `.cls`, `.n_all` |
| C3 MW | `BS1_basin_switch/bs1_basin_switch_results.json` | `primary.mw.<foot>.cls`, `.n_L1_L2a_L2b`; README literals in fg1_read `LITS`. Its own L |
| C4 MW | `X5_mw_joint_baryons/README.md` | literals in fg1_read `LITS` and `build_c4`, row MW. FG1 discloses a source swap from RF1 |
| C1 DM | `UR3_direct_weighing/ur3_diskmass.json` | `"1.5 hR|off".r`, `.Y` |
| C2 DM | same | `"1.5 hR|blum".r`, `.Y`, `.n`; fragility literal `UR3_direct_weighing/README.md`, in `LITS` |
| C3, C4 DM | `campaign_fresh_gravity/CFG576_diskmass_sigz/README.md`, `CFG577_diskmass_grid/README.md` | literals in `LITS`. NOT GRADED |
| C1 IC | `ND1_native_dwarfs/nd1_ab.out` | line for IC 1613, literal in `LITS` |
| C2 IC | none | NOT GRADED |
| C3 IC | `BS1_basin_switch/bs1_basin_switch_results.json` | `primary.dwarfs.<foot>.flags["IC 1613"].E`, `.Z`. RF2 class below |
| C4 IC | `ND1_native_dwarfs/README.md` | literal in `LITS` |
| all IC | `RF2_ic1613_inclination_footing/rf2_ic1613_results.json` | `verdict.<foot>` |
| C2 G | `NR3_ur1_on_nr2/nr3_MEDIAN_results.json` | `runs["EM1|blum"].groups.Z`, `.verdict` |
| C2 Ln | `FC1_cold_share_native_eta/x79_rule/x79_kids_grade_native.json` | `footings.<foot>.verdict`, `.all.dchi2` |
| C2 Dw | none | NOT GRADED |
| C4 X | `HO1_xcop_hotgas_heldout/README.md` | literal in `LITS`. NOT GRADED |

---

## 8. Checks, implementable

**K1 injection,** through the same functions, before real data.
- **SPARC mock.** Take the 175 real rotmods' radii, Vdisk, Vbul, Vgas. Set `Vobs² = R·g_model/1e6`, using the law at canonical at a per-galaxy Υ_true = 0.60, eV unchanged, no noise. Run 2.5. Pass: Υ_med within 0.01 of 0.60.
- **Shear mock.** For cluster set N, at one cell, set `D_i = A_inj · v^C_i/(W_i Bst)` where the denominator is positive, else 0, `leakP = 0`, A_inj = known excess, with the real sigma array. Take A_inj = 1.30. With prediction 1 (V = v^C), G-OUT-all's Z, computed by the code, must equal `(A_inj − 1)/σ` within 0.10, where σ is the code's own σ on the same run.

**K2 data.** Print sha256 and row counts of every input; compare with `inputs/MANIFEST.txt`. Check sizes: SPARC 175, tilt 153/47/53, LT 20, groups 63, clusters 326, KT 106, X-COP 35 rows on 7 clusters, dwarf classes as 6.1, zoom snapshots 27 + 63, BCG non-nan 190.

**K3 repeat.** Rerun, results byte-identical. Sort keys; fixed float format.

**MUTATE.** Separate outputs.
- ν ≡ 1 in the law. Line S for C4 must fail.
- Sign of the excess flipped in K's mock (A_inj − 1 → 1 − A_inj against the same target). K1 must fail, exit 1.

**K4 trace.** Done by COMPARE on section 7: each value appears in its named file by key or literal.

**Other known answers. These are mathematics or inputs, and a failure before the seal means no verdict.**
- `B_B`, `B_S` closed forms against quadrature of their densities (`ρ0 r0³/((r+r0)(r²+r0²))`; `ρ0 r0³/(r²+r0²)^{3/2}`), rel 1e-6. `solve_r0` returns M, rel 1e-8.
- K-S: σ8 from the class file `W(8k)` integral against `backgrounds.<tag>.sigma8`, |d| ≤ 1e-3.
- Contract: `M_b = 0, F = 0` returns `M_0` to 1e-6 away from the five grid ends; with `M_b` a point mass `M_p`, `F` given and `M_0 = k r`, `r_f (M_p + M_f) = r_i k r_i (1+F)`, rel 1e-3.
- Zoom: sampled NFW c = 4, N = 57777, 20 samples through the shape measurement: the mean of `m/m_exact` at x 0.05–1 within 1 %, R200 within 1 %.
- `wls`: on n=[1,2,3], d=[2,1,5], X=[[1,.3],[1,-.2],[1,.7]], check by direct normal equations.
- Groups: no-halo estimator with ν ≡ 1 against the closed integral of the same quantity by a second quadrature, 1e-4 dex.
- η per seed vs `nr2.per_seed_eta`: report the maximum difference.
- C(s) vs `efe_table_*`: report the maximum relative difference.

---

## 9. Output

`results/crg1_results.json`, sorted keys, committed with sha256 before any comparison:
`{candidate: {footing: {line: {status, values...}}}}`. Values at minimum:
- S: Υ_med, rms per background. Tl: tilt per background, plus Υ by Vflat bins [20,60), [60,100), [100,150), [150,200), [200,250), [250,400) in the quality set. LT: median E per background.
- K: per h, for each key: A, σ, pred, Z; failing list. X: mean, rms, by x, per cluster, counts of no-fair-share, no-tail, wide-γ.
- G: mean, se, sys, tot, Z, class. Ln: χ² L2H, ENV2H, H2H, Δχ² both, b. C1: D0, D1, D2, verdict.
- Dw: per class N, median, sd, Z.
- Run time, peak memory.

Tags: every cell carries `[recomputed]`, `[INPUT AS GIVEN: <inputs>]` or `NOT GRADED`.

---

## 10. DISCLOSURES: non-native values and given items in the chain

These are stated plainly, and left in place because the source lanes use them. They're not to be swapped.

- **Two-halo template:** P_grav from a T1x run at CFG650 settings. Its conversion uses `h = 0.6736`, `ω_b = 0.02237`, `ω_c = 0.1200`, which are Planck-type values.
- **Catalogue rescale:** `DA_cat` uses H0 = 70, Ω_m = 0.3. It undoes the catalogue's assumed distances, and isn't a model input. The KiDS conversion's fiducials 0.2793 and 0.3 are of the same kind, as are `h_N = 0.679`, `Ω_N = 0.3085`, `T = 1.0128` from F2/CFG885.
- **External field `1.2e-10`** in `y_e` is the Chae 2021 table's unit, not a footing.
- **C4's K row** comes from a chain that also carried Planck 5.364, 0.0493 and 67.4 in `M_fair` and r_ta. In law mode neither is read, so they are omitted here.
- **Backgrounds:** CLASS with `omega_cdm` is the record's own fit (F3), framework-native by the source lanes, with cold dark energy treated as a w ≈ 0 component for growth. Tables are given.
- **Taken as given, not re-estimated:** EM1 map a, b; c_f(1e13), c_f(1e14) in NR2's table (ng 64 stacks); A2, A3 tables; `ce1_a3/a4_eta_med`; X80's ratios; GS1's slope; GS4's +0.005; X-COP's +0.111; BCG; X7's A_CAL, s_CAL.
- **Shape stacks mix resolution:** 1e13 at ng 64, 1e14 and 1e15 at ng 80, as ZN4 froze it. The z 0.50 node at 1e15 uses a z_f snapshot where no z 0.50 exists.
- **Measured chain limits:** the rebuild can't catch an error in these inputs.

---

## 11. AMBIGUITIES

Every plain reading is stated. For each one, grade the **first reading** as the primary and, where marked, report the second beside it. Don't choose by outcome.

**A1. η12 anchor.** NR2's ρ's and c_f(1e12) use the literal 21.53, carried from NR1, and not that lane's freshly printed median. (a) Literal 21.53, with medians at 1e10, 1e11 from the re-estimate. (b) All three medians from the re-estimate. Report (b)'s η12 and ρ's and, if the η table moves, S for C1.

**A2. float32 zoom coordinates.** Inputs were reduced to fit the size cap. (a) Use as given. (b) Original float64 isn't available here. Report differences through the per-seed check.

**A3. C3 on Tl and LT.** FG1 uses the law on all systems, ignoring those in basins above T. (a) That. (b) Basin-consistent: above-T systems with the halo branch. Report (b) if cheap, not graded.

**A4. Per-galaxy Υ vs pooled S in C1.** The record's S path uses `B_S(R/r0)` and its tilt path `B_S(min(R, R200)/r0)`, with R200 at or beyond the data for essentially all points. (a) As stated. (b) One form for both. Report the largest difference.

**A5. Mixed constants.** Sets E, F, T, P, D differ in the fourth digit, and group halos mix P's M☉ with E's Mpc in R200 and M_t. (a) As tabulated. (b) One CODATA set. Report (b) on one line only if time allows.

**A6. Gas factor and X-COP.** The factor g scales eRASS1's catalogue gas only. X-COP's own measured gas isn't scaled. (a) As stated. (b) Scale X-COP's too. (b) not graded; report if cheap.

**A7. C1's h-cell and gas pairing on K.** Primary f* 0.034. Is the K cell f* 0.034 alone, or must it hold at 0.0615? (a) f* 0.034 graded, 0.0615 reported. (b) Both graded. Report both rows either way.

**A8. C4's mass keys.** FG1's row uses X7's A_CAL and s_CAL as given. (a) As given: the template is X7's at f* 0.20, and its C* is the same. (b) One-template rescale, as C1 and C2. Report (b) beside (a).

**A9. Footing in C1 and C2 cluster rows.** "No a0" applies to the cold sector, yet the C* normaliser uses a0. (a) Canonical C*, as FG1 reads. (b) Alt C*, reported, never pooled.

**A10. C(s).** (a) Own solve. (b) Given table. Report the difference, and if K's Z moves by more than 0.10 anywhere, report (b)'s Z too.

**A11. Σ_coll in lensing.** The record's X53 path interpolates five tabulated nodes log-log; other paths evaluate 0.1 directly. (a) As X53, five nodes. (b) Direct. Report (b)'s Δχ² if cheap.

**A12. C1's Ln rule.** FG1's criteria say "read FC1's class, tagged not on NR2". The rule in that chain keeps a floor, uses an older η table and doesn't divide M by f_c, while C1's own S path differs on all three. (a) The chain as in 5.4. (b) C1's S_N in 5.2. Report (b) beside (a), tagged.

**A13. C3's flag in Dw.** The code flags by host ("satellite"), independent of T. FG1's criteria call C3 "the law below T 12.3, halos above". (a) Host flag, as the harness. (b) Mass flag M200 > 10^12.3. Report (b) beside (a).

**A14. C1's Dw inputs.** ND1's rule uses older anchors (`ce1_a4_eta_med`, X80's r10, r11), not NR2's. (a) As ND1. (b) NR2's table and ρ's. Report (b) beside (a), tagged.

**A15. Bootstrap streams.** σ in K and Z in Dw are seeded with numpy PCG64. If numpy's `default_rng([a, b])` or `integers` behaviour differs by version, values shift. (a) Current numpy. Report the numpy version.

**A16. Interpretation of "both h cells" for failing keys in C4's table.** FG1 grades a key as failing if over 2 in either h, and prints worst at h 0.672. (a) As stated. No other reading is graded.

**A17. Lensing sign of T's flag mass.** C3's halo flag uses M200 from the catalogue mass, not M_t. (a) M200. (b) M_t = M200/f_c: not on record for C3. (b) isn't computed.

---

κ = ½ FITTED. T LOCATED. Not theory closed.
