# Z2_satellite_systematics: FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** The dwarf satellites sit +1.33 / +1.30 dex above v3's static prediction (S1), about +2.0 dex above v3's
dust-free dynamical prediction (U1 B0), and +0.55 / +0.50 dex above isolated AQUAL (S1 S2). How much of that is real?
And why does T1 see the residual rise with host field (+0.76 ± 0.26 dex per dex at ε = 0) while CFG838/839 found no
tidal or host-distance signal?

**Read before freezing (disclosed).** The aggregate results of S1, T1 (incl. A3), U1, E3, CFG838, CFG839, CFG875 and the
LEDGER rows CFG822–CFG878. The per-system residuals of 4 systems (Aquarius II, Boötes I–III) were seen in CSV headers.
No residual has been split, correlated or regressed against any flag below. Input availability (PMs, ellipticities,
member counts, σ references) was listed without residuals.

κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 / alt 1.1312e-10 m/s², never pooled. No dark-matter particle (the
extra mass is cold energy). Not "theory closed". Nothing here says the data favour the framework.

## 1. Sample, data side, statistic (E3/S1, rebuilt with this lane's own code)

- **Sample S_E3:** LVD MW + M31 + local-field rows with σ_los > 0, R_e > 0, log M★(Υ_V = 2) < log(a₀ L★²/G), L★ = 24 pc.
  45 canonical / 46 alt (alt adds Andromeda XXVIII).
- **Data (primary, "clean" in E3's sense):** LVD σ × Arroyo-Polonio free-f ratio (system-specific where matched, else
  the median ratio); 2000 MC draws of σ, R_e and distance modulus (split normals); g_obs = 3σ²/r₁₂, g_bar = G(M★/2)/r₁₂²,
  r₁₂ = (4/3)R_e. **W** (worst-clean: Υ_V 4, f = 0.7, lower of LVD/DEIMOS σ, no upper limits) reported beside it.
- **Statistic:** Δ_F = bootstrap median over systems of the per-draw log₁₀(g_obs/g_pred,F) (4000 resamples of systems ×
  random MC column), ± its bootstrap sd. A split reports Δ_in, Δ_out and Δ_in − Δ_out (independent bootstraps).
  Regressions use per-system central residuals r_i (T1's convention): OLS slope ± bootstrap sd (4000), Spearman ρ with a
  permutation p (10000 permutations, seeded), Theil–Sen slope.
- **Flavors F (prediction subtracted), all on the stiffened AQUAL solver of D10 (read-only), μ = x/(1+x), E-W estimator:**
  - **V3S** v3 static: AQUAL + host field (E_mid) + native screening at the L★ floor 21.68 / 22.85 pc (S1 S4).
  - **V3D** v3 dynamical, dust-free (U1 B0): Newtonian Plummer (no held dust in a falling satellite).
  - **MOND** plain AQUAL with the host field, L★ = 0 (S1 S3). Side row **ISO**: isolated AQUAL, L★ = 0 (S1 S2).
  - T1's ε = 0 prediction (**V3S0**: isolated, screened at the floor) is used only for the reconciliation (§2).

## 2. Task 1: reconcile T1 with CFG838/839 (factor grid, every cell reported)

- **Samples:** S_E3; S_838 = CFG838's 24 MW/M31 satellites (CFG828's dwarfs with a host); S_839 = CFG839's 12 MW
  satellites with PMs; S_ovl = S_E3 ∩ S_838.
- **Residuals:** R_828 = CFG828's committed Δ (ν_e law, Υ_SFH, literature σ; S_838/S_839 only); and, in E3's data
  conventions for every system, R_N (Newton), R_ISO, R_V3S0 (T1 ε = 0), R_V3S (T1 ε = 1).
