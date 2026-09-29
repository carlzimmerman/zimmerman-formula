#!/usr/bin/env python3
"""A3 -- the inequality table (WGC, Lambda-corrected extremality, Festina Lente margin) and the scale statement (pre-registered I1-I5).
Measured masses appear ONLY as inputs for margins; nothing is derived about masses. Run: python3 a3_inequalities_and_scale.py [MUTATE]
MUTATE swaps the WGC inequality direction (z <= 1); the electron check must then FAIL (exit 1)."""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

# ---------- constants (SI) and conversions
G = mp.mpf("6.67430e-11"); hb = mp.mpf("1.054571817e-34"); c = mp.mpf(299792458); eC = mp.mpf("1.602176634e-19")
J2eV = 1/eC
mP_eV = mp.sqrt(hb*c/G)*c**2*J2eV                 # Planck mass (not reduced), eV
Mpl_red_eV = mP_eV/mp.sqrt(8*mp.pi)                 # reduced Planck mass, eV
alpha0 = 1/mp.mpf("137.035999177")
e_HL = mp.sqrt(4*mp.pi*alpha0)
me_eV = mp.mpf("0.51099895e6")                      # measured electron mass (INPUT, margin only)
Mpc = mp.mpf("3.0856775814913673e22"); H0 = mp.mpf("67.4e3")/Mpc
Lam = 3*mp.mpf("0.6847")*H0**2/c**2                 # 1/m^2
H_L = c*mp.sqrt(Lam/3)                              # 1/s, de Sitter Hubble rate of Lambda
H_L_eV = hb*H_L*J2eV
lP2 = G*hb/c**3
x = Lam*lP2
print(f"m_P = {mp.nstr(mP_eV/1e9,6)} GeV, reduced M_Pl = {mp.nstr(Mpl_red_eV/1e9,6)} GeV, hbar H_Lambda = {mp.nstr(H_L_eV,4)} eV, x = {mp.nstr(x,4)}")

# ---------- I1: derive the extremal M(Q) relation, then the WGC ratio for the electron
Msym, Gs, q, Mpl = sp.symbols("M G q Mpl", positive=True)
# geometric: G M^2 = Q_geo^2 = G q^2/(4 pi)  ->  M^2 = q^2/(4 pi G); reduced Planck M_pl^2 = 1/(8 pi G)
Mext = sp.sqrt(q**2/(4*sp.pi*Gs))
Mext_red = sp.simplify(Mext.subs(Gs, 1/(8*sp.pi*Mpl**2)))
print("extremal RN (Lambda=0):  M_ext =", Mext_red, " (HL charge q, reduced Planck mass Mpl)")
chk("I1a M_ext = sqrt(2) q M_pl (derived from G M^2 = Q^2)", sp.simplify(Mext_red - sp.sqrt(2)*q*Mpl) == 0)
Mext_e = mp.sqrt(2)*e_HL*Mpl_red_eV
z_e = Mext_e/me_eV                                  # charge-to-mass ratio in extremal units (z = Q/M over the extremal value)
print(f"WGC scale sqrt2 e M_pl = {mp.nstr(Mext_e/1e9,5)} GeV;  electron: z_e = (Q/M)/(Q/M)_ext = {mp.nstr(z_e,4)}  (m_e/M_ext = {mp.nstr(1/z_e,4)})")
if MUT:
    chk("I1b [MUTATED direction] electron has z <= 1", z_e <= 1, f"z_e = {mp.nstr(z_e,4)}")
else:
    chk("I1b electron satisfies the WGC inequality z >= 1 (an inequality; margin ~ 2e21)", z_e >= 1 and mp.mpf("1e21") < z_e < mp.mpf("1e22"))
print("   I1c (statement, not a check) saturation would require m = sqrt2 e M_pl = a mass ~ 1e18 GeV; the inequality contains no x")

# ---------- I2: Lambda-corrected extremality shift, z_ext(y) = sqrt(1-y)/(1-2y/3), y = Lambda r0^2
def zext(y):
    with mp.workdps(500):
        return mp.sqrt(1 - y)/(1 - 2*y/3)
r_e = mp.sqrt(alpha0)   # in l_P: electric n=1 extremal radius
for lab, yv in [("Planck-size object r=l_P", x), ("electric n=1 extremal r=sqrt(alpha) l_P", alpha0*x), ("ultracold (Hubble size)", mp.mpf(1)/2)]:
    with mp.workdps(500):
        dz = zext(yv)-1
    print(f"   y = {lab:42s} = {mp.nstr(yv,4):>10s}   z_ext - 1 = {mp.nstr(dz,6)}")
chk("I2a on the cold branch 1 <= z_ext <= 3/(2 sqrt 2) = 1.0607 (bounded, x-independent)", zext(mp.mpf(0)) == 1 and abs(zext(mp.mpf(1)/2) - 3/(2*mp.sqrt(2))) < mp.mpf("1e-25"))
with mp.workdps(500):
    ratio = (zext(x)-1)/(x/6)
