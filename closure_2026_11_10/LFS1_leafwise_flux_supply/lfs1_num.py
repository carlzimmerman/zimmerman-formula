"""LFS1 numeric part (criteria 8ddf81950c): S2 / KA6, KA4, KA5, A1-A4 per footing, brackets.

Inputs exactly as FROZEN_CRITERIA section 2. Point-mass baryons, law S, static constitutive law (gamma_L = 0 in P; the
gamma_L Pi_+ factor is kept in X). MUTATE (env LFS1_MUTATE): MU1 flips lambda's sign in S2; MU2 injects lambda := lambda_s
in A1; MU3 continues P past the edge in A2 (no P = 0 exterior). Each writes lfs1_num_MUTATE_<id>.json/.out.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

MUT = os.environ.get("LFS1_MUTATE", "")
tag = f"_MUTATE_{MUT}" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))
lines = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); lines.append(s)

G = 6.674e-11; MSUN = 1.98847e30; KPC = 3.085677581e19; C = 2.99792458e8; GYR = 3.15576e16
MPC = 1e3 * KPC; PC = KPC / 1e3
H0 = 67.4e3 / MPC
h = 0.674
I0 = 4.037e-8                       # Mpc^-2
Om_d = I0 / (3 * (H0 * MPC / C) ** 2)
Om_b = Om_d / 5.41
Om_r = 4.15e-5 / h**2
Om_L = 1 - Om_d - Om_b - Om_r
rho_crit0 = 3 * H0**2 / (8 * math.pi * G)
rho_d0 = Om_d * rho_crit0

def Hz(z): return H0 * math.sqrt(Om_r * (1 + z) ** 4 + (Om_d + Om_b) * (1 + z) ** 3 + Om_L)
def t_of_z(z): return quad(lambda zz: 1 / ((1 + zz) * Hz(zz)), z, np.inf, limit=200)[0]

FOOT = {"canonical": dict(a0=9.3603e-11, X=59.486, Ls=21.7 * PC),
        "alt": dict(a0=1.1312e-10, X=59.503, Ls=22.9 * PC)}
LOGM = [9.4, 10.45, 10.7, 10.9]
FLD1 = {9.4: dict(Rta=120, inner=81, middle=190, Rcap=116, Rfold1=34, Rfold2=21),
        10.45: dict(Rta=268, inner=272, middle=637, Rcap=389, Rfold1=76, Rfold2=48),
        10.7: dict(Rta=325, inner=362, middle=849, Rcap=518, Rfold1=92, Rfold2=58),
        10.9: dict(Rta=378, inner=456, middle=1069, Rcap=653, Rfold1=108, Rfold2=68)}
RATIO_TA = {1: 0.46, 2: 0.435}
ALPHA0 = 0.8; ALPHAS = [0.4, 1.5]
ZGRID = [0.0, 0.5, 1.0, 2.0]
RGRID = [10, 30, 100, 300]

res = {"mutate": MUT, "inputs": dict(Om_d=Om_d, Om_b=Om_b, Om_L=Om_L, rho_d0_Msun_kpc3=rho_d0 / MSUN * KPC**3)}
say(f"Background: Omega_d {Om_d:.4f} Omega_b {Om_b:.4f} Omega_L {Om_L:.4f}; t0 {t_of_z(0)/GYR:.3f} Gyr; "
    f"mean cold dark energy today {rho_d0/MSUN*KPC**3:.2f} Msun/kpc^3")

# ---------------- the law ----------------
def gS(M, r, a0):
    gN = G * M / r**2
    return gN / 2 + math.sqrt(gN**2 / 4 + gN * a0)
def Claw(M, r, a0):
    gN = G * M / r**2
    return r**2 * (gS(M, r, a0) - gN) / G
def Rcap(M, a0, X): return math.sqrt(G * M * X * (X + 1) / a0)
def rho_ph(M, r, a0):
    e = 1e-4
    return (Claw(M, r * (1 + e), a0) - Claw(M, r * (1 - e), a0)) / (2 * e * r) / (4 * math.pi * r**2)
def Phi(M, r, a0, X, Rout=None):
    """Law out to Rout (default R_cap), point mass M nu(Rout) beyond; Phi(inf) = 0."""
    Ro = Rcap(M, a0, X) if Rout is None else Rout
    Mtot = M + Claw(M, Ro, a0)
    if r >= Ro: return -G * Mtot / r
    I = quad(lambda rr: gS(M, rr, a0), r, Ro, limit=200, epsrel=1e-11)[0]
    return -I - G * Mtot / Ro
def gamPi(M, r, a0, Ls): return 2 * math.pi * G * rho_ph(M, r, a0) * Ls**2 / C**2

# ---------------- KA4, KA5 ----------------
ka4 = math.sqrt(MSUN * 9.3603e-11 / G) * KPC / MSUN
say(f"KA4 sqrt(Msun a0/G) = {ka4:.1f} Msun/kpc (target 25914, rel {abs(ka4/25914-1):.1e})")
res["KA4"] = dict(value=ka4, pass_=abs(ka4 / 25914 - 1) < 1e-3)
ka5 = {}
for lm in LOGM:
    rc = Rcap(10**lm * MSUN, 9.3603e-11, 59.486) / KPC
    ka5[lm] = (rc, abs(rc / FLD1[lm]["Rcap"] - 1))
say("KA5 R_cap canonical (kpc) vs FLD1:", {k: (round(v[0], 1), FLD1[k]["Rcap"]) for k, v in ka5.items()})
res["KA5"] = dict(values={str(k): v[0] for k, v in ka5.items()}, pass_=all(v[1] < 5e-3 for v in ka5.values()))

# ---------------- S2 / KA6: finite-volume khronon charge with lambda from the normal equation ----------------
def s2_run(mode):
    """mode 'normal' | 'flip' (MU1) | 'supply' (lambda set to the value that makes the charge grow by (1+t))."""
    nr = 400
    r = np.linspace(1e-3, 1.0, nr)
    gl = 0.7
    Nf = lambda t: 1 + 0.3 * np.sin(2 * np.pi * t) * np.exp(-r**2) + 0.1 * t * r
    hf = lambda t: 1 + 0.2 * t * r**2
    Pif = lambda t: 1 + 0.5 * np.cos(t) * r
    Xf = lambda t: Nf(t) * (1 + gl * Pif(t))
    sf = lambda t: r**2 * hf(t)
    P0 = r * np.exp(-r)
    Y0 = sf(0) * P0
    Qenc = Xf(0) * Y0                       # enclosed charge (identity S1(a); the evolution below uses only the flux)
    Q0 = Qenc.copy()
    dt = 1e-3; eps = 1e-6
    def lam(t):
        N1, N2 = Nf(t + eps), Nf(t - eps); Pi1, Pi2 = Pif(t + eps), Pif(t - eps)
        dlnN = (np.log(N1) - np.log(N2)) / (2 * eps); dPi = (Pi1 - Pi2) / (2 * eps)
        return ((1 + gl * Pif(t)) * dlnN + gl * dPi) / Nf(t)
    def flux(t, Q):
        Y = Q / Xf(t)                       # recover Y = s P from the enclosed charge
        P = Y / sf(t)
        if mode == "supply":
            # lambda_s: makes the enclosed charge follow Q0 (1 + t):  lambda N^2 Y = Q0
            return Q0.copy()
        L = lam(t) * (-1 if mode == "flip" else 1)
        return sf(t) * L * Nf(t)**2 * P      # zero shift: d/dt Q_enc(r) = s lambda N^2 P at r
    t = 0.0; Q = Qenc.copy()
    for _ in range(1000):
        k1 = flux(t, Q); k2 = flux(t + dt / 2, Q + dt / 2 * k1)
        k3 = flux(t + dt / 2, Q + dt / 2 * k2); k4 = flux(t + dt, Q + dt * k3)
        Q = Q + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += dt
    Y1 = Q / Xf(t)
    return float(np.max(np.abs(Y1 / Y0 - 1))), float(np.max(np.abs(Xf(t) / Xf(0) - 1)))

s2 = {}
for mode in (["flip"] if MUT == "MU1" else ["normal", "supply"]):
    s2[mode] = s2_run(mode)
    say(f"S2/KA6 mode {mode}: max |Y(1)/Y(0) - 1| = {s2[mode][0]:.3e} (X itself moved by up to {s2[mode][1]:.3f})")
res["S2"] = s2
res["KA6"] = dict(pass_=(s2["normal"][0] < 1e-6 and s2["supply"][0] > 0.1) if "normal" in s2 else None)

# ---------------- A1-A4 per footing ----------------
def Mb(M0, z, alpha): return M0 * math.exp(-alpha * z)
def dtdz(z): return -1 / ((1 + z) * Hz(z))

def a1_point(M0, R, z, a0, X, Ls, alpha, Rout_mode="cap"):
    dz = 1e-3 if z > 0 else 1e-3
    zs = (z + dz, z - dz) if z >= dz else (z + dz, z)
    vals = []
    for zz in zs:
        M = Mb(M0, zz, alpha)
        Ro = None if Rout_mode == "cap" else 10 * MPC
        vals.append((Claw(M, R, a0), Phi(M, R, a0, X, Ro) / C**2 + gamPi(M, R, a0, Ls)))
    Dz = zs[0] - zs[1]
    dlnC_dz = (math.log(vals[0][0]) - math.log(vals[1][0])) / Dz
    dlnX_dz = (vals[0][1] - vals[1][1]) / Dz       # ln X = ln(1 + Phi/c^2) + ln(1 + gPi) ~ Phi/c^2 + gPi (|.| < 1e-5)
    f = dtdz(z)
    lam_s = dlnC_dz / f; lam_n = dlnX_dz / f        # per second (lambda N^2 / X in each case)
    if MUT == "MU2": lam_n = lam_s
    return lam_s, lam_n

A = {}
for foot, F in FOOT.items():
    a0, X, Ls = F["a0"], F["X"], F["Ls"]
    A[foot] = {}
    say(f"\n===== footing {foot}: a0 {a0}, X_cap {X}, L* {Ls/PC:.1f} pc =====")
    t0 = t_of_z(0)
    for lm in LOGM:
        M0 = 10**lm * MSUN
        rc0 = Rcap(M0, a0, X)
        row = dict(Rcap0_kpc=rc0 / KPC, grid=[])
        Rlist = [R * KPC for R in RGRID] + ([rc0] if rc0 > 300 * KPC else [])
        worst = None; signs = set(); finite = True
        for R in Rlist:
            for z in ZGRID:
                ls, ln = a1_point(M0, R, z, a0, X, Ls, ALPHA0)
                ratio = ln / ls
                finite &= math.isfinite(ls); signs.add(np.sign(ls))
                lsb = [a1_point(M0, R, z, a0, X, Ls, al)[0] for al in ALPHAS]
                lnb = [a1_point(M0, R, z, a0, X, Ls, al)[1] for al in ALPHAS]
                ln10 = a1_point(M0, R, z, a0, X, Ls, ALPHA0, "10Mpc")[1]
                rb = [lnb[i] / lsb[i] for i in range(2)] + [ln10 / ls]
                g = dict(R_kpc=R / KPC, z=z, lam_s_perGyr=ls * GYR, lam_n_perGyr=ln * GYR, rho_lambda=ratio,
                         rho_brackets=rb)
                row["grid"].append(g)
                dev = abs(ratio - 1)
                if worst is None or dev > worst[0]: worst = (dev, R / KPC, z, ratio)
        # integrated z2 -> 0 at each R
        integ = []
        t2 = t_of_z(2.0)
        for R in Rlist:
            M2, Mz0 = Mb(M0, 2, ALPHA0), M0
            lnC = math.log(Claw(Mz0, R, a0) / Claw(M2, R, a0))
            lnX = (Phi(Mz0, R, a0, X) - Phi(M2, R, a0, X)) / C**2 + gamPi(Mz0, R, a0, Ls) - gamPi(M2, R, a0, Ls)
            if MUT == "MU2": lnX = lnC
            integ.append(dict(R_kpc=R / KPC, lnC=lnC, lnX=lnX, ratio=lnX / lnC))
        row["integrated_z2_0"] = integ
        # frozen halo deficit, creep speed, origin radius
        froz = {}
        for zs_ in (2.0, 1.0, 0.5):
            Ms = Mb(M0, zs_, ALPHA0)
            froz[zs_] = [dict(R_kpc=R / KPC, C_ratio=Claw(Ms, R, a0) / Claw(M0, R, a0)
                              * (1 + Phi(M0, R, a0, X) / C**2) / (1 + Phi(Ms, R, a0, X) / C**2)) for R in Rlist]
        row["frozen_halo"] = {str(k): v for k, v in froz.items()}
        creep = []
        for R in Rlist:
            for z in ZGRID:
                M = Mb(M0, z, ALPHA0)
                e = 1e-4
                dCdR = (Claw(M, R * (1 + e), a0) - Claw(M, R * (1 - e), a0)) / (2 * e * R)
                ls, _ = a1_point(M0, R, z, a0, X, Ls, ALPHA0)
                v = ls * Claw(M, R, a0) / dCdR
                creep.append(dict(R_kpc=R / KPC, z=z, v_kms=v / 1e3))
        row["creep"] = creep
        orig = []
        for R in Rlist:
            Cn = Claw(M0, R, a0)
            for zz in (1, 2):
                Mz = Mb(M0, zz, ALPHA0)
                Rp = brentq(lambda x: Claw(Mz, x, a0) - Cn, R, 1e4 * MPC)
                Rta_z = FLD1[lm]["Rfold%d" % zz] / RATIO_TA[zz]
                orig.append(dict(R_kpc=R / KPC, z=zz, Rorigin_kpc=Rp / KPC, Rta_z_kpc=Rta_z, ratio=Rp / KPC / Rta_z))
        row["origin"] = orig
        row["A1"] = dict(finite=finite, one_sign=(len(signs) == 1), worst=worst,
                         pass_=bool(finite and len(signs) == 1 and worst[0] <= 0.5))
        # ---------------- A2 / A3 / A4 at R_s = R_ta(z0) and R_cap ----------------
        edge = {}
        for name, Rs in (("R_ta", FLD1[lm]["Rta"] * KPC), ("R_cap", rc0)):
            Cs = Claw(M0, Rs, a0)
            qedge = 0.0 if MUT == "MU3" else -Cs
            w = 0.1 * Rs
            rho_edge = qedge / (4 * math.pi * Rs**2 * w)
            # mu_K = 1 per Mpc bracket: the dust part inside R_s
            muK = 1 / MPC
            dust = quad(lambda rr: 4 * math.pi * rr**2 * muK**2 * (-Phi(M0, rr, a0, X)) / (4 * math.pi * G),
                        1e-3 * KPC, Rs, limit=200)[0]
            # A3 lensing: Delta Sigma of the law (baryon point mass + phantom out to R_s) and of the edge shell
            def dsig_law(Rp):
                rho = lambda rr: rho_ph(M0, rr, a0)
                M3 = M0 + Claw(M0, Rp, a0)
                Mcyl = M3 + quad(lambda rr: 4 * math.pi * rr**2 * rho(rr) * (1 - math.sqrt(1 - Rp**2 / rr**2)),
                                 Rp, Rs, limit=200)[0]
                u_max = math.sqrt(Rs**2 - Rp**2)
                Sig = 2 * quad(lambda u: rho(math.sqrt(Rp**2 + u**2)), 0, u_max, limit=200)[0]
                return Mcyl / (math.pi * Rp**2) - Sig
            def dsig_shell(Rp, Ms):
                x = Rp / Rs
                return Ms / (math.pi * Rp**2) * (1 - math.sqrt(1 - x**2)) - Ms / (2 * math.pi * Rs**2 * math.sqrt(1 - x**2))
            lens = {}
            for f in (0.5, 0.9):
                dl = dsig_law(f * Rs); ds = dsig_shell(f * Rs, qedge)
                lens[str(f)] = dict(dsig_law=dl, dsig_shell=ds, frac=ds / dl)
            gs = gS(M0, Rs, a0)
            edge[name] = dict(R_s_kpc=Rs / KPC, C_over_Mb=Cs / M0, q_edge_over_Mb=qedge / M0,
                              rho_edge_over_rho_d0=rho_edge / rho_d0,
                              dust_needed_over_Mb=Cs / M0, cosmic_share=5.41, fld1_arrival_over_Mb=0.051 * Cs / M0,
                              muK1_dust_over_C=dust / Cs,
                              g_over_a0=gs / a0, sigma_edge_Msun_pc2=Cs / (4 * math.pi * Rs**2) / MSUN * PC**2,
                              dg_over_g=-(Cs / (M0 + Cs)), lensing=lens,
                              A4=("NO EDGE (P continued; MU3)" if MUT == "MU3" else ("WALL" if gs > 0 else "SMOOTH")),
                              fold=(name != "R_ta"))
        row["edge"] = edge
        row["A2"] = dict(pass_=all(v["q_edge_over_Mb"] >= 0 for v in edge.values()))
        row["A3"] = dict(R_s_kpc=FLD1[lm]["Rta"], R_cap_kpc=rc0 / KPC, inner=FLD1[lm]["inner"],
                         middle=FLD1[lm]["middle"], short_of_cap=FLD1[lm]["Rta"] < rc0 / KPC)
        row["A4"] = edge["R_ta"]["A4"]
        A[foot][str(lm)] = row
        # print
        w = row["A1"]["worst"]
        say(f"\nlog M_b {lm}: R_cap {rc0/KPC:.1f} kpc. A1 {'PASS' if row['A1']['pass_'] else 'FAIL'}: "
            f"worst rho_lambda {w[3]:.3e} at R {w[1]:.0f} kpc z {w[2]}; lambda_s finite {finite}, one sign {len(signs)==1}")
        for g in row["grid"]:
            if g["z"] in (0.0, 2.0):
                say(f"   R {g['R_kpc']:7.1f} z {g['z']}: lambda_s {g['lam_s_perGyr']:.4f}/Gyr  lambda_n {g['lam_n_perGyr']:.3e}/Gyr"
                    f"  rho {g['rho_lambda']:.3e}  brackets(a0.4, a1.5, 10Mpc) {[f'{b:.2e}' for b in g['rho_brackets']]}")
        say("   integrated z2->0: " + "; ".join(f"R {i['R_kpc']:.0f}: lnC {i['lnC']:.3f} lnX {i['lnX']:.2e} ratio {i['ratio']:.2e}" for i in integ))
        say("   frozen halo since z 2/1/0.5, C/C_law at z0 (R 100, 300 kpc): " + "; ".join(
            f"z{k}: " + ", ".join(f"{v['C_ratio']:.3f}" for v in froz[k] if v['R_kpc'] in (100, 300)) for k in froz))
        say("   creep speed (km/s) at z 0, R 10/30/100/300/cap: " + ", ".join(f"{c['v_kms']:.2f}" for c in creep if c['z'] == 0))
        say("   origin of today's charge: " + "; ".join(f"R {o['R_kpc']:.0f} z{o['z']}: {o['Rorigin_kpc']:.0f} kpc = {o['ratio']:.2f} R_ta(z)" for o in orig if o['R_kpc'] in (100, 300)))
        for name, e in edge.items():
            say(f"   edge at {name} {e['R_s_kpc']:.0f} kpc: C/M_b {e['C_over_Mb']:.2f}, edge charge {e['q_edge_over_Mb']:.2f} M_b, "
                f"edge rho (w 0.1 R_s) {e['rho_edge_over_rho_d0']:.1f} x mean cold dark energy; FLD1 arrival {e['fld1_arrival_over_Mb']:.2f} M_b; "
                f"mu_K=1/Mpc dust/C {e['muK1_dust_over_C']:.3f}; g/a0 {e['g_over_a0']:.4f}; sigma_edge {e['sigma_edge_Msun_pc2']:.3f} Msun/pc^2; "
                f"dg/g {e['dg_over_g']:.3f}; lensing shell/law at 0.5,0.9 R_s: {e['lensing']['0.5']['frac']:.3f}, {e['lensing']['0.9']['frac']:.3f}; A4 {e['A4']}{' + FOLD' if e['fold'] else ''}")
        say(f"   A2 {'PASS' if row['A2']['pass_'] else 'FAIL'}; A3 R_s(R_ta) {FLD1[lm]['Rta']} kpc vs R_cap {rc0/KPC:.0f}, "
            f"KiDS inner {FLD1[lm]['inner']} middle {FLD1[lm]['middle']}; A4 {row['A4']}")
res["A"] = A
say("\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.")
json.dump(res, open(os.path.join(here, f"lfs1_num{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(here, f"lfs1_num{tag}.out"), "w").write("\n".join(lines) + "\n")

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
