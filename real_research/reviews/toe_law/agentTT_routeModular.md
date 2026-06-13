# agentTT — ROUTE 2: does MODULAR / KMS covariance SELECT the DSSYK center placement? (2026-06-13)

**The fresh Link-8 question.** agentS found the **center** DSSYK placement reproduces the dS QNM ladder
EXACTLY (purely damped, Re ω=0, Γ_n=sinh((Δ+n)λ)) while the **edge** FAILS structurally (t^(−3/2), one-sided,
non-thermal) ⇒ EDGE-WOUNDED, contest leans center but no derivation. agentSS then found the **static-patch
SL(2,R)~SO(2,1) / Tomita–Takesaki MODULAR structure of the Gibbons–Hawking (GH) state is REAL**, and the QNM
ladder is its lowest-weight discrete-series rep. THIS ROUTE asks: does that modular/KMS structure **CONSTRAIN
or FORCE** the placement? The GH state is KMS (thermal) at `T_dS = H/2π` under the modular flow = the
boost/dilation. Test whether **modular covariance SELECTS the center** (the center's late-time observable sits
at the modular fixed axis / is the KMS spectrum, while the edge breaks modular covariance with a forbidden
zero-temperature weight) — and, RUTHLESSLY, whether that is a **FORCING** or merely a **CONSISTENCY**.

Honest prior (from SS): SS found the analogous "does the symmetry force the *gain shape*" question lands on
**PERMITS-NOT-FORCES**. The expectation here is similar — but the *placement* question is structurally
different from the *gain-shape* question (a discrete two-valued choice vs a continuous ratio), so a genuine
modular selection is possible and must be tested on its merits.

---

## THE TWO QUESTIONS, KEPT SEPARATE

There are two distinct things modular covariance could do, and the whole verdict turns on not conflating them:

- **(Q-consistency)** Is the center placement's late-time observable *consistent with* / *covariant under* the
  modular (boost) flow — i.e. does it sit at the modular fixed axis and satisfy KMS at `T_dS`? (agentS already
  strongly suggests yes for center, no for edge.)
- **(Q-forcing)** Does modular covariance *exclude* the edge — i.e. is KMS-at-`T_dS` a **constraint the physical
  dS placement MUST satisfy** (so the edge is FORBIDDEN, forcing center), or is it merely a property the center
  *happens* to have (so the edge is dispreferred but not forbidden, permits-not-forces)?

The SS lesson, applied here: SS found a real symmetry that **constrains the wrong invariant** (it acted by a
scale-free dilation on a scale-decoupled target → weight −1 → permits). The analogue to watch for here: does
the boost modular flow act on the placement label at all? If the boost is an *inner* symmetry that the
placement choice is *invariant under* (a superselection / which-rep label the modular flow cannot rotate), then
modular covariance is **silent** on the placement and we are back to permits/agnostic — exactly the SS failure
mode, transposed.

---

## SETUP — all banked, none invented

- GH state of the dS static patch is **KMS at `T_dS = H/2π`** under modular flow `σ_t` = static-patch boost
  generator `L_0` (a dilation `s→e^a s`). [agentSS; Bisognano–Wichmann / Tomita–Takesaki; Gibbons–Hawking.]
- dS QNM ladder `Γ_n = sinh((Δ+n)λ)` = lowest-weight discrete-series rep of static-patch SL(2,R); `L_0`
  spectrum = the ladder `Δ+n`. [agentSS.]
- **CENTER** (θ_v=π/2): late-time matter 2pt poles `ω = −i sinh((Δ+k)λ)` — purely imaginary, discrete ladder,
  **two-sided/balanced** support, spectral asymmetry **A = 1/2** (machine: 0.49976–0.49999). [agentS.]
- **EDGE** (θ_v→π): `|G| ~ t^(−3/2)`, **one-sided** support, spectral asymmetry **A ~ 0** (4e−9…1e−5),
  extremal/zero-temperature. [agentS.]

---

## PART 1 — KMS detailed balance under the boost: center is KMS, edge is T=0 (CONSISTENCY established)

