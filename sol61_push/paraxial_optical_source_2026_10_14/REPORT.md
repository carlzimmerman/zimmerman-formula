# Optical creation with reciprocal paraxial Gaussian modes

2026-10-14. Parent checkpoint: 63387f1cd2d5b1e3ac9f8e7f58aeacb2dd627028.

The optical source survives replacement of the arbitrary Gaussian envelope by
matched counterpropagating paraxial modes. At the inherited assigned peak
intensity, the finite vacuum-region calculation gives approximately 155
mediators/s for a 1 m cavity and 1495/s for a 10 m cavity. These are conditional
model outputs, requiring 6.28 MW circulating in EACH direction. They do not
establish attainable optical operation, allowed new particles, capture, or a
connection to the repo's cosmological cold component.

The previous turn supplied a finite effective source but left its Maxwell
geometry arbitrary. This turn makes progress on that particular obligation;
it does not replace the full creation-and-capture objective with a source-only
claim.

## Verified optical convention and its scope

MIT OpenCourseWare's 6.974 Fundamentals of Photonics, Spring 2006,
[Gaussian Beams and Resonators, section 2.6](https://www.ocw.mit.edu/courses/6-974-fundamentals-of-photonics-quantum-electronics-spring-2006/e9852c138493233bc2813f683da5b199_gaussian_bem_res.pdf)
was checked on 2026-10-14. Equation 2.260 supplies the complex-q Gaussian
form, Eq. 2.266 gives z_R=pi w0^2/lambda, and the resonator section gives
mirror matching and the g-parameter stability relation. These support the
optical conventions, not the hypothetical scalar production law. The source
search was limited to those optical formulas, with no novelty claim.

Choose a forward positive-frequency mode with dimensionless transverse envelope

    U(r,z) = 1/(1+i z/z_R)
             * exp[-r^2/(w0^2(1+i z/z_R))],
    z_R = k_photon w0^2/2.

The opposite mode is its spatial complex conjugate, including the carrier
phase. Its wavefront and Gouy phases therefore cancel in the product. In the
leading transverse-field paraxial approximation, B reverses sign between the
two propagation directions. Their cross term in F_munu F^munu provides the
same frequency-2omega scalar source normalization as the plane-wave case,
with spatial envelope

    F(r,z) = F0 |U|^2
      = F0/[1+(z/z_R)^2]
        * exp[-2r^2/(w0^2(1+(z/z_R)^2))],
    F0 = g u_peak/sqrt(2M_R).

This cancellation requires matched reciprocal modes and controlled relative
phase. Arbitrary unrelated beams need not satisfy it. The script checks the
paraxial wave equation and the conjugate-envelope identity symbolically.
An initial direct SymPy simplification did not reduce the latter to zero;
the successful check proves its rational prefactor and exponent coefficients
separately. No failed scientific run is represented as passing evidence.

The scalar paraxial field is not an exact vector Maxwell boundary solution.
Longitudinal optical components and higher paraxial orders are omitted; the
nominal divergence is 1.97e-4 radians. Its square is a scale estimate for
usual paraxial corrections, not a rigorous error bar on the scalar source.
Mirror material fields, coatings, thermal loading, diffraction losses and
pump stabilization are outside this calculation.

## Finite cavity and Fourier source

Retain m=1 eV, M_R approximately 2 eV, g=1e-20/eV and the earlier scalar
momentum k=1.3953124595e-4 eV. The source waist radius is w0=2 mm, matching
the previous transverse source width L_t=w0/2=1 mm. Smooth optical factors use
photon energy 1 eV; the tiny resonance and kinetic offsets must still be
included in actual frequency tuning.

Take an ideal vacuum interval -Z<z<Z between symmetric mirrors. The source
within it is the paraxial envelope above, and the modeled source outside is
zero. This is an ideal boundary approximation, not a calculation of mirror
surface contributions. At the mirrors choose curvature

    R_mirror = Z + z_R^2/Z,
    g_cavity = 1-2Z/R_mirror.

Both cases below satisfy 0<g_cavity^2<1, so their ideal Gaussian resonator
geometry meets the usual ray-stability condition. This does not certify
thermal, optical, mechanical or active-control stability at the assumed power.

After the transverse Gaussian Fourier transform, with convention (2pi)^(-3/2),

    F_tilde(k_perp,k_z) = F0 L_t^2/sqrt(2pi) * exp(-A)
                         * integral_{-Z}^{Z} dz exp[-A z^2/z_R^2-i k_z z],
    A = L_t^2 k_perp^2/2.

The mediator shell rate remains

    Ndot_R = 2pi M_R k integral dOmega |F_tilde(k)|^2 / hbar.

The finite calculations integrate the full angular dependence, including the
finite axial transform; they do not insert a delta function for longitudinal
momentum or assume a homogeneous scalar population.

## Numerical result and controls

The Rayleigh range is 10.1355 m. At peak intensity 1e12 W/m^2 per traveling
wave, each circulating power is

    P_each = I_peak pi w0^2/2 = 6.2832 MW.

This is circulating optical power, not a calculated wall-plug requirement or
an assertion that a suitable cavity can sustain it.

| Mirror separation | Mirror curvature | g_cavity^2 | Mediators/s |
|---|---:|---:|---:|
| 1 m | 205.96 m | 0.99031 | 155.45 |
| 10 m | 25.55 m | 0.37032 | 1494.85 |

The former arbitrary axial Gaussian source gave 275.75/s. It represented a
different spatial overlap and is not a prediction for either finite cavity.
All these rates scale as g^2 I_peak^2 while the fixed weak-source approximations
remain valid. They are not evidence that g has this value or that R exists.

For an independent narrow-angle comparison, Parseval integration of the axial
profile gives

    Ndot_R approximately 4pi^2 M_R F0^2 L_t^4 exp(-L_t^2 k^2)/hbar
                        * integral_{-Z}^{Z} exp[-L_t^2 k^2 z^2/z_R^2] dz.

This differs from the full angular calculation by 0.0407% and 0.00253% for the
1 m and 10 m cases respectively. Twelve- and 24-node quadratures within each
angular oscillation interval agree within the recorded 2e-10 tolerance.

As a separate analytic control, formally taking Z to infinity gives

    F_tilde = F0 L_t z_R/k_perp
       * exp[-L_t^2 k_perp^2/2-k_z^2 z_R^2/(2L_t^2 k_perp^2)]

for k_perp>0. Its angular integration gives 3952.52/s at the chosen k. This
is an infinite ideal-beam control, not a finite apparatus prediction. Its
small-k enhancement samples increasingly remote parts of the beams. It must
not be extrapolated to zero momentum as a laboratory enhancement; the finite
geometry and formation time have to be retained. The k_perp=0 Fourier limit
also needs distributional care and is not evaluated by this formula.

## Cold products and unresolved production-to-storage steps

The monochromatic mediator momentum magnitude is the same as the preceding
package, so the exact two-body daughter energy interval remains
3.14e-10 to 6.55e-9 eV, below the assigned 1e-8 eV cut for every decay angle.
This refers to free daughters after decay, not a confined population. A finite
pump linewidth would broaden the mediator momentum shell and must be folded
into a final accepted yield.

The prior decay examples still apply: mean flight distances approximately
7.74 m for lambda_rep=1e-6 and 7.74e9 m for lambda_rep=1e-15, with the chosen
mu^2=lambda_rep M_R^2. These remain diagnostic coupling choices without a
joint empirical-admission test. Increasing source rate does not shorten the
lifetime or supply a force that retains the daughters. A dark-sector density
profile, energy loss channel and capture fraction have not been computed.

This result resolves the arbitrary optical-envelope concern only to leading
paraxial order in an ideal finite resonator. The next high-impact obligation
is the new eV mass branch's interaction constraints, particularly the relation
between a rapid mediator decay, the same scalar's carrier scattering, and
transport/capture. A source estimate alone cannot justify reusing strong
carrier couplings from the MeV branch. No new gravitational mechanism follows.

## Evidence status

Eight bounded checks pass: exact symbolic paraxial and reciprocal-product
algebra, three longitudinal Fourier controls, an infinite-source angular
control, and finite-cavity quadrature refinement for both lengths. Manifest
validation confirms recorded hashes and execution, not physical viability.
The record includes the inherited source result as an input. This is self-review.
No new Lean proof or full vector-Maxwell certification is claimed.

Reproduce:

    python3 sol61_push/paraxial_optical_source_2026_10_14/check.py /tmp/paraxial_source_results.json

The full goal remains open: hypothetical optical creation now has a more
specific field geometry, but no empirically established carrier or demonstrated
creation-and-capture protocol has been obtained.
