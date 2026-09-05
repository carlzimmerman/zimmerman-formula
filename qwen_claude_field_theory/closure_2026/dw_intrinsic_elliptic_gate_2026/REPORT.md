# Intrinsic-Elliptic DW Candidate: Exact FLRW No-Go

Date: 2026-09-04

## Verdict

The explicit intrinsic-elliptic Deffayet--Woodard mutation tested here is
**DEAD**.  The decisive obstruction is shorter and stronger than a disputed
finite-mode count:

\[
\boxed{D^2X-R_{\mu\nu}\hat u^\mu\hat u^\nu=0},
\qquad D^2X_{\rm FLRW}=0,
\]

so every homogeneous FLRW solution of this action must obey

\[
R_{\hat u\hat u}=0
\quad\Longrightarrow\quad
{d^2a\over d\tau^2}=0
\quad\Longrightarrow\quad
a(\tau)=a_*+v_*\tau.
\]

De Sitter, radiation domination, matter domination, and accelerating
LambdaCDM therefore fail the same action equation.  This is an exact
action-level falsification of this candidate.  It is not a no-go theorem for
every possible nonlocal or spectral metric theory.

An exit status of zero from the scripts means that the falsification algebra
was reproduced.  It does not mean the theory passed the fried-chicken gates.

## 1. Frozen action and off-shell definition

The candidate is

\[
S_{\rm eDW}=\int d^4x\sqrt{-g}\left[
{R-a_0^2M\over\kappa}
+\xi\left(D^2X-R_{\mu\nu}\hat u^\mu\hat u^\nu\right)
+\lambda(v^2+1)
-Q\hat u^\mu\nabla_\mu\nu
+\mathcal L_m(g,\psi)
\right],
\]

\[
v_\mu=\nabla_\mu\phi,
\qquad
\hat u_\mu=-{v_\mu\over\sqrt{-v^2}},
\qquad
h_{\mu\nu}=g_{\mu\nu}+\hat u_\mu\hat u_\nu,
\]

\[
Q=M+f(Z_s),
\qquad
Z_s={4D_iX D^iX\over a_0^2}.
\]

This normalized normal and induced metric fix the off-shell meaning of the
intrinsic derivative.  The lambda equation separately imposes \(v^2=-1\).
The \(\xi\) Euler equation is the displayed intrinsic equation.  It must not
be silently replaced by the lapse-weighted Laplacian: integration by parts
with the \(N\sqrt h\) measure produces a lapse-acceleration term in the
formal adjoint.

Ordinary matter is minimally coupled to the single metric \(g_{\mu\nu}\).

## 2. Exact exponential branch, with an important scope limit

The chosen constitutive function is

\[
f(Z)=4-2(\sqrt Z+2)e^{-\sqrt Z/2}.
\]

The script differentiates it:

\[
f_Z(4y^2)={1\over2}e^{-y},
\qquad
\mu(y)=1-2f_Z(4y^2)=1-e^{-y}.
\]

The nonlinear elliptic eigenvalues are

\[
\lambda_\perp=1-e^{-y},
\qquad
\lambda_\parallel=1+(y-1)e^{-y}.
\]

Both are positive for \(y>0\), while both vanish at \(y=0\).  Thus the exact
zero-field degeneracy is exposed rather than ignored.  Moreover,

\[
f_{ZZ}=-{e^{-\sqrt Z/2}\over8\sqrt Z}\longrightarrow-\infty
\quad(Z\to0^+),
\]

so the action is \(C^1\) but not \(C^2\) at the origin.  Absence of strong
coupling at that degenerate point has not been established.

On the assumed static \(Q=0\), \(X=\Phi\), no-slip reduction, the same
function gives

\[
\mathcal L_{\rm grad}
=-2A|\nabla\Phi|^2+A a_0^2f(4|\nabla\Phi|^2/a_0^2),
\qquad A={1\over16\pi G},
\]

and direct variation yields

