# A regular coupled source branch cannot have a leading square-root response

Base `81af81ba8a7207bca2bc4f13375c757feee7afcd`. This is a general conditional statement about a **coupled** local source problem, extending the earlier fixed-linear positive-pole test. It is not a statement that physical health implies a regular static inverse, or that MOND is excluded.

## Precise statement and proof

Let u collect all metric, matter-response and auxiliary fields after a declared gauge choice and elimination or retention of constraints. On a fixed finite spatial domain with fixed admissible boundary/initial prescription, write the source equations as E(u,M)=0, where a smooth baryon density shape is multiplied by its mass M. Work in Banach spaces U,V for which E:U×R→V is C¹ in a neighbourhood of (u₀,0), E(u₀,0)=0, and A=D_uE(u₀,0) has a bounded inverse V→U. Let the measured source-induced acceleration B(u,M) be C¹ into an observable space and B(u₀,0)=0. Evaluation at an exterior test location must be a bounded operation in that space; distributional point sources are not assumed.

The local implicit-function branch is C¹ and

    u(M)=u₀−M A⁻¹D_ME(u₀,0)+o(M),
    B(u(M),M)=M[D_MB−D_uB A⁻¹D_ME]+o(M).

In particular B=O(M). It cannot equal a nonzero leading C√M+o(√M) as M→0⁺ at the fixed test location. A zero linear coefficient strengthens the exclusion rather than giving √M: C¹ still implies B=o(M) in that case.

For completeness the local inverse follows without assuming a global elliptic theorem. Put h=u−u₀ and R(h,M)=E(u₀+h,M)−Ah. The equation is the fixed point h=−A⁻¹R(h,M). Continuity of D_uE makes this map a contraction in a sufficiently small fixed neighbourhood, since its h derivative vanishes at (0,0). A ball whose radius is proportional to |M| is invariant for small |M| because R(0,M)=O(M); this establishes h=O(M). Difference quotients in E then give the displayed derivative. The standard C¹ implicit-function theorem packages the same local argument. None of it assumes linear equations away from the background.

The general-d sourced MOND law g²/a₀=G_N M/r^(d−2), with positive fixed a₀,G_N and fixed r, has exactly the excluded √M leading behaviour. If instead one continues flat rotation curves to arbitrary d by a different nonlinear power, the corresponding fractional mass power is excluded whenever it is below one. This statement involves neither ħ nor a selected numerical coefficient.

## What can invalidate the hypotheses

A gauge zero mode is not automatically a physical critical mode: gauge and boundary ambiguities must first be removed. Conversely a nondynamical constrained field can have an invertible elliptic static operator, so merely removing its propagating degree of freedom does not evade the proof.

Possible genuine escapes are a zero/unbounded-inverse static mode, a nonsmooth equation or observable, a source-dependent boundary or cosmological matching prescription, or a nonuniform limit in radius, source size, evolution time or spatial volume. Multiple branches or a transition can matter; the theorem applies only to the regular branch attached to the specified source-free state. Near-zone equations must be derived before assuming their inverse exists. Positive cosmological kinetic energy by itself establishes none of these static premises.

An external-field MOND branch often has a linear response for sufficiently small additional mass, consistent with this result. The theorem does not exclude a finite nonlinear MOND window, empirical galaxies in that window, or a response studied by sending r→∞ together with M. A full de Sitter matching may also stop a static approximation from existing to arbitrarily large radius. These are different limits and require their own source/boundary analysis.

## Exact crossover control and its interpretation

As an explicitly restricted scalar constitutive example, let

    L_static=−[ε|∇Φ|²/2+|∇Φ|³/(3a₀)]/(Ω_(d−2)G_N)−ρΦ,
    ε>0, a₀>0.

With the isolated radial flux branch, define g=|Φ′|, b=G_N M/r^(d−2). The equations give

    εg+g²/a₀=b,
    g=(a₀/2)[sqrt(ε²+4b/a₀)−ε].

This is a low-acceleration mathematical control, not an interpolating theory calibrated at high acceleration. Its ε=0 branch is the cubic MOND equation; its ε>0 branch has a positive static quadratic stiffness at zero field. At fixed ε,

    g=b/ε−b²/(a₀ε³)+O(b³).

The logarithmic source susceptibility is

    d ln g/d ln b=(ε+g/a₀)/(ε+2g/a₀),

which changes from 1 to 1/2. Let x=g/(εa₀). Then b=ε²a₀ x(1+x). The quadratic and cubic flux terms are equal at x=1, b=2ε²a₀. In the cubic limit ε→0 first, g=√(a₀b); in the weak-source limit b→0 at fixed ε, g is linear. Thus the two limits do not commute for g/√b.

There is an observable finite-window consequence independent of a fitting convention. Relative to pure MOND at the same b,

    g/√(a₀b)=sqrt[x/(1+x)].

Requiring a fractional deficit at most δ, 0<δ<1, at a measured minimum b gives

    x≥(1−δ)²/[1−(1−δ)²],
    ε≤sqrt{b/[a₀ x_min(1+x_min)]}.

This bounds a residual linear stiffness in this stated constitutive model. It does not bound every relativistic theory's cosmological kinetic coefficient or identify ε with H/a₀. Such a relation needs the same action's constraints and measurement dictionary.

## New decision this screen supplies

The algebraic-source exclusion from the previous phase leaves additional fields as a real escape. Their existence alone is insufficient: each proposed coupled rolling state must show where its static source inverse loses regularity, or identify the actual finite MOND window and its matching scale. This discriminator is being applied to cuscuton, generalized aether and kinetic-braiding candidates. A degeneracy can enable a fractional force law; it does not itself select its normalization or the vacuum curvature. Those remaining obligations retain the original 32π target.

`regular_response_checks.py` corroborates the radial equations, susceptibility and tolerance conversion only. The Banach-space result above is a separate proof with explicit hypotheses; finite arithmetic cannot establish inverse bounds for a candidate gravity theory.
