# IC7: an action-derived isotropic quartic repair, not full closure

Base: `0b75e72bf5797e451beb258847ade528cd9c4551`. This is a new explicit
phase-action revision of IC6, not an extra PASS assigned to that earlier theory.
Definitions of the global IC6 action, activation eta, clock and barred variables
remain those of [TENSOR_BALANCE.md](TENSOR_BALANCE.md) and
[IC5_ACTION.md](IC5_ACTION.md). The failed nearby-branch calculation and its
independent action variation are retained in
[IC6_EVEN_CHARACTERISTICS.md](IC6_EVEN_CHARACTERISTICS.md).

## One additional action term

Write V=sqrt(det(bar h)), rho=bar pi/V, tau=bar pi_tf²/V²,
w=(u−1)xi, E=exp((4−3u)xi), and J=1+exp(−6w)rho² F/(m²a0²).
On the existing eta=1 plateau, the nongradient Hamiltonian per barred volume is

    h(rho,tau,xi,u) = 2 E/m (tau/J − rho²/6)
                     + m exp((3u−2)xi)[Lambda+a0² U(u²)]
                     − kappa exp((3u−4)xi)/2.

Here F, b, U and all constants are the frozen IC6 functions, not new fits.
Set c=m exp(u xi)J and D_t=partial_u−b partial_xi at fixed rho,tau.
The symbol D_t here is a field-space derivative, NOT a time derivative.
Define, differentiating before setting tau=0,

\[
\mathsf M=\left.\begin{pmatrix}
 h_{\rho\rho}/4+h_\tau/12 & D_t h_\rho/2\\
 D_t h_\rho/2 & D_t^2h
\end{pmatrix}\right|_{\tau=0},\qquad
v=\binom{c_\rho/2}{D_t c}.
\]

The uncut coefficient is c_raw=v^T M^(-1)v/8. It is an explicit function of
rho,xi,u defined by derivatives of the displayed action density. Neither
measured eigenvalues nor a desired wave speed define it.

The inverse must NOT be multiplied by zero at a singular point. At the exact
witness det(M_star)=−4 Tcal² h0²/81, which is nonzero. Define
D=det(M)/det(M_star). A smooth cutoff theta(D) is one when |D−1|≤1/4 and zero
when |D−1|≥1/2. In between set x=4(|D−1|−1/4) and

    theta = exp(−1/(1−x)) / [exp(−1/x)+exp(−1/(1−x))].

Define c7=theta*c_raw on |D−1|<1/2 and c7=0 directly elsewhere. This smooth
zero extension stays away from the inverse's singularity. In particular it
is defined on the zero-momentum static branch. The full additional term is

\[
\boxed{\Delta H_7=\int d^3x\,V\,\eta(r)c_7(\rho,\xi,u)\bar R^2.}
\]

Equivalently, the SAME covariant phase action is

\[
S_7=\int d^4x\sqrt{-g}\,[2P^{ij}Q_{ij}-\mathscr H_6
 -\eta(r)e^{w-\xi}c_7(e^{3w}p,\xi,u)\widehat R^2]+S_m[g,\psi].
\]

Indeed bar R=exp(2w)Rhat, rho=exp(3w)p and sqrt(−g)=N exp(3w)V.
The coefficient's regularity domain also requires the preexisting J>0,
timelike clock and 0<u<1. Neither cutoff transition is certified healthy.

For completeness the additional canonical Euler derivatives can be written
before any background substitution. Put A=eta*c7, pbar^ij=bar pi^ij/V and
U^ij=pbar^ij−rho*bar h^ij/2. With barred covariant derivatives throughout,

    delta(Delta H7)/delta bar pi^ij = A_rho bar R² bar h_ij,
    delta(Delta H7)/delta q^a = V A_a bar R²,             q^a=(xi,u),
    V^(-1) delta(Delta H7)/delta bar h_ij
      = (bar h^ij A/2 + A_rho U^ij) bar R²
        − 2 A bar R bar R^ij
        + (D^i D^j − bar h^ij Delta)(2 A bar R).

These follow by varying the spatial curvature and integrating by parts on
the same closed-leaf or vanishing-boundary-variation domain as IC6. They add
to its canonical metric, momentum and auxiliary equations with the standard
Hamiltonian signs. The coefficient is not an externally prescribed source.
Away from bar R=0 the momentum equation changes: an exact nonlinear compact
Lagrangian would require a fresh stationary momentum elimination, not
substitution of the old IC6 trace solution. The code's independent Lagrangian
bridge is specifically a quadratic Legendre check on flat backgrounds.

## Variation and exact isotropic cancellation

