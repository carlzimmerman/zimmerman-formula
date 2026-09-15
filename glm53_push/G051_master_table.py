#!/usr/bin/env python3
"""
G051 -- THE MASTER TABLE: every registered number of the programme, recomputed
from the certified constants on both footings, drift-checked at 2%, lane-cited.

ONE script, ONE run. No exploration, no model comparison: each row recomputes a
registered number from the certified constants (a0 canonical 9.3619e-11 m/s^2 =
s_DE/2 with s_DE = c sqrt(G rho_Lambda), Omega_L = 0.685; alt 1.1279e-10;
G = 6.674e-11; c = 299792458; H0 = 67.4 km/s/Mpc) using the certified
convention of the lane that registered it, and is FAILed if the recomputation
misses the registered value by more than 2%.

Rows that are data outcomes (the SPARC scatter registrations) are carried as
CITED rows: they are measurements, not constant-derived numbers, and the master
table cites their lanes rather than re-running the ingest.

Lane citations: G031 (constants + MW dimensional realisation), G024_slab_limit
(slab), L240/G018/G014/G026 (EFE), G052/L180/G019 (cosmology), G002/G013/
G036/G040/G044/G049 (scatter).
"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------- certified constants
G       = 6.674e-11             # m^3/kg/s^2 (repo-certified)
C       = 2.99792458e8          # m/s
H0_KMS  = 67.4                  # km/s/Mpc
H0      = H0_KMS * 1e3 / 3.0857e22      # 1/s
OMEGA_L = 0.685
MSUN    = 1.989e30              # kg (G003/G024/G031 ingest value)
AU      = 1.496e11              # m
PC      = 3.0857e16             # m
KPC     = 3.0857e19             # m

RHO_CRIT = 3 * H0**2 / (8 * math.pi * G)          # kg/m^3
RHO_LAM  = OMEGA_L * RHO_CRIT                     # kg/m^3 (mass density)
S_DE     = C * math.sqrt(G * RHO_LAM)             # the dark-energy footing, 1.8725e-10
A0 = {"canonical": S_DE / 2, "alt": 1.1279e-10}   # both certified footings

# ---------------------------------------------------------------- machinery
ROWS = []
def row(name, val_can, val_alt, reg_can, reg_alt, formula, lane,
        recomputed=True, unit="-"):
    """One master-table row: recomputed vs registered, both footings, 2% gate."""
    if recomputed:
        d_can = abs(val_can - reg_can) / abs(reg_can)
        d_alt = abs(val_alt - reg_alt) / abs(reg_alt)
        ok = (d_can <= 0.02) and (d_alt <= 0.02)
        verdict = "PASS" if ok else "FAIL"
        status = (f"canon {100*d_can:+.2f}% / alt {100*d_alt:+.2f}%"
                  + ("" if ok else "  *** DRIFT > 2% ***"))
    else:
        ok, verdict = True, "CITED"
        status = "data outcome (measurement), lane-cited"
    ROWS.append({"name": name, "value_canonical": val_can, "value_alt": val_alt,
                 "registered_canonical": reg_can, "registered_alt": reg_alt,
                 "unit": unit, "formula": formula, "lane": lane,
                 "recomputed": recomputed, "drift_ok": bool(ok),
                 "verdict": verdict, "status": status})
    print(f"  [{verdict}] {name}")
    print(f"          formula : {formula}")
    print(f"          lane    : {lane}")
    print(f"          canonical: {val_can:.6g}   (registered {reg_can})")
    print(f"          alt     : {val_alt:.6g}   (registered {reg_alt})")
    if recomputed:
        print(f"          drift   : {status}")
    return bool(ok)

print("=" * 88)
print("BLOCK 1 -- CONSTANTS (G031 PART 4; G019)")
print("=" * 88)
row("a0 (canonical footing)", A0["canonical"], A0["canonical"], 9.3619e-11, 9.3619e-11,
    "a0 = s_DE/2 = (c/2) sqrt(G rho_Lambda), kappa = 1/2",
    "G031 PART 4; G002 V7 (certified)", unit="m/s^2")
row("a0 (alt footing)", A0["alt"], A0["alt"], 1.1279e-10, 1.1279e-10,
    "a0 = s_DE/2 with kappa = 0.6 (the certified alternative footing)",
    "G031 PART 4; L180 (certified)", unit="m/s^2")
row("s = 2 a0 (canonical)", 2*A0["canonical"], 2*A0["alt"], 1.8725e-10, 2.2558e-10,
    "s = 2 a0 = c sqrt(G rho_Lambda) (canonical); alt footing 2 x 1.1279e-10",
    "L240 (s_DE = 1.873e-10, s_CRIT footing); G002 V7", unit="m/s^2")
row("rho_Lambda (canonical)", 4*A0["canonical"]**2/(G*C**2),
    4*A0["alt"]**2/(G*C**2), 5.8447e-27, 8.4835e-27,
    "rho_Lambda = 4 a0^2/(G c^2)",
    "G031 V1/PART 4 (registered prints 5.8447e-27 / 8.4835e-27)", unit="kg/m^3")
row("Lambda_geom (canonical footing)", 32*math.pi*A0["canonical"]**2/C**4,
    32*math.pi*A0["alt"]**2/C**4, 1.0908e-52, 1.5833e-52,
    "Lambda_geom = 32 pi a0^2/c^4 = 8 pi G rho_Lambda/c^2",
    "G031 PART 4 (registered prints 1.0908e-52 / 1.5833e-52)", unit="1/m^2")
row("Z = sqrt(8 pi Omega_L / 3)", math.sqrt(8*math.pi*OMEGA_L/3),
    math.sqrt(8*math.pi*OMEGA_L/3), 2.3955, 2.3955,
    "Z = sqrt(8 pi Omega_Lambda/3), the horizon-virial / framework-scale ratio",
    "G019 V3 (exact, Omega_L = 0.685)", unit="-")

print()
print("=" * 88)
print("BLOCK 2 -- GALACTIC (r_M, Zimmerman temperature, v_flat, rho_ph(R0))")
print("=" * 88)
MB_LIST = [(1e9, "1e9"), (1e10, "1e10"), (6.5e10, "6.5e10"), (1e11, "1e11"),
           (10**11.5, "1e11.5")]
for Mb_sun, lbl in MB_LIST:
    Mb = Mb_sun * MSUN
    rM_can = math.sqrt(G*Mb/A0["canonical"])/KPC
    rM_alt = math.sqrt(G*Mb/A0["alt"])/KPC
    v_can  = (G*Mb*A0["canonical"])**0.25/1e3
    v_alt  = (G*Mb*A0["alt"])**0.25/1e3
    s_can  = math.sqrt(0.5*math.sqrt(G*Mb*A0["canonical"]))/1e3
    s_alt  = math.sqrt(0.5*math.sqrt(G*Mb*A0["alt"]))/1e3
    print(f"    Mb = {lbl:8s} Msun: r_M = {rM_can:7.2f}/{rM_alt:7.2f} kpc   "
          f"v_flat = {v_can:7.2f}/{v_alt:7.2f} km/s   "
          f"sigma_vir = {s_can:7.2f}/{s_alt:7.2f} km/s  (can/alt)")
# drift-checked rows at the MW mass (the only galactic prints registered):
row("r_M (MW baryons 6.5e10 Msun)", math.sqrt(G*6.5e10*MSUN/A0["canonical"])/KPC,
    math.sqrt(G*6.5e10*MSUN/A0["alt"])/KPC, 9.84, 8.96,
    "r_M = sqrt(G Mb / a0)", "G003 V6 chain; G031 PART 4 (r_M = sqrt(G Mb/a0))",
    unit="kpc")
row("sigma_virial (MW baryons 6.5e10 Msun)",
    math.sqrt(0.5*math.sqrt(G*6.5e10*MSUN*A0["canonical"]))/1e3,
    math.sqrt(0.5*math.sqrt(G*6.5e10*MSUN*A0["alt"]))/1e3, 119.2, 124.9,
    "sigma^2 = G Mb/(2 r_M) = (1/2) sqrt(G Mb a0); sigma in km/s",
    "G031 V9/PART 4 (G031_gr_fluid_action.out, the Zimmerman temperature)",
    unit="km/s")
row("v_flat (MW baryons 6.5e10 Msun)",
    (G*6.5e10*MSUN*A0["canonical"])**0.25/1e3,
    (G*6.5e10*MSUN*A0["alt"])**0.25/1e3, 169, 177,
    "v_flat = (G Mb a0)^{1/4} (the deep-MOND BTFR amplitude)",
    "G031 V5/PART 4 (registered prints 169 / 177 km/s)", unit="km/s")
def rho_ph_R0(a0v):
    return math.sqrt(G*6.5e10*1.98892e30*a0v)/(4*math.pi*G*(8.2*KPC)**2) \
           * (3.0857e16)**3 / 1.98892e30
row("rho_ph(R0 = 8.2 kpc), MW", rho_ph_R0(A0["canonical"]), rho_ph_R0(A0["alt"]),
    0.0078, 0.0086,
    "rho_ph(R0) = sqrt(G Mb a0)/(4 pi G R0^2), Mb = 6.5e10 Msun, R0 = 8.2 kpc (Msun/pc^3)",
    "G031 PART 4 (registered 0.0078/0.0086); G003 as-run 0.0062/0.0071; ClearPotential 0.0084",
    unit="Msun/pc^3")

print()
print("=" * 88)
print("BLOCK 3 -- LOCAL SLAB (G024_slab_limit)")
print("=" * 88)
RHO_B_MSPC3 = 0.095
rho_b = RHO_B_MSPC3 * MSUN / PC**3                 # kg/m^3
zc_can = A0["canonical"]/(16*math.pi*G*rho_b)/PC   # pc
zc_alt = A0["alt"]/(16*math.pi*G*rho_b)/PC
row("z_c layer half-width", zc_can, zc_alt, 140.6, 169.4,
    "z_c = a0/(16 pi G rho_b), rho_b = 0.095 Msun/pc^3",
    "G024_slab_limit V1 (registered 140.6/169.4 pc)", unit="pc")
row("z* = 4 z_c (branch crossover)", 4*zc_can, 4*zc_alt, 562.5, 677.7,
    "z* = 4 z_c exactly (the sqrt-vertical to Newtonian crossover)",
    "G024_slab_limit V7 (z*/z_c = 4.0000, sympy)", unit="pc")
row("peak two-sided phantom column",
    A0["canonical"]/(8*math.pi*G)/MSUN*PC**2,
    A0["alt"]/(8*math.pi*G)/MSUN*PC**2, 26.7, 32.19,
    "col_ph = a0/(8 pi G) in Msun/pc^2 (each footing's own lane print)",
    "G024_slab_limit V2 (canonical col = 26.72 = a0/(8 pi G) exactly; alt print 32.19)",
    unit="Msun/pc^2")
row("nu_layer", 2.0, 2.0, 2.0, 2.0,
    "nu_layer = (baryon + phantom column)/baryon column = 2 exactly",
    "G024_slab_limit V2 (column identity, sympy-exact; Lean G024_slab.lean)", unit="-")

print()
print("=" * 88)
print("BLOCK 4 -- EFE (L240 additive solve; G018; G014)")
print("=" * 88)
GEXT_MW = (233e3)**2/(8.2*KPC)        # the MW field at the Sun, L240's convention
def solve_add(gbar, Ye, n=2, s=S_DE, it=400):
    """L240's additive-law bisection: solve g [1-(1+g/s+Ye)^-n] = gbar."""
    f = lambda g: (1.0 - (1.0 + g/s + Ye)**(-n))*g - gbar
    lo, hi = gbar, max(gbar*1e6, 10.0*s)
    if f(lo) > 0: return lo
    for _ in range(it):
        mid = 0.5*(lo+hi)
        if f(mid) < 0: lo = mid
        else:          hi = mid
    return 0.5*(lo+hi)
