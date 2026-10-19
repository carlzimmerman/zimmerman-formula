# Closed four-form contact sector and its compact singlet

FSP-004 coordinator derivation, 2026-10-19 UTC. This is an explicitly defined effective model, not a derivation of the QCD generating functional. Natural units. No experimental alpha or cosmological value is used.

## 1. Action, measure, and source translation

Let C be a compact abelian three-form connection on a smooth, oriented, closed round S4. Write V=8 pi^2/(3 H^4), integral F=2 pi Q with Q integer, and

    S = (1/(2 q^2)) integral F wedge *F - i theta Q,
    q^2 = 4 pi^2 chi_g,  chi_g > 0.

chi_g has mass dimension four. It is a matched susceptibility parameter, not a computed QCD number. The harmonic representative has action Q^2/(2 chi_g V). All couplings are held fixed during metric variation. There are no charged membranes, extra three-forms, boundary states, or curvature-dependent matching terms in this action.

Donnelly–Michel–Wall 1611.05920v1, equations (2.9), (2.14), (2.18)–(2.19), give the compact p-form oscillator, harmonic gauge-volume, and flux factors. Their q and mu are used without rescaling; apply their partition formula at p=3, D=4. No assertion about a negative-degree electromagnetic dual is needed. Dvali hep-th/0507215v1, section 4, equations (36)–(44), identifies the QCD Chern–Simons three-form and motivates this contact description. His general function K(F) is explicitly unknown; choosing its quadratic term here is an extra effective-model assumption.

For p=3 the nonzero-mode product is

    Zosc = det'(Delta3/mu^2)^(-1/2) det'(Delta2/mu^2)
           det'(Delta1/mu^2)^(-3/2) det'(Delta0/mu^2)^2.

Write Cj for the determinant on coexact j-forms. The Hodge decomposition gives det' Delta_j=Cj C_(j-1). Hodge duality of exact/coexact nonzero spectra on a closed four-manifold gives C3=C0 and C2=C1. Thus the displayed product cancels exactly in a shared spectral regulator, not just at a fixed angular momentum. On S4 only b0=b4=1; the three-form gauge hierarchy leaves

    Zzero = q/(sqrt(2 pi) mu^4 sqrt(V)).

There is no torsion. Combining this with the flux sum gives a fixed metric-independent factor q^2/(2 pi mu^4) times the following normalized partition. This factor can be divided out for this fixed-coupling metric question; it must not be silently discarded for a question about coupling-dependent absolute normalizations.

## 2. Exact contact partition and stress

Poisson summation gives

    Ztop = (2 pi chi_g V)^(-1/2)
           sum_Q exp[-Q^2/(2 chi_g V) + i theta Q]
         = sum_k exp[-V chi_g (theta+2 pi k)^2/2].                (1)

The invariant metric stress of this volume-only functional is rho=-d_V log Z. Equivalently f=-log(Z)/V and rho=f-(H/4)d_H f. Equation (1) therefore gives

    rho_top = <chi_g (theta+2 pi k)^2/2>_k.                     (2)

At theta=0, rho_top=4 pi^2 chi_g exp[-2 pi^2 chi_g V] plus smaller exponentials. The flat-branch energy is zero and the coefficient of H is exactly zero in this specified compact Gaussian contact sector. Nevertheless its infinite-volume topological susceptibility is chi_g, since -d_theta^2 log(Z)/V tends to chi_g near theta=0. Nonzero contact susceptibility and a linear-H vacuum term are different assertions.

Keeping the Q sum while omitting the gauge-volume factor multiplies Z by sqrt(2 pi chi_g V). It changes the stress by -1/(2 V). That is a spurious H^4 term, not an H term. At theta=pi the two equal lowest branches only contribute a metric-independent degeneracy at leading order. The theta-to-pi and infinite-volume susceptibility limits need separate treatment; the theta=0 results do not use that cusp.

More generally, if a specified contact Hamiltonian has volume-independent energy densities E_k(theta), then Z=sum_k exp(-V E_k) gives rho=<E_k>. A positive density gap above the lowest branches gives exponentially small finite-volume stress. This is a conditional statement about that Hamiltonian and its measure, not a general mass-gap theorem for QCD on a horizon background.

## 3. Compact singlet constant mode: avoid an artificial massless divergence

