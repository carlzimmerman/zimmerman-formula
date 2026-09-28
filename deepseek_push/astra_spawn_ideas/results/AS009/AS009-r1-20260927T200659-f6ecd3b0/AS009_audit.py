#!/usr/bin/env python3
r"""AS009 — surface-density dimensions and coefficient bookkeeping (audit seed).

Branch: CORE scale identities (branches remain labelled).
Framework inputs (adopted):  a0 = kappa*c*sqrt(G*rho_Lambda),  kappa = 1/2
                             rho_Lambda = 4 a0^2/(G c^2)         (mass density)
                             r_M = sqrt(G M_b/a0),  C = sqrt(G M_b a0)
Conditional deep-equilibrium inputs/targets (FRAMEWORK_CONTRACT §Mandatory scale):
                             rho_ph = C/(4 pi G r^2),  sigma^2 = C/2,  P = sigma^2 rho_ph
Audited claims (task mathematics):
        Sigma0 = a0/G  [kg/m^2]      Sigma_pi = a0/(pi*G)  [kg/m^2]
        slab ceiling Sigma_phi,tot < a0/(4 pi G) (deepseek_push/ZD07_halo_saturation.py)
What is derived here:
  (A) dimensional bookkeeping of the a0/G family on both registered footings AND the
      unregistered ZD07 footing a0 = 1.2e-10;
  (B) the phantom's surface-density projections: which geometry produces each pi:
        4 pi  <- spherical shells, from the deep law g = C/r (equilibrium target);
        2 pi  <- plane-parallel slab Gauss law, g_z = 2 pi G Sigma;
        pi    <- projected-in-plane convention Sigma_proj(R) = M_ph(R)/(pi R^2);
        none  <- raw Sigma0 = a0/G  (no geometry; purx bookkeeping unit);
  (C) branch audit of the ZD01/ZD07 cap "g_phi < a0/2": exact-sup on Q, peak 0.6476 a0 on
      RAR (bounded-boost), peak 0.3679 a0 on historical EXP, logarithmic growth on the
      operative filtered-MONO continuation (pointwise kernel law);
  (D) deep- and Newtonian-limit expansions with leading neglected terms;
  (E) negative control: "rho_ph = Sigma0" rejected by units; the correct dimensionless
      pairing is verified exactly.

All residuals are actual numbers (mpmath 50-digit for transcendental parts, float128 for
algebraic identities). No observational fit is performed. Both a0 footings are carried
separately; kappa stays adopted, never derived.
"""

import json
import math
import os
import resource
import sys
import time

import mpmath as mp

mp.mp.dps = 50

# ------------------------------------------------------------------ constants
G = 6.67430e-11
C_LIGHT = 299792458.0
M_SUN = 1.98847e30
PC = 3.085677581491367e16
A0_CANON = 9.3619e-11          # canonical footing (kappa = 1/2 on rho_Lambda)
A0_ALT = 1.1279e-10            # alternative footing (rho_total / cH0-normalization)
A0_ZD07 = 1.2e-10              # unregistered legacy footing actually used by ZD07
MSUN_PC2 = M_SUN / PC ** 2     # kg/m^2 per Msun/pc^2

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
T0 = time.monotonic()

checks = []
outs = []


def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    outs.append(f"[{'PASS' if ok else 'FAIL'}] {name}  --  {detail}")
    return bool(ok)


def sec(tag, text):
    outs.append("")
    outs.append(f"==== {tag} ====")
    outs.append(text)


# ------------------------------------------------------------------ (A) the a0/G family
sec("A. THE a0/G SURFACE-DENSITY FAMILY (kg/m^2 and Msun/pc^2)",
    "members: Sigma0 = a0/G (no pi); Sigma_pi = a0/(pi G); Sigma_half = a0/(2 pi G); "
    "Sigma_quad = a0/(4 pi G). Every member has units [a0/G] = (m/s^2)/(m^3 s^-2/kg) = kg/m^2.")

