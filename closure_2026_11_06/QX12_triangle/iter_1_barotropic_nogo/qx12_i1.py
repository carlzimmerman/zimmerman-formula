#!/usr/bin/env python3
"""QX12 iter_1 (FROZEN_CRITERIA.md, 7a1afa9b6b): universal-density no-go for every barotropic sector in hydrostatic
equilibrium with the cosmic sea. rho_X = H_t(D) for every system (D = depth to the sea), H nondecreasing; inside a
system rho_X is nonincreasing outward, so local <= enclosed mean (galaxy upper bound) and local >= outer shell mean
(group/cluster lower bound). A violating pair: D_A,low >= D_B,high and l_B > u_A.
    python3 qx12_i1.py            -> qx12_i1.json/.out
    python3 qx12_i1.py --mutate   -> qx12_i1_MUTATE.json/.out  (M1 planted constant-H sector; M2 bounds x1e3)
kappa = 1/2 FITTED; not theory closed; footings never pooled. SI internally; densities reported in Msun/kpc^3."""
import os, sys, json, math, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx12_i1_MUTATE" if MUT else "qx12_i1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# QX5's data, executed from its source up to its grading section (read-only reuse, as QX10 iter_2 does)
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], Q5, "exec"), NS)
sys.argv = argv0
G, MS, KPC, A0, XC, GR, EL, LE, DATA = (NS[k] for k in ("G", "MS", "KPC", "A0", "XC", "GR", "EL", "LE", "DATA"))

R = 0.11958060485606123 / 0.0215                       # omega_d / omega_b (QX7/QX10 corner)
RHO_M0 = 39.16 * MS / KPC ** 3                          # kg/m^3 (QX10's rho_m0 = 39.16 Msun/kpc^3)
RHOU = MS / KPC ** 3                                    # report unit
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * np.maximum(gN, 0.0))
def inv(g, a0): g = np.maximum(g, 0.0); return g ** 2 / (g + a0)
def r_ta(Mtot_b): return (Mtot_b * (1 + R) / (4 * math.pi / 3 * 5.55 * RHO_M0)) ** (1 / 3)
def law_tail(M, r0, r1, a0, n=600):
    if r1 <= r0: return 0.0
    rr = np.geomspace(r0, r1, n); return float(np.trapz(glaw(G * M / rr ** 2, a0), rr))

# X-COP: hydro profiles with their errors (re-read EM_FORW per radius)
XPROF = {}
for name in sorted({z["name"] for z in XC}):
    with fits.open(os.path.join(DATA, "xcop", name, f"{name}_hydro_mass.fits")) as h:
        d = h[1].data; XPROF[name] = (np.array(d["RADIUS"], float), np.array(d["M_FORW"], float), np.array(d["EM_FORW"], float))


