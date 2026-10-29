# VR28 adversarial self-review

Primary claim audited: the stated PN28/VR28 local equilibrium, positive
scalar energy, vacuum stationarity/stability, and internal symmetry inputs
select a unique positive stiffness/full-vacuum ratio.

**Verdict: refuted, with an explicit continuous counterfamily.**
This is a self-review by the author /root, not an independent-agent audit or
formal certificate. Exact reviewed file hashes are in VERIFICATION.json.
The verdict is confined to these hypotheses; no general impossibility of
microscopic selection is asserted.

## Dependency reconstruction

U and Z plus a selected canonical state -> local stationary energy -> total
pressure -> reduced enthalpy -> Newtonian halo core -> adopted acceleration
dictionary. The last dictionary is a separate physical assumption.
Vacuum value and curvature enter different derivatives. Extra equations
relating them, exact scaling of the full effective action, state selection,
and a covariant completion are not supplied by that chain.

## Obligation matrix

| Obligation | Result | Reason |
|---|---|---|
| Unique full B/V under current assumptions | Failed | U+C preserves internal symmetries and minimally coupled local scalar health but changes the ratio in an open de Sitter interval. |
| B_curv/V_sector=delta under the stated scaling equation | Passed conditionally | Directly solve A_s=-3delta A, A=U_s-3U and impose stationary positive vacuum; U_ss(0)=9delta V_sector. |
| Physical selection of delta or exclusion of C | Not addressed by that equation | Both require additional microscopic information; declaring the equation is not deriving a Ward identity. |
| Full local pressure and scalar uniqueness | Passed | U_ss>0 and K exp(-2s)>0 make W strictly convex and coercive; P=U_s/3-U at the minimum. |
| Identification of B_curv with dense log slope for delta>0 | Failed | The exact pressure derivative tends to zero; the nonzero constant slope exists only in the subtracted delta=0 limit. |
| Reduced finite matter radius | Passed within stated model | n>=psi^(3/2), bounded n below central enthalpy, and the m/r versus 9/r^4 contradiction give finite edge and mass. |
| Dense-core scaling and crossing | Passed within stated model | The exact central source and derivative have uniform compact limits; the limiting quarter crossing is finite and transverse. |
| Infinite-density physical gradient control | Out of scope | PN28 already shows gradients need separate control. The new calculation is an auxiliary local-scalar limit. |
| Scalar-tensor vacuum test | Passed within stated extension | R=4U/F_g, U_s=2U F_g_s/F_g and positive Einstein-frame curvature give an inequality with free alpha. |
| Thermodynamic source transfer | Conditional | The source identities are verified, but q=q0 exp(3s) is an added mapping; fixed-mu potential must not be confused with varying-mu equilibrium energy. |
| PCDC fixes positive cosmological vacuum | Failed | Source uses a subtracted sector and saturation; even granting field identifications gives negative sector energy and a free positive uplift. |
| One-loop protection in the isolated scalar extension | Failed | The Gaussian pole contains a nonzero exp(6s) mode outside the classical potential family. This does not exclude cancellations in an added theory. |
| Worldwide novelty | Not assessed | The elementary negative-power/log limit is explicitly known; no global priority claim is made. |

## Independent algebraic reconstructions within this self-review

Pressure check: under a volume change with fixed phase-space level,
K=k rho^(5/3). The envelope derivative is W_K=exp(-2s). Therefore
rho W_rho-W=(2/3)K exp(-2s)-U. Combining with W_s=0 gives A/3,
including the scalar pressure that would be lost in a kinetic-only check.

Enthalpy check: the chemical potential of the minimized excess energy is
(5/3)k rho^(2/3)exp(-2s), zero at rho=0. In units h_*=5B/(2rho_*),
its positive 5/2 power is [1-y^(-1-delta)]/(1+delta). This gives exactly
n=psi^(3/2)[1-(1+delta)psi^(5/2)]^[-1/(1+delta)]. The mass source and
core rescaling retain the factor 5/2. The column is xi_delta times
sqrt(B y_c^(-delta)/(4piG)), not xi_delta sqrt(B/(4piG)).

Boundary check: psi_max is approached only in a sequence of central
states. Each individual state has psi_c<psi_max and bounded density, so
the finite-edge proof does not assume uniform bounds in that sequence.
For the core limit, v is monotone and at most zeta^2/6; this allows the
uniform compact source comparison before the quarter-density crossing.
No infinite numerical integration substitutes for the analytic argument.

Vacuum check: in the minimal extension, changing C alters H but neither
the scalar minimum nor its mass. In the nonminimal test the actual scalar
mass is determined in the Einstein frame, not just by Jordan-frame U_ss.
This gives 9B-4alpha V for F_g=M^2 exp(alpha s^2), with a strictly positive
kinetic coefficient at s=0. Equality is marginal and does not follow from
stability.

Quantum check: one-loop divergence is a function of U_ss^2. Its steepest
exponent is 6 for every delta>0. Parameter renormalization of the two
original exponents produces at most their exponential-polynomial tangent
space, so it cannot absorb that new mode on any open field interval.
The calculation is conditional on a conventional canonical scalar
vacuum sector and makes no claim about the unknown full quantum parent.

## Computational coverage and residual risks

The main script enumerates all 5 delta values crossed with all 3 y_c values
in the contract; it stops at quarter density, not at the outer matter edge.
The finite-edge assertion is analytic, not a claim about those integrations.
There are 20 separate minimized-energy pressure checks and 3 tighter repeats.
Mass is checked by quadrature of the solved core, and enthalpy by quadrature
of the EOS; these are distinct identities from the root event. The limiting
theta equation uses a separate implementation from the finite source.
Stable expm1/log1p evaluation avoids high-density subtraction loss.

All 32 main and 8 protection checks pass. This does not make the proof
formal or the floating-point errors certified. SciPy/SymPy correctness,
regular central-series initialization, numerical tolerance and the specified
approximations remain limitations. No empirical tests, full nonlinear
stability analysis, finite-gradient new-family solve or microscopic
selection have been performed. The exact unresolved implication is a
physical principle fixing the full energy offset and scaling response.

Physical hierarchy check: the large V_sector=B/delta cannot silently be
discarded from gravity. In a conventional relativistic vacuum completion,
the outward vacuum force relative to enclosed matter attraction is
2V_total/[mean_rho(r)c^2]. Dominant rest mass and a small value of this ratio
are additional conditions, not consequences of the formal core theorem.
Their uniform validity as delta->0 has not been established.
