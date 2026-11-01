# Startup by a localized stress semigroup: exact reduction, scalar theorem, and remaining inequality

Base: `X48-TRANSPORT-2026-11-01-B`; normalized parameters and the exact
`ConvectiveCollapse` semidiscrete equations. This note owns this file only.
No model change, trajectory integration, or finite-grid extrapolation was used.

**Verdict.** The requested full-system startup lemma is not proved here. There
is a useful exact positive-square identity for compression, an explicit
mesh-uniform boundary-penetration theorem for its homogeneous principal
operator, and a single explicit nonlinear commutator estimate which would
complete the startup lemma with `T=1/1000`, `c=4`, and every `N>=32`.
The commutator estimate is not established by this note. In particular, the
scalar theorem below must not be substituted for the full equations.

## 1. Compression has no adverse geometric velocity term

Use cells `i=1,...,N`, nodes `r_0=u_0=0`, masses `dm=M/N`,
`M=pi/3`, node weights `mu_i=dm` for `i<N` and `mu_N=dm/2`.
Write

\[
 V_i={4\pi\over3}(r_i^3-r_{i-1}^3),\qquad
 x_i=-\theta_i=-{4\pi(r_i^2u_i-r_{i-1}^2u_{i-1})\over V_i},
 \qquad \rho_i=dm/V_i.
\]

Here `x` is signed compression; the heater uses `(x)_+`. Define

\[
 a_i={(4\pi r_i^2)^2\over\mu_i},\quad a_0=0,\qquad
 (\mathcal L_r f)_i=
 {a_i(f_{i+1}-f_i)-a_{i-1}(f_i-f_{i-1})\over V_i},
 \tag{1}
\]

with exterior stress `f_{N+1}=0`. The center has no flux. The full material
stress is, exactly,

\[
 S_i=P_i+\kappa_i(x_i-2)_++\zeta_i x_i,\qquad
 \kappa_i={1\over2}\rho_iW_i h_i,\qquad
 \zeta_i=\kappa_i{K_i\over K_i+1/100},\qquad
 P_i=K_i\rho_i^2h_i.
 \tag{2}
\]

Differentiating the volume divergence and using the actual nodal momentum
equation gives the following exact identity while geometry is valid:

\[
 \boxed{\quad
 \dot x_i=R_i+(\mathcal L_rS)_i,\qquad
 R_i=4\pi\rho_i+{x_i^2\over3}+
 {6r_ir_{i-1}(r_i u_{i-1}-r_{i-1}u_i)^2
  \over(r_i^3-r_{i-1}^3)^2}\ge0.
 \quad}                                                     \tag{3}
\]

Indeed, with `D=r_i^3-r_{i-1}^3`, the kinetic part before completion of
squares is

\[
 x_i^2-{6(r_iu_i^2-r_{i-1}u_{i-1}^2)\over D}
 ={x_i^2\over3}
 +{6r_ir_{i-1}(r_i u_{i-1}-r_{i-1}u_i)^2\over D^2}.
\]

The gravitational term is `4pi dm/V_i`, including in the outer cell;
the half outer nodal weight affects `a_N`, not this term. Thus compression
loss comes entirely from the stress Laplacian, not from an uncontrolled
negative radial shear term.

A limited but exact invariant follows: **if `P` and `zeta` are omitted**, the
old-heater-only equations preserve `x_i>=2` globally from these activation
data. At a first contact with `x_i=2`, its own old stress is zero, every
neighboring old stress and the exterior stress is nonnegative, and (3)
points inward. This neither proves strict excess above two on a fixed
interior region nor applies unchanged when the omitted stresses are restored.

## 2. Homogeneous principal graph and an explicit penetration bound

Continue the exact homogeneous dust functions after activation as reference
functions only:

\[
 r_i^d=a(s)(i/N)^{1/3},\qquad
 \rho_d={1\over4a^3},\qquad x_d=-3a'/a,\qquad
 a''=-{\pi\over3a^2},\qquad a(0)=4^{-1/3}.
\]

The activation velocity gives the `C_a=x_d(0)` in `seed_route.md`.
Let `K_d(0)=0` and evolve the homogeneous local heaters, including memory
damping, on this reference geometry; its heat flux is zero. This defines
`kappa_d`, `zeta_d`,

\[
 \nu_d=\kappa_d+\zeta_d,\qquad
 S_d=\kappa_d(x_d-2)+\zeta_dx_d+P_d.
 \tag{4}
\]

