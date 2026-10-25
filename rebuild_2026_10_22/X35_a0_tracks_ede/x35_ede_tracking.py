"""X35_a0_tracks_ede: can a0(z) = kappa c sqrt(G rho_DE(z)), tracking an early-dark-energy (EDE) component, switch the law
on at recombination and supply steady (non-oscillating) potential wells without a separate cold component?

The owner's idea. Frozen criteria: FROZEN_CRITERIA.md (02848d0330); AMENDMENT_A1.md (ODE potential equation, drag redshift anchor, K1 sign). kappa = 1/2 FITTED; footings never pooled; EDE
parameters are literature values (PROVISIONAL), never fitted. Not theory closed.

Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x35_ede_tracking.py
MUTATE twin:  X35_MUTATE=1 ... (named checks M-A..M-D must FAIL; exit 1).
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("X35_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
OUT, CHECKS, MCHECKS = [], [], {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val=""):
    CHECKS.append((name, bool(ok), str(val))); P(f"  [{'PASS' if ok else 'FAIL'}] {name} {val}")


# ---------------- constants and the record's ruler cosmology (CFG689) ----------------
C = 2.99792458e8; G = 6.67430e-11; MPC = 3.0856775814913673e22
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
H = 0.677; OMB = 0.02236; OMC = 0.1202; TCMB = 2.7255; NEFF = 3.046
OMG = 2.47282e-5 * (TCMB / 2.7255) ** 4
OMNU = OMG * 0.22711 * NEFF
OMR = OMG + OMNU
HC = 100.0 / 299792.458          # H100 / c in Mpc^-1
AS, NS, KSTAR = 2.1e-9, 0.965, 0.05   # PROVISIONAL (Planck 2018)
A_REC = 1.0 / 1101.0

MODELS = {"M-LCDM": OMC, "M-NATIVE": 0.0}

# literature EDE points (PROVISIONAL, transcribed; never fitted). p = 3(1 + w_n); n = 3 -> w 1/2 -> p 4.5; n = inf -> p 6.
LIT = {
    "L1 Smith+20 (f 0.122, log zc 3.562)": (0.122, 10 ** 3.562),
    "L2 Poulin+19 (f ~0.08, zc ~5000)": (0.08, 5000.0),
    "L3 Hill+20 bound (f 0.087, zc 3500)": (0.087, 3500.0),
    "L4a generic (f 0.10, zc 3000)": (0.10, 3000.0),
    "L4b generic (f 0.10, zc 5000)": (0.10, 5000.0),
}
PEXP = {"n3 (a^-4.5)": 4.5, "ninf (a^-6)": 6.0}
if MUT:   # M-A / M-B: EDE switched off
    LIT = {k: (0.0, v[1]) for k, v in LIT.items()}


class Bg:
    """Background in omega units (rho / rho_crit,100). EDE fluid: rho = 2 rho(a_c) / (1 + (a/a_c)^p)."""

    def __init__(self, omc, f=0.0, zc=3000.0, p=4.5):
        self.omc = omc; self.oml = H * H - OMB - omc - OMR
        self.ac = 1.0 / (1.0 + zc); self.p = p; self.f = f
        oth = self.others(self.ac)
        self.rc = f / (1.0 - f) * oth if f > 0 else 0.0

    def others(self, a):
        return (OMB + self.omc) / a ** 3 + OMR / a ** 4 + self.oml

    def ede(self, a):
        return 2.0 * self.rc / (1.0 + (a / self.ac) ** self.p) if self.rc > 0 else 0.0

    def tot(self, a):
        return self.others(a) + self.ede(a)

    def rde(self, a):
        return self.oml + self.ede(a)

    def a0ratio(self, a):
        return math.sqrt(self.rde(a) / self.rde(1.0))

    def calH(self, a):   # conformal Hubble rate in Mpc^-1
        return a * HC * math.sqrt(self.tot(a))


# ---------------- perturbation ODE (conformal Newtonian, Phi = Psi, tight coupling, nu fluid) ----------------
KGRID = np.logspace(-3, 0, 41)
ZSAVE = np.unique(np.concatenate([np.logspace(math.log10(300), 5, 60), [1100.0]]))[::-1]
LNA_SAVE = np.log(1.0 / (1.0 + ZSAVE))


def evolve(bg, k):
    def rhs(lna, y):
        a = math.exp(lna); Hc = bg.calH(a); tot = bg.tot(a)
        Ob = OMB / a ** 3 / tot; Oc = bg.omc / a ** 3 / tot; Og = OMG / a ** 4 / tot; On = OMNU / a ** 4 / tot
        phi, dc, thc, dg, th, db, dn, thn = y
        R = 3.0 * OMB * a / (4.0 * OMG)
        # 00 Einstein equation (stable super-horizon): k^2 phi + 3 Hc (phi' + Hc phi) = -(3/2) Hc^2 sum Omega_i delta_i
        dphi = -Hc * phi - (k * k * phi + 1.5 * Hc * Hc * (Oc * dc + Ob * db + Og * dg + On * dn)) / (3.0 * Hc)
        ddc = -thc + 3 * dphi; dthc = -Hc * thc + k * k * phi
        ddg = -(4.0 / 3.0) * th + 4 * dphi; ddb = -th + 3 * dphi
        dth = (-Hc * R * th + k * k * dg / 4.0) / (1.0 + R) + k * k * phi
        ddn = -(4.0 / 3.0) * thn + 4 * dphi; dthn = k * k * dn / 4.0 + k * k * phi
        return np.array([dphi, ddc, dthc, ddg, dth, ddb, ddn, dthn]) / Hc
    ai = 1e-8; tau = ai / bg.calH(ai)
    y0 = [1.0, -1.5, 0.5 * k * k * tau, -2.0, 0.5 * k * k * tau, -1.5, -2.0, 0.5 * k * k * tau]
    sol = solve_ivp(rhs, (math.log(ai), LNA_SAVE[-1]), y0, t_eval=LNA_SAVE, method="DOP853", rtol=1e-7, atol=1e-11)
    assert sol.success, sol.message
    return sol.y


def zeta(k):
    return math.sqrt(AS * (k / KSTAR) ** (NS - 1.0))


def fields(bg):
    """|Psi|(k, z) per ln k (normalised to zeta), photon amplitude and R on the save grid."""
    psi = np.zeros((len(KGRID), len(ZSAVE))); amp = np.zeros_like(psi)
    for i, k in enumerate(KGRID):
        y = evolve(bg, k); zk = (2.0 / 3.0) * zeta(k)
        psi[i] = np.abs(y[0]) * zk
        a = 1.0 / (1.0 + ZSAVE); R = 3.0 * OMB * a / (4.0 * OMG); cs = 1.0 / np.sqrt(3.0 * (1.0 + R))
        amp[i] = np.sqrt(y[3] ** 2 + (4.0 * y[4] / (3.0 * cs * k)) ** 2) * zk
    return psi, amp


def xfield(psi, bg, a0):
    """x(k, z) = k_phys |Psi| c^2 / a0(z)."""
    a = 1.0 / (1.0 + ZSAVE)
    kphys = KGRID[:, None] / a[None, :] / MPC
    a0z = a0 * np.array([bg.a0ratio(aa) for aa in a])
    return kphys * psi * C * C / a0z[None, :]


ACOUS = (KGRID >= 0.01 - 1e-12) & (KGRID <= 0.3 + 1e-12)
IZ1100 = int(np.argmin(np.abs(ZSAVE - 1100.0)))


def xstats(x):
    xmax = x[ACOUS].max(axis=0)
    lk = np.log(KGRID)
    xrms = np.sqrt(np.trapz(x ** 2, lk, axis=0))
    return xmax, xrms


# ---------------- sound horizon ----------------
def zdrag(omb, omm):
    b1 = 0.313 * omm ** -0.419 * (1 + 0.607 * omm ** 0.674); b2 = 0.238 * omm ** 0.223
    return 1291 * omm ** 0.251 / (1 + 0.659 * omm ** 0.828) * (1 + b1 * omb ** b2)


ZD_PLANCK = 1059.94   # Planck 2018 drag redshift (PROVISIONAL); AMENDMENT A1.2 anchor for EH98's z_d scale


def rdrag(bg):
    zd = zdrag(OMB, OMB + bg.omc) * ZD_PLANCK / zdrag(0.02236, 0.1426)
    f = lambda lna: (math.exp(lna) / math.sqrt(3.0 * (1.0 + 3.0 * OMB * math.exp(lna) / (4.0 * OMG)))) / (math.exp(lna) ** 2 * HC * math.sqrt(bg.tot(math.exp(lna))))
    val, _ = quad(f, math.log(1e-12), math.log(1.0 / (1.0 + zd)), limit=400)
    return val, zd


RES = {"mutate": MUT}
P(f"X35_a0_tracks_ede  mode={'MUTATE' if MUT else 'normal'}")
P(f"ruler cosmology: omega_b {OMB} omega_c {OMC} h {H} omega_r {OMR:.4e} (N_eff {NEFF}); A_s {AS} n_s {NS} (PROVISIONAL)")

# ================= STEP 0 =================
P("\n=== STEP 0 (stop rule) ===")
bg0 = Bg(OMC)
psi0, amp0 = fields(bg0)
lk = np.log(KGRID)
S0 = {}
for fn, a0 in FOOT.items():
    x = xfield(psi0, bg0, a0)
    S0[fn] = float(np.exp(np.interp(math.log(0.05), lk, np.log(x[:, IZ1100]))))
P(f"  record estimator x(k 0.05, z 1100), M-LCDM, Lambda only: canonical {S0['canonical']:.2f}, alt {S0['alt']:.2f}  (record: ~14 / ~11; |Psi| {np.interp(math.log(0.05), lk, psi0[:, IZ1100]):.3e})")
check("S0-1 record x ~ 11-14 at z 1100 within x2 (canonical [7, 28], alt [5.5, 22]) [order-of-magnitude reproduction of an audit estimate]",
      7 <= S0["canonical"] <= 28 and 5.5 <= S0["alt"] <= 22, f"({S0['canonical']:.2f} / {S0['alt']:.2f})")


def R_dec(z, w0=-0.838, wa=-0.62):   # CFG223 verbatim
    return math.sqrt((1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * z / (1.0 + z)))


rd = [R_dec(z) for z in (0, 1, 2, 3)]
check("S0-2 M-DEC R(0,1,2,3) = 1, 0.990, 0.874, 0.775 (+-0.002)", all(abs(u - v) <= 0.002 for u, v in zip(rd, (1, 0.990, 0.874, 0.775))), f"({', '.join(f'{u:.4f}' for u in rd)})")
rdec1100 = R_dec(1100.0)
P(f"  M-DEC a0(1100)/a0(0) = {rdec1100:.4f} -> x(k 0.05, 1100) canonical {S0['canonical'] / rdec1100:.1f}, alt {S0['alt'] / rdec1100:.1f} (DESI w0wa: a0 lower, law more inert)")
J689 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689.json")))
m689 = {k: J689[k]["P1"]["2.33"]["sqrtX_q"][2] for k in ("BAO+SN", "BAO")}
check("S0-3 CFG689 primary sqrtX medians at z* 2.33 read back: 0.909 (BAO+SN), 0.950 (BAO) +-0.002",
      abs(m689["BAO+SN"] - 0.909) <= 0.002 and abs(m689["BAO"] - 0.950) <= 0.002, f"({m689['BAO+SN']:.4f}, {m689['BAO']:.4f})")
rd0, zd0 = rdrag(bg0)
check("S0-4 r_d of the ruler cosmology within 1% of CFG689's 147.07 Mpc", abs(rd0 / 147.0667 - 1) < 0.01, f"({rd0:.2f} Mpc, z_drag {zd0:.1f})")
x1100_lcdm = {fn: xfield(psi0, bg0, a0)[:, IZ1100] for fn, a0 in FOOT.items()}
RES["step0"] = {"x_k005_z1100": S0, "Psi_k005_z1100": float(np.interp(math.log(0.05), lk, psi0[:, IZ1100])),
                "MDEC_R_0123": rd, "MDEC_a0ratio_1100": rdec1100, "cfg689_sqrtX_med_2p33": m689, "r_d_ruler": rd0, "z_drag": zd0}
STOP = not all(ok for n, ok, _ in CHECKS if n.startswith("S0"))
if STOP:
    P("STOP RULE FIRED -> UNDECIDED"); RES["verdict"] = "UNDECIDED (step 0)"

# ================= STEP 1 =================
P("\n=== STEP 1 (magnitude) ===")
bgN = Bg(0.0); psiN, ampN = fields(bgN)
RES["step1"] = {}
zrows = [0.0, 2.33, 300.0, 1100.0, None, 1e5, 4.26e9]
mag_ok_any = False; a0_gt10_any = False
tbl = []
for lname, (f, zc) in LIT.items():
    for pname, p in PEXP.items():
        key = f"{lname} | {pname}"; row = {}
        okall = True
        for mname, omc in MODELS.items():
            bg = Bg(omc, f, zc, p)
            psi, amp = fields(bg)
            r = {"a0ratio": {}}
            for z in zrows:
                zz = zc if z is None else z
                r["a0ratio"]["z_c" if z is None else f"{z:g}"] = bg.a0ratio(1.0 / (1.0 + zz))
            for fn, a0 in FOOT.items():
                x = xfield(psi, bg, a0); xmax, xrms = xstats(x)
                deep = ZSAVE[(xmax < 1)]
                r[fn] = {"xmax_1100": float(xmax[IZ1100]), "xrms_1100": float(xrms[IZ1100]),
                         "x_k005_1100": float(np.exp(np.interp(math.log(0.05), lk, np.log(x[:, IZ1100])))),
                         "z_window_xmax_lt1": [float(deep.min()), float(deep.max())] if len(deep) else None}
                okall &= (xmax[IZ1100] < 1) and (xrms[IZ1100] < 1)
            r["rho_ede_over_tot_1100"] = bg.ede(A_REC) / bg.tot(A_REC)
            r["rd"] = rdrag(bg)[0]
            row[mname] = r
        if lname[:2] in ("L1", "L2", "L3", "L4"):
            mag_ok_any |= okall
            a0_gt10_any |= row["M-LCDM"]["a0ratio"]["1100"] > 10
        RES["step1"][key] = row
        lc, na = row["M-LCDM"], row["M-NATIVE"]
        P(f"  {key}")
        P(f"    a0/a0(0) [M-LCDM]: z0 {lc['a0ratio']['0']:.7f}  z2.33 {lc['a0ratio']['2.33']:.6f}  z300 {lc['a0ratio']['300']:.3g}  z1100 {lc['a0ratio']['1100']:.4g}  z_c {lc['a0ratio']['z_c']:.4g}  z1e5 {lc['a0ratio']['100000']:.4g}  BBN {lc['a0ratio']['4.26e+09']:.4g}")
        P(f"    a0/a0(0) [M-NATIVE] z1100 {na['a0ratio']['1100']:.4g}; rho_EDE/rho_tot(1100) LCDM {lc['rho_ede_over_tot_1100']:.3g} NATIVE {na['rho_ede_over_tot_1100']:.3g}")
        for mname in MODELS:
            rr = row[mname]
            P(f"    {mname:8s} x_max(1100) can {rr['canonical']['xmax_1100']:.3g} alt {rr['alt']['xmax_1100']:.3g} | x_rms can {rr['canonical']['xrms_1100']:.3g} alt {rr['alt']['xrms_1100']:.3g} | window x_max<1 (can) z {rr['canonical']['z_window_xmax_lt1']} | r_d {rr['rd']:.2f}")
        tbl.append((key, lc["a0ratio"]["1100"], lc["canonical"]["xmax_1100"], na["canonical"]["xmax_1100"], lc["canonical"]["xrms_1100"], na["canonical"]["xrms_1100"]))
# no-EDE baselines
base = {}
for mname, (bg, psi) in {"M-LCDM": (bg0, psi0), "M-NATIVE": (bgN, psiN)}.items():
    base[mname] = {}
    for fn, a0 in FOOT.items():
        xmax, xrms = xstats(xfield(psi, bg, a0))
        base[mname][fn] = {"xmax_1100": float(xmax[IZ1100]), "xrms_1100": float(xrms[IZ1100]), "xmin_acoustic_1100": float(xfield(psi, bg, a0)[ACOUS, IZ1100].min())}
    base[mname]["rd"] = rdrag(bg)[0]
RES["step1"]["no-EDE baseline"] = base
P(f"  no-EDE baseline x at z 1100 (acoustic k): M-LCDM can min {base['M-LCDM']['canonical']['xmin_acoustic_1100']:.3g} max {base['M-LCDM']['canonical']['xmax_1100']:.3g} rms {base['M-LCDM']['canonical']['xrms_1100']:.3g}; M-NATIVE can min {base['M-NATIVE']['canonical']['xmin_acoustic_1100']:.3g} max {base['M-NATIVE']['canonical']['xmax_1100']:.3g}")
# context grid (a0 ratio only; x scaled from the no-EDE M-LCDM field, labelled approximate)
grid = {}
for f in (0.05, 0.087, 0.122):
    for zc in (3000.0, 3650.0, 5000.0):
        for pname, p in PEXP.items():
            bg = Bg(OMC, 0.0 if MUT else f, zc, p); rr = bg.a0ratio(A_REC)
            grid[f"f {f} zc {zc:g} {pname}"] = {"a0ratio_1100": rr, "xmax_can_scaled": base["M-LCDM"]["canonical"]["xmax_1100"] / rr}
RES["step1"]["context_grid"] = grid
P("  context grid a0(1100)/a0(0): " + "; ".join(f"{k}: {v['a0ratio_1100']:.3g}" for k, v in grid.items() if "n3" in k))
MAG_OK = mag_ok_any
RES["MAG_OK"] = MAG_OK
P(f"  MAG_OK = {MAG_OK}")
MCHECKS["M-A MAG_OK"] = MAG_OK
MCHECKS["M-B a0(1100)/a0(0) > 10 for some literature point"] = a0_gt10_any

# late-time checks (K5)
lt23 = 0.0
for lname, (f, zc) in LIT.items():
    for pname, p in PEXP.items():
        b1, b0 = Bg(OMC, f, zc, p), Bg(OMC)
        lt23 = max(lt23, abs(b1.a0ratio(1 / 3.33) / b0.a0ratio(1 / 3.33) - 1))
sh0 = max(abs(math.sqrt((Bg(OMC, f, zc, p).oml + Bg(OMC, f, zc, p).ede(1.0)) / Bg(OMC).oml) - 1) for (f, zc) in LIT.values() for p in PEXP.values())
check("K5a a0 today unchanged by EDE: sqrt(rho_DE(0)/rho_L) - 1 < 1e-4", sh0 < 1e-4, f"({sh0:.2e})")
check("K5b direct EDE shift of a0 at z 2.33 < 1e-3 (CFG689 band untouched directly)", lt23 < 1e-3, f"({lt23:.2e})")

# indirect: CFG689's ruler (ESTIMATE, flat Lambda at CFG689's omega_m)
OMM689 = 0.1426
s_rd = RES["step1"]["L1 Smith+20 (f 0.122, log zc 3.562) | n3 (a^-4.5)"]["M-LCDM"]["rd"] / rd0


def sqrtX_shift(z, s):
    wt = lambda zz: OMM689 * (1 + zz) ** 3 + (H * H - OMM689)
    de = lambda zz: wt(zz) / s ** 2 - OMM689 * (1 + zz) ** 3
    return math.sqrt(de(z) / de(0.0)) if de(z) > 0 else float("nan")


RES["cfg689_ruler_estimate"] = {"r_d_ratio_L1": s_rd, "sqrtX_2p33_noEDE": sqrtX_shift(2.33, 1.0), "sqrtX_2p33_EDE_ruler": sqrtX_shift(2.33, s_rd),
                                "sqrtX_1p0_EDE_ruler": sqrtX_shift(1.0, s_rd)}
P(f"  CFG689 ruler ESTIMATE (L1 n3, r_d ratio {s_rd:.4f}; flat Lambda at omega_m {OMM689}): sqrtX(2.33) {sqrtX_shift(2.33, 1.0):.3f} -> {sqrtX_shift(2.33, s_rd):.3f}; sqrtX(1.0) -> {sqrtX_shift(1.0, s_rd):.3f}")

# ================= STEP 2 =================
P("\n=== STEP 2 (decisive physics) ===")
# D1: no background khronon charge
t, xs, eps = sp.symbols("t x epsilon", real=True)
rho = sp.Function("rho")(t, xs); v = sp.Function("v")(t, xs)
cont = sp.diff(rho, t) + sp.diff(rho * v, xs)
d1a = sp.simplify(cont.subs(rho, 0).doit())
Xi = sp.Function("Xi")(xs); J = sp.Function("J")(xs)
d1b = sp.simplify(sp.diff(Xi * J * sp.diff(Xi, xs), xs) - (J * sp.diff(Xi, xs) ** 2 + Xi * sp.diff(J * sp.diff(Xi, xs), xs)))
# numeric energy identity on a periodic 1-D field with the true J_Y = -1/(1+|Xi'|/a0), a0 = 1
uu = np.linspace(0, 2 * np.pi, 4097)[:-1]; du = uu[1] - uu[0]; kk = np.fft.fftfreq(len(uu), d=du) * 2 * np.pi
Xn = 0.3 * np.sin(uu) + 0.1 * np.cos(2 * uu + 0.4); dX = np.real(np.fft.ifft(1j * kk * np.fft.fft(Xn)))
JY = -1.0 / (1.0 + np.abs(dX)); MU2 = 0.2
lhs = np.sum(Xn * (np.real(np.fft.ifft(1j * kk * np.fft.fft(JY * dX))) + MU2 * Xn)) * du
rhs_ = np.sum(dX ** 2 / (1 + np.abs(dX)) + MU2 * Xn ** 2) * du
d1c = abs(lhs - rhs_) / rhs_   # AMENDMENT A1.3: frozen sign (+)
check("K1 D1: rho_tau = 0 solves khronon continuity exactly; product rule residual 0; energy identity int Xi[(J_Y Xi')' + mu^2 Xi] = +int[Xi'^2/(1+x) + mu^2 Xi^2] (periodic)",
      d1a == 0 and d1b == 0 and d1c < 1e-8, f"(cont {d1a}, product {d1b}, identity rel {d1c:.1e})")


def solve_hold(S, mu2=MU2, it=4000):
    """(d^2 - mu^2) Xi = S + d[mu(x) dXi], a0 = 1; Picard (as L1). Returns Xi and convergence."""
    Xi_ = 0.05 * np.sin(3 * uu + 0.7) + 0.02 * np.cos(uu)   # non-zero start
    for n in range(it):
        dXi = np.real(np.fft.ifft(1j * kk * np.fft.fft(Xi_))); x_ = np.abs(dXi); mu = x_ / (1 + x_)
        rhs = S + np.real(np.fft.ifft(1j * kk * np.fft.fft(mu * dXi)))
        new = np.real(np.fft.ifft(np.fft.fft(rhs) / (-(kk ** 2) - mu2)))
        if np.max(np.abs(new - Xi_)) < 1e-14: Xi_ = new; break
        Xi_ = 0.5 * Xi_ + 0.5 * new
    return Xi_, n


Splant = (4 * math.pi * 0.01 * np.cos(uu)) if MUT else np.zeros_like(uu)   # M-D: planted charge
Xs, nit = solve_hold(-Splant)
xi_max = float(np.max(np.abs(Xs)))
check("K1b D1: with rho_tau = 0 the hold equation's solution from a non-zero start is Xi = 0 (max|Xi| < 1e-10)", xi_max < 1e-10, f"({xi_max:.2e}, {nit} its)")
MCHECKS["M-D Xi == 0"] = xi_max < 1e-10

# D2: kernel
k_, m_, f_, S_, xx = sp.symbols("k m f S x", positive=True)
Xi_k = -S_ / ((1 - f_) * k_ ** 2 + m_ ** 2)
phi_k = -S_ / k_ ** 2
s_expr = sp.simplify((phi_k - Xi_k) / phi_k)
s_target = (m_ ** 2 - f_ * k_ ** 2) / ((1 - f_) * k_ ** 2 + m_ ** 2)
d2a = sp.simplify(s_expr - s_target)
d2b = sp.simplify(sp.limit(s_expr.subs(f_, xx / (1 + xx)), xx, 0) - m_ ** 2 / (k_ ** 2 + m_ ** 2))
d2c = sp.simplify(sp.limit(s_expr.subs(f_, xx / (1 + xx)), xx, sp.oo) - (m_ ** 2 - k_ ** 2) / m_ ** 2)
d2ser = sp.simplify(sp.series(s_expr.subs(f_, xx / (1 + xx)), xx, 0, 2).removeO() - m_ ** 2 / (k_ ** 2 + m_ ** 2))
check("K2 D2: dust self-gravity kernel s = (m^2 - f k^2)/((1-f)k^2 + m^2); x->0 gives m^2/(k^2+m^2) (a0-free); x->inf gives (m^2-k^2)/m^2",
      d2a == 0 and d2b == 0 and d2c == 0, f"(first-order term in x: {d2ser})")
skern = {}
for muK in (0.03, 0.1, 10.0):
    m = muK * A_REC
    skern[f"mu_K {muK} Mpc^-1"] = {f"k {kq}": (m * m) / (kq * kq + m * m) for kq in (0.01, 0.09, 0.3)}
RES["D2_kernel_z1100_xto0"] = skern
P("  D2 kernel at z 1100 in the EDE regime (x -> 0): " + "; ".join(f"{a}: " + ", ".join(f"{b} s={c:.2e}" for b, c in d.items()) for a, d in skern.items()))

# D3: plane-wave AQUAL
y = sp.symbols("y", positive=True)
nu = (1 + sp.sqrt(1 + 4 / y)) / 2
g = y * nu
d3 = sp.simplify(sp.radsimp(g * (g / (1 + g)) - y))
d3n = max(abs(float((g * g / (1 + g) - y).subs(y, yv))) for yv in (1e-6, 1e-3, 0.1, 1, 10, 1e4))
check("K3 D3: exact 1-D AQUAL plane wave mu(g) g = g_N with g = g_N nu(|g_N|), and G(-g_N) = -G(g_N) (odd)", d3 == 0 or d3n < 1e-9, f"(symbolic {d3}, numeric max {d3n:.1e})")


def Gl(s):   # odd law response, a0 = 1
    s = np.asarray(s, float); a = np.abs(s)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(a > 0, np.sign(s) * a * (1 + np.sqrt(1 + 4 / np.where(a > 0, a, 1))) / 2, 0.0)
    return out


UQ = np.linspace(0, 2 * np.pi, 2049)[:-1]


def nubar(yA):   # boost of the Fourier fundamental for a plane wave of Newtonian amplitude yA (in a0)
    if yA <= 0: return 1.0
    return float(np.mean(Gl(yA * np.sin(UQ)) * np.sin(UQ)) * 2 / yA)


# physical parameters at z 1100, M-NATIVE + L1 n3 (the graded point), per footing
bgL1 = Bg(0.0, *LIT["L1 Smith+20 (f 0.122, log zc 3.562)"], 4.5)
psiL1, ampL1 = fields(bgL1)
a = A_REC; Hc = bgL1.calH(a); tot = bgL1.tot(a); Og = OMG / a ** 4 / tot; R = 3 * OMB * a / (4 * OMG); cs2 = 1 / (3 * (1 + R))
osc = {}
for fn, a0f in FOOT.items():
    a0z = a0f * bgL1.a0ratio(a); osc[fn] = {}
    for kq in (0.02, 0.05, 0.09, 0.2):
        Aq = float(np.interp(math.log(kq), lk, ampL1[:, IZ1100]))
        PhiN = 1.5 * Hc * Hc * Og * (1 + R) * Aq / kq ** 2            # Newtonian potential amplitude of the plasma
        yA = (kq / a / MPC) * PhiN * C * C / a0z                        # its acceleration in units of a0(z)
        beta = 6 * Hc * Hc * Og * (1 + R) ** 2 / kq ** 2                # Newtonian gravity / pressure (GR part)
        nb = nubar(yA)
        # tabulate nubar on |delta| in [0,1] for speed
        dgrid = np.linspace(0, 1.5, 601); nbt = np.array([nubar(yA * dd) for dd in dgrid])
        if MUT:   # M-C: law extra replaced by a constant of equal amplitude (CDM-like external well)
            cst = beta * (nb - 1.0); extra = lambda d: cst
        else:
            extra = lambda d: beta * d * (np.interp(abs(d), dgrid, nbt) - 1.0)
        rhs = lambda tt, yy: [yy[1], -yy[0] + beta * yy[0] + extra(yy[0])]
        T = np.linspace(0, 40 * np.pi, 20001)
        sol = solve_ivp(rhs, (0, T[-1]), [1.0, 0.0], t_eval=T, rtol=1e-9, atol=1e-12, method="DOP853")
        d = sol.y[0]; ex = np.array([extra(dd) for dd in d])
        F = abs(np.mean(ex)) / max(np.max(np.abs(ex)), 1e-300)
        Aasym = np.max(d) / abs(np.min(d)) if np.min(d) < 0 else float("inf")
        crosses = bool(np.min(d) < 0)
        # CDM control: constant external well of the same amplitude
        cst2 = beta * (nb - 1.0)
        solc = solve_ivp(lambda tt, yy: [yy[1], -yy[0] + beta * yy[0] + cst2], (0, T[-1]), [1.0, 0.0], t_eval=T, rtol=1e-9, atol=1e-12)
        dc = solc.y[0]; Ac = np.max(dc) / abs(np.min(dc)) if np.min(dc) < 0 else float("inf")
        osc[fn][f"k {kq}"] = {"yA": yA, "beta_GR": beta, "nubar": nb, "beta_eff": beta * nb, "F_law": F, "A_law": Aasym,
                              "law_crosses_zero": crosses, "F_cdm": 1.0, "A_cdm": Ac}
RES["D3_oscillator"] = osc
for fn in FOOT:
    P(f"  D3 oscillator [{fn}] (M-NATIVE + L1 n3, z 1100): " + "; ".join(f"{kq}: y_A {r['yA']:.2e} beta {r['beta_GR']:.2e} boost {r['nubar']:.1f} beta_eff {r['beta_eff']:.3f} F {r['F_law']:.2e} A {r['A_law']:.4f} (CDM A {r['A_cdm']:.3f})" for kq, r in osc[fn].items()))
ref = osc["canonical"]["k 0.09"]; refa = osc["alt"]["k 0.09"]
FLAW = max(ref["F_law"], refa["F_law"])
check("K4 steady fraction at k 0.09 (third peak): F_law < 0.05 both footings; CDM control F 1 with A_cdm > 1.05; |A_law - 1| < 0.02",
      FLAW < 0.05 and min(ref["A_cdm"], refa["A_cdm"]) > 1.05 and max(abs(ref["A_law"] - 1), abs(refa["A_law"] - 1)) < 0.02,
      f"(F {ref['F_law']:.2e} / {refa['F_law']:.2e}; A_law {ref['A_law']:.4f} / {refa['A_law']:.4f}; A_cdm {ref['A_cdm']:.3f})")
MCHECKS["M-C F_law < 0.05"] = FLAW < 0.05

# effective Jeans scale (mean-field, static reading)
jeans = {}
for lname, (f, zc) in LIT.items():
    bg = Bg(0.0, f, zc, 4.5); psi, _ = fields(bg)
    Hc_ = bg.calH(a); Og_ = OMG / a ** 4 / bg.tot(a)
    jeans[lname] = {}
    for fn, a0f in FOOT.items():
        _, xrms = xstats(xfield(psi, bg, a0f)); xN = float(xrms[IZ1100])
        xt = (xN + math.sqrt(xN * xN + 4 * xN)) / 2       # x^2/(1+x) = x_N
        mu = xt / (1 + xt); L = 1 / (1 + xt)
        gl, gh = 1 / (mu * (1 + L)), 1 / mu
        kJ = lambda gg: math.sqrt(6 * Hc_ * Hc_ * Og_ * (1 + R) ** 2 * gg)
        jeans[lname][fn] = {"x_rms_N": xN, "x_true": xt, "Geff_over_G": [gl, gh], "kJ_eff": [kJ(gl), kJ(gh)], "kJ_GR": kJ(1.0)}
RES["jeans_static_reading"] = jeans
for lname, d in jeans.items():
    P(f"  Jeans (static reading, M-NATIVE, n3) {lname}: " + "; ".join(f"{fn} x_N {r['x_rms_N']:.2e} G_eff/G {r['Geff_over_G'][0]:.1f}-{r['Geff_over_G'][1]:.1f} k_J,eff {r['kJ_eff'][0]:.3f}-{r['kJ_eff'][1]:.3f} Mpc^-1 (GR {r['kJ_GR']:.4f})" for fn, r in d.items()))
kJmin = min(r["kJ_eff"][0] for d in jeans.values() for r in d.values())

# classification
COV_STEADY = False          # D1: identically zero extra potential without background charge (K1, K1b)
STATIC_STEADY = (FLAW >= 0.5) and (kJmin < 0.02)
STEADY = COV_STEADY or STATIC_STEADY
OSC = (not STEADY) and FLAW < 0.5
RES["classification"] = {"covariant_D1": "NULL (Xi == 0, no extra potential without khronon charge)" if xi_max < 1e-10 else "NON-NULL",
                         "static_F": FLAW, "kJ_eff_min": kJmin, "STEADY": STEADY, "OSCILLATING": OSC}
P(f"  classification: covariant D1 {RES['classification']['covariant_D1']}; static F {FLAW:.2e}; k_J,eff min {kJmin:.3f} -> STEADY {STEADY}, OSCILLATING {OSC}")

# ================= STEP 3 =================
P("\n=== STEP 3 === " + ("run" if STEADY else "not run (Step 2 not STEADY)"))

# ================= STEP 4 =================
P("\n=== STEP 4 (reported) ===")
zb = 4.26e9; ab = 1 / (1 + zb); st4 = {}
for lname, (f, zc) in LIT.items():
    for pname, p in PEXP.items():
        bg = Bg(OMC, f, zc, p); ratio = bg.ede(ab) / (OMR / ab ** 4)
        st4[f"{lname} | {pname}"] = {"rhoEDE_over_rhor_1MeV": ratio, "dNeff_equiv": ratio * (1 + 0.22711 * NEFF) / 0.22711,
                                    "a0ratio_1MeV": bg.a0ratio(ab), "a0_1MeV_can": FOOT["canonical"] * bg.a0ratio(ab)}
RES["step4_bbn"] = st4
P("  BBN (T 1 MeV): " + "; ".join(f"{k.split(' (')[0]} {k.split('| ')[1]}: rho_EDE/rho_r {v['rhoEDE_over_rhor_1MeV']:.1e}, a0 {v['a0_1MeV_can']:.2e} m/s^2" for k, v in st4.items() if "n3" in k))
rdtab = {"M-LCDM": base["M-LCDM"]["rd"], "M-NATIVE": base["M-NATIVE"]["rd"]}
for k_, r in RES["step1"].items():
    if k_.startswith("L") and "n3" in k_:
        rdtab[f"M-LCDM + {k_.split(' |')[0]}"] = r["M-LCDM"]["rd"]; rdtab[f"M-NATIVE + {k_.split(' |')[0]}"] = r["M-NATIVE"]["rd"]
RES["step4_rd"] = {k: {"r_d": v, "H0_rough": 67.70 * rdtab["M-LCDM"] / v} for k, v in rdtab.items()}
for k_, v in RES["step4_rd"].items():
    P(f"  r_d {k_:40s} {v['r_d']:.2f} Mpc   rough H0 (fixed theta*) {v['H0_rough']:.1f}")
damp = kJmin >= 0.1
RES["step4_damping"] = {"kJ_eff_min": kJmin, "static_reading_reaches_damping_range": damp}
P(f"  damping tail: static-reading k_J,eff min {kJmin:.3f} Mpc^-1 -> {'reaches' if damp else 'below'} the damping range (k >= 0.1)")

# ================= verdict =================
check("K6 ODE sanity: Psi(k 0.001, z 1100)/Psi_init in [0.80, 1.0] (M-LCDM)", 0.80 <= psi0[0, IZ1100] / ((2 / 3) * zeta(1e-3)) <= 1.0, f"({psi0[0, IZ1100] / ((2 / 3) * zeta(1e-3)):.3f})")
if STOP:
    V = "UNDECIDED"
elif not MAG_OK:
    V = "MAGNITUDE INSUFFICIENT"
elif STEADY:
    V = "UNDECIDED (Step 3 not implemented for STEADY)"
elif OSC:
    V = "LAW ACTIVE BUT OSCILLATES WITH BARYONS (covariant sub-case: NULL)"
else:
    V = "UNDECIDED"
RES["verdict"] = V
P(f"\nVERDICT: {V}")
P("kappa = 1/2 FITTED; footings never pooled; EDE parameters literature (PROVISIONAL); not theory closed.")

if MUT:
    P("\nMUTATE named checks (must FAIL):")
    for n_, ok in MCHECKS.items(): P(f"  [{'PASS' if ok else 'FAIL'}] {n_}")
RES["checks"] = [{"name": n, "ok": ok, "val": v_} for n, ok, v_ in CHECKS]
RES["mutate_named"] = MCHECKS
json.dump(RES, open(os.path.join(HERE, f"x35_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"x35_ede_tracking{TAG}.out"), "w").write("\n".join(OUT) + "\n")
nfail = sum(not ok for _, ok, _ in CHECKS)
P(f"checks: {len(CHECKS) - nfail}/{len(CHECKS)} pass")
if MUT:
    sys.exit(1 if not any(MCHECKS.values()) else 2)   # 1 = every named check failed, as required
sys.exit(0 if nfail == 0 else 1)
