# K08 — THE SHELL-GEOMETRY DOOR
**2026-09-23 · engine: `J02_moment_hierarchy.py::simulate` (exact optical-depth
bisection, kappa = tau0(1+q r²), c=1, T=1) + shell-source extension
(`K08_shell.py::simulate_shell`: source uniform on |x| = a, isotropic
direction, transport loop byte-identical to J02)**

Door question (J11 follow-up): real BLR clouds are **shell-like**, not uniform
balls and not point sources. For a shell emitting layer at radius fraction a,
is the window `W_shell = -ln A_s / E[D]_s` **tau0-free** (like central, where
W = (1+q/3)/(1/2+q/4) ∈ [4/3,2]) or **tau0-dependent** (like volume)?

---

## 1. Geometry and the exact atom

Photon starts at |x| = a, isotropic direction u; mu = x̂·u uniform in [-1,1].
Straight-line chord to the wall (positive root of |x + s u| = 1):

```
L(mu) = sqrt(1 - a^2 (1 - mu^2)) - a mu
```

Optical depth along the chord, |x + s u|² = a² + 2 a mu s + s²:

```
tau_esc(mu) = tau0 [ L + q ( a^2 L + a mu L^2 + L^3/3 ) ]
```

Zero-scatter escape (the atom) is **exact** by quadrature — a no-scatter
photon is straight-line by construction, so the survival probability is
`exp(-tau_esc)`:

```
A_shell(tau0, q, a) = (1/2) ∫_{-1}^{1} dmu  exp(-tau_esc(mu))
```

Limits: a→0 ⇒ L ≡ 1, A = exp(-tau0(1+q/3)) (central, direction-free);
a→1 (surface emissive) is a distinct measure from the J11 volume source.

**Verified vs engine MC at 16 configs** (a ∈ {0.15,0.3,0.5,0.7} ×
tau0 ∈ {0.5,1,2} q=0, plus q=3 tau0=1): max |z| = 2.38 (400k photons/pt).
The closed form is exact; the engine sampler/transport is consistent with it.

## 2. Protocol and pre-registered kill conditions

Grid: a ∈ {0.15, 0.3, 0.5, 0.7} × tau0 ∈ {0.5, 1, 2} × q ∈ {0, 3} (24 shell
runs, 400k), volume surface (6 runs, 300k), central anchors (6 runs, 200k),
plus **S7 high-stat reruns (1.5M/photon)** of the headline cells
(a=0.3 q=0/3, a=0.7 q=0) — motivated by first-pass data showing the a=0.3
classification was SE-limited.

Classification (pre-registered): per (a,q), chi² = Σᵢ (Wᵢ − W̄)²/SEᵢ² over
tau0 ∈ {0.5,1,2} (2 dof); chi² < 6 ⇒ **tau0-FREE**, ≥ 6 ⇒ **tau0-DEPENDENT**
+ slope (W(2)−W(0.5))/1.5. SE budget 0.05 on every window.

Kills (none fired): K1 quadrature-vs-MC atom |z| ≥ 4 (any of 16) · K2 E[D] ≤ 0
or window ∉ [0.5,4] · K3 transport cap · K4 window SE ≥ 0.05 · K5 central
closed-form drift > 0.05+5SE · K6 volume-at-tau0=1 vs J11 anchors 1.897/1.710
by > 0.07.

**Correction log (honesty):** v1 S5 check used the closed form
E[D|N=0] = <(tau0 f − L)e^{−τ0 f}>/A — **wrong**: D is built from *geometric*
segment lengths, not optical depth, so a zero-scatter photon has elapsed = L
and (x_f − x_0)·u_f = L ⇒ **D ≡ 0 identically**. Replaced by the exact
bookkeeping identity E[D|N=0] = 0, verified: means 1.0e-19 ± 3.9e-19 (q=0)
and 4.4e-19 ± 6.6e-19 (q=3), max|D| 6.7e-16 — machine zero, z = 0.26/0.67.

## 3. Results

**Atom (S1/S2, quadrature vs MC, max z):** 16/16 pass, max |z| = 2.38 (a=0.7,
tau0=2, q=0). Central anchors (S4): W within 0.005 of closed form at all 6
configs.

**Shell windows W = −ln A_s / E[D]_s (n=400k, SE per point ~0.003–0.006):**

