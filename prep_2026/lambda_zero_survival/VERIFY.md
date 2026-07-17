# VERIFY — Λ→0 Survival of the de Sitter-Unruh Modified-Inertia Framework

**Workflow:** does the framework survive Subir Sarkar's "dark energy may not be real" (Colin-Mohayaee-Rameez-Sarkar 2019, A&A 631 L13, arXiv:1808.04597: isotropic monopole deceleration q_m only ~1.4σ from zero; the robust signal is the bulk-flow dipole q_d)?

**Script:** `lambda_survival.py` — re-run **exit 0**, all 4 machine checks OK. Both footings carried throughout (canonical cH_Λ/Z=9.36e-11; ALT cH0/Z=1.13e-10 Planck / 1.18e-10 at H0=70).

---

## (1) THE CRUX — is the Cai-Kim apparent-horizon temperature a legitimate a0 basis at Λ=0? — resolved honestly

**Answer: it delivers the a0 VALUE but NOT the distinctive DERIVATION. In a decelerating (Λ=0) universe it is a horizon-thermodynamics bookkeeping temperature, not the real Gibbons-Hawking bath modified inertia requires. Using it = POSTULATING a0=cH0/Z by formal analogy.**

Literature grounding, both ways:
- **In favor (real, acknowledged):** Cai-Kim 2005 (hep-th/0501055) + Padmanabhan "thermodynamics of spacetime" is a genuine structural result — the first law dE=TdS+WdV at the apparent horizon r_A=c/H, with T=ħH/2π and S=A/4, reproduces the Friedmann equations for *arbitrary* FLRW (matter/radiation included). This is more than loose analogy; the *value* cH/Z is not manufactured.
- **Against a DERIVATION in a decelerating universe (why it degrades to a postulate):**
  1. The apparent horizon in a decelerating FLRW is **not a causal event horizon** — signals cross it. The Gibbons-Hawking construction (Euclidean periodicity / Wightman analyticity across a true horizon, static patch, global timelike Killing vector) does **not** apply.
  2. A comoving Unruh-DeWitt detector registers an exactly thermal spectrum at T=H/2π **only in de Sitter**; in general FLRW the response is time-dependent and non-thermal. T=H/2π is the surface-gravity/bookkeeping temperature, not a demonstrated detectable bath.
  3. The dynamical (Kodama-Hayward) apparent-horizon surface gravity carries a correction κ=−(1/r_A)(1−ṙ_A/2Hr_A); T=H/2π is exact only quasi-statically (de Sitter). Even the value is de-Sitter-clean / FLRW-corrected.
  4. Holographic-DE precedent (Hsu 2004; Li 2004, hep-th/0403127): the Hubble/apparent horizon as IR cutoff gives the **wrong** equation of state (w=0, no acceleration); the fix is the future **event** horizon (needs Λ>0). The apparent-horizon IR scale is the *weaker* horizon reading — the repo's own `THE_EVENT_HORIZON_DOOR.md` already records this.

**Adversarial steelman tested and rejected:** Jacobson 1995 gets Einstein's equations from δQ=TdS on *local Rindler* horizons, whose Unruh bath T=ħa/2πc is real and Λ-free. But the pure Unruh temperature is ∝a with **no fixed acceleration scale** — it yields no a0. The scale a0 appears only in the quadrature T=√(a²+a_c²), and the cosmological floor a_c=cH must be a *real* bath to set the scale. The scale-setting bath is the cosmological-horizon bath, a real Gibbons-Hawking bath only for a true event horizon (Λ>0). So the Unruh half is Λ-free but scale-free; the scale derivation needs Λ>0. The kill is of the derivation-of-the-scale, not manufactured; the value is never killed.

## (2) The Λ>0-requiring step, re-derived independently

