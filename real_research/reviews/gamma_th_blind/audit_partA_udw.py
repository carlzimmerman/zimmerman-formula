"""
AUDIT Part A: Unruh-DeWitt detector in de Sitter (dS4), Bunch-Davies vacuum.
Independent re-derivation from FIRST PRINCIPLES.

Physics:
- massless scalar, BD vacuum, comoving (geodesic) detector in dS4.
- Pullback of the BD Wightman fn onto the geodesic worldline is (in proper time dtau):
    W(dtau) = -(H^2 / 16 pi^2) / sinh^2( (H/2)(dtau - i*eps) )
  This is the standard dS4 result (Birrell-Davies; Garbrecht-Prokopec; Gibbons-Hawking).
- Response (transition rate) per unit proper time at gap E:
    F(E) = int_{-inf}^{+inf} d(dtau) e^{-i E dtau} W(dtau)
  E>0 => excitation (absorption), E<0 => de-excitation (emission).

GOAL: derive
  (1) the contour integral J(nu) = int du e^{-i nu u} / sinh^2(u - i0)
  (2) detailed balance ratio R_up/R_down,
  (3) Gibbons-Hawking temperature T = H/2pi,
  (4) Gamma_th = R_up + R_down = lambda^2 |mu|^2 (omega/2pi) coth(pi omega/H),
  (5) gapless limit,
  (6) tau_c from Wightman decay.
ALL via sympy where possible; numeric cross-checks.
"""
import sympy as sp
import numpy as np

print("="*70)
print("AUDIT PART A: dS4 UDW detector, independent derivation")
print("="*70)

# ---------------------------------------------------------------
# (1) The core contour integral via residues.
# Substitute u = (H/2) dtau, so dtau = (2/H) du, and define nu = 2E/H.
#   W dtau = -(H^2/16pi^2)/sinh^2(u-i0) * (2/H) du = -(H/8pi^2)/sinh^2(u-i0) du
#   F(E) = -(H/8pi^2) * J(nu),  J(nu)=int du e^{-i nu u}/sinh^2(u-i0).
# sinh^2(u) has double poles at u = i*pi*n (n integer).
# For e^{-i nu u} with nu>0, close in LOWER half-plane (Im u <0): poles u=-i pi m, m=1,2,...
# The i0 prescription u-i0 shifts poles; the m=0 pole sits just below axis -> included.
# Residue of e^{-i nu u}/sinh^2(u) at a double pole u0 (where sinh(u0)=0):
#   near u0, sinh(u)= cosh(u0)(u-u0) + ... and cosh(u0)=+-1, cosh^2=1.
#   1/sinh^2 = 1/[(u-u0)^2 cosh^2(u0)] * (1 - (u-u0) tanh? ...) -> use sympy.
# ---------------------------------------------------------------
u, nu, m = sp.symbols('u nu m', real=True)
nu_pos = sp.symbols('nu', positive=True)

# Residue at a generic pole u0 = -i*pi*m (lower half plane, m>=0 integer)
# Compute residue of f(u)=exp(-I nu u)/sinh(u)^2 at u0 symbolically.
f = sp.exp(-sp.I*nu_pos*u)/sp.sinh(u)**2

def residue_at(m_val):
    u0 = -sp.I*sp.pi*m_val
    # double pole: residue = d/du [ (u-u0)^2 f ] at u0
    g = (u - u0)**2 * f
    res = sp.limit(sp.diff(g, u), u, u0)
    return sp.simplify(res)

# Compute residues for m=0..3
res_list = []
for mm in range(0,4):
    r = residue_at(mm)
    res_list.append(r)
    print(f"  Residue at u0=-i*pi*{mm}: {sp.simplify(r)}")

# Sum: J(nu) = -2 pi i * sum_{m>=0} Res (clockwise contour in lower half-plane => -2 pi i)
# Build the series sum_{m>=0} residue. From pattern residue = -I*nu*exp(-pi*nu*m)? check.
print("\n  Pattern check: residue_m / (-I*nu*exp(-pi*nu*m)):")
for mm in range(0,4):
    ratio = sp.simplify(res_list[mm] / (-sp.I*nu_pos*sp.exp(-sp.pi*nu_pos*mm)))
    print(f"    m={mm}: {ratio}")

