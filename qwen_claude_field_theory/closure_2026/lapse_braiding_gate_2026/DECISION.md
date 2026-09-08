# Changed-primary MOND audit: a constraint, not just a null kinetic direction

Base revision: `3f564b75dc48a0a5ac995fd46165b17e1d546e19`.
Status: **the proposed repairs are not a closed theory; the full research goal is OPEN**.
These are separate candidate screens, not a mixture of their favorable properties.
There is no global novelty claim or universal MOND impossibility theorem here.

## 1. Explicit physical-frame candidate and variation

Use c=1, m=M²>0, a timelike clock T, and its unitary gauge T=t.
The physical lapse is N=(-g^{μν}∂μT∂νT)^(-1/2)>0. Define

\[
 \widetilde g_{\mu\nu}=N^{2\eta}g_{\mu\nu},\qquad
 S_\eta={m\over2}\int\sqrt{-\widetilde g}(\widetilde R-2\Lambda)
       +m\int N\sqrt h f(s)+S_\sigma[g,\sigma]+S_b[g,x_A],
\]
\[
 s=h^{ij}D_i\ln N D_j\ln N,\quad
 f(s)=2a_0^2[1-(1+\sqrt{s}/a_0)e^{-\sqrt{s}/a_0}].
\]

Here S_sigma=−(1/2)∫√(−g) g^μν∂μσ∂νσ and
S_b=−Σ_A m_A∫√(−g_μν dx_A^μ dx_A^ν) are both minimal to physical g.
The static source diagnostic sets σ constant and retains the leading
nonrelativistic particle density. Expanding S_b gives −∫ρ_b Phi, with no
leading spatial source; the script differentiates this particle action.
Pressure and anisotropic stress must be negligible at this order. This is
not a claim that exactly stationary dust solves all its dynamical equations.
The homogeneous constraint diagnostic instead sets the particle density to
zero and retains σ: two specified sectors of the same action, not a massless
scalar treated as dust. These diagnostic limits are not a full matter mixture.
Λ is an optional seed cosmological constant; Λ=0 gives the zero-potential
seed. The map has tilde N=N^(1+η), tilde h=N^(2η)h and unchanged shift.
It is invertible only for η≠−1. The matter action is **not** the transformed
seed matter action: its constraint count must be recomputed.

`conformal_action.py` constructs the spatial Ricci tensor and extrinsic
curvature, then varies their quadratic amplitude expansion. At a local
static point with Nbar=1, hbar=δ, Kbar=0 and finite acceleration transverse
to k>0, put h=e^(2z cos kx)δ, δN=n cos kx, shift=v sin kx.
Frozen-background principal derivative order two gives

\[
 L_2=m\{-3(\dot z+\eta\dot n)^2+2kv(\dot z+\eta\dot n)
 +k^2[z^2+2(1+2\eta)nz+(2\eta+3\eta^2+\alpha)n^2]\},
 \quad\alpha=f_s=e^{-y}.
\]

This is an action-derived local principal model, not a solved global
background or the full nonlinear constraint system. Its complete equations
are Euler derivatives of this displayed Lagrangian. In particular its
independent static z and n variations, including source −ρn, give

\[
 z=-(1+2\eta)n,\quad \Psi=(1+2\eta)\Phi,\quad
 \nabla\!\cdot\{[(1+\eta)^2-e^{-y}]\nabla\Phi\}=\rho/(2m).
\]

The last equation is the leading weak-field static equation obtained by
retaining the full f and leading Einstein gradients; higher weak-field terms
are not asserted to vanish exactly. Independently measured at high acceleration,

\[
 G_{\rm measured}={1\over8\pi m(1+\eta)^2},\qquad
 \mu_{\rm measured}(y)=1-{e^{-y}\over(1+\eta)^2}.
\]

Thus the fixed normalization does not preserve the target law for general η.
No slip forces η=0; at that value the target exponential law is recovered.
The static ratio is **not** a full moving-source PPN calculation. No β or
α₁, α₂, α₃ values are assigned.

## 2. Actual nonzero-mode Dirac closure

Legendre differentiation derives primaries Ψ_N=p_n−ηp_z and p_v.
Set Z=z+ηn, P=p_z, Π_n=p_n−ηp_z, and b=1+η. The Hamiltonian is

\[
 H=-P^2/(12m)+kvP/3-mk^2v^2/3-mk^2(Z^2+2bnZ+\alpha n^2).
\]

Preservation derives secondaries C_n=2mk²(bZ+αn) and
C_v=−kP/3+2mk²v/3. In order (Π_n,p_v,C_n,C_v), actual Poisson
differentiation gives

\[
 \Omega=\begin{pmatrix}
 0&0&-2m\alpha k^2&0\\
 0&0&0&-2mk^2/3\\
 2m\alpha k^2&0&0&-2mbk^3/3\\
 0&2mk^2/3&2mbk^3/3&0
 \end{pmatrix},\qquad
 \det\Omega={16m^4\alpha^2k^8\over9}.
\]

