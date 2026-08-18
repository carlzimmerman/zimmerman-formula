# 100 ideas — one per session

Each is self-contained. Do not read the others. Format: **HYP** hypothesis, **DO** method,
**DATA** where to get it, **PASS/KILL** the pre-registered decision.

---

## A. The 233x incompatibility — escape routes (highest value: this is the live problem)

**I001 — Does the EFE factorise against a density-dependent a0?** HYP: the committed EFE
reduction (119-189x) was computed at constant a0; against a0(rho) it may compound
differently. DO: take the EFE suppression as a function of the ratio g_ext/a0, then let a0
vary per the promotion and recompute. DATA: `real_research/reviews/a0_local_ephemeris_2026.py`.
PASS: the combined reduction exceeds 233x. KILL: it stays near the multiplicative estimate.

**I002 — Is saturation actually forced?** HYP: `U -> const` follows from monotone U plus
`U/y -> 0`; test whether a legal U can grow without bound while still giving `nu -> 1`. DO:
try `U = sqrt(y) * f(y)` with f decaying slower than `1/sqrt(y)`; check monotonicity, the
Newtonian limit, and the resulting 1 AU anomaly. PASS: a legal non-saturating U exists.
KILL: monotone + Newtonian forces a finite limit.

**I003 — Disc (non-spherical) correction to the local law.** HYP: `u J_Y(u^2) = g_bar` is
exact only in spherical symmetry; discs may shift the RAR requirement on s. DO: solve the
AQUAL-type equation for a Miyamoto-Nagai disc numerically, compare u(r) with the spherical
algebraic answer. PASS: the disc value of s needed drops below 0.1. KILL: shift is < 20%.

**I004 — Ephemeris refit with the signal in the model.** HYP: the anomalous-precession
limits assume no such term; fitting it jointly with GM_sun weakens them. DO: build a toy
2-parameter fit (GM, u_infinity) to the four inner planets' precessions and get the
marginalised bound on u_infinity. PASS: the bound loosens by >10x. KILL: <2x.

**I005 — Multi-valued J with hysteresis branches.** HYP: a multi-valued free function might
be admissible if branches are selected by history, rescuing Route A. DO: write the two
branches of Route A's U(y) explicitly, check whether a physical trajectory could stay on the
lower branch in the solar system, and whether the branch jump is thermodynamically allowed.
PASS: a consistent branch selection exists. KILL: the ghost is present on either branch.

**I006 — Time-dependent chi in the solar system.** HYP: the saturated anomaly assumes a
static chi; an oscillating solution could average to a smaller mean. DO: add
`chi = chi_0(r) + delta(r) cos(omega t)` and compute the orbit-averaged radial force.
PASS: time-average reduces the anomaly by >10x. KILL: <2x.

**I007 — Does the anomaly point sunward at all?** HYP: the direction of `grad chi` in the
solar system is set by the Galactic boundary condition, not the Sun, so the anomaly may be
a uniform (unobservable) offset plus a small tide. DO: solve for chi with a Sun embedded in
a uniform external scalar gradient; decompose into uniform + tidal parts. PASS: the sunward
constant part largely cancels. KILL: it survives at >0.3 of the naive value.

**I008 — A second scalar that screens only at high y.** HYP: adding a field coupled so it
cancels the saturated anomaly above some y* without touching galaxies. DO: write the
minimal such coupling, check ghost-freedom and whether y* can sit between galactic and
solar-system y. PASS: a ghost-free construction exists. KILL: it needs a wrong-sign kinetic
term.

**I009 — Non-minimal matter coupling.** HYP: letting matter couple to a disformal metric
rather than g alone could suppress the solar-system anomaly. DO: apply a disformal
transformation and see how the anomaly and gamma_PPN transform. PASS: anomaly suppressed
with gamma_PPN still 1. KILL: gamma_PPN breaks.

**I010 — K_B-dependent screening.** HYP: the aether sector's K_B might enter the
quasi-static anomaly at high y even though it drops out at low y. DO: retain K_B in the
quasi-static solve and check whether the saturation value depends on it. PASS: s depends on
K_B. KILL: it does not.

