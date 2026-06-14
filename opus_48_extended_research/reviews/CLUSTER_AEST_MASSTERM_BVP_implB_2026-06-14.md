# Implementation B — AeST scalar mass term vs the cluster deficit eta~2.15 (independent BVP cross-check)

**Date:** 2026-06-14 · **Opus 4.8 work folder** · Companion code: `cluster_aest_massterm_BVP_implB.py`
**Grade: FALSIFIED-AS-CLOSURE** (the mass-term route is NOT a first-principles cure; bank it as a prediction).
**Relation to Implementation A (`cluster_aest_massterm_derivation.py`):** independent method + independent
baryon profile, **AGREES with A** and sharpens *why*.

## The job
Solve the FULL nonlinear AeST scalar mass-term equation independently of Implementation A (which shoots on
the phase-space momentum with a point-mass baryon source). Implementation B uses (i) a **scipy collocation
BVP** (`solve_bvp`) cross-checked against a **phase-space IVP march**, and (ii) an independent baryon
profile: **beta-model hot gas + Hernquist BCG** (A uses a point mass). Same framework `a0=9.36e-11`, same
single CMB-pinned `1/mu`, held identically for clusters and galaxies. `mu` is a FREE AeST constant — NOT
`a0/Z` derived (flagged; the quarantine holds — `a0/Z` is never asserted as derived here).

## The equation (grounded in the literature, text extracted from the source PDFs)
Verwayen, Skordis & Zlosnik 2024 (MNRAS 531 272, arXiv:2304.05134), their Sec. 2.2 — the weak-field
quasi-static scalar sector is an **inhomogeneous Helmholtz** equation,
> `grad^2 Phi + (1+beta0) mu^2 Phi = 4 pi G_N rho_b`,

realized nonlinearly through the modified-Laplacian (MOND) operator. Durakovic-Skordis 2024
(arXiv:2312.00889) Eq. 2.40, spherical:
> `(1/r^2) d/dr[ r^2 M(x) phi' ] + mu^2 phi = 4 pi G_N rho_b`,  `x=|phi'|/a0`,
> `M(x)=(sqrt(1+4x)-1)/(sqrt(1+4x)+1)`  (M->1 Newton, M->x deep-MOND).

I solve it in the **canonical-momentum variables** `P := r^2 M(x) phi'` (the Durakovic-Skordis 2023
Hamiltonian form that removes the oscillatory zero-crossing singularities; my naive direct-`phi` Newton
diverged on those steep crossings — exactly the artifact the lit warns about, line-confirmed). At `mu=0`,
`P'=0 => P=G_N M_enc = const`, recovering EXACT MOND. The acceleration is `g=phi'` (signed; the force can
go repulsive in the oscillatory regime).

## The load-bearing physics: `+mu^2` makes this OSCILLATORY, so `phi(inf)->0` does NOT fix the solution
This is the single most important finding, confirmed directly from the lit text (Verwayen+ Sec. 2.2.4,
4.2.3): the **+mu^2** sign is a **Helmholtz** operator. Its homogeneous solutions are
`[A cos(mu r)+B sin(mu r)]/r` — **oscillatory, both branches decaying as 1/r**. So `phi(inf)->0` is satisfied
by an entire one-parameter family; it does **not** select a unique solution. Verwayen+ carry an explicit
**free boundary constant** `chi_hat_out` (parameterized by `Delta`, deviation from the value maximizing the
MOND->mu transition scale `r_C`) and state the zero-point is "**arbitrary**". The force "can become
repulsive" beyond `r_C` (the negative-phantom-mass deficit).

My solver reproduces this verbatim: forcing the mass term ON gives a repulsive-onset oscillation (first
zero-crossing ~2.5 Mpc for `M=5e14`), and **the |phi| envelope decays ~1/r for EVERY value of the free
constant** (`max|r*phi|` ~ const across 2-38 Mpc). So `phi(inf)->0` holds for the whole family while
`eta@R500` slides freely. **That is the falsification of "natural BC closes it": there is no single
physical BC — the boundary is genuinely degenerate, and a finite-radius free constant sets eta.**

## Numbers (real python; all reproduced in the companion script)

**Validation.** `mu=0` phase-space IVP reproduces analytic MOND to 5 sig figs at R500 and at r=0.3-4 Mpc
(ratio 1.00000). The collocation BVP and the IVP march **agree** (gA/gMOND@R500: BVP −1.0445, IVP −1.0439).
**B's solver on A's EXACT point-mass setup reproduces A's deficit: gA/gMOND(R500)=+0.2038 (A reports 0.206)
— a 1% cross-implementation match.**

