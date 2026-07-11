# LANE 2 -- The Nonlocal Lead (Deffayet-Woodard nonlocal-metric MOND)

## The question
Is the Woodard/Deffayet nonlocal-gravity class a PURE-MI (no DM, no medium,
GW-safe, one metric) lensing channel for the framework, or does it thread the
double-count knot only by becoming modified GRAVITY?

## What the literature actually shows (papers cited, verbatim structure)

**DEW 2011 (arXiv:1106.4984, PRD 84, 124054) -- "sufficient lensing".**
Static spherical metric ds^2 = -B dt^2 + A dr^2 + r^2 dOmega^2, potentials
a=lnB (temporal), b=lnA (spatial). Two physically distinct relations:
- eq (9)/(11): `r b' = 2GM/(c^2 r) = 2v^2/c^2` -- **dynamics** (temporal, orbits).
- eq (10): `a(r) = k r b'(r)` -- ties the **lensing** potential to the dynamical one.
MOND is imposed by changing eq (9) to eq (12): `r b' -> 2 sqrt(a0 GM)/c^2`.
Crucially they then **isolate rho on the LEFT (geometric) side** (eq 13):
`(c^2/2a0) (r b')^2 / r^2 = 8piG rho/c^4`. This is a modification of the
Einstein field equations' geometry response, with matter minimally coupled and
geodesic. Choosing k=1 recovers *exactly* the GR-with-dark-halo weak lensing
from a SINGLE metric. Solar system: variable `y[g]=(c/3a0)|b'|` is >1e4 (I get
6.3e7 at 1 AU), so the MOND Lagrangian `~ y^2 e^{-y}` (eq 82) is
**exponentially screened** -> PN/binary-pulsar safe.

**Deffayet-Woodard 2018 review (Universe 4, 88; arXiv:1712.05463)** and
**2016 cosmology (Kim et al, PRD 94, 104009; arXiv:1608.07858)**: the
interpolation is a **free function**; "predict any amount of weak lensing by
changing k". Nonlocality = functions of 1/Box acting on curvature; localized
with **auxiliary scalar fields under RETARDED boundary conditions** -> causal &
conserved by the partial-integration trick (DEW 2011 eqs 58, 984-1042). Woodard's
stance: not free Cauchy data (would-be ghosts), but an *effective* action from
IR-graviton vacuum polarization during inflation, so the aux fields have fixed
initial data.

**Deffayet-Woodard 2026 (arXiv:2512.10513, JCAP 04(2026)081)** -- single model
interpolating cosmology <-> bound systems. `L_MOND = -(a0^2/16piG) M[g] sqrt(-g)`,
`Z[g] = (4c^4/a0^2) g^{mn} d_m[1/Box(R_ab u^a u^b)] d_n[1/Box(R_rs u^r u^s)]`,
interpolation `f(Z)=(1/2)Z exp[-1/(3 sqrt|Z|)]`. Uses a unit timelike u.
GW170817 safe **by construction**: Z carries two Ricci factors -> vanishes for
tensor radiation ("no change in propagation of tensor modes"). No ghost/runaway
(Barvinsky mimetic-type analysis). a0 ~ 1.2e-10 (Milgrom), exploits cH0 coincidence.

## The match to the framework

Both theories are nonlocal, both use a preferred unit timelike u, both keep the
MOND term out of the tensor sector (GW-safe), both claim causal via
retarded/Herglotz structure. **But the nonlocal operator sits in a different
sector:**
- Framework (MI): `K(Box_u/a0^2)` acts on the **matter current** rho_m u.
  Nonlocal INERTIA. G_mu_nu keeps the standard baryonic source.
- DEW (MG): `f(Z[g])`, Z built from `1/Box` acting on **curvature** R_ab u^a u^b.
  Nonlocal GRAVITY. The MOND enhancement is inserted into G_mu_nu's LEFT side.

