# Ideal thermal capacity does not establish an interacting cold medium

This calculation tests a necessary statistical distinction before attempting to
stabilize the preceding neutral coherent branch by thermal motion. It is an
ideal-gas reference, not a finite-temperature solution of the interacting model.
The original cold-energy creation objective remains open.

## Reference model and derivation

Use natural units with temperature T in eV, m=1 eV, mediator kinetic mass M=2 eV,
detuning delta=2e-9 eV, and constituent density n=3e14/m^3. This is an assigned
benchmark, not an observed density of these particles. Take two distinguishable
bosonic carrier species a,b and one mediator r. Charge neutrality and chemical
equilibrium give mu_a=mu_b=mu and mu_r=2mu. Conserved constituent number is
N=Na+Nb+2Nr. The atomic ground energy fixes mu<=0; the mediator dispersion is
delta+p^2/(2M). These are ideal bare dispersions with interactions neglected.

Integrating the Bose occupations at their maximum allowed mu=0 gives

    n_max(T) = 2 (m T/(2 pi))^(3/2) zeta(3/2)
             + 2 (M T/(2 pi))^(3/2) Li_(3/2)(exp(-delta/T)).

The mediator factor two counts constituents, not two mediator species.
The kinetic energy density, with no extra constituent factor on mediator energy,
is

    U_kin(T) = (3 T/2) [2 (m T/(2 pi))^(3/2) zeta(5/2)
                       + (M T/(2 pi))^(3/2) Li_(5/2)(exp(-delta/T))].

The separate detuning energy is delta*n_r. Rest energies are excluded throughout.
The standard single-species Bose distribution, density of states and condensation
criterion are described in David Tong, Statistical Physics, chapter 3, sections
3.1 and 3.5, author's unversioned Cambridge HTML, checked October 14, 2026:
https://www.damtp.cam.ac.uk/user/tong/statphys/statmechhtml/S3.html
Here they are applied to the assigned species with the number weights above.
This source supports the ideal reference only, not the interacting model.
No source PDF was cached and no novelty claim is made.

## Results and the temperature distinction

Solving n_max(Tc)=n gives Tc=0.000149155599456 eV, or 1.730878857 K.
At this threshold U_kin/n=7.271521753e-5 eV, corresponding to a constituent-mass
weighted one-dimensional speed of 2087.31 km/s. The zero-detuning ideal reference
has Tc=0.000148790890 eV; omitting the mediator gives 0.000364130114 eV.

Setting T=m(s/c)^2 is a CLASSICAL temperature label. At s=200 km/s this gives
T=4.4506e-7 eV and an ideal thermal capacity fraction 0.000152902. It would be
incorrect to identify that label with the equilibrium temperature at the same
kinetic energy in a quantum-degenerate gas.

Instead match U_kin(T)/n=3m(s/c)^2/2 on the saturated ideal branch. Excess number
occupies the zero-energy atomic modes, equally between charges. The results are:

| Assigned 1D speed | Energy-matched ideal T, eV | Ideal noncondensed constituent fraction |
|---|---:|---:|
| 30 km/s | 5.00889e-6 | 0.00605386 |
| 100 km/s | 1.31219e-5 | 0.0258672 |
| 200 km/s | 2.28459e-5 | 0.0596033 |
| 1000 km/s | 8.27888e-5 | 0.413002 |

Thus the energy-matched 200 km/s ideal reference has 94.0397% of its constituents
in atomic condensates, not the 99.9847% inferred from inserting the classical
label into the capacity formula. Neither number is an actual interacting halo
condensate fraction. The match is to kinetic energy; detuning energy is recorded
separately, and no claim of matching interacting total energy is made.

## What this changes and what remains open

One cannot justify a normal classical gas pressure at these parameters by merely
assigning a halo velocity dispersion. Equilibrium Bose statistics must be addressed.
This does not prove thermal motion cannot stabilize the full model. It also does
not transfer the earlier coherent-state instability to all mixed states.

Treating the above-threshold mediator as an independent ideal thermal species is
itself a reference approximation. At zero coupling chemical equilibrium is not
dynamically established; at finite coupling the spectral density, interaction
energy, mode mixing and relaxation must be computed. The benchmark h*sqrt(n)/Tc
is 0.00508945, but this is not a bound on interaction corrections, particularly
near condensation or an instability. Gravity, inhomogeneity, traps and collisionless
nonequilibrium occupation distributions are absent. A highly occupied multimode
field need not be thermally equilibrated.

The next meaningful route is a conserving interacting or nonequilibrium kinetic
calculation of the actual neutral source population, including mediator dynamics.
It must derive pressure and response from the same state rather than append an
ideal pressure to the unstable zero-temperature branch. It must also retain the
unresolved connection between the optically created carriers and the repo's
cosmological cold component. This calculation supplies no new production channel,
propulsion effect, experimental evidence, or Lean certification.

## Reproduction and verification

The bounded runner executed check.py with the preceding explicit-medium JSON as
input; contract.json and run/manifest.json record scope, hashes and environment.
Nine numerical checks pass: the threshold equation, four independent momentum
integrals versus polylogarithms, and four kinetic-energy matching equations.
Two additional assertions bracket Tc between analytic limiting cases and require
the matched states to lie below thermal capacity. These verify the stated ideal
calculation, not the underlying physical assumptions.
