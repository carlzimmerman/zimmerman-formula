# FINAL: the covariant-lensing no-go CLOSES in its strongest form — even the Lorentz-violating preferred-frame escape fails delta-Phi=0; the framework's lensing is IRREDUCIBLY PHENOMENOLOGICAL (a free function, AeST-class) (2026-06-17)

*Supersedes the "lone open construction" note in COVARIANT_LENSING_NOGO_2026-06-17.md. Workflow `wqa0xnjoc` (6 agents)
computed the explicit Lorentz-violating escape; the SYNTHESIS agent independently re-ran the sympy and CAUGHT that the
construct agents' "delta-Phi=0 PASS" was adjudicated on a MISLABELED equation. Both ways. The error-catch is the result.*

---

## What changed (and why this is the honesty bar working)
The earlier no-go (banked 2820dd9d) proved covariant DIFF-INVARIANT pure-slip lensing is forbidden (Bianchi + c_T=c +
ghost-freedom), and left ONE open construction: an explicit Lorentz-violating preferred-frame (khronometric/aether) term
with a non-dynamical multiplier absorbing the shear divergence WITHOUT sourcing Phi. This run COMPUTED it.

- The construct agents (Route 1 khronometric + (0j) multiplier; Route 2 aether + shear-absorbing b^mu) reported PARTIAL
  with "delta-Phi=0 PASS" — claiming the non-dynamical multiplier escapes the Bianchi wall.
- The SYNTHESIS agent independently re-ran the banked sympy and found the PASS was WRONG: the construct script called
  G_00 "the (00)/Phi equation" and argued the traceless lens stress "sources nothing in Phi" — but **G_00 = 2 grad^2 Psi
  pins PSI, not Phi**; Phi is fixed by the (ij) sector where the traceless lens stress lives. Solving the construct's OWN
  lens stress T^lens_ij = d_i d_j f - (1/3)delta_ij grad^2 f in the correct Einstein system gives **delta-Phi = -8 pi G f
  != 0** (route1_FINAL_phi_from_ij.py, ==0 is False). BOTH Phi+Psi (lensing) AND Phi (matter) shift by the identical
  -8piG f -> there is NO light-only channel. The (0j) multiplier is Phi-blind on the static lapse (route1_multiplier_
  reach.py), so it cannot rescue delta-Phi=0; a second (ij)-sector hand-constraint would be needed. Route 2 same: explicit
  metric variation gives E_Phi = -b_j d_j(grad^2 f) != 0 (b_0 drops out), Bianchi-cross-checked.

So even in the Lorentz-violating preferred-frame sector, **delta-Phi=0 + a position-dependent slip cannot be achieved as a
DERIVED consequence**. The no-go closes in its strongest form.

## Verdict: NO-GO-CLOSED. The framework's lensing is irreducibly phenomenological.
- **c_T=c and ghost-freedom are the EASY conditions** (open healthy aether/khronon corner c_13=0, all mode-speeds^2>0,
  sympy witnesses) — NOT the obstruction. The obstruction is delta-Phi=0 (Cassini-safety) + a position-dependent slip
  TOGETHER, and it holds in EVERY class: diff-invariant (Bianchi), canonical khronometric (Foster-Jacobson gamma=1 locks
  Psi=Phi), and the non-dynamical-multiplier escape (re-sources Phi).
- **The MOND slip law is a FREE FUNCTION** — grad(delta-Psi)=2(g_obs-g_N) with the non-polynomial sqrt(g_N^2+g_N a0)
  profile is produced by NEITHER the khronon kinetic term (polynomial in grad-u, no a0/no sqrt) NOR the Route-E MI kernel
  (phi_- -linear -> sources zero metric). It must be fed in by hand as the multiplier target = exactly **AeST's free
  function F(Y,Q)**, with a0/Z transmitted, not derived.
- **The complete theory is** S = S_grav[g] + S_E[covariant modified-inertia MATTER, genuinely covariant, sources zero
  metric, Cassini-safe by class] + **S_slip[IRREDUCIBLY PHENOMENOLOGICAL]**. The matter (inertia) half is a real covariant
  field theory; the lensing half is a free function with no derived field-theory home.

