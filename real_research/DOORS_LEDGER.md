# The Six Cosmogony Doors — Systematic Ledger

**C. Zimmerman, June 2026.** *All six doors explored rigorously: Door A driven and verified by me; Doors B–F each a
parallel investigation, every load-bearing number re-verified independently (`reviews/project_doors_verify.py`,
`project_doorA_static_patch.py`, `project_doorF_complexity.py`). Verdicts are honest — closed is called closed.*

---

## Executive scorecard

| Door | Question | Verdict | Status |
|------|----------|---------|--------|
| **A** | Derive a₀ from the de Sitter horizon | **Scale FORCED** (a₀∝c√Λ=cH via Unruh + Friedmann + Verlinde); coefficient Z **data-preferred** over Milgrom's 2π but not airtight | 🟢 **OPEN — the live constructive door** |
| **F′** | DSSYK↔dS microscopic underpinning | Genuine research ally for Door A; a **falsifiable** deep-MOND-sign target (chord overlaps) | 🟢 **OPEN — feeds Door A** |
| **C** | Cosmic topology — the shape of space | LIVE but narrow (band 27–33 Gpc + rotation topologies); framework **predicts nothing** — passenger | 🟡 **TESTABLE — watch Euclid, not a prediction** |
| **D** | DESI as falsifier | Framework **~3σ exposed**; phantom crossing of w=−1 (not mere drift) is the real threat to the static-Λ foundation | 🟡 **LIVE FALSIFIER — the thing that could break it** |
| **B** | Derive Λ / solve the CC problem | Does **not** derive Λ; an O(1) can't move 10¹²³. (I corrected the agent's Ω_Λ=1/Hsu over-reach — epoch artifact.) | 🔴 **CLOSED on deriving Λ** |
| **D** | No-boundary kick-off mechanism | **Sidesteps, not solves** the empty-universe problem; supplying Λ makes nucleation circular | 🔴 **CLOSED as a mechanism** |
| **E** | Low-entropy past / Boltzmann brains | Finite entropy does **not** rescue (needs ∞-dim); modestly **worsens** BB; must add a past-hypothesis postulate | 🔴 **OBLIGATION — a cost, not a win** |
| **F** | a₀ = complexity rate ("geometry unfolding") | **Slogan, not calculation**: exponent mismatch (a₀∝S^−½ vs rate∝S^+¹) overshoots by 10¹²³ | 🔴 **CLOSED as stated → redirects to F′** |

## The one-paragraph meta-verdict

The framework is **not** a theory that derives the universe from nothing, and the sweep says so plainly. Exactly
**one** thing is genuinely derived-ish — the MOND scale a₀ from the de Sitter horizon (**Door A**): its *scale* and
√Λ dependence are forced by three independent thermodynamic routes, and the data even prefer the framework's
coefficient Z over Milgrom's canonical 2π. Everything else either **relates without deriving** (Λ; Door B), is a
problem the framework **inherits unsolved** (the kick-off, Door D; the low-entropy past, Door E), is a **passenger
test** it doesn't drive (cosmic topology, Door C), or is an **evocative slogan that fails the numbers** (a₀ as
complexity, Door F). And it carries **one live falsifier**: if DESI's hint of a phantom crossing (w₀≈−0.5 today,
w crossing −1) hardens, the *constant*-Λ de Sitter horizon that makes a₀ a *derivation* dissolves into a present-day
coincidence. So the honest map: **a₀-from-the-horizon is real and worth pushing (via DSSYK↔dS); the cosmogony
(why Λ, why low entropy, what kicked it off) is unsolved here as everywhere; and DESI is the sword over it.**

## Door-by-door

### 🟢 Door A — a₀ from the de Sitter horizon (the one to push)
Two independent routes give a₀ = cH/O(1): **Unruh** (T_dS=ℏH/2πk_B → a₀=cH/2π) and **Friedmann free-fall**
(a₀=(c/2)√(Gρ_crit)=cH/Z, Z=2√(8π/3)). **Forced:** a₀∝c√Λ — the horizon origin of the MOND scale, robust across
Unruh, Friedmann, and Verlinde's entropic derivation. **Not uniquely forced:** the exact O(1) — Z=5.79 and 2π=6.28
agree to 8% and the data do not pick between them: on the same pure-Λ footing as Z, the observed ratio is
`cH_Λ/a₀ ≈ 4.5–4.9` (κ≈0.56–0.64), sitting *below* 5.79 — the framework's ½ is viable but at the **low edge**, not
softly favored. (The cross-footed `cH₀/a₀=5.46–5.91` is what makes it *look* like it lands on 5.79; see
`reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md` §4a.) **Next:** turn the scale-argument into a genuine derivation via the de Sitter static-patch
(modular Hamiltonian / stretched horizon).

### 🟢 Door F′ — DSSYK↔de Sitter (feeds Door A)
The complexity *slogan* (Door F) fails, but its neighborhood is gold: **DSSYK↔dS** (Narovlansky–Verlinde 2023) is
the first *solvable* "gravity from the de Sitter horizon," with R²_dS/G=4πN/p². The repo's own
`DSSYK_DEEPMOND_PROBLEM.md` reduces the deep-MOND **sign** to two chord-overlap calculations — a concrete,
**falsifiable** on-mission target (central overlap w(0)≠0 → MOND; =0 → not). This is where Door A gets a microscope.

