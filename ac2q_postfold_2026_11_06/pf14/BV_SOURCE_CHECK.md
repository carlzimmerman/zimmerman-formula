# Source check: approximate-jump Rankine–Hugoniot

Checked 2026-11-06: Alberto Bressan, *One Dimensional Hyperbolic Conservation
Laws: Past and Future*, author-hosted notes dated October 20, 2023.
https://bpb-us-e1.wpmucdn.com/sites.psu.edu/dist/c/168431/files/2023/10/Erice-2.pdf

Definition 2.3 specifies an approximate jump by half-space L1 blowup.
Theorem 2.1, PDF pp4–5, states Rankine–Hugoniot for such a jump of a bounded
weak solution. The next displayed averaged-Jacobian identity identifies its
speed as an eigenvalue. Title, author and date were checked in the retrieved
PDF. No full text retained locally; no local source hash is claimed.

Application here freezes continuous auxiliary/metric coefficients at the jump.
The bounded source disappears in the rescaled equation. This extra reduction
is proved in BV_JUMP_EXCLUSION.md and independently audited; it is not a general
AC2q theorem supplied by the source. The BV rectifiable-jump derivative identity
or the same rescaling gives the stress and clock-compatibility relations.

Verdict: verified standard approximate-jump implication and notation translation.
No entropy/admissibility uniqueness or inevitability of shock formation is
imported from this reference. The internal Einstein/Bianchi regularity and
constitutive convexity arguments remain separate obligations.
