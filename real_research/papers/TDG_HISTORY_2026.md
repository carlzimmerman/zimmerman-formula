# Tidal Dwarf Galaxies as a Test of History-Dependent Inertia: How a Long-Memory Kernel Can Leave Young Dwarfs Near-Newtonian

**Carl Zimmerman**
Briar Creek Tech (carl@briarcreektech.com)

---

## Abstract

Tidal dwarf galaxies (TDGs) — condensations formed from tidal debris pulled out of a progenitor disc during a galaxy interaction — are the classic sign-flip test between dark matter and modified dynamics. In $\Lambda$CDM they are born devoid of non-baryonic dark matter and should be Newtonian ($M_{\rm dyn}/M_{\rm bar}\simeq 1$). In *instantaneous* modified dynamics — modified gravity (AQUAL/QUMOND) or short-memory modified inertia — they sit deep in the low-acceleration regime (current baryonic acceleration $g_{\rm bar}/a_0 = 0.015$–$0.073$; Lelli et al. 2015) and should show a large boost, $\nu\!\sim\!6$, $M_{\rm dyn}/M_{\rm bar}\sim 4$–$8$. The best HI kinematics (Lelli et al. 2015, six TDGs) instead give $M_{\rm dyn}/M_{\rm bar}=0.9$–$1.5$: near-Newtonian. Instantaneous modified dynamics over-predicts the rotation velocities even with the external-field effect (EFE), at roughly $2$–$3\sigma$ per NGC 5291 object. This paper reads the same data through a de Sitter–Unruh *modified-inertia* framework with a **committed memory kernel** $\tau_{\rm mem}=2Z/H_\Lambda = 203\,{\rm Gyr}$ (the same kernel used in the relational $\sigma$-spread and SHLEM analyses). Because TDG ages ($\sim\!0.36$ Gyr) are minute compared with $\tau_{\rm mem}$, the debris gas has *not* relaxed to its current deep-regime inertia; its effective inertia should instead be dominated by the $\sim\!10$–$13$ Gyr it spent at higher acceleration in the progenitor disc. Averaging the way the framework's own $\sigma$-spread analysis does — over the convex response $\nu$, not the acceleration — a plausible outer-disc history gives $M_{\rm dyn}/M_{\rm bar}\sim 1.4$–$1.9$: this resolves the gross factor-$\sim\!4$ instantaneous over-prediction but lands at the **high edge of, and mildly above,** the data (over-predicting the older NGC 7252/VCC within their errors), a consistency rather than a bullseye. We stress this is a **plausibility estimate, not a derived prediction**: the map from the memory-weighted history to an effective boost is not pinned by the committed formalism (averaging $y$ vs the response swings it $\sim\!20$–$30\%$), so we frame the result as a hypothesis plus a forecast rather than a firm number. We report it *together with its cost*: under the long-memory reading the framework yields the **same** near-Newtonian TDGs as $\Lambda$CDM, so the classic sign-flip discriminator against dark matter **dissolves** for this framework. The instantaneous-MOND tension is real but re-scoped to modified gravity and short-memory inertia. We flag three caveats — (i) Lelli's non-equilibrium escape is degenerate with the memory reading, (ii) the map from the 203-Gyr acceleration history to an effective boost $\nu_{\rm eff}$ is not pinned by the committed formalism (the estimate is kernel-hostage), and (iii) an earlier pass of this analysis wrongly reported a framework tension by applying the instantaneous-MOND prediction, which we retract here. This paper must not be read as "TDGs show no dark matter" or as confirmation of the framework.

---

## 1. Introduction

Tidal dwarf galaxies occupy a privileged position in the dark-matter-versus-modified-dynamics debate. They form out of gas and stars flung into tidal tails during a major interaction (Bournaud et al. 2007). In the standard cosmological picture their material comes from the *baryonic* disc of the progenitor, not from its extended cold-dark-matter halo; the debris is dynamically cold baryons and any pre-existing halo cannot be efficiently captured into these small, late-forming condensations. TDGs should therefore be essentially free of non-baryonic dark matter and obey Newtonian dynamics on their own baryonic content, $M_{\rm dyn}/M_{\rm bar}\simeq 1$ (Barnes & Hernquist 1992; Bournaud et al. 2007).

