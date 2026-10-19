# Claude handoff for the analytic kinetic halo program

19 October 2026, America/New_York. Prepared at the user's request. Latest completed checkpoint: **ZAR-2026-10-19-08**. Repository HEAD when this handoff began: `e54c33252909e38a529a69f7adac265e37b54cb4`. The checkpoint ancestry and exact proof hashes are pinned in the linked JSON records; the repository is shared with concurrent work.

**The all-time confinement theorem requested below is still open. Do not report it as proved.** The nonlinear radial stability theorem, finite-time protection theorem, several exact obstructions and a bounded first-response calculation have been written and internally audited. The last attempt at full feedback was stopped when the user requested this handoff; it produced no new accepted result beyond checkpoint 08.

## User objective and resource boundary

Continue analytically toward a bound on the **full self-consistent energy transfer**, then all-time full spatial confinement for sufficiently small **strictly radial, genuinely nonstationary, canonical data** with:

- A fixed negative **initial** particle-energy cap independent of perturbation size.
- Exactly the original **initial** support. The latest work uses the stronger full phase-space support equality, not just equal spatial radii.
- Exact original species masses, fixed-L Casimirs and a positive bounded angular-momentum interval.
- Retained nonlinear stability, controlled density/force law and nonzero radial dispersion.

Do not silently substitute angular-current data, an added exterior population, a shrinking initial gap, a stationary state, or an assumed future work bound. A larger finite enclosing radius is allowed later. Requiring the entire old phase-space support to remain identical for all time is a different demand and forces stationarity in this canonical class.

The user explicitly requested **analytic work only** and to **leave Claude's ongoing calculations alone**. Codex ran no scientific scripts, simulations, numerical integrations, array analysis, or process inspection/control. Only small text/hash/document checks were used. Existing files and jobs were not modified. The repository contains extensive unrelated dirty/untracked work: do not bulk-stage, clean, reset or stop it.

## Read first

1. [Latest summary](real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/README.md) and [exact continuation](real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/AUDIT_AND_HANDOFF.md).
2. [Canonical labels and resonant first response](real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/RESONANT_WORK_PROGRESS.md). This is the nearest raw proof for the remaining feedback task.
3. [Canonical rigidity and support](real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/CANONICAL_RIGIDITY_AND_SUPPORT.md) and [finite-time protection](real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/FINITE_TIME_CONFINEMENT.md).
4. [Nonlinear coercivity](real_research/analytic_review_2026_10_18_codex/nonlinear_radial_2026_10_19/NONLINEAR_COERCIVITY.md) and [global flow/nonlinear stability](real_research/analytic_review_2026_10_18_codex/nonlinear_radial_2026_10_19/NONLINEAR_FLOW.md).
5. [Exact smooth warm equilibrium](real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md). The boundary geometry and flat cutoff come from here.

For exact revisions and modular review conditions, see the latest [CHECKPOINT.json](real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/CHECKPOINT.json). Earlier checkpoints and source/provenance records remain in the same research folder. The internal fresh-context audits are mathematical reviews, not external peer review or a formal proof certificate; check the raw arguments before extending them.

Packaging verified 75 artifact/input hashes, including all internal proof artifacts. One historical external status snapshot recorded by checkpoint 02 has since changed: `argon_push/ARGON11_nonlinear_fragmentation_2026-10-17/STATUS.md` (recorded `6d8a8e72fc34b678a936d2c5442075a8859d680e239679a310f7c640343ace21`, current `df7543b406fb3e0abad4e33a52f08788e4b6a793e770cf4185c03a0deace7db3`). That file was not edited or restored, and the historical pin was not refreshed. Re-read it before treating that old external status as current evidence.

## Model and conventions

Radial variables are r, radial velocity v, and **squared** specific angular momentum L. The phase measure is dGamma=4 pi^2 dr dv dL. There are separately conserved tethered/free populations, a positive fixed point baryon mass M_b, G>0 and a_0>0. Put c=G^2/a_0. The equations are

