# FSP-010 hard proton result

The full renormalized physical proton derivative M_u remains open. This
package calculates a previously unspecified finite quark matching term
and a genuine new lattice-data functional in a declared harder photon
window. Neither partial result is a complete hard proton mass.

The older FSP-007 result already included the scalar full-tensor hard
shell, its isoscalar gluon contribution, and the UV logarithm cancellation.
Those are not rediscovered here. The changed matching step is the finite
sharp-O(4)-photon-cutoff to MSbar quark-mass conversion at leading strong
order:

    M_u,ct^q = sum_f Q_f^2 sigma_f^p
       [3 log(mu^2/Lambda^2)+5/2]/(16 pi^2) + O(alpha_s).

The 5/2 follows from subtracting the sharp complete Dirac loop finite
constant 3/2 from the independent dimensional/MSbar constant 4. Matching
is on an elementary external quark; Feynman-Hellmann then transfers the
local mass insertion to a proton scalar matrix element. This does not
replace the proton's nonlocal current tensor by a Dirac particle. The
complete derivation and limitations predate execution in DERIVATION.md.

Using the explicit continuum sigma calibrations of
[Alexandrou et al., 2412.01535v1](https://arxiv.org/abs/2412.01535v1),
Tables VI/VIII, and the MSbar(2 GeV) light mass calibrated in
[2104.13408v3](https://arxiv.org/abs/2104.13408v3), gives

    sum_(u,d,s,c) Q_f^2 sigma_f^p = 52.0711466667 MeV,
    finite M_u,ct^q(mu=Lambda) = 0.8243609709 MeV per e^2.

The linearized covariance-agnostic marginal-error ceiling for the latter
is 0.2729073064 MeV per e^2, conditional on the stated cross-source
common-path identification. This is not a total theory uncertainty.
The inputs include sea scalar contractions, empirical scale and quark
mass calibrations, correlator fits, renormalization and continuum/model
averages. It is a source-calibrated leading matching term, not a no-fit
ab initio proton prediction. No numerical alpha enters the transformation.

Equivalently the leading-power quark Wilson tail has the factor
[3 log(mu^2/Q0^2)+5/2]. Thus taking mu=Q0 removes the logarithm but does
not remove this finite quark term. No finite numerical Q0 is asserted to
make the active-charm mass powers, QCD power terms or higher strong
orders negligible. The independent finite gluon matching coefficient,
mixed quark corrections and threshold matching remain essential.

## New 2026 finite-momentum data

[2507.20910v2](https://arxiv.org/abs/2507.20910v2), revised 30 June 2026,
supplies new multi-state/AIC extractions at three lattice spacings. Its
Tables XVI-XVIII give finite-a nodes; its Table XX continuum results are
fitted functions. Equations (5)-(6) use only the light electromagnetic
current (2 j_u-j_d)/3. The Nf=2+1+1 gauge sea does not supply absent
strange/charm electromagnetic-current insertions.

The executed functional uses the complete Born angular kernel, including
its non-pole Dirac term, and integrates its nodal piecewise-linear
interpolant only over 0.56 <= Q^2 <= 0.88 GeV^2. For the declared common
calibration m_ref=0.9389 GeV, K_tab=M_u,B/m_ref per e^2 is:

| Source ensemble | a (fm) | K_tab, full light current | Change from light disconnected elastic matrix elements |
|---|---:|---:|---:|
| cB211.072.64 | 0.07957 | -0.0003343715368 | +0.0000277095520 |
| cC211.060.80 | 0.06821 | -0.0004164176385 | +0.0000242478177 |
| cD211.054.96 | 0.05692 | -0.0004332606994 | +0.0000213715900 |

No new fit or extrapolation is applied. These are literal tabulated-data
functionals, not error-controlled continuous band integrals or a new
continuum extrapolation. Negative values are permitted: the complete
Born tensor contains the regular Dirac subtraction and Pauli terms.

The first-order marginal-error ceilings for full-light K are respectively
0.0002201518, 0.0001798461 and 0.0001376164. For the disconnected differences
the ceilings are 0.0004618110, 0.0003800696 and 0.0002967379. Consequently
the displayed positive disconnected changes are not sign-resolved physical
measurements here. The source provides no joint nodal covariance. These
ceilings are not nonlinear errors, interpolation errors or complete
finite-volume/continuum/mass-matching errors. The change of a quadratic
elastic functional is not the complete two-current sea covariance.

The reference mass is an empirical calibration, not a matched finite-a
QCD mass. Mass sensitivity controls are preserved in result.json. Using
the actual B64 mass 0.9440(44) GeV from the new
[2610.20362v1](https://arxiv.org/abs/2610.20362v1) study gives
K_tab=-0.0003271171267 and a linearized mass-error effect 0.0000062008.
This cross-source control discloses the small scale difference between
the two source analyses. That October 2026 source also examines residual
sigma excited states and quotes finite-a retuned B64 values; it does not
silently supersede the continuum sigma calibration above.

The source Appendix D prose describes 50 bins in [0,1), while the printed
Tables XVI-XVIII give 21 irregular nodes and B extends above 1. This
package uses literal printed/TeX nodes, visually checked for Table XVIII,
and does not infer unprinted raw bins or their covariance.

## Execution and remaining physical step

Authoritative record: run_001/manifest.json, real bounded runner schema v2,
status completed. Installed manifest validation passed; all 16 pre-execution
pins remain unchanged. The 38 counted controls include nine independent
angular contractions, 18 analytic-gradient checks, exact rational clipped
quadrature/charge/flavor/logarithm checks and the sharp-cutoff asymptotic
primitive. Interpretation remains conditional on source calibration and
the declared matching order. No earlier scientific artifact was changed.

The finite quark conversion is now specified at leading strong order.
The next matching calculation must determine the finite gluon/strong
parameter conversion and mixed scalar-quark corrections in this same
photon prescription and MSbar path. Hill-Paz's four-dimensional gluon
coefficient and the trace anomaly alone do not provide the required
evanescent terms and scalar-operator mixing for that finite conversion.
The full mass also still needs the complete all-current proton tensor,
the non-Born and low/intermediate parts, all sea classes, common mass
retuning and controlled limits. The curved vacuum A_rho is independent.
No value of R(alpha), full M_u, finite-alpha response or alpha selection
equation is obtained by adding these partial sectors.

Exact sources/versions/byte hashes are in SOURCE_RECEIPTS.json, input
decimals in INPUTS.json, ancestry in ANCESTRY_PINS.json and regeneration
commands in REPRODUCE.md. The run is self-audited; independent source-first
review is requested before the coordinator relies on the new matching
transfer or data interpretation. Mechanical v2 validation does not supply
that physical review.
