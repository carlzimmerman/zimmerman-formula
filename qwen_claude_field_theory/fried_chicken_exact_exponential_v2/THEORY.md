> ⚠️ **QUARANTINED / SUPERSEDED — NOT the current candidate.** Fried-Chicken **exact-exponential** kernel
> (μ=1−e⁻ʸ / tanh), eliminated by the Cassini EFE quadrupole at 3.76× the ceiling (committed:
> `qwen_claude_field_theory/closure_2026/FC_AEST/scripts/fc_cassini_CORRECTED_2026.py`). The frozen candidate
> is **SHARP-J₁₀ FC-FINAL** (AeST + μ₁₀(y)=y/(1+y¹⁰)^{1/10}, a₀ constant, 6-DOF) in
> `qwen_claude_field_theory/fc8_closure_2026/`. Do not mix the exponential branch into FC-FINAL. Historical record.

# Candidate theory

S = S_GR + S_MOND + S_m

S_GR = (1/16 pi G) integral sqrt(-g) (R - 2 Lambda) d^4x

S_MOND = -(a0^2/16 pi G) integral sqrt(-g) M[g] d^4x.

The causal nonlocal definitions follow Deffayet & Woodard (2026):

u_mu = partial_mu phi,
 g^{mu nu} partial_mu phi partial_nu phi = -1,
 phi(t0,x)=0.

U[g] = Box_ret^{-1}(R_{mu nu} u^mu u^nu),

Z[g] = (4 c^4/a0^2) g^{mu nu} partial_mu U partial_nu U.

M[g] is defined by the first-order transport equation

partial_mu[sqrt(-g) u^mu M] = -partial_mu[sqrt(-g) u^mu f(Z)],

with the same type of initial data used in the published construction.

For the exact exponential interpolation, let y = c^2 |grad Psi| / a0 and Z = 4 y^2 in the static weak-field sector. Require

mu(y) = 1 - exp(-y).

Then the exact positive-Z branch is

f_+(Z) = 4 [1 - (1 + sqrt(Z)/2) exp(-sqrt(Z)/2)],  Z >= 0,

so

f_+'(Z) = (1/2) exp(-sqrt(Z)/2),

and with the weak-field normalization mu = 1 - 2 f'(4 y^2), one gets exactly

mu(y) = 1 - exp(-y).

The corresponding AQUAL primitive is

F(y) = y^2/2 + (1+y) exp(-y) - 1.
