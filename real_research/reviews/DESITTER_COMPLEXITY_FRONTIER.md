# The de Sitter complexity / holography frontier — pursued honestly

**Carl Zimmerman · June 2026.** The framework's deepest acknowledged gap (`THEORETICAL_CONTEXT.md` §2)
is that **de Sitter holography is "not under control (AdS only)."** This is the one genuinely
unexplored *way-forward* direction the ai_slop salvage review surfaced. Pursued here with real
calculation and — given what the rest of this repo turned out to be — scrupulous labeling of
**[ESTABLISHED] / [RESULT] / [OPEN]**. No complexity→a₀ derivation is asserted; none exists in the
literature (verified by search, June 2026). Companion code: `reviews/desitter_complexity_sign.py`.

---

## 1. What is established (the program is real and, newly, tractable)

- **[ESTABLISHED] de Sitter scales.** R_dS = c/H₀ ≈ 4.4 Gpc; Gibbons–Hawking entropy S_dS = A/4ℓ_P² ≈
  2.3×10¹²²; temperature T_GH = ℏH₀/2πk_B; horizon surface gravity = cH₀ = 6.5×10⁻¹⁰ m/s².
- **[ESTABLISHED, 2023–2026] DSSYK–de Sitter duality.** The double-scaled SYK model is dual to the de
  Sitter static patch (Susskind; Narovlansky–Verlinde; Rahman; arXiv:2310.16994 → JHEP 05(2025)032;
  2406.19089; chord-algebra refinement Rahman 2024). The holographic screen is the **stretched
  horizon**. This is the first version of de Sitter holography that is *computationally tractable*.
- **[ESTABLISHED, 2025] de Sitter complexity = volume grows linearly** in the static patch, at a rate
  **∝ the horizon DOF (∝ S_dS)** (arXiv:2508.10093) — correcting the earlier "hyperfast growth" picture.

## 2. Results from this pass

**[RESULT — a₀∼cH is dimensionally forced; the O(1) is not.]** The de Sitter data are {c, H, and the
*dimensionless* S_dS}. The only acceleration one can build is cH × (function of S_dS), and S_dS cannot
change the *power* — only an O(1) prefactor. So **every** de Sitter-scale mechanism (surface gravity,
Verlinde entropy, holographic complexity) yields a₀∼cH by necessity; only the coefficient differs
(5.79 vs Verlinde 6 vs Milgrom 2π vs 1). This is *why* the coefficient is unpinned, and why no de
Sitter mechanism — complexity included — can derive the exact 5.789 (consistent with the number-field
no-go in `desitter_entropy_coefficient.py`). **The scale is robust; the coefficient is not.**

**[RESULT — complexity tracks entropy at leading order.]** Because dC/dt ∝ S_dS (2508.10093), de Sitter
complexity at leading order is governed by the *same* quantity the Verlinde route already uses. For the
**scale a₀**, complexity therefore gives **no shortcut** beyond the entropy route, and the linear-growth
result weakens the earlier hope that *hyperfast* complexity growth was a distinctive new ingredient.
Pursued rigorously, the productive near-term handle is the **entropy/DOF route**, of which complexity is
the dynamical shadow.

**[RESULT — the decisive sign calculation: DOF, not temperature.]** On a holographic screen (bits
N = 4πr²c³/Gℏ, Unruh k_BT = ℏa/2πc):
- **Full equipartition** Mc² = ½N k_BT ⟹ a = GM/r² (**Newton**).
- **Debye DOF-freezing** (only fraction f = a/a₀ of bits excited below a₀): Mc² = ½N(a/a₀)k_BT ⟹
  a = √(g_N a₀) — **deep MOND, gravity enhanced below a₀** (correct sign), a₀∼cH (Verlinde 2011,
  arXiv:1001.0785; relativistic version arXiv:2511.05632, 2025).
- **Temperature modification** (T→√(a²+(cH)²)/2π in Jacobson δQ=TδS) ⟹ G_eff = G/W → 0: **anti-MOND**
  (`clausius_sign_calculation.py`).

> **The MOND sign is decided by which thermodynamic factor you modify: the ENTROPY/DOF count → MOND;
> the TEMPERATURE → anti-MOND.** This unifies the framework's own negative result with Verlinde 2011 and
> the 2025 relativistic-entropic-MOND paper, and isolates the open problem to a single, well-posed demand.

**[CAVEAT — modified inertia vs modified gravity, so this does *not* contradict Layer 0.]** The de
Sitter-Unruh *temperature* gives MOND in `desitter_unruh_mond.py` because there it modifies **inertia**
(Milgrom 1999), not the field equation. The anti-MOND result is for modified **gravity**. Summary:
modified-inertia + temperature → MOND (the working Layer 0, fits SPARC 0.105 dex); modified-gravity +
temperature → anti-MOND; modified-gravity + DOF/entropy → MOND (Debye). The framework's open problem is
the *covariant (modified-gravity)* completion — which is exactly why it needs the **entropy/DOF door**,
where de Sitter complexity's DOF-dynamics is the natural language.

