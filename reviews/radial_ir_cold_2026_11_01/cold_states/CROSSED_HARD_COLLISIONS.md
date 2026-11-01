# Crossed hard annihilation check

This finite continuation is authorized by the coordinator and leaves the
frozen soft evidence unchanged. Use the independently reconstructed
one-loop heavy bundle majorant in
`gapless_charge/decay_bound/DERIVATION.md` and its run_001 result. No new
box is claimed: this is crossing the same bounded 1PI four-point class
into chi chi -> two unbroken gauge bosons in the leading NR limit.

Both external gauginos are now the normalized U1 generator. The author
norm bounds apply to every normalized unbroken external gaugino, and all
internal lines still carry nonzero U1 charge. The external momenta and
any routed sum are at most2m, far below the common charged gap; the
author's factor2 continuation envelope remains ample. Each external
spinor norm is sqrt(2m), and the two outgoing gauge momenta have Euclidean
norm sqrt(2)m. Thus the same pointwise amplitude bound applies:

    |M| <= 4 B_loop m³/Mcharged³.

The sum over final vectors and polarizations is at most12²×2²=576;
overcount it by the decay proof's32768. Averaging the four initial spins
does not increase a uniform bound. Drop all identical-final suppression.
At threshold sigma v_rel= sum|M|²/(32pi m²), so

    sigma v_rel <= 16384 B_loop² m⁴/(pi Mcharged⁶)
                <= c7_eff_bound² m⁴/(pi Mcharged⁶),

where c7_eff_bound=512 B_loop. The last inequality adds a factor16 of
margin. It also covers the vanishing or additionally suppressed channels
without assigning them a nonzero physical coefficient.

This is a bound on the named leading heavy one-loop annihilation class,
not every thermal or nonperturbative process. The scalar arithmetic run
uses the same explicit local density .3GeV/cm³ and1MeV,e=.003 state.
The phase-pair annihilation bound is independent and already in run_soft.
No thermal average or production rate is inferred. One thread, wall30s,
CPU25s, measured RSS below1GB, no new dependencies or outside edits.
