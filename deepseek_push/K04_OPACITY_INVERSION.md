# K04 — THE OPACITY INVERSION and the THREE-OBSERVABLE TEST
**2026-09-23 · K-series · family κ(r) = τ₀(1 + qr²), T = 1, central source · all numbers machine-checked on J02's independent solver (n = 10⁶ per cloud, exact optical-depth bisection, no null-collision thinning)**

**What this registers.** An observer with a *velocity-resolved transfer function* Ψ(τ, v) reads three numbers off one dataset — the atom-spike fraction (zero lag, zero width), the mean lag, and the line width — and the model makes a fully determined, non-circular statement: the first two *invert* to the two opacity parameters in closed form; the **third is then predicted, not fitted**, and compared. If it disagrees at ≥ 5σ the Thomson-sphere reading with κ = τ₀(1 + qr²) is falsified. Nothing in (B) touches the data used in (A).

| | closed form | where it appears |
|---|---|---|
| inversion | τ̂₀ = −3 ln Â − 4Ê[D],  q̂ = 4Ê[D]/τ̂₀ − 2 | §1, derived; §2 verified at 5 clouds |
| third-observable chain | E[v²] = 2E[ang] = 2E[N] = 2∫κ(r)ρ(r)dr | §3, exact identities |
| E[N] surface | E[N] = Π₀ + ∫₀¹ κe^{−Λ}(A + B)dr, A,B the closed Thomson moments | §3, deterministic solver |
| thin-cloud limit | E[N] = τ₀(1 + q/3) + c₂τ₀² + O(τ₀³), c₂ closed form | §3, verified |
| falsifier | one number: z = (E[v²]ₘ − 2E[N](τ̂₀,q̂))/σtot; kill at z ≥ 5 | §5 |

---

## 1. (A) The closed-form inversion

Two exact, on-record identities fix the map (τ₀, q) → (A, E[D]) for the central source:

> **atom law**  A = P(N = 0) = exp[−τ₀(1 + q/3)]     (to-wall optical depth from the origin is direction independent; T-independent; K03 G4)
> **mean delay**  E[D] = ∫₀¹ r κ(r) dr = τ₀(½ + q/4)     (Theorem 1, J02 B1)

Eliminate q: q = 4E[D]/τ₀ − 2, insert:

```
−ln A = τ₀(1 + q/3) = τ₀ + τ₀q/3 = τ₀ + (4E[D] − 2τ₀)/3 = τ₀/3 + 4E[D]/3
      ⟹  τ₀ = −3 ln A − 4 E[D]            ⟹  q = 4E[D]/τ₀ − 2          (1)
```

**τ̂₀ = −3 ln Â − 4 Ê[D],  q̂ = 4Ê[D]/τ̂₀ − 2.** Bijective on τ₀ > 0, q > −1; the two observables are *additively separated* in the first inverse. Error propagation (delta method, used in the tests):

```
σ(τ̂₀) = √( (3σ_A/A)² + (4σ_D)² ),   σ(q̂) = √( (4σ_D/τ̂₀)² + (4Ê[D]σ(τ̂₀)/τ̂₀²)² )
```

## 2. (A) Verification on the engine (n = 10⁶, ≥ 4 clouds)

Measured (A, E[D]) → (1) → (τ̂₀, q̂), compared with the set inputs. All five clouds pass at z < 6 (full table in `K04_inversion.out`):

| cloud | (τ₀,q) | A | E[D] | τ̂₀ | q̂ | z_τ | z_q |
|---|---|---|---|---|---|---|---|
| C1 | (1, 0) | 0.36724 | 0.50052 | 1.00316 ± 0.00487 | −0.0042 ± 0.0101 | 0.65 | 0.42 |
| C2 | (1, 3) | 0.13506 | 1.24986 | 1.00656 ± 0.00930 | 2.9669 ± 0.0462 | 0.71 | 0.72 |
| C3 | (1, 10) | 0.01302 | 2.99754 | 1.03297 ± 0.02823 | 9.6075 ± 0.3174 | 1.17 | 1.24 |
| C4 | (2, 3) | 0.01839 | 2.50127 | 1.98277 ± 0.02367 | 3.0460 ± 0.0604 | 0.73 | 0.76 |
| C5 | (0.5, 2) | 0.43443 | 0.50003 | 0.50104 ± 0.00457 | 1.9919 ± 0.0369 | 0.23 | 0.22 |

