"""ZT11_zstar_cherenkov: Z-T11 of the Z* (v3s-OC) test plan -- Cherenkov emission of the khronon/dust pair by stars.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (committed alone first, 9ecd65dbd4).
kappa = 1/2 FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 zt11_cherenkov.py            (exit 0 iff all K* pass)
      OMP_NUM_THREADS=1 nice -n 15 python3 zt11_cherenkov.py --mutate   (factor-2 sound-speed error; K1, K3 must fail)
"""
import os
import sys
import json
import math
import time
import hashlib
import resource

MUTATE = ("--mutate" in sys.argv) or os.environ.get("ZT11_MUTATE", "0") == "1"
sys.argv = [a for a in sys.argv if a != "--mutate"]          # s3_aqual reads --mutate from argv: never pass it on
os.environ.pop("S3_MUTATE", None)
os.environ.pop("S3_CACHE_DIR", None)

import numpy as np
import sympy as sp
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"zt11_cherenkov{TAG}.out")
JSN = os.path.join(HERE, f"zt11_cherenkov_results{TAG}.json")
FM = 2.0 if MUTATE else 1.0                                  # mutation: c_s^2 -> 2 gamma_L rho, G -> 2 D.P

T0 = time.time()
lines, checks, res = [], [], {"mutate": MUTATE}


def log(s=""):
    print(s, flush=True)
    lines.append(s)


def check(name, ok, got, want):
    checks.append((name, bool(ok)))
    log(f"  {name} {'PASS' if ok else 'FAIL'}: {got}  [want: {want}]")
    res.setdefault("checks", {})[name] = {"pass": bool(ok), "got": str(got), "want": want}


# ------------------------------------------------------------------ constants (SI)
c_SI = 2.99792458e8
G_SI = 6.67430e-11
GMSUN = 1.32712440018e20
MSUN = GMSUN / G_SI
RSUN = 6.957e8
PC = 3.0856775814913673e16
KPC = 1e3 * PC
AU = 1.495978707e11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTARS_PC = [24, 90]
H0 = 67.4e3 / (1e3 * KPC)                 # s^-1
T_H = 1.0 / H0
YR = 3.15576e7
R0_MW = 8.122
SUN_V = [230.0, 250.0]
DISC_R = [4.0, 6.0, 8.122, 12.0, 16.0]
DISC_M = [1.0, 20.0]
P3_MU_K = 1.0 / (100 * KPC)

log("ZT11_zstar_cherenkov: Cherenkov emission of the khronon/dust pair by stars (Z-T11)")
log(f"mutate = {MUTATE}; kappa = 1/2 FITTED; footings never pooled; mu_K removed in Z* (DESIGN section 3)")
res["constants"] = {"H0_km_s_Mpc": 67.4, "t_H_yr": T_H / YR, "footings": A0, "Lstar_pc": LSTARS_PC}

# ==================================================================== K1: P3's Solar-System c_pi, mu_K dropped
log("")
log("K1: P3 reproduction (c_pi = sqrt(G/Z), mu_K terms dropped)")
p3 = json.load(open(os.path.join(RB, "P3_v3_strong_field", "p3_v3_strong_field_results.json")))["E4"]
phE = 3.986e14 / (6.371e6 * c_SI ** 2)
phS = GMSUN / (AU * c_SI ** 2)
k1rows, k1ok = {}, True
for foot in A0:
    for Lpc in LSTARS_PC:
        L = Lpc * PC
        for sname, kk, Phi in (("Eot-Wash (38.6 um)", 1 / 38.6e-6, phS + phE), ("planets (1 AU)", 1 / AU, phS)):
            KDP = 2 * Phi / L ** 2                         # screened hedgehog, K D.P (m^-2)
            Qbar = 1 + 1e-6
            zh = kk ** 2 / (Qbar ** 2 * (1.0 + L ** 2 * kk ** 2 / 2))   # Z_P (hatted), mu_K^2 dropped
            gh = FM * KDP * (1 + KDP * L ** 2 / 2)                     # G (hatted), mu_K^2 (Qbar-1)/Qbar dropped
            cpi = math.sqrt(gh / zh)
            ref = p3[f"{sname}|{foot}|{Lpc}pc"]["c_pi"]
            rel = abs(cpi / ref - 1)
            k1ok &= rel < 1e-3
            k1rows[f"{sname}|{foot}|{Lpc}pc"] = {"c_pi_here": cpi, "c_pi_P3": ref, "rel": rel, "c_pi_km_s": cpi * c_SI / 1e3}
