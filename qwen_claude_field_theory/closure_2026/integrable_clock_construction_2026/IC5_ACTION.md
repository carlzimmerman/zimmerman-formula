# IC-5: nonlinear auxiliary-square completion

Base: `6708f1e3e695a99f3fc3f121e14528f68ace641c`, 2026-09-08.
**New explicit action/Hamiltonian; full theory OPEN.** This is not IC-4 under
a change of name. Its cubic and higher interactions change. Its static and
flat isotropic homogeneous restrictions, and its quadratic action at the
specified expanding witness, are connected to IC-4 by the calculations below.
No global novelty claim or empirical fit is made.

## Definitions and parameters

Use exactly the fields, signature, physical metric, clock, $U$, $w$, $Q_{\mu\nu}$,
$\widehat R$, $J$, and $F$ defined in [IC4_ACTION.md](IC4_ACTION.md). In particular
$\xi=\ln N$, $w=(u-1)\xi$, $0<u<1$, $X>0$, and ordinary matter has the single
unchanged action $S_m[g,\psi]$. Keep every IC-4 coefficient, including
$\sigma=1/3$ and its fixed expanding-witness parameter values. Put

\[
b=-\frac{\mathcal T}{9}-\frac38,\qquad h_0=\sqrt{\kappa/(6m)}.
\]

Let $P^{\mu\nu}$ be a symmetric tensor tangent to the clock leaves, with
**six independent leaf components**. Equivalently parameterize those six
components in a leaf frame; do not introduce ten unconstrained components.
Set $p=h_{\mu\nu}P^{\mu\nu}$ and
$P_{\rm TF}^{\mu\nu}=P^{\mu\nu}-p h^{\mu\nu}/3$.
This tensor is the first-order metric momentum, not another matter species.

Define a smooth, momentum-reversal-even activation by

\[
E(t)=\begin{cases}\exp(-1/t),&t>0,\\0,&t\le0,\end{cases}\quad
d(r)=(r^2-1)^2,\quad
\eta(r)=\frac{E(1/4-d(r))}{E(1/4-d(r))+E(d(r)-1/16)},
\qquad r=-\frac{Np}{3mh_0}.
\]

The denominator never vanishes. Thus $\eta=1$ for $|r^2-1|\le1/4$, and
$\eta=0$ for $|r^2-1|\ge1/2$. There is a static plateau near $p=0$ and an
expanding plateau near $r=1$. This is a specified design choice, not an
observationally derived switch. No health claim covers its transition yet.

## Complete covariant phase-space action

All contractions below use the physical leaf metric. Write
$C=\Lambda+a_0^2U(u^2)$. Define

\[
\begin{aligned}
\mathscr H_5={}&\frac2m(P_{\rm TF}^{\mu\nu}P^{\rm TF}_{\mu\nu}-p^2/6)
+mC-\kappa X-\frac m2\widehat R-\frac{p^2F\widehat R}{2ma_0^2}\\
&-(1-\eta)\left\{m[2u\xi\,a\cdot Du+\xi^2(Du)^2]
+\frac{p^2J}{2ma_0^2}\right\}
-\eta m\alpha\,|D(\xi+bu)|^2,
\end{aligned}
\]
\[
\boxed{S_5=\int d^4x\sqrt{-g}\,[2P^{\mu\nu}Q_{\mu\nu}-\mathscr H_5]
+S_m[g,\psi].}
\]

The clock is a varied field; unitary coordinates $T=t$ are chosen only after
defining the action. No derivative of $P^{\mu\nu}$ occurs. All quantities
are tensor/scalar constructions from the physical metric, the timelike clock,
$u$, and the six leaf components of $P$. This gives an explicit covariant
first-order action, not merely a prescription to restore covariance later.
Its complete metric/clock variation has not been expanded in this package.

## Exact canonical map

Set $V=\sqrt{\bar h}$, $\bar h=e^{-2w}h$,
$\bar\pi^{ij}=Ve^{5w}P^{ij}$ and $\pi=\bar h_{ij}\bar\pi^{ij}$.
Then $p=e^{-3w}\pi/V$. The exact symplectic density is

\[
2N\sqrt h\,P^{ij}Q_{ij}
=\bar\pi^{ij}(\dot{\bar h}_{ij}-\mathcal L_{\boldsymbol\beta}\bar h_{ij}).
\]

It contains no $\dot\xi$ or $\dot u$. Multiplying $\mathscr H_5$ by
$N\sqrt h=NVe^{3w}$ gives the following same Hamiltonian. Barred gradients
and curvature are used throughout this display:

