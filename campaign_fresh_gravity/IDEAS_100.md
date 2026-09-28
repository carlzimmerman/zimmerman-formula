# 100 ideas, written after the 2026-09-27 results

Why these should beat the earlier seed list: astra's 2,000 seeds (`deepseek_push/astra_spawn_ideas/`) were written
before today's results. Each idea below does four things:
- starts from what the record now knows (lane or commit cited);
- aims at one of the few real bottlenecks;
- names a decisive test that uses data or machinery already on disk;
- states its cost in constants and the result that would kill it.

The base is the core framework, a₀ = κc√(Gρ_Λ) with κ = ½ fitted and flat in z, plus the target law of CFG4. That
target law needs:
- a galaxy law that is on only in bound systems;
- a cold component that behaves as cold dark matter elsewhere;
- a phantom edge;
- the max rule.

The field in each entry labelled "Cost" is the change in the constant count: −1 removes a constant, 0 leaves the
count unchanged, +1 adds one.

## The top ten, ranked

1. **FG001: hierarchical MOND.** The phantom belongs only to the outermost bound system.
2. **FG016: the phantom edge derived as the first-apocentre (splashback) caustic.** This is the one ingredient CFG4 is
   missing.
3. **FG097: a one-command gate harness.** It scores any candidate law on every model-independent gate in minutes.
4. **FG004: the max rule derived as the ground state of the framework's coherent field.**
5. **FG041: tidal dwarf galaxies.** The cleanest kill test for FG001.
6. **FG040: embedded vs isolated dwarfs.** The same stellar mass, a different law predicted.
7. **FG029: ξ removed.** The Solar System is screened by being embedded, not by a length.
8. **FG053: a three-way Gaia DR4 registration.** Hierarchy (γ = 1), chain (1.07), external-field MOND.
9. **FG063: the Local Group with the edge.** The phantom ends near 0.3–0.5 of the turnaround radius; R0 recomputed.
10. **FG061: cosmology passes by construction.** A bound-only phantom that equals the cold component, verified on CMB
    lensing, S8, the forest and cluster counts.

---

## A. Principles that could produce the target law (FG001–FG015)

**FG001. Hierarchical MOND.**
- **Idea.** The MOND phantom belongs only to the outermost bound, virialized system. Satellites, star clusters, the
  Solar System, wide binaries and cluster members are embedded systems. Each one is Newtonian in its own frame, plus
  the host's field and its own cold component.
- **Decides.**
  - It removes ξ: the Solar System is screened by being embedded.
  - It makes wide binaries and globular clusters Newtonian.
  - It turns the external-field problem into a rule about who owns a phantom.
- **Test.** Run the gate harness (FG097) on four populations:
  - isolated SPARC and Local Volume dwarfs: predicted MOND with no host effect, matching CFG1's +0.080 ± 0.047;
  - MW and M31 satellites: predicted Newtonian plus a cold halo;
  - Coma UDGs: embedded, so dynamically hot is natural;
  - Cassini: no MOND quadrupole.
- **Cost:** −1 (ξ).
- **Kill:** tidal dwarfs show a MOND-like discrepancy (FG041), or cluster spirals follow the RAR more tightly than cold
  halos allow.

**FG002. The free-fall-frame kernel.**
- **Idea.** The kernel's argument is the acceleration relative to the top-level system's freely falling frame, so a
  uniform external field drops out exactly. Derive this as the unique frame-covariant choice. It supplies XR36's
  missing prescription and FG001's frame.
- **Test.** KiDS with the web's field (FP23's machinery) must fall from +111–153 to ≤ +9.
- **Cost:** 0.
- **Kill:** a clean external-field detection above 3σ; CFG1 rates Chae's signal contested.

**FG003. A bound-state action.**
- **Idea.** A multiplier field enforces "this region is bound": negative binding energy against the Hubble flow. That
  defines where the phantom lives, with no threshold constant.
- **Test.** Conservation; the XR18-style symbol and second variation.
- **Cost:** 0.
- **Kill:** an ill-posed symbol at the bound surface.

