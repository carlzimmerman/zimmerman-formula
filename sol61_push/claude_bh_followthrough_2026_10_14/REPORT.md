# Follow-through on Claude's new black-hole/dark-energy branch

2026-10-14. Read directly: CFG775 source, results, frozen criteria, README and both post-result addenda. Source-result checkpoint8a7634027, narrowed amount interpretation8a817615f, source-history correctione20f1767d. The current work here changes no Claude result or sealed prediction.

**Main advance:** the conserved BH-source comparison separates a vacuum-density mechanism from a genuine event-horizon mechanism. They predict opposite acceleration-scale evolution. A second exact result shows how cold matter could share the conversion budget without altering the expansion history, while changing the surviving baryon/cold ratio. The calculation does not supply the microscopic conversion interaction.

## What Claude actually added

CFG775 re-expresses the geometric ratios through q=a0/(cH_Lambda). Its source branch integrates star formation weighted by a^-3 to build vacuum density. The initial claim that the amount was excluded was subsequently narrowed to stellar remnants alone. Its second addendum recognizes that the literature fit uses a different high-redshift history and an approximately doubled low-redshift normalization. Thus the pure MD14 amount calculation is not an exclusion of every accreting coupled-BH model.

The primary source, [Croker et al.2405.12282v3](https://arxiv.org/html/2405.12282v3), explicitly includes baryon depletion and solves the background expansion with it. Its fitted Trinca history is not available as a numerical input here, so no reproduction of its Xi~1.4 or likelihood is claimed. The source conversion is phenomenological and background-level; it does not establish a local horizon-mediated action.

## 1. The stronger geometric result: density and event horizon move oppositely

The project law is

\[
a_\rho=\kappa c\sqrt{G\rho_V}
=\alpha c^2/L_V,\quad
L_V=\frac{c}{\sqrt{8\pi G\rho_V/3}},\quad
\alpha=\kappa\sqrt{3/(8\pi)}.
\]

For true de Sitter geometry L_V is the horizon radius. For a matter-filled universe producing vacuum, it is an auxiliary curvature length. The ACTUAL future event horizon is

\[
R_E(t)=ca(t)\int_t^\infty\frac{dt'}{a(t')}.
\]

If positive pressureless matter transfers energy into pure vacuum while total stress-energy is conserved,

\[
\dot H=-4\pi G\rho_m\le0,\quad
R_E\ge c/H,\quad \dot R_E=HR_E-c\ge0.
\]

Vacuum production increases sqrt(rho_V), while 1/R_E decreases. Therefore a_rho and a_E=constant*c²/R_E cannot be the same evolving mechanism with constant coefficients. This conclusion does not depend on MD14 or a fitted source normalization. The [complete argument](HORIZON_TREND_PROOF.md) states the finite-future-horizon and matter assumptions and the de Sitter limiting case. It does not cover arbitrary modified-gravity backgrounds or extra matter violating these energy conditions.

The same distinction applies to a Hubble/apparent-horizon acceleration cH: H decreases in this model. The density-only scale is proportional to H_Lambda=sqrt(8piG rho_V/3), which increases. These are different functions of time. The dictionary q=alpha can still refer to H_Lambda, but that does not make it a physical evolving-horizon derivation.

## 2. One conserved numerical history, not an extra integral on fixed expansion

Use N=ln a and densities normalized to a reference h=.70 critical density. Let B=a³rho_b/rho_ref, C=a³rho_c/rho_ref, and V=rho_V/rho_ref. Adopt the assigned projected matter .308 and primordial ratio C/Bi=5.364. With the same MD14 psi used by Claude,

\[
E^2=H^2/H_{ref}^2=(B+C)e^{-3N}+V,
\quad J=\frac{\Xi\psi}{\rho_{ref}H_{ref}E},
\quad B'=-J,\quad C'=0,\quad V'=Je^{-3N}.
\]

Start at z8 with V=0 and shoot Xi so E(today)=1. The flatness condition then determines today's V together with depleted matter; it is not simultaneously fixed to .692. Radiation and neutrino details are omitted in this late-time assigned comparison. Source-start15 and30 are sensitivity tests, not new high-redshift observations.

