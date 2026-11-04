# Independent audit: protected neutral fermion and photino current

**Normalized claim.** For the specified n=3-epsilon logarithmic K, quartic
H, W_SU5+W0, constant gauge kinetic data, and finite rigid-CW stationary
point, the uneaten neutral pole has mass epsilon/n m32, retains matter
current sqrt(n/3)/F_hidden, and gives the quoted photino lifetime.

**Primary verdict: incomplete, with the smallest missing implication being
the transverse neutral 1PI two-point function.** Exact tree geometry and
the leading current projector pass this audit. The 81.1811 eV number is
the result of a particular Ward-completing prescription; scalar
stationarity and the Ward identity alone do not determine it. This does
not refute that number for the fixed model. Its missing correction is an
uncomputed property of that model, not an extra adjustable parameter.
The quoted 1.32489e20 s has a useful stronger interpretation that does not
require the 81 eV pole: **with the stated leading rigid dipole held fixed,
it is a lower bound on this partial lifetime**, attained for a massless
accessible final fermion. It is not an established total lifetime.

## Severity and exact scope

| Finding | Severity | Scope and consequence |
|---|---|---|
| The Ward-completed matrix is not uniquely fixed by the scalar action | P1 for the requested complete gravity/production result | A physical neutral pole and scalar-to-fermion-pair vertices remain uncomputed. No numerical bound on the missing transverse self-energy is supplied. |
| Calling epsilon/n m32 a physical eigenvalue without its prescription qualifier | P2 claim calibration | `DERIVATION.md:162` and its opening paragraph are stronger than the later explicit caveats. `finite_normal.py:58` assigns the formula rather than deriving a finite-normal pole. |
| Leading hidden-current normalization | Passed in the declared small-field/rigid-current limit | Replacing F_hidden by F_total would spuriously lengthen the lifetime by about 30000. |
| Unknown neutral mass versus partial survival | Passed as a fixed-current upper-width bound | Unknown mass can reduce or close this channel; it cannot increase its phase space beyond the massless value. Missing current corrections and other loss channels remain outside the bound. |
| W0 sensitivity versus total vacuum cancellation | Passed, after distinguishing the two quantities | Fractional W0 precision is about 3.583e-75 under correlated auxiliary response. The positive auxiliary vacuum energy is about 4.186e78 rho_DE, much larger than F_hidden^2/rho_DE. |

## Dependency graph and obligation matrix

The exact K,W imply the complex metric, potential, tree auxiliaries and tree
mass Ward identity. The finite scalar functional supplies a stationary
background. These data fix the eaten vector and constrain the action of
the completed mass matrix on that vector. An additional **unverified**
arrow identifies the full transverse mass/kinetic functions and vertices
with the TT-only reconstruction. The leading rigid transition operator
plus the geometric current projector separately imply a fixed-current
partial-width upper bound. Neither branch determines all production
vertices or all photino loss channels.

| Obligation | Status |
|---|---|
| Complex metric, positive domain, no-scale cancellation | Passed, by direct differentiation and Schur complement below |
| Proper K-normalized eaten and orthogonal directions | Passed at leading small field; finite effective-metric corrections uncomputed |
| Raw tree mass and tree scalar Ward relation | Passed at the stated leading stabilized jet; independently differentiated |
| TT rigid Ward prescription produces epsilon/n m32 | Passed as a conditional algebraic statement |
| Stationarity uniquely fixes the physical transverse mass | Failed as an inference; explicit Ward-null family below |
| Missing 1PI terms are quantitatively subleading to 81 eV | Not established by the submitted artifacts |
| Hidden rigid-current projector and massless partial-width bound | Passed at that leading operator order |
| Finite anomaly/Higgs thresholds and complete transition current | Conditional; not computed here or by the submitted packet |
| Actual radial/phase pair-production widths | Not addressed by this matrix/current projection |
| W0 sensitivity at the preferred scalar packet | Independently verified at one packet |

