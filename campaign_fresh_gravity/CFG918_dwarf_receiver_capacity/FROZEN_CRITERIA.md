# CFG918 FROZEN CRITERIA: sol61 roadmap gate 1, outer-envelope energy and angular-momentum receiver capacity (Draco, Sextans, Fornax, Leo I)

Committed alone, before any script exists and before any number of this lane is computed. Block 910–919 (LEDGER reservation
row, CFG918 = "sol61 roadmap gate 1"). Source request: `sol61_push/ROADMAP_COLD_ENERGY_MECHANISMS_2026-10-19.md` ("NEXT TEST")
and its companion `sol61_push/FORMATION_TO_CLAUDE_ONE_SHOT_2026-10-19.md` (astra's files, read only, not edited).

κ = ½ is FITTED. The footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s²) are scored separately and never pooled.
The cold energy's mass is required; no dark-matter species is added. Raw data and framework-native inputs only: no HMcode,
BAHAMAS, ΛCDM mass function or ΛCDM spin distribution enters any class. Not "theory closed".

## Record check (done before writing these criteria)

Gate 1 has not been attempted. Checked: LEDGER (no receiver-capacity row for the four dwarfs; CFG645 and CFG722 concern
settling export, not this budget), the commit log since 2026-10-19, and the 10-19/10-20 sol61 files. Astra's CFG877 arrival
note (10-20) says "Initial J/E receiver inputs still absent". CE-FM-089 (sol61 `spin_and_survival_2026_10_19`, section 2) gives
one isolated Sextans energy example without angular momentum; it is reproduced here as a control (K5), not as a result.
CFG853 R3 is a friction-delivery J estimate, not this capacity bound.

## The question

Can a finite outer envelope accept the energy and angular momentum that a forming central cold-energy core must shed? The
test is run in each of the four dwarfs with one common model and the dwarfs' finite stock. Necessary bound (roadmap):

    |J_req|² <= 2 I_out K_out <= 2 M_out R_max² K_available,

with K_available from ONE conserved energy ledger. This is a necessary capacity condition only. It gives no rate, mechanism,
selectivity or formation.

## Model (identical for all four dwarfs)

**M0, gravity and the ledger.**
- All mass gravitates in the Newtonian way. Cold self-gravity is class A (CFG888), which is the convention behind
  M_need = 3Rσ²/G (CFG853).
- The galaxy law enters only through the settled cap s (below).
- Everything is spherical. The external potential is static and is the sum of two parts:
  - the stars, a Plummer sphere (M★, a);
  - the settled (tethered) cold mass s M★, with M ∝ r inside R and constant outside.
- Neither external part receives energy or J:
  - stars as receivers are CFG853 T1's separate test, and are reported here only as an ungraded diagnostic;
  - the settled cold is tethered at rest on the law.
- The one conserved ledger is the cold sector in that static potential:

      E_c = K_c + W_cc + W_c,ext   (conserved),     J_c conserved.

- External torque and external work are zero (isolated assembly). A tidal torque would be a different, unsupplied receiver.
- Declared approximation: the stars do not respond.
- No radiative channel and no rest-energy or fusion terms are included.
- Charge is not modelled: this Newtonian reduction has no charged carrier, so the charge flux is n/a.

**M1, record inputs (CFG853 convention; K1 reproduces it).**
- Observables: M_V, a and σ from LVD (σ from CFG824's `so` where present), with Υ_V from the CFG827 SFH fits (Sextans: Υ = 2,
  assumed).
- Derived quantities:
  - M★ = Υ 10^{0.4(4.83 − M_V)};
  - aperture R = 4a/3 and p = 64/125;
  - y = G p M★ / (R² a0);
  - s = min[p(√(¼ + 1/y) − ½), 5.364];
  - remaining stock M_rem = (53.64 − s) M★;
  - core target M_x = M★ [3Rσ²/(G M★) − p − s] inside R, and F = M_x / M_rem.
- Mass-budget branches (never pooled):
  - **B0**: catalogue σ.
  - **B1**: σ × 10^{δ/2}, with δ from CFG861 (the conditional binary shift applied globally). B1 is a sensitivity, not a
    replacement observation.
- The catchment radius r_ta comes from CFG822 for each footing.

