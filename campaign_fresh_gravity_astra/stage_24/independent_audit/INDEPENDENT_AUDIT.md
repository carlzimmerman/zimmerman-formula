# Independent audit of FGF037

**Primary verdict: proved as written.** The worker's counterexamples validly refute promotion of weighted linear control to a finite/continuous nonlinear Q energy neighborhood or a uniform quadratic Taylor bound in that topology. This verdict concerns the stated counterexample, not a refutation of the core framework or of all possible nonlinear evolutions.

The normalized claim fixes one reviewed Q crossing, its finite interval, positive density, bounded positive scale and induced walls/mass. On the phi-only slice, the completed weighted space includes directions whose exact energy is infinite at every nonzero amplitude. Even its smooth finite-energy subset has a sequence tending to zero in the weighted norm while exact energy diverges. The earlier closed linear form/operator/evolution theorem survives on its stated spaces.

## Independence and evidence record

The auditor froze FROZEN_ENERGY_DERIVATION.md at 2026-09-30T18:35:13.119850+00:00, SHA256 c72af1656dacb5865a47e04382cbd38967481de2b1dd8616ad1fd1175613ca5b, before any new author/root proof or formula preview. The frozen audit independently chose beta=1/2; the author chose beta=3/8. Author source and metadata were read only after the freeze; the new stage24 root proof was never read. No author correction was requested. The strong-H1 continuity statement was checked after reading the author; it is not presented as part of the pre-read independent freeze.

This is a mathbox proof audit with no numerical, symbolic, ODE or spectral run. Python was used only for file hashing, JSON verification and report writing. No computation manifest or enforced numerical resource bounds are claimed. All 10 worker input hashes, all 3 worker artifact hashes, the 5 independent source pins, frozen-proof identity and required result-contract fields were checked. Ancestor hash matching is provenance verification, not a claim to freshly re-audit every historical proof.

## Dependency graph and obligation matrix

The internal chain is: inherited exact Q action and signed equilibrium -> global growth inequalities -> exact finite-energy classification and finite linear cancellation -> one singular weighted direction -> one smooth concentration family -> failed weighted continuity/Taylor control. The action, crossing and completed domain are pinned prior results; the remaining implications are proved by elementary inequalities, a change of variables and integration by parts. No external-source or computation leaf is required.

| Obligation | Status | Decisive evidence |
|---|---|---|
| Exact large-gradient growth | Passed | Direct square-root bounds, valid also at small gradients |
| Finite-energy domain classification | Passed | W bounded above and below by quadratic expressions with integrable constants |
| Signed source and full matter term | Passed | B'=C rho cancels int rho psi against int B psi'/C |
| Singular direction admissibility | Passed | Smooth transformed-coordinate profile, globally AC, zero outer traces, finite weighted norm |
| Infinite energy at nonzero amplitude | Passed | Its physical derivative is not L2; interaction and subtractions are finite |
| Author beta=3/8 family | Passed | Weighted squared norm scales as delta^(1/4), exact increment as delta^(-1/4) |
| Independent beta=1/2 control | Passed | Weighted norm vanishes but exact increment has a strictly positive finite limit |
| Taylor factor and error estimates | Passed | Quadratic energy is Q/2; the normalized remainder diverges in both controls |
| Strong-H1 continuity on fixed slice | Passed | Exact W difference controlled by an L2 gradient product |
| Nonlinear instability or field-theory transfer | Out of scope | No time mode, nonlinear Cauchy theorem, metric or observational evidence |

## Exact constitutive growth and energy accounting

For s>=0, 2s<=sqrt(a²+4s²)<=2s+a gives

    s-a/2 <= b(s,a) <= s,
    s²/2-a s/2 <= W(s,a) <= s²/2,
    W(s,a) >= s²/4-a²/4.

The last inequality follows because the difference of the two lower expressions is (s-a)²/4. W is separately nonnegative. On the finite interval with a bounded above, s²<=4W+a_max² and W<=s²/2 establish int W(|G|,a)<infinity iff G belongs to L2. This is the exact high-gradient Q energy; extrapolating the small-gradient cubic law to this question would be wrong.

