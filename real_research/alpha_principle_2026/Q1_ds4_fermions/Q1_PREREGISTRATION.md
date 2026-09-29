# Q1 -- the induced current of a charged Dirac fermion in dS_4: direct mode sum vs the published closed form, and what it says about alpha (pre-registration)

Written 2026-09-28 BEFORE any script in this directory was run.  The only work done before writing this file: reading the literature (below)
and deriving the structure by hand; no code of this lane has been executed.  Follows AH4 (scalar dS_4), N5 (fermion dS_2) and the audit P
(which lists "charged fermions in dS_4" as NOT TESTED).

## The question

AH4 computed the dS_4 induced current of a charged SCALAR.  The audit flagged fermions and vectors as untested.  This lane does the dS_4 Dirac
fermion, by the direct mode-sum method, with the same standard as AH4/N5:
(i)   does sigma/H = alpha x G_f(m/H), alpha = e^2/(4 pi), with G_f mass-dependent, so that no tie fixes alpha?
(ii)  is the coefficient of ln(m/H) the one-loop Dirac-fermion running of e (d(1/e^2)/d ln mu = -1/(6 pi^2), i.e. b = 4/3 per unit charge, four times the
      complex scalar's 1/3) times the divergence of the field tensor |nabla_nu F^{nu z}| = 2 E H?  (Which parts are a coefficient match, which an independent computation.)
(iii) how does G_f differ from the scalar G at large and small mass (power law? threshold?);
(iv)  is any special value of the coupling forced by the fermion case?

**Scope (binding on every statement below):** ONE Dirac fermion, minimal coupling, dS_4 planar patch, Bunch-Davies (in-)vacuum, constant-energy-density electric
field A_z = -(E/H)(a - 1) (i.e. F_{tau z} = E a^2), LINEAR/exact response in E as computed (no backreaction), one-loop adiabatic (order-2) subtraction.
Not tested: vectors, non-minimal coupling (irrelevant for spin 1/2), backreaction, other states, sums over the charged species, higher loops, other renormalization
conditions than the two published ones (minimal-order-2 adiabatic and Hayashinaka-Xue "maximal subtraction", the latter only quoted, not re-derived).

## Sources (read status stated honestly)

* Hayashinaka, Fujita, Yokoyama, arXiv:1603.04165 (JCAP 1607 (2016) 012): FULL TEXT read (pdftotext of the PDF, sections 1-5, appendix A, start of appendix B) and the
  equations of interest taken from the LaTeX SOURCE (the arXiv e-print), eq. (3.10)-(3.12) and (4.3)-(4.5).  Appendix B (adiabatic WKB details) and Appendix C
  (integration of the Whittaker function) read only in part / not checked.  The closed form (3.12) is a COMPARATOR to be validated by the direct sum, not assumed.
* Hayashinaka & Xue, arXiv:1802.03686 (PRD 97, 105010) "Physical renormalization condition for de Sitter QED": FULL TEXT read (PDF text layer; the two-column layout is garbled
  in places, the equations (11), (12), (14)-(16) are unambiguous).  They keep (3.12) as the "minimal subtraction" result and propose "maximal subtraction":
  J_max = J_min - (L/(3 pi^2)) [ln M - Re psi(iM)] (fermion, their (15)).  I do NOT re-derive the maximal subtraction; it is used only as a quoted scheme comparison.
* Kobayashi & Afshordi arXiv:1408.4141: the scalar comparator, exactly as used in AH4 (closed form (2.58) copied from AH4's script, already validated there to 2e-5).
* Stahl, Strobel, Xue arXiv:1507.01686 and lane N5 (dS_2 fermions): the Whittaker-mode method for Dirac fermions, as in N5 (not re-read here beyond N5's own record).
* Hayashinaka's PhD thesis (cited in 1802.03686) not read.  Other follow-ups on dS QED currents (e.g. later induced-EMT papers) NOT read.  Standard one-loop QED beta-function
  (d(1/e^2)/d ln mu = -(4/3) N_f/(4 pi^2)/... = -1/(6 pi^2) per Dirac fermion, -1/(24 pi^2) per complex scalar) is RECALLED textbook knowledge (also used in AH4), not derived here.

## Variables and conventions

hbar = c = H = 1, planar patch ds^2 = a^2(-dtau^2 + dx^2), a = -1/tau, evaluate at tau = -1 (a = 1).  L = eE/H^2, M = m/H (the same symbols as HFY), mu := M.
Rescaled spinor Xi = a^{3/2} psi obeys the flat Dirac equation with mass m a(tau) and vector potential; Hamiltonian
  h(tau) = alpha_z p(tau) + alpha_perp . k_perp + beta M a(tau),   p(tau) = k_z + L/tau   (kinetic momentum; the K&A/AH4 convention),  M a = -M/tau.
Current: J^z = e <psi^dagger alpha_z psi>, normal-ordered symmetrically (charge-conjugation symmetric), regularised by subtracting the adiabatic expansion of the SAME integrand
through order 2 (derivative counting: k, p, M a are order 0; d/dtau order 1), a spherical momentum cutoff being common to both terms (as in HFY (3.9)).
The dimensionless current is J_HFY := <J^3>_ren/(e a^3 H^3) with HFY's sign (positive = along the force on the charge at large L; the raw integral is -L Lambda^2/(3 pi^2) + ...).

Hand derivation (to be CHECKED by script 1, not assumed):
1. With k_perp along x, alpha_z, alpha_x, beta are three anticommuting matrices: the 4x4 problem splits into two 2x2 blocks h_pm = sigma_z p + sigma_x k_perp +- sigma_y M a; the blocks
   are related by k_perp -> -k_perp (conjugation by sigma_z), so J_HFY = +(1/(4 pi^2)) Int_0^inf k^2 dk Int_{-1}^{1} dr [ s_z(k_perp) + s_z(-k_perp) ]_reg, s_z = <sigma_z> of the
   positive-energy in-mode, r = cos(theta) = k_z/k.
2. Squaring: (i d_tau + h) solves the first-order system if Phi'' + (h^2 - i h') Phi = 0; h = sigma_z k_z + sigma_x k_perp + r_0 B/tau with B = (L sigma_z - M sigma_y)/r_0, r_0 = sqrt(L^2 + M^2),
   B^2 = 1; h^2 = k^2 + 2 L k_z/tau + r_0^2/tau^2, h' = -r_0 B/tau^2.  On B = s eigenvectors: phi'' + [k^2 + 2 L k_z/tau + (r_0^2 + i s r_0)/tau^2] phi = 0, solved by
   phi = W_{kappa, 1/2 - i s r_0}(2 i k tau), kappa = -i L r  (matches HFY (2.22) and K&A).  Positive-frequency in-mode: Xi = (i d_tau + h)(phi w_s) (Whittaker W, |z| -> infinity asymptotics).
3. Bloch-vector adiabatic expansion of s = <sigma>: ds/dtau = 2 n x s, n = (k_perp, M a, p): s_0 = n_hat, s_1 = -(n_hat x n_hat')/(2 omega),
   s_2 = -|s_1|^2 n_hat/2 - (n_hat x s_1')/(2 omega), omega = |n|.  The k_perp-odd first order term cancels in the block sum.
4. Small-L expectation from HFY (4.3): J_HFY = (L/(3 pi^2)) [ ln M - Re psi(iM) - pi M (4 M^2 + 1)/(3 sinh(2 pi M)) ], so that
   G_f(M) := 4 pi sigma_HFY(M) = (4/(3 pi)) [ ... ]  (sigma_HFY := J_HFY/L at L -> 0; sigma_c/H = e^2 sigma_HFY = alpha G_f with G_f = 4 pi sigma_HFY, exactly AH4's G = f_1/pi).
   Large M: sigma_HFY -> -1/(36 pi^2 M^2) (power law, NEGATIVE), G_f -> -1/(9 pi M^2); the scalar has G_s -> +7/(18 pi M^2) = 0.1238/M^2 (AH4).  Small M: sigma_HFY ~ (1/(3 pi^2))(ln M + gamma_E - 1/6),
   a logarithm (no power-law hyperconductivity), vs the scalar ~ 1/M^2.
5. ln M coefficient: (e H^3/(4 pi^2)) L (4/3) ln M = e^2 E H ln M/(3 pi^2), which is 4 x the scalar's e^2 E H/(12 pi^2), and equals (1/(6 pi^2)) x 2 E H x e^2 (Dirac running x |nabla F|).

## Scripts and what each must establish (order fixed; nothing added later without a visible amendment)

Mutation invocation for ALL three scripts: **`--mutate`** (not positional).  Each real run exits 0 iff all its checks pass.  Each control run exits 1 if the targeted check FAILS as required
(the control "works"), and exits 3 if the targeted check does NOT fail (the control has no power).  The docstring of each script states this.

### Script 1 `q1_1_dirac_modes_ds4.py` (structure and mode validation)
* D1 (sympy/explicit matrices) with the tetrad e^a_mu = a delta^a_mu and the spin connection computed from it, the curved-space Dirac equation for psi = a^{-3/2} Xi reduces to the flat
  system i Xi' = h Xi (residual identically 0); the 2D block decomposition holds (an explicit unitary maps h_4x4 to diag(h_+, h_-), error <= 1e-13 at random points).
* D2 h^2 - i h' = [k^2 + 2 L k_z/tau + r_0^2/tau^2] 1 + i r_0 B/tau^2 (sympy, identically); the scalar reduction phi'' + [...] phi = 0 with the stated index; e and E enter h only through
  (L, M) and k/H (sympy substitution check: h(e, E, m, H; k) with L = eE/H^2, M = m/H gives H x h(L, M; k/H)).
* M1 Whittaker modes: the first-order system is satisfied by Xi = (i d_tau + h)(W w_s) with residual <= 1e-10 (relative) at eight (k, r, L, M, tau) points, both s = +-1;  Xi_{s=+} and
  Xi_{s=-} are proportional (|cross-product| <= 1e-10) (uniqueness of the positive-frequency solution).
* M2 Bunch-Davies / normalisation / k_perp sign: independent ODE integration of i Xi' = h Xi from tau_0 = -T/k (T = 4000, first-order adiabatic eigenvector initial condition) reproduces
  s_z at tau = -1 of the Whittaker construction to <= 1e-4 (absolute) at eight (k, r, L, M) points including negative r and both k_perp signs.
* M3 full 4x4 check: integrating the four-component Dirac system (explicit chiral gamma matrices, in-vacuum = the two negative-energy in-modes; the sea) at three (k, r, L, M) points,
  the trace  -Tr[alpha_z P_+]  equals  -(s_z(k_perp) + s_z(-k_perp))  (2x2 blocks) to <= 1e-6.
* A1 adiabatic series: with s_0 + s_1 + s_2 built symbolically, the residual of ds/dtau - 2 n x s is O(3) (checked by scaling the derivative-counting parameter: residual/eps^3 bounded, and
  the eps^1, eps^2 residuals identically 0); |s_0+s_1+s_2| = 1 + O(eps^3); and against the exact ODE at large k the error of s_z after order 2 falls as k^-3 (log-log slope in [-3.4, -2.6] between k = 40 and 160), while after order 0 it falls as k^-1.
* MUTATE (`--mutate`): the Whittaker index is changed to the scalar-type index (1/2 - i s r_0 -> - i s r_0, dropping the spin-1/2 shift); M1 must FAIL.

### Script 2 `q1_2_induced_current_ds4.py` (the decisive direct sum)
* V0 the published closed form (3.12), transcribed from the LaTeX source, is finite and linear as L -> 0 (|J/L(1e-4) - J/L(1e-3)|/|.| < 1e-3 at two masses), odd in L, and its L -> 0 limit
  equals the weak-field formula (4.3) (rel diff < 1e-4 at M = 0.5, 1, 2).
* V1 DIRECT mode sum (Whittaker modes validated in script 1, order-2 adiabatic subtraction inside the integrand, log-spaced Gauss-Legendre in k on (1e-40, K], Gauss-Legendre in r, fitted large-k tail
  c2/k^2 + c3/k^3 + c4/k^4 as AH4) = closed form (3.12): worst relative difference <= 2e-3 with one consistent sign (expected ratio +1 in HFY's sign convention), on the declared grid
  (L, M) = (0.5,2.0) (1.0,1.5) (0.3,1.0) (0.5,0.6) (1.5,0.8) (0.4,1.4) (0.3,3.0) (2.0,1.0) (0.2,0.4) (0.05,1.0) (0.05,3.0) (0.3,0.15): twelve points.
  If V1 fails the run is reported as UNRESOLVED (transcription or direct sum wrong), never as a physics result; a failure at only the lightest points (M <= 0.15) would be reported as a
  limit of the adiabatic expansion, not silently dropped.
* V1s sign check independent of the comparator: at large L (L = 8, M = 1) the direct J_HFY is POSITIVE and its ratio to the Minkowski Schwinger asymptote of HFY (4.2), J ~ L^2 e^{-pi M^2/L}/(6 pi^3),
  lies in [0.6, 1.6] ((4.2) is an asymptotic form for L >> 1, M, so only the sign and the order of magnitude are tested).
* V1r raw-integral ln Lambda coefficient (EXACT modes only, no adiabatic terms): let G(k) = (k^2/(4 pi^2)) Int dr [s_z(k_perp) + s_z(-k_perp)] be the integrand of the raw (unsubtracted) J_HFY in dk.  The raw integral
  with a spherical cutoff is -L Lambda^2/(3 pi^2) + (L/(3 pi^2)) ln(2 Lambda) + const + ... (HFY (3.10) with the sign fixed by the large-Lambda estimate above), so G(k) = c1 k + c0 + c_{-1}/k + ... with
  c1 = -2L/(3 pi^2), c0 = 0, c_{-1} = +L/(3 pi^2).  Fit G(k) at k in {60, 90, 135, 200, 300, 450} to c1 k + c0 + c_{-1}/k + c_{-2}/k^2 + c_{-3}/k^3 at (L, M) = (0.3, 1.0): c1 and c_{-1} must agree with those values to 3% and
  |c0| <= 3e-3 |c1| x 1 (unit k).  This is an exact-mode, adiabatic-free check of the log-divergence coefficient 1/(3 pi^2) = 4/(12 pi^2).
* V2 order counting: dropping the order-2 term leaves a divergent (log) integral: the K-convergence of the subtracted integral at (0.3, 1.0), K = 100, 200, 400, agrees to 1e-4 relative for the real run; for the control (order 0 only) the value drifts by > 5% between K = 100 and 400 or disagrees with (3.12).
* MUTATE (`--mutate`): the order-2 term s_2 is dropped from the subtraction (order 0 only; s_1 cancels in the block sum); V1 must FAIL.

### Script 3 `q1_3_physics_answers.py` (uses only the closed form validated in script 2, and the AH4 scalar closed form)
* Q1 structure: (sympy) the induced current is e H^3 F(L, M): sigma_c/H = 4 pi alpha G_f(M)/(4 pi) with G_f(M) = 4 pi lim F/L; the coupling enters only through alpha = e^2/(4 pi) times G_f; no other e-dependence
  (from script 1 D2).  Ties sigma_c/H = c, c in {kappa, kappa/pi, 1/(2 pi), 1/pi, 1, 2 kappa} (kappa = 1/2 FITTED; the same six constants as AH4/N5), masses M in {0.5, 1, 2, 5}: alpha is DETERMINED by a tie only if
  (a) c/G_f(M) is positive and (b) its spread over the four masses is < 2 (declared).  Both the minimal scheme (3.12)/(4.3) and the Hayashinaka-Xue maximal scheme (quoted) are scored.  Expected: NOT determined in either.
  Electron-mass reading (an extrapolation): required alpha ~ c/|G_f| at M_e = m_e/H_0 = 3.55e38 using the large-M law; labelled extrapolation.
* Q2 ln(M) coefficient: (a) sympy: |nabla_nu F^{nu z}| = 2 E H (as AH4); (b) the coefficient of e^2 E H ln M in the current from (3.12) is 1/(3 pi^2); (c) one-loop Dirac running x 2 E H = 2/(6 pi^2) = 1/(3 pi^2): |ratio| = 1 to 1e-12;
  (d) ratio to the scalar coefficient (1/(12 pi^2), AH4) = 4 exactly.  This is a COEFFICIENT MATCH (the beta-function coefficient is recalled input, the ln M coefficient of (3.12) is read from the validated closed form);
  the INDEPENDENT computation is script 2's V1r (the ln Lambda coefficient of the exact mode sum).  Also: heavy-mass decoupling: the small-L closed form at M = 10, 20, 40 gives |sigma_HFY|
  falling as a power, slope of log|sigma| vs log M in [-2.3, -1.7] between M = 10 and 40, and |sigma_HFY|(40) < (1/3)(1/(3 pi^2)) ln 40 (the ln is cancelled by -Re psi(iM)).
* Q3 G_f vs G_s: tabulate G_f(M) and G_s(M) (scalar, AH4 closed form at small L) at M in {0.1, 0.3, 1, 2, 5, 10, 20, 40}.  Tests: (a) sigma_HFY(M) < 0 at every tabulated M (HFY claim "negative for all M"; NOT assumed); (b) |G_f| M^2 -> 1/(9 pi)
  (= 0.03537) within 2% at M = 40 and G_s M^2 -> 7/(18 pi) (= 0.1238) within 2% at M = 40; (c) at small M the fermion grows only logarithmically: (G_f(0.01) - G_f(0.1))/(4/(3 pi) ln 0.1) within 5% of 1 and |G_s(0.1)| M^2 ~ O(1)
  (power law) -- the scalar being evaluated where its closed form is stable (declared; if the scalar closed form is not reliable below M = 0.1 that row is reported as not computed); (d) both are power laws at large M (no exponential
  threshold): slopes in [-2.3, -1.7]; (e) sign: G_f/G_s -> -2/7 at M = 40 within 3%.
* Q4 special value of the coupling: (a) zeros of sigma_HFY(M) in M in (0, 50): none expected (search on a 400-point log grid); (b) the current's own zero L*(M) (HFY's "stable point", the field value at which J_HFY(L, M) changes sign) at M in {0.5, 1, 2, 5}: found by bracketing on the closed form
  if it exists; it is a FIELD value eE/H^2, and for E free every e is compatible with it, so it selects no coupling (reported descriptively; existence not a pass criterion); (c) the massless conformal limit: G_f^max(0) = -2/(9 pi) and the minimal scheme's ln M divergence: with no mass there is no scale
  other than the renormalization scale mu, and ln(mu/H) is a free input.  No value of alpha is selected.  Candidate special values (the six ties above at masses {0.5, 1, 2, 5}, the M -> 0 limit of the maximal scheme, and L* at the four masses) are a closed list of 6x4x2 + 1 + 4.
* MUTATE (`--mutate`): the scalar ln M coefficient (1/(12 pi^2)) replaces 1/(3 pi^2) in the check that (3.12)'s ln coefficient equals the Dirac running; Q2(d) must FAIL.

## The bar

No numerical match to 1/137.036 is claimed or sought.  Any later attempt to identify a conductivity tie with alpha must clear lane D's bar (P < 1e-3 after look-elsewhere, miss <= 5e-10 or a stated predicted precision, zero fitted reals,
scale stated); the ties above are scored only for mass-independence, as in AH4.

## Reading rules

* The ln(m/H) term is the running of e from scale m to H; the renormalization condition that makes the published scheme physical (the flat-space vacuum polarisation vanishes for m >> H) is exactly "alpha is the measured low-energy value at scale m", so alpha enters as an INPUT; a finite counterterm c e^2 E H (a shift of 1/e^2) is the same freedom as in flat space.
  The Hayashinaka-Xue maximal subtraction shows that the M-dependence of the finite remainder (power law vs exponential at large M) is itself a renormalization-condition choice; this is reported, not resolved.
* A pass of V1 says the current is computed correctly (with the published subtraction) and says nothing in favour of any alpha.
* Failing to find a forcing tie is the expected outcome and is reported as such.
* kappa = 1/2 stays FITTED; the SM mass sector is walled; nothing from the do-not-cite list is cited.  No commit is made by this lane.

## Count of everything that will be run

3 scripts x (1 real run + 1 mutate run) = 6 runs, plus any re-runs after a disclosed amendment (each recorded below, FIRSTRUN outputs kept).  Numbers of trials: 12 grid points (V1) + 8 + 8 + 3 (script 1) + 6 fit nodes (V1r); ties 6 x 4 x 2 schemes; special-value list closed as above.

## Amendments

### Amendment 1 (written before any of the three scripts was run; disclosed development smoke test)

Before writing the scripts I ran a smoke test of the helper library `q1_lib.py` (two Whittaker-mode spinors against a far-past ODE at four (k, r, L, M, k_perp-sign) points: absolute differences 2e-8 to 4e-7 in s_z, so the mode construction works; and the transcribed closed form (3.12) at L = 1e-3, 1e-4).  Two things came out of it, neither used to tune anything:
(a) the transcribed (3.12) is NOT finite as L -> 0: J/L grows like 1/L^2 (e.g. about -4.4e5 at L = 1e-3, M = 0.5).  Script 2 will still run its V0 as registered (and is expected to FAIL V0 and V1 on the transcription as printed); its FIRSTRUN output will be kept.
    Diagnosis by hand, recorded here before the run: the Ei term of (3.12) has, at small L, the leading behaviour -6 M^2 cosh(2 pi r)/L^2 when its exponential prefactor is e^{+2 pi r s}, and the 1/L^2 cancels exactly if the prefactor is e^{-2 pi r s} (the same combination that appears in the psi integral).  The e^{+2 pi r s} version also grows like e^{4 pi r} at large mass, which contradicts the paper's own decoupling.  I will therefore ALSO run the variant with e^{-2 pi r s}; that is the only change considered, it is motivated by the registered finiteness criterion V0 and by decoupling, not by fitting to direct-sum numbers; V1 then decides whether the variant is right.  If V1 fails for the variant the comparator is reported as UNRESOLVED and the direct sum's own weak-field and large-mass behaviour are compared with (4.3)-(4.5) instead.
(b) a parity argument, noticed before any script ran: s_z^(j) has parity (-1)^j under k_perp -> -k_perp, so in the block SUM the odd orders cancel and the remainder after order 2 is order 4 (about k^-4), not order 3.  The registered A1 slope windows are amended accordingly: after order 2, single block (one k_perp sign) slope in [-3.4, -2.6] and PAIR SUM slope in [-4.6, -3.4]; after order 0, single block [-1.4, -0.6] and pair sum [-2.4, -1.6].  The k-integrand remainder after order 2 is then k^2 x k^-4 = k^-2 (which the registered tail fit c2/k^2 + c3/k^3 + c4/k^4 covers).
    Also: V2's "drift" criterion for the order-0-only control stays as registered (a c_{-1}/k integrand gives a logarithmic drift ln 4 x L/(3 pi^2) between K = 100 and 400).

### Amendment 2 (after the FIRST RUN of `q1_1_dirac_modes_ds4.py`; the first-run output is kept as `q1_1_dirac_modes_ds4_FIRSTRUN.out`)

First run: 11 of 12 checks PASS (D1a-d, D2a-c, M1, M2, M3, A1a); **A1b FAILED**.  The measured log-log error slopes (k = 40 -> 160) were: single block after order 0: -2.00 (registered window [-1.4, -0.6]); single block after order 2: -4.00 (registered [-3.4, -2.6]);
pair sum after order 0: -3.02 (registered [-2.4, -1.6]); pair sum after order 2: -5.02 (registered [-4.6, -3.4]).  Diagnosis: my Amendment-1(b) counting assumed the order-j term of s_z falls as k^-j.  It falls as k^-(j+1) for j >= 1, because the unit Bloch vector n_hat is O(1) and each
derivative n_hat' ~ n'/omega ~ 1/k, and the series then divides by another omega (s_1 = -n_hat x n_hat'/(2 omega) ~ k^-2, s_2 ~ k^-3, s_3 ~ k^-4).  The parity argument (odd orders cancel in the k_perp-summed pair) was right; the exponent bookkeeping was off by one.
This is NOT a physics failure (A1a, the exact residual identities, passes to 5e-16, and M1-M3 pass to 1e-8..1e-12).  The corrected windows are: single order 0 [-2.4, -1.6]; single order 2 [-4.4, -3.6]; pair order 0 [-3.4, -2.6]; pair order 2 [-5.4, -4.6].
**These windows were set after seeing the numbers (the exponents are the exact integers -2, -4, -3, -5) so A1b is a post-hoc-window check and is scored only as a consistency statement; nothing else depends on it.**  Consequences that matter and are recorded now, before script 2 runs:
the remainder after the order-2 subtraction of the k-integrand k^2 x (pair) is ~ k^-3 (faster than the k^-2 the fit form allows); after order 0 only, the pair error is ~ k^-3 so the integrand k^2 x k^-3 ~ 1/k, i.e. the order-0-only control diverges logarithmically (as V2 already assumes).

### Amendment 3 (after the FIRST RUN of `q1_2_induced_current_ds4.py --variant printed`; first-run output kept as `q1_2_induced_current_ds4_FIRSTRUN.out`)

First run, comparator = (3.12) exactly as printed: **V0 FAIL, V1 FAIL, V2 FAIL; V1s PASS, V1r PASS** (2 of 5).  Details.  (a) V0: the printed (3.12) is not finite as L -> 0 (J/L ~ -4.4e5 at L = 1e-3, M = 0.5, growing as 1/L^2); the amended variant (Amendment 1(a): Ei prefactor s e^{-2 pi r s}) is finite, odd and equals (4.3) to 6e-10 at M = 0.5, 1, 2.
(b) V1: with the printed form the comparator is astronomically off (ratios 0 to 0.18); the DIRECT sum values at the twelve grid points were printed in the same run.  Reading them against the amended variant AFTER the run (the amendment had been fixed beforehand by V0 and decoupling, not by these numbers) gives agreement at the 1e-5 level (worst 1.1e-5, at the two lightest-signal points (0.05, 3.0) and (0.3, 3.0), where |J| ~ 1e-5 and the double-precision cancellation in exact - adiabatic limits the direct sum); this is now the registered V1 comparator (default of the script).
    A remaining possibility that the amended form and the direct sum share a common error is excluded by V1s (sign, magnitude of the Schwinger limit), V1r (exact-mode ln Lambda coefficient c_{-1} = L/(3 pi^2) to 4e-6) and by the direct sum being built from independently validated modes (q1_1 M1-M3, ODE agreement 1e-8) -- but the closed form itself is not re-derived here.
    Physics consequence recorded: (3.12) as printed in the arXiv source contains a misprint (Ei prefactor sign); the published weak-field limit (4.3)-(4.5), used in all later numbers, is correct (it equals the direct sum's small-L behaviour at the two small-L grid points to 1e-5 and the amended (3.12) to 1e-9).
(c) V2 FAILED marginally in the first run: the order-2 truncated integral (no tail) drifted 1.25e-3 relative between K = 100 and 400 against the registered < 1e-3, because the k^-3 remainder (A1b: pair error ~ k^-5, so the k-integrand ~ 3/k^3) has a tail ~ 1.4e-6 at K = 100; with the fitted tail the values are -0.001137586, -0.001137589, -0.001137590 (K = 100, 200, 400; 3.5e-6 relative spread).  My registered threshold under-estimated the tail.  **Amended (post-hoc, after seeing the numbers) V2: the order-2 integral WITH its fitted tail drifts < 1e-4 between K = 100 and 400; order 0 only (truncated) drifts > 5% (it drifted by +1.2e3 %, a logarithmic divergence 0.0140 = L ln 4/(3 pi^2) = 0.01405 in the first run: +0.0390, +0.0461, +0.0531 for K = 100, 200, 400, steps 0.0070 = L ln 2/(3 pi^2)).**  This is a threshold change and is flagged as post-hoc; the substance (order 2 converges, order 0 diverges logarithmically with exactly the predicted coefficient) is unchanged.
(d) The pre-registered ln Lambda test V1r passed in the first run with c1 = -2L/(3 pi^2) to 5e-12 and c_{-1} = +L/(3 pi^2) to 4e-6.  One small clarification: the fitted c_{-2}, c_{-3} are not expected to vanish; only c1, c0, c_{-1} were registered.
The tail-fit constant c2 printed in the table (about 1e-6 to 5e-5) is double-precision roundoff of (exact - adiabatic) times k^4 (the true remainder is k^-3), not physics; its contribution to the integral is < 1e-9.

### Amendment 4 (after the first run of `q1_3_physics_answers.py`; first-run output kept as `q1_3_physics_answers_FIRSTRUN.out`)

First run of script 3: 9 of 10 checks PASS (Q2a, Q2b, Q2c, Q3a, Q3b, Q3d, Q3e, Q1a, Q4a); **Q3c FAILED**.  The failing sub-condition was my registered "|G_f(0.1)/G_f(0.3)| < 2" (it was 2.209); the other two sub-conditions passed
((G_f(0.01) - G_f(0.1))/((4/(3 pi)) ln 0.1) = 0.997, and the scalar ratio G_s(0.1)/G_s(0.3) = 9.84 > 5).  Diagnosis: the "< 2" threshold was an ill-chosen proxy for "logarithmic": a logarithm with the additive constant (gamma_E - 1/6) has ratio 2.2 between M = 0.1 and 0.3.
**Amended (post-hoc, after seeing the numbers):** replace the ratio bound by the exact small-M law implied by (4.4): G_f = (4/(3 pi))(ln M + gamma_E - 1/6) within 2% at M = 0.01 and 0.1 (the values are -1.7803 vs -1.7803 and -0.8063 vs -0.8030 in the first run, i.e. 0.0% and 0.4%).  This makes the check tighter about the log law and drops the ad hoc ratio; it is flagged as a post-hoc rewording.
Also added (descriptive, registered here before the re-run): a 41-point log scan of J(L, M) on L in (0.02, 40) counts the sign changes for the L*(M) search (the first run only bisected between the two ends, so uniqueness of the zero was not shown); Q4a now also requires exactly one sign change at each mass.

### Amendment 5 (run inventory and disclosures, written after all scripts had run)

* Runs: script 1: FIRSTRUN (11/12; A1b failed, Amendment 2), then real (12/12, exit 0) and `--mutate` (M1 fails as required, exit 1).  Script 2: FIRSTRUN with `--variant printed` (2/5), then real with the amended comparator (5/5, exit 0) and `--mutate` (V1 fails as required, worst ratio deviation 5.5e2, exit 1).
  Script 3: FIRSTRUN (9/10; Q3c failed, Amendment 4), then real (10/10, exit 0) and `--mutate` (Q2a and Q2b fail as required, exit 1).  Total: 3 first runs + 3 real + 3 controls = 9 runs (registered: 6 + disclosed re-runs).
* One tooling slip: my first `--mutate` run of script 1 crashed with a KeyError (the check dictionary was keyed by the full tag string); Python's exit code 1 for the uncaught exception would have looked like "control failed".  Fixed (keys are the first token of the tag) and the control re-run; the committed `.out` is from the fixed script.  No physics result changed.  The three `--mutate` outputs in this directory contain the explicit line "FAILED as required -- the control works".
* Disclosure about Amendment 1(a): after writing the amended variant into the library I evaluated it at L = 1e-3, 1e-4 (M = 0.5, 1, 2) during the development smoke test, BEFORE the first run of script 2; it reproduced the weak-field formula (4.3) to about 1e-8.  So the amended variant was chosen by the V0 pole cancellation and decoupling argument and had already been seen to pass V0 before script 2's first run; V1, the decisive test, was first seen in the first run (direct sum printed next to the printed form).
* The first-run outputs kept: `q1_1_dirac_modes_ds4_FIRSTRUN.out`, `q1_2_induced_current_ds4_FIRSTRUN.out`, `q1_3_physics_answers_FIRSTRUN.out`.
* Post-hoc items (all flagged above): the A1b windows (Amendment 2), the V2 threshold (Amendment 3c), the Q3c wording (Amendment 4).  Everything else is as registered.
* What was NOT tested here: see the Scope paragraph at the top; in addition the maximal-subtraction scheme is only quoted from Hayashinaka-Xue (their (16)), the closed form (3.12) itself is validated against a direct sum at twelve points, not re-derived, the scalar closed form beyond m/H = 3 is unvalidated by direct sums, and the Q2 "coefficient match" reads the ln M coefficient off the transcribed closed form (only V1r, the ln Lambda coefficient of the exact mode sum, is independent).
