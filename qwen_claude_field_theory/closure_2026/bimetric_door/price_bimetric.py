# >>> RETRACTION 2026-08-30 (see closure_2026/bimetric_secondfield/galileon_scaling_theorem.py + DC-018):
# The 'nonlinear helicity-0 rescue' priced below (r^2 (pi')^2 ~ GM => pi' ~ 1/r = MOND) is WRONG.
# The correct spherical Galileon quadratic balance is r (pi')^2 / Lambda3^3 ~ GM (an explicit extra 1/r
# from the derivative structure) => pi' ~ r^-1/2 (standard Vainshtein), NOT 1/r. Standard ghost-free HR
# helicity-0 gives pi' ~ r^(1-3/n) for integer n in {1,2,3,4} = {r^-2,r^-1/2,r^0,r^1/4}; MOND r^-1 needs
# n=3/2 (non-integer) => NEVER. Also: Higuchi is a constraint, not the primary kill. The live loophole
# moved to DOOR-X32-RELATIVE (a nonanalytic X^(3/2) relative operator whose BD-constraint status is open).
# <<< END RETRACTION

#!/usr/bin/env python3
"""PRICE the bimetric (Hassan-Rosen ghost-free bigravity) door. Two dynamical metrics g (matter) and f,
HR interaction => massless graviton (2) + massive graviton (5) = 7 DOF, ghost-free by construction.
Appeal: the SECOND metric sources the g-sector anisotropy OFF the single-metric delta-R ray WITHOUT a
preferred frame (Lorentz-invariant) => genuinely EXITS the slip-lock theorem DC-013, and the massless
graviton rides g's light cone => PASSES GW170817. Price the costs. sympy where decidable."""
import sympy as sp

r, mg, G, Mtot, a0, c, H0 = sp.symbols('r m_g G M a0 c H0', positive=True)

print("=== 1. DOF + why it escapes the closed single-metric class ===")
print("   7 DOF (2 massless + 5 massive graviton); HR potential = ghost-free (no Boulware-Deser).")
print("   Matter couples to g ONLY; the g<->f mass term sources g's anisotropic sector via the f tensor")
print("   structure -- NOT locked to the delta-R direction (1,-2) that killed frame-free single-metric.")
print("   Lorentz-invariant (no preferred frame) => not touched by P7/DC-010/DC-013/DC-014. GENUINE EXIT.")

print("\n=== 2. THE CORE PROBLEM: a linear massive graviton gives YUKAWA, not MOND ===")
# massive-graviton modified potential (vDVZ): short range 4/3 enhancement, long range Yukawa cutoff.
g_massive = G*Mtot/r**2 * (1 + sp.Rational(1,3)*(1+mg*r)*sp.exp(-mg*r))   # helicity-0 adds 1/3, Yukawa
print(f"   g(r) = {g_massive}")
short = sp.limit(g_massive/(G*Mtot/r**2), r, 0)
long  = sp.simplify((g_massive/(G*Mtot/r**2)).subs(mg*r, 10))  # r>>1/m
print(f"   r<<1/m_g (short): g/g_N -> {short} (= 4/3, vDVZ ENHANCEMENT)")
print(f"   r>>1/m_g (long):  g/g_N -> 1 + tiny (Yukawa CUTOFF => gravity returns to 1/r^2, then weaker)")
print("   => scale-dependence is ENHANCE-at-short, CUTOFF-at-long. MOND needs the OPPOSITE:")
print("      ENHANCE-at-long (low acceleration), g_dyn=sqrt(gN a0)~1/r (flat rotation curves).")
print("   A fixed Compton length lambda=1/m_g is a LENGTH scale; MOND is an ACCELERATION scale a0.")
print("   Linear bigravity is ANTI-MOND in the relevant regime -> CANNOT give flat curves/BTFR.")

