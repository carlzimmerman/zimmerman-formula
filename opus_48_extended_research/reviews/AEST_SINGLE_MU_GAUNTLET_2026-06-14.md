# The single-mu consistency gauntlet: can ONE CMB-pinned 1/mu keep galaxies MOND-pure AND lift clusters 2x?

*Opus 4.8 (1M), 2026-06-14. Implementation C of the AeST cluster mass-term workflow.
Companion script: `aest_single_mu_gauntlet.py` (full nonlinear AeST scalar EOM, Green's-function
+ BVP, validated against analytic MOND to 0.2%). Grade: **FALSIFIED-AS-CLOSURE.**
Quarantine held: a0/Z never asserted derived; mu flagged a FREE AeST constant.*

## The question
Carl's framework: a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, MOND at z=0, covariant via AeST
(Skordis-Zlosnik 2021). The cluster liability: MOND/AeST misses ~2x the mass at R500 (eRASS1
eta_median ~ 2.15). The one intrinsic AeST candidate is the scalar **mass term mu^2 phi**, with
1/mu ~ 1 Mpc pinned by the CMB acoustic fit. **My decisive constraint:** can a SINGLE mu both
(i) keep SPARC galaxies MOND-pure at 5-30 kpc AND (ii) supply eta~2 at cluster R500?

## The equation solved (full nonlinear, NOT the (mu R)^2 expansion)
Durakovic-Skordis 2024 (JCAP 04 040, arXiv:2312.00889) Eq. (2.40), the quasi-static weak-field
AeST scalar:

```
(1/r^2) d/dr[ r^2 Mtilde(x) dphi/dr ] + mu^2 phi = 4 pi G_N rho_b(r)
   x = |dphi/dr|/a0,  Mtilde(x) = (sqrt(1+4x)-1)/(sqrt(1+4x)+1)   (->1 Newton, ->x MOND)
   g = |dphi/dr|;   mu^2 = 2 K2 Q0^2/(2-K_B),  1/mu ~ 1 Mpc CMB-pinned
```
Solved with the EXACT Mtilde (no leading expansion), realistic baryons (beta-model gas
beta=0.7, rc=0.18 R500, fgas=0.13 + a Hernquist BCG), M500 = 1e14-1e15 Msun, R500 from
500 rho_crit.

## The load-bearing boundary-condition physics (what the prior route got subtly wrong)
The mass term is **+mu^2 phi** -- a POSITIVE-sign Helmholtz operator, **NOT** Yukawa (-mu^2 phi).
With u = r phi, the source-free far field is `u'' + mu^2 u = 0` => `u = A sin(mu r) + B cos(mu r)`,
so **phi = u/r ~ 1/r for BOTH homogeneous modes**. Consequence: **phi(inf)->0 is satisfied
automatically by every mode and does NOT by itself fix the inner constant.** The prior route
shot on a single endpoint value and walked the answer with a free `Phi_shift` -- that is exactly
the under-determination this sign structure creates, and it is why a per-cluster boundary tune
"reached" 2.15.

The UNIQUE physical solution needs TWO conditions: **regularity at r=0** (enclosed-flux inner BC)
AND the **bounded, source-localized standing tail at infinity** (no free homogeneous piece added).
I realize this with the exact spherical Helmholtz **Green's function** (standing/principal-value
kernel, regular at 0, bounded ~1/r at infinity) convolved with the MOND-equivalent source -- the
unambiguous "natural BC, zero tuning" answer. NO per-cluster constant; identical operator for the
galaxy and every cluster.

Validation: as mu->0 the Green's solution reproduces analytic pure MOND at R500 to **0.2%**.
Robustness: eta(R500) is **stable at 0.95-0.96** as the outer cutoff varies 30 -> 125 Mpc.
(The finite-domain `solve_bvp` cross-check returned eta=13 -- a spurious Helmholtz near-resonance
when mu R_OUT lands near a Dirichlet eigen-node; the infinite-domain Green's function is immune
and is the reference. Flagged in-script.)

## RESULTS at the CMB-pinned 1/mu = 1 Mpc (held identical for galaxy + cluster)

**Galaxies stay MOND-pure (PASS).** Across the SPARC mass range (Mbar 1e9-3e11 Msun) at 5-30 kpc,
the AeST/MOND ratio deviates by **<= 0.18%** (max). Galaxies are untouched -- as required.