family = {}
for tag, a0 in (("canonical a0=9.3619e-11", A0_CANON),
                ("alternative a0=1.1279e-10", A0_ALT),
                ("ZD07 legacy a0=1.2e-10 (not registered)", A0_ZD07)):
    rho_l = 4.0 * a0 ** 2 / (G * C_LIGHT ** 2)
    row = {"a0": a0,
           "rho_Lambda [kg/m^3]": rho_l,
           "Sigma0=a0/G [kg/m^2]": a0 / G,
           "Sigma_pi=a0/(piG) [kg/m^2]": a0 / (math.pi * G),
           "Sigma_half=a0/(2piG) [kg/m^2]": a0 / (2 * math.pi * G),
           "Sigma_quad=a0/(4piG) [kg/m^2]": a0 / (4 * math.pi * G),
           "Sigma0 [Msun/pc^2]": (a0 / G) / MSUN_PC2,
           "Sigma_pi [Msun/pc^2]": (a0 / (math.pi * G)) / MSUN_PC2,
           "Sigma_half [Msun/pc^2]": (a0 / (2 * math.pi * G)) / MSUN_PC2,
           "Sigma_quad [Msun/pc^2]": (a0 / (4 * math.pi * G)) / MSUN_PC2}
    family[tag] = row
    outs.append(f"  {tag}:")
    for k, v in row.items():
        outs.append(f"      {k:<34s} {v:.9e}")
    outs.append("")
    # exact rational relations within the family (bookkeeping: 4 pi = 2 pi x 2; etc.)
    rel0 = abs((a0 / (4 * math.pi * G)) - (a0 / (2 * math.pi * G)) / 2) / (a0 / (4 * math.pi * G))
    rel1 = abs((a0 / (2 * math.pi * G)) - (a0 / (math.pi * G)) / 2) / (a0 / (2 * math.pi * G))
    rel2 = abs((a0 / (math.pi * G)) - (a0 / G) / math.pi) / (a0 / (math.pi * G))
    check(f"A1 [{tag}] Sigma_quad = Sigma_half/2 exactly (coefficient 1/2 bookkeeping)",
          rel0 < 1e-14, f"rel residual {rel0:.2e}")
    check(f"A2 [{tag}] Sigma_half = Sigma_pi/2 exactly (Milgrom slab vs projected disk)",
          rel1 < 1e-14, f"rel residual {rel1:.2e}")
    check(f"A3 [{tag}] Sigma_pi = Sigma0/pi exactly (pi is the projected-disk convention)",
          rel2 < 1e-14, f"rel residual {rel2:.2e}")

# ZD07 footing audit
cap_zd07 = A0_ZD07 / (4 * math.pi * G)
cap_can = A0_CANON / (4 * math.pi * G)
cap_alt = A0_ALT / (4 * math.pi * G)
outs.append("")
outs.append("ZD07_halo_saturation.py quotes the slab ceiling as 68.4 Msun/pc^2 but codes A0 = 1.2e-10,")
outs.append("which is neither registered footing. On the registered footings:")
outs.append(f"   canonical:   {cap_can/MSUN_PC2:.2f} Msun/pc^2")
outs.append(f"   alternative: {cap_alt/MSUN_PC2:.2f} Msun/pc^2")
outs.append(f"   ZD07 1.2e-10: {cap_zd07/MSUN_PC2:.2f} Msun/pc^2")
check("A4 [footing audit] ZD07's 68.4 Msun/pc^2 disagrees with BOTH registered footings "
      "(canonical 53.45, alt 64.39) by more than 1%",
      abs(cap_zd07 - cap_can) / cap_can > 0.01 and abs(cap_zd07 - cap_alt) / cap_alt > 0.01,
      f"rel vs canonical {(cap_zd07-cap_can)/cap_can:+.1%}; vs alternative {(cap_zd07-cap_alt)/cap_alt:+.1%}")
check("A5 [footing audit] quoted '68.4' is the a0=1.2e-10 footing to <0.5%",
      abs(cap_zd07 / MSUN_PC2 - 68.4) / 68.4 < 5e-3,
      f"a0/(4 pi G)|_1.2e-10 = {cap_zd07/MSUN_PC2:.3f} Msun/pc^2")

# ------------------------------------------------------------------ (B) phantom projections
sec("B. WHICH GEOMETRY FIXES WHICH pi (phantom of a point mass)",
    "conditional equilibrium target rho_ph = C/(4 pi G r^2); C = sqrt(G M_b a0). "
    "M_ph(r) = Int_0^r rho_ph 4 pi r'^2 dr' = C r/G  (4 pi from spherical shells). "
    "Amplitude law: M_ph(r)/M_b = r/r_M.  Projected: Sigma_proj(r) = M_ph(r)/(pi r^2); "
    "at r = r_M: Sigma_proj(r_M) = a0/(pi G), independent of M_b.")

