# agentRR — ROUTE 1: the SATURATED-GAIN / laser-threshold construction. Does saturated gain deliver the bounded edge-pinned roton fold, FORCED or model-dependent? (2026-06-13)

**The banked state (agentQQ, commit 20b0a43e).** The controlled roton fold is
SELF-CONSISTENT-BUT-UNDELIVERED. Established: σ4<0 (the dS-bath bend) is FORCED; a stable
CS-violating window EXISTS (active ≠ anti-damped — negative spectral-weight SIGN breaks passivity
while the pole LOCATION stays in the LHP = stable); the no-ghost threshold is σ6* = σ4²/(4c_χ²) = 1/16
in QQ's units, with the soft sonic edge at the triple root. THE GAP: a plain LTI active gain is
BOUNDS-BUT-UNSTABLE — a *visible* fold needs gain ≫ the instability onset e_inst~0.015, and any LTI
gain that strong opens a UHP pole (runaway). So delivery needs a PEAKED, SATURATED (non-LTI /
nonlinear) active response that lands σ6≥σ6* on the STABLE branch with k* pinned at b→c_χ.

**The physical hook this route tests.** A SATURATED GAIN MEDIUM near threshold (laser/maser physics)
is the textbook example of a peaked, active, STABLE response: saturation pins the operating point and
tames the LTI runaway. The question — is the Λ-pumped khronon (X2's active reservoir) a saturated-gain
"maser-like" medium, and does saturated gain deliver the bounded edge-pinned fold, FORCED by the dS
pump or a tunable model choice?

**Quarantine (held throughout).** q=1/4, ζ̃, (16π/3)^{1/4} never asserted — only signs, pole counts,
saturation-fixed-point structure, the σ6-vs-σ6* threshold, and the forced-vs-free ledger.

---

## PART 0 — the model and the three demands (stated before computing)

The X2 active reservoir gives a khronon retarded inverse propagator
> D(ω,k) = ω² − c_χ²k² − Σ(ω,k),
with Σ the in-medium self-energy from the Λ-pumped (active) dS bath. The LTI piece QQ exhausted is a
negative-residue Lorentzian gain band; this route replaces it with a SATURATED gain — the laser form
> Σ_gain = g(k) / (1 + |χ|²/I_sat),
where |χ|² is the khronon intensity at the operating point and I_sat the saturation intensity. The
three demands delivery must meet, all at once:

- **(D1) tame the LTI runaway** — the operating point self-stabilizes above threshold (gain clamps to
  loss; the UHP pole QQ found is pulled back to the real axis / LHP at the steady state).
- **(D2) produce a PEAKED response** at the gain center (so σ6 can cross σ6*, which the smooth
  continuum's σ6<0 cannot).
- **(D3) land σ6 ≥ σ6* = 1/16 on the STABLE branch with k* at the b→c_χ sonic edge** — the bounded
  fold itself.

The load-bearing honesty question (forced_or_model): of the saturated-gain parameters — gain g,
saturation I_sat, gain-center k0/ω0, width Γ — which are FORCED by the dS pump (H, T_dS=H/2π) and
which are FREE model choices? A "delivers but with N free knobs" is the honest likely outcome and
must be reported as such.

---

## PART 1 — D1: saturation TAMES the LTI runaway (gain clamping). PASS.

`agentRR_part1_clamp.py`. The unstable band's slowly-varying intensity I=|χ|² obeys the standard
above-threshold laser rate equation built from D(ω,k):
> dI/dt = [ g0/(1 + I/I_sat) − κ ] I,
g0 the small-signal (unsaturated) gain, κ the cold khronon loss. **Exact (sympy):**

- Two fixed points: I=0 and **I\* = I_sat·(g0/κ − 1)**.
- Above threshold (g0>κ): f′(0) = g0−κ > 0 ⟹ the I=0 point (QQ's LTI seed) is UNSTABLE — this is
  exactly QQ's runaway. BUT the nonzero operating point I\*>0 is STABLE:
  **f′(I\*) = κ(κ−g0)/g0 < 0** for all g0>κ (confirmed at g0/κ = 3.3, 6.7, 67, and a second I_sat).
- **The gain CLAMPS:** g_eff(I\*) = g0/(1+I\*/I_sat) = **κ exactly** (sympy-simplified). At the operating
  point the saturated gain equals the loss — Im(ω_pole) returns to 0, the pole is pulled back from the
  UHP to the real axis (marginal/limit-cycle steady state), and the exponential runaway is self-limited.

**D1 PASS.** Saturation converts QQ's BOUNDS-BUT-UNSTABLE LTI runaway into a self-limited, stable
steady state — exactly the physical hook the brief named. The operating-point intensity is finite and
the gain is clamped to the loss. *This is forced by the nonlinearity, not a tuning:* any saturating
gain (any monotone-decreasing g(I)) clamps; the clamp value = loss is a structural identity, not a
knob. (Which g(I) shape and where κ comes from IS a modeling choice — tracked in the forced/free
ledger, Part 5.)

---

## PART 2 — D2/D3: the operating-point dispersion from the saturated PEAKED gain. The signs, exactly.

`agentRR_part2_dispersion.py`. The saturated/clamped peaked gain contributes a dispersive (real-part)
self-energy. Model it as one negative-residue (active) Lorentzian gain line centered at k0 with width
Γ in the k²-variable u: Re χ(u) = −AΓ(u−k0²)/((u−k0²)²+Γ²), and read off the IR roton tower
ω²(k) = c_eff² k² + σ4 k⁴ + σ6 k⁶ by Taylor-expanding c²u + Re χ about u=0 (sympy, exact):

- **σ4 = AΓk0²(k0⁴ − 3Γ²)/(Γ²+k0⁴)³** ⟹ **σ4<0 ⟺ k0⁴ < 3Γ²** (gain center inside ~√3·Γ of DC).
- **σ6 = AΓ(Γ⁴ − 6Γ²k0⁴ + k0⁸)/(Γ²+k0⁴)⁴** ⟹ σ6 sign flips with k0²/Γ.
- So the saturated peak CAN supply σ4<0 (D2: a genuinely peaked, non-monotone response, unlike the
  smooth GH continuum which gives σ6<0 — QQ). The sign the fold needs is reachable.

## PART 3–5 — the bounded-fold WINDOW, and that σ6≥σ6* is NECESSARY but NOT SUFFICIENT

`agentRR_part3_scan.py`, `part4_foldcheck.py`, `part5_window.py` (+ symbolic re-check).
**The load-bearing correction to a naive reading of QQ's σ6*:** σ6 ≥ σ6* = σ4²/(4c_eff²) = the
NO-GHOST (ω²>0) threshold, NOT the fold-existence threshold. A *visible* roton fold needs
v_g² = d(ω²)/dk² < 0 somewhere, i.e. v_g²_min = c_eff² − σ4²/(3σ6) < 0 ⟺ **σ6 < σ4²/(3c_eff²) = σ6_fold**.
So a **BOUNDED, VISIBLE fold lives in the narrow window σ6* < σ6 < σ6_fold, i.e. σ6/σ6* ∈ (1, 4/3)**
(symbolically: σ6_fold/σ6* = 4/3 exactly). Above 4/3 the k⁶ term re-convexifies and there is only a
softening, no fold; below 1 it is a ghost. **A 33%-wide window.**

Consequences, machine-verified:
- A scan returned 115 (A,Γ,k0) points with σ4<0 AND σ6≥σ6* (IR "no-ghost"), but checking the FULL
  branch, σ6 was usually ≫ σ6_fold (large margins) ⟹ **the full saturated-gain dispersion is
  MONOTONE — NO dip — at most of them** (`part4`: a point with σ6/σ6*=14 has v_g²_min=+0.195, no fold).
- Only ~5% of the natural (x=k0²/Γ, y=A/c²Γ) area gives a TRUE full-branch bounded fold (v_g²<0
  somewhere AND ω²>0 everywhere): a band at **x∈[0.10,0.30], y∈[1.00,1.30]** (`part7`). It is a
  genuine 2D region (not a knife-edge), but it is a small, tuned corner — **~1.3 dex of tuning.**
- **The fold is bought by SONIC-EDGE SOFTENING.** The deeper the fold (v_g²_min down to ~−0.30), the
  smaller the IR sound speed c_eff² (down to ~5×10⁻⁴): corr(c_eff², v_g²_min)=+0.43 (`part8`). A
  non-shallow fold drives c_eff²→0 — exactly the b→c_χ sonic-edge coincidence QQ wanted, but reached
  by tuning the gain to the edge, not by the pump landing there.

## PART 1 + PART 9–10 — STABILITY: the clamp bounds AMPLITUDE but not the LINEAR fold pole

`agentRR_part1_clamp.py`, `part9d_resolve.py`, `part10_nonlinear_sim.py`.
- **D1 (amplitude) PASS, two ways.** The rate equation clamps g_eff(I\*)=κ and I\* is a stable fixed
  point (f′(I\*)=κ(κ−g0)/g0<0); the direct nonlinear integration settles |χ|→√(I_sat(g0/κ−1)) to
  <1% (`part10`). Saturation DOES tame QQ's exponential amplitude runaway. **But** the settled state
  is a self-sustained oscillation χ(t)=|χ\*|e^{iΩt} — a lasing, *radiating* band sitting at the pole
  ON the real axis (marginal), not a quiescent static roton branch.
- **D3 (a static stable fold) FAILS under plain (scalar) saturation.** Convention pinned against the
  passive reference and the tachyon (DC level-crossing) separated out, the retarded-pole sweep
  (`part9d`) shows: at the *small-coupling* active level the pole is LHP (Im=−0.025, the QQ
  "active≠anti-damped" stable window), but at **FOLD strength** (B~y~1.0–1.3, the magnitude the
  dispersive σ4/σ6 fold requires) the active line drives a pole into the **UHP (Im≈+0.6 to +0.9)**,
  and **NO khronon loss κ up to 1.0 rescues it.** The single global intensity clamp pins only the
  gain-center band marginal; it cannot k-resolve to hold the *off-center* fold modes in the LHP.

**The crux, plainly:** saturation bounds the amplitude of ONE mode (D1, forced), but a fold is a
property of the dispersion across a RANGE of k, and a scalar saturation clamp does not stabilize that
range. Delivering a static stable fold needs a **k-resolved / non-Markovian / structured** saturation
(a KK partner shaped to keep every fold-band pole in the LHP) — that is EXTRA structure beyond plain
laser saturation, and it is precisely the adaptive/QNM input QQ already named, now seen from the
saturated-gain side.

## PART 11 — the FORCED-vs-FREE ledger (the load-bearing answer)

`agentRR_part11_forcedfree.py`.

**FORCED by the dS pump / T_dS=H/2π / X2:**
1. the medium is ACTIVE (X2 passivity theorem — the reservoir must do net positive secular work);
2. the bend σ4<0 (dS-bath level-repulsion, banked 851e7649);
3. **saturation EXISTS and CLAMPS the amplitude** — any pumped medium saturates; the clamp value =
   loss is a structural identity. ⟹ the LTI *amplitude* runaway QQ found is TAMED. (This is the one
   genuinely new thing this route banks: D1 is forced, not a knob.)

**FREE model choices (each load-bearing for delivery — NOT pinned by the pump):**
- (a) the gain peak being **NARROW with x=k0²/Γ∈[0.1,0.3]** — the smooth GH continuum is broad and
  gives σ6<0 (QQ); the narrow peak with the right center/width ratio is the QNM input, not the bath;
- (b) the gain **MAGNITUDE** landing y~1.0–1.3 (fold strength) — pump fixes the SIGN, not the
  threshold-crossing magnitude (QQ: "forced in direction, free in magnitude");
- (c) k0 **COINCIDING with the sonic edge** (edge-pinning = the peaked QNM, not the smooth bath);
- (d) the saturation being **k-RESOLVED/non-Markovian** to hold the off-center fold modes LHP — plain
  scalar laser saturation provably does NOT (Part 9d/10).

---

## VERDICT — DELIVERS-BUT-UNFORCED (the saturated peak delivers a bounded amplitude and a peaked
## response, but NOT a static stable edge-pinned fold without 3–4 free knobs)

The physical hook is real and partly pays off: the Λ-pumped khronon, treated as a saturated-gain
medium, **does tame QQ's LTI runaway** — the amplitude self-limits (gain clamps to loss; verified
analytically and by nonlinear integration). That is FORCED by the nonlinearity, and it is the new
content this route banks over QQ. The saturated *peaked* response also **can produce σ4<0 and reach
the no-ghost floor σ6≥σ6*** (D2).

But it does NOT deliver the controlled fold on its own terms:
- **σ6≥σ6* is necessary but not sufficient** — a visible bounded fold needs the *narrow* window
  σ6/σ6*∈(1,4/3); most of the saturated-gain family overshoots into a monotone (no-fold) branch;
- the true-fold corner is a **tuned ~5% region** that requires the **sonic-edge collapse c_eff²→0**
  for any non-shallow fold;
- and decisively, at **fold strength the linearized retarded pole goes UHP for any khronon loss** —
  the scalar intensity clamp bounds amplitude but leaves the off-center fold band anti-damped. A
  static stable fold needs a **k-resolved/non-Markovian** clamp (the named QNM/adaptive input), not
  plain saturation.

**forced_or_model = MODEL-DEPENDENT.** Saturated gain converts the *amplitude* runaway into a bounded
limit cycle (forced), but the bounded-fold DELIVERY rests on four free choices — the peak's narrow
center/width ratio, the fold-strength magnitude, the edge-coincidence, and a k-resolved clamp — none
fixed by the dS pump. This is the "delivers but with free knobs" outcome the brief flagged as the
honest likely result. It does NOT regrade QQ's PARTIAL-NEEDS-MORE to delivered; it **sharpens** it:
the saturation hook removes the amplitude-runaway objection (a real gain), but relocates the entire
remaining burden onto the SAME peaked-QNM input QQ named, now joined by an explicit fourth condition
(k-resolved saturation) that scalar laser physics does not supply.

### k* edge-pinning — does the saturation scale pin k* at the edge, or is it tuned?
**Tuned.** k* is set by the gain center k0 (Part 6/8); the dS bath fixes its ORDER (k*~(c_χ/√a0)H),
but the COINCIDENCE k0 = b→c_χ is not pump-forced — it is reached only by driving c_eff²→0 (the
sonic-edge collapse), which is a tuning of the gain to the edge, exactly QQ's codim-1 edge-pinning.
The saturation/clamp scale Isat pins the AMPLITUDE I\*, not k*.

### Quarantine
Held. Only signs (σ4<0, σ6 vs σ6*, σ6 vs σ6_fold, Im pole vs 0, f′(I\*) vs 0), the 4/3 window ratio,
clamp fixed-point structure, and pole locations were computed. q=1/4, ζ̃, (16π/3)^{1/4} never touched.

### ONE-SENTENCE LINK-5 UPDATE
The saturated-gain hook **delivers the missing amplitude-stabilizer** (the LTI runaway is tamed by
gain clamping — forced), but it does **not** deliver the bounded edge-pinned fold by itself: that
still needs the narrow σ6∈(σ6*,4σ6*/3) window, the fold-strength magnitude, the sonic-edge
coincidence, AND a k-resolved/non-Markovian (not scalar) clamp — so the controlled fold stays
SELF-CONSISTENT-BUT-UNDELIVERED, now with the amplitude objection retired and the residual burden
fully concentrated on the peaked dS QNM resonance plus a k-structured saturation.

