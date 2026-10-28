# Actual-vacuum finite-block coercivity: one focused bridge attempt

Checkpoint YM-C2, 2026-09-22. Parent: `../CHECKPOINT.json` (YM-C1).
Repository input: `a0dc7c516f7a5c33ae9db03a9af6340ffdc74d2c`.
Evidence: analytic derivation and self-review; no novelty or formal-verification
claim. The original Yang–Mills existence and mass-gap target remains unresolved.

## 1. Claim and conventions

Use the finite SU(N) link Hamiltonian and metric of `../vacuum/PROOF.md`:

    H = (x/2) sum_l C_l + (b/x) sum_p (1-Re Tr U_p/N),
    C_l = -Delta_l,  x>0, b>=0, N>=2, a>0.

There are finitely many dynamical links E. Fix a nonempty subset B of m links;
write their configurations u and all remaining configurations y. Let p_B count
plaquette terms involving at least one link of B, counting each term once.
Let psi be the unique positive normalized ground function, E0 its eigenvalue,
and mu=psi^2 dU. No explicit formula for psi is assumed.

Let P f=E_mu[f | y], Q=I-P, and

    K = psi^{-1}(H-E0)psi/a.

Thus P is an orthogonal projection in L2(mu), and P1=1. Set
C_F=(N^2-1)/(2N), n=N^2-1, and let D_N be the diameter of SU(N) in the
specified Casimir metric. Let k_s denote the one-link heat kernel of exp(-s C)
relative to normalized Haar, and define

    kappa_N(s) = max_{u,v} k_s(u,v) / min_{u,v} k_s(u,v),  s>0.

The denominator is positive. The operator D_B below is the self-adjoint
operator associated with the restriction of the closed form of K to QL2(mu).
Writing QKQ is shorthand for this form compression, not an assertion about
unbounded operator products.

**Finite-block theorem.** For every s>0,

    D_B >= d_B(s) I,
    d_B(s) = [x C_F/(2a)] kappa_N(s)^(-2m)
                         exp[-8s b p_B/x^2].                    (1)

In particular, if b p_B>0,

    D_B >= [x C_F/(2a)] 2^(-2mn) exp[-C_B/x] I,
    C_B = 4 D_N sqrt(3m b p_B).                                (2)

The bounds are independent of the number of links outside B, with B, its
incident plaquette count and the displayed parameters fixed. They are not
uniform in m or N. They hold on the full space and therefore on the physical
gauge-invariant subspace whenever that discarded subspace is nonempty. If
b p_B=0, the sharper bound D_B>=x C_F/(2a) holds.

## 2. Feynman–Kac comparison removes dependence on exterior volume

Split V=V_out(y)+V_hit(u,y), with

    0 <= V_hit <= W_B := 2b p_B/x.

For Brownian motion (U_t,Y_t) with independent link generators (x/2)Delta,
the ground-state semigroup identity at any time t>0 gives

    exp(-t E0) psi(u,y)
      = E_{u,y}[exp(-integral_0^t V(U_r,Y_r)dr) psi(U_t,Y_t)].

Remove only V_hit from this positive expectation and call the result F_t(u,y).
Then

    exp(-t W_B) F_t(u,y) <= exp(-t E0) psi(u,y) <= F_t(u,y). (3)

Independence of the link Brownian motions and independence of V_out from u
give, with s=xt/2,

    F_t(u,y) = integral k_s^B(u,v) A_t(y,v) dv,
    A_t(y,v) = E_y[exp(-integral_0^t V_out(Y_r)dr) psi(v,Y_t)] > 0.