**[RETRACTED — fabrication caught by the full-repo integrity audit, June 2026.]** This paragraph
previously asserted as a `[RESULT]` that *"Debye/entropic fits SPARC at 0.100 dex with a₀ = 1.32×10⁻¹⁰,
vs 0.105 dex / 1.78×10⁻¹⁰ for de Sitter-Unruh,"* and concluded the modified-gravity/DOF route is
"sign-correct *and* data-viable." **No such SPARC fit was ever computed.** `desitter_complexity_sign.py`
contains **no SPARC load and no fit machinery** — the "0.100 dex / 1.32×10⁻¹⁰" numbers were narrative,
never measured, and were paired with the *genuinely*-computed de Sitter-Unruh value (1.78×10⁻¹⁰ / 0.105
dex) to look measured. The "better data fit" claim is **withdrawn**. What survives honestly: the
Debye/DOF route gives the right deep-MOND *sign* (Section 2, computed); whether it *also* fits SPARC
better than de Sitter-Unruh is **untested** and must not be asserted until a real error-weighted SPARC
fit is actually run. (This was the single outright fabrication found in the 320-script / 121-doc audit;
it is recorded in `INTEGRITY_AUDIT.md` and retracted here.)

## 3. Where de Sitter complexity could genuinely add value — open problems, labeled

- **[OPEN Q1 — the sign from first principles].** The Debye freezing fraction f = a/a₀ is *posited*
  (right answer, by hand — like the framework's contested volume-law entropy). What principle *forces*
  DOF to freeze (→ MOND) rather than the temperature to rise (→ anti-MOND)? Candidate: the **second law
  of complexity** (Brown–Susskind, arXiv:1701.01107) — if the dark/MOND response is the system relaxing
  toward maximal *complexity*, the induced-force sign is a computable property of the complexity
  functional, **not** a posit. *No one has done this.* It is the honest way complexity could **earn** the
  sign rather than assume it.
- **[OPEN Q2 — the interpolation].** The Newton↔MOND crossover μ(a/a₀) is unforced. In the DSSYK-dS dual
  the stretched-horizon / finite-cutoff structure is computable (arXiv:2602.06113); whether the chord /
  transfer-matrix structure predicts a *specific* μ(x) is a concrete, solvable question in a model that
  is actually under control.

## 4. Honest verdict & next steps

- a₀∼cH is forced; the coefficient is not, and complexity does not change this.
- Complexity **tracks entropy at leading order** → no shortcut to a₀; the productive handle is entropy/DOF.
- **Decisive, verified:** MOND requires modifying the **DOF/entropy** (Debye), not the temperature — and
  that route gives the right deep-MOND *sign* (computed, §2). Whether it *also* fits SPARC better than
  de Sitter-Unruh is **untested** and must not be asserted until a real error-weighted SPARC fit is run.
- Complexity's genuine, **unclaimed** prize is the **sign from the second law of complexity** (Q1) and the
  interpolation from DSSYK-dS (Q2). Real, unsolved, now stated precisely.

**Concrete next steps:** (1) **still to do** — run a *real* error-weighted SPARC fit of the Debye/entropic interpolation, head-to-head vs de Sitter-Unruh (the fit the retraction above shows was never actually computed). (2) read 2511.05632 in
full and test whether its surface-DOF modification is sign-defensible by the §2 logic or smuggles in the
freezing. (3) *the prize* — in the DSSYK-dS dual, formulate a baryonic probe and compute whether the
static-patch response **enhances** at low acceleration (MOND); the first time the framework's deepest
question can be asked where the holography is under control. This is a research program, not a session's
work — but it is real, and it is not numerology.

---

### References (verified, June 2026)
- Susskind; Narovlansky & Verlinde; Rahman — *Double-scaled SYK & de Sitter holography*, arXiv:2310.16994 (JHEP 05(2025)032); *dS, complexity & DSSYK*, arXiv:2406.19089; chord-algebra refinement, Rahman 2024.
- *De Sitter Complexity Grows Linearly in the Static Patch*, arXiv:2508.10093 (2025).
- *Deforming the Double-Scaled SYK / stretched horizon from finite cutoff*, arXiv:2602.06113 (2026).
- E. Verlinde — *On the Origin of Gravity*, arXiv:1001.0785 (2011); *Emergent Gravity and the Dark Universe*, arXiv:1611.02269 (2016).
- *Relativistic MOND from Modified Entropic Gravity*, arXiv:2511.05632 (2025).
- Jacobson — *Thermodynamics of Spacetime*, gr-qc/9504004 (1995). Brown & Susskind — *Second law of complexity*, arXiv:1701.01107 (2018).

*In-repo companions: `desitter_complexity_sign.py` (this calculation), `clausius_sign_calculation.py`
(the anti-MOND temperature result), `yphi32_from_entropy.py` (the contested volume-law route),
`desitter_unruh_mond.py` (the modified-inertia Layer 0), `desitter_entropy_coefficient.py` (the
coefficient no-go).*
