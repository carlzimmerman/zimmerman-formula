# SETUP — External-Upsilon-prior lever on the a0-line (data + prior model)

**Lane:** SETUP/DATA. **Run:** `setup_mlpriors.py` (exit 0) → `setup_mlpriors_results.json`.
**Frozen repo + `prep_2026/a0_line` READ-ONLY; outputs only here.**

**Line under test:** `E ≡ g_obs² − g_bar² = a0·g_bar` (through origin, slope = a0), unique to
the framework's own dS-Unruh interpolation `g_obs = √(g_bar² + g_bar·a0)`
(ν = √(1+1/y) = Milgrom 1999 PLA 253:273 Eq.9; distinctive content = the cH_Λ/Z
coefficient + the MI completion). **Footings:** canonical **9.355e-11** (a0=cH_Λ/Z, pure-Λ)
vs alt **1.1305e-10** (cH₀/Z); gap 20.9%, so splitting at 2σ needs **σ_tot ≤ |Δ|/2 =
9.75e-12**. a0 value + s=−1 remain **postulates** regardless of anything here.

---

## (1) Current Upsilon treatment — verified COHERENT

`fire_common.budget`: `SIG_LNU = 0.23 nat = 0.0999 dex`, injected as
`sysU = KU·a0·SIG_LNU` with `KU = Σ_allpts w·g_bar²·φ·(2y+1)/S` — **one global number,
fully coherent across galaxies** (φ = stellar share of g_bar). Gas-cal `SIG_LNG = 0.10 dex`
is likewise global/coherent. Being coherent, **sysU does NOT average down with N** — it is a
floor.

Banked gas-dominated budget (reproduced from raw data, model-based iterated GLS):

| Ud | N/Ngal | a0_hat | sysU | sysG | sysD | **sysEst** | stat | √(U²+G²) | σ_tot |
|----|--------|--------|------|------|------|--------|------|----------|-------|
| 0.50 | 426/62 | 1.363e-10 | 1.053e-11 | 1.000e-11 | 8.19e-12 | 1.280e-11 | 4.76e-12 | 1.452e-11 | 2.174e-11 |
| 0.70 | 310/49 | 1.181e-10 | 9.57e-12 | 8.63e-12 | 7.63e-12 | 1.044e-11 | 4.67e-12 | 1.288e-11 | 1.903e-11 |

**Coherence proof (Ud=0.7):** the *same* 0.0999 dex applied fully-coherent → 9.57e-12
(= banked); applied fully-per-galaxy-independent → **1.66e-12** (ratio 0.17 ≈ 1/√N_eff,
N_gal=49). So the banked treatment is the **worst case**, and the per-galaxy portion of the
M/L error would already have averaged down hard.

## (2) External per-galaxy Upsilon info — data availability (HONEST)

**None locally.** `sparc_master_clean.csv` = `[name,T,D,fD,inc,L36,MHI,Vflat,Q,ref]`: `L36`
is the [3.6] **luminosity** (not an M/L), `MHI` is HI mass. **No per-galaxy colours** (no
[3.6]−[4.5], no B−V), **no per-galaxy SPS M/L**. The rotmod files carry SBdisk/SBbul at a
**single fixed Upsilon** — SPARC ships one M/L, not a per-galaxy vector. `SPARC_Lelli2016c.mrt`
(local) is the same content (L[3.6], SBeff, Reff, MHI), still no colour/SPS column.

