# The in-in worldline MI action → AeST: the join, constructed and adjudicated

**C. Zimmerman framework, 2026-06-15.** The framework's single most important first-principles
construction: build the time-nonlocal in-in (Galley / Schwinger-Keldysh / Feynman-Vernon) worldline
action for de Sitter-Unruh **modified inertia**, and test the conjecture that it coarse-grains to
**AeST** — joining the two pillars into one theory.

**VERDICT: PARTIAL, leaning NOT-JOINED on the decisive (Cassini/mechanism) axis.** Real structural
overlap (shared IR law + field content + EFT-slot pattern); a hard gap (the MI gate is not a droppable
truncation; the aether kinetic sector is unproduced). AeST is a **sibling EFT** of the worldline MI,
**not its coarse-grained truncation**. Both ways: no manufactured join, no manufactured failure.

Files: `build_part1_worldline_to_field.py` (the in-in MI action), `build_part2_aest_match.py`
(term-by-term vs AeST eq 5), `build_part3_truncation_cassini.py` (active→passive truncation + Cassini),
`build_part4_adversarial.py` (the gate, the load-bearing both-ways stress test). Primaries verified
firsthand from the PDFs (text cached: `GALLEY.txt`, `AEST.txt`).

## Primaries (verified firsthand, eq numbers cited)
- **Galley 1210.2745** (PRL 110 174301): doubled action **eq (5)** `S=∫dt[L(q1)−L(q2)+K(qa,q̇a)]`;
  physical limit **eq (11)** `δS/δq₋|p.l.=0`, only terms linear in q₋ give forces; energy
  non-conservation **eq (19)** set by K; the drag example **eq (20)** `Λ=m ẋ₋·ẋ₊ − α x₋·ẋ₊|ẋ₊|^{n−1}`.
- **AeST / Skordis-Złośnik 2007.00082** (PRL 127 161302): the action **eq (5)**
  `S=∫√−g/16πG̃ [R − (K_B/2)F² + 2(2−K_B)Jᵘ∇ᵤφ − (2−K_B)Y − F(Y,Q) − λ(A²+1)] + S_m`,
  with `F_{μν}=2∇_[μA_ν]`, `Jᵘ=Aᵃ∇ₐAᵘ`, `Q=Aᵘ∇ᵤφ`, `Y=qᵘᵛ∇ᵤφ∇ᵛφ`, `qᵘᵛ=gᵘᵛ+AᵘAᵛ`; deep-MOND
  `J→(2λ_s/3(1+λ_s)a0)Y^{3/2}` (a0 enters here); weak-field reduction **eq (6)** → AQUAL + µ²Φ² mass.

## The dictionary tested (the charge), term by term

| AeST eq (5) term | from MI worldline coarse-graining? | status |
|---|---|---|
| field content: A^μ (unit-timelike), φ (shift-sym) | coarse-grained congruence gives u^μ (u²=−1) + collective φ, right symmetries | **MATCH** (B.2) |
| `−F(Y,Q) → Y^{3/2}` (deep-MOND) | deep-MOND MI law = AQUAL `|∇φ|³=Y^{3/2}`, SAME 1/a0 (sympy EL-flux exact) | **MATCH** (B.1) |
| `−λ(A²+1)` (unit constraint) | u^μ is a 4-velocity, automatic | MATCH |
| `−(2−K_B)Y` | part of scalar self-action; full F(Y,Q) free both sides | OK (free) |
| `2(2−K_B)Jᵘ∇ᵤφ` (aether-accel · ∇φ mixing) | plausible form (congruence accel · MI response); coeff tied to K_B | PARTIAL |
| `−(K_B/2)F²` (aether KINETIC) | NOT produced — MI uses u^μ as a background clock, not a propagating field | **HARD GAP** |
| `R + Λ` (host gravity) | NOT produced — supplied separately | supplied |

## The four verified results

**B.1 — the Y^{3/2} match (sympy, exact).** The deep-MOND MI law `m·μ_fw(a/a0)·a=F` with `μ_fw→a/a0`
coarse-grains to the AQUAL functional whose Lagrangian `L=−(1/3)(1/a0)|∇φ|³` has EL flux exactly the
MOND flux `−(|∇φ|/a0)∇φ` (sympy: difference = 0). `|∇φ|³ = (|∇φ|²)^{3/2} = Y^{3/2}`. AeST's prefactor
`2λ_s/3(1+λ_s) → 2/3` (screening limit). The **power Y^{3/2}** and the **1/a0 scaling** are
convention-independent and match. *Honest caveat:* this is the shared deep-MOND attractor (both reduce
to AQUAL/BM84); it pins the IR fixed point, not the UV completion.

