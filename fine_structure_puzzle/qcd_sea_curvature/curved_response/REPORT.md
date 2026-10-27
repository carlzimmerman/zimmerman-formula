# FSP-007 curved QCD response result

A new, evaluated low-energy contribution is available: the unconditioned
two-pion cut of QCD's vacuum trace response and its nonlocal scalar
gravitational form factor. The full A_rho and R(alpha)=A_rho/m_p^3 remain
unevaluated.

The LO massive-pion result is

    rho_Theta(s)=sum_a (s+2 M_a^2)^2 sqrt(1-4 M_a^2/s)/(32 pi^2),
    integral ds rho_Theta(s)/s^4
       =17/(2240 pi^2) sum_a M_a^(-2).

The report also gives an explicit finite-cutoff formula, so using this
as a low-energy QCD contribution requires no LO extrapolation into the
UV. In a three-times-subtracted, weak conformal-source response it
produces, for each real pion, the dispersive term

    W_hat^(2)=17/(161280 pi^2 M^2) integral R(-partial^2)R+... .

The discontinuity is scheme independent. The coefficient above is the
defined dispersive matter contribution: an independent local R Box R
term in a full gravitational EFT can change its total local coefficient.
The leading inverse-mass singularity is fixed by the pion cut; the
complete physical-mass moment needs higher orders and the QCD tail.

The charged-pion mass-shift component is calculated at finite e^2 with
M0^2=M^2 and Mplus^2=M^2+2e^2C/F^2, holding declared strong inputs fixed.
It yields

    M3_mass(e^2)=17/(2240 pi^2)[1/M^2+2/(M^2+2e^2C/F^2)].

This includes the mass change of the trace vertex as well as phase
space. It is not the complete electromagnetic response.

The primary source Kubis--Meissner,
[hep-ph/9908261v2](https://arxiv.org/abs/hep-ph/9908261v2), including the
2001 correction, identifies the independent curvature operator k15 in
(4.7), its beta function in (4.8), and the charged-pion trace form factor
in (5.12). The latter has photon loops, infrared terms and an independent
k15 contribution beyond the shifted mass. With the explicit charge
normalization audited in DERIVATION.md, the isolated k15 insertion into
the moment has coefficient 3 k15^r/(10 pi^2 M^2) per e^2 derivative, whereas
the mass piece is -17 C/(560 pi^2 F^2 M^4). The k15 contribution is a
higher-order, scale-dependent component until its accompanying loops
are included. An inclusive radiative spectral function is required.

Metric seagulls and all mixed metric/current contacts are retained by
regulated source differentiation; the exact three-source identity is
recorded in the derivation. A susceptibility, a proton matrix element,
or an exclusive mass split does not supply that vacuum response.

These results cannot be converted into a linear-H sphere energy by
setting momentum equal to H. On round S4, R is constant and the calculated
R Box R term vanishes. The k15 homogeneous pion tadpole starts at R M^2,
then R^2 and higher local powers, hence H^2,H^4,H^6,... at fixed positive
masses. It supplies no tunable linear-H coefficient. The flat quadratic
calculation does not determine the global one-point vacuum functional,
curvature-cubic terms or a nonuniform global remainder. No zero-charge,
chiral and H limits are interchanged.

The concrete next check is a common-regulator unconditioned trace
correlator, its metric seagull, and the finite third dispersive moment
at several positive quark masses. The two-flavor leading chiral
prediction is M^2[-Pi_E'''(0)/6] -> 51/(2240 pi^2). For its charge
dependence, the independently needed finite k15 can be matched through
the charged-pion trace slope using (5.12), including photon/strong terms.
Neither check is a substitute for the target datum: the full-charge
one-point integrated stress on the specified globally curved ensemble.
A bounded primary search found no new unquenched curved-QCD stress data
that supply it.

Verification: the dependency-free script passed exact rational
normalization checks, five bounded-cutoff integrals and 20 independent
dispersion/Feynman kernel comparisons. Maximum absolute kernel difference
was 4.55e-15. No measured alpha, cosmological scale, physical hadron mass
or fitted LEC was inserted. See DERIVATION.md, SOURCES.json, INPUTS.json,
checks/RESULTS.json and checks/MANIFEST.json for the reproducible evidence
and its limits. This is a calculated component with a precise remaining
global-response input, not a physical prediction of R(alpha).
