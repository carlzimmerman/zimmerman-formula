# CFG937 FROZEN CRITERIA: two-floor primordial halos (H-CF2), an atomic-cooling floor for systems quenched at reionization and a post-reionization filtering floor for systems that kept forming stars

- **Date:** 2026-10-20. Block 930–939 (LEDGER row "CFG930–939", 10-20 ~20:00 entry names CFG937). Agent lane.
- **Kind:** HYPOTHESIS TEST that builds on CFG934. One new rule (the SFH-selected second floor), zero new fitted constants.
  Every declared input is a bracket or a record value, never fitted.
- **Settings:** κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 m/s² are scored separately and never pooled. The extra
  mass is cold energy, not a particle species. Verdicts use raw data and framework-native inputs only. No Moster, Behroozi,
  ΛCDM mass function, abundance matching or Dutton–Macciò c(M) enters any verdict; CFG42's Moster + Dutton–Macciò inputs appear
  ONLY in the K1 reproduction test (as in CFG934). Not "theory closed". Nothing here can say the data favour the framework.
- These criteria are committed ALONE, before any CFG937 script exists and before any CFG937 number is computed. Any later change
  is a dated, labelled amendment in a separate file.

## 0. Disclosure (not blind)

**H-CF2 was formed AFTER CFG934's result** (criteria 9782c3df7, results e8bb2ae70, README and post-hoc diagnostic). Seen before
freezing: everything in CFG934's README, `cfg934.out`, `cfg934_posthoc.out` and `cfg934_results.json`; in particular that the
cooling floor closes the MW ultra-faints at the ionised τ50 corners, leaves the classicals, M31 dSphs and SPARC untouched, and
leaves the intermediate dSphs (−10 < M_V ≤ −7.7) at +0.24 to +0.36 ln because f_ex = 0 there (Draco: edge phantom 8.2e8 vs
cold floor 3.4e8 M☉), so LVD-83 is CONTRADICTED at 11 of 12 corners. Also seen: CFG42/CFG45 (as disclosed in CFG934 §0),
CFG782 (photo-evaporation selector, V_th = √2 c_s(T_IGM), DEAD: it flags ~half of M31's satellites), CFG784 (not run; its
z_f = 8 from CFG336, 6/10 reported), THEORY_CANONICAL_2026-10-16 ("photo-evaporation selector removed"), CFG923 (Weisz grid's
first node 12.59 Gyr; the record's onset mapping, F = 0 at 13.3 Gyr), CFG933 and CFG936 READMEs.

**Relation to the removed S4 selector.** CFG782 used T_vir ≥ T_IGM as a selector for which systems' cold energy becomes FREE
(SUDDEN vs RETAINED, from the present-day V_init). H-CF2 does not revive that selector. It uses the same threshold only as a
lower bound on a star-forming system's primordial halo mass, applied by the system's own SFH. No cold energy is freed.

**Selector membership was counted before freezing** from `cfg934_results.json`'s z_f table (an input inspection; no H-CF2 number):
under the primary rule (§2.3) the only quenched objects are Hercules (U, L), Andromeda VII and Andromeda XIII (M31 LVD, L).
Every group default τ90 (CFG934 §2.4) lies below the 12.59-Gyr node, so every object without its own SFH is a late former,
including 28 of 31 MW ultra-faints. H-CF2 therefore acts, in practice, as "the filtering floor for almost every dwarf".

**Back-of-envelope arithmetic before freezing (no lane code, no sample prediction):**
- **E1.** V_th = √2 c_s(T_IGM), c_s = √(k T_IGM/(0.59 m_p)): 16.73 / 20.49 / 23.66 km/s at T_IGM = 1 / 1.5 / 2 × 10⁴ K (CFG782's
  committed values). The ionised cooling-floor velocity is 16.73 km/s and the neutral one 11.63 km/s. At fixed z the floor mass
  goes as V³: the filtering floor is ×1.84 (1.5e4) or ×2.83 (2e4) the ionised cooling floor, and ×2.97 / ×5.46 / ×8.41 the
  neutral one.
- **E2 (structural, stated before any number).** At T_IGM = 1e4 K the filtering velocity EQUALS the ionised cooling velocity.
  So at the corners (μ 0.59, T_IGM 1e4) H-CF2 reproduces CFG934's μ 0.59 corners exactly, for every object. Consequences under
  the frozen verdict rule (§4.1), over the full declared bracket:
  - (S): SURVIVES is unreachable (CFG934's L is CONTRADICTED at μ 0.59 / τ50 / C1500), and FAILS is unreachable (at μ 0.59 /
    τ50 / C6000 CFG934 has no class CONTRADICTED). The headline (S) verdict can only be PARTIAL or PARTIAL (corner-selectable).
  - (M): CFG934's μ 0.59 / τ50 / C6000 corner has all six classes CONSISTENT, so (M) is at least corner-selectable; SURVIVES is
    unreachable (CFG934 (M) U is CONTRADICTED at μ 0.59 / τ90 / C1500).
  The bracket is NOT narrowed to avoid this. Because the full-bracket verdict is fixed in advance, §4.2 adds a pre-declared,
  graded **upper-bracket question** (the corners where the second floor differs from CFG934), which can come out either way.
- **E3 (expectation).** From CFG934's post-hoc numbers at τ50 / C6000: Draco's cold floor 3.4e8 → 6.2e8 (1.5e4, f_ex still 0)
  → 9.6e8 (2e4, f_ex ≈ 0.15) against an edge phantom of 8.2e8; And IX 5.7e8 → 1.05e9 / 1.6e9 (f_ex ≈ 0.34 / 0.57) against 6.9e8;
  And V 4.4e8 → 8.1e8 / 1.24e9 (f_ex 0 / ≈ 0.12) against 1.1e9. Expected: under (S) the filtering floor reaches part of the
  intermediate dSphs only at the hot end, with small f_ex, so the LVD-83 class is expected to stay above the law at most corners;
  the faint end (CFG934's best corner +0.02) and the ultra-faints (CFG934's best −0.066 dex) are expected to be pushed below the
  law at the hot, dense corners. (M) is expected to do more for the intermediate dSphs, and to over-predict the faint end sooner.
- **E4.** The record's onset mapping (CFG920/CFG923: cumulative SFH F = 0 at 13.3 Gyr, linear in log t to the 12.59-Gyr node)
  gives every dwarf at least about 36% of its stars after z = 6 and about 76% after z = 8. Under that mapping every dwarf is a late former (V11).

## 1. Hypothesis H-CF2 and posits

**H-CF2.** As in CFG934, cold energy is ordinary cold collisionless matter before any bound system exists (CFG649/CFG654) and
collapses into primordial halos; a system forms stars only if its halo reached T_vir = 1e4 K (the atomic-cooling floor). In
addition, a system that **kept forming stars after reionization** must have sat in a halo that could keep accreting photo-heated
IGM gas: its virial velocity at its formation epoch must reach the post-reionization filtering threshold V_th = √2 c_s(T_IGM)
(the record's own retention condition T_vir ≥ T_IGM, CFG782). Systems **quenched at reionization** need only the cooling floor.
H-CF2 assigns each dwarf the minimal halo its own SFH requires (any larger mass would need an assembly history, i.e. a parameter).

| posit | status | value / source |
|---|---|---|
| **second floor for late formers: collapse mass = max(M_cool, M_filt) at z_f; quenched: M_cool** | **NEW (the only new rule)** | this lane |
| filtering threshold V_th = m c_s(T_IGM), c_s = √(k T_IGM/(μ_f m_p)) | record (CFG782's retention condition) | m = √2, μ_f = 0.59 (ionised IGM) |
| T_IGM | record BRACKET (CFG782; measured Lyα-forest range) | {1.0, 1.5, 2.0} × 10⁴ K |
| selector: late former iff τ90 < 12.589 Gyr (the first Weisz node, z 4.96) | declared rule (§2.3) | Weisz+14 τ90 (CFG824's rule), CFG934's defaults |
| z_reion | declared BRACKET, inert under the primary rule (§2.3) | 6–8 (record: z = 8, CFG336/CFG784) |
| everything else (T_vir = 1e4 K, μ, z_f = τ50/τ90, Δ_vir, NFW with ρ_s = C ρ̄_m(z_f), C, native background, f_ex, CFG35 edge, readings (S)/(M), estimators, class statistics) | inherited from CFG934 unchanged | CFG934 §1–§3 |

## 2. Construction

### 2.1 Inherited (CFG934, unchanged)
Every CFG934 definition is reused by executing `CFG934_cooling_floor_halos/cfg934.py` read-only up to its K section (the same
method as CFG934's own post-hoc script), with builtins.open replaced by a read-only wrapper during that exec so that no CFG934
code can write. No CFG934 file is edited. Inherited: native CFG654 background (h, Ω_m, Ω_r, f_b), Δ_vir(z_c) = 8 Δ_ta(z_ta)
[(1+z_ta)/(1+z_c)]³, M_cool(z) = (2kT/(μ m_p G))^{3/2} (4π/3 Δ_vir ρ̄_m(z))^{−1/2}, the truncated NFW with ρ_s = C ρ̄_m(z_f),
z_f from Weisz+14 τ50/τ90 (CFG824's rule; CFG934's group defaults for missing SFH), SPARC z_f = 0, the readings (S) and (M),
f_ex = max(0, 1 − M_ph,edge(M_b)/((1 − f_b) M_floor)), and the class estimators and statistics U, C, M, I, S, L.

### 2.2 Filtering floor
- V_th = m c_s(T_IGM) with m = √2, μ_f = 0.59, so V_th² = 2 k T_IGM/(0.59 m_p) (CODATA constants of CFG934).
- **M_filt(z) = (V_th²/G)^{3/2} (4π/3 Δ_vir(z) ρ̄_m(z))^{−1/2}**, i.e. CFG934's M_cool formula with T → T_IGM and μ → 0.59.
  Same r_vir, same NFW, same concentration rule (c depends only on Δ_vir, C and z; not on M).

### 2.3 Selector (status per object, from its SFH)
- **L (late former)** iff τ90 < 12.589 Gyr (= 10^10.1 yr, the first node of the Weisz+14 grid, z = 4.96): at least 10% of its
  stars formed after the first epoch the data resolve. **Q (quenched at reionization)** iff τ90 sits at that node (the cumulative
  fraction at 12.59 Gyr is ≥ 0.9).
- τ90 is the object's own Weisz+14 value (CFG824's rule) or CFG934's default (median of the same host group × luminosity class).
  The status is a property of the object; the same status applies at the τ50 and τ90 corners.
- **z_reion** is declared as the bracket 6–8. Its native lookback (12.84–13.13 Gyr) lies beyond the grid's first node, so the
  data cannot place any star between z_reion and z = 4.96; the selector reads "≥ 90% formed before the first resolvable node" as
  "quenched at reionization". The z_reion bracket is therefore inert under the primary rule (disclosed; asserted in K4).
- **SPARC dwarfs:** L (star-forming today), z_f = 0 (CFG934's conservative rule).

### 2.4 Floor rule
- Q: M_floor = M_cool(z_f; 1e4 K, μ) (CFG934).
- L: M_floor = max(M_cool(z_f; 1e4 K, μ), M_filt(z_f; T_IGM)), the larger virial velocity at the same z_f. With m = √2 and
  μ_f = 0.59, M_filt ≥ M_cool always (equal at T_IGM = 1e4 and μ = 0.59).

## 3. Classes, estimators and statistics
Identical to CFG934 §3 (U MW ultra-faints, C MW classicals, M M31 dSphs (Collins+13 and M31 LVD, the more severe), I CFG874's
11 isolated LG dwarfs with gas counted, S CFG42-H4's 110 SPARC gas-rich dwarfs, L CFG880's LVD-83), with each class's statistic
and error as in CFG934. **Class rule:** z = statistic/error; |z| < 2 CONSISTENT; 2 ≤ |z| < 3 TENSION; |z| ≥ 3 CONTRADICTED
(negative = over-predicted). S: fraction ≥ 0.90 CONSISTENT; 0.75–0.90 TENSION; < 0.75 CONTRADICTED.

## 4. Verdict

### 4.1 Headline (full declared bracket)
- **Corners (per footing, per reading):** μ {0.59, 1.22} × τ {τ50, τ90} × C {1500, 3000, 6000} × T_IGM {1.0, 1.5, 2.0}e4 = 36.
- **H-CF2 SURVIVES:** every class (U, C, M, I, S, L) CONSISTENT at every corner on both footings, reading (S), zero fitted
  constants. **FAILS:** at least one class CONTRADICTED at all 36 corners on at least one footing, reading (S). **PARTIAL:**
  otherwise, labelled "corner-selectable" if at least one corner has all six classes CONSISTENT on both footings. Choosing such a
  corner is a discrete fit, not a survival; the **corner spread** is reported (the number and list of all-CONSISTENT corners per
  footing, per-class label counts, and the counts per T_IGM value).
- (M) gets the same rule as the alternative verdict; the headline is (S). E2 states which outcomes are reachable.

### 4.2 Upper-bracket question (graded, pre-declared because of E2)
- The 24 corners with T_IGM ∈ {1.5, 2.0}e4, where the second floor differs from CFG934 for the late formers. Same rule:
  **SURVIVES-UPPER / PARTIAL-UPPER (corner-selectable) / FAILS-UPPER**, reading (S) headline, (M) reported.
- Reading fixed now: SURVIVES-UPPER would mean "the two-floor rule holds if the post-reionization IGM was at least 1.5e4 K", a
  result conditional on part of the declared bracket, NOT a survival of H-CF2. FAILS-UPPER would mean the filtering floor cannot
  repair the failing class even at the hot half of the record's T_IGM bracket.
- Also reported (no grade): every class statistic at each upper corner minus CFG934's at the same (μ, τ, C).

### 4.3 Variants (reading S; any variant that changes the headline (S) verdict or the upper-bracket (S) verdict marks it FRAGILE)
- V1 Δ_vir = 18π²; V2 onset z_coll (13.3 Gyr); V3 Υ_V 1 and Υ_V 4 for I and L; V4 CFG930's uniform recipe (Υ ×½–×2 floor on I
  and L errors); V5 CFG827's Υ_SFH for I and L; V6 luminosity-class τ default (all as CFG934).
- **V7** selector by τ50: L iff τ50 < 12.589 Gyr (most stars after the first resolvable node).
- **V8** own-evidence selector: L iff the object has its own Weisz+14 τ90 below the node or holds HI (M_HI > 0 in its row);
  otherwise Q; SPARC L.
- **V9** m = 1 (V_th = c_s); **V10** m = 2 (V_th = 2 c_s).
- **V11** the record's onset mapping (E4): every dwarf L.

## 5. Controls (run first; the lane stops and reports no class if any K fails)
- **K0** CFG934's committed K passed (`cfg934_results_K.json` K_all true); sha256 of `cfg934.py` printed.
- **K1** CFG42 reproduced through the inherited generic estimator with CFG42's own inputs (CFG934's K1 replayed): 60 UF/CL
  numbers and H4 to 1e-9 against `CFG42_satellites_rule_results.json`; **K1b** CFG45's (M) reading to 1e-6.
- **K2** CFG934 reproduced with the **second floor switched off** (every object Q, SPARC at the cooling floor): every number in
  `cfg934_results.json` "corners" (S and M, 12 corners, both footings) and "bare_law" to 1e-12, identical labels, identical (S) and
  (M) verdicts, and identical verdicts for CFG934's six variants.
- **K3** record IGM quantities: V_th at T_IGM 1 / 1.5 / 2e4 equals CFG782's formula with CFG782's constants to 1e-5 (relative)
  and its printed 16.73 / 20.49 / 23.66 km/s to 0.005 km/s; M_filt(T_IGM 1e4) equals M_cool(μ 0.59) exactly; V_vir(M_filt) =
  V_th to 1e-10.
- **K4** selector inputs: the selector's τ90 equals CFG824's committed tau90 for every CFG824 object (1e-12); "τ90 at the node" ⇔
  "Weisz f(12.59 Gyr) ≥ 0.9" for every Weisz object; the native lookbacks of z = 6 and z = 8 exceed 12.589 Gyr (z_reion inert).
- **K5** the sealed prediction's synthetic estimator (§6) equals the L class estimator's boost for the real 83 at one corner per
  reading (1e-12).

**MUTATE** (separate outputs, after K, before the seal and main):
- **MUTATE_EQ** (filtering floor := cooling floor: T = 1e4 K and μ = the corner's μ): every class number at all 36 corners equals
  CFG934's at the matching (μ, τ, C) corner to 1e-12, both readings, both footings.
- **MUTATE_T10** (T_IGM × 10): must over-predict. Reading (S), every corner, both footings: U, C, M (Collins+13 and M31 LVD
  separately), I and L each with statistic < 0 and z ≤ −2, and S not CONSISTENT. Else the control did not fully bite: the failing
  cells are listed and the affected class is flagged as having limited power to detect over-prediction (CFG934's T100 had this
  for M and C at some corners; expected again, disclosed here).

## 6. Sealed prediction P937 (an untested class; produced before the main run)
- **Class:** gas-free dwarf spheroidals with a resolved CMD-based SFH and a stellar σ, none of which is in any sample used by the
  record (CFG42, CFG874, CFG880/LVD-83, CFG933, CFG936), e.g. future discoveries. Split by the selector: **Q** (f(12.59 Gyr) ≥ 0.9)
  vs **Lm** (formed most stars after reionization: τ50 < 12.589 Gyr).
- **Quantity:** ΔE = ⟨ln(σ_obs/σ_law)⟩_Lm − ⟨ln(σ_obs/σ_law)⟩_Q at matched M_V and r_h, σ_law from CFG880's estimator (Υ_V 2, ν_e).
- **H-CF2 prediction:** ΔE_pred = E_pred(Lm) − E_pred(Q), E_pred = ½ ln(σ_pred²/σ_law²), on the grid M_V ∈ {−5, …, −11} (step 1),
  r_h ∈ {100, 200, 300, 500} pc, no gas, all 36 corners, both footings, both readings. Templates: Q has τ50 = τ90 = 12.589 Gyr;
  Lm has τ50, τ90 = the medians over Weisz+14 objects with an LVD row and τ50 < 12.589 Gyr (SFH table only; no σ data).
- **Sealed statements:** the range [min, max] of ΔE_pred over the 36 corners per grid point, footing and reading, and its value in
  the bins −10 < M_V ≤ −7.7 and M_V > −7.7. **Kill line:** with ≥ 5 dwarfs per group matched within 0.5 mag and 0.15 dex in r_h,
  H-CF2's two-floor rule is excluded on a footing if the observed ΔE lies outside [min − 2 se, max + 2 se] of the (S) prediction
  evaluated with the sealed function at the sample's own M_V, r_h and SFHs (the template table applies when SFHs give only the split).
- **Sealing:** a SEAL mode writes `cfg937_SEALED_P937.json` from the model alone (synthetic grid; no σ data exists for this class);
  its sha256 is printed and committed (with the script and the K/MUTATE outputs) before the main run.

## 7. Reported separately, ungraded
- **LVD-83 by luminosity** (declared now, so not post hoc): mean E in M_V ≤ −10, −10 < M_V ≤ −7.7, M_V > −7.7 and the number with
  f_ex > 0 per bin, every corner, both readings; edge phantom vs cold floor and f_ex for Draco, Andromeda IX, Andromeda V, Bootes I,
  Segue 1 at each T_IGM.
- **CFG880 scatter:** ML intrinsic scatter s_int of E_i under the bare law, H-CF2 (S/M) at each corner and CFG877's universal
  clump; Spearman ρ between H-CF2's predicted boost and the observed excess.
- **Coma UDGs** (CFG933's 9): H-CF2 prediction at z_f ∈ {0, 0.5, 1, 2, 3, 5}, both statuses, every μ / T_IGM / C, (S) and (M),
  against E_obs.
- **DF2/DF4 and tidal dwarfs** (CFG933, CFG936): no primordial halo, so E_pred = 0; compared with the recorded deficits; what a
  floor halo would give DF2/DF4 under either status (z_f scan).
- Selector membership per class; the floor masses (M_cool, M_filt, r_vir) on a z grid; per-object status, τ, z_f and floor masses.

## 8. Compute and repository rules
One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, each process under 1 GB (in-script RSS guard: abort above
900 MB); no downloads; other lanes' code exec'd read-only, their JSON only read. Modes and outputs: `CFG937_MODE=K` →
`cfg937_K.out` / `cfg937_results_K.json`; `MUTATE_EQ` and `MUTATE_T10` → `cfg937_MUTATE_EQ.out` / `cfg937_results_MUTATE_EQ.json`
and `cfg937_MUTATE_T10.out` / `cfg937_results_MUTATE_T10.json`; `SEAL` → `cfg937_SEAL.out` / `cfg937_SEALED_P937.json`; `main` →
`cfg937.out` / `cfg937_results.json`. MUTATE, SEAL and main refuse to run unless K passed. Commits with explicit paths only; no
push; no edits to the LEDGER, THEORY_CANONICAL files, CFG934's files or any other lane's files.

κ = ½ FITTED; footings never pooled; cold energy, not a particle; not theory closed.
