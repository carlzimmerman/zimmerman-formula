# Existing scalar source exchange: exact sign results and the missing memory join

20 October 2026. Base pinned at inspection:
`b10ed68d6bbc90744c5aa77ae7c702c2898507c1`.
Only this new `scalar/` directory was written. This is an analytic research
derivation with a bounded symbolic cross-check, not a completed memory mechanism.
HEAD moved externally to `502a070a275bb307da40a7f8847f20e30f6e9178` by final
source hashing. The master working copy differs from the pinned base in
unrelated added dwarf/transport discussion; its scalar Hamiltonian and frozen
benchmark were re-read unchanged. Several later review inputs are untracked
at the pinned base; `source_hashes.json` records their exact working bytes.

The exact analytic convention and its finite-regulator qualification are
stated explicitly; no claim is made that continuum point contact alone
defines the full quantum theory.

**Result.** Retaining the original repulsive contact prevents virtual source
exchange from binding two daughters below the flat-space threshold. The exact
one-mode fixed-charge blocks also have positive charge-addition curvature in
that regime. A sufficiently confining pre-existing gravitational host can
reverse both signs, without changing a microscopic coupling: it lowers the
source level relative to two daughter levels. The sign reversal is exact in
the specified mode projection, and the daughter-pair binding implication has a
conditional finite-regulator variational formulation. No actual host is specified by the frozen
inputs, and this charge-addition curvature is not the required fixed-inventory
conversion curvature. In the fixed-Q=4 source-count basis that latter bare
diagonal curvature remains **8 kappa > 0**. The memory closure therefore remains
incomplete, with a precisely identified projector, host and dynamics gap.

## 1. Raw Hamiltonian and matching, without counting exchange twice

The analyzed leading retained-source, normal-ordered NR Hamiltonian is

```
H = m Q + integral [ |grad psi|^2/(2m) + |grad b|^2/(2M)
       + delta b†b + c3 (b†psi^2 + psi†^2 b) + kR psi†^2 psi^2 ],
Q = integral (psi†psi + 2 b†b),
delta=M-2m>0, c3=g/(2m sqrt(2M)).
```

The original positive-frequency reduction has `kc=lambda_tot/(4m^2)` and
`lambda_tot=g^2/[delta(M+2m)]+lambda_rep`. The fully threshold-matched
retained-source kernel includes only the analytic negative-frequency correction

```
delta_k = -g^2/[8m^2 M(M+2m)],
kR = kc + delta_k,
kR - c3^2/delta = lambda_rep/(4m^2) > 0.             (1)
```

The propagating positive-frequency source is retained explicitly. Its exchange
is not also subtracted from `kR`. Conversely, using the already eliminated
daughter contact `g2/2=lambda_rep/(4m^2)` while retaining the same source would
count its threshold exchange twice. These conventions are from the raw master
equations, `micro_response/DERIVATION.md` section 1, and its exchange audit.
Directly completing the square with (1) proves positivity for this *specified*
matched finite-regulator NR truncation as well. This does not claim a full
renormalized relativistic theorem.

## 2. Exact virtual-source elimination in the flat Q=2 sector

Let `A` map a daughter pair into its coincident spatial amplitude, with the
bosonic normalization included in A. At a finite common spatial/contact
regulator, the source block is `delta+Tb`, `Tb>=0`, and the daughter block is
`T2+kR A†A`. The exact Schur operator at excess energy z is

```
F(z) = T2 + kR A†A - c3^2 A†(delta+Tb-z)^(-1) A.
```

For `z<=0`, inverse ordering follows by diagonalizing the nonnegative finite
matrix Tb, giving

```
F(z) >= T2 + (kR-c3^2/delta) A†A >= 0.             (2)
```

Thus the full retained source, including virtual propagation and the repulsive
contact exactly once, produces no negative-energy pair eigenvalue below the
flat `2m` threshold. This is the source-exchange test, not an inference merely
from a bare quartic sign. The previously recorded rank-one source-resolvent
argument reaches the same flat-space conclusion; (2) makes its operator domain
and contact bookkeeping explicit.