Let F_x(z)=W(|z|,a(x)). Its signed derivative at the background is B=sgn(g)b(|g|,a), and F_x''(z)>=0. At fixed rho and chi the complete static energy change is

    int rho psi + (1/C)int[F_x(g+psi')-F_x(g)].

Every weighted-domain psi is bounded and globally AC with derivative in L1. Since B is C1 and psi has zero outer traces, all linear terms are finite and int B psi'=-C int rho psi. Thus the complete increment is the integral of the convex remainder F_x(g+psi')-F_x(g)-B psi', divided by C. This is valid as an extended nonnegative value also when the nonlinear term is infinite, because the background and subtractions are finite. The field source is B', never g'. Fluid internal and scale terms are unchanged; no omitted matter term or infinity-minus-infinity cancellation supplies the conclusion.

The perturbations are admissible configurations for the energy functional with its fixed wall and mass constraints. They are not claimed to be new hydrostatic solutions; requiring every variation to satisfy the equilibrium equations would change the variational test.

## Singular direction

In the finite reciprocal-A coordinate s(x)=int_left^x 1/A, choose smooth compactly supported v with nonzero constant v_s near the center. The pullback psi=v(s(x)) is a genuine V_A member with one continuous center value and zero outer traces. Its derivative is v_s/A, hence comparable to |x|^(-1/2). The weighted energy integral is finite, while its unweighted squared derivative has logarithmic divergence. This is a full form-domain triple (0,psi,0); no claim that the phi-only triple is in the stronger operator domain is needed.

For every epsilon not zero, g+epsilon psi' cannot be in L2: otherwise subtraction of the background L2 gradient would make psi' L2. Exact field energy is therefore infinite. The bounded potential keeps the matter interaction finite, and B psi' is integrable (near the center it is of order sqrt(|x|)). The weighted norm of epsilon psi nevertheless tends to zero. This proves that every weighted ball includes configurations of infinite exact energy. It does not imply a finite nonlinear directional derivative along that singular direction: the quadratic form is a closed extension of the linearized form, not a finite-valued nonlinear variation on every completed direction.

## Author's smooth family and independent control

The worker's fixed bump exp[-1/(1-y²)] on |y|<1, zero outside, is smooth, compact, nonconstant and has positive derivative-squared integral J0. At beta=3/8,

    psi_delta=Psi_ref delta^(3/8) f(x/(L_ref delta)),
    p_delta=(Psi_ref/L_ref)delta^(-5/8) f'(x/(L_ref delta)).

Direct substitution x=L_ref delta y gives exactly int p_delta²=(Psi_ref²/L_ref)J0 delta^(-1/4). The weighted integral is asymptotic to (a_A Psi_ref²/sqrt(L_ref))JA delta^(1/4), where JA=int sqrt(|y|)f'²>0. The potential L2 term is proportional to delta^(7/4), hence subleading. The uniform local bound for A(x)/sqrt(|x|) justifies the rescaled coefficient limit, including the single point y=0. The physical gradient L2 norm grows as delta^(-1/8), while its supremum grows as delta^(-5/8); the potential itself converges uniformly to zero.

Using the global estimate |W(s,a)-s²/2|<=a_max s/2, all errors in the exact increment are integrable and controlled, even where f' vanishes. The author exponents check independently:

| Integrated term | Order for beta=3/8 |
|---|---|
| int abs(p_delta) | delta^(3/8) |
| int abs(g p_delta) | delta^(7/8) |
| int abs(B p_delta) | delta^(11/8) |
| int g² on the support | delta² |
| int W(|g|,a) on the support | delta^(5/2) |

The integrated constitutive approximation error is O(delta^(3/8))+O(delta^(3/2)); every error tends to zero. The positive leading gradient-square term grows as delta^(-1/4). Therefore the author's exact full increment is asymptotic to Psi_ref² J0 delta^(-1/4)/(2 C L_ref). Its quadratic energy is Q/2, of order delta^(1/4), and the remainder divided by the squared weighted norm diverges as delta^(-1/2). Each smooth member has finite energy, preserves the outer walls and keeps density, mass and scale exactly unchanged.

Independently, before seeing the author exponent, the auditor fixed beta=1/2 and any fixed nonzero smooth compact f. Then int psi_delta'²=(Psi_ref²/L_ref)int f'² is constant, int A psi_delta'² is proportional to sqrt(delta), and int psi_delta² is proportional to delta². The same exact growth inequalities give

    E(phi+psi_delta)-E(phi)
        -> Psi_ref² int f'²/(2 C L_ref) > 0.

All constitutive and background errors vanish: int |psi_delta'|=O(sqrt(delta)), int |g psi_delta'|=O(delta), and the integrated signed linear term is O(delta^(3/2)). This separately disproves continuity, even without using a divergent energy sequence. Its squared weighted norm tends to zero as sqrt(delta), and its remainder after Q/2 has the same positive limit. These are two separately chosen analytical controls, not a numerical or exponent scan.

## Interpretation and surviving theorem

Continuity already fails on smooth finite-energy configurations with the weighted relative topology. Hence there can be no bounded local quadratic upper control, no uniform O(norm²) Taylor remainder, and no o(norm²) Frechet second-order expansion in that topology. The result is compatible with ordinary second variations along each fixed smooth bounded-gradient direction: uniformity over concentrating directions is the failed implication. Both families have nonnegative exact energy increments on this fixed-rho/chi slice; they provide no negative-energy instability or growing mode.

For this slice, g is L2 and every weighted perturbation is bounded, so exact field energy is finite precisely on ordinary H1_0 perturbations. The author's additional strong-H1 continuity assertion is correct: |F_x(G1)-F_x(G2)| <= (|G1|+|G2|)|G1-G2|, with its integral bounded by Cauchy-Schwarz, while the fixed-density interaction is continuous in L2. This is neither a full coupled nonlinear-domain characterization nor proof of twice-Frechet differentiability or nonlinear well-posedness.

FGF036's positive closed weighted quadratic form, actual transmission operator, compact inverse and conserved linear energy evolution remain valid in their stated domains. The present counterexample closes only the attempted implication from that theorem to nonlinear energy control in its completed topology. It does not rule out stronger nonlinear domains. Repeating weighted positivity or scanning more exponents cannot remove the accepted obstruction.

Psi_ref and L_ref retain their physical potential and length units while delta is dimensionless. Energy increments are per transverse area; a_A has inverse-square-root-length units. Both positive a_ref choices remain separate hypotheses and the bounded local a is held fixed during each test. Constant-vacuum, frozen-H and actual evolving-H branches remain distinct; responsive local scale and the physical reservoir obligation are unchanged. Q alone is tested. No RAR/M transfer, fitted V, filtered-MONO result, metric/photon/DOF, calibration or theory closure follows.

There is no load-bearing gap in the scoped counterexample. The cheapest further action is to record this implication as closed by counterexample. Further nonlinear work requires a separately justified target and stronger domain before proving any differentiability or evolution theorem; no new task or run was created by this review.

## Exact pins

- `campaign_fresh_gravity_astra/stage_23/independent_audit/INDEPENDENT_AUDIT.md`: `71ed1fb888826970c03f3494731ae94becf1a0ebc3310fc647522df1cbd6a19e`
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/ROOT_DERIVATION.md`: `1ad5e82feb6a57aebd7a30df7ce0b6fb3be0a42e01ea14a084371aff578e2dc0`
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/audit_result.json`: `fa69589f5bf89d9ffd10faf5e15f35b6dab691d8b7e34f84a1da585d114e6075`
- `campaign_fresh_gravity_astra/stage_24/independent_audit/DERIVATION_FROZEN.json`: `a8259762ff6bc22f59fcb7ae80c33aefcbcfa4ac233719b83915e9a05da41acf`
- `campaign_fresh_gravity_astra/stage_24/independent_audit/FROZEN_ENERGY_DERIVATION.md`: `c72af1656dacb5865a47e04382cbd38967481de2b1dd8616ad1fd1175613ca5b`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/FRAMEWORK_AND_EXECUTION.md`: `ff0d2873065578b0bd8aa50907e0a39495ff8da775bf2b4890768d83775fd750`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json`: `ba388d0ca8e447a38649a478483e3ff4c2d3293e842eedc8f035499c77a20c29`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-023/fgf023_run_001/DERIVATION.md`: `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-035/fgf035_run_001/DERIVATION.md`: `5aa9e64b81a9dcaac14926f43c680a82d44d57be838423ccc4b0ebeee1cb1d3b`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/DERIVATION.md`: `71727e56c1c7d88bd2d24988af4683339b5fdc4db6f9ca54d9c800752a747f1a`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/result.json`: `d238f3db45e4aacbce15487c89c1c66f7131915cba7a1c6e5043179b0e30c515`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-037/fgf037_run_001/DERIVATION.md`: `07a7a0d4e22c18c8963d4264dc61b69de035c99acd09624f8a54966d8822ce38`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-037/fgf037_run_001/REPORT.md`: `f7f1fe8958f06030fe0052a8419f17bf26c1254fe8b2ce81c5323d2947e276fd`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-037/fgf037_run_001/input_sha256.json`: `976e140d9d12e235c7931183311cbb74f608e588053fb9ca35cabcb89578cf75`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-037/fgf037_run_001/result.json`: `12b386bc172121cb21379a67fa57f6ccad18d97b051f7c049c3d40e9ec34863e`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-036_RECONCILIATION.md`: `2ce6b03d38f4d5f7bb63da3a718c87b04e8bd46143c4e3c5da49045e06b259c5`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-037.md`: `2653a38bbfb66c710ff2ec47c22c8992543063ce80fcf871478f503873f005ad`
