#!/usr/bin/env python3
"""UX6: UX3's gas term on the Bullet's map. Criteria FROZEN_CRITERIA.md, committed alone first. Set UX6_MUTATE=1 for the twin.
A description: no action, no field equation. kappa = 1/2 FITTED; not theory closed. Reinstates nothing."""
import os, sys, json, math, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = os.environ.get("UX6_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CHECKS = {}
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
KFIT = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json"))); PI2 = math.pi**2
SIG_CRIT = 1.827e9; Z_BOX = 18000.0; SIG_DELTA = math.sqrt((1/8)**2 + 0.15**2); SIG_O3 = 0.15
GAS = [(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0), (1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)]
GAL = [(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)]
BCG1 = np.array([0.0, 0.0]); BCG3 = np.array([820.0, 220.0]); GASM = np.array([190.0, 90.0]); GASB = np.array([670.0, 170.0])
OBS300 = {"BCG1": 3.5e14, "BCG3": 2.3e14}; PAIRS = {"main": (BCG1, GASM), "sub": (BCG3, GASB)}
SIG_B = 1500.0; V_BULK = 2700.0; TH_SUB = SIG_B**2/(SIG_B**2 + V_BULK**2); WEIGHTS = [1.0, TH_SUB, TH_SUB, TH_SUB]
LS = {"N3a": 300.0, "N3b": 1000.0}

def law(g, a): return 0.5*g + np.sqrt(0.25*g*g + a*g)
def nut_v3(y): return 0.5*(np.sqrt(1.0 + 4.0/np.maximum(y, 1e-300)) - 1.0)
def fld(X, Y, Z, c):
    M, a, xc, yc = c; dx = X - xc; dy = Y - yc; dz = Z
    f = -G*M*MSUN/((dx*dx + dy*dy + dz*dz + a*a)**1.5*KPC**3)*KPC
    return f*dx, f*dy, f*dz
def enc_table(comps, centre, restore=False):
    """M(<r) about centre, spherical shells; restore puts every component on centre"""
    r = np.geomspace(0.5, 3e5, 3000); nod, wt = np.polynomial.legendre.leggauss(96); tot = np.zeros_like(r)
    for M, a, x, y in comps:
        d = 0.0 if restore else float(np.hypot(x - centre[0], y - centre[1]))
        s2 = r[:, None]**2 + d*d - 2*r[:, None]*d*nod[None, :]
        rho = 3*M/(4*math.pi*a**3)*(1 + s2/a**2)**-2.5
        sh = 4*math.pi*r*r*(0.5*(rho*wt[None, :]).sum(1))
        lg = np.log(r); tot += np.r_[0.0, np.cumsum(0.5*(sh[1:]*r[1:] + sh[:-1]*r[:-1])*np.diff(lg))] + M*(r[0]/a)**3/(1 + (r[0]/a)**2)**1.5*(d == 0)
    return r, np.maximum(tot, 0.0)
class System:
    def __init__(s, gas, gal, groups):
        s.gas, s.gal = gas, gal; s.tab = {}
        for key, restore in (("N1", False), ("N2", True)):
            s.tab[key] = []
            for ctr, ig, ii in groups:
                r, mg = enc_table([gas[i] for i in ig], ctr, restore); _, ms = enc_table([gal[i] for i in ii], ctr, False)
                f = G*MSUN/(r*KPC)**2; s.tab[key].append((np.asarray(ctr, float), np.log(r), f*mg, f*(mg + ms)))
    def ctx(s, X, Y, Z):
        C = dict(X=X, Y=Y, Z=Z, gas=[fld(X, Y, Z, c) for c in s.gas]); st = [fld(X, Y, Z, c) for c in s.gal]
        C["st"] = tuple(sum(v[i] for v in st) for i in range(3))
        return C
    def soft(s, C, key):
        L = LS[key]; K = "soft" + key
        if K not in C:
            v = [fld(C["X"], C["Y"], C["Z"], (M, math.sqrt(a*a + L*L), x, y)) for M, a, x, y in s.gas]; C[K] = tuple(sum(q[i] for q in v) for i in range(3))
        return C[K]
    def extra(s, sp, C, reg=True):
        """g_total - g_b. sp: form, k, a0, scale"""
        a0, k, sc, form = sp["a0"], sp["k"], sp.get("scale", 1.0), sp["form"]
        gv = tuple(sc*sum(c[i] for c in C["gas"]) for i in range(3))
        gb = [gv[i] + C["st"][i] for i in range(3)]
        if reg: gb[1] = gb[1] + a0/1000.0
        g = np.sqrt(gb[0]**2 + gb[1]**2 + gb[2]**2); L = law(g, a0); m = L/np.maximum(g, 1e-300)
        if form in ("L1", "L1c", "S", "N3a", "N3b"):
            if form == "L1": t = gv
            elif form == "L1c": t = tuple(sc*sum(w*c[i] for w, c in zip(WEIGHTS, C["gas"])) for i in range(3))
            elif form == "S": t = C["st"]
            else:
                q = s.soft(C, form); t = tuple(sc*q[i] for i in range(3))
            h = k*np.sqrt(t[0]**2 + t[1]**2 + t[2]**2)/a0
            return tuple(gb[i]*(m*(1 + h) - 1) for i in range(3))
        out = [gb[i]*(m - 1) for i in range(3)]
        if form == "LAW": return tuple(out)
        if form == "L2":
            sg = -1.0 if MUT else 1.0
            return tuple(out[i] + sg*k*(L/a0)*gv[i] for i in range(3))
        for ctr, lr, tg, tb in s.tab[form]:
            dx = C["X"] - ctr[0]; dy = C["Y"] - ctr[1]; dz = C["Z"]; r = np.maximum(np.sqrt(dx*dx + dy*dy + dz*dz), 0.5)
            q = np.log(r); gg = np.interp(q, lr, tg); gt = np.interp(q, lr, tb)
            f = -law(gt, a0)*k*gg/a0/r
            out[0] = out[0] + f*dx; out[1] = out[1] + f*dy; out[2] = out[2] + f*dz
        return tuple(out)
GROUPS = [(BCG1, [0], [0]), (BCG3, [1, 2, 3], [1])]
SYS = System(GAS, GAL, GROUPS)

def zgrid(Z, n_in=500, n_out=500, z_in=1500.0):
    return np.concatenate([np.linspace(0.0, z_in, n_in + 1), np.geomspace(z_in, Z, n_out + 1)[1:]])
ZS = zgrid(Z_BOX); ZM = zgrid(6000.0, n_in=140, n_out=110, z_in=1200.0)
def sig_pl(D, M, a): return M*a*a/(math.pi*(D*D + a*a)**2)
def M2D(x0, y0, R, plum, nrho=400, nphi=720):
    rho = np.linspace(0.0, R, nrho + 1); phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi
    X = x0 + rho[:, None]*np.cos(phi)[None, :]; Y = y0 + rho[:, None]*np.sin(phi)[None, :]; S = np.zeros_like(X)
    for M, a, xc, yc in plum: S += sig_pl(np.sqrt((X - xc)**2 + (Y - yc)**2), M, a)
    return float(np.trapz(np.sum(S, axis=1)*(2*math.pi/nphi)*rho, rho))
def plum_of(sp):
    sc = sp.get("scale", 1.0)
    return [(sc*M, a, x, y) for M, a, x, y in GAS] + GAL
def surface(specs, x0, y0, R, nphi=360, nrho=200):
    """extra mass in cylinder for every spec, same grid as X32"""
    phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi; CP, SP = np.cos(phi), np.sin(phi)
    X = (x0 + R*CP)[:, None]*np.ones((1, len(ZS))); Y = (y0 + R*SP)[:, None]*np.ones((1, len(ZS))); Zg = np.broadcast_to(ZS[None, :], X.shape)
    C = SYS.ctx(X, Y, Zg); side = {}
    for n, sp in specs.items():
        e = SYS.extra(sp, C); side[n] = 2.0*np.trapz(np.sum(e[0]*CP[:, None] + e[1]*SP[:, None], axis=0)*(2*math.pi/nphi)*R, ZS)
    rho = np.linspace(0.0, R, nrho + 1); Xc = x0 + rho[:, None]*CP[None, :]; Yc = y0 + rho[:, None]*SP[None, :]
    C = SYS.ctx(Xc, Yc, np.full_like(Xc, Z_BOX)); out = {}
    for n, sp in specs.items():
        e = SYS.extra(sp, C); caps = 2.0*np.trapz(np.sum(e[2], axis=1)*(2*math.pi/nphi)*rho, rho)
        out[n] = -(side[n] + caps)*KPC**2/(4*math.pi*G)/MSUN
    return out
XS = np.arange(-500.0, 1400.0 + 1e-9, 10.0); YS = np.arange(-400.0, 700.0 + 1e-9, 10.0); XX, YY = np.meshgrid(XS, YS, indexing="ij")
def maps(specs, h=2.0):
    S = {n: np.zeros_like(XX) for n in specs}
    for j0 in range(0, len(YS), 6):
        ys = YS[j0:j0 + 6]; X, Y, Z = np.meshgrid(XS, ys, ZM, indexing="ij"); div = {n: 0.0 for n in specs}
        for ax, (dx, dy, dz) in enumerate(((h, 0, 0), (0, h, 0), (0, 0, h))):
            for sgn in (1.0, -1.0):
                C = SYS.ctx(X + sgn*dx, Y + sgn*dy, Z + sgn*dz)
                for n, sp in specs.items(): div[n] = div[n] + sgn*SYS.extra(sp, C)[ax]
        for n in specs:
            S[n][:, j0:j0 + 6] = 2.0*np.trapz(-div[n]/(2*h)/(4*math.pi*G)*KPC**2/MSUN, ZM, axis=2)
    for n, sp in specs.items():
        for M, a, xc, yc in plum_of(sp): S[n] += sig_pl(np.hypot(XX - xc, YY - yc), M, a)
    return S
def localmax(S, top=4):
    c = S[1:-1, 1:-1]; ok = np.ones_like(c, bool)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di or dj: ok &= c > S[1 + di:S.shape[0] - 1 + di, 1 + dj:S.shape[1] - 1 + dj]
    ii, jj = np.nonzero(ok); o = np.argsort(-c[ii, jj])[:top]
    return [[float(XS[ii[q] + 1]), float(YS[jj[q] + 1]), float(c[ii[q], jj[q]]/SIG_CRIT)] for q in o]
def peak(S, A, B):
    mid = 0.5*(A + B); w = np.hypot(XX - mid[0], YY - mid[1]) <= 350.0
    i = int(np.argmax(np.where(w, S, -np.inf))); a, b = np.unravel_index(i, S.shape)
    edge = not (0 < a < S.shape[0] - 1 and 0 < b < S.shape[1] - 1) or not w[a - 1:a + 2, b - 1:b + 2].all()
    lm = (not edge) and S[a, b] >= S[a - 1:a + 2, b - 1:b + 2].max() and (S[a - 1:a + 2, b - 1:b + 2] == S[a, b]).sum() == 1
    return np.array([XX[a, b], YY[a, b]]), bool(lm)
def observe(S, m):
    o = {}
    for k, (bc, gc) in PAIRS.items():
        pk, lm = peak(S, bc, gc); dg = float(np.hypot(*(pk - gc))); db = float(np.hypot(*(pk - bc))); sep = float(np.hypot(*(bc - gc)))
        o[k] = dict(peak=pk.tolist(), local_max=lm, d_gas=dg, d_bcg=db, delta=dg/sep, Z=(dg/sep - 1)/SIG_DELTA, guard=bool(lm and db < dg),
                    dkappa=(m[f"bcg_{k}"] - m[f"gas_{k}"])/(math.pi*1e4)/SIG_CRIT, kbar_bcg=m[f"bcg_{k}"]/(math.pi*1e4)/SIG_CRIT, kbar_gas=m[f"gas_{k}"]/(math.pi*1e4)/SIG_CRIT)
    o["M300"] = [m["BCG1"], m["BCG3"]]; o["ZO3"] = [(m["BCG1"]/OBS300["BCG1"] - 1)/SIG_O3, (m["BCG3"]/OBS300["BCG3"] - 1)/SIG_O3]; o["ratio"] = m["BCG3"]/m["BCG1"]; o["M250"] = [m["P1"], m["P3"]]
    o["top"] = localmax(S); o["kappa_max"] = float(S.max()/SIG_CRIT)
    pos = [not (o[k]["guard"] and abs(o[k]["Z"]) <= 3 and o[k]["dkappa"] > 0) for k in PAIRS]; o["pos_or_sign_fail"] = bool(any(pos))
    mass = any(abs(z) > 3 for z in o["ZO3"]); o["mass_fail"] = bool(mass)
    o["cls"] = "FAIL" if (o["pos_or_sign_fail"] or mass) else ("PASS" if all(abs(o[k]["Z"]) <= 2 for k in PAIRS) and all(abs(z) <= 2 for z in o["ZO3"]) else "TENSION")
    return o
APS = dict(BCG1=(BCG1, 300.0), BCG3=(BCG3, 300.0), P1=(BCG1, 250.0), P3=(BCG3, 250.0), bcg_main=(BCG1, 100.0), gas_main=(GASM, 100.0), bcg_sub=(BCG3, 100.0), gas_sub=(GASB, 100.0))
def run(specs):
    sf = {a: surface(specs, *c, R) for a, (c, R) in APS.items()}; S = maps(specs); res = {}
    for n, sp in specs.items():
        pl = plum_of(sp); m = {a: M2D(*c, R, pl) + sf[a][n] for a, (c, R) in APS.items()}
        res[n] = (S[n], m)
    return res

say("=" * 90); say("UX6_gas_term_bullet" + ("  [MUTATE]" if MUT else "")); say("=" * 90)
say(f"k fit {KFIT}; pi^2 {PI2:.4f}; L1c weight on bullet-side gas {TH_SUB:.3f}")
# K4
RECS = {os.path.join(REPO, "hunt_2026", "h57_bullet_peaks.py"): ["(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0)", "(1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)", "(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)", '{"BCG1": 3.5e14, "BCG3": 2.3e14}', "SIG_CRIT = 1.827e9"],
        os.path.join(REPO, "opus_48_extended_research", "reviews", "bullet", "bullet_data_table.py"): ["(6,58,35.3), (-55,56,56.3), 5.5,0.6, 0.54,0.08, 0.36,0.06", "(6,58,30.2), (-55,56,35.9), 6.6,0.7, 0.23,0.02, 0.05,0.06", "(6,58,16.0), (-55,56,35.1), 2.7,0.3, 0.58,0.09, 0.20,0.05", "(6,58,21.2), (-55,56,30.0), 5.8,0.6, 0.12,0.01, 0.02,0.06"]}
miss = [s for p, v in RECS.items() for s in v if s not in open(p).read()]
check("K4", not miss and abs(KFIT["canonical"] - 13.2868) < 1e-3 and abs(KFIT["alt"] - 14.2506) < 1e-3, f"transcribed strings missing {miss}; k from UX3 JSON")
# K2
k2sys = System([(1e14, 400.0, 0.0, 0.0)], [(1e13, 100.0, 0.0, 0.0)], [(np.zeros(2), [0], [0])])
rt = np.array([20.0, 100.0, 300.0, 1000.0, 3000.0]); C = k2sys.ctx(rt, np.zeros(5), np.zeros(5)); a = A0F["canonical"]; k = 10.0; dev = {}
gg = np.abs(C["gas"][0][0]); gb = gg + np.abs(C["st"][0]); want = law(gb, a)*(1 + k*gg/a)
for fm in ("L1", "L2", "L1c", "N1", "N2"):
    e = k2sys.extra(dict(form=fm, k=k, a0=a), C, reg=False) if fm != "L1c" else None
    if fm == "L1c":
        sv = list(WEIGHTS); WEIGHTS[:] = [1.0]; e = k2sys.extra(dict(form=fm, k=k, a0=a), C, reg=False); WEIGHTS[:] = sv
    dev[fm] = float(np.max(np.abs((gb + np.abs(e[0]))/want - 1)))
check("K2", max(dev.values()) <= 1e-3, f"concentric cluster vs law x (1 + k g_gas/a0), max rel dev {dev}")
# specs
SP = {}
for f in FEET:
    SP[f"LAW|{f}"] = dict(form="LAW", k=0.0, a0=A0F[f], scale=2.0 if MUT else 1.0)
    if MUT: continue
    for fm in ("L1", "L2", "L1c", "N1", "N2", "N3a", "N3b"):
        for kl, kv in (("pi2", PI2), ("fit", KFIT[f])):
            SP[f"{fm}|{f}|{kl}"] = dict(form=fm, k=kv, a0=A0F[f])
    SP[f"S|{f}|fit"] = dict(form="S", k=KFIT[f], a0=A0F[f])
    for fm in ("L1", "L2", "N1", "N2"): SP[f"{fm}|{f}|halfk"] = dict(form=fm, k=0.5*KFIT[f], a0=A0F[f])
    for fm in ("L1", "L2"):
        for sc in (0.8, 1.2): SP[f"{fm}|{f}|gas{sc}"] = dict(form=fm, k=KFIT[f], a0=A0F[f], scale=sc)
R = run(SP)
# K1
X32 = json.load(open(os.path.join(RB, "X32_bullet_cold_sector", "x32_bullet_cold_sector_results.json")))["law_only"]; devs = []; pk_ok = True
OBS = {n: observe(*R[n]) for n in SP}
for f in FEET:
    o = OBS[f"LAW|{f}"]; x = X32[f]
    devs += [abs(o["M300"][0]/x["M300_BCG1"] - 1), abs(o["M300"][1]/x["M300_BCG3"] - 1), abs(o["main"]["dkappa"]/x["dkappa_main"] - 1), abs(o["sub"]["dkappa"]/x["dkappa_sub"] - 1)]
    pk_ok &= o["main"]["peak"] == x["peak_main"] and o["sub"]["peak"] == x["peak_sub"]
check("K1", max(devs) <= 1e-6 and pk_ok, f"k = 0 vs X32 law-only JSON, peaks equal {pk_ok}, max rel dev {max(devs):.2e}")
# K6 controls
CTRL = {}
for f in FEET:
    S0, m0 = R[f"LAW|{f}"]
    a_ = 150.0; tgt = np.array([OBS300["BCG1"] - m0["BCG1"], OBS300["BCG3"] - m0["BCG3"]])
    A = np.array([[M2D(*BCG1, 300.0, [(1.0, a_, *BCG1)]), M2D(*BCG1, 300.0, [(1.0, a_, *BCG3)])], [M2D(*BCG3, 300.0, [(1.0, a_, *BCG1)]), M2D(*BCG3, 300.0, [(1.0, a_, *BCG3)])]])
    Mc = np.linalg.solve(A, tgt)
    for lab, cen in (("onBCG", (BCG1, BCG3)), ("onGas", (GASM, GASB))):
        if MUT and lab == "onBCG": cen = (GASM, GASB)
        pl = [(Mc[0], a_, *cen[0]), (Mc[1], a_, *cen[1])]
        S = S0 + sig_pl(np.hypot(XX - cen[0][0], YY - cen[0][1]), Mc[0], a_) + sig_pl(np.hypot(XX - cen[1][0], YY - cen[1][1]), Mc[1], a_)
        m = {q: m0[q] + M2D(*c, Rq, pl) for q, (c, Rq) in APS.items()}
        CTRL[f"{lab}|{f}"] = observe(S, m)
check("K6", all(CTRL[f"onBCG|{f}"]["cls"] == "PASS" and CTRL[f"onGas|{f}"]["cls"] == "FAIL" for f in FEET), "controls " + str({k: v["cls"] for k, v in CTRL.items()}))
if not MUT:
    n = "L1|canonical|fit"; S = R[n][0]; mp = float(S[np.hypot(XX, YY) < 300.0].sum()*100.0); ms = R[n][1]["BCG1"]
    check("K3", abs(mp/ms - 1) <= 0.08, f"map M300 {mp:.3e} vs surface {ms:.3e} at BCG1, {100*(mp/ms - 1):+.1f} %")
    S1 = maps({n: SP[n]}, h=1.0)[n]; p0 = [peak(S, *PAIRS[k])[0].tolist() for k in PAIRS]; p1 = [peak(S1, *PAIRS[k])[0].tolist() for k in PAIRS]
    check("K7", p0 == p1 and abs(S1.max()/S.max() - 1) < 0.01, f"h 2 to 1 kpc: peaks {p0} vs {p1}, kappa max {S.max()/SIG_CRIT:.4f} vs {S1.max()/SIG_CRIT:.4f}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9
check("K5", rss < 4.0, "RSS under 4 GB")
print(f"RSS {rss:.2f} GB", file=sys.stderr)

say("\n=== model gas and stars in Clowe's 100 kpc apertures, 1e12 Msun (M_X; M_*) ===")
CLO = dict(bcg_main=(5.5, 0.54), gas_main=(6.6, 0.23), bcg_sub=(2.7, 0.58), gas_sub=(5.8, 0.12)); AP = {}
for q, (mx, ms) in CLO.items():
    c, Rq = APS[q]; mg = M2D(*c, Rq, GAS)/1e12; mg_ = M2D(*c, Rq, GAL)/1e12; AP[q] = [mg, mx, mg_, ms]
    say(f"  {q:9s} gas {mg:5.2f} (Clowe {mx}), stars {mg_:5.2f} (Clowe {ms})")
say("\n=== rows ===")
say("spec | peak main (d_gas, d_bcg, Z, lm) | peak sub | dkappa m, s | M300 1e14 (Z) | sub/main | class")
def row(n, o):
    a, b = o["main"], o["sub"]
    say(f"{n:24s} {a['peak']} {a['d_gas']:.0f},{a['d_bcg']:.0f} Z{a['Z']:+.2f} lm{int(a['local_max'])} | {b['peak']} {b['d_gas']:.0f},{b['d_bcg']:.0f} Z{b['Z']:+.2f} lm{int(b['local_max'])} | {a['dkappa']:+.3f} {b['dkappa']:+.3f} | {o['M300'][0]/1e14:.2f} ({o['ZO3'][0]:+.1f}) {o['M300'][1]/1e14:.2f} ({o['ZO3'][1]:+.1f}) | {o['ratio']:.2f} | {o['cls']}")
for n in SP: row(n, OBS[n])
for n in CTRL: row("ctrl " + n, CTRL[n])
LAB = {}
if not MUT:
    say("\n=== top local maxima, kappa units, k fit ===")
    for f in FEET:
        for fm in ("L1", "L2", "L1c", "N1", "N2", "N3a", "N3b", "S"):
            say(f"  {fm} {f}: {OBS[f'{fm}|{f}|fit']['top']}")
    say("\n=== labels ===")
    for fm in ("L1", "L2", "L1c", "N1", "N2", "N3a", "N3b"):
        cells = [OBS[f"{fm}|{f}|{k}"] for f in FEET for k in ("pi2", "fit")]; fit = [OBS[f"{fm}|{f}|fit"] for f in FEET]
        if all(c["pos_or_sign_fail"] for c in cells): l = "DEAD"
        elif all(c["cls"] == "PASS" for c in fit): l = "ALIVE"
        elif all(not c["pos_or_sign_fail"] for c in fit): l = "WOUNDED"
        else: l = "MIXED"
        LAB[fm] = l; say(f"  {fm}: {l}; cells {[c['cls'] for c in cells]}")
    mp = {}
    for fm in ("LAW", "L1", "L2", "N1", "N2"):
        n = f"{fm}|canonical" + ("" if fm == "LAW" else "|fit"); mp[fm] = np.round(R[n][0][::2, ::2]/SIG_CRIT, 4).tolist()
    json.dump(dict(x=XS[::2].tolist(), y=YS[::2].tolist(), units="kappa, Sigma/1.827e9", first_index="x", maps=mp), open(os.path.join(HERE, "ux6_maps_canonical_fit.json"), "w"))
need = ("K1", "K2", "K6")
json.dump(dict(checks=CHECKS, labels=LAB, rows=OBS, controls=CTRL, apertures=AP, kfit=KFIT, weight=TH_SUB), open(os.path.join(HERE, f"ux6_results{TAG}.json"), "w"), indent=1, default=float)
if MUT:
    say("MUTATE required failures: " + ", ".join(f"{k} {'FAILED' if not CHECKS[k] else 'passed (BAD)'}" for k in need)); OUT.close(); sys.exit(1)
say(f"\nVerdict allowed: {all(CHECKS[k] for k in need)}; failed checks: {[k for k, v in CHECKS.items() if not v]}"); OUT.close()
