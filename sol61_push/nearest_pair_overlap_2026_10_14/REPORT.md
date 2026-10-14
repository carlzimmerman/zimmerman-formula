# Nearest excited-pair overlaps and depleted-vacuum evolution

Parent checkpoint: 778a5e0bc66f4753c40c301e2f2de56243c8d8fd.
This follows the spectral check with actual optical and mediator matrix
elements for the ground pair and the three nearest p-p pairs of total
magnetic quantum number zero. It does not replace the parent's lossy
multipair calculation or establish the full physical preparation mechanism.

## Projection and angular factors

The pair basis is [s0 s0, p0 p0, p+ p-, p- p+]; the two entries in each
pair refer to different charge signs, so both ordered p+/p- states exist.
Use normalized radial functions v_l(x), integral v_l^2 dx=1, x=r/a,
matched from spherical j_l inside the reference well to decaying k_l outside.
With conventional complex spherical harmonics, the angular pair products are

    s0 s0: 1/(4 pi),
    p0 p0: (1+2 P2)/(4 pi),
    p+ p- and p- p+: (-1+P2)/(4 pi).

Thus c0=(1,1,-1,-1), c2=(0,2,1,1). The antisymmetric combination of the
last two channels is dark to these scalar sources.

Expand the optical source as F0 sum_L f_L(x) P_L(cos theta), with

    f_L(x)=(2L+1)/2 integral[-1,1]
           exp[-200 x^2(1-u^2)] P_L(u) du,

inside x<=1, zero outside. This is the parent's prescribed source, not a
Maxwell solution through the shell. Only L=0,2 contribute to these channels.
Define radial pair densities D_iL=c_iL v_i^2/x, where v_i is the s or p
radial mode, and the positive radial inverse operator

    A_L = [-d^2/dx^2 + L(L+1)/x^2 + C^2]^-1,
    C=a sqrt[2 M_R (delta-E*)].

Freeze E* at the preceding dressed ground-pair energy. Then

    Sigma_ij = -M_R h^2/(2 pi a)
               sum_L integral D_iL A_L D_jL dx/(2L+1),
    d_i = -2 M_R a^2 h F0
          sum_L integral D_iL A_L(x f_L) dx/(2L+1).

The projected contact matrix uses the same angular factors and the parent's
nonresonant coefficient (lambda-mu^2/(4 M_R^2))/(4 pi m^2 a^3).
Adding bare orbital sums, Sigma and contact gives a Hermitian four-channel
matrix. The optical drive d_i/hbar links vacuum to each pair channel.

The fixed-energy resolvent is an approximation. Its ground-energy response
is directly relevant to the pump; its excited eigenvalues are NOT
self-consistent excited-state poles. Derivative/residue normalization is not
included in this bare projected evolution. The ground drive, multiplied by
the parent's square-root residue, reproduces the parent's dressed drive.
No additional claim about the fully normalized mediator dynamics follows.

## Calculated matrix elements

Bare optical drive frequencies in the stated basis are

    [-8.70660, -10.52403, 2.50524, 2.50524] per second.

The p0-p0 source is slightly stronger than the ground source. Excited-mode
suppression therefore cannot be justified by assuming negligible overlap.
Ground-to-p0-p0 mediator mixing is -7.63871e-14 eV, and the two other
ground-to-p-p entries have the opposite sign. Diagonalizing the projected
matrix gives ground-state p-p admixture 2.04133e-8. The ground eigenenergy
changes by -1.89048e-17 eV from the parent value, corresponding to a small
required retuning. This includes numerical and projection differences as
well as excited-channel mixing; it is not assigned wholly to one effect.

## Propagation with vacuum depletion

Use vacuum plus the four one-pair eigenstates. Retune to the lowest matrix
eigenvalue and retain the parent's 0.185421246 s pulse with 5 ms ramps.
Propagation uses exact exponentiation of the midpoint Hamiltonian on each
time interval; thus the large static detuning is exponentiated rather than
resolved with a naive explicit timestep. Refine 2000, 4000 and 8000 intervals.

At 8000 intervals the lowest eigenpair population is 0.9999999151, compared
with 0.9999999152 from the isolated two-level analytic pulse. The largest
sampled occupation of the three other eigenpairs is 6.23e-11. Final excited
population is below 1e-14 at all tested resolutions. Raw values around 1e-18
are stored but should not be interpreted as certified physical probabilities.
The roughly 2e-8 bare p-p admixture is part of the dressed ground eigenstate;
it is distinct from population in excited eigenstates.

This propagation includes vacuum depletion, removing the preceding weak-source
Fourier-bound assumption for THESE channels. It excludes two or more pairs,
tunneling, all other losses and other orbital channels. Consequently the
near-unit lossless probability here is not an update of the parent's 93.8%
lossy multipair prediction. Integrating those sectors remains necessary.

## Verification and next work

Eleven checks cover radial and angular refinement, ground self-energy and
source agreement with the independent preceding BVP calculation, matrix
Hermiticity, propagation norm and time refinement. The radial inverse is
computed with tridiagonal finite differences on 12000/24000 intervals over
0<x<6, with zero endpoints. At the outer endpoint both the confined densities
and mediator solutions are exponentially small; no rigorous domain-error
bound is asserted. Angular quadrature uses 192/256 Gauss-Legendre points.
The bounded run and input/output hashes validate in run/manifest.json.
No new Lean proof or experimental certification is claimed.

The nearest p-p channels do not spoil selectivity in this calculation.
Remaining work includes additional even-parity pairs (notably s-d and radial
s excitations), energy-dependent mediator normalization and matching this
multimode calculation to the multipair/loss model. Independent major gaps
remain: physical existence and constraints of the assigned particles and
couplings, full material response, achievable optical mode, total losses,
and identity with the repo's cosmological cold component. The goal is open.
