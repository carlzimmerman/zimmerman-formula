# CFG938 exact-source and saved-numerical audit

**Result:** the key saved arithmetic is consistent with the pinned final source and its disclosed conditional interpretation. Corrected audit receipt `CFG938_NUMERICAL_AUDIT_v2.json` has 48 passing source/provenance/arithmetic checks. No CFG938 model, optimizer, ODE, symbolic script or original module was run/imported. The repository remained read-only; this report and receipts are confined to the requested temporary numerical directory.

The audited revisions are:

| Role | Exact revision |
|---|---|
| Frozen criteria | `7a0d41e8b6e3cc12b09326a236dcc39a0f9f3558` |
| Final code, derivation and raw main/K/MUTATE/first-failure outputs | `92606e049be780aa6ac7d57de60d97e2324c74b3` |
| Ledger row | `a947836f7f6b47d6b6e325092b9e207b11b87cf7` |

Read-only ancestry checks confirm criteria before result before ledger. The working bytes of all audited CFG938 artifacts and dependencies equal their pinned revision blobs. The receipt pins SHA256 values for the criteria, final code, derivation/README, all eight saved JSON/text outputs, common constants, SPARC input and full-precision FP0 input; it also pins the exact ledger blob/row. Original runs have committed raw outputs rather than this audit's own runner manifest, so this verifies the available bytes and their consistency, not a new replay of the symbolic/physical computation.

## Counts and preserved failures

| Saved run | Recorded checks | False checks | Interpretation |
|---|---:|---|---|
| Main | 30 | None | All recorded numerical/identity/reporting controls true; class remains CONDITIONAL |
| K | 3 | None | K1 reduction, K2 dust, K3 weak-field limit |
| MUTATE | 6 | None | The three K controls plus three checks that mutations bite; source prescribes exit 1 when all teeth bite |
| First main | 28 | S3e only | Failed intermediate flow check is retained, not relabeled successful |

The two checks added between first and final main are exactly S8a/S8b, matching disclosure A2. The first output already printed `CLASS: CONDITIONAL` and `all checks pass: False`, which the final derivation explicitly acknowledges. The integrator repair must therefore not be described as if no class label had appeared in the failed output.

The count is not 30 independent data successes. Source checks `S2d3_local_stiffness_EoS_early_universe` and `S8b_differential_free_fall_flag` are explicitly `chk(..., True)` reporting checks. The first reports an excluded local-EoS realization; the second records a structural tension, not an empirical acceptance. Likewise S6's true check means a growth obstruction was computed, not that growth data passed.

The final 20-gate scorecard remains: PASS 2; CONDITIONAL 4; UNTESTED 7; DECLARED 4; FAIL 1; NOT DECIDED 1; PENDING 1. D2 is UNTESTED with the growth flag, and C3 remains FAIL. Main's five true P1–P5 booleans do not promote those other gates.

## K and mutation consistency

Main/K/MUTATE preserve identical unmutated K1 summaries, separately for both footings: 43 radii, zero unsolved points, max relative difference from the encoded law 2.220446049250313e-16, below the frozen 1e-6 line. The code forms the static Euler–Lagrange equation symbolically, verifies its proportionality to R(u)-g_N, then solves its roots. This is a reduction/implementation consistency control; it is not an independent fit demonstrating empirical support or closing four dwarf outcomes. No pointwise roots were recomputed in this audit.

The stored mutation summaries satisfy their declared teeth:

- M1: Newton deviation zero, with law deviations 0.827033/0.841308.
- M3: law deviations 1.644520/1.884435.
- M2: negative large-k omega squared and log-growth slopes 1.0000005–1.0000465, within 0.01 of one.

M2's canonical/alternative tables are identical because the source deliberately uses footing-independent normalized variables; they are not two independent dimensional experiments. No footings were statistically pooled here.

## Slip arithmetic and scope

Recomputing maxima from all ten saved system/footing rows and three stress variants gives:

| Measure | Maximum | Location |
|---|---:|---|
| s_grad | 5.791624731785173e-6 | Alternative footing, cluster, W-only |
| s_847 | 1.539799903790011e-5 | Alternative footing, cluster, +1 kpc stiffness |

The latter is 0.8104210 of the frozen 1.9e-5 bound. Saved inertia margins span 58,545.5345 to 249,845,818.5 and exceed one for these templates. This confirms the recorded finite-table arithmetic, not the inertia inequality for every state.

Source scope matters: S4 evaluates u and rho on the gamma-to-zero law profile and then adds isotropic pressure pi G Lstar squared rho squared for the stiffness variants. It does not solve a stiffness-modified equilibrium or independently calculate the complete adopted chi-tidal metric stress in that loop. The reported bound is thus a weak-field stress estimate on the declared templates, not a new full covariant/finite-stiffness solution or an interval-certified universal slip bound. Those proof/realization questions are outside this saved-numerical audit.

