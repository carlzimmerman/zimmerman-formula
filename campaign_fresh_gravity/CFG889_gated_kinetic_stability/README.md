# CFG889: is the deficit gate dynamically sound once orbits mix?

**Class as frozen: INCONCLUSIVE (K-test: K-OU FAILS) + CLUMP ERODED in all 8 primary cells.**

**What it says, read past the K-OU failure:** the gate does **not** keep CFG877's clump once orbits are included. With collisionless
orbits, the gated drift and the gated OU, the clump's excess inside r_t halves in t_50 = 105–148 Myr/α. It is gone (R ≈ 0) by
about 2–3 t_50, on both footings, at α = 0.5 and 1, and at both noise levels. The same happens at 4× the particle number.
- The gate slows the drain by 11–14× compared with the ungated drift (t_50 = 9.5–21 Myr, matching CFG882's drift-only rate to
  within 1.01–1.11). It does not stop it.
- CFG882's "gated retains exactly" (V2) depended on its drift-only model having no orbits.
- CFG882's empty-shell knife edge does heal by mixing: no empty or half-empty bins appear in any run with orbits. But the knife
  edge's one-way outward push reaches into the clump through the clump's own orbits.
- Post-hoc runs with the OU switched off (the part that fails K-OU) erode the clump the same way (t_50 = 154 / 159 Myr at N ≈ 1e5
  / 4e5). So the erosion comes from the drift acting along orbits, not from the OU problem.

Taken at face value, keeping half the clump for 12 Gyr needs α ≲ 1e-2. That assumes t_50 ∝ 1/α holds at small α (not run to
12 Gyr; a post-hoc α = 0.05 run keeps R = 0.70 after 1.5 Gyr). The bound (0.9–1.2e-2) is ×4–6 below CFG882's lenient floor of 0.05 and
×40–57 below the galaxy side's α ≳ 0.5.

κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are kept apart, never pooled. Law ν_e. Cold energy is real gravitating mass
(Newtonian Poisson); no particle species. Framework-native inputs. Not "theory closed". Nothing here says the data favour the
framework. No constant added; α stays free.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (0337ade83). Lane block CFG890–899 row ("CFG889 gated kinetic stability").
- **Script:** `cfg889.py`. One part per process, one core, `OMP_NUM_THREADS=1 nice -n 10`. Every part ran in < 5 min and < 1 GB.
  - `run_889.sh` runs the frozen parts K, G1a, G1b, G2a, G2b, U1, U2, N1, N2, H1, H3, then MUTATE M, the MUTATE summary
    (exit 1 by design) and the summary. Log: `parts/run_889.log`.
  - `run_889_posthoc.sh` re-runs part K, then the post-hoc parts P1 and P2, then the summary. Log: `parts/run_889_posthoc.log`.
- **Inputs, read only:** `CFG877_finite_cold_clump/cfg877_results.json` (V_x, M_cl, r_t). CFG882's s_50 for the O(1) check.
  Nothing downloaded; no other lane touched.

## Model (as frozen)

- **Particles.** A spherical shell code with N ≈ 1e5 equal-mass particles (m_p ≈ 618 M_⊙ for H2). Gravity is Newtonian, from
  static Plummer baryons plus the cold particles' own enclosed mass.
- **Initial state.** An isotropic Eddington equilibrium (f > 0 everywhere; ρ from f matches ρ to ≤ 0.3% from 1 pc to 4.5 kpc) of:
  - the law-settled halo, ρ_c = ρ_ph of the host's own baryons times a catchment taper from 3 to 5 kpc;
  - plus CFG877's clump, with the same core and M_cl but a smooth cap. A hard cap cannot be an isotropic equilibrium.
- **Dynamics.** Vlasov (kick-drift-kick, individual substeps) plus:
  - the record's drift v_s = α τ G M_ex(<r)/r², moving positions at fixed (v_r, v_t);
  - FIX-2 OU, rate α/τ, toward the Jeans dispersion of the current binned density.
  - Both act per radial bin. Gated: χ = 1[d > 0], with d = m_tgt − m_c. Ungated: χ = 1. MUTATE: χ = 1[d < 0].
- **Primary host.** H2 (3e5 M_⊙, 200 pc), the CFG882 D1 host. T = 1500 Myr, about 6.5 crossing times at 2 kpc and about 80 at r_t.
- **Overfill profile.** The smooth-capped clump's overfill ρ_x/ρ_tgt is 1.36 at 200 pc, 0.30 at 300 pc, 0.07 at 400 pc and 0.02 at
  500 pc (canonical). The overfill sinks into the shot noise (3–8% per bin) at about 350–450 pc.

## Results

### Primary gated cells (H2; clump run minus its paired no-clump run; final values = mean over the last 100 Myr)

