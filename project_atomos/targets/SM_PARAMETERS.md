# SM_PARAMETERS — the authoritative target list for project_atomos

**Purpose.** Enumerate every free/empirical parameter of the Standard Model (+ the neutrino extension), with current
measured values and uncertainties, the known mechanism hook (if any) for each sector, and a **ranked hit-list** of where
an interlock (forced-kernel / Koide-class) is most likely to be *real* — so the engine/gate can be aimed where the prior
payoff is highest, not blindly.

**Discipline reminder (the gate is the whole project).** Every number below is a *target*, not a hint. A formula that
hits a target is worthless until it survives the three-part gate: (1) FDR survival vs the search-space size, (2) a
**forced kernel** (a coefficient pinned by symmetry/geometry *before* fitting), (3) an **interlock** (the same structure
forces ≥2 independent observables, or ties ≥3 constants with one parameter, Koide-class). Same bar both ways: do not
manufacture a win, do not high-priest a real signal.

Values are PDG-2024-class from model knowledge (cutoff Jan 2026). Each entry is flagged with a confidence tag:
**[H]** high (well-measured, stable), **[M]** medium (scheme/scale-dependent or moderate error), **[L]** low (poorly
known / unsure — verify before using as a tight target).

---

## 0. The honest count — "all 53 or whatever"

There is no single canonical integer; the count depends entirely on convention. Honest tally:

| Convention | Count | What's included |
|---|---|---|
| **Minimal SM (massless ν)** | **19** | 9 charged-fermion masses · 3 gauge couplings (g₁,g₂,g₃ ≡ α_em,α_s,sin²θ_W form) · 2 Higgs (v, m_H, equiv. μ²,λ) · θ_QCD · 4 CKM (3 angles + 1 phase) |
| **SM + Dirac neutrinos** | **26** | +3 ν masses +3 PMNS angles +1 Dirac phase |
| **SM + Majorana neutrinos** | **28** | as above +2 Majorana phases |
| **"~53" maximal accounting** | **~37 if you also add gravity** | see below |