for k_, v in k1rows.items():
    log(f"    {k_:40s} c_pi {v['c_pi_here']:.6e} (P3 {v['c_pi_P3']:.6e}, rel {v['rel']:.1e}) = {v['c_pi_km_s']:.2f} km/s")
check("K1", k1ok, f"max rel diff {max(v['rel'] for v in k1rows.values()):.2e}", "< 1e-3 for every row (P3: ~1e-4 c)")
res["K1"] = k1rows

# ==================================================================== K2: dispersion + source from the PN Lagrangian
log("")
log("K2: linear response of the held medium from X3's PN Lagrangian (3D form restricted to the longitudinal line; mu_K = 0)")
t, z = sp.symbols("t z", real=True)
K, gL, Mw, rho0, eps = sp.symbols("K gamma_L M rho_0 epsilon", positive=True)
k, w = sp.symbols("k omega", positive=True)
phi = sp.Function("phi")(t, z)
sig = sp.Function("sigma")(t, z)
Pz = sp.Function("P")(t, z)
rhom = sp.Function("rho_m")(t, z)
Xi = phi - sp.diff(sig, t) + sp.diff(sig, z) ** 2 / 2
Lag = (-sp.diff(phi, z) ** 2 / (2 * K) - rhom * phi + Pz * sp.diff(Xi, z) - K * Mw * Pz ** 2 / 2
       - gL / 2 * sp.diff(Pz, z) ** 2)                 # W(K|P|) linearised: dW/dP = K M P (stiff side)
from sympy.calculus.euler import euler_equations
ELs = euler_equations(Lag, [phi, sig, Pz], [t, z])
f1, s1, p1, m1 = sp.symbols("phi1 sigma1 P1 rhom1")
E = sp.exp(sp.I * (k * z - w * t))
subs_ = {phi: eps * f1 * E, sig: eps * s1 * E, Pz: rho0 * z + eps * p1 * E, rhom: eps * m1 * E}
lin = []
for e_ in ELs:
    ex = e_.lhs.subs(subs_).doit()
    c1 = sp.simplify(sp.diff(ex, eps).subs(eps, 0) / E)
    lin.append(sp.expand(c1))
sol = sp.solve(lin, [f1, s1, p1], dict=True)[0]
drho = sp.simplify(sp.I * k * sol[p1])                          # delta rho_tau = dP/dz
resp = sp.simplify(drho / m1)                                    # delta rho_tau / rho_m (Fourier)
wk2 = K * rho0 * (Mw - 1) + gL * rho0 * k ** 2
r_resp = sp.simplify(resp - K * rho0 / (wk2 - w ** 2))
x3 = json.load(open(os.path.join(RB, "X3_switched_stiffness", "x3_switched_stiffness_results.json")))["B1S"]["omega2_P"]
MLs, MTs, th, muK, r0s = sp.symbols("M_L M_T theta mu_K rho_0")
x3e = sp.sympify(x3, locals={"M_L": MLs, "M_T": MTs, "theta": th, "mu_K": muK, "rho_0": r0s, "K": K, "gamma_L": gL,
                              "k": k})
x3_long = sp.simplify(x3e.subs({muK: 0, th: 0}).subs({MLs: Mw, r0s: rho0}))
den = sp.denom(sp.together(resp))
w2_here = [s_ for s_ in sp.solve(sp.Eq(den, 0), w) if s_.is_positive is not False]
w2_here = sp.simplify(w2_here[0] ** 2) if w2_here else None
r_x3 = sp.simplify(w2_here - x3_long) if w2_here is not None else "no root"
log(f"    response delta rho_tau / rho_m = {resp}")
log(f"    minus K rho0/(omega_k^2 - omega^2) with omega_k^2 = K rho0 (M-1) + gamma_L rho0 k^2: {r_resp}")
log(f"    dispersion omega^2 = {w2_here}; X3 B1-S omega2_P at mu_K = 0, theta = 0: {x3_long}; difference {r_x3}")
check("K2", r_resp == 0 and r_x3 == 0, f"response residual {r_resp}; vs X3 {r_x3}",
      "0 and 0: forced eq. d2rho/dt2 - c_s^2 lap rho + omega_g^2 rho = K rho0 rho_m; matter couples only via phi")
res["K2"] = {"response": str(resp), "omega2": str(w2_here), "X3_longitudinal": str(x3_long)}

