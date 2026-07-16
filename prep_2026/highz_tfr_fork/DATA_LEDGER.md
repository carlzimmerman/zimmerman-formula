# DATA_LEDGER — Published high-z Tully–Fisher zero-points for the a0(z) footing fork (Lane D)

**Assembled 2026-07-16.** Companion files: `data_ledger.csv` (machine-readable, one row per
measurement), `ledger_fork_context.py` (footing-locked fork predictions per z; reproduces the
banked anchors of `prep_2026/btfr_forecast_audit/btfr_forecast_check.py` before printing anything).

**Convention used throughout:** `Δb` = TFR zero-point offset **along the mass axis** at fixed
velocity, relative to the quoted local (z≈0) reference relation, in dex. Negative = *less* mass at
fixed velocity at high z. Deep-MOND fork mapping: `Δb_bTFR = −log10(a0(z)/a0(0))`
(velocity-axis `dlogV = −Δb/slope ≈ −Δb/4`; the banked z=3 numbers −0.033/+0.164 dex are
velocity-axis).

---

## 1. The ledger

### z ≈ 0.9–1 bin

| # | Study | Survey / N | Relation | Δb (dex) | stat | Local ref (slope) | Velocity / pressure support |
|---|-------|-----------|----------|----------|------|-------------------|------------------------------|
| 1 | Übler et al. 2017, ApJ 842, 121 (arXiv:1703.04321) | KMOS3D, 65 @ z≈0.9 | sTFR | **−0.44** | ±0.04 | Reyes+11 (3.60) | v_circ,max (≈2.2R_d), σ0-corrected: v_circ²=v_rot²+2σ0²(r/R_d) |
| 2 | Übler et al. 2017 | KMOS3D, 65 @ z≈0.9 | bTFR | **−0.44** | ±0.04 | Lelli+16b (3.75) | same |
| 3 | Tiley et al. 2016, MNRAS 460, 103 | KROSS, 56 (V80/σ>3) @ z≈0.9 | sTFR | **−0.41** | ±0.08 | local M*-TFR (their fit) | v80, **no** pressure-support term (strict rotators instead); K-band TFR: **no evolution** |
| 4 | Tiley et al. 2019, MNRAS 482, 2166 (arXiv:1810.07202) | KROSS vs **quality-matched** SAMI z≈0 | sTFR | **−0.09** (disky) / **+0.02** (v/σ>1) | ±0.06 | matched SAMI (identical pipeline) | v2.2 (1.3Re), beam-smearing corr., **no** pressure-support term |
| 5 | Tiley et al. 2019 | same | K-band TFR | −0.08 mag | ±0.09 mag | matched SAMI | same |
| 6 | Pelliccia et al. 2017, A&A 599, A25 | HR-COSMOS @ z≈0.9 | sTFR | ≈0 ("mild if any", per Jeanneau+26 §1) | — | — | slit spectroscopy, v2.2 |
| 7 | Jeanneau et al. 2026 (MUSE-DARK II), A&A aa59953-26 (arXiv:2603.28856) | 95 lensed SFGs, 0.56≤z≤1.37, M*=10^8.1–10.3 | sTFR | **−0.42** | ±0.05 | Reyes+11 (3.70 form) | v_c(1.8Re), 3D GalPaK3D w/ lensing; Dalcanton-Stilp pressure-support corr. |
| 8 | Jeanneau et al. 2026 | same | **bTFR** | **0.00** | ±0.06 | **Lelli+19 (3.14)** | v_c(2Re), same |
| 9 | Mancera Piña et al. 2026, A&A 705, A180 (arXiv:2511.08685) | 43 KROSS+KMOS3D discs @ z=0.9, JWST/HST imaging | sTFR | **≈ +0.1** (intercept @150 km/s) + slope 3.82 vs local 5.21 (~2σ shallower) | ±0.07 | Marasco+25 (SPARC HI) | V_circ,flat, asymmetric-drift corrected |

### z ≈ 2–2.5 bin

