# Retention and driven production in the conditional miscible window

This extends the changed-parameter window with finite-wall poles and a recomputed
source overlap. It finds conditional low-occupation production with sufficiently
thick ideal barriers and prescribed coherent illumination. It does not establish
an apparatus, total lifetime, particle existence or cosmological identity.

## Finite shell, not an infinite-wall lifetime

Use the two candidate parameters from the preceding stable-window results:

| Candidate | Radius a | Detuning | mu | Assigned barrier U |
|---|---:|---:|---:|---:|
| Near resonant, large | 0.20 m | 2e-9 eV | 1.78885e-7 eV | 2.55567e-12 eV |
| Detuned, small | 0.02 m | 1e-5 eV | 1.26490e-5 eV | 1.80710e-10 eV |

The material model remains the prior Coulomb-only scalar response. For a shell
of thickness d with vacuum outside, impose an outgoing l=0 wave. In dimensionless
variables z=ka, q=sqrt(2mUa^2-z^2), with a in natural units, the pole equation is

    z cot(z) = [i z - q tanh(q d/a)] / [1-i z tanh(q d/a)/q].

Complex E=z^2/(2ma^2) gives Gamma=-2 Im(E) and tau=hbar/Gamma.
Independent transfer through the shell checks the outgoing boundary. Roots use
90 decimal digits; the longest-lived row for each candidate is repeated at 110.

| Candidate | Wall thickness | Pole lifetime, tunneling only |
|---|---:|---:|
| Large | 0.10 m | 0.000719 s |
| Large | 0.50 m | 0.0875 s |
| Large | 1.00 m | 16.3 s |
| Large | 2.00 m | 535641 s (6.20 days) |
| Small | 0.01 m | 5.20e-6 s |
| Small | 0.10 m | 0.00368 s |
| Small | 0.30 m | 166.5 s |
| Small | 0.50 m | 7201528 s (83.35 days) |

The thin 1 cm small-cavity pole lies above the barrier and is broad. Its inverse
width is only a resonance diagnostic, not a demonstrated exponential storage law.
For the two thickest shells, real energies agree with the infinite-exterior
reference to 2.21e-10 and 4.36e-13 relative, respectively. This supports using that
reference for a source comparison, but is not a bound on all wavefunction errors.

## Recompute the optical overlap

Prescribe I=1e12 W/m^2 in each wave and the preceding 2 mm Gaussian waist
(6.28 MW circulating per wave). This is an imposed source, not a solved optical
cavity through metre-scale material. Use the spherical-average source, truncated
at the cavity boundary, and the normalized infinite-exterior radial ground mode v.
Only 61.08% and 39.80% of each reference orbital lie inside its cavity.

For pair energy approximated by 2E0, set C=a sqrt(2M(delta-2E0)). The radial
mediator inverse is (-d^2/dx^2+C^2)^(-1), with zero value at the origin and a
decaying exterior. Source and pair-density right-hand sides are x*S(x) and
v(x)^2/x. Source overlap gives

    hbar Omega = -2 M a^2 h F0 integral [v(x)^2/x] w_source(x) dx,
    h=mu/(2m sqrt(2M)),

with F0 the previous canonically normalized optical source. The code rescales the
BVP unknown by C^2 for conditioning. Independent Green integrals at four radii
and BVP/quadrature refinement check the result. The reference energy levels are
2.02927e-12 eV and 1.66845e-10 eV, both small compared with the 1 eV rest energy.

| Candidate | Omega | Time with Omega*t=0.1 |
|---|---:|---:|
| Large | 1.91563e-6 /s | 52202 s (14.50 hours) |
| Small | 1.60974e-6 /s | 62122 s (17.26 hours) |

The net contact-plus-virtual pair shifts are approximately -1.59e-28 eV and
-8.30e-28 eV. Contrary to assuming a positive pair blockade from the bulk density
criterion, the midpoint choice nearly cancels the unlike-charge contact. These
tiny shifts must not be used to claim a two-level blockade. The source calculation
is first order in the pair mixing; its computed shift/gap is below 8e-20. This
small ratio does not bound every other omitted correction.

## Pair production with losses and common-laser phase noise

Retain two bosonic orbital modes and their leading quadratic pair drive. Let n
be mean occupation PER CHARGE, b the real anomalous moment in the drive phase,
kappa=1/tau the single-particle number-loss rate, and gamma=4pi*linewidth the
common-laser pair-phase diffusion rate. At assigned exact mean resonance,

    n_dot = 2 Omega b - kappa n,
    b_dot = Omega (2n+1) - (kappa+gamma) b.

The vacuum +1 term seeds production. These moment equations include bosonic
stimulation and singly surviving particles. A phase-diffused state need not be
Gaussian; closure of these second moments does not imply Gaussian statistics.
Mean occupation is NOT a one-pair probability.

At the comparison times above, using the thickest shells:

| Candidate | No phase noise | 1 microhertz linewidth | 1 millihertz linewidth |
|---|---:|---:|---:|
| Large, mean n | 0.0094043 | 0.0076572 | 0.000029004 |
| Small, mean n | 0.0099758 | 0.0078167 | 0.000025477 |

Zero linewidth is a control, not a physical laser claim. When
kappa(kappa+gamma)>4Omega^2, the quadratic model has

    n_stationary = 2Omega^2/[kappa(kappa+gamma)-4Omega^2].

At 1 mHz this gives 0.000312985 and 0.00298772. Some low-noise rows instead have
positive moment growth. This is unsaturated parametric gain in the quadratic
model, NOT unlimited energy creation or a high-population storage prediction.
The imposed pump supplies energy. Nonlinear shifts, other orbitals, depletion
and real noise must be included before extrapolating those rows.

## Verification and remaining creation requirements

Forty checks pass: 22 pole/precision checks, 14 source checks and 4 quantum-moment
controls. The lossless result n=sinh(Omega*t)^2 provides an independent moment
benchmark. Source and retention outputs are individually hashed by the bounded
run. No new Lean theorem is claimed.

The calculations exhibit nonzero production of cold orbital excitations under
specified model assumptions, while avoiding the old strong-coupling density
instability at the previously tested large-candidate bulk point. The small
candidate currently has threshold stability criteria, not a full finite-density
spectrum audit. They do not justify treating the millimetre-wall apparatus or old
preparation probabilities as retained after changing mu.

Outstanding requirements include full material response and wall noise; delivering
and stabilizing the assumed optical fields through thick shells; actual resonance
location and drift; readout; parameter constraints for these changed points; and
the connection to the cosmological cold component. The minimal next discrimination
is whether total wall-induced loss can be derived without overwhelming these tiny
driving rates. Tunneling alone cannot settle it. The original goal remains open.
