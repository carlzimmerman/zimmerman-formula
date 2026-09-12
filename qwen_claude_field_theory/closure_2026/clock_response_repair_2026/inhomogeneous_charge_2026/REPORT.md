# A constructed inhomogeneous slice, its stability failure, and the L194 check

2026-09-12. Started from live `738773278`; concurrent Claude commit `9212f4498` added L194 without changing the pinned action. **The requested complete relativistic gravity theory is not closed.** This continuation did construct nonuniform initial data of the unchanged action, including the clock-preserving lapse, and then tested it. The tested data fail scalar stability. No late-time galaxy-depletion evolution was promoted past that failure.

## 1. What was actually constructed

Use the same action as the preceding audit,

\[
S=\int d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
+P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi\right]+S_m[g,\psi],
\]

where \(X=-\nabla\chi\cdot\nabla\chi\), \(s=\sqrt{-\nabla\tau\cdot\nabla\tau}>0\), and \(Y\) is the squared clock-projected gradient. All numerical coefficient functions are unchanged. The source's existing gamma corrections are retained; gamma=1e-6, M²=1 and Lambda=.7 in its dimensionless convention. These numbers do not constitute a physical calibration of galaxies or recombination.

The [constraint construction](constraints/REPORT.md) takes an initially flat spatial slice, plane symmetry, positive-expansion extrinsic curvature \(K_i{}^j=\mathrm{diag}(k,h,h)\), \(D_x\chi=b(x)\), spatially uniform physical \(Q=n\chi\), and aligned clock \(\tau=t\), so \(s=1/N\). Comoving baryons and radiation supply ordinary matter. Let \(C=W_Y+2b^2W_{YY}\). Action variation and the Einstein geometry give

