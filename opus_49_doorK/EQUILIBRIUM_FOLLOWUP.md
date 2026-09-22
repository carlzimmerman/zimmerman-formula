# OPUS_49 doorK — NSE EQUILIBRIUM FOLLOW-UP (the pre-registered question)

**Pre-registration** (N05_VERDICT.md § 4, item 1): *"T ≥ 160 at N = 32, the
undamped classes: settles whether the truncated classical flow equilibrates —
a purely numerical question, cleanly pre-registered."*

**Answer: NO.** The truncated classical 3D Navier–Stokes flow with the
framework's undamped-force classes (classical, a0cap-0.02) **keeps pumping
enstrophy**: no equilibrium at the literal T = 160 horizon (two-decade slope
α[1.6,160] = 1.257), none through T = 200 (N04c reproduced **bit-exact**,
α_end = 1.135), and none through T = 320 (6.4 viscous times; α_end = 0.864,
still ≥ 0.8). The pump only *decelerates*: sup|u| nearly saturates
(35.25 → 35.84 over T = 200 → 320, +1.7%) and the last-quarter local slope
collapses to 0.04, so an equilibrium is approaching but has not been reached
within any run by the registered settled-threshold (α_end ≤ 0.3).

**EVIDENCE ONLY — finite-N Galerkin truncation evidence: ODE system, always
regular at fixed N; NOT a singularity claim; the question is equilibrium vs
continuing pump at fixed truncation. Simulations are not proofs.**

---

## 1. Method (reused verbatim from N04c; no imports)

3D periodic dealiased (2/3-rule) spectral Galerkin of

    u_t + (u·∇)u = −∇p + ν Δu − c_d |u| u + f     (+ optional a₀-cap |d| ≤ 0.02)

RK4 in Fourier space, divergence projection, forcing A·s with sup|s| = 1 on
low modes (|k| ≤ 4), exact real-space per-volume means for
energy/enstrophy, snapshots every 25 steps. Parameters: n = 32, ν = 2e-2,
dt = 4e-3, A = 1, seed = 7, dealiased cutoff k_max = 10.67.

The **undamped classes** — cd-0.3 was already equilibrated in N04b and is not
part of the registered question:

| case | c_d | a₀-cap | role |
|---|---|---|---|
| classical | 0 | none | the registered question (the truncated classical flow) |
| a0cap_002 | 0 | \|d\| ≤ 0.02 | bounded-force companion, sub-regularizing N2 class (no \|u\|-damping) |

Two phases on the same grid and seed:

* **Phase A — reproduction of N04c**, T = 200 = 4 viscous times at the forcing
  scale (1/(ν k_f²) = 50).
* **Phase B — extension**, T = 320 = 6.4 viscous times, past the registered
  horizon, plus the literal T = 160 readout from the same trajectory.

## 2. Phase A — reproduction of N04c (T = 200): BIT-EXACT

All 12 recorded quantities agree with the committed N04c
results to **0.000% relative** (identical trajectories):

| quantity | N04c | here | rel. diff |
|---|---|---|---|
| classical sup_final | 35.245642 | 35.245642 | 0.000% |
| classical enst_final | 318.945561 | 318.945561 | 0.000% |
| classical alpha_end | 1.135418 | 1.135418 | 0.000% |
| classical CFL | 1.503814 | 1.503814 | 0.000% |
| classical E_final | 156.984705 | 156.984705 | 0.000% |
| a0cap sup_final | 33.608760 | 33.608760 | 0.000% |
| a0cap enst_final | 287.672644 | 287.672644 | 0.000% |
| a0cap alpha_end | 1.134932 | 1.134932 | 0.000% |
| a0cap CFL | 1.433974 | 1.433974 | 0.000% |
| a0cap E_final | 141.476351 | 141.476351 | 0.000% |

**VERDICT A (both classes): keeps pumping enstrophy through T = 200**
(α_end = 1.135, > 0.8), exactly as N04c.

## 3. Phase B — extension to T = 320 (6.4 viscous times)

