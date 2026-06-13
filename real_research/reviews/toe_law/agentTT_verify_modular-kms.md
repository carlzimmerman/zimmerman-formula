# agentTT VERIFY — adversarial referee of ROUTE 2 (MODULAR/KMS selection of the DSSYK placement)

**Date 2026-06-13. Target:** `agentTT_routeModular.md` — claim that the Tomita–Takesaki
modular flow of the Gibbons–Hawking state SELECTS the DSSYK **center** placement, verdict
**CENTER-FAVORED-STRENGTHENED** (explicitly *not* CENTER-FORCED).

**CENTRAL MISSION (the brief):** distinguish **FORCING** (the edge placement is provably
EXCLUDED by the modular/SL(2,R) structure) from **CONSISTENCY** (the center fits, but the
edge is not ruled out). Independently re-derive the rep/modular-weight claims; if the route
claimed CENTER-FORCED, check ruthlessly whether the edge is genuinely the wrong rep / a
forbidden modular weight or could live in another admissible sector; respect agentR's
"terminal at the algebra"; regrade. **Default assumption: 'forced' is overclaimed; honest
likely outcome CENTER-FAVORED-STRENGTHENED.**

Compute-first. Three independent scripts (all run, outputs reproduced):
`agentTT_verify_p1_repweight.py` · `agentTT_verify_p2_forcing.py` · `agentTT_verify_p3_steelman.py`.
The route's own six scripts were also re-run end-to-end: all execute and emit the claimed
numbers (KMS residual 6.2e−33 at β=2π / 0.043 at β=4π; edge β=∞; ladder norms; θ_v=π/2 root).

---

## 1. RE-DERIVATION of the structural inputs (V1–V3): the route's machinery CHECKS OUT

Independently recomputed, no route conclusions imported (`agentTT_verify_p1_repweight.py`):

- **(V1) Boost-fixed root.** `Re(E_pole) = cos(θ_v)·cosh((Δ+n)λ)`; since `cosh ≥ 1 > 0`,
  `Re=0 ⇔ cos(θ_v)=0`, and `solveset` on `[0,π]` returns **exactly `{π/2}`**, *n-independent*
  (every rung fixed at the same θ). **CONFIRMED.** *Caveat re-derived and confirmed:* the
  selector is sharp only at finite λ; small-λ `Re/|Im| = cot(θ)(Δ²λ²+3)/(3Δλ)` → it
  **degrades to O(λ)** semiclassically (agentS's own flagged limitation — not new, but
  load-bearing for "boost-fixed" being a sharp selector).
- **(V2) Discrete-series ladder norm** `(n+1)(2Δ+n)`: both factors strictly positive for
  `n≥0, Δ>0` ⇒ closed unitary lowest-weight module. **CONFIRMED** (symbolic + samples).
- **(V3) Edge homogeneous weight:** `(e^a t)^{−3/2}/t^{−3/2} = e^{−3a/2}` ⇒ weight **−3/2**,
  a pure number, **Δ-independent** (the soft-edge exponent `s_E=1/2` is fixed by the sqrt
  edge; Δ enters amplitude only). **CONFIRMED.**

So the route did not fabricate its inputs: center = boost-fixed, two-sided (A≈0.5), discrete
ladder lowest-weight Δ; edge = one-sided (A≈0), Δ-independent homogeneous weight −3/2. These
reproduce agentS exactly. **Nothing in the route's arithmetic is wrong.**

---

## 2. THE DECISIVE TEST — is the edge a FORBIDDEN rep, or a DIFFERENT admissible sector?

The route's FORCING-direction rests on **one** pillar (Part 3B/3C, Part 5/H3): *"the GH
modular flow is realized on the lowest-weight DISCRETE series; the edge carries a
continuous-series weight −3/2, hence the edge is EXCLUDED."* I attacked that pillar four
independent ways (`agentTT_verify_p2_forcing.py`); **all four say the pillar yields
CONSISTENCY, not FORCING:**

- **(A) Continuous series is NOT forbidden in dS.** A massive scalar in dS_d is quantized on
  the **principal** (`Δ=(d−1)/2+iμ`, complex weight — for dS₃: `1+iμ`) or **complementary**
  (`Δ∈(0,d−1)` real) — the **continuous** series of SO(d,1). The genuine normalizable
  **discrete** series is the *special* SL(2,R)~SO(2,1) / dS₂ lowest-weight tower — exactly
  the q→1 DSSYK ladder. So *"GH modular flow lives on the discrete series"* is true only for
  that special sector; a continuous-series weight is **the generic dS-scalar sector, not a
  forbidden one**. The edge's rep class is therefore **not excluded by dS rep theory**.
- **(B) `Re ω=0` is NOT a discrete-series selector.** Lopez-Ortega dS QNMs
  `ω=−iH(2n+l+Δ_±)`: for **light/real-Δ** scalars `ω` is purely imaginary (`Re=0`) — and
  real-Δ spans **both** the complementary (continuous) *and* discrete series; only **heavy**
  (principal, complex-Δ) scalars ring (`Re ω = H√3 ≠ 0` at m=2H, recomputed). So the route's
  `(P-fixed)` property excludes **ringing/heavy** modes, **not** the edge's rep class — a
  strictly weaker statement than a rep-theoretic exclusion.
