# G224 — THE SOLAR-SYSTEM FACE CLOSEOUT
**The paper's force-section statement, assembled: the equilibrium reading's cleanest domain.**
*Lane: G224. Repo: zimmerman-formula. Date: 2026-09-16.*
*Sources (all committed, nothing recomputed): G155 (the sourced-equation closure), G204 (the k⁴ family dead), G03 (the Cassini campaign: g03_s0_calibration.\*, g03_candidate1_gates_v2.out, g03_verdict.md), G086 (PPN = GR by construction, 9/9), L244 (the disformal preferred frame), G007 (the bimetric, Lean, 11 theorems), H045 (the k-essence ghost), L243 (the exact-AQUAL quadrupole), G006 (the EFE cap), G202 (the MNRAS results skeleton, §4.5), G205/G207 (the closure and falsifier ledgers), the SPARC and DES moonshot registers (G002/L232/G114; G020/G022). Verification: G224_solar_face.py + G224_results.json — 20/20 checks PASS, cross-read from the artifacts.*

---

## 1. THE COMPLETE SOLAR-SYSTEM CASE

### (a) The equilibrium reading — PASS BY CONSTRUCTION

The phantom is *absent* in the Solar System, and that absence is what makes the
face pass:

1. **g ≫ a₀ everywhere.** The Sun's MOND radius is r_M = √(GM_☉/a₀) = **7960 AU
   (0.0386 pc, canonical footing)** — the entire classical Solar System sits at
   g/a₀ ≥ 7e5, four to seven orders into the strong-field regime. The kernel's
   departure from Newton inside Neptune's orbit is bounded by 1 − μ₂ ≤ **8.07e-10**
   (at Neptune; 9.96e-16 at 1 AU; L244 V1). (Lanes: G204 header, L244)
2. **The phantom does not exist there.** The equilibrated charge dust is a
   sub-a₀ phase — it lives where the sector has equilibrated (galaxies, clusters)
   and is absent where the field is strong. The local cloud is **unbound and
   EFE-capped at 7.4 kAU** (G006, registered): no transition shell inside the
   Solar System, hence **no l = 2 moment**, hence no quadrupole — trivially under
   the Park 2026 ceiling (5.2e-27 s⁻²), which is itself Newton-consistent.
   (Lane: G006; assembled in g03_verdict.md)
3. **The metric is GR's.** Φ = Ψ (no anisotropic stress: the sector is ordinary
   barotropic dust, p = 0, w = 0), the scalar is frozen in the strong-field
   regime (no vector sector, no preferred frame), and the lensing response sees
   the full real mass: **PPN γ = 1, β = 1, α₁ = α₂ = 0, Φ − Ψ = 0 — exactly**,
   and **c_T = c identically** (GW170817 |c_T − c|/c < 3e-15 passes at 0, nothing
   to arrange). (Lane: G086 9/9; H027 T1)
4. **Stated, not fitted.** There is no fit: the predicted deviations are exactly
   zero, so every solar-system bound passes with the *full bound* as margin. This
   is the property that distinguishes the reading from Horn A (which needed a
   fixed congruence) and from every force-law class (which needed a screening the
   smooth-shell lemma proved impossible). (Lane: G086 V1/V4)

### (b) THE DEAD ROUTES TABLE — every alternative, its gate, its killing number

| # | Route | Gate | The killing number | Lane |
|---|---|---|---|---|
| 1 | **k-essence force-law ghost** (H001, bare) | energy / ghost + Mercury precession | P_X = −μ₂ < 0 (wrong-sign gradient energy) → ghost, energy unbounded below; **−90 arcsec/cy vs 0 ± 0.04** | H045 |
| 2 | **The sourced equation** (G155 candidate a: conformal trace coupling) | PPN γ + WEP/MICROSCOPE | At the MOND-required coupling M = √2 M_pl (fixed by G alone): **γ = 1/2 → 2.2e4× the Cassini \|1−γ\| < 2.3e-5**; MICROSCOPE η < 1.4e-15 forces M in [3.8e4, 3.8e5] M_pl, which suppresses the source by **[7.1e8, 7.1e10]** — the flat curve dies 4–5 orders. **No consistent scale exists** (C8, the deciding constraint). | G155 C4–C8 |
| 3 | **Biharmonic k⁴ screened parent** (H004) | ghost + Cassini at the parent's own ξ | P_X = −f′ is *invariant* (spatial operator); the affine modes {a + b·x} lie in ker(Δ²) with negative gradient energy → **ξ_c = ∞**; at its own ξ = 0.045 pc the quadrupole is **6.45×/7.65×** the ceiling = Mercury drift 0.26/0.31 arcsec/cy vs 0 ± 0.04. | G204 a2–a4, B2 |
| 4 | **Disformal preferred frames** (TeVeS/AeST class) | PPN α₁ | **α₁ = 4 (MMG/khronometric) = 4.0e4× the \|α₁\| < 1e-4 bound**; AeST α₁ = −2(K_B+2) = O(1) with K_B ≲ 0.25 from BBN; the μ₂ swap leaves it unchanged to < 1e-9 (kernel-independent). | L244, DC-013/DC-019 |
| 5 | **Bimetric / composite** | lensing sum (exact frame algebra) | The conformal lever carries the force but **cancels in the lensing sum** (`lensing_sum_cancellation`); the disformal lever is dual-inert (`disformal_entries`); the scalar's stress channel is **2e-6 short** (`stress_vs_phantom_ratio`) — **Lean-certified, 11 theorems, zero sorry**. | G007 |
| 6 | **The k⁴ family** (G030/G034/f31/H006) | the same static operator + Pais–Uhlenbeck | H001 dead (row 1), H004 dead (row 3), the whole-sector stiffening's static limit is the SAME scanned operator (g03 C2), its PPN evasion a time-sector phenomenon invisible in the static frame; 7 local k⁴ operators tried. **The family has NO surviving member — H048 DOOR 1 CLOSED.** | G204 V3; G03 S2 |

