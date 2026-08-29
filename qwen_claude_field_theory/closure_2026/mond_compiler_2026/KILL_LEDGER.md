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

---

## STAGE 4 (ADVERSARIAL REFUTATION of Route A and Route B), 2026-08-29

Scripts (written from scratch, importing nothing from compiler.py / mc_*.py / routeA_* /
ppn_khronon_routeB_* / sec11_*):
  `adv_refute_static_carrier_2026.py` (+ `.out`, 21/21)  -- dictionary, static gates, carrier, GR branch
  `adv_refute_ppn_2026.py`            (+ `.out`, 19/19)  -- independent 1PN preferred-frame engine

**VERDICT: both routes' KILL verdicts STAND and are strengthened; two of their named
sub-results are corrected; one of Route A's is REFUTED.**

### Independently reproduced
* ADM <-> khronometric dictionary is now PROVEN on explicit components, not asserted:
  for hypersurface-orthogonal u, `nab_m u_n nab^n u^m == K_ijK^ij` and `(nab.u) == K`, so
  `K_ijK^ij - K^2 + R3` is EXACTLY Einstein-Hilbert => `bet = lam = 0` EXACTLY (A1-A3).
* My engine reproduces the published khronometric PPN (Foster-Jacobson taken to the HO limit
  IN-SCRIPT, `c1 -> oo` at fixed `c14, c13, c2`) exactly at 5 rational points, and reproduces
  Route B's approach table DIGIT FOR DIGIT: alpha_1 = -16/5, -16/11, -88/101, -808/1001 and
  alpha_2 = -2/5, -50/99, -6424/4545, -5135749/450450 at delta = 1/2, 1/10, 1/100, 1/1000.
  Sign dictionary: our (alp, bet, lam) = aether (c14, -c13, -c2).
* AT the locus, for SYMBOLIC w, the on-shell first-order acceleration `a_mu^(1) == 0`
  IDENTICALLY (F3a) -- MOND switches itself off.  Exact in w, not "O(w^2) suppressed".
  At w = 0 exactly, a_mu != 0 and G_eff/G = 1/(1-alp/2): DISCONTINUOUS (F3b).  Off the
  locus at bet=lam=1e-3 with the SAME w, MOND survives (F3c).  System rank is 7/7 (full)
  at the locus with w != 0 and drops to 6/7 at w = 0 (F4).

### Why (deeper than either route stated)
**EXACT GR BRANCH THEOREM [PROVEN].**  At bet = lam = 0 every non-GR term is at least
QUADRATIC in a_mu, and the frozen V has V'(chi) = 0 only at chi = 0 with V(0) = 0.  Hence
`(any GR solution, any GEODESIC slicing T, chi = 0, Q = 0)` solves EVERY field equation
exactly, for EVERY source (e.g. exact Schwarzschild with the Painleve-Gullstrand foliation).
GR-with-no-MOND is an exact branch; nothing selects the MOND branch.  This closes only at
bet or lam != 0, where the khronon EOM carries K_ij / K terms that do not vanish on a
geodesic foliation.
**And the linearised khronon operator at the locus is `~ alp k^4 (w.k)^2/(1-w^2)^3`**: no
time derivative, ZERO at w = 0, degenerate for every k PERPENDICULAR to w.  This is
c_123 = 0 <=> c_s^2 = 0 <=> the lambda_Horava -> 1 strong-coupling point.  So
"alpha_1 = alpha_2 = 0 at the locus" is not a physical pass -- it is the unique solution of a
singular limit whose neighbours give alpha_1 -> -4 alp and alpha_2 -> infinity.

