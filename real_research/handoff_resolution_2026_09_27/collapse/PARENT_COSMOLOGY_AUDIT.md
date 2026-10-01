# Independent audit of parent XR23/XR32 reproductions

Audited 2026-09-27, read-only, against preserved results in `real_research/cross_thread_review_2026_09_26` and completed `reproduction/*_py311` main/mutation artifacts. This is an audit of these declared numerical gates, not an independent validation of the observational likelihoods. No new heavy calculation was needed.

| Lane | Preserved failed checks | Fresh main failed checks | What changed |
|---|---|---|---|
| XR23 mass-function ceiling | H1 (reported, not load-bearing) | H1 and K1 | Strict FP13 reproduction fails: maximum absolute boost drift 1.3108929e-5 exceeds 1e-9; no scientific hypothesis changes verdict. |
| XR32 matter power | H1e | H1e, C1, C2 | Exact-equality reference controls fail at 1.1e-16 and 2.2e-16; every scientific H-check retains its verdict. |
| XR32 consistency | H3b, H3d | H3b, H3d | Parent comparison has zero differences; no changed gate verdict. |

All three fresh main processes return 1. That common exit status must not be interpreted as three new scientific exclusions. XR32's preserved main results already failed their stated hypotheses. XR23's new load-bearing failure is the numerical reference control.

## Scientific meaning retained by the reruns

XR23 H1's broad abundance bound remains false: reading T differs by 22.44%, beyond its 10% threshold; reading B differs by 0.03%. The actual observed-cell efficiency comparison B4 still passes (0.08%/0.01% deviations from LCDM), while the sharp top-hat bracket gives 12.58%. High-redshift linear-power control K4 still has zero difference. The largest new K1 drift is the z=0, k=1 boost, 1.9221777816685215 to 1.9221908905973133. This fails the declared reproduction accuracy; it does not overturn the high-redshift or observed-cell ceiling conclusions. The mass-function run consumes the preserved collapse-threshold JSON, whose SHA256 is `49f7bf3f148de247dbc896b0e78b870d33baf8942a5a0038cf2743cc53ec73a8`; it is not a fresh end-to-end substitution of new collapse barriers.

XR32 matter power retains its suppression results: sigma8 ratio 0.9310–0.9496, S8 0.7738–0.7893; representative nonlinear ratios 0.377/0.358. H1e's proposed 1.7-Mpc phantom more-than-restoration fails on both footings, with ratios 0.904/0.982 rather than >1. This is a preserved failed hypothesis, not a new consequence of the fresh runtime. Exact component recombination and no-conversion identity controls C3/C4 still pass.

XR32 consistency retains H3b's failure of the declared |A−1|≤0.023 gate: A_band=0.9757, A_cv=0.9542. Against the source's actual ACT center 1.013±0.023, the band result is −1.62 sigma, so the failed unity-centered one-sigma gate is not a >2-sigma ACT exclusion. H3d retains the f-sigma8 proxy discrepancy: implied sigma8=0.7676 versus 0.842±0.034, −2.19 sigma (LCDM −0.91 sigma). This proxy is not a full joint DESI likelihood. H3c's count-equivalent S8 values 0.768/0.800/0.805/0.813 lie below Planck 0.831; that passed direction-of-change test does not establish agreement with every cluster survey. H3e's lensing-equivalent +0.098-eV neutrino shift is a scoped degeneracy estimate; the printed 4.9×0.020-eV comparison is not a 4.9-sigma joint mass exclusion.

## Mutations and provenance

The mutations reach and fail meaningful scientific gates rather than merely returning nonzero because of the reference drift. XR23's removed band-pass causes B4 to fail (infinite reading-T efficiency discrepancy). XR32 matter's no-conversion mutation fails H1a/H1c/H1d/H1f, with unit power/growth ratios and zero recapture difference; H1e becomes true under the changed model, which does not rescue the main. Consistency's no-conversion mutation fails H3a/H3c/H3e, while H3b/H3d become true at LCDM and its controls remain true.

Fresh environment: Python 3.11.15, NumPy 1.26.4, SciPy 1.11.4, CLASS 3.3.4.0 local vanilla build, arm64; dependency path `/private/tmp/handoff-python311-20260927/site`. Main runtimes are about 6.16, 125.05, and 116.96 seconds. Every audited opened input hash is unchanged (15/8/7 inputs), and each main source hash matches before/after:

- XR23: `eec33cc65beed97be74ff596d1ae6006dda7036cb1745a5e6d3f47a4caa1d4c9`.
- XR32 matter: `05cd7effed0735777bc4995c9052bd39b5139fcdb0bacf16a4b659ba98a1f2cf`.
- XR32 consistency: `22c012e5619bb5fa34a167697388ddf8062c5e84fbe40f319ff27467c9cb624d`.

The new reference deviations are therefore genuine failures under the declared strict comparison rules with unchanged source and inputs. The preserved runtime is not fully pinned by these artifacts, so the precise origin of XR23's 1e-5 drift cannot be uniquely assigned to an individual library or compiler. XR32's 1–2e-16 differences are at ordinary floating-point roundoff scale. Neither warrants rewriting a preserved scientific gate as newly failed or silently relaxing its registered numerical tolerance.