Here k_s^B is the product of m one-link heat kernels. For the same fixed y,
the factor A_t is the same for every initial u. Consequently

    psi(u,y)/psi(u',y)
       <= exp(t W_B) kappa_N(s)^m =: R_B(s).                  (4)

The large exterior potential and E0 cancel in this ratio; neither has been
bounded by a volume-independent number. This cancellation is why (4) does
not acquire a factor proportional to the number of exterior plaquettes.

## 3. Conditional variance gives the actual discarded-sector bound

The conditional measure is

    mu_y(du) = psi(u,y)^2 du / integral psi(v,y)^2 dv.

Its maximum-to-minimum density ratio relative to product Haar is at most
R_B(s)^2. Product Haar has Poincare constant 1/C_F: each nonconstant
Peter–Weyl component has a positive sum of Casimirs at least C_F. If a
probability density w relative to Haar has max(w)/min(w)<=R^2, then

    Var_w(f) <= max(w) Var_Haar(f)
              <= [max(w)/C_F] integral |grad_B f|^2 dHaar
              <= [R^2/C_F] integral |grad_B f|^2 w dHaar.

The first step uses the minimizing-constant definition of variance, so no
Haar-mean-zero assumption on a mu_y-centered function is being inserted.
Integrating this conditional inequality over y yields

    ||Qf||_mu^2 <= [R_B(s)^2/C_F] integral |grad_B f|^2 dmu.

For f in QL2(mu), use the exact ground-state form

    <f,Kf> = [x/(2a)] integral sum_l |grad_l f|^2 dmu
            >= [x C_F/(2a R_B(s)^2)] ||f||_mu^2.

Since t=2s/x and W_B=2b p_B/x, this proves (1), including its factor 8.
For each fixed finite graph, psi is smooth and bounded away from zero.
P maps smooth functions to smooth functions and is bounded in H1 (constants
may depend on that graph). Smooth Q-functions are therefore dense in the
restricted form domain; the inequality extends by closure. This establishes
the form compression without requiring uniform bounds on derivatives of psi.

Gauge transformations act separately on the selected and remaining link
coordinates, preserve Haar, and preserve psi. Changing variables in the
conditional integral shows that P commutes with the gauge action. Thus the
projection also respects Gauss invariance. No gauge fixing is used.

If b p_B=0, the Hamiltonian splits into free B-links and an exterior operator.
Its positive ground function is constant on B; the exact Haar bound applies.

## 4. Explicit weak-coupling rate, with the heat estimate derived

The bi-invariant SU(N) metric has nonnegative Ricci curvature. On a compact
manifold of dimension n with nonnegative Ricci curvature, a positive heat
solution satisfies

    |grad log u|^2 - partial_t log u <= n/(2t).                (5)

For completeness, put f=log u, w=|grad f|^2-f_t, F=tw. Bochner gives

    (Delta-partial_t)F
       >= 2F^2/(nt) - F/t - 2<grad f,grad F>.

At a positive space-time maximum larger than n/2 this contradicts the maximum
principle. Start with a smooth positive initial function; for a heat kernel
apply the argument after an arbitrarily small positive time shift and then
let that shift tend to zero. Compactness removes boundary and escape issues.
This is the compact case of the Li–Yau estimate, also checked against their
Theorem 1.1; see `SOURCES.md`.

Integrating f_t+<grad f,dot gamma> >= -|dot gamma|^2/4-n/(2t)
along a constant-speed minimizing geodesic gives

    u(z,t1) <= u(w,t2) (t2/t1)^(n/2)
                        exp[dist(z,w)^2/(4(t2-t1))].          (6)

Apply (6) to k_t(v,.) between s and 2s and integrate the later point to get

    max k_s <= 2^(n/2) exp[D_N^2/(4s)].

Apply it between s/2 and s and integrate the earlier point to get

    min k_s >= 2^(-n/2) exp[-D_N^2/(2s)].

Both integrations use normalized Haar and total heat-kernel mass one. Thus

    kappa_N(s) <= 2^n exp[3D_N^2/(4s)].

Substitution into (1) gives a lower certificate

    [x C_F/(2a)] 2^(-2mn)
       exp[-3m D_N^2/(2s) - 8s b p_B/x^2].                   (7)

For b p_B>0, minimize the positive exponent at

    s_* = (x D_N/4) sqrt[3m/(b p_B)].

The minimized exponent is C_B/x, proving (2). This is a rigorous but coarse
estimate; it is not an asymptotic formula for the actual discarded spectrum.

## 5. Try the bridge: where this particular certificate stops

The exact Schur comparison in `../blocking/SCHUR_GAP.md` accumulates inverse
discarded gaps. Formula (2) supplies an actual d for one vacuum-preserving
finite-block projection of the original Wilson Hamiltonian, subject to that
comparison's remaining form/domain hypotheses. It does not supply a theorem
that an exact coarse Hamiltonian is another Wilson Hamiltonian.

Even hypothetically granting the same fixed-block certificate at every scale,
write its constants as c0=(C_F/2)2^(-2mn), C=C_B. For the illustrative profile

    a_r=A L^(-r), x_r=1/(sigma+q r), r>=1,
    A>0, L>1, sigma>0, q>=0,

the certified inverse-gap budget is

    sum_r a_r exp(C/x_r)/(c0 x_r)
      = (A/c0) exp(C sigma) sum_r (sigma+q r) rho^r,
    rho=exp(Cq)/L.                                          (8)

It is finite exactly when rho<1, and then equals

    (A/c0) exp(C sigma)
      [sigma rho/(1-rho)+q rho/(1-rho)^2].                   (9)

For rho>=1 this certificate cannot furnish a finite upper inverse-gap
budget. The actual inverse-gap sum might still be smaller. No actual
Yang–Mills trajectory, scale factor or running coefficient is asserted here.

There is a separate volume obstruction to this attempted application. A full
blocking layer generally discards an extensive set of links. Taking that
whole set as B makes the prefactor in (2) decay exponentially in m and, when
p_B grows proportionally to m, also makes C_B proportional to m. Removing
one bounded block at a time instead requires estimates for the successive
exact coarse operators and control of the accumulated number of steps.
Neither follows from (1). Uniform single-block conditional estimates do not
tensorize for an unknown interacting vacuum; `../vacuum/PROOF.md`, section 5,
already gives an explicit counterexample to that abstract inference.

**Outcome of this one-shot attempt.** An unconditional, exterior-volume-uniform
finite-block bound for the actual nonlinear finite-lattice vacuum has been
derived. The bridge still lacks a uniform estimate for an entire elimination
layer and its successive exact coarse forms, terminal metric/form coercivity,
and the continuum field construction. Therefore this is partial progress,
not Yang–Mills closure. Neither failure of this bound to close the budget nor
its poor block-size dependence disproves the Yang–Mills mass gap.
