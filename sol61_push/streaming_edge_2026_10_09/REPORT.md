# A kinetic support theorem for finite RAR halos

Checkpoint: 2026-10-09, based on `baf7e3dd46582631887fa889c6e9a12ea5362210`.
Scope: the cold-energy target in `campaign_fresh_gravity/THEORY_v1_2026-10-09.md`.

**The full theory remains open.** This calculation supplies a nonnegative stationary orbital distribution for a specified family of its finite halos. It also identifies two constraints on the still-missing settling dynamics. It does not derive the RAR kernel, the cold abundance, the dark-energy coupling, or kappa=1/2.

## Target and result

Use units G=M_b,total=a0=1, so the length unit is r_M=sqrt(G M_b,total/a0). Let the spherical baryons have a Hernquist scale b:

\[
M_b(r)=\frac{r^2}{(r+b)^2},\qquad
M_c(r)=\frac{M_b(r)}{e^{1/(r+b)}-1}\quad(0<r<R).
\]

Choose any finite supply q>0 and fix R by M_c(R)=q. Hold M_c=q outside R. Baryons retain their full Hernquist profile outside R. The cold density jumps to zero at R; there is no delta-function mass shell because enclosed mass is continuous.

**Theorem.** For every b>=1 and every q>0, this halo has a nonnegative, globally stationary distribution in the fixed spherical, self-consistent baryon-plus-cold potential, with tangential Osipkov–Merritt (TOM) orbital structure and an invariant angular-momentum cutoff. Interior orbits can have radial motion. This is an equilibrium existence theorem under a collisionless kinetic description, not a formation or stability theorem.

