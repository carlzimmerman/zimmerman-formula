# Scalar external-field screen as a Cassini fix — FINAL VERDICT

Constitutive law (frozen): `div[ mu_eff(|DPhi|/a0, e/a0) DPhi ] = 4πG ρ`, with
`mu_eff(x,eps) = 1 − A(eps)·(1 − mu_gal(x))`, `mu_gal(x)=x/√(1+x²)` (Standard),
`A(eps)=1/(1+(eps/eps_s)^m)`, `eps=e²/a0²`, `a0=cq/Z` global so `a0(z)=a0,0 H(z)/H0`.
`e` = scalar elliptic auxiliary (verified 2+0, second-class); BC `e→|g_ext|` in an embedded
subsystem, `e→0` isolated galaxy. Solar external field `g_e=Vc²/R0=2.0726e-10 m/s²`
(Vc=229 km/s, R0=8.2 kpc), so `eps_e=eta²`, `eta=g_e/a0`.

Scripts (both run green): `escreen_Q2_map_2026.py` (validates vs Milgrom Tab.1 to +3.3%,
`nu_eff(A=1)==nu_standard`, `nu_eff(A=0)==1`), `escreen_widebinary_fork_2026.py`.

---

## (1) Q2(m, eps_s) headline — CAN scalar screening beat Cassini while keeping galaxy MOND?

**Yes, on a non-empty region — but only by the same knob that guts the wide-binary boost.**

`Q2 = (3/2) q_screened(eta,m,eps_s) · a0/R_M`, and because
`(1−mu_eff)=A(eps)·(1−mu_gal)`, the whole MOND deviation is diluted **linearly** in
`A(eps_e)`: `Q2(A)/Q2(A=1) ≈ A` (numerically 0.214 at A=0.2). Limits both hold exactly:
`e→0` (isolated galaxy) ⇒ `A→1` ⇒ `mu_eff==mu_gal` to `4.4e-17` ⇒ `v⁴=GMa0` UNTOUCHED;
`A→0` ⇒ `mu_eff→1` and `dmu_eff/dx→0` ⇒ `Q2→0` exactly.

Baseline unscreened quadrupole (all FAIL the Cassini 95% upper of 5.1e-27 s⁻²):

| footing | a0 [m/s²] | eta | eps_e | a0/R_M [s⁻²] | Q2(A=1) [1e-27 s⁻²] |
|---|---|---|---|---|---|
| standard  | 1.20e-10  | 1.727 | 2.983 | 1.141e-25 | 20.40 |
| canonical | 9.362e-11 | 2.214 | 4.901 | 7.862e-26 | 14.66 |
| alt       | 1.128e-10 | 1.838 | 3.377 | 1.040e-25 | 18.87 |

Cassini-passing (`Q2 < 5.1e-27`) requires `A(eps_e) < A_pass = 5.1e-27/Q2(A=1)`:
standard 0.250 (17/40 cells), canonical 0.348 (31–33/40), alt 0.270 (19–20/40). In every
footing the boundary is `eps_s` sitting **below** the solar-neighborhood `eps_e~3–5`, so the
Sun lands on the screened side of the threshold. Larger `eps_e` (canonical) screens most
easily. **The passing region is real.**

## (2) THE TRADE-OFF — is the wide-binary EFE necessarily killed? Give the numbers.

**Necessarily killed. There is NO window at the solar-neighborhood field, because the
quadrupole and the wide-binary boost carry the identical `A(eps_e)`.**

Solar-neighborhood wide binaries (the DR4 sample, at R≈R0) see the same `g_e` ⇒ same
`eps_e` ⇒ same `A`. The radial EFE boost `1/mu_eff(eta,eps_e)−1` collapses with `A` in
lockstep with Q2: numerically `boost(A)/boost(1) ≈ 0.9·A`, so `Q2/boost` is
**A-independent** — you cannot drive Q2 down 3–4× without dragging the boost down the same
factor. At the *least-screened passing* cell:

