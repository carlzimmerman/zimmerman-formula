# Finite-shell radial thermal phase coupling

This replaces the previous bulk/free-particle reference for one specific question:
first-order DIAGONAL pair-energy noise from radial elastic modes of the actual
assigned spherical shell dimensions. It does not compute off-diagonal excitation
or escape. Material constants and damping are explicit assumptions, not data.

## Elastic boundary problem

Assign rho=2201 kg/m^3, longitudinal speed cL=6000 m/s, transverse speed cT=3750 m/s,
T=300 K, and quality factor Q=100 for every mode. Define shear modulus G=rho*cT^2
and Lame lambda_el=rho*(cL^2-2cT^2). The shells have inner/outer radii 0.2/2.2 m
and 0.02/0.52 m. Both mechanical surfaces are traction free; supports, attachments,
optical openings and static loads are absent.

For radial displacement X(t) f(r),

    f'' + 2f'/r + [k^2-2/r^2] f = 0,
    f = A j1(kr) + B y1(kr), omega=cL*k,
    sigma_rr = (lambda_el+2G) f' + 2lambda_el f/r = 0

at both surfaces. With alpha=lambda_el/(lambda_el+2G), define
S_j(z)=j1'(z)+2alpha*j1(z)/z and likewise S_y. The determinant is

    S_j(ka) S_y(kb) - S_y(ka) S_j(kb) = 0.

The root scan uses q=kb in [0.0001,160), spacings 0.02 and 0.01, retaining the
first forty positive roots found. This is not a certified root count. Independent
elastic-energy Rayleigh quotients, free-surface residuals and low-mode mass
orthogonality check the computed eigenfunctions. The first radial frequencies
are 1047.98 Hz and 4442.24 Hz for the large and small cavities.

Source: Benny Lautrup, chapter 13 "Elastic vibrations", revision 7.7,
January 22, 2004, section 13.4, equations (13-30)--(13-31) and the displayed radial
stress, PDF pages 8--9 (printed 219--220), inspected October 14, 2026:
https://cns.gatech.edu/~predrag/courses/PHYS-4421-04/lautrup/book/vibrations.pdf
The source gives the radial equation, j1/y1 general solution and stress law.
Here the second free surface is imposed explicitly to obtain the hollow-shell
determinant. The solid-sphere root formula is not reused for a hollow sphere.
A separate attempted PMC nanoshell article returned a browser check and was not
used. No PDF was cached locally.

## Moving boundaries and density are one perturbation

For a scalar potential proportional to conserved material density, the shell
perturbation is delta V=-div[V u], including its distributional boundary terms.
Let w(r)=|u_carrier(r)|^2 be the normalized radial carrier probability density.
For one elastic mode the PAIR energy derivative with respect to X is

    C_pair = -2U [integral_a^b w(r)(f'+2f/r)dr
                   + w(a)f(a)-w(b)f(b)].

It is wrong to add the surface and bulk variances as independent sources.
Integrating by parts gives the equivalent expression

    C_pair = 2U integral_a^b [w'(r)-2w(r)/r] f(r) dr.

For the reference bound orbital in the wall, w'= -2*kappa_wall*w, so

    C_pair = -4U integral_a^b (kappa_wall+1/r)w(r)f(r)dr.

Both forms agree numerically for every retained mode. The moving-surface terms
cancel the integration-by-parts endpoints; this does not mean the physical
surface response vanishes. The reference orbital is the preceding infinite-
exterior approximation for the thick, weakly leaking shell.

In exact spherical symmetry an s-wave carrier's diagonal matrix element of a
mechanical perturbation with l>0 vanishes by angular integration. Torsional
modes have no leading density or normal-surface perturbation here. Thus radial
modes are the relevant angular sector for this ideal first-order diagonal
question. This selection rule does not eliminate transitions to other carrier
angular momenta, symmetry breaking, or higher-order noise.

## Thermal phase spectrum under an explicit damping model

The mechanical coordinate has mass

    M_eff=4pi rho integral_a^b r^2 f(r)^2 dr.

Assume independent classical viscously damped Langevin modes with
Gamma_mech=omega/Q and thermal force correlation
<F(t)F(0)>=2 M_eff Gamma_mech kB T delta(t). Then

    S_X(0)=2 kB T/(M_eff omega^3 Q),
    gamma_pair=(C_pair/hbar)^2 kB T/(M_eff omega^3 Q).

This uses the preceding two-sided angular-frequency convention. The arbitrary
normalization of f cancels between C_pair^2 and M_eff. Temperatures are high
relative to all retained phonon energies, so classical thermal occupations are
consistent within this model. The long-time dephasing rate describes the low-
frequency viscous tails; it is not the full finite-time oscillatory coherence.

| Candidate | First 10 modes | First 20 modes | First 40 modes |
|---|---:|---:|---:|
| Large, gamma /s | 5.01079e-30 | 5.08365e-30 | 5.08603e-30 |
| Small, gamma /s | 1.58314e-24 | 2.02688e-24 | 2.05986e-24 |

These partial sums are far below the preceding assigned 1e-6/s extra phase-noise
budget. A 20-to-40-mode refinement is evidence about this truncation, not an
all-mode upper bound. Values scale as T/Q at fixed elastic and trap parameters.
Changing the low-frequency damping law can change the spectrum; these values do
not establish the behavior of glass defects, structural damping, drift or 1/f
noise. No measured Q or material noise spectrum has been substituted.

## Evidence and implication

330 numerical checks pass, including root-grid refinement, Rayleigh quotients,
free-surface conditions, mass orthogonality, quadrature refinement, and the full
bulk-plus-boundary coupling identity. The bounded runner records hashes and
software. This is a conditional analytic/numerical result, not a new Lean proof.

Under the assigned model, the resolved radial thermal modes do not impose a
significant diagonal phase penalty on the preceding source calculation. The
calculation still leaves total wall-induced LOSS unresolved: inelastic transitions
require final carrier scattering states, mode-frequency spectral weight and
all allowed angular channels. It also leaves real material response, optical
feasibility, readout and cosmological identity unresolved. The original cold-energy
creation goal remains open; this package narrows one noise mechanism only.
