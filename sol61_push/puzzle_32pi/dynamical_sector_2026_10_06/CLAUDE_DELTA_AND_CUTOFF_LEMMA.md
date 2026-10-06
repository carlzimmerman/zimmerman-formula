# Concurrent kernel proposals: symmetry fixes one choice, self-reflection fixes no universal coefficient

Read-only inspected concurrent commits `52c96a80f` (p54) and `220bff33c` (p55), specifically sonnet55_push/puzzle_32pi/p54_what_fixes_alpha_yt.py and p55_turnoff_principles.py. This is a mathematical reading and the independent uniform argument below, not a new authenticated rerun of their scripts or a new astronomical data analysis.

## Exchange symmetry and source normalization

Under the coincident nonzero-vacuum consistency assumptions of p53, f′(1)=(1−α)/(1+α). Imposing exact sector exchange symmetry gives f′(1)=0 and hence α=1. This removes that coupling freedom within the exchange-symmetric action class; it does not derive the exchange principle from matter, and ordinary matter confined to one sector does not automatically share that symmetry. Positive Einstein coefficients are a necessary sign choice, not a complete bimetric perturbation-health proof. The earlier special zero-vacuum and singular-α branches remain separate.

With α=1, their C=Λc⁴/a₀² equals ∫y(ν−1)dy. Restoring g_N=a₀y gives Λc⁴=∫(g−g_N)dg_N. This is a correct conditional source-to-vacuum dictionary when its endpoint and normalization assumptions hold. The kernel's finite moment remains to be selected. The script now correctly labels the πT/4−ln(4T)/8+1/16 expression as asymptotic, not an exact integral, and preserves the earlier failed stricter criterion. Its solar turn-off forecast is a prediction of the assumed fitted radial kernel; no external-field, planetary or fully coupled relativistic source calculation is established by that arithmetic.

## Uniform no-go for the stated self-reflection equation with k≥2

For T>0,k>1 define

    C_k(T)=∫₀∞ [y(√(1+1/y)−1)]/[1+(y/T)^k] dy,
    q(y)=y(√(1+1/y)−1)=1/[√(1+1/y)+1].

Then 0<q<1/2, q is strictly increasing, and

    C_k(T)/T=∫₀∞ q(Tt)/(1+t^k)dt.

Let I(k)=∫₀∞dt/(1+t^k), finite for k>1. For k≥2, I(k)≤I(2)=π/2. One direct proof of monotonicity, requiring no special-function formula, splits at one and sends t→1/t in the lower half of the derivative integral:

    I′(k)=−∫₁∞ t^(k−2)ln(t)(t²−1)/(1+t^k)² dt<0.

Differentiation is justified locally in k>1 by an integrable logarithmic power tail. Therefore

    C_k(T)<T I(k)/2≤πT/4<T,  for all T>0,k≥2.

The proposed self-reflection equation T=C_k(T) has no positive solution in this **entire** cutoff-exponent range, not merely the sampled shapes and finite T values in p55. This is a sharpened route-specific exclusion. It does not rule out a differently defined energy balance, other turn-off functions or the 32π target itself.

## Why allowing the exponent to float restores the fitting freedom

For a fixed T, the same split of the derivative gives

    ∂_k[C_k(T)/T]
      =−∫₁∞ t^(k−2)ln(t)[t²q(Tt)−q(T/t)]/(1+t^k)² dt<0.

The strict sign uses t>1 and monotonic q. At k→1⁺ the tail diverges, since q(Tt)→1/2; at k=2 the ratio is below one. Continuity and strict monotonicity give a unique k(T)∈(1,2) satisfying C_k(T)=T for **every** chosen T>0. Thus broadening the self-reflection construction to a freely chosen real exponent can reproduce every desired positive coefficient. The equation alone does not select a universal one.

For fixed k>1, C_k(T)/T is strictly increasing in T. It tends to zero as T→0 and to I(k)/2 as T→∞, by dominated convergence with q bounded by 1/2. Accordingly a positive self-reflection root exists uniquely precisely when I(k)>2; equality gives no finite root. This also explains why the large-T slope is a necessary discriminator and why “slope at least one” needs strictness at its boundary. The classification is analytic; it is not inferred from a finite set of numeric exponents.

No physical positivity, global ellipticity, solar-system viability or microscopic justification is asserted for all these real-exponent kernels. The result concerns the proposed integral equilibrium equation. It strengthens the sampled negative result while isolating the extra shape-selection premise needed to turn a viable root into an independently forced 32π.

There is also a controlled static-admissibility statement for large fitted roots. In the earlier symmetric NR dictionary, f(y)=y(ν−1)=q(y)/[1+(y/T)^k] and D=1+2f′. Since q′>0, q<1/2 and x^(k−1)/(1+x^k)²≤1 for all x>0,k>1, D>1−k/T. Every prescribed self-reflection coefficient T=C>2 therefore admits its unique k(T)∈(1,2) with D>0 globally in this stated NR action dictionary. Positive finite moments and this strict radial ellipticity do not select the target even after the self-reflection equation is imposed. This is a static-sector claim, not full relativistic or quantum health.
