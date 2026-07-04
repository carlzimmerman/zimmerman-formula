# The 4th-Order Sign Wall: The Last Computable Crack, Closed (2026-07-03)

**Question.** The whole sign chain — Theorems III–VI plus residual doors D1/D2 — lives at **2nd order in the detector–field coupling g**. At 4th order and beyond, connected 4-point functions of the interacting field first act on the detector and the Källén–Lehmann positive-mixture reduction (D1) goes silent. This is the *last computable* place the MOND sign could still hide *in the vacuum itself*, with no pump. Carl: "give me the best one and swing for it." Swung.

**Verdict: the sign wall is effectively all-orders.** No free-from-vacuum inversion or negative dressing appears at any order, on uniform or non-uniform trajectories, in free or genuinely interacting (nonintegrable) baths, or in the de Sitter corner — with named physics inputs (Bisognano–Wichmann modular theory, mean-force Gibbs states, Starobinsky–Yokoyama resummation, Bros–Epstein–Moschella Euclidean construction) rather than claimed full mathematical proof. Method note: the original 6-agent verification fleet died on a Fable-5 spend limit before doing work; this was computed directly (Opus), and includes a **self-caught overclaim** (below) — the both-ways rule doing exactly its job.

Scripts (all exit 0, ≤ the runtimes noted): `real_research/reviews/fourth_order_2026_07/`.

---

## L1 — uniform (KMS) trajectories: the lock extends to all orders

Bisognano–Wichmann is an algebra statement: the Minkowski vacuum restricted to the Rindler wedge is KMS at T_U for the *entire* n-point hierarchy of any interacting Wightman QFT — not just the 2-point function. Consequence: a detector coupled at *any* strength thermalizes toward T_U at every order, so no inversion.

Two exact, coupling-nonperturbative checks (`L1_meanforce_allorders.py`):
- **KMS / detailed balance of an interacting bath:** for a quartic (genuinely anharmonic) bath mode in a thermal state, the spectral function obeys S(−ω) = e^{−βω}S(ω) to **6.6×10⁻¹³**, at λ up to 1.5 and β from 0.7–2.5. The up/down rate ratio is fixed at e^{−βω} < 1 at every order ⇒ stationary p_e/p_g < 1: no inversion.
- **Mean-force Gibbs populations** (the exact all-orders stationary state, no Born, no RWA): diagonalizing the full joint qubit+anharmonic-bath Hamiltonian, the bare-basis gap p_g − p_e stays positive across g = 0→3 — **min +0.092 at g=3**, where mean-force has already shifted populations by 0.41 from bare Gibbs (i.e. far beyond 2nd order). Bare-basis inversion never occurs from a KMS bath. The mean-force subtlety (the one candidate crack) was checked explicitly: it shifts the gap but never flips its sign.

## L2 — non-uniform trajectories, exact (all orders automatically), and a self-caught overclaim

Off uniform motion there is no wedge/KMS and the external agent does work — the 2nd-order KL lock was the only shield, silent at 4th order. Attacked with exact joint unitary evolution (contains all orders in g) of a detector dragged through the exact ground state of a **nonintegrable mixed-field Ising chain** (hz≠0, genuine connected 4-point functions), free control hz=0.

**The overclaim, and its correction (recorded, per the both-ways rule).** The first pass labeled a single monotone kick a "vacuum probe" and reported it does not invert (p_e=0.39) while multi-kick/oscillation drives do — concluding the vacuum is safe and only structured drives pump. A robustness sweep (`verify_L2_vacuum_probe_robustness.py`, 54 configs) **refuted this**: single sudden kicks *do* invert (p_e up to 0.83) at strong g and short duration. The error: a *sudden switch-on of the coupling is itself a quench that does work* (its W_agent was 0.63, not zero) — the probe/drive label was physically meaningless.

**The correct, exact invariant** (`L2_nonuniform_interacting_vacuum.py`): the chain starts in its **ground state = the global energy minimum**, so it can only *absorb* energy, never donate it. Hence E_chain_gain ≥ 0, and by energy conservation for the closed detector+chain system,

> **E_det = W_agent − E_chain_gain ≤ W_agent.**

