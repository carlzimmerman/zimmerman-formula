# PN28 transport: Fourier conduction and the required kinetic pressure response

The ordinary positive-conductivity route fails for the compact MC27 halos whose quarter-density core lies in the exact-log interval. Homologous compression requires outward heat flux, while Fourier conduction points inward near their centers. Expansion can match the local sign, but its required conductivity diverges at the temperature maximum and then changes sign. A finite conductivity cannot carry the required nonzero flux across that maximum.

The constructive result is an explicit cooling/heating obligation, including a central loss rate and an integrated power bound. It is an inverse requirement on a future reciprocal mechanism, not a derived mechanism or a selection of the pressure amplitude.

**Evidence label:** analytical proof, self-reviewed; nine finite numerical checks passed. The parent coordinator should independently check the central sign and power ledger before promoting the result. No external theorem or observational input is load-bearing.

## Target, conventions and scope

Requested base: `66c45c5082f651dd54e171f98c11acd9cb3d9086`. The shared tree advanced during the task; `INPUT_PROVENANCE.json` records observed revisions and actual input hashes. This route writes only `pressure_selection_2026_10_28/transport/`.

Let the mass density be \(\rho\), bulk velocity \(u\), isotropic kinetic stress \(\Pi=pI\), and random kinetic heat flux \(q\). Put \(D=\partial_t+u\cdot\nabla\), \(\theta=\nabla\cdot u\), and let \(Q\) be a volumetric source of random kinetic energy, positive for heating. The central-moment trace is

\[
\frac32Dp+\frac52p\theta+\nabla\cdot q=Q,
\qquad D\rho=-\rho\theta.
\tag{1}
\]

An exact material pressure closure \(p=P(\rho)\), with its parameters fixed, therefore requires

\[
Q-\nabla\cdot q=\frac12 C(\rho)\theta,
\qquad C=5p-3\rho P'(\rho).
\tag{2}
\]

Inside the MC27 exact-log region,

\[
p=A\ln(\rho/\rho_{\rm ref}),\quad C=5p-3A,
\quad T:=p/\rho.
\tag{3}
\]

Here \(T\) is the kinetic temperature proxy with units of velocity squared; a positive physical temperature conversion can be absorbed into the conductivity. We test the local instantaneous constitutive law

\[
q=-\kappa\nabla T,\qquad \kappa\geq0,
\tag{4}
\]

with finite regular scalar \(\kappa\). The density and pressure at the tested instant are those of a regular spherical hydrostatic equilibrium, and its bulk flow is prescribed as a small homologous compression or expansion, \(u=Hr\), \(\theta=3H\). The equilibrium profile is used to calculate its temperature gradient; the moving state is not claimed to remain hydrostatic. This is a necessary instantaneous compatibility test, not a time-dependent solution.

Only isotropy of the second moment is used in (1). The exact isotropic equilibrium distribution itself has zero third moment. A positive Fourier law on its nonuniform temperature would already alter that equilibrium unless another source balances it. Allowing a nonzero third moment while keeping the same density and isotropic second moment is a more permissive test of the proposed transport repair.

## Route A: the exact required radial flux

For \(Q=0\), spherical symmetry and regularity at the origin give a unique flux:

\[
q_{\rm req}(r)=-\frac{1}{2r^2}
\int_0^r C(s)\theta(s)s^2\,ds.
\tag{5}
\]

There is no free integration constant: adding a term proportional to \(r^{-2}\) introduces a central point source or sink, outside the regular finite-halo assumptions. For uniform \(\theta\), define \(\bar p(r)=3r^{-3}\int_0^r p(s)s^2ds\). Then throughout the log region,

\[
q_{\rm req}(r)=-\frac{\theta r}{6}[5\bar p(r)-3A].
\tag{6}
\]

MC27 uses \(x=(\Phi-\Phi_*)/\Delta_m\), \(\rho_m=A/\Delta_m\), and its inner pressure is

\[
\rho=\rho_m/x,\qquad p/A=-\ln x+2/3,\qquad0<x\leq1.
\tag{7}
\]

