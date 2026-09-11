# Nonlinear clock/baryon initial data: a solved gate, not theory closure

2026-09-10. Work started at `62a6ee687`; other agents changed the live repository
concurrently. No existing action was changed by this package.

**Outcome:** solved a regular nonlinear spherical constraint problem including
clock preservation; computed initial time derivatives and independently recovered
both weak-field potentials. The source-induced areal acceleration is bounded
linearly in source amplitude, incompatible with instantaneous deep MOND on this
initial-data family. **Finite-time nonlinear infall has not been evolved.**
The late-time/quasistatic candidate remains **OPEN**, not ACTUALLY CLOSED and not
universally excluded by this initial calculation.

## Attribution and empirical motivation

Credit to **Carl Zimmerman** for suggesting the dynamical/inference distinction
after sharing **Brian Keating's YouTube video**:
[user-supplied video](https://www.youtube.com/watch?v=HRnselv8Y6E).
The user-provided extraction motivated this test. Direct video retrieval failed
on 2026-09-10: its title and spoken statements were not independently verified.
This is credit for motivation, not endorsement or authorship of these calculations.
The commit body carries the same attribution.

Primary observational context: [Jiao et al., *Detection of the Keplerian decline
in the Milky Way rotation curve*, arXiv:2309.00048v4, A&A 678 A208
(2023)](https://arxiv.org/abs/2309.00048v4). Inference caution:
[Koop et al., *On the Galactic rotation curve inferred from the Jeans equations*,
arXiv:2405.19028v2, A&A 692 A50 (2024)](https://arxiv.org/abs/2405.19028v2).
The latter examines disequilibrium and tracer-density biases in outer rotation
curves. Both primary records were checked on 2026-09-10. Neither establishes this
clock theory. A finite radial window cannot alone exclude all exterior halo mass.
The extraction's centripetal acceleration should read v²/r, not v⁴/r².

No Gaia data were fitted here. Expanding spherical dust is not the Milky Way's
hot rotating stellar disk. Tracer disequilibrium does not by itself establish
a time-dependent gravitational potential. No global novelty claim is made.

## Same action, fixed background

With signature (-+++), constant gamma and positive M², use

\[
S=\int\sqrt{-g}\,[\tfrac{M^2}{2}(\mathcal R-2\Lambda)+P(X,\tau)
 +\sqrt{-\nabla\tau\cdot\nabla\tau}\,W(Y,\tau)-V(\tau)
 +\gamma X\Box\chi]+S_d,
\quad S_d=-\tfrac12\int\sqrt{-g}\rho_b[(\nabla\theta)^2+1].
\]

Here X=-grad(chi)², n is the unit normal to tau, Q=n.grad(chi), Y=Q²-X.
The existing reconstructed constitutive functions, differentiated in `background.py`,
are

\[
P=-\frac U2\log\frac{U-2dX}{U-2dq^2}+3\gamma qH(X-q^2),\quad V=U,
\quad W=U+2d\ell(\sqrt{1+Y/\ell}-1)-2\gamma q^2\dot q_{bg}.
\]

The coefficients are functions of the homogeneous clock flow, not the local
source. At a=1,m=0.1,v=0.5,M²=Qc=1,I=0.1,Lambda=0.7: q=10/11,
U=1/110,d=0.005,ell=q²m/2,H=sqrt(0.8/3). Time partials hold X fixed before
restricting to X=q². These functions were **inverse reconstructed**, not derived
from first-principles coefficient selection. The cubic operator is known, not
a claimed invention. No a0 or MOND law enters the action or constraint solver.

## Varied constraints and preservation

All spherical metric functions in ds²=-N²dt²+A²(dr+v_shift dt)²+R²dOmega²
are varied before choosing tau=t, R=r, chi'=0, Q=q_bg,
Kr=K_Omega=H_bg, v_shift=0, and normal-rest dust at t0. Choose
rho_b=epsilon sigma(r), sigma=exp(-(r/w)²). These are initial data, not equilibrium.
The complete symbolic pullback is in `slice_action/REPORT.md` and `derive.py`.

The momentum constraint vanishes. The Hamiltonian gives

\[
{}^{(3)}\mathcal R=2\rho_b/M^2,\quad f=A^{-2}=1-\frac{I_b(r)}{M^2r},
\qquad I_b(r)=\int_0^r\rho_b(s)s^2ds.
\]

4pi I_b is the areal-energy mass; proper rest mass is 4pi integral A rho_b r² dr.
Both are recorded. G_bare=1/(8pi M²) is not assumed to equal measured G.
Positive mass gives a 1/r curvature tail: f is not set to one at a finite boundary.

The unrestricted clock equation is

\[
T=V_\tau-P_\tau+WK-2W_YK^{ij}\chi_i\chi_j-2Q D_i(W_YD^i\chi)=0.
\]

Initially partial_t chi'=qN', so preserving T includes -2q²W_Y Delta_h N;
setting the initially vanishing gradient to zero for all time would miss it.
Define the following *derived* coefficients at the fixed slice:

\[
J=2qP_X-6\gamma Hq^2,\quad
\widehat B=2P_X+4q^2P_{XX}-12\gamma Hq+6\gamma^2q^4/M^2,
\]
\[
C_t=2qP_{\tau X}+3\gamma q^2W/M^2,\quad S=W-2q^2W_Y,\quad
D_0=3J(H+\gamma q^3/M^2),\quad D_\rho=\gamma q^2/M^2.
\]

The scalar-current and metric-trace equations give

\[
Q_t=-[N(D_0+D_\rho\rho_b)+C_t]/\widehat B,\quad
K_t=\Delta_hN-\frac{N(3qJ+\rho_b)+3W}{2M^2}-\frac{3\gamma q^2Q_t}{M^2}.
\]

Their coefficient matrix has computed determinant -2M² Bhat; this is **not**
a Poisson-bracket matrix or a DOF count. Clock preservation gives

\[
\boxed{S\Delta_hN-\lambda_0(N-1)-\lambda_b\rho_bN=0},\qquad
\Delta_hN=fN''+(2f/r+f'/2)N',
\]
\[
\lambda_0=-3J[-Wq/(2M^2)+C_t(H+\gamma q^3/M^2)/\widehat B],\quad
\lambda_b=W/(2M^2)-\gamma q^2C_t/(M^2\widehat B).
\]

The constant term Vtt-Ptt+3H Wt-3W²/(2M²)+Ct²/Bhat is independently
computed and agrees with lambda0, rather than being assigned to it. At gamma=1e-6,
S=0.0008265149328, lambda0=0.005194848096, lambdab=0.004545509971,
Bhat=2.309997183. The dimensionless length sqrt(S/lambda0)=0.39887694 is
a background coefficient, not an astrophysical fit or a propagation speed.

Boundary conditions are regular N'(0)=0 and finite-domain N(L)=1, with increased
L as a matching control. For the Gaussian the solver uses a uniform certificate

\[
f\ge1-\varepsilon w^2\max(1/3,\sqrt\pi/4)/M^2>0.
\]

This follows by bounding I_b/r separately for r<=w and r>=w. Rejection outside
this sufficient condition does not prove every larger source is inadmissible.

For smooth f>0 and S,lambda0,lambdab>0 on a finite ball, uniqueness follows by
integrating the difference equation against its solution: both the gradient
energy and (lambda0+lambdab rho_b)u² integral must vanish. Existence also follows
directly from (pN')'=w_r(V_rN-lambda0), with p=r²sqrt(f),
w_r=r²/(S sqrt(f)), V_r=lambda0+lambdab rho_b. The regular homogeneous
solution u(0)=1,u'(0)=0 stays positive by its positive flux derivative. Its
integrated Volterra equation has a regular O(r) integrand at the origin. The
regular particular solution plus a multiple of u uniquely meets N(L)=1 because
u(L)>0. These elementary radial arguments are analytic, not Lean formalizations
or a well-posedness theorem for the complete time-dependent system.

## Initial physical acceleration and potentials

Dust has zero four-acceleration, following metric geodesics. -N'/(NA) measures
acceleration relative to clock-normal observers; it is not alone the desired
gravitational force. The independent angular metric equation gives

\[
h_t=fN'/r-N[(1-f)/(2r^2)+qJ/(2M^2)]-W/(2M^2)-\gamma q^2Q_t/M^2.
\]

Compute d²R/ds_d² and subtract the same background. The inward result is

\[
\boxed{g_{areal}=\frac{1-f}{2r}-\frac r{2M^2}
 \left[U-\frac{W+2\gamma q^2Q_t}{N}\right].}
\]

Explicit lapse-gradient terms cancel. Initially dR/ds_d=H_bg R: the dust is
expanding, not areally at rest. rho_b,t=-3NH rho_b and theta'_t=N' are also
computed; neither the source nor the clock is frozen.

In the weak-field scalar decomposition beta=a²(B-E_t),
Phi_B=deltaN+beta_t, Psi_B=-zeta-H beta. Isotropic initial K gives beta=0,
not beta_t=0. `potentials.py` separately integrates

\[
\Psi_B'=(A-1)/r,\quad \beta_t''-\beta_t'/r=-(K_t-3h_t),\quad
\Phi_B=\delta N+\beta_t.
\]

Distinct spatial/evolution data and stated exterior tails are used. A manufactured
nonzero-slip control prevents accidental equality by construction. At amplitudes
0.002,0.001,0.0005 the maximum difference is approximately
5.316e-9,1.329e-9,3.323e-10: no linear slip is detected in this family.
Quadratic differences arise from applying linear gauge formulas to nonlinear
data; they are not a nonlinear physical-slip observable. This is not PPN or
null-geodesic lensing certification.

## Precise initial-branch obstruction and conditional Lean certificate

Put eta=1-N. The maximum principle, for the stated positive coefficients,
smooth finite ball and N=1 boundary, gives

\[
0\le\eta\le d_*\varepsilon,\quad d_*=\lambda_b/\lambda_0.
\]

The lapse is positive by its minimum principle; if epsilon d_*<=1/2 then N>=1/2.
Define n(r)=integral_0^r sigma(s)s²ds/(2M²r²) and
U_*=U+2gamma q²D0/Bhat. Substitution into the *derived* force gives

\[
g_{areal}=\varepsilon n(r)-\frac{\gamma^2q^4\varepsilon\sigma r}{M^4\widehat B}
                   +\frac{rU_*\eta}{2M^2N}.
\]

Since sigma decreases, n(r)>=r sigma/(6M²). Therefore, when U_*>=0 and
gamma²q⁴/(M² Bhat)<=1/6 (both checked here),

\[
0\le g_{areal}\le C(r)\varepsilon,\qquad C(r)=n(r)+rU_*d_*/M^2.
\]

For fixed r>0 and any fixed global a0>0, the exact exponential tangent inequality
then gives

\[
0\le\frac{(1-e^{-g_{areal}/a_0})g_{areal}}{\varepsilon n(r)}
\le\frac{C(r)^2\varepsilon}{a_0n(r)}\longrightarrow0,
\]

instead of the unit ratio required by instantaneous MOND. Seven Lean declarations
prove the finite inequalities and strict mismatch below epsilon<a0 n/C²,
**assuming** the linear force bound. The PDE bridge above remains analytic,
outside Lean; see `lean.md`. No added axioms or sorry are used.

This is **not a no-go for eventual galactic MOND**: the target is quasistatic,
whereas these initial data expand. Observation time, shape, boundary, radius,
and coefficients are held fixed. A distinct late-time nonperturbative branch
remains an open possibility, not an established escape.

## Range and reproducibility

Thirty cases: gamma={0,1e-6}, w={0.05,0.3,1}, epsilon={1e-7,1e-5,1e-3,0.05,0.5}.
At r=3w the measured small-source log slopes are between 0.99999995 and
1.00000000, not 1/2. The global diagnostic a0=sqrt(Lambda/(32pi)) is constant
across cases. This uses Carl's phenomenological relation in c=1 background units;
it is **not derived** or inserted into the force solver. No local a0 is used.

Independent finite differences with refinement, off-collocation residuals,
outer-domain refinement, zero-source/gamma=0 controls and unrestricted action
variation test the computation. Nodal roundoff residuals are interpolation
consistency only; the off-grid residuals in `run_001/experiment.json` assess
differential accuracy. Evolution residuals are absolute substitution checks,
not a finite-time evolution.

Run from the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_infall_2026/run_checks.py
```

`run_001/manifest.json` records exact commands, working directories, exit codes,
input hashes and platform. All stdout/stderr are retained. Three jobs run in
parallel; no dependencies are installed. Development included intentional
missing-module failures, a near-duplicate mesh failure, a factor error in a metric
diagnostic, and finer independent finite differences to meet the declared
tolerance. Final claims depend on the final verified run, not development exits.

Final verification: all 13 runner jobs exited 0, including the 18 unit tests,
37 new symbolic slice identities, existing action/matter/background controls and
seven Lean declarations. Across the 30 source cases the maximum off-grid
source-normalized lapse residual was 7.76e-10; maximum absolute time-equation
substitution residual was 6.32e-16. The minimum lapse was 0.7871 and the smallest
uniform f lower bound was 0.7784. These are bounded computations, not universal
health or empirical certificates. For example, at gamma=1e-6,w=0.3,epsilon=0.001,
r=0.9 the computed g_areal/gN_bare=1.00488669 while the diagnostic exponential
MOND balance ratio is 8.9328e-5 instead of one.

Mathbox computation-audit guided fail-capable checks, proof-audit prompted invariant
force and independent potentials, and proofread-math guided final self-review.
Independent agents checked action pullback, background jets and numerical accuracy.

## Next unavoidable calculation

Evolve the complete nonzero-chi' clock equation, scalar and dust currents, and
metric, solving the preserved constraints at every time slice and stopping before
caustics/shell crossing. This initial-only lapse equation cannot be reused after
chi' develops. Then measure relaxation, physical potentials and null focusing.
Full Dirac closure, PPN, measured G, perturbative health, CMB, empirical fitting
and first-principles coefficients are **not certified here**. A positive elliptic
coefficient does not prove ghost freedom or exclude an instantaneous physical
channel. The whole theory remains OPEN.
