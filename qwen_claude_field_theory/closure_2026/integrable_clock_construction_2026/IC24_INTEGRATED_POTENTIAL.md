# IC24: an integrated action coefficient, not independent pointwise repairs

Base: `12fd52243236cacda49b58224e6876e6ca5531ec`, plus the recorded IC23 working
tree. Full theory **OPEN**. Carl Zimmerman's exponential MOND kernel,
vacuum-scale relation and primordial-clock proposal motivate this construction.
No empirical calibration or novelty priority is established here.

## Action and construction contract

Keep the IC20 action and the TWO simultaneous minimally coupled IC23 matter
actions, but replace the prescribed exponential D(S) by a coefficient defined
by the following initial-value problem. Keep A(S), E4(S) and all other
functions unchanged. The pinned flat-background gravitational density is

    h = -exp(2S)q²/(6v) - A(S)qz - exp(S)P0(S)
        - D(S)z² - E4(S)z⁴,   v=exp(S+2wc)/2+z².

The full covariant first-order action, not just this background restriction,
is defined in IC20_JOINT_COMPLETION.md. The replacement is D(S) ONLY; it adds
no momentum or matter dependence to the action coefficient. Its domain is a
local interval traversed by S, not a supplied global extension to the static
branch. The construction is designed using one matter background. Healthy
behavior on other backgrounds of this same function is a separate obligation.

Let rhoH=sum h_i, pH=sum w_i h_i, Q=ln(barred scale factor), and target a
negative auxiliary lapse Schur coefficient M_*=-3 (an engineering choice in
the normalized model, not a measured number).

At a point (S,q,z,Q) with z>0, determine coefficient jets in this order:

    D = h_z|D=0 /(2z),
    D' = (h_S|D'=0 + rhoH)/z²,
    D'' = (h_SS|D''=0 + rhoH - h_Sz²/h_zz - M_*)/z².

Each subsequent line uses the preceding jets. Raw partial derivatives are
derived from the action with coefficients regarded as functions of S alone.
After inserting the jets, compute, rather than assign,

    M=h_SS+rhoH-h_Sz²/h_zz,
    Qdot=h_q/2,   qdot=-3(h-pH)/2,
    [[h_SS+rhoH,h_Sz],[h_Sz,h_zz]] (Sdot,zdot)^T
      = -(h_Sq qdot-3Qdot(rhoH+pH), h_qz qdot)^T.

Evolve d(S,q,z)/dQ=(Sdot,qdot,zdot)/Qdot. Initial (S,q,z) is the actual
IC23 mixed constraint solution at q=-3,Q=0, with Mr=Mm=10^-6 and wm=10^-8.
The new second jet differs intentionally from IC23; their spectra are not
pooled as though they were the same action.

## Integrability lemma

Assume the reconstruction and flow are differentiable, z!=0, Qdot!=0,
h_zz!=0 and M_*!=0. The reconstruction satisfies Fz=h_z=0 and
FS=h_S+rhoH=0. Differentiate Fz along the reconstructed trajectory, allowing
D to be an initially independent coefficient value. Subtract the varied
preservation equation. The difference is

    -2z [Ddot-D'Sdot]=0.

Thus Ddot=D'Sdot. Differentiating FS and subtracting its preservation equation
then leaves

    -z² [(D')dot-D''Sdot]=0.

Hence (D')dot=D''Sdot. These identities make the reconstructed jets derivatives
of one function wherever S is locally invertible. Numerical directional
derivatives check both identities independently of the jet-selection formula,
as well as d[exp(3Q)(h+rhoH)]/dt=0. If Sdot vanishes, invertibility must be
reassessed; dividing by Sdot is not allowed without additional compatibility.
This is a conditional local integrability argument, not a global existence
or interval-certification theorem.

## Auxiliary and perturbation checks

The same-action auxiliary block has Schur complement

    M(k)=M_*-2B k²,   B=exp(S+2wc)(1-u²)>0.

On this regular pinned branch with h_zz<0 and M_*<0 it cannot have a spatial
zero for any real k. The actual four-by-four Poisson matrix, including its
secondary-secondary block, is built and numerically ranked at k²=0,1,10000.
This does not prove general nonlinear functional closure or the pin-off
stratum. The local clock remains one explicitly counted scalar, in addition
to two tensors and the two genuine matter scalars.

The IC23 three-field quadratic action is evaluated with the new raw action
jets. Time derivatives use D'''=(dD''/dt)/Sdot along the IVP. Crucially, the
off-shell differentiation uses a Taylor function of S alone with these jets,
NOT algebraically reconstructed D(S,q,z,Q). This distinction prevents a
spurious momentum-dependent action from masquerading as the proposed theory.
All six instantaneous roots and all kinetic eigenvalues are retained.
Finite-k roots are not, by themselves, cosmological growth histories or
characteristic signal speeds. The homogeneous background and k=0 constraint
block are tested separately; the spatial scalar reduction uses k!=0.

## Bounded result and remaining calculation

The first numerical continuation with DOP853 (relative tolerance 10^-10,
maximum Q step .0002; mpmath30 coefficient evaluation) carries the branch
beyond the IC23 light-cone crossing Q~.00372333. A new light-cone event occurs
at Q~.0486008725; the requested Q=.1 is NOT reached. At the new event,

    S~.1112448918, q~-2.9182139850, z~.9757976648,
    (D,D',D'')~(.8721840751,11.11940028,-112.7118323),
    h_zz~-4.879489, M=-3, H_physical~.3251384,
    coupled c²~(1,.3333331158,9.9999966e-9).

Charge drift is about 2.9e-15 in normalized units on that run. The event point
is a boundary, not a strictly subluminal interior point. Sampled sign checks
do not exclude an unsampled excursion. A finer-step/tolerance run and actual
finite-wavelength spectra are recorded in the companion computation output.

This is a successful integrated local repair, not a healthy long cosmology.
The next constructive calculation is to vary a second coefficient function,
A(S), together with D(S): use the combined characteristic inequality to
determine its first derivative while the lapse-Schur condition determines
the potential's second derivative. Integrate both and check compatibility;
do not merely prescribe a sound speed in the perturbation equations. If the
first-derivative branch folds or S turns, identify and resolve that singularity.

Static/zero-field extension, Phi/Psi, measured Newton constant, PPN, nonlinear
Dirac closure, relative flows, interactions/strong coupling, plasma evolution
and empirical galaxy/cluster/CMB fits remain open. The a0-Lambda relation and
its normalization remain input. No Lean certificate or independent review is
claimed. Mathematical proofreading and computation self-review cover this
note and its new script only. Exact commands and statuses are in the run index.
