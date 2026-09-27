# CA4-PN: projected, Newton-normalized common-action candidate

This is the **main revised candidate** of CD26-4. It supersedes the
unprojected trial in `ACTION_REPORT.md`. Its improvements are constructive:
an action-level projection admits homogeneous carrier density, the
Newton-normalized host removes a finite-alpha frozen scalar instability,
and a weighted convex-composition gate supplies its own interface terms.
It is not a global evolution or phenomenology certificate. In particular,
the gate adds a lapse principal term which fixed-lapse convexity does not
control automatically.

The assigned base is `ecffd2af3623ff3e32318234fd51e1fac50b9126`, with prior
dirty work preserved. The active target is filtered `nu_mono`, criterion B,
one physical metric for baryons/photons, and no new dark-matter particle
species. Classical carrier fields have independent, explicitly counted
initial data; no abundance is supplied by a name.

## A. Frozen definition of the action

Use `c=1`, signature `-+++`, `M^2=(8pi G_bare)^(-1)>0`, and

\[
 0<\alpha<2,\quad c_N=1-\alpha/2>0,\quad c_2>0.
\]

The varied clock `tau` has `X_tau=-(partial tau)^2>0` and defines
`n=-d tau/sqrt(X_tau)`, `h=g+n n`, `N=X_tau^(-1/2)`,
`a=n dot nabla n=D ln N`, and `Kij`, `K`. Its leaves are compact, closed,
connected and spacelike. Let

\[
 \langle F\rangle_h=\frac{\int_{\Sigma_\tau}\sqrt h F}
                              {\int_{\Sigma_\tau}\sqrt h},\quad
 z=Z-\langle Z\rangle_h,\quad Q_K=K-\langle K\rangle_h.
\]

The fields `U,Z` are independent scalar auxiliaries, not names assigned to
Newtonian potentials before variation. The carrier consists of real
classical fields `varphi_A`, for example the already specified Cartesian
U(1) pair with optional additional trigger field, with a declared `V>=0`.
Set

\[
 K_d=\tfrac12\sum_A(n\cdot\partial\varphi_A)^2,\quad
 W_d=\tfrac12\sum_A|D\varphi_A|^2+V,\quad
 {\cal L}_d=e^zK_d-e^{-z}W_d,\quad\rho_d=e^zK_d+e^{-z}W_d. \tag{A1}
\]

Take the geometric heat operator `S_h=exp(b Delta_h)`, `b=xi^2/2>0`,
where `Delta_h=div_h D` is the actual intrinsic Laplacian. Introduce heat
fields `W(s,x),L(s,x),lambda0(x)`, `0<=s<=b`, with

\[
 H_{\rm heat}=\int_0^bL(\partial_sW-\Delta_hW)ds+\lambda_0(W_0-U).
\]

The kernel primitive is exactly

\[
 J(p)=2a_0^2q(|p|^2/a_0^2),\quad
 q'(y^2)=\nu_{\rm mono}(y)-1,\quad q(0)=0. \tag{A2}
\]

Thus `J_p=4(nu_mono−1)p`, and its nonzero-gradient Hessian eigenvalues are
`4 C_T,4 C_L`. The actual XC4 floor splice at `y_star≈2.3374`, the
zero-gradient `C^1` behavior, and the non-`C^3` splice are retained.

Define `Delta_N=div_N D=N^-1 D_i(N D^i)` and

\[
 Y=J(DW_b)+\ell\Delta_NW_b-\theta,\qquad f=G'(Y),
 \quad\ell,\theta,\delta>0\ \hbox{constants}. \tag{A3}
\]

Here `G` is convex and smooth, `G=G'=0` for `Y<=0`, `G'=1` for
`Y>=delta`. An explicit choice is `G(Y)=integral_0^Y F(t/delta)dt` for
`Y>0`, zero otherwise, with the symmetric smooth step
`F(t)=g(t)/(g(t)+g(1-t))`, `g(t)=exp(-1/t)` for `t>0`, zero otherwise.
Its symmetry gives `G(Y)=Y-delta/2` above the transition.

The action is

\[
\boxed{\begin{split}
S_{\rm PN}={}&\frac{M^2}{2}\int\sqrt{-g}\,[
 R^{(4)}-2\Lambda+\alpha|a-DZ|^2-c_2Q_K^2
 +4a\cdot DZ-2|DZ|^2-4c_N DZ\cdot DU\\
&\hspace{43mm}+c_N G(Y)+c_N H_{\rm heat}]
 +\int\sqrt{-g}\,{\cal L}_d+S_b[g]+S_{\rm GHY}.
\end{split}} \tag{A4}
\]

