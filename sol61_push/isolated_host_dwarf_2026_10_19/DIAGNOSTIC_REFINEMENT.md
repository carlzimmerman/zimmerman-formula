# Remnant-centre correction and additional precision check

The v1 dynamics, source hashes, contracts and completed outputs are preserved. No force, collision or initial-condition parameter is changed by the remnant-centre correction.

After strong tidal stripping, the v1 stellar shrinking-sphere centre is unreliable: it retains at least one quarter of all original stars, including debris. The baseline host final snapshot reports zero cold mass at that displaced centre, while a cold-density peak contains about2.4million Msun inside300pc and nearby stars. Zero at the original centre must not be interpreted as destruction of every remnant.

Use an independent potential/density remnant diagnostic on the saved particles. An observational replay may replace only the centring/recording routines and save full100Myr snapshots plus per-particle accumulated host work/torque. Verify the replay's initial and final particle positions/velocities are bitwise identical to v1. This separates diagnostic repair from physical evolution.

The isolated cloud's100pc structure is only2.5baseline softenings across. A separate epsilon20pc, dt1Myr run at the baseline particle count is added; compare it to the existing dt1Myr/epsilon40pc control. This is a numerical precision check, not a different physical interaction or tuned target profile. Its code/arguments are in launch_extra.py, with an independent run manifest.

At most one additional single-thread worker is used beside the original sequential suite; every process remains low priority. This uses bounded small-memory experiments and leaves unrelated live jobs untouched.
