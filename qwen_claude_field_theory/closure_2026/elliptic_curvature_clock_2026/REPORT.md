# Elliptic curvature/clock construction: positive health gates, unresolved causal completion

Base `11c37540d1e70cdd6b2f40077a0ce34c605b3ccd`, 2026-09-10.
**The full gravity goal remains OPEN.** This is a new explicit work package,
not a claim of literature-wide novelty. It constructs an action which repairs
the previous radial scalar gradient sign at leading weak-field principal
order while retaining static MOND, no slip, tensor luminality, and an exact
expanding homogeneous sector. It then encounters a distinct **principal causal
FAIL**, derived using compact constrained vacuum initial data. The nonlinear
background/global-boundary lift of that response remains unproved.

No test assigns a PPN parameter, expected rank, determinant, or number of
degrees of freedom as its calculation. Lean formalizes conditional inequalities,
not the Einstein equations or empirical truth. No new data fit is presented:
the candidate has not passed the gates needed to interpret such a fit as a
completed theory's prediction. Carl Zimmerman's fixed framework target and
requested separation of local auxiliary constraints from cosmological expansion
motivate this construction; the added curvature/clock mechanism and its audit
are the assistant's work.

## 1. The same explicit action throughout

Use c=1, signature (-+++), m=M²>0, lapse N>0, induced derivative D_i,
K_ij=(dot h_ij-Lie_shift h_ij)/(2N), a_i=D_i log N, and F=exp(2chi).
On finite-volume leaves define

\[
\bar K_F=\frac{\int N\sqrt h F K}{\int N\sqrt h F}.
\]

The candidate preferred-foliation action is

\[
\boxed{S=m\int dt\,d^3x\,N\sqrt h\left[
\frac F2(R^{(3)}+K_{ij}K^{ij}-K^2)-\Lambda+f(a)
+2(D\chi)^2+4D_i\chi a^i+2\chi a^2
+\frac{2F}{3}(K-\bar K_F)^2+\nu(t)\chi\right]+S_m[g,\psi],}
\]
\[
f(a)=2a_0^2[1-(1+y)e^{-y}],\qquad y=|a|/a_0.
\]

nu is ONE global function, not an independent multiplier at every point.
Its variation imposes int N sqrt(h) chi=0. It does not impose chi(x)=0.
chi has no time derivative. This does not by itself prove it is auxiliary;
its actual principal and homogeneous Dirac chains are computed below.
An action-level clock-covariant completion and full nonlinear functional
Dirac analysis remain open. The surviving scalar is counted explicitly as a
clock/gravitational scalar; it is NOT hidden in a claim that total gravity
has only two local modes. Its admission requires the user's separately
counted healthy-clock allowance, which is not yet fully satisfied.

The coefficients are construction choices, not derived constants of nature.
The optional a0²=Lambda/(32 pi) remains an input with fitted kappa=1/2.

### Why these terms are different from another trace-coefficient scan

After integration by parts with the N sqrt(h) measure, the spatial chi terms
are equivalent, up to boundary flux, to

\[
2(D\chi)^2-4\chi D_i a^i-2\chi a^2.
\]

Together with the linear term chi R3 from F R3/2, they couple chi to
I=R3-4div(a)-2a². At leading weak field, eliminating chi gives the negative
spatial curvature contact term required to change the scalar stiffness.
The matching F multiplier on the tensor time kinetic term prevents the
spatial-curvature coefficient from changing only the tensor speed.
The F-weighted trace variance keeps its local kinetic ratio fixed even if
chi varies; the unweighted choice would introduce an additional finite-chi
kinetic degeneracy. Neither variance nor its first variation kills FLRW.

The full chi Euler equation, dividing by m N sqrt(h), is

\[
0=F(R^{(3)}+K_{ij}K^{ij}-K^2)
-4(D^2\chi+a^iD_i\chi+D_i a^i)-2a^2
+\frac{4F}{3}(K-\bar K_F)^2+\nu.
\]

The average's denominator must be varied. In its chi variation, the term
proportional to delta Kbar vanishes because int N sqrt(h)F(K-Kbar)=0.
The script independently checks the spatial derivative equation in one
dimension. The full metric functional equations are NOT yet supplied.

## 2. Static MOND and both potentials, independently varied

On the leading weak-field, quasistatic branch, the density is

\[
L_{stat}=m[(\nabla\Psi)^2-2\nabla\Phi\cdot\nabla\Psi
+f(|\nabla\Phi|)+2(\nabla\chi)^2
+4\nabla\chi\cdot(\nabla\Phi-\nabla\Psi)]-\rho\Phi.
\]

Independent Psi and chi variations give, with compatible boundary conditions,
Psi-Phi-2chi=0 and Phi-Psi+chi=0. Hence chi=0 and Psi=Phi on this branch.
The independently varied lapse equation then is

