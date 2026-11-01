# DR8_pressure_core_response: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** An outside text says Blumenthal's rule wrongly treats a cored halo's inside as circular orbits, proposes a pressure term, and claims a 5-10× cut inside 2.2 R_d for L★ spirals with dwarfs staying strong. (A) What does the rule do on the record's lines? (B) Decisive: how does a live cored equilibrium halo actually respond to a grown disc, against Blumenthal on the same start?

**Record check.** The proposed rule isn't in any lane (grep). DR7 says "No live test with a core: LC1 starts from the zoom's own profile"; X81 says zoom halos are cusps. PZ1 and LC1 grow discs in zooms. No Eddington realization of the smooth core exists in the repo (grep "Eddington": unrelated hits). So B is new; DR7 capped Blumenthal by Q and is not an orbit calculation.

**Standing.** κ = ½ FITTED, unused here. Newtonian, gravity only, no feedback. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **The rule is posited by the outside text, not derived.** Its numbers (R_d 2.5, r₀ 15-25 kpc, 5-10×) are unverified and are checked here. It adds no free number, but its form is a choice.

**Not blind.** NR3, DR3, DR7, LC1, RM1, UR1 and X81 results were read. B's live outcome is unknown to me.

**Expectation on record.** A: as stated the rule loses repo's (1+F), so no cluster expansion, and keys and X-COP worsen; the linear term grows with r_i, so it suppresses contraction at every radius, not just inside r₀, and Υ rises well above 0.35; tilt stays or worsens, dwarfs get cut too; no full clearance. B: Blumenthal over-predicts on a core inside r₀, by ×1.5-3 in Q − 1 near R_d and approaching 1 by r₀ or beyond (the known harmonic-core limit: isotropic adiabatic growth gives ρ ∝ r^(-3/2), Blumenthal r^(-9/4)). The exact isotropic action calculation should track live; the rule's 5-10× won't hold live at 2.2 R_d. NFW control: LC1's class. If the correction is confined inside r₀, the 150-250 km/s bins, which read at 2-5 R_d, get only part of the relief.

## Rules
With r_f, r_i shells, M_i ≡ M_c0(r_i), P(r_i) ≡ M_c0(r₀) r_i/r₀, mass conservation M_f(r_f) = M_i:
- **RULE (as stated, primary of A):** r_i/r_f = 1 + M_b(r_f)/[M_i + P].
- **RULE_F (reported and graded):** the repo's Blumenthal carries F = M_b,tot/M_c,tot: r_f (M_b + M_i) = r_i M_i (1+F). The stated rule's Blumenthal drops it. Minimal restoration, reducing to the repo's at P = 0 and to the stated rule at F = 0, with the edge fixed: r_i/r_f = [M_i + M_b(r_f) + P]/[(1+F) M_i + P].
- **BLUM0 (reported):** the stated rule with P = 0 (F dropped, no pressure), to separate the two changes.
- **Analysis (not grades):** invariant it implies; monotonicity r_f(r_i), crossings counted; edge mapping; limit with a point mass in a harmonic core (compare Young 1980's ρ ∝ r^(-3/2), and Blumenthal's r^(-9/4)); Gnedin's form; what the Jeans argument really gives. Literature look-ups provisional.
- r₀ inferred in the wrapper from M₀'s own shape, so the harness isn't edited; check K3.

## A: runs
UR1's path through a driver, as NR3, own cache, NR2 MEDIAN (ρ 1.241, 1.147, η(10¹²) 21.53), canonical, f★ 0.034, EM1, both backgrounds: rows EM1|off, EM1|blum (baseline), EM1|RULE, EM1|RULE_F, EM1|BLUM0, MUTATE. Reported: r₀, R_d, r₀/R_d, r_i/r₀ for shells landing at 2.2 R_d, and (Q_blum − 1)/(Q_rule − 1) at 2.2 R_d and r₀, by V_flat. LOW and HIGH inputs only if a row reaches the SPARC line at MEDIAN.

