# X64_oblique_object_keys — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane id: X63 was taken (X63_displacement_forest_prediction), so this lane is X64.

**Question.** Does any physically meaningful COMBINED (oblique) object variable separate the classes that must RETAIN
cold dark energy {dwarfs, groups, clusters} from those that must be EXCLUDED from it {L* galaxies and lenses}?

**Why.** X58_object_keyed_switch (c3b4f2c7d9) found the retention pattern the data need is non-monotone in mass: dwarfs
(M200 10⁸–10¹⁰ M☉) retain, L* lenses (10^11.35–10^12.05) follow the law with no halo, groups and clusters (≥ 10¹³)
retain. Already excluded as keys: mass (X58_object_keyed_switch), acceleration (X60_acceleration_dependent_cold_sector),
formation epoch (X59_formation_epoch_switch), local / Yukawa / coherence-scale forms (X57_exclusion_mechanism).
X57 left three unbuilt object keys: **K1** a phase-space key, **K2** a retarded nonlocal key, **K3** a bound-region
constraint. X19_selector_rank_test tested single catalogue variables and axis-aligned pairs only, against a different
(E-based) labelling. This lane tests single *combined* variables against X58's retention pattern.

**Environment is out of scope.** The environment-keyed switch is being tested by the peer lane
X62_environment_keyed_switch. No environment variable (ρ_env, hosted flag H, host field e, host potential term) enters
the candidate list; where X19's |Φ| contains a host term, this lane uses the internal potential only (§3); the
host-inclusive form is reported only.

Standing rules: κ = ½ FITTED. Footings canonical (a₀ = 9.3603e-11 m s⁻²) and alt (a₀ = 1.1312e-10 m s⁻²), never pooled.
"Cold dark energy" is the gravitating w ≈ 0 clumping field component; it is not matter and not a particle. Framework-
native only. No knob fitting: V* is read off as the centre of a gap between class intervals. Not "theory closed".
Nothing here may say the data favour the framework.

## 1. Classes and labels

Rows are X19's class table (`X19_selector_rank_test/x19_classes.csv`, members rebuilt by X19's own code, §5) plus one new
class, **KiDS lenses**, built from F2_outer_lensing's inventory (ASSUMPTION_LEDGER A2).

