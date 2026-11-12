# THEORY (FINAL-1, 2026-11-11): form B, written as a formation theory

An assembly. It grades nothing new about nature. Every claim below carries the lane it comes
from, and where this file and a lane's own RESULT.md differ, the lane is right.
**kappa = 1/2 FITTED; not theory closed. Adopts nothing.**
Footings never pooled: a0 = 9.3603e-11 (**canonical**) and 1.1312e-10 (**alt**) m/s^2.
G = 6.6743e-11 SI, c = 299792458, K = 4 pi G, Z = 2 sqrt(8 pi/3) = 5.7888.
Arithmetic recomputed here in SI: `final1.py` -> `final1.out` (primary) and `final1_MUTATE.out`.

**Why this form.** The diagnostic landed before this lane ran: the settled halo cannot be cold
charge that fell in (T4 + LFS1 cap delivery at 1.06-1.40 M_b; lensing demands 41.5-97.8 M_b at
FLD1's window edges), and the missing-baryon escape is closed on both exits (GAS1). His data prefer
the formation reading — the amount is real, conserved, and **SET WHEN A SYSTEM FORMED** (HIS1: 4 of 5
frozen statements; HIS1R regraded with separate code: same label) — over the force reading
(1 of 5). So this is that reading, written out.

---

## 1. The ontology, in plain words

**What there is.**

1. **One spacetime metric** g_mn. Ordinary matter couples to it and nothing else.
2. **A clock sector**: a scalar field tau (the khronon). It is not a substance you can hold; it
   picks out a slicing of spacetime — the surfaces tau = const — with a unit normal n_m, a rate
   Q = sqrt(-g^{mn} d_m tau d_n tau), and a conserved charge carried along n.
3. **A polarization P^m** on the clock's slices (P^m n_m = 0). The clock sector's response to
   baryons lives here.

**The one sentence that matters: there is no dark-matter particle.**

There is no new particle, no new fluid of particles, no cold relic. The "dark mass" that shows up in
rotation curves, in galaxy-galaxy lensing and in clusters is **the clock sector's own
stress-energy**. It is a field component. It gravitates because its stress-energy stands in
G_mn; it lenses for the same reason, and for no other. It is not made of anything that could be
detected in a laboratory.

**What the sector's energy density is** [C: QX17 K5]:

    rho_c = (mu_K^2 / 2K)(Q^2 - 1) + W(K|P|) + Pi + gamma_L F(Pi),   Pi = D_m P^m

In the weak field it splits into two pieces on **one** conserved charge:

    rho_c = D.P + n_d ,     n_d = mu_K^2 (Q - 1) / K

- **D.P** is the halo: the bound polarization charge sitting around baryons.
- **n_d** is the clock's dust: the same charge in the state where it just falls with the
  expansion.
- **"Counted once" is exactly this statement in equations**: they are not two components, they
  are one charge in two states.

**What it is not.** It is not a gas of particles: the stress that holds the settled halo is
anisotropic, and in the deep field it is **Pi_rr = −Pi_tt exactly**, so the radial "dispersion" is
**negative**, sigma_r^2 = −v_inf^2/2 with v_inf^4 = G M_b a0 [C: FB1 note; recomputed here].
No kinetic gas can do that. It is also **not a local elastic solid**: the material stress is
sigma = −Pi with mu_s = +(3/2) J (rho_ref/(3 rho_c))^(1/3), which is local, momentum-conserving
and normally self-gravitating, so **M5's NO-GO bites**, and the solid yields at the Bullet
(Mach 7-22, yield parameter 76-478) and melts in clusters [C: ELA1]. The negative sigma_r^2 is a
statement about the sector's **stress**, not about anything's velocity.

**Where the sector sits.** In the expanding universe it is dust: P = 0 by symmetry, and the charge
per comoving volume is constant, n_d a^3 = const — 5.41 times the baryons [C: CO1, R541]. Around
assembled baryons the clock stands still, and the charge takes the law's shape: M_c(<r) = M_b X(x),
X(x) = (sqrt(1 + 4 x^2) − 1)/2 [C: SHP1, QX17].

**What is set when, and what never changes.** The cold charge N of a closed comoving region is
conserved: it is not manufactured while the clock free-falls (**T4**, exact, any momentum
equation) and it does not grow once the clock stands still (**LFS1**, exact, changes only by
O(|Phi|/c^2) ~ 1e-6). What is *fixed at formation* is the **ratio** X_f = M_C,f / M_b,f. Afterwards
only transport moves it.

---

## 2. The action

One term per line. Everything in the bulk is the record's certified action (A) (QX17); the new
content is the assembly hypersurface, the rule imposed there, and the transport bookkeeping.

    S = Int sqrt(-g) {
                                                        ---- bulk ----
      R / (4K)                                                              [FROM (A)]
    - Lambda / (2K)                                                         [FROM (A)]
    + (mu_K^2 / (2K)) (Q - 1)^2                      the clock's dust    [FROM (A)]
    + P^m A_m                       polarization x the clock's acceleration [FROM (A)]
    - W(K|P|)                       the law's own potential                 [FROM (A)]
    - gamma_L F(Pi)                 the fold / screening term                [FROM (A)]
    + lambda n^m P_m                the constraint n.P = 0                  [FROM (A)]
                                                        ---- the new part ----
    + delta(Sigma_f) [ zeta ( J^m n_m - X_L(g_b; a0) rho_b u^m n_m ) ]     [NEW - the
        assembly rule: on Sigma_f the cold charge is pinned to the law's
        value at the formation field.  Not a bulk term: an initial condition.]
    + Int sqrt(-g) theta_K A_m T^m_trans                                    [NEW - transport:
        the charge leaves or enters only by crossing the system's boundary.
        Gives f_C; f_b is the baryons' own transport.]
    }  +  S_m[g; baryons, photons, neutrinos]                                [FROM (A)]


    W(p)     = (a0^2 / K) [ -p/a0 - ln(1 - p/a0) ]                      [FROM (A)]
    F(Pi)    = [max(Pi, 0)]^2 / 2 ,   gamma_L = K Lstar^2 / 2             [FROM (A)]
    Q        = sqrt(-g^{mn} d_m tau d_n tau)                                 [FROM (A)]
    n_m      = -d_m tau / Q ,   A_m = n^n nabla_n n_m ,   Pi = D_m P^m        [FROM (A)]
    J^m      = n^m rho_Q - lambda P^m / Q                                    [FROM (A), E3]
    X_L(g)   = ( sqrt(1 + 4 a0/g) - 1 ) / 2      the law's ratio          [FROM (A)]
    a0       = kappa c sqrt(G rho_Lambda) = c H_Lambda / Z                  [FROM (A), FITTED]

**New objects, one line each.**

| tag | new object | what it does | where the definition comes from |
|---|---|---|---|
| **N1** | **Sigma_f**, the assembly hypersurface | the surface on which the amount is fixed: where the clock's expansion along n first reaches zero going into collapse | fold at 0.52 R_ta (FLD1); settling shock at 0.51 R_ta (VSH1), every mass, both footings, since z = 4.96 / 3.45 / 1.46 |
| **N2** | the **assembly rule** Q | X_f = M_C,f/M_b,f = X_L(g_b,f); i.e. rho_c,f = (1/K) div[(1 - mu(g_b,f/a0)) grad Phi_b,f] on Sigma_f | the law's static branch (QX17), evaluated at formation, not today |
| **N3** | **transport** (f_C, f_b) | charge and baryons cross the boundary; X = X_f (f_C/f_b) | T4 + LFS1 (no bulk source or sink) |
| **N4** | **g_b,f** | one constant of integration per system: the formation field. Not a term — a label | disclosed as such by FRM1 (§ "What it does not settle") |

**The structural point, stated once: no bulk term is new.** Every term inside the volume integral is
FROM (A). The formation reading therefore *inherits* everything (A) delivers and everything (A)
fails to deliver — it does not repair a single gate by adding dynamics. It changes only **which
solution of (A) a region is on, and what normalisation that solution carries**. What the data say
is that the normalisation is not what a transport story would give (CRUX) and is what a formation
story gives (HIS1 4/5, FRM1 14/16).

**Why N1 is not the closed door.** Keying a *dust stiffness* on the clock's expansion is dead
(TK1: BREAKS AT TURNAROUND — a collapsing region passes through zero expansion while its clock is
still falling, and there short waves grow without bound). Keying an *initial condition* on the zero of
the expansion is a different object: it never enters the field equations, so TK1's instability has
nothing to act on. N1 uses the zero of the clock's expansion only to say **when** to impose N2.

---

## 3. The conserved quantity, and the epoch at which the amount is fixed

**The conserved quantity.** The cold charge of the clock sector, on the current [C: QX17 (E3)]

    J^m = n^m rho_Q - lambda P^m / Q ,
    rho_Q = nabla_m[(1 + gamma_L Pi_+) P^m] / Q  +  mu_K^2 (Q - 1) / K ,
    nabla_m J^m = 0 .

In the weak field, for a comoving region V,

    N(V) = Integral_V ( D.P + n_d ) dV   =   M_C(V) ,

the non-baryonic mass in V. Baryons are a second, separately conserved charge. **Both are
non-negative — that is where the floor comes from.**

**What is conserved, in one line each:**

| statement | status | lane |
|---|---|---|
| no polarization charge is manufactured inside a free-fall-bounded ball, at any time, for any momentum equation | **exact** | T4 (SMF1 S0b) |
| once the clock is static, the polarization is frozen; the halo's charge changes only by O(\|Phi\|/c^2) ~ 1e-6 | **exact** | LFS1 |
| therefore the halo's charge is an **initial condition**, not an advected quantity | **exact consequence** | CRUX, R541 |

**The epoch.** The amount is fixed on **Sigma_f**, defined as the hypersurface where the clock's expansion
along its own normal first vanishes going into collapse — the fold. This is a physical, label-free
surface, it exists at every mass on both footings, and it has been located: the fold sits at 0.52 of
the turnaround radius (FLD1) and the clock settles behind a shock at 0.51 of it (VSH1), since
z = 4.96 / 3.45 / 1.46.

**What is fixed there** is the **ratio**, not the mass:

    X_f  =  M_C,f / M_b,f  =  X_L( g_b,f ; a0 )
          = ( sqrt(1 + 4 a0/g_b,f) - 1 ) / 2

The epoch does **not** rescale the law. a0 = (1/2) c sqrt(G rho_DE) with rho_DE constant (w = −1),
so the same a0 fixes the amount at every epoch. The epoch enters only through the field g_b,f at
which the ratio was pinned, and through the time available for transport. A system that settled and
transferred nothing has g_b,f = g_bar and sits on the law today: that is the anchor, and it holds
with no free parameter (FRM1 F5).

**After Sigma_f, the master equation governs everything** [C: FRM1, with its own disclosures]:

    X  =  X_f ( f_C / f_b ) ,
    d  =  log10[ ( 1 + X_L(g_b,f) f_C/f_b ) / ( 1 + X_L(g_bar) ) ] ,
    d  ~  (1/2) log10( g_bar / g_b,f )  +  log10( f_C / f_b )        (deep regime)

| channel | what moves | sign of d |
|---|---|---|
| **S** stripping of the charge (f_C < 1, f_b = 1) | charge leaves | negative |
| **B** baryon loss (f_b < 1, f_C = 1; the field falls with the baryons) | baryons leave | **positive — the only upward channel** |
| **A** late baryon accretion (f_b > 1, f_C = 1) | baryons arrive | negative |
| none (f_C = f_b = 1, g_b,f = g_bar) | — | zero (the anchor) |

Two structural consequences, both pre-registered and both graded: **the floor** X ≥ 0 (neither
charge can be negative), and **the ceiling** — baryon loss saturates, because with f_C = 1,
X = X_L(u f_b)/f_b rises as f_b falls but tends to u = a0/g_bar. No amount of baryon loss can
lift a system above

    d_max(u) = log10[ (1 + u) / (1 + X_L(u)) ]

---

## 4. The field equations

**FROM (A), certified in QX17:**

- **(E1)** n^m P_m = 0.
- **(E2), the law.** On the leaves: (1 + gamma_L Pi_+) A_m + gamma_L D_m Pi_+ = K W'(K|P|) Phat_m.
  At gamma_L = 0: K|P| = a0 u/(1 + u), u = |A|/a0. Eliminating P gives J(|A|) = (a0^2/K)[u − ln(1+u)] [C: QX17 K0].
- **(E3), conservation.** nabla_m[ n^m rho_Q − lambda P^m / Q ] = 0, with rho_Q as in §3.
- **(E4), gravity.** G_mn + Lambda g_mn = 2K ( T^matter + T^Q + T^W + T^P ), stresses as printed in QX17.
- **(E5), baryons.** Minimal coupling: baryons fall on geodesics. No fifth force, no switch, no wall.
- **(E6)** The sector's stress is conserved on shell; the Bianchi identity holds.

**The static weak field, any geometry** [C: QX17; TPA1 4.5]:

    K P = (1 − mu) grad Phi ,     mu(u) = u/(1 + u) ,     u = |grad Phi| / a0
    div[ mu grad Phi ] + mu_K^2 Phi = K rho_b
    rho_c = D.P + n_d ,           n_d = − mu_K^2 Phi / K        (static clock)
    Poisson:  lap Phi = K ( rho_b + rho_c )

The halo is held by the law's own stress **[H: FB1 note]**,

    Pi_ij = J(g) delta_ij − g_i g_j / ( K (1 + u) ) ,   d_j Pi_ij = (D.P) g_i  (exact),

and in the deep field Pi_rr = −Pi_tt, so sigma_r^2 = −v_inf^2/2 < 0.

**NEW:**

- **(E7), the assembly condition on Sigma_f.** With y^m the fields on Sigma_f,

        J^m n_m |_{Sigma_f}  =  X_L( g_b ; a0 ) rho_b u^m n_m ,
        equivalently  rho_c,f = (1/K) div[ (1 − mu(g_b,f/a0)) grad Phi_b,f ] .

  The clock's expansion enters only through **where** Sigma_f is (its zero), never through the field
  equations — which is why TK1's gradient blow-up does not apply here.

- **(E8), the transport equation.** For the system's comoving volume V(t),

        d/dt M_C(V)  =  Flux across boundary(V)  (stripping: negative; merging: positive),
        d/dt M_b(V)  =  (the baryons' own budget: expulsion, accretion, stripping),
        X  =  X_f ( f_C / f_b ) .

  Both charges stay non-negative; that is the only constraint the theory puts on the fluxes.

---

## 5. The three regimes

### 5A. The expanding background (the clock falls with the Hubble flow)

P = 0 by symmetry; the sector is the cold component of cosmology. Then [C: QX17 limits; MK1]

    n_d a^3 = const ,
    Qbar − 1 = I0 / (2 mu_K^2 a^3) ,   w = w0 / (w0 + a^3) ,   w0 = I0 / (4 mu_K^2) ,
    c_s^2 = (Qbar − 1)/Qbar ,   Jeans wavenumber k_J = mu_K  (physical) ,

with I0 = 8 pi G rho_c0 = 3 (H0/c)^2 Omega_c = 4.037e-8 per Mpc^2. Cold by z = 3400
(w ≤ 0.01) needs mu_K ≥ 198 per Mpc; the record's CMB-lensing Jeans line needs 2.5e4 per Mpc.
The law is **off** here: it is not a force, and it is not part of the background's dynamics.
Result: the CMB, CMB lensing and the growth rate are carried — and they pass when computed
(CO1 C1: chi^2 − chi^2_cal = −65.21 / −65.07 against a line of ≤ 9; CO2 P2: 0.9928 ± 0.0239,
−0.30 sigma; CO2 P3: chi^2 1.95 / 2.14 over four DESI DR1 bins).

### 5B. The settled galaxy (the clock stands still)

Static clock, and with the dust term suppressed on galaxy scales the field equation closes to

    div[ mu(g_bar/a0) grad Phi ] = 4 pi G rho_b ,

whose solution is the law. Around a round galaxy of baryon mass M_b [C: QX17; H: `eq1_check.py`]:

| quantity | equation |
|---|---|
| the law | g_N = g^2/(g + a0), i.e. g = g_N [1/2 + sqrt(1/4 + a0/g_N)] |
| the cold pull | g_c = g − g_N = a0 g/(g + a0); equivalently g_c g = a0 g_N; **never exceeds a0** |
| enclosed cold mass | M_c(<r) = M_b X(x), X = (sqrt(1+4x^2) − 1)/2 = M_b a0/g |
| scales | r_M = sqrt(G M_b/a0) = 6.479 / 5.894 kpc at log M_b = 10.45; X = 1 at 9.163 / 8.335 kpc |
| deep field | rho_c = a0/(2 pi G r) — **one column, a0/2 pi G = 106.849 / 129.128 Msun/pc^2, for every galaxy** |
| weak field | rho_c = sqrt(G M_b a0) / (4 pi G r^2) — an isothermal halo |
| flat speed | v_inf^4 = G M_b a0  (= 136.8 / 143.4 km/s at log M_b = 10.45) |
| dispersion | sigma^2 = (1/2) sqrt(G M_b a0)  (= 96.7 / 101.4 km/s) |
| stress | Pi_ij = J(g) delta_ij − g_i g_j/(K(1+u)); deep field Pi_rr = −Pi_tt (sigma_r^2 < 0) |
| where it ends | for a share X_s, x_t^2 = X_s(X_s+1); with PD1's X_s = 59.5, x_t = 59.998 → R_trunc = 388.7 / 353.6 kpc |

The state exists and is stable with gravity coupled around point masses (SCS1 STABLE) and isolated discs
(SCS2 STABLE: positive halo density in every cell of every isolated disc solved). A disc in an external
field is **NO VERDICT** (SCS2/SCS3; SCS3 finds negative density and slow growth on every such
background, e-folding 0.74-2.4 Gyr at 0.1 a0).

**And here is the number the record cannot pay.** X(x) exceeds the whole cosmic budget 5.41 M_b at
x = 5.8888 r_M (38.155 / 34.708 kpc), and grows as x thereafter. Recomputed at FLD1's actual KiDS
window edges, log M_b = 10.45:

| r | x | demand | /5.41 budget | /1.06 delivered | /1.40 settled |
|---|---|---|---|---|---|
| 272 kpc (inner edge) | 41.98 / 46.15 | 41.48 / 45.65 M_b | 7.67 / 8.44 | 39.14 / 43.07 | 29.63 / 32.61 |
| 637 kpc (middle edge) | 98.31 / 108.08 | 97.82 / 107.58 M_b | 18.08 / 19.89 | 92.28 / 101.49 | 69.87 / 76.84 |

So in a settled galaxy the amount is **not** carried in by the flow. It is written in at Sigma_f.

### 5C. The cluster (no static-clock state exists there)

This is the regime where the record says the theory stops, and it is named as such rather than papered
over.

- **CLS1: NO STATE.** Solved in action (A) at form B's own dust constant (mu_K ≥ 198 per Mpc),
  **0 of 7** clusters hold a static-clock state. The clock's own pressure is too weak there.
- **QX2 / MK1:** a static clock in a cluster gives the law plus −mu_K^2 Phi / K, which leaves X-COP
  short by 0.47 / 0.43 dex.
- **What the data say instead** [C: RB1 gate 1, HIS1 H4, DD1]: in a cluster the cold inventory
  sits at roughly the **cosmic share**, X ≈ 4.94-5.12 against a budget of 5.41 — i.e. a closed
  system that kept everything. Groups, which are *open* (40 % of their baryons now outside R500), sit
  at X = 9.07.
- **FRM1's verdict:** the only channel that raises a system is baryon loss, it saturates at
  d_max = +0.310 (X-COP) / +0.219 (CLASH) canonical, and the two cluster classes sit at
  +0.496 ± 0.022 and +0.553 ± 0.023 — **0.185 and 0.334 dex above anything the ledger's channels
  can do**, with 77 % / 98 % of their individual points above the absolute ceiling a0/g_bar.

**So the third regime is: the sector is still dust there — 5.41 times the baryons that are present — and it has
not been converted into the law's halo.** Rule 5 of `THEORY_ASSEMBLED_2026-11-10.md` states that as a rule
("for a hot system 5.41 times the baryons that fell in"); PD1 concedes the hot branch is a rule, not a
solution (P7). It is an initial condition, and nobody has derived it.

| regime | clock | sector's state | what it looks like | where graded |
|---|---|---|---|---|
| expanding background | falling with H | dust, P = 0, n_d a^3 const | the cold component of cosmology: 5.41 x baryons | CO1, CO2, MK1, R541 |
| settled galaxy | static | halo, D.P, shape X(x) | the law; isothermal halo; deep column a0/2piG | SHP1, PD1, SCS1, SCS2, FB1 |
| cluster | not static | dust at full share | 4.94-5.12 M_b closed, 9.07 for open groups; law's halo absent | RB1, CLS1, MK1, QX2, FRM1 |

---

## 6. Every empirical row the theory must satisfy

Measured values as the lanes landed them. **canonical / alt** where a lane graded both. Rows this lane
recomputed from the frozen DD1 table are marked *recomputed* and print in `final1.out`.

| # | row | what the theory must give | measured (canonical / alt) | lane |
|---|---|---|---|---|
| 1 | SPARC rotation curves | the law | rms **0.0569 / 0.0556** dex, PASS | PD1 P2 |
| 2 | nothing truncated inside its last point | no halo ends early | **0** galaxies | PD1 P2 |
| 3 | shape of what is not baryons, from raw data | X(x) | within **0.057 / 0.021** dex, x = 0.18-10 | SHP1 |
| 4 | the cold pull's ceiling | never exceeds a0 | g_c = a0 g/(g+a0) **exact** | QX17 |
| 5 | deep-field column | a0/(2 pi G) | **106.849 / 129.128** Msun/pc^2 (record 106.9 / 129.1) | EQ1 §6; *recomputed* A2 |
| 6 | flat speed | v_inf^4 = G M_b a0 | **136.8 / 143.4** km/s at log M_b 10.45 | EQ1 §6; *recomputed* A9 |
| 7 | isothermal dispersion | sigma^2 = (1/2) sqrt(G M_b a0) | **96.7 / 101.4** km/s | FB1; *recomputed* A9 |
| 8 | primary CMB (Planck PR4 + ACT DR6) | dust branch | chi^2 − chi^2_cal = **−65.21 / −65.07**, line ≤ 9 | CO1 C1 |
| 9 | cold / baryon at that fit | one number | **5.410 / 5.412** | CO1 |
| 10 | CMB lensing amplitude (pinned) | dust spectrum | **0.9928 ± 0.0239** (−0.30 sigma) | CO2 P2 |
| 11 | growth rate f sigma8 (DESI DR1, 4 bins) | dust branch | chi^2 **1.95 / 2.14**, largest pull 1.13 | CO2 P3 |
| 12 | KiDS host-free lenses, 1.6 R_h veto | law, counted once | shape ratio **0.811 ± 0.134** vs 1.003 (1.1 sigma), PASS | ONE1 |
| 13 | KiDS outer amplitude, host-free | the law's level | **1.4002 ± 0.2211 / 1.2740 ± 0.2012** of the law | KO1 E7 (reproduced GAS1) |
| 14 | KiDS pooled isolated lenses | the law's level | **FAIL 1.34 / 1.39**, 44 of 59 over | PD1 P2 |
| 15 | cosmic-share exclusion | direct measurement | rejected at **+4.85 / +4.93 sigma** | ONE1 brackets |
| 16 | groups (Lovisari, R500) | full share fell in | f_ret **0.597 [0.556, 0.637]**, CONSISTENT | RB1 gate 1 |
| 17 | X-COP, last radius | at the ceiling | f_ret **1.095 [0.885, 1.259]** | RB1 gate 1 |
| 18 | X-COP at R500 | the ceiling | f_ret **1.057 [1.046, 1.072]** (above 1 beyond errors) | RB1 gate 1 |
| 18b | X-COP X (outermost point) | cosmic budget | X_last **4.94** [4.30, 6.11] | DD1, HIS1 H4 |
| 19 | groups X | above the budget | X **9.07** [8.49, 9.73] | DD1, HIS1 H4 |
| 20 | cluster offset from the law | formation ledger | X-COP **+0.496 ± 0.022** (22.5 se); CLASH **+0.553 ± 0.023** (24.0 se) | FRM1 |
| 21 | baryon-loss ceiling | d <= d_max | X-COP ceiling **+0.310**; CLASH **+0.219** — both violated | FRM1; *recomputed* A10 |
| 22 | Bullet: peaks with the galaxies | collisionless charge | d_gal **14 / 22** kpc vs d_gas **197 / 136** kpc | PD1 P5, RB1 gate 4 |
| 23 | nothing below Newton | the floor | **0 of 626** (HIS1); **3 of 626** by this lane's per-system median; line ≤ 3 | HIS1 H2, DD1, *recomputed* A4 |
| 24 | tidal dwarfs | Newton, X = 0 | median Y **+0.067 ± 0.115**; d_L **−0.687 / −0.725 ± 0.115** | HIS1 H1, CFG936, G2 |
| 25 | DF2, DF4 | between Newton and the law | DF2 **−0.743** (e 0.344); DF4 **−0.943** (e 0.349) | HIS1 H2 |
| 26 | formation bands | 16 pre-registered class intervals | **14 of 16** canonical / **13 of 16** alt — HOLDS EXCEPT | FRM1 F3 |
| 27 | the free rule (no theory assumed) | beats the class-constant reference | held-out scatter **0.213** vs 0.284 ref, but **10 of 16** classes fail — FAILS | FRM1 F4 |
| 28 | the anchor classes | on the law, no free parameter | SPARC **+0.004 ± 0.012**; KiDS **+0.137 ± 0.109**; LG field **−0.090 ± 0.062** — HOLDS | FRM1 F5 |
| 29 | the halo is not infallen charge | deliver 41-98 M_b | delivered **1.06 / 1.40** M_b | CRUX (T4, LFS1, VSH1, COL1); *recomputed* A5 |
| 30 | missing baryons | close 11.0x | **excluded**: Sigma needed 6.1627 / 7.4477 Msun/pc^2; amplitude 0.0392 ± 0.0069 / 0.0324 ± 0.0057 vs gate 0.891 | GAS1 |
| 31 | the medium is a local solid | pass M5 | **fails**: strain 11-249, W/J 3.6-241, Bullet yield 76-478, melts 6/6 | ELA1, M5 |
| 32 | one dust constant | one mu_K | **NO VALUE**: ≥ 198 /Mpc vs ≥ 2.5e4 /Mpc vs ~1 | MK1, MK2 |
| 33 | the joint | how falling becomes standing | **NOT DERIVED**: clock folds at the centre in 0.06-0.15 Gyr; fold reach 1.3-5.4x short | COL1, FLD1 |

**What this lane's own recomputation adds** (`final1.out` A4): it rebuilds all 16 class offsets **from the
frozen table, per system, per footing**, and reproduces FRM1's published per-class offsets to the third
decimal in every case (SPARC +0.004 / −0.023; faint rotators −0.239 / −0.274; tidal dwarfs −0.687 /
−0.725; X-COP +0.496 / +0.465; CLASH +0.553 / +0.524; MW ultra-faints +0.592 / +0.552; Coma UDGs
+0.319 / +0.280). It also reproduces the record's own scales independently: r_M = 6.479 / 5.894 kpc,
budget radius 38.155 / 34.708 kpc, truncation 388.7 / 353.6 kpc.

---

## 7. The top five predictions that are not yet measured

Each has a number, a recipe, and a falsifier. None has been graded by a lane of the record.

---

### P1 — The ceiling: no transfer can lift a system above d_max(a0/g_bar)

**The claim.** Baryon loss is the only upward channel, and it **saturates**: with f_C = 1,
X = X_L(u f_b)/f_b rises as f_b falls but tends to u. So every system obeys

    d  <=  d_max(u) = log10[ (1 + u) / (1 + X_L(u)) ] ,   u = a0/g_bar ,
    X_L(u) = ( sqrt(1 + 4u) − 1 ) / 2 .

**The number.** `d_max` is footing-free (u already carries a0). Computed (`final1.out` A3):

| u = a0/g_bar | 0.5 | 1 | 2 | 4.5 | 10 | 30 | 100 |
|---|---|---|---|---|---|---|---|
| d_max (dex) | +0.041 | +0.092 | +0.176 | +0.312 | +0.473 | +0.713 | +0.983 |

Deep limit: d_max → (1/2) log10 u, reached to 0.999 at u = 1e4 (0.99894).

**The recipe.** For each system in a new sample: (i) take the baryon mass distribution and the DD1
aperture; (ii) form g_bar at the outermost measured radius; (iii) u = a0/g_bar;
(iv) d = log10(g_obs/g_bar) − log10(1 + X_L(u)); (v) require d ≤ d_max(u) + 3 s.e.

**The falsifier.** ≥ 5 % of a clean **unhosted** sample sitting above d_max at more than 3 s.e., in a
case where the retained baryon fraction is independently measured at f_b ≥ 0.5. That kills the channel
algebra itself, not merely the cluster classes.

**Current state, honestly.** 4 of the 16 classes already sit above their ceiling, and the two cluster
classes are structural violations, not rounding: X-COP by **+0.185** dex canonical (+0.119 alt) and
CLASH by **+0.334** (+0.273), where FRM1 finds **77 % / 98 %** of individual points above the
absolute ceiling a0/g_bar. **That is the theory's landed failure, printed here as such and not counted as
a prediction.** The prediction is the bound's behaviour on systems whose transfers are measured: for those,
the theory says you will never again see a +0.5 dex excess.

**Lane:** FRM1 (master equation, saturation, F3) — inputs from DD1 (frozen 626-system table), HIS1/HIS1R,
RB1 (cluster amounts). Arithmetic recomputed here (`final1.out` A3, A10).

---

### P2 — The floor: second-generation baryons carry exactly X = 0, at every radius

**The claim.** A system assembled from baryons that were **already stripped** — tidal debris, a stripped
nucleus, a DF2/DF4-class object — inherits no cold charge. Both charges are non-negative, so the ratio
cannot be negative. It is exactly zero, and the system is Newtonian **at all radii**, not merely on average:

    M_dyn(<r) = M_b(<r)  for every r,   with no radial rise in g_obs/g_bar.

**The number.** Predicted median Y = **0.000 ± 0.030** dex for a confirmed debris-formed class. The law,
evaluated at the same fields, demands Y_L = **+0.691** canonical / **+0.733** alt for the tidal-dwarf
sample — a **23 sigma** separation. Per object the theory predicts |Y_sys| ≤ 0.10 dex.

**The recipe.** For each confirmed debris-formed object with a resolved kinematic profile: regress
log10(g_obs/g_bar) on log10 r. Require |Spearman rho| ≤ 0.5 with p > 0.05 (no rise) and intercept
0.000 ± 0.030. The intercept test is the one nobody has run; HIS1's H1 tested only the median.

**The falsifier.** Two independently confirmed debris-formed systems whose enclosed non-baryonic mass
exceeds 0.5 M_b at more than 3 s.e., or one showing a significant positive radial trend in
g_obs/g_bar. Either kills "the amount was set at formation and debris inherits none".

**Lane:** HIS1 H1/H2, DD1 (the six tidal dwarfs and DF2/DF4), CFG936, G2, FRM1 (the floor).

---

### P3 — The accretion deficit: a system still assembling sits at d = −(1/2) log10 f_b

**The claim.** Late baryon accretion (f_b > 1, f_C = 1) lowers the ratio, because the accreted
baryons dilute a charge that was already fixed. The shift is exact in the deep regime, **footing-free**:

    d = −(1/2) log10 f_b .

**The number.** f_b = 1.5 → −0.088 dex; **f_b = 2 → −0.151**; **f_b = 3 → −0.239**; f_b = 5 → −0.349;
f_b = 10 → −0.500. (`final1.out` A8.)

**The recipe.** Take isolated, gas-dominated rotators. Independent f_b = M_b(today)/M_b(at the epoch the
halo's charge was fixed), inferred either from the star-formation history (a stellar mass built up over
a Hubble time means most of the gas arrived after the halo's charge was set) or from the HI-to-stellar
disc size ratio (an extended, still-accreting gas disc). Bin the sample in f_b and regress d on
−(1/2)log10 f_b; require slope 1.00 ± 0.30.

**The falsifier.** An independent assembly estimate giving **f_b ≤ 1.5** for the isolated faint rotators. That
caps the deficit at **−0.088** dex against the measured **−0.239 ± 0.045** (canonical) /
**−0.274 ± 0.044** (alt).

**Why this one is on the list.** It is the lane's own **H3, and H3 landed as a FAIL** (FRM1; HIS1: isolated
faint rotators −0.278 ± 0.080 canonical, −0.315 ± 0.080 alt, 3.5 / 3.9 standard errors below the law).
P3 names the one measurement that would turn it: either the accreted-baryon budget is really ≈ 6x the formation
budget (and the reading survives) or it is ≤ 1.5x (and the formation rule is wrong for assembling systems).
Note also that H3's failure is **not robust to a coherent 20 % distance error**: with every distance 20 %
smaller it reads 2.3 / 2.7 standard errors (HIS1).

**Lane:** FRM1 (master equation, channels, H3), HIS1 H3, DD1.

---

### P4 — Epoch invariance: at matched g_bar, the offset does not care what time it is

**The claim.** a0 = (1/2) c sqrt(G rho_DE) with rho_DE constant, so the law's scale does not run. The amount
is fixed at the **formation** field. Therefore two systems of the same present-day depth but different observed
epochs must show the **same** offset.

**The number.** Formation + constant a0: **d(z ≈ 0.45) − d(z ≈ 0.05) = 0.000 ± 0.100 dex.**
A charge that accumulates in proportion to cosmic time: **−0.165 dex** over the same interval and **−0.320 dex**
out to z = 0.90. The force reading: 0.000, with **both** individual values 0 — already excluded by the
measured +0.496 / +0.553. (`final1.out` A7: t(0.05) = 13.0924, t(0.45) = 8.9601, t(0.90) = 6.2708 Gyr;
log10 of the ratios −0.1647 and −0.3197; H0 = 67.4 km/s/Mpc, Om = 0.3154.)

**The recipe.** Re-bin X-COP (z ≈ 0.05) and a relaxed cluster sample at z = 0.40-0.60 in **g_bar**, at the
**same** hydrostatic aperture, then compare class medians. The formation reading says equal; a source says the
older one is higher.

**The falsifier.** A monotone trend with |Delta d| ≥ 0.30 dex at 3 standard errors between the two epochs.
That says the amount is still being written today — a source, not an initial condition.

**Current state.** **UNAVAILABLE / no result.** CLASH (z 0.18-0.89) reads +0.553 against X-COP's +0.496 — a
gap of only +0.057 dex, the wrong sign for a time-proportional source and 1.8 standard errors — but the two
samples are **not** matched in g_bar or aperture, so this is a lead, not a test.

**Lane:** FRM1 names exactly this as the separating measurement (relaxed clusters at z ~ 0.5 against z ~ 0 at
the same g_bar and aperture). HIS1 H5 / FRM1 F5 constrain the **undisturbed** classes only, and there
redshift contributes nothing (N2: held-out scatter 0.285 vs 0.284 reference).

---

### P5 — The gas column: the formation reading requires NO amount-fixing hot gas

**The claim.** If the non-baryonic mass is the clock sector's own stress-energy, conserved from formation,
then it is **not baryons**, and there is no reservoir of hot gas at 0.1-2.6 Mpc waiting to be counted. The
baryon reading needs one, and GAS1 computed exactly what it would have to be:

    Sigma_gas = a0 / (pi G x_b^2) ,    x_b^2 = R(1+R) = 5.41 x 6.41 = 34.6781

**The number.** **Sigma_gas = 1.287355e-2 / 1.555779e-2 kg/m^2 = 6.1627 / 7.4477 Msun/pc^2**, constant in
radius, out to 2.6 Mpc, **the same for every galaxy**. (This lane recomputes it from G = 6.6743e-11 as
1.287297e-2 / 1.555710e-2 kg/m^2 = 6.1623 / 7.4472 Msun/pc^2; agreeing with GAS1 to 6.5e-5 relative,
the difference being GAS1's printed G = 6.674e-11. `final1.out` A2.)

**The recipe.** Stack eROSITA and/or SZ data around a set of isolated L* galaxies (KO1's host-free cut,
spectroscopic redshifts), convert to gas mass in annuli at 1.3-2.6 Mpc, divide by pi R^2, compare with
6.16 / 7.45 Msun/pc^2.

**The falsifier.** A measured hot-gas column ≥ **2.0 Msun/pc^2** at 1.3-2.6 Mpc around isolated L* galaxies.
**But the amplitude gate fires first, and it is the stronger statement:** put that gas into g_bar and the outer
points move to **0.0392 ± 0.0069 / 0.0324 ± 0.0057** of the law — 36x / 41x below the record's 0.891 line,
more than 100 sigma. So the two readings cannot both be true: **a positive detection at that column is not
a rescue of form B, it is the same gas counted twice, and it destroys the fit it was invoked to save.**

**Current state.** **UNAVAILABLE.** GAS1 states explicitly that no measured hot-gas mass at Mpc radii around
isolated galaxies exists in this repo, and that no eROSITA or SZ upper limit is on disk. This prediction is
therefore a measurement to be made, not a number to be read.

**Lane:** GAS1; cross-checked against KO1 R6 (B21's own hot gas moves their published outer points from
1.50 to 0.47 of the law) and GO1 (the only measured gas at Mpc radii on disk: 102 eRASS1 groups).

---

## 8. What is not claimed

- **kappa = 1/2 is fitted, not derived.** Z = 2 sqrt(8 pi/3) is a consequence of the definition
  a0 = c H_Lambda / Z; the factor 1/2 is input. The record's kappa ledger says so.
- **g_b,f is a constant of integration per system, not a prediction.** FRM1 discloses this. Any
  per-class budget printed here is an inference from the measured offset, not a forecast.
- **The joint is not derived.** How a falling clock becomes a standing one has a failing verdict on
  the two routes tried (COL1 BREAKS DOWN; FLD1 1.3-5.4x short). **This file does not supply it.**
  It says what the formation reading is, what it costs, and what it predicts.
- **There is no completion here.** No new bulk term is added, so no gate moves because of this file.
  What this file does is put the theory the data picked into one place, with every lane named.

---

## 9. The verdict, with what survives attached

**What survives, and it is a lot:** form B's law passes SPARC at 0.057 / 0.021 dex with no galaxy
truncated (SHP1, PD1); it passes host-free KiDS at the 1.6 R_h veto (ONE1); its cosmology rows hold
when computed (CO1, CO2); its static state is stable around point masses and isolated discs (SCS1,
SCS2); the cold charge is real, separately conserved, and bounded below by Newton (HIS1 H1-H2, DD1)
— 14 of 16 pre-registered class bands met (FRM1 F3) against 1 of 5 for the plain force reading.

**What does not survive:** the amount in clusters. The ledger's only upward channel saturates at
+0.310 / +0.219 dex; X-COP and CLASH sit +0.185 and +0.334 dex above it, with 77 % / 98 % of their
points beyond the absolute ceiling. The halo is not infallen charge (1.06 / 1.40 M_b delivered against
41.5 / 97.8 M_b demanded), and the gas that would square that circle is excluded by its own
consequence (GAS1).

**So the theory as the record supports it is: one conserved cold charge, in two states of one clock,
with the ratio between it and the baryons fixed on the hypersurface where the clock's flow stopped
expanding — and a cluster we cannot yet account for.** The positive law attached to the verdict is P1
through P5 above: a hard ceiling, an exact floor, a dilution law for assembling systems, an epoch
that does not run, and a gas column that must not be there.

---

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
