# SMF1 RESULT: the simplest smooth-frame parent, written and graded (2026-11-10)

**Label, canonical and alt: STRUCTURE FAILS / STRUCTURE FAILS. The first failing part is S0.**
- **S0b (exact, Gauss):** the exchange cannot fill the law's halo in net. Take any region whose boundary lies where the
  frame free-falls (P = 0). The frame's polarization charge in that region is zero at every time, for every exchange rate,
  alignment and ell. In net the exchange feeds only the frame's dust part and the boundary fluxes.
- **S0c (exact, starvation):** where the halo is counted once (rho_Psi = 0), the exchange source is identically zero.
  So the halo cannot grow there, and LFS1's C1 freeze returns.
- S0a holds exactly: in a static-frame region the member's equations give (A)'s law with rho = rho_b + rho_Psi. S1, S2
  and S3 pass as frozen. S4 was not run, because S0 leaves no counted-once state to reach (only its known answer KA3 was
  run). S5 was not graded.

**Wave-specific or not (AMENDMENT A1, post hoc, section 5).** Neither failing gate is wave-specific. S0b (Gauss) and S0c
(starvation) do not depend on the carrier being a wave. A **collisionless** (kinetic, multi-stream, non-wave) carrier in
the same B-Tm-smooth structure does not escape either one: S0b's identity contains no carrier variable, and a kinetic
loss term is zero where the carrier's density is zero (C1, C2, Lean). So this result also decides the collisionless
member at S0. The reported stiffness band is not wave-specific either: its quantum cutoff is, and a cold collisionless
carrier loses it (section 5).

Every known answer passes (KA1 LFS1's frozen Y; KA2 T-SCR; KA3 COL1's fold time, reproduced to relative difference 0).
Every MUTATE arm bites. `SMF1.lean` compiles (9 theorems, standard axioms) and all 6 of its false twins fail.

