# M04 — J10-I(z): THE BLR ATOM+LAG PAIR AS A COSMOGRAPHY PROBE

**2026-09-23 · moment channel → framework core · port of J10 (6/6) to redshift via G237's z-law · exit 0, 14/14 · synthetic data only, no git commit**

**Status: PORT VERIFIED — the closed-form chain passes its own pre-registered 5-SE self-kill**
bound at 2.2×10⁻¹⁶ (bound 5×10⁻⁶). Every formula below is verified numerically in
`M04_j10z.py` (C1–C13). L05 (JWST observation-design lane) is **IN FLIGHT, not landed** →
the per-object S/N is **assumed S/N = 30 in the atom** (task's fallback, stated plainly;
a landed L05 number would only rescale σ).

## 1. The chain (one new substitution: the a₀-radius acquires z)

| step | statement | status |
|---|---|---|
| (1) | J10-I = −ln A · r_B / (c·d̄_phys) = (r_B/R)·W(q), central W(q) = (1+q/3)/(½+q/4) ∈ **[4/3, 2]** (τ₀-free; volume W_v grid [0.5003, 1.9144] per K09) | J10 6/6, J09 27/27, K09 19/19 |
| (2) | G237 L2: u(z)/u(0) = [a₀(0)/a₀(z)]^{1/2} (derived, sympy) — here the density-local BLR radius inherits the SAME z-factor: r_B(z) = r_B(0)·[a₀(0)/a₀(z)]^{1/2} | G237 5/5 |
| (3) | **inversion of G237's law (this port):** u(z) = u(0)[a₀(0)/a₀(z)]^{1/2} ⇒ a₀(0)/a₀(z) = [u(z)/u(0)]² ⇒ **a₀(z) = a₀(0)·[u(0)/u(z)]²** | C1: max rel err **3.3×10⁻¹⁶** over framework/M-RISE/(1+z)^{3/2} × 6 z |
| (4) | **J10-I(z) = −ln A(z)·r_B(z)/(c·d̄_phys(z)) = (r_B(z)/R(z))·W(q, τ₀(z))** | C3: identity exact to 2.5×10⁻¹⁶ |

**Rest-frame opacity — stated plainly.** τ₀ and q are rest-frame quantities: τ₀ is the
differential Thomson depth of the scattering cloud in the emitting gas's own frame, and
q is the source-geometry index of the transfer function; neither redshifts. Therefore
the atom at z is A(z) = exp(−τ₀(1+q/3)) = A(0) **z-invariant**, and W(q, τ₀(z)) = W(q)
**z-invariant** (C4: mock carries this exactly). Any measured z-drift of A beyond errors
is BLR evolution or a failure of the rest-frame assumption — itself a registered check.
Observer-frame lags must be corrected: d̄_rest = d̄_obs/(1+z) (C7: forgetting the factor
phantom-violates the window — J10-I_naive = 0.770 < 4/3 at z=2 in a framework world).

**a₀(z) law (G237's file-committed prescription — recoverable from its files, so no
u(z)-table interpolation is needed):** framework `a₀(z)/a₀(0) = 1 − 3×10⁻⁵ z` (S3-05, z ≤ 3);
rivals: M-RISE `1 + 1.6986 z` (Ciocan 1.59×10⁻¹⁰ m/s² per z), Milgrom `(1+z)^{3/2}`.

## 2. The z-curve of the radius and of J10-I

Synthetic: M_b = 1×10⁹ M☉ (enters only the contrast below — it **cancels in every ratio**),
r_B(0) = **40.9 ld** (doorB A2744-QSO1 density-local scale); deep-MOND √(GM_b/a₀) =
1.454×10⁶ ld ≈ 1.22 kpc is **not** the BLR radius (contrast only, C2b).

r_B(z)/r_B(0) = [a₀(0)/a₀(z)]^{1/2} = u(z)/u(0):

| z | framework (S3-05) | M-RISE | (1+z)^{3/2} |
|---|---|---|---|
| 0.5 | 1.000008 | 0.7354 | 0.7378 |
| 1.0 | 1.000015 | 0.6088 | 0.5946 |
| 2.0 | **1.000030** | 0.4769 | 0.4387 |

