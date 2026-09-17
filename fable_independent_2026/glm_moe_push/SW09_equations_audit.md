# SW09 — Equations Audit (do-not-redo map)

- Lane: `fable_independent_2026/glm_moe_push/` — SW01–SW08 landed and pushed at `9fa915a01` (anchor as declared; verified by filename glob + mtime only — **no git commands used**, so "since 9fa915a01" is a filename/mtime heuristic, not a commit check).
- Scope: read-only + exactly this one file. Nothing else was touched.
- Method: `rg`/`find` over the lane `.py`/`.out` files and repo-wide for the OPEN-spec symbols. All provenance below was read off disk in this audit swing.

**Context reconciliation.** The five framework equations and the ON-RECORD P1–P9 numbers were present in the task brief and were **independently verified against the on-disk `.out` files** — every number quoted below was confirmed in-repo (grep evidence per row). No value is cited from the brief alone; nothing is fabricated.

---

## 1. Framework equations — verbatim + provenance

All owner lane: `fable_independent_2026/glm_moe_push` unless noted.

| # | Equation (verbatim from source) | Provenance (file:line) | Status | Verification / gate |
|---|---|---|---|---|
| E1 | `Gamma^2 = <|g_N|^2>_ang - \|<g_N>_ang\|^2       (angular variance: the field's own structure)` | `SW01_envscalar_response.py:11` (canonical statement); computed by quadrature `SW01b_envscalar_orthogonality.py:108–136` | **computed** | SW01b C1: centered sphere `eta = 0, Gamma = g_N` (quadrature, <1e-10); C2 superposition; C3 offset hinge `Gamma = 1.33` at d = 0.5 r vs 1.00 centered — barycenter condition is load-bearing (SW08 reuses it) |
| E2 | `eta     = \|<g_N>_ang\| / a0                    (the sphere's l=1 component: the environment)` | `SW01_envscalar_response.py:12` (canonical); computed `SW01b_envscalar_orthogonality.py:93–101` (eta_sun = 2.292 / 1.902, SW01b B1); per-object `SW03_dSph_eta_sequence.py:121` | **computed** | SW01b B1 PASS; SW03 A3 control PASS |
| E3 | `g_obs = g_free + [ (1 - S(eta)) + S(eta) * nu(Gamma/a0) ] * g_src` (canonical full form) | `SW06_conformal_mu.py:14` (docstring, canonical); older sourced-sector form `SW01_envscalar_response.py:13`, `SW02_helmholtz_kill.py:11`; implementations `SW04_conformal_efe.py:74–89` (`g_obs_aqual`, `g_obs_class`), `SW06_conformal_mu.py:76–77` (`g_obs_direct`) | **computed** | SW06 C round-trip: mu-inversion reproduces direct law to **2.22e-16** (`SW06_conformal_mu.out:24`) |
| E4 | `def S_env(eta, eta_c): return 1.0 / (1.0 + (eta / eta_c) ** 2)` | `SW01b_envscalar_orthogonality.py:62–63` (canonical def); identical `SW03_dSph_eta_sequence.py:77–78`, `SW08_preferred_frame.py:62–63` | **declared** (form) / computed (values) | S-form itself is an ANSATZ, kernel-level uncertainty — SW07 H5 KILLED the derivation claim (`SW07_eta_c_attack.out:31`); values computed in SW01b F gates, SW03 S_p, SW08 B3 (`S(eta_sun)`, dS/dln eta) |
| E5 | `mu_S  =  1 / [ 1 + S * ( nu_src - 1 ) ]        (nu_src = nu at the SOURCED y)` | `SW06_conformal_mu.py:19` (canonical); implementation `mu_S_of_yobs` `SW06_conformal_mu.py:79–89` | **computed** | SW06 B1 WELL-POSED (single-valued, monotone g→g_obs for every S) + round trip 2.22e-16 (`SW06_conformal_mu.out:19,24`) |
| E6 | `v^4 = S(eta)^2 G M_b a0          (THE eBTFR: slope exactly 4, zero point S^2)` | `SW04_conformal_efe.py:19` (canonical); P9 framing `SW05_kepler_freeze.py:34`; sympy check `SW04_conformal_efe.py:108`; Lean `SW06_lemmas.lean:13` (`theorem eBTFR`) | **computed** | SW04 A2 sympy PASS (slope 4 preserved, zero point S^2); P9 ladder `SW05_kepler_freeze.out:32,42` |
| E7 | `ETA_C = {"canonical": 0.2034, "alt": 0.1688}     # declared (SW01b B2)` | `SW03_dSph_eta_sequence.py:53` (frozen, "NOT tuned here"); original declaration `SW01b_envscalar_orthogonality.py:97–105` (derived from the Oort budget at eta_sun; SW01b B2); reused `SW07_eta_c_attack.py:52` | **DECLARED** — second measured constant | SW07: every derivation mechanism KILLED (1/6 checks PASS) → "eta_c is the law's SECOND MEASURED CONSTANT" (`SW07_eta_c_attack.out:50,60`) |
| E8 | `nu_rar(y) = 1.0 / (-math.expm1(-math.sqrt(y)))     # 1/(1-e^-sqrt(y))` | `SW06_conformal_mu.py:69–70` (canonical impl); also `SW01:63`, `SW02:52`, `SW03:74`, `SW04:56`, `SW05:65`, `SW08:59` | **DATA-SELECTED** (rung 2) | control value nu_RAR(2.5) − 1 = 0.259 (L264 record) reproduced in SW01/SW03/SW05 (±0.002 threshold) |
| E9 | `A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}` (a0, both footings) | `SW07_eta_c_attack.py:51`; used throughout SW01–SW08 | **measured** | kappa = 1/2 is the first measured constant (`SW07_eta_c_attack.out:50`) |