**I011 — The curl sector at solar-system scales.** HYP: the transverse aether mode might
contribute an anomaly of the opposite sign. DO: compute the curl-sector contribution to the
radial force at 1 AU. PASS: opposite sign and >10% cancellation. KILL: negligible or same
sign.

**I012 — Is the RAR requirement on s really 0.558?** HYP: `U(y~2) >= 0.4` was read off the
a0-line; a proper fit may allow smaller s if Upsilon is refitted. DO: for s in
[0.05, 0.1, 0.2, 0.3, 0.5, 1, 2], refit Upsilon and report the best rms dex. DATA:
`ai_slop/website/public/data/rar_real_sparc.json`. PASS: some s < 0.1 reaches < 0.15 dex.
KILL: rms blows up below s ~ 0.4.

**I013 — Does the BTFR constrain s?** HYP: the baryonic Tully-Fisher slope and zero point
depend on the deep-MOND limit only, so may be s-blind — or may not. DO: derive V^4 = G M a0
for the legal family and check the s-dependence. DATA: SPARC master table. PASS: BTFR
constrains s. KILL: it is s-blind (still useful).

**I014 — Wide binaries as an s-meter.** HYP: the Gaia wide-binary boost depends on s. DO:
compute gamma_v for s = 0.1, 0.5, 1, 2 using the same closure as
`prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py` (COPY it, do not edit it). PASS:
gamma_v separates the s values by >0.02. KILL: degenerate.

**I015 — Clusters as an s-meter.** HYP: cluster dynamical-to-lensing mass ratios depend on
s. DO: compute the predicted eta at R500 for a range of s. PASS: some s fits clusters AND
is below the ephemeris bound. KILL: no overlap.

---

## B. The legal class — characterise it properly

**I016 — Full characterisation of the legal class.** DO: prove or disprove that every legal
U is generated by `J_Y = y(U)/U` and that this map is a bijection onto strictly-increasing
U with the stated limits. PASS: bijection proved. KILL: counterexample.

**I017 — Minimum-anomaly legal kernel at fixed RAR quality.** HYP: there is a legal U
minimising the 1 AU anomaly subject to fitting the RAR at <= 0.12 dex. DO: parameterise U
with 3-4 knots, optimise. DATA: RAR json. PASS: the minimiser gets the ephemeris ratio
below 10x. KILL: it cannot go below 100x.

**I018 — Is the a0-line special in the legal class at all?** HYP: some property (analyticity,
minimal parameter count, an exact algebraic g_obs-g_bar relation) singles it out. DO:
enumerate candidate distinguishing properties and test each against the family
`J_Y = v/(1-v/s)`. PASS: a property picks s = 1/2. KILL: none does.

**I019 — Legal kernels with an inflection.** HYP: U may be monotone but non-convex, buying
a fast rise in galaxies and a slow one after. DO: construct U with an inflection above
y ~ 10 and check legality and the 1 AU value. PASS: ephemeris ratio < 10x with RAR intact.
KILL: monotonicity forbids the shape.

**I020 — Two-scale legal kernels.** HYP: `U = s1*sqrt(y)/(s1+sqrt y) + s2*(...)` with two
scales could satisfy both constraints. DO: build it, check legality, fit RAR, compute 1 AU.
PASS: both constraints met. KILL: the sum breaks monotonicity or the deep-MOND limit.

**I021 — The Newtonian-limit condition, sharpened.** HYP: `U/y -> 0` may be stronger than
needed; the real requirement is only that g_obs -> g_bar to within observational error at
solar-system y. DO: quantify what U(6e7) is actually allowed by solar-system data directly.
PASS: the allowed U is larger than the ephemeris bound implies. KILL: same.

**I022 — Legality under a different Y definition.** HYP: if `Y` were built from the total
potential gradient rather than the scalar's, Route A becomes legal (AQUAL-like). DO: write
the modified action term and check whether it still gives AeST's CMB behaviour. PASS: a
consistent variant exists. KILL: it breaks the CMB sector.

**I023 — Does legality survive at finite K_B?** HYP: the monotonicity criterion was derived
in a limit; check it at general K_B. DO: redo the longitudinal stiffness with K_B retained.
PASS: unchanged. KILL: K_B modifies the criterion.

