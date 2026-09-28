# AS247 — Same-action Shapiro-delay integral: derivation, engines, and certificate

Run: `AS247-r1-20260928T1945Z-dsv4f-hermes`
Task: `deepseek_push/astra_spawn_ideas/AS247_construct_a_same_action_shapiro_delay_integral.md`
Task SHA-256: `68357b52d30e87c91f7fad43e8c0798c4db573dacf3ca5adf6aa746913562714`
Worker: `deepseek/deepseek-v4-flash-0731` (via OpenRouter), subagent of the AS campaign orchestrator.
Start: 2026-09-28T19:41Z UTC · Finish: see `result.json`.

---

## 1. Pinned sources and conventions

- Action sources (hashes verified against `SOURCE_MANIFEST.json`):
  - `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` ✓
  - `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` ✓
- Framework: `a0 = kappa·c·sqrt(G·rho_Lambda)` with `kappa = 1/2` **adopted as input** (not derived here), `r_M = sqrt(G·M_b/a0)`, `v_flat^4 = G·M_b·a0`.
- Footings carried separately (seed: "they cannot share both fixed vacuum density and fixed kappa"):
  - canonical: `a0 = 9.3619e-11 m/s²` → `rho_Lambda = 5.844412454e-27 kg/m³`;
  - alternative: `a0 = 1.1279e-10 m/s²` → `rho_Lambda = 8.483089620e-27 kg/m³`.
  - Both give `kappa_roundtrip = a0 / (c·sqrt(G·rho_Lambda)) = 0.5` exactly (verified numerically to 50 digits).
- Numerics: `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI).
- Branch: CA5-GNC-R physical-metric branch. Q (algebraic), RAR, historical EXP and MU2 laws are **not** used as the operative law; criterion-B filtered MONO is the operative branch for gate statements. No branch translation is performed; all comparisons to historical branches are explicitly labeled conditional.
- Upstream: `results/AS228` (deep-regime lapse/spatial potentials) is **in flight — no submitted result** (verified: absent from `results/`, tracked in `CAMPAIGN_LEDGER.json`). Therefore the deep-regime part of this task is executed **conditionally** (hypotheses H1/H2 below), and fully labeled as a working-hypothesis prediction, not a derived metric statement.

## 2. Target and derivation of the delay functional

**Target (as displayed in the seed):**

```
Delta t = (1/c^3) integral[-(Phi + Psi)] dl     (weak-field sign and baseline convention)
```

Setup: static source, one null ray with finite endpoints outside the source support; metric potentials derived independently (AS226 conventions adopted: `Phi` = time-time potential with `g_tt = -(1+2u) c^2`, `u = Phi/c^2`; `Psi` = spatial potential with `g_xx = (1-2v)`, `v = Psi/c^2`).

**Step 1 — line element and null travel time.** For the weak-field CA5-GNC-R physical-metric line element

```
ds^2 = -(1 + 2u) c^2 dt^2 + (1 - 2v) dx^2 ,    u = Phi/c^2 ,  v = Psi/c^2 ,
```

a null ray gives `(1+2u) c^2 dt^2 = (1-2v) dx^2`, hence the coordinate speed

```
c dt/dl = sqrt( (1 - 2v) / (1 + 2u) ) ,
```

where `dl = |dx|` is the Euclidean coordinate arc length. The exact coordinate travel time along a ray of coordinate length `L` is

```
T = (1/c) * integral sqrt( (1 - 2v)/(1 + 2u) ) dl .
```

**Step 2 — linearization with exact remainder.** With `s = u + v`, the squared speed satisfies the exact identity (certified)

```
linear_remainder (u v) :
    (1 - (u+v))^2 * (1 + 2u) - (1 - 2v)
      = (u+v)^2 + 2u (u+v)^2 - 4u (u+v) ,
```

i.e. `(1 - s)^2 (1 + 2u) = (1 - 2v) + O(s^2, us^2, us)`. The certificate proves the two-sided bound `|(1-s)^2 (1+2u) - (1-2v)| <= 151/125000` for `|u|, |v| <= 1/100` (`linear_remainder_bound`), i.e. the linearization error of the squared travel-time integrand is `O(u^2)` with the explicit constant `151/125000`. At first order:

```
T = (1/c) integral (1 - u - v) dl + O(u^2)
  = L/c - (1/c) integral (u + v) dl + O(u^2).
