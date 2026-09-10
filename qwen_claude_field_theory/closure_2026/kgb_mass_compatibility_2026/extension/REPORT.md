# One conformal DHOST extension: verified static matching freedom

2026-09-10. Base: `9a088d45c9c3349de154446aeee4500a84f31c9a`.
Status: the extra static operator and its necessary inverse equation are
verified; a healthy shared extended solution remains open.

The selected extension adds one function of the existing physical clock:

\[
 S=\int d^4x\sqrt{-g}\left[
 F(X)\mathcal R+\frac{3F_X^2}{2F}(\nabla X)^2
 +P(X)-G(X)\Box\phi\right]+S_m[g],\qquad
 X=-\tfrac12(\nabla\phi)^2.
\]

The companion coefficient is fixed by degeneracy, not a second free function.
The old action is recovered at \(F=m/2\). Matter and light remain minimally
coupled to the physical metric \(g\), and \(\phi=qt+\psi(r)\), \(q\ne0\),
is the explicit clock. No dark matter particles or extra physical field are
introduced. This is the known \(A_3=0\) luminal quadratic DHOST subclass,
verified in [Langlois et al., equations (5)-(8)](https://arxiv.org/html/1711.07403v2)
and [Creminelli et al., equation (72)](https://arxiv.org/html/1809.03484v2).
Version, convention, and source hashes are recorded in `SOURCES.md`.

## Why this is additional physical matching freedom

The curvature sector is the Einstein-Hilbert action, up to a boundary term,
under the derivative-dependent conformal transformation

\[
 \widetilde g_{\mu\nu}=\frac{2F(X)}m g_{\mu\nu},\qquad
 \widetilde X=\frac{mX}{2F(X)},\qquad
 \frac{d\widetilde X}{dX}=\frac{m(F-XF_X)}{2F^2}.
\]

The map is locally invertible when \(F>0\) and \(F-XF_X\ne0\).
The transformed description has a changed matter coupling. Consequently this
does not remove the extra function while retaining the original minimal matter
coupling to the same physical metric. The scalar and tensor light cones must
always be interpreted relative to that specified metric.

There is an executable, stronger-than-parameter-counting discriminator. For
the original KGB action, the off-shell identity is \(p_r-pJ^r=P(X)\),
where \(p=\psi'\). Split off the constant Einstein term \(m\mathcal R/2\)
and call the new curvature contribution \(\Delta\). The calculation below
finds two local jets with the same \(X\) but different
\(\Delta(p_r-pJ^r)\): 0 and \(89/460\). Thus no redefinition of
\(P(X)\) or \(G(X)\), with the physical metric fixed, absorbs this operator.
This is a necessary source of new matching freedom, not a successful
cross-mass solution.

## Static reduced action and actual variation

Keep the area function independent before variation:
\(ds^2=-A(r)dt^2+B(r)dr^2+R(r)^2d\Omega^2\),
\(X=q^2/(2A)-p^2/(2B)\). Primes mean \(d/dr\).
After angular integration, suppress the common \(4\pi\) and time integral.
Integration by parts gives the curvature-sector radial Lagrangian

\[
 L_F=\sqrt{\frac AB}\left[
 2FB+2F(R')^2+2FRR'\frac{A'}A
 +F'\left(R^2\frac{A'}A+4RR'\right)
 +\frac{3R^2(F')^2}{2F}\right].
\]

The original curvature density equals this expression plus \(d\mathcal B/dr\),
where

\[
 \mathcal B=-\frac{FR^2A'}{\sqrt{AB}}
             -4FR\sqrt{\frac AB}\,R'.
\]

Add the unchanged KGB radial term
\(\sqrt{AB}R^2[P+G_X X'p/B]\). The script constructs the scalar curvature
independently from the Christoffel symbols and checks the integration-by-parts
identity. It then actually varies \(B\) and \(p\), including their radial
derivatives, before setting \(R=r\).

For \(K(X)=3F_X^2/(2F)\), direct scalar variation gives the additional current

\[
 J_F^r=\frac pB\left[F_X\mathcal R-K_X\frac{(X')^2}{B}-2K\Box X\right],
 \qquad
 \Box X=\frac{1}{\sqrt{AB}R^2}
 \frac{d}{dr}\left(\sqrt{\frac AB}R^2X'\right).
\]

The total current is \(J^r=J^r_{\rm KGB}+J_F^r\); it is this total current
that is set to zero. Reusing the old KGB zero-current equation would be wrong.

Define \(E_B^F=\delta L_F/\delta B\) and
\(J_F^r=-(\delta L_F/\delta p)/(\sqrt{AB}R^2)\). The independently varied
combination, in areal gauge, is

\[
 \frac{2BE_B^F}{\sqrt{AB}r^2}-pJ_F^r
 =-2F G^r{}_r-\frac{(2g+4/r)F'}B-\frac{3(F')^2}{2FB},
 \qquad g=\frac{A'}{2A}.
\]

The general identity also follows by varying \(B\to B+2B\eta(r)\),
\(p\to p+p\eta(r)\): this fixes \(X\) pointwise, hence fixes \(F,F'\).
All \(\eta'\) terms cancel. Exact Euler-Lagrange checks are performed for the
nontrivial invertible family \(F=F_0(1+\lambda X)\); an independent symbolic
check with unrestricted \(F,F'\) verifies the general combined equation.

Combining it with the KGB identity, negligible baryonic radial pressure, and
\(J^r=0\), the necessary radial equation becomes

\[
 2F G^r{}_r=P-\frac{(2g+4/r)F'}B-\frac{3(F')^2}{2FB}.
\]

Write \(h=F'/F\) and \(T=1+2rg\). Solving gives

\[
 \boxed{B=\frac{T+r^2(g+2/r)h+\tfrac34r^2h^2}
                     {1+r^2P/(2F)}}.
\]

This changes both the radial metric equation and the total scalar current.
The denominator must remain nonzero and \(A,B\) positive. Since \(F'=F_X\,X'\)
contains the clock derivative, this is an implicit inverse relation, not an
independent prescription for \(B\).
The formula reduces exactly to the previous KGB relation for constant
\(F=m/2\).

For the operator witness, choose \(A=B=R=1\), \(R'=1\), \(q=2\), \(p=1\),
\(A'=B'=0\), \(F_0=1/2\), \(\lambda=1/10\), and zero second jets.
Vary only \(p'\) between 0 and 1. Both jets have \(X=3/2\), \(F=23/40>0\),
and an invertible conformal map. Their curvature-sector corrections to the
KGB identity are exactly 0 and \(89/460\). These off-shell jets are a test of
operator independence; they are not claimed solutions or healthy backgrounds.

## Physical weak-field no-slip condition

Imposing the exact metric target \(B=T\) on the new radial equation gives

\[
 \boxed{\frac{P}{2F}=\frac{(g+2/r)h+\tfrac34h^2}{T}}.
\]

The script substitutes this pressure into the varied equation and obtains
zero. Thus no slip is a constraint on the shared functions and their radial
profiles; it is not obtained merely by naming a luminal theory.

For small \(rg\), \(rh\), metric potentials, and \(r^2P/F\), expand in a
single smooth weak-field ordering and introduce isotropic physical potentials
\(ds^2=-(1+2\Phi)dt^2+(1-2\Psi)(dR_{\rm iso}^2+R_{\rm iso}^2d\Omega^2)\).
The same angular and radial coordinate matching as in the lensing calculation
gives

\[
 \Phi'=g,\qquad \Psi'=g+h-\frac{rP}{4F},\qquad
 \Phi_W'=g+\frac h2-\frac{rP}{8F}.
\]

At leading order, equality of the physical slopes therefore requires
\(P=4F'/r\). The exact target \(B=T\) is not equality of nonlinear logarithmic
potentials beyond weak-field order. No slope ratio is identified with PPN
\(\gamma\), and no observational tolerance or complete ray integral is supplied.

## Conditional mode count and remaining gates

The source classification and invertible conformal relation supply a
conditional two-tensor-plus-one-clock mode count. It is not inferred from a
rank calculation of the radial Lagrangian. Seven application conditions are
kept explicit here; some are additional restrictions for this proposed use,
not all separate hypotheses quoted verbatim from the papers:

1. Four-dimensional local covariant metric gravity with the one scalar shown.
2. Smooth \(P,G,F\) and exactly the displayed companion coefficient; no omitted
   independent higher-derivative terms are silently included.
3. Finite \(F>0\), giving the positive tensor kinetic normalization of this class.
4. \(F-XF_X\ne0\), so the conformal map is invertible; singular mimetic limits
   are excluded.
5. A regular timelike clock patch \(X>0\), with the required coordinate maps valid.
6. The stated ordinary minimally coupled matter sector and consistent constraints;
   arbitrary derivative matter couplings cannot be appended without a new check.
7. A regular scalar kinetic branch, without accidental strong coupling or loss of
   the clock mode; exactly three propagating modes require this extra regularity.

The classification removes the additional Ostrogradsky scalar under its
conditions. It does not by itself fix the clock's kinetic sign or sound cone.
Those, the complete scalar-tensor principal matrix on the proposed spherical
background, vector/constraint evolution, full Dirac closure with matter, and
cosmological perturbations remain uncomputed. Tensor luminality does not
substitute for these checks.

The diffeomorphism Ward identity still links the metric Euler-Lagrange
divergence to the scalar equation; its new current must be retained. This
checkpoint has not varied the off-diagonal metric, checked its static flux
condition, or verified the independent lapse and angular equations of a shared
solution. The diagonal radial equation is necessary, not sufficient.
The boundary term above is recorded, but a well-posed boundary action, exterior
matching, center/horizon conditions, and common clock normalization remain open.

The old project `exceptional_branch.py` imposes a particular spacelike-gradient
\(1/r\) profile and bounded-\(F_X\) asymptotics. It does not evaluate this ticking
inverse. Conversely, its failure cannot be treated as evidence that the present
extension succeeds. The source's usual screened exterior approximation cannot
be imported at \(A_3=0\), and the selected conformal family does not automatically
inherit the quartic screening mechanism discussed in the source.

The next concrete test is a joint inverse for common \(P,G,F\) that solves the
new current and all metric equations while enforcing the displayed no-slip
pressure relation. Neither the existence of an extra function nor this radial
identity proves that such a system has an admissible solution.

## Reproduction

From repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/extension/test_extension.py
```

Seven exact SymPy tests pass. They check independently constructed curvature,
boundary equivalence, actual scalar/radial variation, coefficient translation,
operator independence, the constant-\(F\) limit, no-slip algebra, and the affine
conformal inverse. The bounded run and hashes are under `run_001/`; source-cache
verification also passes. Only files under this extension directory were
written, and this task made no commit or push.

Literature-check verified the known source parameterization; computation-audit
guided the independent variation and provenance; proofread-math self-review
covered the new equations. No full theory, empirical novelty, measured Newton
constant, or new dark matter particle claim is made.
