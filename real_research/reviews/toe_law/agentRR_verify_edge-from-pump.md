# agentRR VERIFY — hostile referee of ROUTE 2 (edge-coincidence from the pump scale). Is k*=edge FORCED or TUNED? (2026-06-13)

**Claim under review** (`agentRR_routeEdge.md`, verdict FOLD-DELIVERED-MODEL-DEPENDENT):
the dS pump introduces exactly ONE scale (H), which FORCES the k* MAGNITUDE
k*~(c_χ/√a₀)H from pre-banked constants (zero new knobs), but the edge-COINCIDENCE
k*=sonic-edge is the single equation σ6=σ6* ⟺ G=4 j3/j2², living on free saturated-gain
line-shape knobs {G, center/s0, width/s0} = a codim-1 surface ⇒ TUNED, not predicted.

**Central mission:** separate FORCED from MODEL-DEPENDENT. Re-derive the load-bearing
step; count the free parameters myself; check the saturated response is genuinely stable;
regrade. Default posture: 'forced' overclaimed until the parameter count is zero.
Coefficient quarantine held (q=1/4, ζ̃, (16π/3)^{1/4} never asserted — only signs,
ratios, scales, counts).

---

## CHECK 1 — the inflection cubic + triple-root factorization (independent sympy)

Built ω(k)=√(c_χ²k²+σ4 k⁴+σ6 k⁶) from scratch and took d²ω/dk² (NOT copied from the
memo). The vanishing condition is `k·[6σ6²k⁶ + 9σ4σ6 k⁴ + (10c_χ²σ6+2σ4²)k² + 3c_χ²σ4]=0`,
i.e. with u=k²:
> 6σ6²u³ + 9σ4σ6 u² + (10c_χ²σ6 + 2σ4²)u + 3c_χ²σ4 = 0  — **matches memo STEP 1 exactly.**

Substituting σ6=σ4²/(4c_χ²) the cubic factorizes (sympy) to
> **3σ4(2c_χ²+σ4 u)³/(8c_χ⁴)** — a clean TRIPLE root at u*=−2c_χ²/σ4,

and ω²(u*)|_{σ6*} = 0 exactly (the soft sonic edge). **CHECK 1 PASS** — σ6*=σ4²/(4c_χ²),
u*=−2c_χ²/σ4 reproduced independently; QQ's "1/16, u*=4" is the same identity in QQ's
(c_χ,σ4) normalization. The edge-coincidence really is the single equation σ6=σ6*.

## CHECK 2 (CENTRAL) — does the gain amplitude G cancel in σ6/σ6*?

The hostile crux: if G cancels, the edge would be shape-only (no amplitude knob); if it
does NOT, the edge is a genuine equation on {G, shape}. With the memo's banked mapping
σ4=−G j2 c_χ², σ6=+G j3 c_χ²:
- σ6* = σ4²/(4c_χ²) = **G²j2²c_χ²/4** (scales as G²);  σ6 = **G j3 c_χ²** (scales as G¹).
- σ6/σ6* = **4 j3/(G j2²) ∝ 1/G** (sympy, exact). Edge ⟺ **G = 4 j3/j2²** (sympy solve).

**CHECK 2 PASS** — G does NOT cancel. The memo's self-reported "first-pass G-cancels
error" was real, and the corrected 1/G scaling is what makes the edge a codim-1 SURFACE
(≥1 free knob), not a point. This is the load-bearing correction and it holds under
independent re-derivation.

## CHECK 3 — explicit gain-line moments: is the edge surface genuinely free?

Computed j2=⟨1/s²⟩, j3=⟨1/s³⟩ as real Lorentzian-line inverse moments over an IR-gapped
bath (s≥s0=H²=1), scanning center s_g∈{1.5,2,3,5}, width Γ∈{0.3,1,2}. The edge amplitude
G_edge=4 j3/j2² ranges **6.85 .. 27.0 (≈3.9×)** over this modest grid — it is NOT a single
number, it roams with the line shape. So σ6=σ6* is one equation on a free shape ratio.
**CHECK 3 PASS** (the memo's wider 10–266× span just reflects a broader knob range; same
qualitative result — never identically 1).

## CHECK 4 — STEELMAN: does saturation pin G to the edge or to gain=loss?

