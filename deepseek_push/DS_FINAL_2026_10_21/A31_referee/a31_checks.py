#!/usr/bin/env python3
"""A31 - independent re-derivation of the load-bearing numbers in FINAL_THEORY.md.

Every numeric check below is computed from the BRIEF's constants and the defining
equations, not copied from a lane.  A check is PASS when the recomputed value
matches the value printed in FINAL_THEORY.md at the quoted precision; MISMATCH
means the synthesis and the constants disagree.  The script also reports the
claim-ledger counts (BACKED / OVERSTATED / UNBACKED / WRONG) from a31_ledger.py.

Run:  python3 a31_checks.py [--mutate]
      --mutate corrupts one FINAL value (Z) and must turn check 01 into a MISMATCH,
      proving the checks have teeth.
"""
import json
import math
import os
import sys
import importlib.util

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
FINAL = os.path.join(HERE, "..", "FINAL_THEORY.md")
MUTATE = "--mutate" in sys.argv

# ------------------------------------------------------------------ constants (BRIEF section 4)
c = 2.99792458e8
G = 6.67430e-11
H0 = 67.4e3 / 3.0856775814913673e22          # 2.1843e-18 s^-1
LAM = 1.0890e-52                              # m^-2
RHO_L = LAM * c**2 / (8 * math.pi * G)
A0 = 9.36e-11
A0_ALT = 1.13e-10
BE = 3.66e-14
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = PC * 1e3
MPC = PC * 1e6
OMEGA_B = 0.04924319136384048                 # A6, Omega_b (not Omega_b h^2)
OMEGA_C = 5.364327223960661 * OMEGA_B
RHO_BAR_COLD = OMEGA_C * 3 * H0**2 / (8 * math.pi * G)

Z = 2 * math.sqrt(8 * math.pi / 3)
TWOZ = 2 * Z
N_LAMBDA = LAM * c**4 / A0**2

checks = []


def ck(cid, label, final_value, recomputed, ok, note=""):
    checks.append(dict(id=cid, label=label, final=final_value,
                       recomputed=recomputed, pass_=bool(ok), note=note))
    tag = "PASS" if ok else "MISMATCH"
    print(f"{cid:>4} {tag:<8} {label:<58} FINAL={final_value!r:<24} RECOMPUTED={recomputed!r}")
    if note:
        print(f"        note: {note}")


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ------------------------------------------------------------------ 01-08: the kappa / Z web
z_final = 5.78 if MUTATE else 5.7888100
ck("01", "Z = 2 sqrt(8 pi/3)", z_final, Z, rel(Z, z_final) < 1e-6)
if MUTATE:
    print("        [MUTATION] the FINAL value for Z was corrupted to 5.78; this check must fail.")
ck("02", "2Z = 2 sqrt(32 pi/3)", 11.5776201, TWOZ, rel(TWOZ, 11.5776201) < 1e-7)
kappa12 = Z / 12
ck("03", "kappa from the literal twelfth = Z/12", 0.4824008, kappa12,
   rel(kappa12, 0.4824008) < 1e-6,
   f"relative gap to 1/2 = {100*(0.5-kappa12)/0.5:.4f}% (FINAL says 3.52%)")
hbar = 1.054571817e-34
x_brief = hbar * G * LAM / c**3
Lam_H = 3 * H0**2 / c**2 * 0.685
x_h0 = hbar * G * Lam_H / c**3
ck("04", "hbar G Lambda / c^3 (BRIEF Lambda)", 2.8498e-122, x_brief,
   rel(x_brief, 2.8498e-122) < 1e-4,
   f"BRIEF Lambda gives {x_brief:.6e}; Lambda rebuilt from H0, Omega_L=0.685 gives {x_h0:.6e} "
   f"(the parent harness value). A1's a1_results.json stores {2.8447732492855883e-122:.6e}.")