Certified algebra: `SW06_lemmas.lean` compiles **5 theorems** exit 0 — `eBTFR` (:13), `conformal_BR` (:29), `newton_limit` (:35), `mond_limit` (:39), `mu_S_equiv` (:45).

**DO NOT REDO any of the above.** Derivations of the S-family (E4) and eta_c (E7) are CLOSED by SW07 (killed 1/6, ansatz finding); the mu_S reformulation (E5) is CLOSED by SW06; the conformal cancellation is CLOSED by SW04/SW06-lean.

## 2. Frozen predictions P1–P9 — all computed, with .out citations

| P# | Description | Status | Value (from disk) | Source file:line |
|----|---|---|---|---|
| P1 | Gaia DR4 wide-binary gamma_v (dated 2026-12-02) | **computed** | class gamma_v = **1.00000 / 1.00016 / 1.00065 / 1.00236 / 1.00620 / 1.01012** at s = 1000/3000/5000/10^4/2×10^4/3×10^4 AU; clean-run solar value 1.0010; AQUAL runs 1.00003→1.17462; kill band 1.16–1.23 | `SW04_conformal_efe.out:44–53`; `SW05_kepler_freeze.out:7,42` |
| P2 | WB angular modulation A2 | **computed** | **A2 = 2.22e-16** (exactly zero by structure) vs AQUAL ~6% | `SW05_kepler_freeze.out:22,42` |
| P3 | Solar-System EFE quadrupole | **computed** | c2 = **−6.074e-14 a0** → tidal **3.38e-39 s^-2** vs ceiling 5.2e-27 | `SW01b_envscalar_orthogonality.out:48`; framing `SW05_kepler_freeze.py:19` |
| P4 | High-eta Keplerian floor (this class → Newtonian, a0_eff = S^2 a0) | **computed** | gaps **0.118 / 0.083 / 0.049 / 0.019 dex** at eta = 2/3/5/10 (vs 0.06-dex floor); distinctive window eta ~ 2–3.5 | `SW05_kepler_freeze.out:18,42` |
| P5 | dSph phantom elongation aligned with g_ext | **computed (structural)** — 0, direction-blind; no dedicated .out number (it is the P2 quadrature result restated) | 0 vs AQUAL nonzero (DE03/DE09) | `SW05_kepler_freeze.py:27`; `SW01b_...out:58` ("direction-blind at every order") |
| P6 | Ultra-faint dSphs at eta ≳ 1: near-Newton | **computed (analytic)** — S(1) = 0.040 → anomaly ≲ 2.4%; confirmatory per-object Jeans is OPEN | S(1) = 0.040 | `SW05_kepler_freeze.py:28`; per-object Jeans open: `SW00_INDEX.md:150`, `SW03_...out:50` |
| P7 | z ~ 2.5 BTFR zero point (flat a0, rung 8, ±0.13 dex) | **computed** | **0.00 dex** (a0(2.5)/a0(0) = 1 under w = −1) | `SW05_kepler_freeze.out:36,42` |
| P8 | DESI/Rubin R = a0(3)/a0(0) | **computed** | **R = 1.0000** (flat) vs registered DESI-DR2 band 0.775 [0.68, 0.88] | `SW05_kepler_freeze.out:38,42` |
| P9 | THE eBTFR zero-point ladder (a0_eff/a0 = S(eta)^2, slope exactly 4) | **computed** | field **0.996** → group **0.717** → cluster **0.336** | `SW05_kepler_freeze.out:32,42` |

