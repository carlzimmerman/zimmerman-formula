# HZ1 RESULT: is there a UV completion of action (A)? Gate T3 of the TOE0 battery (2026-11-10)

**T3: FAIL. (i) FAIL, (ii) PASS, (iii) PASS.** The law's function J cannot be a term of any power-counting-renormalizable
UV action: it is non-analytic and non-polynomial in the acceleration. The one one-loop mechanism that reproduces its shape
(a boson-fermion pair on the 3-d leaves) needs a coupling 10^55.4 times the natural ceiling (canonical; alt 10^55.3).
The Lorentz-violation window for the Horava scale, M_* between 5.1e-3 eV and 1.75e6 GeV, is real, but nothing usable sits
inside it.

Criteria: `FROZEN_CRITERIA.md` (local c1bc0c0977, committed alone before any script); post hoc amendment
`AMENDMENT_A1.md` (local fb95bfc882, one stronger MUTATE twin; changes no graded line). Script `hz1.py`; output
`hz1.out` / `hz1.json`; twins `HZ1_MUTATE=1` -> `hz1_MUTATE.out` / `hz1_MUTATE.json`. Runtime 7 s, 0.12 GB.
TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled.
Origin ids are at the end.

## The deciding number

G3, the leaf boson-fermion pair, passes sign and shape: max |mu - x/(1+x)| = 0.026 and deep slope 0.964 against the law's
0.990. To make its bump equal to one, it needs nu g_B^3 = 4 pi B c/(K a0) = **5.6e89 eV**, where B is the bump height and
c the fitted crossover; canonical footing, alt 4.6e89 eV. The ceiling is N nu g^3 with N <= 1000 copies, nu <= M_Pl and
g <= 4 pi, which gives 2.4e34 eV. So **log10 R_c = 55.36 (canonical) / 55.28 (alt)**. Twin M3 shows the fail is
the hierarchy and nothing else: with a0 replaced by M_Pl the same test passes at log10 R_c = -6.4.

## (i) A UV action for (A): FAIL

**(A) written as a Horava theory** (unitary gauge tau = t, Q = 1/N, A_i = d_i ln N). Reading off the coefficients:
- lambda = 1: the FRW minisuperspace of R gives it exactly (KA2).
- beta = 0, so c_T = 1; xi = 1.
- The law's term is a khronometric alpha-term with a running coefficient, alpha(u) = 4 J(u)/u^2, where u = |A|/a0. Its
  fluctuation values are alpha_par = 2/(1+u)^2 and alpha_perp = 2/(1+u).
- **At A = 0 all three equal 2.** That is exactly Blas-Pujolas-Sibiryakov's G_N = G/(1 - alpha/2) -> infinity point,
  rederived here in sympy (KA2). The deep-MOND regime is khronometric gravity sitting at alpha = 2, where the lapse's
  quadratic gradient term 1 - alpha_par/2 vanishes, with the non-analytic cubic of J taking over. The khronometric
  scalar speed^2 is 0 there (lambda = 1).

Three other features of (A) matter for a UV completion:
- The clock term mu_K^2 (1/N - 1)^2/(2K) is a potential for the lapse. It breaks the time reparametrization of Horava's
  FDiff, so (A) sits outside the class in which renormalizability has been proven (projectable, FDiff). Its coupling has
  dimension 6 at z = 3, so it is relevant and harmless to power counting.
- Power counting (KA1): [1/kappa^2] = d - z, which is 0 at z = 3 and 2 at z = 1. Every coupling of the general z = 3
  potential, projectable and non-projectable, has dimension >= 0. The criteria file prints this formula as "z - d"; the
  values it names (0 and 2) are those of d - z, which is what was checked.
- **J1/J2 (computed, sympy).** J(u) = u - ln(1+u) has non-zero odd orders u^3, u^5, ..., so it contains odd powers of
  |A| = (A_i A^i)^(1/2). Those are not polynomials in A_i, so J is non-analytic at A = 0. It also has non-zero orders
  n >= 7, whose couplings have dimension 6 - n < 0 at z = 3, so J is non-renormalizable. Its series does not terminate.
  **J is not admissible as a UV term.** The Legendre form does not help: W(p) = -p - ln(1-p) has odd orders and radius 1
  (the flux cap). The stiffness F = max(Pi,0)^2/2 has a jump of 1 in F'' at Pi = 0, a third non-analytic piece. The
  detector is not trivially negative: twin M2, an even degree-6 polynomial, is accepted.

