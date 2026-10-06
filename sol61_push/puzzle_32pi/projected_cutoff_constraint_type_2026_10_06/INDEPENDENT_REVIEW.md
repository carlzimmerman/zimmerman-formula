# Independent raw constraint-type audit

Accepted as a scoped spatial-constraint result. The finite positive moment forces a negative longitudinal interaction-lapse principal coefficient somewhere on a globally regular matched radial map. This does not imply a time ghost, loss of physical nonlinear-Poisson ellipticity, or failure of the fully coupled constraints. I reconstructed the ADM and radial identities before reading the report's conclusion; no blocking correction was found.

## Frozen pins and evidence

Inspected REPORT SHA256 b535a6931e81d3fef7940571c9d0582ab26173a70241d2c2f2ab6eef73473a2b; checks SHA256 4dde715379922b98e10248b8ceb21ee39c8058f19d2e8e8ed61c4077bfc1a88e; contract 44d1ad7019d4a12e084ca51cba64dd768f25a90598fc9f756a333129ed067754; provenance 490c235590086e82b6dec428113fc6e946c74d9b9f7e7be28fde486802186524. Base declared and inspected source checkpoint is 67e981cf7888172c584868ae80a178492af40fa1.

All four current a manifests independently validate against current inputs: main28/28, controls force/cutoff/derivative28/29 with one intended failure each. The independent algebra below uses a different q parameterization for the threshold and crossing, without importing author functions. No author input was changed or author experiment executed by this reviewer.

## Actual ADM principal and physical radial map

At fixed spatial metrics the actual projected invariant is I=h^{ij}r_i r_j/a0², h positive definite. Differentiating the flux m h^{ij}r_j gives m h^{ij}+2M_II(h∇r)^i(h∇r)^j/a0². In an h-orthonormal frame its transverse and longitudinal coefficients are m and m+2I M_II=m+x m_x. The common volume/lapse factors are positive multipliers for this Hessian; the volume term contributes no highest spatial derivative. This is a frozen-spatial-metric interaction row. The EH metric constraints and mixed transport rows remain part of the full system.

Independently, the actual sourced NR equations give y=(1−2m)x and visible g/a0=(1−m)x. If the visible spherical law is ν(y), x=(2ν−1)y=y+b, b=2y(ν−1). On a C1 globally regular x_y>0 map,

m=b/(2x), m+xm_x=[1−dy/dx]/2=b_y/[2(1+b_y)].

Physical star-force longitudinal ellipticity is instead dy/dx=1/x_y>0. It is therefore consistent for the star operator to remain elliptic while the interaction-lapse row has opposite transverse/longitudinal signs. Erasing the derivative part of the row would miss the result.

## Uniform finite-moment implication

Assume b≥0, b positive somewhere, b∈C1 and J=∫b dy finite. If b_y≥0 everywhere, a positive value b(y0) provides a positive constant lower bound on the whole tail, contradicting finiteness. Hence b_y<0 somewhere and, by continuity, on an interval. At such an interior point b cannot be zero while remaining nonnegative. Thus m>0 and m+xm_x<0 there under x_y>0. No assumption that b has a pointwise limit at infinity is needed.

A deep-to-negative crossing additionally requires b_y>0 near zero. The report explicitly uses a differentiable deep asymptotic for this leaf. Pointwise ν∼y^(−1/2) alone would not permit differentiating the remainder. This optional crossing premise is separate from the finite-moment negative-interval theorem. The excluded sign-changing, nonsmooth, multibranch and different-operator cases are real changes of hypotheses.

The normalization J=∫(ν−1)d(y²)=∫b dy agrees with the optional endpoint vacuum normalization A=J=2C_response. It does not select a cutoff or establish vacuum admission/health.

## Independent cutoff and global threshold reconstruction

For the declared cutoff set q=√(y²+y)−y. Then 0<q<1/2, y=q²/(1−2q), and b=2q T²/(T²+y²). Direct differentiation gives the exact crossing equation

T²=q⁴(3−2q)/(1−2q)³.

Using s=√(1+1/y), q=1/(s+1), this becomes precisely (3s+1)/[(s−1)³(s+1)²]. Its derivative in s is negative and its endpoint limits are infinity and zero. There is exactly one positive-y b_y=0 crossing for every T; global source regularity is still needed to turn it into the principal coefficient crossing.

For the source-fold threshold, clearing the denominator of 1+b_y in the q parameterization and eliminating T² between that numerator and its q derivative independently yields, apart from excluded endpoint factors,

288q⁸−1872q⁷+5328q⁶−8688q⁵+8832q⁴−5688q³+2246q²−492q+45.

Multiplication by (s+1)^8 after q=1/(s+1) gives exactly the author's R(s). This separately confirms the resultant and source derivative normalization.

The exact Sturm sign lists for R at1 and infinity are respectively (−,−,+,−,+,+,+,+,−) and (+,+,+,−,−,+,+,+,−), with variations4 and3. For the discriminant cubic they are (−,−,+,−) and (+,+,+,−), with variations2 and1. Thus each has exactly one root above1. The discriminant birth s0≈2.36579 lies below s*≈2.45661. Just above birth T_plus has positive divergent derivative, while at infinity T_plus→0 with negative derivative. The unique resultant root is on its upper branch, so it is the unique maximum; T_minus has no separate critical root. The open interval family between the two positive roots has connected projection and reaches cutoff values arbitrarily close to zero. Its union is therefore (0,Tcrit), not a numerical grid conjecture.

The values Tcrit≈0.20863684329757 and y*≈0.19861237062816 agree with the raw stationary equations. Equality gives an isolated zero derivative and a nonregular smooth-inverse limit; it does not satisfy strict global x_y>0. For the declared T=128.915, the unique radial principal crossing is y≈12.55623258489415. At twice that y the recorded x_y≈0.99758946 remains positive while the relative longitudinal coefficient≈−0.00120818 and m≈0.01830004 have opposite signs. This is a load-bearing example of the two ellipticity notions differing.

## Exact remaining implication

The result identifies a spatial row changing type on the inherited radial family. It does not classify its constraint preservation, eliminate the mixed common/relative operators, prove an admitted source background, or establish a temporal instability. Coupled metric/clock constraints can change what this frozen-row symbol means physically. The report preserves that missing arrow and does not elevate either the finite moment or the numerical p57 cutoff into a selected constant or all-MOND exclusion.
