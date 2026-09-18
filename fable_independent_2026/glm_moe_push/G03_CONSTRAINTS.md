# G03_CONSTRAINTS.md

> **STATUS BOX**
> G03 is the derivation door: a covariant completion reproducing the framework's (Gamma, eta) response law. This document is the constraint set it must satisfy — a checklist, not a theory. The ghost quadratic-form theorem is the remaining kill gate; alpha_2 is priced (SW08). The words derived/closed/breakthrough are not used as claims.

Status semantics, used throughout:

- **HARD** = the completion fails without it.
- **OPEN** = the completion must supply it.

Every item is cited to a landed check under this directory (`SW01b` = `SW01b_envscalar_orthogonality.out`, `SW04` = `SW04_conformal_efe.out`, `SW07` = `SW07_eta_c_attack.out`, `SW08` = `SW08_preferred_frame.out` (+ `SW08_preferred_frame_MUTATE.out`), `SW09_meanvalue` = `SW09_meanvalue.out`, `SW10_pair` = `SW10_pair.out`). Nothing here is a Lagrangian; this is a checklist, not a theory.

---

## The constraints

**G1 — Uniform field ⇒ Gamma == 0 exactly.**
A uniform environment field has zero fluctuation on the sphere; it cannot move Gamma. The orthogonality theorems hold by quadrature, and the DC/AC split confirms Gamma is invariant under a uniform environment while eta absorbs it.
Citation: `SW01b_envscalar_orthogonality.out` C1/C2 (orthogonality theorems, computed by quadrature; critic fixes C1/C2); `SW09_meanvalue.out` C1 (UNIFORM environment: eta absorbs it, Gamma INVARIANT — Gamma 1.688593599329 vs isolated 1.688593599329, rel 1.31e-16).
Status: **HARD**

**G2 — Isolated barycentered ⇒ Gamma = |g_N|, eta = 0.**
The isolated point mass on a centered sphere must return the bare Newtonian response: eta = 0 and Gamma = g_N.
Citation: `SW01b_envscalar_orthogonality.out` C1 — isolated point mass, centered sphere: eta = 0, Gamma = g_N (quadrature; eta = 5.55e-17).
Status: **HARD**

**G3 — Conformal pointwise scaling Q(R) = S * Q_iso(R).**
The conformal scaling relation must hold pointwise, not just on average, in the conformal Einstein-frame-equivalent (EFE) sector; the eBTFR algebra v^4 = S^2 G M_b a0 rides on it (sympy-certified in the same artifact; DR4 run gamma_v 1.00000–1.01012 vs AQUAL 1.17462).
Citation: `SW04_conformal_efe.out` B1 — class vs isolated, max |BR_class/BR_isolated − 1| = 2.22e-16 (S cancels pointwise; AQUAL shows 0.446 for contrast).
Status: **HARD**

**G4 — Barycenter centering is load-bearing.**
The decentered mutant (the same construction with the barycenter condition dropped) is PPN-dead by ~1.9e6x (tight) / ~1.9e4x (conservative). The centering condition is not a convenience — the construction fails PPN without it, so the completion must implement the barycenter-centered sphere, not a dropped-centering trigger.
Citation: `SW08_preferred_frame_MUTATE.out` B4[MUTATED] — decentered preferred-frame estimate = 0.76, PPN-dead (mix_frac 0.33 x eta_sun 2.29); FAIL IS THE FINDING.
Status: **HARD**

**G5 — The matter-frame coupling c_S must sit inside the priced bound.**
The coupling the G03 Hessian's matter-frame sector contributes is the named missing input; the bound is stated in terms of S(eta_sun):
c_S <= 4.23 (Nordtvedt 4e-7) / <= 423 (LLR-scale 4e-5).
Citation: `SW08_preferred_frame.out` B5[KILL-A] — the bound G03 must satisfy, stated in terms of S(eta_sun); the coupling is the named missing input.
Status: **HARD**

**G6 — No l >= 2 anisotropy at planetary x.**
The induced planetary preferred-frame anisotropy must be zero at measurable level: 0.00e+00 (doubly suppressed — trigger anisotropy 6.09e-06 x |dS/dln eta| 0.016 x response; quadratically suppressed, a structural pass).
Citation: `SW08_preferred_frame.out` B4 — induced PLANETARY preferred-frame anisotropy = 0.00e+00 (doubly suppressed).
Status: **HARD**

**G7 — Causal / retarded completion: the retarded kernel is UNSUPPLIED.**
The instantaneous NR sphere functional is observationally silent at NR scale — crossing/orbital = 1.94e-07 for wide binaries (s = 1e4 AU; t_cross = 57.8 d, P_orb = 8.16e+05 yr) and crossing/dynamical = 3.34e-05 for classical dSphs (r = 300 pc, sigma = 10 km/s; t_cross = 978.4 yr, t_dyn = 2.93e+07 yr). That silence is why the instantaneous functional survives today's data — but it does not supply causality. The retarded kernel is the completion's job and is UNSUPPLIED: no causal (retarded) completion exists in this swing (C4 FAIL-as-finding).
Citation: `SW08_preferred_frame.out` C1/C2 (the silence numbers), C4[KILL-B] (FAIL-as-finding: no causal completion in this swing; "the retarded completion is G03's job and is OPEN").
Status: **OPEN**

**G8 — Ghost quadratic-form theorem.**
The quadratic form of the completion's scalar ghost sector must be shown healthy (the theorem establishing the ghost's quadratic form / its non-ghostliness in the covariant action). This is the remaining kill gate: without it, the completion is dead regardless of every other item on this list.
Citation: none yet — no landed check exists for this item in this swing; that is precisely why it is the remaining kill gate.
Status: **OPEN**