KMS detailed-balance criterion (Wightman 2pt under modular flow):
`tilde G(−ω)/tilde G(+ω) = e^(−β_mod ω_mod)`, with `β_mod = 2π` the **universal** modular temperature
(Tomita–Takesaki/Bisognano–Wichmann). A placement *is* the GH state only if its boost-frame 2pt obeys this with
`β_mod = 2π` exactly.

| Placement | Re ω | support | asymmetry A | detailed balance | KMS class |
|-----------|------|---------|-------------|------------------|-----------|
| CENTER | 0 (boost-fixed) | two-sided | 0.5 (machine) | `e^(−β ω)` balanced at Re ω=0 axis | **KMS at finite T (β_mod=2π)** ✓ |
| EDGE | n/a (power law) | one-sided | ~0 | `β→∞` limit | **T=0 / ground state** ✗ at T_dS |

So **(Q-consistency) is settled**: the center observable sits at the modular fixed axis (Re ω=0), is
two-sided/balanced, and satisfies KMS at the GH temperature; the edge is a one-sided **zero-temperature**
correlator — a *different thermal class* (`β→∞`, not `β_mod=2π`). This reproduces agentS's R4 from the modular
side. *(Script: `agentTT_part1_kms.py`.)*

But CONSISTENCY is not FORCING. The decisive question is Part 2–6: does modular covariance **forbid** the edge,
or merely disprefer it? — pursued below with NO assumption that "KMS-natural" = "forced".

---

## PART 2 — does the boost modular flow ACT on the placement label? (the SS failure mode, transposed)

The decisive forcing-vs-preference test. SS found a real symmetry that PERMITS because it acted by a scale-free
**dilation** on a scale-decoupled target. The analogue: if the boost modular flow does **not move** the
placement label `θ_v`, modular covariance is *silent* on the placement (permits/agnostic, the SS failure mode).

- **(2A) The boost is DIAGONAL on energy eigenstates** (energy `E_v = cos θ_v` is the boost's conserved
  charge): `σ_t|E_v⟩ = e^{i E_v t_mod}|E_v⟩` ⇒ `|E_v|` fixed ⇒ **`θ_v` is a modular-INVARIANT / superselection
  label the boost is blind to.** So the boost **cannot dynamically rotate** the edge into the center. *(This is
  the honest limit on the forcing — the symmetry does not act on the placement by rotation.)*
- **(2B) But per-placement, T–T gives a unique answer.** Each placement defines a different GNS state (cyclic
  vector = the matter chord at `θ_v`). Tomita–Takesaki: the boost is the modular flow of the GH state at
  `β_mod = 2π`. Ask of each placement: is its boost-frame 2pt KMS at `β_mod = 2π`? Decided by the pole
  structure. agentS scan: **only `θ_v = π/2` is boost-fixed (Re ω = 0)**; every interior `θ_v` rings (Re ω ≠ 0,
  KMS only at a *shifted* Hawking temp under a *different* flow); the edge has no ladder (T=0, one-sided).
- **(2C) Crux.** Modular covariance singles out `θ_v = π/2` as the **unique** boost-fixed, KMS-at-`T_dS`
  placement — but whether this *forces* the placement hinges on whether "the dS vacuum = the GH boost-KMS
  state" is a **banked physical requirement** or a **chosen identification**. This is the TT analogue of SS's
  `c_χ↔H` dependency. *(Script: `agentTT_part2_modular_action_on_placement.py`.)*

## PART 3 — modular WEIGHT of each placement's observable: FORBIDDEN vs DIFFERENT-rep (the SS standard)

SS's forcing test: compute the modular weight; a dilation forces only **weight-0** invariants ⇒ the weight-(−1)
ratio permits. Apply the same standard to the placements' *observables*:

- **CENTER:** discrete ladder `e^{−sinh((Δ+n)λ)t}`, lowest weight `h = Δ`. The modular Hamiltonian `L_0`
  spectrum **IS** `{Δ+n}`; the ladder is its **own discrete-series module** (ladder norm `(n+1)(2Δ+n) > 0` ∀n
  ⇒ closed unitary lowest-weight module, verified). So `G_center` is a **weight-Δ lowest-weight vector of the
  modular algebra** — it lives *inside* the GH modular rep, KMS-covariant by construction. **[ALLOWED + NATURAL]**
