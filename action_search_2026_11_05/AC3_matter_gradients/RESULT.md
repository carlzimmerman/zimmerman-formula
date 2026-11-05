# Coupled matter propagation: an exact FRW principal result

The original goal of a fully healthy action with derived normalization is not
reached. One previously missing implication is resolved: the two scalar
short-wavelength modes of the single-clock candidate have positive gradients
and subluminal characteristic speeds on the stated FRW backgrounds.
Author self-review; not independent certification.

## Claim and domain

Use the action in ../AC2_single_clock/ACTION.md, or the density portal in
../../action_scale_investigation_2026_11_05/SINGLE_CLOCK_RESULT.md. They share
this P=0 quadratic block because a0 enters W beyond quadratic order. The
matter is a minimally coupled scalar F(Y). Set M²=1/(8pi G),
epsilon_phi=phidot²/(2 M² H²)>0, v=psidot, F1=F_Y>0,
Rm=F_Y+v² F_YY>0. Assume expanding FRW, fixed finite Lstar>0 and
0<F1/Rm<=1. Exact pressureless dust is excluded. Scalar gradients are timelike.

For every such background point, the UV scalar principal matrices are
positive definite. Their two generalized eigenvalues, squared speeds relative
to the metric, are exactly

    c_phi² = epsilon_phi / [epsilon_phi + 2/(H Lstar)²],
    c_m² = F1/Rm.

Thus 0<c_phi²<1 and 0<c_m²<=1. This is an instantaneous characteristic
statement as k_phys/H tends to infinity at fixed Lstar, not a proof of
retarded support, finite-wavelength stability, weak coupling, nonlinear
regularity or observational success. No coefficient b, xi or kappa is fixed.

## Derivation

Use unitary clock gauge and q=(Z,C), with curvature Z and matter perturbation C.
The momentum constraint gives alpha=Zdot/H+F1 v C/(2 M² H).
Reconstruct the ADM quadratic Lagrangian directly, including the matter
shift contraction. Write

    L2 = (qdot^T K qdot)/2 + qdot^T B q + (q^T P q)/2.

The symmetric part Bs of B is a total derivative plus a coordinate term:
G = dBs/dt - P. Dropping Bs without its time derivative is incorrect.
The background equation Hdot=-epsilon_phi H²-F1 v²/(2M²) is needed.
For the spatial k² coefficient, derivatives of epsilon_phi and Rm do not enter;
the constant-V specialization used elsewhere in the script does not restrict
this principal statement. The exact extracted coefficient is

    G/(a³ k_phys²) =
        [[M² epsilon_phi + F1 v²/(2H²), -F1 v/(2H)],
         [-F1 v/(2H),                   F1/2       ]].

Polarization contributes M² a³ cY k_phys² alpha²/2 with
cY=[1+Lstar² k_phys²/2]^-1. At fixed positive Lstar, cY k_phys² tends to
2/Lstar². Its coordinate and mixed terms are bounded in k, so they add no
UV spatial principal coefficient or order-k mixed term. Its velocity term
survives in the principal kinetic matrix:

    K/a³ = [[M² E + Rm v²/(2H²), -Rm v/(2H)],
            [-Rm v/(2H),        Rm/2       ]],
    E = epsilon_phi + 2/(H Lstar)².

Transform C=Q+(v/H) Z. Derivatives of v/H contribute only lower-order
terms. In (Z,Q) the principal matrices are diagonal:

    K/a³ = diag(M² E, Rm/2),
    G/(a³ k_phys²) = diag(M² epsilon_phi, F1/2).

The speeds follow by division. Independently, the matrix inequality

    K/a³ - G/(a³ k_phys²)
      = [2M²/(H Lstar)²] diag(1,0)
        + (Rm-F1)/2 * (-v/H,1)^T (-v/H,1)

is positive semidefinite for subluminal bare matter. Determinants are
M² Rm E/2 and M² F1 epsilon_phi/2, both positive.

## Verification and limitations

The exact ADM gradient, principal limits, determinants and congruence are
checked in derive_v2.py. An independent Cholesky-whitened generalized
eigensolve checks81 fixtures at40/80 digits against the analytic roots.
The original failed run is preserved: it compared expanded and factored
SymPy expressions structurally, rather than testing their zero difference.
COMPARISON_ERRATUM.md records the repair; no scientific threshold changed.

All statements concern the isotropic FRW scalar sector. Neither angular
perturbations of sourced backgrounds nor exact dust follows. Lstar=0 is a
singular order-of-limits case: cY k_phys² then grows without bound, and the
bounded-lower-order argument fails. A small speed can make strong coupling
or slow-mode evolution important even when the UV principal form is positive.

## Finite wavelength result and unresolved slow modes

The full frozen-frequency check in finite_v3.py uses canonical matter (not
dust), a constant positive potential and81 specified background/wavelength
fixtures. It includes the antisymmetric velocity mixing A=B-B^T. Its frequency
polynomial is

    det(K) x² - [K11 G22+K22 G11-2K12 G12+A12²] x + det(G),
    x=omega².

Both the universal symbolic2x2 determinant identity and numerical direct
complex determinants agree;40/80-digit roots agree within the frozen bound.
Eight of81 cases have one negative root; none has complex roots. All eight
use H Lstar=.001 and k_phys/H=10 or100. Their negative omega²/H² lies between
-.898421 and-.167147. The smallest clock speed does NOT justify declaring
finite-wavelength stability. Conversely these slow, Hubble-scale roots do
not establish a short-wavelength gradient instability: their rates are below H,
where freezing the evolving coefficients is not a controlled approximation.
A time-dependent change of perturbation variables can change such a frozen
mass diagnostic. Integrate the full evolving constrained equations before
claiming physical growth or its absence.

The original finite run timed out while expanding the full symbolic determinant.
finite_v2.py instead proved the same identity for generic symmetric2x2 matrices;
its first numerical loop then failed due to an omitted k value in unpacking.
finite_v3.py corrects that four-value unpacking, retaining all81 cases and
thresholds. All unsuccessful run records remain alongside the completed run.

Next exact equation, derived from the same quadratic Lagrangian, is

    K qddot + [Kdot+B-B^T] qdot + [Bdot-P] q = 0.

This, rather than repeatedly sampling frozen eigenvalues, is the next
calculation for the eight slow-mode witnesses. Initial data and perturbation
normalization must be frozen before testing amplification. It has not yet
been executed at this checkpoint.
