# Constraint preservation and the clock current

2026-10-15. This continues the proper material-velocity source of [CHB](../cold_harmonic_boundary_2026_10_15/SOURCE.md). All results here concern the pure Einstein-plus-algebraic F(ΦI,B,C) action unless explicitly stated. There is no derivative repair term, optical pump or controller-current interaction in this constraint calculation. The physical propulsion goal remains open.

## 1. The nonlinear Hamiltonian constraint is not by itself first class

Normalize M=1. In an interior patch where h>0 is constant, at the V=0 rest branch the constitutive source jets vanish. The reduced Hamiltonian constraint is

\[
\mathcal C=\mathcal H_{GR}+{P_iP_i\over8h\sqrt\gamma}
+{h\sqrt\gamma\over2}|\gamma^{-1}-I|^2.
\]

Here P_i=−2γik Dj p^{kj} is the Einstein spatial momentum density. It is not separately constrained to zero in this material patch: the algebraic shift equation determines the ratio β/N from P. In vacuum it is retained as a constraint, not divided by h.

For a legitimate local subsector take γ=diag(q1,q2,q3), p^{ij}=diag(p1,p2,p3), all depending on z. Smear C with compactly supported functions n(z),m(z) in that constant-h patch. Energies and brackets are per unit transverse area. At this subsector the off-diagonal functional derivatives vanish for such smearings, so the diagonal bracket is also the full bracket evaluated on these data.

The exact expressions before imposing flat γ are

\[
P_z=p_1q_1'+p_2q_2'-p_3q_3'-2q_3p_3',\quad
\mathcal H_{GR}={2\sum_i(q_ip_i)^2-(\sum_iq_ip_i)^2\over\sqrt{q_1q_2q_3}}
-\tfrac12\sqrt{q_1q_2q_3}\,{}^{(3)}R,
\]

\[
{}^{(3)}R=-{q_1''\over q_1q_3}-{q_2''\over q_2q_3}
+{(q_1')^2\over2q_1^2q_3}+{(q_2')^2\over2q_2^2q_3}
-{q_1'q_2'\over2q_1q_2q_3}
+{q_1'q_3'\over2q_1q_3^2}+{q_2'q_3'\over2q_2q_3^2}.
\]

Take Euler functional derivatives with respect to qi and pi **before** evaluating at q1=q2=q3=1. Freezing the metric before variation would incorrectly remove the curvature terms and the momentum-density metric dependence.

On the further family p1=p2=t(z), p3=p(z)>0, the constraint becomes

