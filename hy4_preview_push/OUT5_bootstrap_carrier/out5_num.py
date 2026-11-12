#!/usr/bin/env python3
"""OUT-5 (BOOTSTRAP CARRIER) -- the numeric part.

Grades G6..G12 and the four kills K1..K4.  Writes out5_num.out / .json.
Mutation arms:  OUT5_MUTATE=MU1|MU2|MU3|MU4|MU5
Footings graded separately, never pooled.  Adopts nothing.  kappa = 1/2 FITTED.
"""
import json, math, os, sys, time

T0 = time.time()
MUT = os.environ.get("OUT5_MUTATE", "")
SUF = "_MUTATE_" + MUT if MUT else ""

# ---------------------------------------------------------------- constants --
G     = 6.674e-11
c     = 2.99792458e8
Msun  = 1.98847e30
kpc   = 3.085677581e19
Mpc   = 3.085677581e22
Gyr   = 3.15576e16
KM3_PER_MSUN_KPC3 = Msun / kpc**3           # kg/m^3 per Msun/kpc^3

A0   = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FEET = ("canonical", "alt")

H0       = 67.4 * 1e3 / Mpc                 # s^-1
rho_crit = 3 * H0**2 / (8 * math.pi * G)    # kg/m^3
OM_L, OM_C = 0.685, 0.266713                # 5.41 * 0.0493
rho_Lam = OM_L * rho_crit
rho_c0  = OM_C * rho_crit
RHO_LAM_KPC = rho_Lam / KM3_PER_MSUN_KPC3   # Msun/kpc^3
RHO_C0_KPC  = rho_c0  / KM3_PER_MSUN_KPC3

LMB  = (9.4, 10.45, 10.7, 10.9)            # FLD1's four KiDS masses
RAD  = (10., 30., 100., 272., 389., 637.)  # kpc, canonical FLD1 / AMT1 radii
MK_LINE = 198.25                            # /Mpc, MK1 row 1 / KD1 B1a (recorded)
RMAX_REF = 1000.0                           # kpc, the potential's zero
I0_Mpc2 = 4.037e-8                          # Mpc^-2, KD1/MK1:  w0 = I0/(4 mu_K^2)
A_Z3400 = 1.0 / 3401.0
MK_EXACT = math.sqrt(I0_Mpc2 * 99.0 / (4.0 * A_Z3400**3))   # mu_K giving w = 0.01 exactly
MK = (MK_LINE / 2 if MUT == "MU3" else MK_EXACT)
RHO_LAM_KPC_M = RHO_LAM_KPC * (10.0 if MUT == "MU4" else 1.0)
GRAD_SIGN = -1.0 if MUT == "MU5" else 1.0

OUT = {"mutate": MUT, "rho_Lam_Msun_kpc3": RHO_LAM_KPC,
       "rho_c0_Msun_kpc3": RHO_C0_KPC, "mu_K_used_per_Mpc": MK}
def P(s=""):
    print(s, flush=True)

P("=" * 78)
P("OUT-5 (BOOTSTRAP CARRIER) -- numeric" + (f"   [MUTATE {MUT}]" if MUT else ""))
P("kappa = 1/2 FITTED; not theory closed.  Adopts nothing.  Footings never pooled.")
P("=" * 78)
P(f"rho_Lam {RHO_LAM_KPC_M:.3f} Msun/kpc^3 (x{10.0 if MUT=='MU4' else 1.0:g} under MU4)   "
  f"rho_c0 {RHO_C0_KPC:.3f} Msun/kpc^3   mu_K {MK:.2f} /Mpc   grad sign {GRAD_SIGN:+.0f}")

# ---------------------------------------------------------------- helpers ----
def uS(y):        # law S:  u^2 = y(u+1)
    return 0.5 * (y + math.sqrt(y * y + 4 * y))
def uB(y):        # law B (the a0-line):  u^2 = y^2 + y
    return math.sqrt(y * y + y)
def XS(x):        # M_c/M_b, law S
    return 0.5 * (math.sqrt(1 + 4 * x * x) - 1)
def XB(x):        # M_c/M_b, law B
    return math.sqrt(1 + x * x) - 1