The method is known: [Baes, *Self-consistent dynamical models with a finite extent—II*, arXiv:2301.03873v1](https://arxiv.org/abs/2301.03873), equations (9)–(16), supplies the TOM inversion. Its general consistency hypothesis is not imported as a theorem. The positivity proof below is specific to this RAR/Hernquist family. This is a new calculation in this work package, not a claim of worldwide novelty. The already-recorded circular-orbit construction in `../RESULTS_2026-09-29.md` is not counted again.

## Distribution, support, and exact potential

Write g=Phi'>0, psi(r)=Phi(R)-Phi(r), A=1-r^2/R^2, and h=A rho_c. Here

\[
g=\frac{1}{(r+b)^2[1-e^{-1/(r+b)}]},\qquad
\psi=\log(e^{1/(r+b)}-1)-\log(e^{1/(R+b)}-1).
\]

The potential needs no numerical radial integration. Define

\[
Q=\psi-\frac{v_r^2}{2}-\frac{A(v_\theta^2+v_\phi^2)}2.
\]

Rescaling the tangential velocities gives

\[
h(\psi)=4\pi\sqrt2\int_0^\psi f(Q)\sqrt{\psi-Q}\,dQ,
\quad
f(Q)=\frac{1}{\sqrt8\pi^2}
\left[\frac{h_\psi(0)}{\sqrt Q}
+\int_0^Q\frac{h_{\psi\psi}(u)}{\sqrt{Q-u}}du\right].
\]

At the edge, h_psi(0)=2 rho_R/(R g_R)>0. For b>0 the maximum psi is finite; the inversion is used for 0<Q<psi(0), with the central cusp understood as a limit.

There is an important global support condition. With E=v^2/2+Phi and L the specific angular momentum, set

\[
F(E,L)=f(Q)\Theta(Q)\Theta(L_R^2-L^2),\qquad
Q=\Phi(R)-E+\frac{L^2}{2R^2},\qquad L_R^2=R^3g_R.
\]

Without the last cutoff, f(Q) alone could populate an unwanted external branch. It removes no interior velocities: nondecreasing total enclosed mass gives

\[
L^2<\frac{2\psi r^2}{A}
\le\frac{2G M_{\rm tot}(R)Rr}{R+r}<L_R^2\qquad(r<R).
\]

Outside R, the effective potential has derivative
G M_tot(r)/r^2-L^2/r^3>0 for L^2<=L_R^2. But Q>0 requires E<V_eff(R), so no exterior phase-space point is occupied. Both cutoffs use integrals of spherical motion. Thus F is globally stationary and its velocity integral reproduces the assigned cold density; that density generates the assigned potential together with the fixed baryons.

## Positivity proof for b>=1

Put x=1/(r+b), n=(e^x-1)^(-1), c=1+n, t=1/c, a=x c, d=x(1+2n), z=b x. The symbol a in this proof is dimensionless and is not a0. For b>=1 and r>0,
0<x<1, 0<z<1, 1<a<2, and d<3. Indeed e^x-1>x gives xn<1, so a=x+xn<2 and d=x+2xn<3; 1-e^-x<x gives a>1.

With D=t d/dx=d/dpsi, the density decomposes as

\[
4\pi\rho=F_0+VU,\qquad
F_0=x^4nc,\quad U=x^4n,\quad V=\frac{2b}{1-bx}.
\]

Direct differentiation gives

\[
DU=e^{-x}x^3(4-a)>0,
\quad D^2U=t e^{-x}x^2[12-4(x+a)+a^2]>0,
\]
\[
D^2F_0=\frac{n x^2}{c}
[12-12a+4a^2+x(4-3a)]>0.
\]

The first square bracket is at least (a-2)^2+4. For the second, if a<=4/3 drop its nonnegative x term; otherwise bound x<=1 and obtain 4a^2-15a+16>=31/16. Also V,DV,D^2V are positive, so rho_psipsi>0.

The density slope gamma=-r rho'/rho exceeds one, because

\[
\partial_x(4\pi r\rho)
=xn\{a(3-d)(1-z)+(6-3a)z\}>0.
\]

The force slope alpha=-r g'/g obeys

\[
\alpha=(1-bx)(2-xn)
\le(1-x)(1+x/2)\le1.
\]

Here xn>=1-x/2 follows from x coth(x/2)>=2. Finally,

\[
\boxed{h_{\psi\psi}
=A\rho_{\psi\psi}
+\frac{2\rho}{R^2g^2}(2\gamma-1-\alpha)>0.}
\]

Both terms in the inversion are positive. This proves f(Q)>0 throughout the open physical energy interval, for every finite edge R and therefore every q>0. The proof does not require the numerical scout.

## The finite edge has a physical stress limit

The second moments obey

\[
\sigma_r^2=\frac{\int_0^\psi h(u)du}{h(\psi)},\qquad
\sigma_\theta^2=\sigma_\phi^2=\frac{\sigma_r^2}{A},\qquad
\beta=-\frac{r^2}{R^2-r^2}.
\]

As r approaches R from below,

\[
\sigma_r^2\sim\frac{g_R(R-r)}2,\qquad
\sigma_\theta^2,\sigma_\phi^2\longrightarrow\frac{Rg_R}4.
\]

Radial pressure vanishes at the edge although density remains finite. No rigid wall is introduced. This is a population of bound inward- and outward-moving orbits with zero net flux. It is not a net through-stream, nor a derivation of capture or irreversible retention.

## What fails, and what the numerical checks add

The literal point-baryon target cannot have this TOM structure. Its central density behaves as r^-4 exp(-1/r), hence h tends to zero while psi tends to infinity. A nonzero nonnegative f makes its Abel transform h nondecreasing. This contradiction rejects TOM for the point-source target, not every anisotropic distribution.

The frozen scout used b in {0.03,0.1,0.3,1,3}, q in {0.5364,5.364}, 72 energies per case, and a separate augmented-density derivative grid. The q values are illustrative retained supplies, not fitted or selected abundances.

| b/r_M | q=0.5364 | q=5.364 | conclusion |
|---:|---:|---:|---|
| 0.03 | 10 negative samples | 10 negative samples | TOM fails |
| 0.1 | 17 negative samples | 17 negative samples | TOM fails |
| 0.3 | 0 negative samples | 0 negative samples | finite numerical support only |
| 1 | 0 negative samples | 0 negative samples | also covered by proof |
| 3 | 0 negative samples | 0 negative samples | also covered by proof |

The compact failures also violate the necessary h_psi>=0 condition. Negative inversion contributions are order-one fractions of their absolute integrals, not cancellation at roundoff. No exact compactness threshold has been located.

`scout.py` passes 743 implementation checks, primarily potential inversion and analytic boundary identities; these are not independent physical tests. Omitting the boundary term fails all three uniform-sphere benchmark reconstructions. `roundtrip.py` independently codes the density formula and forward-integrates the resulting orbital populations at 18 model/radius combinations. It recovers the target to a maximum relative difference 7.11e-15; 32-to-64-point refinement changes it by at most 1.45e-15. This is a numerical identity check, not observational precision. Both codes share the Abel formula and SymPy. All three provenance manifests validate, and stderr logs are empty.

## Two constraints on a settling mechanism

### A passive bath must satisfy the thermal stability gate

For weakly coupled equilibrium branches with additive conserved total energy, positive temperatures, and heat capacities C_h and C_b, the assumed exchange Qdot=K(T_h-T_b), K>0, gives

\[
\dot S=\frac{K(T_h-T_b)^2}{T_hT_b}\ge0,\qquad
S''=-T^{-2}(C_h^{-1}+C_b^{-1}).
\]

If the halo branch has C_h<0<C_b, a strict local entropy maximum requires

\[
\boxed{0<C_b<|C_h|.}
\]

A large thermostat is unstable in this model. These are equilibrium-branch heat capacities; the sign of the actual halo branch must be computed, not inferred from the local gas heat capacity. With C_h=-A_h, C_b=B constant, the equilibrium export is
DeltaE=(T_h0-T_b0)/(1/B-1/A_h). Tuning B to hit the target is not a mechanism selecting it.

For context, CFG489's existing canonical 10^10-solar-mass point-host budget has E_i=-0.7556616779 and E_target=-3.5751560218 in M_b V_f^2. It requires export 2.8194943439, about 78.9% of |E_target|. This is that earlier model's budget, not the energy of the TOM models constructed here. Source: `campaign_fresh_gravity/CFG489_nc1_gr_cold_fluid_mond/cfg489_results.json`, `step3.rows.point|1e10|canonical`.

Any settling-stress work also needs explicit energy storage or transfer. Adding a bath equation alone does not repair CFG489's stress energetics or its off-target spatial instability. The conductance law above is illustrative, not microscopically derived.

### A scalar pressure cannot hold an exactly round halo in a disk field

For static nonrotating isotropic stress, grad p=-rho grad Phi implies
grad rho cross grad Phi=0. Where a spherical density has rho'(r)!=0, the total force must therefore be radial. An uncompensated disk quadrupole violates this condition. Constant-density regions, extra forces, anisotropic stress, rotation and time dependence require their own analysis. Boundary pressure cannot cure the smooth bulk obstruction.

The TOM model supplies anisotropic stress in a spherical potential. It has not yet been continued into a disk potential, where E and the magnitude L are no longer the same pair of conserved quantities.

## Decision and next discriminating work

1. Retain the b>=1 equilibrium theorem and use it as a concrete target for perturbations. Do not rerun the old circular construction or the rejected isotropic-fluid attractor.
2. Before a formation simulation, calculate the response of this orbital population to a baryonic quadrupole and test its free quadrupole modes. This decides whether the round-halo requirement survives a disk. The spherical invariants cannot simply be carried over.
3. For compact baryons, test a different inner anisotropy or a general orbit-superposition construction. The specific TOM rejection does not establish nonexistence. Preserve the exact RAR target during that test.
4. A formation calculation needs a specified energy/angular-momentum receiver and a coupling with total energy and entropy accounting. Its kinetic equilibrium must be derived without inserting this f as a prescribed attractor. The bath heat-capacity gate is necessary within its stated model, not sufficient.

The theory's remaining named obligations are formation and spatial stability, compact/disk hosts, supply selection and sharing, a covariant completion, and the exact coefficient. The present work advances equilibrium realizability only. It does not make a priority claim over CARDA or other literature.

Review: the kinetic formulas, global support restriction, point-source obstruction, and positivity proof were derived by a separate agent and checked by the lead. A further independent audit is recorded in REVIEW.md. The thermal and roundness gates received separate algebraic review. The numerical code was inspected against the independently derived formulas.
