# IC-4: one explicit clock–curvature action

Base checkpoint: `0a9f9fa33be9d4ace0e1496cef9ff19f48215017`, 2026-09-08.
**OPEN theory; constructive linear-background result, not full closure.**

This is a new action revision. It does not inherit IC-2's scalar stability
results: its corrected scalar equations are rederived. The unchanged
constitutive function, matter action, and homogeneous reduction are explicitly
identified below. No empirical fit or global novelty claim is made.

## Fields and the complete action

Use signature $(-+++)$ and $c=1$, with $m>0$, $\kappa>0$, $a_0>0$.
The varied fields are one physical metric $g_{\mu\nu}$, a timelike clock $T$,
an independent auxiliary $u$ on the regular branch $0<u<1$, and ordinary
matter $\psi$. Define

\[
X=-\tfrac12 g^{\mu\nu}\partial_\mu T\partial_\nu T>0,\quad
N=(2X)^{-1/2},\quad n_\mu=-\partial_\mu T/\sqrt{2X},\quad
h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu.
\]

$D$ is the intrinsic physical-leaf derivative,
$a_\mu=D_\mu\ln N$, $K_{\mu\nu}=h_\mu{}^\rho\nabla_\rho n_\nu$,
$K=h^{\mu\nu}K_{\mu\nu}$. Set

\[
U(c)=(1-c)[\ln^2(1-c)-2\ln(1-c)+2]-2,
\quad w=(u-1)\ln N,\quad W=n^\mu\nabla_\mu w,
\]
\[
Q_{\mu\nu}=K_{\mu\nu}-h_{\mu\nu}W,\quad Q=K-3W,
\quad \bar h_{ij}=e^{-2w}h_{ij},\quad
\widehat R=e^{-2w}R^{(3)}[\bar h].
\]

The barred metric is a change of variables on the clock slices, **not** a
second metric for matter or light. Equivalently
$\widehat R=R^{(3)}[h]+4\Delta_h w-2|D w|_h^2$.

The full action is

\[
\boxed{S_4=\int d^4x\sqrt{-g}\left\{
\frac m2\left[R^{(4)}-2\Lambda+4KW-6W^2
+2(1-u^2)a_\mu a^\mu-2a_0^2U(u^2)
+\frac{Q^2}{a_0^2}(J+\widehat R F)\right]+\kappa X\right\}
+S_m[g,\psi].}
\]

Here

\[
J=\frac{3}{4\ell^2}
  [\alpha a^2+\beta a\mathbin{\cdot}Du+\gamma(Du)^2],\qquad
F=A_R(\ln N-1/4)+B_R(u-2/3),
\]
\[
\ell=\ln(9/5),\quad \mathcal T=-\frac{27}{16}+\frac{54}{5\ell},
\quad e=\frac18,\quad d=-\frac{9e}{\mathcal T},\quad
\alpha=\frac{81e}{\mathcal T^2},
\]
\[
\beta=2d-\frac13-\frac{3\alpha}{4},\qquad
\gamma=e-\frac1{16}+\frac{9\alpha}{64}-\frac{3d}{4}.
\]

Define $a_*=3-81/(4\mathcal T)>0$ and select the **fixed design parameter**
$\sigma=1/3$. More generally the calculation covers $0<\sigma\le1$.

\[
p_R=\frac83+4a_*\sigma,\qquad q_R=-1-\frac{3p_R}{8},\qquad
A_R=\frac{3p_R}{16\ell^2},\quad B_R=\frac{3q_R}{16\ell^2}.
\]

These coefficients are fixed before any sector is tested. The squared-speed
parameter $\sigma$ is a construction choice, not a prediction fitted to data.
The computation
solves the compatibility conditions for these coefficients and then varies
the resulting action; it does not substitute a desired wave equation as input.

## Nonempty expanding witness

The same parameters as the explicitly varied IC-1 homogeneous construction give

\[
u_0=2/3,\quad N_0=e^{1/4},\quad
a_0^2=\frac{9\kappa e^{-1/2}}{16m\ell^2},\quad
\Lambda=\frac{\kappa e^{-1/2}}m-a_0^2U(4/9)>0,
\]
\[
B=B_0e^{ht},\quad h=\sqrt{\kappa/(6m)}>0,\quad
A=B e^{-1/12},\quad H_{\rm phys}=h/N_0.
\]

The symbol $A$ here denotes the physical scale factor, not $A_R$.
The clock is varied before choosing unitary coordinates $T=t$.
This is a tuned expanding solution, not a demonstrated realistic cosmology
or a derivation of the proposed observed $a_0$–$\Lambda$ relation.

## Which same-action bridges hold

- On an exactly stationary branch with $K=W=0$, $Q=0$. Both new terms and
  their complete first-variation coefficients vanish. The static equations
  of [IC-1](ACTION.md) are unchanged, including their clock-source caveat.
  This transfers the equations, not an unproved global galactic solution.
- On the displayed flat homogeneous witness, $a=Du=0$ and
  $\widehat R=F=0$. The correction and all first variations vanish. The
  entire flat homogeneous reduced action is unchanged and is varied
  independently for the exactly uniform mode.
- For a pure tensor perturbation of this witness, $N,u$ retain their
  background values, so $F=0$ identically and $J=0$. The positive, luminal
  tensor quadratic action transfers on this background only.
- In barred variables,
  $Q_{ij}=e^{2w}(\dot{\bar h}_{ij}-\mathcal L_{\boldsymbol N}\bar h_{ij})/(2N)$.
  The correction has no independent $\dot N$ or $\dot u$. Its spatial
  integration by parts is checked explicitly; no time integration by parts
  is invoked to discard an auxiliary velocity. This preserves IC-1's
  primary integrability mechanism, not a full nonlinear Dirac count.
- The independently diffeomorphism-invariant $S_m[g,\psi]$ is unchanged.
  Its own on-shell Ward identity remains $\nabla_\mu T_m^{\mu\nu}=0$.
  No extra force on ordinary matter is inserted.

The exact static regular branch still has
$u^2=1-\exp(-|a|/a_0)$. The local baryon-only MOND equation and no-slip
reduction still require control of the clock/vacuum terms and boundary
matching as stated in the original [report](REPORT.md). These conditions
have **not** been promoted to unconditional MOND or PPN passes.

## Verification boundary

[LOCAL_WAVE_REPORT.md](LOCAL_WAVE_REPORT.md) gives the actual scalar variation,
local physical clock equation, independently reconstructed readouts, energy
identity, compact packet construction, and separate zero mode. The programs
`curvature_operator_bridge.py` and `local_clock_wave.py` independently check the
critical operator-to-quadratic-action map.

No complete nonlinear metric/clock Euler–Lagrange system, functional constraint
closure, all-background stability theorem, realistic matter cosmology or PPN
solution is certified here. No field has been classified as harmless merely
because it is called a clock or auxiliary. Full theory remains **OPEN**.
