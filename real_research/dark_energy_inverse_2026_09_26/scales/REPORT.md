# Scale inverses, coupling conventions and what they can identify

Checkpoint CD26-3, base `7daaa5426076a2d78a50f3316007c7093255ce9a`, on the existing dirty CD26-2 workspace. This is an inverse audit of specified relations, not a derivation of the vacuum source, a new fit, or a claim that the gravity theory is complete. Existing framework files are retained unchanged by this audit. Concurrent work advanced HEAD; frozen evidence snapshots were captured at `ecffd2af3623ff3e32318234fd51e1fac50b9126` and are mapped to their original paths and hashes in `source_snapshot_inventory.json`.

The main finding is that the scale dictionary is invertible **only after its independent coefficient, coupling and branch choices are fixed**. Rewriting the same scale as density, curvature, horizon size or temperature supplies no additional evidence about its physical origin. In particular, the archived κ estimates already use a cosmological vacuum-density calibration; inserting the same estimates into the inverse density formula merely returns that calibration.

## 1. Units and the actual domain

Use measured local `G_N>0`, `c>0`, `κ>0`, and vacuum **mass-equivalent density** `rho_vac>0` in kg/m³. Define energy density `epsilon_vac=rho_vac c²` in J/m³ and, only for a true `w=-1` vacuum, pressure `p_vac=-epsilon_vac` in Pa. The proposed relation is

    a0 = κ c sqrt(G_N rho_vac) = κ sqrt(G_N epsilon_vac),
    a0² = κ² G_N (-p_vac)              [only after p_vac=-epsilon_vac].

The factor `c` belongs in the mass-density form and disappears in the energy-density/pressure forms. Calling all three quantities “vacuum energy” without their units obscures this distinction. If the primary postulate is the pressure relation for a component with `p=w rho c²`, it determines `-w rho`, not density alone. The separate evolving-component audit must supply `w`.

The forward square root also exists at `rho=0` and then gives `a0=0`, but logarithms, reciprocal radii and κ recovery are singular there. At `κ=0`, the forward law is zero for every density and has no inverse. Negative density has no real positive scale in this branch; replacing rho by its absolute value would be a different law. Squaring loses the sign of a signed acceleration or κ. The physical acceleration here is a nonnegative magnitude, and κ is fixed positive. A squared Friedmann equation likewise has expanding and contracting signs; `H_vac` below denotes the positive vacuum rate.

Dimensional analysis with only `(c,G_N,rho)` forces powers `(1,1/2,1/2)` but leaves κ free. The explicit exponent matrix in the order `(mass,length,time)` has determinant `-2`; reordering rows can give `+2`. Only its nonzero magnitude matters. This is uniqueness under the stated dimensional premise, not an equation of motion fixing κ.

## 2. Both directions, with the coupling ratio retained

Let `g=G_cosm/G_N>0`. Assume the vacuum contribution to the background equation is

    H_vac² = (8pi/3) G_cosm rho_vac.

This is a background-law assumption. It is not implied by the galactic acceleration relation. Define the **geometric vacuum curvature** `Lambda_geom=3H_vac²/c²` and the separate **Newton-normalized density parameter** `Lambda_N=8pi G_N rho_vac/c²`. Then `Lambda_geom=g Lambda_N`.

| Quantity | Forward form | Inverse, with other symbols fixed |
|---|---|---|
| Mass density | `a0=κ c sqrt(G_N rho)` | `rho=a0²/(κ² G_N c²)` |
| Energy density | `a0=κ sqrt(G_N epsilon)` | `epsilon=a0²/(κ² G_N)` |
| Vacuum pressure | `a0²=κ² G_N(-p)` | `p=-a0²/(κ² G_N)` |
| Coefficient | `a0=κ c sqrt(G_N rho)` | `κ=a0/[c sqrt(G_N rho)]` |
| Geometric curvature | `a0=κ c² sqrt(Lambda_geom/(8pi g))` | `Lambda_geom=8pi g a0²/(κ² c⁴)` |
| Vacuum rate | `a0=κ c H_vac/sqrt(8pi g/3)` | `H_vac=sqrt(8pi g/3)a0/(κ c)` |
| Horizon ratio | `Z_H=c H_vac/a0=sqrt(8pi g/3)/κ` | `κ=sqrt(8pi g/3)/Z_H`; `g=3κ²Z_H²/(8pi)` |