`S_b` contains ordinary matter and photons minimally coupled to `g`.
`S_GHY` has the standard Einstein temporal-cap terms. Use interior
variations, or fix metric and clock jets on those caps. There is no spatial
boundary. Heat endpoints are varied; the auxiliary heat coordinate is not
physical time. The action is leafwise nonlocal, with no hidden cutoff.

There is **one independent physical metric**. The carrier coupling is
explicitly nonminimal and uses the composite lapse `N_d=N exp(-z)`, or
composite characteristic metric `g_d=g+(1-exp(-2z))n n`. This is a derived
carrier characteristic structure, not a second varied metric or a photon
metric. It cannot be described as universal minimal matter coupling.

`a0,xi,ell,theta,delta,alpha,c2,Lambda` remain declared inputs. In these
units `ell` is dimensionless, while `J,theta,delta` have dimension inverse
length squared. The gate is an energy-plus-density gate, not DE1's
vacuum-fraction threshold or L361's screened region mask. Their empirical
passes and screening properties are not inherited. Promoting `theta` to
`theta(K)` is a different action and is not done here.

## B. Projection repairs the actual compact zero-mode contradiction

For the unprojected exponential carrier, the `Z` equation would imply
`integral N sqrt(h) rho_d=0`. Positive homogeneous carrier energy would be
forbidden. Subtracting the mean only after deriving that equation is not
a repair of its action.

In (A4), varying `Z` at fixed `N,h` instead gives the source

\[
 \rho_d-\frac{\langle N\rho_d\rangle_h}{N},\quad
 \int N\sqrt h\left(\rho_d-\frac{\langle N\rho_d\rangle_h}{N}\right)=0.
 \tag{B1}
\]

The exact symmetry `Z -> Z+c(tau)` is restored. The carrier sees `z`, and
the gravity action sees only `DZ`. This removes an unphysical source of
the zero mode, without adding a new propagating homogeneous `Z` degree of
freedom. It does not eliminate the carrier's own homogeneous energy or
initial data.

Because this is the **h-volume**, not lapse-weighted, mean, fixed-h lapse
variation still gives precisely `rho_d`. Its spatial-metric variation is
not zero:

\[
 \delta_h\langle Z\rangle_h=\tfrac12\langle z h^{ij}\delta h_{ij}\rangle_h,
 \quad
 \Delta T^{ij}_{\rm mean}=-\frac{\langle N\rho_d\rangle_h}{N}z h^{ij}.
 \tag{B2}
\]

This term supplements the local variation of `Ld` through `n,h`; it must
not be omitted from the full metric equation. No lapse mean-stress term
is silently substituted from a different weighted projector.

The clock also moves its leaves. At fixed `g,Z`, put
`B_Z=n(Z)+K z`, so `d<Z>_h/dtau=<N B_Z>_h`. The mean's deformation gives

\[
 \delta_\tau z(x)=\langle N\delta\tau B_Z\rangle_h
                  -\delta\tau(x)\langle N B_Z\rangle_h,
\]
\[
 \frac1{\sqrt{-g}}\frac{\delta S_d}{\delta\tau}\bigg|_{\rm mean}
 =\langle N\rho_d\rangle_h B_Z-\rho_d\langle N B_Z\rangle_h. \tag{B3}
\]

The variation vanishes under a pure leafwise relabeling, as it should.
For the mean of `K`, include its explicit local `delta K` as well as the
same leaf-shape and volume variations; it is not a prescribed background.

## C. All auxiliary equations and the derived interface force

Let

\[
 R_W=-\operatorname{div}_N(fJ_p)+\ell\Delta_N f,
 \qquad S_N^\dagger=N^{-1}S_hN.
\]

The heat and endpoint equations are

\[
 \partial_sW=\Delta_hW,\ W_0=U,\quad
 \partial_sL=-N^{-1}\Delta_h(NL),\quad L_b=-R_W,\quad\lambda_0=L_0.
\]

The independent `U,Z` equations are

\[
 \boxed{4\Delta_N Z=S_N^\dagger[
       \operatorname{div}_N(fJ_p)-\ell\Delta_Nf],} \tag{C1}
\]
\[
 \boxed{2M^2c_N\operatorname{div}_N(DZ-a+DU)
          +\rho_d-\langle N\rho_d\rangle_h/N=0.} \tag{C2}
\]

The heat generator is geometric `Delta_h`; the adjoint and differential
operators in its Euler equations are weighted by the action lapse. These
facts are compatible and cannot be replaced by one guessed Laplacian.
Equation (C1) contains the derived interface term
`-ell S_N^dagger Delta_N f`. Dropping it is not an approximation with an
unchanged action.

