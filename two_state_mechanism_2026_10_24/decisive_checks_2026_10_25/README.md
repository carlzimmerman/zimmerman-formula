# The decisive question: does the mechanism survive its own state physics?

**The requested physical theory has not been found. The current passive
critical-spectrum tether construction should not be treated as a leading
explanation on the strength of its static fit.** Its law-producing state was
assumed, not derived. This pass adds a decisive thermal-response calculation,
a conditional mass/response constraint, and a test of a potential alternative
state-selection route. These results restrict named models, not all possible
dark matter or modified-gravity theories.

## Strongest new result: the critical law is not thermally robust

For the actual singlet-plus-vector four-level medium, including both dark
excited levels, the finite-temperature polarization follows from its partition
function. For every fixed positive internal temperature, its response becomes
analytic and odd at sufficiently small field.

With microscopic charge matching held fixed, the baryonic source behaves as
**S proportional to g**, rather than the desired **S proportional to g²**.
Even retuning the charge to cancel the thermal linear term would leave a cubic
law; it would also violate the requirement of common microscopic parameters.
The zero-temperature continuum's nonanalytic law does not survive that limit.

Numerical logarithmic slopes independently confirm the analytic result:

| Dimensionless internal temperature tau | Fixed-charge low-field source power | Power after hypothetical linear-term retuning |
|---:|---:|---:|
| 0 | 1.99993 | 1.99993 |
| .001 | 1.01756 | 2.99575 |
| .01 | 1.00018 | 2.99996 |
| .1 | 1.00000 | 3.00000 |

These are evaluations near E/s_max=1e-4,2e-4, not fits to observed galaxies.
The proof concerns this independent finite-level ensemble with the specified
continuous spectrum. An interacting thermodynamic critical phase, a nonthermal
prepared state or another force mechanism can evade it; none is derived here.

At x=g/a0=.01, staying within .05dex of the same candidate's cold prediction
requires tau=kBT/(d*s_max)<=.009459. Combining the canonical oscillator-strength
bound with the generous full-dark-inventory density of the large-disk proxy and
epsilon=.1 gives an optimistic internal-temperature ceiling **2.62e-27 K**.
This is a cross-check under those assumptions, not a measured galaxy temperature
or a universal physical limit. The actual local density at a low-acceleration
radius is not supplied by that central inventory proxy. Using the full inventory
makes the bound generous and does not justify neglecting its gravity. Internal
excitation temperature must not be confused with orbital velocity dispersion.
Temperature tolerance here is relative to the approximate cold candidate curve,
not an additional .05dex allowance around an exact observed RAR.

## Mass and response cannot be tuned independently

Within the predecessor sum-rule and spherical-average response assumptions,

(Omega_relevant*t_dyn)² <= 18*x²/(epsilon*f³) * rho_medium/rho_total.

At x=.01, an illustrative .05dex extra-mass budget permits medium fraction only
.002271. Requiring the representative modes to respond ten times faster than
t_dyn then demands epsilon<=5.28e-8. At x=1e-4 the corresponding conditional
ceiling is5.37e-14. These are necessary screens in that model, not sufficient
conditions for a working medium or proofs excluding arbitrarily light carriers.
The exact simple-law mass budget and approximate critical constitutive law are
compared diagnostically; they are not asserted to hold identically together.

An audit prevented a tempting false no-go: making countercharges light cancels
out of a response/plasma-frequency comparison only when their local density
remains comparable to the positive carriers. An evacuated-countercharge region
can behave differently. Pressure-supported, nonadiabatic, nonlocal and nonthermal
states remain loopholes requiring actual derivations.

## Could a different state-selection interaction work?

The equilibrium degeneracy indicator rho/sigma³ is 14,142 times larger in the
smallest-dwarf proxy, and127 times larger in the second-dwarf proxy, than in the
large disk. A common monotone condensation threshold under these virial/inventory
assumptions cannot select only the disk. This is a state-model result, not a
statement about observed dwarf internal temperatures or all superfluid theories.

A short-range classical rate proportional to rho*sigma does favor the dense
disk. A single effective cross section per mass between .000877 and .01786cm²/g
satisfies a10Gyr one-zone processed-fraction screen: disk>=80%, others<=20%.
This is a real surviving **classical exposure selector**, but its cross section
is an additional input and processed matter is not automatically tethered.

We then tested the intended Bose interpretation using the explicitly schematic
rate enhancement (1+N), N=n*lambda_thermal³. If the disk meets the ideal-gas
N>=zeta(3/2) degeneracy screen, its maximum rate advantage over the smallest dwarf
is2.7655; the required ratio is7.2126. No common interaction normalization fixes
that conflict in this proxy. An analytic monotonicity argument establishes the
bound; a301-mass scan finds zero joint successes. A full quantum collision
integral, another internal phase or nonvirial history remains open. The proxy
cannot be promoted to an exclusion theorem for self-interacting dark matter.

## What this changes

Further refining the same ground-state tether ansatz is not presently justified
as a route to the requested answer. It can improve numerical accuracy while
leaving its crucial constitutive state unphysical or unprepared. A viable next
Hamiltonian must derive a nonlinear force response **and** a thermally/dynamically
realized state. Selecting a state by collisions alone does not derive its force.

The original goal remains open: no first-principles a0, microscopic tether/free
populations, conserved formation history, or observational disk/dwarf/cluster
explanation has been obtained. These files report why the tested constructions
fall short, without inventing a breakthrough or silently broadening a no-go.

## Evidence and review

- [Full derivation](DERIVATION.md)
- [Contact-route assumptions and bound](CONTACT_ROUTE.md)
- [Thermal/mass/state results](run_checks/results.json), [manifest](run_checks/manifest.json)
- [Contact-screen results](run_contact/results.json), [manifest](run_contact/manifest.json)
- [Self-audit and exact limitations](AUDIT.md)

Both runs completed with empty stderr and validated source/result hashes.
The response formula was checked against differentiation of the full four-level
partition function (maximum absolute discrepancy3.46e-10); the thermal linear
susceptibility agrees with independent quadrature within1.12e-16. No claim of
independent external review is made. Earlier evidence and sources were preserved.
