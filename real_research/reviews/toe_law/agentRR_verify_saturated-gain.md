# agentRR HOSTILE VERIFICATION — route SATURATED-GAIN (referee, 2026-06-13)

Mission: separate FORCED from MODEL-DEPENDENT in agentRR's claim
`FOLD-DELIVERED-MODEL-DEPENDENT`. Central hostile test: did the route smuggle tunable gain/saturation
knobs and relabel them FORCED? Default assumption: "forced" is overclaimed until the free-knob count
is zero. All checks rewritten independently of agentRR's code objects
(`agentRR_indep_verify.py`, `agentRR_indep_verify2.py`).

---

## (A) Dispersion coefficients σ4, σ6 — INDEPENDENTLY REPRODUCED

Re-derived via Maclaurin derivatives f⁽ⁿ⁾(0)/n! of ω²(u) = c²u − AG(u−k0²)/((u−k0²)²+G²),
u=k², NOT via the route's `sp.series` on a prebuilt `Rechi`. Exact agreement:

- σ4 = AGk0²(k0⁴−3G²)/(G²+k0⁴)³  → **matches** (sympy diff == 0).
- σ6 = AG(G⁴−6G²k0⁴+k0⁸)/(G²+k0⁴)⁴ → **matches**.
- σ4 < 0 ⟺ k0⁴ < 3G² (numerator sign; denominator and A,G,k0 all positive). Confirmed.

The peaked active line CAN supply σ4<0 (the bend the smooth GH continuum cannot — QQ). REPRODUCED.

## (B) The bounded-fold window 1 < σ6/σ6* < 4/3 — INDEPENDENTLY REPRODUCED, model-independent

This is the load-bearing geometric claim. Derived from a GENERIC IR tower
ω²=c²k²+s4k⁴+s6k⁶ (s4<0, s6>0), no gain model:

- **No-ghost** (ω²>0 ∀k>0): discriminant of s6x²+s4x+c² ≥ 0 boundary → **σ6* = s4²/(4c²)** (=1/16 in QQ units, reproduced).
- **Visible fold** (d(ω²)/dk² < 0 somewhere): min of c²+2s4x+3s6x² at x*=−s4/(3s6) negative → **σ6_fold = s4²/(3c²)**.
- Ratio σ6_fold/σ6* = **4/3 exactly** (sympy). Numerical scan flips ghost at σ6/σ6*=1.000 and fold at 1.333 to 4 digits.

⟹ bounded+visible fold lives in **σ6/σ6* ∈ (1, 4/3)**, a 33%-wide window. The route's "necessary
but not sufficient" correction to a naive reading of σ6* is CORRECT and is the real content here.

## (C) Clamp identity g_eff(I*)=κ — FORCED (existence), but I* set by FREE scales

Solving g(I*)=κ for the saturating gain gives I*=I_sat(g0/κ−1) and g_eff(I*)=κ. The hostile point:
the clamp VALUE = loss is forced by ANY monotone-decreasing g(I) via IVT — NOT special to the laser
form, hence a structural statement, not a knob. CORRECTLY labeled forced. BUT the operating amplitude
I* is set by I_sat (free) and the ratio g0/κ (free) — so the clamp EXISTS (forced) while WHERE it sits
is free. The route states exactly this. Honest.

## (D) Off-center fold-band pole at fold strength — INDEPENDENTLY REPRODUCED

Rebuilt the dressed-khronon quartic from scratch and rooted it. At fold strength (B~0.6–1.3) the worst
off-center pole is UHP (Im ≈ +0.2 to +0.9) for κ up to **5.0** (extended beyond the route's κ≤1). A
scalar/Markovian saturation clamp provably cannot hold the off-center fold band in the LHP. The route's
4th condition (k-resolved/non-Markovian clamp) is REAL, not invented. REPRODUCED and strengthened.

## (E) HOSTILE PARAMETER COUNT — the central mission

Everything the fold needs reduces to TWO dimensionless ratios in narrow bands plus one coincidence:
- x = k0²/Γ ∈ [0.10,0.30]  (center-to-width)
- y = A/(c²Γ) ∈ [1.00,1.30] (clamp strength / fold magnitude)
- k0 = b→c_χ sonic edge (coincidence)
- + a k-resolved clamp (Check D).

**The FORCED subset is clean — every member is a SIGN or EXISTENCE statement, no continuous value asserted:**
1. medium active (g0>0) — X2 passivity, sign of activity not magnitude;
2. σ4<0 bend — dS-bath level repulsion (851e7649), sign only;
3. saturation clamps amplitude — IVT, existence of the clamp not its location.

**The dS pump pins SCALES (k0~H, Γ~H), but the fold needs RATIOS.** Setting both k0 and Γ to the bath
scale H gives x~O(1), NOT a forced value in [0.1,0.3]; the smooth GH continuum is broad (large Γ, small
x in the wrong sense → σ6<0, QQ). So x, y, the edge coincidence, and the k-resolved clamp are **4 free
knobs**, none pinned by H or T_dS.

**FREE-KNOB COUNT FOR DELIVERY = 4 ≠ 0.** No knob is mislabeled forced; but delivery rests on 4 tuned
choices. The "forced" claim is correctly limited to signs/existence.

---

## REGRADE: CONFIRMED — FOLD-DELIVERED-MODEL-DEPENDENT

- recompute_agrees = YES (σ4/σ6 exact, 4/3 window exact, clamp identity exact, UHP-at-fold-strength reproduced and extended to κ=5).
- forced_claim_holds = the FORCED subset is exactly {active-sign, σ4<0-sign, clamp-existence} — all
  sign/existence, zero continuous values. The route did NOT smuggle gain/saturation magnitudes into
  "forced." The amplitude-runaway-tamed result is genuinely the one new forced thing this route banks.
- The route's own self-grade MODEL-DEPENDENT is correct and, if anything, conservative — the hostile
  count independently returns 4 free delivery knobs, matching the route's (a)-(d).

Verdict UPHELD: **FOLD-DELIVERED-MODEL-DEPENDENT.** Saturation forces the amplitude clamp (retires QQ's
runaway objection); the bounded edge-pinned fold still needs the narrow x, the fold-magnitude y, the
sonic-edge coincidence, and a k-resolved clamp — 4 knobs the dS pump does not fix.

Quarantine held: only signs, ratios (4/3), pole locations, fixed-point structure computed. q=1/4, ζ̃,
(16π/3)^{1/4} never touched.
