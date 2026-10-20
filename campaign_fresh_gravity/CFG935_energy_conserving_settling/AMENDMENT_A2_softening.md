# CFG935 AMENDMENT A2: softened N-type thin-shell kernels (implementation fix, POST-RESULT for R-d)

Date: 2026-10-20. Committed alone, after FROZEN_CRITERIA.md (38f4b6f18), A0 (e9a824153) and A1 (679994050), and before any
A2-code run. FROZEN_CRITERIA.md is not edited. **A2 is post-result for R-d:** the frozen-code R-d runs on IC-L and IC-I had
been seen (below). It is pre-result for every other N-type repair (R-a(i), R-b, R-c, none of which had been run).

## What failed

With the frozen N-type discretisation (thin shells, 1/r² kernels), the R-d run on IC-I (Rd_I) lost energy conservation in
bursts:
- ε_E = 2.2e-4 at t = 350, then 1.6e-3 at t = 400, 1.7e-3 at t = 500 and 4.0e-3 at t = 550;
- inside each burst the global step fell to about 1e-4 (242k steps in t = 350–400; 502k in t = 500–550).

Mechanism (diagnosed from the equations, not from extra runs): FIX-2's bath scales each bin's random velocities, including L,
towards σ_J. A shell whose L is scaled close to zero becomes radial. The thin-shell self-energy −Gμ²(k + ½)/r is singular
at r → 0 (a shell of finite mass collapsing on itself), so such a shell falls into a singular well that the leapfrog cannot
follow. R-a(i)'s λF kernel and the drift kernel carry the same 1/r² factor. K2 (IC-I, L = 0.05 r v_c, no bath) never met
this and passes.

## The fix

All N-type thin-shell 1/r² kernels are softened with ε = 0.02 (a shell of finite thickness):
- self-gravity V_cc = −Gμ² Σ(k + ½)/√(r² + ε²), force −Gμ(k + ½)μ r/(r² + ε²)^{3/2} (exact gradient; the pair energy depends
  only on the outer shell, so it stays continuous when shells cross);
- λF = (λG/2)∫_0^{R_C}[M_ph − m]²/(r² + ε²) dr, force −λGμ[M_ph − (k + ½)μ]/(r² + ε²) (exact gradient);
- drift v_s = −ατ G D/(r² + ε²), with D the frozen one- or two-sided deficit.

The baryons (Plummer, already smooth) and the S2 term (A1: its barrier keeps shells at r ≥ √(G(k + ½)μ/a₀) ≥ 0.02) are
unchanged. ε is 50× below the inner edge of the law gate (r = 1), and the law holds less than one shell (M_ph(<0.05) < μ)
inside 0.05.

## What had been seen before A2 (frozen code, kept on record as `parts/preA2_*.json`)

- **Rd_L (R-d, IC-L):** ε_E 6.2e-4; D(W2) = −0.151, dD −0.009, NOT ON THE LAW; m(<2, 5, 8) = 0.70, 2.86, 5.08 against the law's
  1.37, 4.41, 7.43; f_esc 0.002. The partner paid matter 14.3 energy units, almost all through the drift (outward/spin-up work
  −21.2 against +4.5 inward release; bath net +2.4 back to the partner).
- **Rd_I (R-d, IC-I):** m(<2, 5, 8) = 2.10, 4.99, 7.45 at t = 50 (the infall reaches about the law, overshooting at r = 2), then
  the same puffed state (0.60, 2.67, 4.81 at t = 350; 0.56, 2.37, 4.34 at t = 550), with the integrator bursts above. After the
  t = 550 burst the step fell to about 1e-5. This lane's own process was stopped by hand by PID at t ≈ 550–600, so it has no final
  analysis; its progress lines are kept in `parts/preA2_Rd_I.json`. No other process was touched.

Because A2 follows these numbers, the A2 R-d results are not blind with respect to them. Both are reported. A2 was motivated
by the energy bursts, which make (a) fail for a numerical reason, not by the gate. A post-hoc control part P0_L (pure N-type
Vlasov on IC-L, no settling, A2 code) is added to test whether the settled start is steady without any settling term. It
carries no verdict weight.

## Runs with the A2 code

K2 (rerun as the integrator check with ε), ETH, all N-type parts (Rd, Rb, Rc, Ra1, Ra1x100), the S2 parts (A1), MUTATE
(M1, M2 with A2; M3 with A1), P0_L, then the summary. K0 and PHYS do not depend on A1 or A2 and are rerun unchanged.
