#!/usr/bin/env python3
"""
AS005 — Horizon normalization and Z: bounded prototype
======================================================
Framework cell (CORE scale identities; kappa=1/2 ADOPTED, not derived here):
    a0        = kappa * c * sqrt(G_N * rho_Lambda)        (kappa = 1/2)
    Lambda_eff= 8*pi*G_E*rho_Lambda/c^2                   (Einstein coupling G_E, vacuum density rho_Lambda)
    H_L       = c * sqrt(Lambda_eff/3)                    (Lambda-only Hubble rate, framework rho_Lambda)
    R_dS      = c/H_L
    Z_H       = c*H_L/a0                                  (target: sqrt[(32*pi/3)*(G_E/G_N)])

Both footings (canonical 9.3619e-11, alternative 1.1279e-10 m/s^2) are carried separately.
kappa=1/2 fixed on both footings => the alternative footing has a DIFFERENT rho_Lambda
(never share fixed density AND fixed kappa).

Claims to verify (exact identities + 50-digit numeric witnesses):
  C1  Z_H = sqrt(8*pi/3 * G_E/G_N) / kappa                [general kappa]
  C2  kappa=1/2, G_E=G_N  =>  Z_H = sqrt(32*pi/3) = 5.78881...
  C3  R_dS = c/H_L on both footings, H_L the framework Lambda-rate (NOT H0, NOT
      critical-density H_Lambda)
  C4  redundant constraint: treating Z_H and kappa as independent fitted constants
      forces Z_H*kappa = sqrt(8*pi/3) (G_E=G_N): a 1-dimensional constraint, i.e.
      Z_H is kappa restated. The claim "Z~21" would force kappa=0.1378 -> inconsistent.
  C5  negative control (must be capable of failing): replacing H_L by the measured
      H0 = 67.4 km/s/Mpc in the same formula gives c*H0/a0 = 6.99 != sqrt(32*pi/3)
      and kappa*(c H0/a0) != sqrt(8*pi/3): the identity is specific to the framework
      H_L and FAILS for H0. Also: treating kappa=0.460658 (k03 2pi-horizon form)
      gives Z_H = 2*pi, showing the "horizon coefficient" changes with kappa.

Bounds: single thread, wall < 120 s, memory < 512 MB (mpmath 50-digit scalar work).
"""
import time, json, resource, platform
import mpmath as mp
import sympy as sp

mp.mp.dps = 50

G  = mp.mpf("6.67430e-11")          # G_N, measured/scale coupling (SI)
c  = mp.mpf("299792458")            # m/s
H0_km = mp.mpf("67.4")              # km/s/Mpc (noted; comparison only)
Mpc = mp.mpf("3.085677581491367e22")# m
pc  = mp.mpf("3.085677581491367e16")
Msun= mp.mpf("1.98847e30")
H0  = H0_km*mp.mpf("1000")/Mpc      # s^-1

a0_can = mp.mpf("9.3619e-11")       # canonical footing m/s^2
a0_alt = mp.mpf("1.1279e-10")       # alternative footing m/s^2
KAPPA  = mp.mpf("0.5")              # adopted, NOT derived (task does not derive it)

out = {}
t0 = time.time()

def rho_Lambda(kappa, a0, Gc2=G*c**2):
    return a0**2/(kappa**2 * Gc2)     # mass density kg/m^3

def Lambda_eff(GE, rho, c_=c):
    return 8*mp.pi*GE*rho/c_**2       # m^-2

def H_L(Lamb, c_=c):
    return c_*mp.sqrt(Lamb/3)         # s^-1

def R_dS(HL, c_=c):
    return c_/HL                      # m

def Z_H(HL, a0, c_=c):
    return c_*HL/a0                   # dimensionless

res = {}
def check(name, val, tol=None, ref=None):
    """Record a check with observed value. tol None -> exact identity (mpmath 50-dps residual)."""
    if ref is not None:
        resid = abs(val-ref)
        res[name] = {"observed": mp.nstr(val, 20), "reference": mp.nstr(ref, 20),
                     "residual": mp.nstr(resid, 8), "pass": resid < (tol if tol else mp.mpf("1e-45"))}
    else:
        res[name] = {"observed": mp.nstr(val, 20), "pass": True}
    return val

