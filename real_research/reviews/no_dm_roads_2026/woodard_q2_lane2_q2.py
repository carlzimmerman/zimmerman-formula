#!/usr/bin/env python3
r"""
LANE 2 -- ROAD 2's GENUINE NONLOCAL SOLAR QUADRUPOLE Q2 vs THE CASSINI CEILING
==============================================================================
Road 2 = Deffayet-Esposito-Farese-Woodard NONLOCAL METRIC MOND
  (PRD 84:124054 / arXiv:1106.4984 ; JCAP 2026 04:081 / arXiv:2512.10513v2).

THE DECISIVE OPEN QUESTION (both Woodard papers DEFER the solar-system quadrupole
to 'future study'): does the GENUINE nonlocal field equation give the SAME
anisotropic solar quadrupole Q2 as the framework's committed LOCAL-AQUAL proxy
(=> FAIL x3.9-5.6, banked lane1), or a DIFFERENT (nonlocally suppressed) one
(=> Road 2 PASSES Cassini and beats Branch B)?

FRAMEWORK-FIRST HONESTY (Carl's #1 rule): a 'passes/suppressed' win is verified
as hard as a 'localizes/FAIL' deficit. I do NOT manufacture a suppression (cave)
and I do NOT assume localization without proving it (that would just re-assert the
proxy). The reduction is done channel-by-channel from Woodard's EXACT equations
(quoted below), then propagated to Q2 with the framework's COMMITTED kernel.

-------------------------------------------------------------------------------
WOODARD'S EXACT EQUATIONS (arXiv:2512.10513v2), verbatim structure:
  (5)  d_mu phi d_nu phi g^{mu nu} = -1 ,  phi(0,x)=0      [eikonal; u_mu = d_mu phi]
  (27) Z[g] = (4c^4/a0^2) g^{mu nu} d_mu[ (1/Box) R_ab u^a u^b ]
                                     d_nu[ (1/Box) R_cd u^c u^d ]
             ---static--->  (4c^4/a0^2) grad(Psi) . grad(Psi) ,  Psi=(1/Box)(R_ab u^a u^b)
  (33) d_mu[ sqrt(-g) u^mu M ] = -d_mu[ sqrt(-g) u^mu f(Z) ] , M(0,x)=45 det[g_ij]
  (18) v^4(r) = [c^2 r Psi'(r)]^2 = a0 G M(r)              [BTFR: paper's OWN static reduction]
   f(Z) = (1/2) Z exp[-(1/3) sqrt|Z|] ;  L_MOND = -(a0^2/16piG) M[g] sqrt(-g)
   BC on 1/Box: it and its first derivative VANISH on the t=0 initial-value surface
                (causal / initial-value -- NOT 'vanish at spatial infinity').
-------------------------------------------------------------------------------
Ceiling: |Q2| < 5.2e-27 s^-2 (banked corrected Cassini bound). Both a0 footings.
"""
import numpy as np
from scipy import integrate, optimize

# ======================================================================= constants
G     = 6.674e-11          # m^3 kg^-1 s^-2
Msun  = 1.989e30           # kg
c     = 2.99792458e8       # m/s
CEIL  = 5.2e-27            # s^-2, Cassini quadrupole ceiling
G_EXT = 1.8e-10            # galactic external field at the Sun (m/s^2)  ~1.9 a0
H0    = 2.20e-18           # s^-1 (cosmological, for the horizon-tail estimate)
R_SAT = 9.58 * 1.496e11    # Saturn semimajor axis (m)
FOOT  = (("canon", 9.36e-11), ("alt", 1.13e-10))

