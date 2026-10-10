# CFG556: a resolution-free halo model of the gravitating matter power. Verdict: INTRINSIC on both footings (VARIANT-SENSITIVE to the emergent edge and to the catchment scope)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (77ec620e0). Date: 2026-10-10.
- **Script:** `cfg556_halo_model.py`, about 15 s. `OMP_NUM_THREADS=4 nice -n 10 python3 cfg556_halo_model.py` writes `cfg556_halo_model.out` and `cfg556_results.json`. `CFG556_MUTATE=1` writes `_MUTATE.out` / `_MUTATE.json` and exits 1 when all teeth bite (they do).
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled; flat a0; kernel ν(y) = 1/(1 − e^−√y). The cold energy's MASS is still required; no particle species. This is not "theory closed". No PM run and no download. CFG555's caches, the S0 JSONs and CFG515's `fret_of` were read only.
- **Inputs:** the PM's own Eisenstein–Hu no-wiggle spectrum (copied verbatim from `cfg361_pm.py`, σ8 = 0.811); Tinker08 mass function and Tinker10 bias (Δ = 200m); NFW with Duffy08 c200m; turnaround radius at Δ_ta = 11.81; census f_ret from CFG416; Moster13 stars (Hernquist) and β-model gas. All numbers below come from `cfg556_results.json` / `_MUTATE.json`.

## The answer

**The excess is in the framework's halo profiles, not only in the PM bookkeeping.** In candidate B with the census edge (R2) and the shell draw (R5), each halo's whole catchment cold supply, (1 − f_b) M_ta, settles inside r_e ≈ 0.26–0.40 r_ta. That is about r200m. ΛCDM keeps only about 0.55 M_ta inside that radius. So at the same turnaround mass the framework's halo is far more concentrated on the 0.2–0.5 r_ta scale: M_F/M_L at 0.3 r_ta is 1.25–1.75 (canonical) and 1.39–1.76 (alt). It is less concentrated in the very core: 0.40–0.99 at 0.05 r_ta.

**Halo-model ratio R(k) (primary: census f_ret, census edge, all halos):**

| k [h/Mpc] | 0.1 | 0.2 | 0.3 | 0.35 | 0.5 | 0.7 | 1.0 | 2.0 | 3.0 | σ8 ratio |
|---|---|---|---|---|---|---|---|---|---|---|
| canonical | 1.008 | 1.044 | 1.124 | 1.180 | 1.375 | 1.589 | **1.716** | 1.532 | 1.279 | 1.0402 |
| alt | 1.008 | 1.049 | 1.140 | 1.204 | 1.431 | 1.696 | **1.885** | 1.788 | 1.551 | 1.0463 |

**Variants (E = max(R − 1), D = min(R − 1) over 0.05 ≤ k ≤ 1; "ratio form" = P_F,ta/P_L,ta):**

