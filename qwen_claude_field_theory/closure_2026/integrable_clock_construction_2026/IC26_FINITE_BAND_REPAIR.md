# IC26: finite-band repair through a third action coefficient

Base `b2a5cc4ec32122984c19e5749e29a15b191ae716`, 2026-09-09.
Full theory **OPEN**. This continues Carl Zimmerman's exponential MOND kernel,
vacuum-scale relation and primordial-clock construction; no new empirical
fit, priority claim or completed relativistic theory is announced.

## 1. Check the quadratic derivation before altering the theory

The IC25 k_initial²=100 propagator amplified by about2.26e5 over Q in[0,1].
That result survived an independent60-digit calculation. We first checked
whether the homogeneous quadratic expansion had dropped gravitational mass
terms. It had not.

For physical trace perturbation p=delta q, scalar metric perturbation zeta
and volume V exp(3zeta), the gravitational canonical term is

    V exp(3zeta)[2(q+p)(Qdot+zetadot)-h(q+p)].

At second order, integration by parts of 6Vq zeta zetadot and the actual
background equations Qdot=h_q/2, qdot=-3(h-pH)/2 leave

    L2_gravity/V=2p zetadot-h_qq p²/2-(9/2)pH zeta².

For each matter Hamiltonian h_i exp(-3w_i zeta)(1+s_i/j_i)^(1+w_i), its
quadratic zeta mass is (9/2)w_i²h_i and its zeta-s_i cross coefficient is
-3w_i u_i. Thus the combined Hamiltonian mass is exactly
(9/2)sum w_i(1+w_i)h_i, as used in IC23-25. These cancellations and matter
derivatives are checked symbolically. There is no missing homogeneous term
to remove the observed growth by a bookkeeping correction.

## 2. One action with three reconstructed functions

Keep the full IC20 covariant first-order action and the two IC23 minimally
coupled ideal-fluid matter actions. Replace A(S),D(S),E4(S), and nothing
else, by functions defined through the following construction IVP. The
pinned density is

    h=-exp(2S)q²/(6v)-A(S)qz-exp(S)P0(S)-D(S)z²-E4(S)z⁴,
    v=exp(S+2wc)/2+z².

The tensor, curvature and spatial terms remain those in IC20; the displayed
density is not substituted for the full covariant action. The functions are
defined on the traversed S interval, not yet globally extended.

Use S_Q=kappa exp(-3Q), kappa=.01, and design the clock principal diagonal
c_g²=.3. Unlike IC25, independently keep the auxiliary lapse Schur coefficient
at a negative constant M_*. These are design choices, not measured predictions.
The initial constraint solution, A and E4 values and both matter amplitudes
are the same as IC25; the new action derivatives are genuinely different.

Set alpha=A', beta=E4'. Solve h_z=0 for D and h_S+rhoH=0 for D'. On that
shell, at fixed alpha,

    C=h_Sq-h_Sz h_qz/h_zz=C0+[2z³h_qz/h_zz] beta.

This derivative is checked directly against the raw varied action. Therefore
the actual lapse preservation equation, with Sdot=S_Q Qdot, gives

    C_target=(-M_* Sdot+3Qdot(rhoH+pH))/qdot,
    beta=(C_target-C0)/(2z³h_qz/h_zz).

The divisions require qdot and the displayed coefficient to be nonzero;
the implementation rejects degeneracy rather than silently dividing by it.
Substitute beta(alpha) into the actual principal expression and solve the
resulting quadratic for alpha on its smaller real-root branch. Then choose

    D''=[h_SS|D''=0+rhoH-h_Sz²/h_zz-M_*]/z².

Re-vary the raw action and SOLVE the auxiliary preservation matrix. The
computed lapse Schur, multiplier and coupled characteristic eigenvalues
must agree with their design conditions; they are not assigned as outputs.
The active pin and regular chart are tested explicitly.

Evolve q,z,A,E4 using the actual flow and

    A_Q=alpha S_Q,  (E4)_Q=beta S_Q.

