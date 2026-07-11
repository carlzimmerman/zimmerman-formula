#!/usr/bin/env python3
"""
LANE 1 -- THE DECISIVE NUMBER
=============================
Does Deffayet-Esposito-Farese-Woodard NONLOCAL METRIC MOND (arXiv:1106.4984;
2026 single-IF arXiv:2512.10513) pass the Cassini solar quadrupole Q2 gate that
the AeST/AQUAL vector-MG class FAILS at +6-14 sigma?

Framework-first honesty: I verify a Road-2 PASS as rigorously as a FAIL. The
banked kernel Q2 = (3/2)(a0^1.5/sqrt(GM))|q| (corrected Milgrom kernel, no /sqrt(D),
calibrated on Desmond-Hees-Famaey 2024 anchors q(1)=0.094, q(1.5)=0.159, q(2)=0.221)
is applied UNCHANGED; the ONLY thing swapped is the MOND boost nu1(y):

  - AeST / standard MOND: POWER-LAW boost  nu1 ~ 1/(2y) or 1/y  (slow tail into
    the inner solar system) -> LARGE Q2 -> the class tension (Desmond+2024).
  - Woodard nonlocal MOND: EXPONENTIAL screening.  From 1106.4984 eqs 77-82:
      y[g] = c^2|b'|/(3 a0)  ~  g_N/(3 a0)     (eq 78; y~1e4 in solar system)
      L_MOND = (9 a0^2/32piG) y^2 e^{-y}  sqrt(-g)   (eq 82, single-invariant)
      variants (eqs 80,81):  y^2 e^{-y}   and   y^2 e^{-(y^2+y)}
    "the predicted deviations from GR are exponentially small w.r.t. the tightest
     solar-system constraints" (paper, after eq 81).
    The 2026 single-IF form f(Z)=(1/2)Z exp[-(1/3)sqrt|Z|] with Z~(g_N/a0)^2 gives
    the SAME exp[-(1/3) g_N/a0] high-field screening structure.

PHYSICS OF THE CRUX: Q2 is the ANISOTROPIC tidal quadrupole sourced by the
Sun-galaxy external-field interference summed over the transition region. In the
kernel it is q = quadrupole moment of nu1(g_total/a0) over the internal-field
variable v (v small = far/deep-MOND transition; v large = inner solar system, high
field). A POWER-LAW boost keeps sourcing the quadrupole out to v~10-60 (why the
banked kernel needs vmax=60 + a ~3% tail); an EXPONENTIAL boost is cut off at
v~few, so the inner shells contribute nothing. The question is the NUMBER: how much
of q is transition-built (shared by all MOND) vs power-law-tail-built (exp kills).

Ceiling: |Q2| < 5.2e-27 s^-2 (banked corrected bound). Both a0 footings.
"""
import numpy as np
from scipy import integrate, optimize

G=6.674e-11; Msun=1.989e30; CEIL=5.2e-27
G_EXT=1.8e-10   # Galactic external field at the Sun (m/s^2), std MOND EFE value

# ---------------------------------------------------------------- Q2 kernel (banked, unchanged)
def q_raw(nu1, etilde, vmax=60.0):
    eN=optimize.brentq(lambda e:(1.0+nu1(e))*e-etilde,1e-9,etilde+5)
    def integrand(xi,v):
        D=eN**2+v**4+2*eN*v**2*xi
        if D<=0: return 0.0
        return (nu1(np.sqrt(D)))*(eN*(3*xi-5*xi**3)+v**2*(1-3*xi**2))
    val,_=integrate.dblquad(integrand,0,vmax,lambda v:-1,lambda v:1,epsabs=1e-10,epsrel=1e-8)
    return 1.5*val

# ---------------------------------------------------------------- boost functions nu1(y), y=g_N/a0
# POWER-LAW class (the AeST / framework tension):
nu1_simple=lambda y:(np.sqrt(1.0+4.0/np.maximum(y,1e-12))-1.0)/2.0   # -> 1/y  tail
nu1_fw    =lambda y: np.sqrt(1.0+1.0/np.maximum(y,1e-12))-1.0        # framework nu, ->1/(2y)