\[
\partial_t f_i+v\partial_r f_i+(L/r^3+a_i[f])\partial_v f_i=0,
\]

\[
a_t=-\frac{G(M_b+M_f)}{r^2}+\frac{cM_t^2}{r^4},
\qquad a_f=-\frac{G(M_b+M_t+M_f)}{r^2}.
\]

Potentials vanish at infinity. The reciprocal Hamiltonian and force derivation are in [KINETIC_PARTITION.md](real_research/analytic_review_2026_10_18_codex/KINETIC_PARTITION.md). This is the existing spherical deep-cubic, zero-stiffness effective model, not a full interpolation/covariant completion or new observational validation.

The equilibrium F_i(E_i^F,L) is bounded, smooth and compact, with E_i^F=v^2/2+L/(2r^2)+Phi_i^F(r), F_i,E<0 wherever occupied, and a fixed negative energy cap. Its support is a hollow shell r_0<r<R_F. On the law annulus M_t=fAr and M_f=(1-f)Ar, A=sqrt(a_0 M_b/G). It has genuine radial dispersion, positive on the closed law annulus and tapering to zero at the edges. The population fraction and amplitude are chosen, not dynamically selected.

Canonical initial data have f_i0=F_i composed with T_i0 inverse, with T_i0 symplectic in (r,v) at fixed L. Smooth generators compactly supported inside K_i=supp F_i give T_i0(K_i)=K_i and even f_i0=F_i near the support boundary while allowing nonstationarity.

## What is established

- **Exact smooth equilibrium:** checkpoint 04 removes the circular ridge while matching the target density exactly, retaining F_E<0, radial warmth and a finite boundary. This is a fixed positive-temperature construction; its cold limit is singular.
- **Nonlinear radial stability:** checkpoint 05 gives global classical flow and all-time smallness in X=sum_i int(1+v^2+L/r^2)|f_i-F_i|dGamma, with fixed positive angular gap and transported height bound. It controls cumulative masses, forces and integrated centered radial pressure, not every particle's outer radius.
- **Confinement criterion:** checkpoint 06 gives sharp exterior comparison launch caps. A common negative reserve at every repeated outward crossing suffices for an explicit uniform radius. This is a dynamical criterion; propagation from initial data is the open leaf.
- **Canonical finite-time protection:** checkpoint 08 uses conserved energy defect Delta H and exact canonical entropy to obtain epsilon_H=C_X(sqrt(Delta H/gamma)+Delta H/gamma) as an all-time X bound. With beta_0 the equilibrium energy gap, A_G=G(M_b+T+U), rho=ell/(2A_G) and Gamma=G/(2rho^2)+cT/rho^4, the full support stays within R_H=4A_G/beta_0 until T_H=beta_0/(4Gamma epsilon_H). The guaranteed interval grows like (Delta H)^(-1/2). This does not prove an all-time neighborhood.
- **Canonical rigidity:** global inverse-entropy convexity and the virial show that a radial canonical solution keeping both original density fields must be F. Exact old full-support invariance also forces F. A same-initial-support, fixed-gap canonical perturbation can immediately move the old orbital boundary; this is not an escape counterexample.

The law is controlled in cumulative-mass/force norm for disturbed solutions, not generally preserved as an exact pointwise density identity. Integrated centered radial pressure stays close. There is an all-time positive dispersion bound at any fixed radial resolution. Canonical connected positivity gives pointwise positive annulus dispersion on each finite time interval for each solution, not one universal all-time pointwise floor.

## The exact quantity still to control

Let S_i^t denote the actual flow and define the advected canonical energy label

\[
e_i(t,z)=E_i^F\bigl(T_{i0}^{-1}(S_i^t)^{-1}z\bigr),
\quad u_i=e_i-E_i^F,
\quad\psi_i=\Phi_i[f]-\Phi_i^F,
\quad\delta a_i=-\partial_r\psi_i.
\]

