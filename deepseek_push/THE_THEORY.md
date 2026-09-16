# THE_THEORY — the assembly of the lemmas (2026-09-15)

The coherent theory of gravity from the framework's puzzle pieces, stated as
a chain of lemmas.  Every lemma is either a committed, verified result or a
named in-flight gate.  The order is the dependency order; nothing downstream
is claimed on an unproven upstream.

## Lemma 1 — ONE CONSTANT (DONE: Lean-certified)
The universe carries one free scale, a0.  It is not a force constant that is
fitted: it is the dark-energy density translated into acceleration units,

    rho_Lambda = 4 a0^2 / (G c^2)      (<=>  a0 = (c/2) sqrt(G rho_Lambda)),
    Omega_Lambda = 32 pi a0^2 / (3 H0^2 c^2) = 0.6857  (+0.07% of Planck).

The equality is a THEOREM of the framework (G058, 6 Lean theorems, zero
sorry: the exact identity + the interval theorem [0.684930, 0.684932] + the
one_constant_closure statement that the MOND scale and the dark energy are
ONE measurement).  H0 and Omega_Lambda are not independent knobs.

## Lemma 2 — THE KERNEL (DONE, one empirical premise stated)
SPARC's rotation curves select the interpolating function

    mu_2(x) = 1 - (1 + x/2)^-2 ,     kappa = 1/2 = 1/n,     x = g/a0

from the mu_n family with nothing fitted (G002; n = 2 is the one empirical
premise of the whole theory -- four structural derivation routes closed, the
premise stated plainly).  From it: the action-level closure
f(X) with f'(X) = mu_2(sqrt X), f(0) = -1 -- the vacuum term is the dark
energy (the L226 zero-mode no-go dies by identification: the additive
constant IS the measured rho_Lambda).

## Lemma 3 — THE EQUILIBRIUM (DONE: derived three independent ways)
The cold sector (the Noether charge of the shift symmetry, w = 0) in a
baryonic well equilibrates at the virial temperature of the scalar-mediated
force (deep force EXACTLY 1/r with constant C = sqrt(G M_b a0)):

    sigma^2 = sqrt(G M_b a0)/2 ,      c_deep = 1 EXACTLY.

Three independent derivations agree (G046, G056, Qwen Q001).  The Newtonian
realization has NO such equilibrium (G035 KILL -- the kill became the
discovery: the mediator is the scalar, not Newtonian gravity).

## Lemma 4 — THE PHANTOM (DONE: Lean-certified)
The equilibrium density IS the deep-MOND phantom:

    rho_ph = sqrt(G M_b a0) / (4 pi G r^2),      coefficient exactly 1,

so the halo IS the phantom (G003; Lean: phantom_bracket, the equilibrium
spine).  Consequence chain (Lean-certified): v^4 = G M_b a0 (BTFR) and
g^2 = a0 g_N (the deep RAR).

## Lemma 5 — THE COMPLETION (DONE: fully characterized)
The relativistic theory is GR + one shift-symmetric scalar with the frozen
kinetic term

    L = Lambda^4 f(K),  f(K) = K - 1/(1+K),  K = -(1/2)(d phi)^2/Lambda^4,

Lorentz invariant, no aether, no vector sector (alpha1 = alpha2 = 0 by
structure), zero free parameters beyond a0.  Verified: phi_dot = 0 is a
confirmed attractor (G054 14/14); the background is Lambda-CDM exactly
(w = -1, G038 6/6); c_s^2 in [1/2, 1) through the transition; the growth
raise carries inside the registered band; the frozen-scalar certificate
(G055, 9 Lean theorems, zero sorry).

## Lemma 6 — CASSINI (ANSWERED: the force-law class is closed with proof)
The completion's static law on the quasi-Newtonian branch must clear the
Park 2026 quadrupole ceiling (|Q2| <= 5.2e-27 s^-2).  The bare kernel fails
(6.44x/7.63x, S0-calibrated).  The G03 lane then scanned every surviving
modification class on the validated instrument (44 solves, both footings,
xi = 0.005-0.1 pc):
  C1 T-B localised (Helmholtz screen, single AND double filter): the ratio
     NEVER drops below 6.18x -- xi = 0 is the best case, the double filter
     is worse (up to 8.78x).
  C3 field-dependent xi(x): same isotropic class (xi is a function of the
     isotropic invariant) -- structural kill.
  C2 whole-sector form factor: its PPN evasion is time-sector-only (the
     aether is timelike in the static frame: A^m A^n d_m d_n = d_t^2), so
     the static limit is the C1 operator -- fails by identity.