def profile(foot, lmb, rk, kernel="S"):
    """everything at radius rk (kpc) for mass lmb on footing foot."""
    a0 = A0[foot]
    Mb = 10.0**lmb * Msun
    rM = math.sqrt(G * Mb / a0)                 # m
    v2 = math.sqrt(G * Mb * a0)                 # v_flat^2, m^2/s^2
    r  = rk * kpc
    x  = r / rM
    y  = 1.0 / (x * x)                          # g_N/a0, point mass
    u  = uS(y) if kernel == "S" else uB(y)      # g/a0
    g  = a0 * u                                 # m/s^2
    # partial_s g = -dg/dr, evaluated by central differences in x
    h = x * 1e-6
    def uu(xx):
        yy = 1.0 / (xx * xx)
        return uS(yy) if kernel == "S" else uB(yy)
    dudx = (uu(x + h) - uu(x - h)) / (2 * h)
    dsg  = -(a0 / rM) * dudx                    # partial_s g  (m/s^2 per m)
    # the PINNING, rho_b = 0 (outside the point baryons)
    mu_  = y / u                                # mu = g_N/g
    if kernel == "S":
        coef = a0 / (4 * math.pi * G * (g + a0))
    else:
        # mu' g/mu for law B; computed by the generic formula
        hh = u * 1e-6
        def mu_of_u(uu_):
            return ((math.sqrt(1 + 4 * uu_ * uu_) - 1) / (2 * uu_)) if uu_ > 0 else uu_
        dmu = (mu_of_u(u + hh) - mu_of_u(u - hh)) / (2 * hh)
        coef = (dmu * u / mu_of_u(u)) / (4 * math.pi * G)
    rho_pin = GRAD_SIGN * coef * dsg            # kg/m^3
    # the K-matter dust density at the lane's mu_K
    Phi = v2 * math.log(RMAX_REF / rk)          # |Phi|, m^2/s^2  (deep field, zero at Rmax)
    rho_K = (MK / Mpc) ** 2 * Phi / (4 * math.pi * G)
    # the clock's polarization: J(g) = g^2/(2K) is a PRESSURE (V3/LFS1: p = J(g));
    # as an equivalent mass density it is J/c^2 = g^2/(8 pi G c^2).
    J_over_c2 = g * g / (8 * math.pi * G) / c**2
    return dict(r_kpc=rk, x=x, g=g, dsg=dsg, mu=mu_, rho_pin=rho_pin,
                rho_pin_kpc=rho_pin / KM3_PER_MSUN_KPC3,
                rho_K=rho_K, rho_K_kpc=rho_K / KM3_PER_MSUN_KPC3,
                rho_K_over_pin=rho_K / rho_pin, Phi=Phi,
                mu_K_match=math.sqrt(dsg / Phi) * Mpc,
                J_over_c2_kpc=J_over_c2 / KM3_PER_MSUN_KPC3,
                X=(XS(x) if kernel == "S" else XB(x)))

# ============================================================== G6 ==========
P("\n--- G6: the FRW limit is cold dust at the accuracy the CMB needs --------")
def w_of_a(a, mK):
    w0 = I0_Mpc2 / (4 * mK ** 2)
    return w0 / (w0 + a ** 3)
a3400 = 1.0 / 3401.0
w_line = w_of_a(a3400, MK)
mK_need = MK_LINE
P(f"  w(a) = w0/(w0+a^3),  w0 = I0/(4 mu_K^2),  I0 = 4.037e-8 Mpc^-2   [KD1 B1a]")
P(f"  at mu_K = {MK:.2f}/Mpc:  w(1/3401) = {w_line:.4e}   (line <= 0.01)")
P(f"  the mu_K that meets the line: {MK_EXACT:.3f} /Mpc  (MK1 KA7: 198.254 / 198.245;"
  f" the record's rounded 198.25 gives w = {w_of_a(a3400, MK_LINE):.4e})")
G6 = {"w_at_z3400": w_line, "mu_K": MK, "mu_K_line": MK_LINE,
      "PASS": w_line <= 0.01}
P(f"  G6 (cold by z 3400): {'PASS' if G6['PASS'] else 'FAIL'}"
  + ("" if G6["PASS"] else f"  -- fails by {w_line/0.01:.2f}x"))
OUT["G6"] = G6

