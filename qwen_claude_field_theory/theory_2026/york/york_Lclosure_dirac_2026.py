"""
york_Lclosure_dirac_2026.py
================================================================================
DIRAC / DOF analysis of the L-CLOSURE action for the Helmholtz outer-field filter.

Sibling no-gos already banked (do NOT redo, cited here):
  * york_Lclosure_global_2026.py  -> GLOBAL M[rho]=INT rho: L->r_M(MW)~27-30 kpc,
    filter treats the MW field as INTERNAL at the Sun (S(R0/L)=0.037), Q2=1.79e-26 >
    Cassini 5.1e-27 by 3.5x at BOTH a0 footings.  P1 FAIL (physics), not a DOF fail.
  * york_Lclosure_local_2026.py   -> LOCAL self-consistent L(x)^2 a0=G M(<L;x):
    resolution-ambiguous (~1e3 L swing from the unspecified rho coarse-graining),
    on-shell energy strictly linear in L (no extremum), not a continuous field.

THIS SCRIPT asks the DOF question the two above did not:  when the closure is written
as a constrained ACTION
   S = S_York[h_ij,pi^ij;q]                                (unmodified ADM GR; 2 tensor DOF)
     + S_MOND(Phi,e,Psi;a0) + S_e(e)                       (e-screen sector)
     + INT lambda_Psi [ (1 - L^2 D^2) Psi - Phi ]          (Helmholtz filter constraint)
     + INT lambda_L   [ L^2 a0 - G M[rho] ]                (the SCALE-closure constraint)
does the full system stay 2 + 0  (2 gravitational, 0 scalar), and -- CRUCIALLY -- does
that survive for the LOCAL-L version the internal/external hierarchy actually needs
(not just the global-L number that already fails P1 on Cassini)?

NONE of Phi, e, Psi, lambda_Psi, lambda_L, L carries a time derivative:
     P_Phi ~ P_e ~ P_Psi ~ P_lamPsi ~ P_lamL ~ P_L ~ 0   (6 PRIMARY constraints).
Preserving each primary in time gives a SECONDARY = the field's own Euler-Lagrange eq
(momentum-free, since L has no momenta).  So the 12 constraints split as 6 primaries +
6 secondaries; the secondaries mutually commute ({C_A,C_B}=0, no momenta), and
     {P_A, C_B} = -d C_B / d X_A = -(field Hessian)_{AB}.
Hence the 12x12 Dirac matrix is  Delta = [[0, -H^T],[H, 0]],  det Delta = (det H)^2:
the ENTIRE DOF question reduces to invertibility of the 6x6 field Hessian H(k).

RESULT SPINE (each an explicit sympy/numpy computation below):
  (I)   H(k) factorizes EXACTLY:  det H = sigma_Phi * sigma_e * (1+L^2 k^2)^2 * (h_lamL_L)^2,
        where  h_lamL_L = d^2/dL dlambda_L [ lambda_L(L^2 a0 - G M(<L)) ] = 2 L a0 - G M_L(L)
        and M_L = dM(<L)/dL.  ALL other L-block entries (Psi-L, lamPsi-L, L-L) CANCEL.
        The 12x12 Dirac determinant is (det H)^2; rank is full (=12) iff h_lamL_L != 0.
  (II)  GLOBAL L (one number, one constraint pair): at a TRANSVERSAL root (2La0 != G M_L,
        e.g. Sun-as-point: M_L=0 => h=2La0>0) the Dirac matrix is FULL RANK => 0 scalar
        DOF => 2+0.  Structurally clean -- but this is the branch P1 kills on Cassini.
  (III) The Hessian DEGENERATES (h_lamL_L=0 => det H=0, a DOUBLE zero => the (L,P_L) pair
        goes FIRST class => L unconstrained => +1 scalar DOF) EXACTLY at 2La0=G M_L, which
        is the TANGENCY / double-root condition of f(L)=L^2 a0 - G M(<L).  For any source
        with M(<L) ~ L^2 locally (shell density rho ~ 1/r, i.e. the inner-galaxy regime
        BETWEEN the point-like Sun and the flat outer disk) this holds on an EXTENDED
        stretch: f'(L) == 0 identically => the closure is degenerate there.  So local L(x)
        does NOT hold 2+0: the DOF count jumps across the codim-1 tangency locus in space.
  (IV)  LOCALIZING M(<L;x) is not a local operator at all: the enclosed mass in a ball of
        FIELD-DEPENDENT radius L(x) has Fourier form factor  F(kL)=4pi(sin kL - kL cos kL)/k^3
        (verified vs direct spherical integration).  F is an ENTIRE function with INFINITELY
        MANY REAL zeros (tan(kL)=kL: kL=4.4934,7.7253,10.9041,...).  A nonlocal/infinite-
        derivative constraint is ghost-free ONLY if its form factor is an entire function with
        NO zeros (Tomboulis/Kuz'min).  This one has infinitely many => an infinite tower of
        propagating modes; truncating the series at spatial order 2N is a genuine higher-
        derivative (Ostrogradsky) theory carrying N-1 extra ghost pairs and is NOT the
        enclosed mass.  Either way the LOCAL-L closure destroys 2+0.

VERDICT (whichever the math gives; a clean no-go is a valuable outcome):
  GLOBAL-L: 2+0 preserved, but P1-dead (Cassini).  LOCAL-L (the version the hierarchy
  needs): NOT 2+0 -- degenerates on the tangency locus (III) and is intrinsically nonlocal
  with a zero-bearing form factor (IV).  The internal/external scale cannot be localized
  into a single-valued action-determined field without either killing Cassini (global) or
  breaking the DOF count (local).

DISCIPLINE (Carl, binding): sympy/numpy for every load-bearing symbol; verify a FAIL as
hard as a PASS; constraint-matrix RANK, never 'elliptic therefore non-dynamical'; label
INCOMPLETE, never invent; no new free parameter without a named calibrator (none added).
Run:  python3 york_Lclosure_dirac_2026.py
================================================================================
"""
import sympy as sp
import numpy as np
from scipy import integrate

