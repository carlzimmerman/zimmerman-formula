# O04 — THE JOINT DEEP-A0 STATEMENT (synthesis wave, 2026-09-23)

**Status: L06-partial.** O01 (G114-dwarfs a0_eff), O02 (HeCS virial-T z-invariance) and
O03 (MW rotation curve) have NOT landed at execution time; N01 (density-locality on SPARC)
is RUNNING (live process, only the 3-line preamble `.out` written). This statement builds
the joint framework with every missing number marked **PENDING** — no number below is
invented; every value is quoted from its lane file (paths given). Per-channel a0_eff rows
that have not landed are placeholders by design.

Reference: registered a0 = 9.3619e-11 m/s^2 (a0_DE; L06_results.json, N05_results.json).

---

## (1) THE a0_eff TABLE

| Channel | Status | a0_eff/a0 | SE (a0_eff/a0) | z vs 1.0 | N | Systematics channel | Files |
|---|---|---|---|---|---|---|---|
| **SPARC-deep (L06)** — deep HI rotation curves, g_bar < 0.2 a0 | **LANDED** | **0.7241** (= 6.78e-11 m/s^2 = 0.73 a0, L06 verdict) | **± 0.0662** (galaxy-clustered bootstrap, se_Delta_used = 6.425e-23 on a0·E[g_bar] = 9.712e-22) | **−4.17** (verdict text: 4.2-sigma) | 1152 rings / 135 gals | HI rotation curves (SPARC, G071 conventions: v_b^2 = sign(Vgas)Vgas^2 + m2l(Vdisk^2+Vbul^2), m2l fallback 0.5; inclination/modeling systematics in the clustered SE) | `deepseek_push/L06_results.json`, `deepseek_push/N05_results.json` (leg `deep_sparc_L06`: Delta = −2.679e-22, a0eff_a0 = 0.7241) |
| **G114-dwarfs (O01)** — dwarf resolved kinematics, deepest regime | **PENDING** (data layer LANDED as G114) | *a0_eff: PENDING — no O01 file exists* | — | — | 55 dwarfs (26 LT + 29 FIGGS) | Dwarf resolved kinematics (LT: V_max AD-corrected at R_max; FIGGS: pressure-corrected V_rot at last point; M_star KIN/SED or diet-Salpeter M/L) | `deepseek_push/G114_results.json` (rms 0.150 dex, median r +0.015, N=55; **deep tail g_N<0.1 a0, N=7: median r = −0.094 dex, rms 0.168** — sitting ON the (G M_b a0)^(1/4) line; median r/SE = −1.5σ, consistent with both a0=1 and 0.73 a0 within ~1σ) |
| **MW (O03)** — MW rotation curve / MW tracers | **PENDING** — no O03 file exists | *PENDING* | — | — | — | MW tracers (in-repo Eilers+19 38 pts 5.27–24.82 kpc; Ou+24 37 pts 6.3–27.3 kpc; tangent-point gas kinematics; G072/G157 lanes landed) | `deepseek_push/G072_mw_law.out`, `deepseek_push/G157_slope_floor.py` (context; O03 itself PENDING) |
| *(adjacent, not one of the three) HeCS virial-T z-invariance = **O02** — PENDING, no file* | — | — | — | — | — | cluster virial-T anchor (E1/E2 z-invariance registrations; G236 eRASS3 catalogue-only) | — |

**Registered deep a0\* context (landed lanes, quoted):** ZD08 velocity-domain a0\* = 6.015e-11
(= 0.94 × the registered SPARC-deep a0\* = 6.407e-11, 6% agreement, `ZD08_results.json`);
G03D bare register a0 = 6.48e-11 = 0.69 a0_DE (`g03d_efe_refit_results.json`); G208 in-file
SPARC_deep_fit = 6.43e-11 (N01 docstring register reconciliation). The L06 a0_eff = 6.78e-11
sits in this 0.69–0.73 family.

---

## (2) THE JOINT TEST

**Combined a0_eff (inverse-variance weighted):** x̄ = Σ(x_i/σ_i²)/Σ(1/σ_i²),
SE = 1/√Σ(1/σ_i²), z = (x̄ − 1)/SE.

- With the **one landed channel** (L06): **combined = 0.724 ± 0.066 → z = −4.17**:
  the deep regime as measured on SPARC rings is **inconsistent with a0 = 9.3619e-11 at
  4.2σ (clustered SE)**. This IS the registered L06 tension; the joint number equals the
  single channel until O01/O03 land.
- **Joint (3-channel): PENDING** — requires ≥ 2 landed a0_eff channels. Placeholder rows:
  O01 = *PENDING*, O03 = *PENDING*.
- **Consistency of the three channels with each other: chi2 = Σ(x_i − x̄_w)²/σ_i² over the
  landed channels → PENDING** (n = 1 landed: undefined; needs O01/O03). Non-decision
  caution already on the record: the deep regime is **two-sided** — MIGHTEE deep
  (N=72 rings, `N05_results.json`) measures a0_eff/a0 = 2.16, z = +6.58, **opposite sign**
  to SPARC-deep (the G199 1.87× normalization rung): a pooled deep reading is a
  ring-weighted tug-of-war (pooled fraction −0.235, `N05_results.json`). Any joint
  statement must first referee that sign split; O01/O03 are the referee lanes.

