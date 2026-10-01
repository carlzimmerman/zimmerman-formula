# Independent root-only audit: FGF043 local energy

Primary verdict: **correct only after a stated restriction**. The stationary counterexample, all residual calculations, local energy defect and spatial bounded-velocity estimate pass. The original general flux corollary needs a time-integrability hypothesis before concluding spacetime residual convergence. CORRECTION.md supplies that missing qualification and the corrected result passes.

## Exact claim and audit provenance

A time-independent sequence on the same Q background has initial and total relative energy tending to zero, exact global energy equality, and all the stated vanishing weak equation residuals, while its local energy residual converges to a nonzero spatial derivative of a delta measure. This refutes the specified approximation criterion, not exact-solution conservation. A separate uniform velocity bound, together with the proved zero-excess energy/entropy convergence, suffices for spatial strong L1 convergence of the complete energy flux. Its spacetime consequence additionally requires the corrected time-integrability conditions.

This was a root-only independent analytic audit under the proof-audit workflow. I read the root proof, record, task FGF043 and pinned old off-shell energy derivation. Other old record inputs were hash-checked; prior root/action audits supply disclosed inherited context. No new FGF043 author or other reviewer proof or preview was read. I identified the time-scope gap during the initial review and sent it to root before finalizing either audit file. Root preserved its original proof and wrote the attributed CORRECTION.md; I then independently checked its revised sufficient conditions. No pre-correction completed audit was overwritten. No numerical scan or other mathematical executable was used. Hashing and report serialization are provenance operations.

Principal pins:

- ROOT_DERIVATION.md: 45236fe01ee93bdcedbe785bcb2948d408b4ea05869aa81235095e2cfec2ca27
- PROOF_RECORD.json: 1b232c9b97c284dc0a640302fe8486316f4c22cbae0ebf5e88a0362a831b8197
- CORRECTION.md: cfa5cc3117ba7b42b3fafee936fec35f1353042c5d429986277a24e51fdafa74
- Task FGF-043.md: c1468fef3816a6d41c047609eb6d5817ca15116496e74a9087f77675c69fc33a
- Old off-shell ROOT_DERIVATION.md: c37b0c4831348da9676d6ab420dff375262f68da403b8275eef3925f265c50a5

Every input and artifact hash in PROOF_RECORD.json matched its actual file. Root's declared freeze timing is recorded rather than independently reconstructed from all messages. The original proof bytes remain unchanged.

## Dependency graph and obligation matrix

| Obligation | Status | Decisive evidence |
|---|---|---|
| Fixed Q background, action and walls | Conditional inherited input | Exact MOND source, hydrostatic constant and scale equation |
| Every conservative and primitive residual | Passed | Explicit differentiation and localized scaling |
| Claimed weak residual norms | Passed | L1 primitive bounds for Lipschitz tests; separate j L2 bound for H−1 |
| Initial/global full energy accounting | Passed | Static kinetic increment, all other terms unchanged |
| Local energy distribution and sign | Passed | Positive cubic-flux delta, derivative pairing with either sign |
| Initial and wall terms | Passed | Vanishing initial excess and zero wall flux; static time-boundary cancellation |
| Off-shell convention change | Passed | Rj=Rv+v Rc and the resulting negative kinetic coefficient |
| Amplitude control | Passed | Fixed amplitude, shrinking support gives all moments O(N^-3) |
| Spatial bounded-velocity full-flux estimate | Passed | Exact logarithmic entropy identity, no density cap |
| Original spatial-to-spacetime inference | Needs restriction | Pointwise-in-time convergence alone does not imply time-integrated convergence |
| Corrected spacetime corollary | Passed | Explicit L1 time condition, or uniform-in-time FGF042 hypotheses |
| Exact evolution or general compactness theorem | Out of scope | Neither follows from this example or the local admissibility exclusion |

The dependency chain is: inherited static equilibrium plus the prescribed current -> exact residual formulas; scaling -> small weak residuals and small global energy but nonzero cubic flux measure; the inherited full current -> local energy derivative and its signs. Separately, entropy and kinetic convergence plus bounded velocity -> the spatial full-flux estimate. Only after the correction's time hypotheses does that last branch imply spacetime residual convergence.