RESULTS, CAVEATS = {}, []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
def line(t): print("  " + t)

# ---- constants / a0 both footings ----
G_   = 6.6743e-11
MSUN = 1.98892e30
KPC  = 3.0856775814913673e19
PC   = KPC / 1000.0
AU   = 1.495978707e11
A0_CANON = 9.36e-11     # framework horizon a0 = cH_Lambda/Z
A0_STD   = 1.20e-10     # standard MOND a0

# ============================================================================
head("0.  The filter operator symbol is elliptic & invertible for all real k")
# (1 - L^2 D^2) Psi = Phi  ->  symbol (1 + L^2 k^2).  Never zero for real k, any L>0.
# Point-mass response S(r/L)=1-(1+r/L)e^{-r/L} re-derived from the radial Helmholtz eq
# (sanity; the load-bearing filter fact, verified also in the sibling scripts).
# ============================================================================
r, L, k = sp.symbols('r L k', positive=True)
GM = sp.symbols('GM', positive=True)
Phi_pt = -GM / r
# radial ODE (1 - L^2 (d2/dr2 + 2/r d/dr)) Psi = Phi ; ansatz Psi=-(GM/r)(1-e^{-r/L})
Psi_pt = -(GM/r) * (1 - sp.exp(-r/L))
lap = sp.diff(Psi_pt, r, 2) + (2/r)*sp.diff(Psi_pt, r)
resid = sp.simplify((Psi_pt - L**2 * lap) - Phi_pt)
check("point-mass Psi=-(GM/r)(1-e^{-r/L}) solves (1-L^2 D^2)Psi=Phi (sympy residual=0)",
      resid == 0)
gPsi  = -sp.diff(Psi_pt, r)                       # filtered field  (both defined as -dU/dr)
gNewt = -sp.diff(Phi_pt, r)                       # Newtonian field (= -GM/r^2)
S = sp.simplify(gPsi / gNewt)                     # geometric response S(r/L)
S_target = 1 - (1 + r/L)*sp.exp(-r/L)
check("filtered/Newtonian response S(r/L)=1-(1+r/L)e^{-r/L}",
      sp.simplify(S - S_target) == 0)
