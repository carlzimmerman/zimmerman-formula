# ALC on-shell obstruction: the mimetic clock kills its own MOND source

The ALC action is

\[
S=\int\!\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
-\frac{\sigma}{2}(X+1)-2M^2a_0^2H(\sqrt{a^2}/a_0)\right]+S_m,
\quad X=g^{\mu\nu}\partial_\mu T\partial_\nu T,
\]

with \(n_\mu=-\partial_\mu T/\sqrt{-X}\) and
\(a_\mu=n^\nu\nabla_\nu n_\mu\).  Varying \(\sigma\), as the action
requires, gives \(X=-1\).  On that shell \(n_\mu=-\partial_\mu T\), hence

\[
a_\mu=-n^\nu\nabla_\nu\nabla_\mu T
       =-n^\nu\nabla_\mu\nabla_\nu T
       =\frac12\nabla_\mu(n^\nu n_\nu)=0.
\]

`alc_mimetic_acceleration_nogo.py` derives this identity from a symmetric
Hessian rather than asserting it.  Its linear static check uses
\(g_{00}=-(1+2\epsilon\Phi)\), \(T=t+\epsilon\tau\):

\[
X+1=2\epsilon(\Phi-\dot\tau),\qquad
\dot\tau=\Phi,
\]

and the acceleration perturbation is the spatial gradient of
\(\dot\tau-\Phi\), so it vanishes after the constraint is imposed.  For a
strictly static clock perturbation \(\dot\tau=0\), the same constraint forces
\(\Phi=0\) at this order.  A projectable lapse independently gives
\(D_i\ln N=0\).

The ALC correction is

\[
H(y)=2(1+y)e^{-y}-2,
\quad H(0)=H'(0)=0,
\]

so after the on-shell acceleration vanishes it supplies no linear MOND
source.  The previously derived AQUAL equation came from varying an
unconstrained static lapse; it cannot be combined with the \(\sigma\) equation
to describe the same solution.

This is an exact obstruction for the displayed mimetic ALC action, not a
universal no-go for a non-mimetic clock, a non-gradient carrier, or a different
auxiliary action.  The candidate status is therefore **DEAD_FOR_ALC_ACTION_AS_WRITTEN**.

Reproduce:

```text
python3 -B alc_mimetic_acceleration_nogo.py
python3 -B test_alc_mimetic_acceleration_nogo.py
```
