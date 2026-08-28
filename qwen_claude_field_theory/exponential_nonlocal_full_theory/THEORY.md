> ⚠️ **QUARANTINED / SUPERSEDED — NOT the current candidate.** This document uses the **exponential MOND
> kernel** (μ=1−e⁻ʸ / tanh family), which was **eliminated by the Cassini EFE quadrupole at 3.76× the
> ceiling** (committed: `qwen_claude_field_theory/closure_2026/FC_AEST/scripts/fc_cassini_CORRECTED_2026.py`).
> The **frozen candidate is the SHARP-J₁₀ FC-FINAL** — AeST + `μ₁₀(y)=y/(1+y¹⁰)^{1/10}`, a₀ constant,
> 6-DOF-AeST — in `qwen_claude_field_theory/fc8_closure_2026/` (`FROZEN_CANDIDATE.md`, `THEOREM_PACKAGE.md`).
> **Do not mix the exponential branch into FC-FINAL.** Retained as historical record (append-only).

# Exact-Exponential Nonlocal MOND Candidate

Status: explicit candidate / not fully certified.

## 1. Action

In the conventions of Deffayet & Woodard (JCAP 04 (2026) 081), take

S = S_GR + S_MOND + S_m,

S_GR = (1/16 pi G) int d^4x sqrt(-g) (R - 2 Lambda),

S_MOND = -(a0^2/16 pi G) int d^4x sqrt(-g) M[g].

The nonlocal functional M[g] is defined below; this is a metric-only causal construction once the retarded/initial-value prescriptions are fixed.

## 2. Timelike clock field

Define phi[g] by

g^{mu nu} partial_mu phi partial_nu phi = -1,
phi(0,x)=0,

and u_mu = partial_mu phi.

Equivalently, in ADM variables,

dot(phi) = N sqrt(1 + gamma^{ij} partial_i phi partial_j phi) - N^i partial_i phi.

## 3. Nonlocal acceleration invariant

Define

Z[g] = 4 c^4/a0^2 * g^{mu nu} partial_mu U partial_nu U,

where

U[g] = Box_ret^{-1}(R_{alpha beta} u^alpha u^beta),

with null retarded initial data.

In the static weak-field limit,

Z -> 4 (c^2 |grad Psi|/a0)^2 = 4 y^2.

## 4. Exact exponential MOND branch

For Z >= 0 define

f_+(Z) = 4 [1 - (1 + sqrt(Z)/2) exp(-sqrt(Z)/2)].

Then

f_+'(Z) = 1/2 exp(-sqrt(Z)/2),

and the weak-field relation in this normalization is

mu(y) = 1 - 2 f_+'(4 y^2) = 1 - exp(-y).

The corresponding AQUAL primitive is

F(y) = y^2/2 + (1+y) exp(-y) - 1,

with F'(y)=y[1-exp(-y)].

## 5. Cosmological continuation (candidate)

For Z < 0 one needs a continuation for which f is suppressed at large negative Z and which matches the MOND branch at Z=0.

A minimal test continuation is

f_-(Z) = Z exp(Z)/2.

It obeys f_-(0)=0 and f_-'(0)=1/2 and tends to zero as Z -> -infinity.

This continuation is a test ansatz, not an established result. The full theory remains dependent on the cosmological/transition analysis.

## 6. Interpolation functional M[g]

Define M by the causal first-order transport equation

partial_mu [sqrt(-g) u^mu M]
 = - partial_mu [sqrt(-g) u^mu f(Z)],

with initial data

M(0,x) = 45 / sqrt(det[g_ij(0,x)]).

For cosmology, Z is large and negative so f(Z) is suppressed and M approaches the positive homogeneous solution that reproduces the dustlike effective stress tensor.

For a gravitationally bound region where spatial dependence dominates, the transport equation can drive M toward -f(Z), giving the MOND branch.

## 7. Weak-field equation

On the static, weak-field branch with M -> -f(Z), variation reduces to

nabla . [ mu(|grad Psi|/a0) grad Psi ] = 4 pi G rho_b,

with

mu(y)=1-exp(-y).

Hence

nabla . [(1-exp(-|grad Psi|/a0)) grad Psi] = 4 pi G rho_b.

## 8. What is actually established

Established by direct algebra in this repository:

* exact positive-Z reconstruction of the exponential mu;
* AQUAL primitive;
* static constitutive ellipticity;
* causal nonlocal definitions of phi, U and M consistent with the published architecture.

Not established here:

* full nonlinear ADM/Dirac physical degree-of-freedom count;
* proof that the retarded prescription is dynamically equivalent to a ghost-free reduced phase space;
* full Z<0 to Z>0 transition solution;
* nonlinear structure formation;
* cluster phenomenology and external-field effect;
* all-background scalar/vector stability;
* derivation of M[g] from a microscopic quantum-gravity resummation.

The candidate is therefore a concrete theory to attack, not a certified final theory.