| cell | R(T) | t_50 (Myr) | ΔH_e / ΔH_d | ΔM_zone/M_cl | C(1 kpc) clump / no clump | E_inj/\|E0\| (drift, OU) | f_esc (no clump) | frozen status |
|---|---|---|---|---|---|---|---|---|
| can α 0.5 ε 0.01 | −0.013 | 295 | 0 / 0 | −0.21 | +0.39 / +0.39 | +0.29 (0.26, 0.04) | 0.130 (0.104) | not KEPT, not HEALED, WB no |
| can α 0.5 ε 0.1 | −0.010 | 285 | 0 / 0 | −0.21 | +0.44 / +0.40 | +0.29 (0.26, 0.03) | 0.130 (0.103) | same |
| can α 1 ε 0.01 | −0.022 | 134.5 | 0 / 0 | −0.28 | +0.26 / +0.24 | +0.32 (0.25, 0.07) | 0.132 (0.085) | same |
| can α 1 ε 0.1 | −0.024 | 126.5 | 0 / 0 | −0.27 | +0.25 / +0.27 | +0.32 (0.26, 0.06) | 0.131 (0.084) | same |
| alt α 0.5 ε 0.01 | −0.004 | 220 | 0 / 0 | −0.16 | +0.62 / +0.53 | +0.23 (0.22, 0.01) | 0.126 (0.104) | same |
| alt α 0.5 ε 0.1 | −0.009 | 215 | 0 / 0 | −0.21 | +0.61 / +0.54 | +0.23 (0.23, 0.00) | 0.127 (0.107) | same |
| alt α 1 ε 0.01 | −0.032 | 105.5 | 0 / 0 | −0.30 | +0.34 / +0.33 | +0.26 (0.24, 0.03) | 0.124 (0.089) | same |
| alt α 1 ε 0.1 | −0.033 | 108.5 | 0 / 0 | −0.29 | +0.36 / +0.33 | +0.26 (0.23, 0.03) | 0.123 (0.088) | same |

- **(a) Clump: ERODED everywhere.**
  - t_90 is 33–68 Myr and t_10 is 220–585 Myr. α·t_50 = 105–148 Myr.
  - ε = 0.01 versus 0.1 changes t_50 by ≤ 8%.
  - The resolution run (N = 4e5, shot noise halved) gives t_50 = 140.5 Myr against 134.5 at N = 1e5. Its ΔM_zone ratio is 0.95, and
    its status agrees (as frozen).
  - Over the range tested, the drain rate does not depend on the fluctuation level.
- **(b) Holes: none form with orbits.** H_e = H_d = 0 at T in every run with orbits and a drift (gated, ungated, MUTATE,
  resolution, hosts, post-hoc no-OU), with or without the clump.
  - Not HEALED (as frozen) comes only from ΔM_zone, and that is the eroded clump's own outer mass leaving the zone, not a hole. At
    t = 0, 27% (canonical) / 33% (alt) of M_cl sits outside r_t. ΔM_zone = −0.16 to −0.30 is comparable.
  - The frozen metric did not separate the two. This is reported as frozen and not reinterpreted into a pass.
- **(c) Behaviour.**
  - Mass is conserved exactly (K-M).
  - Energy is BOUNDED in every cell: the injection rate falls 8–20× from the first to the last third. Most of it is drift work,
    +0.22–0.26 |E0|, put in while the clump is being removed (in CFG638's energy equation this is the sink term ρ v_s·∇Φ running
    from dark energy into the cold energy).
  - The escape fraction beyond the catchment is 12–13%, above the 1% criterion, so the cells are not WELL BEHAVED (as frozen).
  - The no-clump baselines escape 8–11% too. Post-hoc runs show this escape comes from the OU (no-OU baseline: f_esc = 0; no-drift
    runs: 9–10%), not from the clump.
- **No GROWING cell** in H2.

### Ungated comparison (V-U, ε = 0.01): DRAINS; CFG882's O(1) drain rate CONFIRMED

| | can α 0.5 | can α 1 | alt α 0.5 | alt α 1 |
|---|---|---|---|---|
| t_50 kinetic (Myr) | 21.0 | 11.0 | 19.0 | 9.5 |
| t_50 CFG882 = s_50/α | 20.74 | 10.37 | 17.16 | 8.58 |
| ratio | 1.01 | 1.06 | 1.11 | 1.11 |

CFG882's drift-only drain rate holds kinetically to ≤ 11%. Its untested "O(1)" limit is now checked.

### Controls