```

**Step 3 — additive normalization at the endpoints.** With the baseline convention  `T_flat = L/c` (no potentials along the same chord), the delay correction is

```
Delta t = - (1/c) integral_{chord} (u + v) dl = (1/c^3) integral_{chord} [-(Phi + Psi)] dl .   (target)
```

Constant shifts of the potentials change `integral (u+v)` by a term proportional to the chord length (`endpoint_shift` in the certificate: constant shifts `c, c'` contribute exactly `(c + c')(b - a)` to the integral); the *difference* of delays between two rays is invariant under simultaneous constant shifts, which is the gauge-safe observable (used in Engine C). Attractive potentials (`u, v < 0`) make the correction positive — a genuine delay (`delay_sign`, `point_mass_delay` in the certificate); slip is necessary: with `v = u` (no slip) `Delta t = -(2/c^3) integral Phi dl` (`B2` verifies `noslip ≡ full`), and a slip `Psi - Phi = delta` changes the delay by exactly `-(1/c) integral delta dl` (`slip_shift`, `slip_changes_delay`; `B3`, `B4d`, `B4e`).

**Step 4 — closed forms (Newtonian and deep log) certified.** For `Phi = Psi = -GM/r` (point mass, no slip) the certificate proves

```
∫_{-X}^{X} 2m/sqrt(x^2+b^2) dx = 2m log( (X + sqrt(X^2+b^2)) / (sqrt(X^2+b^2) - X) )        (newton_delay_closed)
0 < ∫_{-X}^{X} 2m/sqrt(x^2+b^2) dx                                                          (point_mass_delay)
```

and for the deep log potential `Phi_D = C ln(r/(e r_M))` (used only conditionally):

```
∫_{-X}^{X} log(sqrt(x^2+b^2)) dx
  = 2X log(sqrt(X^2+b^2)) + 2b arctan(X/b) - 2X                                              (deep_log_integral)
