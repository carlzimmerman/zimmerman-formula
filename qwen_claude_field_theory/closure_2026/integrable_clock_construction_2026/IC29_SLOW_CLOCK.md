# IC29: preserve constant tensor coupling while slowing the clock

Base 9eefad6c77bd6aef8b762f3f130347fc7988feec, 2026-09-09.
Full theory **OPEN**. The preceding goal turn was substantive progress:
it derived physical slip and built the constant-tensor branch. This turn
attacks its actual short background lifetime rather than restarting that work.
Credit: Carl Zimmerman's exponential kernel, vacuum-scale relation and
primordial-clock idea motivate the construction. No empirical or priority
claim is made.

## 1. Selected explicit theory

Use the FULL IC20 first-order covariant phase action, with the IC28 replacement
v=v0=exp(S+2w)/2 throughout, and the same two minimally coupled matter actions.
Keep A(S)=.1 and E4(S)=.01. Construct ONE D(S) by the following IVP, with
initial S=.1,q=-3,z=1,Q=0 and the specified IC23 matter amplitudes.

    D=h_z|D=0/(2z),
    D'=[h_S|D'=0+rhoH]/z²,
    D''=[h_SS|D''=0+rhoH-h_Sz²/h_zz-M_*]/z²,
    M_*=-1000.

Each raw partial derivative uses independent S,q,z and S-only coefficient
jets. The actual auxiliary preservation matrix then solves Sdot and zdot,
while Qdot=h_q/2 and qdot=-3(h-pH)/2. These are evolved together.
The construction does NOT prescribe Sdot in the field equations.
Directional derivatives check Ddot=D'Sdot, (D')dot=D''Sdot and charge
conservation. Off-shell variations keep the resulting D fixed as a function
of S only. Third coefficient jets in the Euler matrices come from that same
integrated function.

The selected action also sets the already-present activation scale h0=.5
in r=-exp(-3wc)q/(3h0), with eta(r) as defined in IC18. This is an EXPLICIT
global action-parameter change from h0=1, not an unnoticed rescaling of time.
On eta=1 the pinned equations are independent of h0, but the transition
sector is not. No transition result is inherited from the old choice.

## 2. Why this change addresses the observed failure

The actual lapse-preservation equation is

    Sdot=[3Qdot(rhoH+pH)-C qdot]/M_*.

At the initial state, M_*=-1000 gives Sdot=.01163260223 and
zdot=-.9719875002, instead of3.877534077 and-60.27335544 at M_*=-3.
This is a derived multiplier response to an action coefficient choice,
not an independently imposed clock law. Slower evolution avoids the early
z-to-zero motion seen in IC28 over the new tested history.

With the old h0=1 activation, the slower background approaches the actual
pin transition near one e-fold. The original diagnostic also contained a
numerical trap: a positive mpmath eta could underflow to zero when converted
to double precision. A regression test now exercises that case.
Domain checks use r²-1/2 before conversion, and records retain eta as a
decimal string and its logarithm. The h0=1 control is still run and retained.

The h0=.5 selected trajectory is checked against r²>3/4 at every stored
state, not merely eta>0. A preliminary seven-e-fold run stays in that
plateau. This avoids divisions by a tiny activation coefficient on that
trajectory; it does not establish the global pin-off matching.

## 3. Same-action metric, modes and propagation

The IC28 identities H_qR=H_RR=0, H_SR=-v0 and tdot/t=Sdot hold for arbitrary
D(S) on the active homogeneous pin. The two independently reconstructed
potentials therefore continue to give Phi=Psi, with physical tensor
normalization M_T²=1 and c_T²=1. The script evaluates those quantities from
the actual raw and reduced coefficients at evolved states.

Local 4x4 auxiliary Poisson matrices are computed separately at k=0 and
nonzero modes. Their sampled ranks are not a nonlinear functional Dirac
count. All six scalar/matter Euler roots are kept. The clock remains an
explicitly counted physical scalar candidate, not an auxiliary renamed
to evade the requirements.

The complete six-dimensional time-dependent Hamiltonian generator is
integrated over Q in[0,1] for initial k²=.001,.01,.1,1,10,100. Each wave
redshifts as k²(Q)=k_initial² exp(-2Q). Two operator interpolation grids
are compared. The canonical-density flow has divergence -9Qdot, hence
its transfer determinant is exp(-9 Delta Q); this is checked numerically.

The code also propagates both physical metric response rows independently.
Their agreement is checked after evolution. Their norms are responses per
unit of the fixed initial kinetic norm, not empirical growth factors.
No universal stability threshold is inferred from finite amplification.

## 4. Hold the coefficient function fixed while changing matter

The off-trajectory test first builds a fixed quintic-Hermite representation
of the constructed D(S), using its value and first two derivatives at
reference background nodes. Derivatives are then taken from that ONE
polynomial, evaluated without casting the varied S to double precision.
Changing the matter amplitudes NEVER calls the construction equations to
retune D at the new source.

For source factors2,10,1000 the actual h_S+rhoH=0 and h_z=0 equations are
solved at q=-3,Q=0. Their analytic Jacobian uses the fixed polynomial jets.
The lapse Schur is an OUTPUT in this test and is not forced to stay -1000.
Physical no-slip, regularity and actual local brackets are recomputed.

Two table resolutions,41 and81, test numerical sensitivity, and off-node
coefficient jets are compared with the reference construction. Each fixed
table is a C2 approximate action, not an exact globally smooth extension.
Their results supply numerical evidence for source robustness of the implicit
D(S); they do not prove convergence or turn distinct approximations into
an exact full-theory certificate. No extrapolation beyond the constructed
S interval is allowed.

## 5. Executed bounds and what remains

Construction: Q1 with step.005/rtol1e-12 and Q7 with steps.02/.01 at
rtol1e-11;3000-step cap. Modes at Q=0,.1,1,7 and k²=.001,.1,1,100,1e14.
Propagation: Q[0,1],81/161 operator nodes, six initial wavelengths.
Sources: the fixed41/81-node coefficient approximations described above.
Each recorded job has300sec wall and2MiB log caps, with a cooperative
one-thread numerical-library limit; no hard memory or CPU-affinity cap.

Long-history charge drift must be reported, not hidden by small coordinate
differences. More e-folds are not a substitute for a well-defined limiting
coefficient function or controlled nonlinear interaction scales.

Still required for the full goal: the global D(S) extension and asymptotic
regularity; general nonlinear Dirac closure; physical causal support despite
elliptic constraints; finite-wavelength and nonlinear stability; pin-off,
zero-field and static MOND variations; measured G and full PPN; realistic
matter/plasma and actual galaxy, cluster and CMB data. The a0-Lambda relation
and its normalization remain input. There is no Lean certificate or novelty
certification. Mathematical proofreading and computation checks are self-review.