*The equilibrium reading is the sole survivor: it needs no completion, no
screening, no congruence — because it is not a force law at all. The MOND-like
force is the gravity of equilibrated mass (the halo IS the phantom, G003/Lean,
coefficient 1); the Solar System contains none of that mass.*

### (c) THE CASSINI RECORD

- **The instrument (S0, 5/5).** The validated code reproduces L243's exact-AQUAL
  quadrupole **6.44×/7.63×** the Park 2026 ceiling (1-sig 6.18×/7.29×), g01's
  exact-exponential 2.107e-26 s⁻² (4.05×), the ceiling 5.2e-27 s⁻², and the T-B
  floors. (Lane: g03_s0_calibration.\*)
- **The 44-solve scan floor.** 28 single + 16 double filters on the 512×128 grid,
  both a₀ footings, at g_ext and g_ext − 1σ, ξ = 0.005–0.1 pc: **|Q₂|/ceiling ≥
  6.18× (1-sig) at EVERY screening length tested.** Monotone non-improvement —
  ξ = 0 is the best case (6.44×/7.63×); anyway the double filter *worsens* it.
  (Lane: g03_candidate1_gates_v2.out; assembled g03_verdict.md)
- **The S2 double-filter state.** Canonical 6.46× (0.01 pc) → 6.54× → 6.66× →
  **7.22×** (0.05 pc); alternative 7.68× → 7.83× → 8.04× → **8.78×**. Registered
  S2b min over the double-filter scan, both footings at g_ext−1σ: **6.21×**.
  FAIL on both footings at both floors (canonical 6.54×, alt 8.04× at the central
  value). (Lane: g03_candidate1_gates_v2.out S2 double rows)
- **The smooth-shell lemma (scan-confirmed, class-closing).** An isotropic local
  screen — Helmholtz or Gaussian, single or double, 0.005–0.1 pc — preserves the
  l = 2 moment of the μ-transition shell, because the quadrupole is generated by
  the shell's ANGULAR structure and isotropic radial smoothing does not touch it.
  The static quadrupole is a property of the kernel's transition, not of the
  completion's ultraviolet structure: **the force-law class is closed WITH PROOF,
  at S2, per the spec's cheap-kill order.** (Lane: g03_verdict.md)
- **The class result, structural per candidate.** T-B localised (C1): fails by
  scan. Field-dependent ξ(x): same class — ξ(x) is a function of the isotropic
  invariant x = g/a₀, the screen stays isotropic, the lemma applies verbatim
  (structural kill, no scan needed). Whole-sector form factor (C2): its PPN
  evasion is a time-sector phenomenon — statically invisible, the static limit is
  the operator already scanned — fails by identity with C1's scan.

**Contrast (the two moonshot registers the face must stay consistent with).**
The SPARC moonshot — 155 SPARC curves / 2788 points at zero-parameter rms
**0.150 dex** (L232/G002; the deep end G114) — is the galactic-scale statement
this face protects: the amplitude the completions would have to source at O(1)
fifth-force strength. The DES moonshot — the growth raise at **~3σ vs direct
lensing, DESI final the arbiter** (G020/G022; the BGS→QSO factor-4 fall) — is the
cosmological face, decided by instrument, not by construction. The Solar System
face is the ONLY face with no pending instrument: it is closed by proof.

---

## 2. THE STATEMENT — one paragraph for the paper (§4.5, the force-face)