Modified-dynamics frameworks make the opposite prediction — *if* they act instantaneously. The internal accelerations in TDGs are low. Using the Lelli et al. (2015) kinematics, the current baryonic acceleration spans $g_{\rm bar}/a_0 = 0.015$–$0.073$, i.e. deep in the low-acceleration regime. Any theory whose boost function responds to the *instantaneous* baryonic acceleration — modified gravity in its AQUAL/QUMOND realizations, or a modified-inertia theory with a short response time — then demands a large dynamical enhancement, $\nu = \sqrt{1+1/y}\to 5.9$ at $y\equiv g_{\rm bar}/a_0 = 0.03$, and hence $M_{\rm dyn}/M_{\rm bar}\sim 4$–$8$. This is the sign flip: dark matter says Newtonian, instantaneous modified dynamics says boosted (Gentile et al. 2007; Lelli et al. 2015). TDGs are one of the few systems where the two pictures diverge cleanly *and* the discriminating variable is a directly observed rotation velocity.

The framework examined here is a de Sitter–Unruh **modified-inertia** theory. Inertia is treated as a *time-nonlocal* response of a body to the de Sitter–Unruh bath it experiences at its own proper acceleration (Milgrom 1994, 1999 for the nonlocal-MI programme and the interpolation kernel). Its acceleration scale is horizon-derived, $a_0 = cH_\Lambda/Z$, with $Z=\sqrt{32\pi/3}=5.789$ posited; this yields a canonical $a_0 = 9.355\times10^{-11}\,{\rm m\,s^{-2}}$ and an alternative footing $a_0 = 1.1305\times10^{-10}\,{\rm m\,s^{-2}}$, both carried throughout. The load-bearing feature for the present analysis is not the value of $a_0$ but the *memory time*: the framework commits to a response kernel with

$$
\tau_{\rm mem} = \frac{2Z}{H_\Lambda} = 203\ \text{Gyr},
$$

the same kernel that produced the SHLEM null (Zenodo 10.5281/zenodo.21458605) and the relational $\sigma$-spread signature (Zenodo 10.5281/zenodo.21421896). A memory that long has an immediate consequence for *young* systems, and TDGs are the youngest galaxy-scale objects with clean kinematics. That is the thesis: on this framework's own committed kernel, TDGs cannot have relaxed into their deep-regime inertia state, so the instantaneous-MOND prediction does not apply to them — with a cost we state up front.

---

## 2. The data and the instantaneous-modified-dynamics tension

The kinematic data are from Lelli et al. (2015, A&A 584, A113 = arXiv:1509.05404), the current best HI observations of TDGs, superseding the earlier and higher velocity estimates of Gentile et al. (2007) that had reported consistency with modified dynamics. Lelli's re-analysis finds systematically *lower* circular velocities, which is what makes the honest test bite. We use six TDGs: the three condensations in the NGC 5291 ring (N, S, SW), two in NGC 7252 (E, NW), and VCC 2062.

For each object we take the baryonic acceleration $g_{\rm bar}/a_0$, the observed circular velocity $V_{\rm obs}\pm\delta V$, the baryonic mass, and the observed $M_{\rm dyn}/M_{\rm bar}$, together with Lelli's own MOND predictions for the isolated case ($V_{\rm ISO}$) and with the external-field effect ($V_{\rm EFE}$), computed at their $a_0 = 1.2\times10^{-10}$. In deep-regime modified dynamics the predicted velocity scales as $V^4\propto a_0$, so moving to the framework footings rescales the velocity by $(a_{0,\rm fw}/a_{0,\rm std})^{1/4}$: a factor $0.940$ for the canonical footing and $0.985$ for the alternative. The lower framework $a_0$ therefore *reduces* the predicted velocity by only $\sim\!6\%$ — nowhere near enough to remove the tension.

