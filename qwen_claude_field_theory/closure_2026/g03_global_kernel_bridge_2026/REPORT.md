# The missing bridge: the exponential law, the scalar action, and measured G

2026-09-05. Bounded same-action audit, not a completed theory.

## Result first

The newly proposed `J_Y,Newton = 30` corner cannot reproduce either exact
exponential target with a regular single-valued scalar constitutive function
in the clock-rest, charge-free, long-wavelength static reduction of f34/f35.
This remains true even if the target uses the **large-scale** rather than
locally screened Newton constant. A quantitative necessary condition is

\[
\boxed{f_s>\left[\min_{g_b>0}\frac{dg_{\rm target}}{dg_b}\right]^{-1}-1.}
\]

For the framework's RAR kernel the boundary is 0.03353559927 (3.35356%);
for the closure specification's exponential AQUAL kernel it is exactly
exp(-2) = 0.1353352832 (13.53353%). The new corner gives 0.02990048620.
These are dimensionless and identical on both acceleration-scale footings.
Equality is excluded for a finite regular constitutive derivative; below it
there is an explicit interval of negative longitudinal response.

This is a **restricted obstruction**, not a universal MOND no-go. Taking
f_s above the threshold can pass this one gate. A 3% observational ceiling
has NOT been measured here. The latest repository explicitly leaves that
data comparison undone. Finite-length, charged backgrounds and more general
couplings are not covered by this reduction. No gravitational DOF count or
full stability conclusion is assigned by this script.

## What the wider repository actually contributes

| Layer | Verified distinction or present limit |
|---|---|
| Original March finding | Root commit `84f2393113a087f05abd1bab0200c76384330009` uses critical density: a0 = c H0 / sqrt(32 pi/3). Its expression search selected against the observed a0; the half was not dynamically derived. |
| Current scale hypothesis | `STANDING.md` revision 7 uses dark-energy density and labels kappa=1/2 fitted. Relative to critical density it changes a0 by sqrt(Omega_DE); it changes the conditional redshift prediction too. |
| Current kernel | Revision 7 and THE_COMPLETION use nu_RAR(b)=1/(1-exp(-sqrt(b))), b=g_b/a0. The closure target instead uses mu_exp(x)=1-exp(-x), x=g/a0. They cannot be interchanged in an action or data fit. |
| Empirical support | f25's profiled algebraic-kernel comparison leaves these two exponentials undecided. It is a descriptive, galaxy-resampled SPARC comparison, not independent validation of a covariant theory. |
| Latest relevant commit | `82a8b3eac` adds FLRW and measured-G work. Subsequent `ab4e05027` is unrelated. The source hashes in the manifest identify the versions tested. |
| Relativistic construction | f34/f35 contain lapse-scalar mixing and an inside-J higher-gradient coefficient. g03d uses a constant outside-J coefficient and mu of the TOTAL potential. That nonlinear bridge remains missing. C-H's heat action is a different theory. |

The coefficient audits leave normalization free under their tested premises;
they do not prove that every possible first-principles derivation is impossible.
Likewise, finite families excluded by repository scans are not all possible
actions. We do not promote those headline no-gos to universal theorems.

## 1. Vary the actual static ingredients

Use Phi for the time-time physical potential and Psi for the independent
spatial potential. Set A=2-K_B, B=2-c14 and eta=A/B, with A,B>0.
Suppress the higher-spatial-derivative term only in the stated long-wavelength
or uniform-gradient limit. The weak/static, clock-rest Q0->0 sector is

\[
16\pi\widetilde G\,\mathcal L=
2|\nabla\Psi|^2-4\nabla\Phi\cdot\nabla\Psi
+c_{14}|\nabla\Phi|^2+2A\nabla\Phi\cdot\nabla\chi
-A[|\nabla\chi|^2+a_0^2J(|\nabla\chi|^2/a_0^2)]
-16\pi\widetilde G\rho\Phi.
\]

Sources: f34 lines 118-119 and 173; f35 lines 120-121 and 175. This is a
source-informed static reduction, not a fresh full covariant expansion.
The script varies its independent gradient variables and checks a nonlinear
polynomial free-function control as well as the frozen-coefficient system.