At fixed `N,h`, eliminating the carrier-free `Z` gives the auxiliary energy

\[
 E_U=\int N\sqrt h\,[2|DU-a|^2+G(Y)].
\]

Its second directional variation, wherever a regular tangent exists, is

\[
 4\int N|D\delta U|^2+
 \int N\{f\,\delta p^TH_J\delta p
 +G''(Y)[J_p\cdot\delta p+\ell\Delta_N\delta W]^2\}, \tag{C3}
\]

with `delta W=S_h delta U`. Convexity also follows directly by composition
at zero gradient; no finite Hessian is assumed there. This is strong
convexity modulo the constant `U` gauge on a fixed positive-lapse leaf.
It is not a joint metric/lapse convexity assertion.

The fixed-h lapse variation of the gate is exact:

\[
 \delta_{\ln N}\int N\sqrt hG(Y)
 =\int N\sqrt h\,\delta\ln N
       [G(Y)-\ell\operatorname{div}_N(fDW_b)]. \tag{C4}
\]

For `f=1`, the integrated `ell Delta_N W` is an exact spatial boundary
term, including under lapse variation. The remaining density is
`J-theta-delta/2`. The plateau thus carries a real positive vacuum offset
`M^2 cN (theta+delta/2)/2`; it must be retained. Subtracting
`G(ell Delta_NW-theta)` to remove it would generally lose convexity and
define a different action.

For all metric/clock variations retain

\[
 \delta S_h=\int_0^b e^{(b-s)\Delta_h}(\delta\Delta_h)e^{s\Delta_h}ds.
 \tag{C5}
\]

Metric contraction, volume, and mean variations remain in addition to
(C5). At fixed `g`, `delta_tau n_mu=-h_mu^nu partial_nu(delta tau)/sqrt X`,
`delta h=delta(n n)`, `delta a=(delta n) nabla n+n nabla(delta n)`, and
`delta K=div(delta n)`. Since
`Delta_h F=h^{mu nu}nabla_mu nabla_nu F+K n(F)`, both parts of that operator
must be varied. These rules, (B2)–(B3), and the displayed local action
specify the clock Euler equation `delta S/delta tau=0`; a reduced global
clock evolution theorem is not supplied here.

## D. Exact lapse and momentum constraints in unitary gauge

Set

\[
 T_K=K_{ij}K^{ij}-K^2,\quad A_K=\langle NQ_K\rangle_h,
\]
\[
 V_a=\alpha|a-DZ|^2+4a\cdot DZ-2|DZ|^2-4c_N DZ\cdot DU.
\]

Varying `N` at fixed `h,hdot,shift` after solving the heat constraints gives

\[
\begin{split}
\frac{M^2}{2}\{&R^{(3)}-T_K-2\Lambda
 +c_2[-Q_K^2+2KQ_K-2KA_K/N]\\
 &+V_a-\operatorname{div}_N[2\alpha(a-DZ)+4DZ]
 +c_N[G-\ell\operatorname{div}_N(fDW_b)]\}
 =\rho_b+\rho_d. \tag{D1}
\end{split}
\]

`rho_b` is the actual ordinary-matter normal energy. The mean projector
has no extra fixed-h lapse term. The `A_K/N` term is forced by varying the
centered trace; dropping it changes the constraint.

There are no explicit `hdot` terms in the intrinsic heat or spatial gate
in unitary gauge. The metric momentum is therefore

\[
 \pi^{ij}=\frac{M^2\sqrt h}{2}
 [K^{ij}-Kh^{ij}-c_2(Q_K-A_K/N)h^{ij}]. \tag{D2}
\]

Spatial diffeomorphism invariance gives
`-2 D_j pi^j_i + sum pi_A D_i varphi_A + ordinary matter momentum=0`, with
`pi_A=sqrt(h) exp(z) n(varphi_A)`. Auxiliary zero momenta and their
preservation still require the full Dirac analysis. Equations (D1)–(D2)
are not a degree-of-freedom count. The spatial metric equation also
retains (B2), the centered-trace mean variation and (C5); it is not inferred
from the lapse equation.

## E. Independent static metric equations and measured Newton coupling

In the leading static weak-field expansion write independent potentials
`ds^2=-(1+2Phi)dt^2+(1-2Psi)dx^2`. At the retained order the gravity density
in units `M^2/2`, before eliminating either potential, is

\[
 2|D\Psi|^2-4D\Phi\cdot D\Psi
 +\alpha|D\Phi-DZ|^2+4D\Phi\cdot DZ-2|DZ|^2
 -4c_N DZ\cdot DU+c_N G(Y). \tag{E1}
\]

