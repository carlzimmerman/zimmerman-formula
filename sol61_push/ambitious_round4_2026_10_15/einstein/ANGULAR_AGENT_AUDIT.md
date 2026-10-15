# Independent audit of EINSTEIN-JOIN-1

15 October 2026. Primary verdict: **proved as written for the specified static
Einstein/current/gauge/uncharged-wall branch**. I independently reconstructed
the normalized-frame stress, proper-stock equations, conservation identity,
both Israel jumps, wall mass/load elimination and the uniform contraction
bounds. No sign or source/domain counterexample survived those checks. This
is a separate same-team mathematical audit, not external peer review or a
formal proof certificate. It establishes neither perturbative stability nor
formation/empirical success.

Audited immutable revisions:

- PROOF.md: `8a73f618c321c7e8af1b4abe1d8bc1e4168923b42084d495e3f10d14dc97c8cf`.
- check_einstein.py: `d113ef071444233926410296d94633100f06188f112a5aa17e9568da06766296`.
- inputs/definitions.json: `c51c9fd81183ebacba6243bec1c993a312f745271c8ef4a66260879b821f74ce`.
- run_v3/results.json: `f2ca726269b6699bf6bb04ebdf800846a275e42e096166ec589dcb6c9bc8b01a`.
- run_v3/manifest.json: `def5a3f7d66aaad68d2bcf7b9b2ca5190fe3e4ad97b3c8c8a8a7de70e2507225`.

Claim card: for every eta=c^-2 in [0,10^-4], fixed central proper densities,
EOS coefficients, critical zeta=sqrt(4piG), R=1 and the selected occupied
constitutive phase, the full static radial equations admit a unique solution
in the stated four-function box. For eta>0 a positive selected NG tension
joins it to an ordinary-orientation timelike wall and an asymptotically flat
Maxwell/RN exterior. Uniqueness is within this box only. Tension and proper
stocks are outputs along the branch; the theorem does not continue at fixed
independently prescribed tension and stocks.

## Normalized current and Hilbert stress

At fixed current vector density in a diagonal rest metric, the normalized
current has U^t=1/a, irrespective of the current density magnitude. Thus
E=F_tr/(ab), while the measure is ab z1 z2. Differentiating the actual gauge
action with respect to a,b,z1,z2 gives the logarithmic responses
Le-ED, Le-ED, Le, Le. In mixed orthonormal components these are
(-H,-H,Le,Le). This argument varies the frame normalization with the
metric; it does not substitute a held aether vector.

For first number-current variations at B=0, normalization projects delta U
orthogonal to U. The electric frame derivative is parallel to U and
therefore vanishes on that projection. Every first beta B^2 derivative
vanishes, including its stock derivative. The ordinary chemical potentials
are consequently those of epsilon_a, and the fluids supply their separate
perfect-fluid stresses. The diagonal metric test is sufficient here because
static spherical symmetry and time reversal eliminate the off-diagonal
background stress. The resulting full stress is epsilon_mat+H,
p_r=P-H, p_t=P+Le; internal/gauge energy and all pressures gravitate.

## Independent reconstruction of the bulk equations

For F=1-2G eta m/r, the tt Einstein equation gives
m'=4pi r^2[rho_b+rho_c+eta(P+H)]. The rr equation gives
nu'=G eta[m+4pi eta r^3(P-H)]/(r^2 F). Both agree with the proof.

The proper spatial volume is 4pi r^2dr/sqrt(F), giving
S_a'=4pi r^2rho_a/sqrt(F). Maxwell variation counts only the actual dark
charge, Q'=zeta S_c'. Thus D=Q/(4pi r^2); replacing S_c by a coordinate
rest mass would be incorrect in this GR problem.

The radial current Euler equations are
w_b'=-(c^2+w_b)nu' and
w_c'=-(c^2+w_c)nu'+zeta E/sqrt(F).
The 1/sqrt(F) force factor follows from converting the local proper electric
force to a coordinate radial gradient. Combining these with
H'=E(zeta rho_c/sqrt(F)-2D/r) cancels the charge exchange term and gives
p_r'=-(epsilon+p_r)nu'+2(p_t-p_r)/r. Hence the remaining angular Einstein
equation is consistent rather than an independent missing source condition.
The two chemical first integrals also differentiate to these exact equations.

## Independent reconstruction of both junctions

With a common unit normal pointing from interior to exterior,
K^theta_theta=sqrt(F)/R and K^tau_tau=sqrt(F)nu'. The Lanczos convention
[K^i_j]-delta^i_j[K]=-8piG S^i_j/c^4 with S^i_j=-sigma delta^i_j
therefore gives [K^i_j]=-4piG sigma delta^i_j/c^4. Writing k=4piGsigma/c^4
and a=sqrt(F_-), b=sqrt(F_+) yields exactly

    a-b=kR,       b nu'_+-a nu'_-=-k.

