# opus_49_doorH — the EXACT second-variation operator (I14 SOURCE OPERATOR)

**Question.** The I14 t-lattice trichotomy (`fable_independent_2026/lean_2026/I14_phantom_vacuum_wall.lean`)
certifies: for the defined form `A = sum (u_{n+1} − u_n − u_n/2)^2`, `E = A − κ² U + μ² q U`,
the uniform-over-boxes threshold is `κ² ≤ 1/4` (unconfined), with `κ² = 1/4` exactly marginal.
The framework-identification audited in `real_research/reviews/spectral_spine_closure_2026_09_22/i14/SOURCE_BRIDGE.md`
was found INCOMPLETE: (i) the direct radial variation of G155's kinetic action about the committed
background `φ0 = C ln r` yields a deep log-coordinate weight that is CONSTANT, not the `e^t` of I14's
`sqrt(r)` dressing; (ii) the action supplies no independently derived `−κ²/r²` term; (iii) the log
background is not an exact solution of the full interpolant. This door COMPLETES that derivation:
the exact second-variation operator of the framework's actual action about its actual background,
for the FULL interpolant `μ₂(u) = u(2+u)/(1+u)²` (no deep-corner truncation), with every coefficient,
the exact algebraic condition for realization of the Hardy-marginal potential `1/4`, the stability
boundary of the real operator, and the verdict on the `κ = 1/2` spectral-rigidity route.

All algebra below is the checked output of `sympy_derivation.py` (log: `sympy_derivation.out`,
`27/27` checks PASS, JSON: `results.json`). Notation: SOURCE_BRIDGE's `x = sqrt(K)` is G155's `u`
relabelled (u = x there); every formula below is the same rational function of the argument.

---

## 1. Conventions and the interpolant identity

G155 (`deepseek_push/G155_sourced_eq.py:100-102`) computes `df/dK` by dividing `df/du` by `2u`,
i.e. its kinetic convention is

    K = (dφ)²/Λ⁴ = u² ,        u := |∇φ|/Λ² ,        f(u) = u² − 2 ln(1+u) − 2/(1+u) + 1 ,

    f′(K) = μ₂(u) = u(2+u)/(1+u)²        (C0: checked, df/dK − μ₂ = 0)

(C1b: with the alternative convention K = u²/2 one gets f′ = 2μ₂; the operator coefficients
`a_r = μ₂ + u μ₂′`, `μ₂` are unchanged — the physical content is convention-invariant.)

Static constrained functional (fixed spatial background, gradient part only), 3D:

    F[φ] = ∫ d³x Λ⁴ f(K) .

## 2. The exact second variation at φ0 = C ln r (full interpolant)

Put `φ = φ0 + εη`, `u0(r) = φ0′/Λ² = C/(Λ² r) =: b/r` (b := C/Λ²). With
`K = u²`, `K(ε) = u0² + ε·2u0η_r/Λ² + ε²η_r²/Λ⁴` (η_r := ∂_r η). Expanding `f` to O(ε²):

    dK₁ = 2 u0 η_r / Λ² ,   dK₂ = η_r² / Λ⁴ ,
    ε²-coefficient of f(K(ε)) = f′(K0)·dK₂ + (1/2) f″(K0)·dK₁²
        = μ₂(u0) η_r²/Λ⁴ + (1/2)·(μ₂′(u0)/(2u0))·(4 u0² η_r²/Λ⁴)
        = [ μ₂(u0) + u0 μ₂′(u0) ] η_r² / Λ⁴          (C2: direct-series check = 0)

Because `(∇φ0·∇η)² = φ0′² η_r²` the second Hessian term couples ONLY to the radial component.
The exact Hessian quadratic form (coefficient of ε², i.e. half the "second variation") is

    Q[η] = (1/2) ∫ d³x [ f′(K0)|∇η|² + 2K0 f″(K0) η_r² ]        (2K0 f″(K0) = u0 μ₂′(u0))

**Radial mode operator (standard radial decomposition).** With `η = Σ u_L(r) Y_Lm(Ω)` the mode
decouples (a_r, μ₂ depend only on r):

    Q_L[u_L] = (1/2) ∫ 4π r² [ a_r(u0) u_L′² + μ₂(u0) L(L+1) u_L²/r² ] dr ,
    O_L = −(1/r²) d/dr [ r² a_r(u0(r)) d/dr ] + μ₂(u0(r)) L(L+1)/r² ,
    a_r(u) = μ₂(u) + u μ₂′(u) = u(u²+3u+4)/(1+u)³ = 1 + (u−1)/(1+u)³ .      (C1)

EVERY coefficient: radial weight `a_r` (kinetic + the 2K0 f″(K0) dressing piece), angular
(centripetal) weight `μ₂(u0)` — positive, a REPULSIVE barrier. I14's lattice form has no L(L+1)
term: **the I14 comparison is the L = 0 sector only**,

    O_0 = −(1/r²) d/dr [ r² a_r(b/r) d/dr ]      on L²(4π r² dr),  u0(r) = b/r .

## 3. Log-coordinate reduction: weight, shift, potential (exact)