\[
\nabla\!\cdot\!\left[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi\right]
=4\pi G\rho.
\]

Consequently, spherical symmetry gives \(\mu(g/a_0)g=GM_b/r^2\), the deep
limit gives \(g^2=a_0GM_b/r^2\), and circular motion gives

\[
v^4=Ga_0M_b.
\]

This is a verified reduced branch, not a derivation of \(X=\Phi\) or
\(\Phi=\Psi\) from the full metric equations.  The code labels that limitation
instead of promoting it to a PPN result.

## 3. Seven-field frozen-coefficient principal action

For a scalar Fourier mode with \(k\ne0\), unitary gauge, and fields

\[
(\zeta,E,\sigma,x,n,B,\delta\lambda),
\]

the principal quadratic density is assembled from the ADM Einstein--Hilbert block,
the varied \(-\sigma R_{\hat u\hat u}\) vertex, the elliptic localizer, and
the clock norm term.  In particular,

\[
\mathcal L_{\lambda}^{(2)}
=n\left[2\delta\lambda
+2\bar\lambda(3\zeta-k^2E)-\bar\lambda n\right].
\]

The \(\delta\lambda\) Euler equation enforces \(n=0\).  Omitting this term
produces the obsolete six-field count and is not allowed.

The inverse spatial metric also gives, even for \(k\) transverse to the
background \(D_i\bar X\),

\[
\delta Z_s=-8y^2\zeta.
\]

The transport calculation retains this metric dependence.

This characteristic calculation assumes \(\bar\xi=0\) and a supported
constant-gradient background.  It omits lower-principal-order
\(\zeta^2\)/tadpole terms from the full \(\sqrt h f(Z_s)\) expansion.  Its
pole is therefore a frozen-coefficient/high-\(k\) result, not the complete
finite-wavelength dispersion relation about a proved global background.

## 4. Calculated principal finite-k Dirac chain

The velocity Hessian is generated from the density, not entered as a test
fixture:

\[
\det W=-12Ak^4,
\qquad \operatorname{rank}W=3.
\]

The four primaries are

\[
p_n,\quad p_B,\quad p_x,\quad p_{\delta\lambda}.
\]

Their Hamiltonian preservation generates

\[
\begin{aligned}
S_n={}&4Ak^2\zeta-2\bar\lambda k^2E+2\delta\lambda
+k^2\sigma-2\bar\lambda n+6\bar\lambda\zeta,\\
C_B={}&p_E,\\
C_x={}&k^2(\sigma-2\beta x),\\
C_\lambda={}&n,
\end{aligned}
\]

with \(\beta=2Ae^{-y}>0\).  The constraint Jacobian has rank eight.  The
actual calculated \(8\times8\) Poisson matrix has rank six and the program
finds a rank-size nonzero principal minor

\[
16\beta^2k^4.
\]

Preservation fixes \(u_n,u_x,u_{\delta\lambda}\); \(u_B\) remains gauge, and
no tertiary is generated.  Thus this unitary-gauge block has two scalar
configuration degrees of freedom (two first-class and six second-class
constraints in a fourteen-dimensional scalar phase space).

This is deliberately described as a unitary-gauge block, not a finished
pre-gauge covariant \(N_{\rm grav}\) theorem.

## 5. The shift cannot be deleted before variation

After imposing \(n=0\), \(x=\sigma/(2\beta)\), and the spatial gauge \(E=0\),
the shift remains as a multiplier:

\[
\mathcal L
=-6A\dot\zeta^2-3\dot\sigma\dot\zeta
-k^2B(4A\dot\zeta+\dot\sigma)
+2Ak^2\zeta^2-{k^2\sigma^2\over4\beta}.
\]

Its equation is

\[
k^2(4A\dot\zeta+\dot\sigma)=0.
\]

Keeping this equation gives the harmonic determinant

\[
\det\mathcal O
=-{4Ak^4\omega^2\over\beta}
\left(2Ak^2-\beta k^2-3\beta\omega^2\right).
\]

