# Radial stability without a finite susceptibility assumption

18 October 2026. Claim ZAR-W2. The equilibrium is the exact warm construction in [EXACT_WARM_DF.md](EXACT_WARM_DF.md), in the same hollow spherical effective model. Stability here means linear Lyapunov stability for dynamically accessible spherical radial perturbations in the defined energy completion. It does not assert nonlinear, nonspherical or classical L1 stability at the possible circular ridge.

## Model coefficients and perturbations

Let v denote radial velocity and L squared specific angular momentum. For species i define

\[
D_i=v\partial_r+(L/r^3+a_i)\partial_v,\qquad
d\Gamma=C\,dr\,dv\,dL,\quad C=4\pi^2,
\quad \mu_i=M_i'.
\]

The field potential Hessian for enclosed mass perturbations m_i is

\[
H(r)=\begin{pmatrix}
2G^2M_t/(a_0r^4)&-G/r^2\\-G/r^2&-G/r^2
\end{pmatrix},\qquad \delta a=Hm,\quad\delta\Phi_i'=-\delta a_i.
\]

Write B_i = -a_i'-3a_i/r for the frozen-background epicyclic coefficient, and

\[
\kappa_t^2=G(M_b+M_f)/r^3+G^2M_t^2/(a_0r^5),\qquad
\kappa_f^2=G(M_b+M_t+M_f)/r^3.
\]

The target's strict core condition gives uniform constants

\[
0<\beta\leq B_i\leq K<\infty,\qquad
\kappa_i^2\geq b=GM_b/R^3>0.
\]

For its countable packets put w_in = -partial_E F_in >= 0. On a dense core take one common smooth radial canonical generator g_i for all packets of physical species i, preserving L, and

\[
h_{in}=\{g_i,F_{in}\}=-w_{in}D_i g_i,\qquad
\mathcal A=\sum_{i,n}\int h_{in}^2/w_{in}\,d\Gamma.
\]

Zero-weight ratios are omitted. The packet labels are a representation of one physical species; they do not receive independent force laws or source masses. On this core A equals sum_i int(-F_i,E)(D_i g_i)^2 dGamma wherever that aggregate expression is defined.

## The exact warm identity

Split g_i into parts even and odd in v. Only its odd part produces a density perturbation. For odd g write g = r v u with smooth even u. Direct differentiation gives

