# Carrier self-repulsion limits the initial production extrapolation

2026-10-13. This adds one existing interaction to the initial thermal-production
diagnostic: V_rep=lambda_rep |phi|^4 with lambda_rep=1e-6, as assigned in
../stable_source_completion_2026_10_13/REPORT.md. The reduced muon-source value
mu=27.72246466 eV is retained. This is a truncated feedback calculation, not
the complete original multi-field theory or a full cosmological evolution.

## Distribution-dependent mass contribution

For charge-symmetric, incoherent populations define

    J=integral d^3p/(2pi)^3 [fphi(p)+fanti(p)]/E_p.

No thermal daughter distribution is assumed. Writing phi=(phi1+i phi2)/sqrt(2)
turns the repulsive potential into lambda_rep*(phi1^2+phi2^2)^2/4. Its Hartree
curvature with <phi1^2>=<phi2^2>=J/2 is

    Pi_rep=2lambda_rep J.

The symbolic calculation checks this normalization directly. This is the
leading tadpole of the explicit quartic; it is not a replacement for all
exchange diagrams of the source or the original charged chi sector.

Let D0(T) be the positive pair excess after the preceding thermal-R mass
update, before carriers accumulate. To first order in mass shifts, holding the
source pole and bath fixed,

    D(J)=MR-2m_eff approximately D0-2lambda_rep*J/m.

The on-shell phase space closes at the moment scale

    Jstar=m*D0/(2lambda_rep).

Calling this a closure of on-shell phase space does not mean all production
ceases: finite source widths, off-shell scattering and time-dependent spectral
response are omitted.

## Compute the moment source from the actual decay kinematics

The previous initial calculation supplied a number source. A mass shift depends
on J, so simply replacing J with number density divided by m would be wrong for
moving daughters. For a parent momentum k and energy ER, define the daughter
rest-frame speed beta*=sqrt(1-4m_eff^2/MR^2). Its two lab energies are

    Eplus/minus=(ER +/- k*beta* cos(theta))/2.

The isotropic decay-angle average relevant to J is

    <1/Eplus+1/Eminus>
      =4/ER * atanh(k*beta*/ER)/(k*beta*/ER).

It tends to 4/ER as beta* tends to zero. The initial moment source is therefore

    dJ/dt = Gamma_phi*MR * integral d^3k/(2pi)^3
              fR(k)/ER * <1/Eplus+1/Eminus>.

Numerical angle integration verifies the analytic average. Independently
integrating the corresponding number source recovers the previous calculation.
This avoids imposing a thermal or nonrelativistic daughter distribution.

## Leading feedback solution

In the very small-excess limit, the decay shape changes negligibly while its
normalization scales as sqrt(D). Ignoring inverse reactions and bath depletion
for this early-stage diagnostic,

    dJ/dt=Jdot0*sqrt(1-J/Jstar),
    J(t)=Jstar*[2s-s^2],
    s=t/tstar, tstar=2Jstar/Jdot0, 0<=s<=1.

Here natural-unit times are converted with hbar. A numerical ODE solution up to
s=0.99 agrees with the analytic expression to 2.3e-11 in J/Jstar. We do not
continue a numerically clipped zero rate beyond closure and call it a physical
late-time solution.

| R bath temperature | Jstar (eV^2) | Leading on-shell closure time | Estimated parent fraction consumed |
|---:|---:|---:|---:|
| 0.5 MeV | 2.20143e5 | 29.95 ns | 8.29e-5 |
| 1 MeV | 2.46191e6 | 5.205 ns | 3.74e-5 |
| 2 MeV | 1.14156e7 | 1.543 ns | 1.66e-5 |
| 3 MeV | 2.28389e7 | 0.8732 ns | 1.02e-5 |

The parent fraction estimate is n_phi,total/(2nR), with the daughter number
obtained from the computed number/moment source ratio. It shows why fixed R
abundance can be a reasonable first diagnostic before closure: very little of
that bath has been consumed. It does not establish energy conservation for a
complete externally maintained bath or include subsequent replenishment.

At 2 MeV the estimated p=0 daughter occupation by this point is about 2e-4.
This is a consistency check on initial low occupation in that mode, not a bound
on the entire phase-space distribution or proof that all inverse processes may
be discarded. The stored results also give a formal number density, but this
is a hot-bath population, not a cold captured laboratory inventory.

## Known omissions and coefficient dependence

The direct R mean field induced by carrier density contributes
Pi_tadpole=-mu^2*J/(2MR^2). Its magnitude is 4.80e-5 of the repulsive Hartree
term at the chosen lambda_rep. That particular omitted term is small here;
this ratio does not bound all resonant exchange or spectral corrections.

The earlier tree-level square completion requires
lambda_rep>=mu^2/(2MR^2)=9.60669e-11 for its specified potential family. Lowering
lambda_rep towards that value changes both the closure population and the
importance of previously omitted feedback. The table cannot be rescaled by
four orders of magnitude while keeping its fixed-bath and low-occupation
approximations unquestioned. The independent R^2|phi|^2 coefficient and the
other fields of the original theory also remain separate model choices.

As D approaches zero, a sharp on-shell approximation becomes least reliable.
Finite-width tails, memory effects, interactions and evolving dispersion can
replace abrupt closure with residual production or a moving threshold. Bose
enhancement and inverse decay must be restored as appropriate; the detailed
balance identities in the preceding package remain mandatory. Cosmic expansion
and source cooling subsequently move the threshold as well.

## Research consequence and evidence

The initial production rate cannot be integrated indefinitely to claim either
a large reservoir or complete thermalization. The already assigned repulsive
quartic changes the phase space after a small fraction of the source population
has converted. This is an explicit countercheck to that extrapolation, not a
final relic-abundance calculation or proof that cosmological constraints vanish.

Eleven checks pass: the quartic curvature identity, four independent number-source
comparisons, four decay-angle integrations, successful ODE evolution and agreement
with its analytic solution. The manifest hashes the preceding initial-production
and coupling inputs. No new Lean or experimental certification is claimed.

A complete route must evolve the momentum distributions, source abundance,
mean fields and finite-width reactions with a common energy accounting. The
present moment equation identifies the feedback that such a calculation must
include, while the manufacturing goal remains unresolved.

Reproduce:

    python3 sol61_push/carrier_self_feedback_2026_10_13/check.py /tmp/carrier_self_feedback_results.json
