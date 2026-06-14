# The scaling-MOND web: the whole structure, what it predicts, and where it stands

**2026-06-01.** A physicist-ready synthesis of the *real* surviving framework — one premise,
its forced consequences, the data that now tests them, and the honest frontier. This
**supersedes nothing in `FRAMEWORK.md`/`NOVELTY.md`** (their calibrated skepticism stands); it
*collects the web* and records what this session's calculations actually changed. Everything
here is reproducible from the cited scripts. The numerology (`ai_slop/`) is not part of this.

---

## 0. One paragraph

A single premise — **the MOND acceleration scale is the cosmic dynamical acceleration,
a₀ = (c/2)√(Gρ_c) = cH(z)/Z, Z = 2√(8π/3) = 5.789** — forces a connected set of relations
through standard equations (Friedmann + Bekenstein–Milgrom). It is *over-constrained*: one
number pins ~5 independent measurements, and they cohere (+4 net constraints). Its one
distinctive, coefficient-free prediction is that a₀ **evolves as E(z)**; the 2026 data now
**favor evolving over constant a₀ at 5σ** — a reversal of the repo's earlier "disfavored." It
is **not** a Theory of Everything: it does not derive the Standard-Model constants (that was
numerology, quarantined), the coefficient Z is posited not derived, and the CMB still needs a
relativistic completion. What it *is*: a falsifiable scaling-MOND cosmology with one number,
many forced edges, and a live, data-tested frontier.

---

## 1. The premise and the one number

$$a_0 = \tfrac{c}{2}\sqrt{G\rho_c} = \frac{cH(z)}{Z},\qquad Z = 2\sqrt{8\pi/3}=\sqrt{32\pi/3}=5.78881,\qquad \frac{a_0}{cH}=\frac1Z=0.17275.$$

Via Friedmann (H² = 8πGρ/3) the two forms are algebraically identical. The novel *framing*
(see `NOVELTY.md`) is the **Schwarzschild surface-gravity reading** a₀ = c²/2R of the cosmic
free-fall scale R = √(8π/3)·c/H. **Honest status:** this is a novel form/interpretation of
Milgrom's 40-year coincidence a₀≈cH₀, *not* new physics; the coefficient 1/Z is a **posit**
(the ½ is heuristic Schwarzschild, the √(8π/3) is the Friedmann free-fall/Hubble ratio), an
8% near-miss of Milgrom's 1/2π, bracketed but not derived.

---

## 2. The web — one invariant in many costumes (`REAL_WEB.py`, `web_search_relations.py`)

The dimensionless invariant **a₀/cH = 1/Z**, held fixed while H(z) evolves, is the *generator*.
Dimensional analysis projects it into six unit-costumes — the same number on six walls:

| costume | quantity | value |
|---|---|---|
| acceleration | a₀ = cH/Z | 1.13×10⁻¹⁰ m/s² (RAR) |
| length | ℓ_a = c²/a₀ = Z·R_H | 5.79 R_H |
| surface density | Σ_M = a₀/G | 811 M⊙/pc² (HSB/LSB line) |
| velocity | v⁴ = G M a₀ | BTFR zero-point |
| temperature | T_a₀ = T_dS/Z | 4.6×10⁻³¹ K |
| time | t_dyn = 1/√(Gρ) | 2.894 t_H |

From this, **~13 forced edges** (each a real equation, not a fit): a₀↔ρ_c, ↔H₀, ↔Λ floor,
a₀(z)↔E(z), ↔q, ↔T_dS, ↔RAR knee, ↔BTFR, ↔high-z M_dyn; plus the derived consequences —
BTFR/Faber–Jackson slope is z-invariant with a 1/E(z) intercept; a redshift-mixed RAR must
broaden by log E(z_max); the phantom-halo density runs as **√E(z)** (`mond_first_principles.py`,
a derivation that *corrected* an earlier √-error); dispersions clock as E(z)^¼ (de Graaff's
channel); a₀-cosmography (a₀(z) *is* H(z)); MOND is eternal (a₀ floors at Λ, ~21% below today).

