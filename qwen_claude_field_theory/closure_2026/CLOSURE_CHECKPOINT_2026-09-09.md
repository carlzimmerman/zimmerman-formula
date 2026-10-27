# Closure checkpoint — 2026-09-09

## Bottom line

The deposited AeST-like one-metric action is **DEAD as a healthy complete
theory**. This is not a claim that every conceivable relativistic MOND action
is impossible. It is the result for the explicit action in
`fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md` and its repaired
kernel branch.

The decisive independent rerun is
`fable_independent_2026/L60_anisotropic_health.py`: 64/64 checks, exit 0. Its
three routes agree that the transverse scalar-gradient stiffness changes sign
below (s=g_N/a_0\simeq0.3985). The repaired MOND branch therefore has a
gradient instability in the regime it is intended to explain. At (s=0.1)
the fastest mode has a roughly 0.73 pc wavelength and a 762 yr e-folding time
on the canonical footing (1.10 pc and 1142 yr on the alternate footing); at 1
kpc the e-folding time is still about 0.74 Myr. This is a gradient instability,
not a ghost claim. The action also has four propagating modes (two tensor, a
clock, and a MOND scalar), so it does not satisfy the requested
(N_{\rm grav}=2) target even before this instability.

The live branch then added L65, a direct test of the memory/wake idea. Its
causal doubled-field in-in action does produce a retarded kernel, but the
doubling is a response-field representation of hidden states: a branch-cut
kernel requires a continuum of bath initial data per spatial point, while a
rational kernel carries a ghost residue. The same lane finds that a purely
temporal or frame-free memory kernel cannot supply the static MOND scale and
cannot evade the lensing lock. Memory is therefore a viable variational
formulation, not a two-tensor-DOF completion.

Two newer live lanes sharpen the closure. L63 (`L63_degeneracy_locus.py`,
78/78 checks) proves that the submitted action's full velocity Hessian has only
three degeneracy hyperplanes: (c_2=-2/3), (c_{14}=0), and (K_2=0). The
clock and MOND scalar have identically zero Hessian mixing; switching both
kinetic terms off leaves their antisymmetric first-order coupling as a
symplectic pair, so the floor is three degrees of freedom, not two. The one
uniform branch with two tensors plus a separately counted clock is (K_2=0),
but it inherits the L60 threshold and buys an instantaneous elliptic channel.

L67 (`L67_emergent_mond.py`, 26 checks, exit 0) tests the superfluid/emergent
MOND hatch. It genuinely evades the added-sector “spent once” hypothesis, but
the phonon does not lens: the predicted dynamics/lensing ratio is at least
about 5.2 where the measured overlap is about 1.02. Normalising the condensate
to lensing restores the rotation-curve overshoot. That class is therefore dead
at lensing and not a completed alternative.

The current exact-exponential AQUAL route is not a rescue: its executable
Solar-System quadrupole audit classifies the unscreened external-field branch
as dead against the stated Cassini ceiling, and its regular-center audit proves
that the exact (μ(0)=0) equation is incompatible with a classical (C^2)
positive-density force-free center. Those are branch-scoped results, not a
universal relativistic no-go.

Door 4 closes the local analytic one-metric curvature fork.  For the varied
action (S=\int\sqrt{-g}(FR+aR^2)+S_m), the independently solved static
potentials give

\[
\gamma_{\rm PPN}=\frac{F+4aK}{F+8aK},
\]

so exact no-slip for all (K>0) forces (a=0); (a\neq0) has a finite trace
scalar pole and a linear source response (degree one), incompatible with the
deep-MOND degree-one-half scaling.  A Weyl-squared extension adds a second
spin-2 pole with opposite residue.  This is a subclass closure, not a theorem
against nonlocal, preferred-frame, or matter-field actions.

The derivative-bimetric door is now also boundedly closed for the tested
five-invariant tuned subspace.  The action-level Stückelberg calculation finds
the pure scalar row/column identically zero but a transverse vector term

\[
L_{A_1}=-\frac{\lambda}{2}(2u_0+u_1)(\kappa-\omega)^2(\kappa+\omega)^2A_1^2,
\qquad a_{\rm MOND}=-2(2u_0+u_1).
\]

Thus a MOND-alive direction has a fourth-order vector operator and the local
Ostrogradsky ghost obstruction in this representative basis.  Independently,
the static interaction-dominated lensing ratio is