```

via certified antiderivatives (`newton_antideriv`, `deep_log_antideriv`).

## 3. Engine B — functional certification at toy scale (c = 1)

`as247_functional.py`, c = 1, u ≡ Phi, v ≡ Psi: Gaussian `Phi = -u0 exp(-r²/(2σ²))` with `u0 = 1e-3`, `σ = 2.0`, half-chord `L = 20`, impact `b = 1.0`, slip `δ = ε Phi`, `ε = 0.25`. Checks (all pass; values from `func_raw.json`):

| check | result | tolerance |
|---|---|---|
| B1 linearization residual (exact vs linear integrand) | rel 6.249e-4 | ≤ 5e-3 (O(u0)) |
| B1b pointwise remainder | max 1.558e-6 | ≤ 2e-2 (certified ≤ 1.3e-3) |
| B2 no-slip: `-∫(u+v)dl` ≡ `-2∫u dl` | rel 0.0 | 1e-14 |
| B3 slip changes delay: Φ-only formula fails | rel 0.111 (fires) | > 0.05 |
| B4a Fermat-path RK4 geodesic hits endpoint | miss 1.75e-10 | 5e-8 |
| B4b refinement h/2 | miss 1.66e-10; T stable | 5e-9 ; 1e-4 |
| B4c geodesic matches functional | diff −2.25e-5 (bending order) | ≤ 1e-2·|dt| |
| B4e geodesic slip gap vs linearized slip integral | diff 2.25e-5 | ≤ 5% rel |

Numerics: `dt_slip = 9.9544125973e-3`, `dt_noslip = 8.8483667532e-3`; geodesic `T - 2L = 9.93186519e-3`. The geodesic (RK4, h=0.01 → 0.005, bisection on launch slope, root = 1.264638e-3) confirms the functional at bending order: the residual of the linearized functional is the O(u0²) bending term, in both the total and the slip-part.

## 4. Engine A — one ray through the box/torus same-action metric (SI)

`as247_box.py` — shared AS226 parameter cell: `alpha = 0.3` → `c_N = 0.85`, `ell = 0.04` (heat-filter length), `ξ²/2 = 0.045` (`ξ = 0.3`), box `L = 100 m`, `N = 48 → 96`, `M_b = 5 kg`, `σ = 2.5 m`, `G_N = 6.67430e-11`, `c = 299792458`, gate threshold `θ = 1e-4 m⁻²`, mean-subtracted torus source. Metrics used: `G_bare = c_N G_N` (canonical) and the alternative `rho_Lambda` footing; `G_N/G_bare/G_cosmo` kept separate throughout.

Mode-picture solution of the filtered operator:  `Phi_hat = -rho_hat / (2 MP2 c_N k² Q(k))`,  `Q(k) = 1 - (ell/4) exp(-ξ²k²/2)`,  `Z_hat = (ell/4) exp(-ξ²k²/2) Phi_hat` (heat-filter stress tied to `Phi`), so `Phi = Z + U` with `Delta U = -rho`-type sourced equation. Verified residual: `max|E1|/scale = 3.37e-16` (N48), `1.80e-16` (N96); the gate is inactive (`max Y_h = -1.000e-4 < 0`; margin `|max J + ell ΔW|/θ = 6.67e-9`).

Ray: chord `x ∈ [-L/4, L/4]` at impact `b = 8.0, 20.0 m`, 2001 → 4001 points, evaluated by the **exact two-stage spectral chord evaluation** in FFT-native coordinates (verified against full IFFT rows on-grid to `7.3e-16` relative — `A3c`).

| observable | N=48 | N=96 | rel. change (A5) |
|---|---|---|---|
| `dt(b=8 m)` | 5.8198858e-35 s | 5.8199094e-35 s | 4.05e-6 |
| `dt(b=20 m)` | 1.8563537e-35 s | 1.8563899e-35 s | 1.95e-5 |
| filter contribution `(dt - dt0)/dt` | 9.9997e-3 (≈ 1%) | 9.9997e-3 | — |
| filter-off `dt0(b=8)` | 5.761688e-35 s | 5.761712e-35 s | — |

Sign control: both delays positive (attractive potentials → delay) ✓. The heat filter contributes ~1.00% of the delay at both impacts — the low-k boost `1/Q ≈ 1.0101` — matching the analytic expectation to 4 significant digits.

## 5. Engine C — deep-galactic conditional evaluation (50-digit)

`as247_deep.py` — **CONDITIONAL**: uses the AS044 labeled scalar-substitute deep non-relativistic potential `Phi_D(r) = C ln(r/(e r_M))`, with `C = sqrt(G M_b a0)`, `r_M = sqrt(G M_b a0)/a0`-scale — under two **unproved** hypotheses:

- **H1**: no-slip continues in the deep regime (`v = u`);
- **H2**: the AS044 non-relativistic scalar potential is the metric time-time potential `Phi = Phi_D`.

Chord `x ∈ [0, 5 Mpc]`-scaled, impact parameters `b1 = 1.5 Mpc, b2 = 3.0 Mpc`, deep band `r >= 100 r_M` (`y = B/a0 <= 1e-4`: `b1/a0-domain = 1.5e-4` ✓, clamped 1e-4 per band check); `r_M = 12.20 kpc (canonical), 11.12 kpc (alt)`; `e r_M = 33.2 kpc` — the whole chord sits in `Phi_D > 0`.

Result (50-digit mpmath quadrature + certified closed forms):

| footing | `Δτ(b1) - Δτ(b2)` (differential) | Newtonian reference (same chord, `-GM_b/r`) |
|---|---|---|
| canonical 9.3619e-11 | **+2.9392e8 s** (advance; deeper ray less delayed) | 1.2828e6 s (delay) |
| alternative 1.1279e-10 | **+3.2261e8 s** | 1.2828e6 s |

Sign: `Phi_D > 0` → the correction term `-(1/c)∫(u+v)dl` is negative — an *advance* — qualitatively opposite to the Newtonian delay; the log potential dominates the Newtonian term on these chords (`|Δτ|/|Δτ_Newt| ~ 230`). Absolute delays are gauge-dependent (log potentials); only the **differential** between impact parameters is gauge-safe. This is a **working-hypothesis prediction**, not a derived metric statement, until AS228 supplies the deep lapse/spatial potentials.

## 6. Negative control (must be capable of failing — it fires)

Seed control: "Use only Phi while claiming no-slip has been derived and require a synthetic slip control to change the answer."

- **B3/B3b**: with slip `ε = 0.25`, the Φ-only (no-slip-assumed) formula misses the change by rel **0.111** — the control **fires** (residual 1.1060e-3 vs the slip-required threshold 5%).
- **B4d**: the slip is visible on the actual geodesic (gap 1.0835e-3 > 5% of the slip effect).
- **B4e**: the geodesic gap equals the linearized slip integral `-(1/c)∫δΨ dl` to bending order.
- **A4**: the same-action filter contribution is ~1.00%; using the unfiltered potential `dt0` alone would silently misstate the delay by 1% (residual 1.0e-2 recorded).

All controls are framed so a wrong sign, a wrong normalization, or a dropped slip term changes the pass condition.

## 7. Lean 4 certificate

`AS247_cert.lean` — 11 certified theorems + 3 helper lemmas (14 statements total), zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound} (verified: `#print axioms` on all 14 statements, `lake env lean` EXIT 0):

