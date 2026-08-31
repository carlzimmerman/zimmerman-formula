# PASS_KILL.md — terminal verdict

# ██ KILL ██   (failure class A — structural; branch-wide, not benchmark-specific)

## One-line obstruction
On the FC-KH `α=2β` branch the reduced khronon's **radial gradient speed²** is
```
c²_par(y0; β,λ) = (4 − f''(y0)) (β+λ) / [ f''(y0) (1−β)(2+β+3λ) ] ,
```
and because `4−f''≥0` and `(β+λ)/[(1−β)(2+β+3λ)]>0` for every β>0, λ>0,
```
sign c²_par  =  sign f''(y0)  <  0    for   1 < y0 < y* (≈31–45),
```
a gradient instability **independent of (β,λ)** — no branch point evades it.

## Why the K²(β,λ) backbone cannot save it
- It DOES cure the ghost: `A = (1−β)(2+β+3λ)/(β+λ) > 0` (kinetic term positive, finite). The
  f'' sign flip is correctly NOT a ghost — the MISSION seed is right on that point.
- It does NOT cure the gradient: f'' enters the **spatial lapse-gradient constraint**
  `D_lapse = W0 a0² y0 + W1 kx² + W2 kz² y0`. Its radial (kz²) stiffness is `f''·y0`. When f''<0
  that stiffness is negative, and the backbone only multiplies the whole thing by the positive
  factor `(β+λ)/[(1−β)(2+β+3λ)]` — it rescales magnitude, never sign.

## Why higher spatial derivatives (Hořava L4/L6) cannot save it
The instability is at 2-derivative order and k-independent across the physical sub-horizon band
(a0 ≪ k ≪ M_*). A positive `+B4 k⁴/M_*²` only stabilizes `k ≳ M_*√(|c²_par|/B4) ~ M_*`,
leaving the entire astrophysical band unstable. A positive k⁴ cannot cure a genuine `B2<0`
(MISSION rule).

## Why it is physically realized
Every static source's acceleration a(r) sweeps continuously through a0…(few×10)a0, so the
unstable shell 1<a/a0<y* is a finite radial band at every galaxy's MOND radius (Phase 3).
Growth time in that shell ~5e4 yr (kpc) to ~5e3 yr (100 pc): catastrophic.

## Robustness of the KILL (why it is not a false positive)
1. Two independent reductions (Hermitian Schur vs EL-determinant) agree to ≤1.5e-16.
2. Reproduces BB Eq.(14) exactly in both the pure-quadratic and high-a limits; c_T²=1/(1−β).
3. Transverse mode comes out c²_perp>0 ∀y0 (the expected safe direction) — the code is not
   blindly returning negatives.
4. Deep-MOND (y0<1) and Newtonian (y0>y*) come out c²_par>0 (stable) — the instability is
   confined exactly to the f''<0 window, as it must be.
5. Convention double-locked: `(1−β)` coefficient (⇒c_T²=1/(1−β)), physical f_FC (not the old
   a0²W); both traps identified and avoided (CONVENTION_MAP.md).

## What passes (for the record)
GW170817 (c_T−1~4e-16), solar α1 (=0 on α=2β), BB 1PN floor (β+λ≥2.5e-7 achievable via λ),
G_N/G_C≈1. FC-KH clears the observational pincer that killed the α=½ predecessor; it fails on
internal transition stability instead.

## What would be needed to overturn KILL (none available on this branch)
- A term that makes the radial lapse-constraint stiffness positive where f''<0 WITHOUT a
  preferred-frame/ghost cost and WITHOUT breaking μ_phys=1−e^{−y}. Within the stated action
  (R + θ²,σ² khronometric backbone + f_FC), no such term exists: the radial stiffness IS f''.
- Equivalently, an interpolation with f''≥0 everywhere — impossible for any μ→0 (deep-MOND) and
  μ→1 (Newtonian) with a residual α a² high-a piece: f'' must dip negative in between
  (Flanagan's boundary-condition no-go, here made into a definite local instability).
