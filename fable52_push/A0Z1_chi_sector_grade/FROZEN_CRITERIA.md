# A0Z1 FROZEN CRITERIA: the chi sector and a0(chi) of DT1's action

Committed alone, before any A0Z1 script or number. TEST lane, quarantined. Adopts nothing, relabels nothing, registers
nothing. Footings canonical / alt graded separately, never pooled. kappa = 1/2 FITTED; not theory closed.

## What is graded

DT1 (`../DT1_dust_term_design/ACTION.md`) replaces the constant Lambda by a field chi with potential V(chi) and writes the
owner's relation as a term of the action:

    S = Int sqrt(-g) { R/(4K) - (1/2) g^{mn} d_m chi d_n chi - V(chi) + L_K(Q)
                       + P^m A_m - W(K|P| ; a0(chi)) - gamma_L F(Pi) + lambda n^m P_m } + S_matter       (DT1)

    a0(chi) = kappa sqrt(G V(chi)),  kappa = 1/2 FITTED,  K = 4 pi G,  W(p;a0) = (a0^2/K)[-p/a0 - ln(1 - p/a0)],
    F(Pi) = [max(Pi,0)]^2/2,  Pi = D_m P^m,  gamma_L = K Lstar^2/2 .

MK2 graded the **dust term** of (DT1) and it failed (NO VALUE / NO VALUE; clusters and groups at no sound speed). The
**chi sector and a0(chi) were not graded by MK2.** This lane grades them. Nothing here re-grades the dust term, and
nothing here can repair it: a pass in this lane would still leave (DT1) failed on clusters.

## The four questions (frozen, in this order)

1. **Q1 the chi equation of motion.** ACTION.md section 3 gives, by hand,
   `box chi = V'(chi) [ 1 - S(u) kappa^2/(8 pi) ]` with `S(u) = 2(u - ln(1+u)) - u^2/(1+u)`, `u = |A|/a0(chi)`, in a
   static weak field. Verify or refute it **term by term** by certified variation (sympy, exact): the Legendre
   elimination of P (QX17 K0), the on-shell law term J(|A|;a0) and its sign, dJ/da0, da0/dchi, and the bracket.
2. **Q2 the sign of the bracket.** It turns negative where `S(u) > 8 pi/kappa^2 = 32 pi`. Compute u in the Solar System
   (r = 1 AU from the Sun; at the Earth's surface), in a galaxy at 1 / 10 / 100 kpc for log M_b = 10 and 11, and in a
   cluster core. Say whether the bracket goes negative anywhere observed; if it does, say whether chi runs away or a0
   varies, and on what timescale.
3. **Q3 a0(z) against FRZ2's frozen gate.** For the smallest example potential `V = V0 exp(-lambda chi sqrt(K))`, compute
   the a0(z) this action predicts and put it through FRZ2's own gate (Delta chi^2 <= 4 per footing over the 12 DESI P1D
   bins, reading L) with FRZ2's own machinery. FRZ2's numbers, which this lane must reproduce where they apply:
   P0 9916.2 / 9008.7, P0.5 251.8 / 167.1, P1 13338.6 / 23421.4, D 13418-14859, Q 8292-10509, H 20943 / 34390; all FAIL.
4. **Q4 screening.** Is the chi coupling screened by `gamma_L F(Pi)` in a galaxy?

## Method

**Q1 (sympy, exact, no numbers).** Build the Lagrangian density of the chi and law sectors on flat-space jet symbols;
maximize over |P| (K0); substitute the on-shell |P|; take the Euler-Lagrange derivative with respect to chi at fixed
|A|; simplify. Compare the result with ACTION.md's line, factor by factor:
 (i) `max_P [P.A - W(K|P|)] = (a0^2/K)[u - ln(1+u)]`, attained at `K|P| = a0 u/(1+u)` (QX17 K0);
 (ii) `dJ/da0` at fixed |A|;
 (iii) `da0/dchi = kappa^2 G V'/(2 a0)` from `a0^2 = kappa^2 G V`;
 (iv) the bracket, using K = 4 pi G.
