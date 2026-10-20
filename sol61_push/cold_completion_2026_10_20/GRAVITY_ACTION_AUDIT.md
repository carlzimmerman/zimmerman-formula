# Gravity and polarization action audit

20 October 2026. Assigned base checkpoint: `dce2a2e3da65565cd30b4b2c0d20b8cf4b3e8c42`.

**Verdict:** the corrected Newtonian polarization action gives the stated simple interpolation in its spherical, negligible-stiffness static limit. It does not by itself supply the independent cold mass, conservative settling/capture, a stable free excess, a microscopic carrier–polarization bridge, the vacuum normalization, or the relativistic lensing metric. The canonical identification branch and Class-A settling branch are different dynamical systems; they cannot be combined by exchanging their convenient terms.

This is a read-only source audit and analytic rederivation, not a reproduction of any source experiment. Twenty-one source hashes are in `sources_gravity.json`. Nineteen match the assigned commit exactly. The local `ACTION_CORRECTION.txt` and `MASTER_COLD_ENERGY_EQUATIONS.md` do not match that commit; their current bytes are pinned as local evidence, without promoting them to committed base evidence. No original source, criterion, publication, live job or shared checkpoint was changed.

## 1. Source authority and version boundaries

- `closure_map/ACTIONS_AND_NOGOS.md` is a September 28 route map with its own supersession/reliability warning. Its old gap count and statements that certain routes were never run are not current verdicts. Its no-gos have explicitly scoped hypotheses; none is a universal exclusion of cold-energy models.
- `THEORY_v3_DRAFT_2026-10-13.md` now contains the FULL/REMAINDER correction. Its earlier displayed square action must be read through that correction.
- Frozen `THEORY_CANONICAL_2026-10-14.md` S2 already uses the corrected remainder potential explicitly.
- `THEORY_CANONICAL_2026-10-21_DRAFT.md` is the latest v4 **draft written October 20**, not an adopted replacement for older seals. It says it supersedes nothing until adopted. It explicitly leaves the covariant parent and selector open, marks kappa fitted, and distinguishes the baryon-source and free-excess problems.
- The v4 audit checks source citations, headline transcription and wording. Its 533 passes do not constitute 533 physical closure tests or derive its action from a microscopic model.
- CFG542 is a Newtonian dissipative/GENERIC construction; CFG638 derives moments of its specified kinetic settling law. They are not a covariant completion of canonical S2.
- CFG888 is the committed internal source/equation comparison that identifies the self-gravity cancellation and the unwritten self-boost coupling. Its script/result bytes match the base checkpoint.

## 2. Exact equation dictionary

Use physical coordinates, K=4 pi G, and an outward radial gradient convention: gravitational acceleration is **minus** grad Phi. Define

| symbol | exact meaning |
|---|---|
| Phi | Newtonian dynamical potential; it is not yet a complete two-potential metric |
| P | polarization/displacement vector, with density-divergence units under ID |
| u_vec=K P; u=|u_vec| | polarization vector in acceleration units and its magnitude |
| B=grad Phi-u_vec | source flux vector, with div B=K rho_b |
| g_Nb=G M_b(<r)/r^2 | positive baryonic Newtonian radial field |
| g=Phi'(r) | positive total radial field; physical acceleration is -g r_hat |
| a0 | acceleration scale supplied to the potential; not derived by the constitutive relation |
| gamma=K Lstar^2/2 | positive spatial stiffness coefficient; Lstar is an input/bounded scale |

For 0 <= u < a0 define the **physical energy-density potentials**

    W_full(u) = [-a0 u - a0^2 ln(1-u/a0)] / K,
    W_rem(u)  = W_full(u) - u^2/(2K).

Their acceleration-normalized derivatives are different:

    D_full(u) := K dW_full/du = a0 u/(a0-u) = u/(1-u/a0),
    R(u)      := K dW_rem/du  = u^2/(a0-u),
    D_full = u + R.

Thus source statements `W'(u)=u/(1-u/a0)` and `f(u)=u^2/(a0-u)` do **not** identify one interchangeable physical W. The first is the full restoring acceleration (with the K normalization absorbed); the second is the residual restoring acceleration after subtracting the critical quadratic. An unnormalized derivative with respect to u has an extra factor 1/K. A derivative with respect to |P| instead already includes K.

The two equivalent static actions are

    L_expanded = -|grad Phi|^2/(2K) + P dot grad Phi
                 -rho_b Phi - W_full(u) - gamma |grad P|^2/2,

    L_square   = -|grad Phi-KP|^2/(2K)
                 -rho_b Phi - W_rem(u) - gamma |grad P|^2/2.

Expanding the square produces -K|P|^2/2=-u^2/(2K), which is precisely the quadratic already included in W_full. Using W_full in L_square double counts it.

## 3. Euler–Lagrange equations and static law

Variation in Phi, with the appropriate fixed/decaying boundary data, gives

    div(grad Phi-KP) = K rho_b,
    laplacian Phi = K[rho_b + div P].

Variation in P gives

    grad Phi-KP = R(u) P_hat - gamma laplacian P,

