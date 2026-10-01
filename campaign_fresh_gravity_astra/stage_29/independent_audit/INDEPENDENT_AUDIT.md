# Independent FGF042 audit

**Verdict: proved as written**, for the stated static zero-excess compactness theorem on a sufficiently short restriction of the fixed-reference Q crossing, and its separately conditional time corollary. This excludes energy-density and momentum/stress concentration in that zero-excess class. It neither constructs trajectories nor identifies general matter energy-transport flux.

## Independence and normalized claim

The claim quantifies over nonnegative fixed-mass finite-entropy matter, finite kinetic energy with j²/n=0 on n=j=0 and infinity on n=0,j!=0, H1_0 potential/scale perturbations, the scale quarter-cap, fixed positive physical coefficients, and all signed finite-action gradient increments. On a selected fixed interval satisfying alpha<=k/8 and beta2<=1/4, FULL relative total energy tending to zero implies strong unweighted L2 field-gradient and field-velocity convergence, background relative-entropy convergence, density/internal-energy L1 convergence, and strong L1 full energy-density and combined momentum/stress convergence. The reference equilibrium is fixed throughout a convergence sequence.

My independent derivation was frozen at 2026-09-30T23:35:20.150810+00:00, SHA256 7b7b39527363bbf110db05a72bb76b05e54598172fb4773ae847d056b8b83b5b, before any new author/root proof or formula preview. I notified both agents of that freeze, then received the author's readiness message and read its proof. The author and reviewer obtained the same half-remainder split independently. My increment bound is z² A(|z|/4,a)/16; the author's is z² A(|z|,a)/64, proved with a different good-set interval. Both are valid. I did not read the new root proof. Old stage28 root ancestry was hash-checked only. No computation or scan was executed; administrative source hashes and schema validation are not a mathematical run.

## Dependency graph and obligation matrix

The pinned Q action, actual central crossing and FGF038 finite-scale decomposition supply the signed constitutive definitions and equilibrium identities. Corrected FGF039 supplies exact normalized entropy elimination and its global variance bound. FGF041 is used only for the recorded packet/control comparison. The new implications are the retained-remainder lower bound, increment-sensitive estimate and elementary convergence arguments. No new external theorem or literature mechanism is used. Hash agreement verifies ancestry identity, not mathematical correctness; the relevant raw parent algebra was read separately.

| Obligation | Status | Reason |
|---|---|---|
| Exact full energy, mass and wall cancellation | Passed | Hydrostatic constant, signed source and scale equation eliminate only their actual linear variations. |
| Vacuum and normalized entropy | Passed | Equal mass, positive bounded tilted reference and 0log0 convention cover n=0. |
| Retained exact remainder and signs | Passed | Half of H stays intact; remaining half absorbs mixed scale terms with explicit Young constants. |
| Nonempty strengthened shortness gate | Passed | Same central solution has alpha=O(d^(3/2)), beta2=O(d^(7/2)); fixed couplings. |
| Uniform all-increment inequality | Passed | Good-set measure estimate works for arbitrary signed g,z and all capped scales. |
| Unweighted compactness | Passed | Physical-threshold split and ordered limits; no positive Hessian assumption at crossing. |
| Density, entropy, internal energy and kinetic convergence | Passed | Background conversion and nonnegative relative-entropy integrand checked separately. |
| Full momentum/stress and energy-density products | Passed | Strong L2 and L1 bounds control precisely listed components. |
| General matter energy transport and separate force | Not established | Explicitly excluded; an independent static velocity-concentration control confirms the distinction. |
| Uniform time statement | Conditional | Existing trajectories, fixed-reference energy inequality and H1 scale continuity are explicit hypotheses. |
| Nonlinear existence, finite nonzero energy compactness, physical completion | Out of scope | No transfer is accepted. |

## Retained full energy and nonempty gate

