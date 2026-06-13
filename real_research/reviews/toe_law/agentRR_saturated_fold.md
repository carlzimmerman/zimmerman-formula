# agentRR — BANKING MEMO: does a SATURATED-GAIN ('maser-like') response deliver the bounded, stable, edge-pinned roton fold? FORCED or MODEL-DEPENDENT? (2026-06-13)

## OVERALL VERDICT — FOLD-DELIVERED-MODEL-DEPENDENT

**The saturated-gain medium CAN build the bounded, stable, edge-pinned roton fold, but it is NOT
forced by the dS pump — it rests on N = 4 free knobs.** Both routes, counted only at hostile-VERIFIED
grade, return FOLD-DELIVERED-MODEL-DEPENDENT (2/2 CONFIRMED). The fold is a *consistent, buildable,
X2-consistent construction*, not a derivation. This is the honest likely outcome the brief named.

**HEADLINE (forced-vs-model-dependent, the central question):**
- **FORCED by the dS pump / T_dS=H/2π / X2 (all SIGN or EXISTENCE statements, zero continuous value
  asserted):** (1) the medium is ACTIVE [X2 passivity theorem]; (2) the bend σ4<0 [banked 851e7649];
  (3) **saturation EXISTS and CLAMPS the amplitude** — gain clamps to loss, g_eff(I*)=κ exactly, an
  IVT structural identity for ANY monotone-decreasing g(I). This is the **one genuinely new forced
  result** this round banks: QQ's LTI *amplitude* runaway is TAMED. (4) the k* SCALE
  k*~(c_χ/√a₀)H, built from pre-banked {H, c_χ, a₀}, zero new knobs — a clean scale-grade prediction.
