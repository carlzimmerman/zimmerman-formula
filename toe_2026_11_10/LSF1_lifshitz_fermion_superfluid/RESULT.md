# LSF1 RESULT: a Lifshitz fermion superfluid as the law's microscopic origin? (2026-11-10)

**Label: KILLED AT G0, on both footings.** No renormalizable dispersion gives the |grad phi|^3 regime. Once the phase
gradient dominates, the paired gas has no condensate left: its gradient energy is flat at the condensation energy
(slope **0.000** against the 3 that deep MOND needs) in all 20 graded cells. So this rival candidate does not clear
T3(i). Its UV contacts are renormalizable, but the sector they define has no MOND regime to carry into a renormalizable
action, and BK's baryon-phase coupling is not a polynomial in the fermion fields.

TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Owner lift (no-particle and metric-only
rules, this lane only): `../OWNER_DECISION_2026-11-10_LSF1_RULE_LIFT.md` (origin 2e4c9e9b4b). Inside this lane the
fermion is a dark component carried by a particle; outside it the cold component is cold dark energy. Not a LCDM lane.
Footings never pooled.

Files:
- criteria `FROZEN_CRITERIA.md` (committed and pushed alone, before any script);
- script `lsf1.py`, outputs `lsf1.out` / `lsf1.json`;
- twins `LSF1_MUTATE=1` -> `lsf1_MUTATE.out` / `lsf1_MUTATE.json`;
- Lean `LSF1.lean` (`compile.txt`, exit 0) and false twin `LSF1_MUTATE.lean` (`compile_MUTATE.txt`, 3 errors).

Each run takes about 95 s and peaks at 3.5 GB RSS. No amendment.

## The deciding number

**Slope 0.000.** That is d ln|Delta L| / d ln q of the microscopic paired gas in BK's gradient-dominated window
(E_q >= 10|mu_eff|), against the frozen line [2.9, 3.1]. It was graded on:
- five dispersions;
- weak and strong pairing;
- both signs of mu_eff.

In 8 cells Delta L is flat at minus the condensation energy. In 10 it is identically 0, because the gas is empty
there. The two remaining cells, the tangle (D5) with mu_eff > 0, show 0.002 and 0.069: they approach the same plateau
as 1/q.

Reading F, BK's formal continuation (reported, never the lane label):
- the **k^6 candidate gives slope 9.03 / 8.97**, so the lead's |grad phi|^9 is right;
- the k^2 + k^6 crossover gives 5.2 to 9.0;
- only an isotropic tangle of 1-d Galilean channels gives 3.07 / 2.93.

## Why: the gradient-dominated regime is the depaired (or empty) gas

Three exact facts carry the result.

1. **The pair-kinetic inequality (KA8, sympy).** eps_S(k; q) - eps(k) - eps(q) is:
   - 3k^2 q^2 (k^2 + q^2)(4u^2 + 1) >= 0 for k^6 and for k^2 + k^6;
   - 0 for k^2.

   So the pair band at twist q lies at least 2 E_q above the q = 0 pair band.
2. **A positive margin certifies that no condensate exists.** With xi_S > 0 everywhere and E - |xi_S| <= Delta^2/(2|xi_S|):

       deltaOmega(Delta) >= Delta^2 [1/|g| - chi(q)] > 0   for every Delta > 0,

   because chi(q) < chi_0(mu_vac) <= 1/|g| once E_q > mu_eff. The depaired-quasiparticle terms only add. The script
   computes the margin at every window point:
   - every one of the 20 cells is positive (smallest 4.3e-3, D3 strong);
   - direct minimization over a Delta grid (finite-Delta states included) returns Delta_min = 0 at all 36 check points.

   So in the window L(mu, q) = P_normal(mu), whatever q is. Delta L = -E_cond is flat when mu_eff > 0, and Delta L = 0
   when mu_eff < 0.
3. **BK's X < 0 branch has negative compressibility (KA10).** P''(X) = -3/(4 sqrt|X|) < 0. No equilibrium state has
   it. This is CFG122's c_s^2 = 2X/m < 0, and BK's own "wrong sign" (arXiv:1507.01019 section 4.1, PROVISIONAL).

**The phase-gradient energy of a superfluid is bounded by its condensation energy:** |Delta L| <= E_cond, checked
along the whole reported curve. Deep MOND needs it to grow as |q|^3 without bound.

