#!/usr/bin/env python3
"""XF1 cells: every input of the Stage B table (FROZEN_CRITERIA.md 8b99d12c42) read from the record's own data paths,
with the dimensionless scales of the moving-body problem derived per cell, row, footing and V reading.

  python3 closure_2026_11_08/XF1_moving_host_field/xf1_cells.py      -> xf1_cells.json (+ a printed table)

Data paths (read only):
  B1 Coma UDGs      rebuild_2026_10_22/S1_v3_hosted_small/s1_coma_per_galaxy.csv (SE2's per-galaxy rows; host field
                    g_host = x_e_dmean a0 from S1's Coma beta model, FROZEN SE2 section 1)
  B2 MW classical   rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv (cls "MW classical"; host field X1's g_host:
                    Hernquist 6e10 Msun, A_H 3 kpc, the law; x_e_mid per row)
  B3 group member   closure_2026_11_06/QX10_window_hardening/iter_2_capture_dynamics (GR, the Lovisari groups CE2 grades):
                    group law field at 300 kpc, member proxy 10^10.5 Msun stars + 20 % gas, Plummer a = 3 kpc, readout 10 kpc
  B4 X-COP member   the same loader's XC (7 X-COP clusters): core law field at 500 kpc, member proxy 1e11 Msun, a = 5 kpc
  B5 the Sun        action_search_2026_11_05/AC12_comoving_halo / AC15 cells: Galactic Pi 0.0447 / 0.0514 Msun pc^-3,
                    x_e 1.15 / 2.6 (AZ37), L* floor, V 220 / 369 km/s, readouts 1 / 1.524 / 9.58 AU
Footings: the record's hosted path values a0 = 9.3603e-11 (canonical) / 1.1312e-10 m s^-2 (alt) (S1, X1, SE2, AC12),
never pooled. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, csv, json, math, io, contextlib
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16                 # X1 / S1 constants
KPC = 1e3 * PC; AU = 1.495978707e11; CL = 2.99792458e8
GK = 4.30091e-6                                                             # kpc (km/s)^2 / Msun (QX10)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                           # the hosted path's footings (S1 / X1 / SE2)
LFLOOR = {"canonical": 21.68, "alt": 22.85}                                 # pc, screening at the floor
FOOTS = ("canonical", "alt")
RHO_DE = {f: (2 * A0[f] / CL) ** 2 / G for f in FOOTS}                      # kg m^-3 from a0 = c sqrt(G rho_DE)/2
MSUN_PC3 = MSUN / PC ** 3                                                   # 1 Msun pc^-3 in kg m^-3

# ------------------------------------------------------------------ host fields of the record
A_H = 3.0 * KPC; MHOST_MW = 6.0e10                                          # X1's Hernquist host (E_mid)
def law(gN, a0): return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))        # g_N = g^2/(g + a0) inverted
def g_host_x1(R_m, a0, Mb=MHOST_MW):                                       # X1 / S1 g_host
    return law(G * Mb * MSUN / (R_m + A_H) ** 2, a0)
def rho_dyn(gfun, R_m):
    """phantom-inclusive local dynamical density of a spherical field, (1/4 pi G r^2) d(r^2 g)/dr  [kg m^-3]"""
    h = 1e-4 * R_m; f = lambda r: r * r * gfun(r)
    return (f(R_m + h) - f(R_m - h)) / (2 * h) / (4 * math.pi * G * R_m * R_m)

KEV, MP = 1.602176634e-16, 1.67262e-27                                      # S1's Coma beta model (L23 / CFG948)
BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6); CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP)
KPC_C = 3.0857e19
def g_beta(d_kpc):
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB * r / (r * r + rc * rc)
def rho_beta(d_kpc):
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB / (4 * math.pi * G) * (r * r + 3 * rc * rc) / (r * r + rc * rc) ** 2


def load_qx10():
    f = os.path.join(REPO, "closure_2026_11_06", "QX10_window_hardening", "iter_2_capture_dynamics", "qx10_i2.py")
    src = open(f).read(); cut = src.index('if __name__ == "__main__":')
    NS = {"__file__": f, "__name__": "qx10_i2_reused"}; argv0 = sys.argv; sys.argv = [f]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], f, "exec"), NS)
    sys.argv = argv0; return NS


def derived(row, f):
    """dimensionless scales per V reading. row: M_b [Msun], a_pc (Plummer scale; 0 = point), r_read_pc (list),
    x_e, rho_h [Msun pc^-3], V list [km/s]."""
    a0 = A0[f]; Ls = LFLOOR[f] * PC; M = row["M_b_Msun"] * MSUN; rho = row["rho_h_Msun_pc3"] * MSUN_PC3
    cs = math.sqrt(2 * math.pi * G * Ls ** 2 * rho)                         # stiffness sound speed, c_s^2 = gamma rho_h
    out = []
    for V in row["V_kms"]:
        v = V * 1e3; RA = 2 * G * M / v ** 2
        L0 = row["a_pc"] * PC if row["a_pc"] > 0 else RA
        gpar = G * M / (L0 * v ** 2)                                        # GM/(L0 V^2): 1/2 for the point Sun
        Minf = v / cs
        kq = 4 * math.pi * G * rho * L0 ** 2 / v ** 2                       # charge coupling (self-gravity / Legendre)
        rr = []
        for rp in row["r_read_pc"]:
            r = rp * PC
            gN = G * M / r ** 2 * (1.0 if row["a_pc"] <= 0 else (r / L0) ** 3 / (1 + (r / L0) ** 2) ** 1.5)
            rr.append(dict(r_pc=rp, r_over_L0=r / L0, r_over_RA=r / RA, gN=gN, gN_over_gext=gN / max(row["g_ext"], 1e-300),
                           restoring_over_inertia=4 * math.pi * G * rho * (1 + row["x_e"]) ** 2 * r ** 2 / v ** 2,
                           omega_p_t_cross=math.sqrt(4 * math.pi * G * rho) * (1 + row["x_e"]) * r / v,
                           stiffness_over_legendre=(Ls / r) ** 2 / (2 * (1 + row["x_e"]) ** 2),
                           deflection_gR_over_V2=gN * r / v ** 2))
        cap = 4 * math.pi / 3 * (2 * RA) ** 3 * rho * (1 + 0.75 * Minf ** 2)   # AC15 Bernoulli cap inside 2 R_A
        out.append(dict(V_kms=V, R_A_pc=RA / PC, L0_pc=L0 / PC, gpar=gpar, M_inf=Minf, kappa_q=kq, c_s_kms=cs / 1e3,
                        cap_2RA_over_Mb=cap / M, readouts=rr))
    return out


def build():
    C = dict(lane="XF1_moving_host_field", criteria="8b99d12c42", a0=A0, L_floor_pc=LFLOOR,
             rho_DE_Msun_pc3={f: RHO_DE[f] / MSUN_PC3 for f in FOOTS}, cells={f: {} for f in FOOTS},
             note="kappa = 1/2 FITTED; not theory closed. Footings never pooled. Adopts nothing.")
    # ---------------- B1 Coma UDGs (SE2's rows)
    rows = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small", "s1_coma_per_galaxy.csv"))))
    for f in FOOTS:
        B = []
        for r in rows:
            if r["footing"] != f: continue
            a_pc = float(r["Re_kpc"]) * 1e3; M = float(r["Mstar"]); xe = float(r["x_e_dmean"]); d = float(r["d_mean_kpc"])
            y = G * M * MSUN / ((a_pc * PC) ** 2 * A0[f])
            row = dict(name=r["name"], M_b_Msun=M, a_pc=a_pc, r_read_pc=[a_pc], d_host_kpc=d, x_e=xe, g_ext=xe * A0[f],
                       rho_h_Msun_pc3=rho_beta(d) / MSUN_PC3, rho_h_source="S1 rho_beta(d_mean) (phantom-inclusive dynamical density)",
                       V_kms=[1000.0, 1000.0 * math.sqrt(3)], V_note="SE2 sigma_Coma 1000 (1D) and x sqrt 3 (3D speed)",
                       sigma_obs=float(r["sigma"]), esig=float(r["esig"]), y_plummer=float(r["y_plummer"]), y_check=y,
                       E_v3_dmean=float(r["E_v3_dmean"]), sE=float(r["sE"]), E_old=float(r["E_old"]), Lam_floor=LFLOOR[f] / a_pc)
            row["derived"] = derived(row, f); B.append(row)
        C["cells"][f]["B1"] = dict(label="Coma UDG (SE2 cell)", body="Plummer a = R_e (S1/SE2)", rows=B)
    # ---------------- B2 MW classical dSphs (X1's rows)
    rows = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
    for f in FOOTS:
        B = []
        for r in rows:
            if r["footing"] != f or r["cls"] != "MW classical": continue
            a_pc = float(r["rh_pc"]); y = float(r["y_plummer"]); M = y * (a_pc * PC) ** 2 * A0[f] / G / MSUN
            d = float(r["d_host_kpc"]); R_m = d * KPC; xe = float(r["x_e_mid"])
            gh = g_host_x1(R_m, A0[f]); Vc = math.sqrt(gh * R_m) / 1e3
            row = dict(name=r["name"], M_b_Msun=M, M_source="X1 y_plummer a^2 a0 / G (the solver's mass)", logMstar=float(r["logMstar"]),
                       a_pc=a_pc, r_read_pc=[a_pc], d_host_kpc=d, x_e=xe, x_e_check=gh / A0[f], g_ext=xe * A0[f],
                       rho_h_Msun_pc3=rho_dyn(lambda R: g_host_x1(R, A0[f]), R_m) / MSUN_PC3,
                       rho_h_source="X1 g_host (Hernquist 6e10, A_H 3 kpc, the law): (1/4 pi G r^2) d(r^2 g)/dr at d_host",
                       V_kms=[Vc, Vc * math.sqrt(2)], V_note="MW circular speed at d_host from X1's host field, and x sqrt 2",
                       sigma_obs=float(r["sigma"]), y_plummer=y, Lam_floor=float(r["Lam_floor"]),
                       record=dict(Delta_v3_floor=float(r["Delta[v3 L*floor]"]), sd_v3_floor=float(r["sdMC[v3 L*floor]"]),
                                   Delta_v3_floor_EV=float(r["Delta[v3 L*floor E-V]"]),
                                   Delta_Newton=float(r["Delta[Newton]"]), sd_Newton=float(r["sdMC[Newton]"]),
                                   Delta_iso_AQUAL=float(r["Delta[iso AQUAL L*0]"]),
                                   Delta_AQUAL_EFE_L0=float(r["Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"]),
                                   s_i=float(r["s_i"]), k_i=float(r["k_i"])))
            row["derived"] = derived(row, f); B.append(row)
        C["cells"][f]["B2"] = dict(label="MW classical dSph (X1 cell)", body="Plummer a = r_h (X1)", rows=B)
    # ---------------- B3 / B4 host fields from QX10's loader (CE2's path)
    NS = load_qx10(); XC, GR, profile_from, glaw = NS["XC"], NS["GR"], NS["profile_from"], NS["glaw"]
    A0K = {f: A0[f] / (1e6 / KPC) for f in FOOTS}                           # (km/s)^2 / kpc
    def field_rho(host, rk, a0k):
        """law field [m/s^2] and dynamical density [Msun pc^-3] of an enclosed-baryon profile host(r_kpc) at rk."""
        gl = lambda x: glaw(GK * host(x) / x ** 2, a0k)                      # (km/s)^2/kpc
        g = gl(rk); h = 1e-3 * rk
        rho_kpc3 = (((rk + h) ** 2 * gl(rk + h)) - ((rk - h) ** 2 * gl(rk - h))) / (2 * h) / (4 * math.pi * GK * rk ** 2)
        return g * 1e6 / KPC, rho_kpc3 * 1e-9
    for f in FOOTS:
        gs, rs = [], []
        for gp in GR:
            for fst in (0.0, 1.0):
                host = profile_from([q["r_kpc"] for q in gp["pts"]], [q["M_gas"] * (1 + fst) for q in gp["pts"]], gp["g5"] * (1 + fst), gp["R5"])
                g, rho = field_rho(host, 300.0, A0K[f]); gs.append(g); rs.append(rho)
        g3, r3 = float(np.median(gs)), float(np.median(rs))
        row = dict(name="group member proxy", M_b_Msun=10 ** 10.5 * 1.2, M_source="10^10.5 Msun stars + 20 % gas (proxy assumption)",
                   a_pc=3000.0, r_read_pc=[10000.0], d_host_kpc=300.0, x_e=g3 / A0[f], g_ext=g3, rho_h_Msun_pc3=r3,
                   rho_h_source="median over the 20 Lovisari groups (CE2 path, fst 0 and 1) of the law field's dynamical density at 300 kpc",
                   g_ext_bracket=[float(np.min(gs)), float(np.max(gs))], V_kms=[300.0, 300.0 * math.sqrt(3)],
                   V_note="group sigma_1D 300 and x sqrt 3", Lam_floor=LFLOOR[f] / 3000.0)
        row["derived"] = derived(row, f); C["cells"][f]["B3"] = dict(label="group member (Lovisari cell proxy)", body="Plummer a = 3 kpc (assumption)", rows=[row])
        clusters = {}
        for z in XC: clusters.setdefault(z["name"], []).append(z)
        gs, rs = [], []
        for nm, pts in clusters.items():
            Ml, rl = pts[0]["Mb_last"]; host = profile_from([p["r_kpc"] for p in pts], [p["M_b"] for p in pts], Ml, rl)
            g, rho = field_rho(host, 500.0, A0K[f]); gs.append(g); rs.append(rho)
        g4, r4 = float(np.median(gs)), float(np.median(rs))
        row = dict(name="X-COP member proxy", M_b_Msun=1e11, M_source="1e11 Msun (criteria)", a_pc=5000.0, r_read_pc=[10000.0],
                   d_host_kpc=500.0, x_e=g4 / A0[f], g_ext=g4, rho_h_Msun_pc3=r4,
                   rho_h_source=f"median over the {len(clusters)} X-COP clusters (CE2 path) of the law field's dynamical density at 500 kpc",
                   g_ext_bracket=[float(np.min(gs)), float(np.max(gs))], V_kms=[1000.0, 1000.0 * math.sqrt(3)],
                   V_note="cluster sigma_1D 1000 and x sqrt 3", Lam_floor=LFLOOR[f] / 5000.0)
        row["derived"] = derived(row, f); C["cells"][f]["B4"] = dict(label="X-COP member (cluster member proxy)", body="Plummer a = 5 kpc (assumption)", rows=[row])
    # ---------------- B5 the Sun (AC12 / AC15 cells)
    SUN = {"canonical": dict(rho=0.0447, xe=1.15), "alt": dict(rho=0.0514, xe=2.6)}
    for f in FOOTS:
        row = dict(name="Sun", M_b_Msun=1.0, a_pc=0.0, r_read_pc=[AU / PC, 1.524 * AU / PC, 9.58 * AU / PC], r_read_names=["Earth", "Mars", "Saturn"],
                   d_host_kpc=8.2, x_e=SUN[f]["xe"], g_ext=SUN[f]["xe"] * A0[f], rho_h_Msun_pc3=SUN[f]["rho"],
                   rho_h_source="AC12/AC15 Galactic Pi (AZ37), x_e AZ37", V_kms=[220.0, 369.0], V_note="AC15's two Sun speeds",
                   bounds_ms2=dict(Earth=8.7e-15, Mars=1.4e-15, Saturn=7.0e-15), cassini_s2=5.2e-27)
        row["derived"] = derived(row, f); C["cells"][f]["B5"] = dict(label="control: the Sun", body="point mass (AC15)", rows=[row])
    return C


def table(C):
    L = []
    for f in FOOTS:
        L.append(f"[{f}] a0 {A0[f]:.4e} L* {LFLOOR[f]} pc rho_DE {C['rho_DE_Msun_pc3'][f]:.3e} Msun/pc^3")
        for k, cell in C["cells"][f].items():
            L.append(f"  {k} {cell['label']} ({cell['body']})")
            for r in cell["rows"]:
                d0, d1 = r["derived"]
                rr0 = d0["readouts"][0]; rr1 = d1["readouts"][0]
                L.append(f"    {r['name'][:20]:20s} M_b {r['M_b_Msun']:.3g} a {r['a_pc']:.4g} pc read {r['r_read_pc'][0]:.4g} pc x_e {r['x_e']:.3f} "
                         f"rho_h {r['rho_h_Msun_pc3']:.3e} (rho_h/rho_DE {r['rho_h_Msun_pc3'] / C['rho_DE_Msun_pc3'][f]:.0f}) "
                         f"V {d0['V_kms']:.0f}/{d1['V_kms']:.0f}: R_A {d0['R_A_pc']:.3g}/{d1['R_A_pc']:.3g} pc, gpar {d0['gpar']:.3g}/{d1['gpar']:.3g}, "
                         f"M_inf {d0['M_inf']:.3g}/{d1['M_inf']:.3g}, kappa_q {d0['kappa_q']:.2e}/{d1['kappa_q']:.2e}, "
                         f"restoring/inertia@read {rr0['restoring_over_inertia']:.1e}/{rr1['restoring_over_inertia']:.1e}, "
                         f"gN/gext@read {rr0['gN_over_gext']:.3g}, stiff/Legendre@read {rr0['stiffness_over_legendre']:.1e}, "
                         f"cap(2R_A)/M_b {d0['cap_2RA_over_Mb']:.1e}/{d1['cap_2RA_over_Mb']:.1e}")
    return "\n".join(L)


if __name__ == "__main__":
    C = build()
    json.dump(C, open(os.path.join(HERE, "xf1_cells.json"), "w"), indent=1, default=float)
    print(table(C))
    print("kappa = 1/2 FITTED; not theory closed.")