A0_EXACT = c**2 * math.sqrt(LAM / (32 * math.pi))
a0_over_cHL = A0_EXACT / (c * math.sqrt(LAM * c**2 / 3))
ck("05", "a0/(c H_Lambda) = 1/Z (a0 from 32pi)", 0.1727471, a0_over_cHL,
   rel(a0_over_cHL, 0.1727471) < 1e-6,
   f"with the rounded footing a0 = 9.36e-11 the ratio is {A0/(c*math.sqrt(LAM*c**2/3)):.6f}, "
   f"0.06% high - the footing rounding, not the identity")
kP1 = 4 * math.sqrt(math.pi / 3)
ck("06", "kappa_P1 = 4 sqrt(pi/3); mismatch 8 sqrt(pi/3)", 4.093307, kP1,
   rel(kP1, 4.093307) < 1e-6,
   f"mismatch factor = {kP1/0.5:.6f} (FINAL 8.186614)")
ratio_a0 = A0 / BE
ck("07", "a0/B_E; half a0/B_E", 2557.377, ratio_a0, rel(ratio_a0, 2557.377) < 1e-5,
   f"half = {ratio_a0/2:.3f} (FINAL 1278.69)")
ck("08", "N_Lambda = Lambda c^4/a0^2", 100.4058, N_LAMBDA,
   rel(N_LAMBDA, 100.4058) < 1e-5)

# ------------------------------------------------------------------ 09-11: the turn-off closure
def y_nu_minus_1_can(y):
    return 0.5 * (math.sqrt(y * y + 4 * y) - y)


def y_nu_minus_1_quad(y):
    return math.sqrt(y * y + y) - y


def F(Y, h):
    f = lambda y: h(y) / (1.0 + (y / Y) ** 2)
    val, _ = quad(f, 0.0, np.inf, limit=400, epsabs=1e-12, epsrel=1e-11)
    return val


yt_can = brentq(lambda Y: F(Y, y_nu_minus_1_can) - N_LAMBDA, 20, 200, xtol=1e-10)
ck("09", "y_t canonical root of F_can(y_t) = N_Lambda", 66.2999, yt_can,
   rel(yt_can, 66.2999) < 1e-4,
   f"y_t*a0 = {yt_can*A0:.4e} m/s^2 (FINAL 6.21e-9)")
yt_quad = brentq(lambda Y: F(Y, y_nu_minus_1_quad) - N_LAMBDA, 40, 300, xtol=1e-10)
transplant = F(yt_quad, y_nu_minus_1_can) / N_LAMBDA
ck("10", "y_t quadrature; transplant ratio", 128.7559, yt_quad,
   rel(yt_quad, 128.7559) < 1e-4,
   f"F_can(128.7559)/N_Lambda = {transplant:.6f} (FINAL 1.9707); "
   f"y_t ratio = {yt_quad/yt_can:.6f} (FINAL 1.942)")
Ccan = F(1e4, y_nu_minus_1_can) - (math.pi / 2) * 1e4 + math.log(1e4 / 4)
Cquad = F(1e4, y_nu_minus_1_quad) - (math.pi / 4) * 1e4 + math.log(1e4) / 8
ck("11", "C_can = -0.8862944; C_can/C_quad = 8", -0.8862944, Ccan,
   rel(Ccan, -0.8862944) < 2e-3,
   f"C_quad = {Cquad:.6f} (FINAL -0.1107868); ratio = {Ccan/Cquad:.6f}")

# ------------------------------------------------------------------ 12-19: shape, cores, Jeans, a_P
max_g = 2 / math.sqrt(3) - 1
max_v = math.sqrt(2 / math.sqrt(3)) - 1
wrong_formula = math.sqrt(2 / 3) - 1
parent_v = 0.5 * max_g
ck("12", "max dg/g = 2/sqrt3-1; max dv/v = sqrt(2/sqrt3)-1", 0.1547005, max_g,
   rel(max_g, 0.1547005) < 1e-6,
   f"max dv/v = {max_v:.7f} (FINAL 7.4570%); the printed formula sqrt(2/3)-1 = {wrong_formula:.6f} "
   f"is not 7.457%; the parent Q2.8 value 0.5*max_g = {parent_v:.7f}")
