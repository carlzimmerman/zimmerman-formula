"""CFG793: is there a cold-energy -> light portal inside the committed action (no new coupling)?
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg793.py      (CFG793_MUTATE=1: L* = photon reduced wavelength, c_P = c)
Seconds. External inputs provisional (quoted from memory): rho_c = 0.01 Msun/pc^3, local Galactic field 2.1e-10 m/s^2.
"""
import os, json, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp

MUT = os.environ.get("CFG793_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg793{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n")

G = 6.67430e-11; c = 2.99792458e8; mu0 = 1.25663706212e-6; eps0 = 1.0 / (mu0 * c**2)
hbar = 1.054571817e-34; eV = 1.602176634e-19; PC = 3.0857e16; MSUN = 1.989e30
K = 4 * np.pi * G
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
RHO = 0.01 * MSUN / PC**3; U0 = RHO * c**2
G_LOC = 2.1e-10
LSTAR = {"5.75pc": 5.754 * PC, "1kpc": 1000 * PC}
CPS = {"c": c, "1e-3c": 1e-3 * c, "200m/s": 200.0}
EPH = {"optical_2.5eV": 2.5, "native_2.24meV": 2.24e-3}
R = {"lane": "CFG793", "mutate": MUT}
P("CFG793  built-in portal: P <-> photon mixing through -rho Phi_P (EM energy gravitates)" + ("  [MUTATE L*=lambdabar, c_P=c]" if MUT else ""))
P(f"  rho_c c^2 = {U0:.3e} J/m^3 (provisional), K = 4 pi G = {K:.4e}")

# ---------- generic two-mode mixer (energy-flux normalised) ----------
def delta_from_g(g, omega, v1, v2):
    """canonical fields: phi1'' + v1^2 k^2 phi1 = -g phi2, etc. -> flux-normalised mixing rate per metre."""
    return g / (2.0 * omega * np.sqrt(v1 * v2))

def p_analytic(D, q, L):
    Dosc = np.sqrt(q**2 + 4 * D**2)
    return (2 * D / Dosc)**2 * np.sin(Dosc * L / 2)**2

def p_numeric(D, q, L):
    # first-order coupled amplitudes: a1' = -i D a2, a2' = -i (D a1 + q a2)  (q = k1 - k2 mismatch)
    def f(z, y):
        a1 = y[0] + 1j * y[1]; a2 = y[2] + 1j * y[3]
        d1 = -1j * D * a2; d2 = -1j * (D * a1 + q * a2)
        return [d1.real, d1.imag, d2.real, d2.imag]
    s = solve_ivp(f, [0, L], [0, 0, 1, 0], rtol=1e-12, atol=1e-14, method="DOP853")
    return s.y[0, -1]**2 + s.y[1, -1]**2

# couplings (derived in FROZEN_CRITERIA): P-mode g_P = K B sqrt(eps0/I), I = gamma/c_P^2, gamma = K L*^2/2
def g_P(B, Lst, cP):
    I = K * Lst**2 / 2 / cP**2
    return K * B * np.sqrt(eps0 / I)
def delta_P_closed(B, omega, Lst, cP):
    return np.sqrt(2 * K * eps0) * B * np.sqrt(cP / c) / (2 * omega * Lst)
# graviton (linearised GR, + polarisation): L_h = c^2/(32 pi G)(hdot^2 - c^2 (dh)^2) -> phi_h = h c/sqrt(16 pi G)
# L_int = 1/2 h_ij T^ij = -h B0 b/mu0, b = k phi_gam/sqrt(eps0), k = omega/c  => g_h = sqrt(16 pi G) B omega sqrt(eps0)
def g_grav(B, omega):
    return np.sqrt(16 * np.pi * G) * B * omega * np.sqrt(eps0)

# ---------- K2: Gertsenshtein ----------
om1 = 2.5 * eV / hbar
Dg = delta_from_g(g_grav(1.0, om1), om1, c, c)
Pg_11 = (Dg * 1.0)**2
Pg_std = 4 * np.pi * G * 1.0**2 * 1.0**2 / (mu0 * c**4)
k2a = abs(Pg_11 / Pg_std - 1); k2b = abs(Pg_11 / 8.3e-38 - 1)
K2 = k2a < 1e-10 and k2b < 0.05
P(f"K2 graviton: mixer P(1T,1m) = {Pg_11:.4e}; 4piG B^2L^2/(mu0 c^4) = {Pg_std:.4e} (rel {k2a:.1e}); vs 8.3e-38 lit (rel {k2b:.3f}) -> {'PASS' if K2 else 'FAIL'}")

