# PF15 — diffuse singularities require a dynamical theorem

**The continuous/Cantor escape is neither eliminated nor established as a unique
native continuation. An extension is not proved necessary.** The calculation
below explains why the successful jump/sheet exclusions do not close it.

## What the native equations say about a Cantor part

[Diffuse singular identity](DIFFUSE_SINGULAR_IDENTITY.md) and
[independent audit](review/CANTOR_SYMBOL_AUDIT.md) use canonical BV approximate
values, so there is no freely chosen jump-product prescription. The on-branch
stress satisfies

    D_a^c T^a_b=-p_b D_a^c k^a+k^a(D_b^c p_a-D_a^c p_b).

The scalar equation and clock compatibility already make this vanish. Thus
stress conservation does not add a separate algebraic obstruction to diffuse
singular derivatives. This does not make the full Einstein equations redundant.

The remaining measure equations force acoustic polarization. The review also
checks the primary rank-one theorem: at almost every nonzero Cantor measure
point its normal is characteristic and its state variation belongs to one
acoustic family. This does not mean the support is a family of smooth curves,
and it provides no unique characteristic flow or propagation theorem.

These are necessary conditions, not a Cantor solution. They also show precisely
why the finite-jump convexity contradiction cannot simply be reused.

## Tested regularity route

[SBV theorem check](SBV_THEOREM_CHECK.md) verifies the actual assumptions of
Ancona–Caravenna–Marson's Theorem 7, arXiv:2409.06087v4. The result concerns the
specified viscosity/entropy solution with a sufficiently regular closed source.
AC2q's bounded auxiliary Jacobian does not establish those hypotheses or identify
its full Einstein evolution with that selected process. No Cantor exclusion or
native admissibility rule has been imported from it.

Even SBV plus no jumps would not by itself restore the strong theorem's bounded
derivatives. The [regularity countertest](REGULARITY_COUNTERTEST.md) gives an
explicit continuous W1,1 solution of a genuinely nonlinear scalar balance with
bounded source, no jump/Cantor part, unbounded derivative and nonunique classical
characteristic trajectories. It is NOT an AC2q solution, a PDE nonuniqueness
example, or a continuation from the incoming packet. Its role is to reject an
invalid shortcut from weak regularity to strong evolution/flow uniqueness.
[Independent countertest and source audit](review/REGULARITY_COUNTERTEST_AUDIT.md).

## Exact remaining mathematical obligation

The original weak equations and instantaneous auxiliary reconstruction are
well-defined in the declared classes. Their existence/uniqueness problem is
still open for the incoming terminal data. To close it, one must prove a native
one-sided/interaction or renormalized-flow estimate that controls continuous
and Cantor variation with the actual auxiliary/Einstein coupling, or construct
and verify a native weak evolution and its uniqueness/nonuniqueness directly.

The prebreak Riccati equation cannot be extended by squaring derivative measures.
Nor does algebraically allowing a nonzero acoustic Cantor polar show that the
PDE can generate it from smooth data. No such unsupported step has been used.

R1 resolves the diffuse principal identities and shows the stress consequence
is redundant there. R2's checked external theorem is not yet applicable. R3's
regularity shortcut is false at the abstract bounded-source level. The coupled
dynamical estimate and actual native construction remain deferred open routes,
not exhausted or proved impossible. The universal survival-versus-extension
verdict remains unachieved.

Research base a3aa3abdeb. Proofs, source checks and independent review records
are retained. No new numerical evolution, physical viscosity, or action term
was introduced. This is a partial research checkpoint.
