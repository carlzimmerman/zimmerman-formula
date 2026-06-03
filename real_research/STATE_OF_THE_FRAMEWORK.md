# State of the framework — the foundational risk, and a complete consequence map

**Carl Zimmerman · June 2026** · *the honest current picture: what the framework rests on, what
follows from it, where it wins, and where it fails. Companion to `COMPLETE_ASSESSMENT.md` (the
demolition→survivor arc) and the two technical papers.*

---

## 0. The one thing to read first — the foundational risk

Everything below is **conditional on MOND being a real description of nature** — that a₀ is a
genuine acceleration scale, not an artifact of dark matter. That premise is **not settled, and is
under serious, active challenge.** The honest risk hierarchy is:

1. **Is MOND real at all?** — *unresolved, the foundation.*
   - **Wide binaries:** Banik, Pittordis, Sutherland et al. (2023, MNRAS 527, 4573) find Newtonian
     gravity preferred at **16–19σ**, excluding MOND, from Gaia DR3 wide binaries. **But** Chae
     (2023–2026), using similar data, finds the *opposite* — a MOND-consistent anomaly at high
     significance. The two disagree over hidden triple companions and sample cuts; the test is
     systematics-limited and methodology-dependent. **Genuinely unresolved.**
   - **a₀ universality:** Rodrigues et al. (2018) and 2024 follow-ups argue a₀ is *not* universal
     across galaxies (rejecting MOND-as-fundamental at >5–10σ); McGaugh/Kroupa rebut these as
     prior/systematic artifacts. **Also contested.**
2. Is a₀ specifically *cosmological and evolving*? — a ~2σ hint, ΛCDM-degenerate on amplitude.
3. Is the coefficient Z derivable? — **no** (a posit; the number-field argument forbids an entropy
   derivation of 2√(8π/3)).

**If #1 falls, the framework dies at the root** — there is no a₀ to evolve. A reasonable physicist
can read the current literature as leaning *against* MOND. So the honest framing of this whole
project is a **conditional**: *if* MOND is real, *then* here is how its scale evolves and what
follows. Read everything below in that light.

---

## 1. The one original claim

Stripped of inherited MOND and the dead numerology, the framework's distinctive content is best
stated not as the redshift evolution alone but as the **density law** behind it:

> **a₀ = (c/2)·√(Gρ)** — the MOND scale is set by the *ambient density* ρ.

