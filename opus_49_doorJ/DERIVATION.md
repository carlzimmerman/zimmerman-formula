# OPUS 49d — DOOR J: THE G03 DRAG FROM THE ACTION (DERIVATION, 2026-09-22)

Lane: `opus_49_doorJ/doorJ_drag.py` (run: `python3 doorJ_drag.py | tee
doorJ_drag.out`; sympy log and gates: `doorJ_drag.out`, results JSON:
`doorJ_drag_results.json`). Door: N05's next lane — *"The G03 action that
would DERIVE the drag (κ, ℓ₀) from the action instead of leaving it awaited
– the phantom sector's coupling to baryonic flow is the one open physics
input the theorem's hypothesis names"* (N05_VERDICT.md §4, item 2).

**Verdict in one line: the registered ZNS(κ, ℓ₀) pair is NOT derivable from
the committed action at linear order — the frame-shift coupling yields
either exactly zero (gauge reading, κ = 0 < 2.6e-10 silence floor) or a
survival-excluded, wrong-signed coupling (absolute reading, |κ| ≈ 3.6e-4 ≫
2.6e-9 refined / 2.6e-8 naive). The exact failing terms are on the record
below; everything derived, nothing fitted.**

---

## 0. The door and its premises (registered)

P0 — COMMITTED FRAMEWORK (THE_THEORY.md L5 + Lemma 1; G154; G155; N07):

    S = ∫ Λ⁴ f(K) d⁴x,   f(K) = K − 1/(1+K),   K = −½(dφ)²/Λ⁴
    f′(K) = μ₂(u),  u = |dφ|/Λ²,  μ₂(u) = u(2+u)/(1+u)² = 1−(1+u)⁻²   (L232, n = 2)
    phantom equation (G154 eq. II, sourceless):  d_μ[μ₂ d^μφ] = 0  →  div[μ₂ grad φ] = 0
    background:  φ₀ = (C/√G) ln r,   C = √(G M_b a₀) = v_c²
    L_vac = −Λ⁴ = ρ_Λ c²,  ρ_Λ = 4a₀²/(Gc²)  ⇒  Λ⁴ = 4a₀²/G,  Λ² = 2a₀/√G
    ρ_ph = √(G M_b a₀)/(4πG r²)  (N07 D1, exact)
    a₀ = 9.3619e-11 m/s² (MEASURED), G = 6.674e-11, M_b = 1e10 M_sun.

