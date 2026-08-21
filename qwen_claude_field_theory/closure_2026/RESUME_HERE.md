# RESUME HERE — state as of 2026-08-20, end of session

## Published
- **v3 (current): DOI 10.5281/zenodo.22044021** — concept `10.5281/zenodo.22036262`
- v1 (22036263) **superseded**: it claimed "one of six mechanisms survives". **WITHDRAWN.**

## The one-line state
**No mechanism survived. The obstruction is ARM-LEVEL, not mechanism-level, and that is proved** —
all four mechanisms reduce to `div[(1 - mu_v/B^2) grad Phi] = 4 pi G rho_b` for a general
`Phi(x,y,z)` with no symmetry assumed. **Which field carries the halo cannot move the Cassini
quadrupole. Only the interpolation function can.** So searching for another mechanism is the wrong
search.

## The calculation that decides the programme (RUN THIS FIRST)
> Does an interpolation `nu(y)` exist that simultaneously (a) fits the SPARC RAR at <= 0.06 dex
> intrinsic with Upsilon inside the Spitzer prior, (b) gives `Q2 <= 5.2e-27 s^-2` at
> `g_ext = 1.9-2.6 a0` computed with the **AQUAL** (not QUMOND) quadrupole, and (c) keeps the 1-AU
> monopole inside per-planet EPM budgets?

**YES** -> the modified-Poisson arm survives and every mechanism reopens.
**NO** -> the arm is closed by a no-go; only entropic / nonlocal / multi-streaming remain.
Validate any Q2 pipeline against the published anchors `q(1)=0.094, q(1.5)=0.159, q(2)=0.221`
BEFORE trusting a single number from it.

**A workflow on exactly this was IN FLIGHT at session end** — run id `wf_fc86867a-c1d`, six routes
(squeeze / revive-C / verlinde / vainshtein / caustics / maxent-nonlocal). Resume with
`Workflow({scriptPath: ".../find-a-survivor-wf_fc86867a-c1d.js", resumeFromRunId: "wf_fc86867a-c1d"})`
— completed agents replay from cache. **Check its journal.jsonl before assuming anything.**

## What is genuinely BANKED (survives everything)
- The halo is a **unique functional of rho_b with ZERO free data** and an **attractor in radius**
  (forward integration from a 10x spurious dark point mass converges by 100 r_M). A real theorem.
- **p_r - p_t is unobservable in the weak field** (exact flat direction). The equation-of-state
  route is not the constraint.
- **Every STATIC single k-essence has p_t = -rho**, any F. Carl's condensate `phi = Q0 t + psi(r)`
  is what escapes it.
- **The khronon cannot produce the amplitude law**, by a scaling theorem (a0 is an acceleration and
  cannot be built from c and G alone).

## DO NOT CITE (new to this session)
- **"one mechanism survives"** — withdrawn in v2.
- **"the amplitude law is a derivation"** — it is EQUIVALENT to `v_c^4 = G M_b a0`, i.e. to flat
  curves at the BTFR value. Four mechanisms return the identical Bekenstein-Milgrom 1984 phantom
  density.
- **"coefficient 1.000000 supports Carl's kernel"** — `mu = x/(1+x)` and `mu = x/sqrt(1+x^2)` give
  it too. It measures the deep-MOND normalisation and nothing else.
- **"1278x / 1544x" ephemeris** — UNDERSTATES by ~27x. Correct: **33,435x / 40,282x** on Mars.
  Two independent derivations. ADVERSE; propagate as a corpus correction.
- **"identifying the scalar with the condensate fixes the double count"** — it does not. The cross
  term is `-kappa^2 s^3/(24 pi)`, needing `s* = 6.7062` against a hard cap `s <= 1/2`.

## Never tried, ranked (a stated limitation of the published work)
1. **Verlinde / entropic** — the ONE published derivation of exactly this amplitude law; its scale
   `cH_0/6 = 1.0914e-10` is **within 3.3% of the ALT footing**. Not a field equation, so it escapes
   every theorem that killed the six.
2. **Caustics / multi-streaming** — could supply the support with NO second field and NO modified
   Poisson, dodging Q2 structurally. Note: the amplitude law IS "singular isothermal sphere with
   `sigma = v_c/sqrt(2)`" exactly, on both footings — a statement about a TEMPERATURE.
3. **Revive Mechanism C** — its ghost refutation covariantised the mediator as a GAUGE vector where
   AeST's is a Lagrange-multiplier-constrained UNIT TIMELIKE vector. May be an artefact.