\[
M^2(2kh+h^2-\Lambda)
=2P_XQ^2-P+V+\rho_m
+2\gamma[(Q^2-b^2)b'-Q(Q^2-b^2)k-2Q^3h],
\]
\[
-2M^2h'=2P_XQb-2\gamma b[(Q^2-b^2)k+2Q^2h],
\]
\[
V_\tau-P_\tau+W(k+2h)-2W_Ykb^2-2QC b'=0.
\]

The first and third equations solve for \((k,b')\); the second gives \(h'\). Spatial Einstein equations and the original scalar equation determine the instantaneous normal accelerations. Requiring preservation of the clock constraint then gives the **derived**, linear lapse equation

\[
\boxed{FN''+(F'+4QbW_Yh)N'+a_0N+f_0=0,
\qquad F=W-2Q^2C-2b^2W_Y.}
\]

Here \(a_0,f_0\) label lapse-ODE coefficients, **not the MOND acceleration scale**. Their complete expressions are generated from the action and archived; neither is reconstructed to fit a chosen solution. This was a finite-interval central initial-value solve in x, not an asymptotic boundary-value solve for an isolated galaxy.

Three runs cover x in [-.5,.5]: a homogeneous control; uniform matter with b(0)=.009; and a Gaussian baryon overdensity .0001 exp[-(x/.3)²] added to background baryons .001 and radiation .01, with b(0)=0. Physical Q=.907832150577 differs from the stored coefficient reference qbar=.909090909091. No extra matter species is introduced.

All three runs satisfy the solved constraints and clock preservation with positive lapse. Orthogonal checks include the scalar equation using a directly reconstructed Ricci tensor, fourth-order spatial finite differences, actual-coefficient temporal differences of the clock constraint, reflected-gradient invariance, and tighter integration. State refinement changes are below 5.81e-13; independent spatial derivative residuals are below 8.61e-12; the finer clock-preservation difference is below 8.02e-12. These are numerical evidence, not interval-certified existence or nonlinear constraint-propagation proofs.

The nontrivial runs **fail the next gate**. Their full-cubic longitudinal quarter-discriminants \(\Xi=B^2/4+KG\), evaluated on the solved instantaneous Hessians, are:

| Initial patch | Xi range over 101 sampled points |
|---|---:|
| Uniform-matter finite gradient | [-5.59308e-4, -3.68913e-5] |
| Gaussian baryon overdensity | [-.00741482, -.00740135] |

These are actual constrained initial jets, unlike an arbitrary gradient pasted onto FLRW, but they are not a finite-time spacetime solution. One negative scalar direction is enough to fail this stability gate. No stable all-angle spectrum is inferred from two sampled directions, and no universal profile search is claimed.

## 2. Where its charge initially goes

The [independent action-current derivation](current/REPORT.md) gives

\[
J^\mu=-2(P_X+\gamma\Box\chi)\nabla^\mu\chi
+2sW_Y h_\tau^{\mu\nu}\nabla_\nu\chi-\gamma\nabla^\mu X,
\qquad \nabla_\mu J^\mu=0.
\]

On the uniform-Q initial patches,

\[
J^n=2P_XQ+2\gamma[Qb'-(Q^2-b^2)k-2Q^2h],
\quad J^x=2b(sW_Y-P_X)+2\gamma b[H_{nn}+Q(k+2h)].
\]

Continuity therefore fixes the instantaneous box-charge rate per transverse coordinate area as the left endpoint \(NJ^x\) minus the right endpoint \(NJ^x\). It includes the evolving spatial volume measure, not just a time derivative of the local density.

- Uniform-matter gradient: box charge .09707980422, instantaneous loss rate -3.208068e-5.
- Gaussian overdensity: box charge .09717242348, instantaneous gain rate +4.719312e-6, with inward flux at both endpoints.

The homogeneous comparison is .09717242386. Fixing Q to the background value does **not** fix the global conserved charge. Global charge matching and an FLRW exterior were not imposed on these finite patches. The Gaussian example gives inward, not outward, initial flow; neither example supports a long-time dust-depletion prediction because it is unstable. No galaxy mass-dependence or cluster/galaxy separation has been demonstrated.

The spherical audit also avoids an overstrong no-go. For a regular source-free center, outward flux is \(-\partial_t C(<r)\). Only actual charge stationarity forces zero net outward flux; a static metric does not, because the coefficients depend explicitly on clock time. Cubic zero-flux branches need not have zero spatial gradient. One small-radius timelike witness has nonzero gradient and vanishing instantaneous radial current, but negative charge density and nonzero time derivative. Its exact center relation is \(J^t(0)=Q[3W_Y(0)-P_X(0)]\), approximately -.0349700 for this frozen test slice. It is not stationary positive-charge Einstein data.

## 3. A localized repair cannot keep this unstable late-time exterior

The [exterior computation](exterior/REPORT.md) evaluates the original sourced physical state, including the FLRW Hessian, the full gamma-dependent coefficients, and Einstein feedback. At its first stored epoch a=1,

\[
K=2.18438106049>0,\quad G=-.00339447314151<0,
\qquad \boxed{c_s^2=G/K=-.00155397480911.}
\]

The reduced scalar principal form \(K\omega^2-G|\mathbf k|^2\) is definite, not a tilted real propagation cone. This concerns the propagating scalar factor; tensor characteristics remain null and the auxiliary clock still has its distinct elliptic constraint. The exceptional k=0 reduction is not being certified here.

An independent calculation of the existing six-state constrained transfer matrix gives growing eigenvalues divided by physical k/a approaching .0394204872 as k rises from 100 to100000, matching \(\sqrt{-c_s^2}\). Its high-k solve has recorded conditioning limitations. Decimal arithmetic confirms the sign of rounded jets but does not upgrade the background to an exact interval-certified solution.

The exact conditional statement is stronger than those finite samples: **if a localized configuration's complete regular principal coefficients converge along a ray to a negative limiting quarter-discriminant, it cannot have real scalar characteristics everywhere.** Complete convergence includes the covariant scalar Hessian and the clock/metric data; gradient decay alone is insufficient. This follows from continuity and square completion and is formalized in `AsymptoticCone.lean`.

Other earlier archived epochs have positive scalar speed squared and are not excluded by this particular argument. Nor does it exclude different asymptotics, a globally altered statistical gradient state, or every solution of the action. It excludes a healthy localized cure that retains this specific unstable late-time exterior, conditional on the stated asymptotic mapping and numerical exterior sign.

## 4. Concurrent Claude L194: reproduce the useful result, test the missing implication

L194 (`9212f4498`) proposes the variance-rate closure

\[
\frac{d\ln Y}{d\ln a}=-2+2\kappa_k\sqrt{-c_s^2(Y)},
\qquad \kappa_k=k_{\rm physical}/H,
\]

on its negative-c² branch. This kappa is unrelated to Zimmerman's acceleration coefficient. The [tracking audit](tracking/REPORT.md) executes the original pure functions without overwriting Claude's results. Its finite-mode ODE attraction is a useful reproducible property of that **assumed approximation**.

But at its fixed point the signed relation is

\[
\boxed{c_s^2=-\kappa_k^{-2}<0,\qquad |c_s|k_{\rm physical}=H.}
\]

An added mode with \(\kappa_{\rm new}>\kappa_k\) has positive initial log-variance rate \(2(\kappa_{\rm new}/\kappa_k-1)\). The bounded audit seeds such a mode and tests its invasion. The closure has not derived an ultraviolet cutoff from this action. Its global statistical-background proposal is outside the preceding localized-exterior theorem, but is not established as a solution of the covariant equations.

There is also a nonuniform approximation issue: at balance, the presumed fluctuation growth time is Hubble-scale, so expansion/friction and coefficient-rate terms need not be small merely because k/H is large. As an explicitly labeled approximation control, a mode equation \(\sigma_{NN}+\nu\sigma_N-\kappa_k^2u^2\sigma=0\) with N=ln a requires \(\kappa_k^2u^2=1+\nu\), rather than1, when \(Y\propto e^{-2N}\sigma^2\) is stationary. This is not a replacement gravity model or a derivation that nu=3 for the full action. It shows the omitted terms can affect the claimed balance at leading order. `TrackingBalance.lean` certifies these signed-balance, added-mode and drag-control implications.

Consequently the L194 result does not yet establish the action-derived tracking mechanism, a controlled continuum limit, or a Lyman-alpha transfer/hydrodynamic pass. Its nonlinear averaging and finite-gradient sound-speed prescription remain derivation obligations. No empirical forest bound is independently certified in this checkpoint.

## Status and the remaining calculation

**Constructed:** bounded nonuniform full-action initial patches with clock preservation and calculated currents. **Failed:** their local scalar stability gate. **Conditionally excluded:** a healthy localized cure retaining the identified late-time exterior. **Not established:** globally charge-matched, stable cosmology-to-galaxy evolution, or a completed relativistic MOND theory.

The next physical obligation is a healthy cosmological/background state from this same fixed action, rather than evolving the unstable slices. If pursuing L194's genuinely different statistical exterior, derive its covariance/mode-coupling equations, retained expansion terms and short-distance control from the action, solve the corresponding Einstein/clock constraints, and test the resulting principal system. The finite-mode rate ansatz alone is not that calculation. No coefficients were retuned to force a pass, and none of the old CMB, lensing, PPN, exact-MOND or full nonlinear degree-count gates is upgraded here.

Nine scoped Lean lemmas compile with only standard logical axioms and no sorry/custom axioms. They formalize the exact implications above, not empirical truth or every action equation. The research and computation-audit skills kept these proof obligations separate from numerical evidence; independent proof review and mathematical self-review checked the new derivations and scope. Carl Zimmerman's conserved-clock/redistribution direction motivates the construction; Claude's L194 motivates the separate tracking check. No global novelty priority claim is made.

See [files](FILES.md), [commands and exit status](COMMANDS.md), and the four linked subreports for reproducibility and all limitations.
