#!/usr/bin/env python3
r"""
Q2 (ROBUSTNESS): does the eta-free NULL rest on the massless-conformal choice? Confirm the GENERAL-MASS
de Sitter Wightman function leaves the KMS/Matsubara pole LOCATION at Delta_tau = 2pi i / kappa_eff,
kappa_eff = sqrt(H^2 + a^2) -- the mass shifts residues/Matsubara weights, NOT the pole position.
================================================================================================
Framework = de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman). The pullback (mi_closure_pin/PULLBACK.md)
used the massless conformal scalar as the representative dS 2-point function. Here we redo the pole-location
analysis for a scalar of ARBITRARY mass m (principal series nu=i*mu real m>3H/2, complementary series nu real
0<m<3H/2, and the conformal point m^2=2H^2), and show the nearest off-real-axis singularity in proper time
stays at Delta_tau = 2pi i/kappa_eff independent of m. This is because:
  (i)  the accelerated-worldline embedding gives Z(Delta_tau)=s^2 cosh(kappa_eff Delta_tau)+(1-s^2),
       kappa_eff=sqrt(H^2+a^2) -- a GEOMETRIC fact, mass-independent;
  (ii) the massive dS 2-point function G(Z) is singular ONLY at coincidence Z=1 (the Hadamard/UV singularity,
       mass-independent LEADING coefficient) and its KMS images Z=1;
  (iii)Z(Delta_tau)=1  <=>  cosh(kappa_eff Delta_tau)=1  <=>  kappa_eff Delta_tau = 2pi i n  -> nearest pole
       n=1 at Delta_tau=2pi i/kappa_eff, mass-independent. Mass changes the RESIDUE only.
All exit-0 sympy/mpmath, no hard-coded verdict booleans. Both footings for kappa_eff at a=a0.
"""
import mpmath as mp
import sympy as sp
from _common import banner, Checker, FOOTINGS, c, Z as Zconst
mp.mp.dps = 40
chk = Checker()

# =====================================================================================
banner("[1] the accelerated-worldline embedding: Z(Delta_tau) and kappa_eff=sqrt(H^2+a^2) (sympy, EXACT)")
# =====================================================================================
print(r"""
 dS_4 = hyperboloid X.X = 1/H^2 in M^{1,4}. Static-patch worldline at fixed areal radius r0 (uniformly
 accelerated, proper accel a = H^2 r0 / sqrt(1-H^2 r0^2)). The dS-invariant Z = H^2 X(tau).X(tau'):
     Z(Delta_tau) = s^2 cosh(kappa Delta_tau) + (1-s^2),   s=sqrt(1-H^2 r0^2),  kappa = H/s.
 This is PURE GEOMETRY (the field mass never enters). Derive kappa^2 = H^2 + a^2.""")
H, r0, dtau = sp.symbols('H r0 Deltatau', positive=True)
s = sp.sqrt(1 - H**2*r0**2)
a_proper = H**2*r0/sp.sqrt(1 - H**2*r0**2)              # proper acceleration
kappa = H/s
kap2_minus = sp.simplify(kappa**2 - (H**2 + a_proper**2))
print(f"  s = sqrt(1-H^2 r0^2),  kappa = H/s,  a = H^2 r0/sqrt(1-H^2 r0^2)")
print(f"  kappa^2 - (H^2 + a^2) = {kap2_minus}")
chk("embedding gives kappa_eff^2 = H^2 + a^2 EXACTLY (geometric, mass-independent)", kap2_minus == 0)
Zexpr = s**2*sp.cosh(kappa*dtau) + (1 - s**2)
# Z=1 (coincidence + images): cosh(kappa dtau)=1 -> kappa dtau = 2 pi i n
coinc = sp.simplify(Zexpr - 1)
print(f"  Z(Delta_tau) - 1 = {sp.simplify(coinc)}  = s^2 (cosh(kappa Delta_tau) - 1)")
chk("Z=1 <=> cosh(kappa Delta_tau)=1 (the coincidence/KMS-image condition is geometric)",
    sp.simplify(coinc - s**2*(sp.cosh(kappa*dtau) - 1)) == 0)
# nearest imaginary-axis root of cosh(kappa dtau)=1 : kappa dtau = 2 pi i -> dtau = 2 pi i/kappa
print("  cosh(kappa Delta_tau)=1  =>  kappa Delta_tau = 2 pi i n  =>  nearest pole Delta_tau = 2 pi i/kappa_eff")
chk("nearest KMS pole at Delta_tau = 2pi i/kappa_eff (period 2pi i/kappa_eff -> T=kappa_eff/2pi)",
    sp.simplify(sp.cosh(kappa*(2*sp.pi*sp.I/kappa)) - 1) == 0)

