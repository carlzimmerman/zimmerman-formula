# hy4_push — The Zimmerman–AeST Completion

A relativistic field theory of gravity built on the Zimmerman acceleration
scale $a_0 = \tfrac12 c\sqrt{G\rho_\Lambda}$.

**This repository is public.** Everything here is written to be read by a
hostile referee. Every lane prints measurement and threshold separately;
every FAIL is kept as a finding; nothing is claimed beyond what was run.

## The theory

$$
S=\int\!\sqrt{-g}\left[\frac{M_P^2}{2}R-\Lambda^4 f(\mathcal{X})
-\tfrac12\xi^2(D^2\phi)^2\right]+S_m[g,\psi]
$$

$$
f(\mathcal{X})=\mathcal{X}-2\ln\!\bigl(1+\sqrt{\mathcal{X}}\bigr)
-\frac{2}{1+\sqrt{\mathcal{X}}}+1,\qquad
f'(\mathcal{X})=\mu_2(\sqrt{\mathcal{X}})=\frac{u(2+u)}{(1+u)^2}
$$

* $\mathcal{X}=h^{\mu\nu}\partial_\mu\phi\partial_\nu\phi/2\Lambda^4$, with
  $h^{\mu\nu}=g^{\mu\nu}-u^\mu u^\nu/u^2$ the spatial projector of a unit
  timelike aether.
* $\xi = 0.045\,\mathrm{pc} = 1.17\,r_M(M_\odot)$, the MOND radius.

The function is **not free** — it is fixed by the SPARC mode count $n=2$.
That is the whole point: in every previous relativistic MOND the free
function is fitted; here it is integrated once from a measurement.

## Four regimes, one action

| Regime | Mechanism | Result |
|---|---|---|
| **FRW** | homogeneity ⇒ $D^2\phi=0$, $\mathcal{X}=0$ | $f(0)=-1$ ⇒ $w=-1$ **exactly**. CMB background is exactly ΛCDM |
| **Galactic** | $(\xi/r)^2\sim3\times10^{-11}$ ⇒ term negligible | sourced AQUAL ⇒ $g^2=a_0g_N$; RAR to **5.9% unfitted** |
| **Solar** | Green's fn $(1-e^{-r/\xi})/r$ — **no $1/r$ inside $\xi$** | $S(1\,\mathrm{AU})=5.8\times10^{-9}$; $\gamma-1,\beta-1,\alpha_1,\alpha_2$ vanish at leading order |
| **Cold** | shift symmetry ⇒ Noether charge | $n\propto a^{-3}$, exactly cold, **no particle, no direct detection** |

Health (checked, not assumed): no ghost ($f'>0$); subluminal and stable
($c_s^2=(u^2+3u+2)/(u^2+3u+4)\in[\tfrac12,1)$); $\rho>0$.

## Lanes

| File | Result |
|---|---|
| `H001_zimmerman_aest_action.py` | **17/17** — the action: one function, three sectors, $a_0=s/2$ |
| `H004_biharmonic_completion.py` | **9/9** — the screening term: solar system recovered, three sectors survive |
| `PAPER_ZIMMERMAN_AeST.tex` | MNRAS-format draft |

## Honest status

**Open:** linear perturbations and CMB acoustic *amplitudes*; $\xi$'s value is
set by the Cassini floor rather than derived; the aether's own dynamics is
inherited; $n=2$ remains a measurement (every derivation route we could
construct is closed, but its necessity is not proven).

**Falsification (pre-registered):**
1. $c_s^2$ leaving $[0,1]$ anywhere — dead (checked on the full branch).
2. CMB acoustic peaks failing at sub-per-cent — dead.
3. $a_0$ off by more than the $\rho_\Lambda$ systematics — dead.
   We get $9.36\times10^{-11}$ vs measured $\sim1.2\times10^{-10}$ (22%).
4. A claimed WIMP detection — dead (the theory predicts none).

## Reproducing

```bash
python3 H001_zimmerman_aest_action.py
python3 H004_biharmonic_completion.py
```

Requires `numpy`, `sympy`. Lean certificates compile with
`lake env lean` against Mathlib v4.34.0-rc2 in
`fable_independent_2026/lean_2026`.