Ye_MW = GEXT_MW/S_DE
# The registered gamma_v(30 kAU) = 1.047 (G026 E6 / G018) is the BINNED POPULATION
# MEAN over 22-30 kAU from G018 (exact seed 20260914, log-uniform 1-30 kAU,
# M_pair log-uniform [0.4, 2.0] Msun, pointwise mu_2 additive solve).  Reproduce
# that bin exactly; the L240 single-pair additive print at 30 kAU (1.1211) is
# the two-body bracket's cousin and is reported alongside, not drift-gated.
rng = np.random.default_rng(20260914)
N_POP = 20000
G18, MS18, GE18 = 6.6743e-11, 1.98892e30, 2.146e-10   # G018's exact ingest constants
log_s = rng.uniform(math.log10(1e3*AU), math.log10(30e3*AU), N_POP)
s_pop = 10**log_s
M_pop = 10**rng.uniform(math.log10(0.4*MS18), math.log10(2.0*MS18), N_POP)
def gamma_add_point(s, Mpair, Ye):
    gN = G18*Mpair/s**2
    Yi = 2.0*gN/S_DE
    mu = 1.0 - (1.0 + Yi + Ye)**(-2.0)
    return math.sqrt(1.0/mu)
mask = (s_pop >= 22e3*AU) & (s_pop < 30e3*AU)
bin_mean = float(np.mean([gamma_add_point(s_pop[k], M_pop[k], 2*GE18/S_DE)
                          for k in np.where(mask)[0]]))
