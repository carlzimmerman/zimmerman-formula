"""CFG390 part B: spherical quasi-static end state of the two-fluid cold-fluid system (MW-like and cluster-like hosts), plus the
Lagrangian isothermal Navier-Stokes viscosity control. Frozen: FROZEN_CRITERIA.md. Both a0 footings, never pooled. kappa = 1/2 fitted.
CFG390_MUTATE=1 sets kappa_s = 0 in every cell (separate outputs)."""
import os, json, math
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG390_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
LOG, CH, RES = [], [], {"mutate": MUTATE}
def say(s=""): print(s, flush=True); LOG.append(s)
def check(name, ok, val=""):
    CH.append({"name": name, "pass": bool(ok), "value": str(val)}); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")

G, MSUN, KPC, GYR, c = 6.674e-11, 1.989e30, 3.0857e19, 3.15576e16, 2.99792458e8
h_P, hbar, eV = 6.62607015e-34, 1.054571817e-34, 1.602176634e-19
H0 = 67.4e3 / 3.0857e22; RHOC = 3 * H0**2 / (8 * math.pi * G); OMC = 0.266; AGE = 13.8 * GYR
ZETA32 = 2.612375348685488
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LAM382, V382 = 0.027995, 200e3
KAP_PRIMARY = (LAM382 * V382) ** 2
KAPS = {"primary": KAP_PRIMARY, "300": 300e3**2, "1000": 1000e3**2, "3000": 3000e3**2, "inf": math.inf}
if MUTATE:
    KAPS = {k: 0.0 for k in KAPS}
M_PRIMARY, M_BRACKET = 0.8066, (0.62, 0.71)
HOSTS = {"MW": dict(Mb=6e10, a=3.0, sig=150e3, fret=(0.18, 1.0), rmin=0.01),
         "cluster": dict(Mb=1e14, a=250.0, sig=1000e3, fret=(1.0,), rmin=0.5)}
nu = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-30))))

def rho_crit(m_eV, sig, g=1):
    m = m_eV * eV / c**2; lamT = h_P / (m * sig * math.sqrt(2 * math.pi)); return ZETA32 * m / (g * lamT**3)
def lam_bullet(m_eV):        # sigma/m = 1 cm^2/g with sigma = lam^2/(128 pi m^2) (CFG384)
    HBARC_CM = 1.97327e-5
    s1 = (1.0 / (128 * math.pi)) * (HBARC_CM / m_eV)**2 / (m_eV * eV / c**2 * 1e3)
    return math.sqrt(1.0 / s1)
def K_int(m_eV):             # h = K rho; c_s^2 = lam rho c^4 (hbar c)^3 / (4 (m c^2)^4)  (CFG384 G3)
    mE = m_eV * eV; return lam_bullet(m_eV) * c**4 * (hbar * c)**3 / (4 * mE**4)
def degeneracy(m_eV, rho, sig, g=1):
    m = m_eV * eV / c**2; return g * (rho / m) * (h_P / (m * sig * math.sqrt(2 * math.pi)))**3
def tau_rel(m_eV, rho, sig):  # CFG384: 1/(D sigma v n), sigma at the Bullet limit
    m = m_eV * eV / c**2; sx = 0.1 * m                      # sigma_x = (1 cm^2/g) m in SI
    D = max(1.0, degeneracy(m_eV, rho, sig)); return 1.0 / (D * sx * sig * (rho / m))

say("CFG390 part B: spherical quasi-static end state" + ("  (MUTATE: kappa_s = 0)" if MUTATE else ""))
say("=" * 100)
say(f"  kappa_s primary: sqrt = lambda_382 * 200 km/s = {math.sqrt(KAP_PRIMARY)/1e3:.3f} km/s (kappa_s = {KAP_PRIMARY:.3e} m^2/s^2)")

# ---------------------------------------------------------------- C3: Bose critical density vs CFG383
rho383 = 0.85 * 500 * RHOC / 3
u383 = ZETA32 / degeneracy(0.8065531755456946, rho383, 1000e3)
check("C3 rho_crit / Bose degeneracy reproduce CFG383 u = 0.5 at m_half (cluster)", abs(u383 - 0.5) < 1e-6, f"u = {u383:.9f}")
check("C3b rho_crit = u * rho at m_half", abs(rho_crit(0.8065531755456946, 1000e3) / rho383 - 0.5) < 1e-6,
      f"{rho_crit(0.8065531755456946, 1000e3)/rho383:.9f}")