- **FREE (N = 4 delivery knobs, none pinned by H or T_dS — the pump fixes dimensionful SCALES ~H, the
  fold needs dimensionless RATIOS):**
  - **(a) narrow gain-peak ratio** x = k0²/Γ ∈ [0.10, 0.30] (the smooth GH continuum is broad → σ6<0);
  - **(b) fold-strength magnitude** y = A/(c_χ²Γ) ∈ [1.00, 1.30] (pump fixes the SIGN, not the
    threshold-crossing magnitude);
  - **(c) edge-coincidence** k0 = b→c_χ sonic edge (= QQ's codim-1 edge-pinning);
  - **(d) a k-RESOLVED / non-Markovian clamp** — plain scalar laser saturation provably leaves the
    off-center fold-band retarded pole in the UHP at fold strength.

**FREE-PARAMETER COUNT = 4 ≠ 0.** No knob was smuggled in as forced; the FORCED subset is exactly
{active-sign, σ4<0-sign, clamp-existence, k*-scale}, all signs/existence/scale.

**ONE-SENTENCE LINK-5 UPDATE.** The saturated-gain hook **retires QQ's amplitude-runaway objection**
(gain clamping bounds the amplitude — FORCED), but it does **not** deliver the controlled fold on its
own: that still needs the narrow σ6∈(σ6*, 4σ6*/3) window, the fold-strength magnitude, the sonic-edge
coincidence, AND a k-resolved/non-Markovian (not scalar) clamp — so Link 5's controlled roton fold
stays **SELF-CONSISTENT-BUT-UNDELIVERED**, now with the amplitude objection gone and the entire
residual burden concentrated on a **peaked dS QNM resonance plus a k-structured saturation**.

---

## ROUTE 1 — SATURATED-GAIN / laser-threshold construction → FOLD-DELIVERED-MODEL-DEPENDENT (CONFIRMED)

`agentRR_routeSaturated.md`; hostile referee `agentRR_verify_saturated-gain.md`; computations
`agentRR_part1..part11` + `agentRR_indep_verify{,2}.py`, all in this dir.

**Construction.** Modeled X2's active dS response as a saturated gain Σ_gain = g0/(1+|χ|²/I_sat)
(laser-saturation form); the dispersive (Re) self-energy of a negative-residue peaked gain line at
center k0, width Γ supplies the IR roton tower ω²(k) = c_eff²k² + σ4 k⁴ + σ6 k⁶.

**What was computed (verified-reproduced):**
- **D1 (tame the runaway) — PASS, two ways.** Rate eq dI/dt=[g0/(1+I/I_sat)−κ]I has a STABLE fixed
  point I*=I_sat(g0/κ−1) with the gain CLAMPED: g_eff(I*)=κ **exactly**, f'(I*)=κ(κ−g0)/g0<0 —
  symbolic AND direct nonlinear integration (|χ|→√(I_sat(g0/κ−1)) to <1%). QQ's amplitude runaway is
  tamed.
- **D2/D3 (dispersion) — exact IR coefficients:** σ4 = AΓk0²(k0⁴−3Γ²)/(Γ²+k0⁴)³ ⟹ **σ4<0 ⟺ k0⁴<3Γ²**;
  σ6 = AΓ(Γ⁴−6Γ²k0⁴+k0⁸)/(Γ²+k0⁴)⁴. The peaked active line CAN supply σ4<0.
- **The load-bearing geometry (model-independent):** σ6 ≥ σ6* = σ4²/(4c²) is the **NO-GHOST**
  threshold, NOT fold-existence. A visible bounded fold needs v_g²_min = c² − σ4²/(3σ6) < 0, i.e.
  **σ6/σ6* ∈ (1, 4/3)** — a 33% window (σ6_fold/σ6* = 4/3 EXACTLY, sympy + numeric flips at 1.000 and
  1.333). Only ~5% of the natural (x,y) area gives a true full-branch bounded fold (x∈[0.10,0.30],
  y∈[1.00,1.30], ~1.3 dex tuning); deeper folds force c_eff²→0 (sonic-edge collapse, corr +0.43).
- **Stability:** at small active coupling the pole is LHP (Im=−0.025, QQ's active≠anti-damped window);
  at **FOLD strength** (y~1.0–1.3) the retarded pole goes **UHP** (Im≈+0.6..+0.9) for ANY khronon loss
  κ — referee extended to **κ=5** and it still fails. The scalar intensity clamp pins only the
  gain-center band marginal (a radiating limit cycle), NOT the off-center fold modes ⟹ exposes the
  4th condition (k-resolved clamp).

**edge-pins:** TUNED, not pinned. k* is set by the gain center k0; its ORDER is bath-set
(k*~(c_χ/√a₀)H) but the COINCIDENCE k0=b→c_χ is reached only by driving c_eff²→0 (the sonic-edge
collapse = QQ's codim-1 edge-pinning). I_sat pins the AMPLITUDE I*, not k*.

**Hostile verification (CONFIRMED).** recompute_agrees = YES (σ4/σ6 via independent Maclaurin
derivatives, the 4/3 window exact, clamp identity exact, UHP-at-fold-strength reproduced and extended
to κ=5). The FORCED subset is exactly {active-sign, σ4<0-sign, clamp-existence} — all sign/existence,
**zero continuous value asserted**; no gain magnitude, saturation scale, gain-center, or width was
relabelled forced. Hostile parameter count returns the SAME 4 free delivery knobs.

**Verified caveat (label honesty):** the route's verdict word "DELIVERED" overstates the memo BODY,
which honestly concludes the fold is **"SELF-CONSISTENT-BUT-UNDELIVERED"**; what is *delivered* is the
amplitude stabilizer, not the fold itself. Banked at the body's reading.

---

## ROUTE 2 — EDGE-COINCIDENCE FROM THE PUMP SCALE → FOLD-DELIVERED-MODEL-DEPENDENT (CONFIRMED)

`agentRR_routeEdge.md`; hostile referee `agentRR_verify_edge-from-pump.md`.

**Question.** Does the dS pump introduce exactly ONE scale such that k*=edge is one equation in ZERO
free parameters (FORCED/predicted), or does pinning k* require a separate tuned ratio independent of
the pump (ACCOMMODATED)?

**What was computed (verified-reproduced):**
- **Edge-coincidence = ONE equation.** The inflection cubic 6σ6²u³ + 9σ4σ6 u² + (10c_χ²σ6+2σ4²)u +
  3c_χ²σ4 = 0 (u=k²) factorizes at the soft sonic edge to a **triple root** at u*=−2c_χ²/σ4 with
  **σ6* = σ4²/(4c_χ²)** (sympy; reproduces QQ's banked threshold exactly). So **k*=edge ⟺ σ6=σ6*.**
- **The central hostile check — G does NOT cancel.** Writing σ4=−G j2 c_χ², σ6=+G j3 c_χ² for a gain
  line of amplitude G, the edge ratio is **σ6/σ6* = 4 j3/(G j2²) ∝ 1/G** (σ6*∝G² but σ6∝G — hostility
  caught and corrected a first-pass "G cancels" error). So **EDGE EQ: G = 4 j3(s_g/s0,Γ/s0)/j2²** —
  ONE equation on THREE line-shape knobs {G, center/s0, width/s0} = a **codim-1 surface, ≥1 free knob.**
- **Scale audit.** The pump has exactly ONE intrinsic scale s0=H² (T_dS=H/2π). It FORCES the k*
  MAGNITUDE k*~(c_χ/√a₀)H from pre-banked {H, c_χ, a₀} — **zero new knobs** (c_χ²=O(γ/α) is an
  independent PPN/Minkowski-form khronon datum, NOT generated by H; referee CHECK 5 confirms no
  c_χ↔H scale collapse against agentEE STEP 1 / 1206.1083). It does NOT fix the dimensionless
  line-shape ratios center/s0, width/s0, nor tie G to 4 j3/j2².
- **Steelman of the maser hook — saturation pins to gain=loss, NOT the edge.** Saturation self-pins
  G to the lasing threshold (gain=loss, g_eff(I*)=κ, f'(I*)<0 — genuinely stable, the real Route-1
  escape), but (edge-G)/(saturation-G) **roams 10×–266×** (referee: 6.85–27× on a modest grid) and
  never identically equals 1. No symmetry ties stability to the soft edge.

**edge-pins:** The saturation/pump scale does NOT pin k* at b→c_χ — it is TUNED. The pump pins only
the k* MAGNITUDE (forced, zero knobs); the COINCIDENCE is one equation in ≥1 free line-shape ratio.

**Hostile verification (CONFIRMED).** Every load-bearing step reproduces independently: inflection
cubic + triple-root σ6*=σ4²/(4c²) (CHECK 1), the G-does-NOT-cancel 1/G edge scaling (CHECK 2, central),
the shape-roaming free edge surface (CHECK 3), saturation pinning to gain=loss not the edge (CHECK 4),
and the absence of any c_χ↔H scale collapse (CHECK 5). The route claims FORCED only for the k* SCALE
(clean zero-knob prediction) and honestly tags the k*=edge COINCIDENCE as tuned (codim-1, ≥1 free
line-shape knob). No surviving knob was relabelled forced; if anything conservative.

---

## SYNTHESIS — the two routes agree, from opposite sides

Both routes independently land **FORCED-IN-SCALE-AND-SIGN, TUNED-IN-COINCIDENCE-AND-MAGNITUDE.**
Route 1 (amplitude/stability side): saturation forces the amplitude clamp (retires the runaway) but
leaves 4 free knobs for the fold. Route 2 (scale-counting side): the pump forces the k* SCALE but the
k*=edge coincidence is one equation on free line-shape ratios. They corroborate: **the maser hook buys
exactly two things — bounded amplitude (Route 1) and a peaked, stable operating point (Route 2's
lasing threshold) — and neither is the fold.** Saturation pins G for STABILITY; the edge pins G for
COINCIDENCE; these are DIFFERENT conditions on the same knob and roam apart 10–266×.

**The honest read:** a saturated-gain ('maser-like') response **CAN deliver** a bounded, stable,
edge-pinned fold as a consistent X2-compatible construction — but with **N=4 free knobs** the dS pump
does not fix. The fold is *buildable*, not *forced*; this is a model-dependent existence, not a
derivation.

## NEXT CALC (both routes converge on the same test)

Compute the actual dS QUASINORMAL-MODE horizon spectral function (its center s_g and width Γ in units
of H², from the Gibbons-Hawking heat kernel) as a NARROW, k-RESOLVED active line — and test whether a
SYMMETRY/identity of the dS QNM spectrum forces {s_g/s0, Γ/s0} onto the edge surface 4 j3/j2² = G_sat,
turning the codim-1 accommodation into a prediction. PASS iff a peaked QNM (i) lands the narrow window
1<σ6/σ6*<4/3 on the stable branch with k0 at b→c_χ, AND (ii) its non-Markovian profile keeps the
off-center fold-band poles in the closed LHP (which scalar saturation cannot). FAIL/ACCOMMODATED if the
QNM center is a free spectral datum that must be hand-tuned to the sonic edge, or if it overshoots to a
monotone branch (σ6/σ6*>4/3) or undershoots to a ghost. Then derive ρ(b)/q=1/4 with γ_req downstream
(quarantined).

## QUARANTINE
Held throughout both routes and both verifications. Only signs (σ4<0, σ6 vs σ6*, σ6 vs σ6_fold, Im
pole vs 0, f'(I*) vs 0), the 4/3 window ratio, the 1/G edge scaling, clamp fixed-point structure,
scales, and pole locations were computed. **q=1/4, ζ̃, (16π/3)^{1/4} never asserted.**