Every bit of detector excitation/inversion is paid for by the moving agent's work — verified per run (E_chain_gain = 0.24, 0.72, 3.85 for the three protocols; ledger OK). This is ground-state passivity made concrete, holding at all orders. Two sharp corollaries:
- **Interactions aid the pump, never the vacuum:** the interacting chain absorbs the agent's work *more* effectively than the free chain (E_det[int] > E_det[free] at matched drive) — 4-point structure makes *pumping* easier, the opposite of what a free MOND sign would need.
- **Weak-g sanity:** at g=0.2 a single kick gives p_e = 0.004 ~ g², reproducing the 2nd-order KL regime.

## L2b — the work-free (adiabatic) dressing: no inversion

The physically correct modified-inertia question is the *reactive* dressing in the work-free limit — the dressed ground state (`L2b_adiabatic_dressing.py`). Ramping the coupling on over increasing T_ramp, the non-adiabatic work defect W_defect falls from 1.02 (sudden) → 0.009 (slow), and the **exact dressed ground state has excited weight p_e = 0.334 (interacting) / 0.286 (free) — both < 0.5: no inversion, δm ≥ 0.** The strong-g transient inversions are quench work (large W_defect at small T_ramp), consistent with Theorem VI's quench (μ=−62 dying in one period) and now shown at all orders in an interacting bath.

## L3 — the de Sitter corner (the Bros–Moschella edge)

The framework's actual bath is de Sitter; free-field Gibbons–Hawking thermality is mass-independent, but interacting *light* fields (complementary series) were the named-open edge (`L3_dS_interacting_corner.py`).
- **Euclidean periodicity ⇒ coupling-independent KMS:** an interacting theory periodic in Euclidean time β_dS = 2π/H inherits KMS regardless of coupling — verified in the computable proxy (interacting mode on the thermal circle) to **1.9×10⁻¹²** across λ = 0→4. The only obstruction is IR-existence of the continuation for light fields.
- **The light-field gap can't reach the band, two ways:** (a) Starobinsky–Yokoyama — massless λφ⁴ in dS self-generates m_eff ~ 0.36 λ^{1/4} H, making perturbation theory IR-finite so the Bros–Epstein–Moschella Euclidean construction (hence KMS) applies; (b) even granting an unresolved complementary-series sliver, the framework's inertia response is **in-band at ω/H ∈ [15, 10800] (canonical) / [15, 8900] (alternate)** — every in-band mode has ω ≫ H, 1–4 orders above the ω ≲ H region where any light-field IR subtlety lives. The sliver cannot source in-band inertia.

---

## Standing

The sign wall — the deepest result the framework owns — now runs to **all orders**, on every route we can compute: free fields (state-blind, all times), stationary passive baths (any anharmonicity, D2), interacting vacua at 2nd order (KL mixture, D1) **and beyond** (uniform: BW all-orders + mean-force, L1; non-uniform: ground-state passivity ledger, L2/L2b), and the interacting de Sitter horizon (L3). The MOND sign requires a pump; every pump is priced and clamped; and **interactions make pumping easier, never free** — they do not help the framework.

**Doors that remain open (named, per the standing rule):** a fully rigorous 4-point theorem in the continuum (we have BW modular theory + exact lattice/ledger arguments + named physics inputs, not a single closed-form all-orders continuum proof); the strict complementary-series dS positivity question in the mathematical literature (bypassed for the framework by band-separation + the stochastic gap, not resolved in general); and all the empirical fronts (s̄^TX, Gaia DR4, DESI DR3, BIG-SPARC, the 2029–2031 σ sign-flip).

**Integrity note.** This adjudication is on record with a self-caught overclaim (the L2 "vacuum probe" mislabel), refuted by its own robustness sweep and replaced with the exact ground-state-passivity ledger. The correction *strengthened* the result: the decisive invariant needs no adiabatic assumption, just energy conservation plus the ground state being an energy minimum.

*C.P.Z. + Claude (Opus), 2026-07-03. Scripts: `real_research/reviews/fourth_order_2026_07/{L1,L2,L2b,L3}*.py, verify_L2_*.py` — all exit 0.*
