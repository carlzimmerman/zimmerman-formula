# K12 — GEOMETRY-IGNORANCE AUDIT of the scatter-clock falsifier battery

**2026-09-23 · machine-checked re-derivation · what each falsifier claims when the emission geometry is unknown (central vs volume-uniform vs thin shell)**
Files: `K12_geometry_audit.py` · `K12_geometry_audit.out` · `K12_results.json` (same dir) · engine: J02 kernel (`J02_moment_hierarchy.py::simulate`) + a local shell birth sampler (same transport logic).

## The question

An observer cannot know the emission geometry a priori. The frozen lane's own
AUDIT.md marks central-source scope "essential; tested adversarially" (the
uniform-volume source already differs from the central lag formula by 63.83 MC
SE). This lane asks, per falsifier: **what does the claim still assert when the
geometry assumption is dropped?** Everything below is pre-registered (kill
thresholds printed before any number in the `.out`) and machine-checked on
τ₀ = 1 clouds, kernel κ(r) = 1+q r², R = c = s_e = 1, isothermal, conservative
Thomson, all photons counted.

## Pre-registered checks (kill thresholds — declared before running)

| check | content | kill threshold |
|---|---|---|
| C0 engine sanity (volume) | exposure identity E[v²] = 2E[N]; Q-bookkeeping E[t] = E[D]+E[Q]; P2 Dynkin E[t]_vol = ∫rκ dr + E[μ_exit] − ½E[F(r₀)] (E[F(r₀)] = 3/5 + q·3/14) | any violation > 5 SE (P2: > 8 SE) ⇒ engine fault, other checks void |
| C1 J05 bound under volume | E[D²] ≥ L = 3E[Dv²]²/E[v⁴], slack = E[D²]/L | slack < 1.02 absolute, or slack < 1 + 3σ (50-block jackknife) on any volume cloud; target slack ≥ 1 |
| C2 J07 envelope under volume | \|H(w)\| + 6(se_c+se_s) ≥ max(0, 1−½w²E[D²]) − 1e-9, w ∈ {0.25…8} | any w below the envelope by > 6 SE |
| C3 frozen Thm2 band under volume | (√(1+R)−1)/2 ≤ d ≤ √R/2, d = E[D]_vol (J02B-corrected), R = E[v²] | either endpoint violated > 3 SE on any volume cloud ⇒ band is not geometry-free; central control must pass both endpoints |
| C4 naive observer | d := ∫rκ dr (central Thm1) injected on volume clouds | informational (false pass recorded) |
| C5 shell spectrum | r₀ = 0.5, 0.9, q = 0 | informational |

## Machine-checked re-derivation (the analytic spine)