- **Variables:** log x_e (S1's host field, E_mid; M31 1e11; field systems in the MW field at heliocentric distance),
  log D_host, log T_now (CFG838's tidal parameter |dg_host/dD| r₁₂ / g_int, with S1's host field and g_int the isolated
  AQUAL field at r₁₂ from the stars), log T_peri (same at the PM-based pericentre, §3a).
- **Statistics:** T1's OLS slope (sign convention: + = residual rises with x_e or T, falls with D) and Spearman ρ
  (one-sided in the same direction).
- **Attribution rule.** Start from T1's cell (S_E3, R_V3S0, log x_e, OLS). Change one factor at a time toward CFG838's
  cell (S_838, R_828, log T_now / D, Spearman). A factor is **the cause** if changing it alone moves the trend from
  ≥ 2 sd (or p < 0.05) to < 1 sd (or p > 0.2) on the same cells; more than one factor may qualify. If no single swap
  does, the reading is **COMBINED**.

## 3. Task 2: physical systematics (pre-declared splits/regressions on S_E3, both footings, every flavor)

**(a) Tidal susceptibility at pericentre.** q_F = r₁₂ / r_t, King's radius r_t³ = G m_F / (Ω_p² − Φ''(r_p)), Ω_p = L/r_p².
- Orbit: LVD ra, dec, heliocentric distance, pmra, pmdec, vlos_systemic → astropy's default Galactocentric frame (as
  CFG839); turning points in **S1's own MW field** (law with μ = x/(1+x) on a Hernquist M_b 6e10 M☉, a_H 3 kpc; E_lo/E_hi
  bracket). Static, spherical, no LMC (disclosed). Leo T is integrated in the MW field. M31 satellites have no PMs on
  disk: their q is **not certifiable** (q at the present distance is reported as a lower bound).
- Satellite mass m_F = M★ × 10^{logG_F} / f_W (f_W = Newtonian Plummer E-W factor), i.e. the mass flavor F says it has.
  V3D: m = M★ (strictest). 300 MC draws of PM, distance, v_los give a q interval; flags use the central orbit.
- **Threshold (frozen):** tidally safe q_F < 0.5; exposed q_F ≥ 1.
- Tests: split q_F < 0.5 vs ≥ 0.5; Spearman/OLS of r_F on log q_F; and, because q_F and r_F share m_F (partly by
  construction), the **partial slope on log ρ_tid** (host tidal density (Ω_p² − Φ'')/G at pericentre) with log(m_F/r₁₂³)
  as control. **TIDES IMPLICATED (flavor F)** iff that partial slope is ≥ +2 sd.

**(b) Tidal morphology / kinematics.** Ellipticity flag ε ≥ 0.5 (LVD; an upper limit < 0.5 is not flagged). Velocity
gradient: Walker et al. 2023 per-star velocities on disk, CFG51's membership rule (imported read-only), systems with
≥ 10 members; likelihood-ratio test of v = μ + k·(ξ, η) with free σ vs no gradient (2 dof); flag if p < 0.01. Systems
without per-star data on disk are not flagged (disclosed; not certifiable). Tests: split and Spearman on ε.

**(c) Measurement quality.** N_q = member count of the dataset LVD's σ cites, where on disk (Geha 2026 II when LVD cites
Geha 2026; Collins 2013 when LVD cites Collins 2013; Arroyo-Polonio when its reference equals LVD's; Geha-cited systems
absent from Geha II have N < 10 by that paper's rule); otherwise the proxy N_eff = ½(σ/δσ)², δσ = mean of LVD's
asymmetric errors. Tests: split N_q ≥ 10 vs < 10; Spearman on log N_q and on δσ/σ. Reported only: system-specific vs
median binary correction.

**(d) UFD vs classical:** UFD iff M_V > −7.7. Split.

**(e) Host distance and host field:** OLS/Spearman on log D_host and log x_e; MW vs M31 split; Leo T noted.

