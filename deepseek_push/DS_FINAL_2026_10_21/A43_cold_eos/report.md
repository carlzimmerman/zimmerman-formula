# A43 — the cold sector's equation of state from kinetic theory

## Claim

**The cold sector cannot have w ≈ −1/6, and the obstruction is dimensional, not microphysical.**
Deriving the stress tensor from `f(x,v,t)` with the displacement constraint `P = −ρ̄ ξ` — which is
the theory's own `∇·P = ρ − ρ̄` — splits the pressure exactly into a kinetic part `ρσ²` and a tether
part `(n/3)ε_T`. Both are non-negative for a stable tether and a positive-energy polarization field,
so `w ≥ 0`, hence `u = 1+3w ≥ 1`, for **any** collisionless medium of the postulated class: `u < 1`
requires a component with a negative trace. The tether is the only route that gives `w < 0` at all,
and it gives the right sign, the right shape (`0` outside at virial, negative inside when sub-virial)
and the **wrong magnitude by 2.35×10⁴**: `w = (2σ²+Φ)/c²` lies in `[−7.5×10⁻⁶, 0]` for this stack.
The three stated routes fail with numbers. **(i)** Kinetic `w = σ²/c²` needs `σ = 0.408c` = 1.47×10⁴
σ_c (2.16×10⁸ short in w), and anisotropy cannot change the sign: only `σ_r²+2σ_t²` enters the trace.
**(ii)** The counter-stream stress is `ρ(v²+σ²) > 0` for every `(v,σ)` — Cauchy–Schwarz, not a tuning
problem — and even the erroneous `p_z = ρ(σ²−v²)` needs `v = 0.707c`. **(iii)** At half capacity
`u = μ` and `u = 1−μ` coincide at exactly 1/2, half capacity sits at 0.201 Mpc (5.30× inside the
measured crossing at 1.065 Mpc), and neither monotone profile fits the eight bins (χ²/dof 21.0 and
20.4 against 1.09 for the step). The exact missing premise is **a cold-sector binding energy of
0.26–0.33 mc² per particle** — a rest-mass-scale, non-gravitational rigidity. Failing that, the
measurement is not an equation of state: `u = 1+3⟨w⟩` needs the cold *rest* mass in the denominator,
and the same amplitudes then require `f_ret = 2.20 ± 0.34` (MID, 3.6σ above the catchment ceiling
`f_ret ≤ 1`) and `3.09 ± 0.52` (INNER, 4.0σ). `u = 0.47` is a **sourcing fraction** (A18's P-A18), not tension.

Two sub-results are derived, not no-go: **(D1)** `T^ij` is positive semidefinite for `f ≥ 0`, so every
principal pressure is `≥ 0`; **(D2)** `w = 0` for the virialized isothermal sphere, a second route to A29's `u_OUT`.

## Derivation

Units `c = 1` except where written; `G = 6.67430e-11`; `a0 = 9.36e-11 m/s²`; `K = 4πG`. The stack:
318 eRASS1 × KiDS clusters, median `z = 0.23365`, `M200c = 1.483×10¹⁴ M⊙`, `c = 4.5`; eight CFG687
bins, three bands (A29).

**1. The medium.** `N` elements of mass `m`; `n = ∫f d³v`, `ρ = mn`, `ū_i = ⟨v_i⟩`,
`δv_i = v_i − ū_i`, `Σ_ij = ⟨δv_i δv_j⟩`. Vlasov with gravity and a tether force,
`∂_t f + v·∇f + (g + F_T)·∂_v f = 0`, has moments
`∂_t ρ + ∂_i(ρ ū_i) = 0`, `ρ(∂_t + ū·∇)ū_i = −∂_j(ρΣ_ij) + ρ g_i + ρ F_T,i`  (A43.1).

**2. The constraint.** With the Lagrangian map `x = q + ξ(q,t)`, mass conservation `ρ d³x = ρ̄ d³q`
gives

    ρ = ρ̄ / det(∂x/∂q) = ρ̄ (1 − ∇·ξ) + O(ξ²)   ⇒   ∇·P = ρ − ρ̄,   P ≡ −ρ̄ ξ .           (A43.2)

So `P` is not an analogy for the mass displacement — it *is* the mass displacement, at the order at
which the theory writes `∇·P = ρ − ρ̄` (K2, symbolic). This is the whole content of "tethered to the
field": the collective displacement is constrained to be the polarization, and the constraint
reaction is what appears below as `p_T`.

**3. The stress tensor.** From `∫v_iv_j f d³v = n(ū_iū_j + Σ_ij)` (K1, exact), plus the constraint
reaction as an isotropic stress,

    T^00 = ρ + ρσ²/2 + ε_T,   T^0i = ρ ū_i,   T^ij = ρ ū^iū^j + ρ Σ^ij + p_T δ^ij .     (A43.3)

The second moment is exhaustive for a kinetic medium; `p_T` is the only non-kinetic piece a
displacement constraint can add. The measured quantity is the trace,

    T^i_i = ρ(σ_r² + 2σ_t²) + 3p_T ,     p_kin ≡ ρσ² ,                                  (A43.4)

so **anisotropy redistributes pressure but never changes the trace**; rotation is bulk motion
(`ρ ū^iū^j`) and only adds.

**4. The tether pressure.** The tensor virial theorem gives `3p_T = ⟨ρ ξ·∇φ_T⟩`; for
`φ_T = kξ^n/n` this is `n ε_T` exactly (K4, sympy and Monte-Carlo to 1e-9):

    p_T = (n/3) ε_T      ⇒   p_T ≥ 0  for any stable (positive-definite) tether,          (A43.5)

harmonic `n = 2` giving `p_T = (2/3)ε_T`. The tether reduces `w` only through a negative `ε_T`,
i.e. through a binding energy, never through a restoring force.

**5. The constraint fixes `p_T` with no new parameter.** For the tether implied by (A43.2) — the
medium sits at the polarization — radial force balance in a static spherical model is
`0 = −(1/ρ)d(ρσ²)/dr + g + F_T`, `g = −dΦ/dr`; integrating `dp_T/dr = ρF_T`,

    p_T = ρ(σ² + Φ)      ⇒   p_tot = ρσ² + p_T = ρ(2σ² + Φ),                              (A43.6)

    w(r) = [2σ²(r) + Φ(r)] / c² .                                                        (A43.7)

This is the lane's central formula: no tether modulus, no new scale, no fitted number — the
constraint alone fixes the reaction.

**6. What (A43.7) gives.** `Φ < 0`, so `w ∈ [Φ/c², 0]`: **negative only for a sub-virial medium**
(`σ² < −Φ/2`), and zero identically for the virialized isothermal sphere (`σ² = GM/2r = −Φ/2`, so
`2σ²+Φ = 0`; K7, sympy) — a parameter-free derivation of `u = 1`, independent of A29's "single
stream ⇒ zero dispersion" argument. A general virialized profile has volume average
`−⟨σ²⟩/c² = −3.75×10⁻⁶` (`u = 1 − 1.1×10⁻⁵`); a cold free-falling medium gives the same to 10⁻⁵. At
the stack's `r = 0.6 Mpc`, `Φ/c² = −7.496×10⁻⁶`:

    w ∈ [−7.5×10⁻⁶, 0]    vs    measured ⟨w⟩_MID = −0.1761 ± 0.0120 .                    (A43.8)

The sign is right, the shape is right, the amplitude is short by **2.35×10⁴** (K7b).

**7. Why the amplitude is the whole story.** The demanded stress is `|p| = 0.176 ρc² = 2.91×10⁻⁸ Pa`
at 0.6 Mpc (K16), 3.6×10⁴ times the 5 keV ICM pressure there. Every stress the sector can carry is
bounded by `ρ × max(σ_c², |Φ|, a₀²/8πGρ)`. Reservoirs at 0.6 Mpc, as `ρc²` and as the shortfall vs
0.176: kinetic `7.72×10⁻¹⁰` (2.16×10⁸), gravitational `|Φ|/c² = 7.50×10⁻⁶` (2.35×10⁴), the potential
depth `|Φ| ≥ c²/3` that `w = −1/6` needs even at `σ = 0` (4.45×10⁴), and the polarization field
`a₀²/8πG = 3.16×10⁻⁵` (5.58×10³).

The last line is decisive for the tether: the polarization field *is* the tether, and its
stress-energy is `≤ a₀²/8πG = 5.22×10⁻¹² J/m³` (its value at `u ≈ a₀/4`, the maximum of `W`). That
is 3.16×10⁻⁵ of the cold rest energy. **The tether is nearly four orders of magnitude too weak to
hold the medium at a displacement that costs 0.18 ρc².**

## Route (i) — virial, anisotropy, rotation

`w = σ²/c²` (K3). `w = −1/6` would need `σ² = −c²/6 < 0`; even the magnitude needs
`σ = c/√6 = 1.2239×10⁸ m/s = 0.4082c`, **1.469×10⁴ σ_c** (K9). The cold sector is non-relativistic
*by construction* — THEORY §3.3 makes `L_*/L_MOND = σ_c²/c² = 7.7×10⁻¹⁰` — so its kinetic pressure
is `7.7×10⁻¹⁰ ρc²` and the route is short by 2.16×10⁸.

Anisotropy: `w = (σ_r²+2σ_t²)/3c²` (K8). Over `β ∈ [−10, 1]`, `σ_r ∈ [0, 3σ_c]` the minimum is
`w = 0` at `σ = 0`; there is no `(β, σ_r)` with `w < 0`. **No anisotropy is "needed" — none works.**
Rotation adds `ρv_φ²` to the trace, moving `w` the wrong way. The virial theorem makes this general:
for an equilibrium with only kinetic stress, `3⟨p⟩V = 2K ≥ 0`.

## Route (ii) — two counter-streams

Two streams `±v` along `z`, dispersion `σ`:

    T^zz = ρ(v²+σ²),  T^xx = T^yy = ρσ²  ⇒  w = (3σ²+v²)/3c² ≥ 0 .                       (A43.9)

`3σ²+v² = −c²/2` has **no real solution** (K10). The reason is structural: `p_ij = ρ⟨δv_iδv_j⟩` is a
covariance matrix, hence positive semidefinite; negative longitudinal pressure would violate
Cauchy–Schwarz (`⟨(δv)²⟩ = ⟨v²⟩ − ⟨v⟩² ≥ 0`). Even the *erroneous* `p_z = ρ(σ² − v²)` needs
`v = c/√2 = 0.707c` (K11) — 303× the virial velocity, crossing 1 Mpc in 4.6 kyr, 3.0×10³ crossings
in a Hubble time: hot dark matter that free-streams out of the halo. The response is no escape: for
two cold beams the linear Vlasov–Poisson response has `c_eff² = v² > 0` as `k → 0`, and its negative
branch needs `λ > 2πv/ω_J = 1.10×10³ Mpc` — 366× the whole annulus (K12). **The "negative
longitudinal pressure" is neither the stress nor, at cluster scales, the response.** It is a
category error between `T^ij` (what gravitates) and `c_eff²` (what stabilises).

## Route (iii) — saturation at half capacity

With `X ≡ g/a₀`, `μ(X) = X/(1+X)`, so `μ(1) = 1/2` and `1−μ(1) = 1/2`: **at half capacity the two
readings are identical**, so `u = 0.47` cannot select between them (K13). `u = 0.4716` needs
`X = 0.892` (`u = μ`) or `X = 1.121` (`u = 1−μ`) — −11%/+12% off half capacity. The radial test is
decisive (stack NFW for `X(r)`):

| R (Mpc) | 0.181 | 0.263 | 0.383 | 0.556 | 0.809 | 1.176 | 1.711 | 2.488 |
|---|---|---|---|---|---|---|---|---|
| `X = g/a₀` | 1.070 | 0.827 | 0.606 | 0.421 | 0.278 | 0.176 | 0.107 | 0.063 |
| `u = μ` | 0.517 | 0.453 | 0.377 | 0.296 | 0.218 | 0.149 | 0.096 | 0.059 |
| `u = 1−μ` | 0.483 | 0.547 | 0.623 | 0.704 | 0.782 | 0.851 | 0.904 | 0.941 |
| **data (A29)** | **0.294** | **0.373** | **0.333** | **0.417** | **0.412** | **0.532** | **1.088** | **0.939** |

`u = μ` falls where the data are flat and rises where they jump; `u = 1−μ` does the reverse.
χ²/dof: **21.05** (`μ`), **20.42** (`1−μ`), 5.92 (constant), **1.09** (step, dof 6; recomputes A29's
1.455) — Δχ² = 160 and 155 against the step for zero extra parameters (K14). Half capacity sits at
`X = 1`, `r = 0.201 Mpc`, **5.30× inside** the measured `u = 1/2` crossing at 1.065 Mpc (K13); the
data's transition is at `X = 0.137`, i.e. `g = 1.28×10⁻¹¹ m/s² = 0.137 a₀`, a factor 7.3 below
`g = a₀` (K15). Saturation does not put the transition where the data have it.

## Task 3 — the prediction beyond u, and why there is none

**No route survives, and the request for a prediction beyond `u` exposes why.** Any *isotropic* `w`
enters every gravitational channel only through `ρ+3p`. So `w = −1/6` is **exactly degenerate** with
a rescaling `M_c → 2.12 M_c` — same lensing, same dynamics, same redshift-space signal, at every
radius. An isotropic tension therefore makes **no prediction beyond `u`**; it is unfalsifiable in
the only channel that measures it. That is a theorem (the trace identity), and it is the strongest
single argument that `u` is not measuring `w`.

The only *falsifiable* carriers of 0.18 ρc² of negative trace are anisotropic. A string network
(`w = −1/3`) at `f = 3|w| = 0.528`, or a wall network (`w = −2/3`) at `f = 0.264`, gives
`(Φ−Ψ)/Φ ≈ 2f = 1.06` — against the theory's lensing = dynamics gate of **2.63×10⁻⁷** (A12/A3/A32),
a factor **4.0×10⁶** (K19). Dataset: the same 318-cluster stack with eROSITA temperatures versus
KiDS/DES lensing; a 10% mass calibration sees a slip of 1.06 immediately. An isotropic "foam" of
three tensioned families avoids the slip only by fine tuning, does not cluster (`c_s² < 0`,
`ρ+3p = 0`), and its tension is a UV scale, not `a₀`.

**What is decidable** is the identification, and it needs no new data: the EOS reading requires the
cold rest mass in the MID band to be **2.12×** what the `u = 1` reading assigns (2.99× INNER). With
P4 (rest mass = the catchment's cosmic share, `f_ret ≤ 1`), that is `f_ret = 2.20 ± 0.34` — a
**3.6σ** violation in MID, **4.0σ** in INNER (K20). The same amplitudes that give `u = 0.47` exclude
its EOS interpretation. A velocity signature would be decisive too — a two-stream gives a two-peaked
distribution — but the cold medium is dark, so the only tracer is biased galaxies, and a 0.707c
stream is 300× their observed dispersion: not accessible, which is the point.

## Status

- **Task 1 — DERIVED.** `T^ij = ρū^iū^j + ρΣ^ij + p_Tδ^ij`, `p_kin = ρσ²`, `p_T = (n/3)ε_T ≥ 0`; the
  constraint fixes `p_T = ρ(σ²+Φ)`, hence `w = (2σ²+Φ)/c²` (A43.3–A43.7). **(D1)** `T^ij` PSD ⇒
  `w ≥ 0`; **(D2)** `w = 0` for the virialized SIS ⇒ `u = 1` with no parameter.
- **Task 2(i) — NO-GO(exact).** `σ_need = 0.408c = 1.47×10⁴ σ_c`, short by 2.16×10⁸; anisotropy min 0
  over all `β`; rotation adds. **Task 2(ii) — NO-GO(exact).** `w = (3σ²+v²)/3c² ≥ 0` for all `(v,σ)`
  (covariance matrix ⇒ Cauchy–Schwarz); the erroneous formula needs `v = 0.707c`.
- **Task 2(iii) — NO-GO(numerical).** `μ(1) = 1−μ(1) = 1/2`; χ²/dof 21.0/20.4 vs 1.09; half capacity
  5.30× inside the measured crossing; the data's transition is at `0.137 a₀`, not `a₀`.
- **Task 3 — NO-GO + a theorem.** Isotropic `w` is exactly degenerate with `M_c`; the anisotropic
  version gives slip 1.06 vs the 2.63×10⁻⁷ gate (4.0×10⁶). The decidable number is `f_ret`.
- **Task 4 — CLOSED-NO-GO.** The exact missing premise is a cold-sector binding energy
  `ε_T/ρc² = −0.264` (MID) / `−0.333` (INNER), i.e. **0.26–0.33 mc² per particle**: a rest-mass-scale,
  non-gravitational rigidity. Nothing gravitational supplies it (§7); a network does, but fails the
  slip gate. Independently: the EOS reading needs `f_ret = 2.20 ± 0.34 > 1`.

## Checks

`a43_checks.py` — 23 checks, deterministic, stdlib + numpy/scipy/sympy, 2.3 s, no network, reads the
CFG687 npz; exit 0 iff all pass; three mutations each break exactly one check (`MUTATE.md`).

| id | proves | measured |
|---|---|---|
| K0–K3 | npz provenance; `∫v_iv_j f`; `∇·P = ρ−ρ̄`; `p_kin = ρσ²` | exact 0 (sympy) |
| K4, K6 | `3p_T = nε_T`; stable tether ⇒ `w ≥ 0` | 0.6667/1/1.3333; min 1.0e-16 |
| K7, K7b, K7c | SIS ⇒ `w=0`; range `[Φ/c²,0]`; `|Φ| ≥ c²/3` for −1/6 | 0; 2.35e4 short; 4.45e4, 11.8σ |
| K8, K9 | anisotropy min; kinetic `σ_need` and shortfall | 0; 0.4082c = 1.47e4σ_c; 2.16e8 |
| K10–K12 | counter-stream `w ≥ 0`; no real root; response | 0; v=0.707c = 303σ_vir; λ=1.10e3 Mpc |
| K13–K15 | `μ(1)=1−μ(1)=1/2`; crossing radius; four χ²; `X_tr` | 0.201 vs 1.065 Mpc; 21.05/20.42/5.92/1.09; 0.137 |
| K16–K18 | tension vs ICM; field stress; fluid stability | 2.91e-8 Pa (3.64e4×); 3.16e-5; 0.763 Myr |
| K19–K21 | network slip; `f_ret`; four shortfalls | 1.06 (4.0e6×); 2.20±0.34 (3.6σ); 2.2e8/2.3e4/5.6e3/4.4e4 |

(Per-check thresholds and the full labels are in `a43.out`; each row's numbers are the ones quoted
in the text.)

## What this does not do

1. **It does not re-derive `u`.** `u` is taken from A21/A29 at face value (K0 reproduces it from the
   npz), so everything after (A43.6) is conditional on that inversion and on P4. If the band→3D
   mapping moves `u` by its ±0.06 systematic, `f_ret` moves by 12.7% and the 3.6σ becomes 2.7σ —
   still above the ceiling.
2. **The static spherical model is a coarse graining.** (A43.6) assumes a stationary medium whose
   coarse-grained displacement is `P`; in a virialized cluster the medium orbits, and the "tether" is
   the effective reaction holding the coarse-grained displacement, not a physical rope.
3. **`p_T` is a constraint reaction**, so its `T^{00}` partner is not computed: a multiplier's energy
   is fixed by total conservation, and the lane uses only the spatial trace that `u` measures. The
   `ε_T` form (A43.5) is the potential-tether reading, related by the tether stiffness, not equated.
   **Not attempted:** a covariant completion, a tether derivation from the P-sector action, a
   deprojection of `u(r)`, or any cold sector outside {f ≥ 0, stable tether, positive-energy field,
   Newtonian limit}. `a₀²/8πG` is an order-of-magnitude ceiling; `p_ICM` is illustrative.

## Next

1. **Settle the identification, not the mechanism.** The EOS reading is excluded at 3.6σ by
   `f_ret ≤ 1`; the alternative (A18's P-A18: `u` is the sourced share, the rest falls natively) has no
   such problem and predicts the same amplitudes. The separating measurement is a *baryon census* in
   the same annuli (eROSITA gas + BCG stellar + KiDS lensing), not a velocity measurement.
2. **If one insists on a tension**, the only survivor is a pre-stressed elastic medium with
   `p₀ = −0.26ρc²`: a modulus of order `ρc²`, i.e. a relativistic solid, contradicting THEORY §3.3's
   `σ_c = 8.33 km/s` by 10⁹ in `σ²`. **Deprojection** (A29's top item) is now more urgent than any
   microphysics: it moves `u_3D`, hence `w`, and the whole no-go is stated in `w`.

## Falsifier

The lane's claim is that `u < 1` is not tension. Its falsifier is a **direct** measurement of the cold
rest mass in the inner band: if the cold-to-baryon ratio inside `r_sp` is the cosmic 5.364 (within the
8% that `R_req = 5.552 ± 0.427` allows), `w = 0` and `u` is a sourcing fraction; if it is
`11.4 ± 1.7` (2.12×), the EOS reading stands. The observable is the baryon budget at 0.15–1.4 Mpc:
eRASS1 temperatures plus HSC/BCG stellar masses plus the existing KiDS shear, in the same eight bins.
Precision needed: 8% on `R(<r)`; the present stack already has 7.7% in MID — **so the test is already
decided, in favour of `f_ret = 1.035 ± 0.080` at 0.44σ (A18's `R_req/R_cosmic`).**
