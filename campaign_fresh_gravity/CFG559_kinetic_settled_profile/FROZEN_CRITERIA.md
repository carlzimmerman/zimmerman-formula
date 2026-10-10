# CFG559 FROZEN CRITERIA: a kinetically supported settled profile. Does one kinetic profile fix growth AND KiDS?

Frozen 2026-10-10, before any CFG559 script is written or any CFG559 number is computed. Committed alone, never edited afterwards; later notes go in the README as dated disclosures.

Standing settings: κ = ½ is FITTED; footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s², scored separately, never pooled; flat a0; kernel ν_mono; candidate B; G9 (only real mass gravitates); no EFE. The cold energy's MASS is still required; no particle species. Not "theory closed"; nothing here says the data favour the framework. Other lanes are read-only (imported or exec'd, never edited); CFG558 (running) is not touched and is read only at the end, if its results exist. No downloads, no PM runs; nice -n 10, ≤ 4 processes.

## 0. Hypothesis and the one change

CFG557: with the α-free finite-age supply ceiling s_c* (0.80 → 0.50 over log M_ta 11 → 15) and a SHARP supply edge, growth still fails (E +0.382 / +0.458 at k ≈ 1) and KiDS f30 gets worse (median edge x = r_e/r_ta 0.196 / 0.169; KiDS prefers x ≈ 0.45–0.50). Hypothesis: the excess is the settled cold energy being too concentrated inside a sharp edge. A kinetically supported settled halo (isotropic Jeans support, CFG544 FIX-2 = CFG554 route (b) end state) spreads settled mass outward, lowering the mass at ~0.3 r_ta and moving the effective edge outward. The ONE change in every test below: the source lane's sharp settled profile gets the kinetic redistribution Δm defined in §1. No knob is introduced or scanned.

## 1. The kinetic profile (task 1)