\[
\mathcal C_f=p^2-4tp+{(p')^2\over2h}.
\]

The exact functional bracket is

\[
\{\mathcal C[n],\mathcal C[m]\}
=\int(nm'-mn')\,\mathcal B\,dz,\qquad
\mathcal B=-2p'\left(1+{\mathcal C_f\over4h}\right).
\]

A total spatial divergence drops because the smearings are compact. The [exact run](run_v1/calculation/results.json) computes all six Euler derivatives from the unfrozen Hamiltonian and independently checks them against direct flat-metric formulas, then checks the bracket modulo that exact divergence. This is a universal identity in the specified smooth local family, not a sampling of profiles.

Choose

\[
t={p^2+(p')^2/(2h)\over4p}.
\]

Then C_f=0 identically, including all its derivatives, but B=−2p'=P_z can be nonzero. Thus the bare Hamiltonian constraint is **not first class modulo itself**. No claim is made about its bracket modulo additional constraints that the full Dirac algorithm may impose.

Preservation under H[N]=C[N] in this local family gives

\[
\dot{\mathcal C}=2P_zN'+P_z'N=0.
\]

For positive N this is equivalent to (N²P_z)'=0. Where P_z is nonzero it determines a local lapse profile rather than automatically producing the additional mode-removing constraint one might have inferred from lapse linearity. For p=p0 e^{kz}, a positive local solution is N=N0 e^{−kz/2}. This is a constraint-consistency solution on an initial-data patch, not an evolving spacetime solution.

At a zero of P_z, a positive regular lapse requires P_z'=0. For an explicit smooth constraint-compatible family p=δ(1+ε cos z), δ>0,0<ε<1, at z=0 one has P_z=0 but P_z'=2δε>0. No positive regular lapse can preserve C there. These data satisfy the bare Hamiltonian constraint but not the full consistency conditions. Since δ may be arbitrarily small, one cannot omit the consistency condition merely by asking for small momenta. This is not a ghost proof: inadmissible initial data must be removed by the constraint algorithm.

In a genuinely one-dimensional connected region where this flux relation holds throughout, a zero of P_z and a finite positive lapse force the conserved N²P_z to vanish, hence P_z=0 throughout that region. The earlier frozen-metric family need not extend globally through a material boundary. No global spherical inference is made from this statement.

## 2. The exact all-three-dimensional clock equation

Let X=−(∂Φ0)²>0, with Uμ=−∂μΦ0/√X and contravariant projector P=g inverse+U tensor U. The clock enters F only through

\[
B^I=U^\mu\partial_\mu\Phi^I,\qquad
C^{IJ}=P^{\mu\nu}\partial_\mu\Phi^I\partial_\nu\Phi^J-\delta^{IJ}.
\]

There is no explicit Φ0 dependence. Under δΦ0=π,

\[
\delta U^\mu=-{P^{\mu\nu}\partial_\nu\pi\over\sqrt X},\qquad
\delta\mathcal F=\delta U^\mu\partial_\mu\Phi^I
[\mathcal F_{B^I}+2\mathcal F_{C^{IJ}}B^J].
\]

Integration by parts yields the clock equation

\[
\nabla_\nu\left[{P^{\mu\nu}\partial_\mu\Phi^I\over\sqrt X}
(\mathcal F_{B^I}+2\mathcal F_{C^{IJ}}B^J)\right]=0.
\]

In unitary gauge Φ=x, P00=P0i=0, Pij=γij and √X=1/N. Define the material-coordinate vector density

\[
W^i=\sqrt\gamma\,\gamma^{ij}
[\mathcal F_{B^j}+2\mathcal F_{C^{jI}}B^I].
\]

The exact equation is

\[
\boxed{\partial_i(N^2W^i)=0.}
\]

After eliminating the algebraic shift, W is a function of canonical fields and their spatial derivatives, while the lapse appears as above. This is an instantaneous consistency condition, not a demonstrated signal-speed law. General covariance relates it to consistency of the metric equations; it is not an independently added force law.

Near the rest state, F_B=4hB and F_C B is second order, so W≈4hB. The shift equation gives W≈−P. The linear clock condition therefore enforces div P=0, consistent with the secondary consistency condition that cannot be inferred from C=0 alone.

For smooth W in the material chart and N>0, along a flow dx/ds=W,

\[
{d\over ds}\log N=-\tfrac12\partial_iW^i.
\]

A closed orbit needs zero integrated divergence to admit a single-valued positive lapse. A point with W=0 needs div W=0. These are necessary conditions, not sufficient global existence or uniqueness criteria. A finite three-dimensional current can circulate; one-dimensional zero-flux reasoning must not be applied to every three-dimensional field.

The previously constructed controller current depends on the inverse material Jacobian and adds clock-variation terms when ∂Λ≠0. It vanishes in that variation on the constant-Λ stationary target. The boxed pure-core equation alone is not the complete powered-controller equation.

## 3. The geometric stationary current is explicit

On the assigned stationary target γ=I,N=1,β=b ez, source matching specifies

\[
F_B=-j,\quad F_C=(F_0I-S)/2,\quad B=-b e_z,\quad F_0=bj_z-\rho.
\]

Hence

\[
W_i=-j_i+bS_{iz}-bF_0\delta_{iz}.
\]

Transforming the normal-frame stress into coordinates gives exactly W^i=T^i{}_0. With the usual sign convention the Killing-energy current associated with ∂t is −Tμ{}_0, so W is the **negative** of its spatial part. This is not a material velocity. It also depends on the chosen stationary time generator; it is not a frame-independent fuel inventory.

For the target metric

\[
ds^2=-dt^2+dx^2+dy^2+[dz+b(x,y,z)dt]^2,
\]

the earlier frozen exact Ricci expression gives, on defining Ψ=b+b³/3,

\[
\boxed{\mathbf W={M^2\over2}(\Psi_{xz},\Psi_{yz},-\Psi_{xx}-\Psi_{yy}).}
\]

Equivalently W=M² curl(Ψy,−Ψx,0)/2, so its divergence is identically zero. Both the constitutive-current calculation and an independent frame-to-coordinate stress conversion produce this result. It follows from the assigned geometry and Einstein stress; it does not show how a physical medium creates that stress.

For radial b(r), use cylindrical radius s and axial z. The meridional streamfunction is

\[
\chi(s,z)=-{M^2\over2}s\Psi_s,\qquad
W_s=-\chi_z/s,\quad W_z=\chi_s/s.
\]

A smooth wall with flat cabin and constant exterior has compact derivatives, so this current is confined to the transition. The [plot](plot_run_v1/calculation/clock_current.png) shows contours and normalized directions for one smooth radial profile, V=0.1. It is a stationary conserved stress-energy-current pattern, not particles moving in loops or a thrust calculation. Here gtt=−1+b²<0 everywhere; no Killing-horizon crossing or special intrinsic sphere curvature is involved in obtaining the current.

The geometry therefore determines a conserved current that the clock/material model must satisfy. It does not supply a cold-energy reservoir, a baryon-conversion reaction, or a launched payload. The next nonlinear task is the full constraint algorithm including the global positive-lapse problem and the phase boundary, followed by curved-mode stability.

## 4. Closed currents create a range condition and a lapse kernel

On the stationary target div W*=0 and N*=1. For a pure-core perturbation, write N=1+δN, W=W*+δW. The linearized consistency condition is

\[
2\mathbf W_*\cdot\nabla\delta N+\nabla\cdot\delta\mathbf W=0.
\]

Parameterize a regular closed current orbit by dx/ds=W*. Integrating around its period T gives the necessary condition

\[
\int_0^T\nabla\cdot\delta\mathbf W\,ds=0,
\]

or equivalently the integral of div δW divided by |W*| against arclength. Otherwise δN cannot return to its initial value on the same orbit. No assumption that every δW arises from an admissible canonical perturbation is made: this is a necessary test for those that do.

There is also a nontrivial homogeneous kernel. In the radial, axisymmetric case W*·∇χ=0. Therefore any smooth axisymmetric δN=F(χ) satisfies the homogeneous transport equation. Choose F with compact support in a band of regular negative χ levels; this δN vanishes outside the wall, so fixing N→1 at infinity does not remove it from the clock equation alone. It may later be fixed, constrained or identified with gauge by the rest of the Dirac algorithm; no physical classification of this kernel is asserted here.

For the monotone smooth radial profile used in the plot, χ vanishes in the cabin, exterior and symmetry axis and is negative within the wall away from the axis. Each regular nonzero level component is compact, has no boundary, and is a closed meridional curve. W* is nonzero and tangent on such a component. Thus the compatibility issue is present in this assigned geometry; it is not an invented orbit unrelated to the model.

This establishes why the stationary conserved current is useful but insufficient to prove a unique, stable powered evolution. The controller's extra clock variation must also be included before applying any analogous range condition to a launch.

## 5. The strong bracket identity also holds away from flat spatial metric in the diagonal sector

A separate [exact run](general_run_v1/calculation/results.json) retains arbitrary positive q1(z),q2(z),q3(z), rather than substituting q=1 after variation. In the same constant-h rest-source theory, it finds

\[
\{\mathcal C[n],\mathcal C[m]\}=\int(nm'-mn')[-W^z+s^z\mathcal C]dz,
\]

\[
s^z={P_z\over4h\sqrt\gamma},\qquad
W^z=-{P_z(3-1/q_3)\over2q_3}.
\]

This W is precisely the constitutive clock-current density: F_B=4hB, F_C=−hC, Bz=−Pz/(4h√γ). The explicit off-shell C term explains the extra C/(4h) factor in the flat family. On the full constraint surface the bracket coefficient is −W, so preservation agrees with the independent clock variation div(N²W)=0, including its sign.

The computation checks the possible third-smearing-derivative coefficient vanishes and reduces the remaining exact differential rational expression to zero. This proves the stated diagonal planar identity, not a general non-diagonal three-dimensional bracket or the full Dirac chain. It strengthens the connection between the nonlinear consistency condition and the clock current without assuming that lapse linearity makes the constraint first class.