\[
\nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]
=\rho/(2m)=4\pi G_N\rho,\qquad G_N=(8\pi m)^{-1}.
\]

The spherical/Newtonian/deep-MOND consequences follow from this exact
constitutive function at leading weak-field order, not from an empirical fit.
Harmonic boundary modes and relativistic corrections are not silently
assigned. Full PPN gamma, beta, alpha1, alpha2, alpha3 are still uncomputed.
Ordinary minimally coupled matter retains its separate on-shell Ward identity;
that fact does not establish the gravity completion's covariance or causality.

## 3. Scalar, tensor and actual principal constraints

Retain the scalar spatial gauge coordinate E through the Legendre transform.
In a local orthonormal frame at leading weak potential, chi_bar=0 and K_bar=0,
but arbitrary finite y>0, put

\[
\alpha=e^{-y}(1-y\cos^2\theta),\quad
\mu_\theta=1-\alpha>0,
\quad K_{ij}=\operatorname{diag}(\dot z+k^2(B-\dot E),\dot z,\dot z).
\]

The code constructs, varies, and transforms

\[
L_2=\frac m2(K_{ij}K^{ij}-K^2)+\frac{2m}{3}K^2
+mk^2[z^2+2nz+\alpha n^2+2\chi^2+4\chi(z+n)].
\]

For k!=0, the calculated primary constraints are pn,pB,pchi. Preservation
gives alpha*n+z+2chi=0, pE=0, n+z+chi=0 (equivalent to the normalized
rows in the raw output). The computed six-by-six Poisson matrix has rank 4,
two first-class and four second-class constraints; the ten-dimensional
scalar phase space leaves ONE scalar pair. Preservation fixes the lapse and
chi primary multipliers and leaves the shift gauge multiplier free.
The code rebuilds the chains at alpha=1 (zero field) and alpha=0 (radial
turnover); the rank remains 4. The normalized generic row divided by
alpha-1 is NEVER used to infer the alpha=1 result.

The independent auxiliary spatial Hessian has determinant
8m²k⁴(alpha-2), nonzero throughout the exponential branch alpha<=1.
Thus the previous radial lapse zero at alpha=0 is no longer a singularity
of the **coupled** auxiliary system.

Eliminating the varied auxiliaries gives

\[
B=-\frac{3\dot z}{2k^2},\quad
n=-\frac{z}{1+\mu_\theta},\quad
\chi=-\frac{\mu_\theta z}{1+\mu_\theta},
\]
\[
\boxed{L_{red}=\frac{3m}{2}\dot z^2
-m k^2\frac{\mu_\theta}{1+\mu_\theta}z^2,
\qquad c_s^2=\frac{2\mu_\theta}{3(1+\mu_\theta)}.}
\]

This has positive scalar kinetic energy, positive gradient energy for y>0,
and 0<c_s²<2/3. Lean proves the inequality for every positive mu_theta.
At y=0, c_s²=0 but kinetic energy and the auxiliary constraint rank remain
nonzero. Nonlinear control of this zero-gradient limit is still owed.

The derived tensor kinetic matrix is (m exp(2chi_bar)/2)I, positive for
all real chi_bar, and its frequencies obey omega²=k². Other background
inhomogeneity corrections and the full nonlinear scalar health conditions
are not replaced by these principal results. No extra dynamical chi pair
appears in the computed blocks, but that is not a full nonlinear DOF theorem.

## 4. Exact homogeneous constraint analysis, not H=0 by fiat

For flat homogeneous FLRW the variance vanishes. With ordinary dust clock T,
whose momentum pT is conserved comoving matter mass, the gravitational
minisuperspace action and transformed total Hamiltonian are

\[
L_g=-3m e^{2\chi}A\dot A^2/N-m\Lambda NA^3+mNA^3\nu\chi,
\]
\[
H=N[-p_A^2e^{-2\chi}/(12mA)+m\Lambda A^3-m\nu A^3\chi+p_T].
\]

Primary pN,pchi,pnu preservation gives three secondary constraints. On their
surface,

\[
\chi=0,\qquad \nu=p_A^2/(6m^2A^4)=6H^2,
\qquad H^2=\Lambda/3+p_T/(3mA^3).
\]

The actual Poisson matrix, differentiated before imposing the surface, has
rank 4. All subsequent preservation residuals vanish after solving the
chi and nu primary multipliers; the lapse multiplier is arbitrary. There
are two first-class and four second-class constraints in ten-dimensional
homogeneous phase space: one remaining pair INCLUDING the dust clock.
No condition H=0 or pT=0 was introduced. nu absorbs the homogeneous chi
equation; it is not secretly an independently propagating scalar.

## 5. The next gate: positive wave speed is not enough for physical causality

