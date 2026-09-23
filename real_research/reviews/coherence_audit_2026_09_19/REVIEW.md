**September 12–19 research review: a useful structural reduction, three broken bridges, and a constructive continuation.**

**Latest result:** [the closure continuation](closure_resume/STATUS.md) carries the constructive search further. It preserves the positive-kinetic theorem, reconstructs physical gravitational potentials, corrects the interpretation of the earlier short response transient, tests a same-field fluid repair, and derives an explicit vacuum/screening scale tradeoff. The same-field repair changes the galaxy equation; the normalization still needs an additional physical relation. The theory is not closed. The [earlier constructive checkpoint](frw_repair/CONSTRUCTION.md) and raw numerical records remain available with the interpretation correction marked.

The programme remains **incomplete**. The smallest central missing implication is that one precisely specified action, on a consistent expanding background, has healthy physical perturbations and evolves into the required galactic/cluster response. Existing certificates from different actions, approximations, and matter interpretations do not establish that implication.

There is useful new progress here: an exact clock-loading criterion, an operator mismatch that explains why some recent conclusions cannot be transferred to the written action, and explicit counterexamples to two other claimed bridges. This is a bounded audit and mathematical checkpoint, not a completed gravitational theory or a solution of a Millennium problem.

**Scope and provenance.** I surveyed the last week's Git history (over 600 commits), current candidate/work-order documents, and selected load-bearing proofs and scripts. I did not read or rerun every changed file. Detailed work covered L279–L288, the equilibrium/normalization branch, and selected RH/YM/NSE bridges. Initial checkpoint was `49802f046e584bad399a86ba081f001d0d6e6739`. Another task committed L288 during this review; the recorded verification runs pin `23d3890790291c0ec44b4ca7da784a806d7094d2` plus the dirty working tree. Source hashes, rather than commit alone, identify the audited inputs. Existing research files were not changed. Everything produced here is in this new directory.

**1. The newest clock calculation changes the healing operator. This is a definite mathematical mismatch.**

