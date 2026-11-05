# Cosmology, core formation and mathematical-closure audit

The central surviving result is narrower than a closed gravitational theory: the record contains exact conditional semidiscrete entropy-preservation results, several finite numerical diagnostics, and an unresolved one-field AeST formation problem. No reviewed route supplies both a healthy action and the observed galaxy/cluster configuration from cosmological initial data. Kappa remains fitted. Canonical and alternate acceleration footings are kept separate throughout.

The most useful new finding is that AN1's large Gaussian K11 failures are almost exactly the behavior of independent, correct dust-shell solutions. They should not be interpreted as evidence of numerical runaway or physical failure. This does not grant AN1 a pass: its frozen verdict stays NO VERDICT, the cluster top-hat still misses its check, and the full finite-Q0 theory was not evolved.

## Scope, provenance and limits

Requested window: base `4cba03defe795a2f8e40bc181d8bd7c1a5362752` to initial HEAD `c8b2586bb1921cff3bcb75feae827233ce62db8b`. `coverage.json` enumerates **916 changed artifacts, 134 Markdown files, 30 changed README/STATUS entrypoints, 15 changed lanes** after removing spurious ARGON matches. Current summaries in all 15 lanes were reviewed, along with historical CSM1 and DF1 and the top-level theory statement. The CSM2 accumulation was read selectively, including initial estimator/finite-search results, its numerical-certificate progression, and latest coverage; this is not a line-by-line re-audit of all 682 historical lines. The exact scope is an entrypoint and bottleneck audit, not a fresh validation of all 916 artifacts or every supporting theorem.

Changed-lane artifact counts: AN1 55; AN2 19; AR1 30; AS1 9; AS2 18; AS3 19; BOLTZ1 9; CSM2 26; DF2 101; DF3_barotrope 21; DF3_fluid_next_gates 40; RF5 39; RF6 31; WF1 45; X48 454. CSM1 and DF1 are relevant unchanged foundations, outside that changed count.

Applicable proof-audit and computation-audit skills were read; research-program was read for route discipline. This is a fresh subagent reconstruction of selected raw formulas/code, not an assertion that independence guarantees correctness. No existing project file was modified. No production simulation, watcher, or running job was touched. All new files are under `/private/tmp/cosmology_core_audit_20261103/`.

The shared HEAD advanced during review. The completed independent run records observed HEAD `8e5b84e6a12bf0367eb4c4e520373db540a49783`, dirty. Its eight project inputs and independent script have before/after SHA-256 observations in `manifest.json`, all unchanged. That current-file evidence is distinct from the pinned historical diff inventory.

