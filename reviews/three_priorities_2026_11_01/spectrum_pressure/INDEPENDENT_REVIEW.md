# TP01 spectrum/pressure: independent mathematical reconstruction

1 November 2026. Reviewer: `/root/independent_math_transport`, separate from
the spectrum author. **Primary verdict: correct only with the stated rigid,
canonical-K, fixed-coupling one-loop and assumed-portal restrictions.** The
full-spectrum algebra supports the finite threshold result. It does not yet
support a physical halo-pressure no-go for the matched microscopic theory.

This review reconstructed the valley, Hessian, vector normalization and the
pressure identity from `INVERTED_HIERARCHY.md` and the pre-run contract, then
inspected the dense implementation, independent blocks, symbolic trace check
and saved outputs. It was not a blind audit: the author supplied the final
trace formula and scope caveats before the final trace reconstruction. No
new spectrum/pressure calculation was executed by this reviewer. Input hashes
and manifest-validation results are in `INDEPENDENT_REVIEW_INPUTS.json`.

## 1. Claim card and dependency graph

The quantified microscopic objects are two canonical adjoint chiral fields
A,B and one canonical singlet X of rigid SU(5), with positive f,h,λ and

    W=fX+(h/2)X Tr A²+(λ/2)Tr A²B.

Adjoint coordinates satisfy Tr(T_a T_b)=δ_ab, while the gauge generators are
T_a/√2. The radial slice has real X≥0 and commuting A=i aD, B=bD,
D=diag(2,2,2,−3,−3). The exact classical spectrum is followed by a one-loop
potential in the stipulated supersymmetric subtraction scheme. The pressure
claim adds K=kρ^(5/3), a positive source and the trial factor exp(−2s), with
s=ln(X/v). The action does not itself derive this material coupling.

The dependency chain is:

    specified W,K and gauge normalization
      → stationary D-flat valley
      → chiral Hessian + gauge Hessian + gaugino mixing
      → complete physical tree spectrum
      → stipulated one-loop supertrace and finite thresholds
      → U(s), with fixed couplings and a prescribed portal
      → local radial stationarity and pressure/compressibility.

Running/matching, loop-corrected transverse stability, light/IR modes, a
microscopic occupied-state portal and the full gravitational vacuum are
additional unchecked physical leaves. No algebraic success closes them.

## 2. Valley and canonical singlets: passed

Since Tr D²=30 and (D²)_traceless=−D, direct differentiation gives

    F_A=i a(hX−λb)D,
    F_X=f−15h a²,
    F_B=(λa²/2)D.

Set Δ=30h²+λ², a²=2fh/Δ and b=hX/λ. Then

    F_A=0, F_X=fλ²/Δ, F_B=(fhλ/Δ)D,
    Σ|F_i|²=f²λ²/Δ.

The remaining F stationarity condition follows from the same relations;
commuting normal A,B imply D-flatness. Thus the printed valley is an actual
stationary valley of this W, not a radial substitution into a different
potential.

For the singlet adjoint direction write A=ãD/√30, B=b̃D/√30. Its restricted
superpotential is

    W=fX+(ã²/2)(hX−λb̃/√30).

An orthogonal rotation of X,b̃ isolates the flat coordinate
T=√Δ X/λ and its orthogonal partner. On the valley the nonzero singlet
mixing has magnitude √(2fh). Consequently this sector contains four real
scalar mass squares 2fh, two real scalar zeros, two Weyl mass squares 2fh
and one Weyl zero. Its one-loop contribution cancels. This independently
checks the singlet block, including its independence of X.

## 3. Full matrices, gauge mixing and multiplicities: passed

With F_i=W_i, M_ij=W_ij and B_ij=Σ_k conjugate(F_k)W_kij, the real Hessian
in δz=(q+ip)/√2 is exactly the four-block form printed in DERIVATION.md.
At D=0, the D contribution is the positive form J_DᵀJ_D, with
J_D=√2g(Re(R_a z),Im(R_a z)). No omitted D times a second derivative remains.

The covariant kinetic term gives vector mass matrix
2g² Re[(R_a z)†(R_b z)]. Off-block roots connect eigenvalues 2 and −3 of D,
so there are twelve equal masses 25g²(a²+b²); the twelve SU(3)×SU(2)×U(1)
generators are unbroken. The factor 25 and the factor 2 in the general
matrix agree with the two generator-normalization conventions.

