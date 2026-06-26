# Frontier Deep-Dives — Track A (Susskind/DSSYK and Z) + Track B (running-Koide)

Date: 2026-06-26
Framework constants: a0 = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3) ≈ 5.78881, 1/Z ≈ 0.172747.
1/Z = (½)·√(3/8π) **machine-exact** (verified diff < 3e-42, mpmath dps=40): the ½ is κ (the lone FREE part),
√(3/8π) is the forced Friedmann-3 / Einstein-8π geometry.

Two independent live frontier threads were deep-dived. Both come back **honestly negative on the hoped-for
"someone else derives the open number," but each leaves a precisely-characterized residue.** No manufactured win,
no high-priesting; every number below was re-derived here (mpmath/sympy, dps=40).

---

## TRACK A — Does Susskind's DSSYK–de Sitter program fix Z?

### Verdict: **NO. Z stays an independent gravitational (field-equation) coefficient.** post-hoc-null.

DSSYK / "Many Temperatures of de Sitter Space" (Rahman–Susskind, arXiv:2401.08555, full text via ar5iv;
cross-checked 2501.09423, 2511.10907) addresses a **factor-of-2/π question — *which* O(1)×H temperature is
physical — not the value of Z.** The 8π Einstein normalization that lives inside Z is **invisible** to a thermal
or entropy count. At most this work informs the κ=½ question, and even there it pushes the *wrong way* (β=1, the
standard Gibbons–Hawking value, not κ=½).

### What the four Susskind temperatures actually give (accelerations a = 2πcT, in units of cH_Λ)

Using the Unruh map a/(cH) = T/T_GH, with T_GH = H/2π giving a_GH = cH **exactly**:

