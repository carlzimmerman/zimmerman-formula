# L100 — How to kill or confirm the framework: a one-page observing spec

The framework's two sharpest, no-wiggle-room MOND-vs-dark-matter falsifiers
(from L89, L90), turned into concrete, quantitative test plans. Both a₀
footings (canonical 9.3619e-11, alt 1.1279e-10 m/s²). All numbers are computed
in `L100_killshot_test_plan.py` (16/16 PASS; statistical machinery
Monte-Carlo-validated in controls C2/C3). Verdict here is neutral: this lane
builds the test, it does not claim the framework passes it.

---

## TEST 1 — Dwarf spheroidal σ vs Galactocentric distance R_gc (the EFE)

**Predicted signal.** A nonlinear MOND kernel violates the strong equivalence
principle: the Milky Way's field g_ext(R_gc)=V_c²/R_gc partially Newtonises a
dwarf. Internal dispersion σ = σ_N/√μ_e(g_ext/a₀), capped at the isolated
deep-MOND value σ_iso = ((4/9)GMa₀)^{1/4}. For a fiducial dwarf (M_b=10⁶ M_⊙,
r_½=300 pc):

| R_gc (kpc) | 40 | 80 | 150 | 250 |
|---|---|---|---|---|
| σ_can (km/s) | 4.42 | 6.05 | 8.15 | 8.62 |
| σ_alt (km/s) | 4.80 | 6.60 | 8.91 | 9.03 |

→ σ rises **×1.95 (canonical) / ×1.88 (alt)** across 40→250 kpc. Amplitude is
mass-dependent (larger for fainter, lower-M dwarfs).

**Dark-matter null.** σ set by the subhalo, independent of R_gc → **flat** (0×
trend), absent tides.

**Precision.** σ error ≈ 1/√(2(N−1)) per dwarf: N=40 members at a few km/s each
→ 11% (0.049 dex). Routine for classical dSphs (σ~7–10 km/s ≫ e_v~2 km/s);
harder for ultra-faints.

**Sample size.** Per-dwarf residual scatter budget ≈ 0.12 dex (measurement +
M^{1/4} mass error + intrinsic/structural). Against the flat null:
**N ≈ 10 dwarfs for 3σ, ≈ 28 for 5σ** (both footings). The **17 named targets
below already give ≈ 3.9σ** at this scatter — the data largely exist.

**Real targets (R_gc ≈ 28–254 kpc):** Segue 1 (28), Ursa Major II (38),
Segue 2 (42), Coma Ber (45), Boötes I (64), **Draco (76), Ursa Minor (78),
Sculptor (86), Sextans (89), Carina (107)**, Crater II (117, LSB touchstone),
Hercules (126), **Fornax (149)**, Leo IV (155), Canes Venatici I (218),
**Leo II (236), Leo I (254)**. Bold = classical dSph, easy σ.

**Confounds (honest).** *Tidal stripping is the crux:* in ΛCDM, dwarfs at small
R_gc are more stripped → lower halo mass → lower σ — the **same sign** as the
EFE. So "DM predicts zero R_gc-dependence" holds **only for tidally-undisturbed
dwarfs**. Break the degeneracy with Gaia orbits: the EFE tracks the **current**
g_ext(R_gc); tides track **pericenter/history** — so σ-vs-pericenter *at fixed
R_gc* separates them. Also: binaries inflate σ (worst for UFDs; need multi-epoch),
non-equilibrium dwarfs violate the virial estimator, and V_c declines at
100–250 kpc (use an enclosed-mass g_ext, not flat V_c).

---

## TEST 2 — Flat a₀(z): the deep-MOND BTFR zero-point at z≈2

**Predicted signal.** Deep-MOND BTFR V_flat⁴ = G M_b a₀, so at fixed M_b,
V_flat ∝ a₀^{1/4}. The framework ties a₀ = c²/2πL_dS to a Λ-locked de Sitter
scale ⇒ **a₀(z) flat ⇒ BTFR zero-point offset at z≈2.5 = 0.00 dex.**

