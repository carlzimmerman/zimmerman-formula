# Four-dimensional curved pion determinant: a direct calculation

This calculation targets a genuine four-dimensional infrared part of the proposed vacuum response. It is the ordinary one-loop determinant of the leading chiral pion operator on a closed round S4. It is not the full QCD generating functional, an eta-prime/topological completion, or a computation of the proposed cosmological coefficient.

## Action and exact spectrum

The leading covariant chiral action, expanded at its aligned vacuum and continued to Euclidean signature, gives one real pion quadratic operator L=-nabla²+M². Its curvature coupling is minimal at this chiral order. Equation (1) of Alharazin et al.2006.05890v1 supplies the covariant leading action. Additional curvature-dependent chiral operators occur at higher orders and must not be silently set to zero in a full prediction.

On S4 of radius H^-1, scalar spherical harmonics have eigenvalues H² l(l+3), l=0,1,..., and degeneracy d_l=(l+1)(l+2)(2l+3)/6. The eigenvalue follows by applying the R5 Laplacian to r^l times a spherical harmonic. The degeneracy is the number of homogeneous degree-l polynomials in five variables minus their r² traces. The constant mode is retained at M>0; deleting it would change the defined determinant.

Define K(u)=sum_l d_l exp[-u l(l+3)], V=8pi²/(3H4). With n=l+3/2 one can include the n=1/2 term because its degeneracy is zero:

K(u)=exp(9u/4)/3 sum_(k>=0) [(k+1/2)^3-(k+1/2)/4] exp[-u(k+1/2)²].

The Mellin/Hurwitz expansion of sum n^p exp(-u n²) has integral term Gamma((p+1)/2)/(2u^((p+1)/2)) and residues (-u)^j zeta(-p-2j,1/2)/j!. Therefore

6u²K(u) ~ 1+2u+(29/15)u²+(74/63)u³+(149/315)u4+... .

The coefficients also agree with Kluth–Litim1910.00543v2 Table1 (R=12H²); its Table4 gives the spectrum. The asymptotic expansion is not a convergent series asserted for arbitrary u.

## Define and calculate the subtracted determinant

For one real field f=(1/2V)log det L. Removing the first three local heat terms defines a finite, specified residual:

f_res(H,M)=-H4/(32pi²) integral_0^infinity du u^-3 exp[-(M/H)²u]
 [6u²K(u)-1-2u-(29/15)u²].

This subtracts constant, curvature and curvature-squared terms, with the same positive mass and covariant measure. Finite choices of these local terms do not affect a linear-H coefficient. An additional higher-curvature EFT matching term could change H6 and higher coefficients, but is not an H term.

For fixed positive M and H/M->0, the bracket is (74/63)u³+O(u4). Splitting the integral at a fixed positive u0, the small-u remainder gives O(H8/M4), and the large-u tail is exponentially suppressed in (M/H)²u0. Watson's asymptotic argument consequently gives

f_real,res=-(74/63)H6/(32pi² M²)+O(H8/M4).

In particular the coefficient of H is exactly ZERO for this determinant, not merely small on a tested grid. This conclusion uses the actual positive massive scalar spectrum and its controlled small-u remainder, not an assertion about every gapped or topological QFT. No exact transseries exponential coefficient is claimed here.

For the round invariant stress prescription rho=f-(H/4)partial_H f,

rho_real,res=+(74/63)H6/(64pi² M²)+O(H8/M4).

Local curvature counterterms of all higher integer orders likewise cannot create a linear H term. Their presence does prevent identifying the displayed H6 coefficient with the complete physical QCD coefficient. The inverse-M² leading chiral singularity of this pion loop is the specified calculated contribution.

## Actual electromagnetic function from the charged-pion mass

For the two charged real pion modes, retain their leading mass shift Delta=2e²F²Z, with e²=4pi alpha, M²+Delta>0. The difference of this one-loop contribution between charge e and charge zero is

delta rho_charged,res=(74/63)H6/(32pi²)
 [1/(M²+Delta)-1/M²]+O(H8),

partial_(e²) delta rho_charged,res at zero
=-(74/63)F²Z H6/(16pi² M4)+O(H8).

This is an explicit alpha-dependent four-dimensional curvature contribution. Its linear-H coefficient and that coefficient's charge derivative are both zero for every fixed positive pion mass. No alpha value or numerical Z has been assigned. The function contains the genuine QCD matching parameter Z; no complete physical finite-mass numerical response is claimed.

The calculation retains the LO charged mass inside one pion loop. It omits interacting photon-pion loops, higher-curvature pion operators, higher loops, non-pion matching and any proposed additional nonlocal/global sector. Its leading inverse-mass singularity can be an infrared benchmark, while the full H6 response needs those additional terms. The hierarchy is H << M << Lambda_chi. Sending M->0 at fixed H invalidates this expansion and enters a different zero-mode regime. It is not a result about that regime or a nonadiabatic cosmological state.

## Independent finite checks

The script derives the heat coefficients from exact Bernoulli/Hurwitz residues and compares with a direct positive spectral heat sum. A second check uses the UV-finite third mass derivative:

partial_(M²)^3 f=(1/V)sum_l d_l/[M²+H²l(l+3)]³.

For a=M²/H²-9/4>0, set z=1/2+i sqrt(a) and

S2=-Im psi1(z)/(2sqrt(a)),
S3=-Im psi1(z)/(8a^(3/2))+Re psi2(z)/(8a).

Then the exact derivative is [S2-(a+1/4)S3]/(8pi²H²). It follows by differentiating the paired digamma partial fractions twice; the divergent zeroth sum is never assigned an arbitrary finite value. Direct positive partial sums with a conservative n^-3 tail bound independently bracket this expression at the declared finite points.

Its small-H expansion satisfies

32pi²M² partial_(M²)^3 f
=1+2(H/M)²+(58/15)(H/M)4+(148/21)(H/M)6+... .

This derivative check alone would leave mass-independent integration terms undetermined. The proper-time definition above fixes them within this determinant; the zero-H-coefficient conclusion does not rest on the mass derivative alone. Finite checks support the algebra/implementation, while the asymptotic argument supplies the stated zero coefficient. Numerical tolerances are not interval-certified errors.

This narrows the proposed mechanism: an H Lambda³ term cannot be attributed to this ordinary massive pion determinant. Full QCD might contain additional matched physics only if its specific generating functional establishes it. A source analogy or a susceptibility value cannot supply that missing coefficient.
