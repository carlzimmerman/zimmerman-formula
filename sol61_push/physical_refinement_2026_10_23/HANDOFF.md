# Handoff: PR-20261023

Active objective remains formation of mass-selected bound cores with dwarf/rotation/growth compatibility. This phase completed finite spherical physical-radius refinement and matched-mode preparation-history tests; the overall theory objective is unresolved.

Start with RESULT.md, DERIVATION.md and AUDIT.md. `radial_v2.py` is the accepted local evolution implementation. Preserve `radial.py` and `base` as failed initial-preparation evidence. `analyze.py` integrates deposited aperture masses and computes explicitly insufficient Newtonian energy diagnostics. Commands, inputs, versions, bounds and hashes are in each run manifest. No simulations are left running.

Key results: .03 cold peak6.12583→6.13184 on256→512; reference-aperture mass25,552→25,370 solar masses. .05 peak2,659→9,504 while aperture mass436,666→434,356. Atz8 its aperture mass2,776,826: ongoing accretion, no plateau. The actual central concentration is below grid scale. Pure-cold control peak1.396, no crossings; pressureless baryonic focusing and the changed prepared state matter. Half-size seed aperture mass76,105; double-size fails chi guard beforez10. No selected mass catalogue.

Matched one matter mode fromz2200 gives20.1% different finalpeak; this is not a matched full-state or primordial transfer calculation. Thez4400 stationary branch is already strongly excited and guard-rejected. Do not simply loosen the guard or claim this proves impossibility.

Next discriminators: (1) derive a baryonic pressure/thermal evolution and cosmological field/metric preparation within a specified action; (2) carry the same prepared state through overlapping start epochs, matching velocities and all relevant modes instead of only one displacement projection; (3) implement physical refinement in nonradial geometry with action-consistent flux/deposition and a binding/escape diagnostic; (4) test a population and the large-scale growth benchmark before claiming dwarf, rotation or cluster preservation. Introducing gas pressure or a different background is a model extension that must be derived and labeled, not silently inserted into this run.

The strict null-force gate still fails from amplified floating point roundoff, but its null evolution stays homogeneous at3e-14. The null relative work gate also fails at essentially zero energy. All failed outputs remain. Metadata says Gaussian in some early contracts although the actual seed is a radial sine; see audit. No universal no-go result, full relativistic solution, empirical fit, or derived core abundance was obtained.
