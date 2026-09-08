# IC-2: explicit scalar-kinetic completion, not full closure

2026-09-08; parent checkpoint `6dd851cf55039986b4ff1d1d88ca59c483328ca5`.
The action is now [IC-2](IC2_ACTION.md), an explicitly specified correction
to IC-1. **IC-2 remains OPEN.** IC-1's homogeneous positive kinetic sign is
not sufficient: its unmodified nonzero-wave-number scalar has negative
kinetic energy at sufficiently high wave number. The constructive result
here is an action term that removes that quadratic defect, while preserving
the static equations and expanding homogeneous branch by exact identities.

## Background and the action-derived reduction

Retain IC-1's exact expanding branch. Put

\[
\ell=\ln(9/5),\quad h=\dot B/B=\sqrt{\kappa/(6m)},
\quad \mathcal T=-\frac{27}{16}+\frac{54}{5\ell},
\quad x=\frac{e^{2/3}k^2}{h^2B^2}
      =\left(\frac{k_{\rm physical}}{H_{\rm physical}}\right)^2.
\]

Here L2 denotes twice the spatially averaged coefficient of epsilon^2, as in
the companion script; this harmless common factor does not change the equations.
The scalar variables are the barred metric perturbation z, lapse perturbation
n=delta ln N, auxiliary perturbation v=delta u and longitudinal shift.
For each real cosine/sine mode with k>0, vary the shift before eliminating it.
The momentum equation gives \(n=\dot z/(2h)+3v/8\).

For a general correction J=A a^2+B_J a.Du+C(Du)^2 define
\((\alpha,\beta,\gamma)=(4\ell^2/3)(A,B_J,C)\),
\(d=1/6+3\alpha/8+\beta/2\),
\(e=3/16+9\alpha/64+3\beta/8+\gamma\).
Eliminating the remaining algebraic equation gives

\[
\frac{L_2}{m e^{-1/2}B^3}
=a(x)\dot z^2+h b(x)z\dot z+h^2c(x)z^2,
\]
\[
a=3+\frac{\alpha x}{4}-\frac{(-9+dx)^2}{4(\mathcal T+ex)},
\quad b=\frac{2x}{3}-\frac{x(-9+dx)}{2(\mathcal T+ex)},
\quad c=x-\frac{x^2}{4(\mathcal T+ex)}.
\]

These formulas must be checked against the expansion of the actual action,
not adopted as a guessed quadratic model. The companion computation retains
the curvature and the terms from the lapse-dependent conformal factor.

## Constructive coefficient choice

The fixed IC-2 term has
\(\alpha=0,\beta=-1/3,\gamma=1/16\), so d=0,e=1/8. Its reduced kinetic
coefficient is

\[
\boxed{a(x)=3\frac{8\mathcal T+x-54}{8\mathcal T+x}>0
\quad(x\ge0).}
\]

Since \(\mathcal T=3(D+9)/4\), with IC-1's exactly positive D, the inequality
is analytic over all x, not inferred from a finite sampling. The eliminated
auxiliary denominator \(\mathcal T+x/8\) is also strictly positive. This is
a regular quadratic scalar reduction for k>0 on the displayed background.
It is not a nonlinear Dirac theorem or a proof that every physical scalar
channel is causal. The k=0 homogeneous system must be derived separately;
its unchanged action is IC-1's homogeneous action, not a substituted k->0
count inferred from the momentum equation above.

## Time dependence and the limitation that must not be hidden

Here \(\dot x=-2hx\). Integrating the mixed term by parts changes c to

\[
g=c-\frac12(3b-2xb')
=-\frac{2x[-64\mathcal T^2+8\mathcal T x+216\mathcal T
                   +2x^2+81x]}{3(8\mathcal T+x)^2}.
\]

The resulting equation is
\(\ddot z+[3h+\dot a/a]\dot z-h^2g/a\,z=0\).
The high-frequency physical scalar speed is **derived** as
\(\lim_{x\to\infty}-g/(ax)=4/9\). This repairs the UV kinetic/gradient
problem of the seed, but is not the entire stability requirement.

There is one positive sign-transition root, approximately x=46.2937226611:
g>0 below it and g<0 above it. Thus a band has negative instantaneous
frequency squared. In particular
\(g/x\to2/3-9/(4\mathcal T)>0\). No finite A,B_J,C in this correction
family changes that leading small-x sign. It must not be called an all-scale
gradient PASS. Conversely, an instantaneous negative frequency term is not
by itself a proof of unbounded future evolution on this expanding background.

Changing independent variable to x, the late-time indicial equation has
roots 0 and 3/2: regular future solutions freeze or decay as x redshifts to
zero. This limited asymptotic statement does not establish finite-time growth
bounds, observational acceptability, a retarded physical domain of dependence
or absence of nonlinear instabilities.

## What transfers to this action, and what does not

The correction is Q^2 times spatial auxiliary gradients. It and its first
variations vanish on static Q=0 and on homogeneous a=Du=0 configurations.
Therefore the original static equations and exact expanding background are
preserved, including their source/matching caveats. Pure homogeneous TT
perturbations still have zero correction. The canonical change of variables
still removes lapse and u velocities. Those are same-action bridges, not
borrowed PASS labels.

Next unavoidable calculations: reconstruct gauge-invariant matter/curvature
responses and their retarded support from the reduced scalar constraints;
bound the finite horizon-band evolution; continue nonlinear functional Dirac
preservation and track rank-changing/zero-field surfaces. Full PPN, realistic
cosmology, the static clock matching and empirical tests remain open. The
constant coefficients above are a constructed choice, not a derived universal
a0/Lambda relation or an established novelty claim.

## Executed checks and independent review

The final retained scalar script derives 27 exact zero residuals, including
raw Ricci/ADM identities, all three eliminated-field equations, the time
boundary term, zero-mode equations and static/homogeneous correction-transfer
checks. Its 11 tests and IC-1's 9 tests pass together (exit0); the relevant
32 existing lapse/constraint tests also pass (exit0). The default scalar run
exits0; both the all-wavelength-frequency and full-closure flags exit2. These
nonzero results are retained, not turned into overall physical PASS labels.

The author fixed a symbolic logarithm-normalization issue exposed during
development. A root test run was interrupted (exit130); the final fresh run
passed all 20 tests in 4.786 seconds. No physical conclusion rests on the
interrupted run. Independent review of the final module
`801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745`
recomputed the physical normalization, time-dependent potential, UV/IR signs
and zero-mode distinction, finding no critical issue within the stated scope.
Agreement between reviewers is not a replacement for the retained derivation.

The exact commands and immutable run records are in [REPRODUCE.md](REPRODUCE.md).
