# Ghost condensate as the framework's dark sector: AMOUNT + PATHOLOGIES (2026-06-19)

Primary sources pulled verbatim this session (PDFs extracted with pdfplumber):
- **ACLM** = Arkani-Hamed, Cheng, Luty, Mukohyama, *Ghost Condensation and a Consistent IR
  Modification of Gravity*, hep-th/0312099 (JHEP 0405:074, 2004).
- **VSB** = Verwayen, Skordis, Boehm, *AeST: Quasistatic spherical solutions*, arXiv:2304.05134
  (MNRAS 531:272, 2024).
- **SZ21** = Skordis, Zlosnik, *AeST: Linear stability on Minkowski space*, arXiv:2109.13287
  (PRD 106:104041, 2022).
- **Mukohyama 2005**, *Black Holes in the Ghost Condensate*, hep-th/0502189.

Calc: `amount_and_pathologies_calc.py` (this dir, runs clean).

---

## (a) AMOUNT — does the ghost condensate PIN Omega_dm?

**NO. The dust amplitude is a free symmetry-breaking offset / integration constant. Only the
dark-ENERGY face is pinned by Lambda; the dark-MATTER (w=0) amplitude is free.** The ghost
condensate has TWO faces, ACLM's own (Eqs 3.1, 3.2):

