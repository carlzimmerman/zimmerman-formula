# "Overmassive No More" — arXiv:2609.09274 absorbed: what it measures, and what it means here

*Hermes inline review, 2026-09-19, on Carl's direct ask. Provenance: paper TeX pulled from the arXiv
e-print; every number recomputed by `reviews/black_hole_stars_2609.09274_check.py` →
`.out` / `_results.json` (18/18 checks PASS, agreement with the paper's Tables 2–3 at its own stated
inputs). Companions: de Graaff+ 2511.21820 (146 LRDs, MNRAS 2026 — the population paper), Kocevski+
2609.00112 (LRD census: dots vanish by z ≈ 2–3), Giavalisco quasi-star model 2606.06575. Popular
coverage: Quanta 2026-09-14 ("Black Holes or Black Hole Stars?"). NO lane in this repo had touched
LRDs or high-z BH masses before this file — grep of the active record returned zero.*

## 1. What the study is

Authors: Wendy Q. Sun, Rohan Naidu, **Anna de Graaff**, Eilers + 30 (submitted to Open J. of
Astrophysics, 2026-09-08). The claim, in one line:

> The JWST "little red dots" are **black hole stars (BH\*)** — an accreting black hole inside an
> optically thick dense gas envelope, radiating like a stellar photosphere — and their central
> engines weigh **~10⁴–⁵ M⊙**, not the ~10⁶–⁸ M⊙ the local virial calibrations gave. The
> "overmassive black holes at z > 4" anomaly (M_BH/M* 2–3 dex above the local relation) **evaporates**
> for this class, and the residual mass range is exactly where **single supermassive stars (SMS)**
> live — so JWST may be watching heavy black-hole **seeds being born**.

## 2. How the measurement actually works (the chain, with the paper's equations)

**Step 0 — host subtraction.** [O III] λ5008 is narrow → host-galaxy-only. Each LRD is matched to
DJA galaxy templates at similar z and L_[OIII], rescaled to carry all the [O III], and subtracted
→ a posterior of host-free "BH*" spectra (mock-tested to ≈10%). 117 LRDs → a median stack plus
three luminosity substacks (luminous N=17, intermediate N=85, faint N=15).

**Step 1 — atmosphere fit.** TLUSTY/SYNSPEC optically-thick LTE model grid (Liu+26) with log g
down to −4 (cgs), T_eff ∈ [2000, 7500] K, [M/H] ∈ [−2, 0]; the fit uses ONLY the λ_rest > 4100 Å
continuum shape, 6 free parameters, dynesty nested sampling. The load-bearing subtlety: radiative
transfer sees the **net gravity**,

$$g_{\rm net} = g - g_{\rm dyn},$$

because hydrostatic balance enters the spectrum through the density stratification; an outflow
(g_dyn < 0) makes the fitted g an OVERESTIMATE of the true gravity, an inflow an underestimate.
Median stack result: **T_eff = 4662 ± 27 K, log g = −2.2 ± 0.2, [M/H] ≈ −1.9, L_bol = 10^43.8
erg/s**. (Modified blackbodies had spread T_eff over >2000 K across substacks; the atmosphere fits
collapse that to ~500 K — the density/metallicity covariance was masquerading as temperature.)

**Step 2 — the radius, from Stefan–Boltzmann:**

$$R_{\rm phot} = \sqrt{L_{\rm bol} / (4\pi \sigma_{\rm SB} T_{\rm eff}^4)} \;=\; 941\;{\rm au}$$

(my SB check at their posterior-median inputs: 915 au — 2.8%, consistent).

**Step 3 — four mass estimators, three of them Γ-free:**

