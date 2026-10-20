# CFG689 addendum A2 — the CMB acoustic angle θ*, two more supernova sets, and the link to the z ≈ 2.5 framework-vs-ΛCDM test (FROZEN before any CFG689 run or number)

Owner, 2026-10-20: "write CFG689 addendum A2 (theta* native constraint, DES-SN5YR and Union3 brackets, P6 linking the native a0
band to the z~2.5 framework-vs-LCDM decision rule), frozen and committed alone before any run; criteria and code only while NC2x is
live."
Base 1c237145d and A1 0db6da294 have never run: the waiter blocks until chain7/NC2x finishes. A2 adds to them and changes nothing
already frozen.

## A2.0 Why
- BAO alone cannot separate the framework from ΛCDM. Both share the same background ingredients (CFG654 principle; CFG253 ≤ 3%).
- Its most useful role is to fix the framework's own a0(z) prediction, natively.
- **θ\***
  - What it is: the CMB acoustic angle, θ* = r_s(z*)/D_M(z*).
  - Why it is native: r_s(z*) is pre-switch physics, and D_M(z*) is the same distance integral the model already computes. CFG654
    used θ* this way to set h.
  - What it adds: an absolute distance at z* ≈ 1090. That sharpens both the constant-dark-energy test (P2) and the curvature test
    (P0).
- **SN swaps:** DES-SN5YR (Dovekie) and Union3 test whether a P2 result depends on the supernova set.
- **P6** carries the native band into the record's framework-vs-ΛCDM decision rule:
  - record: prep_2026/a0z_crossscale/FRAMEWORK_VS_LCDM_TEST_2026.md, commit 9d40e9c15c;
  - the rule: one clean deep-MOND point at z ≈ 2.5 with σ ≤ 0.13 dex decides FLAT vs ΛCDM-native at 20:1.

## A2.1 θ* (native)
- **Datum:** 100θ* = 1.04109 ± 0.00030. Record value: Planck 2018 VI, TT,TE,EE+lowE column (`cfg654_ics.py` PROVENANCE). No other
  CMB distance quantity is used (no R, no l_A, no lensing). The θ*–ω covariance is ignored (declared; the θ* error is 0.03%).
- **Model:**
  - 100θ*_model = 100 r_s(z*; ω_b, ω_c) / D_M(z*).
  - r_s(z*) and z* come from CAMB 1.6.6 (`rstar`, `zstar`; base settings, m_ν = 0). r_s uses the same ±2σ power-law emulator form
    as r_d.
  - z* is held at its CAMB value at the mode's ω centres. Its shift over ±2σ moves D_M(z*) by < 1e-5, which is checked as K9.
  - χ(z*) = χ(2.5) + ∫ c dz/H over 2.5 → z*, integrated in ln(1+z) with a 4001-point Simpson rule.
  - H uses the same ω_m, ω_r, ω_k and w ≡ w(2.33) beyond the last node. D_M(z*) uses the same sinh/sin curvature form.
- **χ² term:** ((100θ*_model − 1.04109)/0.00030)².
- **Not combined with B2** (massive ν): that mode counts the neutrino as matter, which is wrong at z ≳ 100.
- **K8:** at the A1 pair, flat, with w ≡ 0.6777² − ω_m − ω_r, 100θ*_model = 1.04109 ± 0.00005. CFG654 A1 solved h = 0.67770 from θ*
  with CAMB, so this independently checks the long integral.
- **K9:** the r_s(z*) emulator matches CAMB at the four ±2σ corners to ≤ 2e-4, and z* varies by < 1 over those corners.

## A2.2 SN sets (inputs on disk since CFG684, `_external_data/cfg684_inputs/`, sha256 in its READMEs)
- **DES-SN5YR Dovekie:** Hubble diagram plus the STAT+SYS inverse covariance. Loader verbatim from `cfg684_robust.py`.
- **Union3:** spline-node μ plus weight matrix. Loader verbatim from `cfg684_robust.py`.
- In both, M is marginalised analytically (shape only), as for Pantheon+.

