# dS₄/CFT₃ BOUNDARY ANOMALY → SM FORCING: the deep swing (2026-06-26)

**The question (Carl's deepest dS/CFT swing):** the framework's premise is that we live inside an
*inverted black hole* = the de Sitter / cosmological horizon. Strominger dS/CFT (hep-th/0106113,
Anninos-Hofman) maps the **dS₄ bulk** to a **CFT₃ boundary** at future infinity. In 10D, the perturbative
chiral *hexagon* anomaly (Green-Schwarz) **FORCES** the gauge group: anomaly cancellation pins
`dim G = 496`, and `SO(32)` / `E₈×E₈` are the only solutions. **Does the dS/CFT boundary anomaly likewise
FORCE an SM feature** (gauge group, N_gen = 3, fermion content / hypercharge relation) **non-circularly**,
or is it **structurally capped** at the discrete Z₂/Z₁₆ anomalies the SM already passes?

**VERDICT: (B) STRUCTURALLY CAPPED — `REAL-DOOR-forces-SM` is FALSE.** The deepest swing **does not
connect**, and the reason is structural, not a failure of effort: **the dS/CFT boundary is 3D = ODD, and the
content-forcing mechanism that exists in 10D is mathematically *unavailable* in odd dimensions.** Every 3D
anomaly is a finite-abelian (Z₂/Z₁₆) congruence that the SM satisfies *trivially, for every N_gen*. Nothing
is OUTPUT; the SM passes by virtue of already being a consistent 4D chiral theory. This is the deep,
definitive null the LOW prior anticipated — **3D ≠ 10D, structurally**. No manufactured win, no
high-priesting. Where the structural home is genuine (SO(4,1) = Conf(S³); the boundary IS a non-unitary
CFT₃) it is credited — but a hostable home is not a deriving bridge.

All five sub-computations were re-verified **clean-room** (independent of the asserted sub-scripts):
`/tmp/dscft_independent_verify.py`, `/tmp/witten_and_inflow_verify.py`, `/tmp/nonunitary_verify.py`,
plus the banked `/tmp/parity_anomaly_sub1*.py`. Every load-bearing number reproduced.

---

## THE STRUCTURAL CRUX (the one fact that settles it)

The chiral gauge anomaly in `d` spacetime dimensions is governed by the **(d+2)-form** anomaly polynomial
`I_{d+2}` (Alvarez-Gaumé–Witten / Stora–Zumino descent). A *perturbative, continuous, ℝ-valued* gauge
anomaly — the kind that can produce a **continuum equation** on the group label and thereby *force* the
group — requires the symmetric trace `tr F^{(d+2)/2}`, i.e. an **integer** power `n = (d+2)/2` of the
field-strength 2-form.

| d | anomaly form-degree (d+2) | F-power (d+2)/2 | perturbative chiral gauge anomaly? |
|---|---|---|---|
| 2 | 4 | 2 | yes |
| **3** | **5** | **5/2** | **NO (non-integer)** |
| 4 | 6 | 3 | yes (ΣY³=0, ΣY=0) |
| 6 | 8 | 4 | yes |
| 10 | 12 | 6 | yes (**hexagon → GS → dim G = 496**) |

**d = 3 is odd ⇒ (d+2)/2 = 5/2 is not an integer ⇒ there is no `tr F^{5/2}`, hence NO perturbative chiral
gauge anomaly at all.** The exact diagram that lets 10D Green-Schwarz *force* `SO(32)/E₈×E₈` (verified:
`SO(32)` dim = 496, `E₈×E₈` dim = 496, the only solutions of the GS gravitational-anomaly equation) **cannot
even be written down** on a 3D boundary. This is dispositive and was the prompt's flagged crux: confirmed by
explicit computation, not assumed.

What 3D *does* have is only a **fistful of mod-N bits**: parity (Z₂), Witten global (Z₂), Dai-Freed (Z₁₆),
and a gravitational-framing c-number. A finite-abelian congruence can impose a *parity/divisibility
condition on a count* — it can **never solve for a unique value** (a group, a generation number).

---

## SUB-1 — 3D parity anomalies on SM content (Redlich/Witten Z₂, U(1)_Y half-CS, gravitational)

All sympy-exact; SM = one generation, left-handed Weyl, `Q = T₃ + Y`. 4D sanity: `ΣY = 0`, `ΣY³ = 0`
(the SM exists). On the integer charge lattice `q = 6Y`:

- **(a) U(1)_Y parity anomaly** (induced half-level `½ Σ q²`). Per-multiplet `(6Y)²·mult`:
  `Q:6 + u^c:48 + d^c:12 + L:18 + e^c:36 = 120 / gen` (EVEN), `360` for 3 gens (EVEN). Half-level
  `½·120 = 60` = INTEGER ⇒ **no uncancellable half-CS.** And `Σ(6Y)²` even is *implied by* 4D
  anomaly-freedom via inflow (Witten 2015) — it transmits **no new boundary constraint.**
- **(b) SU(2)_L Witten global anomaly** (`π₄(SU(2)) = Z₂`, doublet count must be even): `3 (quark, one per
  color) + 1 (lepton) = 4 doublets/gen` = EVEN **already at N_gen = 1**; 12 for 3 gens (matches banked).
  Rescued by **color** (`N_c + 1 = 4`), *independent of N_gen.*
- **(c) SU(3)_c:** `π₄(SU(3)) = 0` ⇒ **no parity anomaly, silent.**
- **(d) Gravitational parity anomaly:** total 2-component fermions = **15/gen = ODD** (minimal SM, no ν_R);
  **16/gen EVEN** with ν_R (the SO(10) **16**-spinor).

**N_gen scan {1,2,3,4,5}: every N passes both Z₂ constraints** because each generation is even by itself
(4 doublets, `Σ(6Y)² = 120`). **The parity anomaly does NOT select N_gen = 3.** Vector-like content always
gives even `Σq²` (Dirac pairs ±q). **Forces NO SM feature.**

The lone non-trivial wrinkle is the **15/gen gravitational ODD** — credited honestly. But Witten (1988)
proved a *single* 3D Dirac fermion is a **consistent** theory with a half-integer grav-CS counterterm, so an
odd total is **not an inconsistency** — it is a consistent SPT label choice. Its only "output" (16/gen = add
ν_R = SO(10) **16**) **value-matches a gauge-side fact already known independently** (Baez-Schwahn / Furey),
hence **circular as a derivation.**

## SUB-2 — dS₄ MacDowell-Mansouri SO(4,1) bulk inflow → CFT₃ content?

A real inflow exists (the MM action is a Pontryagin/Euler 4-form ⇒ a boundary grav-CS 3-form by Stokes — not
a category error). But it cannot do GS-style forcing for three computed reasons:

1. **The gauge part vanishes on-shell.** `F_internal = R_ab − e_a∧e_b/ℓ² = 0` identically on the
   maximally-symmetric dS saddle (`R_ab = e_a∧e_b/ℓ²`). sympy-verified: `F_on_shell = 0`. Only a
   **gravitational framing** piece survives — **flavor-blind**, matched by a bulk grav-CS counterterm for
   *any* content.
2. **4D→3D descent yields ONE mod-ℤ number**, whereas 10D forcing needs the simultaneous Casimir equations
   of the even-dim 8-/12-form hexagon. Odd-3D has no perturbative chiral gauge anomaly to descend.
3. **The survivor is parity-type, capped at Z₂/Zₙ** the SM passes trivially (even 48-Weyl count, even
   12-doublet count) — N_gen = 3 parity-locked-out, consistent with the banked S⁴ 16-index null.

**Forces NO SM feature.** No-natural-content-forcing-inflow on the standard on-shell MM saddle.

## SUB-3 — Does ANY 3D anomaly constrain N_gen, or is 3 still free?

- **Z₁₆ Dai-Freed** (Garcia-Etxebarria–Montero 1808.00009; Wang-Wen-Witten JHEP07(2020)232): one generation
  = 16 Weyl (incl. ν_R) `= 0 mod 16`, so `16·N_gen ≡ 0 mod 16` for **every** N_gen {1,2,3,4,5,17,…}.
  Constrains the **presence of ν_R** (the `X = −2Y + 5(B−L)` mixed anomaly), **NOT the count.** (Without
  ν_R: `15·N_gen mod 16` = 15, 14, 13… ≠ 0 — wants the 16-completion, but once complete, any N_gen passes.)
- **Parity / Witten Z₂:** 4 doublets/gen even ⇒ satisfied for all N_gen (rescued by color, not generations).
- **Discrete flavor-Z₃** (`H⁴(BZ₃, U(1)) = Z₃`, Dijkgraaf-Witten): the only object that even *mentions* 3 —
  but the Z₃ is **defined** as permuting 3 generations, so it **inputs** N_gen = 3 and **cannot output it.
  Circular.** The framing chiral central charge is a content-free c-number matched by a counterterm.

**N_gen = 3 remains entirely free.** No 3D anomaly outputs the value 3.

## SUB-4 — Does the non-unitary CFT₃ (complex central charge) rescue a content-forcing anomaly?

dS₃ central charge is **imaginary**: `c_dS = 3iℓ/2G` (Brown-Henneaux `c = 3ℓ/2G` under `ℓ → iℓ`). The
**continuous** conformal/gravitational-CS anomaly carries this `c`, so in the cosmological `|Ψ|²` its
exponent **self-cancels** (`amp + amp* = 0`, sympy-verified) — the *one class that could force content* is
made **vacuous / ill-defined** by non-unitarity. The **discrete** Witten/Dai-Freed anomalies carry no factor
of `ℓ`, are untouched by `ℓ → iℓ`, and **survive** — but they are exactly the trivial Z₂/Z₁₆ the SM already
passes. **Both branches shut the door:** the lever is removed *or* what survives is capped-discrete.

## SUB-5 — Direct 10D-vs-3D comparison

10D forces the group because **D = 10 is even**: chiral hexagon anomaly is ℝ-valued and continuous in the
group label; GS factorization forces `dim G = 496` via three independent Casimirs. **D = 3 is odd:** the
gauge anomaly polynomial is a (d+2)-form nonzero only for even D (textbook AGW descent), so there is **no
continuum equation.** The 3D menu — parity-Witten-Redlich Z₂, framing c-number, Dai-Freed Z₁₆ mod-N — returns
a **discrete verdict on given content, never solves for the group.** Both real loopholes (inflow fixes a
level not a group; non-unitary CFT removes the lever) close. **Deep definitive null, prior LOW confirmed.**

---

## Anti-circularity ledger (the decisive gate)

| 3D anomaly | What it could constrain | SM status | Non-circular SM OUTPUT? |
|---|---|---|---|
| U(1)_Y parity (Z₂) | `Σ(6Y)²` even | 120/gen even, ALL N_gen | **NO** — implied by 4D inflow, not new |
| SU(2)_L Witten (Z₂) | doublet count even | 4/gen even, ALL N_gen | **NO** — even via color, blind to N_gen |
| SU(3)_c parity | — | `π₄=0`, silent | **NO** — no anomaly |
| Gravitational parity | total Weyl even | 15 odd / 16 even | **NO** — counterterm-absorbed; ν_R fix value-matches a known gauge fact |
| Dai-Freed Z₁₆ | 16-completion | `0 mod 16`, ALL N_gen | **NO** — constrains ν_R presence, not count |
| Flavor-Z₃ (H⁴) | the value 3 | defined by 3 gens | **NO** — circular (inputs 3) |
| MM SO(4,1) inflow | boundary grav-CS | gauge part = 0 on-shell | **NO** — flavor-blind framing only |
| Non-unitary `c_dS` rescue | continuous anomaly | self-cancels in `|Ψ|²` | **NO** — vacuous/ill-defined |

**Every row OUTPUTS nothing.** The SM satisfies every 3D Z₂/Z₁₆ bit purely by being a consistent 4D chiral
theory. Consistent with the banked gravity/gauge **disjointness** (Schur, Coleman-Mandula, Baez-Schwahn
J₃(𝕆)/F₄ gauge-only) and the prior `INVERTED_BH_TO_PARTICLE_PHYSICS_2026-06` Angle-1a structural-absence.

---

## For Carl — straight talk

**Did the deepest dS/CFT swing connect? No — and it's not because we didn't push hard enough. It's because
3D is structurally the wrong dimension for content-forcing.** This is the single deepest reason the
inverted-BH gravity result does not reach into the Standard Model: the Green-Schwarz "consistency forces the
gauge group" machine is a property of **even** dimensions (the hexagon is a 12-form; it needs `tr F⁶`). The
dS/CFT boundary is **odd** (3D), and odd dimensions have **no perturbative chiral gauge anomaly at all** —
only a handful of discrete Z₂/Z₁₆ on-off switches, and the SM flips all of them correctly for *any* number of
generations. There is no equation here that could spit out `SU(3)×SU(2)×U(1)`, or `3`, or a hypercharge
relation.

**The ONE thing that would have to be true for it to work — and whether it is:** a content-forcing anomaly
needs an **even-dimensional** boundary with a **continuous (ℝ-valued)** chiral gauge anomaly polynomial.
The dS/CFT boundary of dS₄ is fixed at **3D** by the bulk being 4D (boundary dim = bulk − 1) — **it is not
free, it is not.** The only escape routes — (i) the SO(4,1) bulk inflow supplying a continuous boundary
constraint, (ii) the non-unitary CFT's complex `c` reviving a forcing anomaly — were both computed and both
close: inflow's gauge part **vanishes on the dS saddle** (`R_ab = e_a∧e_b/ℓ²`), and the complex `c` makes the
*continuous* anomaly **self-cancel in `|Ψ|²`**, leaving only the trivial discrete sector. There is no fourth
lever.

So the honest bottom line: **the inverted-BH structure closes the gravity side beautifully
(a₀ ~ √Λ, one-parameter EFT) but transmits no kernel to the SM through the anomaly channel — the door is the
wrong dimension.** I credited the one genuinely nontrivial wrinkle loudly (the 15/gen gravitational ODD, the
SO(10)-**16** preference) before showing it is counterterm-absorbed and circular. No manufactured forcing, no
manufactured deficit. **SM gauge group, N_gen = 3, and fermion content remain free.** This is the deep,
definitive answer — we pushed the best overlooked angle (the explicit 3D parity/Witten/Z₁₆/inflow/non-unitary
enumeration) all the way to the bottom, and 3D is structurally incapable of forcing the SM.

---

*Verification (clean-room, sympy-exact): `/tmp/dscft_independent_verify.py`, `/tmp/witten_and_inflow_verify.py`,
`/tmp/nonunitary_verify.py`, plus banked `/tmp/parity_anomaly_sub1*.py`. Primary refs: Strominger dS/CFT
hep-th/0106113; Witten "Fermion Path Integrals and Topological Phases" 1508.04715 (parity anomaly, 4D inflow);
Redlich PRL 1984 / Witten 1988 (3D parity anomaly); Garcia-Etxebarria–Montero 1808.00009 + Wang-Wen-Witten
JHEP07(2020)232 (Z₁₆ Dai-Freed); Alvarez-Gaumé–Witten 1984 (descent / (d+2)-form); Baez-Schwahn (J₃(𝕆)/F₄
gauge home). Banked: INVERTED_BH_TO_PARTICLE_PHYSICS_2026-06.md (Angle 1a), CKN_LAMBDA_VALUE_VERDICT,
particle_numerology_standing, project_covariant_mi_completion. LOCAL ONLY — not git-pushed.*