**Generation by the flow: five one-loop candidates.** Each one keeps the UV action local and polynomial in A_i (the fields'
masses depend on A_i polynomially). The induced Lagrangian is read from L = -V, never from V.

| candidate | sign of the |A|^3 term in L (law needs < 0) | best fit: max dmu / deep slope (law 0.990) | log10 R_c canon / alt | fails on |
|---|---|---|---|---|
| G1 leaf scalar, m^2 = g^2 A^2 (the lead's candidate) | **+ nu g^3/(12 pi): WRONG** | 0.92 / 0.00 (band alone 0.49) | 55.48 / 55.39 | sign, shape, coefficient |
| G2 leaf Cl(6) fermion, \|m\| = g\|A\| | - 8 nu g^3/(12 pi): right | 0.75 / 0.24 (mu = a + bx, no saturation) | 54.57 / 54.49 | shape, coefficient |
| **G3 leaf pair, g_B = 2 g_F, m0 != 0** | - nu g_B^3/(12 pi): right | **0.026 / 0.964: ok** | **55.36 / 55.28** | coefficient only |
| G4 thermal boson (J_B) / fermion (J_F) | + T g^3/(12 pi) / none: WRONG | 0.99 / 0.00 (mu decreasing; both statistics) | 28.26 / 28.22 (g 2.3e29 at T 1.7 meV) | sign, shape, coefficient |
| G5 4-d Coleman-Weinberg, boson / fermion | none (A^4 ln A) | boson 0.98 / 0.00; fermion 0.77 / 0.23 | 29.31 / 29.27 (g 2.6e30) | sign, shape, coefficient |

What carries this:
- **The lead's candidate has the wrong sign.** The 3-d determinant is V_3 = -|m|^3/(12 pi) per real boson (KA4a). It
  enters L as +nu |m|^3/(12 pi). J's cubic enters L as -(a0^2/K) u^3/3 (KA3 fixes the convention: GR + (a0^2/K) J gives
  mu = x/(1+x) exactly). So a leaf boson pushes the deep regime the repulsive way. "Same sign" compared V with L.
  A Grassmann field flips the sign (twin M1: the same G2 with boson statistics fails the sign test).
- **A single species cannot saturate.** Every determinant with m^2 linear in A^2 is concave (boson) or convex (fermion)
  in A^2 for all A. So mu is monotone the wrong way (G1, G4) or grows without bound (G2, G5). Only the pair G3, with its
  large-A cubic cancelled by g_B = 2 g_F (a supersymmetry-like tuning), gives
  mu(s) = 1 + s - sqrt(1 + s^2), with s = c x. This tracks x/(1+x) to 0.026 (fit alpha_t 0.060, B 0.970, c 0.796).
  Twin M4 (G3 without its boson) loses the shape (Q 7.5).
- **The coefficient is the hierarchy.**
  - The leaf routes need nu g^3 ~ M_Pl^2/a0: 55-58 orders above any natural ceiling, about the square of the record's
    30-order wall W3.
  - The 4-d routes (thermal, Coleman-Weinberg) need a dimensionless coupling g ~ sqrt(M_Pl/a0) ~ 1e29-1e30. The thermal
    route also lands at T = 1.7 meV, the dark-energy scale. That is W3 itself.
  - Even G3's right shape puts a0 into the UV action by hand, as the mass ratio m0/(c g_B), and needs two tunings
    (g_B = 2 g_F, and K nu g_B^2 m0 = 4 pi, i.e. alpha = 2 at A = 0 exactly).
  - The leaf density nu of a time-ultralocal field is a cutoff-defined parameter (a dimensionally regularized omega
    integral would give zero). The ceiling nu <= M_Pl is the frozen natural bound.
- Power counting: every added coupling has dimension >= 0 at z = 3 for all five candidates. The fail is not there.

**Scope of the FAIL.** It covers J as a UV term (shown for any polynomial action) and the five candidates stated. A
non-perturbative origin of J (a condensate, a strongly coupled sector) is not computed and is not excluded.

## (ii) Percolation into matter: PASS

