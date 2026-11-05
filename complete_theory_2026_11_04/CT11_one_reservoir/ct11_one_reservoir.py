"""CT11 one reservoir: dust phase converting into the dark-energy phase (FROZEN_CRITERIA.md, written first).
Models M1 (Q = Gamma rho_x), M2 (Q = xi H rho_x), M3 (threshold / generalized Chaplygin, natural a_* = 1), M4 (Q = xi H rho_DE).
G5 through vanilla CLASS 3.3.4 + CT3's peak finder; background check on the DESI DR2 BAO table as transcribed in CFG681 and
Pantheon+ shape (diag errors, reported only). No downloads. Run:
OMP_NUM_THREADS=1 nice -n 10 python3 ct11_one_reservoir.py > ct11_one_reservoir.out   (minutes, < 0.5 GB).
kappa = 1/2 FITTED. Adopts nothing; reinstates nothing; no particle."""
import json, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from classy import Class

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
KAPPA = 0.5                                               # FITTED
OL, OL_ERR = 0.666, 0.018; H_LO, H_HI = 0.6722, 0.6856; H_C = 0.5 * (H_LO + H_HI)
OB = 0.0224; OB_LO, OB_HI = 0.0217, 0.0229
w_r = 2.4728e-5 * (1 + 0.22711 * 3.046)
wDE = OL * H_C ** 2; wDE_lo = (OL - OL_ERR) * H_LO ** 2; wDE_hi = (OL + OL_ERR) * H_HI ** 2
Z_REC = 1090.0; A_REC = 1 / (1 + Z_REC)
TARGET = 5.36 * OB                                        # CT3 / RF5 centre; window 4.9-5.4
OUT = {"inputs": {"omega_DE": [wDE, wDE_lo, wDE_hi], "omega_b": OB, "omega_r": w_r, "h": H_C}}
print(f"inputs: omega_DE {wDE:.4f} [{wDE_lo:.4f}, {wDE_hi:.4f}]  omega_b {OB}  omega_r {w_r:.4e}  h {H_C:.4f}")
H_L = np.sqrt(wDE)                                        # de Sitter rate in units of H100 (H_L/H100 = sqrt(omega_DE))
def gam_units(n, wde=wDE):                                # Gamma = n sqrt(G rho_DE) in units of H100: sqrt(3 wde/(8 pi))
    return n * np.sqrt(3 * wde / (8 * np.pi))

# ---------------- M1: Q = Gamma rho_x, onset z_on, rho_DE(z_on) = 0, Lambda_bare = 0 ----------------
def m1_evolve(x_on, g, z_on, wb=OB):
    """y = [omega_x, omega_DE] (physical densities); d/dln a. Returns (omega_x*a^3 at rec, omega_DE(0), x(0), frac converted after rec)."""
    # well-scaled variables: u = ln rho_x, w = rho_DE/rho_x (w = 0 at onset)
    def rhs(lna, y):
        a = np.exp(lna); rx = np.exp(y[0]); H = np.sqrt(wb * a ** -3 + w_r * a ** -4 + rx * (1 + max(y[1], 0)))
        gh = g / H
        return [-3 - gh, gh + y[1] * (3 + gh)]
    la_on = -np.log(1 + z_on)
    s = solve_ivp(rhs, [la_on, 0.0], [np.log(x_on), 0.0], method="LSODA", rtol=1e-10, atol=1e-14, dense_output=True)
    yr = s.sol(np.log(A_REC)); y0 = s.y[:, -1]
    xrec = np.exp(yr[0]) * A_REC ** 3; x0 = np.exp(y0[0])
    conv_after = 1 - x0 / xrec                            # fraction of the dust present at rec converted by today
    return xrec, x0 * y0[1], x0, conv_after
def m1_solve(g, z_on, wde=wDE):
    f = lambda lx: np.log(m1_evolve(np.exp(lx), g, z_on)[1] / wde)
    lx = brentq(f, -250, 60, xtol=1e-12)
    return m1_evolve(np.exp(lx), g, z_on)
M1 = {}
for nm, n in [("kappa (a0/c)", KAPPA), ("de Sitter sqrt(8pi/3)", np.sqrt(8 * np.pi / 3))]:
    for z_on in [3e4, 1e6]:
        g = gam_units(n); xrec, de0, x0, conv = m1_solve(g, z_on)
        key = f"n={n:.4f},z_on={z_on:.0e}"
        M1[key] = {"n": n, "z_on": z_on, "omega_x_rec": xrec, "ratio": xrec / OB, "omega_x_today": x0, "conv_after_rec": conv}
        print(f"M1 Gamma = {nm} = {n:.4f} sqrt(G rho_DE0), z_on {z_on:.0e}: predicted omega_x(rec) {xrec:.3e}  ratio {xrec/OB:.3e}  converted after rec {conv:.3f}")