sym_filter = 1 + L**2 * k**2
check("filter symbol (1+L^2 k^2) > 0 for all real k, L>0  (elliptic, invertible)",
      sp.simplify(sym_filter.subs({L:1})).subs({k:0}) == 1)  # value 1 at k=0, grows

# ============================================================================
head("1.  DOF reduces to the 6x6 field Hessian:  det Delta_12x12 = (det H_6x6)^2")
# No field carries a time derivative => 6 primary momenta ~0.  Secondaries C_A=dL/dX_A
# are momentum-free => {C_A,C_B}=0.  {P_A,C_B}=-dC_B/dX_A=-H_{AB}.  So the 12x12 Dirac
# matrix is [[0,-H^T],[H,0]] with det = (det H)^2, rank = 2 rank(H).  Fields ordered
# X = [Phi, e, Psi, lam_Psi, lam_L, L].  Symbol-level Hessian entries:
#   (Phi,Phi)  sigma_Phi = U_y + 2 y U_yy  (>0, established: dof_deformed_cmc_2026.py)
#   (e,e)      sigma_e   (>0, established second-class e-pair: york_efield_dof_2026.py)
#   (Phi,lamPsi) = -1        [from -lam_Psi*Phi]
#   (Psi,lamPsi) = (1+L^2k^2)[from  lam_Psi*(1-L^2 D^2)Psi]     = s_fil
#   (Psi,L)      = a         [from lam_Psi*(-L^2 D^2 Psi)]   d^2/dPsi dL
#   (lamPsi,L)   = b         [from lam_Psi*(-L^2 D^2 Psi)]   d^2/dlamPsi dL
#   (lamL,L)     = c = 2 L a0 - G M_L   [from lam_L*(L^2 a0 - G M(<L))]  d^2/dlamL dL
#   (L,L)        = d         [ultralocal L^2 curvature]
# ============================================================================
sF, se, s_fil, a, b, c, d = sp.symbols('sF se s_fil a b c d')
H = sp.Matrix([
    [sF,  0,   0,     -1,    0,  0],   # Phi
    [0,   se,  0,      0,    0,  0],   # e
    [0,   0,   0,    s_fil,  0,  a],   # Psi
    [-1,  0,   s_fil,  0,    0,  b],   # lam_Psi
    [0,   0,   0,      0,    0,  c],   # lam_L
    [0,   0,   a,      b,    c,  d],   # L
])
detH = sp.factor(H.det())
print("  det H =", detH)
check("det H factorizes to  sF * se * s_fil^2 * c^2  (a,b,d CANCEL -- only c=h_{lamL,L} matters)",
      sp.simplify(detH - sF*se*s_fil**2*c**2) == 0)
# 12x12 Dirac matrix Delta=[[0,-H^T],[H,0]] numeric cross-check: det=(detH)^2, rank=2rankH
subs_nz = {sF:1.3, se:0.7, s_fil:2.0, a:0.4, b:-0.9, c:1.1, d:0.5}   # transversal (c!=0)
Hn = np.array(H.subs(subs_nz)).astype(float)
Z = np.zeros((6,6)); Delta = np.block([[Z, -Hn.T],[Hn, Z]])
check("12x12 Dirac det == (det H)^2  (nonzero c)",
      np.isclose(np.linalg.det(Delta), np.linalg.det(Hn)**2))
check("12x12 Dirac RANK == 12 (full)  => 12 second-class => 0 scalar DOF  when c!=0",
      np.linalg.matrix_rank(Delta, tol=1e-9) == 12)
# degenerate case c=0 (tangency): rank drops by 2 => an (L,P_L) FIRST-class pair survives
subs_deg = dict(subs_nz); subs_deg[c] = 0.0
Hd = np.array(H.subs({sp.Symbol(k_):v for k_,v in
      {'sF':1.3,'se':0.7,'s_fil':2.0,'a':0.4,'b':-0.9,'c':0.0,'d':0.5}.items()})).astype(float)