# ---------------------------------------------------------------- grid and target
def build(host, a0, Rdom, N=3000):
    H = HOSTS[host]
    e = np.concatenate([[0.0], np.geomspace(H["rmin"] * KPC, Rdom, N)])
    rc = np.concatenate([[e[1] / 2], np.sqrt(e[1:-1] * e[2:])])
    vol = 4 * np.pi / 3 * (e[1:]**3 - e[:-1]**3)
    Mb = H["Mb"] * MSUN; a = H["a"] * KPC
    Mb_e = Mb * e**2 / (e + a)**2
    gb_e = np.where(e > 0, G * Mb_e / np.maximum(e, 1e-30)**2, G * Mb / a**2)
    Mph_e = np.where(e > 0, (nu(gb_e / a0) - 1) * Mb_e, 0.0)
    rho_ph = np.diff(Mph_e) / vol
    return dict(e=e, rc=rc, vol=vol, Mb_e=Mb_e, gb_e=gb_e, Mph_e=Mph_e, rho_ph=rho_ph, Mb=Mb, a=a)

def potential(g, Mcold_e):
    """Phi at cell centres from baryons (Hernquist, analytic) + cold enclosed mass (closed sphere; point mass outside)."""
    e, rc = g["e"], g["rc"]
    Mc_c = np.interp(rc, e, Mcold_e)
    gc = G * Mc_c / rc**2
    # integrate from the outside in
    Rd = e[-1]
    phi_c_out = -G * Mcold_e[-1] / Rd
    # cumulative integral of gc dr from rc_i to Rd (trapezoid on centres + last segment)
    seg = 0.5 * (gc[1:] + gc[:-1]) * np.diff(rc)
    tail = gc[-1] * (Rd - rc[-1])
    I = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) + tail
    phi_cold = phi_c_out - I
    phi_b = -G * g["Mb"] / (rc + g["a"])
    return phi_cold + phi_b

def condensate_rho(lph, psi, kap, K):
    """solve kap (x - lph) + K e^x = psi for x = ln rho (Newton from the right, convex increasing)."""
    if kap == 0.0:
        return np.maximum(psi, 0.0) / K
    x0 = lph + psi / kap
    if np.all(K * np.exp(np.minimum(x0, 600.0)) < 1e-13 * kap):      # interaction term negligible: exact closed form
        return np.exp(x0)
    ub = np.where(psi > 0, np.maximum(lph, np.log(np.maximum(psi, 1e-300) / K)), lph)   # the root is <= this (see README)
    x = np.minimum(np.minimum(x0, ub), 700.0)
    for _ in range(400):
        ex = np.exp(x); f = kap * (x - lph) + K * ex - psi
        step = f / (kap + K * ex)
        x = x - step
        if np.max(np.abs(step)) < 1e-12:
            break
    return np.exp(x)

def equilibrium(g, S, kap, m_eV, sig, maxit=3000, tol=1e-9):
    lph = np.log(g["rho_ph"]); K = K_int(m_eV); rcn = rho_crit(m_eV, sig); vol = g["vol"]
    Mcold_e = np.concatenate([[0.0], np.cumsum(S * vol / vol.sum())])   # start: uniform (the Lagrangian sphere)
    for it in range(maxit):
        phi = potential(g, Mcold_e)
        if math.isinf(kap):
            def dens(al):
                rs = g["rho_ph"] * math.exp(al)
                rn = np.full_like(rs, rcn if al > 0 else 0.0)
                return rs, rn
            lo, hi = -50.0, 50.0
        elif kap == 0.0:
            def dens(mu):
                return condensate_rho(lph, mu - phi, 0.0, K), rcn * np.exp(np.minimum(0.0, (mu - phi) / sig**2))
            lo, hi = phi.min() - 1e3 * sig**2, phi.max() + 1e20
        else:
            useK = True
            def dens(al):
                psi = kap * al - phi
                rs = condensate_rho(lph, psi, kap, K) if useK else np.exp(np.minimum(lph + psi / kap, 600))
                rn = rcn * np.exp(np.minimum(0.0, psi / sig**2))
                return rs, rn
            lo, hi = (phi.min() - 1e4 * max(kap, sig**2)) / kap, (phi.max() + 1e4 * max(kap, sig**2)) / kap
        mass = lambda p: float(np.sum((dens(p)[0] + dens(p)[1]) * vol)) - S
        while mass(lo) > 0: lo -= (abs(lo) + 1) * 2
        while mass(hi) < 0: hi += (abs(hi) + 1) * 2
        p = brentq(mass, lo, hi, xtol=1e-14 * max(1.0, abs(lo), abs(hi)), rtol=1e-15, maxiter=500)
        rs, rn = dens(p)
        Mnew = np.concatenate([[0.0], np.cumsum((rs + rn) * vol)])
        dif = np.max(np.abs(Mnew - Mcold_e)) / S
        w = 0.5 if it < 50 else 0.2
        Mcold_e = (1 - w) * Mcold_e + w * Mnew
        if dif < tol:
            break
    phi = potential(g, Mnew)
    return dict(rs=rs, rn=rn, phi=phi, Mcold_e=Mnew, iters=it + 1, resid=dif, K=K, rcrit=rcn, p=p)