# the Gamma the CMB window needs (z_on 3e4 and 1e6)
for z_on in [3e4, 1e6]:
    def fn(ln_n):
        g = gam_units(np.exp(ln_n)); return np.log(m1_solve(g, z_on)[0] / TARGET)
    ln_n = brentq(fn, -15 if z_on < 1e5 else -20, 2, xtol=1e-10); n_need = np.exp(ln_n)
    xr, de0, x0, conv = m1_solve(gam_units(n_need), z_on)
    M1[f"needed_z_on={z_on:.0e}"] = {"n_needed": n_need, "Gamma_over_H_L": gam_units(n_need) / H_L, "conv_after_rec": conv}
    print(f"M1 needed for ratio 5.36 at z_on {z_on:.0e}: n = {n_need:.3e} (Gamma/H_Lambda = {gam_units(n_need)/H_L:.3e}); converted after rec {conv:.2e}")
OUT["M1"] = M1

# ---------------- M2: Q = xi H rho_x (analytic) ----------------
def m2_pred(xi, z_on, wde=wDE):
    a_on = 1 / (1 + z_on)
    # rho_x = X1 a^-(3+xi); rho_DE(a) = xi/(3+xi) X1 [a_on^-(3+xi) - a^-(3+xi)]
    X1 = wde * (3 + xi) / xi / (a_on ** -(3 + xi) - 1)
    return X1 * A_REC ** (-(xi)), X1                       # omega_x * a^3 at rec, omega_x today
xrec_half, x0_half = m2_pred(0.5, 3e4)
print(f"M2 (a) onset a -> 0, Lambda_bare = 0: rho_DE(a) = xi/(3+xi)[rho_x(a_on) - rho_x(a)] diverges as a_on -> 0; finite rho_DE0 forces omega_x -> 0")
print(f"M2 (b) xi = kappa = 1/2 (hand choice), z_on 3e4: predicted omega_x(rec) {xrec_half:.3e}  ratio {xrec_half/OB:.3e}")
xi_need = brentq(lambda lx: np.log(m2_pred(np.exp(lx), 3e4)[0] / TARGET), -60, 2)
xi_need = np.exp(xi_need)
xi_need6 = np.exp(brentq(lambda lx: np.log(m2_pred(np.exp(lx), 1e6)[0] / TARGET), -80, 2))
print(f"M2 xi the window needs: {xi_need:.3e} (z_on 3e4), {xi_need6:.3e} (z_on 1e6); converted after rec ~ xi ln(1091) = {xi_need*np.log(1091):.1e}")
OUT["M2"] = {"xi_half_z3e4": {"omega_x_rec": xrec_half, "ratio": xrec_half / OB}, "xi_needed_z3e4": xi_need, "xi_needed_z1e6": xi_need6}

# ---------------- M3: threshold / GCG, natural a_* = 1 ----------------
x_m3 = wDE
print(f"M3 natural a_* = 1 (dust reaches the vacuum it becomes, today): omega_x,early = omega_DE0 = {x_m3:.4f}, ratio {x_m3/OB:.2f} [{wDE_lo/OB_HI:.2f}, {wDE_hi/OB_LO:.2f}]")
print(f"M3 a_* the window needs: a_*^3 = {TARGET/wDE:.4f}, a_* = {(TARGET/wDE)**(1/3):.4f}, z_* = {(wDE/TARGET)**(1/3)-1:.3f} (a free epoch)")
OUT["M3"] = {"omega_x": x_m3, "ratio": x_m3 / OB, "a_star_needed": (TARGET / wDE) ** (1 / 3)}
# ---------------- M4 ----------------
print("M4 Q = xi H rho_DE: rho_DE = rho_seed a^xi (seed an integration constant), dust amount untouched (shift charge): NO PREDICTION; CFG131 |xi| < 0.0275 for flat a0(z)")
OUT["M4"] = {"prediction": None}

# ---------------- G5 ----------------
def peaks(p, base):
    c = Class(); q = dict(base); q.update(p); c.set(q); c.compute()
    cl = c.raw_cl(2200); ll = cl["ell"][2:]; DD = ll * (ll + 1) * cl["tt"][2:]
    pk = [(ll[i], DD[i]) for i in range(5, len(DD) - 5) if DD[i] == DD[i - 5:i + 6].max() and ll[i] > 100][:3]
    c.struct_cleanup(); return pk[2][1] / pk[1][1]
