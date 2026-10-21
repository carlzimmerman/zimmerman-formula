# The tensor-only correction has a constrained vector kinetic obstruction

**The full cold-energy theory remains open.** The next stability test is now partially resolved: the proposed alpha=1 correction to CFG938 has an explicit negative reduced-vector kinetic interval on its consistent lambda=0 dust background, if that interval lies inside the action's validity range. This statement keeps the metric vector constraint and the homogeneous multiplier. It is stronger than the previous frozen-metric warning. It supplies neither a dwarf formation mechanism nor an exponential growth rate.

**Primary audit verdict: conditional on a named input** for the physical obstruction: the displayed derivative action must apply at the specified wavenumbers and permit its transverse three-label fluid perturbations. The quadratic reduction and sign intervals below are analytic results of that action. No viable correction was asserted in the previous checkpoint; this resolves one of its explicitly untested obligations and retains the earlier tensor cancellation identity.

## Exact claim card and dependencies

Base action: CFG938 `92606e049be780aa6ac7d57de60d97e2324c74b3`, `campaign_fresh_gravity/CFG938_medium_continuum_eft/DERIVATION.md`, with criteria `7a0d41e8b6e3cc12b09326a236dcc39a0f9f3558`. The new operator is the proposal in `../cold_covariant_audit_2026_10_20/RESULT.md`; it is not an adopted change to Claude's action or scorecard.

Use c=1, K=4piG, C=u_medium^mu partial_mu chi, and

    L = R/(4K) - mn - W_full(sqrt(h^munu chi_mu chi_nu))
        - 3 gamma (tau_munu+C sigma_munu)^2/(4K^2)
        + lambda [h^munu nabla_mu nabla_nu chi-Kmn].

Tau is the trace-free projected four-Hessian, and sigma is projected symmetric trace-free medium shear. W_full(s)=s^2/(2K)+O(s^3). Gamma=K Lstar^2/2 is the source convention, not K Lstar^2. Labels are the source's three medium fields. Homogeneous chi/lambda and a flat FRW metric are the background. Background equations are required; a convenient exact branch is identified below.

The dependency chain is: literal action and projector definitions -> transverse ADM expansion -> retained shift constraint -> reduced kinetic form -> analytic sign interval -> background branch and validity-domain interpretation. No external theorem, empirical gravitational-wave bound, static Poisson substitution, or rerun of Claude's dynamics is used. Additional matter is handled under explicitly stated ideal-fluid assumptions; arbitrary S_b is not silently solved.

## Geometry before eliminating the shift

For a transverse perturbation use spatial-vector gauge E_i=0 and retain the ADM shift,

    ds^2 = -dt^2 + a^2 delta_ij (dx^i+S^i dt)(dx^j+S^j dt),
    div S=div pi=0,   phi^I=x^I-pi^I.

In particular g00=-1+a^2 S^2; setting g00=-1 while retaining the shift would change this quadratic calculation. Define physical Fourier velocities U=a pi_dot, B=a S and V=U+B, and physical wavenumber q=k_com/a. A common positive Fourier phase-average factor is normalized consistently across all terms.

The covariant expansion gives

    sqrt(-g) mn = a^3 rho (1-|V|^2/2) + spatial divergence,
    h^munu chi_mu chi_nu = C^2 |V|^2,
    h^munu nabla_mu nabla_nu chi
        = -3HC + (C_dot-HC)|V|^2 + O(3).

There is no linear transverse scalar constraint. Scalar chi/lambda perturbations therefore do not mix bilinearly with this transverse irrep on an isotropic background. Their background values still contribute. Dust, W and the multiplier yield

    A0 = rho(1+K lambda_bar) - C^2/K
         + 2 lambda_bar(C_dot-HC).

Using K rho=-3HC, this is also rho-C^2/K+2lambda_bar C_dot-5lambda_bar HC. Lambda has not been discarded or assigned a value in the reduction.

For the corrected tensor, direct connection/projector contraction gives

    delta(tau+C sigma)_ij = C a^2 partial_(i)(pi_dot+S)_(j),
    [delta(tau+C sigma)]^2 = (C^2/2) q^2 |V|^2,
    L_tidal,V^(2) = -3 gamma a^3 C^2 q^2 |V|^2/(8K^2).

The operation that cancelled the homogeneous tensor shear has introduced a medium relative-velocity gradient. Einstein-Hilbert supplies

    L_EH,V^(2) = a^3 q^2 |B|^2/(8K).

Thus, per transverse polarization,

    L_V^(2) = a^3/2 [ A(q)|U+B|^2 + b(q)|B|^2 ],
    A(q) = A0 - 3gamma C^2 q^2/(4K^2),
    b(q) = q^2/(4K).

Vary B only now. For A+b != 0,

    B = -A U/(A+b),
    L_V,reduced^(2) = a^3/2 I_V |U|^2,
    I_V = A b/(A+b).

The sign of A alone was insufficient in the earlier fixed-metric diagnostic. This reduced coefficient includes the actual vector metric constraint. At A+b=0, division is invalid and constraint rank must be analyzed separately.

## Exact sign result and consistent background

Let d=3gamma C^2/K>0, so A=A0-d b. For A0>0 and q>0:

- If 0<d<=1, the denominator A0+(1-d)b is positive and I_V<0 whenever b>A0/d.
- If d>1, I_V<0 on A0/d<b<A0/(d-1). This interval is nonempty because d>d-1>0. The upper endpoint is a shift-constraint pole; beyond it the formal reduced coefficient becomes positive. The naive statement that every sufficiently high-k vector is negative is incorrect in this regime.

A=0 is the first kinetic degeneracy. The pole A+b=0 is a different locus. Neither is an ordinary propagating normal mode.

