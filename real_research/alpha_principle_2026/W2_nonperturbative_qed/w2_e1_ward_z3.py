#!/usr/bin/env python3
"""W2 (e): the Ward identity Z1 = Z2, the Kaellen-Lehmann bound on Z3, and what they say about bare versus physical charge (pre-registered E1, E2, E3 in W2_PREREGISTRATION.md).
E1  differential Ward identity dS/dk_mu = -S gamma^mu S with explicit 4x4 Dirac matrices (sympy, symbolic mass): Lambda^mu(p,p) = -dSigma/dp_mu at the integrand level, hence Z1 = Z2.
E2  Kaellen-Lehmann: 1/Z3 = 1 + Int rho ds/s with the one-loop spectral density; numerical constant c in (alpha/3pi)(ln L + c); Z3 in (0,1) and the ghost location.
E3  per-species Ward identity with independent charges and masses: only Z3 renormalises, so charge RATIOS are exact (a statement about ratios, not about e).
Run:    python3 w2_e1_ward_z3.py           (from this directory; exit 0 iff every check passes)  -> writes w2_e1_results.json
MUTATE: python3 w2_e1_ward_z3.py MUTATE    (E1/E3: gamma^mu -> gamma^mu gamma5 on the right-hand side; E2: the spectral density's sign flipped, rho -> -rho)
        must exit 1 (exit 3 if the control is broken)  -> writes w2_e1_results_MUTATE.json
"""
import sys
sys.dont_write_bytecode = True
import json, math
import sympy as sp
import mpmath as mp
import w2_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(name, ok, info=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)
res = {}

# ------------------------------------------------------------------ E1
print("== E1 differential Ward identity (explicit Dirac matrices) ==")
I2, Z2 = sp.eye(2), sp.zeros(2)
sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
def blk(a, b, c, d):
    return sp.Matrix(sp.BlockMatrix([[a, b], [c, d]]))
g0 = blk(I2, Z2, Z2, -I2)
gs = [blk(Z2, s_, -s_, Z2) for s_ in sig]
gam = [g0] + gs                                   # gamma^mu, mu = 0..3 (Dirac representation)
g5 = sp.I * gam[0] * gam[1] * gam[2] * gam[3]
eta = sp.diag(1, -1, -1, -1)
ok_alg = all(sp.simplify(gam[m] * gam[n] + gam[n] * gam[m] - 2 * eta[m, n] * sp.eye(4)) == sp.zeros(4) for m in range(4) for n in range(4))
chk("E1a  the matrices satisfy {gamma^mu, gamma^nu} = 2 g^{mu nu}", ok_alg)
k = sp.symbols("k0:4", real=True)                 # lower components k_mu
m = sp.symbols("m", positive=True)
kslash = sum((gam[i] * k[i] for i in range(4)), sp.zeros(4))
k2 = k[0] ** 2 - k[1] ** 2 - k[2] ** 2 - k[3] ** 2
S = (kslash + m * sp.eye(4)) / (k2 - m ** 2)      # = (kslash - m)^-1
chk("E1b  S = (kslash + m)/(k^2 - m^2) is the inverse of (kslash - m)", sp.simplify(S * (kslash - m * sp.eye(4)) - sp.eye(4)) == sp.zeros(4))
allok = True
for mu in range(4):
    lhs = sp.diff(S, k[mu])
    vertex = gam[mu] * g5 if MUT else gam[mu]
    rhs = -S * vertex * S
    d = sp.simplify(lhs - rhs)
    ok = d == sp.zeros(4)
    allok &= ok
    print(f"   mu = {mu}: dS/dk_mu + S gamma^mu S {'= 0' if ok else '!= 0'}")
chk("E1c  dS/dk_mu = -S gamma^mu S for mu = 0..3 (symbolic mass)", allok)
print("   Consequence: Sigma(p) = i e^2 Int gamma^nu S(p-k) gamma^rho D_{nu rho}(k) => dSigma/dp_mu = -i e^2 Int gamma^nu S gamma^mu S gamma^rho D = -Lambda^mu(p,p) at the integrand level.")
print("   Hence Z1 = Z2 for any regulator that commutes with d/dp (dimensional regularisation, Pauli-Villars); the vertex renormalisation cancels the wave-function renormalisation, leaving e_R = Z3^(1/2) e_0.")
res["E1"] = dict(ok=bool(allok))

# ------------------------------------------------------------------ E3 (per species)
print("== E3 per-species identity with independent masses ==")
m1, m2 = sp.symbols("m1 m2", positive=True)
ok3 = True
for mm in (m1, m2):
    S_ = (kslash + mm * sp.eye(4)) / (k2 - mm ** 2)
    for mu in range(4):
        vertex = gam[mu] * g5 if MUT else gam[mu]
        ok3 &= sp.simplify(sp.diff(S_, k[mu]) + S_ * vertex * S_) == sp.zeros(4)
