# Agent P — The Verlinde coefficient: is the 1/6 forced, and can data tell 6 from Z = 5.789?

**2026-06-10. Question:** the repo banked (Route 2, `project_routes_to_sign.py`; `ESTABLISHED_PATHS_LEDGER.md`;
`verlinde_foundation_stress_test.md`) that Verlinde 2016 **assumes** the MOND structure. The possibly
under-weighted angle: Verlinde *derives a coefficient* — a_M = cH₀/6 — where the framework's Z = √(32π/3) =
5.789 is data-selected. Audit the coefficient chain on its own terms, per the working rule (test both ways;
never report a convention artifact as a verdict). Companion: `agentP_verlinde_coefficient.{py,out}` (run on
the repo's own SPARC data). Sources pinned from the actual LaTeX source of arXiv:1611.02269v2 (downloaded,
equation numbers verified against the arXiv-v2 PDF; SciPost Phys. 2, 016 (2017) numbering differs — noted
where relevant).

## VERDICT UP FRONT: **COEFFICIENT-CHAIN-EXISTS (conditional)** — with the condition named at full weight

A published derivation (Verlinde 1611.02269, §7) produces, from de Sitter entropy displacement plus an
elastic-response dictionary, a **dimension-forced, π-free, zero-data-input** coefficient Z_V = 6 against the
framework's data-selected Z = 5.789 — a **3.65% gap that no defensible convention can currently distinguish**
(verified on the repo's own SPARC pipeline: Υ-profiled scatter differences of 0.0002–0.0012 dex, both metrics,
both footings, both interpolation shapes). The chain is **conditional on Verlinde's contested postulates**
(volume-law dS entropy + the elastic dictionary + equality-saturation of a derived inequality): if those fail
(Dai–Stojkovic), there is no MOND term and hence **no coefficient at all** — the coefficient cannot be more
derived than the structure it normalizes. What this gives the program: an existence proof that **the
scale-from-Λ link with a derived O(1) is publishable physics, not numerology** — somebody got an O(1) out of
dS entropy and it landed within data precision of ours. What it does NOT give: the framework's exact Z (6 is
rational, Z² = 32π/3 is π-bearing — structurally different objects, mutually exclusive as exact claims), nor
an uncontested derivation (the postulates remain the live dispute), nor the framework's interpolation shape
or a₀(z) branch.

---

## 1. The derivation, pinned verbatim (arXiv:1611.02269v2 — where the 1/6 enters)

**The scale (eq 1.2):** `κ = cH₀ = c²/L = a₀` — the Gibbons–Hawking surface gravity of the dS horizon. The
scale is the dS temperature/horizon scale; **no freedom here beyond the footing (see §2)**.

**The coefficient (eq 1.7):**

> g_D = √(g_B a_M)  with  **a_M = (d−3)/((d−2)(d−1)) · a₀**

and the text following it: *"In d = 4 these equations are equivalent to the baryonic Tully-Fisher relation…
In this case one finds a_M = a₀/6, which is indeed the acceleration scale that appears in Milgrom's
phenomenological fitting formula."* So **the 6 factorizes as 3 × 2, both pure dimension/geometry factors**:

| factor | where it enters | status |
|---|---|---|
| (d−1) = 3 | the volume-law normalization: S_DE(r) = V(r)/V₀ with V(r) = Ω_{d−2}r^{d−1}/(d−1) (eq 2.13) and V₀ = 4GħL/(d−1) (eq 2.14), fixed by the boundary condition S_DE(L) = A(L)/4Għ = the Bekenstein–Hawking dS entropy (eq 2.12) | geometry + boundary condition — **forced once the volume-law postulate is granted** |
| (d−2)/(d−3) = 2 | the ADM/Gauss conversion Σ = (d−2)/(d−3)·g/8πG (eq 1.6) | uncontested Newtonian/GR factor — **forced** |

