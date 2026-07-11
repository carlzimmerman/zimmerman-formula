# There Is No Dark Matter in Galaxies

## A staked position: what galaxies call "dark matter" is the cosmological constant at work — the MOND scale is derived from $\Lambda$, the lensing is strained dark energy, and the whole claim lives or dies on one measurable number

**Carl P. Zimmerman** · Briar Creek Tech · 2026-07-11 · *Position whitepaper*

---

### The claim, in one breath

The flat rotation curves of galaxies, the tight radial-acceleration relation, and the weak-lensing signal attributed to dark-matter halos are all manifestations of a single acceleration scale that is **not a new constant of nature but a derived property of the vacuum we already measure**:

$$\boxed{\;a_0 \;=\; \frac{c}{2}\sqrt{G\rho_\Lambda}\;=\;c^2\sqrt{\frac{\Lambda}{32\pi}}\;=\;9.36\times10^{-11}\ \mathrm{m\,s^{-2}}\;}$$

The dark-energy density $\rho_\Lambda$ — the same number that accelerates the cosmic expansion — sets, through the de Sitter horizon's Unruh temperature, the acceleration at which matter's response to gravity departs from Newton. Below that acceleration, galaxies do what they are observed to do — with **no dark matter anywhere in the account**. Where dark matter is invoked for gravitational lensing, the working source in this account is **the dark energy itself, elastically strained by the baryons** — the one dark component we already know exists, doing double duty. And the position stakes its life on a single falsifiable statement: **$a_0$ must track the dark-energy density, $a_0(z)\propto\sqrt{\rho_{\mathrm{DE}}(z)}$** — a prediction the current DESI era is positioned to test within this decade.

We are aware this is a strong position. This whitepaper states it plainly, itemizes the evidence chain (every link a published, machine-verified computation), states with equal plainness what is *not* claimed, and pre-registers the observations that kill it.

### Five claims

**C1 — The scale is derived, not fitted.** The MOND acceleration $a_0$ is the surface-gravity scale of the dark-energy horizon: $a_0=c^2\sqrt{\Lambda/32\pi}$. The functional dependence on $\Lambda$ is forced by dimensional analysis once the identification is made; only the $O(1)$ normalization $Z=\sqrt{32\pi/3}$ is an input (and it cancels in the falsifiable ratio of C5). To our knowledge — after an explicit survey of every relativistic MOND-class theory in the literature (TeVeS, AeST, the khronon, $f(Q)$, nonlocal metric MOND, emergent gravity) — **no other theory derives this scale; all insert it by hand.**

**C2 — It fits the real sky with one physical parameter.** On all 175 SPARC galaxies (3,389 measured points), the law $g_{\mathrm{obs}}=\sqrt{g_{\mathrm{bar}}^2+g_{\mathrm{bar}}a_0}$ at the derived $a_0$ reproduces the radial-acceleration relation to $0.108$ dex with a single stellar mass-to-light ratio inside its independently measured range — marginally tighter than standard MOND's own fit. The interpolation between the Newtonian and deep regimes is not chosen: it is fixed by the Deser–Levin temperature of an accelerated observer in de Sitter space.

**C3 — The dynamics is modified inertia, and it is a real theory.** The account is developed covariantly: general relativity untouched, a passive cosmic-rest frame with provably zero propagating degrees of freedom, the MOND content carried by a causal, bounded, nonlocal operator in the matter sector. Machine-verified: closed constraint algebra, ghost-free two-point sector, gravitational waves at exactly $c$ (GW170817 satisfied identically), and the solar-system quadrupole that excludes modified-gravity MOND at $6$–$14\sigma$ is evaded because the inertial response is trajectory-dependent.