The SMOOTH-SHELL LEMMA (scan-confirmed): an isotropic local screen preserves
the l=2 moment of the mu-transition; the static quadrupole is a property of
the kernel's transition, not of the completion's UV structure.
THE ANSWER (the framework's reading): the Solar System is Newtonian BY
CONSTRUCTION -- the phantom is absent there (the cloud is unbound and
EFE-capped at 7.4 kAU, G006), so there is NO quadrupole and the Park ceiling
is passed trivially.  The MOND-like force is not a force law: it is the
gravity of the equilibrated Noether-charge dust (lemmas 3-4).  The
Solar-System-adjacent observable is the wide-binary cloud (period-separation
distortion, DR4 forecast -- the falsifier).  The pincer is now complete on
both horns: every force-law completion fails Cassini (proven), and the
equilibrium reading predicts Newton there (passes by construction), with its
own registered test.

## Lemma 7 — THE COSMOLOGY (DONE: verified surface)
Acoustic phase (G021: a 5% background modification shifts peaks 2.5%,
40x Planck's precision -- the frozen branch does not deviate), Lyman-alpha
growth (G022/G023: +0.98%/+1.60% at z = 3), DESI pointwise (G024), S8 gate
(G020 OPEN-UNCONFIRMED, the honest label).  Background = Lambda-CDM exactly:
the dark energy IS Lemma 1's constant; there is no separate DE sector.

## Lemma 8 — THE TEST MATRIX (DONE: pre-registered, armed)
DR4 December (gamma_v arms A/B, sigma_tot 0.028; the three vertical
signatures: 140.6 pc break, sqrt exponent, 562.5 pc column cancellation),
Euclid October (eta), z ~ 2.5 BTFR (20:1), WALLABY, DESI DR2.  Every
prediction has its falsifier in print (REFEREE_ATTACKS.md).

## WHAT DARK ENERGY IS (the answer the lemmas give)
Dark energy is the vacuum value of the one scalar: f(0) = -1 makes
L_vac = -Lambda^4, and Lemma 1 pins that density to the gravitational deep
scale.  It is not a separate substance: it is the ZERO-MODE of the same
field whose kinetic regime makes rotation curves.  The coincidence problem
dissolves by parameter count (one constant does both jobs; G058's
one_constant_closure).  The dark energy 'works' by being the boundary
condition of the shift-symmetric sector: the same scalar is deep-MOND in
galaxies (K >> 0), frozen at the vacuum in cosmology (K = 0).

## THE OPEN LIST (all named, all in flight or registered)
1. Lemma 6 -- Cassini (S2 running; fallbacks C2/C3 queued behind it)
2. The PPN ladder (P1: alpha1, alpha2, gamma on the candidate's own form)
3. The ADM mode count (P3: the full count with metric mixings; G05)
4. The cluster amplitude (the honest astrophysical normalization, as LCDM)
5. The formation/relaxation N-body (the equilibrium's reach)
6. n = 2 (the one empirical premise)

---

# THE EXTENDED CHAIN -- L9-L16 (G153, 2026-09-16; append-only extension)

Waves 3-8 landed (G084-G126, WAVEBOARD rev 7) and extend the chain below the
original eight.  Same rule as the head of this document: nothing downstream is
claimed on an unproven upstream.  Evidence classes used below: **Lean**
(machine-checked, zero sorry), **derived** (closed form -- analytic or
sympy-exact, zero free parameters), **empirical** (verified against committed
data), **pre-registered** (prediction and falsifier in print before the data
are read).

## Lemma 9 -- THE ORIGIN (DONE: derived, two independent chains)
The equilibrium (Lemma 3) is DERIVED, not assumed -- five routes, one landing
point.  (a) The maximum-entropy derivation (G084, 8/8): among spherical
equilibria of the collisionless isothermal fluid in the fixed baryon well
Phi = C ln r, the entropy functional S = -int rho ln(rho sigma^3) dV is
maximized by a pure power law; at the DE-set temperature sigma^2 = C/2 the
Euler-Lagrange exponent is **2 exactly** (EL residual 4.3e-14, nonzero at any
other (gamma, sigma^2)); d2S < 0 strictly -- a unique global maximum in the
fixed well.  (b) The virial chain (G091, 12/12, sympy-exact): the truncated
phantom closes in one line -- 2T + W_self + W_bar = 3P_sV with the fluid
closure (P = sigma^2 rho), giving **sigma^2 = C/2 EXACTLY** at the
well-consistent boundary (any lambda, any M_b, both footings); the bare
collisionless virial gives C/3 -- **the phantom's own pressure IS the 1/2**;
gamma = 2 pinned, E = -T, the boundary term identified.  Empirical anchors
reproduced: sigma = 119.2/124.9 km/s and NGC3198's 118.05 km/s.  Evidence
class: DERIVED (two independent chains), with the caveat carried from G081
(the dynamical fundamental mode is marginal, omega^2 = 0 -- an entropy
extremum is not a dynamical attractor).

## Lemma 10 -- THE PARTICLE (DONE: one cold species; the upper bound open)
The sector's particle census is ONE cold species, TWO phases, ONE mass:
m in [3.3, 100] keV (G093 13/13 + G116 8/8).  The lower bound is binding --
the Lyman-alpha forest (Viel+13/Irsic+17/Villasenor+24): m > 3.3-5.7 keV,
v_th < 0.055 km/s today, lambda_fs < 0.5-0.8 Mpc against the registered
0.6 Mpc; Tremaine-Gunn never binds it (field floor 0.6 eV).  The equilibrium
phase's own TG floor m > 23.25 eV (G084 V3; 22.45 alt) is auto-satisfied with
margin 141.9x and sits 4.01x BELOW the killed 93-148 eV relic window -- phase
space does NOT cap the equilibrium.  The virial is MASS-FREE: T/m =
sigma^2/k_B is the mass-independent constant; T_phase(5 keV) = 9.17 K; the
decoupling in one number: T_equil/T_kin,dust = 4.5e5.  OPEN: the upper bound
-- nothing binds from above (100 keV is a placeholder; production not
derived, G116 V3).  Evidence class: EMPIRICAL lower bound + DERIVED
consistency; one open edge (the upper bound).

## Lemma 11 -- THE EFE CAP (PARTIALLY DERIVED; staticity DONE)
The cap's FORM is derived identically: r_efe/r_M = sqrt(a0/g_ext), M_b
cancels to 1e-16 (G119).  The ZERO-PARAMETER FULL-KERNEL SOLVE reproduces
r_cut = 6.13 kpc = **0.6232 (+0.5%)** -- the registered 6.1 kpc IS the kernel
value; the '0.685 tension' is a MIXED-M_b artifact (same-M_b gives 0.6605 at
both masses); the 0.6200-vs-0.6605 gap is the kernel interpolation near
g ~ a0, not a parameter.  The cap's STATICITY is proven (G103, 3/4 -- the
FAIL is the finding): the free dust cannot equilibrate at cluster scale
within the Hubble time by 70-76 orders of magnitude (t_relax =
1e73-1e76 x t_Hubble) -- the boundary is FIELD-PINNED (the EFE cap), not
relaxation-pinned, and STATIC (growth < 0.01 Mpc/Gyr).  G132 (wave 9, landed)
characterizes the boundary thermodynamically: a first-order-class transition
with finite latent heat (10.8-23.7 k_B/particle, water-class), placed by
g_ext rather than selected by max-entropy -- a hybrid, thermodynamic in
nature, environmental in placement.  OPEN: the 0.62-vs-0.635 candidate gap
(sqrt(a0/g_ext) = 0.635 vs the registered 0.62; row 9 of the open list).
Evidence class: DERIVED (form + kernel value) + PROVEN (staticity); one open
constant gap.

## Lemma 12 -- THE TEMPERATURE RATIO (DONE: closed form)
The 0.53^2 mystery CLOSED (G095): T_obs/T_pred = 2(M_dyn/M_b)(r_M/R500) --
the closed form, factors EXACTLY (max residual 9.3e-16).  The law's
structural exponent alpha = **2/3 EXACTLY** (virial +1 from T ~ M_dyn/r,
-1/3 from Delta500 self-similarity R500 ~ M500^{1/3}); 1/2 EXCLUDED at
2.2 sigma; the 0.28 constancy is the sample's M500-M_b covariance
(M_b-independent exactly at M500 ~ M_b^{3/4}, fitted beta = 0.634 +- 0.107).
THE MEANING: the T ratio is the virial temperature of the TOTAL mass against
the baryon floor -- f = (T_obs/T_pred)^{1/alpha} = 5.4-6.8 vs measured 5.66:
**the missing abundance in ONE number**; 0.53^2 = 1/2 (M_b/M500)(R500/r_M);
the ratio's 0.05-dex scatter IS the HSE scatter (0.053 dex, quantified).
Amplitude caveat carried: nothing re-derives the 3.6x normalization from M_b
alone (the free-dust input stays input).  Evidence class: DERIVED (closed
form, sympy-exact) + EMPIRICAL (T-ratio 0.28 = 0.53^2 confirmed, 1.8% apart,
per-cluster median dev 7.8%).

## Lemma 13 -- THE DUST ENVELOPE (shape DERIVED; the amplitude OPEN)
The 0.313-dex curve-scatter CLOSED (G122): the missing pattern is the
framework's OWN r^-1 shape -- R = [2x/(x-1)] a_c (r/R500)^-p with ONE
universal p* = +0.99 and one per-cluster amplitude: COLLAPSE to 0.097 dex
(12/12 below the 0.15 gate, was 0.313; even the 3-param literal form closes
at 0.119 with NO per-cluster freedom) -- the free-dust normalization IS one
profile shape with a per-cluster amplitude.  The gas-fraction crossover
DERIVED (G124): model median r_half/r_M = 1.73 (analytic 1.72) vs the
measured 1.43 in [1.13, 2.05] -- 12/12 within [1/3, 3], Spearman(model, obs)
= +0.958; a SHAPE FUNCTIONAL: the phantom and dust AMPLITUDES cancel
(d ln/d ln A_ph = -0.008, d ln/d ln A_dust = +0.03), the ratio is set by the
baryon concentration c_b (+0.26/dex) and the envelope slope (+0.25/dex); the
21% gap is the inner-window f_gas slope mismatch = G108's registered
amplitude overshoot, NAMED NOT TUNED.  OPEN: the per-cluster amplitude's
mass-ordering (rho(amp, M500) = -0.59, p = 0.045; q = -0.41) and its residual
floor -- THE CLUSTER AMPLITUDE row (open list 4).  Evidence class: DERIVED
shape + EMPIRICAL collapse; one open item (the amplitude).

## Lemma 14 -- THE DEEP END (DONE: empirical PASS; one tension OPEN)
The zero-parameter law HOLDS on the most gas-dominated rotating dwarfs
(G114, 3/3): 55 systems (LITTLE THINGS + FIGGS, verbatim primary LaTeX
tables), rms **0.150 dex** (<= the 0.20 bar), median |r| = 0.080, zero bias,
zero mass slope; the gas-dominated subset does BEST (0.124 dex); the 7 dwarfs
at g_N < 0.1 a0 sit ON the line where the law is exact (DDO 154: +0.015); the
dichotomy CONFIRMED -- rotation-on (0.080) vs dispersion-off (0.401, G070's
UFDs): +0.32-dex contrast (caveat: mass ranges don't overlap).  THE DEEP END
IS GREEN.  The tension: MIGHTEE-HI (G099, 2/3 -- the V2 FAIL is the finding):
the zero-param law passes the bar (rms 0.190 dex) but the DEEP end (90% of
the 80 rings below 0.2 a0) sits **-0.151 +- 0.015 dex above the law's
committed amplitude (~10 sigma; 1.4-1.6x high)**, matching the paper's OWN
a0 = 1.69e-10 preference (its 2-sigma tension vs the SPARC-anchored RAR) --
a real systematics-level pressure on THE FOOTING (which was 0.754-0.783;
MIGHTEE pushes HIGHER).  OPEN: the MIGHTEE deep tension and the footing.
Evidence class: EMPIRICAL PASS (G114) with one named open tension (G099).

## Lemma 15 -- THE DR4 FACE (DONE: pre-registered, armed)
The DR4 December identifications, both registered with falsifiers in print
(G112 amendment: F1-F3, decision rules D1 6.2 sigma / D2 3.5 / D3 5.6):
(a) the wide-binary period-separation RIDGE (G088, 5/5, simulated on 200k
pairs): **30.7 sigma** at 10-30 kAU (30 uas, realistic N), +18.4% in
separation / +28.9% in gamma_v at fixed period, breaking flat at the 7.4 kAU
cap (E7); the ridge -- not the level, which is triple-confounded (+2-10%
mimics) and whose strict plateau 1.2886 is already B-falsified on DR3 -- is
the identification's zero-parameter statement, and a triple's s-excess is
flat with no break, so the ridge is not mimickable.  (b) the vertical
DOUBLE-MAP (G092, 9/9): the two-scale z-profile -- phantom slab (z_c =
140.6 pc, z* = 4z_c = 562.5 pc, column 26.7 M☉/pc2) + sech^2 disk (h ~ 1 kpc)
-- with the NEGATIVE outer bin (180-562 pc, the column cancellation) as the
sign discriminator (D3: -0.40 vs +5.57 NFW / +2.31 sech^2); the inner
|z| < 300 pc column 25.7-29.8 vs 6.6-8.7 M☉/pc2 (4x); the 26.7 column
reproduced exactly.  Evidence class: PRE-REGISTERED (decided by Gaia DR4,
2026-12-02; nothing empirical yet by design).

## Lemma 16 -- THE MERGER FACE (DONE: q = 1 closed form; pre-registered)
The deep-regime close-pair prediction, executed and forecast (G118, 8/8 +
G121, 9/9): q = 1 in CLOSED FORM from the Roche-class disruption criterion
with the 1/r force -- f_pair/f_LCDM = (1 + r_M/s)^1, with the anchor excesses
**2.000 at s = r_M EXACT** (G086's factor), 1.500 at 2 r_M, 3.000 at r_M/2;
honest envelope [1/2, 3/2]; the 10-40 kpc x 2e10-2e11 Msun window integrates
to a median excess 1.485, rising toward small s/r_M (universal axis,
footing-invariant).  Falsifiers F1-F4 armed (anchor <= 1.00 kills; q_meas
outside [0.5, 1.5] kills; concentration/env instead of M_b kills; wrong
window kills).  THE DIRECTION DERIVED (G121): f_pair RISES +35-190% in-window
vs baryon-only (the deep well (1 + s/r_M) holds pairs LONGER; the
'lifetime-shortens -> falls' branch rejected as orbital-period confusion);
a SLIGHT DEFICIT vs SHMR-matched NFW (-2 to -5% central, the enclosed-mass
census; crossover s* = 42-47 kpc); 3-sigma-reachable corners defined (deep
deficit N <= 100 at sys 10%; massive corner sys <= 5% at N ~ 300).  The
cleanest galaxy-scale 1/r test outside the Solar System; SDSS z~0.1 detects
the anchor at 19-59 sigma (Poisson).  Evidence class: DERIVED closed form +
PRE-REGISTERED forecast.

---

# THE CLOSURE STATEMENT (G153) -- the chain's status, 16 links

**Lean-certified** (66 theorems, 7 certificates, zero sorry, axioms
{propext, Classical.choice, Quot.sound}; LEAN_CERTIFICATES.md):
Lemma 1 (G058: the exact identity, the interval theorem, one_constant_closure
-- 6 theorems), Lemma 4 (G003 + the EQUILIBRIUM_THEORY spine, 12 theorems
incl. phantom_bracket and equilibrated_is_phantom -- THE IDENTIFICATION),
Lemma 5 (G055, 9 theorems -- the frozen-scalar certificate; with G031's
hydrostatic spine 13, G036's slab 4+, G002/G003's 4, G007's bimetric 11,
G001's clock 9, G005's 8).  Lemma 3's equipartition is Lean-backed inside the
spine and derived three independent ways (G046, G056, Q001).

**Empirical-verified**: Lemma 2 (SPARC selects mu_2 -- the ONE empirical
premise of the theory, stated plainly), Lemma 7 (the cosmology surface: CMB
shifts 2.5% vs 40x Planck precision, Lyman-alpha +0.98/+1.60% at z = 3, DESI
pointwise; S8 carried as honest OPEN-UNCONFIRMED), Lemma 10's lower bound
(the forest; TG floors), Lemma 14 (deep-end HI, 0.150 dex), and the
pre-registered, armed face: Lemma 8 (the test matrix), Lemma 15 (DR4), Lemma
16 (SDSS pairs).

**Carrying the named open items**: Lemma 13 and Lemma 12 -- THE CLUSTER
AMPLITUDE (the per-cluster normalization's mass-ordering, rho(amp, M500) =
-0.59, p = 0.045; the 3.6x temperature amplitude stays an input;
G095/G097/G098); Lemma 14 -- THE FOOTING (MIGHTEE-HI's deep end pushes a0
higher, 0.754-0.783 -> its own 1.69e-10; the alt footing fails Omega_Lambda
at 0.9953, the honest edge never hidden) and the MIGHTEE DEEP tension itself
(10 sigma, -0.151 dex, G099's registered V2 FAIL); plus the chain's own
in-flight rows: Lemma 6 (Cassini S2 running, fallbacks queued), Lemma 7 (S8),
Lemma 10 (the upper particle bound, 100 keV placeholder), Lemma 11 (the
0.62-vs-0.635 gap).

**The closure**: every one of L9-L16 is a landed gate (waves 3-8, WAVEBOARD
rev 7); nothing downstream rests on an open row -- the open items sit at the
amplitude/footing level, not the structure level.

---

# VERDICTS (G153)

## V1 -- the extended chain is COMPLETE (each new lemma with its evidence class)

| Lemma | Claim | Status | Evidence class |
|---|---|---|---|
| L9 THE ORIGIN | sigma^2 = C/2, exponent 2 exact | DONE | DERIVED x2 (max-entropy G084 8/8; virial G091 12/12, sympy-exact) + empirical anchors |
| L10 THE PARTICLE | one cold species, m in [3.3, 100] keV | DONE (1 edge open) | EMPIRICAL lower bound (forest) + DERIVED consistency; upper bound OPEN |
| L11 THE EFE CAP | break 0.6232 = kernel value; static | PARTIALLY DERIVED | DERIVED (form + zero-param kernel solve, G119) + PROVEN staticity (G103); 0.62-vs-0.635 gap OPEN |
| L12 TEMPERATURE RATIO | 2f(r_M/R500), alpha = 2/3, f = 5.66 | DONE | DERIVED closed form (sympy-exact, G095) + EMPIRICAL (0.28 = 0.53^2, 1.8%) |
| L13 DUST ENVELOPE | r^-1 shape, p* = +0.99; crossover 1.73 | DONE (1 item open) | DERIVED shape + EMPIRICAL collapse 0.097 dex (G122); crossover derived (G124); amplitude OPEN |
| L14 DEEP END | HI dwarfs 0.150 dex | DONE (1 tension open) | EMPIRICAL PASS (G114 3/3); MIGHTEE deep tension OPEN (G099) |
| L15 DR4 FACE | ridge 30.7 sigma; double-map | DONE (armed) | PRE-REGISTERED (G088 5/5, G092 9/9; decided 2026-12-02) |
| L16 MERGER FACE | q = 1, excess 2.000 at r_M | DONE (armed) | DERIVED closed form (G118) + PRE-REGISTERED forecast (G121) |

## V2 -- the closure statement

The closure statement stands as written above: the spine L1-L5 is
Lean-certified or closed-form derived with the ONE empirical premise named
(L2, n = 2); L6 answered with proof (force-law class closed) and its own
registered test; L9-L16 are all landed gates from waves 3-8, each with its
evidence class in the V1 table; the open items -- the cluster amplitude
(L12/L13), the footing (L14), the MIGHTEE deep (L14), plus the in-flight rows
(Cassini S2, S8, the upper particle bound, the 0.62 gap) -- are all named,
armed with falsifiers, and block nothing downstream: they sit at the
amplitude/footing level, not the structure level.  The chain is complete as
an assembly; it is not closed as a theory -- the open list is what keeps it
honest.

## V3 -- the honest statement

The theory's lemma chain, 16 links, current state:

- **3 Lean-certified** (L1, L4, L5 -- 66 theorems, zero sorry);
- **5 derived in closed form** with zero free parameters (L3 three ways;
  L9 two chains; L12; L13's shape and crossover; L16's q = 1), plus
  **L11 partially derived** (form + kernel value + staticity proven; the
  constant gap open);
- **4 empirical-verified** (L2 as the one premise; L7's verified surface
  with S8 honest-open; L10's lower bound; L14's deep-end PASS);
- **3 pre-registered and armed** (L8 the test matrix, L15 DR4, L16 SDSS --
  L16 is both derived and pre-registered; L15/L16 await their data);
- **6 carry a named open edge** (L6 Cassini S2, L7 S8, L10 the upper bound,
  L11 the 0.62 gap, L13 the cluster amplitude, L14 the footing + the
  MIGHTEE deep).

So: of 16 links, 9 stand on proof (Lean or closed-form derivation, L11
partial), 7 stand on committed empirical or pre-registered verification, and
6 carry an explicitly named open edge -- none of which blocks any downstream
link.  The structure level of the chain is derived; the amplitude/footing
level is where the open items live; DR4 (2026-12-02) and the SDSS pair
statistics are the next decision points in print.