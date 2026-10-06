# A covariant shared-leaf projector with positive radiation principal stiffness

Status: a changed action with an analytic, conditional radiation-principal repair. It is not full stability, a cold-abundance mechanism or a 32pi selector. Base f2c6144f842b9d56b61781d7399e598a1328a726. The full arithmetic-action radiation reduction is a pinned dependency in provenance.json; its finite-wavelength caveat remains relevant.

## Geometry, without an externally chosen coordinate metric

Restrict each spacetime metric to the common timelike clock's tangent leaf. These positive definite covariant leaf metrics are gamma and gammahat. Set

h=(gamma+gammahat)/2, d=(gamma-gammahat)/2,
h_lambda=h+lambda d h^-1 d, lambda>0.

Define the spacetime contravariant tensor B_lambda by embedding the inverse leaf metric h_lambda^-1 with a leaf tangent basis. Basis changes cancel between the inverse and embedding. Thus B_lambda annihilates dtheta as a covector and is independent of the tangent coordinates. A monotone relabeling of theta leaves the leaf unchanged. It is exchange symmetric because d reverses sign twice; it uses no reference metric. For any tangent v, v^T h_lambda v=v^T h v+lambda(dv)^T h^-1(dv)>0. This works for every n>=3, although the matter computation below is n=3 only.

Change only the acceleration invariant to

I_lambda=B_lambda^{mu nu}(a_g-a_h)_mu(a_g-a_h)_nu/a0^2.

All volume, Einstein, shear, ordinary-matter and M_eff terms are retained. This defines an actual covariant action, not merely a dial attached to a perturbation matrix. Accelerations are each normal's own covector; the contraction projects their difference onto the common leaf. In unitary clock coordinates it is exactly (h_lambda^-1)^ij partial_i ln(N/L) partial_j ln(N/L)/a0^2. The full clock and metric variations of this new invariant must be used in any nonlinear extension.

Write Z=h^-1/2 d h^-1/2; its eigenvalues lie strictly in (-1,1), since h +/- d are both positive. The original arithmetic inverse average, harmonic inverse, and new inverse are respectively

h^-1/2 (1-Z^2)^-1 h^-1/2,
h^-1,
h^-1/2 (1+lambda Z^2)^-1 h^-1/2.

Consequently B_lambda <= B_harm <= B_arith in the positive-matrix order. This is a geometric identity, not an assumption of commuting metrics. The new invariant is nonnegative on its action domain.

## What is preserved and what changes

Every homogeneous isotropic branch has a_g=a_h=0. The invariant and its first variations therefore vanish, irrespective of the spatial metric mismatch; M_eff(0) and the volume equations are unchanged. The original exact homogeneous radiation branch remains admitted. Its quadratic perturbation action changes only the coefficient of (nu_g-nu_h)^2: all metric/clock variations of B_lambda multiply the background-zero squared acceleration difference and first enter at order three about this branch. The boundary terms, fluid action and three auxiliary variables derived in the pinned radiation report are therefore unchanged at quadratic order.

At coincidence d=0, B_lambda=B_arith=gamma^-1. About a coincident weak-field background, B_arith-B_lambda=O(d^2), and the acceleration difference is O(epsilon). The action difference starts at order epsilon^4. Thus the leading static MOND kernel, vacuum quadratic constraints and cubic norm force are the same. This does not preserve the exact noncoincident static source equations or their metric first variations. Claude's source fits and numerical observational verdicts require recomputation in the new action. No pre-existing QUMOND verdict is assigned to it.

The tensor speed remains c_T^2=1/(1-eta) on these isotropic branches: a pure linear tensor perturbation has no lapse-gradient acceleration difference, so the changed interaction has no tensor quadratic contribution. Neither A nor eta nor lambda is selected by these identities.

## Exact high-frequency radiation discriminator

On the pinned Q=1 branch use a,b,L=a^3/b^3,H,H2=L hhat and M=2K. For a nonzero comoving wave vector define P_g=k^2/a^2, P_h=k^2/b^2 and