### 🟡 Door C — cosmic topology (watch the data)
χ_rec=13.88 Gpc (matches Planck to 0.11%); matched circles kill simple tori below **27 Gpc** (the 20.6 Gpc torus
is dead, ~6 Gpc margin); surviving testable band **~27–33 Gpc** plus rotation/corkscrew topologies whose loops miss
us. **The framework predicts no topology and no scale** — S_dS≈10¹²² fixes Λ and the causal-patch size, nothing
about compactification (at most it argues for *three* dimensions). The only prior (Zel'dovich–Starobinsky's
unsuppressed toroidal nucleation) mildly favors *compactness* but leaves the size free. **Note:** CMB-S4 was
cancelled (Jul 2025); the real leverage is now 3-D large-scale structure — **Euclid DR1 (Oct 2026)** → Rubin →
21-cm (2030s). Honest: a beautiful corroboration if a topology is ever found, but "watch the data," not a forecast.

### 🟡 Door D — the kick-off, and DESI the falsifier
The de Sitter instanton action **is** the horizon entropy (S_E=3π/GΛ=A/4G=3.3×10¹²², verified exactly) — so the
horizon that sources a₀ doubles as the nucleation action. Elegant, but **circular**: supplying Λ externally removes
the empty-universe runaway only by removing the *prediction* the amplitude was supposed to make, demoting "the
action that kicked off the universe" to a constant weight on a pre-chosen background. The no-boundary↔tunneling
sign war (Feldbrugge–Lehners–Turok vs Hartle–Hawking–Hertog) is **unresolved**, only *parametrized* by the Robin-BC
family. **DESI:** ~3σ honest (≤4.2σ generous). A merely *drifting* Λ is survivable (a₀ responds as ½·δΛ/Λ ≈ ≤15%,
and the framework already allows a₀=cH(z)/Z) — **but** DESI's specific signature, a *phantom crossing* of w=−1, is a
change of **kind** (constant-Λ static horizon → dynamical fluid) the de Sitter derivation cannot represent. That,
not parameter drift, is the load-bearing exposure.

### 🔴 Door B — does not derive Λ (and a correction)
The identity 32π/Z²=3 is real, but the agent's leap to "this forces Ω_Λ=1, a liability" is an **epoch artifact** I
corrected: the two headline formulas hold at *different* epochs — **a₀(today)=cH₀/Z=1.13×10⁻¹⁰** (matches the data)
vs the **de Sitter floor c²√(Λ/32π)=9.36×10⁻¹⁰**... =9.36×10⁻¹¹, smaller by exactly √Ω_Λ=0.83. The framework's Λ is
a genuine **constant** (w=−1) and a₀∝H(z) is kinematic, so the Hsu w=0 critique is **misdirected**. What *does* stand:
fixing the coefficient **relates** a₀ to H₀; it does **not derive Λ's value** — ρ_Λ/ρ_Planck~10⁻¹²³, and an O(1)=5.79
moves that by zero orders. The cosmological-constant problem is untouched. **Action item:** the repo docs should label
a₀=c²√(Λ/32π) as the *de Sitter-asymptotic floor*, not today's a₀ (which is cH₀/Z, ~20% higher).

### 🔴 Door E — the low-entropy past (an added cost)
Boltzmann brains (ΔS~10⁴²) recur at exp(10⁴²) Hubble times; a full low-entropy universe at exp(10¹²²) — so in an
eternal thermal de Sitter, freak observers outnumber ordinary ones by exp(10¹²²):1. The one clean rescue
(Boddy–Carroll–Pollack: stationary de Sitter nucleates no brains) **requires an infinite-dimensional Hilbert
space** — the framework's *finite* ceiling (dim e^{S_dS}) is precisely the case BCP flag as *still* catastrophic, and
Davenport–Olum show the framework's own horizon supplies the decoherence that lets brains become real. So finiteness
**doesn't rescue and mildly worsens** the problem; the framework must **add a past hypothesis** — Chen's
initial-projection-as-law is the most native fit (a projector onto a low-dim subspace of the framework's own finite
Hilbert space). Stated openly as a **cost**, not advertised as a prediction.

### 🔴 Door F — a₀ is not a complexity rate
The decisive test: a₀ = a_Planck·(√π/Z)·**S_dS^(−1/2)** — the √S suppression is the **holographic area law**
(R/ℓ_P=√(S/π)=8.5×10⁶⁰), pure geometry. The 2025-established de Sitter complexity rate grows as **S_dS^(+1)**
(dC/dt~κ·S_dS·T_GH). Opposite powers of S: complexity-as-acceleration overshoots a₀ by ~S_dS≈10¹²³, and dividing the
overshoot out just returns plain cH with no complexity left. With "Complexity=Anything" making the O(1) non-unique
exactly where Z lives, complexity can't even pin the coefficient. **"Geometry unfolds = complexity grows" is
evocative analogy, not a calculation** — the calculable on-mission work is the entropy/density-of-states route (F′).

## Bottom line — where to spend effort

1. **Push Door A through Door F′.** The only genuinely constructive, on-mission frontier: derive a₀ from the de
   Sitter static-patch, using DSSYK↔dS and the chord-overlap deep-MOND-sign calculation as the microscope. This is
   where "gravity from the de Sitter horizon" is real and quantitative.
2. **Track Door D/DESI as the falsifier.** Watch whether the phantom crossing hardens — it is the single result that
   could break the constant-Λ foundation. Distinguish *drift* (survivable) from *crossing* (fatal).
3. **Fix the Door B documentation.** Label the two a₀ expressions by epoch (today cH₀/Z vs de Sitter floor
   c²√(Λ/32π)); stop implying Λ derives today's a₀ directly.
4. **State Doors C and E as honest costs/passengers**, not wins: topology is "watch Euclid," the low-entropy past is
   an added postulate. Don't overclaim either.
5. **Door B/CC and the kick-off (D) are closed** — the framework inherits these unsolved, like every other. Naming
   that plainly is the honest move.
