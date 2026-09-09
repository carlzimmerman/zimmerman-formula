# L17 — the A5 lane: a spatially nonlocal elliptic operator is not a protein

2026-09-08. Lane L17 of [CHARTER.md](CHARTER.md).
Script: [L17_elliptic_nonlocal.py](L17_elliptic_nonlocal.py) → [L17_elliptic_nonlocal.out](L17_elliptic_nonlocal.out).
Exit 0 (32 checks: **7 controls C0–C6, all PASS**, then 8 gate PASSes and 17 gate FAILs). Both footings.
Nothing under `closure_2026/integrable_clock_construction_2026/` was read, imported or executed.

`CRISPY_FRIED_CHICKEN_RECIPE.md` §3 lists five acceptable proteins. Four have been used to build
candidates; **A5 — spatially nonlocal elliptic operators, `(-D²)⁻¹`, `f(-D²/a₀²)`** — had not. Its
attraction is real and specific: an elliptic operator adds no temporal mode *by construction*, which is
the only obvious route to MOND without the extra scalar that every local single-metric construction buys,
and I3a wants exactly two tensor polarisations. This lane built it and ran it.

**Verdict: A5 is a seasoning, not a protein.** It cannot produce MOND — in the placement where it is the
mechanism it is killed by linearity, in the placement where it modifies an existing mechanism the length
a₀ licenses is 10⁶–10⁸ times too long and destroys MOND rather than shaping it. The recipe's own note —
"changes momentum scaling, NEVER perturbative amplitude order" — is not a caution about precision; it is
a theorem, and this lane derives it. **The failure is GENERIC to the class**, not to my realisation.

---

## The construction

A filter `F = f(-l² Δ)` can occupy exactly two places in the programme's filtered action (PAPER4's, with
`q'(s²) = ν(s) - 1` and ν the exact inverse partner of the frozen `μ(y) = 1 - e^{-y}`):

**A5-L — the filter is the mechanism.** `div[F grad Φ] = -4πGρ`, i.e. `σ(k) Φ_k = -4πG ρ_k`,
`σ = k² f(lk)`. The most MOND-like symbol a linear operator admits was chosen deliberately,
`f(x) = x/(1+x)` ⇒ `σ(k) = l k³/(1 + lk)`: Newtonian `k²` at short wavelength, `l k³` at long, positive
for every `k > 0`. It splits exactly, so the point-mass solution is elementary and needs no numerics:

    Φ(r) = -GM/r + (2GM/πl) ln r + const,      g(r) = GM/r² + 2GM/(π l r).

**A5-F — the filter modifies an existing mechanism.** PAPER4's action with `ξ → l₀`:
`Δu = 4πGρ`, `ΔΦ = 4πGρ + S ∇·[(ν-1)∇(Su)]`, `S = e^{l²Δ/2}`.

A5's own dimensional instruction `f(-D²/a₀²)` fixes `l`. A linear solve over the dimension exponents
(controlled against the Planck length from {G, ħ, c}) shows the length is **unique**, with no free
family: `l₀ = c²/a₀`. G cannot enter without a mass.

    l₀ = 9.6001e26 m = 31.11 Gpc   (canonical a0 = 9.3619e-11)
    l₀ = 7.9684e26 m = 25.82 Gpc   (alternate a0 = 1.1279e-10)

## What kills it

**1. The length is cosmological, and the mismatch is exactly `(c/v_flat)²`.** The length MOND needs
around a mass M is `r_M = √(GM/a₀)`, and

    l₀ / r_M = c² / √(GM a₀) = (c / v_flat)²

identically. Over 10⁸–10¹² M⊙ that is 8.1e7 down to 8.1e5 (canonical), 7.3e7 to 7.3e5 (alternate). It is
also mass-dependent (∝ M^{-1/2}), so no single operator length serves the observed mass range: the
required length spans a factor 100 over four decades in mass.

**2. Linearity, which is independent of the length and of the symbol.** A filter is a linear operator, so
the field equation obeys superposition and `g ∝ M` exactly. MOND needs `g ∝ M^{1/2}` (the BTFR). Measured:
`d ln g/d ln M = 1.000000` for A5-L against `0.5030` for the frozen exponential kernel on the same
estimator. The same statement was re-tested on an arbitrary dense nonlocal positive-definite operator
(200×200, not a differential operator): source ×100 gives field ×100 to 1e-11. For pure powers
`σ = l^{a-2} k^a`, `a = 3` is the unique exponent with `g ~ 1/r` — and every `a` has `d ln g/d ln M = 1`.
**The symbol has one free function and it buys the radial slope only; the mass slope is not for sale.**

