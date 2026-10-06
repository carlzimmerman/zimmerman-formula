# An all-external-field quadrupole sum rule for the vacuum moment

The continuum quadrupole response is not blind to the moment C=integral y[nu(y)-1]dy. Under an absolute-moment hypothesis, the exact point-source QUMOND operator satisfies

    integral_0^infinity e^(-1/2) Q2(e) de = (9 pi a0)/(35 r_M) C,
    r_M=sqrt(GM/a0).

The Mellin weight is nonzero: K(1/2)=-4pi/35. Thus identical quadrupole responses at all external Newtonian fields imply identical C in this function class. This closes the ideal continuum moment-identification arrow, while supplying no theoretical selection of the value 32pi and no full-kernel injectivity theorem.

## Operator and full weight

Use the actual Claude force convention G=-GM rhat/r^2+a0 e zhat, psi=-Phi_p, anomalous physical acceleration grad psi. In the same convention as the parent report, Q2=3A2 and

    Q2(e)=-(9a0)/(4r_M) integral_0^infinity f(y) w_e(y)dy,
    f(y)=nu(y)-1,
    w_e(y)=sqrt(y) F(e/y).

Here e is the external Newtonian acceleration divided by a0, not the observed external acceleration eta=e nu(e). The uniform external field contributes only the removed dipole. This is the point-source, uniform-external-field quadrupole harmonic coefficient; it is not a disc response, finite-distance quadrupole fit, or the full p57 orbital force.

For q=e/y, define

    P(q)=2q^3+q^2+6q+12,
    R(q)=-2q^3+q^2-6q+12.

The full weight on both sides of the cancellation shell is

    F(q)=-2/(35q^3) [P(q)/sqrt(1+q)
                         -sgn(1-q) R(q)/sqrt(|1-q|)],  q != 1.

No q<1 expression is extrapolated to q>1. To reconstruct it, start from the exact angular-radial integral

    w_e(y)= integral_|y-e|^(y+e) y/(2e t^(3/2))
                [e(3xi-5xi^3)+t(1-3xi^2)]dt,
    xi=(y^2-e^2-t^2)/(2et).

Rescale t=y tau. At y=1,e=q an exact primitive is

    [-25q^6+35q^4 tau^2+75q^4-35q^2 tau^4+70q^2 tau^2
      -75q^2-7tau^6-105tau^4-105tau^2+25]/(280q^3 tau^(7/2)).

Its upper endpoint is -2P/[35q^3 sqrt(1+q)]. Its lower endpoint is -2R/[35q^3 sqrt(1-q)] for q<1 and +2R/[35q^3 sqrt(q-1)] for q>1. Subtracting lower from upper proves the full formula. The value assigned exactly at q=1 is immaterial for integration.

The three relevant asymptotics are

    F(q)=q^2/10+O(q^4), q -> 0,
    F(q)=-q^(-7/2)+O(q^(-11/2)), q -> infinity,
    F(q)=+2/[7sqrt(1-q)]+O(1), q -> 1-,
    F(q)=-2/[7sqrt(q-1)]+O(1), q -> 1+.

Consequently integral q^(s-1)|F(q)|dq converges for -2<Re(s)<7/2. The shell is an integrable one-sided inverse-square-root singularity, not a delta term. An early preflight deliberately exposed a mistaken high-q exponent; the exact limit check failed it, and the exponent was corrected before any frozen execution record. The final inputs use q^(-7/2).

## Exact Mellin factor at the required index

At s=1/2, write the Mellin integral as -2/35 times the combined integral of q^(-7/2)P/sqrt(1+q), minus q^(-7/2)R/sqrt(1-q) below one, plus q^(-7/2)R/sqrt(q-1) above one. The individual terms diverge at zero or infinity; only their combined finite-cutoff expression is used. This avoids unjustified splitting into divergent beta integrals.

The substitutions z=sqrt(1+1/q), sqrt(1/q-1), sqrt(1-1/q), respectively, have elementary primitives

    Splus(z)=-24z^5/5+12z^3-14z-2ln(z-1)+2ln(z+1), z>1,
    Slow(z)=-24z^5/5-12z^3-14z+4atan(z), z>=0,
    Shigh(z)=24z^5/5-12z^3+14z+2ln(1-z)-2ln(1+z), 0<=z<1.

For epsilon<1<Rcut, the combined Mellin integral is

    -2/35 [Splus(sqrt(1+1/Rcut))+Shigh(sqrt(1-1/Rcut))
                   +Slow(sqrt(1/epsilon-1))-Splus(sqrt(1/epsilon+1))].

