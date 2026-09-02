# CCNL-MOND — Condensate-Clock Nonlocal MOND: the fried-chicken candidate (2026-09-02) — **DEAD at gate 7 (same night)**

> **2026-09-02, later the same night.** The owed in-in phase-space item was computed at linear order on a MOND background
> (`ccnl_inin_linear_scalar_2026.py`, `NONLOCAL_KERNEL_LINEAR_INSTABILITY_VERDICT.md`): the retarded kernel's scalar sector has a
> longitudinal gradient instability for y ≳ 0.5 (Im ω = 0.2–0.5 ck, driven by f″, absent transversely, present for DW's own f) and a
> negative-energy mode in the deep-MOND window. **CCNL fails gate 7; so does Deffayet–Woodard's kernel; the nonlocal door is closed at
> this level.** Everything below stands as computed and is now the record of how the last door was walked through and found shut.


**Status: a single explicit action that clears every known killer of every earlier candidate on every gate a local
Lagrangian can compute, with 29 committed checks passing (`ccnl_mond_gates_2026.py`, rc=0, output in `.out`; `MUTATE=1`
breaks A2). Gate 2 is passed in its honestly restated form 2′ (the strict form is unsatisfiable by the banked universal
dark-field theorem) — and, for the kernel sector, ONLY under the in-in (Schwinger–Keldysh) definition of the nonlocal
theory: an independent action-level Dirac audit run the same night (`CCNL_ACTION_DIRAC_VERDICT_2026-09-02.md`) shows the
ordinary localised action carries a ghost-signed auxiliary pair. That in-in phase space is the decisive owed item. This
is the strongest candidate the programme has produced; it is not declared closed.**

## The action

$$S=\int d^4x\sqrt{-g}\;\Big\{\frac{c^4}{16\pi G}\big[R+a_0^2 f(Z)\big]\;+\;\frac{K(Q)}{8\pi\tilde G}\;+\;\xi\big(\Box X-R_{\mu\nu}u^\mu u^\nu\big)\Big\}\;+\;S_m[g,\psi]$$

| piece | definition | role |
|---|---|---|
| clock | $\phi$ shift-symmetric; $Q=\sqrt{-g^{\mu\nu}\partial_\mu\phi\,\partial_\nu\phi}$; $u_\mu=\partial_\mu\phi/Q$; $K(Q)=-2\Lambda+K_2(Q-Q_0)^2$ (v9 DBI has the same quadratic term) | the preferred frame for lensing, the dark energy, and the dust: a $\gamma=2$ polytrope with $c_s^2=\lvert\Psi\rvert c^2$ in wells (item C) |
| kernel | $X=\Box^{-1}_{\rm ret}(R_{\mu\nu}u^\mu u^\nu)$ localised by the multiplier $\xi$ with null initial data; $Z=(4c^4/a_0^2)\,g^{\mu\nu}\partial_\mu X\partial_\nu X$ | the MOND force, carried by a retarded nonlocal operator (no local scalar graviton, no aether) |
| interpolation | $f_{\exp}(Z)=4-2(\sqrt Z+2)e^{-\sqrt Z/2}$ (odd continuation for $Z<0$) | gives $\mu(y)=1-2f'(4y^2)=1-e^{-y}$ exactly |
| matter | minimal coupling to the one metric $g$ | gate 5, 11 |

It is Deffayet–Woodard 2026 (arXiv:2512.10513) with two changes: the mimetic clock $(\partial\phi)^2=-1$ and its
advected dust $M(0)=45/\sqrt{\det g}$ are replaced by the condensate clock $K(Q)$ (so the dark field is the
polytrope of item C), and DW's transport functional $M$ is not used: the action contains $f(Z)$ directly. (If one keeps
DW's transport, null data for $X$ give $f_0=0$, so $M_0=0$ implies $M=-f$ exactly along every flow tube; the audit's
formula $M=-f+(n_0/n)f_0$ reduces to this.)

## Why this and not the others — each killer, and the computed mechanism that dodges it