> **The Solar System is the equilibrium reading's cleanest domain, and the place
> where the theory most sharply shows what it is not.** Because the phantom is
> the *equilibrated* state of the dark sector, and equilibration requires g ≲ a₀,
> the Sun's field — which exceeds a₀ by four to seven orders of magnitude out to
> the Oort cloud — contains no phantom, no transition shell, and no quadrupole:
> the local cloud is unbound and EFE-capped at 7.4 kAU, and the metric is
> Einstein's exactly, with PPN γ = β = 1 and α₁ = α₂ = 0 by construction rather
> than by fit, and c_T = c identically. **The Cassini null is therefore
> architectural, not fitted**: every attempt to make the RAR a force law dies
> with its number — a sourced k-essence field (γ = 1/2 at the coupling fixed by
> Newton's constant, a fifth force of order unity, killed by Cassini at 2.2e4×
> and by MICROSCOPE at a source suppression of 7e8–7e10), a biharmonic screened
> parent and the whole k⁴ family (a ghost at every screening length, ξ_c = ∞, and
> a quadrupole that a 44-solve scan never lowers below 6.18× the Park ceiling —
> 6.45×/7.65× at the parent's own ξ = 0.045 pc), a disformal vector sector
> (α₁ = O(1), 4 × 10⁴× the preferred-frame bound, kernel-independent), and a
> bimetric completion (lensing-dead by exact frame algebra, Lean-certified) — while
> the equilibrium reading needs no completion, no screening, and no free
> parameter to predict Newton there exactly. The Solar System is where the
> theory's claim is sharpest: **the RAR is not a modified force; it is the
> gravity of mass that has equilibrated, and in the Solar System that mass is
> absent.**

---

## 3. VERDICTS

### V1 — THE ASSEMBLED CASE. PASS (20/20).
(a) The pass-by-construction chain is complete and every number is read from its
committed artifact: PPN = GR exactly with all four parameters and Φ = Ψ (G086
9/9), c_T = c at 0 vs the 3e-15 bound, 1 − μ₂ ≤ 8.07e-10 out to Neptune (L244),
the phantom absent by the EFE cap at 7.4 kAU (G006), r_M(☉) = 7960 AU placing
the whole system at g/a₀ ≥ 7e5. (b) All six dead routes carry their gate and
their killing number — the ghost at −90 arcsec/cy (H045), γ = 1/2 at 2.2e4×
Cassini and the 7e8–7e10 MICROSCOPE suppression (G155 C6–C8), ξ_c = ∞ + 6.45×/
7.65× at the parent's own ξ (G204), α₁ = 4 = 4.0e4× the bound (L244), the lensing
sum cancelling in 11 Lean theorems (G007), and the k⁴ family with no surviving
member (G204 V3). (c) The Cassini record is complete: the 44 solves (28+16), the
6.18× 1-sig floor at every screening length, the double filter's registered
6.21× minimum with its worsening canonical 6.54→7.22× / alt 7.68→8.78×, and the
smooth-shell lemma closing the class with proof.

### V2 — THE PAPER PARAGRAPH. PASS.
The statement in §2 is a single self-contained paragraph, in the MNRAS skeleton's
§4.5 voice, carrying every number a referee needs (6.18×, 6.44×/7.63×, 6.45×/7.65×,
2.2e4×, 7e8–7e10, 4e4×, ξ_c = ∞, 7.4 kAU, γ = β = 1, α₁ = α₂ = 0) with lane
citations, and it asserts what the face asserts — an architectural null — without
claiming a measurement. It slots directly under the skeleton's §4.5 headline
numbers (c_T = c; the Cassini null; no fifth force anywhere).

### V3 — THE HONEST STATEMENT. PASS.
**The force-face is the cleanest section of the paper — the only one closed by
construction.** Every alternative route is dead with its number on the record,
the equilibrium reading is the sole survivor, and — unlike every other section —
the Solar-System face carries **no pending instrument and no open falsifier**
(its falsifiers, such as they are, are the deep-regime tests in *other* regimes:
the DR4 wide-binary ridge is Solar-System-*adjacent*, G088, and decides the
unbound-cloud architecture, not the face's GR-ness). The contrast is the honest
ledger: the Solar System face is an *identity* — stated, not fitted — while the
theory's testable content lives in the deep regime (DR4, tSZ, JWST/ALMA, XRISM,
the sub-1e6 collapsed count), each with its kill number in print (MNRAS
§4.6, FALSIFIER_MATRIX 20 rows). Nothing on this face is claimed measured; the
face is claimed *proven* — which is stronger, and which is what the pincer
(G155/G204/G03/G086/G007/L244) established.

---

*Deliverable complete. Pass: 3/3 verdicts, 20/20 checks. G224_results.json written alongside.*