The algorithm continues preservation weakly, obtains multiplier solutions,
and checks every residual. For α≠0 it closes with four second-class
constraints and no first-class constraints in this gauge-fixed scalar model:
(6−4)/2=**one scalar phase-space pair**. Neither rank nor count is input.
Solving both the mixed primary and the secondaries yields

\[
 \boxed{H_{\rm red}=mk^2(b^2/\alpha-1)Z^2,\qquad\dot Z=0.}
\]

The lack of P² does not remove the canonical pair. On α=b² the entire
quadratic Hamiltonian vanishes but the bracket rank stays four. This is not
evidence of a healthy scalar wave, a proven ghost, a nonlinear gauge symmetry,
or a complete nonlinear gravitational DOF count. It fails to supply the
regular scalar-removing mechanism sought here.

The independent α=0 control (η≠−1) recomputes four constraints, rank two,
two first-class and two second-class constraints, and zero scalar pairs.
It is a different constraint stratum, not substitution into H_red/α.
At the exact zero-acceleration point, α=1; η=0 still has rank four and
H_red=0 in the principal model. This does not settle nonlinear strong coupling.

## 3. k=0 recomputed before perturbing: physical matter matters

Let a denote the **transformed** flat FLRW scale, with physical scale a/N^η.
Since D_iN=0, f vanishes identically before variation. The exact homogeneous
Lagrangian and its actual Legendre transform are

\[
 L=-3ma\dot a^2/N^{1+\eta}-m\Lambda a^3N^{1+\eta}
   +a^3\dot\sigma^2/(2N^{1+3\eta}),
\]
\[
 H=N^{1+\eta}\mathcal A+N^{1+3\eta}\mathcal B,\quad
 \mathcal A=-p_a^2/(12ma)+m\Lambda a^3,\quad
 \mathcal B=p_\sigma^2/(2a^3).
\]

Primary p_N generates C=−H_N. On C=0, at η≠−1,

\[
 \boxed{\{p_N,C\}={\eta(1+3\eta)p_\sigma^2N^{3\eta-1}\over a^3}.}
\]

On a nonempty regular real branch with p_sigma≠0 and η outside
{−1,−1/3,0}, these two constraints are second class, preservation fixes the
lapse multiplier, and the homogeneous metric-plus-matter system has two
canonical pairs. This is an exact minisuperspace count, not an inhomogeneous
count. The real-branch condition is

\[
 p_a^2=12m^2\Lambda a^4+
 {6m(1+3\eta)\over1+\eta}{p_\sigma^2N^{2\eta}\over a^2}>0.
\]

For Λ=0 there is no such real branch for −1<η<−1/3. At η=0 the
separately recomputed constraints are first class, leaving one homogeneous
pair: the regular GR-plus-matter control admits expansion, not H=0 by decree.
At η=−1/3, C imposes A=0; further preservation imposes p_a=0, hence
Λ=0, but then dot p_a=3p_sigma²/(2a⁴)>0. No consistent p_sigma≠0
homogeneous branch exists. η=−1 is a singular map, not a loophole.
At p_sigma=0 the bracket changes rank; at also Λ=0, C=0 forces p_a=0
and the secondary differential vanishes. No regular count is inherited there.

## 4. Why an invertible lapse-dependent map is insufficient

For a general point map tilde h=C(N)h, tilde N=D(N)N, C,D>0, write
c=d ln C/d ln N, d=d ln D/d ln N and W=D√C. Actual curvature and
tensor variations give

\[
 t=1+d+c/2,\quad Q=c(1+d)+c^2/4,\quad
 \Psi=t\Phi,\quad t^2-Q=(1+d)^2,\quad c_T^2=D^2/C.
\]

The positive tensor kinetic coefficient is m C^(3/2)/D. For the Einstein
seed with no extra spatial operators, luminality on a connected lapse
interval gives D=√C and d=c/2; no slip then gives c=d=0. Moreover the
exact static density mN√h W[R/2+Q(N)s] has coefficients depending on
lapse, not acceleration magnitude. A point map alone cannot generate the
specified gradient constitutive law for arbitrary local profiles.

If C and D instead depend on s, curvature integration generates

\[
 c_s a^iD_i s+(c_sd_s+c_s^2/4)(D_i s)^2,
\]

where c_s=∂s ln C and d_s=∂s ln D. Under the same formal light-cone
matching, the second coefficient is 3c_s²/4, with principal quadratic term
3c_s²(a·k)²k²n². Such higher spatial derivatives cannot be silently dropped.
Their presence alone proves neither a propagating ghost nor invertibility
of this derivative-dependent map; a different constrained cancellation is open.

Separately, `transformed_lapse.py` pulls back the fixed physical f through
tilde h=e^(2w(N))h onto a separately audited affine-lapse seed. The canonical
one-form gives tilde p_N=p_N−2w_Nπ. The added Hamiltonian density is
−m√(tilde h)P, with P=N e^(−3w)f(e^(2w)tilde h^ij∂iN∂jN/N²).
At homogeneous lapse and tilde h=a²δ, direct functional variation gives

