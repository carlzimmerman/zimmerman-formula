# Ghost-condensate EFT VALIDITY + consistency window for the framework's dark sector — verdict 2026-06-19

**Topic:** `eft_validity_window`. **CRUX:** does the ghost-condensate (GC) EFT that houses
the framework's dark sector (AeST K(Q)=μ²(Q−1)², banked GHOST_CONDENSATE_2026-06-19) stay
VALID and CONSISTENT across the scales the framework uses it (cosmology k~H₀, galaxies
kpc–Mpc, solar system)? Three sub-questions from ACLM (Arkani-Hamed–Cheng–Luty–Mukohyama,
hep-th/0312099) Sec 4–8, pulled verbatim this session (PDF → pdfplumber, `/tmp/aclm.txt`):
(a) strong-coupling cutoff Λ_strong; (b) antigravity/oscillating-force scale; (c) the
dark-matter-vs-dark-energy seesaw tension; plus (d) the k⁴ dispersion → a P(k) feature?

**HEADLINE (both ways): COMFORTABLE validity window — no observable EFT breakdown, no
intruding antigravity, the seesaw tension is DODGED by the framework's additive-Λ split —
but the one place the GC could give a NEW distinctive signal (the k⁴ feature at k~μ) is
DEGENERATE with the free clustering scale μ and already absorbed into AeST's CMB/P(k) fit.
So: validity = GOOD (credited at full weight); a new falsifiable front = NO, not at full
weight (the candidate signal collapses onto a free parameter). Quarantine held; no
manufactured win, no reflexive dismissal.**

