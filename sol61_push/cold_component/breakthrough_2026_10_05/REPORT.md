# Cold-wave / T5 matching: a positive-density obstruction and two repairs

The physical identity and conserved formation mechanism remain **OPEN**. The
new result is sharper than amplitude freedom or the earlier shell-assembly
obstruction: **FL1's unchanged action cannot implement a radial maximum of a
pre-existing finite cold budget and its baryonic phantom profile whenever the
required residual enclosed mass decreases.** An explicit positive, finite,
smooth cold-budget witness fails this necessary condition. Matching only one
edge aperture escapes the obstruction and has a concrete rotation prediction.

Base supplied by coordinator: `a36191815030afddf1277d413f488fb0c3ac520f`.
Actual source hashes and observed HEAD are recorded in `main_manifest.json`.
Disjoint write scope is this directory. No parent index, Claude file, global
state, commit or push is changed. This is author self-review, not independent
refereeing. No external theorem or global novelty claim is used.

## Exact contract

Assume the **FL1 static gate-on plateau**, f=1, M2=0, with matched homogeneous
boundary modes. The wave couples as in FL1, baryons couple to Phi, and the
auxiliary kernel is sourced by baryons alone. Assume spherical symmetry,
positive wave mass m, and a spherical region interior to a density edge where
the phantom enclosed mass P(r) is defined. Let B(r) be baryon enclosed mass,
C(r) the actual material-wave enclosed mass, and F(r) the stipulated cumulative
cold-budget curve used in a **radial** maximum prescription.

Target: infer whether the same action can give

    M_effective(r) = B(r) + max(F(r), P(r))

without negative material density, dropping source reaction, or changing the
dark force. A radial maximum is an explicit CFG45 reading; the simpler T5
global/edge mass statement need not mean this radial prescription.

## 1. Varying FL1 gives an additive source, with reciprocal reaction

The relevant plateau Lagrangian, keeping auxiliaries independent, is

    L = -(rho_b+rho_c) Phi
        -(2 grad Phi.grad u-|grad u|²)/(8piG)
        + q(|grad w|²)/(8piG)
        + Psi (Delta w-Delta u+Delta v)/(8piG)
        + lambda (Delta v-4piG rho_c)/(8piG),
    rho_c=m|psi|².

The script independently reconstructs and varies the one-dimensional
restriction; the displayed scalar Laplacian identities extend to the flat
three-dimensional static restriction. Their boundary proviso is essential:
the equations determine Laplacians, and homogeneous differences vanish only
under the stated matching boundary conditions.

Phi, lambda, Psi, v and u variations give, respectively,

    Delta u = 4piG(rho_b+rho_c),
    Delta v = 4piG rho_c,
    w = u-v,
    lambda = -Psi,
    Phi = u+Psi/2.

Consequently w is baryon-sourced, the baryon potential is Phi=u+chi, and the
dark potential is Phi+lambda/2=u. If chi is calibrated to the selected
baryonic MOND phantom, spherical baryonic dynamics sees

    M_effective = B + C + P.                                      (1)

This repeats and verifies the known additive-source issue; it is not itself
the novelty claim. Giving C the name P does not replace one source by the
other: C=P in this action gives B+2P. The dark contribution to baryon gravity
is real and reciprocal. Its cross interaction energy is

    E_bc = -G integral rho_b(x)rho_c(y)/|x-y| dx dy.

Both source variations produce the same Newtonian kernel, and translation
invariance gives equal opposite net cross forces. The baryonic kernel
functional has no cold argument on this plateau. Thus “dark feels u only”
does not mean its gravity can be omitted from the baryon equation.

The real and imaginary Schrodinger equations also give exactly

    partial_t rho_c + div j_c = 0,
    j_c = Im(psi* grad psi),       rho_c=m|psi|²>=0.

Vanishing boundary flux conserves total material mass. Interference, nodes,
multistream behavior and high occupation cannot make C'(r) negative.

## 2. New positivity theorem for radial max completion

**Proposition.** Under (1), the target radial maximum requires uniquely

    C_required(r) = [F(r)-P(r)]_+.                               (2)

A necessary condition for any positive spherical material source is that
(2) be nondecreasing. If it is locally absolutely continuous, this is

    F'(r) >= P'(r) wherever F(r)>P(r),                           (3)

