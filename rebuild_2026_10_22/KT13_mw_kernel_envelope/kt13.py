#!/usr/bin/env python3
"""KT13: eight QUMOND kernels on the Milky Way's in-prior cells, UX5's form Q, boxes and lines unchanged. python3 kt13.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import itertools, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "UX5_mw_stellar_mass"))
import ux5_core as C
import numpy as np
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0; L = C.L
def P(s): print(s, flush=True); OUT.append(s)
Y = lambda y: np.maximum(np.asarray(y, float), 1e-300)
def bis(f, y, lo, hi, n=90):
    for _ in range(n):
        m = 0.5 * (lo + hi); s = f(m) < y; lo = np.where(s, m, lo); hi = np.where(s, hi, m)
    return 0.5 * (lo + hi)
def nu_n(n): return lambda y, mut=False: (0.5 * (1 + np.sqrt(1 + 4 * Y(y) ** -n))) ** (1 / n)
def nu_sharp(y, mut=False): return np.maximum(1.0, Y(y) ** -0.5)
def nu_rar(y, mut=False): return 1 / -np.expm1(-np.sqrt(Y(y)))
def nu_mu2(y, mut=False):
    y = Y(y); return bis(lambda x: x * (1 - (1 + x / 2) ** -2), y, np.sqrt(y) * 0.5, y + 4.0) / y
def nu_compact(y, mut=False):
    y = Y(y); out = np.ones_like(y); s = y < 2.0
    if s.any(): out[s] = bis(lambda x: x * x * (1 - x / 4), y[s], np.sqrt(y[s]), np.full(s.sum(), 2.0)) / y[s]
    return out
KER = {"simple": C.nu, "nu_2": nu_n(2), "nu_3": nu_n(3), "nu_6": nu_n(6), "sharp": nu_sharp, "RAR": nu_rar, "OR mu_2": nu_mu2, "compact": nu_compact}
MU = {"simple": lambda x: x / (1 + x), "nu_2": lambda x: x / (1 + x ** 2) ** .5, "nu_3": lambda x: x / (1 + x ** 3) ** (1 / 3), "nu_6": lambda x: x / (1 + x ** 6) ** (1 / 6), "sharp": lambda x: np.minimum(x, 1.0), "OR mu_2": lambda x: 1 - (1 + x / 2) ** -2, "compact": lambda x: np.where(x <= 2, x - x * x / 4, 1.0)}
yy = np.geomspace(1e-4, 100, 300)
for k, mu in MU.items():
    x = yy * KER[k](yy); e = float(np.max(np.abs(x * mu(x) / yy - 1))); ok = e <= 1e-8; fail += not ok; P(f"C3 {k}: max |x mu(x)/y - 1| {e:.1e}: {'PASS' if ok else 'FAIL'}")
r = KER["RAR"](yy); ok = bool(np.all(np.diff(r) < 0) and abs(r[-1] - 1) < 1e-4 and abs(r[0] * yy[0] ** .5 - 1) < 0.01); fail += not ok; P(f"C3 RAR: monotone, nu(100) {r[-1]:.6f}, sqrt(y) nu at 1e-4 {r[0] * yy[0] ** .5:.4f}: {'PASS' if ok else 'FAIL'}")
if MUT: KER = {"Newton": lambda y, mut=False: np.ones_like(Y(y))}
HT, HK, FK = (0.25, 0.30, 0.35), (0.72, 0.90, 1.08), (0.12, 0.26, 0.35)
def cells():
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID): yield dict(box="B175", sb=sb, mbb=mbb, rd=rd)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID, HT, HK, FK): yield dict(box="BV", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, [L.RD_GRID[2], L.RD_GRID[3], L.RD_GRID[4]], HT, HK, FK): yield dict(box="BV2", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk, rdk=2.0)
KEYS = ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk")
for foot in ("canonical", "alt"):
    a0 = C.A0[foot]; g, Mu = C.grid(a0); LU = C.Lapl(g); st = [json.loads(l) for l in open(os.path.join(RB, "UX5_mw_stellar_mass", "cache", f"{foot}_1.0.jsonl"))]
    IP = []
    for c, s in zip(cells(), st):
        rhof, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        if L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]: IP.append((c, rhof, ms, s))
    P(f"\n[{foot}] in-prior cells {len(IP)}"); R = RES[foot] = {}
    for kn, nu in KER.items():
        C.nu = nu; rows = []
        for c, rhof, ms, s in IP:
            o = C.solve(rhof, a0, g, Mu, LU, "Q"); o.update({k: c[k] for k in KEYS if k in c}); o["Mstar"] = ms; rows.append(o)
        if kn == "simple" and not MUT:
            e = max(max(abs(o["Q"]["vc"] / s["Q"]["vc"] - 1), abs(o["Q"]["K0"] / s["Q"]["K0"] - 1)) for o, (_, _, _, s) in zip(rows, IP)); ok = e <= 1e-6; fail += not ok; P(f"C1 [{foot}] simple vs UX5 form Q, {len(rows)} cells, max rel {e:.1e}: {'PASS' if ok else 'FAIL'}")
        if kn == "compact" and not MUT:
            k12 = json.load(open(os.path.join(RB, "KT12_compact_kernel_milky_way", "kt12.json")))[foot]; e = 0.0
            for box in ("B175", "BV", "BV2"):
                b = k12[box]["best_ip"]; m = [o for o in rows if all(o.get(k) == b.get(k) for k in ("sb", "mbb", "rd", "ht", "hk", "fk", "rdk")) and o["box"] == box][0]; e = max(e, abs(m["Q"]["vc"] / b["vc"] - 1), abs(m["Q"]["K0"] / b["K0"] - 1))
            ok = e <= 1e-6; fail += not ok; P(f"C2 [{foot}] compact vs KT12 in-prior best cells, max rel {e:.1e}: {'PASS' if ok else 'FAIL'}")
        q = [o["Q"] for o in rows]; n4 = sum(all(x[l] for l in ("L1", "L2a", "L2b", "L3")) for x in q); cnt = {l: sum(x[l] for x in q) for l in ("L1", "L2a", "L2b", "L3")}
        b = min(rows, key=lambda o: o["Q"]["D"]); bq = b["Q"]; kp = bq["K0"] * (L.VC_BRIEF / bq["vc"]) ** 2; kl1 = min((x["K0"] for x in q if x["L1"]), default=None); vmax = max(x["vc"] for x in q)
        R[kn] = dict(n_pass=n4, lines=cnt, vc_max=vmax, K_min_L1=kl1, best={k: b.get(k) for k in KEYS + ("Mstar",)} | {k: bq[k] for k in ("vc", "K0", "cK", "cO", "h", "D")} | {"vN": b["N"]["vc"], "KN": b["N"]["K0"], "K_proj": kp})
        P(f"[{foot}] {kn:8s}: all four {n4}; L1 {cnt['L1']} L2a {cnt['L2a']} L2b {cnt['L2b']} L3 {cnt['L3']}; v_c max {vmax:.1f}; lowest K with v_c in line {('%.1f' % kl1) if kl1 else 'none'}; best D {bq['D']:.2f} ({b['box']} Rd {b['rd']:.2f} Sb {b['sb']} M* {b['Mstar']:.3g}) v_c {bq['vc']:.1f} (N {b['N']['vc']:.1f}) K {bq['K0']:.1f} (N {b['N']['K0']:.1f}) Ou {bq['cO']:.0f} K_proj {kp:.1f}")
        if n4 and not MUT:
            pc = [o for o in rows if all(o["Q"][l] for l in ("L1", "L2a", "L2b", "L3"))]; c0 = min(pc, key=lambda o: o["Q"]["D"]); gh, _ = C.grid(a0, hi=True); LH = C.Lapl(gh); rh, _ = C.rho_struct(c0["sb"], c0["mbb"], c0["rd"], c0.get("ht"), c0.get("hk"), c0.get("fk"), c0.get("rdk")); o1 = C.solve(rh, a0, gh, Mu, LH, "Q"); dK = o1["Q"]["K0"] - c0["Q"]["K0"]; R[kn]["Q5_dK"] = dK; P(f"    Q5 doubled grid on passing cell: dK {dK:+.2f}{' [GRID-DEPENDENT]' if abs(dK) > 1 else ''}")
    found = [k for k in KER if R[k]["n_pass"]]; lab = ("KERNEL FOUND: " + ", ".join(found)) if found else "NO KERNEL IN FAMILY"; R["label"] = lab; P(f"LABEL [{foot}]: {lab}")
    if not found: bnd = all((R[k]["K_min_L1"] or 1e9) > 70.8 for k in KER); R["baryon_set"] = bnd; P(f"[{foot}] every kernel's lowest K with v_c in line above 70.8 (or no v_c): {bnd}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt13{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt13{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or fail) else 0)