**Primary labelling P (X58's pattern, literal):**
- **RETAIN:** MW ultra-faint, bright M31, M31 others (the dwarf classes the law under-predicts at Z ≥ 2 in X58 / X19),
  Groups, Clusters T1, Clusters T2, Clusters T3.
- **EXCLUDED:** KiDS lenses, SPARC large, MW disc.
- **Unconstrained (shown, no verdict weight):** SPARC small, LG field, MW classical, Crater II, Antlia II, Coma UDGs,
  UMa members, TDGs, DF2/DF4, Cosmic background (not placeable on most candidates; its requirement is R1, §6).

**Reported labellings (no verdict weight):**
- **G (strict need):** P with Groups and Clusters T1 unconstrained (X19: the isolated law already fits them, Z < 1).
- **W (wide):** P plus MW classical → RETAIN; UMa members, TDGs, DF2/DF4, Crater II → EXCLUDED (each needs no more
  than the law, Z < −2 in X19, so a halo would worsen it).

Labels are the same on both footings (they are X58's requirement, not a per-footing Z).

## 2. Candidate variables (frozen list), with the mechanism stated before computing

All quantities per member, at X19's measurement radius r (pressure-supported: r_½ = 4/3 R_e; rotators: last measured
point / R_out / R₀; groups R_e; clusters 0.548 Mpc; lenses §A2), with X19's σ convention (σ_LOS; V/√2 for rotators;
√(kT/μm_p) for clusters) and baryonic M_b(<r), ρ_b(<r), M_b (total). Values compared in log₁₀. G = Newton's constant;
t_H = 13.8 Gyr (X19's convention); Σ_a₀ = a₀/(2πG).

| id | candidate | formula | key type and mechanism (why it could be a key) | verdict-bearing? |
|---|---|---|---|---|
| C1 | baryonic phase-space density | Q_b = ρ_b(<r) / σ³ | **K1.** A clumping field mode is captured only where the well is phase-space dense (a Tremaine–Gunn-like occupancy bound on a coherent component): retention iff Q above (or below) a critical value | yes |
| C1d | dynamical phase-space density | Q_dyn = ρ_dyn / σ³, ρ_dyn = 9σ²/(4πG r²) (Wolf mass M_dyn = 3σ²r/G in a sphere of radius r) ⇒ Q_dyn = 9/(4πG r² σ) | **K1**, same mechanism with the total (observed) well; depends only on r and σ | yes |
| C2 | virial ratio | σ² / \|Φ_int\| | **K3.** The component stays attached only inside a region whose kinetic-to-binding ratio is below a critical value (a bound-region constraint) | yes |
| C3a | crossing time over Hubble time | t_cross/t_H = (r/σ)/t_H | **K2.** A retarded nonlocal kernel with memory ~ t_H: an object whose crossing time is a sizeable fraction of t_H has not re-equilibrated with the background field, so it keeps (or loses) the component | yes |
| C3b | two-body relaxation time over Hubble time | t_rel/t_H = [N / (8 ln N)] · t_cross/t_H, N = M_b / 0.5 M☉ | **K1.** Granular two-body scattering by the baryons decoheres a coherent field mode; short relaxation erases retention | yes |
| C4 | baryon fraction × surface density | f_b · Σ_b / Σ_a₀, f_b = M_b(<r)/M_dyn(<r) (X19 V8), Σ_b = M_b(<r)/(π r²) | **K3.** A surface-density bound (X43's Σ_a₀ flag) weighted by baryon dominance: baryon-dominated regions above Σ_a₀ expel | **REPORTED ONLY**: f_b contains the observed dynamics that define the need (X19's by-construction risk) |
| C4L | law-fraction × surface density | (1/ν(x)) · Σ_b / Σ_a₀ | as C4 with the E-free law fraction 1/ν. **Identity stated now:** Σ_b/Σ_a₀ = 2x for a spherical mean, so C4L is a monotone function of x alone (X19 V4); computed to show it | yes (reduces to x) |
| C5 | halo dynamical age | A = [t₀ − t(z_f)] / t_cross(r), z_f = EPS half-mass formation redshift of the object's M200 | **K2.** Number of crossings since formation: a retarded key that retains while the object is dynamically young relative to the kernel (or the reverse) | yes |
| C6 | escape over circular speed at the a₀ radius | v_esc/v_c = √(2\|Φ_int\| / (ν(1) a₀ r_a₀)), r_a₀ = √(G M_b / a₀), ν(1) = (1+√5)/2 | **K3.** The component at the a₀ transition stays bound to the object only if v_esc exceeds v_c by a critical factor | yes |

Notes fixed in advance (no numbers):
- C3a is close to 1/N_orb (X19 V9, which failed X19's labels) up to class-dependent constants (√3σ vs V); it is tested
  here against X58's labels.
- A halo-scale phase-space density ρ₂₀₀/σ₂₀₀³ is monotone in M200 (ρ₂₀₀ fixed, σ₂₀₀ ∝ M200^{1/3}) and is therefore
  excluded by X58 by construction; it is not a candidate.
- For a point mass, v_esc/v_c at r_a₀ is the constant √(2/ν(1)); C6 varies only through extended mass (clusters, Plummer
  dwarfs, discs at r) and the choice of Φ_int (§3).
- C5's M200: EM1's R1 relation lgM200 = 11.18 + 0.9 (lgM_b − 10) (A_c2b_refit) for SPARC, MW, lenses, groups, clusters;
  dwarfs: X51_dwarf_cooling_floor's cooling-floor M200 (the record's only halo mass for the retaining dwarfs). EPS z_f
  and t(z) from EM1's background A_c2b_refit (the machinery X59 uses), executed read-only.

## 3. Internal potential Φ_int (environment removed)

- pressure-supported dwarfs, Coma UDGs, DF2/DF4: Plummer G M_b / √(r² + R_h²) with R_h = ¾ r (X19's internal term);
- SPARC, UMa, MW disc, TDGs, groups: G M_b / r (X19's convention);
- clusters: X19's β-model value (it has no host term);
- KiDS lenses: G (M★ + M_cold)/r + hot gas as a uniform sphere of radius 100 kpc, G M_hot (3R² − r²)/(2R³) inside.

Reported variant: X19's host-inclusive |Φ| in C2 and C6.

## 4. Separation rule (X19 §4 generalised to one oblique variable)

Per footing, per labelling, per candidate:
- **Intervals.** 16–84 % range of members (N ≥ 3), [min, max] for N < 3; log₁₀ values.
- **Separates** iff there is a gap: max(hi over EXCLUDED) < min(lo over RETAIN) (direction UP: retain at high V) or
  max(hi over RETAIN) < min(lo over EXCLUDED) (direction DOWN). V* = centre of the gap (geometric); **margin** = gap
  width in dex. Reported, not fitted.
- **Complete:** every decisive class has a value; otherwise INCOMPLETE (cannot be the verdict key).
- X19's grading condition (b) is dropped: X58's pattern is binary (retain / exclude) and carries no graded amount.
- **Offenders** at the best threshold (fewest misordered classes) are named for every candidate.
- **Strict variant (reported):** [min, max] for every class.

## 5. Trials correction across candidates

Exact enumeration on each footing: all C(n_dec, n_EXCL) relabellings of the decisive classes with the class counts
fixed (primary: C(10, 3) = 120). For each candidate, p_k = fraction of relabellings in which it separates. The
family-wise value **p_any = fraction of relabellings in which ANY verdict-bearing candidate separates** (this accounts
for correlation between candidates). A separation counts toward a key only if **p_any ≤ 0.05** on that footing.
(Note: a perfectly ordered variable separates at least 2 of 120 labellings, so p_k ≥ 0.017 is the floor.)

## 6. Verdict classes (primary: labelling P, 16–84 %, Φ_int)

- **OBLIQUE KEY FOUND: V (threshold V\*)** — at least one verdict-bearing candidate separates, complete, on BOTH
  footings, with p_any ≤ 0.05 on both. All such V are listed with V* and margin per footing.
- **NO OBLIQUE KEY** — no verdict-bearing candidate separates on either footing.
- **UNDECIDED** — the footings disagree; or the only separations have p_any > 0.05 (chance level); or a separating
  candidate is INCOMPLETE only; or the step-0 stop rule fires.

Qualifiers (reported, no verdict weight): labellings G and W; strict intervals; host-inclusive Φ; lens class at the
single radius 0.104 Mpc; C5 with EM1's relation extrapolated to dwarfs; C4.

## 7. Step 0 (stop rule)

X19's script is executed read-only in this lane's process, truncated before its output writes (nothing is written to
X19's directory), with X19_MUTATE unset.
- (i) Every class × variable cell (median, p16, p84, N) and every E, s, Z, label of X19's class table must equal the
  committed `x19_classes.csv` (relative tolerance 1e-9; N exact).
- (ii) X19's primary verdict string and every per-variable primary status must equal the committed
  `x19_selector_rank_test_results.json` ("NO LOW-DIMENSIONAL SELECTOR").
- **Stop** (verdict UNDECIDED) if (ii) fails or more than two class rows fail (i).

## 8. Step 4 (reported only; run only if some candidate separates on a footing)

For each separating V: (R1) evaluate V for Ly-α forest structures at z = 2 and 3 (δ_b = 0–10 about the mean baryon
density of background A, T = 1–2 × 10⁴ K, σ = √(kT/μm_p), r = the baryon Jeans length) and state on which side of V* they
fall (retaining the background-level component there is what keeps linear growth); (early capture) evaluate V for the
EPS main progenitor of an L* lens (M200 10^11.35–10^12.05 today) at z = 2 and 3, r = 0.015 R200, σ = V200/√2, and state
whether the progenitor sits on the RETAIN side (X59's tension: content captured early stays bound under no heating).
Rough numbers; no verdict weight.

## 9. Checks and MUTATE

- **K0** step 0 (i) and (ii) pass.
- **KL** the label sets used equal §1 (P, G, W).
- **K1** radius reconstruction: r = 3 x a₀ / (4πG ρ_b) for every non-group class (groups: R_e from Tian+26); MW r = 8.122
  kpc and clusters r = 548 kpc within 1e-9; ρ_b round trip on every member within 1e-9.
- **K2** positive control: an oracle built from the frozen labels (1 RETAIN / 0 EXCLUDED, point intervals) separates
  under the labels used, on both footings.
- **K3** unit tests of the separation and enumeration code on synthetic tables (one separable, one not; p for a
  perfectly ordered variable = 2 / C(n, k)).
- **K4** lens M200 from EM1's relation on the lens baryons agrees with X53's bin means (11.35 / 11.72 / 11.90 / 12.05)
  within 0.10 dex; EPS z_f(10¹²) equals X59's printed 0.944 within 0.01.
- **K5** peak RSS < 1 GB.

**MUTATE** (`X64_MUTATE=1`): the labels of MW ultra-faint ↔ SPARC large and Clusters T3 ↔ KiDS lenses are swapped in the
label table used by the rank test. **KL and K2 must FAIL** (the oracle is built from the frozen labels). Outputs
`*_MUTATE.*`; exit 1.

## 10. Compute

One script, single thread, `nice -n 15`, < 1 GB, minutes. No downloads. `PYTHONHASHSEED=0`. Outputs `.out`,
`_results.json`, a per-class CSV. Every README number comes from these.
