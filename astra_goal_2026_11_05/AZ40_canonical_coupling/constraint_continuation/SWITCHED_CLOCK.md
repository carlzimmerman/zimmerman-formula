# Positive switched stiffness does not impose zero clock momentum

This is an analytic continuation of C1 beyond its Lstar=0 bilinear calculation.
It does not assert the switched action has an ordinary quadratic Hessian at
P=0. It retains its actual leading, degree-two, generally nonquadratic
functional. Scope: fixed finite Fourier/Galerkin scalar perturbations about
P=0,Q=1 scalar-only FRW, fixed spatial regulator and periodic boundaries;
no continuum well-posedness, nonlinear constraint count or caustic theorem.
Proof status: author self-review of the finite-dimensional statement.

At a fixed background time, use the physical spatial gradient/divergence and
K=4piG>0. The leading polarization energy is exactly

    F_sw(P)=K ||P||^2/2+gamma ||(D.P)_+||^2/2, gamma>=0,

where positive part is taken in real space BEFORE integration. It cannot in
general be replaced by a constant Fourier multiplier. P lives in a fixed
finite vector Fourier space, with the standard spatial L2 inner product.
Let k_max be its maximum physical wave number. Define

    F_0(P)=K ||P||^2/2,
    F_full(P)=K ||P||^2/2+gamma ||D.P||^2/2.

Then F_0<=F_sw<=F_full for every P. F_sw is continuously differentiable,
K-strongly convex and coercive in this finite space: x -> (x_+)^2/2 is
convex and C1, and its derivative x_+ is 1-Lipschitz. Therefore its gradient
has Lipschitz bound L=K+gamma*k_max^2. The positive part may generate spatial
harmonics; differentiation/variation is projected back onto the fixed space.
No assumption that one input Fourier mode stays isolated is made.

The acceleration coupling is <P,grad chi>, chi=alpha-sigma_dot. Eliminating
P by its unique stationary maximum in <P,u>-F_sw(P), u=grad chi, gives the
convex conjugate T_sw(u)=F_sw*(u). Ordering reverses under conjugation:

    F_full*(u)<=T_sw(u)<=F_0*(u).

For a scalar chi in the same finite Fourier space this means

    (1/2) sum_k k^2 |chi_k|^2/(K+gamma*k^2)
      <= T_sw(grad chi)
      <= (1/(2K)) sum_k k^2 |chi_k|^2.

It is strictly positive for a nonconstant chi. Moreover it is strongly convex
on the nonzero-mode scalar space, not merely positive at its minimum. One can
prove this without assuming a Hessian at zero: if P_u maximizes the conjugate,
then grad F_sw(P_u)=u. The upper quadratic bound on F_sw is

    F_sw(P_u+d)<=F_sw(P_u)+<u,d>+L||d||^2/2.

Insert the trial P_u+d with d=z/L into the supremum defining T_sw(u+z):

    T_sw(u+z)>=T_sw(u)+<P_u,z>+||z||^2/(2L).

Thus its gradient map is injective and its velocity dependence cannot be a
Lagrange multiplier imposing a vanishing momentum. In a fixed finite scalar
space excluding k=0, grad has a positive minimum singular value; the same
strict-convexity conclusion holds for chi. The norm penalty adds the
nonnegative mu_K^2 ||chi||^2/(2K), preserving this conclusion.

The metric shift still appears only in the canonical Einstein/scalar term,
so its leading constraint is alpha=bq, exactly as in RESULT.md. The new
leading clock Lagrangian is therefore

    R^3 [ T_sw(grad(bq-sigma_dot))
                   +mu_K^2 ||bq-sigma_dot||^2/(2K) ].

It is independent of sigma itself. After spatial integration by parts its
momentum is the projected density

    j=R^3[D.P+(mu_K^2/K)(sigma_dot-bq)],   j_dot=0.

The momentum map admits nonzero small data; it is not a constraint j=0.
Thus adding the actual positive switched stiffness does not provide the
missing zero-mode-momentum selection in this regulated leading system.
The homogeneous scalar mode remains exceptional when mu_K=0.

Limitations: the lower strong-convexity constant deteriorates as k_max grows;
this proof does not take a continuum limit, prove a smooth solution across
switching interfaces, establish a physical dispersion relation for the
nonquadratic leading functional, or analyze a nonzero-P background. The
exact independent-clock caustic branch remains unaffected. The Lstar=0
36-check ADM evidence is not relabeled as a computation of this extension.
No finite sample supplies this proof, and no new action or coefficient is
introduced by it.