- **(C) Edge one-sidedness is a CONTINUOUS band-edge artifact, not a binary T=0 certificate.**
  For a probe at band energy `E_v∈[−1,1]`, the 2pt support is `[−1−E_v, 1−E_v]`; the
  fraction with ω<0 slides **continuously** 0.500 → 0 as `E_v→−1` (computed:
  0.500/0.250/0.050/0.0005 at `E_v=0/−0.5/−0.9/−0.999`). The edge's `A≈0` is the *kinematic*
  statement "the probe sits at the spectral boundary, half the band is absent" — a
  **continuous** placement property, not a discrete certificate of a forbidden modular sector.
- **(D) The boost does NOT act on the discriminating label** (the route's **own** concession,
  Part 2A/H5): `σ_t|E_v⟩ = e^{iE_v t}|E_v⟩`, `E_v=cos θ_v` conserved ⇒ `θ_v` is a
  modular-invariant superselection label. **A symmetry that does not act on the discriminating
  label cannot FORCE its value** — it can only declare which fixed value is *consistent with*
  being the GH boost-KMS state. By construction this is a **necessary-condition / consistency**
  argument, not an algebraic forcing that forbids writing the edge state.

---

## 3. STEELMAN (both-ways rule) — where the route is GENUINELY right; where forcing fails

Per Carl's working rule, a "not-forced" finding must survive the route's best rebuttals as
rigorously as a "works" claim (`agentTT_verify_p3_steelman.py`):

- **(S1) Concede the real point.** The static-patch modular Hamiltonian `L_0` *does* have the
  **discrete QNM ladder** `{Δ+n}` as its resonance spectrum; the center **is** its
  lowest-weight module; the edge's power-law (branch-cut) **is not** that module. My point (A)
  refutes the *blanket* "continuous-series forbidden in dS," **not** the narrower "for the
  RELAXATION/QNM content, the center is the natural `L_0` module." So the route's
  **favoring is real**, and agentS's edge-wound is genuinely **deepened** — the edge does not
  merely *fail* the ladder, it carries the wrong modular weight *for the GH state*.
- **(S2) But the "not-a-slide" rhetoric overshoots.** The route argues (H3) the edge is the
  β=∞ point "no dS occupies," structurally *unlike* SS's slide over finite values. Mapping the
  spectral asymmetry to an effective inverse temperature `βw = ln((1−A)/A)`: interior
  placements have **finite** `βw` (0.00/1.10/2.94 at A=0.5/0.25/0.05) and the edge is the
  `β→∞` **endpoint** of that **continuous** family. So the placements *do* form a continuous
  one-parameter line of effective temperatures with the edge at the boundary — **structurally
  the SS slide after all.** The route's binary "discrete-vs-continuous series" is the q→1
  idealization; at finite λ the placements interpolate continuously. *In fairness:* A=1/2
  (center) is the **unique** value matching the **fixed** `T_dS=H/2π` and sits at the
  **symmetric** point (not tuned) — so the center is genuinely **special/favored**, even
  though the edge is not **banned**.
- **(S3) The decisive arbiter — the edge state EXISTS.** Per the brief, *"any surviving edge
  sector ⇒ CENTER-FAVORED-STRENGTHENED at best, not FORCED."* **agentR (banked,
  CONTESTED-TERMINAL):** the chord algebra supplies **both** a natural center state (N̂-vacuum
  / infinite-T) **and** natural edge states (H-extremal) — both admissible cyclic vectors in
  the **same** chord Hilbert space. The edge is **not algebraically forbidden**; it is a
  writable GNS state. **There is a surviving admissible edge sector** ⇒ by the brief's own
  criterion the verdict **cannot be CENTER-FORCED.**

---

## 4. RECOMPUTE AGREEMENT

Every load-bearing number the route reports reproduces independently: the boost-fixed root
θ_v=π/2 (unique, n-independent); ladder-norm positivity; edge weight −3/2 / Δ-independence;
the KMS residual hierarchy (≈0 at β=2π, 0.043 at β=4π — though, **as the route itself
concedes in its Part 6 "honest scope" note, the ≈0 residual is partly by-construction**:
`G_+ = ρ/(1−e^{−βν})` satisfies its own Bose identity; the load-bearing content is that the
center's spectrum *is* the discrete ladder and the edge's one-sided support admits no
finite-β balance); edge β=∞ from one-sidedness. **recompute_agrees: yes.**

---

## 5. FORCING vs CONSISTENCY — the verdict on the central question

**The modular argument is a CONSISTENCY / FAVORING, not a FORCING.** The edge is **not**
excluded:
1. its rep class (continuous series) is **not forbidden** in dS (generic massive-scalar
   sector) — (A);
2. the `Re ω=0` and one-sidedness "certificates" are **not** binary rep-theoretic bans —
   `Re=0` spans complementary+discrete series (B), one-sidedness slides continuously with
   placement (C, S2);