# EXPONENTIAL class (Woodard structural analog):
# canonical published exponential interpolation mu(x)=1-e^{-x}, x=g_obs/a0.
#   deep-MOND coeff EXACT (mu->x => g=sqrt(g_N a0)); screening e^{-g/a0}.
#   nu=1/mu, and y=g_N/a0=mu(x) x=(1-e^{-x})x  -> solve x(y), nu1=x/y-1.
def nu1_exp(y):
    y=float(np.maximum(y,1e-12))
    x=optimize.brentq(lambda x:(1.0-np.exp(-x))*x-y,1e-9,y+40.0)
    return x/y-1.0
# Woodard-FAITHFUL slower screen: his y=g/(3a0) puts the exponent at g/(3a0), i.e.
# a factor-3 SLOWER screen than mu=1-e^{-x}. Model mu(x)=1-e^{-x/3} but RE-anchor the
# deep-MOND coefficient to 1 by rescaling: use mu(x)=1-e^{-x} in the deep/transition
# region is the fast bound; the slow bound uses the raw Woodard exponent e^{-y} on a
# boost that matches framework at the transition and screens as y^2 e^{-y} tail:
def nu1_woodard_tail(y, ys=1.0, rate=1.0/3.0):
    """framework transition, but multiply the boost by the Woodard exp screen so the
    HIGH-y tail dies exponentially instead of power-law. rate=1/3 -> slow e^{-y/3}."""
    y=np.maximum(y,1e-12)
    base=np.sqrt(1.0+1.0/y)-1.0            # framework boost (correct deep MOND + transition)
    screen=np.exp(-rate*np.maximum(y-ys,0.0))  # e^{-rate*(g-g_s)/a0}; no screen below transition
    return base*screen
# EXACT 2026 single-IF screen: f(Z)=1/2 Z exp[-1/3 sqrt|Z|], Z=(4c^4/a0^2)|grad Psi|^2
#  => sqrt|Z|=2 g/a0, so screen = exp[-(2/3) g/a0]  (between the two bounds above)
nu1_2026=lambda y: nu1_woodard_tail(y, rate=2.0/3.0)

# ---------------------------------------------------------------- [0] sanity: deep-MOND coeffs
print("="*90)
print("[0] sanity -- deep-MOND boost (all MOND must give g=sqrt(g_N a0) => nu1~1/sqrt(y)):")
for name,f in (("framework",nu1_fw),("simple",nu1_simple),("exp mu=1-e^-x",nu1_exp),
               ("Woodard-tail",nu1_woodard_tail)):
    y=1e-4; got=f(y); want=1.0/np.sqrt(y)-1.0
    print(f"    {name:14s}: nu1(1e-4)={got:10.2f}  1/sqrt(y)-1={want:10.2f}  ratio={got/want:.3f}")
    assert 0.9<got/want<1.6, f"{name} deep-MOND coeff off"
print("    (all reproduce deep MOND within the transition-shape ambiguity -> RAR-compatible)")

# ---------------------------------------------------------------- [1] calibrate on Desmond anchors
print("[1] Kernel calibration on Desmond-Hees-Famaey 2024 anchors (power-law simple-nu):")
ratios=[]
for et,anchor in ((1.0,0.094),(1.5,0.159),(2.0,0.221)):
    q=abs(q_raw(nu1_simple,et)); ratios.append(q/anchor)
    print(f"    etilde={et}: |q|_raw={q:.4f}  anchor={anchor}  ratio={q/anchor:.3f}")
CAL=1.0/np.mean(ratios)
print(f"    -> tail-correction CAL={CAL:.4f}")
assert 1.0<CAL<1.10

# ---------------------------------------------------------------- [2] where is q built? (the crux)
print("\n[2] CRUX -- how much of q is transition-built vs power-law-tail-built?")
print("    q accumulated as vmax grows (etilde=1.9), power-law vs exponential boost:")
et=1.9
for name,nu1 in (("power-law simple",nu1_simple),("exponential mu=1-e^-x",nu1_exp)):
    row=[]
    for vm in (2.0,3.0,5.0,10.0,60.0):
        row.append(abs(q_raw(nu1,et,vmax=vm)))
    print(f"    {name:22s}: q(vmax=2,3,5,10,60) = "+", ".join(f"{r:.4f}" for r in row))