**This is not specific to k^6.** D1, the Galilean control (BK's own kinematics), fails G0 the same way. The general
argument below was not computed beyond the scanned branches:
- Galilean invariance makes P(mu, q) = P_0(mu - q^2/2m) exactly (KA6, to 8.2e-8);
- for any equilibrium gas, P_0(X) = 0 below the vacuum threshold;
- so BK's MOND branch is the empty gas for any Galilean superfluid, bosons with three-body contacts included. BK's
  X|X|^(1/2) is a continuation that no ground state realises.

## G0 (graded): microscopic Omega(mu_eff, q), Fulde-Ferrell mean field, T = 0

Units |mu_eff| = 1, dispersion coefficient 1. Window: 16 log-spaced q in [q_a, 10 q_a], with E_{q_a} = 10. Couplings:
- weak: Delta(q = 0) of about 0.05 at mu = 1;
- strong: E_b = 10.

D1 uses 1/a = -1.5 (weak) and +1.5 (strong).

| branch | weak, mu_eff + 1 | weak, - 1 | strong, + 1 | strong, - 1 | G0 |
|---|---|---|---|---|---|
| D1 3-d Galilean k^2 (control) | Delta L = -1.3368e-4 flat, slope 0.0000 | 0 (empty) | -1.3044e-1 flat, 0.0000 | 0 | FAIL |
| **D2 3-d Lifshitz k^6 (candidate)** | -1.4947e-5 flat, **0.0000** | 0 | -3.9320e-3 flat, 0.0000 | 0 | **FAIL** |
| D3 3-d crossover k^2 + k^6 | -1.0912e-5 flat, 0.0000 | 0 | -3.4247e-3 flat, 0.0000 | 0 | FAIL |
| D4 quasi-1-d (t = 1e-3), twist along x | -2.7796e-4 flat, 0.0000 | 0 | -7.9258e-2 flat, 0.0000 | 0 | FAIL (and no window along y) |
| D5 isotropic tangle of 1-d channels | -2.797e-4 to -2.813e-4, 0.0023 | 0 | -6.560e-2 to -7.791e-2, 0.0689 | 0 | FAIL |

- Gaps at q = 0: D1 0.1028 / 4.718; D2 0.0579 / 3.545; D3 0.0500 / 3.756; D4 0.0576 / 3.620; D5 0.0579 / 3.619
  (weak / strong).
- Condensation energies check against the textbook value N_sigma(0) Delta^2/2:
  - D1 weak: 1.337e-4, against 1.34e-4 by hand;
  - D2 weak: 1.495e-5, against 1.5e-5 by hand.
- D4 along y: E_q = 2t(1 - cos q) <= 4t = 4.0e-3, below 10|mu_eff|. No gradient-dominated window exists along y, so D4
  fails the isotropy clause by construction.
- The two-body bound state: k^6 in 3-d (KA9: chi_0 grows as E_b^(-1/2)) and the 1-d channels bind for any attraction.
  So the weak D2, D4 and D5 couplings have mu_vac = -0.0959, -0.0917 and -0.0959. D1 (a < 0) and D3 weak do not bind.

**Reported curve (mu_eff = +1, weak).** It runs from q = 1e-3 k_F to the window.

| | D2 (k^6) | D1 (k^2) |
|---|---|---|
| Small q | Delta L = -(rho/2) q^2 with d^2L/dq^2 = -0.179: analytic in q^2, a Newton-like stiffness | -0.0685, against the Galilean -2n = -0.0675 |
| Depairing | Delta = 5.0e-4 at q = 1.44e-2, 0 from q = 2.01e-2 | Delta = 0.097 at q = 5.6e-2, 0 from q = 7.8e-2 |
| Saturation | -E_cond from there on | same |
| Largest local log-slope below the window | 2.02 | 2.00 |

Neither curve ever approaches 3.

## Reading F (BK's formal odd continuation; reported, never the lane label)

L_F = P_odd(mu_eff - E_q) - P_odd(mu_eff), each branch's own free-sea EOS, same window and line.

| branch | slope (mu_eff + 1 / - 1) | G0F |
|---|---|---|
| D1 k^2 | 5.09 / 4.92 | FAIL |
| **D2 k^6** | **9.03 / 8.97** | FAIL |
| D3 k^2 + k^6 | 5.21 to 9.03 over mu_eff 1e-3 ... 1e3, both signs | FAIL |
| D4 quasi-1-d | x: 3.04 / 2.96; y: saturates at -2.54e-3 (bounded by the transverse band) | FAIL (anisotropic) |
| D5 isotropic tangle | 3.07 / 2.93 | PASS |

**The dimensional rule** (sympy; Lean `lsf1_only_1d_galilean`). The gradient-dominated L goes as c q^(d+z). Requiring
q^3 and P_0 ~ mu^(3/2) gives the unique solution {d = 1, z = 2}.

The k^6 candidate meets the EOS condition (2 x 9 = 3 x 6) but not the gradient one (3 + 6 = 9). So, as the lead
expected:
- the crossover is Galilean with the wrong P on one branch and k^6 with the wrong gradients on the other;
- only effectively 1-d Galilean fermions do both.

Under reading F the tangle is **SHAPE ONLY**: S and C pass, U2 and E fail, and D3 is inherited.

## S, C, U, E, D

**S** (NPJ1's definition; footing-independent). The force law is a = a_N + (a_*^(p-2) a_N)^(1/(p-1)), fitted to the
law:

| p | max dmu | deep slope | a_*/a0 | S |
|---|---|---|---|---|
| micro (no gradient energy: a_theta = 0) | 0.9901 | 0.0000 | - | FAIL |
| 3 (D5 under F; = BK, NPJ1 a1 reproduced) | 0.0946 | 0.9558 | 0.4223 | PASS |
| 5 (D1 under F) | 0.7039 | 1.6940 | 0.0145 | FAIL |
| 9 (D2 under F) | 0.7955 | 1.7856 | 0.0085 | FAIL |

**C** (D5 under F, rule H). In BK normalization the tangle is L = -nu_s |grad theta|^3/(48 pi m_f), so
Lambda_eff = nu_s/(32 pi m_f) (sympy).

| | alpha = 4 pi, canonical / alt | alpha = 1, canonical / alt |
|---|---|---|
| Lambda (eV) | 1.16e-4 / 1.27e-4 | 5.16e-3 / 5.67e-3 |
| m_f >= (eV), from D1 | 0.369 / 0.387 | 0.104 / 0.109 |
| nu_s (eV^2) | 4.3e-3 / 5.0e-3 | 5.4e-2 / 6.2e-2 |
| channel spacing | 3.0 / 2.8 micrometres | 0.85 / 0.79 micrometres |
| C-amp log10 R | 0.00 (alpha at its 4 pi ceiling; every dimensionful input is 28 or more decades below M_Pl) | -1.10 |
| C-loc | -23.3 | -22.75 |
| C | PASS | PASS |

Reported (R3): the k^6 scale that reproduces BK's EOS amplitude at QX28's implied (m, Lambda) is
c_6 = 1/(576 pi^4 Lambda^2 m^3), that is M_6 = 0.166 eV (canonical) / 0.184 eV (alt).

**U.**
- U1, contact dimensions z + d - n d:

  | (d, z) | two-body | three-body | U1 |
  |---|---|---|---|
  | (3, 2), D1 | -1 | -4 | FAIL |
  | (3, 6), D2 and D3 | +3 | 0 | PASS |
  | (1, 2), D4 and D5 | +1 | 0 | PASS |

  The k^6 pairing integral converges in the UV (KA4: Int d^3k/eps changes by 1e-6 from cutoff 1e2 to 1e3; at z = 2 it
  grows 10x).
- U2 FAILS for every branch. theta = atan2(Im, Re) of psi_down psi_up is not a polynomial (sympy PolynomialError). So
  -alpha Lambda theta rho_b/M_Pl has no polynomial UV form; it is undefined wherever Delta = 0, which is the normal phase
  BK use in clusters.
- The polynomial alternative is -lambda n_B (psi psi + h.c.). It has dimension +3 at z = 6, but its static source is
  2 A lambda n_B sin theta: theta-dependent and bounded. Gauss's law then does not give the enclosed baryon mass, so
  KA3's law does not follow.
- U = FAIL for every branch.

**E** (inputs PROVISIONAL, the record's CFG122 values; coupling to baryon number, Delta(B/mu) Ti-Pt = 9.05e-4).
- **Reading F (unscreened):**

  | | canonical | alt |
  |---|---|---|
  | a_theta(1 AU) | 4.84e-7 m/s^2 | 5.32e-7 m/s^2 |
  | Cassini | 7.1x the bound | 7.8x |
  | MICROSCOPE | 2.0e6x | 2.2e6x |
  | ephemeris ceiling | 4.1e8x | 3.7e8x |
  | E | FAIL | FAIL |

  These are CFG122's Reading B scaled by sqrt(0.42), checked by hand in SI. Coupling to mass instead gives eta = 0 and
  leaves Cassini and the ephemeris unchanged.
- **Micro reading:** the superfluid's real screening is the depairing G0 computes. It gives a_theta = 0 and E passes,
  but vacuously: the same depairing removes the MOND force wherever the gradient dominates.

**D** (reported items).
- **D1 Pauli / superflow** (D5 under F): m_f >= 0.37 eV (alpha 4 pi) or 0.10 eV (alpha 1) keeps the superflow and the
  channel Fermi speed below 2 v_f. Not excluded.
- **D2 forest:** the record's line, quoted: "undecided on raw forest data; a 1-D proxy against a ΛCDM yardstick falls
  1000–5000 × short". No flag.
- **D3 clusters:** QX28's BK-class result (G4, G5 FAIL, both footings) is inherited. Excluded (inherited).
- **D4 cold share.** Any branch with P_0 ~ mu^(3/2) is the polytrope P = K rho^3 (k^6: K = 6 pi^4 c_6/m_f^3). With K
  from QX28's galaxies:

  | | canonical | alt |
  |---|---|---|
  | w(1089) | 3.34e4 | 2.11e4 |
  | kinetic energy / radiation at z = 1089 | 4.4e4 | 2.8e4 |
  | kinetic energy / radiation at BBN | 4.0e32 | 2.5e32 |
  | largest share of 5.41 rho_b with kinetic <= 0.1 radiation, at 1089 | 1.3e-2 | 1.5e-2 |
  | the same share at BBN | 6.3e-12 | 7.3e-12 |

  w(1089) reproduces QX28's G6a (3e4 / 2e4) independently. **The superfluid cannot be the CMB's cold component; it must
  sit beside it**, at a share below about 1e-11 if the degenerate gas runs back to BBN.

## Labels

| branch | renormalizable (U1) | lane reading: G0 -> label | reading F: G0F -> label |
|---|---|---|---|
| D1 Galilean (control) | no | FAIL -> KILLED AT G0 | FAIL -> KILLED AT G0 |
| D2 k^6 (candidate) | yes | FAIL -> **KILLED AT G0** | FAIL (slope 9) -> KILLED AT G0 |
| D3 k^2 + k^6 | yes | FAIL -> KILLED AT G0 | FAIL (5-9) -> KILLED AT G0 |
| D4 quasi-1-d | yes | FAIL -> KILLED AT G0 | FAIL (anisotropic) -> KILLED AT G0 |
| D5 1-d tangle | yes | FAIL -> KILLED AT G0 | PASS -> SHAPE ONLY |

The labels are the same on both footings. **Lane: KILLED AT G0.** Reading F (reported only): SHAPE ONLY, via the tangle.

## Known answers (all PASS, read before any graded line)

| check | result |
|---|---|
| KA1 3-d Galilean free gas | (2m)^1.5 mu^2.5/(15 pi^2), rel 9.9e-32. The frozen line's "(spin 1/2)" formula is the pressure per spin state; two spin states give twice it, which is KA2 at z = 2 |
| KA2 eps = c k^z | rel 0 at z = 2, 4, 6; z = 6 coefficient 2/(9 pi^2) exact, exponent 1.5000000000; 1-d (4/(3 pi)) sqrt(2m) mu^1.5 rel 0 |
| KA3 BK | EL residual 0; a_theta^2/a_N = alpha^3 Lambda^2/(8 pi M_Pl); P(X = -(grad theta)^2/2m) = -(2 Lambda/3)|grad theta|^3 |
| KA4 power counting | (3,2): -1, -4 (NPJ1's -4); (3,6): +3, 0 (the lead's seed); (1,2): +1, 0; UV: z = 6 converges, z = 2 linear |
| KA5 BCS gap | mean field / (8/e^2) exp(-pi/(2 k_F|a|)): 1.00057 at 1/(k_F a) = -2, 1.00003 at -3 |
| KA6 Galilean invariance of the FF code | Omega_FF(mu, q) = Omega_BCS(mu - q^2) to 8.2e-8, no depaired quasiparticles |
| KA7 Delta = 0 is the normal state at q > 0 | D2 6.2e-10, D1 1.4e-8, D3 1.6e-8 |
| KA8 pair-kinetic inequality | above (manifestly non-negative) |
| KA9 k^6 binding | slope -0.500000; closed form 1/(12 pi sqrt(2 E_b)) ratio 1.000000000000 |
| KA10 convexity | free gas P'' = p(p-1) c mu^(p-2) > 0; BK P''(X < 0) = -3/(4 sqrt|X|) < 0 |

## MUTATE (all bite; `lsf1_MUTATE.out`)

| twin | result |
|---|---|
| M1 BK's formal X\|X\|^(1/2) through the G0 window test | slope 3.044, cost, growing: PASS (the detector can pass) |
| M2 S detector | p = 3: 0.0946 (NPJ1's number, to 1e-3) PASS; p = 9: 0.7955 FAIL |
| M3 U1 counter | (3,2) three-body -4; (1,2) two-body +1; (3,6) two-body +3 |
| M4 E | zero force PASS; formal force FAIL |
| M5 Galilean identity applied to k^6 | measured Omega shift 3.6e-7 at q = 0.002, against n q^6 = 2.1e-18: the identity fails (it is Galilean-specific) |
| M6 convexity detector | free gas stable; BK's odd branch unstable |
| M7 superfluid forbidden to depair (Delta held, no quasiparticles), D2 | Delta L -1.9512e-2 -> -1.9516e-2: growing (bites, as frozen), slope 5.5e-5 |

**What M7 shows** (reported, it moves no label): the frozen twin's premise was that the saturation is the depairing.
That is only half right. A superfluid forced to keep its gap also saturates, at the vacuum level (-(P_0 + E_cond +
Delta^2/|g|)), because the twisted pair band empties once E_q > mu_eff. Depairing (weak) and band emptying (any
coupling) both cap the gradient energy.

Lean: `LSF1.lean` compiles, exit 0, with 5 theorems:
- lsf1_only_1d_galilean;
- lsf1_eos_iff (z = 2d);
- lsf1_k6_eos;
- lsf1_k6_gradient;
- lsf1_crossover_ends.

`LSF1_MUTATE.lean` fails as it should, with 3 errors: (3,6) gives exponent 3; the EOS forces z = 6; 3-d Galilean gives
3/2.

## Reported (not graded)

- **R1, BK's Solar-System screening.** BK argue that near the Sun the flow exceeds a critical velocity and the
  condensate decoheres (1507.01019 section 5, PROVISIONAL). The criterion G0 computes, E_q > mu_eff, is the
  gradient-dominated condition itself, so it holds wherever BK's MOND regime is used, not only near the Sun. Applied
  consistently, the screening and the MOND force vanish together.
- **R2, what "effectively 1-d" would mean.** Fermions confined to an isotropic, static tangle of strings, flux tubes or
  wires, with all of these at once:
  - a channel spacing of about 3 micrometres;
  - m_f of at least 0.1-0.4 eV;
  - a string tension at most (7.7e-5 eV)^2 (canonical, alpha 4 pi) or (2.2e-5 eV)^2 (alpha 1), so that the network's
    own energy stays below rho_DE.

  Such a network must not scale like a cosmological string network: it would be a frozen "string solid" in the clock's
  frame. Its fermions must be massive Galilean bound states, not the massless (z = 1) zero modes of superconducting
  strings, which give P ~ mu^2. Stated in words, not computed. Even granted all that, G0 kills it: the tangle's
  microscopic gradient energy saturates like every other branch.
- **R4, kappa and 5.41.** a0' = alpha^3 Lambda^2/(8 pi M_Pl), with Lambda_eff = nu_s/(32 pi m_f) (tangle) or set by
  c_6 (k^6). Every branch carries a free dimensionful input, not tied to rho_DE. The 5.41 is untouched (D4: the
  superfluid cannot carry it).
- **R5, strong pairing.** On the BEC side (E_b = 10) d ln P/d ln mu_eff is 1.994 (D2) and 1.902 (D5): a Bose gas of
  pairs with a two-body EOS, not the Fermi sea's 3/2. Strong pairing loses the X^(3/2) that motivated k^6. The pairs
  are at least 2 E_q heavier at twist q (KA8), and the gradient energy still saturates.

## Step R (quoted, not re-graded)

The criteria file's section R carries the record's lines. They are not re-graded here, and none of them changes:
- NPJ1 a1 (SHAPE ONLY: S 0.0946, C pass, U FAIL);
- CFG117 (the additive form failed in all 16 cases);
- QX28 (FAILS at G3, G4, G5, G6, G8);
- CFG122 / CFG154 (G5.1 c_s^2 < 0; Solar System Reading B);
- HF1 / HC1 (light-fermion lifts: FAILS);
- the forest audit (never quoted flat).

This lane adds:
- the microscopic reason for CFG122's G5.1: the X < 0 branch is not a state;
- an independent reproduction of QX28's w(1089);
- an independent reproduction of NPJ1's 0.0946.

## What this means for the TOE

T3(i) stays FAIL (HZ1's label; this lane does not regrade it). The ROOT note asked for a sector whose infrared regime
gives the -|A|^3/3 term. NPJ1 found that only BK's superfluid has the shape, size and locality, and it lacked a
renormalizable UV.

This lane gave BK a renormalizable UV (k^6 fermions, contacts +3 and 0). The price was the shape:
- formally |grad phi|^9 (slope 9.03);
- microscopically no MOND regime at all: the gradient energy of any equilibrium paired gas is capped by its
  condensation energy, and BK's X < 0 branch has negative compressibility.

The superfluid route to emergent MOND therefore needs something this lane did not compute. Candidates are a
finite-temperature or non-equilibrium state (BK's beta >= 3/2 operator), or a non-mean-field fixed point. A static T = 0
paired gas of any dispersion does not supply it.

## Numerical history (stated in full)

- **Run 1** crashed in KA5 (mpmath findroot). No graded line was printed.
- **Run 2** crashed in KA5: the script's asymptotic formula had exp(-pi/(2|1/a|)) for exp(-pi|1/a|/2), a typo against
  the frozen formula. Fixed before any graded line.
- **Run 3** printed the graded lines with **KA6 failing** (rel 1.06e-4) and labelled itself OPEN. The 2-d grid for D1
  stopped at k = 4, where the regulated tail approximation is too crude. k_max for D1 was extended to 40 in the fine
  and curve grids.
- **Runs 4-5:**
  - KA6 passes at 8.2e-8;
  - the G0 section is byte-identical between run 3 and run 5, so the KA6 fix touched only the D1 control's KA and its
    reported curve (D1 small-q stiffness -2.95 in run 3, an artefact, now -0.0685);
  - U2's sympy check returned None in run 3; it now uses PolynomialError, with the same verdict;
  - peak memory came down from 6.8 GB to 3.5 GB by freeing the KA grids;
  - M5 was re-expressed against the Galilean prediction n q^6, because its first form divided by a 1e-18 shift.

  No criterion changed.

## Limits

- Mean field at T = 0, with an s-wave contact and a single-plane-wave (Fulde-Ferrell) pair state. LOFF multi-q states,
  vortices, finite T (BK's own fix) and fluctuations beyond mean field are not computed. The certificate in point 2 is
  exact for the mean-field normal-state instability and for the two-body bound state at twist q.
- In 1-d there is no true long-range order (a Luther-Emery liquid). A tangle would need inter-channel coupling, which
  is not modelled.
- E and D inputs are the record's recalled values (PROVISIONAL), and K is QX28's galaxy calibration.
- The literature is PROVISIONAL: BK arXiv:1507.01019 (sections 4.1, 4.2, 5 read via a summariser); Sharma-Khoury-
  Lubensky arXiv:1809.08286 (the three-body EOS's wrong-sign problem); BFK arXiv:1711.05748.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Commit ids (local / origin)

| commit | local | origin |
|---|---|---|
| criteria | 1bc74e543d | 700e0c9c1c |
| result (script, outputs, Lean, this file) | (filled by the id-table commit) | |
