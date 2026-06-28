# FRAMEWORK-NATIVE POSITS SLATE (graded, both-ways, NOT a TOE)

> ## ⚠️ CORRECTION (2026-06-27, on adversarial review — overrides B4 below)
> **B4 (velocity-ellipsoid anisotropy sign) is RETRACTED as a "genuinely-new MG-impossible discriminator"
> and DOWNGRADED to SPECULATIVE-UNVERIFIED. It is NOT added to the live ledger.** On review of the backing
> script (`reviews/posit_empirical_sharpen.py`), the "MG-impossible / opposite-sign" claim rests on TWO
> coded assumptions, not derivations: (1) `beta_MG` is **hardcoded positive** (built so L_e>0 ⇒ β>0) with
> **no modified-gravity dynamical calculation**; (2) `beta_MI` uses an unjustified `σ² ∝ 1/μ(boost)` proxy
> (real velocity anisotropy comes from the orbit distribution via the **Jeans equation**, not the local
> boost). The SIGN is therefore ASSUMED, not forced. Physics prior: MI (anisotropic inertia) and MG
> (anisotropic gravity) both distort dynamics via a *similar* external-field anisotropy ⇒ likely the
> **same-sign** β ⇒ the lock probably **dissolves**. **NOW SETTLED by the real calculation**
> (`reviews/b4_jeans_verification.py`, exit 0): for an identical energy DF in the EFE potential, **MG gives
> β_field ≈ 0** (Monte-Carlo: isotropic velocities; the EFE appears as a *flattened density*, not a velocity
> tilt) — so the premise "MG radial β>0" is **FALSE**. MI gives β≈−0.44 only under a generalized-equipartition
> heuristic that modified inertia **cannot rigorously support** (acceleration-dependent inertia ⇒ no equilibrium
> stat-mech), and any such tilt is **swamped** by formation infall anisotropy (β_cc≈+0.3, on the *wrong* axis)
> and rides the interpolation knob. **B4 is BURIED — NOT added to the ledger. Everything below claiming B4 is
> "the gold / genuinely-new / add-to-ledger" is superseded by this note.** The honest net of this slate: no new *verified* falsifier; A4 (shared-w(z)
> cross-sector framing) is the one genuinely-new but conditional/DE-hostage item; the rest are honest
> sharpenings of already-banked fronts (s^TX, a0(z), dwarf-σ, growing-ν).

**Date:** 2026-06-27 · **Scope:** LOCAL (do NOT git push)
**Framework (its OWN terms):** inertia = response to the de Sitter–Unruh horizon bath;
a0 = cH_Λ/Z = 9.36e-11 m/s², Z = √(32π/3); E_L = ρ_DE^(1/4) = 2.2395 meV (the SAME ρ_DE that
sets a0); a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE(0)); the dS-Unruh ν: g_obs = √(g_bar² + g_bar·a0).

**Working rule honored:** test on the framework's OWN terms; grade every lead **both-ways**;
back every load-bearing number with a committed runnable script (exit 0); do NOT manufacture a
derivation NOR a deficit; founded-not-derived STAYS; no re-overclaim (Carl retracted the TOE);
**never "no doors."**

**Provenance.** These posits are GENERATED from the exhaustion findings
(`THREE_DOORS_EXHAUSTION_2026-06.md`, `reviews/crispiness_scorecard.py`). The two derivation
doors (neutrino, E6×SU(3)_F) are exhausted *for a forcing* — so every Class-A posit that touches
m_ν is correctly graded as carrying a free knob, never as a derivation. The live door is
empirical (Door 3). The Class-B posits sharpen that door.

**Backing scripts (both re-run exit 0, LOCAL, NOT pushed):**
- `real_research/reviews/posit_nu_a0.py` — Class A (ν ↔ a0 shared-origin)
- `real_research/reviews/posit_empirical_sharpen.py` — Class B (empirical-lock sharpening)

