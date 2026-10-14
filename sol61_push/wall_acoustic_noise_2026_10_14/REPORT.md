# Wall acoustic reference and phase-noise requirements

The preceding thick-shell lifetimes include tunneling only. This calculation
adds a bulk acoustic absorption REFERENCE and derives diagonal energy-noise
sensitivities of the reference trap. The bulk rate is not a finite-trap ejection
rate or an upper bound. The sensitivities give requirements on a material noise
spectrum; no such spectrum is measured or supplied here.

## A derived homogeneous acoustic reference

Assume an isotropic continuum with mass density rho=2201 kg/m^3, longitudinal
sound speed cs, and potential proportional to local mass density. The static
barrier U then fluctuates as delta V=-U div(u), where u is displacement. This
assumes fixed composition and the previously assigned scalar response per mass.
Quantizing one longitudinal mode in volume V gives the absorption matrix element
squared, apart from the thermal occupation,

    |M_q|^2 = U^2 hbar q/(2 rho V cs).

Here U is in joules and q is a wave number. A free carrier initially at rest in
an infinite uniform medium absorbs a phonon when

    hbar^2 q^2/(2m_phys) = hbar cs q,
    q0 = 2m_phys cs/hbar, epsilon0 = 2m_phys cs^2.

The three-dimensional mode measure and the derivative hbar*cs at q0 give

    Gamma_bulk = U^2 q0^3 nB(epsilon0)/(2 pi rho hbar cs^2),
    nB(epsilon) = 1/[exp(epsilon/(kB T))-1].

For assigned cs=6000 m/s and T=300 K, the wavelength is 3.097 cm and absorbed
energy is 8.01108e-10 eV. The bulk rates are 8.60e-25/s for the large-cavity
parameter point and 4.30e-21/s for the small-cavity point. These numbers are
conditional on the assigned acoustic model, not measured silica losses.
Scans at 1, 4 and 300 K and speeds 3000, 6000 and 10000 m/s are in the results.

The normalization is checked in independent SI and natural-unit forms and by
regularizing the energy delta function around its nonzero root. The zero root
has vanishing phase-space weight. A continuum transverse mode has zero divergence
at this order, which does not exclude transverse surface or anisotropic effects.

Source context: Trickle, Zhang, Zurek, Inzani and Griffin, "Multi-Channel Direct
Detection of Light Dark Matter: Theoretical Framework", arXiv:1910.08092v3,
27 October 2021, sections II and V, checked October 14, 2026:
https://arxiv.org/html/1910.08092v3
The source distinguishes the particle coupling from the target dynamic structure
factor and derives single-phonon matrix elements. It does not calculate this
finite trap. The thermal absorption reference above is derived here under its
own explicit continuum assumptions, rather than importing a detector exclusion
or the paper's ground-state emission rates. HTML inspected; no local PDF cache.

The acoustic wavelength is comparable to the small cavity. Its wavefunction is
not a free particle at rest, and interfaces change modes and momentum selection.
Consequently multiplying Gamma_bulk by the wall occupation probability is NOT a
justified finite-trap rate. Surface motion, full elastic eigenmodes, final-state
scattering and thermal reverse processes need the actual trapped-state matrix
elements. This diagnostic cannot close the wall-loss budget.

## Exact energy sensitivities within the reference well

For an infinite-exterior spherical barrier U*Theta(r-a), write the normalized
radial wave as u(r). Hellmann-Feynman and differentiation of the step boundary give

    dE/dU = P_out,
    dE/da = -U |u(a)|^2.

The normalized s-wave formula used in the preceding source calculation evaluates
both derivatives analytically. Central finite differences at two step sizes
independently check them. For fractional barrier fluctuation eta and fractional
radius fluctuation epsilon, the pair transition frequency changes by

    delta omega_pair = K_U eta + K_a epsilon,
    K_U=2U P_out/hbar, K_a=2a(dE/da)/hbar.

The factor two counts the two particles in the pair transition. Interaction shifts
are neglected here, consistent with the tiny previous pair shifts. For uniform
isotropic dilation at conserved material mass, eta=-3epsilon, giving
K_dilation=K_a-3K_U. Barrier and boundary variations are correlated in that example;
adding their noise powers as if independent would be incorrect.

| Candidate | P_out | K_U, /s | K_a, /s | K_dilation, /s |
|---|---:|---:|---:|---:|
| Large | 0.389236 | 3022.61 | -6286.78 | -15354.6 |
| Small | 0.601979 | 330543 | -352842 | -1344470 |

These are derivatives of the infinite-exterior reference. The real energies of
the selected thick finite shells were previously checked against that reference,
but this does not certify their full noise response.

## State the spectral convention before giving a tolerance

For a stationary zero-mean Gaussian fractional fluctuation x, define the two-sided
angular-frequency spectrum S_x(omega)=integral dt exp(i omega t)<x(t)x(0)>.
For a smooth approximately white spectrum over the low frequencies relevant to
the preparation, and times long compared with its correlation time,

    gamma_wall = K^2 S_x(0)/2.

The corresponding one-sided per-Hz PSD is G_x(f)=2S_x(2pi f). Assigning an extra
phase-decay budget gamma_wall=1e-6/s gives sqrt(G_x)=2sqrt(gamma_wall)/|K|.
This is a diagnostic budget comparable to the small source rates, not a user
success criterion or an experimentally established noise floor.

| Candidate | Fractional barrier ASD limit | Uniform dilation ASD limit |
|---|---:|---:|
| Large | 6.62e-7 /sqrt(Hz) | 1.30e-7 /sqrt(Hz) |
| Small | 6.05e-9 /sqrt(Hz) | 1.49e-9 /sqrt(Hz) |

A white-noise ASD limit is not a bound on an unknown mean detuning, slow drift,
1/f noise, discrete mechanical resonances or nonlinear fluctuations. For a general
spectrum the coherence exponent is instead

    chi(t) = K^2/2 integral[domega/(2pi)] S_x(omega)
                        *4 sin^2(omega t/2)/omega^2.

For correlated barrier and radius fluctuations use the full spectral matrix
K_i S_ij K_j. Loss to other states additionally requires off-diagonal matrix
elements and spectrum at transition frequencies; diagonal dephasing alone cannot
supply it. No thermal equilibrium noise amplitude is inferred from the static U.

## Verification and decision

Thirty-eight checks pass: eight finite-difference energy derivative comparisons,
eighteen SI/natural-unit rate comparisons, and twelve regularized-delta integrals.
The bounded run pins the two parent results and script. No Lean theorem or
physical certification is claimed.

The simple bulk longitudinal channel is very weak in its assigned model, while
the derived phase sensitivity is a concrete constraint on the low-frequency
material response. Neither licenses dropping wall noise. The next real calculation
requires a finite-shell elastic spectrum and its coupling to the trapped orbital,
including interfaces. That response must be independently specified or derived;
a static mean barrier does not determine it. The cold-energy creation objective
and the particle's cosmological identity remain open.
