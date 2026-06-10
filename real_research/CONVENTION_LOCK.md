# Convention lock — the single source of truth for the footing (and the honest status of the evolution)

*C. Zimmerman, 2026-06-09. Fable's "step 0": the corpus flip-flopped between footings ~5× over its
history; this file locks the convention so no future doc re-litigates it. Load-bearing CURRENT docs
(the paper, `FIRST_PRINCIPLES_FOUNDATION`, the README, the synthesis ledgers) must conform to this.
Historical dated docs are research-log snapshots — provenance is preserved, they are NOT retro-edited.*

## 1. The footing is LOCKED (this is not in dispute)
$$a_0 = c^2\sqrt{\Lambda/32\pi} = \tfrac{c}{2}\sqrt{G\rho_{\rm DE}} = \frac{cH_\Lambda}{Z},\quad Z=\sqrt{32\pi/3}=5.789,\quad a_0 = 9.36\times10^{-11}\ {\rm m\,s^{-2}}$$

- Footed on **ρ_DE (dark energy ALONE)** — the pure-Λ density Ω_Λρ_crit. **NOT** ρ_total (which gives 1.13×10⁻¹⁰), **NOT** the regular-MOND value 1.2×10⁻¹⁰.
- Built on **cH_Λ** (the pure-Λ / asymptotic-de-Sitter rate), **NOT** cH₀ (the total present-day rate).
- Stellar M/L **Υ ≈ 0.70** (the framework's own RAR-optimal value, not the MOND-default 0.50).
- This is the value at which the RAR/BTFR/MDAR coincide to 8% and the rising-cH rival is excluded at Δχ²≈49. **The footing — the SCALE — is the most-anchored piece of the framework** (GEMS anchors it rigorously at the pure-Λ fixed point; `GEOMETRIC_FRAMEWORKS_FIVE_TESTS_2026-06-09.md`).

## 2. The EVOLUTION is where the honesty lives — three readings, NOT one
The five-geometry program + the adiabaticity calc (`reviews/adiabaticity_of_a0z.py`) force a more honest tally than "declining, full stop." **The evolution of a₀ — the specifically-Zimmerman, "decisive" C3 claim — is the LEAST-anchored component of the framework.** The three readings:

| Reading | a₀(z) | Status | Where it is licensed |
|---|---|---|---|
| **Constant** | 9.36×10⁻¹¹ at all z | What the **strict KMS/thermal argument actually licenses** — the asymptotic-dS fixed-point value | The unique KMS-thermal horizon is the dS attractor; keying a₀ to its *fixed-point* value is the strictly-valid move |
| **Declining** ★framework | a₀(0)·√(ρ_DE(z)/ρ_DE0), DESI w₀wₐ | The framework's distinctive **ansatz** (the "instantaneous-horizon" choice). **Self-consistent only at z≲1.3** — at z=3 the adiabaticity parameter ε≈4–28≫1, so it is a **non-adiabatic extrapolation** | An *adiabatic extension* of the thermal argument into the matter era — validity quantified only now, and it fails by z≈2 |
| **Rising** ✗rival | a₀(0)·E(z) ∝ cH_total | The **RIVAL** (the June-3 scaling-MOND reading). **Excluded** at Δχ²≈49; CMB-falsified as modified inertia; the ρ_total/ρ_DE (1/Ω_Λ) conflation | One home (AeST: θ=∇·A=3H) natively expresses it — but the GEMS "derives rising" claim was **refuted** (category error + non-KMS FRW horizon) |

**The locked position:** the framework's reading is **declining-√ρ_DE as an ansatz**, with the **strict-thermal fallback being constant**, and **rising as the excluded rival** (never the framework's own law). The decline is a *soft* prior, not a derivation:
- the strict thermal argument gives **constant**;
- **no geometry derives declining** (`GEOMETRIC_FRAMEWORKS_FIVE_TESTS_2026-06-09.md`);
- the empirical lean toward declining — the clean-data fit a₀∝(1+z)^(−0.74±0.34) — **inherits a dataset choice** (it demotes MUSE-DARK III, the opposite judgment from the June-3 paper). State it as a lean, not a result.

