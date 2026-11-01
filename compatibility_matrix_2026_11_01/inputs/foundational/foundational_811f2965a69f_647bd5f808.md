# Latest Claude work and one-shot theory closure attempt

**The theory is not finished.** The latest work supplies a useful calibrated picture and increasingly discriminating tests, but no inspected model jointly meets its own later tests or derives its halo/switch behavior from closed dynamics. This review also finds an exact law/certificate mismatch and a false universal exclusion. Neither is a reason to discard valid numerical results; both change which conclusions those results support.

Date: 28 October 2026. Checkpoint OSC28. Requested base: `44fd23a71c9888d9ea204c0ee832805829f9c090`; the review includes the subsequently committed FD1 result at `36b861cb7414dde9e39bdc2e9653facb620b1b01`. The shared checkout's eight pre-existing tracked modifications were preserved. All work from this review is under this directory, with no commits or publishing.

The [target contract](TARGET.md) defines completion. [RECENT_COMMITS.json](RECENT_COMMITS.json) inventories 562 commits since October 24, including 453 with Claude coauthor attribution. This is **not a claim to have rerun or line-audited all 562 commits**. Review depth is concentrated on the current theory statements, the latest calibration and subsequent-test lanes, their decisive scripts/results, and the mechanism dependencies. The specialist reports record exact inspected files and hashes. Old headline summaries are not treated as current evidence.

## 1. The substantive progress that survives

The CL2/CL3 result is real within its declared grading: selected canonical configurations pass the aggregate galaxy, group and cluster lines. CL3 reduces the chosen scalar settings from `(T,L)` to one concentration level by stipulating a crossover relation. It does not derive either the concentration level or why that crossover switches the governing force prescription. The concentration normalization remains external/unconverged, even when a native mass slope is used.

The subsequent tests expose information that the earlier aggregate scorecard misses:

| Test | Current result and practical meaning |
|---|---|
| X-COP cluster profiles, HO1 | Mean residual about −0.002 dex, but RMS 0.126 versus the 0.10 rule. Correct mean does not imply correct radial shape. |
| SLUGGS, HO2 | The graded treatment underpredicts by about 0.15 dex. Gas assumptions matter; it is not a universal halo exclusion. |
| Individual Local Group dwarfs, HO3 | Class medians hide excess object-to-object scatter, approximately 0.22–0.27 dex under the stated error model. |
| Milky Way, BS1 | The basin switch enables a solution only with wide baryonic priors; the standard comparison point still fails the rotation constraint. Other failures remain. |
| Hot-gas group comparison, HG2/GA1/DY1 | Negative measured contrast survives the specified gas and velocity audits; tested models predict positive contrast. Small samples and estimator/model uncertainty prevent treating it as a clean physical exclusion. |
| IC 1613, completed FD1 | Catalogue substitutions reduce the residual from −0.535 to −0.305 dex canonical. The frozen result still fails, but unresolved tracer geometry and unpropagated new input errors prevent reading its formal Z as a definitive physical significance. |

The detailed audit is [empirical/empirical_report.txt](empirical/empirical_report.txt). It also explains why LEE1's 10/24 pass count is local robustness in a box chosen after exploration, rather than a global trials correction or evidence against a competing theory. Repeatedly carrying the same failed alternative-footing lines into new lanes does not create independent evidence.

## 2. The most consequential correction: two different laws were called equivalent

The current P4/CL3 code uses the simple kernel `mu(x)=x/(1+x)`, hence

\[
g_N=\frac{g^2}{g+a_0}
\quad\Longleftrightarrow\quad
g^2=g_N(g+a_0).
\]

`V3_FULL_PICTURE.md` identifies that with

\[
g^2=g_N^2+a_0g_N.
\]

They are different equations. At `a0=g=1`, `gN=1/2`, the first holds while the second asserts `1=3/4`. The Lean affine-excess certificate proves the second law under its stated premise; it even contains a theorem distinguishing the simple kernel. Transferring that certificate, its Newtonian bound and its scalar external-field cubic to the first law is invalid.

The maximum difference between the fixed predictions is **15.47%**, or **0.06247 dex**. This is not a refitted likelihood difference. Existing numerical fits remain results for the law their code actually runs. The [foundations review](foundations/FOUNDATIONS_REVIEW.md) gives the correct dictionary, derives both stationary action kernels, and provides concrete replacement text retaining the executed simple-kernel model. It also specifies what would have to be rerun if the exact squared-excess law were adopted instead. Original theory files were not silently changed in this shared checkout.

The same review proves that covariance, dimensional conversion from Lambda, and the asymptotic galaxy limits leave a continuous family of kappa values. They do not select `kappa=1/2`. A predictive theory may legitimately fit kappa; the extra claim of deriving that coefficient is still unsupported.

## 3. A purported no-go is false, while a narrower obstruction is exact

DS1's claim that **no** `g_pred=F(g_bar)` can give HG2's negative contrast is too strong. The statistic compares residuals relative to a rising reference curve. Increasing absolute acceleration does not force an increasing residual.

An independent calculation on the saved rows reproduces measured `D=-0.2939827`. A positive, strictly increasing function `F(g)=A*g^0.1`, normalized to satisfy `F>=g` over that finite sample, gives `D=-0.2112794`, inside the stored interval. This is a counterexample to the universal statement, **not a viable replacement gravity theory**. The failures of CL2, GT1 and DS1 themselves are unchanged. See the [finite check](empirical/statistic_run/result.json).