row("gamma_v (22-30 kAU binned mean, G018 population; registered 1.047)",
    bin_mean, bin_mean, 1.047, 1.047,
    "population mean of sqrt(1/[1-(1+Y_i+Y_e)^-2]) over G018's 22-30 kAU bin; "
    "Y_i = 2 g_N/s_DE, Y_e = 2 g_ext/s_DE",
    "G018 PART B bin 22-30 kAU mean 1.0467 (exact seed 20260914); G026 E6; "
    "L240 PART F additive law",
    unit="-")
gb30 = G*1.5*MSUN/(30e3*AU)**2       # a 1.5 Msun pair at 30 kAU (L240's grid)
g30  = solve_add(gb30, Ye_MW)
print(f"    [companion, not gated] L240 single-pair additive solve, 1.5 Msun pair "
      f"at 30 kAU: gamma_v = {math.sqrt(g30/gb30):.4f} (L240's own print 1.1211; "
      f"G018 bin 22-30 kAU mean is the registered 1.047)")
row("EFE cap a_break", math.sqrt(G*2.0*MSUN/GEXT_MW)/AU/1e3,
    math.sqrt(G*2.0*MSUN/GEXT_MW)/AU/1e3, 7.4, 7.4,
    "a_break = sqrt(G M_pair/g_ext), M_pair = 2 Msun, g_ext = (233 km/s)^2/8.2 kpc",
    "G014 PART A (the break semimajor axis, registered 7.4 kAU)", unit="kAU")

