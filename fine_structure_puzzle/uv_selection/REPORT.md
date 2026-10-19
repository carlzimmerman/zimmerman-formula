# FSP-U: genuine UV predictivity and the inverse Yukawa test

**Result:** no derivation of alpha(0). There is a useful conditional mechanism: a fully interacting two-U(1) fixed point fixes the complete Abelian kinetic matrix relative to a specified charge lattice, leaving its magnitude dependent on a gravity coefficient. A mass-correlation test can eliminate that coefficient in a reduced model. The actual inverse test below predicts a hypercharge value 12.8% below a held-out reference; its assumptions do not cover the current full-flavor UV branch. This strengthens the map of what must be calculated rather than ruling out UV prediction.

Scope and provenance: new work only under `uv_selection/`; input FSP-000 at Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, pre-existing dirty baseline. Read-only old inputs and SHA-256 hashes are in INPUT_PROVENANCE.json. Source equations are pinned in source_equations.json; exact versions and claim-level source checks are in SOURCES.md. No measured alpha is promoted to a prediction.

## 1. The coupled candidate

The selected candidate is [Carone, arXiv:2512.12044v1](https://arxiv.org/html/2512.12044v1), Tables I-II and Eqs. (3)-(18), published in February 2026. Its new feature relative to the old lane-B scalar analysis is correlated kinetic mixing. The source uses one-loop MSbar matter flows with a universal gravity term parameterized by f_g; it does not determine f_g from gravity. The numerical fhat=1.5473 example is calibrated through its hypercharge boundary. We use it only as an arithmetic benchmark, never a prediction.

Use canonical gauge fields A and a declared fixed rational charge lattice:

\[
D=\partial-iq^TGA,\quad q=(Y,X)^T,\quad Q=T_3+Y,
\quad G=\begin{pmatrix}g_Y&\widetilde g\\0&g_x\end{pmatrix},
\quad H=GG^T,\quad K=H^{-1}.
\]

Charges and scalar content are exactly those in the source tables, including three right-handed neutrinos and a complex scalar phi with charges (0,1). The integer units can be taken as 6Y and 3X; they are coordinate choices, not tunable charge normalization. A fixed invertible change q'=S q sends B'=S B S^T and H'=S^{-T}H S^{-1}, leaving physical norms invariant.

The charge-trace matrix is independently summed here:

\[
B_{ab}=\frac23\sum_{\rm Weyl}q_aq_b+
\frac13\sum_{\rm complex\ scalar}q_aq_b,
\]

\[
B_{B-L}=\begin{pmatrix}41/6&16/3\\16/3&11\end{pmatrix},
\quad\det B_{B-L}=841/18;
\qquad
B_\chi=\begin{pmatrix}41/6&-2/9\\-2/9&497/27\end{pmatrix},
\quad\det B_\chi=20369/162.
\]

Both are positive definite. Let F=16 pi^2 f_g>0 and t=ln(mu/mu0), relative to a fixed reference mu0. The source's three triangular-coupling beta functions, after converting g1=sqrt(5/3)gY, satisfy the exact identity

\[
\dot H=\frac{1}{8\pi^2}(HBH-FH).
\tag{U1}
\]

This identity is verified against an independent charge sum, not obtained by fitting coefficients. It remains conditional on the phenomenological one-loop + universal-gravity truncation. Higher matter loops, nonminimal terms, backreaction, or distinct gravity vertices can change U1.

## 2. What is fixed, and by what condition

For invertible H, U1=0 implies BH=F I. Thus the **unique full-rank matter fixed point** at fixed F and B is

\[
H_*=F B^{-1},\qquad K_*=B/F.
\tag{U2}
\]

The uniqueness is within this branch; it is not uniqueness of all UV completions. Linearization gives

\[
\delta\dot H=2f_g\,\delta H.
\]

All three matter stability eigenvalues are +2f_g and the critical exponents theta=-eigenvalue are -2f_g. They are UV-repulsive/irrelevant and therefore predictive after a gravity trajectory is supplied. These are matter eigenvalues at fixed F. A full gravity-matter stability matrix may mix these directions with relevant gravitational parameters; U2 alone is not that full calculation.

In triangular coordinates the exact conditional fixed-point ratios are

| Model | gY*^2/F | gx*^2/F | tilde-g*/gx* |
|---|---:|---:|---:|
| B-L | 6/41 | 123/841 | -32/41 |
| chi | 6/41 | 1107/20369 | 4/123 |

At F=1.5473 they reproduce the source's rounded (gx,tilde-g) benchmarks (0.4757,-0.3713) and (0.2900,0.0094). No calibration to these numbers enters the derivation of the ratios.

There is also a continuum. Set X=B^(1/2) H B^(1/2)/F. Then

\[
\dot X=2f_g(X^2-X).
\tag{U3}
\]

The real symmetric fixed points are orthogonal projectors. Rank one gives an angular family: in triangular variables gY*=0 and (gx*,tilde-g*) lie on the source's ellipse. The angular eigenvalue is zero; the other triangular-coupling eigenvalues are -f_g and +2f_g. The -f_g hypercharge direction is relevant/free. Linearization in H instead has -2f_g for its vanishing eigenvalue, because H is quadratic in the coupling at that rank boundary; one must not compare the singular coordinates as if they were a nonsingular variable change.

For any 0<c0<1,

\[
c(t)=\frac{c_0}{c_0+(1-c_0)e^{2f_gt}},
\quad X(t)=P+c(t)(I-P),\quad P^2=P,\quad\operatorname{rank}P=1,
\tag{U4}
\]

solves U3 and approaches the **interacting** rank-one endpoint P. Thus demanding some interacting matter fixed coupling still leaves a continuous finite-scale gauge matrix. More generally 0<X(0)<=I is the UV-finite positive cone in this exact truncated flow, because each eigenvalue obeys the scalar U3 equation; eigenvalues above one produce a finite-t Landau singularity. Requiring the full-rank endpoint X=I, rather than merely UV completeness/asymptotic safety, is the condition selecting U2. This is a uniform analytic argument, with a symbolic identity check as backup.

## 3. Physical photon matching removes an apparent shortcut

When phi condenses, its charge (0,1) leaves the generator n=(1,0) unbroken. The coefficient of the surviving massless pole is determined by

\[
\frac{1}{g_{Y,\rm phys}^2}=n^TKn=K_{YY}=\frac{1}{g_Y^2}.
\tag{U5}
\]

The right-hand identity follows by inverting GG^T; using H_YY=gY^2+tilde-g^2 would count the massive boson's contribution as long-range hypercharge. At the full-rank fixed point,

\[
g_{Y,\rm phys,*}^2=F/B_{YY}=6F/41.
\tag{U6}
\]

Therefore the orientation really is fixed relative to the lattice, but it supplies no extra absolute hypercharge number. In these two spectra B_YY is unchanged. After electroweak breaking the tree-level relation is 1/e^2=1/g2^2+K_YY. In this truncation g2 is asymptotically free with a relevant amplitude; it is not fixed by U2. All of these statements are tree-level matching identities at a declared common scale, not an alpha(0) run.

Finite breaking thresholds, the gravity-to-SM crossover, the electroweak matching scheme, charged masses and hadronic vacuum polarization would still be needed. No phi vev, scalar potential or physical new-vector mass is derived in this route. The charge lattice fixes the surviving direction, but not those threshold data.

## 4. A coefficient-free correlation that is worth testing

Subtracting the top and bottom nonzero fixed-point equations cancels the common f_y, common left-doublet gauge norm and common trace terms. For the two-Yukawa truncation,

\[
\Delta_*\equiv y_{t*}^2-y_{b*}^2
=q_u^T H_*q_u-q_d^T H_*q_d.
\tag{U7}
\]

At U2, both Delta* and gY*^2 are proportional to F. Exact elimination gives

| Model | Delta*/F | Delta*/gY*^2 |
|---|---:|---:|
| B-L full rank | 2/841 | 41/2523 = 0.0162505... |
| chi full rank | 18/20369 | 123/20369 = 0.00603859... |
| SM third-generation, one U(1) | 2/41 | 1/3 |

This is a real testable correlation, not a universal free-coefficient obstruction. In particular, given independently established **UV** values of both Yukawas, B-L would imply F=(841/2)Delta* and chi F=(20369/18)Delta*. The three models must not be interchanged. No equality between IR quark masses and UV Yukawas is asserted.

## 5. Executed reverse test: masses to hypercharge, reduced SM only

We implemented the [Eichhorn-Held third-generation mechanism, arXiv:1803.04027v2](https://arxiv.org/html/1803.04027v2), Eqs. (1)-(5), in reverse. Inputs were declared in inverse_inputs.json before the run: yt(mt)=0.935, yb(mt)=0.0136, mt=172.56 GeV, alpha2^-1(mZ)=29.589 and alpha3^-1(mZ)=8.475 from Carone Appendix A; mZ=91.1876 GeV. No explicit electromagnetic alpha, gY, or alpha1 number is in the fit input. These phenomenologically matched MSbar boundaries may nevertheless share electroweak/radiative/covariance dependencies; statistical or raw-measurement independence is **not** established. This is a conditional relation test.

Non-Abelian running is integrated analytically from its given IR boundaries, with the same universal gravity term above a step at M. Hypercharge is constant above M and runs at one loop below it. Parameterize the nonzero UV Yukawa branch by v=yb*^2>0:

\[
g_{Y*}^2=16\pi^2 f_g/(41/6),\quad
y_{t*}^2=v+g_{Y*}^2/3,\quad
f_y=\frac{3}{8\pi^2}\left(v+g_{Y*}^2/72\right).
\tag{U8}
\]

Fit only (f_g,v) to the two IR Yukawas, integrate backwards from t_UV=t_M+4000 and then across the step, and leave gY as a held-out output. The local logarithmic map has full rank. The result is a **locally isolated** inverse solution, not a certified exhaustive search for all branches/roots.

| Declared gravity step M | fitted f_g | fitted f_y | predicted gY(mt) |
|---|---:|---:|---:|
| 1.22089e19 GeV | 0.0062973650 | 7.6997065e-5 | 0.31266317 |
| 2.435e18 GeV, sensitivity only | 0.0066307921 | 8.1077094e-5 | 0.32035075 |

For the first row, the Jacobian determinant d(log yt,log yb)/d(log f_g,log v) is 0.0320412, with singular values 0.702615 and 0.0456028. Thus two mass equations can indeed remove the two phenomenological gravity parameters on this reduced branch. Simply calling f_g an unknown would have missed this possibility.

Only **after** this fit, Carone's held-out alpha1^-1(mZ)=59.005 was run with the same one-loop convention, giving gY(mt)=0.35873460. The toy prediction is 12.8428% lower. This is a discrepancy of this defined leading-order model, with no sigma or physical-precision claim. Changing the declared step from unreduced to reduced Planck mass changes its prediction by +2.46%; the physical crossover must therefore be calculated for a precision inference.

The numerical inverse is conditional on floating tolerance and source boundary matching. UV cutoff/tolerance changes shift the returned Yukawas by about 3.3e-11 relatively; a different integration algorithm is also checked. These are numerical stability diagnostics, not estimates of perturbative/physical uncertainty. No Thomson-limit matching is attempted for a branch that already fails this hypercharge holdout.

## 6. Why the current full-flavor route remains open and different

The [latest full-flavor primary version, arXiv:2507.18304v3, 2026-10-09](https://arxiv.org/html/2507.18304v3), Sec. 2 and Appendix C Table 1, uses a bottom-dominated true UV fixed point plus an intermediate top-dominated regime. It parameterizes gravity and calibrates fg, fy and the scalar coefficient. In Table 1, theta_t,UV=+0.0015 but theta_b,UV=-0.00053. Thus the top has a relevant UV amplitude; U7's two-nonzero-Yukawa UV hypothesis does not hold on that branch.

Consequently the exact inverse problem includes at least (fg,fy,relevant top amplitude), equivalently a datum controlling the cascade, before fitting two quark masses. Two mass constraints do not generically eliminate three data. Intermediate top focusing can suppress sensitivity and offer approximate predictions, with its error controlled by the duration; it cannot automatically be substituted for an exact missing UV boundary condition. This is a parameter-counting implication of the extracted relevance assignment, not a new full-flavor numerical calculation. Independent CKM/other correlations could constrain it further, and have not been tested here.

The [Riabokon-Schiffer-Wagner check, arXiv:2508.03563v1](https://arxiv.org/html/2508.03563v1), Appendix C, also does not currently supply the needed regulator-stationary fg at SM content in its Einstein-Hilbert/background-field setup. Its own unreliability cautions are retained. This leaves a concrete calculation missing, not a proof that exact gravity cannot fix it.

## 7. First uncertain arrows and continuation

1. **Gravity -> U1 and F:** establish a controlled gravity-matter fixed point, the gauge avatar(s), stability matrix and threshold trajectory for the specified charge spectrum. A fitted F is not this calculation.
2. **UV completeness -> full-rank branch:** U4 is a counterfamily within the checked flow. Supply a physical branch-selection criterion or accept that only a region/conditional prediction follows.
3. **UV Yukawas -> actual IR spectrum:** the inverse test is closed only in the explicitly reduced model. For a realistic inverse test, use the latest full-flavor branch, identify the rank of its relevant-parameter-to-observable map, and determine whether independent CKM data close the cascade direction without fitting alpha.
4. **Gauge matrix -> alpha(0):** derive phi breaking/crossover/masses and perform common-scheme electroweak and hadronic matching. Tree-level U5 prevents a spurious kinetic-mixing enhancement.

The strongest surviving claim is that a fully interacting matrix fixed point can predict kinetic orientation and furnish gravity-coefficient-free correlations. The reduced inverse holdout fails; the exact alpha target remains unresolved. No claim is made that the mathematical mechanism is new globally, or that all asymptotic-safety/gauge-Yukawa completions fail.

## 8. Verification and artifacts

- `run-003/manifest.json`: authoritative exact run, status completed, 25 symbolic checks. Validator passed against current inputs. Two-model charge sums, beta identity, roots, critical polynomials, basis covariance and physical matching are checked. A uniform matrix/projector argument above covers the continuum beyond the finite checks.
- `inverse-002/manifest.json`: authoritative numerical inverse run, status completed. Validator passed. Domain/bounds and non-claims are in inverse_contract.json. DOP853 cutoff/tolerance and Radau algorithm comparisons are recorded in its result.
- `mutation-001/manifest.json`: status failed, as expected. Reversing only the source mixed beta coefficient is detected by the independent charge-trace identity; absence of its declared result is expected for the assertion failure.
- `run-001`: preserved first attempt, failed because SymPy's characteristic-polynomial symbol and a same-named assumed-positive symbol were distinct. Its original script is retained there. This was a symbolic-variable identity error, repaired without changing the mathematical target.
- `run-002` and `inverse-001`: earlier completed checkpoints, superseded by expanded projector/algorithm verification. Their current-path input hashes may be stale after those source additions; they are not the authoritative evidence.

No commits, old-work edits, full-PDF cache writes or shared-status edits were made. Final artifact hashes are in HASHES.json. The math-proofreading self-review covers this new report and equations. Its one notation clarification makes the otherwise implicit reference scale explicit: t=ln(mu) becomes t=ln(mu/mu0). Derivatives and conclusions are unchanged. No unresolved typographical issues remain in the reviewed scope.

The coordinator's independent algebra review is in `../reviews/UV_MATRIX_REVIEW.md`; it rederives U1-U7 and confirms the singular rank-boundary eigenvalue distinction. That is a separate same-team proof review, not an independent full FRG calculation or a rerun of the numerical inverse.
