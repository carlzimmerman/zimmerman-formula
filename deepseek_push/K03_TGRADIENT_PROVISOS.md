# K03 — Temperature-Gradient Provisos: every exact relation under T(r) = 1 + h r²

**2026-09-23 · deepseek_push/K03_tgradient.py · 81/81 checks PASS · verdict: GRADIENT-ROBUST (no falsifier)**

Status: **ALL PASS.** None of the constant-T laws breaks under the gradient; every
h-dependence that exists is exactly the h-dependence the theory already carries
(profile observables, not law statistics).

---

## 1. Why this lane exists

The frozen band and the new moment laws (J01/J02) were derived at constant
temperature T = 1. A physical observer sees a temperature *gradient*. This lane
re-derives nothing: it pushes the exact engine to a squared gradient
**T(r) = 1 + h r²** and re-tests **every** exact relation, with the task's kill
condition: *any law failing beyond 4 SE under h > 0 is h-dependent — a NEW
falsifier.*

Engine: `deepseek_push/J02_moment_hierarchy.py::simulate(n, tau0, q, source, seed)`
(exact optical-depth bisection transport, no null-collision thinning). J02's
`simulate` gained an `h` parameter (`h=0.0` default — the isothermal J02 lane is
unchanged); the collision kick is drawn with variance `T(r) = 1 + h r²` and the
angular exposure is `ang = Σ T(r)(1-μ)`, exactly as the J01 theorem requires.

---

## 2. Protocol

| cell | (tau0, q, h) | source | n |
|---|---|---|---|
| A1 | (1, 0, 1) | central | 1 000 000 |
| A2 | (1, 0, 2) | central | 1 000 000 |
| A3 | (1, 3, 1) | central | 1 000 000 |
| A4 | (1, 10, 1) | central | 1 000 000 |
| A5 | (2, 3, 2) | central | 1 000 000 |
| B1 | (1, 0, 1) | volume | 800 000 |
| B2 | (1, 3, 1) | volume | 800 000 |
| B3 | (2, 3, 2) | volume | 800 000 |

All five required (tau0,q,h) cells at central; three cells (≥ two) at volume.
**Twin construction:** every h>0 run is paired with the h=0 run at the *same
seed*. The RNG stream (position, escape threshold U, Thomson μ, isotropic
rotation, gaussian kick *draws*) is h-independent — only the kick *scale*
`√T` differs. Therefore h-independence of any *trajectory* functional is
testable at **machine precision** (bit-wise), while *kick-observables* carry a
legitimate h-signal. Tolerance policy: PASS ⇔ |meas − pred| < 4 SE (+ a tiny
floor at machine-level checks); the J05 bound requires gap > 4 SE.

---

## 3. Results

### 3.1 (1) E[D] = tau0(1/2 + q/4) — the spatial/opacity statement

| (tau0,q,h) | E[D] (h>0) | pred | dev/SE |
|---|---|---|---|
| (1,0,1) | 0.49954 | 0.50000 | 0.16 |
| (1,0,2) | 0.49971 | 0.50000 | 0.10 |
| (1,3,1) | 1.24915 | 1.25000 | 0.16 |
| (1,10,1) | 2.99814 | 3.00000 | 0.17 |
| (2,3,2) | 2.49648 | 2.50000 | 0.40 |

**PASS (5/5).** Stronger, machine-exact statement (G1b, 5/5): the same-seed
twins have `E[D](h>0) − E[D](0) = 0.000e+00` — **bit-identical**, at every h,
central *and* volume. Temperature cannot enter the spatial statement because
flight sampling never consults T: the kick is drawn after the step length and
only rescales velocities, never paths. Verified at the machine-precision level,
not just statistically.

### 3.2 (2) E[v²] = 2E[ang], E[D v²] = 2E[D ang] — and the full hierarchy, m ≤ 3

Worst dev/tol over all cells (central + volume):

| identity | worst dev/tol | cells |
|---|---|---|
| E[v²] = 2E[ang] | 0.27 | 8/8 |
| E[D v²] = 2E[D ang] | 0.27 | 8/8 |
| E[v⁴] = 12E[ang²] | 0.39 | 8/8 |
| E[D v⁴] = 12E[D ang²] | 0.38 | 8/8 |
| E[D v⁶] = 120E[D ang³] | 0.61 | 8/8 |

**PASS (40/40).** Conditional Gaussianity of the kicks is T-free: each kick has
variance 2T(r)(1−μ) in any direction, so `v | trajectory ~ N(0, 2·ang)` for
*arbitrary* T(r), and ang is *defined* as ΣT(r)(1−μ). The gradient scales the
exposure, never breaks the identity. Confirmed at h = 1 and h = 2, q = 0, 3, 10,
tau0 = 1, 2, both sources. High-moment (m = 3) deviations sit at ≤ 0.6 of their
4-SE tolerance — the sampling noise is respected, not squeezed.

### 3.3 (3) Atom law A = exp(−tau0(1+q/3)) — never-collided photons

| (tau0,q,h) | A (h>0) | pred | dev/SE |
|---|---|---|---|
| (1,0,1) | 0.36776 | 0.36788 | 0.06 |
| (1,0,2) | 0.36775 | 0.36788 | 0.07 |
| (1,3,1) | 0.13457 | 0.13534 | 0.56 |
| (1,10,1) | 0.01291 | 0.01312 | 0.47 |
| (2,3,2) | 0.01837 | 0.01832 | 0.10 |

