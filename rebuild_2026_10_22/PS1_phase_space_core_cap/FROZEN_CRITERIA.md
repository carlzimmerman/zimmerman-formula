# PS1_phase_space_core_cap: FROZEN CRITERIA (committed alone, before the graded script exists or any graded number)

Written 2026-10-26, at the owner's request: "draft frozen criteria for a native phase-space-density core rule on the IB1
clusters. Criteria only, no run yet."

Standing rules:
- κ = ½ FITTED.
- Footings canonical / alt are graded separately and never pooled.
- Cold dark energy, not matter, never a particle. There is no particle mass, so no Tremaine–Gunn-type bound (which
  needs one) is used.
- No new constant. No ΛCDM number enters the rule. Inherited inputs are listed in §7.
- Nothing here says the data favour the framework. Not "theory closed".

## 0. The record before this lane (checked 10-26)

| lane | what it did with phase space | why it is not this lane |
|---|---|---|
| NU1 (9f0026743e) | Tremaine–Gunn cap on massive neutrinos in clusters | added ordinary mass; particle bound; PARTLY |
| CFG921 P4 (f4c87a342f) | phase-space-density **capture** selector, Q\_\* fitted on 83 LVD dwarfs | one fitted constant; dwarf excess; clusters z −7.3 / −6.2 |
| CFG461 C1, CFG130 | Lynden-Bell / max-entropy cold fluid with a maximum η | targets the law's profile; η not tied to formation |
| captured_profile (0e3b9616a3) | a finite f_max cannot make the law's r^−1/2 cusp | a theorem about cusps; route E halos are cored |
| IB1 (2d4ef7952f, 85dae14ee3) | none; gas HSE fixes the cluster core | the miss this lane targets |

No prior lane caps the **collapse-cored** branch of the current core law with a phase-space density fixed by the halo's own
formation. This is that lane.

## 1. Hypothesis PQ (formation phase-space cap)

Cold dark energy is collisionless (route E), so its fine-grained distribution obeys Liouville. Mixing during assembly can
only lower the coarse-grained phase-space density.

**The posit:** the central coarse-grained phase-space density of a collapse-cored halo does not exceed the mean
phase-space density of the half-mass object that formed it.

    Q_core ≡ ρ_0 / σ_0³  ≤  Q_form ≡ ρ̄_f / σ_f³

**Disclosed: a posit, not a theorem.** Liouville bounds Q_core by the progenitor's **maximum** fine-grained f. The progenitor's
mean is lower, so this cap is stronger than the theorem gives. Choosing the mean is the one modelling choice. It is fixed
here, not scanned.

**Formation side.** This uses X41's own EPS machinery (`zform`, `sigma_coll`), unchanged:
- ρ̄_f = Δ ρ̄_m (1 + z_f)³, with Δ = 18π²;
- r_f = (3 (M/2) / (4π ρ̄_f))^{1/3};
- σ_f² = G (M/2) / (2 r_f), the singular-isothermal virial relation for the half-mass object.

**Core side.** The halo is the record's Burkert (`solve_r0`) at surface density Σ, with the same M and R_out as X43:
- ρ_0 = Σ / r_0.
- σ_0 is the **isotropic Jeans central dispersion of the cold component in the total potential** (cold + baryons,
  Newtonian):

      σ_0² = (1/ρ_0) ∫_0^{R_out} ρ_c(r) G M_tot(r) / r² dr

**Rule (graded).**

    Σ_core = max( a₀/(2πG),  min( η(c_f) Σ_coll(M),  Σ_Q(M) ) )

Σ_Q is the Σ at which Q_core(Σ) = Q_form, solved per object. The a₀ floor is untouched. The cap acts **only on the collapse
branch**, so halos on the floor (below about 10¹² M☉) are unchanged by construction.

Where the cap binds, the core no longer depends on c_f. This matters because c_f is not converged (X48 A2 is running).

## 2. Model (graded run)

The baseline is the flagship as scored on the 10-26 theory statement: **X48 regrade at ng 48** (`x48_regrade_ng48.json`).
That is X43's rule with η(M) = (4/(3 B(1))) c_f(M)^{5/4} from the ng-48 c_f table.