or equivalently

    B = R(u) u_hat - (Lstar^2/2) laplacian u_vec.

In the expanded convention the same equation is

    grad Phi = D_full(u) u_hat - (Lstar^2/2) laplacian u_vec.

The limit u=0 is understood continuously. If one separately chooses `L_kin=I|dot P|^2/2`, its field equation would be

    I ddot P = B - R(u) P_hat + gamma laplacian P.

That kinetic term and I do not follow from the displayed static action, and a carrier displacement supplies a different inertia structure unless derived. Static constitutive convexity is not a proof of a healthy full kinetic/covariant theory.

For a spherical regular solution, B=g_Nb r_hat. For radial u_vec=u(r) r_hat,

    g_Nb = u^2/(a0-u)
            - (Lstar^2/2)[u'' + 2u'/r - 2u/r^2].

This is a **vector** Laplacian; dropping the -2u/r^2 term is not the spherical vector equation. Neglecting stiffness yields

    g_Nb = R(u),
    g = g_Nb + u = D_full(u),
    u = a0 g/(a0+g),
    g_Nb = g^2/(g+a0),
    nu_s(y) = 1/2 + sqrt(1/4 + 1/y), y=g_Nb/a0.

In general geometry, div B=K rho_b is a divergence equation; it does not alone set B equal to the baryonic gradient pointwise. Collinearity/longitudinal conditions and boundary data must be stated before applying the algebraic spherical law.

For comparison, the erroneous square-plus-full-W action gives B=D_full(u) u_hat, so in the same spherical zero-stiffness limit

    u=a0 g_Nb/(a0+g_Nb),
    g/g_Nb = 1 + a0/(a0+g_Nb) -> 2 in the deep limit.

It does not give the claimed deep square-root law. This is an exact correspondence failure, already identified by CE-FM-010, not a numerical-resolution effect.

## 4. Physical carrier, net polarization charge and self-gravity

Under the identification (ID),

    div P = delta rho_c = rho_c-rhobar_c,
    dot P_L = -j_c,L

implements continuity for the longitudinal displacement, modulo initial/boundary data. For an isolated basin with P=0 on its outer boundary, integral div P dV=0. An interior positive polarization charge is balanced by an edge deficit. The pure polarization divergence therefore cannot supply a positive cosmological mean cold mass or an independently moving rest-mass inventory. A real carrier's mean density, inertia, phase space and production are additional ingredients.

After eliminating Phi, the carrier's Newtonian self-energy is cancelled by the critical quadratic in the ID branch. For a longitudinal Fourier mode rho_b=B cos(kx), delta rho_c=C cos(kx), the quadratic on-shell Lagrangian is

    <L_ID> = K B(B+2C)/(4k^2),
    <L_Newton> = K(B+C)^2/(4k^2).

The C^2 term vanishes; the baryon–carrier cross term remains Newtonian. This is cancellation of the ordinary quadratic carrier self-gravity, not absence of every nonlinear restoring/stiffness interaction.

With suitable longitudinal boundary conditions, the reduced potential energy is schematically

    E_red = W_bb - integral P dot grad Phi_Nb dV
            + integral W_rem(u) dV + gamma/2 integral |grad P|^2 dV.

For a cold radial carrier at rest, the corresponding net outward acceleration is

    a_r = -g_Nb + R(u) - gamma (laplacian P)_r.

Equivalently, before cancellation its force is total gravity `-g` plus the full tether `D_full`; afterwards it is baryonic gravity `-g_Nb` plus the residual tether `R`. Do not add total gravity and residual tether after having already removed self-gravity, or add full tether to baryonic-only gravity.

Since R'(u)=u(2a0-u)/(a0-u)^2>0, adding positive excess above the static law raises the outward residual force. The existing ID action does not provide a self-bound excess clump. For longitudinal P, Parseval/integration by parts gives

    integral |grad P_L|^2 dV = integral (delta rho_c)^2 dV.

Thus the stiffness is an integrated repulsive density-squared energy. This is not a pointwise identity `|grad P|^2=(div P)^2` for every arbitrary three-dimensional vector field.

### Independent free mass is a different source decision

If P is an independent field and one adds ordinary matter coupling `-(rho_b+rho_f)Phi`, the Poisson/source equation becomes

    div(grad Phi-KP)=K(rho_b+rho_f).

The free density then enters the constitutive source. If P instead remains the displacement of that same rho_f, adding it again as independent matter double counts the intended carrier density. A separate real free sector plus independent polarization is a possible *different architecture*, but it is not the already written ID action and must derive its reciprocal source/force rules.

In Class A, `laplacian Phi=K(rho_b+rho_c)` and both species feel Phi, so cold self-gravity is Newtonian. The target phantom is a separate baryon-only functional. CFG541 uses

    nu_e(y)=1/[1-exp(-sqrt(y))],
    M_ph(<r)=[nu_e(g_Nb/a0)-1] M_b(<r),

rather than the exact nu_s above. They agree in the leading deep limit but are distinct interpolations. A successful Class-A numerical moment or settling calculation does not prove action correspondence to canonical S2.

This explains CFG888's finding: the finite clump mass `81 sigma^4/(4 G a0)` assumes law-boosted self-gravity, while the implemented star force adds that clump Newtonianly. Neither ID nor the baryon-only Class-A target supplies that hybrid as a derived result. The unwritten self-sourcing coupling is an obligation, not a normalization correction.

## 5. CFG542/638 energy exchange is not the missing microscopic bridge

CFG542's Newtonian dissipative construction uses Vlasov–Poisson for real mass and a partner field. It arranges a positive dissipative operator with `M delta E=0`, so drift energy can be transferred to that partner. Its source Q is

    Q = rho_c alpha tau 1_B 1_C grad psi dot grad Phi
      = -rho_c v_s dot grad Phi.

But the full GENERIC entropy degeneracy `L delta S=0` fails: orbital transport can increase the deficit functional. Mobility alpha, segmentation, catchment and the switch remain inputs. Its inertial slip extension Pb* is recorded INCONSISTENT, not a conservative formation completion.

CFG638's momentum-conserving OU kinetic form is

    dt f + div_x[(v+v_s)f] - grad Phi dot grad_v f
       = (alpha/tau) div_v[(v-u_c)f + sigma_J^2 grad_v f].

The matter-energy source contains

    rho_c v_s dot grad Phi
       + (alpha/tau)[3 rho_c sigma_J^2 - tr Pi].

Closed boundaries do not make those terms divergences or make them vanish. The second is bath exchange; the first changes sign between inward settling and outward removal of an overfill. One cannot call this a closed isolated collision/merger operator merely because mass or momentum moments close.

The proposed partner equation `ddot phi +3H dot phi-c^2 laplacian phi+V'(phi)=Q/dot phi` requires a dynamical receiver; it is singular at dot phi=0. An exactly constant vacuum cannot absorb finite Q and remain that same constant vacuum. A microscopic interaction action and its reciprocal stress-energy exchange are still required. This partner is not automatically ARGON, the original charged carrier, the P field or a merger radiation channel.

## 6. What remains unknown about normalization and lensing

The scale relation is an external input/target,

    a0=kappa c sqrt(G rho_DE),
    a0^2=kappa^2 Lambda c^4/(8 pi),
    Lambda c^4/a0^2=32 pi  when kappa=1/2.

Here rho_DE is mass-equivalent density. The saturation potential gives a force law after a0 is specified; it does not select kappa, explain the measured G, fix the vacuum offset, derive the cosmic abundance 5.364, or determine retention/catchment. Rewriting the same chosen normalization with 16 pi or 32 pi in different potential conventions is not an independent prediction. The v4 synthesis explicitly labels kappa fitted and Lstar, alpha and supply ingredients unresolved.

Canonical S2 has one Newtonian potential. In a relativistic metric, slow motion probes Phi while lensing probes Phi+Psi. Neither a scalar force nor the single Poisson equation derives Psi, its slip, gravitational-wave propagation or cosmological perturbations. CFG847's small-slip estimate is conditional on a well-posed parent and its stress assumptions; it is not that parent. The MASTER inventory explicitly leaves S_bridge unspecified and warns against adding a real halo and an inferred force discrepancy twice. Preferred basin anchoring, hot-versus-condensed source selection and a covariant matter/medium coupling remain unbuilt obligations. A declaration that real mass gravitates in GR is not a derivation of the combined restoring-force stress tensor.

## 7. CFG932: declared next test, not a closure result

At the assigned checkpoint CFG932 has frozen criteria only (`dce2a2e3d`). At this audit's source receipt a local `DERIVATION.md` had appeared, but no script/output/result was used, and no live work was duplicated.

It plans: (Q1) the energy equation and a drift-work identity for one-/two-sided/gated Class A; (Q2) rearrangement costs for declared primordial native-NFW debris; (Q3) a universal efficiency window against declared SN/AGN energy; and (Q4) an engine-energy-budget code reading. Primary/alternative energy measures, collapse/concentration brackets, dwarf baryon-loss factors 1/10/100, and the hypothesis's post-hoc origin are disclosed before the run.

These are useful discriminating checks. They do not derive the microscopic collision/merger kernel or adopt a new action. The representative system list does not contain Sextans or Leo I, so passing it would not close the existing four-dwarf budgets. Also, removing a primordial central surplus can require **import**, whereas assembling a diffuse patch into a dense core requires **export**; the different signs refer to different initial states and must not be exchanged silently. The source-relative and self-consistent energy measures are declared alternatives, not automatically identical action-level energies.

## Completion gate supplied by this audit

A viable unified continuation must specify which density is the ID displacement, which density is independently gravitating, which exact interpolation potential is varied, what field carries exported energy/J/charge, and how its stress couples to the physical metric. Then derive the reciprocal matter equations and the global conserved ledger from that one choice. Until that dictionary and bridge are explicit, combining canonical rest equilibrium, Class-A settling, a self-boosted clump mass and separate ARGON merger fuel is a collection of conditional mechanisms, not the completed cold theory.