## Reconstructed decisive calculations

**All residuals and norms.** Since n=rho and both fields are static background, Rphi=Rchi=0 and field compatibilities are exact. Continuity is Rc=(rho v)_x. Hydrostatic balance cancels cs²rho_x+rho g0, leaving conservative momentum Rj=(rho v²)_x and primitive material-velocity residual Rv=rho v v_x. Direct expansion gives Rj=Rv+v Rc and Rv=(rho v²)_x/2-rho_x v²/2. The perturbation lies in a regular compact region, so rho and rho_x are bounded and rho is bounded away from zero there.

For v=v0 N f(N³(x-x*)/L), the change of variable gives ||j||1=O(N^-2), integral rho v²=O(N^-1) and ||j||2=O(N^-1/2). A derivative of an L1 function has fixed Lipschitz-test-dual norm at most its L1 norm. Hence Rc is O(N^-2) and Rj is O(N^-1) in that norm. The undifferentiated rho_x v² term in Rv is also O(N^-1), so the primitive residual has the stated rate. Rc is O(N^-1/2) in H−1 because j is that small in L2. No analogous H−1-smallness for Rj is inferred. These are uniformly-in-time estimates for the stationary sequence, not small pointwise or strong L1 derivative residuals. The combined momentum has P=j and Pi=Pi0+rho v²; Pi0 is constant distributionally, so its residual is the same Rj. Both coefficient differences converge in L1.

**Global and initial energy.** The only change in full energy density is rho v²/2. Density internal energy, n phi interaction, both field energies and field kinetic terms remain background. Thus E_N=integral rho v²/2 is exactly time-independent and tends to zero as N^-1. Initial energy is already of that order; weighted initial fluid velocity tends strongly to zero. This is an exact statement about the comparison functional, not a consequence of the equations, since continuity is not satisfied exactly. All current perturbations have compact interior support and all field traces remain fixed, giving zero wall mass and energy flux. There is no nonzero hidden initial energy measure of the kind in FGF041.