\[
D_i(rv)=v^2+L/r^2+ra_i,\qquad
D_i^2(rv)=v(3a_i+ra_i')=-B_i rv.
\]

Since D_i w_in = 0, integration by parts packet by packet yields

\[
\int w_{in}(D_i g)^2d\Gamma
=\int w_{in}\left[r^2v^2(D_i u)^2+B_i g^2\right]d\Gamma.
\]

Define the nonnegative quantities

\[
\begin{aligned}
J_i(r)&=C\sum_n\int w_{in}g_{i,\rm odd}^2\,dv\,dL,\\
T_i(r)&=C\sum_n\int w_{in}r^2v^2
\left[D_i\left(\frac{g_{i,\rm odd}}{rv}\right)\right]^2dv\,dL.
\end{aligned}
\]

Thus A_odd = sum_i int(T_i+B_i J_i)dr. There is no division singularity at v = 0 for smooth odd generators.

The enclosed mass perturbation and moment identity are

\[
m_i=-C\sum_n\int w_{in}v g_{i,\rm odd}\,dv\,dL,\qquad
C\sum_n\int w_{in}v^2\,dv\,dL=\mu_i.
\]

The latter follows from integration by parts in v and Tonelli. Therefore m_i^2 <= mu_i J_i. Put z_i = m_i^2/mu_i on Omega; set m_i = j_i = z_i = 0 where mu_i = 0. For completed perturbations this is a support convention, with no boundary trace or pointwise limit required.

Differentiating the actual forces gives

\[
B_t=\kappa_t^2+G\mu_f/r^2-2G^2M_t\mu_t/(a_0r^4),\qquad
B_f=\kappa_f^2+G(\mu_t+\mu_f)/r^2.
\]

Add the exact field Hessian to A. Its self-density terms cancel against these B_i terms, yielding

\[
\boxed{\begin{aligned}
Q={}&\mathcal A_{\rm even}
+\sum_i\int[T_i+B_i(J_i-z_i)+\kappa_i^2z_i]dr\\
&+\int\frac{G\mu_t\mu_f}{r^2}
\left(\frac{m_t}{\mu_t}-\frac{m_f}{\mu_f}\right)^2dr.
\end{aligned}}
\]

Here Q = A + int m^T H m dr. The generator-even sector has velocity-odd perturbation and zero field term, so its contribution is exactly A_even. Comparing the nonnegative terms with A_odd gives the coercive estimate

\[
Q\geq c\mathcal A,\qquad c=\min(1,b/K)>0.
\]

This is an identity for warm radial phase-space perturbations. It does not infer stability from continuity of circular-shell frequencies or assume a finite susceptibility.

## The ridge and the energy completion

For smooth generators on the compact hollow support, the packetwise right-hand integrands are bounded by constants times w_in v^2: g_odd = r v u, and D_i u is bounded. In the generator-even sector, partial_v g_even is v times a smooth bounded function, so D_i g_even is also v times a bounded function. Their sum is integrable by the moment identity. Thus the accessible quadratic remains finite even when int(-F_E)dv diverges. Packetwise integration by parts followed by Tonelli proves the identity for the constructed sum.

Define the Hilbert space H_DA as the closure of the common-generator core in the direct-sum norm A. A convenient initial core is localized by smooth invariant cutoffs in E_i and L, away from E_i = E_ci(L); only finitely many packets then contribute. Removing these cutoffs is dense in A because D_i of an invariant cutoff is zero and the preceding total energy is finite. The original equilibrium can be L1 even though its aggregate accessible tangent is a distribution, rather than an L1 function.

The mass map is bounded before using Q: from B_i >= beta,

\[
\sum_i\int m_i^2/\mu_i\,dr\leq\sum_i\int J_i\,dr
\leq\mathcal A/\beta.
\]

It therefore extends uniquely to H_DA. Let

\[
Y=\bigoplus_i L^2(\Omega,dr/\mu_i).
\]

Thus the mass map takes H_DA continuously into Y. Define

\[
C_H=\sup_r\left\|
\operatorname{diag}(\sqrt{\mu_i})H
\operatorname{diag}(\sqrt{\mu_i})\right\|_{\rm op}<\infty.
\]

Hollow finite support and smooth masses make this finite. Consequently

\[
c\mathcal A\leq Q\leq(1+C_H/\beta)\mathcal A.
\]

The estimates extend Q and its coercivity to the completed space. This is a specified energy topology; it must not be presented as an ordinary L1 perturbation estimate.

## Linear flow and conservation

Only occupied characteristics are needed. They remain in the compact hollow orbital region, where the equilibrium Hamiltonian flow is smooth and complete. Free transport is a strongly continuous unitary group in the packet norm, preserves common generators, and preserves H_DA. This does not assume completeness for arbitrary ambient trajectories into the point singularity.

The self-consistent field source is

\[
(\mathcal B h)_{in}=w_{in}v\,\delta a_i[m].
\]

Its norm satisfies

\[
\|\mathcal B h\|_{\mathcal A}^2
=\sum_i\int\mu_i(\delta a_i)^2dr
\leq(C_H^2/\beta)\mathcal A[h].
\]

For the aggregate equation its distributional meaning is -partial_v(delta a_i F_i), which is well-defined: int |delta a_i| F_i dGamma = int mu_i |delta a_i| dr is finite by Cauchy-Schwarz and the displayed source bound. This avoids assuming a product between a general distribution partial_v F_i and a rough force.

It lies in H_DA: it is generated by the common radial potential delta Phi_i. Approximate that potential's force in L2(mu_i dr) by smooth forces, then apply invariant energy and angular-momentum cutoffs; their transport derivatives vanish and the moment identity controls the norm limit. Thus the source is a bounded operator on this completed space, not an assumed classical multiplication by an integrable susceptibility.

The Duhamel series for free transport plus this bounded source converges on finite time intervals and gives a unique global linear energy-form flow. Define the shell current j_i = C sum_n int v h_in dv dL, first on the core. Its continuous extension is bounded by

\[
\sum_i\int j_i^2/\mu_i\,dr\leq\mathcal A.
\]

On the finite-packet localized core, free continuity gives m U(t)h - m h = -int_0^t j U(s)h ds. Boundedness of the mass and current maps extends this identity by density. The field source has zero density and hence m B h = 0. The mild equation therefore gives dot m = -j in the corresponding L2 spaces, without assuming a classical density derivative at the ridge.

The free unitary evolution contributes no norm change. More precisely, in the interaction picture U(-t)h(t), the bounded source makes the solution strongly differentiable; unitarity then gives the norm derivative below without assuming that h lies in the domain of the transport generator. The field work gives

\[
\tfrac12\frac{d\mathcal A}{dt}=\sum_i\int j_i\delta a_i dr,
\qquad
\tfrac12\frac d{dt}\int m^THm\,dr=-\sum_i\int j_i\delta a_i dr.
\]

Thus Q is conserved and

\[
\boxed{\mathcal A[h(t)]\leq
\frac{1+C_H/\beta}{c}\mathcal A[h(0)].}
\]

This proves radial linear Lyapunov stability in H_DA. The flow and estimate are defined even if the aggregate tangent requires a distributional interpretation.

That interpretation is continuous, rather than merely formal. For a smooth radial test function split by velocity parity, its odd part is bounded by a constant times |v|, so pairing it with the velocity-odd perturbation is controlled by A and the finite moment integral of sum_n w_in v^2. For the velocity-even perturbation integrate by parts packetwise to write its pairing as sum_n int w_in g_odd D_i(test_even) dGamma. Here D_i(test_even) is v times a bounded function; Cauchy-Schwarz, J_i and the same moment identity bound the pairing by a constant times sqrt(A). Apply these estimates to any finite set of packet labels; the tails tend to zero by the direct-sum norm. The aggregate distribution therefore extends continuously from the core to H_DA and satisfies the linearized equation distributionally. Its mass and current are the bounded maps already defined.

A classical differentiable Vlasov flow in L1 at the circular ridge, nonlinear orbital stability and nonspherical stability are not established by this theorem.