**The full chain** (every step machine-located in the source): S_M(r) = −2πMr/ħ (eq 4.28; the Bekenstein
bound/Wald-formalism entropy removed by mass — *derived*, §5) → V_M(r) = (8πG/a₀)·Mr/(d−1) (eq 4.33) → the
Eshelby elastic-inclusion condition ∫₀^r ε²(r′)A(r′)dr′ = V_M(r) (§4.4, eq 4.46-class; rigorous version §7.1)
→ Σ_D = (a₀/8πG)ε (eq 7.x `SigmaD`; shear modulus μ = a₀²/16πG fixed by matching elastic to gravitational
self-energy, §6) → ∫_B(8πGΣ_D/a₀)²dV = ((d−2)/(d−1))∮(Φ_B/a₀)n·dA (eq 7.36) → **∫₀^r GM_D²/r′² dr′ =
M_B a₀ r/6 (eq 7.40, "the main formula and central result of our paper")** → g_D = √(a_M g_B), a_M = a₀/6
(eq 7.43, point mass).

**Answer to Q1: GIVEN the postulates, the 1/6 is FORCED — a dimension/geometry factor with zero tunable
freedom and zero data input.** It is *not* a choice the way the framework's ½ prefactor is a route choice.
The freedom lives one level up, in five named postulates: **(P1)** the volume-law dS entanglement entropy
(the heart of the contestation — most derivations give area law only); **(P2)** the linear-in-r interpolation
of the removed entropy (Verlinde grounds it in the Bekenstein bound; the weakest-documented step);
**(P3)** the elastic dictionary (medium = dark energy, modulus a₀²/16πG); **(P4)** equality-saturation —
Verlinde's §7.1 *derives only an inequality* ∫ε²dV ≤ V_M and says so plainly: *"we actually derived an
inequality… we have made an assumption about the largest principle strain"*; **(P5)** spherical/static/
isolated/equilibrium. Verlinde's own framing: *"these scaling relations are not new laws of gravity or
inertia, but appear as estimates of the strength of the extra dark gravitational force"* — an **estimate**,
by its author's own label.

