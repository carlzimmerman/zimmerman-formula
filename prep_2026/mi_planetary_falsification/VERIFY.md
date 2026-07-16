# VERIFY — MI planetary falsification (adversarial, both ways)

**Date:** 2026-07-16. **Verdict: UPHELD.** The lane's finding — *SURVIVES CONDITIONALLY; the surviving
~Myr crossover corner is a FREE 5th constant, not a forced scale* — holds under independent re-derivation.
Neither a manufactured save nor a manufactured deficit was found. Companion: `verify_independent.py`
(numpy only, exit 0, no hard-coded verdict booleans; every number rebuilt from first principles).

## 0. Reproduction + hygiene
- `window_joint.py` exit 0, ALL CHECKS PASS; `origin_window_scales.py` exit 0, ALL CHECKS PASS;
  `verify_independent.py` exit 0, ALL CHECKS PASS.
- Hard-coded-check grep over all 3 scripts: **0** `check(...,True/False)` literals, **0** verdict vars
  set to a bool literal. `PASS=True`/`PASS=False` are the standard accumulator init/fail only. The
  `forced=True/False` kwargs in `origin_window_scales.py` are physics *labels* (is the candidate a theory
  constant?), not window verdicts — the "lands in window" test they feed is computed.

## 1. Per-planet δg re-derived independently (Gauss secular equation) — HONEST, not inflated
Derived the constant-radial-accel bound from scratch: for a constant sunward A_r, Gauss gives
dω/dt = −(A_r/e)√(p/GM) cos f; the **time-average ⟨cos f⟩_t = −e** (verified numerically to 1e-3 at
e=0.093 and e=0.206), so ⟨ω̇⟩ = A_r√(p/GM) ⟹ **A_r = |ω̇|·√(GM/p)**, p=a(1−e²). Feeding FM24 Table 10
perihelion σ's (mas/yr) reproduces the banked δg for **all six planets to ≤2%**:

| planet | σ (mas/yr) | my δg | banked FM24 | a₀/2 excl. (canon) |
|---|---|---|---|---|
| Mercury | 0.006 | 4.51e-14 | 4.6e-14 | 1038× |
| Venus | 0.015 | 8.07e-14 | 8.0e-14 | 580× |
| Earth | 0.0019 | 8.70e-15 | 8.7e-15 | 5382× |
| **Mars** | 0.00037 | 1.38e-15 | 1.4e-15 | **33 972×** |
| Jupiter | 0.28 | 5.62e-13 | 5.6e-13 | 83× |
| **Saturn** | 0.0047 | 6.96e-15 | 7.0e-15 | **6726×** |

Exclusion factors match the banked table (Mars ~34k×, Saturn ~6.7k× canon; ×1.2 alt). The a₀/2 landmine
is real and the kill is **not** inflated — the σ→δg conversion is the textbook Gauss result, independently
reproduced.

## 2. The a₀/2 tail's observable GROWS with a (Mars/Saturn dominate) — confirmed
From ⟨ω̇⟩ = A_r√(a(1−e²)/GM) ∝ **√a**, a *constant* sunward a₀/2 produces a precession that rises
monotonically with semimajor axis: Mercury 6.2 → Saturn 31.6 mas/yr, ratio Saturn/Mercury 5.08 ≈
√(a_S/a_M)=4.98. So outer planets dominate the exclusion — consistent with Mars/Saturn being the binding
planets. The ω_c reactive-suppression conversion Re G=(ω_c/ω)² ⟹ ω_c ≤ ω√(2δg/a₀) is the *exact* root of
(a₀/2)(ω_c/ω)²=δg (residual <1e-30); binding planet Saturn, ω_c ≤ 8.24e-11 (canon) — **3–4 dex looser than
the drift edge**, so it does not set the window. Correct.

## 3. The secular-drift UPPER edge re-derived independently — this is what binds
Gate G=1/(1+iω/ω_c). |G|²=Re G machine-verified (KK pair). Re-derived da/dt=2T/n ⟹
d ln r/dt = 2f_t/(ωr) with f_t=(a₀/2)|Im G|; at ω≫ω_c, |Im G|≈ω_c/ω ⟹ **d ln r/dt = a₀ω_c/g_N**. Direct
2f_t/(ωr) vs closed form agree to the asymptotic (ω_c/ω)²~1e-17 at the Moon (once g_N is the *dynamical*
ω²r; a benign 0.96% arises only if one mixes GMⴻ/r² with the rounded lunar ω/a — immaterial to a ×2.5
window). LLR Biskupek & Müller 2021 Ġ/G=(−5.0±9.6)e-15/yr → 2σ ceiling |cen|+2σ = **2.42e-14/yr** ⟹
ω_c ≤ 2.21e-14 (canon)/1.83e-14 (alt). Verified LLR binds tighter than MESSENGER (Genova 2018, <4e-14/yr)
and than the reactive per-planet edge.

