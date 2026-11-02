#!/usr/bin/env python3
"""MX1 Bullet with the cold placed, MG1's pairs, P2 curl. UX6's and MG1's scripts are read for inputs, map and grader; the rule is this lane's. MX1_MUTATE=1 is the twin. Reinstates nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, HERE)
import mx1_core as M
MUT = M.MUT; TAG = "_MUTATE" if MUT else ""; OUT = open(os.path.join(HERE, f"mx1_bullet{TAG}.out"), "w"); RES = {}
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CH = {}
def check(n, ok, d): CH[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = tuple(A0F)
AX = 1.5 if MUT else 1.0
# ---------- UX6
p = os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py"); s = open(p).read().split('say("=" * 90); say("UX6')[0]; a = 'OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")'; assert s.count(a) == 1; s = s.replace(a, "import io as _io; OUT = _io.StringIO()")
n = {"__file__": p, "__name__": "b"}; exec(compile(s, p, "exec"), n); SYS = n["SYS"]; GAS, GAL, KPC = n["GAS"], n["GAL"], n["KPC"]; REF = json.load(open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_results.json")))
def pl_enc(comps, Rkpc): return sum(m * Rkpc ** 3 / (Rkpc ** 2 + a ** 2) ** 1.5 for m, a, *_ in comps)
GR = [("main", (0.0, 0.0), [GAS[0], GAL[0]]), ("sub", (820.0, 220.0), [GAS[1], GAS[2], GAS[3], GAL[1]])]
TAB = {}
def table(mass):
    if mass in TAB: return TAB[mass]
    o = []
    for nm, c, comps in GR:
        Mt = pl_enc(comps, 3e5); M200 = M.m200_rule(lambda R: max(pl_enc(comps, R / (M.PCM * 1e3)), 1e-30), mass, Mt); h = M.Halo(M200, True); rk = np.geomspace(0.1, 3e4, 1200); Mr = h.M0(rk * 1e3 * M.PCM); o.append((nm, c, np.log(rk), M.GN * Mr * M.MSUN / KPC ** 2 / rk ** 3, M200, h.R / (M.PCM * 1e3)))
    TAB[mass] = o; return o
def coldv(C, mass):
    k = "cold_" + mass
    if k not in C:
        v = [0.0, 0.0, 0.0]
        for _, c, lr, f, *_r in table(mass):
            dx, dy, dz = C["X"] - c[0], C["Y"] - c[1], C["Z"]; r = np.maximum(np.sqrt(dx * dx + dy * dy + dz * dz), 0.1); w = -np.interp(np.log(r), lr, f); v[0] = v[0] + w * dx; v[1] = v[1] + w * dy; v[2] = v[2] + w * dz
        C[k] = v
    return C[k]
def Bfun(g, a): return n["law"](g, a) - g
def A_(g, a):
    u = 0.5 * g + a; s_ = np.sqrt(np.maximum(u * u - a * a, 0)); return 0.25 * g * g + u * s_ - a * a * np.log((u + s_) / a)
def h_(g, a):
    q = np.minimum(g / a, 1 - 1e-12); return a * (-g - a * np.log1p(-q))
def extra(sp, C, reg=True):
    a0 = sp["a0"] * AX; f = sp["form"]; gv = tuple(sum(q[i] for q in C["gas"]) for i in range(3)); gb = [gv[i] + C["st"][i] for i in range(3)]
    if reg: gb[1] = gb[1] + a0 / 1000.0
    g = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2); L = n["law"](g, a0); m = L / np.maximum(g, 1e-300)
    if f in ("onBCG", "onGas"):
        P = sp["pl"]; v = [n["fld"](C["X"], C["Y"], C["Z"], q) for q in P]; t = tuple(sum(q[i] for q in v) for i in range(3)); return tuple(gb[i] * (m - 1) + t[i] for i in range(3))
    cv = coldv(C, sp.get("mass", "share")); X = sp.get("X", 1.0); cv = [X * q for q in cv]; Cv = [gb[i] + cv[i] for i in range(3)]; Cm = np.sqrt(Cv[0] ** 2 + Cv[1] ** 2 + Cv[2] ** 2)
    if f == "V0": return tuple(gb[i] * (m - 1) + cv[i] for i in range(3))
    if f == "V1": z = Cm > L
    elif f == "V2":
        g2 = np.sqrt(cv[0] ** 2 + cv[1] ** 2 + cv[2] ** 2); z = 0.5 * Cm * Cm > A_(g, a0) + h_(g2, a0)
    elif f == "V4":
        g2 = np.sqrt(cv[0] ** 2 + cv[1] ** 2 + cv[2] ** 2); z = g2 >= Bfun(g, a0)
    elif f == "V3":
        pw = 8.0; Nn = np.maximum(np.maximum(L, Cm), 1e-300); wl = (L / Nn) ** pw; wc = (Cm / Nn) ** pw; tot = Nn * (wl + wc) ** (1 / pw); u = [(wl * gb[i] * m + wc * Cv[i]) for i in range(3)]; um = np.maximum(np.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2), 1e-300); return tuple(u[i] / um * tot - gb[i] for i in range(3))
    else: raise ValueError(f)
    return tuple(np.where(z, cv[i], gb[i] * (m - 1)) for i in range(3))
SYS.extra = extra
say("=" * 90); say("MX1 Bullet" + (" [MUTATE]" if MUT else "")); say("=" * 90)
for mass in ("share", "em1"):
    for t in table(mass): say(f"  {mass} {t[0]}: M200 {t[4]:.3e}, R200 {t[5]:.0f} kpc")
RES["halos"] = {mass: {t[0]: dict(M200=t[4], R200=t[5]) for t in table(mass)} for mass in ("share", "em1")}
SP = {}
for f in FEET:
    SP[f"K5|{f}"] = dict(form="V1", a0=A0F[f], X=0.0)
    for fm in ("V0", "V1", "V2", "V3", "V4"): SP[f"{fm}|{f}"] = dict(form=fm, a0=A0F[f])
    SP[f"V1em1|{f}"] = dict(form="V1", a0=A0F[f], mass="em1")
    SP[f"V0em1|{f}"] = dict(form="V0", a0=A0F[f], mass="em1")
    SP[f"onBCG|{f}"] = dict(form="onBCG", a0=A0F[f], pl=[(3.0e14, 150.0, 0.0, 0.0), (2.0e14, 150.0, 820.0, 220.0)]); SP[f"onGas|{f}"] = dict(form="onGas", a0=A0F[f], pl=[(3.0e14, 150.0, 190.0, 90.0), (2.0e14, 150.0, 670.0, 170.0)])
R = n["run"](SP); O = {}
for k, (S, m) in R.items(): O[k] = n["observe"](S, m)
for f in FEET:
    r = REF["rows"][f"LAW|{f}"]; o = O[f"K5|{f}"]; dm = max(abs(o["M300"][i] / r["M300"][i] - 1) for i in (0, 1)); dk = max(abs(o[q]["dkappa"] / r[q]["dkappa"] - 1) for q in ("main", "sub")); pk = all(o[q]["peak"] == r[q]["peak"] for q in ("main", "sub"))
    check(f"K5 {f}", dm < 1e-6 and dk < 1e-6 and pk, f"cold x 0 vs UX6's LAW: M300 rel {dm:.2e}, dkappa rel {dk:.2e}, peaks equal {pk}")
    check(f"K6 {f}", (O[f"onBCG|{f}"]["cls"] != "FAIL") and (O[f"onGas|{f}"]["cls"] == "FAIL"), f"control on BCGs {O[f'onBCG|{f}']['cls']}, M300 {O[f'onBCG|{f}']['M300'][0]:.2e} {O[f'onBCG|{f}']['M300'][1]:.2e}; on gas {O[f'onGas|{f}']['cls']}")
say("\nform|foot class | main peak delta Z dkappa | sub peak delta Z dkappa | M300 ZO3 | B28 line: PASS only if class not FAIL and |Z_M| <= 2")
for k, o in O.items():
    B = o["cls"] != "FAIL" and all(abs(z) <= 2 for z in o["ZO3"]); o["B28"] = "PASS" if B else "FAIL"
    say(f"{k:14s} {o['cls']:8s} | {o['main']['peak']} {o['main']['delta']:.2f} {o['main']['Z']:+.2f} {o['main']['dkappa']:+.3f} guard {o['main']['guard']} | {o['sub']['peak']} {o['sub']['delta']:.2f} {o['sub']['Z']:+.2f} {o['sub']['dkappa']:+.3f} guard {o['sub']['guard']} | {o['M300'][0]:.3e} {o['M300'][1]:.3e} Z {o['ZO3'][0]:+.2f} {o['ZO3'][1]:+.2f} ratio {o['ratio']:.3f} | M2D<250 {o['M250'][0]:.2e} {o['M250'][1]:.2e} | B28 {o['B28']}")
RES["bullet"] = O
# K7, h 1 and map vs surface
S1 = n["maps"]({"V1": SP["V1|canonical"]}, h=1.0)["V1"]; S2 = R["V1|canonical"][0]; d = float(abs(S1.max() / S2.max() - 1)); i1 = np.unravel_index(np.argmax(S1), S1.shape); i2 = np.unravel_index(np.argmax(S2), S2.shape); dp = float(10.0 * math.hypot(i1[0] - i2[0], i1[1] - i2[1]))
check("K7", d <= 0.03 and dp <= 10.0, f"V1 canonical h 2 to 1 kpc: kappa max rel {d:.4f}, global peak moved {dp:.0f} kpc")
XX, YY = n["XX"], n["YY"]
mask = (np.hypot(XX, YY) > 30.0) & (np.hypot(XX - 820.0, YY - 220.0) > 30.0); pre = float(np.max(np.abs(S1[mask] / S2[mask] - 1))); pm = float(np.median(np.abs(S1[mask] / S2[mask] - 1))); hit = np.unravel_index(np.argmax(np.where(mask, np.abs(S1 / S2 - 1), 0)), S1.shape); RES["K7_detail"] = dict(kappa_max_rel=d, off_cusp_max=pre, off_cusp_median=pm, where=[float(XX[hit]), float(YY[hit])]); say(f"  K7 detail, added: outside 30 kpc of each BCG, h 2 to 1 kpc, Sigma rel change max {pre:.4f} at {XX[hit]:.0f}, {YY[hit]:.0f}, median {pm:.5f}. Inside 30 kpc is the cold's own cusp on the grid point")
for key in ("V1|canonical", "V1|alt"):
    S = R[key][0]; m_ = R[key][1]; cyl = np.hypot(XX, YY) <= 300.0; mm = float(S[cyl].sum() * 100.0); say(f"  map vs flux M300 BCG1, {key}: map {mm:.3e}, flux {m_['BCG1']:.3e}, rel {mm / m_['BCG1'] - 1:+.3f} (UX6's tolerance 8 %)"); RES.setdefault("map_vs_flux", {})[key] = mm / m_["BCG1"] - 1
# ---------- zones on BCG lines, plain numbers
def line(a, b, nn=15): return np.linspace(a[0], b[0], nn), np.linspace(a[1], b[1], nn)
for f in FEET:
    x, y = line((-200.0, -100.0), (1000.0, 300.0), 25); C = SYS.ctx(x, y, 0 * x); e = extra(dict(form="V1", a0=A0F[f]), C); gv = tuple(sum(q[i] for q in C["gas"]) for i in range(3)); gb = [gv[i] + C["st"][i] for i in range(3)]; g = np.sqrt(sum(q * q for q in gb)); L = n["law"](g, A0F[f] * AX); cv = coldv(C, "share"); Cm = np.sqrt(sum((gb[i] + cv[i]) ** 2 for i in range(3))); RES.setdefault("zone_line", {})[f] = dict(x=x.tolist(), lnCL=np.log(Cm / L).tolist()); say(f"  ln(C/L) along the bar, {f}: " + " ".join(f"{a:+.2f}" for a in np.log(Cm / L)))
# ---------- P2
xs = np.arange(-500.0, 1400.0 + 1e-9, 20.0); ys = np.arange(-400.0, 700.0 + 1e-9, 20.0); zs = np.arange(-600.0, 600.0 + 1e-9, 20.0); X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij"); dl = 20.0 * KPC
def total(sp):
    C = SYS.ctx(X, Y, Z); e = extra(sp, C); gv = tuple(sum(q[i] for q in C["gas"]) for i in range(3)); gb = [gv[i] + C["st"][i] for i in range(3)]; gb[1] = gb[1] + sp["a0"] * AX / 1000.0; return [gb[i] + e[i] for i in range(3)], C, gb
P2 = {}
for f in FEET:
    for fm in ("V0", "V1", "V3", "V4"):
        sp = dict(form=fm, a0=A0F[f]); v, C, gb = total(sp); D = [np.gradient(v[i], dl, axis=j) for i in range(3) for j in range(3)]; div = D[0] + D[4] + D[8]; cu = np.sqrt((D[7] - D[5]) ** 2 + (D[2] - D[6]) ** 2 + (D[3] - D[1]) ** 2); g = np.sqrt(sum(q * q for q in gb)); L = n["law"](g, sp["a0"] * AX); cv = coldv(C, "share"); Cm = np.sqrt(sum((gb[i] + cv[i]) ** 2 for i in range(3))); z = Cm > L; b = np.zeros_like(z)
        for ax in range(3): b |= z ^ np.roll(z, 1, axis=ax)
        P2[f"{fm}|{f}"] = dict(curl_over_div=float(np.sqrt((cu ** 2).mean()) / np.sqrt((div ** 2).mean())), share_absdiv_boundary=float(np.abs(div[b]).sum() / np.abs(div).sum()), vol_boundary=float(b.mean()), vol_cold_zone=float(z.mean()))
        say(f"  P2 {fm}|{f}: rms curl/rms div {P2[f'{fm}|{f}']['curl_over_div']:.4f}; share of |div| in boundary cells {P2[f'{fm}|{f}']['share_absdiv_boundary']:.3f} in {P2[f'{fm}|{f}']['vol_boundary']:.3f} of volume; cold zone {P2[f'{fm}|{f}']['vol_cold_zone']:.3f} of volume")
RES["P2"] = P2
# ---------- MG1
p = os.path.join(RB, "MG1_merger_sample", "mg1_merger.py"); s = open(p).read().split('say("=" * 90); say("MG1_merger_sample"')[0]; a = 'OUT = open(os.path.join(HERE, f"mg1_merger{TAG}.out"), "w")'; assert s.count(a) == 1; s = s.replace(a, "import io as _io; OUT = _io.StringIO()"); m1 = {"__file__": p, "__name__": "g"}; exec(compile(s, p, "exec"), m1)
CUR = {}
def extra_pair(form, k, a0, gas, star, s_, C, tabs, reg=True):
    a0 = a0 * AX; gv, st = C["g"], C["st"]; gb = [gv[i] + st[i] for i in range(3)]
    if reg: gb[1] = gb[1] + a0 / 1000.0
    g = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2); L = m1["law"](g, a0); m_ = L / np.maximum(g, 1e-300)
    if form == "LAW": return tuple(gb[i] * (m_ - 1) for i in range(3))
    dx = C["X"] - s_; dy = C["Y"]; dz = C["Z"]; r = np.maximum(np.sqrt(dx * dx + dy * dy + dz * dz), 0.1); w = -np.interp(np.log(r), CUR["lr"], CUR["f"]); cv = (w * dx, w * dy, w * dz)
    if form == "V0": return tuple(gb[i] * (m_ - 1) + cv[i] for i in range(3))
    Cv = [gb[i] + cv[i] for i in range(3)]; z = np.sqrt(Cv[0] ** 2 + Cv[1] ** 2 + Cv[2] ** 2) > L; return tuple(np.where(z, cv[i], gb[i] * (m_ - 1)) for i in range(3))
m1["extra"] = extra_pair
MG = {}; say("\nMG1 rows, PROVISIONAL inputs. system sub | observed | s | M200 | V1 canonical delta dkappa, d(peak, gal) | V1 alt | V0 canonical | LAW canonical")
sp_ = {f"{fm}|{f}": (fm, 0.0, A0F[f]) for f in FEET for fm in ("LAW", "V0", "V1")}
for r in m1["rows"]:
    comps = [(r["M_gas"], r["a_gas"]), (r["M_star"], r["a_star"])]; M200 = M.m200_rule(lambda R: max(pl_enc(comps, R / (M.PCM * 1e3)), 1e-30), "share", r["M_gas"] + r["M_star"]); h = M.Halo(M200, True); rk = np.geomspace(0.1, 3e4, 800); CUR.update(lr=np.log(rk), f=M.GN * h.M0(rk * 1e3 * M.PCM) * M.MSUN / KPC ** 2 / rk ** 3)
    res, _ = m1["run_pair"]((r["M_gas"], r["a_gas"]), (r["M_star"], r["a_star"]), r["s"], sp_); L_, zg, zq = m1["label"](r["d_lens_gal"], r["e_lens_gal"], r["d_lens_gas"], r["e_lens_gas"]); t = f"{r['system']} {r['sub']}"
    for q in res.values(): q["d_gal"] = float(math.hypot(q["peak"][0] - r["s"], q["peak"][1]))
    MG[t] = dict(system=r["system"], counted=r["counted"] == "yes", label=L_, s=r["s"], s_over_row=r["s"] / r["e_lens_gas"], M200=M200, M_lens=r["M_lens"], d_lens_gal=r["d_lens_gal"], e_lens_gal=r["e_lens_gal"], res=res)
    say(f"{t:18s} {L_:10s} s {r['s']:5.0f} M200 {M200:.2e} M_lens {r['M_lens']:.2e} | V1c {res['V1|canonical']['delta']:.2f} {res['V1|canonical']['dkappa']:+.3f} d {res['V1|canonical']['d_gal']:.0f} (obs {r['d_lens_gal']:.0f}+-{r['e_lens_gal']:.0f}) | V1a {res['V1|alt']['delta']:.2f} {res['V1|alt']['dkappa']:+.3f} | V0c {res['V0|canonical']['dkappa']:+.3f} | LAWc {res['LAW|canonical']['dkappa']:+.3f}")
RES["mg1"] = MG
for f in FEET:
    for fm in ("V1", "V0", "LAW"):
        pr = {k: v for k, v in MG.items() if v["counted"] and v["s_over_row"] > 2}; g_ = sum(1 for v in pr.values() if v["res"][f"{fm}|{f}"]["dkappa"] > 0 and v["res"][f"{fm}|{f}"]["delta"] > 0.5); ag = sum(1 for v in pr.values() if v["label"] == "GAL" and v["res"][f"{fm}|{f}"]["dkappa"] > 0 and v["res"][f"{fm}|{f}"]["delta"] > 0.5); ngal = sum(1 for v in pr.values() if v["label"] == "GAL"); ngas = sum(1 for v in pr.values() if v["label"] == "GAS"); say(f"  MG1 primary, {fm}|{f}: {len(pr)} rows, observed GAL {ngal}, GAS {ngas}; model galaxy-side {g_}; observed GAL and model galaxy-side {ag}"); RES.setdefault("mg1_tally", {})[f"{fm}|{f}"] = dict(rows=len(pr), obs_gal=ngal, obs_gas=ngas, model_gal=g_, both=ag)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; check("RSS", rss < 4, f"{rss:.2f} GB"); RES["checks"] = CH
json.dump(RES, open(os.path.join(HERE, f"mx1_bullet_results{TAG}.json"), "w"), indent=1, sort_keys=True, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
if not all(CH.values()): say("CHECK FAILED", [k for k, v in CH.items() if not v]); OUT.close(); sys.exit(1)
OUT.close()