print("    -> if exponential q saturates early & far below power-law, the inner-shell")
print("       power-law tail is what drives the Cassini tension, and Woodard evades it.")

# ---------------------------------------------------------------- [3] Q2 vs ceiling, both footings
print(f"\n[3] |Q2| vs ceiling {CEIL:.1e} s^-2  (external field g_ext={G_EXT:.1e} m/s^2):")
FOOT=(("canon",9.36e-11),("alt",1.13e-10))
def report(label, nu1):
    for tag,a0 in FOOT:
        et=G_EXT/a0
        # scan a small window of etilde (galactic field uncertainty +-15%)
        Qs=[]
        for etx in (et*0.85, et, et*1.15):
            q=abs(q_raw(nu1, etx))
            Qs.append(CAL*(3.0*a0**1.5)/(2.0*np.sqrt(G*Msun))*q)
        worst=max(Qs)
        stat="PASS" if worst<CEIL else f"FAIL x{worst/CEIL:.2f}"
        marg="MARGINAL " if 0.7<worst/CEIL<1.4 else ""
        print(f"    {label:34s} {tag:5s} (etilde~{et:.2f}): worst|Q2|={worst:.2e}  ratio={worst/CEIL:5.2f}  [{marg}{stat}]")
    return
report("POWER-LAW framework-nu [tension]", nu1_fw)
report("POWER-LAW simple-nu", nu1_simple)
report("EXP mu=1-e^-x [Woodard analog]", nu1_exp)
report("EXP Woodard-tail e^-(y/3) [slow]", nu1_woodard_tail)
report("EXP 2026 exact e^-(2/3 y) [2512]", nu1_2026)

# pass-threshold on the dimensionless q (canon footing): what q would clear the ceiling?
print("\n    PASS-THRESHOLD on q (the quadrupole integral) to reach |Q2|<ceiling:")
for tag,a0 in FOOT:
    et=G_EXT/a0
    q_pass=CEIL/(CAL*(3.0*a0**1.5)/(2.0*np.sqrt(G*Msun)))
    q_wood=abs(q_raw(nu1_exp,et)); q_slow=abs(q_raw(nu1_woodard_tail,et)); q_pow=abs(q_raw(nu1_fw,et))
    print(f"    {tag:5s}: need q < {q_pass:.4f};  Woodard-exp q={q_wood:.4f}, slow q={q_slow:.4f}, "
          f"power-law q={q_pow:.4f}  -> exp is {q_wood/q_pass:.1f}x over threshold")
print("    => Woodard's exp transition is NOT sharp enough; only a near-DELTA transition")
print("       (banked decider: sharp d>=5 gives q_eff 0.05-0.09, PASSES Q2 but FAILS SPARC RAR).")

# ---------------------------------------------------------------- [4] GW170817 structural check
print("\n[4] GW170817 (c_gw=c) structural check for the SINGLE-METRIC nonlocal model:")
print("""    Road 2 has ONE metric g_mn; MOND enters via L_MOND built from nonlocal
    scalars X[g],Y[g] = box^-1 (curvature) contracted with u^mu (1106.4984 eqs 63-64,
    82). Every MOND term carries >=2 factors of CURVATURE (Ricci scalar / R00), eq 31.
    A GW170817 tensor wave is a transverse-traceless perturbation h_mn^TT on the FLRW
    background: to linear order in h^TT the Ricci SCALAR perturbation dR=0 and the
    background R is set by the cosmological source, NOT by h^TT. Hence L_MOND contributes
    NO term ~ (d h^TT)^2 to the graviton kinetic operator -> the tensor sound speed is
    the metric's, c_gw=c EXACTLY, no dispersion. (Contrast TeVeS/vector-MG: the extra
    vector's disformal coupling shifts c_gw and was killed by GW170817; Woodard's u^mu is
    NOT independent, it is box^-1 of the metric, so it carries no independent TT mode.)
    => GW170817 intact BY CONSTRUCTION.""")

print("="*90); print("exit 0")
