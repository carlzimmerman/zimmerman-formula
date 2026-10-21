# Shell arrival audit — committed amendments and provisional live results

Captured 2026-10-20; exact UTC, copied bytes and hashes are in `sources.json` and `snapshots/`. Repository read-only. No model, shell, field, control or sensitivity experiment was run. This is a scoped arrival audit, not a finalized verdict on either lane.

## Committed footing

- CFG935 criteria `38f4b6f18`, pre-result A0 `e9a824153`, and A1 `67999405006d326b5a8132212031f6c27bf91fa2` match their committed blobs exactly. A1 is an implementation/discretization amendment committed alone after failed S2 runs; criteria remain unchanged.
- CFG939 criteria `3524438b2`, pre-result A1 `7dace0a16`, and post-hoc A2 `92e2f0627d79e3ddc098c75fb02438218a8e0d32` match their committed blobs exactly. A2 discloses two failed-check runs, a finer-step Newtonian control and three report-only robustness runs. It does not move the primary C1 threshold.
- The examined scripts, derivations and result files in both lanes are live/uncommitted at this checkpoint. Their hashes identify the captured bytes only, not a published or finalized source revision. Individual outputs do not pin the exact script version that produced them. The copies preserve failed/old results alongside newer source without attributing every old output to the newest script.

## CFG935 A1: a genuine finite-shell barrier change

Write

    w(u) = -u^2/2 - a0 u - a0^2 ln(1-u/a0),
    w'(u) = h(u) = u^2/(a0-u).

The frozen step-shell outward force is `(r^2/G)[w(G(k+1)mu/r^2)-w(Gkmu/r^2)]`. At the outer step boundary `r_b=sqrt(G(k+1)mu/a0)`, it diverges only as `-log(r-r_b)`. Its approach work is finite because the logarithmic singularity is integrable. Thus a finite shell can reach the boundary of the action's domain at finite step-model energy. NaN energies from that continuation cannot support a physical escape or settling result.

A1 instead uses `F_mid=mu h(A_k/r^2)`, `A_k=G(k+1/2)mu`, with the discrete Hamiltonian

    V_mid = sum_k mu phi(r_k,A_k),
    phi = (A/r)[atanh(sqrt(x))/sqrt(x)-1], x=A/(a0 r^2),
    -d phi/dr = h(A/r^2).

This has logarithmically infinite potential at its own midpoint wall and a force proportional to inverse gap. The stated static quantiles follow from `h(u_law)=g_b`. The source's force and energy now use this same midpoint model. The adaptive step also limits inward motion relative to the midpoint wall and flags its minimum-step floor.

**Restriction:** the new rule is a different finite-N Hamiltonian and capacity domain, although it is a mass quadrature for the same smooth continuum functional. Indeed,

    (1/G) integral r^2 w(G m(r)/r^2) dr
      = integral dr integral_0^m(r) h(G m'/r^2) dm'.

For step-shell mass, each mass interval is integrated exactly in the frozen model and sampled at its midpoint in A1. That approximation is regular away from the singular wall; it is not uniform at the wall. The old first wall uses `(k+1)mu`, the new one `(k+1/2)mu`. It is therefore too strong to treat the midpoint model's infinite finite-particle barrier as an already demonstrated continuum convergence result. N refinement and minimum-capacity-gap diagnostics are the relevant future checks. No such experiment was duplicated here.

Captured `Ra2_I` and `Ra2_S` still have literal string `"nan"` energy errors and `conserves_1e3=false`; the recorded escape fractions0.3838/0.2392 are inadmissible as valid conservative results. A1 explicitly disowns those failed runs. The static `Ra2_L` control is finite, but does not validate the failed infall/surplus cases. The captured MUTATE file has `all_bite=false`; exit0 means the teeth did not all bite under this lane's exit convention, not success. The runner's `rc0` lines are also unreliable because `$(date)` can reset `$?`, as A1 discloses. There is no finalized normal aggregate/README in the captured inventory.

A0's earlier energy correction remains important: zero-energy escapers give an **upper** escape fraction compatible with a law remnant, not a positive minimum. Conservation still requires a booked destination for excess energy; a changed finite-shell barrier is not itself a cooling reservoir. These models conserve shell mass, not the alternative scalar action's independently normalized U(1) charge.

## CFG939 A2 and current provisional arithmetic

The frozen C1 labels are threshold diagnostics, not direct tests that the force switched off:

| Captured run | K | m/m_law at2,5 | C1 | S4 text |
|---|---|---|---|---|
| First dt0.005 |9/10, fails K5c |0.997684,0.965851 |TETHERED AFTER CROSSING |NOT DERIVABLE, unreadable while K fails |
| Second dt0.00125 |10/11, fails K5c |0.998928,0.949087 |UNTETHERED |UNDETERMINED |
| Current live main, finer control |11/11 |0.998928,0.949087 |UNTETHERED |UNDETERMINED (UNTETHERED) |

The latest main's K booleans independently count11/11 and its C1 label follows the unchanged0.95 boundary: m5 misses it by0.000912626. A2 appropriately calls this BORDERLINE-SENSITIVE and declares report-only dt0.0025, dt0.000625 and a6000-time-unit run. No completed A2 result file is present in this captured inventory; the route remains reserved/live. The current JSON still names only A1 in its header, so its association with A2's control fix rests on the captured source and matching control change, not a self-contained run manifest.

C2(a) remains0.445 for frozen E_tf,0.444 for own-rank E_q and0.0135 for actual ESC. The >=0.9 condition for S4 DERIVED fails. The narrowly UNTETHERED C1 label also prevents the stated NOT-DERIVABLE class, yielding an unassigned/undetermined primary result rather than an S4 derivation. The analytic fact that the action sources P from the total current supplies no automatic stream-dependent switch in coupling; it is separate from the brittle C1 grade.

The live derivation text is stale relative to the newer JSON: it still prints C1 TETHERED and S4 NOT DERIVABLE and older numerical values. Do not promote that draft text over the captured result history or amendment.

## Receiver and barrier cautions shared by the lanes

Current939's infall has a possible **outbound receiver**:43.8% of shell mass is beyond R0 with outward velocity and positive own-rank energy, carrying kinetic energy0.541706. Its actual ESC predicate is much stricter: beyond10R0 and outward, only1.35% at the finite endpoint. Thus the43.8% number must not be called completed asymptotic escape. E_tf is frozen-configuration test-element energy, not a per-element conserved energy of a changing multistream field; E_q is invariant only before rank changes under the stated single-stream assumptions. The receiver is still tethered cold medium in this model, not an independently derived free, self-gravitating population or a galaxy-normalized wind.

The captured939 spherical implementation also still uses the exact step-shell Wdiff energy/force, and clips `s_out>=1` to `1-1e-12` in acceleration. It has not adopted935A1's midpoint model. There is no clipping-count/minimum-wall-gap output in the inspected result. Occurrence is unknown: global endpoint energy and intermittently sampled force checks do not alone establish avoidance of that singular wall. This is a concrete finite-N implementation sensitivity to preserve alongside the inner-reflection and C1 time-window sensitivities, not proof that the new run is invalid.

Neither committed amendment nor these provisional numerics provides the four-dwarf retention selector, physical energy/charge normalization, galactic angular-momentum export or survival closure. The actionable advance is identifying which Hamiltonian and receiver are being tested, while excluding NaN results and unstable operational labels from the claim ledger.