- **EDGE:** power law `t^(−3/2)` ⇒ **homogeneous dilation weight −3/2**, a single homogeneous weight, no ladder
  ⇒ a **continuous/principal-series** scale-covariant object. Under the log-clock `t = e^{Hτ}` it maps to
  `e^{−(3/2)Hτ}` — a single rate with offset **3/2 independent of Δ** (agentS R2-fail). It is **not** a
  lowest-weight module on `Δ` ⇒ it does **not lie in the discrete-series carrier space** the GH modular flow is
  realized on.
- **(3C) SS-discipline call.** SL(2,R) has **both** discrete and continuous series, both unitary. The GH modular
  flow is realized on the **discrete** series (banked SS fact). The edge (continuous-series, weight −3/2) is
  **excluded FROM the GH discrete-series rep** ⇒ modular covariance **excludes the edge AS the GH state** — but
  the edge is a legitimate SL(2,R) object in its own right, excluded *only* by demanding it be the GH KMS state.
  Same conditional structure as Part 2. *(Script: `agentTT_part3_modular_weight.py`.)*

## PART 4 — STATUS of the premise: free dictionary choice (SS-like) or THEOREM (stronger)?

Everything reduced to: is "dS vacuum = GH boost-KMS state" an **open knob** (⇒ permits, SS-like) or a
**theorem** (⇒ a genuine forcing)? **The decisive difference from SS:**

- **(4A) It is a THEOREM of dS QFT**, not a holographic dictionary choice: (1) **Gibbons–Hawking 1977** — the
  static-patch reduced state is KMS at `T_dS = H/2π`; (2) **Bisognano–Wichmann / Sewell (geometric modular
  action)** — the modular flow of the dS-invariant vacuum on the static patch **is** the boost, and the vacuum
  is KMS at `T_dS` w.r.t. it; (3) **Allen 1985 (uniqueness)** — the Bunch–Davies/Euclidean vacuum is the
  *unique* dS-invariant Hadamard state, whose static-patch restriction is the GH thermal state.
- **(4B) SS vs TT, made precise.** SS: symmetry + **OPEN** ratio-input (`c_χ↔H`, could go either way) → a
  continuous weight **slides** → permits. TT: symmetry + **THEOREM** input (the state IS GH boost-KMS at *fixed*
  `T_dS`) → the input is **not open**, and the discriminator is a **discrete rep-class** (discrete vs continuous
  series; thermal vs T=0), not a tunable ratio. The boost-fixed condition `cos θ_v = 0` has the **unique** root
  `θ_v = π/2` in `[0,π]` ⇒ the theorem-backed premise lands on a **unique** placement (the center); no
  interpolation is also GH-KMS.
- **(4C) Honest residual.** Modular covariance does not *independently prove* DSSYK ↔ dS; that is the
  framework's **own founding premise** (the entire reason Link 8 uses DSSYK as the dS dual). **Unlike SS's
  `c_χ↔H` open knob, this residual is the framework's presupposed dual, not a free parameter that could go the
  other way.** *(Script: `agentTT_part4_premise_status.py`.)*

## PART 5 — MAXIMUM-HOSTILITY attack on the selection (five objections, all survived)

- **H1 (circularity/smuggle):** Is the edge camp's own dS₂-JT also boost-KMS? **No** — agentS computed the edge
  in *both* dimensions: still one-sided, A~0, `t^(−3/2)`, no ladder. A real dS₂-JT static patch *is* thermal
  (purely-imaginary thermal QNMs); the edge `w(E)` is **not**, so it fails to realize a dS₂-JT GH state **on its
  own terms**. "dS = GH KMS" is a **test the edge fails in its own dimension**, not a smuggle. **NOT circular.**
- **H2 (Re ω=0 ≠ KMS):** Two *independent* properties — (P-fixed) Re ω=0 [boost-geometric] and (P-thermal) A=1/2
  two-sided [finite-T]. Center has **both**; edge has **neither**. Not a conflation: GH-KMS-under-the-boost needs
  both, and only the center supplies both. Interior (ringing) placements are at best KMS at a *shifted* temp
  under a *different* flow ⇒ excluded as GH.