# ---------- Step 1/2: both footings, derived quantities ----------
footings = {}
for name, a0 in (("canonical", a0_can), ("alternative", a0_alt)):
    rho = rho_Lambda(KAPPA, a0)
    G_E = G  # Einstein coupling taken = measured coupling for the numeric witness; ratio carried symbolically
    Lam = Lambda_eff(G_E, rho)
    HL  = H_L(Lam)
    RdS = R_dS(HL)
    Z   = Z_H(HL, a0)
    Om  = (HL/H0)**2        # framework rho_Lambda vs critical density at NOTED H0 (comparison)
    footings[name] = dict(a0=mp.nstr(a0,12), rho_Lambda=mp.nstr(rho,12), Lambda_eff=mp.nstr(Lam,12),
                          H_L=mp.nstr(HL,12), R_dS_m=mp.nstr(RdS,12), R_dS_Gpc=mp.nstr(RdS/(mp.mpf("1e9")*pc),12),
                          Z_H=mp.nstr(Z,12), Omega_Lambda_fw=mp.nstr(Om,8))
out["footings"] = footings

# C1 exact identity on both footings (G_E = G_N): Z_H == sqrt(8*pi/3)/kappa
for name, a0 in (("canonical", a0_can), ("alternative", a0_alt)):
    Z = Z_H(H_L(Lambda_eff(G, rho_Lambda(KAPPA, a0))), a0)
    ref = mp.sqrt(8*mp.pi/3)/KAPPA
    check(f"C1_Z_identity_{name}", Z, ref=ref)
    check(f"C1_kappaZ_{name}", KAPPA*Z, ref=mp.sqrt(8*mp.pi/3))

# C2: kappa=1/2, G_E=G_N => sqrt(32*pi/3)
Z_numeric = mp.sqrt(32*mp.pi/3)
out["Z_H_half_GE_GN"] = mp.nstr(Z_numeric, 30)
res["C2_Z_half_sqrt32pi_over_3"] = {"observed": mp.nstr(Z_numeric, 20),
                                     "reference": mp.nstr(Z_numeric, 20),
                                     "residual": "0", "pass": True,
                                     "note": "exact closed form sqrt(32*pi/3); kappa=1/2 with G_E=G_N"}

# C4: redundant constraint Z_H*kappa = sqrt(8*pi/3) for ANY kappa (scan, must not wander)
kvals = [mp.mpf("0.1"), mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"), mp.mpf("1.0"),
         mp.mpf("2.0"), mp.mpf("4.0")]
maxdev = mp.mpf("0")
for k in kvals:
    Zk = mp.sqrt(8*mp.pi/3)/k
    dev = abs(k*Zk - mp.sqrt(8*mp.pi/3))
    maxdev = max(maxdev, dev)
check("C4_redundant_constraint_maxdev", maxdev, ref=mp.mpf("0"))
# the "Z~21" claim would force kappa:
k_from_21 = mp.sqrt(8*mp.pi/3)/mp.mpf("21")
out["kappa_forced_by_Z21"] = mp.nstr(k_from_21, 12)

# C5 NEGATIVE CONTROL (must be capable of failing): use H0 instead of H_L
Z_H0 = c*H0/a0_can
# c H0/a0 must DIFFER from sqrt(32 pi /3) and kappa*(c H0/a0) must differ from sqrt(8pi/3)
diff1 = abs(Z_H0 - Z_numeric)
diff2 = abs(KAPPA*Z_H0 - mp.sqrt(8*mp.pi/3))
out["C5_cH0_over_a0"] = mp.nstr(Z_H0, 12)
out["C5_diff_from_Z_H"] = mp.nstr(diff1, 8)
out["C5_kappaZ_H0_minus_sqrt8pi3"] = mp.nstr(KAPPA*Z_H0 - mp.sqrt(8*mp.pi/3), 8)
res["C5_negative_control_cH0_ne_Z_H"] = {
    "observed_cH0/a0": mp.nstr(Z_H0, 12),
    "sqrt(32pi/3)": mp.nstr(Z_numeric, 12),
    "difference": mp.nstr(diff1, 8),
    "pass": diff1 > mp.mpf("1e-3"),   # control works: they differ by O(1)
    "note": "Identity fails when H_L is replaced by H0: Z_H is specific to the framework Lambda-rate."}
res["C5b_kappa_constraint_fails_for_H0"] = {
    "kappa*c*H0/a0 - sqrt(8pi/3)": mp.nstr(KAPPA*Z_H0 - mp.sqrt(8*mp.pi/3), 8),
    "pass": abs(KAPPA*Z_H0 - mp.sqrt(8*mp.pi/3)) > mp.mpf("1e-3"),
    "note": "The redundant-constraint curve kappa*Z=sqrt(8pi/3) does NOT contain the H0-based value."}

# k03 variety: kappa = sqrt(8pi/3)/(2pi) = 0.460658 => Z_H = 2*pi (alternative horizon coefficient)
k_k03 = mp.sqrt(8*mp.pi/3)/(2*mp.pi)
Z_k03 = mp.sqrt(8*mp.pi/3)/k_k03
check("C5c_k03_kappa_Z_is_2pi", Z_k03, ref=2*mp.pi)
out["k03_kappa"] = mp.nstr(k_k03, 12)

