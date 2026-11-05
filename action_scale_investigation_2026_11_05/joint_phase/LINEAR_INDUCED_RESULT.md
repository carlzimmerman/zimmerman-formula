# Linear condensate coupling: scale cancellation and its force obstacle

Contract frozen at b8552a2691. This changed action cancels the condensate
scale from a held-background ratio. It does not yet predict the operational
MOND normalization or its coefficient. Its additional scalar cannot be
made short-ranged relative to the Hubble scale by its mass in this model.

## Vacuum and scalar-metric mixing

Use the positive parameters and explicit critical-surface assumption of
LINEAR_INDUCED_CONTRACT.md. With p=0, F=D sigma and
U=U0+C_A sigma^3/3. The constant scalar and metric equations require

    U_sigma=2 F_sigma U/F,
    sigma0^3=6U0/C_A,
    F0=D sigma0,
    U_vac=C_A sigma0^3/2,
    H^2=C_A sigma0^2/(6D).

All are finite and positive for the declared domain. In the Einstein frame,
with its conformal factor normalized to one at this vacuum,

    V_E=F0^2 U/F^2,
    K_E=F0[Z/F+(3/2)(F_sigma/F)^2],
    K_E(vac)=Z+3D/(2sigma0),
    V_E''(vac)=C_A sigma0,
    m_sigma^2=C_A sigma0/[Z+3D/(2sigma0)].

Both homogeneous amplitude kinetic energy and squared mass are positive.
This is a scalar-tensor subsector result, not full polarization/clock health.
The dimensionless Einstein-frame matter charge obeys

    alpha^2=F0 [d ln sqrt(F0/F)/d sigma]^2/K_E
           =D/(4Z sigma0+6D),
    m_sigma^2/H^2=6D/(Z sigma0+3D/2)=24alpha^2<4.

The inequality is strict for Z>0; its limiting equality is at Z=0.
There is no radius with both m_sigma r>>1 and Hr<<1. A small charge at
large Z is possible, but mass decoupling in that window is not. This does
not rule out a separate nonlinear screening mechanism, absent here.

## The cancellation that survives

At fixed R>0, write r=sqrt(sigma^2+p^2). The amplitude equation becomes

    sigma [C_A r-D R/(2r)]=0,
    r_star^2=D R/(2C_A).

On the sigma>0 branch, for 0<=p<r_star, elimination gives

    (U-FR/2)_eff=U0+C_A r_star^3/3-D R r_star/2+C_B p^3/3.

There is no quadratic p term from these stationary potential/curvature
terms. This is a tree-level cancellation at fixed curvature; it neither
proves quantum protection nor includes metric and scalar source exchange.

For comparison with the previous held-background calculation only, define
G_tensor=1/(8pi F0), K_tensor=1/(2F0), and a_held=1/(K_tensor C_B).
Then

    kappa_tensor^2=a_held^2/(G_tensor U_vac)
                 =64pi D^3/(C_A C_B^2).

The arbitrary U0 sets sigma0 and the separate dimensional scales but drops
out of this expression. This is an improvement over the previous quadratic
F model's uncancelled detuning. It is not a selected numerical value:
D^3/(C_A C_B^2) still requires microscopic matching. Nor is G_tensor the
locally measured force coupling when scalar exchange is active.

If one writes D=xi A h, C_A=A h^3 and C_B=B h^3 merely as a dictionary,
the expression is 64pi xi^3/[(B/A)^2 h^6]. No values are assigned to these
parameters. A nodal spectrum alone does not justify the covariant operator
D r R: an actual curved-space determinant must establish its tensor form,
sign and finite coefficient, including allowed counterterms.

## Conditional local source calculation

