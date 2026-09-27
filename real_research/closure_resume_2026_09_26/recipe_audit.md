# Recipe reconciliation audit — 2026-09-26

**Normalized claim:** one explicitly defined particle-free relativistic action
derives all thirteen requirements of `FRIED_CHICKEN_SPEC.md`, including the exact
exponential quasistatic law, the stipulated gravitational/matter mode count,
ordinary matter conservation and acceptable physical causal response, on mutually
compatible nonempty branches.

**Primary verdict: incomplete, with the smallest missing implication identified.**
The recent screened C-H/K, source-restricted kernel, vacuum gate and carrier
results have not been derived from one action with the frozen specification's
kernel and field classification. In fact, `nu_mono` changes the exact constitutive
target. This audit is not a universal no-go and does not close the research goal.

This is an independent bounded source audit at HEAD
`4e16ccf585f6fcc775a2f9d62ac30d329212e0af`, including existing untracked September
26 material. No existing scientific script was rerun or modified by this audit.
Its only edits are this report and a dated amendment to the recipe. The success specification is
unchanged. No `.mathbox` ledger exists at repository root. Literature claims are
treated as conditional inputs here rather than silently reverified.

## Authoritative objects and dependency graph

Paths in this report are repository-relative; line numbers refer to the source
versions hashed below.

1. **Contract:** `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`,
   requirements 1–13. Exact exponential AQUAL and one common action are explicit.
   The exception to two gravitational modes requires a genuine, separately
   counted healthy matter/clock scalar. A name does not prove that exception.
2. **C-H definition:** `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`,
   “Fields, constants and domain,” “Intrinsic operator, measure and all endpoint
   terms,” and “Auxiliary equations.” This supplies the metric, varied clock,
   heat-flow auxiliaries, operator domain and boundary terms. Its opening states
   that screened T-B is not strict exponential AQUAL T-A. `Lambda`, `a0` and `xi`
   are independent inputs. Its elimination proof does not certify the full
   physical-time mode count. The compact-leaf domain and its isolated limit must
   not be interchanged silently.
3. **C-H/K addition:** `real_research/g03_audit_2026/L340_filtered_khronon_completion.py:8`
   specifies `I_CHK=I_CH+(c^3/16πG)∫√(-g)[α_c a²−c₂K²]` and changes the kernel
   to `nu_mono`. Its actual scalar block is at lines 137–177. Its health test at
   lines 180–214 is linear, frozen-coefficient principal-order work, expressly
   scoped at lines 60–64. The 243-cell H3 scan is at lines 216–233.
4. **Later modifications:** L353 adds a dark-source subtraction pair; L359 adds a
   vacuum gate; L361 supplies a nonrelativistic region-local action. These are
   additional action dependencies, not labels under which the old full-action
   obligations remain automatically proved. L361's scope expressly holds the
   gate prescribed and does not redo the relativistic embedding.
5. **Observable checks:** KM3 uses the reduced Solar-System khronometric action;
   XC1 uses frozen-background decoupling power counting; gate/cluster/forest
   calculations use their stated field laws and numerical initial data. Each
   depends on an action-to-approximation bridge and a shared parameter cell.
6. **Full conclusion:** requires those bridges, full variations and constraints,
   and compatibility of the branches. These leaves are still missing.

## Obligation matrix

| Obligation | Result of this audit | Exact scope |
|---|---|---|
| Exact exponential law, requirements 1/12 | Failed as an identification of `nu_mono` with the frozen law | A distinct kernel and screened QUMOND response cannot establish exact AQUAL for general sources. This does not refute the exact law itself. |
| Separate gravitational/clock count, requirement 2 | Not addressed at full-action scope | L340 has a scalar mode; a nonlinear canonical classification of the assembled action and the clock exception remain necessary. |
| Both lensing potentials, requirement 3 | Conditional | Static leading-order C-H/K block has independently solved equal potentials. New source restrictions/gate stresses need the same derivation. |
| Full PPN and measured Newton constant, requirements 4/10 | Conditional | KM3 derives static `β=γ=1` and `G_N=G/(1−α_c/2)` for its reduced sector. Other parameters and filtered corrections are documentary or imported. |
| Ordinary-matter Ward identity and one physical metric, requirements 5/11 | Conditional for the assembled action | Original minimal matter has the usual separate identity; new field/source/gate couplings need an explicit covariant completion. |
| Tensor speed and energy, requirement 6 | Conditional | The original β=0 khronometric sector and specified TT checks are useful. Full modified action, background and boundary obligations remain. |
| Scalar health and causal response, requirement 7 | Incomplete; metric-cone subluminality fails in XC1's stated UV window | Linear positive energy does not prove nonlinear well-posedness. XC1 reports `c_s/c≈444…793559`; preferred-time causality is a different criterion. |
| Expanding FLRW and separate homogeneous mode, requirement 8 | Conditional | A leaf-average `K−⟨K⟩` repair changes the homogeneous action; it must be included in the action identity. Numerical evolution is not full perturbative closure. |
| Zero-gradient/constraint-rank limit, requirement 9 | Not addressed by this audit | C-H's composite primitive is C¹ but not C² at zero gradient; divided nonzero-mode formulas do not extend by assertion. |
| Vacuum normalization, requirement 13 | Conditional input permitted by the contract | C-H itself does not derive `a0` from Λ. Four-form or condensate proposals must retain their own free constants and field equations. |
| Full G8 strong coupling | Conditional | XC1 tests particular cubic/quartic vertices and selected bounds; filter variations, full background mixing and other vertices are uncomputed. |
| No dark-matter particle | A legitimate explicit construction constraint | It neither forbids classical field data by definition nor derives independently supplied dark density from baryons. |