| test | result |
|---|---|
| K-V pure Vlasov steadiness | PASS both footings. Max \|Δlog ρ\| 0.027 / 0.021 dex; \|ΔR\| 0.023 / 0.039; \|ΔE/E\| 3.8e-3 / 3.4e-3; \|Δvir\| 0.005 / 0.006 |
| K1 gated path with χ ≡ 1 = ungated | PASS: every snapshot and the R series identical |
| K1b d > 0 everywhere | NOT APPLICABLE: the precondition cannot hold by construction (see disclosures) |
| **K-OU** OU alone on the no-clump equilibrium | **FAIL**: max \|Δlog ρ\| 0.185 dex (50–75 pc bin, −35%), zone +6.8%, f_esc 1.4% after 500 Myr |
| K-M mass | PASS, 42 frozen runs |
| K-E energy bookkeeping | PASS: worst \|ε_E\| 1.5e-3 over the verdict runs |
| T-H orbits off must reproduce CFG882's holes | **BITES**: drift-only particles give ΔH_e = +0.217 (ε 0.01) and +0.239 (ε 0.1), with R = 1 and C(1 kpc) ≈ 1.0. CFG882 D1 (12 Gyr density flow) found 39–45% |
| M1 MUTATE inverted gate | **BITES**: R(T) = 0.002 / 0.008, t_50 = 11.0 / 9.5 Myr (same as ungated) |
| Resolution N ×4 | AGREES (KEPT/HEALED status unchanged; t_50 140.5 vs 134.5 Myr) |

**Why K-OU fails** (post-hoc diagnosis in part P1, `OU-diag` lines).
- In populated bins the binned OU target equals the particles' own dispersion: ⟨σ_J²⟩/⟨v_r²⟩ = 0.975–1.06 from 60 pc to 5 kpc.
- **(i) Shape.** The equilibrium velocity distribution is truncated, with kurtosis 2.1–2.4 beyond 1 kpc against 3 for a Gaussian.
  The OU replaces it with a Gaussian of the right width. That breaks the Eddington equilibrium and sends Gaussian-tail particles past
  the catchment edge. This is a property of FIX-2's posited closure on any non-isothermal equilibrium: CFG544 K3d already noted that
  no global E − TS exists for T = σ_J²(x).
- **(ii) Noise.** In the sparse central bins (≈ 11 particles per bin at 20–60 pc) the target is biased high (×1.20), which heats the
  centre.
- So the frozen premise "the Jeans target is neutral on an equilibrium" was wrong for this equilibrium. It is reported as a FAIL, not
  loosened.

### Hosts (report-only; canonical, α 1, ε 0.01)

- **H3** (2e7 M_⊙, 700 pc; 2340 clump particles): ERODED, t_50 = 55 Myr, R(T) = −0.05.
- **H1** (1e4 M_⊙, 30 pc): ERODED, t_50 = 630 Myr. Its energy bookkeeping broke in one event between 100 and 200 Myr
  (ε_E = 17.3, then constant), with drift sub-cycles at the cap of 16 (clipping 4.7e-5) in H1's dense phantom cusp. Treat H1 as
  numerically unreliable.

## Post-hoc diagnostics (added after the frozen runs had been seen; no class weight)

These are in parts P1 and P2 of the same script, all canonical, H2, ε 0.01, gated.

| run | R(T) | t_50 | C(1 kpc) clump / no clump | zone ratio | f_esc (no clump) | reading |
|---|---|---|---|---|---|---|
| no OU (Vlasov + gated drift) | 0.006 | 153.5 Myr | −0.05 / +0.005 | 0.943 (d > 0 in 76% of zone bins) | 0.042 (0.000) | erosion without the OU; the excess inside 1 kpc is fully compensated (C(2 kpc) −0.30, overshoot) |
| no OU, N = 4e5 | 0.002 | 158.5 Myr | −0.055 | 0.938 | 0.047 | same; noise-independent |
| no drift (Vlasov + gated OU) | 1.013 | none | +1.51 / +0.66 | 1.215 | 0.101 (0.089) | the OU alone keeps the clump but contracts the halo (K-OU artefact) |
| full gated, α = 0.05 | 0.705 (R90 0.64) | > 1.5 Gyr | +0.48 / +0.007 | 0.988 | 0.067 (0.051) | at the lenient floor, 30% lost in 1.5 Gyr (consistent with t_50 ≈ 2.7 Gyr ∝ 1/α) |
| Dmix2: mass-conserving comb, pure Vlasov | n/a | n/a | n/a | 0.993 → 0.984 | 0.0001 | half the zone bins emptied at t = 0 (particles moved one bin out) refill completely within 10 Myr (H_e, H_d 0.50 → 0.00) |

A re-run of frozen part K with the final script is identical to the first run, apart from wall times. The post-hoc edits only added
code.

## Reading