For each fixed positive κ, c and G_N, the map `rho -> a0` is one-to-one on nonnegative densities; the square inverse is unique. It does not jointly determine rho and κ. Similarly, a measured `Z_H` determines `κ/sqrt(g)`, not κ and g separately.

Consequently `κ=1/2` gives

    a0 = c² sqrt(Lambda_geom/(32pi g)),
    Z_H² = 32pi g/3,
    Lambda_geom (c²/a0)² = 32pi g.

The familiar `a0=c² sqrt(Lambda/(32pi))` and `Z_H=sqrt(32pi/3)` additionally require `g=1` if Lambda is geometric. The corresponding Newton-density Lambda_N relation retains `32pi` without that assumption. Alternatively one can define `κ_cosm=a0/[c sqrt(G_cosm rho)]=κ/sqrt(g)`, but that is a different coefficient convention and must be named.

### Same-action normalization example

CD26-2's specified action gives

    G_N=G_bare/C,
    G_cosm=G_bare/(1+3B/2),
    g=C/(1+3B/2).

If `Lambda_bare` is the constant in that action and its vacuum mass density is `Lambda_bare c²/(8pi G_bare)`, then

    Lambda_N=Lambda_bare/C,
    Lambda_geom=Lambda_bare/(1+3B/2).

Thus the bare action constant, a density converted using measured G_N, and the curvature read from vacuum expansion are three different quantities in this family. The algebraic control `C=.5,B=.1` gives `g=10/23`; that particular family failed its preferred-frame test and is **not** a viable measured cosmological coupling. It is used here only to test whether inverse formulas silently assume equality of the couplings.

## 3. H_vac is not H_total

Define `Omega_vac=H_vac²/H_total²` on a chosen expanding background. Then

    H_vac=H_total sqrt(Omega_vac),
    a0 = c H_total sqrt(Omega_vac)/Z_H,
    H_total = Z_H a0/[c sqrt(Omega_vac)].

The last inverse requires independent information about Omega_vac and the background law. The relation `H_total=Z_H a0/c` is valid only in the vacuum-only limit Omega_vac=1. If other components have nonnegative contributions, `0<Omega_vac<=1` and `H_vac<=H_total`. Curvature or additional gravitational terms require their own convention for the fraction; it should not be equated automatically with a density fraction formed using G_N.

Using the archived `Omega_vac=.685`, substituting total H for vacuum H overstates the acceleration by `1/sqrt(.685)=1.208244...`; reading total expansion as a vacuum density overstates that density by `1/.685=1.459854...`. These are convention controls, not new observational discrepancies.

The June `real_research/FRAMEWORK.md` explicitly investigates total-density `a0(z) proportional to H_total(z)` and matter-density alternatives. The later `THE_CLEAN_PATH_2026-09-26.md` instead adopts a vacuum-pressure scale, approximately constant for w=-1. These are different physical postulates, not two rearrangements of one equation. In particular, the old `STATE_OF_THE_FRAMEWORK.md` consequence `H0=Z a0/c` cannot be carried unchanged into the later vacuum reading. The paper `zimmerman_framework_for_physicists.tex`, lines 120–133, already states the correct H_vac/H0 distinction for its g=1 convention. No existing file was edited here.

## 4. Horizon and temperature inverses

Define three distinct lengths:

    R_acc=c²/a0,
    R_dS=c/H_vac=sqrt(3/Lambda_geom),
    R_star=c/sqrt(G_N rho_vac)=κ R_acc.

Their ratios are

    R_acc/R_dS=Z_H,
    R_star/R_dS=sqrt(8pi g/3),
    a0=κ c²/R_star.