print("\n=== 3. The MOND-mass sits on the Higuchi bound (helicity-0 near-ghost cosmologically) ===")
# MOND as a graviton mass: m_g ~ a0/c ~ H0. Higuchi bound (dS): m_g^2 >= 2 H^2.
m_mond = a0/c
print(f"   MOND graviton mass m_g ~ a0/c = {m_mond};  a0 ~ c H0/(2 pi Z) => m_g ~ H0 (order unity).")
print(f"   Higuchi bound (massive spin-2 on dS): m_g^2 >= 2 H^2. With m_g ~ H0 ~ H, this is MARGINAL:")
print(f"   the helicity-0 mode is on the edge of becoming a ghost on cosmological backgrounds. Real tension.")

print("\n=== 4. THE DECISIVE FORK (ghost-free XOR MOND) ===")
print("   HR ghost-free potentials -> linear Yukawa -> NOT MOND (section 2).")
print("   To FORCE MOND (mu(y)=1-e^-y, acceleration scale) you must deform the interaction away from the")
print("   HR ghost-free form into the nonlinear helicity-0 (Vainshtein) sector -- but Vainshtein SCREENS")
print("   at short range (restores GR near sources), the opposite of enhancing at LOW acceleration, and")
print("   deforming off the HR point risks the Boulware-Deser ghost. Milgrom's BIMOND gives the MOND")
print("   phenomenology but is NOT the HR ghost-free construction; its ghost-freedom is NOT established.")

print("\n=== PRICE SUMMARY ===")
print("Bimetric is the FIRST door that genuinely EXITS the closed single-metric class (2nd metric sources")
print("the slip off-ray, no preferred frame) AND passes GW170817 (massless graviton on g's light cone).")
print("PRICE: (i) 7 DOF; (ii) the MOND graviton mass m_g~a0/c~H0 sits ON the Higuchi bound => helicity-0")
print("near-ghost on cosmological backgrounds; (iii) DECISIVE: HR ghost-free => linear YUKAWA (length")
print("scale, ENHANCE-short/CUTOFF-long) = ANTI-MOND, cannot give flat rotation curves; forcing the MOND")
print("acceleration scale needs the nonlinear helicity-0 sector deformed off the HR ghost-free point,")
print("risking the Boulware-Deser ghost (the ghost-free-XOR-MOND fork). DECISIVE OPEN CALC: can a")
print("ghost-free HR-class potential reproduce mu(y)=1-e^-y (acceleration scale, flat curves) in its")
print("nonlinear helicity-0 sector without reintroducing the BD ghost or violating Higuchi? Leans")
print("PESSIMISTIC (Yukawa wrong-sign scale-dependence is structural) but NOT a clean no-go.")
import json
cert={"gate":"PRICE-bimetric","status":"OPEN-PRICED-PESSIMISTIC",
 "certificate":("HR ghost-free bigravity EXITS the closed single-metric class (2nd metric sources the "
   "lensing slip off the delta-R ray, no preferred frame) and passes GW170817 (massless graviton on g "
   "light cone). PRICE: 7 DOF; MOND graviton mass m_g~a0/c~H0 sits ON the Higuchi bound (helicity-0 "
   "near-ghost); DECISIVE FORK: HR ghost-free => linear YUKAWA (fixed Compton length, enhance-short/"
   "cutoff-long) = ANTI-MOND (no flat curves/BTFR); forcing the a0 acceleration scale needs the "
   "nonlinear helicity-0 sector off the HR point, risking the Boulware-Deser ghost. Milgrom BIMOND "
   "gives MOND but is not HR-ghost-free. OPEN CALC: ghost-free HR potential reproducing mu=1-e^-y "
   "without BD ghost/Higuchi violation? Leans pessimistic (Yukawa scale-dependence is structural)."),
 "assumptions":["HR ghost-free bigravity","vDVZ 4/3 short + Yukawa long","m_g~a0/c~H0","Higuchi m^2>=2H^2"],
 "numeric_values":{"DOF":7,"vDVZ_short":"4/3","long_range":"Yukawa cutoff","m_g":"~H0 (Higuchi edge)"}}
print("CERTIFICATE_JSON:", json.dumps(cert))