At positive energy the coefficient `kR-c3^2/(delta-z)` can become negative.
Its zero is `zc=delta-c3^2/kR>0`. At the frozen published benchmark
`m=1 MeV,u*=.02,r_lambda=2,g=2168 eV` (g is its published rounded value),
`delta=399.960008 eV`, `zc=266.648891 eV` approximately. This is a
positive-energy near-resonant scattering sign. It does not supply negative
ground-state occupation curvature or a stable receiver. A real source cannot
be removed as though it were virtual across its pole.

## 3. Exact lowest Q=2 and Q=4 mode blocks, including the sign reversal

Project onto one normalized daughter orbital phi and one normalized source
orbital chi, with one-body energies epsilon_a, epsilon_b measured relative to
their respective rest masses. Define

```
I4=integral |phi|^4,
I3=integral chi* phi^2,
kappa=kR I4>0, eta=c3 I3,
Delta=delta+epsilon_b-2epsilon_a.
```

A phase choice makes eta real. Subtract `epsilon_a Q`; the retained Hamiltonian
is exactly

```
h = Delta nb + eta(b†a^2+a†^2b) + kappa a†^2 a^2.
```

This is an exact Hamiltonian on the projected Fock space; spatial projection
is not asserted to be an invariant subspace of the full field theory. In the
Q=2 basis `(na,nb)=(2,0),(0,1)`,

```
h2 = [[2 kappa, sqrt(2) eta], [sqrt(2) eta, Delta]],
e=E2=(2kappa+Delta-sqrt((2kappa-Delta)^2+8eta^2))/2. (3)
```

For nonzero eta, `e<min(2kappa,Delta)`. In the Q=4 basis
`(4,0),(2,1),(0,2)`,

```
h4 = [[12kappa, sqrt(12)eta, 0],
      [sqrt(12)eta, Delta+2kappa, 2eta],
      [0, 2eta, 2Delta]].                          (4)
```

Using `eta^2=(2kappa-e)(Delta-e)/2`, eliminate the positive endpoint pivots
`A=12kappa-2e` and `C=2Delta-2e` of `h4-2e I`. Its middle Schur complement is

```
S = Delta+2kappa-2e - 12eta^2/A - 4eta^2/C
  = 2e(Delta-e)/(6kappa-e),
det(h4-2e I)=8e(Delta-e)^2.                        (5)
```

All factors other than e in S are positive. Completing these two scalar
squares proves

```
sign(E4-2E2+E0) = sign(e),  E0=0.                 (6)
```

For `Delta>0`, this is also the sign of `kappa Delta-eta^2`. For `e=0`, the
matrix is positive semidefinite with a zero eigenvalue; equality in (6) is
exact. For `eta=0` the decoupled exceptions must be treated directly; (6) is
not asserted for that exception. The frozen benchmark has nonzero coupling.

Consequently the flat uniform mode (`Delta=delta`, `|I3|^2<=I4`) has both
`E2>0` and `E4-2E2>0`, for every regulator volume. The original contact
condition and Cauchy-Schwarz prove this without selecting a volume or fitting
an interaction. Conversely, `0<Delta<eta^2/kappa` gives **negative** values
of both curvatures even while the unmixed source channel remains above the
two-daughter level. This is virtual closed-source attraction in the declared
occupied-mode projection, not just a bare negative exchange term.

There is also an explicit magnitude bound. For `e<0`, take the vector with
middle entry 1 and endpoint entries `-sqrt(12)eta/A,-2eta/C`. Its norm is
`N=1+12eta^2/A^2+4eta^2/C^2`, so the variational principle gives

```
E4-2E2 <= S/N < 0.                               (7)
```

Were this quantity the actual memory pair energy, (7) would suffice for the
declared finite-latch sign/temperature condition whenever
`theta < -S/(3 N ln2)`. No theta or host is chosen here, and the identification
required by that conditional sentence is absent.

## 4. A host from the existing gravity can reverse the mode sign

The previous `occupied_landscape/LANDSCAPE.md` supplies a conditional
Newtonian baryon-host potential, but supplies no actual host mass/profile.
Use its heavy, static, point-center Coulomb control, now for both original
species, with gravitational masses m and M respectively:

