# Existing attraction and the physical memory join

20 October 2026. Checkpoint `existing-attraction-2026-10-20`.

**Attractive contributions follow from the existing equations without a
new fitted coupling. They do not yet close the physical memory gap.**
This phase derives the actual interaction, distinguishes the relevant
occupations, and counts the positive terms that compete with attraction.
The [target contract](TARGET.md) fixes what a memory pass would require.

## The existing gravitational response

For a spatial transfer of a cold mass parcel `m` from outside to inside
an orbiting baryonic shell, the existing Newtonian and orbital energies
give

\[
 E_h(n,q)={M_hj_h^2\over2q^2}
       -{GM_h(M_0+mn+M_h/2)\over q}.
\]

The shell has positive radial curvature at
`q_n=j_h^2/[G(M_0+mn+M_h/2)]`. Eliminating it yields exactly

\[
 \boxed{\Delta^2E_h=-{G^2M_hm^2\over j_h^2}<0.}
\]

The interaction is the energy gained when the host contracts. `G` is an
existing coupling; host mass and conserved angular momentum are state
data. Neither is a newly fitted `J`. Conversely those state inputs have
not been specified by an inherited physical memory system, so this is
not a unique numerical prediction.

The [counted derivation](relaxation/RESULT.md) includes the outer stock's
orbital support, the tethered Newtonian self cancellation, nonzero
canonical stiffness, and the complete saturating remainder. It exhibits
a configuration where the attractive term dominates these energy costs.
It also bounds its magnitude: increasing the host mass cannot create
unlimited attraction.

The [supported continuation](relaxation/SUPPORTED_CONTINUATION.md) gives
the inner particles conserved circular actions and derives their energy
minimum. The [comparison proof](relaxation/BARRIER_PROOF.md) removes the
artificial support boundary: the profile stays compact by its own force
balance. This establishes radial support and positive shape energy in
the specified rank-preserving circular-shell model. It does not establish
stability against nonspherical or action-changing perturbations.

The [finite bounds](relaxation/BOUNDS.md) then give a constructive pass of
the energy test, with the full remainder and stiffness included:
`U_pair < -0.442 Gm^2/a` in the stated nonempty state range, while
`0<theta<=0.1 Gm^2/a` suffices for the inherited threshold. These numbers
are bounds for a constructed family, not selected physical measurements.
The same supported family has a necessary ceiling

\[
 \boxed{\theta<{8Gm^2\over27\ln2\,L_*}.}
\]

This ceiling follows from the stiffness and the maximum possible host
response under the common-support and fixed-action hypotheses. It
prevents treating arbitrary host susceptibility as a free enhancement.
In a separately justified thermal interpretation `theta=m sigma^2`,
the host bound also requires a parcel mass comparable to
`sigma^2 q/G`. The microscopic scalar mass and a collective parcel
mass cannot be interchanged in this test.

## What the other existing exchanges actually do

The [scalar calculation](scalar/RESULT.md) keeps both source exchange and
the original matched repulsive contact. Flat-space subthreshold pairing
fails. Existing gravitational confinement can reverse the interaction in
a specified mode projection; the exact charge-two/charge-four theorem
identifies when. But attraction between added charge-two objects is a
different observable from conversion at fixed inventory. In the literal
fixed-charge source-count basis, the bare curvature is `8 kappa>0`, and
the exact ground-state population cannot have two endpoint peaks.

The [existing phonon calculation](modes/RESULT.md) derives
`U_ex=-2 sum Re(g_1* g_2)/E` with no new vertex. A closed free-to-tether
change requires the *difference* of its two physical density sources.
For identical co-located densities that difference is zero, and so is
this attraction. A spatial conversion requires its actual overlaps and
complete energy; the sign is not universal. The general exchange
mechanism is known; [the primary-source comparison](modes/LITERATURE.md)
does not claim it as a discovery.

## Does it close memory?

For the inherited finite count `(1,4,2)`, the static hurdle is

\[
 E_2-2E_1+E_0<-3\theta\ln2.
\]

The gravitational construction can meet this *conditional energy test*.
Its geometry, angular actions and temperature are constructed state
inputs, and the count itself is not derived from those shells. A real
memory additionally needs one physical identification of free/tether
states, their allowed transition, a receiver that counts energy and
angular momentum, and a finite retention/release calculation.

The [conservation join](CONVERSION_JOIN.md) makes the decisive limitation
explicit: separately conserved tethered/free transport cannot change
those global stocks merely because an attractive density term lowers an
energy. Actual spatial capture remains possible and must be derived as
such. No lifetime, permanent one-way release, or S4 pass is inferred.

See [the bounded local delta](NOVELTY_DELTA.md) for what changes relative
to the nearest prior work. Proof reviews, exact symbolic checks, source
hashes, and the unchanged earlier packets are recorded in
`VERIFICATION.json` and `CHECKPOINT.json`. The two earlier phase packets
remain immutable; only this chat's live navigation pointer is updated.