## Independent tree geometry

Set k=sum |phi_i|^2, P=H_tau, Q=H_tau,taubar,
Y=H-k/(nM^2), D_H=|P|^2-HQ. Differentiating K gives

    g_tau,taubar = nM^2 (|P|^2/Y^2-Q/Y),
    g_tau,jbar   = -P phi_j/Y^2,
    g_i,taubar   = -Pbar phibar_i/Y^2,
    g_i,jbar     = delta_ij/Y+phibar_i phi_j/(nM^2 Y^2).

The matter block B has ordinary inverse

    B^-1 = Y [I-phibar phi^T/(nM^2 H)].

Its modulus Schur complement is nM^2 D_H/(YH). Thus for n>0 the full metric
is positive precisely on Y>0,D_H>0, with H then positive. Keeping the
ordinary inverse's index orientation, the scalar contraction is
Dbar^T g^-1 D. Completion of the remaining rank-one block yields

    V=Y^-n [Y sum|W_i|^2+(n-3)|W|^2/M^2
            +Y Q |sum phi_i W_i-nW|^2/(n D_H M^2)].

For n=3,Q=0 this is Y^-2 sum|W_i|^2. A constant W0 cancels its own no-scale
contribution; it does not cancel a nonzero matter source. I find no
complex-conjugation or inverse-metric error in `exact_geometry.py:14-24`.

## Fresh light-matrix derivation and its exact ambiguity

Use canonical light basis (sqrt(n)M chi_tau,chi_T), and write m=m32.
At leading small matter/M the tuned relation is F^2=epsilon m^2 M^2.
The quartic modulus stationarity gives, to the same order,

    H=1, P=1, Q=H_tau,tau=0,
    H_tau,tau,taubar=-epsilon/n.

The last jet follows from tau+taubar-1=-epsilon/(24 n b). It cannot be
discarded just because the displacement itself is tiny. Direct
differentiation of e^(K/2) nabla_i D_j W, using W=W0+FT for the light
fields, gives the pre-unitary matrix

    R_tree/m = [[n-1+epsilon/n, -(n-1)sqrt(epsilon/n)],
                [-(n-1)sqrt(epsilon/n), 0]].

The normalized auxiliary/eaten and orthogonal directions are

    eta = (-sqrt(n),sqrt(epsilon))/sqrt(3),
    zeta= (sqrt(epsilon),sqrt(n))/sqrt(3).

The tree Ward contraction already vanishes in the modulus equation, but
its matter component has residual -epsilon sqrt(epsilon) m^2 M. Adding
only Delta R_TT=epsilon m cancels that residual. Subtracting the usual
rank-one gravitino mixing term then gives

    U0/m = [[epsilon^2/(3n), epsilon sqrt(epsilon)/(3sqrt(n))],
            [epsilon sqrt(epsilon)/(3sqrt(n)), epsilon/3]],
    U0 eta=0,       zeta^T U0 zeta=(epsilon/n)m.

This independently reproduces the submitted **prescription** and explains
why the tree-off-shell projected -162 eV value cannot be read as a pole.
It does not show that the prescription contains every term of the same
accuracy. In particular, for every real a on this CP slice,

    U(a)=U0+a m zeta zeta^T,
    Delta U/m=(a/3)[[epsilon,sqrt(n epsilon)],
                    [sqrt(n epsilon),n]],
    U(a) eta=0,
    zeta^T U(a) zeta=m(epsilon/n+a).

Adding the same Delta U to the pre-unitary matrix preserves its stationary
Ward contraction too. This is the full one-dimensional transverse freedom
of a symmetric 2x2 matrix with a specified null vector. The exact symbolic
control verifies it, without importing any submitted implementation.