**Dynamically clean subset (frozen), per flavor F:** C1 q_F < 0.5 from a PM-based pericentre; C2 ε < 0.5; C3 no velocity
gradient flag (where testable); C4 N_q ≥ 10. Also reported: **STRICT** = clean under m = M★ (V3D's q, every flavor);
**C2–C4 only** (no PM needed, includes M31). A subset with N < 6 is **TOO FEW** (numbers shown, no class).

## 4. Verdict lines (per flavor and footing)

- **V1 robustness.** **ROBUST** if Δ_F(clean) ≥ 3 sd above zero and ≥ ½ Δ_F(all); **REDUCED** if ≥ 2 sd above zero but
  < ½ Δ_F(all); **NOT ROBUST** if < 2 sd. W in the clean subset reported beside it.
- **V2 systematics fraction.** f_sys = 1 − Δ_F(clean)/Δ_F(all), with the clean subset recomputed inside each bootstrap
  resample of S_E3; 68 % and 95 % percentile intervals. Per-test fractions f_k = 1 − Δ_F(passes test k)/Δ_F(all).
  Caveat (frozen): C1 selects denser systems, so f_sys mixes tides with any density dependence of the residual.
- **V3 T1's host-field trend.** On S_E3 with R_V3S0 and log x_e:
  - **TRACKS HOST FIELD** if all hold: partial OLS slope with log y₀ and log Λ (= log L★/R_e) controlled ≥ 2 sd; MW-only
    Spearman one-sided p < 0.05; every drop-one (jackknife) slope > 0; Theil–Sen slope > 0.
  - **PROXY (named)** if the partial slope on log x_e falls below 1 sd once one named covariate (log y₀, log Λ, M_V,
    log σ, binary-correction status, M31 membership) is added and that covariate's own partial slope is ≥ 2 sd.
  - **NOT ROBUST** if the Spearman permutation p > 0.05 or one drop-one removes it (< 1 sd), and no PROXY applies.
  - **UNDECIDED** otherwise.
- **V4 flavors.** For each flavor: the clean-subset Δ, its class, and whether TIDES IMPLICATED fired. A flavor whose
  excess is ROBUST in the clean subset has a real satellite excess that systematics do not remove.

## 5. Checks (script prints `K# PASS/FAIL value threshold`; exit 0 iff all pass)

- K1 E3 reproduced with this lane's own code: Newton E_N +2.013 / +1.998 and the unscreened law +0.557 / +0.508, |Δ| ≤ 0.02.
- K2 S1 reproduced: S4 +1.331 / +1.299, S3 +1.130 / +1.075, S2 +0.553 / +0.502 (|Δ| ≤ 0.02); per-system central logG
  vs `s1_per_system.csv` max |Δ| ≤ 0.01; V3D vs U1's Delta_B0 max |Δ| ≤ 0.005.
- K3 T1 reproduced: tracking slope at ε = 0 +0.761 / +0.838 and A3 partial +0.779 / +0.853 (|Δ| ≤ 0.02).
- K4 CFG838/839 reproduced from their committed rows: ρ(Δ, log T) −0.00, ρ(Δ, D) −0.02, ρ(Δ, log T_peri) +0.08
  (|Δ| ≤ 0.01); this lane's orbit code in CFG839's field gives Draco r_p / r_a 53.4 / 120.0 kpc within 2 %.
- K5 orbit code: turning points vs a direct leapfrog in S1's MW field (Draco) within 2 %.
- K6 King radius: Newtonian point mass, circular orbit → r_t = r (m/3M)^{1/3} to 1e-3.
- K7 gradient test: an injected 10 km/s/kpc gradient on a real member set is recovered (p < 0.01); shuffled
  velocities give a false-flag rate ≤ 3 % (200 shuffles).
- K8 peak RSS < 1 GB.
- **`--mutate`** (separate `*_MUTATE.*` outputs): every system's data are replaced by a pure tidal artefact,
  log(g_obs/g_bar) = V3S prediction + log₁₀ q_V3S + N(0, 0.1) (seed 2), with q_V3S computed at the present distance for
  systems without a pericentre. K1–K3 must FAIL; TIDES IMPLICATED must fire for V3S; the host-field permutation control
  must not class TRACKS HOST FIELD.

Compute: `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB, minutes. No downloads. Missing data are listed, not fetched.
Commits: this lane's paths only, pathspec; never push.