Part-1 saturation rate equation dI/dt=[g0/(1+I/I_sat)−κ]I has stable operating point
I*=I_sat(g0/κ−1), f'(I*)=κ(κ−g0)/g0<0, and the gain CLAMPS to g_eff(I*)=κ exactly
(sympy identity). So saturation pins the operating amplitude to **G_sat=loss** — a
loss-set number, NOT 4 j3/j2². Across the line-shape scan G_edge/G_sat roams 6.85–27×
and never equals 1. **CHECK 4 PASS** — saturation delivers a genuinely STABLE, peaked
operating point (the real maser win, resolving QQ Route-1's LTI runaway), but pins it to
the lasing threshold, a DIFFERENT condition than the dispersion soft edge. Stability ≠
edge-coincidence.

## CHECK 5 — scale audit: is c_χ tied to H by any X2/foliation constraint? (would collapse a scale)

Verified against the banked source `agentEE_sigma_khronon.py`: the khronon modes are
Minkowski-form (1206.1083 reparam-symmetric foliation), c_χ²=O(γ/α) is an independent
matter-sector/PPN datum, and the pullback amplitude A(b)=H²/(16π²c_χ(c_χ²−b²)) carries
c_χ and H as SEPARATE scales. No identity collapses c_χ→H. **CHECK 5 PASS** — agentEE
STEP 1's "NO" stands; the one thing that could upgrade the verdict (a scale collapse) is
absent. The k* magnitude prediction therefore genuinely uses pre-banked {H, c_χ, a₀}.

---

## INDEPENDENT PARAMETER COUNT

| parameter | role | fixed by dS pump? |
|---|---|---|
| s0=H² | bath spectral scale | **YES** (H = pump's only scale) |
| c_χ | khronon sound | NO — independent datum (agentEE) |
| a₀ | deep-MOND floor | pre-banked constant |
| → k* MAGNITUDE k*~(c_χ/√a₀)H | | **0 new knobs ⇒ FORCED** |
| s_g/s0 (center) | gain/QNM line center | NO — free spectral datum (KNOB 1) |
| Γ/s0 (width) | gain/QNM line width | NO — free spectral datum (KNOB 2) |
| G (amplitude) | operating point | pinned by saturation to gain=loss ≠ 4 j3/j2² (KNOB 3) |
| → k*=EDGE (σ6=σ6* ⟺ G=4 j3/j2²) | | **≥1 free knob survives ⇒ NOT FORCED** |

After saturation fixes G=loss for stability, the edge still requires the leftover shape
ratio center/width tuned so that 4 j3/j2²=loss — one residual tuned dimensionless ratio,
a codim-1 surface. **The forced-claim does NOT hold on the coincidence axis.**

---

## REGRADE — CONFIRMED (FOLD-DELIVERED-MODEL-DEPENDENT)

Every load-bearing step reproduces independently: the inflection cubic and triple-root
σ6*=σ4²/(4c_χ²) (CHECK 1); the G-does-not-cancel 1/G edge scaling (CHECK 2, the central
hostile check); the genuinely free, shape-roaming edge surface (CHECK 3); the saturation
pinning to gain=loss not the edge (CHECK 4); and the absence of any c_χ↔H scale collapse
(CHECK 5). The saturated response is genuinely stable (no hidden runaway: f'(I*)<0, gain
clamps to loss).

**The route did NOT smuggle a tunable knob in as forced.** On the contrary, it is honest:
it claims FORCED only for the k* MAGNITUDE (which I confirm is a clean zero-knob
scale-grade prediction from pre-banked constants) and explicitly labels the edge
COINCIDENCE as tuned (codim-1, ≥1 free line-shape knob). My independent parameter count
returns the SAME split — magnitude forced, coincidence tuned. No surviving free knob was
relabelled as forced; if anything the memo is conservative (it does not over-credit the
maser hook, correctly noting saturation buys stability, not coincidence).

**Verdict: FOLD-DELIVERED-MODEL-DEPENDENT — CONFIRMED.** The framework PREDICTS the k*
scale and ACCOMMODATES the k*=edge coincidence via one tuned QNM/gain-shape ratio.
The next calc the memo names (compute the actual dS QNM spectral center/width from the
Gibbons-Hawking heat kernel and test whether a SYMMETRY forces it onto the edge surface
4 j3/j2²=G_sat) is the correct and only way to upgrade accommodation → prediction.
