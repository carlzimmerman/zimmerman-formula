# ROUTE C — broader scale-dependent-DM clustering: can a dark sector be galaxy-smooth AND cluster-clumpy? NO. The no-go STANDS.

*Route C of the evade-the-cluster-no-go hunt (the `CLUSTER_RESIDUAL_EXPLAIN_2026-06-20` no-go). Both-ways,
quarantine held (a0/Z/kappa/I0 never derived). Script:
`opus_48_extended_research/reviews/evade_nogo/routeC_scale_dependent_DM_clustering.py` (exit 0).*

## The question
Is there a KNOWN mechanism by which a dark sector clusters in CLUSTER cores (~Mpc) but stays SMOOTH in
GALAXY disks (~kpc) — the opposite of the no-go's "galaxies clump more" verdict — and can the AeST
ghost-condensate Q-mode REALIZE that scale? The candidate families: warm DM, fuzzy/ultralight DM, SIDM,
plus the AeST host's own k⁴ tail and mu mass term.

## The directionality trap (the crux)
The familiar "small-scale-suppression" DMs (warm/fuzzy/SIDM) suppress clustering BELOW a scale or BELOW a
density. **Galaxies are BOTH the smaller-LENGTH and the denser environment** (banked: galaxy disk
9.7e13 rho_crit vs cluster core 2.6e13 rho_crit — galaxies 3.7x DENSER). So a cutoff tuned to smooth
galaxies fails the split in one of two structural ways:
1. **Density-gated mechanisms (FDM, ghost-condensate k⁴): Jeans length ~ rho^{-1/4}.** The LESS-dense
   cluster core has the LARGER Jeans length → it is suppressed MORE than the galaxy. Backwards. Robust
   across the whole density-ratio range (clus/gal Jeans ratio = (rho_g/rho_c)^{1/4} = 1.39 at 3.7x, still
   >1 even at 1.1x).
2. **Power-removing mechanisms (WDM free-streaming, SIDM scattering):** they REMOVE a halo / make a core
   = they take mass AWAY. The no-go needs the field to ADD ~6.4e13 Msun of clumped mass to the cluster
   CORE. A free-streaming or scattering cutoff deposits NO extra core mass — it just smooths the field
   everywhere below the cutoff. Wrong job entirely.

## Per-mechanism (real numbers, from the script)
| mechanism | characteristic scale | why it fails | AeST host? |
|---|---|---|---|
| Warm DM (free-stream) | lambda_fs: 264 kpc @0.3keV → 5 kpc @10keV | smooths sub-kpc only in the Ly-a-allowed range (m>5.3 keV); to erase a galaxy halo needs HOT/excluded m; removes halos, adds NO core mass | NO |
| Fuzzy/ULDM (quantum Jeans) | lambda_J ~ rho^{-1/4}; cosmic-mean ~68 kpc @1e-22 eV | density-gated: denser galaxy clumps MORE, less-dense core suppressed MORE (clus/gal Jeans = 1.39x) | NO |
| SIDM (vel-dep sigma/m) | cores via scattering | REMOVES central mass (makes cores); wrong sign twice | NO |
| Ghost-condensate k⁴ Jeans (IF B>0) | lambda_J ~ rho^{-1/4} | same density-ordering defeat as FDM; **AND B=0 in the AeST host so it does not exist** | NO (B=0) |
| AeST mu mass term K=mu²(Q-1)² | screens > mu⁻¹ ~ 22 Mpc | kills the LARGEST scales not the smallest (backwards); both galaxy & core sit ~1e26x above the rho-threshold mu²/4piG → both collapse | NO |

## The decisive host facts (primary-source verified this session)
- **Blanchet-Skordis 2024 (arXiv:2404.06584) abstract, verbatim:** the propagating scalar dof has
  **"dispersion relation omega=0"** — non-propagating, no k² or k⁴ dispersion in the linear sector.
- **The Hamiltonian is "bounded from below for wavenumbers larger than ~10⁻³¹ eV"** = lambda ~ 402 Mpc
  ~ 0.09x the Hubble radius. The ONLY scale in the linear AeST scalar problem is **HORIZON-sized** —
  there is no sub-Mpc dynamical scale to separate galaxies from clusters.
- **Door-A pin (banked wxe4q0b5x, re-confirmed):** the k⁴ coefficient **B = 0 EXACTLY** in the AeST
  khronon; the lone k⁴ in the action is the non-dynamical constraint momentum P_nu, gauge-fixed to zero.
  → the candidate loophole's premise (a finite k⁴ Jeans scale between kpc and Mpc) **does not exist**.

## Verdict (both ways)
**NO known scale-dependent-clustering mechanism realizes the galaxy-safe/cluster-clumpy split in the
direction the no-go requires, and the AeST Q-mode cannot embody one.** We hunted hard — granting B>0,
scanning particle masses (WDM 0.3-10 keV, FDM 1e-24..1e-21 eV), scanning k⁴ length scales (0.1-10 Mpc),
checking the mu term and the omega=0 stability scale — and the window does not open. The two failure
modes are structural: density-gated Jeans goes the wrong way (rho^{-1/4} favors the denser galaxy), and
power-removing cutoffs subtract mass instead of adding it to the cluster core. **The no-go STANDS.**

No manufactured loophole (the window genuinely does not open under any tested choice); no high-priest
dismissal (every mechanism's real scale was computed and its direction checked honestly; FDM/WDM ARE the
"right direction" for *suppressing galaxy power* — they just cannot *fill a cluster core*). Quarantine held.

### Sources
Blanchet-Skordis 2024 (arXiv:2404.06584, abstract: omega=0, bounded H for k>1e-31 eV); Skordis-Zlosnik
2021 (arXiv:2007.00082, cs²→0 sub-horizon); Arkani-Hamed-Cheng-Luty-Mukohyama 2004 (hep-th/0312099, ghost
condensate omega²=cs²k²+k⁴/M²). Banked: DOORA_PIN_REAL_COEFFICIENTS (B=0), CLUSTER_RESIDUAL_EXPLAIN_2026-06-20
(the no-go + density landscape), AEST_EMBEDDING_2026-06-19. WDM half-mode (Schneider/Viel/Bode-Ostriker-Turok);
Ly-a bound m_WDM>5.3 keV (Villasenor 2023 / Irsic).
