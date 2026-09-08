# IC-6: constructive tensor balance beyond the special FLRW witness

Base `6708f1e3e`, 2026-09-08. **New action revision; full theory OPEN.**

The tensor balance passes on general flat homogeneous isotropic backgrounds
of the new action, on the explicit positive-$J_T$ branch. The actual IC-6
auxiliary equations also admit the bounded finite-grid witness below. Neither
result is an all-background causality or nonlinear closure certificate.

## New Hamiltonian, not an inherited tensor pass

Use the physical metric, genuine clock, auxiliary field, potential, ordinary
matter action, and smooth activation of the frozen [IC-5 action](IC5_ACTION.md).
In its covariant phase formulation, $P^{\mu\nu}$ is tangent to the clock
leaves, $p=P^\mu{}_{\mu}$, and $P_{\rm TF}$ is its traceless part. The phase
density is

\[
\mathcal L_{\rm phase}
=2P_{\rm TF}:Q_{\rm TF}+\frac{2pQ}{3}-\mathcal H.
\]

IC-5 contains

\[
\mathcal H_5=\frac{2P_{\rm TF}^2}{m}-\frac{p^2}{3m}
-\frac m2\widehat R-\frac{p^2F}{2ma_0^2}\widehat R
+\text{the specified potential, clock, and auxiliary-gradient terms}.
\]

Define

\[
J_T=1+\frac{p^2F}{m^2a_0^2},\qquad
\boxed{\mathcal H_6=\mathcal H_5+
\frac{2P_{\rm TF}^2}{m}\left(\frac1{J_T}-1\right).}
\]

No other term, matter coupling, or activation is changed. This is an explicit
new Hamiltonian on the open branch $J_T>0$, not a statement about regular
extension through $J_T=0$. The fixed design member remains $\sigma=1/3$;
$F=A_R(\xi-1/4)+B_R(u-2/3)$ retains its IC-4 coefficients. The frozen
IC-5 implementation used by the numerical solver has SHA256
`4c9a79caa9a6d54a6a5f006440886f54b9092d68978249fb79f95a0f73229ece`.

On the $\eta=1$ plateau, all five traceless momentum components can also be
eliminated **nonlinearly**. Their actual Euler equations yield
$P_{\rm TF}=mJ_TQ_{\rm TF}/2$. Retaining the resulting $p$ dependence gives

\[
\mathcal L_{\rm after\ TF}
=\frac m2Y+\frac{2pQ}{3}+\frac{p^2}{3m}K_6
-mC+m\alpha|D\xi+bDu|^2+\kappa X,
\]
\[
Y=\widehat R+Q_{\rm TF}^2,\qquad
K_6=1+\frac{3FY}{2a_0^2},\qquad p=-\frac{mQ}{K_6},
\]
\[
\boxed{\mathcal L_6=\frac m2\left[
Y-\frac{2Q^2}{3K_6}-2C+2\alpha|D\xi+bDu|^2\right]+\kappa X.}
\]

Here $C=\Lambda+a_0^2U(u^2)$, and ordinary $\mathcal L_m$ is unchanged.
The program differentiates the five-component phase action, checks the
envelope-theorem identity for its remaining $p$ variation, and verifies
this compact expression exactly. Its equivalence requires the $\eta=1$
plateau, $J_T>0$, and $K_6\ne0$. It is not a claim of positive energy or
healthy characteristics for arbitrary fields.

## Actual tensor geometry and phase variation

Let $A(t)$ denote the **physical** scale factor, with arbitrary homogeneous
$N(t)>0$, $u(t)$ and $w(t)=(u-1)\ln N$. For one tensor polarization take

\[
h_{ij}=A^2\operatorname{diag}
\left(e^{\epsilon\gamma\cos kz},e^{-\epsilon\gamma\cos kz},1\right),
\qquad N^i=0.
\]

The program constructs the Christoffel symbols and Ricci tensor of this
metric. It obtains

\[
\det h=A^6,\qquad
\widehat R=R^{(3)}[h]
=-\frac{\epsilon^2 k^2\gamma^2\sin^2 kz}{2A^2},
\]
\[
Q=\frac3N\left(\frac{\dot A}{A}-\dot w\right),\qquad
Q_{\rm TF}=\frac{\epsilon\dot\gamma\cos kz}{2N}
\operatorname{diag}(1,-1,0).
\]

