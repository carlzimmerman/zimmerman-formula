# KT7_nonthermal_ensemble: NO-GO IN THIS CLASS. No Gaussian single-field ensemble, massless at the vacuum, has the odd term, w = -1 and cell counting together. KT6's loophole closes. Argon's two replies scored below

Criteria: `FROZEN_CRITERIA.md` (cfdd2117a9), alone first, confirmed landed before the run, **not blind**. `kt7.py`, `kt7.out`, `kt7.json`, `kt7_MUTATE.out`. No download. kappa = 1/2 FITTED. Not theory closed. Nothing derived. Register K821 (KT7), K822 (Argon score).

| Ensemble | Odd term R1 | w = -1 R2 | Counting R3 | Numbers |
|---|---|---|---|---|
| Thermal, KT6 | yes | no, w > 0 | yes | w = ln(T/hbar omega) |
| E1 frozen, same spectrum | yes | no, w -> -1/3 | yes, c_E = 2 | w -0.3334 at m a = 0.01; kappa 0.707, outside both windows |
| E2 quenched source | no | not reached | not reached | G(0) = D/(8 pi m), diverges |
| E3 Lorentz vacuum, 4D | no | yes | no | mu ~ Y^(2/3), hand scaling printed as text |
| E4 Lorentz, fractional propagator | yes, by construction | yes | no | G(0) = -m/(4 pi^2); c_E = 1 gives kappa 0.282 but has no meaning here; self-consistent c_E = 12 pi^2, kappa 3.07 |

**The dichotomy.** rho + p = T S / V, so w = -1 needs U = F. Counting needs U set per mode, apart from V(m). So when the count means something, w isn't -1. When w = -1, energy is V + C, and that's KT3's zero mode. This argument is written by hand in the criteria and isn't a script's output. Not covered: non-Gaussian, multi-field, non-equilibrium ensembles. Not a no-go theorem outside the class. MUTATE, stress sign flipped: w -> +1/3, exit 1.

## Argon reply 1: NO-GO
**Stands, scoped:** for algebraic chi, (alpha, u) -> (lambda alpha, u/lambda) is an exact redundancy and every ratio cancels alpha. kappa^2 = pi alpha reproduced; form (b) reproduced. Also correct: at fixed a0, Q2 doesn't depend on alpha. Its useful reading: alpha = 1/(4 pi) is the conversion between 4 pi G and G. "Human convention" overstates it, since a0 / c sqrt(G rho) is a measurable number; what's true is that nothing here selects it. Its proof rests on chi being algebraic, so it doesn't reach KT5 to KT7's fluctuating chi. It also adds u(1) = 0, which my question didn't state; that removes C by hypothesis, as KT4 did.

**Errors, `argon_score_check.out`:**
- Table variants 3 and 4 are inverted. Argon gives kappa = (L/L1)/2 where its variants 1 and 2 use 1/(2 L/L1). Consistently: de Sitter radius kappa 1.447, alpha 2/3 (Argon 0.1727, 3/(32 pi^2)); active mass kappa 1.023, alpha 1/3 (Argon 0.2443, 3/(16 pi^2)). Both of Argon's values landed nearer the data than correct ones. 0.1727 is on CFG894's forbidden list as a0/cH_Lambda.
- Y = 1 sits at 5630 AU at the Sun, not 7000 (its sqrt(2) form gives 7960).
- Its second prediction, 15.47 and 8.20 percent boosts at Y = 1, is arithmetically right but isolated-mass only, ignoring the external field, and a principle doesn't fix it. No principle was selected, so S4 isn't met.
- "Raise the order of the zero of u' at chi = 1" would destroy the linear slope; its reply 2 corrects this.

## Argon reply 2: fix Cassini through u' near chi = 0
**Holds:** chi -> 1 is deep MOND and chi -> 0 is the high-g side. u'_p = chi^p (1-chi)^2 gives slope 2 for all p, tail exponent 4/(1-p). chi ln^2 chi gives chi = exp(-Y) exactly. u_{p=1} polynomial is right. Sign slip: u'''(1) = +2, not -2. g_e/s is 1.015, not 0.79. Its eq "chi^((p-1)/2)(1-chi) = 1/Y" should read = Y.

**Its headline is wrong.** It claims exponential mu = 1 - exp(-2Y) has Q2 = 4.10e-27, passing. That's the record's exact-exponential kernel. Computed: **3.76x ceiling, Q2 1.96e-26, FAIL**, as RETRACTIONS has it. So a fast-vanishing tail isn't enough; sharpness in the transition is what counts. Argon's number has no calculation behind it.

`argon_p_family_check.out`, `argon_p1_recheck.out`, canonical a0, Cassini only on canonical. SPARC gate as KT5: within 0.005 dex of OR mu_2, |median| <= 0.05.

| u' | Cassini | SPARC rho_DE rms, median | SPARC rho_crit rms, median |
|---|---|---|---|
| p = -1, form a | 5.48x FAIL | 0.1712, +0.047 PASS | 0.1684, +0.021 PASS |
| p = 0, form b | 3.92x FAIL | 0.1763, +0.074 FAIL | 0.1699, +0.044 PASS |
| p = 0.5 | 2.35x FAIL | 0.1804, +0.086 FAIL | 0.1720, +0.056 FAIL |
| **p = 1, polynomial** | **0.376x PASS** | 0.1863, +0.101 FAIL | 0.1757, +0.070 FAIL |
| chi = exp(-Y) | 3.76x FAIL | 0.1765, +0.075 FAIL | 0.1700, +0.046 PASS |

**p = 1 is the one real find,** mu = 2Y - Y^2 for Y <= 1, mu = 1 above, a compact Newtonian region. It passes Cassini with no heat filter and fails SPARC at the stated Upsilon. Higher Upsilon would reduce the offset (KT1 showed sharper shapes prefer it), which is not graded here. Hand-picked, no action behind p = 1. **All of this holds alpha = 1/(4 pi) fixed, so none of it bears on kappa.**

**Defect.** The first p = 1 run printed Cassini 0.00x: dblquad stepped over the corner y < 2 where nu - 1 is non-zero. `argon_p1_recheck.py` integrates that corner: 0.376x at three resolutions, and its control reproduces exponential 3.76x. The "PASS" stands; the 0.00x doesn't. The p = 1 row of `argon_p_family_check.out` is superseded on Cassini.