Use the ordinary post-Newtonian scaling of the dimensionless potentials
and `a0`; the new `ell` corresponds to a fixed physical velocity-squared
parameter divided by `c^2`, while `theta,delta` scale with the quadratic
gravity density. In that limit the spatial metric dependence of the gate,
projector and filter stress is one weak order higher. Outside this
ordering it must be kept via (B2), (C4), (C5) and the full action.

Independent `Psi` variation gives `Delta(Psi-Phi)=0`, hence `Psi=Phi` on
the fixed nonzero-mode branch. Its substitution reduces (E1) to

\[
 -2c_N|D(\Phi-Z)|^2-4c_N DZ\cdot DU+c_NG(Y). \tag{E2}
\]

For leading cold carrier/source contrasts on a flat compact perturbation
leaf, or isolated sources with the corresponding boundary normalization,
the separate lapse and `Z` equations give

\[
 2M^2c_N\Delta(\Phi-Z)=\delta\rho_b+\delta\rho_d,\quad
 2M^2c_N\Delta(Z-\Phi+U)=-\delta\rho_d.
\]

Consequently

\[
 \boxed{G_N=G_{\rm bare}/c_N,\qquad
       \Delta U=4\pi G_N\delta\rho_b.} \tag{E3}
\]

The contrasts are part of the compact background/perturbation split, not
an imposed deletion of homogeneous carrier energy; section G treats that
energy in the same action. Baryons and photons see the metric potential
`Phi`, while the cold/WKB carrier potential is `Phi-z`. Its full field
transport is its actual wave equation, not an independently assigned
particle force law.

On a full-on plateau, `J_p=4(nu_mono−1)DW` and (C1) yields the prescribed
filtered phantom term. At a transition there is the new interface term;
the full gate law is changed. Regional Yukawa screening from L361 is absent
in this new action, so external-field/lensing gates require fresh work.

**Negative control.** Keeping the old `alpha a^2` term and the unnormalized
cross term would give `Delta(U-alpha Phi/2)=rho_b/(2M^2)`. The kernel would
read a carrier-dependent lapse contribution. The normalization in (A4)
repairs this algebra rather than declaring that small leakage exactly zero.

## F. A new positive frozen scalar block, and its remaining transition test

On a carrier-free full-on plateau, eliminate `Z` using `DZ=a-DU`.
The host becomes
`EH +alpha a^2+2cN|DU-a|^2+cN J-c2 Q_K^2`, in units `M^2/2`.
Around a homogeneous background at nonzero spatial momentum the centered
trace has the same quadratic fluctuation as `K`.

For a frozen constitutive coefficient `C>=0` the scalar quadratic action
before solving the lapse, shift and `U` is

\[
\begin{split}
L_2={}&-6\dot\psi^2+4k^2\beta\dot\psi
 -c_2(3\dot\psi-k^2\beta)^2+2k^2\psi^2-4k^2\Phi\psi\\
 &+2c_Nk^2(U-\Phi)^2+\alpha k^2\Phi^2+2c_Nk^2 C U^2.
\end{split}
\]

Direct elimination gives

\[
 U=\frac{2\psi}{2C+\alpha},\quad
 \Phi=\frac{2(1+C)\psi}{2C+\alpha},\quad
 \beta=\frac{2+3c_2}{c_2k^2}\dot\psi,
\]
\[
 \boxed{L_{2,\rm red}=\frac{2(2+3c_2)}{c_2}\dot\psi^2
       -\frac{2(2-\alpha)}{2C+\alpha}k^2\psi^2,\quad
 c_s^2=\frac{c_2(2-\alpha)}{(2+3c_2)(2C+\alpha)}>0.} \tag{F1}
\]

This is verified by both substitution and the independent four-row
determinant. The old unnormalized host instead has a numerator
`2-alpha(1+C)` and fails at sufficiently large `C`. The revised host
removes that crossing. It retains a genuine scalar canonical pair in this
reduced sector; a declaration of exactly two total modes would be false.
Its classification as an allowed clock/matter scalar and the full count
must follow the completed constraints, not terminology.

`C->infinity` still sends the frozen sound speed to zero. The inactive
open-zero branch instead has `C=0` and is regular in this block. The
convex gate's transverse active-zero and filtered-operator estimates are
useful local bounds, but do not turn (F1) into a global nonlinear theorem.