The gauge Yukawa term supplies √2g z†R_a as a chiral/gaugino mixing block.
A common gaugino phase can remove the conventional factor i because there
is no independent gaugino mass here. Singular values of the complete
symmetric 73×73 matrix give the Weyl masses; diagonalizing the complex
matrix as a Hermitian mass matrix would be incorrect, and the code does
not do that.

The representation labels r=2,−3,−1/2 arise from the D anticommutator in
the SU(3), SU(2) and off-block sectors, with multiplicities 8,3,12. Together
with three chiral singlets, these account for all 49 chiral fields. The
twelve broken gauginos are included in the 3×3 blocks; the twelve unbroken
gauginos remain massless. After removing twelve gauge Goldstone scalar
coordinates there are 86 physical real scalars plus 60 vector polarizations,
matching the 146 Weyl degrees of freedom. Zero masses contribute zero to
the potential, so retaining Goldstone zeros in the numerical Hessian does
not add a spurious massive-vector polarization.

The code retains the extra zero fermions at X=0. It does not replace the
entire spectrum by only a massive radial mode. Positivity of a sampled
tree transverse gap does not justify integrating out the Goldstino,
unbroken gauge sectors or the R phase.

The exact blocks also prove positive tree transverse masses beyond the
sampled points. For the unbroken scalar 2×2 blocks,
det H_±=q²(q²±β): the factors q²±β are 5c,11c for r=2 and 16c,20c for
r=−3, with positive traces. For a broken block β=q², so H_minus has
determinant zero and positive trace m²+q²; this is precisely its Goldstone
direction. The other block has

    det H_plus=2q⁴+q²L²+(m²+2q²)R²−2mqLR
              =2q⁴+q²L²+(m²+4q²)R²>0,

where mL+qR=0 was used only in the second equality. Its trace is positive.
Together with the singlets this proves tree transverse positivity for
every finite X≥0, f,h,λ>0 and g≥0 in the declared model. It is not a
uniform positive gap as X tends to infinity, nor a quantum transverse
stability theorem. The complex flat direction remains flat at tree level.

## 4. Supertrace independently reconstructed: passed

Define c=fhλ²/Δ. For each unbroken block write
m=(1+r)hX, q=rλa and β=(1+r)c. In a chiral block the scalar-minus-Weyl
fourth trace is 2β². Multiplicity-weighting r=2,−3 therefore gives

    8×2(3c)²+3×2(−2c)²=168c².

For a broken block let L=5ga and R=5gb. Its stationarity relations are

    β=q²=c/2,        mL+qR=0.

Expanding the scalar blocks, the full 3×3 Weyl block and the vector term
gives, before using the last relation,

    STr M⁴(block)=2β²+2(β−3q²)L²−6(mL+qR)².

Thus the actual valley gives c²/2−50g²a²c per broken block. Summing twelve
of them and the unbroken sectors yields

    STr M⁴=174c²−600g²a²c
            =6f²h²λ²(29λ²−200g²)/Δ².

The same trace expansion gives STr M²=0. Both identities are independent
of X. This reconstruction did not infer missing eigenvalues from the trace;
the full matrices and multiplicities were checked first.

At the inherited comparator g²=29λ²/200, explicit one-loop subtraction-scale
dependence and the common log c term cancel. Every noncanceling squared
mass is c times a function of z=hX/√c: in particular
(5ga)²/c=29/4 and (5gb)²/c=29z²/8. Therefore CW=c²F(z) at this order.
The finite function F need not vanish and is not selected by the cancellation.
No two-loop, all-field or gravitational protection follows.

The logarithmic coordinate has kinetic term |T_v|²exp(2s)(∂s)². Thus an
isolated loop calculation using constant canonical s is a different theory;
its exp(6s) operator cannot simply be added as a mandatory correction here.
Conversely, cancellation of the one-loop divergent supertrace does not
eliminate unknown Kähler or higher-order operators.

## 5. Pressure implication: passed conditionally