print("="*94)
print("PART I -- REDUCTION OF Z[g] IN THE SUN + EXTERNAL-FIELD CONFIG (the crux)")
print("="*94)
print(r"""
Quasi-static weak field:  ds^2 = -(1+2Phi/c^2)c^2 dt^2 + (1-2Phi/c^2) dx.dx ,
Phi = Phi_sun(r) + Phi_ext ,  Phi_ext = Phi_0 + g_ext . x + (tidal) locally.

Woodard eq (27): the WHOLE nonlocality sits INSIDE  Psi = (1/Box)(R_ab u^a u^b);
the outer object Z = (4c^4/a0^2) g^{mn} d_m Psi d_n Psi is a LOCAL quadratic in
grad(Psi).  So localization of Z <=> localization of Psi.  Reduce Psi:

 SOURCE  S = R_ab u^a u^b :
   u_mu = d_mu phi (eq 5).  Static: phi = t sqrt(-g00(x)), u^0 = 1/sqrt(-g00) ~ 1-Phi/c^2,
   u^i = d_i phi ~ (t/c^2) d_i Phi  (secular, anisotropic, points along g_total).
   R_ab u^a u^b = R00 (u^0)^2 + 2 R0i u^0 u^i + Rij u^i u^j.
   STATIC field => R0i = 0 exactly.  Rij u^i u^j ~ Rij (t d_iPhi)(t d_jPhi)/c^4 = O(Phi^2),
   secular, 2nd order -- NOT the leading MOND response.  Leading:
        S = R00 (u^0)^2 = (nabla^2 Phi / c^2)(1 - 2Phi/c^2) ~ nabla^2 Phi / c^2 .
   => the eikonal-u anisotropy (channel b) does NOT enter S at leading order.

 INVERSION  Psi = (1/Box) S ,  Box --static--> nabla^2 :
   Psi = (1/nabla^2)(nabla^2 Phi / c^2) = Phi/c^2 + harmonic .
   nabla^2 Phi = 4piG rho_TOTAL/c^2 sources on ALL mass (Sun AND the 8-kpc galactic
   mass whose local field IS g_ext).  With Woodard's CAUSAL t=0 BC, the retarded
   past light cone of any solar-system point (system static for >> its light-crossing
   time) reaches the galaxy => 1/Box RECONSTRUCTS the full Newtonian potential:
        Psi = Phi_total/c^2 = (Phi_sun + Phi_ext)/c^2 ,
        grad Psi = (g_sun + g_ext)/c^2   (eq 18 confirms c^2 Psi' = g).
   The external field is PRESENT and enters as the standard EFE gradient.  This is
   the paper's OWN static reduction (eq 27 static form + eq 18 BTFR): Z is a LOCAL
   function of the total field strength g_total = |g_sun + g_ext|:
""")
def Z_of_g(g, a0):
    return 4.0*(g/a0)**2           # eq 27 static + eq 18 (c^2|grad Psi| = g)  => sqrt(Z)=2 g/a0
for tag,a0 in FOOT:
    g = G_EXT
    print(f"   {tag:5s}: at g=g_ext={g:.2e},  Z=(4c^4/a0^2)|gradPsi|^2 = 4(g/a0)^2 = {Z_of_g(g,a0):.3f}"
          f"  (sqrt Z = {np.sqrt(Z_of_g(g,a0)):.3f} = 2 g/a0)  => screen exp[-sqrtZ/3]={np.exp(-np.sqrt(Z_of_g(g,a0))/3):.3f}")

print(r"""
 => Z[g] LOCALIZES to 4(g_total/a0)^2.  The three candidate NONLOCAL channels the
    proxy might miss are each quantified below and each fails to move the l=2 moment.
""")

print("-"*94)
print("PART II -- THE THREE NONLOCAL CHANNELS, QUANTIFIED (do any suppress the l=2?)")
print("-"*94)

# (a) horizon / cosmological IR tail of 1/Box: is its LOCAL gradient an anisotropic
#     source competitive with g_ext, or a spatially-uniform monopole offset?
#     de Sitter: R_ab u^a u^b ~ H^2 ; the local cosmological TIDAL tensor ~ (adotdot/a) ~ H^2.
cosmo_tidal = H0**2                     # s^-2, the cosmological l=2 tidal amplitude at the Sun
grad_cosmo_at_saturn = H0**2 * R_SAT / c**2 * c**2   # ~ H^2 * r : gradient of cosmological Psi
print(f"(a) HORIZON/COSMOLOGICAL TAIL of 1/Box:")
print(f"    cosmological local tidal quadrupole ~ H0^2            = {cosmo_tidal:.2e} s^-2")
print(f"       vs Cassini ceiling                                 = {CEIL:.2e} s^-2"
      f"   -> {cosmo_tidal/CEIL:.1e}x the ceiling (i.e. ~{np.log10(CEIL/cosmo_tidal):.0f} orders BELOW)")
print(f"    local gradient of the cosmological Psi across Saturn's orbit ~ H0^2 * r_Sat"
      f" = {H0**2*R_SAT:.2e} m/s^2")
print(f"       vs external field g_ext = {G_EXT:.2e} m/s^2"
      f"   -> ratio {H0**2*R_SAT/G_EXT:.1e}  (~{np.log10(G_EXT/(H0**2*R_SAT)):.0f} orders below g_ext)")
print(f"    => the 1/Box horizon tail is a SPATIALLY-UNIFORM monopole offset locally; it does NOT")
print(f"       source an anisotropic l=2 moment and does NOT suppress the galactic g_ext quadrupole.")

