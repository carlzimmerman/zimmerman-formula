# agentPP — ROUTE 2: the peakedness / Q-factor test of the dS QNM horizon response

**The decisive question (downstream of agentOO 851e7649 + agentS).** A roton minimum (He-II)
requires the bath response χ(k) to PEAK at a FINITE momentum k0 with a finite quality factor Q,
so that the induced self-energy lifts σ6>0 (bounds the fold) and pins the inflection k* at the
sonic edge b→c_χ. agentOO proved the smooth Gibbons-Hawking thermal continuum FAILS this (σ6<0
unbounded, Cauchy-Schwarz I2²≤I1 I3 far from saturation, k* free-floating) and named the dS
QUASINORMAL-MODE resonance as the single unbanked input that might supply the peak. agentS computed
that ladder: it is PURELY DAMPED, ω_{n,l} = −iH(2n+l+Δ), Re ω = 0 — a geometric tower of overdamped
modes with an angular (l→k) structure.

**HOSTILE PRIOR (default expectation).** Purely-damped (Re ω=0) modes are zero-centered Lorentzians
A_N(W) = (1/π)Γ_N/(W²+Γ_N²): each PEAKS AT W=0, monotone in |W|, quality factor Q = Re ω/(2 Im ω) = 0.
A roton needs a peak at FINITE k. So the default expectation is that the QNM response is BROAD /
zero-centered / stiffening, NOT roton-capable. A claimed finite-k peak must survive scrutiny against
this prior.

**Coefficient quarantine (enforced).** This round is STRUCTURE only — peaked-at-finite-k vs
broad/monotone, and the effective Q vs the roton threshold. q=1/4 / ζ-tilde / (16π/3)^(1/4) stay
quarantined downstream; q=1/4 NEVER asserted.

---

## PART 1 — the single-mode shape: each QNM is a zero-centered Lorentzian, Q=0 (computed)

`/tmp/agentPP_p1.py`. A purely-damped QNM ω = −iΓ contributes A_N(W) = (1/π)Γ/(W²+Γ²): for
Γ ∈ {0.3,1,3} the peak is at W=0.0000 (machine), monotone decreasing in |W|. Re ω = 0 ⇒ Q = 0.
**Each individual dS QNM is the broadest possible (zero-centered, Q=0) Lorentzian — the hostile
prior's starting point is confirmed at the single-mode level.** The only way a finite-k peak can
appear is COLLECTIVELY, from the l→k angular tower. That is the real test (Parts 2–4).

---

## PART 2–3 — the collective χ(k, W=on-shell) from the QNM tower (computed)

`/tmp/agentPP_p2.py`, `/tmp/agentPP_p3.py`. Build the retarded response at momentum k from the
QNM expansion χ(k,W) = Σ_{n,l} c_{n,l}(k)/(W−ω_{n,l}), with the standard horizon dictionary l↔k
(proper wavenumber at the horizon k_phys = √(l(l+D−2))/r_h ~ l·H ⇒ l ~ k/H), evaluated on-shell
W = c_χ·k.

- **Stripped of any Gaussian angular window (p3, the honest test), the response is broad/monotone.**
  Across residue models (unit / thermal-overtone-suppressed / geometric-QNM) and c_χ ∈ {1,2}: |χ|
  always peaks at k→0; Re χ (the dispersion-shifting part) has at most a LOW-k shoulder at
  k ≈ 0.16–0.46 (the horizon scale), then falls. The p2 apparent "finite-k peak at k~5" was a
  Gaussian-window artifact — it disappears under the proper l↔k dictionary.

## PART 4 — the analytic heart: why no roton peak (sympy)

`/tmp/agentPP_p4.py`. The dominant n=0 mode at l=k/H has width Γ_0(k) = HΔ + k and on-shell
W = c_χ k, giving the exact response

    Re χ(k) = c_χ k / ( c_χ² k² + (HΔ + k)² ).

- **Q-factor ≡ 0 at every k.** Every dS QNM is purely damped (Re ω=0), so its quality factor
  Q = Re ω/(2 Im ω) = 0. A sum of poles all on the negative imaginary axis cannot produce a
  finite-real-frequency pole (no cancellation moves a pole off the imaginary axis). So the
  collective response is a zero-centered Lorentzian of width Γ_0(k) for EVERY k: Q(k)=0 ∀k. The
  roton/underdamped threshold Q ≳ 1/2 is NEVER met. **Structurally BROAD — confirmed analytically.**