Then f_i=F_i(e_i,L) exactly, and

\[
(\partial_t+D_i^F)u_i=D_i^F\psi_i-\delta a_i\partial_vu_i,
\qquad
\frac d{dt}(\psi_i-u_i)(t,S_i^tz)=\partial_t\psi_i(t,S_i^tz).
\]

This avoids dividing by vanishing F_E. Since the occupied labels satisfy e_i<=-beta_0, a propagated bound on ||u_i||_infinity+||psi_i||_infinity below beta_0 would maintain a negative actual-energy gap and prove confinement. The existing X/energy theorem controls the potential, but not this uniform label displacement or its nonlinear gradients.

Equivalently, the exact work rates are

\[
\partial_t\Phi_f=G\int_r^\infty(j_t+j_f)s^{-2}ds,
\qquad
\partial_t\Phi_t=G\int_r^\infty j_fs^{-2}ds
-2c\int_r^\infty M_tj_ts^{-4}ds.
\]

Keep those signs/cancellations. Small X gives only an instantaneous O(epsilon_H) rate, hence O(epsilon_H t) under absolute integration. Fixed-radius current cancellation does not bound work evaluated on moving particles.

## Full feedback task

In equilibrium action-angle variables q=(J,L), theta, the linear equation is

\[
(\partial_t+D_i^F)h_i=F_{i,E}D_i^F\psi_i,
\quad D_i^F=\Omega_i(q)\partial_\theta,
\quad\psi=\mathcal P h.
\]

The physical shell kernels are P_ff=P_ft=P_tf=-G/max(r,r') and P_tt=2c int_max(r,r')^infinity M_Ft(s)s^(-4)ds. Their double angle averages K use the source action measure 2 pi C_Gamma dJ dL. The coupled Fourier Duhamel equation is

\[
h_{i,k}(t)=e^{-ik\Omega_i t}h_{i,k}(0)
+ik\Omega_iF_{i,E}\int_0^t e^{-ik\Omega_i(t-s)}\psi_{i,k}(s)ds.
\]

Checkpoint 08 bounds the field work formed from the **free first term only**. It uses coarea/Dini cancellation at actual resonances and actual-kernel k^(-3/2)(1+log k) summability. The source generator has a fixed finite nonzero angle harmonic set and compact eccentric support where grad Omega is nonzero; receiving actions are in a compact eccentric band. These bands exist near circular orbits inside the exact-law annulus.

**Next step:** bound the full actual feedback operator on the entire occupied action set. Its coefficients contain the fixed equilibrium F_E, so it is order one as initial amplitude tends to zero. A Neumann or resolvent argument needs a proved operator estimate, not merely small initial data. Source action bands are not invariant under feedback. Circular and flat support edges, possible discrete responses and nonlinear actual-path/label-gradient control remain separate obligations after the first-response bound.

## Pitfalls already resolved

- Canonicality does not remove the diagonal resonant numerator; the actual free-species diagonal kernel is nonzero.
- The smooth cutoff does not force an algebraic division failure for canonical data: use u instead of h/F_E. The issue is uniform propagation.
- An unchanged initial boundary collar does not keep the old orbital support invariant.
- Exact radial density invisibility cannot provide a nonstationary canonical family; the entropy/virial argument rules it out.
- The angular-odd L_z construction in checkpoint 07 is a real confined nonstationary sector with spherical density, but not a strictly radial canonical solution.
- The positive-Hamiltonian initially bound outer-shell example in checkpoint 07 is genuinely self-consistent, but changes masses/Casimirs, adds an exterior population, uses a broad angular interval and has a shrinking gap. It does not refute the requested class.
- Separate nearby homologous breathing was excluded; other radial breathing families have not been excluded.
- A finite-horizon neighborhood for every chosen horizon cannot be exchanged into one all-time neighborhood.

No full-feedback or all-time confinement claim has been accepted beyond checkpoint 08. Resume from the raw proofs and pinned revisions, not from a stronger interpretation of the summaries.