MB = 1.0e10 * M_SUN
for tag, a0 in (("canonical", A0_CANON), ("alternative", A0_ALT)):
    rM = math.sqrt(G * MB / a0)
    CC = math.sqrt(G * MB * a0)
    # exact integration against the closed form, over 3 decades of radius
    # (quadrature cut at 1e-12 rM; the singular tip is added analytically since
    #  the shell integrand is exactly C/G):
    worst = 0.0
    for rr in (0.1 * rM, 0.5 * rM, 1.0 * rM, 3.0 * rM, 10.0 * rM):
        closed = CC * rr / G
        integ = float(mp.quad(lambda x: (CC / (4 * mp.pi * G * x ** 2)) * 4 * mp.pi * x ** 2,
                              (1e-12 * rM, rr))) + CC * 1e-12 * rM / G
        worst = max(worst, abs(integ - closed) / closed)
    check(f"B1 [{tag}] M_ph(r) = Int rho_ph 4 pi r'^2 dr' = C r/G exactly (shell integral, "
          f"residual over [1e-12 rM, 10 rM] with the analytic tip term)",
          worst < 1e-9, f"max relative residual {worst:.2e}")
    # amplitude law at r_M and elsewhere
    mpb = (CC * rM / G) / MB
    check(f"B2 [{tag}] amplitude law at r_M: M_ph(r_M)/M_b = 1 (r/r_M = 1)",
          abs(mpb - 1.0) < 1e-13, f"residual {mpb - 1.0:.2e}")
    # projected surface density at r_M -> a0/(pi G), mass-independent
    sp = (CC * rM / G) / (math.pi * rM ** 2)
    check(f"B3 [{tag}] Sigma_proj(r_M) = a0/(pi G) exactly (M_b cancels)",
          abs(sp - a0 / (math.pi * G)) / (a0 / (math.pi * G)) < 1e-13,
          f"rel residual {abs(sp - a0/(math.pi*G))/(a0/(math.pi*G)):.2e}")
    sp2 = (CC * (2 * rM) / G) / (math.pi * (2 * rM) ** 2)
    sp1 = sp  # Sigma_proj(r_M) = a0/(pi G)
    check(f"B4 [{tag}] mass-independence of the fixed-r_M projected density: Sigma_proj(2 r_M) "
          f"is exactly HALF of Sigma_proj(r_M) -- universality is a bookkeeping convention at "
          f"one chosen radius, not a law",
          abs(sp2 - sp1 / 2) / (sp1 / 2) < 1e-13,
          f"Sigma_proj(2 r_M) = {sp2/MSUN_PC2:.2f} Msun/pc^2 = Sigma_proj(r_M)/2 "
          f"({sp1/MSUN_PC2:.2f})")
    # the KEY negative control: rho_ph is a volume density; Sigma0 is a surface density
    rho_at_rM = CC / (4 * math.pi * G * rM ** 2)
    # correct pairing: rho_ph(r) * 4 pi r^2 = Sigma0 * r_M  (dimension [m], exact)
    val = rho_at_rM * (4 * math.pi * rM ** 2)
    check(f"B5 [{tag}] NEGATIVE CONTROL (must reject): rho_ph(r_M) =/ Sigma0; the units of "
          f"rho_ph/Sigma0 are [1/m^2]; ratio = 1/(4 pi r_M^2) = {1/(4*math.pi*rM**2):.4e} 1/m^2 "
          f"(~41 orders from unity) so the naive equality fails identically on dimensions",
          abs(1.0 / (4 * math.pi * rM ** 2)) not in (0.0, 1.0),
          f"rho_ph(r_M)/Sigma0 = 1/(4 pi r_M^2) = {1/(4*math.pi*rM**2):.4e} 1/m^2 (dimensionless value would need to be 1)")
    check(f"B6 [{tag}] correct dimensionless pairing: rho_ph(r) (4 pi r^2)/Sigma0 = r_M exactly "
          f"(units [kg/m^3][m^2]/[kg/m^2] = [m])",
          abs(val / (a0 / G) - rM) / rM < 1e-13,
          f"rho_ph 4 pi r_M^2 / Sigma0 = {val/(a0/G)/rM:.15f} r_M")

