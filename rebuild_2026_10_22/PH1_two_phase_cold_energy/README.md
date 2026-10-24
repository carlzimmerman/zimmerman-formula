# PH1_two_phase_cold_energy: can a condensed + normal cold energy fix what O1 left open?

## Verdict (frozen §0): NO-GO, both under the owner's rule and on the data

**No phase criterion built from {κ, a₀, G, c, Λ, L★} gives every class the phase it needs.**
- The best criterion is the Landau one (C-V). It splits satellites from isolated galaxies with no new constant. But it leaves
  the linear universe CONDENSED, so growth reaches 0.075 / 0.077 of dust against the 0.95 line.
- Making the early universe normal is possible only as an initial condition, f_n ≥ 0.855 / 0.854 (+1 IC).
- That normal mass can never condense later (D5). So it sits in every isolated galaxy and double counts:
  - SPARC median Υ falls from 0.52 to the 0.30 floor (canonical);
  - rms rises by +0.044 / +0.059 dex (canonical / alt).
- Both branches fail at least two scored rows.

The useful by-product is the Landau "freeze-out" of a satellite's held phantom into a bound normal component, worked out in
§3. It brackets the satellite excess with no EFE. It lives only in the branch whose cosmology fails.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy is a classical field, not a particle.
Not "theory closed". Nothing here says the data favour the framework.

**Checks: main 11/12 PASS (exit 1).** KS2b fails by 0.005 dex; this is disclosed in AMENDMENT A1. **`--mutate`** gives the
normal phase Ξ-charge. It fails D3 (ε_n = 1) and KG (f_n = 1 growth 0.075) as frozen: 9/12, exit 1.
- Main run: 216 s with the cached grid; the first grid build took 774 s.
- Peak RSS 0.18 GB, one thread, nice 15.
- Nothing downloaded.

## 1. The action (T1) and what sympy derives

    S = (c³/16πG)∫√−g [R − 2Λ − 2J_x(Y[θ]) + 2K(Q[θ])] + S_γL/switch[θ] + ∫√−g [−|∂ψ_n|² − μ²|ψ_n|²]_incoh + S_m[g]

One classical complex scalar:
- **Condensed phase:** the coherent part √ρ_s e^{iθ}. Its phase is the khronon, so this is v3s unchanged.
- **Normal phase:** the incoherent part ψ_n (⟨ψ_n⟩ = 0). In the Wigner limit its stress is multi-stream dust. It is
  Ξ-neutral and minimally coupled.

| id | derived | result |
|---|---|---|
| D1 | condensed static limit | g μ(g/a₀) = g_N, residual 0. Held dust = the phantom of (ρ_b + ρ_n), so **normal mass sources the law like baryons** |
| D2 | normal static limit | the isothermal ρ = σ²/2πGr² solves Jeans + Poisson (residual 0); M_n = v_n² r/G |
| D3 | composite weight (O1 W) | F = (M_b + M_n + M_s)g − M_s\|∇Ξ\| ⇒ **ε_n = 0**: the normal share falls with its host and has weight (ε_s = 1) |
| D4 | Landau criterion | v_c = min ω/k = L★√(2πGρ̄): 1.16 / 1.22 km/s at ρ 0.1 M☉/pc³ (canonical / alt) |
| D5 | unfolding lemma | a multi-stream medium never returns to single-stream: **normal → condensed is impossible** without a dissipative channel |

**Constant count.**
- C-V adds none: v_c is built from L★, which is FITTED but allowed.
- Branch EN adds one initial condition, f_n.
- A field-level normal phase that is multi-stream on dwarf scales (λ_dB ≤ 100 pc at σ = 10 km/s) needs a wave scale
  μ⁻¹ ≤ ~3e-3 pc. That is **NEW**: no combination of the allowed constants gives it. μ = 1/L★ gives m c² ≈ 2.9e-25 eV, which
  is fuzzy everywhere.

## 2. Criterion menu (T2): none ADMISSIBLE

| criterion | constants | disc | satellite | early universe | failure |
|---|---|---|---|---|---|
| C-g: g < a₀ | 0 | C outer / N inner | C ✗ | N to z ≈ 90, then C ✗ | satellites, growth (Theorem G) |
| C-ρ: ρ vs ρ_Λ | 0 (+O(1)) | either sign fails one of disc / early | | | both signs |
| C-σ: σ < (GMa₀)^¼ | 0 | C | C ✗ (ratio 0.47, unchanged at infall) | C ✗ | satellites, growth |
| **C-V: Landau V_rel < c_s(L★)** | **0** | **C (0.03 ≪ ~1 km/s)** | **N, bound (released at Δv = v_c ≪ σ)** | **C ✗ (no relative flow on FRW)** | growth; cluster debris is added to the law |
| C-SX: single-stream | 0 | N ✗ | N | C ✗ | backwards on both |
| C-λ: coherence | +1 NEW (μ) | C | C ✗ (660 kpc at μ = 1/L★) | C ✗ (fuzzy) | rule, satellites, growth |

## 3. Rows (T4)