3. the boost **does not act** on the placement label (D, route's own concession) — so it
   **cannot force**, only impose a necessary condition;
4. **the edge state EXISTS** as an admissible chord-algebra vector (S3, agentR) — a surviving
   sector, which by the brief's criterion **forecloses CENTER-FORCED**.

What the modular structure **does** deliver (genuinely, and more than agentS alone): the
center is the **unique** placement that is simultaneously boost-fixed, two-sided/balanced
(A=1/2 ⇔ the **fixed** `T_dS=H/2π`), and the discrete-series lowest-weight `L_0` module — a
**theorem-backed** (Gibbons–Hawking + Bisognano–Wichmann geometric modular action + Allen
uniqueness), **state-level** *necessary condition for being the GH state* that **only the
center meets**. This is a **real favoring** — strictly stronger than a numerical coincidence,
and not the SS open-knob failure mode (the GH temperature is a fixed theorem input, not a
free `c_χ↔H` ratio). It **deepens** agentS's edge-wound (the edge carries the *wrong modular
weight for the GH state*, not merely a different falloff). But it **stops at favoring**: the
edge is a non-GH, but **writable and not-forbidden**, sector.

---

## 6. RESPECT agentR — has anything been DERIVED, or restated?

agentR's verdict **CONTESTED-TERMINAL "at the algebra level"** is **intact and untouched.**
The chord *algebra* still supplies both states and **cannot pick** — nothing here derives the
placement *from the algebra*. The route's contribution is a **state-level** (modular/KMS)
*favoring* the algebra-level sweep did not have; it is **not** an algebra-level derivation.
The honest residual flagged by the route (modular covariance presupposes DSSYK↔dS, and does
not prove it) is real and correctly stated. So: **a state-level favoring is established;
nothing is DERIVED at the algebra level; agentR stands.**

---

## 7. REGRADE — **CONFIRMED** at **CENTER-FAVORED-STRENGTHENED**

The route's stated verdict word is already **CENTER-FAVORED-STRENGTHENED** (and the JSON
`placement_constrained` reads "center-favored-not-forced"). **It did NOT overclaim a
forcing in its verdict.** My independent recompute agrees with every number and **confirms
the forcing-vs-consistency call**: this is a CONSISTENCY/FAVORING (theorem-backed,
state-level), the edge is **favored-against but not excluded**, a surviving admissible sector
remains, and agentR's algebra-level terminality is unmoved.

- **regrade: CONFIRMED**
- **regraded_verdict: CENTER-FAVORED-STRENGTHENED**
- **recompute_agrees: yes**
- **forcing_or_consistency: CONSISTENCY** (a strong, theorem-backed FAVORING; the edge is the
  wrong rep *for the GH state* but is not a forbidden SL(2,R)/chord-algebra object — it exists
  as a writable sector, so it is not FORCED-out).

**Honesty notes (both directions, per the working rule):**
- *Against the route:* two sub-arguments in Parts 4–5 are **rhetorically stronger than the
  math licenses** — (i) `Re ω=0` is presented as effectively a discrete-series selector, but
  it is a real-weight property spanning complementary+discrete series (my B); (ii) the "binary
  discrete/continuous, NOT an SS slide" framing (H3) is the q→1 idealization — the effective
  temperature `βw=ln((1−A)/A)` slides continuously over placements, edge at the β→∞ endpoint
  (my S2). Neither overturns the verdict (the route's final word is still favored-not-forced),
  but the FORCING-adjacent language should be read as favoring, not exclusion.
- *For the route:* the central claim is **not** manufactured. The center genuinely is the
  unique boost-fixed + two-sided + discrete-`L_0`-module placement at the **fixed** `T_dS`,
  and the GH premise genuinely is a **theorem** (not SS's open knob). The edge-wound is really
  deepened to a modular-weight statement. Calling this merely "consistency, nothing gained"
  would **under-credit** it; it is a real, theorem-backed, state-level **favoring** — just not
  a forcing.

**ONE-LINE:** Independent recompute reproduces every TT number and confirms the call — the
GH modular/KMS structure **FAVORS** the center (unique boost-fixed, two-sided, discrete-`L_0`
placement at the fixed `T_dS`; a theorem-backed state-level necessary-condition that deepens
agentS's edge-wound) but does **NOT FORCE** it (continuous-series weights are not forbidden in
dS, `Re=0`/one-sidedness are not binary rep-bans, the boost does not act on the placement
label, and the edge state still EXISTS as a writable chord-algebra sector) ⇒ **CONFIRMED,
CENTER-FAVORED-STRENGTHENED**, agentR's algebra-level terminality intact.

## QUARANTINE
Held. Only computed: pole real-part root (θ_v=π/2), ladder-norm positivity, dilation weights
(−3/2 edge / Δ center), spectral-asymmetry→effective-β map, support fractions, dS QNM
real-parts (light vs heavy). `q=1/4`, `ζ̃`, `(16π/3)^{1/4}` untouched, never asserted. No
coefficient touched.

## FILES (all in `real_research/reviews/toe_law/`)
`agentTT_verify_p1_repweight.py` · `agentTT_verify_p2_forcing.py` · `agentTT_verify_p3_steelman.py`