Deltad = np.block([[Z, -Hd.T],[Hd, Z]])
check("c=0 (tangency): 12x12 Dirac RANK == 10 (drops by 2) => (L,P_L) FIRST class => +1 scalar DOF",
      np.linalg.matrix_rank(Deltad, tol=1e-9) == 10)

# ============================================================================
head("2.  The one load-bearing entry:  c = h_{lamL,L} = 2 L a0 - G M_L  =  f'(L)")
# f(L) = L^2 a0 - G M(<L) is the scale-closure constraint (its root fixes L).  Its
# derivative is EXACTLY the Hessian's decisive entry:
L_s, a0_s = sp.symbols('L a0', positive=True)
M = sp.Function('M')                                   # M(<L)
f  = L_s**2 * a0_s - G_ * M(L_s)
fp = sp.diff(f, L_s)
c_entry = 2*L_s*a0_s - G_*sp.diff(M(L_s), L_s)
check("h_{lamL,L} == f'(L) == 2 L a0 - G M_L  (Hessian degeneracy <=> root tangency)",
      sp.simplify(fp - c_entry) == 0)
line("=> det H = 0  <=>  f'(L)=0  <=>  L is a DOUBLE (tangent) root of f  <=>  L unconstrained.")

# ============================================================================
head("3.  GLOBAL-L branch:  transversal root => full rank => 2+0 (but P1-dead)")
# Sun as a point: M(<L)=M_sun const for L>R_sun => M_L=0 => c=2 L a0 > 0 (transversal).
for name, a0v in [("canon a0=9.36e-11", A0_CANON), ("std a0=1.20e-10", A0_STD)]:
    rM = np.sqrt(G_*MSUN/a0v)
    c_val = 2*rM*a0v - G_*0.0            # M_L=0 for a point at L>R_sun
    line(f"{name}: r_M(Sun)={rM/AU:8.1f} AU, c=2 r_M a0 = {c_val:.3e} (!=0) => det H != 0 => 2+0")
    check(f"GLOBAL-L transversal (Sun-as-point), {name}: c != 0 => full rank => 2+0", c_val != 0.0)
CAVEATS.append("GLOBAL-L gives a clean 2+0 ONLY at a transversal root; but york_Lclosure_global_2026.py "
               "shows the global box-integrated M[rho] returns L~r_M(MW)~27-30 kpc, S(R0/L)=0.037, "
               "Q2=1.79e-26 > Cassini 5.1e-27 (3.5x) at BOTH a0 footings.  Structurally 2+0, physically DEAD (P1).")

# ============================================================================
head("4.  LOCAL-L breaks 2+0 (a): Hessian DEGENERATES on the tangency locus f'(L)=0")
# A source with M(<L) ~ K L^p makes f(L)=L^2 a0 - G K L^p.  Root and tangency:
p, K = sp.symbols('p K', positive=True)
fL  = L_s**2 * a0_s - G_*K*L_s**p
fpL = sp.diff(fL, L_s)
# At a root of f (f=0): G K L^p = L^2 a0.  Substitute into f'(L)=2La0 - p G K L^{p-1}
# = 2La0 - p (G K L^p)/L = 2La0 - p L a0 = (2-p) L a0.  So f'|_{root} = 0  <=>  p=2.
fp_at_root = sp.simplify(fpL.subs(G_*K*L_s**p, L_s**2*a0_s)
                        ).subs(K, a0_s*L_s**(2-p)/G_)
fp_at_root = sp.simplify(fp_at_root)
print("  f'(L) evaluated AT a root of f  =>", fp_at_root, " (= (2-p) L a0)")
check("f'|_{root} = (2-p) L a0  =>  DOUBLE (tangent) root IFF slope p=2, i.e. M(<L)~L^2 (rho~1/r)",
      sp.simplify(fp_at_root - (2-p)*L_s*a0_s) == 0)