*(Disambiguation: the "1/6" in `agentB_door1_static_kernel` (raw UDW λ² response coefficients "1, 0, 1/6,
1/2π²") is an unrelated bath-response number; the structurally-meaningless flag there does NOT transfer to
Verlinde's 1/6, which is a different object with an actual derivation chain behind it.)*

## 2. The comparison done right (both footings × both coefficients)

**Verlinde's own footing caveat — the find of this audit** (§8, arXiv v2, verbatim):

> "we made use of the value of the present-day Hubble parameter H₀ in our equations… In our calculations the
> parameter H₀ was assumed to be constant, since we made the approximation that our universe is entirely
> dominated by dark energy… This suggests that **H₀ or rather a₀ should actually be defined in terms of the
> dark energy density, or the value of the cosmological constant.** This would imply that a₀ is indeed
> constant, even though it takes a slightly different value."

I.e. **Verlinde himself points at the ρ_DE/cH_Λ footing — the framework's footing — as the correct reading
of his own derivation.** The face-value cH₀ is his pure-dS approximation, not a considered choice of the
rising branch.

| (H₀ = 67.4, Ω_Λ = 0.685) | /6 (Verlinde) | /Z = 5.789 (framework) | gap |
|---|---|---|---|
| cH₀ = 6.548×10⁻¹⁰ (ρ_total footing) | **1.091×10⁻¹⁰** | 1.131×10⁻¹⁰ | 3.65% |
| cH_Λ = 5.420×10⁻¹⁰ (ρ_DE footing) | **9.033×10⁻¹¹** | **9.363×10⁻¹¹ (canonical)** | 3.65% |

- The **footing fork (20.8%) is ~6× the coefficient fork (3.65%)** — the branch question dominates, exactly
  as the footing audit found for the framework's own corpus.
- **External anchor for the footing**: the quasi-de-Sitter EG literature (Diez-Tejedor+ 1612.06282, MNRAS
  477, 1285; adopted by Yoon+ 2206.11685) uses a₀ = 5.41×10⁻¹⁰ — **numerically cH_Λ, the repo's canonical
  rate** — and finds it fits SPARC *better* than cH₀ (mean RAR offset −0.027 ± 0.003 vs −0.060 ± 0.004 dex).
  An independent, non-framework group, testing Verlinde's own coefficient, drifted to the ρ_DE branch
  because the data pushed them there. (Their 2601.01715 continues on this footing.)

**Distinguishability (Q2), against every banked error scale** (`agentP_verlinde_coefficient.out`, Part 3):
the 3.65% gap is 0.18× the McGaugh+16 M/L systematic (g† = 1.20 ± 0.02_stat ± 0.24_syst ×10⁻¹⁰,
arXiv:1609.05917), 0.09× the banked fit-metric swing (~40%: 8.5×10⁻¹¹ unweighted-dex → 1.3×10⁻¹⁰ linear at
fixed Υ = 0.70), 0.12× the interpolation-shape systematic (~30%: the EG-shape SPARC fit prefers a_M ~30%
below cH₀/6 — Yoon-Hwang 1909.01734, Yoon+ 2206.11685). Splitting 6 from Z at 3σ needs σ(a₀) < 1.2% total —
~20× below the honest systematic floor and below even the formal stat-only error. The BTFR channel is worse:
v_f shifts by (Z/6)^¼ − 1 = 0.9%.

**Decisive same-shape run on the repo's own data** (Part 4; 175 SPARC rotmod files; the working rule's
both-ways protocol — both metrics, both footings, fixed-Υ AND Υ-profiled): with Υ profiled (the only honest
comparison; a₀–Υ degenerate), the scatter gap between cH_Λ/6 and cH_Λ/Z is **+0.0004 dex (unweighted) /
+0.0012 dex (weighted)** on the quadrature shape, and −0.0002/+0.0003 dex on the additive shape — pure noise
against the 0.105–0.2 dex relation width. **SPARC cannot tell 6 from 5.789 under any defensible convention.
Neither value wins; neither is in deficit.** (Honesty both ways: under the weighted metric the cH₀-footing
values fit marginally better, under unweighted all four are flat — the *footing* is the only live data axis,
and even it is inside the M/L systematic here.) Side-finding: the additive-vs-quadrature **shape** fork moves
the fit far more than the coefficient fork — the additive (original-Verlinde) form needs Υ ≈ 0.39 (below the
population-synthesis range) to match what the quadrature form does at Υ ≈ 0.6, consistent with Lelli+17's
"hook" being an artifact of the additive combination rule, not of the scale.

## 3. The 2020s status of the chain (Q3) — contested, never killed, never tightened away; the coefficient survived every revision

**The core dispute — unresolved in print:** Dai & Stojkovic, *"Inconsistencies in Verlinde's emergent
gravity"* (JHEP 11 (2017) 007, arXiv:1710.00946): the strain ε ~ ∇u scales as 1/r², so the elastic argument
done carefully returns **Newton, not MOND** (their added fluctuation term δ(x,y,z) restores 1/r² in Σ_D).
Yoon, arXiv:2003.03198 (preprint, unpublished): D-S misread the dictionary — their fluctuation term belongs
to the *baryonic* energy bookkeeping; the a₀-bearing deviatoric elastic energy (the RHS of Verlinde's eq 20)
is the apparent-DM piece by construction, and Σ_D = (a₀/8πG)ε stands. **No third-party adjudication exists
(checked June 2026).** The banked stress-test wording stands: *active debate, not a closed refutation* — in
either direction.

**Did anyone tighten or kill the 1/6? No — it survived every published revision; only the combination rule
moved:** Yoon 2003.03198 (eq 22 reproduces Verlinde's (2/3)-relation, hence the same 1/6) and Yoon 2024
(*Phys. Dark Universe* 45, 101551 — corrects an overlooked Eshelby surface term) both **keep a_M = a₀/6
exactly** and change only the total: **g = √(g_B² + g_D²) instead of Verlinde's g = g_B + g_D**. Note what
that is: g = √(g_B² + a_M g_B) — **character-for-character the framework's working interpolation**
(`rar_framework_a0_mlfit.py`'s `g_obs_pred`) with a₀ → cH/6. The published corrected-EG equation IS the
framework's RAR equation with a 3.65%-different coefficient. The Verlinde–Zurek line (1902.08207, PLB 822
(2021) 136663; 1911.02018; shockwave modular fluctuations PRD 106 (2022) 106011) develops causal-diamond
*vacuum fluctuations* for interferometry and **never revisits the galactic 1/6** — the dS-entanglement
program neither re-derived nor retracted it.

**Data confrontations of the EG formula (the class's own ledger, full weight both ways):**
- **KILLS (worldline/solar-system):** Hees, Famaey & Bertone (PRD 95, 064019, arXiv:1702.04358) — eq (7.40)
  taken as a force law over-predicts perihelion precession by **~7 orders of magnitude** (banked in
  `agentH1_candidate_matrix.md`: EG "dead", ×10⁷). The only escape is incompleteness ("the formula does not
  apply to non-isolated/non-spherical systems" — Verlinde's own P5 list), the same locked wording as the
  SfDM Cassini escape. The quadrature correction does not rescue this (the +a_M/2 additive tail at high g_B
  is the same one the framework's shape fights in its own solar-system battles).
- **STRUCTURAL (cannot do disks):** Milgrom & Sanders 1612.09582 — eq (7.40) is spherical/static/isolated
  only, *"cannot predict rotation curves, except asymptotically"*; Lelli, McGaugh & Schombert (MNRAS 468,
  L68, arXiv:1702.04355) — the additive point-mass form leaves a hook-shaped inner-region residual.
- **PASSES (lensing, parameter-free):** Brouwer+ 2017 (MNRAS 466, 2547, arXiv:1612.03034) — first test,
  agreement in four stellar-mass bins with NO free parameters; Brouwer+ 2021 (A&A 650, A113, 2106.11677) —
  the lensing RAR to 2 decades below a₀ agrees with the EG prediction (ΛCDM-degenerate, per the paper).
  *(These are the framework's own lensing-RAR data — the 8.6–9.2σ type-split exposure cuts against EG
  exactly as against every universal law.)*
- **MIXED-to-FAVORABLE (the 2022–2026 quasi-dS line, advocacy-flagged — all Yoon-group):** SPARC RAR offset
  −0.027 dex on the cH_Λ footing (2206.11685); the corrected (quadrature) EG claimed to reproduce the Chae
  wide-binary anomaly (PDU 45, 101551 — low weight: the repo's banked WB verdict is that the DR3 observable
  is degeneracy-limited, and the anomaly itself is contested); dwarf spheroidals claimed to favor quasi-dS
  EG over MOND at 5.2σ on 23 dSphs (arXiv:2601.01715, Jan 2026 — directly opposite to the *mixed* verdict of
  Diez-Tejedor+ 1612.06282 on the same class; unadjudicated, single-group). Watch item, not a result.
- **Covariant attempts:** Hossenfelder 1703.01415 (PRD 95, 124018) — covariant CEG exists but its dS
  background is perturbatively unstable (banked); no CMB framework; clusters retain the MOND-like ~2×
  core residual (ZuHone & Sims 1905.03832; Tamosiunas+ 1901.05505; Halenka & Miller 1807.01689), though
  eq (7.40) with extended gas (d(M_B r)/dr > M_B) reduces it relative to pure MOND — Verlinde §7.2.

**Net Q3 verdict: the derivation survives as a live, contested heuristic** — wounded where every MOND-class
universal law is wounded (solar-system face value, type-split lensing, no covariant completion, no CMB), and
its coefficient has been **independently re-derived (twice, by its critics' critic), re-footed onto cH_Λ by
data pressure, and never moved off 1/6.**

## 4. The critical diff against the banked verdict (Q4): does "assumed-not-derived" kill the coefficient too?

The banked Route-2 wording (`project_routes_to_sign.py`): *"motivated ANSATZ — a₀=cH₀ identified, sign from
a volume-law+elastic postulate; Dai-Stojkovic say done right it gives Newton not MOND. Not derived."* Two
things are true at once, and the banked wording captured only the first:

1. **The critique transfers to the coefficient in the conditional sense.** Shape and scale are NOT separable
   in this chain: the 1/6 is the normalization OF the volume-law/elastic structure. If P1/P3/P4 fail, the
   formula reverts to Newton and there is no a_M to have a coefficient. The 1/6 is exactly as conditional as
   the √-law and the sign. **"The SCALE is derived even where the SHAPE is not" is FALSE as an unconditional
   claim** — they stand or fall together.
2. **But "assumed" is the wrong word for the coefficient, and this is the under-weighting the question
   suspected.** Within the candidate derivation the 1/6 carries **zero data input and zero tunable freedom**
   — it is dimension-forced ((d−3)/((d−2)(d−1))), unlike the framework's Z, which is selected by SPARC from
   a κ·Z = √(8π/3) family of routes. On the derive-vs-assume axis the two coefficients have **opposite
   epistemic signs**: Verlinde's is derived-conditional-on-contested-postulates; the framework's is
   data-certain-but-underived. The banked scorecard line "Verlinde 2016 — CONTESTED" stands; the banked
   *flattening* of his coefficient into the same "posited" bucket as Smolin's 8.3 (read off data) or the
   framework's Z was too coarse. `project_routes_to_sign.py`'s FACT-2 ("coefficient MATCHED, not FORCED —
   schemes disagree") also stands at the across-schemes level — the spread 2π/6/5.789/8.3 is real — but
   within-scheme, Verlinde's is the only one of the four where the O(1) is forced by the scheme's own
   geometry rather than matched. That distinction was previously unrecorded.

## 5. What this gives the program — and what it does not

**Gives:** (a) an existence proof that the program's central missing step — **Λ/dS-horizon physics → a
MOND-scale a₀ with a derived O(1)** — has a published instance landing within data precision (3.65%) of the
framework's data-selected value, on the framework's own footing (by Verlinde's own §8 caveat and the
quasi-dS literature's drift); (b) a published interpolation identical in form to the framework's working
equation (Yoon-corrected EG), making the framework's kernel + shape combination *less* isolated in the
literature than the banked picture had it; (c) a sharpened statement of what any future derivation of Z must
beat: the Verlinde chain shows a rational 6 is reachable from volume-law entropy counting — the framework's
π-bearing Z² = 32π/3 requires a *different* counting (the Friedmann/geometric route), and the two are
**mutually exclusive as exact claims** (6 ≠ √(32π/3)), distinguishable only at sub-1.2% precision that no
RAR-class measurement will reach (the Υ systematic is the wall).

**Does not give:** the framework's exact Z (a 3.65%-different number from disjoint structure — agreement
here is the empirical *degeneracy* of two different theoretical objects, not a confirmation of either); an
uncontested derivation (P1–P4 remain the live dispute, D-S unresolved); a covariant theory, a CMB story, an
a₀(z) branch (Verlinde's §8 explicitly defers cosmological evolution), or any relief on the lensing
type-split — the program's standing exposures are untouched.

**Watchlist additions:** (i) any third-party adjudication of Dai–Stojkovic vs Yoon (the equality-saturation
step P4 is the decidable core); (ii) the 2601.01715 dSph 5.2σ claim — if independently reproduced, it is
evidence FOR a ~9.0×10⁻¹¹ acceleration scale on the ρ_DE footing, i.e. directly framework-relevant data
(3.5% below the canonical 9.36×10⁻¹¹), and AGAINST the regular-MOND 1.2×10⁻¹⁰; treat with the same
both-ways discipline as the MUSE confrontation.

---
*Sources, arXiv-pinned: 1611.02269v2 (LaTeX source read directly; eqs 1.2, 1.5–1.7, 2.12–2.15, 4.27–4.28,
4.33, 7.36–7.40, 7.43; §8 caveat) · 1710.00946 (JHEP 11 (2017) 007) · 2003.03198 (preprint) · 1909.01734
(preprint) · 2206.11685 (Yoon, Park & Hwang) · Yoon 2024, Phys. Dark Universe 45, 101551 · 2601.01715 ·
1612.06282 (MNRAS 477, 1285) · 1702.04355 (MNRAS 468, L68) · 1702.04358 (PRD 95, 064019) · 1612.09582 ·
1612.03034 (MNRAS 466, 2547) · 2106.11677 (A&A 650, A113) · 1703.01415 (PRD 95, 124018) · 1902.08207 (PLB
822, 136663) · 1911.02018 · 1609.05917 (PRL 117, 201101) · 1905.03832 · 1901.05505 · 1807.01689. In-repo:
`agentP_verlinde_coefficient.{py,out}`, `COEFFICIENT_FOOTING_AUDIT_2026-06.md`, `project_routes_to_sign.py`,
`ESTABLISHED_PATHS_LEDGER.md`, `verlinde_foundation_stress_test.md`, `rar_framework_a0_mlfit.py`,
`agentH1_candidate_matrix.md`.*
