# The Residual Doors, Computed (2026-07-03)

**Question.** The six-theorem chain (Theorems I–VI; VI = Zenodo 10.5281/zenodo.21175723) closed covariant modified inertia and, per this program's practice, *named* its own residual doors instead of declaring victory: (D1) the interacting-field windowed response; (D2) the passive-anharmonic corner; (D3) the unsettled-population transient observable; (D4) the flat-curve EP closure of Theorem IV. Carl's directive: "more doors are open so we need to calculate them." All four computed — 4 lanes + 4 independent adversarial verifiers (two verifier re-runs after infrastructure failures, zero physics failures), 21 scripts, all exit 0, both a₀ footings throughout.

**Net: the theory-side doors CLOSE (D1 at 2nd order, D2 generally, D4's soft spot found-then-killed), and the pheno door D3 OPENS into a pre-registerable prediction table with one clean MI-unique signature.** Corrections found by verifiers are printed beside the results they amend, including one genuine partial success of an open-direction attack (D2) and one correction to our own published Fourth Horn (D4).

Scripts: `real_research/reviews/residual_doors_2026_07/`. Runs: `wf_825bbb8f-919` + direct verifier agents.

---

## D1 — The interacting-field window: CLOSED at 2nd order

The named mind-changer of Theorem VI leg (iii): free-field positivity locks might not bind *interacting* fields.

- **Positivity is theory-independent:** F(ω) ≥ 0 is a Gram/norm fact for any state of any QFT (two-line operator proof; confirmed to machine precision in a nonintegrable Ising chain — global min +3.7e-7 on scale 316).
- **Uniform trajectories, any interacting Wightman QFT:** Bisognano–Wichmann gives wedge-KMS; a new **monotone-window lemma** (proved + verified) shows F(ω) ≤ F(−ω) survives *any* window length for Gaussian-class windows — max[F(ω)/F(−ω)−1] = −2.7e-2 over the scan; T→∞ recovers e^{−βω} to 5 digits. The one artifact class (boxcar windows: sinc zeros × narrow lines, ratio 22.7) vanishes for Gaussian windows (~1e-118) and for all continua — a *window* artifact, not physics.
- **Non-uniform trajectories:** honestly NOT closed by Pusz–Woronowicz (the external agent supplies work) — so computed. Key theorem: **Källén–Lehmann reduces the interacting vacuum's windowed response on any trajectory to a positive mixture of free massive-slice responses** (exact at 2nd order in detector coupling). Scanned 28 burst/oscillation/kick configurations across the mass slices: no inversion anywhere (closest margin −3.8e-2, quadrature-stable; the massless slice reproduces Theorem VI's identity to 0.9999).
- **The driven benchmark keeps everyone honest:** a nonperturbative driven interacting lattice (Kim–Huse) *does* invert (11.4× at the drive-Stokes sideband ω\*=2Ω−ΔE) — but the free-fermion control inverts **407×** under the same drive. Inversion is agent-pumped Raman gain — the pump channel Theorem VI already prices (×2.9e10 shortfall).

**Verifier: UPHELD.** The KL positive-mixture step was independently re-derived from scratch on a genuinely composite operator (:φ²:, two-particle continuum, KL density ρ=1/(πμ²β) derived via the CM Jacobian): the direct position-space pulled-back response on a non-uniform burst equals the free-slice mixture to 1e-4–4e-4 **with zero fitted constants**. Strongest open attack (7 configs beyond the lane's grid — light masses, sharp fast bursts s→0.01/v0=0.95, chirps, off-center windows, resonance-tuned oscillations mimicking the lattice gain): **no inversion anywhere**; the margin thins monotonically toward zero as kicks sharpen (−4.6e-2 → −1.9e-2 → 0⁻) — **asymptotic equality, never crossed** (in 3+1D the k²dk phase space never blocks emission resonances, unlike the discrete lattice). Corrections: one cosmetic number-provenance error (the claimed positivity min +3.7e-7 is the moving-probe row; the true global min is 4.5e-14 — positivity holds either way) and one docstring sign-convention swap (code correct). Named residuals genuinely open (assessed, not closable now): 4th-order/4-point-function effects (outside Theorem VI's own object) and Bros–Moschella dS-KL positivity for light/complementary-series interacting fields.

## D2 — The passive-anharmonic corner: CLOSED, with the verifier's instructive catch

