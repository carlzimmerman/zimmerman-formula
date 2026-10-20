# CFG915 FROZEN CRITERIA: population-label (history) mobility H-POP against the merger, galaxy and dwarf-clump constraints

Date 2026-10-20. Block 910–919 (LEDGER.md:662 reserves CFG915 for H-POP). Committed alone, before any script exists.

**Kind of lane: HYPOTHESIS TEST** (constructive, from CFG913/914). Feasibility of one hypothesis against the record's own
results, plus light single-setting re-use of the CFG598 drift PDE. Nothing is fitted to data. No knob scan: every setting
below is declared here and none is searched. A clean CONTRADICTED is a valid result.

**Settings.** κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.1312e-10 (alt) m/s², never pooled; every verdict is per footing
and a pass needs both. Cold energy is real gravitating mass (class A); no particle species is added. Not "theory closed".
Nothing here says the data favour the framework. No downloads. One core (`OMP_NUM_THREADS=1 nice -n 10`), each process
< 1 GB, each PDE run < 5 min, no long grids, nothing heavy while the 1024³ job is live. Inputs read only; no other lane edited.

## 0. Why (record context)

- CFG913: no law α(local variables) in ρ_m/ρ_Λ, g/a0, y_J, q, δ, 𝓜 meets mergers (α ≈ 0; CFG623/639/641), galaxy settling
  (α ≳ 0.5; CFG598, causality ≤ 1.186, CFG542) and retained dense dwarf clumps (α ≲ 1e-2; CFG882/889) at once; a feasible law
  needs a variable outside that list. Common cause: a galaxy's dense inner region must stay mobile to finish settling.
- CFG914: the open excesses (dwarfs, red lenses, cluster cores) do not order by local density; system type does.
- H-POP proposes a non-local history variable: the population label.

## 1. Naming caveat (load-bearing)

In the record, "tethered" (CFG698 J3, CFG722, CFG747/776, canonical S2–S4) means cold energy held at the law's profile by the
tether push, i.e. the population that SETTLES; "free/untethered" means the collisionless component the push does not act on
(CFG776's lasting constraint: a persistent excess must be such a component). H-POP as posed uses the words the other way round
by mobility: its "tethered" population is collisionless (α_t ≈ 0) and its "free" population settles. To avoid a clash this lane
writes **t** (H-POP "tethered" = bound into a structure at its formation, immobile) and **f** (H-POP "free" = arrived later,
or released, mobile). Dynamically t belongs to the record's untethered/collisionless class and f to the record's settling class.
H-POP's new content is the ASSIGNMENT RULE (by history), not the existence of two classes.

## 2. H-POP, frozen

- **Two labels, one medium.** ρ_c = ρ_t + ρ_f; both gravitate; both count toward the law's target (∇²ψ = 4πG(ρ_ph − ρ_t − ρ_f),
  or the one-sided cumulative deficit of the G model); no species.