| # | Study | Survey / N | Relation | Δb (dex) | stat | Local ref (slope) | Velocity / pressure support |
|---|-------|-----------|----------|----------|------|-------------------|------------------------------|
| 10 | Übler et al. 2017 | KMOS3D, 46 @ z≈2.3 | sTFR | **−0.42** | ±0.05 | Reyes+11 (3.60) | as rows 1–2 |
| 11 | Übler et al. 2017 | KMOS3D, 46 @ z≈2.3 | bTFR | **−0.27** | ±0.05 | Lelli+16b (3.75) | as rows 1–2 |
| 12 | Straatman et al. 2017, ApJ 839, 57 (arXiv:1703.00016) | ZFIRE @ z≈2.2 | sTFR | **−0.25** | ±0.16 | z=0 obs (fixed inverse slope 0.29) | v2.2-type |
| 13 | Amvrosiadis et al. 2025, MNRAS (arXiv:2312.08959) | 12 ALMA CO disc DSFGs, z=1.2–4.7 (median≈2.4) | sTFR | **−0.53** | ±0.29 | Reyes+11 (3.60) | V_circ(2Re), visibility-space 3D |
| 14 | Amvrosiadis et al. 2025 | same | **bTFR** | **−0.26** | ±0.19 | Lelli+16a (3.75) | same; α_CO=0.92±0.36 |
| 15 | Sharma et al. 2024, A&A (arXiv:2406.08934) | 263 KROSS+KMOS3D+KGES, 0.6≤z≤2.5, 3DBarolo | sTFR+bTFR | "subtle deviation" (free slope+ZP; sTFR α=3.03±0.25, bTFR α=3.21±0.28) | — | Lapi+18 | v_c(≈5R_d), pressure-**gradient** corr. (not Dalcanton-Stilp) |
| 16 | Nestor Shachar et al. 2023, ApJ 944, 78 (RC100) + McGaugh 2025 (tritonstation blog, informal) | 100 RCs, z=0.6–2.5 | bTFR (re-binned) | "no clear evolution" | — | Lelli+19 | outer-RC v; pressure-support corrected (Genzel-group) |

### z ≳ 3.5 bin (JWST/ALMA era)

| # | Study | Survey / N | Relation | Δb (dex) | stat | Local ref (slope) | Velocity / pressure support |
|---|-------|-----------|----------|----------|------|-------------------|------------------------------|
| 17 | Turner et al. 2017, MNRAS 471, 1280 (KDS, arXiv:1704.06263) | KDS @ z≈3.5; only 34±8% rotation-dominated | sTFR | ≈**−0.4** family once v_tot=√(v²+4σ²) used (their reconciliation of ALL literature at z~1 gives ≃−0.4) | — | Reyes+11 | v_tot (pressure folded into the velocity) |
| 18 | Danhaive et al. 2025 MNRAS 543, 3249 + Danhaive et al. 2026 MNRAS 546 (geko, arXiv:2510.14779) | 163 Hα emitters (FRESCO/CONGRESS+JADES), z≈4–6, JWST NIRCam grism | sTFR | **≈−1.3 vs Übler cosmic-noon** (≈−1.7 vs local), fixed slope 3.60, b=0.76±0.07 at their pivot | ±0.07 (fit) | Übler+17 chain | v_circ(Re), v_circ²=v_rot²+2(r/r_s)σ0²; **σ_int=0.49±0.06** (2× cosmic noon); majority dispersion-dominated (36–41% rot-supported in parent) |
| 19 | Übler et al. 2024 (GA-NIFS), de Graaff et al. 2024 A&A 684 (JADES/NIRSpec z≳6 M_dyn), Nelson et al. 2024 ApJ 976 L27 (FRESCO z=5.4), Rizzo et al. 2020/2021, REBELS-25 (Rowland et al. 2024, z=7.31), Neeleman et al. 2020 (z=4.26) | individual/small-N dynamically cold discs | — | no population TFR zero-point; single objects roughly consistent with high-z relations | — | — | context rows only |

**Also in the Jeanneau+26 Fig. 8 compilation** (all sTFR, Turner+17 reprocessing, v_tot convention,
sitting in the −0.2 to −0.6 band at their respective z): Epinat+12 (MASSIV z≈1.2), Simons+16
(SIGMA z≈1.5, 2.3), Cresci+09 (SINS z≈2), Girard+20 (KLASS z≈1.3), Abril-Melgarejo+21 & Mercier+22
(MAGIC z≈0.7), Pelliccia+19 (ORELSE z≈0.9).