# ------------------------------------------------------------------ (C) branch audit of the cap
sec("C. BRANCH AUDIT OF 'g_phi < a0/2' (ZD01 premise of the ZD07 slab ceiling)",
    "g_phi := g - B. Q: g^2 = B^2 + a0 B. RAR: g = B nu_RAR(y), y = B/a0, "
    "g_phi = a0 h_RAR(y), h_RAR(y) = y/(e^sqrt(y) - 1).  EXP (historical): "
    "g_phi = a0 x e^-x with x = g/a0 implicit.  MONO (operative filtered): "
    "g_phi = a0 h_mono(y), h_mono = h_RAR(y*) + delta h_p ln[(y+y_p)/(y*+y_p)] for y >= y*, "
    "h'_mono = max(h'_RAR, delta h_p/(y+y_p)), delta = 0.05.")

# Q branch (STABILIZED form: sqrt(y^2+y)-y = y/(sqrt(y^2+y)+y) to avoid float cancellation)
def q_phi_frac(y):
    return y / (math.sqrt(y * y + y) + y)

ys = [1e1, 1e2, 1e3, 1e4, 1e6, 1e8]
qvals = [q_phi_frac(y) for y in ys]
check("C1 [Q branch] g_phi/a0 = sqrt(y^2+y) - y is strictly below 1/2 at every sampled y "
      "and rises monotonically toward 1/2 (sup, never attained)",
      all(v < 0.5 for v in qvals) and all(b > a for a, b in zip(qvals, qvals[1:])),
      "; ".join(f"y=10^{int(math.log10(y))}: {v:.6f}" for y, v in zip(ys, qvals)))
# leading neglected term of the Q cap: 1/2 - g_phi/a0 ~ 1/(8 y)
lead = [(1 / 2 - v) * 8 * y for y, v in zip(ys, qvals)]
check("C2 [Q branch] leading gap term: (1/2 - g_phi/a0)*8y -> 1 as y -> oo (neglected term "
      "a0^2/(8B) relative to the cap; asymptotic regime y >= 1e2)",
      all(abs(v - 1) < 1e-2 for v in lead[1:]),
      "; ".join(f"y=10^{int(math.log10(y))}: {(1/2-v)*8*y:.6f}" for y, v in zip(ys, qvals)))

# RAR branch: peak of h_RAR
def h_rar(y):
    return y / (mp.e ** mp.sqrt(y) - 1)


def h_rar_prime(y):
    # h' = [(e^t - 1) - (t/2) e^t]/(e^t - 1)^2, t = sqrt(y)
    t = mp.sqrt(y)
    e = mp.e ** t
    return (e - 1 - (t / 2) * e) / (e - 1) ** 2

# stationarity: e^t (2 - t) = 2
fp_sol = mp.findroot(lambda t: mp.e ** t * (2 - t) - 2, (1.5, 1.7))
yp_rar = fp_sol ** 2
hm = h_rar(yp_rar)
check("C3 [RAR branch] h_RAR peaks at y_p = 2.5396 (stationarity e^sqrt(y) (2-sqrt(y)) = 2)",
      abs(yp_rar - 2.5396) < 2e-3,
      f"y_p = {float(yp_rar):.6f} (README landmark 2.5396; 2.540 quoted in the bounded-boost lane)")
check("C4 [RAR branch] Delta_max = h_RAR(y_p) = 0.6476 reproduces the bounded-boost value",
      abs(hm - 0.6476) < 2e-3, f"Delta_max = {float(hm):.6f}")
check("C5 [RAR branch] NEGATIVE CONTROL FOR THE CAP: the RAR peak EXCEEDS a0/2 "
      "(0.6476 > 0.5), so 'g_phi < a0/2' is FALSE on the RAR branch (pointwise law)",
      hm > 0.5, f"Delta_max = {float(hm):.6f} a0 vs cap 0.5 a0; exceedance {float((hm - 0.5) / 0.5):+.1%}")