```
Va=-G Mb m/r, Vb=-G Mb M/r,
epsilon_a=-(G Mb)^2 m^3/2, epsilon_b=-(G Mb)^2 M^3/2,
ad=1/(G Mb m^2), ab=1/(G Mb M^2), beta=ad/ab=M^2/m^2.
```

The physical source mass convention includes the small detuning contribution
to gravitational mass; retaining only `mQ` is the further leading cold-rest
approximation. These assumptions are explicitly a conditional external-host
calculation, not a discovered baryon material phase. For the exact 1s orbitals,

```
I4 = 1/(8 pi ad^3),
I3 = 8 ab^(3/2)/[sqrt(pi)(ad+2ab)^3],
rho=|I3|^2/I4=512 beta^3/(beta+2)^6.               (8)
```

Thus the sufficient closed-source attraction interval in this projection is

```
0 < Delta_h=delta-(G Mb)^2(M^3-2m^3)/2
  < rho c3^2/kR.                                 (9)
```

Writing `alpha=G Mb m`, its algebraic endpoints at the frozen scalar benchmark
are approximately `0.01010 < alpha < 0.01154`; exact arithmetic values are in
`run_002/results.json`. **These are derived boundaries, not selected/scanned
hosts.** The speed parameters alpha and `(M/m)alpha` remain small in this
conditional Coulomb calculation. A host would also have to be compact on the
source-orbital scale `Rhost << ab`, live long enough, permit the bound state,
and supply recoil/work consistently. None is furnished by the frozen inputs.

At a **common finite regulator**, choose phi to be the exact regulated
single-daughter ground orbital, and use the same regulated matrix elements
for I3,I4 and the source level. If `Delta_reg<eta_reg^2/kappa_reg`, (3) is
a full-regulated-Hamiltonian variational witness: the true Q=2 ground energy
is no larger, and E1 is known exactly by that definition. This proves
`E2_full,reg<2 E1_full,reg` under that explicitly checkable regulated condition.
The continuum Coulomb expressions (8)-(9) are not themselves a completed
3D contact-QFT construction: a continuum point contact needs a regulator and
matching prescription. At a finite grid/cutoff, the exact Coulomb 1s energies
and overlaps are modified. Transferring their strict inequality requires a
consistently regulated, suitably smooth physical host/orbital calculation
which preserves its margin. That additional check has not been performed.
In contrast, even a negative regulated Q=2 witness does not prove the
full-field inequality `E4_full-2E2_full<0`: separate upper bounds on E4 and E2
cannot establish their difference. Omitted orbitals and all induced
interactions must be controlled to transfer (6)-(7). No full-mode
source-sized attraction is claimed here.

A useful exclusion check requires no Coulomb idealization. If a specified
host has `Phi_N in [-Psi0,0]`, then `epsilon_b>=-M Psi0` and
`epsilon_a<=0`, so `Delta_h>=delta-M Psi0`. If
`delta-M Psi0>=c3^2/kR`, Cauchy-Schwarz excludes the sign reversal for every
such two-orbital projection. This is a sufficient bound, not a necessity.
The weaker `Psi0<delta/M` merely keeps this lower bound positive; it does
not by itself prove the contact-subtracted pair curvature positive.

## 5. Fixed inventory and the source-to-memory dictionary

Charge-addition curvature compares lowest energies in different local Q
sectors. It can be embedded in an overall fixed-Q=4 bookkeeping by keeping
the unused charge in an isolated free reference region: a linear reservoir
energy cancels from the second difference. That embedding requires a real
receiver and negligible interregion terms. It does not derive sites,
distinguishability, or a conversion operator.

An especially important distinct question is **source count at fixed Q=4**.
For the literal bare source-count n=0,1,2 in (4), the diagonal energies are

```
E_diag(n)=(12kappa, 2kappa+Delta, 2Delta),
E_diag(2)-2E_diag(1)+E_diag(0)=8kappa>0.            (10)
```

