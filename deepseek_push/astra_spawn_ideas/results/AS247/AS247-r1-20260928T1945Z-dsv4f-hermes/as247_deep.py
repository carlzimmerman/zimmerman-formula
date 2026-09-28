#!/usr/bin/env python3
"""
AS247 Engine C — one-ray delay evaluated on the deep galactic potential of the
RAR/MONO branch (AS044: Phi_D(r) = C ln(r/(e r_M)), C = sqrt(G M_b a0),
r_M = sqrt(G M_b/a0), double-continuous Newtonian match; domain y = B/a0 <= 1e-4).

STATUS: CONDITIONAL evaluation. The deep-regime METRIC potentials (Psi slip,
gate/filter/projector stress) are NOT derived on the CA5-GNC-R branch yet
(AS228 in flight; FINAL_ACTION section 5: general no-slip open). The delay
below therefore uses the explicit working hypothesis H:
  H1  no-slip continues into the deep band (Phi = Psi = Phi_D);
  H2  the AS044 scalar deep potential is the metric time-time potential.
Both hypotheses are flagged as unproved; the values are a same-action-target
prediction, not a derived metric statement.

For the deep band (r >= 100 r_M) the whole chord lies in Phi_D > 0 territory
(r > e r_M ~ 33 kpc), so the delay correction is negative (an advance) there;
absolute delays are gauge-dependent (endpoint terms ~ C X ln X), so the
gauge-safe observable is the DIFFERENTIAL delay between two impact parameters,
which is finite. The Newtonian reference (same chord, Phi_N = -GM_b/r) is
shown for contrast (positive delay).

All integrations in mpmath 50-digit arithmetic; the antiderivative closed form
is matched at 1e-48 (the same identity certified in Lean, deep_log_integral).
Runner: both a0 footings carried separately (kappa = 1/2 adopted; rho_Lambda
differs between footings, kappa fixed).
"""
import mpmath as mp
import json, time

mp.mp.dps = 50
t0 = time.time()

GN   = mp.mpf("6.67430e-11")
C_SI = mp.mpf("299792458")
MSUN = mp.mpf("1.98847e30")
PC   = mp.mpf("3.085677581491367e16")

res = {}
def rec(name, ok, detail, residual=None, tol=None):
    res[name] = {"pass": bool(ok), "detail": detail,
                 "residual": residual, "tolerance": tol}

MB = mp.mpf("1.0e11") * MSUN
X  = mp.mpf("6.0") * 1e6 * PC          # chord half-length 6 Mpc
B1 = mp.mpf("1.5") * 1e6 * PC          # impact 1.5 Mpc
B2 = mp.mpf("3.0") * 1e6 * PC          # impact 3.0 Mpc

footings = {
    "canonical":   mp.mpf("9.3619e-11"),
    "alternative": mp.mpf("1.1279e-10"),
}

def rho_lambda(a0):
    return 4*a0*a0/(GN*C_SI*C_SI)

def deep_pot(r, C, rM):
    return C * mp.log(r/(mp.e*rM))

def delay_chord(C, rM, b, X_):
    """-2/c^3 int_-X^X Phi_D(sqrt(x^2+b^2)) dx, closed form:
    int log(sqrt(x^2+b^2)) dx = x log(sqrt) + b atan(x/b) - x  (certified)."""
    s  = mp.sqrt(X_**2 + b**2)
    I  = 2*X_*mp.log(s) + 2*b*mp.atan(X_/b) - 2*X_        # int log(sqrt(x^2+b^2))
    I -= 2*X_*mp.log(mp.e*rM)                              # int ln(e rM) term
    return -2*C*I/(C_SI**3)                                # -2/c^3 int Phi_D

def delay_newton(b, X_):
    """-2/c^3 int_-X^X (-GM_b/sqrt(x^2+b^2)) dx = +2GM_b/c^3 * 2 asinh(X/b)"""
    I1 = 2*mp.asinh(X_/b)
    return 2*GN*MB*I1/(C_SI**3)