## Decisive exact kernel calculation

On the isolated spherical branch with no extra central flux, use the contract's
variables, not L340's differently named argument:

\[
x=g/a_0>0,\qquad t=g_N/a_0=x(1-e^{-x}),\qquad
h/a_0=(g-g_N)/a_0=xe^{-x}.
\]

For `x>0`, `dt/dx=1+(x−1)e^(−x)>0`: on `0<x<1`, the subtracted
quantity `(1−x)e^(−x)` is strictly less than one, and at `x≥1` the result is
at least one. Consequently the longitudinal inverse-response coefficient is

\[
C_L=\frac{d(h/a_0)}{dt}
=\frac{1-x}{e^x+x-1},\qquad
C_L\big|_{x=2}=-\frac1{e^2+1}\approx-0.1192029220.
\]

It is negative for every `x>1`. L340's construction instead requires positive
`C_T=nu−1` and `C_L=d[t(nu−1)]/dt` in its tested scalar block and builds a
different monotone-phantom kernel for that reason. This is an exact conflict
with importing the exponential law into that positive-`C_L` branch; it is not
a proof that no other constrained action can realize the law.

L340 defines `nu_RAR(t)=1/(1−exp(−sqrt(t)))`, while the exact spherical inverse
of the recipe is implicit in `t=x(1−exp(−x))`. Those are already different
interpolations, even before the `nu_mono` modification and heat filter.
Agreement to a small number of dex in a sampled statistic cannot establish
identity of the functions or equality of their nonspherical PDEs.

## Claims that must not be inherited without qualification

- **“Health in every momentum channel,”** in
  `real_research/dark_energy_2026/THE_CLEAN_PATH_2026-09-26.md:22`, cites 243/243.
  L340's H3 loops sample three values of `C`, three `c2` values and three values
  each of three extra couplings. Its 243 cases prove no exhaustive coverage of
  functions, constraints or different field content. Preserve “in the scanned
  families and cells.”
- **“1PN = GR,”** in that synthesis's sector table, is too broad without its
  approximation. `KM3_chk_one_pn.py:85` varies a radial static khronometric
  Lagrangian and solves its second-order equations. Lines 130–140 explicitly
  mark the zero-parameter and filtered-remainder claims as documentary `True`
  checks. This is useful β/γ evidence, not a derivation of every PPN term of the
  combined gate/filter/carrier theory.
- **“G8 ... PASSES on C-H/K,”** in `XC1_strong_coupling_chk.py:454`, exceeds the
  scope stated at lines 55–60. It derives decoupling cubic/quartic structures
  and power-counting scales, with a failing `alpha_c=0` control, but omits the
  filter's metric/foliation vertices and treats MOND metric mixing only at
  order-of-magnitude level. Keep the bounded result; full G8 is not closed.
  An exponential filter is extremely small at finite large momentum, not
  identically zero. Exact zero-filter identities and finite-momentum estimates
  must remain distinct.
- **“This is the one open theory problem,”** at the clean-path synthesis line
  84, is not supported: its own table also lists nonlinear well-posedness and
  relativistic embedding, and the source audits add canonical classification,
  full PPN, filter vertices and common-action assembly.
- **“Vacuum sets the scale,”** is a model-building premise until an actual
  action enforces it. XC1's identity
  `sqrt(M_P a0)=(κ²/(8π))^(1/4) ρ^(1/4)` in natural units explicitly substitutes
  `a0=κ sqrt(Gρ)` at line 403. It is a conditional algebraic consequence, not
  an independent derivation of that substitution or of κ. Dimensional analysis
  fixes units and possible powers only after the permitted inputs are declared.