\[
Q'/P'=u_1/[2(u_0+u_1)],
\]

and setting it to one forces (u_1=-2u_0\), which simultaneously sets
the MOND acceleration coefficient to zero.  The tensor-speed check passes for
the tested point ((c_T=1), positive kinetic coefficient), but that does not
rescue the vector/lensing failures.  The report explicitly scopes this to the
displayed local derivative-bimetric action, not all two-metric theories.

The nonlinear-background follow-up strengthens that result. On a nonzero
static (T_4-T_1) background with ̄T=-4(p^2+2q^2), the computed vector
time-kinetic matrix is

\[
 W=\operatorname{diag}(-2M'(\bar T),4M'(\bar T)),
 \qquad \det W=-8[M'(\bar T)]^2.
\]

For (M(T)=(-T)^{3/2}), this is
\(W=\operatorname{diag}(3\sqrt{p^2+2q^2},-6\sqrt{p^2+2q^2})\). Hence
the local vector ghost persists on every tested nonzero MOND background,
not just the zero-field quadratic expansion. This remains a bounded
invariant-direction result, not a universal bimetric theorem.

The mimetic-clock audit closes a different escape hatch. For

\[
S_c=-\tfrac12\int\sqrt{-g}\,\lambda[(\nabla\phi)^2+1],
\]

the computed Dirac matrix for \((p_\lambda,C_2)\) has rank two in both
\(k=0\) and \(k\ne0\) sectors, leaving one clock configuration degree of
freedom. The expanding FLRW branch has \(\rho_c=\lambda\), \(p_c=0\), and
\(a^3\lambda=\mathrm{constant}\), so the nonzero dust source is exactly
the branch on which the clock is not an algebraic auxiliary. This is a
scoped obstruction to the memory proposal, not a universal no-go.

The latest G03 C-H action work remains **OPEN**, with a conditional causal
FAIL: its full variation passes nine algebraic checks, while the retained
shift-inclusive retarded screen passes eight numerical diagnostics but finds
nonzero curvature outside conserved-source support. The new
matter-admissibility check passes 10/10 and shows the particular cylindrical
source is signed and zero Killing-energy, so it cannot simply be reinterpreted
as added positive ordinary matter. The causal result therefore does not yet
close the compact ordinary-matter theory.

## New local calculations in this checkpoint

### Door 1: no-slip plus zero-flux compatibility

`door01_joint_2026/` scans 484 fixed-gradient states and enforces the scalar
zero-flux constraint while testing the no-slip curvature condition. The exact
constraint residual is (\lesssim1.6\times10^{-12}), but no state has zero
curvature residual. The follow-up `free_gradient_search.py` also allows the
common matched metric gradient to vary; over its deterministic bounded starts,
the best residual remains (1.43\times10^{-2})–(1.78\times10^{-2}). This is
a bounded search, not an exclusion theorem.

### Door 2: local ADM Hessian and homogeneous branch

`door02_adm_2026/check_adm.py` gives the exact local seven-velocity Hessian

\[
 \operatorname{diag}(D/2,\,(A/2)\mathbf 1_5,\,-K''),
 \quad A=F-c_{13},\quad D=-2F-c_{13}-3c_2.
\]

The generic rank is seven, so the submitted (K(Q)=K_2Q^2) branch contains an
extra scalar. Rank loss requires (A=0), (D=0), or affine (K), each of
which changes another required sector. The new
`homogeneous_generalK.py` check passes exactly and derives, on (D=0),

\[
\rho+p=4F\kappa/a^2+QK',\qquad \dot Q=-3H K'/K'',
\]

with exact matter continuity. In flat FLRW, (dp/d\rho=K'/(QK'')); the
standalone positive scalar-kinetic sign (K''<0) with (QK'>0) is therefore a
gradient-instability warning. The affine limit gives (3\ell a^3H=0), so
nonzero affine (K) forbids homogeneous expansion in this ansatz.

### Door 3: tensor speed

`door03_tensor_2026/` derives the frozen-background tensor principal symbol

\[
c_T^2=\frac{F+bJ'v^2\xi^2}{F-c_{13}},
\qquad b=2-K_B.
\]

Exact luminality requires (c_{13}=-bJ'v^2\xi^2). For the calibrated
exponential branch this required (c_{13}) varies with (y), so one constant
coupling cannot keep (c_T=c) over an extended MOND branch unless a coefficient
or the gradient operator is removed. This is a local principal-symbol result,
not a global no-go for a different action.

## Empirical prediction ledger (conditional, executable)

The strongest surviving outputs are weak-static predictions of the exact
exponential branch, not predictions of a closed relativistic theory:

1. **Two-clock inverse spectrometer.** For a spherical exterior,
   (q=\kappa^2/\Omega^2\in(1,2)) gives
   (Y=-L-W_{-1}(-Le^{-L})), (L=(q-1)/(3-q)), and
   (a_0=r\Omega^2/Y), (GM=r^3\Omega^2[1-e^{-Y}]). Cross-radius
   consistency is the null; (W_0) is explicitly rejected.
2. **Finite-eccentricity EFE nodal law.** In the external-field regime,
   (P\dot\Omega_{\rm node}=\pi[L_e/(1+L_e)]\cos i\,[1-
   (e/(1+\sqrt{1-e^2}))^2\cos2\omega]/\sqrt{1-e^2}) to first order in
   the anisotropy. The sign and (e,i,\omega) dependence are testable with
   long-baseline binary/flyby timing, but the calculation is explicitly
   nonrelativistic and branch-limited.
3. **Deep-MOND eccentric radial clock.** The same spherical force gives
   (T_r^4=F(e)^4R^4/(GM_ba_0)) and
   ((\langle v^2\rangle_t)^2=GM_ba_0) for a bound test particle wholly
   in the logarithmic regime. This is a bounded consequence, not an ensemble
   galaxy fit.
4. **Supernova relation audit.** The full-covariance Pantheon+ rerun gives a
   conditional shape-only (H_0=68.50\,\mathrm{km\,s^{-1}\,Mpc^{-1}}) for
   the (a_0=9.4\times10^{-11}\,\mathrm{m\,s^{-2}}), (H_0=67.4) footing,
   with profile interval 67.60--69.47. Because the background expansion and
   (a_0\)-\(\Lambda) law were inputs, this is not evidence that the action
   derives the relation; it is a reproducibility/consistency result only.

The live tests therefore provide falsifiable orbital nulls and a conditional
SN consistency number, but no empirical result can certify the missing
relativistic action, PPN, constraint, and stability gates.

## Exact commands and statuses

All commands below were run in the shared working tree while the live branch
advanced through `d6b81512c` (PAPER9 second-order reasoning amended after the
memory, degeneracy, and emergent-MOND deposits).  The current branch also
contains the pushed Fable commits `9bd3e7199`, `44e295d98`, `519bab5f9`,
`394c62785`, and their predecessors.

| command | status | result |
|---|---:|---|
| `python3 fable_independent_2026/L60_anisotropic_health.py` | 0 | 64 PASS / 0 FAIL; independent output differs from the recorded file only in runtime seconds |
| `python3 fable_independent_2026/L61_permitted_branches.py` | 0 | 47 checks; finding-failures are marked results, not crashes; two branches dead, two-metric branch still open |
| `python3 fable_independent_2026/L65_memory_kernel.py` | 0 | all controls/structural checks pass; 9 explicitly marked gate failures; memory route does not meet the destination |
| `python3 fable_independent_2026/L63_degeneracy_locus.py` | 0 | 78/78 checks; raw two-DOF floor is unavailable; (K_2=0) gives 2 tensors plus one separate clock but inherits L60 |
| `python3 fable_independent_2026/L67_emergent_mond.py` | 0 | 26 checks; emergent/superfluid hatch dies at lensing; failure lines are marked results |
| `python3 qwen_claude_field_theory/closure_2026/door01_joint_2026/free_gradient_search.py` | 0 | bounded no-slip/constraint search completed; no residual below (10^{-8}) |
| `python3 qwen_claude_field_theory/closure_2026/door03_tensor_2026/tensor_luminal_calibration.py` | 0 | required (c_{13}(y)) is nonconstant |
| `python3 qwen_claude_field_theory/closure_2026/door02_adm_2026/homogeneous_generalK.py` | 0 | exact symbolic identities and witness passed |
| `python3 qwen_claude_field_theory/closure_2026/door04_metric_curvature_2026/metric_curvature_gate.py` | 0 | 9/9 checks; local (FR+aR^2) curvature subclass closed |
| `python3 qwen_claude_field_theory/closure_2026/door04_metric_curvature_2026/test_metric_curvature_gate.py` | 0 | 2 tests passed |
| `python3 qwen_claude_field_theory/closure_2026/bimetric_secondfield/run_wf2_suite.py` | 0 | five child gates returned 0; scientific verdict is FAIL from vector ghost and MOND/slip dichotomy |
| `python3 qwen_claude_field_theory/closure_2026/bimetric_secondfield/wf2_nonlinear_vector_background.py` | 0 | nonzero-background (W=\operatorname{diag}(-2M',4M')), det (=-8(M')^2) |
| `python3 qwen_claude_field_theory/closure_2026/memory_clock_audit_2026/mimetic_clock_dirac.py` | 0 | Dirac rank 2 in (k=0,k\ne0); one clock DOF on nonzero FLRW dust branch |
| `python3 qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/g03_full_variation.py` | 0 | 9/9 checks; G03 remains OPEN |
| `python3 qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/g03_retarded_screen.py` | 0 | 8/8 diagnostics; conserved-source causal criterion FAIL, G03 remains OPEN |
| `python3 qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/g03_matter_admissibility.py` | 0 | 10/10 checks; tested cylinder source is not positive ordinary matter |
| `python3 -B qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/audit.py` | 0 | full-covariance SN likelihood reproduced; result is conditional, not an action-derived SN prediction |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/exponential_mond_kepler_spectrometer_2026 -p 'test_*.py'` | 0 | 73 tests passed; exact exponential weak-static/spectrometer ledger reproduced |
| `python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026 -p 'test_*.py'` | 0 | 17 tests passed; EFE Kepler/nodal calculation reproduced |
| `python3 -m unittest -v qwen_claude_field_theory/closure_2026/hpi_delta_eccentric_kepler_2026/test_hpi_delta_eccentric_kepler_2026.py` | 0 | 23 tests passed; finite-eccentricity law reproduced |
| `python3 -m json.tool .../homogeneous_generalK.json` | 0 | JSON parses |
| `python3 -m unittest -v .../test_exact_exponential_aqual_q2_2026.py` (from its directory) | 0 | 8 tests passed |
| `python3 -m unittest -v .../test_exact_mond_regular_center_no_go_2026.py` (from its directory) | 0 | 15 tests passed |
| `validate_manifest.py .../door02_adm_2026/run/manifest.json` | 0 | valid evidence record; mathematical interpretation requires review |
| `git diff --check` | 0 | no whitespace errors |

The standalone q2 mesh solver was not used for the checkpoint conclusion; its
documented unit suite passed, while a fresh full mesh rerun exceeded the bounded
interactive wait and was stopped. The existing committed/recorded q2 result
and its tests remain the evidence for that branch-scoped Cassini classification.

## Status labels

- **Candidate in `THE_COMPLETE_THEORY_2026-09-08.md`: DEAD.** It fails the
  requested (N_{\rm grav}=2) count and has a deep-MOND gradient instability.
- **Door-2 degeneracy claim: CLOSED NEGATIVELY.** The action cannot produce a
  genuine mixed clock–MOND-scalar null direction; its raw two-DOF floor is
  three because of the symplectic coupling.
- **Exact-μ exponential AQUAL-only branch: DEAD at the tested Cassini and
  regular-center gates.** A new relativistic completion could alter those
  gates only by changing the action-level weak-field branch.
- **Derivative-bimetric door: DEAD for the tested local five-invariant action.**
  The vector Ω² operator persists on nonzero MOND backgrounds and the
  independent MOND/slip algebra both fail.  A
  full covariant Dirac derivation would be needed only to promote this bounded
  local result to a theorem for a broader bimetric class.
- **Entire research programme: OPEN, not closed.** No single explicit action
  in the repository has yet met all ten gates simultaneously; the negative
  results are action- and branch-scoped rather than a universal no-go theorem.

## Next unavoidable calculation

For an honestly new candidate, the next calculation is not another static
MOND fit. It is an action-level perturbation test on a nonzero MOND background:
derive the full covariant constraint algebra, then evaluate the anisotropic
scalar principal symbol and the tensor cone on the same branch. Any candidate
that fails that test is discarded before PPN or galaxy fitting. For the
repository's derivative-bimetric door, those local tests now already exhibit
the vector ghost and slip obstruction; the unavoidable follow-up for any
replacement is a genuinely new covariant action and its full Dirac algebra,
then FLRW and data-level predictions.
