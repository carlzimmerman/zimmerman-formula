# ROUTE cluster_aest_massterm: the AeST scalar mass term vs the cluster deficit eta~2.15

*Opus 4.8, 2026-06-14. First-principles derivation. Companion script:
`cluster_aest_massterm_derivation.py` (validated integrator, all numbers below
reproduced on the exact Durakovic-Skordis Eq. 2.40). Grade: **CANDIDATE-UNPROVEN**
(PARTIAL at best). Not a manufactured cure; not a clean fail.*

## The target (banked, eRASS1 9830 clusters, framework a0 = 9.36e-11)
At R500 ~ 1.3 Mpc, M500 ~ 5e14 Msun: g_bar/a0 = 0.44 (near-MOND, NOT deep), and MOND
misses a factor **eta = g_obs/(nu g_bar) = 2.15** = **+0.66 dex in M_eff**. The
distinctive a0(z) lever supplies only +0.025 dex (~4%) -- irrelevant. The intrinsic
candidate is the AeST scalar **mass term mu^2 Phi**.

## The equations (exact, Durakovic-Skordis 2024 arXiv:2312.00889)
- Quasi-static modified Helmholtz (2.40): `(1/r^2) d/dr[r^2 M(x) Phi'] + mu^2 Phi = 4pi G_N rho_b`
- Interpolation (2.9): `M(x) = (sqrt(1+4x)-1)/(sqrt(1+4x)+1)`, `x=|Phi'|/a0` (M->1 Newton, M->x MOND)
- Mass scale (2.18): `mu^2 = 2 K2 Q0^2/(2-K_B)`, **1/mu >~ 1 Mpc PINNED by CMB/cosmology**
- Phase-space (3.4-3.9), `P = r^2 M(x) Phi'`: `Phi'=a0 x`, `dP/dr = r^2(-mu^2 Phi + 4pi G_N rho_b)`.
  Pure MOND (mu=0, vacuum): P=G_N M=const. The mass term **drains/pumps P** -> perturbs g.

## What the derivation shows (integrator validated vs analytic MOND to 0.03%)

**1. The scale is right (CONFIRMED, derived).** With 1/mu=1 Mpc: (mu r)^2 = 6e-20 (Solar
System), 1e-4 (galaxy 10 kpc), **1.7 (R500)**, 9 (3 Mpc). The mass term is OFF below
clusters, ON at clusters. Galaxies stay MOND-pure (MW-like, 30 kpc: AeST/MOND = 0.998,
0.17% deviation). This part works -- a genuine intrinsic mechanism ordinary MOND lacks.

**2. The amplitude/sign at R500 is set by a FREE boundary condition, not predicted.**
Integrating the exact EOM with the CMB-pinned 1/mu=1 Mpc:
- **Natural inner BC** (P=G_N M const): g_AeST/g_MOND **@R500 = 0.21 -- a DEFICIT**, not a
  2.15x boost. The mass term first DRAINS g at R500; the helpful peak (3.8x) sits at
  ~6 Mpc, the WRONG radius.
- Sliding the free boundary shift chi_inf over a range ~|Phi_MOND(R500)| ~ (2000 km/s)^2
  walks the ratio@R500 from 0.21 -> 1.1 (and higher). **eta=2.15 is REACHABLE -- but
  fitted per cluster, not predicted.** No inner-physics reason lands it at 2.15.

**3. Scale tension (Mistele+2023 A&A 676 A100, cited).** A >=10% cluster deviation needs
m^2/fG > 2.5 Mpc^-2 (1/mu < 0.63 Mpc), TIGHTER than the galaxy/CMB bound 1/mu >~ 1 Mpc.
A 115% lift (eta=2.15) needs mu larger still. **One mu cannot keep galaxies MOND-pure
AND lift clusters by 2x.** (My inversion of their Eq.9 did not reproduce 2.5 -- the
WebFetch-reconstructed coefficient is unreliable -- so I cite their number, not a
re-derivation.)

**4. Wrong radial SHAPE.** The AeST RAR is "a peak ... FOLLOWED BY A DEFICIT ...
interpreted as a negative phantom mass" (Durakovic-Skordis). eRASS1 needs a SUSTAINED
~2x boost out to/beyond R500 (deficit deepens outward). AeST gives a local bump (radius
~ M via mu_hat^2 = mu^2 r_M^2) then UNDERSHOOTS -- a per-cluster tune to park the peak
at each R500.

**5. Stability caveat (both ways).** The helpful enhancement is the positive-density
part; the sub-MOND deficit needs NEGATIVE condensate density. Mistele+2023: "condensates
with negative energy-density are unstable ... we expect the AeST model to be unstable in
this oscillatory regime." Durakovic-Skordis counter the singularities are "only apparent"
(removed by evolving the canonical momentum) -- but that is NUMERICAL regularity, NOT a
proof of physical/perturbative stability. Only isothermal toy models; NO eta-vs-M500 fit.

## Verdict: CANDIDATE-UNPROVEN
Right scale (derived), right sign at onset, a genuine intrinsic AeST mechanism. But it
does NOT close eta=2.15 from first principles: the natural BC gives a *deficit* at R500;
the boost rides a free, per-cluster boundary shift; one mu faces a galaxy<->cluster scale
tension; the radial shape is a local peak+deficit not a sustained boost; the helpful
regime borders a flagged instability. **A real candidate, unproven -- not a manufactured
cure, not a clean fail.**

Sources: Durakovic & Skordis 2024 JCAP 04 040 (arXiv:2312.00889); Verwayen, Skordis &
Zlosnik 2024 MNRAS 531 272 (arXiv:2304.05134); Skordis & Zlosnik 2021 PRL 127 161302;
Mistele, McGaugh, Schombert 2023 A&A 676 A100 (arXiv:2301.03499).