# ---------- K1: numeric vs analytic ----------
k1 = []
for D, q, L in [(1e-3, 0.0, 300.0), (1e-3, 5e-3, 2000.0), (2e-2, 1e-2, 400.0)]:
    pa, pn = p_analytic(D, q, L), p_numeric(D, q, L)
    k1.append(abs(pn / pa - 1))
K1 = max(k1) < 1e-6
P(f"K1 ODE vs analytic: max rel {max(k1):.2e} -> {'PASS' if K1 else 'FAIL'}")

# ---------- K3: dimension route ----------
k3 = max(abs(delta_from_g(g_P(45, om1, ), om1, c, cp) / delta_P_closed(45, om1, LSTAR["5.75pc"], cp) - 1)
         if False else abs(delta_from_g(g_P(45, LSTAR["5.75pc"], cp), om1, c, cp) / delta_P_closed(45, om1, LSTAR["5.75pc"], cp) - 1)
         for cp in CPS.values())
K3 = k3 < 1e-12
P(f"K3 (g,I) route vs closed form: max rel {k3:.1e} -> {'PASS' if K3 else 'FAIL'}")
R["controls"] = {"K1": K1, "K1_maxrel": max(k1), "K2": K2, "K2_rel_std": k2a, "K2_rel_lit": k2b, "K3": K3, "K3_rel": k3}

# ---------- vacuum gap from W_rem at the local field (each footing) ----------
def gap(a0, Lst, cP, g_tot=G_LOC):
    gN = g_tot**2 / (g_tot + a0); u = g_tot - gN            # polarisation field u = K|P| = g - g_N (simple mu)
    W2 = K * (2 * u * a0 - u**2) / (a0 - u)**2               # d^2 W_rem / dP^2
    I = K * Lst**2 / 2 / cP**2
    return np.sqrt(W2 / I), u

# ---------- Q1: mixing ----------
P("\nQ1  P-wave -> photon conversion (phase matching incl. W_rem gap at the local field)")
cases = [(10, 1), (10, 10), (45, 1), (45, 10), (45, 100), (1e10, 1e4)]
Q1 = []; lab_max = 0.0; ratio_rows = []
for en, E in EPH.items():
    om = E * eV / hbar; lam_bar = c / om
    for lsn, Lst0 in LSTAR.items():
        Lst = lam_bar if MUT else Lst0
        for cpn, cP0 in CPS.items():
            cP = c if MUT else cP0
            for fn, a0 in FOOT.items():
                wg, u = gap(a0, Lst, cP)
                kP = np.sqrt(max(om**2 - wg**2, 0)) / cP
                q = om / c - kP
                for B, L in cases:
                    Dp = delta_from_g(g_P(B, Lst, cP), om, c, cP)
                    Dgr = delta_from_g(g_grav(B, om), om, c, c)
                    pP = p_analytic(Dp, q, L); pG = (Dgr * L)**2
                    row = dict(photon=en, Lstar=lsn, cP=cpn, footing=fn, B=B, L=L, P_P=pP, P_grav=pG,
                               ratio_amp=Dp / Dgr, gap_rad_s=wg, q_per_m=q)
                    Q1.append(row)
                    if B <= 45: lab_max = max(lab_max, pP)
    # predicted ratio check
    for lsn, Lst0 in LSTAR.items():
        Lst = lam_bar if MUT else Lst0
        for cpn, cP0 in CPS.items():
            cP = c if MUT else cP0
            pred = np.sqrt(cP / c) * lam_bar / Lst / np.sqrt(2)
            got = delta_from_g(g_P(1, Lst, cP), om, c, cP) / delta_from_g(g_grav(1, om), om, c, c)
            ratio_rows.append(dict(photon=en, Lstar=lsn, cP=cpn, pred=pred, got=got))
P("  amplitude ratio Delta_P/Delta_grav (pred = sqrt(c_P/c) lambdabar/(sqrt2 L*)):")
for r in ratio_rows:
    P(f"    {r['photon']:15s} L*={r['Lstar']:6s} c_P={r['cP']:7s}  got {r['got']:.3e}  pred {r['pred']:.3e}")
P("  best cases (c_P = c, L* = 5.75 pc, canonical):")
for r in Q1:
    if r["cP"] == "c" and r["Lstar"] == "5.75pc" and r["footing"] == "canonical":
        P(f"    {r['photon']:15s} B={r['B']:.0e} T L={r['L']:.0e} m  P_P = {r['P_P']:.2e}   (Gertsenshtein {r['P_grav']:.2e}; gap {r['gap_rad_s']:.1e} rad/s)")