- Command: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 /private/tmp/cosmology_core_audit_20261103/audit_checks.py`
- Validation: `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py /private/tmp/cosmology_core_audit_20261103/manifest.json --root /`
- Run status: **completed**, about 1.6 s; validator: **valid evidence record**. The filesystem root is `/` because authorized outputs are in `/private/tmp` and inputs remain in the project; paths in the manifest are relative to that root. First manifest-format validation rejected absolute paths; corrected format and rerun validated. No scientific result changed.
- Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4. ODE checks use binary64 DOP853, tolerance around 1e-11, no outward-rounded certificate.
- Script SHA-256: `654449d1eb37f42052a74359bba0485b8d88fcc1516d616ecf324e29a577b6d3`.
- Results SHA-256: `252d245392e585b03e60bd10eae8e5da4f45a2fd4fd4f9b6472e09a3b828f905`.
- Manifest SHA-256: `a391bd9e3e89adf09f939c14c29347d8225a8bb2b4326f6853ede74df9f1045e`.

All relative locators below are within `/Users/carlzimmerman/new_physics/zimmerman-formula/`.

## Four bottleneck audits

### 1. AN1 origin force, exact sphere and K11

**Claims audited:** the historical early central focus was a discretization defect; the revised Gaussian non-homology check diagnoses an excessive single-shell runaway.

**Verdicts:** the center-cell diagnosis is correct; using the Gaussian K11 discrepancy as a runaway diagnostic is **refuted by a finite, valid dust benchmark**. This is a correction to interpretation and future test design, not a retroactive change to frozen grades.

For uniform density in the first cell, M(<r)=M_cell(r/r_cell)^3. The old interpolation uses M_cell(r/r_cell), so the force is excessive by (r_cell/r)^2: exactly 4 at a half-cell baryon node. Refining the grid preserves that ratio. Thus apparent convergence in N cannot detect this error. Compare old `AN1_aest_nonlinear_dust/an1.py:191–226` with corrected `an1_v3.py:23–51` and `:54–75`; correction is disclosed at `README.md:5–19`.

I independently integrated the scale-free dust equation for x=r/q,

    x'' = -(4*pi*G*rho_m0/3)/x^2 + Omega_L*H0^2*x,

with the declared Zel'dovich start at z_i=20 and d=0.2030, without importing any project solver. It gives t_focus=4.643900733 Gyr and z_focus=1.361704885. Subtracting the rounded box mean 0.0082*d gives 4.701047569 Gyr and z=1.341524377. This corroborates the corrected AN1 benchmark and the Nov3 AN2 sphere-lag diagnostic, not the old z~2.93 result. Sources: `rebuild_2026_10_22/AN1_aest_nonlinear_dust/an1.py:11–47`; `rebuild_2026_10_22/AN1_aest_nonlinear_dust/an1_v3.py:384–408`; `rebuild_2026_10_22/AN2_aest_3d_fold/diag_a2/SPHERE_LAG_NOTE.md:5–8`.

For the actual Gaussian profile, each shell has a different enclosed contrast. I integrated four exact dust shells q_k=k*2*q_t/N, k=1,2,3,5, with the Gaussian mean overdensity from the declared input. I stopped when the first shell reached x_1/a=1e-3, matching K11's diagnostic threshold. The resulting quantity is precisely |r_1*k/r_k-1|=|x_1/x_k-1|.

| N | Independent exact-dust max deviation | Saved AN1 P1 galaxy max deviation | Frozen limit |
|---:|---:|---:|---:|
| 300 | 0.908392739 | 0.908083044 | 0.02 |
| 1200 | 0.540161467 | 0.540618805 | 0.02 |
| 4800 | 0.082572804 | not compared | 0.02 |

The first two independent values match the production diagnostic within 0.00046 absolute, despite exceeding the frozen limit by factors 45 and 27. A peaked profile is not homologous near its first focus. In the local dust asymptotics t_c(q)=t_c(0)+Aq^2, r~q[t_c(q)-t]^(2/3), so fixed-shell ratios can depart dramatically from homology even before crossing. K11 conflates physical differential focusing with a numerical artifact. Its exact implementation is `an1_v3.py:435–486`; saved values are `an1_v3_checks.json`, `K11.rows`; current narrative is `README_V3.md:6–9,79`.

**Remaining numerical issue:** the cluster top-hat at N300 gives 0.036961091 against 0.02; this is not removed by the Gaussian comparison. The N1200 top-hat value is 0.002422635. Baryon stopping and the finite-mu hold term must be separated from the exact dust reference. Do not simply delete K11 or loosen its threshold. The replacement should compare each shell with its own exact characteristic trajectory for an unforced Gaussian and require homology only for a genuinely homogeneous dust sphere.

**Current safe AN1 statement:** 61/68 rows fold, 5 never collapse, 2 reach z=0 oscillating, 0 settle in the corrected reduced implementation; this is a finite diagnostic, still NO VERDICT. Both oscillating rows lapse the quadratic-K approximation. All seven z=0 rows have at most 0.001 of the baryons stopped on the target profile, so none is an observed galaxy/cluster ready to grade. `README_V3.md:11–42,59–75,92–94`.

### 2. AN2 capture and geometry checks

**Claim audited:** M_d(<R_test)>=M_ph(<R_test) at any step establishes a possible formed well.

**Verdict:** **refuted as a formation/capture diagnostic** by the unperturbed cosmological background. The project's current README already recognizes the problem; independent arithmetic establishes its size and two-footing behavior.

At z=20 and R=1350 kpc, using the declared mean field/baryon densities, a perfectly homogeneous universe has

    M_d = 3.1687347217e15 Msun,
    M_b = 5.9228686386e14 Msun,
    true excess field mass = 0.

Applying the same g_law and M_ph calculation as the code gives M_d/M_ph=**5.234967752 canonical** and **4.622077865 alt**. Both pass M_d>=M_ph despite no object and no capture. The code uses total counts in a fixed physical aperture, `AN2_aest_3d_fold/an2.py:400–406`, and stores the first threshold hit at `:487`. The force calculation already uses background-subtracted density, so the observable diagnostic and dynamical source are inconsistent in this respect.

A corrected future diagnostic should report excess charge relative to the same background convention as the field equation, a Lagrangian captured fraction after turnaround, and the flux through the chosen material/control surface; require the baryonic target profile to exist before comparing against a static law. Merely adding an arbitrary redshift cut would avoid one false positive without proving capture.

Current AN2's six unresolved check categories (KZ, KE2, KT, KB, KE, KG) and 16–18% sphere lag prevent a model grade. The relative shape shifts at mu56.6 track the dust ellipsoid within about 3 percentage points, but cannot establish that actual 3D folds no later than the continuum spherical solution. `README.md:3,7–20,39–43`. KT/KB also reveal that a test demanding a finite fold time cannot be evaluated on valid no-fold rows; those rows need a finite-time trajectory/Jacobian error diagnostic, not a made-up fold time.

The Nov3 D0–D4 sphere-lag experiment is already specified in `diag_a2/SPHERE_LAG_NOTE.md:10–25`. It is not a new proposed route here, and I did not launch or disturb it.

### 3. RF5/BOLTZ1: a timing fit is not a field-action closure

**Claim audited:** RF5's growing comoving cold mass can be represented by one healthy shift-symmetric P(X) barotrope.

**Verdict:** **refuted within the single-barotrope hypotheses**, not for every multifield or shift-breaking action.

For dust born from an unclustered vacuum reservoir,

    rho_c = rho_c0*a^-3*S(a),
    rho_total' = -3*rho_c,
    P_total' = rho_c*S'/S,

where prime is d/dln a. Therefore c_a^2=P_total'/rho_total'=-S'/(3S). A monotonically increasing S has negative c_a^2. For the declared tanh step S=(1+tanh x)/2, x=(ln a-ln a_on)/w, w=.05,

    c_a^2 = -(1-tanh x)/(3w),

which equals -6.666666667 at the midpoint and tends to -13.333333333 on the early side. This independently reproduces the sign and range quoted at `BOLTZ1_covariant_closure/README.md:7,21–23`. It assumes the stated dust+vacuum release, not arbitrary CPL fluctuations or a second independent entropy degree of freedom.

RF5 demonstrates a finite, family-dependent early-dust window z_on>=3e4 on its registered grid, not a universal cosmological onset bound. Both footings share its linear surface because a0 is absent. Its forest channel fails its own adequacy gate even in the dust limit and cannot be used as an exclusion curve. BOLTZ1's mu->infinity comparison shows that the forest mismatch persists without turn-on; going to larger z_on is not a missing rescue. `rebuild_2026_10_22/RF5_growth_native_yardstick/README.md:10–22,37–55`; `rebuild_2026_10_22/BOLTZ1_covariant_closure/README.md:38–57`.

The polytropic pressure floor R=pi/mu at mu_BBN=1.24e8/Mpc is 0.0253 pc. This rules out a kpc pressure core within that literal quadratic form and BBN assumption. It is not a lower sound-speed bound and does not exclude all nonquadratic K, nonbarotropic stress, or multistream completions. Those require a selected action; the zoo cannot be merged into one likelihood.

### 4. X48: what the floor theorem actually proves

**Normalized theorem:** for the exact finite-shell transport ODE with positive masses, valid geometry and the given outward heat law, a seed K>=k0 on a central prefix of mass M_s gives, on any smaller prefix M_c<M_s,

    K_i(t) >= k0*((M_s-M_c)/(M-M_c))^3

for every later valid time. Together with the stated mechanical energy and cold compression threshold, the argument gives global continuation for each fixed N. It does not give bounds uniform in N on the geometry or prove that the specified cold data create the seed.

**Verdict:** **proved as written for the conditional semidiscrete preservation implication**, after independent reconstruction of its signs, comparison flow, entropy inequality, index bound, and fixed-mesh continuation argument. This pass does not extend to every downstream conditional energy lemma, which was reviewed through its current status and prior audit rather than independently reproved here.

Dependency chain in `.../floor_theorem/preservation_route.md`:

1. Face luminosity is increasing in supplying K and decreasing in receiving K, so the heat ODE is cooperative (`:80–107`).
2. Source-free auxiliary flow on the actual geometry preserves descending K ordering and has max<=k0 (`:109–136`). Actual heated K need not preserve the order.
3. Its entropy sum dm*(K/Kstar)^(1/3) cannot decrease; zero-temperature initial data are handled by positive approximation (`:138–164`). Geometry is prescribed and entropy has no W_t term.
4. Entropy from the original seeded prefix plus ordering/max bound gives the exact bound above (`:166–230`). A strict mass margin is necessary.
5. Tail preservation protects every warmed cell on a fixed mesh. Unwarmed cells have compression at most1/tau below the density gate; internal energy diverges as r_1^-3 against gravitational energy at worst r_1^-1, preventing finite-time collapse on fixed N (`:232–310`). Constants may deteriorate with N.

For seed mass 10% and protected mass5%, the guaranteed floor is only 0.0001457938475*k0. For seed25%, protected5%, it is 0.009330806240*k0. These are bounds, not the measured equilibrium K~0.349624.

The actual missing implication is **uniform finite-time seed production from the declared virgin collapse**. The proposed sufficient condition C>=4 on a central quarter during one common interval would yield (64/125)T^3(1-2T), but no such common interval has been proved for all N. N32..1024 startup samples do not supply it. `floor_theorem/README.md:53–83,113–129`.

The latest density/collar theorem proves a conditional Y_inner<=Cs^5 and weighted compression-square<=Cs^6 under a pre-existing tight prefix bound. It cannot close that same prefix assumption: small weighted L2 permits a concentrated origin spike, and an interior cutoff does not improve the outer edge of its hypothesis. The all-p heat remainder and prefix propagation remain open. `density_closure_2026_11_01/STATUS.md:8–48`; `pointwise_bootstrap_2026_11_01/STATUS.md:7–18`. This is a proof gap, not a counterexample to the specified cold IVP.

The physical model includes rho_q, tau, D, ell_g and gate/damping constants in addition to the a0 normalization; its positive stiffness, finite cores and exact quiet gate do not derive those parameters or show that real forest histories lie in the inactive region. `entropy_transport/README.md:49–70,108–117,142–144,207–214`. The parked owner decision remains in force; this review did not restart that program.

## Synthesis of other covered lanes

| Lane | What survives | What must not be promoted |
|---|---|---|
| CSM1 | Correcting core/switch identity destroys the previous joint calibration; alternate fixed UFD construction has two exhaustive failing states | Not a no-L theorem for canonical or all halo models. README:3–40,51–63 |
| CSM2 | Binning alone changes first -2 crossing drastically in2/3 test profiles; 15 registered L levels fail necessary cuts; latest group interval covers L[2.62,3.08] within fixed analytic numerical scope | No globally certified continuous-L exclusion, robust native L, or physical closure. README:7–39,53–74,672–682 |
| X48 production | Finite concentration measurements and failed inner/mid cluster keys under specified recipes | Grid-redrawn realizations confound force-resolution convergence; first-crossing estimator instability invalidates an unqualified concentration lower-bound/convergence claim. README:142–161,190–213,217–241. A5_RESULT:5–7 concerns superseded floor rule |
| RF6 | Realistic measured gas leaves cluster softening short at current ng64 eta | Ceiling cells with stipulated coupling/load are not a derived mechanism; prior SPARC needs are stale after floor removal. README:8–14,35–59 |
| AR1 | Isotropic action-conserving adiabatic response improves live agreement and lifts Upsilon by~0.09 | Does not cure tilt/LITTLE THINGS/cluster profile; at least one frozen baseline check misses. README:7–33,45–55,74–80 |
| AS1 | Powered photometric isolation bins favor law-like slope; cleaner samples are not powered and lean differently | Slope alone does not fix amplitude, environment, or absolute fit. Frozen mutation was incorrectly specified. README:5–8,25–41 |
| AS2 | Explicit finite grammar has no all-gate pass; parameter-budget obstruction is real in that grammar | Not an action-space no-go: health usually ND, QUMOND SX absent, enumeration cap partial, PPN extension assumed. README:7–27,67–71 |
| AS3 | Static/moving source branches differ singularly; current report locates a unit-constraint quadratic-term defect in old v9 PPN calculation; exact GR geodesic branch exists up to caustic | Zero moving PPN coefficients do not restore the galaxy law. New scalar corner inherits growth and H4 failures. README:3–18,22–48,50–65. Not independently symbolically rerun here |
| DF1 (foundation) | Seven tested fixed shapes fail the registered requirements | Does not exhaust history-dependent mechanisms or prove a unique EOS; scatter model affects shape significance. README:16–37,45–55,87–96 |
| DF2 | Five of ten barotrope cells pass its gate1 requirement map | Gate1 is not nonlinear exclusion, retention, BBN or forest viability; background w neglected and some controls amended after result. README:7–19,38–57 |
| DF3 (both) | Tested five barotropes do not jointly supply disc exclusion and cluster mass under fair-share/static assumptions | Collapsed unresolved Newtonian core is not a physical solution. Fermi-gas TOV completion is one high-density completion, not determined by a low-density polytropic exponent alone. Static failure is scoped to stipulated share/envelope and selected relativistic continuation |
| WF1 | Wave pressure can remove field from small discs; finite linear gate1 pass begins m~1e-25eV | Selected state still fails clusters/groups; core-envelope prescription and nonformation limit remain; chosen k_half~0.31h/Mpc has ungraded severe forest suppression. README:5–17,19–45 |
| BOLTZ1 | Pure P(X) dust limit reproduces linear harness; no healthy single-barotrope realization of RF5 step | Neither native zoom profile nor imposed core rule follows past the first field caustic. README:14–23,25–35,56–64 |

A specific overreach deserving correction in future synthesis: `DF3_fluid_next_gates/README.md` states the Gamma5/3 core exceeds its own relativistic limit using a Fermi-gas TOV completion with the same low-density K. A Newtonian EOS P=K*rho^(5/3) does not uniquely specify a relativistic epsilon(n) at high density. The particular Fermi completion may be a useful comparator, while the claimed universal GR removal is conditional on that choice. The huge Newtonian compactness and empirical mass failure survive without the stronger assertion.

## Proper next route: current one-action formation, with discriminating work before new production

These recommendations preserve the Nov1 retirement and Nov2 one-action lane. They do not reinstate X48 stress, a separate cold component, or a particle interpretation. They are a complement to the coordinator's distinct action-consistent source-filter route. Within the one-field branch, the following are jointly required work packages, not three supposedly independent solutions.

### A. Full finite-Q0 validity and characteristic route

The changed premise is to keep the aether-current/fast-sector dynamics that AN1/AN2 discard, rather than refining the same Q0=infinity model. Start from the exact selected one-field action, including the second-order unit constraint exposed by AS3, and derive the constrained principal symbol around actual occupied homogeneous and held-profile states. Retain the full conserved charge n_eff=n+divPi/Q0. Recover the current slow limit analytically, with its domain expressed by genuine dimensionless derivative and velocity ratios.

**First discriminating test:** evaluate the full constrained kinetic and characteristic matrices along one mu0.1 held profile and one mu56.6 incipient collapsing profile, including a finite-Q0 sweep only as a validity comparison, not fitting. Reject a claimed usable regime if kinetic signature or characteristic speeds fail, or the small-parameter hierarchy reaches order one before the physical event. Existing H1 vacuum and H4 negative-charge obstructions must remain explicit; a finite-Q0 calculation that merely rediscovers them without a changed admissible background is not a rescue.

A specific present mismatch must be fixed in the derivation: frozen AN1 criteria:31 define Q0_need=max(g/(c*v)), but `an1_v3.py:267–274` uses V_c=sqrt(g*r), not actual flow speed. A circular-speed proxy cannot certify a slow-flow approximation near turnaround. Current all-shell reported demands reach Q0~300/Mpc on the BBN floor, far beyond C7's0.1/Mpc. This is not proof that finiteQ0 cures anything; it shows the discarded sector is uncontrolled in the regions deciding some folds.

Only if that test permits an admissible regime should a bounded finite-Q0 IVP be built. Use exact sphere and shell-by-shell Gaussian references, plus a smooth manufactured occupied perturbation exciting the retained current; do not inherit the Gaussian homology check.

### B. Charge reachability instead of a planted static well

The new question is whether the same conserved field charge can reach the law-supporting held branch with the necessary extra cluster mass, from an admissible cosmological state, before characteristics cross. AN1 establishes that placing a field on a held branch can survive a small radial kick; that is not a basin-of-attraction or capture result. Its current formation starts stop with hardly any baryons on the target profile.

**First discriminating test:** derive and verify the exact control-volume charge balance, including background subtraction and boundary flux, on a blank FRW control and one smooth spherical infall. Blank FRW must have exactly zero excess/captured mass on both footings; the current AN2 diagnostic fails by factors5.235/4.622. Then compare, at the same physical time and formed baryonic profile, (i) actually bound excess charge, (ii) charge required for the law, and (iii) remaining cluster excess. Require conserved total charge and energy accounting before interpreting a successful local force fit.

A useful analytic discriminator before costly evolution is the constrained energy/charge budget of the target held profile versus the initial configuration plus permitted boundary flux. If the target is inaccessible under those invariants, no amount of angular-resolution refinement can make it an attractor. If accessible, an actual finite-time transport mechanism remains to be demonstrated. This is distinct from adding a separate dark fluid or choosing an arbitrary retention function.

### C. Cosmologically matched initial data, rather than generous dust initialization

Current AN1/AN2 use dust growing-mode velocities and native dust-limit peak spectra at z20 even where the action's earlier growth is suppressed. That was disclosed as generous, and it is neither an action-derived initial state nor a prediction. RF5's turn-on fit and the no-action fluid requirement maps cannot supply this missing transfer function.

**First discriminating test:** for the same selected action and finiteQ0 branch surviving A, propagate the field, baryon and current transfer functions to z20 at the two tested mass scales. Compare all of density amplitude, relative velocity and charge/current correlations with the frozen dust initialization. Test the real primordial normalization, not a rescaled peak chosen after failure. If no allowed primordial cell makes a nonlinear peak while meeting the same CMB/linear observations, the late collapse route is removed before expensive3D work. If it does, those matched profiles become the only production initial data for B.

This is a new load-bearing input rather than another mu/shape grid. It can falsify reachability independently of whether a hydrostatic equilibrium exists. It does not inherit a forest bound from RF5's failed-adequacy forward model.

## Highest-value reporting changes

1. Separate a failed frozen control from physical falsification. K11 has an independently exhibited wrong expectation; the current NO VERDICT record stays, but do not count it as an independent kill of the action.
2. Use one current successor table per lane. AN1's original all68fold statement and the theory statement's old floor/success table are historical, while X48's A5 is complete despite its README's pending block. The current owner decisions and branch status must lead.
3. Treat conservation identities, conditional theorems, finite-grid facts, observational grades and full-action validity as different evidence types. Passing many arithmetic/mutation checks cannot bridge a missing physical or continuum implication.
4. Do not spend another cycle on unchanged CSM interval tiles, a larger action grammar with inherited labels, or more post-warming X48 grids as though these address the current one-action bottleneck. They are distinct scoped historical tasks, not missing evidence for finiteQ0 formation.
