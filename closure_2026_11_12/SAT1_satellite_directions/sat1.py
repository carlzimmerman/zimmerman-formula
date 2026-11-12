#!/usr/bin/env python3
"""SAT1: apparent enclosed mass at the Milky Way satellites' actual positions under G239's QUMOND
external-field formula, against the angle average. Criteria: FROZEN_CRITERIA.md (frozen first).
Run with python3 -I from this folder's parent or anywhere: paths are relative to this file.
Writes sat1.out, sat1_results.json; mutations to sat1_mut.out.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import csv, json, math, os, sys
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
EN = {"canonical": 0.01273, "alt": 0.01054}
FIELD_LB = (268.5, 33.0)
R0, ZSUN = 8.122, 0.0208
FLOOR = 0.2

OUT = open(os.path.join(HERE, "sat1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()

# ---- McMillan 2017 baryons (copied from G239 / MWJ1)
MC = dict(thin=dict(S0=896.0 * MSUN_PC2, Rd=2.50 * KPC, zd=0.300 * KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0 * MSUN_PC2, Rd=3.02 * KPC, zd=0.900 * KPC, Rm=0.0, vert="exp"),
          HI=dict(Sfid=10.0 * MSUN_PC2, Rfid=8.33 * KPC, Rd=7.00 * KPC, zd=0.085 * KPC, Rm=4.0 * KPC, vert="sech2"),
          H2=dict(Sfid=2.0 * MSUN_PC2, Rfid=8.33 * KPC, Rd=1.50 * KPC, zd=0.045 * KPC, Rm=12.0 * KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
_ZC = {}
def zprofile(c, n=1201):
    key = (c["vert"], round(c["zd"], 9))
    if key in _ZC: return _ZC[key]
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp"
          else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); cum /= cum[-1]
    _ZC[key] = (zg, cum); return _ZC[key]
_MS = {}
def M_sph(r_kpc):
    key = round(float(r_kpc), 6)
    if key not in _MS:
        r = float(r_kpc) * KPC; tot = MBULGE * r ** 2 / (r + ABULGE) ** 2
        Rg = np.linspace(1e-4 * KPC, min(r, 60 * KPC), 4000); h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
        for c in MC.values():
            zg, cum = zprofile(c); tot += float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
        _MS[key] = tot
    return _MS[key]
def M_hot(r_kpc): return 4.3e10 * MSUN * (r_kpc / 250.0) ** 1.5
def M_bar(r_kpc, hot): return M_sph(r_kpc) + (M_hot(r_kpc) if hot else 0.0)

def nu(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
MU = np.linspace(-1.0, 1.0, 4001)

def M_app(r_kpc, a0, e, mu, hot=False, rel=False):
    """G239's M_dyn_dir (vectorised in mu); rel subtracts the Galaxy's own uniform acceleration nu(e) e mu"""
    Mb = M_bar(r_kpc, hot); gb = G * Mb / (r_kpc * KPC) ** 2 / a0
    mu = np.asarray(mu, float)
    gm = np.sqrt(np.maximum(gb * gb + e * e + 2 * gb * e * mu, 0.0))
    gr = nu(gm) * (gb + e * mu)
    if rel and e > 0: gr = gr - float(nu(e)) * e * mu
    return gr / gb * Mb / MSUN / 1e11
def M_avg(r_kpc, a0, e, hot=False):
    return float(TRAPZ(M_app(r_kpc, a0, e, MU, hot), MU) / 2.0)

# ---- coordinates
DEG = math.pi / 180
RA_NGP, DEC_NGP, L_NCP = 192.85948 * DEG, 27.12825 * DEG, 122.93192 * DEG
def radec_to_lb(ra, dec):
    ra, dec = ra * DEG, dec * DEG
    sb = math.sin(dec) * math.sin(DEC_NGP) + math.cos(dec) * math.cos(DEC_NGP) * math.cos(ra - RA_NGP)
    b = math.asin(max(-1, min(1, sb)))
    y = math.cos(dec) * math.sin(ra - RA_NGP)
    x = math.sin(dec) * math.cos(DEC_NGP) - math.cos(dec) * math.sin(DEC_NGP) * math.cos(ra - RA_NGP)
    l = (L_NCP - math.atan2(y, x)) % (2 * math.pi)
    return l / DEG, b / DEG
def unit_lb(l, b):
    l, b = l * DEG, b * DEG; return np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])
def galcen(l, b, d):
    v = d * unit_lb(l, b); return np.array([v[0] - R0, v[1], v[2] + ZSUN])
def mu_of(pos, field_lb, sign=-1.0):
    return sign * float(np.dot(pos / np.linalg.norm(pos), unit_lb(*field_lb)))

# ---- PLT1 pull (copied)
S_FL = math.log10(1.0 + FLOOR)
def pull(Ml, r):
    side = math.log10(r["M"] / (r["M"] - r["lo"])) if Ml < r["M"] else math.log10((r["M"] + r["hi"]) / r["M"])
    return (math.log10(Ml) - math.log10(r["M"])) / math.hypot(side, S_FL)
PLT = json.load(open(os.path.join(ROOT, "closure_2026_11_12", "PLT1_outer_mass_vs_literature", "plt1_results.json")))
FAR_S = [r for r in PLT["rows"]["S"] if r["r"] >= 150.0]

FAILS = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")
    if not ok: FAILS.append(name)

# ---- data
def load(path):
    rows = list(csv.DictReader(open(path)))
    out = []
    for x in rows:
        try: dm = float(x["distance_modulus"]); ra = float(x["ra"]); dec = float(x["dec"])
        except ValueError: continue
        if not math.isfinite(dm): continue
        d = 10 ** (dm / 5 + 1) / 1000.0
        l, b = radec_to_lb(ra, dec); pos = galcen(l, b, d)
        try: pm = math.isfinite(float(x["pmra"]))
        except ValueError: pm = False
        out.append(dict(name=x["name"], host=x["host"], real=x["confirmed_real"] == "1",
                        gal=x["confirmed_galaxy"] == "1", l=l, b=b, d=d, r=float(np.linalg.norm(pos)), pos=pos, pm=pm))
    return rows, out
RAW, ALLSAT = load(os.path.join(HERE, "lvdb", "dwarf_mw.csv"))
def sample(kind):
    s = [x for x in ALLSAT if x["host"] == "mw" and 50.0 <= x["r"] <= 300.0]
    if kind == "primary": return [x for x in s if x["gal"]]
    if kind == "V-ALL": return [x for x in s if x["real"] or x["gal"]]
    if kind == "V-PM": return [x for x in s if x["gal"] and x["pm"]]
BINS = {"B1": (100.0, 150.0), "B2": (150.0, 300.0)}
def in_bin(x, bn):
    lo, hi = BINS[bn]; return lo <= x["r"] < hi if bn == "B1" else lo <= x["r"] <= hi

def bin_stats(sats, a0, e, field_lb=FIELD_LB, sign=-1.0, hot=False, rel=False, boot=True):
    res = {}
    for bn in BINS:
        s = [x for x in sats if in_bin(x, bn)]
        n = len(s)
        if n == 0: res[bn] = dict(n=0); continue
        mu = np.array([mu_of(x["pos"], field_lb, sign) for x in s])
        ma = np.array([float(M_app(x["r"], a0, e, m, hot, rel)) for x, m in zip(s, mu)])
        mv = np.array([M_avg(x["r"], a0, e, hot) for x in s])
        R = float(ma.mean() / mv.mean())
        d = dict(n=n, R_mean=R, R_med=float(np.median(ma) / np.median(mv)), med_ratio=float(np.median(ma / mv)),
                 mean_app=float(ma.mean()), mean_avg=float(mv.mean()), med_app=float(np.median(ma)), med_avg=float(np.median(mv)),
                 n_neg=int(np.sum(ma < 0)), mean_mu=float(mu.mean()), mean_mu2=float((mu ** 2).mean()),
                 names=[x["name"] for x in s], mu=mu.tolist(), M_app=ma.tolist(), M_avg=mv.tolist(), r=[x["r"] for x in s])
        if n > 1:
            loo = [float(np.delete(ma, i).mean() / np.delete(mv, i).mean()) for i in range(n)]
            d["loo"] = (min(loo), max(loo))
        if boot and n > 1:
            rng = np.random.default_rng(12); bs = []
            for _ in range(2000):
                k = rng.integers(0, n, n); bs.append(ma[k].mean() / mv[k].mean())
            d["boot16_84"] = (float(np.percentile(bs, 16)), float(np.percentile(bs, 84)))
        res[bn] = d
    return res

def factor_F(a0, e, hot):
    def med(F): return float(np.median([pull(F * M_avg(r["r"], a0, e, hot), r) for r in FAR_S]))
    if med(1.0) >= -2:
        lo, hi = 0.2, 1.0
    else:
        lo, hi = 1.0, 5.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if med(mid) < -2: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi), med(1.0), med
def label_B2(d, F):
    if d["n"] < 5: return "NO POWER"
    def lab(R):
        en = R >= F
        if R >= 1.02: return "ANISOTROPY RAISES IT ENOUGH" if en else "ANISOTROPY RAISES IT, NOT ENOUGH"
        if R <= 0.98: return "ANISOTROPY LOWERS IT" + (", STILL ENOUGH" if en else ", NOT ENOUGH")
        return "NO CHANGE" + (", ENOUGH" if en else ", NOT ENOUGH")
    L = lab(d["R_mean"])
    if "loo" in d and (lab(d["loo"][0]) != L or lab(d["loo"][1]) != L): L += ", FRAGILE"
    return L
def label_B1(d):
    if d["n"] < 5: return "NO POWER"
    def lab(R): return "RAISES" if R >= 1.02 else ("LOWERS" if R <= 0.98 else "NO CHANGE")
    L = lab(d["R_mean"])
    if "loo" in d and (lab(d["loo"][0]) != L or lab(d["loo"][1]) != L): L += ", FRAGILE"
    return L

# =================================================================================================
say("SAT1  satellites' actual directions vs the external field, G239's QUMOND formula. kappa = 1/2 FITTED.")
say("Known-answer checks first; labels only if all pass.")
a0c, ec = A0["canonical"], EN["canonical"]
# KA1
rng = np.random.default_rng(7); mur = rng.uniform(-1, 1, 20000000)   # AMENDMENT_A1: 2e7 draws (run 1 used 2e5)
_ma = M_app(200.0, a0c, ec, mur); iso = float(_ma.mean()); se = float(_ma.std() / math.sqrt(len(mur))); del _ma
quadv = M_avg(200.0, a0c, ec)
ka("KA1 isotropic directions reproduce G239's angle average at 200 kpc (5.264e11, 0.5 per cent) and the quadrature",
   abs(iso / 5.264 - 1) <= 0.005 and abs(iso / quadv - 1) <= 0.005,
   f"isotropic mean {iso:.4f}e11 +- {se:.4f} (MC s.e., 2e7 draws), quadrature {quadv:.4f}e11")
# KA2
m80 = M_avg(80.0, a0c, ec); par = float(M_app(80.0, a0c, ec, 1.0)) / m80 - 1; perp = float(M_app(80.0, a0c, ec, 0.0)) / m80 - 1
ka("KA2 G239 anisotropy at 80 kpc: parallel +0.58 and perpendicular +0.01, each to 1 percentage point",
   abs(par - 0.58) <= 0.01 and abs(perp - 0.01) <= 0.01, f"parallel {par:+.4f}, perpendicular {perp:+.4f}, M_avg(80) {m80:.4f}e11")
# KA3
r1 = float(np.linalg.norm(galcen(0, 0, R0))); r2 = float(np.linalg.norm(galcen(180, 0, 10.0)))
_, bp = radec_to_lb(192.85948, 27.12825); ls, bs_ = radec_to_lb(266.40500, -28.93617)
dl = ((ls - 359.94 + 180) % 360) - 180
pf = 200.0 * unit_lb(*FIELD_LB); mu_par = mu_of(pf, FIELD_LB); mu_anti = mu_of(-pf, FIELD_LB)
m200 = M_avg(200.0, a0c, ec)
ok3 = (r1 < 0.03 and abs(r2 - 18.122) < 0.03 and abs(bp - 90) < 0.01 and abs(dl) < 0.1 and abs(bs_ + 0.05) < 0.1
       and abs(mu_par + 1) < 1e-12 and float(M_app(200.0, a0c, ec, mu_par)) < m200
       and abs(mu_anti - 1) < 1e-12 and float(M_app(200.0, a0c, ec, mu_anti)) > m200)
ka("KA3 geometry, coordinates and sign convention", ok3,
   f"r(Sun-GC) {r1:.4f}, r(180,0,10) {r2:.4f}, NGP b {bp:.4f}, SgrA* ({ls:.3f},{bs_:.3f}); along field mu {mu_par:+.0f} "
   f"M {float(M_app(200.0, a0c, ec, mu_par)):.3f}; opposite mu {mu_anti:+.0f} M {float(M_app(200.0, a0c, ec, mu_anti)):.3f}; avg {m200:.3f}")
# KA4 independent SI
Mb_SI = M_sph(200.0); rSI = 200.0 * KPC; gN = G * Mb_SI / rSI ** 2; gext = ec * a0c
def integrand(m):
    gtot = math.sqrt(gN ** 2 + gext ** 2 + 2 * gN * gext * m)
    return (1.0 / (1.0 - math.exp(-math.sqrt(gtot / a0c)))) * (gN + gext * m)
gr_SI = quad(integrand, -1, 1, epsabs=0, epsrel=1e-11)[0] / 2.0
MSI = rSI ** 2 * gr_SI / G / MSUN / 1e11
ka("KA4 SI hand check of M_avg(200 kpc) canonical with scipy quad", abs(MSI / m200 - 1) <= 0.001,
   f"SI {MSI:.5f}e11 vs script {m200:.5f}e11; M_b(<200) {Mb_SI/MSUN:.4e} Msun")
# KA5
byname = {x["name"]: x for x in ALLSAT}
lmc = byname.get("LMC"); leo = byname.get("Leo I"); prim = sample("primary")
ka("KA5 data: LMC 45-55 kpc helio, Leo I 240-270 kpc Galactocentric, >= 20 primary rows in 50-300 kpc",
   lmc is not None and 45 <= lmc["d"] <= 55 and leo is not None and 240 <= leo["r"] <= 270 and len(prim) >= 20,
   f"{len(RAW)} rows read; LMC d {lmc['d']:.2f}; Leo I r {leo['r']:.1f}; primary n {len(prim)}")
# KA6 factor
FAC = {}
for f in A0:
    for hot in (False, True):
        F, m1, med = factor_F(A0[f], EN[f], hot)
        FAC[(f, hot)] = dict(F=F, med_at_1=m1, med_at_F=med(F))
okF = all(abs(v["med_at_F"] + 2) < 1e-3 for v in FAC.values() if v["F"] > 1)
ka("KA6 the scaled line at F gives median class-S plateau pull -2 to 1e-3", okF,
   "; ".join(f"{f}{' HOT' if h else ''}: F {v['F']:.4f} (median at F=1 {v['med_at_1']:+.3f}, at F {v['med_at_F']:+.4f})" for (f, h), v in FAC.items()))
if FAILS:
    say(f"STOP: known-answer check(s) failed: {FAILS}. No label printed."); OUT.close(); sys.exit(1)

# =================================================================================================
say("\nSAMPLE (primary: host mw, confirmed galaxy, 50 <= r <= 300 kpc; mu = -cos psi, field to (268.5, +33.0))")
say("  name                        l       b       d_helio  r_GC    cos(psi)")
for x in sorted(prim, key=lambda x: x["r"]):
    say(f"  {x['name'][:26]:26s} {x['l']:7.2f} {x['b']:+7.2f} {x['d']:8.1f} {x['r']:7.1f}  {-mu_of(x['pos'], FIELD_LB):+.3f}")

RES = dict(lane="SAT1", date="2026-11-12", criteria_sha256=open(os.path.join(HERE, "FREEZE_STAMP.txt")).read().split()[-1],
           data="lvdb/dwarf_mw.csv", factors={f"{f}{'_HOT' if h else ''}": v["F"] for (f, h), v in FAC.items()}, cases={})
def show(tag, st, F):
    for bn in BINS:
        d = st[bn]
        if d["n"] == 0: say(f"  {tag} {bn}: n = 0"); continue
        lab = label_B2(d, F) if bn == "B2" else label_B1(d)
        say(f"  {tag} {bn} n={d['n']:2d}: mean M_app {d['mean_app']:.3f} vs mean M_avg {d['mean_avg']:.3f} -> R_mean {d['R_mean']:.3f} "
            f"[LOO {d.get('loo',(float('nan'),)*2)[0]:.3f}-{d.get('loo',(float('nan'),)*2)[1]:.3f}; boot16-84 "
            f"{d.get('boot16_84',(float('nan'),)*2)[0]:.3f}-{d.get('boot16_84',(float('nan'),)*2)[1]:.3f}]; "
            f"median {d['med_app']:.3f} vs {d['med_avg']:.3f} -> R_med {d['R_med']:.3f}; median per-sat ratio {d['med_ratio']:.3f}; "
            f"negative {d['n_neg']}; <mu> {d['mean_mu']:+.3f}, <mu^2> {d['mean_mu2']:.3f}  => {lab}"
            + (f"  (F = {F:.3f})" if bn == "B2" else ""))
        RES["cases"].setdefault(tag, {})[bn] = dict({k: v for k, v in d.items()}, label=lab)

say("\nGRADED (headline = census, primary sample) and variants")
for hot in (False, True):
    for kind in ("primary", "V-ALL", "V-PM"):
        for rel in (False, True):
            for f in A0:
                tag = f"{f:9s} {'HOT   ' if hot else 'census'} {kind:7s} {'REL' if rel else 'G239'}"
                st = bin_stats(sample(kind), A0[f], EN[f], hot=hot, rel=rel)
                show(tag, st, FAC[(f, hot)]["F"])
json.dump(RES, open(os.path.join(HERE, "sat1_results.json"), "w"), indent=1, default=float)

# =================================================================================================
MUT = open(os.path.join(HERE, "sat1_mut.out"), "w")
def ms(s): print(s); MUT.write(s + "\n")
ms("SAT1 MUTATIONS (census, primary sample)")
bite1 = bite2 = bite3 = True
for f in A0:
    base = bin_stats(prim, A0[f], EN[f], boot=False)
    Rb = base["B2"]["R_mean"]
    ra_ = bin_stats(prim, A0[f], EN[f], field_lb=(358.5, 33.0), boot=False)["B2"]["R_mean"]
    rb_ = bin_stats(prim, A0[f], EN[f], field_lb=(88.5, 57.0), boot=False)["B2"]["R_mean"]
    b1 = max(abs(ra_ - Rb), abs(rb_ - Rb)) >= 0.01; bite1 &= b1
    ms(f"  {f}: M1 rotate 90 deg: B2 R_mean {Rb:.4f} -> M1a (358.5,+33) {ra_:.4f}, M1b (88.5,+57) {rb_:.4f} [{'bites' if b1 else 'DOES NOT BITE'}]")
    ra1 = bin_stats(prim, A0[f], EN[f], field_lb=(358.5, 33.0), boot=False)["B1"]["R_mean"]
    rb1 = bin_stats(prim, A0[f], EN[f], field_lb=(88.5, 57.0), boot=False)["B1"]["R_mean"]
    ms(f"        B1 R_mean {base['B1']['R_mean']:.4f} -> M1a {ra1:.4f}, M1b {rb1:.4f}")
    fl = bin_stats(prim, A0[f], EN[f], sign=+1.0, boot=False)["B2"]["R_mean"]
    b2 = abs(fl - Rb) >= 0.01; bite2 &= b2
    ms(f"  {f}: M2 flip sign (mu = +cos psi): B2 R_mean {Rb:.4f} -> {fl:.4f} [{'bites' if b2 else 'DOES NOT BITE'}]")
    z = bin_stats(prim, A0[f], 0.0, boot=False)
    b3 = all(abs(z[bn]["R_mean"] - 1) < 1e-9 for bn in BINS); bite3 &= b3
    ms(f"  {f}: M3 e_N = 0: R_mean B1 {z['B1']['R_mean']:.12f}, B2 {z['B2']['R_mean']:.12f} [{'as required' if b3 else 'FAILS'}]")
ms(f"M1 {'BITES' if bite1 else 'DOES NOT BITE'}; M2 {'BITES' if bite2 else 'DOES NOT BITE'}; M3 {'PASSES' if bite3 else 'FAILS'}")
MUT.close()
say(f"\nMutations: M1 {'bites' if bite1 else 'DOES NOT BITE'}, M2 {'bites' if bite2 else 'DOES NOT BITE'}, M3 {'passes' if bite3 else 'FAILS'} (sat1_mut.out)")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