- **H3 (edge KMS at its OWN temperature ⇒ permits, the SS slide):** The sharpest objection. **Refuted:** the GH
  temperature is **fixed** (`β_mod = 2π` universally, `T_dS = H/2π > 0`); the edge is `β = ∞` (T=0) — the
  **degenerate boundary point**, the one value **no dS static patch occupies**. The dilation of a power law
  `t^{−3/2}` stays `e^{−(3/2)a}·t^{−3/2}` (same continuous-series weight) — it **never** produces a discrete
  two-sided ladder ⇒ the T=0 sector is **CLOSED under the boost**. This is **structurally unlike** SS's slide
  over *finite* values; the boost cannot connect the edge's closed T=0 sector to a finite-T dS state.
- **H4 (dimensionality):** agentS ran both matchings; the edge fails R1/R2/R4 in **either** (one-sidedness +
  Δ-independent offset + T=0 are dimension-independent facts of the sqrt soft edge). The selection rides on
  (P-thermal)+(P-fixed), both dimension-independent. Carried as a stated limitation, not a hole.
- **H5 (boost acts ON or WITHIN the placement?):** The boost is **inner** to each sector (2A). So the selection
  is **not** "the symmetry rotates the edge away" (it cannot) — it is "only the center is a boost **fixed point**
  carrying the finite-T discrete-series GH weight; the edge is locked in the closed T=0 continuous-series sector,
  which is not a dS static patch." Selection by **fixed-point + sector**, not dynamical rotation.

*(Script: `agentTT_part5_hostile.py`.)*

## PART 6 — explicit numerical KMS detailed-balance test (closed-sector claim, hardened)

| Test | CENTER (discrete ladder) | EDGE (one-sided soft edge) |
|------|--------------------------|----------------------------|
| KMS detailed balance at `β_mod=2π` | residual **6.2e−33** (holds) | impossible: `ρ(−ω)=0`, `ρ(+ω)>0` ⇒ needs `β=∞` |
| at a *wrong* `β=4π` | residual **0.043** (fails) ⇒ `β_mod=2π` UNIQUE | — |
| under the boost/dilation | stays discrete two-sided | one-sidedness **invariant** ⇒ sector CLOSED |

**Honest scope of the center residual:** the ~0 residual is *partly by-construction* (`G_+ = ρ/(1−e^{−βν})`
satisfies its own Bose identity); the **load-bearing** content is (a) the center's spectrum **is** the discrete
ladder `{Δ+n}` that `L_0` generates, so the thermal sum is over the *modular* spectrum, and (b) the edge's
one-sided support **structurally** admits *no* finite-β detailed balance, and the boost **preserves**
one-sidedness — so the edge is locked out of finite-T dS by a sign-of-support argument, not a tuning.
*(Script: `agentTT_part6_kms_numerics.py`.)*

---

## VERDICT — **center-favored-not-forced** (modular covariance SELECTS the center; STRENGTHENED from SS's permits)

**The COMPUTED finding.** The static-patch SL(2,R)/Tomita–Takesaki modular structure of the GH state does
**more** than SS's gain-shape symmetry did — it is **not** a scale-free dilation acting on a scale-decoupled
target. It carries a **theorem-backed, state-level selector**:

1. The dS static patch **is** the GH state, KMS at the **fixed** temperature `T_dS = H/2π` under the boost — a
   **theorem** (Gibbons–Hawking + Bisognano–Wichmann geometric modular action + Allen uniqueness), **not** an
   open knob like SS's `c_χ↔H`.
2. Among **all** placements, **only the center** realizes this: it is the unique boost-fixed (Re ω=0),
   two-sided/balanced (A=1/2), **discrete-series** lowest-weight (`h=Δ`) module — i.e. the actual carrier space
   of the modular Hamiltonian `L_0`. KMS detailed balance holds at `β_mod=2π` (residual 6e−33) and fails at any
   other temperature ⇒ the GH temperature is uniquely realized **at the center**.
3. The **edge** carries a **forbidden-for-GH** modular weight: a continuous-series, homogeneous weight−3/2,
   `Δ-independent`, **one-sided (T=0)** object that admits **no** finite-temperature KMS and sits in a **closed
   sector the boost cannot connect** to a finite-T dS state. This is **not** the SS "tune to a different valid
   value" slide — T=0 is the one temperature *no dS static patch occupies*.