The first two terms tend to zero together; their logarithmic divergences cancel. The last difference tends to 2pi; its polynomial divergent parts cancel, leaving 4atan(infinity). Therefore K(1/2)=-4pi/35 exactly. The script differentiates all three substituted primitives and checks both combined limits symbolically; a separately split numerical quadrature with exact tail restoration agrees.

## Fubini hypotheses and identification theorem

Assume f is measurable and integral_0^infinity y|f(y)|dy is finite. Let the same kernel govern every e>0, with fixed a0 and fixed central GM. Since

    integral de e^(-1/2) integral dy |f(y)|sqrt(y)|F(e/y)|
       = [integral y|f(y)|dy] [integral q^(-1/2)|F(q)|dq] < infinity,

Tonelli and then Fubini justify the variable substitution e=yq and every interchange. Q2 is defined almost everywhere and integrable with this external-field weight; smooth locally bounded physical kernels avoid exceptional shell pathologies. This establishes the displayed sum rule for signed f as well as positive f.

More generally, whenever the corresponding absolute y-moment is finite and -2<Re(s)<7/2,

    integral e^(s-1)Q2(e)de
      = -(9a0)/(4r_M) [integral q^(s-1)F(q)dq]
                          [integral y^(s+1/2)f(y)dy].

No full closed form for this general Mellin factor or inversion theorem is required here. At s=1/2 the factor is demonstrably nonzero. For two kernels with finite absolute C moments, if their Q2 functions agree almost everywhere for all e>0, subtraction and this sum rule force their C values to agree. This is moment identification, not proof that the kernels themselves are identical. Constant f is a familiar quadrupole-null response but falls outside the finite absolute-moment hypothesis; it is not a counterexample.

## Why finite measurements still leave a missing arrow

For an external-field interval [emin,emax], the response integral is instead

    -(9a0)/(4r_M) integral y f(y)
          [integral_(emin/y)^(emax/y) q^(-1/2)F(q)dq]dy.

Its y-dependent factor is not the constant K. The finite-band test in checks.py demonstrates this directly. Dominated convergence recovers the full sum rule as emin tends to zero and emax tends to infinity, but no error bound independent of unmeasured response tails follows from a finite dataset alone. If f has known support [ymin,ymax], a sufficient truncation-error bound is |9a0/(4r_M)| times its absolute C moment times the sum of the absolute Mellin tails below emin/ymin and above emax/ymax. Those tails scale respectively as (emin/ymin)^(5/2)/25 and (emax/ymax)^(-3)/3 in their small/large limits. These support and tail assumptions are additional information, not inferred here.

The finite-even-multipole null theorem in the sibling higher_multipole_identifiability report remains valid: finitely many external fields do not supply this continuum integral. Actual environmental external fields are not independently dialed over (0,infinity), and external Newtonian e must be calibrated; integrating over observed eta without the Jacobian d eta/de=nu+e nu' changes the operator. Moreover, other bodies may not share a strictly uniform external field. Present orbital likelihoods do not measure the ideal continuum.

If a separate covariant action rigorously maps its normalized vacuum coefficient to this same C, the ideal continuum quadrupole data would determine that coefficient. This report supplies no such mapping, no relativistic stability result, and no prediction that the coefficient equals 32pi. The smallest remaining physical arrow is an accessible response-tail reconstruction with the same calibrated action and normalization, or a microphysical selector that predicts the integral independently.

## Reproducibility and source scope

The exact field-law input is Milgrom, arXiv:0911.5464v2 (2 March 2010), equations (3)-(8), https://arxiv.org/html/0911.5464v2, checked during the preceding sibling audit. The parent QUMOND primitive and Claude solver are pinned as raw inputs, not imported or executed. This Mellin calculation is reconstructed from their field operator; no global novelty claim or external observational assertion is made.

The final checks cover both q branches, exact primitive/endpoint factors, endpoint convergence, three exact substitution primitives, combined limits, independent numerical K, and bounded operator controls. A signed two-shell test is distributional and only checks the linear moment dictionary; it is not a physical interpolation kernel. Seventy-digit quadrature is not interval-certified. Three intended negative controls assert a zero Mellin factor, use the wrong shell branch, or equate a finite band to the continuum. Standard fresh manifests record both successes and intended failures. Parent files and previous evidence remain unchanged.