def score(g, sol, a0, rlo=10.0, rhi=100.0):
    e = g["e"]; sel = (e >= rlo * KPC) & (e <= rhi * KPC)
    Mtot = g["Mb_e"] + sol["Mcold_e"]
    V = np.sqrt(G * Mtot[sel] / e[sel]); Vl = np.sqrt(nu(g["gb_e"][sel] / a0) * g["gb_e"][sel] * e[sel])
    dev = V / Vl - 1
    return float(np.max(np.abs(dev))), float(np.median(dev)), dev

def half_mass_radius(g, sol, comp="rs"):
    Mc = np.cumsum(sol[comp] * g["vol"]); return float(np.interp(0.5 * Mc[-1], Mc, g["e"][1:]) / KPC)

def R500_law(g, a0):
    e = g["e"][1:]; Ml = nu(g["gb_e"][1:] / a0) * g["Mb_e"][1:]
    mean = Ml / (4 * np.pi / 3 * e**3); i = np.where(mean < 500 * RHOC)[0][0]
    return float(e[i])

def R_L(S):
    return (3 * S / (4 * math.pi * OMC * RHOC)) ** (1 / 3)

# ---------------------------------------------------------------- C1 target check
gC1 = build("MW", A0["alt"], 2.0e3 * KPC)
r_mid = gC1["rc"][1:]; y_mid = G * gC1["Mb"] * r_mid**2 / (r_mid + gC1["a"])**2 / r_mid**2 / A0["alt"]
eps = 1e-6
def Mph_an(r):
    Mbr = gC1["Mb"] * r**2 / (r + gC1["a"])**2; return (nu(G * Mbr / r**2 / A0["alt"]) - 1) * Mbr
drho = (Mph_an(r_mid * (1 + eps)) - Mph_an(r_mid * (1 - eps))) / (2 * eps * r_mid) / (4 * np.pi * r_mid**2)
sel = (r_mid > 0.1 * KPC)
c1err = float(np.max(np.abs(gC1["rho_ph"][1:][sel] / drho[sel] - 1)))
check("C1 cell-averaged rho_ph matches the analytic dM_ph/dr/(4 pi r^2) to 1e-3 (r > 0.1 kpc); rho_ph > 0", c1err < 1e-3 and np.all(gC1["rho_ph"] > 0),
      f"max rel err {c1err:.1e}; min rho_ph {gC1['rho_ph'].min():.2e}")

# ---------------------------------------------------------------- C4 normal fluid alone, fixed potential, Boltzmann
phi_t = -G * gC1["Mb"] / (gC1["rc"] + gC1["a"])
rn_t = np.exp(-(phi_t - phi_t[0]) / 150e3**2); rn_t *= 1e40 / np.sum(rn_t * gC1["vol"])
# hydrostatic residual: d ln rho/dr + dphi/dr / sigma^2 = 0
res_c4 = np.max(np.abs(np.diff(np.log(rn_t)) + np.diff(phi_t) / 150e3**2))
check("C4 normal fluid alone in a fixed potential: Boltzmann profile is hydrostatic to 1e-6", res_c4 < 1e-6, f"{res_c4:.1e}")

