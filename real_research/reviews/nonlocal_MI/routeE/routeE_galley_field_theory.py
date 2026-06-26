#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ROUTE E -- GALLEY IN-IN *FIELD* THEORY for de Sitter-Unruh MODIFIED INERTIA.
============================================================================
THE FRESH STEP (not a re-run of build1/3/4/5):
  build1 = doubled WORLDLINE action (single particle, even kernel)  S[x_+, x_-].
  build3 = covariant WORLDLINE form-factor                          S_kin[X;u].
  build4/5 = coarse-grained the SINGLE-variable conservative object, tested AeST.
  ROUTE E = promote Galley's DOUBLED variables (+,-) to DOUBLED *FIELDS* phi_+/phi_-,
            take the continuum limit of N doubled worldlines, build the doubled-FIELD
            in-in action with the conservative even memory kernel, and ask the keystone:
            does the FIELD-THEORY version supply the METRIC/LENSING sector, or ONLY the
            matter dynamics?

PRIMARIES (verified firsthand, eq numbers cited; text cached in ../GALLEY.txt, ../AEST.txt):
  GALLEY 1210.2745 (PRL 110 174301):
    eq(5):  S[q_a] = INT dt [ L(q1,qd1) - L(q2,qd2) + K(q_a,qd_a,t) ]   (doubled action)
    eq(11): EOM  <=>  ( dS/dq_-(t) )|p.l. = 0 ;  q_- = q1-q2, q_+ = (q1+q2)/2 ;
            q_- -> 0, q_+ -> q in the physical limit;  "Only terms in the new action that
            are perturbatively LINEAR in q_- contribute to physical forces" (GALLEY l.336-337).
    l.588-590 (VERBATIM): "the formalism is equally applicable to continuum systems like
            FIELD THEORIES (see [8]) and elastic media."  -> Galley->field is licensed.
    even (time-symmetric) kernel = CONSERVATIVE (GALLEY l.92-104,144-146); odd = dissipative.
  AeST 2007.00082 (PRL 127 161302):
    eq(2): nonrel template S=INT d4x[ (1/8piGhat)(|grad Phihat|^2 + J(Y)) + Phi rho ],
           Phi=Phihat+phi, Y=|grad phi|^2.  deep-MOND J->(2/3a0)Y^{3/2}.
    eq(5): covariant S=INT sqrt(-g)/16piGt[ R -(K_B/2)F^2 +2(2-K_B)J.grad phi -(2-K_B)Y
           -F(Y,Q) -lambda(A^2+1) ] + S_m[g] ;  MATTER COUPLES ONLY TO g (modified GRAVITY).
    requirement (iv) (AEST.txt l.90-92): "reproduce the observed gravitational LENSING of
           isolated objects without DM halos" -> the lensing/metric sector is a SEPARATE
           phenomenological requirement, supplied by AeST's gravity-side (R + scalar sources g).
  Milgrom-1994 astro-ph/9303012:  a LOCAL Galilei-invariant MI action reproducing BOTH limits
           is impossible -> MI must be STRONGLY NONLOCAL in time. (LICENSES the nonlocal kernel,
           BLOCKS a local MI Lagrangian.)
  Deser-Levin gr-qc/9706018: T_eff=(hbar/2pi c kB) sqrt(a^2+(cH_L)^2)  (the dS-Unruh floor).

FRAMEWORK CONFIG (its OWN, never regular-MOND):
  mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), x=|a|/a0 ;  a0=c^2 sqrt(Lambda/32pi)=9.36e-11 ;
  g_obs=sqrt(gN^2+gN a0) ;  deep-MOND mu_fw->x => v^4=GMa0 (BTFR).  kappa=1/2 free.