# ==================================================================== K3: P3 decoupled pair vs K2 (self-gravity)
log("")
log("K3: P3's decoupled pair (G = D.P, Z = k^2/(K M + gamma_L k^2), mu_K = 0) vs K2")
Gp3 = FM * rho0                                                 # D.P = rho_tau (K D.P = 4 pi G rho_ph)
Zp3 = k ** 2 / (K * Mw + gL * k ** 2)
r3 = sp.simplify(Gp3 * k ** 2 / Zp3 - w2_here - K * rho0)
log(f"    G k^2/Z - omega^2(K2) - K rho0 = {r3}  (the decoupling limit drops self-gravity only)")
check("K3", r3 == 0, f"residual {r3}", "0")
cs2 = sp.simplify(sp.limit(w2_here / k ** 2, k, sp.oo))
log(f"    sound speed c_s^2 = lim omega^2/k^2 = {cs2}; gap omega_g^2 = {sp.simplify(w2_here.subs(k, 0))}")
res["K3"] = {"residual": str(r3), "c_s2": str(cs2)}

# ==================================================================== K5: static coupling G_eff(k)
log("")
log("K5: coupling of a point mass to the medium (linear statics, omega -> 0)")
Lst = sp.symbols("L_star", positive=True)
phi_s = sp.simplify(sp.limit(sol[f1] / m1, w, 0))
geff = sp.simplify((-k ** 2 * phi_s / K).subs(gL, K * Lst ** 2 / 2))
want = (Mw + Lst ** 2 * k ** 2 / 2) / (Mw - 1 + Lst ** 2 * k ** 2 / 2)
r5a = sp.simplify(geff - want)
UN_x15 = K * (Lst ** 2 * k ** 2 + 2) / (Lst ** 2 * k ** 4)
r5b = sp.simplify(geff.subs(Mw, 1) - UN_x15 / (K / k ** 2))
lim_hi = sp.limit(geff, k, sp.oo)
lim_lo = sp.simplify(sp.limit(geff, k, 0))
log(f"    G_eff/G = {geff}; minus (M + L^2k^2/2)/(M - 1 + L^2k^2/2): {r5a}; at M = 1 minus X15 U_N/(K/k^2): {r5b}")
log(f"    limits: k L* -> oo: {lim_hi} (screened: Newtonian coupling); k -> 0: {lim_lo}")
check("K5", r5a == 0 and r5b == 0 and lim_hi == 1 and sp.simplify(lim_lo - Mw / (Mw - 1)) == 0,
      f"residuals {r5a}, {r5b}; limits {lim_hi}, {lim_lo}", "0, 0; 1 and M/(M-1)")
res["K5"] = {"G_eff_over_G": str(geff), "lim_screened": str(lim_hi), "lim_IR": str(lim_lo)}

# ==================================================================== K4: Cherenkov angular integral + prefactor
log("")
log("K4: drag force from the retarded wake (angular delta integral analytic)")
mu, v, wk, Ms = sp.symbols("mu v omega_k M_star", positive=True)
mu0 = wk / (k * v)
fprime = sp.Abs(sp.diff(wk ** 2 - k ** 2 * v ** 2 * mu ** 2, mu)).subs(mu, mu0)
ang = sp.simplify(2 * mu0 / fprime)                              # both roots +-mu0, integrand mu sgn(mu)
r4a = sp.simplify(ang - 1 / (k ** 2 * v ** 2))
# F = -pi M^2 K^2 rho0 int d^3k/(2pi)^3 (k_par/k^2) sgn(k.v) delta(omega_k^2 - (k.v)^2)
pref = sp.simplify(sp.pi * Ms ** 2 * K ** 2 * rho0 / (2 * sp.pi) ** 3 * 2 * sp.pi * k ** 2 * (k / k ** 2) * ang * k)
Gs = sp.symbols("G", positive=True)
r4b = sp.simplify(pref.subs(K, 4 * sp.pi * Gs) - 4 * sp.pi * Gs ** 2 * Ms ** 2 * rho0 / v ** 2)
# numeric: Gaussian-broadened delta
kv, wkv, vv, sg = 3.0, 1.2, 1.0, 2e-3
fnum = lambda m_: m_ * np.sign(m_) * np.exp(-((wkv ** 2 - kv ** 2 * vv ** 2 * m_ ** 2) / sg) ** 2 / 2) / (sg * math.sqrt(2 * math.pi))
num = quad(fnum, -1, 1, points=[-wkv / (kv * vv), wkv / (kv * vv)], limit=400)[0]
r4c = abs(num * kv ** 2 * vv ** 2 - 1)
log(f"    angular integral = {ang} (minus 1/(k^2 v^2): {r4a}); dF/d ln k = {pref} -> with K = 4 pi G minus "
    f"4 pi G^2 M^2 rho0/v^2: {r4b}; Gaussian numeric rel err {r4c:.1e}")