The absence of a mass-decoupling window makes the following extra check
necessary. This paragraph specifies a possible leading local completion;
it is not asserted to follow from an unspecified full vector/clock action.
Let chi be the canonical amplitude fluctuation, Phi_E the tensor Newtonian
potential, q=d ln sqrt(F0/F)/d chi at the vacuum, and
Phi=Phi_E+q chi the potential coupled to matter. Let K=K_tensor. Take

    L_local=-(grad Phi_E)^2/(2K)-(grad chi)^2/2
            +p_vec . grad(Phi_E+q chi)/K
            -s2 |p_vec|^2/(2K)-C_B |p_vec|^3/3
            -rho_b (Phi_E+q chi).

Here s2 is a dimensionless quadratic coefficient, initially s2=1 as in
the earlier tensor-only polarization matching. Work in the static,
weak-potential, unscreened, approximately massless window Hr<<1;
hold the background coefficients fixed. These assumptions do not remove
possible higher-order corrections to the cubic response from a full action.

Varying the two potentials, rather than imposing a Newton constant, gives

    laplacian Phi_E=K rho_b+div p_vec,
    laplacian chi=q rho_b+(q/K) div p_vec.

With no independent homogeneous scalar gradient, chi=(q/K)Phi_E, hence

    Q=1+q^2/K=1+2alpha^2,
    G_local=Q G_tensor,
    g=Q(g_N_tensor+p)

for an aligned spherical configuration. The p equation is
g=s2 p+K C_B p^2. Combining the equations with
g_N_local=Q g_N_tensor yields

    g_N_local=(s2-Q)p+K C_B p^2.

Thus s2=1 is not the critical coefficient once this scalar is retained.
Since Q>1, the positive p branch for a positive source tends to
(Q-1)/(K C_B), not zero, as the source tends to zero. The p=0 vacuum still
exists at exactly zero source. This branch statement is not a proof of a
time-dependent instability or of a global cosmological solution.

Restoring a MOND critical response in THIS local truncation requires
s2=Q. That is an additional matching identity, not a permissible automatic
retuning. If it were independently justified, the local formulas would be

    g=g_N_local+Q sqrt[g_N_local/(K C_B)],
    a_operational=Q^2/(K C_B),
    kappa_operational^2=Q^3 64pi D^3/(C_A C_B^2).

For constant Z>0, Q depends on sigma0 through Z sigma0/D, so this correction
can reintroduce the vacuum-state dependence that the tensor ratio removed.
A different induced kinetic term proportional to D/sigma, or the Z=0 limit,
would change that conclusion, but needs its own microscopic justification
and sourced-field audit. Finite scalar mass also makes the exchange
momentum-dependent outside the stated window. The local calculation is a
diagnostic, not a derivation of the complete force law from the frozen
scalar-tensor potential alone.

## Evidence, self-review and next obligation

linear_induced.py checks 16 exact identities: homogeneous equations,
conformal kinetic and mass, matter charge, hierarchy, fixed-curvature
response and tensor ratio. All pass in evidence/linear_induced. Removing
the conformal kinetic term fails five targeted/dependent checks in
evidence/linear_induced_mutate. Both v2 manifests validate against the
current inputs and outputs. No scans, empirical parameters or numerical
coefficient selection were performed. The local-source calculation above
is an analytic variational derivation, not covered by those 16 checks.

Self-review verdict: conditional on the specified actions and local regime.
Checked units, positive-domain vacuum, conformal mixing, factor of two in
scalar exchange, fixed-curvature versus sourced elimination, boundary
gradient assumption and scalar mass window. Microscopic generation,
critical-surface protection, full source matching and full constraint health
are not addressed. No independent audit is claimed.

The next useful calculation is the joint curved-space microscopic matching
of D, C_A, C_B, Z(sigma), and the polarization quadratic term. It must
explain the s2=Q identity (or a different viable source law), rather than
only the scale-cancelled tensor ratio. A curved nodal medium may generate
preferred-frame curvature operators rather than Einstein gravity; that
operator identification is the first uncertain implication. The coefficient
goal remains open, and this candidate has not been adopted.