This has **two** faces, and I had only been testing the first:
> - **(cosmic)** ρ = ρ̄(z) gives **a₀(z) = a₀(0)·E(z)** — the evolution (Milgrom's 2014 idea).
> - **(environmental)** ρ = the *local* ambient density (Mpc-smoothed) gives a **larger a₀ inside
>   overdensities** — so clusters (a ~200× overdensity) get a₀ ~14× cosmic, ≈ what they *require*.

The environmental face is the sharper, more distinctive claim (it is *not* just Milgrom 2014; it is
kin to EMOND, Hodson–Zhao 2017, but parameter-free). It predicts **a₀ varies with environment** —
the make-or-break test (and the reason the a₀-universality debate, §0, matters so much). The
framework adds a covariant realization (Paper I), a linear-CMB-safety proof (Paper II), and the
consequence map below. Everything that is *not* the density law is inherited from Milgrom (1983) and
Skordis–Złošnik (2021). **Caveat:** the coarse-graining scale in "ambient ρ" is currently an input,
not derived — the central open problem.

---

## 2. The complete consequence map (all conditional on §0)

Honest labels: **[DERIVED]** forced; **[FOLLOWS]** clean but weaker; **[DEGENERATE]** real but not
distinct from ΛCDM; **[HINT]** ~2σ data; **[LIMIT]** a genuine failure; **[OPEN]** unsettled test.

### Cosmology
| consequence | result | status |
|---|---|---|
| a₀-cosmography → H₀ | H₀ = Z·a₀/c = **71.5 km/s/Mpc** from SPARC (in the tension band) | **NEW** |
| a₀-cosmography → q(z) | a₀'s *slope* gives the deceleration: q₀ = −0.527 (= ΛCDM); **dark energy from rotation curves** | **DERIVED** |
| expansion shape | a₀(z)/a₀(0) = E(z), the Z-independent probe of w(z) | NEW, systematics-limited |
| dark-sector floor | a₀ → a₀(0)√Ω_Λ = 0.99×10⁻¹⁰ ∝ √Λ — one scale, matter end + Λ end | **FOLLOWS** (Milgrom's √Λ link) |
| BAO ruler | r_s = 144 Mpc unchanged (a₀ absent from linear pert.) + a new a₀-vs-BAO H(z) cross-check | **DERIVED** |
| linear CMB | running a₀ leaves C_ℓ exactly invariant (δq⁰⁰=0; Paper II) | **DERIVED** |
| two-regime universe | linear growth a₀-free (ΛCDM); galaxies MOND | **DERIVED** |
| second-order CMB | estimated ~0.01–0.1%, soft (𝒴^{3/2} non-analyticity) | **OPEN** |

### Galaxies
| consequence | result | status |
|---|---|---|
| phantom "dark" halo | ρ_ph = √(M_b a₀/G)/(4πr²) — isothermal ∝1/r², no DM, ∝√E(z) (×3.2 by z=6) | **DERIVED** |
| BTFR / Faber–Jackson | v⁴=GMa₀, σ⁴=(4/9)GMa₀; zero-point ∝ −log E(z) | **DERIVED** (evolution) |
| Freeman surface density | Σ_c = a₀/(2πG) = 137 M⊙/pc², ∝E(z) → 1428 by z=6 | **DERIVED** |
| galaxy lensing | lensing mass ≈ dynamical mass (phantom halo lenses), ∝√E at high z | **FOLLOWS** |
| the JWST cascade | M_dyn/M⋆∝√E, v∝E¼ … one E(z) | **DEGENERATE** (ΛCDM apparent a₀ also ∝E) |
| **EFE redshift-weakening** | η = g_ext/a₀(z) ∝ 1/E(z) — high-z galaxies more isolated-MOND | **the one distinctive test** |

### Local systems
| consequence | result | status |
|---|---|---|
| solar-system EFE | Galaxy's field = 1.74 a₀ > a₀ → EFE hides MOND locally | **DERIVED** (why MOND isn't glaring) |
| dwarf spheroidals | σ depends on host distance (EFE); **Crater II: predicted ~2 km/s, obs ~2.7** (ΛCDM ~4) | **DERIVED** — a MOND win |
| Local Group timing | MW–M31 boost ~58× supplies the timing mass on baryons | **FOLLOWS** + velocity tension |
| wide binaries | nominally ~0.7 a₀ but EFE-suppressed | **OPEN/contested** (§0) |
| secular drift | ȧ₀/a₀ ≈ −3×10⁻¹¹/yr | **DERIVED**, unmeasurable |

### Conceptual
| consequence | result | status |
|---|---|---|
| a₀ is emergent | a constant can't evolve; a₀∝cH ⇒ emergent gravity (Verlinde/Padmanabhan) | **HINT** (~2σ) |
| Mach's principle | MOND switches on when a particle's Rindler horizon ~ the cosmic horizon | **FOLLOWS** |
| "why now" dissolved | a₀∝cH holds at *every* epoch; constant-a₀ requires the coincidence | **DERIVED** |
| acceleration hierarchy | a₀ at the cosmic-minimum end of a ~62-order span; the "geometric mean" coincidence is **false** | **FOLLOWS** |

### The failures — stated plainly
| failure | why | status |
|---|---|---|
| **galaxy clusters** | MOND needs a₀ **~10–13× the galaxy value, rising inward** (Blaksley & Bonamente 2009, 38 clusters). This is the WRONG test of a₀(*z*) but the RIGHT test of **a₀=(c/2)√(Gρ)**: a cluster is a ~200× Mpc-scale overdensity, so the *density* formula predicts in-cluster a₀ ≈ √200 ≈ **14× cosmic** — on the required value — and ∝√ρ(r), rising inward as observed. The residual that leaves standard MOND ~3× short **closes to ~1.0**. Standard MOND (universal a₀) cannot do this; cf. EMOND (Hodson & Zhao 2017), but the √ρ form is **parameter-free**. **Caveats:** needs ρ = *Mpc-smoothed ambient* density (local clumpy reading gives a₀ ~10³× too big in galaxy disks); possible core over-prediction; predicts **environmental a₀-variation** (cluster galaxies > field) — testable, in tension with strict RAR universality. `reviews/cluster_a0_from_density_HIS_FORMULA.py` | **OPEN / promising** — a distinctive density-a₀ mechanism, *not* the failure I'd called it |
| **the Bullet Cluster** | the lensing convergence (Clowe 2006) is reconstructed *model-independently* — the offset onto the galaxies is geometric, **not** an a₀/GR assumption. The naive "MOND lensing must track the gas" is **wrong**: QUMOND phantom mass is nonlinear in baryon *density*, so κ can peak off the gas (Angus+06). Hernandez 2026 (arXiv:2604.10811) claims a **pure-baryon constant-a₀ QUMOND fit** (offset+amplitude); arXiv:2605.10022 + my own toy (`reviews/bullet_qumond_redo.py`) find the effect too weak / a residual remains. **Genuinely contested in 2026 — not a clean falsification, not cleanly resolved.** a₀-evolution is irrelevant (+17% at z=0.3). | **CONTESTED/OPEN** (inherited, constant-a₀) |
| **cosmic DM budget** | the galaxy phantom halo is local; it does *not* supply Ω_DM≈0.265 — AeST needs the separate 𝒬-sector dust mode. "Dark matter" here is **two things**, not one | **LIMIT** |
| **the coefficient Z** | a posit; provably not entropy-derivable (square-root vs rational) | **LIMIT** |

---

## 3. The Bullet Cluster, since you asked — *corrected after re-examination*

I earlier called this a clean "inherited, unsolved failure" needing ~2 eV neutrinos. **That was based
on the 2006 consensus and is outdated; the honest 2026 status is *contested*.** Here is the corrected
picture, built from the actual measurement papers (`reviews/bullet_qumond_redo.py`):

**How it was measured.** Clowe et al. (2006) reconstruct the weak+strong-lensing **convergence map
κ(x) model-independently** — *no* assumption about the gravity law or a₀. So the famous **offset**
(κ peaks on the galaxies, displaced from the dominant X-ray gas) is a geometric fact about where
light bends. a₀ enters *only* when a theory tries to predict κ from the baryons. (The *amplitude* —
the factor ~7–8 "missing mass" — does depend on the gravity law; the *offset* does not.)

**The naive disproof is wrong.** "MOND gravity sits on the gas, so κ must peak on the gas" is the
*linear* caricature. In MOND/QUMOND the phantom mass is a **nonlinear functional of baryon density**,
so κ need **not** trace the baryonic surface density (Angus, Famaey & Zhao 2006 — *"κ can be non-zero
where there is no projected matter"*). Compact galaxy concentrations source a sharply-peaked phantom
(Σ_p ∝ 1/R), diffuse gas a flat one — so the minority, compact galaxies can dominate the convergence.

**Where it stands in 2026 — genuinely split.** Hernandez (2026, arXiv:2604.10811) computes constant-a₀
QUMOND for the real Bullet baryons and claims it reproduces **both the offset and the amplitude with
pure baryons, no neutrinos** (galaxies = 7% of baryons but ~48% of phantom mass). Against that:
arXiv:2605.10022 still finds a **residual** missing mass centred on the galaxies, and **my own
independent toy** (a fair test with the gas dominating the baryonic Σ) finds the density-weighting
**too weak to flip the lensing peak** unless the galaxies are modelled very compactly — so I *cannot*
certify the pure-baryon fit. Net: **the offset is no longer the airtight falsification it is sold as,
but it is not cleanly resolved either.** An open, actively debated problem.

**What this means for the framework.** The Bullet is **constant-a₀ MOND** through and through —
a₀-evolution changes nothing (+17% at z≈0.3). So it neither falsifies nor supports the framework's
one distinctive idea; it rides entirely on the **foundational** question already flagged as risk #1
in §0 (*is MOND real?*). It is **not** an independent kill-shot. *(Minor correction to the earlier
draft: the original repo's own script logged the Bullet as "challenging but not fatal," not "solved" —
less of an overclaim than I first said.)* And the separate, deeper **cluster residual-mass problem**
(MOND under-predicts relaxed-cluster masses by ~2×) remains a genuine inherited MOND weakness,
independent of the Bullet offset (see the "galaxy clusters" row above).

---

## 4. The honest pattern, across every domain

| | finding |
|---|---|
| **galaxy-scale wins** (rotation curves, BTFR, lensing, dwarfs, Local Group) | real but **inherited from Milgrom** — evidence for MOND, not for *this* framework |
| **cluster residual / Bullet** | the relaxed-cluster ~2× residual is real and **inherited**; the Bullet *offset* is now **contested** (Hernandez 2026 vs the residual literature), not a clean failure — either way **inherited** MOND, not fixed nor tested by evolution |
| **the only distinctive content** | the **high-redshift evolution** (a₀∝E(z)) and its consequences — the EFE-weakening, the a₀-cosmography (H₀ and q from galaxies), the BAO cross-check |
| **the foundation** | **conditional on MOND being real — currently unresolved (§0)** |

## 5. Bottom line

The framework is a **well-built conditional structure on contested ground.** If MOND is real, it
adds exactly one original idea — that the scale evolves — and from that follows a genuinely new
capability (read H(z) and q(z) off galaxy dynamics), one clean distinctive test (the EFE weakening
at high z), and a tidy covariant realization that is provably CMB-safe at linear order. It inherits
MOND's galaxy-scale successes *and* MOND's cluster/Bullet failure unchanged. Its coefficient is a
posit. And the whole edifice rests on a question — *is MOND real?* — that the wide-binary and
universality literature has **not** settled and may answer "no."

That is the truthful state of it: **original in one place, inherited in most, failing where MOND
fails, and conditional on a foundation still under fire.**

---

*Reproducibility (the derivations behind each row):* `reviews/provable_consequences_with_data.py`,
`reviews/more_derivations.py`, `reviews/widening_consequences_phd.py`,
`reviews/widening_lensing_bao_LG_dsph.py`, `reviews/efe_evolution_forecast.py`; the foundational
risk in the Banik (2023, MNRAS 527, 4573) vs Chae (2023–2026) wide-binary literature; the Bullet
Cluster in Angus, Famaey & Zhao (2006). Papers I & II in `papers/`.