**Clusters get NO 2x boost (the closure FAILS).** At M500=5e14, R500=1.21 Mpc:
- **eta(R500) = 0.96** -- essentially pure MOND, a slight DEFICIT, not a boost.
- The radial shape is a **shallow peak (eta_pk = 1.09 at ~4.3 Mpc) then a dip** (eta=0.46 at 2 Mpc)
  -- the Durakovic-Skordis "peak-then-negative-phantom" oscillatory RAR. The peak is only +9%,
  sits at the WRONG radius (~4 Mpc, well beyond R500), and the eRASS1 requirement is a SUSTAINED
  ~2.15x out to R500. AeST delivers neither the amplitude nor the shape.
- **eta(M500) trend (1e14 -> 1e15): DECLINING, 1.08 -> 0.79** at R500 -- the WRONG direction
  (eRASS1 is flat-to-slightly-falling at ~2.15) and never above ~1.1 anywhere in the range.

| M500 [Msun] | R500 [Mpc] | g_bar/a0 | eta(R500) | eta_peak | r_peak [Mpc] |
|---|---|---|---|---|---|
| 1e14 | 0.71 | 0.042 | 1.08 | 1.10 | 4.3 |
| 3e14 | 1.02 | 0.058 | 1.03 | 1.10 | 4.3 |
| 5e14 | 1.21 | 0.068 | 0.96 | 1.09 | 4.3 |
| 1e15 | 1.52 | 0.085 | 0.79 | 1.08 | 4.3 |

## Thread-the-needle: NO single mu works
Scanning 1/mu for the value that lands eta(R500)=2.15 (M500=5e14): eta **OSCILLATES** with mu
(1.03 -> 0.75 -> 0.15 -> 0.48 -> 0.94 ...) -- the peak-dip RAR sweeping past R500 -- and **never
cleanly reaches 2.15** for any 1/mu in 0.1-1.0 Mpc. Chasing the cluster by shrinking 1/mu also
breaks galaxies: the galaxy deviation climbs 0.08% (1.0 Mpc) -> 1.7% (0.2 Mpc) -> **5.4% (0.1 Mpc)**.

This independently confirms the **Mistele+2023 (A&A 676 A100)** galaxy-vs-cluster bound: galaxies
MOND-pure needs 1/mu >~ 1 Mpc; a >=10% cluster lift needs 1/mu < 0.63 Mpc -- the windows do not
overlap, and a 2x lift needs mu larger still. One mu cannot do both.

## VERDICT: FALSIFIED-AS-CLOSURE
With the galaxy-safe, CMB-pinned 1/mu=1 Mpc and the **physical** (regular-at-0 + bounded-tail)
boundary condition imposed with **zero per-cluster tuning**, the AeST mass term gives
**eta(R500) ~ 0.96 -- pure MOND, no boost** -- not the eRASS1 eta~2.15. The shape is a shallow
(+9%) misplaced peak followed by a deficit, the eta(M500) trend declines (wrong sign), and no
single mu threads galaxies-MOND-pure AND clusters-2x. The earlier "eta=2.15 reachable" was the
artifact of a free per-cluster boundary shift that the +mu^2 Helmholtz sign structure spuriously
permits -- once the boundary is fixed by the actual asymptotic physics, the boost vanishes.

The mass term IS a genuine intrinsic AeST mechanism at the right SCALE (off in the Solar System
and galaxies, on at Mpc) -- that part is real and confirmed. But it is **NOT a first-principles
cure for the cluster deficit.** Bank it as a prediction: **AeST with the CMB-pinned mass term
predicts clusters stay essentially MOND at R500 (eta ~ 1, NOT 2) -- the eRASS1 ~2x deficit is
NOT closed by this structure.** The cluster liability remains MOND's inherited unsolved problem
(patched only by ~2 eV neutrinos / additional baryonic-dark mass), not resolved by the mass term.

Honesty, both ways: galaxies genuinely pass (0.18%); the scale-onset is genuinely right; the
mechanism is genuinely intrinsic to AeST. The closure genuinely fails on amplitude, shape, AND
trend simultaneously, robustly under the convention-fixed BC. Not manufactured, not dismissed.

Sources: Skordis & Zlosnik 2021 PRL 127 161302 (arXiv:2007.00082); Durakovic & Skordis 2024
JCAP 04 040 (arXiv:2312.00889); Verwayen, Skordis & Zlosnik 2024 MNRAS 531 272 (arXiv:2304.05134);
Mistele, McGaugh & Schombert 2023 A&A 676 A100 (arXiv:2301.03499). eRASS1 eta~2.15: banked workflow value.