| row | branch EC (C-V, early condensed) | branch EN (early normal by IC) |
|---|---|---|
| **F3 growth** | **FAIL**: δ/δ_dust 0.0747 / 0.0773 (backgrounds A / B); KG matches F3's BSK2 kernel at μ → 0 to 1e-5 | PASS only with f_n ≥ 0.8547 / 0.8539 (+1 IC) |
| **P4 isolated RAR** | PASS with no merger debris (control 0.0541 / 0.0537, Υ 0.52 / 0.44 = P4 exactly; alt misses Υ as in P4). Debris at λ = 0.5 of the galaxy's own phantom: rms 0.121 / 0.145, Υ 0.30. λ_max = 0 (canonical sits 0.02 above the Υ edge) | **FAIL (double count)**: rms **0.098 / 0.113**, median Υ **0.30 / 0.30**; Δrms **+0.044 / +0.059**, ΔΥ −0.22 / −0.14. Background B is the same to 0.001 |
| **Z2 satellites** (C2–C4, N 19) | data over ISO **+0.467 ± 0.071 / +0.427 ± 0.073**. Over the radial-collapse freeze-out: **−0.146 ± 0.051 / −0.187 ± 0.050 (BELOW)**; with the pericentre R_J: −0.128 ± 0.078 (CONSISTENT) / −0.165 ± 0.078 (BELOW). The data lie **between** the no-collapse (ISO) and radial-collapse bounds. Host-field slope at fixed M_V +0.32 ± 0.19 / +0.34 ± 0.19 (inside 2 se). Frozen class: **neither PASS nor FAIL** | **FAIL**: +1.628 ± 0.056 above (a fair share of the present stars is far too little) |
| **F1 cluster cores** (REUSED X2) | FAIL: the members' released debris is **added** to the cluster law, because the cluster's khronon still holds; X2: the added form overshoots | FAIL: the fair-share normal mass sources the law (X6 C1b, "CDM under another name") |
| **U1 TDGs, DF2/DF4** (REUSED) | PASS: born at V_rel ≫ v_c, so no condensate; U1 B0 +0.055 ± 0.114 | PASS for TDGs |
| **Solar System, globulars** (REUSED O1 VS) | PASS | PASS for the condensate |

- **The freeze-out mechanism** (EC, derived, no constant):
  - An infalling dwarf's held phantom starts to lag its stars at ε = 1 (O1).
  - When the lag reaches v_c ≈ 1 km/s, far below σ_sat, the held medium turns normal while still bound.
  - It is at rest and curl-free, so it collapses radially.
  - The satellite then carries self-gravitating cold mass with no EFE.
  - With the adiabatic stellar response, log B has median +0.594 / +0.595, and the stars contract by log c = −0.30.
  - Radial (j = 0) collapse is the upper limit. Radial-orbit instability and host torques would lower B toward the data.
  - This result is not available to EN, and EC's growth fails.
- **The double-counting number** (P4's statistic, EN at f_n,min on present baryons, a lower bound on the supply):
  - **canonical:** rms 0.054 → 0.098 dex and Υ 0.52 → 0.30 (floor);
  - **alt:** rms 0.054 → 0.113 dex and Υ 0.44 → 0.30.
  - The rms change alone is under the 0.110 line on canonical; the Υ collapse fails the line.

## 4. O1 and CFG946 (T3)

- **O1's theorem is evaded only for the normal share.**
  - D3 gives ε_n = 0 exactly, because the normal share carries no Ξ-charge. It self-gravitates and falls with its host, so it
    is not held.
  - O1's premises are "held phase" and α = 1. Neither applies to ψ_n.
  - The condensed share still has ε_s = 1. The two-phase idea does not make held matter weigh; it changes which matter is held.
- **CFG946 (T-O2).** Its premises are dust cold energy, local universal sectors, a profile-independent deep BTFR, and no EFE.
  - The two-phase construction evades "universal": the BTFR holds for condensed systems and the no-EFE property for normal
    ones. The price is a phase label (C-V is local: V_rel = −u·v_b).
  - Under the owner's field rule it is **not excluded**: ψ_n is a classical field, not a particle species.
  - Gravitationally it is what CFG946 and CFG723 call a "particle in disguise": a cold collisionless component, exactly X6
    C1b in branch EN.

## 5. What this does not show

- **Spherical, radial collapse.** The phantom truncation uses a flat-host Jacobi radius at the present distance (pericentre
  variant reported). There is no radial-orbit instability and no host torque. The stellar back-reaction on the dust is
  neglected (≤ 1/√y of the mass).
- **The phase transition at v_c is POSITED** (A6). v3s's action has one phase. D4 gives the Landau speed, not a derived
  conversion law.
- **Normal-halo shape.** EN's isothermal profile with a 200ρ_crit edge is POSITED and partly ΛCDM-PROCESSED. Present baryons
  make the double count a lower bound.
- **F1, U1, Solar System and globular rows are reused.** No member-galaxy census exists for a cluster debris budget.
- **EFE.** P4's EFE is omitted (it changes the result by < 0.001 dex).

## Files and run

- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (11270eef61, committed alone first); `AMENDMENT_A1.md` (post-result).
- `ph1_two_phase.py` → `ph1_two_phase.out`, `ph1_two_phase_results.json`; `*_MUTATE.*`.
- `ph1_collapse_grid_A1.json` is the cached collapse grid; delete it to rebuild (about 13 min).
- Functions are reused read-only through `ast` extraction: P4's SPARC loader, fit and pool; F3's `make_E` and
  `growth_ratio`. Z2 and U1 per-system csv files are also read.

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/PH1_two_phase_cold_energy/ph1_two_phase.py            # exit 1 (KS2b, disclosed)
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/PH1_two_phase_cold_energy/ph1_two_phase.py --mutate   # exit 1 by design
```