The famous "**~53**" (sometimes "37", "44") inflates the count by **adding parameters that are *not* SM-Yukawa free
parameters**:
- **+1 gravity:** Newton's G (or M_Planck). **+1:** the cosmological constant Λ. **+1:** the Hubble/cosmology sector if
  one counts ΛCDM. (Tegmark's "31 fundamental" / the popular "26" both make choices here.)
- **+ seesaw heavy sector:** 3 right-handed-neutrino Majorana masses + the full Dirac Yukawa matrix (9 moduli + phases)
  → a high-scale UV completion can carry **18+** extra parameters that are *not* observable at low energy (they collapse
  into the 7–9 light-ν observables). This is where "53" usually comes from: SM-19 + a *fully parameterized* seesaw +
  gravity + Λ.
- Some counts add the **3 lepton + 3 baryon** accidental global-symmetry charges, or QCD's running-coupling reference
  scale Λ_QCD as a separate input (it is *not* — it is α_s at a reference scale).

**The honest statement for atomos:** the SM proper has **19** free parameters; with the observed neutrino sector it is
**26–28**; "53" is SM-19 + a *specific, non-minimal, mostly-unobservable* UV/gravity accounting. **Our target list is the
26–28 low-energy observables** — those are the only numbers a kernel could actually pin against data. We note the "53"
framing so we never confuse a UV-completion parameter (unobservable, infinitely re-parameterizable) for a target.

---

## 1. Charged-fermion masses (9) — the Yukawa eigenvalues

The hardest sector: in the SM these are **eigenvalues of free Yukawa matrices** — *no forced kernel* (the asymmetry the
zimmerman corpus already proved). Listed at conventional scales (leptons = pole mass; quarks = MS-bar, with the scale
noted, because quark "masses" are scheme/scale-dependent and **not** physical poles).

### Charged leptons (pole masses)
| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| m_e | 0.51099895000 MeV | ±1.5e-10 | **[H]** | electron pole mass |
| m_μ | 105.6583755 MeV | ±2.3e-6 | **[H]** | muon pole mass |
| m_τ | 1776.86 MeV | ±0.12 | **[H]** | tau pole mass |

Derived dimensionless targets (these are what a relation must hit):
- **m_μ/m_e = 206.7682830** **[H]**
- **m_τ/m_μ = 16.8170** **[H]**
- **m_τ/m_e = 3477.23** **[H]**
- **Koide Q_lep = (m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)² = 0.666661** (≈ 2/3, dev −9.2e-6) **[H]** ← the live interlock

### Up-type quarks (MS-bar)
| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| m_u(2 GeV) | 2.16 MeV | +0.49/−0.26 | **[L]** | light-quark, large frac. error |
| m_c(m_c) | 1.27 GeV | ±0.02 | **[M]** | charm, running mass |
| m_t (pole) | 172.57 GeV | ±0.29 | **[H]** | top pole (≈ Yukawa ≈ 1) |

### Down-type quarks (MS-bar)
| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| m_d(2 GeV) | 4.70 MeV | +0.48/−0.17 | **[L]** | light-quark |
| m_s(2 GeV) | 93.5 MeV | ±0.8 | **[M]** | strange |
| m_b(m_b) | 4.18 GeV | +0.03/−0.02 | **[M]** | bottom, running mass |

Useful within-sector dimensionless targets:
- **m_c/m_u ≈ 588**, **m_t/m_c ≈ 136** **[L/M]** (light-quark errors dominate)
- **m_s/m_d ≈ 19.9**, **m_b/m_s ≈ 44.7** **[M]**
- **m_t/m_b ≈ 41.3** **[H]**, **Koide Q_up = 0.85**, **Koide Q_down = 0.73** (both ≠ 2/3 → cross-fermion *falsifies* a
  naive cube-geometry Koide; see hook note)

**Mechanism hooks for the mass sector:**
- **Koide Q=2/3 [REAL, leptons only].** Parameter-free, FDR-surviving (~1-in-44,000), 45-yr puzzle. Geometric content:
  √-mass vector at exactly 45° to (1,1,1) ⇔ Q = 1/3 + r²/6 with r=√2. **The framework only re-labels it; r=√2 is an
  unforced interior point** (sympy-exact). The dS-Unruh IR-mechanism route is CLOSED (4 lethal legs). **This is the one
  proven interlock in the whole SM mass sector — the engine must re-find and re-certify it (calibration positive), and
  the open question is whether a *flavor-symmetry* forced kernel can pin r=√2 where the gravity spine cannot.**
- **Charged-lepton hierarchy / Yukawa textures:** Froggatt-Nielsen U(1)_FN charges generate powers of a small ε; these
  are *fitted charges*, not forced — FDR-suspect by construction.
- **m_b = m_τ at GUT scale [REAL-ish, SU(5)].** A genuine GUT relation (b-τ Yukawa unification) that *works* to ~10–20%
  after running; **Georgi-Jarlskog** factors (m_μ/m_s ≈ 3, m_e/m_d ≈ 1/3 at GUT scale) are a structured, *forced-by-
  group-theory* texture — a real forced-kernel candidate worth re-testing under the gate.
- **Proton mass m_p:** NOT a Yukawa — it is QCD dimensional transmutation (Λ_QCD/M_P = exp(−2π/b₀α_s)). The one SM mass
  with a *forced kernel* (the QCD β-function), already analyzed: m_p/m_e is NOT-derivable because it still needs y_e
  (free). Noted so we never re-open 6π⁵ (FDR-dead).

---

## 2. Gauge couplings (3)

| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| α_em(0) (fine-structure, Thomson) | 1/137.035999177 | ±2e-8 (rel ~1.5e-10) | **[H]** | low-energy |
| α_em(M_Z)⁻¹ | 127.951 | ±0.009 | **[M]** | running to M_Z |
| sin²θ_W(M_Z) (MS-bar) | 0.23122 | ±0.00003 | **[H]** | weak mixing, scheme-dep |
| α_s(M_Z) | 0.1180 | ±0.0009 | **[M]** | strong, *the* loosest gauge input |
| g₁,g₂,g₃ | — | — | — | equivalent GUT-normalized form of the above |

**Mechanism hooks:**
- **GUT coupling unification [REAL structural target].** In the MSSM g₁,g₂,g₃ meet at ~2e16 GeV; in the plain SM they
  *nearly* meet — a genuine, well-known structural hint that the 3 couplings are *not* independent at high scale. This is
  the gauge sector's analogue of a forced kernel (one α_GUT + running pins 3 low-energy values). **High-value target: a
  relation among the 3 couplings that interlocks via the β-functions is exactly the forced-kernel class.**
- **Weinberg angle sin²θ_W = 3/8 at GUT scale (SU(5)) [REAL].** A clean group-theory prediction (runs down to ~0.231).
  The *tree GUT value 3/8 is forced by the embedding* — a real forced kernel. (The 3/13 "fit" of the *running* value is
  FDR-dead — do not resurrect.)
- **α_em⁻¹ ≈ 137:** the 4Z²+3 fit is FDR-dead (5 justifications for "4", fitted −π/600). No forced kernel known.

---

## 3. Higgs / electroweak sector (2)

| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| v (Higgs vev) | 246.21965 GeV | ±0.0006 | **[H]** | = (√2 G_F)^(−1/2); sets all masses |
| m_H | 125.20 GeV | ±0.11 | **[H]** | → λ ≈ 0.129 (m_H²/2v²) |
| equiv: μ², λ | — | — | — | the two Lagrangian parameters |

Related EW observables (derived, not independent): M_W = 80.3692 ± 0.0133 GeV **[H]**, M_Z = 91.1880 ± 0.0020 GeV **[H]**,
G_F = 1.1663788e-5 GeV⁻² **[H]**.

**Mechanism hooks:** v sets the *overall scale* of every Yukawa mass but not the *ratios* (the hard part is the ratios,
which v divides out). λ ≈ 1/8-ish has spawned "near-critical / metastability" arguments (Higgs self-coupling runs to ≈0
near M_Planck) — a *dynamical* hint, not a forced number. **Low interlock prior** (these are scales, not ratios; a kernel
on a single dimensionful scale is weak unless it ties to Λ — and the a₀ work already owns the Λ↔scale tie).

---

## 4. Strong CP / θ_QCD (1)

| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| θ̄_QCD | < 1e-10 | upper bound (nEDM) | **[H, bound]** | effectively zero — "the strong CP problem" |

**Mechanism hooks:** The puzzle is *why it's ~0*, not its value. Hooks: **Peccei-Quinn / axion** (dynamical relaxation to
0 — the leading explanation), or **Nelson-Barr / spontaneous CP**. A "kernel that forces θ̄=0" would be a structural
selection rule, not a fitted number. **Distinct flavor of target:** the gate's forced-kernel test *can* apply (a symmetry
forcing exactly zero is the cleanest possible forced kernel), but there is no number to regress — so the engine is the
wrong tool; this is a symmetry-argument target, logged but **deprioritized for the search engine**.