| TDG | $g_{\rm bar}/a_0$ | $V_{\rm obs}$ (km/s) | $V_{\rm ISO}$ (canon) | $V_{\rm EFE}$ (canon) | tension (canon, +EFE) | $M_{\rm dyn}/M_{\rm bar}$ |
|---|---|---|---|---|---|---|
| NGC 5291 N  | 0.073 | $45\pm9$ | 72 | 58 | $+1.5\sigma$ | $1.5\pm0.7$ |
| NGC 5291 S  | 0.033 | $35\pm6$ | 71 | 51 | $+2.6\sigma$ | $1.3\pm0.5$ |
| NGC 5291 SW | 0.033 | $28\pm7$ | 58 | 43 | $+2.2\sigma$ | $1.2\pm0.7$ |
| NGC 7252 E  | 0.019 | $18\pm5$ | 49 | 28 | $+2.0\sigma$ | $0.9\pm0.6$ |
| NGC 7252 NW | 0.015 | $21\pm6$ | 59 | 39 | $+2.9\sigma$ | $1.0\pm0.6$ |
| VCC 2062    | 0.022 | $16\pm7$ | 39 | 25 | $+1.3\sigma$ | $1.0\pm0.9$ |

*(Velocities on the canonical framework footing $a_0=9.355\times10^{-11}$; the alternative footing $1.1305\times10^{-10}$ raises each by $\sim\!5\%$ relative to canonical and does not change the sign of the tension. $V_{\rm ISO}$, $V_{\rm EFE}$ from Lelli et al. 2015, rescaled by the deep-regime $V^4\propto a_0$ law.)*

The pattern is unambiguous. All six TDGs are deep in the low-acceleration regime ($g_{\rm bar}/a_0 = 0.015$–$0.073$, every value well below unity), so any instantaneous boost function demands $M_{\rm dyn}/M_{\rm bar}\sim 1/\sqrt{y}\sim 4$–$8$. The data show $M_{\rm dyn}/M_{\rm bar}=0.9$–$1.5$: near-Newtonian. Equivalently, the instantaneous prediction over-predicts the rotation velocity, and it does so *even with* the external-field effect (the EFE columns): the NGC 5291 trio is over-predicted at $+1.5/+2.6/+2.2\sigma$, and the full set at $+1.5/+2.6/+2.2/+2.0/+2.9/+1.3\sigma$.

A naive quadrature over all six gives $5.3\sigma$, but this is not the honest figure: the six objects share systematics — a common EFE model, correlated inclination and distance assumptions, and a shared equilibrium assumption — so the effective tension is closer to the per-object $\sim\!2$–$3\sigma$ seen in the NGC 5291 trio. We quote the honest range: **instantaneous modified dynamics over-predicts TDG velocities at $\sim\!2$–$3\sigma$**, and the EFE is not a sufficient escape. This is a genuine tension for modified gravity (AQUAL/QUMOND) and for any short-memory modified-inertia theory; it flips the Gentile et al. (2007) consistency, which rested on higher assumed velocities.

---

## 3. The framework-first re-read: a frozen disc-era inertia

The tension in Section 2 is a statement about theories that respond to the *current* acceleration. The framework studied here does not. Its inertia is a time-nonlocal response with a committed memory time $\tau_{\rm mem}=2Z/H_\Lambda = 203\,{\rm Gyr}$. The relevant comparison is between this memory time and the age of the material whose inertia we are trying to predict.

TDGs are young. The NGC 5291 system formed in a near head-on collision roughly $360\,{\rm Myr}$ ago; the debris in the other systems is of comparable or somewhat greater but still sub-Gyr age. Taking a representative TDG age of $\sim\!0.36$ Gyr, we have