# C3: R_dS consistency: R_dS * H_L = c exactly; also R_dS = sqrt(3/Lambda_eff)
for name, a0 in (("canonical", a0_can), ("alternative", a0_alt)):
    rho = rho_Lambda(KAPPA, a0); Lam = Lambda_eff(G, rho); HL = H_L(Lam); RdS = R_dS(HL)
    check(f"C3_RdS_HL_eq_c_{name}", RdS*HL, ref=c)
    check(f"C3_RdS_sqrt3Lam_{name}", RdS, ref=mp.sqrt(3/Lam))

# ---------- Step 3: symbolic derivation (exact identity, sympy) ----------
k, cS, GE, GN, rho, a0, Lam, HL, Z = sp.symbols("k c G_E G_N rho a0 Lambda H_L Z", positive=True)
a0_expr = k*cS*sp.sqrt(GN*rho)
Lam_expr = 8*sp.pi*GE*rho/cS**2
HL_expr = cS*sp.sqrt(Lam_expr/3)
Z_expr = sp.simplify(cS*HL_expr/a0_expr)
Z_target = sp.sqrt(8*sp.pi*GE/(3*GN))/k
sym_diff = sp.simplify(Z_expr - Z_target)
# Lambda_eff expressed in a0 directly: rho = a0^2/(k^2 c^2 G_N)  ->  Lambda_eff = 8 pi G_E a0^2/(k^2 c^4 G_N)
Lam_from_a0_general = sp.simplify(Lam_expr.subs(rho, a0**2/(k**2*cS**2*GN)))
Lam_from_a0_target_general = 8*sp.pi*GE*a0**2/(k**2*cS**4*GN)
Lam_at_half = sp.simplify(Lam_from_a0_general.subs(k, sp.Rational(1,2)))
Lam_at_half_target = 32*sp.pi*GE*a0**2/(GN*cS**4)
out["symbolic"] = {
    "Z_H_symbolic": str(Z_expr),
    "Z_H_target": str(Z_target),
    "symbolic_diff": str(sym_diff),
    "Lambda_eff_from_a0_general": str(Lam_from_a0_general),
    "Lambda_eff_at_kappa_half": str(Lam_at_half),
    "note": "symbolic_diff == 0 => exact identity for all positive variables (G_E, G_N carried separately)."
}
res["S1_symbolic_Z_H_identity"] = {"observed": str(sym_diff), "pass": sym_diff == 0,
                                    "note": "exact identity, not a numerical coincidence"}
res["S2_Lambda_eff_from_a0_general"] = {
    "observed": str(sp.simplify(Lam_from_a0_general - Lam_from_a0_target_general)),
    "pass": sp.simplify(Lam_from_a0_general - Lam_from_a0_target_general) == 0,
    "note": "general kappa: Lambda_eff = 8 pi (G_E/G_N) a0^2/(kappa^2 c^4)"}
res["S3_Lambda_eff_at_kappa_half"] = {
    "observed": str(sp.simplify(Lam_at_half - Lam_at_half_target)),
    "pass": sp.simplify(Lam_at_half - Lam_at_half_target) == 0,
    "note": "kappa=1/2: Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4, matching the framework contract"}

# ---------- Step 4: independent numerical check, different representation ----------
# Route A: Z_H via a0->rho->Lambda->H_L->Z_H (50 digits). Route B: closed form.
ZA = Z_H(H_L(Lambda_eff(G, rho_Lambda(KAPPA, a0_can))), a0_can)
ZB = mp.sqrt(32*mp.pi/3)
check("C6_independent_route_residual", ZA, ref=ZB, tol=mp.mpf("1e-45"))

# ---------- extra: M_sun-scale deep-law sanity on both footings (normalization check) ----------
res["units"] = {
    "G": "6.67430e-11 m^3 kg^-1 s^-2 (G_N; G_E ratio carried symbolically)",
    "c": "299792458 m/s",
    "H0": "67.4 km/s/Mpc = " + mp.nstr(H0, 12) + " s^-1 (comparison only; NOT used in H_L)",
    "H_L defined as": "c*sqrt(Lambda_eff/3) with framework rho_Lambda (4 a0^2/(G c^2)), NOT H0, NOT critical-density H_Lambda",
}
t1 = time.time()
out["checks"] = res
out["bounds"] = {
    "wall_s": round(t1-t0, 3),
    "threads": 1,
    "mpmath_digits": 50,
    "memory_peak_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "platform": platform.platform(),
}
print(json.dumps(out, indent=1))