- **Mobility by label, not by local state.** Drift v_s,X = −α_X 1_B τ∇ψ for X ∈ {t, f}, τ = (4πG(ρ_b + ρ_t + ρ_f))^(−1/2).
  α_t = 0 exactly (t moves only under gravity, i.e. collisionlessly). α_f ∈ {0.5, 1.0} (the record's existing O(1) coefficient
  at its G-passing values; 1.0 = CFG542's causal maximum at q → 1; not new constants). Each constraint keeps its source lane's
  drift form (G: CFG598 one-sided P0; M: CFG623 two-sided; D: CFG882/889), as CFG913 did.
- **Label rules (two, both graded):**
  - **L0 (literal; primary).** At a structure's formation epoch t_form, all cold energy inside its bound region
    B = {r < r_ta(t_form)} is relabelled t (formation snapshot). Before t_form everything is f. Cold energy arriving later
    (catchment inflow) is f forever. t_form := the half-mass epoch, X_ta(t_form) = 0.5 (the record's α_sup convention,
    CFG598 README:62–64). **New: the convention X_form = 0.5 (flagged as a constant-like choice).** No rate constant.
  - **LC (capture).** From the start, f → t instantaneously in every cell inside B that is settled (ρ_t + ρ_f ≥ ρ_ph) and
    has no deficit inside it (cumulative deficit through its inner face = 0, i.e. where the one-sided drift has stopped).
    **New: the capture rule (no rate constant; a finite-rate capture would add one, Γ_cap, not run).**
  - **Release (t → f).** None in either graded rule. Release by gas expulsion (H-EX type) or by tidal stripping is a declared
    variant evaluated by mapping only (§4 D, §5): any release rule is a new rule.
- **Settled state of a galaxy (stated before computing).** LC: the law's profile inside the settling front, all t, with f in
  transit at/beyond the front; overfill (t) is retained wherever the phantom later falls (baryon loss, sub-additive mergers,
  shrinking Newtonian-core phantom). L0: the formation snapshot (the law at t_form inside the front, plus in-transit cold
  energy inside r_ta(t_form), frozen) plus f filling today's deficits; t overfill retained wherever t exceeds today's phantom.

## 3. The three constraints (numbers as committed; reproduced by K-tests, §7)

- **M:** CFG623 (all-baryon source, ungated): α = 0 ALLOWED both footings (Z_B +1.09/+1.06, Z_H +1.47/+1.44); 0.1, 0.3, ∞
  EXCLUDED; 0.03 Z_B +3.12/+2.65. Rule (CFG623 FROZEN_CRITERIA.md:44–46): Z_B = (f − 0.045)/0.125, ALLOWED iff scorable,
  |Z_B| < 2, |Z_H| < 2 (Harvey σ 0.07). CFG641 (stars-only source + gate): arm S (RI) every node ALLOWED, arm P (RN) every node
  EXCLUDED, gate off 99.96% (α plays no role).
- **G:** CFG598 MW P0 (i): min q ≥ 0.99 for r ≤ 30 kpc AND M_c/M_ph(<30) − 1 ≤ 0.01; α = 0.25 fails (0.9842/0.9849), 0.5 passes
  (0.9928/0.9930). Causality α_max 1.000 (q = 1) / 1.1864 (CFG542).
- **D:** CFG882 ungated α_c ≤ 1.37e-3, α_50 6.2e-4–1.02e-3; CFG889 gated α·t_50 = 105.5–147.5 Myr → α_D,gated 0.88–1.23e-2;
  clump CFG877 (σ 7.53 km/s, M_cl 5.25e6/4.24e6 M_⊙).

## 4. How each constraint is evaluated for H-POP

**G (graded; two-population G-test).** CFG598's MW P0 PDE (`cfg598_lib`, read-only import; N = 300; both footings) extended to
two labelled cell-mass arrays m_t, m_f. Deficit, cumulative deficit D(<r), τ from the TOTAL cold mass; each label drifts with its
own α (donor-cell flux = ρ_X v_X A, last-trace rule per label); dt limits as CFG598 (CFL 0.4 over live donors of each mobile
label; Γ dt ≤ 0.2 with Γ = 4πG ρ_c,tot τ α_X over cells where label X is live). Deposits are f. L0: snapshot at the first step
with t ≥ t_form (cells with inner face < r_ta(t_form): m_t += m_f, m_f = 0). LC: capture applied after every flux step and every
deposit. α_f → ∞ (report-only bracket, "transport-unlimited"): f-only analogue of CFG598's `settle_inf` (pool m_f from the first
deficit cell outward inside B; refill inside-out to need_f = max(m_ph − m_t, m_f)). Reported per run: min q (r ≤ 30), max q,
M_c/M_ph(<30), f share of the cold mass inside 30 kpc, steps, cap hit, mass error.
- **G(rule) PASS** iff CFG598's (i) holds on BOTH footings at the same α_f ∈ {0.5, 1.0}. Otherwise FAIL.
- Report-only brackets: α_f → ∞; L0-early (t_form = start, X = X[0], i.e. only the initial content is t), α_f 0.5 and 1.

**M (graded at first order; mapping + mixture bound).**
- (a) Mapping. The record's passing merger configurations have effectively all cold energy immobile (CFG623 α = 0; CFG641 arm S
  gate off 99.96%). LC's settled t is the law-settled progenitor profile that CFG623's α = 0 runs use; L0's t profile differs
  (approximation, flagged).