It is not a solution of the vacuum-boundary ODE after activation.

Let `L_d(s)` be (1) on the homogeneous reference geometry, retaining the
actual half outer nodal weight. Consider just the scalar boundary problem

\[
 \dot w=\nu_d(s)\mathcal L_d(s)w,\qquad
 w_i(0)=0,\qquad
 w_{N+1}(s)=B_d(s):={S_d(s)\over\nu_d(s)}.
 \tag{5}
\]

The ratio has a finite right limit at zero, namely `C_a-2`. It is prescribed
as boundary data in (5). This is the principal stress-diffusion problem,
not the coupled shell problem.

**Scalar theorem.** For every `N>=32` and `0<=s<=1/1000`,

\[
 0\le w_i(s)<{1\over32},\qquad i\le\lfloor N/4\rfloor.
 \tag{6}
\]

**Proof, including constants.** On the larger interval `s<=1/100`, the dust
ODE has

\[
 1\le\rho_d\le2,\quad x_d\le8,\quad a\le1,
 \quad h_d\le243s^2,\quad \nu_d\le972s^2.
 \tag{7}
\]

For example `21/4<C_a<6` follows directly from its exact expression and
`3<pi<22/7`, `19/12<4^(1/3)<8/5`. As long as `rho_d<=2`, `x_d<=8`,
its derivative `4pi rho_d+x_d^2/3` is below 47; these bounds cannot first
fail before `1/100`. Also `rho_d-1<=exp(8s)-1<=9s`, giving the gate bound.
Since `W_d<=2`, `kappa_d<=486s^2` and `zeta_d<=kappa_d`.
The homogeneous heater obeys

\[
 \dot K_d\le 8h_d(8/2-1)+\tfrac12h_d8^2
 \le13608s^2,\qquad K_d\le4536s^3<1.
\]

Consequently

\[
 0\le B_d\le x_d+{P_d\over\kappa_d}
 =x_d+{2K_d\rho_d\over W_d}<12.
\]

The scalar maximum principle, valid for this finite time-dependent graph,
gives `0<=w_i<=12` on the entire grid. We may therefore restrict (5) to
`i<=N-1` and use `w_N<=12` as boundary data, avoiding the special outer
weight in the exponential-barrier calculation.

For `i<N`, write the two jump rates of `nu_d L_d` as `b_i^+`, `b_i^-`.
Direct substitution of `M=pi/3` gives

\[
 b_i^+=36\nu_daN^2(i/N)^{4/3},\quad
 b_i^-=36\nu_daN^2((i-1)/N)^{4/3},
\]

and hence

\[
 b_i^++b_i^-\le72\cdot972s^2N^2,\qquad
 0\le b_i^+-b_i^-\le48\cdot972s^2N.
\]

For `E_i=exp[-lambda(1-i/N)]`, Taylor's inequality gives

\[
 {\nu_d\mathcal L_d E_i\over E_i}
 \le s^2\Psi(\lambda),\qquad
 \Psi(\lambda)=48\cdot972\lambda
             +36\cdot972\lambda^2e^{\lambda/32}.
 \tag{8}
\]

Thus `12 E_i exp[Psi(lambda)s^3/3]` is a supersolution on `i<N`, has
boundary value at least 12 at `i=N`, and dominates the zero initial data.
For `lambda=8`, `Psi(8)<4*10^6`. Since `i/N<=1/4`,

\[
 w_i(s)\le12\exp[-6+\Psi(8)s^3/3]
 <12\exp[-6+1/500]<1/32
\]

for `s<=1/1000`, proving (6). All constants are independent of `N`.

This elementary finite-graph barrier needs no continuum heat-kernel theorem.
It also avoids a false uniform short-time Gaussian claim: for fixed `N`, a
matrix exponential has a polynomial first nonzero off-diagonal Taylor term,
which cannot be bounded by `C exp(-d^2/t)` as `t` decreases to zero with
fixed constants. The exponential-distance estimate (8), with its explicit
jump-size correction `exp(lambda/32)`, remains valid in that regime.

## 3. One exact nonlinear inequality that would finish startup

The scalar calculation can be embedded into an exact variation-of-constants
identity for the full system. This makes the unproved input unambiguous.
Use the actual solution in all quantities carrying no `d` subscript. Set

