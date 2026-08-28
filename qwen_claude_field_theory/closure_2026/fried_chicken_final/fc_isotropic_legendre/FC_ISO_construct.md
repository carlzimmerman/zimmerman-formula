# FC-ISOTROPIC-LEGENDRE — CONSTRUCTION ATTEMPT

**Task.** Try HARD to **construct** an *isotropic* second-class Legendre completion of the
MOND law D_i[μ(y)D^i q]=4πGρ whose on-shell traceless metric stress **vanishes**
(Σ_P=0 ⇒ Φ=Ψ, γ_PPN=1, FRIED CHICKEN), while (a) reproducing the MOND/AQUAL Gauss law,
(b) keeping N_grav=2 (no new propagating DOF), (c) c_T=1. Report
ISOTROPIC-COMPLETION-CONSTRUCTED **only** with a full certificate; else PARTIAL/INCONCLUSIVE.

**Certificate:** `fc_iso_construct.py` → `fc_iso_construct.out`, **28/28 boolean checks PASS,
exit 0.** Every load-bearing line prints `simplify(...)==0` or a residual. A "this Σ_P is
nonzero" check is itself a PASS — we certify the *computation*, and verify a WIN (Σ_P=0)
exactly as hard as a FAIL (the Newtonian/solar limit is checked to switch the slip off).

Frozen kernel (not tweaked — the obstruction is kernel-general, any μ′≠0):
μ₁₀(y)=y/(1+y¹⁰)^(1/10), μ₁₀′=(1+y¹⁰)^(−11/10)>0.

---

## Result (one line)

**No isotropic completion constructed.** All three named mechanisms fail, each with a
*computed* Σ_P and an identified cost that breaks (a), (b), or (c). Within the **local,
action-based (Hilbert-stress), ≤2-derivative** second-class class the obstruction is
**forced**; the fully-general no-go (arbitrary higher-derivative / arbitrary auxiliary
content, closed by a Dirac count) is the residual open item = the next task. **Honest
verdict: PARTIAL** (construction fails; obstruction forced in-class; full no-go pending;
the non-local elliptic gate E1 stays genuinely open).

---

## The rigidity that defeats the construction (DERIVATION + COMPUTATION)

The traceless metric stress that sources Φ−Ψ is Σ_P = −2[∂L/∂g^{ij}]^TF (the √g measure is
pure trace, check 01). For any **local scalar** MOND sector this is *rigidly the same
functional as the force*:

| construction | force operator | traceless Hilbert stress Σ_P | Σ_P = 0 ⟺ | check |
|---|---|---|---|---|
| AQUAL single scalar | ∇·[2F_X∇q] | **2 F_X X = μ_eff X** | F_X=0 (no force) | 02,05,06 |
| naive-Legendre (direct) | ∇·[μ∇q] | **a₀ n y (2μ + yμ′)** | μ=0 ∧ μ′=0 (no force) | 13,14 |
| QUMOND bipotential (2 fields) | ∇²Φ=∇·[ν∇Ψ] | **3 ν w²** (on-shell) | ν=0 (no force) | 18,19 |

Two honest points, verified:

- The setup's **Σ_P = yμ′** is the traceless part of the *constitutive Hessian*
  A^{ij}=μδ+yμ′ uu — the **multiplier-chain** object governing the MOND-as-lapse slip
  (μ+yμ′)/μ (committed `fc4ac_slip.py`). The **actual gravitating Hilbert stress**, computed
  directly by perturbing g^{ij}=δ+h (check 13), is **a₀ n y (2μ + yμ′)** — dominated by the
  **force modulus 2μ** (the AQUAL piece), with yμ′ a subleading kernel-shape correction. So
  the Hilbert coupling is if anything *worse* than yμ′; Σ_P=0 needs the force switched off
  entirely. We report this even though it is stronger than the inherited claim — honesty over
  tidiness.
- **Solar-system safety is verified as hard as the failure** (checks 10, 15): the excess
  yμ′/μ → 0 as y→∞. The slip is a **deep-MOND (galactic-lensing)** effect, not a solar one.
  The a₀-line, RAR, BTFR, Cassini bounds etc. are untouched — this is purely the γ_PPN axis of
  the *relativistic lensing completion*.

**Reduction (check 12).** A local, *algebraically*-reducible auxiliary (e.g. a flux P^i with
an algebraic EOM) integrates out to L_eff = F(X): it opens **no new traceless-stress
channel**. So enlarging the local algebraic field content cannot help — you always land back
on a single-/multi-scalar F(X) whose stress is tied to the force.

---

## The three mechanisms, each computed to fail