def build(a0, plant=None):
    """Allowed (galaxy) upper bounds and required (hot) lower bounds with conservative depths. plant: rho0 (kg/m^3) of a
    planted constant-H sector (M1): every observed mass/acceleration is replaced by the law acting on baryons + sector."""
    def Mx(r): return 0.0 if plant is None else 4 * math.pi / 3 * plant * r ** 3
    A, B = [], []
    # KiDS isolated galaxies (4 mass bins, point-mass baryons)
    bins = {}
    for p in LE: bins.setdefault(round(math.log10(p["Mb"] / MS), 4), []).append(p)
    for lm, pts in bins.items():
        Mb = pts[0]["Mb"]; rows = []
        for p in pts:
            r = math.sqrt(G * Mb / p["gbar"])
            go = p["gobs"] if plant is None else float(glaw(G * (Mb + Mx(r)) / r ** 2, a0))
            rows.append((r, go, p["err"]))
        rows.sort(); rr = np.array([x[0] for x in rows]); gl = np.maximum(np.array([x[1] - 2 * x[2] for x in rows]), 0.0)
        rt = r_ta(Mb)
        for i, (r, go, e) in enumerate(rows):
            MXmax = max(float(inv(go + 2 * e, a0)) * r ** 2 / G - Mb, 0.0)
            u = 3 * MXmax / (4 * math.pi * r ** 3)
            m = (rr >= r) & (rr <= rt)
            D = float(np.trapz(gl[m], rr[m])) if m.sum() >= 2 else 0.0
            A.append(dict(src="KiDS", sys=f"bin{lm}", r_kpc=r / KPC, u=u, D=D, z_epoch="0.2-0.3"))
    # ellipticals at 2, 4, 8 Re (G7 line 10^0.15)
    for e in EL:
        rg = np.linspace(2 * e["Re"], 8 * e["Re"], 400) * KPC
        def Mtot(xk): return e["Mtot"](xk) if plant is None else float(glaw(G * (e["Mbar"](xk) * MS + Mx(xk * KPC)) / (xk * KPC) ** 2, a0)) * (xk * KPC) ** 2 / G / MS
        gt = np.array([G * Mtot(x / KPC) * MS / x ** 2 for x in rg])
        for m_ in (2, 4, 8):
            xk = m_ * e["Re"]; r = xk * KPC; Mb = e["Mbar"](xk) * MS
            gmax = G * Mtot(xk) * MS * 10 ** 0.15 / r ** 2
            MXmax = max(float(inv(gmax, a0)) * r ** 2 / G - Mb, 0.0)
            i = int(np.argmin(abs(rg - r))); D = float(np.trapz(gt[i:], rg[i:]))
            A.append(dict(src="ellipticals", sys=e["name"], r_kpc=xk, u=3 * MXmax / (4 * math.pi * r ** 3), D=D, z_epoch="<0.1"))
    # X-COP consecutive radius pairs
    byc = {}
    for z in XC: byc.setdefault(z["name"], []).append(z)
    for name, pts in byc.items():
        pts = sorted(pts, key=lambda z: z["r_kpc"]); hr, hM, hE = XPROF[name]; hrm = hr * KPC
        Mb_last, r_bl = pts[0]["Mb_last"]
        def Mobs(z): return z["M_obs"] if plant is None else float(glaw(G * (z["M_b"] * MS + Mx(z["r_kpc"] * KPC)) / (z["r_kpc"] * KPC) ** 2, a0)) * (z["r_kpc"] * KPC) ** 2 / G / MS
        hMp = hM if plant is None else np.array([float(glaw(G * (np.interp(x, [p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts]) * MS + Mx(x * KPC)) / (x * KPC) ** 2, a0)) * (x * KPC) ** 2 / G / MS for x in hr])
        Mlast = (hMp[-1] + 2 * hE[-1]) * MS
        rt = r_ta(max(Mb_last * MS, Mlast / (1 + R)))
        for z1, z2 in zip(pts[:-1], pts[1:]):
            r1, r2 = z1["r_kpc"] * KPC, z2["r_kpc"] * KPC
            Mmax1 = float(inv(G * (Mobs(z1) + 2 * z1["eM"]) * MS / r1 ** 2, a0)) * r1 ** 2 / G - z1["M_b"] * MS
            Mmin2 = float(inv(G * max(Mobs(z2) - 2 * z2["eM"], 0) * MS / r2 ** 2, a0)) * r2 ** 2 / G - z2["M_b"] * MS
            l = (Mmin2 - Mmax1) / (4 * math.pi / 3 * (r2 ** 3 - r1 ** 3))
            m = hrm >= r1
            rr = np.concatenate([[r1], hrm[m]]); MM = np.concatenate([[Mobs(z1) + 2 * z1["eM"]], hMp[m] + 2 * hE[m]]) * MS
            D = float(np.trapz(G * MM / rr ** 2, rr)) + law_tail(Mlast, hrm[-1], rt, a0)
            B.append(dict(src="X-COP", sys=name, r_kpc=z1["r_kpc"], l=l, D=D))
    # groups: shell [R2500, R500], weaker of the two stellar allowances
    for gp in GR:
        p1, p2 = gp["pts"]; r1, r2 = p1["r_kpc"] * KPC, p2["r_kpc"] * KPC
        ls = []
        for fst in (0.0, 1.0):
            Mb1, Mb2 = p1["M_gas"] * (1 + fst) * MS, p2["M_gas"] * (1 + fst) * MS
            if plant is None: Mo1, Mo2 = p1["M_obs"] * MS, p2["M_obs"] * MS
            else:
                Mo1 = float(glaw(G * (Mb1 + Mx(r1)) / r1 ** 2, a0)) * r1 ** 2 / G; Mo2 = float(glaw(G * (Mb2 + Mx(r2)) / r2 ** 2, a0)) * r2 ** 2 / G
            Mmax1 = float(inv(G * (Mo1 + 2 * p1["eM"] * MS) / r1 ** 2, a0)) * r1 ** 2 / G - Mb1
            Mmin2 = float(inv(G * max(Mo2 - 2 * p2["eM"] * MS, 0) / r2 ** 2, a0)) * r2 ** 2 / G - Mb2
            ls.append((Mmin2 - Mmax1) / (4 * math.pi / 3 * (r2 ** 3 - r1 ** 3)))
        if plant is None: Mo1, Mo2 = p1["M_obs"] * MS, p2["M_obs"] * MS
        M1h, M2h = Mo1 + 2 * p1["eM"] * MS, Mo2 + 2 * p2["eM"] * MS
        sl = math.log(M2h / M1h) / math.log(r2 / r1); rr = np.geomspace(r1, r2, 200)
        Dd = float(np.trapz(G * M1h * (rr / r1) ** sl / rr ** 2, rr))
        rt = r_ta(max(gp["g5"] * 2 * MS, M2h / (1 + R)))
        B.append(dict(src="groups", sys=gp["name"], r_kpc=p1["r_kpc"], l=min(ls), D=Dd + law_tail(M2h, r2, rt, a0)))
    return A, B