The last pump-free route to the MOND sign. Lane result, all theorem-grade where claimed:

1. **Linear response, any anharmonicity, any stationary passive state:** in the common ρ/H eigenbasis every Bohr-line weight is (p_n−p_m)|B_nm|² ≥ 0 under passivity ordering ⇒ ω·Imχ(ω) ≥ 0 ⇒ δm = (2/π)g²∫Imχ/ω³ ≥ 0. **KMS is not needed** — passive-but-not-KMS covered directly. (Min Bohr-line weight over 2000 random anharmonic passive cases: +1.2e-8; passive-polytope extreme points: 0 exactly, term-by-term.)
2. **Non-perturbative in coupling** (adiabatic worldlines): the O(v²) mass coefficient is the exact pair sum 2g²Σ(p_n−p_m)|⟨m|dH/dx|n⟩|²/ω³ over the full displaced spectrum — term-by-term ≥ 0. Exact-diagonalized quartic scans (λ 0–3, displacement 0–5, thermal + random-passive): global min +3.2e-4; the most adversarial *non*-passive state gives −0.0038 (passivity, not model structure, is the binding constraint). One fake counterexample caught and killed by the lane itself (NF=90 truncation artifact printing −213; converged NF=320 → all-passive positive).
3. **Degeneracy edge sealed:** within-subspace coherences (which passivity permits) commute with the block Hamiltonian — constant geometric forces, zero inertia contribution; near-degenerate passive pairs *harden* (+1/ω₀³).

**Verifier: UPHELD, with a partial success of the open-direction attack — the most instructive result of the fleet.** Pushing into the lane's own named un-theoremed sliver (gA=5 at the two-photon resonance 2Ω≈gap, beyond the lane's gA≤3 scan): the reactive dressing **genuinely goes negative from a passive start** (δm_dyn = −0.0169, quartic λ=1). The lane's "never crosses 0" was a scan-range artifact. The autopsy shows why this is not a pump-free MOND channel: (i) frequency-locked to a narrow window (Ω/gap 0.40–0.56; positive again at 0.60) — a frequency law, never μ(a/a₀); (ii) Pusz–Woronowicz holds throughout (bath *absorbs* +5.07 per protocol; never negative); (iii) the drive de-passivizes the bath before softening it (6 ordering violations vs 0 initially) — **the drive IS the pump**; (iv) band-mapped, it needs bath gaps ≲1e-31 eV → the gas clamp (Theorem V) applies exactly as for the sub-drive pole.

**Amended closure (as it should be cited):** passivity alone forces δm ≥ 0 (linear response at any anharmonicity; non-perturbatively for adiabatic worldlines; degeneracy edge sealed); the passive softening channels are the sub-drive pole **and its multiphoton/Floquet-dressed generalization** — both frequency-locked, both drive-pumped, both clamped by Theorems IV/V. **No pump-free MOND-sign channel exists.** The verifier independently re-derived the pair-sum formula on a different anharmonic model, different truncation, different integrator: dynamical mass measurement matches the dispersion formula to 0.58%, gap-sweep log-log slope −3.000000.

## D3 — The unsettled-population observable: A PRE-REGISTERABLE PREDICTION TABLE (verified, with 4 corrections folded)

The productive door. The Theorem-VI transient (Luo window tail) fused with the banked memory-kernel σ-spread into one amplitude-vs-settledness curve, on the framework's own objects (Lorentzian memory kernel, τ=0.45 Gyr, θ₀∈[√2,2] band).