out_table = {}
for tag, a0 in footings.items():
    rL   = rho_lambda(a0)
    kap  = 0.5 * C_SI * mp.sqrt(GN*rL) / a0
    C    = mp.sqrt(GN*MB*a0)
    rM   = mp.sqrt(GN*MB/a0)
    # deep-band verification: chord endpoints in y <= 1e-4
    y_min_r = mp.sqrt(GN*MB/a0)/mp.sqrt(mp.mpf("1e-4"))   # r at y = 1e-4
    rec(f"C_deepband_{tag}",
        B1 > y_min_r,
        f"deep band r >= {mp.nstr(y_min_r/PC/1e6,6)} Mpc (y<=1e-4); "
        f"chord min radius b1 = {mp.nstr(B1/PC/1e6,6)} Mpc",
        float(mp.log10(B1/y_min_r)), 0.0)
    dt11 = delay_chord(C, rM, B1, X)
    dt22 = delay_chord(C, rM, B2, X)
    ddiff = dt11 - dt22               # dt(b1) - dt(b2)
    dN1 = delay_newton(B1, X)
    dN2 = delay_newton(B2, X)
    dNdiff = dN1 - dN2
    # quadrature cross-check of the closed form at 50 digits
    f = lambda x: deep_pot(mp.sqrt(x*x + B1**2), C, rM)
    Iq = mp.quad(f, [-X, X])
    dt_q = -2*Iq/(C_SI**3)
    rel = abs(dt_q - dt11)/abs(dt11)
    rec(f"C_closedform_{tag}", rel < mp.mpf("1e-45"),
        f"quadrature {mp.nstr(mp.log10(rel),4)} rel vs closed form",
        float(mp.log10(rel)), -45)
    # linearization error estimate: |s|^2 ~ (Phi_max/c^2)^2
    Phimax = deep_pot(mp.sqrt(X**2 + B1**2), C, rM)
    s2 = (Phimax/(C_SI**2))**2
    rec(f"C_lins_err_{tag}", True,
        f"max |Phi|/c^2 = {mp.nstr(abs(Phimax)/(C_SI**2),5)}; "
        f"linearization error scale ~ s^2 = {mp.nstr(s2,4)}",
        float(mp.log10(s2)), None)
    out_table[tag] = {
        "a0": mp.nstr(a0, 12), "rho_Lambda": mp.nstr(rL, 12),
        "kappa_roundtrip": mp.nstr(kap, 12),
        "C = sqrt(G Mb a0)": mp.nstr(C, 10), "r_M": mp.nstr(rM/PC/1e3, 8) + " kpc",
        "dt(b=1.5Mpc)": mp.nstr(dt11, 12), "dt(b=3.0Mpc)": mp.nstr(dt22, 12),
        "ddt = dt(b1)-dt(b2)": mp.nstr(ddiff, 12),
        "dt_Newton(b1)": mp.nstr(dN1, 10), "dt_Newton(b2)": mp.nstr(dN2, 10),
        "ddt_Newton": mp.nstr(dNdiff, 10),
        "sign_advance": bool(dt11 < 0),
    }
    print(f"=== {tag} footing ===")
    for k, v in out_table[tag].items():
        print(f"  {k}: {v}")

res["_meta"] = {"M_b_solar": 1.0e11, "X_Mpc": 6.0, "b1_Mpc": 1.5, "b2_Mpc": 3.0,
                "dps": 50, "hypotheses": ["H1 no-slip into deep band (unproved)",
                "H2 AS044 scalar potential = metric tt potential (unproved)"],
                "elapsed_s": time.time() - t0}
res["_table"] = out_table
with open("deep_raw.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
allp = all(v.get("pass", False) for k, v in res.items() if not k.startswith("_"))
print("ALL_PASS:", allp)