With z=psi', H=D_(a exp eta)(g,z), E_p=C^-1 integral A z² and E_eta=J C^-1 integral eta'², the exact full relative energy includes K, normalized entropy, minimized matter functional, finite field-scale remainder and scale derivative/potential remainder. Fixed mass cancels the hydrostatic first variation. Fixed potential walls and B'=C rho give integral(B psi'/C+rho psi)=0. The actual scale equation and fixed scale walls cancel integral[J chi' eta'+(U'-T)eta]/C. These identities remain valid across the central crossing without an internal boundary term. No Eulerian density perturbation is replaced by a finite displacement formula.

At fixed background gradient define qhat and Dhat over the entire scale quarter-cap. The exact split gives

    Frel >= H-qhat|eta z|-Dhat eta²/2
          >= H/2+(k/4)A z²-[qhat²/(k A)+Dhat/2]eta².

This follows from H/2>=k A z²/2 and Young with consumed coefficient k A/4. The quotient is zero-extended at the isolated crossing where qhat=Dhat=0. Using the exact density minimizer and Fmin>=-alpha E_p, and Urel>=S0 eta²/2, the strengthened gates give

    Erel >= K+cs²D(n|q_psi)+(1/(2C))integral H
                +(k/8)E_p+E_eta/4+(S0/(2C))integral eta².

Every term is nonnegative. Saturation of this inequality is not confused with zero excess energy: it is Erel=0 that forces the reference state. The same-solution shortness asymptotics are inherited with coefficients bounded on a positive compact scale interval; doubling the old qhat²/(2kA) coefficient changes only a finite constant. Restricting d makes both gates hold. Induced mass/walls may change as d is selected, and are fixed thereafter. No empirical radius or retuned coefficient is produced.

## Finite increments, exact constants and failure of quadratic coercivity

For the author's bound, the set |g+t z|<|z|/8 has t-length at most1/4. Within [0,1/2] at least1/4 of the interval remains; there 1-t>=1/2 and A(|g+t z|,b)>=A(|z|/8,b)>=A(|z|,b)/8. Thus

    H_b(g,z)>=z² A(|z|,b)/64

for every g,z and positive b, including sign reversal. For z=0 the result is immediate. My independently frozen argument instead excludes a set of length1/2 from [0,3/4] and obtains z² A(|z|/4,b)/16. Neither proof requires the segment to avoid zero everywhere.

Set a_*=exp(1/4)max a. For a physical threshold h=a_* r, the large-increment set has H>=z² A_r/64, A_r=2r/sqrt(1+4r²). Since integral H<=2C Erel,

    ||psi'||2² <= ell a_*² r²+128 C Erel/A_r.

For fixed r>0 take the zero-energy sequence limit, then let r decrease to zero. This proves unweighted L2 convergence with fixed physical units. Uniform positive quadratic coercivity is not inferred: H_a(0,z)/z² tends to zero cubically. The author's integrated control psi_r=a_* L r³ f(x/(L r²)) also checks: z=O(r), g=O(r) on its O(r²) support, so A along the entire segment is O(r), and integral H/integral z²=O(r). It is an admissible finite-action, fixed-wall control, preserving the failure rather than erasing the degeneracy.

## Matter, vacuum and every identified product

The lower bound gives eta' and both field velocities strong L2 convergence, eta uniform convergence, D(n|q_psi)->0 and integral j²/n->0. Potential fixed endpoints and the gradient conclusion give psi uniform convergence. Therefore log(q_psi/rho) tends uniformly to zero; normalization Z is essential. The entropy L1 bound gives n-q_psi->0 in L1, hence n->rho. The exact equal-mass relation

    D(n|rho)=D(n|q_psi)+integral n log(q_psi/rho)

then gives background entropy convergence, using fixed mass to bound the last term. This is valid at vacuum. Pointwise relative entropy h(n,rho) is nonnegative, and

    e(n)-e(rho)=cs² h(n,rho)+e'(rho)(n-rho).

Its first term has integral tending to zero and the second is L1-small because positive background rho has bounded logarithm. Internal energy therefore converges strongly L1, not merely in integrated signed value. The square-root density and weighted velocity conclusions follow directly. No pointwise density cap, no-vacuum condition, unweighted velocity or density-L2 convergence is claimed.

B is1-Lipschitz in signed gradient and has scale derivative bounded by a/2, so B converges strongly L2. The gradient-growth bound for W and |W_log a|=T<=a|G|/2 give W convergence in L1 despite arbitrarily large admissible increments. Cauchy-Schwarz then controls every listed field product. U converges uniformly. Matter interaction n Phi converges L1 by fixed mass, n->rho L1 and Phi uniform. Together with j²/n and internal energy, this verifies every component of total energy DENSITY and combined momentum density/stress. Field energy flux is also identified.

General matter energy flux additionally contains j³/(2n²) and j cs²log(n/rho_ref). Neither is controlled by these kinetic/entropy norms. The j Phi part alone is controlled, since j->0 L1 and Phi stays bounded; the author's exclusion is correctly understood as the cubic/enthalpy pieces and thus the full general flux. Separate n Phi_x is also not supplied by density-L1 and gradient-L2 alone.

My frozen derivation includes one independent static negative control for the cubic piece: hold n=rho and both fields at the background, and choose v_N=v0 N f(N³(x-x*)/L), f nonnegative smooth compact nonzero. This is finite energy with exact fixed mass/walls and zero scale perturbation. K=O(N^-1)->0, whereas after change of variables the cubic flux tends to rho(x*)v0³L integral f³/2 times delta_x*. Lower enthalpy/potential flux vanishes. This is a comparison-state control only, not an actual solution, weak-residual sequence or violation of the accepted density/stress theorem. No extra run or new primary task was executed.

## Conditional time result and exact surviving gap

From Erel>=E_eta/4 and ||eta||infinity²<=ell||eta'||2²/4, reaching the quarter-cap costs J/(16C ell). On already-existing trajectories with H1-continuous scale, initially strict cap and an assumed full fixed-reference energy inequality, a first cap exit is impossible below that energy. For Erel_m(0)->0 the barrier applies to all sufficiently large m. All static estimates are uniform for 0<=Erel_m(t)<=Erel_m(0), giving uniform-in-time spatial convergence on the assumed existing interval. This does not prove initial/wall traces, an energy inequality, existence, uniqueness or continuation. It does not apply automatically to an externally varying H reference with unaccounted work.

The FGF041 main packet retains positive full excess and therefore fails the changed hypothesis; its recorded small-amplitude control satisfies it. No old packet calculation was rerun. Vanishing energy about this static reference does not settle compactness at finite nonzero perturbation energy. The remaining smallest transport question is an explicit additional moment sufficient for the cubic and enthalpy energy flux; actual equation-residual admissibility and solution construction remain separate obligations.

The two registered a0 hypotheses, constant-vacuum/frozen-H/evolving-H distinctions, actual signed Q source and fixed physical inertias are preserved. This is an exact conditional diagnostic-model theorem, with no RAR/M, filtered-MONO, physical metric/photon/DOF, vacuum reservoir, empirical or theory-closure promotion.

## Provenance and verification

No author correction was required and no frozen bytes were replaced. An administrative Python check verified every declared input/artifact SHA256, matching input-map JSON, all required result-contract fields, all independently frozen source pins and frozen derivation bytes. Exact hashes appear in audit_result.json. Proof-only: no numerical script, scan, bounded runner, manifest or computationally tested range is claimed.