PS1 changes one line: the collapse-branch Σ becomes min(η Σ_coll, Σ_Q). Everything else is X48 / X43 unchanged:
- the cluster M_tot and R_out (`prep`'s Mfair, rta);
- the baryons;
- route-E Newtonian lensing (`dvecN`);
- the C\* denominator, cells, weights, offsets and reduced shear;
- the SPARC fit and the group estimator.

**The c_f table is frozen to ng 48** for the graded run. If X48 A2's converged table is committed before the run, PS1 is
also run on it, as a reported line only.

**Objects:**
- clusters (all 326, both h cells 0.672 / 0.686);
- groups (63, P4 T3, X43's group grade);
- SPARC (175, X43's SPARC line).

**Background:** EM1's A_c2b_refit, as in X41/X43/X48. B_cfg886_bg is reported only.

## 3. Grades (per footing; a cell passes only if |Z| ≤ 2 at both h)

The cells are the 15 X38/OS1 cluster cells (`ic1b_lib.cells_from`):
- G-MID-T1..T3, G-MID-b;
- G-OUT-all, G-OUT-T1..T3, G-OUT-b;
- G-IN-all;
- G-OUT-Mall, G-OUT-M1..M3;
- G-IN-Mall.

**Side lines, which must still pass:**
- SPARC: X43's frozen line;
- groups: |Z| ≤ 2.

| class | rule |
|---|---|
| **INERT** | the cap binds in fewer than 10 % of the 326 clusters, or moves G-IN-Mall's pred by < 3 % at both h. The posit is not active at cluster scale. This is checked first and overrides the classes below. |
| **PASS** | all 15 cells pass, and SPARC and groups pass |
| **IMPROVES** | G-IN-Mall's max over h of \|Z\| is below the baseline's; none of the baseline's 14 passing cells fails; SPARC and groups pass |
| **TRADES** | G-IN-Mall passes or improves, but ≥ 1 baseline-passing cell, SPARC or the groups fails |
| **FAILS** | G-IN-Mall is not improved, and the class is not INERT |

The verdict needs both footings to agree, else UNDECIDED.

**Reported, not graded:**
1. **F0 map.** Q_core(baseline)/Q_form at M = 10^11, 10^12, … 10^15 (both backgrounds), and the fraction of SPARC galaxies,
   groups and clusters where the cap binds.
2. KT-only rule: the 106 KT clusters, with cells rebuilt as in IB1's reported item 1.
3. **Theorem-strength variant.** Q_form replaced by the progenitor's own central Q_core: its Burkert at the baseline Σ for
   M/2, evaluated at z_f. This is the weaker cap the Liouville argument actually licenses.
4. **Anisotropy bracket.** σ_0 from a radial-orbit Jeans integral (β = 0.5 constant), against the graded isotropic σ_0.
5. Σ_PQ / Σ_HG for the 106 KT clusters, beside IB1's median Σ_HG/Σ_OS1 = 0.37. This asks whether the cap lands where the
   gas says the core sits.
6. Per-bin pred/meas (all 326).

## 4. Checks

- **K0.** With the cap disabled, the script reproduces `x48_regrade_ng48.json`:
  - G-IN-Mall pred, both footings and both h, to 1e-9;
  - the SPARC rms (0.0650 / 0.0657) to 1e-9.
- **K1.** The Jeans integrator returns the Plummer central dispersion. For a self-gravitating Plummer sphere,
  σ_0² = G M / (6 a). Relative agreement must be 1e-6.
- **K2.** Q_core(Σ) is monotonic increasing on the solver's bracket for 5 test masses (10^12.5 … 10^15). The root
  residual must satisfy |Q_core(Σ_Q)/Q_form − 1| < 1e-8.
- **K3.** The formation side reuses X41's internals: ρ̄_f r_f equals `sigma_coll`'s Σ to 1e-12.
- **K4.** Peak RSS < 2 GB, one thread.
- **MUTATE** (`--mutate`, separate `_MUTATE` outputs). K1's analytic side uses G M/(3a). K1 must FAIL, and the script exits
  1. The mutated grades are reported only.

## 5. Seen before freezing (disclosed)

**Seen:**
- X48 regrade ng 48: all cells, SPARC and groups. G-IN-Mall fails OVER (canonical Z −2.4); G-MID-T1 Z −1.84 (over);
  G-OUT-M3 Z +1.80 (under).
- IB1: the cluster cores are ~2.5× denser than the gas's hydrostatic mass (Σ_HG/Σ_OS1 median 0.37).
- The record rows in §0.

**Not seen:** any Q_core, any Q_form, where the cap binds, or any capped grade.

**Expectation stated now (scaling only, no number computed).** At fixed M and R_out, Q_core ∝ Σ^{3/4} M^{−5/4} (Burkert,
baryons neglected). Lowering Σ widens r_0 at fixed mass. That lowers the inner prediction and moves mass outward:
- right direction for G-IN-Mall, G-MID-T1 and G-OUT-M3;
- wrong direction for G-OUT-all (Z −1.43, over).

The live outcomes are:
- **INERT**, if formation objects are denser in phase space than the cores;
- **TRADES**, if the cap binds hard enough to push G-OUT-all over;
- **TRADES via groups**, since groups are collapse-cored too.

## 6. Outputs

`ps1_phase_space_cap.py` → `ps1_phase_space_cap.out` and `ps1_phase_space_cap_results.json` (`_MUTATE` for the control). Run
with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`. It is a small job, under the standing rule for a live 1024³ run.

## 7. Inherited inputs (flagged)

| input | status |
|---|---|
| EPS formation: δ_c 1.686, ω̃ 0.974, Δ 18π², half-mass convention | X41 collapse statistics, unchanged |
| σ(M), D(z), Ω_m | EM1's own background (A_c2b_refit) |
| cluster cold mass = `prep`'s Mfair within rta | the flagship's (X43) budget. **Carries the 5.364 abundance the owner's 10-25 rule flags.** It is inherited unchanged from the baseline, not introduced here. IB1's HG removed it; PS1 does not. |
| c_f table | X48 ng 48, unconverged (×2) |
| R500, Mgas500, kT | eRASS1 catalogue: **ΛCDM-processed**, rescaled by qd to the h cell |
| σ_f virial relation, isotropic σ_0 | modelling choices, fixed here; variants reported in §3 items 3–4 |
| C\* denominator, offsets, reduced shear, weights, boost | the record's (X2/X7/X30) |