# =====================================================================================
banner("[2] the GENERAL-MASS dS 2-point function G(Z): singular ONLY at Z=1, mass-independent LEADING")
# =====================================================================================
print(r"""
 The de Sitter-invariant Wightman two-point function for a scalar of mass m in dS_4 is (Bunch-Davies):
     G(Z) = (H^2/16 pi^2) Gamma(h_+) Gamma(h_-) 2F1(h_+, h_-; 2; (1+Z)/2),
     h_pm = 3/2 +- nu,   nu = sqrt(9/4 - m^2/H^2).
 (nu real & in (0,3/2): complementary series; nu = i mu imaginary: principal series, heavy m>3H/2;
  nu=1/2 i.e. m^2=2H^2: the conformally-coupled/massless-conformal point used in the pullback.)
 2F1(a,b;c;x) has its branch point at x=1, i.e. (1+Z)/2 = 1 -> Z=1 (coincidence). With c-a-b = 2-h_+-h_- =
 2-3 = -1 < 0, near x->1:  2F1 ~ Gamma(c)Gamma(a+b-c)/(Gamma(a)Gamma(b)) (1-x)^{c-a-b} = ...(1-x)^{-1}.
 Compute the LEADING coincidence coefficient of G and show the mass (h_pm) dependence CANCELS.""")
nu = sp.symbols('nu')
hp = sp.Rational(3, 2) + nu
hm = sp.Rational(3, 2) - nu
# leading coefficient of 2F1(hp,hm;2;x) as x->1 : Gamma(2)Gamma(hp+hm-2)/(Gamma(hp)Gamma(hm)) (1-x)^{2-hp-hm}
a_, b_, c_ = hp, hm, sp.Integer(2)
exp_pow = sp.simplify(c_ - a_ - b_)                     # = -1
lead_2f1_coeff = sp.gamma(c_)*sp.gamma(a_+b_-c_)/(sp.gamma(a_)*sp.gamma(b_))
prefac = (sp.Symbol('H', positive=True)**2/(16*sp.pi**2))*sp.gamma(hp)*sp.gamma(hm)
G_lead_coeff = sp.simplify(prefac*lead_2f1_coeff)      # coefficient of (1-x)^{-1}
print(f"  2F1 exponent c-a-b = {exp_pow}  (=-1 -> simple pole in (1-x) -> in (Z-1))")
print(f"  leading G coefficient (of (1-(1+Z)/2)^-1) = {G_lead_coeff}")
dcoeff_dnu = sp.simplify(sp.diff(G_lead_coeff, nu))
print(f"  d(leading coeff)/d nu = {dcoeff_dnu}  (=0 -> LEADING coincidence singularity is MASS-INDEPENDENT)")
chk("massive dS 2-point has a SIMPLE pole at coincidence Z=1 (exponent c-a-b=-1, all masses)", exp_pow == -1)
chk("LEADING coincidence coefficient is MASS-INDEPENDENT (Hadamard universality): d/dnu = 0", dcoeff_dnu == 0)

# =====================================================================================
banner("[3] the pole LOCATION in Delta_tau is 2pi i/kappa_eff for EVERY mass; only RESIDUES shift (mpmath)")
# =====================================================================================
print(r"""
 Numerically evaluate the full massive G(Z(Delta_tau)) along the imaginary Delta_tau axis for several masses
 and confirm the nearest singularity sits at Delta_tau = 2pi i/kappa_eff (i.e. kappa_eff Delta_tau = 2pi i),
 independent of mass; then show the SUBLEADING (mass-dependent) piece genuinely differs by comparing G at a
 fixed off-coincidence Z for different masses.""")
def G_massive(Zval, nuval):
    hp = mp.mpf('1.5') + nuval; hm = mp.mpf('1.5') - nuval
    x = (1 + Zval)/2
    return (mp.mpf(1)/(16*mp.pi**2))*mp.gamma(hp)*mp.gamma(hm)*mp.hyp2f1(hp, hm, 2, x)

# work in units H=1; kappa_eff=1/s. Pick an accelerated worldline s=0.8 -> kappa=1.25, a=sqrt(kappa^2-1).
s_val = mp.mpf('0.8'); kap = 1/s_val
a_over_H = mp.sqrt(kap**2 - 1)
def Zof(dt):                                            # dt real; imaginary proper time = i*dt
    return s_val**2*mp.cosh(kap*(1j*dt)) + (1 - s_val**2)