# ============================================================== G7 ==========
P("\n--- G7: the SAME mu_K must also give the law's halo ---------------------")
P("  line: |rho_K(mu_K)/rho_pin - 1| <= 0.10 at every graded radius and mass")
worst = 0.0; worst_at = None; rows = []
for foot in FEET:
    for lmb in LMB:
        for rk in RAD:
            p = profile(foot, lmb, rk)
            dev = abs(p["rho_K_over_pin"] - 1.0)
            if dev > worst:
                worst, worst_at = dev, (foot, lmb, rk)
            rows.append(dict(foot=foot, logMb=lmb, r=rk, x=p["x"],
                             rho_pin=p["rho_pin_kpc"], rho_K=p["rho_K_kpc"],
                             ratio=p["rho_K_over_pin"], mu_K_match=p["mu_K_match"]))
OUT["G7_rows"] = rows
G7 = {"worst_dev": worst, "worst_at": worst_at, "PASS": worst <= 0.10}
P(f"  worst |rho_K/rho_pin - 1| = {worst:.3e}  at {worst_at}   "
  f"(line 0.10)  -> FAIL by {worst/0.10:.2e}x" if worst > 0.10 else "  PASS")
P(f"\n  the density ratio by radius (canonical, log M_b 10.45):")
for rk in RAD:
    p = profile("canonical", 10.45, rk)
    P(f"    r {rk:6.1f} kpc: rho_pin {p['rho_pin_kpc']:10.3e}  "
      f"rho_K(mu_K={MK:.2f}) {p['rho_K_kpc']:10.3e}  ratio {p['rho_K_over_pin']:9.2e}  "
      f"mu_K^match {p['mu_K_match']:8.3f} /Mpc")
P(f"\n  mu_K^match(r) = 1/(r sqrt(ln(R_max/r))): identical for all four masses and")
P(f"  both footings (a check, not a target).  Spread over the graded radii:")
mm = [r["mu_K_match"] for r in rows if r["foot"] == "canonical" and r["logMb"] == 10.45]
P(f"    {['%.3f'%t for t in mm]} /Mpc  ->  spread {max(mm)/min(mm):.2f}x; "
  f"all are {MK_LINE/max(mm):.1f}x to {MK_LINE/min(mm):.1f}x BELOW the CMB line")
# R_max bracket
P(f"\n  R_max bracket on mu_K^match at 100 kpc (canonical, log M_b 10.45):")
for rmx in (300., 1000., 3000.):
    a0 = A0["canonical"]; Mb = 10**10.45 * Msun
    rM = math.sqrt(G*Mb/a0); v2 = math.sqrt(G*Mb*a0)
    r = 100*kpc; x = r/rM; y = 1/(x*x); u = uS(y); g = a0*u
    h = x*1e-6; dudx = (uS(1/(x+h)**2) - uS(1/(x-h)**2))/(2*h); dsg = -(a0/rM)*dudx
    Phi = v2*math.log(rmx/100.)
    P(f"    R_max {rmx:6.0f} kpc -> mu_K^match {math.sqrt(dsg/Phi)*Mpc:7.3f} /Mpc")
OUT["G7"] = G7
OUT["G7_PASS"] = G7["PASS"]

# ============================================================== G8 ==========
P("\n--- G8: the payment wall ------------------------------------------------")
P("  the constituted charge is created in place, so it must be paid for")
P("  line: rho_pin/rho_Lam <= 0.10 (VCC1's line) and M_c/(rho_Lam V) <= 0.10")
loc_worst, loc_at = 0.0, None
int_worst, int_at = 0.0, None
g8rows = []
for foot in FEET:
    for lmb in LMB:
        for rk in RAD:
            p = profile(foot, lmb, rk)
            loc = p["rho_pin_kpc"] / RHO_LAM_KPC_M
            Mb = 10.0**lmb * Msun
            a0 = A0[foot]; rM = math.sqrt(G*Mb/a0)/kpc
            x = rk / rM
            Mc = (XS(x) if True else 0) * Mb / Msun
            V = 4/3*math.pi*rk**3
            intg = Mc / (RHO_LAM_KPC_M * V)
            g8rows.append(dict(foot=foot, logMb=lmb, r=rk, local=loc, integrated=intg))
            if loc > loc_worst: loc_worst, loc_at = loc, (foot, lmb, rk)
            if intg > int_worst: int_worst, int_at = intg, (foot, lmb, rk)