Standing gates re-verified on disk in this swing: SW04 conformal per-object BR cancellation max |BR_class/BR_isolated − 1| = 2.22e-16 (`SW04_conformal_efe.out:26`); SW06 gate ratio both readings 152.1/220.3 (per-field) and 304.1/440.7 (dilution-inclusive), internal departure 0.2590, GATE_CONVENTION.md resolves the reading mixing (`SW06_conformal_mu.out:35–38`); SW07 **1/6** checks PASS, every mechanism KILLED (`SW07_eta_c_attack.out:59–60`); SW08 **10/11** PASS clean / **9/11** under MUTATE, alpha_2 ~ 0 structurally (doubly suppressed), c_S ≤ 4.23 (Nordtvedt) / ≤ 423 (LLR), C4 FAIL-as-finding (`SW08_preferred_frame.out:27,37,45–46`; 9/11 in `SW08_preferred_frame_MUTATE.out`). All match the on-record numbers exactly.

## 3. Concurrent-landing sweep: SW09*/PROOF* under fable_independent_2026/

**NONE FOUND** at audit time (find on name `SW09*` and `PROOF*`, case-sensitive, entire `fable_independent_2026/` tree; re-checked immediately before this write — zero hits both times). No SW09 file pre-existed, so this write is the sole new file. Caveat repeated: without git, "since 9fa915a01" is filename-glob evidence only.

## 4. OPEN-specs data presence (repo-wide, excluding nothing read-only)

- **Walker per-object Jeans likelihood data: ABSENT.** The per-object Jeans estimator (L263 E2) is the *registered open confirmatory step*: `SW00_INDEX.md:150` ("OPEN: G111 spec (>10 CPU-min), per-object Jeans, DE04's η≥2 sample count, ..."), `SW03_dSph_eta_sequence.py:116–118`, `SW03_dSph_eta_sequence.out:50`, `SW05_kepler_freeze.out:42`. The only "Walker" hits in the repo are: (a) bibliography citations in `deepseek_push/G070_data/dwarf_tab.tex:82` and `simon_ufds_v8.tex:536–537, 3777–3796` (Walker+2009 dSph compilation refs / membership probabilities — data tables, not likelihood functions); (b) `real_research/predictions/door2_dsph_ultraprecision.py:64` ("representative literature values (Walker+2009, Wolf+2010 era)" — quoted errors only); (c) 2D-likelihood machinery exists but for **clusters** (Wojtak-class: `deepseek_push/G206_wojtak_2d.out`, `G209_beta_profile.py:949–951`, `MNRAS_METHODS.md:81`), not per-object dSph Jeans. → No one has built the Walker per-object Jeans likelihood; the spec is genuinely open.
- **DE04 eta≥2 tables: ABSENT (and impossible from the audited sample).** DE04 itself EXISTS at repo-root `deepseek_push/` (NOT under fable_independent_2026/): `DE04_sample_audit.py`, `DE04_sample_audit.out`, `DE04_results.json`, indexed in `DE00_INDEX.md:12` — verdict "max eta_env = 0.019; median R_out/r_EFE = 0.256; THE PLAN'S PREMISE IS FALSE: zero SPARC galaxies at eta >= 0.3" (`DE_FINAL.md:15,93,121–123`). The open item "DE04's η≥2 sample count" (`SW05_kepler_freeze.out:42`, `SW00_INDEX.md:150`) is answered by that audit: the η≥2 sample is empty. The only η = 2.0 rows anywhere are the DE01 solver-table columns (`DE01b_cap_closed_form.py:65` ETAS list includes "2.0"; eta ≥ 1 scoring) — not a DE04 sample table. DE08 (`DE08_extreme_eta_lmc.py`) re-points the extreme-eta channel at the LMC.