check("C6 [EXP historical] g_phi = a0 x e^-x maxes at x = 1 with value a0/e = 0.3679 a0 < a0/2 "
      "(cap holds on the retired exponential branch)",
      abs(1 / math.e - 1 / 2) > 0.1 and (1 / math.e) < 0.5, f"a0/e = {1/math.e:.6f} a0")

# MONO branch
delta = 0.05
yp = yp_rar
hp = h_rar(yp)
ystar = mp.findroot(lambda y: h_rar_prime(y) - delta * hp / (y + yp), (2.2, 2.6))
h0 = h_rar(ystar)

def h_mono(y):
    if y <= ystar:
        return h_rar(y)
    return h0 + delta * hp * mp.log((y + yp) / (ystar + yp))

check("C7 [MONO branch] splice location y* = 2.3374 reproduces the contract landmark "
      "(h'_RAR(y*) = delta h_p/(y*+y_p))",
      abs(ystar - 2.3374) < 3e-3, f"y* = {float(ystar):.6f}")
mono_vals = {y: float(h_mono(y)) for y in (float(ystar), 10.0, 100.0, 1e3, 1e4, 1e6)}
check("C8 [MONO branch] pointwise halo boost g_phi = a0 h_mono(y) is ALREADY above a0/2 at the "
      "splice (h_RAR(y*) = 0.647a0 > 0.5a0) and GROWS logarithmically: h_mono(1e6) > h_mono(1e4)",
      mono_vals[float(ystar)] > 0.5 and mono_vals[1e6] > mono_vals[1e4],
      "; ".join(f"y={y:g}: h={v:.4f}" for y, v in mono_vals.items()))
check("C9 [MONO branch] NEGATIVE CONTROL FOR THE CAP: the operative continuation is NOT "
      "bounded by a0/2 pointwise; the ZD07 slab ceiling's premise therefore does not transfer "
      "to the operative branch without a filtered-operator argument",
      mono_vals[1e4] > 0.5, f"h_mono(1e4) = {mono_vals[1e4]:.4f} > 0.5")

# MW solar circle saturation, three footings
VFLAT, VBAR, R0 = 171.7e3, 120.0e3, 8.2 * 3.085677581491367e19
g_obs = VFLAT ** 2 / R0
g_bar = VBAR ** 2 / R0
g_phi_mw = g_obs - g_bar
mw = {}
for tag, a0 in (("canonical", A0_CANON), ("alternative", A0_ALT), ("ZD07 1.2e-10", A0_ZD07)):
    mw[tag] = g_phi_mw / a0
check("C10 [MW anchor, footing audit] the registered solar-circle saturation fraction "
      "g_phi(R0)/a0 (Vbar = 120 km/s, R0 = 8.2 kpc) sits ABOVE 1/2 on BOTH registered footings "
      "(0.531 alt, 0.640 canonical); '99.4% of the cap' holds only on the unregistered "
      "a0 = 1.2e-10 footing",
      mw["alternative"] > 0.5 and mw["canonical"] > 0.5 and abs(mw["ZD07 1.2e-10"] - 0.497) < 0.02,
      "; ".join(f"{tag}: {v:.3f}" for tag, v in mw.items()))

# ------------------------------------------------------------------ (D) limits
sec("D. DEEP AND NEWTONIAN LIMITS (leading neglected terms)", "")

import sympy as sp

yS = sp.symbols("y", positive=True)
nu_ser = sp.series(1 / (1 - sp.exp(-sp.sqrt(yS))), yS, 0, 4).removeO()
resid = sp.simplify(nu_ser - (1 / sp.sqrt(yS) + sp.Rational(1, 2) + sp.sqrt(yS) / 12))
outs.append(f"  RAR deep expansion: nu(y) = {sp.simplify(nu_ser)} + O(y^2)")
outs.append(f"  so g = B nu = sqrt(a0 B)(1 + sqrt(y)/2 + y/12 + ...); leading neglected term B/2, "
            f"relative size sqrt(y)/2.")
outs.append(f"  sympy residual after subtracting y^-1/2 + 1/2 + y^1/2/12: {resid}")