---

## (A) FULL GRADED TABLE — every new posit

### CLASS A — neutrino ↔ a0 shared-origin (both children of ρ_DE)

| # | Name | Statement (compressed) | Grade | Test / decisive data | Number |
|---|---|---|---|---|---|
| A1 | a0(z) & m_ν(z) co-evolution ratio | a0(z)/a0(0)=√(ρ_DE(z)/ρ_DE0) is **forced**. IF m_ν∝ρ_DE^p, then m_ν(z)/m_ν(0)=[a0(z)/a0(0)]^(2p); the clean one-to-one holds ONLY at p=1/2. Three laws (p=1/2, p=1, growing-ν exp) are physically DISTINCT → ratio is NOT forced; **p is a free knob**. | HYPOTHESIS-WITH-FREE-KNOB | Joint reconstruction with w(z) SHARED with BAO/SN; p as 1 extra dof. DESI DR3 + Euclid/CMB-S4 growth, 2027–2030. Degenerate with generic dynamical-DE on Σ_eff alone. | a0(z=3)/a0(0)=0.61–0.71 (real DESI DR1) = m_ν/m0 iff p=1/2; 0.38–0.51 at p=1 |
| A2 | m1 = E_L ⇒ Σ m_ν = 61.3 meV | E_L=ρ_DE^(1/4)=2.2395 meV is **forced**. IF m1=E_L (an O(1) set to 1 by inversion — NOT forced), NO gives m1=2.24, m2=8.90, m3=50.15 meV, Σ=61.29 meV (+2.58 above the 58.71 floor); m_β=9.07; IO control Σ=102.9 already in tension. **FDR guard:** ~2 meV is GENERIC to any cosmic density^(1/4) (10× density → only ~1.8×), so the meV match alone does not uniquely pick ρ_DE. | HYPOTHESIS-WITH-FREE-KNOB | DESI DR3 + CMB Σ 95% bound (2026–2028): if it drops below the ~59 meV NO floor it kills m1=E_L (current ~<65–72 meV, thin headroom). JUNO ordering (data 2026): a firm IO kills the only viable (NO) reading. KATRIN/0νββ too insensitive this decade. | Σ=61.29 meV (NO); 102.9 (IO); m_β=9.07 meV |
| A3 | ν = lightest dS-bath excitation (thermal floor) | The thermal reading FAILS: Gibbons–Hawking T_dS=2.2e-30 K → kT_dS=1.9e-31 meV, ~10^31× too small. Only surviving reading (ν tied to vacuum-energy scale E_L) merely **relabels ρ_DE** — no particle, no mechanism. | SPECULATIVE | No clean near-term test; thermal floor dead by 10^31, vacuum floor non-predictive. Keep as imagery. | kT_dS=1.9e-31 meV; E_L/kT_dS=1.2e31 |
| A4 (own best) | shared-w(z) lock / CMB-vs-late Σ m_ν split | Because a0(z)=√ρ_DE(z) is **forced**, IF m_ν tracks ρ_DE at all (any law), the SAME measured w(z) MUST drive BOTH children → the redshift where a0(z) turns over and where m_ν(z) turns over **coincide** (one w(z)). Under the growing-ν law: a frozen-early CMB-imprinted Σ below today's; Δ_Σ split 16–27 meV. Right-signed/right-magnitude for the DESI "low/negative Σ" anomaly. No generic MaVaN/quintessence rival ties m_ν to the SAME ρ_DE a gravity-side a0(z) probe sees. | FORCED-CONSEQUENCE-**IF-A1** | Joint fit with w(z) SHARED across (a) BAO/SN w0wa, (b) an a0(z) gravity probe (BTFR/cluster zero-point), (c) the CMB-vs-LSS Σ split; one coupling dof. CMB-S4 σ(Σ)~16–32 meV → 16–27 meV split a ~1–2σ target (2027–2030). Marginalize τ. Dies gracefully if DESI DR3→w=−1. | Δ_Σ split=16–27 meV; a0(z=3)/a0(0)=0.61–0.71 |