**M2, initial cold patch.** The patch is the whole remaining stock M_rem.
- Initial density, two geometries, each classed separately:
  - **G1**: ρ ∝ r⁻² on [R, r_ta] (the record's catchment, CFG822; CFG853 G1);
  - **G2**: ρ ∝ r⁻² on [R, 5R] (the handoff's compact-cloud scale; CFG853 G2).
- Initial velocity field:
  - Coherent rotation about one common axis, v_φ = λ_c V_c,i(r) sin θ, with λ_c ∈ [0, 1].
    - Upper bound 1: an equilibrium patch cannot rotate coherently faster than circular.
    - Lower bound 0: the action does not predict the initial spin (gate 3 is open), and no record quantity gives a positive
      lower bound.
  - Plus isotropic random motion. The total initial kinetic energy is
    K_i = K_rot(λ_c) + φ_K [K_vir − K_rot(λ_c)], with φ_K ∈ {0, ½, 1}, where:
    - K_rot(λ_c) = (2/3) λ_c² K_vir;
    - K_vir = ½ ∫ V_c,i² dm is the virial maximum (a patch with more kinetic energy expands);
    - φ_K = 0 is the turnaround-like start, with no kinetic energy beyond the rotation.
- Angular momentum and energy:
  - J_init = λ_c J_1, with J_1 = (2/3) ∫ r V_c,i dm;
  - E_init = K_i + W_cc,i + W_c,ext,i.
- Core and envelope material share one spin vector (one patch). A counter-rotating envelope would need an independent input;
  it is not admissible here and is not computed. Vector cancellation is never counted as transport.

**M3, final state.**
- Core mass M_x lies inside R.
- Receiver mass M_out = (1 − F) M_rem. This is the most favourable choice:
  - all non-core stock acts as the receiver;
  - there is no core inefficiency and no other loss;
  - 1 − F is the roadmap's optimistic upper allowance.
- Core, bound envelope and escaped mass are tracked separately.
- Core states (a bracket, because the profile inside R is not fixed by the estimator):
  - **C-S**: thin shell at R on coherent circular orbits, with v_c,S² = G[M_Pl(R) + s M★ + M_x/2]/R.
    - This is the least-bound arrangement inside R.
    - It is also the kinematic maximum of retained J: J_core,f ≤ M_x R v_c,S, because material confined to r ≤ R has
      j ≤ r_apo V_c(r_apo) ≤ R V_c(R).
  - **C-U**: uniform sphere of radius R, pressure supported, J_core,f = 0.
  - **C-C**: the record's cored shape (CFG870), M(<r) ∝ r³/(r² + r_c²) with r_c = 104 pc, truncated at R and normalised to
    M_x. It is pressure supported, with J_core,f = 0. Only the shape is used; CFG870's V_x and its mass budget are not.
  - The core's kinetic energy is virial in the total potential: K_core = ½ ∫ G M_tot(<r)/r dM_core, with the thin shell
    taking half its own mass.
- Receiver family. The most favourable admissible receiver is the maximum over this family, which has two components:
  - **A**: mass (1 − x) M_out, a thin shell at r1 on circular orbits (half self-force).
  - **B**: mass x M_out at r2 ≥ r1, moving purely tangentially. Its kinetic energy K_B closes the ledger:
    K_B = E_init − (every other final term: core kinetic and potential, A, B's potential, all cross terms).
- Constraints on the family:
  - R ≤ r1 ≤ r2 ≤ R_max;
  - K_B ≥ 0;
  - B's pericentre is ≥ R (the receiver never enters the aperture, so Fornax and Leo I gain no uncounted inner mass).
- Receiver branches, graded separately:
  - **RB, bound finite envelope**: B's apocentre is ≤ R_max, so the orbit stays confined to [R, R_max].
  - **RE, escape permitted**: there is no apocentre condition, so B may leave R_max after receiving J. Its return is not
    evolved, which is favourable and disclosed.
- J_cap is the maximum over (x, r1, r2) of m_A r1 v_A + m_B r2 v_B. Coherent planar orbits give the maximal J at each
  component's energy.
- Declared grids:
  - r1 and r2 on 80-point log grids in [R, R_max] (r2 ≥ r1);
  - x on 60 points in (0, 1].
- Rationale: for test particles at fixed total energy, the maximum of ∫ j dm is reached on at most two energy levels, with
  each parcel at the maximal j for its energy (the linear-programming vertex property). Including the receiver's
  self-gravity, the family maximum is the declared bound, not a proof over all distributions. This is disclosed.
- The final potential for the orbit conditions is static and spherical: stars, settled cold, core, shell A, plus half of B's
  own shell potential.

**M4, R_max (the maximum cylindrical radius during the transfer phase).**
- G1: r_ta, which is also the reservoir's edge.
- G2: the bracket {5R, r_ta}.
  - 5R is the patch edge and the receiver's initial outer radius.
  - r_ta, the z = 0 catchment turnaround radius, is the most favourable: no material of the dwarf's own supply ever lies
    farther out.
- R_max = r_ta presumes the transfer is finished before infall. Present Jacobi radii (CFG916, where available) are reported
  as context only.
- Assembly duration is not used: capacity carries no rate. It is the input for gate 2.

## Test of one bracket combination

- The core is allowed to keep J_core,f = min(J_init, J_core,f,max(state)), aligned with J_init.
- The required receiver angular momentum is J_req = J_init − J_core,f ≥ 0. It is the receiver's FINAL J, and includes the
  receiver's own initial J, because J_init is the whole patch's.
- A combination (λ_c, φ_K, core state, R_max) **passes** iff the family contains a configuration that closes the ledger
  exactly under all constraints, with m_A r1 v_A + m_B r2 v_B ≥ J_req.
- For the maximising configuration, the roadmap form is also reported, with K_available = K_A + K_B and
  I_out ≤ M_out R_max² (checked by K3c).

## Classes

There are 64 graded cells: 4 dwarfs × 2 mass branches × 2 footings × 2 geometries × 2 receiver branches. The bracket grid is
λ_c ∈ {0, 0.01, …, 1} × φ_K ∈ {0, ½, 1} × core ∈ {C-S, C-U, C-C} × R_max ∈ (the geometry's set).

1. **CAPACITY EXCLUDED**: no combination passes at any λ_c. The most favourable admissible receiver at the most favourable
   spin (λ_c = 0) is audited first.
2. **CAPACITY ALLOWED**: every combination passes at every λ_c ∈ [0, 1], so capacity is not the obstacle for any admissible
   value of the unfixed inputs. This is necessary feasibility only, NOT formation.
3. **INDETERMINATE**: anything else. Each such cell reports:
   - λ_crit,MF, the largest λ_c at which some combination passes;
   - λ_crit,all, the largest λ_c up to which every combination passes;
   - which bracketed input decides.

Summaries (reported):
- **Per dwarf × branch × footing × receiver branch**: EXCLUDED if both geometries are EXCLUDED, ALLOWED if both are ALLOWED,
  otherwise INDETERMINATE (the initial density field is not fixed).
- **Four-dwarf line** for each branch, footing, geometry and receiver branch:
  - BROKEN if any dwarf is EXCLUDED;
  - otherwise "no capacity obstruction" (not formation).

## Controls (all must pass; any failure → exit 1 and the classes are labelled NOT COMPLETED)

- **K1, roadmap mass table.**
  - M_rem, F_B0 and F_B1 for all four dwarfs (12 numbers) agree to half a unit in the last printed digit.
  - M_rem and F agree with CFG853's results JSON to 1e-9 relative.
- **K2, roadmap receiver examples.** M_out/M ≥ (j²/α)(R_i/R_out)² for j ∈ {0.05, 0.1, 0.2} × α ∈ {0.1, 1, 10} reproduces
  the sol61 `receipt.json` minimum fractions to 1e-12, including .0025/.01/.04 at α = 1.
- **K3, Cauchy–Schwarz.**
  - (a) A coplanar ring with tangential velocities has J² = 2 I K to 1e-12.
  - (b) 10⁴ isotropic random velocities (fixed seed) give J² < 2 I K.
  - (c) Every maximising configuration satisfies J_cap² ≤ 2 M_out R_max² (K_A + K_B).
- **K4, energetics.** The numeric routines match the analytic values to 1e-6 relative:
  - uniform sphere, W = −(3/5)GM²/R;
  - thin shell, −GM²/(2R);
  - ρ ∝ r⁻² shell, W = −Gμ²[(r2 − r1) − r1 ln(r2/r1)];
  - Plummer sphere, W = −(3π/32)GM²/a.
- **K5, CE-FM-089 example.** Input: a uniform virial cloud of 2.540e7 M☉ with R_i = 3239 pc forms a uniform virial core of
  fraction .988540 and radius 25.21 pc. The release must be 6.37e46 J and the escape speed of the 1.146% non-core stock about
  469 km/s, each to half a unit in the last printed digit.
- **K6, roadmap Sextans.** 1 − F_B0 = .01146 and 1 − F_B1 = .35471, to half a digit.
- **K7, ledger closure.** For every maximising configuration, recomputing E_fin from its parts equals E_init to 1e-9
  relative.
- **Grid refinement (reported).** r grids of 160 points and x of 120 points. A class that changes under refinement is
  disclosed and flagged; the frozen-grid class stands.

## MUTATE (separate outputs: `CFG918_MUTATE=1` → `*_MUTATE1*`, `CFG918_MUTATE=2` → `*_MUTATE2*`)

- **MUT-1, core binding removed.** The core's final state sits at radius r_F = R + M_x/μ instead of R. r_F is the outer edge
  of the innermost stock that supplies M_x in the declared geometry, so there is no net contraction. Receivers stay outside
  r_F. It must change ≥ 1 graded class.
- **MUT-2, starved receiver.** The receiver is 0.01 M_out. The other 0.99 M_out leaves before the transfer with exactly zero
  energy and zero J, which costs its initial binding. E_init is unchanged; the removal cost is charged to the ledger. It
  must change ≥ 1 graded class.
- MUTATE PASS iff both arms change at least one class. Otherwise MUTATE FAILS (exit 1), and that is reported.

## Reported, not graded

- The Peebles spin of the initial patch at the λ_crit values, λ_P = J|E_init|^{1/2}/(G M_rem^{5/2}), for orientation only.
  No spin distribution is used.
- Stars as an auxiliary energy receiver: p M★ × 3σ² ln 10 (the CFG853 T1 permissive tolerance), compared with each RB energy
  shortfall.
- Present Jacobi radii from CFG916 compared with R_max.
- Per-cell ledgers at the most favourable optimum, with units and origins:
  - mass: core, bound envelope, escaped;
  - energy: E_init, E_core,f, E_A, E_B;
  - angular momentum: J_1, J_core,f,max, J_cap.

## Compute and scope

- Stdlib and numpy only; one core, `nice -n 10`, OMP_NUM_THREADS=1, one process, under 1 GB.
- Nothing is downloaded, no PDE is run, and no other lane's files are edited.
- Outputs: `cfg918.py`, `cfg918_K.out`, `cfg918.out`, `cfg918_results.json`, and the MUTATE outputs.
- Any change after a number is seen will be a dated, labelled amendment appended below.

## Amendment A1 (2026-10-20, POST HOC, committed alone before it is run): three reported-only diagnostics

This was written after the K, MUTATE-1, MUTATE-2 and main runs, whose classes have been seen. It changes no frozen class,
control, grid or input; it adds three ungraded diagnostics to the main output.

Why: in the frozen receiver family, the energy-optimal configuration can put a large envelope mass on circular orbits just
outside R. Example: Leo I, RE, G1, λ_c = 1, which puts 1.15e8 M☉ at r1 = R. That respects the declared aperture rule (mass
outside R is not aperture mass). But the roadmap warns that Fornax and Leo I must not acquire extra uncounted inner envelope
mass, and a resolved stellar-kinematics test (gate 4) would see such mass. Separately, the core state C-S (thin shell at R)
is a kinematic limit, not the record's description of the dwarf core.

- **PH1, no envelope crowding.** Classes recomputed with the receiver family restricted to r1, r2 ≥ 2R. Otherwise identical.
- **PH2, Peebles spin at the critical points.** λ_P = λ_c J_1 |E_init(λ_c, φ_K)|^{1/2} / (G M_rem^{5/2}) at λ_crit,MF and
  λ_crit,all (φ_K = 0 and 1). For orientation only; no spin distribution is used.
- **PH3, record core only.** Classes recomputed with the core state restricted to C-C (the CFG870 cored, pressure-supported
  shape), dropping the C-S and C-U limits.

PH1 and PH3 are reported next to the frozen classes. They carry no class weight. The graded classes remain those of the
frozen criteria.