Schombert-McGaugh-Lelli 2019 per-galaxy SPS M/L was **not fetched as a per-galaxy vector**;
we inject the **defensible literature decomposition** instead and flag it honestly (per the
run's ground rules).

**NIR caveat (load-bearing):** at [3.6] the M/L is *"nearly constant"* — ~0.1 dex **total**
scatter (McGaugh-Schombert 2014; Meidt+2014; SML19) — so the per-galaxy **reducible** part is
intrinsically **small**, and a large share of the 0.1 dex is the **coherent SPS/IMF
zero-point that external colours cannot reduce**. The lever's ceiling is low by construction.

## (3) Decomposition prior model → hand to estimator lanes

Split `SIG_LNU` into **σ_coh** (coherent SPS/IMF zero-point, irreducible — if the IMF/SPS
zero-point is off, every Upsilon shifts together; external colours don't touch it) + **σ_pg**
(per-galaxy reducible, SFH/metallicity scatter — external colour/SPS M/L shrinks it, and it
averages 1/√N). Two calibration-preserving scenarios (quadrature ≈ banked 0.0999 dex, so this
**redistributes, never inflates** the budget):

| scenario | σ_coh (dex) | σ_pg,pre | σ_pg,res (post external prior) | quad(coh,pre) |
|----------|-------------|----------|-------------------------------|---------------|
| balanced (task-suggested) | 0.060 | 0.080 | 0.040 | 0.100 |
| nir_realistic (coherent-heavy) | 0.075 | 0.065 | 0.035 | 0.099 |

σ_pg,res ≈ 0.035–0.040 dex = colour-M/L relation precision at [3.6] (Bell-de Jong 2001; SML19)
— the reducible part shrinks to this floor, not to zero.

**Injection** (implemented in `budget_decomp`, algebra byte-identical to fire_common):
- coherent floor: `sU_coh = KU·a0·(σ_coh·ln10)` — global, stuck.
- per-galaxy: `sU_pg = √( Σ_gal (cU_gal·σ_pg·ln10)² )`, `cU_gal = a0·Σ_{pts∈gal} w·g_bar²·φ·(2y+1)/S`
  (same per-galaxy RSS as fire_common's sysD loop; `Σ_gal cU_gal = KU·a0`). Averages ~1/√N.
- `sysU_total = hypot(sU_coh, sU_pg)`; sysG/sysD/sysI/sysEst/stat unchanged.

### Residual floor the estimator lanes must beat (post external prior)

| Ud | scenario | a0_hat | sysU: banked→coh+pg_res=tot | sysG | sysEst | √(U²+G²) pre→post | **σ_tot** | vs 9.75e-12 |
|----|----------|--------|------------------------------|------|--------|-------------------|-----------|-------------|
| 0.7 | balanced | 1.181e-10 | 9.57e-12 → 5.75+0.66=**5.79e-12** | 8.63e-12 | 1.044e-11 | 1.29e-11→**1.04e-11** | **1.74e-11** | NO |
| 0.7 | nir_real | 1.181e-10 | 9.57e-12 → 7.19+0.58=**7.21e-12** | 8.63e-12 | 1.044e-11 | 1.13e-11→**1.12e-11** | **1.80e-11** | NO |
| 0.5 | balanced | 1.363e-10 | 1.05e-11 → 6.32+0.72=**6.36e-12** | 1.00e-11 | 1.280e-11 | 1.19e-11→**1.19e-11** | **2.01e-11** | NO |

## Honest handoff (both ways)

1. **The Upsilon line is coherent → the lever's real gain is the split, not the priors.**
   sysU drops 9.57→~5.8e-12 (balanced, Ud=0.7) **mostly from acknowledging that part of the
   M/L error is per-galaxy and already averages down**; the external colour prior then shrinks
   an already-sub-dominant residual (0.17× coherent). At [3.6] there is little per-galaxy
   signal to buy.
2. **Beating Upsilon does NOT decide the footing.** σ_tot moves only 1.90e-11 → 1.74e-11
   (~9%), still ~1.8× the 9.75e-12 threshold. **The wall shifts to a COMBINATION**: after the
   Upsilon lever the largest lines are **estimator-choice sysEst (1.04e-11) > gas-cal sysG
   (8.63e-12) > the coherent Upsilon floor (5.8–7.2e-12) ≈ sysD (7.6e-12)**. sysEst **alone**
   already exceeds the threshold. → honest outcome **(B/C): TIGHTENS-BUT-NON-DIAGNOSTIC**;
   the residual wall is gas-cal + estimator-choice + the irreducible coherent SPS floor,
   which needs BIG-SPARC count + a better gas-mass calibration + points reaching y~1.
3. **Do not read the sysU collapse as a detection.** The post-prior central still straddles
   both footings (tension canon +1.4σ / alt +0.3σ at Ud=0.7). Carry the verifier's caveat:
   per-point a0 = E/g_bar **declines with g_bar** (ν-shape leaking into magnitude), so the
   GLS-weighted central is not a clean single a0; sysEst stays a real, binding line.

**Credits:** SPARC = Lelli-McGaugh-Schombert 2016. M/L decomposition: Schombert-McGaugh-Lelli
2019, McGaugh-Schombert 2014, Meidt+2014, Bell-de Jong 2001. a0 value + s=−1 = postulates.