**J10-I(z) curve (q = 1, τ₀ = 2, rest-frame lags; d̄_phys days below):**

| z | framework world (R(z)=r_B(z)) | M-RISE world (R(z) obeys rival a₀) |
|---|---|---|
| 0.0 | 1.7778 OPEN | 1.7778 open |
| 0.1 | 1.7778 OPEN | 1.9228 open |
| 0.3 | 1.7778 OPEN | **2.184 CLOSED** |
| 0.5 | 1.7778 OPEN | **2.418 CLOSED** |
| 1.0 | 1.7778 OPEN | **2.920 CLOSED** |
| 2.0 | 1.7778 OPEN | **3.728 CLOSED** |

d̄_phys rest-frame days (τ₀=2, q=1 → E[D] = τ₀(½+q/4) = 1.5; d̄ = 1.5·r_B_ld):
framework 61.350 / 61.350 / 61.351 / 61.352; M-RISE 49.934 / 45.115 / 37.348 / 29.258
at z = 0.3 / 0.5 / 1 / 2; observer-frame: ×(1+z) → 79.76 / 92.03 / 122.70 / 184.06 d.

## 3. The cosmography probe — closed-form prediction chain (the novel step)

The pair (A(z₁), d̄(z₁)) inverts to (τ₀, q) **once** (C5: q = (1−W/2)/(W/4−1/3),
τ₀ = −ln A/(1+q/3) → recovered 1.0000000000 / 2.0000000000 at z₁ = 0.3, W_obs = 1.777778);
then the a₀(z) law predicts the ratio at any other z:

```
    d̄(z₂)/d̄(z₁) = r_B(z₂)/r_B(z₁) = [a₀(z₁)/a₀(z₂)]^{1/2} = [u(z₂)/u(z₁)]
```
E[D] cancels (τ₀- and q-free — verified: ratio identical at (τ₀,q) = (0.4,0) and (2,1)),
M_b cancels: **the rest-frame scatter-lag pair is a pure a₀-cosmography measurement.**
Framework-world synthetic verification (z₁ = 0.3; z₂ = 0.5 / 1 / 2): predicted ratios
1.000003 / 1.000011 / 1.000026 vs generated — **max |pred/meas − 1| = 2.2×10⁻¹⁶**
(C6, bound 5×10⁻⁶). The framework law predicts **lag z-invariance** (the u-chain is flat
to 10⁻⁵); a growing-a₀ rival predicts the lag to shrink with z.

## 4. Window CLOSE vs OPEN; 3σ resolution in days (S/N = 30)

- **Framework law world:** J10-I(z) = W(q) = 1.7778 **flat, window OPEN at every z < 3**
  (C8). Predicted consistency band at S/N=30 (K09 derivative
  se(J10-I)/J10-I = √[(se(A)/(A|lnA|))² + (se(d)/d)²] = √[(1/(30·8/3))² + (1/30)²] = 3.56%):
  **1.778 ± 0.190 → [1.588, 1.968] ⊂ [4/3, 2]** — the prediction never touches the window edges.
- **M-RISE world:** the true radius shrinks faster than the framework's; the lag is too
  short at the framework radius ⇒ J10-I(z) = W(q)·√(a₀_MR/a₀_fw) **exits HIGH**: nominal
  closure **z_c = 0.156** (q = 1); q-dependence z_c = {≈0.00 (q=0), 0.156 (q=1), 0.331 (q=3),
  0.540 (q=10)}; volume window (W_v(2,1) ≈ 1.676 interpolant of the K09 τ₀=2 row):
  z_c ≈ 0.179; Milgrom rival: z_c ≈ 0.170. **3-sigma violation from z ≈ 0.345** (C10).
