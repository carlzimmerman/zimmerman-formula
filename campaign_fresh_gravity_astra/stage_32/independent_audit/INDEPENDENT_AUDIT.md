# FGF045 independent author audit

Normalized claim: for each fixed task-specified regular positive-side signed-Q
background and unchanged C1,1 polynomial velocity profile, explicit constants
B,N0 exist so that no positive-density C1 solution of the actual isothermal
fluid PDE in the fixed potential covers the stated local characteristic cone
through T_N=B L/(v0 N^4) for N>=N0. Actual smooth fluid solutions independently
obey the full fixed-potential energy balance; integrated zero-flux conservation
is conditional on existence and compatible boundaries.

Primary verdict: **proved as written**, precisely as an a priori
nonexistence-through-time / conditional classical lifespan bound. This verdict
does not assert local existence, a constructed maximal branch, an unconditional
first gradient singularity, coupled gravity, or physical closure.

Authoritative target is the completed author package:
`deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-045/fgf045_run_001/result.json`
SHA256 `c4429fcd1732e85a70161eb2575141b557578aa773d8332943e33f1c9d3b1789`,
and its raw `DERIVATION.md` SHA256
`889775ec9b85969afb58f7f05e4d64601fea4760325a07110dc5e0c8aec26a3b`.
The final raw proof, report, input pins and result were read, not merely the
worker's verdict or checks. All 12 input pins and three artifact pins match.

## Independence and comparison

The separate derivation was frozen at 2026-10-06T01:40:18.726793+00:00:
`FROZEN_DERIVATION.md` SHA256
`4cd8ed17a4305edb503d70e9082d5af4841a6da6eb16f9563039e4626e280028`.
Its timestamp, inputs and independence attestations are in
`DERIVATION_FROZEN.json`. At that freeze I had read task/framework and pinned
old ancestry, but no new author or stage-32 root proof, result, preview or
conclusion. The new stage-32 root proof remains unread in this audit.
Author exposure was recorded separately in `AUTHOR_EXPOSURE.json`.

Both independently obtained the exact density-weighted gradient equations.
The frozen derivation normalized density by nref and used a cosh/sinh envelope
followed by an integrated force error. The author uses dimensionful h=n^-1/2,
a linear bootstrap envelope, and a force threshold guaranteeing increasing
compression. These differ in estimates and constants, but share the critical
weight cancellation; route diversity beyond that is not claimed. Agreement
is not the mathematical evidence: the displayed identities and inequalities
were recomputed below.

## Dependency graph

1. Pinned old ancestry supplies the task's fixed regular background, positive
   rho, hydrostatic balance, exact profile, physical scales and conventions.
   This audit uses these as given premises, not a new global existence proof.
2. Actual fluid PDE + positive C1 regularity -> Riemann characteristic equations.
3. Characteristic flow differentiated in its label -> gradient ODEs under C1,
   without a hidden C2 assumption at the polynomial endpoints.
4. Density weight -> exact cancellation of the uncontrolled mixed gradient.
5. Riemann invariant speed bounds -> shrinking cone containing every backward
   curve used by the sup-envelope inequalities.
6. Upper weighted-gradient envelope -> uniform inverse-density bound on T_N.
7. Initial right-flank compression + bounded force derivative + that envelope
   -> closed Riccati inequality on a specifically contained plus-characteristic.
8. Reciprocal integration -> impossible negative reciprocal by T_N.
9. Separately: actual fluid PDE -> exact kinetic/internal/potential energy law;
   appropriate wall traces -> conditional integrated conservation.

Steps 2–9 are internal analytic derivations. There are no external-theorem,
literature, empirical, numerical, or circular leaves. No dependency arrow
supplies local PDE existence or a continuation theorem.

## Obligation matrix

| Obligation | Status | Decisive check |
|---|---|---|
| Exact task/profile | passed | ell=L/N³, V=v0 N; same zero-extended polynomial |
| C1,1 endpoints | passed | f and f' join continuously; no C2 claim or smoothing |
| Pressure and force | passed | v +/- c_s speeds, -g0, -g0' h and energy pressure work retained |
| Characteristic equations | passed | Direct substitution of both fluid equations |
| Gradient equations for C1 | passed | Differentiate integrated characteristic identity by label |
| Weight sign and power | passed | h=n^-1/2; D+h=h beta/2 cancels the mixed term |
| Density coefficient | passed | M<2A omega and h<=h0+A omega t from coupled envelope |
| Force derivative sign | passed | Uses G1=max |g0'|; no positivity assumption |
| N0 is attainable | passed | Five thresholds have fixed constants; omega grows N4 |
| Cone localization | passed | Strict speed margin; ell+2S_N T_N<R |
| Compression stays positive | passed | Initial w>=b omega and w'>0 at threshold |
| Reciprocal contradiction | passed | Logarithm at T_N equals 8A/b; RHS<0 |
| Classification of breakdown | passed in scope | Nonexistence of full C1 slab; earlier maximal endpoint not classified |
| Local existence/continuation | not addressed | Explicitly outside the proved claim |
| Full energy including potential | passed | Pressure work and fixed-force work cancel exactly |
| Global zero-flux conservation | conditional | Actual smooth solution plus compatible impermeable wall traces |
| Zero-velocity hydrostatics | passed | n=rho,v=0 satisfies both equations, energy current zero |
| Frozen field source | passed | C(n-rho) retained, not inferred zero from fluid energy |
| Both a0 and histories | passed | Separate fixed backgrounds; no evolving-H solution |
| Coupled/observational closure | out of scope | No such transfer asserted |

