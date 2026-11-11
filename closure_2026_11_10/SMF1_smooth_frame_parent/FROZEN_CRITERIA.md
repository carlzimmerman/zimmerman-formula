# SMF1 FROZEN CRITERIA: the simplest smooth-frame parent (branch B-Tm-smooth), written and graded (2026-11-10)

Committed alone, before any script, derivation output or number. TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), never pooled. The cold
component is cold dark energy, a field (here the complex field Psi), never a particle. Read-only to every other lane
(PAR1, WV1, LFS1, COL1, FLD1, CLS1, QX17, QG1 included). No `PAPER72_*`, `CLOSURE.md` or `fable52_push/README.md` edit.

## 0. Question

PAR1 (origin 6be0bf30d1, A2 a238fb0fba) left one branch with no member written: B-Tm-smooth, a multi-valued cold field
Psi plus a separate single-valued law frame tau that follows Psi's coarse-grained mean flow, with a charge exchange
between Psi's U(1) and the frame's polarization charge (only the sum conserved). PAR1 section 3 says the exchange is
needed because without it "C1 freezes the frame's halo and makes it neutral". This lane writes the simplest member as a
full action and grades it on structure (S0 to S4), then on static data rows (S5) only if the structure holds.

## 1. The member SMF1-M (fixed here, before grading)

### 1.1 Covariant action (units c = 1, K = 4 pi G; restore c as in QX17 section 6)

    S = Int d^4x sqrt(-g) { [R - 2 Lambda]/(4K) + L_A + L_Psi + L_al + L_st + L_x } + S_m[g; baryons]

- **L_A, the frame (action (A) as adopted):** QX17's (A) with the adopted Pi^6 blend stiffness (QX17D):
  L_A = mu_K^2 (Q - 1)^2/(2K) + P^m A_m - W(K|P|) - F_blend(Pi) + lambda n^m P_m, with Q, n, A, Pi as QX17 section 1,
  W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)], F_blend = gamma b^2 f(Pi/b), b = rho_DE, gamma_L = K Lstar^2/2. a0 =
  (1/2) c sqrt(G rho_DE) (kappa = 1/2 FITTED). Unchanged from the record.
- **L_Psi, the cold field:** a complex scalar phi of mass m, minimally coupled:
  L_Psi = -(hbar^2/2m)[g^{mn} d_m phi* d_n phi + (m c/hbar)^2 |phi|^2], normalized so that in the non-relativistic limit
  phi = e^{-i m c^2 t/hbar} psi, psi = sqrt(rho_Psi) e^{i m theta/hbar} (Madelung), with rho_Psi the mass density and
  v_Psi = grad theta. Its U(1) current J^m (phi -> e^{i a} phi) is conserved when L_x = 0. Its charge is the cold dark
  energy, 5.41 x the baryons on FRW (an integration constant, as R541 found).
- **L_al, the alignment:** L_al = -alpha rho_Psi c^2 (gamma_rel - 1), gamma_rel = -n_m u_Psi^m, u_Psi = J/|J| (the
  relative Lorentz factor between the frame normal and Psi's fine-grained current). It is >= 0 in energy and zero iff
  n is parallel to J. alpha is dimensionless.
- **L_st, the frame stiffness (sets ell):** L_st = -(lambda_s/(2K)) (nabla_m n^m)^2, the khronometric lambda term
  (beta stays 0). With L_al it smooths the frame's flow over ell^2 = lambda_s c^2/(4 pi G alpha rho_Psi): the frame
  follows Psi's mean flow averaged over ell.
- **L_x, the exchange:** in the Madelung variables
  L_x = -g_x rho_Psi sin^2(chi), chi = (m/hbar)(theta - phi_f),
  where phi_f is the frame's velocity potential (tau = t - phi_f/c^2 in the Newtonian limit). Covariantly it is
  -(g_x m/(2 hbar^2)) [|phi|^2 - Re(phi^2 e^{2 i m c^2 tau/hbar})] (up to the normalization of phi): the simplest term that
  is analytic in phi, keeps phi = 0 a solution, has energy >= 0 and is invariant only under the diagonal
  (phi -> e^{i a} phi, tau -> tau - a hbar/(m c^2)). So only the sum of Psi's charge and the frame's charge is conserved.
  g_x has units of velocity^2. The frequency m c^2/hbar is fixed by requiring chi = 0 on FRW (not a new constant).

### 1.2 Constants (counted honestly)

Beyond (A)'s (kappa = 1/2 fitted, the 5.41 share as an integration constant, Lstar / gamma_L, mu_K, the blend's b):
**m, alpha, lambda_s, g_x = 4 new constants** (ell is not independent: ell^2 = lambda_s c^2/(4 pi G alpha rho_Psi)).
Initial conditions (not constants): the frame's FRW charge fraction and Psi's share.

