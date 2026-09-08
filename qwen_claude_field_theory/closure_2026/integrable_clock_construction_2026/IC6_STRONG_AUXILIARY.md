# IC6: local strong auxiliary solve and smooth Dirac-domain bridge

Base `0b75e72bf5797e451beb258847ade528cd9c4551`, 2026-09-08.
**Same IC6 action; full theory OPEN.** This extends the weak inverse in
[NONLINEAR_SQUARE_REPORT.md](NONLINEAR_SQUARE_REPORT.md); it is not a proof
of a well-posed or causal coupled time evolution.

## 1. Fixed theory, fields and new statement

Use the complete phase action in [TENSOR_BALANCE.md](TENSOR_BALANCE.md),
including its IC5 definitions, with no ordinary matter in this calculation.
On the open expanding plateau, at fixed barred metric and canonical momentum,

\[
-H_6=\int dV_g\,[P(s,t;g,\pi,R[g])+A(s,t)|Ds|_g^2],\qquad
s=\xi+bu,\quad t=u,\quad A=m\alpha e^{t(s-bt)}>0.
\]

Here and below **(g) is the barred three-metric**, not the physical
four-metric. The explicit nongradient density is

\[
P=-\frac{1}{V}\left[
\mathcal H_b+\mathcal DF R+
\mathcal H_{5,\mathrm{shear}}(J_T^{-1}-1)\right],\quad
J_T=1+\frac{e^{-6(u-1)\xi}\pi^2F}{m^2V^2a_0^2}.
\]

All symbols on the right retain the definitions in IC5_ACTION.md; (P)
is not an adjustable potential. The logarithmic potential requires
(0<t<1). Keep (J_T>0), positive metric, and strict plateau membership.
The phase Hamiltonian is used; no additional Legendre denominator is needed
for the argument. The optional compact Lagrangian also needs (K_6\ne0).

**Local conclusion.** Around the specified flat expanding initial state,
the two auxiliary equations have a unique nearby solution in the strong
spaces below for sufficiently small canonical-data perturbations. Smooth
data give smooth auxiliary solutions. The actual auxiliary Poisson operator
and its inverse consequently act on a common smooth domain. At such a
smooth state, secondary preservation determines unique smooth auxiliary
multipliers. These are instantaneous constraint statements, not an
existence theorem for the resulting coupled time-dependent PDE.

## 2. Eliminating the algebraic variable changes the principal operator

Let (p_i=D_i s) only in this section; this (p_i) is not a canonical
momentum. The equations obtained by varying the same energy are

\[
C_s=P_s+A_s p^2-2D_i(Ap^i)=0,\qquad C_t=P_t+A_t p^2=0.
\]

Put (M=P_{tt}+A_{tt}p^2). Near the witness (M>0). The pointwise
algebraic equation gives a local function (t=\tau(s,p;g,\pi,R)) and

\[
\tau_{p_i}=-\frac{2A_t p^i}{M},\qquad
\tau_s=-\frac{P_{ts}+A_{ts}p^2}{M}.
\]

For (E=P+A p^2), the reduced energy is
(e(s,p)=E(s,\tau(s,p),p)). The envelope identity (E_t=0) gives

\[
e_{p_i p_j}=2Ag^{ij}-\frac{4A_t^2}{M}p^ip^j.
\]

Thus the two transverse eigenvalues are (2A), while the longitudinal
one is (2A-4A_t^2|Ds|^2/M). Positivity of (A) alone would not suffice.
This exact correction follows by varying and eliminating the quadratic
passive response, as independently checked in `ic6_strong_auxiliary.py`.
The test fixture with large gradient actually becomes indefinite; the
program does not automatically label all auxiliary configurations healthy.
The bound

\[
M>0,\qquad 2A M>4A_t^2|Ds|^2
\]

is strict at the witness and persists in a sufficiently small smooth
neighborhood. It is a spatial auxiliary ellipticity condition, not a
physical signal-speed or positive-energy statement.

## 3. A strong-space local solve, not just a weak inverse

Use the fixed coordinate three-torus of period (2\pi), with flat witness
(g_0=\delta), (V_0=1), and retain the original positive (m,h_0).
Let (r\ge2) be an integer and define