4. Vainshtein / k-mouflage — the only class that screens the FORCE (the hole that killed two).
5. Nonlocal (Mashhoon, Deser-Woodard); max-entropy; QUMOND; BIMOND.

## Standing
`kappa = 1/2` is **FITTED**. All numbers both footings: `a0 = 9.3619e-11` canonical /
`1.1279e-10` alt. Clusters still ~2x short (pre-existing, inherited).

---

## ⭐ UPDATE — THE ARM IS **NOT** CLOSED (route1B, 25/25)

The kernel question RESUME_HERE named as decisive has an answer: **YES, a kernel exists.**
`route1B_monotone_escape_2026.py`. And Route 1's own monotone no-go **does not reproduce** —
withdrawn, direction: it **manufactured a deficit**.

The standard published family `mu_n(x) = x/(1+x^n)^(1/n)` is monotone (`dmu/dx > 0` proved
symbolically, so AQUAL stays strictly convex and the "unique functional of rho_b" theorem
survives) and clears the squeeze. 175 real SPARC curves, Upsilon refit per kernel, AQUAL:

| kernel | Ups | RAR rms | chi2/dof | **Q2/ceiling** can/alt | 1-AU monopole / Mars |
|---|---|---|---|---|---|
| RouteA/MS08 | 0.62 | 0.0998 | 7.6 | 7.77 / 8.52 (21.6/23.7 sig) | 0 |
| **a0-line (Carl)** | 0.70 | 0.1083 | 21.1 | **5.59 / 6.39 (15.3/17.6 sig)** | 3.34e4 / 4.03e4 |
| mu3 | 0.81 | 0.1179 | 34.0 | 1.55 / 2.44 | 2.80 / 3.70 |
| **mu5** | 0.84 | 0.1233 | 42.4 | **0.39 / 0.82** | 2.7e-8 / 4.2e-8 |
| **mu10** | 0.85 | 0.1266 | 49.1 | **0.08 / 0.21** | 4e-28 |

`mu10` clears across the FULL +-2 sigma of the *measured* Gaia `g_ext` on **both footings**
(0.050-0.351x); `mu5` clears everywhere canonical, and everywhere alt except -2 sigma.

**⭐ AND a0 IS UNTOUCHED: the deep-MOND limit is identical for every `mu_n` to 5e-7 at
y = 1e-12.** So `a0 = kappa c sqrt(G rho_Lambda)`, the amplitude law, the BTFR and the
BTFR-based kappa all survive the kernel swap intact. **The solar system is a statement about
the TRANSITION region, not about a0.**

**THE COST, stated plainly:** the RAR fit degrades, rms 0.1083 -> 0.1266 dex and chi2/dof
21.1 -> 49.1. The a0-line is the better RAR fit; `mu_n` is the only one that survives Cassini.
That trade is the real content and must not be hidden.

## ⚠️ THE BINDING OBSTRUCTION HAS MOVED
**Gate 5 (the double count) is failed or vacuous on EVERY route, and it is KERNEL-INDEPENDENT.
That, not Cassini, is now the wall.** No choice of `mu_n` touches it.

## Other results this run
- **Mechanism C's parallel-mode ghost DOES NOT EXIST** on Carl's own a0-line:
  `K_par = 1 - 2x/sqrt(1+4x^2) > 0` for every real x, no root (400 samples, 26 decades).
  `c_T = 1` exactly; transverse modes `c^2 = 1` exactly; Cherenkov cleared. **v2's ghost kill was
  wrong** — flagging it as contested was right. C still dies on gates 2/3.
- **Verlinde**: clears the amplitude law term-for-term (sympy residual 0) and has the fleet's only
  force-screen that comes from *counting* rather than a chosen mu (entropy budget saturating at
  `r_* = 4256 AU` for the Sun; every planet inside; residual EXACTLY zero). But **health CANNOT BE
  POSED** (no action, no field equations, no DOF), and read as published it is 3.77e8x the Mars
  budget. **It genuinely escapes the arm-level Q2 proof by falsifying its hypothesis** — Eq (7.40)
  is an algebraic map, not a PDE for general Phi, so entropic gravity has no EFE at all.
- **A "tuned-zero" bump kernel does NOT reach 0.000x the ceiling** (1.08-1.68x). Do not cite it.

## Owed / unrun
- **Vainshtein / k-mouflage is UNRUN, not dead** — it produced no script and no verdict. It is the
  only class that screens the FORCE.
- **Caustics errored mid-response**; its synthesis row is from a PARTIAL and is not reliable.
- `mu_n` needs: a relativistic host, gate 4 (health) is UNDETERMINED for it, and gate 5 fails.