pole_dt = float(2*mp.pi/kap)                            # imaginary-time coordinate of the nearest KMS pole
print(f"  worldline s=0.8 -> kappa_eff=1.25 (a/H={mp.nstr(a_over_H,4)}); predicted pole at Im(Delta_tau)=2pi/kappa={pole_dt:.5f}")
masses = [("conformal nu=1/2 (m^2=2H^2)", mp.mpf('0.5')),
          ("light complementary nu=1.2", mp.mpf('1.2')),
          ("near-massless nu=1.49",      mp.mpf('1.49')),
          ("heavy principal nu=i*1.5 (m^2=(9/4+2.25)H^2)", 1j*mp.mpf('1.5'))]
print(f"\n  {'mass label':44s} {'|G| just below pole':>20s} {'|G| just above pole':>20s} {'blows up AT 2pi/kappa?':>22s}")
below_frac = float(mp.mpf('0.985')); above_frac = float(mp.mpf('1.015'))
for label, nuv in masses:
    Gb = abs(G_massive(Zof(pole_dt*below_frac), nuv))
    Gp = abs(G_massive(Zof(pole_dt*0.9999), nuv))       # very near the pole
    Ga = abs(G_massive(Zof(pole_dt*above_frac), nuv))
    diverges = (Gp > 20*Gb) and (Gp > 20*Ga)            # sharp peak exactly at 2pi/kappa
    print(f"  {label:44s} {mp.nstr(Gb,4):>20s} {mp.nstr(Gp,4):>20s} {str(bool(diverges)):>22s}")
    chk(f"[{label}] nearest singularity at Im(Delta_tau)=2pi/kappa_eff (pole LOCATION mass-independent)",
        diverges)

# residues differ: compare G at a FIXED off-coincidence Z across masses -> mass-dependent (subleading) content
print("\n  residue/subleading check: G at a fixed off-pole Z=0.5 differs across masses (mass shifts residues):")
Gvals = [abs(G_massive(mp.mpf('0.5'), nuv)) for _, nuv in masses]
for (label, _), gv in zip(masses, Gvals):
    print(f"     {label:44s} |G(Z=0.5)| = {mp.nstr(gv,6)}")
spread = max(Gvals) - min(Gvals)
chk("mass genuinely changes the 2-point function (residues/Matsubara weights differ; only LOCATION is fixed)",
    spread > mp.mpf('1e-3'))

# =====================================================================================
banner("[4] the KMS temperature T = kappa_eff/2pi is mass-independent, at a=a0 both footings")
# =====================================================================================
print(r"""
 The pole period 2pi i/kappa_eff sets the KMS temperature T_eff = kappa_eff/2pi = sqrt(H^2+a^2)/2pi, which the
 massive analysis leaves untouched (it depends only on the geometric Z(Delta_tau), not on m). Report it at the
 MOND transition a=a0 for both footings -- identical to the massless pullback value.""")
for name, a0, HL in FOOTINGS:
    kap_a0 = mp.sqrt(HL**2 + (a0/c)**2)
    ratio = kap_a0/HL
    print(f"  {name:18s}: kappa_eff(a=a0)/H_L = {mp.nstr(ratio,8)} (=sqrt(1+1/Z^2)), "
          f"T_eff=kappa_eff/2pi={mp.nstr(kap_a0/(2*mp.pi),5)}  (mass-independent)")
    chk(f"[{name}] KMS pole ratio at a=a0 = sqrt(1+1/Z^2) (mass-independent, matches massless pullback)",
        abs(ratio - mp.sqrt(1 + 1/Zconst**2)) < mp.mpf('1e-20'))

print(r"""
 SYNTHESIS (Q2): the eta-free NULL does NOT rest on the massless-conformal choice. For a scalar of ANY mass
 (complementary, principal, or the conformal point), the de Sitter Wightman function is singular only at the
 geometric coincidence Z=1 and its KMS images; the accelerated-worldline embedding fixes Z(Delta_tau) and
 hence the nearest pole at Delta_tau = 2pi i/kappa_eff, kappa_eff=sqrt(H^2+a^2) -- a MASS-INDEPENDENT LOCATION.
 The mass shifts residues/Matsubara weights only. The Pythagorean pole (>= H_L for every acceleration) that
 makes the pullback weighting-blind is robust to the field mass. Both footings; s=-1, a0 postulates.""")
raise SystemExit(chk.done())
