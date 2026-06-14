# ROUTE B — LSS / turnaround matching: does cosmology fix chi_out universally? — VERDICT: UNIVERSAL-BUT-DEFICIT (2026-06-14)

*Opus 4.8. Independent of Route A (envelope-min BC). The question: the +mu^2 Helmholtz
operator leaves a FREE boundary constant chi_out (Verwayen-Skordis-Boehm 2024, their
chi_hat_out, Eq.18-20). Route A killed it by minimizing the outer oscillation (=> deficit).
Route B asks the physical alternative Carl posed: a cluster detaches from the Hubble flow
at the TURNAROUND radius r_ta (~few Mpc); beyond r_ta the field is the surrounding
cosmological/LSS background, not a decaying isolated tail. So the boundary condition is
Phi_bar(r_ta) = Phi_bg(z), matched to the COSMOLOGICAL background — one prescription for
every cluster. Companion script: `cluster_routeB_turnaround_matching.py`.*

---

## VERDICT: **UNIVERSAL-BUT-DEFICIT** (the BC is genuinely universal — and that *kills* it)

> The turnaround/LSS matching DOES fix chi_out from cosmology to a single universal
> prescription — chi_out = Phi_bg(z) = 4 pi G rho(z)/mu^2 — with **no per-cluster knob**.
> But that physically-derived value is **~100x too small to bite**: it gives
> **eta(R500) = 0.63 – 1.03 (mean ~0.90), a mild DEFICIT**, the SAME deficit Route A
> found — NOT the eRASS1 ~2.15 boost. The matching is honest and universal; it simply
> lands on the deficit. **This is NOT a tune-in-disguise, and NOT a cure — it is a clean,
> physically-pinned confirmation of the deficit, by a second independent route.**

The crux number, both ways:
- **Cosmologically-fixed** chi_out = Phi_bg(matter, z=0.3) = **4.7e9 (m/s)^2 = (69 km/s)^2**
  -> eta(R500) = **0.94** (5e14 cluster).
- **Required** chi_out for eta=2.15 = **-4.5e11 (m/s)^2 = -(671 km/s)^2** — **95x larger**
  in magnitude, comparable to the MOND potential depth itself. Cosmology supplies ~1%
  of what the boost needs.

## The physics (the genuine result)