The written [action, lines 6–10](../../../qwen_claude_field_theory/closure_2026/THE_ACTION_2026-09-05.md#L6) uses

\[
V_\mu=q_\mu{}^\nu\nabla_\nu\phi,\qquad
A_{\mu\nu}=q_\mu{}^\alpha q_\nu{}^\beta\nabla_\alpha V_\beta,
\qquad A_{\mu\nu}A^{\mu\nu}.
\]

With the convention \(K_{\mu\nu}=q_\mu{}^\alpha q_\nu{}^\beta\nabla_\alpha n_\beta\), direct differentiation gives

\[
A_{\mu\nu}=q_\mu{}^\alpha q_\nu{}^\beta\nabla_\alpha\nabla_\beta\phi
+QK_{\mu\nu},\qquad Q=n^\mu\nabla_\mu\phi.
\]

By contrast, L287:53–57 and `real_research/clock_2026/clock_action_build.py:227–230` square only
\(C=q^{\mu\nu}\nabla_\mu\nabla_\nu\phi\). On homogeneous flat FRW,

\[
A_{\mu\nu}=0,\qquad C=-3HQ,\qquad C^2=9H^2Q^2.
\]

Thus one operator vanishes on the homogeneous solution while the other changes its action and background equations. This is already warned about for the intrinsic Laplacian in the older, distinct C-H action (`g03_covariant_action_2026/ACTION.md:59–69`). That older action is a corroborating definition, not a substitute for the current action.

On the rolling Minkowski background, with scalar perturbation P, clock perturbation T, shift b, and spatial metric potential Phi, the correct linearized spatial object is

\[
\chi=P-Q_0T,\quad A_{ij}^{(1)}=\partial_i\partial_j\chi,
\quad C^{(1)}=\Delta P+Q_0\partial_i b_i+3Q_0\dot\Phi.
\]

The relative scalar chi is invariant under the residual linearized time transformation. For a single Fourier direction on flat homogeneous slices the intended outside-kernel healing term is proportional to \(k^4|\chi|^2\). It is not proportional to the square of the displayed C. The early bare \((\Delta P)^2\) implementation also misses the rolling clock's contribution.

Two qualifications matter. The tensor Hessian norm and intrinsic Laplacian square agree in the integrated flat quadratic problem with appropriate boundary conditions, not in arbitrary curved nonlinear geometry. Also, putting healing inside nonlinear J and putting it outside J define different theories; their quadratic coefficients can be matched by \(\xi_{\rm out}^2=J_Y(0)\xi_{\rm in}^2\) when that derivative exists. This review uses the explicitly permitted outside-kernel variant for its corrected flat quadratic calculation.

**Consequence:** the L287/L288 results do not yet prove the corresponding claims for the displayed action. This does not show that the candidate is healthy. In fact, the next result explains why correcting this operator alone may leave a serious low-frequency problem.

**2. A useful exact reduction: the clock's density-loading threshold is independent of the well curvature and spatial healing length.**

Notation: \(F_1=F_Q(\bar Q)\), \(F_2=F_{QQ}(\bar Q)\), \(Q=\bar Q\), \(W=\omega^2\), and \(\beta=(2-K_B)/(2-c_{14})\). I reconstructed L287's quadratic matrix independently, matching all 25 entries, replaced its healing term by the flat quadratic symbol of the written spatial-gradient operator, and extracted the exact coefficient of \(k^4\) in the gauge-fixed determinant. All 24 determinant permutations were included. The result is

\[
[k^4]\det M_4=
\frac{-3F_1Q}{c_{14}-2}
\left[3F_1^2-2F_2(3c_2+2)W\right]
\left[F_1Q(2-c_{14})+2(2-K_B)^2Q^2
-2c_{14}(2-c_{14})W\right].
\]

In particular the second factor's frequency is

\[
\boxed{m_{\rm clock}^2=
\frac{(2-K_B)^2Q^2/(2-c_{14})+F_1Q/2}{c_{14}}.}
\]

The entire displayed coefficient is independent of the corrected spatial healing length. This root is also independent of F2. For \(0<c_{14}<2\), its sign changes when

\[
-F_1Q/2 > (2-K_B)^2Q^2/(2-c_{14}).
\]

This explains an aspect of the newly recorded L288 instability and turns a parameter scan into an algebraic diagnostic: **altering F2 at fixed F1 and Q cannot change this root; neither can the corrected spatial healing term.** Changing the full well may still change the background history Q(a), so that possibility remains open.

For the illustrative L285 matter loading, Q/H0=1, KB=1/5, c14=1/40000, and F1/H0=-1.56 a^-3, the root in units H0^2 is approximately 33600.81 at a=1, -184799.19 at a=1/2, and -3.11999352e10 at a=1/100. These are frozen-background diagnostic values, not a cosmological growth history.

**Exact scope:** this is a theorem about the specified symbolic Fourier matrix and its long-wavelength coefficient. Interpret limiting branches only on the generic stratum F1 Q != 0, F2 != 0, c14 != 0, c14 != 2, with simple roots as needed; the F1=0 stratum has a different leading power and must be treated separately. A matter-loaded Minkowski background is not an exact FRW solution. Taking k toward zero there does not establish a physical superhorizon instability. The full expanding-background reduction, kinetic signs, horizon regime, and constraint propagation remain required. No general no-go theorem for all wells or all covariant completions is claimed.

There is a coherent next reduction. From the background charge conservation a^3 F1=constant, define \(R=-F_1/Q\). Where differentiable,

\[
\frac{d\log Q}{d\log a}=-3\frac{F_1}{QF_2},\qquad
\frac{d\log R}{d\log a}=-3+3\frac{F_1}{QF_2}.
\]

If the well holds Q nearly constant, R grows rapidly toward the past and threatens the threshold above. The ratio F1/(Q F2) here describes the well/background response; it is **not** being identified with the physical coupled mode's sound speed. Prove or disprove this loading obstruction in the consistent FRW equations before trying another well by name.

**3. Two verification claims need narrower interpretations.**

L287 tests the wrong signs for the residual gauge vector. The correct vector in its conventions is `(i omega, i k, 0, -1, -Q)`, which annihilates the exported matrix identically. The output's failed gauge-vector checks are a diagnostic sign error, not proof of gauge breaking. Its determinant-degree calculation is evidence for the linear spectrum at tested backgrounds; it is not the full nonlinear Dirac–Bergmann analysis requested by CK06. Such a count needs constraint classification and separate rank-changing strata.

L288 constructs `Tvec` and `Tr_f` at lines 98–103 but never evaluates that trace residual later. It also adiabatically eliminates a very stiff direction at lines 133–139. The unused residual and singular reduction need verification before its constraint-preservation language can be accepted. Agreement with a frozen Minkowski surrogate is a valuable comparison, not a replacement for those checks.

L279 and L282 contain a valuable surviving connection: eliminating the gravitational constraints produces the coefficient J_Y-beta0, and the deep-MOND condition makes the relevant quadratic sound-speed root zero. This was already found in the repository; I do not claim it as new. It means that bare scalar ellipticity (L281) does not by itself establish positivity or regularity of the fully reduced physical system. Use the constrained quadratic action as the common object.

**4. The equilibrium stability certificate uses an incomplete force equation.**

G081:27–40 declares a self-gravitating isothermal fluid with rho0=A/r^2 and sigma^2=C/2, and perturbations xi(r) exp(-i omega t). Its Euler linearization drops `-delta_rho * Phi0'`; its final mode equation also has the wrong omega^2 sign for that convention. Including the missing term gives

\[
\sigma^2\xi''+(2\sigma^2/r^2+\omega^2)\xi=0.
\]

The advertised zero modes xi=r and xi=r^2 have nonzero residuals 2 sigma^2/r and 4 sigma^2. Q009 proves identities for the operator it was given, but that operator is not this Euler–Poisson linearization.

A constructive replacement is an exact variational witness. On an annulus [1,64], choose xi=(r-1)(64-r)/r, with both endpoints zero. Then

\[
\int_1^{64}[(\xi')^2-2\xi^2/r^2]dr
=-115605/64+1560\log2\le-15765/64<0.
\]

SymPy checked the integral; Lean checked the force cancellation, nonzero mode residuals, and negativity of the closed form. A full spectral instability theorem still requires the operator-domain/variational bridge. This finding applies to the specified self-gravitating isothermal fluid, not to collisionless matter or to the clock action. The arbitrary profile amplitude/temperature selection problem remains: Q004 correctly exposes that hydrostatic balance alone does not choose the desired halo.

**5. The major-problem bridges require repairs before further extensions.**

| Branch | Audited issue | Strongest safe next step |
|---|---|---|
| Yang–Mills | YM07's universal magnetic-deficit estimate fails even in its own finite hard-core model. Polynomial positivity in Lean does not establish an operator spectral gap. | Define the true interacting ground state and prove an operator inequality over the declared state space. |
| Navier–Stokes / phantom fluid | N07 identifies an exact r^-2 halo force with the excess from an interpolation law that has a different transition and inner asymptotic. N09 explicitly uses an unprojected gravitational forcing. | Derive the excess profile from the chosen full law; keep that static inversion separate from a fluid evolution equation and incompressible NSE. |
| Riemann hypothesis | RH05L's proposed normalized beta-family edge limit is false; reflection symmetry and moment identities supply no zero-location bridge. | Correct the normalization and state an actual analytic implication about zeta; the existing counterexample to symmetry alone remains useful. |

For YM07 (`YM07_uniform_gap.py:435–457, 492–506, 576–584`), set x=8, N=2 and
\(\psi=(|0\rangle+\epsilon|p\rangle)/\sqrt{1+\epsilon^2}\), epsilon=1/100. This is in the type of vacuum/loop superpositions its tested family explicitly includes. Its own definitions give

\[
\ell=1/10001,\quad D_B=-25/10001,\quad
6.5\ell=13/20002<|D_B|.
\]

The proposed bound fails by 50/13. Moreover \(12\ell+D_B=-13/10001<0\), so the electric vacuum is not the interacting ground state used in the claimed subtraction. The code computes `Ee - DB` at line 625 even though its definition of DB requires `Ee + DB`. The structural obstruction is stronger than a single example: occupation is quadratic in epsilon but vacuum-loop interference is linear. Lean proves that no fixed positive multiple of epsilon^2 bounds epsilon/4 for all positive epsilon. This refutes this proof bridge, not the actual Yang–Mills mass-gap conjecture.

For the particular law used by N07:61–66, g_obs=sqrt(g_N^2+a0 g_N), a spherical point baryon mass gives

\[
M_{\rm ph}=M_b[\sqrt{1+(r/r_M)^2}-1],\qquad
\rho_{\rm ph}=\frac{a_0}{4\pi G r\sqrt{1+(r/r_M)^2}}.
\]

Its inner slope is -1, outer slope -2, and g_ph(r_M)=(sqrt(2)-1)a0. N07:24–31 instead assigns g_ph(r_M)=a0 from the deep asymptotic. These cannot both be exact statements about the same object. These formulas concern N07's specified interpolation law, not every kernel in this repository. Its assigned pressureless dynamics does not follow from the static excess-density inversion.

RH05L:68 asks for `(l-1) B(s,l-s) -> B(s,1-s)`. At s=1/2 the left side tends to zero, the right side is pi. This is an unproved statement in a comment, not an accepted Lean theorem. The unnormalized beta function has the stated nonzero limit. Fixing that does not produce a zeta-kernel embedding or RH proof. The useful log-moment/reflection results remain statements about their actual functions.

**6. The research priority I would choose.**

Work on the gauge-invariant relative scalar chi and the conserved cosmological charge within a single pinned outside-kernel action. Rebuild its background and quadratic action together. Derive the lapse/shift constraints, verify their propagation including the trace equation, and reduce to physical variables before integration. Then seek one theorem with an explicit alternative: either the density-loading mode remains acceptably slow on an expanding branch that also produces the galactic response, or a parameter-independent obstruction excludes that specified class.

Only after that succeeds should the same action's galactic/cluster solution and its stability be compared. The amplitude/halo-selection problem remains separate from writing an equilibrium profile. The kappa=1/2 normalization also remains free in the action reviewed here; changing that requires additional physics breaking the already documented normalization freedom.

The three executed routes were: operator equivalence (refuted, with constructive corrected flat symbol), structural spectral reduction (exact conditional clock-loading criterion obtained), and falsification of cross-domain bridges (finite counterexamples / missing force term found). The new result narrows the next experiment without asserting that the original physical goal is reached.

**Literature scope.** A narrow primary-source check of Skordis and Zlosnik, arXiv:2109.13287v2, sections III–IV, confirms that reduced scalar modes and Hamiltonian constraints are already central in AeST stability analysis. Cold or nonpropagating modes alone are not a novelty claim. The repository's khronometric/healing action differs, so that paper is a comparison and methodology reference, not an external proof of this candidate. [Primary source](https://arxiv.org/html/2109.13287v2). No global literature-novelty claim is made.

**Verification and remaining trust boundary.** `run_symbolic/manifest.json` records the successful 18.37-second exact symbolic run, including input hashes before/after. `run_lean/manifest.json` records a successful 9.17-second compilation of 13 small algebraic theorems in `ClockAndBridge.lean` and `EquilibriumReview.lean`. Printed axioms contain only propext, Classical.choice, and Quot.sound; no sorryAx. Both manifests validated against the current files. One harmless unused-variable warning remains in EquilibriumReview. Geometry, variational derivation and the determinant-to-cosmology bridge are not formalized in Lean; the first two have explicit symbolic/analytic checks here, while the physical expanding-background conclusion remains open. Three bounded delegated reviews were reconciled with direct source inspection and fresh checks by the coordinating reviewer; their agreement alone is not the certificate.

For direct reruns from the repository root:

```bash
python3 real_research/reviews/coherence_audit_2026_09_19/check.py
python3 real_research/reviews/coherence_audit_2026_09_19/run_lean.py
```

The direct symbolic command regenerates `run_symbolic/results.json`; the preserved manifests/logs document the original audited run. For a newly timestamped evidence record, use the supplied contracts with the mathbox computation-audit runner and a fresh output directory, updating the declared result path correspondingly.