**The over-constraint ledger.** Real web: 5 independent measurements − 1 parameter = **+4**.
The constants "web" (α=4Z²+3, …): 4 data − 7 free integers = **−3** (a fit). A coincidence does
not survive 4 independent agreements; a real relation does.

**The discriminator** (`web_search_relations.py`): a genuine edge is **z-invariant** (a₀/cH=1/Z
at every epoch); a coincidence is not. Applied: it *keeps* the forced relations and *rejects*
a₀↔T_CMB (drifts ×1.66 in z) and a₀↔particle scales (×10). The same z-evolution that makes the
web real is an objective filter for future claims.

---

## 3. What the data says (the tests done this session)

The single coefficient-free prediction is the redshift law. Fit a₀(z)=A·E(z)^p — the premise
forces **p=1** (a theorem: a₀∝√ρ_total∝H) — to the real compilation (`a0_powerlaw_confrontation.py`):
SPARC 1.20±0.26 (z≈0), Vărăşteanu 1.69±0.13 (z≈0.05), MUSE-DARK 2.38±0.11 (z≈0.9):

| scaling | meaning | χ² | verdict |
|---|---|---|---|
| p = 0 | constant a₀ (standard MOND) | 27 | **rejected, 5σ** |
| **p = 1** | √ρ_total — the premise | **3.8** | **favored** |
| p = 1.5 | √ρ_matter (dust-tracking) | 27.5 | **rejected, 5σ** |
| best fit | — | 2.5 | **p = 0.80 ± 0.17** |

Independent nodes that cohere: Planck CMB H₀ → a₀ (0.1% of SPARC), MUSE-DARK a₀(z≈1), de Graaff
JADES M_dyn (z≈6), the Λ floor, and the KiDS weak-lensing RAR (confirmed → ledger +5). Gaia wide
binaries are a contested seventh node (a +6-or-falsify fork). **Honest caveats:** the dominant
uncertainty is the ~40% local-anchor systematic (SPARC 1.20 vs Vărăşteanu 1.69, 1.7σ apart at
the same z); and an evolving RAR is *also* expected in ΛCDM from halo evolution — so favoring
evolving is **not** a unique confirmation of the framework.

---

## 4. The relativistic frontier and the TOE attempt

**Two readings of the MOND scale** (`relativistic_frontier.py`), degenerate today, divergent
later: a₀∝√Λ (de Sitter, **constant**, p=0 — the default of relativistic MOND) vs a₀∝√ρ_total∝H
(the premise, **evolving**, p=1). They agree to 21% now (the Λ floor) but separate to ~12× by
z=6; the data picks the evolving one. **AeST** (Skordis–Złośnik 2021), the one CMB-capable
relativistic MOND (c_GW=c), recovers *constant* a₀ as built — so the premise is a **sharper**
claim than AeST, and the two are already observationally distinguishable. The premise has a
natural covariant home: couple a₀ to the **aether expansion θ = ∇·A = 3H** (a *local* field),
giving a₀ = cθ/(3Z) = cH/Z — the Machian channel, no action-at-a-distance. **[Proposal, not
theorem.]**

**The TOE attempt, computed** (`toe_cmb_calculation.py`). Take the framework as foundation, no
CDM. The CMB needs Ω_m h²≈0.14 of *clustering* dust; baryons give 0.022. The decisive internal
result: since a₀²∝ρ_χ, for ρ_χ to *be* CMB dust (∝(1+z)³) one needs a₀∝(1+z)^1.5 — **the very
exponent the galaxy data reject at 5σ**. So a₀'s own density tracks the *smooth* total density
(∝H²), and **a₀ cannot be the dark matter** — the exponent that fits galaxies forbids it. The
background is otherwise benign (a₀/cH=1/Z is epoch-independent even though a₀ is 2×10⁴× larger at
recombination). **Conclusion:** the CMB clustering must come from the relativistic sector's scalar
*perturbations* δφ (the SZ mechanism), with a₀ promoted to a₀(z) — a separate knob. The one real
calculation that remains, sharply posed: the SZ δφ Boltzmann run with a₀→a₀(z). I set it up; I
do not fake it.