## Settling endpoint energy

Both saved endpoint balances satisfy Delta E_grav + Delta E_W + heat = 0 to the displayed arithmetic precision:

| Saved run | Delta E_grav | Delta E_W | Heat | Recorded monotonicity |
|---|---:|---:|---:|---|
| First | +0.007559110277 | -0.008820411125 | 0.001261300849 | False |
| Final | +0.005304806240 | -0.006566057336 | 0.001261251096 | True |

The heat differs by about 3.9445e-5 fraction (0.003945%), while the separate gravitational/tether changes differ substantially. The final source adds a shell-curvature step restriction to its explicit overdamped integration and retains the first failed output. Endpoint heat arithmetic is independently checked here. The intermediate flow series is not exported in these JSON files, so its entire monotonicity was not independently reconstructed without a rerun.

The source explicitly calls this a gradient flow **by construction**. The ideal conservative action has no mobility/drag/heat law. Adding the tether energy fixes the illustrated bookkeeping omission; it does not derive an actual dissipative settling or transport mechanism or identify its heat receiver.

## Growth flag

Using the declared Omega_c/Omega_b=5.364 gives fb=0.15713387806411064 and fc=0.8428661219358894. The source's matter-era coupling matrix is

    [[fb, fc],
     [fb,  0]].

Its positive eigenvalue is

    mu=(fb+sqrt(fb^2+4 fb fc))/2=0.45087808087112324.

The source's growth equation then gives the scale-factor exponent

    p=(sqrt(1+24 mu)-1)/4=0.6095447174560988,

matching saved 0.6095447174560983. The record's class-A matrix has mu=1 and p=1. This verifies the stated a^0.61 versus a^1 flag under that matter-era/post-recombination/free-baryon model. It does not rerun raw growth data or transfer a prior T2x/class-A pass to this distinct parent. The missing linear medium self-gravity is an obstruction requiring separate work, not a sign of a completed formation mechanism.

## Component differential-field flag and precision reconciliation

The source reads **full FP0 footings** 9.360324825027975e-11 and 1.1312035414413022e-10 m/s squared. Headings round these values. Using the precise inputs verifies every saved medium-field/a0 ratio and residual identity R(u)=u squared/(a0-u)=g_total-u. The resulting table is:

| Host radius | Canonical medium field / a0 | Alternative medium field / a0 |
|---|---:|---:|
| 50 kpc | 0.172040703 | 0.157834028 |
| 100 kpc | 0.090172923 | 0.082376632 |
| 250 kpc | 0.037106152 | 0.033811369 |

The range 0.03381137–0.17204070 supports the rounded 0.03–0.17 statement for the declared 6e10 Msun host calculation. These are model field estimates, not measured offsets or graded satellite survival results.

The quadratic longitudinal ID expression has no C1 C2 cross term, while its baryon-medium cross term remains. This is the stated cancellation of ordinary medium-medium gravity in that sector; residual tether interactions and nonlinear/environmental terms must not be silently discarded. The component-dependent fall and its comparison with CFG925 R3 remain a separate unresolved test. No specific Draco/Sextans/Fornax/Leo I outcome is graded from this pooled-looking summary.

The first **audit** receipt, `CFG938_NUMERICAL_AUDIT.json`, is retained with 12 failed S8 checks because it used the rounded heading footings. The corrected v2 receipt adds the exact pinned FP0 dependency and changes only that audit input, preserving the same arithmetic tolerances and all source/raw bytes. All 48 corrected checks pass. This is an audit precision correction, not a CFG938 model/result correction.

## Forced identities versus chosen structure

Within the assumed dust/current-identification construction, conserved-current identities and the medium's minimal gravitational coupling motivate the longitudinal P identity and tether term. A homogeneous comoving F=-mc squared n state has the dust/isotropic result under those assumptions.

The final source itself appropriately marks W_full as an input, the chi-plus-multiplier realization as a choice, and the tidal-versus-local-EoS stiffness realization as a choice. The argument that the target enclosed-mass u requires extra structure does not prove this particular auxiliary-field realization unique. Positive stiffness and the state-dependent inertia inequality are necessary conditions in the examined WKB construction, not a proof of every nonlinear or non-spherical sector. Matching remains longitudinal/spherical and single-stream, with the stated extra fields and background assumptions.

Consequently the strongest supported numerical conclusion remains **COVARIANT PARENT CONDITIONAL**, with the growth, component-force and inherited C3 flags retained. The data do not establish a unique physical medium, a derived selector/switch, a full dissipative formation mechanism, or theory completion.