# ---------------------------------------------------------------- main runs
for foot, a0 in A0.items():
    RES[foot] = {}
    say(f"\n--- footing {foot}: a0 = {a0:.4e} m/s^2")
    # MW
    H = HOSTS["MW"]
    for fret in H["fret"]:
        S = 5.364 * H["Mb"] * MSUN / fret; RL = R_L(S)
        for Rfac in ((1.0, 0.5) if fret == 0.18 else (1.0,)):
            g = build("MW", a0, RL * Rfac)
            say(f"  MW f_ret {fret}: S = {S/MSUN:.3e} Msun, R_L = {RL/KPC/1e3:.3f} Mpc, R_dom = {Rfac} R_L; "
                f"M_ph(<R_dom) = {g['Mph_e'][-1]/MSUN:.3e} Msun -> ideal scale A = S/M_ph = {S/g['Mph_e'][-1]:.3f}")
            for kn, kap in KAPS.items():
                if Rfac != 1.0 and kn != "primary":
                    continue
                sol = equilibrium(g, S, kap, M_PRIMARY, H["sig"])
                mx, md, _ = score(g, sol, a0)
                fn = float(np.sum(sol["rn"] * g["vol"]) / S)
                rh = half_mass_radius(g, sol)
                Qflag = None
                ok = mx <= 0.05
                key = f"MW|fret{fret}|Rdom{Rfac}|kap_{kn}"
                RES[foot][key] = dict(max_dev=mx, median_dev=md, recovered=ok, normal_frac=fn, r_half_s_kpc=rh, iters=sol["iters"],
                                      resid=sol["resid"], mass_err=abs(float(np.sum((sol['rs']+sol['rn'])*g['vol']))/S - 1))
                say(f"    kappa {kn:>7s}: max|V/V_law-1| (10-100 kpc) {mx:8.3f}  median {md:+8.3f}  -> {'RECOVERED' if ok else 'not recovered'};"
                    f" normal frac {fn:.2e}; condensate r_half {rh:9.3f} kpc; it {sol['iters']} resid {sol['resid']:.1e}")
                if kn == "inf" and fret == 0.18 and Rfac == 1.0 and not MUTATE:
                    ratio = sol["rs"] / g["rho_ph"]
                    check(f"C2b [{foot}] kappa -> inf: rho_s/rho_ph uniform to 1e-3", np.ptp(ratio) / np.mean(ratio) < 1e-3, f"{np.ptp(ratio)/np.mean(ratio):.1e}")
                if fret == 0.18 and Rfac == 1.0:
                    # Q a posteriori, only where rho_s is resolved (> 1e-12 of its max); collapsed cores sit in the first grid cell
                    sq = np.sqrt(sol["rs"]); r = g["rc"]; ok_m = sol["rs"] > 1e-12 * sol["rs"].max()
                    d1 = np.gradient(sq, r); lap = np.gradient(r**2 * d1, r) / r**2
                    Q = np.abs(hbar**2 / (2 * (M_PRIMARY * eV / c**2)**2) * lap / np.maximum(sq, 1e-300))
                    Qr = float(np.max(Q[1:-1][ok_m[1:-1]]) / np.ptp(sol["phi"])) if ok_m[1:-1].any() else 0.0
                    RES[foot][key]["Q_over_DeltaPhi"] = Qr
                    say(f"      Q a posteriori (resolved cells): max|Q| / Delta Phi = {Qr:.1e}{'  FLAG' if Qr > 1e-3 else ''}")
                if kn == "primary" and fret == 0.18 and Rfac == 1.0:
                    RES[foot]["MW_primary"] = RES[foot][key]
                    check(f"C2a [{foot}] equilibrium holds the supply mass to 1e-6 (MW primary)", RES[foot][key]["mass_err"] < 1e-6, f"{RES[foot][key]['mass_err']:.1e}")
        if fret == 0.18 and not MUTATE:
            # C2c supply matched, ideal settling -> law exactly
            g = build("MW", a0, RL)
            Sm = g["Mph_e"][-1]
            sol = equilibrium(g, Sm, math.inf, M_PRIMARY, H["sig"])
            mx, _, _ = score(g, sol, a0)
            check(f"C2c [{foot}] supply-matched ideal settling reproduces the law to 1e-3 over 10-100 kpc", mx < 1e-3, f"max dev {mx:.1e}")
    if MUTATE:
        rec = [v["recovered"] for k, v in RES[foot].items() if k.startswith("MW|") and isinstance(v, dict)]
        check(f"T-MUT [{foot}] MW law NOT recovered in any kappa_s cell (kappa_s = 0)", not any(rec), f"{sum(rec)} of {len(rec)} recovered")
        rh = RES[foot]["MW_primary"]["r_half_s_kpc"]
        check(f"T-MUT [{foot}] condensate collapses to a Thomas-Fermi core: r_half < 1 kpc", rh < 1.0, f"{rh:.3f} kpc")
    # cluster
    H = HOSTS["cluster"]
    S = 5.364 * H["Mb"] * MSUN; RL = R_L(S)
    g = build("cluster", a0, RL)
    R5 = R500_law(g, a0)
    say(f"  cluster: S = {S/MSUN:.3e} Msun, R_L = {RL/KPC/1e3:.2f} Mpc, R500(law) = {R5/KPC:.0f} kpc, M_ph(<R_L) = {g['Mph_e'][-1]/MSUN:.3e}"
        f" -> A = {S/g['Mph_e'][-1]:.3f}")
    for m_eV in (M_PRIMARY,) + M_BRACKET:
        for kn, kap in KAPS.items():
            sol = equilibrium(g, S, kap, m_eV, H["sig"])
            Mn = np.concatenate([[0.0], np.cumsum(sol["rn"] * g["vol"])]); Mc = sol["Mcold_e"]
            u500 = float(np.interp(R5, g["e"], Mn) / max(np.interp(R5, g["e"], Mc), 1e-300))
            i5 = np.searchsorted(g["rc"], R5)
            uloc = float(sol["rn"][i5] / (sol["rn"][i5] + sol["rs"][i5]))
            Mtot5 = np.interp(R5, g["e"], g["Mb_e"] + Mc); Mlaw5 = np.interp(R5, g["e"], nu(g["gb_e"] / a0) * g["Mb_e"])
            trel = tau_rel(m_eV, float(sol["rs"][i5] + sol["rn"][i5]), H["sig"]) / AGE
            key = f"cluster|m{m_eV}|kap_{kn}"
            RES[foot][key] = dict(u500=u500, u_local=uloc, M500_over_law=float(Mtot5 / Mlaw5), tau_rel_over_age_R500=trel,
                                  normal_frac_total=float(Mn[-1] / S), iters=sol["iters"], resid=sol["resid"])
            say(f"    m {m_eV:.4f} kappa {kn:>7s}: u500 (enclosed) {u500:.3f}, local {uloc:.3f}, M(<R500)/M_law {Mtot5/Mlaw5:.3f}, "
                f"tau_rel/age at R500 {trel:.2g}, total normal frac {Mn[-1]/S:.3f}; it {sol['iters']}")
            if m_eV == M_PRIMARY and kn == "primary":
                RES[foot]["cluster_primary"] = RES[foot][key]
    # timescales (reported)
    rhoMW50 = 170e3**2 / (4 * math.pi * G * (50 * KPC)**2)
    RES[foot]["timescales"] = dict(
        tau_rel_MW50_over_age=tau_rel(M_PRIMARY, rhoMW50, 150e3) / AGE,
        settle_cross_MW50_over_age=(50 * KPC / math.sqrt(KAP_PRIMARY)) / AGE,
        settle_cross_cluster_R500_over_age=(R5 / math.sqrt(KAP_PRIMARY)) / AGE)
    say(f"  timescales / age: tau_rel MW(50 kpc) {RES[foot]['timescales']['tau_rel_MW50_over_age']:.2g}; settling crossing r/sqrt(kappa_s) "
        f"MW 50 kpc {RES[foot]['timescales']['settle_cross_MW50_over_age']:.2g}, cluster R500 {RES[foot]['timescales']['settle_cross_cluster_R500_over_age']:.2g}")