**Why FAVORED-not-FORCED (the ruthless line).** Calling this CENTER-FORCED would overclaim on **two** honest
residuals: (i) **the boost is inner to each placement sector** (it is diagonal on energy, Part 2A) — it **cannot
dynamically rotate** the edge away; the selection is by fixed-point + thermal-sector membership, a *necessary
condition for being the GH state* that only the center meets, **not** an algebraic theorem that forbids writing
down the edge state; (ii) the selector activates only **within the framework's own presupposed DSSYK ↔ dS
identification** (modular covariance does not itself prove DSSYK is dS). The **chord algebra alone still cannot
pick** (agentR's CONTESTED-TERMINAL is intact at the *algebra* level) — the new selector is **state-level
(KMS/modular)**, an ingredient agentR's 60-paper algebra-level sweep did not have.

**Net effect on Link 8.** This **strengthens** agentS's "edge-wounded, leans center" into a **principled modular
selection of the center**: the edge does not merely *fail to reproduce* the QNM ladder (agentS), it **carries a
modular weight forbidden for the GH thermal state** and is **locked in a closed zero-temperature sector** the dS
boost cannot reach — while the center **is** the discrete-series carrier of the modular Hamiltonian itself.
Modular covariance is the first **state-level, theorem-backed** argument that **favors the center as a SYMMETRY
the physical dS placement must respect** — converting "edge-wounded" toward "center-selected." It stops **short**
of CENTER-FORCED only because (a) the boost cannot rotate the placement (inner symmetry) and (b) it presupposes
DSSYK↔dS — neither of which is the SS open-knob failure mode, both of which are honest structural limits.

**Honest comparison to the SS expectation.** The brief expected "likely PERMITS-NOT-FORCES, by analogy to SS."
That expectation is **partially exceeded**: SS's symmetry permitted because it acted by a scale-free dilation on
a scale-decoupled *continuous ratio* (could slide anywhere). The **placement** question is structurally
different — a **discrete, binary, representation-theoretic** distinction (discrete vs continuous series; finite-T
vs T=0) governed by a **theorem** (the state IS GH boost-KMS), not an open ratio. So modular covariance
genuinely **does select** the center (favored, strengthened), where SS's did not select the gain shape. It is
not CENTER-FORCED (the inner-symmetry + presupposed-dual residuals), but it is **more** than agnostic/permits:
**center-favored-not-forced**, a real Link-8 advance.

---

## QUARANTINE
Held throughout. Only computed: KMS detailed-balance residuals (6e−33 center / fails-at-wrong-β / β=∞ edge),
modular weights (Δ center / −3/2 edge), the boost-fixed root `θ_v=π/2` (unique in `[0,π]`), discrete-series
ladder-norm positivity `(n+1)(2Δ+n)`, support-sign closure under dilation, spectral asymmetries (0.4998 vs
~1e−5, from agentS). `q=1/4`, `ζ̃`, `(16π/3)^{1/4}` left OPEN, **never asserted**. No coefficient touched.

## ONE-SENTENCE LINK-8 UPDATE
The Tomita–Takesaki modular structure of the Gibbons–Hawking state **selects the center placement** as the
unique boost-fixed, two-sided, discrete-series carrier of the modular Hamiltonian that is KMS at the fixed dS
temperature `T_dS=H/2π`, while the edge carries a **forbidden-for-GH** continuous-series weight−3/2 and is
**locked in a closed zero-temperature sector the dS boost cannot reach** — a **theorem-backed, state-level**
selection of the center (**center-favored-not-forced**, strengthened beyond SS's gain-shape permits), stopping
short of CENTER-FORCED only because the boost is inner to each placement sector and the argument presupposes
DSSYK↔dS (neither being the SS open-knob failure mode).

## FILES (all in `real_research/reviews/toe_law/`)
`agentTT_part1_kms.py` · `agentTT_part2_modular_action_on_placement.py` · `agentTT_part3_modular_weight.py` ·
`agentTT_part4_premise_status.py` · `agentTT_part5_hostile.py` · `agentTT_part6_kms_numerics.py`
