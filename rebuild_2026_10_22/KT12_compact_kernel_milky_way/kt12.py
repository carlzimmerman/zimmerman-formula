#!/usr/bin/env python3
"""KT12: compact kernel mu = x - x^2/4 (x <= 2), 1 above, on the Milky Way through UX5's form Q (QUMOND), boxes and lines unchanged. python3 kt12.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import itertools, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "UX5_mw_stellar_mass"))
import ux5_core as C
import numpy as np
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
LAW = C.nu
def x_of(y):
    y = np.asarray(y, float); lo = np.sqrt(np.minimum(y, 2.0)); hi = np.full_like(y, 2.0)
    for _ in range(64):
        m = 0.5 * (lo + hi); f = m * m * (1 - m / 4) - y; lo = np.where(f < 0, m, lo); hi = np.where(f < 0, hi, m)
    x = 0.5 * (lo + hi)
    for _ in range(3): x = x - (x * x * (1 - x / 4) - y) / np.maximum(2 * x - 0.75 * x * x, 1e-30)
    return x
def nu_compact(y, mut=False):
    y = np.maximum(np.asarray(y, float), 1e-300)
    if mut or MUT: return np.ones_like(y)
    out = np.ones_like(y); s = y < 2.0; out[s] = x_of(y[s]) / y[s]; return out
def nu_mu2(y, mut=False):
    y = np.maximum(np.asarray(y, float), 1e-300); lo = np.sqrt(y) * 0.5; hi = y + 4.0
    for _ in range(80):
        m = 0.5 * (lo + hi); f = m * (1 - (1 + m / 2) ** -2) - y; lo = np.where(f < 0, m, lo); hi = np.where(f < 0, hi, m)
    return 0.5 * (lo + hi) / y
# C2 inversion
yy = np.geomspace(1e-6, 10, 400); xx = np.where(yy < 2, x_of(np.minimum(yy, 2)), yy); mu = np.where(xx <= 2, xx - xx * xx / 4, 1.0); e2 = float(np.max(np.abs(xx * mu / yy - 1))); ok = e2 <= 1e-12; fail += not ok; P(f"C2 inversion max rel {e2:.1e}: {'PASS' if ok else 'FAIL'}"); RES["C2"] = e2
L = C.L; HT, HK, FK = (0.25, 0.30, 0.35), (0.72, 0.90, 1.08), (0.12, 0.26, 0.35)
def cells():
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID): yield dict(box="B175", sb=sb, mbb=mbb, rd=rd)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID, HT, HK, FK): yield dict(box="BV", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, [L.RD_GRID[2], L.RD_GRID[3], L.RD_GRID[4]], HT, HK, FK): yield dict(box="BV2", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk, rdk=2.0)
def run(c, a0, g, Mu, LU):
    rhof, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); o = C.solve(rhof, a0, g, Mu, LU, "Q"); o.update({k: c[k] for k in ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk") if k in c}); o["Mstar"] = ms; o["inp"] = bool(L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]); return o
def cls(rows):
    f = "Q"; a = [r for r in rows if all(r[f][l] for l in ("L1", "L2a", "L2b", "L3"))]; vk = [r for r in rows if all(r[f][l] for l in ("L1", "L2a", "L2b"))]; ip = [r for r in a if r["inp"]]
    c = "FEASIBLE IN PRIORS" if ip else "FEASIBLE (WIDE PRIORS ONLY)" if a else "V+K ONLY" if vk else "INFEASIBLE"; pr = [r for r in rows if r["inp"]]
    ds = lambda r: {k: r.get(k) for k in ("sb", "mbb", "rd", "ht", "hk", "fk", "rdk", "Mstar")} | {k: r[f][k] for k in ("vc", "K0", "cK", "cO", "h", "D", "L1", "L2a", "L2b", "L3")} | {"vN": r["N"]["vc"], "KN": r["N"]["K0"]} if r else None
    b = min(rows, key=lambda r: r[f]["D"]); bi = min(pr, key=lambda r: r[f]["D"]) if pr else None
    cnt = {l: sum(r[f][l] for r in pr) for l in ("L1", "L2a", "L2b", "L3")}
    return dict(cls=c, n=len(rows), n_all=len(a), n_ip=len(ip), n_VK=len(vk), strict=sum(r[f]["Lh"] for r in a), best=ds(b), best_ip=ds(bi), inprior_line_counts=cnt, n_prior=len(pr), vc_ip=[min(r[f]["vc"] for r in pr), max(r[f]["vc"] for r in pr)] if pr else None, ip_cells=[ds(r) for r in ip][:20])
for foot in ("canonical", "alt"):
    a0 = C.A0[foot]; g, Mu = C.grid(a0); LU = C.Lapl(g)
    if not MUT:
        C.nu = LAW; st = [json.loads(l) for l in open(os.path.join(os.path.dirname(HERE), "UX5_mw_stellar_mass", "cache", f"{foot}_1.0.jsonl"))][:175]; e1 = 0.0
        for c, s in zip(cells(), st):
            o = run(c, a0, g, Mu, LU); e1 = max(e1, abs(o["Q"]["vc"] / s["Q"]["vc"] - 1), abs(o["Q"]["K0"] / s["Q"]["K0"] - 1))
        ok = e1 <= 1e-6; fail += not ok; RES[f"C1_{foot}"] = e1; P(f"C1 [{foot}] law nu reproduces UX5 form Q on B175, max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
        C.nu = nu_mu2; r2 = [run(c, a0, g, Mu, LU) for c, _ in zip(cells(), range(175))]; k2 = cls(r2); RES[f"mu2_{foot}"] = k2; b = k2["best_ip"]; P(f"[{foot}] comparison mu_2, B175: {k2['cls']}; in-prior best D {b['D']:.2f} vc {b['vc']:.1f} K {b['K0']:.1f} Ou {b['cO']:.0f}")
    C.nu = nu_compact
    if foot == "canonical" and not MUT:
        M = 6e10 / Mu; a = 3.0; PS = C.PS
        def field(Phi, R, Z):
            dr, dt = g.grad_cells(Phi); dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt; dR = np.sin(g.t2d) * dr + np.cos(g.t2d) * dt; return g.interp_cells(dR, R, Z), g.interp_cells(dz, R, Z)
        rho1 = g.rho_axisym(lambda R, z: (3 * M / (4 * math.pi * a ** 3)) * (1 + (R * R + z * z) / a ** 2) ** -2.5, nq=4); PQ = LU.qumond(LU.newton(rho1))
        r = np.geomspace(a, 30 * a, 12); th = math.radians(60); gN = M * r / (r * r + a * a) ** 1.5; fR, fz = field(PQ, r * math.sin(th), r * math.cos(th)); e3 = float(np.max(np.abs(np.hypot(fR, fz) / (nu_compact(gN) * gN) - 1))); ok = e3 <= 0.01; fail += not ok; RES["C3"] = e3; P(f"C3 Plummer compact form Q max rel {e3:.4f}: {'PASS' if ok else 'FAIL'}")
        A = 3.0; eps = 0.02; rho2 = g.rho_axisym(lambda R, z: (M * A / (2 * math.pi * (R * R + A * A) ** 1.5)) * np.exp(-np.abs(z) / eps) / (2 * eps), nq=4); PQ = LU.qumond(LU.newton(rho2))
        Rq = np.array([4., 6., 8., 10., 12.]); Zq = np.full(5, 1.1); dd = Rq * Rq + (Zq + A) ** 2; gNk = M / dd; ez = nu_compact(gNk) * gNk * (Zq + A) / np.sqrt(dd); fR, fz = field(PQ, Rq, Zq); e4 = float(np.max(np.abs(fz / ez - 1))); ok = e4 <= 0.02; fail += not ok; RES["C4"] = e4; P(f"C4 Kuzmin compact form Q K(1.1) max rel {e4:.4f}; y range {gNk.min():.2f}-{gNk.max():.2f}: {'PASS' if ok else 'FAIL'}")
    rows = [run(c, a0, g, Mu, LU) for c in cells()]; R = RES[foot] = {}
    for box in ("B175", "BV", "BV2"):
        k = cls([r for r in rows if r["box"] == box]); R[box] = k; b, bi = k["best"], k["best_ip"]
        P(f"[{foot}] {box} compact: {k['cls']}; n {k['n']} all4 {k['n_all']} in-prior {k['n_ip']} V+K {k['n_VK']} strict {k['strict']}; in-prior cells {k['n_prior']}, lines passed L1 {k['inprior_line_counts']['L1']} L2a {k['inprior_line_counts']['L2a']} L2b {k['inprior_line_counts']['L2b']} L3 {k['inprior_line_counts']['L3']}; in-prior vc range {k['vc_ip'][0]:.1f}-{k['vc_ip'][1]:.1f}")
        P(f"    best D {b['D']:.2f} Rd {b['rd']:.2f} Sb {b['sb']} Mbb {b['mbb']:.3g} M* {b['Mstar']:.3g} vc {b['vc']:.1f} (N {b['vN']:.1f}) K {b['K0']:.1f} (N {b['KN']:.1f}) cK {b['cK']:.1f} Ou {b['cO']:.0f} h {b['h']:.2f}")
        P(f"    in-prior best D {bi['D']:.2f} Rd {bi['rd']:.2f} Sb {bi['sb']} Mbb {bi['mbb']:.3g} M* {bi['Mstar']:.3g} vc {bi['vc']:.1f} (N {bi['vN']:.1f}) K {bi['K0']:.1f} (N {bi['KN']:.1f}) cK {bi['cK']:.1f} Ou {bi['cO']:.0f} h {bi['h']:.2f} lines {[l for l in ('L1','L2a','L2b','L3') if bi[l]]}")
    vcmax = max(r["Q"]["vc"] for r in rows if r["inp"]); R["vc_max_inprior"] = vcmax; P(f"[{foot}] highest in-prior v_c {vcmax:.1f} against line {L.VC_BRIEF} - {L.VC_BRIEF_LINE}")
    if not MUT:
        b = min((r for r in rows if r["inp"]), key=lambda r: r["Q"]["D"]); gh, _ = C.grid(a0, hi=True); LH = C.Lapl(gh); o1 = run(b, a0, gh, Mu, LH); dK = o1["Q"]["K0"] - b["Q"]["K0"]; dv = o1["Q"]["vc"] - b["Q"]["vc"]; R["Q5"] = dict(dK=dK, dv=dv); P(f"Q5 [{foot}] in-prior best on doubled grid: dK {dK:+.2f} dv {dv:+.2f}{' [GRID-DEPENDENT]' if abs(dK) > 1 else ''}")
    ks = [R[b]["cls"] for b in ("B175", "BV", "BV2")]; lab = "MW PASSES IN PRIORS" if "FEASIBLE IN PRIORS" in ks else "MW WIDE PRIORS ONLY" if all(k == "FEASIBLE (WIDE PRIORS ONLY)" for k in ks) else "MW FAILS" if all(k in ("V+K ONLY", "INFEASIBLE") for k in ks) else "MIXED: " + ", ".join(ks); R["label"] = lab; P(f"LABEL [{foot}]: {lab}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt12{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt12{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or fail) else 0)