### Corrections to the routes
1. **REFUTED (Route A, S3).**  "The carrier cancels Sigma_P for the chi-DEPENDENT kernel
   `M = (c_Q/c_M)(1-chi)V'(chi)`; a repair, not a no-go."  FALSE.  Eliminating the auxiliary
   TT tensor EXACTLY gives `L_on = (1/2)(f^2/M) A_ij A^ij = (f^2/(3M)) A^2` -- for ANY LOCAL
   kernel (algebraic, chi-dependent, y-dependent) this is a pure redefinition
   `F(A) -> F(A) - f^2 A^2/(3M)`.  The carrier adds NO new tensor structure, so hypothesis
   (H4) is never violated and the Part-I theorem applies verbatim to the redefined F.
   Route B's order-counting (carrier stress O(a^4) vs Sigma_P O(a^2)) is the same fact.
   Only genuinely NONLOCAL M escapes -- and that is an (H1)/(H2) escape, not (H4).
2. **CORRECTED framing (both routes).**  The Solar-System suppression has NOTHING to do with
   `f(chi) -> 0`.  The static gates force the a.a coefficient to be `alp_kh(y) = 2(1-mu(y))`,
   so `alpha_1 = -8(1-mu(y))` and `alpha_2 = -(1-mu) + 2(1-mu)^2/c2 + 3(1-mu)^2` -- generated
   by the LAPSE-TIED MOND SECTOR ALONE.  1e-2751 is a property of the FROZEN kernel e^{-y}.
   With the framework's own canonical mu (g_obs = sqrt(g_bar^2 + g_bar a0)) the suppression is
   only 1/(2y): |alpha_1| = 6.3e-8 at Earth, 5.7e-6 at Saturn, 5.7e-5 at Neptune (bound 1e-4).
3. **NEW liability.**  Deep MOND needs `alp_kh -> 2`, i.e. `c14 -> 2` -- the OTHER pole of
   alpha_2 (the `1/(2-alp)` factor) and the edge of the aether stability domain 0 <= c14 < 2.
