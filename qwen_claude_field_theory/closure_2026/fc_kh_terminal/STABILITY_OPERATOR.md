# STABILITY_OPERATOR.md — the reduced quadratic scalar action (Phases 4–5)

Source: `decisive_reduction.py` (+ `.out`, `decisive_symbols.pkl`); numeric map
`phase5_numeric_dispersion.py` (+ `.out`). Two INDEPENDENT routes agree to 1e-16.

## Setup — local frozen MOND background, unitary gauge
Static spherical ⇒ K̄_ij=0 ⇒ β,λ do not touch the background (SHARPENED TARGET, verified).
Freeze the background acceleration at a point: `ā_i = ḡ ẑ`, `ḡ = a0 y0`, `ln N̄ = ḡ z`,
flat `γ̄_ij=δ_ij`. This is the principal-symbol / geometric-optics limit valid for
`k ≫ 1/L_bg` (short-wavelength vs background variation). Scalar perturbations (residual
spatial diff fixes E=0):
```
N = e^{φ},   N_i = ∂_i B,   γ_ij = e^{2ψ} δ_ij,   a_i = ḡ ẑ + ∂_i φ  (a_i=∂_i ln N, exact)
```
Fields: φ (lapse, non-dynamical), B (shift, non-dynamical), ψ (the propagating khronon).
Count: 3 scalars − 2 constraints (φ,B) = **1 physical scalar DOF** (+ 2 tensor, separate).

## Quadratic action
```
L2 = N√γ[ (1−β)K_ijK^ij − (1+λ)K² + ³R + f_FC(a) ] to O(perturbation²)
```
with K_ij^{(1)} = ψ̇ δ_ij − ∂_i∂_j B, the ³R measure e^{φ+3ψ}, and the acceleration expansion
a² = e^{−2ψ}[(ḡ+∂_zφ)²+(∂_xφ)²], potential entered as (W0,W1,W2)=(F,F′,F″)(y0). Machinery
cross-validated against BB Eq.(14) in the Minkowski limit (`wf_flat_validation.py`, exact match).

## Reduction (Hermitian Schur complement)
Fourier `k=(kx,0,kz)`, kz∥ā. Build the Hermitian quadratic form H(ω,kx,kz) (period-average
method ⇒ eigenvalue signs are physical; Hermiticity residual = 0). The (φ,B) block is
**ω-free** (both non-dynamical). Integrate them out:
```
G(ω,k) = H_ψψ − H_ψc H_cc^{-1} H_cψ   (reduced inverse propagator for ψ)
       = A ω² − V(kx,kz),      dispersion  ω² = V/A.
```

### Kinetic coefficient (the K² backbone; f'' does NOT enter here)
```
A = (1−β)(2+β+3λ)/(β+λ)   >  0    for all β>0, λ>0.
```
Confirms MISSION seed `K_scalar ∝ (2+β+3λ)/(β+λ) > 0`: **no ghost**; the f'' sign change is
NOT a ghost. A is k-independent (verified).

### The lapse constraint carries f'' — the crux
The (φ,B) determinant factorizes as
```
det H_cc ∝ (β+λ)(kx²+kz²)² · D_lapse,   D_lapse = W0 a0² y0 + W1 kx² + W2 kz² y0
```
`D_lapse` is the spatial lapse-gradient (modified-Poisson) operator. Its kz² (radial)
stiffness is `W2 y0 = f''·y0`; its kx² (transverse) stiffness is `W1 = f'·(a0/a) ...`.
This is exactly the MISSION seed statement "f''(a) enters the SPATIAL lapse-gradient
constraint." D_lapse appears in the DENOMINATOR of V ⇒ the reduced propagator is nonlocal;
the dispersion is `ω² = V(k)/A` with V rational in k, crossover at `k ≈ ḡ = a0 y0`
(**super-horizon**, since a0 ≈ 1/Hubble-length in geometrized units).

### Physical (sub-horizon, k≫a0) gradient speeds — the decisive numbers
Taking `k → ∞` (deep sub-horizon = the entire astrophysical band a0≪k≪M_*):
```
c²_par,UV  = (4 − W2)(β+λ) / [ W2 (1−β)(2+β+3λ) ]        (kz ∥ ā ; radial)
c²_perp,UV = (4 y0 − W1)(β+λ) / [ W1 (1−β)(2+β+3λ) ]      (kx ⟂ ā ; tangential)
```
- **Transverse:** `4y0−W1 = 2y0(2−α)(1−e^{−y0}) > 0` and `W1>0` ⇒ **c²_perp>0 ∀y0**. Safe,
  exactly as predicted (transverse Hessian f'/a>0 never flips).
- **Radial:** `4−W2 > 0` always (W2≤4) and the factor `(β+λ)/[(1−β)(2+β+3λ)] > 0` for all
  β>0,λ>0. Therefore
  ```
  sign(c²_par,UV) = sign(W2) = sign(f'')      — INDEPENDENT of (β,λ).
  ```
  `f''(y) = 2α + 2(2−α)(1−y)e^{−y} < 0` for `1 < y < y*` (`y*≈31–45`, the MISSION 1≲y≲38 window).
  ⇒ **c²_par,UV < 0 through the entire transition window, and NO β,λ on the branch can fix it.**

### Consistency checks passed (decisive_reduction.out)
- Pure-quadratic f=αa² ⇒ `c²_par,UV = c²_perp,UV = BB Eq.(14)`, y0-independent, m²=0. ✓
- High-a (y0→∞, W2→2α>0): c²_par,UV → (β+λ)/[β(2+β+3λ)] = BB c_s² (huge, ~5e11 at P1 — the
  known α→0 strong-coupling; positive/stable-but-superluminal). ✓
- Deep-MOND (y0<1, W2>0): c²_par,UV>0, small. ✓
- Route II (EL-determinant −D0/D1, independent) reproduces ω²(k) to 1e-16 at all sampled k. ✓

## Hyperbolicity / where the instability lives
`ω² = c²_par,UV k²` with `c²_par,UV<0` and k-independent across a0≪k≪M_* (converged by k~100 a0,
verified over 4 decades). So the radial khronon mode has `ω² < 0` (imaginary frequency,
exponential growth) for **all** sub-horizon k in the f''<0 shell — a genuine gradient
instability, not a bounded finite-k band. The higher-spatial-derivative L4/L6 (Hořava, scale
M_*≳eV) add `+B4 k⁴/M_*²`, which can only stabilize `k ≳ k_c ~ M_*√(|c²_par|/B4) ~ M_*`; the
unstable band `a0 ≲ k ≲ k_c` still spans essentially all physical scales. Consistent with the
MISSION rule: a positive k⁴ term cannot cure a genuine `B2<0`.