**Answer in plain words.** The parent PAR1 left open cannot be built the way PAR1 specified it. PAR1 section 3 item 4 says
the charge exchange is needed because otherwise "C1 freezes the frame's halo and makes it neutral". The exchange does
remove the freeze, but only where Psi is present, and Psi present means the halo is not counted once. It cannot remove
the neutrality at all. Neutrality is Gauss's theorem: the law's halo is the divergence of P, and P vanishes wherever the
frame falls freely, which on the web it must. So the halo's positive charge is always matched by an equal negative
layer where the static region ends (LFS1 A2's -34 to -68 M_b at R_ta). What the exchange can do is move Psi's charge from
inside the halo to that edge. For the result to be counted once and to have no wall, the real cold charge C(R_s) must
then sit in the edge layer and be held there. This member has nothing that can hold it (S0e):
- Psi made by the exchange is phase-locked to an irrotational frame, so it carries no circulation.
- Accreted Psi has about 1/20 of the spin a rotation-supported shell needs (PROVISIONAL citation).
- The frame's own dust is a function of depth, largest at the centre (PAR1 C6).
- No isotropic pressure can hold a hollow shell (Lean `jeans_empty_core`).

S0b uses only that the halo is the frame's polarization charge and that the frame comoves (A = 0) on the web. So it holds
for every member of B-Tm-smooth as PAR1 wrote the branch, not just this one. A re-specified branch, with the halo as the
image of a held edge layer of real cold charge, is not graded here.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled: a0 enters the well
depths, the law's dispersion and LFS1's edge charges. Cold dark energy is a field (Psi), never a particle.

## 1. The member, written out (FROZEN_CRITERIA.md section 1, fixed before grading)

    S = Int d^4x sqrt(-g) { [R - 2 Lambda]/(4K) + L_A + L_Psi + L_al + L_st + L_x } + S_m[g; baryons]      (c = 1, K = 4 pi G)

| piece | term | constants |
|---|---|---|
| frame (action (A) as adopted) | L_A = mu_K^2 (Q - 1)^2/(2K) + P^m A_m - W(K\|P\|) - F_blend(Pi) + lambda n^m P_m (QX17 (A), QX17D Pi^6 blend, b = rho_DE) | (A)'s: kappa = 1/2 (fitted), Lstar / gamma_L, mu_K, b |
| cold field | L_Psi = -(hbar^2/2m)[g^{mn} d_m phi* d_n phi + (m c/hbar)^2 \|phi\|^2]; NR: psi = sqrt(rho_Psi) e^{i m theta/hbar}; its U(1) charge is the 5.41 x baryons (an integration constant) | **m** |
| alignment | L_al = -alpha rho_Psi c^2 (gamma_rel - 1), gamma_rel = -n_m u_Psi^m (>= 0, zero iff n parallel to Psi's current) | **alpha** |
| frame stiffness | L_st = -(lambda_s/(2K)) (nabla_m n^m)^2 (khronometric lambda; beta = 0); ell^2 = lambda_s c^2/(4 pi G alpha rho_Psi) | **lambda_s** |
| exchange | L_x = -g_x rho_Psi sin^2 chi, chi = (m/hbar)(theta - phi_f); covariantly -(g_x m/2hbar^2)[\|phi\|^2 - Re(phi^2 e^{2 i m c^2 tau/hbar})]; invariant only under the diagonal (phi -> e^{ia} phi, tau -> tau - a hbar/(m c^2)) | **g_x** (the frequency m c^2/hbar is fixed by chi = 0 on FRW) |

**Constants beyond (A): 4 (m, alpha, lambda_s, g_x).** ell is not independent. The spec asked for at least 3. Initial
conditions: Psi's share and the frame's FRW charge fraction.

**rho (S0a, exact):** in a static-frame region, div[mu(|grad Phi|/a0) grad Phi] + mu_K^2 (Phi - c0) = 4 pi G (rho_b + rho_Psi).
The alignment and exchange energies are O(v^2/c^2) of rho_Psi c^2 and do not source Phi at Newtonian order. So (A)'s
law with rho = rho_b (counted once) holds iff rho_Psi = 0 there.

## 2. The theorems (sympy residual 0 unless stated; `smf1_sym.out`)

- **E1.** The Euler-Lagrange equations of the grading form are two continuity equations:
  d_t N + div F_f = S_f and d_t rho_Psi + div F_Psi = -S_f, with S_f = (g_x m/hbar) rho_Psi sin 2(m/hbar)(phi_f - theta).
  Here N = mu_K^2 h/K + div P (the frame charge), F_f = N grad phi_f + alpha rho_Psi (grad phi_f - grad theta)
  - (lambda_s/K) grad lap phi_f, and F_Psi = rho_Psi grad theta - alpha rho_Psi (grad phi_f - grad theta).
  Only the sum is conserved. Residual 0 for any J.
- **S0b (Gauss).** Integrated over a ball:
  Int_0^R S_f r^2 dr = d/dt Int_0^R (mu_K^2 h/K) r^2 dr + d/dt[R^2 P(t,R)] + R^2 F_f(t,R).
  With a regular centre and a free-falling boundary (P(t,R) = 0 at all t), the net transfer into the polarization charge
  is exactly 0. The 3D check without symmetry (a P vanishing on the faces of a cube) gives 0. Lean: `gauss_zero`,
  `exchange_net_zero`.
- **S0c (starvation).** S_f is proportional to rho_Psi, so it is 0 at rho_Psi = 0 (Lean `starvation`). With the frame
  static, the frame equation is r^2 S_f = -(g_x m/hbar) r^2 rho_Psi sin(2 m t (E - c0)/hbar): a stationary state needs
  rho_Psi = 0 or a locked phase.
- **KA1.** With L_x = L_al = 0, mu_K = 0 and zero shift, the frame equation is d_r d_t Y = 0 (Y = r^2 P^r), so Y is frozen:
  PAR1 C1 = LFS1 S1(d). With L_x on, d_t Y(R) = Int_0^R S_f r^2 dr.
- **KA2.** The frame alone around free fall gives omega^2 = -K n_d mu_K^2/(mu_K^2 + k^2) (T-SCR / TPA1).
- **S1-FRW.** The determinant is A w^4 + B w^2 + C with A = k^2 (k^2 + mu_K^2)/K^2 > 0. At k -> 0 the growing root is
  exactly -K (n_d + rho_Psi): Psi clusters like dust with the total cold density (Lean `jeans_root`). As k -> infinity the
  small root tends to -lambda_s mu_K^2, which is bounded, and the large root grows like hbar^2 (1 + alpha) k^4/(4 m^2).
  All unmixed energy coefficients are positive. Around the static counted-once galaxy (psi = 0) a psi-frame cross term is
  at least cubic, so the two decouple at linear order. GW: no K_ij K^ij, curvature or beta term, so c_T = c.
- **Reported, not label-setting as frozen: the stiffness has the destabilizing sign.**
  - The growing root is -K (n_d + rho) + c1 k^2 + ..., with c1 = -lambda_s + K hbar^2 n_d^2/(2 g_x m^2 rho + hbar^2
    mu_K^2 (n_d + rho)) (residual 0; Lean `c1_split`).
  - lambda_s > 0 is what makes ell^2 > 0. At the khronometric alpha = 2 point the frame then gives Psi a negative sound
    speed squared, cut off only by Psi's quantum pressure.
  - At z = 3, with ell = 1 kpc at a 10 kpc halo density, the growth rate peaks at 6.3 times Jeans (m 2.3e-22 eV) and
    18 times Jeans (2e-21 eV) at k ~ 0.3 to 0.75 per kpc physical. With ell = 0.1 kpc the peaks are 1.1 and 2.5 times.
  - At z = 1100, k = 0.1 per Mpc, the effect is below 1e-6 (`smf1_num.out`).
  - Any successor member needs a smoothing stiffness that does not do this.

## 3. Table

| part | canonical | alt | numbers |
|---|---|---|---|
| KA1 LFS1 frozen Y (exchange off) / supply (on) | PASS | PASS | residuals 0 / 0 |
| KA2 T-SCR (alignment, exchange off) | PASS | PASS | residual 0 |
| KA3 COL1 fold time (alignment, exchange off) | PASS | PASS | log M_b 10.45: 0.082331 / 0.082340 Gyr; 9.4: 0.153217 / 0.153230 Gyr; relative difference 0 |
| MU1 static boundary | bites | bites | net transfer = R sqrt(a0) dM_b/dt/(4 sqrt(pi K M_b)) != 0 |
| MU2 non-analytic exchange | bites | bites | S_f at rho_Psi = 0 = -(g_x m/hbar) V'(chi) != 0 |
| MU3 flipped alpha, g_x | bites | bites | negative energies; gradient instability |
| Lean `SMF1.lean` / `SMF1_MUTATE.lean` | exit 0, 9 theorems, standard axioms / exit 1, 6 of 6 false statements fail | | |
| **S0a** reduction, rho = rho_b + rho_Psi | PASS | PASS | residual 0 |
| **S0b** net fill of the polarization charge | **FAIL** | **FAIL** | identically 0 (Gauss); NOT wave-specific, collisionless does not escape (A1 C1) |
| **S0c** fill where counted once holds | **FAIL** | **FAIL** | S_f = 0 at rho_Psi = 0; NOT wave-specific, collisionless does not escape (A1 C2) |
| S0c trade (reported) | | | delta = rho_Psi/rho_ph for the law's growth (LFS1 A1: 0.025-0.028 per Gyr at z 0, 0.24 at z 2): locked Psi 2e-6 to 1.4e-4; unlocked, band-averaged, needs sqrt(g_x) >= 14-24 km/s (z 0) and 24-41 km/s (z 2) for delta <= 0.093 (SHP1); alt within 4 % |
| S0d detuning (reported) | | | in the graded wells (120-364 km/s), chi runs with a period of 0.04-8 Myr, which is 5e3 to 1.6e6 cycles per fill time; lock band g_x/depth = 6e-4 to 0.006 at g_x = cbar^2 and 0.07 to 0.7 at (100 km/s)^2. Locked Psi is single-valued (PAR1's B-Ts) |
| S0e edge (reported) | | | real charge needed in the edge layer at R_ta: 61.5 / 40.9 / 37.1 / 34.3 M_b (alt 67.7 / 45.0 / 40.9 / 37.7; LFS1 A2, read); frame dust at mu_K = 1 per Mpc covers 0.6-9 %; a rotation-held shell needs spin 0.71 against about 0.035 (20 x short, PROVISIONAL) |
| S1 FRW / static / GW | PASS | PASS | Jeans root -K(n_d + rho) exact; small root -> -lambda_s mu_K^2; static decoupled (cross term order 3); c_T = c |
| S2 (a) CMB, (b) frame comoving and charged, (c) exchange inert, (d) m window | PASS | PASS | (a) 1 to 1e-6; (b) A = P = 0 by isotropy, n_d > 0 given mu_K > 0 and a positive FRW frame charge; (c) S = 0 at chi = 0, lock sound speed 0.002 km/s at z 3 (line 9.2); (d) [2.28e-22, inf) eV canonical, [2.17e-22, inf) alt (lambda_dB <= 1 kpc at the law's sigma), published forest bounds inside, PROVISIONAL |
| S3 C16 / C17 | PASS | PASS | M5, Theorem G, Theorem S, mu-pincer, J1: EVADES (named hypothesis not met); D-T', V1: NOT ESTABLISHED |
| S4 collapse | NOT RUN | NOT RUN | S0 fails; KA3 run |
| S5 static rows | NOT GRADED | NOT GRADED | |
| **Label** | **STRUCTURE FAILS (S0)** | **STRUCTURE FAILS (S0)** | |

## 4. Disclosures

- **Development runs before the graded run.**
  - The first `smf1_sym.py` stalled in sympy's simplification of the full radial equations with the explicit log-form J,
    and was killed after about 10 minutes. No number came from it. E1 and KA1 now use a generic J (the identities hold
    for any J), and the explicit J enters only the static S0a check.
  - S0b's first integration of generic functions raised a sympy error. It now uses the fundamental theorem on an opaque
    flux W = r^2 P.
  - The full dispersion stalled in sympy's root and limit step. S1 now works from the coefficients A, B, C (exact
    limits), plus a numeric sweep.
  - A "frame held rigid" Psi branch was dropped before grading. Holding the frame fixed is unphysical here, because the
    law's term cancels gravity's gradient energy.
  - Two dead lines were removed. A rerun gave identical JSON, runtime excluded.
- **S2(b) "charged"** is conditional: n_d = mu_K^2 h_bar/K > 0 needs mu_K > 0 and a positive FRW frame charge, which is
  an initial condition. "Comoving" is exact by isotropy.
- **S3 is read.** No theorem was re-derived. D-T' and V1 are NOT ESTABLISHED. The exchange lock is a local hold that D-T'
  may cover.
- **The S0c trade and S0d are estimates.** The band-average model assumes that the fraction of Psi within g_x of the
  frame's rate is g_x/depth. The reference parameters of the stiffness band (alpha = 1, ell at a 10 kpc halo density,
  n_d = 0.01 rho, mu_K = 0.1 per Mpc, g_x = cbar^2) are choices, not fits.
- **Citations.** The spin 0.035 (Bullock+2001) and the published forest bounds (2e-21 eV and up) are PROVISIONAL: quoted
  from memory, not fetched.
- **Scope of the reduction.** The Newtonian grading form drops gamma_L terms ((Lstar/r)^2 ~ 1e-8 at galaxy radii) and
  W, as COL1 did. The PPN row is not computed: with Psi absent the Solar System is (A) plus v3s (C6 / C6P, read).
- **KA3** imports COL1's solver read-only and writes nothing in COL1's folder.

## 5. AMENDMENT A1 (post hoc): which gates are wave-specific, and does a collisionless carrier escape?

A1 was requested by the coordinating session after the result and committed alone (local cfa91d3feb) before its checks
were written or run. It changes no criterion, gate or label. Here "wave-specific" means failing because the carrier is
a wave: nodes, interference fringes, the de Broglie core against the law's a0/(2 pi G r), quantum pressure, phase
locking, or the ultralight mass window. Checks: `smf1_a1_collisionless.py` -> `.out` / `.json` (under 1 s) and
`SMF1_A1.lean` (3 theorems, exit 0, standard axioms; its false twin `SMF1_A1_MUTATE.lean` fails on 3 of 3, exit 1).

| item | status | wave-specific? | would a collisionless carrier in the same structure escape? |
|---|---|---|---|
| **S0b** net fill (Gauss) | FAIL | **NOT** | **No.** C1: with a kinetic carrier the frame's source is the loss term Int gamma f dv. The balance contains no carrier variable, and the net transfer into the polarization charge with a free-falling boundary is exactly 0 |
| **S0c** starvation | FAIL | **NOT** | **No.** C2: S = n Int gamma g dv = n/2 for the test shape, so S = 0 at n = 0. Lean `kinetic_starvation`: f_i >= 0 and Sum f_i = 0 give Sum gamma_i f_i = 0 for any rates. MA1 bites: a sign-indefinite f with zero density loses sqrt(pi)/2. For point particles a local action cannot change their number at all |
| S0a, rho = rho_b + rho_carrier | PASS | NOT | the same reduction |
| S0d detuning and lock (reported) | reported | **WAVE-SPECIFIC** | does not apply: there is no phase |
| S0c trade (reported) | reported | its rate model (lock, band average) is WAVE-SPECIFIC | a kinetic loss rate gamma gives delta >= (d ln C/dt)/gamma (stated, not graded) |
| S0e held edge layer (reported) | reported | NOT (empty-core Jeans step, accreted-spin shortfall, frame depth-dust). The "irrotational exchange product" item is wave-specific | a kinetic source could deposit carrier with a velocity spread, but the empty-core and spin items still apply |
| S1 stiffness band (reported) | reported | the -lambda_s term is NOT; its quantum cutoff is | **Escapes only if warm enough.** C3 is a fluid stand-in (g_x = 0, isothermal sigma^2). It gives c1 = sigma^2 rho/(n_d + rho) - lambda_s + K n_d^2/(mu_K^2 (n_d + rho)) (residual 0; Lean `c1_collisionless`). The growing branch saturates at omega^2 = -lambda_s (K rho + mu_K^2 sigma^2)/sigma^2 (residual 0), which is about sqrt(lambda_s)/sigma times the Jeans rate. A cold carrier (sigma -> 0) has an unbounded band. At sigma = 9.2 km/s (the forest line) the band is removed only for ell <= 0.67 kpc (alpha = 1); at ell = 1 kpc the saturated rate is 1.49 x Jeans |
| S2(d) m window | PASS | **WAVE-SPECIFIC** | does not apply |

**In one line:** the S0 failure is structural (Gauss plus positivity), not a wave artefact, so a collisionless member
of B-Tm-smooth fails S0 the same way. Such a member would also need a velocity dispersion near the forest line, with
ell <= 0.67 kpc, to keep the frame's smoothing stiffness from driving growth faster than Jeans.

A1 disclosures:
- In the first run of `smf1_a1_collisionless.py`, C3's comparison target left out the weight rho/(n_d + rho) on
  sigma^2, giving a residual of -n_d sigma^2/(n_d + rho).
- Its printed large-k sentence ("a gradient instability with no cutoff") was written before the limits were computed.
  The computed limit is a bounded saturation for sigma > 0.
- Both were corrected before this section was written. The exact c1 expression the script derives did not change.
- C3 is a fluid stand-in for a kinetic carrier, not a Vlasov computation.
- Compute: every A1 job ran single-thread at nice 19, one at a time, while BX1's run was live.

## Files and re-run

`FROZEN_CRITERIA.md` (alone, first). Run in order: `python3 smf1_sym.py`;
`SMF1_MUTATE=MU1|MU2|MU3 python3 smf1_sym.py`; `python3 smf1_num.py`; `python3 smf1_ka3.py`; `python3 smf1_grade.py`.
Each takes a few seconds and well under 1 GB. Lean: `cd fable_independent_2026/lean_2026 && lake env lean
../../closure_2026_11_10/SMF1_smooth_frame_parent/SMF1.lean` (logs in `compile.txt`, `compile_MUTATE.txt`). A1:
`AMENDMENT_A1.md` (alone, post hoc); `nice -n 19 python3 smf1_a1_collisionless.py`; `SMF1_A1.lean`, `SMF1_A1_MUTATE.lean`
(logs `compile_A1.txt`, `compile_A1_MUTATE.txt`).

Commits (local / origin): criteria 9586b716e6 / b3879c6cad; result 8339a435fe / 884ddfb854; ids d52635e2a4 / 92a8ce5f0e;
A1 cfa91d3feb / 10e7d72ac3 (alone); A1 result d074525445 / 92a0855574.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