\[
\begin{aligned}
\mathcal H_b={}&\frac{2e^{(4-3u)\xi}}{mV}(\pi_{\rm TF}^2-\pi^2/6)
-\frac m2Ve^{u\xi}\bar R+mVe^{(3u-2)\xi}C
-\frac\kappa2Ve^{(3u-4)\xi},\\
\mathcal D={}&-\frac{e^{(6-5u)\xi}\pi^2}{2mVa_0^2},\\
\mathcal G={}&-mVe^{u\xi}[2u\xi\bar D\xi\cdot\bar Du+\xi^2|\bar Du|^2]
+\mathcal D\bar J,\\
\mathcal S={}&-mVe^{u\xi}\alpha|\bar D(\xi+bu)|^2,\\
\boxed{\mathcal H_5={}&\mathcal H_b+\mathcal D F\bar R+(1-\eta)\mathcal G+\eta\mathcal S.}
\end{aligned}
\]

Here $\bar J=3[\alpha|\bar D\xi|^2+\beta\bar D\xi\cdot\bar Du+
\gamma|\bar Du|^2]/(4\ell^2)$ and
$r=-\pi e^{(4-3u)\xi}/(3mVh_0)$.
The standard spatial shift generator and the minimally coupled matter
Hamiltonian must be added; neither is discarded by this notation.

## Momentum variation and the plateau Lagrangian

On $\eta=1$, put $K_R=1+3F\widehat R/(2a_0^2)$. Actual variation of the
phase action with respect to the trace-free and trace momenta gives

\[
P_{\rm TF}^{\mu\nu}=\frac m2 Q_{\rm TF}^{\mu\nu},\qquad
p=-\frac{mQ}{K_R}.
\]

For $K_R\ne0$, substituting these stationary values yields

\[
\boxed{\mathscr L_{5,\eta=1}=
\frac m2\left[Q_{\rm TF}^2-\frac{2Q^2}{3K_R}
+\widehat R-2C+2\alpha|D(\xi+bu)|^2\right]+\kappa X.}
\]

This formula applies only when the eliminated momentum satisfies the plateau
condition. Outside it the full phase action, including derivatives of $\eta$
in its momentum equation, defines the candidate. A global regular Legendre
inverse across that transition has not been established.

## Proved comparisons and their limits

1. **Static:** at $\bar\pi^{ij}=0$, $\eta=0$ on a neighborhood and every
   first jet of the difference from the IC-4 Hamiltonian vanishes. The static
   IC-1 action agrees modulo its declared spatial divergence, with compactly
   supported or periodic variations, sufficient decay, or a boundary
   prescription annulling that divergence's variation. Fixed boundary values
   alone do not automatically fix its normal derivatives. Consequently the
   independently varied static equations, including the regular constitutive
   law $u^2=1-\exp(-|a|/a_0)$, transfer. The clock-source, vacuum-source and
   galactic-boundary matching obligations do not disappear.
2. **Flat isotropic homogeneous evolution:** all gradients, $\bar R$ and
   $\pi_{\rm TF}$ vanish, leaving the full previously varied homogeneous
   Hamiltonian. The exact expanding solution with $r=1$ and the separate
   genuine uniform-mode calculation transfer. This is not realistic cosmology.
3. **Quadratic witness:** at $(\xi,u)=(1/4,2/3)$,
   $\mathcal G^{(2)}=\mathcal S^{(2)}$. The exact IC-4 reciprocal trace
   factor and its linearized Hamiltonian differ by a computed $O(Z^2)$
   remainder, where $Z=e^{-2w}(\bar J+F\bar R)/a_0^2=O(\epsilon^2)$.
   Hence $H_5-H_4=O(\epsilon^3)$ for general perturbations of this witness.
   The existing scalar wave, tensor quadratic action and quadratic constraint
   analysis transfer through the same regular canonical map—not by assigning
   their results to an unrelated action.
4. **Ordinary matter Ward identity:** the covariant $S_m[g,\psi]$ is unchanged.
   Its independent infinitesimal diffeomorphism variation gives
   $\nabla_\mu T_m^{\mu\nu}=0$ on the ordinary-matter equations. This is a
   statement about that matter action, not separate conservation of the
   interacting clock's bare $\kappa X$ stress.

The [nonlinear auxiliary report](NONLINEAR_SQUARE_REPORT.md) states the actual
algebraic/elliptic equations, function spaces, coercivity bound and remaining
preservation gap. No auxiliary sign or existence statement is used to infer
full physical stability, all-background luminal tensors, PPN, zero-field
regularity or a finished theory.
