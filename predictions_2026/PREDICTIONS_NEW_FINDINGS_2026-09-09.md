# Testable predictions from the 2026-09-08/09 findings (de Sitter–MOND framework)

Compiled 2026-09-09 from the L74–L80 arc (`fable_independent_2026/FINDINGS.md`) and astra's F(Q)Θ affine
construction (`qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/`). Every entry is stated inside
the framework — a₀ tied to the de Sitter/Λ scale, **a₀ = c²/(2πL_dS)** (verified to ~5% in L78), κ = ½
fitted, MOND carried *inside the clock*, and the surviving distinctive law **a₀ ∝ H(z)**. Each prediction
names its grounding lane, the observable, the discriminator against ΛCDM, and its status (NEW / SHARPENED,
and whether CONTINGENT on the pending scalar-health verdict).

Verification note: these are empirical predictions, verified by committed runnable scripts (the cited
lanes), not by a proof assistant — Lean formalizes theorems, not observations, and would not catch the error
classes this programme actually hits (footing leaks, arithmetic-in-prose). Both a₀ footings
(9.3619e−11 / 1.1279e−10 m s⁻²) apply to every dimensional number.

---

## A. GALAXY SCALE — the clock carries MOND, with no cold component and no slip

**P1 — The RAR is blind to halo assembly history.** Because galaxies are driven entirely by the clock
(MOND), with *no* cold component transmitting into them, the radial-acceleration-relation residual at fixed
baryonic acceleration is **uncorrelated with halo concentration, formation redshift, or environment**.
*Ground:* L76 measured Spearman(concentration, RAR residual) = **+0.012** (N=155, SPARC). *Test:* correlate
RAR residuals against concentration/assembly proxies in larger samples (BIG-SPARC, MaNGA). *Discriminator:*
ΛCDM assembly bias predicts a small but nonzero correlation; the framework predicts **zero** to the
intrinsic scatter (~0.06 dex). **Status: NEW (sharpened into a null by L76).**

**P2 — Lensing and dynamics obey the SAME RAR in isolated galaxies (no slip).** The F(Q)Θ static branch
gives **Φ = Ψ exactly**, so the weak-lensing acceleration equals the dynamical acceleration equals the MOND
prediction — no extra lensing mass. *Ground:* L80 (static-branch Φ=Ψ, verified). *Test:* galaxy–galaxy weak
lensing vs rotation-curve RAR for isolated galaxies. *Discriminator:* any lensing–dynamics mass discrepancy
in an isolated galaxy (beyond the MOND prediction) falsifies it. **Status: SHARPENED (now from an explicit
action).**

**P3 — a₀ rises with redshift as a₀(z) ∝ H(z).** a₀ is the de Sitter scale (P0-level: a₀ = c²/2πL_dS, L78),
so it tracks the Hubble rate. *Test:* high-z BTFR zero-point and RAR scale; the registered Gaia DR4
wide-binary γ_v band. *Discriminator:* deep-MOND BTFR zero-point at z≈2.5 is **flat (0.00 dex)** in the
framework vs **+0.33 dex** in ΛCDM; a robustly *constant* a₀(z) would falsify the framework's core law.
**Status: SHARPENED (a₀–Λ tie now verified to 5%).**

**P4 — The phantom acceleration saturates at a finite ceiling.** The bounded-boost kernel caps the extra
acceleration at **Δ_sat = 0.6476 a₀** (peak phantom acceleration 0.648 a₀ at g_bar = 2.54 a₀). *Test:* the
RAR has a maximum excess; no galaxy exceeds the ceiling at its corresponding g_bar. *Discriminator:* an
unbounded halo contribution would exceed it. **Status: SHARPENED.**

---

## B. CLUSTER SCALE — a separate, collisionless conserved-charge dust

**P5 — Clusters need a separately-gravitating pressureless dust, and it is collisionless.** The complete
theory is "MOND below a galaxy + a distinct dust for clusters" (excess-spent-once, tested L61/L74–L77); in
the F(Q)Θ completion that dust is the clock's **conserved charge** (a⁻³, pressureless). *Test:* merging
clusters (Bullet-type). *Discriminator:* the lensing mass **separates from the gas and traces the
galaxies** — like collisionless CDM, and **unlike pure MOND**, which fails the Bullet offset. **Status: NEW
(mechanism identified L79/L80).**

**P6 — The cluster dark component is NOT a thermal relic in the ~11–28 eV window.** The relic route is a
pincer with no interior, and the clock's own MOND *deepens* galactic wells so phase-space capture rises,
widening the pincer (protection mass 11 eV vs 17 eV Newtonian, vs the 27.6 eV N_eff floor). *Ground:* L77.
*Test:* laboratory/astro searches for a ~10–30 eV thermal relic. *Discriminator:* a positive detection of a
relic in that window would contradict the framework, which puts the cluster dust in the clock's
conserved-charge sector, not a particle. **Status: NEW.**

**P7 — The cluster dark-to-baryon ratio is set by cosmological infall, not internal acceleration.** Since
the dust is absent from galaxy dynamics but present cosmologically, its cluster abundance (~6.9× baryons in
the core region) tracks **cluster mass / assembly / cosmological infall**, not the internal acceleration
scale. *Ground:* L77 (ordering closed), g04a (amplitude 6.9). *Test:* cluster dark-fraction vs mass and
formation time. *Discriminator:* MOND-only predicts the residual scales with internal acceleration; the
framework predicts it scales with cosmological infall. **Status: NEW.**

---

