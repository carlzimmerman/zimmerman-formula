# RESUME HERE — state as of 2026-08-20, end of session

## Published
- **v2 (current): DOI 10.5281/zenodo.22036376** — concept `10.5281/zenodo.22036262`
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
