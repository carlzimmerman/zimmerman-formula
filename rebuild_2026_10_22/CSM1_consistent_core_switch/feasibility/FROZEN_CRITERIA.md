# CSM1 scalar feasibility audit: frozen before new arithmetic

This independent subagent audit is authorized by the CSM1 coordinator. It writes only new artifacts in this
`feasibility/` directory. The current checkout is dirty; base requested by the coordinator is
`2c6b17d683c1a69a1c95754c255de1cc6f79800a`. Existing artifacts, live jobs, and Git history are read only. No commits.
Current instructions override older briefs' commit requirements. No full observational harness, simulation,
download, free-T adjustment, shape adjustment, slope adjustment, or new fitted number is authorized here.

## Claim card

For fixed S9 shape `q(x)=interp(x;12,13,14;S9)/S9(14)`, clamped outside its tabulation, and fixed background-A
CLASS/EPS collapse column `S(x)>0`, put `A=4/(3*(3*log(2)-pi/2))`. On footing `f`, define

    C_f(x,L) = A * (L*q(x))^(5/4) * S(x) / floor_f,
    Lcrit_f(x) = (floor_f/(A*S(x)))^(4/5) / q(x).

The corrected switch is `C_f(x,L)>1`. For every fixed x and L>0 this is equivalent to `L>Lcrit_f(x)`.
The scalar equality T is derived; it is never an independent input. A switch/core change cannot be split.

Finite computation, not a universal observational feasibility theorem: evaluate the existing levels
`L={3.75,3.9,4.0}` and the critical levels for the pre-existing CF2 threshold markers `x={12.1,12.2,12.3,12.5}`
on each footing. These markers are external cached-harness diagnostics, not necessary observed bounds on
the corrected model. The only proposed challenge point is `Lchallenge=Lcrit_canonical(12.3)`: its definition is
frozen now; it may be reported but its observational harness is not executed by this subagent. Alt uses the same
challenge L when its crossover is reported, rather than acquiring another fitted level.

## Fixed implementation and controls

Independently implement the recorded CL3 finite CLASS/EPS recipe: k in [1e-4,150] h/Mpc at 3000 log samples;
sigma squared at 191 log masses [7,16.5]; 3001 redshifts [0,30]; delta_c=1.686; half-mass coefficient 0.974;
virial overdensity 18*pi^2. Read the background-A parameters from the F3 JSON. Use existing full precision
S9 `cf_by_mass` values. Reproduce all six cached constant-L CL3 roots within 0.002 dex before interpreting new roots.

Checks, fixed before execution:

1. All constant-L roots reproduce to 0.002 dex.
2. Algebraic `Lcrit` substitution yields C=1 to relative 1e-12 at all four diagnostic masses/footing.
3. Direct C>1 and L>Lcrit classifications agree at Lcrit*(1+-1e-6), including exact equality as floor branch.
4. New consistent roots reproduce prior independent native_l_t scalar roots to 1e-6 dex at the existing levels.
5. Roots are reported with all sign-changing brackets on the fixed 1001-point [9,16] grid. One bracket is a finite
   observation; global uniqueness is not inferred from a grid.
6. The canonical challenge is derived once from T*=12.3, and its canonical root reproduces 12.3 within 1e-6 dex.
7. Deterministic rerun JSONs must match; mutation divides q by two in the direct formulation only and must fail
   the independent Lcrit equivalence check.
8. Input hashes stable; observed peak RSS below 1 GB. No RLIMIT_AS claim on macOS. CPU/wall/thread bounds in manifest.

Frozen outcome interpretation:

- For fixed mass, monotonicity with L and the algebraic activation criterion are mathematical identities
  conditional on the declared positive inputs. Monotonicity of T requires monotonicity of `q^(5/4) S`, which is
  not assumed globally from a root grid.
- A challenge core-amplitude ratio `(Lchallenge/Lold)^(5/4)` quantifies the unavoidable linked tradeoff. It cannot
  determine an observed residual without a new grade at that L.
- Cached CL2/CL3/CF1/CF2/CL1 score patterns may demonstrate empirical tension or contradict a universal inference;
  they do not establish that no corrected-model L works. Report exact cached cases separately.
- The proposed challenge is a diagnostic definition, not a permitted new empirical refit. User authorization is
  limited to the existing three L cells; do not run a new observational cell here.
- If all three corrected primary cells fail, the strongest conclusion is failure of this existing discrete set.
  A whole-family exclusion needs an actual bound or an independently authorized discriminating cell.

## Assumption ledger

- RAW: existing measured-file provenance and job artifacts are not reprocessed here.
- FRAMEWORK-NATIVE numerical output: X48 finite ng48 S9 medians, including their estimator and extrapolation.
- FRAMEWORK-NATIVE phenomenology: eta(c), positive surface-density floor, fitted kappa=1/2; these have no
  condensation derivation established here. Both a0 footings remain separate.
- ANALYTIC MODEL ASSUMPTIONS: EPS half-mass formation recipe, spherical collapse delta_c and 18*pi^2.
- CMB PARAMETER CALIBRATION: F3 background-A CLASS/primordial parameters; scalar reproduction does not validate physics.
- CACHED EMPIRICAL HARNESS: CF2 switch window, CL2/CL3/CL1/CF1 score lines mix raw measurements, survey calibration,
  and framework ingredients. They are read as existing model-dependent results, not treated as universal inequalities.
- No particle interpretation, standard-MOND prescription, imported c-M relation, PM simulation, or native L derivation
  is introduced. No claim that the theory is closed or that data favor the framework.

Computation and proof reviews are independent of the calibration/held-out implementation agents, but share these
declared inputs. All numerical conclusions are conditional on floating arithmetic and CLASS version.

## Amendment A1 (pre-result): coordinator authorization of the sole challenge

After the criteria were written, and before this lane's new arithmetic, the coordinator authorized one additional
existing-parameter challenge if all three existing primary L values fail: `Lcrit_canonical(12.3)` as already defined
above. The calibration and held-out agents may be asked to grade that same fourth L. It is explicitly a refit of
the existing sole L using the old empirical T midpoint. It is neither a new independent T nor a blind prediction.
This lane computes and reports the value only; the coordinator dispatches any observational run. No other
challenge, target adjustment, or scan is authorized. This supersedes only the challenge authorization boundary above.

## Amendment A2 (pre-result): preserve the actual pipeline representations

Source inspection identifies three collapse-column/floor representations. Add cheap scalar diagnostics for all:
X43 background A and B each use fresh CLASS/EPS, with SI floor converted using PC=3.0857e16 and MSUN=1.98847e30;
old CL3's root solver instead uses PC=3.0856775814913673e16; X53 uses the cached five-point background-A collapse
table with log-log interpolation/extrapolation and its own Gpc=4.30091e-3 plus rounded PC. Preserve all conventions,
label each root, and do not treat one root as a replacement for each pipeline's direct flag. The sole challenge
is defined from X43 background A with X43's actual floor conversion, not the old CL3 diagnostic conversion.
Use the same CLASS/EPS discretization for background B from its existing F3 parameter vector. Check background-A
scalar collapse columns against all five X43 cached values to relative 1e-10. Old independent native_l_t roots
are compared using old CL3's floor convention. This is a representation audit, not a physical rule change.
