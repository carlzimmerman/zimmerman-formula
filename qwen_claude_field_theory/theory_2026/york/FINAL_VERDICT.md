# FINAL VERDICT — CMC-gauge MOND-deformed GR (Task H)

Grader: harsh. Rule applied: **a gate the adversary breached is NOT a PASS.**
Machine evidence: every row below is backed by a committed, runnable script in
`theory_2026/york/` (filenames given). Three referee scripts re-run clean at grading time:
`referee_gateE_doublecount_2026.py` (9/9), `referee_gateF_2026.py`, `referee_gates_BC_robustness_2026.py`.

---

## (1) GATE TABLE

| Task | Verdict | One-line reason |
|------|---------|-----------------|
| A — reduced CMC-gauge GR + elliptic-MOND action | **PASS** | ADM reduction machine-verified; MOND term ultralocal in h_ij, K_ij-free; not attacked. |
| B — modified Lichnerowicz-York + CMC lapse | **CONDITIONAL** | Ellipticity is real (principal symbol −8D̄²; V_MOND=a0²(YU'−U)≥0 ⇒ lapse well-posed), and weak-field is locally unique; but the "unique positive solution guaranteed" wording is **over-stated for the isolated strong-field solve** — the MOND phantom's ψ-weight is fixed by Y=ψ⁻⁴ȳ and cannot be York-reweighted, m(y)=5U−4yU' flips sign at g/a0=1.434, and the only guaranteed stabiliser (10/3)q²ψ⁴→0 as q→0. Inherits GR-matter non-uniqueness (BÓMP folds), no worse, no better. `referee_gates_BC_robustness_2026.py`. |
| C — DOF = 2 (Φ second-class, H_perp algebra closes) | **PASS** | Adversary attack 2 fully repelled; principal symbol √y(y+2)/(1+y)^{3/2}>0; Dirac-DeWitt algebra closes because MOND density is ultralocal. `dof_deformed_cmc_2026.py`. |
| D — cosmology / a0(z) | **PASS** | Y=0 ⇒ U=0 ⇒ homogeneous MOND stress = 0 (all 16 components); pure-GR Friedmann, no Λ_eff; K=q=3H; **a0(z)/a0,0 = H(z)/H0 derived, Z-independent.** `cosmology_flrw_2026.py`. |
| E — weak-field / S_source (double-counting check) | **FAIL** | Adversary breached: the two channels carry a **bare 4πGρ each** and the test mass falls in Ξ=Φ_g+φ, so in the Newtonian regime (μ→1) g=g_N+g_N ⇒ **G_eff = 2G, solar-system gravity doubled.** The disformal choice fixes light-bending, not the doubled scalar+metric source. `referee_gateE_doublecount_2026.py` (9/9). |
| F — PPN / lensing / Cassini | **FAIL** | Adversary breached on two legs: (i) γ_PPN=1 is an **engineered disformal input** — a conformal shift leaves the slip D=Φ_g−Ψ_g invariant, so no free φ(Φ) sets γ=1; lensing=dynamics is imported (TeVeS/AeST), not derived; (ii) **Cassini Q2 = 19–21e-27 s⁻² for the theory's own μ=x/√(1+x²) ⇒ 3.9–6.0σ** over the (3±3)e-27 bound (8.3–11.2σ for the RAR/MS08 kernel). a0(q) spatially constant ⇒ **no DHF Case-B environmental escape.** `referee_gateF_2026.py`, `ppn_lensing_cassini_2026.py`. |
| G — global consistency / stability | **PASS** | c_T²=1 exactly; tensor kinetic +1/2 (no ghost), gradient −1/2 (no gradient instability); MOND term K_ij-free ⇒ cannot alter c_T; Φ non-propagating (ellipticity replaces ghost test); a0→0, q→0, Minkowski, FLRW all regular; U'' singularity at Y→0 harmless. `stability_taskG_2026.py`. **Scope caveat:** G tested the gravity+Φ sector; it did NOT test the matter coupling S_source that fails in E. |

---

## (2) OUTCOME

### OUTCOME 2 — GATE(S) FAIL.

**This theory is NOT complete.** LY-ellipticity (B), MOND-equation, 2-DOF (C), and stability (G)
pass, but **the weak-field MOND-force gate (E) and the PPN/lensing/Cassini gate (F) both fail.**
Per the grading rule ("do not call it complete unless … PPN/lensing gate is explicitly passed"),
the theory cannot be graded complete.

### Failing equations

**E — the doubling pair.** With
```
∇²Φ_g = 4πG ρ + a0²(Y U' − U)          [metric time potential]
∇·[μ(x) ∇φ] = 4πG ρ                     [imported scalar, sec14 Eq.14.3]
force on test mass = −∇Ξ,  Ξ = Φ_g + φ
```
in the Newtonian regime μ(x)→1 so **φ→full Newtonian potential** and Φ_g's bare 4πGρ term
**also** gives g_N ⇒ g_tot = 2 g_N. The additive two-potential bookkeeping is inconsistent
with its own imported single-field equation (which needs φ→0, not φ→Φ_N, at g≫a0).

**F — the frozen interpolation object.** The action's
```
U(Y) = √(Y(1+Y)) − arcsinh(√Y),   U'(Y)=μ(√Y),   μ(x)=x/√(1+x²)
```
gives an EFE quadrupole Q2 = (3/2) q(η) a0^{1.5}/√(GM) ≈ 19–21e-27 s⁻² at Saturn, i.e.
3.9–6.0σ over Cassini. The isotropic 1−μ=(a0/g)²/2 term (which Task F priced and passed) is
**not** what Cassini bounds; the anisotropic-stress quadrupole is, and it is the SAME object as
the lensing slip.

### MINIMUM modification to the action (no new named theory)

Two independent structural repairs are required; **neither is a wording change.**

1. **Single-channel matter coupling (fixes E).** S_source must couple matter to **one** physical
   metric whose weak-field potential solves a **single** AQUAL equation
   `∇·[μ(|∇Φ|/a0) ∇Φ] = 4πG ρ`, with the **same Φ** entering the LY/lapse source — not a GR
   metric potential Φ_g **plus** an independent scalar φ each sourced by a bare 4πGρ. Concretely,
   the disformal potential must satisfy **φ(Φ) ∝ (Φ − Φ_N), so φ→0 (not φ→Φ_N) as g≫a0**, i.e.
   the scalar carries only the phantom EXCESS ρ_ph = (1/4πG)∇·[(μ−1)∇Φ]. This is a **derivation
   owed from S_m[g̃]**, not a free adoption.

2. **Cassini-safe interpolation (fixes F's Cassini leg).** Because a0(q) is spatially constant,
   the theory has no environmental escape, so the fixed μ=x/√(1+x²) tension is honest and fatal.
   The minimal change is to **replace U(Y)** by a member of the exponential-approach family whose
   μ'(x) is suppressed faster than x⁻³ at large x (the ν=1/(1−e^{−√y}) kernel already adopted
   elsewhere in the program is the natural candidate) so that Q2 falls below (3±3)e-27 s⁻². This
   is a change to U in the action, not a fit.
   Even after (1)+(2), **γ_PPN=1 remains an INPUT** (the disformal n·n retuning is a choice); a
   genuine derivation must force the disformal structure uniquely from the matter–Φ coupling.

### Gates that must be RE-RUN after the fix

- **E** — re-derive the weak-field force from the single-channel S_source; confirm one Newton, one MOND, no cross term.
- **F** — recompute γ_PPN and the Cassini Q2 for the replacement U(Y).
- **G** — re-check a0→0, deep-MOND, principal-symbol U'+2YU''>0, and stability for the new U.
- **B** — re-verify LY/lapse ellipticity for the new U (V_MOND≥0).
- **D** — trivially survives (uses only U(0)=0), but re-assert for the new U.

---

## (3) FROZEN ACTION — **WITHHELD**

Item (3) is delivered **if and only if everything structural passes.** It does not.
**The action is NOT frozen.** Blocking items: E (G_eff=2G doubling) and F (Cassini 3.9–6.0σ +
engineered γ). The candidate action below is recorded for reference only, explicitly **NOT
ratified**, with the S_source line marked as the unresolved object:

```
S = (c³/16πG) ∫dt d³x N√h (K_ij K^ij − K² + R³)
  − (1/8πG) ∫dt d³x N√h a0(q)² U(Y)  +  S_source            ← S_source UNRESOLVED (Gate E)
  Y = D_iΦ D^iΦ / a0(q)²,   U(Y) = √(Y(1+Y)) − arcsinh(√Y)   ← U FAILS Cassini (Gate F)
  U'(Y)=μ(√Y),  μ(x)=x/√(1+x²)
  K = q(t) global CMC clock;  a0(q)=c q/Z spatially constant;  q_FLRW=3H;  a0(z)=a0,0 H(z)/H0.
  Φ elliptic auxiliary (no time derivative).
```

### Honest open items (independent of the two failures)
- **Z is FITTED (~21).** Only the proportionality **a0(z) ∝ H(z)** is predicted; the normalization is not. The factor 3 in a0=3cH/Z vs the "cH_Λ/Z" shorthand is absorbed into Z.
- **Disformal lensing fix is an INPUT, not a derivation.** γ_PPN=1 is engineered via the disformal n·n term (TeVeS/AeST mechanism); the bare gravity action gives γ_PPN=log r/(log r−2)≠1 and under-lenses.
- **Cassini residual: 3.9–6.0σ (theory's own μ), 8.3–11.2σ (RAR/MS08 kernel).** A live falsification, not a soft tension. No environmental escape (a0 spatially constant).
- **LY isolated-system uniqueness caveat: real.** Weak-field well-posed and locally unique; strong-field global uniqueness conditional, no worse than GR-with-un-reweighted-matter.

---

## (4) FALSIFIABLE PREDICTIONS (recorded even though the theory fails structurally)

1. **a0(z) = a0,0 · H(z)/H0** — DERIVED, Z-independent (Gate D). Distinguishes this construction from constant-a0 MOND and from ΛCDM. **Falsifier:** any robust measurement of a0 evolution departing from H(z)/H0 (e.g. a rise or a flat history below z~5) kills it. This is the theory's one clean, load-bearing prediction.

2. **Standard-μ Solar-System signature** — μ=x/√(1+x²) gives an internal isotropic anomaly 1−μ=(a0/g)²/2 ⇒ dg ≈ 1.1e-16 m/s² at Saturn (below Cassini sensitivity ~1e-14), BUT an EFE quadrupole **Q2 ≈ 19–21e-27 s⁻² that EXCEEDS Cassini (3±3)e-27 by 3.9–6.0σ.** This is a falsification-grade prediction that **currently fires AGAINST the theory** (Gate F). It is the sharpest discriminator and the reason F fails.

3. **Lensing = dynamics** — status: **CONDITIONAL / MODEL INPUT.** Predicted only if the disformal coupling is adopted; the gravity action alone predicts γ_PPN=log r/(log r−2)≠1 (under-lensing). Not a derived prediction until S_source is shown to force the disformal structure uniquely.

---

### Bottom line
Structural core (A, C, D, G pass; B ellipticity passes with a uniqueness caveat) is sound, but
**the theory as written fails at the matter coupling (E: G_eff=2G) and at the Solar System
(F: Cassini 3.9–6.0σ).** OUTCOME 2. Not complete. The two named fixes above (single-channel
S_source; Cassini-safe replacement for U) are the minimum, and E/F/G/B/D must be re-run after.
