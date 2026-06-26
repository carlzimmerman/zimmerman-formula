# Frontier Leads — THE NUMBERS (calc-backed, both-ways)

**Date:** 2026-06-26
**Framework anchor:** a0 = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3) = 5.78881; a real dS–Unruh modified-inertia
MOND result that **hosts** the Koide *shape* via Spin(8)-triality but **not** the amplitude. SM/TOE
overclaims were honestly retracted — this file is REAL checks, not a re-overclaim.

**Method:** every claim grounded in an actual arXiv/ar5iv fetch (abstract + full text where reachable);
every number recomputed in mpmath (dps=40) / sympy against PDG 2024 masses **with errors**. Both-ways:
a prediction that holds is credited; one that fails is reported at full weight; no inflation either way.
Clean-room scripts: `/tmp/frontier_calcs.py`, `/tmp/milgrom_calc.py`.

---

## 1. THE NUMBERS — what the actual calculations showed

### (A) Singh & Teli first-generation √m ratio — PINNED to ar5iv 2508.10131 / 2604.06288
Paper claim (verbatim, fetched): "explains the lightest-generation relation √m_e:√m_u:√m_d = 1:2:3 as a
direct consequence of the trace split" (equivalently mass 1:4:9). Abstract accuracy hedge: quark ratios
"agree at the few-percent level once a common renormalisation scale is used."

COMPUTED vs PDG 2024 (m_e=0.51099895 MeV pole; m_u=2.16⁺⁰·⁴⁹₋₀.₂₆, m_d=4.70⁺⁰·⁵⁰₋₀.₄₅ MeV MS̄ @2 GeV):

| quantity | computed | predicted | sigma |
|---|---|---|---|
| √(m_u/m_e) | 2.056 ± 0.179 | 2 | **+0.31σ** |
| √(m_d/m_e) | 3.033 ± 0.153 | 3 | **+0.21σ** |
| √-triple | 1 : 2.056 : 3.033 | 1:2:3 | up +2.8%, down +1.1% |
| mass-triple | 1 : 4.227 : 9.198 | 1:4:9 | — |

**VERDICT: HOLDS at ~0.2–0.3σ — NOT falsified, sits right on prediction. But NON-DIAGNOSTIC**: the
light-quark MS̄ errors (~12–23%) are so wide the test cannot distinguish 1:2:3 from a few-% departure.
Low discriminating power.

### (B) m_τ/m_μ = m_s/m_d — PINNED to 2605.24866 Eq.(60), Table 3
Paper: Eq.(60) "m_τ/m_μ = m_s/m_d". Fetched Table 3: √(m_τ/m_μ)_exp = 4.12314 ± 0.00023;
√(m_s/m_d)_exp = 4.35494 ± 1.09947 (their single fitted value 4.18832 deviates 1.58% lepton / 3.83% quark).

COMPUTED vs PDG 2024 (m_s=93.5⁺⁸·⁶₋₃.₄ MeV):

| test | computed | sigma |
|---|---|---|
| MASS m_τ/m_μ | 16.817 ± 0.001 | — |
| MASS m_s/m_d | 19.894 ± 2.382 | s/d is **+18.3%** above τ/μ |
| MASS difference (s/d − τ/μ) | +3.077 ± 2.382 | **+1.29σ** |
| √ version, fresh PDG errors | diff +0.359 ± 0.267 | **+1.35σ** |
| √ version, Teli's own Table-3 errors | diff +0.232 ± 1.099 | **+0.21σ** |