$$
\tau_{\rm mem} = 203\ {\rm Gyr}\ \gg\ t_{\rm TDG}\sim 0.36\ {\rm Gyr},
$$

and indeed $\tau_{\rm mem}$ exceeds the age of the universe. On the framework's own kernel the debris gas has had essentially no time to relax toward the deep-regime inertia state that its *current* low acceleration would eventually imply. Its effective inertia is instead dominated by the acceleration history it accumulated over the $\sim\!10$–$13$ Gyr it spent as part of the progenitor's disc, before the interaction expelled it into the tail.

This is the same duty-factor argument used in the SHLEM analysis: what enters the boost is a memory-weighted average of the acceleration history, not the instantaneous value, and when the memory window vastly exceeds the time spent in the current state the average is pinned to the earlier, higher-acceleration epoch. Two features of the *committed* formalism make this freeze robust rather than ad hoc. First, the field-theory closure carries a single scale $a_0$ and rejects any orbital-time (dynamical) relaxation corner as a new scale absent from the action; the 203-Gyr memory is therefore orbit-independent, and the debris does not re-equilibrate on a galaxy dynamical time (the natural first objection). Second, the kernel is power-law and non-saturating, so the *residence-time* weight of the recent low-acceleration epoch is $w\sim t_{\rm TDG}/t_{\rm cosmic}\sim 0.36/13.8 \simeq 2.6\%$ — small, but not vanishing.

To turn this into a number we must *assume* a representative disc-era acceleration. Tidal tails are drawn preferentially from the *outer* disc, where $y_{\rm hist}\sim 0.5$–$2$ (the least-bound gas skews toward the low-$y$, higher-boost end). Crucially, we average the way the framework's *own* $\sigma$-spread analysis does — over the **response** $\nu$ (a Jensen gap over the convex $\nu$), not over the acceleration $y$ — giving $\nu_{\rm eff}=(1-w)\,\nu(y_{\rm hist})+w\,\nu(y_{\rm now})$ with $\nu(y_{\rm now}{=}0.03)=5.9$. This is the framework-faithful prescription; averaging $y$ instead (the generic MOND shortcut) yields a systematically *lower*, more favorable boost, and the $\sim\!20$–$30\%$ gap between the two is the dominant kernel-hostage uncertainty (Caveat 2). We emphasize $y_{\rm hist}$ is an assumption, not a trajectory-integrated result, so the entries below are a plausibility estimate, not a derived prediction:

| outer-disc history | response-averaged $\nu_{\rm eff}$ | predicted $M_{\rm dyn}/M_{\rm bar}$ |
|---|---|---|
| $y_{\rm hist}\sim 0.5$ | 1.84 | $\sim1.8$ |
| $y_{\rm hist}\sim 1.0$ | 1.53 | $\sim1.5$ |
| $y_{\rm hist}\sim 2.0$ | 1.35 | $\sim1.4$ |

For contrast, the instantaneous prediction at the TDGs' *current* $y\sim0.03$ is $\nu=5.9$ — the source of the Section 2 over-prediction. The framework's long-memory, response-averaged estimate is instead $M_{\rm dyn}/M_{\rm bar}\sim 1.4$–$1.9$ (central $\sim\!1.5$, higher if the least-bound-gas prior pushes $y_{\rm hist}$ low). This **resolves the gross factor-$\sim\!4$ instantaneous over-prediction** ($\nu\!\sim\!6\!\to\!\sim\!1.5$) but lands at the **high edge of, and mildly above,** the observed range (NGC 5291 trio $1.2$–$1.5$, NGC 7252 and VCC 2062 $0.9$–$1.0$): it over-predicts the older, lower-mass NGC 7252/VCC by a few tenths — within their $\pm0.6$ errors, but a mild over-prediction, not a bullseye. The consequence is asymmetric across the three pictures, and it is worth stating precisely what is and is not established. What follows firmly from the committed kernel is *qualitative*: a 203-Gyr memory forbids a 0.36-Gyr object from having relaxed into its current-acceleration boost, so the framework does **not** inherit the Section 2 over-prediction — that $\sim\!2$–$3\sigma$ tension belongs to instantaneous modified gravity and short-memory modified inertia, which lack the long kernel. What does **not** follow firmly is the *quantitative* landing at $1.4$–$1.9$: that number rides on the assumed $y_{\rm hist}$ and on the averaging rule, so it is a plausibility estimate broadly consistent with (though at the high edge of) the data, not a prediction the framework forces. We therefore advance the near-Newtonian-young-TDG result as a hypothesis and a forecast (§5), not as a firm prediction.