---

## 5. What's new this session — honestly, vs. what the repo already had

> *Your instinct was right: most of the core already existed.* The formula, the Schwarzschild
> reading, the evolving prediction + the E(z) vs (1+z)^1.5 fork, the AeST completion, and the
> honest ledger were all in `FRAMEWORK.md`/`NOVELTY.md`/`Z2_cascade.py`/`papers/`. Here is the
> **delta** — what we learned that we did not know before:

| # | what changed | before (in repo) | now (this session) |
|---|---|---|---|
| 1 | **the prediction got tested, and the verdict flipped** | "untested" (FRAMEWORK §6); "disfavored" (NOVELTY) | constant a₀ **rejected 5σ**, evolving favored, p=0.80±0.17 |
| 2 | **the fork was resolved by data** | both E(z) and (1+z)^1.5 open | E(z) (√ρ_total) favored; (1+z)^1.5 **rejected 5σ** |
| 3 | **a₀ cannot be the CMB dark matter** | AeST CMB "likely safe, unproven" | *proven from the data*: dust needs p=1.5, excluded 5σ → clustering must be δφ |
| 4 | **over-constraint quantified** | "interlocking web" asserted | +4 (real) vs −3 (constants) — a number, not a slogan |
| 5 | **objective real-vs-coincidence filter** | — | z-invariance test (keeps edges, rejects T_CMB/particle coincidences) |
| 6 | **derivations that corrected assertions** | phantom density ~E(z) | ~√E(z) (derived from ∇·g_MOND); "MUSE-DARK over-shoot" shown anchor-driven, not exponent-driven |
| 7 | **the aether-expansion home** | "needs AeST" (deferred) | a₀∝θ=3H realizes the premise locally — a named covariant route |

**What did *not* change (the skepticism stands):** it is a novel *framing* of known physics,
not new physics; Z is still posited, not derived; it is **not** a TOE (no SM constants); the
constants numerology and the T³/Z₂ topology are still dead. The flip in (1)–(2) is real but
bounded — ΛCDM also predicts an evolving RAR, so this is "favored," not "uniquely confirmed."

---

## 6. Can a TOE be "proven" — the right way?

You cannot *prove* a physical theory the way you prove a theorem; you can only make it
**compelling** by raising the cost of it being a coincidence. The legitimate levers — the
opposite of the numerology that the audit killed — are three:

1. **Over-constraint.** Few numbers forcing many *independent* predictions that all hold. Each
   independent agreement multiplies the odds against coincidence. This is the web's +4. The way
   to "prove it the right way" is to *increase* that number — add independent nodes (lensing-RAR
   did: +4→+5; wide binaries would: +6), never add free integers (the constants web did the
   opposite: every line cost a knob, ledger −3 → ~0 bits, the false-discovery result).
2. **Confirmed *novel* predictions.** A forward prediction, measured *after* it is made, is worth
   orders of magnitude more than a retrodiction. The framework's is a₀(z): the decisive one is a
   **clean deep-MOND a₀ at z>2**. If it lands on E(z) with p=1±0.1, that is a genuine novel
   confirmation — the single most valuable thing the program can obtain.
3. **Reducing the posits.** Every derived parameter is a parameter you no longer fit. The one
   posit here is Z (the factor-of-2). *Deriving* it from first principles (not the dead
   eta-invariant numerology) would convert the last free number into a prediction.

So: **a TOE cannot be proven, but a theory can be made coincidence-proof** by driving
over-constraint up, getting a novel prediction confirmed, and driving posits down. The honest
ceiling for *this* framework is a **compelling scaling-MOND cosmology of the dark sector**, not a
theory of *everything* — because it says nothing forced about the Standard-Model constants. The
moment a "TOE" claim reaches for α or the masses, it has crossed back into `ai_slop/`. The
discipline *is* the method: real where it flows through one equation, illusory where it jumps
domains on a number.

