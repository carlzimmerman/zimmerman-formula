# Particle-free result and the exact closure gap

2026-09-20. User constraint: **no dark-matter particle**. This supersedes the
earlier recommendation to explore an independently normalized chi carrier as
the answer to the user's closure request. A classical gravitational field is
not automatically a particle species; the previous carrier nevertheless added
an independently specified gravitating component and did not establish the
requested closure.

**Full novel theory: not closed. Static conditional response: certified below.**
No cold species, particle mass, decay line, or free-streaming assumption is used.

## What the new certificate actually proves

Use the explicit two-channel family examined in the normalization audit:

\[
 \mu_\lambda(y)=1-(1+\lambda y)^{-2},\qquad y=g/s,
 \quad \lambda,s>0.
\]

This is an admissible constitutive example and normalization counterfamily,
not a derivation of the repo's exponential response or a replacement claimed
to be its unique fundamental action. A nonrelativistic action realizes it:

\[
 L=-\int\left[\frac{s^2}{8\pi G}F_\lambda(|\nabla\Phi|^2/s^2)
                    +\rho_b\Phi\right]d^3x,
\]
\[
 F_\lambda(y^2)=y^2-\frac2{\lambda^2}
  \left[\log(1+\lambda y)+(1+\lambda y)^{-1}-1\right].
\]

Exact symbolic differentiation verifies \(F'_\lambda(y^2)=\mu_\lambda(y)\).
For fixed-boundary variations, the ordinary variational calculation gives
\(\nabla\cdot[\mu_\lambda(|\nabla\Phi|/s)\nabla\Phi]=4\pi G\rho_b\).
The spatial variational calculus and Gauss theorem are explained here, not
formalized in the Lean file.

For a spherical isolated baryonic source, with no additional central flux,
\(\mu_\lambda(g/s)g=GM_b(r)/r^2\). Define
\(t=\lambda g/s\) and \(b=\lambda GM_b(r)/(sr^2)\). Then

\[
 f(t)=t[1-(1+t)^{-2}]=b.
\]

**Lean proves that every real \(b\ge0\) has exactly one real \(t\ge0\).**
The proof uses a strictly positive difference quotient for unequal nonnegative
arguments, continuity, and the intermediate value theorem. It is not a grid
search. Therefore this spherical law has no independent halo amplitude once
the baryonic source, constitutive scales and boundary flux are fixed. The
zero-source solution is zero. This is a pointwise spherical existence result,
not a global PDE or time-evolution theorem.

The transverse and longitudinal static response eigenvalues are positive at
nonzero gradient:

\[
 \mu=\frac{t(t+2)}{(1+t)^2},\qquad
 \mu+y\mu_y=\frac{t(t^2+3t+4)}{(1+t)^3}>0.
\]

They vanish at zero gradient. No uniform ellipticity or dynamical stability
claim is inferred from these expressions.

In the deep limit, \(\mu\sim2\lambda g/s=g/a_0\), with
\(a_0=s/(2\lambda)\). The limiting Gauss law and circular balance imply

\[
 r^2g^2=GM_ba_0,\quad v^2=rg
 \quad\Longrightarrow\quad \boxed{v^4=GM_ba_0}.
\]

This implication is separately checked in Lean. It is exact for the limiting
equations and asymptotic for the interpolating model. Outside a compact source,
write \(C=\sqrt{GM_ba_0}\). Then the Newtonian-inferred total mass is
\(M_{\rm dyn}=Cr/G\), the excess is \(M_{\rm dyn}-M_b\), and its local
exterior density is \(C/(4\pi G r^2)\). This density is a rewrite of the
gravitational response, not an independently postulated material distribution
or a demonstrated equality to a covariant scalar's Hilbert stress tensor.
These exterior deep-regime formulas cannot be extended to the source center.

## Why this still does not close the novel theory

1. **The normalization remains free.** The whole positive-lambda family has
   two channels, the correct asymptotic regimes and positive nonzero-gradient
   static response. Nevertheless \(\kappa=a_0/s=1/(2\lambda)\). The existing
   `../pd_normalization/PDNormalization.lean` proves the generalized slope and
   normalization statements. Counting two channels cannot select lambda=1.
2. **A static inferred density is not a cosmological dynamical component.**
   The missing calculation is one specified particle-free covariant action
   whose variations yield the galactic response, both lensing potentials and
   stable cosmological perturbations with the same constants and stated initial
   data. The earlier carrier kinetics certificates do not supply this result.
3. **PD04/PD05 do not supply that bridge.** PD04 imports a cold particle species
   and substitutes assertions for the claimed branch/channel correspondence.
   PD05's compiled limit theorem rules out an added nonzero constant in a
   particular origin limit; it does not prove absence of all particles or derive
   a gravitational stress tensor. See `PD04_NOTE.md` for the source audit.

The useful reframing is to derive the observable gravitational response from
the action and baryonic source, retaining only field data actually required by
that action. The independent-particle interpretation is unnecessary for the
static theorem. Whether the same theory closes cosmology remains open.

## Scientific attribution and evidence

The action-based particle-free modified-Poisson mechanism is established prior
work: Bekenstein & Milgrom, *Does the missing mass problem signal the breakdown
of Newtonian gravity?*, ApJ 286 (1984), pp.7–14, especially §II equations 2b–5,
[primary paper](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B),
[DOI](https://doi.org/10.1086/162570). Full primary text was checked through the
web tool on 2026-09-20 after consulting the repo's literature scope. No new local
paper copy was downloaded. This citation supports the variational framework,
not empirical validation or novelty of the user's full theory. BTFR and this
general mechanism are not claimed as a new discovery.

`BaryonResponse.lean`: nine named theorems, freshly compiled with printed axiom
dependencies. `verify.py`: thirteen exact symbolic identities/limits plus fresh
Lean compilation. `run/manifest.json`: command, pinned input and result hashes,
software, revision, dirty state and resource bounds. `run/lean.txt` and
`run/result.json` are the actual outputs. Standard Lean foundations only:
`propext`, `Classical.choice`, `Quot.sound`; no added physics axioms or `sorryAx`.

The certificate's mathematical implications are universal in their stated real
domains. No observation fit, particle ontology, first-principles scale selection,
or complete relativistic/cosmological theory is certified.