---

## 4. The honest ledger

We now record what is gained and what is lost, both ways, with no manufactured win.

**Gain.** TDGs become a candidate *history-dependence* discriminator. Among the three pictures on the table, instantaneous modified dynamics (modified gravity, short-memory inertia) is the one disfavored by the Lelli (2015) data at $\sim\!2$–$3\sigma$, while long-memory modified inertia and $\Lambda$CDM both survive. This makes TDGs a new member of the framework's history-dependence family alongside the relational $\sigma$-spread and SHLEM — and, unlike those, it is a system where existing data are at least compatible with the memory-kernel direction rather than merely permitting the mechanism in the abstract. The internal-consistency value is real but bounded: what the committed 203-Gyr kernel forces is the *qualitative* verdict (a 0.36-Gyr object cannot have relaxed into its current-acceleration boost, so no large deep-regime enhancement is expected); the *quantitative* agreement with the observed $M_{\rm dyn}/M_{\rm bar}$ additionally requires the assumed outer-disc history and averaging rule of Caveat 2, and should be read as compatibility, not as a fit landed without adjustment.

**Cost (stated prominently).** Under the long-memory reading, the framework predicts the *same* near-Newtonian TDGs as $\Lambda$CDM. The classic sign-flip discriminator — the whole reason TDGs were considered a decisive modified-dynamics test — **dissolves** for this framework. TDGs do *not* distinguish long-memory modified inertia from dark matter. This paper therefore must not be read as "TDGs show no dark matter" nor as confirmation of the framework. It shows only that the framework is *consistent* with the data, at the price of surrendering TDGs as an anti-dark-matter argument.

**Caveat 1 — non-equilibrium degeneracy.** Lelli's own, well-motivated escape for instantaneous MOND is that TDG orbital times greatly exceed their ages, so the discs may not be dynamically settled; an unrelaxed disc under-estimates the circular velocity and hence the enclosed potential. Lelli explicitly states the dark-matter-free conclusion holds *only* assuming equilibrium. That same non-equilibrium correction would rescue instantaneous MOND by raising the true velocities toward the boosted prediction. Consequently "long-memory modified inertia" and "instantaneous MOND plus non-equilibrium" are **degenerate** on current data: the history-dependence reading is *consistent* with the data but is not *uniquely selected* by it.

