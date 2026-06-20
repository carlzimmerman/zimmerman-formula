# CRUX (ii)-A — does the ghost-condensate k⁴/M² dispersion give a NEW falsifiable P(k) front? — verdict 2026-06-19

**Topic:** `pk_k4_signature`. **Both-ways + quarantine.** Sympy + real k in h/Mpc; primary
sources pulled verbatim this session (SZ21 PRL, ACLM, VSB24, SZ22 abstract).

**HEADLINE: NO NEW DISTINCTIVE FRONT — HONEST NULL, both ways.** The k⁴/M² dispersion is real,
and its Jeans/sound scale `k_J = M²/(√2 M_Pl)` is **exactly the AeST mass parameter μ** (the μ²Φ
"mass term for the potential," which SZ21 themselves call "akin to ghost condensation"). The
SHAPE of the deviation is a **suppression / modified-growth Jeans feature at k ≈ μ**, NOT a
propagating BAO-like oscillation in P(k). The SCALE is pushed **out of the observable P(k) window
by the same `μ⁻¹ ≳ 1 Mpc` that galaxies force**: realistically `k_J ~ 0.01–0.05 h/Mpc` (below
the lower edge of every survey), and only at the *most galaxy-disfavored* edge `μ⁻¹ = 1 Mpc`
(↔ M≈0.13 eV) does `k_J ~ 1.5 h/Mpc` reach the Lyman-α/Euclid window — where a single suppression
scale is **degenerate with Σmₙ / WDM nuisances** and **a sharp cutoff at k~1 h/Mpc is already in
Lyα tension**. Empirically, **SZ21 already computed AeST's linear P(k)** (Fig.2) and it is a
**tuned-to-mimic LCDM**: cold-dust evolution, few-% residual that is *function-dependent*
(Cosh/Exp/Higgs give different residuals), absorbed by a per-model bias b. **NET: degenerate with
CDM, not a third live front** (the framework's two live fronts — s^TX SME dipole, a0(z) DESI —
stand alone). Both ways: the in-principle k⁴ feature credited at full weight; its out-of-window /
free-μ / tuned-mimic status conceded at full weight. No manufactured signal, no reflexive dismissal.

---

## (a) The dispersion, the sign of A, and the SHAPE — sympy

ACLM (hep-th/0312099) broken-phase π-fluctuation, mixed with gravity (their Eq. 7.8):

> **ω² = (α²/M²) k⁴ − (α²M²/2M_Pl²) k² = B k⁴/M² − A k²**, with B = α² = O(1), A = α²M²/2M_Pl².

- **Sign of A: the k² term is NEGATIVE → Jeans-UNSTABLE below k_J** — but only because of the
  **gravitational back-reaction** (the M²π̇ linear-gravity coupling, ACLM Eq.1.9). The *bare*
  condensate (no gravity) has `ω² = +k⁴/M²` (pure quartic, **stable**, no k² at all). So the
  instability is a gravitational Jeans instability, not a kinetic ghost.
- **Jeans wavenumber** (ω²=0): `k_J = M√(A/B) = M²/(√2 M_Pl)` (sympy-exact). This is **ACLM's
  graviton-mass/antigravity scale m**, and it is **identically AeST's μ** (SZ21: `μ = √[2K₂/(2−K_B)]·Q₀`;
  the `μ²Φ` term "is akin to ghost condensation," SZ21 verbatim).
- **SHAPE:** for `k > k_J` the mode is a stable oscillator with `ω ~ k²/M` (sound speed
  `c_s = dω/dk ~ k/M → 0` as k→0): pressureless dust on large scales, k-dependent stiffness
  on small scales → a **Jeans SUPPRESSION** above k_J, **NOT a propagating oscillation**. For
  `k < k_J` the mode is Jeans-unstable but **cured by de Sitter** (Hubble friction, H>Γ by
  25–31 orders; ACLM Sec.8; SZ21 "does not cause vacuum instability at low momenta").
  The "oscillation" VSB24 see is in the **real-space halo potential at r > r_C ~ 156 kpc** —
  a halo-profile feature, not a linear-P(k) feature.

## (b) Locate k_J in h/Mpc — pushed out of the window

Two independent handles, **self-consistent** (they pick the same M):

| handle | input | k_J (h/Mpc) | where |
|---|---|---|---|
| GC graviton mass M²/(√2 M_Pl) | M = 0.04 eV | 1e−5..2e−5 | super-survey |
| | M = 0.13–0.15 eV | ~1.0–1.5 | Lyα/Euclid edge |
| | M = 1 eV | ~67 | far UV, unphysical here |
| AeST μ direct | μ⁻¹ = 1 Mpc (forced edge) | 1.48 | Lyα/Euclid edge |
| | μ⁻¹ = tens of Mpc (galaxy-favored) | 0.01–0.05 | **below P(k) window** |

