# ROUTE D — the reconciliation: can the AeST dark sector cluster in cluster cores while staying smooth in galaxies? — NO-GO STANDS (2026-06-20)

**Goal (Carl's right move):** before publishing the density-ordering no-go, hunt HARD for the loophole —
a real AeST/ghost-condensate mechanism that clusters at CLUSTER scales (~Mpc) but stays SMOOTH at GALAXY
scales (~kpc), preserving BOTH the CMB 3rd-peak fit AND the galaxy RAR. Candidate the no-go may have
missed: the ghost-condensate k⁴ dispersion ω² = (B/M²)k⁴ − A k² sets a FINITE Jeans wavenumber k_J that
orders BY SCALE, not density — sidestepping "galaxies are denser." Both ways; quarantine (a0/Z/κ/I0 never
derived).

## HEADLINE: the evasion's LOGIC is sound, but it FAILS quantitatively on every leg → THE NO-GO STANDS.

**Credit (both-ways, at full weight):** the k⁴-Jeans mechanism is a REAL physics idea and its sign
topology is exactly right. Sympy-confirmed from the ACLM dispersion: for k < k_J the mode is UNSTABLE
(clumps), for k > k_J it is STABLE (smooth). Since galaxies are SMALLER (larger k) than clusters, IF k_J
sat between them the field would clump in clusters and smooth in galaxies — ordering by SCALE, sidestepping
the density argument entirely. Carl's instinct (this is the loophole to test) was the right move.

**But it dies on three independent, convention-robust legs:**

- **[A] B = 0 in the named host (the root kill).** Blanchet–Skordis 2404.06584 Sec 6.2, verbatim: "there
  are no higher derivative interaction terms in the action, which are also quadratic in the fields"; the
  dark-matter scalar has **dispersion ω = 0** (the non-propagating khronon mode). With B = 0 the k⁴
  stabilization **does not exist** — there is no scale-selection at all. Growth reverts to the mass-term
  gate ρ > μ²/4πG = 1.47×10⁻¹⁰ ρ_crit, which BOTH galaxies (9.7×10¹³) and cluster cores (2.6×10¹³) blow
  past by ~13 orders, **galaxies by 3.7× more**. The ordering is by density and backwards. (Re-confirms the
  banked Door-A pin.)

- **[B] Even granting an idealized GC (B = O(1)), k_J = μ is OUT OF WINDOW.** The window the evasion needs
  is **k_J ∈ [7.5, 314] /Mpc** (λ_J between ~10 kpc galaxy-disk and ~420 kpc cluster-core). AeST's
  galaxy-MOND constraint **μ⁻¹ ≳ 1 Mpc** (Skordis–Zlosnik 2007.00082, verbatim) forces **k_J ≤ 1 /Mpc** —
  **below the window by 7.5×–100×.** At that k_J, BOTH galaxy and cluster-core scales sit on the STABLE
  side → the field is smoothed in cluster cores TOO. Wrong side.

- **[C] The μ-scale contradiction is hard.** k_J = μ **identically** in AeST/ACLM (sympy-exact, banked
  PK_K4_SIGNATURE) — the SAME single μ sets both the galaxy MOND scale and the Jeans scale; **they are not
  independent levers.** Cluster-core-clumpy needs μ⁻¹ < **0.134 Mpc**; galaxy MOND needs μ⁻¹ > **1.0 Mpc**.
  **Contradiction by 7.5×.** No μ satisfies both. (Adversarial two-lever / tuned-B escape: not available;
  raising B only LOWERS k_J, further from the window; AeST has one scalar.)

- **[D] μ screening is wrong-scale help.** μ⁻¹ ≳ 1 Mpc suppresses k < μ (>Mpc supercluster scales),
  leaving cluster cores (k~7.5/Mpc) AND galaxies (k~100/Mpc) — both sub-μ⁻¹ — unscreened. No contrast.

- **[E] CMB 3rd peak forces cs²→0 (cold dust) for k ≳ 0.057 /Mpc.** The only scale-selection lever (k_J=μ)
  is pinned ≲1/Mpc and galaxy-illegal — it cannot simultaneously preserve the peak, clump cluster cores,
  and smooth galaxies.

**Adversarial revival (all fail):** two-lever escape NOT available (one μ; B=0 anyway); nonlinear-MOND
escape is wrong sector (acts on the Y/spatial mode, not the cold Q/dust mode — shift symmetry + a Ward
identity forbid Y→Q sourcing, banked Route-C); "galaxies are denser" is robust (3.7× banked, 370× on a
matched mean-enclosed baryon proxy) → any density-gated mechanism clumps MORE in galaxies.

## VERDICT for the paper
**The paper is the NO-GO, not the galaxy-safe solution.** The k⁴-Jeans evasion is the right idea and the
right place to look — but it is killed at the root (B=0 in the named host) and, even granting an idealized
ghost condensate, the single scale k_J=μ cannot sit in the required [7.5, 314]/Mpc window without violating
galaxy MOND by ~7.5×. The field clusters by DENSITY (galaxies clump more), not by scale — exactly the
no-go's argument. No manufactured loophole; the genuine soundness of the mechanism's topology is credited
at full weight, the quantitative failure conceded at full weight. Quarantine held (a0/Z/κ/I0 never derived).

## Scripts (exit 0)
- `routeD_scale_selective_clustering.py` — the scale window, k_J(M), direction test, B=0 host, μ screening, CMB constraint.
- `routeD_adversarial_signcheck.py` — sympy sign re-derivation + 5 revival vectors, all fail.

## Sources
Blanchet–Skordis 2024 (arXiv:2404.06584, Sec 6.2 — B=0, ω=0 scalar); Skordis–Zlosnik 2021
(arXiv:2007.00082 / PRL 127 161302 — μ⁻¹≳1 Mpc, μ²Φ "akin to ghost condensation", ω²=cs²k²+M²);
Arkani-Hamed–Cheng–Luty–Mukohyama 2004 (hep-th/0312099 — ghost-condensate dispersion ω²=(B/M²)k⁴−Ak²,
k_J=M²/√2 M_Pl). Banked: DOORA_PIN_REAL_COEFFICIENTS_2026-06-19, GHOST_CONDENSATE_CONSEQUENCES_2026-06-19
(PK_K4_SIGNATURE k_J=μ sympy-exact), CLUSTER_RESIDUAL_EXPLAIN_2026-06-20, CLUSTER_CLOSURE_HUNT2_2026-06-20.