r = e^t.  Q/(2π) = ∫ w(t) η_t² dt with

    w(t) = r a_r(b/r) = e^t a_r(b e^{−t})  (as function of u = b e^{−t}:  w = (b/u)·a_r(u)).

Dress `v = √w η`; the canonical (Gauss-factorized) form is

    Q/(2π) = ∫ (v_t − s v)² dt = ∫ ( v_t² + V v² ) dt ,
    s  = (1/2) d ln w/d ln r = (1/2)(1 − u a_r′/a_r)
       = u(u²+4u+9) / [2(1+u)(u²+3u+4)] ,             s(0) = 0 , s(∞) = 1/2 ,   (C5)
    V  = s² + ds/dt = s² − u ds/du                            (since d/dt = −u d/du)
       = u(u⁵+8u⁴+42u³+64u²+17u−72) / [4(1+u)²(u²+3u+4)²] ,   V(0) = 0 , V(∞) = 1/4 .  (C6)

So the canonical radial operator is `−d²/dt² + V(u(t))` with a RUNNING potential — never the
constant `1/4 − κ²` of I14. Exact facts about V (C7, C8):

    V − 1/4 = (3u⁴ − 16u² − 32u − 4) / [(1+u)²(u²+3u+4)²]
    quartic' = 4(u−2)(3u²+6u+4) → sole positive stationarity at u = 2, value −84
    → exactly ONE positive crossing u* = 3.0051:  V < 1/4 on (0,u*),  V > 1/4 on (u*,∞),
      V − 1/4 ~ 3/u² → 0⁺  (decay from ABOVE);
    min V = −0.1089 at u = 0.252  (negative dip, deep corner);
    V = 0 at u = 0.764 ;  max V = 0.2691 at u = 5.50 .

