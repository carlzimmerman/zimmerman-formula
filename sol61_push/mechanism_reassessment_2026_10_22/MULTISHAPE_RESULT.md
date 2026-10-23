# Expanded kinetic feedback recovers a candidate cold breathing response

A low-frequency response peak appears at omega=.810–.815 when the field space is expanded to four and eight radial shapes. It is close to the independently computed cold-fluid fundamental .827760 and to the live simulation's breathing scale. Its location is stable on the tested .005 frequency grid across four/eight shapes and two numerical broadenings; changing the orbit sample from1024 to4096 shifts it by one grid cell. This is stronger evidence for a collective kinetic response than the failed one-shape approximation, but is not a converged continuum eigenvalue or measured damping rate.

## Consistent field basis

At the same finite-A10000 equilibrium, choose displacement trials

    xi_k(r)=r P_k(2r²/R²-1), k=0,...,7,
    s_k=r²rho xi_k,
    delta rho_k=-s_k'/r².

Here P_k is a Legendre polynomial and R is the finite-A support radius. Construct phi_k=K delta rho_k from the same potential-energy Hessian used previously; normalize each maximum absolute potential to1. Nested first1,2,4,8 shapes preserve the dilation as shape0. The stiffness matrix S_ij=<phi_i,K^-1 phi_j> agrees with the independent second-variation formula to maximum absolute error1.62e-8. Its eight-shape condition number is about18519; it remains positive definite in this calculation.

Each finite-temperature density trial vanishes appropriately at its own support edge. No exactly cold edge condition or independent-field radiation equation is imported into this kinetic calculation.

For each occupied orbit, evaluate sixteen Fourier harmonics of all eight potential shapes. The matrix susceptibility is

    Pi_ij(z)=M mean_f[sum_n
       2(n Omega_r)² phi_in phi_jn / {Q[z²-(n Omega_r)²]}].

Self-consistency in the chosen field space uses D=S-Pi. For an external dilation potential (basis vector0), the induced scalar response is

    chi_00=[S D^-1 S-S]_00.

This includes feedback among all retained shapes. It is still a Galerkin restriction, not the full spatial kinetic equation.

## Numerical checks and limitations

1024 and4096 deterministic orbit samples reproduce the matrix high-frequency sum rule to relative Frobenius errors7.00% and2.05%, respectively. This matrix-norm metric can hide larger relative errors in weak directions, so it is not a uniform susceptibility error bound. Fourier integration on1024/2048 midpoint meshes agrees below4.4e-7 in absolute coefficient value. Each direct orbit run passes its four stated construction checks. The response is passive on the tested positive-frequency grid.

The high-frequency approximation M/z² alone is not used to identify the kinetic peaks. Its generalized lowest trial frequency changes substantially with basis size, reaching .288 in eight shapes; it is not a cold-fluid eigenfrequency. Only the full finite-broadening matrix response below is compared with the live oscillation.

## Response comparison

Scan angular frequency .4–1.7 in steps .005 with z=omega+i epsilon at epsilon=.03 and .01. The low peak near the cold fundamental is:

| orbit samples | field shapes | epsilon=.03 | epsilon=.01 |
|---|---:|---:|---:|
| 1024 | 4 | .810 | .810 |
| 1024 | 8 | .810 | .810 |
| 4096 | 4 | .815 | .815 |
| 4096 | 8 | .815 | .815 |

The .815 peak corresponds to period about7.71. This is close to the cold-fluid period7.59059 and the finite-A live prominent peak spacings7.1–8.3, without fitting a frequency to those runs. Finite dispersion, finite amplitude, source discretization and multiple-mode beating still differ among the calculations; the agreement is not an exact waveform validation.

In the4096-orbit/eight-shape result at epsilon=.01, additional prominent peaks occur near1.220 and1.545. The .815 peak has height2.477 and is not the largest peak for this particular external-potential observable. The response to an external dilation potential is distinct from the canonical-dilation initial-value experiment, so relative peak heights must not be equated to live radius amplitudes.

One shape instead peaks near1.37 and two shapes retain significant basis dependence. The four/eight comparison therefore corrects an identified spatial truncation error rather than merely tuning an earlier frequency. Further basis enlargement is still needed before claiming convergence.

## Damping remains unresolved

At the low peak, reducing epsilon from .03 to .01 increases the eight-shape height from about .852 to2.477. The approximately inverse-width behavior indicates substantial regularization control of the peak. Neither peak width nor peak height is a physical damping rate. Finite orbit sampling also retains discrete reversible frequencies; a continuum initial-value calculation or justified continuation with sampling and basis convergence is needed to infer damping.

The result supports a candidate collective kinetic mode near the observed cold ringing frequency. It does not show that this mode decays efficiently, that the finite occupation is selected dynamically, or that a primordial population forms the required halo. No novel coupling, full parent theory or breakthrough claim follows.

## Evidence

multishape_1024/4096.json and .npz preserve the direct orbit construction, stiffness and Fourier data. multishape_run_v2 performs the bounded feedback scan using those pinned inputs, passes three audit checks, and has a valid completed manifest. The initial multishape_run failed before calculation due to a plot-title string syntax error; its source/record remain preserved and v2 fixes that syntax. This does not replace any failed physical gate. multishape_response.png was visually inspected. All interpretation is self-reviewed.
