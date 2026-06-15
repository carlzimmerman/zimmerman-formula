# Route 2 — FOOTING AUDIT: are the lensing-"DM proof" measurements using a local/canonical a0? (Opus 4.8, 2026-06-15)

Framework a0 = c² √(Λ/32π) = (c/2)√(G ρ_DE) = **9.3547e-11 m/s²** (pure dark energy), verified to the identity
to 7 figs (`/tmp/footing_verify.py`: c²√(Λ/32π)=9.3547e-11 = (c/2)√(Gρ_DE)=9.3547e-11, ratio 1.000000).
Framework interpolation = dS-Unruh g_obs=√(g_bar²+g_bar·a0), ν(y)=√(1+1/y). Wrong footings watched for:
1.2e-10 (canonical/local McGaugh, framework is −22.0%), 1.13e-10 (ρ_total/cH0), simple-mu, McGaugh-ν.
Carl's specific ask: make sure the lensing-DM measurements are NOT using a local/canonical a0. Both ways.

---

## THE LOAD-BEARING REFRAME (Q1, verified from the AeST field equations)

**In AeST weak field the lensing potential equals the dynamical potential: Φ = Ψ.** Confirmed from the literature
(Skordis & Zlosnik 2021; Verwayen/Skordis/Boehm 2024 MNRAS 531 272 quasistatic solutions): "the two standard
weak-field metric potentials Φ and Ψ are equal, which ensures that the lensing mass is equal to the dynamical mass."
The scalar field sources BOTH potentials equally, so the deflection of light is enhanced by the SAME MOND factor as
the dynamics — this is exactly what relativistic MOND (TeVeS, AeST) is CONSTRUCTED to do, and is the property that
fixed original non-relativistic MOND's under-lensing.

**CONSEQUENCE (the load-bearing footing point): cluster LENSING mass = cluster DYNAMICAL mass in the framework.**
Therefore "lensing proves DM" does NOT add an independent DM proof beyond the cluster dynamical residual. It REDUCES
to the known cluster problem (η(R500)~2.1–2.3). This is confirmed empirically by Mistele, McGaugh & Hossenfelder
(2023, A&A 676 A100, arXiv:2301.03499): they confront AeST's OWN relativistic lensing against KiDS weak-lensing at
small accelerations — AeST predicts only SMALL deviations from the MOND lensing amplitude and "the data show no clear
indication of these predicted deviations," AND to explain the CLUSTER residual in AeST they need m²/fG ≈ 1 Mpc⁻²
"when requiring that the minimum acceleration matches where observed clusters deviate from MOND" — i.e. the lensing
residual and the dynamical residual are the SAME residual at the SAME scale. **Lensing does not double-count.**

---

## THE FOOTING TABLE — what a0 each "lensing-DM" measurement actually uses

| measurement | a0 in the MEASUREMENT | a0 in the framework COMPARISON | footing verdict |
|---|---|---|---|
| **Cluster WL masses** (Bulbul+2024 eRASS1; DES-Y3 2402.08455; HSC 2503.09952) | **NONE — pure GR**, NFW κ/γ→ΔΣ→M (no a0 anywhere) | framework needs its OWN AeST relativistic lensing @ 9.36e-11 | (i) CLEAN measurement; comparison must use 9.36e-11 |
| **Brouwer+2021 GGL RAR** (KiDS, banked) | **NONE — g_obs=4·G·ΔΣ** (SIS/GR, no a0); g_bar from baryons (no a0) | banked door1 table used **1.2e-10** (mild FALSE-WIN); ultra/VERIFY use 9.36e-11 (correct) | (ii) measurement a0-free; one cosmetic over-footing, retracted |
| **Morphology split** (early−late, 8.8σ) | **NONE — data−data at fixed g_bar; a0+ν cancel exactly** | n/a (a0-independent by construction) | (iii) a0-INDEPENDENT — verified, offset does NOT move with a0 |
| **Bullet/JWST lensing** (Famaey 2026; Rihtarsic 2026; TeVeS Angus+08) | **GR convergence map**, no a0 | collisionless residual read via AeST Φ=Ψ lensing | conceded loss, GR-mass footing, no local-a0 inflation |