\[
 w_i=x_d-x_i,\qquad
 S_i^{lin}=S_d-\nu_dw_i,\qquad
 \delta S_i=S_i-S_i^{lin}.
\]

Both `S^{lin}` and `delta S` have zero exterior stress. For algebraic use of
`L_d` on `w`, prescribe the same ghost value `w_{N+1}=B_d` as in (5).
No assumption about a physical ghost compression is being made. Then (3)
is exactly

\[
 \dot w=\nu_d\mathcal L_dw+(R_d-R)+\mathcal E,
 \qquad R_d=\dot x_d=4\pi\rho_d+x_d^2/3,
 \tag{9}
\]

where

\[
 \boxed{\quad
 \mathcal E=(\mathcal L_d-\mathcal L_r)S^{lin}
                      -\mathcal L_r\delta S.
 \quad}                                                     \tag{10}
\]

In particular this remainder retains the full moving geometry, old-heater
coefficient variation, pressure, and memory damping. The actual heat law
enters through its actual `K` in these stresses. It has not been discarded.

Let `P_N(s,v)` denote the positive evolution operator of
`nu_d L_d` with **zero** exterior boundary value. It is a contraction on
`l^infinity`, by the finite-graph maximum principle. The boundary solution
of (5) will be denoted `w^0`. Exact Duhamel gives

\[
 w(s)=w^0(s)+\int_0^sP_N(s,v)[R_d(v)-R(v)]\,dv
                  +\int_0^sP_N(s,v)\mathcal E(v)\,dv.
 \tag{11}
\]

The new square identity is useful here: since `R>=0` and `R_d<47`,

\[
 \int_0^sP_N(s,v)[R_d-R]\,dv\le47s\,\mathbf1
 \tag{12}
\]

without any upper bound on the actual compression, density, or shear.

Therefore the following single estimate, if proved for the full law, is
sufficient:

\[
 \boxed{\quad
 \sup_{N\ge32}\ \sup_{0<s\le10^{-3}}\
 \max_{i\le\lfloor N/4\rfloor}
 \left[\int_0^sP_N(s,v)\mathcal E(v)\,dv\right]_i\le1.
 \quad}                                                     \tag{NE}
\]

Indeed (6), (11), (12), and `C_a>21/4` would give

\[
 x_i(s)\ge C_a-1/32-47/1000-1>4
\]

throughout the central quarter for this common interval. Signed compression
is then positive there and equals `C_i`. The existing source-driven
auxiliary theorem in `seed_route.md` would give the requested persistent
inner-five-percent entropy floor with

\[
 \epsilon=64\cdot10^{-9}(1-2\cdot10^{-3})(2/19)^3>0.
\]

This is an implication from (NE), not a proof of (NE). Local valid geometry
on the interval is also required to write (9); fixed-mesh continuation is
addressed separately in `preservation_route.md`.

## 4. Why the available energy identities do not prove (NE)

There are two derivative-bearing terms in (10), not merely a bounded local
reaction. Even with geometry fixed, the old-heater part of the stress error
on the branch `x>2` includes

\[
 [\kappa(\rho)-\kappa(\rho_d)](x-2).
\]

Near activation, `kappa=O(s^2)` but `partial_rho kappa=O(s)`, while

\[
 \log(\rho_i/\rho_d)=-\int_0^s w_i(v)\,dv.
\]

Thus a bounded compression deviation gives a density deviation of order
`s`, and a stress error of order `s^2` — the same order as the principal
stress. Decreasing `T` alone does not make this coefficient variation a
small relative perturbation. Applying `L_r` further creates second spatial
differences. A pointwise constitutive bound is not a bound on this term.

The center and vacuum boundary also rule out silently using a uniform
Cartesian graph bound on arbitrary actual geometries. The conductances in
(1) involve `r_i^4/(mu_i V_i)`; energy controls neither individual cell
volumes nor their second differences uniformly in `N`. The exact surface
`N^2s^3` compression correction in `seed_route.md` is consistent with (6),
but prevents estimating (10) in a global unweighted pointwise norm by local
ODE continuity.

A direct scalar minimum argument for `x` has the same obstruction. At a
first interior contact `x_i=c>2`, assuming neighboring `x_j>=c`,

\[
 (\mathcal L_rS)_i\ge
 (c-2)(\mathcal L_r\kappa)_i
       +c(\mathcal L_r\zeta)_i+(\mathcal L_rP)_i.
 \tag{13}
\]

