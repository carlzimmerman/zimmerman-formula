# Applying the local gate to an actual spherical equilibrium profile

2026-10-15. MC-HALO-001. Conditional weak-field static calculation. Base
`5c06d239febe644b9f485477b4c2f93390a23b3e`. Direct derivation and self-review;
no external theorem, empirical parameter fit or full halo-health claim.

**Result.** The assigned pure-chi dust equilibrium supplies a definite density
to insert into the principal gate. A finite baryon source scale can change the
point-source inner failure. For the finite-mass Hernquist family, an explicit
sufficient condition places every nonzero finite-radius point of the formal
occupied profile inside the RTM local principal domain. More compact members
can still fail that domain. Neither outcome supplies a regular origin, a finite
outer edge, settling, or a full metric/matter solution.

## 1. Hypotheses and the density identity

Take one critical species \(\chi\), \(q_\chi/m_\chi=\sqrt{4\pi G}\),
pressureless matter \(h=\rho_\chi c^2\), the assigned RTM electric law and a
spherical static leading Newtonian rest-mass comparison. Ordinary baryons are
outside the constitutive material frame. Neglect pressure, any additional
stiffness, relativistic corrections and the gravitational backreaction of
gauge-field stress. No portal remnant population or conversion is included.
The retained force balance is

\[
 u=\frac{GM_\chi(r)}{r^2}=a_0x,\qquad
 g_b=\frac{GM_b(r)}{r^2}=a_0\frac{x^2}{1-x},\qquad 0<x<1.
\]