To test axial screening, define a compact singlet phi of period 2 pi, kinetic coefficient f_s^2, and a periodic mass-pinning potential B(1-cos phi), B>=0. Here B is a separate matched parameter of dimension four, not a baryon mass. The anomaly coefficient is one by definition of this model. For its constant mode, use the canonical coordinate f_s sqrt(V) phi and measure mu d(f_s sqrt(V) phi)/sqrt(2 pi). After integrating the contact sector, the exact constant-mode partition is

    Z0 = mu f_s sqrt(V/(2 pi)) sum_k integral_[-pi,pi] dphi
         exp{-V[B(1-cos phi)+chi_g(theta+phi+2 pi k)^2/2]}
       = mu f_s sqrt(V/(2 pi)) integral_R dx
         exp{-V[B(1-cos x)+chi_g(theta+x)^2/2]}.                (3)

This is a definition of the smooth constant-mode model. Compact field shifts and the branch label are identified by unfolding once. Replacing the periodic mass term by a quadratic function on the entire real line and then summing all branches would overcount shifts and give a false divergence as B tends to zero.

Fourier expansion of the periodic factor yields an orthogonal exact representation,

    Z0 = (mu f_s/sqrt(chi_g)) exp(-BV)
         sum_n I_n(BV) exp[-n^2/(2 chi_g V)] exp(-i n theta).   (4)

For B=0, (3)–(4) give Z0=mu f_s/sqrt(chi_g), independent of theta and V: the theta susceptibility and this constant-mode stress both vanish. This is finite axial screening, without a singular sum of identical vacua.

For theta=0 and fixed positive B, set a=chi_g+B. A Laplace expansion about the unique absolute minimum x=0 gives

    Z0 = (mu f_s/sqrt(a)) [1+B/(8 a^2 V)
          +(35 B^2/(384 a^4)-B/(48 a^3))/V^2+O(V^-3)],
    log Z0 = log(mu f_s/sqrt(a)) + B/(8 a^2 V)
             +(B^2/(12 a^4)-B/(48 a^3))/V^2+O(V^-3),
    rho0 = B/(8 a^2 V^2)
           +2(B^2/(12 a^4)-B/(48 a^3))/V^3+O(V^-4).           (5)

The canonical sqrt(V) cancels the saddle width. The first constant-mode correction to stress scales as H^8, not H. Gaussian moments give this expansion independently of the Fourier representation. At theta=0 the exact finite-volume susceptibility can be calculated either as the n^2 average in (4) divided by V, or as chi_g-chi_g^2 V <x^2> in (3). Its large-volume value is

    chi_screened = chi_g B/(chi_g+B),
    M_s^2 = (chi_g+B)/f_s^2.                                  (6)

Equation (6) is the local small-theta curvature of the minimized potential, not a full multi-flavour QCD matching prescription.

## 4. Nonconstant singlet and matching limits

In the local quadratic approximation the singlet contributes one real scalar determinant det[(-Box+M_s^2)/mu^2]^(-1/2), including its constant eigenfunction. The constant part of this determinant is mu/M_s, exactly the leading factor in (5). Thus an explicitly defined Gaussian-plus-exact-constant-mode approximation multiplies the full determinant only by Z0/(mu/M_s). Multiplication by Z0 itself would duplicate the constant eigenfunction. This construction does not include the interactions of nonconstant singlet modes or domain walls.

For fixed M_s>0 and H/M_s tending to zero, the covariantly subtracted ordinary scalar determinant has the already established FSP-003 stress a3 H^6/(64 pi^2 M_s^2)+O(H^8/M_s^4), a3=74/63. It contributes no H term in that regime; the extra factor (5) starts at H^8. Taking a light-mass limit at fixed H requires the original compact integral or another controlled effective expansion, not this massive asymptotic formula.

An arbitrary multiplicative exp[-V E_match(H,alpha)] remains invisible to normalized theta correlators. Equations (1)–(6) do not determine E_match, curved hard matching, quark/proton parameters, or electromagnetic charge normalization. In particular, no physical R(alpha)=A_rho/mp^3 or alpha root follows. In this model, at fixed positive matched parameters the linear-H coefficient is zero; varying those fixed parameters with alpha does not manufacture a nonzero slope of that coefficient. This does not establish a full-QCD no-go. It identifies the metric matching/global-state input that a successful topological QCD proposal must supply beyond this compact contact sector.