check("K4", r4a == 0 and r4b == 0 and r4c < 1e-3, f"{r4a}, {r4b}, {r4c:.1e}", "0, 0, < 1e-3")
res["K4"] = {"angular": str(ang), "dF_dlnk": str(pref)}

# ==================================================================== K6: dimensions
log("")
log("K6: dimensions of t_loss = v^3/(8 pi G^2 M rho lnL)")
from sympy.physics import units as u
tl = (1 * u.meter / u.second) ** 3 / (8 * sp.pi * (u.gravitational_constant) ** 2 * u.kilogram * u.kilogram / u.meter ** 3)
tls = u.convert_to(tl, u.second)
dim_ok = tls.free_symbols <= {u.second} and tls.has(u.second) and not tls.has(u.meter) and not tls.has(u.kilogram)
log(f"    1 (m/s)^3 / (8 pi G^2 * 1 kg * 1 kg/m^3) = {sp.N(tls, 6)}")
check("K6", dim_ok, f"{sp.N(tls, 4)}", "a pure time")

# ==================================================================== MW input (S3 cache, read-only)
log("")
log("MW held medium: phantom density rho_dyn - rho_b from S3's cached isolated AQUAL solve (McMillan17)")
sys.path.insert(0, os.path.join(RB, "S3_v3_mw_seals"))
import s3_aqual as S
import s3_mw as M3
assert not S.MUTATE
grid = S.Grid(*M3.GRID_MAIN)
mw = {}
k7ok = True
VC_REC = {"canonical": 215.170, "alt": 220.377}
for foot in A0:
    key = f"main{S.TAG}|{foot}|s{1.0:.6f}|eN{0.0:.6f}|"
    fn = os.path.join(S.CACHE, "mw_" + hashlib.sha1(key.encode()).hexdigest()[:16] + ".npz")
    if not os.path.exists(fn):
        log(f"STOP: cached solve {os.path.basename(fn)} absent; this lane never solves or writes into S3")
        sys.exit(2)
    zz = np.load(fn)
    Phi = zz["Phi"]
    PB = {k_: zz["PB_" + k_] for k_ in ("R", "B", "T")}
    rd = grid.lap_density(Phi, PB)
    rb = M3.rho_mcm(grid.RR, grid.ZZ)
    a0u = S.A0[foot]
    rows = {}
    for R in sorted(set(DISC_R + [R0_MW])):
        rph = float(grid.interp2(rd - rb, [R], [0.0])[0]) / 1e9          # Msun/pc^3
        rbb = float(grid.interp2(rb, [R], [0.0])[0]) / 1e9
        vc = float(math.sqrt(grid.vc2(Phi, R)))
        x = vc ** 2 / R / a0u
        rows[R] = {"rho_ph_Msun_pc3": rph, "rho_b_Msun_pc3": rbb, "vc_km_s": vc, "x": x}
    mw[foot] = rows
    vc0 = rows[R0_MW]["vc_km_s"]
    rel = abs(vc0 / VC_REC[foot] - 1)
    k7ok &= rel < 0.01 and rows[R0_MW]["rho_ph_Msun_pc3"] > 0
    log(f"    {foot}: v_c(R0) {vc0:.3f} km/s (record {VC_REC[foot]}, rel {rel:.2e}); "
        f"rho_ph(R0, 0) {rows[R0_MW]['rho_ph_Msun_pc3']:.4f} Msun/pc^3 (rho_b {rows[R0_MW]['rho_b_Msun_pc3']:.4f}); "
        f"x = {rows[R0_MW]['x']:.3f}")
    for R, r_ in rows.items():
        log(f"      R {R:6.3f} kpc: rho_ph {r_['rho_ph_Msun_pc3']:.4f}  v_c {r_['vc_km_s']:.2f}  x {r_['x']:.3f}")
check("K7", k7ok, "v_c(R0) within 1 % of the record and rho_ph(R0) > 0 on both footings", "both")
res["MW"] = {f: {str(R): r_ for R, r_ in rows.items()} for f, rows in mw.items()}