| variant | canonical E / D (ratio form E) | alt E / D (ratio form E) | σ8 ratio can / alt |
|---|---|---|---|
| census edge (PRIMARY) | +0.715 / +0.002 (+0.553) | +0.883 / +0.002 (+0.683) | 1.0402 / 1.0463 |
| CFG544 softened, 25% | +0.671 (+0.519) | +0.838 (+0.648) | 1.0381 / 1.0444 |
| CFG544 softened, 55% | +0.572 (+0.442) | +0.737 (+0.569) | 1.0331 / 1.0399 |
| f_ret = 1 (the PM runs' retention) | +0.882 (+0.682) | +1.047 (+0.809) | 1.0470 / 1.0527 |
| emergent edge (untruncated gas) | **+0.077** / −0.009 (+0.049) | **+0.146** / +0.001 (+0.097) | 1.0072 / 1.0124 |
| catchment = r200m ball (r200m scope) | −0.000 / **−0.081** | −0.000 / −0.047 | 0.9973 / 0.9985 |

**Drivers.** At k = 1, ΔR is +0.715 (canonical). Of that, log M_ta 14–15 gives +0.567 (one-halo) and +0.022 (two-halo); 13–14 gives +0.056; 15–16 gives +0.061. At k = 0.35, 14–16 gives about 90% of ΔR. So group and cluster halos drive it, on radii 0.2–0.5 r_ta (≈ 0.6–2 Mpc/h). The shell is strongly drained there: q = 0.76 / 0.90 / 0.96 at log M_ta 13 / 14 / 15.

## Comparison with CFG555's PM (gravitating field)

**Frozen test: the PM-matched halo model** (f_ret = 1, census edge, framework only above the PM's resolved mass) against the CFG424-family runs. The result is **NOT REPRODUCED for all seven runs**, and it fails in one specific way:
- **At the PM's peak, k ≈ 0.32, the halo model matches the PM almost exactly.** R3 canonical: PM 1.163 vs HM 1.162 (fraction 0.99). DE: 1.167 vs 1.162. CFG518: 1.150 vs 1.162. Alt at k = 0.41: 1.193 vs 1.325 (fraction 1.69).
- **At k = 1 the signs disagree.** The PM is 0.80–0.87; the halo model is 1.88 (canonical) and 2.05 (alt).
- CFG460 peaks at k = 0.97 (0.816), so its fraction is −4.76.
- The 256³ runs fall short of the halo model at every k > 0.2 (k = 0.35: 1.075 vs 1.201).
- The σ8 ratio agrees closely: halo model 1.040 / 1.046 (primary), PM 512³ 1.0405 / 1.0459.

**Reading.** The PM's excess at k ≈ 0.3–0.4 is what the law's profiles predict. The PM's **deficit** at k ≈ 1 is not predicted by the profiles. The halo model makes R rise to k ≈ 1 instead. That deficit is where CFG526 already found the old per-catchment draw robbing the cores (engine core R 0.65–0.77 of the law's mass, deepening with resolution). So the k ≈ 1 deficit is an artefact of the CFG424-family draw. But removing that artefact makes the excess **larger**, not smaller.

**Post-freeze cross-check (2026-10-10; reported, not a verdict input).** CFG530 runs the R5 law-respecting engine, whose halos match the law's profile (core R 0.94–0.98). Its gravitating ratios (from `cfg555_results.json`) are compared with the primary halo model:

| CFG530 run | r(0.5) PM / HM | r(1) PM / HM |
|---|---|---|
| L200 N512 can | 1.499 / 1.375 | 1.384 / 1.716 |
| L200 N512 alt | 1.546 / 1.431 | 1.408 / 1.885 |
| L100 N512 can | 1.485 / 1.375 | 1.487 / 1.716 |
| L100 N512 alt | 1.558 / 1.431 | 1.560 / 1.885 |

The law-respecting PM has an **excess at k = 1** and sits within about 10% of the halo model at k = 0.5. This supports the reading that the excess is intrinsic and that the CFG424-family k ≈ 1 deficit was the draw.

## Verdict per footing (frozen rule)

- **canonical: INTRINSIC.** E = +0.715 at k = 0.99.
- **alt: INTRINSIC.** E = +0.883 at k = 0.99.
- **VARIANT-SENSITIVE (stated plainly):**
  - **The emergent edge** gives +0.077 on canonical (within 10%, so the ARTEFACT class) and +0.146 on alt (+0.097 in ratio form). That variant leaves the declared β-model gas untruncated out to r_ta (ρ ∝ r⁻² outside 0.1 r200c), so a large share of the baryons sits outside the census edge. The phantom then exhausts the supply further out (r_e 0.42–0.53 r_ta, q 0.59–0.68), and the settled mass is spread over a wider shell. This variant's size is set by the declared outer gas shape, which was not fitted.
  - **The r200m scope** (catchment = r200m ball, supply (1 − f_b) M200m) gives a deficit instead: −8.1% / −4.7% at k = 1. With the virial mass only, the law's isothermal profile is *less* concentrated than an NFW cusp. **So the sign of the effect is set by how much cold energy the catchment supplies.** The framework's declared catchment (R2/R5) is the turnaround ball; r200m scope is a bracket for halo-model double counting, not the framework's rule.
- **What "intrinsic" means.** It applies to the framework as now written: the R2 edge exhausts the whole turnaround catchment, and R5 draws from the shell. The supply amount (A6) is itself still inherited, not derived (CFG541).

## Observational implication (context only; literature values recalled, PROVISIONAL)

- With the census edge, the gravitating matter power is up by 12–14% at k = 0.3, 38–43% at k = 0.5 and 72–89% at k = 1 h/Mpc. The nonlinear σ8 is up by 4.0–4.6%.
- Cosmic shear (KiDS, DES) weights k ≈ 0.1–5 h/Mpc. The recalled values are KiDS-1000 S8 ≈ 0.76, DES Y3 ≈ 0.78 and Planck ≈ 0.83, and the recalled A_mod ≈ 0.82–0.86 (CFG526). So the data already sit *below* the ΛCDM-equivalent small-scale power. The framework's halos push the other way, adding power where lensing sees a deficit.
- Read at face value, the predicted effective S8 moves up, away from the lensing measurements, unless something else (baryonic feedback is not in candidate B's cold-energy profile) removes more than the excess. This is a serious tension for the current settling rules, not a detection. It points at the supply rule: the whole catchment settling inside about r200m.
- Cluster-scale lensing masses at fixed turnaround mass would also be 1.3–1.75× ΛCDM's inside 0.3 r_ta. This is the same physics as CFG546's inner excess.

## Validation and controls

- **ΛCDM halo model vs our S0 PM:**
  - 256³, k 0.1–1: ratio 0.871–1.090. **GOOD** (±20%). σ8: HM 0.9011 vs S0 0.9064.
  - 512³, k 0.1–2: 0.873–1.223. **POOR.** The misses are k = 2 (1.223), where the PM lacks resolution-limited small-scale power, and k = 0.2 (1.167), where box sample variance shows.
  - The usual halo-model transition deficit (0.87–0.90 at k ≈ 0.3–0.5) is present.
  - The verdict uses ratios, so absolute agreement is not required. POOR is stated beside the verdict.
- **C1** σ8(P_lin) = 0.81109 (1.1e-4): PASS.
- **C2** I(k = 1e-3) = 1 to 4.3e-7 (ΛCDM) and 3.4e-7 (framework): PASS.
- **C3** mass conservation inside r_ta: 1.1e-16: PASS.
- **C4** numerical vs analytic truncated NFW transform: 7.0e-6: PASS.
- **C5** (reported) P_lin vs the S0 z_i spectrum / D²: median 1.009 (256³) and 0.990 (512³).
- **MUTATE (all bite):**
  - **M1:** framework profile = NFW gives |R − 1| = 0.
  - **M2:** removing the edge (bare law to r_ta, no cap) raises E to +9.7 / +12.0. The ball then holds 2.4–3.3 M_ta.
  - **M3:** removing the drained shell changes R over k 0.3–1 by up to 1.24 / 1.39 (the ball gains mass).

## Disclosures (dated 2026-10-10)

- **CFG544 softened variants.** Mass conservation needs the taper amplitude at r1 rescaled by a factor A, recorded per halo. A ≈ 1 for an isothermal settled profile; the frozen text says "from its E-cen value at r1".
- **Bare-law MUTATE.** Read as "the law everywhere inside r_ta, nothing else". With no edge there is no shell.
- **"Reproduces the 512³ run(s)".** Read as "any 512³ run of that footing". None did.
- **CFG518 DC-can 512³.** It uses census retention. The frozen PM-matched model uses f_ret = 1 for every run; the census primary at k = 0.32 is 1.142 against the PM's 1.150.
- **The post-freeze CFG530 block** was added after the verdict and does not enter it.
- **Halo-model double counting.** The extended NFW puts 1.75 M200m inside r_ta (mean over 1e12–1e15). The primary therefore inflates both ta spectra; P_L,ta/P_L,std = 1.29 at k = 1. The ratio form (E 0.55 / 0.68) and the r200m scope bracket this.
