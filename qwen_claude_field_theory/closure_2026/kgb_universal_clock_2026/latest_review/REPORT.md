# L125: ordered cutoffs do not connect different wavenumbers

Primary verdict: **refuted, with an exact counterexample**, for the claimed
logical implication from cutoff ordering to galaxy-scale clustering. The
purported universal hybrid no-go is therefore not established by this argument.
No physical hybrid theory or MOND+CMB fit is constructed here.

Audited commit: `d0db626c4035117798922587fa5a9edc1e9fb40d`.
Only new `latest_review/` files are written. Existing theory, health, source
code and Git history are unchanged. The audit uses computation-audit for
exact tests/provenance, proof-audit for quantifiers, literature-check for the
physical formula, and proofread-math for this new report.

## Decisive missing implication

Let the idealized clustering proxy at epoch \(a\) be
\(\mathcal C_a=\{k>0:k<K_a\}\). If \(K_r<K_0\), then
\(\mathcal C_r\subset\mathcal C_0\). Hence

\[
 k_{\rm CMB}<K_r<K_0\ \Longrightarrow\ k_{\rm CMB}<K_0.
\]

This conclusion concerns the **same mode**. It gives no upper bound on a
different \(k_{\rm gal}\). The exact rational assignment

\[
 k_{\rm CMB}=\frac1{10},\quad K_r=\frac15,\quad K_0=1,
 \quad k_{\rm gal}=10
\]

satisfies all the displayed strict ordering and CMB-membership premises,
but \(k_{\rm gal}\notin\mathcal C_0\). Its smallest ordering margin is
\(1/10\), so this is not an equality-boundary artifact. More generally, for
every \(0<K_r<K_0\), choose \(k_{\rm CMB}=K_r/2\) and
\(k_{\rm gal}=K_0+1\). Lean proves this quantified counterexample family.

The failure even survives L125's assigned law \(K_a=a/v_0\): take
\(a_r=1/1091\), \(a_0=1\), \(v_0=10^{-6}\),
\(k_{\rm CMB}=1\), and \(k_{\rm gal}=2\times10^6\).
Then \(1<10^6/1091<10^6<2\times10^6\). These numbers have arbitrary toy
units and are not observational scales or a physical relic specification.

| Severity and exact locator | What is actually checked | What does not follow |
|---|---|---|
| Important: `L125_final_verdict_health_vs_cosmology.py:103-107` | Only `kfs_now > kfs_rec` | No comparison with a galaxy wavenumber, transfer amplitude, nonlinear halo density, or the claimed 1.69 overshoot is computed. |
| Important: same file `89-101` | Assigns \(K=a/v_0\) | A thermal-velocity ordering alone does not define the physical comoving free-streaming scale. |
| Important: `lean_2026/Mondlean.lean:403-409` | `hybrid_pincer_no_interior` proves same-\(k\) transitivity | Its type contains no second wavenumber or galaxy condition; the docstring's implication is stronger than the theorem. |
| Important: L125 `142-151` | Both verdict/scope predicates are literal `True` | They do not certify a mechanism-independent cosmological no-go. |

The file paths in this table are relative to `fable_independent_2026/` and
refer to the pinned commit. The valid same-mode theorem is retained; the
quantifier substitution is the failed step. Full Phase B constraint/health
claims are outside this bounded audit.

## Physical formula and scope of the velocity premise

Lesgourgues–Pastor, §4.5.2, Eqs. (93)–(96), defines a Jeans-like instantaneous
comoving scale \(k_{\rm FS}=\sqrt{3/2}\,aH/v_{\rm th}\) in its background
convention. With homogeneous nonrelativistic \(v_{\rm th}=v_0/a\), this is
proportional to \(a^2H\), not simply \(a\). The source's geodesic equation
(114) includes momentum changes from metric perturbations: the homogeneous
redshifting law is not a law for virialized velocity dispersions, nor a
derived propagation law for the interacting clock field.
[Primary source, exact v2](https://arxiv.org/html/astro-ph/0603494v2#S4.SS5.SSS2)

As an algebraic consequence of that stated definition, \(H\propto a^{-2}\)
gives constant \(k_{\rm FS}\), while \(H\propto a^{-3/2}\) gives
\(k_{\rm FS}\propto a^{1/2}\). The tests verify both substitutions. This
correction does not itself decide a CMB or galaxy fit: even granting monotonic
cutoff growth, the separate-wavenumber counterexample already applies.

## Prior counterexample reused, not recreated

L125 `116-117` repeats a generic stiff-density assertion. The committed
`kgb_nonaffine_clock_2026/l123_review/REPORT.md` already derives the exact
counterexample \(P=X^N\), \(N\ge2\), with
\(\rho\propto a^{-6N/(2N-1)}\), rather than unavoidable \(a^{-6}\).
Its nine tests are rerun read-only by this audit. This family is not being
added to the actual clock action and is not a dust, BBN or CMB solution.

## Reproduction and strongest safe conclusion

`test_cutoff_counterexample.py` has four tests: rational ordered cutoffs,
the literal assigned cutoff law, nine same-mode controls plus invalid input,
and the symbolic expansion-factor substitutions. `ScaleCounterexample.lean`
proves three ordered-real statements without a `sorry` axiom.
`run_review.py` records these, the existing nine L123 tests, and literal L125
execution. L125's seven PASS labels reproduce but are explicitly not accepted
as seven verified physical claims. The bounded manifest is in `run_001/`.
The actual read-only L125 run exited 0 and printed `7/7 checks PASS`; the
reused L123 suite exited 0 with nine passing tests. All four new tests pass,
and the three new Lean lemmas compile successfully.

The strongest conclusion is that the displayed L125 inference is invalid and
cannot close the claimed hybrid class. Resolving any physical candidate still
requires its common action, actual scale-dependent perturbation evolution,
matter coupling and sourced galaxy response. No dark-matter particles have
been introduced into the candidate, and no CMB viability has been claimed.