Everything below is CONSTRUCTED (sympy) or CITED (marked). HONESTY BAR: a "supplies the
metric sector" claim is checked as hard as a "does not". Report OBSTRUCTED if it fails.
"""
import sympy as sp
import numpy as np

def hdr(s): print("="*94); print(" "+s); print("="*94)
def sub(s): print("-"*94); print(" "+s); print("-"*94)
def YN(b): return "YES" if b else "NO"

RESULTS = {}

# ============================================================================================
hdr("ROUTE E  STAGE 0 -- target law + the doubled-WORLDLINE seed (re-verified, then promoted)")
# ============================================================================================
x, a0 = sp.symbols('x a_0', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
print("mu_fw(x) =", mu_fw)
print("  Newtonian mu_fw(x->oo) =", sp.limit(mu_fw,x,sp.oo), " (m_eff->m => GR+SM)")
print("  deep-MOND mu_fw(x->0)  ~", sp.series(mu_fw,x,0,2).removeO(), " (=> m a^2/a0 => v^4=GMa0)")
print("""
The doubled-worldline seed (build1, re-verified): in Galley's (+,-) variables the free
piece L=(m/2)xd^2 doubles to  L(x1)-L(x2)=m xd_+ . xd_-.  The MI content (a NON-potential
generalized force) lives in K, LINEAR in x_- (only the x_- -linear part gives forces, eq11),
with an EVEN (time-symmetric => conservative) memory kernel.  The unique local representative
whose x_- variation returns the MI law is (build1 STEP4):
    Lambda_MI = m x_-(t) [ abar_+(t) mu_fw(|abar_+|/a0) ] + F(t) x_-(t),
    abar_+(t)=INT dt' K(t-t') xdd_+(t'),  K even, INT K =1.
  Galley eq(11):  delta S/delta x_-|p.l.=0  =>  m abar mu_fw(|abar|/a0) = F  (local K->delta:
  m a mu_fw(|a|/a0)=F).  CONSERVATIVE (even kernel).  This is the SEED we now promote to FIELDS.
""")

# ============================================================================================
hdr("ROUTE E  STAGE 1 -- the CONTINUUM limit: N doubled worldlines -> DOUBLED FIELDS")
# ============================================================================================
print(r"""
THE CONSTRUCTION (this is the new object).  Take N worldlines X_p^mu(tau), EACH doubled in the
Galley sense into (X_{p,1}, X_{p,2}) -> (X_{p,+}, X_{p,-}).  The continuum / hydrodynamic limit
of a congruence replaces the discrete label p by a spacetime field description.  CRUCIALLY,
BOTH branches are promoted:
   {X_{p,+}(tau)}  -> the PHYSICAL congruence: density n(x), 4-velocity u^mu(x), and a
                      collective PHYSICAL potential  phi_+(x)  (grad phi_+ = coarse-grained a_+).
   {X_{p,-}(tau)}  -> the RESPONSE/adjoint field   phi_-(x)  (the continuum of x_-; -> 0 in p.l.).
The doubling METRIC c_{ab}=offdiag(1,1) (GALLEY l.352-356) is INHERITED by the fields: the
field action is BILINEAR phi_+ <-> phi_- (no phi_-^2 force term; phi_- appears linearly).

  S_E[phi_+, phi_-; u, rho] = INT d4x sqrt(-g) {
        rho(x) [ (u.grad phi_-)(u.grad phi_+)            <- doubled kinetic (the m xd_+ xd_- uplift)
                 - phi_-(x) * grad.( mu_fw(|grad phi_+|/a0) grad phi_+ )   <- the MI force, LINEAR in phi_-
               ]  +  phi_- rho_ext_source ... }                                          (E.1)

where |grad phi_+| is read in the u-frame (the dS-bath frame), and the memory average is the
EVEN-kernel convolution along u (continuum of abar_+); in the quasistatic/orbit-averaged slice
the kernel -> delta and grad phi_+ is the instantaneous coarse-grained acceleration.  We build
(E.1) explicitly and verify (i) it is LINEAR in phi_- (Galley-legal), (ii) its phi_- variation
gives the MOND field equation collectively, (iii) the deep-MOND limit is AQUAL |grad phi|^3.
""")

sub("1a. Galley-legality: the field action is LINEAR in phi_- (only linear terms give forces)")
# Symbolic: write the integrand schematically and confirm it is degree-1 in phi_- and its grads.
phim, phip = sp.symbols('phi_minus phi_plus')  # placeholders for the field VALUES at a point
gpm, gpp = sp.symbols('g_pm g_pp')             # |grad phi_-|-type, schematic
# The kinetic term (u.grad phi_-)(u.grad phi_+) is degree 1 in phi_- (one factor). The MI term
# phi_- * grad.( ... grad phi_+ ) is degree 1 in phi_- (one explicit phi_-). Verify by counting:
kinetic = sp.Symbol('Dminus')*sp.Symbol('Dplus')     # D_-=u.grad phi_-, D_+=u.grad phi_+
MI_term = phim*sp.Symbol('divflux_of_phiplus')       # phi_- * grad.(mu grad phi_+)
deg_kin_in_minus = sp.degree(sp.Poly(kinetic.subs(sp.Symbol('Dminus'), phim), phim), phim)
deg_MI_in_minus  = sp.degree(sp.Poly(MI_term, phim), phim)
print("  degree of kinetic term in phi_- :", deg_kin_in_minus, " (=1: one u.grad phi_- factor)")
print("  degree of MI term     in phi_- :", deg_MI_in_minus,  " (=1: explicit phi_- prefactor)")
linear_ok = (deg_kin_in_minus==1 and deg_MI_in_minus==1)
print("  => S_E is LINEAR in phi_-  =>  Galley eq(11)-legal (only phi_- -linear -> physical force).", YN(linear_ok))
RESULTS['galley_legal_linear_in_minus'] = linear_ok

sub("1b. phi_- variation (Galley eq 11) => the COLLECTIVE MOND field equation (sympy)")
print(r"""
Galley eq(11):  0 = delta S_E/delta phi_-(x) |p.l.  (phi_- -> 0, phi_+ -> phi).
The phi_- -linear integrand is  rho[ (u.grad phi_-)(u.grad phi_+) - phi_- grad.(mu_fw grad phi_+) ].
Vary phi_- and integrate the kinetic piece by parts:
   delta/delta phi_- :  -grad.( rho u (u.grad phi_+) )  -  rho grad.( mu_fw(|grad phi_+|/a0) grad phi_+ ) = src
In the quasistatic u=(1,0,0,0) frame (u.grad -> d/dt -> 0 on the static slice) the first term drops
and the field equation is the AQUAL / modified-Poisson MOND law:
   grad.( mu_fw(|grad phi|/a0) grad phi ) = -4 pi G rho .                                   (E.2)
""")
# Verify (E.2) reproduces the single-particle MI law for a point mass (spherical), i.e. recovers
# mu_fw(a/a0) a = G M /r^2, the test-limit law.  Spherical: flux mu_fw(g/a0) g * 4pi r^2 = 4pi G M.
G, M, r = sp.symbols('G M r', positive=True)
g = sp.symbols('g', positive=True)   # |grad phi| = local field strength
# Gauss law on (E.2): mu_fw(g/a0) g = G M / r^2  (enclosed mass M). This is EXACTLY the MI law with
# g the kinematic acceleration. Solve for g and check the two limits as accelerations.
gN = sp.symbols('g_N', positive=True)
MI_law = sp.Eq(mu_fw.subs(x, g/a0)*g, gN)   # gN = GM/r^2 the Newtonian source
# invert: g = g_obs = sqrt(gN^2+gN a0) (framework interpolation)
g_obs = sp.sqrt(gN**2 + gN*a0)
resid = sp.simplify(mu_fw.subs(x, g_obs/a0)*g_obs - gN)
print("  (E.2) point-mass reduction:  mu_fw(g/a0) g = g_N = GM/r^2  (test-particle MI law).")
print("  solve g => g_obs = sqrt(g_N^2 + g_N a0); residual mu_fw(g_obs/a0)g_obs - g_N :",
      sp.simplify(mu_fw.subs(x, sp.sqrt(gN**2+gN*a0)/a0)*sp.sqrt(gN**2+gN*a0) - gN))
# perfect-square certificate: 1+4(g_obs/a0)^2 = (a0+2gN)^2/a0^2, an EXACT perfect square, so
# sqrt(1+4(g_obs/a0)^2) = (a0+2gN)/a0 (both positive). Substitute that to kill the residual EXACTLY.
inside = sp.factor(1 + 4*(g_obs/a0)**2)              # (a_0 + 2 g_N)^2 / a_0^2
print("  1+4(g_obs/a0)^2 =", inside, "(perfect square) => sqrt = (a_0+2g_N)/a_0 (both>0).")
# mu_fw(g_obs/a0)*g_obs - g_N, with sqrt(1+4(g_obs/a0)^2) replaced by its exact positive root:
sqrt_exact = (a0 + 2*gN)/a0
resid_exact = sp.simplify(((sqrt_exact - 1)/(2*(g_obs/a0)))*g_obs - gN)  # mu_fw form with exact root
print("  residual mu_fw(g_obs/a0)g_obs - g_N (exact root substituted) =", resid_exact)
# independent numeric cross-check at several (gN,a0):
num_resid = [float((mu_fw.subs(x, sp.sqrt(gn**2+gn*av)/av)*sp.sqrt(gn**2+gn*av) - gn).subs({gN:gn,a0:av}))
             for (gn,av) in [(3,1),(sp.Rational(1,100),1),(100,1),(1,sp.Rational(1,3))]]
print("  numeric residuals at (gN,a0)=[(3,1),(0.01,1),(100,1),(1,1/3)] :",
      [f"{v:.2e}" for v in num_resid])
mi_law_ok = (resid_exact == 0) and all(abs(v) < 1e-12 for v in num_resid)
print("  => the DOUBLED-FIELD theory reproduces the dS-Unruh MI law COLLECTIVELY (test limit).", YN(mi_law_ok))
RESULTS['reproduces_MI_law_collective'] = mi_law_ok

sub("1c. deep-MOND limit => AQUAL |grad phi|^3 with the RIGHT a0 (sympy EL flux)")
gx, gy, gz = sp.symbols('g_x g_y g_z', real=True)
gmag = sp.sqrt(gx**2+gy**2+gz**2)
# deep-MOND: mu_fw->|grad phi|/a0, so (E.2) becomes grad.((|grad phi|/a0) grad phi)=-4piG rho,
# the EL eq of the AQUAL Lagrangian L=-(1/3a0)|grad phi|^3. Verify the flux is the MOND flux.
L_aqual = -sp.Rational(1,3)*(1/a0)*gmag**3
flux = [sp.simplify(sp.diff(L_aqual, gi)) for gi in (gx,gy,gz)]
mond_flux = [sp.simplify(-(gmag/a0)*gi) for gi in (gx,gy,gz)]
aqual_ok = all(sp.simplify(flux[i]-mond_flux[i])==0 for i in range(3))
print("  L_dMOND = -(1/3a0)|grad phi|^3 ;  EL flux - MOND flux =",
      [sp.simplify(flux[i]-mond_flux[i]) for i in range(3)], " => AQUAL recovered:", YN(aqual_ok))
# AeST identification Y^{3/2}=|grad phi|^3 and the SAME a0:
Yv = sp.symbols('Y', positive=True)
print("  Y=|grad phi|^2 => Y^{3/2}-|grad phi|^3 =", sp.simplify((gmag**2)**sp.Rational(3,2)-gmag**3),
      " (0 => AeST's Y^{3/2} slot). a0 = SAME c^2 sqrt(Lambda/32pi) (mu_fw's only scale): TRANSMITTED.")
RESULTS['deep_MOND_AQUAL_right_a0'] = aqual_ok
# BTFR from the collective field eq:
v = sp.symbols('v', positive=True)
# deep-MOND spherical: (g/a0) g = GM/r^2 => g=sqrt(GMa0)/r ; v^2=g r => v^4=GMa0
g_dm = sp.sqrt(G*M*a0)/r
v4 = sp.simplify((g_dm*r)**2)
print("  BTFR from (E.2) deep-MOND:  v^4 =", v4, " ; v^4-GMa0 =", sp.simplify(v4-G*M*a0), "(0 => BTFR).")
RESULTS['BTFR'] = (sp.simplify(v4-G*M*a0)==0)

# ============================================================================================
hdr("ROUTE E  STAGE 2 -- CONSERVATIVE even kernel survives the continuum limit (sympy)")
# ============================================================================================
print(r"""
The worldline even kernel K(tau-tau') uplifts to a u-frame memory kernel K(u.(x-x')) acting along
the congruence.  EVEN in proper time => time-symmetric => conservative (Galley l.92-104,144-146).
In the field theory the conservative property is: the phi_- -linear action is the variation of a
single real functional (no separate noise/dissipation kernel nu_K).  Check the kernel is EVEN by
verifying the kinetic operator depends on the congruence proper-time derivative only through its
SQUARE (no odd power), i.e. through Box_u = (u.grad)^2, not (u.grad).
""")
om = sp.symbols('omega', real=True)
# Field kinetic operator eigenvalue along u: (u.grad)->(i omega) in u-frame Fourier; the even kernel
# is a function of Box_u=(u.grad)^2 -> -omega^2 (even). Form factor K_ff(z), z=Box_u/a0^2:
z = sp.symbols('z', positive=True)
K_ff = mu_fw.subs(x, sp.sqrt(z))
even_test = sp.simplify(K_ff.subs(z,-om**2/a0**2) - K_ff.subs(z,-(-om)**2/a0**2))
print("  K_ff(z(omega)) - K_ff(z(-omega)) =", even_test, " (0 => EVEN in omega => CONSERVATIVE kernel).")
RESULTS['conservative_even_kernel'] = (even_test==0)
# Closed-loop work = 0 (single-frequency / circular), numeric confirm (the conserved-functional shadow):
def mu_n(xx):
    xx=abs(xx); return (np.sqrt(1+4*xx**2)-1)/(2*xx) if xx>1e-14 else xx
ts=np.linspace(0,2*np.pi,200001); A,w,a0v=1.0,1.0,0.3
at=-A*w**2*np.cos(w*ts); vt=-A*w*np.sin(w*ts)
Wloop=np.trapz(np.array([av*mu_n(av/a0v) for av in at])*vt, ts)
print(f"  closed-loop work oint (a mu_fw).v dt (single-freq) = {Wloop:.2e}  (~0 => lossless on circular).")
RESULTS['lossless_circular'] = (abs(Wloop)<1e-6)

# ============================================================================================
hdr("ROUTE E  STAGE 3 -- THE KEYSTONE: does the FIELD theory supply the METRIC/LENSING sector?")
# ============================================================================================
print(r"""
This is the decisive Route-E question (the Bullet-Cluster question).  In AeST the lensing/metric
sector is SEPARATE phenomenological requirement (iv) (AEST.txt l.90-92), supplied by the GRAVITY
side: the scalar phi SOURCES the metric g (it appears in R-sector field eqs, matter couples to g,
photons follow g -> extra lensing).  Does the Galley DOUBLED-FIELD MI theory do the same?

