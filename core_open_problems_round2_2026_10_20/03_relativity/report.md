# Round 2: the physical de Sitter endpoint and all-angle static principal system

**Two previously open calculations are now resolved for the specific round-1 candidate:** its S1-linked de Sitter vacuum has a positive, future-bounded linear perturbation system, and its polarized static principal system can be reduced for every propagation angle. **The complete four-gate relativistic theory remains open.** These results neither supply S3's conserved cold mass nor establish nonlinear stability, a strong-coupling cutoff, low-frequency halo stability, or Solar System preferred-frame bounds.

Base: published commit `8aa3f7046a7ae14a99f3515fd42df5bf061fb1db`. Frozen inputs are the round-1 relativity report and independent review05. Because unrelated work changed the shared checkout, final input identities were pinned from `/private/tmp/core-open-publish.GPoQNP/`, not inferred from live HEAD. See `source_provenance.json`. Writes are confined to this round-2 directory. No sibling agent's new work was consulted. Raw candidate derivations were sent to the coordinator before final interpretation; the coordinator reports separate checks of the ADM scalar expansion and rank-one shift elimination. This packet's own review remains labelled self-review; coordinator integration evidence is separate.

## 1. Exact claim cards and status

**C2-DS — proved for the stated quadratic vacuum problem, subject to the action definition.** For the unchanged round-1 Hodge/clock action, K,beta,eta,gamma>0, a timelike clock, pure bare positive Lambda, and `a0²=Lambda/(32pi)`, the expanding unpolarized de Sitter solution exists with the beta-modified expansion rate below. Every fixed nonzero comoving Fourier mode has positive reduced kinetic coefficients and bounded future linear evolution. The exactly homogeneous sector is derived separately and has no negative physical quadratic kinetic direction. This is not a nonlinear stability theorem or a uniform constraint estimate as k approaches zero.

**C2-OB — proved for the stated frozen static principal system.** On regular static clock-aligned polarized backgrounds with finite `u<a0`, the full shift constraints yield the angular kinetic coefficient `eta/Delta`. A strict positive principal margin for every orientation and approaching the saturation cap is equivalent to `beta>2eta a0²/K`. This concerns the high-frequency continuum symbol, not low-frequency modes or arbitrary evolving backgrounds.

**C2-CUB — bounded partial result.** The direct cubic term of W has the amplitude-envelope bound in §5. The complete reduced cubic action and physical strong-coupling scale are not computed.

**Original four-gate claim — incomplete.** The smallest remaining stability implication is from these particular vacuum/static principal results to the full constrained system on actual polarized solutions at all wavelengths, including nonlinear constraint propagation. The S3 bridge and PPN calculations are separate indispensable obligations.

The complete derivation, with lapse and all shifts shown before elimination, is in `raw_derivation.md`. `checks.py` independently expands the geometric ADM expression and verifies the reductions using exact algebra; it does not import the round-1 script or a repository solver.

## 2. Physical endpoint: background first

The unchanged candidate, in unitary clock gauge, is

\[
\frac{L}{N\sqrt h}=\frac{{}^{(3)}R+K_{ij}K^{ij}-(1+\beta)\theta^2-2\Lambda}{4K}
+P^iD_i\log N-W_{\rm full}(u)+\frac\eta2E_iE^i
-\frac\gamma2(D_iP^i)^2-\frac\gamma4F_{ij}F^{ij},
\]

where `P0=N^iPi`, `Ei=(dot Pi−Lie_shift Pi)/N`, `Fij=partial_iPj−partial_jPi`, `u=K sqrt(h^ijPiPj)`, and

\[
W_{\rm full}=\frac{a_0^2}{K}[-u/a_0-\log(1-u/a_0)].
\]

The covector convention, K=4piG, c=1 and signature (-+++) are retained. Beta is dimensionless and `[eta]=[gamma]=[K] length²`. No coefficient or operator was changed to obtain this round's result.

For `Pi=0`, `Ni=0`, `hij=a²deltaij`, retaining the lapse gives

\[
L_{bg}=-\frac{3(2+3\beta)a\dot a^2}{4KN}-\frac{\Lambda Na^3}{2K}.
\]

Lapse and scale-factor variation give, at N=1,

\[
3(2+3\beta)H^2=2\Lambda,\qquad
(2+3\beta)(2\dot H+3H^2)=2\Lambda.
\]

Thus the expanding solution has

\[
H^2=\frac{2\Lambda}{3(2+3\beta)},\qquad \dot H=0.
\]

The expansion term contributes `rho_beta=−9beta H²/(4K)` and `p_beta=3beta(2Hdot+3H²)/(4K)`. Keeping Einstein gravity on the left, this is the clock's separately varied effective background stress. It cannot be dropped while retaining its perturbation effects. Its negative effective background density does not determine physical kinetic signs.

For pure bare-Lambda energy, `rho_DE=Lambda/(8piG)`. Enforcing S1 with the existing fitted kappa=1/2 gives

\[
a_0^2=\frac{\Lambda}{32\pi},\qquad
H^2=\frac{64\pi a_0^2}{3(2+3\beta)}.
\]