\[
\mathcal E_r=H^{r+2}_s\oplus H^{r+1}_t,\quad
\mathcal F_r=H^r_s\oplus H^{r+1}_t,\quad
\mathcal Z_r=H^{r+3}_{g}\oplus H^{r+1}_{\pi}.
\]

Metric components are symmetric and the metric stays positive. Coordinates
and the reference Sobolev norms are fixed; smooth nearby metrics give
equivalent norms. Normalize the constraint map by the fixed positive
constant (m e^{-1/2}h_0^2), not by a varied field. The normalized map
(\mathcal C:\mathcal E_r\times\mathcal Z_r\to\mathcal F_r) is smooth
on a sufficiently small open ball about the witness. To check the orders:

- (R[g]\in H^{r+1}), and all nondifferential functions of (q,g,\pi,R)
  are in (H^{r+1}) while denominators stay bounded away from zero.
- (Ds\in H^{r+1}), so (C_t\in H^{r+1}).
- (D_i(A D^i s)\in H^r); there is no second derivative of (t).
- In three dimensions (H^{r+1}), (r\ge2), supports the required
  products and smooth compositions. These are finite-regularity maps,
  not a nonlinear map on an arbitrary open (H^1\oplus L^2) ball.

At the witness, differentiating (H_6) **before** fixing the momenta gives
the mass matrix, normalized as above, in (q=(\xi,u)):

\[
M_q=\begin{pmatrix}24&-27\\-27&2\mathcal T+135/8\end{pmatrix},
\qquad \mathcal T=-27/16+54/[5\ln(9/5)]>27/4.
\]

The canonical coordinate change has
(p_s=p_\xi, p_t=p_u-bp_\xi). Its Jacobian and one-form are checked
explicitly. In the ((s,t)) coordinates the mass is

\[
M_0=\begin{pmatrix}
24&2(4\mathcal T-27)/3\\
2(4\mathcal T-27)/3&2\mathcal T(4\mathcal T-27)/27
\end{pmatrix}.
\]

For every Fourier vector (k\in\mathbb Z^3), the actual linearization is

\[
L_0(k)=M_0+2a|k|^2\begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
a=\frac{\alpha e^{2/3}}{h_0^2}>0,
\]
\[
\det L_0(k)=\frac{3(4\mathcal T-27)}{2\mathcal T h_0^2}
\left[8\mathcal T h_0^2+e^{2/3}|k|^2\right]>0.
\]

This determinant is computed, not supplied as an input. In particular
(k=0) is invertible by its mass; no zero mode is deleted.
For sources ((f,g)), write (a_{ij}=(M_0)_{ij}). Then

\[
v_k=\frac{f_k-a_{12}g_k/a_{22}}
 {2a|k|^2+a_{11}-a_{12}^2/a_{22}},\qquad
w_k=\frac{g_k-a_{12}v_k}{a_{22}}.
\]

The denominator is bounded below by (c(1+|k|^2)) for some (c>0).
Multiplying by the Sobolev weights and summing proves

\[
\|(v,w)\|_{\mathcal E_r}\le K_r\|(f,g)\|_{\mathcal F_r}.
\]

There is also a bounded forward map of the displayed orders; hence this
is a strong isomorphism. The nine numerical Fourier controls in the script
only check implementation/conditioning. The all-(k) conclusion comes
from this exact positive denominator and weight estimate.

For completeness, the nonlinear existence step can be implemented as a
contraction: for fixed canonical data (z), iterate

\[
q_{n+1}=q_n-L_0^{-1}\mathcal C(q_n,z).
\]

Continuity of (D_q\mathcal C) allows a ball where
(\|I-L_0^{-1}D_q\mathcal C\|_{\mathcal E_r\to\mathcal E_r}<1/2).
Choose (z) close enough that
(\|L_0^{-1}\mathcal C(q_0,z)\|<R/2), with a closed radius-(R) ball
contained in that neighborhood. The iterate stays in this complete ball,
successive differences are bounded by a geometric series, and its limit
is the unique root there. At that root the inverse linearization is the
norm-convergent Neumann series around (L_0^{-1}).