Varying Psi gives Delta(Psi-Phi)=0. With the harmonic difference removed by
the static boundary conditions, Psi=Phi. This is a static no-slip result,
**not** a calculation of the full PPN parameter set.

Define Phi0=Phi-eta chi and physical scalar potential psi=eta chi. Completing
the square gives

\[
16\pi\widetilde G\mathcal L_{\rm red}
=-B|\nabla\Phi_0|^2
-A[(1-\eta)|\nabla\chi|^2+a_0^2J]
-16\pi\widetilde G\rho(\Phi_0+\eta\chi).
\]

The independent variations therefore give

\[
\Delta\Phi_0=4\pi G_0\rho,\quad G_0=2\widetilde G/B,
\qquad \nabla\cdot[F(|\nabla\psi|)\nabla\psi]=4\pi G_0\rho,
\quad F=\frac{1+J'-\eta}{\eta}.
\]

The free function depends on the scalar's gradient, not the total physical
gradient. In spherical symmetry, with no extra integration charge,
g=g0+s and F(s)s=g0, s=|grad psi|.
For constant Newtonian J'=j, direct solution of the quadratic Euler equations
gives

\[
f_s=\frac{s}{g_0}=\frac{\eta}{1+j-\eta},\qquad
G_{\infty}=(1+f_s)G_0.
\]

This reproduces f35's j=30 scalar share without loading its cached quadratic
action or copying its measured-G answer. It does not refit its PPN ladder.

## 2. Reconstructing J has a necessary slope condition

Be generous to the candidate and define the target baryonic acceleration
using G_infinity: g_b=(1+f_s)g0. Then

\[
s(g_b)=g_{\rm target}(g_b)-\frac{g_b}{1+f_s}.
\]

Differentiating the scalar flux equation independently gives

\[
\frac{d(Fs)}{ds}=\frac{1}{(1+f_s)\,[D(g_b)-1/(1+f_s)]},
\qquad D=\frac{dg_{\rm target}}{dg_b}.
\]

Positive, finite longitudinal static stiffness requires the denominator to
be strictly positive. Since both kernels have positive slope and approach
the Newtonian slope 1 from below at some accelerations, the boxed condition
follows. If a decreasing interval is present, the desired s(g_b) also folds,
preventing a single-valued regular global reconstruction of J. If instead
the exact target's G is the locally screened G0, set f_s=0 in this matching
condition: both kernels already fail. Relabelling the measured G is thus
not an automatic escape.

For RAR, put u=sqrt(g_b/a0). Then

\[
D(u)=\frac1{1-e^{-u}}-\frac{u e^{-u}}{2(1-e^{-u})^2},\quad
D'(u)=\frac{e^{-u}[u-3+(u+3)e^{-u}]}{2(1-e^{-u})^3}.
\]

Let h=u-3+(u+3)e^-u. We have h(0)=0, h'(0)=-1,
h''=(u+1)e^-u>0, and h(3)>0. Thus h has exactly one positive root;
D diverges at zero, decreases to its unique minimum, then approaches 1.
The root is computed independently with binary64 bracketing and 70-digit
arithmetic, not inserted as an expected answer. At the simple witness u=2.5
the j=30 denominator is already negative.

For mu_exp, g_b/a0=x(1-e^-x), so
1/D=1+(x-1)e^-x. Its derivative is (2-x)e^-x: its global maximum is
1+e^-2 at x=2. The lower scalar-share boundary is consequently exact.
The equivalent upper boundaries on the constant j are computed in results.json.

A positive xi^2 k^4 term cannot change a negative k^2 coefficient as k->0.
This does not establish a finite-xi galaxy instability: the relevant background,
allowed wavelengths, time kinetic matrix and constraints must be checked.
It shows why UV stiffness and tests at j=30 on Minkowski do not by themselves
certify the entire MOND transition. This audit does not analyze k=0 Dirac rank.

## 3. Cosmological sign audit

g03e uses L_phi=-N a^3 K(phi_dot/N). Its physical RHS density in the
gravitational normalization used there is

\[
\rho_\phi=-a^{-3}\frac{\partial L_\phi}{\partial N}
=K-QK',\qquad a^3K'=C.
\]

g03e instead calls the opposite-sign LHS term the density and accepts either
sign at line 65. For K=K2(Q-Q0)^2 the actual density is

\[
\rho_\phi=-\frac{Q_0 C}{a^3}-\frac{C^2}{4K_2a^6}.
\]

Healthy K2<0 makes the stiff piece positive, and the charge sign can make
the dust positive. Example K2=-10,Q0=1,C=-2,a=1: actual density +2.1,
claimed density -2.1. Thus the published sign interpretation fails, but
FLRW existence is not killed. The clock coefficient and charge conservation
survive. We have not edited a concurrently maintained g03e file.

## 4. Prior art and novelty boundary

This is **not a new general monotonicity theorem**. The relation between
single-valued scalar functions and Newton-constant renormalization is already
explicit in Famaey, Gentile, Bruneton & Zhao, *Insight into the baryon-gravity
relation in galaxies*, arXiv:astro-ph/0611132v2 (version identifier 9 February
2007), sections III B-E, particularly equations 24, 30, 39-41:
https://arxiv.org/pdf/astro-ph/0611132v2 . Primary PDF checked 2026-09-05;
the PDF body has a conflicting automatically generated date, so the arXiv
version identifier is the locator used. No source file retained.

Their Xi G translates to G0, and nu0 G to G_infinity. Their scalar gradient
s is our scalar force in a0 units. Their renormalization freedom is our
1+f_s. The present calculation specializes this known mechanism to both
repository kernels and tests it against f35's newly proposed corner. The
older local `DETERMINING_THE_AEST_FREE_FUNCTION.md` already notices the RAR
turnover with f_s=0; the nonzero measured-G comparison is the added audit.
Search scope: pertinent local papers and one targeted web search followed
to this primary source. No global novelty claim.

## 5. Reproduction and verdicts

From the repository root:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/bridge_audit.py
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/bridge_audit.py --strict-corner
python3 -B qwen_claude_field_theory/closure_2026/g03e_flrw_background.py
python3 -B hunt_2026/f25_profiled_kernel_comparison_mu10.py
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_clock_constraint_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_flrw_scalar_2026 -p 'test_*.py' -v
git diff --check
```

Recorded outcomes: initial test discovery before the module existed exited 1
(missing implementation); completed unittest suite 7/7 exits 0; audit exits 0
only for its internal checks; strict-corner exits **2**, a failed mathematical
necessary gate, not a runtime error. Existing g03e exits 0 despite the sign
bug; f25 exits 0 with 8 checks. The earlier C-H constraint and FLRW suites
pass 9/9 and 10/10, respectively, each exit 0; these are regressions of a
different action, not extra passes awarded to the present candidate.
`git diff --check` exits 0. No empirical claim is certified by these exits.
The audit writes results.json and a provenance manifest with input hashes.

An independent read-only reviewer reran the new suite and strict gate, checked
the source normalization and both thresholds, and requested explicit
regularity and measured-G qualifications; those are stated above.
Mathbox self-proofreading covered only this new report: a malformed `rm red`
LaTeX subscript and one last-digit decimal transcription were corrected;
no mathematical argument was changed by proofreading.

Files created here: bridge_audit.py, test_bridge_audit.py, REPORT.md,
results.json, computation_manifest.json. No pre-existing source altered,
no commit or push performed. Broader synthesis is selective, not a claim to
have read every file in the repository.

**Verdict:** the specific j=30 + either exact-kernel regular long-wavelength
identification is DEAD under the stated assumptions. The broader relativistic
programme remains **OPEN**. Next unavoidable calculation: choose and write
the complete nonlinear action (including the operator placement and the
physical Newton normalization), reconstruct its J along the MOND transition,
and test whether it genuinely evades this slope gate before reusing solar,
FLRW or PPN results. Increasing f_s above the gate is one mathematical escape,
not a demonstrated empirical or relativistic completion.
