# Route 3 — the Bullet Cluster + offset-lensing through the framework (2026-06-15)

*Task [bullet_offset]: assess the Bullet (1E 0657-558) and the offset-lensing "direct DM proof" through the
framework's OWN relativistic lensing law (AeST, a0 = c²√(Λ/32π) = 9.36e-11, dS-Unruh ν=√(1+1/y)). Both ways:
where the framework genuinely accommodates the offset, where it still needs the (shared) cluster residual, where
the Bullet is actually a PROBLEM for ΛCDM. Builds on the banked `bullet_qumond_redo.py`,
`bullet_and_s8_reexamination.py`, the cluster synthesis (η(R500)≈2.33), and the lensing footing audits.*

---

## HEADLINE (both ways)

The Bullet's lensing **offset** (κ peaks on the galaxies, not the dominant X-ray gas) is **NOT an independent
DM proof and NOT a clean MOND falsifier** — the 2026 JWST literature (Rihtaršič+2026 lens model; the consistent-
QUMOND model 2604.10811; Famaey 2026, 2605.10022) now shows the QUMOND **phantom mass reproduces the offset**
(compact galaxies make concentrated phantom; diffuse gas makes a flat sheet) AND that what remains is the
**same residual missing-mass discrepancy as every other cluster** — collisionless, centered on the galaxies,
NO neutrinos needed. So "the Bullet proves DM" **reduces to** "clusters need a residual" (the banked η≈2.33
cluster problem), which is **MOND-SHARED** and inherited, not a separate Bullet-specific kill.

Two things the framework genuinely gets to cite: (a) AeST has **no gravitational slip** (Φ_lens = Φ_dyn), so
lensing mass ≡ dynamical mass — lensing adds **zero** independent DM evidence beyond the dynamical residual;
(b) the Bullet's **collision velocity** (~3000–4700 km/s) is a genuine ΛCDM problem (P~10⁻⁹–10⁻¹¹, Lee &
Komatsu 2010) that Λ-MOND faster structure formation accommodates naturally.

Two honest concessions: (a) the framework's lower a0 makes the residual **~12–13% LARGER**, not smaller (the
banked cluster surcharge); (b) the banked `bullet_qumond_redo.py` toy could **not itself** reproduce the
offset-flip — the 2026 literature (compact per-galaxy modelling) does, but the framework imports that result
rather than deriving it. The Bullet stays an **inherited, MOND-shared, soft** liability — not solved here, not a
clean kill either way.

---

## (i) AeST ties lensing to dynamics — lensing is NOT an independent DM proof (CONFIRMED, full weight)

