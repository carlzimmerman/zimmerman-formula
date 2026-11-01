# PZ1_disc_during_collapse: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** LC1_live_contraction grew a disc in the live zoom from z_f to z = 0 and found f_Q 0.872 [0.54, 1.07], BLUMENTHAL HOLDS; R_live 2.154 [1.65, 2.52], STRONG. Its disc starts after the half-mass object has collapsed. Does a disc that starts growing at turnaround, so that it is present during violent relaxation, change f_Q or R_live?

**Record check.** No lane has grown a disc before z_f. LC1 starts at z_f. RM1 maps response strength and doesn't run zooms. reviews/three_priorities_2026_11_01/spin_contraction reads LC1's snapshots and runs no new zoom. This is untested.

**Standing.** κ = ½ FITTED, unused here. Newtonian, gravity only, no feedback. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. No new free number enters: turnaround is measured from the run, and the growth law is LC1's with its start moved. The law itself is a stated choice, not derived and not scanned.

**Not blind.** LC1's results, its per-seed numbers and the SPARC scaling are known to me before this was written.

**Expectation on record.** Little change: the disc holds little mass early, and LC1's ratio rises 1.47, 1.75, 2.15 from z = 0.5 to 0. Against that, this law puts more disc mass in earlier than LC1's at every time before z = 0, so a change in either direction would be a real result.

## Runs
- Seeds 1–9 at 10¹², ng 64, plus MUTATE and null runs below. Same initial conditions as X48 (`constrained_field`, z_i 40), same softening, same step rule with the disc's force in it, same compiled force kernel (ZK1), same M_d 6.72e10 and R_d 3.565 kpc (`LC1_live_contraction/lc1_setup.json`), one thread, nice 15.
- **Turnaround, from the run.** T = the particles with Lagrangian |q| ≤ q_M, the M/2 object whose collapse defines z_f. R_T(t) = their mean physical distance from their own centre of mass, sampled every 10 steps. t_ta = the sample where R_T is largest. It is found in the disc-free run: when R_T has fallen 0.2 % below its running maximum, the run goes back to the stored state at the maximum and the disc starts there. Each seed gets its own t_ta. Before t_ta each run is the disc-free engine.
- **Growth law.** LC1's, with its start moved: M_d(t) = M_d (t − t_ta)/(t₀ − t_ta), linear in time, 0 at t_ta, M_d at z = 0. Same M_d at z = 0 as LC1, so z = 0 is the fair comparison. At z_f, 0.5, 0.25 the disc mass differs from LC1's and this is stated beside those read-outs.
- **Size.** a = R_d, b = 0.2 R_d, fixed in physical size from the start, as LC1. No disc size growth: a limit, disclosed.
- **Mass conservation.** m(t) = m [1 − M_d(t)/M_sim], as LC1.
- **Placement.** Centre = X48's `centre`, every 10 steps, as LC1. Axis = LC1's own axis for that seed (angular momentum inside 0.1 r_vir of X48's `snap_zf`, fixed), so that start time is the only difference in the pair. This uses a later state to set the axis: disclosed. No back-reaction on the disc. The centre's largest jump between updates is logged, since a shrinking-sphere centre can jump between clumps before collapse is finished. Reported, not a grade.
- Snapshots at z_f, 0.5, 0.25, 0.

## Read-outs, same reader as LC1 (`lc1_read.py`'s `pair`, imported, not edited)
- Each seed against ZN1's no-disc run: Q(r), Q_Blumenthal, Q_Gnedin, f_Q, R_live, at z = 0.5, 0.25, 0. At z_f the no-disc partner is X48's `snap_zf`.
- Each seed against LC1's run of the same seed: **ρ = R_live(PZ1)/R_live(LC1)** and **Δf = f_Q(PZ1) − f_Q(LC1)** at z = 0.
- Reported: t_ta, z_ta, M_d(z_f)/M_d by seed, centre jumps, median-radius turnaround as a side check on the definition.

## Verdict
At z = 0 over seeds finished, with **fewer than 6 finished seeds: UNDECIDED.**
1. **Class, LC1's lines, unchanged:** WEAK R_live ≤ 1.25, STRONG ≥ 1.45, else INTERMEDIATE; BLUMENTHAL HOLDS f_Q ≥ 0.8, PARTIAL 0.4–0.8, WEAK RESPONSE below 0.4.
2. **Pair label:** seed-bootstrap 95 % interval on the median of ρ and on the median of Δf (20,000 draws of the seeds, fixed rng seed 1).
   - **NO DETECTED CHANGE** if ρ's interval contains 1 and Δf's contains 0.
   - **SHIFT UP** or **SHIFT DOWN** if either excludes its null, by sign. If the two disagree: **MIXED**.
   - Sign counts by seed are reported beside it.
A class change with no detected pair shift is reported as such and not read as a change, since f_Q sits near LC1's 0.8 line.

**Reported, not graded, labelled SCALING ONLY:** SPARC's line with CN1's contraction scaled by the measured f_Q, by LC1's own `lc1_x74.py` route (rule with floor, CE1's ng 64 table, one 10¹² number carried across SPARC's masses). It compares with LC1's Υ 0.32 / 0.32 at 0.872, and is not a run of version N. SPARC pass line, for reference: rms ≤ 0.110, Υ 0.50–0.80 both backgrounds. The other record lines (keys, X-COP, groups, LITTLE THINGS) aren't touched: this lane changes one number at one mass.

## Checks (any failure: no verdict)
- **K1 zero-mass disc:** M_d 0 through the disc code path, forced through the disc's force call from step 0, 60 steps from the initial conditions, against the unmodified engine (`x48_fast` `main`, `--max-steps 60`): |d| ≤ 1e-12 relative, positions and velocities.
- **K2 disc force:** LC1's analytic force against a numerical gradient, 1,000 points: ≤ 1e-6.
- **K3 turnaround finder:** on a uniform sphere with a known top-hat solution, Λ off, measured t_ta within 2 % of the ODE's, and the state handed back is the stored state at the maximum.
- **K4 reader baseline:** the imported reader on LC1's own runs reproduces `lc1_results.json` at z = 0 for all nine seeds (Q, f_Q, R_live): |d| ≤ 1e-6.
- **K5 preemption:** SIGTERM and resume, across both the pre-turnaround and disc phases, against an uninterrupted run over the same steps: |d| ≤ 1e-12.
- **K6 whole-path null:** seed 1, M_d 0 through the full path to z = 0. At z_f against X48's `snap_zf`: max |Q − 1| at r/R_d 2–10 ≤ 0.10 and S ratio within 15 %. X48's seed was run before the compiled kernel, so round-off chaos is expected and exact equality isn't. At z = 0 against ZN1: reported as the chaos floor on same-seed pairs.
- **MUTATE:** M_d × 2 on seed 1, written to its own run directory, must move Q(3 R_d) − 1 by more than 30 %. Otherwise UNDECIDED.
- **Wall time:** measured on one seed before launching all, and stated.

Co-ordination: only this lane's directory is written. Pre-compiled bytecode is off, so nothing lands in LC1, X48, ZK1 or ZN1.
