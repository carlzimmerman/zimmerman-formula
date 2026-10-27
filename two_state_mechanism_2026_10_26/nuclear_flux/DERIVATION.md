# What the new operators compute

## Electronic Hamiltonian and geometry

In dark atomic units, m_C=hbar=Q²/(4pi epsilon)=1. The charge+1 centers are
separated by R. In an orthonormal spatial orbital basis, the one-alpha/one-beta
Hamiltonian is H_ab,cd=h_ac delta_bd+delta_ac h_bd+(ac|bd)+delta_ac delta_bd/R.
Symmetric two-electron products with total Ag symmetry give the spin singlet
sector. The original aug-cc-pVDZ space has42 such states; the diffuse augmentations
used here give130,192 and266. These are finite Gaussian spaces, not a complete
physical electronic spectrum. Independent PySCF singlet FCI checks the lowest
three eigenvalues at selected separations.

The `rydbergN` basis adds N uncontracted s exponents0.02/3^j and p exponents0.04/3^j
per center. These are numerical basis choices tested for convergence, not new
Hamiltonian parameters fitted to galaxies. Their inadequacy must not be hidden
by shifting product thresholds to their exact values after solving dynamics.

## Projected radial nuclear operator

Let Psi_a(R_i) be orthonormal electronic eigenfunctions at each grid point and
O_i,ab=<Psi_a(R_i)|Psi_b(R_i+h)> include the actual moving-center AO overlaps.
For reduced nuclear mass mu=50, the symmetric second difference projects to

 H_ii=V(R_i)+2t I,  H_i,i+1=−t O_i,  H_i+1,i=−t O_i^T,
 t=1/(2 mu h²).

Hermiticity is exact in this discretization. The kinetic quadratic form is the
sum of squared differences of the physical electronic-valued nuclear amplitudes,
so it does not assume completeness of a small electronic-state subset. Its
continuum limit includes the derivative metric/projection terms. The norm outside
the retained electronic eigenstates is therefore not silently set to zero, unlike
using tau=d'+d² inside an incomplete state set. Omitted electronic states still
exclude dynamical channels and basis truncation still changes the potentials.

This is a radial, fixed-axis model. The `J:0` field in the earlier run_grid outputs
means that no centrifugal term was added; it is NOT a complete total-J=0 solution.
Ag includes electronic projections beyond Sigma. Rotational kinetic couplings,
full finite-mass center-of-mass corrections and nuclear spin statistics remain
absent. A final physical rate cannot inherit a J/spin weight from this shortcut.

## Outgoing modes and the failed ideal boundary

The first implementation attached a diagonal free lattice lead to the final
adiabatic energies. Its flux and reciprocity checks pass, but the moving electronic
basis retains asymptotic derivative couplings. Attaching an independent-channel
lead there creates an artificial interface. Those probabilities are not accepted
as physical branching. The raw calculations are retained as a diagnosed failure.

For a stationary coupled lead with onsite H0 and hopping W, solve

 [W lambda²+(H0−E)lambda+W^T] u=0.

Keep decaying modes |lambda|<1 and outgoing propagating modes with current
j=−2 Im(u†W lambda u)>0. Normalize the latter to unit current. If U contains all
outgoing/decaying modes, F=U diag(lambda) U^-1 and Sigma_right=W F exactly embed
this stationary lattice. Matching the incoming conjugate modes supplies the
reflected amplitudes; no absorbing-strength parameter is introduced.

The stationary lead uses the end-of-grid potentials and the overlap with the
next computed geometry, with electronic signs aligned. This is still a numerical
asymptotic approximation. Mode weights are retained so an arbitrary mode index
is not silently called an atomic product. Closely spaced excited atomic channels
can mix; comparing individual mode probabilities between different bases is not
an invariant product-branch comparison. Boundary and grid refinement remain
necessary. Current conservation by itself certifies neither.

## Microscopic electron capture/escape block