**ΛCDM null.** The repo-committed expectation (`project_framework_vs_lcdm_test`)
is **+0.33 dex** at z≈2.5. (A naive a₀∝H(z) would give +0.12 dex in the
V-zero-point — the same-sign, cleanly separable direction.)

**Precision.** Per-rotator offset error σ_off = √(σ_logMb² + (4σ_logV)² +
σ_int²) ≈ **0.27 dex** with σ_logMb≈0.20 (stars+gas), σ_logV≈0.04 (V to ~9%;
enters BTFR ×4 → 0.16 dex), σ_int≈0.10. **Rotation velocity to ~9% is the
binding requirement.**

**Sample size.** σ_ZP = σ_off/√N; to split 0.00 from +0.33 dex:
**N ≈ 7 rotators for 3σ, ≈ 18 for 5σ** (footing-independent — a₀'s value sets
the local zero-point, not its z-invariance).

**Real targets / existing data.** *Must reach the deep-MOND regime (g<a₀) with a
defined V_flat.* Massive z~1–2.5 SFGs (KMOS³D, SINS/zC-SINF; Genzel+2017/2020,
Übler+) are the **wrong regime** (baryon-dominated, declining RCs). Right
targets: **lensed disks** (magnification → lower eff. mass/larger radii → g<a₀;
Cosmic Snake z=1.04, A521-sys1) and **ALMA [CII]/CO cold rotators** z~2–4.5
(Rizzo+2020/21, Lelli+2021). JWST NIRSpec IFU Hα can extend the sample; SPARC
(Lelli+2016) fixes the z=0 anchor. Current archive can **start** the test with a
handful; not yet decisive.

**Confounds (honest).** z~2 disks are dynamically hot (V/σ~2–5): need
asymmetric-drift correction and beam-smearing control. Gas dominates M_b;
α_CO uncertain ~0.3 dex. Must verify each object is deep-MOND. Lensing
magnification uncertainty ~10–20% for lensed targets.

---

## Prioritised plan — which is cleaner, cheaper, sooner

| | Dwarf σ–R_gc (Test 1) | Flat-a₀ BTFR (Test 2) |
|---|---|---|
| Cost / timeline | **Cheapest, soonest** — local, ~17–25 dSph already have kinematics; Gaia orbits in hand | Expensive per object (lensed/ALMA/JWST); rare deep-MOND z~2 rotators |
| Sample for 3σ / 5σ | ~10 / ~28 dwarfs | ~7 / ~18 rotators |
| Cleanliness | **Confounded**: tidal stripping mimics the same-sign trend | **Cleanest**: no astrophysical effect of comparable strength mimics a BTFR-zero-point z-drift |
| Binding limit | Separating EFE from tides (use pericenters) | Reaching g<a₀ with well-measured M_b |

**Recommended order.** (1) Run **Test 1 now** on archival classical-dSph
kinematics + Gaia orbits — a fast, cheap first-look screen. (2) Build the
**Test 2** sample of ~10–18 lensed/ALMA deep-MOND rotators at z~2 — the
**definitive, degeneracy-free killshot**, and the one that directly probes the
framework's defining principle a₀ = c²/2πL_dS.

**What a null means.**
- **Test 1 null** (σ flat vs R_gc for undisturbed dwarfs) → kills the EFE →
  favours dark matter. A ~1.9× trend surviving the tidal control confirms it.
- **Test 2**: a flat BTFR zero-point (0.00 dex) at z~2 confirms the Λ-locked
  a₀; a robust +0.33 dex (ΛCDM), or a rising a₀∝H(z), kills the flat-a₀
  prediction — the framework's sharpest distinctive signature.

**Bottom line.** The dwarf test is the one to run *first* (it can be done with
today's data), but the BTFR test is the *cleaner killshot* — the dwarf trend
shares its signature with tidal stripping, whereas a BTFR-zero-point z-drift
does not. Both footings carry both falsifiers.