**Caveat 2 — the $\nu_{\rm eff}$ mapping is kernel-hostage.** The step from a 203-Gyr acceleration-history average to a specific effective boost $\nu_{\rm eff}\sim1.4$–$1.9$ is *not* pinned by the committed formalism, in two ways. (a) It assumes a plausible outer-disc history $y_{\rm hist}\sim 0.5$–$2$ rather than a trajectory-integrated value; the least-bound-gas prior favours the low-$y$, higher-$\nu_{\rm eff}$ end. (b) The averaging *rule* itself is unpinned: averaging the response $\nu$ (the framework's own $\sigma$-spread prescription, adopted here) gives $\nu_{\rm eff}\sim1.4$–$1.9$, whereas averaging the acceleration $y$ (the generic shortcut) gives a lower, more favorable $\sim1.2$–$1.7$ — a $\sim\!20$–$30\%$ swing that is the dominant systematic. The $\nu_{\rm eff}$ figure is a plausibility estimate, not a derived prediction.

**Caveat 3 — self-correction on the record.** The first pass of this analysis reported a $\sim\!2$–$3\sigma$ tension *against the framework*, obtained by applying the instantaneous-MOND (standard-lens) prediction to a framework that commits to a 203-Gyr kernel. That was a category error: the framework is not an instantaneous theory, and its committed kernel forbids the deep-regime boost for objects this young. We retract the adverse framework verdict and re-scope the tension to instantaneous modified gravity and short-memory inertia. This correction is preserved in the reference script (its CORRECTION block) and is stated here transparently rather than quietly overwritten.

The net entry: the framework **passes on its own premises**; the adverse verdict of the first pass is retracted *as a framework claim* and re-scoped; discriminating power against $\Lambda$CDM is lost; a candidate modified-inertia-versus-modified-gravity lever is gained, hostage to equilibrium systematics and to the kernel mapping.

---

## 5. Relation to the history-dependence family, and what would break the degeneracy

The TDG result is not an isolated re-interpretation. The 203-Gyr kernel is a *single* commitment that has already been carried into two other analyses: the relational $\sigma$-spread signature (Zenodo 10.5281/zenodo.21421896), which introduced the memory time and its history-dependence class, and the SHLEM null (Zenodo 10.5281/zenodo.21458605), which shares the identical kernel and duty-factor logic. The formal basis for the kernel is set out in the modified-inertia field-theory results (Zenodo 10.5281/zenodo.21403470). TDGs add a third system in which the same long memory has an observable consequence — here, freezing young debris into a near-Newtonian state — and the consequence is data-facing rather than a forecast.

What the family shares is also its present limitation: every member is degenerate with a more conventional escape on current data (non-equilibrium here; astrophysical scatter and modelling assumptions elsewhere). Breaking the TDG degeneracy specifically requires one of the following.

- **Equilibrium-robust kinematics.** The single biggest confound is whether the observed $V_{\rm circ}$ reflects a settled potential. Stellar and gas kinematics from ELT-class instruments or from wide-field integral-field spectroscopy (MUSE and successors), combined with dynamical-state indicators, could establish whether the near-Newtonian $M_{\rm dyn}/M_{\rm bar}$ is intrinsic or an artifact of unsettled discs. If the discs are demonstrably settled, the non-equilibrium escape for instantaneous MOND closes, and the disfavouring of instantaneous modified dynamics — not of the long-memory framework — sharpens.
- **An age-versus-discrepancy gradient across TDGs.** The distinctive, MOND-impossible prediction of the long-memory reading is that the *degree* of near-Newtonian behaviour should correlate with age. Very young debris ($t\ll\tau_{\rm relax}$) should be most Newtonian (inertia frozen at the disc-era value); progressively older TDGs should drift toward the deep-regime boost as their inertia begins to relax to the current low acceleration. A measured gradient of $M_{\rm dyn}/M_{\rm bar}$ with TDG age — flat and near unity for the youngest, rising for the oldest — would be a genuine history-dependence signature that neither $\Lambda$CDM (which predicts Newtonian at all ages) nor instantaneous MOND (which predicts a large boost at all ages) can produce. **A candid warning on this forecast: within the present six-object sample the sign runs the *wrong* way** — the more evolved NGC 7252 debris shows *lower* $M_{\rm dyn}/M_{\rm bar}$ ($0.9$–$1.0$) than the younger NGC 5291 ($1.2$–$1.5$), the opposite of an older-is-more-boosted trend. This is within the $\pm0.6$ errors and confounded by mass and geometry, but it is not supporting evidence, and an honest test must confront it. Assembling a TDG sample spanning a range of ages, with uniform kinematics, is the observational programme that would turn the present consistency into a test — and could equally kill the reading.

Neither route is available on the Lelli (2015) sample alone, which is why the current status is *consistency*, not confirmation.

---

## 6. Conclusion

Tidal dwarf galaxies are the textbook sign-flip test between dark matter and modified dynamics, and on the best available kinematics (Lelli et al. 2015) they are near-Newtonian: $M_{\rm dyn}/M_{\rm bar}=0.9$–$1.5$, with instantaneous modified dynamics over-predicting the rotation velocities at $\sim\!2$–$3\sigma$ per NGC 5291 object even with the external-field effect, and the lower framework $a_0$ helping by only $\sim\!6\%$. Read through the standard instantaneous lens this is a tension. Read through the de Sitter–Unruh modified-inertia framework's *own* committed 203-Gyr memory kernel, it is not: TDGs are far too young ($\sim\!0.36$ Gyr) to have relaxed out of their inherited disc-era inertia, so the framework does not inherit the deep-regime boost, and on the framework's own response-averaging rule it lands at $M_{\rm dyn}/M_{\rm bar}\sim1.4$–$1.9$ — resolving the gross factor-$\sim\!4$ over-prediction but sitting at the high edge of / mildly above the data, a plausibility estimate rather than a firm prediction, since the map from the memory average to the boost is not pinned by the committed formalism. The tension is real but belongs to instantaneous modified gravity and short-memory inertia, not to this long-memory framework — a correction we make explicitly, having initially mis-assigned it.

The cost is equally explicit: the framework thereby predicts the same near-Newtonian TDGs as $\Lambda$CDM, so TDGs stop being a discriminator against dark matter for this theory. The gain — TDGs as a candidate history-dependence lever, disfavouring instantaneous modified dynamics — is degenerate with Lelli's non-equilibrium escape and hostage to a $\nu_{\rm eff}$ mapping that the committed formalism does not pin down. Whether the lever becomes a test depends on equilibrium-robust kinematics and, most decisively, on the search for an age-versus-discrepancy gradient across a uniform TDG sample. The values of $a_0$, of $Z$, and of the map from the 203-Gyr history average to $\nu_{\rm eff}$ remain posited or estimated, not derived. This paper reports a consistency and a lost discriminator, not a confirmation.

---

## References

- Barnes, J. E., & Hernquist, L. 1992, *Nature*, 360, 715 — tidal-tail formation of dwarf condensations.
- Bournaud, F., et al. 2007, *Science*, 316, 1166 — missing mass / kinematics in tidal dwarf galaxies.
- Gentile, G., Famaey, B., Combes, F., et al. 2007, *A&A*, 472, L25 — TDGs as a MOND test (earlier, higher assumed velocities; reported consistency).
- Lelli, F., Duc, P.-A., Brinks, E., et al. 2015, *A&A*, 584, A113 (arXiv:1509.05404) — best HI kinematics of six TDGs; $g_{\rm bar}/a_0$, $V_{\rm ISO}$, $V_{\rm EFE}$, $M_{\rm dyn}/M_{\rm bar}$; non-equilibrium caution.
- Milgrom, M. 1983, *ApJ*, 270, 365 — the low-acceleration scale $a_0$.
- Milgrom, M. 1994, *Ann. Phys.*, 229, 384 — nonlocal modified-inertia programme.
- Milgrom, M. 1999, *Phys. Lett. A*, 253, 273 — the interpolation kernel $\nu=\sqrt{1+1/y}$ (Eq. 9).
- Kroupa, P. 2012, *PASA*, 29, 395 — dynamical-state cautions for tidal dwarfs.
- Zimmerman, C. — relational $\sigma$-spread signature and the 203-Gyr commitment, Zenodo 10.5281/zenodo.21421896.
- Zimmerman, C. — SHLEM null (same kernel), Zenodo 10.5281/zenodo.21458605.
- Zimmerman, C. — modified-inertia field-theory results, Zenodo 10.5281/zenodo.21403470.

*Novelty note: a literature search found no prior long-memory modified-inertia reading of the TDG data; "no duplicate found" is not "none exists." This work is scoped to the $a_0$ reframing and the history-dependence family, consistent with the author's 2026-06-23 retraction of broader claims.*
