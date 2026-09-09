# IC18: pin the conformal auxiliary; retain the pole clock

Base: `84030ea93e51b3cdb359812edabc41cefb175f8f`, 2026-09-08.
**Constructive plateau repair; full theory OPEN. The specified global
interpolation has a located homogeneous constraint-preservation obstruction.**
This continues the actual [IC17 failure](IC17_HANDOFF.md), not its aligned
pass alone. Carl's primordial-clock idea and pre-recombination question remain
the physical motivation. Holonomic pinning and the calculations here were
introduced in this investigation; no literature-wide novelty is asserted.

## 1. Why simply separating the pressure is insufficient

Consider the proposed local repair `P(X,w)=F(X)+V(z)`, `z=exp(2w)`.
It removes the mixed clock derivative, but not the algebraic matter response.
For the explicit convex example `V=k(z-1)^2/2`, a minimally coupled physical
canonical scalar gives barred matter pressure `z Y`. Varying z gives
`z=1-Y/k`; eliminating it gives `Y-Y^2/(2k)`. Therefore

    D=1-Y/k,  K=1-3Y/k,  c_matter²=(1-Y/k)/(1-3Y/k).

At `k=1,Y=1/10`, the kinetic term is positive but `c_matter²=9/7`.
For physical irrotational dust, vary
`V(z)+lambda_d(Y-z/2)` before eliminating: `z=2Y`. Its reduced pressure
is `V(2Y)` and `c_dust²=(z-1)/(3z-1)`, positive on the positive-density
branch z>1. This potential repairs one source but not the required common
light-cone condition. This is an explicit counterexample to the proposed
repair, not a theorem excluding every auxiliary potential or gravity model.

## 2. One specified global phase action

Keep the physical metric, varied clock, six leaf momenta, canonical map,
static primitive U, and boundary prescription of [IC5](IC5_ACTION.md) and
[IC10](IC10_LOCAL_CLOCK.md). These linked files define every term of H10.
Use the one-sided eta_up of [IC17](IC17_POLE_CLOCK.md), not the old compact
window. All matter still has the single action `Sm[g,psi]`.
In units `m=h0=1,kappa=6`, choose the design constants

    wc=-1/40, Sstar=3/40, Xstar=exp(-2 Sstar)/2, epsilon=10^-5,
    Xtilde=exp(2w) Xphysical=exp(-2S)/2,
    F18(X)=-m Lambda exp(4wc)+epsilon (X/Xstar)^2/(1-X/Xstar),
    J18=exp(-2w+2wc), J9=exp(-2w-1/6),
    P0(X,w)=-m exp(4w)[Lambda+a0² U(u²)]+kappa exp(2w)X,
    u=(S+2w)/(S+w), r=-Np/(3mh0).

Lambda and a0² retain the IC5 values. wc, Sstar and epsilon are design
inputs, not observations or derived constants. Introduce a varied auxiliary
multiplier L (called `lam` in the script), with no derivative term. Define

    H18 = H10[eta_up] + eta_up {
      (2 P_TF²-p²/3)/m (1/J18-1/J9)
      -m (J18-J9) Rhat/2
      +exp(-4w)[P0(Xtilde,w)-F18(Xtilde)-L(w-wc)] },

    S18 = integral sqrt(-g) [2 P:Q-H18] + Sm[g,psi].

Domain: the inherited regular chart `0<u<1, Xphysical>0` intersected with
`{r²<1/2} union {0<Xtilde<Xstar}`. In the inactive open region the entire
correction is defined to be zero before evaluating the pole. The excluded
corner `r²=1/2,Xtilde=Xstar` is not silently filled. On the pin, S>Sstar
implies `1/2<u<1`, so the early pole does not force the old u=0/1 boundary.

Near r=0 every correction jet vanishes, including the multiplier term.
Consequently the independently varied static exponential constitutive
equations survive under the inherited boundary prescription. This is NOT a
matched galaxy solution or proof that the static clock source disappears.

On eta=1, vary both momentum components first. Their stationary values are
`P_TF=m J18 Q_TF/2`, `p=-m J18 Q`. The resulting curvature/kinetic density
is Einstein gravity for `gtilde=exp(-2w)g`, with `mstar=m exp(2wc)`. Thus
the EXACT plateau action, before varying or eliminating either auxiliary, is

    integral sqrt(-gtilde) [mstar Rtilde/2+F18(Xtilde)+L(w-wc)]
      +Sm[exp(2w)gtilde,psi].

The multiplier equation is `w=wc`; the w equation determines L from the
physical matter trace. It does not prescribe a new baryon force. For example
with a physical canonical scalar, `L=-2 exp(2wc)Y`. Elimination gives

    integral sqrt(-g) [m R/2+Fphysical(Xphysical)] +Sm[g,psi],
    Fphysical(X)=exp(-4wc) F18(exp(2wc)X).

