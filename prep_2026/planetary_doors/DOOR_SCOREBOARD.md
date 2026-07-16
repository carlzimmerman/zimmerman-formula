# DOOR SCOREBOARD — the framework's solar-system doors vs the cited bounds

**Date:** 2026-07-16. Numbers from `laneK_kernel_planets.py` (exit 0), `laneR_bounds_compute.py`,
prior committed `cassini_mi_evasion_2026/` + `branchB_q2_gate_2026/`, and re-checked in
`vfy_kernel_planets.py` (exit 0). Both footings: **canon a₀=9.362e-11**, **alt a₀=1.130e-10**.

**HONEST CEILING (applies to every row):** at planetary accelerations (10⁴–10⁸ a₀) GR predicts zero
anomaly and healthy MOND-family theories predict near-zero. Every row below **discriminates BETWEEN the
framework's own doors** — none can prefer the framework over ΛCDM.

The doors / readings of the ONE published action:
- **Door A / MG (AeST-class, own ν):** modified-gravity realization; EFE/nonlinear Poisson.
- **Door C / MI reading A (constitutive):** first-moment closure K(+a²/a₀²) → the galactic ν-recovery.
- **Door C / MI reading B (operator/spectral):** Borel calculus on the orbit's own □_u spectrum.
- **Door C / MI reading C (gated):** SPEC off-circular completion S(a/a₀)·L(ω/ω_c), free corner.
- **Door B / Branch-B elastic:** elastic-medium realization (separate committed lane).

---

## 1. The a₀/2 isotropic constant tail (the landmine) — per planet

Bound: laneR per-planet constant-radial-δg from Fienga & Minazzoli 2024 (Living Rev. Relativ. 27:1,
Table 10) via the Gauss secular equation. Amplitude a₀/2 = 4.68e-11 (canon) / 5.65e-11 (alt) m/s².

| planet | δg bound [m/s²] | **Door A / MI-read-A** excl. (canon / alt) | Door C MI-read-B (operator) | verdict |
|---|---|---|---|---|
| Mercury | 4.6e-14 | 1018× / 1228× | 7.1e-28 (6.5e13× under) | A dead / B invisible |
| Venus | 8.0e-14 | 585× / 706× | 1.3e-27 | A dead / B invisible |
| Earth | 8.7e-15 | 5380× / 6494× | 1.8e-27 | A dead / B invisible |
| **Mars** | 1.4e-15 | **33 436× / 40 357×** | 2.8e-27 | A dead / B invisible |
| Jupiter | 5.6e-13 | 84× / 101× | 9.5e-27 | A dead / B invisible |
| Saturn | 7.0e-15 | 6687× / 8071× | 1.7e-26 | A dead / B invisible |

**Reading A reproduces the tail (V5, <0.1%) and it is NOT GM-absorbable (V2): dead 10³–10⁴×. Reading B
never generates it (kinematic): invisible 10¹⁰–10¹³× under bounds — but RAR-dead + drift-excluded (rows 3,4).**

## 2. The EFE quadrupole Q₂ — the sharpest MOND-family observable

Ceiling: **Park+ 2026 (arXiv:2602.17884) Q₂ = (1.6±1.8)×10⁻²⁷ s⁻², 2σ = 5.2×10⁻²⁷** (full DE440;
supersedes Hees+2014 9.0e-27). RAR-vs-Q₂ discrepancy 3–15σ; MOND boost at Sun ≤2% (95% CL).