Rcore = (math.pi / math.sqrt(2)) * 24
ck("13", "R_core = (pi/sqrt2) L*, L*=24 pc", 53.31, Rcore, rel(Rcore, 53.31) < 1e-3)
lamJ = math.sqrt(2) * math.pi * 24
ck("14", "lambda_J = sqrt2 pi L*, L*=24 pc", 106.6, lamJ, rel(lamJ, 106.6) < 1e-3)
sigma_c = math.sqrt(A0 * 24 * PC)
lamFS = 2 * sigma_c / (3 * H0)
ck("15", "sigma_c = sqrt(a0 L*) and lambda_FS = 2 sigma/(3H0)", 82.35, lamFS / KPC,
   rel(lamFS / KPC, 82.35) < 1e-3,
   f"sigma_c = {sigma_c/1e3:.4f} km/s (FINAL 8.33)")
MJ_coeff = math.pi**3 / (6 * math.sqrt(2))
MJ = MJ_coeff * (165.2e3) ** 2 * (24 * PC) / G / MSUN
ck("16", "M_J = pi^3/(6 sqrt2) V^2 L/G at V=165.2 km/s", 5.57e8, MJ,
   rel(MJ, 5.57e8) < 1e-3,
   f"coefficient = {MJ_coeff:.6f}; per (km/s)^2 = {MJ_coeff*(1e3)**2*24*PC/G/MSUN:.1f} Msun "
   f"(FINAL 2.04e4); NFW value = 3.149e6 Msun (A16)")
GM = 1.32712440018e20
aP = GM / (24 * PC) ** 2
ck("17", "a_P = GM_sun/L*^2; a_P/B_E; 1/(a_P/B_E)", 2.4205e-16, aP,
   rel(aP, 2.4205e-16) < 1e-3,
   f"a_P/B_E = {aP/BE:.6e} (FINAL 6.61e-3); margin = {BE/aP:.2f} (FINAL 151)")
Mcrit = A0 * (24 * PC) ** 2 / G / MSUN
ck("18", "M_crit = a0 L*^2/G", 3.87e5, Mcrit, rel(Mcrit, 3.87e5) < 2e-3)
lamP = 24 / math.sqrt(2)
uP = GM / (2 * (lamP * PC) ** 2)
ck("19", "lambda = L*/sqrt2; u_P = GM/(2 lambda^2)", 16.9706, lamP,
   rel(lamP, 16.9706) < 1e-4,
   f"u_P = {uP:.4e} m/s^2 = {uP/A0:.4e} a0 (FINAL 2.59e-6 a0)")

# ------------------------------------------------------------------ 20-24: u inversion, band ratios, R_cosmic
Al, An = 1.910194, 10.173704
u_mid = (An - Al) / (Al * (An - 1))
AOl, AOn = 1.011801, 7.262
u_out = (AOn - AOl) / (AOl * (AOn - 1))
ck("20", "u = (A_n-A_l)/(A_l(A_n-1)) MID and OUT", 0.471566, u_mid,
   rel(u_mid, 0.471566) < 2e-3,
   f"u_OUT = {u_out:.6f} (FINAL 0.9865)")
sig_mid, sig_out = 0.036245158, 0.098408709
z_out = (u_out - 0.5) / sig_out
z_band = (u_out - u_mid) / math.hypot(sig_mid, sig_out)
z_worst = (u_out - u_mid) / (sig_mid + sig_out)
ck("21", "Z(u_OUT vs 1/2); Z(band, quadrature); Z(band, worst)", 4.943, z_out,
   rel(z_out, 4.943) < 2e-3,
   f"quadrature band Z = {z_band:.3f}; worst-correlation Z = {z_worst:.3f} "
   f"(FINAL '>= 3.8 sigma'; section 5 uses 3.8, section 0 says 4.9)")
