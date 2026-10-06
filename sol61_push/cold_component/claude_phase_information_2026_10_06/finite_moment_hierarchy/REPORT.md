# No exact finite instantaneous velocity-moment closure on this kinetic class

**Verdict: proved under the stated Newtonian kinetic hypotheses.** For every finite integer N>=0 there are positive phase-space initial densities with the same entire spatial fields of all polynomial velocity moments of degree <=N, and the same self-consistent potential/tidal field, whose rank-N moment time derivatives differ. Their spatial jets also coincide to every finite order. For N>=2 this directly includes the density, mean, full dispersion and tidal readers of Claude CFG354/355. It strengthens the parent eight/six-stream examples without editing their frozen inputs.

The class here is positive collisionless distribution initial data smooth inside the velocity support and C³ at the escape surface, not necessarily a finite cold-sheet distribution or a state of the actual CFG288 wave action. “Finite instantaneous fields/jets” means fields constructed from the declared finite polynomial velocity moments and their spatial derivatives, together with their common Newtonian density-sourced potential. It does **not** mean every conceivable finite observable, time derivative or time history.

## Construction and positivity

Use the exact parent Plummer equilibrium, with G=M=b=1:

`psi=(1+r²)^(-1/2), rho=3 psi^5/(4pi), Phi=-psi`,

`f0=24 sqrt(2)/(7 pi³) [psi-v²/2]_+^(7/2)`.

Let `ell=N+1`, `v_esc=sqrt(2psi)` and define the solid harmonic

`H_ell(v)=|v|^ell P_ell(v_z/|v|)`.

This is a homogeneous polynomial of degree ell; the expression at v=0 is its polynomial continuation. Define, for fixed 0<epsilon<1,

`f_epsilon(x,v)=f0(x,v)[1+epsilon H_ell(v)/v_esc(x)^ell]`.

On the common support `|v|<=v_esc`, `|H_ell/v_esc^ell|<=1`. Here is a self-contained bound for the Legendre polynomial, avoiding a quadrature hypothesis. The polynomial identity

`P_ell(mu)=(1/pi) integral_0^pi [mu+i sqrt(1-mu²) cos theta]^ell dtheta`

follows by binomial expansion, using odd cosine moments zero and `average cos^(2k)=binom(2k,k)/4^k`, then comparing the finite coefficients with the Rodrigues expression. Each complex integrand base has squared modulus `mu²+(1-mu²)cos²theta<=1`. Hence `|P_ell(mu)|<=1` for |mu|<=1. The polynomial identity is real after integration.

It follows that `(1-epsilon)f0<=f_epsilon<=(1+epsilon)f0`. Thus the perturbation is positive wherever f0 is, has exactly the same velocity escape support, finite mass and every finite velocity moment. The bound also applies with -epsilon. No negative distribution or change of boundary potential is used. The local polynomial factor is smooth at v=0 and x=0; the escape-surface regularity is C³, inherited from the 7/2 cutoff, sufficient for the initial weak transport identities. It is not a C-infinity distribution at that surface. Both distributions occupy strictly negative energy apart from their zero-density boundary. This is not an escape witness.

## Every retained Cartesian velocity moment vanishes in the difference

Let a,b,c be nonnegative integers with m=a+b+c<=N. On a velocity sphere write `v_z=|v|mu`, `v_x=|v|sqrt(1-mu²)cos phi`, `v_y=|v|sqrt(1-mu²)sin phi`. If a or b is odd, its azimuthal average is zero. Otherwise the angular integral of `v_x^a v_y^b v_z^c H_ell(v)` is a radial factor times

`integral_-1^1 q(mu) P_ell(mu) dmu`,

where `q(mu)=mu^c(1-mu²)^((a+b)/2)` times a real azimuthal constant, a polynomial of degree m<ell.

Rodrigues gives `P_ell=(2^ell ell!)^-1 d_mu^ell (mu²-1)^ell`. Integrating by parts ell times has no boundary contribution: `(mu²-1)^ell` and its derivatives through order ell-1 vanish at both endpoints. The surviving integral is proportional to q^(ell), which is zero. Thus

`integral v_x^a v_y^b v_z^c (f_epsilon-f0) d³v=0`