---

## 7. External anomaly: the cosmic dipole (a candidate, held to the same standard)

The Secrest et al. quasar-dipole anomaly — the matter dipole exceeds the CMB-kinematic
expectation — was 4.9σ (2021) and, after the 2025 reassessment (arXiv:2511.00822), **survives at
~3.3–3.6σ** (clustering and the survey mask do not explain it). Does the framework speak to it?

- **The legitimate direction:** MOND — *a fortiori* evolving-a₀ MOND with stronger gravity at the
  quasars' redshift (a₀(z≈1.5)≈2–3× today) — generically predicts **larger bulk flows** than
  ΛCDM. That is the right *direction* for an enhanced matter dipole, and it is mechanistic
  (literature-grounded), not a fitted number. **Status: candidate, qualitative.** Converting it to
  the observed ~1.5–2× requires the bulk-flow amplitude — i.e. the *same* structure-formation
  calculation that is the open frontier (§4). It is **not** a forced web edge (it is at fixed z,
  fails the z-invariance test as a *clean* a₀ probe), so it sits outside the over-constrained core.
- **The dead version (for contrast):** `ai_slop/research/COSMIC_DIPOLE_ANOMALY_Z2.md` "explained"
  it as **R = 19/6 = 3.167** from T³/Z₂ "degree-of-freedom structure" — pure number-fitting on the
  quarantined topology, and the observed ratio has since dropped toward ~1.5–2, missing 3.17. That
  is the trap; it stays in `ai_slop/`.

Honest verdict on the dipole: a **plausible qualitative target** for evolving-a₀ MOND (right
direction, real mechanism), **not** a prediction the framework computes yet, and explicitly *not*
the 19/6 numerology. It earns a line on the roadmap, not a claim.

---

## 8. Bottom line and the decisive next tests

**What stands:** a₀=(c/2)√(Gρ)=cH/Z — a novel framing of Milgrom's coincidence — with an
over-constrained (+4), data-coherent web; the evolving prediction a₀∝E(z) now **favored over
constant at 5σ** (the genuine new result), with the √ρ_matter/dust alternative also excluded;
galaxies, GW speed, and the cosmic background all accounted for. **What is open:** the coefficient
Z (posited), the CMB δφ Boltzmann run (a₀ cannot itself be the dust — proven), and the unique-vs-
ΛCDM degeneracy of the evolving signal. **What is dead:** the SM-constant numerology and the
topology — including the 19/6 dipole.

**The three measurements that would decide it:**
1. a **clean deep-MOND a₀ at z>2** → pins p to ±0.1; confirms or kills the premise (novel test).
2. a **2–3% local a₀** (resolve SPARC 1.20 vs Vărăşteanu 1.69) → removes the dominant systematic.
3. the **SZ δφ Boltzmann run** with a₀→a₀(z) → settles whether the dark sector can be no more than
   baryons + a scaling scalar.

That is the whole honest web: one number, many forced edges, one prediction now data-favored, one
posited constant, and a frontier that is finally *sharp* rather than vague.

---

*Reproduce:* `REAL_WEB.py` · `web_search_relations.py` · `mond_first_principles.py` ·
`a0_powerlaw_confrontation.py` · `relativistic_frontier.py` · `toe_cmb_calculation.py` ·
`rar_evolution_test.py`. *Grounding:* `FRAMEWORK.md`, `NOVELTY.md`, `INTERLOCKING_WEB_ASSESSMENT.md`,
`papers/v12_SCALING_MOND_ACTION.md`. *Foundations:* Milgrom 1983; McGaugh–Lelli–Schombert 2016
(SPARC); Skordis–Złośnik 2021 (AeST); Secrest et al. 2021 + arXiv:2511.00822 (the dipole).