Exact identities (verified numerically per cloud in `.out`; the q = 0 reduction
is exact to the engine's noise):

1. **J05 is geometry-free.** Conditional on the trajectory v ~ N(0, 2·ang) for
   *any* source geometry (P1); hence E[v²] = 2E[ang] = 2E[N] (isothermal),
   E[Dv²] = 2E[D·ang], E[v⁴] = 12E[ang²]. Cauchy–Schwarz on (D, ang) then
   gives E[D²] ≥ 3E[Dv²]²/E[v⁴] — no κ, no n_e, no geometry parameter.
   Engine: holds on all volume clouds (slack 1.36 / 1.19 / 1.09 for q = 0/3/10).
2. **J07 is geometry-free.** cos x ≥ 1 − x²/2 for all x ⇒ E[cos(wD)] ≥
   1 − ½w²E[D²]; \|H(w)\| ≥ E[cos(wD)]; D ≥ 0. Only E[D²] enters.
   Engine: holds at all w ∈ {0.25…8} on all volume clouds.
3. **The frozen Thm2 band is central-source-specific.** R = σ²/s² = 2E[N] and
   E[N] = E[∫κ ds] hold for any source (exposure + compensator). The band is
   obtained by eliminating τ through *central-source* relations
   (E[D] = τ/2, E[N] = τ²/2 + τb, b = E[μ_exit] ∈ [0,1]). Under volume the
   coupling rotates: with d = cE[D]_vol/R and, for **uniform κ**, E[N] = E[t] =
   d + E[Q] (Q = (x_exit−x₀)·u_exit), so R = 2d + 2E[Q] and
   **lower endpoint holds ⇔ E[Q] ≤ d + 2d²** (verified: q=0 gives
   E[Q] − (d+2d²) = +0.0313 ⟺ lower endpoint violated by 14.9 SE). For q > 0,
   κ ≥ 1 everywhere makes E[N] = E[∫κds] ≫ E[t] (measured E[N]/E[t] = 2.56 and
   6.02 for q = 3, 10): the frozen R↔d relation fails harder and the reduction
   has no closed form (labeled N/A in the output). The upper endpoint
   d ≤ √R/2 ⇔ E[Q] ≥ 2d² − d survives (Q ≥ 0).

## Results

### C1 — J05 width bound on volume sources (target: slack ≥ 1)

| cloud (τ₀=1) | E[D²] | L = 3E[Dv²]²/E[v⁴] | slack ± σ_jk | verdict |
|---|---|---|---|---|
| volume q=0 | 0.5255 | 0.3854 | **1.364 ± 0.009** | PASS |
| volume q=3 | 2.1842 | 1.8325 | **1.192 ± 0.005** | PASS |
| volume q=10 | 9.6771 | 8.8600 | **1.092 ± 0.005** | PASS |
| central q=0 (control) | 0.7646 | 0.6158 | 1.242 ± 0.007 | PASS (≈ J05's 1.25) |

The bound is **density-free AND geometry-free**; volume slacks are in the same
1.09–1.36 near-tight band as the central slacks (1.06–1.25) that J05 reported.

### C2 — J07 quadratic envelope on volume sources

| cloud | \|H(w)\| ≥ max(0,1−½w²E[D²]) all w ∈ {0.25,…,8} | min(\|H\|+6SE−env) |
|---|---|---|
| volume q=0 | PASS | +0.0051 |
| volume q=3 | PASS | +0.0289 |
| volume q=10 | PASS | +0.1572 |

The envelope is **geometry-free** (linear frozen T3 also holds, but the
quadratic one is the binding, asymptotically-exact floor).

### C3 — THE FROZEN-LANE CROSS-CHECK: Thm2 band vs volume, J02B-corrected E[D]_vol

Measured triple (σ²/s² = E[v²], s_e = 1, d = E[D]_vol): **does it stay in the frozen band?**

| cloud | d = E[D]_vol | R = E[v²] | lo = (√(1+R)−1)/2 | hi = √R/2 | lower | upper |
|---|---|---|---|---|---|---|
| **central** q=0 (control) | 0.5002 | 2.807 | 0.4756 | 0.8377 | PASS (−34 SE) | PASS (−471 SE) |
| volume q=0 | 0.3381 | 1.874 | 0.3476 | 0.6844 | **VIOLATED +14.9 SE** | PASS (−540 SE) |
| volume q=3 | 0.8579 | 6.898 | 0.9052 | 1.3132 | **VIOLATED +39.3 SE** | PASS (−378 SE) |
| volume q=10 | 1.9328 | 28.239 | 2.2037 | 2.6570 | **VIOLATED +111.1 SE** | PASS (−297 SE) |

**The band is NOT geometry-free: with the J02B-corrected (honest, measured) lag
the lower endpoint fails on every volume cloud — 3-seed-central control passes,
so the harness is sound.** The J02B lag correction is *necessary but not
sufficient*: correcting E[D] does not repair the band because the band's
endpoints are themselves consequences of the central-source E[N]↔E[D] relations
(THEOREM.md Thm 2 proof, steps 3–4). The defensive consequence: a
geometry-ignorant observer who measures (σ, s_e, E[D]) and applies the frozen
band to a volume-emitting LRD gets a **false kill** of a model that is actually
Thomson-consistent — and, per C4, the same observer gets a *false pass* by
injecting the central formula value instead:

### C4 — naive-observer control (the trap, quantified)

| volume cloud | d injected = ∫rκ dr (central Thm1) | band verdict | honest d verdict |
|---|---|---|---|
| q=0 | 0.500 | **PASSES (FALSE PASS)** | fails (lower) |
| q=3 | 1.250 | **PASSES (FALSE PASS)** | fails (lower) |
| q=10 | 3.000 | fails (upper) | fails (lower) |

Either way the frozen band misleads under volume: the wrong lag passes it (q=0,3),
and at q=10 the *central-formula* lag kills it from the wrong side.

### C5 — shell spectrum (informational)

| shell (q=0, τ₀=1) | E[D] | R | lo | hi | membership |
|---|---|---|---|---|---|
| r₀ = 0.5 | 0.4340 | 2.461 | 0.4301 | 0.7843 | INSIDE (margin −5.6 SE) |
| r₀ = 0.9 | 0.2800 | 1.513 | 0.2927 | 0.6151 | OUTSIDE (+21.1 SE lower) |

Even mid-shell emission sits precariously at the lower edge; surface-near shells
violate like volume sources. Only the central source is safely inside the band.

## Verdict table (deliverable 4)

| falsifier | geometry-free | needs-correction | broken-under-volume | correction reference |
|---|---|---|---|---|
| **J05** E[D²] ≥ 3E[Dv²]²/E[v⁴] | **YES** (Cauchy–Schwarz + P1 hierarchy hold for ANY source) | no | no | none needed |
| **J07** \|H(w)\| ≥ max(0, 1−½w²E[D²]) | **YES** (cos x ≥ 1−x²/2; \|H\| ≥ E[cos(wD)]) | no | no | none needed |
| **frozen Thm1** E[D] = ∫rκ dr | NO (central-only) | YES | YES | J02B P2: E[D]_vol = E[t] − E[Q], E[t] = ∫rκ dr + E[μ_exit] − ½E[F(r₀)] (recorded Q = 0.597; 63.8 SE failure) |
| **frozen Thm2** lag–width band | NO (central-only) | **correction unavailable from (σ, s_e, E[D]) alone** — R = 2E[N] with E[N] = E[∫κds]; uniform-κ volume: R = 2d + 2E[Q], lower endpoint fails iff E[Q] > d + 2d² (E[Q] unobservable to a geometry-blind observer); q>0 E[N] ≥ E[t] amplifies | **YES — lower endpoint fails under volume EVEN with the J02B-corrected E[D]_vol** (14.9 / 39.3 / 111.1 SE at q = 0/3/10); upper endpoint survives | J02B P2 Q-coupling; E[N] = E[∫κds] compensator; volume-domain band needs E[Q]/κ-resolved data or the lower endpoint is withdrawn under unknown geometry |
| J09-D / J10 window [4/3, 2] | NO (geometry-specific per J11: volume window ≈ [1.3, 1.9], τ₀-dependent) | YES | YES | J11 volume atom / J11 window (cross-ref, not re-run here) |

## Honest edges

- All numbers are MC estimates at n = 10⁶ (SEs reported; R = E[v²], d = E[D]_vol
  measured, never derived-from-D fed back). The identities checked (exposure,
  compensator, P2-Dynkin, C–S bound, cos envelope) are exact within the model;
  the numbers are evidence.
- The reduction E[Q] ≤ d + 2d² is exact only for uniform κ (q = 0), where it
  machine-verifies (E[N] = E[t] exactly); for q > 0 it is absent by design and
  the mechanism (E[N] ≫ E[t]) is printed instead.
- Shell runs reuse the J02 transport kernel with a locally-written shell birth
  sampler — same engine, not a third independent implementation; shells are
  informational per pre-registration.
- No circularity: nothing in this audit reuses a band-derived D; the band test
  uses the independently measured moments exactly as the frozen lane demands.
- Not claimed: any observational outcome, novelty, or a "correct" volume band —
  the audit's deliverable is the geometry-validity registry above.

## Register line

**GEOMETRY FREE: J05, J07** (verified on volume q = 0/3/10). **GEOMETRY KILLED:
frozen Thm2 lower endpoint** under volume (3/3 volume clouds, 14.9–111.1 SE,
even with the J02B-corrected lag); Thm1 central-only (J02B on record);
J09-D/J10 window geometry-specific (J11 on record). An observer armed with the
battery under unknown geometry may safely fire **J05 and J07**; the frozen
**lag–width band's lower endpoint must carry the central-source label** or be
withdrawn for volume/thick-shell emitters.