# Frozen continuation: microscopic protection of the amplitude

2026-10-20. Base b37b50b1c; reviewed analytic checkpoint be8fc76cb.
The previous turn made progress but did not reach the original goal:
a healthy microscopic theory forcing xi=1/4 and an end-to-end Lean proof.
The user now explicitly asks for a microscopic symmetry forbidding the
amplitude deformation and selecting R=128pi/9. A protected exponent,
an arbitrarily chosen nonrenormalized coefficient, an EFT symmetry without
the MOND source, or another quarter in a different observable is insufficient.

Kappa=1/2 is FITTED. CFG493 gives separately kappa_Lambda=0.417+/-0.095
and kappa_crit=0.345+/-0.078. The footing here is rho_DE, with epsilon
the physical gravitating energy density. No measured acceleration, Hubble
scale, density ratio, kappa, charge or target-equivalent coupling is input.

## Inherited exact problem and overlap

Read ../geometric_source/RESULT.md, GRAVITY_PHASE.md and EVIDENCE.json.
For dimensionless metric potential Phi, h=|grad Phi|, the local static
gravitational phase has

    E=M^2 h^2[1/(1+chi^2)+chi^2 h^2/(9a0^2)],
    Lkin=-Z^2(partial chi)^2/2, Z>0,
    C2=M^2, C3=2M^2/(3a0), G=1/(8pi M^2).

Its bounded deformation U_eta=epsilon+eta chi^6/(1+chi^2)^6, eta>=0,
preserves chi0 vacuum/UV/quadratic data but changes the formal local
cubic. The covariant normal-fluid/halo/UV obligations remain open. No
same-state globally healthy family was certified. Retain this scope.

The operational single-mediator dictionary in n>=2 spatial dimensions is
G_n=q^2/(2Omega C2), a_IR=2qC2/(3C3), R=epsilon C3^2/C2^3 and
xi=8Omega/(9R); n=3 has Omega=4pi. C2 is the actual Newtonian force
coefficient, not an IR Taylor term. Tensor-plus-scalar G must be rederived.
For dimensionless Phi, physical acceleration is c^2|grad Phi|; restoring
units gives xi=a_IR,phys^2/(G epsilon_energy). Natural dimensions:
[M]=[Z]=[a0]=1, [chi]=0, [C2]=2, [C3]=1, [epsilon]=4.

W4-04/K631 already treats pure nilpotent dS supergravity and electric
BI/FI, and K634 D3 electric tension/endpoint normalization. W4-02/K613
already tests the Cai-Wang DBI radius bridge. The present question must
instead analyze exact transformations/operator protection of the new
gravitational-phase deformation or a different actually sourced model.
W4-08 protected_normalization already treats five-dimensional vector
prepotentials/CS and electric radial relaxation; protected_auxiliaries
treats N1 chiral folds. Their wrong source/state/force results are not
new trials. Do not repeat them under a different symmetry name.

## P0. Nonlinear local supersymmetry and the actual forbidden operator

Authenticate Dall'Agata-Farakos1512.02158v2,22January2016, section3.2,
Eqs64,71-79. Test the exact real-scalar constraint X(A-Abar)=0, X^2=0,
K=X Xbar-Z^2(A-Abar)^2/4, W=w+X f_eta(A). Determine whether a local
holomorphic f_eta can realize U_eta at fixed positive vacuum, canonical
kinetic data, supersymmetry-breaking scale and gravitino mass. Enforce
F_X!=0 and the source's constrained auxiliary reduction; do not use the
unconstrained scalar-potential formula for a removed auxiliary.
Distinguish local holomorphic patches from a globally entire UV model.
An explicit supersymmetric completion of a potential operator is not a
supersymmetric completion of the entire higher-gradient MOND theory.

## P1. Exact Goldstone and exceptional spacetime symmetries

Classify genuine internal point symmetries of the inherited action with
the physical metric and arbitrary massive matter source fixed. A field
reparameterization or transformation of input coefficients is not a
symmetry selecting an invariant. Test nonlinear Goldstone/brane DBI and
Galileon alternatives by their actual Ward identities and source responses.
Require a nontrivial invariant action, retained healthy fluctuations and
correct low/high acceleration ordering; preserving a tension ratio with
the wrong force exponent does not pass. Couplings separately allowed by
the symmetry remain separate, even if radiative running is absent.

## P2. Extended SUSY, moment maps and protected moduli geometry

Authenticate the actual four-dimensional N2 electric/magnetic FI partial-
breaking action or another explicit protected microscopic candidate.
Derive its exact stationary auxiliary/scalar equations, vacuum stress,
source map and response before transferring a central-charge identity.
Check which hypotheses of Higgs-branch nonrenormalization survive
supersymmetry breaking, gravity and the higher-derivative MOND operator.
Do not equate an electric cubic, finite-density pressure or BPS charge
ratio to an attractive universal gravitational amplitude. Any extra matter
charge, FI parameter, uplift or prepotential coefficient must be exposed.

## P3. Interacting fixed points and duality

Test a concrete interacting conformal/duality candidate beyond the prior
free sphere determinant and thermal expansion. Derive the actual operator
dimension and source dependence, not only the response exponent. Identify
which amplitude/Ward coefficient is fixed, and all allowed identity,
Einstein and source counterterms when coupling to gravity. A universal
ratio of singular critical amplitudes does not automatically normalize
the positive regular vacuum energy. Any large-charge/timelike P(X)
application needs its full spacelike-source and stress bridge. Bound
the source search and report conditional/missing arrows precisely.

## Success, controls and resources

This is initially free/audit, not a determinate kappa trial. If a real
selector appears, freeze its complete admissible option space before
evaluation. No coefficient/flux/multiplicity scan or target fit is allowed.
An a0/H-only or dS-invariant identification retains the inherited odd-pi
obstruction; entropy/temperature conventions cannot insert a quarter.
If hbar or loops enter, show their physical matching and cancellation.

Necessary success includes the healthy microscopic action/quantum state,
attractive MOND and actual UV Newton regime, positive same-state stress,
independent invariant amplitude selection and a second observable, followed
by complete formal bridges. Failure in a tested class is no global no-go.
Semantic controls are: a genuine extra exact shift must eliminate the
nonconstant potential but be tested on all retained gravitational/source
operators; removing the relevant spurion must remove its breaking terms;
an allowed supersymmetric eta deformation must change the static cubic
without changing the fixed vacuum data. Any actual Lean computation must
have true controls and separate genuine False mutants, printed theorem
types/axioms and no admissions/custom axioms/native substitutes.

Commit this criteria file alone before new scripts/Lean. Do not add modules
merely to reprove a coefficient dictionary or elementary minimum. Retain
raw analytic actions, exact primary versions, disjoint authored packets,
independent action-level reviews and artifact hashes. Append campaign rows
sequentially and regenerate its four artifacts. Do not edit reserved lanes.
No downloads or broad builds. Continue light one-core work under about1GB
while the large simulation state is unknown; never interrupt it. Any Lean
uses the existing pinned read-only runner, -j1 -M1024,30sCPU,45swall.
The original goal remains active unless actually achieved or genuinely
blocked under the standing goal rules.