**I024 — Legality with the Q-sector coupled.** HYP: cross terms F_YQ could change the
stiffness condition. DO: include F_YQ in the kinetic matrix and re-derive. PASS: criterion
unchanged. KILL: a new term appears.

**I025 — Relativistic corrections to the criterion.** HYP: the criterion is quasi-static;
check it holds for propagating modes. DO: compute the dispersion relation for delta-chi
about a nontrivial background. PASS: same condition. KILL: different.

---

## C. kappa — the three routes still open

**I026 — Non-monomial pi-free combinations.** HYP: kappa = 1/2 arises from a non-monomial
combination of horizon quantities. DO: enumerate ratios of sums (not products) of
{R_H, l_P, T_dS, S_dS} that are dimensionless and pi-free; check which give 1/2.
PASS: a forced 1/2 with no free parameter. KILL: all carry a free parameter.

**I027 — A theory-fixed radius ratio.** HYP: kappa = 1/2 is the ratio of two radii the
theory itself fixes (e.g. the DBI wall radius to the Hubble radius). DO: compute
Lambda_D/Q_0 in length units and compare to 1/2 of anything natural. PASS: an identity.
KILL: no match within 10%.

**I028 — A combinatorial factor of 2.** HYP: the 1/2 is a degeneracy/counting factor
(two horizons, two polarisations, particle-antiparticle). DO: enumerate the countable
2s in the derivation chain and check which would land kappa at 1/2. PASS: exactly one
survives scrutiny. KILL: several or none.

**I029 — kappa from the DBI wall.** HYP: beta = 1 plus the promotion forces kappa. DO:
write a0^2 = kappa^2 G(-K) at the wall and at the minimum and see whether consistency fixes
kappa. PASS: kappa determined. KILL: it cancels.

**I030 — kappa from the deep-MOND coefficient.** HYP: the (2/3) in `J -> (2/3)Y^(3/2)/a0`
is fixed by the action, and matching it to SZ21's printed `2 lambda_s/(3(1+lambda_s)a0)`
may fix a combination involving kappa. DO: do the matching carefully at finite lambda_s.
PASS: a relation involving kappa. KILL: kappa absent.

**I031 — Measure kappa from the gas-dominated subsample only.** DO: rerun the gas-dominated
estimator with tighter cuts (f_gas > 0.8) and report kappa +/- sigma. DATA: SPARC master
table. PASS: sigma < 0.05. KILL: sample too small.

**I032 — kappa from the BTFR zero point alone.** DO: fit the BTFR normalisation and invert
for kappa with the framework's own kernel. PASS: an independent kappa with sigma < 0.08.
KILL: degenerate with Upsilon.

**I033 — kappa's H0 dependence, mapped.** HYP: kappa depends on H0 through the distance
scale; map kappa(H0) over 67-74. DO: recompute for a grid of H0. PASS: a clean linear map.
KILL: nonlinear/unstable.

**I034 — Is kappa the same on both footings?** DO: measure kappa independently assuming the
alt footing and compare. PASS: consistent within errors. KILL: footing-dependent (important).

**I035 — kappa from clusters.** DO: invert the cluster eta requirement for kappa. PASS: a
value within 2 sigma of 0.53. KILL: wildly different (also informative).

---

## D. The dust problem (2d) — use the free filters first

**I036 — Screen the four dead candidates through the filters.** DO: run
`qwen_38_experiment/dust_filters.py --explain`, write a spec JSON for each of the four
candidates in `real_research/reviews/second_field_catalog_2026.py`, screen each.
PASS: 4/4 agreement with the review's verdicts. KILL: a disagreement (means the filter is
wrong — report loudly).

**I037 — Is the dust forced to be irrotational?** HYP: the corpus assumes an irrotational
potential flow; if vorticity is allowed, centrifugal support evades all five filters. DO:
check whether the shift symmetry plus the equation of motion forbid vorticity identically or
only for irrotational initial data. PASS: vorticity allowed. KILL: forbidden identically.
**This is the highest-value item in section D.**

**I038 — Non-charge-built pressure: enumerate.** DO: list candidate pressure sources not
built from the conserved charge (second condensate, gauge field, fermion degeneracy,
turbulent stress, gradient energy, finite-temperature radiation); screen each with
`dust_filters.py`. PASS: any survivor. KILL: all die.

