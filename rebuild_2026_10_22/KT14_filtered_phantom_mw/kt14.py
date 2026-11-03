#!/usr/bin/env python3
"""KT14: filtered QUMOND on the Milky Way. Phi = Phi_N[rho] + QUMOND[rho_xi] - Phi_N[rho_xi], rho_xi = 3D Gaussian (sigma xi) of rho, board law's simple nu, UX5's grid and lines. python3 kt14.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import itertools, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "UX5_mw_stellar_mass"))
import ux5_core as C
import numpy as np
from scipy.special import ive
from scipy.signal import fftconvolve
from scipy.interpolate import RegularGridInterpolator
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0; L = C.L; ns = C.ns; F = C.F; R0 = C.R0
def P(s): print(s, flush=True); OUT.append(s)
XI = [1.0] if MUT else [0.0, 0.25, 0.5, 1.0, 2.0]
def i0e(x):
    x = np.asarray(x, float); out = np.empty_like(x); b = x > 500; out[~b] = ive(0, x[~b]); xb = x[b]; out[b] = (1 + 1 / (8 * xb) + 9 / (128 * xb * xb)) / np.sqrt(2 * math.pi * xb); return out
RIN = np.arange(0.0, 80.0 + 1e-9, 0.01); WIN = np.full_like(RIN, 0.01); WIN[0] = WIN[-1] = 0.005
ROUT = np.r_[np.arange(0.0, 20.0, 0.02), np.arange(20.0, 70.0 + 1e-9, 0.1)]
ZIN = np.arange(-25.0, 25.0 + 1e-9, 0.002)
def radial_matrix(rout, rin, win, s):
    M = np.empty((len(rout), len(rin)))
    for i in range(0, len(rout), 100):
        Ro = rout[i:i + 100, None]; M[i:i + 100] = (win * rin / s ** 2) * np.exp(-(Ro - rin) ** 2 / (2 * s * s)) * i0e(Ro * rin / (s * s))
    return M
def vsmooth(h, s, dz=0.002):
    k = np.arange(-int(6 * s / dz), int(6 * s / dz) + 1) * dz; w = np.exp(-k * k / (2 * s * s)); w /= w.sum(); return fftconvolve(h, w, mode="same")
# C3
for s in (0.25, 1.0, 2.0):
    w = 1.3; M = radial_matrix(ROUT, RIN, WIN, s); f = np.exp(-RIN ** 2 / (2 * w * w)); ex = (w * w / (w * w + s * s)) * np.exp(-ROUT ** 2 / (2 * (w * w + s * s))); e = float(np.max(np.abs(M @ f - ex)) / ex.max())
    hz = vsmooth(np.exp(-ZIN ** 2 / (2 * 0.3 ** 2)), s); exz = (0.3 / math.hypot(0.3, s)) * np.exp(-ZIN ** 2 / (2 * (0.09 + s * s))); ez = float(np.max(np.abs(hz - exz)) / exz.max()); ok = e <= 1e-3 and ez <= 1e-3; fail += not ok; P(f"C3 xi {s}: radial max rel {e:.1e}, vertical {ez:.1e}: {'PASS' if ok else 'FAIL'}")
RBA, ABa, R0B, RCB, QB = ns["RHO0_B"], ns["ALPHA_B"], ns["R0_B"], ns["RCUT_B"], ns["Q_B"]; HI, H2 = ns["S0_HI"], ns["S0_H2"]
BR = np.arange(0.0, 8.0 + 1e-9, 0.01); BW = np.full_like(BR, 0.01); BW[0] = BW[-1] = 0.005; BZ = np.arange(-8.0, 8.0 + 1e-9, 0.005); BRo = np.arange(0.0, 14.0 + 1e-9, 0.02)
def bulge_shape(R, z):
    rp = np.maximum(np.sqrt(R * R + (np.abs(z) / QB) ** 2), 1e-7); return RBA / (1 + rp / R0B) ** ABa * np.exp(-(rp / RCB) ** 2)
Rs_ = np.maximum(RIN, 1e-6); HIr = HI * np.exp(-4.0 / Rs_ - Rs_ / 7.0); H2r = H2 * np.exp(-12.0 / Rs_ - Rs_ / 1.5)
HIz = 1 / (4 * 0.085) / np.cosh(np.minimum(np.abs(ZIN) / 0.17, 300)) ** 2; H2z = 1 / (4 * 0.045) / np.cosh(np.minimum(np.abs(ZIN) / 0.09, 300)) ** 2
OPS = {}
def ops(s):
    if s in OPS: return OPS[s]
    M = radial_matrix(ROUT, RIN, WIN, s); Mb = radial_matrix(BRo, BR, BW, s); B = bulge_shape(BR[:, None], BZ[None, :]); Bs = Mb @ B
    zpad = np.arange(-14.0, 14.0 + 1e-9, 0.005); Bp = np.zeros((len(BRo), len(zpad))); i0 = int(round((-8.0 + 14.0) / 0.005)); Bp[:, i0:i0 + len(BZ)] = Bs
    k = np.arange(-int(6 * s / 0.005), int(6 * s / 0.005) + 1) * 0.005; w = np.exp(-k * k / (2 * s * s)); w /= w.sum(); Bp = fftconvolve(Bp, w[None, :], mode="same")
    bI = RegularGridInterpolator((BRo, zpad), Bp, bounds_error=False, fill_value=0.0)
    mB = float(np.sum(B * (2 * math.pi * BR * BW)[:, None]) * 0.005); mBs = float(np.trapz(np.trapz(Bp, zpad, axis=1) * 2 * math.pi * BRo, BRo))
    o = OPS[s] = dict(M=M, bI=bI, HIr=M @ HIr, H2r=M @ H2r, HIz=vsmooth(HIz, s), H2z=vsmooth(H2z, s), cache={}, mB=(mB, mBs)); return o
def comp_r(o, s, rd):
    k = ("r", rd)
    if k not in o["cache"]: o["cache"][k] = o["M"] @ np.exp(-RIN / rd)
    return o["cache"][k]
def comp_z(o, s, h):
    k = ("z", h)
    if k not in o["cache"]: o["cache"][k] = vsmooth(np.exp(-np.abs(ZIN) / h) / (2 * h), s)
    return o["cache"][k]
def amps(c):
    rd = c["rd"]; p = F.params(c["sb"], c["mbb"], rd); ZT = ns["ZD_THIN"] if c.get("ht") is None else c["ht"]; ZK = ns["ZD_THICK"] if c.get("hk") is None else c["hk"]; ft = F.f_thin if c.get("fk") is None else 1 - c["fk"]; rk = rd if c.get("rdk") is None else c["rdk"]; ss = p["sig_star_R0"] * 1e6
    return dict(st=ft * ss * math.exp(R0 / rd), sk=(1 - ft) * ss * math.exp(R0 / rk), fb=p["fb"], rd=rd, rk=rk, ZT=ZT, ZK=ZK)
def rho_xi(c, s):
    a = amps(c); o = ops(s); rt, rk = comp_r(o, s, a["rd"]), comp_r(o, s, a["rk"]); zt, zk = comp_z(o, s, a["ZT"]), comp_z(o, s, a["ZK"])
    def f(R, z):
        R = np.asarray(R, float); z = np.asarray(z, float); sh = np.broadcast(R, z).shape; Rf = np.broadcast_to(R, sh).ravel(); zf = np.broadcast_to(z, sh).ravel(); I = lambda x, y, v: np.interp(x, y, v, right=0.0)
        out = a["st"] * I(Rf, ROUT, rt) * I(zf, ZIN, zt) + a["sk"] * I(Rf, ROUT, rk) * I(zf, ZIN, zk) + I(Rf, ROUT, o["HIr"]) * I(zf, ZIN, o["HIz"]) + I(Rf, ROUT, o["H2r"]) * I(zf, ZIN, o["H2z"]) + a["fb"] * o["bI"](np.c_[Rf, zf])
        return out.reshape(sh)
    return f
def solve(c, s, a0, g, Mu, LU):
    rhof, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); PhiN = LU.newton(rho1)
    if s == 0.0: Phi = LU.qumond(PhiN)
    else:
        fx = rho_xi(c, s); rx = g.rho_axisym(lambda R, z: fx(R, z) / Mu, nq=4); PNx = LU.newton(rx); Phi = PhiN if MUT else PhiN + LU.qumond(PNx) - PNx
    oN = ns["mw_obs"](g, PhiN, a0); q = C.field_lines(g, Phi, a0); return dict(N=dict(vc=oN["vc_R0"], K0=oN["K_R0"]), Q=q, Mstar=ms)
HT, HK, FK = (0.25, 0.30, 0.35), (0.72, 0.90, 1.08), (0.12, 0.26, 0.35)
def cells():
    for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID): yield dict(box="B175", sb=sb, mbb=mbb, rd=rd)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID, HT, HK, FK): yield dict(box="BV", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk)
    for sb, mbb, rd, ht, hk, fk in itertools.product(L.SIG_B_GRID, L.MBB_GRID, [L.RD_GRID[2], L.RD_GRID[3], L.RD_GRID[4]], HT, HK, FK): yield dict(box="BV2", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk, rdk=2.0)
for foot in ("canonical", "alt"):
    a0 = C.A0[foot]; g, Mu = C.grid(a0); LU = C.Lapl(g); C.nu = C.nu; st = [json.loads(l) for l in open(os.path.join(RB, "UX5_mw_stellar_mass", "cache", f"{foot}_1.0.jsonl"))]
    IP = []
    for c, sx in zip(cells(), st):
        _, ms = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        if L.RD_TAG[0] <= c["rd"] <= L.RD_TAG[1] and L.MSTAR_TAG[0] <= ms <= L.MSTAR_TAG[1]: IP.append((c, sx))
    P(f"\n[{foot}] in-prior cells {len(IP)}"); R = RES[foot] = {}
    for s in XI:
        OPS.clear()
        if s > 0:
            for nm, c in (("first in-prior cell", IP[0][0]), ("shortest disc, heaviest bulge", max(IP, key=lambda t: (t[0]["mbb"], -t[0]["rd"]))[0])):
                f = rho_xi(c, s); rf, _ = C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); m1 = float(np.sum(g.rho_axisym(lambda R_, z_: f(R_, z_) / Mu, nq=4) * g.vol)); m0 = float(np.sum(g.rho_axisym(lambda R_, z_: rf(R_, z_) / Mu, nq=4) * g.vol)); e = abs(m1 / m0 - 1)
                ob = ops(s)["mB"]; eb = abs(ob[1] / ob[0] - 1); ok = e <= 1e-3 and eb <= 1e-3; fail += (not ok) and not MUT; P(f"C2 [{foot}] xi {s} {nm}: solver-grid mass ratio - 1 {m1 / m0 - 1:+.1e}; bulge fine-grid {ob[1] / ob[0] - 1:+.1e}: {'PASS' if ok else 'FAIL'}")
        rows = []
        for c, sx in IP:
            o = solve(c, s, a0, g, Mu, LU); o.update(c); rows.append(o)
        if s == 0.0:
            e = max(max(abs(o["Q"]["vc"] / sx["Q"]["vc"] - 1), abs(o["Q"]["K0"] / sx["Q"]["K0"] - 1)) for o, (_, sx) in zip(rows, IP)); ok = e <= 1e-6; fail += not ok; P(f"C1 [{foot}] xi 0 vs UX5/KT13 simple, max rel {e:.1e}: {'PASS' if ok else 'FAIL'}")
        q = [o["Q"] for o in rows]; n4 = [o for o in rows if all(o["Q"][l] for l in ("L1", "L2a", "L2b", "L3"))]; cnt = {l: sum(x[l] for x in q) for l in ("L1", "L2a", "L2b", "L3", "Lh")}
        b = min(rows, key=lambda o: o["Q"]["D"]); bq = b["Q"]; kl1 = min((x["K0"] for x in q if x["L1"]), default=None)
        R[str(s)] = dict(n_pass=len(n4), strict=sum(o["Q"]["Lh"] for o in n4), lines=cnt, K_min_L1=kl1, vc_max=max(x["vc"] for x in q), best={k: b.get(k) for k in ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk", "Mstar")} | {k: bq[k] for k in ("vc", "K0", "cK", "cO", "h", "D")}, passing=[{k: o.get(k) for k in ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk", "Mstar")} | {k: o["Q"][k] for k in ("vc", "K0", "cK", "cO", "h")} for o in sorted(n4, key=lambda o: o["Q"]["D"])][:30])
        P(f"[{foot}] xi {s}: all four {len(n4)} (strict h {R[str(s)]['strict']}); L1 {cnt['L1']} L2a {cnt['L2a']} L2b {cnt['L2b']} L3 {cnt['L3']} Lh {cnt['Lh']}; v_c max {R[str(s)]['vc_max']:.1f}; lowest K with v_c in line {('%.1f' % kl1) if kl1 else 'none'}; best D {bq['D']:.2f} ({b['box']} Rd {b['rd']:.2f} Sb {b['sb']} Mbb {b['mbb']:.3g} ht {b.get('ht')} hk {b.get('hk')} fk {b.get('fk')} M* {b['Mstar']:.3g}) v_c {bq['vc']:.1f} K {bq['K0']:.1f} cK {bq['cK']:.1f} Ou {bq['cO']:.0f} h {bq['h']:.2f}")
        if n4 and not MUT:
            c0 = min(n4, key=lambda o: o["Q"]["D"]); gh, _ = C.grid(a0, hi=True); LH = C.Lapl(gh); o1 = solve({k: c0[k] for k in ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk") if k in c0}, s, a0, gh, Mu, LH); dK = o1["Q"]["K0"] - c0["Q"]["K0"]; dv = o1["Q"]["vc"] - c0["Q"]["vc"]; R[str(s)]["Q5"] = dict(dK=dK, dv=dv); P(f"    Q5 doubled grid on best passing cell: dK {dK:+.2f} dv {dv:+.2f}{' [GRID-DEPENDENT]' if abs(dK) > 1 else ''}")
    ps = [s for s in XI if R[str(s)]["n_pass"]]; lab = f"FILTER PASSES MW at xi = {min(ps)} kpc (passing xi {ps})" if ps else "NO XI PASSES"; R["label"] = lab; P(f"LABEL [{foot}]: {lab}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt14{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt14{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or fail) else 0)
