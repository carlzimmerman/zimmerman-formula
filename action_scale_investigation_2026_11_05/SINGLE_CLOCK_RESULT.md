# A single-clock density portal: positive cosmological kinetic block

Candidate, not adopted. No derived coefficient. Kappa=1/2 FITTED.
This is a new density-dependent variant of AC2, not a claim that AC2 or v3s
already has the following universal bare-density identity.

## Action and density convention

In c=1 units define X=-(grad phi)^2/2>0, n=-grad phi/sqrt(2X),
h=g+n n, A=n.nabla n, K=4 pi G, M^2=1/(8 pi G), p=K sqrt(P.P), n.P=0.

    S = integral sqrt(-g) [ M^2 R/2 + X - V(phi) + P.A
          - W(p,a0(X,phi)) - gamma (D.P)^2/2 + lambda_P n.P ] + S_m,
    W = a0^2/K [-p/a0-log(1-p/a0)], 0<=p<a0,
    a0^2 = b [X+V(phi)], b>0, gamma=K Lstar^2/2.

There is no independent clock tau and no separate Q penalty. The stiffness
is smooth and unswitched; no v3s observational pass transfers. The density
X+V is that of the bare canonical scalar. The full interacting stress tensor
also contains polarization and portal variations. Calling X+V the measured
dark-energy density on a charged background requires additional matching.
On homogeneous P=0 backgrounds, the extra first variations vanish and the
canonical interpretation is exact. The equation for a0 is a specified portal,
not the result of solving an independent scale equation. b=kappa^2 G remains
a free coupling. Restoring c in the homogeneous relation gives a0^2=b c^2 rho.

In unitary gauge phi=phi_bar(t), X=phidot_bar^2/(2N^2) and A_i=partial_i log N.
The density-dependent scale introduces lapse dependence but no lapse time
derivative in these terms. This observation is not a full nonlinear Dirac
constraint count or proof against all higher-derivative pathologies.

## Matter included in the FRW kinetic calculation

Add a minimally coupled matter scalar psi with shift-symmetric L=F(Y),
Y=-(grad psi)^2/2 and background v=psidot>0. Define F1=F_Y>0,
Rm=F_Y+v^2 F_YY>0 and sound speed squared F1/Rm>0. Let
epsilon_phi=phidot_bar^2/(2 M^2 H^2)>0, H>0. The total -Hdot/H^2 is
epsilon_phi+v^2 F1/(2 M^2 H^2), not epsilon_phi alone.

Use zeta=Z cos(kx), delta psi=C cos(kx), lapse alpha cos(kx), and scalar
shift. Here a_FRW is the cosmological scale factor, not the MOND acceleration.
At P=0 the polarization sector adds

    (a_FRW^3/2) M^2 cY k_phys^2 alpha^2,
    cY=1/(1+Lstar^2 k_phys^2/2), k_phys=k/a_FRW.

The 1/2 is the spatial cosine average. Variation of the shift gives

    alpha = Zdot/H + F1 v C/(2 M^2 H).

After both lapse and shift constraints are eliminated, the velocity Hessian
in (Zdot,Cdot), including this same spatial average, is

    Kkin = a_FRW^3 [ [ M^2 E + Rm v^2/(2H^2), -Rm v/(2H) ],
                    [ -Rm v/(2H),                Rm/2     ] ],
    E = epsilon_phi + cY k_phys^2/H^2,
    det Kkin = a_FRW^6 M^2 Rm E/2 > 0.

Its lower diagonal element is positive, so both eigenvalues are positive
for the stated domain. Completing the velocity square is an independent
analytic reading:

    L_kin = a_FRW^3/2 [ M^2 E Zdot^2
                         + Rm/2 (Cdot-v Zdot/H)^2 ].

No beta, xi or b was selected. The portal dependence begins at cubic order
in P, so both the potential-only and density-dependent single-clock portals
share this FRW quadratic calculation. The shift term in Y was kept explicitly;
omitting it would miss the matter term in the lapse solution.

## Exact content and limitations

Proved as written: the displayed constrained FRW kinetic matrix is positive
under the listed assumptions. No claim of positive gradient/mass terms,
causal retarded support, weak coupling, exact dust constraint limit, X>0
preservation, or inhomogeneous stability follows. Taking sound speed toward
zero makes Rm large; exact pressureless matter needs its own variables.

The original two-field obstruction cannot be carried over: delta phi and
the clock are no longer independent velocities. Conversely, this positive
FRW result cannot be carried over to a galaxy with P nonzero. The next
discriminator is the candidate's own sourced system and its perturbations.

## Evidence

single_clock.py reconstructs the ADM Einstein, clock and matter density;
solves constraints; and independently checks the raw Hessian Schur complement.
All 72 frozen 40/80-digit fixtures meet the agreement and positivity checks.
The reversed induced lapse-gradient control has separate output and is
required to fail positivity. Run records live under evidence/single_clock*
and include input hashes. No background fit or physical-data comparison.

Self-review only. Proof-audit obligations checked: Friedmann background
substitution, matter shift contraction, phase average, Hessian normalization,
constraint elimination, distinction between total epsilon and epsilon_phi,
finite-sound-speed scope and absence of portal dependence at quadratic order.
Original target remains open.