**Local energy and signs.** The full fluid energy flux is rho v(v²/2+e'(rho)+phi0). Since mu=e'(rho)+phi0 is spatially constant, this equals rho v³/2+mu j; both field fluxes vanish. The cubic term has measure limit Kdelta delta_x*, with

Kdelta=rho(x*) v0³ L integral f³/2>0.

The enthalpy/potential term mu j tends to zero in L1. Time-independence gives RE=partial_x Q. For compact smooth spacetime zeta, its limit pairing is exactly -Kdelta integral zeta_x(t,x*)dt. A nonnegative compact spatial bump can have either sign of derivative at x*, and a nonnegative time bump preserves that sign, so the limiting distribution is neither nonpositive nor nonnegative. In particular a local energy inequality RE<=0 with error tending to zero on each nonnegative compact test excludes this family, as does local equality. This argument does not turn such an inequality into a general compactness theorem.

At every finite N, the spatial integral of the residual is zero because Q vanishes at both walls. For tests reaching t=0 and vanishing at the final endpoint, integral H_N zeta_t plus its initial term cancels exactly because H_N is static. The remaining weak local term is the flux contribution, with the derivative sign just stated. Initial energy and momentum perturbation traces also tend to zero in L1. Thus neither a missing initial term nor wall influx supplies the defect. It is not net energy creation or failure of the limiting static background to solve its equations.

**Off-shell identity.** The pinned fixed-reference smooth identity uses the primitive residual:

RE=v Rv+(v²/2+e'(n)+phi)Rc+u Rphi/C+w Rchi/C.

Replacing Rv by Rj-v Rc gives the coefficient e'(n)+phi-v²/2 in front of Rc. On the selected states, expansion yields

v(rho v²)_x+(mu-v²/2)(rho v)_x
= (rho v³/2)_x+mu(rho v)_x.

The rho_x v³ coefficient is 1/2 and the rho v² v_x coefficient is 3/2, as required. No hydrostatic term remains. Each identity is applied before taking the limit to regular members on the perturbation support. Weak residual estimates against fixed tests do not control multiplication by the growing v or v²; this is the explicit failed implication. No undefined limiting distribution product is introduced.

**Amplitude control.** Dividing v_N by N keeps velocity amplitude fixed and support width N^-3. Its first, second and third weighted spatial moments are all O(N^-3). Every previous residual still vanishes, the energy remains exactly constant and small, and the complete flux L1 norm is O(N^-3). Its derivative therefore vanishes in the spatial Lipschitz-test dual, uniformly in time. This is a single control on the same action, walls, support location and density; it is not a scan.

**Bounded-velocity sufficient estimate.** For general zero-excess states on the fixed gated background, set h=n log(n/rho)-n+rho. The exact identity n log(n/rho)=h+n-rho and h>=0 imply n|log(n/rho)|<=h+|n-rho|, including n=0 by the stated convention. Decompose e'(n)+phi=cs²log(n/rho)+mu+psi. With |v|<=V on n>0 and j=0 on vacuum,

||Qmatter||1 <= V Kfluid
 +V cs²[D(n||rho)+||n-rho||1]
 +(abs(mu)+||psi||infinity)sqrt(2M Kfluid).

The cubic part uses n|v|³/2<=V n v²/2, the entropy part uses the pointwise identity, and the final term uses ||j||1<=sqrt(2M Kfluid). All constants and factors are correct. No current-density upper/lower bound or log-squared moment is needed. Vacuum products extend by zero; the bounded positive background only fixes the logarithm and hydrostatic constant. The FGF042 spatial convergence makes every term vanish. The field flux converges in L1 by its already established strong L2 factors. This gives the complete spatial flux conclusion under the extra velocity bound, which is neither derived from energy nor declared a physical speed cutoff.

## Scope correction and corrected time consequence

The paragraph after (2) originally moved from spatial L1 convergence to convergence of compact spacetime local-energy residuals without explicitly supplying integration-in-time control. Pointwise-in-time convergence alone is insufficient: nonnegative functions of time can have shrinking supports, fixed integrals and pointwise limit zero. One cannot silently exchange the time limit and integral.

I identified this scope gap before finalizing this audit. CORRECTION.md attributes that cue and retains the original bytes. Its corrected condition is sufficient: require the right side of (2) to tend to zero in L1(0,T), and full energy density and field flux to converge in spacetime L1. Then the spatial estimate integrates to complete spacetime L1 flux convergence. Against each compact smooth test, both density and flux derivative residual pairings tend to those of the background by the supremum bounds on test derivatives. As a concrete sufficient case, FGF042's uniform-in-time vanishing full-energy setup on a fixed finite slab, with the same uniform velocity cap, supplies all these bounds uniformly and hence in time-integrated L1. No pointwise-in-time-only reading is accepted. The stationary counterexample and control require no alteration because all their estimates were uniform in time from the outset.

## Units, limits and remaining gap

N and f are dimensionless, L is a length and v0,V are speeds. Kdelta has the units of spatially integrated energy flux. Each term of (2) has the same units: velocity times integrated kinetic energy, velocity times cs² times mass-per-area entropy/density difference, or potential times integrated current. The off-shell factors have the expected local energy-rate units. Signed Q source/inertia and both a0 backgrounds remain intact; fixed-vacuum, frozen-H and evolving-H histories are distinct. The unbounded-velocity mathematical family is not a physical superluminal prediction or a relativistic matter model.

The corrected result identifies one necessary local-admissibility test for these approximants and one sufficient full-flux condition in the zero-excess class. It does not construct nonlinear trajectories, propagate a velocity bound, infer arbitrary-state strong compactness from local balance, supply initial/wall traces in general, or produce a physical metric, reservoir, calibrated prediction, novelty claim or theory closure. An energy-consistent approximation/evolution with justified local flux regularity remains the next missing implication.
