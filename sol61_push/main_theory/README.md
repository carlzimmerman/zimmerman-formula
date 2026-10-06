# Main theory: resumed audit and closure obligations

Assessment date: 2026-10-05, checkpoint SOL61-RESUME-2026-10-05-A.
Base: `0893bc5cdef187ffb10ccb5b539cb469443d57f0`.
Previous Sol61 stop: `d1e19d49ee932195035ab9b973e095ea463b4e91`.
**Verdict: incomplete, with no single demonstrated action producing candidate B.**
This is a targeted self-review of Claude-associated repository work, not an
independent-agent review or an exhaustive audit of the whole repository.
See [scope](../RESUME_SCOPE_2026-10-05.json) and [joint closure order](../CLOSURE_ROADMAP_2026-10-05.md).

## What changed since the stop

| Front | Current evidence | What it earns; what remains |
|---|---|---|
| Conserved, filtered chassis | CFG329, G9/G0 | Explicit reduced-sector Noether and structural checks; general nonlinear elliptic solvability remains conditional. These results do not construct B's gate. |
| Nonlinear zero-field evolution | CFG325/328 and verification addenda | Finite-grid Lyapunov growth levels off; the recorded frozen verdict is OPEN. This weakens the earlier numerical discontinuity diagnosis, not the independent excessive linear-growth result. |
| Linear cosmology | AUDIT_SIGMA8, CFG324 | Ungated chassis fails; B recovers standard growth under its stipulated bound-only rule. The rule still needs a conserved action and its new stresses. |
| Ultra-faint dwarfs | CFG338/339/340, then CFG343/344/345 | The earlier retention candidate broke large systems and was withdrawn. Post-reionisation accretion can fix dwarfs in a narrow assumed formation/infall window, conditional on cold small-scale power and formation history. |
| Ellipticals | CFG323, CFG330/331 | Overall significance weakens with measured tracers, but group/cluster centrals retain a discrepancy. Tested contamination/environment adjustments do not remove it. |
| Lensing/environment | CFG315/316 | Non-isolated lensing includes environment; spectroscopic isolation has inadequate power. Neither closes the early/late isolated-lens question. |
| Ownership across populations | CFG332/333 | Formation classes help several populations; the required class and cold-mass rules are still not one dynamically derived ownership law. |
| Switch | CFG337/346/347 | A stable smeared switch loses dwarf MOND response; expansion-triggered alternatives fail reach, flicker or gas fidelity. All the quoted no-gos are class-specific. |
| Strong field | CFG318/319 | Exterior observables survive restricted tests; moving-hole regularity and sensitivity remain conditional. The singular solution cannot silently be promoted to a fully regular one. |
| Radiative stability | CFG320 | EFT estimates survive at a specified cutoff; UV Lorentz-violation transfer is conditional. No complete UV construction. |

Inputs are under `campaign_fresh_gravity/`; the September 29 standing has later
appendices. The October 3 recipe audit's NOT RUN entries for G0/G9/G12 and
running CFG319 are historical: CFG329/320/319 now supply results. Conversely,
a new PASS for a chassis subsystem cannot be transferred to the assembled
bound-only action. Formal certificates prove their encoded premises and
inequalities, not source applicability, statistical adequacy or action closure.

## New audit: FRW-off does not mean the switch has no stress

CFG347 proposes a propagating field with constants Z>0, M²>0 and C,

    L_sigma = -Z (d sigma)^2/2 - Z M² sigma²/2 + C sigma div(u_b),

and multiplies the MOND term by f(sigma). Its FRW test puts f=0 in a finite
neighbourhood and feeds that multiplier to the existing growth harness.
It does not derive the new field's homogeneous stress or perturbations.

On comoving FRW, u_b is the unit normal, theta_b=3 adot/(a N). For the stated
local action and c=1, the homogeneous action per coordinate volume is

    L = a³[Z sigma_dot²/(2N) - N Z M² sigma²/2] + 3 C a² adot sigma.

Direct lapse and scale-factor variation gives

    rho_sigma = Z (sigma_dot² + M² sigma²)/2,
    p_sigma   = Z (sigma_dot² - M² sigma²)/2 - C sigma_dot,
    Z(sigma_ddot + 3H sigma_dot + M² sigma) = 3 C H.

Indeed rho_dot+3H(rho+p) equals sigma_dot times the scalar equation's residual.
For constant H, the particular solution sigma=3 C H/(Z M²) has

    rho_sigma = 9 C² H²/(2 Z M²) > 0   if C != 0.

Thus f=0 does not make the action GR with unchanged matter and dark energy.
With a conventional Einstein term 3 M_Pl² H², this particular de Sitter branch
replaces its coefficient by 3[M_Pl² - 3 C²/(2 Z M²)]. This is a homogeneous
reduction, not a full perturbation or instability theorem. The chassis's own
background terms, calibration and comoving matter variation must be included
before any observed G or growth conclusion.

At CFG347's **costed universal point only**, ZM²=B_edge and C=B_edge/theta_on,
theta_on=a0/c. Restoring SI units, the frozen-H ratio of that particular
solution's energy to 3H²c²/(8pi G) is

    12 pi G B_edge / a0² = 0.1190 (canonical), 0.0820 (alt).