P("  c_P < c (phase mismatch), optical, 45 T, 100 m, L* 5.75 pc:")
for r in Q1:
    if r["photon"].startswith("optical") and r["B"] == 45 and r["L"] == 100 and r["Lstar"] == "5.75pc":
        P(f"    c_P={r['cP']:7s} {r['footing']:9s} P_P = {r['P_P']:.2e}  coherence length pi/|q| = {(np.pi/abs(r['q_per_m'])) if r['q_per_m'] else float('inf'):.2e} m")
mag = max(r["P_P"] for r in Q1 if r["B"] == 1e10)
q1_class = "GRAVITATIONALLY SUPPRESSED" if lab_max < 1e-30 else "NOT SUPPRESSED below 1e-30"
P(f"  max lab P_P = {lab_max:.2e} (log10 {np.log10(lab_max):.1f}); magnetar max {mag:.2e}  -> Q1: {q1_class}")
R["Q1"] = {"class": q1_class, "lab_max": lab_max, "magnetar_max": mag, "ratio_rows": ratio_rows,
           "rows": Q1}

# ---------- Q2: static field ----------
P("\nQ2  static ambient P: conservative gravity + cold-mass continuity")
# (a) non-symmetric bounded static clump (two Plummer spheres), real trajectory: net KE change after crossing
def acc(x):
    a = np.zeros(3)
    for M, b, x0 in [(1e5 * MSUN, 0.3 * PC, np.array([0, 0.2 * PC, 0])), (4e4 * MSUN, 0.1 * PC, np.array([0.5 * PC, -0.1 * PC, 0.05 * PC]))]:
        d = x - x0; a += -G * M * d / (d @ d + b * b)**1.5
    return a
v0 = 2.0e4
def f(t, y): return np.concatenate([y[3:], acc(y[:3])])
y0 = np.array([-40 * PC, 0.05 * PC, 0, v0, 0, 0]); T = 80 * PC / v0
s = solve_ivp(f, [0, T], y0, rtol=1e-11, atol=1e-3, method="DOP853", dense_output=True)
ts = np.linspace(0, T, 4001); ke = np.array([0.5 * (s.sol(t)[3:] @ s.sol(t)[3:]) for t in ts])
dke_net = ke[-1] - ke[0]; dke_peak = np.max(np.abs(ke - ke[0]))
pot_end = sum(-G * M / np.sqrt((s.y[:3, -1] - x0) @ (s.y[:3, -1] - x0) + b * b) for M, b, x0 in
              [(1e5 * MSUN, 0.3 * PC, np.array([0, 0.2 * PC, 0])), (4e4 * MSUN, 0.1 * PC, np.array([0.5 * PC, -0.1 * PC, 0.05 * PC]))])
pot_beg = sum(-G * M / np.sqrt((y0[:3] - x0) @ (y0[:3] - x0) + b * b) for M, b, x0 in
              [(1e5 * MSUN, 0.3 * PC, np.array([0, 0.2 * PC, 0])), (4e4 * MSUN, 0.1 * PC, np.array([0.5 * PC, -0.1 * PC, 0.05 * PC]))])
cons = abs(dke_net + (pot_end - pot_beg)) / dke_peak       # energy conservation residual
net_rel = abs(dke_net) / dke_peak                           # what is left of the work after leaving
# (b) uniform gradient: dKE = g d exactly
gu, d = 2.1e-10, 1e15
s2 = solve_ivp(lambda t, y: [y[1], gu], [0, 1e9], [0, 1e5], rtol=1e-12, atol=1e-6, dense_output=True)
tt = (-1e5 + np.sqrt(1e10 + 2 * gu * d)) / gu; yy = s2.sol(tt)
uni_rel = abs((0.5 * yy[1]**2 - 0.5e10) / (gu * yy[0]) - 1)
P(f"  bounded clump crossing: net dKE / peak dKE = {net_rel:.2e}; energy residual {cons:.1e} (should be tiny; residual = far-field potential left)")
P(f"  uniform gradient: dKE/(g d) - 1 = {uni_rel:.1e}")
Q2_num = (net_rel < 1e-6) and (uni_rel < 1e-6)          # graded exactly as frozen
P(f"  frozen check (net/peak < 1e-6 and uniform < 1e-6): {'PASS' if Q2_num else 'FAIL as frozen'}")
# reported, not graded: the residual is the potential difference left at finite endpoints; push them out
ext = {}
for Dpc in (400, 4000):
    y0e = np.array([-Dpc * PC, 0.05 * PC, 0, v0, 0, 0]); Te = 2 * Dpc * PC / v0
    se = solve_ivp(f, [0, Te], y0e, rtol=1e-11, atol=1e-3, method="DOP853")
    ext[Dpc] = abs(0.5 * (se.y[3:, -1] @ se.y[3:, -1]) - 0.5 * v0**2) / dke_peak
    P(f"  reported: endpoints at +-{Dpc} pc -> net/peak = {ext[Dpc]:.2e}")