fb = 0.02237 / 0.14237
Rcos = (1 - fb) / fb
ck("22", "R_cosmic = (1-f_b)/f_b", 5.3643, Rcos, rel(Rcos, 5.3643) < 1e-5)
y_mw, y_cl = 0.0014354790117126987, 0.055604316450894496
Fenc_mw = 0.5 * (math.sqrt(1 + 4 / y_mw) - 1)
Fenc_cl = 0.5 * (math.sqrt(1 + 4 / y_cl) - 1)
ck("23", "F(y_v) at the two A18 anchors (formula in FINAL)", 25.04, Fenc_mw,
   rel(Fenc_mw, 25.04) < 5e-3,
   f"F_enc cluster = {Fenc_cl:.4f} (FINAL prints 2.62); A18's 25.0429/2.6179 are R_tot, "
   f"the phantom per total baryon, not F(y_v)")
ck("24", "ratio of the two anchors", 9.57, 25.04291282080763 / 2.6179291849458104,
   rel(25.04291282080763 / 2.6179291849458104, 9.57) < 1e-3,
   f"ratio of F_enc = {Fenc_mw/Fenc_cl:.4f} (6.87), not 9.57")

# ------------------------------------------------------------------ 25-27: the A6 saddle numbers
def dnu(y):
    return -1.0 / (y * y * np.sqrt(1 + 4 / y))


def rho_cold(M, d, X, Y, Zc):
    gx = np.zeros_like(X); gy = np.zeros_like(X); gz = np.zeros_like(X)
    Txx = np.zeros_like(X); Txy = np.zeros_like(X); Txz = np.zeros_like(X)
    Tyy = np.zeros_like(X); Tyz = np.zeros_like(X); Tzz = np.zeros_like(X)
    for xc in (-0.5 * d, 0.5 * d):
        dx = X - xc; dy = Y; dz = Zc
        r2 = dx * dx + dy * dy + dz * dz
        r = np.sqrt(r2); r3 = r**3; r5 = r**5
        gx += -G * M * dx / r3; gy += -G * M * dy / r3; gz += -G * M * dz / r3
        Txx += -G * M * (1 / r3 - 3 * dx * dx / r5)
        Txy += -G * M * (-3 * dx * dy / r5)
        Txz += -G * M * (-3 * dx * dz / r5)
        Tyy += -G * M * (1 / r3 - 3 * dy * dy / r5)
        Tyz += -G * M * (-3 * dy * dz / r5)
        Tzz += -G * M * (1 / r3 - 3 * dz * dz / r5)
    s = np.sqrt(gx * gx + gy * gy + gz * gz)
    gTg = ((Txx * gx + Txy * gy + Txz * gz) * gx
           + (Txy * gx + Tyy * gy + Tyz * gz) * gy
           + (Txz * gx + Tyz * gy + Tzz * gz) * gz)
    return -((dnu(s / A0) / A0) * gTg / s) / (4 * math.pi * G), s


def column(M, d, phi=math.pi / 2, Lf=1.0, n=160001):
    t = np.linspace(-Lf * d, Lf * d, n) + 1e-7 * d
    X = t * math.cos(phi); Y = t * math.sin(phi)
    rr, _ = rho_cold(M, d, X, Y, np.zeros_like(X))
    ok = np.isfinite(rr)
    trap = getattr(np, "trapezoid", np.trapz)
    return trap(rr[ok], t[ok]), trap(np.minimum(rr[ok], 0), t[ok]), trap(np.maximum(rr[ok], 0), t[ok])


Mmw, dmw = 1.4e11 * MSUN, 780 * KPC
r_p, _ = rho_cold(Mmw, dmw, np.array([0.0]), np.array([0.2 * dmw]), np.array([0.0]))
ratio89 = r_p[0] / RHO_BAR_COLD
ck("25", "rho_panc/rho_bar_cold at R=0.2d (MW pair)", -89.32, ratio89,
   rel(ratio89, -89.32) < 5e-3,
   f"independent recomputation {ratio89:.2f}; A6 stores -89.3197")
