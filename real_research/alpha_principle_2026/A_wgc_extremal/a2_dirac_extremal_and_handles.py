#!/usr/bin/env python3
"""A2 -- Dirac quantization + extremality: what is forced, what is only re-expressed (pre-registered D1-D5).
Run: python3 a2_dirac_extremal_and_handles.py [MUTATE]   (MUTATE: Dirac condition with 4 pi instead of 2 pi; must exit 1)"""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

hb, c, G, al, n = sp.symbols("hbar c G alpha n", positive=True)
lP2 = G*hb/c**3
dirac = 4*sp.pi if MUT else 2*sp.pi   # HL: e g = dirac * n hbar c   (correct value 2 pi)

# ---- D1: Heaviside-Lorentz bookkeeping
e_HL2 = 4*sp.pi*al*hb*c
g_HL2 = (dirac*n*hb*c)**2/e_HL2
QeHL2 = G*e_HL2/(4*sp.pi*c**4)
QmHL2 = G*g_HL2/(4*sp.pi*c**4)
# ---- Gaussian bookkeeping: e^2 = alpha hbar c, e g = n hbar c / 2  (correct value; mutation scales by dirac/(2 pi))
e_G2 = al*hb*c
g_G2 = (sp.Rational(1, 2)*n*hb*c*(dirac/(2*sp.pi)))**2/e_G2
QeG2 = G*e_G2/c**4
QmG2 = G*g_G2/c**4
prodHL = sp.simplify(sp.sqrt(QeHL2*QmHL2)/lP2)
prodG = sp.simplify(sp.sqrt(QeG2*QmG2)/lP2)
print("Q_e Q_m / l_P^2 (HL)      =", prodHL)
print("Q_e Q_m / l_P^2 (Gaussian) =", prodG)
chk("D1a HL product = n/2, alpha-free", sp.simplify(prodHL - n/2) == 0)
chk("D1b Gaussian product = n/2, alpha-free", sp.simplify(prodG - n/2) == 0)
chk("D1c the two unit systems agree", sp.simplify(prodHL - prodG) == 0)
chk("D1d Q_e^2 = alpha l_P^2 in both", sp.simplify(QeHL2/lP2 - al) == 0 and sp.simplify(QeG2/lP2 - al) == 0)
Qm2 = sp.simplify(QmHL2/lP2)
print("Q_m^2 / l_P^2 =", Qm2)
chk("D1e Q_m^2 = n^2 l_P^2/(4 alpha)", sp.simplify(Qm2 - n**2/(4*al)) == 0)

# ---- D2: extremal Lambda=0 objects (r_+ = Q in geometric units), symbolic then numeric
alpha0 = mp.mpf(1)/mp.mpf("137.035999177")
r_m = sp.sqrt(n**2/(4*al))          # in l_P
A_m = 4*sp.pi*r_m**2                # in l_P^2
S_m = A_m/4                         # in units of k_B, = A/(4 l_P^2)
Mm = r_m                            # M/m_P = Q/l_P (extremal)
print("\nD2 magnetic extremal, n quanta: r_+/l_P =", sp.simplify(r_m), " A/l_P^2 =", sp.simplify(A_m), " S =", sp.simplify(S_m), " M/m_P =", sp.simplify(Mm))
chk("D2a A/l_P^2 = pi n^2/alpha and S = pi n^2/(4 alpha)", sp.simplify(A_m - sp.pi*n**2/al) == 0 and sp.simplify(S_m - sp.pi*n**2/(4*al)) == 0)
vals = {al: alpha0, n: 1}
rm1 = float(r_m.subs(vals)); Am1 = float(A_m.subs(vals)); Sm1 = float(S_m.subs(vals))
print(f"   n=1 at alpha=1/137.036: r_+ = M/m_P = {rm1:.5f} l_P, A = {Am1:.3f} l_P^2, S = {Sm1:.4f}")
print(f"   electric n=1 extremal: r_+ = M/m_P = sqrt(alpha) = {float(mp.sqrt(alpha0)):.5f} l_P  (< 1: sub-Planckian, classical RN not trustworthy)")
chk("D2b electric n=1 extremal radius sqrt(alpha) l_P < l_P; magnetic n=1 radius 1/(2 sqrt alpha) l_P > l_P", float(mp.sqrt(alpha0)) < 1 < rm1)
# r_+ Q_e-by-Q_m ratio
print(f"   Q_m/Q_e (n=1) = 1/(2 alpha) = {float(1/(2*alpha0)):.4f}")

# ---- D3: self-dual point
selfdual = sp.solve(sp.Eq(sp.sqrt(al), sp.sqrt(n**2/(4*al))), al)
print("\nD3 self-dual Q_e = Q_m:  alpha =", selfdual)
chk("D3a self-dual alpha = n/2", selfdual == [n/2])
chk("D3b self-dual alpha (n=1 -> 1/2) is NOT within 1e-3 of the target", abs(0.5/float(alpha0) - 1) > 1e-3, f"(ratio to target {0.5/float(alpha0):.1f})")