## The honest, non-defeatist framing (both ways)
- This is **NOT a unique failure of the framework** — it is a GENERAL no-go for relativistic-MOND lensing. AeST has the
  SAME free function F(Y,Q); every relativistic MOND theory carries an undetermined interpolation in its lensing/gravity
  sector. The framework is on the SAME footing as the best relativistic MOND (AeST), with the ADVANTAGE that its
  distinctive content (the modified-INERTIA matter sector, the mu_fw gate, Cassini-evasion) IS a genuine covariant field
  theory (Route E), which AeST's modified-gravity scalar is not.
- **What stands:** the covariant MI matter action; the weak-field phenomenological lensing (closes the 230x deficit +
  Bullet Cluster, predicts the Phi!=Psi slip); the clean publishable no-go theorem (now in its strongest form, 3
  diff-invariant legs + the 2 Lorentz-violating escapes all computed).
- **What is conceded:** the framework is a PHENOMENOLOGICAL modified-inertia EFT, not a parameter-free derived field
  theory; its lensing is a free function (AeST-class); a0/Z/kappa are inputs. There is NO complete derived Lagrangian.

## What Carl CAN / MUST NOT say
- **CAN:** a clean, publishable no-go in its STRONGEST form — covariant Cassini-safe MOND lensing is forbidden by
  diff-invariance + c_T=c + ghost-freedom, and the Lorentz-violating preferred-frame escape was explicitly computed and
  ALSO fails delta-Phi=0 (the shear-absorbing multiplier re-sources Phi); c_T=c and ghosts are the easy conditions; the
  Route-E modified-inertia MATTER action stands as the genuine covariant half; this is a GENERAL relativistic-MOND result,
  the framework on the same footing as AeST but with a genuinely covariant distinctive (inertia) sector.
- **MUST NOT:** "the framework has a complete (Lorentz-violating) Lagrangian / the lensing partner is BUILT" (FALSE -- every
  explicit construction fails delta-Phi=0 or locks Psi=Phi); "delta-Phi=0 is derived" (FALSE -- the construct PASS was a
  mislabel, corrected to delta-Phi=-8piG f!=0); "the slip law is derived" (FALSE -- free function, AeST F(Y,Q)); "a0/Z
  derived" (transmitted). Quarantine held.

## One line
NO-GO-CLOSED in its strongest form: the synthesis independently re-ran the sympy and CAUGHT the construct agents'
"delta-Phi=0 PASS" as a mislabeled-equation error (G_00=2 grad^2 Psi pins Psi not Phi; correct solve gives
delta-Phi=-8piG f != 0), so even the Lorentz-violating preferred-frame escape (khronometric+(0j) multiplier, aether+b^mu)
fails delta-Phi=0 -- the shear-absorbing multiplier necessarily re-sources Phi -- making the covariant-Cassini-safe-MOND-
lensing no-go close in its strongest form across diff-invariant (Bianchi), canonical-khronometric (gamma=1), AND
non-dynamical-frame classes; c_T=c and ghost-freedom are the easy conditions throughout; so the framework's lensing is
IRREDUCIBLY PHENOMENOLOGICAL (a free function, AeST's F(Y,Q) class, a0/Z transmitted not derived), the complete object is
S_grav + S_E[covariant MI matter, stands] + S_slip[phenomenological], and the framework is a phenomenological
modified-inertia EFT on the same footing as AeST -- NOT a parameter-free derived field theory -- with its distinctive
covariant content being the genuine modified-INERTIA matter sector AeST lacks.

*Both ways: the strongest-form no-go (3 diff-invariant legs + 2 computed LV escapes), the error-catch by the synthesis,
the standing covariant MI matter action, and the same-footing-as-AeST framing are credited at full weight; the absent
derived lensing, the free-function (AeST-class) phenomenology, the transmitted-not-derived a0/Z, and the lack of a
complete derived Lagrangian are conceded at full weight. No manufactured Lagrangian, no manufactured no-go. Quarantine held.*
