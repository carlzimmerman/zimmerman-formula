# FGF036: weighted coupled crossing form and linear evolution

Accepted conditional theorem in the inherited Q diagnostic action: every
FGF035 central solution with positive coefficients admits sufficiently short
induced-wall restrictions on which the FULL coupled form is positive, closed
and coercive in its weighted energy domain. The actual transmission operator
has a compact positive inverse and a discrete positive spectrum, giving unique
conservative finite-energy LINEAR evolution. No calibrated physical length,
nonlinear theorem or physical-theory closure is supplied.

The phi space consists of globally absolutely continuous functions with zero
outer traces and finite integral A psi_x², A~constant sqrt(|x|). Integrability
of 1/A gives |psi(y)-psi(x)|²<=integral A psi_x² integral_x^y 1/A and
||psi||²<=ell integral(1/A) integral A psi_x². The reciprocal-A coordinate
identifies this space with ordinary H1_0 on a finite transformed interval.
Root alternatively reconstructs it by convergence of weighted derivatives and
the zero-integral constraint. Smooth physical-x functions are dense; center
flattening or corrected derivative approximation proves it without assuming
an extra boundary. Completion preserves one continuous center value, not jumps.

Let E_d=integral cs²d²/rho, E_p=integral A psi_x²/C,
E_eta=integral J eta_x²/C, d=-(rho xi)_x. The author retains every matter/scale
cross term and gets Q>=E_d/2+(1/2-alpha)E_p+(1-beta)E_eta, with
alpha=2C rho_max ell integral(1/A)/cs² and
beta=ell²[2sup(q_s²/A)+sup(-m)_+]/J. Taking alpha<=1/4,beta<=1/2
proves coercivity. These conditions hold as the same fixed central solution
is shortened; no coefficients or potentials are retuned. Root's separate
bound uses m-2q_s²/A>=m(0)/2>0 and the same fluid shortness margin.
The two sufficient bounds agree in implication, not in identical constants.

The bounded form and complete domain prove closedness. Uniform weighted
continuity estimates give compact kinetic-L2 embedding by finite-grid
approximation, including the center. Minimizing Q/2 minus the source pairing
constructs the inverse; symmetry/positivity/density yield a compact positive
injective inverse. The supplied Rayleigh-maximization and orthogonal-complement
argument supplies an eigenbasis; the diagonal domain proves self-adjointness.
Modal energy sums then give a unique weak linear wave solution in V times H,
with conserved quadratic energy. This is not a formal spectral claim inferred
from a finite grid. No numerical or symbolic mathematical process was run.

With h=cs²d/rho+psi and P=A psi_x-q_s eta, the exact operator is
L_xi=h_x, L_psi=(C d-P_x)/tau,
L_eta=(-J eta_xx+m eta-q_s psi_x)/sigma.
Its domain is u in V with h,P in H1 and eta in H2. Weak equations establish
necessity and global integration by parts establishes sufficiency. Thus
psi,h,P and J eta_x transmit continuously across zero. No P(0)=0 condition
is allowed merely because A(0)=0. Both author and root construct a complete
coupled domain state with nonzero center flux, using a singular weighted psi
and a compensating mass-preserving fluid displacement so h is constant.
A phi-only singular state would not automatically satisfy the fluid domain.
This check prevents replacing the crossing by two reflecting half-intervals.

The author's symbolic gap Q>=N/T_h² retains inverse-time-squared units:
T_h²=max[2rho_max² ell²/(cs²rho_min²),4tau ell integral(1/A),
2sigma ell²/J]. It is a sufficient bound on each selected small interval,
not an observed frequency or a shared astrophysical scale. Ordinary psi H1
coercivity still fails exactly as FGF035 proves. The weaker completed linear
energy domain may exceed the domain of the exact nonlinear energy; no
nonlinear Taylor approximation or nonlinear stability follows automatically.

