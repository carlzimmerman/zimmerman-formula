# QCD-S: rederive the tilted-torus Schwinger normalization

Parent FSP-002, new work package FSP-003. Coordinator derivation, 2026-10-18 America/New_York. This is a bounded audit of one claimed exact supporting analogy, not a calculation of four-dimensional c_H. No novelty claim.

## Raw setting and target

Use a flat Euclidean torus with coordinates x0,x1 in [0,L), metric g=[[|tau|^2,tau1],[tau1,1]], tau=tau1+i tau0, tau0>0, and volume V=L^2 tau0. Its scalar Laplacian eigenvalues are

p_n^2=(2 pi/L)^2[(n0-tau1 n1)^2+tau0^2 n1^2]/tau0^2.

This follows directly by inverting g and applying -Delta to exp(2 pi i n.x/L). It agrees with the raw metric convention in Sachs–Wipf hep-th/9508142v1 eq(13). The mass m=m_gamma=e_2/sqrt(pi)>0 is the Schwinger mass; e_2 has units of mass and is not four-dimensional alpha.

Define the convergent, zero-mode-excluded kernel

m^2 K=(1/V) sum_(n!=0)[1/p_n^2-1/(p_n^2+m^2)].

Target: independently evaluate it and the associated normalized condensate, including the constant mode of the massive Green function. Determine whether a uniform large-L limit at fixed nondegenerate tau has the alleged 1/L term.

## Direct zero-slice calculation

On the n0=0 slice, p^2=(2 pi/L)^2 |tau|^2 n1^2/tau0^2. The exact massive sum, INCLUDING n1=0, is

(1/V) sum_(n1 in Z) 1/(p_(0,n1)^2+m^2)
=1/(2mL|tau|) coth(mL tau0/(2|tau|)).

This uses sum_(n in Z)1/(n^2+b^2)=pi coth(pi b)/b. No source condensate formula or interpretation enters this elementary sum.

The prefactor printed in hep-th/9508142v1 eq(119), PDF page 44 / manuscript page43, instead reads 1/(2mL tau0) with the same coth argument. The original PDF pixels were inspected; the difference is not only OCR. That expression is correct on rectangular tori (tau1=0) but disagrees with this zero slice at tau1!=0. Independent review and comparison to the full spectral sum are required before adjudication.

For a=mL|tau|/(2 pi), define

F(a)=sum_(n>=1)[1/n-1/sqrt(n^2+a^2)],

B(a,tau)=sum_(n>=1)1/sqrt(n^2+a^2)
 * [1/(exp(b_n+i theta_n)-1)+1/(exp(b_n-i theta_n)-1)],

b_n=2 pi tau0 sqrt(n^2+a^2)/|tau|^2,
theta_n=2 pi tau1 n/|tau|^2.

Summing the other integer index by the standard shifted coth sum gives

m^2 K= -coth(mL tau0/(2|tau|))/(2mL|tau|)
+1/(m^2 V)
+[-log|eta(-1/tau)|^2+F(a)-B(a,tau)]/(2 pi).

The massless eta term, F and B have the same convention as the source's eqs(119)–(121); only the demonstrated zero-slice prefactor is replaced. The finite convergent double spectrum provides a check independent of the eta/F representation.

## Condensate and the allegedly linear term

In the Schwinger limit of the same source's raw Gaussian formula eq(115), before inserting its eq(119),

Sigma_+(L,tau)=|eta(tau)|^2/L
 * exp[-2 pi/(m^2 V)+2 pi m^2 K].

A chirality/sign convention changes the overall constant; normalized size dependence is the claim. The explicit instanton factor cancels the massive zero-mode 1/(m^2 V), rather than leaving an artificial inverse-area term. The eta transformation |eta(-1/tau)|^2=|tau| |eta(tau)|^2 then gives

Sigma_+=1/(L|tau|)
 * exp[-pi coth(mL tau0/(2|tau|))/(mL|tau|)+F(a)-B(a,tau)].

Use the Poisson/Bessel identity

F(a)=gamma+log(a/2)+1/(2a)-2 sum_(k>=1) K0(2 pi a k).

With Sigma_+infty=m exp(gamma)/(4 pi), the finite ratio is

log(Sigma_+/Sigma_+infty)
= [1-coth(mL tau0/(2|tau|))]/(2a)
 -2 sum_(k>=1) K0(mL|tau| k)-B(a,tau).

For fixed tau0>0 and fixed tau1, every term is exponentially small as mL grows. In particular, the apparent 1/(2a) cancels. The source prefactor with tau0 instead would leave

delta log Sigma = -pi [1/tau0-1/|tau|] coth(mL tau0/(2|tau|))/(mL),

which has precisely the nonzero inverse-L coefficient used in Urban–Zhitnitsky0906.2165v2 eqs(42)–(44) and repeated in2506.14182v4 eq(35). Printed additional signs/plus symbols in the older condensate expressions are not silently trusted; the comparison starts with the operator sum and Gaussian formula.

An independent representation follows from the infinite-volume-normal-ordered Gaussian vertex: massive Green images give

log(Sigma_+/Sigma_+infty)
=-sum_((n0,n1)!=0) K0(mL |n1+tau n0|).

This is also exponentially small at fixed nondegenerate shape. It is invariant under changing lattice basis. Gaussian bosonization and correct global/zero-mode integration are the physical identification; the raw spectral kernel and its wrong coefficient can be checked without assuming that identification.

## Scope, uncertainty and consequences

For small fermion mass m_f, the leading theta-dependent vacuum energy is -m_f Sigma cos(theta)+O(m_f^2), with the matching full-condensate factor held consistently. Its first-order susceptibility inherits the computed finite-size dependence. At exactly m_f=0, total topological susceptibility vanishes; the nonzero condensate is not a nonzero massless susceptibility. Uniform fixed-shape limits are essential; degenerating a cycle or adding boundaries/defects changes the problem.

If independently confirmed, the tilted-torus coefficient in the claimed supporting formula is not reliable positive evidence for a four-dimensional linear-H term. This does not prove physical QCD c_H=0, rule out every topological/boundary mechanism or disprove the framework's macroscopic findings. It removes one exact-analogy justification and identifies a concrete normalization error to resolve. Actual de Sitter/global QCD still requires its own calculation.

Source authentication: hep-th/9508142v1 (1995-08-25),0906.2165v2 (2009-09-11),1005.1822v1 (2010-05-11 archival 1991 manuscript); titles/authors and histories checked on arXiv. The first two PDFs fetched to temporary storage and their pertinent pages inspected. The rectangular Sachs–Wipf1005.1822 eqs(5.6)–(5.12) explicitly show zero-mode cancellation and Bessel-sum behavior, consistent with the rectangular specialization. Exact source hashes/locators are in SOURCES.json. No old research record was changed.
