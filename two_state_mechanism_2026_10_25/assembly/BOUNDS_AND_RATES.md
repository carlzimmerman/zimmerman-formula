# Uniform restricted-network bound and linked radiative coefficients

For the computed finite spectrum let W=sum(2J+1) and D_max<B_A=.5.
Write A_mu=(mu_AX/mu_XC)^(3/2). Then at every T>0,
K_T/K_A=A_mu exp(B_A/T)/sum_j w_j exp(D_j/T) >= A_mu/W.
Together with t<=1/(2+sqrt(K_T/K_A)), this gives

f_T <= [(2M+1)/(M+1)]/[2+sqrt(A_mu/W)].

This removes alpha, light mass, density and temperature from the equilibrium
screen *for this four-species statistical model and its specified spectrum*.
At M100 the two meshes agree on15 rovibrational levels and W83, giving .48692047.
It is not a universal bound for the exact Coulomb potential: the LCAO basis
misses states/tails and other species/statistical factors change the network.
At M50 and1000 the corresponding coarse spectra give similar but separate
bounds. The80% threshold is an operational screen inherited from earlier work,
not a derived observational requirement or a theorem about astrophysical need.

The first environmental scan had no parameter point passing applicability in
all four profiles, because the cluster's minimum T/E_H=.08544 exceeded the
stated .05 ground-atom screen. Those raw maximum fractions therefore have no
physical interpretation as realizable galaxy compositions. Extend only alpha
to .15 and .2 to reach the previously missing applicability regime. Corrections
to the nonrelativistic electronic parent scale as alpha² (up to4% here); these
are not computed. Keep the original scan and its limitations intact.

For the selected molecular ground J0 to u-continuum J1 dipole channel, normalized
box eigenstates b and E_j have D_j=<b|R/(2sqrt(1-S²))|E_j>. In an isotropic
blackbody photon bath, the truncated photo-dissociation coefficient is

Gamma_PI(T)=4 alpha³/3 sum_(0<E_j<Emax) omega_j³ |D_j|² n_B(omega_j),
omega_j=E_j+D_0, n_B=1/[exp(omega_j/T)-1].

The continuum density is already represented by the discrete box strengths;
do not multiply by level-spacing again. This follows by combining the stated
dipole cross section with photon density omega²/(pi² c³)n_B and c=1/alpha.
Thermal detailed balance determines the inverse coefficient for this selected
channel (including stimulated emission):

k_RA(T)=Gamma_PI(T)/[(mu_AX T/(2pi))^(3/2) exp(-D_0/T)].

This is a derived thermal inverse relation, not an independent numerical test of
microscopic reciprocity. The selected angular/spin convention is the same as in
the spectrum calculation; unmodeled spin/exchange weights remain a limitation.
It supplies no independently adjustable forward/reverse rate. Units are E_H/hbar
for Gamma and a_D³ E_H/hbar for k. Both scale alpha³ in atomic units. Photon
energy E+D_0 explicitly balances matter binding/kinetic energy per event. This
bath-controlled coefficient calculation is distinct from the isolated-matter
chemical endpoints; we do NOT insert blackbody rates into them while omitting
the photon energy ledger.

Check boxes60/120 and Emax.25/.5 for T=.002,.01,.03. These finite checks do not
establish total radiative formation, excited-state branching, optical escape or
finite-age population assembly. No galaxy formation times are claimed.

A common local velocity boost, including the locally uniform part of rotation,
cancels from A-X relative energy and these internal matrix elements. Rotation
can matter through actual density, temperature, gradients, transport and
assembly history; adding an Omega-dependent multiplier to these coefficients
would not follow from this Hamiltonian.
