# CFG915: population-label (history) mobility H-POP. HYPOTHESIS TEST. Class as frozen: CONTRADICTED under both declared label rules

**Label: HYPOTHESIS TEST** (constructive, from CFG913/914). Criteria `FROZEN_CRITERIA.md`, committed alone first (014b7ba1d),
block 910–919 (LEDGER.md:662). κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 are kept apart and never pooled. Cold energy is
real gravitating mass; no particle species is added. Not "theory closed". Nothing here says the data favour the framework.

## New assumptions and constants (read first)

| item | status |
|---|---|
| α_t = 0 for the t population (cold energy present at a structure's formation) | **new posit**. It contradicts the record's universal drift and tether push (CFG638, CFG747/776), which act on all cold energy. CFG776's lasting constraint allows it |
| α_f ∈ {0.5, 1.0} for the f population (later arrivals) | not new: the record's existing O(1) coefficient at its galaxy-passing values |
| rule L0: formation snapshot at the half-mass epoch, X_form = 0.5 | **new convention** (acts as a constant); no rate constant |
| rule LC: f → t on exact settling (q ≥ 1 − 1e-12, no deficit inside) | **new rule**; no rate constant. A finite capture rate would add Γ_cap (not run) |
| release t → f (gas expulsion, stripping) | none in either graded rule. Any release is a further new rule (evaluated by mapping) |
| dwarf clump amount | **new per-object input**: each dwarf's formation-epoch baryon mass (unmeasured) |
| naming | H-POP's "tethered" (t) is dynamically the record's *untethered*, collisionless class. Its "free" (f) is the record's settling class. The new content is the assignment by history |

## What H-POP says and how it was tested

Mobility depends on the cold energy's population label (its history), not on its local state.
- **t** = cold energy bound into a structure at its formation. α_t = 0: it is collisionless and retained.
- **f** = cold energy that arrived later by catchment inflow. α_f = 0.5 or 1.0.

Both labels gravitate, and both count toward the law's target. Two label rules were declared and graded:
- **L0 (literal, primary).** At X_ta = 0.5, everything inside r_ta becomes t. Later arrivals stay f forever.
- **LC.** f becomes t in any cell that is exactly settled with no deficit inside it.

Each constraint uses its source lane's own drift form. The three constraints come from the record:
- **G (galaxies):** CFG598's MW P0 (i), tested by a two-population version of the CFG598 PDE. The code reproduces CFG598
  bit-for-bit when there are no t labels.
- **M (mergers):** CFG623/641. Tested with first-order mixture bounds plus the label split in the cluster-mass hosts of the same
  PDE.
- **D (dwarf clumps):** CFG882/889. Tested by record mapping.

The necessary corollaries were also checked against the record (CFG726, CFG777, CFG845, CFG776, CFG722).

## Result

| | G: CFG598 MW (i), both footings | M (first order) | D | corollary C1: merger memory | class |
|---|---|---|---|---|---|
| **L0** | **FAIL.** α_f 0.5: min q 0.635 / 0.687, M_c/M_ph(<30) 0.71 / 0.75. α_f 1: min q 0.921 / 0.961. The α_f → ∞ bracket passes (0.9996) | UNDERDETERMINED. φ_f(<200 kpc) is 0.085–0.21 in the log-14 host against φ_lin,H 0.039 / 0.041 | CONSISTENT (conditional) | AT RISK (≈ CFG726's N×0.5 bracket, which fails) | **CONTRADICTED** (breaks CFG598 MW (i)) |
| **LC** | PASS. α_f 0.5: 0.9909 / 0.9915. α_f 1: 0.9955 / 0.9957 (but see PH1) | UNDERDETERMINED. φ_f(<200) is 0.86–0.88 in the log-14 host (an over-estimate for LC) | CONSISTENT (conditional) | **CONTRADICTED**: identity with H-MM, so CFG726's fails apply | **CONTRADICTED** (breaks CFG726) |

**Overall H-POP, best over the two rules: CONTRADICTED.** Each rule is broken by a different committed record result:
- **L0** breaks the galaxy constraint.
- **LC** breaks the cluster lensing record through merger memory. CFG726's H-MM fails three ways:
  - eRASS1 OUTER, Z −3.63 / −4.05;
  - ACCEPT OUTER, Z −4.83 / −5.19;
  - eFEDS.

### G: why L0 fails, and what LC really does
- **L0.** The formation snapshot (t_form 4.51 Gyr, r_ta 515 kpc) freezes 1.6e12 M_⊙. Of that, 98.4–99.4% is unsettled cold energy
  still in transit (PH2); the settled interior reaches only 4.7–8.6 kpc.
  - The 20–30 kpc shell must then be filled by cold energy deposited after X = 0.5 at 500+ kpc. At α_f ≤ 1 it does not arrive by t0.
  - The failure is transport-limited: with unlimited f transport, the f supply is enough.
  - Under a collisionless reading, the frozen t inside turnaround would fall in instead (P2-like). CFG598 found that P2
    overfills the MW at every α for the whole catchment; this was not computed for the half catchment here.
- **LC.** Exact capture almost never fires in a growing host. The phantom keeps rising, so settled cells always lag slightly.
  - LC ends with t share 3.8% / 3.0%. The L0-early bracket, where only the initial 2% content is t, gives the same min q to
    1e-5 (PH1).
  - LC's t is therefore the **overfill** population. LC is in effect a permanently latching version of CFG639's deficit gate.
  - With a realistic settled tolerance (post-freeze, pre-run variant LC-tol: q ≥ 0.99 and inner deficit ≤ 1%), LC **fails G**
    by jamming: min q 0.69–0.87, M_c/M_ph(<30) 1.30–1.97.
  - So LC passes G only in its exact-capture form.
- **Swapped control (MUTATE).** Making L0's snapshot mobile and its late arrivals immobile passes the MW (0.9928 / 0.9930 at 0.5).
  The galaxy needs its early cold energy to stay mobile. This is CFG913's common cause seen through the label.

### M: mergers
- **(a) Mapping.** The record's passing merger configurations have effectively all cold energy immobile: CFG623 α = 0
  (ALLOWED, Z_B +1.09 / +1.06), and CFG641 arm S with the gate off 99.96%.
  - H-POP passes only if the merging cores are almost all t.
  - CFG641's RI-allowed / RN-excluded contrast (stars-only branch) says any collisionless t reservoir must trace the baryons.
    H-POP does not fix that profile. Reported only.
- **(b) First-order tolerance** (linear mixture; the mobile part sits at the α = ∞ configuration):

  | footing | φ_lin,B | φ_lin,H |
  |---|---|---|
  | canonical | 0.135 | 0.039 |
  | alt | 0.134 | 0.041 |

  With the α = 0.3 node instead of ∞: 0.138–0.144 and 0.041–0.043. The record's β_obs = −0.0400 is constant across nodes.
- **(c) Label split in the hosts.** CFG598 grid hosts have point-mass baryons and an inherited EPS history. Log-15 cores
  (200 kpc) are almost all t under both rules (f ≤ 0.05): the near-Newtonian core is overfilled, M_c/M_ph(<200) 1.36–1.54. Log-14 cores are
  f 8.5–21% (L0) and 86–88% (LC).
  - First order never excludes, so M is UNDERDETERMINED for both rules.
  - For LC the static split over-states mobility (argument): overfill keeps latching during a merger wherever the phantom leaves
    with the gas.

### D: dwarf clumps
- **Retention.** α_t = 0 sets CFG882's Γ_t = α_t q/τ = 0. CFG889's erosion acted through the drift along orbits (its no-OU runs
  eroded the same), so it is switched off for t. The clump is retained if it is t:
  - under LC, yes (it is latched overfill);
  - under L0, yes if the overfill formed from t after formation.
- **Amount (route D-i: t settled at formation, baryons lost later, t retained).** In the deep regime with t dominant,
  M_obs/M_law = (M_b,form/M_b,now)^½ (order of magnitude).
  - CFG827's 28 out-of-sample dwarfs need a loss factor e^{4E} of median 4.3 (16–84%: 1.2–17.8). Three need none.
  - CFG890's uniform V_x (6.48 / 6.29 km/s) needs √M_b,form − √M_b,now = 377 / 323 M_⊙^½. Loss factors are then:

    | M_b,now (M_⊙) | loss factor |
    |---|---|
    | 1e3 | ×167 / ×126 |
    | 1e5 | ×4.8 / ×4.1 |
    | 1e7 | ×1.25 / ×1.22 |

- **Route D-ii is not available.** D-ii (t = cold energy collapsed at the assembly epoch) is CFG844's H-PRIM, which CFG845
  excludes (D −0.273 ± 0.026).
- **D-i against the record.** No listed record result contradicts it:
  - CFG880 scatter: allowed, as per-dwarf loss;
  - CFG827 no age trend;
  - CFG843 MW = M31;
  - CFG883 globulars: t ≈ 0 when g ≫ a0 or inside a host field (NGC 1851's robust clump is unexplained);
  - CFG845 rotators: no net loss;
  - CFG829: blue lenses on the law, red lenses above.

  CFG860/873 (isolated gas-bearing dwarfs above the law) become a prediction: early baryon loss there too.
- **Release variants** would free the overfill to drift at α_f ≫ α_c (1.37e-3), which erases the clump. Release is incompatible
  with H-POP's own D route.

### Corollaries
- **C1, merger memory.** t is collisionless and retained, and f only fills deficits. A remnant of settled pieces therefore keeps
  M_b + max(Σ T_i, T_rem), which is CFG726's H-MM formula.
  - **LC:** the identity holds even though LC latches only overfill while hosts grow (argument, not computed). The remnant's
    sub-additive excess is overfill with no deficit inside it, so it is latched at once. CFG726's FAIL applies, with that lane's
    own caveats: POST-HOC; 3 VOID controls that touch no failing score; X-COP and Bullet not run; the member-count rule declared.
  - **L0:** in the deep regime, members' t ≈ √X_form = 0.707 of their halos. That matches CFG726's N_mem × 0.5 bracket, which
    also fails (T-R OUTER Z −2.50 / −3.19; T-A OUTER −3.13 / −3.59). The mapping is approximate, so this is AT RISK only.
- **C1b, minor accretion** (CFG726 T-S2, unscored there): accreted pieces keep their t under both rules, so disc V rises ×1.12
  for 3% accreted in 1% pieces. AT RISK.
- **C2, frozen relic** (CFG777, FAIL 0/3): it depends on the law's source. Report only.
- **C4.** α_t = 0 is the posit that the record's push does not act on t.
- **C5.** CFG722 Q1 (conditional): a ballistic collisionless carrier is a particle species in the identified-carrier dictionary.
  H-POP's t inherits this open issue; nothing is added here.

## Predictions H-POP makes (named for the owner; none run here)

1. **Dwarfs (D-i).** Faint dwarfs had about 4× today's baryons at formation (median; 1.2–18). If the excess is one uniform V_x,
   the factor rises steeply toward the ultra-faints.
   - Test: excess against an outflow indicator at fixed M*, such as the metallicity offset from the mass–metallicity relation or
     an SFH-based lost-mass estimate (CFG827's Weisz+14 SFHs).
   - Isolated gas-bearing dwarfs (CFG860/873) must show early loss too.
2. **Rotating dwarfs and blue lenses stay on the law**, because they lost no baryons (already true: CFG845, CFG829). Any gas-rich
   rotator with an excess would count against D-i.
3. **Red / spheroidal lenses.** The excess should scale with baryons lost since formation (quenching), not with M* or
   environment (CFG850/912). Test: B21-type stacks split by quenching or outflow proxies at fixed M_b; data not on disk.
4. **Merger remnants (LC).** The retained sub-additive excess gives early types a lift of √N − 1 (CFG726 T-K passes at N = 2).
   Test: early types split by a merger indicator at fixed M_b. The cluster form of the same memory is already contradicted
   (C1).
5. **Cluster cores.** H-POP gives core overfill only from baryon loss, which is absent where the hot gas is retained, or from
   memory, which overshoots OUTER. It does not explain eRASS1's MID ×1.9 consistently with OUTER.

## K-tests (16 PASS, 1 PARTIAL)

| K | result |
|---|---|
| K-M1 CFG623 | α 0 ALLOWED both; 0.1 / 0.3 / ∞ EXCLUDED both; Z_B(0.03) +3.12 / +2.65; β_obs −0.0400 at every scorable node |
| K-M2 CFG641 | arm S ALLOWED in all 14 cells, arm P EXCLUDED; gate off 0.9996; RN main reservoir share 0.872 |
| K-G1 CFG598 | 0.9842 / 0.9849 (0.25), 0.9928 / 0.9930 (0.5) |
| K-G2 | two-population code (no t) against CFG598 MW P0 at 0.5, 1, ∞, both footings: max rel 0.0 |
| K-G3 | same, grid hosts log 15 and 14 (α 0.5): max rel 0.0 |
| K-C CFG542 | α_max 1.0000 / 1.1864 |
| K-D1 CFG882 / K-D2 CFG889 | α_c 1.371e-3, α_50 6.18e-4..1.02e-3 / α·t_50 105.5–147.5 Myr |
| K-R | CFG827 (28, 25 above, Ē +0.375, ρ +0.089), CFG880 (ŝ 0.38), CFG843 (c +0.055 ± 0.117), CFG845 (D −0.273 ± 0.026), CFG829 (blue 1.016 ± 0.086, red 1.587), CFG883 (6 NO CLUMP, 1 robust CLUMP), CFG890 (V_x 6.480 / 6.295), CFG726 (all eight Z values, FAIL verdicts) |
| **K-R860 PARTIAL** | CFG860's canonical primary is not stored in its JSON. The README values (+0.285 ± 0.108 / +0.370 ± 0.073) are used; the nearest stored variant is "cut 350 kpc" (+0.357 / +0.371). As frozen |

## MUTATE (frozen: swap α_t ↔ α_f): BITES for both rules (exit 1)

- **L0 swapped.**
  - G now passes (0.9928 / 0.9930 at 0.5; 0.9963 / 0.9964 at 1).
  - M fails at first order: mobile fraction ≥ 0.79, above φ_lin,B.
  - D fails: the clump drifts at α ≥ 0.5 ≫ α_c.
  - Newly failed: M and D.
- **LC swapped.**
  - G fails: min q 0 (cells emptied), M_c/M_ph 0.59–0.80.
  - M is not failed (mobile fraction 0.12–0.14).
  - D fails.
  - Newly failed: G and D.
- Disclosed: the D tooth is by mapping only.

## Corrections, post-hoc items and disclosures (2026-10-20)

- **Post-freeze, pre-run (no class weight): LC-tol.** Added while the script was written, before any run. The reason was the
  expectation that exact capture rarely fires during growth, which PH1 confirmed.
- **Post-hoc (after the first full run; no class weight).**
  - PH1: LC against L0-early.
  - PH2: where the L0 snapshot's mass sits.
  - PH3: L0-settled, where only the q ≥ 0.99 interior becomes t (a different, unfrozen rule). It fails by overfill,
    M_c/M_ph(<30) 1.025–1.062, with min q ≥ 0.993.
  - PH4: where the overfill sits. In L0-settled, 78–93% of the overfill inside 30 kpc is f stranded in transit when the inner
    deficit closes; the one-sided drift cannot remove it. In L0, LC and L0-early, the 0.46–0.64% overfill is t in the
    Newtonian core (the initial content, as in CFG598's own disclosure).
  - The reading notes in `cfg915.out` (C1 under LC; the static split over-states LC's mobile fraction).
  - All frozen numbers were re-run from scratch with the final script and are identical (diffed).
- **Implementation choices, within the frozen text.**
  - "Exactly settled" uses the record's own `settle_inf` tolerance, 1e-12.
  - Capture is applied after the flux step and again after the deposits.
  - The snapshot is taken at the first step with t ≥ t_form.
  - The P0 model holds t at rest where it is, so the model has no ballistic infall.
- **Approximations.**
  - M at first order only: lens statistics taken as linear in the mixture.
  - The host label split comes from the CFG598 grid model (point-mass baryons, inherited EPS history), used only for the split.
  - D uses deep-regime, t-dominated, order-of-magnitude relations.
  - C1 for LC is an argument (identity of the settled state), not a merger run.
- **Heavy run.** Not queued: no rule ended UNDERDETERMINED. If C1 were lifted (for example by a release-on-stripping rule, which
  is a new rule), M(LC) would need a merger run with *dynamic* latching. The static-label spec in criteria §9 would be the wrong
  test for LC.
- **Compute.** One core, nice 10. Main run 35 s, MUTATE 40 s; every PDE run under 9 s; peak memory well under 1 GB. The run was
  made beside the live 1024³ job; no other process was touched. Nothing was downloaded.
- **Not claimed:** that H-POP is derived; any measured α_f or X_form; κ derived; "theory closed".

## Reading

- **H-POP in the literal form (L0) fails the galaxy constraint.** Freezing a structure's formation-epoch cold energy leaves too
  little mobile cold energy to finish settling the MW by t0.
- **The form that survives the galaxy and dwarf tests is "latch the overfill" (LC).** Cold energy becomes permanently immobile
  once it sits in an overfilled region with no deficit inside. That is a history variable outside CFG913's six local ones, and
  it removes CFG889's skin erosion.
- **Its price is merger memory.** The sub-additive excess of every merger is latched, which is CFG726's H-MM. The cluster
  lensing record already excludes H-MM in the outer band.
- So the population label moves CFG913's obstruction from mergers against galaxies to clusters' outer profiles. It does not
  remove it.
- **Constructive lead (untested; needs new rules):** latching plus a release of t when it is stripped from its host. That would
  have to leave satellites' inner clumps intact (CFG838 found no tidal signal), keep Bullet-type cores immobile, and remove
  member-halo memory in clusters.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (014b7ba1d) |
| `cfg915.py` | K-tests; two-population CFG598 PDE (`Run2`); G-tests; host label splits; M bounds; D mapping; corollaries; classes; post-hoc PH1–PH4; MUTATE |
| `cfg915.out`, `cfg915_results.json` | main run |
| `cfg915_MUTATE.out`, `cfg915_results_MUTATE.json` | MUTATE run (exit 1 = tooth bites) |
| `cfg915_runs_cache.json` | every PDE run's diagnostics, keyed by setting |

Rerun from this directory with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg915.py`. Then run the same command with
`CFG915_MUTATE=1`; the MUTATE run needs the main results JSON.

Read-only inputs:
- `cfg598_lib` (imported);
- the result JSONs of CFG623, 641, 598, 542, 882, 889 (parts), 726, 777, 827, 829, 843, 845, 860, 880, 883, 890.

No other lane was edited.