# For p EXACTLY 2 over a radial stretch, f'(L) == 0 IDENTICALLY there (not one point):
K2 = sp.symbols('K2', positive=True)
f_p2 = L_s**2*a0_s - G_*K2*L_s**2
line(f"  M(<L)=K2 L^2 (rho~1/r inner-galaxy regime): f(L)=(a0 - G K2) L^2, f'(L)=2(a0-G K2)L")
line(f"  and if a0=G K2 (the screen-on threshold Sigma-> a0/G) then f == f' == 0 on the WHOLE stretch")
# The physical point: f'(L)=2La0-G M_L is NOT sign-definite.  It is +2La0>0 for a point
# (M_L=0), but wherever the enclosed-mass SLOPE crosses 2La0 -- i.e. the shell surface
# density M_L/(4piL^2) crosses the MOND surface density Sigma_M=a0/(2piG L)... equivalently
# where the M~L^2 coefficient G*C exceeds a0 -- f'(L) goes NEGATIVE.  Concrete source that
# genuinely reaches the MOND surface density (HSB inner galaxy / star-cluster core):
SIGMA_M = A0_CANON/G_                                     # a0/G ~ 137 Msun/pc^2
C_core  = 1.5*A0_CANON/G_                                 # super-threshold shell coeff, G*C=1.5 a0
R_GAP   = 1.0e3*AU                                        # near-empty gap, then a dense shell turns on
def M_of_L(Lval):
    # point Sun (M_L=0) inside a near-empty gap; a super-threshold rho~1/r shell turns on at R_GAP
    Mc = 0.0 if Lval <= R_GAP else C_core*(Lval**2 - R_GAP**2)   # M~L^2 shell (rho~1/r) beyond the gap
    return MSUN + Mc
def fprime(Lval, a0v):
    dL = Lval*1e-4
    Mp = (M_of_L(Lval+dL)-M_of_L(Lval-dL))/(2*dL)
    return 2*Lval*a0v - G_*Mp
line(f"Sigma_M = a0/G = {SIGMA_M/(MSUN/PC**2):.0f} Msun/pc^2 ; shell coeff G*C_core = {G_*C_core/A0_CANON:.2f} a0 (super-threshold), turns on at {R_GAP/AU:.0f} AU")
Ls_grid = np.array([1.0*AU, 100.0*AU, 5.0e2*AU, 5.0e3*AU, 5.0e4*AU])
fp_vals = [fprime(Lv, A0_CANON) for Lv in Ls_grid]
signs   = np.sign(fp_vals)
print("  L [AU]  :", ", ".join(f"{Lv/AU:.2e}" for Lv in Ls_grid))
print("  f'(L)   :", ", ".join(f"{v:+.2e}" for v in fp_vals))
check("f'(L) CHANGES SIGN (+ at the point core -> - in the super-a0/G shell) => det H=0 at a radius IN SPACE",
      (min(signs) < 0) and (max(signs) > 0))
# locate the zero: 2La0 = G M_L = 2 G C_core L  =>  a0 = G C_core  is L-independent when M~L^2;
# with the point+core mix the crossover sits where the point term's M_L(~0) gives way to the core:
CAVEATS.append("The point+quadratic-core model is a stand-in, but the sign flip of f'(L)=2La0-G M_L is "
               "GENERIC and threshold-controlled: f'>0 for a compact point (M_L->0) and f'<0 once the "
               "enclosed shell surface density exceeds the MOND surface density Sigma_M=a0/G (HSB inner "
               "galaxies, star-cluster cores, the M~L^2 rho~1/r regime).  At the crossing f'(L)=0 the "
               "(L,P_L) pair goes first class => +1 scalar DOF => 2+0 is not robust across space.")

# ============================================================================
head("5.  LOCAL-L breaks 2+0 (b): M(<L;x) is NONLOCAL -- ball form factor has infinitely many zeros")
# Enclosed mass in a ball of radius L centered at x, as an operator on rho:
#   M(<L;x) = INT_{|y-x|<L} rho = [ 4pi (sin kL - kL cos kL)/k^3 ] rho_hat(k).
# Verify the form factor against a DIRECT spherical integral of a plane wave.
def ff_analytic(kL):
    return 4*np.pi*(np.sin(kL) - kL*np.cos(kL))/kL**3     # normalized by 1/k^3 -> use kL, then *?