Thus \(p\geq2A/3>3A/5\), so \(C>0\) everywhere in that inner region. Homologous compression requires \(q_{\rm req}>0\), outward; expansion requires \(q_{\rm req}<0\), inward.

Hydrostatic balance \(p'=-\rho g\), with \(g=GM(r)/r^2>0\), gives the exact temperature-gradient identity

\[
T'=\frac{A-p}{\rho^2}\rho'
   =\left(\frac pA-1\right)g.
\tag{8}
\]

Hence where \(p>A\), temperature rises outward and Fourier conduction with \(\kappa\geq0\) points inward. This has the opposite sign to (6) under compression, including \(\kappa=0\), which supplies no required flux.

For a regular self-gravitating center,

\[
g=\frac{4\pi G\rho_c}{3}r+O(r^3),\quad
T'=\left(\frac{p_c}{A}-1\right)\frac{4\pi G\rho_c}{3}r+O(r^3),
\]
\[
q_{\rm req}=-\frac{(5p_c-3A)\theta_c}{6}r+O(r^3).
\tag{9}
\]

Consequently the central conductivity required by the trace equation is

\[
\kappa_{{\rm req},c}
=\frac{(5p_c-3A)\theta_c}
{8\pi G\rho_c(p_c/A-1)}.
\tag{10}
\]

For \(p_c>A\), it is negative under compression. Every MC27 member with \(x_c\leq1/4\), the condition placing its quarter-density core inside the exact-log region, has
\(p_c/A\geq\ln4+2/3>1\). The obstruction therefore applies to all those members, not just the numerical examples.

It is not a theorem about every shallow log core. If \(3A/5<p_c<A\), a compressing center has the Fourier-compatible sign. The explicit \(x_c=0.8\) numerical control verifies that this regime is not falsely excluded. At \(p_c=A\), the leading temperature gradient vanishes and the next term is cubic in radius, while the required flux is linear for nonzero \(\theta_c\); finite conductivity again fails there.

## Route B: expansion, the temperature maximum and general divergence

In MC27's inner region,

\[
T=\Delta_m x(-\ln x+2/3),\qquad
\frac{dT}{dx}=\Delta_m(-\ln x-1/3).
\tag{11}
\]

The temperature has its unique maximum at
\(x_T=e^{-1/3}=0.7165313106\ldots\). For every quarter-core-contained member, \(x_c<x_T<1\), so the maximum occurs at a finite interior radius \(r_T\). It is a true nondegenerate maximum because

\[
T''(r_T)=-\Delta_m[x'(r_T)]^2/x_T<0.
\tag{12}
\]

For homogeneous expansion, (10) permits positive conductivity at the center. Nevertheless, (5) requires \(q_{\rm req}(r_T)<0\), while any finite \(\kappa\) gives \(q(r_T)=-\kappa T'(r_T)=0\). Equivalently, \(\kappa_{\rm req}=-q_{\rm req}/T'\) has a positive pole approaching \(r_T\) from inside and becomes negative outside. Compression has the opposite sign pattern, already failing in the inner region. A singular \(\kappa\) is not an ordinary finite conductivity and does not restore a positive sign on both sides.

This gives a compact integral proof covering both signs of nonzero homogeneous \(\theta\): equation (5) is nonzero at \(r_T\), whereas equation (4) is zero there. No adjustment of positive finite \(\kappa(r)\), even one depending on local state or flow, repairs this incompatibility while retaining these instantaneous profiles.

For general spherical \(\theta(r)\), define

\[
J(r)=\int_0^r C(s)\theta(s)s^2ds.
\]

The exact necessary sign condition for nonnegative Fourier conductivity is

\[
\kappa_{\rm req}(r)=\frac{J(r)}{2r^2T'(r)}\geq0.
\tag{13}
\]

Where \(T'>0\), this requires \(J\geq0\). Any nonzero purely compressing region from the center violates it. At every temperature extremum, finite conductivity further requires \(J=0\). A mixed compression/expansion pattern could meet these integral conditions; that case is not excluded. The inverse relation

\[
\theta(r)=\frac{2\nabla\cdot(\kappa\nabla T)}{C(r)}
\tag{14}
\]

shows what divergence would be required by a chosen conductivity in the no-source model. Near a center with \(p_c>A\) and \(\kappa_c>0\), it requires expansion, not compression. This is a compatibility condition only; it does not solve the momentum equation or establish invariant pressure closure.

## Route C: the minimum missing cooling and heating

Allow a direct reciprocal random-energy exchange \(Q\). Equation (2) fixes

\[
Q_{\rm req}(r)=\frac12C(r)\theta(r)+\nabla\cdot q.
\tag{15}
\]

With transport set to zero, this gives the simplest exact instantaneous target profile

\[
Q_0(r)=\frac12[5p(r)-3A]\theta
\tag{16}
\]

inside the log region: cooling for compression and heating for expansion. This is a derived requirement, not a proposed thermostat. A physical parent would have to produce it with an equal and opposite energy ledger and the required stress evolution.

For smooth positive conductivity at a self-gravitating center with \(p_c>A\) and \(\theta_c<0\), the required cooling is

\[
-Q_c=\frac12(5p_c-3A)|\theta_c|
 +4\pi G\kappa_c\rho_c(p_c/A-1)
\geq\frac12(5p_c-3A)|\theta_c|.
\tag{17}
\]

Ordinary conduction adds heat to this cold center and therefore increases the required central energy loss. For a homologous compression define the cooling power inside radius \(r\) by \(L_Q(r)=-4\pi\int_0^rQ(s)s^2ds\). The exact integrated ledger is

\[
L_Q(r)=2\pi|\theta|\int_0^rC(s)s^2ds
       +4\pi r^2\kappa(r)T'(r).
\tag{18}
\]

Throughout \(0<r\leq r_T\), the second term is nonnegative, giving a rigorous integrated lower bound. It is not a pointwise lower bound away from the center for arbitrarily varying \(\kappa(r)\). At \(r_T\), the second term vanishes: the net cooling inside the temperature maximum is fixed independent of the conductivity. For expansion, the corresponding integrated source at \(r_T\) is positive and fixed, so net heating is unavoidable there as well.

For zero transport the central random energy \(3p_c/2\) divided by its required loss is

\[
t_{Q,c}=\frac{3p_c}{(5p_c-3A)|\theta|}.
\tag{19}
\]

This is an instantaneous energy/loss timescale, not an evolved cooling time. For the four tested quarter-core-contained members, \(t_{Q,c}|\theta|\) ranges from 0.701 to 0.847. The necessary exchange is therefore of the same order as the compression rate; arbitrarily weak conduction cannot substitute for it.

## What the finite exterior changes, and what it does not

The actual MC27 exterior is

\[
\rho=\rho_m(3-x)^2/4,\quad p=A(3-x)^3/12,
\quad T=\Delta_m(3-x)/3,\quad1\leq x\leq3.
\tag{20}
\]

It leaves the inner temperature minimum and maximum unchanged. It provides decreasing temperature beyond the matching radius and a finite vacuum edge. Thus the central sign argument and the interior extremum contradiction are independent of a boundary condition at that edge.

An additional, explicitly stronger hypothesis is to promote the *entire constructed equilibrium curve* to a fixed material EOS, including its exterior \(p\propto\rho^{3/2}\). Then

\[
C_{\rm full}=
\begin{cases}5p-3A,&x\leq1,\\p/2,&1\leq x\leq3,\end{cases}
\tag{21}
\]

which is continuous and strictly positive wherever the halo has matter. Formula (5) then requires a nonzero flux through its vacuum edge for either sign of nonzero homogeneous \(\theta\). If that edge is an isolated regular kinetic boundary with \(q(R)=0\), no-source transport of any kind can meet the global energy requirement under these extra fixed-EOS and homology assumptions. Indeed, the compact reference distribution has bounded relative speeds tending to zero at its edge, and \(|q|\leq(3p/2)v_{\max}\to0\). Allowing escaping populations or an external heat bath changes this boundary premise.

With zero boundary flux the net loss under compression is exactly

\[
L_{Q,\rm full}=\frac{|\theta|}{2}\int C_{\rm full}\,dV.
\tag{22}
\]

Since \(p/2\leq C_{\rm full}<5p\) and \(K=(3/2)\int p\,dV\),

\[
\frac{|\theta|}{6}K\leq L_{Q,\rm full}
 <\frac{5|\theta|}{3}K.
\tag{23}
\]

This is a conditional global exchange obligation, not a universal prohibition on nonlocal or anisotropic kinetic mechanisms. Such mechanisms can change the stress–strain term, flow geometry, time dependence, pressure relation or boundary population. The full exterior need not obey its equilibrium curve during formation. None of those alternatives is refuted by this calculation.

## Bounded computation and reproducibility

`check_transport.py` solves the dimensionless Poisson profile in units \(A=\Delta_m=4\pi G=1\), with
\(\ell=\Delta_m/\sqrt{4\pi GA}\), then integrates \(J_C=\int C_{\rm full}r^2dr\). It compares that integral with a separate adaptive quadrature, checks the conductivity signs on both sides of the temperature maximum, tests its analytic pole coefficient, and tightens the solver on three cases. It performs no time evolution.

| \(x_c\) | \(p_c/A\) | \(r_T/\ell\) | \(r_{1/4}/\ell\) | \((5p_c-3A)/(2A)\) | \(L_{Q,\rm full}/(4\pi A\ell^3|\theta|)\) |
|---:|---:|---:|---:|---:|---:|
| 0.03 | 4.1732 | 1.0131 | 0.1753 | 8.9331 | 1.4936 |
| 0.10 | 2.9693 | 1.0315 | 0.5845 | 5.9231 | 1.5352 |
| 0.20 | 2.2761 | 1.0478 | 1.1690 | 4.1903 | 1.5666 |
| 0.249 | 2.0570 | 1.0436 | 1.4553 | 3.6424 | 1.5537 |
| 0.50 | 1.3598 | 0.8565 | 2.3312 | 1.8995 | 1.2552 |
| 0.80 | 0.8898 | none | 2.7830 | 0.7245 | 0.7876 |

The final row is an intentional shallow-center control; its listed central coefficient is the **zero-transport** loss, not a conductivity-independent lower bound. In the saved JSON the field `center_min_loss_over_A_absTheta` has that latter interpretation only when \(p_c>A\). This qualification prevents extending (17) outside its hypotheses. The \(x_c=0.2,0.249\) quarter radii lie beyond \(r_T\); for them (18)'s nonnegative-conduction bound is applied only up to \(r_T\), not over the entire quarter-density core.

The run passed 9/9 checks. Maximum independent-quadrature disagreement was \(1.03\times10^{-8}\); maximum relative change under tighter tolerances was \(1.03\times10^{-8}\). These finite checks validate the implemented examples, not the universal analytic signs. Exact execution information, before/after input hashes, software versions, caps and result hashes are in `run/manifest.json`; status is `completed`.

From the repository root, use the same `contract.json` and a fresh output directory with the installed mathbox bounded runner. The recorded argv is available in the manifest. Direct script usage is `python3 pressure_selection_2026_10_28/transport/check_transport.py NEW_RESULT_PATH`; its sole write is that result path. Source results must not be overwritten.

## Route disposition and continuation

- **Positive local Fourier conduction, no direct exchange, homologous MC27 quarter-core halo:** refuted as an exact instantaneous closure repair by (8)–(13).
- **Locally compatible expansion:** pursued through the thermal maximum; it fails globally within the exact-log interval for finite nonnegative conductivity.
- **Reciprocal volumetric exchange:** remains open, with explicit required profile, central rate and integrated power given by (15)–(23). Selecting these formulas by hand is not physical derivation.
- **Mixed flow, nonlocal transport, anisotropic stress, changing exterior or escaping populations:** not excluded. A future route must specify its evolution law and check both the energy trace and traceless stress equations. None is counted here as completed or exhausted.

The pressure amplitude \(A\), matching scale \(\Delta_m\) and central state remain free. This transport result does not select them or close the theory. It does provide a more restrictive target: a successful parent must supply central cooling during compression despite the inward Fourier flux, and, under the fixed full-EOS isolated-halo premise, a nonzero net reciprocal energy exchange.