| door / reading | Q₂ [s⁻²] canon / alt | vs 5.2e-27 ceiling | source |
|---|---|---|---|
| **Door A / MG (own ν)** | **2.5e-26 / 3.3e-26** | **4.8× / 6.4× (+13σ / +17.5σ)** | `branchB_q2_gate_2026/` |
| crude a₀/2-as-Q₂ (MG-read of the tail) | ~a₀/2r_Sat = 3.3e-23 / 3.9e-23 | ~6300× (~3.8 orders) | BOUNDS.md §2 |
| **Door C / MI (readings A/B/C)** | **7.4e-34 / 1.1e-33** | **1.4e-7× (invisible)** | `cassini_mi_evasion_2026/` (true l=2, 2nd order, deep-Newton ν−1=a₀/2a_int) |
| Door B / Branch-B (own ν ref) | 2.5e-26 / 3.3e-26 | 4.8× / 6.4× | inherits the MG number |
| Door B / Branch-B (scalar sharp-screen) | needle: one thread (canon only, 0.9×) | marginal / fails alt | `branchB_q2_gate_2026/` |
| Door B / Branch-B (vector-elastic β=2/7) | fails ×1.3–2.7 all footings | FAIL (needs β≥0.42–1.19, outside natural [0.18,0.33]) | `vector_elastic_w_2026/` |

**Q₂ is the Door-A wall (+13 to +17.5σ) — MI evades it (invisible); Branch-B passes only on a needle or
via underived posits.** Q₂ does NOT distinguish MI from ΛCDM (both invisible); it distinguishes Door A
(dead) from Door C (safe) *within the framework*.

## 3. The secular drift a₀/c — the previously-uncomputed dissipative channel

Universal d ln r/dt = a₀/c (orbital-mechanics factor ODE-checked to 0.2%). Magnitude sign-blind; sign of
inspiral/outspiral inherits the s=−1 postulate.

| door / reading | drift | vs MESSENGER Ġ/G<4e-14/yr | vs LLR | verdict |
|---|---|---|---|---|
| Door C MI-read-B (operator) | a₀/c = 9.86e-12 / 1.19e-11 /yr | **×246 / ×297** | lunar 47σ / 57σ; LLR Ġ/G ×407/×492 | **excluded ~2.4–2.7 orders** |
| Door C MI-read-A (constitutive) | **0** (DC dressed by real K(a²/a₀²)) | — | — | no drift (but IS the row-1 landmine) |
| Door C MI-read-C (gated, max corner) | ≤ bound by construction | at Saturn/Mars sensitivity | ≤0.02 mm/yr lunar | conditional pass |

## 4. The reactive residual (operator reading) — per planet, both footings

g_N·(a₀/cω)²/8 = 7e-28 (Mercury) … 1.7e-26 (Saturn, canon) m/s² — **10–13 orders under the bounds** of
row 1. This is the kinematically-forced suppression; it is the operator reading's fingerprint and is
invisible on every current instrument.

---

## 5. Door standing entering / leaving this lane

| Door | Inner-SS status | load-bearing number |
|---|---|---|
| **A — MG/AeST (own ν)** | **WALL, inherited** | Q₂ = 2.5–3.3e-26 = 4.8–6.4× ceiling (+13 to +17.5σ); boost 28–33% vs 2% allowed |
| **B — Branch-B elastic** | **needle / posit-dependent** | scalar: one marginal thread (canon only, 0.9×); vector-elastic natural β FAILS Q₂ ×1.3–2.7 |
| **C — MI reading A (constitutive)** | **DEAD at planets** | a₀/2 landmine excluded 10³–10⁴×; not GM-absorbable (V2); no EFE rescue in MI |
| **C — MI reading B (operator)** | **kinematically evades the tail, but RAR-dead + drift-excluded** | reactive 10⁻²⁸–10⁻²⁵ (invisible); drift a₀/c excluded ×246–492; RAR erased (1−ReK≤2e-6) |
| **C — MI reading C (gated)** | **CONDITIONAL pass, two-sided-open** | ω_c ∈ [~1e-14, ~3.5e-14] rad/s (~Myr sliver, width ×1.7–2.5); falsifiable by ephemeris refit ×3 and by wide binaries |

**Net:** the solar system pins the framework's off-circular corner two-sidedly and leaves exactly one
open reading (gated Reading C). It does **not** decide framework-vs-ΛCDM — every number here separates
the framework's own doors.