def pairs(A, B, scale=1.0, Asrc=None):
    v = []
    for b in B:
        if b["l"] <= 0: continue
        for a in A:
            if Asrc and a["src"] not in Asrc: continue
            if a["D"] >= b["D"] and b["l"] > scale * a["u"]:
                v.append(dict(A=f"{a['src']}:{a['sys']}@{a['r_kpc']:.0f}kpc", B=f"{b['src']}:{b['sys']}@{b['r_kpc']:.0f}kpc",
                              ratio=b["l"] / max(scale * a["u"], 1e-300), DA=a["D"], DB=b["D"]))
    return v


RES = dict(lane="QX12 iter_1", criteria="7a1afa9b6b", mutate=MUT, R=R, note="kappa = 1/2 FITTED; not theory closed")
P(f"QX12 iter_1 ({'MUTATE' if MUT else 'main'}): barotropic universal-density no-go. kappa = 1/2 FITTED; not theory closed.")
P(f"Samples: KiDS {len(LE)} pts, ellipticals {len(EL)}, X-COP {len(XC)} pts, groups {len(GR)}. R = {R:.3f}.")
if not MUT:
    a0 = A0["canonical"]; gg = np.geomspace(1e-14, 1e-7, 2001); ka1 = float(np.max(np.abs(glaw(inv(gg, a0), a0) / gg - 1)))
    xm = []
    for f, a in A0.items():
        xm.append(float(np.mean([math.log10(z["M_obs"] / (glaw(G * z["M_b"] * MS / (z["r_kpc"] * KPC) ** 2, a) * (z["r_kpc"] * KPC) ** 2 / G / MS)) for z in XC])))
    ka2 = 0.0
    for z in XC:
        r = z["r_kpc"] * KPC; Ml = float(glaw(G * z["M_b"] * MS / r ** 2, a0)) * r ** 2 / G
        ka2 = max(ka2, abs(float(inv(G * Ml / r ** 2, a0)) * r ** 2 / G - z["M_b"] * MS) / (z["M_b"] * MS))
    RES["KA"] = dict(KA1_inverse_maxrel=ka1, KA2_zero_sector_maxrel=ka2, KA3_xcop_plain=xm,
                     pass_=bool(ka1 <= 1e-12 and ka2 <= 1e-9 and abs(xm[0] - 0.4675) <= 1e-3 and abs(xm[1] - 0.4345) <= 1e-3))
    P(f"KA1 inverse max rel {ka1:.1e}; KA2 zero sector max rel {ka2:.1e}; KA3 X-COP plain {xm[0]:+.4f}/{xm[1]:+.4f} -> {'PASS' if RES['KA']['pass_'] else 'FAIL'}")
    RES["foot"] = {}
    for f, a0 in A0.items():
        A, B = build(a0); vp = pairs(A, B); vs = pairs(A, B, Asrc=("ellipticals",))
        Bpos = [b for b in B if b["l"] > 0]
        best = sorted(vp, key=lambda x: -x["ratio"])[:5]
        RES["foot"][f] = dict(n_A=len(A), n_B=len(B), n_B_pos=len(Bpos), n_viol=len(vp), n_viol_same_epoch=len(vs),
                              max_ratio=max([x["ratio"] for x in vp], default=0.0), max_ratio_same_epoch=max([x["ratio"] for x in vs], default=0.0),
                              top=best, top_same_epoch=sorted(vs, key=lambda x: -x["ratio"])[:3],
                              u_range=dict(KiDS=[min(a["u"] for a in A if a["src"] == "KiDS") / RHOU, max(a["u"] for a in A if a["src"] == "KiDS") / RHOU],
                                           ell=[min(a["u"] for a in A if a["src"] == "ellipticals") / RHOU, max(a["u"] for a in A if a["src"] == "ellipticals") / RHOU]),
                              l_range=dict(XCOP=[min((b["l"] for b in Bpos if b["src"] == "X-COP"), default=0) / RHOU, max((b["l"] for b in Bpos if b["src"] == "X-COP"), default=0) / RHOU],
                                           groups=[min((b["l"] for b in Bpos if b["src"] == "groups"), default=0) / RHOU, max((b["l"] for b in Bpos if b["src"] == "groups"), default=0) / RHOU]),
                              D_range=dict(KiDS=[min(a["D"] for a in A if a["src"] == "KiDS"), max(a["D"] for a in A if a["src"] == "KiDS")],
                                           ell=[min(a["D"] for a in A if a["src"] == "ellipticals"), max(a["D"] for a in A if a["src"] == "ellipticals")],
                                           XCOP=[min(b["D"] for b in B if b["src"] == "X-COP"), max(b["D"] for b in B if b["src"] == "X-COP")],
                                           groups=[min(b["D"] for b in B if b["src"] == "groups"), max(b["D"] for b in B if b["src"] == "groups")]))
        o = RES["foot"][f]
        P(f"[{f}] allowed pts {o['n_A']} (u KiDS {o['u_range']['KiDS'][0]:.3g}-{o['u_range']['KiDS'][1]:.3g}, ellipticals {o['u_range']['ell'][0]:.3g}-{o['u_range']['ell'][1]:.3g} Msun/kpc^3); "
          f"required pts with l>0 {o['n_B_pos']}/{o['n_B']} (l X-COP {o['l_range']['XCOP'][0]:.3g}-{o['l_range']['XCOP'][1]:.3g}, groups {o['l_range']['groups'][0]:.3g}-{o['l_range']['groups'][1]:.3g})")
        P(f"   depths (km/s)^2: KiDS {o['D_range']['KiDS'][0]/1e6:.3g}-{o['D_range']['KiDS'][1]/1e6:.3g}, ell {o['D_range']['ell'][0]/1e6:.3g}-{o['D_range']['ell'][1]/1e6:.3g}, "
          f"X-COP {o['D_range']['XCOP'][0]/1e6:.3g}-{o['D_range']['XCOP'][1]/1e6:.3g}, groups {o['D_range']['groups'][0]/1e6:.3g}-{o['D_range']['groups'][1]/1e6:.3g}")
        P(f"   violating pairs: {o['n_viol']} (max l_B/u_A {o['max_ratio']:.3g}); same-epoch (ellipticals only): {o['n_viol_same_epoch']} (max {o['max_ratio_same_epoch']:.3g})")
        for x in best: P(f"      {x['B']} needs > {x['ratio']:.3g} x what {x['A']} allows (D_A {x['DA']/1e6:.3g} >= D_B {x['DB']/1e6:.3g} (km/s)^2)")
    dead = all(RES["foot"][f]["n_viol"] > 0 for f in A0); dead_se = all(RES["foot"][f]["n_viol_same_epoch"] > 0 for f in A0)
    RES["label"] = ("NO VERDICT (known answer)" if not RES["KA"]["pass_"] else ("DEAD (barotropic class)" if dead else "ALIVE"))
    RES["label_same_epoch"] = "DEAD (same-epoch)" if dead_se else "ALIVE (same-epoch)"
    P(f"LABEL: {RES['label']}; same-epoch: {RES['label_same_epoch']} (label final only if MUTATE M1/M2 bite: see qx12_i1_MUTATE.out)")