# ---- D4: dS capacity, x from AH5 inputs
G_si, hb_si, c_si = mp.mpf("6.67430e-11"), mp.mpf("1.054571817e-34"), mp.mpf(299792458)
Mpc = mp.mpf("3.0856775814913673e22")
H0 = mp.mpf("67.4e3")/Mpc
Lam = 3*mp.mpf("0.6847")*H0**2/c_si**2
lP2n = G_si*hb_si/c_si**3
x = Lam*lP2n
print(f"\nD4 x = Lambda l_P^2 = {mp.nstr(x,4)}")
Nmax_e = 1/(2*mp.sqrt(alpha0*x))        # electric quanta at ultracold Q^2 = 1/(4 Lambda)
Nmax_m = mp.sqrt(alpha0/x)              # Dirac quanta n with n^2/(4 alpha) x = 1/4
print(f"   N_max(electric quanta at Q^2 = 1/(4 Lambda)) = {mp.nstr(Nmax_e,4)}")
print(f"   N_max(Dirac quanta)                          = {mp.nstr(Nmax_m,4)}")
# alpha as a function of the integer: alpha = y(1-y)/(n^2 x)  (electric), y=1/2 -> 1/(4 n^2 x)
window = Nmax_e*mp.mpf("1e-3")          # width in n for |dalpha/alpha| < 1e-3  (dalpha/alpha = -2 dn/n)
print(f"   integers n giving alpha within 1e-3 of target (electric, ultracold): about {mp.nstr(window,3)}")
chk("D4a alpha = 1/(4 n^2 x) reproduces target at n = N_max_e", abs(1/(4*Nmax_e**2*x)/alpha0 - 1) < mp.mpf("1e-25"))
chk("D4b a 1e-3 window in alpha contains > 1e50 integers, so an integer fit is automatic (no evidence)", window > mp.mpf("1e50"))
chk("D4c N_max is ~ 1e61 (i.e. Q_special is 122 orders from Planck), not O(1)", mp.mpf("1e60") < Nmax_e < mp.mpf("1e62"))

# ---- D5: declared handles on k = r_+/l_P of the minimal magnetic extremal BH; alpha = 1/(4 k^2)
Z = 2*mp.sqrt(8*mp.pi/3)
handles = [("1", mp.mpf(1)), ("2", mp.mpf(2)), ("sqrt(8pi/3)", mp.sqrt(8*mp.pi/3)), ("Z=2sqrt(8pi/3)", Z),
           ("2pi", 2*mp.pi), ("4pi", 4*mp.pi), ("Z^2=32pi/3", Z**2), ("N/2, N=11", mp.mpf(11)/2), ("N/2, N=12", mp.mpf(12)/2)]
kreq = 1/(2*mp.sqrt(alpha0))
print(f"\nD5 required k = 1/(2 sqrt alpha) = {mp.nstr(kreq,8)} (reported, not fitted)")
hits = 0
for name, k in handles:
    a = 1/(4*k**2)
    rel = a/alpha0 - 1
    hit = abs(rel) < mp.mpf("1e-3")
    hits += hit
    print(f"   k = {name:16s} = {mp.nstr(k,7):>10s}  alpha = 1/{mp.nstr(1/a,6):>8s}  rel.dev = {mp.nstr(rel,4):>10s}  {'HIT' if hit else 'no hit'}")
# self-dual handle
hit_sd = abs(mp.mpf("0.5")/alpha0 - 1) < mp.mpf("1e-3"); hits += hit_sd
ntrial = len(handles) + 1
p1 = 2*mp.mpf("5e-4")/mp.log(100)
print(f"   + self-dual alpha=1/2: {'HIT' if hit_sd else 'no hit'}")
print(f"   TRIAL COUNT = {ntrial}; per-handle chance probability = {mp.nstr(p1,3)}; expected chance hits = {mp.nstr(ntrial*p1,3)}; observed hits = {hits}")
chk("D5a trial count declared = 10", ntrial == 10)
chk("D5b zero hits among the declared handles (as expected)", hits == 0)
print(f"   post-hoc, NOT scored: Z/k_req = {mp.nstr(Z/kreq,6)} (1.1% off); 1/(4 alpha) = {mp.nstr(1/(4*alpha0),6)} vs Z^2 = {mp.nstr(Z**2,6)}, difference = {mp.nstr(1/(4*alpha0)-Z**2,4)} (numerology 4Z^2+3 would need this = 3/4)")

print("\nSUMMARY: %d/%d checks pass (MUTATE=%s)" % (sum(c[1] for c in checks), len(checks), MUT))
sys.exit(0 if all(c[1] for c in checks) else 1)