**eta at R500 (the central number).** With the literature's "natural" inner anchor (`phi0=-a0 x0 r0`,
= A's convention, held identical for all clusters):
- A's point mass (`g_bar/a0=0.44` at R500): **gA/gMOND = +0.20, gA/g_needed = +0.50 — a DEFICIT.**
- B's beta+BCG profile (`g_bar/a0~0.03` at R500, deep-MOND — the realistic eRASS1 regime):
  **gA/gMOND = −1.04, gA/g_needed = −0.70 — a DEFICIT/repulsive at R500.**
Either way, **the non-tuned BC does NOT give the +2.15 boost** — it gives a deficit, the sign of the
discrepancy eRASS1 actually has, but here as an AeST *failure to lift*, not a cure.

**The tuning cost.** Sliding the free constant `dphi0` walks `gA/g_needed@R500` monotonically from the
deficit through **2.15 to large/repulsive** (e.g. for B's profile, dphi0 from 0 -> −2.7e12 moves
gA/g_need 0.50->1.40; reaching ~2.15 needs a specific dphi0 ~ −few×1e12 to −1e13 that differs per cluster
and per profile). **eta=2.15 is REACHABLE only by a per-cluster boundary tune — not predicted.**

**eta(M500) trend (fixed non-tuned anchor, identical across mass).** gA/g_needed@R500 = +0.33 (1e14) ->
−0.27 (2e14) -> −0.43 -> −0.56 (5e14) -> −0.63 -> −0.69 (1e15): **STEEP and mostly a deficit**, with the
helpful peak parked at ~2.6-3.4 Mpc (>> R500). eRASS1 wants **FLAT ~2.15 with the boost AT R500**. Mismatch
in both amplitude AND mass-trend.

**Radial shape (M=5e14).** ~MOND in the core (0.97 at 0.3 Mpc), falls through R500 (−1.0 at 1.3 Mpc), DIPS
repulsive just past R500, far peak ~5-8 Mpc — a **peak-then-dip whose helpful peak is at the wrong radius**.
eRASS1 needs a sustained ~2x THROUGH R500; AeST gives a dip there.

**Galaxy safety (SAME mu, clean mass-ON vs mass-OFF differential test).** SPARC-like M*=6e10, exp disk:
dev = −0.004% (10 kpc), −0.05% (20 kpc), −0.16% (30 kpc), −0.91% (50 kpc). **Galaxies stay MOND-pure at
1/mu=1 Mpc** (matches A's 0.165%). Honest caveat: clusters need a LARGER mu to lift eta, which would grow
this outskirt term — the Mistele+2023 galaxy<->cluster scale tension, surfacing independently here.

## Verdict: FALSIFIED-AS-CLOSURE (independently confirmed)
Two independent implementations (A: shooting + point mass; B: collocation-BVP/march + beta-model+BCG)
**agree**: with one CMB-pinned `1/mu` and a non-tuned boundary, the AeST mass term gives a **deficit
(~0.2-0.5x, even repulsive for a realistic deep-MOND baryon profile) at R500**, not the +2.15x boost; 2.15
returns only under a **per-cluster boundary tune** (Verwayen `chi_hat_out`); the mass-trend is steep (wrong
shape) and the helpful peak sits at the wrong radius. The deeper reason — newly made decisive here — is that
the `+mu^2` term is a **Helmholtz (oscillatory) operator**, so `phi(inf)->0` is **degenerate** and cannot
fix the amplitude; the eta is set by a free finite-radius constant, exactly the lit's "arbitrary" zero-point.
Galaxies remain MOND-pure at the same mu. **The mass-term route is a genuine intrinsic AeST mechanism but
NOT a first-principles cure for eta~2.15 — bank it as a prediction (a deficit, not a boost, under the
physical convention).** Quarantine held: `a0/Z` never asserted derived; `mu` flagged as a free constant.

Sources: Verwayen, Skordis & Zlosnik 2024 MNRAS 531 272 (arXiv:2304.05134, text extracted & quoted);
Durakovic & Skordis 2024 JCAP 04 040 (arXiv:2312.00889); Skordis & Zlosnik 2021 PRL 127 161302
(arXiv:2007.00082); Mistele, McGaugh, Schombert 2023 A&A 676 A100 (arXiv:2301.03499); eRASS1 target
banked from Bulbul+2024 (eta_median~2.15, the repo's `cluster_dsunruh_baryons.py` on N=9830).
