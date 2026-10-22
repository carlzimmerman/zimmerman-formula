# D7_turnoff_yt — FROZEN CRITERIA (written before any script or number)

Door: the origin of the strong-field turn-off P5, `ν_fix = 1 + (ν−1)/(1+(y/y_t)²)`, `y = g_N/a₀`,
and its scale `y_t` fixed by the closure `I(y_t) = Λc⁴/a₀² = 8π/κ²`.

## Record checked before freezing

`deepseek_push/DS_FINAL_2026_10_21/`: THEORY.md §1 (P5), §3.6 (closure, lines ~440–470, 738–753);
A4_ppn (canonical tail a₀ = 2557.38 B_E; y_t = 66.2999; planet caps; "EFE O(10²) not recomputed");
A25 (kernel L = canonical, Q = quadrature, R = RAR; F_L ~ (π/2)y_t); A28 (y_t is κ in disguise;
local-balance class gives y_t = O(Z⁰) or O(Z¹)); A22/A60 (P-sector hedgehog inside λ, M_crit =
a₀L★²/G = 3.87e5 M⊙); A26 (fork settled LAW-FIRST: medium-first rejected on 45 sub-M_crit dwarfs);
A30 (a_P = GM/L★²); A16, A44, A63; BRIEF.md lines 41–47; CANDIDATE_LAWS_REGISTER rows 676–677, 710;
Zenodo notes (A5) for 23171085 / 23251231; memory note PARAMRED CFG830–835 (read-only).

Disclosure: while reading the record (before this file) I noticed that `(c²/(a₀L★))^{1/5} ≈ 66.4`.
It is pre-declared here as **numerology regardless of outcome** (exponent 1/5 is outside the frozen
exponent set below) and is only tested for robustness (footings, κ points), never promoted.

## Inputs (all labelled)

a₀ = 9.36e-11 (canonical) and 1.13e-10 m/s² (alt), never pooled; Λ = 1.0890e-52 m⁻² (A28); κ = ½ (FITTED),
κ_th = Z/4π (POSTULATE), Z = 2√(8π/3); B_E = 3.66e-14 m/s² and the per-planet bounds of A4 §D6;
L★ = 24 pc (window 24–90), σ_c from L★ = σ_c²/a₀; g_N,gal at the Sun from A60 (u_gal = 0.566 a₀);
A26 numbers (N_below = 45, step c = +0.453 ± 0.099 dex, 21σ) quoted as external input only.

## Checks and pass lines (PASS = the stated claim is what the computation shows)

- **K1** canonical law ⇒ ν−1 = (√(1+4/y)−1)/2 exactly; tail coefficient c = lim y(ν−1) = 1 (quadrature 1/2).
  Pass: sympy residual 0 and limits exact.
- **K2** bare canonical anomaly at 1.5 AU / B_E on both footings. Pass line for "the canonical law needs
  a turn-off": ratio > 1 on **both** footings.
- **K3** EFE: phantom density ∇·[(ν−1)g_N] at 1.5 AU with the Galaxy's Newtonian field added
  (algebraic QUMOND source, Sun + uniform g_e), max relative change vs isolated over directions.
  Pass line for "EFE cannot buy the factor": the anomaly is reduced by less than 2× (|Δρ/ρ| < 0.5),
  and the tidal estimate a₀·r/r_M at 1.5 AU is < 1e-2 a₀.
- **K4** with P5 at the closure y_t (canonical κ=½, alt, thermal) the 1.5 AU anomaly is < B_E. Pass: all three.
- **K5** closure roots reproduce the record (66.2999 at the quoted Λ, a₀; 66.3803 at 32π; 46.0148 alt)
  to 1e-3 relative; thermal-κ root computed and compared with both THEORY values (77.85 and 77.944).
- **K6** closure is a bijection κ ↔ y_t (F strictly increasing); the band [60,140] maps to
  κ ∈ [0.3415, 0.5265] to 1e-3. Pass: monotone and both edges reproduced. (Outcome meaning: the band
  is a κ statement, not an independent y_t measurement.)
- **K7** direct observability of y_t today: (a) largest planetary signal / published bound for
  y_t = 140 (top of band) — pass line for "not measurable now": < 1; (b) wide binaries at the separation
  where y = y_t (2 M⊙ total): fractional change of g between y_t = 60 and 140 — pass line for "not
  measurable now": < 1 %.
- **K8** P-sector stiffness as turn-off: local balance g_N = u²/(a₀−u) + L★²u/r² (anomaly = u exactly in
  spherical symmetry). Show the gradient/saturation ratio in the saturated regime is M_crit/M (no y in
  it), and that the y at which the anomaly falls to a₀/2 differs by > 10× (or exists for one mass and
  not the other) between M = 1e-3 and 1e3 M_crit. Neglected derivative terms must be < 5 % of kept ones
  where evaluated. Pass = "the stiffness turn-off is a mass threshold, not a y threshold".
- **K9** the Sun is below M_crit on both footings over the whole L★ window, so a stiffness cure of the
  planets puts the Sun on the same side of M_crit as the 45 dwarfs A26 uses to reject medium-first.
  Pass = same side for every (footing, L★ ∈ {24, 90} pc).
- **K10** gate representability: under P5 the anomaly A(g) is non-monotone (peak at y_pk, then falls);
  since A = u, g = K W'(u) would be double-valued. Pass: non-monotone for y_t ∈ {60, 66.3, 77.85, 140,
  46.0} and an explicit pair g₁ ≠ g₂ with equal A found to residual < 1e-10.
- **K11** scale candidates from the action, frozen list: accelerations built from {a₀, cH_Λ (= Z a₀ on
  the κ convention of A28), c²/L★}, as y = Z^m R★^n with R★ = c²/(a₀L★), m, n ∈ {−2,−1,−½,0,½,1,2}
  (the trivial m = n = 0 excluded). Pass ("no-go") line: no member lands within 5 % of the closure y_t
  on the canonical κ=½ point **and** the alt point **and** the thermal point simultaneously.
  The disclosed R★^{1/5} is reported with the same three-point test, labelled numerology.

## What each outcome means

K2 PASS ⇒ P5 (or some turn-off) is needed by the canonical law under law-first; K2 FAIL ⇒ P5 drops out.
K8+K9 PASS ⇒ the only action-native suppression (stiffness) cannot be the turn-off without reviving the
medium-first reading A26 rejected. K10 PASS ⇒ P5 cannot live in the gate potential W(u); it needs a new
invariant/coupling with its own constant. K6+K7 PASS ⇒ "y_t tied to Λ" has no testable content today.
Verdict SCOPED NO-GO if K2, K8–K11 pass; CRISP FINDING if K2 fails (P5 drops out) or K11 finds a
three-point member.

## Mutation

`--mutate`: replace the canonical kernel with the RAR kernel (tail c = 0). Must break K1/K2 (no tail)
and K5 (no closure root).