## 5. eta_c consistency (SW01b vs SW03)

- **SW01b** (origin of the declaration): derived from the Oort budget at the true solar environment, `SW01b_envscalar_orthogonality.py:97–105`; `.out:15` prints **"eta_c = 0.2034 (canonical), 0.1688 (alt)"**; verdict line prints 3 s.f. "0.203/0.169 ... DECLARED" (`.out:58`).
- **SW03** (second determination): `SW03_dSph_eta_sequence.py:53` — `ETA_C = {"canonical": 0.2034, "alt": 0.1688}` "# declared (SW01b B2), NOT tuned here"; docstring :8 quotes "0.203 canonical / 0.169 alt, SW01b".
- **SW06/SW07** reuse the same constants (`SW06_conformal_mu.py:226–227`; `SW07_eta_c_attack.py:52`).
- **Window**: Oort ceiling "Oort demands eta_c <= 0.203" (`SW03:172`, `SW06:226`) and Fornax bound "Fornax tightens to <= 0.145" (`SW07:164–165,186`; SW03's implied-eta_c = **0.145** exactly, `SW03_...out:50`; `SW06:226–227`). So the operative window [0.145, 0.203] is on disk as stated.

**Verdict: CONSISTENT.** SW01b and SW03 declare the identical constants (0.2034 canonical / 0.1688 alt; SW07 :52, :31 confirms "1.9% from the declared 0.2034" and "5.7% from the alt-footing value 0.1688"). Two presentation notes, not inconsistencies: (i) the alt value appears on disk as **0.1688** (4 s.f.) — the 5-s.f. form 0.16879 does not appear verbatim anywhere in the lane; (ii) the Oort ceiling appears as **0.203** (3 s.f.) while the declared canonical is **0.2034** — the ceiling statements are the same quantity rounded, and SW07's SW01b-inherited OORT_WINDOW is (0.028, 0.203) with Fornax tightening the lower-naming bound to 0.145 (`SW07:57,164–165`). Anyone quoting the constants should use 0.2034/0.1688 as written in code.

## 6. Do-not-redo register (owner: glm_moe_push unless noted)

| Artifact | Landed result | Status |
|---|---|---|
| SW04 (conformal EFE) | per-object cancellation 2.22e-16; gamma_v curve 1.00000–1.01012; eBTFR slope-4 sympy | computed — CLOSED |
| SW05 (Kepler freeze) | A2 = 2.22e-16; P4 gaps 0.118/0.083 dex; P9 ladder 0.996/0.717/0.336; P7/P8 flat-a0 | computed — CLOSED |
| SW06 (+ lemmas.lean) | gate both readings 152.1/220.3 & 304.1/440.7; mu_S round trip 2.22e-16; mu_S single-valued; 5 Lean theorems exit 0 | computed — CLOSED |
| SW07 (eta_c attack) | 1/6; every eta_c mechanism killed; eta_c = SECOND MEASURED CONSTANT; window [0.028, 0.203], Fornax ≤ 0.145 | computed — CLOSED |
| SW08 (preferred frame) | 10/11 clean, 9/11 MUTATE; alpha_2 doubly suppressed ~0; c_S ≤ 4.23/423; C4 FAIL-as-finding | computed — CLOSED |
| SW01b | eta_c declaration (0.2034/0.1688); eta_sun 2.292/1.902; Gamma/eta quadrature; P3 quadrupole | computed+declared — CLOSED |
| SW02 (Helmholtz kill), SW03 (dSph eta-sequence) | Oort 130x over-budget kill; dSph residual −0.207 dex, implied eta_c = 0.145, NOT-DISTINCTIVE gate open | computed |
| SW01 | gamma_v = 1.0010 standing; L264/L263/L265 kill citations | computed |

**Still OPEN** (do not mark done without new work): per-object Jeans (L263 E2); G111 spec; DE04's η≥2 sample count (answered as empty by deepseek_push — cite it, don't recompute); covariant action / ghost theorem / alpha_2 kill gates; DR4 falsifier dated 2026-12-02 (gamma_v inside 1.16–1.23 or > 1.05 kills the class).

*Write discipline: this is the only file created in this swing; nothing else modified; no git commands run.*