---

## 5. CKM quark mixing (4: 3 angles + 1 phase)

Wolfenstein parameterization (the natural one — exposes the hierarchy as powers of λ):

| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| λ (= sinθ_C = |V_us|) | 0.22501 | ±0.00068 | **[H]** | Cabibbo angle |
| A | 0.826 | +0.016/−0.015 | **[M]** | |
| ρ̄ | 0.1591 | ±0.0094 | **[M]** | |
| η̄ | 0.3523 | +0.0073/−0.0071 | **[M]** | CP-violating phase |
| Jarlskog J | 3.08e-5 | ±0.13e-5 | **[M]** | invariant measure of CPV |

Standard-angle form: θ₁₂ ≈ 13.0°, θ₂₃ ≈ 2.4°, θ₁₃ ≈ 0.20°, δ_CP ≈ 66°.

**Mechanism hooks:**
- **Wolfenstein hierarchy [REAL, structured].** |V_ij| ≈ powers of λ≈0.225: V_us~λ, V_cb~λ², V_ub~λ³. This *power-law
  structure* is the forced-kernel signature — strongly suggests Froggatt-Nielsen-like charges. The numbers A, ρ̄, η̄ are
  O(1) coefficients on top (less likely kernel-forced).
- **Quark-lepton complementarity [REAL, cross-sector — high value].** θ_C + θ₁₂^PMNS ≈ 45° (Cabibbo ≈ 13° + solar ≈ 33–35°
  ≈ 45–48°). If real, this is an **interlock across two sectors** (the gate's strongest class) and points to a GUT relating
  CKM and PMNS. Worth a dedicated test.
- **GST/Gatto-Sartori-Tonin relation:** √(m_d/m_s) ≈ |V_us| (θ_C from down-quark masses). A *mass-mixing interlock* — the
  cleanest forced-kernel candidate in the quark sector: it ties a mixing angle to a mass ratio with no free parameter.
  **HIGH PRIORITY.**

---

## 6. Neutrino sector (PMNS: 3 angles + 1–3 phases; masses: 2 splittings + abs scale)

The most *symmetry-structured* sector — and where the charter's "probably geometric" instinct most plausibly lands.

### Mass-squared splittings
| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| Δm²₂₁ (solar) | 7.42e-5 eV² | +0.21/−0.20 e-5 | **[H]** | |
| |Δm²₃₁| (atm) | 2.510e-3 eV² (NO) | ±0.027e-3 | **[M]** | sign = ordering unknown |
| Σm_ν | < 0.12 eV | cosmo bound | **[L]** | absolute scale unknown |
| ordering | Normal favored ~2-3σ | — | **[L]** | NO vs IO open |

### PMNS mixing angles (NuFIT-class, Normal Ordering)
| Param | Value | Unc | Conf | Note |
|---|---|---|---|---|
| sin²θ₁₂ | 0.303 | ±0.012 | **[H]** | → θ₁₂ ≈ 33.4° (solar) |
| sin²θ₂₃ | 0.572 | ±0.018 | **[M]** | → θ₂₃ ≈ 49.1° (near-maximal; octant open) |
| sin²θ₁₃ | 0.02203 | ±0.00056 | **[H]** | → θ₁₃ ≈ 8.54° (small but nonzero) |
| δ_CP | ≈ 197° (1.2π) | ±27° | **[L]** | poorly constrained, ~ consistent w/ 0/π at ~1σ–2σ |
| Majorana α₂₁,α₃₁ | unknown | — | **[L]** | only if Majorana; 0νββ-sensitive |

**Mechanism hooks (this is the richest sector):**
- **Tri-bimaximal mixing (TBM) [REAL pattern, broken by θ₁₃].** TBM predicts sin²θ₁₂=1/3, sin²θ₂₃=1/2, sin²θ₁₃=0 — i.e.
  θ₁₂≈35.3°, θ₂₃=45°, θ₁₃=0. The data sit *strikingly close* except θ₁₃≈8.5° (the famous nonzero value that killed exact
  TBM in 2012). The *deviations from TBM* are themselves structured ("TBM + corrections"). This is a **forced-pattern**
  with a small breaking — exactly the forced-kernel-plus-perturbation signature the gate is built to certify.
- **Discrete flavor symmetries A₄ / S₄ / Δ(27) [REAL candidate mechanisms].** TBM arises naturally from A₄ (and S₄, Δ(27))
  — the leading model-building paradigm. These are *literally* the symmetry/geometry forced kernels the engine treats as
  first-class. The open question post-2012 is which group + breaking gives θ₁₃≈8.5° and δ_CP.
- **θ₁₃ ≈ θ_C/√2 [REAL-ish numerical coincidence].** sin θ₁₃ ≈ 0.148 ≈ λ/√2 = 0.159 (~7% off) — a cross-sector CKM↔PMNS
  hint (charged-lepton correction to TBM). Worth a gated test.
- **θ₂₃ near-maximal (45–49°):** a μ-τ exchange symmetry forces θ₂₃=45° and θ₁₃=0; the data's deviation tracks θ₁₃≠0.
  Another forced-pattern-plus-breaking.
- **Quark-lepton complementarity** (see §5): θ₁₂^PMNS + θ_C ≈ 45°.
- **Cobimaximal, golden-ratio (θ₁₂ with tan θ₁₂=1/φ), and "Δ(96)" patterns:** secondary geometric candidates.

---

## RANKED HIT-LIST — where an interlock is most likely to be REAL

Ranked by **prior probability that a forced-kernel/interlock actually exists** (not by ease). The ranking reflects: (a)
is there an *already-FDR-surviving* parameter-free relation? (b) is the structure *symmetry-forced* (discrete group /
GUT embedding) rather than a free eigenvalue? (c) does it *interlock* across ≥2 observables/sectors?

1. **Koide Q=2/3 (charged leptons).** ⭐ The single proven, FDR-surviving, parameter-free interlock in the entire SM.
   Already certified real (just not derived). **First target: re-find + re-certify (calibration), then attack the one
   open knob — can a flavor symmetry force r=√2 where the gravity spine provably cannot?** Highest prior by far.

2. **PMNS structure: TBM + A₄/S₄/Δ(27), with θ₁₃≈8.5° as the breaking.** ⭐ The most *symmetry-forced* sector. sin²θ₁₂≈1/3
   and θ₂₃≈45° are forced-pattern values; the engine's geometric/discrete-group hypotheses are tailor-made here. Highest
   prior among the *unsolved* sectors. The charter's "probably geometric" instinct points here.

3. **GST mass-mixing relation √(m_d/m_s) ≈ |V_us| (Cabibbo from quark masses).** A clean mass↔mixing interlock with no
   free parameter — the quark-sector analogue of Koide. Testable now against the gate.

4. **Quark-lepton complementarity θ_C + θ₁₂^PMNS ≈ 45°  AND  θ₁₃ ≈ θ_C/√2.** Cross-sector interlocks (the gate's strongest
   class). If real, they tie CKM and PMNS together → a GUT-scale forced kernel. ~7% level agreement; needs the gate to
   say coincidence vs structure.

5. **Gauge-coupling unification + sin²θ_W=3/8 (GUT).** A real structural hint that 3 couplings collapse to one at high
   scale; the Weinberg-angle GUT value is genuinely forced. Interlock via β-function running.

6. **Georgi-Jarlskog GUT mass relations (m_b=m_τ, m_μ≈3m_s, m_e≈m_d/3 at GUT scale).** Group-theory-forced Yukawa textures
   that *work* to 10–20%. A real forced-kernel candidate in the otherwise kernel-free mass sector.

7. **Wolfenstein/CKM hierarchy as powers of λ.** Structured but the O(1) coefficients (A, ρ̄, η̄) look fitted; Froggatt-
   Nielsen charges are themselves free. Medium prior.

8. **Charged-lepton & quark mass hierarchies generally (Yukawa eigenvalues).** The proven-hard sector (no forced kernel;
   164 FDR-dead). Low prior — engine should report FDR-dead honestly here and not manufacture.

9. **Higgs v, m_H, λ (single scales).** Scales not ratios; weak interlock prior unless tied to Λ (already owned by a₀).
   Low.

10. **θ_QCD ≈ 0.** A symmetry-selection target (PQ/axion), not a regression target — log it, but it's outside the
    number-search engine's reach. Lowest for *this* tool.

---

## Notes for the engine/gate

- **Anonymize before search.** Feed the engine *dimensionless ratios* with variable names stripped, exactly as a₀ was
  found over anonymized cosmological constants — so it cannot "know" it is looking at masses.
- **Within-sector ratios first.** The overall scale (v, or any one mass) is a free dial; the *ratios* are the physics.
  Hunt ratios and the Koide-class invariants (Q, Jarlskog J, the PMNS sin² values), not dimensionful masses.
- **Calibration must pass first.** The engine must re-find √(8π/3) for a₀ and Q=2/3 for Koide, and reject the 164 FDR-dead
  re-labelings, before any new lead is trusted (README §"CALIBRATE before you trust").
- **Cross-sector interlocks are the jackpot.** Items 3–4 (mass↔mixing, CKM↔PMNS) are worth extra search budget because an
  interlock spanning two sectors is the hardest thing to fake and the strongest possible certificate.
- **Flag the [L] values** (m_u, m_d, Σm_ν, δ_CP, ordering, Majorana phases) — do not let the engine fit a tight formula to
  a loosely-measured target and call it a hit. Width of the target gates the strength of any claim.

*Provenance: PDG-2024-class values from model knowledge (cutoff Jan 2026); FDR/Koide discipline from
zimmerman-formula real_research/reviews + opus_48_extended_research/reviews/koide_dsunruh. Same bar both ways.*