There is also a new transition obligation. Write `p=DW`. Lapse variation
of `ell Delta_NW` contains `ell p dot D(delta ln N)`. The quadratic gate
therefore adds an **unfiltered** lapse-gradient coefficient. In the aligned
frozen high-frequency direction the evolution lane obtains

\[
 \alpha_{\rm UV}=\alpha+\frac{c_N}{2}G''(Y)\ell^2|p|^2,
 \qquad \alpha_{\rm UV}<2
 \ \Longleftrightarrow\ G''(Y)\ell^2|p|^2<4. \tag{F2}
\]

The action's convexity does not enforce this bound. This is a separate
principal-symbol condition, not the retired metric-cone speed condition.
A possible restricted NR domain uses positivity of total baryon density:
`Delta S U>=-4pi G_N rho_bar_b`. On the ramp this bounds
`J(p)<=theta+delta+ell 4pi G_N rho_bar_b`, hence `|p|<=p_max` and permits
the sufficient choice `||G''||inf ell^2 p_max^2<4`. The full action has not
yet been shown to propagate that source/geometry domain. Do not claim
global health from this conditional repair.

On a homogeneous inactive branch, the tensor principal quadratic action
is just Einstein's: `M^2 a^3[hdot_ij^2-a^-2(Dh_ij)^2]/8`. `Q_K=0` and
its TT first variation is zero; all gate derivatives vanish and scalar
spatial gradients are zero. Thus that branch has positive standard tensor
kinetic energy and speed one. General inhomogeneous/transition tensor and
clock mixing are not certified by this special background.

## G. The homogeneous branch is present in the same action

If `f=G'=0` on the whole compact leaf, (C1) gives `Delta_N Z=0`; hence
`DZ=0`, so `z=0`. On an exactly homogeneous FRW branch also `a=DU=0`,
`Y=-theta<0`, and `Q_K=0`. Both the projection stress and its clock
variation vanish. The carrier is then the ordinary canonical field system
with positive density, not a forbidden mean source.

The field equations reduce to

\[
 3M^2H^2=M^2\Lambda+\rho_b+\rho_d,\quad
 -2M^2\dot H=\rho_b+P_b+\rho_d+P_d,
 \quad G_{\rm cosm}/G_N=c_N. \tag{G1}
\]

The carrier obeys its canonical homogeneous field equations and
`rho_dot+3H(rho+P)=0`; a U(1) pair retains its independent conserved charge.
These are admissible expanding backgrounds when the right side is
positive. They are not a cosmological abundance, perturbation, CMB, forest
or late-time transport fit.

For comparison, the **different uncentered-trace variant** replaces
`-c2 Q_K^2` by `-c2 K^2`. Its homogeneous Friedmann equation is
`3M^2(1+3c2/2)H^2=M^2Lambda+rho`, and
`G_cosm/G_N=cN/(1+3c2/2)`. Centering the trace is an explicit action change,
with its nonlocal mean variations already present in (D1)–(D2), rather
than a silent deletion of the cosmological mode.

## H. Conservation, transport and the remaining closure

Ordinary matter satisfies its own covariant conservation identity because
`S_b[g]` is minimal and the gate does not explicitly depend on baryon
fields. For the carrier,

\[
 C_d^{\mu\nu}=e^{-z}h^{\mu\nu}-e^z n^\mu n^\nu,\quad
 \nabla_\mu(C_d^{\mu\nu}\partial_\nu\varphi_A)-e^{-z}V_{,A}=0.
\]

An invariant pair has its corresponding conserved U(1) current. In a
fixed flat foliation the exact energy exchange is
`partial_t E_d+div F_d=-zdot rho_d`, with
`E_d=e^z dotvarphi^2/2+e^-z(|Dvarphi|^2/2+V)` and
`F_d=-e^-z sum dotvarphi_A Dvarphi_A`.
The projection and constrained gravity sector receive that exchange. It
is not a disappearance of energy, and it does not by itself prove spatial
evacuation or determine a cosmological velocity distribution.

The concrete advances are the projected common action, its exact source
identity and interface terms, independent weak metric equations, measured
Newton normalization, homogeneous branch, and the positive revised frozen
scalar block. The missing implication is a constraint-preserving coupled
evolution theorem controlling the gate's lapse block, timelike foliation,
mean operators, metric/field regularity and zero/splice strata. PPN and
empirical tests must then use this same action. The present record does
not claim that implication has been established.

`check_revised.py`/`revised_run1/` record 28 passing exact and bounded
checks; the original bridge `check_action.py`/`run1/` records 46. The two
sources and their contracts are separately pinned. Neither run executes
the old large campaigns. `EVIDENCE.md` and source provenance distinguish
these checks from the independent evolution/transport lane results.
