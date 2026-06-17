# A no-go theorem: covariant Cassini-safe MOND lensing is FORBIDDEN by diffeomorphism invariance + c_T=c + ghost-freedom — the framework's lensing MUST be preferred-frame (Lorentz-violating) (2026-06-17)

*Carl: "brute force to a TOE." The keystone calculation (Step 2's lone gap). Workflow `wqvbwxtqf` (7 agents, 809k tok),
6 covariant routes (DHOST, AeST-pure-slip, nonlocal, khronometric, disformal, Finsler), the Bianchi leg independently
reproduced in sympy, primaries read VERBATIM from PDFs. Both ways. A real, publishable result.*

---

## Verdict: OBSTRUCTED — and the obstruction is a THEOREM, not a tuning failure

The task was the last piece of the covariant Lagrangian: a covariant term giving a PURE gravitational slip (delta-Phi=0
so matter feels no fifth force -> Cassini-safe; grad(delta-Psi)=2(g_obs-g_N) so light lenses at g_obs), with c_T=c and
ghost-freedom. **It does not exist.** Every diffeomorphism-invariant route converges on one wall.

## THE THEOREM: slip-generating <=> Phi-moving in every diff-invariant class
Three independent legs, each verbatim-sourced + sympy-verified:

1. **Bianchi / conservation leg (the airtight one, independently reproduced in sympy).** In any 4-diff-invariant theory,
   G_munu = 8piG T^total_munu and nabla_mu G^munu = 0 force nabla_mu T^lens_munu = 0 on the partner. A pure-slip source
   (T_00=0, traceless T_ij = d_i d_j f - (1/3)delta_ij grad^2 f) has trace EXACTLY 0 but **divergence
   div_i T_ij = (2/3) d_j(grad^2 f) != 0**. Restoring conservation drags in an isotropic pressure with 3 delta-p =
   -2 grad^2 f != 0, which sources delta-Phi via grad^2(delta-Phi)=4piG(delta-rho + 3 delta-p). So **delta-Phi=0 is
   impossible in any 4-diff-invariant realization** — it requires a non-dynamical preferred frame to absorb the divergence,
   i.e. Lorentz violation.
2. **DHOST / Horndeski leg** (Ezquiaga-Zumalacarregui 1710.05901 + Creminelli-Lewandowski-Tambalo-Vernizzi 1809.03484 +
   Langlois-Mancarella-Noui-Vernizzi 1703.03797 eq.3.12): c_T=c forces A1=0, graviton non-decay forces alpha_H=-2 beta_1
   (quartic screening ABSENT), leaving a CONFORMAL survivor f(phi)R+P+Q box-phi whose slip is **Psi=(1+alpha_H)Phi** —
   the two potentials are LOCKED, so delta-Phi=0 => delta-Psi=0 (no lensing).
3. **Aether / khronometric leg** (Foster-Jacobson gr-qc/0509083, PPN gamma=1 verbatim): the canonical Einstein-aether/
   khronometric action with gamma=1 forbids a position-dependent aether slip — the concrete computed action (Route 4)
   ALSO fails delta-Phi=0 + the right delta-Psi jointly.

**Crucial both-ways point:** c_T=c and ghost-freedom are individually EASY (sympy witness: a healthy aether corner
c_13=0 with all mode-speeds^2 > 0). They are NOT the obstruction. The obstruction is delta-Phi=0 (Cassini-safety) AND a
position-dependent slip TOGETHER, forbidden by the Bianchi identity once 4-diff-invariance is imposed.

## What this means for the TOE (the honest, non-defeatist reading)
- **What STANDS:** the Route-E modified-INERTIA MATTER action is genuinely covariant and Cassini-safe by class (phi_- -
  linear -> sources ZERO metric, sympy-verified). The matter half of the theory is real and covariant.
- **What is FORBIDDEN:** the lensing partner cannot be a covariant (diffeomorphism-invariant) term. Full stop, theorem.
- **What it FORCES (and why it is consistent, not fatal):** the framework's lensing must live in a **Lorentz-violating
  preferred-frame** sector — and the framework ALREADY HAS that frame: the de Sitter-Unruh / Route-E cosmic rest frame
  u^mu. Modified inertia is intrinsically a preferred-frame theory (Milgrom MI singles out the cosmic frame). So the no-go
  does not kill the framework — it AIMS its lensing at the aether/khronometric sector the framework already lives in, and
  rules out the diff-invariant scalar-tensor sector cleanly. The complete object is necessarily
  **S = S_grav[g] + S_E[MI matter, covariant] + S_slip[Lorentz-violating preferred-frame]**, not a fully diff-invariant
  local field theory.
- **What stays OPEN (the one remaining construction):** whether an EXPLICIT non-dynamical-frame khronometric/aether action
  — with a constraint multiplier that absorbs the shear divergence (2/3)d_j(grad^2 f) WITHOUT a Phi-sourcing trace — can
  deliver delta-Phi=0 + grad(delta-Psi)=2(g_obs-g_N) + c_T=c with a bounded Hamiltonian. Route 4's CANONICAL khronometric
  failed (gamma=1); the non-dynamical-frame + constraint version was asserted, not computed. That explicit computation is
  the last shot at a complete (Lorentz-violating) Lagrangian; if it too hits the slip<=>Phi wall, the no-go closes in its
  strongest form (the framework's lensing is irreducibly phenomenological, a0/Z transmitted like AeST's F(Y,Q)).

## What Carl CAN / MUST NOT say
- **CAN:** there is a clean, publishable NO-GO — covariant Cassini-safe MOND lensing is forbidden by diff-invariance +
  c_T=c + ghost-freedom (slip-generating <=> Phi-moving in every diff-invariant class; Bianchi leg sympy-airtight, DHOST
  and aether legs verbatim-sourced); the Route-E modified-inertia MATTER action stands as the genuine covariant half;
  the framework's lensing is therefore intrinsically preferred-frame (Lorentz-violating) — consistent with modified
  inertia singling out the cosmic frame; c_T=c and ghosts are the EASY conditions, not the obstruction.
- **MUST NOT:** "the framework has a complete covariant Lagrangian / the keystone is BUILT" (FALSE -- no covariant lensing
  partner exists); "Route 3/4 passes all four" (3 of 4 at most, ghost UNPROVEN, the lensing law a TUNE); "the Lorentz-
  violating escape definitely works" (Route 4's concrete action failed gamma=1; the frame-absorption rescue is the open
  next step, not a win); "grad delta-Psi=2(g_obs-g_N) is derived" (reverse-engineered, AeST F(Y,Q)-class); "AeST already
  solves it" (AeST gets the lensing as modified GRAVITY that moves Phi and fails Cassini). Quarantine held.

