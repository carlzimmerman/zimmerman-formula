# Lane K -- the a0^2-linear-in-a-density family (Newtonian-normalised AQUAL offset), c = G = 1 in the algebra

## Bottom line
- Reproduced lane G's relocation independently and made it exact: with L = -(a0^2/8piG)F(y) - rho phi and F -> y at large y, the vacuum offset is
  **G rho/a0^2 = c/(8 pi), c = int_0^inf (1-mu) dy = <x^2>_mu (the SECOND MOMENT of the transition, x = g/a0)**. The puzzle needs c = 32 pi = 100.5
  (footing a0 = cH_L/Z) or c = 69 (SPARC-fitted a0): c_req = 3 Omega_L (c H0/a0)^2, no G, no pi.
- **c depends on the far tail of mu, weighted by x dx, and nothing in the data reaches it.** c is finite iff the tail exponent p > 2 (simple: linear divergence, standard: log,
  Milgrom-1999 vacuum-temperature form: linear, the record's own N = 2 OR-channel shape: log). SPARC covers x <= 62 (12 points above 30); Solar System x >= 5.7e5; nothing between.
  Replacing the RAR tail beyond 10-30 a0 by a power law that makes c = 100.5, 68.5 or infinity moves no SPARC prediction by more than 1.2e-3 dex (rms by 8e-7 dex).
  So the offset reading is a constraint on an unmeasured tail (c >= 1/3 for any mu' <= 1; no upper bound), **not a prediction that data can confirm or kill**.
- One conditional, discriminating by-product: in the record's own OR family (mu = 1-(1+g/s)^-N, a0 = s/N) the reading is (N-1)(N-2) = 1/(4 pi), N* = 2.0741, kappa* = 0.4821 -- **not 1/2**
  (N = 2 has c = infinity). The offset reading also forces **flat a0(z)** (w_off = -1 + (2/3) dln a0/dln(1+z)); a0 ~ H(z) with offset = dark energy is Einstein-de Sitter (0.39 mag at z = 0.5).
- No potential-term principle fixes W_v = 4 (extremum/BPS/Z2 are blind to the additive constant; SUSY vacua have V <= 0; Coleman-Weinberg carries hbar and fixes a mass, 11.2 meV).
- **Verdict: SHARP NO-GO for fixing the coefficient inside the offset family (the coefficient moves into an untested tail exponent); one narrow conditional DISCRIMINATING statement (kappa* = 0.482 in the OR family; flat a0(z)). Nothing derived. kappa = 1/2 stays FITTED.**

## What is a prediction and what is an input
INPUTS (assumptions of the reading, not results): (I1) the vacuum energy is the constant of the a0-sector Lagrangian, rho_L = a0^2 F(0)/(8 pi G); (I2) F is normalised so the Newtonian
regime carries no vacuum energy, F(y)-y -> 0 (the physical content is the DIFFERENCE rho(g=0)-rho(g->inf) = K c, K = a0^2/8piG; the reading sets rho(g->inf) = 0); (I3) mu's whole shape.
DERIVED (scripts): F(0) = c = int(1-mu)dy given I2 (k01 A); positive sign automatic for mu < 1; the relation G rho_L/a0^2 = c/(8 pi) given I1; every number below.
NOT A PREDICTION: c = 32 pi. The reading gives a *relation among three measured things* (rho_L, a0, the shape functional c[mu]); the tail is unmeasured, so it fixes c, it is not fixed by anything.

## Task 1 -- the relocation, independently reproduced and made precise (`k01_offset_relocation.py`, 38/38)
- Euler-Lagrange by sympy: div(F'(y) grad phi) = 4 pi G rho, mu = F' (A1; wrong prefactor rejected A2); F -> F + C is invisible to the field equation (A4), so the offset exists only through
  the normalisation I2; the constant piece L = -rho_off gives T_00 = +rho_off, T_ii = -rho_off from the metric variation of sqrt(-g)L (A6).
- **Identity (B):** c = int(1-mu)d(x^2) = int x^2 dmu, because mu is a CDF on x >= 0. **Bound (C):** if mu' <= mu'(0) = 1 (concave mu suffices), c >= 1/3 (bathtub; 20000 random monotone densities, sharp
  transition attains 1/3; CONTROL: allowing mu' > 1 gives c = 0.017). No upper bound: c(n) ~ 1/(n-2).
- **Finiteness (D):** c < infinity <=> int^inf x(1-mu)dx < infinity; for 1-mu ~ A x^-p finite iff p > 2. Verified: simple 2X - 2 ln(1+X) (linear); standard asinh X + X^2 - X sqrt(1+X^2) ~ ln 2X - 1/2 (log);
  Milgrom-1999 T-excess mu = (sqrt(1+4x^2)-1)/(2x), 1-mu ~ 1/(2x) (linear); p = 1.5 grows as X^(1/2).
- **Values (E)** (two integrations each; agree with lane G to all printed digits):

| mu | c | G rho/a0^2 = c/8pi | note |
|---|---|---|---|
| sharp min(x,1) | 1/3 | 0.013 | the minimum |
| Milgrom mu_n, n = 3, 4, 6, 10 | 1, 0.599, 0.431, 0.366 | 0.040 ... 0.015 | closed form below, n > 2 only |
| exponential 1-e^-x | 2 | 0.080 | |
| record OR N = 3, 5 (mu = 1-(1+x/N)^-N) | 9, 4.17 | 0.36, 0.17 | c(N) = 2N^2/((N-1)(N-2)), N > 2 |
| RAR-nu (McGaugh; proper AQUAL inverse) | 25.976 | 1.034 | 3.87x short of 32 pi |
| literal mu = 1-e^-sqrt(x) at g_obs | 24 | 0.95 | WRONG deep-MOND limit (mu ~ sqrt x); not a MOND mu, tail only |
| simple, standard, Milgrom-1999 T-excess, record OR **N = 2** | infinity | -- | p = 1, 2, 1, 2 |
| record OR, literal compact p = min(g/s,1) | 2N^2/((N+1)(N+2)) < 2 | -- | no solution for any N (F7) |

  Milgrom mu_n: **c(n) = -(2/n) Gamma(3/n) Gamma(-2/n)/Gamma(1/n)** for n > 2 (Mellin/Beta; checked at n = 2.05...10 by log-variable quadrature); c ~ 1/(n-2) as n -> 2+.
- **What c = c_req needs (F):** Milgrom n* = 2.0099 (32 pi) / 2.0144 (69.3); stretched exponential exp(-x^s) s* = 0.4085 / 0.4281 (lane G's 0.4085 reproduced); record OR N* = 2.080 / 2.116.
  Marginal or divergent families would need a cutoff X_c (units of a0) at which the partial c reaches 32 pi: simple 54.3, record N = 2 1.56e6, standard 3.8e43 -- bookkeeping, no scale identified.
  The requirement itself is footing-dependent: c_req = 100.53 (a0 = cH_L/Z; exactly 3Z^2), 69.27 (a0 = 1.1279e-10), 61.2 (a0 = 1.2e-10); with each family's own fitted a0 it ranges 29-72 (k02 B).
- **The record's own shape (F6, conditional).** mu = 1-(1-p)^N, p = y/(1+y), y = g/s (unit response per channel): slope N so a0 = s/N; the reading G rho = c a0^2/(8pi) with s^2 = G rho gives
  c(N) = 8 pi N^2, i.e. (N-1)(N-2) = 1/(4 pi), N* = (3+sqrt(1+1/pi))/2 = 2.0741, kappa* = 0.4821, G rho/a0^2 = 4.30. N = 2 (kappa = 1/2) is the MARGINAL member with c = infinity. So *if* the OR shape and the
  offset reading are both true, kappa = 1/2 is NOT what results (a0 = 9.03e-11 on the rho_L footing vs the framework's 9.36e-11: 3.6% apart, far below present a0 systematics). Coincidence disclosure: kappa* is 0.05% from Verlinde's
  sqrt(2 pi/27); different chains, I attribute no meaning to it (F8 guards against reading one).
- Where c accumulates (G): RAR-nu: 4% from x < 3, 25% from x < 10, 66% from x < 30, 97% from x < 100. A near-marginal tail (n = 2.01, c = 99.5): only 7% from x < 1e3, 13% from x < 1e6.
- State dependence (G3): the offset left at field g is eps(g) = K int_{g^2/a0^2}^inf (1-mu); for RAR-nu eps/eps(0) = 0.98 at a0, 0.88 at 3 a0, 0.58 at 10 a0, 0.19 at 30 a0. Inside bound systems the "vacuum energy"
  is reduced; the reading needs the cosmic vacuum at g << a0 (large-scale g ~ 2e-3 a0 at 10 Mpc, k04 E: consistent).

## Task 2 -- which part of mu, and what data constrain (`k02_data_and_the_tail.py`, 21/21; SPARC rotation curves, 155 curves / 2786 points, Upsilon_d 0.5, Upsilon_b 0.7)
Controls: nu_RAR scatter reproduces the committed 0.1453 / 0.1421 dex (A2); a permuted pairing is rejected (0.735 dex, A3).
- **Dependence:** c weights the tail by 2x dx; the transition region x ~ 1 contributes O(1) (0.3-few). For c ~ 100 the weight must sit at x >~ 10-100 (RAR-nu) or beyond 1e6 (near-marginal power tails).
- **Coverage:** SPARC g_obs/a0 reaches 62 (79 points above 10, 12 above 30); clusters x ~ 0.07 (baryons at 500 kpc); Milky Way at the Sun 1.9; Saturn 5.7e5, Earth 5e7 (Cassini class; I opened only the abstract of 1510.01369, no tail bound extracted).
- **Family fits (B, a0 free; then a0 + a global M/L scale free)**, rms in dex: RAR-nu 0.14212 / 0.14153; simple 0.14212 / 0.14200; record OR N = 2 0.14296 / 0.14157 (N = 2.074 0.14303 / 0.14156); exponential 0.14596 / 0.14216;
  standard 0.14776 / 0.14319; mu_n n = 3 0.15193 / 0.14514; n = 6 0.15608 / 0.14767; T-excess 0.14389 / 0.14244. Paired galaxy bootstrap (C, fixed M/L, 3000 draws) vs RAR-nu:
  standard +0.0056 [0.0013, 0.0094], n = 3 +0.0098 [0.0039, 0.0150], exponential +0.0038 [0.0002, 0.0070], record OR N = 2 +0.0008 [-0.0004, 0.0020], simple 0.0000. Shallow transitions fit best (their c is infinite or 26),
  sharp finite-c transitions worst. **Data-allowed c is not ordered by fit: [~2, infinity) for the shapes tried** (lower edge from the exponential once M/L floats; I did not scan every shape).
- **Tail graft (D, core result).** Keep the best-fit RAR-nu for x <= X_J (10, 20, 30 a0) and continue with A x^-p (continuous, monotone). p = 2.10 / 2.16 (X_J = 10) hits c = 100.53 / 68.53; p = 2 is c = infinity.
  Max change of any SPARC prediction 1.2e-3 dex; rms change <= 8e-7 dex; a 2% shift of a0 moves the rms by 3.6e-5 (control D6). 1-mu at Saturn is <= 1.4e-11; 11-31% of the grafted c sits above Saturn's acceleration.
  Hence no SPARC, cluster (x < 1) or Solar-System (x >= 5.7e5) statistic measures c; the Solar-System class cannot cap it from above.
- **What the data DO force (F):** Markov, c >= X^2 (1-mu(X)) = 4.9 at X = 15 for the best-fit RAR-nu shape; nothing more.
- **The prediction inside Milgrom's mu_n (E):** self-consistent n* = 2.028 (c(n*) = 35 = c_req at its own fitted a0 1.6e-10); at fixed M/L the shallower n = 1.5 (c = infinity) fits better by 0.0033 dex, with a global M/L scale floated
  the preference is 0.0017 dex. Compatible, not confirmed.

## Task 3 -- potential-energy term W(phi) (`k03_potential_principles.py`, 18/18): list of where a principle would act; none derived
W_v = G rho/a0^2 is dimensionless with no hbar and no c (A). Normalisation-independent form: **c = F(0)/F'(inf)** is invariant under F -> lambda F; F(0) alone is not (the 8 pi lives in the F normalisation).
Parameter-free, data-shaped members with finite c span 0.33-26; 32 pi = 100.5 lies >= 3.9x above the largest, so an "O(1)" reading predicts W_v in 0.013-1.03, not 4 (B). The record's F0 = 4 (lane E) and c = 100.5 are the same number in two normalisations.

| candidate principle | what it gives | status |
|---|---|---|
| extremum / Z2 minimum / Bogomolny kink | fixes shape, masses, tension; blind to the additive constant (C1, C2, sympy) | no value |
| symmetric point of a double well V(0) = lambda v^4/4; sine-Gordon 2 m^2 f^2 | product of free couplings (C3, C4) | free |
| Hamilton-Jacobi V = 3W^2 - 2W'^2 (real superpotential, verified: Friedmann, Raychaudhuri, KG) | dS points W' = 0 with V_* = 3 W_*^2 = 3H_*^2; W_* free (D1, D2) | tautology, no a0 |
| SUSY / BPS in N=1 sugra | V_* = -3 e^K |W|^2 <= 0 at DW = 0: Minkowski or AdS, never rho_L > 0 (D3, textbook algebra) | excluded for dS |
| Coleman-Weinberg one loop | W = G m^4 c^5/(64 pi^2 hbar^3 a0^2); W = 4 needs m c^2 = 11.2 meV = (64 pi^2)^(1/4) rho_L^(1/4) (E) | fixes a mass, not a number |
| generic completion (a0 and V0 independent parameters) | W_v = G V0 w_v/a0^2, free (F1) | free |
| single-length (Milgrom) completion | W_v = F(0) exactly; the value is decided by the SHAPE of F = c[mu] (F2) | back to Task 1: needs c = 32 pi |
| the "4" as the trace of delta^mu_mu, Einstein-Hilbert 8 pi x 4 pi | not tested here (lane F handles d-dependence; numerology risk) | none |

Pointer, outside my lane: a pure-tension wall has proper acceleration 2 pi G sigma (BRIEF addendum), so the puzzle can be written rho_L = 16 pi^2 G sigma^2; that route (membrane, free e/sigma) is not touched here.

## Task 4 -- testable consequences (`k04_evolution_and_footings.py`, 13/13)
- **Flat a0(z) is forced, and it is an equation-of-state probe.** If the offset is a separately conserved component with rho_off ~ a0^2 and a time-independent mu: **w_off = -1 + (2/3) dln a0/dln(1+z)** (A1, sympy).
  q = 0 gives w = -1; a0 ~ (1+z)^(3/2) gives w = 0. A 10% measurement of a0(2.5)/a0(0) bounds |w_off + 1| < 0.051 (30%: 0.14). The record's high-redshift status (campaign_fresh_gravity/STANDING_2026-09-29.md section 4: KURVS, MUSE-DARK,
  gas/pressure-dependent leans) is non-diagnostic; I did not re-verify it.
- **a0 ~ H(z) is incompatible with offset = dark energy.** rho_off ~ a0^2 ~ H^2 makes Omega_off constant and the expansion exactly H^2 = H0^2 (1+z)^3, q = +1/2: distance moduli differ from LCDM by 0.10 / 0.39 / 0.58 / 0.75 mag
  at z = 0.1 / 0.5 / 1 / 2 (B; control: the same integrator returns 0 for Omega_m = 1). (The rival is a different world, not this reading.)
- **The two footings.** rho_total footing: a0 = (1/2) c sqrt(G rho_crit0) = 1.1312e-10 (0.3% from the SPARC-fitted 1.1279e-10); rho_Lambda footing: 9.362e-11 (17% low). The offset reading lives on the rho_Lambda footing:
  there a0 = kappa c sqrt(G rho_L) is constant. On the rho_total footing it would force rho_off/rho_tot = c/(32 pi) = constant, contradicting LCDM's Omega_L(z) (0.685, 0.214 at z = 1, 0.075 at z = 2), and would need c = 68.9 (= c_req at the SPARC a0).
- **Testing through mu itself is hopeless with current or foreseeable data:** distinguishing c = 26 from c = 100 or infinity is a difference of <= 3e-3 in 1-mu (<= 1.2e-3 dex in g_obs) at x = 10-60 (D table), far below the 0.14 dex scatter.
- **Kill conditions.** (i) A robust rise or fall of a0(z) with a fixed-mu offset reading (w_off != -1 at the measured precision): the reading fails as "offset = dark energy" (not the framework's a0 law). (ii) a direct measurement of mu at x = 60-1e4 to ~1e-3 could test only FAST tails; a near-marginal tail (n ~ 2.01) puts >85% of c beyond x = 1e6, so c = 100 is then untestable in principle; (iii) the OR-family statement (kappa* = 0.482) is decided only by an a0 known to better than 3% on the rho_L footing (present M/L/distance systematics are larger).

## Own errors fixed (kept visible)
(i) first B1 failed: naive 1-mu_n cancels catastrophically at large x (1e27); replaced by the stable 1-x(1+x^n)^(-1/n) = -expm1(-log1p(x^-n)/n) and by the closed derivative (1+x^n)^(-1/n-1). (ii) first D4 (n = 2.05) failed because linear-x quadrature cannot
resolve a tail decaying like x^-0.05; switched to log-variable quadrature to x = e^6000. (iii) findroot at the n = 2 and N = 2 poles diverged; bracketed. (iv) my first graft check ("never below the baseline") was WRONG: at X_J = 10 the power law is locally steeper than the exponential and dips
below it by <= 1e-3; the property I need is continuity + monotonicity, which is what D4 checks. (v) thresholds I guessed for G1/G3/F5/F6/E2 were wrong (97% not 99% of c below x = 100; eps(10 a0) = 0.58 not < 0.2; n = 1.5 beats n* by 0.0033 not 0.005) and were replaced by the computed values.
(vi) pre-run expectation: I expected the record's N = 2 shape to give a finite c; it is exactly marginal (c = infinity), which turned the check into F6. (vii) k04's hard-coded "62.4 a0" is the k02 coverage maximum.

## Not established
- That the offset identification (I1, I2) is a real feature of any relativistic completion: the AQUAL Lagrangian is nonrelativistic; the state-dependent eps(g) shows the identification is not innocent. No relativistic action is exhibited here.
- F6 assumes the OR-channel shape, unit slope per channel and a tail exponent tied to the channel count; the shape itself is the record's unproven thermal route.
- The fit-quality comparisons are on one dataset with fixed (and one-parameter floated) M/L; the bootstrap respects within-curve correlation but not distance/inclination systematics. I did not scan all shapes, so "[~2, infinity)" is the range over the shapes tried.
- Xu's rho_DE = A0 a^2/G (arXiv 2203.05606) is used only as summarised by lane E (not re-opened); Milgrom's naturalness passage (2001.09729, sec. II.A: any constant in F "of order unity" gives Lambda ~ l^-2, no coefficient fixed) was read from the PDF text and is the same point as I1.
- Nothing here derives kappa = 1/2 or 32 pi; kappa = 1/2 stays FITTED.

## Files
k01_offset_relocation.py/.out (38/38), k02_data_and_the_tail.py/.out (21/21), k03_potential_principles.py/.out (18/18), k04_evolution_and_footings.py/.out (13/13); total 90/90. Run from this directory (k02 reads real_research/data/sparc_data).