- **The single extremum of Re χ(k) is at k* = HΔ/√(c_χ²+1) (sympy, exact).** This is a horizon-scale
  shoulder (set by H and Δ), NOT a roton minimum at a large internal-scale k0.
- **The on-shell ratio W/Γ_0 = c_χ k/(HΔ + k) → c_χ = const as k→∞.** The damping grows LINEARLY
  with k (because l ~ k/H ⇒ Γ_0 ~ k): the mode never sharpens at any k. There is no momentum at
  which the response goes underdamped. This is the structural reason a purely-damped, geometrically-
  spaced tower cannot peak.

## PART 5–6 — does it lift σ6>0? Cauchy-Schwarz saturation test (computed)

`/tmp/agentPP_p5.py`, `/tmp/agentPP_p6.py`. Feed the QNM bath spectral density J_QNM(W) =
Σ_{n,l} c (1/π)Γ_{n,l}/(W²+Γ_{n,l}²) (a tower of ZERO-CENTERED Lorentzians) into agentOO's
spectral-moment machinery. σ6>0 (bounded fold) requires the Cauchy-Schwarz ratio
R_CS = I2²/(I1 I3), I_p = ∫dW J/W^{2p}, to approach its ceiling 1 (only a sharp/peaked spectrum
saturates).

- **CONTROL (validates the test):** a Gaussian peak at W0=5 with width s: s=0.02 → R_CS=0.9999;
  s=0.2 → 0.9935; s=3 → 0.53. A genuinely SHARP peak DOES saturate ⇒ would lift σ6>0. The test
  discriminates correctly.
- **dS QNM bath:** R_CS = 0.558 (unit), 0.577 (thermal), 0.584 (geom) — **the same broad/unbounded
  band as agentOO's smooth GH continuum (0.33–0.63), nowhere near 1.** ⇒ **σ6 < 0 (UNBOUNDED) —
  the purely-damped tower does NOT lift the stabilizer.**

## PART 7 — hostile self-check: give the framework its best shot (computed)

`/tmp/agentPP_p7.py`. Three attacks on my own "broad" conclusion:

- **(A) Isolate the lowest single QNM:** R_CS = 0.57 — a single zero-centered Lorentzian is the
  broadest possible. Isolating modes does NOT help.
- **(B) Single angular channel, evenly-spaced overtone tower (KMS/Matsubara-like comb of imaginary
  poles):** R_CS = 0.556–0.570 for l=0,5,20. **A comb on the negative imaginary axis builds no
  real-frequency resonance** — a Matsubara comb is not a peak in real W.
- **(C) Direct roton-dip test** on ω_eff²(k) = c_χ²k² − κ·Re χ(k)·k²: a local minimum at finite k
  appears at ONLY ONE fine-tuned point (c_χ=1, κ=2, at a horizon-scale k≈0.6) and VANISHES for
  κ=0.5, κ=5, and all c_χ=2 — monotone-rising (stiffening) everywhere else. **The dip is fragile,
  coupling-tuned, and horizon-scaled — not a structurally forced roton minimum.**

## PART 8 — numerical integrity + the edge-pin verdict (computed)

`/tmp/agentPP_p8.py`. R_CS is stable under grid refinement (400k→1.5M points) and tower truncation
(n≤20,l≤40 → n≤40,l≤90): 0.5588 → 0.5579 → 0.5573 — robustly ≈0.56, robustly <1 (unbounded).

**Edge-pin:** the only extremum of Re χ(k) is k* = HΔ/√(c_χ²+1) — set by the horizon scale H and
the probe dimension Δ, with NO dependence on the sonic edge b→c_χ. **The QNM response cannot PIN k*
at the sonic edge; k* tracks H, not the sonic horizon.** Edge-pin FAILS in addition to the peak and
the σ6 bound.

---

## VERDICT: BROAD-ZERO-CENTERED — the QNM route does NOT supply the peak (STILL-UNBOUNDED)

