# What the calculable sea ultraviolet logarithm can determine

FSP-007, parent FSP-006. Coordinator derivation; no measured alpha or QCD coupling is inserted. This calculation separates a genuine mixed-QCD/QED ultraviolet effect from a putative prediction for a dimensionless infrared ratio.

## Mixed running, with explicit convention

Use u=e^2, g=g_s and rational quark charges Q_f, S_Q=sum Q_f^2. In the source's MS-bar coupling convention, a fixed active-flavor window, and t=log(mu/mu0), the first mixed coefficient gives

dg/dt=-b0 g^3/(16pi^2)+2S_Q u g^3/(16pi^2)^2+pure two-loop QCD and higher terms,
b0=11-2n_f/3.

Primary source: Billis–Tackmann–Talbert, arXiv:1907.02971v2, equation (2.11), (A.10), charge definition (A.13): beta^s_01=-4T_F S_Q=-2S_Q, T_F=1/2. Only its mixed strong coefficient is used here. QED running changes u only at O(u^2), so u is constant for the leading derivative at u=0. Threshold conversion, finite matching and higher strong orders are not discarded in a physical prediction; they are outside this explicitly truncated check.

Writing y=1/g^2, the retained equation is exactly

y(t)=y0+[b0/(8pi^2)-S_Q u/(64pi^4)]t,
partial_u y(t)|y0=-S_Q t/(64pi^4).

The sign is physical: for downward evolution t<0, turning on positive u at fixed UV g makes y larger (g smaller), in this retained approximation. The formal one-loop pole scale has

log(Lambda_pole/mu0)=-8pi^2/[g0^2(b0-S_Q u/(8pi^2))],
partial_u log Lambda_pole|0=-S_Q/(b0^2 g0^2).

The pole is a formal integration constant/proxy, not a perturbatively reliable calculation of confinement. The large logarithm cannot be used as an accurately known hadronic response. The exact weak-window running check does not continue the beta function through strong coupling.

To keep a low-scale coupling at a fixed weak matching scale unchanged while varying u, the boundary coupling must retune:

partial_u g0= -S_Q g0^3 t/(128pi^4).

Together with this boundary tangent, the mixed contribution to partial_u y(t) cancels exactly at that matching scale. This is a check of the local strong-counterterm direction, not a cancellation of the complete finite sea response.

## Matching projection and the physical ratio

Let ell=log Lambda denote one matched non-electromagnetic scale coordinate and h_i the held quark-mass coordinates. Let M be the flat proton threshold, A=A_rho the physical curvature coefficient if it exists. The fixed-proton derivative is

(dR/du)_(M,h)=[A_u-(M_u/M_ell)A_ell]/M^3,

on a regular branch M_ell nonzero. If a renormalization or UV-matching contribution is purely a change delta ell=k delta u at fixed h, then its changes obey A_u=k A_ell, M_u=k M_ell. Its contribution to this constrained ratio derivative is zero exactly. No assumption A nonzero is needed. If the corresponding quark-mass conversion is not held fixed, scalar insertions must also be included before applying this statement. The mixed strong beta coefficient alone does not supply all of that mass conversion.

More generally, for calibration observables M_b and matched parameters lambda_a, let J_ba=partial_a M_b. A scheme/boundary change k_a in that parameter tangent changes the unprojected vacuum derivative by k_a partial_a A and the calibration derivative by J_ba k_a. The projected derivative

A_u-(partial_a A)(J^-1)_ab partial_u M_b

is unchanged. This is why the calculable UV mixing and its counterterm must agree between proton and vacuum calculations. It is not a mechanism selecting u. The remaining finite current insertion is independent of these local parameter directions and still requires QCD matrix elements.

The logarithm is not the missing low-momentum same-loop sea covariance. Even at SU(3)-degenerate masses where the sea insertion is a flavor singlet, no identity equates the whole photon-mediated determinant to the strong-scale insertion. That would be an additional, unjustified dynamical premise. Finite sea response can remain after the local UV term is matched.

## The actual scalar UV term and its ratio cancellation

The sea-OPE lane independently evaluates the full photon angular integral and the leading gluon scalar operator. The counterterm normalization can also be checked directly from Gasser et al., arXiv:1506.06747v3, equations (56),(57),(64). Its rescaled field square is O_G=g^2 G_canonical^2. The source's counterterm symbol is

delta g/u=-g^3 S_Q log(Lambda_UV^2/mu^2)/(256pi^4).

It is essential that the mass counterterm is -delta g partial_g M, rather than +delta g partial_g M. The source Lagrangian inserts -delta g partial_g L. In a fixed-n_f massless theory the leading anomaly gives partial_g M/M=16pi^2/(b0 g^3), hence the scalar loop ultraviolet coefficient is

(partial_u M/M)_UV = -S_Q log(Lambda_UV^2/mu^2)/(16pi^2 b0),

and its counterterm has the opposite sign. This is not a finite complete proton mass: the separation is regulator/matching dependent. For three massless flavors the logarithm's coefficient is -1/(216pi^2); a shell Q0<|Q|<2Q0 has asymptotic loop contribution -log4/(216pi^2). Spin-two subtraction pieces cannot be added as uncanceled full-mass logarithms; the full angular tensor is necessary.

If the target A exists in this massless theory and scales as Lambda^3 at zero charge, the same local strong-parameter direction gives (partial_u A)_UV=3(A/M)(partial_u M)_UV. Therefore

(partial_u R)_UV = (partial_u A)_UV/M^3 - 3A (partial_u M)_UV/M^4 = 0.

This identity also holds at A=0 by its unlogged form. It is a calculable cancellation of a shared UV contribution, not a calculation of R or of its finite infrared derivative. At nonzero masses use the full calibration projector and mass counterterms above; the simple factor-three argument alone is insufficient. No nonlocal sea response was removed by assumption.

## Why one measured sea moment cannot finish the convolution

The sea-data lane obtains a low-momentum derivative of a particular Euclidean Compton function. For a transparent inverse-data test, consider a scalar Stieltjes function C(z)=sum_i r_i/(s_i+z). Its value and initial slope fix sum r_i/s_i and sum r_i/s_i^2; its leading high-z coefficient fixes sum r_i. These three constraints do not fix a photon-weighted integral. For example, with s=(1,2,3,4) in one declared unit, the variation delta r=(-1,12,-27,16) has sum delta r=0, sum delta r/s_i=0, and sum delta r/s_i^2=0. Yet the convergent difference of integrals from z=0 to infinity equals

delta integral C(z) dz=27log3-44log2, which is nonzero.

A positive baseline r=(40,40,40,40) remains positive for both signs of a sufficiently small variation, so even positivity alone would not remove this example. In the actual sea contribution the vacuum-subtracted baryon covariance does not have a positive spectral measure, making a naive positivity bound still less justified. This counterfamily proves only insufficiency of these three scalar moments; it is not a family of microscopic QCD theories or a substitute for the full Compton tensor, its Ward identities, energy dependence or threshold constraints. No source's measured moment is fitted with it. It explains exactly why a new sea datum can constrain a calculation without determining the complete mass integral.

## Evidence limits

The bounded exact-arithmetic check derives the coupling conversion, weak-window solution, matched cancellation and moment counterexample independently of numerical alpha. No phenomenological beta-function integration, confinement-scale extraction, full sea mass, curved vacuum coefficient or ratio is evaluated. Exact source byte hashes, corrected version and checked locators are recorded in SOURCES.json. The initial sandbox DNS failure and successful public refetch are acquisition observations, not physics results.