## C. COSMOLOGY — the dust is a conserved charge tied to Λ

**P8 — Dark matter is pressureless dust with c_s² = 0 (CDM-like at background + linear order).** The
conserved-charge dust redshifts as a⁻³ with w = 0. *Ground:* L79/L80 (ρ ⊃ −2M²AC/3f²a³, pressureless).
*Test:* CMB acoustic peaks and BAO. *Discriminator:* this is a **consistency requirement** — the F(Q)Θ dust
must reproduce the CDM-like CMB/BAO fits; a failure of the third-peak/BAO fit would falsify it. Deviations
appear only at nonlinear/small scales (see P11). **Status: NEW — SUPPORTED by L82: the Noether dust is pressureless (c_s²=0) and clusters exactly like CDM at linear sub-horizon order, with standard G_eff; the g04h suppression mode is absent. Caveat: astra's near-horizon k→0 strong coupling bears on the lowest CMB multipoles.**

**P9 — Dark energy is a pure cosmological constant, w_DE = −1 exactly, tied to a₀.** The a₀ sector is the
w = −1 Λ scale (L78), not a separate quintessence field; a₀ and the dark-energy scale are the *same* scale.
*Test:* w_DE(z) from DESI/Euclid. *Discriminator:* the framework forbids evolving dark energy — a robust
w_DE ≠ −1 (dynamical DE) would break the a₀–Λ identity. **Status: NEW (from the a₀–Λ verification).**

**P10 — A bounded stiff early-time component (w = 1) from the charge term.** The eliminated density carries
a separate **C²/a⁶ (stiff, w=1)** piece alongside the a⁻³ dust. *Ground:* L80 (astra's REPORT: "the C²/a⁶
term is a separate stiff correction"). *Test:* early-expansion / BBN / N_eff bounds. *Discriminator:* the
framework predicts a *small, bounded* stiff contribution decaying faster than radiation — an upper bound on
its amplitude that BBN can test; a large stiff component is excluded. **Status: NEW (quantitative bound
requires astra's coefficient calibration).**

**P11 — Small-scale structure carries a MOND imprint, not a pure-CDM one.** CONTINGENT on the scalar-health
verdict: if the F(Q)Θ scalar is a non-propagating cuscuton, growth matches CDM at large scales while
galaxy-scale dynamics are MOND-enhanced. *Test:* satellite counts, Lyman-α, small-scale P(k). *Ground:*
L78/L80/L82. **Status: SUPPORTED at linear order — L82 shows linear cosmology is standard gravity + pressureless dust (CDM-like large scales) while galaxies are MOND, both from the one cubic operator; the MOND imprint is a nonlinear/small-scale effect. Near-horizon k→0 remains astra's open item.**

---

## D. GRAVITATIONAL WAVES — standard tensor sector, scalar polarization pending

**P12 — GW speed equals c exactly, with no dispersion.** The tensor sector is standard Einstein–Hilbert
(M²/2 R), so c_T = c. *Ground:* L80 (the action's gravitational term). *Test:* multi-messenger GW timing
(GW170817-type). *Discriminator:* any measured c_T ≠ c falsifies it. **Status: SHARPENED (now from the
explicit F(Q)Θ action).**

**P13 — No scalar (breathing) GW polarization.** CONTINGENT: if the affine degeneracy makes the scalar a
non-propagating cuscuton, there is **no extra scalar polarization** in gravitational waves. *Ground:* the
det W = 0 degeneracy (L80) + the pending DOF count. *Test:* polarization content in GW networks
(LISA/ET/pulsar timing). *Discriminator:* detection of a scalar mode would falsify the cuscuton structure
(and would mean a propagating scalar whose c² = −1 warning becomes a real problem). **Status: CONTINGENT.**

---

## E. LOCAL / SOLAR SYSTEM

**P14 — γ_PPN = 1, Cassini-consistent, no fifth force.** The clock's MOND has no unscreened long-range
scalar force in the Solar System. *Ground:* framework (screened scalar, no-slip) + L80 (Φ=Ψ). *Test:*
Cassini, LLR. *Status: STANDING, reinforced.**

**P15 — Wide-binary a₀-scale deviation (registered).** The framework predicts a specific γ_v at kAU
separations, registered and hash-frozen for Gaia DR4 (Amendment 11/12; a₀ ∝ H(z) footing). *Test:* Gaia DR4
wide binaries. *Discriminator:* Newtonian γ_v = 1.00 vs the framework's registered band. **Status: STANDING
(frozen preregistration).**

**P16 — Dark matter cannot decay or annihilate.** The dust is the conserved Noether charge of the
clock-scalar's shift symmetry (L81), so it is exactly stable. *Test:* indirect-detection searches (decay
lines, annihilation excesses). *Discriminator:* the framework predicts **no** DM decay or annihilation
signal, unlike a WIMP/particle relic — a confirmed detection of either would falsify it. **Status: NEW.**

---

## The single open item these predictions hinge on

P11 and P13 are **contingent** on one calculation: whether the F(Q)Θ affine scalar is a non-propagating
cuscuton (healthy, the c² = −1 decoupling value unphysical) or a genuine propagating mode (then c² = −1 is a
real gradient instability and the completion fails at that witness). The MOND term is cubic and drops from
the quadratic FLRW action, so this reduces to a pure cuscuton K(Q)+F(Q)Θ+EH degree-of-freedom count. That
is astra's live deciding calculation; the fable side has verified everything up to it (L80) and reduced it
to the cuscuton DOF question.