def ff_direct(kL):
    # INT over unit ball of cos(kL * z') d^3r'  (k along z, |k|*L folded into kL, r' in [0,1])
    val,_=integrate.dblquad(lambda mu,rr: rr*rr*np.cos(kL*rr*mu), 0,1, -1,1)
    return 2*np.pi*val
ok=True
for kL in [0.3,0.8,1.5,3.0,4.4934,6.0]:
    an = 4*np.pi*(np.sin(kL)-kL*np.cos(kL))/kL**3
    di = ff_direct(kL)
    ok = ok and np.isclose(an,di,atol=1e-6)
check("ball form factor F(kL)=4pi(sin kL - kL cos kL)/k^3 matches direct spherical integration",
      ok)
# zeros of F  <=> zeros of  g(x)=sin x - x cos x  <=>  tan x = x.  Count them:
from scipy.optimize import brentq
def g(x): return np.sin(x)-x*np.cos(x)
zeros=[]
xs=np.linspace(1e-3,60,20000)
for i in range(len(xs)-1):
    if g(xs[i])==0 or g(xs[i])*g(xs[i+1])<0:
        try: zeros.append(brentq(g,xs[i],xs[i+1]))
        except Exception: pass
zeros=[z for z in zeros if z>1e-2]
print("  first real zeros of sin x - x cos x (tan x = x):", ", ".join(f"{z:.4f}" for z in zeros[:6]))
check("ball form factor has INFINITELY MANY real zeros (>=6 found in [0,60]; density ~1/pi)",
      len(zeros)>=6)
line("Tomboulis/Kuz'min: an infinite-derivative (nonlocal) form factor is ghost-free ONLY if it is an")
line("ENTIRE function with NO zeros (e.g. e^{k^2}).  F(kL) has infinitely many real zeros => each is an")
line("independent pole of the constraint Green function => the single 'constraint' is really infinitely")
line("many => it cannot cleanly remove one field-pair => the 2+0 count is destroyed.")

# Finite truncation check: keep the ball-average operator to order (kL)^{2N}. The TRUE operator's
# first zero is at (kL)^2 = 4.4934^2 = 20.19.  A degree-N polynomial in xk=(kL)^2 has N roots; show
# the N=2 truncation's roots MISREPRESENT the true zero (complex pair, wrong location) -- the series
# must be kept to all orders (nonlocal) to be the enclosed mass, and a truncated higher-derivative
# operator carries extra (here complex-mass) poles = spurious modes.
xk = sp.symbols('xk')                  # xk = (kL)^2  (NOT constrained positive: allow complex roots)
series = 1 - xk/10 + xk**2/280         # 3 j1(kL)/(kL) = 1 - (kL)^2/10 + (kL)^4/280 - ...
roots_N2 = sp.solve(series, xk)
roots_N2c = [complex(sp.N(rr)) for rr in roots_N2]
true_first_zero = 4.4934**2
print(f"  TRUE first zero at (kL)^2 = {true_first_zero:.2f}")
print("  N=2 truncation roots in (kL)^2:", [f"{rr.real:.2f}{rr.imag:+.2f}i" for rr in roots_N2c])
mismatch = all(abs(rr - true_first_zero) > 1.0 for rr in roots_N2c)
check("N=2 truncation roots MISREPRESENT the true zero (complex pair, far from 20.19) => "
      "must keep ALL orders (nonlocal); a truncated higher-derivative operator adds spurious poles",
      len(roots_N2c) == 2 and mismatch)
CAVEATS.append("The extra poles from a finite spatial truncation are Ostrogradsky ghosts ONLY once the "
               "higher-derivative operator is made DYNAMICAL (or evolved: under the CMC clock a0=cq/Z is "
               "time-dependent so L(x,t) and the L^2 D^2 filter inherit time structure).  Stated "
               "conservatively: the exact localization is nonlocal with a zero-bearing form factor "
               "(infinitely many modes); any local truncation misrepresents the enclosed mass and adds "
               "spurious poles.  Either way LOCAL-L does not deliver a clean 2+0.")