chk("I2b Lambda shifts the WGC threshold by ~ x/6 = 5e-123 for a Planck-size object (invisible)", abs(ratio - 1) < mp.mpf("1e-10"), f"(ratio to x/6 = {mp.nstr(ratio,12)})")

# ---------- I3: Festina Lente margin (constant c_FL unknown in what was read; two conventions, not scored)
for cfl in [1, 10]:
    lhs = me_eV**2; rhs = cfl*e_HL*Mpl_red_eV*H_L_eV
    print(f"   FL-type bound m^2 >= c e M_pl H  with c = {cfl:>2d}: m_e^2 = {mp.nstr(lhs,4)} eV^2 vs {mp.nstr(rhs,4)} eV^2, margin = {mp.nstr(lhs/rhs,4)}")
chk("I3 the electron satisfies a FL-type lower bound with margin > 1e15 for c in {1,10} (lower bound = inequality; no alpha fixed)",
    me_eV**2/(10*e_HL*Mpl_red_eV*H_L_eV) > mp.mpf("1e15"))
print("   I3 saturation would give alpha ~ (m^2/(c M_pl H))^2/(4 pi):", mp.nstr((me_eV**2/(e_HL*Mpl_red_eV*H_L_eV))**2/(4*mp.pi), 3), "-- absurd, i.e. FL saturation is not close to the electron")

# ---------- I5: scale of the BH relations (AMENDED, see A_PREREGISTRATION.md Amendment 1)
# One-loop SM running of alpha_em^-1 = alpha_Y^-1 + alpha_2^-1 above m_Z (b1=41/10 GUT-normalised, b2=-19/6); MEASURED couplings at m_Z are INPUTS.
# No new physics, no thresholds, no two-loop: this is an order-of-magnitude scale statement, not a prediction.
mZ = mp.mpf("91.1876"); mPGeV = mP_eV/1e9
ia_Z = mp.mpf("127.95"); sw2 = mp.mpf("0.23122")
a2inv = ia_Z*sw2; aYinv = ia_Z - a2inv
L = mp.log(mPGeV/mZ)
bY = mp.mpf(3)/5*mp.mpf(41)/10; b2 = -mp.mpf(19)/6
aYinv_P = aYinv - bY/(2*mp.pi)*L; a2inv_P = a2inv - b2/(2*mp.pi)*L
ia_P = aYinv_P + a2inv_P
print(f"\nI5 one-loop SM, measured inputs at m_Z: 1/alpha_em(m_Z) = {ia_Z}, sin^2 = {sw2}")
print(f"   ln(m_P/m_Z) = {mp.nstr(L,5)};  1/alpha_Y(m_P) = {mp.nstr(aYinv_P,5)}, 1/alpha_2(m_P) = {mp.nstr(a2inv_P,5)}, 1/alpha_em(m_P) ~ {mp.nstr(ia_P,5)}")
print(f"   Thomson: 1/alpha = 137.036 -> m_Z: 127.95 (input) -> m_P: ~{mp.nstr(ia_P,4)}  (shift from Thomson = {mp.nstr(100*(ia_P/(1/alpha0)-1),3)} %)")
print(f"   k_req (Thomson) = {mp.nstr(1/(2*mp.sqrt(alpha0)),5)};  k_req with alpha(m_P) ~ {mp.nstr(mp.sqrt(ia_P)/2,5)}   [post-hoc, NOT scored: Z = 5.7888 is {mp.nstr(100*(mp.sqrt(ia_P)/2/5.7888-1),2)} % from this, using an approximate one-loop spectrum-dependent input]")
chk("I5a the SM one-loop shift of 1/alpha between m_Z and m_P is between 1% and 10% (small but far above the 1e-3 hit tolerance)", 0.01 < abs(ia_P/ia_Z - 1) < 0.10, f"({mp.nstr(100*(ia_P/ia_Z-1),3)} % from m_Z)")
chk("I5b Thomson-to-m_P shift exceeds the 1e-3 hit tolerance by > 10x, so a BH-scale relation cannot be matched to the Thomson value at 1e-3 without a spectrum", abs(ia_P/(1/alpha0) - 1) > 1e-2, f"({mp.nstr(100*(ia_P/(1/alpha0)-1),3)} %)")
print("   => a relation alpha = 1/(4 k^2) forced at r_+ ~ 6 l_P concerns alpha at mu ~ m_P (true spectrum), not the Thomson value.")

print("\nSUMMARY: %d/%d checks pass (MUTATE=%s)" % (sum(c[1] for c in checks), len(checks), MUT))
sys.exit(0 if all(c[1] for c in checks) else 1)