The Pospelov-Shang scaling (arXiv:1010.5249, PROVISIONAL: the transfer of LV into the SM is "protected by the ratio
L_HL^2/M_P^2") is used as delta c_X = C alpha_LV (M_*/Mbar_P)^2/(16 pi^2), with C scanned over 1e-3 to 1e3. The graded
case uses alpha_LV = 2, (A)'s value at A = 0. Bounds are Kostelecky-Russell v19 (arXiv:0801.0287, Tables S2/S3, maximal
sensitivities, PROVISIONAL): photon kappa_tr 1e-20, electron c_TT 1e-21, proton c_TT 1e-22, and the neutron by the boost
route, c_Z 1e-29 over beta_CMB^2, i.e. 6.6e-24.

| C | window top M_hi (alpha 2, both footings) | binding |
|---|---|---|
| 1e-3 | 1.75e9 GeV | neutron (boost) |
| 1 | 5.5e7 GeV | neutron (boost) |
| 1e3 | 1.75e6 GeV | neutron (boost) |

M_lo = 5.1e-3 eV (short-range gravity), so the window is non-empty at every C on both footings: PASS. Reported variants:
- In the lab, (A)'s alpha is tiny: alpha_perp(Earth) = 1.9e-11 (canonical) / 2.3e-11 (alt), which moves the top to
  1.8e13 GeV at C = 1.
- At the Sun's Galactic orbit, alpha_perp = 0.61 / 0.69 (u = 2.29 / 1.90) and the enhanced alpha_perp/(2 - alpha_par) is
  0.34 / 0.39, which gives 1.0e8 to 1.4e8 GeV at C = 1.
- Matter keeps z = 1, so its one-loop dimension-6 LV sits near 4 pi Mbar_P/sqrt(C), 1e18 to 1e21 GeV, far above the GRB
  time-of-flight bound (about 1.3e11 GeV, PROVISIONAL).

## (iii) The window with gravity's own limits: PASS

At C = 1e3 and alpha 2, the caps on M_* are:

| limit | cap on M_* |
|---|---|
| c_T, GW170817 (arXiv:1710.05834): tree c_T = 1 from beta = 0, one-loop delta c_T from the same estimate | 2.2e10 GeV |
| one-loop PPN alpha_2 <= 1.6e-9 (pulsars, PROVISIONAL) | 2.7e13 GeV |
| one-loop lambda - 1 <= 6e-4 (the record's L350 channel) | 1.7e16 GeV |

None of these binds; the matter bounds do. The lower end is set by short-range gravity (hbar c/38.6 um = 5.1e-3 eV,
Lee et al. 2020, PROVISIONAL). The z = 3 tensor dispersion at 100 Hz and the UV corrections at 1 AU and 10 km all ask for
less (<= 1.3e-5 eV). **Window: 5.1e-3 eV to 1.75e6 GeV (17.5 decades) at C = 1e3, both footings.** These are the
solar-system and pulsar limits the record already passes in the IR; they are not re-graded.

**Cross-gate note (T2's ground, not graded).** At A = 0 (FRW, voids) the lapse's quadratic gradient term vanishes
identically in (A) (1 - alpha_par(0)/2 = 0) and the khronometric scalar speed^2 is 0. Perturbation theory around those
backgrounds is therefore not controlled. If only the z = 3 term remains, the exchange is strong below about
M_*^2/Mbar_P, roughly 1 MeV at the window top (estimate). The window's top must also sit below QG1's Lambda_s.

## Reported, not graded

- **R1, kappa and the 5.41: NOT FIXED.** In G3, a0 = m0/(c g_B) and rho_DE = Lambda/(8 pi G), so
  kappa = 2 sqrt(2 pi) m0/(c g_B sqrt(Lambda)). Lambda and m0 are independent relevant couplings (dimensions 6 and 2 at
  z = 3), and the tuning K nu g_B^2 m0 = 4 pi fixes nu, not Lambda. The 5.41 is an integration constant of the khronon
  equation (E3) (R541); a UV completion does not set initial data.
- **R2, COL1's fold: NOT RESOLVED.** Above M_* every mode disperses as omega = k^3/M_*^2. That balances an infall of
  100-300 km/s at ell = (hbar c/M_*) sqrt(c/v), which is 1.2-2.1e-3 m at M_lo and 1.1-2.0e-22 m at the window top
  (C = 1). COL1's fold is resolved at 1e-5 kpc = 3.1e14 m, 17 to 36 orders larger. The z = 3 terms are terms of an
  action, so they conserve the clock's energy. They turn the fold into a dispersive (wave) caustic at ell; they do not
  make a standing clock. COL1's other finding, only 1-4 % of the halo's charge falling in, is set on kpc scales and is
  untouched. The lead's hand expectation on the fold holds.

## Step R: what is new relative to the record

- The June map (leg v) graded the AeST aether's Horava host as ONLY-COMPATIBLE -> contested, on the
  projectable/non-projectable mismatch.
- STANDING L350 bounded the C-H/K khronon's lambda channel (c2 <= 0.6-2.9e-3).
- Book chapter 31 notes an induced SME gravity-sector coefficient (~1e-12).

All three predate (A). New here:
1. (A) is khronometric gravity with lambda = 1, beta = 0 and alpha pinned to exactly 2 at zero acceleration (G_N -> inf).
2. The branch question is moot for the law. J is non-analytic and non-polynomial, so no power-counting-renormalizable
   action, projectable or not, can contain it.
3. A computed sign error in the natural generation mechanism (leaf bosons give anti-MOND), and a coefficient wall of
   10^55 (leaf routes) or 10^29-10^30 in coupling (4-d routes).
4. The first matter-sector percolation numbers for the record: M_* <= 1.75e6-1.75e9 GeV.
5. The A = 0 vanishing of the lapse's quadratic term, flagged for T2.

## Known answers (all PASS, read before any graded line)

| check | result |
|---|---|
| KA1 power counting | [1/kappa^2] = 2 at z = 1 and 0 at z = 3; all z = 3 couplings >= 0 |
| KA2 | R^(3) of exp(-2 psi) delta: residual 0; static weak field: G_N/G = -2/(alpha - 2) = 1/(1 - alpha/2); FRW: lambda = 1 |
| KA3 | mu = A/(A + a0) from GR + (a0^2/K) J |
| KA4a 3-d determinant | non-analytic part -0.0265258238 = -1/(12 pi) (quadrature error 0) |
| KA4b thermal | J_B's y^(3/2) coefficient -0.523599 = -pi/6 (relative 1.4e-8) |
| KA4c Cl(6) | anticommutators exact; det D = (k^2 + g^2 A^2)^4 to 1.6e-15 |

## MUTATE

| twin | result |
|---|---|
| M1: G2 with boson statistics | sign FAIL (bites) |
| M2: even degree-6 polynomial | admissible (bites) |
| M3: a0 -> M_Pl in G3 | log10 R_c -6.41, PASS (bites) |
| M4: G3 without its boson | shape FAIL, Q 7.53 (bites) |
| **M5: matter bounds 1e-60** | **does NOT bite as frozen**: (ii)/(iii) read OPEN, not FAIL, because the top at C = 1e-3 is 0.68 eV > M_lo |
| M5' (post hoc, amendment A1): bounds 1e-70 | (ii)/(iii) FAIL (bites) |

The pre-run choice of 1e-60 was too weak by the lane's own formula.

## The lead's hand expectation, checked

- (i) FAIL: right. But the leaf determinant's sign is right only for fermions, and the miss is 10^55 for the leaf routes
  (about W3 squared), not 30 orders. The 4-d routes hit W3 itself (g ~ 1e29-1e30, thermal T ~ 1.7 meV).
- (ii): a window exists only far below M_Pl, as expected, but its top is lower: 1.75e6 to 1.75e9 GeV rather than
  1e9-1e10, because of the reduced Planck mass, alpha = 2 and the neutron boost route.
- (iii) PASS.
- Fold: right.

Every literature number here (Kostelecky-Russell sensitivities, Pospelov-Shang scaling, GW170817, Eöt-Wash, the pulsar
alpha_2, the khronometric speed formula) is PROVISIONAL. Changing any of them by a factor of 1000 moves no label.

## Commit ids (local / origin)

| commit | local | origin |
|---|---|---|
| criteria | c1bc0c0977 | 7a9ade7b2e |
| amendment A1 | fb95bfc882 | 89ea6abae7 |
| result (script, outputs, this file) | 2cb36884de | 551bc67dcd |

Pushed by replay onto origin/main (a0710b479c..551bc67dcd). This id table is one more commit, pushed the same way.

kappa = 1/2 FITTED; not theory closed.