# ---------------------------------------------------------------- viscosity control (Lagrangian, normal fluid only, cluster)
def lagrangian(eta_fac, N=120, Rbox=3000 * KPC, rin=30 * KPC, T=30 * GYR, sig=1000e3, Mn=2.682e14 * MSUN, m_eV=M_PRIMARY, avisc=False):
    Mb, a = 1e14 * MSUN, 250 * KPC
    r = np.linspace(rin, Rbox, N + 1)
    vol = 4 * np.pi / 3 * (r[1:]**3 - r[:-1]**3)
    dm = Mn * vol / vol.sum()
    Min = np.concatenate([[0.0], np.cumsum(dm)])
    dme = np.concatenate([[dm[0] / 2], 0.5 * (dm[1:] + dm[:-1]), [dm[-1] / 2]])
    v = np.zeros(N + 1)
    vbar = math.sqrt(8 / math.pi) * sig; m = m_eV * eV / c**2; sx = 0.1 * m
    rcn = rho_crit(m_eV, sig)
    def Fenergy(r, v):
        vol = 4 * np.pi / 3 * (r[1:]**3 - r[:-1]**3); rho = dm / vol; rc = 0.5 * (r[1:] + r[:-1])
        Menc = Min[:-1] + dm / 2
        return float(np.sum(0.5 * dme * v**2) + np.sum(dm * sig**2 * (np.log(rho / rcn) - 1))
                     + np.sum(dm * (-G * Mb / (rc + a))) - np.sum(G * Menc * dm / rc))
    t, KE, Fs, ts = 0.0, [], [], []
    nstep = 0
    nout = 0
    while t < T:
        vol = 4 * np.pi / 3 * (r[1:]**3 - r[:-1]**3); rho = dm / vol; rc = 0.5 * (r[1:] + r[:-1]); dr = np.diff(r)
        p = rho * sig**2
        lam = np.minimum(1.0 / ((rho / m) * sx * np.maximum(1.0, (rho / m) * (h_P / (m * sig * math.sqrt(2 * math.pi)))**3)), rc)
        eta = eta_fac * rho * vbar * lam / 3
        dvdr = np.diff(v) / dr; vr = 0.5 * (v[1:] + v[:-1]) / rc
        srr = 4 / 3 * eta * (dvdr - vr)
        q = np.zeros(N)
        if avisc:
            q = np.where(dvdr < 0, 2.0 * rho * (dr * dvdr)**2, 0.0)
        acc = np.zeros(N + 1)
        acc[1:-1] = (-4 * np.pi * r[1:-1]**2 * np.diff(p + q) + 4 * np.pi * np.diff(rc**3 * srr) / r[1:-1]) / dme[1:-1] \
                    - G * (Mb * r[1:-1]**2 / (r[1:-1] + a)**2 + Min[1:-1]) / r[1:-1]**2
        dtv = np.min(dr**2 * rho / (2 * eta)) if eta_fac > 0 else 1e99          # zone-wise viscous limit
        dt = 0.3 * min(np.min(dr / (sig + np.abs(0.5 * (v[1:] + v[:-1])) + 1e-9)), dtv)
        nstep += 1
        dt = min(dt, T - t)
        v = v + acc * dt; v[0] = v[-1] = 0.0
        r = r + v * dt
        t += dt
        if t >= nout * T / 300:
            KE.append(float(np.sum(0.5 * dme * v**2))); Fs.append(Fenergy(r, v)); ts.append(t); nout += 1
    vol = 4 * np.pi / 3 * (r[1:]**3 - r[:-1]**3); rho = dm / vol; rc = 0.5 * (r[1:] + r[:-1])
    # hydrostatic isothermal reference with the same mass, self-gravity, same box
    rr = np.linspace(rin, Rbox, 4001); rcm = 0.5 * (rr[1:] + rr[:-1]); vv = 4 * np.pi / 3 * (rr[1:]**3 - rr[:-1]**3)
    Me = np.concatenate([[0.0], np.cumsum(Mn * vv / vv.sum())])
    for _ in range(400):
        gtot = G * (Mb * rcm**2 / (rcm + a)**2 + np.interp(rcm, rr, Me)) / rcm**2
        phi = np.concatenate([[0.0], np.cumsum(gtot[1:] * np.diff(rcm))])
        w = np.exp(-(phi - phi.min()) / sig**2); dens = Mn * w / np.sum(w * vv)
        Mnew = np.concatenate([[0.0], np.cumsum(dens * vv)])
        if np.max(np.abs(Mnew - Me)) / Mn < 1e-12: break
        Me = 0.5 * Me + 0.5 * Mnew
    rms = float(np.sqrt(np.mean(np.log(rho / np.interp(rc, rcm, dens))**2)))
    KE = np.array(KE); Fs = np.array(Fs)
    rises = np.maximum(np.diff(Fs), 0.0)
    return dict(rms=rms, KE_final_over_peak=float(KE[-1] / KE.max()), F_max_rise_over_drop=float(rises.max() / max(Fs[0] - Fs[-1], 1e-300)),
                F_drop=float(Fs[0] - Fs[-1]), steps=nstep)