**3. The amplitude, i.e. A5's own caveat, made quantitative.**

    g_A5L(asymptotic) / g_MOND = (2/π)(v_flat/c)²  = 2.4971e-07 (canonical), 2.7408e-07 (alternate)

for 10¹¹ M⊙ — short by 4.0e6 / 3.6e6, and the ratio is r-independent, so no radius rescues it. Under
G0's rescaling `ρ → ερ` the A5-L extra force is `O(ε^1.000000)` — exactly first order, as any linear map
must be — while the frozen kernel's phantom is `O(ε^0.498)`, non-analytic and *dominant* at small ε. A
linear operator cannot lower the order of anything. The transition radius is `π l₀/2` = 48.9 / 40.6 Gpc.

**4. I1 and I4 both fail structurally, not numerically.** A5-L's effective μ is `1/(1 + 2r/πl)`: a
function of *r alone*. Two galaxies at the same radius whose required μ differ by 8.6× receive identical
`μ_eff = 0.999999590752`. A filter is triggered by a **length** (a wavenumber); it cannot see an
amplitude. That is I4's exact prohibition — the trigger is a scale label, not a local acceleration.

**5. The Solar System passes, vacuously.** A5-L's anomalous sunward acceleration at Saturn is
6.1e-20 m/s² (canonical) against the repository's α=1 gate of 3.7e-14 — 1.7e-6 of the bound. It passes
for the same reason it fails the MOND gate: the modification is ~1e-16 of Newton everywhere inside 1 Mpc.
A gate a theory passes by doing nothing is not evidence of screening, and it is reported as such.

**6. A5-F is a pincer with no interior.** At `ξ = l₀` the Gaussian filter smooths the galaxy over 31 Gpc:
at 20 kpc the MOND argument `|∇(Su)|/a₀` is suppressed by **1.4e19** and the deep-MOND phantom by 2.2e9 —
MOND is not modified, it is annihilated, and the result is Newton. The opposite sign, a sharpening filter
`1 - ξ²Δ`, gives `u - 4πGξ²ρ`; in a real exponential disc that is `y = 6.9e15`, so `μ = 1` to machine
precision — Newton again. The window in which a filter is merely *harmless* on a galaxy is `ξ ≲ 4e2 pc`;
`l₀` exceeds it by 8.3e7. PAPER4's Solar-System-fixed `ξ = 0.02–0.05 pc` sits comfortably inside that
window, which is exactly why PAPER4 works and why its length is **not** set by a₀.

## The DOF count: 2 + 0 + 1 = 3

The counter is a linear Dirac analysis (primary constraints from ker M; the chain propagates only the
combinations whose bracket with the primary set vanishes). It reproduces six textbook counts before being
pointed at the candidate — **free scalar 1, scalar+multiplier 0, Maxwell 2, Proca 3, linearised ADM/GR 2,
massive Fierz-Pauli 5** — the GR control being the one the brief asked for. The Fierz-Pauli reduction is
built symbolically at one real Fourier mode with parity `(-1)^{#z indices}`.

| sector | result |
|---|---|
| tensor (linearised GR, control) | **2** |
| filter pair, spatial `(1 - l²Δ)`, localised as `L = λ[(1-l²Δ)w - u]` | **0** — four second-class constraints, exactly as A5 claims |
| the same pair with a temporal `(1 - l²□)` | **2**, kinetic eigenvalues −2/+2, a ghost pair — P6 reproduced |
| at a zero of the symbol | the quartet collapses to 2 first-class: **ellipticity is load-bearing**, the word "auxiliary" is not (P4) |
| the foliation the filter requires | **1** |
| **N_grav** | **3 — fails I3a** |