up to equality sets. More generally its distributional derivative must be a
nonnegative measure; its origin value and total mass must also obey the
specified regularity/budget. These conditions characterize a positive
radial mass measure, not an exact stationary wave solution.

**Proof.** Subtract B+P from the target using (1). For a wave,
C'(r)=4pi r²m|psi(r)|²>=0 almost everywhere. For a general positive density
the mass of every spherical annulus is nonnegative. This proves necessity.
On F>P the derivative of (2) is F'-P', giving (3). A nondecreasing right
continuous cumulative function conversely defines a positive radial measure;
additional smoothness and origin constraints are needed for a regular wave.

**Crossover corollary.** If F(r0)>P(r0) but F(r1)<=P(r1) at r1>r0 in the
same active region, no such material completion exists on [r0,r1]: (2) falls
from a positive value to zero. This requires neither a core prescription nor
an adiabatic orbit approximation. A finite total budget and an unbounded
phantom guarantee a crossover only if the active region extends that far;
an earlier edge can avoid it. The theorem does not remove that qualification.

For the constant radial floor F=eta B outside a compact baryon source,
C'=-P'<0 on every floor-dominated exterior annulus. This observation applies
to any strictly increasing exterior phantom, including different kernels.
It does **not** apply to an edge-only reading of eta B.

## 3. Finite smooth counterexample, exact P2 kernel

Use G=a0=B=1, radius in r_M=sqrt(GB/a0), and specifically

    g_P2 = sqrt(g_N²+a0 g_N),
    P(r)=sqrt(1+r²)-1,
    F(r)=5.36 r³/(1+r²)^(3/2).

F is a positive-density Plummer enclosed mass with finite total 5.36 B.
Both F and P increase. Nevertheless their positive difference decreases:

| r/r_M | F/B | P/B | required C/B |
|---|---:|---:|---:|
| 2 | 3.835304 | 1.236068 | 2.599236 |
| 4 | 4.894084 | 3.123106 | 1.770978 |
| 6 | 5.144178 | 5.082763 | 0.061415 |

At r=4, C'=-0.754227 B/r_M. The exact derivative expression is

    C' = 3(5.36)r²/(1+r²)^(5/2) - r/sqrt(1+r²),

which is negative there, well away from floating-point ambiguity. A cold
wave would need negative density over an annulus. These points must lie
inside the stipulated active region; choose an edge beyond 6 r_M for this
witness. This is a counterexample to universal radial completion in the
retained FL1 class, not to all T5 interpretations, all MOND kernels, or all
possible actions. The numerical coefficients are **P2**, not nu_mono.

## 4. Positive, finite edge-only repair and a measurable residual

Change the premise: match the target only at R=4 r_M and keep a positive
finite Plummer cold profile. Define

    s = 1 - P(R)/F(R) = 0.361861...
    C(r)=s F(r),       C_total=1.939575 B,
    M_effective(r)=B+P(r)+C(r).

This keeps the FL1 additive source and exactly matches max(F,P) at R. C has
positive density and finite total mass, and its total can be an independently
conserved wave charge. **The normalization, scale radius, and initial state
are chosen; their dynamical selection is not derived.** The extra mass outside
R is explicit; no mass disappears at the matching aperture. Treat the phantom
as having its separately specified density edge; do not extend it to infinite
total mass. The calculation interior to R is unaffected by that edge in
spherical dynamics. Full wave-compatible edge behavior remains open.

The same Newtonian dark force admits classical circular-shell support:
choose j²(r)=G[B+C(r)]r. With mass labels fixed, ordered radial-shell stiffness
is positive, omega²=G[B+C]/r³ outside the compact baryons. This uses the
already established shell-support mechanism, and is not a new stability
theorem or a finite-hbar wave equilibrium/formation proof.

At r=2 r_M this repair predicts

    g_repair/g_radial-max = 0.749470,
    v_repair/v_radial-max = 0.865719,
    log10(v_repair/v_radial-max) = -0.062623 dex.

That observable radial shape separates an aperture match from radial T5.
It is a conditional example prediction, not a fitted galaxy result.
The cold Plummer contribution to the Newtonian excess-surface-density proxy
is independently analytic:

    DeltaSigma_c(S)=C_total S²/[pi(S²+h²)²].

