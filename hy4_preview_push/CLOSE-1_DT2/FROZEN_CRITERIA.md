# CLOSE-1 / DT2 — FROZEN CRITERIA (pre-registered before any number)

Lane: **CLOSE-1 (DT2)**. Object graded: the one engineered kinetic function that
`closure_2026_11_10/MEDIUM_DESIGN_2026-11-10.md` §4 named as LEFT UNGRADED:

> "One engineered function: a single kinetic function with a narrow interval of changed compressibility (DT2).
>  Its linear and static checks pass; whether a forming halo can reach its static state is not computed."

The construction exists in the record, ungraded, at
`research_closure_2026_11_10/DT2_response_audit/tradeoff_audit.md` §4 (an explicit regular counterexample to
DT1's pointwise derivative bound). This lane adopts that shape as the canonical DT2, states the interval
explicitly, re-runs the two checks MEDIUM_DESIGN says pass, and then runs the third thing it says was never
computed.

TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled.
kappa = 1/2 FITTED; not theory closed.

## 0. Conventions

Clock kinetic function `V(Q) = K L_K(Q)`, `K = 4 pi G`, `x = Q - 1`, `n(x) = V_Q(Q)` = the gravitationally
normalized charge (units of inverse length squared; `n = K rho_dust / c^2` at leading dust order).
The record's identities (IC1 / TPA1 / tradeoff audit §2):

    c_ad^2 = n/(Q n'),   M_sus^2 = Q^2 n',   c_eff^2(k) = c_ad^2 / (1 + k_phys^2 / M_sus^2),
    static clock:  x_well = x_bar_inf + phi,  phi = |Phi|/c^2.

Reduced Newtonian system (COL1 Part 1, generalised from the quadratic to any `V`):

    L = (1/K) V(1+h) + J(|grad h|) - |grad Phi|^2/(2K) - rho_b Phi,
    h = -(phi_t + |grad phi|^2/2 + Phi),  J(s) = (a0^2/K)[ s/a0 - ln(1 + s/a0) ],
    N = n(h)/K + div P,   P = -a0 grad h / (K (a0 + |grad h|)),
    d_t N + div(N v) = 0,   grad^2 Phi = K (rho_b + N),   dv/dt = -grad Phi - grad h,  v = grad phi.

## 1. The function, and what is free vs pinned

    x(q) = (n0/M)(q - 1) + A * B(q),      q = n/n0,      A = L - (q2 - 1) n0/M,
    B(q) = 0 (q <= q1);  S(t), t = (q-q1)/(q2-q1) (q1<q<q2);  1 (q >= q2),   S = 10t^3 - 15t^4 + 6t^5.

**PINNED by the record's own lines (not free here):**

| pin | value | line that pins it |
|---|---|---|
| P1 cold slope `M = n'` outside the band | 400 Mpc^-2 | DT1 §2: "clumping at 20 per Mpc (physical) from z = 2 to 5" needs `n' >= k^2` |
| P2 deepest spiral well depth `phi` | 4e-6 | DT1 §2: "galaxy wells are 1e-7 to 4e-6 deep" |
| P3 galaxy cap | `n_well <= 216 n0` | DT1 §2: "keep the deepest spirals below 216 times the mean" |
| P4 band sits above the present point | `q1 > 1` | the counterexample's whole purpose: today's derivative is `M` |
| P5 cosmological normalisation | `n0 = 2.1263e-8 Mpc^-2` | DT1's H0 = 70 km/s/Mpc, Omega_c = 0.26 (audit §3) |

**FREE (the design's knobs):** `q1`, `q2` (the band's edges in density), `L` (the offset jump across the band,
equivalently `A`), the shape `S`, and the extension outside the band (taken as `n' = M` on both sides, the
audit's choice). The constraint `x(q_w) = phi` with `q_w = 14` ties `L` to `q1, q2, S`.

**CANONICAL DT2 (the audit §4 numbers, adopted here as the thing graded):**

    q1 = 2,  q2 = 26,  L = 8.00e-6,  S = 10t^3 - 15t^4 + 6t^5.

Interval of changed compressibility, stated explicitly:

| quantity | value |
|---|---|
| support in density `q` | [2, 26] |
| support in redshift (q = a^-3) | z in [0.260, 1.968] |
| support in offset `x` | [5.32e-11, 8.00e-6] |
| CENTRE (where `n'` is minimal, `B'` maximal) | `q_c = 14`, i.e. `n = 14 n0`, `z_c = 1.412` |
| FWHM (`n' <= M/2`) | `q` in [7.5, 20.5], z in [1.04, 1.74] |
| jump across the band | `L = 8.00e-6 = 2.00 phi` |
| minimum `n'` | 0.0340234 Mpc^-2 at `q = 14` (a factor 1.18e4 below `M`) |

## 2. Kill conditions (pre-registered, before any number is produced)

**K1 — LINEAR (the growth the band costs).** With the record's law-on blend (`epsilon = 1` of TPA1 §4.4),
the charge-perturbation growth factor `D(k)` at DT1's own scale `k = 20 Mpc^-1` (physical), integrated from
z = 6 to z = 0 in the record's background, must satisfy

    D_DT2(20/Mpc) / D_pressureless(20/Mpc)  >=  0.50.

That is: the narrow interval may cost at most a factor 2 of amplitude at the scale DT1's line is stated at.
Also reported without a line: `k = 0.2` and `2 Mpc^-1`, and the band-centre suppression factor
`F = Q^2 n'/(Q^2 n' + k^2)`. **FIRE if the ratio is below 0.50.**

**K2 — STATIC (the static state must exist and be admissible).** For each of 4 masses
(log M_b = 9.4, 10.45, 10.7, 10.9), 3 profiles (point mass, Plummer, Hernquist) and both footings, the
self-consistent static clock (`h = x_bar_inf + phi`, `grad^2 Phi = K(rho_b + n/K + div P)`) must

  (a) converge — the static state must exist. (COL1 Part 0 found it *diverges* for the quadratic at
      mu_K = 1.78 and 3.71, an n = 1 Jeans core; DT2's cold slope M = 400 sits between 3.71^2 and 198^2,
      so this is a live check, not a formality); and
  (b) put the clock's dust inside SPARC's radii at or below KD1's diagnostic line
      `M_dust(<4 R_d) / M_b <= 0.33` (canonical) / `0.19` (alt), the line COL1 Part 0 used.

**FIRE if the static state diverges at any mass/profile/footing, or if the dust share exceeds the line.**

**K3 — FORMATION AND REACH (the thing MEDIUM_DESIGN says is not computed).** A clock that starts as cold
dust in Hubble flow at z = 10 around a baryon point mass (softened over 1 kpc) ramping on over 1 Gyr —
COL1's own initial condition — must

  (a) not produce a caustic (any shell reaching r = 0) before z = 0; and
  (b) have settled out to at least the KiDS inner-window edge at each of the four masses by z = 0
      (canonical 81 / 272 / 362 / 456 kpc for log M_b 9.4 / 10.45 / 10.7 / 10.9), and
  (c) cover every SPARC galaxy's last measured radius at its own mass (175 of 175) and every RC100
      galaxy's 2.2 R_e at its own mass and redshift (100 of 100) — FLD1's own coverage lines.

**FIRE if a caustic forms before z = 0, or if any of (b)/(c) fails.**

## 3. Grading against the record's own numbers

- COL1: fold at 0.52 R_ta (0.51 R_ta at the shock); chi-shell first crossings outside 10 kpc at z 4.1-6.2 and
  outside 100 kpc at z 2.3-2.8; only 1.0-4.0 % of the law's halo charge turned around by z = 0.
- FLD1: R_fold(0) = 62 / 139 / 169 / 197 kpc at log M_b 9.4 / 10.45 / 10.7 / 10.9 (canonical);
  R_fold/R_ta = 0.52 today at every mass; KiDS inner window 1.30 / 1.95 / 2.15 / 2.32 times *beyond* R_fold(0);
  middle window 3.06 / 4.57 / 5.03 / 5.43 times beyond.

DT2 passes only if it beats these on (b) and (c), and only if K1 and K2 also hold.

## 4. Label set

Pre-registered label set (the same label must come out on both footings):
`REACHES`, `DOES NOT`, `BREAKS DOWN`, `FOLDS`.
Any K firing sets the label; if no K fires, the label is `REACHES`.

## 5. Derived value and residual

- **Derived value (primary):** `R_set(0)` — the radius at z = 0 out to which the clock has settled into the
  static state — at log M_b = 10.45, reported with the ratio `R_set(0)/R_fold(0)` against FLD1's own 139 kpc
  and against the KiDS inner window edge 272 kpc.
- **Residual per mass:** `|M_settled(<r) - M_b X(x)| / (M_b X(x))` at `r` = the KiDS inner-window edge, for
  each of the four masses, each footing. (Form B: `X = (sqrt(1+4x^2)-1)/2`, `x = r/r_M`, `r_M = sqrt(G M_b/a0)`.)

## 6. Footings

canonical a0 = 9.3603e-11 m/s^2; alt a0 = 1.1312e-10 m/s^2. G = 6.6743e-11, c = 299792458, K = 4 pi G.
**Never pooled.** Every table is reported per footing; the label must be identical on both.