### 1.3 The grading form (Newtonian, as COL1 Part 1)

Weak field, gamma_L terms dropped (they are (Lstar/r)^2 ~ 1e-8 at galaxy radii; kept only in the PPN row), P eliminated
by its Legendre maximum (QX17 K0):

    L = mu_K^2 h^2/(2K) + J(|grad h|)                                  [frame; h = -(phi_f,t + |grad phi_f|^2/2 + Phi)]
      - rho_Psi (theta_t + |grad theta|^2/2 + Phi) - (hbar^2/8m^2)|grad rho_Psi|^2/rho_Psi    [Psi, Madelung]
      - (alpha/2) rho_Psi |grad phi_f - grad theta|^2 - (lambda_s/(2K)) (lap phi_f)^2          [alignment, stiffness]
      - g_x rho_Psi sin^2[(m/hbar)(theta - phi_f)]                                            [exchange]
      - |grad Phi|^2/(2K) - rho_b Phi,

J(s) = (a0^2/K)[s/a0 - ln(1 + s/a0)]. The frame charge is N = mu_K^2 h/K + div P with K P = a0 A/(a0 + |A|),
A = -grad h (COL1 R1). Psi's coarse-grained (multi-stream) state is described by its moments; the exchange and alignment
act on the fine-grained field and are coarse-grained explicitly where it matters (S0d).

## 2. Parts and gates

"Exact" = sympy residual 0. "Read" = quoted from the lane named. Each script under 3 GB and a few minutes; outputs small.

### S0, the static coarse-grained galaxy limit (label-setting: S0a, S0b, S0c)

- **S0a (exact reduction).** In a region V_s where the frame is static (phi_f,t uniform, grad phi_f = 0), derive the
  static field equations of the grading form and state rho. PASS iff (sympy residual 0) they reduce to
  div[mu(|grad Phi|/a0) grad Phi] + (A)'s mu_K term = 4 pi G rho with rho = rho_b + rho_Psi + rho_al + rho_x written out,
  and (A)'s law with rho = rho_b holds iff rho_Psi + rho_al + rho_x = 0 there (counted once).
- **S0b (net fill; tests PAR1 section 3 item 4).** Let V be any region whose boundary lies where the frame free-falls
  (A = 0, so P = 0: FRW, or cold single-stream infall to which the frame is aligned). From the member's frame continuity
  equation (with exchange), compute the net transfer of the exchange into the frame's **polarization** charge in V.
  PASS iff some admissible configuration has a nonzero net transfer into the polarization charge (the exchange can fill the
  law's halo in net). FAIL iff that net transfer is identically zero by an exact identity (the halo stays neutral for every
  exchange rate, alignment and ell).
- **S0c (fill where counted once holds).** PASS iff the exchange source S is nonzero somewhere in a region where counted
  once holds exactly (rho_Psi = rho_al = rho_x = 0). FAIL iff S = 0 identically there (the halo cannot be filled where it
  is counted once). Reported with it (not label-setting): the trade between the counted-once violation delta =
  rho_Psi/rho_ph and the fill rate the law needs (LFS1 A1: ln C(t0)/C(t2) = 0.52-0.80), and the data allowance
  delta_max = 5.56/59.5 = 0.093 (SHP1 R4: the record's own share 5.56 M_b allowed on top of the law; the full 59.5 M_b
  excluded).
- **S0d (reported).** The exchange's time-averaged rate in a static, multi-stream (virialized) well: lock condition and
  detuning (the relative phase chi runs at the difference between Psi's energy and the frame's clock rate), as a fraction
  of the single-stream rate, per footing on PAR1 C9's wells.