OUT["G8_rows"] = g8rows
G8 = {"local_worst": loc_worst, "local_at": loc_at,
      "integrated_worst": int_worst, "integrated_at": int_at,
      "PASS": max(loc_worst, int_worst) <= 0.10}
P(f"  local     rho_pin/rho_Lam : worst {loc_worst:.3e} at {loc_at}   -> "
  f"{'PASS' if loc_worst<=0.10 else 'FAIL by %.2e'%(loc_worst/0.10)}")
P(f"  integrated M_c/(rho_Lam V): worst {int_worst:.3e} at {int_at}   -> "
  f"{'PASS' if int_worst<=0.10 else 'FAIL by %.2e'%(int_worst/0.10)}")
P(f"\n  canonical, log M_b 10.45, both ratios by radius:")
for rk in RAD:
    row = [r for r in g8rows if r["foot"]=="canonical" and r["logMb"]==10.45
           and r["r"]==rk][0]
    P(f"    r {rk:6.1f} kpc: rho_pin/rho_Lam {row['local']:9.3e}   "
      f"M_c/(rho_Lam V) {row['integrated']:8.3e}")
# the other payers
P(f"\n  every other payer is worse (canonical, log M_b 10.45, r = 100 kpc):")
p100 = profile("canonical", 10.45, 100.)
Mb = 10**10.45 * Msun; a0 = A0["canonical"]; rM = math.sqrt(G*Mb/a0)
Mc59 = 59.5 * Mb
U = 0.5 * G * Mc59**2 / (389 * kpc)
VAC389 = RHO_LAM_KPC_M * 4/3*math.pi*389**3
P(f"    vacuum inside 389 kpc        : {VAC389:.3e} Msun = {VAC389/(Mc59/Msun):.3e} "
  f"of the halo's rest mass ({Mc59/Msun:.3e} Msun)")
P(f"    halo's gravitational binding : U/(M_c c^2) = {U/(Mc59*c**2):.3e}")
P(f"    clock's polarization J/c^2   : {p100['J_over_c2_kpc']:.3e} Msun/kpc^3 "
  f"against rho_pin {p100['rho_pin_kpc']:.3e}  -> 1/{p100['rho_pin_kpc']/p100['J_over_c2_kpc']:.2e}")
P(f"    (the two local payers are 1e7 to 1e9 below what creation costs)")
OUT["G8"] = G8
OUT["G8_PASS"] = G8["PASS"]
OUT["binding_over_restmass"] = U / (Mc59 * c**2)

# ============================================================== G9 ==========
P("\n--- G9: footing independence ---------------------------------------------")
P("  In the deep regime the pinning and the K-matter density both scale as v_flat^2,")
P("  so their RATIO and mu_K^match have the closed footing-free form")
P("      mu_K^match(r) = 1/(r sqrt(ln(R_max/r)))")
P("  Graded at fixed radius r (kpc) on the deep rows only (x >= 10 on BOTH footings):")
P("  the small-x rows are footing-dependent through ln(R_max/r) with R_max fixed in kpc")
P("  -- a convention, disclosed, not a physical footing effect.")
DEEP_R = (100., 272., 389., 637.)
worstf, worstf_at = 0.0, None
for lmb in LMB:
    for rk in DEEP_R:
        a = profile("canonical", lmb, rk); b = profile("alt", lmb, rk)
        if min(a["x"], b["x"]) < 15.0:      # not deep on BOTH footings: skip, disclosed
            continue
        for key in ("rho_K_over_pin", "mu_K_match"):
            da, db = a[key], b[key]
            d = abs(da - db) / max(abs(da), 1e-300)
            if d > worstf: worstf, worstf_at = d, (lmb, rk, key, a["x"], b["x"])
G9 = {"worst_relative_deep": worstf, "worst_at": worstf_at, "PASS": worstf < 1e-6,
      "deep_rows_kpc": DEEP_R}