Squaring the angular equation gives

    m_+-m_-=m_w a-Gm_w^2/(2c^2R),  m_w=4pi sigma R^2/c^2.

Adding the Maxwell tail Q^2/(8pi c^2R) then produces equation (16), including
its c^-6 wall self-binding term. Interior Misner-Sharp mass and exterior ADM
mass are distinct and correctly counted.

Taking the normal Einstein constraint difference, or directly eliminating
the time jump with the rr bulk equation, gives

    P-Delta H=sigma[a nu'_-+2a/R-3k/2].

This is precisely equation (17). Its flat limit has P-Delta H=2sigma/R,
and its sigma^2 coefficient is negative. Reversing the normal on just one
side would spoil both the mass formula and this pressure limit; that wrong
orientation is not used. Wall energy and negative surface pressures are
both present, rather than only adding a surface rest mass to a TOV interior.

Primary-source convention check: I opened the original 14-page scanned
Israel paper, *Singular Hypersurfaces and Thin Shells in General Relativity*
(1966), DOI 10.1007/BF02710419, and checked section 3's minus-to-plus normal
and section 5 equations (19)-(20). Its surface-density units translate from
G/c^2 to G/c^4 when S denotes energy density. The general jump convention
agrees with the formula above. The specific charged-fluid/NG load is derived
here, rather than attributed to the paper. Checked 15 October 2026 from
https://images.shoutwiki.com/gamebm/0/02/Israel1966_Article_SingularHypersurfacesAndThinSh.pdf .
No local full-paper cache was created and no novelty search is claimed.

## Uniform contraction and wall root

The variables v=3m/(4pi r^3), y=3Q/(4pi zeta r^3) remove the center's
apparent divisions. Both averaged maps have continuous center limits. The
function box is convex; the maximum norm scales v,y variations by 100 but
leaves the box itself narrow. This is a legitimate norm choice, not a claim
that v,y vary over an interval of width 100.

The strict self-map margins hold on the whole box: 0.99(1+f)>6.3;
1+f+eta(P0+Hcap)<6.4; 0.99f>5.30; f/F_*<5.37. The electric term cannot
reverse the inward dark integrand because
6.3-5.37/[(1-X)F_*]>0. Its omission for the upper enthalpy-drop bound is
in the correct direction. C=v/3+eta(P-H)<3 gives an integrated inward drop
below 25G, within both one-percent enthalpy margins.

For the differential estimates, |delta v|,|delta y|<=100N lead to
|delta F|<(2e-9)r^2N and |delta D|<=rN/75. The bounds on inverse F and
H_D=E then agree with the stated rows. The force variation is below
6e-6 rN; the electric-force y derivative uses (1-x)^-2, not merely
(1-x)^-1. The v row is below .07, y below .061, and both enthalpy rows
below .001. Thus the global norm contraction constant .08 is supported by
uniform derivatives and a self-map; it is not inferred from IVP convergence.
The smooth/continuous radial integral equations give the regular center and
solve the full bulk equations on [0,1].

The actual positive wall load and A_w>2F_* imply a weak root below
sigma_test=.51P0; the quadratic is strictly increasing throughout that
interval. b=a-kR remains positive, so the selected branch is an ordinary
wall rather than a horizon/wormhole branch. The exterior has bounded finite
ADM mass, and F_out>=1-2G eta M/r>0 for r>=1 in these quantitative scales.
Matching the interior additive lapse constant then fixes the induced metric
and the normalization at infinity.

## Obligation matrix and computation scope

| Obligation | Verdict |
|---|---|
| Number-current frame normalization and pure-electric Hilbert stress | passed by independent variation |
| Proper dark charge/rest stock and both fluid force equations | passed |
| Full anisotropic Einstein conservation | passed |
| Both Israel jumps and common-normal sign | passed; original convention checked |
| NG wall mass and ADM Maxwell tail | passed |
| Uniform self-map and all contraction rows | passed |
| Positive weak tension root and ordinary exterior | passed |
| Fixed tension continuation across eta | out of scope, explicitly disclaimed |
| Numerical IVPs as illustration only | correctly restricted |
| GR stability, hyperbolicity, formation and phenomenology | out of scope |

I inspected definitions, code and run_v3's scientific output and manifest.
The Mathbox validator run with repository root confirms current input/output
hashes. I did not rerun an identical IVP suite. The finite 128 checks support
their implemented identities and bounds; the existence theorem rests on the
separate analytic contraction reconstructed above. Rounded scalar edge data
and 80-digit junction residuals do not establish 80-digit stellar profiles,
and the proof does not claim that they do. The two retained failed controls
are implementation-domain/comparator repairs, not hidden mathematical
counterexamples.

No required static implication remains missing in the stated theorem. The
next substantive mathematical task is a GR perturbation/free-boundary
analysis with metric constraints and radiation; none of the hybrid radial
or angular energy results can be imported as that theorem without a new
argument. Chosen EOS, phase/contact and tension selection remain physical
inputs, not consequences of the static construction.