4. **The literal spec is not a MOND theory** (both routes found this; re-derived here from the
   candidate's own ADM action).  With coefficient `chi` and the frozen `V' = -[ln(1-chi)]^2`,
   `mu_eff = 1 + F'/2 = 1 +- chi/2` lies in [1, 3/2] (or [1/2, 1]): no deep-MOND limit for
   EITHER sign, and G_eff/G_N = 2/3 or 2 at high acceleration, violating the compiler's own
   frozen gate.  The repair needs coefficient `2(1-chi)` and `V' = -2[ln(1-chi)]^2` -- on which
   branch the advertised carrier coupling `f = (1-chi) sqrt(V')` is IMAGINARY.  The one
   "exactly verified" identity of the design was computed on the non-MOND constitutive law.

### Both-ways finding (reported because it cuts FOR the candidate class)
The Part-I traceless stress is real (`Sigma^TF_ij = -F'(A)[d_i phi d_j phi]^TF`, same F' that
multiplies the Gauss flux, so `Sigma_P = 0 <=> mu_eff = 1 <=> no MOND` -- PROVEN), but the
metric slip it induces is small: solving the linearised slip equation exactly for a deep-MOND
point mass gives `|d(psi-Phi)/dr| / |dPhi/dr| = sqrt(G M a0) = v_flat^2/c^2`, i.e. 1.4e-8
(dwarf), 5.4e-7 (Milky Way), 1.0e-6 (massive spiral).  mc_gates.py's physical FRAME_SLIP test
is the right one; its SIGMA_P_NONZERO kill is built on a cancellation residual, not a
magnitude.  Worth re-examining before Part-I is used to kill a metric-carried candidate.

---

## STAGE 2B (independent adversarial arm): refutation audit + degenerate-branch deep dive, 2026-08-29

Scripts (all committed, all self-checking, run clean): `stage2b/s2b_palatini_identity_2026.py`
(10/10), `stage2b/s2b_degenerate_branch_2026.py` (35/35), `stage2b/s2b_refute_2026.py` (19/19),
with `.out` logs and per-gate JSON certificates. Written independently of the other verifier's
modules (no import of `mc_*`; `screen_results.json` / `basis.json` read as DATA only).

### (i) REFUTATION VERDICT: **NO_SURVIVORS_TO_TEST** -- but the emptiness needs re-labelling

Nothing was claimed, so nothing is refuted or upheld. What changes is the STATUS of the zero.

The audit targets the 61 deepest non-survivors. Independent identification: they are
**Bekenstein TeVeS**, rediscovered from the 65-parameter basis (M5/M1 = 4.000 for all 59 with a
vector disformal term; linearising `g~ = e^{-2 lam phi}(g+AA) - e^{+2 lam phi}AA` gives
M1 = -lam, M5 = -4 lam exactly). The two exceptions are itemised in the log (one algebraic
vector with V6+V9 instead of Maxwell; one tensor-disformal S_mn variant).

The five named failure modes, each tested by re-deriving the physics analytically:

| mode | verdict |
|---|---|
| (a) secret G_N rescale | **DOES NOT APPLY.** `L_s = -(1/2)chi X + (1/3)chi^3` eliminates to mu_s = \|grad phi\|/sqrt(2); the fifth force grows as sqrt(g_N) and self-extinguishes, so G_eff/G_N -> 1 with no bare-G rescale. (Independent check: g_N = Sigma/8 exactly at 16 pi G = 1, confirming NEWTON_G_FACTOR.) |
| (b) mu actually constant | **DOES NOT APPLY.** Analytic mu(y): mu -> 1 at large y, d ln mu/d ln y -> 1 EXACTLY in deep MOND. Screen's measured slopes 0.919-1.004 agree. |
| (c) strong coupling mislabelled as second class | **N/A for this class** (their vector propagates: Maxwell + unit-norm). But Gate-H2 passes them while leaving up to 13 null directions unclassified -- an unestablished gate, in the direction of leniency. |
| (d) measure-zero tuning | **DOES NOT APPLY.** M5 = 4 M1 is an exact consequence of the single-function disformal map, not a tuned surface. |
| (e) zero traceless stress | **APPLIES mechanistically, NOT observationally.** MOND is FRAME-carried: rho_scalar/rho_phantom = Phi/(2c^2) ~ 1e-7 at galaxy scale (screen's own metric_carried_frac ~ 1e-13). They pass G2 as an observable (Phi~ = Psi~, both enhanced) and fail G2's parenthetical (T^carrier_TF != 0). **G2 is ambiguous as written and the ambiguity selects different theories.** |

**Three findings on the gate that actually killed them (Gate-PPN).**
1. Its KILL direction is not a theorem. The forward direction (boost-invariant vacuum =>
   alpha = 0) is sound; the converse is false, and the degenerate Palatini branch below is an
   explicit COUNTEREXAMPLE (timelike boost-breaking VEV, alpha_1 = alpha_2 = 0 exactly).
2. Bookkeeping: the gate's own comment says these are "reported, not scored", but the mortality
   table counts them as killed. Honest statement of the run: **0 survivors, 58476 physics kills,
   17551 solver-undecided, 23991 never-constructed, and 59 GATE-UNDECIDED.** The 59 are not
   refuted.
3. Coverage gap at exactly this gate: the basis has K3 (c_2), K4 (c_1=-c_3), K5 (c_1) but **no
   acceleration-squared operator a^m a_m (c_4)**, which is degree 4 and inside the stated cap.
   In the one limit with a validated dictionary in this directory (khronometric, BPS 5.34 via
   `routeA_alpha12_ppn_2026.py`), alpha_1 = -4 c_14, so alpha_1 = 0 needs c_4 = -c_1: the search
   could not have found that root. NOT quoting the HO extrapolation as a kill: it is derived for
   a hypersurface-orthogonal aether, and its lambda = c_2 = 0 is exactly the degenerate point
   where the companion script's direct computation found the formula misleading.
   **alpha_1, alpha_2 for the deepest class remain NOT ESTABLISHED in both directions.**
   RECOMMENDATION: a direct 1PN solve of the K4+V15 vector sector decides 59 candidates.

Also confirmed: the screen never independently tested Part I's Sigma_P branch (its
curvature-coupled sweep reached Gate-SLIP zero times). Every lensing kill in the run is a
FRAME-slip kill. Part I is inherited, not reproduced.

### (ii) DEGENERATE-BRANCH DEEP DIVE: the archetype is CARRIER_OFF in disguise

`R(Gamma) = R(g) - 3 div A + 3 A^2` **verified independently** (exact rational jets, 4 random
metrics, coefficients metric-independent). Closure PROVEN by enumeration and verified for 7
torsion-free (alpha=beta,gamma): a vector distortion can reach the action ONLY through
{div A, A^2}, and div A is a total derivative at constant coefficient. Torsionful members
(alpha != beta) declared OUT OF SCOPE, not failed (basis exclusion #1 + convention ambiguity).

On the degenerate branch chi = -3/25:
* **Q2** A IS nonzero -- but `A^2 = a0^2 V'(-3/25)/25` is a **UNIVERSAL CONSTANT** (V' is
  evaluated at frozen chi), and the DIRECTION is fixed by no field equation. A constant-norm
  vector interpolates nothing: G1 is dead before any stress question is asked.
* **Q1** PARTIAL. rank(M) = 2: (A_parallel, dchi) IS a genuine second-class pair; the 3
  transverse components are UNDETERMINED MULTIPLIERS, not second-class. So this is not
  "det H = 0 with a genuine second-class constraint" in Part I's sense.
* **Q4/T2** `T_mn|_branch = -a0^2 V(-3/25) g_mn` EXACTLY -- a pure cosmological constant.
  **Sigma_P == 0 identically**, because the coefficient P(chi) = 3+25chi that degenerates the
  A-equation is the same coefficient that multiplies the entire carrier stress.
* **Q3** Field equations are exactly GR + Lambda => mu == 1. NO MOND.
* **Q4** Phi - Psi = 0 and alpha_1 = alpha_2 = 0 EXACTLY -- **vacuous passes**.
* **Q5** The naive expectation survives and is worthless: no ghost, no strong coupling (the
  degeneracy is exact, not a limit), no propagating mode, no preferred-frame pole -- and no
  carrier. Failure mode (d) does NOT apply: chi = -3/25 is a field value, not a tuning.

Gate verdicts: **G1 FAILED, G2 FAILED, G3 PASS (vacuous), G4 PASS (vacuous), G5 PARTIAL.**
Escapes E1-E5 each followed to death in the log (D1 chi div A turns the vector into minimally
coupled QUINTESSENCE; K3 makes A_0 a ghost; K4 returns to the aether jaw; C4 is background-
dependent with non-constant rank; matter coupling over-determines; a tensor chi^{ab} carries no
metric dependence at all).

### NEW THEOREM (and an OPEN DOOR it leaves)

For ANY algebraic carrier `S = int sqrt(-g)[C^{ab}A_aA_b + B^aA_a + L_0]` with `C^{ab}n_b = 0`:
(i) `B.n != 0` -> over-determined; (ii) STRUCTURAL degeneracy (holds identically in g) ->
`A -> A + c n` leaves L exactly invariant, dT_mn == 0, WELL-POSED; (iii) CONFIGURATIONAL
degeneracy -> `dT_mn = -2 (d Delta/d g^{mn}) F(c) != 0`, ILL-POSED with non-constant rank.
**Corollary 1:** the isotropic case `C = P g` (the only <=2-derivative option without a
curvature coupling) has dim ker = 4 at P = 0, so Sigma_P == 0. **The archetype's whole class is
CLOSED** -- this is the vector-sector twin of Part I's "the same mu controls the Gauss law and
Sigma_P".
**Corollary 2 -- DOOR LEFT OPEN, and it is the recommended next target:** a STRUCTURALLY
degenerate ANISOTROPIC `C^{ab} = N(q^a q^b - q^2 g^{ab})`, q_a = d_a chi, has dim ker = 1. It is
well-posed, non-propagating in A, and its three DETERMINED components carry a NONZERO traceless
stress (verified: TF_11 = -TF_22 = beta^2/(4 N kappa^2), independent of the undetermined
component). Eliminating A returns `L_eff = (1/(4 N q^2))[B^2 - (q.B)^2/q^2]` -- a non-polynomial
function of the kinetic invariants generated from a FINITE operator basis. Caveat before anyone
gets excited: q_a = d_a chi carries derivatives, so chi propagates and the preferred-frame
question re-enters through that door.

NOTE ON MY OWN PROCESS: my first draft of the theorem claimed anisotropic degenerate carriers
are always ill-posed. The machine check REFUTED it and forced the structural/configurational
split above. The refuted draft is recorded here rather than quietly replaced.

#### STAGE 2B AMENDMENT 1 (same session, after the parallel arm reported)

**Correction to my own row (a) above.** My first pass examined only the SCALAR sector and
concluded "no bare-G rescaling anywhere". That is incomplete. The unit-timelike aether is
aligned and static in the Newtonian limit, so `g^{00}A_0^2 = -1` forces `A_0 = 1 + Phi`, hence
`F_{z0} = -Phi'` and `F^2 = -2 Phi'^2`: the Maxwell term feeds directly into the Phi-Phi
quadratic form. Derived from scratch in `s2b_refute_2026.py` R2b (quadratic EH density for the
plane-symmetric metric reduces to `-4 Phi' Psi' + 2 Psi'^2`; adding `gamma F^2` gives
`Phi' = Sigma/(8(1+gamma))`, calibrated so gamma = 0 returns pure GR):

* **G_N/G_bare = 4/3** for the deepest class (K4 coefficient gamma = -1/4, i.e. c_14 = 1/2),
  agreeing with the standard Einstein-aether `G_N = G/(1 - c14/2)` and with the parallel arm's
  exact static solve. Three independent routes, same number.
* **Row (a) corrected: APPLIES in the vector sector, does not apply in the scalar sector.** It
  is a RENORMALISATION, not a repair -- absorbed into the measured G_N, G3 survives -- but
  stage-1's Gate-MOND scored mu against `g_N = Sigma/8`, the PURE-GR reference, so the
  background it used for these candidates was wrong. What is not absorbable is
  `G_cosmo/G_N = 1 - c14/2 = 3/4`, a separate testable (BBN) prediction.

**Status of the 59.** They were GATE-UNDECIDED as stage 1 left them. The 1PN computation I
recommended has since been done by the parallel stage-2A arm (`s2a_ppn_exact_2026.py`), which
reports alpha_1 = -2 and alpha_2 a POLE, with the mechanism being that F^2 is blind to the
longitudinal aether mode (c123 = 0), giving infinite strong coupling rather than a second-class
constraint. I did not recompute alpha_1/alpha_2 and do not report them as my result. What I can
say adversarially: their alpha_1 = -2 matches the khronometric extrapolation alpha_1 = -4 c_14
that I declined to quote on its own; their G_N = 4/3 G matches my independent R2b; and their
c_4 basis-truncation finding was reached independently here. The 59 are therefore DECIDED at
G4+G5 by that certificate, not by stage-1's proxy -- and stage-1's Gate-PPN kill rule remains
a non-theorem with an explicit counterexample.

**Two arms, same dichotomy, one difference worth recording.** Stage-2A's S6 says G4 fails in
BOTH branches, including the degenerate one. My T4 says the degenerate Palatini branch has
alpha_1 = alpha_2 = 0 EXACTLY. These agree: 2A's branch (b) assumes the G2-forcing disformal
MATTER coupling is present, and with it the undetermined transverse components over-determine
matter (my E4). Without that coupling the carrier is invisible, G4 passes vacuously, and G2
fails instead. Either way there is no viable corner -- but the failure is well-posedness in one
case and zero stress in the other, and the distinction matters for what to try next.

---

## STAGE 5 (SYNTHESIS): the 1PN preferred-frame verdict, 2026-08-29

Full result: **`CANDIDATE_1PN_VERDICT.md`**. Script: `synth_1pn_independent_checks_2026.py`
(+ `.out`, 26/26), written from scratch, importing nothing from `compiler.py`, `mc_*.py`,
`routeA_*`, `ppn_khronon_routeB_*` or `adv_refute_*`.

**VERDICT: KILL -- but NOT by the preferred-frame bounds.**

`alpha_1 = alpha_2 = 0` EXACTLY at the candidate's locus. Route A, Route B and the refuter
all agree, all pass their own GR validation, all anchor to published khronometric PPN. So the
gate is not violated. It is a **VACUOUS pass**: the same solve returns `a_mu == 0` on-shell,
`G_eff/G = 1`, and no MOND force. `bet = lam = 0` is `c_123 = 0` <=> the `lambda_Horava -> 1`
strong-coupling point; the alphas are DISCONTINUOUS there (limit `-4 alp` and `oo`, value `0`).

The candidate dies instead on three PROVEN results, none of them a bound comparison:
K1 the literal spec is not MOND (`mu_eff in [1/2,3/2]`, never 0); K2 the carrier is a pure
redefinition `F(A) -> F(A) - f^2 A^2/(3M)`, so (H4) is never violated; K3 GR-with-no-MOND is an
EXACT branch for every source.

**CRUX ANSWERED:** neither option as posed. `f(chi) -> 0` is a red herring (carrier is `O(a^4)`,
two PN orders below). The lapse-tied MOND sector DOES generate `alpha_1 = -8(1-mu(y))` on its
own -- but only OFF the locus; AT the locus even that is empty because MOND is gone.

**GAP FOUND AND CLOSED in STAGE 4's section C.** The spec says `Q_ij` is "spatially-TRANSVERSE-
traceless (`Q^i_i = 0`)" -- two different constraints, and the refuter varied traceless-only
components. For the traceless-only reading C1 is confirmed exactly (my B3). For the strictly
TT reading it FAILS: eliminating a TT `Q` returns `A_ij (P^TT A)^ij`, verified NOT proportional
to `A^2` and carrying explicit angular dependence on the wavevector, i.e. NONLOCAL (my C3/C4).
Not a rescue: it is an (H1) nonlocality escape (same verdict as `M = -D^2`), it makes `Q`
non-algebraic so the DOF count must be redone, and it changes nothing about K1 and K3.

**CORROBORATION.** Stage 2B's degenerate Palatini branch independently exhibits the SAME
signature -- `alpha_1 = alpha_2 = 0` exactly with a timelike boost-breaking VEV, labelled a
vacuous pass because `mu == 1`. Two structurally unrelated branches producing "zeros because
the theory is secretly GR" is strong evidence the zeros here are degeneracy, not symmetry.

**OPEN DOORS (none closed).** `lambda_K != 1` (healthy khronon, keeps MOND, passes both alphas)
-- `c_T`, BBN, cosmology, stability, DOF all UNTESTED. Dirac count is 3 DOF not 2 and JUMPS
between vacuum and every excited state. And the `alpha_2` bound assignment is UNRESOLVED:
standard PPN assumes CONSTANT alphas, but `alp_kh` depends on position through `y` -- at the
Sun's field `alpha_2 ~ 1.7e-13` (passes hugely), at Neptune's `y` the framework kernel gives
`~7.1e-6` (would EXCEED the 4e-7 bound by ~18x). Flagged, not hidden.

**PROCESS NOTE.** My first Section D reconstructed Foster-Jacobson from recall; it was WRONG
and its checks failed. Rewritten to check only pole structure and the discontinuity of the
in-script formulas. The failure is recorded rather than quietly repaired.