| earlier candidate | its killer (committed) | how CCNL dodges it | check |
|---|---|---|---|
| AeST / v9 (+c₂,c₄) | $\alpha_1=-2(K_B+2)$ from the aether drag $(2-K_B)(2J\!\cdot\!\partial\phi-Y)$, un-tunable | no aether vector; the MOND force is the retarded kernel, multiplied by $f'\sim e^{-y}$, $y\sim10^{11}$ in the Solar System | C1–C4 |
| every local 2-DOF constraint carrier (CDE-L4C, MMG, York) | $\alpha_3=O(1)$: an instantaneous second-class constraint | retarded $\Box^{-1}$: $\omega$-dependent response, $\alpha_3=0$ | C3 (structure, nonlocal-door verdict) |
| frame-free $F(X)$ scalar | $O(1)$ slip (DC-013; slip-lock theorem) | the clock supplies the frame; the kernel enters through $R_{uu}$; its anisotropic stress $f'\partial_iX\partial_jX$ is 2PN | G1 |
| Deffayet–Woodard as written | mimetic dust is geodesic and pressureless: CDM halo in galaxies, RAR shifted 0.06–0.24 dex | condensate dust with $c_s^2=\lvert\Psi\rvert$: 0.001 dex at the same cosmic share | A1–A3 |
| DW's retarded-by-hand equations | conservation "not Euler–Lagrange" (open since 08-31) | the localised action is diffeomorphism-invariant: off-shell Noether identity verified; retardation is a choice of solution | D1–D2 |
| nonlocal localisation ghost | $(X-\xi)/\sqrt2$ has negative kinetic sign (sf43) | linear in $X,\xi$ ⇒ unique retarded functional for any metric history; nonlinear minisuperspace integration confirms slaving and conservation | I1–I5 |

## The 13 gates

