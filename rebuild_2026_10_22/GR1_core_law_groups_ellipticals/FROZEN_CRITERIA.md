# GR1_core_law_groups_ellipticals — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25. κ = ½ FITTED. Footings canonical / alt, graded separately, never pooled. Cold dark energy (not matter,
never a particle). Nothing here says the data favour the framework or ΛCDM. Not "theory closed".

**Question.** OS1's core law has one constant, q, fixed once on SPARC: q_f = 0.892 (canonical) / 0.748 (alt), from
`OS1_core_law_out_of_sample/os1_out_of_sample_results.json` (a8b817e19e). With **no refit**, does it predict two classes of
system it never saw?
- galaxy groups (P4 T3's line), which X38 (q = 0) fails ABOVE at Z +2.48 / +2.29;
- red / elliptical systems.

## 0. Law (OS1, unchanged)

X38's route-E Burkert halos (Newtonian, no law force), at surface density Σ_i = Σ_a0 (σ_i/σ_ref)^q, where:
- Σ_a0 = a₀/(2πG) (X38's SIG);
- σ_ref = 70.50 km/s (SC1);
- M200 comes from EM1 background A's relation, log M200 = a + b (log M_b − 10), with R200 at 200 ρ_c(h_A), exactly as X38 / X43;
- r0 comes from X38's `solve_r0` (compact root; saturation counted).

q is read from OS1's JSON and never moved. **σ convention: X19's V2, σ_LOS** for every pressure-supported system:
- groups: the catalogue's σ_LOS, 10^ls (Tian+2026, column used by P4);
- SLUGGS centrals: the linear mean of the measured GC σ_LOS over the outer bins that CFG528 grades (`B[n]["Sb"][outer]`).

The observed σ sets Σ, and the same system's observed σ is then compared with the prediction. SPARC (V_last/√2) and the
clusters (kT) work the same way in OS1. Reported only: the self-consistent fixed point, where σ_i in Σ is the *predicted*
σ (iterated to 1e-6 dex).

## 1. Classes in scope

### 1a. Galaxy groups (graded)

- **Data:** Tian+2026 BFJR groups, 63 rows. The file is `../_external_data/vizier2026/J_A_A_710_L39.tsv`, outside git and
  already on disk.
- **Estimator:** P4 T3's, executed read-only exactly as X40b / X43 (`group_logsig` with the X38 halo; `class_stats`, with
  the slope from ±0.01 dex in M_b).
- **Class, per footing:**
  - **PASS:** verdict CONSISTENT (|Z| < 2 and tot ≤ 0.045).
  - **IMPROVES ON X38:** verdict still ABOVE LAW, but the mean Δ is lower than X38's by ≥ 0.020 dex (X38: +0.0973 /
    +0.0907).
  - **FAILS:** anything else. This includes no gain, an overshoot (BELOW LAW) and NOT DIAGNOSTIC.

### 1b. SLUGGS centrals (graded)

- **Systems:** NGC 4486, 4365, 4374 and 5846.
- **Data and tracers:** CFG528b's, executed read-only. Its measured GC density profiles and measured anisotropy (row M)
  feed the variable-β multi-population Jeans solver `sig_multi`. Inputs sit in `../_external_data/cfg528_work/src/`, outside
  git and already on disk.