- **Deviation in days at z = 1 that resolves it at 3σ:** σ(d̄) = d̄/30 = 2.045 d →
  **3σ floor = 6.14 d** (lag-only; 6.55 d with the atom term). The M-RISE deviation is
  **Δd̄ = |61.351 − 37.348| = 24.0 d = +11.7σ (lag) / +8.9σ (window)** — **one S/N=30
  object at z=1 resolves the framework vs a growing-a₀ rival**.

## 5. Falsifier (pre-registered) — the cosmographic level

1. **F-COSMO (this port):** a(z) measured from BLR scatter-lag across **two redshifts**
   whose rest-frame lag ratio violates the a₀(z)-law window at **≥ 3σ** —
   |d̄(z₂)/d̄(z₁) − [a₀(z₁)/a₀(z₂)]^{1/2}| ≥ 3·√2/S/N — kills the framework **radius law at
   the cosmographic level** (not just locally): the pair-inversion probe is dead, not a
   single object. At S/N=30 a growing-a₀ rival is excluded at 3σ from z₂ ≈ 0.62, at 5σ
   from z₂ ≈ 0.85 (C11: −2.1σ / −5.4σ / −8.8σ at z₂ = 0.5 / 1 / 2); the J10-I window
   itself is the sharper knife (≥3σ from z ≈ 0.35, single pair; 98.5% single-pair
   violation rate at z=0.5, C12). Framework world: chain residuals −2.2×10⁻¹⁶ σ.
2. **F-local (inherited, unchanged):** J10-I(z) outside [Wmin_g, Wmax_g] + 3σ under the
   framework radius kills that geometry's a₀-radius reading (K09 F1); outside ALL
   geometries' windows kills the transfer reading outright (K09 F3).
3. **F-atom:** |A(z₂) − A(z₁)| > 3σ_A voids the rest-frame-opacity assumption (C4/C12:
   conserved to 10⁻¹² in the mock; S/N=30 draws recover τ₀ = 2.001, q = 1.046 ± 0.452).
4. **F-method:** any analysis using observer-frame lags without the /(1+z) correction
   phantom-violates the window (0.770 < 4/3 at z=2) and is discarded on sight (C7).
5. **Kill-condition self-check (pre-registered):** if the closed-form chain fails its own
   noiseless synthetic check at > 5 SE (SE set at 5×10⁻⁶ relative), the port is wrong and
   reported honestly. Measured closure **2.2×10⁻¹⁶ ≪ 5×10⁻⁶** — the port is self-consistent.

## 6. Status ledger

- M04: **derived + verified 14/14, exit 0** (`M04_j10z.py` → `.out` → `M04_results.json`).
  G237's u-law inverted algebraically (a₀(z) = a₀(0)[u(0)/u(z)]², 3.3×10⁻¹⁶); r_B(z) law
  1:1 with G237's u-chain; J10-I(z) identity 2.5×10⁻¹⁶; inversion exact (1/2 recovered to
  10⁻¹⁰); chain closure 2.2×10⁻¹⁶; z-curve flat-OPEN vs M-RISE CLOSED from z_c = 0.156
  (3σ from 0.345); z=1 resolution 24.0 d = 11.7σ/8.9σ vs a 6.1–6.6 d 3σ floor at S/N=30;
  seeded draws: 98.5% single-pair falsification at z=0.5.
- Momentum: local radius test (doorB 40.9 vs 45 ld, CONSISTENT-OPEN ×1.10), virial-T
  null (G236), sector z-invariance (G237). M04 adds the **transfer-function channel** as
  a z-probe: one object pair ≈ one cosmography measurement, no dark-matter parameter.
- Honest limits: volume window at (τ₀=2, q=1) is a 2-point interpolant of K09's τ₀=2 row
  (K07 lane owns the full surface; z_c,vol ≈ 0.18 is indicative); σ model assumes S/N=30
  in both atom and lag (L05 not landed); the mock is noiseless-exact plus seeded S/N=30
  draws — real BLR evolution, geometry mixing, and calibration systematics are not in it.
- **No git commit; synthetic data only.**

## Files

- `M04_j10z.py` (lane: 14/14 PASS, rerunnable), `M04_j10z.out`, `M04_results.json`.