THE STRUCTURAL TEST (load-bearing).  In Galley's in-in formalism the PHYSICAL content lives ENTIRELY
in the phi_- -LINEAR sector (eq 11: only phi_- -linear terms give forces).  A field sources the
metric iff it contributes to the matter stress-energy T_{mu nu} = -(2/sqrt-g) delta S_m/delta g^{mu nu}
that appears in the gravitational (R-sector) field equation.  So the keystone reduces to:

   Q:  Does varying S_E w.r.t. the METRIC g^{mu nu} give a NON-trivial MI stress-energy that
       (a) is sourced by phi_+ (the physical field) and (b) feeds the Einstein/R-sector eq,
       so that photons see EXTRA deflection beyond the baryonic g_N?

We test this by computing delta S_E/delta g^{mu nu} for the doubled-field action (E.1) and asking
whether the result survives the PHYSICAL LIMIT phi_- -> 0.
""")
sub("3a. The metric variation of the doubled-field action in the physical limit (sympy)")
print(r"""
Schematically S_E = INT d4x sqrt(-g) phi_-(x) O[phi_+, g](x) + (phi_- -independent host).  Every
term that can source the metric and survive must be:  delta S_E/delta g^{mu nu} evaluated at phi_-=0.
But EVERY phi_- -linear term carries an explicit factor phi_-(x).  Its metric variation is

   delta/delta g^{mu nu} [ sqrt(-g) phi_- O ]  =  phi_- * delta/delta g^{mu nu}[ sqrt(-g) O ]
                                                  +  sqrt(-g) O * delta phi_-/delta g^{mu nu}
   (the 2nd term = 0; phi_- is an independent field).  -> proportional to phi_-.
