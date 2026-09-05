"""
!!! SUPERSEDED by wf_decisive_v2_correct.py !!!
This file used the ACTION-LEVEL map (-2f <-> a0^2 W), which is INCONSISTENT with
Flanagan's own MOND-function definition mu = 1 + fbar'/(2 abar).  The correct map is
via mu: fbar' = 2 abar (mu-1).  Under the correct map the DANGEROUS coefficient is the
LONGITUDINAL KINETIC term -fbar''/2 = (1-y)e^-y (ghost for y>1), NOT the gradient.
Kept only for provenance.  Use wf_decisive_v2_correct.py.
"""

"""
wf_decisive_gradient.py  -- THE decisive test.

Candidate (khronometric MOND + K^2 backbone), primitive
  W(y)=y^2/2+(1+y)e^-y-1,  mu=W'/y=1-e^-y (H_perp),  W''=1+(y-1)e^-y (H_par).

Perturbative scalar action  S = (M_Pl^2/2) int [ A(y) pidot^2 - B_par (d_par pi)^2 - B_perp (grad_perp pi)^2 ]
with  A=A_KH+A_M,  B_i=B_{i,KH}+B_{i,M}.

Literature anchors (transcribed, cited):
 * Flanagan arXiv:2302.14846 (ApJ 958,2): minimal khronometric-MOND, action R-2f(a).
     - kinetic tensor  h^{ij} = -1/(4piG)[ chibar (d^ij - ahat^i ahat^j) + fbar''/2 ahat^i ahat^j ],
       chi = f'/(2a).  NO-GHOST  <=>  f'<=0 AND f''<=0            (Eq43)
     - gradient coeff  rho_T0 = -1/(4piG) div[ chibar grad Phi ].  NO-GRAD-INSTAB <=> rho_T0>=0,
       which on the stationary MOND background gives  f' <= a f'' <= 0   (Eq54)
     - NO-GO: (43)/(54) hold in deep MOND but CANNOT hold through the transition because
       f -> Lambda_inf (a CONSTANT) at high a forces f'' to change sign. NO K^2 backbone present.
 * Bonetti-Barausse arXiv:1502.05554 (PRD91,084053): forcing EXACT GR at high a => scalar
     strongly coupled at low a; escape = RETAIN khronometric (LV) structure at high a.

MAP (matching -2f(a) <-> a0^2 W(a/a0), i.e. f=-1/2 a0^2 W + C, y=a/a0):
   f'  = -1/2 a0  W'(y)     ->  f'<=0   <=>  W'>=0
   f'' = -1/2     W''(y)    ->  f''<=0  <=>  W''>=0
   a f'' = -1/2 a0 y W''    ->  f'<=a f''  <=>  W' - y W'' >= 0
So Flanagan Eq43 (no-ghost) <=> W'>=0 AND W''>=0.
   Flanagan Eq54 gradient part <=> G(y):=W'-yW'' >= 0.
"""
import numpy as np

def mu(y):    return 1.0 - np.exp(-y)                 # H_perp
def Wpp(y):   return 1.0 + (y-1.0)*np.exp(-y)         # H_par
def Wp(y):    return y*(1.0 - np.exp(-y))
def W(y):     return 0.5*y*y + (1.0+y)*np.exp(-y) - 1.0
def G(y):     return Wp(y) - y*Wpp(y)                 # = -y^2 e^-y  (Eq54 combo)

ys = np.concatenate([np.logspace(-6,6,400001), np.linspace(1e-3,30,400001)])
ys = np.unique(ys)