**I039 — A scalar that falls outward.** HYP: filter F5 kills gates monotone in a quantity
rising outward; find a theory scalar that falls outward. DO: list local scalars (Q, Y,
|grad phi|, rho, curvature invariants) and compute each one's radial gradient sign in the
committed support profile. PASS: one falls outward. KILL: none.

**I040 — Is r_x/R_supp = 0.194 universal?** DO: recompute the crossover across the SPARC
range of M_bar/M_dyn. DATA: SPARC master table. PASS: some class reaches > 0.5. KILL: it is
0.15-0.25 everywhere.

**I041 — Which input dominates the Sgr A* falsification?** DO: locate the committed
calculation in `nbody_2026/`, re-derive, sweep its inputs. PASS: a halo class where the
margin < 10x. KILL: robust everywhere.

**I042 — Two-component split.** HYP: a fraction f of the charge is dust, the rest something
else. DO: bound f from below by the CMB clustering requirement and from above by the
collapse. PASS: a non-empty interval. KILL: empty.

**I043 — Transport with the framework's own enhanced gravity.** DO: recompute the committed
690 Gyr transport timescale with `g = nu(y) g_bar` and the derived a0(z). PASS: drops below
a Hubble time. KILL: still >> Hubble.

**I044 — The a0-gate escape corner.** DO: map where the restriction `nu0*r_supp >= 10`
fails and recompute the corner on its own terms. PASS: a live escape. KILL: closed.

**I045 — Maximum tolerable lensing pile-up.** DO: using the KiDS fit, compute the maximum
mass excess at 0.3-1 Mpc allowed at 2 sigma. DATA: `prep_2026/kids_rar/kids_rar_lambda.py`.
PASS: a tolerance curve (add it to dust_filters as F6). KILL: cannot extract.

**I046 — Observable signature short of a black hole.** DO: compute the intermediate-state
density profile and its effect on rotation curves at 0.1-10 kpc. PASS: a named observable.
KILL: unobservable (still useful).

**I047 — Literature: dust retention in shift-symmetric condensates.** DO: search the
ghost-condensate / khronon / superfluid-DM / BEC-DM literature for support mechanisms in a
sector with a conserved shift charge. Cite only what you read. PASS: an annotated list.
KILL: nothing found.

**I048 — Does the collapse actually reach the endpoint?** HYP: the free-fall time may exceed
a Hubble time for realistic profiles. DO: compute the collapse time for the committed
profile. PASS: exceeds Hubble. KILL: much shorter.

**I049 — Does a0 suppression slow the collapse?** HYP: as the dust concentrates, a0 drops
(promotion), weakening the MOND enhancement driving collapse — a negative feedback. DO:
compute d(collapse rate)/d(rho) including the a0(rho) dependence. PASS: feedback changes the
sign or the exponent. KILL: too weak to matter.

**I050 — Is the dust's own a0 suppression enough to unbind it?** DO: compute a0 at the
collapsed density and check whether MOND is off there. PASS: MOND switches off inside the
collapsing region. KILL: still on.

---

## E. a0(z), cosmology, CLASS

**I051 — CLASS with the corrected nu0 <= 2.36e-6.** DO: rerun the committed CLASS
comparison at the new nu0 ceiling and report the change in the TT spectrum. DATA:
`nbody_2026/stage76_nu0_recombination_pin_2026.py` as the template. PASS: within cosmic
variance. KILL: a visible shift.

**I052 — Does the RAR bound on nu0 survive per-galaxy Upsilon fitting?** DO: redo the nu0
bound using the ML pipeline rather than raw scatter. PASS: bound holds within 2x. KILL: it
moves by >5x.

**I053 — a0(z) against the MUSE measurement.** DO: compare the derived a0(z) at the new nu0
to the MUSE-DARK III result. DATA: `real_research/data/a0_of_z.csv`. PASS: consistent.
KILL: excluded.

**I054 — Growth of structure at the new nu0.** DO: recompute sigma_8 and the growth rate.
PASS: within 1 sigma of Planck. KILL: tension.

**I055 — The Lyman-alpha forest at the new nu0.** DO: recompute the forest suppression with
the corrected nu0 and Lambda_D/Q_0. PASS: within the WDM yardstick. KILL: excluded.