The equality $\widehat R=R^{(3)}[h]$ here uses spatially homogeneous $w$;
it is not asserted on an inhomogeneous background. The exact exponential
completion fixes the spatial volume, so no discarded volume term supplies
an artificial tensor mass. Spatial isotropy supplies the identical result
for the rotated tensor polarization.

Set $P_{\rm TF}=\epsilon P_T\cos kz\operatorname{diag}(1,-1,0)$.
The trace momentum is varied, not held to its desired value. Its background
Euler equation gives $p_0=-mQ$, its first tensor jet is zero, and its second
jet is computed from the same phase action. The latter contributes nothing
to the quadratic action because the background trace Euler equation is
satisfied. For example, after eliminating $P_T$, IC-6 gives

\[
p=p_0+\epsilon^2\frac{3FmQ}{4a_0^2}
\left(\frac{\dot\gamma^2\cos^2 kz}{N^2}
-\frac{k^2\gamma^2\sin^2 kz}{A^2}\right)+O(\epsilon^3).
\]

Both trace-jet Euler residuals are checked. The actual tensor-momentum
equations give $P_T=m\dot\gamma/(4N)$ for IC-5 and
$P_T=mJ_T\dot\gamma/(4N)$ for IC-6, where $J_T$ in the quadratic result is
evaluated at $p_0$.

In the twice-spatial-average convention used by the preceding packages,

\[
L_2=\frac{mNA^3}{4}
\left[K_T\frac{\dot\gamma^2}{N^2}
-G_T\frac{k^2\gamma^2}{A^2}\right].
\]

The coefficients are extracted by differentiating the reduced phase action:

| Action | $K_T$ | $G_T$ | Physical $c_T^2=G_T/K_T$ |
|---|---:|---:|---:|
| IC-5 | $1$ | $1+FQ^2/a_0^2$ | $1+FQ^2/a_0^2$ |
| IC-6 | $1+FQ^2/a_0^2$ | $1+FQ^2/a_0^2$ | $1$ |

For $m>0$ and $J_T>0$, the new tensor kinetic and gradient coefficients are
positive. Equal negative coefficients would not be healthy and are excluded.
The time-dependent measure is retained in the IC-6 equation:

\[
\ddot\gamma+
\left(3\frac{\dot A}{A}-\frac{\dot N}{N}
+\frac{\dot J_T}{J_T}\right)\dot\gamma
+\frac{N^2k^2}{A^2}\gamma=0.
\]

Thus the characteristic cone agrees with physical light on these backgrounds.
Time-dependent damping is not a complete finite-time amplification theorem.
Anisotropic or inhomogeneous backgrounds, mixed sectors, and their
characteristics have not been reduced here.
The coefficient calculation permits arbitrary homogeneous values; its
on-shell use assumes the homogeneous background equations. Scalar
second-order responses multiply those background Euler equations and do
not alter the quadratic tensor action.

## Nearby homogeneous solutions do not enforce $F=0$

The exactly isotropic homogeneous Hamiltonian is unchanged by the revision.
At fixed barred volume $V$, differentiate its two auxiliary constraints
before substituting the witness. With the normalization
$mVe^{-1/2}h_0^2$, the actual auxiliary Hessian is

\[
H_{qq}=-\begin{pmatrix}24&-27\\-27&2\mathcal T+135/8\end{pmatrix},
\quad q=(\xi,u),\qquad \det H_{qq}=12(4\mathcal T-27)>0.
\]

Let $j=\bar\pi/\bar\pi_0$ with $V$ and action parameters fixed. Implicit
differentiation of the constraints gives

\[
\frac{dq}{dj}=
\begin{pmatrix}
-(8\mathcal T+27)/[4(4\mathcal T-27)]\\
-18/(4\mathcal T-27)
\end{pmatrix},
\]
\[
\left.\frac{dF}{dj}\right|_0
=-\frac{5\mathcal T-27}{2\ell^2(4\mathcal T-27)}\ne0,
\qquad
\left.\frac{dJ_T}{dj}\right|_0
=-\frac{4(5\mathcal T-27)}{3(4\mathcal T-27)}\ne0.
\]

