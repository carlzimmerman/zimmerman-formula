# Metric response and a direct, unfitted definition of the QCD coefficient

Parent FSP-002, phase FSP-003. Coordinator hand derivation. This is an operational reduction of the desired coefficient to a specified QCD+QED observable; it does not evaluate that observable.

## A round-sphere prescription

Choose the ordinary smooth Euclidean QCD+QED theory on the closed round S4 of radius a=H^-1, with a specified regulator, full charge and quark-mass matching, theta, and the regular-state analytic continuation if used. Let W(H)=-log Z(H), V4=Omega4 H^-4, Omega4=8 pi^2/3, and f(H)=W/V4. Keep renormalized physical comparison data fixed when varying the metric.

Under a uniform scale change, delta g_ab=2 delta log(a) g_ab. Define the Euclidean stress by delta W=(1/2)int sqrt(g) T_E^ab delta g_ab. For an invariant state, T_E^ab=rho_E g^ab, and therefore

rho_E=(1/(4V4)) dW/dlog(a)
=f-(H/4) df/dH.

This sign convention assigns rho_E=f to a constant potential. Its analytic continuation gives the corresponding invariant Lorentzian vacuum energy if that continuation/state exists. The relation uses all metric-dependent determinants, measure and matching terms. It is not obtained by regarding H as an external fixed-temperature number during the metric variation.

In particular, f=A_f H gives rho_E=(3/4)A_f H. More generally a power H^n contributes (1-n/4)f. Thus a coefficient in -log Z / volume and the gravitating linear-H coefficient are distinct. This is a test for the specified round-sphere prescription, not a universal factor to attach to the source's hyperbolic thermal ensemble. The latter has independent circle/space/boundary variables, and values on one diagonal do not determine the required partial metric variation.

## Remove local subtraction terms without fitting them

At fixed input data, write D=H d/dH and P(D)=D(D-2)(D-4). Finite local bulk vacuum/gravity counterterms through curvature squared restrict on a round sphere to shifts f -> f+b0+b2 H^2+b4 H^4. Hence P annihilates them exactly. If f has a differentiable asymptotic expansion with a unique linear term and only higher regular/logarithmic terms,

A_f = lim_(H->0+) P(D)f(H)/(3H),
A_rho = lim_(H->0+) P(D)rho_E(H)/(3H) = (3/4)A_f.

The factor 3 is P(1)=1*(-1)*(-3). Terms such as H^4 log H and higher analytic powers vanish after the displayed division and limit. A hypothetical H log H term would not define a finite constant A_f; its limit must be tested, not assumed. The operator is a formal observable requiring derivatives/convergence control; numerical derivatives on noisy data are not automatically a successful measurement.

A chosen boundary-free microscopic theory could therefore calculate the nonanalytic coefficient without fitting local cosmological or Newton counterterms. Ordinary local counterterm freedom is not by itself an arbitrary freedom to add H Lambda^3. Whether QCD produces this term is still a dynamical question. Analytic local curvature expansions have A_rho=0, but this alone is not a proof about every proposed global topological response.

## First electromagnetic derivative as an actual path-integral insertion

After integrating the canonically normalized photon at a fixed regulator, write

S_eff=S_QCD+e^2 I_g+O(e^4),
I_g=(1/2) int_(x,y) J_mu(x) D_g^(mu nu)(x,y) J_nu(y)+I_g^ct,

where the counterterms implement the chosen renormalized quark-mass/strong convention and the local gravitational subtraction. For the Euclidean Dirac convention S_int=i e int A.J, Gaussian photon integration gives the positive e^2 I_g in S_eff. All disconnected, sea and valence contractions are part of the expectation. A specified charged-state infrared prescription is required for the proton.

Then

partial_(e^2) W = <I_g>,
partial_(e^2) f = <I_g>/V4,

partial_(e^2) rho_E
=[1-D/4](<I_g>/V4).

If the relevant derivatives and small-H limit can be interchanged,

partial_(e^2) A_rho
=lim_(H->0+) P(D)[1-D/4](<I_g>/V4)/(3H).

At fixed matched quark and strong data this is the geometric current-current insertion actually needed; a flat theta-susceptibility insertion alone is a different observable. A photon normalization factor or current-charge convention must be treated consistently rather than silently used to fix alpha.

For a proton correlation C_p(T)=<N_p(T) Nbar_p(0)>,

partial_(e^2) m_p
=lim_(T->infty) [<N_p(T)Nbar_p(0) I_flat>/C_p(T)-<I_flat>]/T,

with matched endpoint/contact and infrared prescriptions. This follows from differentiating the normalized path integral and extracting the large-time rest threshold. It is not determined by a proton-neutron difference alone. The EM agent independently derived the same insertion signs and physical-sector distinction.

The ratio asked for is R=A_rho/m_p^3, not the similarly dimensioned susceptibility or A_f. Physical alpha uses e^2=4 pi alpha with threshold/charge matching. When the measured proton mass is fixed by retuning the strong scale, its derivative must be eliminated with the matching Jacobian, as in the prior constrained-sensitivity note. A fixed-MSbar-mass path additionally requires its declared reference scale; fixed-invariant masses are a different path until converted.

## What this accomplishes

This identifies a coefficient and its EM derivative that could be measured from a common regulated QCD+QED generating functional without using observed alpha or dark energy as a fit target. None of the present finite Maxwell, Schwinger or deformed-QCD calculations evaluates this four-dimensional observable. A future lattice/functional calculation needs a specified state/geometry, controlled regulator and size limits, complete matching and uncertainty estimates. The requested physical R(alpha) therefore remains uncalculated.

External basis: the current-current perturbative expansion is checked by the electromagnetic route against de Divitiis et al.1303.4896v1; the metric relations here are independently derived from delta W and sphere scaling. No external source is claimed to have established the proposed QCD small-H limit.