- **On the attractor** (P'(c^2)=0): T_munu -> -g_munu M^4 P(c^2), i.e. **w=-1** = cosmological
  constant. ACLM Eq 1.11: if the GC drives today's acceleration, rho_DE ~ M^4 ~ (1e-3 eV)^4 =>
  **M ~ 1e-3 eV**. Calc reproduces M = (rho_DE)^(1/4) = 2.24e-3 eV. This face IS ~pinned by Lambda
  — and it is EXACTLY the framework's banked a0 <-> Lambda tie (the dark-ENERGY unification),
  nothing new for the dark-MATTER amount.
- **Off the attractor** (ACLM Eq 3.2): P'(phidot^2) ~ 1/a^3 => T_00 ~ M^4 P', T_ij=0 =>
  **sources gravity like NON-RELATIVISTIC MATTER (w=0 dust)**. ACLM verbatim: *"the ghost
  condensate may contribute to dark matter as well as the vacuum energy."* This IS the
  framework's "temporal Q-mode = dark matter." But the amplitude is the **offset from the
  attractor** = a free initial condition. In AeST language: shift symmetry => first integral
  `a^3 K'(Q) = I0`; `d rho_dust/d Lambda = 0` (Lambda enters K only as the additive -2Lambda).

**Verdict (a):** the ghost condensate does NOT pin Omega_dm ~ 0.26. M^4 (the P(X) curvature) sets
the overall SCALE, ~Lambda; the dust amplitude I0 rides the orthogonal OFFSET and is a free
boundary datum. The why-now ratio Omega_dm/Omega_L = 0.387 is epoch-dependent, so it cannot be a
constant of the a-independent dS vacuum, and AeST's scalar is pure a^-3 dust with no
tracker/attractor to pin it. **This is IDENTICAL to the banked AeST result** (I0 free) — the
ghost-condensate reading adds the *mechanism* (it is the symmetry-breaking offset) but changes
nothing about the amount being free. Zero-free-numbers stays FALSE; one free amplitude conceded.

---

## (b) PATHOLOGIES — the honest cost, and whether de Sitter / AeST cures them

### Pathology timescales (ACLM Eqs 1.10, 7.10; calc table)

| scale | M (eV) | r_c=M_Pl/M^2 | t_c=M_Pl^2/M^3 | Gamma=M^3/4M_Pl^2 | H0/Gamma |
|---|---|---|---|---|---|
| DE (ACLM 1.11) | 1e-3 | 1.6e7 kpc (~H0^-1) | 1.2e32 Gyr | 6.4e-50 s^-1 | **3.4e31** |
| AeST (mu=1/Mpc) | 0.15 | 707 kpc | 3.8e25 Gyr | 2.1e-43 s^-1 | **1.0e25** |
| 10 MeV (ACLM upper) | 1e7 | 1.6e-13 kpc | 124 Gyr | 6.4e-20 s^-1 | **34** |

### Pathology 1: Jeans-like IR instability — CURED by de Sitter (this is the GATE EVASION too)

ACLM dispersion (Eq 7.8): `omega^2 = alpha^2 k^4/M^2 - (alpha^2 M^2/2M_Pl^2) k^2`. For `k < m =
M^2/(sqrt2 M_Pl)`, `omega^2 < 0` => Jeans instability, growth rate (Eq 7.10) `Gamma =
alpha M^3/(4 M_Pl^2)`. **ACLM Sec 8 (Eqs 8.19-8.24): in de Sitter with `H > Gamma`, the
instability is REMOVED by Hubble friction — the potential decays as `Phi ~ e^{-Ht}` ("they decay
at least as fast as the redshifting so there is no growing potential").** For EVERY relevant M,
H0/Gamma >> 1 (table: 3e31 at the DE scale, 1e25 at AeST's scale, even 34 at the 10 MeV ceiling).
**The framework LIVES in a de Sitter universe (Lambda>0) — exactly the regime ACLM prove stable.**
This is a real, double-duty result: the framework's dS foundation is *what makes the ghost
condensate's worst pathology benign.* (It is also why this could break wall 1: the dS *background*
is doing the stabilizing work — a *condensate solution* in a dS universe is healthy where the dS
*vacuum* could not induce the field.)

SZ21 confirm the residual in AeST: the only possibly-unstable mode is the **non-propagating
omega=0 Y-mode** with linear-in-t growth, unbounded Hamiltonian only for `k < k_* ~ mu`. SZ21
verbatim: *"Such instabilities are likely akin to Jeans-type instabilities and do not cause
quantum vacuum instability at low momenta."* And `mu^-1 >~ Mpc` on observational grounds (else
no galaxy MOND), so `k_* <~ Mpc^-1`: *"such instabilities do not occur in the GR limit of the
AeST for all systems of interest."*

### Pathology 2: antigravity / oscillatory force — pushed beyond observed scales (AeST: by mu)

ACLM Eq 1.9: E_grav ~ M^2 pidot, linear in pidot => lumps of pi gravitate OR **antigravitate**
depending on sign. The Newtonian potential becomes oscillatory at `r > r_c ~ M_Pl/M^2`, onset
time `t_c ~ M_Pl^2/M^3`. At M~1e-3 eV: `r_c ~ H0^-1` and `t_c >> H0^-1` (Eq 1.11) — *"no
modifications of gravity can be seen directly, and no cosmological experiment can distinguish the
ghost-driven acceleration from a cosmological constant."* In **AeST** the oscillation is a SPATIAL
feature: VSB Eq 11 is *literally* the GC weak-field Poisson eq `grad^2 Phi + (1+beta0) mu^2 Phi =
4 pi G rho_b` (VSB say so 3x verbatim: *"also results from the non-relativistic weak-field limit
of the Ghost condensate model"*). Oscillation onset `r_C ~ (r_M/mu^2)^{1/3}`; VSB Fig 4:
mu={0,1,10} Mpc^-1 -> r_C={inf,156,33.6} kpc. **Choosing mu small (mu^-1 >~ 1 Mpc) pushes the
oscillatory/antigravity regime beyond galaxy disks.** Cost: **mu is a FREE parameter, squeezed in
OPPOSITE directions by galaxy weak-lensing (wants mu^-1 large) vs clusters** — the banked
signature of a free constant, not a derived scale.

### Pathology 3: accretion onto massive bodies — benign (dust-like, not catastrophic)

Mukohyama 2005 (hep-th/0502189): the ghost condensate **accretes onto a black hole like
pressureless dust** — a finite, slow `dM/dt`, NOT a runaway antigravity blow-up. ACLM: turning
on pi gravitationally "requires long distances and time scales"; the spin-dependent 1/r force
needs a *direct* SM coupling (optional, forbiddable by a phi->-phi symmetry) and its static limit
is valid only on `tau >~ M r^2` (Eq 5.9). No solar-system catastrophe.

### Pathology 4: w=0 only at leading order — true, and it is a FEATURE here, not a bug

ACLM: w=-1 on the attractor (Eq 3.1), w=0 off it (Eq 3.2); gradient/curvature corrections give
small `c_s^2 k^2` pieces (Eq 6.22, the `M_tilde^2 K_ij^2` terms). For the framework's dust mode
this is fine: AeST fits Planck incl. the 3rd peak *because* the dust is cold (c_s^2 ~ 0
sub-horizon); the small gradient corrections are what make AeST's CMB transfer differ slightly
from pure CDM — a falsifiable feature, not a pathology.

### Pathology 5: strong coupling — the EFT cutoff is M itself; UV completion needed (shared with all of MOND/AeST)

ACLM: the leading operator is irrelevant, so there is a controlled IR EFT, but it *"need[s] to be
embedded in a UV completion above"* the scale `Lambda_c ~ M`. The coupling strength `lambda =
Lambda/M`; ACLM work in the window `1e-3 eV < M < 10 MeV`. This is NOT a fatal flaw — it is the
generic statement that AeST/ghost-condensate is an EFT with a UV cutoff (same as the framework's
own quarantine: it is a one-parameter EFT at a frontier, not a UV-complete TOE).

### AeST's specific form — does it avoid them? The STABILITY WINDOW (SZ21 Eqs 61-63)

SZ21 ghost-free + positive-sound-speed conditions (the "Skordis-Zlosnik stability window"):
> **0 < K_B < 2 (61);  mu^2 > 0 (62);  lambda_s > 0 (63)** — "These conditions also imply G_N > G̃
> always." Propagating vector AND scalar modes are massive with **c_s = c** (LIGO-safe), Hamiltonian
> bounded below.

Two things make AeST's form *more* stable than the bare ghost condensate:
1. **mu^-1 >~ Mpc** pushes both the residual Jeans-type k<mu instability AND the antigravity
   oscillation onto cosmological/super-galactic scales.
2. **The nonlinear MOND term `J_NL ~ (2 lambda_s/3(1+lambda_s)a0)|Y|^{3/2}` actively stabilizes
   the residual mode** SZ21 verbatim: *"the nonlinear MOND term creates a nontrivial minimum in
   the Hamiltonian density, so [it is stabilized]."* The framework's OWN MOND function (the
   Y^{3/2} term carrying a0) is what closes the last stability gap the linear analysis left open.

---

## BOTTOM LINE (both ways)

**Amount:** NOT pinned. M^4 ~ Lambda fixes the dark-ENERGY scale (= the banked a0<->Lambda tie),
but the w=0 dust amplitude is the free symmetry-breaking offset / integration constant I0 ~
Omega_dm. The ghost condensate adds the *mechanism* for the dust (off-attractor P'~1/a^3) but
leaves the amount free — identical to the banked AeST conclusion.

**Pathologies:** NONE is fatal for use as the framework's dark sector, given the framework's own
de Sitter background + AeST's window. The Jeans IR instability is **removed by Hubble friction in
de Sitter (H>>Gamma by 25-31 orders)** — ACLM's own result, and it is the same dS background that
makes the gate-evasion plausible. Antigravity oscillation is pushed beyond galaxies by mu^-1 >~
Mpc (FREE parameter, squeezed by data — the honest cost). Accretion is dust-like/benign. w=0 is
leading-order with small cold-dust gradient corrections (a CMB feature, not a bug). Strong
coupling at M needs a UV completion (shared EFT caveat). AeST's J(Y)/K(Q) form satisfies a
3-condition stability window {0<K_B<2, mu^2>0, lambda_s>0} and its nonlinear MOND term actively
stabilizes the residual mode.

**Net for wall 1:** the ghost-condensate reading is a GENUINE upgrade of the *mechanism* (the
dark sector is the symmetry-breaking offset of a Lorentz-violating condensate; the dS background
cures the Jeans pathology), with a real partial gate-evasion (the condensate SOLUTION + dS
BACKGROUND together do what the dS VACUUM alone could not). But it does NOT pin the amount and
does NOT remove the free parameters — it relocates "why this amplitude" to "what is the
symmetry-breaking offset / IC," which is still free. Honest line held: viable window EXISTS, no
fatal pathology, amount FREE.