This removes the mixed clock–matter principal derivative exactly. It is a
new action, not IC17 with its bad eigenvalues overwritten. The adjusted J18
is important: the physical Einstein coefficient is m, not the rescaled IC17
coefficient. The plateau Poisson coefficient of ordinary Einstein curvature
is `G_E=1/(8 pi m)`; clock-sourced force contributions and the Newton
constant inferred in a matched MOND/PPN solution remain to be calculated.
The physical vacuum density is m Lambda. No derivation of the empirical
a0–Lambda coefficient 1/2 is supplied.

## 3. Variations, constraints and their precise scope

After the regular plateau auxiliary elimination, independent metric and clock
variation give

    m G_mu nu = Fphysical,X T_mu T_nu + Fphysical g_mu nu + Tm_mu nu,
    nabla_mu(Fphysical,X nabla^mu T)=0.

The matter Ward identity comes from the unchanged minimally coupled Sm:
its compactly supported diffeomorphism variation, on the matter equations,
gives `nabla_mu Tm^{mu nu}=0`, including before auxiliary elimination.
The scalar is a counted physical clock, not a second metric polarization.

For first-derivative scalar/fluid matter on the plateau, `p_w=p_L=0` are
primaries. Preservation gives the pin equation and the w equation as the
two secondaries. At fixed canonical matter momentum the auxiliary Schur
matrix has the form `A=[[a,1],[1,0]]`, where a is the actual matter response,
not a prescribed sign. Differentiating the raw two-velocity action computes
`det A=-1`. With constraint order `(p_w,p_L,C_w,C_L)`, the homogeneous
Poisson matrix is `[[0,-A],[A,0]]` and has determinant 1 and rank 4.
The numerical routine forms the matrix and computes its rank; it does not
return a requested rank. Preservation solves for both multipliers with no
new homogeneous auxiliary condition, whatever finite a is.

For spatial modes the pin supplies an algebraic inverse, rather than an
inverse Laplacian: if the full secondary bracket is an operator B, the
block matrix `[[0,-A],[A,B]]` remains invertible by solving its two block
equations. There is no division by k, so this auxiliary argument treats
k=0 and k!=0 equally. It is not a calculation of the global transition's
distribution-valued gravitational algebra.

On this regular plateau, eliminating the four second-class auxiliary
constraints leaves exactly Einstein gravity plus one first-derivative clock
and ordinary matter. Before elimination, metric(10)+clock(1)+w(1)+L(1)
give 13 canonical pairs; lapse/shift primaries and their diffeomorphism
secondaries give eight first-class constraints. Hence `(26-16-4)/2=3`
physical gravity-plus-clock modes, before separately counting matter:
two tensors plus one explicitly counted clock. This is the consequence of
the exact reduced action, not a numerical global Dirac certificate.

On eta=0, L drops out and p_L instead generates an auxiliary gauge freedom.
One may not carry the plateau rank across this stratum. The next section
actually checks the homogeneous transition's preservation rather than
assuming that the rank change is harmless.

## 4. Matter cones and early history from the same plateau

Put delta=1-Xtilde/Xstar in (0,1). Exact differentiation gives

    F_X = epsilon/Xstar (delta^-2-1),
    Q = F_X+2X F_XX
      =epsilon/Xstar (1-delta)(delta²+delta+4)/delta³,
    rho_pole=epsilon (1-delta)^2(delta+2)/delta²,
    c_clock²=delta(1+delta)/(delta²+delta+4),
    p_pole/rho_pole=delta/(delta+2).

Both kinetic/gradient coefficients are positive for 0<delta<1, and
`1-c_clock²=4/(delta²+delta+4)>0`. This is an analytic interior-domain
result, not a finite scan elevated to a theorem. The Einstein tensor
principal part has positive m and c_T=c throughout this plateau.

The characteristic determinant factorizes because the derived mixed jet is
zero. The script differentiates the uncoupled clock and actual minimally
coupled `Y^n` matter actions and solves their boosted quadratic factors,
checking each root in the direct determinant. Twenty tests use five signed
velocities through |v|=.9 and n=1,2,10,100. The original failing choice
S=.1, |v|=.1 is included, now in the new action's admissible chart.
This is not a claim to retain the old action's sourced density solution.

Pressureless dust is ALSO varied, not substituted by n=100. Its multiplier
constraint leaves the repeated transport characteristic c=v and the two
independent clock roots. The mixed symbol has determinant proportional to
`-d²`, d proportional to c-v. This removes IC17's complex mixed pair but
does not prove strict dust hyperbolicity or absence of ordinary dust caustics.
Fourier convention is exp[i k(x+c t)], so physical phase speed is -c.

The homogeneous equations are

    3 mstar Htilde² = rho_clock + R + M,
    q=F_X sqrt(2Xtilde), q Atilde³=constant,
    R Atilde^4=constant, M Atilde³=constant,
    Sdot=3 Htilde c_clock², Hphysical=exp(-wc)Htilde.