**The table as it should stand (= the verifier's corrected chM-only version):**

| System / class | Predicted relational σ signal (both footings) | Notes |
|---|---|---|
| Crater II | **+13.6 to +26.5%** | y_cur=0.57, y_peri=3.28, t_peri=0.77 Gyr, phase 0.27 |
| Antlia II | +3.4 to +6.7% | phase 0.96 (near apo) |
| Sagittarius | +23 to +27% | tidally dirty — not a clean carrier |
| **First-infall dwarfs/cluster members** | **−11 to −21% (a DEFICIT)** | **the sign flip at pericentre — the one clean MI-unique signature** |
| Leo I | ~0 (density-gate null) | chM-null control |
| Settled controls (Fornax/Sculptor class) | <2% | |
| Cluster relational spread (recent-infall vs virialized) | +6 to +13% | recovers the banked band |

**Verifier corrections (all folded above):** (1) a factor-2 bug in the Luo-tail print (chL(n=1) = 4.0%, not 2.0%; tail band 0.4–4.0%); (2) the named-systems script's TOTAL column double-counted the one-sided chL *upper envelope* as a central value (printing Crater II +28–41%) — the defensible numbers are the chM-only table above; (3) the "exponential-decay clock is MI-unique" discriminator is **downgraded**: post-shock tidal revirialization mimics it on diffuse carriers (t_cross = 0.86·τ_mem for Crater II) — **the clean MI-unique signature reduces to the first-infall sign flip** (tides and MG cannot make a coherent *deficit* that flips to excess at pericentre; MG/AeST predict exactly zero relational effect); (4) the Luo tail alone is a positivity-locked one-sided envelope — no standalone test (a null cannot falsify an envelope).

**Decisiveness:** matched-pericentre matched-density phase comparisons; 3σ ≈ **2029–2030** (MW dwarfs: Gaia DR4 orbital phases + WEAVE/4MOST σ's; 9 carriers/arm at 10% signal, 7% error) and **2028–2031** (CHANCES cluster infall populations, 6% vs 2% bin error). Footing fork: orbits/phases are a₀-free; carrier status holds both ways; no verdict flips.

## D4 — The flat-curve EP closure: PARTIAL — the named residual finished, a soft spot found, and the horn still dead (by a different brick)

Theorem IV's "pending Coriolis linearization" done in full (radial-azimuthal PU linearization in the self-consistent flat-curve potential, degree-8 characteristic polynomial, verified by companion-matrix eigenvalues AND nonlinear orbit integration — runaway rate matches the EP prediction to 1.5%).

- **The exact flat-curve answer:** PT-broken band **μ ∈ (0.7579886, 0.8947874)** (zeros of 664μ⁴−3036μ³+5086μ²−3681μ+971). The published crude estimate 0.854 was wrong in *both* directions (it sits inside the band; there is a re-entrant real window (0.5, 0.758) the scalar shortcut missed; below μ=1/2: saddle + complex quartet, doubly unstable). Family map κ/Ω ∈ [1,2]: upper edge 0.892–0.9 nearly universal; the harmonic case is the unique never-breaking endpoint — **a printed correction to our own published Fourth Horn number.**
- **A genuine soft spot (found by our own both-ways rule):** for general kernels k(y), the fold obeys the exact law **μ_fold = 1 − 1/(2p)**. Sub-quadratic PU kernels (the framework-tail p=1/2) are **PT-real at ALL μ < 0.5486** — deep-MOND PU orbits *exist and are linearly stable* there. The Fourth Horn's blanket "deep MOND fails by orbit non-existence" is **quadratic-proxy-specific**, not PU-class-general.
- **The horn stays dead — by profile inversion, not the EP:** those kernels force d ln(1−μ)/d ln R = −2p while the framework's ν on a flat curve requires ≈ +1 — sign-opposite slopes, mismatch **×49–80 on realistic 2–20 kpc disks** (verifier-corrected from the ×100 asymptotic bound; ×493–799 for p=1). Footing spread ~10%, no flips. Verifier: UPHELD (26-check independent re-derivation; nonlinear confirmation of the fold law at p=3/4, fold exactly μ=1/3; tried to kill the soft spot — it's real — and to kill the kill — it holds).
- Scope: PU horn only. The framework's own nonlocal-kernel MI and its phenomenology are untouched.

---

## Standing after the fleet

- **The pump requirement is now fully general** (D2): no passive medium of *any* structure, probed *any* way, carries the MOND sign — the sign needs a pump, and every named pump is priced and clamped.
- **The interacting-field escape is closed at the order the theorems live at** (D1); the honest remaining edges are 4th-order/4-point effects and dS-KL positivity — named, specific, unclaimed.
- **Theorem IV's flat-curve bookkeeping is exact** (D4), one of its mechanisms corrected in print, its conclusion re-derived through a different wall.
- **The framework gains one new pre-registered, dated, MI-unique observable** (D3): the first-infall σ-deficit → post-pericentre excess sign flip, decisive ~2029–2031.

Per the standing rule: doors that remain open — the D1 4th-order/4-point window; dS Bros–Moschella positivity; the D3 table awaiting data; and all the empirical fronts (s̄^TX, Gaia DR4 WB, DESI DR3, BIG-SPARC).

*C.P.Z. + Fable 5 fleet, 2026-07-03.*
