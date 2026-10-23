# Cold orbital frequencies separate from the collective mode

A finite orbit sample gives a concrete candidate explanation for persistent cold oscillations: the typical orbital frequency falls below the collective radial frequency as the occupation parameter increases. Higher orbital harmonics can still resonate. This is a diagnostic, not a damping-rate calculation or proof that collisionless settling is impossible.

## Computation and checks

Reintegrate the continuum fixed-mass equilibria with the saved central potentials at A10,100,1000,10000, gamma=.01 and anisotropy radius1. Set the cutoff energy to zero, so the effective single-particle potential is -Psi(r). Sample1024 deterministic Sobol phase points from each positive f(Q) distribution. Find the two turning points of

    vr²(r)=2[E+Psi(r)]-L²/r².

Evaluate the radial period with r=rp+(ra-rp) sin²(theta), which removes the square-root endpoint singularities:

    Tr=2 integral_rp^ra dr/sqrt(vr²),  Omega_r=2pi/Tr.

Quadrature orders64 and128 agree to better than1.1e-8 relatively. Turning-point residuals are below5.5e-13. Total-mass error is below8.2e-7, inherited from the saved shooting solution. These are numerical accuracy checks for the sampled orbits, not a guarantee that all occupied phase space has been covered.

| A | median Omega_r | 10th–90th percentile | sampled maximum |
|---|---:|---:|---:|
| 10 | .58265 | .36425–.81205 | 1.76506 |
| 100 | .47524 | .45442–.50963 | 1.56165 |
| 1000 | .34213 | .27892–.38946 | 1.26973 |
| 10000 | .22734 | .16024–.28659 | .93132 |

The comparison frequency .827760 is the zero-dispersion cold-fluid fundamental. It is not a computed kinetic eigenfrequency for each warm branch.

For A10000, none of the1024 sampled fundamental orbital frequencies falls within5% of that reference. This does not prove a resonance gap: the sampled maximum exceeds it, a finite sample can miss narrow resonance surfaces, and interpolation between orbits was not used to locate an exact resonance. The fractions within5% for n*Omega_r are .195% for n=2,15.23% for n=3,13.57% for n=4,8.01% for n=5,2.83% for n=6 and .879% for n=7. These are sample proximity fractions, not resonant mass fractions, absorption probabilities, or damping rates. The5% band is an exploratory diagnostic.

## A conditional scaling insight

The equilibrium family obeys

    rho_A=A Psi_A^(5/2)/(1+r²).

If its density converges to a finite nonzero cold profile on a fixed interior region, then

    Psi_A = A^(-2/5) [rho_A(1+r²)]^(2/5).

For orbit families whose scaled turning points remain in a regular limiting potential, velocity scales as A^(-1/5), time as A^(1/5), and Omega_r as A^(-1/5). This is a conditional interior scaling argument; uniform control at the free edge, center and exceptional orbit families has not been proved. The observed median frequency ratio from A1000 to10000 is .6645, compared with .6310 for the asymptotic power.

Meanwhile the cold-fluid collective operator retains a finite restoring frequency determined by the limiting density and stiffness. Thus resonance with that mode moves toward higher orbital harmonic number, formally n_res=O(A^(1/5)), for the regular orbit families described above. The same cold limit that improves the static acceleration profile can therefore make low-order orbital energy exchange less accessible.

This does NOT by itself establish damping suppression. The mode potential's Fourier amplitudes along orbits, derivatives of the equilibrium distribution, self-consistent kinetic response, and exceptional orbits all matter. Smoothness can affect high-harmonic couplings, but no uniform bound or coupling-weight calculation is supplied here.

## Consequence for the mechanism search

A useful next calculation is the orbit-resolved Fourier coupling of a candidate mode, followed by the self-consistent kinetic response. Merely counting frequency matches is insufficient. A derived additional channel may still help, but importing an independent field's radiation law into this identified-medium model without an action and energy accounting remains unjustified. The present result explains a plausible obstacle to cold phase mixing rather than supplying the missing formation/selection mechanism.

The bounded orbit_resonance_run audits the actual orbit calculation with three passing checks and hashed inputs. The derivation and interpretation are self-reviewed. No novelty or complete theory claim is made.