- **Legacy labels:** the old recipe's section 9 expressly says historical and
  warns that its class exclusions/PASS labels were not reaudited. Retain that
  warning. Do not reuse “Current best candidate,” “exhaustive,” or “only live
  class” as a September 26 conclusion. Its old `Z≈21` is not interchangeable
  with the clean-path definition `Z=cH_Λ/a0`, which gives `sqrt(32π/3)≈5.78881`
  if κ=1/2 and the stated vacuum Friedmann normalization is assumed.

## No-particle interpretation and independent initial data

`real_research/reviews/coherence_audit_2026_09_20/no_particle/ANSWER.md` and
`PD04_NOTE.md` already distinguish the three relevant objects:

1. a Newtonian-inferred phantom density obtained from a gravitational response;
2. an action-derived classical field stress and its required initial data;
3. an independently postulated material species with mass/decay/free-streaming
   hypotheses.

They are not interchangeable. The user's constraint rules out introducing the
third as the answer. It does not erase the second's initial data. L353's raw
nonrelativistic action at lines 16–26 explicitly includes `rho_d` and a new
dark coupling; L361's lines 17–31 again include `rho_d`. Neither merely rewriting
an equation as Einstein gravity plus effective stress nor naming that component
a condensate derives its amplitude from the baryonic source. Numerical tracer
particles are a discretization choice; their presence alone does not establish
a fundamental dark-matter particle claim.

The earlier particle-free Lean certificate concerns a separate rational
constitutive family, spherical response existence/uniqueness, and BTFR from
limiting equations. It is not an exponential relativistic action certificate.
No existing Lean file was freshly compiled in this sub-audit; the independent
formalization worker owns the new scoped certificates.

## Verification performed and remaining construction

Read the raw action and the scripts cited above, their scope statements and the
stored L340/XC1 result JSON. Stored L340 records 11 checks with no load-bearing
failure; stored XC1 records 9 checks with no load-bearing failure and its
mutation records one failure. These are provenance observations, not new runs
or acceptance of their broad prose verdicts.

A fresh bounded `python3`/SymPy check differentiated `t=x(1−exp(−x))` and
`h=x exp(−x)`, asserted the displayed rational-exponential identity and the
`x=2` value, and exited 0. It printed `−0.11920292202211756`. The positivity
argument for `dt/dx` and the sign for all `x>1` are given above rather than
inferred from that sample. No broad simulation was run.

**Strongest safe statement:** the recent work supplies constructive components,
scoped analytic identities and bounded tests for an alternative filtered scalar
branch. The exact exponential particle-free relativistic target remains open.

**Cheapest next construction check:** freeze one explicit action revision and
derive its scalar kinetic/constraint block with the exact chosen kernel and all
gate variations present. Determine whether the exponential longitudinal sign
can be accommodated without a forbidden gravitational scalar, a ghost or an
unacceptable physical response. Any repair must retain independent lapse/spatial
metric variation and the matter Ward identity, rather than pool them from
unmodified C-H. This is a construction obligation, not a further parameter scan.

## Source hashes (SHA-256)

| Source | Hash |
|---|---|
| `FRIED_CHICKEN_SPEC.md` | `be0400679673b0bb9463dd399ab8e05b8889659ad97736e1b9926276887361c2` |
| `g03_covariant_action_2026/ACTION.md` | `18b75c25f8842bdb9ea6be22e8f6bfb4ecf67d34819dbb530772632b97d810ed` |
| `L340_filtered_khronon_completion.py` | `b8e52d88c2c3190a015d39a0df2b8f8343ca14164e2f414a289362003a4df1a2` |
| `KM3_chk_one_pn.py` | `4c312663a61655c0e36d0369bccf6322513ab72ca5006f4562ad84008d0d6154` |
| `L353_kernel_invisible_dark_component.py` | `95369bf988ec458819b2a7f569bf7947956d221b8ce795f2828300c5379aea93` |
| `L361_bound_region_kernel.py` | `2246e23236cf6de146e3045dce0df77f4453647313882e399b29f0f2c8bd837e` |
| `XC1_strong_coupling_chk.py` | `66994148e050d18f25f2fe380efb763da21bec25ccb8cdefe909ab7296ac183d` |
| `THE_CLEAN_PATH_2026-09-26.md` | `e35807e8697c4a9050e42de44a8c195d1357f05a72aaa425e01fd4a2fe491734` |
