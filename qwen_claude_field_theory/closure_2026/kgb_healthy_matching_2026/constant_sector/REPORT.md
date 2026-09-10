# Constant-F health reduction and targeted regimes

Base: `5fcb04bb78923f9cbf18cb83ea0e1647b18391a4`. This bounded task uses the
committed direct constant-F reconstruction in
`kgb_logslip_joint_2026/constant_f/constant_f.py`. It does not repeat the
previous \(y=.1\) failed point. No old source, index or HEAD was edited.

The same exponential target, clock \(\phi=-t+\psi(r)\), physical action
\(FR+P(X)-G(X)\Box\phi\), physical minimal matter, and one global
constant acceleration scale are retained. No particles or per-halo
normalizations are introduced. Results are exterior-vacuum local EF
diagnostics, not full physical-frame or cosmological certificates.

## Exact removal of normalization freedom

At fixed \((\epsilon,y)\), let \(X\mapsto a^2X\),
\(F\mapsto b^2F\), where \(a,b>0\), and reconstruct the same constant-F
inverse. The EF quantities scale as

\[
\begin{split}
\widetilde P&\mapsto b^{-2}\widetilde P,&
\widetilde P_\chi&\mapsto a^{-2}\widetilde P_\chi,&
\widetilde P_{\chi\chi}&\mapsto b^2a^{-4}\widetilde P_{\chi\chi},\\
\widetilde G_\chi&\mapsto b^2a^{-3}\widetilde G_\chi,&
\widetilde G_{\chi\chi}&\mapsto b^4a^{-5}\widetilde G_{\chi\chi},\\
v&\mapsto(a/b)v,&\mathsf H&\mapsto(a/b^2)\mathsf H.
\end{split}
\]

Substitution into the **original coupled** scalar principal gives exactly
\(\mathcal M\mapsto a^{-2}\mathcal M\), with all 16 SymPy residuals
zero. Thus constant \(F\) cannot change the local EF health signs, and
\(X\) only supplies a positive overall factor. Cone ratios and strict
health signs are unchanged. A numerical comparison at \(y=3\),
\((X,F)=(.5,.525)\) versus \((2,2.1)\), independently verifies this.

This is local reconstructed-principal invariance. It is not permission
to vary measured Newton coupling or clock boundary normalization between
halos, nor a claim that all physical observables are independent of \(F\).

## An analytic angular prefilter

Write \(E=\rho+p_r\), \(c=(p_t-p_r)/E\),
\(U=2Xc\), \(Z=X'/X=-2g-c'/(1+c)\). The regular direct inverse needs
\(X,F>0,c>0,E\ne0,Z\ne0\). It gives
\(G_X=FpE/(X^2Z)\), with \(p=\sqrt{2BXc}\).

The original principal, after the static clock and zero-current relations
are imposed, yields the exact angular identity

\[
\mathcal M^{\rm physical}_{22}
=\frac{X^2G_X^2}{F}-\frac{2G_X(gX+X')}{p}
 +\frac{pX'}B G_{XX}.
\]

This reduction has its own zero SymPy residual. Since
\(\mathcal M^{\rm EF}=\mathcal M^{\rm physical}/(2F)\), it gives

\[
\mathcal A(\epsilon,y):=X\mathcal M^{\rm EF}_{22}
=\frac{BcE^2}{Z^2}-\frac{E(g+Z)}Z+
\frac{cE}{Z}\left[
\frac{B'}{2B}+\frac{c'}{2c}+\frac{E'}E
-\frac32Z-\frac{Z'}Z\right].
\]

All primes are physical radial derivatives. Strict local scalar energy
requires **\(\mathcal A<0\)**. The helper evaluates this formula without
calling the original principal evaluator or using \(P_{XX}\); tests
compare it with the original coupled principal at four distinct \(y\).
This is a necessary filter, not a sufficient cone/stability certificate.
It does not prove that \(\mathcal A\) has one sign on the entire target.

## Targeted computation and actual boundaries

The finite input set was \(\epsilon\in\{10^{-6},10^{-3},.03\}\) and
\(y\in\{.001,.03,.3,1,3,6,10,20\}\): 24 predetermined points, with
actual total \(P/G\) derivatives at 40 digits. These sample deep-weak,
transition and large-\(y\) regimes, and two larger-compactness controls;
the latter are not claimed as observed galaxy parameters. No \(X,F\)
grid was needed after the exact normalization result.

There were **18 regular points and no healthy point**. Every regular
point had \(\mathcal M_{22}>0\), although the time coefficient changes
sign. Six points were explicitly rejected because \(c\le0\), rather
than being reported as valid failed-health backgrounds.

At \(\epsilon=10^{-6}\), actual scalar root solves locate

\[
y_{Z=0}=1.44363621914181136500877490288\ldots,
\qquad y_{E=0}=15.8915413228188237087155324289\ldots.
\]

Both are bracketed by sign tests in the test suite. The first is a
singularity of the direct action reconstruction, because it divides by
\(X'\); the second changes the sign of \(c\) for this target. Neither is
a physical conformal-map singularity: constant positive \(F\) has
\(C-XC_X=2F>0\). These two roots are not asserted to enumerate every
possible boundary in all \((\epsilon,y)\) regimes.

The more promising **new** positive-kinetic point \(\epsilon=10^{-6},y=3\)
was re-evaluated at 65 digits with actual action curvatures:

| Quantity | Value |
|---|---:|
| Time coefficient | \(9.09276996196\,10^{11}\) |
| Mixed coefficient | \(-2.23154099663\,10^9\) |
| Radial coefficient | \(-1.96687822682\,10^6\) |
| Angular coefficient | \(+5.78105113079\,10^6\) |
| Angular prefilter \(\mathcal A\) | \(+2.89052556540\,10^6\) |

It remains unhealthy because of the angular sign. Physical metric/current
errors are below \(1.9\,10^{-66}\) and \(2.9\,10^{-61}\); independent
EF metric/current errors are below \(5.9\,10^{-61}\) and
\(2.9\,10^{-61}\). The constitutive \(P\)-derivative error is below
\(1.3\,10^{-56}\). These are on-shell checks, not an assigned verdict.

## Reproduction, bound and next constructive gate

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_healthy_matching_2026/constant_sector/run_sector.py --result-file qwen_claude_field_theory/closure_2026/kgb_healthy_matching_2026/constant_sector/results.json
```

Four tests pass. The full recorded run used about **3.6 CPU seconds**,
well within the requested 180-second bound; the loop checks elapsed CPU
time and the runner rejects an over-budget result. No network or broad
optimizer search was used. `results.json` includes every point, rejection
reason, root residual, exact identity residual and refined coefficient.
The parent aggregate pins the final files. The initial TDD run failed
because the implementation was intentionally absent, before the passing run.

The first next construction step is to locate a genuinely negative
\(\mathcal A(\epsilon,y)\) region on a regular component, with actual
boundaries bracketed. Only after that necessary gate passes should one
check the full cone and then common-mass action matching. Searching
normalizations \(X,F\) cannot help. The finite set here does **not** prove
that no such region exists. No healthy interval, universal/common-mass
action, radial continuation, CMB fit, full Hamiltonian/Dirac closure or
all-theory no-go has been established.