## 2b. The CMB does NOT discriminate declining from constant (locked 2026-06-09 — the bath result)
**Any synthesis that claims "the CMB selects declining" or "constant a₀ is CMB-excluded" is a convention violation — that claim is RETRACTED.** It came from feeding the *per-mode* acoustic acceleration (~10⁻⁹ m/s²) into the nonlinear modified-inertia μ-kernel (the `cmb_class_mond` per-mode CLASS run, Δχ²≈117). Modified inertia is nonlinear *and nonlocal*: the μ-argument is the fluid element's **total real-space (bath) acceleration**, a_rms≈2×10⁻⁸ m/s² at recombination (≈21× a single acoustic mode; `reviews/cmb_bath_acceleration.py`). That puts the acoustic modes **deep-Newtonian** (x_flat = a_rms/a₀ ≈ 220) → **flat/constant a₀ is CMB-safe (Δχ²≈0), exactly like declining.** The CMB's *only* robust verdict is that **rising dies** (a₀(z_rec)=1.9×10⁻⁶ ≫ a_rms — prescription-independent, since E(1100)≈2×10⁴). **So: rising excluded; declining and constant both CMB-safe and CMB-indistinguishable.** The standing TODO is the full **bath-kernel CLASS rerun** (a_rms(z) into the kernel, not the per-mode gbar). This is the exact failure mode this lock exists to stop: a result drifting toward the framework's distinctive declining claim regaining support it does not have.

## 2c. The Γ_th blind run + the state-existence result (locked 2026-06-09 — `reviews/gamma_th_blind/`)
A blind 3-method Unruh–DeWitt run **converged** with an independent first pass on **Γ_th(gapless) = λ²H/(2π²)** and **τ_c = 1/H** (both exact). The a₀(z=3) prediction is therefore: **0.737 is the ZERO-LAG value, NOT "maximal decline";** with the Step-4-selected response gate and an adiabatic IC the value is **~0.65**, and the full band over (gate, IC) is **[~0.37, 1.0]**, gate- and IC-dependent — **the IC is exactly the constant-vs-declining fork.** The whole apparatus is conditional on the Step-4 coupling (not derived) and on the gate selection (an *argument* from z=0 phenomenology, not a derivation). **State-existence (locked): no standard calculation yields T ∝ √ρ_DE in the matter-dominated z=3 universe** — a comoving UDW detector's standard-state response is computed *negative/non-thermal* off de Sitter (deceleration-driven; `reviews/gamma_th_blind/`), convergently confirmed by the blind run's Part E. **The demotion is symmetric across footings** (constant's strict-thermal reading also describes only the attractor), and the **Deser–Levin a-dependence (the deep-MOND shape) is untouched.** ⇒ the evolution is a *posited effective law whose standard-state derivation is computed-excluded*, decided empirically at z≈3.

## 3. What this means for the decisive test
A clean a₀(z≈3) measurement discriminates: **rising (≈4.6) is excluded regardless; constant = 1.0; the declining law predicts ~0.65–0.74** (response gate ~0.65, zero-lag 0.737; band [~0.37, 1.0] gate/IC-dependent — §2c). Any value <1 favours some decline. The prediction must always carry its conditionality string — *"given the Step-4 coupling and the response-gate selection"* — and 0.737 must be labelled the **zero-lag** value, never "maximal decline." **No theory choice substitutes for the a₀(z≈3) measurement** — and note the CMB does not discriminate declining from constant (§2b), so z≈3 is the *only* arbiter.

## 4. Enforcement
- The paper §2/§11 and `FIRST_PRINCIPLES_FOUNDATION` Step 2 must read the §2 tally above (footing locked; evolution = declining-ansatz/constant-fallback/rising-excluded; decline is a soft prior).
- Any new doc asserting a₀ ∝ E(z) / cH₀ / ρ_total as the framework's *own* law is a convention violation — that is the **rival**, cited only to be excluded.
- The remaining convention sweep across the ~40 historical docs is a *labelling* pass (mark snapshots as snapshots), not a rewrite — tracked as a follow-up, not a blocker.