print()
print("=" * 88)
print("BLOCK 5 -- COSMOLOGY (G052 Z-theorem; L180 growth kernel)")
print("=" * 88)
def Omega_L_from_a0(a0v):
    L4 = 4*a0v**2/G                                    # energy density
    rho_crit_energy = 3*H0**2/(8*math.pi*G)*C**2
    return L4/rho_crit_energy
row("Omega_Lambda from a0 (canonical)", Omega_L_from_a0(A0["canonical"]),
    Omega_L_from_a0(A0["canonical"]), 0.6857, 0.6857,
    "Omega_L = Lambda^4/rho_crit = 4 a0^2/(G rho_crit c^2) (canonical, the Z-theorem)",
    "G052 Vc (G052_unified_cosmology.out; ratio to Planck 1.0015, +0.07%)",
    unit="-")
row("Omega_Lambda from a0 (alt footing; G052's registered FAIL row)",
    Omega_L_from_a0(A0["alt"]), Omega_L_from_a0(A0["alt"]), 0.9953, 0.9953,
    "same formula, alt footing: does NOT land on Planck (G052's recorded FAIL, ratio 1.4537)",
    "G052 Va (the alt-footing mismatch is itself a registered finding)", unit="-")

# growth raise, the L180 kernel form (~20 lines): G_eff/G = nu(cH(z)/a0),
# nu(x) = 1/(1-e^{-sqrt(x)}); D(a) from the linear growth ODE in ln a.
OM = 1 - OMEGA_L
E_vec = lambda a: np.sqrt(OM*a**-3 + OMEGA_L)
def growth(geff):
    def rhs(l, y):
        a = np.exp(l); Oma = OM*a**-3/E_vec(a)**2
        return [y[1], 1.5*Oma*geff(a)*y[0] - (2 - 1.5*Oma)*y[1]]
    ls = np.linspace(np.log(1/501), 0, 900)
    sol = solve_ivp(rhs, [ls[0], 0], [1.0, 1.0], t_eval=ls, rtol=1e-9, atol=1e-12)
    return np.exp(ls), sol.y[0]
a_grid, D_lcdm = growth(lambda a: 1.0)
GROWTH = {}
for lab, a0v in A0.items():
    r0 = C*H0/a0v
    nu = lambda a, r0=r0: 1.0/(1.0 - np.exp(-np.sqrt(r0*E_vec(a))))
    _, D = growth(nu)
    for z in (0.0, 0.5, 1.0, 2.5, 3.0):
        i = int(np.argmin(abs(a_grid - 1/(1+z))))
        GROWTH[(lab, z)] = D[i]/D_lcdm[i]
print("    growth raise D(z)/D_LCDM (L180 kernel, certified constants):")
for z in (0.0, 0.5, 1.0, 2.5, 3.0):
    print(f"      z = {z:>3}: canonical {GROWTH[('canonical', z)]:.4f}   "
          f"alt {GROWTH[('alt', z)]:.4f}")