The inversion is exact; the only error is measurement error, correctly propagated.

## 3. (B) The third observable, derived and predicted (never fitted)

**The exact chain.** Conditional on the trajectory the velocity increment per collision is Gaussian with variance 2T(1−μ) (J01 lemma), so per photon *exactly*:

```
E[v²] = 2E[ang],   E[ang] = E[Σⱼ (1−μⱼ)] = E[N]·E[1−μ] = E[N]   (T = 1)   (2)
```

(the Thomson kernel has E[μ] = 0 exactly). Hence **E[v²] = 2E[N]**, and N is the collision-rate functional of the path:

```
E[N] = E[∫₀^τ κ(X_s) ds] = ∫₀¹ κ(r) ρ(r) dr,            ρ = exact time-at-r density   (3)
```

**Why there is no algebraic shortcut, and why that is the point.** E[N] is not expressible through (A, E[D]) for this family — the first-flight part is, the continuation is not: the post-collision directional law is Thomson, not uniform, so the residence density obeys a genuine transport fixed point (no direction-average closes the equation; the mean *scattered* direction is zero, which is exactly why the one-collision decorrelation that makes E[D] density-free does not extend). An observer who can only invert (A, E[D]) cannot *derive* E[N]; the registered test therefore uses the **exact surface** computed by a deterministic solver — a different algorithm from the Monte-Carlo engine (deterministic quadrature fixed point vs. stochastic simulation; shared only the model's defining κ-integral).

**The solver (independent, deterministic, converged, certified).** State (r, μ) = (radius, cosine with local radial). One flight from (r, μ): wall distance s_w = −rμ + √(r²μ² + 1 − r²), partial optical depth Λ(s) = τ₀[s + q(r²s + rμs² + s³/3)], collision probability Π = 1 − e^{−Λ(s_w)}. Because the Thomson kernel is quadratic in the scattering cosine, the continuation averages over the scattered direction in **closed form** with the two moment fields

```
A(r') = (3/16)∫₋₁¹ C(r',μ')(3 − μ'²)dμ',   B(r') = (3/16)∫₋₁¹ C(r',μ')(3μ'² − 1)dμ'
```

and the collision-count functional satisfies the contraction fixed point

```
C(r,μ) = Π(r,μ) + ∫₀^{s_w} κ(r(s)) e^{−Λ(s)} [ A(r(s)) + B(r(s)) γ(s)² ] ds,
            γ(s) = u·r̂(s) = (rμ + s)/r(s)                                   (4)
```

For the central source (first flight from the origin: radial direction, and the post-scattering state has γ = 1 because r̂ at the first collision *is* the incoming flight direction):

```
E[N] = (1 − A₀) + ∫₀¹ κ(r) e^{−Λ(r)} [ A(r) + B(r) ] dr,   A₀ = e^{−τ₀(1+q/3)}   (5)
```

(5) is the closed-form statement for central source, exact up to the certified quadrature error: warm-started 1000×88 resolution solve agrees with the science grid (700×72) to 4.7×10⁻⁶ at (1,3) and 2.3×10⁻⁵ at (1,10) (certification check K1 in `.out`); the bound used in the tests is 3× that.

**Thin-cloud closed form (verified).** Expanding (5) around τ₀ → 0:

```
E[N] = τ₀(1 + q/3) + c₂ τ₀² + O(τ₀³),
  c₂ = −(1+q/3)²/2 + (3/8)∫₀¹∫₋₁¹ (1+qr²)(1+μ²)[s_w + q(r²s_w + rμs_w² + s_w³/3)] dμ dr   (6)
```

with s_w = s_w(r, μ) as above — every ingredient elementary. Solver fit vs. closed form: relative agreement 3.6×10⁻⁵ at q = 0 and 3.2×10⁻⁴ at q = 3 (the O(τ₀²) curvature of E[N] is *predicted*, not parametrized). The thin-cloud engine check (§3, K3): surface E[N] = 0.050957 vs measured 0.050942 ± 0.00011 at τ₀ = 0.05, z = 0.13.

**The prediction.** From the *measured* (A, E[D]) of cloud k, invert to (τ̂₀, q̂) — and only then evaluate the surface:

```
E[v²]_pred = 2·E[N](τ̂₀, q̂)          [no datum of cloud k beyond (A, E[D]) enters]
σ_pred = |∂E[N]/∂τ₀|σ(τ̂₀) + |∂E[N]/∂q|σ(q̂) + certified surface err        (7)
```

with the partial derivatives taken from the same surface (delta method, not fits). **Comparison:** registered statistic z = |E[v²]_meas − E[v²]_pred|/(σ_v² + σ_pred); z < 5 required. Results at all five clouds (n = 10⁶, seeds 101–105; E[v²] = 2E[N] and E[v²] = 2E[ang] re-verified on the same runs at z < 6; the surface itself crossed against the engine's own E[N] at z ≤ 0.81 in every cloud):

| cloud | E[v²]_meas | E[v²]_pred = 2 E[N](τ̂₀,q̂) | z |
|---|---|---|---|
| C1 (1,0) | 2.8101 ± 0.0077 | 2.8125 ± 0.0159 | 0.11 |
| C2 (1,3) | 8.7248 ± 0.0202 | 8.7430 ± 0.1250 | 0.12 |
| C3 (1,10) | 37.2224 ± 0.0760 | 37.3424 ± 1.8276 | 0.06 |
| C4 (2,3) | 27.9249 ± 0.0571 | 27.9277 ± 0.5753 | 0.00 |
| C5 (0.5,2) | 2.3865 ± 0.0071 | 2.3850 ± 0.0272 | 0.04 |

(Exact numbers with all errors: `K04_results.json`; the full transcript: `K04_inversion.out`.)

**E[D v²], honestly.** The identity E[D v²] = 2E[D·ang] is exact and re-verified (J02), and E[D·ang] at fixed (τ₀,q) is a deterministic functional — but it is *not* reachable from (A, E[D]) without the same surface machinery extended to a path-dependent functional (the final-direction coupling), so it is not part of the registered prediction. It remains a consistency identity (J01/J02 35/35).

## 4. What the three-observable protocol is for an observer

One dataset, one observing run (velocity-resolved RM transfer function of a Thomson-sphere-like LRD):

1. **A** — the *zero-lag, zero-width spike*: photons with D = 0 (uncollided: exit without scattering; exact in the model) sit at zero lag *and* zero width (v = 0 exactly). A = fraction of flux at (D ≈ 0, v ≈ 0).
2. **E[D]** — the first moment of the lag distribution.
3. **E[v²]** — the second moment of the line profile (i.e., the autocorrelation curvature at zero lag).

Then: §1 gives (τ̂₀, q̂) from 1+2; §3(5) gives the *predicted* width moment; compare. **No fitting:** the third observable never enters the inversion; the surface is evaluated once at the inverted point. This is the registered, reproducible test; the engine, seeds, and the full transcript are in this directory.

## 5. The falsifier (stated exactly)

> **Registered test (any observer can run it).** Under the assumptions — quasi-spherical, optically resolved region; Thomson scattering; isothermal T = 1 band; density family κ(r) = τ₀(1 + qr²); central (point, isotropic) emission — measure (Â, Ê[D], E[v²]ₘ) with reported standard errors (σ_A from the spike count, σ_D, σ_v² from the moments). Compute τ̂₀ = −3 ln Â − 4Ê[D], q̂ = 4Ê[D]/τ̂₀ − 2, then E[v²]_pred = 2E[N](τ̂₀, q̂) from (5). **The family is falsified if** either (i) the inversion returns a physically impossible point (τ̂₀ ≤ 0 or q̂ ≤ −1, which require A or E[D] outside the model's reachable set), or (ii) **z = |E[v²]ₘ − E[v²]_pred| / (σ_{v²} + σ_pred) ≥ 5** at n ≥ 10⁶ equivalent (σ_pred from (7), including the certified surface error). One violation at ≥ 5σ with the assumptions verified kills the κ = τ₀(1+qr²) reading; the *inversion itself* is assumption-independent on its second step only insofar as the two identities (atom law, mean-delay) hold, and both are on-record exact within the model.

**Honest status.** Closed form: the inversion (1); the identities (2)–(3); the central-source functional (5); the thin-cloud expansion (6) with its coefficient. Numerics: surface certified to ≤ 3×10⁻⁵ relative at the extreme clouds; engine agreement at 5 clouds + thin-cloud limit; z-scores reported per cloud. Not claimed: any JWST data contact, general-(τ₀,q)-closed form of E[N] (no elementary dependence on the family parameters exists — (5) is the exact surface), E[D v²] as a *predictable* third observable.