Within this principal block there is one finite-frequency scalar and one
conserved zero-frequency charge:

\[
\boxed{\omega^2={e^y-1\over3}k^2}.
\]

The wave has positive kinetic energy and \(c_s^2>0\) for finite \(y>0\).
It crosses the metric cone at \(y=\ln4\) and \(c_s^2\to\infty\) as
\(y\to\infty\).  Deleting \(B\) too early instead creates a fake second wave
and a fake kinetic ghost; the regression suite prevents that error.

In canonical variables

\[
r=\zeta,
\quad q=\sigma+4A\zeta,
\quad p_r=p_\zeta-4Ap_\sigma,
\quad p_q=p_\sigma,
\]

the reduced Hamiltonian is

\[
H={p_r^2\over24A}-2Ak^2r^2
+{k^2(q-4Ar)^2\over4\beta},
\qquad \dot q={\partial H\over\partial p_q}=0.
\]

For fixed conserved \(q\), the finite wave has positive kinetic and gradient
terms.  Across charge sectors, however, the \((r,q)\) potential Hessian has

\[
\det H_{(r,q)}=-{2Ak^4\over\beta}<0,
\]

so the principal energy is not bounded uniformly across those sectors.

## 6. The true M,nu primaries

After expanding the original \(-C_M M-Q\dot\nu\) terms about the background
\(M\) equation \(\dot{\bar\nu}=-C_M\), the linear \(\delta M\) pieces cancel;
\(C_M\delta f\) is already the constitutive term in the principal action.
The remaining fluctuation transport density is therefore

\[
\mathcal L_{\rm tr}^{(2)}=-\delta Q\,\delta\dot\nu,
\]

the program derives

\[
p_M=0,
\qquad
\Phi_\nu=p_\nu+Q=0,
\qquad
\{p_M,\Phi_\nu\}=-1.
\]

Preservation fixes both associated multipliers and produces no secondary.
In particular, \(p_\nu=0\) and \(Q=0\) are not two independent Dirac
constraints.  The equation from varying \(\nu\) conserves \(Q\); selecting
\(Q=0\) is a branch/initial condition.  The code never inserts it into the PB
matrix as a generated constraint.

Adding these two true primaries to the same shared phase space gives ten
independent constraints, PB rank eight, two first-class and eight
second-class constraints in an eighteen-dimensional scalar phase space:

\[
N_{\rm scalar}^{\rm principal,unitary}
={18-2(2)-8\over2}=3.
\]

Thus the localized action contains the finite wave, the conserved clock-like
charge, and an additional transport canonical pair.  Imposing the conserved
\(Q=0\) branch is initial-data selection, not a Dirac operation that erases
that pair.  A retarded nonlocal prescription could restrict auxiliary initial
data, but the displayed local action/Hamiltonian does not do so.

## 7. Exact homogeneous obstruction

For homogeneous \(X(t)\) on FLRW, every intrinsic spatial derivative vanishes:

\[
D^2X_{\rm hom}=0.
\]

Varying the same action with respect to \(\xi\) therefore gives

\[
R_{\hat u\hat u}
=-3\left({1\over N}{dH\over dt}+H^2\right)=0.
\]

In proper time this is \(\ddot a=0\).  The zero-mode minisuperspace calculation
also retains the clock multiplier:

\[
L_0=-{6a(A+\sigma)\dot a^2\over N}
-{3a^2\dot\sigma\dot a\over N}
+a^3\lambda\left(N-{1\over N}\right).
\]

This displayed metric--\(\xi\)--clock zero-mode subchain (not the omitted
homogeneous \(X,M,\nu,\phi\) chain) has two primaries and two secondaries with
a calculated full-rank PB matrix;
the rank-size determinant is

\[
{a^{12}(N^2+1)^4\over N^8}.
\]

No finite-\(k\) division is used in this zero-mode result.