Directional differentiation yields A''=alpha_dot/Sdot and
E4''=beta_dot/Sdot; D'' is recomputed with these genuine jets. Independent
checks verify both new derivative identities, Ddot=D'Sdot,
(D')dot=D''Sdot and conserved total Hamiltonian charge. During partial
variation all three functions depend on S ONLY. Their third jets are used
in the time-dependent Euler calculation, never off-shell functions of q,z
or the matter amplitudes.

## 3. Finite-band rational diagnostic

The following is a diagnostic PROJECTION onto the clock canonical pair,
not an invariant subsystem or a replacement for the full six-mode problem.
Let p=k², M(p)=m-2Bp, and set

    K=a-C²/(2M),
    L=2dp-C(4ep+g0)/(2M),
    W=-2vp+4d²p²/a+w0-(4ep+g0)²/(2M),
    g0=-3sum(1+w_i)h_i,  w0=(9/2)sum w_i(1+w_i)h_i.

The degeneracy relation H_RR=d²/(2a) follows from the same auxiliary action.
Eliminating the clock momentum gives A_clock=2/K and the exact projected
restoring coefficient

    omega²=KW-L²-K[d(L/K)/dt+3Qdot L/K].

Total time differentiation includes pdot=-2Qdot p. Symbolic cancellation
gives a cubic numerator over a quadratic denominator:

    omega²=N3(p)/[2a(2Bp-m)(4Bap+C²-2am)].

For a>0,B>0,m<0 the denominator has no zero on p>=0. The numerator,
its numerical roots and decomposition into instantaneous Hamiltonian,
time-dependent mixing and volume terms are calculated, not prescribed.
Direct numerical differentiation checks the rational expression. The full
coupled Euler and Hamiltonian propagators remain authoritative; this
projection cannot certify their stability.

## 4. Executed design choices and finite propagation

An initial M_*=-3 reconstruction reduces the preliminary k_initial²=100
amplification over Q in[0,1] from about2.26e5 to about5.6, in the same
initial-kinetic norm convention. It still has a low-wavenumber growing mode.
A local variation of M_* shows that decreasing |M_*| moves the projected
negative-restoring band toward smaller k². This is engineering freedom,
not a new observational law or a proof that all growing modes are harmless.

The selected candidate uses M_*=-.03. It is a DISTINCT action from M_*=-3;
their results are not pooled. Preliminary full propagators for this selected
action give largest singular values around1.20,1.20,1.23,3.19,5.56 at
initial k²=.001,.01,.1,1,100 over the same Q interval. This is finite
amplification, not a stability threshold or a bound for every wavelength.
The bounded report refines the interpolation grid and independently tests
k_initial²=100 with60-digit midpoint matrix exponentials.

The prescribed norm is the fixed initial positive kinetic square root on
(x,xdot/Qdot_initial). It is not a coordinate-independent observable. All
three fields and all six roots are retained. Slow growing roots at some
long wavelengths still require gauge-invariant/physical interpretation.
The code does not declare all-scale stability simply because the formerly
large amplification disappears in the sampled range.

The same-action tensor coefficients are calculated from raw h_R and the
momentum coefficient t: c_T²=-t h_R/exp(2S), with positive tensor kinetic
coefficient1/(4t). Local auxiliary PB matrices are actually constructed for
k=0 and k!=0 samples. No global nonlinear constraint count is inferred from
these finite matrices. Ordinary matter couplings are unchanged, so the
minimal-action Ward-identity argument is unchanged; homogeneous charge
conservation alone is not presented as its proof.

## 5. Remaining obligations

The construction is OPEN, not a full theory. Still required: interpretation
and control of residual long-wave modes; canonically normalized nonlinear
interaction scales; coefficient limits and one globally defined extension;
the SAME functions under different matter sources; nonlinear Dirac closure
and physical elliptic-channel analysis; pin/static/zero-field matching;
independent Phi and Psi, measured G and full PPN; relative flows and vector
perturbations; and actual galaxy, cluster and recombination/CMB calculations.
The a0-Lambda normalization remains input. No empirical claim, Lean proof,
independent peer review or global-novelty certification is supplied.

The post-run review and exact commands/statuses are in ic26_run_001. Mathematical
proofreading and computation self-review cover this note and its new script.