The field normalization: ∇φ_action = g_ph/√G with the physical phantom
field g_ph = √(G M_b a₀)/r (G155's rescaling); the framework's dimensionless
argument u is invariant under it.  With this the committed identity

    u₀(r) = (C/√G)/(Λ² r) = r_M/(2r),   r_M = √(G M_b/a₀)         [G01c, sympy-exact]

holds with the √G, √(4a₀²/G) and √(G M_b a₀) factors cancelling identically —
the door's algebra never needs an approximate regime.

> **Registration note (task phrasing vs the committed identity).**  The task
> brief writes "Λ⁴ = ρ_ph c²"; the committed statement (Lemma 1 + L5) is
> Λ⁴ = ρ_Λ c² = 4a₀²/G with ρ_Λ = 4a₀²/(Gc²) = 5.845e-27 kg/m³ — a
> constant — while the framework's ρ_ph(r) = √(GM_ba₀)/(4πGr²) is the
> Gauss-map mass density (G154 V2/V3), r-dependent, not a constant.  All
> algebra below uses the committed constant identity Λ⁴ = 4a₀²/G; the
> numerical ratio of the two readings is ρ_ph(r)c²/Λ⁴ =
> r_M c²/(16π a₀ r²) ≈ 1.6e5 at r = r_M (the harmonic density is 1.6e5×
> the Λ⁴-energy-density equivalent there), and the mapping would change
> no conclusion (κ scales only with Λ² = 2a₀/√G, common to both
> readings).

P1 — MECHANISM PREMISE (the OPEN input, registered as the door's choice):
baryonic flow enters as a frame shift of the kinetic argument,

    K = −½(dφ − w)²/Λ⁴,   w = (a₀/c) v_b,

the flow velocity mapped to a field gradient through the only committed
rate scale a₀/c = H_Λ/Z (the de Sitter–Unruh footing).  In u-units:

    u_eff = |u₀ r̂ − (v/2c) v̂|,   δu = −(v/2c) cos θ          [G03, exact]

— the 1/2 is Λ² = 2a₀/√G, committed, not fitted.  Two readings:

  P1a GAUGE: w is the Galilean frame shift (a reparameterization).  The
          committed static phantom equation div[μ₂(|∇φ|/Λ²)∇φ] = 0 is form-
          invariant under x → x − vt (u and ∇φ translate; the conserved
          flux F = r²μ₂u₀·Λ²u₀ = 2Λ²(r_M/2)² is r-independent, [G02a,
          G04, sympy-exact]), so φ₀(x − vt) solves it at every instant:
          **the first-order response is identically zero; κ = 0 exactly.**
  P1b ABSOLUTE: w is an absolute velocity against the phantom rest frame
          (breaks Galilean covariance — the only reading that can produce
          a drag).  The full linear response is computed exactly below.

## 1. The action algebra (sympy, all printed in doorJ_drag.out)

Variation of S with the shifted derivative gives

    EOM:  d_μ[ f′(K)(d^μφ − w^μ) ] = 0
    T_mn = f′(K) X_m X_n + g_mn Λ⁴ f(K),   X = dφ − w

(sympy: f′(K) = 1 + (1+K)⁻²).  Linearizing about (φ₀, w = 0) with
φ = φ₀ + δφ, the dipolar ansatz δφ = (v/2c) Λ² h(r) cos θ projects the 3D
operator onto the radial ODE (verified in G05a by finite-difference
substitution of two independent probes on a cylindrical grid — the ODE is
*derived*, not assumed; the source projection matches symbolically):

    (1/r²) d/dr [ r² E_∥(r) h′ ] − (2/r²) E_⊥(r) h = S_r(r)
    E_∥  = μ₂(u₀) + μ₂′(u₀) u₀          (anisotropic "dielectric": μ₂′u₀ ≠ 0)
    E_⊥  = μ₂(u₀)
    S_r  = d/dr[μ₂′u₀] + (1/r²) d/dr[ r² μ₂′u₀ ]

with u₀ = r_M/(2r) and the exact μ₂, μ₂′ = 2(1+u₀)⁻³ — no approximation
anywhere.  The exact coefficient functions as sympy prints them:

    E_∥ = (G^{3/2}M_b^{3/2} + 16√G√M_b a₀ r² + 6 G M_b √a₀ r) /
          (G^{3/2}M_b^{3/2} + 12√G√M_b a₀ r² + 6 G M_b √a₀ r + 8 a₀^{3/2} r³)
    E_⊥ = √G√M_b (√G√M_b + 4√a₀ r) / (√G√M_b + 2√a₀ r)²
    S_r = 48 G M_b a₀ r / (8 G^{3/2}M_b^{3/2}√a₀ r + 32√G√M_b a₀^{3/2} r³
           + G²M_b² + 24 G M_b a₀ r² + 16 a₀² r⁴)  > 0  for all r

**Source structure [G05b]**: lim_{r→∞} r²S_r = 0 exactly (the deep
~1/r² pieces cancel), lim r³S_r = 3GM_b/a₀ = 3r_M²; and S_r → 0 as r → 0
(μ₂′ → 0).  The linear response is therefore generated ONLY at u₀ = O(1),
i.e. in the transition zone r ~ r_M — the deep phantom and the Newtonian
core are both inert at linear order.

## 2. The wake (P1b) — numbers from the committed constants

BVP on [0.1, 6] kpc (the registered MW EFE cap ~ 6 kpc, G003 V5), exact
coefficients, boundary conditions h(r_min) = r_min·h′(r_min) (regular core)
and h(r_cap) = 0 (the phantom is cut at the cap); solve_bvp, tol 1e-9,
N = 8000.  Result (all in `doorJ_drag.out`):

    A = h′(r_min) = −0.6332   (near-field polyfit −0.6329: consistent)
    h < 0 over the whole domain; max |h| at r = 2.22 kpc (~ r_M/1.7, u₀ ≈ 0.87)
    r_cap-sensitivity: A = −0.633 (6 kpc), −0.920 (12 kpc), −1.481 (24 kpc)
        — sign stable, magnitude IR-dominated (the ln-field's memory):
        honest range |A| ∈ [0.63, 1.48]; every conclusion below is
        sign- and magnitude-robust to the cap placement.

Physics of the sign: S_r > 0 with the E∥/E⊥ structure gives A < 0, so the
wake potential δφ = (v/2c)Λ²h(r)cosθ is negative on the downstream side and
the induced field at the baryon is **along** the flow:

    g_wake(0) = −√G ∇(δφ)(0) = −(v/c) a₀ A v̂ = +|A| (v/c) a₀ v̂      (tailwind)

|g_wake(0)| = (v/c) a₀ |A| — the √G·Λ²/2 = a₀ cancellation is exact
[G01d].  Numerically (A = −0.633):

    |a_wake| = 1.977e-19 · v  m/s²          (coefficient per m/s)
    |a_wake|(v_c)    = 2.088e-14 m/s² = 2.23e-4 · a₀      [G06: ≪ a₀/2, cap PASS]
    |a_wake|(220 km/s)= 4.350e-14 m/s² = 4.65e-4 · a₀

## 3. κ in the registered parametrization a_drag = κ √(a₀/ℓ₀) v

    κ = a₀ A / (c √(a₀/ℓ₀))   ⇒   κ(ℓ₀ = 10 kpc) = −3.590e-4
                               κ(ℓ₀ = r_M)     = −2.230e-4 = v_c A/c

**G07 (the derivability kill)**: |κ| = 3.59e-4 exceeds the refined band
2.6e-9 by 1.4e5× and the naive band 2.6e-8 by 1.4e4×, in either sign:
  • as a drag it would drain MW rotation support in ~160 Gyr at 220 km/s
    (observed: ≳ 10 Gyr — excluded);
  • as the tailwind the BVP actually returns, it would spin the disk up
    ~8.6% per Hubble time at the 6-kpc cap (2–4× more at 12–24 kpc caps) —
    comparably excluded by the same survival logic.
The absolute-reading premise P1b is EXCLUDED by the registered survival
gates (G13/G14/N06), with the derived number 1e4–1e5× above them.

Dimensional honesty check: the drag force density in the task's form,
f_drag = −κ ρ_ph v/ℓ₀, maps to the baryon fluid via f = ρ_b·a_wake; with
κ_P1b-copy = κ·(ρ_b-accounting) the same number enters; the wake
acceleration is 2.2e3× below the a₀/2 cap, so the cap is NOT the binding
constraint — the survival band is (this is the door's central quantitative
surprise: the action's own linear coupling, when forced to be absolute, is
far *too strong* for the registered silence, not too weak).

## 4. The exact failing terms (the deliverable)

1. **P1a**: the first-order response of div[μ₂ grad φ] = 0 to *uniform*
   steady baryonic flow is IDENTICALLY ZERO (Galilean invariance of the
   committed static equation — [G04]); κ_P1a = 0 exactly, below the
   silence floor 2.6e-10: the frame shift alone cannot be the N3 drag.
2. **P1b**: the linear response is a transition-localized dipole whose net
   *internal* stress integral vanishes by parity ([G08]: ∫cosθ dΩ = 0 etc.);
   the only linear-in-v momentum channel is the baryon-wake self-force,
   whose committed magnitude (|κ| ≈ 3.6e-4, ℓ₀ = 10 kpc) is 1.4e5× above
   the registered refined band AND has the wrong sign to be a dissipative
   drag (tailwind, not drag).
3. **Structural**: the net force probes the IR: the ln-field's momentum is
   IR-divergent (flux ∝ ε·R at infinity), the EFE cap is the physical
   regulator, and the derived amplitude is cap-dominated (|A| ∈
   [0.63, 1.48]) — a second, structural reason there is no *unique* κ from
   the committed constants without pinning the cap (which the framework
   does — G003 V5 ~6 kpc — and even then the number is far outside the band).
4. **Kinematics**: v_c/c = 3.52e-4 ≪ c_s/c ∈ [1/√2, 1) (L5) — no radiative
   (Cherenkov) channel at linear order [G09]; and G031's dusts couple only
   through the shared Newtonian potential — no J·j_b interaction exists in
   the committed action to generate a dissipative drag at any strength.

**Consequence**: any nonzero linear drag at the registered strength
requires physics outside L5/G031 — a dissipative coupling (phantom
viscosity, or a baryon–shift-current interaction J·j_b absent from G031).
The (κ, ℓ₀) pair remains measurement-awaited, exactly as N05 registered it,
now with the negative proof on the record: this door closes with the
exact obstruction, not with a number from a fit.

## 5. The gates (15/15, `doorJ_drag.out`)

| Gate | Content | Measured | Status |
|---|---|---|---|
| G01a | μ₂ = u(2+u)/(1+u)² = 1−(1+u)⁻² (sympy) | exact identity | PASS |
| G01b | Λ⁴ = ρ_Λc² = 4a₀²/G (sympy identity) | 5.2529e-10 kg/(m s²) | PASS |
| G01c | u₀ = (C/√G)/(Λ²r) = r_M/2r (sympy exact) | exact | PASS |
| G01d | (C/√G)/Λ² = r_M/2 (√G·Λ²/2 = a₀ chain) | exact | PASS |
| G02a | deep branch: d[r²μ₂u₀Λ²]/dr = 0 (sympy) | F = √G·M_b const | PASS |
| G03 | δu = −(v/2c) cos θ (committed 1/2) | exact | PASS |
| G04 | P1a: translated configuration solves the static equation | κ = 0 exact | PASS |
| G05a | dipolar ODE = 3D operator projection (2 probes, FD) | max rel 1.49e-4 / 7.40e-5 | PASS |
| G05b | source transition-localized (sympy limits) | lim r²S_r = 0, tail 3r_M²/r³ | PASS |
| G05c | BVP converged; A same sign all caps, |A| ≥ 0.5 | A = −0.633/−0.920/−1.481 | PASS |
| G06 | wake acceleration vs a₀/2 cap | 2.23e-4·a₀ ≪ a₀/2 | PASS |
| G07 | |κ| vs bands (derivability kill) | 3.59e-4 ≫ 2.6e-9 / 2.6e-8 | PASS |
| G08 | net internal-stress integrals vanish (parity) | ≤ 1.1e-16 | PASS |
| G09 | no Cherenkov channel | v_c/c = 3.5e-4 ≪ c_s/c | PASS |
| G10 | honesty gate (verdict + failing terms in-file) | tokens present | PASS |

Reproduce: `python3 opus_49_doorJ/doorJ_drag.py | tee
opus_49_doorJ/doorJ_drag.out` (sympy + scipy ≥ 1.14).  Results JSON:
`opus_49_doorJ/doorJ_drag_results.json`.

— the G03 door, executed. The drag is not derivable from the committed
action at linear order: exactly zero (gauge) or survival-excluded and
wrong-signed (absolute). The negative proof is the deliverable.