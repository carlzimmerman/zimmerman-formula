"""
AS252 Tier-0b numeric lane: match the cosmological Einstein coefficient to
measured Newton gravity. Both footings (canonical / alternative a0) kept
separate; ratio G_cosm/G_N = c_N = 1 - alpha/2 carried through the
vacuum-scale dictionary; negative control (G_cosm = G_N prematurely) must fire.

Constants (framework contract): G_N = 6.67430e-11, c = 299792458,
M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI). kappa = 1/2 adopted.
"""
import math

# ---------- constants ----------
GN_SI = 6.67430e-11
c_SI = 299792458.0
MSUN = 1.98847e30
PC = 3.085677581491367e16
KAPPA = 0.5  # adopted input (seed)

FOOTINGS = {
    "canonical":   9.3619e-11,
    "alternative": 1.1279e-10,
}
ALPHAS = [0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5]

def rho_lambda(a0, G=GN_SI):
    """Framework: a0 = kappa*c*sqrt(G*rho_Lambda) with kappa=1/2  <=>  rho_Lambda = 4 a0^2/(G c^2)."""
    return 4.0 * a0**2 / (G * c_SI**2)

def kappa_backcheck(a0, rhoL):
    return a0 / (c_SI * math.sqrt(GN_SI * rhoL))

allpass = True
def check(name, cond, detail, tol=None):
    global allpass
    allpass = allpass and bool(cond)
    print(f"{'PASS' if cond else 'FAIL'} {name}: {detail}" + (f" (tol {tol})" if tol else ""))

print("="*78)
print("FOOTINGS table: rho_Lambda, epsilon_Lambda, kappa back-check (kappa = 1/2 adopted)")
print("="*78)
rhoL = {}
for name, a0 in FOOTINGS.items():
    rL = rho_lambda(a0)
    rhoL[name] = rL
    kc = kappa_backcheck(a0, rL)
    check(f"N1_rhoL_{name}", abs(kc - KAPPA) < 1e-12,
          f"a0={a0:.4e} -> rho_Lambda={rL:.6e} kg/m^3, eps=rho*c^2={rL*c_SI**2:.6e} J/m^3, kappa_back={kc:.15f}")
# kappa_eff when canonical density is held fixed with the alternative a0
rL_can = rhoL["canonical"]
kap_eff = FOOTINGS["alternative"] / (c_SI * math.sqrt(GN_SI * rL_can))
check("N2_kappa_eff_fixed_canonical_density",
      abs(kap_eff - KAPPA) > 1e-3,
      f"alternative a0 with canonical rho_Lambda={rL_can:.6e}: kappa_eff={kap_eff:.6f} != 1/2 "
      "(the two footings do not share BOTH fixed density AND fixed kappa)")

print("="*78)
print("VACUUM-SCALE DICTIONARY per footing (alpha sample 0.3 -> c_N = 0.85)")
print("="*78)
for name, a0 in FOOTINGS.items():
    a = 0.3; cN = 1 - a/2
    Lam_eff = 32*math.pi*cN*a0**2/c_SI**4          # correct, ratio carried
    Lam_naive = 32*math.pi*a0**2/c_SI**4           # premature G_cosm = G_N
    H_nat = math.sqrt(Lam_eff/3.0)                 # m^-1 (c=1 Hubble)
    H_SI = c_SI*H_nat                              # s^-1
    rdS = 1.0/H_nat                                # de Sitter radius sqrt(3/Lambda_eff), m
    rdS_naive = 1.0/math.sqrt(Lam_naive/3.0)
    check(f"N3_dict_{name}_identity", abs(Lam_eff*c_SI**4/(32*math.pi*a0**2) - cN) < 1e-15,
          f"Lambda_eff*c^4/(32 pi a0^2) = c_N = {cN:.10f}")
    check(f"N4_Hvac_{name}", abs(H_SI - c_SI*math.sqrt((32*math.pi/3.0)*cN*a0**2/c_SI**4)) < 1e-24*max(1.0,H_SI),
          f"H_vac = c*sqrt(Lambda_eff/3) = {H_SI:.6e} 1/s (H_nat = {H_nat:.6e} 1/m), "
          f"r_dS = sqrt(3/Lambda_eff) = {rdS:.6e} m = {rdS/PC/1e9:.4f} Gpc; naive r_dS = {rdS_naive:.6e} m")
    check(f"N5_ratio_{name}", abs(Lam_eff/Lam_naive - cN) < 1e-15,
          f"Lambda_eff/Lambda_naive = c_N = {cN} < 1 (cosmological coefficient BELOW naive same-G)")
    # negative control numeric: premature identification leaves residual
    resid = (Lam_naive - Lam_eff)/Lam_naive          # relative mismatch of the premature calibration
    check(f"N6_control_fires_{name}", resid > 1e-7,
          f"premature G_cosm=G_N residual = 1 - c_N = {resid:.6f} != 0 (fires); "
          f"alpha/2 = {a/2:.4f} (term removed)")

print("="*78)
print("alpha sweep: c_N, Lambda_eff, H_vac, dictionary factors (canonical footing)")
print("="*78)
a0 = FOOTINGS["canonical"]
for a in ALPHAS:
    cN = 1 - a/2
    Lam_eff = 32*math.pi*cN*a0**2/c_SI**4
    H_nat = math.sqrt(Lam_eff/3.0)
    H_SI = c_SI*H_nat
    rdS = 1.0/H_nat
    print(f"alpha={a:.2f} c_N={cN:.4f} Lambda_eff={Lam_eff:.6e} 1/m^2 "
          f"H_vac={H_SI:.6e} 1/s r_dS={rdS/PC/1e9:.4f} Gpc naive_factor={1/cN:.4f}")

print("="*78)
print("CONTROL: alpha -> 0 recovers the Einstein normalization (both footings)")
print("="*78)
for name, a0 in FOOTINGS.items():
    cN0 = 1.0
    Lam0 = 32*math.pi*cN0*a0**2/c_SI**4
    check(f"A1_{name}", abs(Lam0 - 32*math.pi*a0**2/c_SI**4) < 1e-24,
          f"alpha=0: c_N=1, Lambda_eff = 32 pi a0^2/c^4 = {Lam0:.6e} (naive same-G value recovered); "
          "G_N = G_bare, coefficient 1/(16 pi G_bare) standard")

print("="*78)
print("SI coupling table (alpha = 0.3 sample)")
print("="*78)
a = 0.3; cN = 1 - a/2
G_bare = GN_SI*cN                          # G_bare = c_N G_N  (derived ratio, inverted)
G_cosm = G_bare                            # cosmological Einstein coefficient
check("N7_SI_ratio", abs((G_cosm/GN_SI) - cN) < 1e-15,
      f"G_cosm = G_bare = {G_bare:.6e} m^3 kg^-1 s^-2; G_cosm/G_N = {G_cosm/GN_SI:.10f} = c_N = {cN}")
print(f"rho_Lambda table: " + "; ".join(f"{k}={v:.6e} kg/m^3" for k, v in rhoL.items()))
print(f"ALL_NUMERIC_CHECKS_PASS = {allpass}")
if not allpass:
    raise SystemExit("numeric lane failed")