**C4 — Lensing does not send you back to dark matter; it sends you to dark energy.** We proved a structural trilemma: *no* pure modified-inertia theory can bend light correctly on one metric with no dark component — the enhancement must touch curvature. There are exactly two dark-matter-free ways to do that, and we computed both against the Cassini bound. The surviving best road is the one native to this framework: **the dark-energy medium itself, modeled as a relativistic elastic solid whose relaxed state *is* the cosmological constant, strained by the baryons and gravitating as a real source.** Its written action reproduces the required lensing profile — shape, per-galaxy scaling, and amplitude to $1.8\%$ ($\sqrt{Z/6}=0.982$, a genuine numerical coincidence with Verlinde's independently derived elasticity coefficient) — with a derived response cutoff at $y_c=Z/2$ pinned to Verlinde's own published entropy budget. Light bends because strained dark energy gravitates. **Nothing in this account is a new particle.**

**C5 — The whole position is falsifiable by one number.** If $a_0$ is built from $\rho_{\mathrm{DE}}$, then $a_0(z)=\tfrac{c}{2}\sqrt{G\rho_{\mathrm{DE}}(z)}$. The posited normalization cancels in the ratio $a_0(z)/a_0(0)$, so this is parameter-free. If dark energy is exactly a cosmological constant, $a_0$ is constant and this framework dissolves into ordinary MOND — distinctive content gone, honestly. If dark energy evolves (as DESI's current expansion history hints), $a_0$ *must* evolve with it — measurably, in high-redshift rotation curves and the baryonic Tully–Fisher zero-point.

### Why we can say this now

The position rests on a two-year computational program in which **every load-bearing claim is backed by a committed, runnable, adversarially verified script in a public repository**, and every major result carries a DOI: the covariant completion and its radiative structure (one and two loops, the scale unrenormalized); the lensing trilemma with its last loophole closed by direct computation [10.5281/zenodo.21312377]; the elastic-medium action with its solar-system cost reduced to a single material constant [10.5281/zenodo.21303747]; the derived response cutoff pinned to the published literature [10.5281/zenodo.21300855]; and the full synthesis with real-data figures [10.5281/zenodo.21312654]. The program's own false steps — a disformal lensing construction killed by GW170817, a mis-stated magnitude claim, an early over-broad framing — were found by its own verification discipline and corrected *in public, in versioned records*. A position paper this bold is only worth writing on top of that kind of audit trail.

### What we are *not* claiming

This section is load-bearing. **Not claimed:** that this is a theory of everything (earlier overclaims to that effect were publicly retracted in June 2026 and are not reasserted); that the normalization $Z$, the sign of the inertial response, or the Standard Model follow from the framework (they are inputs or untouched); that the solar-system question for the lensing medium is closed (it reduces to one undetermined material constant — the shear Poisson ratio — whose natural values sit a factor $\sim1.1$–$1.8$ over the Cassini bound: formally open, honestly tilted, and stated on the record); that clusters are solved (the residual cluster-core deficit is shared with all MOND-class theories; our cutoff neither cures nor materially worsens it); or that any single existing dataset confirms the evolving $a_0$ (the current fronts are consistent, not yet decisive). **The claim is the position and its falsifiability — not a completed final theory.**

### The wager: what kills this

We pre-register the kill conditions, because a bold position that cannot lose is not physics.

1. **DESI DR3 and successors return dark energy to an exact cosmological constant** ($w=-1$ at high confidence): the distinctive content of C5 dissolves. The framework survives only as a reading of constant-$a_0$ MOND — the position as staked here is gone.
2. **Confirmed evolving dark energy with a flat or anti-tracking $a_0(z)$** (high-redshift rotation curves / BTFR zero-point failing to follow $\sqrt{\rho_{\mathrm{DE}}(z)}$): direct kill of C5, and with it the identification C1.
3. **A dedicated solar-system fit** (Cassini-class ephemeris quadrupole, or the fixed-direction $\bar s^{TX}$ boost-dipole at the CMB apex, decisive with Gaia DR4-era ephemerides ~2028–2032) **finding the modified-gravity signature where modified inertia predicts evasion** — or tightening the quadrupole bound below the elastic medium's floor: kills C3 or the C4 road respectively.
4. **A galaxy-scale aligned external-field asymmetry at the AQUAL amplitude** (the directional-EFE test, fully specified and pre-registered in the repository; needs $\sim10^3$ galaxies with per-side kinematics and reconstructed environmental field vectors): kills the suppressed-shear medium.
5. **A deep-core cluster lensing RAR at $\sim0.01$ dex precision showing no break at $y_c=Z/2=2.894$** where the derived cutoff demands one: kills the medium's budget structure.

If, instead, dark energy keeps evolving and $a_0$ tracks it; if the quadrupole fits keep landing where modified inertia — and only modified inertia — predicts; if the break at $y_c$ shows up when the data reach it: then the least-added-structure account of galactic gravity on the table is this one, and the dark-matter particle era in galaxies is over.

### What it would mean

If this position survives its tests, the ledger of the universe simplifies radically. The two dark sectors collapse into one: **dark energy is real and does everything** — it accelerates the cosmos, it sets the acceleration scale of every galaxy through the horizon it generates, and, strained by baryons, it supplies the lensing mass we have spent forty years attributing to undiscovered particles. The "coincidence" $a_0\sim c\sqrt{\Lambda}$ that every student notices and every textbook waves away becomes the central physical fact it always looked like. Galactic dynamics becomes a *probe of the vacuum*: every rotation curve is a measurement of $\Lambda$, and every high-redshift disk is a measurement of the dark-energy equation of state. And the decades-long null record of direct-detection experiments stops being a puzzle — there was nothing there to detect.

That is the position. It is bold because the evidence chain now permits it, bounded because honesty demands it, and falsifiable because otherwise it would be worthless. The data will decide. We are content to wait.

### Record

Companion records (all Zenodo, all with committed verification scripts): flagship synthesis [10.5281/zenodo.21312654]; lensing trilemma v3 [10.5281/zenodo.21312377]; elastic-medium action v3 [10.5281/zenodo.21303747]; $y_c=Z/2$ cutoff [10.5281/zenodo.21300855]; program concept [10.5281/zenodo.21253644]. Repository: the public zimmerman-formula archive; every figure and number regenerates from committed scripts.

*Both $a_0$ conventions carried in all quantitative companions. Every claim here is labeled: C1–C5 staked, the not-claimed list binding, the kill conditions pre-registered. No theory-of-everything claim is made or implied.*