print("="*70)
print("PART A -- NO-GHOST (background-independent): Flanagan Eq43 <=> W'>=0, W''>=0")
print("="*70)
print(f"  min mu  (H_perp) over 1e-6..1e6 = {mu(ys).min():.6e}  (>0 : {np.all(mu(ys)>0)})")
print(f"  min W'' (H_par ) over 1e-6..1e6 = {Wpp(ys).min():.6e}  (>0 : {np.all(Wpp(ys)>0)})")
print(f"  min W'          over 1e-6..1e6 = {Wp(ys).min():.6e}  (>0 : {np.all(Wp(ys)>0)})")
print("  W'' local min at y=2 :", f"{Wpp(2.0):.10f}", " (= 1+e^-2, never dips below 0)")
print("  => f'=-a0/2 W' < 0 and f''=-1/2 W'' < 0 for ALL y>0 INCLUDING transition.")
print("     Flanagan's f'' MUST flip sign (f->Lambda_inf const); W''->1 (W->y^2/2) so it")
print("     NEVER flips. The background-independent no-ghost no-go is EVADED outright.")
print()
print("="*70)
print("PART B -- GRADIENT combo G(y)=W'-yW''  (Flanagan Eq54 needs G>=0)")
print("="*70)
gy = G(ys)
imin = np.argmin(gy)
print(f"  G(y) = W'-yW'' ; closed form = -y^2 e^-y")
print(f"  min G = {gy[imin]:+.6f} at y = {ys[imin]:.4f}   (max G = {gy.max():+.3e})")
print(f"  G(y) < 0 for ALL y>0 : {np.all(gy<=1e-14)}  -> SIGN-DEFINITE NEGATIVE")
# analytic worst point: d/dy(-y^2 e^-y)=0 -> y=2 ; G(2)=-4 e^-2
print(f"  analytic worst: y*=2  (a=2 a0, the TRANSITION),  G(2) = -4 e^-2 = {-4*np.exp(-2):.6f}")
print()
print("  Two readings of B_{i,M}:")
print("   (i)  constitutive Hessian eigenvalues (2nd var of a0^2 W wrt a_i):")
print("        B_perp,M = mu  in (0,1]  and  B_par,M = W'' in (0,1.135]  -> POSITIVE-DEFINITE.")
print("        (short-wavelength / quasi-static gradient stiffness).")
print("   (ii) Flanagan reduced rho_T0 on the SELF-CONSISTENT stationary background:")
print("        controlled by G=W'-yW''<0  -> would be NEGATIVE, worst -0.541 at y=2.")
print("   The self-consistent background for THIS W is NOT re-derived here, so which of")
print("   (i)/(ii) the physical B inherits is left explicit (see honesty labels).")
print()
print("="*70)
print("PART C -- BACKBONE FLOOR needed IF B inherits the worst dip (reading ii)")
print("="*70)
worst = -gy[imin]                    # 0.541...
print(f"  Worst negative dip |G|max = {worst:.4f} at y=2 (transition).")
print(f"  Need B_KH + B_M > 0 everywhere.  Bounded positive backbone B_KH >= {worst:.4f}")
print(f"  (O(1), in units of the O(1) Hessian) SUFFICES to keep B_total>0 for all y.")
print()
print("  Compatibility with c_T=1 (GW170817) and PPN:")
print("   c_T^2 = 1/(1-beta) = 1  =>  beta = 0 exactly ;  alpha_eff = 2 beta = 0.")
print("   With beta=0 the K^2 backbone is  K_ij K^ij - (1+lambda) K^2  (coeff of K_ijK^ij")
print("   is 1+beta=1, unaffected).  Its khronon GRADIENT stiffness B_KH is set by lambda,")
print("   INDEPENDENT of beta -> B_KH can be O(1)>=0.541 with beta=0 held fixed.")
print("   => the required floor does NOT fight c_T=1.  (Bonetti-Barausse: kinetic")
print("   normalisation stays finite as beta->0, so NO strong coupling.)")
print()
print("="*70)
print("PART D -- table across the transition")
print("="*70)
print(f"{'y':>8} {'mu=Hperp':>10} {'Wpp=Hpar':>10} {'G=W-yWpp':>10} {'B_tot(BKH=.55)':>14}")
for yy in [1e-3,1e-2,0.1,0.3,0.5,1.0,1.5,2.0,3.0,5.0,10.0,100.0]:
    btot = 0.55 + G(yy)
    print(f"{yy:8.3g} {mu(yy):10.5f} {Wpp(yy):10.5f} {G(yy):+10.5f} {btot:14.5f}")