- **Per-galaxy error:** CFG466's bootstrap SIG, and CFG528's `score`.
- **Field (route E):**

      g(r) = G [M★ r²/(r + a_h)² + M_h(r)] / r²

  where:
  - M_h(r) = π Σ_i r0² B(min(r, R200)/r0);
  - the baryon mass for M200 is M★ (stars only, as CFG528b's K0 reading);
  - **M★ is the route-E analogue of CFG528's 'jam' reading.** M★ solves 0.5 M★ + M_h(< r12; M★) = 0.5 M_JAM, by Brent in
    log M★ on [M_JAM·10⁻³, M_JAM]. If there is no root, that galaxy is "not computable" (None in `score`) and is counted.
- **Class, per footing:**
  - **PASS:** CFG528's `closes`: ≥ 3 of 4 with Z < 2, none with Z < −2, all 4 computable.
  - **IMPROVES ON X38:** not PASS, the class mean offset |mean| at q_f ≤ 0.5 × |mean| at q = 0 (X38 halos on the same
    machinery), and none reversed (Z < −2).
  - **FAILS:** anything else.

### 1c. Red KiDS lenses — NOT GRADED (fixed now)

The KiDS-1000 red lenses (S2 / CFG850) carry only M★ per lens. X19's V2 assigns them no σ, and no per-lens σ_LOS is on disk.
Grading them would need a new M★→σ map or a σ from the model itself. Either is a new input outside the "same σ convention"
rule. A route-E 4GΔΣ forward model over the 181,477 lenses also does not exist in the record. This lane therefore
**does not grade them** and names them as a follow-up. No red-lens number is computed here.

## 2. Lane class (per footing; the verdict needs both footings to agree, else UNDECIDED)

| lane class | rule |
|---|---|
| GR1 PREDICTS BOTH | groups PASS and SLUGGS PASS |
| GR1 PREDICTS GROUPS, ELLIPTICALS SHORT | groups PASS, SLUGGS IMPROVES or FAILS |
| GR1 PREDICTS ELLIPTICALS, GROUPS SHORT | SLUGGS PASS, groups IMPROVES or FAILS |
| GR1 IMPROVES ONLY | neither passes, at least one IMPROVES |
| GR1 FAILS | both FAIL |

## 3. Reported only (no class weight)

- **Groups:** the self-consistent σ fixed point; q_f ± 0.05; the fraction of groups whose halo r0 saturates.
- **SLUGGS:**
  - the 'bar' reading (CFG528's extrapolated hot gas added to g_N and to M_b);
  - the Salpeter population M★ (CFG528 `Mpop` 'salp') instead of the JAM analogue;
  - the self-consistent σ fixed point;
  - each galaxy's M★/M_JAM and Σ_i/Σ_a0.

## 4. Checks

- **K0a:** at q = 0, SPARC (OS1 machinery, bg A) equals X38's 0.0795 rms (to 1e-9 against X38's JSON).
- **K0b:** at q = 0, groups equal X40b's X38 row on both footings (mean to 1e-6, Z to 1e-4): +0.09726 / +2.479 and
  +0.09071 / +2.291.
- **K0c:** the SLUGGS Jeans machinery reproduces CFG528b row M K0 per galaxy (law field, measured tracers) to 1e-6 dex on
  both footings.
- **K0d:** no-halo groups reproduce P4's group_logsig (ν = 1) to 1e-4 dex (X43's K4).
- **K1:** at q_f, SPARC A rms equals OS1's 0.06049 / 0.05910 (to 1e-6).
- **K2:** the SLUGGS route-E M★ root returns 0.5 M★ + M_h(< r12) = 0.5 M_JAM to 1e-8.
- **K3:** peak RSS < 1 GB, one thread.
- **MUTATE (separate outputs, `--mutate`):** q → −q_f (Σ ∝ σ^(−q)), everything else unchanged. The tooth bites if both
  hold on both footings:
  - the groups' mean-Δ shift from q = 0 has the opposite sign to the real run's shift;
  - the SLUGGS class-mean shift from q = 0 has the opposite sign to the real run's shift.

  Exit 1 if the tooth bites, as in OS1. Reported only inside MUTATE: σ permuted across the 63 groups (seed 20261025).

## 5. Disclosed before freezing

- **Expected direction.** Group σ ≈ 100–250 km/s (median ≈ 140) is above σ_ref, so Σ rises by about (2)^q ≈ 1.7–1.9×. The
  groups' predicted σ should rise, moving toward the data (X38 sits ABOVE). Whether by the ≈ 0.1 dex needed is unknown.
  X43's η-floor got Z to +2.05.
- **SLUGGS centrals.** These are massive ellipticals (σ_GC ≈ 200–400 km/s), so Σ rises 3–6×. The law-based record
  (CFG528 / 528b) has the data ABOVE by +0.15 to +0.18 dex. Route E at q = 0 has never been graded on them. Its baseline may
  differ in sign from the law's, and the JAM-analogue M★ will drop as the halo grows. Writing it down now: the answer could go
  either way.
- **Extrapolation.** EM1's M200(M_b) relation was fitted on SPARC (log M_b ≲ 11.5). Groups (log M_b ≈ 11–12.5) and the
  SLUGGS centrals use it beyond that range, as P4 / X40b / X43 already did for groups.
- **Hosts.** M87 and NGC 5846 are host centres. Route E here gives each galaxy only its own M200(M★) halo. The Virgo / group
  host halo is not added. This is the "isolated" reading, and it is disclosed as such.