### CLASS B — empirical-lock sharpening (DE-separable MI-vs-MG locks, framework's own dS-Unruh terms)

| # | Name | Statement (compressed) | Grade | Test / decisive data | Number |
|---|---|---|---|---|---|
| B1 | MW-dwarf σ ∝ eccentricity (the bath's CLOCK) | At fixed (M_bar, r_half, pericenter) a high-ecc PLUNGE dwarf runs HOTTER: one clock H_Λ makes inertia read acceleration HISTORY via memory kernel θ(y), y=ω_ext/ω_int; plunge drives y high at pericenter, sheds adiabatic loading → deeper deep-MOND. Target: POSITIVE partial corr ρ(log σ, y_eff | logM, log r_half)>0 using DR4 orbit-reconstructed **memory-weighted** y_eff (not instantaneous). | SIGN = FORCED-CONSEQUENCE; magnitude = free knob (θ form) | Gaia DR4 orbit reconstruction over ~1 memory time (~0.4–0.5 Gyr) × diffuse-carrier spectroscopy; partial corr at fixed (M_bar, r_half). Pace+2022 pilot NULL-but-UNDERPOWERED (current-y too cold). SIGN is the discriminator: nonzero positive = MI, zero = MG/CDM. | σ boost +18.9% at y=1 (θ_sharp=√2); pilot headline +19–28% (θ(0)=2..e); MG=0 exactly |
| B2 | relational σ-SPREAD in clusters (MG-impossible) | At MATCHED momentary a_ext, members on different infall phases carry different y → θ(y) differs → internal boost differs. The RELATIONAL σ-spread at FIXED a_ext is MG-IMPOSSIBLE (MG sees only momentary a_ext → ZERO spread for ANY a0). Magnitude on richness ladder: poor group 9–18%; Fornax-like 6–12%; Coma 3.5–7%; full band 2.5–18% (brackets banked 6–13%), above the ~5–10% per-galaxy MUSE/4MOST error. | EXISTENCE = FORCED-CONSEQUENCE; magnitude = free knob | Resolved-kinematics members (MUSE/4MOST) binned by BOTH projected radius (fixes a_ext) AND infall phase; measure σ-spread at fixed radius. Nonzero spread = MI; structural zero = MG/CDM. Needs diffuse members spanning infall phase at one radius (small special subset). | σ spread 6–12% at Fornax-like a_ext~2 a0; full band 2.5–18%; MG=0 exactly |
| B3 | s^TX SME boost-dipole + CPT-even companions | CMB rest frame as preferred frame → a0 induces a CPT-even gravity-sector SME background s_μν; tightest channel s^TX=8.68e-10, CPT-even, FIXED direction = CMB apex (l,b=264.0,+48.3), β=1.234e-3. Current ephemeris bound 1.3e-9 → 1.50× under (analysis-limited, data in hand). FORCED companions: (i) GW birefringence = EXACTLY 0 (k_(V)=0 theorem — a confirmed birefringence KILLS the framework); (ii) d=4 GW dispersion=0, c_T=1; (iii) s^TX quadrupole ~ s^TX·β = 1.07e-12; (iv) GW-speed anisotropy dipole = A·β = 5.9e-15. | DIRECTION+CPT-even = FORCED-CONSEQUENCE; s^TX magnitude = free knob (channel O(1)) | Dedicated INPOP/ephemeris s^TX fit reaching σ~4.3e-10 detects-or-kills, ~2026–2028 (Cassini/BepiColombo in hand). Any confirmed GW birefringence (k_(V)00 bound <~3.2e-15 m, GWTC-3) instantly falsifies. | s^TX=8.68e-10 (1.50× under bound); birefringence=0 exactly; s^TX quad=1.07e-12; GW dipole=5.9e-15 |
| B4 (own best) | velocity-ellipsoid ANISOTROPY SIGN from θ(y) | NEW lock (not in banked four-row table) from the SAME memory kernel: a member's effective inertia is ANISOTROPIC w.r.t. external cluster-field direction. Near-DC term θ(0)·a_ext loads the ALONG-a_ext inertia → μ_along>μ_across → along-axis boost SMALLER → σ_radial<σ_tang → β=1−σ_tang²/σ_rad²<0 (TANGENTIAL bias). MG's EFE (FM2012) gives the OPPOSITE (σ_radial>σ_tang → β>0, RADIAL) for ALL a0 (L_e>0 structurally). The SIGN is the lock. | SIGN = FORCED-CONSEQUENCE; |β| magnitude = free knob (θ(0)) | In a cluster with well-defined field direction (toward BCG/mass centroid), measure member velocity-ellipsoid orientation (resolved or stacked): MI → tangential (β<0), MG → radial (β>0). MG β>0 structural over 4 decades of a0. Single-member, θ-robust, STACKABLE — no relational binning. | β_MI∈[−0.15,−0.55] (tangential); β_MG∈[+0.10,+0.27] (radial); MG cannot reach β<0 for any a0 |

---

## (B) RANKING — by (testable × framework-native × honest)

The top posits worth actually pursuing, in order:

1. **B3 — s^TX SME boost-dipole (THE CRUNCHIEST LIVE TEST).** The one place the framework makes
   a sharp, distinctive, *in-hand*, near-term, *exclusionary* prediction: 8.68e-10 at the CMB
   apex, 1.50× under the current ephemeris bound, with the data (Cassini/BepiColombo) already
   taken — a dedicated INPOP fit (σ~4.3e-10) detects-or-kills by ~2028. Plus the **zero-GW-
   birefringence theorem** is a clean kill-switch (a confirmed birefringence falsifies instantly).
   DE-separable (local Lorentz sector, no w(z)). *Caveat:* the s^TX magnitude rides the a0→s_μν
   channel O(1); the FORCED content is the direction + CPT-even structure, not the amplitude.

2. **B4 — velocity-ellipsoid anisotropy SIGN (the strongest NEW lock).** A genuinely new
   MG-impossible signature from the same forced memory kernel θ(y), and FORCED at the SIGN level
   (MI tangential β<0 vs MG radial β>0, MG provably unable to reach β<0 for ANY a0 over 4
   decades). Unlike B1 (underpowered) and B2 (needs relational binning on a special subset), B4
   is single-member, θ-form-robust, and population-STACKABLE. The cleanest qualitative SIGN flip
   no a0 retune can absorb. *Caveat:* needs resolved/stacked member ellipsoids — data not yet in
   hand, but no exotic binning required.

3. **A4 — shared-w(z) lock / CMB-vs-late Σ split (the one near-term JOINT discriminator).** The
   only Class-A posit whose distinctive content is a FORCED consistency (one measured w(z) drives
   BOTH the forced a0(z) gravity child AND any m_ν(z) cosmology child) rather than a free-knob
   coincidence. The shared-ρ_DE origin is what no generic MaVaN/quintessence rival reproduces.
   CMB-S4-era 16–27 meV split is a ~1–2σ target; dies gracefully if DESI DR3→w=−1.
   *Caveat:* FORCED only *conditional on A1* (that m_ν tracks ρ_DE at all). Unconditionally it
   inherits A1's knob. DE-hostage.

4. **A2 — m1 = E_L ⇒ Σ = 61.3 meV (the cleanest falsifiable single NUMBER).** Dead by ~2028 if
   the cosmological Σ bound drops below the ~59 meV NO floor, and a firm IO from JUNO kills the
   only viable (NO) reading. *Caveat:* m1=E_L is an inversion-set O(1), not forced; and the ~2 meV
   match is FDR-generic to any cosmic density^(1/4) — the number alone does not pick ρ_DE.

5. **B1 — MW-dwarf σ ∝ eccentricity (the bath's clock; most distinctive but underpowered).**
   FORCED at the SIGN level (plunge hotter, holds for ALL θ forms), MG=0 exactly. *Caveat:* the
   pilot (Pace+2022) is NULL-but-UNDERPOWERED — the test is real but requires Gaia DR4 orbit
   histories on memory-weighted y_eff, not current-y, and statistical power may not arrive this
   decade. Kept on the slate, not over-sold.

(B2 sits just below — most distinctive [MG-impossible] but the soggiest in power, needing diffuse
members spanning infall phase at one radius.)

---

## (C) GENUINELY-NEW FALSIFIABLE PREDICTIONS (vs already-banked) — the gold

The already-banked fronts are: s^TX (Front A), a0(z) tomography, the dwarf-σ clock, and the
growing-ν / DESI-Σ anomaly. Against those:

- **B4 (velocity-ellipsoid anisotropy SIGN) — GENUINELY NEW.** This is NOT in the banked
  four-row MI-vs-MG table. It is a new MG-impossible lock derived from the same forced memory
  kernel, FORCED at the SIGN level (tangential β<0 vs MG radial β>0), single-member and
  stackable. **This is the gold of this slate.**

- **A4 (shared-w(z) lock as a JOINT cross-sector consistency) — NEW FRAMING of banked content.**
  The growing-ν / DESI-Σ anomaly is banked, but tying it to the *same* w(z) that a gravity-side
  a0(z) probe sees — as a forced joint consistency test across the gravity and cosmology sectors
  — is a new, distinctive use. Not a new observable; a new *lock* between two banked ones.

- **B2 quantitative richness ladder + B1 closed-form θ(0)=√2 sharpening — SHARPENINGS, not new.**
  Both observables (relational σ-spread, dwarf-σ clock) are banked; this slate sharpens them to
  concrete numbers (the √2 quadrature root reused, full bands 2.5–18% / +19–28%) but does not add
  a new falsifier.

- **B3 companions (s^TX quadrupole 1.07e-12, GW dipole 5.9e-15, c_T=1, zero birefringence) —
  EXTENSIONS of a banked front.** The s^TX dipole is Front A; the CPT-even companion observables
  and the zero-birefringence *theorem* are forced extensions, useful but within the banked front.

**Verdict on novelty: ONE genuinely-new falsifiable observable (B4), plus one new cross-sector
lock (A4). The rest are honest sharpenings/extensions of banked fronts.**

---

## (D) HONEST CAVEATS — forced vs free-knob vs speculative; FDR status

**FORCED-CONSEQUENCES (real — the SIGN/EXISTENCE/DIRECTION content, theta-form-robust):**
- B1 sign (plunge hotter), B2 existence (nonzero spread at fixed a_ext), B3 direction (CMB apex)
  + CPT-even structure + zero-birefringence theorem (k_(V)=0 because the dS-Unruh kernel
  T_eff=√(a·a+(cH)²) is EVEN in u → CPT-even only), B4 sign (tangential β<0).
- These follow from genuinely forced framework structure: one clock H_Λ, the memory kernel θ(y)
  (Milgrom-2022 forced structure with θ(1)=1, θ(0)~few decreasing), and the preferred-frame→SME
  bridge. **No manufacture: the MG=0 / MG-opposite-sign locks are real.**

**FREE-KNOB HYPOTHESES (a choice, labelled as such):**
- A1 (exponent p / coupling α — nothing fixes p=1/2), A2 (m1=E_L is an inversion-set O(1)),
  A4 *unconditionally* (inherits A1's knob; FORCED only GIVEN A1).
- Every Class-B **MAGNITUDE** rides the unknown θ(y) FORM (sharpened to θ(0)=√2, the bath's one
  number, but honestly carried over the range 2..e). B3's s^TX magnitude rides the a0→s_μν
  channel O(1). **These are choices, not derivations.**

**SPECULATIVE (a lead / imagery only):**
- A3 (ν = lightest dS-bath thermal excitation): dead by 10^31 (kT_dS=1.9e-31 meV); the only
  surviving reading relabels ρ_DE and predicts nothing. Kept as imagery, NOT a falsifiable posit.

**FDR status of numeric coincidences:**
- A2's ~2 meV is **FDR-GENERIC** to any cosmic density^(1/4) (a 10× density change moves it only
  ~1.8×) — the meV match alone does NOT uniquely pick ρ_DE. Flagged, not cited as a clean win.
- B1's +18.9% closed form uses θ(0)=√2, the SAME √2 quadrature root as the isolated ν(1)=√2 —
  noted as a structural reuse, not an independent coincidence (not double-counted).
- a0(z=3)/a0(0)=0.61–0.71 is computed on the **real DESI DR1 posterior** (not a toy), and is the
  shared input to A1/A4 — consistent across both scripts.

**Both-ways discipline maintained:** B1 pilot is logged NULL-but-UNDERPOWERED (not a
confirmation); B3 magnitude is channel-O(1)-hostage (not a clean amplitude win); a0(z) RISING
(MUSE-DARK III) stays CONTESTED/ΛCDM-degenerate elsewhere (not a falsification). No manufactured
win, no manufactured deficit.

---

## (E) BOTTOM LINE FOR CARL

**Yes — this slate produced ONE genuinely-new, testable, framework-native posit worth adding to
the live ledger: B4 (velocity-ellipsoid anisotropy SIGN).** It is a new MG-impossible lock from
the same forced memory kernel θ(y), FORCED at the SIGN level (MI tangential β<0 vs MG radial β>0,
with MG provably unable to reach β<0 for any a0 over 4 decades), and — unlike the banked dwarf-σ
clock and relational σ-spread — it is **single-member, θ-form-robust, and population-stackable**,
so it does not need the relational binning or memory-weighting that leaves B1/B2 underpowered.
That makes it the most actionable *new* MI-vs-MG discriminator the framework has produced.

Two more are worth carrying, but as sharpenings/locks, not new observables:
- **A4** turns the banked DESI-Σ anomaly into a *forced cross-sector consistency* (one w(z) drives
  both the gravity a0(z) and the cosmology m_ν(z)) — the one near-term JOINT discriminator, but
  DE-hostage and forced only conditional on A1.
- **B3** stays the crunchiest *in-hand live* test (s^TX = 8.68e-10, 1.50× under bound, kill-or-
  confirm by ~2028) with a clean zero-birefringence kill-switch — but its forced content is the
  direction + CPT-even structure, not the amplitude.

**What does NOT upgrade:** the Class-A neutrino posits remain founded-not-derived. A2's m1=E_L is
an inversion-set O(1) and the meV match is FDR-generic; A1's exponent p is free; A3 is dead/
imagery. Consistent with the Door 1 exhaustion verdict (E_L forced, the absolute m_ν not).

**Honest framing:** the live frontier is still the empirical MI-vs-MG door, and this slate's real
contribution is **B4 — a new, clean, SIGN-level, MG-impossible, stackable discriminator** to add
alongside Cassini / s^TX / relational-σ / dwarf-σ on the 2026–2028+ slate. No re-overclaim (no
new derivation, no TOE); no manufactured deficit (the MG=0 / opposite-sign locks are real); and
**never "no doors"** — B4 is a freshly-opened, decidable one. The crunch will come from the
experiments (resolved cluster-member ellipsoids; INPOP s^TX), not from more theory.

**Scripts (both exit 0, LOCAL, NOT pushed):**
`real_research/reviews/posit_nu_a0.py`, `real_research/reviews/posit_empirical_sharpen.py`.