# So residue_m = -I*nu*exp(-pi*nu*m). Sum over m=0..inf:
S = sp.summation(-sp.I*nu_pos*sp.exp(-sp.pi*nu_pos*m), (m, 0, sp.oo))
S = sp.simplify(S)
print(f"\n  Sum_m residue = {S}")
J = sp.simplify(-2*sp.pi*sp.I * S)   # clockwise -> -2 pi i
print(f"  J(nu) = -2 pi i * Sum = {J}")
J_simpl = sp.simplify(J)
print(f"  J(nu) simplified = {J_simpl}")

# Expected: J(nu) = -2 pi nu/(1 - e^{-pi nu})
J_expected = -2*sp.pi*nu_pos/(1 - sp.exp(-sp.pi*nu_pos))
print(f"  Expected -2 pi nu/(1-e^{{-pi nu}}) ; difference = {sp.simplify(J_simpl - J_expected)}")

# ---------------------------------------------------------------
# (2) Excitation / de-excitation rates.
# F(E) = -(H/8pi^2) J(nu), nu = 2E/H.
# For E>0 (excitation): nu>0.
#   J(nu) = -2 pi nu/(1-e^{-pi nu}). With nu=2E/H:
#   F_up = -(H/8pi^2)*(-2 pi (2E/H)/(1-e^{-2 pi E/H})) = (E/(2pi))/(1-e^{-2piE/H})... check sign.
# Multiply by lambda^2|mu|^2. Let omega=|E|.
# ---------------------------------------------------------------
H, E, omega = sp.symbols('H E omega', positive=True)
nu_of_E = 2*E/H
F_up = sp.simplify(-(H/(8*sp.pi**2)) * J_expected.subs(nu_pos, nu_of_E))
print("\n  Excitation kernel F_up (E>0) = ", sp.simplify(F_up))
# For de-excitation E<0 => nu=2E/H<0. Re-derive J for nu<0 by closing UPPER half plane.
# By the symmetry J(-nu) relation: the KMS/detailed-balance shortcut: F(-E)=e^{2pi E/H} F(E).
# Verify via direct: for nu<0 close upper half, poles u=+i pi m, residues give:
nu_neg = sp.symbols('nu', negative=True)
fneg = sp.exp(-sp.I*nu_neg*u)/sp.sinh(u)**2
def residue_at_upper(m_val):
    u0 = sp.I*sp.pi*m_val
    g = (u - u0)**2 * fneg
    return sp.simplify(sp.limit(sp.diff(g, u), u, u0))
print("\n  (de-excitation, nu<0, upper-half poles)")
resU = [residue_at_upper(mm) for mm in range(0,3)]
for mm in range(0,3):
    ratio = sp.simplify(resU[mm] / (sp.I*(-nu_neg)*sp.exp(sp.pi*nu_neg*mm)))
    print(f"    m={mm} ratio to I*|nu|*exp(pi nu m): {ratio}")
SU = sp.summation(sp.I*(-nu_neg)*sp.exp(sp.pi*nu_neg*m), (m, 0, sp.oo))
JU = sp.simplify(+2*sp.pi*sp.I*SU)  # upper half closed counterclockwise -> +2 pi i
print(f"  J(nu<0) = {sp.simplify(JU)}")
JU_expected = -2*sp.pi*nu_neg*sp.exp(sp.pi*nu_neg)/(1 - sp.exp(sp.pi*nu_neg))
print(f"  Expected form -2 pi nu e^{{pi nu}}/(1-e^{{pi nu}}); diff={sp.simplify(sp.simplify(JU)-JU_expected)}")