# ==================================================================== K8: k-integral cross-check
log("")
log("K8: Ostriker cross-check of the k-integral (g = 1)")
kmin_t, kmax_t = 1e-20, 1e-9
I = quad(lambda lk: 1.0, math.log(kmin_t), math.log(kmax_t))[0]
r8 = abs(I / math.log(kmax_t / kmin_t) - 1)
check("K8", r8 < 1e-6, f"rel {r8:.1e}", "< 1e-6")


# ==================================================================== the loss times
def lnL_env(kmin, kmax, Lm, Mmin):
    g2 = lambda lk: ((Mmin + Lm ** 2 * math.exp(2 * lk) / 2) / (Mmin - 1 + Lm ** 2 * math.exp(2 * lk) / 2)) ** 2
    a, b = math.log(kmin), math.log(kmax)
    pts = [math.log(math.sqrt(2) / Lm)] if a < math.log(math.sqrt(2) / Lm) < b else None
    return quad(g2, a, b, points=pts, limit=400)[0]


def row(foot, Lpc, R, Mst, v_kms):
    m = mw[foot][R]
    L = Lpc * PC
    rho = m["rho_ph_Msun_pc3"] * MSUN / PC ** 3                 # kg/m^3
    x = m["x"]
    Mmin = 1 + x                                                  # M_T: smallest W-stiffness
    gam = 4 * math.pi * G_SI * L ** 2 / 2                         # gamma_L / (K/G-normalisation): c_s^2 = gam rho
    cs = math.sqrt(FM * gam * rho)
    v = v_kms * 1e3
    Mkg = Mst * MSUN
    Rst = RSUN * Mst ** 0.8
    out = {"foot": foot, "Lstar_pc": Lpc, "R_kpc": R, "M_star": Mst, "v_km_s": v_kms, "rho0_Msun_pc3": m["rho_ph_Msun_pc3"],
           "x": x, "c_s_km_s": cs / 1e3, "Mach": v / cs}
    if v <= cs:
        out.update(t_loss_env_tH=float("inf"), note="subsonic: no emission")
        return out
    wg = math.sqrt(4 * math.pi * G_SI * rho * (Mmin - 1))
    kmin = wg / math.sqrt(v * v - cs * cs)
    racc = 2 * G_SI * Mkg / v ** 2
    rnl = Mkg / (2 * math.pi * L ** 2 * rho)
    base = v ** 3 / (8 * math.pi * G_SI ** 2 * Mkg * rho)        # s, per unit lnLambda
    lnR = math.log(1 / (kmin * Rst))
    lnenv = lnL_env(kmin, 1 / Rst, L, Mmin)
    lnacc = math.log(1 / (kmin * racc))
    lnnl = math.log(1 / (kmin * rnl)) if rnl * kmin < 1 else 0.0
    out.update(omega_g_s=wg, lambda_min_kpc=1 / kmin / KPC, R_star_m=Rst, r_acc_AU=racc / AU, r_nl_AU=rnl / AU,
               lnL_env=lnenv, lnL_Rstar=lnR, lnL_racc=lnacc, lnL_rnl=lnnl,
               t_loss_env_tH=base / lnenv / T_H, t_loss_g1_Rstar_tH=base / lnR / T_H, t_loss_g1_racc_tH=base / lnacc / T_H,
               t_loss_g1_rnl_tH=(base / lnnl / T_H) if lnnl > 0 else float("inf"),
               t_loss_env_rho10_tH=base / 10 / lnenv / T_H)
    return out


log("")
log("Loss times t_loss / t_H (envelope = g^2 = (G_eff/G)^2 at M_T = 1 + x, k_max = 1/R_star; owner frame = MW free fall)")
table = []
for foot in A0:
    for Lpc in LSTARS_PC:
        for vs in SUN_V:
            table.append(dict(row(foot, Lpc, R0_MW, 1.0, vs), body="Sun"))
        for R in DISC_R:
            for Mst in DISC_M:
                table.append(dict(row(foot, Lpc, R, Mst, mw[foot][R]["vc_km_s"]), body=f"disc star {Mst:g} Msun"))
hdr = (f"  {'foot':9s} {'L*':>3s} {'body':18s} {'R':>6s} {'v':>6s} {'rho0':>7s} {'c_s':>6s} {'Mach':>6s} {'lam_min':>7s} "
       f"{'lnL_env':>7s} {'t/tH env':>9s} {'g1,R*':>9s} {'g1,racc':>9s} {'env,rho10':>9s}")
