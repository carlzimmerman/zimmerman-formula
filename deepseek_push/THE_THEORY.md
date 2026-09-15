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