The corrected UKRmol calculation provides inner eigenvectors U, eigenvalues E_k,
and boundary amplitudes W_ck. Reconstruct H=U diag(E_k) U^T and B=W U^T.
The final42 configuration coordinates form the pure-target Gaussian singlet Q
space; the other644 form its continuum P complement. The identification is tested
by reproducing all Q eigenvalues with independent Gaussian CI and by finding
negligible Q boundary amplitudes. These Q coordinates are not yet tracked across R.

The pure-Coulomb exterior has retarded logarithmic derivative L_c. For an open
channel use (G'+iF')/(G+iF); for a closed one use the decaying Whittaker solution.
With the UKRmol boundary normalization,

 G_P(E)=[E−H_PP+B_P^T L(E) B_P]^-1,
 Sigma_Q(E)=H_QP G_P(E) H_PQ,
 A(E)=H_QP G_P(E) B_P,open^T sqrt(2 Im L_open),
 Gamma_Q(E)=i[Sigma_Q−Sigma_Q†]=A A†.

The optical identity is checked numerically, including positivity and the number
of open lead channels. This links capture and escape amplitudes using the same
Hamiltonian, with no guessed collision normalization. In energy-normalized
continuum conventions the coupling is A/sqrt(2pi). Diagonal entries of Gamma in
a chosen Q basis are NOT spontaneous lifetimes of off-shell bound levels and
are NOT thermal reaction coefficients. The whole energy-dependent resolvent is
needed. Pure-Coulomb outer matching neglects external multipole couplings; the
resulting S is compared against UKRmol's propagated matrix, not assumed exact.

A full nuclear Feshbach problem requires the operator

 Sigma_N(E)=H_QP [E+i0−H_PP(full electronic+nuclear)]^-1 H_PQ,
 [E−H_QQ(full electronic+nuclear)−Sigma_N(E)] chi_Q=source_P(E).

The source and escape term must be generated by the same entrance channels.
Replacing Sigma_N(R,R';E) with delta(R−R') Sigma_Q(R;E) is a local approximation,
not a derivation of full dissociation rates. The open ionic rovibrational channels
are not a complete nuclear basis at low energy. Principal-value energy shifts,
closed-channel structure, compatible state gauges and product thresholds matter.
The newly computed fixed-R A and Sigma_Q are inputs toward that problem, not its
solution. No arbitrary incoming nuclear wave or neutral reflection coefficient
is relabeled electron capture.

## Photon branch accounting

In the earlier leading-BO thermochemical convention, T_b has energy−.5−D_b,
A_1 has−.5 and A_2 has−.125. Therefore

 T_b+C -> A_1+A_1 : heat .5−D_b,
 T_b+C -> A_1+A_2 : heat .125−D_b,
 A_2p -> A_1+photon : photon energy .375.

The missing .375 is stored in excitation, then radiation; it is not immediate
thermal heating. The inverse line transition reabsorbs that photon. The Coulomb
2p->1s electric-dipole coefficient is

 A_21=(4/3) alpha³ omega³ |<1s|r|2p_m>|² /t_D
     =0.03901844231062337 alpha³/t_D,

where omega=.375 and the squared vector matrix element for each p magnetic
sublevel is [256/(243 sqrt(2))]². The numerical atomic calculation checks this
normalization. For the aggregate p triplet, emission minus absorption is
A_21[n_2p(1+f_gamma)−3 n_1 f_gamma]. f_gamma denotes phase-space occupation, not
photons per atom. This obeys thermal Einstein balance. Single-photon 2s->1s
emission is forbidden; two-photon decay has not been added.

branch_energy.py supplies the conservative event ledger and this physical E1
line term. test_branch_energy.py uses specified signed events only to check
algebraic energy/charge/constituent conservation. It does not supply physical DR
rates, their inverse coefficients, spectral photon occupation or galaxy transport.
The earlier photon solver has NOT been run with these unvalidated nuclear rates.
Its thermochemical approximation must be reconciled with finite-mass thresholds
before a physical coupling, rather than conserving an inconsistent energy ledger.