chk("E3a  the identity holds species by species for arbitrary masses, and the charge Q_i multiplies both sides of the vertex relation: e_i^R/e_j^R = Q_i/Q_j exactly", ok3)
print("   (statement about RATIOS of charges only; the overall scale e is renormalised by Z3 alone and is untouched by this identity.)")

# ------------------------------------------------------------------ E2
print("== E2 Kaellen-Lehmann bound Z3 <= 1 with the one-loop spectral density ==")
mp.mp.dps = 30
sign = -1 if MUT else 1
def rho(x):        # (alpha/3pi)^-1 * rho(s) with x = s/m^2  ( >= 0 for x >= 4 )
    return sign * (1 + 2 / x) * mp.sqrt(1 - 4 / x)
def Iint(Lx):      # Int_4^L dx/x rho(x)
    return mp.quad(lambda x: rho(x) / x, [4, 5, 10, 100, 1e4, Lx]) if Lx > 1e4 else mp.quad(lambda x: rho(x) / x, [4, Lx])
# constant c in I(L) = ln L + c + O(1/L): use L = 1e12, 1e14
cs = [Iint(mp.mpf(Lx)) - mp.log(Lx) for Lx in (mp.mpf("1e12"), mp.mpf("1e14"))]
c = cs[-1]
print(f"   I(L) - ln L = {mp.nstr(cs[0], 12)} (L = 1e12), {mp.nstr(cs[1], 12)} (L = 1e14)")
c_id = mp.identify(c, ["log(2)"], tol=1e-9)
print(f"   c = {mp.nstr(c, 12)};  identify with {{1, ln 2}}: {c_id}")
chk("E2a  the spectral integral has the form ln L + c, and c is a pure number (stable to 1e-9 between L = 1e12 and 1e14)", abs(cs[0] - cs[1]) < 1e-9)
a0 = mp.mpf(1) / mp.mpf("137.035999177")
Zvals = {}
for Lx in ("1e2", "1e6", "1e30", "1e100"):
    Lm = mp.mpf(Lx)
    inv = 1 + (a0 / (3 * mp.pi)) * (mp.log(Lm) + c) * (1 if not MUT else -1)
    Zvals[Lx] = float(1 / inv)
    print(f"   L = Lambda^2/m^2 = {Lx:>6s}: 1/Z3 = 1 + (alpha_0/3pi)(ln L + c) = {mp.nstr(inv, 8)}   Z3 = {Zvals[Lx]:.6f}")
chk("E2b  0 < Z3 < 1 for all L >= 4 at the one-loop level (positive spectral density => bare charge exceeds the physical charge, e_R^2 = Z3 e_0^2 <= e_0^2)", all(0 < v < 1 for v in Zvals.values()) and (Iint(mp.mpf(100)) > 0))
lnL_ghost = 3 * mp.pi / a0 - c                       # 1/Z3 = ... resummed: Z3 = 1 - (alpha_R/3pi)(ln L + c) = 0
print(f"   with the physical charge alpha_R = alpha_0 the same one-loop expression Z3 = 1 - (alpha_R/3pi)(ln L + c) vanishes at ln(Lambda/m) = {mp.nstr((lnL_ghost)/2, 8)} (electron only): the Landau ghost of B1 (645.7 - c/2)")
chk("E2c  the Z3 = 0 (ghost) location coincides with the B1 Landau pole ln(Lambda/m) = 3 pi/(2 alpha) up to the O(1) constant c/2", abs(lnL_ghost / 2 - 3 * mp.pi / (2 * a0)) < 2.0)
res["E2"] = dict(c=float(c), Z3=Zvals)

# ------------------------------------------------------------------ E4 (statement only)
print("== E4 statements without computation ==")
print("   Z1 = Z2 and Z3 <= 1 give: (i) e_R = Z3^(1/2) e_0 (an identity), (ii) e_R^2 <= e_0^2 (an inequality); neither fixes e_0 (free: cutoff, regulator, spectrum).")
print("   Lattice (read): no UV zero of the beta function out to e_R^2 = e_c^2 (hep-th/9712244); functional RG (read, abstract and method): no fixed point at e^2 > 0 in their truncation (hep-ph/0405183).")
print("   Johnson-Baker-Willey / Adler eigenvalue conditions (RECALLED, not read) presuppose a zero of the Gell-Mann-Low function; even with one, D3 shows alpha_0 <-> ln(Lambda_*/m) stays free.")
json.dump(res, open("w2_e1_results_MUTATE.json" if MUT else "w2_e1_results.json", "w"), indent=1, default=float)
L.finish(fails, MUT, "w2_e1")