delta^2=(P_g-P_h)^2/(P_g+P_h)^2.

Since both leaf metrics are multiples of the coordinate identity, the new inverse has eigenvalue

P_lambda=2P_g P_h/[(P_g+P_h)(1+lambda delta^2)].

Expansion of 2K a0^2 v M_eff(I) with M_eff'(0)=1/2 and v=a^3 on Q=1 gives

Gamma_lambda=K a^3 P_lambda=Gamma_crit/(1+lambda delta^2),
Gamma_crit=M a^3 P_g P_h/(P_g+P_h).

For lambda=0 this is the harmonic candidate: the relative principal spatial stiffness vanishes. It is not a healthy sound-wave conclusion. Positive lambda moves strictly below the actual threshold when the scales differ.

The raw constrained action has auxiliary u,n_g,n_h and physical w,chi. Write g=M a^3 P_g H, j=M L b^3 P_h H2, alpha=g/(g+j), r=j/(g+j), T=gj/(g+j). Its independently reconstructed leading auxiliary solution, retaining a general positive Gamma, is

u=-alpha chi,
n_g=-r(dotchi+e w)-r(2alpha ell+T/Gamma)chi,
n_h=alpha(dotchi+e w)+alpha[ell(1-2r)+T/Gamma]chi.

Substitute into the raw action. The leading spatial action is -2T chi(dotchi+e w)-T(2alpha ell+T/Gamma)chi^2. Integration by parts must use Tdot/T=r(H-e)+alpha(2ell+H2), not a static snapshot. In the principal physical variable R=w+r chi one gets

L_principal=A dotR^2+E dotchi^2-g e R^2-S_lambda chi^2,
A=(3/2)a^3 W>0,
E=B r^2+D alpha^2>0,
B=M a^3 [3(1-eta)/eta]H^2,
D=M b^3 [3(1-eta)/eta]H2^2/L,
S_lambda=T(T/Gamma_lambda-rH-alpha H2)
        =lambda T(rH+alpha H2)delta^2.

Therefore both physical principal kinetic coefficients are positive and both gradient eigenvalues are positive when 0<eta<1, lambda>0 and a!=b on the positive-radiation branch. Radiation has omega^2=P_g/3. The relative mode has

omega_lambda^2=lambda P_g P_h(P_g-P_h)^2/
 {[3(1-eta)/eta](P_g+P_h)(P_h^2+P_g^2/L^2)}.

It is exactly minus lambda times the original arithmetic relative frequency. At the admitted initial fixture L=1/8, P_h/P_g=1/4 and eta=1/4, its c_rel^2=omega^2/P_g is lambda/5125. At equality of scales the relative gradient still vanishes. As eta tends to zero, the extra kinetic direction becomes singular; the original eta=0 constraint reduction cannot be substituted.

## What this result does not establish

The positive principal limit is not positivity at every finite k. The general auxiliary determinant has positive small-k leading Gamma ell^2(A+B)D and negative high-k leading -Gamma(g+j)^2 when ell!=0. The new Gamma therefore still has at least one intermediate rank-loss point in this elimination chart. The original constrained/canonical system must be analyzed there before a physical ghost or singularity can be inferred. This repair alone cannot be called fully healthy.

Nor does a small positive sound speed supply a conserved positive cold abundance, recombination history or structure transfer. Its dependence on mismatch, eta and lambda is explicit, not a parameter-free cosmological prediction. The C2 norm envelope and the prepared-node regularity issue are unchanged through cubic order at coincidence. Higher-order admission, nonlinear clock variations, exact static source corrections, and the general-dimensional matter calculation remain open. A and its normalization are untouched, so 32pi is still unexplained.

The next discriminating test is the canonical finite-k system at the auxiliary rank point for this actual geometric action. A second independent obligation is the modified static metric variation, since preserving the leading kernel is weaker than preserving the fitted full source solution.
