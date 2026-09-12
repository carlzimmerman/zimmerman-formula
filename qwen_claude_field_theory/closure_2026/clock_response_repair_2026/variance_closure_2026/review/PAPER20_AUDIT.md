# Independent PAPER20 audit

2026-09-12. Target revision: `48ab93de3`; PAPER20's cited calculation is
`fable_independent_2026/L194_tracking_dynamics.py`, with its committed output.
Independent raw-source review using proof-audit; only this report was written.

**Normalized claim.** For the unchanged action
\(S=\int\sqrt{-g}[M^2(R-2\Lambda)/2+P(X,\tau)-V(\tau)+sW(Y,\tau)
+\gamma X\Box\chi]+S_m\), on an expanding history with clock rate
\(s_0>1\), its own nonlinear gradient variance approaches a stable statistical
state whose physical scalar squared sound speed is positive and of order
\((H/k_{\max})^2\); an adequate ultraviolet reach then satisfies the forest
requirement without coefficient tuning. Here \(X=-\nabla\chi\cdot\nabla\chi\),
\(s=\sqrt{-\nabla\tau\cdot\nabla\tau}\), and \(Y\) is the squared gradient
projected onto the clock slices. PAPER20 does not specify an averaging measure,
an ensemble, admissible initial covariances, or a physical ultraviolet domain.

**Primary verdict: incomplete, with the smallest missing implication being
the action-derived nonlinear statistical evolution.** The proposed ODE has a
reproducible finite-mode attractor, but its signed equilibrium is negative,
and neither its variance closure nor its physical sound-speed prescription is
established by the full constrained action. This does not exclude a different
nonlinear statistical state of that action.

## Dependencies and obligations

The claimed chain is action → finite-gradient principal operator → variance
evolution → attracting constrained statistical state → physical stress and
characteristics → forest response. The following table distinguishes its leaves.

| Obligation | Status | Decisive raw source |
|---|---|---|
| Fixed constitutive functions and homogeneous quadratic action | Passed as a defined local starting object | `nonlinear_evolution_2026/constitutive.py:25–38`; `cosmological_bridge_2026/derive.py:29–61` |
| L192/L194 proxy is the full finite-gradient characteristic | Failed as an identification | `L192_gradient_criticality.py:37–45,92–94`; the directly varied restricted two-field Hessian in `l192_principal_audit_2026/principal_audit.py:34–63` already has extra direction-dependent terms |
| Action implies the two-rate variance ODE | Not addressed | `L194_tracking_dynamics.py:45–52,86–93` inserts the rate and the common proxy; no field/constraint or moment derivation occurs |
| Tested finite-list ODE converges to its prescribed balance | Computationally verified only in its stated range | `L194_tracking_dynamics.out:5–18,23–29`; four starts at one frozen epoch, five root-scan wavenumbers, one five-mode list |
| Balance has positive physical sound speed | Failed within the proposed ODE itself | `L194_tracking_dynamics.py:56–61` targets \(-1/\kappa^2\); `.out:5–8` prints the negative sign; `.py:73–76,105–107` stores its magnitude |
| Stress degeneracy proves cold matter/forest viability | Incomplete | `L193_stress_degeneracy.py:25–59` verifies a gamma-zero off-shell determinant; it does not set the common pressure to zero or calculate a forest response |

