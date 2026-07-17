# MI Linear Cosmology — first tractable pass (2026-07-17)

**Scripts** (both exit 0): `mi_growth.py` (A: self-consistent MI growth ODE),
`mi_spectra.py` (B: sigma8, P_v, bulk flow V(R), figure `mi_cosmo_fig.png`).

## What was built (A)

Modified-inertia equation of motion mu(|a_pec|/a0)·a_pec = g_pec with the
framework's OWN kernel a_pec = sqrt(g² + g·a0) ⇔ 1/mu = nu(y)=sqrt(1+1/y),
y = g_pec/a0 (not McGaugh's nu). Linearized growth in N = ln a on an
AeST-standard (ΛCDM-like) background:

    delta'' + (2 + dlnH/dN) delta' = (3/2) Ω_m(a) · nu_eff(a) · delta

with **nu_eff = nu(g_rms(a)/a0) evaluated self-consistently at the linear rms
peculiar gravity of the growing mode** (g_rms ∝ D(a)/a², SI-computed from the
Planck-normalized BBKS Δ²(k); D ↔ g_rms iterated to 1e-5, converges in ~17
geometric-mixing iterations). Amplitude anchored at z=200 to the branch that
gives ΛCDM sigma8 = 0.811 (AeST fits the CMB — Skordis–Złośnik 2021,
PRL 127:161302; the banked ghost-condensate Q-mode is the dark sector, so
baryon+condensate = Ω_m feels the MI enhancement).

Key structural fact: the MI kernel has **no analytic linear limit** (nu → ∞ as
y → 0), so "linear" MI growth is amplitude-dependent — consistent with the
banked AeST(=MG) theorem that strictly-linear growth is ΛCDM exact (δq⁰⁰=0);
the MI realization instead gives the quasi-linear amplitude-dependent growth
computed here. This is the classic MOND-structure regime (Nusser 2002,
astro-ph/0109016; cf. Llinares/Angus MOND structure sims).

## Numbers (canonical a0 = 9.36e-11 | alt a0 = 1.13e-10)

ΛCDM reference: g_rms(z=0) = 1.02e-12 m/s² (y = g/a0 ≈ 0.011 → raw nu ≈ 9.6–10.6),
f(0)=0.527, V(35)=333, V(100)=202 km/s (top-hat, BBKS).

| case | sigma8 (vs 0.81) | f(0) | V(35) vs Qin 380 | V(100) vs Qin 410 |
|---|---|---|---|---|
| **SC (spec: pure linear a_pec)** can | **6.90 (8.5×)** | 1.03 | 5508 (**14.5×**) | 3337 (**8.1×**) |
| SC alt | 8.00 (9.9×) | 1.04 | 6469 (17.0×) | 3919 (9.6×) |
| naive V_L×nu(g_R/a0) can/alt | — | — | 4004/4397 (~10.5×) | 3112/3419 (~7.6×) |
| floor_a0 (element g ≥ a0) can/alt | 2.19/2.24 (2.7×) | 0.65 | ~1120 (2.9×) | ~680 (1.6×) |
| floor_cH (total accel ≥ cH_Λ) both | 1.02 (1.26×) | 0.55 | 439 (**1.16×**) | 266 (**0.65×**) |

**Self-consistent dynamics (SC):** growth runs to an attractor where g_rms
locks at ≈ 0.09–0.18·a0 (nu ∝ delta^(−1/2) feedback ⇒ delta ∝ a² in the matter
era; measured exponent 1.63 at a=0.3, nu_eff(z=0) = 3.4, vs the raw 9.6). The
enhancement **saturates at the attractor, not at nu→1**: linear sigma8 reaches
unity already at z ≈ 2.7–3.0, i.e. structure goes nonlinear far too early;
extrapolated sigma8(z=0) = 6.9–8.0.

## Verdict (C): **STILL-OVERSHOOTS — self-consistency does NOT tame the bulk flow**

- The naive ×nu double-count is real and reproduced (nu evaluated at the tiny
  R-scale smoothed g_R ≈ 12–17 → the banked ~10× overshoot). But replacing it
  with the self-consistent element-acceleration treatment does **not** cure it:
  the amplitude feedback is a runaway-to-attractor, leaving V(R) 8–15× Qin 2021
  and sigma8 8.5–9.9× Planck. **On the specified footing (kernel argument =
  peculiar acceleration), MI over-produces large-scale structure — the classic
  MOND-structure problem (Nusser 2002) reproduced inside this framework's own
  kernel.** Both a0 footings agree (spread ~15%, alt slightly worse).
- The **only taming lever found** is the kernel-argument ambiguity: if the
  dS-Unruh argument is the element's TOTAL proper acceleration (floored by the
  cosmological ~cH_Λ = Z·a0 ≈ 5.8·a0), nu_eff ≈ 1.083 and the model lands
  sigma8 = 1.02 (26% high — still a real tension at modern precision) with
  V(35) = 439 vs 380±25 and V(100) = 266 vs 410±80 (~1.8σ low but ABOVE ΛCDM,
  in the direction Qin's high flows want). That variant, however, nearly
  switches MI off in cosmology by construction; the intermediate
  nonlinear-element floor (g ≥ a0, the galactic RAR regime) still overshoots
  (sigma8 ≈ 2.2, V ≈ 1.6–3× Qin). Where the truth sits between "linear g_rms"
  and "total element acceleration" is exactly the unbuilt covariant question.

## First-pass caveats (open, flagged honestly)

Newtonian/quasi-linear MI growth on an AeST background — NOT the covariant MI
perturbation theory. Unbuilt: frame-field perturbations, condensate–baryon
coupling, CMB acoustic physics (nu_eff is already 1.08–1.16 at z=200 on the SC
branch — a covariant treatment must check recombination), fully-relativistic
transfer, scale-dependence of the enhancement (taken scale-independent via the
rms), and the kernel-argument fork (peculiar vs total acceleration) that spans
the whole verdict range above. sigma8 ≫ 1 values are linear-extrapolated
diagnostics; the physical statement is "nonlinear far too early."

Credits: Nusser 2002 (astro-ph/0109016) — MOND linear-growth runaway;
Skordis–Złośnik 2021 (PRL 127:161302) — AeST background/CMB; Llinares, Angus —
MOND structure-formation sims. Qin 2021 points as banked (CF4TF 380@35,
W09 410@100, approximate errors).
