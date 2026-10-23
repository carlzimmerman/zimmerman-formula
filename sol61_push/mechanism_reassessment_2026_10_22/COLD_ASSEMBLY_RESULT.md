# A continuous cold branch provides a conditional assembly route

An initially cold population need not be manufactured by damping a warm equilibrium. We find a finite unit-mass cold equilibrium for each of nine baryonic amplitudes between.01 and1, continuously followed by boundary-value continuation. Each tested background has positive lowest radial eigenvalues. This supports testing adiabatic baryonic assembly as a separate route; it does not demonstrate live tracking or explain primordial cold occupation.

## Model and computation

Keep gamma=.01, the Plummer length1, and cold mass1 fixed in the existing units. Change only the prescribed baryonic acceleration to beta r/(1+r²)^(3/2). The cold equations are

    m'=r²rho,
    gamma rho'=R(m/r²)-beta r/(1+r²)^(3/2),
    R(q)=q²/(1-q).

The outer radius is unknown, with regular central mass, m(edge)=1 and rho(edge)=0. Continuation proceeds from beta1 downward; it is a numerical branch construction, not an evolution in time. Positive densities and q<1 are checked on the background grid.

For each solution use the previous cold radial perturbation equation

    -gamma(s'/r²)' + R'(q)s/r² = omega² s/(r²rho),

with the same center and free-edge conditions as COLD_SPECTRUM_RESULT.md. The fixed external baryonic potential enters through the equilibrium profile. Its explicit force perturbation at fixed Eulerian radius vanishes. Compare the three lowest frequencies at512 and1024 radial nodes; the2% refinement check passes for every background.

| beta | edge | central density | lowest omega,1024 nodes |
|---|---:|---:|---:|
|1|1.70505|4.93857|.827765|
|.7|1.87908|4.03185|.596425|
|.5|2.07749|3.31743|.432760|
|.3|2.45869|2.45079|.259653|
|.2|2.84847|1.91638|.169495|
|.1|3.75671|1.24424|.0785662|
|.05|5.08625|.796267|.0349986|
|.02|7.80077|.431465|.0115684|
|.01|10.9101|.266597|.00492974|

## Formation implication and limitation

All these equilibria have zero kinetic dispersion and L=0. Unlike the previously compared finite-A warm/cold distributions, they do not require an angular-inventory change along the sequence. A cold sheet is also outside the assumption of a finite warm fine-grained phase-space ceiling. This evades those particular warm-to-cold obstructions by changing the initial population, not by refuting the bounds.

The positive radial spectrum supplies restoring dynamics around each tested equilibrium. It does not prove a uniform adiabatic theorem, global nonlinear stability or nonspherical stability. A baryonic growth time must be compared with the response times along the whole trajectory, not only at its end. The lowest inverse frequency at beta.01 is about203 in these units, versus1.21 at beta1, a factor168. The corresponding periods are about1275 and7.59. These are dimensionless diagnostic scales, not a claimed cosmic formation time. Parameter-variation rates and forcing amplitudes also matter; merely exceeding one inverse frequency is not a proven tracking criterion.

There is an exact boundary to this route. At beta0, the stationary virial balance for a finite isolated regular configuration is

    2T + (3gamma/2) integral rho² dV
       + integral rho r R(q) dV = 0.

Every term is nonnegative and the stiffness term is strictly positive for nonzero density. Under vanishing boundary terms and gamma>0 there is therefore no such finite equilibrium. Our sequence cannot start as a finite isolated zero-baryon equilibrium. An expanding cosmological medium, confinement, nonzero initial baryonic seed, or other initial-value setting must be specified. The sampled growth of radius and decrease in frequency do not establish a precise asymptotic scaling at beta0.

This narrows a constructive test: begin with a specified cold seed equilibrium at nonzero beta, increase the baryonic amplitude at several rates, and measure tracking error, oscillation excitation, shell crossing and energy supplied by the changing external potential. The imposed baryonic history is an external source of work; energy of the cold subsystem alone is not conserved during the ramp. Such a test would establish only conditional assembly from that seed, not a natural primordial selector.

## Evidence

cold_assembly.py contains the boundary-value continuation and spectra without imported project code. cold_assembly_run completed, its manifest validates, and four checks pass: all nine amplitudes reached, acceptable backgrounds, positive retained eigenvalues and spectral refinement. The finite numerical evidence is self-reviewed; a sampled continuation is not a uniqueness or all-amplitudes proof. The full parent, kappa derivation and novelty remain unresolved.
