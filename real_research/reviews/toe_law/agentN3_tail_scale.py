#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agentN3_tail_scale.py — THE SCALE QUESTION for the non-Huygens (light-scalar) tail escape.
2026-06-10. Companion to agentN3_tail_scale.md. House rules: raw numbers first, post-hoc
comparisons flagged; both ways at full weight; every external pin carries an arXiv id.

Task (from the swarm prompt): for a LIGHT scalar in dS (m << H; physically motivated candidate:
the dark-energy field itself, m ~ H — motivation only, nothing claimed):
 (1) the TAIL amplitude of the retarded Green function inside the light cone (closed form, m/H scaling;
     IR signature <phi^2> = 3H^4/8pi^2m^2);
 (2) the induced memory-force magnitude on a worldline of proper acceleration a, coupling lambda,
     as a function of (lambda, m/H, a/H);
 (3) the WINDOW QUESTION: any (lambda, m/H) where the tail term ~ m*a0 at a ~ a0 = 9.36e-11 while
     below the banked solar budgets (Saturn quadratic-tail 2.3e-15; agentE survival line s < 0.34 a0
     magnitude-keyed; frequency-suppressed (H/Omega)^p, p in {1,2}, bracketed for N2);
 (4) RAW coefficients from exact pieces BEFORE comparison; Z/2/2pi comparison flagged post-hoc.

Pinned external anchors (ids verified 2026-06-10):
  [BHP]  Burko, Harte & Poisson, PRD 65, 124006 (2002), arXiv:gr-qc/0201020 — dS tail of the massless
         minimally coupled retarded GF is CONSTANT (their eq. 6.1: G_smooth = 1/C^2 = H^2 in their
         4pi-Gaussian normalization, eq. 2.10) and the comoving charge loses mass at dm/dtau = -q^2 H^2
         (their eq. 6.8) — all mass radiated in finite proper time.
  [HP]   Haas & Poisson, arXiv:gr-qc/0411108 — extension (mass change of scalar charges in cosmology).
  [Q]    Quinn, PRD 62, 064029 (2000), arXiv:gr-qc/0005030 — scalar self-force + dm/dtau axiomatics
         (the tail-integral + R/12 structure used by BHP eq. 2.9).
  [SY]   Starobinsky & Yokoyama, PRD 50, 6357 (1994), arXiv:astro-ph/9407016 — equilibrium variance
         <phi^2> = 3H^4/(8 pi^2 m^2); growth law H^3 t/4pi^2 before equilibration.
  [DL]   Deser & Levin, CQG 14, L163 (1997), arXiv:gr-qc/9706018 — T_eff = sqrt(a^2+H^2)/2pi family.
  [SSV]  Spradlin, Strominger & Volovich, arXiv:hep-th/0110007 — standard BD hypergeometric two-point
         function W(P) = (H^2/16pi^2) Gamma(h+)Gamma(h-) 2F1(h+,h-;2;(1+P)/2), h± = 3/2 ± nu,
         nu = sqrt(9/4 - m^2/H^2).
  [WILL] Will, Living Rev. Rel. 17, 4 (2014), arXiv:1403.7377 — Cassini: gamma-1 = (2.1±2.3)e-5
         => universal-scalar coupling beta^2 < 1.15e-5 (gamma-1 = -2beta^2/(1+beta^2)).
  [MIC]  MICROSCOPE final, PRL 129, 121102 (2022), arXiv:2209.15487 — eta(Ti,Pt) =
         [-1.5±2.3(stat)±1.5(syst)]e-15 (binds composition-DEPENDENT couplings far harder).
  [CAR]  Carroll, arXiv:astro-ph/9806099 — quintessence couplings to matter must be suppressed well
         below Planck/gravitational strength or long-range-force/varying-constant bounds fire.
  [JJKT] Joyce, Jain, Khoury & Trodden, Phys. Rept. 568, 1 (2015), arXiv:1407.0059 — screening review
         (the chameleon caveat: local screening would also kill the galactic-field enhancement).