Paths without the `fable_independent_2026` prefix above are relative to
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026`; L192–L194
are in `fable_independent_2026`. PAPER20's action-to-flow claim is at
`papers_2026/PAPER20_tracking_dynamics_2026.tex:14–30` under
`qwen_claude_field_theory`; its empirical inference is at lines 54–62.

Several exact restrictions matter. L194 freezes its coefficient values and
\(\kappa\) throughout each eight- or twelve-e-fold integration, whereas a
fixed comoving mode has \(\kappa=k/(aH)\). Its `coeffs` at lines 34–35 selects
the coefficient reference \(\bar q\); the physical scalar rate is the distinct
`q` recorded by `radiation_probe.py:89–97`. It also omits the existing gamma
contributions in the full constitutive functions. These distinctions must be
retained even when their numerical effects happen to be small at a sample.

The proxy stress determinant at gamma zero is valid for its transverse
numerator, but not an all-angle characteristic calculation. The actual
restricted kinetic coefficient is \(2P_X+4Q^2P_{XX}\), whereas the proxy uses
\(2P_X+4XP_{XX}\). Oblique/longitudinal propagation also has drift terms and
the clock denominator \(W-2Q^2(W_Y+2w^2W_{YY})-2w^2W_Y\), with \(w\) the
gradient component along the wavevector. These follow by taking the Hessian
of the invariant density, as explicitly implemented at
`l192_principal_audit_2026/principal_audit.py:36–63`; they are not supplied by
replacing \(W_Y(0)\) in a zero-gradient formula. The full gamma/Einstein system
requires its own reduction on admissible data.

At the ODE balance, \(k_{\rm phys}\sqrt{-c^2}=H\). Consequently the discarded
expansion, acceleration and coefficient-rate terms need not be small at that
balance even when \(k_{\rm phys}/H\) is large. A stable oscillatory mode also
does not in general retain constant field amplitude after its instability
switches off. The preceding tracking audit already establishes the sign,
higher-mode invasion and this nonuniform-limit problem; repeating those
checks would not close the new action-level obligation.

## What the six-state covariance system can decide

Let \(u_k=(\sigma,\delta Q,\delta r,\delta Q_r,\theta,\delta\rho_b)^T\)
be the real cosine-mode state. The existing reduction gives
\(\dot u_k=A_k(t)u_k\). For a centered ensemble of these linear solutions,

\[
\dot\Sigma_k=A_k\Sigma_k+\Sigma_kA_k^T,
\qquad \Sigma_k=\langle u_ku_k^T\rangle.
\]

This is exact **within the linear perturbation system**. It retains
velocity/gradient/matter correlations and coefficient rates. With the
single-real-harmonic convention and a uniform coordinate-period average,
\(\langle Y\rangle_2=k^2\Sigma_{00}/(2a^2)\). Thus, writing
\(p=k^2/a^2\) and \(e_0=(1,0,\ldots,0)^T\),

\[
\frac{d\langle Y\rangle_2}{dt}
=-2H\langle Y\rangle_2+p\,e_0^TA_k\Sigma_ke_0.
\]

The last term includes lapse correlations because
\(\dot\sigma=\delta Q+Q\delta N\), directly visible in
`transfer_evolve.py:100–105`. A variance-only rate cannot generally represent
all admissible covariances with the same \(\Sigma_{00}\).

**The current six-state operator contains no finite-variance feedback.**
`derive.py:38–44` has \(Y=O(\epsilon^2)\), expands the clock sector only as
\(W+W_Y\,Y\), and extracts only the quadratic action at lines 53–61. The
implemented Python term is `W + WY*Y`. `transfer_evolve.py:43` evaluates every
constitutive jet at
\((\tau,Q^2,0)\); its `mode_system(v,k)` has no variance argument. The transfer
equation at lines 173–176 is homogeneous and linear.

Therefore \(\Sigma(t)=T(t)\Sigma(0)T(t)^T\), and multiplying initial covariance
by a positive constant multiplies it at every finite time. A finite nonzero
attractor independent of initial amplitude cannot be inferred from this
system. It can test initial growth and the missing correlations, but cannot
decide nonlinear saturation, a shifted statistical exterior, or its forest
response. A computed loss of the small-perturbation regime is a limit of this
calculation, not a global no-go theorem.

The lowest nonlinear field terms require the cubic action \(S_3\); the
specific MOND curvature feedback \(W_{YY}(0)Y^2/2\) first occurs in \(S_4\)
and produces cubic field equations. For a general expansion
\(\dot u=A u+B_2[u,u]+B_3[u,u,u]+\cdots\), second-moment evolution includes
third and fourth moments beyond the displayed linear covariance equation.
Even initially Gaussian data do not remove the fourth-moment contribution or
the induced mean, geometry and clock response. Average stress/constraints
already receive order-\(\epsilon^2\) sources. A consistent order-four variance
calculation must include those responses, the other cubic/quartic vertices,
and the higher-order definition and averaging measure of \(Y\).

## One cheapest nonlinear action test

**Extract and verify the first omitted MOND vertex and its generated harmonic
directly from the unchanged action.** This needs no background reconstruction,
long integration or observational calibration. Freeze one regular FLRW epoch,
retain its physical clock rate, take \(\chi=\bar\chi+\epsilon\sigma\cos kx\),
and use a uniform coordinate-period average on that slice. Let
\(W_2=W_{YY}(0)=-d/(2\ell)<0\); the existing gamma correction in
`constitutive.py:31` is independent of \(Y\), so it leaves this derivative
unchanged. The isolated clock-MOND density gives

\[
\langle L_W\rangle_{\epsilon^4}
=\frac{3\bar s W_2 k^4\sigma^4}{16a}\epsilon^4.
\]

With the Euler sign convention
\(E_W=a^{-3}\delta S_W/\delta\chi\), direct local variation yields

\[
E_W=-\frac{2\bar s}{a^2}\partial_x(W_Y\partial_x\chi),
\qquad
E_W^{(3)}=
\frac{3\bar s W_2 k^4\sigma^3}{2a^4}
[\cos(kx)-\cos(3kx)]\epsilon^3.
\]

The coefficients multiplying \(\sigma^3\cos kx\) and \(\sigma^3\cos3kx\)
are respectively negative and positive under this Euler convention.
Projection of the local expression onto \(\cos kx\), including the density
factor \(a^3\), reproduces the derivative of the averaged quartic action with
respect to the mode amplitude \(\epsilon\sigma\), giving an independent
normalization check. In this action
sector a single harmonic generates a third harmonic; whether other sectors
cancel or modify the full coefficient is not settled by this isolated test.

There is also an exact averaging check in the same calculation:

\[
\langle Y^2\rangle=\tfrac32\langle Y\rangle^2,
\qquad
\langle W(Y)\rangle-W(\langle Y\rangle)
=\tfrac14W_2\langle Y\rangle^2+O(\epsilon^6).
\]

Thus the first quartic contribution already distinguishes averaging the
action from substituting the variance into it. An executable test should
differentiate the unaveraged invariant density, Fourier-project it, and
independently differentiate its period average; it should preserve both
\(k\) and \(3k\) coefficients and check the second/fourth-moment relation.
Its safe result is the exact isolated vertex and a specific missing coupling.
It is not a saturation simulation: completing that calculation needs all
\(P\), cubic-braiding, metric, clock and constraint contributions at the same
orders. Their coefficients must come from the existing action.

## Source and review record

Read `git show --stat --oneline 48ab93de3` and the numbered raw PAPER20,
L192–L194, action, constitutive, transfer and previous tracking/principal
sources using `nl -ba`, `sed` and `rg`. No source script with top-level writes
was imported or rerun. The vertex identities above are hand derivations from
the displayed density, not a claim of a new executed symbolic/numerical run.
No publication, external forest bound or ultraviolet cutoff was independently
verified; those are outside this local audit.

Mathematical proofreading self-review covered this new report's displays,
orders, signs and source locators. No existing manuscript was corrected.
Skills used: proof-audit and proofread-math (self-review).

## Concurrent L195 dependency addendum

Inspected the new commit
`08281ae2582ef39f853ad85405f3c56cb25dcc37`, dated 2026-09-12 12:43:02 -0400,
including its exact changed files and the raw
`fable_independent_2026/L195_cmb_gate_self_critical.py`, `.out`,
`L195_results.json`, and `FINDINGS.md:5541–5566`. This is a local source audit;
CLASS was not rerun and no external cosmological bound was authenticated.

**Dependency verdict: the new comparison does not close the action-level
gap above.** Its calculations concern assigned constant-sound-speed fluids.
They do not evolve the constrained statistical state or even the full
time-dependent sound-speed law proposed by L195. Specifically:

1. `L195_cmb_gate_self_critical.py:29–33` defines a chosen background
   \(H(z)\), inserts the **positive** law
   \(c_s^2=[H(z)/(k_{\max,\mathrm{com}}(1+z))]^2\), and takes the `0.776 Mpc`
   scale from L194. No action equation is imported. The positive sign is an
   additional premise: L194's root solve targets the negative value, as
   established above. The upstream variance/physical-characteristic
   identification remains unproved.
2. Lines 66–69 perform **two different constant-coefficient fluid runs** for
   each ultraviolet reach: `cs2_fld=cs2_of(1100,kmax)` for the CMB diagnostic
   and `cs2_fld=cs2_of(3,kmax)` for late linear power. Neither run implements
   `cs2_of(z,kmax)` throughout its history. The instantaneous Jeans expression
   at lines 38–43 supplies no equivalence between those distinct histories
   and a run with the proposed time-dependent law.
3. The replacement fluid is assigned `w0_fld=-1e-4`, `wa_fld=0`,
   `Omega_fld=0.1200/h**2` and residual `omega_cdm=1e-6` at lines 67 and 69.
   The action has not derived this equation of state, density, entropy/stress
   closure, or its initial conditions. The L193 isotropic-stress determinant
   does not determine \(w=-10^{-4}\). Lines 82–86 acknowledge constant sound
   speed, assigned density and the unestablished fast clock at recombination;
   those are active dependency conditions.
4. Lines 53–55 and 68 sample \(D_{816}/D_{537}\) and two linear-power
   wavenumbers. This is a finite diagnostic, not a calculation of agreement
   with the complete acoustic spectrum or a forest observable. The Jeans
   comparison at lines 39–43 checks five order-unity ratios; it does not
   prove exact CDM clustering above a sharp cutoff and zero clustering below.

The strongest safe numerical statement from the committed output is that, at
the inserted reach `8.096888282447921 /Mpc`, the **CMB constant-fluid run**
gives the sampled ratio `0.9905804378923699` against reference
`0.9915000904025206` (a `0.09275%` relative difference), while a **separate
late-epoch constant-fluid run** gives the selected linear-power ratio
`0.940773227511366`. Those numbers can motivate a future transfer calculation
after the action-derived statistical state exists; they do not certify it.

There is also a bounded classification error in the advertised threshold.
The `cmb_ok` list at line 76 requires only `restoration>0.9`, with no upper
bound. It therefore admits `kmax=0.05`, whose recorded ratio
`1.0507256503571787` is **5.9733%** above the reference and fails the symmetric
5% criterion used for V3 at line 74. This does not invalidate the recorded
`kmax=8.10` diagnostic. It does prevent treating the stated `0.05` threshold
as the result of that same 5% test, and six samples do not establish a
continuous cutoff threshold. The prose numbers in `FINDINGS.md:5547` also
disagree with the current raw output at lines 6 and 10; raw results were used
for this addendum.

L195 source SHA-256:
`0677c4b85bdc5d87be534a54ed342bb90761286bc9611938d58de012a3079e9d`;
output SHA-256:
`19154785bb18be3112e450eb762c08a023e607d5af11f3f1b35ceb4cec2b1b92`;
JSON SHA-256:
`c7618845a8b873ec0cb9f4b4c1c429c58c1fc4087c370d0de04f53640678a221`.
No new observational pass or global gravity no-go follows from this review.