The sign of (i) in the action is what decides the sign of the bracket, so it is checked, not assumed.

**Q2 (closed form + quadrature).** u = A/a0 with A the **law's** acceleration: the record's spherical static law
`g^2 = g_N (g + a0)` (QX17 section 3, "law S"), `g_N = G M(<r)/r^2`. Inputs:

| place | what is computed |
|---|---|
| Solar System, 1 AU | g_N = GM_sun/r^2, GM_sun = 1.3271244e20 m^3/s^2, r = 1.495979e11 m |
| Solar System, Earth's surface | g = 9.80665 m/s^2 (given, not from a profile) |
| galaxy, log M_b 10 and 11 | point mass M_b at r = 1, 10, 100 kpc (**an upper bound on A at 1 kpc**; a resolved profile puts less mass inside 1 kpc) |
| cluster core | NFW, M200c = 1e15 Msun, c200 = 3.5, at r = 50, 100, 300 kpc |

Constants: a0 = 9.3603e-11 (canonical) / 1.1312e-10 (alt) m/s^2 (CFG556 `A0`); Lstar = 21.7 / 22.9 pc (QX17);
G = 6.674e-11 SI; Msun = 1.989e30 kg; kappa = 1/2.
Consequences where the bracket is negative, in this order:
 (a) **static response** — the perturbation of the KG equation `lap dchi = -V' S(u) kappa^2/(8 pi)` solved as a Poisson
     integral over the source region, giving `da0/a0 = (V'/2V) dchi` on the axis; the region's outer radius is where
     u = 1 (S ~ u^3/3 cuts the integral off), the inner radius is the source's own radius;
 (b) **runaway test** — the effective mass `m_eff^2 = V''(1 - kappa^2 S/(8 pi))` is negative where the bracket is
     negative; a growing mode exists only if the tachyonic Compton wavelength fits in the region,
     `|m_eff| L >= pi`. Report `|m_eff| L` and the growth time `1/|m_eff|` if it fires, the light-crossing time
     `L/c` if it does not.

