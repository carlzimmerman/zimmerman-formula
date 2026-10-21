# Common gravity is a real bridge, but not a static response gate

Coordinator derivation. Absence of a direct scalar-polarization vertex
does not mean that universal gravity cannot connect the sectors. This
note executes that continuation in the already specified reciprocal
two-population energy. No new portal or fitted susceptibility is added.

The static scalar susceptibility used below is an actual state-dependent
kernel, such as the condensate or gas response derived in `phases/RESULT.md`,
or an object's internal response in `multipoles/RESULT.md`. Identifying a
particular microscopic scalar population with the canonical released stock
is still a conditional dictionary. If the same mass is already represented
by `P`, adding it again as an independent density would double count it.

## 1. Count one nonzero real longitudinal mode

Take a stable supported patch and one nonzero spatial wave number `k`.
Use a real mode normalization common to all energies. Let `b,t,f` be
the baryonic source amplitude, tethered-density fluctuation, and ordinary
free-density fluctuation. They are signed fluctuations around positive
stocks, not negative total masses. Set

\[
 v={K\over k^2}>0,\qquad K=4\pi G.
\]

The existing Newtonian energy is `-v(b+t+f)^2/2`. The critical positive
tether self-energy is `+v t^2/2`; it is not applied to the ordinary free
stock. Suppose that free stock's *uncoupled material* static susceptibility
in this mode is finite and positive, `chi>0`, so its quadratic energy is
`f^2/(2chi)`. Denote by `C(t)` the actual canonical remainder/stiffness
contribution in the same mode, retaining the required background and
linear terms when expanding around a nonzero state. The counted control is

\[
 E(b,t,f)=C(t)+{f^2\over2\chi}
        -{v\over2}(b+t+f)^2+{v\over2}t^2.            \tag{1}
\]

This is the mode projection of the previous reciprocal energy and the
actual material response. It is not a new universal local pressure law.
The scalar response must have the same normalization and source variable;
one may not substitute a number compressibility for a mass susceptibility
without its mass factors.

Here `chi` is held at its actual background value in the linear-response
expansion. Differentiating (2) with respect to the mode amplitudes below
does not include uncomputed nonlinear changes of that background state.

## 2. Eliminate only a stable responder

The free-density Hessian is

\[
 D={1\over\chi}-v.
\]

A nondegenerate passive static elimination requires `D>0`, equivalently
`0<v chi<1`. Stationarity then gives exactly

\[
 f_*={v\chi\over1-v\chi}(b+t),
\]

and substitution into (1) gives

\[
 \boxed{E_{\rm eff}(b,t)=C(t)+{v\over2}t^2
       -{v\over2(1-v\chi)}(b+t)^2.}                 \tag{2}
\]

Two consequences are decisive. The mixed baryon-tether coefficient is

\[
 {\partial^2 E_{\rm eff}\over\partial b\partial t}
       =-{v\over1-v\chi},                           \tag{3}
\]

which is nonzero and has magnitude greater than the original `v`.
Stable positive susceptibility strengthens the ordinary attractive
feedback; it does not suppress or gate this source coupling.

The additional tether quadratic curvature is

\[
 \Delta C''=-{v^2\chi\over1-v\chi}<0.               \tag{4}
\]

It is an attractive feedback, not the missing positive critical restoring
term. For `t=div P_L`, the same correction written in polarization units is

\[
 \Delta E_{P_L}^{(2)}
       =-{K^2\chi\over2(k^2-K\chi)}|P_L|^2.          \tag{5}
\]

The full joint state also requires the remaining tether Schur curvature
to be positive; `D>0` alone does not prove coupled stability. Taking
`v chi` close to one makes a responder soft and can destroy that stability.
At or beyond the static Jeans denominator, (2) is not an admitted passive
elimination and cannot be called a large stable switching effect.

## 3. Insert the actual state responses rather than a fitted coefficient

For a finite-gap live bound object's COM-subtracted response,
`chi_int=O(k^4)`. Its contribution to `v chi` is `O(k^2)`, after a
consistent number-density normalization. It changes the long-wavelength
coupling by a derivative correction, not a local on/off mask. The
translating COM response must still be accounted for separately.

For the actual stable scalar condensate the static long-wavelength
material susceptibility is `m^2 q_mu>0`; a prescribed normal gas has
its own positive density susceptibility. Their different values change
the feedback. A finite-density normal state does not set the scalar
vertex to zero. An infinite homogeneous gravitating medium with such
a positive susceptibility loses the stable small-`k` static limit;
one must use a supported finite patch or the proper dynamics.

If the free density disappears, `chi->0`, (2) returns the original
canonical response. It does not turn that response off. To make the
static coefficient (3) vanish would require a different limit or
interaction outside the finite positive passive domain. A dynamic,
complex response can have resonances, antiresonances and noncommuting
limits; no theorem about every frequency or every driven state follows
from this static check. Such a state would require its actual kernel
and stability, rather than a universal permanent released-state label.

## 4. What this closes and what remains open

Common gravitational backreaction is an existing, calculable interaction.
It was not discarded merely because the scalar action lacks a direct
portal to the separate nodal sector. In this admitted static mode it
provides ordinary feedback and a possible instability, not a switch
between the desired response branches. A change of scalar binding or
condensation can change `chi`; it cannot make (3) vanish in the stated
stable domain.

This does not exclude more complicated nonlinear, nonuniform, finite-
temperature or driven states. It closes the specific proposed escape
of deriving the passive quasistatic on/off coupling solely by integrating
out the already responding scalar density. The physical state-to-response
dictionary and a different actual constitutive mechanism remain required.

Verification: direct finite-mode stationary elimination and source
accounting; no computation, fit or external theorem. Review provenance:
coordinator self-review, with separate reconstruction in `audit/RESULT.md`.