**FG004. The max rule as a ground state.**
- **Idea.** In a bound region, the coherent field minimizes its energy at fixed total amount. Show that the minimizer
  sits on the phantom profile ∇·[(ν−1)g_bar]/4πG wherever that exceeds the cosmic share, and spreads as cold dark
  matter elsewhere. That derives CFG4's T5.
- **Test:** X-COP totals (CFG4's 0.946 ± 0.080) and SPARC.
- **Cost:** 0.
- **Kill:** the minimizer is not the phantom profile.

**FG005. Gravity reads bound mass only.**
- **Idea.** The kernel's source is the baryonic mass inside the bound region, not the local density: a causal,
  nonlocal ledger. The web gets no MOND, so CMB lensing is safe by construction.
- **Test:** XR26's lensing amplitude must return to 1.000; FP23's KiDS; XR28's splashback.
- **Cost:** 0.

**FG006. Continuous Hubble-flow screening.**
- **Idea.** The response scales as max(0, 1 − θ_b/3H), where θ_b is the baryon flow's expansion. It is reversible, off
  in the web, and fully on once the flow has turned around.
- **Test:** XR36's scripts, KiDS and the forest.
- **Cost:** 0.
- **Kill:** DE12-type growth at the θ_b = 3H surfaces.

**FG007. The virial clock.**
- **Idea.** A system owns a phantom once its crossing time is shorter than the vacuum time 1/√(Gρ_Λ) = κc/a₀. That
  derives "virialized" from the base's own rate, with no new constant.
- **Test:** classify the Local Group (not virialized, so each giant is top-level), groups and clusters, then score them.
- **Cost:** 0.

**FG008. The phantom as the vacuum's response to bound matter.**
- **Idea.** Only matter that has decoupled from the expansion sources a vacuum response of strength a₀. Derive the
  response kernel from one energy statement against ρ_Λc².
- **Test:** the SPARC RAR shape.
- **Cost:** 0.
- **Kill:** it reproduces ν only with a fitted shape parameter.

**FG009. Two-fluid bookkeeping.**
- **Idea.** Baryons plus one cold component, where the phantom is a state of the cold component (CFG4 T5), not extra
  mass. Write the energy–momentum ledger and check it conserves.
- **Test:** the Bullet offsets (CFG4: 4.6×, 4.9×; 194–209 kpc).
- **Cost:** 0.

**FG010. A cold component that remembers its host.**
- **Idea.** The cold component inside a bound region tracks the baryons' Newtonian potential through a chemical-
  potential lock set by a₀, a "gravitational Fermi level".
- **Test:** the RAR's tightness (CFG4: intrinsic scatter ≤ 0.043–0.048 dex).
- **Cost:** 0.

**FG011. Energy-weighted switching.**
- **Idea.** The switch reads the region's binding energy per unit mass against (κc)² scaled by the vacuum. Nothing is
  a density threshold, so the BIG-SPARC null is respected.
- **Test:** the full switch table (CFG4).
- **Cost:** 0.

**FG012. Merger rule.**
- **Idea.** When two top-level systems become mutually bound, their phantoms merge into one ledger over one crossing
  time.
- **Test:** the MW–M31 timing (FP11) and El Gordo.
- **Cost:** 0.
- **Kill:** timing needs an instant merge.

**FG013. Reversibility.**
- **Idea.** A system that unbinds (tidal stripping, flybys) loses its phantom on its own crossing time.
- **Test:** the dwarfs in XR27's table (Crater II, And XIX); tidal dwarfs.
- **Cost:** 0.

**FG014. No-EFE theorem.**
- **Idea.** Prove that under FG001 plus FG002 a uniform external field never enters any observable of an isolated
  top-level system. Then list the non-uniform (tidal) terms that remain.
- **Test:** Chae's signal reclassified as tidal; CFG1's contested row.
- **Cost:** 0.

**FG015. A single relativistic action for FG001–FG004.**
- **Idea.** A metric plus one coherent field plus a bound-region multiplier. Check PPN (γ = 1), c_T, and the cold
  limit on FRW.
- **Test:** XR25-style strong-field and XR26-style CMB checks.
- **Cost:** 0.

## B. The edge and the switch (FG016–FG027)

**FG016. The edge as the first-apocentre caustic.**
- **Idea.** Derive the phantom's edge as the splashback caustic of the top-level system's baryons plus cold component
  (AS1526, upgraded to today's reading). It is CFG4's one missing ingredient.
- **Test:** XR28's splashback set, KiDS via FP23, and the Ω_c budget via CFG4.
- **Cost:** −1 (x_e).
- **Kill:** it lands outside CFG4's window x_e ∈ [0.31, 0.48].

**FG017. Turnaround radius or splashback radius.**
- Compute both from one collapse model.
- **Test:** which passes KiDS, the Ω_c budget and splashback together.
- **Cost:** 0.

**FG018. A density edge, not a law edge.**
- **Idea.** At a density edge the enclosed phantom keeps gravitating as 1/r² beyond it. At a law edge, the law itself
  stops. CFG4 showed only the density edge survives KiDS. Prove the density edge from FG004's ground state.
- **Cost:** 0.

**FG019. Edge sharpness from the cold component's dispersion.**
- **Idea.** Derive the width of the edge.
- **Test:** the lensing slope depth in XR28 (measured −3.42 to −3.5).
- **Cost:** 0.

**FG020. Satellites share the host's phantom.**
- **Idea.** Derive the "top-level system carries it" rule from FG001 and FG016.
- **Test:** satellite kinematics around isolated hosts, whose velocity dispersion should break at the edge.
- **Cost:** 0.

**FG021. A stacked-lensing edge feature.**
- **Idea.** Predict the break in the excess surface density at about 0.5–1 Mpc around isolated L* lenses.
- **Test:** KiDS-Legacy / HSC-Y3 detectability forecast.
- **Cost:** 0.

**FG022. Edge in the Milky Way.**
- **Idea.** Predict where the MW's phantom ends, then test with the outer halo tracers (Bird 2022 masses, XR29).
- **Cost:** 0.

**FG023. Edges in groups.**
- **Idea.** A group as a top-level system, with one phantom and one edge.
- **Test:** FP12's group R0 values and X-ray groups.
- **Cost:** 0.

**FG024. Edge evolution with redshift.**
- **Idea.** The edge follows splashback, which grows with the accretion rate.
- **Test:** the z = 0.4 and 0.7 KiDS bins; CMASS (FP23).
- **Cost:** 0.

**FG025. The switch's mass threshold, derived.**
- **Idea.** With FG001 the threshold becomes "top-level or not" instead of M\*. Show that CFG4's M\* window
  (1–6.7e6 M☉) is reproduced by embedding statistics.
- **Cost:** −1 (M\*).

**FG026. The switch never reads local density.**
- **Idea.** Prove that no density-read gate survives the BIG-SPARC null plus DE12. That fixes the switch's variable
  class.
- **Cost:** 0.

**FG027. The edge and the compensation trough.**
- **Idea.** Show a derived edge carries no Gauss-compensation trough, since XR28's trough came from the band-pass.
- **Test:** XR28's splashback likelihood.
- **Cost:** 0.

## C. Removing constants (FG028–FG037)

**FG028. The constant ledger as a gate.**
- **Idea.** Every candidate must print its fitted/declared/tied/derived counts (CFG0) and beat the current chain's 5/2+3.
- **Cost:** n/a.

**FG029. ξ removed by embedding.**
- **Idea.** Under FG001 the Sun owns no phantom, so the heat-filter length ξ is unnecessary.
- **Test:** Cassini Q2 ≤ 5.2e-27 s⁻² and planetary residuals with only the Milky Way's smooth field.
- **Cost:** −1.

**FG030. x_e removed by FG016.**
- **Cost:** −1.

**FG031. The max rule derived (FG004).**
- **Cost:** −1 (a declared rule becomes derived).

**FG032. ν's shape from the ground state.**
- **Idea.** If FG004's minimizer fixes the phantom profile, test whether it also fixes ν, so that ν_mono or P2 is
  derived rather than declared.
- **Cost:** −1 if it works.

**FG033. The dark amount.**
- **Idea.** Test whether FG004's ground state, run backwards to z ~ 1100, fixes Ω_c h². Apply a pre-registered
  look-elsewhere penalty. CFG0 flags κ⁴√(8π/3)/Ω_Λ = 0.2642 as numerology.
- **Cost:** −1 only if principled.

**FG034. ε, ζ and q retired.**
- **Idea.** In FG001–FG004 there is no conversion or kick, so FK1's ε, ζ and q are unnecessary.
- **Test:** X-COP, Harvey and the flagship without conversion.
- **Cost:** −3.

**FG035. L_Λ retired.**
- **Idea.** No band-pass is needed if the switch is bound-only.
- **Test:** FP23 and XR28 pass without it.
- **Cost:** −1 (plus −3 natural choices: n, the ramp, c_y).

**FG036. λ fixed at its regulator floor.**
- **Idea.** Declare λ → 0⁺ as a limit and prove the observables continuous there (XR18b: λ ≤ 0.03 is inert).
- **Cost:** 0.

**FG037. κ from the cleanest data.**
- **Idea.** Measure κ from gas-rich TRGB-distance galaxies only. That drops the H₀ distance systematic, which PAPER6
  notes makes κ track the Hubble tension.
- **Cost:** 0 (a sharper fit).

## D. Decisive tests with data on disk (FG038–FG060)

**FG038. The two populations.** Split SPARC and LV galaxies by embedding (FG001) and fit the RAR separately. The
prediction: embedded galaxies follow cold-halo dynamics and isolated ones follow the RAR.

**FG039. Cluster spirals.**
- **Test:** HI rotation curves of Virgo members (VIVA) against field spirals.
- **Prediction:** a halo-like, not RAR-locked, scatter for members.

**FG040. Embedded vs isolated dwarfs at the same stellar mass.**
- **Test:** MW/M31 dwarf spheroidals against isolated LV dwarfs (XR27's tables).
- **Prediction:** an offset in the sign FG001 predicts.

**FG041. Tidal dwarf galaxies (NGC 5291, Lelli et al. 2015).**
- **Prediction under FG001:** no own cold component and embedded, so no mass discrepancy.
- **Kill:** a MOND-like discrepancy is confirmed.

**FG042. Outer-halo globular clusters (NGC 2419, Pal 14, Pal 4).** The prediction is Newtonian. Here FG001 and the
chain differ sharply.

**FG043. The Oort cloud's comet anisotropy** (the record's side-front, DOI 21966646). FG001 predicts none. A robust
signal kills FG001.

**FG044. Wide binaries in DR3 now.** Rescore both published samples under FG001 (γ = 1), the chain (1.07/1.09) and
external-field MOND, using the frozen pipeline read-only.

**FG045. Satellite velocity dispersion vs distance around isolated hosts** (SDSS-type samples). Predict the break at
the edge.

**FG046. X-COP with the hydrostatic bias as a nuisance.** CFG1 says b ≈ 0.14 lies inside 0.06–0.2. Refit FP16's dark
window with b marginalized; the window may open.

**FG047. SLACS under the max rule.**
- **Idea.** In massive ellipticals the cold component can exceed the phantom inside R_E, which lightens the required
  IMF.
- **Test:** XR33's machinery against the spectroscopic IMF relation.

**FG048. The Milky Way's joint fit.** Vertical force (f_M = 1.30), the outer decline (XR29) and M\* from the census,
all under the target law with the edge.

**FG049. Coma UDGs as embedded.** Newtonian plus a cold component: recompute DF44's dispersion with FG001. CFG1 says
this is not soft under MOND.

**FG050. The LV dwarfs' zero point.** Isolated means MOND with no host effect. Fit +0.080 ± 0.047 directly.

**FG051. Crater II and And XIX** under FG001 with tidal stripping, using the radius convention CFG1 flagged.

**FG052. The cluster-infall BTFR under FG001.**
- **Prediction:** infall galaxies inside turnaround are embedded, so their internal dynamics look like cold halos.
  Compare against the M\* failure (2.2–6.3σ).

**FG053. A three-way DR4 registration.** Register γ = 1 (FG001), the chain's separation-resolved curve (XR22) and
external-field MOND before 2026-12-02. This is an append-only amendment, on the author's go.

**FG054. Isolated-lens lensing split by environment** (FP21's pipeline). Group members vs isolated: FG001 predicts
truncation for members.

**FG055. KiDS at 0.3–1.5 Mpc under the density edge.** Refit B21 with the edge and the cold-component 2-halo term
(CFG4).

**FG056. CMASS "lensing is low"** under a bound-only phantom. Check the sign FP23 found wrong for the band-pass.

**FG057. The Bullet cluster's subcluster galaxies as embedded.** Recompute the lensing peaks with FG001 plus FG004.

**FG058. The SN-Ia host step at the a₀ scale.** Test whether the step tracks the top-level/embedded transition of the
hosts (the framework's own 6.9σ step).

**FG059. Galaxy pairs.** Isolated pairs that become mutually bound should show the merged-phantom dynamics of FG012 in
their relative velocities.

**FG060. The BIG-SPARC null as a switch filter.** Rerun the null with FG001's classification. It should stay null.

## E. Cosmology under the target law (FG061–FG070)

**FG061. The full cosmology gate set, with a bound-only phantom equal to the cold component.** Gates: CMB lensing
(CFG4: 1.000), S8, the forest, BAO, RSD and cluster counts, run through the gate harness.

**FG062. XR21's box in bound-only mode.** Switch the phantom on per halo from the box's own binding energy
(FG003/FG011), then run CMB lensing and cosmic shear.

**FG063. The Local Group with the edge.**
- **Idea.** Each giant's phantom ends at x_e r_ta, so the outer flow sees baryons plus the cold component.
- **Test:** recompute R0 with FP11's machinery against 0.96 ± 0.11.

**FG064. The KiDS vs R0 pincer (FP18) under FG001 and FG016.** Both sides move; recompute jointly.

**FG065. The forest by construction.** The expanding IGM owns no phantom. Verify ΛCDM-level P1D with L362's machinery
after XR34's kernel fix.

**FG066. S8 with no conversion.** Under FG034, S8 is ΛCDM's. State plainly that the low-S8 story then needs a
different cause (XR32's conversion result is retired).

**FG067. eRASS1 counts.** Under the max rule, cluster masses are ΛCDM-like, so the counts match.

**FG068. The ISW and CMB-lensing cross-correlation.** A bound-only phantom leaves the linear potentials GR-like.
Predict a null.

**FG069. JWST's early galaxies under FG001.** Early halos are top-level, so their phantom is on. Compute the ceiling
against XR23's result, which matched ΛCDM.

**FG070. The flat a₀(z) test with the edge.** At z ≈ 2.5 the phantom ends at the young splashback. Predict the rotation
curves JWST and ALMA would see.

## F. The dark component: the framework's own field, not a particle (FG071–FG080)

**FG071. The minimal field.** One real coherent field, cold on FRW, with the FG004 ground state in bound regions. Find
the smallest Lagrangian that does both.

**FG072. Its mass window.** The lower bound comes from the forest (FL1: m ≳ 1.9e-19 eV). Find the upper bound that
still allows the ground-state profile.

**FG073. No conversion, no kick.** Retire FK1's machinery and score what is lost. Expect only XR32's S8 dip.

**FG074. Merger behaviour.** Collisionless on crossing, so the Bullet passes. Settles on the new top-level ground state
within a crossing time.

**FG075. Core–cusp.** The ground-state profile is cored at the phantom's inner shape. Compare with SPARC's
surface-density relation (CFG4: 10^2.14–2.25 M☉/pc²).

**FG076. Diversity of rotation curves.** The ground state is deterministic in the baryons. Compute the predicted
diversity at fixed V_max against SPARC.

**FG077. Satellite subhalos.** Embedded, so they keep their own cold component, with its abundance from the cold
initial state (ΛCDM-like). Check the satellite counts.

**FG078. Cluster cores.** The max rule gives the cold component where the phantom is too small. Match X-COP's inner
slope (r^−1.53).

**FG079. The field's stress in lensing.** It is real mass, so γ = 1 with no slip. Check SLACS lensing plus dynamics
(XR33's joint test).

**FG080. Early-universe safety.** The field is frozen before matter–radiation equality. Reuse XR26's BBN and CMB checks.

## G. The framework's own findings as levers (FG081–FG088)

**FG081. The unimodular tie as the source of a₀ in FG008.** The same integration constant sets Λ and the bound-matter
response.

**FG082. The a₀ = (κ/√(24π)) c² K_∞ identity (XR30).** Test whether FG007's vacuum time is K_∞'s inverse, which would
tie the virial clock to the same constant.

**FG083. The flat a₀(z) law as a bound-system property.** Prove FG001's response does not smuggle in H(z); run CFG6's
flat-law checks.

**FG084. The √ρ_DE variant under FG001.** Carry CFG6's labelled band into the FG070 prediction.

**FG085. The Oort-cloud side-front as FG001's falsifier** (FG043), made quantitative with the record's machinery.

**FG086. The directional external-field test.** FG001 predicts zero. Rerun at larger N; CFG1 notes the n = 25 rerun
gave −1.70 ± 2.12.

**FG087. The vertical-force front.** f_M = 1.30 against the census baryons under the target law.

**FG088. The high-z Tully–Fisher archive.** Refit under FG001 plus FG016 with the edge at each galaxy's own
splashback.

## H. New observables nobody has computed (FG089–FG096)

**FG089.** An edge-induced feature in the satellite radial distribution around isolated hosts.

**FG090.** A lensing–dynamics mismatch that appears exactly at the edge, where the density edge keeps lensing while
the law stops.

**FG091.** HI rotation curves that stay flat past the edge until the cold component's own profile takes over.
Predict the transition radius.

**FG092.** The pair-merger phantom reorganization (FG012) seen as a transient velocity anomaly in bound pairs.

**FG093.** The dependence of dwarf dynamics on whether each dwarf is embedded, as a population statistic that
large-survey kinematics could measure.

**FG094.** Globular-cluster tidal tails as Newtonian tracers inside the Milky Way's phantom (Pal 5, GD-1): a
potential-shape prediction.

**FG095.** The escape-speed curve of the Milky Way at the edge (Gaia high-velocity stars).

**FG096.** A cluster-member vs field-galaxy fundamental-plane offset predicted by FG001.

## I. Infrastructure that makes the program crisp (FG097–FG100)

**FG097. The one-command gate harness.** Build it from committed machinery:
- SPARC;
- KiDS with FP20's exact projector, plus the web field;
- XR26's CMB lensing;
- XR28's splashback;
- X-COP;
- the forest proxy;
- XR22's DR4 statistic;
- Cassini;
- the Local Group (FP11).

It reads CFG1's requirement list and scores a candidate law file in minutes. Every idea above then costs one run.

**FG098. Blind registration.** Hash each candidate's predictions before scoring, as done for DR4. This avoids choices
made after scoring (FP19's c_y = 2 was one).

**FG099. Automated reproduction.** Rebuild the hub's scratch-mirror re-run as a committed tool (links `.git`, input
tables and outputs by convention). Clear `REPRO_PENDING.md` with it.

**FG100. An honest novelty check per idea.** Search the literature after the derivation, record overlaps in the
idea's README, and keep a running "new vs known" ledger.