**VERDICT: HOLDS at +0.2σ (Teli's errors) to +1.3σ (fresh PDG) — NOT falsified. NON-DIAGNOSTIC**: the
strange-quark error (±4–9%) swamps the test. The +18% central s/d excess is the only mild tension and it
is well inside 1.3σ.

### (C) Koide shift vs framework drift — SIGN MATCH, same order (~2×)
PINNED to 2508.10131 (verbatim, fetched): "Before triality breaking the centred lepton triplet yields the
exact Koide value K=2/3"; "After electroweak/triality breaking ... a single endpoint tilt on the first
lepton rung shifts it mildly to **K_th ≃ 0.66916**, close to experiment" = **+0.374% above 2/3 (POSITIVE)**.

COMPUTED:
- Observed **pole** Q (PDG 2024) = **0.66666051**, i.e. **−6.2×10⁻⁶ = −0.0009% = −0.91σ BELOW 2/3**
  (τ-mass-limited, σ_Q = 6.8×10⁻⁶). At the pole the data sits essentially AT 2/3, a hair below.
- Framework banked drift (RG running): **+0.18% / 178σ, POSITIVE**.
- Singh +0.374% vs framework +0.18% → **SIGN MATCH** (both predict Q rises ABOVE 2/3 after breaking/running);
  **magnitude ratio 2.08×** (same order).

**VERDICT:** the most interesting convergence — two **independent** mechanisms (EJA endpoint-tilt vs
dS-Unruh RG drift) both push Q *up* from 2/3. But NOT yet a sharp confrontation: neither +0.18% nor +0.374%
is resolved against a *measured running-Koide*; the pole sits at 2/3 − 0.91σ. Track, don't bank as a win.

### (D) EJA δ²=3/8 → Koide identification (sympy-exact)
PINNED to 2508.10131: eigenvalues λ∈{q−δ, q, q+δ}, char. poly λ³−Tλ²+Sλ−D=0, δ²=3/8 (charged), δ_ν²=3/4
(neutrinos), Tr X_e:X_u:X_d = 1:2:3.

VERIFIED (sympy): reading eigenvalues as **√-masses**, Q = ⅓ + 2δ²/(9q²):
- **δ²=3/8 → Q = 5/12 = 0.41667** (matches the framework's banked "EJA δ²=3/8→K=5/12") — **NOT 2/3**.
- **δ²=3/2 → Q = 2/3** exactly.

So Singh's "exact 2/3 before breaking" rests on a **centred-triplet** identification, not on δ²=3/8 directly.
The two δ² values (3/8 vs 3/2) are not interchangeable; "exact Koide from δ²=3/8" is **not literally correct**.
(This also reproduces the banked KOIDE_SELFDUALITY note: triality *breaking* 3/2→3/8 gives 2/3→5/12.)

### (E) Milgrom 2503.07106 "Is MOND necessarily nonlinear?" — PINNED to fetched full text
Verbatim structure: Lagrangian (Eq.14) with kinetic term ∝(r̈)² (modified INERTIA, 4th-order EOM Eq.8),
LINEAR field equation Δ^½ψ = π²A₀ρ (Eq.16, modified GRAVITY), Green's fn G_{1/2}(r)=−1/(2π²r²) (Eq.17),
circular-orbit result V_c=(M·A₀)^¼ i.e. **V∞⁴ = M·G·a₀ with UNITY coefficient** (Eq.28). A₀≡G·a₀ is the
single DML constant, **chosen to data — INPUT, not predicted**; ZERO mention of Λ, H₀, cosmology.

COMPUTED alignment with the framework:

| M_bar | V∞=(GMa₀)^¼ (Milgrom **==** framework Tier-D eq.12 v⁴=GMa₀) |
|---|---|
| 10⁹ M⊙ | 59.37 km/s |
| 10¹⁰ M⊙ | 105.58 km/s |
| 10¹¹ M⊙ | 187.75 km/s |

Deep-regime interpolation (framework g_obs=√(g_bar²+g_bar·a₀) vs Milgrom-linear pure-DML √(g_bar·a₀)):
agrees to **0.49% at g_bar/a₀=0.1, 0.05% at 0.01, 0.005% at 0.001** — identical deep-MOND law.

**ALIGNMENT VERDICT: PARTIAL.** AGREES on the deep-MOND BTFR law (identical to 6 sig figs). DIFFERS on
structure: Milgrom-linear is (i) DEEP-MOND-ONLY — **no Newtonian limit, no interpolation** (his own Sec IV);
(ii) **LINEAR → NO external-field effect** (his abstract); (iii) modifies BOTH inertia and gravity (verbatim:
"A₀ has mixed length and time dimensions ... forces us to modify both the inertial and the gravitational
terms"), not pure-MI. Milgrom's own verdict on his model: "unacceptable as a basis for a full-fledged MOND
theory" (Ostrogradsky-unstable, no Newtonian limit, ψ log-diverges on thin shells). It is **non-relativistic
only — NO covariant completion**. On a₀'s VALUE the two are complementary and non-conflicting:
Milgrom-linear neither confirms nor constrains a₀=√Λ. **Framework a₀ recomputed: 9.425×10⁻¹¹ m/s²**
(Planck-2018 Λ; 0.70% from canonical 9.36e-11; 0.785× regular-MOND).

### (F) Baez & Schwahn 2606.15235 — does EJA-gauge change the disjoint verdict? NO.
PINNED to fetched abstract: derives the **SM gauge group** as a stabilizer inside F4 from J₃(O)
(via 𝔥₂(ℂ) qubit / 𝔥₃(ℂ) qutrit subalgebras). Contains **ZERO** discussion of fermion masses, mass ratios,
the Koide relation, the lepton-mass amplitude, Λ, MOND, a₀, or gravity.

**VERDICT:** Baez-Schwahn is the *same algebraic neighborhood* (F4 / J₃(O) / triality) the framework hosts,
and it independently validates that neighborhood as the right home for the SM gauge structure — but it
touches **neither** the framework's open flavor target (Koide amplitude) **nor** its gravity side (a₀~√Λ).
It does **NOT** change the disjoint verdict: the gravity↔flavor bridge stays absent. It is a gauge-group
result only.

---

## 2. THE GENUINE CALC-BACKED LEAD (single best)

**The Koide sign-agreement (item C): two independent mechanisms both push Q ABOVE 2/3 after breaking/running
— Singh's EJA endpoint-tilt (+0.374%) and the framework's dS-Unruh RG drift (+0.18%), same sign, same order
(2.08×).** This is the one place where a *calc-backed*, *independently-arrived-at* convergence exists between
Singh's program and the framework, on the framework's exact open target (the Koide sector), and it makes a
**concrete falsifiable next step**: resolve a *measured running-Koide* (Q at the EW scale vs the pole).
Today the pole sits at 2/3 − 0.91σ and neither offset is resolved, so it is a tracking lead, not a win — but
it is the only numbers-backed direction with discriminating potential, because both the 1:4:9 and τ/μ=s/d
tests are NON-DIAGNOSTIC (light-quark errors swamp them) and cannot move.

**Why not the alternatives:**
- 1:4:9 / τ/μ=s/d "convergence": real (holds at 0.2–1.3σ) but *non-diagnostic* — can't be built on until
  light-quark masses tighten ~5–10×.
- Milgrom 2503.07106 as "a covariant MI tool the framework lacks": **NO** — it is non-relativistic only,
  Ostrogradsky-unstable, no Newtonian limit; Milgrom himself calls it unacceptable as a full theory. It is
  NOT a usable covariant MI completion. It *does* independently confirm the deep-MOND BTFR law the framework
  shares, and shows a *linear* MI+MG model is possible (no EFE) — useful context, not a tool.
- Singh's EJA "deriving" the spectrum: it derives **ratios** via the Jordan char. polynomial but
  self-describes (2605.24866, verbatim) as "an effective spectral organization, **not** a parameter-free
  replacement," with **fitted moduli (r, p, Φ_e)**. It does not supply the amplitude selector the framework
  lacks.

---

## 3. BOTH-WAYS BOTTOM LINE

**Genuinely checks out (credit):**
- √m 1:2:3 / mass 1:4:9 HOLDS (+0.31σ, +0.21σ) — not falsified, on prediction.
- m_τ/m_μ = m_s/m_d HOLDS (+1.29σ mass / +0.21σ Teli-√) — not falsified.
- Koide post-break SIGN matches the framework's drift (both POSITIVE above 2/3); magnitudes same order (2.08×).
- Deep-MOND BTFR law V∞⁴=GMa₀ is IDENTICAL between Milgrom-linear and the framework (6 sig figs).
- δ²=3/8→Q=5/12 and δ²=3/2→Q=2/3 are sympy-exact, reproducing the framework's banked EJA note.
- Singh's EJA is the *same* F4/J₃(O)/Spin(8)-triality neighborhood the framework hosts, and *derives* the
  spectrum the framework only re-labels — a real, non-trivial flavor-sector cousin.

**Genuinely fails / is weaker than claimed:**
- Every flavor test is **NON-DIAGNOSTIC** at current precision — none is a sharp confrontation; the
  light-quark (u,d,s) errors (12–25%) and the unresolved running-Koide make them low-power.
- "Exact Koide from δ²=3/8" is **not literally correct** — δ²=3/8 gives 5/12; the 2/3 needs a separate
  centring (δ²=3/2).
- Milgrom 2503.07106 is **not** a covariant MI completion (non-relativistic, Ostrogradsky-unstable,
  no Newtonian limit; "unacceptable as a basis for a full-fledged MOND theory" — his words). a₀ is INPUT.

**Stays disjoint (no bridge):**
- Singh's program touches **NO** a₀/Λ — its only gravity gesture is a qualitative, self-admittedly
  undeveloped dark-U(1) "dark electromagnetism" at the **electroweak** scale, with NO a₀ value, NO
  a₀=c²√(Λ/32π), NO Z=√(32π/3). The overlap is **entirely flavor/Koide/triality; NONE in the a₀/Λ gravity
  sector.**
- Baez-Schwahn 2606.15235 is gauge-group-only — touches neither masses nor Λ; does **not** change the
  disjoint verdict.
- The dS↔SM-flavor bridge remains absent across the entire surveyed frontier.

**NET:** a real, non-trivial shared-flavor-structure cousin (Singh/Teli EJA) with an independently-arrived
Koide drift *sign* match — worth tracking — but **no new derivation of the framework's signature numbers
(Z, Λ value, a₀) and no gravity bridge.** Consistent with the banked corpus: triality hosts the SHAPE,
not the amplitude or a₀. No re-overclaim; no dismissal.

---

## 4. FLAGGED — predictions NOT pinnable to a real fetched number

- **Singh K_th = 0.66916** is pinned verbatim from ar5iv 2508.10131, but its **derivation chain** (the exact
  size of the "endpoint tilt" on the first lepton rung) is asserted, not reproduced here from first
  principles — I verified the *value and sign*, not that the tilt magnitude is forced. Treat the +0.374%
  as a quoted result, not an independently re-derived one.
- The framework's **+0.18% / 178σ** Koide drift is taken from the banked corpus (WEIRDNESS_LEDGER_WAVE4 /
  KOIDE_CHANNEL_MEASURE / MAXIMAL_MIXING), not recomputed in this session.
- 2604.06288's **δ_CP = ±π/2 (maximal leptonic Dirac phase)**: the prediction is pinned (abstract), and it
  is qualitatively DISFAVORED by current NuFIT global fits (best-fit ~195–230°, CP-conserving allowed), but
  I did **not** fetch a current NuFIT χ²(δ_CP=90°) to put a sigma on it — flagged as "disfavored, not
  excluded," no number.
- **Majorana vs Dirac** light neutrinos (2604.06288): undecidable now (pending 0νββ: KamLAND-Zen / LEGEND) —
  no number possible.
- Milgrom Eq. numbers (8/14/16/17/28) are pinned from the fetched text; the **Ostrogradsky instability /
  thin-shell log-divergence** are quoted from his own prose, not re-derived here.
