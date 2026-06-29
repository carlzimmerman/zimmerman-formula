#!/usr/bin/env python3
"""
DOES the Deser-Levin de Sitter-Unruh temperature PRODUCE the MOND interpolation?
Running the standard derivation chain a referee would demand, on the framework's OWN terms. Both-ways honest -- the point is to find out
WHERE it works and WHERE it stalls, not to confirm a hope. (Milgrom 1999 'vacuum effect'; the author's a0=cH_Lambda/Z.)
Units: a_Lambda = cH_Lambda = 1. Framework: a0 = cH_Lambda/Z, Z = sqrt(32pi/3).
"""
import numpy as np
Z = np.sqrt(32*np.pi/3); aL = 1.0; a0 = aL/Z
def T(a):  return np.sqrt(a**2 + aL**2)        # Deser-Levin temperature (units)
def dT(a): return T(a) - aL                    # excess over the de Sitter vacuum (Milgrom 1999)

print("="*96)
print(" DESER-LEVIN -> MOND ?   postulate: inertial response F = T(a)-T(0).  (both-ways, a_Lambda=1)")
print("="*96)
print(f"  framework target: a0 = cH_Lambda/Z = 1/{Z:.4f} = {a0:.4f};   g_obs = sqrt(g_bar^2 + g_bar*a0)\n")

# --- 1. THE DEEP-MOND LIMIT (does the sqrt-law fall out?) ---
print(" 1. DEEP-MOND LIMIT (small a):  dT ~ a^2/(2 a_Lambda)  =>  g_bar = a^2/(2 a_L)  =>  a = sqrt(2 a_L g_bar)")
for r in (1e-3,1e-2,1e-1):
    a=r*aL; gbar=dT(a); print(f"     a/a_L={r:.0e}: g_bar=dT={gbar:.3e},  a/sqrt(2 a_L g_bar)={a/np.sqrt(2*aL*gbar):.4f}  (->1 confirms)")
a0_eff = 2*aL
print(f"   => the sqrt-law DOES emerge (Milgrom 1999's real result). BUT the scale is a0_eff = 2 a_Lambda = {a0_eff:.2f}")
print(f"      vs framework a0 = {a0:.4f}  ->  OFF BY FACTOR {a0_eff/a0:.2f} ( = 2Z ).  Right ORDER (~cH_Lambda), wrong COEFFICIENT.\n")

# --- 2. THE FULL INTERPOLATION (is it the framework's sqrt(g^2+g*a0)?) ---
def mu_mech(x): return (np.sqrt(1+x**2)-1)/x          # what the mechanism gives, x=a/a_Lambda
def mu_fw(y):   return (np.sqrt(1+4*y**2)-1)/(2*y)    # framework's convex form, y=a/a0
print(" 2. INTERPOLATION SHAPE:  mechanism mu(x)=(sqrt(1+x^2)-1)/x   vs   framework mu_fw(y)=(sqrt(1+4y^2)-1)/(2y)")
xs=np.array([0.1,0.3,1.0,3.0,10.0])
print(f"     a/a_L:        {xs}")
print(f"     mu_mechanism: {np.round(mu_mech(xs),3)}")
print(f"     mu_framework: {np.round(mu_fw(xs*Z),3)}   (framework, same physical a)")
print(f"   => DIFFERENT functions. The mechanism does NOT output the framework's sqrt(g^2+g*a0); that form is a separate choice.\n")

# --- 3. THE STRUCTURAL MISMATCH (Deser-Levin sum-of-squares vs the framework's product term) ---
print(" 3. STRUCTURE:  Deser-Levin = sqrt(a^2 + a_Lambda^2)   [a_Lambda^2 = CONSTANT term]")
print("                framework   = sqrt(g_bar^2 + g_bar*a0) [g_bar*a0 = PRODUCT-with-variable term]")
print("   => structurally different objects; no bare temperature-postulate yields the g_bar*a0 cross-term.\n")

print("="*96); print(" HONEST VERDICT (both-ways)"); print("="*96)
print(f"""  WORKS (real, this is Milgrom 1999's genuine content, not nonsense):
    * the deep-MOND sqrt-law a=sqrt(a0_eff*a_N) FALLS OUT of subtracting the de Sitter background temperature;
    * the scale is a0 ~ cH_Lambda to order unity -- the a0~cH coincidence is EXPLAINED in kind, not just noted.
  DOES NOT WORK without inserting more (the standard objection, and the gap Milgrom himself flagged):
    * the COEFFICIENT comes out 2 a_Lambda = 2Z*a0 ~ 11.6 a0 -- the precise a0=cH_Lambda/Z is NOT a temperature output;
    * the full INTERPOLATION the mechanism gives is mu=(sqrt(1+x^2)-1)/x, NOT the framework's sqrt(g^2+g*a0);
    * the postulate 'F = T(a)-T(0)' is itself ASSUMED -- why inertia ~ excess temperature is unanswered (Milgrom: an
      actual inertia-from-vacuum mechanism 'is still a far cry off').
  NET: the de Sitter-Unruh idea genuinely yields the SCALE (~cH_Lambda) and the deep-MOND LIMIT; it does NOT yield the
  specific coefficient Z, the specific mu, or a covariant equation of motion. That is exactly where the framework =
  Milgrom 1999, and exactly where any novelty would have to be earned: DERIVE mu + the coefficient from a principled
  postulate (not insert them). a0(z): only declines if w != -1; constant Lambda -> constant a0.""")