**I056 — Does a0(z) affect BBN?** DO: check whether a0 at BBN redshift is small enough to be
irrelevant. PASS: irrelevant. KILL: matters.

**I057 — a0(z) and the first galaxies.** HYP: the derived a0(z) makes early collapse faster
or slower; check against JWST high-z galaxy abundances. DO: compute the collapse-time ratio
at z = 6-15. PASS: a testable prediction. KILL: no difference.

**I058 — Is w = -1 exact at finite nu0?** DO: compute w(nu0) and its deviation from -1
today. PASS: |w+1| < 1e-3. KILL: larger.

**I059 — Dark energy equation of state vs DESI.** DO: compare the derived w(z) to DESI's
CPL constraints. PASS: consistent. KILL: excluded.

**I060 — Does the promotion change the CMB acoustic scale?** DO: check whether a0's presence
at recombination shifts the sound horizon. PASS: no shift. KILL: shift.

---

## F. Clusters and large scale

**I061 — The a0-bump, priced at the new nu0.** DO: recompute the bump amplitude. PASS: still
in [2.72, 4.46]x fiducial. KILL: outside.

**I062 — The eps^2 merger rider.** HYP: eta - 1 ~ eps^2 at 0.1-10% is a framework-specific
signature. DO: compute the predicted eta scatter and compare to the committed 0.1094 dex.
PASS: consistent. KILL: 2x too large (as an earlier estimate suggested).

**I063 — Does a0 locality help clusters?** HYP: cluster cores are dense, so a0 is suppressed
there — which makes the cluster deficit worse or better? DO: compute a0(rho) across a cluster
profile. PASS: helps. KILL: hurts (report either way).

**I064 — Cluster eta with the legal family.** DO: compute eta at R500 for s = 0.1-2. PASS: an
s fitting clusters. KILL: none.

**I065 — The Bullet cluster with the legal kernel.** DO: compute the lensing-dynamics offset.
PASS: consistent. KILL: excluded.

**I066 — Voids.** DO: compute the void profile prediction and compare to observations.
PASS: consistent. KILL: excluded.

**I067 — The external field effect across the SPARC sample.** DO: compute g_ext per galaxy
from 2MRS and test for the predicted EFE signature. DATA: `real_research/data/2mrs_catalog.csv`
plus SPARC. PASS: signature detected. KILL: null (this is already a committed null — confirm it).

---

## G. Empirical reanalyses

**I068 — Is the RAR scatter consistent with zero intrinsic?** DO: decompose the 0.108 dex
into measurement and intrinsic parts. PASS: intrinsic consistent with 0. KILL: significant
intrinsic scatter (constrains the kernel).

**I069 — Does the RAR prefer a0 constant or a0(rho)?** DO: fit both and compare BIC. DATA:
RAR json plus a per-galaxy density proxy. PASS: a0 constant preferred. KILL: a0(rho)
preferred (would be a major result).

**I070 — RAR residuals vs environment.** DO: correlate residuals with 2MRS local density.
PASS: no correlation. KILL: correlation (constrains the promotion).

**I071 — RAR residuals vs galaxy type/gas fraction.** DO: same with morphology. PASS: none.
KILL: correlation.

**I072 — The a0-line's gas-dominated slope, redone.** DO: refit with TLS and report a0 +/-.
PASS: consistent with 9.36e-11. KILL: not.

**I073 — Does the RAR distinguish s at high y?** DO: restrict to the highest-y SPARC points
and fit s there alone. PASS: s constrained. KILL: no leverage.

**I074 — Ultra-diffuse galaxies as a low-y probe.** DO: check whether UDG data constrain the
deep-MOND limit. PASS: consistent. KILL: tension.

**I075 — Dwarf spheroidals.** DO: same for dwarfs. PASS/KILL as above.

**I076 — The BTFR scatter as a kernel test.** DO: compute the predicted BTFR scatter for
different s. PASS: s constrained. KILL: no leverage.

**I077 — Rotation-curve shapes (not just the RAR).** DO: fit full rotation curves rather
than the RAR and check whether s is better constrained. PASS: yes. KILL: no.

**I078 — Solar-system: any existing anomaly consistent with the prediction?** DO: check
whether a constant sunward a0/2 could be hiding in current residuals. PASS: room exists.
KILL: excluded.

