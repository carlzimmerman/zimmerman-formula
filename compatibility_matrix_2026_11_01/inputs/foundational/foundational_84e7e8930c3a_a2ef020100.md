# TP02 matter coupling: two derived states, neither the assumed cold waterbag

The canonical-K SU(5) action supplies definite occupied-state couplings. Its massive eigenmodes have field-dependent **rest and kinetic** energies; retaining rest energy reverses the scalar-source sign compared with a kinetic-only treatment of the light adjoint branch. Its complex flat coordinate supplies a genuine inverse-square phase-charge energy, but with density exponent two, rather than the former five-thirds waterbag. These are constructive, different material states, not a derivation of the old portal by renaming it.

The actual phase-current state remains pressure-rich in the weak-coupling examples, including RG wavefunctions and the known finite occupied heavy-relaxation square. An explicit massive eigenmode occupation has a small cold/stable local window, but is charged and has no derived conserved species number or lifetime. No cosmological abundance, new interaction, observed coefficient, gravity completion or physical halo is selected.

Base checkpoint `40d43dbb8a9f1517e214302380f7659df7626e6a`; active dirty shared checkout. All route writes are confined to this directory. Immutable TP01 artifacts and actual input hashes identify the tested versions. No production simulation, old source edit, download, dependency installation, queue modification or Git mutation was performed by this route.

## Derived coupling and reciprocal ledger

For a slowly varying local eigenmode, E_a(p,s)=sqrt(p^2+m_a(s)^2). Changing eigenvectors adds derivative connections/transitions; ignoring them is a stated WKB/adiabatic restriction. For explicit occupations,

    epsilon_m=sum integral f_a E_a,
    P_kin=sum integral f_a p^2/(3E_a),
    C=partial_s epsilon_m=sum integral f_a m_a m_a,s/E_a.

The scalar source is U_s+C=0. The same action gives the particle force -(m m_s/E)grad s and the energy exchange epsilon_m_dot+3H(epsilon_m+P_kin)=C s_dot, with the scalar ledger carrying the opposite work. It is not a free energy-transfer efficiency. For epsilon(n,s)=U+epsilon_m, the relaxed pressure is

    P=n epsilon_n-epsilon,
    dP/dln n=n^2[epsilon_nn-epsilon_ns^2/epsilon_ss].

This general Schur complement replaces the old Uss>3Us formula for a different occupied state. Rest energy cancels from the direct ideal-gas pressure at fixed s but still controls the scalar force and the relaxed susceptibility. It cannot be removed from that force by changing the pressure's vacuum reference.

The actual unbroken SU(3) Weyl masses obey m_H m_L=q^2 and logarithmic slopes ±M/sqrt(M^2+4q^2), with M=3hX and q=2lambda a. A field-independent rest energy plus independently varying inertial mass is not the canonical one-mode dispersion. This rules out that identification for free/WKB eigenmode occupations; it is not a no-go over all interacting many-body phases. The action-derived phase current below is one explicit collective alternative, with a different equation of state.

Details, current normalization, gauge/number limitations and the massless sectors are in [DERIVATION.md](DERIVATION.md).

## Actual phase current and its coldness

Writing T=R exp(i theta), the classical phase current has n=q_theta=2R^2 theta_dot. Fixed charge gives epsilon=n^2/(4R^2)+U and therefore

    P=Us/2-U, D=Uss+2Us,
    c_IR^2=(Uss-2Us)/(Uss+2Us).

This is a coherent rotating field state; its coefficient scales as n^2, not rho^(5/3). R(T)=2 means q_R=2q_theta. The SU(5)^2 U(1)_R anomaly coefficient is 5-5+5=5, so the classical current is not an exact quantum protected abundance. Timelike gradients, radial adiabaticity and the missing quantum/current lifetime remain explicit.

At weak trial couplings h=lambda=e in {.03,.1}, f=Q=1 and the inherited comparator g=sqrt(29/200)e, the exact one-loop spectrum gives the following *same dimensionless* values at both points:

| X/Xmin | Vacuum-subtracted w_ex | IR c_s^2 |
|---:|---:|---:|
| 1.0001 | 0.999800 | 0.999600 |
| 1.01 | 0.980108 | 0.959847 |
| 1.05 | 0.902592 | 0.795383 |
| 1.12 | 0.774048 | 0.485379 |
| 1.20 | 0.636843 | 0.076328 |
| 1.21339321, compressibility boundary | 0.614799 | 0 |
| 1.30 | 0.478251 | -0.569792 |