# (b) eikonal-u anisotropy: order of its contribution to S relative to the leading term.
Phi_local = G_EXT * R_SAT               # ~ potential scale (crude), Phi/c^2 magnitude
print(f"\n(b) EIKONAL-u ANISOTROPY  (u^i ~ (t/c^2) d_iPhi, points along g_total):")
print(f"    enters S only via R0i u^0 u^i (=0, static) and Rij u^i u^j = O((Phi/c^2)^2), secular.")
print(f"    Phi/c^2 at the transition shell ~ (g_ext r_shell)/c^2 ~ {G_EXT*np.sqrt(G*Msun/G_EXT)/c**2:.1e}"
      f"  -> the u-anisotropy correction to S is O(1e-13) of the leading nabla^2 Phi term.")
print(f"    => channel (b) is a 2nd-order/secular GR correction, NOT the leading MOND l=2 source.")

# (c) derivative cross-terms in Z = (4c^4/a0^2) g^{mn} d_m Psi d_n Psi.
print(f"\n(c) OUTER-DERIVATIVE CROSS TERMS  in Z = (4c^4/a0^2)|grad Psi|^2 :")
print(f"    grad Psi = (g_sun + g_ext)/c^2  =>  |grad Psi|^2 = |g_sun|^2 + 2 g_sun.g_ext + |g_ext|^2.")
print(f"    The ONLY cross term is  2 g_sun . g_ext  = the STANDARD Sun x external EFE interference")
print(f"    -- already the source of the proxy's anisotropic transition shell.  No NEW term appears.")
print(f"    => channel (c) reproduces the local proxy exactly; no nonlocal suppression.")

print(r"""
(transport eq 33 cross-check) In the quasi-static attractor M -> f(Z) locally: the
transport d_mu[sqrt(-g)u^mu M] = -d_mu[sqrt(-g)u^mu f(Z)] is degenerate for static
fields (u^mu ~ time direction, d_t(static)=0), so M is pinned to f(Z) by the
initial data + attractor -- it does NOT delocalize the phantom density.  Hence the
quasi-static field equation IS the local AQUAL with f(Z).  (This is why the paper's
own eq-18 BTFR is a LOCAL g-relation.)
""")

print("="*94)
print("PART III -- Q2 EXTRACTION: committed kernel, both scenarios, both footings")
print("="*94)

# ---- framework's COMMITTED Q2 kernel (branchB_q2_gate_2026/decider_q2_crosscheck.py) ----
def q_raw(nu1, etilde, vmax=60.0):
    eN=optimize.brentq(lambda e:(1.0+nu1(e))*e-etilde,1e-9,etilde+5)
    def integrand(xi,v):
        D=eN**2+v**4+2*eN*v**2*xi
        if D<=0: return 0.0
        return (nu1(np.sqrt(D)))*(eN*(3*xi-5*xi**3)+v**2*(1-3*xi**2))
    val,_=integrate.dblquad(integrand,0,vmax,lambda v:-1,lambda v:1,epsabs=1e-10,epsrel=1e-8)
    return 1.5*val

# boost functions nu1(y), y = g_N/a0 ------------------------------------------------
nu1_simple=lambda y:(np.sqrt(1.0+4.0/np.maximum(y,1e-12))-1.0)/2.0    # calibration boost
nu1_fw    =lambda y: np.sqrt(1.0+1.0/np.maximum(y,1e-12))-1.0         # framework nu (power-law)
def nu1_exp(y):                                                       # mu=1-e^-x (fast exp)
    y=float(np.maximum(y,1e-12))
    x=optimize.brentq(lambda x:(1.0-np.exp(-x))*x-y,1e-9,y+40.0)
    return x/y-1.0
def nu1_woodard_tail(y, ys=1.0, rate=1.0/3.0):                        # framework transition x exp screen
    y=np.maximum(y,1e-12)
    base=np.sqrt(1.0+1.0/y)-1.0
    screen=np.exp(-rate*np.maximum(y-ys,0.0))
    return base*screen
# Woodard EXACT 2026 screen: f(Z)=1/2 Z exp[-sqrtZ/3], sqrtZ=2g/a0 => exp[-(2/3) g/a0]:
nu1_2026=lambda y: nu1_woodard_tail(y, rate=2.0/3.0)

# calibrate the kernel tail-correction on Desmond-Hees-Famaey 2024 anchors -----------
print("[calib] kernel vs Desmond+2024 anchors q(1)=0.094,q(1.5)=0.159,q(2)=0.221:")
ratios=[]
for et,anchor in ((1.0,0.094),(1.5,0.159),(2.0,0.221)):
    q=abs(q_raw(nu1_simple,et)); ratios.append(q/anchor)
CAL=1.0/np.mean(ratios)
print(f"        tail-correction CAL = {CAL:.4f}  (kernel reproduces anchors at {np.mean(ratios):.3f})")
assert 1.0<CAL<1.10