A5's "no temporal mode" is **true of the filter and false of the theory the filter has to live in.** There
is no covariant elliptic operator on a Lorentzian manifold — `D²` built from `g` alone is `□`, hyperbolic
— so "spatial" requires a unit timelike `n_μ`, i.e. a khronon. And the A5 term cannot pay for it: built
from `γ_ij` alone with `N` only in the measure, its khronon kinetic matrix is **exactly zero** (checked
against the host's `c₁₄ (∂_i ln N)²`, which gives `2c₁₄k² > 0` and one mode). So either the host supplies
`c₁₄ ≠ 0` and `N_grav = 3`, or nothing does and the foliation scalar is infinitely strongly coupled —
**P7 verbatim**. Inertness is not the same as being free.

## The ledger

| | check | |
|---|---|---|
| PASS | C0–C6 | seven controls: kernel series, Planck length, the log-term integral, the M-slope estimator on the frozen kernel, PAPER4's ξ inert at 20 kpc, both filters' interior limits, six textbook Dirac counts |
| PASS | L1 | A5's operator length is unique: `c²/a₀` |
| FAIL | L2 | it is not the length MOND needs — `l₀/r_M ≥ 7.3e5` |
| FAIL | L3 | one operator cannot carry the 100× length spread of the galaxy mass range |
| FAIL | L4 | no length is I4-legal **and** carries a₀ **and** equals `r_M` |
| FAIL | M1 | `d ln g/d ln M = 1.000000`, MOND needs 0.5 |
| FAIL | M2 | asymptotic amplitude short by 4.0e6 / 3.6e6 |
| FAIL | M3 | transition at 48.9 / 40.6 Gpc, not at `r_M` |
| FAIL | M4 | `μ_eff` depends on r alone; I1's `μ(y)` unreachable |
| FAIL | M5 | no symbol gives the flat force law **and** a mass slope ≠ 1 |
| PASS | N1 | Newton recovered with the measured G |
| FAIL | N2 | the correction is power-law (index +1), not exponentially small |
| FAIL | F1 | the a₀-scaled filter suppresses the MOND argument by 1.4e19 (Gaussian) / 4.8e12 (Helmholtz) |
| FAIL | F2 | the sharpening branch saturates it, `y = 6.9e15` |
| FAIL | F3 | no monotone a₀-scale filter has its transition inside 1 Mpc |
| PASS | D1 | the elliptic localisation adds **zero** canonical initial data |
| PASS | D2 | the temporal localisation adds 2, with a ghost pair (P6) |
| PASS | D3 | ellipticity is load-bearing: the count changes at a zero of the symbol |
| FAIL | D4 | the A5 term's khronon kinetic matrix is exactly zero (P7) |
| FAIL | D5 | `N_grav = 3`, not 2 (I3a) |
| FAIL | S1 | the trigger is a wavenumber, not a local acceleration (I4) |
| PASS | S2 | the Solar System passes — vacuously, at 1.7e-6 of the gate |
| PASS | O1 | the momentum scaling **is** changed, `1/r² → 1/r` |
| FAIL | O2 | the amplitude order is not: `O(ε¹)` against the kernel's `O(ε^0.5)` |
| FAIL | V1 | A5 cannot be a protein |
| PASS | V2 | A5 survives as a seasoning |

## Why, in one line

**A nonlocal operator is triggered by a LENGTH; MOND is triggered by an ACCELERATION.** The dictionary
between them is `r_M = |Φ|/a₀` — the *potential*, which I4 forbids by name, which is not a local
invariant, and which is mass-dependent and therefore not an operator at all. It is worth recording that
this near-miss is exact: of the four lengths available, `|Φ|/a₀` is the only one that lands on `r_M`
(1.99 r_M at the solar circle; the agreement is an identity, since `v² = GM/r_M`). With only a₀ and c the
dictionary gives `c²/a₀`, too long by `(c/v_flat)² ≈ 2.6e6`.

## Generic or specific

**Generic to the A5 class**, on two independent legs:
- linearity (M1, M5, O2) — kills the A5-L placement for *every* symbol and *every* length, no
  cosmological number involved;
- the dimensional uniqueness of `c²/a₀` (L1–L4) — kills the a₀-*scaled* version of the A5-F placement for
  every filter shape and both signs.

**Specific to this realisation:** nothing that changes the verdict, and the filter shape was varied to
check that. Both shapes PAPER4 names were run: at ξ = l₀ the Gaussian suppresses the MOND argument by
1.4e19 and the Helmholtz by 4.8e12 (canonical). They differ by seven orders of magnitude and neither is
remotely survivable — which is the point: the deficits are so large that shape choices cannot reach the
threshold.

## What A5 does still buy, and what is not closed

A5 is **not** worthless and should not be struck from §3. Two of its claims are simply true and are now
verified rather than asserted: the elliptic localisation adds **zero** canonical initial data, and the
contrast with the temporal localisation (0 vs 2 modes with a ghost) is a clean quantitative statement of
why P6 is closed and A5 is not. PAPER4's filtered action is A5 used correctly — as a modifier of an
already-MOND nonlinear term, with a length imported from the Solar System. The §3 entry should be
amended to say so: **A5 is admissible as a seasoning and excluded as a protein.**

Stated rather than hidden:
1. A filter whose length is a **field**, `l = l[u]`, is not an operator and is not what A5 licenses — but
   it is also not tested here. The one such length that works is `|Φ|/a₀`, which I4 forbids; any other
   would have to be exhibited.
2. A nonlocal operator acting on something other than the potential (the metric determinant, a matter
   current) is outside this construction.
3. The `N_grav = 3` statement assumes the foliation is carried by a khronon. A **non-dynamical** preferred
   frame gives 2, at the price of general covariance and of matter conservation; that trade is not
   evaluated here.