Internal (repo): MI_BATH_TAIL_CONSTRAINT.md, MI_COUPLING_FAMILY.md, agentB_door1_*, agentF_nonpert_*
(the blindness lemma this door escapes), agentE_solar_reflex.* (survival line), TOE_STATUS_AND_DOORS.md.
"""

import numpy as np
import sympy as sp
import mpmath as mp
from numpy.polynomial.legendre import leggauss

mp.mp.dps = 30
LINE = "-" * 100

def hdr(tag, title):
    print("\n" + "=" * 100)
    print(f"[{tag}] {title}")
    print("=" * 100)

# ----------------------------------------------------------------------------------------------
hdr("N3-0", "CONVENTIONS & CONSTANTS (repo footings carried BOTH ways per the working rule)")
# ----------------------------------------------------------------------------------------------
c_SI    = 2.99792458e8        # m/s
hbar_SI = 1.054571817e-34     # J s
G_SI    = 6.67430e-11         # m^3/kg/s^2
eV_J    = 1.602176634e-19     # J
Mpc_m   = 3.0856775814913673e22
yr_s    = 3.155814954e7

a0      = 9.36e-11            # m/s^2  framework kernel a0 = c^2 sqrt(Lambda/32pi)  (banked)
Zfac    = 5.789               # data-selected; NO derivation claim on the table
cHL     = 5.418e-10           # m/s^2  = Z*a0  (rho_DE footing; agentE value)
cH0     = 6.55e-10            # m/s^2  (rho_total footing, both-ways)
a0_MOND = 1.2e-10             # regular-MOND default (working-rule baseline)
HL_SI   = cHL / c_SI          # s^-1
H0_SI   = cH0 / c_SI

# natural-unit conversions (everything via eV)
H_eV   = hbar_SI * HL_SI / eV_J                 # Hubble (Lambda footing) in eV
acc_eV = hbar_SI / c_SI / eV_J                  # multiply SI accel by this -> eV (a_nat = hbar a/c)
m_p_eV   = 938.27208816e6
M_red_eV = 2.435323e27                           # reduced Planck mass, eV

# sanity: cH as an acceleration must equal H in natural units
assert abs(acc_eV * cHL / H_eV - 1) < 1e-9, "natural-unit conversion broken"
print(f"  H_Lambda = {HL_SI:.4e} s^-1 = {H_eV:.4e} eV ;  1/H_Lambda = {1/HL_SI/yr_s/1e9:.2f} Gyr")
print(f"  a0 = {a0:.3e} m/s^2 ; cH_Lambda = {cHL:.3e} ; Z = cH_L/a0 = {cHL/a0:.3f}")
print(f"  x_gal == a0/cH_Lambda = {a0/cHL:.4f} (=1/Z) ; both-ways alt: a0_MOND/cH0 = {a0_MOND/cH0:.4f}")
print(f"  m_p = {m_p_eV:.4e} eV ; M_Pl,red = {M_red_eV:.4e} eV ; m_p/M_red = {m_p_eV/M_red_eV:.4e}")
print(f"  H/M_red = {H_eV/M_red_eV:.4e}   <- the hierarchy that will decide the window")

# banked solar budgets (internal pins)
SAT_QUAD   = 2.3e-15   # m/s^2  quadratic-tail Saturn budget (MI_COUPLING_FAMILY.md)
FOLKNER    = 1.0e-14   # m/s^2  Cassini radiometric Saturn radial (arXiv:1001.3686 via repo pin)
AGENTE_S   = 3.21e-11  # m/s^2  agentE survival line s < 3.21..3.76e-11 (= 0.34..0.40 a0), Mars-carried
A_SUN      = 2.1e-7    # m/s^2  Sun's Jupiter-driven reflex (agentE [2])
SUN_BUDGET = AGENTE_S**2 / (2 * A_SUN)  # the solar-response magnitude the survival line tolerates
A_SAT      = 6.46e-5   # m/s^2  Saturn g_N (MI_BATH_TAIL_CONSTRAINT.md)
A_MARS     = 1.327e20 / (1.523679 * 1.495978707e11) ** 2
x_sat, x_sun, x_mars = A_SAT / cHL, A_SUN / cHL, A_MARS / cHL
print(f"  budgets: Saturn quad-tail {SAT_QUAD:.1e} ; Folkner {FOLKNER:.0e} ; agentE line s<{AGENTE_S:.2e}"
      f" => solar-response budget {SUN_BUDGET:.2e} m/s^2")
print(f"  x (=a/cH_L): Sun {x_sun:.1f} ; Saturn {x_sat:.3e} ; Mars {x_mars:.3e} ; galaxy 0.0018..1.8")

# Lambda-domination span (the equilibration cap): flat LCDM lookback to z
Om, OL, H0_km = 0.315, 0.685, 67.4
H0_t = H0_km * 1e3 / Mpc_m
zz = np.linspace(0, 0.8, 4001)
Ez = np.sqrt(Om * (1 + zz) ** 3 + OL)
def t_lookback(z):
    m_ = zz <= z
    return np.trapz(1.0 / ((1 + zz[m_]) * Ez[m_]), zz[m_]) / H0_t
z_eq, z_acc = (OL / Om) ** (1 / 3) - 1, (2 * OL / Om) ** (1 / 3) - 1
t_eq, t_acc = t_lookback(z_eq), t_lookback(z_acc)
TDS_LO, TDS_HI = t_eq * HL_SI, t_acc * HL_SI
TDS_MID = 0.5 * (TDS_LO + TDS_HI)
print(f"  Lambda-domination z={z_eq:.3f} (t={t_eq/yr_s/1e9:.2f} Gyr) ; accel onset z={z_acc:.3f} "
      f"(t={t_acc/yr_s/1e9:.2f} Gyr)  =>  t_dS*H_Lambda in [{TDS_LO:.3f}, {TDS_HI:.3f}], mid {TDS_MID:.3f}")

# ----------------------------------------------------------------------------------------------
hdr("N3-A1", "EXACT PIECE 1 (sympy): massless minimally coupled scalar in dS4 — retarded tail = H^2/4pi,"
             " CONSTANT inside the cone [matches BHP gr-qc/0201020 eq. 6.1 after 4pi-normalization]")
# ----------------------------------------------------------------------------------------------
# conformal frame: a(eta) = -1/(H eta), phi = psi/a ; psi'' + (k^2 - 2/eta^2) psi = 0
eta, k = sp.symbols("eta k", negative=True), sp.symbols("k", positive=True)
eta = sp.symbols("eta", negative=True)
u = sp.exp(-sp.I * k * eta) / sp.sqrt(2 * k) * (1 - sp.I / (k * eta))   # Bunch-Davies mode
eom = sp.simplify(sp.diff(u, eta, 2) + (k**2 - 2 / eta**2) * u)
wr  = sp.simplify(u * sp.diff(sp.conjugate(u), eta) - sp.conjugate(u) * sp.diff(u, eta))
print(f"  BD mode u_k = e^(-ik eta)(1 - i/(k eta))/sqrt(2k):  EOM residual = {eom}   Wronskian u u*' - u* u' = {wr}")
assert eom == 0 and sp.simplify(wr - sp.I) == 0

# commutator mode-sum: Im[u_k(eta) u_k*(eta')] = (1/2k)[ -(1+1/(k^2 eta eta')) sin(k D) + (D/(k eta eta')) cos(k D) ]
etap = sp.symbols("etap", negative=True)
D = sp.symbols("Delta", positive=True)   # D = eta - eta' > 0
prod = sp.expand(u * (sp.conjugate(u).subs(eta, etap)))
imexp = sp.simplify(sp.im(prod.rewrite(sp.cos)).subs(eta - etap, D))
target = (-(1 + 1/(k**2*eta*etap))*sp.sin(k*D) + (D/(k*eta*etap))*sp.cos(k*D))/(2*k)
chk = sp.simplify(sp.expand_trig(imexp - target.subs(D, eta - etap)))
print(f"  Im[u u*'] structure check (should be 0): {chk}")
assert chk == 0

# the two tail k-integrals (Dirichlet primitives, sympy-exact):
p_, q_ = sp.symbols("p q", positive=True)
I_one_minus_cos = sp.integrate((1 - sp.cos(p_ * k)) / k**2, (k, 0, sp.oo))
I_sin_over_k    = sp.integrate(sp.sin(p_ * k) / k, (k, 0, sp.oo))
print(f"  primitives: Int (1-cos pk)/k^2 = {I_one_minus_cos} ;  Int sin(pk)/k = {I_one_minus_cos*0 + I_sin_over_k}")
# => Int sin(ak)sin(bk)/k^2 dk = (pi/2) min(a,b) ;  Int cos(ak)sin(bk)/k dk = (pi/2) theta(b-a)
# Assembly (G_R = -2 theta(D) (a a')^{-1} Int d^3k/(2pi)^3 e^{ik.x} Im[u u*'] ; angular -> (1/2pi^2 r) Int k sin(kr)):
#   cone term:  delta(D - r)/(4 pi r a a')                                  [flat-form, exact]
#   tail terms (inside cone, D > r):
#     (1/(eta eta')) * (1/(2 pi^2 r)) * [ (pi/2) r  -  D * 0 ]  =  1/(4 pi eta eta')
#   with a a' eta eta' = 1/H^2  =>  TAIL = H^2/(4 pi) * theta(D - r).      [EXACT]
aap = sp.simplify(((-1 / (sp.Symbol('H', positive=True) * eta)) * (-1 / (sp.Symbol('H', positive=True) * etap))) * eta * etap)
print(f"  a(eta) a(eta') eta eta' = {aap}  =>  TAIL of G_ret = H^2/(4 pi), constant inside the cone. [EXACT]")
print("  cross-anchor [BHP eq. 6.1]: G_smooth = 1/C^2 = H^2 in their gauss-4pi normalization (eq. 2.10:")
print("  box G = -4pi delta/sqrt(-g)); divide by 4pi -> H^2/4pi. Consistency: their dS mass-loss eq. 6.8")
print("  dm/dtau = -q^2 H^2 (gauss) = -q^2 H^2/4pi (natural) = q * d/dtau[q (H^2/4pi) tau] — the SAME tail. OK")

# ----------------------------------------------------------------------------------------------
hdr("N3-A2", "EXACT PIECE 2 (mpmath): the MASSIVE tail V(P) in dS from the BD hypergeometric"
             " discontinuity [SSV hep-th/0110007 form] — four independent anchors")
# ----------------------------------------------------------------------------------------------
# W(P) = (H^2/16pi^2) G(h+)G(h-) 2F1(h+,h-;2;(1+P)/2), h± = 3/2 ± nu, nu = sqrt(9/4 - (m/H)^2)
# G_R = 2 theta Im W(P + i eps)  (BD ieps; branch orientation fixed by the m->0 anchor below, printed)
# Hadamard transport gives the EXACT cone value: V(P->1+) = -(1/8pi)[m^2 + (xi-1/6)R] ; xi=0, R=12H^2
#   =>  V_cone = (H^2/4pi) (1 - m^2/(2H^2)).   Conformal point m^2 = 2H^2: tail vanishes IDENTICALLY
#   (2F1(2,1;2;w) = 1/(1-w), pure pole, no discontinuity) — Door I's Huygens class sits at the zero.
def nu_of(mh):  return mp.sqrt(mp.mpf(9) / 4 - mp.mpf(mh) ** 2)
def hm_of(mh):  return mp.mpf(3) / 2 - nu_of(mh)

_SIGN = None
def v_raw(P, mh):
    """4pi * V(P) / H^2 with V = 2 Im W(P+ieps); plateau -> 1 as m -> 0."""
    nu = nu_of(mh); hp, hm = mp.mpf(3)/2 + nu, mp.mpf(3)/2 - nu
    w = (1 + mp.mpf(P)) / 2
    F = mp.hyp2f1(hp, hm, 2, mp.mpc(w, mp.mpf(10) ** (-mp.mp.dps + 8) * max(1, abs(w))))
    pref = mp.gamma(hp) * mp.gamma(hm) / (2 * mp.pi)      # = 4pi/H^2 * 2 * (1/16pi^2) * G G
    return float(pref * mp.im(F))

s_probe = v_raw(1 + 1e-6, 0.5)
_SIGN = 1.0 if s_probe > 0 else -1.0
def v_tail(P, mh): return _SIGN * v_raw(P, mh)
print(f"  branch orientation: raw Im at (mh=0.5, P=1+1e-6) = {s_probe:+.6f} -> global sign {_SIGN:+.0f} applied")
print(f"  calibration check vs EXACT cone value (1 - mh^2/2): {v_tail(1+1e-6,0.5):.6f} vs {1-0.5**2/2:.6f}")

print("\n  anchor (i): m->0 plateau == 1 (BHP constant tail), mh = 0.01:")
for P in (1.001, 2.0, 10.0, 1e3, 1e6):
    print(f"     v(P={P:>8.3g}) = {v_tail(P, 0.01):+.6f}")
print("  anchor (ii): cone values v(1+) vs EXACT (1 - mh^2/2)  [Hadamard transport]:")
for mh in (0.1, 0.5, 1.0, 1.3, 1.45):
    va, ve = v_tail(1 + 1e-7, mh), 1 - mh**2/2
    print(f"     mh={mh:4.2f}: numeric {va:+.6f}  exact {ve:+.6f}  ratio {va/ve:+.6f}")
print("  anchor (iii): conformal point mh = sqrt(2): v should vanish for ALL P:")
for P in (1.001, 10.0, 1e4):
    print(f"     v(P={P:>8.3g}) = {v_tail(P, float(mp.sqrt(2))):+.3e}")
print("  anchor (iv): large-P falloff exponent -> h- = 3/2 - nu  (fit d ln v/d ln P, P in [e^25, e^33]):")
for mh in (0.3, 0.5, 1.0, 1.3):
    lp = np.linspace(25, 33, 9)
    lv = np.log(np.abs([v_tail(float(np.exp(u_)), mh) for u_ in lp]))
    slope = np.polyfit(lp, lv, 1)[0]
    print(f"     mh={mh:4.2f}: fitted slope {slope:+.5f}  vs  -h- = {-float(hm_of(mh)):+.5f}")

# ----------------------------------------------------------------------------------------------
hdr("N3-A3", "EXACT PIECE 3 (sympy): the IR signature — SY equilibrium variance & the equilibration cap"
             " [SY astro-ph/9407016]")
# ----------------------------------------------------------------------------------------------
phi, m_, H_ = sp.symbols("phi m H", positive=True)
rho_eq = sp.exp(-sp.Rational(8) * sp.pi**2 * (m_**2 * phi**2 / 2) / (3 * H_**4))
var = sp.simplify(sp.integrate(phi**2 * rho_eq, (phi, -sp.oo, sp.oo)) / sp.integrate(rho_eq, (phi, -sp.oo, sp.oo)))
print(f"  SY equilibrium <phi^2> = {var}   [target 3H^4/(8 pi^2 m^2)]")
assert sp.simplify(var - 3 * H_**4 / (8 * sp.pi**2 * m_**2)) == 0
t_ = sp.symbols("t", positive=True)
sol = sp.dsolve(sp.Derivative(sp.Function('y')(t_), t_) - (H_**3/(4*sp.pi**2) - (2*m_**2/(3*H_))*sp.Function('y')(t_)),
                sp.Function('y')(t_), ics={sp.Function('y')(0): 0})
y_inf = sp.limit(sol.rhs, t_, sp.oo)
print(f"  Langevin balance d<phi^2>/dt = H^3/4pi^2 - (2m^2/3H)<phi^2>: equilibrium = {sp.simplify(y_inf)}")
print(f"  relaxation time tau_relax = 3H/(2 m^2) = 1.5 (H/m)^2 / H ;  growth law (m->0): <phi^2> = H^3 t/4pi^2")
for mh in (0.1, 0.3, 1.0):
    print(f"     mh={mh:4.1f}: tau_relax*H = {1.5/mh**2:8.2f}  vs t_dS*H = {TDS_MID:.2f}"
          f"  -> equilibrated? {'NO — cap binds' if 1.5/mh**2 > TDS_MID else 'marginal/yes'}")
print(f"  => the 3H^4/8pi^2m^2 enhancement is NOT available in our universe for m << H: usable variance")
print(f"     is capped at H^3 t_dS/4pi^2 = {TDS_MID/(4*np.pi**2):.4f} H^2 (m-independent).  [SY + Lambda timeline]")

# ----------------------------------------------------------------------------------------------
hdr("N3-A4", "EXACT PIECE 4 (sympy): Deser-Levin worldline invariant — P(dtau) = 1 + (2H^2/k^2) sinh^2(k dtau/2),"
             " kappa = sqrt(a^2+H^2)  [DL gr-qc/9706018]")
# ----------------------------------------------------------------------------------------------
r0, tb1, tb2, Hs = sp.symbols("r_0 t_1 t_2 H", positive=True)
f0 = sp.sqrt(1 / Hs**2 - r0**2)
X  = lambda t: (f0 * sp.sinh(Hs * t), f0 * sp.cosh(Hs * t), r0)      # static-patch worldline embedding
P_emb = sp.simplify(Hs**2 * (-X(tb1)[0]*X(tb2)[0] + X(tb1)[1]*X(tb2)[1] + X(tb1)[2]*X(tb2)[2]))
P_tgt = (1 - Hs**2*r0**2) * sp.cosh(Hs*(tb1 - tb2)) + Hs**2*r0**2
print(f"  embedding P = H^2 X.X' - target check: {sp.simplify(P_emb - P_tgt)}")
assert sp.simplify(P_emb - P_tgt) == 0
# proper acceleration of the static worldline (Christoffels of the static patch):
rr, tt = sp.symbols("r t", positive=True)
gtt = -(1 - Hs**2 * rr**2); grr = 1 / (1 - Hs**2 * rr**2)
ut = 1 / sp.sqrt(-gtt)
Gamma_rtt = -sp.Rational(1, 2) * (1 / grr) * sp.diff(gtt, rr)
a_r = sp.simplify(Gamma_rtt * ut**2)            # a^r = Gamma^r_tt (u^t)^2
a_mag = sp.simplify(sp.sqrt(grr) * a_r)         # |a| = sqrt(g_rr) a^r
kap2 = sp.simplify(a_mag**2 + Hs**2)
print(f"  |a| = {a_mag} ;  a^2 + H^2 = {sp.factor(kap2)} = H^2/(1-H^2 r^2)")
# proper time dtau = sqrt(1-H^2 r0^2) dt, and 1-H^2 r0^2 = H^2/kappa^2:
dtau = sp.symbols("dtau", positive=True); kapp = sp.symbols("kappa", positive=True)
P_proper = (1 + (Hs**2/kapp**2) * (sp.cosh(kapp * dtau) - 1))
print(f"  => P(dtau) = 1 + (H^2/k^2)(cosh(k dtau) - 1) = 1 + (2H^2/k^2) sinh^2(k dtau/2), k = sqrt(a^2+H^2)  [EXACT]")
print(f"     T_eff = kappa/2pi [DL]; geodesic a=0: P = cosh(H dtau) OK ; flat H->0: Rindler sinh^2 OK")
print(f"  NOTE: this P(dtau; a) is what the massive tail V(P) sees -> the dissipation kernel is")
print(f"  TRAJECTORY-DEPENDENT — the structure agentF's blindness lemma says is the unique bath-side escape.")

# ----------------------------------------------------------------------------------------------
hdr("N3-B1", "THE MEMORY DRESSING: dm(a) = -q^2 (H^2/4pi) tau_eff(a/H; m/H)  [BHP/Quinn lineage:"
             " m_eff = m0 + q*phi_self, phi_self = -q Int G_ret -> mass-REDUCING]")
# ----------------------------------------------------------------------------------------------
# tau_eff(x; mh) = Int_0^{cap} v(P(dtau; x)) ddtau   (H=1 units; v = 4pi V/H^2; uncapped = steady state)
GL_N = 64
gl_x, gl_w = leggauss(GL_N)

def make_spline(mh, lnPmax=35.0):
    # sample on P-1 log grid for the near-cone region and lnP grid for the far region
    P1 = 1 + np.exp(np.linspace(np.log(1e-8), np.log(20.0), 60))
    P2 = np.exp(np.linspace(np.log(21.0), lnPmax, 80))
    Ps = np.concatenate([P1, P2])
    vs = np.array([v_tail(float(P), mh) for P in Ps])
    lnPs = np.log(Ps)
    def v_int(P):
        lp = np.log(P)
        if lp >= lnPs[-1]:                            # asymptotic continuation A P^{-h-}
            return vs[-1] * np.exp(-(lp - lnPs[-1]) * hm_f)
        return np.interp(lp, lnPs, vs)
    hm_f = float(hm_of(mh))
    return v_int, hm_f, float(vs[-1]), float(lnPs[-1])

def tau_eff(x, spl, cap=None):
    """integral of v(P(dtau;x)) ddtau, H=1; cap in units 1/H (None = steady state)."""
    v_int, hm_f, v_end, lnP_end = spl
    kap = np.sqrt(1 + x * x)
    bet = 2.0 / kap**2
    # y = kappa * dtau ; P(y) = 1 + bet sinh^2(y/2) ; split where ln P = lnP_end
    sh2_end = (np.exp(lnP_end) - 1) / bet
    Y_end = 2 * np.arcsinh(np.sqrt(sh2_end))
    Y_cap = kap * cap if cap is not None else np.inf
    Y_num = min(Y_end, Y_cap)
    # numeric part on [0, Y_num] (split into <=3 GL segments in y, integrand smooth)
    segs = [s for s in (0.0, 2.0, 20.0, Y_num) if s < Y_num] + [Y_num]
    segs = sorted(set(min(s, Y_num) for s in segs))
    tot = 0.0
    for a_, b_ in zip(segs[:-1], segs[1:]):
        ym = 0.5 * (b_ - a_) * gl_x + 0.5 * (b_ + a_)
        Pm = 1 + bet * np.sinh(ym / 2) ** 2
        tot += 0.5 * (b_ - a_) * np.sum(gl_w * np.array([v_int(P) for P in Pm]))
    if cap is None and Y_end < np.inf:
        # analytic remainder: Int v dy = v(P_end) / h-   (d lnP/dy -> 1)
        tot += v_end / hm_f
    elif cap is not None and Y_cap > Y_end:
        # capped but beyond spline: asymptotic piece up to Y_cap
        tot += (v_end / hm_f) * (1 - np.exp(-hm_f * (Y_cap - Y_end)))
    return tot / kap

MH_GRID = [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 1.2, 1.3, 1.40, 1.45]
X_GRID  = [0.0, 0.01727, 0.1, 0.17277, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, x_sun, 1e3, 1e4, x_sat, x_mars]
X_LBL   = {0.17277: "a0(frame)", 0.01727: "a0/10", x_sun: "SUN", x_sat: "SATURN", x_mars: "MARS"}

print("  building tail splines (mpmath hyp2f1) ...")
SPL = {mh: make_spline(mh) for mh in MH_GRID}

print("\n  tau_eff(x; mh) * H   — STEADY-STATE (eternal-dS idealization).  small-m anchor:"
      " tau_eff(0) -> (1/h-)(1/2)^{h-} ~ 3H/m^2:")
print(f"  {'x':>12s} | " + " | ".join(f"mh={mh:<5.3g}" for mh in MH_GRID))
T_STEADY = {}
for x in X_GRID:
    row = []
    for mh in MH_GRID:
        T_STEADY[(x, mh)] = tau_eff(x, SPL[mh])
        row.append(f"{T_STEADY[(x, mh)]:9.3g}")
    lbl = X_LBL.get(x, "")
    print(f"  {x:12.4g} | " + " | ".join(row) + ("   <- " + lbl if lbl else ""))
for mh in (0.05, 0.1, 0.3):
    pred = (1 / float(hm_of(mh))) * 0.5 ** float(hm_of(mh))
    print(f"  check tau_eff(0; mh={mh}) = {T_STEADY[(0.0,mh)]:.4g} vs (1/h-)(1/2)^h- = {pred:.4g}"
          f"  (h- = {float(hm_of(mh)):.4g}; small-m law 3/mh^2 = {3/mh**2:.4g})")

print("\n  CAPPED at t_dS (physical universe, t_dS*H = " f"{TDS_MID:.2f}): tau_eff^cap(x; mh)*H:")
T_CAP = {}
print(f"  {'x':>12s} | " + " | ".join(f"mh={mh:<5.3g}" for mh in MH_GRID))
for x in X_GRID:
    row = []
    for mh in MH_GRID:
        T_CAP[(x, mh)] = tau_eff(x, SPL[mh], cap=TDS_MID)
        row.append(f"{T_CAP[(x, mh)]:9.3g}")
    lbl = X_LBL.get(x, "")
    print(f"  {x:12.4g} | " + " | ".join(row) + ("   <- " + lbl if lbl else ""))

print("\n  SELF-CAUGHT CORRECTION (bug-log discipline): the pre-registered guess for the high-a falloff of")
print("  tau_eff was the P-space power x^-(1+2h-). The computation REFUTES it: the worldline integral is")
print("  dominated by the NEAR-CONE plateau (recent past, P ~ 1 for y < ~2 ln kappa), giving the EXACT-asym law")
print("       tau_eff(x>>1) ~ (v_cone/kappa) * (2 ln kappa + 1/h- + c0),   v_cone = 1 - mh^2/2")
print("  i.e. a (ln x)/x tail — the LINEAR-tail (F1/Milgrom-99) ephemeris class, at EVERY mass. Verification:")
for mh in (0.3, 1.0, 1.3):
    vc, hmf = 1 - mh**2/2, float(hm_of(mh))
    for xq in (1e3, 1e4):
        kap = np.sqrt(1 + xq**2)
        pred = (vc/kap) * (2*np.log(kap) + 1/hmf)          # c0 absorbed: report raw vs 2lnk+1/h-
        print(f"     mh={mh:4.2g}, x={xq:8.3g}: tau_eff*kappa/v_cone = {T_STEADY[(xq,mh)]*kap/vc:8.3f}"
              f"  vs  2 ln kappa + 1/h- = {2*np.log(kap)+1/hmf:8.3f}   (c0 = {T_STEADY[(xq,mh)]*kap/vc - 2*np.log(kap)-1/hmf:+6.3f})")
print("  (consequence: there is NO mass-tunable solar-safe exponent corridor; see [N3-B3].)")

print("\n  profile diagnostics g(x) = tau_eff(x)/tau_eff(0)  [steady-state]:")
print(f"  {'mh':>6s} | {'g(x_gal)':>9s} | {'g(SUN)':>9s} | {'g(SATURN)':>10s} | hi-x slope fit (1e3->1e4) | x at 10% drop (capped)")
for mh in MH_GRID:
    g_gal = T_STEADY[(0.17277, mh)] / T_STEADY[(0.0, mh)]
    g_sun = T_STEADY[(x_sun, mh)] / T_STEADY[(0.0, mh)]
    g_sat = T_STEADY[(x_sat, mh)] / T_STEADY[(0.0, mh)]
    xs = np.array([1e3, 1e4]); gs = np.array([T_STEADY[(1e3, mh)], T_STEADY[(1e4, mh)]])
    expo = np.log(gs[1]/gs[0]) / np.log(xs[1]/xs[0])
    # capped-profile bend: first x with g_cap < 0.9
    xbend = None
    for xq in np.logspace(-1, 5, 61):
        if tau_eff(xq, SPL[mh], cap=TDS_MID) / T_CAP[(0.0, mh)] < 0.9:
            xbend = xq; break
    print(f"  {mh:6.3g} | {g_gal:9.3g} | {g_sun:9.3g} | {g_sat:10.3g} | {expo:+8.3f} (log/x law: ~ -0.9)"
          f" | {xbend if xbend else float('nan'):9.3g}")
print("  -> sign: dm < 0 (inertia DEFICIT, larger at low a) for mh < sqrt(2): the MOND sign — the first")
print("     MOND-signed object any bath channel has produced (Doors I/I-b were anti-MOND). Flagged for N2:")
print("     the deep limit SATURATES (g -> 1, mu -> 1 - eps = const) — NOT the mu ~ x deep-MOND structure;")
print("     and in the CAPPED (physical) case the profile is FLAT across the entire galactic decade")
print("     (bend sits at x >~ 30-100): the a-dependence MOND needs at x ~ 0.02..2 is not there. [structure: N2's lane]")

# ----------------------------------------------------------------------------------------------
hdr("N3-B2", "WINDOW CHANNEL (i) — THE COUPLING WALL. Required: |dm|/m ~ O(1) at x_gal."
             "  dm = -q^2 (H^2/4pi) tau_eff ; q = beta m/M_red (universal quintessence coupling)")
# ----------------------------------------------------------------------------------------------
# eps(beta, mh; x) = |dm|/m_p = (beta^2 m_p / M_red^2) (H^2/4pi) tau_eff(x; mh)/H^2... all in eV:
def eps_per_nucleon(beta, mh, x, capped=True):
    tau = (T_CAP if capped else T_STEADY)[(x, mh)]          # in 1/H units
    return beta**2 * (m_p_eV / M_red_eV**2) * (H_eV**2 / (4 * np.pi)) * (tau / H_eV) / m_p_eV * m_p_eV**2 / m_p_eV
# simplify: eps = beta^2 (m_p/M_red)(H/M_red) * tau_eff*H / 4pi   — dimensionless, verify:
def eps_clean(beta, mh, x, capped=True):
    tau = (T_CAP if capped else T_STEADY)[(x, mh)]
    return beta**2 * (m_p_eV / M_red_eV) * (H_eV / M_red_eV) * tau / (4 * np.pi)
assert abs(eps_per_nucleon(1, 1.0, 0.0) / eps_clean(1, 1.0, 0.0) - 1) < 1e-12
BETA_CASSINI = np.sqrt(1.15e-5)        # [WILL] gamma-1 = -2 beta^2/(1+beta^2), |gamma-1| < 2.3e-5
x_g = 0.17277
print(f"  eps(x_gal) = |dm|/m per nucleon = beta^2 (m_p/M_red)(H/M_red) tau_eff H/4pi ;"
      f" (m_p/M_red)(H/M_red) = {(m_p_eV/M_red_eV)*(H_eV/M_red_eV):.3e}")
print(f"\n  {'mh':>6s} | {'eps(Cassini b=3.4e-3)':>22s} | {'eps(beta=1)':>12s} | {'eps(q=1/nucleon)':>17s} |"
      f" {'beta_req(eps=1)':>15s} | {'F_phi/F_N req':>13s} | {'vs Cassini':>11s}")
for mh in MH_GRID:
    e_cas = eps_clean(BETA_CASSINI, mh, x_g)
    e_b1  = eps_clean(1.0, mh, x_g)
    q1_beta = M_red_eV / m_p_eV                       # q = 1 <-> beta = M_red/m_p
    e_q1  = eps_clean(q1_beta, mh, x_g)
    b_req = np.sqrt(1.0 / e_b1) if e_b1 > 0 else np.inf
    F_req = 2 * b_req**2
    print(f"  {mh:6.3g} | {e_cas:22.3e} | {e_b1:12.3e} | {e_q1:17.3e} | {b_req:15.3e} | {F_req:13.3e} |"
          f" x{F_req/2.3e-5:9.2e}")
print(f"\n  note mh=1.45 row: negative eps = the anti-MOND sign past the conformal point (inertia ADDED at")
print(f"  low a) — that mass range cannot do the galactic job at ANY coupling; beta_req = inf is exact.")
print(f"  eternal-dS idealization instead of the cap: eps(beta=1, mh=0.05) = "
      f"{eps_clean(1.0, 0.05, x_g, capped=False):.3e}; the formal mh->0 divergence (tau ~ 3/mh^2) is the BHP")
print(f"  secular runaway [gr-qc/0201020: the charge radiates ALL its mass — destruction, not MOND] and is")
print(f"  killed physically by the t_dS cap anyway (the dressing is then ~m-independent, ~0.27/H). Verdict unmoved.")
print(f"  REQUIRED for the window: eps*g ~ 1 (charitable 0.1). Best allowed (Cassini, best mh):"
      f" {max(eps_clean(BETA_CASSINI, mh, x_g) for mh in MH_GRID):.2e}")
print(f"  visceral anchors: q_req(eps=1, mh=1) = {np.sqrt(1/eps_clean(1,1.0,x_g))*m_p_eV/M_red_eV:.2e} per nucleon")
print(f"   -> scalar exchange between two protons = 2 beta_req^2 = {2/eps_clean(1,1.0,x_g):.2e} x gravity")
print(f"      (EM Coulomb p-p is 1.2e36 x gravity: the required fifth force is"
      f" ~{2/eps_clean(1,1.0,x_g)/1.2e36:.1e} x COULOMB)")
print("\n  coherent-body variant (field coherent over the body; eps_body = N eps_1, breaks universality:")
print("  dm/M would scale with M — a 10-dex EP/RAR violation across the SPARC mass range; numbers anyway):")
for name, N in (("nucleon", 1.0), ("star (Msun)", 1.988e30/1.67262e-27), ("galaxy 1e11 Msun", 1e11*1.988e30/1.67262e-27)):
    e_coh = eps_clean(BETA_CASSINI, 1.0, x_g) * N
    b_req = np.sqrt(1.0 / (eps_clean(1.0, 1.0, x_g) * N))
    print(f"   {name:18s}: N = {N:9.3e} ; eps_body(Cassini) = {e_coh:9.3e} ; beta_req(eps=1) = {b_req:9.3e}"
          f" (force ratio {2*b_req**2:.2e} x gravity)")
print("  [MIC 2209.15487]: composition-DEPENDENT couplings are bound ~1e-13..1e-15 in eta — even harsher.")
print("  [JJKT 1407.0059]: chameleon screening cannot rescue it — screening that hides the solar coupling")
print("  also raises m_phi locally AND in galaxies (rho_gal >> rho_cosmic), killing the light-tail there first.")
print("  [CAR astro-ph/9806099]: the quintessence-coupling suppression requirement is the same statement.")

# ----------------------------------------------------------------------------------------------
hdr("N3-B3", "WINDOW CHANNEL (ii) — SOLAR SHAPE CORRIDOR (coupling unconstrained, magnitude-keyed term)."
             " dm(a) keyed to |a|: delta_a = eps g(x) a ; galactic job eps g(x_gal) = 1")
# ----------------------------------------------------------------------------------------------
print(f"  budgets: Saturn radial {SAT_QUAD:.1e} (quad-tail line) / {FOLKNER:.0e} (Folkner);"
      f" solar-reflex response {SUN_BUDGET:.2e} (agentE survival line, Mars-carried)")
print(f"  [steady-state profile used — the most favorable to the mechanism; the capped one only flattens it]")
print(f"\n  {'mh':>6s} | {'h-':>6s} | {'dA(Sat)/budget':>14s} | {'dA(Sun)/budget':>14s} | verdict (eps set to galactic job)")
corr_best, corr_arg = 0.0, None
for mh in MH_GRID:
    g = lambda x: T_STEADY[(x, mh)] / T_STEADY[(0.0, mh)]
    wrong_sign = (1 - mh**2/2) < 0          # past the conformal point: tail ADDS inertia at low a
    eps_need = 1.0 / g(x_g)
    dA_sat = eps_need * g(x_sat) * A_SAT
    dA_sun = eps_need * g(x_sun) * A_SUN
    ok = (dA_sat < SAT_QUAD) and (dA_sun < SUN_BUDGET)
    tag = "WRONG SIGN (anti-MOND past m^2=2H^2) + " if wrong_sign else ""
    print(f"  {mh:6.3g} | {float(hm_of(mh)):6.3f} | {dA_sat/SAT_QUAD:14.3e} | {dA_sun/SUN_BUDGET:14.3e} |"
          f" {tag}{'PASSES solar' if ok else 'solar-DEAD'}")
    # reverse: max galactic term allowed by solar budgets at this mh (coupling unconstrained)
    if not wrong_sign:
        eps_max = min(SAT_QUAD / (g(x_sat) * A_SAT), SUN_BUDGET / (g(x_sun) * A_SUN))
        gal = eps_max * g(x_g)            # in units of a0 at a = a0
        if gal > corr_best: corr_best, corr_arg = gal, mh
print(f"\n  WHY no mass evades it: the high-a tail of the dressing is (v_cone/kappa)(2 ln kappa + 1/h- + c0)")
print(f"  — a (ln x)/x falloff at EVERY mass [N3-B1 correction]: the F1/Milgrom-99 LINEAR-tail class the repo")
print(f"  killed at x54,000 (MI_BATH_TAIL_CONSTRAINT.md), softened only by the log. There is no exponent to tune:")
print(f"  the near-cone amplitude that carries the high-a tail is H^2/4pi x (1 - m^2/2H^2) — and the dS-distinctive")
print(f"  part of that cone amplitude (subtracting the flat-space massive tail -m^2/8pi) is H^2/4pi EXACTLY,")
print(f"  mass-INDEPENDENT: no subtraction scheme changes the class. Past m^2 = 2H^2 the amplitude flips sign")
print(f"  (anti-MOND: inertia ADDED at low a) and the channel can no longer do the galactic job at all.")
print(f"  shape-only cap (coupling completely unconstrained): max galactic magnitude-keyed term allowed by the")
print(f"  solar budgets = {corr_best:.3e} a0 (at mh = {corr_arg}) — short of the MOND job (=1 a0) by"
      f" {1/corr_best:.1e}.")
print(f"  -> the SHAPE wall alone closes the magnitude-keyed channel by ~5 orders, independent of the")
print(f"     ~80-order coupling wall in [N3-B2]. Two independent walls, each sufficient.")

# ----------------------------------------------------------------------------------------------
hdr("N3-B4", "WINDOW CHANNEL (iii) — FREQUENCY-SUPPRESSED BRACKET (H/Omega)^p, p in {1,2}"
             "  [coordination with N2: bracketed, not blocked]")
# ----------------------------------------------------------------------------------------------
O_gal = {"dwarf edge (a=1e-12, v=20km/s)": 1e-12/2e4, "RAR knee (a=a0, v=220km/s)": a0/2.2e5,
         "massive edge (a=1e-9, v=300km/s)": 1e-9/3e5}
O_sol = {"Saturn (29.5 yr)": 2*np.pi/(29.457*yr_s), "Mars (1.88 yr)": 2*np.pi/(1.8808*yr_s),
         "E-J synodic (1.092 yr)": 2*np.pi/(1.0921*yr_s)}
print(f"  Omega/H_Lambda:  " + " ; ".join(f"{k}: {v/HL_SI:.3g}" for k, v in O_gal.items()))
print(f"                   " + " ; ".join(f"{k}: {v/HL_SI:.3g}" for k, v in O_sol.items()))
for p in (1, 2):
    print(f"\n  p = {p}:  required raw amplitude s_p = a0 (Omega_gal/H)^p to do the MOND job at galaxies:")
    for k, Og in O_gal.items():
        s_req = a0 * (Og/HL_SI)**p
        exp_sat = s_req * (HL_SI/O_sol['Saturn (29.5 yr)'])**p
        exp_mar = s_req * (HL_SI/O_sol['Mars (1.88 yr)'])**p
        print(f"   {k:34s}: s_p = {s_req:9.3e} m/s^2 (= {s_req/cHL:9.3g} cH_L) ;"
              f" Saturn exposure {exp_sat:9.3e} (budget {SAT_QUAD:.0e}) ; Mars exposure {exp_mar:9.3e}"
              f" (line {AGENTE_S:.1e})")
print("\n  -> solar-system side: SAFE for p >= 1 (exposures 1e2..1e8 BELOW budgets — frequency suppression")
print("     does open solar room, as the prompt anticipated). Source side: the required raw amplitude is")
print("     30..1900x a0 (p=1) or 1e3..3.6e6 x a0 (p=2) PER UNIT MASS — the bath ceiling at the maximum")
print("     allowed coupling is the [N3-B2] eps-scale (~1e-85 a0-equivalent): short by >= 87 orders.")
print("     Also flagged for N2: Omega = a/v imprints a v-dependence at fixed a — a (H/Omega)^p term breaks")
print("     RAR universality across the SPARC v-range (x15 spread at p=1) — structure-level liability.")

# ----------------------------------------------------------------------------------------------
hdr("N3-B5", "DRAG CHANNEL (order of magnitude): tail dissipation on an orbiting worldline")
# ----------------------------------------------------------------------------------------------
# F_drag/m <= (q^2/m)(H^2/4pi) v  (unsuppressed bound; any (H/Omega)^p factor only reduces it)
v_orb = 220e3 / c_SI
dadrag_eV = (BETA_CASSINI**2) * (m_p_eV / M_red_eV**2) * (H_eV**2 / (4*np.pi)) * v_orb
dadrag_SI = dadrag_eV / acc_eV
print(f"  upper bound at Cassini coupling, v = 220 km/s: delta_a_drag <= {dadrag_SI:.3e} m/s^2"
      f"  = {dadrag_SI/a0:.3e} a0   (any Omega-suppression lowers it further)")

# ----------------------------------------------------------------------------------------------
hdr("N3-C", "RAW COEFFICIENT LEDGER (reported in isolation, BEFORE any comparison)")
# ----------------------------------------------------------------------------------------------
raw = {
  "tail amplitude coefficient (x H^2)                 [EXACT, A1+BHP]": 1/(4*np.pi),
  "cone-value mass factor: 1 - m^2/(2H^2) -> '1/2' at m=H [EXACT, A2]": 0.5,
  "SY variance coefficient (x H^4/m^2)                [EXACT, A3]   ": 3/(8*np.pi**2),
  "small-m decay rate coefficient: h- -> (1/3)(m/H)^2 [EXACT]       ": 1/3,
  "comoving saturated dressing: |dm| = (3/4pi) q^2 H^3/m^2 [EXACT-asym]": 3/(4*np.pi),
  "dressing-variance identity factor: |dm| = 2pi q^2 <phi^2>/kappa  ": 2*np.pi,
  "P-space kernel falloff exponent h- at m=H (NOT the worldline-tail power; cf B1) [EXACT]": float(hm_of(1.0)),
  "trajectory invariant coefficient (2H^2/k^2) sinh^2 [EXACT, A4]   ": 2.0,
}
for k_, v_ in raw.items():
    print(f"   {k_} = {v_:.6f}")
print("\n  POST-HOC COMPARISON (flagged as such; targets 1/Z = {:.6f}, 1/2pi = {:.6f}, 1/2, 2, Z = {:.4f}):"
      .format(1/Zfac, 1/(2*np.pi), Zfac))
targets = {"1/Z": 1/Zfac, "1/2pi": 1/(2*np.pi), "1/2": 0.5, "2": 2.0, "2/Z": 2/Zfac}
for k_, v_ in raw.items():
    best = min(targets.items(), key=lambda t: abs(np.log(v_/t[1])))
    print(f"   {v_:9.5f}  nearest {best[0]:>5s} = {best[1]:.5f}  off by {abs(v_/best[1]-1)*100:6.1f}%")
print("   verdict: NOTHING lands on Z or 1/Z. Closest accidents: 1/3 vs 2/Z (3.5% — the SAME 3.5% family")
print("   as agentB's banked 1/6-vs-1/Z near-miss, doubled; structurally meaningless, recorded so nobody")
print("   'discovers' it later) and the trivial 1/2's. Consistent with the banked verdict: Z is data-selected.")

# ----------------------------------------------------------------------------------------------
hdr("N3-D", "VERDICT ASSEMBLY (numbers the memo quotes)")
# ----------------------------------------------------------------------------------------------
e_best_cas = max(eps_clean(BETA_CASSINI, mh, x_g) for mh in MH_GRID)
e_best_b1  = max(eps_clean(1.0, mh, x_g) for mh in MH_GRID)
print(f"  tail kernel per unit mass is the RIGHT SIZE in H-units at galactic x (bend at kappa ~ H: the dS")
print(f"  bath 'knows' where a0 is — that part of the framework motivation SURVIVES);")
print(f"  the AMPLITUDE conversion (bath energy H -> nucleon inertia m_p) costs (m_p/M_red)(H/M_red):")
print(f"   best eps at Cassini coupling  : {e_best_cas:.2e}   (need ~1; short by {1/e_best_cas:.1e})")
print(f"   best eps at beta = 1          : {e_best_b1:.2e}   (short by {1/e_best_b1:.1e})")
print(f"   best eps at q = 1 per nucleon : {max(eps_clean(M_red_eV/m_p_eV, mh, x_g) for mh in MH_GRID):.2e}")
print(f"   coherent star at Cassini      : {eps_clean(BETA_CASSINI,1.0,x_g)*1.19e57:.2e} (+ universality break)")
print(f"  shape wall alone (coupling unconstrained): galactic magnitude-keyed term capped at {corr_best:.1e} a0")
print(f"  — the dressing's high-a tail is (ln x)/x at every mass: the banked F1 ephemeris class; no corridor.")
print(f"  frequency channel: solar-safe but source-impossible (>= 87 orders).")
print(f"  WINDOW: EMPTY — by margins (1e27..1e86) that no footing/convention choice (Z vs 2pi vs 2; a0 vs cH;")
print(f"  H_Lambda vs H0; capped vs eternal) can dent. Stated at full weight, both directions:")
print(f"  the door is structurally REAL (trajectory-dependent, MOND-signed — unique among all bath channels")
print(f"  probed tonight) and numerically HOPELESS at any coupling a light scalar is allowed to have.")
print("\n[done]")