Let w(ρ,s)=kρ^(5/3)exp(−2s)+U(s). Radial stationarity gives
kρ^(5/3)exp(−2s)=U_s/2, so a positive kinetic source requires U_s>0. The
envelope derivative gives

    P=ρ w_ρ−w=U_s/3−U,
    d lnρ/ds=(3/5)(2+U_ss/U_s).

Consequently

    dP/d lnρ=5U_s(U_ss−3U_s)/[9(2U_s+U_ss)].

On the positive-source branch, local radial stability requires
2U_s+U_ss>0, while positive compressibility requires U_ss>3U_s. At its
compressibility boundary the radial curvature is still 5U_s>0. These are
different physical conditions; a radial potential minimum alone is not a
positive material-pressure theorem.

The saved independent 60-digit derivative calculation places the pressure
boundary at X/X_min=1.1772996111... and the radial endpoint at
1.8533618102... in the fixed-order comparator shape. At X/X_min=1.2,
the reported dP/dlnρ is negative while the radial curvature and every
positive tree transverse gap used in the diagnostic remain positive.
The root values are numerical evidence, not exact transcendental constants
or a proof that no other branch exists outside the searched domain.

The additional density-reach check uses a declared comparison scale,
ρ_*=[3B_curv/(2k)]^(3/5), B_curv=U_ss(v)/9, and s=ln(X/X_min). It gives

    ρ/ρ_*=[U_s exp(2s)/(3B_curv)]^(3/5),
    d lnρ/ds=3(2U_s+U_ss)/(5U_s)>0.

The monotonicity is exact on a connected positive-source radially stable
branch. The saved 33-state supplement finds ρ/ρ_*=0.5908117662... at the
pressure boundary. This strengthens the fixed-order comparison with the
earlier intended dense-log regime. The scale is defined from the vacuum
curvature, not a derived asymptotic log coefficient or measured halo density;
the unknown k cancels only in this ratio. The physical caveats remain.

The radial physical mass factor W_ss/(2|T|²) is correct for the stated
complex-field normalization on a fixed-phase slice. The phase/light-mode
restriction and slowly varying elimination remain essential. A large
tree transverse gap compared with this radial scale is supporting evidence
for that restricted approximation, not a proof of nonlinear halo evolution.

## 6. Obligation matrix and verdict limits

| Obligation | Verdict |
|---|---|
| Specified W/K → printed stationary valley | Passed by direct differentiation |
| Hessian, vector normalization, gaugino mixing and field counts | Passed in the rigid canonical model |
| Tree transverse positivity for every finite X≥0 | Passed by the exact determinant argument above; no uniform-in-X gap or quantum theorem |
| Full-spectrum supertraces and critical shape scaling | Passed by the independent algebra above |
| Numerical spectra, derivative roots and grid signs | Computationally verified only in the recorded finite ranges; reviewed, not rerun here |
| Portal → total pressure and sign criterion | Passed conditional on the declared portal and local elimination |
| Constant-canonical-s exp(6s) test transferred to this model | Inapplicable without a correct field/kinetic dictionary |
| Fixed one-loop result → matched physical vacuum/halo exclusion | Not established |
| Quantum transverse stability, light/IR and gravity matching | Not addressed by these computations |

The largest limitation is quantitatively visible: the older leading-log
two-loop curvature is approximately 0.78,3.13,8.69 times the new one-loop
threshold curvature at equal couplings .3,.6,1. That comparison is an
omitted-order diagnostic, not an error estimate with a proved sign. The
.03 weak-coupling control suppresses this known ratio to about .00782;
it still does not supply all missing matching or IR information.

The strongest safe new statement is therefore the complete tree-spectrum
and fixed-order threshold calculation, together with a conditional local
pressure failure and a corrected canonical-field radiative comparison.
The smallest missing implication is a consistently matched effective
action whose corrections, light sectors and actual matter portal are
controlled on the proposed branch. Repeating the old leading-log radial
minimum would not resolve it.

The numerical record already contains adequate cross-method checks for
this finite assertion; no production calculation or parameter scan was
requested or launched by this reviewer. Any subsequent continuation should
begin in the explicitly weak-coupling regime and state its matching accuracy,
instead of promoting the present .3..1 fixed-order grid to a final physical
exclusion.