The no-go generalizes under stated assumptions: any unconstrained multiplier
\(\xi(\mathcal D_uX-R_{uu})\) whose purely intrinsic/elliptic operator
annihilates homogeneous scalars forces coasting FLRW.  Evasion requires at
least one of a homogeneous subtraction/source, temporal pieces in
\(\mathcal D_u\), an FLRW-breaking \(X\), or abandonment of this multiplier
localization.

## 8. Matter, tensors, slip, and PPN

Because \(S_{\rm aux}\) has no direct matter-field dependence and matter is
minimally coupled, diffeomorphism invariance of \(S_m\) gives on the matter
equation

\[
\nabla_\mu T_m^{\mu\nu}=0.
\]

On the favorable \(\bar\xi=0\) background, the TT block remains the EH block:
two tensor polarizations, positive kinetic coefficient, and \(c_T=1\).  This
is a scoped check, not a proof that every background of the failed action has
\(\bar\xi=0\).

The full metric equations were not pushed through a post-Newtonian expansion
after the exact FLRW failure.  Therefore \(\Phi\) and \(\Psi\) are not claimed
to be independently derived, and \(\gamma,\beta,\alpha_1,\alpha_2,\alpha_3\)
remain explicitly **UNCOMPUTED**.  No PPN value is hard-coded.

## 9. Gate ledger

| Requirement | Result for this action | Reason |
|---|---|---|
| Exact exponential kernel | PASS on reduced branch | \(f_Z(4y^2)=e^{-y}/2\). |
| Deep MOND and BTFR | PASS on reduced branch | Direct variation gives the MOND flux and \(v^4=Ga_0M_b\). |
| Controlled \(y=0\) | FAIL/unresolved strong coupling | Both elliptic eigenvalues vanish and \(f_{ZZ}\to-\infty\). |
| Exactly two gravitational modes | UNRESOLVED covariantly / adverse block | Extended unitary-gauge principal count gives three scalar configurations. |
| No hidden scalar | FAIL for localized action | A finite pole, conserved charge, and transport pair remain. |
| Scalar ghost/gradient | Scoped PASS for finite wave only | Positive kinetic and \(c_s^2>0\) for \(y>0\); energy is indefinite across charge sectors. |
| No superluminal/instantaneous channel | FAIL | \(c_s>1\) for \(y>\ln4\), diverging in the Newtonian limit. |
| Ordinary matter conservation | PASS | Separate minimal matter Ward identity. |
| Tensor speed/energy | PASS on favorable background | EH TT block has two positive modes and \(c_T=1\). |
| Viable FLRW | **FAIL exactly** | Same \(\xi\) equation forces \(\ddot a=0\). |
| \(\Phi=\Psi\), lensing, PPN | UNCOMPUTED | Candidate already fails exactly; no values inferred. |
| \(a_0\)-Lambda relation | INPUT ONLY | No derivation is claimed. |

## 10. Status and next unavoidable calculation

- This explicit intrinsic-elliptic DW candidate: **DEAD**.
- The full fried-chicken program: **OPEN**.

The strongest remaining architecture is genuinely nonlocal/metric-spectral,
not another pure intrinsic multiplier of \(R_{uu}\).  Its unavoidable first
calculation is an explicit covariant action with a frozen spectral projector,
metric-only source \(J[g]\), and nonzero-stress functional
\(U(\chi,\mathcal I[g])\), followed by full metric variation.  The resulting
static \(T_{00}^{\rm aux}\) and trace-free \(T_{ij}^{\rm aux}\) must produce
both the exponential phantom density and zero slip before a Dirac/PPN program
is warranted.

## 11. Reproduction

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/dw_intrinsic_elliptic_gate_2026/dw_intrinsic_elliptic_gate_2026.py
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/dw_intrinsic_elliptic_gate_2026/test_dw_intrinsic_elliptic_gate_2026.py
```

The finalized runs must report 19/19 internal derivation checks and 11 direct
regression tests.  These numbers certify the calculation ran; the scientific
verdict printed by the executable remains **DEAD**.