### (i) Cluster lensing masses — GR+DM, NO a0 (the "DM needed" is the GR-deduced mass)
The eRASS1/DES-Y3/HSC WL masses (Bulbul+2024; arXiv:2402.08455; 2503.09952) are reconstructed by fitting NFW
convergence/shear profiles in **General Relativity** — there is no a0, no MOND interpolation, in the mass pipeline.
So "clusters need dark matter from lensing" means **the GR-deduced enclosed mass exceeds the baryons** — it is NOT a
statement at any a0. The correct comparison is the framework's OWN AeST relativistic lensing at a0=9.36e-11 (which,
because Φ=Ψ, predicts a boost identical to the dynamical MOND boost). The banked eRASS1 η audit does exactly this:
`clusters_eta_audit.py` and `clusters_framework_a0.py` both set A0_FRAME=(c/2)√(Gρ_DE)=9.36e-11 — the framework's
own a0 — and find η(R500)≈2.15 (simple-ν)/2.33 (dS-Unruh). **The deficit is computed against the framework's own
relativistic-lensing-equivalent boost, NOT against a normal-MOND prediction at the wrong a0.**

**Footing-robustness on a0 (verified):** because deep-MOND η ∝ 1/√a0, the framework's LOW a0=9.36e-11 gives the
LARGEST η. Recomputed: η relative to framework = 1.000 (9.36e-11), 0.910 (1.13e-10), **0.883 (1.2e-10)**. Canonical
1.2e-10 would LOWER η ~13%. **So the cluster lensing deficit is NOT inflated by a local/canonical a0 — it is
computed at the framework's OWN least-favorable a0.** (The one banked false-WIN here is the opposite: `door6` and
paper scorecard row 17 reported η=1.92 at the canonical 1.2e-10 — UNDER-stating the framework's own liability by
~12%; corrected to ~2.15–2.33. Anti-framework correction, already banked.)

### (ii) Brouwer GGL RAR — measurement is a0-free; one cosmetic over-footing (FALSE-WIN), retracted
The Brouwer ESD→g_obs conversion is **g_obs = 4·G·ΔΣ_obs** (SIS, Eq. 3–7), pure GR — no a0. g_bar = G·M_bary/r²,
no a0. So the RAR data points themselves are a0-free. The framework comparison:
- `door1_gravitational_lensing.py` displayed the boost table at **a0=1.2e-10 + simple-mu** (mislabeled "framework")
  → this makes the curve land exactly on Brouwer's OWN adopted a0 (near-circular, tighter-looking pass) = mild
  **FALSE-WIN**. Re-footed at 9.36e-11 + dS-Unruh ν: deep-MOND g_obs is **−0.054 dex (−11.7%) LOWER** (verified:
  √(9.36/12.0)=0.883). The pass SURVIVES — it sits ~0.054 dex low, inside Brouwer's ~0.1–0.2 dex scatter — but it is
  a SOFTER pass. **Retract the polished wording; the valid pass stays.** (Anti-framework.)
- `door1_lensing_ultra.py` + `VERIFY_lensing_adversarial.py` already use 9.36e-11 as the central a0 (gold-standard
  footing); 1.2e-10/9.1e-11 appear only as the two EDGES of a stated ν-systematic band. CLEAN.

### (iii) Morphology split — a0-INDEPENDENT, the offset does NOT move with a0 (verified)
The split is χ²(early−late g_obs at matched g_bar), with g_obs=4·G·ΔΣ_t from Brouwer's released KiDS profiles.
**No a0, no ν anywhere** in lr_battery/agentH/agentZ/agentK/esd_conversion (grep-confirmed: zero a0 literal). It
CANNOT be an a0/ν artifact: any model line g_bar·ν(g_bar/a0) is IDENTICAL for both types at matched g_bar, so it
cancels EXACTLY in the difference (verified for simple, dS-Unruh, McGaugh — all three give the same model line, all
cancel). Re-run reproduces χ²=119.9/15 → 8.8σ, 15/15 bins early-above-late, +0.261 dex. **The +0.26 dex offset is
literally invariant under any a0 — it does not move. The split is footing-robust and CONFIRMED as a real standing
loss.** (If it HAD been an a0 artifact, correcting it would have ERASED the framework's #1 loss — it is not, so the
loss stays. Both-ways: no manufactured escape.)

