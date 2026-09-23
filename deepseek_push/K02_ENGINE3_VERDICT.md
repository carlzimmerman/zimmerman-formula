# K02 — ENGINE-3 VERDICT: THIRD-MOTOR RE-VERIFICATION OF JWST MOMENT-CHANNEL HEADLINES

**Verdict: ALL PASS — every headline number independently reproduced within 3 SE; no disagreement found.**
Date: 2026-09-23 (EDT) · Auditor: third independent motor · Files: `K02_engine3.py`, `K02_engine3.out`, `K02_results.json`

---

## 0. What this engine is (and is not)

A from-scratch Monte Carlo of Thomson transport on the unit sphere (c = 1, isothermal T = 1,
κ(r) = τ0(1 + qr²)), with **no shared code path** with engine 1 (`J02_moment_hierarchy.py`) or
engine 2 (`bhstar_scattering_clock_2026_09_21/transport.py`):

| choice | engine 1 (J01/J02) | engine 2 (transport.py) | **engine 3 (this file)** |
|---|---|---|---|
| flight sampling | exact τ, fixed 60-round bisection | null-collision thinning | exact τ, **Newton–bisection hybrid** on analytic bracket [w/(τ0(1+q)), min(w/τ0, wall)] |
| angle μ | rejection on U(−1,1) | rejection on U(−1,1) | **closed-form Cardano inverse CDF** of (3/8)(1+μ²) |
| initial direction / transverse frame | normalised normals / random Gram–Schmidt | normalised normals / random Gram–Schmidt | **spherical angles** (cosθ=2U−1, φ=2πU) / **deterministic cross-product basis** |
| RNG seeds | 13, 17, 19, 29, 31, 41 | 9212600+ | 20260200, 20260203, 20260210, 20260230,… |
| delay arithmetic | (x−x0)·u_final direct | direct | **Σℓⱼ(uⱼ·u_final) accumulator, cross-checked** vs direct (max err 0.0) |

Physics is identical by construction (that is the point of a verification motor). Sampler self-tests:
Thomson inverse-CDF moments E[μ]=−0.00023±0.00046, E[μ²]=0.39998±0.00021, E[1−μ]=1.00023±0.00046
(z ≤ 0.52 vs exact 0, 0.4, 1); q=0 flight root lands on w/τ0 to machine zero (max abs err 0.0).

## 1. Headline reproduction (τ0=1, central, n ≥ 1e6; cited values from engines 1/2)

| quantity | this engine (mean ± SE) | cited | z = Δ/SE |
|---|---|---|---|
| E[D] @ q=0 (n=2e6) | 0.499411 ± 0.000507 | 0.5008 | −2.74 |
| E[v²] @ q=0 | 2.8035 ± 0.0055 | 2.8061 | −0.47 |
| E[D v²] @ q=0 | 3.7048 ± 0.0127 | 3.7316 | −2.11 (J01's own se 0.027 → combined z ≈ −0.8) |
| atom fraction @ q=0 | 0.367932 ± 0.000341 | 0.3679 | +0.10 |
| E[D] @ q=10 | 2.999082 ± 0.002688 | 3.003 | −1.46 |
| atom fraction @ q=10 | 0.013153 ± 0.000114 | 0.0131 | +0.47 |

Cross-engine agreement is consistent everywhere: E[D] q0 0.4994 vs J02 0.50080±0.00072 vs J01
0.50118±0.00114 (all within ~2 combined SE); E[N] 1.4025 / 4.3699 / 18.6995 vs J01 1.4034 /
4.3658 / 18.6717 (q=0/3/10); E[ang] q10 18.6953±0.0161 vs J01 18.6717 (~0.08). **No headline
disagrees with the cited values beyond 3 SE — the loud clause is not triggered.**

## 2. The five verification items

**(1) E[D] vs the exact law** (frozen Theorem 1: E[D]_central = ∫₀¹ r κ dr = τ0(1/2 + q/4)):
q=0: 0.499411 ± 0.000507 vs **1/2** → z = **−1.16** ✓ · q=3: 1.249006 ± 0.001345 vs **5/4** →
z = −0.74 ✓ · q=10: 2.999082 ± 0.002688 vs **3** → z = **−0.34** ✓.

**(2) Mixed moment E[D v²] = 2 E[D·ang]** (per-photon conditional-Gaussian kick identity):
paired per-photon z = mean[D(v²−2ang)]/se = **0.51 (q=0), 1.15 (q=3), −0.17 (q=10)** — all |z|<3 ✓.
Aggregate: E[Dv²]=3.7048±0.0127 vs 2·E[Dang]=2·1.8497=3.6994 (Δ=0.005, ~0.4 SE) at q=0; also holds
at q=3 (22.1727±0.0923 vs 2·11.0418=22.0836) and q=10 (191.899±0.720 vs 192.000±…). Exact.

**(3) Atom-fraction law A = exp(−τ0(1+q/3))**, central:
q=0: 0.367932±0.000341 vs e⁻¹=0.367879 → z=**+0.16** ✓ ·
q=3: 0.135921±0.000343 vs e⁻²=0.135335 → z=**+1.71** ✓ ·
q=10: 0.013153±0.000114 vs e⁻¹³ᐟ³=0.013128 → z=**+0.22** ✓.

**(4) Ratio window −ln A / E[D] ∈ [4/3, 2] with q-dependence (1+q/3)/(1/2+q/4)**:
q=0: −ln A/E[D] = **2.00207 ± 0.00275**, target 2.00000 (z=+0.75) ✓ ·
q=3: **1.59782 ± 0.00265**, target 1.60000 (z=−0.82) ✓ ·
q=10: **1.44414 ± 0.00317**, target 1.44444 (z=−0.09) ✓.
All three sit inside [4/3, 2] (3-SE window straddle; at q=0 the exact value is ON the boundary 2,
as the law requires), and the q-dependence matches the formula at |z| ≤ 0.82 everywhere.

**(5) Volume-source face (J02B)** — uniform-in-ball emission, τ0=1, q=0 (n=1e6):
E[D]_vol = **0.337348 ± 0.000640** vs central 1/2 → **z = −254** (massively different, as required) ·
per-photon identity E[D] = E[τ] − E[Q], Q = (x−x0)·u_final: E[τ]=0.934701±0.000776,
E[Q]=**0.597353 ± 0.000435** (J02B: 0.59715; z=+0.35) → E[τ]−E[Q]=0.337348, z_identity ≈ 2e−13 ✓ ·
independent delay-arithmetic cross-check err = 1.8e−15. Bonus Dynkin check
E[τ]_vol = 0.5 + E[μ_exit] − 3/10: 0.934701 vs 0.5+0.735896−0.3 = 0.935896, z=−1.54 ✓.

## 3. Bottom line

20 numeric laws/headlines checked (28 gates), **28/28 passed**. The JWST moment-channel headline
numbers (0.5008, 2.8061, 3.7316, 0.3679; 3.003, 0.0131) are reproduced by a third, algorithmically
independent motor within 3 SE everywhere; the exact identities they sit on (E[D]=τ0(1/2+q/4),
A=exp(−τ0(1+q/3)), E[Dv²]=2E[D·ang], the [4/3,2] ratio window, E[D]_vol=E[τ]−E[Q] with Q≈0.597)
survive intact. **No discrepancy to report loudly.**