**Excluded as non-usable:** Marongwe & Kauffman (arXiv:2511.20188, "evolving BTFR universal law")
— theory-driven fit, no independent data, fringe provenance. Flynn (arXiv:2605.25339, ALPINE [CII]
corpus) — nonstandard "omega kinematic correction," no TFR zero-point, fringe provenance.

---

## 2. Systematics carried per row (authors' own flags)

- **Übler+17**: stellar mass ±0.15 dex (BC03+Chabrier SED), gas ±0.20 dex (Tacconi+17/18 *scaling
  relations*, not measured); authors state errors "may underestimate the systematic uncertainties"
  and that selection substantially moves zero-points. Their v/σ cut is the strictest
  (v_rot,max/σ0>√4.4). **Local-comparison mismatch**: Reyes+11/Lelli+16 use v2.2/v_flat *without*
  the 2σ0² pressure term — the cross-convention comparison itself is worth ~0.1–0.2 dex.
- **Tiley+19 (the counter-claim)**: degrading SAMI z≈0 to KROSS quality moves the *local* TFR by
  **−0.50±0.10 mag** (K-band) and changes its slope from −8.3 to −6.6 — i.e. **method+selection
  artifacts are as large as or larger than any claimed evolution**. Matched-analysis evolution:
  ≈0. Their velocities carry **no pressure-support correction**; Turner+17/Übler+17 argue that is
  precisely why they see no evolution (rotation-only velocities of turbulent discs are biased low
  at z≈1, cancelling the mass offset). This is THE methodological fork in the literature:
  **evolution (−0.4 dex) appears when pressure support is added to v; disappears when strict
  rotators are compared like-for-like without it** (Tiley+16 row 3, with strict v/σ>3 and no σ
  term, is the counterexample: −0.41 even without the correction — selection again).
- **Jeanneau+26**: M* ±0.15 dex (SED/magnification), M_bar ±0.2 dex; **bTFR gas masses are NOT
  measured** — molecular from Tacconi+20 scaling, atomic from the NeutralUniverseMachine model
  (0.8 dex scatter in the HI-relation) — the bTFR row is *model-mediated*; robustness scan
  (velocity definition, v/σ cut, slope) moves Δb by ~1σ (±0.05–0.06); local bTFR reference
  zero-point itself ±0.16 (Lelli+19). Cluster lens-model spread tested, small.
- **Mancera Piña+26**: opposite-sign result driven mainly by the **choice of local reference**
  (Marasco+25 bends/steepens at low mass — Jeanneau Appendix D); asymmetric-drift corrections
  0.02–0.09 dex in log V; Hα-as-tracer reliability flagged by the authors themselves.
- **Amvrosiadis+25**: α_CO=0.92±0.36 (→±0.17 dex on gas-dominated M_bar), magphys stellar masses
  of dusty starbursts (AGN contamination flagged), 12-object sample at the extreme high-mass end,
  merger/disc misclassification at ~1″ resolution.
- **Danhaive+25/26**: 2D grism (not 3D) kinematics; majority of parent sample
  dispersion-dominated; non-equilibrium/outflow contamination flagged by authors; σ_int=0.49 dex;
  inclination prior q0=0.2; **stellar TFR only** — converting to baryonic with their own
  ⟨f_gas⟩=0.77 would move Δb by +log10(1/(1−0.77)) ≈ +0.64 dex with enormous (±0.3–0.5) systematic.