# de-excitation kernel: E_de = -omega (nu = -2 omega/H)
F_down = sp.simplify(-(H/(8*sp.pi**2)) * JU_expected.subs(nu_neg, -2*omega/H))
F_up_om = sp.simplify(-(H/(8*sp.pi**2)) * J_expected.subs(nu_pos, 2*omega/H))
print("\n  F_up(omega)   =", sp.simplify(F_up_om))
print("  F_down(omega) =", sp.simplify(F_down))

# Detailed balance ratio
DB = sp.simplify(F_up_om / F_down)
print("\n  DETAILED BALANCE  R_up/R_down =", sp.simplify(DB))
print("  Expected exp(-2 pi omega/H); diff =", sp.simplify(DB - sp.exp(-2*sp.pi*omega/H)))

# ---------------------------------------------------------------
# (3) Gibbons-Hawking temperature: R_up/R_down = e^{-omega/T} => T
# ---------------------------------------------------------------
T = sp.symbols('T', positive=True)
sol = sp.solve(sp.Eq(DB, sp.exp(-omega/T)), T)
print("\n  GIBBONS-HAWKING T from detailed balance:", sol)

# ---------------------------------------------------------------
# (4) Gamma_th = R_up + R_down (population relaxation rate)
#   master eq dP/dt = R_up - (R_up+R_down) P
# ---------------------------------------------------------------
g2 = sp.symbols('g2', positive=True)  # lambda^2 |mu_0E|^2
# include coupling prefactor g2 (the kernels above are per unit g2)
Gamma_th = sp.simplify(g2*(F_up_om + F_down))
print("\n  Gamma_th = g2*(F_up+F_down) =", sp.simplify(Gamma_th))
# Compare to coth form
coth_form = g2*(omega/(2*sp.pi))*sp.coth(sp.pi*omega/H)
print("  coth form g2*(omega/2pi)*coth(pi omega/H):", coth_form)
print("  difference =", sp.simplify(Gamma_th - coth_form))

# ---------------------------------------------------------------
# (5) Gapless limit omega->0
# ---------------------------------------------------------------
gapless = sp.limit(coth_form, omega, 0, '+')
print("\n  Gapless Gamma_th(omega->0) =", sp.simplify(gapless))
print("  In units of H: coefficient =", sp.simplify(gapless/(g2*H)))
print("  = g2 * H/(2 pi^2) ?  ->", sp.simplify(gapless - g2*H/(2*sp.pi**2)))
print("  = g2 * T_GH/pi ? (T_GH=H/2pi) ->", sp.simplify(gapless - g2*(H/(2*sp.pi))/sp.pi))
print(f"  numeric coeff H/(2pi^2) = {float(1/(2*np.pi**2)):.6f} * H")

# ---------------------------------------------------------------
# (6) tau_c from Wightman decay: W ~ 1/sinh^2((H/2)dtau) -> 4 e^{-H dtau}
# ---------------------------------------------------------------
dtau = sp.symbols('dtau', positive=True)
Wfun = 1/sp.sinh(H*dtau/2)**2
lim = sp.limit(Wfun*sp.exp(H*dtau), dtau, sp.oo)
print("\n  Wightman large-dtau: W*e^{H dtau} ->", lim, " => decay rate H => tau_c=1/H")

# numeric polyfit cross-check of decay rate
xx = np.linspace(2,8,200)  # H*dtau
Wnum = 1/np.sinh(xx/2)**2
coef = np.polyfit(xx, np.log(Wnum), 1)
print(f"  numeric polyfit ln|W| vs (H dtau) slope = {coef[0]:.4f} (expect -1 => tau_c=1/H)")

print("\n" + "="*70)
print("PART A SUMMARY (audit):")
print(f"  Gamma_th(omega) = g2 * (omega/2pi) * coth(pi omega/H)")
print(f"  Gamma_th(0)     = g2 * H/(2pi^2) = {1/(2*np.pi**2):.5f} g2 H")
print(f"  T_GH            = H/(2pi) = {1/(2*np.pi):.5f} H")
print(f"  tau_c           = 1/H")
print(f"  Detailed balance R_up/R_down = exp(-2 pi omega/H) = exp(-omega/T_GH)")
print("="*70)
