# Independent coincident de Sitter scalar review

**Verdict: accepted for the on-shell n=3 vacuum, H>0 and finite nonzero comoving k, with all relative scalar variables retained. No blocking mathematical error found.** The reduced relative metric scalar has positive temporal kinetic coefficient and zero quadratic restoring term. Neither a full nonlinear scalar/clock health result nor a cold-fluid identity follows.

Final frozen inputs independently hashed:

- REPORT.md: `46a248a9296e5715809644173685d63d419b264b97ee632b4fa719264196870b`.
- checks.py: `9525f7aa5caa4080bd108f19f3bba52bab3cec3e0e254e0c6decd731b7d2fb92`.

I independently rebuilt the action from the Einstein ADM derivative block, the geometric-mean-volume correction and the positive projected invariant. I did not import author functions. The derivation below, rather than a check count or bare lapse rank, establishes the restricted verdict.

## Raw action reconstruction

Use c=Ka³>0 and P=k²/a²>0, with constant H and the on-shell relation a0²A=6H². The scalar shear variable is **e=Delta_coord(E_g−E_hat)**, not the un-Laplaced relative E. The shift convention N_i=partial_i beta gives the trace of the linear shear in the extrinsic curvature as e_dot+P beta. For one metric,

`delta K^i_j=(zeta_dot−Hnu) delta^i_j+partial^i partial_j E_dot−a^-2 partial^i partial_j beta`.

The quadratic trace combination KijKij−K² gives −6f²−4f(e_dot+P beta). The longitudinal rank-one shear square cancels against its trace square. The conformal spatial-curvature formula gives, after spatial integration by parts, +2P zeta²+4P nu zeta. Background terms and time boundaries cancel the individually matched cosmological potential on Lambda=3H². The individual Einstein-plus-own-Lambda scalar identity is therefore the reported expression. Using its separate spatial gauge identity is a way to reconstruct that Einstein block; it is not an unavailable gauge fixing of the interacting relative shear.

Splitting mean and relative fields divides this single-metric form by two for the relative block. The actual constant interaction differs from the two individual Lambda terms by

`2K Lambda(Vg+Vhat−2sqrt(Vg Vhat))`.

For Vg/a³=1+dg+..., the first variation is dg=nu_g+3zeta_g+Delta E_g. The difference above is K Lambda a³(dg−dh)²/2 at quadratic order. It supplies +3cH²D²/2, D=nu+3z+e. In particular the relative shear trace cannot be dropped from this volume term.

Finally the common clock cancels in the linear relative acceleration: delta A_i=partial_i(nu_g−nu_hat). The linear M(I)=I/2 term contributes +cPnu², and the eliminated cubic norm has zero Hessian at the zero-acceleration background. These ingredients reproduce the full raw relative Lagrangian

`L/c=−3f²−2f(e_dot+P beta)+Pz²+2Pnu z+3H²D²/2+Pnu²`,

with f=z_dot−Hnu. The mean sector is the ordinary constrained linear Einstein scalar sector; the shared clock's quadratic flat direction is a separate nonlinear question, not a demonstrated extra gauge of the full theory. All relative variables are invariant under the available common coordinate transformations at coincidence.

## Constraint and physical-sign reconstruction

The unconstrained (z,e) velocity Hessian is invertible. Momenta give Pe=−2cf and Pz=−6cf−2c(e_dot+P beta). Their Legendre transform yields the report's Hamiltonian. The primary Pnu=0 gives a secondary Cnu whose nu derivative is −c(2P+3H²)≠0. This pair is second class. Its elimination leaves the ordinary z,e canonical brackets, because brackets of those variables with the primary Pnu vanish.

After solving for nu define

`Dbar=[HPz/c+2P(2z+e)]/(2P+3H²)`.

The shift primary Pbeta=0 gives Pe=0. Preservation of Pe gives 3cH²Dbar=0. Preservation of Dbar, including c_dot=3Hc and P_dot=−2HP, gives a fourth constraint fixing beta, whose beta coefficient is −2P²/(2P+3H²). The bracket {Pe,Dbar}=−2P/(2P+3H²) is also nonzero. The four-member constraint matrix is nonsingular: its Pfaffian contains only the product of the Pbeta/fourth-constraint bracket and Pe/Dbar bracket, since Pbeta brackets with no other member. The multiplier is fixed on the final preservation step. Together with the lapse pair this gives six second-class constraints in eight relative phase coordinates, leaving one relative metric configuration degree. This is an actual quadratic Dirac chain, not a physical count inferred from bare lapse rank.

The direct Euler reduction independently gives f=0 from shift variation, D=0 from shear variation, and the reported beta from lapse variation. On Pe=Dbar=0, e=−2z−HPz/(2cP); the canonical one-form reduces to Pz dz and the Hamiltonian is

`Hraw=H²Pz²/(4cP)−HzPz`.

Subtracting the time boundary F=cPz²/H shifts Pz=Pi+2cPz/H. Its explicit derivative is F_t=cPz², which is essential. The final Hamiltonian is H²Pi²/(4cP), nonnegative with strictly positive momentum quadratic coefficient. Equivalently

`Lphys=cP z_dot²/H²`.

Because cP grows as exp(Ht), its exact equation is z_ddot+H z_dot=0. The two solutions are constant and exp(−Ht); there is no nonzero scalar sound speed or P-dependent restoring force. Positive kinetic here is not uniform static coercivity, a high-frequency wave theorem, or a complete nonlinear PDE well-posedness result.

## Exceptions and same-action reference

Neither the P=0 shift/shear reduction nor the H=0 lapse substitution used above is valid. In the flat branch the original shift equation instead forces z_dot=0. At k=0 the shear variable e=Delta E is itself absent, and the constraint chain changes.

The report's “separately reviewed positive homogeneous reduction” was clarified by the author/root to mean the new **projected_acceleration_homogeneous_2026_10_06/REPORT.md**, SHA256 `666790069c45c844ebdb2e966879a474f7a5e3888e631512f7d4720dde7c213b`. I read that action and confirmed it is the same zero-acceleration/geometric-mean-volume homogeneous restriction. It is not the older regular difference-connection plus J/S3 positive patch, whose pass cannot be transferred. The homogeneous calculation remains a separate rank branch and is not obtained as a uniform k→0 limit of this finite-k formula.

The physical limitations are retained: shared-clock quadratic absence, nonlinear/spatial constraints, sources, cubic gradient effects, zero restoring term, and possible EFT/domain issues still require analysis. The result supplies neither a conserved cold matter stress/population nor its abundance, primordial amplitude, lensing response, or an offset/32pi selector.

## Frozen evidence validation

I independently validated all four current b manifests against repository artifacts:

| Record | Checks | Intended result |
|---|---:|---|
| main_b |27/27|Pass|
| control_shear_b |27/28|Rejects erasing relative shear by unavailable gauge|
| control_wave_b |27/28|Rejects nonzero positive restoring term|
| control_flat_b |27/28|Rejects uniform reduced H→0 continuation|

Each control has exactly its declared failure. The initial development24/25 check is preserved as failed development output, not passed evidence. The author also preserved the first a report before correcting the Hamiltonian's strict-positivity wording to nonnegative; its pinned report inputs were superseded. The b runs are authoritative and independently validate against the final report. No author input was edited by this reviewer; this peer file is outside executable inputs.