say("\n--- viscosity control (Lagrangian isothermal NS, normal fluid alone, cluster baryon potential, 3 Mpc box, uniform start)")
VC = {}
for lab, fac, av in (("eta_ref", 1.0, False), ("eta_0.1", 0.1, False), ("eta_0", 0.0, True)):
    VC[lab] = lagrangian(fac, avisc=av)
    say(f"  {lab:8s}: rms ln(rho/rho_hydrostatic) {VC[lab]['rms']:.4f}; KE_final/KE_peak {VC[lab]['KE_final_over_peak']:.2e}; "
        f"max F rise / total F drop {VC[lab]['F_max_rise_over_drop']:.1e}")
RES["viscosity"] = VC
check("V1 eta > 0 runs end within 2% (rms ln rho) of the hydrostatic isothermal profile", VC["eta_ref"]["rms"] <= 0.02 and VC["eta_0.1"]["rms"] <= 0.02,
      f"{VC['eta_ref']['rms']:.4f}, {VC['eta_0.1']['rms']:.4f}")
check("V2 F non-increasing in eta > 0 runs (any rise <= 1% of the total drop)",
      VC["eta_ref"]["F_max_rise_over_drop"] <= 0.01 and VC["eta_0.1"]["F_max_rise_over_drop"] <= 0.01,
      f"{VC['eta_ref']['F_max_rise_over_drop']:.1e}, {VC['eta_0.1']['F_max_rise_over_drop']:.1e}")
