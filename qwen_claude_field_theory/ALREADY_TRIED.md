# ALREADY_TRIED — ideas cut from the 500 because the corpus already answered them

Each entry is reproduced verbatim as it stood before the collision check, followed by a
`PRIOR:` line naming what was tried, where, and with what verdict. **Do not re-issue these
to a worker.** They are kept so the reason for the cut is on the record and so the same
idea is not reinvented later.

Sources for every PRIOR line: `PRIOR_WORK_INDEX.md`, `RETRACTIONS.md`, `STANDING.md`,
`qwen_38_experiment/KAPPA_LEDGER.md`, and the named committed scripts.

---

## Range I401-I500 (kappa derivations, sharpened measurements, discriminators)

Seventeen cut. Their ids were reused for backfills drawing on seeded angles S1-S4, so the
range remains contiguous at 100.

**I411 — Brane-tension matching at beta = 1 fixes kappa.** HYP: with M^4 = rho_Lambda c^2 and beta = 1, the
normalisation of K(Q) is not free, so kappa is fixed once M^4 is. USES: N1+N2+N3. DO: write
K(Q) = -M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2) in sympy, impose a0^2(Q) = kappa^2 G(-K), evaluate at
the cosmological fixed point, and solve for kappa with M^4 pinned. DATA: analytic (fixed point
from nbody_2026/stage75_the_closed_theory_2026.py). PASS: kappa = 0.50 +/- 0.05 with no extra
input. KILL: kappa remains a free normalisation of K -- name which rescaling absorbs it.
PRIOR: duplicates the computation of I401 (the -K(Q_0) = M^4 identity) and I404 (the beta=1 +
w=-1 parameter count), violating C2; and its PASS branch is the "solving for the target and
calling the output a result" failure mode logged three times in RETRACTIONS.md (kappa=1/2 solved
for eps_tot; solved for K_B). beta=1 is SELECTED not derived — qwen LEDGER t011/t012,
nbody_2026/stage20_beta_equals_one_derivation_2026.py. Verdict: DEAD, re-tread + poisoned PASS.

**I419 — The aether prefactor (1-K_B/2) and the promoted a0.** HYP: the quasi-static
G-tilde = (1-K_B/2) G rescales what a0^2 = kappa^2 G(-K) means observationally, so the fitted
kappa is really kappa sqrt(1-K_B/2). USES: N1+N2. DO: propagate K_B in [0,0.25] (BBN) through the
promotion and print the implied true kappa given the measured 0.529 +/- 0.034. DATA: analytic.
PASS: the true kappa crosses 0.500 for some allowed K_B -- state which K_B, as a prediction.
KILL: the quasi-static sector is K_B-blind (as the arXiv:2304.05134 check found) -- then record
that the fitted kappa is already the bare one.
PRIOR: both branches are already decided. "K_B = 3/2 from the aether sector as a route to the
factor 2" is RETRACTED — the assumption was INVERTED (G_cosmo/G_local is strictly < 1, supremum
exactly 1, where the candidate needed 4) and its "prediction" was a tautology (kappa=1/2 => K_B=3/2
identically under its own map): stage46 -> stage48 -> stage50. The KILL branch is also already
committed: quasi-static phenomenology is K_B-BLIND in every OBSERVABLE, G-tilde = (1-K_B/2) G-hat,
K_B appears 0x in arXiv:2304.05134 (verified). Verdict: DEAD, PASS branch is a retracted target.

**I420 — Both footings through the same fit.** HYP: the canonical footing (rho_DE, cH_Lambda,
a0 = 9.3619e-11) and the alt (rho_total, cH_0, 1.1279e-10) give kappas that differ by the ratio
of the two a0 values, 1.205, not by anything the data resolve. USES: N1+N5. DO: fit the a0-line
slope once, convert to kappa under both footings with Upsilon refit on BOTH sides, print both
kappas, both chi^2, and the delta-chi^2. DATA: qwen_38_experiment/data/rar_sparc_a0units.json,
real_research/rar_framework_a0_mlfit.py. PASS: |delta-chi^2| < 4 -- the data do not choose a
footing, state that as the standing position. KILL: > 9 -- name the preferred footing.
PRIOR: answered and standing. The SPARC RAR is convention-COMPATIBLE and NON-diagnostic at the
20% level (memory index working rule; redteam_rar_framework_a0.py, sparc_rar_honest.py), and the
four-kernel shape systematic is 26.3% — larger than the 20.5% footing ratio this idea would try
to resolve (mi_routeA_shape_invariant_a0_2026.py, mi_shape_systematic_mechanism_2026.py). The
frozen-nuisance versions of exactly this comparison are RETRACTED. Verdict: DEAD, answered.

**I422 — Is kappa the same in the deep and transition regimes?** HYP: kappa fitted on y < 0.1
and on 0.1 < y < 10 with the a0-line agree, so the normalisation is not absorbing a shape error.
USES: N1+N5. DO: split the RAR at those y, fit a0 in each with Upsilon refit in each, convert to
kappa, and compare with errors. DATA: qwen_38_experiment/data/rar_sparc_a0units.json. PASS: they
agree within 1.5 sigma. KILL: they differ at > 3 sigma -- the a0-line's shape is wrong and kappa
is contaminated; report the sign of the difference.
PRIOR: this is the depth split, already run. The shape systematic across four kernels on the full
SPARC RAR is 26.3%; it COLLAPSES WITH DEPTH but sigma(a0)_stat grows about as fast, so the best
total error is 8.49% and NO depth resolves the kappa gap better than 2 sigma —
mi_routeA_shape_invariant_a0_2026.py, mi_shape_systematic_mechanism_2026.py [SETTLED].
Verdict: DEAD, answered. (The surviving new angle — whether the LEGAL FAMILY agrees with the
a0-line in the deep regime — is retained as I450, which cites this prior work in its DO:.)

**I424 — D-dimensional promotion as a negative control on kappa.** HYP: writing the promotion in D spacetime
dimensions does not produce a factor that equals 1/2 uniquely at D = 4. USES: N2+N3. DO: redo
a0^2 = kappa^2 G_D(-K) with the D-dimensional Newton constant and brane tension, extract the
D-dependent prefactor, and evaluate for D = 4..11. DATA: analytic. PASS: exactly one simple
D-factor gives 0.50 +/- 0.02 at D = 4 and nothing else does. KILL: two or more do, or none does
-- record the count; the corpus already forbids quoting kappa as a D-dependence.
PRIOR: kappa = (2/3)(D-1)/D as a D-dependence is on the DO-NOT-CITE list —
mi_kappa_from_dimension_2026.py, mi_kappa_D_dependence_rigidity_2026.py [RETRACTED]. A PASS here
re-derives exactly that retracted claim, which PRIOR_WORK_INDEX.md §0 names as the worst possible
outcome of the whole run. Verdict: DEAD, poisoned target.

**I425 — pi-free census, unrestricted generators (control for I408).** HYP: the fraction of
simple pi-free rationals-times-roots landing in [0.4,0.6] is small, so hitting 1/2 is mildly
informative even without the theory's own constants. USES: N1+N3. DO: enumerate p/q x r^s for
p,q in 1..6, r in {2,3,5,6}, s in {-1,-1/2,1/2,1}, dedupe, count the fraction in [0.4,0.6], and
compare with the brane-constrained fraction from I408. DATA: analytic. PASS: the fraction is
below 10% AND the brane-constrained set is tighter. KILL: above 20% -- say plainly that "kappa is
a simple number" is weak evidence.
PRIOR: the unrestricted census is done and NULL. qwen LEDGER t002
(runs/t002_epsilon32pi_enumeration.py): "not special: 3 matches vs 2.23 expected in the +-15.6%
window, typical". And stage66_kappa_rational_evidence_2026.py narrowed "kappa=1/2 is
distinctively simple": at +-7.8% precision all five natural parameterisations admit a simple
rational (q <= 10), with 5/9 (0.11 sigma) and 4/7 (0.48 sigma) CLOSER than 1/2 (1.19 sigma).
Verdict: DEAD, answered. (The brane-RESTRICTED census survives as I408.)

**I426 — Adding pi to the generators (why the programme insists pi-free).** HYP: including pi,
sqrt(pi), 2pi, 4pi raises the hit fraction sharply, which is exactly why a0 = kappa c sqrt(G
rho_Lambda) is stated with a pi-free kappa while Z carries sqrt(pi). USES: N1+N3. DO: rerun BOTH
censuses with pi, sqrt(pi), 2pi, 4pi added -- I425's free generators and I408's set built only
from the brane's beta, Lambda_D/Q_0 and Q_0 -- and table all four fractions. DATA: analytic.
PASS: the pi-free fraction is >= 2x smaller in BOTH censuses. KILL: equal in the brane-restricted
census -- the restriction buys nothing where it should matter most; soften the pi-free claim.
PRIOR: depends on I425 (dead), and its PASS branch restates a RETRACTED claim: "the
pi-cancellation in a0 = kappa c sqrt(G rho_Lambda) is evidence for kappa=1/2" is logically
identical to "kappa=1/2 exactly", and at the measured kappa=0.551 the pi's do not cancel at all —
stage66 PART C [RETRACTED]. The pi-free content that survives is stage43's reduction: "kappa=1/2"
is identically "Z = 2 sqrt(8pi/3)" [SETTLED]. Verdict: DEAD, poisoned target.

**I428 — Discriminating power of the four in-2-sigma kappas.** HYP: the four candidates inside
2 sigma of 0.529 +/- 0.034 predict a0 values the SPARC RAR cannot order. USES: N1+N5. DO: list
them, compute each a0, and compute the delta-chi^2 each incurs against the a0-line fit with
Upsilon refit on BOTH sides (never freeze Upsilon). DATA:
real_research/rar_framework_a0_mlfit.py, qwen_38_experiment/data/rar_sparc_a0units.json.
PASS: best minus worst > 9 in chi^2 -- the data DO order them, publish the ranking. KILL: < 4 --
record that the data do not order them and that anchoring buys a cheaper fit, not a better one.
PRIOR: answered in the adverse direction and the favourable banked version is RETRACTED. The
kappa=1/2 versus Milgrom-2020 1/2pi discrimination on SPARC is shape-dependent and NOT resolved:
four transition shapes give 1.192x/1.154x/1.059x/0.938x preferred a0, the operative exponential
kernel FAVOURS 1/2pi at 0.66 sigma, and no shape reaches 3 sigma —
mi_routeA_a0_estimator_invariance_2026.py (7/7). The banked "2.2 sigma favours 1/2" was a
one-shape (alpha=1) result and is RETRACTED. Verdict: DEAD, answered.