Code (this dir, both exit 0): `eft_validity_window_calc.py`, `dS_window_check.py`.
Framework M window (from banked `seesaw_two_scales.py`): the CLUSTERING-length scale the
field is actually used at is **M ~ 0.04–1 eV** (sets μ via the ACLM graviton mass
m=M²/√2 M_Pl = AeST's μ; mu⁻¹ ≳ 1 Mpc ⇔ M ≲ 0.15 eV). The energy-density seesaw scale
M~0.1 GeV is NOT used (Λ is a separate additive constant; see (c)).

---

## (a) Strong-coupling / EFT cutoff Λ_strong — VALID everywhere the framework uses it

**ACLM verbatim (Sec 4, /tmp/aclm.txt line 786):** *"if we work with a UV cutoff Λ that is
somewhat smaller than the scales M, M̄, then the strongest dimensionless coupling strength
in the theory is set by powers of λ = Λ/M."* The cutoff is **Λ_strong ≲ M** — the SSB scale
itself, NOT a boosted (M³M_Pl)^¼ or anything larger. The crucial ACLM result (Eq 4.7,
scaling dims Eqs 4.3–4.6): the leading π self-interaction M⁴π̇(∇π)² is **IRRELEVANT**
(scales as s^(1/4), "just barely!") → the IR EFT is **controlled down to arbitrarily low
energy**; the only danger is on the UV side at ≳ M. ACLM's own window: **10⁻³ eV < M < 10
MeV** (line 806).

The framework uses the GC at energies/momenta DEEP in the IR (calc, M=0.15 eV reference):
| regime | char. energy | E/M |
|---|---|---|
| cosmology (ω~H₀) | 1.4e-33 eV | ~1e-32 |
| galaxy (k~2π/10 kpc) | 4.0e-27 eV | ~3e-26 |
| cluster (k~2π/Mpc) | 4.0e-29 eV | ~3e-28 |
| solar system (k~2π/AU) | 8.3e-18 eV | ~6e-17 |

Every regime sits ≤ ~1e-17 of the cutoff — the EFT is **valid across all of them**.
(Solar system has a large k but the scalar is MOND-screened there, g≫a₀, and the
static-source modification only switches on after t_c≫1/H₀; see (b).) **VERDICT (a):
no regime where the EFT breaks down observably. The "needs a UV completion above M"
caveat is the generic EFT statement shared by ALL of MOND/AeST — not a kill.**

## (b) Antigravity / oscillating-force scale — does NOT intrude on galaxies; reaches cluster outskirts / P(k) only at k~μ (free)

**ACLM Eq 1.10:** r_c ~ M_Pl/M² (length where the Newtonian potential goes oscillatory),
t_c ~ M_Pl²/M³ (the time you must WAIT before it appears); reach at distance r needs
t ~ t_c·(r/r_c) (Eq 7.18–7.20). Graviton mass **m = M²/(√2 M_Pl) (Eq 7.7) = AeST's μ.**

For the framework's clustering window the **wait time is the protector** (calc):
- M=0.15 eV (μ⁻¹=1.0 Mpc): a modification at 20 kpc needs t ~ **1e24 Gyr**; at 1 Mpc ~ 5e25
  Gyr; at 10 Mpc ~ 5e26 Gyr — all ≫ age (13.8 Gyr) → **NEVER develops**.
- M=1 eV (μ⁻¹=22 kpc): same, t ≥ 1.6e23 Gyr at 20 kpc → never.

In AeST the onset is a **spatial** feature at r_C ~ (r_M/μ²)^(1/3); Verwayen–Skordis–Boehm
(2304.05134) Fig 4: μ⁻¹=1 Mpc → r_C≈156 kpc, μ⁻¹=0.1 Mpc → r_C≈33.6 kpc. Choosing μ⁻¹≳1 Mpc
(⇔ M≲0.15 eV) pushes r_C **beyond galaxy disks**, just into cluster outskirts.

**Load-bearing consistency check (`dS_window_check.py`):** ACLM Eq 8.19 places the healthy
regime in a window **Γ = αM³/4M_Pl² < H < m = μ**. For the framework's M=0.04–1 eV:
**H₀/Γ ~ 1e22–1e27** (instability CURED by de Sitter Hubble friction, Eq 8.24:
Φ~e^(−Ht)+e^(−2Ht), by 22–27 orders) AND **m/H₀ ~ 3e2–2e5** (feature INSIDE the horizon).
Window comfortably satisfied across the whole framework window. (At the DE-attractor
M~1e-3 eV the feature is OUTSIDE the horizon, m/H₀=0.2 — ACLM's "indistinguishable from Λ";
the framework's DUST M is bigger, so its feature is sub-horizon.)

**VERDICT (b): the antigravity/oscillation regime does NOT intrude on galaxy dynamics
(wait-time ≫ age at galaxy/cluster radii; r_C≳156 kpc for μ⁻¹≳1 Mpc), and the worst
pathology (the k<μ Jeans instability) is CURED by the framework's own de Sitter background
by >20 orders. It DOES reach cluster outskirts / P(k) at k~μ~Mpc⁻¹ — but μ is FREE and is
squeezed precisely by that data (galaxy-WL wants μ⁻¹ large, clusters small). This is the
banked "free constant pushed to the window edge," not a clean new effect.**

## (c) Dark-matter-vs-dark-energy seesaw tension — DODGED by the framework's additive-Λ split

The literature tension: one GC doing BOTH faces wants two different M. The **dark-ENERGY**
seesaw M⁴/M_Pl² = ρ_DE wants **M_seesaw = (ρ_DE M_Pl²)^¼ ≈ 0.11 GeV** (calc), which exceeds
the **BH-accretion ceiling M ≲ 10 MeV** for the DUST face (hep-th/0404216: a 10 MeV GC
accretes onto a stellar BH at up to ~0.1 M_⊙/s — set by the GC scale M, not the cosmic
density). So a single GC straddling both faces is in genuine tension.

**The framework's split avoids it:** Λ enters K(Q) as a **separate additive −2Λ** (the dark
energy is the explicit cosmological constant, not the condensate's seesaw), so the
framework's GC is asked to be **only the w=0 dust** at M~0.04–1 eV — **~7 orders BELOW the
10 MeV BH-accretion ceiling** (M/10 MeV ~ 1e-7 to 1.5e-8). Accretion is benign, dust-like
(Mukohyama hep-th/0502189). **The straddle tension does NOT bite.**

**VERDICT (c): the seesaw tension is genuinely avoided — a real consistency advantage over
the literature's single-GC dark-matter+dark-energy straddle (credited at full weight). The
price is exactly the banked orthogonality d(ρ_dust)/dΛ = 0: with Λ split off as an additive
constant, Λ cannot pin the dust amplitude I₀ (FREE; conceded at full weight). The dodge IS
the orthogonality.**

## (d) The k⁴ dispersion — a NEW distinctive P(k)/CMB feature, or CDM-degenerate? — DEGENERATE (honest null at full weight)

**ACLM Eq 7.8:** ω² = α²k⁴/M² − (α²M²/2M_Pl²)k². The k⁴ piece DOMINATES (departs from
pressureless CDM) for **k > m = μ**; below k<μ it is the Jeans/ω=0 Y-mode. So the GC dust =
CDM at small scales (high k) and DEPARTS at **large scales k≲μ~Mpc⁻¹** — the *opposite* of
a particle-CDM free-streaming/Jeans cutoff (which is at high k). For the framework's M the
feature sits at k~μ: M=0.04 eV → k_μ≈0.11 h/Mpc (λ≈86 Mpc); M=0.15 eV → 1.5 h/Mpc; M=1 eV →
67 h/Mpc.

This IS nominally in the P(k)/CMB-lensing window. BUT: (i) AeST **already fits full Planck
incl. the 3rd peak + the matter power spectrum** (Skordis–Zlosnik 2021 PRL 127 161302) by
tuning the cold component to mimic CDM — so the leading behavior is CDM **by construction**;
(ii) the residual departs only at k≲μ where μ is **free** and pushed to ≳Mpc⁻¹ precisely to
keep galaxy MOND and satisfy the SZ21 μ≲Mpc⁻¹ stability bound — driving the feature toward
super-survey k as μ→0; (iii) cosmic variance is worst exactly there.

**VERDICT (d): the candidate distinctive signal (k⁴ → a P(k)/CMB-lensing feature at k~μ) is
NOT out-of-window, but it is DEGENERATE with the free μ and already absorbed into AeST's
CMB/P(k) fit. It is NOT a clean new falsifiable front beyond the framework's two live ones
(s^TX SME dipole, a₀(z) DESI) unless μ can be INDEPENDENTLY pinned — which the framework
cannot do (μ, I₀ free). Honest null at full weight; no manufactured signal.**

---

## NET (both ways)

**Validity/consistency: COMFORTABLE.** (a) The EFT cutoff Λ_strong≲M sits ~17–32 orders
above every energy the framework uses the GC at → valid in cosmology, galaxies, clusters,
solar system; the leading interaction is irrelevant (controlled IR). (b) The
antigravity/oscillation scale does not intrude on galaxies (wait-time ≫ age; r_C≳156 kpc
for μ⁻¹≳1 Mpc) and the Jeans instability is cured by the framework's own de Sitter
background by >20 orders (ACLM Eq 8.24, window Γ<H₀<m satisfied). (c) The literature's
dark-matter-vs-dark-energy seesaw tension is genuinely avoided by the additive-Λ split (GC
is dust-only, 7 orders below the BH-accretion ceiling). **All three credited at full
weight.**

**New testable front: NO, not at full weight.** The one place the GC physically departs
from ΛCDM-CDM — the k⁴ feature at k~μ — is degenerate with the free clustering scale μ and
already inside AeST's CMB/P(k) fit. It is in-window but not independently predictive →
honest null (a degeneracy, not a signal). The consistency advantages do NOT come free: they
are bought with the banked free dust amplitude I₀(≈Ω_dm) and the free μ.

**Quarantine held:** a₀, Z, κ, I₀ never asserted derived; μ, I₀ conceded free. Both-ways:
the comfortable validity window + the genuinely-dodged seesaw tension credited at full
weight; the degenerate (CDM-mimicking, μ-free) k⁴ "signal" conceded as an honest null at
full weight. No manufactured win; no reflexive dismissal.

**Sources (pulled verbatim this session):** ACLM hep-th/0312099 Sec 4–8 (Eqs 1.9–1.12,
4.1–4.7, 7.7–7.20, 8.19–8.29; /tmp/aclm.txt); Skordis–Zlosnik 2021 PRL 127 161302
(full-Planck+P(k) fit, μ≲Mpc⁻¹); Skordis–Zlosnik 2021 arXiv:2109.13287 ("μ ≲ Mpc⁻¹ so the
low-momenta instability may only play a role on cosmological scales"); Verwayen–Skordis–
Boehm 2304.05134 (r_C, Fig 4, the GC weak-field Poisson identity); BH accretion of the GC
hep-th/0404216 (the M≲10 MeV ceiling, ~0.1 M_⊙/s); Mukohyama hep-th/0502189 (dust-like
accretion). Banked: GHOST_CONDENSATE_2026-06-19.md, AMOUNT_AND_PATHOLOGIES_NOTES_2026-06-19.md,
AEST_EMBEDDING_2026-06-19.md.

**Files (absolute):**
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/EFT_VALIDITY_WINDOW_VERDICT_2026-06-19.md
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/eft_validity_window_calc.py
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/dS_window_check.py