The homogeneous chi equation for this action is

    d(a^3 H lambda_bar)/dt = 0.

Consequently lambda_bar=0 is a consistent exact branch, rather than an assumption that all multipliers vanish. The multiplier constraint still fixes -3HC=K rho. On that branch W and tidal terms vanish in the background; Einstein plus the declared dust/radiation matter gives H^2=2K rho_tot/3. If 0<f=rho/rho_tot<=1,

    C^2/K = rho^2/(6rho_tot),
    A0 = rho(1-f/6) > 0.

The first negative-band threshold is then

    q^2 Lstar^2 = 16/f - 8/3.

A hand-computable single-medium dust example is K=gamma=1, rho=rho_tot=6, H=2, C=-1 and lambda_bar=0. It satisfies both -3HC=K rho and H^2=2K rho_tot/3. At q^2=8, A0=5, d=3, b=2, A=-1 and I_V=-2; A+b=1 is nonzero. The corrected tensor coefficient is still Q_T=1. These are dimensionless algebraic branch values, not fitted cosmological or dwarf parameters. They display the finite adverse vector direction without evaluating at a constraint pole.

This is a physical-wavenumber relation, not a measured microscopic cutoff. A cutoff below this threshold is not ruled out here, and the source has not supplied a justified one that removes the interval. For a nonzero lambda background, derive its complete consistent solution and evaluate A0 before transferring this branch-specific sign conclusion.

The perfect-fluid vorticity sector has no ordinary transverse elastic restoring gradient. A negative kinetic direction gives an adverse energy sign; this calculation does not derive a rate proportional to imaginary frequency, a nonlinear runaway time, or a quantum completion verdict.

## Additional matter and permitted perturbations

If other healthy minimally coupled ideal fluids carry transverse velocities U_j, retain them before solving the shift:

    L^(2) = a^3/2 [ A|U+B|^2 + sum_j A_j|U_j+B|^2 + b|B|^2 ],
    A_j > 0.

The reduced matrix is diag(A,A_1,...)-w w^T/(b+A+sum A_j), with w=(A,A_1,...). On the admissible velocity subspace U_j=0, its medium-direction coefficient is A(b+sum A_j)/(A+b+sum A_j). It remains negative immediately after A crosses zero, while the denominator is positive. Healthy extra fluids can shift the pole, and do not remove that first adverse direction under these assumptions. Alternatively zero conserved transverse momenta of the extra ideal fluids gives the medium-only expression by Routh reduction. Arbitrary nonideal/anisotropic S_b requires its own complete vector analysis.

The displayed three-label action has physical time-dependent vortical velocities. Time-independent volume-preserving relabelings cannot gauge them away. A separately imposed irrotational restriction could exclude this sector only by an additional constraint or a demonstrated nonlinear consistent truncation; that is a different, presently unproved route. The source's curl-free P/static-spherical scope does not itself add such a variational constraint to its displayed three-label action. This distinction must be retained when interpreting the result.

## Evidence and independent review

`vector_root/vector_geometry_check.py` starts from the four-dimensional ADM metric, derives its connection, projector, four-Hessian and medium shear through second order, and independently obtains the coefficients above. It includes dust, W, background lambda, an ADM EH calculation, exact shift elimination, sign controls and a healthy extra-fluid kinetic-matrix check.

`vector_root/run_001/` is completed: 28 controls pass, peak RSS 55,689,216 bytes, runtime about 0.92 s. The v2 manifest validates against current input/output hashes. One transverse polarization and its exact rotationally equivalent sector are derived; check counts do not establish the physical theory. The analytic sign inequalities, not selected parameter values, establish the entire stated interval.

Two separate analytic derivations are in `vector_review/` and `vector_independent/`. They were given the action and task rather than root code or a guessed reduced formula; both obtained the same shift reduction and multiplier coefficient. Their final notes and exact source receipts are retained. Agreement is supporting review, not a replacement for the derivation. Root geometry run and manuscript scope received a further focused check.

Obligations: action/source identity PASSED; vector geometry and shift reduction PASSED under stated field content; lambda0 branch PASSED; physical validity/cutoff CONDITIONAL; arbitrary S_b NOT ADDRESSED; longitudinal scalar block and full degree count NOT ADDRESSED; dwarf binding/transport/normalization OUT OF SCOPE and still open.

## Claude arrivals and consequence

Since the preceding checkpoint b5e54cc3, clock-projected microscopic results `65be2b68` and their registry `f1565bc9` concern distinct scalar/unit-vector actions. Their conditional ratios and retained tilt failures do not repair CFG938. New curved-constraint criteria `201229b5` likewise specify different actions; no same-action live experiment was duplicated. Exact committed bytes and raw log/manifest bindings are recorded in `formation/`.

CFG938/939/940 have no new finalized receiver/selector result in this source interval. At the first snapshot, CFG935's new A2 softening followed a partial conservation failure and was uncommitted; amended dynamics/outcomes remain provisional. Its new outputs cannot be promoted to a settling or dwarf-budget result. `shell/` retains the narrow live/source comparison, including the uncommitted-versus-committed distinction. A late arrival, `407e7054b48463ed9a8d88bcc19c647ee01438fc`, commits the A2 amendment alone; this supplies amendment provenance, not a new finalized A2 result. See `shell/LATE_A2.md`.

The original CFG938 tensor counterexample remains intact. The alpha=1 candidate retains its tensor cancellation/static first-variation identity but now has a stronger conditional vector obstruction. It does not supply cold-cold attractive binding. The next route is a genuinely constrained/degenerate or restricted field-content action with explicit validity range, followed by the missing scalar analysis and common binding/source/normalization bridge. Actual E/Q/orbital-J export and all four dwarf mass/stellar-profile budgets remain required; no additional cooling efficiency alone resolves those gaps.