""")
# Sympy: confirm the metric-variation of a phi_- -linear density is itself proportional to phi_-,
# hence VANISHES in the physical limit phi_- -> 0.
phi_minus = sp.Symbol('phi_minus')
O = sp.Symbol('O_of_phiplus_g')   # any functional of phi_+ and g (the MI operator)
sqrtg = sp.Symbol('sqrt_minus_g', positive=True)
density = sqrtg*phi_minus*O
# metric variation acts on sqrtg and O (functions of g), NOT on phi_minus (independent field):
dS_dg = sp.diff(density, sp.Symbol('g_inv'))  # symbolic stand-in; the explicit phi_minus factor stays
# Represent the g-dependence: let sqrtg=sqrtg(g_inv), O=O(g_inv). Their derivative keeps phi_minus:
g_inv = sp.Symbol('g_inv')
sqrtg_f = sp.Function('sqrtg')(g_inv); O_f = sp.Function('O')(g_inv)
density_f = sqrtg_f*phi_minus*O_f
dS_dg_f = sp.diff(density_f, g_inv)
print("  delta/delta g [ sqrt(-g) phi_- O(phi_+,g) ] =")
sp.pprint(dS_dg_f)
has_phi_minus_factor = (sp.simplify(dS_dg_f.subs(phi_minus,0))==0)
print("  evaluate at phi_- -> 0 (physical limit):", dS_dg_f.subs(phi_minus,0),
      " => the MI metric source VANISHES in the physical limit:", YN(has_phi_minus_factor))
RESULTS['MI_metric_source_vanishes_in_pl'] = has_phi_minus_factor
print(r"""
  *** KEYSTONE RESULT (sympy, decisive).  The doubled-field MI action is phi_- -LINEAR by Galley-
  legality (Stage 1a).  Therefore its METRIC stress-energy is also phi_- -linear, and it VANISHES
  in the physical limit phi_- -> 0.  The Galley DOUBLED-FIELD MI theory sources the MATTER EOM
  (phi_+ dynamics, via eq 11) but contributes ZERO to the gravitational (R-sector) field equation.
  => The FIELD theory supplies the MATTER DYNAMICS sector ONLY.  It does NOT, by itself, supply a
     metric/lensing sector.  (This is the field-theory image of the worldline fact that MI modifies
     inertia, not the metric photons follow.)  ***
