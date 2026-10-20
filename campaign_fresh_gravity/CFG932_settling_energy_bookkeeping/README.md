# CFG932: energy bookkeeping of cold-energy settling (theory spine for H-ELS)

**Bottom line.**
- **Q1 NON-CONSERVING.** The record's settling (CFG638) does not conserve matter-sector energy. The source term is the drift power
  P_drift = ∫ρ_c v_s·∇Φ dV, plus the bath P_bath = ∫(α/τ)(3ρ_cσ_J² − tr Π) dV.
  - Two-sided deficit (FIX-1): v_s = ατ(g_law − g), so P_drift = α∫ρ_c τ g(g − g_law) dV. Removing a central surplus *injects*
    energy, and CFG542 books it to a dark-energy partner (Q = −ρ_c v_s·∇Φ < 0). Baryons never pay (G9).
  - One-sided and gated rules never push a surplus out.
  - In no reading of the record does baryonic feedback enter the cold energy's books. H-ELS needs a new constitutive rule that
    replaces the partner on the outward branch (DERIVATION.md §4).
- **Q2: nothing to pay for in the dwarfs at the record's supply.** With f_ret = 0.10 (M_ta = 64 M_b) and native NFW debris, every
  dwarf's primordial cold energy lies below the law's phantom over its stellar body, in every cusp corner.
  - At L = 1 their surpluses sit well inside r_h (R_x = 0.05–75 pc over all cusps and both footings) and cost 4e36–1.3e49 erg,
    ε_req ≤ 1.2e-7 of their supernova energy.
  - The retained excess at r_h is ≤ 0.001 dex.
  - Rotators have no surplus (SPARC-like dwarf: none in any corner) or a negligible one.
  - Only the cluster core carries a large surplus: 7.5e62 erg at the central corner, ε_req 0.76 (canonical).
- **Q3 BRACKET-DEPENDENT as frozen** (36/72 corners non-empty). Every non-empty window lies at ε ≤ 1.5e-6, set by sub-parsec to
  ~10 pc surpluses in the faint dwarfs, so no window exists at any coupling above that.
  - Post hoc (A1): with the over-supplied L = 100 dwarfs completed, windows up to ε ≈ 0.5–2% appear, but only when the primordial
    halo is 100× the record's supply. Every window contains ε ≈ 0.
  - So energy never separates rotators from dSphs here: rotators simply have no surplus. "One ε" collapses to "surpluses are not
    removed", which is the record's one-sided minimiser.
- **Q4: no conflict with the shear pass.** The CFG650/CFG654 engine fills deficits instantly from the shell and never removes a
  surplus (its source is one-sided). It is H-ELS's ε → 0 limit for surpluses, and it carries no energy budget.
  - Tension with M3: the census gas expulsion costs 13–38% of the rotators' and cluster's available energy, far above the
    ≤ 2% windows. One universal ε cannot pay for both; gas and cold energy would need separate couplings.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled (every class is computed per footing; both are shown). "Cold