These are about 12% and 8%, not zero. They are not a likelihood or a revised
cosmological G measurement, and they do not apply to the zero-constant route's
unspecified Z. A compensation could exist, but it must be varied and tested;
renormalizing a bare parameter by declaration does not recover perturbations.
**Audit verdict:** the trigger-only FRW/growth check is insufficient for the
new action. This does not reverse its already failed bound-system test.

## New audit: the transition theorem has an omitted hypothesis

The verified trigger-sector dispersion is

    (A-w)(b-w)=G w,
    A=c_s² k²-Gamma_g², b=c_sigma² k²+M², G=C² k²/(rho_b Z).

Its positive-root and Jeans-growth bounds require b>0. Restoring B f(sigma)
adds a diagonal quadratic term B f'' delta_sigma²/2, hence

    b_eff = b - B f''/Z,

and the perturbation of B also contributes f' delta_B delta_sigma. These are
absent from the trigger-only determinant. If A>0 and b_eff<0 the root product
A b_eff is negative, so this reduced completion already has a growing root.
An exact example A=b=Z=1, B=2, f''=1 demonstrates the failure of extending the
positive-root theorem without checking b_eff. This is an algebraic counterexample
to that inference, not a constructed physical host or a global no-go.

The frozen criteria explicitly defer f' B mixing when the bound tests fail.
Accordingly, CFG347's transition PASS is usable for the tested trigger subsystem;
full gate-on transition health is **not addressed**, rather than established.
Criterion B already permits its superluminal characteristics relative to the
preferred foliation; that is recorded in the raw code and is not a new failure.

For A>0, b>=A and G>=0, the lower root w decreases from A as G increases.
The exact necessary and sufficient 10% fidelity boundary for that root is

    G <= b/9 - A/10.

Derivation: set w=(1-d)A in the dispersion to obtain
G=d[b-(1-d)A]/(1-d), then d=1/10. The recorded b/9+A/10 is a valid, weaker
necessary bound that covers either mode; it is not a sign error. The huge
recorded violations already reject the tested costed point without this
refinement. The lower-root restriction matters near exchanged mode identities.

## Source audit of the conditional dwarf repair

[Correa et al., arXiv:1409.5228v2](https://arxiv.org/pdf/1409.5228v2), checked
2026-10-05, section 2.3, equations 19–23 and Appendix B: the coefficients and
q polynomial used by CFG344 match the analytic EPS formulation. That
formulation is explicitly **not calibrated to simulation data**. Its q fit
uses WMAP5. The README's description of these coefficients as N-body calibrated
is inaccurate for the formulas actually implemented. This reduces one stated
caveat; it does not validate their transfer to B. Unresolved: mass-unit
conventions throughout the implementation, nonstandard collapse barriers,
cold-component spectrum, satellite infall/stripping, and object-level histories.

[Hu, Barkana and Gruzinov, PRL 85 (2000)](https://background.uchicago.edu/~whu/Papers/fuzzy.pdf),
equations 8–9, checked 2026-10-05: the cos(x³)/(1+x⁸) transfer and x coefficient
in CFG345 match the primary source. Its half-mode refers to **power** halved,
so T²=1/2 is the appropriate convention for that comparison. A half-mode
mass below the cooling mass is a proxy, not a theorem that the needed halos
form or have the assumed accretion history. Other memory-transcribed source
leaves remain conditional. No source PDF was cached in this work.

## Sol61's older expansion branch remains a separate candidate

The September 30 branch derives a conditional spherical MOND reduction and
a0=2H/beta, C=3beta²/4. It does not supply B's ownership rule. Its regular-center
obstruction, Theta=0 issue, source/cosmology matching, independent beta/U
selection and full health remain open; Claude's filtered-chassis passes do
not repair those equations. The thermal sprint excludes microscopic counting
alone as a selector in its stated model. Resume that branch only with a
changed premise addressing a named obstruction, not another vacuum scan.

## Evidence and continuation

[switch_checks.py](switch_checks.py) performs the exact identities and finite
root discriminators. The current completed run is
[checkpoint_b](runs/checkpoint_b/manifest.json); checkpoint_a predates the FRW
extension and remains historical. Read the raw stdout for every check.

Three distinct live routes, ordered by what they can decide:

1. **Complete the dynamical switch action.** First derive FRW equations and
   perturbations including rho_sigma, p_sigma, the baryon trigger and the
   full f' / f'' matrix. The cheapest discriminator is whether the same
   calibrated parameters can be off on FRW, responsive in dwarfs and healthy
   through the transition. Existing theta_b candidates fail bound tests;
   this is an audit/repair requirement, not an invitation to rerun them unchanged.
2. **Replace the instantaneous bound label with formation/transport dynamics.**
   Derive a conserved cold distribution and its response to baryon loss,
   accretion and a merger. First require one rule to reproduce UFD growth
   without adding the already rejected cold term to spirals or isolated lenses.
   The closure includes the physical reaction and energy budget.
3. **Joint falsification of the effective model.** Freeze one kernel, density
   footing, cold-mass rule and shared nuisance model across gas discs, dwarfs,
   ellipticals and lensing. Independent distances and tracer profiles address
   actual limiting uncertainties; additional uncalibrated samples do not.

Routes 2 and 3 remain open and partly data-dependent; a lack of a current
action is not a proof that they are impossible. Full gravity closure remains OPEN.
