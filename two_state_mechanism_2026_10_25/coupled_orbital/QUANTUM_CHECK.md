# Quantum countercharge benchmark and parameter ties

The 3D solver uses Ehrenfest factorization. Energy conservation alone does not
make its electronic relaxation exact. Test the same electric countercharge
coupling in a small fully quantized model, not by adding a damping rate.

Consider a single orbital doublet sigma and a neutral cell's relative ionic
coordinate x. The polarization is d sigma_x-Qx. In a longitudinal fixed-D mode,

H=Delta sigma_z/2+p²/(2M)+Kx²/2+kappa(D-d sigma_x+Qx)²/2.

D is a fixed displacement-flux sector, not a prescribed local electric field.
E=kappa(D-d sigma_x+Qx) is an operator. The local pair is neutral; no charged
species is created. This mode reduction does not supply a propagating 3D bath.
At D=0, sigma_x²=1 gives
Omega²=(K+kappa Q²)/M,
x_zpf=sqrt(hbar/(2M Omega)),
g_q=-kappa d Q x_zpf,
H=Delta sigma_z/2+hbar Omega(b†b+1/2)+g_q sigma_x(b+b†)+kappa d²/2.

The same Coulomb energy fixes the mode stiffening and the transition coupling;
there is no separate decay coefficient. Positive complete-square energy is
retained; do not drop the countercharge self-energy. Delta is a chosen orbital
splitting (or a selected band transition), not a derived material gap.
Parameters M100,K10,kappa1,Q1,d.2 match the dimensionless 3D tests, except its
elastic K is here the stiffness of the selected mode. This is a local
countercharge oscillator example, not a mode-by-mode projection of that lattice.

Start |excited> tensor |0>. For resonant Delta=Omega and weak |g_q|/Omega,
rotating-wave reasoning predicts exchange time pi/(2|g_q|) and Rabi frequency
2|g_q|. We evolve the full Rabi Hamiltonian including counter-rotating terms,
not that approximation, and test Delta/Omega=.5,1,2. Truncate16 and24 oscillator
states; check energy, unitarity, edge occupation and agreement. Quantized
coupling should transfer energy even though <sigma_x>=<x>=0 by parity. A
factorized Ehrenfest model started with these zero expectations remains stuck.
The exact exchange is reversible; no irreversible formation or universal
forward/reverse Markov rate is inferred. A thermal many-mode bath would require
its full state, spectrum and matrix elements for detailed balance.

Primary literature check, 2026-10-25: 'Modelling non-adiabatic processes using
correlated electron-ion dynamics', EPJ B (2010), publisher abstract:
https://epjb.epj.org/articles/epjb/abs/2010/19/b100364/b100364.html . It describes
Ehrenfest's missing spontaneous-phonon contribution and a correlated extension.
We use only that methodological scope; no numerical material parameters or
formalism are imported from the abstract. Our exact benchmark supplies its own
evidence. This does not establish novelty.

This replaces two independently chosen effective parameters (mode frequency
and coupling) with their common electric origin, conditional on M,K,kappa,Q,d.
It does not derive those material parameters, a0, band assembly or the macroscopic
transport lifetime. Galaxies cannot yet be assigned microscopic time units.