**B.2 — field content (match).** Coarse-graining a worldline congruence produces a unit-timelike
u^μ (= AeST's aether A^μ — physically the dS-bath preferred frame AeST introduces phenomenologically)
and a shift-symmetric collective scalar φ (the MI force depends only on ∇φ, never φ — AeST is shift-sym
too). Both fields, both symmetries: produced, not assumed.

**C.1 / C.2 — the active→passive truncation (constructed; recomputed).** The memory kernel's gradient
expansion `γ̂(ω)=γ₀+γ₁(iω)+γ₂(iω)²+…` splits into a **reactive** (even, time-symmetric) part
`γ₀+γ₂(iω)²` — derivable from a **local passive** action — and a **dissipative/active** (odd) part
`γ₁(iω)` plus the genuine memory tail, which the truncation **drops**. So the structural pattern the
conjecture predicts (passive+local = leading truncation; active+nonlocal = the dropped remainder) **is
realized at the kernel level** — CREDIT. **But** (C.2, recomputed Ohmic/sub-Ohmic/Debye, all J≥0):
every passive reactive truncation gives `m_eff(0) > m_eff(∞)` = **ANTI-MOND**. The truncation that makes
the kernel passive+local does **not** become AeST's MOND — it becomes anti-MOND. AeST's MOND comes from
a **gravity-side** field self-action the inertia coarse-graining never produces.

**Part 4 — the gate, the decisive both-ways result.** Where does the `|∇φ|³` sit?
- **Worldline MI (pillar 1):** in the matter worldline action, **GATED by μ_fw(a/a0)** — present only
  where a ≲ a0, switched OFF where a ≫ a0. Verified: at Saturn a/a0 = 6.9×10⁵, `1−μ_fw = 7.2×10⁻⁷`
  (modified inertia OFF by ~6 orders in the inner solar system). **→ Cassini evaded.**
- **AeST (pillar 2):** in the field action, **UNGATED** — the gravitating scalar is present everywhere,
  with Mpc-scale screening that does not reach the solar system. **→ Cassini failed** (banked
  Q₂≈3.2×10⁻²⁶ s⁻² vs ~5×10⁻²⁷ ceiling).

The **gate μ_fw is the defining content of modified inertia**, and it is **irreducibly absent from
AeST**. Dropping it is not a higher-gradient/non-equilibrium truncation — it changes the theory's class
(MI → MG). **Therefore the Cassini split is NOT "the truncation dropping the evasion"; it is two
different mechanisms (gated MI vs ungated MG) sharing one IR law.**

## What the join forces (nothing new)
κ=½ free (the worldline kernel normalization is a free response strength; every gravitational ½ is
spent). K_B unforced (it is the unproduced aether-kinetic gap). F(Y,Q) free on both sides except the
deep-MOND Y^{3/2}. a0 = c²√(Λ/32π) is **transmitted** into the Y^{3/2} slot, not newly forced (it was
already the kernel's scale). Consistent with the banked standing — the join adds no forcing.

## Honest status (both ways)
- **JOINED** (proven AeST = the EFT, same mechanism) — **NO.** The truncation gives anti-MOND passive
  inertia, not AeST's gravity-side MOND; the aether kinetic sector is unproduced; the MI gate (the
  defining feature) is absent from AeST.
- **PARTIAL** (real structural match + a gap) — **YES, this is the verdict.** Shared deep-MOND IR law
  (Y^{3/2}, 1/a0, exact flux), shared field content (unit-timelike vector + shift-sym scalar with right
  symmetries), and the kernel's reactive part genuinely is the local+passive leading slot. The two
  pillars are **closely related sibling EFTs** sharing IR law + field content.
- **The Cassini split is not resolved as a truncation artifact.** It is two mechanisms (modified inertia,
  μ_fw-gated, Cassini-evading; modified gravity, ungated, Cassini-failing) sharing the deep-MOND
  attractor. The worldline MI evades Cassini (gate, ~6 orders, verified); AeST fails it (no gate);
  neither is the truncation of the other.

This sharpens — does not close — the capstone two-pillar-join gap. The covariant MI theory is **not**
constructed as "AeST + its in-in UV completion"; the in-in worldline MI is a sibling of AeST with the
same IR law and field content but a genuinely different (gated-inertia) mechanism, and the obstruction
to fusing them is exactly the gate μ_fw + the unproduced aether kinetic term — the modified-inertia
content AeST structurally lacks.
