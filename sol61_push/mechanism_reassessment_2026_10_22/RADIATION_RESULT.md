# Radiation checkpoint: an open channel, not yet a settling mechanism

The correctly reduced mixed scalar has a gapless outgoing radiation channel. The mass-gap exclusion in CFG760–762 does not automatically transfer to this different equation. However, low-frequency interface reflection and mass-conserving source suppression can make this channel weak. No halo cooling time or dynamical selection mechanism has been established.

## Model and scope

This calculation continues NONLINEAR_WEAK_RESULT.md, using a formal scalar interface approximation, not a solution of the complete A33 action. In one spatial dimension,

    L = B sigma_t^2/2 + eta sigma_xt^2/2
        - h(x) sigma_x^2/2 - gamma sigma_xx^2/2,

with B, eta, gamma positive and h nonnegative. Here h represents the polarization-dependent restoring stiffness. The equation is

    B sigma_tt - eta sigma_xxtt - (h sigma_x)_x + gamma sigma_xxxx = 0.

For constant h, z=k^2 satisfies

    gamma z^2 + (h-eta omega^2) z - B omega^2 = 0.

For every positive frequency, the product of the two roots is negative. There is one propagating wave and one evanescent pair. There is no positive frequency threshold in this reduced model. This is a property of a standard dispersive equation; novelty is not certified.

CFG760_p_wave_gap and its CFG761–762 continuations instead tested a local massive polarization-wave equation. Their numerical exclusions remain evidence for that model. This result neither reruns nor overturns those experiments, and it does not repair CFG935's failed energy-relaxation experiments.

## Interface flux

With constant eta and gamma and a step in h, variational matching requires continuity of sigma, sigma_x, gamma sigma_xx, and

    gamma sigma_xxx + (eta omega^2-h) sigma_x.

The conserved energy density and flux are

    e = (B sigma_t^2 + eta sigma_xt^2 + h sigma_x^2
         + gamma sigma_xx^2)/2,
    j = -eta sigma_t sigma_xtt - h sigma_t sigma_x
        + gamma sigma_t sigma_xxx - gamma sigma_xt sigma_xx.

A real traveling wave represented by complex amplitude A has mean flux

    <j> = omega k (h+2 gamma k^2-eta omega^2) |A|^2/2.

This equals group velocity times mean energy density. Including both decaying evanescent modes, a unit incident wave at a planar step with B=eta=gamma=h_left=1 and h_right=0 gives:

| Dimensionless frequency | Transmitted energy fraction |
|---|---:|
| 0.000001 | 0.00399201 |
| 0.0001 | 0.03921088 |
| 0.01 | 0.32990285 |
| 0.1 | 0.72062715 |
| 1 | 0.98566570 |

Reflection plus transmission equals one within numerical roundoff. At low frequency, transmission approaches 4 sqrt(omega). Thus the channel is open but mostly reflected at sufficiently low frequency. These dimensionless numbers are not galaxy escape fractions. A smooth spherical halo, variable kinetic coefficients, full mode mixing and its exterior must replace this planar step before making that inference.

## A mass-conserving source can emit, but inefficiently at low frequency

A separate homogeneous unpolarized reduced calculation uses a prescribed weak density perturbation:

    (B-eta Laplacian) sigma_tt + gamma Laplacian^2 sigma = -K delta_rho.

K=4 pi G in the inherited c=1 normalization. For harmonic frequency omega, define positive k and kappa by

    k^2-kappa^2 = eta omega^2/gamma,
    k^2 kappa^2 = B omega^2/gamma.

The outgoing Green function of the harmonic operator is

    G(r) = [exp(i k r)-exp(-kappa r)] /
           [4 pi gamma (k^2+kappa^2) r].

For a spherical source, using real fields represented by complex amplitudes with exp(-i omega t), integration of the far-field energy flux gives

    P_rad = K^2 omega k |delta_rho_tilde(k)|^2 /
            [8 pi gamma (k^2+kappa^2)].

Mass conservation removes the constant Fourier term. With delta_I = integral r^2 delta_rho d^3r,

    delta_rho_tilde(k) = -k^2 delta_I/6 + O(k^4),
    P_rad ~ K^2 omega k^3 |delta_I|^2 / (576 pi gamma).

Since k scales as sqrt(omega) in the low-frequency vacuum, power scales as omega^(5/2) at fixed delta_I. This is finite-size breathing radiation, not radiation from a changing total mass. As an explicit check, a Gaussian of mass M and radius R with perturbation epsilon rho (r^2/R^2-3) has zero perturbed mass, delta_I=6 epsilon M R^2, and transform

    -epsilon M (k R)^2 exp[-(k R)^2/2].

Direct radial quadrature agrees at kR=0.1, 1, and 3. This prescribed-source result is separate from the interface experiment; their numerical factors have not been combined into a halo luminosity.

## Evidence and next obligation

Current bounded records: radiation_run2/manifest.json (10/10 checks), and radiation_source_run/manifest.json (6/6 checks). Both validate against their recorded files. Reversing the outgoing direction in the unequal-media interface fails four checks: energy-flux conservation, outgoing direction, nonnegative transmission, and the low-frequency law. The first mutation produced a singular identical-media control; RADIATION_MUTATION_NOTE.md discloses the correction. radiation_run is historical because the mutation handling subsequently changed the script.

These are symbolic/numerical checks with self-review, not independent proof certification. The next decisive calculation is a self-consistent polarized spherical background and its coupled outgoing perturbation problem, followed by mode energy divided by radiated power. A useful outcome must also account for the cold component and observed timescales. Radiation could let a local system lose energy while the complete system conserves energy; it does not by itself select the missing cold density, derive kappa=1/2, resolve Solar-System constraints, or show that evolution settles rather than destabilizes.