## Recomputed decisive equations and constants

With r=v+c log(n/nref), s=v-c log(n/nref), alpha=r_x, beta=s_x,
Dplus alpha=-(alpha+beta)alpha/2-g0'. Since Dplus log n=-beta,
Dplus(h alpha)=-h alpha²/2-g0'h=-y²/(2h)-g0'h. Similarly for z.
D0h=h v_x/2=(y+z)/4. These signs fix both the cancellation and density bound.

Initial alpha=omega f'-g0/c, beta=omega f'+g0/c. Thus M(0)<=A omega
with A=2d h0 and omega>=G0/(cd). The characteristic inequalities give
M<=A omega+G1 integral H and H<=h0+(1/2)integral M. A first contact at
M=2A omega contradicts G1 Hstar B<A omega². Therefore
h<=h0+A omega t<=Hstar and n>=Hstar^-2. This is an actual uniform lower
bound, not the inadequate invariant-only exp(-constant N) estimate.

At x*+ell/sqrt(3), f'=-d, d=8/(3sqrt(3)), and g0>0 give
w(0)=rho^-1/2(d omega+g0/c)>=b omega, b=d hmin. The threshold
b omega>2 sqrt(G1)Hstar implies G1 h<w²/(4h), so

 w'>=w²/[4(h0+A omega t)]>0.

The bound preserves its own trigger. Its reciprocal is at most
1/w(0)-log(1+A omega t/h0)/(4A omega). For
B=(h0/A)(exp(8A/b)-1), the value at T_N=B/omega is <=-1/(b omega).
Every constant is dimensional where required: A,b,Hstar have units h,
omega inverse time, B dimensionless, G1 inverse time squared. No claimed
optimal constant is needed. The G1=0 case satisfies the same proof without
force-error absorption difficulty; c>0 is essential and is assumed.

The speed bootstrap gives |v|+c<S_N on the cone. A plus-characteristic at
the selected initial label has displacement <=S_Nt; the explicit third N0
threshold keeps it strictly within K_t. Its displacement and initial offset
are O(N^-3). The cone's initial interval remains fixed width; the final
proof states this distinction explicitly.

The full energy density and current are
E=nv²/2+c²n[log(n/nref)-1]+n phi0 and
F=nv[v²/2+c²log(n/nref)+phi0]. Internal pressure work cancels -v p_x
after adding pressure flux, and potential transport cancels -nv g0. Subtracting
the static background and mu times continuity, where
mu=c²log(rho/nref)+phi0, gives the stated relative-energy law. No Reynolds
terms are omitted by falsely claiming conservation on the moving cone.
At t=0, v_t=-v v_x cancels the positive kinetic-energy derivative belonging
to the earlier prescribed stationary velocity. This confirms the distinction
from FGF044 without changing the field source residual.

## Failures, corrections, checks and remaining gap

The raw unweighted mixed-gradient route fails to close from one compression
sign alone. The frozen derivation also records why an invariant-only density
bound and a constant-coefficient short-time comparison are insufficient.
Neither failed estimate is evidence of a singularity; the completed argument
uses the impossible reciprocal as its contradiction.

The initially read author proof had hash
e906db202d89174f3e5f1dff41a6481ebb8e06b772e117b0a0bd95797a7fd11e.
The exact initially read draft bytes were not separately saved; the exposure
record preserves its hash, not a reconstructed historical file. Before packaging,
the author clarified the fixed-width cone versus O(N^-3)
displacement, force-bound notation versus Newton's G, and a stray whitespace.
I reread the complete final proof with hash 889775ec...26a3b. No mathematical
revision was requested by this audit, and no unresolved proofreading issue was
found. My own frozen proof remains byte-preserved. Its administrative source
read-before-separate-hash-check order is disclosed in that proof; all eight
ancestry hashes matched, and there was no changed-premise rescue.

Validation was direct symbolic reconstruction and administrative file/JSON/hash
checks. Shell commands read only the specified sources and package, then wrote
this audit scope. A Python standard-library check verified all declared SHA256
pins and all required RESULT_CONTRACT fields; no mismatches or missing fields.
No mathematical computation, sampling, installs, services, network, commits,
numerical wall/thread/memory claims or literature mechanisms were used.

There is no missing implication inside the stated conditional lifespan theorem.
The exact next gap for a stronger result is direct local C1 existence and a
continuation criterion for these exact C1,1 data, followed by attaching this
bound to a constructed maximal branch. An earlier stopping mechanism is not
classified by the current proof. The cheapest further check would address
that one gate in the same local fixed-potential system, not repeat this bound
or infer coupled/physical closure.

Proofreading coverage: all newly written independent derivation and audit prose;
no routine or mathematical-token edits to the frozen derivation, no unresolved
notation or reference defect found. No LaTeX compilation is applicable to these
plain Markdown records.