This is an actual finite-a0 expanding solution. The auxiliary fixed-a0 Minkowski calculation from round 1 is not used as its endpoint evidence. If rho_DE is instead defined to include additional clock or matter stress, the normalization must be reconsidered explicitly; that alternative is not hidden inside this calculation.

## 3. Complete quadratic endpoint reduction

Set `hij=a²e^(2zeta)deltaij`, `N=1+n`, `Pi=partial_i sigma`, and use spatial gauge to remove the second scalar metric potential. Let `p=k/a>0`, `Y=partial_iN^i`, and `A=2+3beta`. The scalar action before constraints is

\[
\frac{L^{(2)}}{a^3}=\frac{-3A(\dot\zeta-Hn)^2+2A(\dot\zeta-Hn)Y-\beta Y^2
+2p^2\zeta^2+4p^2n\zeta}{4K}
+p^2n\sigma+\frac{\eta p^2}2\dot\sigma^2
-\frac{Kp^2+\gamma p^4}2\sigma^2.
\]

All integrations by parts retain the a³ measure and `pdot=−Hp`. Eliminate Y, then n, then `Z=zeta/K+sigma`:

\[
Y=\frac A\beta(\dot\zeta-Hn),\quad
n=\frac{\dot\zeta}{H}-\frac{p^2Z}{CH^2},\quad
Z=-\frac{CKH}{p^2}(\dot\sigma+H\sigma),\qquad C=\frac A{K\beta}.
\]

Writing `B=CK²=K(2+3beta)/beta`, the result is

\[
S^{(2)}_{scalar}=\frac12\int a^3\left[(B+\eta p^2)\dot\sigma^2
-(\gamma p^4+2BH^2)\sigma^2\right]dt.
\]

This is a full finite-p vacuum reduction, not just a high-frequency approximation. In particular, de Sitter expansion gives the positive restoring term `2BH²`; the flat critical k⁴ cancellation alone would miss it.

For `Q=B+eta p²`, `V=gamma p⁴+2BH²`, the actual time-dependent equation is

\[
Q\ddot\sigma+H(3B+\eta p^2)\dot\sigma+V\sigma=0.
\]

The positive energy `E=(Q sigmadot²+V sigma²)/2` satisfies

\[
\dot E=-H(3B+2\eta p^2)\dot\sigma^2-2H\gamma p^4\sigma^2\le0.
\]

This establishes bounded future evolution for any finite initial time on the expanding branch. It is stronger than assigning an instantaneous frequency. The late-time scalar branches scale as p and p². Reconstruction gives decaying zeta on one branch and asymptotically constant zeta on the other; lapse and physical shift decay. The raw derivation supplies the first correction to each branch and checks that the inverse-p² constraint factor does not by itself generate a growing metric perturbation.

Transverse covector modes have

\[
S^{(2)}_{P_T}=\frac12\int a[\eta|\dot P_T|^2-(K+\gamma p^2)|P_T|^2]dt,
\]

and a positive decreasing oscillator energy. Physical components `qT=PT/a` obey
`qT_ddot+3H qT_dot+[2H²+(K+gamma p²)/eta]qT=0`. Tensors retain
`a³[hdot²−p²h²]/(16K)`, positive kinetic energy and speed c.

**Exactly k=0 is separate.** Its metric scalar action is
`−3Aa³(zetadot−Hn)²/(4K)`. The lapse enforces `zetadot−Hn=0`, leaving no propagating homogeneous metric scalar. Uniform covector components cannot be represented by the periodic gradient `partial_i sigma`; retaining them directly gives three equations
`Pi_ddot+H Pi_dot+(K/eta)Pi=0`, with positive kinetic and restoring terms. Homogeneous traceless metric perturbations have constant and decaying branches. This resolves the quadratic homogeneous sector while preserving the rank discontinuity between the k>0 longitudinal constraint map and exactly k=0. A global low-momentum constraint-domain estimate has not been proved.

## 4. Full oblique static principal reduction

For a regular static clock-aligned background, take the wavevector along z but keep arbitrary `P=(P_L,P_T1,P_T2)`. Write `q=delta P_L`, `r=delta P_T` and `y_i=ik delta N_i`. At leading high frequency the lapse gives `zeta=iKq/k+O(k^−2)`. Retaining **all three shifts**, the remaining principal action is

\[
L_{pr}=\frac\eta2[(\dot q-P\cdot y)^2+|\dot r|^2]
+\frac12y^TS_0y-\frac{\gamma k^2}2(q^2+|r|^2),\quad
S_0=\mathrm{diag}\left[-\frac\beta{2K},\frac1{4K},\frac1{4K}\right].
\]

The rank-one shift correction gives

\[
\Delta=1+\eta P^TS_0^{-1}P
=1-\frac{2K\eta}{\beta}P_L^2+4K\eta|P_T|^2,
\]
\[
y=\frac{\eta S_0^{-1}P}{\Delta}\dot q,\quad
L_{red,pr}=\frac\eta{2\Delta}\dot q^2+\frac\eta2|\dot r|^2
-\frac{\gamma k^2}2(q^2+|r|^2).
\]