- **S0e (reported).** If S0b fails: what a counted-once static state then requires (where the conserved cold charge must
  sit, and what can hold it): the Jeans condition for a Psi shell with an empty interior, the frame's dust as a function of
  depth (PAR1 C6), and the angular momentum of Psi created by the exchange; with LFS1 A2's edge charges (read).

S0 PASSES iff S0a, S0b and S0c all pass.

### S1, DOF, ghosts and gradient stability; GW speed; PPN

- **S1-FRW (exact).** The quadratic grading Lagrangian on a homogeneous background (Jeans swindle; Psi dust rho_Psi_bar,
  frame dust n_d = mu_K^2 h_bar/K > 0, aligned, chi = 0): the dispersion determinant in (omega, k) (sympy). PASS iff
  (i) every kinetic coefficient is positive (no ghost), (ii) no branch has omega^2 -> -infinity as k -> infinity
  (no gradient instability), (iii) Psi's large-scale branch is Jeans growth omega^2 -> -4 pi G rho_Psi_bar (+ corrections
  that vanish as k -> 0 or are reported), i.e. Psi clusters like dust. DOF counted: metric 2 (tensor), Psi 1 (Madelung
  pair), frame 1 (QG1), P auxiliary.
- **S1-static (exact / read).** Around the static counted-once galaxy (frame static, Psi absent): Psi perturbations decouple
  at linear order (every coupling is proportional to rho_Psi_bar = 0) and are a free Schrodinger field in Phi; the frame is
  (A)'s (SCS1 / SCS2 STABLE, QG1 PM rows PASS: read). PASS iff the decoupling is exact.
- **GW (exact statement).** The member adds no term with K_ij K^ij, curvature or the beta structure, so c_T = c
  (c_T^2 = 1/(1 - beta), beta = 0). PASS iff true of the action as written.
- **PPN (read + size).** With Psi absent (counted once), the Solar System is (A) + v3s screening (C6 / C6P labels
  unchanged, read). With Psi at the local halo density, the couplings' relative size is reported.
- S1 PASSES iff S1-FRW, S1-static and GW pass.

### S2, FRW