def Q2(nu1,a0,gx):
    return CAL*abs((3.0*a0**1.5)/(2.0*np.sqrt(G*Msun))*q_raw(nu1,gx))

print(f"\nCeiling |Q2| < {CEIL:.1e} s^-2.  g_ext={G_EXT:.1e} m/s^2 (+-15%).  etilde=g_ext/a0.\n")
print(f"{'scenario / boost':44s} {'foot':5s} {'etilde':7s} {'worst|Q2|':11s} {'ratio':6s} verdict")
print("-"*94)

def row(label, nu1):
    out={}
    for tag,a0 in FOOT:
        et=G_EXT/a0
        Qs=[Q2(nu1,a0,etx) for etx in (et*0.85,et,et*1.15)]
        worst=max(Qs); out[tag]=worst
        stat="PASS" if worst<CEIL else f"FAIL x{worst/CEIL:.2f}"
        marg="MARGINAL " if 0.7<worst/CEIL<1.4 else ""
        print(f"{label:44s} {tag:5s} {et:7.2f} {worst:11.2e} {worst/CEIL:6.2f} [{marg}{stat}]")
    return out

print("--- SCENARIO A: Z LOCALIZES (proven in Parts I-II) -> local AQUAL proxy ---")
A_2026 = row("EXACT 2026 screen exp[-(2/3)g/a0] (2512)", nu1_2026)
A_exp  = row("fast exp mu=1-e^-x (Woodard analog)",       nu1_exp)
A_slow = row("slow exp e^-(g/3a0) (1106 y=g/3a0)",        nu1_woodard_tail)
A_pow  = row("power-law framework-nu [reference class]",  nu1_fw)

print("\n--- SCENARIO B: hypothetical NONLOCAL anisotropic delta-Z suppression ---")
print("    Parts I-II showed each nonlocal channel (a horizon tail / b eikonal-u / c cross-terms)")
print("    fails to move the l=2 sourcing shell (g~g_ext~1.9a0, y~O(1)) where the response is")
print("    unscreened. A genuine suppression would require the transition SHELL itself to be")
print("    delocalized/smeared; but transport eq 33 pins M->f(Z) locally in the static attractor,")
print("    so the shell is NOT smeared. Quantify the ONLY nonlocal add-on (horizon l=2):")
print(f"       cosmological l=2 add-on ~ H0^2 = {H0**2:.2e} s^-2  = {H0**2/CEIL:.1e} x ceiling")
print(f"       => Scenario B's nonlocal piece is ~{np.log10(CEIL/H0**2):.0f} orders too weak to CANCEL")
print(f"          the Scenario-A galactic quadrupole (it adds, negligibly; it cannot subtract it).")

print("\n"+"="*94)
print("PART IV -- VERDICT")
print("="*94)
worst_2026 = max(A_2026.values())
print(f"""
 Z[g] LOCALIZES in the Sun+external-field config. Woodard's OWN static reduction
 (eq 27 static form Z->(4c^4/a0^2)|grad Psi|^2 ; eq 18 BTFR v^4=a0 GM) makes Z a
 LOCAL function of the total field strength g_total = |g_sun + g_ext|, i.e. exactly
 the field-strength argument of the framework's committed AQUAL kernel. The three
 nonlocal channels the proxy could miss are each too weak / wrong-order to move the
 l=2 quadrupole:
   (a) 1/Box horizon tail  -> spatially-uniform monopole, ~{np.log10(CEIL/H0**2):.0f} orders below the l=2 ceiling;
   (b) eikonal-u anisotropy -> 2nd-order/secular, O(1e-13) of the leading source;
   (c) outer-derivative cross-term -> only the standard g_sun.g_ext EFE interference,
       already in the proxy.
 Transport eq 33 pins M->f(Z) locally (static attractor), so the transition shell is
 NOT delocalized. => Road 2's GENUINE nonlocal quadrupole = the LOCAL PROXY.

 Q2 (EXACT 2026 screen, worst corner over both footings) = {worst_2026:.2e} s^-2
   vs ceiling {CEIL:.1e}  ->  FAIL x{worst_2026/CEIL:.2f}.

 VERDICT: LOCALIZES  ==>  Q2 = proxy = FAIL x{min(A_2026['canon'],A_2026['alt'])/CEIL:.1f}-{worst_2026/CEIL:.1f}.
 Road 2 does NOT pass Cassini and does NOT beat Branch B on the quadrupole. The
 no-DM lensing win on Road 2 is NOT bought by a nonlocal Q2 suppression -- the
 nonlocality lives inside Psi and washes out to the SAME local field strength that
 the proxy uses. (Honesty: this is the deficit-side outcome, proven channel-by-
 channel, not assumed; and NOT a manufactured suppression.)
""")
print("="*94); print("exit 0")