**1. chi_out IS fixed by cosmology, and IS universal.** The cluster mass-term equation
(Durakovic-Skordis 2024 Eq.2.20/2.33) `Lap(Phi_bar) + mu^2 Phi = 4 pi G rho_b` has, on the
homogeneous cosmic background (Lap = 0, rho_b -> rho_mean), the particular solution
`Phi_bg(z) = 4 pi G rho(z)/mu^2`. The localized cluster solution must approach THIS as
r -> r_ta. The value depends ONLY on z (cosmology) and mu (CMB-pinned) — **NOT on M500 or
any per-cluster property**. In Verwayen's normalized units chi_hat_out = chi/sqrt(G M a0),
the matched value is a fixed, tiny **chi_hat_out ~ 0.004–0.012** for ALL clusters (vs
Verwayen's O(1) free Delta). It is the literal opposite of a per-cluster tune.

**2. The AeST condensate is dust-like, so chi_out is set by rho_mean over a screening
length 1/mu.** The cosmological AeST scalar (Durakovic-Skordis 2014, p.5; phi = Q0 t + varphi,
their Eq.2.14) has energy density scaling like dust, ∝ (1+z)^3, and the mass
mu^2 = 2 K2 Q0^2/(2-K_B) (their Eq.2.18) is set by Q0 at the minimum. With the CMB-pinned
1/mu = 1 Mpc, Phi_bg = 4 pi G rho/mu^2 is the cosmic-mean potential built up over ONE Mpc:
~(70 km/s)^2. A cluster's own MOND potential depth at R500 is ~(1100 km/s)^2. The background
is ~250x shallower in potential (~16x in velocity), so matching to it barely perturbs the
interior. **The same short screening length 1/mu = 1 Mpc that makes the BC universal makes
it negligible.**

**3. eta(M500) is mass-DECLINING, not flat.** d eta/d log10(M500) = -0.24 (matter match),
-0.30 (total) — the heavier the cluster, the bigger r_ta and the deeper its own well
relative to the fixed Phi_bg, so the universal BC matters even less. This is the WRONG sign
and far too steep vs eRASS1's flat ~ -0.03 at 2.15. A cosmological-BC origin does NOT
reproduce the observed flatness at the 2.15 level — it reproduces a declining deficit.

## Both-ways robustness (the #1 rule — checked, NOT a convention artifact)

- **rho choice** (matter (1+z)^3 condensate / Lambda floor / total): eta(R500) = 0.90 /
  0.90 / 0.90 — identical to 3 figures. The deficit is insensitive to which cosmic density
  sources Phi_bg, because ALL of them give Phi_bg ~ 5e9–9e9 (m/s)^2 << MOND depth.
- **sign of the match** (over-density potential vs potential well, +/-): mean eta 0.896 vs
  0.880 — the deficit holds either way.
- **z_formation** (0.2 -> 1.0): eta(R500) walks only 0.938 -> 0.975 for the 5e14 cluster.
  Even matching at z_f = 1 (Phi_bg 3.6x larger) leaves eta < 1. The formation-redshift
  freedom — the ONLY cluster-to-cluster handle — moves eta by <4%, nowhere near 2.15.
- **required vs supplied**: bisecting, eta=2.15 needs |chi_out| = 4.5e11 (m/s)^2; cosmology
  supplies 4.7e9. The 95x shortfall is the robust truth.

## Is it a TUNE-IN-DISGUISE? NO.

The matching value Phi_bg(z) = 4 pi G rho(z)/mu^2 contains zero per-cluster free parameters:
rho(z) is the cosmic mean, mu is the one CMB-pinned constant (identical to the galaxy run),
z enters only through cosmology. The Verwayen free constant Delta is set to its
cosmologically-determined value (chi_hat_out ~ 0.004, i.e. Delta ~ -chi_hat_out^(max), a
FIXED number), not slid per object. **Route B does NOT smuggle a knob.** That is exactly
why the verdict is honest: a genuinely universal, physically-derived chi_out exists, and it
gives the deficit.

## How this lands vs the workflow's three outcomes

- NOT **MATH-WORKS-FROM-FIRST-PRINCIPLES**: the universal chi_out gives eta ~ 0.9, not 2.15.
- NOT **TUNE-IN-DISGUISE**: no per-cluster parameter hides in the matching.
- It is **STILL-DEFICIT**, reached by a second, independent, fully-physical route. Route A
  (minimize outer oscillation) and Route B (match the cosmological background at r_ta) —
  two different boundary prescriptions, the SAME deficit eta ~ 0.6–1.0. The convergence is
  the point: **whichever physical prescription you adopt for the Helmholtz constant, you get
  the deficit. The 2.15 boost lives only at chi_out ~ MOND-depth, which neither the
  oscillation floor nor the cosmological background supplies.**

## chi_out — the deliverable values (z ~ 0.3)

- **chi_out = Phi_bg(z=0.3) = 4 pi G rho_m(z)/mu^2 = 4.7e9 (m/s)^2 = (69 km/s)^2**
  (matter); = 4.7e9 (Lambda floor); = 9.4e9 (total). Normalized: chi_hat_out ~ 0.004–0.012.
- **This is ONE prescription for all clusters** (modulo z_f, which moves eta <4%). Universal.
- It gives **eta(R500) = 0.63–1.03, mean 0.90** — a deficit, same sign and size as Route A
  and as MOND's known cluster shortfall.

## What Carl CAN / MUST NOT say

- **CAN:** "The cluster Helmholtz boundary constant chi_out is NOT free — cosmology fixes it
  universally to chi_out = 4 pi G rho/mu^2 ~ (70 km/s)^2 via turnaround matching, with no
  per-cluster knob. Solved this way, AeST predicts clusters stay ~MOND at R500 (eta ~ 0.9,
  a mild deficit), confirming Route A by a second independent route."
- **MUST NOT:** "the cosmological boundary value closes the 2.15 deficit" — it is ~100x too
  small. Reaching 2.15 requires chi_out ~ MOND-depth (~(670 km/s)^2), which no physical
  prescription (oscillation floor OR cosmological background) supplies. The 2.15 remains
  MOND's shared, inherited, UNSOLVED liability.

*Quarantine held: a0 and the c^2 sqrt(Lambda/32pi) coefficient never asserted derived; mu is
the free CMB-pinned constant (1/mu = 1 Mpc), identical galaxies<->clusters. No manufactured
cure; no reflexive dismissal — a universal, physically-pinned chi_out genuinely exists, and
it lands on the deficit, both ways.*

Sources: Verwayen, Skordis & Boehm 2024, MNRAS 531 272 (arXiv:2304.05134) — chi_hat_out,
Eq.18-21, Delta=0 maximal-r_C; Durakovic & Skordis 2024, JCAP/arXiv:2312.00889 — Eq.2.14
(phi=Q0 t+varphi), 2.18 (mu^2=2 K2 Q0^2/(2-K_B)), p.5 (Q=Q0+I0(1+z)^3, dust-like condensate),
2.20/2.33 (mass-term Helmholtz); Skordis & Zlosnik 2021 PRL 127 161302 (AeST).