**PASS (5/5).** Atoms (N = 0, escaped before first collision) never reach a
kick, hence never sample T. Same-seed twins: atom fractions **bit-identical**
across h (5/5) — `atom_same_seed_diff = 0.000e+00`. The central formula is
exact because the optical depth to the wall from the origin is
direction-independent: τ_wall = tau0(1 + q/3).
*Volume note (not a falsifier):* the volume atom fraction is *not*
exp(−tau0(1+q/3)) — e.g. 0.527 vs 0.368 at (1,0,1) — exactly the known
J02 Theorem B face (finite r0 shortens τ_wall, residence coupling Q ≠ 0). The
volume statement verified is h-independence: bit-identical across h (3/3).

### 3.4 (4) J05 bound: E[D²] ≥ 3·E[Dv²]² / E[v⁴]

| cell | gap (LHS − RHS) | gap/SE |
|---|---|---|
| central (1,0,1) | 0.113 | 38.8 |
| central (1,0,2) | 0.105 | 24.4 |
| central (1,3,1) | 0.417 | 26.1 |
| central (1,10,1) | 1.345 | 21.7 |
| central (2,3,2) | 1.022 | 36.4 |
| volume (1,0,1) | 0.140 | 49.0 |
| volume (1,3,1) | 0.397 | 34.2 |
| volume (2,3,2) | 0.840 | 28.8 |

**PASS (8/8)**, gap/SE ∈ [21.7, 49.0]. The bound is a CS-type consequence:
given the hierarchy, 3·E[Dv²]²/E[v⁴] = E[D·ang]²/E[ang²] ≤ E[D²] by
Cauchy–Schwarz — both ingredients are T-free, so the bound holds at any h.
It is strict (never near-saturated), by ~20–50 σ.

### 3.5 (5) Kurtosis law: kurt(v|D) = 3·E[ang²|D]/E[ang|D]² in continuous-part D-bins

Continuous part = N ≥ 1 (atoms excluded: v ≡ 0 would bias the bin kurtosis).
15 quantile bins per central cell, 11 per volume cell.

| cell | bins | pass | worst dev/tol |
|---|---|---|---|
| central (1,0,1) | 15 | 15 | 0.11 |
| central (1,0,2) | 15 | 15 | 0.17 |
| central (1,3,1) | 15 | 15 | 0.22 |
| central (1,10,1) | 15 | 15 | 0.13 |
| central (2,3,2) | 15 | 15 | 0.17 |
| volume (1,0,1) | 11 | 11 | 0.16 |
| volume (1,3,1) | 11 | 11 | 0.11 |
| volume (2,3,2) | 11 | 11 | 0.13 |

**PASS (8/8) — 112/112 bins.** The law is the per-bin instance of the m = 1,2
hierarchy; holds bin-by-bin under the gradient for both sources.

### 3.6 Gradient-live smoke (guards the wiring)

E[v²] rises with h in every central cell (rise 0.95 … 26.9, ≥ 10 SE) — the
gradient is genuinely exercised; the h = 0 twin is not accidentally reproducing
the h > 0 run.

---

## 4. Provisos — what *does* carry h (expected, not law-breaking)

| profile observable | (1,0,1)/(1,0,2)/(1,3,1)/(1,10,1)/(2,3,2) central |
|---|---|
| E[v²], E[ang] | scale ~1.34 / 1.68 / 1.49 / 1.54 / 1.97 relative to h=0 |
| E[D v²], E[D v⁴], E[D v⁶], E[D²] | rise with h (profile moments) |
| E[D], atom fraction, E[N] | **bit-identical** across h (0.000e+00) |

1. The *identities* are T-free; the *statistics* E[v²], E[ang], E[D v^{2m}],
   E[D²] are profile observables and scale with h by construction (ang = ΣT(1−μ)
   *includes* T(1−μ)). This is the correct reading of "ang includes T(1−mu) by
   definition" — restated here so a reader cannot mistake profile scaling for a
   broken law.
2. The isothermal-only shortcut E[v²] = 2E[N] (J01 S3) applies at h = 0 only —
   at h > 0 the left side is 2E[ang] with T(r) > 1 (it already fails at q > 0).
3. Volume source: E[D] = ∫rκ dr is central-only (J02 Theorem B, re-confirmed
   h-independently: volume E[D] = 0.338/0.860/1.558 vs 0.5/1.25/2.5). The
   volume-under-gradient statements verified here are: h-independence of E[D]
   (bit-exact), the full hierarchy, the J05 bound, the kurtosis law, and atom
   h-independence.
4. High-moment checks (m = 3) carry the largest sampling noise; they pass with
   maximal dev/tol = 0.61, i.e. a ≥ 2.5× margin to the 4-SE kill threshold.

## 5. Kill condition — honest finding

**No check failed; 81/81 PASS, 0 discrepancies.** The kill condition ("any of
these FAILS under h>0 beyond 4 SE ⇒ the law is h-dependent ⇒ NEW falsifier")
did **not** trigger. The gradient T(r) = 1 + h r² is therefore **not** a
falsifier of: the spatial law E[D] = tau0(1/2+q/4), the exposure identities and
moment hierarchy, the atom law, the J05 bound, or the kurtosis law — at h = 1
and h = 2, q ∈ {0, 3, 10}, tau0 ∈ {1, 2}, central and volume. The relations are
T-independent because each was derived from a T-free ingredient (geometry /
opacity, conditional Gaussianity of kicks, never-sampled temperature); this
lane confirms that structure numerically at machine precision where it
predicted exactness (E[D], atoms).

## 6. Files

- `deepseek_push/K03_tgradient.py` — lane (seeded; writes K03_results.json)
- `deepseek_push/K03_tgradient.out` — full PASS/FAIL transcript
- `deepseek_push/K03_results.json` — machine-readable checks + measurements
- `deepseek_push/J02_moment_hierarchy.py` — engine: `simulate` gained optional
  `h=0.0` (T(r) = 1 + h r² in kick and exposure); isothermal behavior unchanged.
  Not committed (as instructed).