| footing | least-screened passing cell | A | WB boost (frac of full-MOND) | screened gamma_v |
|---|---|---|---|---|
| standard  | m=2, eps_s=1.5 | 0.202 | +0.028 (18% of +0.1555) | 1.038 |
| canonical | m=2, eps_s=3.5 | 0.338 | +0.031 (32% of +0.0973) | 1.068 |
| alt       | m=2, eps_s=2.0 | 0.260 | +0.033 (24% of +0.1385) | 1.050 |

(Newtonian=1.000; NOVERDICT edge >1.26; registered full-MOND target = 1.2139.) Every
Cassini-passing screen forces the registered `gamma_v=1.2139` down to **~1.03–1.07** — the
DHF "alpha_grav driven to ~0 by Cassini" result relocated, not escaped.

## (3) Does any EFE-observed system survive? — YES, the low-field class.

The systems where EFE is actually *detected* sit at host fields far below `eps_s`, so
`A(eps_h)≈1` (fully un-screened, MOND+EFE alive) even for a screen that kills the Solar
System (m=8, eps_s=3.0):

| system | eps_h | A(eps_h) @ m=8,eps_s=3.0 |
|---|---|---|
| solar-nbhd wide binary | 2.98–4.90 (=eps_e) | 0.28 → SCREENED |
| Fornax dwarf | 0.0102 | ~1.000 → un-screened |
| Crater II | 0.0147 | ~1.000 → un-screened |
| Antlia II / And XIX | 0.0119 / 0.0154 | ~1.000 → un-screened |
| Chae RAR-EFE (e_N=0.03–0.1 a0) | 9e-4 – 1e-2 | ~1.000 → un-screened |

**Genuine daylight** here: the e-screen cleanly separates the Solar System (eps_e~3–5) from
the low-field dwarf-satellite and Chae RAR external-field detections (eps_h~1e-4…5e-2). A
sharp screen (large m) also predicts an abrupt `gamma_v(R)` step in the embedded wide-binary
population across the solar circle (boost 0.045 @ R=8 kpc → 0.224 @ R=10 → 0.311 @ R=12 at
m=16, eps_s=3.0) — a testable, awkward DR4 signature, NOT a rotation-curve distortion
(galaxy interior is e→0).

## (4) HONEST STATUS — viable escape, DR4 fork, or lock relabelled?

**The Cassini↔wide-binary lock is RELABELLED, not escaped.** Solar-neighborhood wide
binaries and the Solar System share `eps_e` by construction, and Q2 and the WB boost carry
the same `A(eps_e)`; a Cassini-passing screen therefore *predicts* near-Newtonian wide
binaries (gamma_v~1.03–1.07). The registered `gamma_v=1.2139` DR4 prediction dies under
**every** Cassini-passing screen. This is not a free fork DR4 gets to swing — Cassini already
forces the horn: if DR4 measures gamma_v~1.2, the quadrupole is back and Cassini fails; if
DR4 measures Newtonian, Cassini is satisfied but the MOND-gravity wide-binary reading is
dead. Either way the registered prediction is the casualty.

**The one real gain is PARTIAL:** genuine daylight for the LOW-FIELD EFE class (dwarf
satellites, Chae RAR detections), which remain un-screened and MOND-alive. That class was
never the locked front. The scalar-e screen buys Cassini + low-field EFE at the cost of the
solar-neighborhood wide-binary prediction; it does not buy all three. The pass also rests on
a **structural, not derived** demand: the elliptic e-BC must treat `g_e~2a0` as "external"
(screen on) for embedded two-body subsystems yet "zero/internal" (A=1, `v⁴=GMa0` exact) for
the Milky Way's own rotation curve at the same R0 — a clean external/internal discrimination
at identical field magnitude, asserted by the BC, not output by the action.

**Bottom line:** CASSINI_PASSABLE = true (non-empty region, `eps_s < eps_e`);
no genuine wide-binary window (gamma_v→1 forced); low-field EFE survives; the specific
Cassini↔wide-binary lock is the lock relabelled.