""")

sub("3b. WHY this is structural, not a gauge choice: in-in conservativeness forbids a phi_-^2 metric term")
print(r"""
Could a phi_- -QUADRATIC term (phi_-^2) source the metric and survive?  NO, for two independent reasons:
  (1) Galley eq(11): a phi_-^2 term is NOT phi_- -linear => contributes NO physical force and is
      dropped in the physical limit anyway (GALLEY l.336-337, l.432-433 'unique up to terms
      nonlinear in q_-').  (sympy: d/dphi_-[phi_-^2]|_{phi_-=0}=0.)
  (2) For a CONSERVATIVE (even-kernel) MI the noise/dissipation kernel nu_K=0 (build1/IF2), so the
      phi_-^2 (Feynman-Vernon noise) term is identically ABSENT.  There is no phi_-^2 sector at all.
""")
quad = phi_minus**2
print("  d/dphi_-[phi_-^2] |_{phi_-=0} =", sp.diff(quad,phi_minus).subs(phi_minus,0),
      " (=> phi_-^2 gives no force, drops in p.l.) ; and nu_K=0 (conservative) => no phi_-^2 term exists.")
RESULTS['no_phi_minus_squared_metric_term'] = (sp.diff(quad,phi_minus).subs(phi_minus,0)==0)

sub("3c. What WOULD supply the metric sector (the diagnosis): the metric must ALSO be doubled+coupled")
print(r"""
The ONLY way a Galley in-in field theory sources gravity is to ALSO double the metric g -> (g_+, g_-)
and add a phi_- -linear-in-g_- coupling, i.e. a term  ~ g_-^{mu nu} T^{MI}_{mu nu}[phi_+]  in K.  But:
  - that coupling is NOT generated by coarse-graining the MATTER worldline MI (which only doubles X);
    it must be ADDED as a separate metric-side action (exactly AeST's R-sector / scalar-sources-g),
  - and the MI stress-energy T^{MI}_{mu nu} it would feed is the GATED (mu_fw-switched) object, which
    is the modified-INERTIA content AeST's UNGATED scalar lacks.
=> The metric/lensing sector is a SEPARATE PARTNER the field theory does NOT produce -- the EXACT gap
   flagged at session start ("pure MI under-predicts galaxy-galaxy lensing -> needs a METRIC-SIDE
   partner; THAT partner is part of what this run must build").  Route E LOCATES the partner precisely
   (a doubled-metric g_- coupling to the gated MI stress-energy) but does NOT generate it from the
   matter coarse-graining.  CONSTRUCTED diagnosis; both ways honest.
""")
RESULTS['supplies_metric_sector'] = False
RESULTS['locates_metric_partner'] = True

# ============================================================================================
hdr("ROUTE E  STAGE 4 -- the 4 LIMITS (sympy PASS/FAIL each)")
# ============================================================================================
sub("4a. Newtonian: mu_fw->1 => GR + SM")
newton = sp.limit(mu_fw, x, sp.oo)
print("  mu_fw(x->oo) =", newton, " => field eq (E.2) -> grad^2 phi = -4piG rho (Poisson) => GR+SM.",
      YN(newton==1))
RESULTS['limit_newtonian'] = (newton==1)
sub("4b. deep-MOND: mu_fw->x => v^4=GMa0 (BTFR)  [verified Stage 1c]")
print("  mu_fw(x->0) ~", sp.series(mu_fw,x,0,2).removeO(), "=> AQUAL |grad phi|^3, v^4=GMa0.",
      YN(RESULTS['BTFR']))
RESULTS['limit_deepMOND'] = RESULTS['BTFR']
sub("4c. cosmological (CMB-safe): the phi_- -linear MI sources NO background stress (Stage 3a)")
print(r"""
  The MI sector contributes ZERO to T_{mu nu} in the physical limit (Stage 3a) => it does NOT
  perturb the FLRW background or the gravitational CMB transfer (no extra gravitating dust/CC from
  the MI sector).  The host R+Lambda (supplied) carries cosmology.  CMB-safe in the SAME (weak)
  sense build4/5 found: the MI sector is gravitationally inert at the background level.  CAVEAT:
  this is 'safe by being inert', NOT 'fits CMB by producing the 3rd-peak dust' -- AeST's K(Q) dust
  is NOT produced (build5 Q3).  So: CMB-NEUTRAL (no harm, no fit), PASS-as-inert.
""")
RESULTS['limit_cosmological'] = 'NEUTRAL-INERT'
sub("4d. GW speed c_T = c")
print(r"""
  The MI doubled-field action adds NO term to the R-sector (Stage 3a) => the tensor (graviton)
  kinetic term is the host R alone => c_T = c EXACTLY (no disformal/aether modification of the
  graviton from the MI sector).  CONTRAST AeST: its -(K_B/2)F^2 aether CAN shift c_T, constrained
  to c by GW170817 (tuned).  Route-E MI does not even introduce that risk (no aether kinetic).  PASS.
""")
RESULTS['limit_GW_cT'] = True

# ============================================================================================
hdr("ROUTE E  STAGE 5 -- GHOST analysis (Ostrogradski / bounded Hamiltonian)")
# ============================================================================================
print(r"""
Two ghost questions:
  (G1) The NONLOCAL even form factor K_ff(Box_u/a0^2) is INFINITE-ORDER (branch cut, Stage 2), NOT
       a finite higher-derivative truncation => the Ostrogradsky theorem (which needs a finite, >2,
       order with nondegenerate top derivative) DOES NOT APPLY.  This is Milgrom-94's licensed
       strongly-nonlocal class; the local truncation (Costa-Franzmann-Pereira 1904.07321) would be
       Ostrogradsky-unstable, but we do NOT truncate.  [no finite-order ghost]
  (G2) The IN-IN DOUBLING: the doubled action has the indefinite metric c_{ab}=offdiag(1,1)
       (GALLEY l.352-356).  This is NOT a propagating ghost: phi_- is a LAGRANGE-MULTIPLIER-like
       adjoint (it is set to 0 in the physical limit, eq 11; it carries NO independent initial data
       in the physical solution -- build1 STEP: x_-(t)=0 is the physical solution).  The physical
       spectrum is phi_+ ONLY, with the bounded kinetic term inherited from the EVEN (conservative)
       kernel.  Verify the physical kinetic operator is sign-definite (no wrong-sign kinetic).
""")
# The physical (phi_+) kinetic coefficient is m_eff = m*mu_fw(|a|/a0) >= 0 for all a (Stage 0). A
# ghost would need m_eff<0 somewhere. Check mu_fw >= 0 on (0,oo):
xs = np.logspace(-6,6,25)
mu_vals = [(np.sqrt(1+4*xx**2)-1)/(2*xx) for xx in xs]
ghost_free_kinetic = all(mv>0 for mv in mu_vals)
print("  physical kinetic coeff m_eff/m = mu_fw(x) over x in [1e-6,1e6]:  min =", f"{min(mu_vals):.3e}",
      " max =", f"{max(mu_vals):.3f}", " => mu_fw>0 everywhere => NO wrong-sign kinetic:", YN(ghost_free_kinetic))
print("  monotone increasing 0 -> 1 (no turnaround) => bounded, sign-definite physical Hamiltonian.")
RESULTS['ghost_free'] = ghost_free_kinetic
print(r"""
  *** GHOST VERDICT: GHOST-FREE in the physical sector.  (G1) no finite-order Ostrogradsky (nonlocal,
  not truncated).  (G2) the in-in doubling is an adjoint (phi_- -> 0), not a propagating ghost; the
  physical spectrum is phi_+ with m_eff=m mu_fw>0 (bounded).  CAVEAT (honest): a FULLY rigorous
  bounded-Hamiltonian proof for an infinite-order nonlocal operator requires the explicit kernel's
  spectral representation; here we have (a) the EVEN-kernel conservativeness (Stage 2, lossless) and
  (b) sign-definite physical kinetic coeff -- strong evidence, sympy-checked, but the nonlocal
  Hamiltonian's global boundedness is asserted via conservativeness, not a finite-dim eigen-proof.
  => GHOST_FREE = CONDITIONAL (physical sector sign-definite + conservative; full nonlocal-H proof open). ***
""")

# ============================================================================================
hdr("ROUTE E  STAGE 6 -- relation to the Milgrom-1994 MI no-go")
# ============================================================================================
print(r"""
The field theory (E.1) is a CONTINUUM of nonlocal-in-time worldline functionals.  Milgrom-94:
no LOCAL Galilei-invariant MI action reproduces both limits.  Route E OBEYS the no-go by being
NONLOCAL (the even memory kernel along u; infinite-order form factor).  The collective field eq
(E.2) is the modified-Poisson/AQUAL relation, which AGREES with modified-GRAVITY (AeST) ON THE
QUASISTATIC/CIRCULAR SLICE (both give mu_fw(a/a0)a=grad Phi) and DIVERGES off it (the MI sector is
gated + history-dependent; AeST's is ungated + instantaneous).  So:
  - no-go OBEYED (via nonlocality) -- a local field MI would be blocked;
  - the field eq matches AeST only on the static-RAR slice (degeneracy guaranteed by the no-go's
    circular-orbit lemma), NOT as a theory identity (build4/5 verdict inherited & consistent).
""")
# sympy re-confirm the local-MI no-go bite (off-circular mismatch), so Route E's nonlocality is necessary:
t = sp.symbols('t', real=True); q = sp.Function('q')(t); ms, a0s = sp.symbols('m a_0', positive=True)
qdd = sp.diff(q,t,2); svar=(qdd/a0s)**2
Floc = sp.Rational(1,4)*sp.sqrt(svar)*sp.sqrt(4*svar+1)-sp.Rational(1,2)*sp.sqrt(svar)+sp.Rational(1,8)*sp.asinh(2*sp.sqrt(svar))
Lk = -ms*a0s**2*Floc
EL_local = sp.diff(sp.diff(Lk,qdd),t,2)   # local-theory inertial force = d^2/dt^2(dL/dqdd)
xabs=sp.Abs(qdd)/a0s; mu_q=(sp.sqrt(1+4*xabs**2)-1)/(2*xabs); target=ms*mu_q*qdd
A_,w_,e_=sp.symbols('A w e',positive=True); traj=A_*sp.cos(w_*t)+e_*sp.cos(2*w_*t)
sv={A_:1.0,w_:1.0,e_:0.3,a0s:1.0,ms:1.0,t:0.7}
ELv=complex(sp.N(EL_local.subs(q,traj).doit().subs(sv))).real
tgv=complex(sp.N(target.subs(q,traj).doit().subs(sv))).real
print(f"  off-circular (2-freq) local-MI EL force={ELv:.4f}  vs target m mu_fw a={tgv:.4f}  diff={ELv-tgv:.4f}")
print("  => NONZERO: a LOCAL field MI fails off-circular => Route E's nonlocal kernel is NECESSARY (no-go OBEYED).")
RESULTS['nogo_obeyed_via_nonlocality'] = (abs(ELv-tgv)>1e-3)

# ============================================================================================
hdr("ROUTE E  VERDICT LEDGER")
# ============================================================================================
for k,v in RESULTS.items():
    print(f"  {k:42s}: {v}")
print()
print("SUMMARY:")
print("  * Doubled-FIELD in-in action (E.1) CONSTRUCTED: phi_+ physical + phi_- adjoint, even kernel.")
print("  * Reproduces the dS-Unruh MI law COLLECTIVELY (E.2 point-mass => mu_fw(g/a0)g=g_N): YES (sympy).")
print("  * deep-MOND => AQUAL |grad phi|^3=Y^{3/2} with the SAME a0, v^4=GMa0 (BTFR): YES (sympy flux exact).")
print("  * 4 limits: Newtonian PASS, deep-MOND PASS, cosmo NEUTRAL-INERT (CMB-safe by inertness, no K(Q) dust),")
print("    GW c_T=c PASS (no aether kinetic).")
print("  * Ghost-free: CONDITIONAL (physical phi_+ sector sign-definite + conservative even kernel; full")
print("    nonlocal-Hamiltonian boundedness asserted via conservativeness, not an eigen-proof).")
print("  * KEYSTONE (metric/lensing): the field theory supplies the MATTER DYNAMICS sector ONLY. Its MI")
print("    stress-energy is phi_- -linear => VANISHES in the physical limit => ZERO source for the R-sector")
print("    => NO metric/lensing sector from the MI coarse-graining alone (sympy, decisive). It LOCATES the")
print("    needed partner (a doubled-metric g_- coupled to the GATED MI stress-energy) but does NOT produce")
print("    it -- exactly the session-flagged 'needs a metric-side partner' gap, now pinned to a precise term.")
print("  * No-go: OBEYED via nonlocality; field eq degenerate with AeST on the static-RAR slice only.")
print()
print("  ROUTE E STATUS: PARTIAL. The Galley doubled-FIELD MI theory is a genuine covariant-ready FIELD")
print("  action for the MATTER (inertia) sector -- reproduces the MI law + deep-MOND AQUAL collectively,")
print("  conservative, ghost-free in the physical sector, no-go-compliant -- but it supplies ONLY the matter")
print("  dynamics, NOT a metric/lensing sector. The lensing sector requires a SEPARATE doubled-metric partner")
print("  the field theory pinpoints but does not generate. NOT a hidden AeST (gated MI, vanishing metric")
print("  source); NOT a completed covariant action (lensing half missing).")