**Q3 (FRZ2's machinery, read-only; the a0(z) is this action's own).** f(z) = a0(z)/a0(0) = sqrt(V(chi(z))/V(chi(0)))
because a0 = kappa sqrt(G V). V(z) is computed by integrating the action's own FRW scalar equations for
`V = V0 exp(-lambda chi sqrt(K))`, matter + scalar, flat:

    chi'' + 3 H chi' + V'(chi) = 0,  H^2 = (8 pi G/3)(rho_m + chi'^2/2 + V),  V' = -lambda sqrt(K) V .

In Planck units (8 pi G = 1) the exponent is `-lambda_std chi` with `lambda_std = lambda/sqrt(2)` (K = 4 pi G = 1/2).
Integrated in the standard autonomous variables (x = chi'/(sqrt6 H), y = sqrt(V)/(sqrt3 H)) from z_i = 100 with the
field at rest (x = 0, thawing), shooting the initial y so that Omega_phi(0) = 1 - Om of the footing's form B fit
(F1A B2 cold), Om = (ob + oc)/h^2. **Frozen cases:** lambda is fixed by requiring the model's own w0 to equal each of
FRZ2's three observed CPL w0 (Pan -0.838, DES5 -0.752, Uni -0.667); those three are the graded cases
`X-Pan, X-DES5, X-Uni`. One lambda, one a0(z), no free parameter left.
f(z) is tabulated at the 12 DESI bins and fed to a copy of FRZ2's `frz2_hm.py` / `frz2_forest.py` (FRZ2's copy of
FRZ1's, pipeline set-up unchanged; the only edit is the function `fz(z)`), both footings, reading L.

**Q4 (the record's own diagnostic).** QX17 (E2), the screened constitutive law:
`(1 + gamma_L Pi_+) A_m + gamma_L D_m Pi_+ = K W'(K|P|) Phat_m`. Screening is active where either addition to A is
>= 1 in relative size. Both are evaluated on the **unscreened** on-shell P (`K|P| = a0 u/(1+u)`, the K0 Legendre map,
`Pi = div P` in spherical symmetry) — the standard perturbative test, the same one QX17 section 3 sizes by hand.
Reported: `delta_Pi = gamma_L Pi_+` and `delta_grad = gamma_L |grad Pi_+| / |A|`.

## Gates and labels

- **Q1**: CERTIFIED if the sympy residual of the derived EOM against ACTION.md's line is exactly 0 in S(u), in the
  coefficient kappa^2/(8 pi), and in the sign; REFUTED otherwise. A refutation of the hand EOM is not a pass for the
  sector: it leaves the sector ungraded.
- **Q3**: per case and footing PASSES if Delta chi^2 <= 4, else FAILS (FRZ2's gate, unchanged).
  Lane labels: `a0(chi) FAILS / a0(chi) FAILS` if every X case fails on both footings; `a0(chi) PASSES` (any footing
  name) if any X case passes on both; NO VERDICT if a known answer fails or the mutation does not bite.
- **Q2 / Q4**: graded as stated answers (negative / not negative, screened / not screened) with their numbers; they do
  not carry a PASS/FAIL label of their own.

## Kill conditions (pre-registered, before any number)

- **K1 (EOM).** If the certified variation does not reproduce ACTION.md's chi EOM term by term, the hand algebra of
  (DT1) section 3 is refuted and the chi sector is ungraded (NO VERDICT on Q2 and Q4 as well).
- **K2 (forest, the graded gate).** If every X case fails Delta chi^2 <= 4 on both footings, the a0(chi) branch of
  (DT1) — a0 = kappa sqrt(G V(chi)) with this V — is KILLED on the forest row. This is the lane's label.
- **K3 (runaway).** If `|m_eff| L >= pi` anywhere observed, chi runs away there; the sector is KILLED as unstable and
  the growth time is reported.
- **K4 (a0 varies).** If `|da0/a0| > 1e-2` anywhere observed (Solar System, galaxy, cluster), a0 is not the constant
  the record's fitted laws use; the sector is KILLED. (1e-2 is set generously: the record's SPARC rms is 0.056 in
  dex-ish units and a 1 %-level shift of a0 inside a galaxy is far above what those fits allow.)
- **K5 (screening fails where it is needed).** If `gamma_L F(Pi)` does not screen in a galaxy (Q4 = not screened), the
  coupling is live there at full strength; that is not a kill by itself, but it is what makes the sign of the bracket
  (Q2) decisive in galaxies rather than academic. It is reported as fired/not fired.

## Known answers (must pass; a failure gives NO VERDICT)

- **KA1**: with the law sector removed (J == 0) the chi EOM is `box chi = V'` (sympy residual 0).
- **KA2**: K0 Legendre map, sympy exact, residual 0 — reproduces QX17's K0, `K|P| = a0 u/(1+u)`.
- **KA3**: V = const (the old Lambda): a0' = 0 and the EOM reduces to `box chi = 0`.
- **KA4**: S(u) series `u^3/3 - u^4/2 + O(u^5)`; S(3) = 0.9772 (ACTION.md: "about 1 at u = 3"); S(u) = 32 pi at
  u = 109.6 (ACTION.md: "about u > 100"); S ~ u for large u. These are checks on ACTION.md's own words, not on data.
- **KA5 (pipeline)**: this lane's copy of FRZ2's pipeline, run with f = 1, gives FRZ2's P0 9916.2 / 9008.7, and with
  FRZ2's own D-Pan f(z) gives 13657.7 / 13418.1, each to 0.1. Inherited: KA2/KA3 of FRZ2 (R = 1 -> 0; CO1 z = 0 held
  160.74 / 1025.57).
- **KA6**: `da0/a0` for a point mass in the Newtonian regime has the closed form
  `(lambda^2/4)(a0 G M/c^4) ln(r_1/r_in)` with `r_1 = sqrt(GM/a0)`; the numerical Poisson integral must agree with it
  to 20 % (the closed form keeps only S ~ u and cuts the integral at r_1).

## Mutation (must bite; a mutation that does not bite gives NO VERDICT)

- **MU1** (Q1/Q2): the on-shell law term is given the wrong sign, `L_eff = -J` (equivalently min instead of max in the
  Legendre transform). The bracket becomes `1 + kappa^2 S/(8 pi)`, never negative: Q2's answer must flip.
- **MU2** (Q2): S(u) replaced everywhere by its small-u expansion `u^3/3`. The Solar System bracket and `da0/a0` must
  move by orders of magnitude.
- **MU3** (Q3): f(z) = V(z)/V(0) instead of sqrt(V(z)/V(0)) — the square root of the owner's relation dropped. The
  Delta chi^2 must differ from the graded case.

## Hand estimate before any number

- Q1: I expect the EOM to survive. The Legendre map is QX17's K0 (already sympy-certified there), dJ/da0 at fixed |A|
  gives `(a0/K)[2(u - ln(1+u)) - u^2/(1+u)]` — exactly ACTION.md's S(u) — and `da0/dchi = kappa^2 G V'/(2 a0)`; with
  K = 4 pi G the correction is `S kappa^2/(8 pi)`. The one place it can fail is the sign of the on-shell J in the
  action; QX17 K0 has it as `+J`, so the bracket should come out with the minus sign as printed.
- Q2: u = A/a0. At 1 AU A = 5.9e-3, so u ~ 6e7, S ~ u, bracket ~ -2e6: negative, hugely. At the Earth's surface
  u ~ 1e11. In a galaxy the point-mass bound at 1 kpc gives u ~ 150 at log M_b 11 and ~ 15 at log M_b 10, so the
  bracket should turn negative only in the inner parts of the more massive galaxies; at 10 and 100 kpc u is O(1) and
  S ~ u^3/3, bracket ~ 1. In a cluster core u ~ 5-20, S(10) ~ 6, bracket ~ +0.94: positive. So the bracket should go
  negative in the Solar System and in galaxy centres, not in cluster cores.
- Q2 consequences: the static shift carries `(a0 R)^2` — for the Sun `a0 GM/c^4 ~ 2e-24` — so `da0/a0` should be
  ~1e-23 there and ~1e-13 in a galaxy: no observable variation, K4 should not fire. The tachyonic Compton wavelength
  is set by `sqrt(K V) ~ 7 a0 ~ 1.9e-42 GeV`, i.e. ~Gpc, against regions of <= kpc, so `|m_eff| L << pi`: no runaway,
  K3 should not fire. The response time is then the light-crossing time, ~300 yr for a 100 pc nucleus.
- Q3: for a thawing exponential the DE density grows with z (w >= -1 always), so f(3) > 1: the action's a0(z) lands
  between FRZ2's P0 (f(3) = 1, 9916 / 9009) and P0.5 (f(3) = 2, 252 / 167). FRZ2 found that the crossing sits between
  those two and that no frozen case lands on it; a0 rising like (1+z)^n with 0 < n < 0.5 is exactly the shape the
  action produces, and 252 / 167 is the best power law FRZ2 found. So I expect FAILS / FAILS, by 40-60 times or more.
- Q4: the screening ratio is `(Lstar/r)^2/u` in the Newtonian regime and `(Lstar/r)^2` in the MOND regime, so with
  Lstar ~ 22 pc it is ~1e-4 at 1 kpc in a galaxy and ~1e-8 in a cluster: not screened. In the Solar System it is
  ~4e5 at 1 AU: screened. So the answer to "in a galaxy" should be no.

## Not computed (named, not graded)

The dust sector and every MK2 row; the FRW background and CMB rows of (DT1) with chi (the lane takes Om from the
footing's fit and does not refit the CMB); a0(z) for any V other than the exponential; the stability redo SCS1/SCS2
that ACTION.md section 4 item 3 asks for; a full PDE re-solve of the screened P equation (QX17 says the record has
none); the back-reaction of the shifted chi on the halo model; hosted dwarfs (RB2).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