Author, root and independent reviewer froze their derivations before reading
the other new proofs; the shared task route and prior sources are disclosed.
Root read the full author proof and compared units, factors, domains, smooth
density, center control and spectral construction. A separate root-only audit
checked its proof without the new author/reviewer texts. Audits spell out the
countable-basis weak extraction, spectral exhaustion and invariant mode-tail
convergence used in the abbreviated Hilbert arguments; those elaborations
remain separately credited. Source/result/audit pins match. Proof-only: zero mathematical computations/manifests. Preserved
failed shortcuts are ordinary-H1 coercivity and the artificial reflecting
center; no failed numerical run was fabricated.

Both a0 normalizations remain separate positive-reference hypotheses. Frozen-H,
constant-vacuum and evolving-H branches remain distinct. Actual local scale
response is an added diagnostic premise; no physical V, covariant reservoir,
metric/photon/DOF, RAR/M/filtered-MONO transfer or instrument-calibrated result
is proved. Walls and mass vary when the background interval is shortened;
they are fixed for perturbations on each selected interval. No arbitrary
preassigned BVP, global domain or historical novelty claim.

FGF037 records the next discriminating gate: compare the completed weighted
linear domain with the exact nonlinear action energy. Test finite-amplitude
singular directions and smooth concentration controls before treating weighted
linear control as nonlinear control. This is a ready task, not launched or
accepted evidence. Primary AS228 repair ownership and FGF031 calibration stop
remain unchanged. Physical theory remains open.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/result.json` SHA256 `d238f3db45e4aacbce15487c89c1c66f7131915cba7a1c6e5043179b0e30c515`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/DERIVATION.md` SHA256 `71727e56c1c7d88bd2d24988af4683339b5fdc4db6f9ca54d9c800752a747f1a`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/REPORT.md` SHA256 `885138f7a87fcc8e90d0a204189504b0b1167157c7b76a10dfaa79bea17a495c`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-036/fgf036_run_001/input_sha256.json` SHA256 `ae9326e94db0d82472dc12a6b03c5e11f84573ffe21464af247ceb7231e55fac`.
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/INDEPENDENT_AUDIT.md` SHA256 `261c45599a27f5772aabece8593630588b2947b4712065b7da2312716e8e3f56`.
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/PROOF_COMPARISON.json` SHA256 `afa228c0ec4aa2ca05575ca767eecb6e4791472e8524807ea3cc6d3e3a67b3ea`.
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/PROOF_RECORD.json` SHA256 `6a2a44d3b7b122da42ba29a75c398010e3c2e5cd4c793332635784c0e5bc2ad1`.
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/ROOT_DERIVATION.md` SHA256 `1ad5e82feb6a57aebd7a30df7ce0b6fb3be0a42e01ea14a084371aff578e2dc0`.
- `campaign_fresh_gravity_astra/stage_23/weighted_crossing/audit_result.json` SHA256 `fa69589f5bf89d9ffd10faf5e15f35b6dab691d8b7e34f84a1da585d114e6075`.
- `campaign_fresh_gravity_astra/stage_23/independent_audit/DERIVATION_FROZEN.json` SHA256 `acbb8497b34c63e8e70fc19b85011c6655c619b68a217e7ec68381cfefa6a331`.
- `campaign_fresh_gravity_astra/stage_23/independent_audit/FROZEN_WEIGHTED_DERIVATION.md` SHA256 `5c231865662ada4a210384166d62dcb276f97b1949ae94013a195e53bc42a2f6`.
- `campaign_fresh_gravity_astra/stage_23/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `71ed1fb888826970c03f3494731ae94becf1a0ebc3310fc647522df1cbd6a19e`.
- `campaign_fresh_gravity_astra/stage_23/independent_audit/audit_result.json` SHA256 `3740fd6fa0904e0ee29f6baebbabd7011dd257e8d66817f7c44daa6400bc00d0`.

Reconciled 2026-09-30T17:41:28.022316+00:00.