Self-consistency: `μ⁻¹ = 1 Mpc ↔ M = √(√2 M_Pl μ) = 148 meV ≈ 0.13 eV` (sympy), the banked
clustering-scale center. **Observable window:** CMB-lensing 0.02–0.2, SDSS/DESI 0.01–0.3,
Euclid/LSST 0.05–5, Lyα 0.3–10 h/Mpc. The galaxy-FORCED region `μ⁻¹ ≳ several×10 Mpc` puts
`k_J < 0.05 h/Mpc` — at/below the lower edge of every probe, cosmic-variance- and bias-degenerate.

## (b′) The edge case (both ways, full weight)

There IS a corner (`μ⁻¹=1 Mpc ↔ M≈0.13 eV ↔ k_J~1.5 h/Mpc`) where the GC Jeans scale lands in the
Lyα/Euclid window — **credited at full weight**. But it fails to be a clean front because:
1. **Excluded by galaxies at exactly that edge** — `μ⁻¹=1 Mpc` is the absolute lower bound;
   VSB24's r_C=156 kpc sits inside galaxy/cluster outskirts, squeezed by galaxy-WL toward
   `μ⁻¹ = tens of Mpc`. The Lyα feature and the galaxy MOND fits are mutually exclusive.
2. **Degenerate with a known LCDM nuisance** — a single suppression scale at k~1 h/Mpc has the
   same shape as Σmₙ free-streaming and WDM/thermal cutoffs, already marginalized in every
   Lyα/Euclid analysis. No node structure, no phase → not distinctive.
3. **Not parameter-free** — `k_J = μ` is FREE (banked: μ squeezed opposite-ways by galaxy-WL vs
   clusters; `a0` does NOT set μ — `dρ_dust/da0 = 0`). A detected cutoff would be a *fit*, like Σmₙ.
4. **Lyα tension** — a sharp cutoff at k~1.5 h/Mpc is an order-unity small-scale suppression,
   already disfavored by Lyα WDM bounds (m_WDM > ~5 keV → cutoff k > ~20–50 h/Mpc).

## (c) What SZ21 ACTUALLY computed — tuned-to-mimic, not a k⁴ signal

SZ21 (PRL 127 161302, arXiv:2007.00082) computed the full linear P(k) (Fig.2, fit to SDSS DR7
LRG, k~0.01–0.2 h/Mpc) and CMB (Fig.1, fit to Planck 2018) for three free functions:
- **Cosmological dispersion is k²+M², NOT k⁴** (SZ21: `ω² = K₂(2−K_B)/K_B(1+½K_Bλ_s)k² + M²`,
  a massive acoustic mode, plus an ω=0 Jeans mode unstable only for k<μ). The k⁴ is the
  small-gradient (Y-sector / Minkowski) limit, not the transfer function.
- **Cold mode evolves as dust** (SZ21: "c²_ad and w are small enough so Π→0 and we get dustlike
  evolution"). "For a wide range of parameters, this … theory is consistent with Planck."
- **Residual vs LCDM is few-% AND function-dependent** (Cosh/Exp/Higgs give different residuals),
  with a per-model bias `b` (LCDM 1, Cosh 0.975, Higgs 0.98, Exp 0.995) absorbing low-k offsets.
  That is a **tuned free function**, not a parameter-free distinctive prediction.

## Verdict (both ways, quarantine held)

The k⁴/M² dispersion is real, its Jeans scale is sympy-exactly `k_J = M²/(√2 M_Pl) = μ`, and the
deviation SHAPE is a **suppression**, not an oscillation. But the SCALE is pushed below the
observable P(k) window by the galaxy-forced `μ⁻¹ ≳ 1 Mpc`; the only in-window corner is
galaxy-disfavored, Σmₙ/WDM-degenerate, free-μ-not-a0, and Lyα-disfavored; and SZ21's own computed
linear P(k) is a tuned free-function mimic of LCDM. **This is an honest NULL — degenerate with
CDM, not a new distinctive front.** Quarantine: a0/Z/κ/I₀ never asserted derived; μ conceded FREE.
Both ways: in-principle feature credited; out-of-window/degenerate/tuned status conceded — equally.

**Files (absolute):**
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/pk_k4_signature.py
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/pk_k4_edge_case.py
- this note.
