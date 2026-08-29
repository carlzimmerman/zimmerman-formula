# KILL LEDGER (stage-1 response-space screen)

basis size 17: R3, KijKij_K2, aiai, aiD2ai, R3D2R3, chi2, chiR3, chiD2phi, chiDphi2, chiD2chi, QR3, QDphiDphi, QD2Q, QQ, QDm2Q, chiDm2chi, QDm2Dphi2

EXCLUDED FROM BASIS: time derivatives of auxiliaries (chi-dot, Q-dot) -- deliberately excluded to keep the auxiliary sector non-propagating (that is the design principle: degeneracy as a design variable, not an accident); operators above quartic in the carrier; k^6 and higher kernels; matter-sector modifications (matter stays minimally coupled to the single metric g).

evaluated 400000 canonical candidates

| gate | killed |
|---|---|
| SINGULAR | 187910 |
| CARRIER_OFF | 127893 |
| LENSING | 77274 |
| NEWTON | 6923 |

Gate order (lexicographic, cheapest first): ELLIP, SINGULAR, CARRIER_OFF, NEWTON, LENSING, PPN, DEGEN_ILLPOSED.

A candidate dying at CARRIER_OFF reproduces the minimal-AC-MOND failure (carrier algebraically forced to zero => no MOND).

A candidate dying at LENSING is a direct instance of the Part-I theorem.

---

## STAGE 2 (covariant): the constitutive_search.py candidate, 2026-08-29

Script: `routeA_alpha12_ppn_2026.py` (+ `.out`, 41/41 checks). Coupled (metric, khronon)
1PN solve, exact in the boost velocity w, validated against GR (alpha_1 = alpha_2 = 0,
gamma_PPN = 1 exactly) and against Blas-Pujolas-Sibiryakov arXiv:1007.3503 Eq. (5.34) at
beta = 0 (alpha_1 = -4 alpha, alpha_2 = alpha(alpha-lam2)/(2 lam2), both to 1 part in 1e3
at alpha = 1e-3, for lam2 = 1/3 and 1/10).

**PREFERRED-FRAME GATE: PASSED.** The static gates FORCE the a^2 coefficient to be
`g(chi) = 1 - chi = e^-y`, not `chi` (the literal spec has `mu_eff(y->0) = 1`: no deep-MOND
limit at all). The khronometric dictionary is then `alpha_khrono = 2(1-chi) = 2 e^-y`, and
`G_N = G/(1-alpha/2) = G/mu` reproduces MOND exactly. At Solar-System y = 7e4 - 3e12 this
gives `|alpha_1| = 8 e^-y` and `|alpha_2| ~ 2 e^-y`, i.e. < 1e-30000 against bounds
4e-5 and 1.2e-7. The carrier is additionally (v/c)^4 below the MOND sector: 2PN beyond 1PN.

**KILLED AT DEGEN_ILLPOSED instead.** `K_ijK^ij - K^2 + R3` is the Einstein-Hilbert scalar
(Gauss-Codazzi at lambda_K = 1), so `lam2 = lambda_K - 1 = 0` EXACTLY and the khronon has no
kinetic term. Then a_mu = D_mu ln N enters every non-GR term, so `a_mu == 0` is an exact
stationary point of the khronon EOM and nothing obstructs it. Computed directly at lam2 = 0:
sigma_hat has an alpha-INDEPENDENT `1/(w.k)` pole, `a_mu = O(w^2)` on-shell, `h_00 = 2 Uhat`
with NO G_N renormalisation. gamma_PPN = 1, alpha_1 = alpha_2 = 0 -- and no MOND: the force
is (w/c)^4 ~ 1e-12 suppressed. This is CARRIER_OFF re-appearing covariantly: the H3 escape
(degenerate, no-time-derivative auxiliary sector) is exactly what lets the khronon relax.

Separate finding (S3): the carrier cancels the MOND traceless stress only for a
chi-DEPENDENT kernel `M ~ (1-chi) V'(chi) = y^2 e^-y`. None of `m^2`, `-D^2`, `Delta^{-1}`
works. Note also (S1a) that `Psi = Phi` already holds from the GR sector alone at leading
order, carrier or not.

OPEN DOOR, not closed: `lambda_K != 1` restores a healthy khronon, keeps MOND, and still
passes alpha_1 and alpha_2 by ~1e30000. Its own gates (c_T, BBN lambda_K in [0.923, 1.100],
cosmology, and the chi-dependent Q kernel above) are UNTESTED.