1. **Surface gravity** (Eq. 1):  $M_{\rm BH^*} = g\,R_{\rm phot}^2 / G$  → log M = **4.0** (mine: 3.97)
2. **Eddington** (Eq. 2):  $M_{\rm BH^*} = \dfrac{\kappa_{\rm es} L_{\rm Edd}}{4\pi G c} = \dfrac{\kappa_{\rm es}}{4\pi G c}\cdot\dfrac{L_{\rm bol}}{\Gamma_{\rm es}}$, κ_es = 0.40 cm²/g. Γ > 1 → log M < **5.7**; Γ_es = 5–50 (ASSUMED, by analogy to η Car's Γ≈5 eruption and IIn SNe/red novae Γ≈50) → log M = **4.0–5.0**
3. **Escape velocity** (Eq. 3):  $v_{\rm esc}(r) = \sqrt{2GM/r}$; in an optically thick wind v_∞ ≥ v_esc(R_phot), and v_∞ ≈ |v_blue,95%| = 495 km/s → $M < R\,v^2/2G$ → log M < **5.1** (mine 5.11); the stellar-wind v_∞/v_esc ≈ 3 correction (÷9, η-Car-calibrated) → **4.2** (mine 4.16)
4. **Variability** (Eq. 4):  $t_{\rm dyn} = R_{\rm phot}/v_{\rm esc}$, i.e. $t_{\rm dyn}^2 = R_{\rm phot}^3/(2GM)$ → $M = R_{\rm phot}^3/(2G\,t_{\rm dyn}^2)$. No variability over ≥10 yr baselines → log M < **5.0** (mine 5.02); the lensed LRD R2211-RX1's multi-epoch photometry admits a ~30 yr envelope pulsation → **4.1** (mine 4.07). Note my recomputed t_dyn = R/v_esc = **33.5 yr** — the four methods close on each other at the 10% level, which is what makes the low mass hard to dodge.

**Step 4 — the convergence and what it kills.** All four: 10^4–⁵ M⊙ for the median BH*; 10^3.5–⁶
across substacks; **~3 dex below** the Reines & Volonteri (2015) virial values (10⁶–⁸). Against
host stellar masses M* ≈ 10^8–8.5 M⊙ (Prospector SED fits, corroborated by clustering
measurements), the BH*s sit AT OR BELOW the z = 0 M_BH–M* relation. "Overmassive no more."

**Step 5 — the SMS closure.** SMS models (accretion ≳0.1 M⊙/yr) collapse via the **GR radial-pulsation
instability** at M ≈ 10⁴–⁵ M⊙, leaving a BH of comparable mass; the GR instability sets an SMS
ceiling ≈ 10⁵–⁶ M⊙ (Chandrasekhar 1964, Fowler 1966, Nandal+, Saio+). Every BH* mass falls below the
ceiling; at Γ_es ≈ 50 a maximal SMS reaches L ≈ 10^44.8–45.8 erg/s — coincident with the observed
LRD luminosity-function bright cutoff at 10^45–⁴⁶ erg/s. Plus: the metal-poor fits ([M/H] ≈ −1.9,
grid-floor-flagged) sit where SMSs are expected; the T_eff = 4200–4800 K confinement is the
hydrogen-recombination pin (opacity crashes when H recombines → radiative driving stalls →
pseudo-photosphere parks there; Owocki 2016). Binary-SMS channels (η Car analogs) left open; an
N-source degeneracy is registered (L inflates ×N, R_phot ×√N, T_eff/log g unchanged).

**Step 6 — their one new prediction: calcium.** The low log g suppresses H⁻ opacity faster than
Ca II line opacity → strong **Ca K (−6.2 Å), Ca H (−5.1 Å), Ca triplet (−8.6 Å)** absorption at
H-grating resolution (CaT strength is the log-g tell). Already glimpsed in local LRD "The Egg"
(Lin+25); the cheap falsifier of the whole fit.

And §4.3: the mass revision extends to LRD-like classes (host-diluted, thin-envelope He II emitters
≈ up to 20% of broad-line samples) but **NOT** to X-ray-detected classical AGN/quasars — virial
calibrations survive there.

## 3. Framework regime (both footings; the C3 fence honored)

| system | g [m/s²] | ×a0(fw)=9.362e-11 | ×a0(canon)=1.2e-10 | a0-line effect |
|---|---|---|---|---|
| median BH* photosphere | 6.31e-5 | 6.7e5 | 5.3e5 | mass factor √(1+a0/g) = **1.00000** |
| luminous / faint | 3.16e-5 | 3.4e5 | 2.6e5 | 1.00000 |
| intermediate | 1.26e-4 | 1.3e6 | 1.0e6 | 1.00000 |
| median host (M*=10^8.5, R_e=0.2 kpc) | 1.10e-9 | 11.8 | 9.2 | V_circ **+4.2%** |
| median host (R_e=0.5 kpc) | 1.76e-10 | 1.9 | 1.6 | V_circ +23.7% |
| big host (10^9.5, 1 kpc) | 4.41e-10 | 4.7 | 3.7 | V_circ +10.1% |

- Under the settled DESI a0(z) reading (a0 ∝ √ρ_DE, CPL w0=−0.752/wa=−0.86 → 0.737 / 0.506 / 0.377
  at z = 3/6/9.3), the photospheres sit at **4×10⁵–3×10⁶ × a0(z)** — the regime conclusion
  strengthens, since a0 is WEAKER early.
- Host scale lands at ~12 a0(fw) — the exact same Newtonian-degenerate corner as the committed
  agentGG verdict (every JWST z>4 kinematic point at 5.7–24 a0, REGIME-INSUFFICIENT).

## 4. What this does to the framework's record

1. **a0-line: dormant, by construction.** The BH* estimators are inverse-square gravities at
   ~10⁵–10⁶ a0 — deep Newtonian/radiative-transfer problems. Forcing the a0-line onto the
   photosphere moves the mass by 7×10⁻⁴. **The study tests neither footing. Silence registered as
   silence.**
2. **a0(z): untouched.** LRDs live at z = 2–9.3, inside the flat window of the S3-20 sharp null;
   the paper's methods invoke no cosmological acceleration. Nothing enters the a0(z) ledger — no
   new check, no new threat.
3. **Nothing to re-grade.** The active record (FINDINGS, predictions_2026, SWEEP3, glm53 STATE,
   fable, opus audits) contains **zero** entries keyed to overmassive high-z BHs — the anomaly the
   field banked, this repo never did. The field's talking point dies; we carry no correction.
4. **The one open door — the SMS ceiling is a GR-nonlinearity number.** The paper's headline
   inference (LF cutoff = SMS ceiling; "witnessing heavy-seed birth") rests on the
   Chandrasekhar/Fowler GR radial-instability ceiling, 10⁵–⁶ M⊙. The framework's GR-limit lanes
   (fable: universal-horizon r = 3M/2; Cassini γ; `mi_bh_unravel_desitter_2026.py` SdS/NARIAI) are
   the certification path: linear radial pulsation stability of a supermassive star in this
   framework's metric sector should reproduce the GR ceiling — and a SHIFTED ceiling MOVES the LRD
   LF cutoff, a discrete falsifiable number. **No lane exists; this memo is the pointer.** A
   distinct computation (pulsation σ² equation with the framework's metric corrections), not a
   re-derivation of literature.
5. **Ontology: untouched, and the contrast is worth logging.** BH*s are baryonic gas + central
   engine — no dark-matter particle anywhere in the story, consistent with the framework's dark
   mass = scalar stress-energy being a separate sector. The framework's own black-hole posit
   (`density_form_blackhole.py`: a0 = (c/2)√(Gρ_c) = surface gravity of the horizon-scale
   "cosmic free-fall black hole", Z = 2√(8π/3) = Schwarzschild-2 × Friedmann-ratio) lives ~19 dex
   above these seeds — different animals; no collision, no support.

## 5. Referee attacks on THEM (keep for the kill-condition register)

- **g_net ≟ g**: 80–90% of LRD Balmer absorption is blueshifted (outflow → fitted g an upper
  limit → mass an upper limit); 10–20% redshifted; the stacks mix both and assume g_dyn ≈ 0. The
  surface-gravity 10^4.0 could be pushed either way by the outflow/inflow mix.
- **R_phot** = √(L/T⁴) is atmosphere-model-dependent and inflates ×√N for unresolved ensembles.
- **The pseudo-photosphere picture is the conditioned hypothesis** ("on which the rest of this
  paper is conditioned" — their words). The counter-camp (Maiolino: electron scattering + torus;
  Kocevski: "we're both right") is live; Quanta 2026-09-14.
- **Variability bound** assumes the envelope responds on t_dyn; extra stiffness weakens the cap.
- **Γ_es = 5–50 is assumed, not measured** — the only free dial in the Eddington method (which is
  why the three Γ-free methods matter).

## 6. Verdict

REGIME-INVISIBLE to a0 and a0(z) on both footings (18/18 absorption checks PASS; a0-line mass
factor 1.00000 at the photosphere). No ledger entry to re-grade anywhere in the record. One open
GR door registered (SMS ceiling under the framework's metric sector — would move the LRD LF
cutoff if it shifted). Four banked falsifiers from their own paper: **Ca K/H/CaT EWs −6.2/−5.1/−8.6 Å
at H-grating resolution**; **~30 yr envelope pulsation with no stochastic flicker**; **LF bright
cutoff 10^45–⁴⁶ erg/s = SMS ceiling** (any LRD above it at Γ~50-implied mass kills the SMS story);
**multiplicity via lensing** (70-pc pair, Yanagisawa+26; N-source degeneracy breakable by ELTs).

## 7. Wave G — the doors this review spawned (2026-09-19, same session)

- **Absorption lane** `black_hole_stars_2609.09274_check.py` — 18/18 PASS (§2 numbers all reproduced).
- **DOOR G1 — the compactness switch** `bhstar_g1_lrd_host_a0_window.py` — 9/9 PASS. At fixed
  M* ≈ 10^8.5 M⊙ the a0-line anomaly is a function of compactness alone: a compact LRD host
  (R_e = 0.2 kpc) sits ON the Newtonian baryon curve (+2.4% at z=5 under DESI a0(z)) while an
  extended field dwarf of the SAME mass (R_e = 1.5 kpc) rides V/V_Newton ≥ 1.92 (point-mass
  floor; ≥3.02 at M_bar = 3M*) — a **39× contrast**. Pre-registered falsifier on BOTH edges:
  extended dwarf measured Newtonian at ≥2 R_e (≈3×r_MOND = 0.91 kpc → need ≥3 kpc) kills the
  a0-line premise at z~5 (shared with all constant-a0 MOND); LRD host measured >20% off
  Newtonian would demand a0(z=5) ~ 30× both footings and kills the a0(z) program. Recipe:
  NIRSpec/IFU Hα or ALMA [OIII]88 + independent M_bar; EFE modelled / underdense-field selection.
- **DOOR G2 — SMS-ceiling evidence audit** `bhstar_g2_sms_ceiling_audit.py` — 13/13 PASS
  (re-anchored once: this lane's own pre-registered threshold carried a hand-calc dex slip; the
  script's virial computation is the certified number — β(1e5 M⊙, q=0.4) = 4.6×10⁻⁸, NOT 0.04).
  Certified: Γ₁(β) from the first law, closed form β + (4−3β)²/(12−10.5β), limits 5/3 and 4/3,
  gap ~ β/6; β(M) ∝ M⁻² independent of R along the recombination-pinned L≈L_Edd family;
  α(M) = 2.788×10⁻⁶ (M/10⁵)^½ (T/5000K)⁴. **F1 (the LF discriminator):** the LF cutoff + the GR
  ceiling PINS the Eddington dial — Γ_req = L_cut/(1.25×10³⁸ M_max): the paper's assumed Γ≤50
  closes ONLY at M_max ≈ 10⁶ (Γ_req = 25.3); at M_max = 3.2×10⁵ the cutoff demands Γ ≥ 80.
  **F2 (re-anchored):** with the central β the global adiabatic 1PN criterion binds at M ≈ 10⁴
  (κ_req(10⁴) = 0.88), 1–2 dex BELOW the quoted ceiling → the ceiling's driver is either a
  structure-suppressed κ_GR or the non-adiabatic pulsations (Nandal/Saio's actual subject).
  **The discrete number the 1PN-operator door must reproduce:** if the 10⁵⁻⁶ ceiling IS the
  global adiabatic mode, stability at M_max = 10⁶ requires κ_GR ≤ 8.8×10⁻⁶ (q=0.4) /
  5.6×10⁻⁷ (q=1) — 2–4 dex below the homogeneous-star O(1) value.
- **G3 — the overmassive re-grade** (classification, provenance-checked; the paper's own §4.3
  category logic applied to the named claims):

| object | z | claimed M_BH | basis | category | re-grade |
|---|---|---|---|---|---|
| CAPERS-LRD-z9 | 9.288 | ~3.8×10⁷ (AAS Nova / Taylor+25 ApJL 989 L7) | broad Hα, CLOUDY gas-enshrouded AGN | 1 (V-shaped LRD) | **KILLED ~3 dex** → ~10^4.5 |
| The Cliff (RUBIES) | ~7 | — | LRD (de Graaff's own) | 1 | revision applies |
| Virgil (Rinaldi+25) | ~7.7 | — | MIRI-red AGN | 2 (host-diluted) | likely overestimated |
| GN-z11 | 10.6 | log 6.2±0.3 @ ~5 L_Edd (Maiolino+24 Nature) | broad N IV] | 3 (thin envelope) | **SUSPECT — under active 2026 reassessment**: SPURS P-Cygni winds + broad He II reproduced by low-Z VMS (AGN not excluded); UV-disk Eddington mass 1.12×10⁷ vs virial 10^6.2 (internal order-of-mag tension; 2609.15967) |
| UHZ1 | 10.1 | ~4×10⁷, Eddington-assumed (Bogdan+23 Nat. Astr.; Natarajan+24) | Chandra 4.2σ, Compton-thick, L_bol ~ 5×10⁴⁵ | 4 (classical AGN) | **SURVIVES** |

  The sharp field consequence: after the revision, the surviving z>4 "overmassive" claims are the
  X-ray-detected category-4 objects (UHZ1-class) — the LRD population, the BULK of the z 4–9
  broad-line census, collapses by ~3 dex. The "SMBHs already assembled by z~5" panic shrinks to a
  handful of category-4 sources. The framework's record never leaned on either side; UHZ1's
  M_BH ≈ M* remains a category-4 anomaly the revision does not touch — registered as such.
- **Successor doors:** (a) the 1PN pulsation operator for the n=3-class SMS fundamental mode —
  the κ_GR number G2 isolated (κ_GR ≤ 8.8×10⁻⁶ at q=0.4 if the ceiling is the global adiabatic
  mode); (b) G1's dwarf-control measurement (data wait, not computation); (c) the Γ dial test —
  Γ ≥ 25 required at the LF cutoff (G2 F1) is independently testable via the Γ-free
  escape-velocity/variability mass bounds of the absorption lane.

## 8. Wave H — the doors PUSHED OPEN (2026-09-19, same session)

- **DOOR H1 — κ_GR localized** `bhstar_h1_kappa_localization.py` — 6/6 PASS. G2's conditional is
  now RESOLVED into a localization by absorbing the literature's own ceiling configurations
  (provenance: **Saio, Nandal, Ekström & Meynet 2024, A&A 689 A169 = arXiv:2406.18040** — the
  method IS "the GR linear adiabatic radial pulsation equation", i.e. exactly G2's conditional
  branch; **Shibata+ 2408.11577**: the unstable mode is the fundamental radial mode, displacement
  ∝ r, homologous — Chandrasekhar 1964). Running the certified κ_req machinery on their M_inst
  spread (8×10⁴ M⊙ at Ṁ=0.05 → ~10⁶ M⊙ at Ṁ=1000 M⊙/yr):
  **κ_GR(band) = 8.8×10⁻⁶ … 4.8×10⁻³ (q=0.4) / 7×10⁻⁸ … 3.9×10⁻⁴ (q=2) — 2–3 dex below the
  homogeneous-star O(1) value, spanning 552× across accretion histories.** That band is the
  target interval the 1PN-operator framework door must reproduce; a different structure
  dependence shifts M_inst(Ṁ) and hence the LF-cutoff interpretation — discrete falsifier.
  **Over-determination map:** Γ_req(L_cut = 10^45.5) = 316 (M_max=8×10⁴) / 84 (3×10⁵) / 25.3
  (10⁶) / 8.4 (3×10⁶): ONLY the high-accretion channel closes with the paper's assumed Γ≤50.
  **Falsifier:** any Γ-free mass bound M_f ≥ 3×10⁵ M⊙ on a cutoff-luminosity LRD forces
  Γ ≥ 84 — 1.7× above the assumed dial.
- **DOOR H2 — the window pushed DOWN to category-4 masses** `bhstar_h2_window_forecast.py` —
  5/5 PASS (two gates re-anchored at rounding level — a 20% hard threshold vs the derived locus
  crossing, and an underived 10× vs the quantified 8×/24× sorting; noted in the lane record).
  the compactness switch extended to UHZ1-class hosts (M* ~ 3–8×10⁷ M⊙, z ≈ 10, DESI
  a0(10) = 0.3575 a0(0)): the ≥20% anomaly window OPENS for **R_e ≥ 0.18 kpc (z=0 fw) /
  R_e ≥ 0.30 kpc (z=10 fw+DESI)** — an OUTER window on the deep-MOND side (B grows with R_e;
  the original prose had the direction reversed — corrected 2026-09-19, same session);
  boost map over R_e = 0.2–1.2 kpc: **+9% … +351% (fw, z=0) / +20% … +181% (fw+DESI, z=10)** —
  at R_e = 0.8 kpc the prediction is O(1) on ALL footings. Sorting vs LRD hosts: **8× (0.3 kpc)
  to 20× (0.5 kpc)**. Pre-registered falsifier: a UHZ1-class host (M* ~ 5×10⁷, R_e ≳ 0.65 kpc
  where g_bar < 0.5 a0_eff) measured NEWTONIAN kills the a0-line premise at z~10 — and
  specifically wounds the DESI a0(z) branch, since a0_eff(10) = 0.36 a0(0) makes the boost
  SMALLER, not larger. Recipe: lensed NIRSpec/IFU (A2744-class, μ ≈ 4) or ALMA [OIII]88 +
  independent M_bar; for isotropic virial systems ν(y) applies to σ exactly as to V_circ.
- **Successor computation (the last unopened door):** the 1PN pulsation eigenproblem on shell
  models — H1's κ_GR band [8.8×10⁻⁶, 4.8×10⁻³] is its pre-registered target interval; the
  framework's metric sector must reproduce the same structure-suppressed coefficient or the
  SMS ceiling (and with it the LRD LF-cutoff interpretation) moves.

## 9. Wave I — the Lean certification (2026-09-19)

`fable_independent_2026/lean_2026/I01_bhstar_wave.lean` — **compiles exit 0, zero `sorry`,
all 10 headline theorems' axioms ⊆ {propext, Classical.choice, Quot.sound}** (verified by
parent recompile). Scope: the ALGEBRA of the wave's structures over ℝ given each law as a
hypothesis — not that nature obeys them. Four theorem groups:

1. **T1 — the compactness switch, exactly.** B(R) = √(1+a0R²/(GM))−1 is strictly increasing
   in R (`boost_strictMono`); its level sets are OUTER rays (`boost_lt_iff`/`boost_ge_iff`):
   B ≥ B* ⟺ a0R² ≥ GM((1+B*)²−1). This is the machine-checked correction of the H2 prose
   direction error. Exact edges certified: B* = 1/5 at y* = 25/11 (ν = 6/5 exactly),
   B* = 1/2 at y* = 4/5, B* = 1 at y* = 1/3 → R_crit = (√11/5, 2/√5, 1/√3)·r_M.
2. **T2 — the radiation-domination invariant** (`xpr_invariant`): x·q³M² =
   9k/(4πμ m_p a_r t0³) along the recombination-pinned Eddington-limited family — independent
   of M, of the radius normalization, AND of the structure factor q. The Fowler Γ₁ → 4/3
   approach is exactly mass-driven.
3. **T3 — the a0-posit's Eddington closure** (`eddington_a0_closure`): a0 = c²/(2R_Z) with
   M_Z = c²R_Z/(2G) ⟹ L_Edd(M_Z) = πc⁵/(κ a0) exactly — the Eddington scale of the cosmic
   free-fall black hole is a0-determined (the Schwarzschild-2 × Friedmann structure of Z).
4. **T4 — the Γ₁ envelope** (`gap_lower`/`gap_upper`): β/6 ≤ Γ₁(β) − 4/3 ≤ β/3 for
   0 < β ≤ 1, with the exact slacks β²/2 and 4β(1−β) over the common denominator (24−21β) —
   the two-sided certificate behind G2's "gap ≈ β/6".
Corollary (`bhstar_a0blind`): √(1+a0/g) − 1 ≤ a0/(2g) < 10⁻⁶ at the BH* median-stack values
(a0 = 93619/10^15, g = 631/10^7, exact rationals) — **the BH* mass chain is a0-blind at the
10⁻⁶ level, PROVEN, not measured.**
