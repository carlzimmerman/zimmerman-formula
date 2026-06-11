# agentFF — Hostile audit of agentX's built EOM (the red team)

*C. Zimmerman + Claude, 2026-06-11. The standing rule executed: framework-favorable results get
hostile verification, and agentX's built causal EOM + Theorem X2 + invoice was the campaign's most
framework-favorable construction. Run: `agentFF_x_hostile_audit.py` → `agentFF_x_hostile_audit.out`
([FF-DONE]: all four audit items executed). **Orphan-completed memo**: the agent finished its full
computational program and died (spend limit) before writing this file; every claim below is
transcribed from the machine-verified `.out`, nothing added.*

## VERDICT: **X2 SURVIVES-STRENGTHENED; the EOM SURVIVES every attack; three framings CORRECTED (none verdict-changing); one NEW positive result (the ledger's sign).**

## [FF-1] Theorem X2 re-derived from scratch — SURVIVES, and is STRONGER than X claimed

- **Independent route** (microscopic passive baths, exact elimination — no Bochner/analyticity
  input): every positive bath mode ADDS DC inertia (μ̂(0) − μ̂(∞) = Σmⱼ ≥ 0); 2000 random positive
  baths (1–12 modes, 6 decades): the ordering NEVER inverted. X's numerically-pinned passivity
  convention confirmed by algebra. M22's required inversion infeasible for ANY positive measure.
  **Agreement with X: exact.**
- **Loophole (a) — nonlinearity — CLOSED with a stronger theorem.** X treated the linearized
  kernel; FF proves the nonlinear statement in two lines (Willems storage-function form): for ANY
  medium with energy bounded below prepared in its ground state, the MOND secular trajectory
  requires ∫(1/μ − 1)F·v dt > 0 of free energy — contradiction. **No passive medium, linear or
  NONLINEAR, closes the secular channel.** Machine check: 30 adversarial nonlinear vacuum baths
  (soft/stiff/quartic over 4 decades) reach at best R = 0.30 where MOND needs R = 3.58; a ghost
  bath (energy unbounded below) reaches R = 2.2×10⁷ — the only loophole lives exactly at X's
  corollary option (b), already dead by agentU's gate 1.
- **Loopholes (b)+(c) — the non-L1 kernel and the limit interchange — CLOSED.** The M22 kernel's
  DC kink (μ̂ ~ √(2x_c)|ω|) implies a real 1/τ² tail (verified to 0.1–0.3% against prediction):
  χ is NOT L1, only tempered/L2. The KK-forced Im μ̂ was therefore recomputed by independent
  machinery (adaptive-quadrature Hilbert transform, no FFT, no grid): matches agentX's FFT values
  to 0.02–0.17%; the sum rule closes to 0.6%. The Fourier-limit statements survive non-integrability.

## [FF-2] The Galley/SK dynamics attacked — SURVIVES; the ledger's sign is a NEW positive

Verbatim reruns of `agentX_sk_kernel.py` / `agentX_sk_dynamics.py` first: **both byte-identical**
to the banked .out files. Then:

- **Step force from exact rest**: pre-onset max|a| = max|v| = 0.0 — EXACT machine zero (the
  estimator is structurally retarded); post-onset late-time a matches algebraic MOND to +0.01%.
  X's "1e-2 pre-onset deviation" confirmed as running-estimator ripple on the quiet oscillation,
  NOT future response. **No pre-acceleration, including at the impulsive limit.**
- **Sharp pulses on an empty window**: the construction survives (causal, finite, ledger-closed;
  the onset is an integrable t^(−1/3) spike — integrated observables converge under dt 0.02→0.005
  while the peak is cutoff-dependent, i.e. finite physics). **CORRECTION 1:** X's "transients pay
  ~1% of external work per event" is geometry-specific (a ×3 kick atop an already-loud line). On a
  quiet deep-MOND worldline the medium co-pays (1/μ − 1) of the external work at the event's
  effective scale: measured ×7–34 (705–3414%). The invoice's transient margin (×242) still clears
  the corrected demand comfortably — the WORDING was wrong, not the verdict.
- **The ledger's sign (the kill-question X never asked signed):** X printed |⟨P_ae⟩|. The SIGNED
  steady-state residual is **POSITIVE — the reservoir DRAINS** — and the span test (96 vs 384
  cycles: cumulative loss ×4.64 for span ×4) shows the drain is **SECULAR, not a one-time
  window-fill**. DC run: the reservoir loses 2.63× the external work in deep MOND.
  **This matches Theorem X2's invoice direction EXACTLY** (pumped medium ⇒ reservoir→worldline);
  a sign flip here would have killed the Link-5 story. It didn't — the dynamics independently
  exhibit the activity X2 demands.

## [FF-3] The "0.03% validation" — CIRCULARITY IDENTIFIED; the anchor independently CONFIRMED

**CORRECTION 2:** the 0.03% agreement against agentM's banked numbers is (i) a shared-source
regression test at the kernel level and (ii) an estimator-fidelity test at the dynamics level — a
transcription error in agentM's table would propagate undetected. The word "validation" was
overstated. FF therefore recomputed the solar-reflex anchor through a FULLY independent constants
chain (DE440 system GMs incl. the 0.02% Jupiter planet-vs-system probe, JPL J2000 mean elements,
GRAVITY-era galactic line, Planck-2018 footings re-derived from scratch: a0_fw = 9.3548e-11,
drift −0.06%): A/a_J reproduces to <0.2% for all three θ shapes; the hostile Δa to the few-% level
implied by the ×11 exponential error amplification; the PASS margins land in the same ×13–22 band.
**The banked anchor is CORRECT.** Residual flag: the agentE budget 2.47e-15 remains single-sourced
(inherited, not re-derived here).

## [FF-4] The invoice arithmetic re-derived (own chain, both footings, both H0 conventions)

Stockpile short ×51–55 (secular) / ×3572–4009 (transient) [X: ×50/×3600]; the Λ box pays
×1.5–2.4×10⁴ (secular) / ×213–350 (transient) [X: ×1.7e4/×242]; the ρ_total-vs-ρ_DE footing fork
is a ×1.46 detail — immaterial. Honest reframings hunted:
- **In-galaxy khronon gradient energy** as alternative stockpile: ×91–182 SMALLER than the
  cosmological corner stockpile — "the khronon cannot pay" is gradient-robust.
- **CORRECTION 3:** X's "+15 orders at the horizon level" compares the GLOBAL Gibbons–Hawking
  energy to a SINGLE galaxy's bill. Per-galaxy-honest (N_gal ~ 1.5×10¹¹): global secular demand
  1.6×10⁶² J vs E_GH = 1.7×10⁷⁰ J → **~8 orders, not 15**. Verdict unchanged (the bath pays).
- The box framing is CONSERVATIVE: real L* galaxies command ×2000 the (100 kpc)³ box — the true
  Λ margin is LARGER than quoted.
- H0-convention mix in X's invoice section (Planck-derived footing vs 70.0): 8% hygiene flag,
  immaterial against ×50–×3600.

## Disposition
- Theorem X2: **independently re-derived + EXTENDED to nonlinear passive media** — upgrade its
  standing; the pumped-reservoir conclusion now rests on energy conservation alone.
- The built EOM: survives step/pulse/sign attacks; **the secular reservoir drain in the X2
  direction is a new, independently computed property of the construction** (not assumed).
- Three framing corrections logged (per-event %, "validation" → regression+fidelity, 15→8 orders);
  none changes a verdict; chain/assembly patched with one line each.
- Residual single-source: the agentE reflex budget (2.47e-15) — inherited everywhere, worth one
  independent re-derivation in a future pass.