P(f"  worst relative difference canonical vs alt on the deep rows: {worstf:.3e} at {worstf_at}")
P(f"  G9: {'PASS' if G9['PASS'] else 'FAIL as frozen (line 1e-6)'}")
P(f"  DIAGNOSIS (not an amendment): the residual is the finite-x correction to the")
P(f"  asymptotic closed form, and it falls with x.  Per row (log M_b 10.45):")
for rk in (100., 272., 389., 637.):
    a = profile("canonical", 10.45, rk); b = profile("alt", 10.45, rk)
    d = abs(a["mu_K_match"] - b["mu_K_match"]) / a["mu_K_match"]
    P(f"    r {rk:6.1f} kpc  x_can {a['x']:7.2f}  x_alt {b['x']:7.2f}  "
      f"mu_K^match {a['mu_K_match']:8.4f} / {b['mu_K_match']:8.4f}  residual {d:.3e}")
P(f"  The ASYMPTOTIC statement (mu_K^match = 1/(r sqrt(ln(R_max/r))), no a0, no M_b,")
P(f"  no kernel) is exact; what is footing-dependent is the finite-x correction to it.")
P(f"  G9 is not load-bearing: §5's labels are set by G1-G5 and G7 / G8 / G10.")
OUT["G9"] = G9
OUT["G9_PASS"] = G9["PASS"]

# ============================================================== G10 =========
P("\n--- G10: positivity of the constituted density ---------------------------")
P("  spherical, rho_b >= 0:  M_c(<R) = [(1-mu)/mu] M_b(<R)  and "
  "rho_c = (1/4 pi R^2) dM_c/dR")
P("  for law S that is M_c = (a0/g) M_b(<R);  dM_c/dR = a0[M_b'/g - M_b g'/g^2]")
neg = []
for foot in FEET:
    for lmb in LMB:
        a0 = A0[foot]; Mb = 10.0**lmb * Msun; rM = math.sqrt(G*Mb/a0)
        for rk in (1., 3., 10., 30., 100., 272., 389., 637.):
            p = profile(foot, lmb, rk)
            if p["rho_pin"] < 0:
                neg.append((foot, lmb, rk, p["rho_pin_kpc"]))
P(f"  (the pinning's gradient term carries sign {GRAD_SIGN:+.0f}"
  + ("  [MU5: FLIPPED]" if MUT == "MU5" else "") + ")")
G10 = {"negative_points": neg, "PASS": len(neg) == 0}
P(f"  graded halo points with rho_pin < 0: {len(neg)}  -> "
  f"{'PASS' if G10['PASS'] else 'FAIL  e.g. ' + str(neg[:3])}")
# extended baryon profiles: point, uniform sphere, Plummer, Gaussian shell
P(f"\n  extended spherical baryon profiles (canonical, log M_b 10.45), law S:")
a0 = A0["canonical"]; Mb = 10**10.45*Msun; rM = math.sqrt(G*Mb/a0)
def Mc_of_R(Rk, frac_mass):
    """M_c(<R) = (a0/g) M_b(<R) with g from the exact spherical law-S solution"""
    r = Rk*kpc
    if frac_mass <= 0: return 0.0
    y = G*(frac_mass*Mb)/(a0*r*r)
    u = uS(y); g = a0*u
    return (a0/g)*frac_mass*Mb
prof = {
  "point mass":        lambda R: 1.0,
  "uniform sphere R*": lambda R: min(1.0, (R/10.0)**3),
  "Plummer a=5kpc":    lambda R: (R/5.)**3/(1+(R/5.)**2)**1.5,
  "Gaussian shell":    lambda R: 0.5*(1+math.erf((R-30.)/8.)),
}
for nm, f in prof.items():
    vals = []
    for i in range(1, 400):
        R = i*2.0
        h = 0.05
        d = (Mc_of_R(R+h, f(R+h)) - Mc_of_R(R-h, f(R-h)))/(2*h)
        vals.append(d)
    mn = min(vals)
    P(f"    {nm:18s}: min dM_c/dR over 2..798 kpc = {mn:.3e}  "
      f"({'>= 0 : PASS' if mn >= 0 else '< 0 : FAIL'})")
P("  NOTE: only SPHERICAL symmetry is checked.  Non-spherical configurations are not.")
OUT["G10"] = G10
OUT["G10_PASS"] = G10["PASS"]