**Pass lines (the record's):** SPARC rms ≤ 0.110, Υ 0.50-0.80, both backgrounds; |tilt| ≤ 0.15; 15 keys |Z| ≤ 2; X-COP |mean| ≤ 0.05, rms ≤ 0.10; groups |Z| ≤ 2; LITTLE THINGS |median E| ≤ 0.10. Keys on this path run on UR1's gas inputs as NR3, DR3 and DR7; GS4's +0.005 is applied only if a row otherwise clears everything.

**Labels, on RULE and on RULE_F separately:** CLEARS (all lines; never "pass" before LOW, HIGH and a win's verification); LINE, GATES FAIL (SPARC line reached, name what fails); MOVES, FAILS (Υ moves ≥ 0.02 from 0.35/0.36, line missed); NO MOVE. [NOISE-LIMITED] if LOW or HIGH differ. **Claim's number:** 5-10× is met if the median (Q_blum − 1)/(Q_rule − 1) at 2.2 R_d for 150-250 km/s is in 5-10.

## B: runs
**Halo.** The graded smooth core at total 10¹²: M_c0(r) = π Σ r₀² B_S(r/r₀), B_S = 4[asinh x − x/√(1+x²)], ρ ∝ (1 + x²)^(-3/2), with EM1's M200,cold = f_c 10¹² (LC1's setup), Σ and r₀ read from the harness at that mass, NR2 MEDIAN. **Taper** beyond R200: Kazantzidis form, ρ(R200)(r/R200)^ε exp[−(r − R200)/r_d], r_d = 0.1 R200, slope continuous (the grader cuts sharply; a live halo can't). If f(E) < 0 anywhere, raise r_d to 0.2 then 0.3 R200, disclosed. Cut at R200 + 10 r_d.
**Total mass.** Particles carry M_sim = M_c0,total + M_d; particle mass goes m(t) = m[1 − M_d(t)/M_sim], as LC1, so cold mass at the end equals the grader's M_c0. **Isolated: no accretion, no Λ term (OLH2 = 0), no cosmological expansion. LC1 had all of them.**
**Realization.** Isotropic, Eddington inversion on the unsoftened potential, rejection sampled.
**Disc.** LC1's: Miyamoto-Nagai a = 3.565 kpc, b = 0.2 a, M_d 6.72e10 (lc1_setup.json), fixed axis z, linear in time over **7.7 Gyr** (LC1's t₀ to z = 0), no back-reaction, centred by LC1's `XA.centre` every 10 steps; force by ZK1's x48_fast kernel, step rule LC1's η 0.2 √(ε/a_max).
**Size.** N = 60,000, ε = 0.7 kpc (3ε = 0.59 R_d; below LC1's 1.32). If one measured run projects above 12 h at current load, N = 40,000, disclosed. State N(<r₀), t_relax.
**Runs.** Core seeds 1-5, same realization with and without disc. NFW control seeds 1-3, same setup, same M200, c = 12.95 (LC1's no-disc z = 0 median, measured there on its fit, used here as r200/r_s), same pairs. One no-disc core seed to 13.8 Gyr. MUTATE core seed 1, M_d × 2, own directory. Preemptible, one thread, nice 15. Runs directory gitignored; results JSON committed.
**Centre.** If centre jumps in a no-disc core run have rms > 0.1 R_d between updates, LC1's centre is too noisy on a core: all runs use the centre of mass inside r₀ (iterated), disclosed, before any disc reading.

## B: read-outs
Same-seed pairs at the end (7.7 Gyr). Q(r) = N_disc(<r)/N_nodisc(<r) as LC1, r/R_d 1, 2, 2.2, 3, 4, 6, 8, 10, r/r₀ 0.25, 0.5, 1, 2. Predictions on the seed's no-disc end state (as LC1) and also on the exact analytic start: Q_B (repo's Blumenthal), Q_R (RULE), Q_RF (RULE_F), Q_G (Gnedin 0.85, 0.8, r200), and **Q_A: spherical isotropic adiabatic invariants (J_r, L conserved, disc monopole, self-consistent; particles' own E, L)**, added because it answers what the invariant really gives. Disc M_b(r) is Blumenthal's in LC1's reader (M_d[1 − a/√(r²+a²)]), the same for all.
f_X = median over r/R_d 2, 3, 4 of (Q − 1)/(Q_X − 1), LC1's window, per seed, median over seeds, 95 % seed bootstrap (20,000 draws, rng seed 1; few seeds, so the interval is coarse, and stated). R_live with LC1's `S_fit`, at r/R_d windows as LC1, reported.

**Verdict, core:**
- LC1's lines on f_B: **BLUMENTHAL HOLDS** ≥ 0.8, **PARTIAL** 0.4-0.8, **WEAK RESPONSE** < 0.4.
- **OVER-PREDICTS** if f_B's interval lies below 1; else **NO DETECTED CUT**. Stated also at r/R_d 1 and r/r₀ 0.25, 0.5, 1, 2.
- **Claim 5-10× live:** (Q_B − 1)/(Q − 1) at 2.2 R_d in 5-10 in the median. **Rule's form:** RULE or RULE_F MATCHES if f_X's median is 0.8-1.25 and its interval contains 1.
- **Control:** NFW must read f_B ≥ 0.8 or within LC1's range [0.54, 1.07], and R_live ≥ 1.45. If not, the core's reading is not usable: UNDECIDED.

**SPARC, only if f_B's interval lies below 1 and its width ≤ 0.3, labelled MEASURED AT ONE MASS, not a rule:** on the same path, M_f = M₀ + f(r/r₀)(M_f,blum − M₀), with f(r/r₀) the live median table at this mass, flat beyond the ends. Reported, no pass or fail claimed; LC1's and DR3's carry are the model.

## Checks (failed check: no verdict on that part)
**A.** K1 EM1|blum through the wrapper against NR3 MEDIAN's: Υ, rms, tilt, cluster preds |d| ≤ 1e-6. K2 RULE_F at P = 0 reproduces `contract` on a test profile ≤ 1e-6, RULE at M_b = 0 is identity. K3 r₀ inferred from M₀ ≤ 1e-6 on test and in the path (count failures). K4 M_f monotonic, conservation on a test profile. MUTATE M_b × 2 in RULE moves Υ. Crossings reported.
**B.** K5 Eddington: Hernquist closed-form f(E) against my numerical inversion, ≤ 1 % over the bound range; ρ recovered from f ≤ 1 %; f ≥ 0 for the core and NFW. K6 sampled M(<r) against analytic, within Poisson at 2σ on most radii, |2T/W − 1| ≤ 0.03. K7 stability no disc: |Δ ln M(<r)| ≤ 0.05 at r/r₀ 0.5, 1, 2 and ≤ 0.10 at r/r₀ 0.25 over 7.7 and 13.8 Gyr; energy drift ≤ 1 %. Failing K7: UNDECIDED unless drift is under the measured signal by ×5, then stated. K8 M_d = 0 path against the plain kernel, ≤ 1e-12. K9 LC1's disc force against its potential's gradient ≤ 1e-6. K10 SIGTERM + resume vs uninterrupted ≤ 1e-12. K11 reader: LC1 seed 1 run through my reader reproduces lc1_results Q, Q_B, Q_G ≤ 1e-6; identity pair Q = 1; particles moved to Blumenthal's radii give f_B ≈ 1 within 0.05. K12 action solver: M_b = 0 null, within 2 %; Young's slope −3/2 ± 0.15 for a point mass in a harmonic core; Blumenthal reproduced nowhere needed. MUTATE M_d × 2: Q(3 R_d) − 1 moves > 30 %. Wall time measured on one run first and stated.

Only this directory is written. No pushes, no deposits, no new data.