1. `linear_remainder` — exact algebraic remainder of the linearization;
2. `linear_remainder_bound` — `|R_2| ≤ 151/125000` for `|u|,|v| ≤ 1/100` (two-sided, explicit constant);
3. `delay_sign` — attractive potentials give a positive (delay) correction;
4. `endpoint_shift` — constant potential shifts contribute `(c+c')(b-a)` to the integral; differences are invariant;
5. `slip_shift` — linear response: slip `δ` changes the functional by `∫δ dl`;
6. `slip_changes_delay` — non-zero slip changes the delay;
7. `newton_antideriv` — `d/dt log(t + √(t²+b²)) = 1/√(t²+b²)` (via certified `sqrt_gt_abs`, `sqrt_gt_x`, `sum_pos` helpers using the two-sided-square argument, never `linarith` on expressions inside `√`);
8. `newton_delay_closed` — point-mass chord closed form;
9. `point_mass_delay` — the closed form is strictly positive;
10. `deep_log_antideriv` — `d/dt [t log√(t²+b²) + b arctan(t/b) − t] = log√(t²+b²)`;
11. `deep_log_integral` — symmetric closed form of the deep-log delay.

Build: `cd fable_independent_2026/lean_2026 && lake env lean <run dir>/AS247_cert.lean` — EXIT 0; `#print axioms` confirms no `sorryAx` on any statement.

## 8. Execution bounds (actually enforced)

- Wall/CPU: `ulimit -t 120` enforced per process (CPU seconds); measured wall: B 38.4 s, A 0.63 s, C 0.09 s.
- Memory: declared ≤ 512 MB, measured max RSS: B 48.2 MB, A 433.2 MB (N96 FFT arrays), C 19.7 MB. Memory was **measured, not hard-limited** (no RLIMIT_AS); the 512 MB bound was not exceeded.
- Threads: 1 (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1`; host reports nproc=1).
- Samples/refinement: B RK4 h=0.01 → 0.005; A N=48 → 96 with chord 2001 → 4001; C 50-digit mpmath, mp.dps=50.

## 9. Classification and closure implication

**Outcome: `supports_scoped_claim`** — a properly normalized one-ray delay functional for the CA5-GNC-R candidate metric:

```
Δt(chord) = (1/c^3) ∫_{chord} [-(Phi + Psi)] dl  +  O(|u+v|^2)      (certified bound O(u^2), explicit constant)
```

with the exact geodesic validation at toy scale (Engine B), the mode-exact same-action box evaluation including the heat-filter contribution (Engine A), and the gauge-safe differential evaluation in the deep band (Engine C, conditional on H1 ∧ H2 and on AS228's future potentials).

- **Gate**: criterion-B operative gate (filtered MONO); the gate is inactive for this box source (A2: `max Y_h = -1e-4 < 0`) — the delay functional is therefore derived in the gate-inactive regime; deep-regime statements remain conditional.
- **Not closure of gravity**: the delay functional is one observable; it does not promote the framework to complete gravity closure.
- **Deep regime**: blocked-on-dependency for a *derived* deep delay — AS228 in flight (missing: lapsed/spatial metric potentials in the deep band, and a derived slip in that regime).

## 10. Files

- `AS247_cert.lean` — Lean 4 certificate (12 statements, zero sorry).
- `lean_out.txt` — compiler log, `EXIT 0`, axioms clean.
- `as247_functional.py`, `func_run.out`, `func_raw.json`, `func_time_mem.txt` — Engine B.
- `as247_box.py`, `box_run.out`, `box_raw.json`, `box_time_mem.txt` — Engine A.
- `as247_deep.py`, `deep_run.out`, `deep_raw.json`, `deep_time_mem.txt` — Engine C (conditional).
- `derivation.md`, `result.json` — this report and the contract result.