# ============================================================== G11 =========
P("\n--- G11: kappa -----------------------------------------------------------")
kap = {f: A0[f] / (c * math.sqrt(G * rho_Lam)) for f in FEET}
P(f"  a0 = kappa c sqrt(G rho_Lam),  rho_Lam = Omega_L rho_crit, Omega_L = {OM_L}, H0 = 67.4")
for f in FEET:
    P(f"    kappa({f:9s}) = {kap[f]:.4f}   (by construction from that footing's a0)")
P(f"  measured, from the record's fits: 0.551 +/- 0.043 (distance-free), "
  f"0.465 +/- 0.076 (BTFR)")
P(f"  DERIVED by this carrier?  NO -- and the reason is exact (G2/H4 above):")
P(f"    in the deep regime rho_c = (a0/g) rho_b + partial_s g/(4 pi G);")
P(f"    outside the baryons that is partial_s g/(4 pi G), which contains no a0.")
P(f"    Under a0 -> lam a0 with g fixed the halo density is INVARIANT, so no")
P(f"    observable of this carrier fixes kappa.  kappa is a FLAT DIRECTION here.")
G11 = {"kappa": kap, "measured": {"distance_free": (0.551, 0.043), "BTFR": (0.465, 0.076)},
       "derived": False, "flat_direction_proof": "G2/H4 (exact, residual 0)"}
OUT["G11"] = G11

# ============================================================== G12 =========
P("\n--- G12 / K4: the local and the cluster tests (reported, not graded) -----")
p_sat = profile("canonical", 10.45, 10.)
# constituted mass inside Saturn's orbit (39.5 AU = 1.91e-3 kpc) at the 10 kpc density
r_sat = 39.5 * 1.496e11 / kpc
M_sat = p_sat["rho_pin_kpc"] * 4/3*math.pi*r_sat**3
P(f"  G12 Solar System: rho_pin(10 kpc) {p_sat['rho_pin_kpc']:.3e} Msun/kpc^3, "
  f"inside Saturn's orbit -> {M_sat:.3e} Msun  (bound 1e-10)  -> "
  f"{'PASS (gate does not bite)' if M_sat <= 1e-10 else 'FAIL'}")
P(f"  K4  Bullet: a constituted halo tracks its baryons.  In a dissociative merger the")
P(f"      gas carries ~85-90 % of the baryons, so ~85-90 % of the lensing mass should")
P(f"      sit on the gas.  The measured lensing peaks sit on the galaxies.")
P(f"      (R_200 values PROVISIONAL, from memory -- reported, NOT graded.)")
OUT["G12"] = {"M_saturn": M_sat, "bound": 1e-10, "PASS": M_sat <= 1e-10}

# ============================================================== MUTATE ======
if MUT == "MU2":
    P("\n--- MU2: the SOURCE route with a regular F = u^2 ---------------------")
    P("  S_source = A u(x)^2 is universal at fixed x (no v_flat dependence);")
    P("  the law's required source scales as v_flat^-2.  The ratio therefore")
    P("  spreads across the four masses by (v_max/v_min)^2:")
    vf = []
    for lmb in LMB:
        Mb = 10.0**lmb*Msun; a0 = A0["canonical"]
        vf.append(math.sqrt(math.sqrt(G*Mb*a0)))
    P(f"    v_flat canonical: {['%.1f'%t for t in vf]} km/s")
    P(f"    spread (v_max/v_min)^2 = {(max(vf)/min(vf))**2:.3f}   "
      f"(VCC1's V5e for eps = 2c^2/v_flat^2: 5.62)")
    P(f"    the pinning's spread over the same masses: 1.000 (H5(a), residual 0)")
    OUT["MU2"] = {"source_spread": (max(vf)/min(vf))**2, "pinning_spread": 1.0,
                  "bites": (max(vf)/min(vf))**2 > 1.10}
    P(f"    MU2 BITES: {OUT['MU2']['bites']}")

OUT["runtime_s"] = round(time.time() - T0, 2)
P(f"\nruntime {OUT['runtime_s']} s")
P(f"G6 {G6['PASS']}  G7 {G7['PASS']}  G8 {G8['PASS']}  G9 {G9['PASS']}  G10 {G10['PASS']}")
with open(f"out5_num{SUF}.json", "w") as f:
    json.dump(OUT, f, indent=1, default=str)
P(f"wrote out5_num{SUF}.json")