check("V3 eta = 0 run keeps its kinetic energy (KE_final/peak >= 10x the eta_ref run)",
      VC["eta_0"]["KE_final_over_peak"] >= 10 * VC["eta_ref"]["KE_final_over_peak"],
      f"{VC['eta_0']['KE_final_over_peak']:.2e} vs {VC['eta_ref']['KE_final_over_peak']:.2e}")
# Knudsen numbers
for foot in A0:
    pass
rhoR5 = 0.85 * 500 * RHOC / 3
m = M_PRIMARY * eV / c**2
def kn(rho, sig, r):
    D = max(1.0, degeneracy(M_PRIMARY, rho, sig)); return 1.0 / ((rho / m) * 0.1 * m * D) / r
RES["Knudsen"] = dict(cluster_R500=kn(rhoR5, 1000e3, 1000 * KPC), MW_10kpc=kn(170e3**2 / (4 * math.pi * G * (10 * KPC)**2), 150e3, 10 * KPC))
say(f"  Knudsen lambda_mfp/r: cluster R500 {RES['Knudsen']['cluster_R500']:.2g}; MW 10 kpc {RES['Knudsen']['MW_10kpc']:.2g}")

# ---------------------------------------------------------------- verdict inputs from part B
mw_ok = {f: RES[f]["MW_primary"]["recovered"] for f in A0}
cl_ok = {f: RES[f]["cluster_primary"]["u500"] >= 0.3 for f in A0}
RES["MW_recovered"] = mw_ok; RES["cluster_u500_ok"] = cl_ok
say(f"\nPart B scores (primary): MW law recovered {mw_ok}; cluster u500 >= 0.3 {cl_ok}")
n = sum(c["pass"] for c in CH)
say(f"Part B: {n}/{len(CH)} checks pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG390", "part": "B", "results": RES, "checks": CH}, open(os.path.join(HERE, f"cfg390_spherical_results{TAG}.json"), "w"),
          indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
open(os.path.join(HERE, f"cfg390_spherical{TAG}.out"), "w").write("\n".join(LOG) + "\n")