- (b) First-order mixture tolerance (declared approximation: the lens statistic is linear in the mass mixture; the mobile
  fraction sits at the α = ∞ configuration, since α ≥ 0.3 already gives f ≈ f(∞)): φ_lin,B = (0.295 − f(0))/(f(∞) − f(0)) and
  φ_lin,H = (β_max − β̄(0))/(β̄(∞) − β̄(0)), β_max = β_obs + 2·0.07, β_obs = β̄(0) − 0.07·Z_H(0) (checked constant across nodes to
  ±0.005), per footing, from `cfg623_results.json`. Reported also with the α = 0.3 node in place of ∞. For two separated
  components the peak moves less than the centroid, so φ below φ_lin is safe at first order; above it is NOT decided.
- (c) H-POP's predicted mobile fraction. Two-population runs (same code) of CFG598 grid hosts log M_ta = 15 and 14 (h units;
  the closest grid hosts to the Bullet main 1.5e15 and sub 1.5e14), P0, both footings, rules L0 and LC, α_f 0.5 and 1.0:
  φ_f,core = f share of the cold mass inside 200 kpc (the CFG623 window scale) at t0; also inside 0.1 r_ta and 500 kpc.
  Caveat (declared): CFG598 grid hosts have point-mass baryons and an inherited EPS (ΛCDM-background, PROVISIONAL) accretion
  history; it is the record's own G model, used here only for the label split.
- **M(rule) = CONSISTENT (first order)** iff max over {log 14, log 15} of φ_f,core ≤ φ_lin,H on both footings at an α_f that
  passes G (if G passes at neither, both α_f are reported and the label uses the larger φ_f,core). Otherwise **UNDERDETERMINED**
  (the two-population merger run of §9 decides). First order never EXCLUDES.
- (d) CFG641 (report only): RI allowed / RN excluded means that in the stars-only branch any collisionless (t) reservoir in the
  merging cores must trace the baryons; H-POP does not fix the t reservoir's profile (P0 placement leaves captured overflow where
  it was deposited, i.e. diffuse). Not graded (different source model).

**D (graded by record mapping).**
- Retention: α_t = 0 makes CFG882's exact law Γ_t = α_t q/τ = 0 and removes the drift that eroded the clump along orbits in CFG889
  (no-OU runs eroded the same: the drift is the cause). Satisfied iff the clump is t: under LC (settled overfill is captured)
  and under L0 iff the overfill was created after formation from t (D-i below).