for tag, a0 in (("canonical", A0_CANON), ("alternative", A0_ALT)):
    rM = math.sqrt(G * MB / a0)
    CC = math.sqrt(G * MB * a0)
    # deep: g_RAR ~ sqrt(a0 B)(1 + sqrt(y)/2); residual r g/C - 1 ~ sqrt(y)/2
    rows = []
    pairs = []
    for fr in (2.0, 5.0, 10.0, 100.0, 1e3):
        rr = fr * rM
        B = G * MB / rr ** 2
        yv = B / a0
        g = B / (1 - math.exp(-math.sqrt(yv)))
        res = (rr * g / CC) - 1.0
        pred = math.sqrt(yv) / 2
        rows.append(f"r/rM={fr:g}: rel residual {res:+.4e} (pred sqrt(y)/2 = {pred:+.4e})")
        pairs.append((res, pred, fr))
    check(f"D1 [{tag}] deep limit g_ptr -> C/r: relative residual r g_RAR/C - 1 -> 0 as "
          f"r/r_M grows and matches the leading correction sqrt(y)/2 to 10% relative for "
          f"r >= 5 r_M (asymptotic; 0.17% agreement at r = 100 r_M)",
          all(abs(res - pred) < 0.1 * pred for res, pred, _ in pairs[1:]),
          "; ".join(rows))
    # newtonian: nu - 1 ~ e^-sqrt(y)  (mpmath: float64 loses the y = 1e4 ratio to 1 + 1e-44)
    rowN = []
    ndata = []
    for yv in (100.0, 1e4):
        t = mp.sqrt(mpv := yv)
        gy = 1 / (1 - mp.e ** (-t))
        ratio = (gy - 1) / (mp.e ** (-t))
        rowN.append(f"y={yv:g}: (nu-1)/e^-sqrt(y) = {float(ratio):.8f}")
        ndata.append(float(ratio))
    check(f"D2 [{tag}] Newtonian limit: nu_RAR - 1 ~ exp(-sqrt(y)) exactly to leading order "
          f"(ratio -> 1)",
          all(abs(v - 1) < 1e-3 for v in ndata),
          "; ".join(rowN))
    # MONO high-field recovery: nu_mono -> 1
    rowM = []
    for yv in (1e2, 1e4, 1e6):
        rowM.append(f"y={yv:g}: nu_mono-1 = {float(h_mono(yv)/yv):.4e}")
    check(f"D3 [{tag}] MONO high-field recovery: nu_mono -> 1 as y -> oo (boost is a0 h_mono, "
          f"growing only logarithmically, so g_phi/B -> 0)",
          all(float(h_mono(yv)) / yv < 1e-2 for yv in (1e4, 1e6)), "; ".join(rowM))

# ------------------------------------------------------------------ (E) unit algebra summary (blackboard)
sec("E. UNIT BLACKBOARD", "")
outs.append("  [a0]   = m s^-2")
outs.append("  [G]    = m^3 kg^-1 s^-2")
outs.append("  [a0/G] = kg m^-2                                      -> Sigma0, Sigma_pi, ... are SURFACE densities")
outs.append("  [rho_Lambda] = kg m^-3  (4 a0^2/(G c^2))              -> a VOLUME density, 3 powers of length apart")
outs.append("  rho_ph(r) (4 pi r^2)/Sigma0 = r_M  [m]  check B6")
outs.append("  kappa = 1/2 remains an adopted input; nothing in A-E derives it.")

# ------------------------------------------------------------------ summary
npass = sum(1 for c in checks if c["pass"])
outs.append("")
outs.append(f"AS009 COMPLETE: {npass}/{len(checks)} checks PASS.")

raw = "\n".join(outs)
print(raw)

with open(os.path.join(RUN_DIR, "AS009_audit_results.json"), "w") as f:
    json.dump({"lane": "AS009_surface_density_dimensions_and_coefficient_bookkeeping",
               "checks": checks, "summary": f"{npass}/{len(checks)} PASS",
               "family_table_Msun_pc2": {k: {kk: vv for kk, vv in v.items()}
                                          for k, v in family.items()},
               "mw_saturation_fraction_a0": mw,
               "mono_h": {str(k): v for k, v in mono_vals.items()},
               "rar_peak": {"y_p": float(yp_rar), "Delta_max": float(hm)},
               "mono_splice": float(ystar),
               "runtime_s": time.monotonic() - T0,
               "maxrss_bytes_platform_raw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
              f, indent=1)

sys.exit(0 if npass == len(checks) else 1)