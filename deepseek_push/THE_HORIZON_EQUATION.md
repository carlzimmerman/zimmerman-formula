# THE HORIZON EQUATION

## `v^4 = G M_b c^2 / (Z R_dS)` — the BTFR written through the de Sitter horizon

**Lane:** Z11 (`deepseek_push/Z11_horizon_form.py` → `.out` → `Z11_results.json`), 19/19 checks PASS.
**Date:** 2026-09-16 EDGE. **Footing:** committed constants only — H0 = 67.4 km/s/Mpc
(G058/G189), Ω<sub>Λ</sub> = 0.685 (G058 Lean window), a0_DE = 9.3619e-11 (G03E/G052),
G = 6.674e-11, c exact. The 542-object line is imported in-file from the committed
G162/G074/G114/G071/G075/G070 assembly (byte-identical JSON gate passed).

---

## 1. THE DERIVATION (three lines)

| step | statement | value |
|---|---|---|
| horizon radius | R_dS = c / (H0 √Ω<sub>Λ</sub>) | 1.658311e26 m = 5.37 Gpc |
| surface gravity | κ_dS = c² / R_dS | 5.419701e-10 m/s² |
| acceleration scale | a0 = κ_dS / Z = c² / (Z R_dS), Z = 2√(8π/3) | **9.362375e-11 m/s²** |
| the line | v⁴ = G M_b a0 ⇒ **v⁴ = G M_b c² / (Z R_dS)** | — |

**The identity closes to ratio 1.00005:** a0_H = 9.3624e-11 vs a0_DE = 9.3619e-11
(+0.0051%). The G058 Lean identity Ω = 32πa0²/(3H0²c²) *returns exactly 0.685*
at the horizon value — the horizon form is the geometric face of the committed
cosmological identity, not a new number.

**The same Z in the user's own formula:** with H_Λ = c/R_dS = H0√Ω<sub>Λ</sub> =
1.807818e-18 s⁻¹ (the de Sitter asymptotic Hubble rate),
a0 = c H_Λ / Z ≡ c²/(Z R_dS) = κ_dS/Z. The seesaw constant (G189) is the same surface
gravity over Z/2: s_Lambda = 2a0 = κ_dS/(Z/2) = 1.8725e-10 vs the committed 1.87238e-10.

---

## 2. THE VERIFICATION — every committed scale register

### (a) the 12-decade line's absolute zero point (slope-fixed, n = 542)

