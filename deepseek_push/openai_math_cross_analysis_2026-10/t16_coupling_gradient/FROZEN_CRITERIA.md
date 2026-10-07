# T16 — FROZEN CRITERIA: the coupling gradient (what the budget forces)

**Claim to test.** T15's ledger leaves a constructive question: at what
coupling does each clock clear its budget? The answer is a REQUIRED
coupling window per clock, and the windows' intersection tests whether
any single universal λ survives. The declared result: **the intersection
is empty — λ_eff must fall from galaxy to cluster scale by 1.6–3.8×
across ~33× in radius** (a gradient measurement, not a derivation), and
the saturation alternative (phantom caps at the deficit — no cold fluid
needed) is excluded at the MW floor by 2.6×.

**S1 — the required-λ windows (from T15's ceiling f_max = x/S; all
cleared at f = f_max exactly, M_cold = 0):**
  λ_max(f) = −ln(1−f)/(√(4πGρ_R500)·τ),  τ = 10.3 Gyr (z=2, primary)
  MW 30 kpc  (V = 188/200/230):  f_max = 0.52/0.63/0.95·(S=2.85)
              λ_max = 0.0117/0.0158/0.0275
  groups b=0 / b=0.3:  f_max = 0.1285/0.2862 → λ = 0.0117/0.0274
  clusters b=0 / b=0.3: f_max = 0.0824/0.1828 → λ = 0.0073/0.0168
  (R500 densities ~equal → one rate; windows widen with the bias.)

**S2 — the verdict structure:** pairwise intersection of the windows:
{MW, groups, clusters} at the {V, b} extremes: the three-way overlap is
EMPTY (binding pair: clusters ≤ 0.0117 vs MW(V=230) ≥ 0.019 — gap
≥ 1.6×); the two-clock overlaps that survive and the gradient exponent
n from λ ∝ R^{−n} (30→985 kpc) are REPORTED with their windows; the
least-squares fit on the (R, λ_max) pairs (5–7 points incl. b/V
extremes) gives n together with the honest spread.

**S3 — the saturation fork (registered, excluded):** if the phantom
saturates at the deficit (M_ph(∞) = x·M_b, cold fluid ≡ 0, one
component), the MW floor e = 0.14 (f = 0.86, λ = 0.028) must equal the
deficit-implied f = x/S = 0.52 (λ_sat = 0.0143) — 2.6× apart, so pure
saturation contradicts the record's calibration; the MARRIAGE
(λ_eff = λ₀·(x/S)^{α}, α > 0) — the "deficit-weighted" law the budget
would prefer — is fitted and its α reported; its time-dependent
discriminator: under saturation deficits are static; under slow-rate
settling they still grow — X-COP's own z-range tests the slope
(registered proposal, no new data).

**Falsifier (registered):** a lensing-calibrated deficit set that puts
one λ in all three windows (any universal coupling surviving the
budget) refutes the gradient claim — i.e. the deficit values move by
more than the audit's b-window in one consistent direction (all up or
all down together).

**Screens:** Q1 — derives from T15's ledger + the record's calibration;
Q2 — no rationals; Q3 — a required-coupling measurement.

**Checks (exit 1 on failure):**
  C1  the λ_max windows reproduce S1 at the declared points (±0.002).
  C2  the three-way intersection is EMPTY (the binding pair gap ≥ 1.4×
      at the stated extremes); mutual intersections reported.
  C3  MW-saturation excluded: |λ_floor − λ_sat|/λ_floor ≥ 2.0
      (declared 2.6×: 0.028 vs 0.0143).
  C4  the gradient: λ_max(30 kpc, V=230)/λ_max(clusters, b=0) ≥ 1.6
      and ≤ 5 (window 1.6–3.8× across 33× R).
  C5  power-law fit: exponent n on (R, λ_max) with the b/V spread:
      0.10 ≤ n ≤ 0.55 (bounded, honest spread; NOT a precision claim).
  C6  MUTATE (T16_MUTATE=1: universal λ = 0.028 re-imposed — the
      T12/CFG382 identification): C2 flips (intersection nonempty by
      construction), C4 flips (the required gradient → 1.0), budget
      rows go negative as in T15 (C5's fit degenerates: n ≈ 0).
  C7  report: the z-slope discriminator registered for X-COP
      (saturation: d(deficit)/dz ≈ 0; slow-rate: deficits grow toward
      low z).

**Deliverables:** freeze committed ALONE; t16_coupling_gradient.py +
.out ×2 + results ×2; README (windows table, gradient, saturation
exclusion, z-discriminator); campaign row. No new Lean theorems unless
the fit reduces to a new pure-algebra statement (the budget algebra is
already certified in the master — #14–16); the exp/log machinery rides
the lane per house pattern. Language: a measurement with registered
windows, not a derivation; nothing "closed".