For any spatially flat homogeneous isotropic background in eta=theta=1,
take the actual scalar momentum constraint and spatial gauge used in the IC6
even-sector calculation. The canonical scalar momentum is p_zeta. With
x=p_zeta/V and t=u at fixed s=xi+b u, its nongradient (x,t) Hessian is V M.
Within this fixed-metric block delta rho=x/2 and the quadratic trace-free
invariant is delta tau=x²/24, producing the essential h_tau/12 contribution.
The full constrained scalar variation also has metric terms; the numerical
Hamiltonian reduction retains them in the lower spatial orders.

For a mode along the third barred principal axis B3,

    delta bar R = 4 k² zeta/B3²,
    curvature source = −2 V k² zeta v^T(x,t)/B3².

At high k the other auxiliary direction has nonzero k² stiffness. Its
elimination leaves the above finite two-by-two system. Eliminating (x,t)
gives the scalar quartic stiffness

    S4 = −4 V v^T M^(-1)v / B3^4.

Direct variation of V c7 bar R² adds Delta C_zeta,zeta=32 V c7 k^4/B3^4.
Consequently S4+32 V c7/B3^4=0 identically on this isotropic plateau domain.
This is Schur-complement algebra for the explicit action, not a rank or
dispersion value inserted into a certification script. Isotropy also makes
the leading antisymmetric momentum/curvature mixing vanish.

The reduced Euler equation includes the time dependence of the constrained
homogeneous background. If its old form is qddot=D qdot+E q and A is the
momentum-momentum Hamiltonian Hessian, this action change gives
E7=E6−A Delta C and D7=D6. It does not change A or its time derivative, nor
the mixed Hamiltonian block and its time derivative. Freezing these background
derivatives gives an incorrect scalar result even at the old exact witness.

## What is preserved, and what is actually tested

On every flat homogeneous background bar R=0, the correction and its first
variations vanish. Thus the homogeneous constraint equations and background
flow are exactly the same. At the exact witness F=0, M11=v1=0 but M12 is
nonzero, giving c7=0. The full correction therefore starts at third order
around that witness: its complete quadratic action is unchanged.
On the open static eta=0 plateau all jets of the added term vanish.
These statements preserve the corresponding IC6 calculations, not any
unproved baryon-only AQUAL, PPN or global matching assertion.

No auxiliary time derivative was added to the canonical symplectic form.
That fact alone is NOT a complete new Dirac or DOF proof. The term adds metric
spatial derivatives; general constraint preservation and physical evolution
must still be derived for IC7. Likewise, on a flat homogeneous background
the cross-polarized tensor has delta bar R=0, so its quadratic sector is
unchanged. The earlier inhomogeneous odd-sector result is NOT transferred to
IC7 when background bar R is nonzero.

The script reconstructs h from the frozen IC6 Hamiltonian and differentiates
it. Independent checks compare M and v with the full metric/momentum Hessian,
including nonunit volume and B3, and compare the repaired canonical action
with the independently varied compact IC6 Lagrangian plus its quadratic
Legendre correction. Removing, reversing or mistuning the correction leaves
a nonzero quartic coefficient and is detected by tests.

At trace ratios j=0.998,1,1.002,1.007, actual nonlinear auxiliary roots are
solved at 80-digit precision. All lie inside both unit plateaux. For the last
sample c7≈0.00235189114143216, and at k=100000 the scalar's inferred physical
speed squared is approximately 0.388526918, the tensor's approximately 1.
The mass matrix is positive in the sampled reduced sector. Finite-k complex
pole corrections from expansion are printed, not discarded. These are bounded
high-precision observations, NOT interval-certified causal or all-frequency
stability statements. The symbolic quartic cancellation itself is exact.

## Remaining construction problem

On a sheared background the existing IC6 even pencil has a nonzero leading
antisymmetric mixing. A curvature-square term changes the stiffness but not
this mixing. In the tested sheared state IC7 retains
G2_12≈0.000563025148111, and its remaining S4_11≈0.0151964888331 is also nonzero.
It is therefore NOT a repair of all backgrounds and is not a viable finished
theory. This checkpoint proves a local isotropic construction, with a precise
next design equation rather than an all-requirements PASS.

The next unavoidable calculation is an action-level momentum/curvature
modification satisfying BOTH N2=N2^T and C4−B2 A0^(-1)B2^T=0 on sheared
backgrounds, followed by the remaining k² cones and kinetic signs. Full-field
causal evolution, constraint persistence, zero-mode/zero-field limits,
galactic matching, measured G, PPN and empirical cosmology remain open.
No universal novelty, Kepler-grade prediction or observation-based success
is claimed. Full theory: **OPEN**; the specific IC7 revision still fails the
requested all-background propagation gate.