The last equation for S follows by differentiating q, not by assigning a
dust evolution law. Near the pole `rho_pole/q -> sqrt(2Xstar)`, so the
clock is asymptotically dust-like. Its abundance is free initial charge.
The eight-physical-e-fold history fixes final S=.1, R=.001 rho_clock and
M=.2 rho_pole as illustrative initial data. At 70 digits it reaches
S=0.07500015189375929 with radiation fraction .9990767447. Independent
charge evolution and logarithmic quadrature agree to better than 1e-60.
No present-day calibration, recombination physics, CMB spectrum, or empirical
abundance fit has been performed. The pole and X=0 endpoints and nonlinear
interaction scale remain unclosed.

## 5. Immediate next gate: full homogeneous transition already attacked

For eta>0, vary L before restriction, obtaining w=wc. On a flat isotropic
slice let V=sqrt(hbar), pi be trace barred momentum, and set V=1 to display
the density. With pi held CANONICALLY fixed, the reduced Hamiltonian is

    h(S,pi)=-exp(S-2wc) pi²/3
      -exp(S)[(1-eta(r))P0(S,wc)+eta(r)F18(S)],
    r=-exp(S-2wc)pi/3.

The homogeneous lapse secondary is h_S=0. In the script it is independently
computed from this expression and from

    exp(-S)h_S = -3r² exp(-2S+2wc)
      -(1-eta)(P0+P0_S)-eta(F+F_S)-r eta_r(F-P0).

Omitting the last term would be varying at fixed r, not fixed momentum.
The 7-by-33 search records sign-changing roots without claiming completeness.
It locates a regular-chart, expanding fold by solving h_S=h_SS=0:

    S=0.0804616377482359683, r=0.7648386913136239625,
    eta=.0033086055604015364, L=-3433.444668369335,
    Hphysical=.2947829409702309.

The full homogeneous primaries are p_S,p_w,p_L. Their three secondary
equations are the derivatives of the full homogeneous phase Hamiltonian,
BEFORE imposing the pin. On the pin the auxiliary Hessian determinant is
`-exp(2S) eta² h_SS`; the script also derives the generic identity
`det Hess(h+eta L(w-wc))=-eta² h_SS` with its rescaled multiplier coefficient.
The actual 6-by-6 primary/secondary matrix is computed from the full H,
not assembled using an expected rank. At the located fold its computed rank
is 4 (threshold and all singular values are reported), so preservation
requires a compatibility condition.
The secondary/secondary block is computed from the same canonical variables;
it vanishes on the homogeneous secondary surface, rather than being assumed
zero in constructing the matrix.

Continue preservation: with q_metric=ln B, p_q=2pi, the unreduced volume
density is `H=V h(S,p_q/(2V))`. Its actual canonical bracket yields

    {H_S,H}=(3V/2)(h_S h_pi-h_Spi h).

On h_S=0 and h_SS=0, the pin forces wdot=0; no choice of finite Sdot
or Ldot can cancel this bracket in the remaining lapse equation. At the
fold the bracket is **-103.9793342900156**, not zero. A second direct
differentiation in (q_metric,p_q) agrees below 3e-69. Thus this point solves
the primary/secondary equations but fails the next preservation condition.
It is NOT admissible smooth evolved data. The computation does not claim
that all cosmological initial data reach it, or that every possible smooth
MOND/cosmology interpolation is impossible.
The fold is re-solved at 90 digits and compared with the 70-digit result.
This is high-precision numerical branch evidence, not an interval-certified
existence theorem. The compatibility equation itself is an exact derivation.

This is the next exact construction target, not a reason to discard the
successful plateau mechanism: revise the global interpolation so that its
actual constrained evolution either avoids the fold on a demonstrated
invariant physical domain or supplies a regular, compatible continuation.
A nonzero auxiliary determinant on the plateau cannot establish either.
The proposed IC18 interpolation is **not uniformly Dirac-regular** on its
nominal primary/secondary branch and must not be certified complete.

## 6. What is, and is not, closer to the original objective

The original failure has been repaired by an explicit action-level operation:
the clock no longer acquires a mixed principal coupling through algebraically
responding matter units on the expanding plateau. That same action supplies
a positive tensor sector, a counted causal clock, ordinary matter conservation,
and a dust/radiation/vacuum background. No auxiliary kinetic term was added.

The next global bottleneck is now an explicit transition preservation equation,
not an unspecified desire for a new ansatz. Still missing: regular full spatial
transition, matched galactic solutions with independently derived Phi and Psi,
baryon-only exponential MOND, PPN beta/gamma/alpha_i, zero-field control,
strong-coupling scales, and empirical cosmology/cluster tests. The fitted
a0–Lambda normalization remains input. All must hold in ONE revision.

Reproducibility is in `ic18_run_001/run_index.json`. Self-review covers this
note and the new script/tests, not an independent review of the entire repo.
Lean was not used; an exact identity checker would not by itself certify the
numerical branch or the unsolved spatial field equations.