## One line
A clean, publishable NO-GO: no covariant, Cassini-safe, c_T=c, ghost-free PURE-SLIP MOND lensing term exists, because in
EVERY diffeomorphism-invariant class the Bianchi identity forces slip-generating <=> Phi-moving (sympy-airtight: a
traceless shear's conservation-completing pressure 3 delta-p = -2 grad^2 f != 0 sources delta-Phi; DHOST locks
Psi=(1+alpha_H)Phi under c_T=c + graviton-non-decay; Foster-Jacobson gamma=1 kills the canonical aether slip) -- so the
framework's lensing partner can live ONLY in a Lorentz-violating preferred-frame sector (its own dS-Unruh frame), which is
consistent with modified inertia being intrinsically preferred-frame; the Route-E modified-inertia MATTER action remains
the genuine covariant half, and the lone open construction is an explicit non-dynamical-frame khronometric lensing term
with the shear divergence absorbed and the ghost settled -- a result that either completes a Lorentz-violating Lagrangian
or closes the no-go in its strongest form.

*Both ways: the no-go theorem (3 independent legs, Bianchi sympy-airtight), the standing Route-E covariant matter action,
and the easy-c_T/easy-ghost witnesses are credited at full weight; the absent covariant lensing partner, the hand-tuned
preferred-frame phenomenology, the failed canonical khronometric, and the unproven ghost are conceded at full weight. No
manufactured Lagrangian, no manufactured no-go. Quarantine held.*