- (a) Psi pressureless at the CMB (its effective sound speed from S1-FRW at z 1100, k = 0.1 per Mpc comoving, is < 1e-3
  of the growth scale's velocity, i.e. c_s^2 k^2 << 4 pi G rho); (b) the frame comoving (A = 0, P = 0) and charged
  (n_d > 0; QG1 "every charged background passes"); (c) the exchange inert on the web (S = 0 at chi = 0 exactly; the
  effective sound speed the lock adds is within the record's forest line c_bar <= 9.20 km/s at z = 3, PAR1 C9).
- (d) The m window: lower edge = max(the record's forest line, PAR1 C15's 4.20e-24 eV; the ell window lambda_dB <= ell <=
  1 kpc at the dispersion of PAR1 C9's wells); C15's upper edge binds B-Tm-fine only. Published forest bounds (2e-21 eV
  and up) are PROVISIONAL, reported, not graded.
- S2 PASSES iff (a), (b), (c) hold and the window (d) is non-empty, per footing.

### S3, PAR1 C16 / C17 evasion (read; hypotheses checked against the action as written)

For each of M5 (non-attractor; self-gravity cancelled), Theorem G, Theorem S, D-T', the mu-pincer, J1, V1: EVADES (a
hypothesis is not met by the member, named), COVERED (every hypothesis met, named), or NOT ESTABLISHED. S3 FAILS iff some
row is COVERED; otherwise PASS with the NOT ESTABLISHED rows listed.

### S4, spherical collapse (label-setting only if S0 to S3 all pass)

If S0-S3 pass: COL1's solver for baryons and law (copied, not edited), Psi as coarse-grained radial multi-stream shells
(collisionless; passes through itself), frame + exchange as in 1.3. Gates: no fold singularity; frame static at SPARC
radii (10 / 30 kpc) by z 0; the halo filled by exchange to PD1's cap amount; FLD1's KiDS windows (362 / 849 kpc, beyond
R_ta) graded as infalling Psi. Preemptible, < 3 GB. If any of S0-S3 fails, S4 runs only its known answer KA3 and is
reported NOT RUN (no state to reach).

### S5, static data rows (only if S0-S4 all pass)

SPARC; KiDS host-free; X-COP and groups (between Newtonian (1 + R) M_b and law + full share; QX28 / XCV1); hosted dwarfs
(RB2 / DG1); SHP1 ("no second halo beside the law"). NOT GRADED otherwise.

## 3. Known answers (each must pass, or the lane label is NO VERDICT)

- **KA1 (PAR1 C1 = LFS1 S1(d)), exact.** With L_x = 0 and L_al = 0 the member's frame continuity in spherical symmetry
  with zero shift gives d_t Y = 0 (Y = r^2 P^r frozen) (residual 0); with L_x on it gives d_t Y = Int_0^R S r^2 dr (stated,
  residual 0).
- **KA2 (PAR1 C5 = T-SCR / TPA1), exact.** With alpha = g_x = lambda_s = 0 and Psi absent, the frame's linear response
  around free fall is omega^2 = -K n_bar K chi/(K chi + k^2) with chi = mu_K^2/K, i.e. TPA1's K n_bar/(1 + k^2/mu_K^2)
  growth (residual 0).
- **KA3 (COL1 fold time).** With alpha = g_x = 0 and Psi absent, the member is COL1's system. COL1's solver (imported
  read-only; outputs written in this folder) at mu_K 0.1 per Mpc, J 1200, Hubble mode: the fold time after the mass appears
  matches COL1's recorded value to relative 1e-3 at log M_b 10.45 and 9.4, both footings (COL1 runs/, canonical / alt:
  0.082331 / 0.082340 Gyr at 10.45 and 0.153217 / 0.153230 Gyr at 9.4).

## 4. MUTATE twins (each must bite, or the lane label is NO VERDICT)

- **MU1 (S0b):** keep the frame static (A = g, P != 0) on the boundary of V instead of free-falling. The net transfer into
  the polarization charge must become nonzero.
- **MU2 (S0c):** replace L_x by a non-analytic V(chi) not multiplied by rho_Psi. S must become nonzero where rho_Psi = 0.
- **MU3 (S1):** flip the sign of alpha (anti-alignment) and of g_x. A gradient instability or negative-energy branch must
  appear.
- **Lean twin:** `SMF1_MUTATE.lean`, false versions of `SMF1.lean`'s statements, must fail to compile.

## 5. Lean

`SMF1.lean`: the algebraic cores of S0b (a telescoping flux sum with zero end values is zero), S0c (S = g rho s is zero at
rho = 0), the Jeans empty-core sign step (S0e), the constants count (4 >= 3), and any numeric inequality S2 or S0d
relies on. Compile: `cd fable_independent_2026/lean_2026 && lake env lean <file>`; standard axioms only.

## 6. Labels (per footing)

- **WORKS ON EVERY GRADED GATE:** S0 to S5 all pass.
- **STRUCTURE HOLDS, DATA FAIL (name the gate):** S0 to S4 pass; some S5 row fails.
- **STRUCTURE FAILS (name the part and give the theorem or number):** the first failing part in the order S0, S1, S2, S3,
  S4. S0 to S3 are all evaluated and reported whatever S0 gives.
- **NO VERDICT:** a known answer fails, a MUTATE twin does not bite, the Lean file does not compile, or a needed part
  cannot be evaluated.

A pass under any post hoc amendment needs a blind regrade before anyone folds it into a paper. Amendments are post hoc,
each committed alone and disclosed in RESULT.md.

## 7. Process and files

- Scripts: `smf1_sym.py` (S0a-c, KA1, KA2, S1, MU1-MU3 via `SMF1_MUTATE=MU1|MU2|MU3`), `smf1_num.py` (S0d, S0e, S2
  numbers, per footing), `smf1_ka3.py` (KA3), `smf1_grade.py` (labels). `SMF1.lean`, `SMF1_MUTATE.lean`.
- Inputs read (read-only): PAR1 `par1_numbers.json` (C9 wells, forest line, C15), LFS1 `lfs1_num.json` (A1 rates, A2 edge
  charges), COL1 `runs/` (KA3 references) and its solver modules.
- Commit with explicit paths only; push by replaying commits onto origin/main with merge-tree + commit-tree.
- RESULT.md leads with the label per footing, then the action with every constant counted, then the table, then commit
  ids (local / origin).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