These three signed curvatures have no sign supplied by energy or entropy
production. Replacing them by zero assumes exactly the missing spatial
control. A contact at `c=2` removes the first term but not the other two.

Using stress itself as the parabolic coordinate is promising but does not
remove the issue for free. On `x>2`, the chain rule gives exactly

\[
 \dot S_i=\nu_i(\mathcal L_rS)_i+\nu_iR_i
 +(\partial_\rho S_i)\rho_i x_i
 +(\partial_KS_i)[Q_i+H_i(K)],\qquad
 \nu_i=\kappa_i+\zeta_i.
 \tag{14}
\]

The last term contains the nonlinear heat-divergence operator multiplied by
`partial_K S`. It has no scalar maximum-principle sign at a maximum or
minimum of `S`. Dropping it, or treating the density term as bounded without
its activation scaling, is not a proof. A coupled localized energy estimate
could control it, but such an estimate must also yield the pointwise
Duhamel bound (NE), not only an integrated velocity or entropy bound.

One concrete continuation is to work with the normalized variables
`(S-S_d)/s^2`, `log(rho/rho_d)/s`, and `(K-K_d)/s^3`, retain their coupled
principal matrix, and prove a localized graph estimate with the same
exponential mass-coordinate weights as (8). This would need a mesh-uniform
estimate on the moving conductances or a direct weighted relative-energy
argument that controls their commutator in the dual semigroup norm of
(NE). None of these nonlinear estimates has been supplied here.

## 5. Would a weaker `2+gamma s` threshold avoid the obstruction?

The favorable gravity term makes this a sensible alternative, but does not
by itself prove it. At a first contact with the spatially constant barrier
`x_i=2+gamma s`, assuming its neighboring cells remain above that barrier,
(3) gives the sufficient condition

\[
 \gamma\le4\pi\rho_i+{(2+\gamma s)^2\over3}
       +\gamma s(\mathcal L_r\kappa)_i
       +(2+\gamma s)(\mathcal L_r\zeta)_i
       +(\mathcal L_rP)_i.
 \tag{15}
\]

The first adverse curvature now carries the small factor `gamma s`.
The other two still require spatial control. Near a vacuum surface,
`L_r kappa` can be of order `-N^2s^2`, so the gravity term cannot supply a
global constant barrier on its own. On the central quarter one again needs
a localized estimate; setting those curvatures to zero is not justified.

If this weaker startup barrier were proved, it would still seed the core.
Indeed `rho_i>=exp(2s+gamma s^2/2)>=1+2s`, so for `s<=1/2` the old heater
would obey

\[
 Q_i\ge (2)(\gamma s/2)h(1+2s)
       =4\gamma s^3(3-4s).
\]

Its integrated source is

\[
 B(T)\ge3\gamma T^4-{16\gamma\over5}T^5>0
\]

for a sufficiently short fixed interval. The existing auxiliary comparison
would preserve that seed. This reduces the desired local excess but does
not remove the stress-curvature estimate in (15).

In the exact semigroup reduction, allowing the nonlinear contribution in
(NE) to be bounded by 3 instead of 1 would already imply a fixed compression
bound exceeding 2.17 on the chosen interval, using only `C_a>21/4`.
Consequently an extremely accurate nonlinear perturbation theorem is
unnecessary. A finite uniform upper bound below roughly 3.17 would suffice.
No such bound is established here.

## 6. Proof and verification scope

Proved in this note: the exact identity (3), the old-heater-only weak
threshold invariant, the explicit scalar penetration estimate (6), and the
conditional implication `(NE) => startup with T=1/1000,c=4`.

Open: (NE) for the actual law. No full stability PDE theorem is required by
the reduction, but neither scalar parabolic intuition nor the `s^2` gate
onset closes the nonlinear commutator. No external theorem is invoked;
all graph comparison and barrier steps are finite-dimensional and derived
above. The positive-square identity was also checked by symbolic expansion. The
new note received a mathematical proofreading pass over its notation, indices,
display delimiters, and cross-references.

Read inputs: `collapse.py`, `material.py`, `transport.py`,
`convective_transport.py`, the material/transport derivations, and the three
existing `floor_theorem` route notes. Self-review checked the stress signs,
center and outer nodal weights, the signed/positive compression distinction,
the ghost-stress algebra in (9), and the nonuniform-small-time issue in a
Gaussian kernel claim. No computation is a load-bearing trajectory result.