## 4. Window intersection — NON-EMPTY on both footings (independent)
Lower (RAR gate ≥0.90 at deepest confirmed MOND orbit, y=0.8, v=25 km/s): ω_c ≥ 3ω_gal = 8.99e-15 (canon)/
1.08e-14 (alt). Intersect: **canon [9.0e-15, 2.2e-14] = τ 1.43–3.53 Myr (×2.46); alt [1.1e-14, 1.8e-14] =
τ 1.73–2.92 Myr (×1.69)** — identical to `window_joint.py`/KERNEL_PLANETS.md §6.

## 5. FORCED vs FREE attack — the "FREE" call is honest (no dressing either way)
The lane calls the corner **FREE**; that is the non-inflating call (dressing a free add-on as "forced"
would be the manufactured save, and it was **not** committed). I confirmed no theory scale lands in the
~Myr (2-Myr-period) window: action-forced memory corner a₀/2c = 1.56e-19 rad/s (τ_mem 203/168 Gyr,
CLOSURE_MAP.md item d) sits **10^4.8 below** and is RAR-dead (Re G(ω_gal)=2.7e-9); dS-bath Matsubara =
H_Λ (horizon, ~1e-18); kernel retardation a₀/c (horizon); the Herglotz measure is single-scale a₀ (branch
point t=1/4 dimensionless). The near-miss √(4πGρ_local)=2.4e-15 is ~3.7× below the window bottom **and** is
environmental (spans 3+ dex, can't separate co-located planet/galaxy). Galactic-dynamical ~Myr–100 Myr
scales (Sun z-oscillation 2.9e-15, epicyclic 1.2e-15) also sit below the window and are not theory
constants. **No forced scale was missed that lands in the window.** FREE stands.

## 6. Manufactured-save AND manufactured-deficit hunt (equal force)
- **Not a manufactured save (gate shape):** the single-pole (n=1) relaxator is the *conservative* choice.
  A sharper gate (n≥2) has |Im G|~(ω_c/ω)ⁿ ⟹ drift edge 4 orders *looser* (2.4e-10 vs 2.2e-14) ⟹ window
  ×10⁴ *wider*. Only a gate *softer* than single-pole (fractional n<1, non-standard) could close it. So
  the tight upper edge — hence the whole "does it fit?" tension — is imposed by the most conservative
  causal gate, and the framework survives it. Survival is **robust to the gate assumption**.
- **Not a manufactured deficit:** bounds are used at face/2σ, not inflated. LLR 2σ (not 1σ), Gauss δg
  reproduced not padded.
- **Honest fragility (disclosed, neither hidden nor exaggerated):** the window is genuinely narrow. It
  stays open under harsher RAR (y=1, v=20 → ×1.57) and at 1σ LLR (×1.48), narrows to ×1.18 under an
  aggressive RAR floor (y=1, v=15 km/s), and **pinches shut at a₀ = 1.47e-10** — both footings
  (9.36e-11, 1.13e-10) sit below that, so survival is not knife-edge in a₀, but the margins are modest.
  Confirmed-MOND rotation below v≈20 km/s (dwarf-spheroidal, dispersion-supported) would move the lower
  edge up and could close it — a real, stated vulnerability, handled with a single representative orbit
  rather than the full SPARC sweep (an acknowledged simplification, not a flaw at order-of-magnitude).

## Bottom line
**UPHELD.** Non-empty window on both footings, every load-bearing number independently reproduced (exit 0),
bounds honest, single-pole gate conservative, corner genuinely FREE. The framework **survives the solar
system conditionally**, as a gated Reading-C crossover whose ~Myr corner is an honest 5th constant
{s, a₀, Z, η} → +ω_c that the published action does not supply (its own corner, a₀/2c ~ 200 Gyr, is
RAR-dead). Not a falsification; not a clean win. Two-sided falsifiable exactly as stated: a confirmed
Chae-type AQUAL-strength wide-binary boost kills the gated survivor; a ×3 INPOP/EPM/LLR secular refit
either detects the a₀-scale drift or closes the window from above. Every number discriminates only among
the framework's own readings, never vs ΛCDM.