## A2.3 New modes (reported beside the primary; same P0–P3 classes, K4 per run)
| mode | curvature | SN | θ* |
|---|---|---|---|
| T | free | Pantheon+ | yes |
| TF | flat | Pantheon+ | yes |
| TD5F | flat | DES-SN5YR | yes |
| TU3F | flat | Union3 | yes |
| D5 | free | DES-SN5YR | no |
| U3 | free | Union3 | no |

**P2 rule with θ\* (no cherry-picking of the SN set):**
- "EVOLVING DE REQUIRED with θ*" only if TF, TD5F and TU3F all reach ≥ 3σ.
- "SN-DEPENDENT" if only some do. Otherwise the weakest class among the three is reported.
- The node test has 5 dof. DESI's w0–wa test has 2, so the same Δχ² reads as a lower σ here. That is disclosed, not corrected.

**What any P2 outcome means:**
- It can reject a constant dark energy (the Λ of ΛCDM). It cannot reject cold dark matter, because ΛCDM with evolving dark energy
  survives.
- It is never evidence for the framework over ΛCDM. Its framework meaning is only the a0(z) prediction carried into P6.

## A2.4 P6: native a0(z) vs ΛCDM's emergent acceleration scale (the decision link)
At z_t ∈ {2.0, 2.5, 3.25}, from each mode's posterior (headline modes: primary and T):
- **Framework:** tracking a0(z_t)/a0(0) = √X(z_t), with median and 16/84%.
  - z_t = 2.0 interpolates between the 1.5 and 2.33 nodes.
  - z_t = 2.5 and 3.25 are EXTRAPOLATIONS: they assume w ≡ w(2.33) beyond the last BAO node. This is flagged on every line.
- **ΛCDM (the alternative being tested, ΛCDM's own claim, not a yardstick):** the record's emergent-scale ratios (same file):

  | law | z = 2.0 | z = 2.5 | z = 3.25 |
  |---|---|---|---|
  | DM14 (primary) | 1.756 | 2.126 | 2.823 |
  | D08 | 2.284 | 2.802 | 3.667 |
  | MAG | 2.748 | 3.166 | 3.785 |

- **Gaps** (framework below ΛCDM):
  - Δ_close = log10 L − log10 √X₈₄ (closest edges, conservative, as CFG683);
  - Δ_med = log10 L − log10 √X₅₀.
- **Required error for 20:1**, using the record's rule ln B = Δ²/(2σ²): e_20 = Δ/√(2 ln 20). Reported for both Δ_close and Δ_med.
- **Class at z_t = 2.5, DM14, Δ_close:**
  - TARGET HOLDS if e_20 ≥ 0.13 dex (as reachable as the record's FLAT target);
  - TARGET TIGHTER if 0.10 ≤ e_20 < 0.13;
  - TARGET HARDER if e_20 < 0.10;
  - NO SEPARATION if Δ_close ≤ 0.
- **Reported only (the record calls it too coarse; no verdict):** the record's one clean point, Big Wheel (z = 3.25, +0.06 ± 0.22
  dex, N = 1). log10 B (native tracking / DM14) = [(x − log10 L)² − (x − log10 √X₅₀)²] / (2 ln 10 · (0.22² + s_F²)), with
  s_F = log10 √X₈₄ − log10 √X₅₀.
- **Wording, frozen:** P6 names the measurement that decides; it is not a result. Present data still do not favour the framework
  over ΛCDM.

## A2.5 Checks, MUTATE, order
- K8 and K9 run in mode T.
- MUTATE M4: data replaced by the noiseless flat constant-w truth (as M1), including a θ* datum computed from that truth, run in TF
  configuration. Pass: P2 Δχ² ≤ 0.1 and 100θ* recovered to ≤ 1e-5.
- Waiter order: after A1's list, append T, TF, TD5F, TU3F, D5, U3, M4. P5 stays last.
- The verdict lines of base, A1 and A2 are all reported. A2 adds:
  "θ*: P0 <class>, P2 <class or SN-DEPENDENT>; P6 at z 2.5 (DM14): e_20 = …, <class>; K8/K9; M4".

κ fitted; cold energy mass required; not theory closed; nothing here says the data favour the framework over ΛCDM.
