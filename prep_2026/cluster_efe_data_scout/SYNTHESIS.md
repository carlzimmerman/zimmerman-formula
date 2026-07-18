# Cluster-EFE sigma-spread test — MMU data-availability SCOUT (SYNTHESIS)

**Question scouted:** Is the exploratory cluster-member EFE sigma-spread test — the "nearest bite"
from the cluster-EFE swing (prep_2026/cluster_efe_channel/SYNTHESIS.md) — ASSEMBLABLE from PUBLIC
MultimodalUniverse (MMU) data NOW?

**Observable:** D(zone) = <ln(sigma_int / sigma_bary)>_zone − <>_ancient, evaluated WITHIN a fixed
deprojected caustic-a_ext bin, members tagged by Rhee+2017 (ApJ 843:128) phase-space infall zones,
sigma_bary from beta-immune Wolf+2010. MG gives EXACTLY 0 at fixed true field (theorem). The
framework prediction (sign reconciliation w9xvb10ui / commit dd12427b): EXISTENCE (MG=0, theorem-grade)
+ first-infall-HOTTER leading sign; MAGNITUDE at the framework-committed E10 memory (tau_mem=203 Gyr)
= **~0.3–1.5% absolute / ~4–9.5% relational** (this supersedes the old short-memory 6–13%).

**This is a DATA-AVAILABILITY go/no-go, NOT a physics claim. No "proves". MI-class-generic (MI vs MG=0),
not framework-vs-Milgrom.**

---

## VERDICT: NO-GO from public MMU data now (MARGINAL/UNDERPOWERED only with a non-MMU SAMI stack)

The verdict survives an adversarial verify re-run (VERIFY.md); neither a GO nor a NO-GO is manufactured.

| Configuration | Diffuse tagged carriers N | S/N z (opt / mid / pes) | Call |
|---|---|---|---|
| **MMU-MaNGA ALONE, NOW** | **~40–77 (TENS)** | 1.2 / 0.5 / 0.2 | **NO-GO — dies on statistics** |
| MaNGA + SAMI public stack | ~135–237 | 2.0 / 0.9 / 0.3 | MARGINAL/underpowered; SAMI **not** in MMU |
| Clean-exploratory target | 300–500 | 2.3 / 0.9 / 0.3 | required floor; even this only clears 2–3σ in the optimistic corner |

The "2–2.5σ" figures are the **optimistic corner only** (best-case signal 9.5% + purity 0.65 +
scatter 0.18 + sys 0.012 simultaneously). The **honest central (mid) expectation is a non-detection
at every accessible N** (z < 1 everywhere reachable). The test is **STATISTICS-limited at all
accessible N** (se_stat > the 0.020 systematic floor until N ≳ 400) — the opposite failure mode from
the SDSS single-fiber stack, which was systematics-limited.

---

## WHY (the binding number is the diffuse-carrier COUNT, not the data type)

**What IS available (real GO on these axes):**
- **Resolved stellar sigma IS served by MMU-MaNGA** — externally verified on github: the MMU manga
  builder ships DAP MAPS HYB10-MILESHC-MASTARSSP alongside the DRP LOGCUBEs, keeping the full
  `STELLAR_SIGMA / STELLAR_SIGMA_IVAR / STELLAR_SIGMACORR` extensions. sigma_int is recoverable as a
  resolved 2-D map (aperture 2nd moment inside R_e, quadrature-subtract SIGMACORR) with **no pPXF
  re-derivation**. The kinematics half of feasibility is genuinely fine.
- **Membership / phase-space tagging + caustic a_ext profiles are ABUNDANT and ready** and are NOT the
  bottleneck: GalWCat19 (Abdullah+2020, 1800 clusters z=0.01–0.20, 34,471 members, caustic M/R at
  Δ=500/200/100), HeCS/HeCS-omnibus (Rines+2013/2016, dedicated caustic profiles), Yang SDSS groups,
  and the SAMI cluster redshift survey (Owers+2017, 8 clusters, 2,899 members, caustic+virial masses).
  **DESI DR1 BGS deepens membership ~9.5×** (854 deg⁻² reliable z vs ~90 for SDSS main; Hahn+2023),
  reaching into the dwarf regime at Coma z — but it delivers redshifts, NOT IFU sigma maps. This
  scaffolding slots straight in once the carrier sample exists.

