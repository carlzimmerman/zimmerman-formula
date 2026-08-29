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

---

## STAGE 3: the "sf42 route" -- MOND carried by an INDEPENDENT auxiliary potential Phi, 2026-08-29

Script: `dirac_Phi_Q_sf42_route_2026.py` (+ `.out`, 61/61 checks, exit 0). Tests the repair
proposed by the previous round's Dirac analysis: replace `phi = ln N` by an independent
auxiliary potential `Phi`, keeping the frozen `V'(chi) = -[ln(1-chi)]^2` and the new carrier
`f(chi) = chi V'(chi) -> -mu(y) y^2 = Sigma_P^cov`.

**VERDICT: EXTRA_MODES + STRONG_COUPLING (+ independent LENSING_FAIL). N_dof = 3, not 2.**

* `delta C_N / delta N == 0` EXACTLY -- the entry that failed last round IS repaired [PROVEN].
* But `{pi_N, C_Phi} = -delta^2 U/delta N delta Phi = d_i[J^i .] != 0`, J^i the MOND flux.
  C_chi and C_Q are ALGEBRAIC so N divides out; C_Phi is a DIVERGENCE with N inside it and it
  does not. The obstruction is RELOCATED (N,N) -> (N,Phi), not removed.
* det(Delta) = det(W)^2 [exact 16x16 integer check]; bordered reduction `det W = -(k.J)^2 det B`
  [PROVEN]. rank 16 generically => `N_dof = (1/2)[34 - 12 - 16] = 3` (2 tensor + 1 MOND scalar).
* RANK NOT CONSTANT, and worse than last round: `det W ~ y^5` at y = 0 (was y^2), zero for every
  mode with `k` PERPENDICULAR to `D Phi`, and zero on `m^2 = (2/3) mu y^6`.
* Quadratic action about Minkowski is EXACTLY quadratic Einstein-Hilbert (Phidot cancels
  identically; the khronon enters only via `sigma = D Phi . grad tau`; chi at O(eps^3), Q at
  O(eps^10)) => the third mode has zero quadratic action on the vacuum = INFINITE STRONG
  COUPLING. About a MOND background it is a healthy scalar with kinetic coeff mu and DERIVED
  `c_par^2 = 1 + y mu'/mu -> 2` in deep MOND (superluminal, RAQUAL liability), `c_perp^2 = 1`.

**NEW NO-GO (general, and it also retro-explains stage 2's S3).** For any Lagrangian depending
on Phi only through `X = (D Phi)^2` -- which is what eliminating an algebraic TF carrier coupled
to `A_ij = [D_i Phi D_j Phi]^TF` always returns -- the traceless stress and the Gauss-law flux
are the SAME function:
        `Sigma^TF_ij = (dL_eff/dX) A_ij` and `J^i = -2 (dL_eff/dX) D^i Phi`.
Hence **Sigma_P = 0 <=> J^i = 0 <=> no MOND force.** Matching PROFILES `f(y) = Sigma_P(y)` is not
a cancellation: eliminating Q returns `(1/2) f^2 |A|^2/m^2`, so the carrier's stress is QUADRATIC
in f while the obstruction is LINEAR in the constitutive function. Verified twice (envelope
theorem; independent direct plane-symmetric dL/dE variation, residual 0).

**The new carrier is also worse in y.** `f = chi V'` is analytic in chi (`-chi^3 - chi^4 - ...`,
the handover's claimed advantage -- CONFIRMED) but `f'(chi) = -y^2 - 2 y e^y + 2 y` is
EXPONENTIAL in y, where last round's `f_old = (1-chi)sqrt(-V')` had the polynomial `f_old' = 1-y`.
The Q back-reaction carries exactly `f f'`, so the self-consistent constitutive relation
`(2/3)(f f'/m^2) X^2 - X + yt^2 = 0` has a real root only while `m^2 >= (8/3) f f'(yt) yt^2`:
yt is CAPPED at ~ln(m^2) (m^2=1 caps yt<0.75, i.e. inside the MOND transition; m^2=1e120 caps at
247). mu_eff turns over and NEVER reaches 1 -- **the Newtonian limit is unreachable for any sane
kernel mass**, and `|Q| ~ mu y^4/m^2 ~ 1e24/m^2` at Solar-System y.

**Matter coupling (decided and stated).** Adopted C1, conformal `g~ = e^{2 beta Phi} g`.
beta = 1/2 gives `div[mu grad Phi] = 4 pi G rho` EXACTLY at Q = 0, but `G_eff/G = 1 + 2 beta^2`
strictly > 1 for any bounded mu [PROVEN algebraically] -- G_eff = G_N needs a bare-G rescaling.
And conformal scalars do not lens: the scalar's gravitating density is ~1e-7 of the phantom
density (computed), so lensing stays Newtonian while dynamics is MOND. Moving MOND off the lapse
moves the candidate OUT of the metric-carried class (where Sigma_P is an O(1) obstruction and a
carrier is the right idea) INTO the frame-carried/TeVeS class (where Sigma_P is a 1e-7 effect):
the carrier is aimed at the wrong target as well as unable to hit it.

T5 (alpha_1, alpha_2) NOT_REACHED; no number produced or guessed.

**OPEN DOORS (none closed here):** (a) a carrier coupling to something other than X --
`Q^ij R_ij`, `Q^ij K_ij`, anything LINEAR in the metric perturbation -- evades the new no-go;
(b) the DISFORMAL matter coupling C2, `g~ = e^{2b Phi}(g + u u) - e^{-2b Phi} u u` with u the
foliation normal this theory ALREADY carries (the TeVeS lensing cure at zero extra field cost);
it fixes the frame slip but touches nothing else above; (c) making Phi genuinely DYNAMICAL
(restore Phidot) -- 4-diffeo invariance and first-class H_perp return, at the price of an openly
propagating scalar (RAQUAL), a different theory; (d) a y-dependent kernel KK.

**Invariant lesson.** `N sqrt(g)` is the integration measure, so the lapse always weights the
MOND flux; an auxiliary MOND field cannot be hidden from the Hamiltonian constraint.
