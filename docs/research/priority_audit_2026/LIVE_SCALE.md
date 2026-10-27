# Surviving scale claims: bounded follow-up

Checked September 9–10, 2026. Scope: fixed-half core, coupling ratio, and k04 environmental feedback—not inherited kernels or claims that a failed relativistic host is viable. Literature-check and proof-audit skills used; no physics files changed.

## Verdict: conditional on the stated reduced model

The coupling-ratio identity survives as standalone algebra. The environmental law needs a normalization correction even within that model. Neither establishes a surviving covariant theory or a first-principles half coefficient.

Local evidence: [k04 source](../../../kappa_closure/k04_four_form_promotion_consistency.py), its saved output, and [Paper 6](../../../qwen_claude_field_theory/papers_2026/PAPER6_kappa_no_go_2026.tex), especially “Reframing: the four-form promotion.” Source and output were inspected; numerical experiments were not rerun.

### 1. Fixed-half core and coupling ratio

For `a0=β√G|q|` and `P=(Z/2+bβ²)q²`, the stated four-form energy `ε=qPq−P` yields exactly

\[
\kappa^2=\frac{2\beta^2}{Z+2b\beta^2},\qquad
\kappa=\tfrac12\iff Z/\beta^2=8-2b.
\]

**Passed:** amplitude cancellation and ratio algebra. **Not established:** any principle fixing that ratio. These identities remain valid if their original host fails; physical applicability then requires another consistent host supplying their assumptions.

The elementary positive quadratic four-form energy is established prior art: Bousso–Polchinski (2000), [full primary v3](https://arxiv.org/html/hep-th/0004134v3), §2.1, equation (2.5). Coupling that flux specifically to the MOND scale is an extra project assumption, not supplied by that citation. Classification: known building block plus a conditional construction; exact external counterpart not verified in this search.

Closest recent comparisons do **not** reproduce the fixed half: [CKL v1](https://www.preprints.org/frontend/manuscript/6d93739261be0e369fb0b69d8cf228e9/download_pub), June 22, 2026, equation (4), implies `a0=c√(G〈rho〉/3)`; September 8 v2 equations remain unverified. [Singh v1](https://arxiv.org/html/2601.04290v1), January 7, 2026, equation (5), leaves `a0=c²/(ξ l_dS)` with ξ matched rather than computed. Both are adjacent, not exact matches.

### 2. Environmental feedback: omitted factor

Define `A=(2−KB)β²/(8π)`. k04 states

`q[Z+A(sΔ−j)]=Zq0`, `s=gN/a0loc`, `a0loc=β√G q`, `a0=β√G q0`.

On its positive, saturated branch, direct collection of q terms gives

\[
a_0^{\rm loc}=\frac{a_0-(A\Delta_{\rm sat}/Z)g_N}
{1-Aj_{\rm sat}/Z}.
\]

**Failed as an exact identity:** the quoted `a0loc=a0(1−gN/(155a0))` omits the denominator. k04 uses `jsat=0.4525`, not zero. The denominator differs from one by about 0.45% for its `KB=0`, `Z/β²=8` example. The zero-crossing threshold near `155a0` remains, but that number depends on these couplings and the saturated response.

**Conditional:** interpreting `q=0` beyond the threshold requires the nonsmooth `|q|` boundary treatment; the positive-branch algebra alone does not prove it. Transfer to another host requires rederiving its flux equation. These are the smallest missing implications, not reasons to discard the algebraic construction.

## Priority boundary

Targeted searches included `MOND "four-form"`, `MOND "four form"`, `"a_0" "four-form"`, `MOND "155" acceleration`, and MOND/flux/coupling-ratio/environmental variants. Exact k04 feedback was not authenticated elsewhere. This is a short English web-index search with old four-form primary-source checking, not global novelty or evidence of copying. The broader scale audit supplies dates and additional source coverage.