For smooth data, start with (r=2): (s\in H^4\subset C^{2,\mu})
for (0<\mu<1/2). After algebraic elimination the equation has the form
(a^{ij}(x,s,Ds)D_iD_j s=f(x,s,Ds)), with smooth functions of their
arguments and leading matrix (e_{p_i p_j}), uniformly positive nearby.
Its coordinate difference quotient (v_h=[s(x+he_j)-s(x)]/h) solves a
linear uniformly elliptic equation. The mean-value formula moves terms
containing (D v_h) and (v_h) into its lower-order coefficients; all
coefficients and its remaining source have uniform (C^{0,\mu}) bounds
because (s\in C^{2,\mu}) and the data are smooth. Each fixed-(h)
quotient is already (C^{2,\mu}), so the interior Schauder a priori
estimate applies without assuming additional regularity. Its (C^0)
norm is bounded by (\|Ds\|_{C^0}). Thus (v_h) has uniform local
(C^{2,\mu}) bounds. Compactness, using a smaller Hölder exponent if
needed, gives (s\in C^{3,\mu'}). Iterate on nested interior charts;
the compact torus has no boundary. The algebraic formula then gives
smooth (t). This proves regularity of the already constructed solution,
not a new global existence assertion.

**External regularity leaf.** Leon Simon, *Lectures on PDE*, revision
March 5, 2015, Lecture 12, Theorem 2 (printed pp. 126–127; PDF page 66),
states the interior nondivergence Schauder estimate used for these
difference quotients. Its hypotheses are bounded Hölder coefficients,
uniform ellipticity and a (C^{2,\mu}) solution for order two. The
estimate is for smaller interior balls. The nearby IC6 scalar operator
above supplies those hypotheses; finite chart coverage handles the torus.
The PDF gives the companion divergence-form proof and sets the analogous
Theorem 2 proof as an exercise, so it is an authenticated standard estimate,
not an independently formalized library theorem here. [Author's PDF](https://math.stanford.edu/~lms/lecs-on-pde.pdf).
Checked 2026-09-08; no source cache or Lean build is claimed. This bounded
source check is not a novelty search.

## 4. Actual nonuniform continuum initial data

Set (g=\delta), (\pi_0=-3m e^{-1/2}h_0), and

\[
\pi^{ij}=\frac{\pi_0}{3}\delta^{ij}
+\epsilon\,\operatorname{diag}(\cos z,-\cos z,0).
\]

The spatial constraint (-2\partial_j\pi^{ij}=0) is exact, and the
trace stays fixed. These data approach the witness in every fixed
\(\mathcal Z_r\) as \(\epsilon\to0\). The construction in section 3
therefore supplies their **continuum** auxiliary solution for sufficiently
small \(\epsilon\), not merely a discretized root. Set the auxiliary
and shift primary momenta to zero. All initial constraints are then
satisfied. This existence result has no claimed explicit maximum
\(\epsilon\); the earlier finite-grid value 0.035 is not thereby
certified within the continuum theorem's unspecified neighborhood.

## 5. Common smooth domain and instantaneous preservation

Take unnormalized density constraints
\(\widetilde C_A=\delta(-H_6)/\delta q_A\), so
\(\widetilde C_A=V C_A\). In this section
\(L=D_q(C_s,C_t)\) is the **unnormalized** derivative; the map of section 3
has derivative \(D_q\mathcal C=L/(m e^{-1/2}h_0^2)\).
The density derivative is \(K=V L\), since \(V\) is fixed in auxiliary variations. Multiplication
by the smooth positive \(V\) is an isomorphism. The weak coercivity
argument in NONLINEAR_SQUARE_REPORT.md applies with the IC6 potential.
The strong local inverse and elliptic regularity give
\(K^{-1}:C^\infty\oplus C^\infty\to C^\infty\oplus C^\infty\).
Explicitly, in the inhomogeneous linearized system eliminate
\(w=M^{-1}(g-L_{ts}v)\); the remaining operator is
\(L_{ss}-L_{st}M^{-1}L_{ts}\), with leading matrix (e_{p_i p_j}).
At a smooth root its coefficients and a smooth source are smooth.
The strong inverse first supplies (v\in H^4\); elliptic regularity then
gives smooth (v), and the algebraic formula gives smooth (w).

The constraints' metric-momentum brackets are not set to zero. They are
obtained by varying the same density. For smooth smearing functions let

\[
\widetilde C[f]=\int f^A\frac{\delta(-H_6)}{\delta q_A},\quad
E_f^{ij}=\frac{\delta\widetilde C[f]}{\delta g_{ij}},\quad
B_{f,ij}=\frac{\delta\widetilde C[f]}{\delta\pi^{ij}}.
\]

In independent off-diagonal coordinates the conjugate momentum is
\(2\pi^{ij}\); alternatively sum both ordered indices consistently.
The actual brackets and drift are

\[
\Omega[f,g]=\int(E_f^{ij}B_{g,ij}-B_{f,ij}E_g^{ij}),\quad
d[f]=\int\left(E_f^{ij}\frac{\delta H_6}{\delta\pi^{ij}}
-B_{f,ij}\frac{\delta H_6}{\delta g_{ij}}\right).
\]

The IC6 density depends on (R[g]), momenta and first auxiliary gradients,
with no spatial momentum derivatives. Integration by parts therefore makes
\(\Omega\) a finite-order differential operator on its smearing functions;
all its coefficients and the drift are smooth at smooth states. In particular,
\(\Omega\) maps smooth functions to smooth densities. This proves the
**common smooth domain** needed for the compositions below; it does not
claim boundedness on the original weak (H^1\oplus L^2) space.

With order ((p_s,p_t,\widetilde C_s,\widetilde C_t)), the actual blocks are

\[
\mathbb D=\begin{pmatrix}0&-K\\K&\Omega\end{pmatrix},\quad
\mathbb D^{-1}=\begin{pmatrix}K^{-1}\Omega K^{-1}&K^{-1}\\-K^{-1}&0\end{pmatrix}.
\]

Self-adjointness refers to density/function duality; no normalization is
silently differentiated as if it were constant. No commutation of (K)
and (\Omega) is used. Under (H_T=H_6+\lambda^A p_A+\) spatial shift
terms, primary preservation gives \(\widetilde C=0\), and secondary
preservation is

\[
0=d+K\lambda,\qquad \lambda=-K^{-1}d.
\]

Thus no tertiary auxiliary equation arises **instantaneously on this
smooth regular neighborhood**. Spatial transport adds the corresponding
Lie derivative to the multipliers. This is a formal smooth Dirac
classification with a genuine common domain, not yet a bounded Hamiltonian
vector field on a single finite Sobolev phase space. The metric-curvature
dependence of (d) can cost derivatives; proving coupled local existence
and preservation of the regular neighborhood remains mandatory.

The extended spatial generator is

\[
D[\beta]=\int\left(\pi^{ij}\mathcal L_\beta g_{ij}
+p_s\mathcal L_\beta s+p_t\mathcal L_\beta t
+P_i\mathcal L_\beta\beta^i_{\rm shift}\right).
\]

Its action on every canonical variable is its Lie derivative. The
commutator of Lie derivatives gives \(\{D[\beta],D[\gamma]\}=D[[\beta,\gamma]]\)
with a consistent bracket convention; covariance of the density gives
closure with the other constraints. Locally, before imposing a spatial
gauge, there are 11 canonical pairs (six metric, two auxiliary, three shift),
six first-class constraints (three spatial chains), and four second-class
auxiliary constraints. The formal local reduced phase dimension is
\(22-2\cdot6-4=6\). The two auxiliaries supply no additional canonical
pair. Identification with two tensor pairs and one genuine clock pair
holds perturbatively at the witness; a healthy physical propagation claim
away from it still requires the coupled characteristic analysis.

The number six is a **generic per-point formal count**, not a proof that
the global quotient is a smooth six-dimensional-per-point manifold at
every included state. Translation stabilizers occur at the flat witness
even in the full torus field space; the displayed cosine data also retain
translations in (x,y). Do not apply the local gauge count unchanged to
the homogeneous finite truncation or to those global stabilizer modes. The
auxiliary zero mode itself remains controlled by the mass, as section 3
shows; neither (H=0) nor a zero clock momentum has been imposed.

## 6. What changed, and what did not

New: strong-space nonlinear auxiliary existence near the witness, actual
small nonuniform continuum constrained data, the algebraic Schur correction,
and a common smooth domain for instantaneous auxiliary preservation.
Not new or proved: finite-time nonlinear evolution, all-sector causal
propagation, a global rank statement, transition-region stability, full PPN,
galactic baryon-only AQUAL/lensing matching, or realistic cosmology.

The associated nine tests and script are reproducible. A strict
`--require-full-theory` run returns exit 2 because these remaining
obligations are not proved. This is a construction checkpoint, not a final
relativistic MOND certification or a claim of global novelty.
