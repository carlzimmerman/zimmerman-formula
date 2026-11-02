#!/usr/bin/env python3
"""MX1 physics rows P1, P1b, P3-P8, DiskMass lane row, K3, K4, K8. MX1_MUTATE=1 is the twin: a0 x 1.5, share x 0.5. Reinstates nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, csv, glob, contextlib, io, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); sys.path.insert(0, HERE)
import mx1_core as M
MUT = M.MUT; TAG = "_MUTATE" if MUT else ""; OUT = open(os.path.join(HERE, f"mx1_phys{TAG}.out"), "w"); RES = {}
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CH = {}
def check(n, ok, d): CH[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
A0F = {"canonical": 9.3603e-11 * (1.5 if MUT else 1), "alt": 1.1312e-10 * (1.5 if MUT else 1)}; FEET = tuple(A0F); G, MS, PC = M.GN, M.MSUN, M.PCM; KPC = PC * 1e3; MPC = PC * 1e6; GYR = 3.156e16; law = M.law
ref_a = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
say("=" * 90); say("MX1 physics" + (" [MUTATE]" if MUT else "")); say("=" * 90)
# ---------- K3, K4
class Iso:
    R = 3e21; M = 1.0; cap = True
    def __init__(s, slope, Rv): s.k = slope; s.R = Rv; s.M = slope * Rv / M.FCOLD
    def M0(s, r): return s.k * np.asarray(r, float)
rq = np.geomspace(3e19, 3e21, 30); Mp = 1e10; k_ = 1e11 / 3e21; iso = Iso(k_, 3e21); Mtot = iso.M * M.FCOLD; F = 0.1; Mb_tot = F * Mtot; ra = np.geomspace(1e15, 1e24, 400); ma = np.full_like(ra, Mb_tot)
cnum = M.contracted(rq, iso, ra, ma, Mb_tot, 1.0); ri = np.geomspace(1e18, 3e22, 4000); rf_exact = ri * ri * k_ * (1 + F) / (Mb_tot + k_ * ri); cexact = np.interp(np.log(rq), np.log(rf_exact), k_ * ri); dev = float(np.max(np.abs(cnum / cexact - 1)))
check("K3", dev <= 1e-3, f"contraction, isothermal halo, central point mass: max rel dev {dev:.2e}")
dev4 = 0.0; dr = 0.0
for lg in (10.5, 12.0, 13.0, 14.5):
    h = M.Halo(10 ** lg); dev4 = max(dev4, abs(float(h.M0(h.R)) / (5.35 / 6.35 * h.M) - 1)); dr = max(dr, abs(h.M / (800 / 3 * math.pi * M.RHOC * h.R ** 3) - 1))
check("K4", dev4 <= 3e-3 and dr <= 1e-9, f"M_c(<R200)/(5.35/6.35 M200) dev {dev4:.2e}; R200 consistency {dr:.2e}")
# ---------- P1 aligned loop
def B(g, a): return law(g, a) - g
def Binv(g2, a): return g2 * g2 / (a - g2)
def force(g1, g2, a, tw=False):
    Lz = law(g1, a) > g1 + g2; f1 = np.where(Lz, law(g1, a), g1 + g2); f2 = np.where(Lz, (g1 + g2) if tw else a * g2 / (a - g2), g1 + g2); return f1, f2
def Qf(g1, g2, a):
    u = .5 * g1 + a; s = np.sqrt(np.maximum(u * u - a * a, 0)); A = .25 * g1 * g1 + u * s - a * a * np.log((u + s) / a); h = a * (-g2 - a * np.log1p(-np.minimum(g2 / a, 1 - 1e-13))); return A + h, .5 * (g1 + g2) ** 2
def loop(cx, cy, w, a, tw):
    t = np.linspace(0, 2 * math.pi, 200001); g1 = cx * np.exp(w * np.cos(t)); g2 = cy * np.exp(w * np.sin(t)); f1, f2 = force(g1, g2, a, tw); dI = .5 * (f1[:-1] + f1[1:]) * np.diff(g1) + .5 * (f2[:-1] + f2[1:]) * np.diff(g2); return float(abs(dI.sum()) / np.abs(dI).sum())
P1 = {}
for f in FEET:
    a = A0F[f]; pts = []
    for x in (.03, .1, .3, 1, 3, 10):
        y = float(B(np.array(x * a), a)); pts.append(loop(x * a, y, .35, a, False))
    tw = [loop(x * a, float(B(np.array(x * a), a)), .35, a, True) for x in (.03, .1, .3, 1, 3, 10)]; P1[f] = dict(rel=pts, twin=tw); say(f"  P1 {f}: loop |closed integral|/path, across the boundary: " + " ".join(f"{v:.1e}" for v in pts) + " ; twin, cold force g1 + g2 in the law zone: " + " ".join(f"{v:.1e}" for v in tw))
check("K8", max(max(P1[f]["rel"]) for f in FEET) <= 1e-6 and min(min(P1[f]["twin"]) for f in FEET) > 1e-4, "parent's loop closes within 1e-6; twin doesn't")
# touching: Q_L - Q_C on aligned grid
a = A0F["canonical"]; g1 = np.geomspace(1e-3, 1e2, 400)[:, None] * a; g2 = np.geomspace(1e-3, .999, 400)[None, :] * a; QL, QC = Qf(g1, g2, a); frac = float(np.mean(QL >= QC * (1 - 1e-9))); gb_ = g1[:, 0]; b_ = B(gb_, a); QLb, QCb = Qf(gb_, b_, a); say(f"  P1 aligned: share of (g1, g2) with Q_L >= Q_C: {frac:.5f}; on the boundary, max |Q_L - Q_C|/Q_C {float(np.max(np.abs(QLb / QCb - 1))):.2e}")
# P1b: boundary jump vs angle
P1b = {}
for f in FEET:
    a = A0F[f]; row = {}
    for x in (.1, 1, 10):
        g = x * a; Lv = float(law(np.array(g), a)); out = []
        for th in (0, 30, 60, 90, 120, 150, 179):
            c = math.cos(math.radians(th)); # |g1 + g2| = L: g2^2 + 2 g g2 c + g^2 = L^2
            g2 = -g * c + math.sqrt(max(g * g * c * c - g * g + Lv * Lv, 0)); ql, qc = Qf(np.array(g), np.array(min(g2, a * (1 - 1e-13))), a); out.append((th, g2 / a, float(ql / qc - 1) if g2 < a else float("inf")))
        row[str(x)] = out; say(f"  P1b {f} g1 {x} a0: theta, g2/a0, Q_L/Q_C - 1: " + " ".join(f"{t}:{q:.2f},{v:+.3f}" for t, q, v in out))
    P1b[f] = row
RES["P1"] = P1; RES["P1b"] = P1b; RES["Q_touch"] = frac
# frozen form: zone by Q_max against the rule, angles
rng = np.random.default_rng(1); a = A0F["canonical"]; g1 = a * 10 ** rng.uniform(-3, 2, 200000); g2 = a * 10 ** rng.uniform(-3, -1e-3, 200000); c = rng.uniform(-1, 1, 200000); Cm = np.sqrt(g1 * g1 + g2 * g2 + 2 * g1 * g2 * c); QL, _ = Qf(g1, g2, a); ruleC = Cm > law(g1, a); qC = .5 * Cm * Cm > QL; RES["Qzone_diff"] = float(np.mean(ruleC != qC)); RES["rule_cold_share"] = float(ruleC.mean()); RES["Q_cold_share"] = float(qC.mean()); say(f"  P1 frozen form: cells where Q_max's zone differs from the rule's {RES['Qzone_diff']:.3f}; rule's cold zone {RES['rule_cold_share']:.3f}, Q_max's {RES['Q_cold_share']:.4f}")
# ---------- P3 reciprocity
GQ = np.polynomial.legendre.leggauss(64)
def P3(delta_kpc, a0, Mb=6e10, ab=3.0):
    """Axisymmetric about x; baryons Plummer at 0, cold native at x = delta. Net x force on all matter under universal coupling."""
    h = M.Halo((1 + M.SHARE) * Mb); d = delta_kpc * KPC; ab_ = ab * KPC; rr = np.geomspace(0.01 * KPC, h.R, 500); Mc = h.M0(rr); lr = np.log(rr)
    def fb(x, y):
        q = x * x + y * y + ab_ * ab_; f = -G * Mb * MS / q ** 1.5; return f * x, f * y
    def fc(x, y):
        s = np.sqrt((x - d) ** 2 + y * y); s2 = np.maximum(s, rr[0]); f = -G * np.interp(np.log(s2), lr, Mc) * MS / s2 ** 3; return f * (x - d), f * y
    def rules(x, y):
        bx, by = fb(x, y); cx, cy = fc(x, y); gb = np.hypot(bx, by); L = law(gb, a0); Cx, Cy = bx + cx, by + cy; Cm = np.hypot(Cx, Cy); z = Cm > L; lx, ly = bx * L / np.maximum(gb, 1e-300), by * L / np.maximum(gb, 1e-300); Tx, Ty = Cx + cx * 0, Cy + cy * 0
        tot = Cx + 0, Cy + 0
        return dict(Newton=Cx, MAX=np.where(z, Cx, lx), Law_all=(Cx * law(Cm, a0) / np.maximum(Cm, 1e-300)), Mz=z.mean())
    cth, wth = GQ; out = {}
    # baryons: dm over Plummer
    rb = np.geomspace(0.01 * ab_, 300 * ab_, 500); dMb = np.gradient(Mb * rb ** 3 / (rb * rb + ab_ * ab_) ** 1.5, rb) * np.gradient(rb); X = rb[:, None] * cth[None, :]; Y = rb[:, None] * np.sqrt(1 - cth[None, :] ** 2); Rb = rules(X, Y); WB = dMb[:, None] * wth[None, :] / 2
    dMc = np.diff(np.r_[0.0, Mc]); X = d + rr[:, None] * cth[None, :]; Y = rr[:, None] * np.sqrt(1 - cth[None, :] ** 2); Rc = rules(X, Y); WC = dMc[:, None] * wth[None, :] / 2
    gtyp = float(np.sum(WC * np.abs(Rc["MAX"])) / WC.sum())
    for k in ("Newton", "Law_all", "MAX"): out[k] = dict(Fb=float((WB * Rb[k]).sum()), Fc=float((WC * Rc[k]).sum()))
    out["gtyp"] = gtyp; out["Mc"] = float(WC.sum()); out["Mb"] = float(WB.sum()); out["norm"] = {k: (out[k]["Fb"] + out[k]["Fc"]) / (out["Mc"] * gtyp) for k in ("Newton", "Law_all", "MAX")}; out["a_sys"] = (out["MAX"]["Fb"] + out["MAX"]["Fc"]) / (out["Mc"] + out["Mb"]); return out
R3 = {}
for f in FEET:
    for d in (0.5, 2.0, 8.0):
        r = P3(d, A0F[f]); R3[f"{f}|{d}"] = r; say(f"  P3 {f} offset {d} kpc: (F_b + F_c)/(M_c g_typ): Newton {r['norm']['Newton']:+.2e}, law on both {r['norm']['Law_all']:+.2e}, MAX {r['norm']['MAX']:+.3e}; net acceleration of the system {r['a_sys']:+.2e} m/s^2, a0 units {r['a_sys'] / A0F[f]:+.3f}; F_c/M_c {r['MAX']['Fc'] / r['Mc']:+.2e}")
RES["P3"] = R3
# P3b, added: true QUMOND control and the projected MAX field, Helmholtz by FFT, because the algebraic law on both isn't QUMOND and doesn't conserve momentum
def P3b(delta, a0, Mb=6e10, ab=3.0, N=200, Lbox=500.0):
    h = M.Halo((1 + M.SHARE) * Mb); dx = Lbox / N; xs = (np.arange(N) - N // 2 + .5) * dx; X, Y, Z = np.meshgrid(xs.astype(np.float32), xs.astype(np.float32), xs.astype(np.float32), indexing="ij"); U = KPC; ab_ = ab
    q2 = X * X + Y * Y + Z * Z; fb = -G * Mb * MS / (U ** 2 * (q2 + ab_ * ab_) ** 1.5); rhob = (3 * Mb / (4 * math.pi * ab_ ** 3)) * (1 + q2 / ab_ ** 2) ** -2.5; del q2
    s_ = np.sqrt((X - delta) ** 2 + Y * Y + Z * Z); s_ = np.maximum(s_, .5 * dx); rt = np.geomspace(.2 * dx, h.R / KPC, 800); Mt = h.M0(rt * KPC); fc = -G * np.interp(np.log(s_), np.log(rt), Mt) * MS / (U ** 2 * s_ ** 3); rhoc = np.interp(np.log(s_), np.log(rt), np.gradient(Mt, rt) / (4 * math.pi * rt ** 2)); del s_
    Bv = [fb * X, fb * Y, fb * Z]; Cv = [fc * (X - delta), fc * Y, fc * Z]; del fb, fc, Y, Z
    gb = np.sqrt(Bv[0] ** 2 + Bv[1] ** 2 + Bv[2] ** 2); gs = [Bv[i] + Cv[i] for i in range(3)]; gsm = np.sqrt(gs[0] ** 2 + gs[1] ** 2 + gs[2] ** 2); L = law(gb, a0); z = gsm > L; mL = L / np.maximum(gb, 1e-300); LA = law(gsm, a0) / np.maximum(gsm, 1e-300); del gb
    k = 2 * math.pi * np.fft.fftfreq(N, dx); kz = 2 * math.pi * np.fft.rfftfreq(N, dx); KX, KY, KZ = np.meshgrid(k.astype(np.float32), k.astype(np.float32), kz.astype(np.float32), indexing="ij"); K2 = KX * KX + KY * KY + KZ * KZ; K2[0, 0, 0] = 1.0
    wc = rhoc * dx ** 3; wb = rhob * dx ** 3; o = {}
    for nm, fld_ in (("Newton", gs), ("QUMOND", [gs[i] * LA for i in range(3)]), ("MAX", [np.where(z, gs[i], Bv[i] * mL) for i in range(3)])):
        Fh = [np.fft.rfftn(fld_[i]) for i in range(3)]; D = KX * Fh[0] + KY * Fh[1] + KZ * Fh[2]; del Fh; gx = np.fft.irfftn(KX * D / K2, s=(N, N, N)); del D; fx_b = float((wb * gx).sum()); fx_c = float((wc * gx).sum()); gxa = float((wc * np.abs(gx)).sum() / wc.sum()); o[nm] = dict(Fb=fx_b, Fc=fx_c, norm=(fx_b + fx_c) / (float(wc.sum()) * gxa)); del gx
    o["Mb_grid"] = float(wb.sum()); o["Mc_grid"] = float(wc.sum()); return o
R3b = {}
for f in FEET:
    for d in (2.0, 8.0):
        r = P3b(d, A0F[f]); R3b[f"{f}|{d}"] = r; say(f"  P3b {f} offset {d} kpc, curl-free fields, 2.5 kpc grid: net force/(M_c g_typ): Newton {r['Newton']['norm']:+.2e}, QUMOND {r['QUMOND']['norm']:+.2e}, MAX projected {r['MAX']['norm']:+.3e}; F_b, F_c MAX {r['MAX']['Fb']:.2e} {r['MAX']['Fc']:.2e}; grid masses {r['Mb_grid']:.2e} {r['Mc_grid']:.2e}")
RES["P3b"] = R3b
# ---------- P4
def group_fields(Mt, D_kpc):
    h = M.Halo(Mt); r = D_kpc * KPC; gc = G * float(h.M0(r)) * MS / r ** 2; gb = gc / M.SHARE; return gb, gc, h
P4 = {}
for f in FEET:
    a = A0F[f]; h_g = M.Halo(6.35 * 6e10)
    for Mt in (1e13, 1e14):
        for D in (300, 500, 1000):
            g1, g2, h = group_fields(Mt, D); L = float(law(np.array(g1), a)); zone = "law" if L > g1 + g2 else "cold"; gbary = max(L, g1 + g2); gcold_par = a * g2 / (a - g2) if zone == "law" else g1 + g2; rel = gbary - gcold_par; dr = .5 * abs(rel) * (3 * GYR) ** 2 / KPC; P4[f"{f}|{Mt:.0e}|{D}"] = dict(zone=zone, g1=g1 / a, g2=g2 / a, gb=gbary / a, gc=gcold_par / a, rel=rel, drift_kpc=dr, over_R200=dr / (h_g.R / KPC)); say(f"  P4 {f} group {Mt:.0e}, {D} kpc ({D * KPC / h.R:.2f} R200): zone {zone}; g1 {g1 / a:.3f}, g2 {g2 / a:.3f} a0; baryons fall {gbary / a:.3f}, cold (parent) {gcold_par / a:.3f}; drift in 3 Gyr {dr:.0f} kpc = {dr / (h_g.R / KPC):.2f} R200 of an MW-like galaxy")
RES["P4"] = P4
# ---------- P5a switch radii
def baryon_model(Mb, r):
    if Mb < 1e13:
        ab = 3.0 * KPC * (Mb / 6e10) ** 0.4; return Mb * r * r / (r + ab) ** 2
    h = M.Halo(6.35 * Mb); return Mb * h.M0(r) / float(h.M0(h.R))
P5 = {}
say("  P5a: M_b, f, R200 kpc, crossings of C = L (kpc, in R200), share of cold mass inside R200 in cold zone; max ln(C/L)")
for f in FEET:
    a = A0F[f]
    for lg in (8, 9, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15):
        Mb = 10.0 ** lg
        for fq in (0.0, 0.872):
            Mv = 6.35 * Mb; h = M.Halo(Mv); r = np.geomspace(h.R * 1e-3, h.R * 3, 800); Mbr = baryon_model(Mb, r); gb = G * Mbr * MS / r ** 2; Mc = M.contracted(r, h, r, Mbr, Mb, fq); gc = G * Mc * MS / r ** 2; L = law(gb, a); C = gb + gc; lnCL = np.log(C / L); s = np.nonzero(np.diff(np.sign(lnCL)))[0]; ins = r <= h.R; dM = np.diff(np.r_[0, Mc]); P5[f"{f}|{lg}|{fq}"] = dict(R200=h.R / KPC, cross=(r[s] / KPC).tolist(), share=float(dM[ins & (lnCL > 0)].sum() / dM[ins].sum()), maxln=float(lnCL.max()))
            if fq == 0.872 or f == "canonical": say(f"    {f} {lg} f {fq}: R200 {h.R / KPC:.0f}; crossings " + (", ".join(f"{q / KPC:.1f}" for q in r[s]) or "none") + f"; active cold share {P5[f'{f}|{lg}|{fq}']['share']:.3f}; max ln(C/L) {lnCL.max():+.3f}")
RES["P5a"] = P5
# ---------- P5b friction, P5c, P5d
Mb = 6e10; a = A0F["canonical"]; h = M.Halo(6.35 * Mb); r = np.geomspace(.1, 500, 2000) * KPC; Mbr = baryon_model(Mb, r); gb = G * Mbr * MS / r ** 2; Mc0 = h.M0(r); gc0 = G * Mc0 * MS / r ** 2; gm = np.maximum(law(gb, a), gb + gc0); rho = np.gradient(Mc0, r) / (4 * math.pi * r * r) * MS
inv = np.trapz; sig2 = np.array([np.trapz((rho * gm)[i:], r[i:]) / max(rho[i], 1e-300) for i in range(len(r))]); BF = []
def fric(R, Mbody, v=None):
    Ra = R * KPC; v_ = math.sqrt(np.interp(Ra, r, gm) * Ra) if v is None else v; s_ = math.sqrt(np.interp(Ra, r, sig2)); X = v_ / (math.sqrt(2) * s_); rh = np.interp(Ra, r, rho); lnL = 3.0; A = 4 * math.pi * lnL * G * G * Mbody * MS * rh / v_ ** 2 * (erf(X) - 2 * X * math.exp(-X * X) / math.sqrt(math.pi)); tsink = v_ / (2 * A) / GYR
    zone = "law" if law(np.array(np.interp(Ra, r, gb)), a) > np.interp(Ra, r, gb + gc0) else "cold"; return dict(R=R, Mbody=Mbody, v=v_ / 1e3, sigma=s_ / 1e3, rho_c=rh / MS * PC ** 3, a_drag=A, tsink_Gyr=tsink, zone=zone)
for R, Mb_ in ((20, 3e9), (50, 3e9), (100, 3e9), (5, 1e10)):
    q = fric(R, Mb_); BF.append(q); say(f"  P5b body {Mb_:.0e} at {R} kpc: zone {q['zone']}; v {q['v']:.0f}, sigma {q['sigma']:.0f} km/s, rho_c {q['rho_c']:.2e} Msun/pc^3; drag if the wake pulled {q['a_drag']:.2e} m/s^2, sinking time {q['tsink_Gyr']:.1f} Gyr; under MAX in a law zone drag from cold 0")
RES["P5b"] = BF
ri = np.geomspace(.1, 400, 1500) * KPC; M0i = h.M0(ri); Fm = Mb / (M.FCOLD * h.M); gi = G * M0i * (1 + Fm) * MS / ri ** 2; Tj = ri ** 3 * gi  # j^2 = r^3 g, starting mixed
def gmax_at(x, Mc_):
    gb_ = G * baryon_model(Mb, x) * MS / x ** 2; return np.maximum(law(gb_, a), gb_ + G * Mc_ * MS / x ** 2)
A_, B_ = np.log(ri * 1e-3), np.log(ri * 1.5)
for _ in range(40):
    Cm_ = .5 * (A_ + B_); x = np.exp(Cm_); ok = x ** 3 * gmax_at(x, M0i) < Tj; A_ = np.where(ok, Cm_, A_); B_ = np.where(ok, B_, Cm_)
rf = np.maximum.accumulate(np.exp(.5 * (A_ + B_))); Rs = np.array([4, 8, 15, 30]) * KPC; Mlaw = np.interp(np.log(Rs), np.log(rf), M0i); Mnon = h.M0(Rs); Mbl = M.contracted(Rs, h, ri, baryon_model(Mb, ri), Mb, 1.0); RES["P5c"] = dict(R_kpc=[4, 8, 15, 30], M_native=Mnon.tolist(), M_blum=Mbl.tolist(), M_maxfield=Mlaw.tolist(), f_eff=((Mlaw - Mnon) / (Mbl - Mnon)).tolist()); say("  P5c cold under g_max, j^2 = r^3 g, MW-like, at 4, 8, 15, 30 kpc: M native " + " ".join(f"{q:.2e}" for q in Mnon) + "; Blumenthal " + " ".join(f"{q:.2e}" for q in Mbl) + "; in max field " + " ".join(f"{q:.2e}" for q in Mlaw) + "; f_eff " + " ".join(f"{q:.2f}" for q in RES["P5c"]["f_eff"]))
Rsun = 8.2 * KPC; rl = float(np.interp(Rsun, r, rho)) / MS * PC ** 3; rl2 = rl; RES["P5d"] = dict(rho_c_local=rl); say(f"  P5d local cold density at 8.2 kpc, native, f 0: {rl:.4f} Msun/pc^3; gravitating weight under MAX: 0 where the law wins")
# ---------- P5e growth
H0 = 100e3 * M.HUB / MPC; OMX, OB = .1197 / M.HUB ** 2, .0224 / M.HUB ** 2; OM = OMX + OB; fb = OB / OM; c = 299792458.0; PHI = 3e-5
def hub(a_): return H0 * math.sqrt(OM / a_ ** 3 + 1 - OM)
def rho_m(a_): return OM * 3 * H0 ** 2 / (8 * math.pi * G) / a_ ** 3
def growth(k_Mpc, foot, rule, phi=PHI, ext=None):
    a0 = A0F[foot]; k = k_Mpc / MPC; Rco = 1.0 / k; ai = 1 / 1101.0; di = 2 * k * k * c * c * phi / (3 * OM * H0 * H0) * ai; die = None if ext is None else 2 * (ext / MPC) ** 2 * c * c * phi / (3 * OM * H0 * H0) * ai; d = di; dp = di; Ns = np.linspace(math.log(ai), 0.0, 6001); dN = Ns[1] - Ns[0]; zc = None; znl = None
    def acc(N, d_, dp_):
        a_ = math.exp(N); H = hub(a_); dlnH = -1.5 * (OM / a_ ** 3) / (OM / a_ ** 3 + 1 - OM); gN = 4 * math.pi * G * rho_m(a_) * abs(d_) * a_ * Rco / 3; g1 = fb * gN; g2 = (1 - fb) * gN; L = float(law(np.array(g1), a0)); C = g1 + g2; ge = {"newton": C, "law": L, "max": max(L, C)}[rule]; ratio = ge / max(gN, 1e-300)
        if ext is not None:
            ge_ = 4 * math.pi * G * rho_m(a_) * (die * a_ / ai) * a_ * (MPC / ext) / 3; g1e = fb * ge_; Le = float(law(np.array(g1e), a0)); Lz_ = Le > ge_; Lp = .5 + (.5 * g1e + a0) / (2 * math.sqrt(.25 * g1e * g1e + a0 * g1e)); ratio = 1.0 if rule == "newton" else (fb * Lp if (rule == "law" or Lz_) else 1.0); L, C = (Le, ge_)
        return -(2 + dlnH) * dp_ + 1.5 * (OM / a_ ** 3) / (OM / a_ ** 3 + 1 - OM) * d_ * ratio, L > C
    for i, N in enumerate(Ns[:-1]):
        k1, z1 = acc(N, d, dp); k2, _ = acc(N + dN / 2, d + dN / 2 * dp, dp + dN / 2 * k1); k3, _ = acc(N + dN / 2, d + dN / 2 * (dp + dN / 2 * k1), dp + dN / 2 * k2); k4, _ = acc(N + dN, d + dN * (dp + dN / 2 * k2), dp + dN * k3); d2 = d + dN * dp + dN * dN / 6 * (k1 + k2 + k3); dp = dp + dN / 6 * (k1 + 2 * k2 + 2 * k3 + k4); d = d2
        if z1 and zc is None: zc = 1 / math.exp(N) - 1
        if d >= 1 and znl is None: znl = 1 / math.exp(N + dN) - 1; break
    return dict(delta=d, z_law_zone=zc, z_nl=znl, a_end=math.exp(N + dN), di=di)
GR_ = {}
say("  P5e k/Mpc: foot: rule: z at which the law wins on the mode, z of delta 1, delta at end; amplification at the a where the first of the three ends")
for f in FEET:
    for kk in (.01, .03, .1, .3, 1, 3, 10):
        r_ = {q: growth(kk, f, q) for q in ("newton", "law", "max")}; aend = min(v["a_end"] for v in r_.values())
        def at(q):
            # rerun capped at aend by interpolation in delta isn't kept; report z's and ends
            return r_[q]
        GR_[f"{f}|{kk}"] = r_; say(f"    {f} k {kk}: max: law zone from z {r_['max']['z_law_zone']}, z_nl {r_['max']['z_nl']}, delta {r_['max']['delta']:.3g} | newton: z_nl {r_['newton']['z_nl']}, delta {r_['newton']['delta']:.3g} | law alone: z_nl {r_['law']['z_nl']}, delta {r_['law']['delta']:.3g} | max/newton at z 0 {r_['max']['delta'] / r_['newton']['delta']:.2f} (only if neither stopped)")
RES["P5e"] = GR_
GX = {}
for f in FEET:
    for kk, ph, ex in ((.01, PHI, None), (.03, .1 * PHI, None), (.1, .1 * PHI, None), (.1, .01 * PHI, None), (.3, .01 * PHI, None), (.01, PHI, .03), (.01, PHI, .1), (.03, .1 * PHI, .1)):
        r_ = {q: growth(kk, f, q, ph, ex) for q in ("newton", "max")}; GX[f"{f}|{kk}|{ph}|{ex}"] = r_; say(f"    added, amplitude and external-field rows, {f} k {kk} Phi {ph:.0e} external mode k {ex}: law zone from z {r_['max']['z_law_zone']}, max delta {r_['max']['delta']:.3g} z_nl {r_['max']['z_nl']}; newton delta {r_['newton']['delta']:.3g} z_nl {r_['newton']['z_nl']}; ratio {r_['max']['delta'] / r_['newton']['delta']:.2f}")
RES["P5e_added"] = GX
# ---------- P6 spherical jump at switch, X-COP and a group
P6 = {}
for f in FEET:
    a = A0F[f]; R = M.rule("P")
    for lb, Mb_ in (("1e12.5", 10 ** 12.5), ("1e13", 1e13), ("1e14", 1e14)):
        h = M.Halo(6.35 * Mb_); r_ = np.geomspace(h.R * 1e-2, h.R * 3, 4000); Mbr = baryon_model(Mb_, r_); gb = G * Mbr * MS / r_ ** 2; Mc = M.contracted(r_, h, r_, Mbr, Mb_, .872); gc = G * Mc * MS / r_ ** 2; L = law(gb, a); C = gb + gc; lnCL = np.log(C / L); s = np.nonzero(np.diff(np.sign(lnCL)))[0]; ge = np.maximum(L, C); rh = np.gradient(r_ * r_ * ge, r_) / (4 * math.pi * G * r_ * r_) / MS * PC ** 3; ou = []
        for i in s: ou.append(dict(r_kpc=r_[i] / KPC, in_R200=r_[i] / h.R, rho_inside=float(rh[max(i - 3, 0)]), rho_outside=float(rh[min(i + 4, len(rh) - 1)])))
        P6[f"{f}|{lb}"] = ou; say(f"  P6 {f} M_b {lb}: " + "; ".join(f"switch at {o['r_kpc']:.0f} kpc ({o['in_R200']:.2f} R200): rho_eff {o['rho_inside']:.2e} to {o['rho_outside']:.2e} Msun/pc^3" for o in ou) + ("" if ou else "no switch"))
RES["P6"] = P6
# ---------- SPARC
INP = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc"); T = {}
for l in open(os.path.join(INP, "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) == 19:
        try: T[t[0]] = dict(Inc=float(t[5]), L=float(t[7]), MHI=float(t[13]), Vf=float(t[15]), Q=float(t[17]))
        except ValueError: pass
GAL = []
for fn in sorted(glob.glob(os.path.join(INP, "rotmod", "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", ""); A = np.loadtxt(fn, comments="#", ndmin=2); q = T[nm]
    if q["Q"] > 2 or q["Inc"] < 30 or len(A) < 5: continue
    GAL.append(dict(name=nm, R=A[:, 0] * KPC, V=A[:, 1], eV=A[:, 2], Vg=A[:, 3], Vd=A[:, 4], Vb=A[:, 5], **q))
def gbar(g_, U=.5): return (np.abs(g_["Vg"]) * g_["Vg"] + U * np.abs(g_["Vd"]) * g_["Vd"] + 1.4 * U * np.abs(g_["Vb"]) * g_["Vb"]) * 1e6 / g_["R"]
def Mtot(g_, U=.5): return (U * g_["L"] + 1.33 * g_["MHI"]) * 1e9
P7 = {}
for f in FEET:
    for cell, U in (("P", .5), ("F0", .5), ("P", .35), ("F0", .35)):
        a = A0F[f]; R = M.rule(cell); allL = []; allres = []; slopes = []; ngal = 0; gsw = 0
        for g_ in GAL:
            gb = np.maximum(gbar(g_, U), 1e-14); gc = R.one(g_["R"], gb, lg=math.log10(Mtot(g_, U))); L = law(gb, a); C = gb + gc; ln = np.log(C / L); res = np.log10(np.maximum(g_["V"], 1) ** 2 * 1e6 / g_["R"]) - np.log10(L); allL.append(ln); allres.append(res); ngal += 1; o = np.argsort(g_["R"]); lo_ = ln[o]; s_ = np.nonzero(np.diff(np.sign(lo_)))[0]
            if len(s_):
                gsw += 1; Ro = g_["R"][o]; dlr = np.diff(np.log(Ro)); vL = np.sqrt(np.maximum(L[o] * Ro, 1)); vC = np.sqrt(np.maximum(C[o] * Ro, 1))
                for i in s_: slopes.append(float((np.log(vC[i + 1]) - np.log(vC[i])) / dlr[i] - (np.log(vL[i + 1]) - np.log(vL[i])) / dlr[i]))
        X = np.concatenate(allL); Yr = np.concatenate(allres); key = f"{f}|{cell}|{U}"; P7[key] = dict(n_points=int(len(X)), frac_within_0p1=float(np.mean(np.abs(X) < .1)), frac_cold=float(np.mean(X > 0)), gal_with_switch=gsw, n_gal=ngal, slope_jump_median=float(np.median(slopes)) if slopes else None, n_slopes=len(slopes), slope_jump_16_84=[float(np.percentile(slopes, 16)), float(np.percentile(slopes, 84))] if slopes else None)
        edges = (-3, -1.5, -1, -.6, -.3, -.1, .1, .3, .6, 1.5); tb = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            m_ = (X >= lo) & (X < hi)
            if m_.sum() >= 3: tb.append((lo, hi, int(m_.sum()), float(np.median(Yr[m_])), float(1.25 * np.std(Yr[m_]) / math.sqrt(m_.sum())), float(np.median(np.maximum(X[m_], 0)) / math.log(10))))
        P7[key]["bins"] = tb; cb = (X > .1); P7[key]["cold_excess"] = dict(n=int(cb.sum()), resid=float(np.median(Yr[cb])) if cb.any() else None, se=float(1.25 * np.std(Yr[cb]) / math.sqrt(max(cb.sum(), 1))) if cb.any() else None, added=float(np.median(X[cb]) / math.log(10)) if cb.any() else None)
        say(f"  P7 {key}: {ngal} galaxies, {len(X)} points; |ln C/L| < 0.1 {P7[key]['frac_within_0p1']:.3f}; cold branch {P7[key]['frac_cold']:.3f}; with a switch in the data {gsw}; slope jump median {P7[key]['slope_jump_median']}, n {len(slopes)}, 16-84 {P7[key]['slope_jump_16_84']}; points with ln(C/L) > 0.1: {P7[key]['cold_excess']}")
        for b_ in tb: say(f"     ln(C/L) {b_[0]:+.1f} to {b_[1]:+.1f}: n {b_[2]}, residual vs law {b_[3]:+.3f} +- {b_[4]:.3f} dex; MAX adds {b_[5]:+.3f}")
RES["P7"] = P7
# ---------- P8 orbit average, row 11
SJ = json.load(open(os.path.join(RB, "DW2_disc_wall", "dw2_proc_results.json"))); BN = [(60, 100), (100, 150), (150, 200), (200, 250)]; idx = [1, 2, 3, 4]; a = A0F["canonical"]
def stars(g_):
    return np.maximum.accumulate(np.maximum((np.abs(g_["Vd"]) * g_["Vd"] * .5 + np.abs(g_["Vb"]) * g_["Vb"] * .7) * 1e6 * g_["R"] / G / MS, 0))
QV = np.array([.1, .3, .5, .7, .9]); from scipy.special import erfinv
def maxwell_q(u):
    from scipy.special import gammaincinv
    return np.sqrt(2 * gammaincinv(1.5, u))
VQ = maxwell_q(QV); MU = np.array([.1, .3, .5, .7, .9])
def setup(g_, mass):
    Mbt = Mtot(g_); Mv = 6.35 * Mbt if mass == "share" else 10 ** (11.18 + .9 * (math.log10(Mbt) - 10)); h = M.Halo(Mv); Rl = float(g_["R"].max()); rg = np.geomspace(float(g_["R"][0]) * .1, h.R * 3, 700); Rs_ = g_["R"]; mb = np.maximum.accumulate(np.maximum(gbar(g_) * Rs_ ** 2 / G / MS, 0)); mbg = np.where(rg < Rs_[0], mb[0] * (rg / Rs_[0]) ** 2, np.interp(np.log(rg), np.log(Rs_), mb)); gb = G * mbg * MS / rg ** 2; Mc = h.M0(rg); ge = np.maximum(law(gb, a), gb + G * Mc * MS / rg ** 2); dl = np.gradient(np.log(rg)); Phi = np.cumsum((ge * rg * dl)[::-1])[::-1] * -1.0; rhoc = np.maximum(np.gradient(Mc, rg) / (4 * math.pi * rg ** 2), 1e-300); inte = np.cumsum((rhoc * ge * rg * dl)[::-1])[::-1]; sg2 = inte / rhoc; Ms = np.where(rg < Rs_[0], stars(g_)[0] * (rg / Rs_[0]) ** 2, np.interp(np.log(rg), np.log(Rs_), stars(g_))); rhos = np.gradient(Ms, rg) * PC / (4 * math.pi * (rg / PC) ** 2); rmean = Ms / (4 / 3 * math.pi * (rg / PC) ** 3); return dict(rg=rg, Phi=Phi, sg2=sg2, Mc=Mc, rhos=np.maximum(rhos, 0), rmean=rmean, Rl=Rl, dl=dl)
def expo(S):
    rg = S["rg"]; ins = rg <= S["Rl"]; ii = np.nonzero(ins)[0][::12]; dm = np.gradient(S["Mc"])[ii]; orb = np.zeros(len(ii))
    for n_, i in enumerate(ii):
        r0 = rg[i]; s = math.sqrt(max(S["sg2"][i], 1e-6)); tot = 0.0
        for vq in VQ:
            v = vq * s
            for mu in MU:
                L2 = (r0 * v * math.sqrt(1 - mu * mu)) ** 2; vr2 = v * v + 2 * (S["Phi"][i] - S["Phi"]) + L2 / r0 ** 2 - L2 / rg ** 2; ok = vr2 > 0; 
                lo = i
                while lo > 0 and ok[lo - 1]: lo -= 1
                hi = i
                while hi < len(rg) - 1 and ok[hi + 1]: hi += 1
                w = rg[lo:hi + 1] * S["dl"][lo:hi + 1] / np.sqrt(np.maximum(vr2[lo:hi + 1], 1e-3 * v * v + 1)); tot += float((w * S["rhos"][lo:hi + 1]).sum() / w.sum())
        orb[n_] = tot / (len(VQ) * len(MU))
    return dm, S["rmean"][ii], S["rhos"][ii], orb
T13 = 13.8e9; P8 = {}
for mass in ("share", "em1"):
    SG = SJ[f"star_{mass}"]["sigma"]; byb = []
    for lo, hi in BN:
        G_ = [q for q in GAL if lo <= q["Vf"] < hi]; byb.append([expo(setup(q, mass)) for q in G_])
    def ret(sg, col):
        return [float(np.median([np.sum(e[0] * np.exp(-sg * e[col] * T13)) / e[0].sum() for e in b])) for b in byb]
    mean_, shell_, orb_ = ret(SG, 1), ret(SG, 2), ret(SG, 3); need = [SJ[f"star_{mass}"]["need"][i] for i in idx]; ratio_mean = [o / q for o, q in zip(orb_, mean_)]; ratio_shell = [o / q for o, q in zip(orb_, shell_)]
    tgt = min(need[2], need[3]) if False else None
    # refit by DW2's rule: median over 150-250 on the tighter floor
    flo = need[2:4]; 
    def fit(col):
        fun = lambda ls: float(np.median([np.sum(e[0] * np.exp(-10 ** ls * e[col] * T13)) / e[0].sum() for b in byb[2:4] for e in b])) - min(flo)
        return (10 ** brentq(fun, -14, -2), None) if fun(-14) * fun(-2) < 0 else (float("nan"), fun(-2) + min(flo))
    sgo, sat = fit(3); orbf = ret(sgo, 3) if sat is None else [float("nan")] * 4; P8[mass] = dict(sigma_dw2=SG, mean=mean_, shell=shell_, orbit=orb_, need=need, r_mean=ratio_mean, r_shell=ratio_shell, sigma_refit=sgo, orbit_refit=orbf, sigma_ratio=sgo / SG, saturated_retained=sat)
    lb = "MEAN-LIKE" if all(abs(q - 1) <= .1 for q in ratio_mean) else ("SHELL-LIKE" if all(abs(q - 1) <= .1 for q in ratio_shell) else "NEITHER"); P8[mass]["label"] = lb
    say(f"  P8 {mass}: bins 60-100, 100-150, 150-200, 200-250; sigma DW2 {SG:.2e}: mean-inside " + " ".join(f"{q:.3f}" for q in mean_) + " | shell " + " ".join(f"{q:.3f}" for q in shell_) + " | orbit " + " ".join(f"{q:.3f}" for q in orb_) + " | room " + " ".join(f"{q:.3f}" for q in need) + f" | label {lb}; refit sigma {sgo:.2e} (x{sgo / SG:.2f}), saturated retained {sat}: orbit " + " ".join(f"{q:.3f}" for q in orbf))
RES["P8"] = P8
# ---------- A18 lane row
S = os.path.join(REPO, "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); nsd = {"__file__": os.path.abspath(S), "__name__": "h"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S).read().split('P("=" * 100)')[0], "h", "exec"), nsd)
gal_, terms, KV, sexp, gbarD, GK = nsd["gal"], nsd["galaxy_terms"], nsd["K_VERT"], nsd["sexp"], nsd["gbar"], nsd["G"]; TL = json.load(open(os.path.join(RB, "RQ3_acceptance_v2", "tolerances.json")))["DM"]; KU = 3.0857e13
def a18(foot, cell_X, f_c, form):
    a0 = A0F[foot]; rule = M.Rule(f=f_c, X=cell_X)
    def one(g_, r_):
        nsd["gal_BD"] = g_["BD"]; t = terms(g_, r_); go = t["vrot"] ** 2 / r_; gas = gbarD(t, r_, 0.0); rgrid = np.geomspace(.1, 60, 120) * KPC
        def mbarr(Y):
            ks = rgrid / KPC; return np.array([gbarD(terms(g_, q), q, Y) * q * q / GK for q in ks[::1]])
        def cg(x, Y):
            Mt = Y * t["Ld"] * (1 + g_["BD"]) + t["Ma"] + t["Mm"]; gc = rule.gc_sorted(rgrid, np.maximum(mbarr(Y), 1e-3) * G * MS / rgrid ** 2, lg=math.log10(Mt)); gcr = float(np.interp(r_ * KPC, rgrid, gc)); v = x / KU; return float(max(law(np.array(v), a0), v + gcr)) * KU
        try: Y = brentq(lambda Y: cg(gbarD(t, r_, Y), Y) - go, .02, 5.0, xtol=1e-3)
        except ValueError: return None
        gb = gbarD(t, r_, Y); Sig = Y * t["I0"] * math.exp(-r_ / t["hR"]) + sexp(r_, t["Ma"], 2 * t["hR"]) + sexp(r_, t["Mm"], t["hR"]); KN = 2 * math.pi * GK * Sig * (1 - math.exp(-1)); h_ = math.hypot(gb, KN); Bf = cg(h_, Y) / h_ if form == "A" else 1 + (cg(gb, Y) - gb) * t["hz"] / r_ / KN; return math.sqrt(math.pi * GK * KV * t["hz"] * Sig * Bf) / t["smeas"], Y
    x = [one(g_, 1.5 * g_["hR"]) for g_ in gal_.values()]; x = [q for q in x if q is not None]; rr = np.array([q[0] for q in x]); Ys = np.array([q[1] for q in x]); bs = np.median(np.random.default_rng(576).choice(rr, size=(2000, len(rr))), axis=1); w = float(np.percentile(bs, 84) - np.percentile(bs, 16)) / 2; r0 = float(np.median(rr)); tg = (TL["c_lo"] + TL["c_hi"]) / 2; s = math.sqrt(((TL["c_hi"] - TL["c_lo"]) / 4) ** 2 + TL["line_sigma"] ** 2 + w ** 2); return dict(r=r0, Z=(r0 - tg) / s, n=len(rr), Y=float(np.median(Ys)))
AL = {}
for f in FEET:
    for lab, X_, fc in (("law cold x 0", 0.0, .872), ("P f 0.872", 1.0, .872), ("F0", 1.0, 0.0)):
        for form in ("R", "A"):
            AL[f"{f}|{lab}|{form}"] = a18(f, X_, fc, form); q = AL[f"{f}|{lab}|{form}"]; say(f"  A18 {f} {lab} form {form}: r {q['r']:.3f}, Z {q['Z']:+.2f}, n {q['n']}, median Y {q['Y']:.2f}")
RES["A18"] = AL
Lk = json.load(open(os.path.join(RB, "RQ3_acceptance_v2", "results", "law.json")))["footings"]
ok18 = all(abs(AL[f"{f}|law cold x 0|R"]["r"] - Lk[f]["rows"]["A18"]["forms"]["R"]["value"]) <= 1e-3 for f in FEET)
check("K-A18", ok18, f"cold x 0 vs law's A18 form R: " + " ".join(f"{AL[f'{f}|law cold x 0|R']['r']:.4f} vs {Lk[f]['rows']['A18']['forms']['R']['value']:.4f}" for f in FEET))
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; check("RSS", rss < 4, f"{rss:.2f} GB"); RES["checks"] = CH
json.dump(RES, open(os.path.join(HERE, f"mx1_phys_results{TAG}.json"), "w"), indent=1, sort_keys=True, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
if not all(CH.values()): say("CHECK FAILED", [k for k, v in CH.items() if not v]); OUT.close(); sys.exit(1)
OUT.close()