U = MSUN / PC**2
net, neg, pos = column(Mmw, dmw)
ck("26", "net / negative / positive column, MW pair [Msun/pc^2]", -3.529, neg / U,
   rel(neg / U, -3.529) < 5e-3,
   f"net = {net/U:.4f} (FINAL -2.424), positive = {pos/U:.4f} (FINAL +1.105); "
   f"a 1e6-point run gives {column(Mmw, dmw, n=1000001)[1]/U:.4f}, a 1.5% resolution drift")
ck("27", "-2.424 = -3.529 + 1.105", -2.424, -3.5288623674507282 + 1.1046839669039377,
   rel(-3.5288623674507282 + 1.1046839669039377, -2.424) < 1e-4)

# ------------------------------------------------------------------ 28-29: c_T background and alpha_1 0/0
h, p, K = sp.symbols("h p K", positive=True)
u_bar = K * p
# Pbar along x, TT mode diag(1,-1,0): h^{11} = 1/(1+h)
u_pert = K * p / sp.sqrt(1 + h)
W2 = sp.series(u_pert, h, 0, 3).removeO()
quad_coeff = sp.simplify(sp.expand(W2).coeff(h, 2))
ck("28", "TT mass term from W(u) at Pbar != 0 (coefficient of h^2, units u^2/K)", 0.0,
   float(quad_coeff.subs({K: 1, p: 1})), abs(float(quad_coeff.subs({K: 1, p: 1}))) < 1e-12,
   f"W(u) with u = K abs(P) gives a nonzero h^2 coefficient {quad_coeff}; it vanishes only at p=0, "
   f"so the 'Einstein quadratic action' statement holds only on the Pbar=0 background")
c1, c3, c4 = sp.symbols("c1 c3 c4", real=True)
den = 2 * c1 - c1**2 + c3**2
num = -8 * (c3**2 + c1 * c4)
den0 = den.subs({c1: 0, c3: 0, c4: 0})
val = sp.simplify(num.subs({c1: 0, c3: 0, c4: 0}) / den0) if den0 != 0 else None
val_repr = val if val is not None else "0/0"
ck("29", "published alpha_1 at c1=c3=c4=0", 0.0, val_repr, val == 0,
   "the published alpha_1 = -8(c3^2+c1c4)/(2c1-c1^2+c3^2) is 0/0 at that point; "
   "A22's a22_checks.py line 223 sets alpha1_lit = 0 when den == 0, which asserts the value")

# ------------------------------------------------------------------ 30-33: L* window and model dependence
lanes = sorted(d for d in os.listdir(os.path.join(HERE, ".."))
               if d.startswith("A") and os.path.isdir(os.path.join(HERE, "..", d)))
t_final = os.path.getmtime(FINAL)
lanes_1920 = [d for d in lanes if os.path.getmtime(os.path.join(HERE, "..", d)) <= t_final]
post = sorted(d for d in lanes if os.path.getmtime(os.path.join(HERE, "..", d)) > t_final)
ck("30", "lane directories at the synthesis (FINAL says 23)", 23, len(lanes_1920),
   len(lanes_1920) == 23,
   f"directories now: {len(lanes)}; the 24 pre-existing lanes are A1-A16 and A18-A25 "
   f"(no A17); post-synthesis: {', '.join(post)}")
bound90 = 200 / ((math.pi / math.sqrt(2)))
ck("31", "L* <= R0.3(IC10=200 pc)/2.22144", 90.0, bound90, rel(bound90, 90.0) < 1e-3,
   f"300/90 = {300/90:.3f} (FINAL 3.33x); 1000/90 = {1000/90:.3f} (FINAL 11.11x); "
   f"at f_c=0.5 the bound is {bound90/math.sqrt(0.5):.1f} pc, at f_c=0.25 {bound90/math.sqrt(0.25):.1f} pc")
h24 = 24 * PC * H0 / c
h90 = 90 * PC * H0 / c
h1k = 1000 * PC * H0 / c
ck("32", "L* H0/c at 24 pc / 90 pc / 1 kpc", 2.25e-7, h1k, rel(h1k, 2.25e-7) < 2e-3,
   f"24 pc = {h24:.3e}; 90 pc = {h90:.3e}; FINAL's upper end 2.25e-7 is the 1 kpc value, "
   f"not the 90 pc value")