The audit's claim "V tends to 1/4" is therefore a limit from above, and the constant-1/4
reading is not even a bound. The negative dip is a dressing/norm artifact (the original form
is an integral of positive weighted squares — no physical negative mode; the audit's caution).

## 4. The exact algebraic condition: when is the Hardy-marginal 1/4 realized?

**Theorem (realization).** The canonical operator equals the I14-Hardy-marginal operator
(potential identically 1/4) iff the log weight satisfies the Riccati equation

    V ≡ 1/4   ⟺   s′ = 1/4 − s²   ⟺   2w w″ − (w′)² = w² ,        s = (1/2)(ln w)′ ,   (C9)

whose general solution is  s = (1/2) tanh((t−c)/2)  plus the fixed points  s = ±1/2, i.e.

    w ∈ { C₁ e^t ,  C₂ e^{−t} ,  C₃ cosh²((t−c)/2) }        (each verified: ODE residual 0).

Consequences for the framework's profiles:

1. **Log family (committed):** `w(t) = e^t a_r(b e^{−t})` fails the Riccati identically — the
   exact defect is
       2ww″ − w′² − w² = 4b²·(3u⁴−16u²−32u−4)/(1+u)⁸ ≠ 0        (C10, symbolic)
   — the very quartic of §3. V equals 1/4 at exactly ONE isolated radius per member
   (u = u* ≈ 3.005, i.e. r = b/u*), never identically. (C1/C4: `a_r` runs 0 → 1⁺ → 1; the
   weight is `w ≈ 4b` deep, `w ≈ e^t` only as r → 0.)
2. **Exact sourceless background of the full interpolant.** `div[μ₂∇φ] = 0` radial is
   `r²μ₂(u)φ′ = J` (flux conservation) ⟺ `h(u0) = c/r²` with
   `h(u) = u μ₂(u) = u²(2+u)/(1+u)²`, h′ = a_r > 0 (C11): the ACTUAL background family is
   `u0(r) = h⁻¹(c/r²)`; the log profile is its deep-corner asymptotic only. Its weight has
   (C12, N2):
       deep (r→∞):   u0 ~ √(c/2)/r   ⟹  w → 4√(c/2)  const ;
       near (r→0):   u0 ~ c/r²       ⟹  w → e^t .
3. **No realization.** The Riccati solution families grow like e^t, e^{−t}, e^{2t}/4 at t→∞,
   while every member of both framework families has w(t) → const > 0 as t→∞; conversely the
   only matching asymptote (near-corner e^t) is attained only in the strict limit r → 0 (u→∞)
   (C13). Hence **no framework-compatible profile realizes V ≡ 1/4 at any finite radius**; the
   I14 Hardy-marginal operator appears only at the ideal inner boundary, where the committed
   background is off-shell (below) and the physical halo is EFE-capped (`r_break = 0.62 r_M`,
   u(r_break) ~ 10⁻¹⁹ ≪ 1 — deeply in the V ≈ 0 corner).

## 5. Off-shellness of the committed background (SOURCE_BRIDGE (iii), exact)

    J(r) = r² μ₂(u) φ0′ = C b (u+2)/(1+u)² ,   dJ/dr = C(μ₂ − u μ₂′) = C u²(u+3)/(1+u)³ > 0
                                                                                    (C14)
The flux is non-conserved for every u > 0; the log profile solves `div[μ₂∇φ] = 0` only in the
deep-corner limit u → 0. The first variation of F at φ0 = C ln r is
`δF = −Λ⁴∫d³x η div[μ₂∇φ0] ≠ 0` (C15): the "Hessian about the committed background" is the
second derivative at a NON-critical point of the full interpolant. The exact fluctuation
operator must be taken about the C11 family; both share the weight form w = r a_r(u0(r)), so
all conclusions above carry over.

## 6. The stability boundary of the real operator

Physical form (L = 0): `E[η] = (1/2)∫4π r² [ a_r(u0) η′² − κ² η² ] dr` (I14-type reading:
κ²U against the L²(r²dr) mode norm). Then (C16, C17, N3):

- **Uniform over all boxes: κ*² = 0.** For any κ² > 0 the far-field slab on [R, 2R] gives
  E ≈ −κ²·4π·(7/3)R³ → −∞; at κ² = 0 the form is a positive weighted gradient square, nonneg
  with no uniform gap (Rayleigh quotients → 0: Q/U = 4.9e−3, 1.1e−4, 4e−6 for R = 5, 20, 80).
- **Finite (capped) box:** bottom λ₁(R) > 0, e.g. exact-Galerkin on L²(r²dr):
  bottoms(κ²=0) = 18165, 7.14, 0.0009 for R = 1, 10, 100 → 0⁺; bottoms(κ²=1/4) → −0.2491:
  the I14 marginal couple κ² = 1/4 sits DEEPLY in the unstable region of the real operator.
  This is exactly I14's own finite-vs-uniform distinction (I14:499-533), with the uniform
  threshold shifted 1/4 → **0**.

The real operator is marginal in the I14 sense at κ_real = 0 — not 1/4, not 1/2.

## 7. Deep corner exactly; what the full case adds

    μ₂ = 2u − 3u² + 4u³ − 5u⁴ + … ;   a_r = 4u − 9u² + 16u³ + … ;
    f(K) = (4√2/3) K^{3/2} + … (MOND kinetic);   s = (9/8)u + … ;   V = −(9/8)u + …   (C18)

Deep-corner leading operator about the on-shell corner: `w = 4b + O(u²)`,
`Q = 8πb ∫ η_t² dt` — the FREE form (V = 0, s = 0); the I14 1/4 is absent to all orders there.
The full case adds (C19): subleading u-corrections (w = 4b(1 − (9/4)u + …)), the negative
potential dip, the single exact V = 1/4 crossing at u* ≈ 3.005, the overshoot to 0.269 and
decay from above, and the I14-absent centripetal barrier μ₂(u0)L(L+1)/r².

## 8. I14 dictionary and verdict

I14's `A = (3/2)D + (1/4)U` is the unit-spacing discretization of the canonical weight operator
(w = e^t, s = 1/2): `1/4 = s²` (the Hardy shift), `3/2` is the forward-difference artifact
(continuum coefficient 1), and its marginality lives at `1/4 − κ² = 0`. The framework's real
shift s(u) runs 0 → 1/2 and hits neither endpoint at finite radius on any solution.

**Verdict.** I14's κ = 1/2 marginality is NOT realized by the framework's actual second
variation. The exact Hessian of L = Λ⁴f(K) at φ0 = C ln r (full interpolant) is a positive
weighted gradient form whose canonical L = 0 form is −d²/dt² + V(u(t)) with running V
(V(0) = 0, V(∞) = 1/4, dip −0.109, overshoot 0.269); V ≡ 1/4 requires the Riccati
2ww″ − w′² = w², i.e. w = C e^{±t} or C cosh²((t−c)/2) — realized by neither the log family
(symbolic defect ≠ 0) nor the exact sourceless family u0 = h⁻¹(c/r²) (asymptotic crossing) at
any finite radius, only at the ideal r → 0 boundary (off-shell, EFE-capped). The real
operator's uniform stability boundary is κ² = 0, not 1/4; κ² = 1/4 is deep in its unstable
region (bottom → −1/4). **The spectral-rigidity route to κ = 1/2 does not survive.** I14 is a
model theorem — an exact certificate for a defined t-lattice Dirichlet form, exactly as its own
docstring disclaims any physical identification (I14:30-35) — with the framework connexion dead.

## Self-review / verification record

Every claim above is machine-checked in `sympy_derivation.py` (27/27 PASS):
C0-C2 interpolant/Hessian coefficients (incl. direct ε²-series expansion of the full f),
C3 operator decomposition, C4-C8 weight/shift/potential + exact V−1/4 factorization and
extrema, C9-C13 Riccati condition and non-realization (log family symbolic defect; exact
family asymptotics), C14-C15 flux non-conservation/off-shellness, C16-C17 stability boundary,
C18-C19 deep corner and full-case corrections, N1 dressing identity (integral check, rel. dev
~7e-10), N2 exact-family weight asymptotics, N3 exact-Galerkin stability spectrum and slab
Rayleigh quotients. No commit exists for the prior doorway content; this folder is committed
as `opus_49d doorH I14 SOURCE OPERATOR`.