ct3base = {"h": 0.6736, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "YHe": 0.2454, "output": "tCl", "l_max_scalars": 2200}
chk = peaks({"omega_cdm": 0.12}, ct3base)
print(f"CHECK CT3 row omega_c 0.12: H3/H2 {chk:.3f} (CT3 0.992; |d| <= 0.002: {'OK' if abs(chk-0.992) <= 0.002 else 'FAIL'})")
base = dict(ct3base); base.update({"h": H_C, "omega_b": OB})
k1 = "n=0.5000,z_on=3e+04"; k2 = f"n={np.sqrt(8*np.pi/3):.4f},z_on=3e+04"
graded = [("M1_kappa_z3e4", M1[k1]["omega_x_rec"], M1[k1]["conv_after_rec"]),
          ("M1_deSitter_z3e4", M1[k2]["omega_x_rec"], M1[k2]["conv_after_rec"]),
          ("M2_xi_half_z3e4", xrec_half, 0.5 * np.log(1091)),
          ("M3_a_star_1", x_m3, 0.0)]
G5 = {"check": chk}
for nm, wx, conv in graded:
    res = {ns: peaks({"omega_cdm": max(wx, 1e-12), "n_s": ns}, base) for ns in [0.93, 0.9649, 1.0]}
    inwin = [0.969 <= v <= 0.989 for v in res.values()]; ratio = wx / OB
    v = "PASS" if (4.9 <= ratio <= 5.4 and all(inwin)) else ("FAIL" if not any(inwin) else "NO VERDICT")
    apx = "" if (nm.startswith("M3") or conv < 0.01 or wx < 1e-6) else "  [APPROX FAIL: >1 % converted after rec; dust negligible anyway]"
    G5[nm] = {"omega_x": wx, "ratio": ratio, "H3H2": {str(k): x for k, x in res.items()}, "verdict": v}
    print(f"G5 {nm}: omega_x {wx:.3e} ratio {ratio:.3e}  H3/H2 n_s 0.93/0.9649/1.0 = {res[0.93]:.3f}/{res[0.9649]:.3f}/{res[1.0]:.3f}  -> {v}{apx}")
OUT["G5"] = G5

# ---------------- background check ----------------
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = (0.295, 7.942, 0.075)
sn = np.genfromtxt(os.path.join(ROOT, "prep_2026", "sne_lambda", "pantheonplus_full.dat"), names=True, dtype=None, encoding=None)
msk = (sn["IS_CALIBRATOR"] == 0) & (sn["zHD"] > 0.01)
zs, zh, mb, emb = sn["zHD"][msk], sn["zHEL"][msk], sn["m_b_corr"][msk], sn["m_b_corr_err_DIAG"][msk]
def background(wx):
    h = np.sqrt(OB + wx + wDE + w_r)                      # flat closure with the model's own physical densities
    c = Class(); c.set({"h": h, "omega_b": OB, "omega_cdm": max(wx, 1e-12), "N_ur": 3.046, "YHe": 0.2454}); c.compute()
    rd = c.rs_drag(); chi = 0.0
    for (_, z, dm, sdm, dh, sdh, r) in ANISO:
        m = np.array([c.angular_distance(z) * (1 + z) / rd, 1 / c.Hubble(z) / rd]); d = np.array([dm, dh])
        C = np.array([[sdm ** 2, r * sdm * sdh], [r * sdm * sdh, sdh ** 2]]); chi += (d - m) @ np.linalg.solve(C, d - m)
    z = BGS[0]; dv = (z * (c.angular_distance(z) * (1 + z)) ** 2 / c.Hubble(z)) ** (1 / 3) / rd; chi += ((BGS[1] - dv) / BGS[2]) ** 2
    mu = np.array([5 * np.log10((1 + zh[i]) * c.angular_distance(zs[i]) * (1 + zs[i])) for i in range(len(zs))])
    w = 1 / emb ** 2; res = mb - mu; off = np.sum(w * res) / np.sum(w); chisn = np.sum(w * (res - off) ** 2)
    c.struct_cleanup(); return h, rd, chi, chisn
BG = {}
for nm, wx in [("M1_kappa_z3e4", M1[k1]["omega_x_rec"]), ("M1_deSitter_z3e4", M1[k2]["omega_x_rec"]), ("M2_xi_half_z3e4", xrec_half),
               ("M3_a_star_1", x_m3), ("REFERENCE_fitted_omega_x_0.12_not_graded", 0.12)]:
    h, rd, chi, chisn = background(wx)
    v = "" if nm.startswith("REF") else ("PASS" if chi <= 28.3 else "FAIL")
    BG[nm] = {"h_flat": h, "r_d": rd, "chi2_BAO_13": chi, "chi2_SN_diag": chisn, "N_SN": int(msk.sum()), "verdict": v}
    print(f"BG {nm}: h_flat {h:.4f} r_d {rd:.1f} Mpc  chi2 BAO (13) {chi:.1f} -> {v or 'reference'};  SN diag chi2 {chisn:.0f} / {msk.sum()} (reported)")
OUT["background"] = BG
json.dump(OUT, open(os.path.join(HERE, "ct11_one_reservoir.json"), "w"), indent=1, default=float)