| # | requirement | status | evidence |
|---|---|---|---|
| 1 | exact MOND with $\mu=1-e^{-y}$; deep-MOND $v^4=GMa_0$; galaxies not contaminated by the dark field | **PASS (computed)** | B1–B5 (the $f\leftrightarrow\mu$ map, derived; $f_{\exp}$ exact), A2–A3 (galaxy RAR shift ≤ 0.001 dex at the full cosmic share) |
| 2 | $N_{\rm grav}=2$ | **strict form: unsatisfiable (theorem, banked 09-01)**; **2′: PASS under the in-in definition** (2 tensor + 1 explicit healthy clock + auxiliaries as retarded functionals with no data); **FAIL as an ordinary local action** (the $(X,\xi)$ pair has $W=[[-4e^{-y},1],[1,0]]$, $\det W=-1$: two modes, one ghost-signed, free data) | F1–F2 (clock), I1–I5 (retarded solution self-consistent at nonlinear order), sf44 (linear in-in count = GR's), the 09-02 Dirac audit (ordinary action) |
| 3 | $\Phi=\Psi$, correct lensing | **PASS** | G1 (slip $\le 8f'(v/c)^2<10^{-5}$ in galaxies); DW eq. 22 structure; slip-lock escape via the clock frame |
| 4 | full PPN derived | **PASS**: $\gamma-1=-e^{-y}$, $y=10^{12}$ at Cassini; $\beta-1$ same exponential; $\alpha_{1,2}<10^{-25}$ from the only unscreened frame coupling (the clock fluid's stress); $\alpha_3=0$ | C1–C4; residual: the full boosted extraction of the kernel sector beyond the $e^{-y}$ suppression bound (cannot change the verdict by 10¹¹ orders) |
| 5 | $\nabla_\mu T^{\mu\nu}=0$ as an identity | **PASS (computed)** | D1 (off-shell Noether identity, machine precision, two $f$'s), D2 (control fails), I3 (constraint conserved dynamically to $10^{-10}$) |
| 6 | $c_T=c$, positive tensor kinetic term, 2 polarisations | **PASS** | E1–E3 (kernel tensor-blind; $K(Q)$ metric-algebraic through $Q$) |
| 7 | stability | **PASS for the clock; kernel sector PASS only under the in-in definition** | F1–F4, I2–I5; the ordinary local action's ghost-signed auxiliary is the same object as sf43's; residual: the in-in phase-space construction, then the 3+1 nonlinear PDE system |
| 8 | expanding FLRW, not by freezing | **PASS (background exact; linear by bound)** | H1 (kernel a constant on FLRW, −2% of $\rho_\Lambda$, absorbed), J1–J2 ($c_s^2=2.9\times10^{-8}$ at recombination, 30× under the UDM bound); residual: a CLASS run of this exact action |
| 9 | controlled $y\to0$ | **PASS at the AQUAL level; crossing prescription owed** | H2 ($\mu\to y$); the audit notes $f_{\exp}$ is $C^1$ but not $C^2$ at $Z=0$ ($f''\propto Z^{-1/2}$, the deep-MOND $Z^{3/2}$ non-analyticity shared by every MOND function incl. DW's), so the cosmology→bound crossing at $Z=0$ needs a stated prescription |
| 10 | Newton/GR recovery, $G_N$ | **PASS** | H3 ($\mu\to1$ exponentially, no $(1+J_Y)/J_Y$ renormalisation) |
| 11 | one physical metric | **PASS** | by construction |
| 12 | exponential constitutive law | **PASS** | B4 ($f_{\exp}$), B6–B7 (the forced offset $a_0^2/4\pi G=\rho_\Lambda/16\pi$, a 2% regime-dependent vacuum term, stated) |
| 13 | $a_0=c^2\sqrt{\Lambda/32\pi}$ | **INPUT** ($\kappa$ fitted; no derivation exists, `A0_PROMOTION_VERDICT.md`) | — |

Both footings ($a_0=9.36\times10^{-11}$ canonical, $1.13\times10^{-10}$ alternative) at every numerical gate.

## Independent action-level audit (2026-09-02) — credited, and what it changes
A parallel agent audited the displayed action (`ccnl_action_dirac_audit_2026.py`, `test_…`, manifest, verdict, in this
directory). It confirms the exact exponential law (B4) and finds: (i) as an ORDINARY local action the $(X,\xi)$ kinetic
block is $[[-4e^{-y},1],[1,0]]$ with $\det=-1$ — no auxiliary Dirac constraints, two auxiliary modes, one ghost-signed;
retarded null data selects a history but is not an equal-time constraint, so I1–I5 prove self-consistency of the chosen
solution, not absence of the others; (ii) the trace-free source $f'(\partial_iX\partial_jX-\tfrac13\delta_{ij}|\nabla X|^2)$
means exact nonlinear $\Phi=\Psi$ is not derived (only the 1PN statement G1); (iii) the PPN suppression numbers bound but do
not extract $\beta,\alpha_{1,2,3}$; (iv) $f_{\exp}$ is $C^1$, not $C^2$, at $Z=0$. Its scope statement: the result kills CCNL
*as the displayed ordinary localised action* under a strict ban on hidden auxiliaries, and does not exclude a genuine
in-in construction, which "is not presently in the repository" — note this contradicts the earlier Codex claims sf47/sf48
(CTP local equivalence) for DW; that disagreement is not resolved here. Point (i) is the one that moves a gate.

## What is still owed (the honest residual)

0. **The in-in phase space (gates 2′/7, kernel sector) — decisive.** Define the theory by its causal in-in field
   equations with $X,\xi$ as retarded functionals of $g$ (Deser–Woodard's definition), and derive its physical phase
   space, unitarity and causal variation without treating retarded history data as canonical constraints. This is the
   same open item for DW 2026 and for every nonlocal gravity model; the ordinary local action is not the theory.
1. **Gate 7, kernel sector, 3+1.** The auxiliaries $X,\xi$ obey equations linear in themselves, so the retarded
   solution with null data is unique on any globally hyperbolic background; this is verified at nonlinear order
   in the lapse minisuperspace (I1–I5). The inhomogeneous 3+1 nonlinear PDE run has not been done.
2. **Gate 8, linear cosmology.** The clock dust passes the unified-dark-matter sound-speed bound by 30× and its
   Jeans length at recombination is sub-Mpc (J1–J2), so it is CDM-like at linear order. A CLASS run of this exact
   action (no aether) is the confirmation; v9's CLASS run included the aether.
3. **Gate 4, kernel sector.** The preferred-frame parameters from the kernel are bounded by $e^{-y}$ with
   $y\sim10^{11}$; the exact boosted extraction has not been carried out. No prefactor can matter.

Also stated: the cluster core is not closed by this theory (item C: 23–33% of the residual; the shape binds);
the lever lives at $\mu^{-1}\approx1$ Mpc, which is a choice of $K_2Q_0^2$; gate 13 is input.

## Priority
The kernel is Deffayet–Woodard's (2011–2026); the clock sector is Skordis–Złośnik's Q-sector; the polytrope reading
of that sector is item C; the assembly, the $f_{\exp}$ solution of the $\mu$-inverse problem, the Noether/retarded
resolution as stated, and the galaxy-dust contrast are new here as far as searched (2026-09-01 ledger).

## Reproduce
```bash
cd qwen_claude_field_theory/closure_2026/candidate_ccnl_2026
python3 ccnl_mond_gates_2026.py          # 29 checks, rc=0 (~7 min; Part I is a nonlinear ODE integration)
MUTATE=1 python3 ccnl_mond_gates_2026.py # A2 fails (the galaxy comparison uses the mimetic numbers)
```
Quarantine: $a_0$, $\kappa$, $I_0$ (the clock's cosmic charge), $K_2Q_0^2$ (the polytrope scale) are inputs.