Assume \(M_b(r)>0\) differentiable and \(M_b'(r)\ge0\) in the interval
considered, and define \(\alpha=d\ln M_b/d\ln r\ge0\). Differentiating
the force relation, rather than imposing a density independently, gives

\[
 \frac{r x'}x=\frac{(\alpha-2)(1-x)}{2-x},\qquad
 M_\chi(r)=\frac{a_0r^2x}{G}.
\]

Consequently the actual equilibrium rest density is

\[
 \boxed{\quad
 \rho_\chi=\frac{1}{4\pi r^2}\frac{dM_\chi}{dr}
 =\frac{a_0x}{4\pi Gr}
   \frac{2+\alpha(1-x)}{2-x}>0 .\quad}                       \tag{1}
\]

The pure-dust principal threshold from the pinned mode calculation is

\[
 \rho_{\rm crit}=\frac{a_0^2}{4\pi Gc^2}
                    \frac{x^3}{(1-x)^2},\qquad
 H=\frac{h}{h_{\rm crit}}=\frac{\rho_\chi}{\rho_{\rm crit}}.
\]

Substituting (1) and the force relation yields exactly

\[
 \boxed{\quad H(r)=\frac{c^2}{g_b r}
 \frac{(1-x)[2+\alpha(1-x)]}{2-x}.\quad}                    \tag{2}
\]

Thus the principal domain is tested on the equilibrium density, rather than
on a freely chosen \(h\). When \(H>1\), the engineered RTM magnetic-response
window is nonempty. This is only its local pure-electric principal criterion;
it does not establish stability of the static profile.

## 2. A sufficient bound for any nonnegative spherical baryon density

Write \(q=g_b/a_0\). For \(\alpha\ge0\), the last factor in (2) obeys

\[
 \frac{(1-x)[2+\alpha(1-x)]}{2-x}
 \ge\frac{2(1-x)}{2-x}
 =1-\sqrt{\frac{q}{q+4}} .                                \tag{3}
\]

The last equality follows by putting \(d=1-x\),
\(q=(1-d)^2/d\), with \(0<d<1\); both square-root branches are fixed by
positivity. The right-hand side decreases as \(q\) increases. If a source
satisfies \(g_b\le a_0q_{\max}<\infty\) and
\(g_b r\le V_{\max}^2<\infty\), then throughout its occupied interval

\[
 \boxed{\quad H(r)\ge\frac{c^2}{V_{\max}^2}
 \left[1-\sqrt{\frac{q_{\max}}{q_{\max}+4}}\right].\quad}   \tag{4}
\]

If the constant on the right exceeds one, the entire stated interval lies
inside the local gate. A smaller bound is inconclusive. The two maxima need
not occur at the same radius; using separate maxima makes the bound safely
conservative. This is an analytic bound, not an inference from radial samples.

## 3. An exact source family with an independent scale

Choose the finite-total-mass Hernquist enclosed baryon profile

\[
 M_b(r)=M\frac{r^2}{(r+b)^2},\qquad
 g_b=\frac{GM}{(r+b)^2},\qquad
 \alpha=\frac{2b}{r+b},\qquad M>0,\ b>0.
\]

Here \(b\) is an independent source-size parameter; it is not selected by
the galaxy-law relation. For every \(r>0\),

\[
 g_b\le\frac{GM}{b^2},\qquad
 g_b r\le\frac{GM}{4b},\qquad
 \frac{GM}{4b}-g_b r
 =\frac{GM(r-b)^2}{4b(r+b)^2}\ge0.
\]

Define the comparison scales and two dimensionless inputs

\[
 r_M=\sqrt{GM/a_0},\quad V_f^2=\sqrt{GMa_0},\quad
 B=b/r_M,\quad \epsilon=V_f^2/c^2.
\]

They obey \(GM/(bc^2)=\epsilon/B\). Bound (4) becomes

\[
 \boxed{\quad H(r)\ge L(B,\epsilon)
 =\frac{4B}{\epsilon}
  \left[1-\frac1{\sqrt{1+4B^2}}\right],\qquad r>0.\quad}   \tag{5}
\]

Thus \(L>1\) is a uniform sufficient local-domain condition. One may also
use a simpler rational bound. For \(z=\sqrt{1+4B^2}>1\),

\[
 L-\frac{8B^3}{\epsilon(1+4B^2)}
 =\frac{2B(z-1)^2}{\epsilon z^2}>0.
\]

Therefore

\[
 \boxed{\quad 8B^3>\epsilon(1+4B^2)
 \quad\Longrightarrow\quad H(r)>1\text{ for every finite }r>0.\quad} \tag{6}
\]

For example, the dimensionless *assigned* inputs \(B=1/100\) and
\(\epsilon=10^{-6}\) have \(GM/(bc^2)=10^{-4}\) and give the exact uniform
lower bound

\[
 H(r)>\frac{20000}{2501}>1 .                               \tag{7}
\]

This is an all-radius conditional witness for the formal equilibrium, not a
measured galaxy, a fitted baryon model, or a nonlinear evolution calculation.
At small \(B\), \(L\sim8B^3/\epsilon\); a finite scale does not guarantee
that the gate is passed for every source size.

An explicit failure member is also available without approximate root finding.
Take \(d=10^{-3}\), \(x=1-d^2\),
\(B=d/[2(1-d^2)]\), \(\epsilon=10^{-6}\), and \(r=b\). These choices
satisfy the exact force relation and give \(\alpha=1\) and

\[
 H(b)=\frac{4B}{\epsilon}
       \frac{d^2(2+d^2)}{1+d^2}<1 .                        \tag{8}
\]

Here \(GM/(bc^2)=0.001999998\); the failed local gate is not obtained by
silently choosing a relativistic mass length equal to the source scale. This
one-radius failure rejects the RTM local-response domain for that *particular
formal dust member* at that radius. It does not reject all finite sources or
prove a global dynamical instability.

## 4. Why the point-source and finite-source inner limits differ

For a point baryon mass, \(\alpha=0\), \(y=r/r_M\), and
\(1-x=x^2y^2\). Equation (2) gives

\[
 H_{\rm point}=\frac{2}{\epsilon}\frac{y^3x^2}{2-x}
 \sim\frac{2}{\epsilon}y^3
 =2\frac{c^2}{V_f^2}(r/r_M)^3\longrightarrow0
 \quad(r\to0).
\]

The point-source inner failure therefore follows from the assigned density,
in agreement with the retained RTM calculation.

For any fixed \(b>0\) in the Hernquist family, the central acceleration is
finite. Put
\(x_0=2/[1+\sqrt{1+4B^2}]\), so \(1-x_0=B^2x_0^2>0\).
As \(r\to0\), \(\alpha\to2\), and

\[
 \rho_\chi\sim\frac{a_0x_0}{2\pi Gr},\qquad
 H\sim\frac{2c^2b^2(1-x_0)}{GM r}\longrightarrow\infty.
\]

As \(r\to\infty\), \(x\sim r_M/r\), \(\alpha\to0\), and

\[
 \rho_\chi\sim\frac{a_0r_M}{4\pi Gr^2},\qquad
 H\sim\frac{c^2r}{GM}\longrightarrow\infty.
\]

These limits explain why a finite-source member can have a positive interior
minimum instead of the point-source inner failure. The limits \(b\to0\) and
\(r\to0\) cannot be interchanged: the point source is singular.

Every nonzero finite-radius point of the Hernquist carrier profile has positive
finite density, but its origin has a \(1/r\) cusp. The baryon Hernquist model
itself is also cusped. The divergent carrier density and undefined central
radial direction exclude the origin from a smooth-background principal proof.
The outer density tends to zero, yet \(M_\chi\sim(V_f^2/G)r\) diverges:
there is no finite carrier supply, finite halo edge or vacuum interface in this
formal family. A large outer \(H\) does not validate division by the current
at zero density or supply an exterior action. Regularizing the origin or
truncating the halo changes the field/density problem and must be checked by
its own equations.

## 5. Computation, provenance and the next gap

[check_profile_domain.py](check_profile_domain.py) uses exact symbolic algebra
to differentiate the enclosed mass and implicit force law, reconstruct the
Hernquist density independently, check both source bounds, check the rational
uniform bound and recover the point-source inner coefficient. It also checks
ten exact algebraic radial samples and three exact witnesses: the uniform
healthy member, a compact finite-source failure at \(r=b\), and a point-source
inner failure. The radial samples are implementation controls only; (3)–(6)
supply the all-radius argument. No ODE evolution, source data fit or approximate
eigenspectrum is run.

Inputs are the pinned copies `../inputs/RTM_REPORT.md` (SHA256
`1940b17de6e270567b2c0a9d617b9fc2d34c6cfd7b7228153a649fa51d761046`),
`../modes/PROOF.md` (SHA256
`d46b9a2b8adeb7d2692b29d6ac8d8283dfe6054eb619cc9686aa33e747d2b2ac`),
and `../inputs/source_manifest.json`. The run additionally pins this note and
its exact check script. See [computation_contract.json](computation_contract.json),
[run_exact/manifest.json](run_exact/manifest.json),
[run_exact/results.json](run_exact/results.json), and
[REPRODUCE.txt](REPRODUCE.txt). The manifest records actual hashes, command,
software, runtime and dirty state. Pinned mode files are not modified.

**Next unresolved implication.** The source-scale obstruction can be tested
analytically before a large computation, but local principal compatibility is
still insufficient for an admitted halo. The next candidate needs a regular
core and finite-supply edge with the same action, stress/flux matching and
matter/metric equations, then a finite-frequency/constraint and settling
analysis about that actual background. This calculation supplies none of those
missing steps, and it does not resolve the two-current remnant/portal problem.
The full theory goal remains open.
