# QX2 iter 5: the K(Q) dust term mu_K^2 psi (AeST-type hydrostatic dust)
Frozen before code. Extra density delta rho_K = -mu_K^2 psi / (4 pi G) (V3_FULL_PICTURE 4.4). Generous upper bound:
psi = the potential of the MEASURED hydrostatic mass (deeper than any model with less mass), zero at 3 R200 (taken
from xcop_r500_ettori2019.json), M_K(<r) = (mu_K^2/G) Int_0^r |psi| r'^2 dr', with no self-consistent back-reaction
and no oscillation (both of which only reduce it). M_model = law(M_b) + M_K.
- Graded at mu_K = 0.1 Mpc^-1, the isolated-galaxy lensing bound (S4) that keeps the galaxy passes. Gate G-X.
- Reported, not graded: the mu_K at which the mean Delta reaches 0, against S4's bound 0.1 and BS's cap 10 Mpc^-1.
  Being at most the BS cap does not keep galaxies; S4 found 0/1804 cells pass above the galaxy bound.
MUTATE: mu_K = 10 Mpc^-1 (BS cap) must move the mean by > 0.05 dex.
