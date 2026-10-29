# Can B/V be derived rather than chosen?

**Not from the current parent.** Its stated equilibrium and stability
conditions admit a continuous family of ratios. This investigation finds a
more structured conditional relation, then tests the assumptions that would
be needed to make it a prediction. It does not select the numerical ratio.

## The strongest constructive result

The pressure of the PN28 local matter-plus-scalar equilibrium can be written
as P_total=(U_s-3U)/3. Let A=U_s-3U denote this internal dilation response.
If a microscopic theory were to impose A_s=-3delta A, with constant delta>0,
stationarity gives the positive, strictly convex potential

    U_delta(s)=V_sector[delta exp(3s)+exp(-3delta s)]/(1+delta).

Its unique vacuum is s=0, and it obeys

    B_curv := U_ss(0)/9,
    B_curv/V_sector=delta.

Thus a small ratio could mean a small scaling response. The relation is
derived from the stated equation; that equation and its exponent are not
derived from a microscopic theory. It is not yet a prediction of a number.

There are two substantive catches.

First, adding an allowed constant C preserves the scalar minimum and
stiffness, but gives B_curv/V_total=delta V_sector/(V_sector+C). Internal
field symmetries with a fixed metric cannot forbid this term. The full
gravitating vacuum energy must be determined, not just a subtracted sector.

Second, the changed pressure is P_ex=V_sector(1-y^(-delta)), y=exp(3s).
It approximates B_curv ln y when delta ln y is small, but saturates at high
density. B_curv is therefore not the nonzero asymptotic logarithmic pressure
coefficient of PN28. The log limit at fixed B_curv sends V_sector to infinity.

## A new halo discriminator

The changed EOS still has finite-radius reduced halos. Its formal dense-core
limit, however, is

    Sigma_core ~ xi_delta sqrt(B_curv/(4piG)) y_c^(-delta/2),

with y_c proportional to central particle density in this regime. The column
has a small density dependence when delta is small; it is not exactly
universal. The old adopted acceleration dictionary becomes

    a0_core^2/(G V_sector) ~ pi xi_delta^2 delta y_c^(-delta).

Using the old log target 0.002329458 as delta would therefore not derive an
exact universal kappa=1/2 in this branch. No run fits delta to that target.

| delta | Limiting xi_delta | Column / sqrt(B_curv/(4piG)) at y_c=10^6 |
|---:|---:|---:|
| 0, subtracted log limit | 5.844773 | 5.844768 |
| 0.001 | 5.847782 | 5.807521 |
| 0.01 | 5.874952 | 5.482820 |
| 0.1 | 6.155426 | 3.085020 |
| 1 | 10.045022 | 0.010045 |

The last column comes from the finite central-core integrations. Fifteen
cores, twenty independently differentiated minimized-energy states, five
limiting reference equations and three tighter core repetitions pass their
checks. Maximum mass-quadrature error is 2.60e-11 relative; maximum scaled
pressure-derivative error is 5.15e-9. The highest-density coefficient errors
are below 8.68e-7 and the repeat changes below 2.64e-11. These are numerical
diagnostics, not certified error bounds. Full new-family finite-gradient
halos, formation, stability and observational tests were not computed.
Physical use also requires dominant particle rest mass and negligible vacuum
force. In a conventional relativistic vacuum completion the latter requires
mean_rho(R)c^2 much larger than 2V_total. The formal delta->0 limit at fixed
B does not preserve that hierarchy automatically.

## Other attempted selectors

- **Gravity:** the vacuum equations fix H from V. Nonminimal scalar coupling
  can give a stability inequality, but the tested family has no equality
  selecting B/V.
- **Vacuum thermodynamics:** under an explicit dictionary, B is inverse
  vacuum compressibility. Stiffness and equilibrium energy remain independent.
- **Dilaton anomaly:** the checked mass-energy relation involves a subtracted,
  negative sector vacuum energy. It does not determine the full positive
  cosmological energy.
- **Quantum protection:** a conventional canonical scalar vacuum extension
  generates exp(6s) and other new shapes at one loop. The two-exponential
  potential is not closed under that calculation. Additional symmetry or
  fields might alter this, but none has been supplied or checked.

The negative-power-to-logarithm limit is already present in the literature;
it is not claimed as a new discovery. Exact source conventions and limitations
are recorded in [SOURCES.md](SOURCES.md).

## What would actually finish the ratio calculation?

With a justified vacuum-medium coordinate q, the microscopic targets become

    B=q0^2 epsilon_qq(q0),
    V=epsilon(q0)-q0 epsilon_q(q0).

Equivalently, B/V is the negative logarithmic response of the equilibrium
vacuum energy to q. A physical calculation of epsilon, its state, and its
full offset could determine both. Defining that response, choosing a
subtraction, or assigning delta a plausible small number cannot.

The [full derivation](DERIVATION.md), [offset and quantum checks](OFFSET_AND_LOOPS.md),
[author self-review](SELF_REVIEW.md), [verification record](VERIFICATION.json),
and [continuation handoff](HANDOFF.md) preserve the results and remaining
obligations. Both bounded runs completed with all 40 named checks passing.
The original PN28 files were left unchanged. The normalization goal remains
open; these obstructions apply to the tested mechanisms, not every possible
microscopic completion.