- **Cross-cutting**: Tolman dimming selects big/bright discs at high z; stellar-mass systematics
  across SED codes ±0.2 dex (Tiley+19's uniform adoption); slope-vs-zero-point covariance when
  slopes are left free (Sharma+24's "factor 2" between orthogonal and vertical likelihoods).

## 3. The disagreements, stated plainly

1. **z≈1 stellar TFR**: Übler+17 (−0.44±0.04), Tiley+16 (−0.41±0.08) and Jeanneau+26 (−0.42±0.05)
   vs Tiley+19 (≈0 when matched) vs Mancera Piña+26 (**+0.1, opposite sign**, and slope evolution
   instead). Spread of claims at the SAME redshift: **~0.5 dex**, i.e. 8–10× the quoted
   statistical errors. Drivers identified by the authors themselves: pressure-support convention,
   selection (v/σ cut), data-quality matching, and choice of local reference.
2. **z≈1 baryonic TFR**: Übler+17 (−0.44±0.04) vs Jeanneau+26 (**0.00±0.06**). Same nominal
   observable, 6σ apart on stat errors — the difference is gas-fraction prescriptions + velocity
   convention + sample mass range. Both used scaling-relation gas.
3. **z≈2.3 baryonic TFR**: Übler+17 (−0.27±0.05) and Amvrosiadis+25 (−0.26±0.19) **agree** (same
   local refs, same fixed slopes) — the one genuinely reproduced high-z bTFR number in hand, but
   both are scaling-relation/α_CO-mediated and both samples sit at g_bar ≫ a0.
4. **Direction of sTFR evolution is unanimous except Mancera Piña+26** (lower M* at fixed v at
   higher z); amplitude is not.

## 4. Fork context (from `ledger_fork_context.py`, footing-locked; mass-axis dex)

| z | canonical (pure Λ) | canonical (DESI CPL) | ALT (ρ_tot/cH0) | ΛCDM halo term | typ. g_bar/a0 | dilution | ALT diluted |
|-----|------|--------|--------|--------|-----|------|--------|
| 0.9 | 0.000 | −0.009 | −0.229 | −0.316 | 0.3–1.7 | 0.23–0.63 | −0.05…−0.14 |
| 2.2–2.4 | 0.000 | +0.08…+0.09 | −0.52…−0.55 | −0.63…−0.67 | 2.3–6.4 | 0.07–0.18 | −0.04…−0.10 |
| 3.5 | 0.000 | +0.164 | −0.731 | −0.850 | ~1.0 | 0.34 | −0.25 |
| 5.0 | 0.000 | +0.247 | −0.917 | −1.036 | ~4.5 | 0.10 | −0.09 |

Three honesty results that fall straight out of the table:

- **(a) The ALT footing is ΛCDM-degenerate at every z in this observable.** ALT predicts
  Δb=−log10 E(z); the standard halo-scaling drift is −log10[E(z)√(Δc ratio)] — the two track
  within ~0.1 dex from z=0.9 to z=5. A measured negative drift can never, by itself, pick ALT-MI
  over ΛCDM disk evolution. The degeneracy-breaking observable is a **flat** bTFR zero-point
  (canonical) vs a falling one (ALT *and* ΛCDM-without-gas-compensation) — but ΛCDM can also
  produce a flat bTFR via rising gas fractions (Jeanneau+26's own interpretation of their
  0.00±0.06). So: **flat bTFR = canonical-compatible but ΛCDM-absorbable; falling bTFR =
  ALT-compatible but ΛCDM-degenerate.** The fork is only *internally* decisive (canonical vs ALT),
  exactly as banked; it is not an MI-vs-ΛCDM discriminator at any z probed.
- **(b) Acceleration dilution guts most of the in-hand lever.** The deep-MOND mapping
  Δb=−log10(a0 ratio) assumes g_bar≪a0. Every published high-z TFR sample sits at
  g_bar≈(0.3–6)a0 at the velocity-measurement radius; the framework's own ν gives
  dlnM/dln a0=−x/(2+x), so the usable signal is 7–63% of deep-MOND. The **only** sample near the
  a0 regime is Jeanneau+26 (low-mass lensed, g_bar≈0.3–1 a0, dilution ≈0.5–0.6).
- **(c) In the framework's own Newtonian limit the zero-point tracks SIZE, not a0.** At g≫a0,
  M_bar=v²R/G, so compact high-z discs are predicted to sit **below** the local relation by
  ≈log10(R(z)/R(0)) ≈ −0.2 to −0.3 dex at z≈2 with *constant* a0 — the observed −0.27 at z≈2.3 is
  therefore not evidence against the canonical footing either. High-acceleration rows cannot
  falsify canonical.

## 5. Verdict per bin: what is actually usable

- **z≈0.9–1 (usable, the best bin).** Jeanneau+26 bTFR Δb=0.00±0.06(stat) is the cleanest
  baryonic zero-point in hand: pressure-support corrected, 3D-forward-modelled, lensed down to
  M*=10^8.1 (partially into the a0 regime, dilution ~0.5). Honest total band after adding gas-model
  (±0.2), local-reference (±0.16) and convention (±0.06) terms in quadrature: **0.00±0.27 dex**.
  Fork separation at this z after dilution: canonical 0.000 vs ALT −0.05…−0.14. **Verdict:
  UNDERPOWERED — leaning canonical in sign, but the honest band is 2–5× the diluted fork
  separation.** (On stat errors alone it would disfavor the undiluted ALT −0.23 at ~4σ; the
  dilution and gas-model systematics forbid that claim.)
- **z≈2.2–2.4 (contested, conditionally usable).** Two concordant bTFR numbers: −0.27±0.05 (Übler)
  and −0.26±0.19 (Amvrosiadis); honest band with M/L+gas+convention systematics: **−0.27±0.30**.
  But these samples sit at g_bar≈(2–6)a0 → diluted fork separation ≤0.1–0.15 dex, and the
  framework's own size-evolution term (−0.2…−0.3) plus the ΛCDM halo term (−0.65) both live in
  the same direction as the measurement. **Verdict: WASH for the fork; the −0.27 is
  ΛCDM/size-degenerate, not an a0 signal in either direction.**
- **z≳3.5 (not usable yet).** Danhaive+26 is stellar-only, dispersion-dominated, σ_int=0.49,
  grism-2D; the −1.3 dex offset is dominated by gas+DM/dynamical-state evolution, not a
  zero-point in the fork's sense. Baryonic conversion via ⟨f_gas⟩=0.77 carries ±0.3–0.5 sys.
  Amvrosiadis's z>3 objects are 3 extreme DSFGs at g≈6a0. **Verdict: no in-hand z≳3 bTFR
  zero-point at fork-relevant accelerations exists.** The banked DESI/JWST forecast (N≈15–40
  clean rotators at z≈2.5–3.5 for the velocity-axis signal, low-acceleration selection) remains
  the requirement, not a formality.

**Bottom line for the fork:** in-hand high-z TFR data are **canonical-sign-compatible and
ALT-sign-compatible at once** because (i) the only low-acceleration bin (z≈1) reads 0.00±0.27
against a diluted separation of ≤0.14, and (ii) every negative-drift measurement is
ΛCDM/size-degenerate. Nothing here moves the banked fork; nothing here falsifies either footing.
The one concrete in-hand lever worth pushing (Lane-E material): re-fit the Jeanneau+26 95-galaxy
sample restricted to its lowest-acceleration third (g_bar<0.5a0, dilution>0.6), where the ALT
prediction (−0.15…−0.2) would clear their stat error — if the sub-sample zero-point stays at
0.00±0.10, that is a real (if modest) ALT-side constraint from published data.

## 6. Citations (rows)

- Übler H. et al. 2017, ApJ 842, 121 — arXiv:1703.04321
- Tiley A. L. et al. 2016, MNRAS 460, 103 — arXiv:1604.06103
- Tiley A. L. et al. 2019, MNRAS 482, 2166 — arXiv:1810.07202
- Pelliccia D. et al. 2017, A&A 599, A25 — arXiv:1606.01934
- Turner O. J. et al. 2017, MNRAS 471, 1280 — arXiv:1704.06263
- Straatman C. M. S. et al. 2017, ApJ 839, 57 — arXiv:1703.00016
- Sharma G. et al. 2024, A&A — arXiv:2406.08934
- Nestor Shachar A. et al. 2023, ApJ 944, 78 (RC100); McGaugh S., tritonstation.com 2025-02-10 (informal re-binning)
- Amvrosiadis A. et al. 2025, MNRAS — arXiv:2312.08959
- Jeanneau A. et al. 2026, A&A (MUSE-DARK II) — arXiv:2603.28856
- Mancera Piña P. E. et al. 2026, A&A 705, A180 — arXiv:2511.08685
- Danhaive A. L. et al. 2025, MNRAS 543, 3249 — arXiv:2503.21863; Danhaive A. L. et al. 2026, MNRAS 546 — arXiv:2510.14779
- Local references: Reyes+11 MNRAS 417, 2347; Lelli+16a AJ 152, 157; Lelli+16b ApJ 816, L14; Lelli+19 MNRAS 484, 3267; Marasco+25 A&A 695, L23.