The conversion eta is off diagonal. The lowest eigenstates used in (6) are
coherent mixtures of source counts; they are not three declared diagonal
occupation energies at fixed inventory. A negative charge-addition curvature
therefore cannot be substituted for the memory criterion
`U_pair<-3theta ln2` without constructing the actual coarse occupation
projectors and their complete energies/free energies. A bath/dephasing limit
or a slow coordinate, when justified, can change that coarse description;
neither is generated by merely diagonalizing (4).

There is a stronger exact zero-temperature test for these literal source-count
projectors. After a phase change the two off-diagonal entries are
`-t0,-t1`, with `t0=sqrt(12)|eta|>0,t1=2|eta|>0`. Replacing a ground
eigenvector by the absolute values of its components cannot increase its
energy, and its eigen-equations prohibit a zero component in that nonnegative
vector. Thus choose its three amplitudes A0,A1,A2 strictly positive. If both
source-count endpoint probabilities exceeded the middle probability, then
`A0>A1` and `A2>A1`. The endpoint equations would give

```
d0-E=t0 A1/A0<t0,   d2-E=t1 A1/A2<t1,
```

while the middle equation would give `d1-E>t0+t1`. But (10) also gives
`d1=(d0+d2)/2-4kappa`, hence
`d1-E<(t0+t1)/2-4kappa`, a contradiction. Therefore the exact ground-state
source-count distribution in this Q=4 mode projection cannot have both
endpoint peaks, for any Delta, including the attractive regime (9). Each
bare Fock count has multiplicity one; the memory's `(1,4,2)` does not occur
here. This statement does not cover finite temperature, driven preparation,
or a different physical occupation projector. The parent supplied this
additional discriminator, reconstructed here from the three eigen-equations.

The original fields do identify charge-one daughters, charge-two sources,
and a reciprocal conversion vertex. They do **not** identify which combination
is the memory's tethered/free label, its two distinguishable one-place sites,
its `(1,4,2)` multiplicities, or its finite Metropolis operator. The master
document explicitly treats the carrier and polarization force sector as
separate models with an open join. Adding the negative energy in (7) to the
canonical full-remainder shell H without deriving this common dictionary would
assume that join and could count the same gravitational work twice. No bare
source population is relabeled as an ordinary-gravity-only released stock.

## 6. Exact scope, verification, novelty and remaining gap

Novelty gate: the flat-space positive quartic and rank-one threshold exclusion
were already recorded. The new useful results here are the exact Q=4
Schur/sign theorem (5)-(7), its host-dependent reversal condition including
the exact overlap (8), and the fixed-inventory discriminator (10). The
original occupied-landscape interwell gravity result concerns a different
hard-core well projection and is not counted again as a new source mechanism.

The mathematical proofs are displayed above. `check_algebra.py` cross-checks
the Schur and determinant identities, (8), (10), and the fixed published
coefficient arithmetic. It selects no host, scans no parameters, runs no
dynamics, and uses at most a 3x3 symbolic matrix. Its one-process successful
run has 20 CPU-second and 30 wall-second caps and observed peak RSS 51,412,992
bytes, below 1 GB. The first affinity-requesting runner invocation stopped
before execution because affinity limits are unavailable on this macOS host.
A second launch using a 512 MiB address-space limit failed in preexec before
the mathematical command ran; its failure manifest is preserved in `run_001/`.
The executed run omitted these unsupported limits and selected no host.
`run_002/manifest.json` records the successful command and observed inputs;
the skill validator accepted it with `run.status=completed`. Source bytes are pinned
in `source_hashes.json`. The symbolic check is author self-review. It is
not independent physical validation, a continuum limit, or a sampling proof.

**Primary verdict: conditional on a named input, with memory closure incomplete.**
An actual host and a controlled complete occupied-mode reduction can generate
attraction using only the existing scalar and gravitational interactions.
They have not been specified or verified at the frozen benchmark. More
fundamentally, the negative sign demonstrated for charge addition is not yet
the fixed-inventory conversion energy required by memory; the literal bare
source-count curvature has the opposite sign. The smallest decisive next
step is to specify the physical occupation projectors in one actual existing
host, retain the complete fixed-charge Hamiltonian, and compute those exact
conversion energies and transition matrix elements. Until then there is no
derived J, no declared finite-latch state count, and no memory closure.