1. **Why the gate fails once orbits mix.** The gate is local in position, but orbits are not.
   - Any equilibrium clump has orbits whose apocentres reach its skin, where the overfill ratio falls to the fluctuation level. There
     the gate opens and the drift pushes outward hard (M_ex(<r) ≈ M_cl; v_s ≈ 5–7 α km/s ~ σ).
   - Each time a clump particle passes through an open bin, it is displaced outward at fixed velocity, which raises its energy.
   - The skin thins, the open region moves inward, and the clump is pumped out on ~100–150 Myr/α. In the continuum equation the same
     holds: the drift acts on f(x, v) for all v wherever d(x) > 0.
   - In the drift-only model (CFG882) an overfilled cell can never be reached, because it does not move. That is the only reason V2
     retained exactly.
   - The trigger amplitude does not matter over the tested range: shot noise halved and ε ×10 change t_50 by ≤ 8%. With zero
     fluctuations and a strictly positive overfill nothing would happen, but CFG877's coded hard cap puts d = 0 exactly outside the
     cap, so the knife edge sits on the clump.
2. **CFG882's knife edge is healed, not disarmed.** Mixing refills empty cells within about 10 Myr (Dmix2), and no holes ever appear
   with orbits. The one-way push remains. With the OU off, the halo inside ~1–2 kpc is pushed out until the clump's excess is fully
   compensated (C(1 kpc) ≈ 0, overshooting to −0.30 at 2 kpc). That is CFG882's "ratchet to completion", but it happens after the
   clump has already drained.
3. **What this does to the record.**
   - CFG882's "RETENTION REQUIRES THE GATE" becomes "the gate is not enough": gated retention is 11–14× longer than ungated but
     still needs α ≲ 1e-2 (extrapolated) for 12 Gyr.
   - The clump (CFG877/878 route 2) therefore has no retention mechanism in the stated equations at α in the galaxy-side range.
   - Keeping it would need a new ingredient: a clump whose orbits never reach a settled (d ≈ 0) region, or a rule other than HG that
     stops the drift at the clump's skin. Both would be new assumptions. Neither is supplied or adopted here.
4. **The merger side of CFG639 is untouched.** Gating still switches off settling inside an overfilled merging halo, which keeps the
   result that mergers stay collisionless. This lane shows only that the gate is not a retention mechanism for a bound overfill
   embedded in a settled halo.

## Limits

- Spherical shells (no non-radial instabilities). Isolated illustrative Plummer hosts; static baryons and phantom.
- Catchment taper at 3–5 kpc instead of CFG882's 20-kpc box. Smooth clump cap instead of CFG877's hard cap.
- The clump's own gravity is Newtonian. CFG877's M_cl assumes the law boosts it; CFG882's caveat applies.
- FIX-2's OU is the record's posited closure. Its non-neutrality (K-OU) is a property of that closure on this equilibrium, plus noise
  in sparse central bins.
- t_50 at α < 0.5 is extrapolated (one α = 0.05 run to 1.5 Gyr).
- H1 numerically unreliable. The 12–13% escape past the catchment edge comes from the OU tails and the taper.

## Corrections and disclosures (2026-10-20)

- **Pre-freeze scratch prototype** (disclosed in the criteria): equilibrium builder and Vlasov integrator only, no drift, OU or
  gate. It set the K-V tolerances.
- **Implementation detail before the parts ran:** the Eddington energy grid was changed from quadratic to cosine spacing (6000
  nodes). This fixed the ρ-from-f check at 1 pc, which was wrong in the prototype. It is an equilibrium-construction detail, made
  before any frozen part.
- **Smoke test before the parts:** each mode (gated, ungated, drift-only; clump and no clump) was run for 30 Myr by importing the
  module, to check the code ran. Early numbers were seen (for example, the gated clump R was 0.996 at 30 Myr). Nothing in the criteria
  or code changed afterwards.
- **K1b NOT APPLICABLE by construction.** The catchment-taper bins near R2 have m_tgt → 0, so any occupied one has d < 0, and "d > 0
  in every occupied bin" can never hold. It is reported as frozen (not a FAIL). The code-path identity K1 passes.
- **D-mix (frozen diagnostic) was mis-designed.** Removing the particles changed the potential, and the whole system expanded
  (f_esc 33%), so only its first ~50 Myr say anything (H_e 0.5 → 0 within 10 Myr). The post-hoc Dmix2 moves particles instead of
  removing them.
- **HEALED as frozen** mixes holes with the eroded clump's outer mass (see (b)). It is reported as frozen.
- **The post-hoc parts P1/P2 and the summary's post-hoc section** were added after the frozen results had been seen (no class weight).
  Part K was re-run with the final script and is identical.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (0337ade83) |
| `cfg889.py` | script (parts, post-hoc parts, summary) |
| `run_889.sh`, `run_889_posthoc.sh` | runners |
| `cfg889.out`, `cfg889_results.json` | summary (frozen class + post-hoc section) |
| `cfg889_MUTATE.out`, `cfg889_results_MUTATE.json` | MUTATE summary (M1) |
| `parts/part_*.json`, `parts/part_*.out`, `parts/run_889*.log` | per-part runs (snapshots every 10 Myr, R series) |