The framework's a0=9.36e-11 and nu=sqrt(1+1/y) **can be hosted** as a
free-function choice inside the DEW class (a0 imported, not derived). GW170817,
one-metric lensing, causal/ghost-free structure all carry -- via DEW's own
arguments, not the framework's Herglotz result (which is for the matter operator
Box_u, absent in the migrated theory).

## The load-bearing result (mini-theorem)

**Light bending is fixed by the SUM (Psi+Phi) of the temporal and spatial
potentials; orbits by the temporal gradient alone.** DEW lens correctly by
enhancing the SPATIAL potential b in the field equations (eq 13, geometric LHS)
and locking a=r b' (eq 10). **Pure MI cannot do this:** its nonlocal operator
lives in the matter kinetic sector, modifies the WORLDLINE inertia of massive
bodies, and leaves G_mu_nu = 8piG T(baryonic). So b stays baryonic; photons
(null geodesics of that metric) see only the baryonic potential and **under-lens
by sqrt(g_bar/a0)=sqrt(y)** (deep-MOND deficit -> 0). This reproduces, from the
potential structure alone, the banked source-side fork ("pure MI under-lenses,
~1e7 too weak"). **To enhance b you must touch curvature.** Migrating the
nonlocal operator matter->curvature IS the reclassification MI -> nonlocal MG.

## The double-count knot -- resolved by choosing cleanly

DEW-MG carries nu*g_bar in the ONE metric for both light and orbits, with NO
double count, precisely because it removes the MI worldline response (matter is
geodesic) and tunes the field equation (eq 13) to give flat curves from that
same enhanced geometry. The "over-predict by nu" pathology only arises if you
keep an MI worldline response AND add source enhancement. You cannot have both;
DEW picks metric-only (MG). This confirms the knot is a genuine fork, not a
threadable gap.

## Costs of the found channel (priced honestly)

1. **It is MG, not MI.** Abandons the framework's defining premise
   (trajectory-dependent inertia, Cassini-evaded-by-MI). Honest reclassification.
2. **a0 not derived** -- free-function input; the nonlocal class does not FORCE
   9.36e-11 or nu=sqrt(1+1/y).
3. **Cassini quadrupole (Q2):** DEW gives *exponential* PN screening
   (e^{-y}, y~6e7 at 1 AU) -- structurally STRONGER than AeST's power-law
   external field, so *plausibly* evades the Desmond-Hees-Famaey/Park Q2
   3-15sigma tension that the framework's AeST=MG realization inherits.
   BUT the papers demonstrate only scalar PN suppression; **the anisotropic Q2
   quadrupole is NOT verified in the nonlocal models here** -- open, potentially
   favorable vs Branch B, unproven.
4. **Aux-field/ghost structure:** relies on Woodard's "effective action, fixed
   retarded initial data" framing; treated as fundamental the localized aux
   scalars are the standard nonlocal-ghost worry. Distinct from (not inherited
   from) the framework's Herglotz-Nevanlinna proof.

## Verdict

The nonlocal lead is REAL and DECISIVE, and it **confirms the fork rather than
threading it**. Nonlocal gravity is a legitimate no-DM/no-medium/single-metric/
GW-safe lensing channel that can host the framework's a0 and nu -- but it lenses
*because* it is modified gravity (nonlocality in curvature). It is therefore the
honest reclassification of the framework's MI content into nonlocal MG, NOT a
pure-MI channel. Pure MI (nonlocality confined to the matter kinetic sector)
provably cannot enhance the lensing potential and under-lenses by sqrt(y). This
strengthens the impossibility side: "no dark matter" requires touching curvature
-- either Branch B (elastic dark-energy medium) or a Woodard-type nonlocal-MG
term. Nonlocal-MG is a genuinely distinct third option (medium-free, single
metric, exponentially screened) that may fare BETTER on Cassini-Q2 than Branch B,
at the same price both pay: it is MG, and a0 is imported not derived.