| quantity | classical | a0cap_002 |
|---|---|---|
| sup_final | 35.840 | 34.171 |
| sup_peak | 35.840 | 34.171 |
| enst_final | 329.53 | 297.18 |
| enst last-quarter mean | 326.75 | 294.90 |
| enst previous-quarter mean | 316.57 | 285.54 |
| G60 quarter drift | 3.2% | 3.2% |
| alpha_end (two decades, t ∈ [3.2, 320]) | **0.864** | **0.864** |
| end-slope (last quarter, t ∈ [240, 320]) | 0.043 | 0.043 |
| CFL max(\|u\|·dt·k_max) | 1.529 | 1.458 |

**Literal pre-registered horizon** (t ∈ [1.6, 160], from the reproducible
trajectory): α = **1.257** both classes — pumping, comfortably above the
0.8 pumping threshold; sup(t=160) = 34.45 (classical) / 32.85 (a0cap),
enst(t=160) = 304.95 / 275.08.

**VERDICT B (both classes): keeps pumping enstrophy through T = 320**
(α_end = 0.864 ≥ 0.8, no equilibrium within the run). The pump is,
however, strongly decelerating: the last-quarter local slope is 0.043 —
below the 0.3 settled threshold — and sup|u| moved only +1.7% over
T = 200 → 320. An equilibrium appears to be *approaching* (est. saturation
in the T ≈ 320–400 band) but was **not reached** within any run by the
registered classification.

## 4. CFL and the countervailing energy-identity check (as N04c did)

The lane's CFL proxy (max |u|·dt·k_max < 0.4, calibrated for |u| ~ O(1))
**FAILs in both phases** — phase A: 1.5038 (classical), 1.4340 (a0cap);
phase B: 1.5292, 1.4580 — the registered excess, caused by the very spin-up
this lane probes (sup|u| ~ 35). The countervailing integrator-health check is
the discrete energy identity, dE/dt = −νZ + ⟨f,u⟩ (+ ⟨u,d⟩ for a0cap),
which closes on every run:

| run | worst local residual | accumulated residual |
|---|---|---|
| A/classical | 0.722% | 0.004% |
| A/a0cap | 0.740% | 0.004% |
| B/classical | 0.912% | 0.000% |
| B/a0cap | 0.935% | 0.000% |

All within the registered ≤ 1–2% band at dt = 4e-3 — the integrator is
healthy and the trajectories are trustworthy for the equilibrium-vs-pump
question.

## 5. Gate table

17/19 checks PASS (the two FAILs are the CFL proxy excesses above):

G60 equilibrium (quarter drift ≤ 15%): **PASS** all runs (A: 11.7% — the
loose band; B: 3.2%). G61 growth law (α_end ≤ 0.3 settled / ≥ 0.8 pumping):
**PASS** all runs → "keeps pumping" everywhere (A: 1.135, B: 0.864).
G61b α[1.6,160] = 1.257 → pumping at the literal pre-registered horizon.
G62 sup ordering (a0cap ≤ 1.05·classical): **PASS** both phases (33.609 ≤
37.008 at T = 200; 34.171 ≤ 37.632 at T = 320) — the capped class does not
cap the sup, consistent with N04/N04b/N04c. G63 energy identity: **PASS**
all runs (≤ 1% local). G64 honesty label: **PASS**.

## 6. Settled question — verdict (explicit numbers)

**Does the truncated classical flow equilibrate by T ≥ 160 at N = 32?**

**NO — it keeps pumping enstrophy, in every undamped class at every horizon**
sampled:

* T = 160 (literal pre-registration): α[1.6,160] = **1.257** — pumping.
* T = 200 (reproduction of N04c: bit-exact, 0.000% rel. diff):
  α_end = **1.135** — pumping; sup ~ 35.2, above the a₀-window.
* T = 320 (extension, 6.4 viscous times): α_end = **0.864** — still ≥ 0.8,
  "keeps pumping" by the registered classifier; last-quarter slope 0.04 —
  decelerating toward equilibrium, not reached within the run.

The two undamped classes behave identically in slope (a0cap differs only in
amplitude, ~90% of classical) — the bounded cap is sub-regularizing, exactly
as N04/N04b/N04c found. Consistency with the campaign structure: the pumping
flow lives at sup |u| ≈ 35, far above the a₀-window — Newtonian-face
dynamics, where the framework's law is certified silent.

Run it again: `python3 equilibrium_followup.py` (full trajectory in
`equilibrium_followup_results.json` + `.png`; ~2.5 h on this machine).