Thus the longitudinal polarization has `omega²/k²=(gamma/eta)Delta`, while the two transverse polarizations have `gamma/eta`. At Delta=0 the shift matrix loses rank and compatibility imposes qdot=0; the reduced expression is not valid there. At Delta<0, both the longitudinal kinetic coefficient and omega² are negative.

For `u=K|P|`, `r0=2eta u²/(K beta)` and angle theta between P and k,

\[
\Delta=1-r_0+(1+2\beta)r_0\sin^2\theta.
\]

This proves the uniform angular margin criterion `beta>2eta a0²/K`. Equality permits positive coefficients at every finite `u<a0` but loses the limiting aligned margin at saturation. The round-1 inequality is therefore now an all-angle principal criterion for this static branch, not merely an aligned necessary test.

The largest non-tensor squared speed at fixed u is `(gamma/eta)(1+4eta u²/K)`. In particular eta=gamma gives a superluminal polarization speed for perpendicular propagation at nonzero u. This is distinct from the tensor c_GW=c gate; neither a complete causality theorem nor a whole-theory exclusion follows from this speed alone. An optional requirement that every such principal polarization be no faster than c would impose `gamma/eta+4gamma a0²/K<=1`, in addition to the kinetic margin. No such additional requirement is silently adopted.

These principal conclusions require fixed finite potential curvature, accessible high frequencies, and a regular static clock-aligned background. They do not apply without derivation to backgrounds with evolving P, nonzero electric background, singular foliation, or the order of limits in which `u→a0` precedes the high-frequency limit. The action itself has no finite-energy point at the cap.

## 5. Cubic normalization: a useful bound with limited meaning

The first nonlinear potential contribution is `K²|P|³/(3a0)`. On a linear scalar mode with `u_amp=Kp|sigma|` interpreted as its spatial maximum, the integrated direct-cubic/quadratic-restoring ratio obeys

\[
R_W\le\frac{2Kp^2u_{amp}}{3a_0(\gamma p^4+2BH^2)}
\le\frac{K u_{amp}}{3a_0H\sqrt{2B\gamma}}.
\]

The envelope peaks at `p⁴=2BH²/gamma`. For a single real sine mode, the actual integrated ratio is `8/(3pi)` times the first envelope because of its spatial cubic/quadratic averages. This corrects an initial draft that called the envelope an exact integrated ratio; no executable criterion changed.

The quadratic normalization is positive `sqrt(Q)` per proper-volume scalar mode, but constraint-generated and gravity/clock cubic vertices are not included in this potential-only bound. It identifies a classical small-amplitude regime for one interaction. It does **not** establish the full perturbative cutoff, and the Cartesian potential is C² rather than analytic to third order at P=0. These facts require a separate nonlinear analysis; they are neither a demonstrated instability nor a strong-coupling clearance.

## 6. Four gates and continuation

| Gate | New standing after this round |
|---|---|
| Lensing equals dynamics | Round-1 leading weak-static derivation retained; full moving/anisotropic solution not added |
| Tensor c_GW=c | Exact de Sitter quadratic tensor sector and round-1 regular static principal result retained; non-tensor speeds distinguished |
| Newtonian Solar System | No new PPN or boundary-matched Solar System test; gate remains open |
| Stability at every acceleration | S1-linked unpolarized de Sitter quadratic endpoint resolved, including separate homogeneous sector; full-angle static principal criterion derived; polarized low-frequency/nonlinear/evolving-background stability remains open |

The proposal still changes P's dynamical meaning relative to S3. It does not generate the conserved collisionless mass current, abundance, or formation mechanism. No data fit or experimental pass is inferred from the algebra.

The next bottleneck is now specific: construct an actual finite-stiffness polarized static solution and reduce its **finite-wavelength** coupled system with the angular principal margin imposed. A useful independent route is the Hamiltonian constraint/degree-count analysis on backgrounds with nonzero electric field, where the lapse structure can differ from both calculations here. The de Sitter cubic constraint-generated vertices are another open continuation required before claiming nonlinear endpoint health. PPN and an S3 current embedding must each use the same action, not an independently healthier surrogate.

## 7. Reproduction and evidence scope

Portable command, Python 3.9+ with SymPy:

```sh
python3 core_open_problems_round2_2026_10_20/03_relativity/checks.py --output /tmp/relativity-round2-results.json
```

`contract.json` states symbolic ranges and non-claims. `run_001/manifest.json` records the bounded execution, exact input hashes, software and outputs; validation checks it against this directory. `source_provenance.json` pins the immutable round-1 inputs. `handoff.json` contains output hashes and continuation obligations. No new external theorem is load-bearing: the new results are direct variations and matrix eliminations of the supplied action. The published source versions used for terminology in round 1 remain in that packet's provenance; no broader source theorem is borrowed here.

Primary mathematical interpretation is analytic and scoped as above. Executable identity checks support transcription and elimination correctness, not global physical completeness. The computation and report were self-reviewed, with the source-preserving boundaries and unresolved implications explicitly retained.