Here a parametrizes **what the available identities fail to determine**.
It is not a freely selectable deformation of the stated UV action. A
matched calculation in that action determines a, momentum dependence,
wavefunction residues, and corrections to the auxiliary direction. The
scalar CW function alone does not supply those quantities. At the finite
displaced heavy normals, rigid Ward completion also requires the
heavy-light entries; the TT-only insertion in `solve_protected.py:108`
does not supply them. The finite implementation correctly acknowledges
this and quotes a leading estimate instead (`finite_normal.py:58-60`).

The numerical equality/null checks in `exact_geometry.py:53-61` verify a
matrix that was entered explicitly. They cannot discriminate U0 from
U(a). No submitted run evaluates or bounds a or the corresponding
effective kinetic correction. To establish a relative mass accuracy it
would be necessary, in these conventions, to bound |a| relative to
epsilon/n=3.33344e-5, together with the metric/residue corrections. Weak
couplings and small field/M ratios motivate a controlled expansion, but
are not a calculated bound on the coefficient of this cancellation-
suppressed mass. This audit does not assert that the missing correction
is large; it establishes that the claimed quantitative smallness has not
been demonstrated.

The primary tree source gives the eaten vector and covariant mass matrix,
with Kähler kinetic normalization; it does not turn an off-shell
tree-plus-scalar-loop ansatz into a loop pole. See Eqs. 36-37 and the
tree-level scope of [1104.2598v2](https://arxiv.org/pdf/1104.2598).

The massless modulino theorem is also not a substitute: its almost-no-scale
construction assumes the required sequestering, uplifting-sector
conditions, stationarity and V=0. The paper explicitly distinguishes a
tree result from possible loop masses. The present n=3-epsilon model and
nonzero matter background require their own matching. See Section IV,
especially Eqs. 33-39 of [1104.2600v3](https://arxiv.org/html/1104.2600v3).

## Current and the conclusion that survives the mass ambiguity

In the leading canonically normalized two-light-dimensional space,

    chi_T=sqrt(epsilon/3) eta+sqrt(n/3) zeta.

Therefore the existing rigid matter current couples to zeta with amplitude
sqrt(n/3)/F_hidden. A large modulus auxiliary mainly rotates which
Goldstino is eaten; it does not dilute this uneaten current by replacing
F_hidden with F_total. Here F_hidden=5.930081448e13 GeV^2 and
F_total/F_hidden is approximately sqrt(3/epsilon). The source coefficient
and the tree geometric overlap are justified at this order. Effective
kinetic/current matching is still needed to attach high precision to an
individual physical pole's overlap.

For the fixed operator in the proposal, let Gamma0 denote the massless
final-fermion width. Then

    Gamma0=(n/3)m_chi^5/(16 pi F_hidden^2),
    Gamma(m_zeta)=Gamma0 [1-m_zeta^2/m_chi^2]^3 <= Gamma0

when the channel is open, and Gamma=0 when closed. Independently using the
preferred packet gives

    Gamma0=4.968058139e-45 GeV,
    tau_partial >= 1.324887790e20 s.

Thus the unknown transverse mass does not undo the leading partial-channel
age test, whose margin is about 304 relative to 4.354e17 s. An equality
near this bound requires a sufficiently light accessible state. If
mixing redistributes a fixed current among several orthonormal neutral
states, summing positive phase-space-weighted widths cannot exceed the
unweighted current norm; an inclusive version of the bound remains.
This is a statement about a specified leading current. It neither bounds
unknown additional transition operators nor sums all gravity loss modes.

The anomaly distinction in the proposal is correct: the eaten-Goldstino
coupling is c_lambda=m_lambda-m_AdS, rather than automatically the full
gaugino mass. Keeping the super-Weyl, Kähler and sigma-model terms gives
the stated small-field epsilon(T_G-T_R)m32 mass combination. That algebra
does not match finite Higgs thresholds or establish the uneaten current.
See Eqs. 3.11-3.15 of [1202.1280v3](https://arxiv.org/pdf/1202.1280v3).

In particular, this dipole projector cannot provide radial/phase decays
into two uneaten fermions. Even a known stationary m_zeta would not fix
its scalar derivatives or the required cubic 1PI vertices. That remains
a production obligation, independently of the partial photino bound.

## W0 convention: large cancellation and smaller sensitivity

At a stationary minimum, the envelope theorem permits differentiating
with respect to W0 at fixed fields. The specified loop functional has no
explicit W0 dependence. The leading reduced potential is

    V_eff=F_hidden^2-epsilon |W|^2/M^2+V_loop+...,
    dV_min/dW0=-2epsilon Re(W)/M^2+... .

This is the actual sensitivity along a variation that also changes the
modulus auxiliary. It differs from varying only the universal negative
term while holding the positive total auxiliary norm artificially fixed.

Using a direct inverse of the full four-field tree metric at the preferred
serialized packet gives

    dV/dW0 = -4.870703579e-7 GeV,
    (dV/dW0)/[-2epsilon W/M^2] = 1+3.47e-14,
    rho_DE / |W0 dV/dW0| = 3.583019775e-75.

At the same point,

    positive total auxiliary energy = 1.054976036e32 GeV^4,
    positive total auxiliary energy / rho_DE = 4.186412843e78,
    F_hidden^2 / rho_DE = 1.395470872e74.

The positive auxiliary contribution has W0 slope +0.01461162367 GeV;
the universal negative contribution has slope -0.01461211074 GeV.
Their correlated difference is the epsilon-suppressed slope above. Thus
the approximately 3.58e-75 W0 precision is internally consistent, and
does not mean that the full positive-versus-negative vacuum cancellation
is only one part in 1e74. Its residual-to-positive-energy ratio is about
2.39e-79. Both diagnostics are conditional on the chosen finite action;
neither selects rho_DE, and omitted vacuum corrections require retuning.

## Evidence, reproduction and remaining check

The independent control uses a Kähler jet differentiated from K itself,
not the author's mass formula, and a direct finite-packet inverse metric.
All 12 finite/symbolic assertions passed. The installed mathbox v2 runner
completed in less than 2 seconds; child reported 0.690 s and measured RSS
54,116,352 bytes. `run_control_001/manifest.json` validates with current
input hashes and status `completed`. No submitted scalar solve was rerun
or replaced. `provenance.json` pins every inspected submitted source or
result used in this audit; the shared branch can change independently.

Exact reproduction command, from the project root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract reviews/gravity_completion_2026_11_03/protected_review/control_contract.json --input reviews/gravity_completion_2026_11_03/protected_review/independent_control.py --input reviews/gravity_completion_2026_11_03/protected/run_export_002/result.json --output reviews/gravity_completion_2026_11_03/protected_review/run_control_001 --result reviews/gravity_completion_2026_11_03/protected_review/run_control_001/result.json --timeout 60 --max-cpu-seconds 55 --max-threads 1 --max-output-bytes 1048576 -- python3 reviews/gravity_completion_2026_11_03/protected_review/independent_control.py reviews/gravity_completion_2026_11_03/protected_review/run_control_001/result.json
```

The runner output directory must be fresh when reproducing. The three
primary arXiv versions were authenticated by direct web reads on
2026-11-03; 1104.2598's unversioned PDF identified itself as v2,
1104.2600 HTML identified v3, and 1202.1280 PDF identified v3. No full
external paper was persisted. These source checks validate the formulas
and their scope, not the missing project application.

The cheapest decisive next physics check is the projected zero-momentum
neutral self-energy and wavefunction residue at this background, with
modulus/heavy-light components retained and the same finite scalar
functional's Ward relation checked. That fixes the coefficient left
undetermined above; a scalar-force-derived TT insertion alone cannot.
For production, the corresponding scalar derivatives and cubic vertices
remain separate required output. Review provenance: fresh independent
subagent derivation, followed by a bounded independent symbolic/numerical
control; shared model-family limitations still apply.