for every x. Density is the m=0 case, so the potential solving the isolated Poisson problem is exactly the same Phi in both initial states. All retained moment fields and their entire spatial derivative fields agree. For N>=1 centered moments through order N also agree, because they are polynomial combinations of the identical raw moments and mean. N=0 is only the density-level statement.

## The first invisible flux is nonzero and its divergence changes evolution

The next axial moment has a strictly positive coefficient. Integrating Rodrigues by parts for `q(mu)=mu^ell`, followed by an elementary beta integral, gives

`average_sphere [mu^ell P_ell(mu)]=c_ell=2^ell(ell!)²/(2ell+1)!>0`.

The parent equilibrium's radial velocity law is `u=|v|²/(2psi)~Beta(3/2,9/2)`, checked from the defining density integral. Therefore

`Delta M_(z...z) [ell indices] =epsilon D_ell(r)`,

`D_ell=rho (2psi)^(ell/2) c_ell B(ell+3/2,9/2)/B(3/2,9/2)>0`.

Its radial dependence is exactly `(1+r²)^(-(10+ell)/4)`. The components `Delta M_(z...z x)` and `Delta M_(z...z y)` with ell-1 z indices vanish by angular parity. The raw Vlasov moment equation is

`M_(i1...im)_dot+partial_k M_(i1...im k)+sum_a Phi_,ia M_(i1...omit ia...im)=0`.

Take m=N=ell-1 and every retained index z. All force terms agree because they use retained lower-degree moments and the common potential (for m=0 there is no force term). Hence

`Delta M_(z...z)_dot = -epsilon partial_z D_ell(r)`

`=epsilon (10+ell) z D_ell(r)/[2(1+r²)]`.

At x=(0,0,1) the derivative difference is exactly

`epsilon (10+ell) D_ell(1)/4>0`.

It remains nonzero on an open set z!=0. This is a direct evolution discriminator, not merely a different high-order number. The equilibrium has every time derivative zero; the perturbed initial state is nonstationary. The force signs follow by integrating `-Phi_,k partial_vk f` by parts. No prescribed switch, relaxation time or phenomenological pressure law was used.

## Scoped closure consequence

Suppose an exact deterministic instantaneous closure assigns all retained moment time derivatives from these finite retained moment fields, any finite spatial jets of them, and their common density-sourced potential/tidal data. The two initial states give identical closure inputs everywhere, so the assigned outputs must coincide. The displayed actual Vlasov derivative differs; the closure fails for at least one state. This proves the obstruction for **each finite N** within the declared class. It even defeats arbitrary spatial nonlocal functions of the retained fields, since the entire fields match. It does not defeat a closure endowed with additional phase-space data or an initial-history restriction.

This does not establish that all finite observable classifiers of equilibrium fail, that the states have identical histories, or that a particular caustic/growing-mode-restricted campaign must contain these perturbations. It also does not transfer the theorem to a wave action, GR momentum constraints, collisional gas, or a source-reaction-modified cold force. A same-action kinetic completion can choose restricted data, but must justify that restriction and its evolution. The missing physical datum is the unresolved velocity-space transport flux; merely adding the next finite moment repeats the hierarchy question one level higher.

## Provenance and bounded checks

The separate parent SOURCE_PROVENANCE.json pins the actual Claude345/354/355 files and prior bulk-phase argument. This child source registry also pins the frozen parent report/checks, the registry, and root's review. No parent or Claude input is edited or executed. No external named orthogonality/quadrature theorem or literature novelty assertion is used; the angular identities are derived above.

The universal proof is analytic. The exact code independently expands solid harmonics, verifies their velocity Laplacian, integrates every retained Cartesian monomial by sphere gamma moments, checks the first nonzero coefficient, the Legendre boundedness representation, and the nonzero flux divergence for N=0,...,8. This finite range verifies implementation, not arbitrary N. Main and degree/flux controls preserve stdout, stderr, actual inputs and outputs under the standard computation-audit runner. Wall/CPU/log limits are 60s/45s/100000 bytes, with one cooperative numerical-library thread; no hard memory/affinity cap. The degree control substitutes ell-1 and must expose retained moments; the flux control deletes the next moment and must lose its positive derivative. Run counts and final validation are recorded separately in VALIDATION.md.
