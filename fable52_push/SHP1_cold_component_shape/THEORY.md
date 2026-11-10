# The theory, assembled from the owner's pieces (2026-11-10)

A note, not a lane: it grades nothing, relabels nothing and adopts nothing. Every number is quoted from a lane's
RESULT.md, and where this note and a lane differ, the lane is right. kappa = 1/2 FITTED; not theory closed.

## The theory in five sentences

1. **One dark sector, dark energy, sets the scale.** a0 = (c/2) sqrt(G rho_DE), and a0 moves when rho_DE moves.
   kappa = 1/2 is fitted, not derived.
2. **Part of it is cold.** Cold dark energy, about 5.4 times the baryons, gave the CMB its wells (F1). It is a field
   component, not a particle.
3. **Around baryons the cold component has one shape.** M_C(<r) = M_b (sqrt(1 + 4x^2) - 1) / 2 with x = r / r_M and
   r_M = sqrt(G M_b / a0). Its density goes as 1/r inside r_M and 1/r^2 outside. The law g_N = g^2 / (g + a0) says
   exactly this, read as gravity. That is "counted once": the law is where the cold component sits, not a force on top
   of it.
4. **So there is nothing to clear from galaxies.** The cold component near a galaxy is the law's halo. A second halo of
   cosmic size beside it is excluded by the data (SHP1).
5. **Away from baryons the cold component is ordinary cold matter.** That covers early times, the space between
   galaxies and the extra mass in clusters, and it is where the CMB, growth and lensing of large scales come from.

## What each piece does, and where it stands

| piece | its job | status, from the record |
|---|---|---|
| a0 = (c/2) sqrt(G rho_DE) | sets the scale | kappa fitted (0.465 +- 0.076 from the BTFR); SPARC rms 0.0563 / 0.0558 |
| a0 tracks rho_DE(z) | time dependence | untested at z ~ 2.5 (a few well-measured discs decide) |
| cold dark energy | CMB, growth, clusters | CMB peaks and CMB lensing pass (F1, CO2: -0.30 sigma); weak-lensing level 2.1 widths high on KiDS-Legacy (KL1) |
| the law's shape | where the cold component sits around baryons | **SHP1: measured** (below) |
| counted once | no double counting | **SHP1: a cosmic-sized halo on top of the law is excluded** (Delta chi^2 +565 to +6500) |
| v3s action | holds the shape | the static state holds the law's shape (FB1) and is stable around point masses and isolated discs (SCS1, SCS2) |

## The shape of the cold component (SHP1, raw data)

| x = r / r_M | data | what the cold component does |
|---|---|---|
| 0.2-1 | SPARC, bin medians within 0.06 dex of the law | M_C grows like r^2 (density 1/r); measured slope 2.2-2.5 |
| 1-10 | SPARC, the same | M_C grows like r (density 1/r^2); measured slope 0.9-1.3 |
| 5-260 | KiDS isolated lenses | the same shape. Level 1.28-1.40 times the law with B21's stars, best read as B21's baryons being 1.6-1.9 times heavier; below the law with B21's hot gas, and then it stops growing past x ~ 100-150 (an edge near 1 Mpc for an L* lens) |

The same shape holds for every galaxy on rotation curves: no trend with M_b, +0.03 dex per dex. On lensing, the
lowest-mass KiDS bin sits 0.2 dex low; the cause is not separated.

## What "clearing the cold component" turned into

The clearing problem (SNP1, HE1 and KO1's exits B and C) assumed each galaxy carried its share of the cold component
as a separate halo that had collapsed with it. That is the picture borrowed from cold-dark-matter cosmology. Neither
the record's own physics nor the data hold it up.

- **The action does not do it.** In the record's action the clock's own gravity is cancelled by the law below
  1/mu_K. So it falls onto a galaxy like test particles, and only about one baryon mass of it arrives by today (COL1; FLD1's
  correction leaves that figure unchanged, at 1.6-5.1 % of the law's halo inside 300 kpc).
- **The data forbid it at cosmic size.** A separate 59.5 M_b halo beside the law is excluded on every reading (SHP1
  R4). A share-sized excess (5-11 M_b) is allowed, but a baryon calibration explains the lensing better.

So the cold component does not need pushing out. It needs a shape, and the law is that shape.

## The one thing still missing

**An equation of motion that puts the cold component into the law's shape where the clock has not folded.** The
static state is right and stable; nothing in the action reaches it.

What any such equation must do, as the record measured it:

1. **Stiff early.** The dust must be stiff in the expanding universe at z ~ 3400 (mu_K >= 2.5e4 per Mpc; MK1).
2. **Inert late.** It must be inert in static wells today (mu_K <= 1 per Mpc; MK1). Requirements 1 and 2 hold at the
   same clock offset, 1e-6, so the dust term cannot depend on the offset alone.
3. **Reach far enough.** The shape must hold out to x ~ 60 (PD1's cap), and lensing sees it to x ~ 200. Today the clock
   has folded only out to x ~ 21 for an L* galaxy (FLD1), and outside the fold it carries no law.
4. **Survive the fold.** It must not break down where the infalling clock folds (COL1: within 0.06-0.15 Gyr).

Where each part is being worked:

- **TK1** (θ-keyed dust, running in the Carbon chat) takes requirements 1-2.
- **MK2's sound speed** gets requirement 3 above about 500 km/s, but fails clusters and groups.
- Requirement 4 has no lane.

## What tests it with data that exist or are coming

- **The shape's level at Mpc radii** depends on how the baryons there are counted. A measured gas mass around isolated
  galaxies decides between 1.4 times the law, the law, and an edge near x ~ 100-150. This is CLOSURE.md's first "what
  would move it".
- **Gaia DR4 (2026-12-02)**: the frozen pre-registration, scored as frozen.
- **a0 at z ~ 2.5**: if a0 tracks rho_DE it follows the dark-energy curve; two to four well-measured discs decide.

## What fails or stays open under this theory (quoted)

| item | where it stands |
|---|---|
| Groups | every share rule fails (PD1); RB1 NOT FALSIFIED one-sided |
| Clusters (X-COP) | passes only in a reported bracket; MK1 finds no dust constant for it |
| Bullet | offset right, amount 2.6 sigma low |
| Hosted dwarfs | B FAILS ON THE HOSTED ROWS (RB2); DG1: history does not close them, and the two FAILS HIGH do not survive its budget |
| Outer cluster shear | about 3 sigma |
| Discs in an external field | NO VERDICT (SCS2); SCS3 running |
| Weak-lensing level | 2.1 widths below form B on KiDS-Legacy under a post hoc amendment (KL1); blind regrade KL1R running |

## What is not claimed

- No completion exists.
- Nothing here says the data favour this theory over another.
- Requirements 1-4 are what a completion needs. Nothing has passed them.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