**What FAILS (the binding constraint — confirmed the predicted failure mode):**
- **MaNGA is stellar-mass-limited (M* floor ~5×10⁸, logM ~9) and field-dominated.** The diffuse
  deep-MOND carriers (a_in ≲ 1.5 a0 ⇒ sigma ~20–70 km/s) are BOTH rare in the sample and jammed
  against the instrumental LSF. Chain (transparent estimate, not a cross-match): 977 dwarfs × ~0.45
  in-window × ~0.55 LSF-reliability + intermediate low-tail ≈ **~343 diffuse carriers all-environments**;
  after the rich-cluster-member + caustic-able + Rhee-taggable cut ⇒ **~40–77 in MMU-MaNGA**.
- **Stellar-sigma LSF floor is the real killer.** MaNGA LSF 1σ ≈ 70–76 km/s; reliable STELLAR sigma
  bottoms near ~35–45 km/s, so sigma 20–40 km/s dwarfs are **upper-limit-only**, and the accessible
  ~45–70 km/s carriers sit at shallower a_in and carry a SMALLER true D(zone) than the headline
  4–9.5% — so if anything the S/N above is mildly overstated (a tightening toward NO-GO surfaced by
  the verify). Penny+2016 confirms ~13% of even M*=1–5×10⁹ dwarfs are already unmeasurable below the floor.

Two independent verify tightenings (emission-vs-stellar sigma floor; optimistic-corner S/N) both push
MORE toward NO-GO, leaving the go/no-go unchanged. The DESI BGS 9.5× deepening applied to the specific
z<0.05 host clusters is assumed (not cluster-by-cluster verified) but is NON-BINDING — tagging comes
from GalWCat19/HeCS/Yang regardless.

---

## WHAT IS NEEDED (the gap, in order)

1. **Ingest SAMI cluster IFU into a homogenized stack** (Owers+2017; A85/A119/A168/A2399/A3880/A4038/
   EDCC442/APMCC0917, z=0.029–0.058 — already Rhee-taggable with membership + cluster-centric radius +
   peculiar velocity). This lifts N to ~135–237 and makes an **underpowered ~2–2.5σ firewalled hint**
   — but SAMI is public and **NOT an MMU product**, so it fails the literal "assemble from MMU now" test.
2. For a clean >3–5σ bite: a **dedicated wide nearby-cluster dwarf-IFU survey** with M* floor to
   logM~8, resolved STELLAR sigma reliable well below 45 km/s, and sub-percent systematics
   (~10³–10⁴ diffuse members). Candidate stack additions: MaNGA + SAMI + Hector + MAGPI with a
   low-sigma re-reduction.
3. Ultimately **ELT / HARMONI**-class IFU (~2032) to reach the ~20 km/s diffuse cluster-dwarf regime
   (UDG carriers) cleanly.

The membership/caustic scaffolding (GalWCat19 + HeCS + DESI DR1 BGS) is ready and slots in the moment
a diffuse-carrier IFU sample of the right size and sigma-floor exists.

---

## Artifacts in this directory (all scripts exit 0; frozen zimmerman-formula repo READ-ONLY, untouched)
- `inventory_manga.py` / `INVENTORY_MANGA.md` — IFU/MaNGA lane; resolved sigma served; ~40 alone, ~200 stack
- `inventory_membership.py` / `INVENTORY_MEMBERSHIP.md` — phase-space/caustic lane (abundant, not bottleneck); ~77 alone, ~172 stack
- `overlap_power.py` / `OVERLAP_POWER.md` / `overlap_power.out` — reconciled overlap band 40–77 (alone), 135–237 (stack), full z-table + limiting-factor diagnostic
- `VERIFY.md` — adversarial re-run + both-ways audit; CONFIRMED NO-GO

_Data-availability call only. No physics claim. No "proves"._