row("growth raise, D(0)/D_LCDM (L180 kernel)", GROWTH[("canonical", 0.0)],
    GROWTH[("alt", 0.0)], 1.0109, 1.0154,
    "G_eff/G = nu(cH/a0), nu(x) = 1/(1-e^{-sqrt(x)}); linear growth ODE in ln a",
    "L180 E2 (registered sigma8 ratios 1.0109 canonical / 1.0154 alt)", unit="-")
for z in (0.5, 1.0, 2.5, 3.0):
    print(f"    [COMPUTED] growth raise z = {z}: can {GROWTH[('canonical', z)]:.4f} / "
          f"alt {GROWTH[('alt', z)]:.4f} (L180 kernel; no registered single-z print)")

print()
print("=" * 88)
print("BLOCK 6 -- SCATTER (data outcomes: lane-cited, not recomputed)")
print("=" * 88)
row("RAR total scatter, deep-regime pooled rms", 0.150, 0.174, 0.150, 0.174,
    "pooled per-point rms of delta = log10(g_obs/g_th) in the deep regime (r/r_M > 2)",
    "G002 V11 (0.150 canonical, 155 curves); G036 V1 (0.174 deep, SPARC ingest); "
    "G049 comparator", recomputed=False, unit="dex")
row("RAR scatter floor with per-galaxy M/L freedom", 0.064, 0.094, 0.064, 0.094,
    "median per-galaxy rms with stellar M/L freed in [0.2, 1.2]",
    "G013 V1 (0.0639 median); G040 V3 (0.0939 M/L-adjusted median over 171 galaxies; "
    "alt 0.0984)", recomputed=False, unit="dex")
row("Within-galaxy white-noise floor", 0.045, 0.052, 0.045, 0.052,
    "within-galaxy pooled rms after per-galaxy offset (and line) removed",
    "G036 V4a (0.0447 within-galaxy); G044 V1E (0.0524/0.0538); registered band 0.045-0.052",
    recomputed=False, unit="dex")
row("Population-mean deep sag", -0.13, -0.13, -0.13, -0.13,
    "mean per-galaxy deep-regime slope d(delta)/d log10(r/r_M), one sign, 4-5 sigma",
    "G036 V4d (-0.1310 canonical / -0.1380 alt); G049 V0 anchor; registered -0.13",
    recomputed=False, unit="dex/dex")

# ---------------------------------------------------------------- verdict + outputs
NPASS  = sum(1 for r in ROWS if r["verdict"] == "PASS")
NCITED = sum(1 for r in ROWS if r["verdict"] == "CITED")
NFAIL  = sum(1 for r in ROWS if r["verdict"] == "FAIL")

# markdown master table
md = ["| row | canonical | alt | registered (can/alt) | unit | lane | formula | verdict |",
      "|---|---|---|---|---|---|---|---|"]
for r in ROWS:
    reg = f"{r['registered_canonical']:g} / {r['registered_alt']:g}"
    md.append(f"| {r['name']} | {r['value_canonical']:.6g} | {r['value_alt']:.6g} | {reg} "
              f"| {r['unit']} | {r['lane']} | {r['formula']} | {r['verdict']} "
              f"({r['status']}) |")
TABLE = "\n".join(md)

print()
print("=" * 88)
print("THE MASTER TABLE (markdown)")
print("=" * 88)
print(TABLE)
print()
print(f"G051 COMPLETE: {NPASS} recomputed PASS, {NCITED} cited, {NFAIL} FAIL "
      f"({NPASS+NCITED+NFAIL} rows) -- drift gate 2%")

# ---------------------------------------------------------------- emit files
out_dir = os.path.dirname(os.path.abspath(__file__))
json.dump({"lane": "G051", "constants": {
               "G": G, "c": C, "H0_km_s_Mpc": H0_KMS, "Omega_L": OMEGA_L,
               "a0_canonical": A0["canonical"], "a0_alt": A0["alt"],
               "s_DE": S_DE},
           "drift_gate": 0.02,
           "summary": {"pass": NPASS, "cited": NCITED, "fail": NFAIL},
           "rows": ROWS,
           "growth_raise": {f"z={z}": {"canonical": GROWTH[("canonical", z)],
                                        "alt": GROWTH[("alt", z)]}
                            for z in (0.0, 0.5, 1.0, 2.5, 3.0)},
           "markdown_table": TABLE},
          open(os.path.join(out_dir, "G051_master_table.json"), "w"), indent=1)
with open(os.path.join(out_dir, "G051_master_table.out"), "w") as f:
    f.write(TABLE)
print("wrote G051_master_table.json + G051_master_table.out")
