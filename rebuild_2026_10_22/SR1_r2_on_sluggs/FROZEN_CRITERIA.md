# SR1_r2_on_sluggs: FROZEN CRITERIA (committed alone, before any script or number from this comparison)

Written 2026-10-31.

**Question.** Route E and the a₀ law only come level on clean spectroscopic lenses (SI2; SI3 at R2) if red lenses' stellar masses are raised by R2 = +0.295 dex: +0.123 from CFG667 and +0.172 from CFG926's IMF relation (S2's ladder). That scale has no independent dynamical check. Does SLUGGS's measured dynamics allow it? This lane reads the record's dynamical masses against R2's stellar masses, part by part.

**Standing.** κ = ½ is FITTED. Footings canonical (a₀ = 9.3603e-11 m/s²) and alt (1.1312e-10 m/s²) are never pooled; canonical is the headline. The fluid is cold dark energy, a gravitating field component, never a particle. The theory stays open. No preference between frameworks is claimed anywhere in this lane. No download. One thread, `nice -n 15`.

## 0. What I have seen (not blind)

Before freezing I read HO2, SG1, XG1, GR1, CFG38, CFG55, CFG57, CFG71, CFG111, CFG211, CFG323, CFG326, CFG330, CFG466, CFG528/528b, CFG667, CFG669, CFG505, CFG926, AUDIT_SLUGGS, S2, SI1, SI2, SI3, FC1, KN1, ZN1, and Argon's line in `../ARGON_REPLY_2026-10-31/PREDICTIONS_ON_RECORD.md`.

- **The record already prints, on the same 16 galaxies:** under the law, catalogue masses over-predict the inner JAM mass by a median +0.084 dex (half convention, AUDIT_SLUGGS) and Salpeter masses by +0.120 dex; JAM-law masses sit a median 0.10 dex below the catalogue (CFG55); the record's route-E JAM analogue is M★/M_JAM 0.87–0.95 for the four centrals (SG1); nulling the law's outer offset needs M★ a median +0.30 dex above the JAM ceiling (AUDIT_SLUGGS).
- **A hand estimate I made from those committed tables before freezing:** stars alone at the catalogue mass sit near M_JAM inside r₁/₂, median d lg M about −0.03 dex on the half convention.
- **A machinery probe I ran before freezing** (scratch, not committed): CFG55's head loads; K1's law offsets come back at |d| 0.0 on both footings; bin radii in units of R_e per galaxy (all 16 have at least one bin at 1–5 R_e and at 1–3 R_e); median lg(r₁/₂/R_e) over ATLAS3D is 0.137. No rung and no stars-against-M_dyn number was computed.

**My expectation, on record.** Stars at +0.295 exceed M_JAM inside r₁/₂ beyond 2σ. Stars at +0.172 sit at or over that ceiling on the catalogue's scale. The GC window does not bind stars at any rung. The law at +0.172 or more is over M_JAM inside r₁/₂ and roughly level in the GC window. Route E at +0.172 is close to the inner ceiling and short in the GC window for the centrals. A wrong expectation is reported as found.

## 1. Which scale SLUGGS's masses are on

- **The catalogue:** `real_research/data/sluggs_forbes2017_galaxies.tsv`, J/AJ/153/114 Table 1. Its ReadMe (on disk, `_external_data/sluggs_tracers/readme/J_AJ_153_114_ReadMe`) gives log M★ and R_e from Forbes et al. 2017, MNRAS 464, 4611.
- **What that scale is:** Alabi+17 (on disk, `_external_data/alabi2017/src/halov3.tex`, "Size and stellar mass measurements") states that those masses come from Spitzer 3.6 μm light with an age-corrected M/L at a Kroupa IMF, with a typical uncertainty of about 0.1 dex on M★ and about 0.15 dex on R_e. So **near-IR light, age-dependent M/L, Kroupa.**
- **Corrections to the record's wording:** h50's "near-IR M/L ~1.4" is not a stated value of that scale. AUDIT_SLUGGS's "K-band, ~Kroupa/Chabrier-like" has the IMF right and the band approximately right.
- **Against ATLAS3D's own population masses:** AUDIT_SLUGGS's committed table gives catalogue minus ATLAS3D Salpeter of about −0.10 dex (median, 16 galaxies), so the catalogue's total masses sit about +0.15 dex above ATLAS3D's Chabrier (Salpeter − 0.25). Part of that is more light: the 3.6 μm R_e runs larger at the massive end. This gap is why §5's same-light row exists.

## 2. How R2's two parts carry over

R2 is defined on the record's lens masses, LePhare MASS_MED + 0.15 dex. No galaxy is common to KiDS-bright and SLUGGS, so no direct tie exists on disk.

- **+0.172 (CFG926) is an IMF statement relative to Chabrier.** It should apply to SLUGGS: log α_Salp = −0.0748 + 0.0986 lg(σ_e/200), with Salpeter/Chabrier 1.778, at σ 186 km/s. **It carries over at face value.** Kroupa against Chabrier is recalled as 0.03–0.05 dex and is not on disk (PROVISIONAL, not applied); applying it would lower this rung by at most 0.05 dex.
- **+0.123 (CFG667) does not carry over.** It is median(log M★_Taylor − log M★_LePhare), OLD minus YOUNG, at fixed LePhare mass, inside KiDS's optical photometry. SLUGGS's masses use neither estimator. The same difference on near-IR light is +0.026 (CFG669, OLD − YOUNG on Ks). So on a near-IR scale it has almost no counterpart.
- **So R2 as carried to SLUGGS is +0.172.** This lane's verdict is on that rung.
- **Literal +0.295 is kept** as the upper bracket, as what Argon's lines name, and as the first table asks. It says the SLUGGS catalogue shares the lens catalogue's deficit, which nothing on disk supports or excludes.
- **Rungs, each a uniform shift at all radii, as in S2 and SI2:** R0 (catalogue), **I = +0.172**, **L = +0.295**.
- **Reported rung T = +0.091:** a tie through CFG505. Bell+03 u − r → M/L_K masses sit +0.304 above LePhare + 0.15 on early-type lenses; Bell+03's IMF is about +0.10 above Chabrier (recalled, PROVISIONAL). So R2's lens mass reads 0.295 − (0.304 − 0.10) above a Chabrier near-IR colour scale. Not graded.
- **Reported rung Iσ:** CFG926's relation at each galaxy's own ATLAS3D σ_e, with the coefficients read from `cfg926_results.json`.

**A limit stated now.** CFG926 fits its relation to ATLAS3D's (M/L)_stars, which comes from JAM models with NFW halos. So on ATLAS3D's own population scale, +0.172 is allowed inside r₁/₂ almost by construction. The test at r₁/₂ is not fully independent of the rung. The GC window is independent of ATLAS3D. CFG926's own native check gives +0.168 / +0.154, so the rung's value is not carried by the NFW step. No NFW quantity enters M_dyn, the models or the classes here.

## 3. The dynamical masses (the record's estimators, nothing new)

**Sample:** CFG55's 16 galaxies, the SLUGGS galaxies with ≥ 30 clean GCs, ≥ 2 bins and ATLAS3D JAM quality ≥ 1. h50's name-key artefact drops NGC 821 from that list; it is restored in §8 row 8. Machinery: CFG55's script executed read-only (h50 → CFG38 → CFG55).

- **M_dyn inside r₁/₂:** the ATLAS3D JAM mass, M_dyn(< r₁/₂) = ½ (M/L)_JAM L_r, moved to SLUGGS's distance (M_JAM and r₁/₂ ∝ D), model A, no halo. As CFG33, CFG55, AUDIT_SLUGGS, GR1, HO2 and SG1.
- **M_dyn at GC radii:** h50's σ_LOS bins (raw velocities, clipped, rotation folded in) through CFG55's spherical Jeans solver. For a model X with enclosed mass M_X(r), per bin, lg k = 2 log₁₀(σ_obs/σ_pred,X). k is the constant factor on M_X(r) that matches that bin. It is CFG55's offset × 2, not a new estimator. It weights r ≥ R_b, so it is not a local mass. Any mass added to stars raises σ_pred, so σ_pred > σ_obs for stars alone is a valid ceiling at given tracer and anisotropy.
- **Anisotropy and tracer:** isotropic orbits, γ = 3 for every galaxy, as CFG55. β = ±0.5 (CFG113's bracket, AUDIT_SLUGGS) and CFG111's published-relation γ are reported rows.
- **Hot gas:** omitted, as h50, CFG38 and CFG55. In the ceiling test this favours R2, since gas only lowers the room for stars. Measured gas is a reported row on the four centrals only (§5).
- **Stars:** Hernquist with a = R_e/1.8153 at SLUGGS's R_e, h50's profile.

**Statistic, all rows:** d lg M ≡ lg(M_dyn / M_model) inside the same radius. Positive means the model is short of M_dyn. Negative means the model exceeds M_dyn.

- **At r₁/₂, primary (same radius, same profile):** M★(< r₁/₂) = f_H M★, f_H = r₁/₂²/(r₁/₂ + a)². Reported beside it: the record's half convention, f = ½.
- **GC windows:** per galaxy, the mean of lg k over h50's bins with 1 ≤ R_b/R_e ≤ 5 (Argon's window, graded), and over 1 ≤ R_b/R_e ≤ 3 (Argon's earlier window, for its lines). No re-binning. CFG55's full outer bins are reported.
- **Sample number:** the median over galaxies. Mean and SEM are printed beside it.
- **Error:** σ_b, the standard deviation of the median over 20,000 bootstrap draws of galaxies, seed 20261031.
- **Z_stat** = median/σ_b.
- **Z_sys** = median/√(σ_b² + σ_s²). σ_s = 0.10 dex at r₁/₂, the catalogue's stated M★ uncertainty treated as fully shared, which is the case least harsh on R2. σ_s = √(0.10² + 0.052²) in the GC window, adding CFG323's shared γ term (0.026 dex in log σ).

## 4. First table: stars alone, no halo, no law (no footing enters)

For each of the 16 galaxies: M★(R0), M★(+0.172), M★(+0.295) against M_dyn inside the same radius, at r₁/₂ and in the 1–5 R_e window. A galaxy is flagged **OVER** if d lg M < 0, and **OVER BY 2σ** if d lg M < −2σ_i.

- At r₁/₂: σ_i = √(0.05² + 0.10² + (2a/(r₁/₂ + a) × 0.15)²), with JAM 0.05 dex recalled and PROVISIONAL, and the catalogue's M★ and R_e errors as in §1.
- In the GC window: σ_i = √((2σ_o)² + 0.10²), with σ_o from h50's bootstrap errors on σ_obs.

**Ceiling class, per rung and radius:**

| class | rule |
|---|---|
| BELOW THE CEILING | Z_stat > +2 |
| AT THE CEILING | \|Z_stat\| ≤ 2 |
| OVER THE CEILING | Z_stat < −2 and Z_sys ≥ −2 |
| EXCLUDED | Z_sys < −2 |

A rung's class is the worse of its two radii (order as listed).

## 5. The law and route E on top (each footing separately)

- **The law:** algebraic, spherical, g = g_N ν(g_N/a₀), ν(y) = ½ + √(¼ + 1/y), the kernel HO2 and SI1's law carry. No halo. Stars at the rung.
- **Route E:** Newtonian stars at the rung plus cold dark energy. SI1's `halo_of`, text-executed read-only: FC1's rule, S = max(Σ_a₀, f_c η_conv(M_t) Σ_coll(M_t)), M_t = M200/f_c; smooth core, ρ₀r₀ = S, M_h(r) = π S r₀² B(r/r₀), B(x) = 4[asinh x − x/√(1+x²)]; M200 from EM1's relation; continued to r_ta. z = 0. M200's argument is the galaxy's stars at the rung, as SI2 froze it and as GR1 and HO2 use stars only for SLUGGS (no cold or hot gas in the argument).
- **Native z = 0 line (reported, one row, no footing):** KN1's rule with EM1's masses: M_c(r) = f_c M_t m(r/R_t) for r ≤ x_edge R_t, constant beyond, m the median z = 0 shape from `../ZN1_zooms_to_z0/zn1_shapes.json`, interpolated in lg M between tags, clamped outside.

**State per model, rung, radius:** LEVEL if |median| ≤ 0.07 dex (Argon's width); OVER if median < −0.07 with Z_stat < −2; SHORT if median > +0.07 with Z_stat > +2; WITHIN 2σ otherwise. **LEVEL AT BOTH** means LEVEL at r₁/₂ and in the 1–5 R_e window.

**Reported per model and galaxy:**
- Δ_ceil, the rung at which the model reaches M_dyn at r₁/₂ (the route-E JAM-analogue idea of HO2 and SG1, with the same-radius fraction).
- Δ_null, the rung that zeroes the 1–5 R_e window.
- Their gap, Δ_null − Δ_ceil. A positive gap means no single stellar scale fits both radii.

These are per-galaxy roots, not scans, and they carry no class weight.

## 6. Verdict (frozen; canonical is the headline, alt printed beside it)

On rung I, as carried:

| verdict | rule |
|---|---|
| **SR1 PASS** | stars at I are AT or BELOW at both radii, and the law or route E (named) is LEVEL AT BOTH at I |
| **SR1 ALLOWED, NOT LEVEL** | stars at I are AT or BELOW at both radii, and neither model is LEVEL AT BOTH at I |
| **SR1 OVER** | stars at I are OVER THE CEILING at a radius, not EXCLUDED at either |
| **SR1 FAIL** | stars at I are EXCLUDED at a radius |

**LITERAL R2: <class>** is stated beside it, with the ceiling class of stars at L.

**Qualifiers, appended when they fire:**
- **[RADIUS-CONVENTION-DEPENDENT]:** the r₁/₂ class of stars at I or L changes on the half convention.
- **[SCALE-DEPENDENT]:** the r₁/₂ class of stars at I or L changes when R0 is ATLAS3D's own population Chabrier (Salpeter − 0.25, half the same light, half convention) in place of the SLUGGS catalogue.
- **[TRACER-DEPENDENT]:** the GC window class of stars at I or L changes under CFG111's γ, β = +0.5 or β = −0.5.
- **[CENTRALS-DEPENDENT]:** the class of stars at I or L changes on the 12 non-centrals (without NGC 4486, 4365, 4374, 5846).

## 7. Argon's lines, frozen as stated, with my reading

Relayed from Argon, an external reviewer:

- **A1, its PASS line:** dynamical masses at 1–5 R_e agree with R2 stellar masses within |median d lg M| ≤ 0.07 dex.
- **A2:** |median d lg M_dyn| ≤ 0.05 at 1–3 R_e at R2. `PREDICTIONS_ON_RECORD.md` writes this as median |Δ lg M_dyn|, the median of the absolute value. Both forms are scored.
- **A3:** M_dyn under-predicted by 0.18–0.25 dex at R0, read as +0.18 ≤ median d lg M ≤ +0.25, 1–3 R_e, because it sits in the same sentence as A2.
- **A4, its FAIL line:** SLUGGS rejects R2 by more than 2σ.

**Reading.** R2 in these lines is +0.295, as PREDICTIONS_ON_RECORD says. Its text does not name a model, so A1–A3 are scored on three rows, stars alone, the law and route E, canonical with alt beside, and each HIT is named with its row. A1 also gets a column for the JAM mass at r₁/₂, which sits at about 1.33 of ATLAS3D's own R_e. **A4 fires** if stars at L have Z_stat < −2 at r₁/₂ or in the 1–5 R_e window, or if the law or route E at L has |Z_stat| > 2 in the 1–5 R_e window or Z_stat < −2 at r₁/₂; each firing row is named and Z_sys is printed beside it. All of it is repeated at rung I, reported. These scores change no class.

## 8. Reported, no class weight except §6's qualifiers

1. The half convention at r₁/₂ for stars, the law and route E.
2. ATLAS3D's population Chabrier at the three rungs, stars, half the same light (the [SCALE-DEPENDENT] row).
3. CFG111's γ = clip(−0.63 lg M★ + 9.81, 2, 4), and β = ±0.5, GC windows, three models.
4. The 12 non-centrals and the 4 centrals separately.
5. Rungs T and Iσ, three models.
6. Route E with M200's argument held at the catalogue mass while the stars move (SI2's halo-rung question), at I and L.
7. Route E on CE1's A4 η table (`ce1_a4_results.json`) in place of SI1's.
8. h50's 19 galaxies, GC windows only. CFG55's sample with NGC 821 restored (CFG55's key fix, in memory, N = 17).
9. The four centrals on the record's best tracers: CFG528b's measured GC density profiles and anisotropy (row M), with and without CFG331's measured gas truncated at the X-ray edge, 1–5 R_e, three models, catalogue masses.
10. Alabi+17's published M_tot(< 5 R_e) and f_DM at β = 0, read from the tex on disk as CFG431 reads them: d lg M = −lg(1 − f_DM) − Δ. Its slope α comes from simulated circular-velocity curves, which is why this stays a reported row. The column name is that paper's.
11. Stars at R0: per galaxy, d lg M at r₁/₂ against the innermost bin of the 1–5 R_e window, as a cross-check between the two M_dyn estimators.
12. M★/M_JAM at the three rungs for the four centrals, beside SG1's 0.87–0.95.

## 9. Checks (any K failure: no verdict, exit 1)

- **K1, reproduces the record (exact):**
  - (a) CFG55's committed per-galaxy law offsets and log M★_law on both footings, through the exec'd machinery, |d| ≤ 1e-10;
  - (b) this lane's stars-only path at R0 over CFG55's outer bins equals h50's `off_newt` per galaxy, |d| ≤ 1e-12;
  - (c) this lane's law path, with CFG55's kernel, reproduces CFG55's committed SLUGGS-mass law mean on both footings, |d| ≤ 1e-10;
  - (d) CFG528b's row M K0 per galaxy, |d| ≤ 1e-6, as GR1's K0c.
- **K2, radius matching:**
  - (a) r₁/₂ and M_JAM recomputed from the raw TSV equal the machinery's values, ≤ 1e-9 relative;
  - (b) median lg(r₁/₂/R_e) over ATLAS3D within 0.03 of lg 1.33;
  - (c) f_H at 1.33 R_e = 0.5 within 1e-3;
  - (d) the range of f_H over the 16 rounds to CFG55's printed 0.28–0.57;
  - (e) every graded bin lies inside its window and inside h50's outer bins, and all 16 have ≥ 1 bin at 1–5 R_e and at 1–3 R_e.
- **K3, route E and the native line:**
  - (a) FC1's S/Σ_coll at the nodes, 21.802 / 14.849 / 14.217, within 1e-3;
  - (b) M_h(R200) = M200 within 1e-8 for every unsaturated halo, saturated halos counted (SI1's K3);
  - (c) the native m at x = 1 equals 1 within 1e-3 at each tag;
  - (d) the a₀ values equal P2's text.
- **K4, linearity:** stars' d lg M(+Δ) = d lg M(R0) − Δ at both radii, ≤ 1e-9.
- **K5:** peak RSS < 1 GB.
- **Rerun:** a second normal run gives a byte-identical results JSON (checked after the run, reported in the README).
- **MUTATE (`--mutate`, outputs `_MUTATE`):** every JAM mass × 0.5, every σ_obs × 0.8, route E's and the native halo × 0.5. It must:
  - shift stars' median d lg M at r₁/₂ by −0.30103 and in the GC window by −0.19382, each ±1e-6;
  - shrink |d lg M(route E) − d lg M(stars)| in the 1–5 R_e window at R0 for every galaxy, against the normal run;
  - fail K1 and exit 1.

## 10. What this cannot show

- **The tie between lens masses and SLUGGS masses is not measured.** Rungs I and L are two readings of it, and T a third. Table 1 lets a reader place any other tie by the ceiling rung Δ_ceil.
- **SLUGGS galaxies are local, massive, mostly group or cluster members, and the four centrals carry most of the mass range.** R2's lenses are isolated, red, at z ≈ 0.25, with σ about 186 km/s. A uniform shift across these is an assumption.
- **A measured IMF gradient** (bottom-heavy core, lighter outskirts) would make a uniform rung overstate the outer stars.
- **Isotropy and γ = 3 are assumptions,** bracketed in §8. The GC estimator's significance is statistical plus the stated shared terms.
- **M_JAM assumes mass follows light inside r₁/₂ and carries no anisotropy term beyond JAM's.** Its 0.05 dex per-galaxy error is recalled.
- **The Hernquist profile stands in for the 3.6 μm light.**
- **A pass here would be a check of a stellar-mass scale.** It would not derive κ, and it would not choose between route E and the law.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 -B sr1_grade.py` (twin: add `--mutate`). Amendments only in `AMENDMENT_*.md`, each committed before the run it affects, or marked post-result.
