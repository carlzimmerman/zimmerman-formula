# Correction: the EFE-vs-z prediction (#12) has the wrong mechanism — and, for the declining branch, the wrong sign. The real signal is small, transition-regime, and realization-dependent.

*C. Zimmerman, 2026-06-09. Prompted by an external review (an independent model, "Fable") that ran the QUMOND external-field estimate and found the deep-MOND EFE offset to be a₀-independent; verified and quantified here on the framework's own footing (`reviews/efe_vs_z_recompute.py`). This corrects a live overclaim in the published paper (Zenodo 10.5281/zenodo.20576485, §11 prediction #12) and in the scaling-MOND paper (§VIII). Reported per the working rule: a "this is wrong" claim checked as hard as a "this works" claim — it checks out.*

## What was claimed
- **Theory of Gravity paper, §11 prediction #12:** "EFE strengthens with z, η = g_ext/a₀(z) ∝ 1/√ρ_DE (a₀ declines ⇒ η rises), **+36% by z=3**; marginal galaxies cross to Newtonian." Billed as a distinctive test; forecast ~600–1600 galaxies.
- **Scaling-MOND paper, §VIII:** with a₀ *rising* (a₀ ∝ E(z)), "η = g_ext/a₀(z) ∝ 1/E(z): the EFE weakens with redshift, so high-z galaxies in dense environments behave more like isolated deep-MOND systems" — i.e. the embedded-vs-isolated gap *closes*.

Both narratives use the same mechanism: that the EFE suppression tracks η = g_ext/a₀, so running a₀(z) turns the EFE up or down.

## What is actually true (QUMOND, verified)
Using the standard 1D dominant-direction external-field estimate with the framework's own interpolation ν(y) = √(1+1/y) (g_obs = √(g_N²+g_N a₀)):

**1. In the deep-MOND regime the EFE offset is a₀-independent.** Analytically, for g_N, g_ext ≪ a₀,
> g_int = √a₀ · (√(g_N+g_ext) − √g_ext), so D_iso/D_emb → **√g_N / (√(g_N+g_ext) − √g_ext)** — the √a₀ cancels.

The deep-MOND EFE suppression is set by **g_ext/g_N, not g_ext/a₀.** Numerically (g_N=0.02 a₀, g_ext=0.05 a₀) the offset moves only 0.506→0.490 dex across z=0→4 — flat. **The η-mechanism is wrong; "Fable" is right.**

**2. The real z-signal comes only from *transition-regime* galaxies** (g_N or g_ext within a factor of a few of a₀), sliding relative to the MOND/Newtonian knee as a₀(z) runs. Over a realistic grid (g_N ∈ [0.01,1] a₀, g_ext ∈ [0.05,1.8] a₀):
- **Declining branch (Theory of Gravity):** Δoffset(z=0→4) = **−0.01 to −0.09 dex** (median |0.04|). The suppression **weakens slightly** with z — *opposite in sign* to the published "strengthens +36%," and ~10× smaller. (Reason: declining a₀ pushes galaxies toward Newtonian, where the discrepancy and its suppression both shrink toward zero.)
- **Rising branch (scaling-MOND):** Δoffset(z=0→4) = **+0.03 to +0.30 dex** (median |0.11|). The embedded-vs-isolated gap **widens**, not closes — again *opposite* to that paper's narrative.

**3. Sample size:** for a representative |signal| ≈ 0.045 dex against a per-galaxy scatter 0.25–0.40 dex, a 3σ detection of the offset *change* (two redshift groups) needs **~1,100–2,800 galaxies**, not 600–1,600. The published forecast is optimistic by roughly 2–4×.

## The realization caveat — not a rescue, but where the physics is
The QUMOND result above is for the **modified-gravity** (AeST/QUMOND) realization. The framework's *declared natural home* is **modified inertia** (§4.6), where the EFE is structurally different — it acts on the system's center-of-mass *trajectory*, not on the local field via a nonlinear Poisson equation. A heuristic total-acceleration estimate suggests the MI offset **does not saturate** in deep-MOND (for a deep-MOND galaxy it moves ~−0.055 dex over z=0→4 where the MG offset moves only ~−0.016), because the suppression threshold (the COM MOND acceleration vs a₀(z)) genuinely runs with a₀. **But modified inertia is time-nonlocal and closed-orbits-only; this estimate is not a rigorous solve.** So the EFE-vs-z prediction is **realization-dependent**, and the clean version is an open calculation, not a settled number.

## Consequence (both ways)
- **The headline distinctive test is softer than advertised.** The EFE-vs-z was presented as the one near-term signal separating the framework from both ΛCDM and constant-a₀ MOND. Its magnitude is ~0.03–0.06 dex (MG), its sign was stated backwards for both papers, and the sample is thousands of galaxies. This is a genuine weakening of the empirical case and is now stated as such.
- **But it is not killed.** The offset still *discriminates* (constant-a₀ MOND predicts exactly zero z-change; ΛCDM predicts no embedded-vs-isolated offset structure at all), and the modified-inertia realization may yet give a clean, larger z-signal. What changed is the *mechanism* (transition-regime sliding, not "the EFE turns off") and the *feasibility* (a multi-cycle campaign, not a single program).

## Actions
1. Correct **§11 prediction #12** in `papers/ZIMMERMAN_THEORY_OF_GRAVITY.md` (done) and regenerate the PDF.
2. Re-word the **EFE-strengthens-with-z** item in `data_watch/ROUTINE.md` (done).
3. Publish a **Zenodo v2** of the paper with this correction (Carl, manual).
4. **Open calc (the real follow-up):** a proper numerical QUMOND/AQUAL 2D solve *and* a time-nonlocal modified-inertia treatment of the EFE-vs-z, to pin the signal, its sign, and the realization dependence. This is the calculation that decides whether the framework has a clean near-term distinctive test.

*Verified: `reviews/efe_vs_z_recompute.py` (numpy; deep-MOND saturation analytic + numerical, grid signal, sample-size, MI contrast). The deep-MOND a₀-independence is exact within the 1D estimate; the transition-regime numbers are the right order, pending a 2D field solve (curl corrections ~10–20%, largest where g_ext ≳ g_N).*