**What the cold energy feels.** G9: the field is that of real mass, baryons + all settled cold energy. In candidate B the settled cold energy IS the phantom: the self-consistent requirement is ρ_c = ρ_ph (total mass = the law's) wherever the supply can hold it. This is enforced by FIX-2's two-sided drift v_s = ατ(g_law − g) toward ρ_ph (CFG544 FIX-1); kinetic support is FIX-2's Ornstein–Uhlenbeck relaxation at rate α/τ toward the isotropic Jeans dispersion σ_J² = (1/ρ_c)∫_r ρ_c g dr' of the CURRENT cold-energy density in the CURRENT real-mass field (CFG554 (b); its isotropic target is POSITED per CFG554, the metriplectic structure derived). The phantom never enters Φ.

**How it is solved (direct, per halo; no scaling assumption).** For each grid halo the CFG544 spherical N-body toy is imported unchanged (as CFG554 does) and run with FIX-2 (rule = two-sided, OU on, OU target ×1, α = 1), IC-B (cold uniform infall inside r_ta, 0.05 V_f seed), T = 10 Gyr (CFG554's bench end state), N = 30000, seed 544, code step 5e-4, CFG544's EPS, RMIN, 100 bins. The cell in code units (r_* = 1, V_f = 1, G = 1):
- point-mass baryons M_b = f_ret f_b M_ta (census f_ret, CFG556 `fret_of`);
- settled mass M_set = s_c (1 − f_b) M_ta, with s_c = CFG557's tested α-free free-fall ceiling s_c*(M_ta, z = 0, footing) read from `cfg557_derive_results.json` (PRIMARY) and s_c = 1 (full turnaround supply, DECLARED VARIANT, reported);
- r_* = r_M / ln(1 + M_b/M_set) (the sharp-edge radius, the same formula as CFG556/557), r_M = √(G M_b/a0); code M_b = r_M/r_*, code M_cat = (M_set/M_b) r_M/r_*;
- r_ta/r_* with r_ta from CFG556's `halo_basics` (Δ_ta = 11.81); t_u = r_*/V_f, V_f = (G M_b a0)^{1/4}.
The toy depends only on the dimensionless numbers (r_M/r_*, M_set/M_b, r_ta/r_*, T/t_u), all reported per cell; the "scaling" is therefore exact in code units and each halo is run directly.

**Grid.** log M_ta (Msun/h) = 11.0, 11.5, …, 15.0 (9 nodes; the nearest CFG556 grid halos) × 2 footings × {primary s_c*, variant s_c = 1} = 36 runs (+ 18 MUTATE runs, §4, + 2 control runs).

**Profile extraction.** m_kin(x) = cumulative cold-energy mass fraction vs x = r/r_*, averaged over the 5 snapshots t = 9.0, 9.25, …, 10.0 Gyr; particles beyond r_ta are counted at r_ta (R3: mass inside r_ta is conserved); m_sharp(x) = min(M_ph(<x)/M_set, 1) for the toy's own point-mass phantom (ν_mono). **Δm(x) = m_kin(x) − m_sharp(x)** on x = geomspace(1e-3, x_ta, 400). Reported per cell: r_50, r_90, r_99 of m_kin in units of r_* and of r_ta; ln(r_99/r_99,sharp); Δm at x = 0.05, 0.1, 0.3, 0.5, 1, 1.5, 2; the fraction beyond r_ta; CFG544's diagnostics (log X, D, β, steadiness over the last 2 Gyr, G550 gate). A cell that fails CFG544's gate is flagged "not steady" (reported; its Δm is still used, no substitution).

**Application rule (every test).** Settled profile S_kin(r) = S_sharp(r) + M_set,i · Δm(r/r_e,i), where S_sharp is the source lane's own sharp settled profile (exactly as in CFG557), r_e,i its own edge, and M_set,i its own settled phantom mass at the edge (S_sharp(r_e)). Δm is taken at the object's own census log M_ta, linear in log M_ta between nodes (clamped at 11 and 15), matched in footing and supply variant. Lens/epoch dependence of Δm is not modelled (z = 0 runs, declared). Everything else is the source lane's machinery.

## 2. Tests (task 2), each per footing, primary supply

(i) **Growth, CFG556 halo model** (as CFG557 `frame_profile_sc` with s_c*, + the kinetic term; drained shell, mass inside r_ta conserved). **PASS** iff max |R − 1| ≤ 0.10 over 0.05 ≤ k ≤ 1 h/Mpc AND |σ8,F/σ8,L − 1| ≤ 0.05. Reported: R at k = 0.3/0.5/1, ratio form, drivers by mass decade, M_F/M_L at r/r_ta = 0.1, 0.2, 0.3, 0.5, the change vs CFG557.

(ii) **KiDS f30, CFG529 machinery** (constructions A and B, measured f30 leakage; CFG557's `edge_new` s_c* edge per group at its census M_ta and lens z). The variants path is copied with ONE change: the intrinsic cumulative phantom Md(r) on the extended grid becomes Md + Md(r_out)·Δm(r/r_out) (r_out = min(r_e, r_ta)), and construction A is evaluated on the extended grid (the tail lies beyond r_out). **PASS** iff p > 0.01 in both A and B. Reported: χ², p, inner-9 / outer-6 split, Δ vs CFG529's best sharp node, median effective edge x_99 = r_99/r_ta, the change vs CFG557.

(iii) **Groups, CFG543 P2** (CFG557's per-group s_c*; `sigma_log` copied with ONE change: g += G M_set Δm(r/r_e)/r², r_e = the edge radius, M_set = the phantom at the edge). **PASS** iff |Z| < 2.

(iv) **MW inside 30 kpc** (CFG513 Prof with CFG557's s_c*; Δm at the MW's census M_ta). Report ΔM_c(<r) and ΔV_c(r) at r = 8.2, 16, 20, 30 kpc (and 60 kpc, context), each with the toy's Poisson error, and ΔΣ_dark(|z| < 1.1 kpc) at R0 ≈ 2 × 1.1 kpc × Δρ_c(R0) against CFG553's sealed numbers (not changed). **PASS** iff |ΔV_c| at 20 kpc ≤ 5.4 km/s (half-width of CFG553's census band on V(20 kpc) canonical, 193.9–204.8) AND |ΔV_c| ≤ 5.4 km/s at every r ≤ 30 kpc AND |ΔΣ_dark(R0)| ≤ 5.8 M☉ pc⁻² (half-width of CFG553's K_z(R0, 1.1) census band). The sealed predictions themselves are NOT changed.

(v) **LG timing, CFG522 M1** (CFG557's ShellPair with s_c* and the unsettled drained shell; each galaxy's settled cold profile + M_set,i Δm(d/r_e,i)). **PASS** iff |z_full| < 2. Reported: z_meas (strict radial), M_eff(<780 kpc).

## 3. Verdicts (frozen)

Per test PASS / FAIL with numbers, per footing (primary supply). Overall per footing:
- **KINETIC PROFILE RESOLVES THE CONFLICT** iff all five PASS;
- **PARTIAL** iff at least one of growth (i) and KiDS (ii) passes but not all five (list which pass);
- **DOES NOT** iff growth and KiDS both fail.
Also reported (no verdict): whether the kinetic profile moves BOTH growth and KiDS toward the data (E down AND KiDS χ² down vs CFG557), and the full-supply variant's five results.

## 4. MUTATE (`CFG559_MUTATE=1`; separate `_MUTATE` outputs; exit 1 iff all teeth bite)

- **MK0, kinetic support off (σ = 0, sharp edge ⇔ Δm ≡ 0):** reproduces CFG557's stored numbers: halo model R(k) and σ8 ratio to 1e-10 (both footings); groups P2 means to 1e-6; LG z_full to 1e-6; MW edge to 1e-9 relative; KiDS χ² (A, B, both footings) to 1e-6 by scoring CFG557's cached tables through this lane's scorer. Reported (not a tooth): this lane's kinetic code path run with Δm ≡ 0 vs the source path (max relative table difference and χ² difference).
- **MK2, σ ×2 (OU target σ_J² × 4), primary supply:** the 18 primary toy cells re-run; halo model and KiDS re-scored. **Bites** iff r_99/r_* exceeds the σ ×1 value in all 18 cells AND the halo-model E is lower than σ ×1 on both footings AND the KiDS median x_99 is larger than σ ×1 on both footings (the response has the declared sign: over-spreading). Reported: whether it passes the data (R(k = 1) < 0.90, KiDS χ² and outer-6 residual sign).
- A MUTATE failure labels the lane NO LABEL.

## 5. Controls (all must pass, else NO LABEL)

- **C5:** this lane's run loop reproduces CFG544's stored FIX-2 IC-B 10 Gyr end states (log X, D) for MW_can and cluster_can (CFG544's own cells) to 1e-9.
- **C6:** m_sharp(1) = 1 to 1e-9 in every cell (the edge formula is the toy's exact point-mass edge).
- **C7:** mass exact in every run (no particle lost).
- **KK0:** the CFG529 scorer reproduces its stored census χ² (as CFG557).

## 6. Outputs

`cfg559_toy.py` (task 1, toy grid → `cfg559_toy_results.json`, Δm tables), `cfg559_tests.py` (halo model, groups, MW, LG), `cfg559_kids.py`; `.out` / `_MUTATE.out`; `*_results*.json`; `README.md`. KiDS tables cached outside git in `_external_data/cfg559_work/`. Lane folder only, specific paths, committed with a message starting "CFG559 results:"; not pushed.

## 7. Pre-freeze disclosure (dated 2026-10-10)

Read before freezing: CFG557 README/criteria/tests/kids scripts, CFG556 README and code, CFG544 and CFG554 READMEs and the toy code, CFG558 criteria (not results), CFG529 tables code, CFG504 `kids_Md_ext`, CFG543 `sigma_log`, CFG522 `Pair`, CFG513 `Prof`, CFG553 headline table. Hand estimates (no script run): CFG556's crude 25% / 55% taper with the full catchment lowered E only from +0.715 to +0.671 / +0.572; scaled to the CFG557 ceiling (+0.382) a comparable softening would give roughly +0.30–0.35, so growth is expected to stay above 0.10; an r_99 shift of +25–55% moves the KiDS median effective edge from about 0.20 to about 0.25–0.30, still short of 0.45, so KiDS is also expected to fail. Inside 30 kpc the MW is expected unchanged within the toy noise (the drift holds ρ_c = ρ_ph in 0.1–0.9 r_* to |D| ≤ 0.027 in CFG544/554). None of these sets a threshold above.