### (iv) Any literature MOND-lensing comparison using simple-mu/1.2e-10 mislabeled "framework"?
- The foundational cluster-MOND lit (Sanders 99/03; Angus-Famaey-Buote 08; Eckert/Famaey 24; Famaey-McGaugh 12)
  ALL use canonical 1.2e-10 — the η-FAVORABLE (lower-deficit) end. None mixed in the framework's 9.36e-11. So the
  LITERATURE residual (~factor 2) is computed at a HIGHER a0 than the framework's; on the framework's own footing the
  literature ~2× becomes ~2.15–2.33 (slightly WORSE). **No literature comparison made the framework look worse via a
  WRONG-LOW a0 — if anything the published numbers are mild under-statements of the framework's own liability.**
- The AeST lensing confrontation (Mistele-McGaugh-Hossenfelder 2023) uses the AeST relativistic lensing directly
  (a0≈1.2e-10 class, the standard MOND scale) — correct relativistic footing, and finds AeST lensing ≈ MOND lensing
  ≈ data (no clear deviation). This is the framework's OWN relativistic lensing PASSING the KiDS weak-lensing test.

---

## NET — both ways

**No "DM-proof" lensing measurement uses a local/canonical a0 that inflates a framework loss.** Carl's specific
worry is clean:
1. **Cluster lensing masses are GR+DM (NO a0)** — the "DM needed" is the GR-deduced mass. The framework comparison
   uses its OWN a0=9.36e-11 via AeST's Φ=Ψ relativistic lensing (= the dynamical boost), and that is the
   LEAST-favorable a0 (canonical 1.2e-10 would LOWER η ~13%). The cluster deficit is footing-robust on a0, NOT
   inflated. The only a0 footing error found is the opposite direction (door6/scorecard η=1.92 at 1.2e-10 UNDER-states
   it; corrected to ~2.15–2.33).
2. **Brouwer GGL RAR data are a0-free** (g_obs=4GΔΣ); the framework comparison should use 9.36e-11+dS-Unruh, where it
   passes ~0.054 dex low (soft pass). The banked door1 table's 1.2e-10+simple-mu was a mild cosmetic FALSE-WIN —
   retracted; the pass survives.
3. **The morphology split is a0-INDEPENDENT** — the +0.26 dex offset does not move with a0 (model line cancels in
   early−late). It is footing-robust and CONFIRMED as the real #1 standing loss. The eROSITA-CGM escape closure
   stands (a0 has nothing to do with it).

**The deep reframe (Q1) holds and is the most important footing result:** because AeST ties lensing to dynamics
(Φ=Ψ), cluster lensing mass = cluster dynamical mass, so **"lensing proves DM" REDUCES to the cluster dynamical
residual — it is NOT a second, independent DM proof.** The Bullet/cluster lensing residual is the SAME imported
residual as the cluster dynamics and the CMB — conceded once, not twice.

Both ways, honestly: (a) NO false-deficit from a wrong-low a0 on any lensing front (Carl's worry does not bite —
the cluster numbers are at the framework's worst-case a0 and the data are a0-free); (b) the morphology split is
footing-robust and stays a real loss (NO manufactured escape); (c) two mild FALSE-WINS to retract (door1 RAR table
1.2e-10+simple-mu; door6/scorecard η=1.92 at 1.2e-10) — both ANTI-framework corrections; (d) the genuine resolution
is the REFRAME — lensing is not an independent DM proof in AeST, it reduces to the cluster problem. Quarantine held:
a0/Z never asserted derived.