Chain: (1) Λ>0 ⇒ future de Sitter event horizon; (2) Gibbons-Hawking bath T_dS=ħH_Λ/2π, H_Λ=c√(Λ/3); (3) accelerated body sees Deser-Levin quadrature T(a)=(ħ/2πc)√(a²+a_Λ²), a_Λ=cH_Λ; (4) inertia ∝ ΔT=T(a)−T(0), deep-MOND ΔT≈a²/2a_Λ ⇒ √-law, scale a0=a_Λ/Z=c²√(Λ/32π). **Load-bearing step = 1–2: a real GH bath needs a true event horizon (Λ>0).** As Λ→0: H_Λ→0, T_dS→0, a_Λ→0, canonical a0=c√(Λ/3)/Z→0. Λ=0 exactly ⇒ predicted a0=0 vs measured ~1.2e-10 = **hard falsification of the canonical mechanism**, not a graceful limit. Verified identity a0=c²√(Λ/32π)≡cH_Λ/Z=9.36e-11 (machine check [1] OK).

## (3) Empirical exposure arithmetic (independently checked)

a0_canonical(Ω_L)=(cH0/Z)·√(Ω_L), cH0/Z=1.131e-10 (Planck). Ω_L=0.685→9.36e-11 (0.78× central 1.2e-10 — the long-known ~22% "a0 low" O(1)-coefficient gap, non-diagnostic per memory). Steep √Ω_L exposure: Ω_L=0.30→6.2e-11 (0.52×), factor-2 cut (0.34)→6.6e-11 (~55% of central, clearly inconsistent), Ω_L→0→0. ALT (cH0/Z) is flat, Λ-independent, ~measured. All arithmetic reproduced.

## (4) Value-vs-derivation distinction — kept clean

- **a0 VALUE:** survives Λ→0 numerically via ALT cH0/Z ≈ 1.1–1.2e-10 ≈ measured. Never in question.
- **a0 DERIVATION** (the distinctive "derived from the vacuum" claim): does **not** survive. The event-horizon Gibbons-Hawking route and the CKN cosmic-seesaw route (which welds a0 to ρ_Λ via 4/Z²=3/8π) are **both** Λ-fueled — the CKN route dies too at Λ=0 (no ρ_Λ to seesaw against). The apparent-horizon fallback yields the value only as a postulate.

## (5) Sarkar's actual claim handled (not a strawman)

Not "Λ=0 exactly" — q_m ~1.4σ from zero ⇒ Ω_L poorly bounded away from 0; a *range* [0, 0.685]. Part (C) plots the whole range. The framework's canonical exposure is steep across it; the ALT flat line survives numerically regardless (but only as a postulate).

---

## VERDICT

**SURVIVES-AS-POSTULATE, NOT SURVIVES-AS-DERIVATION.**

- derivation = Λ>0-dependent (true dS event horizon + Gibbons-Hawking bath, steps 1–2); canonical a0→0 as Λ→0.
- survival = value survives (ALT cH0/Z); derivation does not (apparent-horizon route is a postulate/formal analogy in a decelerating universe, not a real GH bath).
- exposure = a0_canon=(cH0/Z)√Ω_L; ~22% below central already at 0.685; falsified as Ω_L→0; ALT flat.

**Both traps avoided:** no manufactured Hubble-horizon save (the derivation genuinely degrades — Cai-Kim is bookkeeping, not a bath, in a decelerating universe); no manufactured kill (the value survives; the Cai-Kim structural result is acknowledged as real, and the CKN route is honestly flagged as dying alongside).

### Honest one-liner for Carl re Sarkar
"If Sarkar is right and Λ is ~0, my a0 *number* still lands (cH0/Z ≈ 1.2e-10, matching data), but my distinctive claim — a0 *derived* from the de Sitter vacuum — is gone: with no future event horizon there's no Gibbons-Hawking bath, only the Cai-Kim apparent-horizon temperature, which in a decelerating universe is thermodynamic bookkeeping, not a real bath a body can feel. So I'd revert to standard MOND with a vacuum-*motivated* but *postulated* scale — that's a real cost, not a save. It's a graceful degradation of the value, a genuine loss of the derivation, and the CKN Λ-seesaw route dies with it. The whole distinctive edge is hostage to Λ actually being nonzero (same hostage as the a0(z)/DESI front)."