else:
    RES["M"] = {}
    for f, a0 in A0.items():
        rho0 = 1e3 * RHOU
        A, B = build(a0, plant=rho0); v1 = pairs(A, B)
        A0_, B0_ = build(a0); n0 = len(pairs(A0_, B0_)); n2 = len(pairs(A0_, B0_, scale=1e3))
        RES["M"][f] = dict(M1_violations=len(v1), M1_bites=bool(len(v1) == 0), M1_l_max=max([b["l"] for b in B], default=0) / RHOU,
                           M1_u_min=min(a["u"] for a in A) / RHOU, M2_viol_before=n0, M2_viol_after=n2, M2_bites=bool(n2 < n0))
        o = RES["M"][f]
        P(f"[{f}] M1 planted constant H = 1e3 Msun/kpc^3: violations {o['M1_violations']} -> {'BITES (specific)' if o['M1_bites'] else 'DOES NOT BITE'}; "
          f"M2 bounds x1e3: {o['M2_viol_before']} -> {o['M2_viol_after']} -> {'BITES' if o['M2_bites'] else 'DOES NOT BITE'}")
    RES["all_bite"] = bool(all(v["M1_bites"] and v["M2_bites"] for v in RES["M"].values()))
    P(f"MUTATE all bite: {RES['all_bite']}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
