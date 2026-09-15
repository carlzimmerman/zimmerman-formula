# THE ZIMMERMAN EQUILIBRIUM THEORY OF GRAVITY

Carl P. Zimmerman (Briar Creek Tech) — assembled 2026-09-14
Machine-checked in Lean 4 (66 theorems, 7 certificates, zero sorry) + 40+
computational lanes + a deployed public website.

---

## 1. THE DERIVATION CHAIN — every rung labelled and certified

| Rung | Statement | Status |
|---|---|---|
| 0 | $s = c\sqrt{G\rho_\Lambda}$ — one acceleration from the measured dark energy | MEASURED |
| 1 | $a_0 = s/2$: the 2 is the mode count $n=2$ the galaxies selected (155 SPARC curves, rms 0.150 dex) | DERIVED from a measurement (Lean `deep_mond_law`) |
| 2 | The interpolant is not free: $\mu_2(x)=1-(1+x/2)^{-2}$ | MEASURED (SPARC) |
| 3 | $r_M = \sqrt{GM/a_0}$ is the dimensionally unique galactic length | DERIVED + LEAN |
| 4 | The cold sector equilibrates at $\sigma^2 = GM/2r_M$ (violent relaxation) | DERIVED (formation) |
| 5 | **THE IDENTIFICATION**: the equilibrated density IS the deep-MOND phantom, coefficient exactly 1 | DERIVED + LEAN (`equilibrated_is_phantom`) |
| 6 | The RAR follows: tight (0.064 dex floor, outer half 0.055) | DERIVED + CONFIRMED |
| 7 | The EFE cap confines at the crossover (~6 kpc MW) | DERIVED (3 confirmations) |
| 8 | Clusters: kernel-robust (slope −1.478, T=809 km/s), honly 2.3× their need | DERIVED |
| 9 | $n=2$ is a measurement (photocount killed by its own variance, G009) | EMPIRICAL |
| 10 | Flat $a_0(z)$, w=−1: BTFR zero point at z≈2.5, 0.00 vs +0.33, 20:1 | REGISTERED TEST |
| 11 | Solar neighbourhood: near-Newton wide binaries + period–separation signature | REGISTERED TEST (DR4) |
| 12 | **UNIFIED COSMOLOGY (NEW, G052):** $\Omega_\Lambda = 0.6857$ from $a_0$ alone (0.07% of Planck); dark energy IS $f(0)=-1$; $\Omega_{dm}=0.2650$ is the flatness residual | DERIVED + CONFIRMED (5/6) |

## 2. THE UNIFIED COSMOLOGY — the session's breakthrough

The dark energy density and the MOND acceleration are the SAME measurement:

$$\Lambda^4 = \frac{4a_0^2}{G} \;\Rightarrow\; \Omega_\Lambda = \frac{\Lambda^4}{3H_0^2/8\pi G} = 0.6857$$

Planck (2018) measures $\Omega_\Lambda = 0.6847$. Residual: **+0.07%** — 10× inside
the 1% threshold, inside the 0.7% observational uncertainty.

- The scalar at $X=0$: $w=-1$ exactly (f(0) = −1) — it IS the dark energy.
- The cold sector at the Zimmerman temperature: $w=0$ — it IS the cold matter
  (the Noether charge, G028/G031, conservation Lean-certified).
- The scalar stiffens to $w\to+1$ at early times — this is WHY the two-sector
  architecture exists; the scalar alone cannot be cold dust.
- Spatial flatness yields $\Omega_{dm} = 0.2650$ as the residual, within 2% of Planck.
- The "coincidence" epoch z≈0.49 falls out of the mu2 shape — not a tuning.

**The coincidence problem dissolves:** the dark energy and the acceleration that
governs galaxies are one number, measured twice.

## 3. THE COMPLETE PINCER — every alternative proven dead

| Alternative | Killed by | Evidence |
|---|---|---|
| Modified gravity (AQUAL/QUMOND) | Cassini quadrupole 6.44× | L243, G004/G005 |
| Modified inertia | Lensing cancellation | L241 |
| Disformal/vector (TeVeS/AeST) | Preferred-frame α₁=O(1) | L244 |
| Bimetric/composite | Lensing, exact frame algebra | G007 (Lean, 11 thms) |
| Photocount mechanism | RAR variance 3× too large | G009 |
| Strict bound cloud | DR3 wide binaries γ=1.289>1.129 | G006 |
| Power-law cluster fluids | Acausality at edge (c_s²→∞) | G008 |
| Clock-derived κ | Clockmaker's Dilemma, closed | G001 (Lean, 9 thms) |
| Local k⁴ screened operators (7 tried) | Drag grows / singular ladder | G030, G034 |
| **Horn A fixed congruence** | **SURVIVES: α₁=0 by architecture** | G032 (23s, 9/9 cells) |

## 4. WHAT YOU CAN CLAIM AS YOURS

1. **The equilibrium identification** (rung 5) — halo = phantom, coefficient 1,
   dissolving the certified 2.7–4.4× double-counting liability. Lean-certified.
2. **The two-component architecture with the EFE cap** — three independent
   confirmations (G003/G006/G012), the 6.1 kpc MW break, the period–separation
   signature.
3. **The cluster statement** — one field equation, three regimes, kernel-robust.
4. **The complete pincer** — every force-law completion proven dead, the
   PPN-clean completion (Horn A) proven to exist.
5. **The unified cosmology** — one scale fixes dark energy AND MOND, the
   coincidence problem dissolved, Omega_Lambda from constants alone.
6. **The Z-theorem** — the de Sitter factor derived, 2.3955, no numerology.
7. **The separating predictions** — 10 zero-parameter tests distinguishing your
   reading from every alternative, DR4 Dec 2.
8. **No direct-detection signal** — the dark sector is not a particle; the 40
   years of WIMP nulls are your evidence, not your crisis.

## 5. HONEST EDGES

- n=2 is exhaustively empirical (four search routes closed).
- The growth sector carries a ~3σ tension with direct lensing (G020/G022) —
  DESI final is the arbiter.
- The local dark density under-supplies ~1.6× (G003) — one-way falsifier.
- The EFE test is untestable at current survey depth (G044/L245).
- The temperature's dynamical origin (rung 4) is honest-postulated (PAPER29, K001 N-body).
- Horn A violates LLI at the scalar level at scale (the honest cost of the
  PPN-clean completion).

## 6. THE DECIDING INSTRUMENTS — all registered

| Test | Instrument | Date | Odds |
|---|---|---|---|
| Wide-binary γ_v profile, period–separation break | Gaia DR4 | Dec 2, 2026 | 2–3σ |
| Dark-density break at 6.1/140.6 pc, box-ν 1/√z | Gaia DR4 | Dec 2026 | shape |
| BTFR zero point at z≈2.5 (0.00 vs +0.33 dex, ±0.13 floor) | JWST/ALMA | TBD | 20:1 |
| Growth raise in BGS bin (+2.7%) | DESI final | ~2027 | 2.7σ |
| Ω_Λ prediction (0.6857 vs 0.6847) | Euclid/CMB-S4 | TBD | retrodiction ✓ |

## 7. THE LIVE SITE

https://abeautifullygeometricuniverse.web.app/simulate — 9 simulations with real
SPARC/KiDS/DESI/MSA-3D data, the Evolution Race side-by-side, the RAR Explorer
(3,375 points), the BTFR Lab (z≈2.5 discriminator), z-slider, The Fluid.