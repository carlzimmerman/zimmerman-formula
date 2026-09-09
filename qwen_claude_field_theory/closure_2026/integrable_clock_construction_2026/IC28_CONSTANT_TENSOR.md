# IC28: the constant-tensor branch omitted by the nondegenerate curvature chart

Base b2a5cc4ec32122984c19e5749e29a15b191ae716 plus hashed IC27 metric
derivation. **Distinct candidate action; full theory OPEN.**
Credit: Carl Zimmerman's exponential kernel, vacuum-scale relation and
primordial-clock direction motivate this construction. No novelty-priority
or empirical success claim is made.

## Same-action construction

In the FULL first-order phase action I20 of IC20_JOINT_COMPLETION.md replace
v=v0+z² by v=v0=m exp(S+2w)/2 everywhere. Leave the other covariant terms,
minimal matter coupling and pin activation unchanged. Choose A,D,E4 as below.
This specifies an action change, not an on-shell substitution or a new
constraint imposed on the old theory. In normalized units m=1, its pinned
trace/curvature Hamiltonian is

    h=-exp(2S)q²/(6v0)-A(S)qz-exp(S)P0(S)
       -D(S)z²-E4(S)z⁴-v0 R.

The old partial Legendre transform divided by H_RR and therefore did not
exhaust the H_RR=0 branch. In the new action h_zR=0, hence

    H_qR=0, H_RR=0, H_SR=-v0,
    h_zz=-2D-12E4 z²,
    a=t/6+H_qq/2=A²/(4D+24E4 z²)>0,
    t=exp(2S)/v0.

For A!=0,D>0,E4>=0 these identities give a regular auxiliary Schur and
positive scalar momentum coefficient. They satisfy the actual compatibility
equation (H_qq+t/3)H_RR-H_qR²=0 without dividing by H_RR.

The physical tensor coefficient is M_T²=2exp(S-2wc)/t=1 and its speed is
-t h_R/exp(2S)=1. Using the IC27 reconstruction with the NEW tdot/t=Sdot
gives independently

    Phi=delta S+exp(-2S)(chi dot-Sdot chi),
    Psi=-zeta-exp(-2S)Qdot chi,
    Phi-Psi=0.

The equality follows from H_qR=H_RR=0, H_SR=-v0 and tdot/t=Sdot in the
derived slip equation. No assignment Phi:=Psi occurs in the code. This is
linear no slip for arbitrary constrained nonzero Fourier data on the active
homogeneous pin, not yet the static pin-off MOND branch or PPN.

## Matter and principal response

Both IC23 irrotational fluids remain in the same action. The full K,L,W
matrices retain their finite-k interactions. Because d=H_qR vanishes
identically, its time derivative and the off-diagonal PRINCIPAL mixing
vanish as derived consequences. The scalar principal value is

    c_g²=2a v0 u²/[exp(2S)(1-u²)],   0<u<1.

Positive values below1 require a real inequality on the coefficient functions,
not an assigned eigenvalue. The other two principal values are computed from
their Legendre maps. Full six-root time-dependent Euler spectra check the
high-frequency limit independently, retaining every mode.

## Explicit initial action and actual evolution

At S0=.1,q0=-3,z0=1,Q0=0 choose A0=.1,E40=.01 and the same two positive
matter amplitudes1e-6, w_m=1e-8. These are engineering inputs, not data fits.
Take A(S)=A0 and E4(S)=E40. The raw varied equations determine D0 and D1
from h_z=0 and h_S+rhoH=0. The raw Schur equation determines D2 using design
target M=-3. Then fix the single explicit function

    D(S)=D0 exp[d1(S-S0)+d2(S-S0)²/2],
    d1=D1/D0, d2=D2/D0-(D1/D0)².

After this choice no coefficient is reconstructed or retuned along evolution.
The actual 2x2 auxiliary preservation matrix solves Sdot and zdot; it is
not replaced by a target trajectory. The actual 4x4 local Poisson matrices,
their determinants and numerical ranks are computed separately at k=0 and
nonzero modes. These finite matrices do not prove global nonlinear closure.

The report attempts Q=.1 at max steps .0001 and .00005, with rtol1e-11,
an explicit step budget and checks of chart/kinetic/Schur/cone signs.
It retains any failed accepted state or unaccepted stage and reports charge
and constraint drift. These are diagnostic outcomes, not forced PASS tests.
The bounded report's scoped checks concern the local derivation and witness;
full-theory strict execution remains nonzero regardless of those checks.

## Scope that cannot be inherited

This action has NOT inherited IC26's seven-e-fold history or finite-band
amplification results. Finite-time and nonlinear stability, general Dirac
closure and physical instantaneous channels remain to be established.
Likewise h(q=0,z=0)=-exp(S)P0-v0R matches the old static value but does not
prove the full static variation, transition constraint count, measured G or
PPN. The primitive and a0-Lambda normalization are unchanged inputs.
Real matter/plasma and galaxy, cluster, recombination/CMB calculations remain.

## Integrated-potential repair of the first continuation

The exponential D trial encounters a lapse-Schur degeneration near Q=.0002211.
The report therefore also executes a distinct integrated D(S) candidate with
the SAME constant tensor coupling, A and E4. It solves D from h_z, D' from h_S
and D'' from a negative constant Schur target, then evolves the actual
preservation equations. Independent directional derivatives check
Ddot=D'Sdot and (D')dot=D''Sdot. Third jets in its Euler spectrum are derived
from this construction, and partial variations still hold D as a function
of S only. The two D choices are not pooled as one action.

The integrated run requests Q=1 on two step grids. Its positive-z
reconstruction divides by z and z², so it rejects nonpositive z before
division and reduces its step according to the actual z velocity.
A declared z=1e-6 floor stops the diagnostic without pretending to continue
through the zero-field boundary. Reaching a numerical guard is NOT a proof
of the exact mathematical endpoint. All failures and residuals remain in
the report.

The next constructive equation is to let A(S) vary as well while retaining
constant tensor coupling. For example, prescribing a positive constant
background z and a nonzero construction Sdot gives from h_z preservation

    A'=[A qdot/Sdot+2(h_S|A'=D'=0+rhoH)/z]/q

when E4 is constant. This is a design equation to be tested, not an imposed
extra constraint, and the sign of the resulting lapse Schur must be derived.
No integrated A repair is claimed here. This retains the no-slip identity
while targeting the auxiliary boundary directly, instead of reintroducing
a fluctuating tensor coupling to fix only the background.
