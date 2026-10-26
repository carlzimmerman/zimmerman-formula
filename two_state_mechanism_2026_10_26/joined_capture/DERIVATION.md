# Signed capture map and nuclear elimination

## Configuration map

CONGEN stores CSFs as signed excitation operators on a reference determinant.
`qmap.py` applies the annihilation and creation operators with fermionic signs,
then converts each two-electron singlet into an alpha/beta spatial CI matrix.
Molden orbital labels fix the orbital permutation; no energy matching determines
signs. The independent Coulomb Hamiltonian is compared element by element with
UKRmol's recovered pure-target Q block at R=2,3,4.

For nuclear eigenstates |a(R)> and original Q configurations |q(R)>, define
T_aq(R)=<a(R)|q(R)> using cross-AO overlap integrals and the two-electron CI
contraction. The old Gaussian space is a subspace of each augmented basis, so
T†T=I. Transfer H_QQ, Sigma and A by T† H_nuclear T, T Sigma T†, and T A.
The identity i(Sigma-Sigma†)=AA† is preserved. This fixes the Q configuration
mapping. It does NOT determine relative entrance-channel phases across different
R, nor add omitted continuum configurations to the capture calculation.

## Fourth-order radial kinetic operator

With t=1/(2 mu h²), the finite-difference coefficients are
c0=5t/2, c1=-4t/3, c2=t/12. Off-diagonal electronic blocks are multiplied by
exact overlaps <a(R_i)|b(R_j)>; reverse blocks are their transposes. Grouping
sites (2i,2i+1) yields a nearest-block Hermitian chain. Use the previous coupled
lead mode calculation on these doubled blocks. No phenomenological absorber.
The free dispersion has error O(h⁴), checked independently.

The original pairing varied the inner endpoint with h. Subsequent runs put the
wall at a fixed R=.2, with sites R_wall+h through R_max. Values at and outside
the wall are zero in the truncated stencil; convergence is additionally tested
by moving this wall to .1 and .05. The true Coulomb endpoint is R=0, so a finite
wall remains an approximation. The exterior repeats the last two-site block and
its next overlaps; it remains an approximate molecular asymptote. No total-J
resolution, electron translation-factor treatment, or mass-polarization correction
has been added.

## Full Feshbach requirement

For a common orthonormal electron+nuclear basis, let P contain ion+electron
channels and Q neutral inner configurations. The required operator is
Sigma_N(E)=H_QP [E-H_PP-Sigma_boundary(E)]^-1 H_PQ.
Nuclear kinetic energy must be inside H_PP. Fixed-R Sigma_Q(R,E) is generally
not a replacement for this nonlocal operator. A physical source must use the
same resolvent and boundary normalization as its escape self-energy.

For the boundary convention used here,
G_P=[E-H_PP+B† L(E) B]^-1,
Sigma_N=V G_P V†,
A_N=V G_P B_open† sqrt(2 Im L_open).
Hermiticity of H_PP gives i(Sigma_N-Sigma_N†)=A_N A_N†. `feshbach_v2.py`
computes source and self-energy independently and checks this identity.
Synthetic checks compare a full Q+P inverse to the Schur solution and verify
unitarity of the effective channel scattering matrix at the same energy.

## Executed nuclear benchmark: explicit approximation

The R-dependent full P overlap matrices and continuum couplings are not yet
available. The executed benchmark freezes the electronic matrices at R=2 and
uses four bound vibrational eigenstates of the independently calculated
one-electron BO ionic Hamiltonian h_ion (mu=50):
H_PP^bench = H_PP(R=2) tensor I + I tensor [h_ion-V_ion(2)].
This uses the old electronic basis consistently. Its nuclear eigenvalues epsilon_v
fix the shifts lambda_v=epsilon_v-V_ion(2). At total E=epsilon_0+e_inc,
Sigma_N^bench(E)=sum_v |chi_v><chi_v| tensor Sigma_Q(E-lambda_v).
The same decomposition gives the incident source. Both real self-energy shifts
and closed electron channels are retained. In the R representation this operator
is nonlocal, even though the electronic interaction was frozen.

This spectral solution is exact for the declared separable, four-mode Hamiltonian,
not for the physical molecule. It has no nuclear product continuum and cannot
yield a dissociation rate or branching. The scalar ionic BO calculation omits
DBOC and rotation; its finite-basis thresholds are not exact finite-mass values.
Only e_inc=.001 and .05 are used: at .199 ionic dissociation is open, so the four
bound-state projection misses an additional continuum.

A comparison replaces all four vibrational blocks by their v=0 electronic width.
At .001 only one physical vibrational block is open in this benchmark; copying
it to four blocks opens three forbidden escape sectors. The relative Frobenius
width error is exactly sqrt(3), not a statement about a DR rate error. At .05 the
computed error is 1.06759. This rejects that local replacement for this benchmark.
It is not a universal bound on other local-potential approximations.

## Conservation and photon scope

Q and P both contain two positive nuclei and two negative electrons. Moving
between them preserves constituent counts and total charge zero. The retarded
stationary kernel conserves total E, including vibrational energy, with optical
flux balance. The existing branch ledger independently conserves constituent
counts, charge, chemical energy, kinetic heat and emitted photon energy for
specified events. Neither check supplies a missing microscopic reaction rate.

No new physical photon-recycling trajectory, rotating disk, gravity calculation,
RAR test, or disk/dwarf/cluster separation is reported. No galaxy-type switches
or extra fitted physical parameters have been introduced.

## External comparison

Hörnquist, Orel and Larson, Phys. Rev. A 109, 052806 (2024),
https://journals.aps.org/pra/pdf/10.1103/PhysRevA.109.052806,
uses a nonlocal autoionization operator summed over ionic rovibrational states.
Its local reduction relies on a completeness approximation to the open states.
This supports keeping nuclear thresholds explicit, but supplies neither our
mass-ratio-100 rates nor our microscopic potential data. Our finite benchmark
is derived from the recovered Hamiltonian; it does not import their fitted curves.
