# FC-KH static-transition ellipticity — a formal partial result (sympy-verified)

**Status:** SOLID (background PDE). Does NOT establish full dynamical stability.

## Claim
For the FC-KH interpolation μ(y)=1−e^{−y}, y=a/a0, the static spherical MOND operator
∇·[μ(a/a0)∇Φ] never loses ellipticity through the transition a~a0.

## Proof
The radial constitutive map is F(a)=a·μ(a/a0)=a(1−e^{−a/a0}). Ellipticity of the quasilinear
operator requires F'(a)>0. Compute:
  F'(a) = 1 + (y−1)e^{−y}.
Let g(y)=1+(y−1)e^{−y}. Then g(0)=0, g'(y)=(2−y)e^{−y} ⇒ g rises on (0,2), max g(2)=1+e^{−2}≈1.1353,
then decreases to 1 as y→∞. Hence g(y)>0 for all y>0 (zero only at the endpoint y=0). ∎
Verified in sympy (/tmp check, 2026-08-31): F'(a) simplifies to (a+a0 e^{a/a0}−a0)e^{−a/a0}/a0,
identical to 1+(y−1)e^{−y}; g(2)=1+e^{−2}.

## Companion khronometric facts (α=2β branch, sympy-verified)
- c_s²(α=2β) = (β+λ)/[β(2+β+3λ)] > 0 for β,λ>0.
- c_s²≥1 ⟺ λ ≥ β(1+β)/(1−3β) (≈β for β≪1). Benchmark (β,λ)=(1e-15,1e-3): c_s²≈5.0e11 ≫ 1.
- c_T² = 1/(1−β) > 1.

## Scope / what this does NOT prove
This is the BACKGROUND static operator only. It removes ONE failure mode (background loss of
ellipticity). It says nothing about the khronon PERTURBATION spectrum. The terminal gate remains:
  λ_min[ K⁻¹(r) G(r,k) ] > 0  through a(r)/a0 ~ 1
for the FULL β,λ≠0 spherical reduction (the reduced principal symbol A ω² − B∥ k∥² − B⊥ k⊥²).
The transverse direction is already safe (B⊥ ∝ f'/a > 0 always); the open question is B∥ near y=1.
The deep-MOND (Flanagan BM, β=λ=0) and high-a (Minkowski) "healthy ends" are computed in DIFFERENT
limits than the spherical interior, so they do not yet rigorously bracket the interior eigenvalue —
an interior zero-crossing is the genuine open possibility. Overall label: PROMISING / ALIVE.