**G9 — The obstruction: (Gamma, eta) are NOT functions of any finite 2-jet at the field point.**
Theorem 2 (`SW10_pair`): two configurations sharing the EXACT 2-jet of g at the field point P (|g|, |J|,... all matched, differences 0.00e+00) while Gamma moves. Corollary in the same artifact: the equal-|g| pair kills mu(|g|) separately — the local trigger mu(|g_N(P)|) is blind to what the sphere functionals see. Therefore the completion's Gamma must be computed by boundary coupling on the sphere, or by an auxiliary field carrying the constraint — NOT by any local differential expression.
Citation: `SW10_pair.out` C/PAIR 1 — the 2-jet kill (H4 centered at the field point P): jets identical while Gamma moves.
Status: **HARD**

**G10 — The two measured constants the completion must reproduce.**
1. a0 = 0.5 c sqrt(G rho_Lambda) — i.e. kappa = 0.5 (a0 = 9.3619e-11 m/s^2 canonical; MEASURED 0.465 ± 0.076 / 0.551 ± 0.043); the kappa slot is adjudicated NOT LIVE (KS01); four candidates sit inside 2σ.
2. eta_c in [0.145, 0.203] — the Fornax-implied ceiling <= 0.145 (from below, SW03 C2) to the Oort ceiling <= 0.203 (from above, L263 C1), with LSS floor >= 0.028 (SW01b F) and the deep-window requirement (P4: eta ≈ 2–3.5 must stay unsuppressed, automatic for any eta_c in the window). SW07: every derivation mechanism in the priced class is KILLED (H1/H2 coherence volume category-III, stiffness width a fit, kernel reuse cited, tidal/self eta_c = 1.66e-05 — four orders below the window and RAR-lethal, the S-form an ansatz (H5), numerology convention (H6: 1/6 checks PASS)). The completion must reproduce both constants by whatever mechanism it supplies.
Citation: `LAW_STATEMENT.md` (the two measured constants: kappa = 0.5, KS01 slot NOT LIVE; eta_c bounded Oort <= 0.203 / Fornax <= 0.145, window is the measurement); `SW07_eta_c_attack.out` (every priced mechanism KILLED; eta_c = the SECOND MEASURED CONSTANT; the derivation door is the G03 sourced-sector action).
Status: **HARD**

**G11 — Photon cone ⇒ the metric split must be screened or absent.**
Any completion that splits photon and graviton metrics (photons on g~ = e^{2 phi} g, gravitons on g) is killed by the GW170817 differential Shapiro delay along the NGC 4993 sightline: the photon-graviton arrival difference is >= 1e5 x the observed 1.7 s (>= 1e4 x a 10 s emission budget), on both footings and kernels, eta_ext 0.01-0.1 — and the local cone mismatch at the Sun, |c_gamma - c|/c = 2|phi(Sun)|, exceeds 1e-15 by >= 8 orders. The conformal factor drops out of the null cone (the photon dispersion g~^{mu nu} k_mu k_nu = 0 is e^{-2 phi} x (g^{mu nu} k_mu k_nu) = 0): the photon cone must be g's — light bending by the baryons only — or the split must be screened.
Citation: `kappa_slot_2026/SW06_lensing_trilemma_quadrature.out` checks 1a/1b/1c/2a (7/7 PASS; the record's horn-B kill, sign as observed — the kill is on magnitude alone, 5-7 orders).
Status: **HARD**

**G12 — alpha_1 ⇒ gravitomagnetism or deep-Newton suppression.**
The fable SW04 theorem: gamma = 1 without gravitomagnetism gives alpha_1 = -8(nu_S - 1)/nu_S. The completion must supply gravitomagnetism (a gamma != 1 structure) or keep nu_S - 1 ≈ 0 at planetary x. The class supplies the latter structurally: S(eta_sun) = 0.0078 → nu_S - 1 ≈ 0 at planetary x (the double suppression, SW08 B4). The smoothed-total-switch action (the fable SW03) fails it: alpha_1~ = -1.4 to -2.1, 1e4-2e4 x the bound; cancellation needs c14 < 0 tuned to the Sun's eta.
Citation: `kappa_slot_2026/SW04_ppn_full.out` (the symbolic PPN, the alpha_1 theorem, the l-scan no-window); `SW08_preferred_frame.out` B4 (the double suppression at planetary x).
Status: **HARD**

---

## What G03 must DELIVER

- **The action with the sourced-sector coupling** — the covariant action whose Hessian's matter-frame coupling c_S satisfies G5 (<= 4.23 / <= 423, SW08 B5) and whose Gamma is computed by boundary coupling on the sphere or by an auxiliary field with the constraint (G9).
- **The ghost quadratic-form theorem** (G8) — the remaining kill gate; no landed check exists yet.
- **The retarded kernel** (G7) — currently UNSUPPLIED (SW08 C4 FAIL-as-finding); the instantaneous functional's NR silence (1.94e-07 WB, 3.34e-05 dSph) is what it must supersede without breaking G1–G6.
- **The alpha_2 coupling within the bound** (G5) — priced, not supplied: the coupling itself is the named missing input of SW08 B5[KILL-A].

## What G03 must NOT do

- **No local differential trigger** — G9. The (Gamma, eta) variables are provably not functions of any finite 2-jet at the field point (`SW10_pair.out`: jets identical while Gamma moves); any local differential expression for Gamma is dead on arrival. Gamma must come from boundary coupling on the sphere or from an auxiliary field carrying the constraint.
- **No eta_c derivation from the priced class** — SW07. Every derivation mechanism in that class is killed (H1–H6; 1/6 checks PASS, the S-form an ansatz, tidal/self four orders below the window and RAR-lethal). The completion must supply a mechanism outside that class that lands eta_c in [0.145, 0.203].