lam_mov = {}
for lsn, Lst in LSTAR.items():
    for beta in (0.1, 0.998):
        lam_mov[f"{lsn}_beta{beta}"] = 2 * np.pi * Lst * c / (beta * c)
for k, v in lam_mov.items():
    P(f"  moving device, k <= 1/L*: photon wavelength >= {v:.2e} m ({v / 9.461e15:.1f} ly)  [{k}]")
d_aCen = 4.37 * 9.461e15
gain = {fn: max(a0, G_LOC) * d_aCen for fn, a0 in FOOT.items()}
need = 0.5 * (0.1 * c)**2
for fn, gnn in gain.items():
    P(f"  energy any device gains over 4.37 ly, <= g_c d = {gnn:.2e} J/kg ({fn}); needed for 0.1c {need:.2e} J/kg -> short x{need / gnn:.1e}")
q2_class = "STATIC CONVERSION FORBIDDEN" if Q2_num else "numerical check FAIL as frozen (theorem: energy residual %.1e)" % cons
P(f"  Q2: {q2_class} (rest mass: cold-mass continuity => eta_rest = 0 exactly)")
R["Q2"] = {"class": q2_class, "net_rel": net_rel, "energy_residual": cons, "uniform_rel": uni_rel, "frozen_check_pass": Q2_num, "extended_net_rel": ext,
           "lambda_moving_m": lam_mov, "gain_J_per_kg": gain, "need_J_per_kg_0.1c": need}

# ---------- Q3: efficiency ----------
P("\nQ3  efficiency eta = output / (rho_c c^2 v A)")
eta = {"eta_rest": 0.0}
for MA_n, MA in (("1mg/m2", 1e-6), ("1g/m2", 1e-3)):
    for gn, gc in list(FOOT.items()) + [("local2.1e-10", G_LOC)]:
        e = MA * gc / U0
        eta[f"grav_{MA_n}_{gn}"] = e
        P(f"  gravitational-work ceiling (work on craft, not light) M/A={MA_n:7s} g_c={gn:12s}: eta <= {e:.2e}")
# moving 45 T, 100 m device converting the static pattern (c_P = c best case), field-energy fraction
for lsn, Lst in LSTAR.items():
    for fn, a0 in FOOT.items():
        v = 0.1 * c; om = v / Lst
        Dp = delta_P_closed(45, om, Lst, c)
        p = min((Dp * 100)**2, 1.0)
        gfield = G_LOC
        frac = gfield**2 / (8 * np.pi * G) / U0
        eta[f"mix_{lsn}_{fn}"] = p * frac
        P(f"  moving-device mixing (45 T, 100 m, 0.1c, L*={lsn}, {fn}): P={p:.2e} x field fraction {frac:.2e} = {p * frac:.2e}"
          f"  (photon wavelength {2 * np.pi * c / om:.1e} m >> device: upper bound)")
eta_max = max(eta.values())
q3_class = "NO BUILT-IN PORTAL" if eta_max < 1e-6 else "PORTAL"
P(f"  eta_max (any channel, even counting work on the craft) = {eta_max:.2e}: short of 0.01 by {np.log10(0.01 / eta_max):.1f} orders, of 1 by {np.log10(1 / eta_max):.1f}")
eta_light = max(v for k, v in eta.items() if k.startswith('mix'))
P(f"  light only (mixing): best {eta_light:.1e}: short of 0.01 by {np.log10(0.01 / eta_light):.1f} orders, of 1 by {np.log10(1 / eta_light):.1f}")
R["eta_light"] = eta_light
P(f"  Q3: {q3_class}")
R["Q3"] = {"class": q3_class, "eta": eta, "eta_max": eta_max,
           "orders_short_0.01": float(np.log10(0.01 / eta_max)), "orders_short_1": float(np.log10(1 / eta_max))}

# ---------- MUTATE bite ----------
if MUT:
    r_opt = [r for r in ratio_rows if r["photon"].startswith("optical")][0]["got"]
    bite = abs(r_opt * np.sqrt(2) - 1) < 1e-9
    P(f"\nMUTATE: Delta_P/Delta_grav = {r_opt:.6f} (1/sqrt2 = {1 / np.sqrt(2):.6f}) -> {'BITES' if bite else 'DOES NOT BITE'}; Q1 class now: {q1_class}")
    R["mutate_bites"] = bite

json.dump(R, open(os.path.join(HERE, f"cfg793_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
ok = K1 and K2 and K3
sys.exit(1 if (MUT and R.get("mutate_bites")) else (0 if ok else 2))
