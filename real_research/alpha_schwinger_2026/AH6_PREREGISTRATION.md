# AH6 -- the Kaluza-Klein route to alpha: a charge-quantization principle (pre-registration)

Written 2026-09-28 BEFORE `ah6_kaluza_klein.py` was run. Follows AH5, which showed the a0 chain cannot output alpha (no hbar, no charge) and that a derivation
needs a new charge-quantization principle or a forced f(x). KK is the standard example of the first: the charge of a momentum mode is set by geometry.

## The idea being tested

5D gravity on a circle of radius R. The metric components g_{mu 5} are a U(1) gauge field (the graviphoton); a mode with 5th-direction momentum n/R carries charge
e_n = n e_0 with e_0 fixed by G and R. If the observed electromagnetism were this U(1), alpha would be a function of R/l_P and the charge would stop being an independent input.

## What is derived (checked by computer algebra, not recalled)

Units hbar = c = 1, Heaviside-Lorentz (alpha = e^2/(4 pi)). Ansatz ds^2 = eta_{mu nu} dx dx + (dw + kappa_g A_mu dx^mu)^2 (kappa_g is the KK gauge parameter, not the framework's kappa):
* K1: the 5D Ricci scalar is R_5 = R_4 - (kappa_g^2/4) F_{mu nu} F^{mu nu} (coefficient checked with a nontrivial background A_y(x) by sympy).
* K2: the mode operator g^{MN} p_M p_N = g^{mu nu}(p_mu - kappa_g A_mu p_w)(p_nu - kappa_g A_nu p_w) + p_w^2 (checked by sympy), so a mode e^{i n w/R} has charge coupling kappa_g n/R.
* K3: reducing (1/(16 pi G_5)) Int R_5 over w in [0, 2 pi R] gives G_4 = G_5/(2 pi R) and gauge kinetic term (kappa_g^2/(16 pi G_4)) (1/4) F^2; canonical normalization sets
  kappa_g^2 = 16 pi G_4, hence e_n = n sqrt(16 pi G_4)/R and  alpha_n = 4 n^2 l_P^2 / R^2.  Also e_n^2 = 16 pi G_4 m_n^2 for m_n = n/R (the extremal KK charge-to-mass ratio).

## What the script must then compute (in this order)

1. K1-K3 as above (sympy; exact).
2. Requirement: for n = 1 and alpha = 1/137.035999177, R = 2 l_P / sqrt(alpha); report R/l_P, R in metres, the carrier mass M_KK = hbar/(R c) in GeV and its ratio to the electron mass.
3. Programme-native and natural handles on k = R/l_P, declared now (a fixed list, so the trial count is 7): k in {1, 2, sqrt(8 pi/3), Z = 2 sqrt(8 pi/3) = 5.7888, 2 pi, 4 pi, Z^2 = 32 pi/3}.
   alpha = 4/k^2. A handle HITS if alpha is within 1e-3 (relative) of 1/137.035999177.
4. Integer flux route: R = N l_P with N integer gives alpha^-1 = N^2/4; report the two nearest integers (N = 23, 24) and whether either hits.
5. The electron obstruction: a KK momentum mode has m >= hbar/(R c) (m^2 = (n/R)^2 + m_5^2). The observed electron has charge e and m_e = 0.511 MeV. Report m_e R c/hbar.

## Pass / fail criteria (declared now)

* VALID: K1, K2, K3 checks all pass, and the MUTATE control fails (a deliberately wrong coefficient, R_5 = R_4 - (kappa_g^2/2) F^2, must FAIL the K1 check).
* The route DERIVES alpha only if (a) some declared handle or integer N hits alpha to 1e-3 AND (b) it is forced by the programme's inputs AND (c) the electron obstruction is absent
  (m_e R c/hbar >= 1).
* Expected outcome, stated in advance: K1-K3 pass; the required R is about 23.4 l_P and M_KK ~ 5e17 GeV; no handle and neither integer N hits; the electron obstruction FAILS by ~21 orders
  (m_e R c/hbar ~ 1e-21). So KK trades alpha for the free modulus R and cannot host a light charged particle: no derivation.

## Scope / not tested

* Radion stabilization (flux, Casimir), the 5D cosmological constant, higher-dimensional or non-abelian KK, and 5D matter with its own gauge charge (there e is a free 5D coupling, so nothing is derived)
  are NOT tested. The claim is only about the graviphoton charge quantum and the declared handles.
* kappa = 1/2 stays FITTED; the SM mass sector stays walled. A positive result on (a) alone would be a value match, not a derivation, unless (b) and (c) also hold.