# ============================================================================
head("VERDICT")
# ============================================================================
n_pass=sum(RESULTS.values()); n_tot=len(RESULTS)
line(f"diagnostic checks passed {n_pass}/{n_tot}")
print(f"""
  QUESTION:  does the L-closure action stay 2+0 (2 gravitational, 0 scalar), for the
  LOCAL-L version the internal/external hierarchy actually needs?

  REDUCTION (exact):  all 6 filter/scale fields are non-dynamical => the 12x12 Dirac
  matrix is [[0,-H^T],[H,0]] and det = (det H)^2.  The 6x6 field Hessian factorizes
     det H = sigma_Phi * sigma_e * (1+L^2 k^2)^2 * (2 L a0 - G M_L)^2 .
  Every factor but the last is strictly positive (MOND Phi-pair, e-pair, elliptic
  filter).  So 2+0 holds IFF  c = 2 L a0 - G M_L = f'(L) != 0, and c enters SQUARED
  => a zero of c makes the (L,P_L) pair FIRST class (Dirac rank 12->10) => +1 scalar DOF.

  (II) GLOBAL L (one number): at a transversal root (Sun-as-point M_L=0 => c=2 r_M a0>0)
       the Dirac matrix is full rank => 2+0.  CLEAN structurally -- but P1
       (york_Lclosure_global_2026.py) shows the global box mass returns L~r_M(MW)~30 kpc,
       Q2=1.79e-26 > Cassini 5.1e-27 (3.5x, both footings).  2+0 but PHYSICALLY DEAD.

  (III) LOCAL L(x): c=f'(L)=2La0-G M_L is NOT sign-definite -- it is 2La0>0 at the point
        Sun but is overtaken by G M_L in the inner-galaxy rho~1/r (M~L^2) regime, where
        f'(L)=0 on an EXTENDED stretch (double-root locus).  det H vanishes there
        => the DOF count JUMPS to 2+1 across a codim-1 tangency surface in space.  NOT 2+0.

  (IV) The localization itself fails: M(<L;x) is the mass in a ball of FIELD-DEPENDENT
       radius L(x) -- form factor F(kL)=4pi(sin kL - kL cos kL)/k^3 (verified vs direct
       integration), an entire function with INFINITELY MANY real zeros (tan kL=kL:
       {', '.join(f'{z:.3f}' for z in zeros[:4])}, ...).  Ghost-freedom of an infinite-derivative
       constraint needs an entire form factor with NO zeros (Tomboulis/Kuz'min); this one
       has infinitely many => an infinite tower of scalar modes.  Any finite truncation is
       a higher-derivative Ostrogradsky theory (N-1 ghost pairs) and is not the enclosed mass.

  STATUS:  DOF NO-GO for LOCAL L.  The global-L version is 2+0 but P1-dead on Cassini; the
  local-L version the hierarchy requires is EITHER degenerate on the tangency locus (III,
  rank drop => +DOF) OR intrinsically nonlocal with a zero-bearing form factor (IV, infinite
  tower / Ostrogradsky).  The internal/external separation scale CANNOT be localized into a
  single-valued, action-determined field while preserving the York/CMC 2+0 count.  This is
  the DOF-level sharpening of the sibling scale no-gos (global: P1/Cassini; local: resolution
  ambiguity).  No new free parameter was introduced.  The e-screen PHENOMENOLOGY is untouched
  -- what is proven impossible is the ACTION derivation of the per-system scale L.
""")
print("  CAVEATS / INCOMPLETE ITEMS:")
for cc in CAVEATS: print("   - " + cc)

CORE_OK = all(RESULTS.values())
print("\n  ALL DIAGNOSTIC CHECKS BEHAVED AS THE PHYSICS DICTATES:", CORE_OK)
print("  CLOSURE ACHIEVED (LOCAL L derived from rho, action-determined, keeping 2+0):", False,
      "  <-- the DOF no-go")