At κ=1/2 the last equation is `a0=c²/(2R_star)`. That does not make R_star a de Sitter horizon or a black-hole radius. It is a density timescale multiplied by c. Calling `1/sqrt(G_N rho)` a “free-fall time” fixes a convention; the collapse time of a specified gravitating system can carry an additional numerical factor. No horizon identification follows merely from the same physical units.

For standard de Sitter/Unruh thermometry of an appropriate relativistic probe, take as input

    T_dS=hbar H_vac/(2pi k_B),
    T_U(a0)=hbar a0/(2pi c k_B).

Then

    T_dS/T_U(a0)=Z_H,
    R_dS=hbar c/(2pi k_B T_dS),
    a0=2pi c k_B T_U/hbar.

These formulas do not prove that the clock sector has the required quantum state or detector response. Equating the two standard temperatures gives **a0=c H_vac**: their factors of `2pi` cancel. The archived k03 proposal `a0=c H_vac/(2pi)` instead gives `T_U/T_dS=1/(2pi)` and requires the extra identification

    κ=sqrt(8pi g/3)/(2pi)=sqrt(2g/(3pi)).

For g=1 this is `.4606588659...`. It is a competing coefficient proposal, not the consequence of simply equating the standard temperatures. Reproducing its old likelihood comparison is outside this audit.

For the also-recorded detector input `T_eff=[hbar/(2pi c k_B)]sqrt(a_detector²+(cH_vac)²)`, the nonnegative inverse exists only for `T_eff>=T_dS`:

    a_detector=sqrt[(2pi c k_B T_eff/hbar)²-(cH_vac)²].

If `a_excess=(2pi c k_B/hbar)(T_eff-T_dS)>=0`, the equivalent inverse is `a_detector=sqrt(a_excess²+2cH_vac a_excess)`. This is a precise temperature dictionary, not a derivation of galactic dynamics from a detector temperature.

Use separate symbols: `Z_H=cH_vac/a0` is not the independent four-form stiffness `Z_q` in `P(q)=Z_q q²/2`. The quoted `Z_q/beta²≈7.96` must not be identified with `Z_H≈5.7888`. The current clean-path note already makes this distinction following commit `738216fbd`; the archived k04 evidence and kappa-closure README still use bare Z for the stiffness. This audit preserves those historical sources and translates their notation explicitly.

## 5. Identifiability and the circular inverse

Fix c and independently measured G_N. For input coordinates `(ln κ,ln rho,ln g)`, the logarithmic rows for `(ln a0,ln H_vac)` are

    J = [[1, 1/2, 0], [0, 1/2, 1/2]].

Rank is two. Adding Lambda_geom, R_dS, T_dS and Z_H computed from those scales leaves the rank at two. The exact null direction is `(1,-2,2)`, corresponding to

    κ -> lambda κ,
    rho -> rho/lambda²,
    g -> lambda² g,                 lambda>0.

Both a0 and H_vac stay unchanged. With G_N also unknown there is an additional product degeneracy `G_N rho`. An independently measured rho would add a third rank direction; a rho already calculated from H_vac and an assumed g would not.

The archived κ estimates are defined using a fiducial rho:

    κ_hat = a0_hat/[c sqrt(G_N rho_fid)].

The putative inverse then gives identically

    a0_hat²/(κ_hat² G_N c²)=rho_fid.

This is not an independent detection of vacuum density. Treating a0_hat and κ_hat as independent measurements would also mishandle their covariance. At fixed c,

    d ln rho = 2 d ln a0 - 2 d ln κ - d ln G_N.

For a κ calibrated from the same a0 and fixed rho_fid, the first two terms cancel. A genuinely informative density inverse needs an independently fixed κ or an action that predicts it, plus the coupling convention. The k01 additive-vacuum-zero obstruction remains relevant: rearranging quantities does not remove its independent constant.

## 6. Archived numerical controls and uncertainty provenance