Primary result:

| Quantity | Conserved MD14 comparison |
|---|---:|
| Xi, total converted mass / source stellar mass | 4.71576 |
| Omega_b, projected before conversion | .0483972 |
| Omega_b, surviving today | .0208457 |
| Omega_c, conserved | .2596028 |
| Omega_V today | .7195515 |
| Baryon survival | .430721 |
| Cold/surviving-baryon ratio today | 12.4535 |
| Source-weighted mean a^-3 | 26.1166 |

These numbers are outputs of the stated diagnostic, not measured depletion or a new fit. They differ from the Trinca-history model by construction. A normalization change psi->2psi gives Xi->Xi/2 exactly and leaves depletion, expansion and normalized acceleration history unchanged. Only a source-SHAPE change, or other cosmological input, changes those predictions. Thus the normalized MD14 rescaling alone cannot reproduce the full Trinca model.

Independently integrated budgets give

\[
D=B_i-B_0=\frac\Xi{\rho_{ref}}\int\psi\,dt,
\quad V_0=\frac\Xi{\rho_{ref}}\int\psi a^{-3}dt,
\quad V_0/D=\langle a^{-3}\rangle_{conversion}.
\]

This is the exact bookkeeping link between vacuum density and consumed primordial matter in this source prescription.

## 3. Actual horizon calculation and a large discriminating prediction

Continue the assumed source into the future using MD14 as a specified extrapolation. Integrate the event horizon to a=exp12 and add its asymptotic de Sitter tail. A second calculation uses scale factor a directly, a different integrator and a different cutoff; it also verifies dR_E/dln a=R_E-c/H. The results agree to the declared1e-8 tolerance.

Both proposed force scales are normalized to their own value today, isolating the time dependence. This comparison does not independently fix either coefficient.

| Redshift | Density law sqrt(V/V0) | Event-horizon law R_E0/R_E(z) | R_E, Gpc |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 4.8337 |
| .5 | .9932 | 1.0767 | 4.4896 |
| 1 | .9703 | 1.1833 | 4.0850 |
| 1.5 | .9219 | 1.3070 | 3.6983 |
| 2 | **.8499** | **1.4399** | 3.3569 |
| 2.5 | .7671 | 1.5778 | 3.0636 |
| 3 | .6853 | 1.7184 | 2.8129 |

At z2 the branches differ by a factor1.694, or .229dex in a0. In the deep BTFR limit Vflat scales as a0^(1/4), so the velocity difference at fixed baryonic mass is about14.1%. This is a model-branch prediction, not a significance estimate or a substitute for inclination, pressure-support and baryon-mass uncertainties in actual galaxies.

Source-start15/30 gives density ratios .8685/.8760 and event ratios1.4428/1.4439 at z2: the opposite directions survive this sensitivity test. Switching all future source production off after today preserves the entire past density history but changes the event horizon; at z2 the normalized event ratio is1.44036 instead of1.43992. This demonstrates its future dependence without suggesting the modest difference is presently measurable.

At the assumed onset of production z8, V=0 while R_E=1.5357Gpc and the today-normalized inverse-horizon scale is3.1476. A future horizon can exist before the first BH source in this model. It cannot be identified with the local vacuum curvature length at that epoch.

The conditional geometric-mean identity remains

\[
r_M/\sqrt{r_gR_E}=\left[2a_\rho R_E/c^2\right]^{-1/2}.
\]

Its coefficient is1.7387 today and2.2632 at z2 in the numerical history, tending to the familiar1.7013 only at the de Sitter limit. The constant1.7013 identity uses L_V instead of R_E. This is the precise correction required when moving from static horizon analogies to the sourced cosmology.

## 4. Bringing the cold component into the conversion budget

If BH-associated production consumes only baryons, the primordial cold-to-baryon ratio does NOT stay fixed. Generally

\[
R_{cb}(t)=\frac{R_{cb,early}}{s_b(t)}
\]

when cold comoving mass is conserved and sb is the surviving baryon fraction. Even sb=.70 would give7.663 rather than5.364. This does not assign every galaxy the global ratio; a late baryonic catchment requires a source and assembly/depletion mapping before using a primordial supply ratio.