| a | q=0: W(0.5/1/2) | chi² | class | q=3: W(0.5/1/2) | chi² | class |
|---|---|---|---|---|---|---|
| 0.15 | 1.9984/1.9938/1.9944 | 0.55 | FREE | 1.6137/1.6126/1.6161 | 0.36 | FREE |
| 0.3  | 2.0024/2.0002/1.9932 | 2.31 | FREE* | 1.6618/1.6610/1.6621 | 0.04 | FREE* |
| 0.5  | 2.0068/1.9994/1.9774 | 21.9 | DEP | 1.7651/1.7455/1.7225 | 44.9 | DEP |
| 0.7  | 1.9787/1.9939/1.9520 | 41.3 | DEP | 1.8976/1.8558/1.7594 | 464 | DEP |

(*SE-limited at 400k — resolved by S7.)

**High-stat (S7, n=1.5M):** a=0.3 q=0: **2.0048/2.0021/1.9958**, chi² = 7.92 ⇒
**DEPENDENT** (slope −0.0060); a=0.3 q=3: **1.6625/1.6570/1.6525**, chi² =
10.85 ⇒ **DEPENDENT** (slope −0.0067). a=0.7 q=0: 1.9847/1.9909/1.9611,
chi² = 84.8 — the tau0=1 “dip” is real (rise 0.5→1, fall 1→2; a genuine
third-order cumulant feature of the ratio).

**Volume surface (S6, this door):** q=0: 1.9017/1.8964/1.7960;
q=3: 1.8272/1.7129/1.4289 at tau0=0.5/1/2 — matches J11 anchors 1.897/1.710
(tau0=1) within 0.0015; J11 q=10: 1.314.

## 4. KEY QUESTION — answer

**The shell window is tau0-DEPENDENT, like volume — not tau0-free like
central.** Exactly flat only at a = 0, where the chord is direction-free
(Var(f) = 0) and the central closed form is recovered. For any a > 0 the
exp-average over mu gives −ln A = tau0⟨f⟩ − tau0²Var(f)/2 + O(tau0³), and the
ratio W is driven off its small-tau0 constant by O(tau0) curvature. The effect
is **weak and continuous in a** — at a = 0.3 it only resolves at n = 1.5M
(chi² 7.9/10.9 vs the pre-registered cutoff 6, fractional drift ~0.5% across
tau0 ∈ [0.5,2]) — then grows fast: chi² 22→464 at a = 0.5→0.7, slope
−0.016 (q=0) to −0.092 (q=3) per unit tau0. So: shell(a=0.3) is neither the
central band [4/3,2] nor the volume surface; it is its own, weakly
tau0-dependent surface that happens to sit *close* to central at q=0 and
*between* central and volume at q=3.

## 5. Three-way geometry discriminator (tau0, q) surfaces

| geometry | W(tau0=0.5/1/2, q=0) | W(0.5/1/2, q=3) | tau0-behavior | W(tau0=1, q=10) |
|---|---|---|---|---|
| central (closed form) | 2.000/2.000/2.000 | 1.600/1.600/1.600 | **FREE** (exact) | 1.444 |
| shell a=0.3 (n=1.5M) | 2.0048/2.0021/1.9958 | 1.6625/1.6570/1.6525 | **weakly DEP** (chi² 7.9/10.9) | (not run) |
| volume | 1.9017/1.8964/1.7960 | 1.8272/1.7129/1.4289 | **strongly DEP** | 1.314 (J11) |

Central is the only exactly flat surface; shell(a=0.3) at tau0=1 is 0.1% above
central (q=0) and +3.6% above central (q=3); volume drops to 5–11% below
central with growing tau0. For the J10-I/JWST correction, a shell-like BLR at
a≈0.3 with q≈3 demands W ≈ 1.66, not the central 1.60 — a 3.6% correction, and
unlike central it carries an O(tau0) residual that must be quoted with the
cloud's optical depth.

## 6. Limitations (honest SEs)

- E[D]_shell has **no closed form here** — measured (SE ~3–6e-3 window units per
  point; quoted). E[D] at q=0, a=0.3: 0.2402 ± 0.0004 (tau0=0.5), 0.4764 ±
  0.0006 (tau0=1), 0.9430 ± 0.0009 (tau0=2), n=1.5M each.
- Window SEs are delta-method incl. Cov(A,D); all quoted sizes ≥ 5 SE unless
  said otherwise; chi² thresholds pre-registered before S7 was added.
- Thin-shell limit: emission exactly at r=a. Finite-thickness layers and the
  a→1 vs J11-volume distinction (different emitter measure) are not yet
  treated; the a→0 side is anchored to the exact central closed form (S4, 6
  configs, |ΔW| ≤ 0.005).
- No git commit (per door policy). All numbers reproducible from
  `K08_shell.py` seeds; outputs in `K08_shell.out`, `K08_results.json`.