The run reuses k01's `a0=9.3619e-11 m/s²`, κ=.5, rounded `c=2.998e8`, and `G_N=6.674e-11`. This is the canonical footing **defined using the vacuum normalization**, not a new measurement of that normalization. It returns

    rho=5.8443811e-27 kg/m³,
    epsilon=-p=5.2529321e-10 J/m³,
    Lambda_N=1.0906900e-52 m^(-2).

At g=1, `H_vac=1.8076805e-18 s^(-1)`, `Z_H=5.7888100`, `R_dS=1.6584789e26 m`, and `T_dS=2.1975293e-30 K`. The temperature calculation uses the SI-defined Planck and Boltzmann constants; it is a unit conversion under the assumed thermometry. Holding the same rho and κ while setting the algebraic action control g=10/23 instead gives `Z_H=3.8170283` and `Lambda_geom=4.7421304e-53 m^(-2)`. No cosmological data have been refitted to this coupling change.

The historical κ summaries retained by the run are:

| Stored summary | Source status |
|---|---|
| `.465 +/- .076` BTFR | kappa_closure/k01–k03 and archived BTFR audit; subsequent H0-convention audit discusses an offset |
| `.551 +/- .043` distance-free | historical kappa_closure value; later audits identify missing convention/systematic terms |
| `.55 +/- .17` distance-free | later 2026-09-22 and 2026-09-26 synthesis; not interchangeable with the old narrow error bar |

The H0-convention audit reports that the “distance-free” theorem covers common distance rescaling, whereas changing only Hubble-flow galaxy distances is not that operation. The quoted summaries therefore are not independent, universally convention-free likelihood inputs. This work neither reruns their estimators nor pools their errors. The archived k03 H0-based reconstruction `9.3625e-11` differs slightly from k01's rounded canonical input; that rounding is recorded rather than converted into new evidence.

## 7. Reproducibility and scope of the certificates

The accepted `run_005/manifest.json` records 34 exact SymPy identities, exact log-rank/nullspace checks, the dimensional exponent system and two coupling controls. Manifest validation passed against frozen source snapshots. The first job had a 60-second cap and failed because SymPy did not recognize an expanded positive perfect square; that development record is retained in `run_001`. The implementation explicitly factors that root argument under its stated nonnegative domain. `run_002` completed the scientific checks but its manifest became stale when a concurrently edited source note changed. `run_003` passed but declared stale software versions; `run_004` failed on a runtime-metadata alias typo after the scientific checks. None is the accepted record. No old data-fitting script is executed.

The accepted run explicitly uses Xcode Python 3.9.6 and SymPy 1.14.0, with the executable and actual imported versions also written inside `results.json`. This avoids reliance on changing shell Python selection. Inputs, outputs, actual argv and hashes are recorded. The numerical values above are algebraic controls, not interval estimates or likelihoods. See `EVIDENCE.md` for accepted records and the retained development-attempt limitations.

`ScalesInverse20260926.lean` formalizes the nonnegative square-root branch, the density inverse and its uniqueness, joint scale degeneracy, a log-null direction, the coupling factor in Z, the total/vacuum rate inequality, thermometric equality, calibration circularity, and coupling/horizon ratios. The accepted compile is `lean_attempt3.log`, with `lean_record.json` recording the command, toolchain, source/log hashes and all 12 statements. It exited 0 in 82.421 seconds with no warnings/errors/admissions and only `propext`, `Classical.choice`, `Quot.sound`. The statements have nonempty hypotheses: unit positive coefficients provide algebraic witnesses, and `(H,H_vac,Omega)=(2,1,1/4)` witnesses the strict-rate assumptions. Earlier timeout and redundant-tactic error logs remain development records, not accepted certificates. Their failed source revisions were not separately archived; those logs cannot be reproduced from the final source, and no source snapshot is being reconstructed from their hashes. No Lean theorem supplies the vacuum equation of state, a physical origin for κ, a cosmological fit or a quantum-temperature mechanism.

What is currently identified is a proposed **vacuum-linked acceleration scale**, conditional on a negative-pressure vacuum and coefficient/coupling choices. That terminology describes the tested relationship. It does not rename all dark energy as a known microscopic substance or establish why its magnitude exists.
