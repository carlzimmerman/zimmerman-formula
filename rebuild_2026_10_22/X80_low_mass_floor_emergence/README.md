# X80_low_mass_floor_emergence (QUEUED; criteria c1c6d82d69)

**Question.** Does native collapse put cores on a₀/2πG at dwarf masses? If so, the floor of the route E core rule would
emerge rather than being put in by hand.

**Status.**
- The 10¹⁰ / 10¹¹ zooms are queued behind A5. `watch_A5_then_X80.sh` runs under nohup and checks every 10 min; its log
  is `watch_X80.log`.
- The script is pre-built. **K1 PASS:** on the committed 10¹² ng 64 halos it reproduces X77's η 20.83 and gives
  ρ₀r₀ = 134.9 M☉/pc², which is R = 1.26 canonical / 1.05 alt.
- **Setup smoke:** ng 32 for 3 steps, in scratch only. z_f is 1.326 at 10¹⁰ and 1.137 at 10¹¹; the latter matches X43's
  table.

**Files:**
- `x80_floor.py`: X77's fit, executed from X77's source; outputs `x80_results.json` and `_MUTATE`.
- `run_low_mass.sh`: 24 preemptible runs.
- `watch_A5_then_X80.sh`.

**Caveats.**
- The zooms are Newtonian, with no a₀ in the dynamics.
- Emergence would be a native coincidence of scales, not a derivation.
- κ = ½ FITTED; not theory closed.