The conserved-source action adds -n rho+z S+B rho_dot+E rho_ddot, S=tr(Tij).
The varied solution includes lapse and shift. Its physical linear Ricci
contraction is R00=-k²n+i omega k²B+3omega²z. The high-frequency limit
is (rho-S)/(2m), so the simplest instantaneous-response term actually cancels.
Stopping at that cancellation would incorrectly certify this candidate.

The source-free test removes the signed-external-source ambiguity altogether
at the level of the frozen principal system. Define the positive constant
spatial symbols

\[
q=k_\perp^2+k_\parallel^2,\quad
D=\mu_t k_\perp^2+\mu_l k_\parallel^2,
\quad \mu_t=1-e^{-y},\quad \mu_l=1+(y-1)e^{-y}.
\]

Let f be smooth with compact support. Choose initial data

\[
z_0=(q+D)f,\quad n_0=-qf,\quad\chi_0=-Df,
\quad\dot z_0=0,\quad B_0=0.
\]

These are local differential operators acting on f: all metric, auxiliary
and momentum perturbations initially vanish outside its support. The two
auxiliary constraints vanish exactly. The source-free equations give

\[
\ddot z+\frac{2Dq}{3(q+D)}z=0,\qquad R_{00}=qz.
\]

R00 initially and its second time derivative are local derivatives of f.
But its fourth time derivative contains

\[
\boxed{R_{00}^{(4)}(0)=\frac{4D^2q^3}{9(q+D)}f.}
\]

Exact polynomial division leaves
-4(mu_l-mu_t)^5 k_parallel^10/[9(1+mu_t)^5] over q+D.
The inverse of q+D has the anisotropic Coulomb kernel, differentiated ten
times longitudinally by the script. On the transverse axis at R>0, outside
the point-source support, the resulting kernel is

\[
\boxed{\mathcal K_4(R,0)=
-\frac{99225(\mu_l-\mu_t)^5}
{\pi R^{11}(1+\mu_l)^{11/2}\sqrt{1+\mu_t}}\ne0.}
\]

Here mu_l-mu_t=y exp(-y)>0 for every y>0. A sufficiently narrow smooth,
nonnegative compact mollifier preserves the exterior kernel's sign, so
the conclusion is not restricted to distributional initial data. Lean proves
the polynomial remainder's sign under its stated hypotheses; SymPy computes
the Green derivative and the isotropic control (zero tail if mu_l=mu_t).
If a smooth solution had a finite propagation cone, all its time derivatives
at an exterior point would vanish initially. This nonzero fourth derivative
therefore disproves that property for this constant-coefficient principal
system, despite its positive energy and subluminal phase speeds.

Scope matters: a regular nonlinear nonzero-gradient background, its global
mean constraint, boundary matching, and the perturbation lift have not been
constructed for THIS new action. The result is a principal causal obstruction,
not an already proved finite-amplitude global no-go or an observed signal.
Unlike earlier tests in other packages, no arbitrary external matter source
is needed for the displayed principal witness.

## 6. What survives and what genuinely has to change next

Bank the action-level stiffness repair, tensor matching, zero-mode multiplier,
and actual constraint calculations. They are constructive gains. The full
theory is NOT certified: causal propagation remains a failed principal gate;
nonlinear closure, clock restoration, PPN, strong-field behavior, zero-field
well-posedness and data-level viability remain incomplete.

The new bottleneck is explicit: the scalar evolution contains Dq/(q+D).
A next repair must remove its physical spatial inverse from curvature evolution
AND from minimally coupled matter response while preserving the static
source equation. Changing only the real wave speed or checking only the
high-frequency response misses the fourth-derivative tail. Making chi a
propagating field requires a new health/count analysis; its positive spatial
term is not a healthy dynamical scalar merely because it was a valid constraint.
No hidden zeroing of its homogeneous solution is a substitute for that analysis.

Run `python3 -B run_suite.py` here. The reproducible manifest pins the action
script, tests, Lean file and reused Dirac engine; raw output contains exact
commands, computed matrices, and exit statuses. The strict closure request
returns 2; ordinary audit success includes the causal failure being detected.
Early regressions failed before implementation. Two implementation defects
were corrected: a positivity assumption incorrectly excluded chi_gradient=0,
and symbolic dictionary keys required explicit JSON serialization. Neither
was fixed by changing a mathematical expected answer. The first full recorded
suite, `run_001`, failed because the new Lean real-division definition lacked
the required `noncomputable` marker, although its proof terms checked. That
failed historical run is preserved; its old input hashes are not current
evidence. The corrected full rerun is `run_002`, whose manifest and stdout
are the authoritative reproducibility record for these files.

Self-review: derivations and notation were checked by the authoring agent,
including the independent Green-kernel derivative and constraint residuals.
There is no external referee report or literature-wide novelty certificate.
