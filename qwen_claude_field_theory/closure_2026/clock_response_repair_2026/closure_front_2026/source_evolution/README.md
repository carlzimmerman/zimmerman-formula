# Conserved source response: the next closure gate

This package varies the fixed quadratic ADM action already derived in
`../finite_wavelength/` and adds only the minimally coupled, conserved Fourier
probe

\[
\delta\rho=\varepsilon a^{-3}\cos(kx),\qquad
\delta T_{0i}=\delta T_{ij}=0.
\]

It does not add a scalar-matter coupling, choose a MOND interpolation function,
replace the background, or reconstruct any coefficient. The probe has zero
homogeneous density and changes sign, so it is not a positive-density galaxy.

## What is proved

Direct variation of the quadratic action gives the exact off-shell identity

\[
2M^2r(\Phi-\Psi)+E_\zeta+3(\partial_t+3H)E_{\rm shift}=0,
\qquad r=k^2/a^2.
\]

Therefore the regular constrained solutions satisfy \(\Phi=\Psi\), but only on
the stated on-shell background and for \(k\ne0\). The three real-algebra
consequences are compiled in `identity/NoSlip.lean`; they use no `sorry` or
custom physics axioms. The full action variation and differentiability
hypotheses remain outside Lean.

The canonical equations are integrated after eliminating lapse, clock and
shift. A time-dependent total-derivative change of momentum,

\[
w=p-a^3\left(\frac{2r}{\Theta}\zeta-\frac{\rho}{\Theta}\right),
\]

is exactly equivalent and removes severe floating-point cancellation. The
independent numerical audit finds 28,438 evaluations in the original
coordinates versus 166 in the shifted coordinates for \(k=100\), with force
response disagreement below \(1.7\times10^{-13}\).

## What the finite source run says

For \(\gamma=0\) and \(10^{-6}\), \(0\le t\le4\), and
\(k\in\{0.3,1,3,10,30,100\}\), both DOP853 and Radau agree, all auxiliary
rows close, and the three-grid residuals decrease. The final dimensionless
response \(-2r\Phi/\rho\) runs from approximately 1.155 at \(k=0.3\) to
1.00004 at \(k=100\). It is consequently Newtonian-side in this bounded
linear probe, not the target exponential MOND law.

That observation is diagnostic only: the deep-MOND equation is nonlinear and a
linear signed probe cannot establish or exclude its finite-amplitude spherical
branch. The repository's separate `../../spherical_baryon_bridge/` checkpoint
does vary a positive-density spherical source; its pinned refined run reports
fourfold force scaling when a Gaussian source's mass is quadrupled and its
width doubled, rather than the factor-two deep-MOND scaling. That is a
candidate-specific linear/spherical
obstruction, not a universal no-go, and its result is not silently combined
with this Fourier calculation. The remaining route is the fully nonlinear,
finite-mass branch with common boundary data.

There is also a separate exact two-radius obstruction for the reduced
constant-\(\gamma\), zero-clock-charge radial action in
`../../mond_braiding_completion/README.md`: a universal acceleration-only
\(F_Y\) cannot coexist with its explicit \(2\gamma u^2/r\) flux at two radii
with the same \(g_N\), unless \(\gamma u=0\). That theorem excludes only the
displayed reduced sector; it does not cover the full time-dependent spherical
action or a new operator.

The newly added `../../../scalar_slip_gate_2026/` closes one more restricted
door exactly: a single local elliptic scalar with action `F(Y)` has
\(\Pi_{ij}=2F_Y(v_iv_j-\delta_{ij}Y/3)\), so pointwise no-slip at every
nonzero gradient forces \(F_Y=0\), while the exponential MOND flux requires
\(2F_Y\propto1-e^{-\sqrt{Y}/a_0}\neq0\). This is a conditional obstruction
only; any viable nonlocal/multiplier construction must derive a compensating
metric stress and rerun the full constraint analysis.

The latest L218 claim of a two-sided \(w\) window is therefore recorded as
conditional, not imported as a result here: its upper edge inherits L217's
unverified clock-rate/charge map, while its lower edge extrapolates one fixed
comoving gradient mode from the forest to recombination. L219's logarithmic-
kinetic cutoff estimate is useful algebraically but is based on a chosen vacuum
fluctuation normalization and a time-derivative-only excursion, not a canonical
mixed-sector unitarity calculation; its withdrawal of the L218 lower bound is
therefore also conditional. The independent review is
`../../../../../fable_independent_2026/L219_REVIEW.md`.

The PAPER25 review in `paper25_audit/REVIEW.md` is kept separate. It finds the
claimed \(s_0\) enhancement is not derived with a consistent physical-tilt
normalization and that the nonzero disformal metric has distinct photon and
tensor cones. The later L217 charge claim must retain the full cubic current;
the exact homogeneous \(\chi\)-charge is

\[
Q_\chi=a^3\left(2P_Xq-6\gamma Hq^2\right),
\qquad \dot Q_\chi=\lambda a^3\rho_b
\]

when a direct \(\lambda\chi\rho_b\) source is present. A separate symbolic
check also gives a source-free logarithmic-kinetic counterexample in which the
inverse margin drifts as \(d\log[1/(1-x^2)]/dN=-6x^2/(1+x^2)\), so a conserved
shift charge does not by itself conserve the clock rate. These facts prevent
treating the clock-rate argument as closure.

## Reproduction

From the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/source_evolution/evolve.py --tmax 4 --k 0.3 1 3 10 30 100
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/source_evolution/test_evolve.py
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/source_evolution/check_response.py --output <fresh-output-directory>/results.json
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/source_evolution/verify.py --output <fresh-output-directory>/regression
```

`run_001/manifest.json` is the computation-audit record for the 12-run source
response. `regression_002/summary.json` records the fresh Python and Lean
regressions (all child exits 0; the assertion negative control intentionally
exits 1). `numerics_audit/run_002/manifest.json` and
`identity/lean_run_001/manifest.json` preserve independent provenance.

## Status

**OPEN.** This checkpoint closes the finite linear source/no-slip calculation,
not the relativistic MOND theory. Remaining named gates include the nonlinear
localized baryon branch and exact \(\mu(y)=1-e^{-y}\), full Dirac counting,
PPN preferred-frame parameters, CMB/cosmological evolution, global stability,
and empirical galaxy/cluster tests.