| Susskind temperature | a / cH_Λ | a / a0 | note |
|---|---|---|---|
| (1) Gibbons–Hawking / "tomperature" τ_H = 2J0 = H/2π = T_GH (eq 1.3, 6.59) | **1.000** | 5.789 = **Z** | the overshoot numerator |
| (2) static-patch / naive dS-Unruh (framework's banked ~2cH) | **2.000** | 11.578 = **2Z** | the banked ~12× overshoot |
| (3) cord / "fake-disk" T_cord = J0/π (eq 4.45) | 0.637 (or ~2, dict-dependent) | 3.685 | blueshift τ_cord/τ_H ~ p **diverges**, not Z-sized |
| (4) Boltzmann T_B | ∞ (cosmic) / ~string-scale | — | maximal-mixing normalization, no a0 connection |

a0 = 0.1727 cH sits **below all of them.** Susskind's static-patch reading **reproduces the framework's own banked
~2cH** — i.e. Susskind and the framework *agree* on the temperature-route scale, and they agree it is the
**overshoot** (~Z to 2Z too big vs a0). That is a real, non-coincidental consistency point, but it confirms the
framework's *diagnosis* (temperature route overshoots), not a *cure*.

### Three grounded reasons no temperature reaches Z — all re-verified here

**(A) STRUCTURAL (decisive).** 1/Z = √(3/32π) is a **square root** of rational/π. Every Susskind dS temperature is
**linear in J (= linear in H)**: τ_H = 2J0, T_cord = J0/π, T_cord = pJ/2π — all of form (rational×π^n)·H. A
linear-in-H temperature can **never** equal √(rational/π)·H without an ad hoc square root. The framework's √ comes
from a0 ~ √ρ_Λ (a **density/energy-squared** route); Susskind's temperatures are **energy-scale** (linear). These
are categorically different objects — which is *exactly why* the temperature route overshoots (linear → a~cH) while
the density route gives a0 ~ cH/Z (sqrt).

**(B) NUMERICAL.** No clean grid factor lands near 1/Z = 0.17275 (verified):
H/2π = 0.15915 is the closest, off by **1.0854×** (an unclean fudge); 2/π, 1/π, 2, 1 are all 1.8–11.6× off.
τ_H reproduces the overshoot numerator exactly (ratio to T_GH = 1.0000000), not a0.

**(C) DECOMPOSITION.** 1/Z = (½)·√(3/8π) exactly. Susskind supplies **neither** factor: not the ½=κ (his
tomperature has β=1) and not the √(3/8π) (his temps are linear, no sqrt). The overshoot 2Z = (1/κ)·Z, and the "2"
there is the *static-patch* factor, unrelated to κ=½.

### The 8π problem (why Z is structurally out of thermal reach)

Z = √(32π/3) = √(4·8π/3). The **8π** is the Einstein field-equation normalization inside ρ_Λ = Λc²/8πG; the **3**
is Friedmann; the **4 = 1/κ²** with κ=½ free. A de Sitter temperature or entropy count sees only the scale H and
O(1) multiples — **never the gravitational field-equation coefficient.** This is the *same quantity* the banked
CKN-holography result (KAPPA_FORCING_DOOR_CLOSED, we1j03q80) proved unforceable by entropy data: κ is the OUTSIDE
fraction; the √(8π) that fixes it lives INSIDE ρ_DE, unseen by sign/ratio/entropy data. Track A is an independent
re-derivation of that wall from the Susskind side.

### Does DSSYK fix a normalization? — and the honest caveats

DSSYK takes the dS scale as **input, not output** (2J0 = 1/2π·ℓ_dS, eq 1.3; ℓ_dS fixed by hand). It only fixes
*which* O(1) coefficient (2, π, or 1/p) multiplies H. Where it *does* pin a temperature, it pins the pode
temperature to **standard GH (β=1)** — the framework's overshoot, Z-times too big.

Honest limits I could not fully pin (flagged, not hidden):
- The two papers gave **inconsistent J0↔ℓ_dS dictionaries** (2π in 2401.08555 eq 1.3 vs 1 in 2501.09423 eq 6.5).
  I worked both; *neither* reaches Z. But this O(1)/2π dictionary ambiguity **is** the "temperature normalization is
  open" issue — and it spans factors {2, π, 2π}, all rational/π-linear, **none** the irrational √(3/32π). So the
  residual freedom is over the wrong *kind* of factor and cannot reach Z even in principle.
- I did **not** find the literal "GH = H/2π = J0 expression" in 2511.10907 (entropy paper) or 2501.09423; the
  τ_H=T_GH identity rests on 2401.08555 eq 1.3, which **is** explicit.
- 2511.10907 turned out partly about a 't Hooft-model T_c = g·M_planck correction, not pure dS temperatures —
  thin contribution.

### What is genuinely forced vs. not (both-ways)

- **GENUINE / credit:** Susskind's program *independently confirms* the static-patch/GH temperature is the natural
  dS thermal scale and that the temperature route lands at the **overshoot** (~2cH), vindicating the framework's own
  banked bookkeeping. The "many temperatures" thesis also vindicates the framework's stance that picking a
  temperature is normalization-ambiguous.
- **NOT forced:** the ambiguity is the **wrong kind** (linear π-factors, not a sqrt); DSSYK supplies neither κ=½ nor
  √(3/8π); it never generates an irrational density-route √. Z is a **field-equation coefficient, not a thermal
  quantity.** Consistent with the banked TOE map flagging DSSYK as a mirage. **Corroborates the overshoot, does not
  derive Z.**

---

## TRACK B — Is running-Koide a real discriminating measurement?

### Verdict: **Calculable, NOT measurable.** A real, sign-confirmed *theoretical* discriminator, but the +0.18% vs
### +0.374% vs 0 separation is ~3 orders of magnitude below any conceivable m_τ precision. Tracking-only at best.

### Computed framework drift (reproduced here, mpmath dps=40, PDG 2024 masses)

Pole Koide (m_e=0.51099895, m_μ=105.6583755, m_τ=1776.86 MeV):
**Q(pole) = 0.66666051**, i.e. Q−2/3 = −6.16e-6 = **−0.905σ** (τ-limited σ_Q ≈ 6.8e-6). At-2/3 to within a σ.

Charge-universal 1-loop QED running, m_i → m_i^(1+g), g = (3/2)(α/π):
- α(0): g = 0.0034842 → **Q = 0.6678089, drift +0.1723%** (POSITIVE)
- α(M_Z)=1/127.95: → **Q = 0.6678904, drift +0.1845%** (POSITIVE)

**Sign = POSITIVE** (Q rises above 2/3 at higher scale) — brackets the banked +0.18%. The deep why is sympy-exact:
charge-universal running is a pure power rescaling, the μ^(−g) factors **cancel exactly**, so the drift is
**scale-FLAT** and equals dQ/dp|_{p=1}·g = 0.32998·0.0034842 = **+0.1725%**. Literature cross-check (Sumino;
Xing–Zhang hep-ph/0602134, "running masses fail Koide, Q(M_Z) deviates ~0.2%") matches **sign AND magnitude.**
**Banked +0.18% CONFIRMED.**

### Singh prediction clarified (+ tension with the at-2/3 pole)

Singh's K = 0.66916 (arXiv:2508.10131 Sec XI.1; catalogue 2604.06288) is the **POST-triality-breaking** value
(pre-breaking = exact 2/3), mechanism = charged spread δ²=3/8 plus a single endpoint tilt on the first lepton rung.
It is **+0.374% above 2/3** (verified). Crucially Singh treats masses as *physical* (Jordan eigenvalues |λ_i|²) and
leptons as "scale-clean" → **0.66916 is scale-INDEPENDENT, a prediction for the PHYSICAL/pole Koide.**

**Tension, stated honestly:** the *measured* pole Koide is Q = 0.66666 (at 2/3 to −0.9σ). Singh's 0.66916 is
**+0.374% = ~3.7e-3 above** the measured pole — that is **~370× the measured offset** and **~+50σ in τ-limited σ_Q**.
So Singh's post-breaking tilt, taken at face value as a *pole* prediction, is **already in tension with the data**
(the pole is at 2/3, not at 0.66916). The framework's RG drift, by contrast, applies to the *high-scale* Koide and
leaves the *pole* at 2/3 — consistent with measurement. The only thing the two share is the **SIGN** (both raise Q
above 2/3); the magnitudes (+0.18% vs +0.374%) and the *scale at which they apply* (high-μ vs physical) differ.
The banked "sign match" is real but is a match of **sign only**, not a magnitude or same-observable agreement.

### Can m_τ precision ever resolve +0.18% vs +0.374% vs 0? — **NO**

This is the decisive both-ways result. Propagating PDG 2024 σ_{m_τ} = 0.12 MeV into Q:
σ_Q (from m_τ) ≈ 6.77e-6 → **0.00102% of 2/3.** That is the *current* dominant Koide uncertainty.

To **resolve** a 0.18% separation in Q (≈ 1.2e-3 in absolute Q) at ~3σ, you would need σ_Q ≈ (target/3),
which back-propagates to **σ_{m_τ} ≈ 7.1 MeV** — but that is the *wrong direction*: the issue is not that m_τ is too
imprecise, it is that **the drift is a property of the THEORY's running, not of the measured pole masses.** The pole
Koide is *fixed at 2/3* by measurement (−0.9σ); the +0.18% lives at high μ where there is **no direct mass
measurement at all** — quark/lepton masses are not measured at M_Z, they are *run* there using the same QED/QCD that
*produces* the drift. There is no independent high-scale "measured Koide" to compare against.

**Therefore running-Koide is calculable-not-measurable:**
- The +0.18% (framework) is a **prediction about a derived quantity** (Q at high μ), with no independent measurement.
- The +0.374% (Singh) is a *pole* prediction already disfavored by the measured pole (at 2/3).
- The "0" (exact 2/3) is the measured pole, confirmed to −0.9σ.
The three differ at the 0.1–0.4% level in Q; the **measurable** pole Koide pins only the "0" branch and confirms it.
No m_τ campaign reaches inside the high-μ regime where +0.18% vs +0.374% would separate, because that regime is
*defined by running*, not measurement. The discriminator is **internal-consistency / sign**, not an experiment.

### Both-ways on Track B

- **GENUINE / credit:** the framework's +0.18% drift is **independently reproduced, sign-confirmed, and matched in
  sign+magnitude by the Sumino/Xing–Zhang literature** — a real, non-trivial fact (charge-universal running raises Q
  above 2/3 by ~0.18%, scale-flat, exactly). The pole sitting at 2/3 to −0.9σ is a genuine ~1-in-44k FDR-surviving
  coincidence (the banked Koide lead). The **sign** agreement between framework drift and Singh's tilt is real.
- **NOT a measurement:** the magnitudes (+0.18% / +0.374% / 0) live on different *observables* (high-μ running vs
  physical pole), Singh's value is in tension with the measured pole, and **no m_τ precision can resolve them** —
  the separation is calculable, not measurable. This is consistent with the banked mass-sector closure
  (KOIDE_FROM_DSUNRUH, re-confirmed wjx8gedyb): the dS-Unruh spine cannot supply the IR protector Q=2/3 needs, and
  κ=½→√2 is two free numbers. Track B adds: even the *running* signature, while real and sign-correct, is not an
  experimental discriminator.

---

## NET — honest status of each thread + single next step

### Thread A (Susskind/DSSYK → Z): **CLOSED (corroborating, not deriving).**
DSSYK answers a factor-of-2/π temperature-choice question and is *blind to the 8π Einstein normalization* that is the
substance of Z. It confirms the framework's overshoot bookkeeping (static-patch = ~2cH = 2Z) but supplies neither
κ=½ nor √(3/8π), and its residual freedom is over rational π-factors while Z is an irrational sqrt. This is an
independent re-derivation of the already-banked KAPPA_FORCING_DOOR_CLOSED wall from the holographic/thermal side.
**No live experiment, no open derivation door. Close it; do not re-open absent a forced *density-route sqrt*, which
no temperature program can produce.**

### Thread B (running-Koide): **TRACKING-ONLY (calculable-not-measurable), leaning closed-as-experiment.**
The +0.18% drift is real, reproduced, and sign-matched to the literature; the pole sits at 2/3 to −0.9σ. But the
+0.18% / +0.374% / 0 separation lives on observables that are *run, not measured*, and no m_τ precision reaches it.
The one genuinely live *measurable* quantity is the **pole Koide itself**, which is τ-mass-limited.

### Single most concrete genuine next step (not theater)
**Track the pole Koide σ as m_τ improves — that is the ONE measurable, falsifiable number in either thread.** σ_Q is
currently dominated by σ_{m_τ}=0.12 MeV (σ_Q≈6.8e-6, pole at −0.9σ from 2/3). Belle II / a future τ-charm factory
m_τ improvement tightens σ_Q linearly. **Falsification gate:** if improved m_τ moves the pole Koide *away* from 2/3
by more than the framework's drift allows (i.e. the pole settles at, say, Singh's +0.374% rather than 2/3), the
at-2/3 reading dies and Singh's pole-tilt is favored; if it stays pinned at 2/3 as σ shrinks, the at-2/3 +
high-μ-drift picture is reinforced. This is a real, banked, watch-list-able number (add to ROUTINE.md data-watch:
"PDG m_τ update → recompute pole Q, σ_Q, n-σ from 2/3"). Everything else in both threads is internal-consistency,
not experiment.

**Bottom line, both-ways:** Track A corroborates the framework's overshoot diagnosis but derives nothing new and is
closed; Track B's drift is real and sign-confirmed but is calculable-not-measurable, leaving only the
τ-mass-limited *pole* Koide as the single genuine falsifiable handle. No manufactured win; no reflexive dismissal —
the at-2/3 pole and the +0.18% drift are both real, the hoped-for "DSSYK fixes Z" and "running-Koide is an
experiment" are both honestly null.