**I436 — Upsilon_disk zero point on the a0-line slope.** HYP: per-galaxy versus global Upsilon
shifts the a0-line kappa by more than 0.02. USES: N1+N5. DO: refit the slope of
g_obs^2 - g_bar^2 = a0 g_bar with (i) global 0.5, (ii) global 0.7, (iii) per-galaxy Upsilon with
a 0.1 dex prior; report kappa and sigma each way. DATA:
qwen_38_experiment/data/rar_sparc_a0units.json, real_research/data/SPARC_Lelli2016c.mrt.
PASS: the three agree within 0.02 -- the zero point is not the blocker. KILL: they spread beyond
0.05 -- name Upsilon as the blocker on the critical path to +/-3.7%.
PRIOR: joint (a0, Upsilon_3.6) SPARC refits, marginalised-M/L RAR and SED priors have all been run
on the framework's OWN nu — rar_joint_a0_upsilon_sedprior.py, rar_marginalized_ml.py,
prep_2026/a0_line_mlpriors/* [SETTLED] — and the stellar M/L zero point is already NAMED as one of
the two unlocks for kappa (mi_kappa_error_budget_unlock_2026.py,
nbody_2026/stage67_kappa_precision_path_2026.py). It also duplicates the Upsilon row of I435's
budget and the population prior of I449. Verdict: DEAD, answered + C2 collision.

**I438 — Bulge-free subsample as a clean a0-line kappa.** HYP: dropping bulge galaxies removes
the largest M/L systematic at tolerable cost in N. USES: N1+N5. DO: split SPARC into bulge and
no-bulge, fit the a0-line slope on each, compare centres and errors, and state the H0 convention
used for distances. DATA: real_research/data/SPARC_Lelli2016c.mrt. PASS: the no-bulge sigma_kappa
<= 0.040 and agrees with the full sample within 1 sigma. KILL: sigma inflates beyond 0.06 without
moving the centre -- the cut is not worth it, say so.
PRIOR: mi_bulge_ml_cannot_be_pinned_2026.py [SETTLED] — the bulge M/L can be neither pinned NOR
eliminated. This idea is the "eliminate" half of a question already closed both ways. Verdict:
DEAD, answered. (The "pin it with a free prior" half is retained as I437, which cites this script.)

**I440 — Gas-dominated subsample: the Upsilon-free a0-line kappa.** HYP: points where gas exceeds
80% of baryonic mass give a kappa with zero stellar M/L dependence -- Carl's sharpest
single-number estimator. USES: N1+N5. DO: select them, fit g_obs^2 - g_bar^2 = a0 g_bar by
orthogonal distance regression, convert to kappa, report sigma and the point count. DATA:
qwen_38_experiment/data/rar_sparc_a0units.json, real_research/data/SPARC_Lelli2016c.mrt.
PASS: sigma_kappa <= 0.05 with no Upsilon dependence. KILL: fewer than 150 usable points or
sigma > 0.10 -- report the count so the channel is priced.
PRIOR: this is the committed a0-line result. The gas-dominated slope is already the sharpest
single-number a0 constraint in the corpus, at 0.84-1.36e-10 (+-16%, no footing lean) — memory
index project_a0_line. Note also that "the a0-line as the sharpest single-number a0 constraint"
is RETRACTED AS SHAPE-FREE: it carries an unquoted shape systematic comparable to or larger than
the gap it is used to probe (STANDING.md §0). Verdict: DEAD, answered.

**I444 — H0 convention on the distance-free kappa = 0.551 +/- 0.043.** HYP: the known ~7%
systematic on the distance-free estimator is entirely the H0 choice, so a band -- not a folded
error -- is mandatory whenever it is compared with the a0-line's 0.529. USES: N1+N5. DO:
recompute it at H0 = 67.4, 70.0, 73.0 km/s/Mpc; print three values, the spread, and the overlap
with 0.529 +/- 0.034. DATA: real_research/rar_framework_a0_mlfit.py,
real_research/data/a0_of_z.csv. PASS: spread is 7% +/- 2% and reported as a systematic band.
KILL: it exceeds 12% -- H0 dominates and must lead every quote of this estimator.
PRIOR: kappa_h0_convention_audit_2026.py (24/24) [SETTLED] already did exactly this and more:
kappa ~ h^(2 q_eff - p), H0-invariant only at q_eff = 0.500 or 0.730 and NEITHER estimator sits
there; a Planck-consistent rescale moves a0 by +6.5-7.3% = 4.0x the 1.84% statistical error;
standing rule is "always quote kappa with its H0", and it is explicitly NOT a direction claim.
Verdict: DEAD, answered. (The per-galaxy-distance exponent, which the audit does not give, is
retained as I442.)

**I456 — Dwarf spheroidals as a deep-MOND kappa with the EFE handled.** HYP: Local Group dSphs
probe y < 0.01 where the a0-line and the legal family coincide, so they measure kappa cleanly if
isolated. USES: N1+N5. DO: use the McConnachie compilation, split isolated versus EFE-dominated
by comparing g_ext with a0, and fit kappa to the isolated ones only. DATA:
real_research/data/dsph/mcconnachie2012_dsph.csv. PASS: >= 6 isolated dSphs give joint
sigma_kappa <= 0.12. KILL: fewer than 4 qualify -- report the count and close the channel.
PRIOR: the dSph channel was DOWNGRADED by real data — systematics-limited, NOT sample-limited;
per-object scatter 0.38-0.48 dex and the dominant Upsilon_V error is COHERENT so sqrt(N) does not
help; "N~150, archival" is RETRACTED (STANDING.md §3D; mi_dsph_closure_test_real_data_2026.py,
mi_forecast_systematics_audit_2026.py). The PASS branch here assumes the sqrt(N) combination that
was withdrawn. Verdict: DEAD, poisoned PASS.

**I462 — What single improvement reaches +/-3.7% on kappa?** HYP: exactly one named error term
must improve, by a computable factor, to reach sigma_kappa = 0.020 on the a0-line estimator.
USES: N1+N5. DO: using the I435 budget, solve for the required fractional reduction in each term
with the others frozen; print the table and mark which are achievable with existing data.
DATA: outputs of I435. PASS: at least one term needs <= 2x improvement. KILL: every term needs
> 4x -- name the new dataset required and stop quoting +/-3.7% as reachable.
PRIOR: nbody_2026/stage67_kappa_precision_path_2026.py and mi_kappa_error_budget_unlock_2026.py
are literally the kappa precision path and the error-budget unlock, and their answer is committed:
the unlock is the stellar M/L zero point to a few percent plus an absolute gas scale [OPEN as a
programme, SETTLED as an answer to this question]. Verdict: DEAD, answered.

**I475 — BTFR zero-point drift as an a0(z) signature.** HYP: the derived a0(z) drifts the BTFR
normalisation as a0(z)^(1/4), a redshift signature no constant-a0 MOND has. USES: N4+N5. DO:
compute the predicted BTFR zero-point offset between z = 0 and z = 1 from the law, and compare
with the published high-z BTFR scatter divided by sqrt(N). DATA: real_research/data/a0_of_z.csv,
real_research/data/kross_harrison2017.csv. PASS: the predicted offset exceeds scatter/sqrt(N).
KILL: it does not -- report the N required, so the test is priced rather than abandoned.
PRIOR: "the high-z BTFR as an independent test of a0(z)" is answered NO — it is GAS-CONFOUNDED:
btfr_evolution_confound.py, and nbody_2026/stage60_btfr_discriminator_2026.py with its two
adversarial referee lanes [SETTLED]. Verdict: DEAD, answered. (The un-confounded high-z channel,
the RAR normalisation rather than the BTFR intercept, is retained as I473.)

**I482 — Planet-by-planet precession from the legality-forced saturation.** HYP: legality forces
U -> s, so every planet inherits a constant sunward anomaly s a0; at s = 1.27e-5 the predicted
precessions are specific numbers, tightest for the outer planets. USES: N1+N6. DO: compute
delta-omega per century for Mercury through Saturn at s = 1.27e-5 and at the RAR-required
s = 0.219, and compare with INPOP/EPM bounds. DATA:
real_research/reviews/a0_local_ephemeris_2026.py. PASS: at least one planet is within 10x of its
bound -- a near-term target. KILL: all more than 1000x below -- state the improvement factor.
PRIOR: circular by construction — s <= 1.27e-5 IS the inversion of those bounds, so evaluating at
s = 1.27e-5 must return "within 10x" for the binding planet and the PASS branch fires no matter
what the physics is (the "null by construction" kill-mode from the qwen harvest). The bounds are
already verified from primary sources, not quoted: Sereno & Jetzer 2006 Table 1 (Pitjeva EPM2004)
inverted through their own Eq.(9) gives delta-A_R <= 3.66e-14 m/s^2 (Earth, 2 sigma) and 3.72e-14
(Mars); bare a0/2 is 1278-1279x over canonical, 1544x alt — mi_alpha1_solar_system_2026.py,
mi_efe_escape_and_ch23_withdrawn_2026.py [SETTLED]. Verdict: DEAD, answered + null by construction.

**I493 — S8 from a late-turning-on MOND.** HYP: the derived a0(z), by turning MOND on late,
predicts an S8 offset from LCDM at a level KiDS/DES can see -- a signature no constant-a0 theory
produces. USES: N2+N4. DO: run CLASS with and without the a0(z) modification of the growth
equation, compute sigma_8 and S8 in both, and record the sign of the shift. DATA: CLASS,
real_research/data/a0_of_z.csv. PASS: the S8 difference exceeds 0.02 -- a live discriminator.
KILL: below 0.005 -- S8 is neutral for this framework, and record that it must not be cited as
support in either direction.
PRIOR: answered NO. S8/sigma_8 is NEUTRAL-BY-THEOREM for this framework —
nbody_2026/stage23_s8_confrontation_2026.py and project_sigma8_evolving_a0.py (which is
specifically sigma_8 with an EVOLVING a0) [SETTLED]. Verdict: DEAD, answered. (The SHAPE of
f sigma_8(z) below z = 0.5, which the amplitude test does not cover, is retained as I494 and
cites both scripts in its DO:.)

## Cut from IDEAS_201_300.md (alternative relativistic homes, I201-I300)

Assessed 2026-08-17 against PRIOR_WORK_INDEX.md. Each entry below was DEAD: the question is
already answered, or it re-derives a RETRACTED claim, or it belongs to the shared-number
coincidence class that produced 95 honest deaths in the qwen autoloop. Their ids were reused
for backfills drawing on seeded angles S1-S4, so I201-I300 stays contiguous at 100.

**I205 — Does the c14 ceiling collide with the Q0 pin.** HYP: LLR's |alpha1| < 1e-4 gives alpha1 = -4 c14
at c13 = 0 and hence a c14 ceiling; independently Q0 in 0.0024-0.0146 Mpc^-1 sets the aether-scalar
mixing scale, and the two can be inconsistent. USES: N7+N2. DO: reduce the Foster-Jacobson alpha1 at c3 =
-c1 with sympy, invert for c14; then express the mixing F_YQ scale implied by Q0's two edges and ask
whether it exceeds the c14 ceiling. DATA: analytic -- no data needed. PASS: consistent at both Q0 edges
-> report the surviving c14 window. KILL: the low Q0 edge (0.0024) forces c14 above the LLR ceiling -- a
real tension.
PRIOR: the LLR route is RETRACTED. "alpha1 = -4K_B => K_B < 2.5e-5" was WITHDRAWN AS A BOUND together
with stage73's "EMPTY WINDOW" (stage74_ppn_fork_adjudicated_2026.py, 24/24; alpha2_{regulated_limit,
linearised_solve,wellposedness,literature_forensics}_2026.py): Foster & Jacobson remove c123 = 0 from the
domain BEFORE deriving the formula, alpha2 is a simple pole with nonzero residue, and at c123 = 0 the
static longitudinal operator changes TYPE. Do not quote K_B < 2.5e-5 and do not quote alpha1 = 0 either.
IN FORCE: K_B in [2.1e-4, 2) on no-ghost, [2.1e-4, 0.25] with BBN. Verdict: DEAD (would re-derive a
retracted bound). The live version of this question is I204/I255 in the rewritten file.

**I206 — Can GW170817's c13 bound reach the DBI wall.** HYP: c_T^2 = 1/(1-c13) caps |c13| at ~1e-15, and
the question is whether that is enough to shift the wall radius |Q-Q0| = Lambda_D where -K -> 0 and a0 ->
0. USES: N3+N7. DO: write the wall condition with the aether mixing kept; compute d(Lambda_D/Q0)/d(c13)
at c13 = 0; ask what |c13| would move the wall by 1%; compare to 1e-15. DATA: analytic -- no data needed.
PASS: required |c13| >> 1e-15 -> the wall is GW-safe, a clean structural statement. KILL: 1e-15 already
moves the wall by >1%.
PRIOR: premise-existence failure. c_T = 1 is EXACT in this completion as an IDENTITY, because c13 = 0 for
every K_B (RETRACTIONS.md §7; prep_2026/gw170817_check/*). There is no c13 to bound, so the derivative
d(Lambda_D/Q0)/d(c13) is evaluated at a point the theory never leaves. Verdict: DEAD. The wall's real
location is now asked in the rewritten I234/I254 (seeded angle S3).

**I207 — Is the single-valuedness criterion independent of c13.** HYP: the condition that forces U(y)
strictly increasing comes from F(Y,Q)'s inversion, not from the tensor sector, so c13 cannot buy any of
the 13,600x gap. USES: N6+N2. DO: redo the scalar-sector kinetic-matrix positivity with c13 general and
the promotion's a0(Q) in place; check whether dU/dy > 0 acquires any c13 dependence at all. DATA:
analytic -- no data needed. PASS: manifestly c13-free -> the tensor sector is not a route to R1, closed
with a reason. KILL: c13 enters -- report the modified condition and the negative dU/dy it permits.
PRIOR: same identity as I206 — c13 = 0 for every K_B, so the PASS branch is true by construction and the
KILL branch is unreachable. Separately, the legality condition is a scalar-sector statement already
derived and committed (typeII_legality_independent_2026.py, aqual_efe_a0line_kernel_2026.py). Verdict:
DEAD. Its useful residue — redoing legality with a0 promoted to a FIELD — is the rewritten I205 (S4).

**I212 — BBN's G bound where a0(z) has already switched MOND off.** HYP: at z ~ 1e9 the derived law gives
a0(z)/a0(0) << 0.0060, so the aether's G_cosmo/G_N = 2/(2-c14) is the ONLY surviving modification at BBN
and the |G_c/G_N - 1| < 0.13 bound applies cleanly to c14. USES: N4+N1. DO: evaluate a0(nu)/a0(0) at nu =
nu0 (1+z)^3 for z = 1e9 with nu0 = 2.36e-6; confirm the MOND term is negligible; then invert the BBN
bound for c14 and compare to the LLR ceiling. DATA: real_research/data/a0_of_z.csv. PASS: MOND is off by
>1e3 at BBN and LLR is the binding constraint -> record which binds. KILL: a0(z) is NOT small at BBN --
re-derive.
PRIOR: both halves are settled. MOND is off at recombination already (a0(1090)/a0(0) = 6.0e-3,
stage17_a0z_from_the_action_2026.py), a fortiori at BBN; and the BBN leg of the K_B window is already in
force as K_B <~ 0.25, with the full in-force range K_B in [2.1e-4, 0.25] (RETRACTIONS.md §7). The
comparison target — the LLR ceiling — is retracted (see I205 above), so the PASS branch asks which of two
bounds binds when one of them no longer exists. Verdict: DEAD.

**I219 — Proca mass a0/c^2 against the wall length Lambda_D/Q0.** HYP: a vector mass set by a0 gives a
Compton range c^2/a0 ~ 1e27 m, which is far larger than the wall scale implied by Q0, so the mass term
and the brane structure cannot be the same physics. USES: N1+N7. DO: compute c^2/a0 for both footings
(9.3619e-11, 1.1279e-10); convert Q0 = 0.0024 and 0.0146 Mpc^-1 to lengths; take the ratios; compare both
to 2.2 Mpc, the outer edge of the lensing RAR. DATA: prep_2026/kids_rar/kids_rar_lambda.py for the outer
radius. PASS: the ranges are separated by >1e3 -> a mass term cannot shape the RAR nor be the wall. KILL:
the c^2/a0 range lands within a factor 3 of Lambda_D/Q0 -- a coincidence worth naming.
PRIOR: the shared-number coincidence class. The qwen autoloop spent 95 sessions on "one dimensionless
number does two unrelated jobs" and produced 95 honest deaths, with four named kill-modes including
tolerance-width null-by-construction (FINDINGS_HARVEST_2026-08-16.md; LEDGER.md rows 0001-0094). The
arithmetic here is also already known: c^2/a0 = 9.6e26 m = 3.1e4 Mpc against a wall scale of order
(Lambda_D/Q0)/Q0 <= 3.1e-6 x 420 Mpc, i.e. separated by >1e7 with no free parameter to close it.
Verdict: DEAD. The id now carries the S2 backfill (dark energy is inhomogeneous by the a0 factor squared).

**I234 — Pin the Galileon Lambda^3 twice: by a0 and by the DBI wall.** HYP: demanding the Galileon
crossover happen at a0 = kappa c sqrt(G rho_Lambda) fixes Lambda^3, and placing the screening
boundary at the wall scale Lambda_D/Q0 is a second condition -- if one Lambda does both, brane and
screening are one structure. USES: N1+N3+N7. DO: solve for Lambda from the crossover at a0 (both
footings), then for the Lambda putting r_V at Lambda_D/Q0 at Q0 = 0.0024 and 0.0146 Mpc^-1; take the
ratio of the two Lambdas. DATA: analytic. PASS: the ratio is within a factor of 3 for some allowed
Q0 -> report it. KILL: off by >100x at both Q0 edges -- the coincidence does not exist; close it.
PRIOR: same coincidence class as I219 (LEDGER.md rows 0001-0094; FINDINGS_HARVEST_2026-08-16.md). The
Vainshtein radius is mass-dependent while the wall scale is not, so "one Lambda does both" cannot hold
for more than one object even if it holds for one — a tolerance-width hit by construction. Verdict: DEAD.
The id now carries the S3 backfill (where the wall actually is, for real objects, at both Q0 edges).

**I254 — Does massive gravity's Lambda_3 coincide with Lambda_D/Q0.** HYP: dRGT's strong- coupling scale
Lambda_3 = (m^2 M_pl)^(1/3) with m ~ H0 gives a length that could equal the brane's wall scale
Lambda_D/Q0, which would make the graviton mass and the wall one structure. USES: N7+N3. DO: compute
1/Lambda_3 in metres for m = H0; convert Q0 = 0.0024 and 0.0146 Mpc^-1 to lengths and multiply by the
growth-allowed Lambda_D/Q0 range; take the ratios. DATA: analytic -- no data needed. PASS: within a
factor of 3 at some allowed Lambda_D/Q0 -> a coincidence worth naming and testing further. KILL: off by
>100x at both edges.
PRIOR: same coincidence class (LEDGER.md rows 0001-0094). Also degenerate with I219 and I234 as a
computation, violating C2 within the file. Verdict: DEAD. The id now carries the S3 backfill (is there an
a0 = 0 shell inside a halo, and would SPARC see it) — which turns the wall into a falsifiable prediction
instead of a numerical coincidence.

**I269 — Is a0 a scalaron mass in disguise, and can it be the brane's M.** HYP: setting the
Starobinsky scalaron mass 1/sqrt(6 alpha) equal to a0/c^2 gives an alpha, which must also
reproduce M^4 = rho_Lambda c^2 if the two are the same physics. USES: N1+N3. DO: compute c^2/a0
for both footings, set it to sqrt(6 alpha) for alpha, check it against laboratory and
solar-system bounds, and compare the implied vacuum energy to rho_Lambda c^2. DATA: analytic.
PASS: alpha allowed AND the vacuum energy within a factor 3 of rho_Lambda c^2. KILL: excluded
by >10 orders -- closes the "a0 is a scalaron mass" numerology permanently.
PRIOR: the entry names itself numerology in its own KILL line, and the class is settled dead 95 times
over (LEDGER.md rows 0001-0094; FINDINGS_HARVEST_2026-08-16.md kill-modes). It also duplicates I219's
computation (both reduce to c^2/a0 versus a second length). Verdict: DEAD. The id now carries the S1
backfill (does a0 LAG the density it tracks, and which homes can lag at all) — which uses a0's derived
mass rather than equating it to somebody else's.

**I275 — Is Mannheim's gamma0 c^2/2 the same number as kappa c sqrt(G rho_Lambda).** HYP: the published
universal gamma0 ~ 3.06e-30 cm^-1 corresponds to an acceleration that should equal a0 if both frameworks
describe one scale, and the implied kappa is then a second measurement of Carl's coefficient. USES:
N1+N5. DO: compute gamma0 c^2/2 in m/s^2; take the ratio to 9.3619e-11 and to 1.1279e-10; invert to the
kappa that conformal gravity would imply and compare to the measured 0.529 +/- 0.034. DATA: analytic --
no data needed. PASS: the implied kappa is within 2 sigma -- an independent anchor worth naming. KILL:
off by >10x -- report it and close the coincidence.
PRIOR: "a second measurement of kappa" from another theory's fitted constant is exactly the estimator
failure the corpus has already retracted twice — kappa is MEASURED at 0.529 +/- 0.034 with at least four
candidates inside 2 sigma, and a +/-7.8% window is crowded (stage66_kappa_rational_evidence_2026.py;
kappa_h0_convention_audit_2026.py; harvest H0023/H0027/H0086 on window-crowding). Conformal gravity's
gamma0 is itself fitted to the same rotation curves, so the comparison is not independent. Verdict: DEAD.
The id now carries the highest-value S4 backfill (what replaces the 13,600x number if U is not a fixed
curve). Note I274 retains the real conformal-gravity test — a like-for-like RAR scatter with Upsilon
refit on both sides.

**I286 — Verlinde's cH0/6 against kappa c sqrt(G rho_Lambda).** HYP: emergent gravity's a0-analogue cH0/6
differs from Carl's normalisation by a pure number computable from Omega_Lambda alone, so the comparison
is a closed-form check on kappa. USES: N1+N2. DO: compute cH0/6 and kappa c sqrt(G rho_Lambda) for both
footings; take the ratio; express it in terms of sqrt(Omega_Lambda); then invert to the kappa Verlinde
would imply and compare to 0.529 +/- 0.034. DATA: analytic -- no data needed. PASS: implied kappa within
2 sigma -> an independent (heuristic) anchor for R3. KILL: differs by >1.5x -- report the number and move
on.
PRIOR: settled. Every published dS-thermodynamic / holographic-screen route to the MOND coefficient
forces a value != 1/2 or forces none, and the table is COMPLETE (qwen LEDGER t001;
established_paths_to_mond.py, project_routes_to_sign.py, project_forcing_the_coefficient.py). The
specific arithmetic — cH0/6 versus kappa c sqrt(G rho_Lambda) reducing to a sqrt(Omega_Lambda) factor —
is a rewriting of the fit, the same defect as the crossover master formula kappa^2 = 8 pi eps_tot
(RETRACTED, stage43). Verdict: DEAD. The id now carries the S2 backfill (does inhomogeneous rho_Lambda
change the EFE non-relief number). Note I287 retains the non-numerological Verlinde question: does an
elastic medium saturate the way N6 says a gradient theory must.

---

## Range I001-I100 (IDEAS.md) — 14 cut 2026-08-17

**I027 — Is Lambda_D or Q_0 a de Sitter length in disguise?** HYP: the theory fixes Q_0 and
Lambda_D, and kappa = 1/2 may be a ratio of one of those to the de Sitter scale. USES: N1+N3+N7.
DO: convert sqrt(Lambda/3) and H_0/c to Mpc^-1, then form Q_0/(H_0/c), Q_0/sqrt(Lambda/3) and
Lambda_D/Q_0 across the pinned range Q_0 = 0.0024-0.0146 Mpc^-1; look for 1/2, 2 or 1/(2 pi).
DATA: analytic. PASS: one ratio lands on a simple number across the WHOLE pinned range, not just
one end. KILL: none does. IMPACT: would derive kappa from the brane's own scales.
PRIOR: two independent kills. (1) Failure mode "tolerance-width null-by-construction" from
FINDINGS_HARVEST_2026-08-16.md — three ratios x three targets across a factor-6 pinned range;
and the PASS as written is unachievable by construction, since Q_0/(H_0/c) varies by 6x across
the pin and cannot be constant. (2) "Pure horizon-geometry ratios are EXCLUDED as a route to
kappa" [NARROWED, qwen LEDGER t009 + stage65 PART B] already covers the monomial ratios this
enumerates. See also the 95-session qwen autoloop, all of which was "one shared dimensionless
number does two unrelated jobs" and produced 95 honest deaths (LEDGER.md rows 0001-0094).

**I032 — kappa from the BTFR zero point alone.** HYP: V^4 = G M a0 gives kappa with no RAR fit
at all. USES: N1+N5. DO: fit log V_flat against log M_bar on SPARC with the slope fixed at 1/4,
read the normalisation, invert for a0 and then kappa, and propagate the gas-scale and distance
errors. DATA: `real_research/data/sparc_master_clean.csv`. PASS: an independent kappa with sigma
< 0.08. KILL: fully degenerate with the assumed Upsilon. IMPACT: a second independent number on
the same coefficient.
PRIOR: DONE. kappa from the BTFR is one of the two committed estimators: 0.465 +/- 0.076 (BTFR)
vs 0.551 +/- 0.043 (distance-free), combined 0.529 +/- 0.034 published / 0.547 +/- 0.034 on the
Planck-consistent rescale. [SETTLED] (RETRACTIONS.md; mi_btfr_intercept_kappa_door_2026.py,
btfr_honest.py). The PASS threshold sigma < 0.08 is already met and the answer is on record.

**I033 — Map kappa(H0) and show a0 itself does not depend on H0.** HYP: a0 = c^2 sqrt(Lambda/32
pi) contains no H0, but the MEASURED kappa does, through SPARC distances. USES: N1+N5. DO:
rescale all SPARC distances by 70/H0 for H0 = 67, 70, 74 km/s/Mpc, refit, and report kappa(H0)
with a stated slope d kappa / d H0. DATA: `real_research/data/sparc_master_clean.csv`. PASS: a
clean monotone map. KILL: nonlinear or unstable. IMPACT: turns the Hubble tension into a stated
systematic on kappa.
PRIOR: DONE and sharper than this. `kappa_h0_convention_audit_2026.py` (24/24): kappa is
H0-CONVENTION-EXPOSED with kappa proportional to h^(2 q_eff - p), H0-invariant only at
q_eff = 0.500 or 0.730, and neither committed estimator sits there; a Planck-consistent rescale
moves a0 by +6.5-7.3%, which is 4.0x the 1.84% statistical error. Standing rule: always quote
kappa with its H0. [SETTLED] Explicitly NOT a direction claim.

**I034 — Is kappa the same on both footings?** HYP: canonical (rho_DE, a0 = 9.3619e-11) and alt
(rho_total, a0 = 1.1279e-10 m s^-2) should give the SAME kappa if the coefficient is physical.
USES: N1+N5. DO: measure kappa on each footing with identical cuts and identical pipeline, and
report the difference and its significance. DATA: `real_research/rar_framework_a0_mlfit.py`.
PASS: consistent within 1 sigma. KILL: differ by >3 sigma. IMPACT: a footing-dependent kappa
would mean the coincidence is chosen rather than measured.
PRIOR: NULL BY CONSTRUCTION. The two footings differ by the DEFINITION of rho in
a0 = kappa c sqrt(G rho) (rho_DE vs rho_total), so a single measured a0 divided by two different
sqrt(G rho) necessarily gives two different kappa in the fixed ratio 1.2048. That footing-fork
ratio is on the qwen dead-numbers list (LEDGER rows 0084, 0087, 0090). The PASS branch is
unreachable and the KILL branch is arithmetic, so the idea has no discriminating power. The live
version of this question — which footing the PROMOTION can host structurally — survives as I089.

**I035 — kappa from clusters, with the core suppression included.** HYP: inverting the cluster
eta requirement gives a third kappa, but only if a0 is evaluated at the cluster's OWN density
rather than a0(0). USES: N1+N4. DO: for the committed cluster profiles compute a0(rho) at R500
and in the core via the density law, invert the eta requirement for kappa, and report the spread
between the two radii. DATA: `real_research/data/kt2017_groups.tsv` or the committed cluster
table. PASS: kappa within 2 sigma of 0.529. KILL: off by >5x. IMPACT: supplies a cluster
mechanism, or shows clusters need new physics.
PRIOR: both branches are pre-determined, so no discriminating power. The committed cluster
requirement is eta(R500) = 1.865 canonical / 1.722 alt on the operative MS08 kernel (2.084/1.917
on the a0-line kernel) — i.e. clusters are off by about 2x, not within 2 sigma of 0.529 and not
off by 5x, so PASS is known-false and KILL is known-false. [SETTLED] (RETRACTIONS.md;
stage30_xcop_two_variable_fit_2026.py, clusters_eta_audit.py). Additionally the density-monotone
lever is structurally trapped: cluster cores are LESS dense than galaxy inners, so no
density-monotone a0 law boosts clusters without boosting galaxies more (STANDING.md §4). The
surviving live version is I035's replacement (kappa(cluster)/kappa(galaxy) as a ratio prediction).

**I036 — Calibrate the dust filters against the four dead candidates.** HYP: `dust_filters.py`
should independently reproduce the review's verdicts on all four; if it does not, the filter is
wrong and everything downstream is suspect. USES: N3+N7 (F1 is rho = Q_0 n -- an energy density
only in natural units, where Q_0 is mass-dimension 1; state the SI conversion. F3 is c_s^2 from
K''). DO: run `python qwen_38_experiment/dust_filters.py --explain`, write a spec JSON per
candidate from `real_research/reviews/second_field_catalog_2026.py`, screen each. DATA: those
two files. PASS: 4/4 agreement. KILL: any disagreement -- name the filter and the candidate.
IMPACT: validates or invalidates every dust verdict at once.
PRIOR: this calibration IS the committed D001 run. The four second-field candidates (k-essence,
ungated Proca, promotion-only, fixed-Lambda) were screened with a killing filter named per row
and all four are dead; `second_field_catalog_2026.py` is 47/47. [SETTLED] (qwen LEDGER D001/D002;
PRIOR_WORK_INDEX §3). Re-running a passing positive control is not a new result.

**I038 — Enumerate pressure sources NOT built from the conserved charge.** HYP: F1
(rho = Q_0 n identically) kills only support built FROM the charge; a source built from something
else may survive all five filters. USES: N3+N7. DO: write specs for a second condensate, a gauge
field, fermion degeneracy, gradient energy, and finite-T radiation, giving each its Gamma and its
gate variable; screen each with `dust_filters.py`. DATA: `qwen_38_experiment/dust_filters.py`.
PASS: any survivor of all five. KILL: all die, with the killing filter named per candidate.
IMPACT: a survivor frees the dust and reopens the galaxy non-claim.
PRIOR: the enumeration exists and is exactly this list. "The NON-charge-built pressure sources
enumerated (second condensate with its own charge, gauge field, fermion degeneracy,
vorticity/turbulent stress, non-local/gradient energy, finite-T radiation) with a killing filter
named per row." [SETTLED as a catalogue] (qwen LEDGER D002; dust_filters.py / D001 calibration).
Two reusable theorems came out of it and should be used instead of re-listing: at Gamma = 4/3 the
violation is calibration-INDEPENDENT at 1.16e3x the cap, and
r_x/R_supp = [M_bar/((pi^2/3) M_dust)]^(1/3) = 0.194 is fixed by the baryon-to-dust ratio alone.

**I040 — The DBI wall's diverging stiffness as a pressure source.** HYP: as the dust
concentrates, Q is driven toward |Q-Q_0| = Lambda_D where d^2K/dQ^2 diverges, giving a stiffness
that is geometric rather than built from the charge -- so F1 does not bite. USES: N3+N7. DO:
compute d^2K/dQ^2 for the DBI form near the wall, identify the effective Gamma of the resulting
P(rho), and screen that spec with `dust_filters.py`. DATA:
`qwen_38_experiment/dust_filters.py`. PASS: it survives all five filters. KILL: the effective
Gamma lands in the DEAD band, or F2 bites. IMPACT: the brane itself would halt the collapse that
falsifies the theory.
PRIOR: duplicate. I315 (IDEAS_301_400.md) is the same computation with the same tool ("write the
wall candidate as a JSON spec ... run `dust_filters.py --screen spec.json`"), and I302/I303/I309
in that file already set up its inputs (rho diverges as (1-u^2/Lam_D^2)^(-1/2) while p -> 0, w
goes monotonically to 0^-, and c_s^2 = gamma^(-2) VANISHES at the wall — so the wall does not
supply pressure). Violates C2 (uniqueness across all 500). Run I315.

**I049 — Integrate the collapse with a0(rho): does it halt at the wall?** HYP: as rho rises, nu
rises and a0 falls toward zero -- which IS the wall -- so the collapse may reach a fixed point
rather than a singularity. USES: N2+N3+N4. DO: integrate d rho/dt for a uniform sphere with
g = nu(y) g_bar and a0 = a0_0 [(1+nu0^2)/(1+nu^2)]^(1/4), and look for a stationary rho; check
its stability by perturbing. DATA: analytic + `nbody_2026/stage75_the_closed_theory_2026.py`
initial conditions. PASS: a stable stationary density below the Sgr A* bound. KILL: rho runs away
for every nu0 <= 2.36e-6. IMPACT: replaces the falsified black hole with a stable object.
PRIOR: duplicate. I320 (IDEAS_301_400.md) is the identical computation with a stronger analytic
frame: "write the collapse equation with a_0(rho) from I304/I319, show analytically that the
acceleration remains >= g_bar for all rho, and integrate one collapse to confirm no stall" — and
it already names the reason the answer is expected negative, namely that
g_obs^2 = g_bar^2 + a_0 g_bar has g_obs >= g_bar identically, so driving a_0 -> 0 removes the
enhancement but leaves Newtonian free-fall. Violates C2. Run I320.

**I057 — Early collapse under the falling-a0 law (JWST high-z abundances).** HYP: because
N4 makes a0 SMALLER at high z, the framework's collapse speed-up must DECLINE with z -- a
shape no constant-a0 MOND has. USES: N4+N5.
DO: compute the turnaround-epoch (not virial-epoch) collapse-time ratio t_MOND/t_Newt using
nu(y) = sqrt(1+1/y) with a0(z) from N4, at z = 6, 10, 15, 25; report the trend.
DATA: analytic. PASS: the ratio declines monotonically with z and stays above 1.1 at z=10.
KILL: the ratio is flat in z, or drops below 1 (collapse slower than Newtonian).
IMPACT: a distinctive high-z signature separating this from constant-a0 MOND.
PRIOR: DONE, and the numbers are already in the ledger: the framework's collapse is 1.34-1.96x
faster than Newtonian and a0(z) makes the speedup DECLINE with z — 2.03x at z=6 falling to 1.14x
at z=25, priced at TURNAROUND (2.3-5.1x), not at the virial radius (<=1.5x). [OPEN as a
discriminator, but the computation is committed] (stage24_cosmic_dawn_confrontation_2026.py,
stage25_cosmic_dawn_own_terms_2026.py, stage26_collapse_acceleration_own_terms_2026.py). This
DO reproduces exactly those four redshifts. The DUST version of the same question — a different
density history — survives as I048.

**I084 — Can a Galileon host the a0-line with Vainshtein instead of saturation?** HYP: a
cubic Galileon's Vainshtein radius could hide the solar-system anomaly while leaving the
galactic a0-line intact -- something the legal family cannot do. USES: N1+N5+N6. DO: normalise the cubic
coupling to reproduce U = sqrt(y^2+y) - y (not generic MOND) at a0 = 9.3619e-11 m s^-2 and
100 kpc, compute r_V, and check whether it exceeds 100 AU but stays inside 1 kpc. DATA: analytic.
PASS: r_V lands in that window AND the unscreened profile reproduces the a0-line to 5%.
KILL: it misses by more than a decade. IMPACT: an alternative relativistic home closing R1.
PRIOR: duplicate, twice over. I130 (IDEAS_101_200.md) inverts r_V(Sun) for Lambda_3 over exactly
the 100-7958 AU window and compares it with the brane's own tension scale
M = (rho_Lambda c^2)^(1/4) = 2.24e-3 eV; I135 refits the a0-line RAR with the Vainshtein
suppression applied and reports the scatter against 0.108 dex; I129 does the r_V ~ M^(1/3) vs
sqrt(GM/a0) ~ M^(1/2) crossover. Violates C2. Run I129/I130/I135.

**I085 — Does Vainshtein screening evade the monotone-U theorem?** HYP: N6 forbids
non-monotone U for algebraic kernels; Vainshtein screening is not algebraic in Y, so it may
sidestep the theorem entirely rather than violate it. USES: N6+N5.
DO: write the screened solution as an effective U(y) including the second-derivative term and
test whether the effective U is monotone while still turning Newtonian at small r.
DATA: analytic. PASS: monotone AND Newtonian at 1 AU. KILL: monotonicity is broken again.
IMPACT: names the one loophole in the legality theorem, or shuts it.
PRIOR: duplicate. I132 (IDEAS_101_200.md) is the same test with an explicit scan range: "solve
the cubic-Galileon spherical algebraic equation, form U(y) = (nu-1) y with the a0-line as the
unscreened limit, and scan dU/dy over y in [1e-3, 1e9]"; and I137 in the same file asks the
sharper version (the two-branch Vainshtein solution IS the N6 illegality, via the discriminant
zero). Violates C2. Run I132, then I137.

**I087 — Is Verlinde's relation literally the a0-line with a different kappa?** HYP: emergent
gravity's g_D^2 ~ a_M g_B/6 has the SAME algebraic form as g_obs^2 - g_bar^2 = a0 g_bar, so
the two theories differ only in the constant. USES: N5+N1.
DO: put Verlinde's relation in the a0-line's variables, read off the implied a0 in m/s^2 and
the implied kappa in a0 = kappa c sqrt(G rho_Lambda), and compare to 0.529 +/- 0.034.
DATA: analytic. PASS: Verlinde's implied kappa lies within 2 sigma of the measured value.
KILL: the forms differ (not just the constant) or kappa is off by > 3x.
IMPACT: an independent theory arriving at the same relation would bear on R3.
PRIOR: duplicate of I286 (IDEAS_201_300.md), which stated the same arithmetic more precisely
(cH0/6 versus kappa c sqrt(G rho_Lambda), ratio expressed in sqrt(Omega_Lambda), inverted to an
implied kappa) — and I286 has ITSELF been cut as DEAD in this file, because the arithmetic is a
rewriting of the fit, the same defect as the crossover master formula kappa^2 = 8 pi eps_tot
[RETRACTED, stage43], and because every published dS-thermodynamic route forces a coefficient
!= 1/2 or forces none [SETTLED, qwen LEDGER t001]. So this is dead twice: C2 and C6. The
non-numerological Verlinde question survives as I287 (does an elastic medium saturate the way N6
says a gradient theory must) — run that instead.

**I094 — Lambda_D from the RAR ceiling via the rapidity identification.** HYP: with
x = (Q-Q_0)/Lambda_D = nu/sqrt(1+nu^2), the RAR bound nu0 <= 2.36e-6 bounds the present-day
excursion in units of Lambda_D, hence Lambda_D given Q_0. USES: N3+N4+N7. DO: compute
x_0 = nu0/sqrt(1+nu0^2), then Lambda_D = |Q-Q_0|/x_0 -- the excursion is NOT measured, so take
|Q-Q_0| = f Q_0 for f = 0.01, 0.1, 1 and name f as the assumption -- and use the pinned Q_0 range
to bracket Lambda_D in Mpc^-1. DATA: analytic. PASS: a finite Lambda_D interval consistent with
the growth/forest bound. KILL: it demands Lambda_D >> Q_0.
IMPACT: pins the last free brane scale, or retires the wall.
PRIOR: duplicate, and the sibling version is better founded. I306 (IDEAS_301_400.md) reaches the
same target — mapping nu_0 onto Lam_D/Q_0 — without this idea's unmeasured free assumption
|Q-Q_0| = f Q_0: it identifies nu = u/Lam_D so that nu_0 = rho_dm,0/rho_wall with rho_wall from
I301, solves for Lam_D/Q_0 at nu_0 = 2.36e-6, and confronts it with the growth + Lyman-alpha
bound. This idea's f is exactly the degree of freedom I306 eliminates. Violates C2. Run I306
(and I301 before it).

---

## Range I101-I200 (screening mechanisms)

Twelve cut. Their ids were reused for backfills drawing on seeded angles S1-S4 (the a0 field
equation, its propagation speed and boundary condition, the wall as a locus, legality re-derived
with a0 a field, and inhomogeneous dark energy), so the range remains contiguous at 100.

**I110 — Does the Sun source a Q excursion of order Lambda_D at all?** HYP: delta Q sourced by
one solar mass is many orders below the pinned Lambda_D, so the wall is never approached and
section A's whole premise is dead. USES: N7+N3. DO: integrate the linearised Q equation for
M_sun out to 1 AU, express delta Q in Mpc^-1, and compare with Lambda_D ~ Q_0 ~ 0.0024–0.0146
Mpc^-1. DATA: analytic — no data needed. PASS: delta Q / Lambda_D > 0.1. PARTIAL EXPECTED: an
order-of-magnitude answer suffices. KILL: delta Q / Lambda_D < 1e-3 — record the premise as dead.
PRIOR: this is verbatim the computation already issued as I005 in `IDEAS.md` ("Does the Sun drive
Q to the DBI wall?", same delta-Q vs Lambda_D comparison at 1 AU and 10 kpc), and it is strictly
contained in this file's own I101, whose r_wall solve cannot be done without it. C2 collision on
both counts. Verdict: DEAD as a separate session; the number will be produced by I005/I101.

**I115 — Evaluate the local reading of N4 at every relevant density.** HYP: a0(rho) computed
from nu = nu_0 rho/rho_0 with nu_0 = 2.36e-6 gives at most a factor ~3 suppression in the
interplanetary medium, nowhere near the 13,600x gap. USES: N4+N2. DO: tabulate a0/a0(0) =
(1+nu^2)^(-1/4) for interplanetary 8e-21, ISM 1.7e-21, mid-plane 1e-20, solar body 1400 kg/m^3;
check the header's quoted 0.355 / 0.716 / 0.318 / 8.5e-13. DATA:
nbody_2026/stage76_nu0_recombination_pin_2026.py. PASS: some environment gives >100x. KILL: the
ambient values cluster within 3x of each other — the local reading cannot separate Sun from disc.
PRIOR: all four numbers it asks for are PRINTED IN THE HEADER OF THE SAME FILE, so the session
would re-derive its own instructions; the underlying computation is committed as
`real_research/reviews/a0_local_ephemeris_2026.py` (the alpha=1 liability recomputed with a0
LOCAL) [SETTLED] and its verdict is already banked in `nbody_2026/stage59_local_a0_verdict_2026.py`
(2-4% suppression inside halos, 13x only at 1e6 rho_dm0). Verdict: DEAD, answer pre-stated.

**I119 — Predicted RAR scatter from real density variation alone.** HYP: because a0 depends on
local density, SPARC galaxies spanning a decade in mid-plane density must show a corresponding
a0 spread, and the observed 0.108 dex already bounds it. USES: N4+N5. DO: compute each SPARC
galaxy's mean disc surface density, map to nu via nu_0 = 2.36e-6, predict the per-galaxy a0
offset, and compare with the measured galaxy-to-galaxy RAR offsets. DATA:
real_research/data/SPARC_Lelli2016c.mrt plus real_research/rar_framework_a0_mlfit.py. PASS: the
predicted spread is below the observed scatter. KILL: it exceeds it — re-derive nu_0's bound.
PRIOR: "the RAR scatter as a QUANTITATIVE upper bound on how much a0 may vary" is committed and
[SETTLED] — `project_rar_bounds_rho_uniformity.py`, `rar_tightness_intrinsic.py`,
`project13_a0_universality.py` (the Rodrigues 2018 per-galaxy universality challenge), plus the
direct null of `project_sparc_a0_vs_density_direct.py`. The framework-form version (fit nu_0
itself to the RAR) survives as I120, which now carries the pointer. Verdict: DEAD, superseded by
I120.

**I125 — The ephemeris anomaly with a0 evaluated locally, not cosmologically.** HYP: replacing
a0 by a0(rho_interplanetary) = 0.355 a0(0) in the constant sunward anomaly s·a0 relaxes the
precession bound on s by exactly 1/0.355. USES: N4+N1. DO: rerun the precession calculation with
the rescaled a0 and report the new bound on s; compare with 1.27e-5. DATA:
real_research/reviews/a0_local_ephemeris_2026.py. PASS: the new bound exceeds 1.27e-5 by >3x.
KILL: the relief is under 3x — record that N4 buys 2.8x of a 13,600x gap and no more.
PRIOR: this is exactly the committed script it cites — `a0_local_ephemeris_2026.py`, "the alpha=1
ephemeris liability recomputed with a0 LOCAL" [SETTLED as a computation] (PRIOR_WORK_INDEX §8).
It is also issued as I002 in `IDEAS.md` ("The 1 AU anomaly is s*a0(local), not s*a0(cosmic)"),
which divides the 13,600-17,300x gap by the same factor. Its own KILL text states the expected
answer (2.8x). Verdict: DEAD, twice-covered and self-answering.

**I135 — Vainshtein plus the a0-line: is the RAR still 0.108 dex?** HYP: a Galileon that screens
the Sun leaves the a0-line fit within its measured scatter. USES: N5+N1. DO: apply the
Vainshtein suppression at each SPARC point's radius and mass, refit Upsilon against
g_obs^2 = g_bar^2 + a0 g_bar with a0 = 9.3619e-11 held, and report the scatter. DATA:
ai_slop/website/public/data/rar_real_sparc.json plus real_research/rar_framework_a0_mlfit.py.
PASS: <= 0.13 dex. KILL: > 0.15 dex, or a visible mass-dependent split.
PRIOR: the DO would read identically for generic MOND (apply a multiplicative suppression, refit
Upsilon, quote the scatter) and is the same computation as this file's I104, I162 and I187 — a
four-way C2 collision. The generic half is committed: the four-kernel shape systematic on the full
SPARC RAR is 26.3% and the best total error is 8.49% (`mi_routeA_shape_invariant_a0_2026.py`,
`mi_shape_systematic_mechanism_2026.py`) [SETTLED], with the baseline 0.108 dex at Upsilon = 0.70
from `real_research/rar_framework_a0_mlfit.py`. The mass-dependent split — the part that is
actually diagnostic of Vainshtein — survives as I136. Verdict: DEAD, generic + superseded by I136.

**I145 — Does the screening branch turn on cosmologically and break w = −1?** HYP: the large-Y
branch activates on the background and destroys the exact w = −1 that the brane minimum gives.
USES: N3+N2. DO: evaluate the background Y from z = 1100 to 0, compare with the screening scale,
and if it crosses, report max|w(z)+1|. DATA: nbody_2026/stage75_the_closed_theory_2026.py plus
real_research/data/a0_of_z.csv. PASS: the background stays below 0.01 of the screening scale at
all z. KILL: it crosses — the CMB fit then sits on the screened branch, which is disqualifying.
PRIOR: "add a term, evolve the background, report max|w+1|" is issued three more times in this
same file (I131 Galileon, I156 potential, I181 aether) — C2. The background side is settled:
w = −1 is exact at the minimum and w = −1 + O(nu_0^2) with a0(z), offset 1e-10–1e-8
(`nbody_2026/stage17_a0z_from_the_action_2026.py`) [SETTLED], and the CLASS re-run with the
derived law gives 0.01 sigma vs cosmic variance (`stage19_class_rerun_derived_law_2026.py`).
Verdict: DEAD as a fourth copy; I131 carries the Galileon version with the a0 shift attached.

**I151 — Chameleon mass variation versus the nu_0 cap.** HYP: the chameleon mass ratio needed
between solar and ISM environments implies an a0 variation with local density exceeding nu_0 =
2.36e-6. USES: N4+N2. DO: translate the required mass ratio into a fractional a0 shift through
a0^2 = kappa^2 G(−K), then compare with the cap. DATA:
nbody_2026/stage76_nu0_recombination_pin_2026.py. PASS: within the cap. KILL: it exceeds — quote
the factor; this is the cleanest chameleon exclusion available and it uses only Carl's own numbers.
PRIOR: identical computation to this file's I117 (nu_0 cap -> maximum achievable screening factor)
and I170 (the same cap applied to every environment-dependent coupling), with only the driver
relabelled — C2. The general statement is the one worth a session; the chameleon is one instance
of it. Verdict: DEAD, subsumed by I117 + I170.

**I158 — Is a chameleon EXCLUDED by kappa's measured stability?** HYP: kappa = 0.529 ± 0.034 is
measured in environments spanning several decades in density, and a chameleon that screens the
Sun would make kappa environment-dependent at more than the 6.4% measurement error. USES: N1+N4.
DO: express the effective kappa as a function of the chameleon suppression, evaluate across the
BTFR sample's density range, and compare the induced spread with 0.034. DATA:
real_research/data/SPARC_table.txt. PASS: the induced spread is below 0.034. KILL: above it —
this converts the kappa measurement into a screening bound, which is new; quote it.
PRIOR: kappa is a0's normalisation, so "environment-dependent kappa" IS "environment-dependent
a0", and the per-galaxy a0 universality test on real SPARC is committed and null —
`project13_a0_universality.py`, `sparc_anchor_universality.py`, `rar_tightness_intrinsic.py`
[SETTLED]; the environmental version is excluded at 10.5 sigma
(`sparc_environmental_a0_test.py`). The kappa error budget itself is closed out in
`mi_kappa_error_budget_unlock_2026.py`. Verdict: DEAD, the a0-universality null relabelled.

**I172 — Environment split on SPARC: beta(rho_env) versus a0(rho_local).** HYP: an
environment-dependent coupling correlates the RAR offset with LARGE-scale environment; N4
correlates it with the galaxy's OWN density. USES: N4+N5. DO: cross-match SPARC with 2MRS for a
local-density proxy, split at the median, fit RAR offsets against both the environmental and the
internal density. DATA: real_research/data/SPARC_Lelli2016c.mrt plus
real_research/data/2mrs_catalog.csv. PASS: exactly one correlation is significant — report which.
KILL: both null at 1 sigma; quote the bounds on d(ln beta)/d(ln rho_env) and on nu_0.
PRIOR: done, on this exact data, with a null: `project_sparc_a0_vs_cosmicweb.py` (per-galaxy a0
against the large-scale cosmic web) and `project_sparc_a0_vs_density_direct.py`, with the
confound priced in `prep_2026/cosmicweb_a0/environment_power_confound.py`; the matched catalogue
is already committed as `real_research/data/sparc_cosmicweb_match.csv` and
`sparc_a0_environment_table.csv` [SETTLED, null]. Verdict: DEAD, re-run of a committed null.

**I184 — A mass term screens the wrong side, and the brane already has one.** HYP: expanding
K(Q) about Q_0 already gives m^2 = M^4/Lambda_D^2, and Yukawa suppression at r > 1/m kills
galaxies while leaving the solar system intact — the wrong sign. USES: N7+N3. DO: compute 1/m
from the pinned Q_0 and Lambda_D band, state where it falls relative to 10 kpc and 1 AU, and
show quantitatively that no m suppresses at small r. DATA: analytic — no data needed. PASS: some
m suppresses at small r. KILL: none does — closes the mass-term route and prices the brane's own
mass term at the same time.
PRIOR: the same 1/m is computed by I006 in `IDEAS.md` ("The brane's stiffness sets a STATIC
screening length; compute it"), which additionally carries the unit chain through the kinetic
normalisation Z — C2. And the KILL branch is definitional, not empirical: a Yukawa factor
e^(-mr) suppresses at LARGE r for every positive m, so "no m suppresses at small r" is true by
inspection and has no discriminating power (the harvest failure mode of the same name).
Verdict: DEAD, duplicate + null by construction.

**I192 — Running kappa as screening, capped by nu_0.** HYP: kappa(rho) falling in dense regions
would screen the Sun, but since a0 = kappa c sqrt(G rho_Lambda), a kappa variation IS an a0
variation and nu_0 <= 2.36e-6 caps it. USES: N1+N4. DO: compute the kappa suppression needed for
s <= 1.27e-5 given s >= 0.219, translate into a fractional a0 change per unit local density, and
compare with the cap. DATA: nbody_2026/stage76_nu0_recombination_pin_2026.py. PASS: within the
cap. KILL: outside — the definitive statement that running kappa cannot rescue R1; quote the
factor and note it also bounds any environmental drift in the measured 0.529 ± 0.034.
PRIOR: its own HYP concedes that a kappa variation IS an a0 variation, so the computation is
identical to I117's (nu_0 cap -> maximum screening factor) with the symbol renamed — C2 against
I117 and I170. Separately, kappa is MEASURED not derived, 0.529 ± 0.034, and is
H0-convention-exposed (kappa ∝ h^(2q_eff−p)) — `kappa_h0_convention_audit_2026.py` 24/24,
`mi_kappa_error_budget_unlock_2026.py` [SETTLED]. Verdict: DEAD, I117 under another name.

**I198 — Was the solar system screened in the past, and does it matter?** HYP: because a0(nu)
declines toward high nu, the sunward anomaly s·a0 was smaller earlier, and the precession
accumulated over 4.5 Gyr is smaller than the constant-a0 estimate. USES: N4+N1. DO: integrate
the precession with a0(z) from the committed law over the last 4.5 Gyr and compare with the
constant-a0 result. DATA: real_research/data/a0_of_z.csv plus
real_research/reviews/a0_local_ephemeris_2026.py. PASS: the reduction exceeds 2x. KILL: below
1.2x — and state whether it is even relevant given that the ephemeris bound is present-epoch.
PRIOR: the a0(z) law is committed and settled — a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} exp(−1.5 wa
z/(1+z)), bump-then-decline (`a0z_desi_chains_propagation.py`, `desi_a0z_loop_CLOSED.py`), with
the derived-law version in `nbody_2026/stage17_a0z_from_the_action_2026.py` — and over 4.5 Gyr
(z <= 0.4) it moves a0 by well under the 13,600x in question. The idea's own KILL line concedes
the decisive point: the Sereno-Jetzer/Pitjeva bound is a PRESENT-EPOCH residual bound, so an
integrated history cannot relax it. Verdict: DEAD, no discriminating power.

---

## Second cut — final audit 2026-08-17 (cross-file duplicates and null-by-construction)

Twenty-three entries cut because another live idea already produces the same computation
(C2), or because the effect they test is O(nu_0^2) ~ 5.6e-12 at the RAR ceiling and could
never fire. Each id was refilled in place with a new idea, so every file still holds 100.
Text below is the entry exactly as it stood before the cut.

**I005 — Does the Sun drive Q to the DBI wall?** HYP: the brane has a wall at |Q-Q_0| = Lambda_D
where -K -> 0 and a0 -> 0; if the Sun's own charge excursion reaches it, the anomaly switches off
at 1 AU while galaxies stay near the minimum. USES: N3+N7+N2. DO: solve the static Q equation
Z grad^2 Q = -dK/dQ + (source) for a point mass with K = -M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2),
M^4 = rho_Lambda c^2; express delta-Q(r) in Mpc^-1 at r = 1 AU, 40 AU, 1 pc, 10 kpc; compare with
Lambda_D over Q_0 = 0.0024 and 0.0146 Mpc^-1 and Lambda_D/Q_0 in {2.3e-9, 1e-6, 1.5e-6, 3.1e-6}.
DATA: analytic (sympy). PASS: delta-Q/Lambda_D >= 1 at 1 AU AND <= 1e-2 at 10 kpc.
KILL: < 1e-3 at both. IMPACT: the wall would switch R1's anomaly off at no cost.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS.md) duplicates I101 (IDEAS_101_200.md), which solves the same static Q equation around the Sun and reports where |Q-Q_0| reaches Lambda_D; I101 is the version 21 other ideas cite, so it is the one kept. Violates C2.

**I049 — Can a collapsing dust core RADIATE a0-waves? (S1)** HYP: I036's equation makes a0 a
propagating field, so a time-dependent dust core is a source of a0 radiation, and that is an energy
loss channel the charge argument does not forbid (it removes ENERGY, not CHARGE). USES: N2+N3+N7.
DO: from the linearised box a0 = m_a0^2 (a0-a0(0)) + S[rho], compute the quadrupole-analogue power
radiated by a core of mass M_dust = 2.51e12 M_sun collapsing on its free-fall time, for
Lambda_D/Q_0 in {1e-9, 1e-7, 3.1e-6} at both ends of the Q_0 pin; convert to a fractional binding
energy lost per free-fall time; check whether m_a0 blocks propagation (a wave exists only above
omega = m_a0 c). DATA: analytic + `qwen_38_experiment/dust_filters.py` for M_DUST. PASS: >1% of the
binding energy is radiated per free-fall time. KILL: the mode is evanescent (omega_ff < m_a0 c) for
every allowed Lambda_D/Q_0 -- record it as a theorem-grade closure of the radiation channel.
IMPACT: an energy-loss route R2's charge conservation cannot block.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS.md) duplicates I374 (IDEAS_301_400.md), which computes the same scalar-radiation energy loss from a collapsing dust core with the same quadrupole-analogue formula and the same binding-energy comparison. I374 is the more explicit version and is cited by I400, so it is kept. Violates C2.

**I115 — Write the equation of motion for a0 itself.** HYP: on the branch |u| < 1 the promotion
a0^2 = kappa^2 G M^4 sqrt(1−u^2) is invertible, so the Q-equation can be rewritten as a field
equation for a0 — which the corpus has never written. USES: N2+N3. DO: set A = a0^2/a0(0)^2 so u =
±sqrt(1−A^2); substitute Q = Q_0 + Lambda_D u(A) into div(F_Q grad Q) = 4 pi G rho_b and reduce to
an equation for a0(x); report (i) the gradient term's coefficient, (ii) the mass m^2 = −K''(Q_0)/Z
in m^-2 (Z = kinetic normalisation), (iii) the rho_b source. PARTIAL EXPECTED: the linearised
equation alone counts as delivered. DATA: `nbody_2026/stage75_the_closed_theory_2026.py`. PASS: a
closed second-order equation for a0 is obtained. KILL: the inversion is two-valued for physical A
— say where. IMPACT: first equation of motion for a0; all downstream screening ideas need it.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_101_200.md) duplicates I036 (IDEAS.md), which derives the same field equation for a0 by inverting a0^2 = kappa^2 G(-K) into the Q equation and reporting m_a0^2 and the source. I036 is the earliest and most-cited version. Violates C2. (I151 and I198, which cited I115, now cite I036.)

**I145 — Does the wall have a surface tension, and can it halt the dust?** HYP: |Q−Q_0| = Lambda_D
is a surface with an energy per area; if the collapsing dust of R2 drives Q toward it, the tension
supplies the pressure the dust provably lacks. USES: N3+N2+N7. DO: compute sigma = Lambda_D
∫_{-1}^{1} M^4 sqrt(1−u^2) du / sqrt(Z) = (pi/2) M^4 Lambda_D/sqrt(Z) in J/m^2 (state Z's units
and carry them); convert to a pressure sigma/R at R = 10, 100, 1000 kpc and compare with the
dust's binding pressure GM^2/(4 pi R^4) for M = 1e12 Msun. DATA:
`nbody_2026/stage42_amplitude_settled_charge_abundance_2026.py` for the charge-abundance no-go
this must not simply reproduce. PASS: sigma/R exceeds the binding pressure below 200 kpc. KILL:
short by >10x — quote the factor. IMPACT: a wall-sourced pressure would be R2's first live repair.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_101_200.md) duplicates I375 (IDEAS_301_400.md) and I462, all three computing the DBI wall's surface tension sigma and comparing sigma/r with a support requirement. I375 solves the profile variationally and is cited by I365, I382 and I400, so it is the version kept. Violates C2.

**I207 — S1: write the equation of motion for a0 itself.** HYP: nobody has written box a0; it follows
in closed form from the beta=1 DBI plus the promotion, and it has a mass, hence a range. USES:
N2+N3+N7. DO: set q = (Q - Q0)/Lambda_D so -K = M^4 sqrt(1 - q^2) and a0 = kappa sqrt(G) M^2
(1 - q^2)^(1/4), M^4 = rho_Lambda c^2. From the shift-symmetric field equation nabla_mu(K_X
nabla^mu Q) = 0 with X = (grad Q)^2/2, derive box a0 = kappa sqrt(G) M^2 [ f'(q) box q + f''(q)
(grad q)^2 ] with f(q) = (1 - q^2)^(1/4), then eliminate q using q(a0) = sqrt(1 - (a0/(kappa
sqrt(G) M^2))^4). Report (i) the coefficient of (grad a0)^2, (ii) m_a0^2 = d^2 V_eff/d a0^2 at
q = 0, (iii) the range 1/m_a0 in kpc for Q0 = 0.0024 and 0.0146 Mpc^-1 and Lambda_D/Q0 = 1.5e-6
and 3.1e-6. DATA: analytic. PASS: a closed second-order equation with m_a0^2 > 0 -> deliver the
range in kpc at all four corners. KILL: m_a0^2 < 0 at q = 0 -- quote the e-folding time in Gyr.
IMPACT: first equation of motion for a0; fixes its range, the input to every S1 idea.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_201_300.md) duplicates I036 (IDEAS.md): both derive the equation of motion for a0 from the Q equation by inverting the promotion, and both deliver m_a0 and the source term. I036 is the earliest and is cited by I038, I040 and I049. Violates C2. (I212, which cited I207, now cites I036.)

**I234 — S3: where is the wall, for real objects, at both Q0 edges.** HYP: |Q - Q0| = Lambda_D is a
LOCUS, not an abstraction, and with Q0 pinned it has a location — the first question is whether
any real object is past it. USES: N3+N7+N4. DO: the wall is where -K -> 0, hence a0 -> 0; using
q = (Q - Q0)/Lambda_D and N4's a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4), the two must agree, so
solve (1 - q^2)^(1/4) = [(1+nu0^2)/(1+nu^2)]^(1/4) for q(rho) and invert to get the density
rho_wall at which q = 1. Evaluate rho_wall/rho0 for nu0 in {2.36e-6, 2.14e-5, 1.77e-4} and compare
it against the mean densities of: the solar system (1e29 rho0), a cluster core (1e6), a galaxy disc
(1e5), a virialised halo (200), a void (0.1). Report which objects are past the wall.
DATA: analytic. PASS: no real object reaches q = 1 -> the wall is a mathematical boundary only;
report the closest object and its q. KILL: any listed environment has q >= 1 -> a0 = 0 there, which
is a testable prediction; name the object and the density. IMPACT: locates N3's wall in the real
universe for the first time.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_201_300.md) duplicates I413 (IDEAS_401_500.md): both identify (1-x^2)^(1/4) with N4's [(1+nu_0^2)/(1+nu^2)]^(1/4), solve x = 1 for rho_wall and compare it against object densities. I413 is cited by I414, I429, I444 and I456, so it is the version kept. Violates C2. (I254, which cited I234, now cites I413.)

**I269 — S1: does a0 LAG the density it tracks, and which homes can lag at all.** HYP: N4 reads a0 as
an instantaneous function of local rho, but I207 gives a0 a mass and hence a finite response time —
so in a merger or a collapsing halo a0 lags, and homes whose a0-analogue is algebraic in rho
(Palatini, DHOST's Ups1, MOG's mu) CANNOT lag, which is a structural discriminator. USES:
N2+N4+N3. DO: from I207's m_a0 (recompute it if I207 has not run: m_a0^2 = d^2 V_eff/d a0^2 at
q = 0 with -K = M^4 sqrt(1-q^2), M^4 = rho_Lambda c^2) get the response time tau = 1/(c m_a0) and
the correlation length L = 1/m_a0; evaluate both at Q0 = 0.0024 and 0.0146 Mpc^-1 and Lambda_D/Q0 =
1.5e-6 and 3.1e-6, in Myr and kpc. Compare tau to (i) a halo crossing time 2R/V_c at R = 30 kpc,
V_c = 150 km/s, (ii) a cluster merger timescale ~1 Gyr. Then tabulate which homes in I201-I268 admit
a dynamical a0 at all. DATA: analytic. PASS: tau exceeds a crossing time at any corner -> a0 lags,
which is an observable prediction (a0 in a post-merger system differs from its equilibrium value);
quote the lag in Myr and the fractional a0 offset. KILL: tau < 1 Myr at every corner -- a0 is
effectively instantaneous, N4's local reading is exact, and the lag discriminator is dead; say so.
IMPACT: produces a merger-timescale discriminator unique to a0-as-field.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_201_300.md) duplicates I038 (IDEAS.md): both compute the a0 relaxation time tau = 1/(m_a0 c) from the same m_a0^2 = M^4/(Z Lambda_D^2) and compare it with a dynamical time to decide which reading of N4 is physical. I038 is the earliest and is cited by I090. Violates C2.

**I275 — S4: what replaces 13,600x if U is not a fixed curve.** HYP: the s-gap is quoted as a ratio
between two evaluations of ONE curve U(y) — 1.27e-5 at y = 6.3e7 (Earth) and 0.219 at galactic y —
but if a0 = a0(rho) then Earth and a galaxy outskirt sit on DIFFERENT curves and the ratio is not a
ratio of one function's values. USES: N6+N4+N5+N1. DO: write y_Earth = g_bar(1 AU)/a0(rho_solar) and
y_gal = g_bar(20 kpc)/a0(rho_disc) using a0(rho) = a0(0)[(1+nu0^2)/(1+nu^2)]^(1/4) with nu = nu0
rho/rho0; compute both y's for nu0 in {2.36e-6, 2.14e-5, 1.77e-4}, taking rho_solar/rho0 = 1e29 and
rho_disc/rho0 = 1e5. Then recompute the REQUIRED s at each location: s_Earth = 3.66e-14/(a0(rho_solar))
and s_gal from the RAR at a0(rho_disc). Report the corrected gap s_gal/s_Earth at each nu0 and
compare to the quoted 13,600 (canonical) / 17,300 (alt). DATA: analytic; budget from
real_research/reviews/a0_local_ephemeris_2026.py. PASS: the corrected gap falls below 100 at any
allowed nu0 -> R1's headline number is nu0-dependent and must be requoted; give the new number and
the nu0. KILL: the gap changes by < 1% at every nu0 -- R1's number is robust to a0-as-field, which
is the strongest possible confirmation; state it that way. IMPACT: directly re-prices R1's headline
number, in either direction.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_201_300.md) duplicates I094 (IDEAS.md) and I424: all three recompute the R1 gap with the RAR end and the ephemeris end evaluated at different a0(nu). I094 is the earliest and states the grid most completely. Violates C2.

**I332 — Write the equation of motion for a_0.** HYP: the promotion makes a_0 a field, so it inherits an equation of motion from the Q-equation, and because a_0 depends on u only through u^2 the a_0 perturbation is QUADRATIC in the field perturbation -- a structural fact nobody has written down. USES: N2+N3+N7. DO: expand S = int sqrt(-g) K(Q) with Q = A^mu d_mu phi to quadratic order in u = Q - Q_0; read off the kinetic coefficient K_QQ(0) = M^4/Lam_D^2 and check whether the shift symmetry forbids a mass term m_u^2 u; then use a_0(u)/a_0(0) = (1-u^2/Lam_D^2)^(1/4) to convert the u-equation into an equation for delta a_0/a_0 = -(1/4)(u/Lam_D)^2 + O(u^4), stating explicitly that a_0 responds at SECOND order in u; report the correlation length xi = 1/m_u (or "infinite" if m_u = 0) in kpc for Q_0 in {0.0024, 0.0146} Mpc^-1 and R in {2.3e-9, 3.1e-6}. DATA: nbody_2026/stage75_the_closed_theory_2026.py, real_research/bridge1_aest_equations.md for the reference AeST transcription. PASS: the equation is written with an explicit source term and xi is finite between 1 pc and 1 Mpc. KILL: the shift symmetry forces m_u = 0 so xi is infinite -- a_0 has no correlation length and cannot support a local gradient; say so, it is equally decisive. IMPACT: First equation of motion for a_0; fixes its correlation length.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_301_400.md) duplicates I036 (IDEAS.md): both write the equation of motion for a_0 by expanding K about the minimum and report the mass and the correlation length. I036 is the earliest; the correlation-length deliverable is also I032's. Violates C2. (I335, which cited I332, now cites I036.)

**I374 — Can a collapsing core radiate a_0 waves, and does that drain it?** HYP: the a_0 field of I332 has wave solutions at speed c_s = 1-u^2/Lam_D^2 (squared), so a non-spherical collapsing dust core radiates scalar waves and loses energy -- the only dissipation channel a shift-symmetric condensate can have, and one nobody in the corpus has priced. USES: N2+N3+N7. DO: linearise u about the collapsing background of I320; using the quadrupole formula for a scalar with kinetic coefficient K_QQ(0) = M^4/Lam_D^2 and speed c_s, compute the luminosity L = (K_QQ(0)/(60 pi c_s^5)) <d^3 D_ij/dt^3>^2 for an L* core of M_dust = 2.51e12 Msun collapsing from 250 kpc with ellipticity e in {0.1, 0.3}; integrate over 13.8 Gyr and compare with the binding energy G M_dust^2/r at r = 1 and 10 kpc. Both footings; Q_0 = 0.0024 Mpc^-1, R in {2.3e-9, 3.1e-6}. DATA: nbody_2026/stage75_the_closed_theory_2026.py, qwen_38_experiment/dust_filters.py for M_DUST. PASS: radiated energy exceeds 10% of the binding energy -- the first dissipation channel in the sector; escalate. KILL: below 1e-6 of the binding energy, or c_s -> 0 makes the mode non-radiative -- the condensate is dissipationless by construction; record it. IMPACT: First dissipation channel for the dust; drains it or provably cannot.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_301_400.md) duplicates I049 (IDEAS.md) as it stood: both computed the scalar-radiation luminosity of a collapsing dust core and compared the radiated energy with the binding energy. I049 has been retargeted to the a0 gradient's own weight, and this slot now carries a different R2 bound. Violates C2 as written.

**I411 — S4: legality re-derived with a0 = a0(rho), the central obstruction's own premise.** HYP: the single-valuedness argument
forcing U -> s assumed a0 constant; with a0 = a0(rho) the variable y = g_bar/a0(rho) is not a coordinate on a fixed curve and the
condition may change. USES: N2+N4+N6. DO: read the derivation in real_research/reviews/typeII_legality_independent_2026.py; re-run
it with a0 -> a0(nu) = a0(0)[(1+nu_0^2)/(1+nu^2)]^(1/4), nu = nu_0 rho/rho_0. Symbolically recompute dF/dY single-valuedness
treating (Y, Q) as independent, and print whether the required monotonicity is in y, in g_bar, or in the pair. DATA: analytic.
PASS: the condition is NOT monotonicity in y -- name the replacement and re-derive s. KILL: identical condition; R1 deepens.
IMPACT: R1 dissolves or is confirmed at the level of its own premise.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I341 (IDEAS_301_400.md): both read the constant-a0 derivation in typeII_legality_independent_2026.py and re-derive single-valuedness with a0 = a0(rho) to decide whether the surviving condition is monotonicity in y or in g_bar. I341 states the two candidate conditions explicitly and is cited by I378. Violates C2.

**I422 — S4: a legal coupled system whose APPARENT U is non-monotone.** HYP: monotonicity is required of the free function, not of
the reconstructed U(y_obs); if a0 varies with the same density that sets g_bar, a legal F can present a non-monotone apparent U --
which is exactly what Route A needs. USES: N2+N4+N6. DO: take U_legal(y;s) = v/(1-v/s) at s = 1e-5 with y = g_bar/a0(nu);
construct rho(g_bar) for an exponential disc (rho ~ g_bar^p, scan p in {0.5, 1.0, 1.5, 2.0}); plot the apparent U_app(g_bar/a0(0))
and test for a maximum, comparing with Route A's peak U = 0.6476 at y = 2.540. DATA: analytic. PASS: any (s,p) gives a maximum
then a decline -- write the explicit legal system, this is the R1 escape. KILL: U_app monotone for all (s,p) at nu_0 <= 2.36e-6.
IMPACT: builds or forbids a legal Route-A-shaped kernel (R1).
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I087 (IDEAS.md): both build a legal J_Y = v/(1-v/s) system with a0 = a0(rho), reconstruct the apparent U under the constant-a0 assumption, and test it for non-monotonicity. I087 is the earlier and ties rho to g_bar explicitly. Violates C2.

**I424 — S4: what replaces the 13,600x gap when a0 tracks density?** HYP: the R1 gap was computed with one a0 for both ends; with
N4 the RAR-required s and the ephemeris-allowed s are evaluated at DIFFERENT a0, so the gap number changes. USES: N2+N4+N6. DO:
recompute both ends of R1 with a0 -> a0(nu): (i) the ephemeris bound s_eph = 3.66e-14 / a0(nu_solar) using the Sereno-Jetzer
inversion in real_research/reviews/mi_alpha1_solar_system_2026.py; (ii) s_RAR from the disc a0; take rho_solar/rho_disc in {1e2,
1e3, 1e4} and nu_0 in {2.36e-6, 1.77e-4}. Print the gap s_RAR/s_eph for all six cells. DATA: analytic. PASS: any cell drops the
gap below 100x -- escalate immediately with the required nu_0. KILL: all six stay above 1e4. IMPACT: recomputes R1's headline
number under the framework's own promotion.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I094 (IDEAS.md) and I275 as written: the same recomputation of the 13,600x/17,300x gap with the two ends evaluated at different a0(nu). I094 is kept. Violates C2.

**I425 — S1: the equation of motion for a0 itself.** HYP: because a0^2 = kappa^2 G(-K(Q)), the Q field equation IS an equation for
a0, and writing it out gives box a0 with an explicit source and an explicit mass term. USES: N2+N3. DO: start from the Q equation
box Q = dV/dQ - (dF/dQ) and change variables to A == a0/a0(0) = (1-x^2)^(1/4), x = (Q-Q_0)/Lambda_D. Derive box A + m_A^2 (A - 1)
= S in sympy, reading m_A^2 from the quadratic expansion of -K and S from the matter coupling. Evaluate m_A in Mpc^-1 for Q_0 in
{0.0024, 0.0146} and Lambda_D/Q_0 in {1e-9, 1e-7, 3.1e-6}. DATA: analytic. PARTIAL EXPECTED: the linearised equation alone counts.
PASS: box A + m_A^2(A-1) = S written explicitly with a numeric m_A in Mpc^-1. KILL: the change of variables is singular at x = 0
or A is not a valid field variable -- say why. IMPACT: gives a0 an equation of motion -- opens the whole S1 programme.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I036 (IDEAS.md), I115, I207 and I332 -- five ideas wrote the same equation of motion for a0. I036 is kept as the canonical derivation. Violates C2.

**I426 — S1: the a0-field's propagation speed and correlation length.** HYP: the a0 perturbation propagates at the Q sector's
sound speed, and 1/m_A is its correlation length -- if that length is sub-galactic, a0 is effectively local and N4's rho-tracking
is justified; if Mpc-scale, it is not. USES: N2+N3+N7. DO: take m_A from I425 (or re-derive the quadratic term of -K if I425 is
not run); compute L_A = 1/m_A in kpc for Q_0 in {0.0024, 0.0146} Mpc^-1 and Lambda_D/Q_0 in {1e-9, 1e-8, 1e-7, 1e-6, 3.1e-6};
compute c_A^2 = 2(m_x/mu)^2 using the committed identity in real_research/reviews/kb_small_limit_safety_2026.py. DATA: analytic.
PASS: L_A < 10 kpc anywhere in the scan -- N4's local rho-tracking is justified, say where. KILL: L_A > 1 Mpc everywhere -- a0
CANNOT track galactic density and N4 needs restating. IMPACT: validates or breaks N4's premise.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I032 (IDEAS.md): both compute the a0 correlation length 1/m from the same m^2 = M^4/(Z Lambda_D^2) on the same Lambda_D/Q_0 grid and compare it with galaxy and cluster scales. I032 is the earlier. Violates C2.

**I428 — S1: does a0 LAG the density it tracks?** HYP: a0 relaxes to a0(rho) on the timescale 1/(m_A c), so in a collapsing or
rotating system a0 is set by the density of the past, not the present -- a hysteresis with an observable sign. USES: N2+N4+N3. DO:
take m_A (from I425 or the quadratic expansion of -K) and form t_relax = 1/(m_A c) in Gyr for Lambda_D/Q_0 in {1e-9, 1e-7,
3.1e-6}; compare with (i) a disc orbital period at 8 kpc (0.22 Gyr), (ii) the turnaround-to-virial time of a 1e12 Msun halo (~2
Gyr). Report the lag phase angle arctan(omega t_relax) for both. DATA: analytic. PASS: t_relax exceeds the orbital period, so a0
is frozen at the mean density -- state which observable inherits the lag. KILL: t_relax < 1e-3 of both times -- a0 is
instantaneous, and say so as a licence for N4. IMPACT: tests N4's quasi-static use of a0(rho).
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I038 (IDEAS.md) and I269 as written: the same relaxation time t_relax = 1/(m_A c) compared with an orbital and a collapse time. I038 is kept. Violates C2.

**I431 — The kappa constraint Jacobian: why R3 stands.** HYP: kappa enters the normalisation N1, the promotion N2 and the
deep-MOND BTFR, and those supply fewer independent constraints than unknowns. USES: N1+N2+N6. DO: START FROM
qwen_38_experiment/KAPPA_LEDGER.md, which already lists every kappa DERIVATION ATTEMPT -- do not rebuild that list. New content:
write the constraint vector C(kappa, M, Lambda_D, Q_0, s) from (i) a0 = kappa c sqrt(G rho_L), (ii) a0^2 = kappa^2 G(-K(Q_0)),
(iii) v^4 = G M_b a0, (iv) beta = mu^2 Lambda_D^2/M^4 = 1; compute the Jacobian rank with sympy. DATA: analytic. PASS: rank
deficiency exactly 1 -- name the one extra measurement that would close it. KILL: full rank -- kappa IS determined; find the
derivation. IMPACT: converts R3 from an observation into a counted rank deficiency.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I404 (IDEAS_401_500.md): both write the kappa constraint system in sympy and report the rank of its Jacobian to decide whether kappa is determined. I404 is the earlier. Violates C2.

**I436 — S2: dark energy is suppressed where the charge is dense -- by how much?** HYP: since a0^2 = kappa^2 G(-K) and -K is the
dark sector's pressure, rho_Lambda -> P(x)/c^2 locally, so rho_Lambda is DEFICIENT inside bound structures by a computable
fraction. USES: N1+N2+N4. DO: compute delta == P(x)/(rho_Lambda c^2) - 1 = [a0(nu)/a0(0)]^4 - 1 = (1+nu_0^2)/(1+nu^2) - 1 at nu_0
= 2.36e-6 for rho/rho_0 = 1e2 (cluster outskirt), 1e5 (cluster core), 1e7 (galaxy disc), 1e30 (solar interior). Report delta and
the implied local rho_Lambda in kg/m^3 for each. DATA: analytic. PASS: |delta| > 1e-3 anywhere -- dark energy is measurably
inhomogeneous, name the site. KILL: |delta| < 1e-8 everywhere at the cap. IMPACT: opens S2 -- inhomogeneous dark energy as a
framework-only prediction.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I219 (IDEAS_201_300.md): both evaluate the local dark-energy deficit 1 - [(1+nu_0^2)/(1+nu^2)]^(1/2 or 1) across the same density ladder. I219 is the earlier and adds the home-sorting deliverable. Violates C2. (I440 and I493, which cited I436, no longer do.)

**I438 — S2: the volume-averaged <P> versus the rho_Lambda Planck fits.** HYP: Planck measures a volume-averaged dark-energy
density, but the promotion says P is suppressed in every bound structure, so <P> < rho_Lambda c^2 at the minimum -- and kappa,
inferred from rho_Lambda, inherits the bias. USES: N1+N2+N4. DO: take the cosmic density PDF as lognormal with sigma_ln = 2.0 at z
= 0 (state the assumption), compute <P>/(rho_Lambda c^2) = <(1+nu_0^2)/(1+(nu_0 rho/rho_0)^2)> by numerical integration at nu_0 =
2.36e-6, 2.14e-5, 1.77e-4; convert the deficit into a delta-kappa = kappa[(<P>/rho_Lambda c^2)^(1/2) - 1]. DATA: analytic. PASS:
|delta-kappa| > 0.005 at any allowed nu_0 -- the measured kappa carries an inhomogeneity bias, quote it. KILL: < 1e-5 at the cap.
IMPACT: a new systematic on R3 that exists only in this framework.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I336 (IDEAS_301_400.md): both volume-average the suppressed -K over a two-component universe and convert the deficit into a bias. I336 is cited by I331 and states the bound-fraction grid, so it is kept. Violates C2; its lognormal PASS branch was also unreachable at nu_0 <= 2.36e-6 (effect ~ nu_0^2).

**I456 — S3: is there a shell inside a halo where a0 = 0?** HYP: if x = (Q-Q_0)/Lambda_D reaches 1 at some interior radius, a0
vanishes on a SHELL and the rotation curve must show a feature there. USES: N3+N4+N7. DO: for an NFW-like baryon+charge profile of
a 1e12 Msun halo, use the I413 density-to-x map to find r where x = 1, scanning Q_0 in {0.0024, 0.0146} Mpc^-1, Lambda_D/Q_0 in
{1e-9, 1e-7, 3.1e-6} and nu_0 in {2.36e-6, 1.77e-4}; where a shell exists, compute the predicted V(r) discontinuity in km/s from
a0 -> 0 across it. DATA: analytic; compare the feature amplitude with the median SPARC velocity error in
real_research/data/SPARC_Lelli2016c.mrt. PASS: a shell exists in any cell with a feature above the median error -- SPARC already
excludes those cells, quote which. KILL: no shell in any of the 12 cells. IMPACT: SPARC rotation curves as an S3 wall constraint
on N7.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I254 (IDEAS_201_300.md): both solve for the radius at which x = 1 in a halo profile and compare the predicted rotation-curve feature with SPARC's errors. I254 is the earlier and searches the 175 curves. Violates C2.

**I462 — S3: does the wall carry a surface tension, and does it show?** HYP: |Q-Q_0| = Lambda_D is a phase boundary, so it should
carry an energy per unit area sigma_wall ~ M^4 Lambda_D / mu^2, which would add a surface term to the virial theorem of any object
enclosing one. USES: N3+N7. DO: derive sigma_wall by integrating the DBI energy density across the wall in the thin-wall
approximation, sigma_wall = int_{-Lambda_D}^{Lambda_D} sqrt(2 (-K(Q))) dQ / mu, evaluate in J/m^2 for Q_0 in {0.0024, 0.0146}
Mpc^-1 and Lambda_D/Q_0 in {1e-9, 1e-7, 3.1e-6}; then form the ratio of the wall energy 4 pi R^2 sigma_wall to the binding energy
G M^2/R for a 1e14 Msun cluster. DATA: analytic. PASS: the ratio exceeds 1e-3 in any cell -- the wall is energetically real and R4
gains a candidate. KILL: below 1e-12 everywhere. IMPACT: prices S3's wall as a cluster energy term.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I375 (IDEAS_301_400.md) and I145: the same wall surface tension computed and compared with a binding term. I375 is kept. Violates C2.

**I482 — Lunar laser ranging as an s-meter: does the anomaly cancel?** HYP: a CONSTANT sunward anomaly s a0 is nearly common-mode
on the Earth-Moon pair, so LLR's 1 mm precision buys far less than its raw sensitivity suggests -- a statement true only because
legality forces U -> s. USES: N1+N6. DO: compute the DIFFERENTIAL anomaly across the lunar orbit, i.e. the change in s a0 between
perihelion-side and aphelion-side lunar positions, which for a constant-magnitude radial field is s a0 (1 - cos(a_moon/d_sun))
plus the direction-change term s a0 a_moon/d_sun; evaluate at s = 0.219 and s = 1.27e-5 with a_moon = 3.84e8 m, d_sun = 1.496e11
m; integrate to a range perturbation over one synodic month and compare with 1 mm. DATA: analytic. PASS: s = 0.219 produces > 1 mm
-- LLR independently bounds s; quote the bound. KILL: even s = 0.219 gives < 0.1 mm -- record the number so LLR is never
re-proposed for R1. IMPACT: prices or closes LLR as an R1 channel.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I079 (IDEAS.md): both compute the Earth-Moon differential of a constant sunward s a0 and compare the induced range perturbation with the 1 mm LLR floor. I079 is the earlier. Violates C2.

**I493 — S2: the ISW signal from inhomogeneous dark energy.** HYP: if P(x) is suppressed where the charge is dense, dark energy
decays inside superclusters and grows in voids, adding an ISW term with the OPPOSITE sign structure to LCDM's -- a signature no
homogeneous-Lambda theory has. USES: N1+N2+N4. DO: using delta(rho) from I436, build delta-rho_Lambda(x)/rho_Lambda =
(1+nu_0^2)/(1+(nu_0 rho/rho_0)^2) - 1 on a lognormal density field (sigma_ln = 2.0, state the assumption); compute the extra
Phi-dot from the local Lambda variation and the resulting delta-C_L^{Tg} at L = 10, 30, 100 relative to the LCDM ISW amplitude; do
it at nu_0 = 2.36e-6 and 1.77e-4. DATA: analytic; LCDM ISW amplitude from CLASS. PASS: the extra term exceeds 1% of the LCDM ISW
at any L -- a live S2 discriminator, name the survey. KILL: below 1e-4 at the cap. IMPACT: turns S2's inhomogeneous dark energy
into a CMB cross-correlation test.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I057 (IDEAS.md): both compute the local dark-energy deficit from 1/sqrt(1+nu^2) and feed it into the ISW kernel to get a fractional change in the ISW-galaxy cross-power. I057 is the earlier; the lognormal version's PASS branch was also unreachable at nu_0 <= 2.36e-6. Violates C2 and was null by construction.

---

## Second cut — final audit 2026-08-17 (cross-file duplicates and null-by-construction)

Twenty-three entries cut because another live idea already produces the same computation
(C2), or because the effect they test is O(nu_0^2) ~ 5.6e-12 at the RAR ceiling and could
never fire. Each id was refilled in place with a new idea, so every file still holds 100.
Text below is the entry exactly as it stood before the cut.

**I086 — Read the framework as INHOMOGENEOUS dark energy, not modified gravity. (S2)** HYP: N1 holds at the brane minimum, but N2 makes -K a
field, so locally rho_Lambda -> -K(x)/c^2: the two lines that tie a0 to dark energy also say dark energy is suppressed where the charge is dense.
USES: N1+N2+N3. DO: compute the deficit 1 - (-K)/M^4 = 1 - 1/gamma with gamma = sqrt(1+nu^2) at rho/rho_0 = 1e5 (cluster), 1e6 (galaxy inner),
1e8 (interplanetary), 0.2 (void), for nu_0 in {2.36e-6, 1e-5, 1e-4}; then compute the volume-averaged <-K>/M^4 over a Hubble volume using the
lognormal density PDF with sigma_ln = 1.5, and compare it to the Planck-fitted rho_Lambda. DATA: analytic. PASS: <-K>/M^4 differs from 1 by >
1e-3, so Planck's rho_Lambda is NOT the brane's M^4 and every a0 anchored to it inherits a bias -- quote the bias in kappa. KILL: below 1e-6
everywhere. IMPACT: a second observable sector out of the same two committed lines.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS.md) duplicates I336 (IDEAS_301_400.md), which volume-averages the suppressed -K and converts the deficit into a bias on kappa, and its first half repeats I219's deficit ladder. I336 is cited by I331 and is kept; this slot now carries the S2 ceiling that grades the rest of the S2 block. Violates C2.

**I447 — Intrinsic scatter as a nu_0 bound.** HYP: any real environmental variation of a0 would appear as intrinsic scatter on the
a0-line, so the measured intrinsic term caps nu_0 more directly than any environmental split. USES: N4+N5. DO: START FROM
real_research/reviews/rar_tightness_intrinsic.py and project_rar_bounds_rho_uniformity.py, which already bound how much a0 may vary
-- do not redo the scatter fit framing. New content: convert the posterior upper limit on the intrinsic term into a limit on nu_0 by
inverting sigma_intrinsic(dex) = (1/4) log10[(1+nu_hi^2)/(1+nu_lo^2)] with nu = nu_0 rho/rho_0 over SPARC's own density range. DATA:
real_research/data/SPARC_Lelli2016c.mrt, real_research/rar_framework_a0_mlfit.py. PASS: the derived cap beats 2.36e-6 -- quote it as
the new bound. KILL: looser than 1e-4. IMPACT: a new N4 cap straight from the RAR's intrinsic scatter.
PRIOR: (second cut, final audit 2026-08-17, from IDEAS_401_500.md) duplicates I071 (IDEAS.md): both convert the committed intrinsic RAR-scatter limit into a cap on nu_0 through the same d ln a0/d ln rho relation over SPARC's density range. I071 is the earlier and names the committed script to start from. Violates C2.

---

## Second cut — final audit 2026-08-17 (cross-file duplicates and null-by-construction)

Twenty-three entries cut because another live idea already produces the same computation
(C2), or because the effect they test is O(nu_0^2) ~ 5.6e-12 at the RAR ceiling and could
never fire. Each id was refilled in place with a new idea, so every file still holds 100.
Text below is the entry exactly as it stood before the cut.

---

## Second cut — final audit 2026-08-17 (cross-file duplicates and null-by-construction)

Twenty-three entries cut because another live idea already produces the same computation
(C2), or because the effect they test is O(nu_0^2) ~ 5.6e-12 at the RAR ceiling and could
never fire. Each id was refilled in place with a new idea, so every file still holds 100.
Text below is the entry exactly as it stood before the cut.