- Amount (what sets it). D-i (H-POP's own route): t settled to the law at formation, baryons later lost, t retained ⇒ overfill.
  Deep-regime, t-dominated relations (declared order-of-magnitude): M_obs/M_law = (M_b,form/M_b,now)^½ and V_x² =
  √(Ga0)(√M_b,form − √M_b,now). D-ii (t = cold energy collapsed at the assembly epoch, H-PRIM) is EXCLUDED by CFG845 and is not
  available to H-POP. Computed: the loss factor e^{4E} from CFG827's out-of-sample per-dwarf E (median, 16–84%); M_b,form from
  CFG890 M5's V_x for M_b,now = 1e3, 1e5, 1e7 M_⊙.
- Pre-declared readings (D-i): CFG880 per-dwarf scatter → needs per-dwarf loss variation (allowed, unmeasured input); CFG827 age
  independence → no contradiction unless loss tracks age; CFG843 host independence → no contradiction (loss internal/early);
  CFG883 no clump in globulars → t ≈ 0 for systems formed at g ≫ a0 or inside a host's field (no contradiction; NGC 1851 noted);
  CFG845 SPARC rotating dwarfs (D −0.273 ± 0.026 vs H-PRIM) → requires no net loss in gas-rich rotators (consistent) and
  excludes D-ii; CFG860/873 gas-bearing isolated dwarfs above the law → requires early loss there too (prediction, not a
  contradiction: no independent removed-baryon measure, CFG846); CFG829 blue lenses on the law, red above → loss in red only.
- **D(rule) = CONSISTENT (conditional on α_t = 0 and on unmeasured formation-epoch baryon masses)** unless one of the listed
  results contradicts D-i, then CONTRADICTED naming it. Release variants (gas-expulsion or stripping release of t) are
  evaluated by mapping: a release that frees the overfill erases the D-i clump (drift α_f ≫ α_c).

## 5. Corollaries beyond the three constraints (necessary consequences checked against the record)

- **C1 merger memory (CFG726 H-MM).** t is collisionless and retained, so a remnant keeps its progenitors' t; f fills deficits
  only. Under LC this is H-MM's formula M_b + max(Σ T_i, T_rem) with T_i = each progenitor's settled halo to its supply edge
  (an IDENTITY, given CFG598's α ≥ 0.5 hosts reach their supply edge). CFG726 (POST-HOC lane; 3 VOID controls that touch no
  failing score) FAILS T-R eRASS1 OUTER (Z −3.63/−4.05), T-A ACCEPT OUTER (Z −4.83/−5.19), T-E eFEDS. Identity ⇒ C1 can
  CONTRADICT. Under L0 the members' t is their formation snapshot; in the deep regime with every edge beyond r, Σ φ_t √f_i with
  φ_t = √X_form = 0.707 equals CFG726's N_mem × 0.5 bracket (Σ√f ∝ √N); that bracket fails T-R OUTER (Z −2.50/−3.19) and T-A
  OUTER (Z −3.13/−3.59). Approximate mapping (finite edges and frozen in-transit mass differ) ⇒ **AT RISK**, not a contradiction.
- **C1b minor accretion (CFG726 T-S2, declared vulnerability there):** accreted pieces keep their t (both rules) ⇒ disc V rises
  ×1.04 / ×1.12 / ×1.37 for 1% / 3% / 10% accreted in 1% pieces. Not scored by CFG726 ⇒ AT RISK only.
- **C2 frozen relic (CFG777)** fails 0/3 in the condensed-baryon framework; whether it maps onto H-POP depends on the law's source.
  Report only.
- **C4 record dynamics (CFG747/776):** the record's push expels surplus; H-POP's α_t = 0 is the posit that it does not act on t
  (allowed by CFG776's lasting constraint). New assumption, not a contradiction. **C5 CFG722 Q1 (conditional):** a ballistic
  collisionless carrier is a particle species in the identified-carrier dictionary; H-POP's t inherits this open issue. Flagged.

## 6. Classes

Per rule (L0, LC):
- **CONTRADICTED** if G FAILS (breaks CFG598 MW (i)), or D is contradicted, or an identity corollary fails (C1 under LC breaks
  CFG726). The record result(s) broken are named; all failing items are listed, not only the first.
- else **UNDERDETERMINED** if M is UNDERDETERMINED (spec §9; script written then, queued after the 1024³ job, not run).
- else **CONSISTENT WITH ALL THREE**, with its new constants/rules listed and AT RISK corollaries listed.
**Overall H-POP** = the best class over the two declared rules (CONSISTENT > UNDERDETERMINED > CONTRADICTED); both reported.
Two rules = two chances; disclosed.

## 7. K-tests (a failed K-test is reported FAIL and not loosened)

- K-M1 CFG623 cells: 0 ALLOWED both; 0.1, 0.3, ∞ EXCLUDED both; Z_B(0.03) 3.12/2.65 (±0.01); β_obs constant across scorable
  nodes to ±0.005.
- K-M2 CFG641: arm S status ALLOWED for every node both footings; arm P EXCLUDED for every node both; T_G gated-off 0.9996;
  RN canonical main reservoir share 0.87 (±0.01).
- K-G1 CFG598 MW P0 min q: 0.25 → 0.9842/0.9849, 0.5 → 0.9928/0.9930 (±1e-4).
- K-G2 the two-population code with no t (all f) reproduces CFG598's MW P0 min q, max q, M_c/M_ph(<30) at α = 0.5, 1 and ∞ on
  both footings to ≤ 1e-9 relative.
- K-G3 the same for grid hosts log 15 and 14 (P0, α 0.5): S and M_c at 0.1 and 0.5 r_ta equal `cfg598_results.json` runs to
  ≤ 1e-9 relative.
- K-C CFG542 α_max 1.000 / 1.1864 (±1e-3).
- K-D1 CFG882 α_c max 1.37e-3 (±0.01e-3), α_50 6.2e-4..1.02e-3. K-D2 CFG889 α·t_50 105.5–147.5 Myr (±1) over 8 cells.
- K-R (record numbers used in D and C): CFG827 OOS N 28, 25 above, mean E 0.375 (±0.005), ρ 0.089 (±0.005); CFG880 ŝ 0.38 both
  footings; CFG843 c 0.055 ± 0.117 (±0.001); CFG845 D −0.273 ± 0.026; CFG860 canonical base a+c0 0.285 ± 0.108 and a+cG
  0.370 ± 0.073 (±0.005; if no base key exists the README numbers are compared to the nearest stored variant and the K-test is
  marked PARTIAL); CFG829 blue A 1.016 ± 0.086, red 1.587; CFG726 Z values quoted in §5 (±0.01) and verdict strings FAIL; CFG890
  M5 V_x 6.48/6.29 km/s (±0.01) if stored.

## 8. MUTATE (separate outputs `cfg915_MUTATE.out`, `cfg915_results_MUTATE.json`; exit 1 when the tooth bites)

Swap the labels' mobilities: α_t ∈ {0.5, 1.0}, α_f = 0.
- G: the two-population MW G-tests re-run swapped for L0 and LC, both footings.
- M: swapped mobile fraction φ_mob = 1 − φ_f,core (log 14, 15). φ_mob ≥ 0.9 ⇒ maps to CFG623's single-α nodes α ≥ 0.3 (EXCLUDED
  both footings) ⇒ M FAILS; else φ_mob > φ_lin,B ⇒ fails at first order.
- D: the clump (t) then drifts at α ≥ 0.5 ≫ α_c = 1.37e-3 ⇒ eroded (CFG882) ⇒ D FAILS.
- **Tooth:** bites (per rule) iff the swapped hypothesis fails at least one of M, G, D that the unswapped hypothesis did not fail.
  If it does not bite, that is reported as frozen.

## 9. Heavy run (only if a rule ends UNDERDETERMINED on M; spec frozen now, script written then, NOT run here)

Two-population merger stopwatch: CFG623's pipeline (CFG622 simulator read-only, CFG623 calibration v0 2666.7 km/s, η 1.132,
window, stability rule, scores unchanged). Each progenitor's cold elements are labelled f with probability φ_f(r) taken from
§4(c) (log 15 profile for the main, log 14 for the sub, per rule, per footing, at the G-passing α_f), the rest t. f elements drift
at α_f, t at 0. Runs: the rule(s) left UNDERDETERMINED × α_f × both footings, plus controls φ_f ≡ 0 (must reproduce CFG623 α = 0
exactly) and φ_f ≡ 1 (must reproduce CFG623's α_f node). Verdict per CFG623's rule. Queue with a waiter: no 1024³ run live,
≥ 16 GB free, ≤ 4 processes, after the T1x/NC1x chain.

## 10. Pre-freeze hand values (disclosed; not verdict inputs)

From README numbers only: φ_lin,B ≈ 0.135 / 0.134 and φ_lin,H ≈ 0.039 / 0.041 (canonical / alt). In CFG598's point-mass grid
hosts the 200-kpc core of a log-15 host is near-Newtonian (y ~ 4), where the ν_e phantom shrinks as baryons grow, so φ_f,core
may be small under both rules. G: the frozen t leaves only the f population to carry late inflow through the settled interior;
whether that holds q ≥ 0.99 is not obvious (a hand flux estimate gave anything from q ≈ 0.98 to ≈ 1); expectation uncertain,
with LC expected no better than L0. C1 under LC is an identity with H-MM, so the expected overall class is CONTRADICTED unless
L0 survives G and M.

## 11. Disclosures and not claimed

Not blind: every source verdict (CFG598, 623, 641, 726, 777, 827, 845, 860, 880, 882, 883, 889, 913, 914) was read before this
file. No PDE has been run for this lane. Not claimed: that H-POP is derived; that any α_f or X_form is measured; κ derived;
"theory closed"; that the data favour the framework.
