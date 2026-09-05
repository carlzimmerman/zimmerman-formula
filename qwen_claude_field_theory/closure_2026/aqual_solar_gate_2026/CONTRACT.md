# Fixed exponential AQUAL: bounded Solar-System audit

Approved task: finish the first falsification gate before constructing a new relativistic action.
Starting HEAD: 90eaf42dd. Work in the live repository; unrelated changes are preserved.

Equation: div[mu(|grad Phi|/a0) grad Phi] = 4 pi G M_sun delta(x),
mu(y)=1-exp(-y), with grad Phi approaching -g_ext zhat. This is AQUAL,
not the inverse-RAR kernel and not a QUMOND substitute.

Reuse the committed logarithmic-radius/colatitude finite-volume operator in
`qwen_claude_field_theory/theory_2026/aqual_solver_2026.py`, without editing it.
Replace its nonorthogonal discrete multipole projection only inside this audit:
fit Legendre orders 0 through lmax simultaneously, then fit the l=2 radial
coefficient to c2*r^2 + constant + d2/r^3. The last term represents a finite
inner-boundary harmonic. Compare three radial fit intervals and lmax=4,6,8.

The negative potential convention is Phi_N=-GM/r. In dimensionless units,
Phi_2=c2*r^2*P2(cos theta). Park's convention implies
Q2=-3*c2*a0^(3/2)/sqrt(GM_sun); retain the sign, not an absolute value.
Inputs: GM_sun=1.32712440018e20 m^3/s^2, canonical a0=9.3619e-11 m/s^2,
alternative a0=1.1279e-10, g_ext=2.32e-10 m/s^2, sensitivity endpoints
2.00e-10 and 2.64e-10. The endpoints are +/-2 times the repo's adopted
0.16e-10 external-field uncertainty, not a newly estimated posterior.

Frozen finite study: 256x64, 512x128 and 768x192 grids; outer radii 1e3,
1e4,1e5 and inner radii 3e-5,1e-4,3e-4 in MOND-radius units; zero versus
leading external-field anisotropic outer potential; two inner dipole choices;
iteration tolerances 1e-9 versus 1e-11. Keep radial grid spacing approximately
fixed when changing domain size. Fourteen cases; 160 iterations and 120 seconds
maximum per case. Deterministic binary64 arithmetic; no randomness.

The asymptotic potential is u=-1/[mu_e*r*sqrt(1+L_e*sin(theta)^2)],
where L_e=d ln(mu)/d ln(g) at the external field. This follows from the
anisotropic linearized AQUAL Green function; it is used only at the outer boundary.
Default inner boundary sets total Phi=-1/r. The alternative sets u=-1/r.
Neither finite boundary condition is asserted to be the exact infinite-domain solution.

Acceptance criteria, frozen before the full run:

- Synthetic monopoles must give zero quadrupole; mixed analytic harmonics must
  recover their supplied coefficient. The legacy extractor must fail the monopole control.
- Exhausted iterations/timeouts/nonfinite values are numerical failures, not theory failures.
- Medium-to-fine Q2 change <3%; boundary, tolerance, angular-order and radial-window
  variations <3% individually are useful convergence evidence, not certified error bounds.
- Independent published exponential-kernel benchmark: Q2 about 3.0e-26 s^-2 at
  a0=1.2e-10, g_ext=1.9e-10; require agreement within 6%, without calibrating the solver.
- Compare the signed prediction with published Q2=(1.6 +/- 1.8)e-27 s^-2.
  The mean+2sigma upper endpoint is 5.2e-27; it is not a hard physical limit.
- An exceedance robust to these checks is conditional empirical exclusion of this
  specified static branch, not a mathematical no-go for all relativistic MOND.

Tests precede implementation. All eight initially failed because the audit module
was absent; all eight passed after implementation. Run every created script and
the existing finite-interval study regression suite. No expected Q2 or theoretical
PASS is inserted into the solver. Physical input/benchmark values are explicitly sourced.

After the first full run, the 1e-11 iteration case exhausted its cap. A new
failing regression required retaining its update/coefficient history. Diagnostics
were added without changing the tolerance, cap, equation or acceptance criterion;
the entire study is rerun with that instrumentation. A plateau is diagnostic
evidence, not permission to relabel the failed tolerance check as a pass.

Limits: one inherited PDE discretization, no interval-certified continuum bound,
no new Cassini fit, no joint galactic nuisance likelihood, no full gravitational
action/Dirac/PPN calculation. No universal kernel or necessary-length-scale theorem.

## Primary-source ledger (checked 2026-09-04)

- Park, Hees, Famaey, Desmond and Durakovic, *Improved constraints on modified
  Newtonian gravity from Cassini radio tracking data*,
  [arXiv:2602.17884v1](https://arxiv.org/html/2602.17884v1), equation (6) and
  section III/Table 1. The fitted quantity is the Galactic-center-aligned
  anomalous quadrupole, estimated jointly with ephemeris parameters. Use its
  reported all-data mean and standard uncertainty; do not infer that the paper
  directly fits this project's exact exponential AQUAL solution.
- Blanchet and Novak, *External field effect of modified Newtonian dynamics in
  the Solar system*, [arXiv:1010.1349v2](https://arxiv.org/pdf/1010.1349v2),
  equations (34), (37), Table 1 and footnote 7. Their mu_exp is this exact
  1-exp(-y), and their positive-potential convention is minus ours. Their
  dimensionless q2 equals -3*c2, not this repo's qzz=2*c2. Table 1 supplies
  an external numerical benchmark, not a theorem or a new prediction here.

Sources inspected through the web reader, not retained as local PDFs. Search
scope: these exact papers and the published Park article DOI 10.1103/r7n8-kw38.
No novelty claim: this is an improved repository computation of known EFE physics.