**I079 — Lunar laser ranging as a direct probe.** DO: compute the LLR signature of the
saturated anomaly. PASS: below sensitivity. KILL: excluded.

**I080 — Pulsar timing.** DO: same for binary pulsars. PASS/KILL as above.

---

## H. Reframings and alternative homes

**I081 — What if a0 is not fundamental but emergent from the dust profile?** DO: assume the
RAR is a consequence of a universal dust profile and derive what profile is needed.
PASS: a simple profile works. KILL: it must be fine-tuned per galaxy.

**I082 — TeVeS instead of AeST.** DO: check whether the legality obstruction applies to
TeVeS. PASS: TeVeS escapes it. KILL: same problem.

**I083 — Einstein-aether with c_2 != 0.** DO: check whether a small c_2 restores PPN validity
without breaking c_T = 1. PASS: a viable corner. KILL: none.

**I084 — A Horndeski/Galileon home.** DO: check whether a Galileon can host the a0-line with
Vainshtein screening. PASS: yes. KILL: no.

**I085 — Vainshtein rather than non-monotone screening.** HYP: the escape is a genuine
Vainshtein mechanism, which screens without breaking monotonicity. DO: check whether the
required Vainshtein radius is compatible with galaxies. PASS: compatible. KILL: not.

**I086 — Is the framework better read as a dark-matter profile than a gravity law?** DO:
convert the a0-line into an equivalent halo profile and see whether it is physically
sensible. PASS: a sensible profile. KILL: unphysical.

**I087 — Emergent/entropic gravity comparison.** DO: compare the a0 = kappa c sqrt(G rho_L)
normalisation with Verlinde's prediction. PASS: they agree/differ in a testable way.
KILL: no contact.

**I088 — What if kappa is not universal?** DO: test whether kappa varies with galaxy
property. DATA: SPARC. PASS: constant. KILL: varies.

**I089 — Is rho_Lambda the right density, or rho_total?** DO: redo the key fits on both
footings and report which the data prefer. PASS: a preference emerges. KILL: indistinguishable.

**I090 — a0 from the horizon at the galaxy's own epoch.** HYP: a0 should be evaluated at the
galaxy's formation redshift, not today. DO: test against SPARC with per-galaxy z. PASS:
improves the fit. KILL: worsens it.

**I091 — Is the DBI form necessary, or would any bounded K do?** DO: test three alternative
bounded K functions for the three properties (w=-1, dust, bounded). PASS: DBI unique.
KILL: others work.

**I092 — beta != 1.** DO: map the allowed beta range from the CMB off-switch plus the RAR.
PASS: beta = 1 preferred. KILL: a range.

**I093 — Q_0 pinned independently.** DO: find a second, independent determination of Q_0.
PASS: consistent with 0.0024-0.0146 Mpc^-1. KILL: not.

**I094 — Lambda_D pinned independently.** DO: same for Lambda_D. PASS/KILL as above.

**I095 — Is the dark-matter amount really an integration constant?** DO: check whether
anything in the theory fixes Omega_dm. PASS: it is fixed. KILL: free (confirms the non-claim).

**I096 — Dimensional analysis of a0 revisited.** DO: enumerate all dimensionally-correct
combinations of {c, G, rho_Lambda, H0, Lambda} giving an acceleration, and see how many land
within 20% of 9.36e-11. PASS: few. KILL: many (weakens the coincidence).

**I097 — Is the a0-Lambda coincidence statistically surprising?** DO: quantify it properly
with a stated prior. PASS: surprising at >3 sigma-equivalent. KILL: unsurprising.

**I098 — What does the framework predict that LCDM does not?** DO: list every prediction
where the two differ by more than current errors, with the number. PASS: at least one clean
discriminator. KILL: none.

**I099 — The cheapest falsification available today.** DO: rank all open predictions by
(discriminating power)/(cost to measure). PASS: a ranked list with the top three costed.
KILL: n/a — this one always produces output.

**I100 — Write the honest one-page summary of where the framework stands.** DO: read
`RETRACTIONS.md` and `nbody_2026/stage75_the_closed_theory_2026.py`, then write one page:
what passes, what fails, what is open, what is novel. No new computation. PASS: n/a — this
one always produces output.