The phase branch loses positive compressibility at 1.21339320552, rather than the old waterbag's 1.17729961112. A vanishing sound speed at the boundary does not make its energy cold: its excess pressure is still about 61% of its excess energy. Radial stability survives to the reported canonical ratio 1.85336181. The bounded evidence does not certify an exhaustive search over disconnected branches.

There is also a structural restriction before quartic occupied matching: on a connected stable two-derivative phase branch with F>0,a=(lnF)'>0, the chemical potential omega^2=Us/(aF) is nondecreasing. Integrating DeltaU=integral omega^2 dF yields w_ex>=F0/(2F-F0). For canonical F this is 1/[2(X/Xmin)^2-1], about .514 at the short branch endpoint. Thus selecting a different charge within such a short stable connected field range cannot by itself yield cold excess energy. The bound's hypotheses and its exclusion of the quartic correction are explicit in [OCCUPIED_DERIVATION.md](OCCUPIED_DERIVATION.md).

## RG angular metric retained, not replaced by a canonical guess

For actual matched angular coefficient F(s), put a=(lnF)'. The derived phase pressure and sound speed are

    P=Us/a-U,
    D=Uss+(a-a'/a)Us,
    c_IR^2=[Uss-(a+a'/a)Us]/D.

The five-case weak e=.03 test used the RG researcher's pinned U,F interface, including its nonzero a'. F is the running-wavefunction part, with finite threshold angular kinetic corrections still absent; U omits the unknown finite two-loop remainder. The values below are numerical sensitivity checks, not complete matching-error bounds.

| Potential/metric scheme | Matching-scale factor | X/Xmin at pressure boundary | w_ex there |
|---|---:|---:|---:|
| Fixed exact one-loop | 1 | 1.21339320552 | 0.6147991 |
| One-loop RG flow | 1 | 1.21521836072 | 0.6126003 |
| Two-loop-flow RG plus required scale logs | 0.5 | 1.21362615200 | 0.6144595 |
| Same | 1 | 1.21362615202 | 0.6144595 |
| Same | 2 | 1.21362615046 | 0.6144595 |

At X/Xmin=1.2 in the central improved case, w_ex=.6368693 and c_IR^2=.0772879. Actual a differs from two by about 1.2e-9, and a' is about -6.2e-10. These were retained. Repeating the central state at 64 RK steps/60 digits changes c_IR^2 by 1.05e-18. Direct differentiation of P(n) agrees with the general-F formula to about 3.5e-7 relative. These are implementation checks; the uncomputed finite matching terms are not thereby bounded.

## Finite occupied heavy relaxation, including the quartic term

The follow-up used full-spectrum normal tadpoles to retain the complete known contribution

    Omega=U_RG-omega^2F_RG
          -1/2[CWa^2/Haa+(CWb-omega^2 60b0)^2/Hbb].

The square was included exactly once. It contains the vacuum shift, induced angular coefficient and occupied omega^4 term; omitting the last term would omit part of the same matching. Let V=U_RG+deltaU_vac, F=F_RG-CWb(60b0)/Hbb and J=(60b0)^2/Hbb, so Omega=V-F omega^2-J omega^4/2. The calculation uses n=-Omega_omega and P=-Omega+Vvac. The fixed-charge Hessian is D=Omega_ss+Omega_somega^2/(-Omega_omegaomega), and c_IR^2=n Omega_ss/[omega(-Omega_omegaomega)D]. No unmatched radial kinetic coefficient was invented.

At e=.03, three finite log-field stencils h=.01,.005,.0025 give endpoint ratios 1.2126320820, 1.2126320815, 1.2126320805. The last two differ by about 1.0e-9; the appropriate reported precision is **1.21263208**, not an exact root certificate. At the finest stencil w_ex=.6156695, and at ratio1.2 w_ex=.6365065, c_IR^2=.0725675. The largest normal shift is 2.29e-6. Direct branch P(n) differentiation agrees to 1.4e-6 relative. The known finite contribution changes the endpoint slightly without making this charge state cold.

An optional *assumed free equilibrated* reservoir of the twelve massless unbroken gauginos contributes -omega^4/(32pi^2) to Omega. At this endpoint its excess-energy fraction is about 1.53e-19. Its constant quartic coefficient has no field derivative, so it leaves the computed Omega_ss endpoint unchanged in this approximation. This bounds only that named free reservoir at this state. No Goldstino occupation, gauge/IR equilibration, confinement or anomaly rate was inferred. Full finite angular two-point graphs and the finite two-loop potential remain missing.

## A genuinely mode-derived cold window, with explicit limitations

The light SU(3)-adjoint Weyl branch was populated as an instantaneous isotropic filled Fermi sphere, with degeneracy16 fixed by its eight gauge components and two massive spin states. This is an explicit trial state, not an abundance prediction or stable species number. Equal colour populations have zero mean charge but do not prove an asymptotic gauge-singlet state or an IR phase.

Solving the exact stationarity equation, retaining sqrt(p^2+m(s)^2), gives at both weak fixed-order coupling points:

| X/Xmin | p_F/m | w_ex | Formal relaxed c_s^2 | Radial D |
|---:|---:|---:|---:|---|
| 1.0001 | .04104 | .000288 | .000464 | Positive |
| 1.001 | .08848 | .001075 | .001628 | Positive |
| 1.01 | .19141 | .002380 | .002360 | Positive |
| 1.01932024 | .23918 | .001871 | 0 | Positive |
| 1.05 | .33132 | -.002794 | -.013334 | Positive |
| 1.20 | .54124 | -.039599 | -.135929 | Positive |

The relaxed-compressibility boundary is 1.01932023621; the radial endpoint is 1.55670273405. The latter is a different branch problem from phase charge. Required n was solved from force balance, not selected to obtain a desired density. The equal-coupling dimensionless agreement follows from the exact fixed-order rescaling c=e/31, masses and momenta proportional to sqrt(c), n proportional to c^(3/2), and occupied/vacuum-subtracted energies proportional to c^2. Making e smaller alone does not enlarge this dimensionless window.

At every sampled state the full scalar source is negative and the kinetic-only source is positive. For example at e=.03,X/Xmin=1.05 they are -1.15435e-10 and +3.70812e-12. This sign reversal is structural for a decreasing mass: partial_s(E-m)=m_s(m/E-1) has the opposite sign from partial_s E=m_s m/E. Removing the rest term would change the force problem.

The light Weyl mass has a lighter positive adjoint scalar branch, with scalar/fermion mass ratio about .793 near the pressure boundary; decay to that scalar plus the massless Goldstino is kinematically open. The model provides no conserved number for these interacting eigenmodes, and no lifetime was calculated. This cold local window is therefore a conditional occupation diagnostic, not a stable dark-matter-particle proposal. Its extension using a matched occupied spectrum, gauge/IR state and collision/decay dynamics remains open.

## Evidence and continuation

All four v2 runs completed with unchanged before/after input hashes and passing intended controls:

- [run_native/result.json](run_native/result.json), [manifest](run_native/manifest.json): actual masses, rest/kinetic sources and canonical phase state; 6.1 s, about18 MB RSS. Exact block masses and analytic mass derivatives agree below1e-40;50/70digit checks pass.
- [run_gas/result.json](run_gas/result.json), [manifest](run_gas/manifest.json): occupied-mode pressure/radial endpoints and density identity;6.1 s, low memory. The direct dn/ds identity agrees to6.5e-10 relative.
- [run_rg_phase/result.json](run_rg_phase/result.json), [manifest](run_rg_phase/manifest.json): five RG scheme/scale cases with actual angular F;54.8 s, about18 MB RSS.
- [run_occupied/result.json](run_occupied/result.json), [manifest](run_occupied/manifest.json): complete known heavy square, three field stencils and optional gaugino reservoir;34.3 s, about84 MB RSS. All conditions recorded, including the negative-compressibility continuation; no failed physical samples were dropped.

Each numerical command uses one conventional numerical thread and supported wall/CPU caps; no unavailable affinity or address-space cap is claimed. Every successful manifest was validated against current hashes. Contract files, implementations and full numeric state tables are retained. This route had no failed execution attempts.

The physical question remains open. The old kinetic-only waterbag is not obtained from the explicit states derived here. The native charge state is pressure-rich on the sampled stable branch, while the occupied massive-mode gas has a small cold window whose lifetime/gauge/current assumptions are unproved. Full finite angular matching, finite two-loop vacuum graphs, a gauge/IR/occupied-state construction, quantum charge lifetime and gravity must be supplied before any of these local results becomes a physical halo prediction. These are named continuation obligations, not permission requests or a theory-closure claim. Fresh coordinator cross-review is separate from these author calculations.
