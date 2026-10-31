# LC1_live_contraction: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** What does a disc growing in a live zoom do to the cold fluid at 10¹², with gravity only? "Contraction breaks SPARC" (CN1: Υ 0.31 Blumenthal, 0.34 Gnedin) rests on spherical formulas, and they're limits. Argon asked for this direct test as its GD1 (Lane 5). The id GD1 is taken, so it's LC1. ZK1's kernel makes it about an hour's work.

**Standing.** κ = ½ FITTED. Newtonian, gravity only, no feedback. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework.

## Runs
- Seeds 1–9 at 10¹², ng 64, continued from X48's `snap_zf.npz` (z_f 0.944) to z = 0 with ZN1's engine, plus a disc. ZN1's same-seed 10¹² runs are the no-disc pairs.
- **Disc:** Miyamoto–Nagai, a = R_d, b = 0.2 R_d (a Kuzmin disc with a = R_d has an exponential disc's half-mass radius). No bulge.
- **M_d:** EM1's relation at M200 = f_c × 10¹²: lg M_d = 10 + (lg(f_c 10¹²) − a)/b, with EM1's a, b. Fitted relation, disclosed.
- **R_d:** median SPARC Rdisk among galaxies within ±0.2 dex of lg M_d, from the record.
- **Growth:** linear in time from 0 at t(z_f) to M_d at z = 0.
- **Mass conservation:** the disc is taken from the particles evenly: m(t) = m [1 − M_d(t)/M_sim].
- **Placement:** the disc's centre follows X48's `centre` every 10 steps. Its axis is the angular momentum of particles inside 0.1 r_vir at z_f, then fixed. It feels no back-reaction.
- Same softening and step rule. The disc's force enters the step rule. Snapshots at z = 0.5, 0.25, 0.

## Read-outs at z = 0, by same-seed pairs, median over seeds
- **Q(r) = N(<r) with the disc / N(<r) without,** at r/R_d = 1, 2, 3, 4, 6, 8, 10.
- **R_live = S with the disc / S without,** S = ρ₀r₀ from X77's smooth-core fit on [r_conv, r_vir].
- **Blumenthal's and Gnedin's Q(r)** computed on each seed's own no-disc profile with the same M_d, the disc's spherical mass taken as M_d [1 − a/√(r² + a²)], and the particles' mass fraction as above.
- **f_Q = median over r/R_d = 2, 3, 4 of (Q_live − 1)/(Q_Blumenthal − 1).**

## Verdict (headline: Argon's lines, frozen here)
- **WEAK:** R_live ≤ 1.25.
- **STRONG:** R_live ≥ 1.45.
- **INTERMEDIATE:** otherwise.
- Beside it: **BLUMENTHAL HOLDS** if f_Q ≥ 0.8, **PARTIAL** if 0.4–0.8, **WEAK RESPONSE** if below 0.4.
- Fewer than 6 finished pairs: UNDECIDED.

Argon's own fail line says R_live ≥ 1.45 confirms the Blumenthal failure in 3D. I'll score that as stated. S from the smooth-core fit may not track inner contraction well, so Q(r) is reported in full.

## Reported, not graded
- SPARC's line with CN1's contraction scaled by the measured f_Q: Υ on both backgrounds, ΔV by V_flat. That carries one number from 10¹² across SPARC's masses, disclosed.
- The same at z = 0.5 and 0.25.

## Checks
- **K1:** M_d = 0 reproduces ZN1's engine exactly over 20 steps: |d| ≤ 1e-12 relative.
- **K2:** the disc's analytic force against a numerical gradient of its potential at 1,000 random points: ≤ 1e-6 relative.
- **K3:** my Blumenthal code reproduces CN1's `contract` on a test profile: ≤ 1e-6.
- **MUTATE:** M_d × 2 on one seed must move Q(3 R_d) − 1 by more than 30 %.
- Any K failure: no verdict, exit 1.
