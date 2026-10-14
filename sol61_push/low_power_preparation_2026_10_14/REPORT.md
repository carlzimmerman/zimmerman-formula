# Lower-power preparation: storage and phase-noise tradeoff

Parent: 9f7daadee237cc6b7ec5b0a7da3b59ef50b92416.
The earlier 6.28 MW circulating-power benchmark is not a model-independent
requirement. With the previously calculated ideal 10 mm shell, slower
preparation can use substantially lower power. This shifts the unresolved
requirements toward retention and coherence; neither is demonstrated here.

## Inherited assumptions and new scope

Use the same 2 cm inner radius, 1 eV carriers and assigned silica barrier.
The previous outgoing-wave pole for a 10 mm shell gives single-particle
*tunneling-only* lifetime tau=527481.639 s. It does not include other loss
channels. Its real ground energy agrees closely with the infinitely thick
reference orbital, so the source matrix element is inherited at fixed
intracavity field. The thicker shell has outer radius 3 cm: the optical
cavity and aspheric correction derived for outer radius 2.5 cm must NOT be
reused as though unchanged. Optical delivery through this new geometry is
still pending.

At fixed spatial beam profile, the pair-drive frequency scales linearly with
intensity in each of two equally intense waves:

    Omega(I)=8.706271354/s * I/(1e12 W/m^2),
    Pwave=I pi (2 mm)^2/2,
    Tpi=pi/(2 Omega).

This calculation imposes that field and exact mean pair resonance; it does
not solve optical buildup, frequency drift, readout or empirical particle
constraints.

## Include phase diffusion and single-particle leakage

In the strong-blockade projection retain vacuum, one pair, and each of the
two single-carrier states left after escape. The Hamiltonian connects only
vacuum and pair with matrix element hbar Omega. Each carrier independently
leaks at rate 1/tau. Keeping the single states avoids incorrectly assuming
a pair escape instantly resets the trap to vacuum.

Assign a common laser with Lorentzian FWHM Delta nu: its phase increments
obey Var[theta(t)-theta(0)]=2 pi Delta nu t. The pair-source phase is twice
the common laser phase, so its coherence decays at

    gamma=4 pi Delta nu.

This factor would differ for independent lasers. It is a specified Wiener
phase-noise model, not a measured laser capability. Lindblad operator
sqrt(gamma/2) diag(-1,+1,0,0) implements this decay in the stated basis.
Zero linewidth is an ideal mathematical control, not an apparatus claim.

At zero leakage an analytic control is

    Ppair(t)=[1-exp(-gamma t/2)
       (cosh(d t)+gamma sinh(d t)/(2d))]/2,
    d=sqrt(gamma^2/4-4 Omega^2),

with its continuous limit if d=0. Matrix evolution matches three underdamped
and overdamped controls. At finite leakage the stationary pair probability is

    Ppair,steady=Omega^2 tau/[gamma+1/tau+4 Omega^2 tau].

To derive it, eliminate the stationary coherence with damping
gamma+1/tau. Each single-state population equals Ppair, so the vacuum
population is 1-3 Ppair. Pair creation/removal then gives the expression.
Its limiting value is 1/4, not 1/2, because the single-carrier states retain
population. This stationary ceiling does not limit a timed coherent pulse.

## Calculated probabilities at the nominal pi-pulse time

All powers are circulating power in EACH direction at the central waist.
The following rows assign common-laser linewidth 1 mHz:

| Power per wave | Pulse duration | Retained pair probability |
|---|---:|---:|
| 6.28 W | 50.1 hours | 0.001572 |
| 628 W | 30.1 minutes | 0.172144 |
| 6.28 kW | 180.4 seconds | 0.644040 |
| 62.8 kW | 18.04 seconds | 0.946347 |

At 628 W, assigning 1 microhertz linewidth instead gives 0.990970;
zero phase noise gives 0.996587. These are sensitivity assumptions, not
claims of attainable 30-minute phase stability. The 1 mHz case still has
conditional nonzero production without demanding near-unit preparation.
No claim is made that these nominal pulse lengths maximize probability.

The 628 W, 1 mHz point is independently recalculated in the parent's full
single-spatial-orbital Fock model with nonlinear pair interaction and the
same phase diffusion. Cutoffs of two and three carriers per sign give
0.172143561520, agreeing with the four-state value 0.172143561656 to
1.4e-10. This checks the projection at that selected point; it does not
validate every row, other orbitals or the nonlinear interaction itself.

## Pulse envelope and unresolved limits

The matrix exponential uses a rectangular pulse. In the four-state model,
replacing it with 5 ms half-cosine ramps and extending the duration by 5 ms
preserves pulse area. A bounded-Hamiltonian comparison limits the event
probability change by Omega*(5 ms)+2*(5 ms)/tau. At 628 W this is about
4.37e-6. The first term bounds the integrated absolute drive change; the
second allows pair escape during the added interval. Phase diffusion alone
does not change final populations after the drive is off.

That comparison controls only these four-state populations. It does not
justify abrupt switching for the full mediator continuum. A physical source
still requires smooth switching and its additional channel analysis; the
previous smooth-pulse free-mediator bound is not silently applied to this
rectangular calculation.

Long retention is the essential new assumption. The parent material study
already showed its extreme barrier sensitivity: halving the modeled barrier
can reduce the 10 mm tunneling lifetime to about 221 s. Additional wall and
radiative losses can also shorten it. Lower optical power therefore cannot
be advertised as a viable apparatus until total retention and material
response are established. Small phase-noise linewidth likewise does not
bound slow drift or an error in the central resonant frequency.

## Evidence and next decision

Seventy-eight numerical checks pass, covering density-matrix invariants,
analytic dephased-Rabi and stationary controls, and the selected Fock-space
comparison. The bounded run and hashes validate in run/manifest.json. No
new Lean proof or physical certification is claimed.

This opens a lower-power preparation route within the hypothetical model;
it does not solve empirical admission, readout, total losses or the thick-shell
optical mode. The next discriminating checks should assess the required
frequency detuning tolerance and total-retention sensitivity before spending
more effort on the earlier megawatt optical geometry. The larger goal remains
open, including whether these carriers realize the repo's cosmological cold
component rather than merely an assigned auxiliary particle model.