**From the AeST field equations (Skordis-Zlosnik 2021; Verwayen, Skordis & Bœhm 2023, arXiv:2301.03499):**
matter couples minimally to the metric, and in the weak-field quasi-static limit the metric has the GR form
with the Newtonian potential replaced by **Φ = Φ̂ + φ** (Φ̂ = metric/tensor part, φ = scalar). The total
acceleration is **a_tot = −∇Φ̂ − ∇φ = −∇Φ**, and **weak lensing uses the SAME Φ** ("we can therefore use the
standard formalism for weak lensing just by taking into account Φ = Φ̂ + φ"). There is **no gravitational
slip** (the lensing/Weyl potential = the dynamical potential), exactly as TeVeS/AeST are CONSTRUCTED to do —
this is what fixed original non-relativistic MOND's under-lensing.

**Consequence (the load-bearing reframe):** the lensing mass M_lens(r) = M_dyn(r) = M_eff(r) = M_baryon +
M_phantom. **Lensing recovers the same total mass dynamics already needs — it adds NO independent DM proof.**
"Lensing proves DM" therefore **reduces to** "the cluster dynamical residual exists" (the known, banked
η(R500)≈2.33 problem). This is a real reframe and is reported at full weight: the standard rhetorical move
"even if you modify gravity for dynamics, lensing independently needs DM" is **false for relativistic MOND**.
(It would be true for a pure-modified-inertia / baryon-only-metric variant — and that variant is separately
killed at 12.5σ by the framework's own `f4_lensing_wall.out`. The framework's actual channel is the AeST
phantom-halo, which lenses correctly.)

## (ii) The OFFSET: QUMOND phantom reproduces it — offset ≠ falsification (the 2026 update)

The naive claim "MOND gravity is sourced by the gas (dominant baryon) so κ MUST peak on the gas" is **wrong**:
QUMOND phantom density ρ_ph = (1/4πG)∇·[(ν−1)∇Φ_N] is a **nonlinear functional of baryon DENSITY**, not of
surface density. **2026 result (Verlinde-independent, web-verified):**

- **Consistent QUMOND model (2604.10811, a0=1.2e-10):** the QUMOND κ map matches the GR lensing reconstruction
  with residuals "below 0.15" — comparable to differences between independent GR reconstructions. The
  **point-like galaxies (7% of baryons) generate ~48% of the phantom mass**; the diffuse gas makes a flat
  ~Mpc sheet. The phantom **concentrates on the galaxies** → κ peaks on the galaxies, offset from the gas,
  reproduced **without** collisionless DM for this feature. Total inferred mass ~1.1×10¹⁵ M☉, compatible with GR.
- **Famaey 2026 (2605.10022, on the Rihtaršič JWST lens model, a0=3700 km²/s²/kpc = 1.20e-10):** MOND with
  observed baryons gives M/M_bar ≈ 2.8–3.3 at 300 kpc vs observed ≈ 8 → a residual factor ~2.4–2.9×; adding a
  residual missing mass of **3.4×10¹⁴ M☉ (collisionless, centered on the galaxies)** matches to <10%. Explicit:
  "this residual missing mass should be mostly collisionless, since it is centred on the galaxies" and "this
  cluster exhibits the **same residual missing mass discrepancy as other clusters** of similar mass." **No
  neutrinos invoked** (a 2026 update vs the old Angus-Famaey-Zhao 2006 ~2 eV neutrino patch).

**Reconciliation with the banked toy.** The framework's own `bullet_qumond_redo.py` SCANNED galaxy compactness
and found that for blob-scale galaxies (b_gal ≥ 70 kpc) the phantom did NOT flip the peak off the gas — and
honestly reported it could not certify the flip. The 2026 literature shows the flip DOES happen when galaxies
are modelled as **individual compact (~10–30 kpc) sources** (sharp 1/R phantom spikes) on the real β-model gas.
**Both ways:** the offset-flip is real in QUMOND but **hinges on the compact per-galaxy modelling** — a real,
defensible, but still-contested choice (2605.10022 still finds the residual centered on the galaxies). The
framework **imports** this resolution; it does not derive it. NET: the offset is **not** the airtight
falsification it is sold as, but it is **not cleanly closed** either.

## (iii) The QUANTITATIVE residual — framework footing (the honest surcharge)

The Bullet residual factor at the **canonical** a0=1.2e-10 (what ALL the cited papers use) is ~2.4–2.9×. On the
**framework's** a0=9.36e-11, deep-MOND boost scales as √(a0): √(9.36e-11/1.2e-10) = **0.883** → the framework
phantom is ~12% WEAKER → the residual is **~13% LARGER** (M/M_bar ≈ 2.8→3.2, 3.3→3.7; residual ~2.5–3.0×). This
is the **same banked cluster surcharge** (η(R500): canonical ~2.07 → framework ~2.33, +13%). **Footing
verdict:** every cited Bullet/MOND-lensing measurement is on **canonical/local a0 (1.2e-10), NOT 9.36e-11** —
but here the wrong footing makes the framework look **BETTER** than it is (smaller residual). Re-footed
correctly the framework is ~13% WORSE, not better. So there is **no false-deficit** to retract (no wrong-a0
inflating the loss); if anything the canonical-a0 literature **understates** the framework's residual.
Reported at full weight: the Bullet residual **is** the (shared) cluster residual, +13% for the lower a0.

## (iv) The COLLISION VELOCITY — a genuine ΛCDM problem the framework can cite (both ways)

The Bullet shock is ~4700 km/s (Markevitch 2006); the gas-bullet itself ~2700 km/s (Springel & Farrar 2007);
the inferred collision velocity ~3000 km/s. **Lee & Komatsu 2010** find P(such a velocity | ΛCDM, in 2–3 R200)
≈ **3.3×10⁻¹¹ to 3.6×10⁻⁹** — a ~1-in-10⁹ event for concordance cosmology. **MOND / Λ-MOND structure
formation** (enhanced gravity → faster growth, earlier collapse, higher infall velocities) produces such speeds
**naturally** (the same engine behind El Gordo's tension with ΛCDM). **This is a real point the framework gets
to cite**: the Bullet is simultaneously (a) NOT the DM proof it is sold as (offset reproduced, residual shared)
and (b) a velocity PROBLEM for ΛCDM that the framework's faster structure formation accommodates.
**Caveat (both ways):** the high velocity is *partly* hydrodynamically enhanced (shock ≠ bulk speed), and large
sims (Thompson+2015, Kraljic & Sarkar 2015) find such ΛCDM speeds rare-but-allowed — so it is a **ding** on
ΛCDM, not a clean kill. (Note: the banked `bullet_and_s8_reexamination.py` correctly marks the OLD
"non-equilibrium phantom-lag" resolution [BROKEN] — the field re-settles on R/c ~2 Myr ≪ 150 Myr collision time,
so a lag cannot freeze the phantom on the galaxies. The 2026 **density-weighting** mechanism, not a lag, is the
correct offset explanation — supersede the lag argument.)

## (v) Other offset cases (both ways)

- **Abell 520 "train wreck":** a "dark core" — a mass concentration ON the X-ray gas with M/L~800, awkward for
  collisionless CDM (DM should follow galaxies, not gas) AND for MOND. But it is **disputed**: Clowe+2012 does
  not detect it; Jee+ re-confirms it (shifted); it is a **multi-merger** with ≥5 mass peaks. **Unsettled — cuts
  both ways**, not a clean win for either side. The framework can cite it as "the offset story is messier than
  the Bullet poster suggests," but cannot bank it.
- **NGC1052-DF2 / DF4 (DM-deficient galaxies):** awkward for ΛCDM (galaxies with ~no DM halo where ΛCDM expects
  >300× stellar mass) and a **genuine MOND EFE test**. MOND predicted σ ≈ 13–14 km/s for DF2 **via the external
  field effect** (proximity to NGC 1052 weakens self-gravity), **consistent with observation** — a real,
  confirmed framework-side prediction (the EFE is a MOND signature ΛCDM has no analog for). The 2024–2026 "bullet
  dwarf" trail (DF2/DF4 + a third, kinematically connected) has both tidal and SIDM readings — contested, but the
  EFE σ-prediction is a clean MOND hit. **Framework can cite DF2 EFE; the trail is contested.**

---

## RESOLUTION STATUS

| sub-claim | status | why |
|---|---|---|
| AeST: lensing = dynamics, no slip | **LIVE-AVENUE (confirmed)** | Φ_lens=Φ_dyn=Φ̂+φ; lensing adds NO independent DM proof — "lensing=DM" REDUCES to the cluster residual |
| Bullet offset (κ on galaxies) | **REDUCES-TO-CLUSTER-PROBLEM** | QUMOND phantom reproduces the offset (2604.10811); residual is the shared cluster η, collisionless, no neutrinos |
| Bullet residual amplitude (~2.4–3×) | **CONCEDED (shared, +13% surcharge)** | = banked η(R500)≈2.33; framework's lower a0 makes it ~13% LARGER, not smaller |
| offset-flip DERIVED by framework | **NOT DERIVED (imported)** | banked toy couldn't flip blob-galaxies; 2026 compact-galaxy modelling does — framework imports it, contested |
| collision velocity vs ΛCDM | **LIVE-AVENUE (framework cites)** | P~10⁻⁹–10⁻¹¹ in ΛCDM (Lee & Komatsu 2010); Λ-MOND natural — a ding on ΛCDM (partly hydro-enhanced) |
| Abell 520 dark core | **UNSETTLED (both ways)** | disputed (Clowe vs Jee), multi-merger; not bankable |
| DF2/DF4 EFE prediction | **LIVE-AVENUE (framework cites)** | MOND EFE predicted σ~13–14 km/s, matches; DM-deficient galaxies awkward for ΛCDM |

## FOOTING

Every cited Bullet/MOND-lensing measurement uses **canonical a0=1.2e-10** (Famaey 3700 km²/s²/kpc = 1.20e-10;
2604.10811 = 1.2e-10; AeST-lensing Verwayen+2023 = 1.2e-10). **None uses the framework's 9.36e-11.** Direction
of the error: canonical a0 makes the framework's residual look ~13% SMALLER than it truly is → the literature
**understates** the framework's Bullet residual. So there is **NO false-deficit** here (no wrong-a0 inflating a
loss); the only correction is **anti-framework** (the residual is ~13% larger re-footed). Reported per the #1
rule. Quarantine held: a0/Z never asserted derived.

## ONE LINE

The Bullet's lensing offset is **not** an independent DM proof — in AeST lensing mass ≡ dynamical mass (no
slip), the QUMOND phantom reproduces the κ-on-galaxies offset (2026 JWST literature), and what's left is the
**same MOND-shared cluster residual** (η≈2.33, +13% on the framework's lower a0, collisionless, no neutrinos);
meanwhile the Bullet's collision velocity is a genuine ΛCDM problem the framework can cite — so the Bullet is
an **inherited, shared, soft** liability and a **mild ΛCDM embarrassment**, NOT the clean DM kill-shot it is
sold as, and NOT cleanly solved by the framework either.