Here h=r_M and physical units are B/r_M². Its amplitude is s times the
unscaled Plummer budget's proxy. Relativistic lensing requires the same-action
two-potential source dictionary; this Newtonian proxy is not asserted to be
FL1's fully derived lensing prediction.

## 5. Alternative repair: a reservoir gate changes the action obligations

Retain a real nonnegative reservoir F and suppress the phantom contribution:

    M_dark = F+W P,
    W=[1-F/P]_+ for P>0, W=0 at P=0.

This gives max(F,P) algebraically. It is a possible **changed-premise**
handoff, not a derived local gate. On the overlap region 0<F<P, a naive
energy insertion E_gate=W(F,P) E0[b] has

    partial E_gate/partial F = -E0/P.

The extra cold source variation and mixed baryon/cold derivative are generally
nonzero. Also partial_r(W E0)=W partial_r E0+E0 partial_r W. Multiplying
the old force by W after variation drops the second term. The finite
coordinate example E0=-B²/r, P=B r gives mixed derivative 1/r² and extra
radial derivative -BD/r³; it is a chain-rule control, **not a MOND action**.

Therefore this recipe cannot simultaneously inherit FL1's unchanged
kernel-blind dark equation by assertion. A new reciprocal action could
potentially implement a reservoir gate, but must derive its extra sources,
forces, stability and conservation. The theorem above does not prohibit
such a changed action. Enclosed F and P are nonlocal functionals and cannot
be treated as independent local scalars without an explicit completion.

## Research routes, overlap and audit

1. **Adiabatic wave-to-shell selection:** inspected and not repeated.
   `sol61_push/support_and_assembly.py` already shows j_target drift and
   failure of pure adiabatic assembly. That route's missing dissipative or
   torque/transport mechanism remains open.
2. **Retained-action radial max:** executed to a counterexample and the exact
   monotonicity criterion. This is the substantive new checkpoint.
3. **Edge-only finite positive repair:** executed constructively, with finite
   mass integral, support check and conditional radial observable. Formation,
   wave spectral state and cosmological amount remain free.
4. **Reservoir-gate repair:** algebra executed; naive gate insertion fails
   unchanged-action reaction. A genuinely reciprocal gate is deferred to the
   main action lane and remains open.

Internal overlap search covered sol61_push, FL1 and CFG4/44/45/253/288/293/344/345.
CFG44 already quantifies additive double count. CFG45 already distinguishes
radial max from an edge-reduced sum and scores the latter's satellite failures.
Thus neither the additive formula nor edge-reduced profile prescription is
claimed new. The new repository result is the **nonnegative-material-source
criterion and finite positive-budget counterexample to unchanged-FL1 radial
max**, with explicit source/force derivation and a source-reaction gate test.
This bounded internal search does not establish worldwide novelty.

Self-review verdict: **refuted, with a valid counterexample**, for universal
radial maximum completion under the exact contract. The action variation,
positive density, finite-budget witness and reaction derivative pass. The
matched homogeneous boundary modes are assumptions. Exact stationary waves,
nonradial stability, halo formation, mergers, cosmology and relativistic
lensing are not addressed. No conclusion transfers automatically to an OFF
region, a different carrier coupling, or a genuinely modified reciprocal gate.

Validation: 21/21 main checks pass, exit 0. Dropping the cold term from the
Phi source gives 20/21 checks and exit 1 exactly at that source check.
Source hashes agree before/after both runs. The standard bounded runner's
**version-2 manifests** in `runs/main_a/` and `runs/mutate_a/` validate against
the repository root and retain stdout/stderr, actual argv, declared-result
hashes and unchanged input hashes. Wall limit is 30 s, CPU cap is 20 s per
process, output cap is 1 MiB, and numerical-library thread cap is cooperatively
1. No hard memory/affinity cap was requested. The failed control remains a
valid failed provenance record. The root-directory custom version-1 manifests
also retain input hashes, but have legacy provenance limitations and are
secondary to these runner records. The cheapest next check is the common-action
variation of a reservoir gate, followed by a finite-wave halo initialized
independently of the target. No such computation is claimed here.

Reproduce from repository root:

```sh
python3 sol61_push/cold_component/breakthrough_2026_10_05/source_matching.py
python3 sol61_push/cold_component/breakthrough_2026_10_05/source_matching.py --mutate-drop-dark-source
```

Second command intentionally exits 1. Results and manifests remain in this
directory. The original cold-identity goal is not closed.
