# A cold-rank reader still lacks bulk phase information

Claude's CFG355 adds a cold-stream covariance-rank veto to CFG354's tidal rule. That supplies information absent from a density-only reader, but not all the phase information needed to identify binding or escape. This is an exact Newtonian test-stream obstruction to a universal instantaneous binding classifier made solely from density/potential and central velocity moments. It is not a disproof of the frozen campaign's narrower sampled turnaround scores, or of a growing-mode-restricted construction.

## Actual input and comparison scope

Read CFG355_tidal_plus_rank_switch/FROZEN_CRITERIA.md at frozen commit 3f59dab1bec9d533a4dceed0f48c039ac05cce87 and its actual script. Its rule is `f=H(lambda2-tau) [1-(rank sigma_c==2)]`, with `sigma_c=sum w_s (v_s-vbar)(v_s-vbar)^T`. The campaign separately scores a particular Zel'dovich/host phase model; no independent rerun or authentication of those scores is claimed. Its declared cold-read permission changes the earlier density-only restriction. The present calculation respects that permission and asks which cold data remain missing.

## Translation lemma

At fixed spatial density and weights, replace every stream velocity by `v_s+U`, holding the host's rest frame and mass fixed. Then `vbar` changes to `vbar+U`, while each centered velocity `v_s-vbar` is unchanged. Consequently the full covariance, its rank, and every central velocity moment are unchanged. The instantaneous Newtonian Poisson potential and all its spatial derivatives also remain unchanged. This is a change of the cold flow relative to the host, not a common Galilean coordinate boost of both host and cold matter.

For the same positive tidal input above threshold, the CFG355 reader therefore returns the same value before and after this change. More generally, every deterministic reader built exclusively from those identical density/potential and central-moment inputs returns the same result. A bulk velocity, an appropriate relative-flow invariant, or a restricted phase-history premise is new information outside that input set. This does not assert that identical complete relativistic constraint data permit the change: momentum constraints include velocities.

## Explicit bound/escape witness

Use the static spherical Newtonian potential with positive vacuum repulsion

`U(r)=-mu/r-H^2 r^2/2`, `mu>0`, `H>0`.

Its maximum lies at `r_s=(mu/H^2)^(1/3)` and has value `U_s=-(3/2)(mu H)^(2/3)`. For angular momentum L, radial motion obeys `rdot^2/2+U_eff(r)=E`, where `U_eff=U+L^2/(2r^2)`. These follow directly from the central acceleration `rddot=-mu/r^2+H^2r+L^2/r^3`.

At r0=1 take mu=1, H=.1, and six equally weighted streams `v_s=+/- .2 e_i`, i=1,2,3. Their covariance is `(.2^2/3) I`, hence rank3. Every stream has E=-.985, strictly below `U_s=-.3231652035`. Since r0<r_s and `U_eff(r_s)>=U_s`, none can cross r_s. This is confinement inside the outer barrier; it does not guarantee a stationary distribution, prevent central collisions, or create a virialized halo.

Now add `U_bulk=2 e_r` to all six velocities at that point. Every radial velocity is positive. The least energy is .615. For every r>=r0, `U_eff(r)<=U_s+L^2/(2r0^2)`, and the largest L in this example is .2. The upper bound is -.3031652035, strictly below every shifted energy. No outward turning point exists: each shifted stream escapes the outer barrier. The covariance and every central moment are still exactly the same rank3 state. The density and tidal data remain identical at this instant, so the rank veto cannot distinguish these opposite outcomes.

This is an external-host/test-stream example. The strict finite energy margins persist for sufficiently small positive cold source perturbations, but no finite self-gravitating halo evolution or GR equality claim is derived here. One can localize the stream data in a small neighborhood of r0 with a smooth density and local frame; the inequalities remain strict by continuity. A global growing-mode restriction can exclude one of these initial states and thus evade the theorem by adding that restriction.

## Consequence for the research route

Rank is informative about stream geometry and can reject the ideal rank2 filament assigned in Claude's model. It cannot by itself establish physical binding or full three-axis turnaround for unrestricted cold flows. A phase-aware completion must specify what relative bulk information it reads, how it is evolved and varied in the same action, and why the intended initial-history restriction is physical. The ideal geometry scores, action legality, transition impulse and source conservation remain independent obligations.

This also connects to the recombination/growth lane: density and centered dispersion alone do not determine the late growing amplitude, which retains the bulk velocity-divergence transfer at drag. The exact linear transfer proof is in ../../recombination_and_structure_growth/growth_and_identity/REPORT.md. No cold particle identity, abundance selector, vacuum coupling or32pi coefficient follows from the rank addition.

## Evidence and scope

The proof above is analytic. checks.py verifies the exact covariance translation, six-stream energy margins and all-r>=r0 upper bound, with a negative control deleting the host-relative bulk change. A bounded finite calculation corroborates the explicit witness; it is not a universal proof by sampling. The run manifests pin this report, script and an archived copy of the frozen CFG355 criteria. No external theorem or new astronomical estimate is imported.