The hostile prior is REALIZED, and it is realized by computation, not by assumption. The dS
quasinormal-mode horizon response is **structurally BROAD / zero-centered, not peaked at finite k**:

1. **Peak — FAILS.** Q(k) ≡ 0 for all k (every QNM has Re ω=0; a sum of negative-imaginary-axis
   poles stays zero-centered, analytically). The damping Γ_0(k) ~ k grows with k, so the on-shell
   ratio W/Γ → c_χ = const — the mode never sharpens. The only extremum of Re χ(k) is a horizon-
   scale shoulder at k* = HΔ/√(c_χ²+1), not a roton minimum.
2. **σ6 bound — FAILS (STILL UNBOUNDED).** R_CS = I2²/(I1 I3) ≈ 0.56 for the QNM bath — the same
   broad/unbounded band as the smooth GH continuum, far from the saturation (→1) a sharp peak
   reaches in the validated control. σ6 < 0 persists; the QNM resonance does NOT lift it.
3. **σ4 sign — held (not the point here).** The bend direction σ4<0 was already FORCED by agentOO
   for any passive bath; the QNM bath is passive (J≥0), so σ4<0 is inherited. The QNM route does not
   threaten the sign — it simply fails to ADD the missing peakedness.
4. **Edge-pin — FAILS.** k* tracks H/Δ, not b→c_χ; still free-floating relative to the sonic edge.

**Why (the structural reason, not a tuning).** A roton (He-II) needs a bath response that PEAKS at
finite momentum with finite Q — a sharp/underdamped resonance. The dS QNM ladder is the OPPOSITE
kinematic class: purely overdamped (Re ω=0, Q=0), and its angular tower has the relevant mode's
WIDTH growing linearly with k. The "internal scale" the QNM ladder carries (the spacing 2H, the
offset HΔ) lives entirely on the IMAGINARY axis, so it shows up as a horizon-scale damping/shoulder,
never as a real-frequency peak. agentOO's hope — that the QNM resonance, being "peaked," would lift
σ6>0 and edge-pin k* — does NOT survive: these QNMs are resonances in the COMPLEX sense (poles) but
NOT peaks in the real-frequency response, and only the latter is what a roton needs.

**LINK-5 UPDATE.** The bend SIGN (σ4<0) remains forced (agentOO, inherited — passive bath). But the
named "peaked dS QNM horizon resonance" — the single unbanked input agentOO/NN pinned the controlled
fold on — is, when actually computed, BROAD: it does not lift σ6>0 (still unbounded), does not peak
at finite k, and does not pin k* at the sonic edge. **The roton operator is NOT delivered on this
route.** The dS QNM ladder is the wrong kinematic class (overdamped) to bound the fold. A controlled
Airy fold now needs a DIFFERENT named input — a genuine finite-real-frequency, finite-Q resonance
(an underdamped horizon/medium mode, which the purely-damped dS static-patch spectrum does not
provide) — or the mechanism stays a candidate with the stabilizer unsupplied.

**This route decided whether the QNM idea works AT ALL: it does NOT supply the missing peak.**

---

## Smuggle guards (held)
- q=1/4 NEVER asserted; ζ-tilde / (16π/3)^(1/4) quarantined. Round computed ONLY peaked-vs-broad,
  Q, R_CS (σ6 sign), and the k* extremum — structure, not coefficient.
- Both-ways honesty: the framework-favorable outcome (a peak) was given its best shot in Part 7
  (isolated modes, KMS comb, direct roton-dip scan) and FAILED on the merits — the broad verdict is
  the computed result the hostile prior expected, not a reflexive dismissal. The CONTROL (Part 6)
  proves the test WOULD have detected a real peak (sharp Gaussian → R_CS=0.9999); the QNM bath simply
  is not sharp.
- The one framework-favorable thing that DID survive (σ4<0 inherited, passive bath) is reported, not
  buried.

## Scripts (all /tmp/, deterministic, re-run clean)
- p1 single-mode zero-centered Lorentzian / Q=0; p2 windowed χ(k) (artifact flagged);
  p3 honest l↔k χ(k) (broad); p4 sympy analytic Q≡0 + k* extremum; p5/p6 Cauchy-Schwarz σ6 test
  + validated control; p7 hostile self-check (A/B/C); p8 integrity + edge-pin.

</content>