**(i) Compensating auxiliary tensor/vector — FAILS, breaks (b).**
- (i-c) *sharpest test — two local fields (QUMOND bipotential).* Its Hilbert traceless stress
  is w(2p+Q′w); on-shell p=νw it is **3νw² > 0** (check 19). The two fields **reinforce** —
  cancellation 2p+Q′w=0 needs Φ′<0 (repulsive), excluded for an attractive MOND force.
- (i-a) *compensating scalar.* To supply −Σ_P<0 it needs G_X = −(yμ′)/(2X_p) < 0 (check 21) —
  a **wrong-sign gradient term = ghost / gradient-instability**, a new pathological propagating
  DOF, not a healthy second-class removal (check 22).
- (i-b) *compensating vector.* Algebraic (mass-only) vector reduces to F(X) (no cancellation,
  Part 3); a vector that carries an **independent** stress needs a kinetic term ⇒ it
  **propagates** (transverse Hessian ~k²≠0, check 23) ⇒ DOF>2. Dichotomy, check 24.

**(ii) Disformal / conformal reshuffle into the trace — FAILS, breaks (c).**
- A **pure conformal** factor shifts Φ and Ψ *equally* ⇒ Φ_phys−Ψ_phys = Φ_g−Ψ_g unchanged
  (check 25): it cannot move the slip into the trace.
- The **disformal** D that *does* move it splits the photon/graviton cone:
  c_γ²/c_GW² = (C−D)/C = 1−D/C (committed `gate2_cone_gw170817_2026.py`, check 26); a
  lensing-sized D/C ~ O(μ−1) ~ O(1) violates GW170817 (|D/C| ≲ 2×10⁻¹⁵) by ~15 orders
  (check 27).

**(iii) Trace-only (det g) coupling — FAILS, breaks (a).**
If the flux couples to g^{ij} only through det g, then ∂L/∂g^{ij}∝g_ij is pure trace and
Σ_P=0 automatically — but then ∂L/∂q is algebraic (F_q=0) and there is **no** Gauss law
D_i[μD^i q]=4πGρ. The MOND force *requires* g^{ij} to raise the flux index; any such
contraction has a nonzero traceless variation (check 16). det g cannot source a force
(check 17).

---

## The two genuine evasions — and why each leaves the class (the contrast)

Exactly two structures reach Φ=Ψ with the same yμ′ Hessian, each by adding what a **local
2-DOF** theory lacks:

- **E1 — non-local elliptic carrier (QUMOND-as-density).** Treat ρ_ph=(1/4πG)∇·[(ν−1)∇Ψ] as
  an **isotropic phantom density** sourcing Φ and Ψ equally ⇒ Φ=Ψ. *Crucial honesty:* this
  sources gravity with a density in the 00-equation, **not** with the sector's own Hilbert
  stress (which is anisotropic, ~2μ, and would reinstate the slip — cf. the 3νw² bipotential
  stress). Eliminating q is non-local (∇⁻²). This is precisely the committed **open gate**
  (`theory_2026/york` RESULT §4c): 2+0 single-metric, γ_PPN=1, but causal acceptability
  **UNSETTLED**. It breaks locality/action-stress, not (a)/(b)/(c) — and it stays open.
- **E2 — propagating vector (AeST / TeVeS).** The aether A_μ carries the scalar's anisotropic
  gradient stress; its disformal is luminal (Skordis–Zlosnik) ⇒ c_T=1 **and** γ_PPN=1
  (committed `FC_AEST/fc_lensing_rar_mu10`, M24 KiDS χ²/dof=0.64). But A_μ **propagates**:
  6(+1) DOF, not 2. It breaks (b).

Both give Φ=Ψ *because* they add non-locality or a propagating field. A pure local
action-based 2-DOF constraint theory has neither — that is the mechanism of the obstruction,
isolated for the unified-no-go next task.

---

## Honest scope / what is NOT claimed

- **Not** an all-completions theorem. Forced is proven for the local, action-based
  (Hilbert-stress), ≤2-derivative, algebraically-reducible class + the three named mechanisms.
  Arbitrary higher-derivative and arbitrary auxiliary field content (closed by a full Dirac
  DOF count) is the next task.
- **Not** a closure of the elliptic gate E1 — that non-local route is genuinely open (its
  causal status is the committed unsettled gate).
- The obstruction is **kernel-general** (any μ′≠0, and even μ≠const for the Hilbert stress);
  it is not an artifact of μ₁₀ and cannot be tuned away by changing the kernel.
- a₀²=κ²c²Gρ_Λ, κ=½, Z~21 remain phenomenological inputs; nothing here touches them.

## Files (output dir; not committed)

- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/fc_iso_construct.py`
- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/fc_iso_construct.out`
- `/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_isotropic_legendre/FC_ISO_construct.md`
