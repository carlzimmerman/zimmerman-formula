# CDE-L4C Dirac preservation gate — VERDICT: the lambda-steal trap is EVADED; full rank OWED (2026-09-01)

**The decisive worry (the sf61 trap): does preservation of the primary lapse momentum p_N GENERATE the MOND
lapse equation, or does the no-slip multiplier lambda_s STEAL it because {p_N, C_slip} != 0? Answer at the
principal-symbol level: MOND is NOT stolen -- it survives as an independent equation. The candidate passes
this gate. The full N_grav=2 Dirac rank is NOT-COMPUTED here (owed covariant closure).**

Script: `cde_cmc_mond_dirac_preservation.py` (per-mode Poisson-bracket preservation chain, no pre-decided
classification, mutation control passes). Kernel frozen: F_M(y)=2[(1+y)e^{-y}-1], F_M'=-2y e^{-y},
1+F_M'/2y=mu=1-e^{-y}. Constraints {C_N=p_N, C_K=K-K0(t), C_slip=3R-4D^2 lnN}; C_MOND NOT inserted.

## The preservation chain (COMPUTED, principal per-mode; kk=k^2, Lpar=1+(y-1)e^{-y}>0)
| preservation eq | result | classification |
|---|---|---|
| {p_lam, H_T} = 0 | dplam = kk*C_slip | **NEW CONSTRAINT**: generates C_slip=0 (secondary), i.e. Phi=Psi for kk!=0 |
| {C_K, H_T} = 0   | -B_p kk(1+Phi) - c_s kk^2 lambda = 0 | **FIXES MULTIPLIER**: solves for lambda_s (contains lambda via {K,3R}~c_s kk^2) |
| {p_N, H_T} = 0   | -B_p Psi kk - Lpar a0^2 kk Phi(...) + c_s kk^2 lambda - pPsi - rho_b = 0 | after lambda-fix: **INDEPENDENT MOND EQUATION** |

## THE CRUX (SOLID at principal level): MOND is NOT stolen
- {p_N, C_slip} = -c_s kk != 0 (the danger is real: N appears in C_slip).
- {C_K, C_slip} = +c_s kk != 0 (the RESCUE channel: K vs 3R).
- **Preservation of C_K fixes lambda_s FIRST** (via the {K,3R} bracket), so preservation of p_N is then read as
  an INDEPENDENT equation. After substituting lambda_s(fixed by C_K), dot p_N=0 is NON-TRIVIAL, CONTAINS the
  MOND operator Lpar*kk*Phi, and RETAINS the baryon source rho_b. So the no-slip multiplier does NOT steal
  the lapse equation. **This is the exact failure mode that killed sf61, and CDE-L4C evades it.**
- Mutation control: an N-INDEPENDENT slip constraint gives {p_N,C_slip}=0 and no lambda in dot p_N -- the test
  discriminates (the survival is due to the specific N-dependence + the C_K rescue channel, not an artifact).

## What is NOT settled (NOT-COMPUTED, owed -- do not overclaim)
- **Full N_grav=2 Dirac rank.** The naive per-mode 4-set {p_N,C_K,C_slip,p_lam} has rank 2 (p_lam is first-class
  in this crude basis; the 3x3 block over {p_N,C_K,C_slip} has rank 2 -- the steal-vs-survive channel). The per-
  mode reduction does NOT capture the full secondary-constraint chain or the momentum-constraint sector, so the
  rank/DOF count is NOT settled here. It is the owed COVARIANT Dirac closure (functional brackets, all k, shift sector).
- Matter nabla_mu T^munu=0 (Bianchi) not verified in this model.
- **PPN alpha_1, alpha_2, alpha_3** -- the predicted killer. CDE-L4C is a preferred-foliation theory; the
  York/DC-019 wall says an instantaneous constraint sourcing MOND gives alpha_3=O(1). The Laplacian trick keeps
  FLRW free but the k!=0 constraint is still instantaneous. This gate does NOT address PPN.

## Status
CDE-L4C SURVIVES the Dirac-preservation crux that killed sf61 -- the first preferred-foliation MOND construction
to do so. Verdict: ALIVE, not yet certified. Next: (1) the full covariant Dirac rank (N_grav=2), then (2) PPN
(alpha_1,2,3). If the full rank holds and PPN gives alpha_3=O(1), the horse dies at PPN as predicted; if alpha_3
is somehow protected, this is a genuine strict-2-DOF MOND completion.