These derivatives use the frozen $\sigma=1/3$ member. Since
$\mathcal T>27/4$, the Hessian is invertible and the coefficients are smooth
on $0<u<1$. The implicit-function theorem gives a nearby homogeneous
constraint surface. Eliminating its auxiliaries yields a smooth finite
Hamiltonian system, hence local homogeneous solutions through its nearby
regular data. Consequently $F$ is not identically zero on actual nearby
homogeneous solutions; $J_T>0$ also persists sufficiently close to the
witness. This is a homogeneous existence argument, not a nonlinear
inhomogeneous initial-data lift.

## Precisely which bridges survive

- The new difference and its complete first jets vanish at $p=0$; the
  stationary branch's previous first-variation equations are unchanged.
- The difference and first jets vanish at $P_{\rm TF}=0$, for arbitrary
  homogeneous $p,F$. The isotropic flat homogeneous Hamiltonian and its
  equations are unchanged. Generic **Bianchi I is not unchanged**.
- At the IC-4/IC-5 witness, $F=0$ and $P_{\rm TF}=0$. The difference starts
  at cubic perturbative order, since $P_{\rm TF}^2=O(\epsilon^2)$ and
  $F=O(\epsilon)$. Its computed second jet vanishes. This transfers the
  previously proved witness quadratic statements, not a new full theory.
- The correction contains no auxiliary spatial derivatives. At fixed
  momenta it leaves the auxiliary gradient square unchanged, but it changes
  lower-order auxiliary coefficients when shear is nonzero. This is why the
  following IC-6 numerical solve is performed anew.

## Actual IC-6 auxiliary numerical witness

The supplied density is

\[
H_{6,\mathrm{nongrad}}=H_{5,\mathrm{nongrad}}
+H_{5,\mathrm{shear}}(J_{T,\mathrm{bar}}^{-1}-1),\qquad
J_{T,\mathrm{bar}}=1+
\frac{e^{-6w}\bar\pi^2F}{m^2V^2a_0^2}.
\]

An independent covariant-to-barred density conversion has zero exact
residual before this expression is passed to the frozen variational solver.
The IC-5 solution values are not reused. The setup is the same bounded
periodic initial-momentum fixture: $\bar h=\delta$, period $2\pi$,
$m=V=h_0=1$, $\bar\pi=-3e^{-1/2}$, and
$\bar\pi_{\rm TF}=\operatorname{diag}(\epsilon\cos z,-\epsilon\cos z,0)$
with $\epsilon=0.035$. Its spatial momentum constraint vanishes. The
discrete auxiliary equations are differentiated from the new density.

| Nodes | Maximum auxiliary residual | Smallest discrete Hessian eigenvalue |
|---:|---:|---:|
| 16 | $1.2282\times10^{-13}$ | $4.3989497$ |
| 32 | $1.2568\times10^{-13}$ | $4.3989557$ |
| 64 | $1.1931\times10^{-13}$ | $4.3989571$ |

Successive-grid differences are $1.9583\times10^{-7}$ and
$4.9781\times10^{-8}$. The maximum deviation of the activation argument
from one is $4.7303\times10^{-4}$, inside the square plateau. A conservative
floating-point rectangle estimate gives $J_T\ge0.99936937$ on the finite
grid. This estimate is not certified interval arithmetic. The computation
is a finite variational solve, not a continuum existence or evolution proof.

## Executed verification

From the repository root, the following command prefix caps cooperative
numerical-library thread usage; it does not claim operating-system affinity:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
```

It was applied to each command below:

```text
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_tensor_balance_completion.py
  Exit 0: 12 tests passed. TDD missing-implementation runs first exited 1.
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/tensor_balance_completion.py
  Exit 0: 28 exact residual groups vanish and the actual IC6 density converges.
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/tensor_balance_completion.py --require-all-background-causality
  Exit 2: the same checks pass; all-background causality is unresolved.
```

Each complete run takes about eight seconds on this machine. The program
pins the frozen local executable dependency closure, reports software and
source hashes, and returns JSON-safe results. The exact geometry, momentum
variation, tensor coefficients, and homogeneous tangent are symbolic
calculations; the grid evidence is separately labeled numerical. No full
requirements checklist is certified by these bounded results.