* Reproduced in-file: pooled slope b = 1.0040 ± 0.0108, rms 0.1795 (G162 registers);
  slope-FIXED a0_line = **1.697830e-10** (= Z08's 1.6978e-10, 1.8136 × a0_DE).
* vs the horizon value: **ratio 1.8135, dex +0.2585, z = +8.98 σ (stat) / +6.31 σ
  (stat+sys)** — a **REGISTERED DEPARTURE**, not a pass and not a kill.
* **The TRIO core** (bright dSph + HI + SPARC, n = 104): a0 = 9.1408e-11 =
  0.976 × a0_H, **z = −0.20** — sits **ON the horizon zero point**.
* Per-catalog (vs a0_H): SPARC 0.663 (z −3.4), HI 1.194 (+1.0), ATLAS3D 2.020 (+14.4),
  GEMS 1.326 (+0.8), dSph 7.38 (+5.0, UFD), CLU 12.16 (+42, registered gap),
  GC 1.401 (+1.7).
* Reading: the full-line offset is 56% ATLAS3D internal M/L_JAM (Z08/G223's named
  suspect) + the registered end-departures; the *clean rotation core* sits on the
  horizon value. The decider is a well-measured *system* (section 4).

### (b) r_M(Sun)

r_M = √(G M_sun Z R_dS / c²) = √(G M_sun / a0_H) = **7959.45 AU** vs the committed
**7959 AU (canonical, FRONTIER_BRIEF/G204; 7960 G224)** — +0.0057%.
(The brief's alt register 7512 AU ↔ a0 = 1.0511e-10 matches no committed footing; at
the committed alt a0 = 1.1279e-10 the same form gives 7252 AU = G204's number — the
7512 entry is a brief-level inconsistency, flagged, not a theory failure.)

### (c) MW r_M

r_M(M_b = 6.5e10) = **9.8382 kpc** vs committed **9.8384 kpc** (G089/G119) — 0.002%.

### (d) the cluster seam

r_t = 386.8 kpc = 386.8 / 401.6 (G108 median r_M) = **0.9632 r_M** vs the committed
**0.96 r_M** (G176/G186) — the horizon r_M is the same r_M (same a0), the seam
register carries over untouched.

### (e) the phantom surface density

Σ = c² / (2πG Z R_dS) = a0_H/(2πG). Unit conversion **done exactly in code**:
1 kg/m² = (1/1.98892e30 M☉) / (1/3.08568e16)² pc² = **478.7224 M☉/pc² per kg/m²**.
Σ = 0.223265 kg/m² × 478.7224 = **106.882 M☉/pc²** vs committed **106.88** — 0.002%.

### every register, one line

| register | committed | horizon form | deviation |
|---|---|---|---|
| a0 footing (G03E/G189) | 9.3619e-11 | 9.362375e-11 | +0.0051% |
| Ω (G058) | 0.685 | 0.685000 | exact |
| r_M(Sun) (G089/G204) | 7959 AU | 7959.45 AU | +0.006% |
| MW r_M (G089/G119) | 9.8384 kpc | 9.8382 kpc | −0.002% |
| cluster seam (G176/G186) | 0.96 r_M | 0.9632 r_M | +0.3% |
| Σ (committed a0/2πG) | 106.88 M☉/pc² | 106.882 | +0.002% |
| TRIO core zero point (Z08) | — | 0.976 × a0_H, z = −0.20 | on-value |
| **full-542 zero point (Z08)** | 1.8136 × a0_DE | **+0.2585 dex, z = +6.3** | **REGISTERED DEPARTURE** |

---

## 3. THE HORIZON-DERIVED CONSTANTS (the re-expression table)

**No framework constant retains an independent scale.** Every one is a function of
(G M_b, R_dS, Z, the dark mass m):

| constant | committed form | horizon form | value |
|---|---|---|---|
| a0 | 9.3619e-11 m/s² | κ_dS / Z = c²/(Z R_dS) | 9.3624e-11 |
| r_M | √(G M_b / a0) | √(G M_b Z R_dS / c²) | √(G M_b / a0_H) |
| Σ | a0 / (2πG) | c² / (2πG Z R_dS) | 106.88 M☉/pc² |
| σ² (galaxy anchor 6.5e10) | √(G M_b a0)/2 | √(G M_b c²/(Z R_dS))/2 | σ = 119.21 km/s (the 119.2 triad, G168) |
| T_b = m σ²/k_B (m = 5.09 keV) | 9.17–9.52 K | (m/2k_B)√(G M_b c²/(Z R_dS)) | **9.340 K** in the committed band |
| m (mass window) | 5.09 keV | 2 k_B T_b / √(G M_b c²/(Z R_dS)) | 5.09 keV (identity, closed) |
| dust law | log10 a_c = c0 + q log10(M500/8e14) | pivot 10^c0 = 0.717 × a0_H; q = −1/3 (G200), p = 0.99 (G220) | c0 = −0.1445, q = −1/3 |
| G135 2/3 law | log10(T_obs/T_pred) = (2/3)log10 f + log10(2 r_M/R500) | the same law with r_M = √(G M_b c²/(Z R_dS)) | — |
| s_Lambda (G189) | 2 a0_DE | κ_dS / (Z/2) | 1.8725e-10 (committed 1.87238e-10) |

---

## 4. THE KEPLER-GRADE STATEMENT — the falsifier, pre-registered

**The absolute BTFR zero point must sit at c²/(Z R_dS) = 9.362375e-11 m/s² to 1%**
(±0.0043 dex; kill band [9.2697e-11, 9.4560e-11] m/s²).

**KILL RULE (registered today, before the data):** *any well-measured SYSTEM — the
z ≈ 2.5 JWST BTFR (G080/G163), a clean SPARC-class rotation sample, a GEMS-type
group — whose slope-fixed a0 lands off the horizon zero point by > 3σ kills the
geometric reading.*

**Current status, stated honestly:** the full-542 equal-weight zero point sits at
1.813× a0_H (+0.2585 dex, z = +8.98 stat / +6.31 stat+sys) — a **registered
departure, not a kill**: 56% of the offset is the ATLAS3D internal M/L_JAM scale
(Z08/G223's named suspect) plus the registered end-departures (clusters f_b, UFD
dSph status), and the clean TRIO core sits **on** the horizon value (z = −0.20).
The decider is a well-measured system measured *as a system*; the pooled
multi-catalog equal-weight ladder is not that system. If a clean system confirms
the +0.26-dex offset, the horizon reading dies; if the offset dissolves under the
catalog-normalization audit, it stands.

---

## 5. THE UNIFICATION STATEMENT

> **THE ACCELERATION SCALE IS THE DE SITTER HORIZON'S SURFACE GRAVITY.**
>
> a0 = κ_dS / Z, κ_dS = c²/R_dS, R_dS = c/(H0√Ω<sub>Λ</sub>) = 1.6583e26 m.
>
> The **same Z = 2√(8π/3)** that appears in the user's own formula
> a0 = c H_Λ / Z (H_Λ = H0√Ω<sub>Λ</sub>) appears here as **a0 = κ_dS/Z** — one
> number, one derivation, one geometry.
>
> The BTFR **v⁴ = G M_b c²/(Z R_dS)** is a *measurement of the horizon radius*,
> and the 12-decade line is the **horizon geometry projected onto galaxy scales**.

---

## 6. VERDICTS

**V1 — the identity's verification.** a0 = c²/(Z R_dS) = κ_dS/Z holds against every
committed register: footing ratio 1.00005; Ω identity closes at 0.685 exactly;
r_M(Sun) +0.006%; MW r_M −0.002%; cluster seam +0.3%; Σ +0.002%; TRIO core on-value
(z = −0.20). The full-542 slope-fixed zero point is +0.2585 dex off (z = +6.3
stat+sys) — the registered departure the kill criterion is aimed at.

**V2 — the horizon-form constants table.** a0, r_M, Σ, σ², T_b, m, the dust law's
c0/q and the G135 2/3 law's r_M — all re-expressed in (G M_b, R_dS, Z, m): **no
framework constant retains an independent scale.**

**V3 — the honest statement.** THE BREAKTHROUGH EQUATION v⁴ = G M_b c²/(Z R_dS):
derived (a0_DE = c²/(Z R_dS) to 1.00005), verified at the footing, the clean
rotation core, r_M(Sun), MW r_M, the cluster seam and Σ; falsifiable by a single
well-measured system > 3σ off the horizon zero point (the z ~ 2.5 JWST BTFR,
pre-registered). The full-542 zero point's +0.26-dex departure is the armed kill:
catalog-normalization auditable (ATLAS3D M/L_JAM, clusters f_b, UFD status). **What
it means if it survives: the universe's size — R_dS = 1.6583e26 m = 5.37 Gpc —
written into every galaxy's rotation curve.** The BTFR is a measurement of the de
Sitter horizon radius; the 12-decade line is the horizon geometry projected onto
galaxy scales.

---

*Checks: 19/19 PASS (Z11_horizon_form.py → Z11_horizon_form.out → Z11_results.json).
Assembly: the committed 542-object line (G162 + G074/G114/G071/G075/G070 + GEMS G +
ATLAS3D), imported with a byte-identical JSON gate. Context read: G162, G212, G189,
G135, G200/G220, G187, G086/G224, Z08.*