---

## (3) THE TWO EXPLANATIONS — which survives

**(a) Deep a0 suppression = density-locality, a0(rho) = (c/2)√(G·rho), rho < rho_Lambda**
(the framework's own law: S1 "KP1 as the local-a0 law", `G_SYNTH_geometric_spine.py`;
canonical a0 ↔ rho_Lambda = 4a0²/(Gc²) = **5.8e-27 kg/m³** (`G155_sourced_eq.py`)).
Verdict: **SURVIVES-UNDECIDED (discriminator armed, N01 in flight).** The L06 number
(0.73 a0, −4.2σ) is exactly the *direction* this law predicts for outer-disk densities
below rho_Lambda, and the landed G114 deep tail (7 dwarfs ON the line, median −0.094 dex,
velocity-level −1.5σ) neither confirms nor kills it. The deciding legs, all pre-registered:
N01 (SPARC-side, running: per-bin a0_eff vs (c/2)√(G rho_gas), h ∈ {100,300,1000} pc, TWO
kill conditions — (a) a0_eff flat across >3× rho variation → DEAD; (b) cross-bin slope off
1/2 power at >5 SE → wrong mapping); O01's G114 f_gas-bin cross-checks (gas-dominated
subset f_gas ≥ 0.7, N=39, rms 0.124 dex — the M_b systematics are minimal exactly where
gas dominates); O03's MW annuli.

**(b) Deep slope change (Milgrom deep slope 1/2 → wrong)**
Verdict: **NOT EXCLUDED empirically, DISFAVORED by the framework's own derivations —
PENDING the O-lanes.** N05's pre-registered discriminator (`N05_results.json`): the 5-SE
M1 kill "excludes the normalization-only family {a0_eff = 1} but CANNOT attribute between
H_A (a0_eff = 0.73 a0: slope 1/2, intercept −0.068 dex) and H_B (slope 0.55, intercept 0)"
— the lines cross at 0.0433 a0 inside the band, and exact LR separates them at only 1.9σ
at the kill N (5σ attribution ≈ 11,699 SPARC-class deep rings; ≈542 with the resolved-SED
recipe). So the moment data as they stand **cannot** kill (b). Against (b): the PD-series
derives the deep slope as the metric's two-channel count, kappa = 1/2 **unique**
(PD07/PD13, Lean, zero sorry), and PD10 measures the SPARC deep slope index cp = 1 ± 0.0033
— the data measure the framework's own 1/2 to 0.33%; (b) would require breaking the
OR-composition premise. O01's dwarf kinematics and O03's MW annuli (plus the deep-HI survey
execution of N05's program card) are the registered attribution instruments.

**Bottom line: with O01/O02/O03 PENDING and N01 RUNNING, neither explanation is decided;
the joint framework above is the scoring table they land into.** The one settled joint fact:
the deep regime is in 4.2σ tension with a0 = 9.3619e-11 on the SPARC-HI channel, with a
sign-contradicting MIGHTEE deep reading on the record.

---

## (4) THE NEXT DOORS THIS STATEMENT OPENS (pre-registered)

1. **UDG / low-SB sample from `G114_data/leisman` figures** — the Leisman+17 HUDS route
   (in-repo: `deepseek_push/G114_data/leisman/`, AGC 122966/219533/334315 PDF figures;
   G114 appendix table gives M_dyn(8 kpc)-derived V_obs, marked UNVERIFIED/DERIVED): the
   lowest-surface-density dwarf channel; resolved kinematics (or M_dyn) on this sample is a
   fourth deep-a0_eff leg far below rho_Lambda where (a) and (b) separate hardest.
2. **Deep-HI surveys** — N05 program card (MeerKAT L-band, MIGHTEE-class): ~59 new deep-HI
   galaxies / ~177 new rings (total ~1329 deep rings / 194 galaxies) for a 5-SE M1 kill;
   MIGHTEE-HI itself (resolved 10-band SEDs, σ_int = 0.045 dex) as the sibling HI channel;
   VLA-B outer rings on the 16 residual never-doubling dwarfs (ZD08 C3 instrument) — all
   three refit the joint combined-a0_eff directly.
3. **PHANGS** — PHANGS-ALMA/MUSE resolved kinematics as the MW-class annulus cross-check
   (star-formation + CO tracer channel orthogonal to HI), completing O03's tracer channel.
4. **O02 HeCS virial-T z-invariance** — the cluster-scale deep channel: a0(z) sharp null
   (Δlog10 T = 0.000 at z ≤ 1) against the virial-T anchor; eRASS3 catalogue-only release
   is the waiting gate (G236 registrations).

---

## DISCIPLINE

No git commit. Every number traced to a lane file (paths above). PENDING = no lane file
exists at 2026-09-23 20:45 EDT (O01/O02/O03) or process running with preamble-only output
(N01, PID live). The combined ± SE, z, and chi2 are arithmetic on quoted lane values
(scripted, reproduced exactly: ratio 0.724123, SE 0.066150, z −4.1705).