There is a constructive extension of the background accounting. Divide the same total comoving loss D between baryons and cold matter with a constant transfer ratio eta=Qc/Qb:

\[
B=B_i-D/(1+\eta),\qquad
C=C_i-\eta D/(1+\eta).
\]

The sum B+C=Bi+Ci-D, V and the expansion history are unchanged. Thus background expansion alone cannot tell whether vacuum production consumed baryons, cold matter or both, for the same total source.

| Source partition, same primary expansion | Baryon survival | Cold survival | Cold/baryon today |
|---|---:|---:|---:|
| Baryons alone | .43072 | 1 | 12.4535 |
| Proportional cold and baryon conversion, eta=5.364 | .91055 | .91055 | 5.3640 |
| Cold alone | 1 | .89387 | 4.7947 |

Keeping the primordial ratio fixed requires equal FRACTIONAL depletion, Qc/C=Qb/B; proportional transfer eta=Ci/Bi is sufficient. This is an additional interaction hypothesis, not a result of horizon geometry, a derivation of5.364, or a capture-rate calculation. Its role is to show a concrete mass-conserving way to couple primordial cold supply to late vacuum production. It is a different model from the published baryon-only case. It must predict the partition from a physical coupling and survive abundance, clustering and baryon inventory tests; fitting H alone cannot do that.

## 5. The local action must do more than the background source equation

If a vacuum sector is EXACTLY T_V^mu_nu=-V delta^mu_nu, its transfer covector obeys

\[
Q_\nu=\nabla_\mu T_V^\mu{}_\nu=-\partial_\nu V,
\qquad\partial_{[\mu}Q_{\nu]}=0.
\]

In a homogeneous rest frame Q0=-S(t), Qi=0 is consistent. Assigning a localized BH source S(t,x) while keeping Qi=0 generally is not: the mixed derivative requires spatial derivatives of S to vanish. The exact test S=S0(1+delta cos kx) gives a nonzero transfer curl. A gradient completion V=tS(x) makes the curl vanish but introduces Qi=-t partial_iS, which must enter the matter momentum equation with the opposite sign.

Thus local conversion into an exactly homogeneous pure vacuum is not supplied merely by naming BHs as a source. A transport/gradient sector, compensating spatial momentum exchange or an explicitly nonlocal/coarse-grained rule is needed. This does not refute the published background model, which is not a completed inhomogeneous action. A real mediator can carry energy while not being pure vacuum; its stress and eventual vacuum-production interaction must be counted.

Likewise point particles with m proportional to a^k still have pressureless particle stress, but their continuity equation contains a source kHrho. Rewriting this as an effective w=-k/3 does not alone derive the negative-pressure stress or make the local gravitating mass disappear. A non-dust interior or averaging construction must provide that step. The present calculation treats the phenomenological vacuum sector as assumed, not derived from variable-mass dust.

## Result and remaining decisive implication

Claude's new source history can be advanced to a conserved cosmology with explicit baryon and cold budgets. The most consequential new discriminator is exact under the stated model assumptions: a growing vacuum-density force scale cannot also be a constant-coefficient inverse-event-horizon scale. At z2 the assigned branches are .850 versus1.440, large enough to define a materially different high-redshift prediction rather than another geometric coincidence.

The cold component can participate in the same total transfer without changing H, but its partition is a new testable physical input. The missing mechanism is now sharply specified: a local/covariant or explicit nonlocal BH-associated interaction that derives the conversion partition, accounts for spatial momentum/transport, and determines which density or horizon scale enters the tether action. None of these equations derives the microscopic carrier, fitted kappa, supply capture or a halo formation attractor.

Evidence:67 joined-model checks,24 independent horizon checks and27 partition checks, total118. All manifests validated. Refinement to1e-12, independent integration coordinate/method, source quadratures, positive remaining stocks, future-source control and source-normalization control passed. No likelihood or large simulation, no publication, no messages to Claude, and no changes to existing frozen predictions. The analytical theorem is self-reviewed; no novelty or independent-person replication claimed.