Conversely, the adopted Burkert floor has an exact limitation. For a spherical halo **on** `rho0*r0=a0/(2*pi*G)`, its acceleration satisfies

\[
g_h\leq0.2544835656\,a_0
\]

regardless of core radius. The exact simple galaxy law demands a larger halo contribution whenever `gN/a0>0.08686849`. Therefore choosing the radius of a halo on this floor cannot make it identical to that law across accelerations. The [proof and normalization checks](necessary_conditions/RESULT.md) distinguish this obstruction from an empirical fit, a halo above the floor, a different profile, or an explicitly separate law branch. These qualifications are essential.

## 4. The dynamical closure attempt produces a useful reduction, not a finished theory

The October 27 multistream work makes a genuine advance: it constructs a positive distribution with finite moments and an exact logarithmic **inner equilibrium** pressure. Its own report correctly leaves the amplitude, formation mechanism and time-dependent closure open.

The new [mechanism derivation](mechanism/REPORT.md) tests whether that equilibrium can inherit the proposed fluid radiation/damping mechanism. For the stated nonrelativistic coupling class depending only on total density and current, the direct force contribution to the central random kinetic-energy equation cancels. Homologous admissible initial compression with zero heat flux gives `Dp/Dt=-5Hp`, while a fixed logarithmic material law requires `Dp/Dt=-3AH`. These disagree throughout the constructed exact-log inner region. Thus substituting that fluid pressure law into the kinetic evolution is not justified. Inhomogeneous forces can still generate transport later; this is not a no-go for eventual relaxation.

A constructive result survives. On a canonical kinetic homology ansatz for an isolated virialized self-gravitating system, the energy has the form

\[
E(a,\dot a)=\tfrac12 I_0\dot a^2+K_0a^{-2}-2K_0a^{-1}.
\]

The potential has a unique global minimum at `a=1` and diverges at collapse. A reciprocal damping model returns negative-energy trajectories to that minimum. This improves the reduced stability picture and is checked with an explicit energy ledger. The outlet is imposed at the collective-coordinate level; it has not been derived as the projection of the complete spatial tracker/mediator system. The homology family is also not invariant under the full kinetic equation for the constructed halo. Thus this reduction does not prove halo formation, nonlinear stability, the force-law switch, or vacuum normalization. The report states the full-equation residual and the missing implication.

## 5. IC 1613 can be pursued with a concrete target

A published stellar-tracer study exists beyond FD1's catalogue substitutions: [Taibi et al. 2024, exact v2, section 6.2](https://arxiv.org/html/2402.01631v2). Its conditional circular-speed estimate can be turned into a precise requirement without regrading FD1.

Under the isolated spherical simple law,

\[
M_b(<r)=\frac{v_c^4}{G(a_0+v_c^2/r)}.
\]

For the source's central values, the inferred required enclosed baryonic mass is **3.92 million solar masses canonical / 3.27 million alternative**. FD1's half-stellar-mass convention gives **35.25 million solar masses** before gas. Reconciling those inputs would require a different resolved baryon/kinematic model or a material modification of the isolated-law assumptions. This comparison is conditional, not a significance or an exclusion: inclination, geometry, tracer populations, non-equilibrium behavior and external fields have to be modelled together. [The source record and calculation](necessary_conditions/RESULT.md) give the exact assumptions and uncertainty rectangle.

A small FD1 prose correction is also needed: its 13 km/s rotation term changes the log residual by **+0.17113 dex**, not +0.06 dex. Its main output table is consistent. Retaining the historical formal errors after changing mass, gas and rotation does not propagate the new uncertainties.

## 6. What remains to finish

The immediate inexpensive correction is to version the exact law and separate its valid proofs from those of the other kernel. Retaining the currently executed simple law is the least disruptive documentary repair; switching kernels would require new numerical work.

The actual scientific continuation needs one model that supplies all of the following together:

1. Conserving field/kinetic dynamics, with explicit initial data and a valid multistream treatment.
2. A physical reason for the environmental switch and the halo profile, with a declared calibration policy for kappa, abundance, concentration and other inputs.
3. A common forward prediction of galaxy dynamics, vertical forces, dwarf tracers, lensing and cosmic growth, including uncertainties and selection.
4. Converged numerical predictions and joint testing on the previously failed systems.

Deriving one concentration number tomorrow would not remove the later-test failures. Finding a better halo fit would not supply an evolution law. The constructive kinetic reduction is a useful starting point, but its next step is full kinetic/mediator evolution with a controlled perturbation and a derived heat-flux response; replacing that response by the desired equation of state would repeat the gap just identified. Resolved IC 1613 modelling is a separate empirical continuation, not a substitute for dynamics.

These routes remain open. None of the present results proves the entire framework impossible, and none justifies calling it complete. The [handoff](HANDOFF.md) records exact next implications and deferred work.

## Verification scope

The new work includes four bounded computation records: the independent group statistic, the law/action dictionary, the kinetic composition/reduction check, and the Burkert/mass-inversion diagnostic. Each has a contract, explicit limitations, software versions, input hashes and output hashes. [VERIFICATION.json](VERIFICATION.json) records the final checks and the actual scope of review. Historical numerical likelihoods and large simulations were inspected at decisive points, not rerun. Existing Lean files were read, not recompiled. The specialist reports and separate proof reviews distinguish direct derivations, finite computation and source-dependent inferences.
