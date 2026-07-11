# LANE 3 -- CONNECTION-LEVEL PURE-MI LENSING: verdict IMPOSSIBLE (trilemma)

Framework-first. a0 = cH_Lambda/Z = 9.36e-11 (Z=sqrt(32pi/3)=5.789);
g_obs=sqrt(g_bar^2+g_bar a0); nu=sqrt(1+1/y). MOND in the MATTER kinetic sector
(nonlocal Box_u worldline operator); u = passive frame (0 dof); ONE metric g.

## The question
Can a torsion/nonmetricity (teleparallel) OR conformal/disformal channel bend
light with the nu-enhancement, keep ONE null cone (GW170817-safe), no medium,
no DM, and stay GENUINELY MI (not relabeled MG)?

## What the literature actually shows
- **f(T) MOND / f(Q) MOND** (D'Ambrosio-Garg-Heisenberg PLB 811:135970,
  arXiv:2004.00888; teleparallel MOND lit): a covariant, ghost-free MOND that
  recovers GR + MOND. Photons feel the enhanced SINGLE metric -> lenses
  correctly. Tensor GW speed = c EXACTLY in f(T) (Cai et al. 1801.05827) and
  f(Q) (2406.12558) -> GW170817 trivially satisfied. **BUT it is MODIFIED
  GRAVITY**: the enhancement is in the connection/field equations; the matter
  worldline is a plain geodesic of the enhanced metric (no inertia modification).
- **Deser-Woodard-Deffayet nonlocal metric MOND** (PRD 84:124054, 1106.4984;
  revised version + lensing 2601.16572): a PURELY-METRIC nonlocal model that
  gets *sufficient lensing* precisely by PRESERVING the GR potential ratio
  a(r) ~ k r b'(r) (Phi ~ Psi), so light bends by the SAME enhanced amount as
  matter dynamics. Single cone, GW-safe. **Also MODIFIED GRAVITY** (nonlocal
  Einstein eqs), not MI. Their Sec. III also proves NO *local* curvature scalar
  can do it (MOND needs (h')^3, local curvatures give only (h'')^n) -> nonlocality
  is mandatory even for the MG route.
- **Dark matter emulators** (Kahya-Woodard; Desai-Kahya-Woodard 0801.1984):
  theories where matter/photons couple to g~ (=GR-with-DM) but gravitons to g
  (=GR-without-DM). Two cones -> GW vs photon time delay -> **KILLED by
  GW170817** (and SN1987A/GRB bounds). TeVeS, SVTG are emulators. Soussa-Woodard
  no-go: a single-metric emulator-free theory must violate one of its 5
  assumptions; the surviving route is nonlocal MG (the DWD model).

## The three obstructions (script: lane3_connection.py, exit 0)
1. **Conformal invariance.** Null cones + Maxwell + null geodesics are
   conformally invariant in 4D: g->Omega^2 g leaves photon deflection
   IDENTICAL. A conformal MI coupling gives ZERO extra lensing. (known wall)
2. **Disformal second cone vs GW170817.** g~=g+B u u gives photon speed
   1/(1-B) on g~ while gravitons ride g. c_gamma=c_GW <=> B=0. GW170817
   (|c/c_GW-1|<6e-15) forces B->0, and B=0 is exactly the NO-lensing member.
   The GW-surviving disformal corner is the no-lensing corner. (banked, re-derived)
3. **Double-count / EP knot.** Rotation curves fix a_obs = nu(y) g_bar ONCE.
   For photons to lens correctly the SINGLE metric must carry the FULL nu.
   A massive body on a geodesic of that metric then already sees nu*g_bar, so
   MI must contribute mu->1 (switched off) or curves over-predict by nu.
   Any partial split (metric carries nu^a, inertia nu^(1-a)) UNDER-lenses for
   a<1 because photons only receive nu^a; correct lensing REQUIRES a=1 => mu=1
   => no modified inertia. So a correct-lensing single-cone theory is MG, period.

## The trilemma theorem (closes the fork)
nu must live somewhere the photon couples to. Exactly three homes:
- (A) the ONE metric/connection (photons+gravitons): f(Q)/f(T)/DWD nonlocal.
  Lenses + GW-safe, but Obstruction 3 => MODIFIED GRAVITY, not MI.
- (B) a species-split second metric/connection (photon-only or graviton-only):
  disformal/emulator => Obstruction 2 GW170817-dead (Obstruction 1 for conformal).
- (C) matter inertia only (the framework's real channel): photons are massless,
  no inertia to modify => NO enhancement => pure MI UNDER-lenses (banked ~1e7);
  sourcing it from the frame => a medium => Branch B.
A u B u C exhausts the connection level. A=MG, B=GW-dead, C=under-lensing.
=> **NO connection-level PURE-MI lensing channel exists.**

## Honest caveats
- This is a theorem about *pure MI*, not a no-DM no-go. A REAL working channel
  DOES exist at the connection level -- f(Q)/f(T)/DWD nonlocal single-metric
  MOND lenses correctly and passes GW170817 -- but it is MODIFIED GRAVITY.
  The framework can ADOPT such a completion, at the cost of the MI premise
  (worldline reverts to geodesic; mu=1).
- Whether the framework's nonlocal MI matter-sector operator can be DUAL to a
  DWD-type nonlocal gravitational operator (a representation change that would
  make MI and this MG the same theory) is an open representational question --
  but even a successful duality is a RELABELING to MG for lensing purposes
  (photons then bend via the metric, not via inertia).
- The trilemma's exhaustiveness rests on "the photon must couple to the
  nu-carrier"; a genuinely new geometric structure that photons couple to
  yet is neither an extra metric (B) nor the shared metric (A) is not known to
  exist consistent with EEP + one cone. If someone exhibits one, the theorem
  reopens; I could not construct one and the emulator/EEP argument says it
  would split the cone.

## Bottom line
Pure MI cannot self-source relativistic lensing at the connection level.
"No dark matter" therefore REQUIRES leaving pure MI: either go full MODIFIED
GRAVITY (an f(Q)/DWD single-metric nonlocal completion -- lenses, GW-safe, but
not MI), or accept Branch B (elastic dark-ENERGY medium). This makes the
lensing gap a genuine fork, not a search failure.
