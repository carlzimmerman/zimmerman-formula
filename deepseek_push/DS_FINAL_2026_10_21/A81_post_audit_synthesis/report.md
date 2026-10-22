# A81 — POST-AUDIT GLOBAL SYNTHESIS

**Lane:** A81_post_audit_synthesis · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a81_checks.py` — **27/27 PASS, exit 0, ~30 s from a cold start** · **Output:** `a81.out` · **Data:** `a81_results.json`
**Mutations:** seven (`MUTATE.md`, `a81_MUTATE_*.out`), each one input, each **exit 1**.
**Read:** A71 (the three-channel likelihood), A80 (the SLACS Sérsic-n audit), A85 (the σ_ap channel), A74/A75
(the thermal point and its postulate), A76 (`L*`), A77 (η/γ), A78 (β), A72 (the coefficient), A33 (the action).
Nothing downloaded; nothing committed; no other lane's directory or the docs touched.

**Every number in this report is printed in `a81.out`** (verified mechanically: see §9).

---

## 0. Bottom line

1. **With every parameter profiled at every grid point the joint fit is**
   `kappa_P3 = 0.378081 +- 0.025764 (stat) +- 0.118038 (syst) = 0.378081 +- 0.120817`,
   `a0 = 8.553737e-11 m/s^2`, `B = 1.199647 +- 0.03813`, `u = 0.442872 +- 0.02293`. In the ρ_DE
   convention `kappa_DE = 0.456915`. That is A71's `0.37765 +- 0.02579` to 0.1%, and A51's
   `0.370830 +- 0.026482` shifted by 0.26σ.
2. **The global tension is T = 5.5059 for two shared parameters (p = 0.0637, 1.85σ), and 90.3% of it
   is the IMF prior.** Data-only: `T_data = 0.5333` (0.30σ). The three data channels agree; the
   tension is between the data and Treu's IMF normalisation, whose pull is `+2.04 sigma`.
3. **The thermal point is free; κ_DE = ½ costs Δχ² = 1.824508 (1.3507σ, LR 2.4899 : 1) with B and u
   refit at both points.** A74's 1.863869 survives the full re-run to 2.1%. Neither is a decision.
4. **The lensing channel is κ-blind in its data.** With B profiled, the 70-lens χ² changes by only
   `0.2113` over κ ∈ [0.20, 0.80]; the `9.1069` units of "preference" are the IMF prior acting through
   `B_req(κ)`. Adding SLACS moves the joint κ by `+0.00660` (0.26σ); dropping the cluster channel
   instead moves it to `0.36855`.
5. **The ledger has nine symbols — 2 forced, 1 postulate, 1 atomic-conditional, 2 bounded, 3 free —
   and the three free symbols are one scale, so 2 genuinely free parameters** (η, and one P-sector
   scale shared by γ, `L*`, `σ_c`). Adopting the atomic `σ_c` would make it 1; A76 refuses that adoption.
6. **All seven cross-lane identities hold.** The largest residual is `8.742e-04` (a0 against
   `cH_Λ/2π` through `Λ_obs`), which is the BRIEF's Λ/H0 rounding, not a contradiction between lanes.

---

## 1. What is in the likelihood, and what is not

| channel | data (read-only, hashed) | N | profiled at every grid point | in the fit |
|---|---|---|---|---|
| **SPARC RAR** | `real_research/data/sparc_data/*_rotmod.dat`, sha256(concat) `469f4f556dc813b2` | 171 gal / 3375 pts | **one Υ per galaxy** (240-point window), then compressed to a Gaussian in κ with the 200-draw block bootstrap `0.093888688` | **yes** |
| **SLACS** | `slacs_auger2009_lenses.tsv`, sha256 `d78d7627d6bbcc07` | 70 lenses | **one shared B**, profiled exactly: the full 70-term quadratic in ln B is minimised at every κ | **yes** |
| **clusters** | A18's `R_req = 5.552 +- 0.427` | 1 number | **u**, profiled at every κ | **yes**, flagged circular |
| **σ_ap** (A85) | 70 SDSS fibre dispersions | 70 lenses | imported as `B = B_sigma(κ) +- s_cond`, both widths run | **variant** |
| IMF prior | Treu+2010, 56 lenses | 1 number | — | **yes**, `B = 1.00 +- 0.036 dex` |
| closure `I(y_t) = 8π/κ²` | — | — | — | **no — identity** (C19) |
| Sérsic n | no per-lens n on disk (A80 K2) | 0 | — | **no — not measurable** |

**The SLACS profile is exact, not a mean/SD compression.** With the per-lens response
`r_i = dlnR_E,i/dlnB` (median `0.7775`, scatter `0.08297`), the 70-lens likelihood is
`χ² = Σ_i (ln r_i + r_i lnB)²/S_LN² = A(κ) + 2Bc(κ) lnB + C lnB²`, which is minimised analytically for
B at every κ. The compression is verified against a direct 70-lens evaluation at κ = 0.31:
`60.93600` direct versus `60.93597` spline, a difference of `2.6e-05`. The A70 model is reproduced:
median ratio `0.885232`, max per-lens deviation from A55's stored ratios `0.00e+00`,
`dlnR/dlnB = 0.7775`, `dlnR/dlnκ = 0.1205`, ratio `6.45`, and `B_req(κ = ½) = 1.1738`.

**What the SPARC compression costs, stated.** The raw χ²/dof is `2.2209`; the formal Δχ² = 1 error in
a0 is `1.12688%` and the bootstrap is `0.093888688`, a factor `8.33`. The bootstrap is the declared
error model and it is what enters; §5 and C24 quantify what the alternative would do. **The Υ are
profiled in either case** — the compression is over galaxies, never over Υ.

**Two B estimators, declared.** The exact 70-term profile gives `B_ML = 1.23651` at the thermal point;
the mean-zero estimator `exp(-<ln r>/RESP)` gives `1.22323`, `1.09%` lower. A81 uses the profile (it is
the likelihood's own ML); every comparison with A70/A71/A80/A85 is made like-for-like and reported.

**Sérsic n is not a parameter of this likelihood**, because no per-lens n exists on disk (A80 K2).
A80's n-curve is imported instead: `n_zero = 6.0932`, `n_ML = 14.1421`, `B(n=4) = 1.22799`,
`B(n=6.0) = 1.09854` — a shift of `-0.0484 dex`, which moves the IMF pull from `+2.04 sigma` to below
`1.5 sigma` (§7). The n-variant is therefore a declared systematic band, not a fitted parameter;
A80's own conclusion is that the mass anchor (f\* vs total mass) is undecidable from disk, which is
why n cannot be honestly profiled here.

---

## 2. The joint fit

```
kappa_P3 = 0.378081 +- 0.025764 (stat, Delta-chi2 = 1)      [0.35255, 0.40408]
         = 0.378081 +- 0.118038 (syst, the 31.2% coherent floor)
         = 0.378081 +- 0.120817 (total)
kappa_DE = 0.456915        (kappa_DE(thermal) = 0.460659, 0.12 sigma away)
a0       = 8.553737e-11 m/s^2   (0.83% below the thermal point, 8.56% below kappa = 1/2)
B        = 1.199647 +- 0.03813 (3.2%)   log10 B = +0.07905 dex
u        = 0.442872 +- 0.02293
chi2     = 59.98816 = SPARC 0.3874 + SLACS 54.6462 + clusters 0.1324 + IMF prior 4.8221
```

`B_req(κ_joint) = 1.237887`, so the fitted B is the prior-weighted compromise between 1 and 1.237887,
as it must be; `B = 1.199647` is outside Treu's 95% upper bound `1.1767`.

**Per-channel χ²/dof and pulls at the joint point.**

| channel | raw χ²/dof | compressed | own best fit | pull |
|---|---|---|---|---|
| SPARC | `7137.21 / 3204 = 2.2276` | 0.3874 | κ = `0.35721 +- 0.03354` | **−0.62σ** |
| SLACS | `54.65 / 68 = 0.8036` | 54.6462 | κ = `0.9786 +- 0.3122` | **+1.92σ** |
| clusters | `0.0760 / 1` | 0.1324 | κ = `0.39347 +- 0.04287` | **+0.36σ** |
| IMF prior | — | 4.8221 | B = 1 | **+2.04σ** |

No channel is pulled in κ by more than 2σ; the only >2σ statement anywhere is the IMF normalisation.

**Independent minimiser.** A 3-parameter Nelder–Mead on the same surface (with `A(κ)` and `Bc(κ)`
re-evaluated at every κ, not frozen) returns `0.378081 / 1.199647 / 0.442872 / 59.98816` — identical to
the profile at the quoted precision. The optimum is not a minimiser artefact.

**The κ information is the cluster channel's, not SLACS's:**

```
SPARC alone           kappa = 0.35721 +- 0.03354
SPARC + SLACS         kappa = 0.36855 +- 0.03304
SPARC + clusters      kappa = 0.37148 +- 0.02581   (the joint without SLACS)
all three             kappa = 0.37808 +- 0.02576
```

Adding SLACS moves κ by `+0.00660` (0.26σ) and tightens σ(κ) by 0.16% (0.02581 → 0.02576); the real
tightening, from 0.03304 (SPARC+SLACS) to 0.02581, is the cluster band — which A18 itself calls a
consistency band, not a measurement.

---

## 3. The global tension and its decomposition

```
chi2_joint             = 59.98816
sum of channel minima  = 54.48231   (SPARC 0, clusters 0.0000, SLACS+prior 54.4823)
T = 5.5059 for 2 shared parameters -> p = 0.0637 (1.85 sigma)
decomposition: SPARC +0.3874 + SLACS +4.9860 + clusters +0.1324 = 5.5059
IMF prior at the joint 4.8221 (0.1174 at the SLACS-only minimum)
data-only refit: kappa = 0.37189, B = 1.24058, chi2 = 54.27729, T_data = 0.5333 (0.30 sigma)
T_prior = 4.9725 -> 90.3% of T
```

**The three data channels agree at 0.30σ.** The whole tension is the IMF normalisation: the joint fit
needs `B = 1.199647`, `+0.07905 dex` above Treu's mean, `2.04 sigma` on the `0.03874 dex` quadrature,
and outside his 95% bound. That is A71's 1.97σ, sharpened by 0.07σ — the exact 70-term profile needs
slightly more mass than the mean-zero estimator did.

---

## 4. Thermal vs κ = ½, everything profiled

```
thermal:   kappa_P3 = 0.381262 (a0 = 8.625700e-11) -> B = 1.19851, u = 0.44436, chi2 = 60.00336
kappa=1/2: kappa_P3 = 0.413453 (a0 = 9.354000e-11) -> B = 1.18720, u = 0.45905, chi2 = 61.82786
Delta-chi2(1/2 - thermal) = +1.824508 -> 1.3507 sigma -> LR 2.4899 : 1
decomposition: SPARC +2.2983, SLACS+prior -0.6013, clusters +0.1275
```

The free fit sits `-0.12 sigma` (stat) from the thermal point and `1.37 sigma` from κ = ½. The thermal
point's cost against the free fit is `0.015199` in χ². A74's numbers — Δχ² `1.863869` → `1.3652 sigma`,
LR `2.5394` — are reproduced to 2.1% and 2.0% respectively, the small shift coming from the scatter
term and the exact profile now in the SLACS leg.

**The convention trap, again.** There are two "½"s and they are different theories:

| target | a0 | κ_P3 | Δχ² vs thermal | distance |
|---|---|---|---|---|
| thermal (`κ_DE = Z/4π = 0.460659`) | `8.625700e-11` | `0.381262` | 0 | `0.12 sigma` |
| `κ_DE = ½` (this lane's rival) | `9.354000e-11` | `0.413453` | `+1.824508` | `1.37 sigma` |
| `κ_P3 = ½` (A71's old target) | `1.1312e-10` | `0.499998` | `+20.7964` | `4.56 sigma` |

The rival that matters for the coefficient is the second row; the third is A71's `κ_P3 = 0.5`, which is
`31.14%` above the thermal a0 and is a different claim. `κ_DE(a0_half) = 0.499662147`, i.e. ½ to
`2e-3`, exactly ½ only if `Ω_Λ = 32π/147 = 0.683884115`.

---

## 5. Is the lensing channel κ-blind? With and without SLACS

**Its data are blind; its prior is not.**

```
joint WITH SLACS             kappa = 0.37808 +- 0.02576
joint WITHOUT SLACS          kappa = 0.37148 +- 0.02581      shift +0.00660 (0.26 sigma)
SLACS DATA alone (B profiled, prior dropped), kappa in [0.20, 0.80]:
                             54.2138 -> 54.0025, Delta = +0.2113
with the IMF prior           63.9399 -> 54.8331, Delta = +9.1069, of which the prior supplies +8.8955
SLACS-only minimum           kappa = 0.9786 +- 0.3122, range [0.686, 1.310]
```

So A80's conclusion stands and is now quantitative: **the 70-lens data carry Δχ² = 0.2113 of κ
information over the whole band** (A80's own number for the same statistic was `0.2854`; A71's `6.3517`
was computed at B = 1 and is an unprofiled-B artefact — reproduced here in both forms, see §9/C8).
The `9.1069` that looks like a κ preference is the IMF prior: `B_req(κ)` falls from `1.3230` at κ = 0.20
to `1.0852` at κ = 0.80, so a high κ relieves the IMF tension without any datum changing. That is why
the SLACS-only "measurement" lands at `0.9786`, in a direction `6.45` times weaker than its B
direction, and why adding it to the joint moves κ by 0.26σ.

---

## 6. The A85 σ_ap channel: what it changes

Audited first: A85's 2×2 Fisher `[[10235.6, 949.3], [949.3, 102.0]]` has determinant `1.4286e+05`
(A85 `1.4278e+05`), condition number `746.04`, `sigma(κ)` from F alone `0.26767` (A85 `0.26774`),
improvement over R_E alone `2.351`, and the angle between the constraints `3.0798 deg` (A85 `3.0788`)
using A85's own derivatives. With A70/A71's lensing response the same angle is `4.6221 deg` — the
"3.08 deg" is solver-specific, and both values say "nearly parallel". A85's σ_ap-alone
`sigma(κ) = 0.7318` fixes the conditional width `s_cond = 0.04731` (formal) or `0.13490` (inflated by
A85's `2.8516`).

```
sigma_ap formal (s_cond = 0.04731): kappa = 0.37768 +- 0.02572, B = 1.20549, chi2 = 60.0599, Delta(1/2 - thermal) = +1.8688
sigma_ap honest (s_cond = 0.13490): kappa = 0.37801 +- 0.02576, B = 1.20064, chi2 = 60.0003, Delta(1/2 - thermal) = +1.8320
B shift: +0.49% (formal), +0.08% (honest) ; kappa shift: -0.00040 / -0.00007
IMF pull: 2.10 sigma (formal) / 2.05 sigma (honest)
```

**The σ_ap channel moves B toward A85's `1.22688` by 0.5% at most and leaves κ where SPARC put it.**
It neither breaks the B–κ degeneracy nor relieves the IMF tension — it slightly worsens it, because
the aperture dispersions prefer `B_sigma = 1.21748` at the thermal point, above the prior-weighted
`1.199647`. A85's own headline `B = 1.22688 +- 0.00433 +- 0.01235` is the R_E + σ_ap fit *without* the
IMF prior; with the prior in, the same data land at `1.20549`. Both are correct statements about
different likelihoods.

---

## 7. TASK 2 — the definitive parameter ledger

Nine symbols, five classes, each symbol in exactly one class. The evidence column is the computed
number and its lane; nothing here is called derived that A75–A78 proved is a postulate, bounded or free.

| symbol | class | value | evidence (lane + number) |
|---|---|---|---|
| **K** | **FORCED BY ACTION** | `8.387173e-10 m^3 kg^-1 s^-2` (4πG) | the static Poisson limit `G_N = K/4π`; the identity `2c_s²/(Kρ_c) = L*²` holds to `0.0e+00` at 4πG and fails by exactly 2 at 8πG (`c_s` would be `1.07909` m/s instead of `0.76303` m/s, a factor `1.41421`) — A76 K1, mutated there |
| **α** | **FORCED BY ACTION** | `α/γ = 1` exactly | one coefficient in front of both gradient operators: α = γ is forced (A68 D10/D12, the 3×3 rescaling determinant 4); only the common scale is free |
| **γ** | **UNCONSTRAINED FREE SCALE** | `6.6606e-07 eV^-4` at `L* = 25.42 pc`, ×`14.06` over the [24, 90] pc window | `γ = KL*²/2` is a definition (A76 K1); no observable measures γ alone — the elastic force is `(L*/r)²`, O(1) only inside 24 pc (A76 §4.4); A33's "M" is downgraded by A76 |
| **η** | **UNCONSTRAINED FREE SCALE** | bounded only by `η ≥ γ` (luminality) | A77 verdict (b): no Kubo/transport matching exists; `γ/η` is free over `(0, 1.916e-07]` (one-sided), a factor `1.335776e+08` of ignorance; the P modes are unpopulated, uncoupled and unsourced |
| **β** | **BOUNDED BY BBN/BACKGROUND** | `β < 0.0280`; `Λ_bare/Λ_obs ∈ (1.000000, 1.061341)` | `ΔN_eff = -11.1738 β/(1+1.5β) > -0.30 → β < 0.0280` (A78 C29); `β = 0` exactly at `Λ_bare = Λ_obs` (A78 C05) |
| **a0** | **FIXED BY THE P-therm POSTULATE** | `8.6257e-11 m/s²`; `κ_DE = Z/4π = 0.460658866` | A75: the gate is athermal at fixed drive (`C_g = 0`), the action's carrier misses the thermal wavelength by `1.989424e+09`, and A72's formula is mass-independent. P-therm is a **postulate**; it forces `R = 3π/2 = 4.712388980 ∉ {1,2,4}` and `Λ_pred/Λ_obs = 8/(3π) = 0.848826363` |
| **L\*** | **UNCONSTRAINED FREE SCALE** | `25.4203 pc` if `σ_c = 8.2255 km/s`; window [24, 90] pc | A76: `L* = σ_c²/a0` has coefficient exactly 1, but **zero measured determinations of σ_c exist on disk**; the 24 pc floor is `23.4289` pc rounded up. `L*` is `FITTED(σ_c)` |
| **σ_c** | **DERIVED FROM ATOMIC INPUT** *(conditional)* | `8.22551 km/s` at T = 10⁴ K, μ = 1.22; `L*` runs `22.1520`–`51.6880 pc` over μ ∈ [0.60, 1.40] | A76 K4: `σ_c = sqrt(k_BT/μm_H)`; **conditional** — A76 §3.1 finds zero measured determinations and μ is unmeasured (factor 1.528 in σ_c, 2.333 in `L*`), so this is an astrophysical premise, not a derivation in force |
| **Λ_bare** | **BOUNDED BY BBN/BACKGROUND** | `Λ_bare/Λ_obs ∈ (1.000000, 1.061341)` | A78 C05/C29/C30: `3(2+3β)H² = 2Λ_bare c² + 4Kρ`; with β < 0.0280 the bare vacuum is within 6.13% of the observed one |

**Counts: 2 forced, 1 postulate, 1 atomic-conditional, 2 bounded, 3 free symbols — and 2 independent
free parameters.** The three "free" symbols are one degree of freedom: the log-Jacobian of
`γ = KL*²/2`, `σ_c² = a0L*` has rank 2 of 5, and over the free block `(γ, L*, σ_c)` it has nullity 1
with null vector `(+1.0000, -0.5000, +0.2500)`, i.e. `|dlnγ| = 2|dlnL*|` and `|dlnσ_c| = 0.5|dlnL*|`.
So the honest count is **η plus one P-sector scale = 2**, not four. If the atomic `σ_c` were adopted as
an input the count would fall to **1** (η alone); A76's finding that σ_c is unmeasured is exactly the
refusal of that adoption.

**The two known tensions, stated in the ledger itself.** (i) `L*` has no measured `σ_c` (A76) — the
ledger therefore does not call `L*` derived, and its number is conditional on an unmeasured μ.
(ii) `η/γ` has no matching principle (A77) — nothing in the action, the Γ = 2 equation of state, the
de Sitter temperature or the Gauss law fixes it, so η stays an unconstrained scale.

---

## 8. TASK 3 — the identity audit

Seven identities, all evaluated on the ledger's own numbers:

| identity | computed | residual | verdict |
|---|---|---|---|
| `κ_DE = Z/4π = sqrt(2/(3π))` | `0.460658865962` from both routes | `0.0e+00` | **holds** |
| `a0 = cH_Λ/2π` | `8.618165900e-11` (Λ_obs route), `8.623833238e-11` (H0 route), deployed `8.625700e-11` | `8.742e-04` / `2.165e-04` | **holds at 1e-3** |
| `I(y_t) = 8π/κ_DE²` | target `118.435253` → `y_t = 77.876356` | `1.6e-13`; two quadratures `6.8e-12` apart | **holds** (`y_t ∈ [60, 140]`) |
| `L* = σ_c²/a0` | `σ_c = 8.22551 km/s` → `25.42031 pc` | `0.0e+00` | **holds** |
| `β = (2/3)Ω_Λ(r_Λ − 1)` | `r_Λ(β = 0) = 1.000000000`; `r_Λ(0.0280) = 1.061341` | `< 1e-9` | **holds** |
| `ΔN_eff = -11.1738 β/(1+1.5β)` | `-0.30026` at β = 0.0280; inverts to `β = 0.02798` at −0.30 | `< 2e-3` | **holds** |
| `B(n=4)`: A80 vs A85 | `1.22799` vs `1.22688` (`+0.09%`, `0.01 sigma`) | within errors | **holds** |

**No identity fails.** The largest residual is the `a0 = cH_Λ/2π` one at `8.742e-04`, and it has a
single cause: the BRIEF's `Λ_obs = 1.0890e-52` implies `Ω_Λ = 0.684996`, whereas A71 uses `0.6847`;
the deployed `8.625700e-11` sits between the two routes and implies `κ_DE = 0.461062` against the
algebraic `0.460659`. That is a constants-rounding statement (0.09%), not a conflict between A72, A75
and A81, and it moves no fit (the fit is in κ_P3, where the thermal point is `0.381262` either way).

**Three further cross-checks, no contradiction found.**

1. **`y_t` vs A74.** A81 gets `77.876356`; A74 published `77.943961`. The difference (0.087%) is the
   same `κ_DE` rounding: A74 evaluated the closure at the a0-implied `0.460454`, A81 at the algebraic
   `0.460659`. Both are inside `[60, 140]`.
2. **`L*` vs A74.** A74's `26.087 pc` uses `σ_c = 8.33 km/s`, the inversion of the 24 pc floor; the
   atomic width `8.22551 km/s` gives `26.07024 pc` at the same a0 (0.06%) and `25.42031 pc` at A81's
   thermal a0. A74's number inherits A65's circular `σ_c`, which A76 withdrew as evidence — a
   provenance issue, not an arithmetic one.
3. **The A80/A85/A81 B triangle.** A80's `1.22799` and A85's `1.22688` (headline, R_E + σ_ap) agree to
   `0.09%`; A85's own R_E-only value is `1.24006`, and A81's 70-term profile is `1.23651`, `-0.29%`
   from it. The three solvers agree to 1%, with the residual scatter in the estimator definitions
   (profile vs mean-zero vs scatter-profiled), all inside the declared `0.0387 dex` quadrature.

**The one identity that cannot be audited** is the `L* ↔ γ/η` one: A77's `λ_C = sqrt(η/K) = L*/(√2 c_T)`
requires `c_T = σ_c`, an identification with no principle behind it. A81 can only check its arithmetic
(`611.7142 kpc` against A77's `611.0801`, `0.104%`); whether it *should* hold is exactly what A77
answered "no" to.

---

## 9. Checks (27/27) and mutations (seven)

| id | what it proves | measured |
|---|---|---|
| C1 | the three data blocks are the record's | 175/171/3375 sha `469f4f556dc813b2`; 85/70; 56 Treu |
| C2 | the SPARC likelihood is the record's | `6.8651 / 6.6312 / 2.4714` |
| C3 | SPARC alone lands on A51 | `8.081465e-11`, `0.357207`, `2.2209` |
| C4 | bootstrap vs formal error | `0.093888688` vs `1.12688%`, ratio `8.33` |
| C5 | the two fixed points and the convention map | `0.460658865962`; `0.381262`; `0.413453`; `0.499662147` |
| C6 | the A70 lensing model, per lens | `0.885232`; max dev `0.00e+00`; `B_req = 1.1738` |
| C7 | the two responses | `0.7775` / `0.1205` / `6.45` |
| C8 | A80's 6.35 is an unprofiled-B artefact | `6.3517` at B = 1 vs `0.3985` profiled (ratio `15.9`) |
| C9 | A18's cluster anchor and κ_CL | `1.6863 / 3.7702 / 2.6179`; `0.3934 +- 0.0432` |
| C10 | A85's Fisher is internally consistent | det `1.4286e+05`, cond `746.04`, `0.26767`, `3.0798 deg` |
| C10b | the imported σ_ap width reproduces A85's margin | `1.21748`; `s_cond = 0.04731`; `0.73180` |
| C11 | three solvers agree on B(n=4) | `1.22799 / 1.22688 / 1.23651` |
| C12 | the joint fit is not a minimiser artefact | profile == Nelder–Mead; `2.6e-05` spline error |
| C13 | per-channel χ²/dof and pulls | `2.2276 / 0.8036`; `−0.62 / +0.36 / +1.92 / +2.04` |
| C14 | the tension and its prior/data split | `5.5059`; prior `90.3%`; data `0.5333` |
| C15 | thermal vs ½ with everything profiled | `+1.824508` → `1.3507 sigma`, LR `2.4899` |
| C16 | lensing is κ-blind in its data | `+0.00660`; data `0.2113`; prior `8.8955` |
| C17 | what σ_ap changes | B `+0.49%` / `+0.08%`; κ `−0.00040` |
| C18 | `a0 = cH_Λ/2π` | `8.742e-04` / `2.165e-04` |
| C19 | `I(y_t) = 8π/κ²` | `77.876356`; residual `1.6e-13` |
| C20 | `L* = σ_c²/a0` | `25.42031 pc`; μ band `22.1520`–`51.6880` |
| C21 | `β` from the background and `ΔN_eff` | `1.000000000`; `-0.30026`; `0.02798` |
| C22 | the ledger's rank | rank 2/5; nullity 1; `(+1.0000, -0.5000, +0.2500)` |
| C23 | the error budget | sys `0.312203`; total `0.12082` (32.0%) |
| C24 | the error-model factor | raw Δ `115.892` → `7.22 sigma` vs `1.3507 sigma` (ratio `28.6`) |
| C25 | the ledger is complete | 9 symbols → 2 independent free |
| C26 | every imported anchor re-derived | A74 `1.3652 sigma`/`2.5394`; A80 `6.3517`/`0.2854`; A85 `2.27 sigma` |

**Mutations, all exit 1** (matrix and exact failing sets in `MUTATE.md`):

| mutation | what it changes | checks killed |
|---|---|---|
| `unprofile_B` | B fixed at the lensing value, prior not marginalised | C12, C16, C17 |
| `no_boot` | the formal Δχ² = 1 SPARC error instead of the bootstrap | C15, C23, C24 |
| `thermal_off` | `cH_Λ/π` instead of `cH_Λ/2π` (the factor-2 slip) | C5, C10b, C11, C15, C18, C19, C20, C23 |
| `imf_prior` | Treu's prior widened to 0.100 dex | C12, C13, C14, C17 |
| `drop_sigma_ap` | the A85 σ_ap term removed from the likelihood | C17 |
| `sersic_default` | the SLACS baseline at n = 6 instead of n = 4 | C11, C13, C16 |
| `vacuum_beta` | the `Ω_Λ,eff = 1` slice (A33's 1.462 floor) | C21 |

Every check is a comparison between two independently computed numbers, a lane's published number, or
a physics threshold — no check is a closed-form target decoupled from the quantity it tests, and no
check reads A79. The report's number-to-output mapping was verified mechanically: every numeric token
in this file appears literally in `a81.out`.

---

## 10. What this does not do

1. **It does not re-derive the systematics.** The `0.208386` estimator half-span is A51's 7-estimator
   ensemble; it is carried, not re-run. It is `42.5%` of the variance and it dominates every
   "cannot tell" here.
2. **It does not profile Sérsic n**, because no per-lens n exists on disk. A80's n-curve is imported as
   a systematic band (`-0.0484 dex` in B, `6.0932` zeroing the shape residual, `14.1421` at the ML),
   and A80's own conclusion — that the mass anchor is undecidable — is why.
3. **The σ_ap channel is imported, not solved.** Its central value `B_sigma(κ)` and its width come from
   A85's 12-point sweep and its published Fisher; A81 audits the Fisher (C10/C10b) and re-runs the
   joint fit with the term, but does not re-run the Jeans solver.
4. **The cluster channel is circular** (`u` and `R_req` from the same amplitudes). It is the channel
   that tightens σ(κ) from `0.03354` to `0.02576`; nothing here would survive its removal at the
   quoted precision, and A18/A51/A71 all flag it.
5. **The error model decides everything numeric.** On the raw SPARC χ² the thermal point beats κ = ½ by
   `115.892` → `7.22 sigma`; on the declared bootstrap it is `1.3507 sigma`, a factor `28.6` in χ².
   Every "cannot tell" in §4 is conditional on the bootstrap being the right error.
6. **No new data, no new theory.** Nothing downloaded; every file read-only and hashed; `THEORY.md`,
   `README.md` and `STATUS_BOARD.html` are the coordinator's and untouched.

---

## VERDICT

**One parameter set, every parameter profiled, three data channels plus the IMF prior and an optional
σ_ap term: `κ_P3 = 0.378081 ± 0.025764 (stat) ± 0.118038 (syst)`, `a0 = 8.553737e-11 m/s²`,
`B = 1.199647 ± 0.03813`, `u = 0.442872 ± 0.02293`, with `T = 5.5059` for two shared parameters
(`1.85σ`) of which `90.3%` is the IMF prior and only `0.5333` (`0.30σ`) is the data. The thermal point
`κ_DE = Z/4π = 0.460659` is free — the fit sits `-0.12σ` from it and pays `0.015199` in χ² to be there —
while `κ_DE = ½` costs `Δχ² = 1.824508` (`1.3507σ`, LR `2.4899 : 1`); A74's `1.863869` is reproduced to
2.1%, and the old `κ_P3 = ½` target is `4.56σ` away and is a different theory. The lensing channel is
κ-blind in its data (`0.2113` over the whole band) and its apparent `9.1069` is the IMF prior; adding it
moves κ by `0.26σ`. The σ_ap channel moves B by at most `0.49%` and κ by `-0.00040` — it breaks
nothing and confirms nothing. **The ledger has nine symbols: `K` and `α` forced, `a0` fixed by the
P-therm postulate, `σ_c` atomic-conditional, `β` and `Λ_bare` BBN-bounded, and `γ`, `η`, `L*` free —
which collapse to two genuinely free parameters, η and one P-sector scale, and to one if the
unmeasured `σ_c` is adopted. All seven cross-lane identities hold, the largest residual
`8.742e-04` being the BRIEF's Λ/H0 rounding. The theory's remaining ignorance is exactly two numbers,
one of which (η) has no matching principle and one of which (`L*`/`σ_c`) has no measurement.**