energy" throughout; its mass is required; no particle species. Not "theory closed". Nothing here says the data favour the
framework. Framework-native inputs only: no ΛCDM simulation fit enters any number.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dce2a2e3d). H-ELS is POST-HOC (formed after the record's results).
- **Derivation:** `DERIVATION.md`.
- **Scripts.** All runs use one core, nice 10, < 200 MB, and take seconds. Nothing was downloaded and no other lane was touched.
  - `cfg932.py` → `cfg932.out`, `cfg932_results.json`. Exit 0: K1–K3 and the Q1 identity pass.
  - `CFG932_MUTATE=1` → `cfg932_MUTATE.out`, `cfg932_results_MUTATE.json`. Exit 1, as designed: both teeth bite.
  - `cfg932_posthoc.py` → `cfg932_posthoc.out`, `.json`. Amendment A1, POST HOC, no verdict weight.

## Q1: energy accounting of the record's settling

The derivation (DERIVATION.md §2) gives

d(K_c + K_b + W)/dt = P_drift + P_bath.

Neither term is a divergence. The 1-D spherical drift-only test (frozen IC: Plummer M_b = 1, a0 = 0.05, NFW cold 30, R_C = 30,
α = 1, G = 1) gives:

| rule | ΔW/\|W₀\| | ∫P dt vs ΔW | outward / inward work | note |
|---|---|---|---|---|
| two-sided (FIX-1) | **+0.593** | 25.35 vs 25.30 (identity 1.9e-3) | +25.35 / −5e-21 | surplus pushed to the catchment edge; energy injected with no baryon coupling |
| one-sided (E5) | 0 | 0 vs 0 | 0 / 0 | the frozen IC has no deficit cell, so nothing moves (trivially) |
| *post hoc PH4*, one-sided, a0 = 1 (31 deficit cells) | −0.020 | identity 1.7e-4 | 0 / −0.848 | inward only; mass in surplus cells unchanged (17.859 → 17.859) |
| *post hoc PH4*, two-sided, a0 = 1 | +0.260 | identity 1.7e-3 | +11.14 / −0.038 | surplus cells lose mass (17.86 → 12.97) |

**Class (frozen rule): NON-CONSERVING.** The identity holds to ≤ 2% and |ΔW|/|W₀| ≥ 1e-3.
- **Hidden source or sink:** P_drift, which CFG542 books to a dark-energy partner φ. An exact Λ cannot exchange energy, so under
  exact Λ the two-sided settling violates energy conservation outright. P_bath has no named partner (CFG544).
- **CFG747 tether dynamics (canonical v2 S2), reported separately.** It is conservative (its own K2), but its cubic push expels a
  tethered surplus using the tether field's own energy, in 50–100 t₀ (CFG776). A tethered surplus does not wait for baryonic
  energy.

## Q2: the cost of reaching the law (central corner: EPS F = 0.05, L = 1, cluster M_BH 5e9)

ΔE_b is primary (the virial energy of the cold mass in the law's potential, inside R_x). The other columns:
- ΔE_a: self-consistent ½ΔW.
- ΔE_c: gross local transport.
- ΔE_tot,b: the whole catchment, infall included (always negative: net release).
- X_ret: the total-mass excess at r_obs if the system is fully starved (one-sided minimiser).

| system (can) | M_ta | c_ta | R_x | M_sur (M☉) | ΔE_b (erg) | ΔE_a | ΔE_c | ΔE_tot,b | E_avail | ε_req (b) | X_ret | E_M3/E_avail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| UFD-c | 3.18e5 | 56.5 | 0.18 pc | 0.012 | 6.8e38 | 2.3e38 | 6.8e38 | −4.3e49 | 8.3e52 | 8.2e-15 | 0.000 | 7.7e-6 |
| UFD-e | 1.91e6 | 52.5 | 27.9 pc | 523 | 6.0e45 | 2.1e45 | 6.0e45 | −4.0e50 | 5.0e53 | 1.2e-8 | 0.000 | 2.4e-5 |
| Draco-like | 3.18e7 | 46.7 | 7.9 pc | 80 | 6.5e44 | 2.2e44 | 6.5e44 | −3.9e52 | 8.3e54 | 7.9e-11 | 0.000 | 1.5e-4 |
| Fornax-like | 2.55e9 | 37.5 | 31 pc | 3.8e3 | 3.9e47 | 1.3e47 | 3.9e47 | −2.4e55 | 6.7e56 | 5.8e-10 | 0.000 | 2.4e-3 |
| SPARC-like dwarf | 2.50e10 | 32.6 | none | 0 | 0 | 0 | 0 | −6.0e56 | 4.3e56 | 0 | 0.000 | 0.148 |
| MW-like | 3.82e12 | 22.2 | 51 pc | 3.4e3 | 1.2e50 | 4.0e49 | 1.2e50 | −4.3e59 | 1.6e60 | 7.4e-11 | 0.000 | 0.135 |
| cluster core | 1.65e15 | 11.4 | 1158 kpc | 2.7e13 | **7.5e62** | 3.1e62 | 7.5e62 | −1.4e64 | 9.9e62 | **0.76** | +0.098 | 0.378 |

Alt footing, same corner:
- The MW-like and SPARC-like rows have no surplus.
- The dwarfs' ΔE are ~½ the canonical values.
- Cluster: ΔE_b 4.3e62, ε_req 0.44, X_ret +0.065.

**Ranges over all 36 corners per footing, ε_req (b):**

| system | canonical | alt |
|---|---|---|
| UFD-c | 8e-17 – 2.1e-2 | 4.5e-17 – 1.9e-2 |
| UFD-e | 2.8e-10 – 7.8e-2 | 1.7e-10 – 7.5e-2 |
| Draco-like | 0 – 1.5e-6 | 0 – 6.6e-7 |
| Fornax-like | 0 – 0.12 | 0 – 0.10 |
| SPARC-like dwarf | 0 in 36/36 | 0 in 36/36 |
| MW-like | 0 – 2.6e-2 (0 in 18/36) | 0 in 36/36 |
| cluster | 0 – 7.0 (0 at PS1) | 0 – 5.5 (0 at PS1) |

**Retained excess at r_obs.** Canonical; the full table is in `cfg932.out`.
- **Dwarfs at L = 1: ≤ 0.001 dex for every cusp and footing.**
- Appreciable only at L = 100 with EPS cusps: UFD-e +0.24 / +0.39, Draco +0.02 / +0.18, Fornax +0.04 / +0.20 (F = 0.05 / 0.01).
  UFD-c stays 0.
- Cluster core: +0.02 to +0.18 against the observed ×1.8 (+0.26 dex, CFG687/922). Even full retention falls short at these cusps.

## Q3: who can pay

**Frozen class: BRACKET-DEPENDENT.**

| measure | starved set | non-empty corners |
|---|---|---|
| b (primary) | S_A | 36/72 |
| b | S_B | 33/72 |
| a | S_A | 36/72 |
| c | S_A | 30/72 |

By footing (b, S_A): canonical 12/36, alt 24/36, both BRACKET-DEPENDENT. The robustness downgrade is not needed, because every
variant gives the same class.

**What the windows are (A1, POST HOC, PH0–PH3):**
- **PH0.** The largest ε_hi over all 36 non-empty frozen windows is **1.47e-6**. The upper edge is set by UFD-c (24 corners) or
  Draco (12), i.e. by surpluses of 0.01–100 M☉ at r < 10 pc. These are physically empty windows.
- **The 16 over-supplied system-corners.** Draco and Fornax at L = 100, both footings and all cusps: there r_* > r_ta, so the law
  cannot hold M_cat inside the catchment. The frozen criteria did not anticipate this. They are completed post hoc by putting the
  overfill (Draco 0.12–0.20, Fornax 0.58–0.61 of M_cat) as a shell at r_ta.
  - Draco then needs ε_req 0.35–0.51.
  - Fornax needs 4.2–6.3 (it can never reach the law).
- **PH1 / PH2** (completed, or flagged set to ∞): BRACKET-DEPENDENT (39/72). **15 corners give windows reaching ε = 0.5–1.9%**,
  all at L = 100 with EPS cusps. Their lower edges are 0 or 7.4e-11.
- **PH3** (flagged corners dropped): the largest ε_hi is 2.0e-11.
- **Reading.** Wherever a window exists, it contains ε ≈ 0. That is because the rotators have no surplus to remove, not because
  they can afford to remove one. Energy limitation adds nothing to "the primordial surplus is never removed", which is the
  record's one-sided minimiser (CFG541 E5 / CFG639 gate). That rule is in turn contradicted by the two-sided FIX-1 drift and by
  CFG776's tether push, and CFG889 found that with orbits the gate does not retain.

## Q4: consistency with theory-v2 and the shear pass (code reading, `CFG650_theory_v2_combined_pm`, Read tool only)

**(i) The modules carry no energy budget.**
- **M1** (per-host supply, engine lines ~986–992) partitions the supply pool.
- **M2** (lines ~665–689, 890–903) makes the law's input the condensed baryons, raised by a cooling gate
  (t_cool = t_dyn, Tozzi–Norman Λ(T)).
- **M3** (`expel_m3`, lines ~1054–1081) removes the census non-retained baryons f_b(1 − f_ret)(1 + δ) from the source and re-places
  them with a Gaussian of σ = r_ON. It is mass-conserving and uses no supernova energy; particles are not moved.
- So energy-limited settling does not contradict M1, M2 or M3 formally.
- **Quantitatively, at the central corner (ε = 1):** M3's expulsion, if the non-retained baryons once traced the primordial NFW,
  needs E_M3/E_avail = 0.148 (SPARC-like dwarf), 0.135 (MW-like) and 0.378 / 0.385 (cluster, can / alt). For dwarfs at L = 1 it
  is ≤ 2.4e-3.
- With one universal ε inside the PH1 windows (≤ 1.9%), M3 could not be paid in rotators or clusters. H-ELS plus M3 needs
  ε_gas ≳ 0.15–0.4 and ε_cold ≲ 0.02: two couplings, not one.

**(ii) The shear pass does not assume surplus removal.**
- The engine's settled source is e = f_sw · edge · max(s_ph − s_c, 0) on catchments (line ~969). It is drawn zero-sum from the
  shell with a per-host cap q ≤ 1 (lines ~1019–1039).
- The total potential is the particles' collisionless density plus that source (`_finish_phik`, lines ~1086–1101).
- So the pass assumes **complete, instantaneous filling of deficits up to the supply cap and zero surplus removal**. The
  primordial surplus stays wherever the particles put it, which is the ε → 0 limit of H-ELS.
- The inward fill releases energy that the engine does not book (CFG541's sink). CFG654 NC1x uses the same engine (input switch
  only).
- **Resolution:** the cell is 97.7 kpc/h at 1024³ / 100 Mpc/h (k_hi 8.04 h/Mpc). Galaxy cores are unresolved; cluster cores are
  marginal.
- **H-ELS is not contradicted by the shear pass, and the shear pass does not test it.**

## Controls

| control | result |
|---|---|
| **K1** | PASS. Truncated NFW c = 10 / 30 rel. error 1.2e-12; Plummer 3.0e-13. |
| **K2** | PASS. Reproduces CFG541's MW-like canonical record: M_cat/M_b = 53.6432722396066 (rel 0) and r_* = 514.3182020135 kpc (rel 2.2e-16). Continuous phantom vs cell sum at r_*: 1.0e-4. |
| **K3** | PASS. Direct Jeans W + K vs ½ΔW over the whole catchment (central corner, canonical): MW −2.3886e59 vs −2.3828e59; Draco −1.5720e52 vs −1.5728e52. |
| **MUTATE M1** | Primordial ≡ settled gives every ΔE = 0 at r_obs and at 0.5 r_* (14 system-footings). **Bites.** |
| **MUTATE M2** | a0 → 1e-6 a0 changes the settled M_c(<r_obs) by 7e7 to >1e190 for all 14. **Bites.** The run exits 1, as designed. |

## Amendments and disclosures (dated 2026-10-20; the frozen text is not edited)

1. **Implementation fixes before any main number.**
   - The first MUTATE attempt stopped on a Python syntax error (a dict key) and wrote nothing.
   - The second showed NaN for the SPARC-like dwarf: catastrophic cancellation in the exponential sphere's M(<r) at r ≈ 1e-10 R.
     Small-x series were added for the exponential sphere, the β-model and the NFW m(x).
   - MUTATE was then rerun (both teeth bite) and the main run followed.
2. **The frozen Q1 IC.** Its cumulative cold mass exceeds the phantom everywhere (a0 = 0.05). The "central zone" therefore covers
   the whole catchment, and the one-sided run has no deficit cell (static, identity trivially met). PH4 (post hoc) adds a mixed
   state (a0 = 1). The Q1 class rests on the frozen two-sided run.
3. **Over-supplied corners (r_* > r_ta).** These were not anticipated by the criteria. The frozen machinery takes R_x from the last
   interior crossing and ignores the overfill. They are treated only in A1 (PH1–PH3), and the frozen class is unchanged.
4. **Surplus significance.** The frozen R_x rule counts any surplus, down to 0.01 M☉ at 0.2 pc (UFD-c), so the frozen windows are
   set by such surpluses. No significance floor was frozen; PH0 and PH3 show the effect.
5. **Inputs.**
   - The systems' parameters are representative values from memory (no downloads). Spherical approximations are used for the discs
     and the cluster.
   - The SN energy (1e49 erg per M☉ formed) and the AGN release (0.1 M_BH c²) are declared.
   - The native tables carry Planck primary-CMB ω_c, A_s, n_s (the CFG654 principle).
   - f_ret is the record's empirical census (CFG416); 5.364 is the record's ratio.
   - The concentration rule (top-hat 18π², δ_c 1.686, EPS/PS1 with the native P(k)) is declared, with F as a bracket. No ΛCDM
     simulation constant is used.
6. **Seen before freezing (in the criteria §0):** prototype concentrations and hand estimates.

## Standing and next step

The record's settling is not energy-limited by baryons in any of its readings; H-ELS would be a new rule. At the record's own
supply, the faint dwarfs have no primordial surplus at r_h to retain, so energy limitation cannot be their selector. The cluster
core is the one place where the surplus is large and its cost is comparable to the available AGN energy. Even there, full
retention gives +0.02 to +0.18 dex against the observed +0.26.

A dwarf excess of the observed size needs a primordial halo ~100× the record's supply. That is a supply question (CFG920's baryon
loss L), not an energy one.

Next:
- If H-ELS is pursued, freeze the new rule (outward-drift throttle with a feedback budget, tether push off on surplus) and test it
  with the L bracket as the main unknown (CFG930/931 territory).
- Otherwise, record that energy bookkeeping cannot select the excess family.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