\[
 H_{NN}^{(f)}(k)=-2ma e^{-w}f_s(0)k^2/N\ne0\quad(k\ne0),
 \qquad f_s(0)=1.
\]

This breaks the inherited affine-lapse mechanism. The k=0 principal symbol
vanishes and does not supply a homogeneous count. The potential Hessian's
normalized longitudinal eigenvalue is (1−y)e^(−y), zero at y=1, whereas the
MOND operator's longitudinal eigenvalue is 1+(y−1)e^(−y), positive there.
They must not be conflated. At s=0 the script uses a fresh C¹ amplitude
expansion, not the singular f_ss(0).

The source routes checked were [Lin et al., v2, Eqs.72–77](https://arxiv.org/html/2011.05739v2)
and [Iyonaga et al., v2, Eq.84](https://arxiv.org/html/1809.10935v2).
We do not inherit their DOF count after adding f or recoupling matter.
In Lin et al. the step from a divergence-free tensor in Eq.86 to its vanishing
in Eq.87 is not used: divergence-free decaying tensors need not vanish.
The scripts note the trace-coefficient index mismatch and use standard ADM lapse.
This was a targeted source check, not an exhaustive novelty search.

## 5. Acceleration-dependent kinetic null vector: exact counterexample

A separate explicit attempt uses the physical metric, the same f, and
kinetic density mN√h(Q_ij Q^ij−Q²)/2 with

\[
 Q_{ij}=K_{ij}+A_{ij}F,\quad F=(\dot N-N^iD_iN)/N,\quad
 A_{ij}=\omega(N)h_{ij}+\eta a_i a_j/a_0^2.
\]

Actual velocity differentiation derives Ψ=p_N−2A_ijπ^ij. Full Euler
derivatives of the smeared primaries, including the metric dependence, give

\[
 \boxed{\{\Psi[u],\Psi[v]\}={4\eta\over a_0^2}
 \int{\pi^{ij}\partial_iN\over N^2}(v\partial_j u-u\partial_jv).}
\]

All local ω and metric terms cancel, but the gradient term does not.
This is not just a nonzero expression off the constraint surface. On a flat
three-torus take n>ε>0, P_0>0, a_0>0, η≠0, N=n+ε sin x>0,
ω=0, and only

\[
 \pi^{xx}=P_0\exp\left[{\eta\over a_0^2}
 ((n^2-\epsilon^2)/N-N+2n\ln N)\right],\quad
 p_N=2\eta\pi^{xx}(N'/N)^2/a_0^2.
\]

The script verifies Ψ=0 and the **full** spatial momentum constraints
H_i=−2h_ik D_jπ^jk+p_N∂iN=0. Nonzero smooth compact smearings u in
|x|,|y|,|z|<1/2 and v=xu give

\[
 \{\Psi[u],\Psi[v]\}=-{4\eta\over a_0^2}
 \int \pi^{xx}N'u^2/N^2\ne0\quad(\eta\ne0).
\]

The sign is exact; the sample integral −1.1502517578 is illustrative, not
the proof. Therefore weak self-commutation modulo these constraints is
refuted. This defeats the intended primary-consistency mechanism, not every
possible extended constraint chain. The symbol is −2iV·k; transverse k and
k=0 vanish at principal order. No blanket inverse or full DOF count is claimed.

## 6. Decision and the next unavoidable calculation

The complete-theory claim for these repairs is **not established**. The
point-map-only exact-law route is DEAD under its stated seed assumptions;
the added-f inherited affine mechanism and the tested gradient-null-vector
consistency claim are also falsified in their stated classes. The conformal
candidate remains unclosed, with explicit local extra-scalar data and
matter-coupled homogeneous obstructions. These results do not prove that
the original full target is impossible.

The next productive calculation is to solve for a **new scalar-removing
constraint and its Hamiltonian together**, keeping physical minimal matter
and the exact f fixed. It must cancel the computed lapse-potential functional
Hessian without resurrecting the nonzero primary self-bracket above. First
test its functional brackets on inhomogeneous data, then preserve every
constraint through closure, separately on homogeneous data. A cancellation
only on one background or a null velocity Hessian is insufficient.

An extra multiplier or a genuinely nonlocal spatial operator is outside the
classes excluded here; neither is a solution until varied and counted. Do
not spend effort on fitted PPN values or empirical victory claims before this
gate passes. Then the same surviving action still owes moving-source PPN,
full scalar/vector/tensor stability, physical causality, realistic FLRW and
controlled zero-field evolution. A fitted a0–Λ relation remains fitted.

Minimal canonical matter has its own diffeomorphism Ward identity
∇μT^{μν}=(Box σ)∇νσ=0 on its equation of motion; this follows from S_m[g,σ]
alone (S_sigma above) and does not cure a gravitational constraint failure.
The particle stress is separately conserved on the geodesic equations from
S_b; the leading static source truncation is not itself that Ward proof. No complete
nonlinear field-equation/Ward/PPN/stability certificate is being bundled into
the present screens. No evidence here establishes deliberate dishonesty by
another model or proves ΛCDM false.