log(hdr)
for r_ in table:
    log(f"  {r_['foot']:9s} {r_['Lstar_pc']:3d} {r_['body']:18s} {r_['R_kpc']:6.2f} {r_['v_km_s']:6.1f} "
        f"{r_['rho0_Msun_pc3']:7.4f} {r_['c_s_km_s']:6.3f} {r_['Mach']:6.1f} {r_.get('lambda_min_kpc', 0):7.2f} "
        f"{r_.get('lnL_env', 0):7.2f} {r_['t_loss_env_tH']:9.3e} {r_.get('t_loss_g1_Rstar_tH', 0):9.3e} "
        f"{r_.get('t_loss_g1_racc_tH', 0):9.3e} {r_.get('t_loss_env_rho10_tH', 0):9.3e}")
res["table"] = table

# Sun's own screened neighbourhood (I5)
log("")
log("Pair speed in the Sun's own neighbourhood (I5)")
sunn = {}
for foot in A0:
    for Lpc in LSTARS_PC:
        L = Lpc * PC
        rho = mw[foot][R0_MW]["rho_ph_Msun_pc3"] * MSUN / PC ** 3
        rnl = MSUN / (2 * math.pi * L ** 2 * rho)
        cgal = math.sqrt(FM * 2 * math.pi * G_SI * L ** 2 * rho)
        d = {"c_pi_v3s_1AU_km_s": math.sqrt(FM * GMSUN / AU) / 1e3, "c_pi_v3s_at_r_nl_km_s": math.sqrt(FM * GMSUN / rnl) / 1e3,
             "r_nl_AU": rnl / AU, "c_pi_Zstar_capped_km_s": cgal / 1e3, "r_sonic_v230_AU": GMSUN / (230e3) ** 2 / AU,
             "r_sonic_v230_Rsun": GMSUN / (230e3) ** 2 / RSUN}
        sunn[f"{foot}|{Lpc}pc"] = d
        log(f"    {foot} {Lpc} pc: v3s hedgehog c_pi = sqrt(GM/r): {d['c_pi_v3s_1AU_km_s']:.2f} km/s at 1 AU, "
            f"{d['c_pi_v3s_at_r_nl_km_s']:.3f} km/s at r_nl = {d['r_nl_AU']:.0f} AU; Z* (R1 cap D.P <= rho_d) "
            f"c_pi = {d['c_pi_Zstar_capped_km_s']:.3f} km/s beyond r_nl; c_pi = 230 km/s only inside "
            f"{d['r_sonic_v230_Rsun']:.2f} R_sun")
res["sun_neighbourhood"] = sunn

# ==================================================================== verdict
log("")
env_min = min(r_["t_loss_env_tH"] for r_ in table)
acc_min = min(r_.get("t_loss_g1_racc_tH", float("inf")) for r_ in table)
per = {}
for foot in A0:
    for Lpc in LSTARS_PC:
        sel = [r_ for r_ in table if r_["foot"] == foot and r_["Lstar_pc"] == Lpc]
        per[f"{foot}|{Lpc}pc"] = {"min_env_tH": min(r_["t_loss_env_tH"] for r_ in sel),
                                  "min_Sun_env_tH": min(r_["t_loss_env_tH"] for r_ in sel if r_["body"] == "Sun")}
if all(r_["t_loss_env_tH"] > 10 for r_ in table):
    verdict = "PASS"
elif any(r_["t_loss_env_tH"] < 10 and r_.get("t_loss_g1_racc_tH", float("inf")) < 10 for r_ in table):
    verdict = "FAIL"
else:
    verdict = "UNDECIDED"
for k_, v_ in per.items():
    log(f"  {k_:16s}: min t_loss/t_H (envelope) all rows {v_['min_env_tH']:.3e}; Sun {v_['min_Sun_env_tH']:.3e}")
log(f"VERDICT (frozen rule): {verdict}  (min envelope t_loss/t_H {env_min:.3e}; min g=1, r_acc {acc_min:.3e})")
res["verdict"] = verdict
res["per_cell"] = per
npass = sum(ok for _, ok in checks)
allok = npass == len(checks)
log(f"Checks: {npass}/{len(checks)} PASS; exit {0 if allok else 1}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
log(f"run {time.time() - T0:.1f} s, peak RSS {rss:.3f} GB")
res["n_pass"], res["n_checks"] = npass, len(checks)
open(OUT, "w").write("\n".join(lines) + "\n")
json.dump(res, open(JSN, "w"), indent=1, default=str)
sys.exit(0 if allok else 1)