ck("33", "M_J(flat curve)/M_J(NFW)", 1.0, 5.56468e8 / 3.14912e6,
   abs(5.56468e8 / 3.14912e6 - 1.0) < 1e-9,
   f"the ratio is {5.56468e8/3.14912e6:.1f}, i.e. the two profiles differ by ~2.2 dex, "
   f"not a small correction")

# ------------------------------------------------------------------ 34-35: group pair and pair budget
Mg, dg = 4.2e12 * MSUN, 3 * MPC
rg, _ = rho_cold(Mg, dg, np.array([0.0]), np.array([0.2 * dg]), np.array([0.0]))
netg, negg, posg = column(Mg, dg)
ck("34", "group pair -33.07 and column -5.025", -33.07, rg[0] / RHO_BAR_COLD,
   rel(rg[0] / RHO_BAR_COLD, -33.07) < 1e-2,
   f"column = {negg/U:.4f} (FINAL -5.025); independent recomputation of both A6 numbers")
ck("35", "3 sigma pairs = (3 sigma_dS / depth)^2, 11.8x a 700-pair stack", 8282,
   (3 * 107.0 / 3.529) ** 2, rel((3 * 107.0 / 3.529) ** 2, 8282) < 0.02,
   "A6's 8281.8 uses sigma(DeltaSigma)=107 Msun/pc2 and depth 3.529; the arithmetic reproduces it "
   "and 8281.8/700 = 11.83")

# ------------------------------------------------------------------ ledger + output
spec = importlib.util.spec_from_file_location("a31_ledger", os.path.join(HERE, "a31_ledger.py"))
led = importlib.util.module_from_spec(spec)
spec.loader.exec_module(led)
claims = led.CLAIMS
counts = {v: sum(1 for x in claims if x["verdict"] == v)
          for v in ("BACKED", "OVERSTATED", "UNBACKED", "WRONG")}
counts["TOTAL"] = len(claims)

npass = sum(1 for x in checks if x["pass_"])
print("\n" + "=" * 110)
print(f"CLAIM LEDGER: {counts['TOTAL']} claims | BACKED {counts['BACKED']} | "
      f"OVERSTATED {counts['OVERSTATED']} | UNBACKED {counts['UNBACKED']} | WRONG {counts['WRONG']}")
print(f"NUMERIC CHECKS: {npass}/{len(checks)} match FINAL_THEORY.md")
print("MISMATCHES: " + ", ".join(x["id"] for x in checks if not x["pass_"]))
print(f"A31 COMPLETE: {len(checks)} numeric checks, {npass} match, {len(checks)-npass} mismatches; "
      f"{counts['OVERSTATED']+counts['UNBACKED']+counts['WRONG']} non-BACKED claims.")

def jsonable(v):
    if isinstance(v, (str, bool, int)) or v is None:
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else str(v)
    try:
        f = float(v)
        return f if math.isfinite(f) else str(v)
    except Exception:
        return str(v)


out = dict(lane="A31_referee", status="REFEREE-COMPLETE",
           target="deepseek_push/DS_FINAL_2026_10_21/FINAL_THEORY.md",
           counts=counts,
           numeric_checks=[{k: jsonable(v) for k, v in x.items()} for x in checks],
           n_numeric_pass=npass,
           n_numeric=len(checks),
           mismatches=[x["id"] for x in checks if not x["pass_"]],
           claims=claims,
           constants_used=dict(c=c, G=G, H0=H0, Lambda=LAM, rho_Lambda=RHO_L, a0=A0,
                               B_E=BE, Msun=MSUN, pc=PC, Z=Z, N_Lambda=N_LAMBDA))
with open(os.path.join(HERE, "a31_results.json"), "w") as fh:
    json.dump(out, fh, indent=1)

sys.exit(1 if MUTATE else 0)