#!/usr/bin/env python3
"""MG1: position and sign reading on published merger offsets. Criteria FROZEN_CRITERIA.md, amendments AMENDMENTS.md. MG1_MUTATE=1 for the twin.
Table numbers PROVISIONAL (web reading). A description, no action. kappa = 1/2 FITTED; not theory closed. Reinstates nothing."""
import os, sys, json, math, csv, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
MUT = os.environ.get("MG1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"mg1_merger{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CHECKS = {}
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30; SIG_CRIT = 1.827e9
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
KFIT = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json"))); PI2 = math.pi**2

# ---------- labels, data only
def label(dg, eg, dq, eq, th=2.0):
    zg, zq = dg/eg, dq/eq
    if zg <= th and zq > th: return "GAL", zg, zq
    if zq <= th and zg > th: return "GAS", zg, zq
    if zg > th and zq > th: return "BETWEEN", zg, zq
    return "UNRESOLVED", zg, zq

# ---------- MACS J0025 from Table 2, arcmin to kpc at the paper's 6.61 kpc per arcsec
SC = 6.61*60
def vec_err(a, ea, b, eb):
    d = np.array(a) - np.array(b); n = float(np.hypot(*d)); u = d/n
    e = math.sqrt((u[0]**2)*(ea[0]**2 + eb[0]**2) + (u[1]**2)*(ea[1]**2 + eb[1]**2)); return n*SC, e*SC
J25 = dict(SE=dict(l=(-0.70, -0.43), el=(0.25, 0.06), g=(-0.79, -0.50), eg=(0.20, 0.20)), NW=dict(l=(0.46, 0.20), el=(0.13, 0.04), g=(0.39, 0.18), eg=(0.20, 0.20)))
GP = (1e-9, 1e-9); EGP = (0.08, 0.08)
rows = list(csv.DictReader(open(os.path.join(HERE, "mg1_table.csv"))))
for r in rows:
    if r["system"] == "MACS J0025":
        p = J25[r["sub"]]; a = vec_err(p["l"], p["el"], p["g"], p["eg"]); b = vec_err(p["l"], p["el"], GP, EGP); c = vec_err(p["g"], p["eg"], GP, EGP)
        r.update(d_lens_gal=a[0], e_lens_gal=a[1], d_lens_gas=b[0], e_lens_gas=b[1], s=c[0], e_s=c[1])
    for k in ("z", "d_lens_gal", "e_lens_gal", "d_lens_gas", "e_lens_gas", "s", "e_s", "M_lens", "a_gas", "a_star"): r[k] = float(r[k])
    for k, f in (("M_gas", 0.12), ("M_star", 0.02)): r[k] = f*r["M_lens"] if r[k] == "DEFAULT" else float(r[k])

# ---------- pair model: forms copied in meaning from UX6, on an isolated pair. Gas at origin, stars at x = s
def law(g, a): return 0.5*g + np.sqrt(0.25*g*g + a*g)
def fld(X, Y, Z, c):
    M, a, xc = c; dx = X - xc; f = -G*M*MSUN/((dx*dx + Y*Y + Z*Z + a*a)**1.5*KPC**3)*KPC
    return f*dx, f*Y, f*Z
def enc_table(M, a, d):
    r = np.geomspace(0.5, 3e5, 1500); nod, wt = np.polynomial.legendre.leggauss(64)
    s2 = r[:, None]**2 + d*d - 2*r[:, None]*d*nod[None, :]; rho = 3*M/(4*math.pi*a**3)*(1 + s2/a**2)**-2.5
    sh = 4*math.pi*r*r*(0.5*(rho*wt[None, :]).sum(1)); lg = np.log(r)
    t = np.r_[0.0, np.cumsum(0.5*(sh[1:]*r[1:] + sh[:-1]*r[:-1])*np.diff(lg))] + M*(r[0]/a)**3/(1 + (r[0]/a)**2)**1.5*(d == 0)
    return r, np.maximum(t, 0.0)
def extra(form, k, a0, gas, star, s, C, tabs, reg=True):
    gv, st = C["g"], C["st"]; gb = [gv[i] + st[i] for i in range(3)]
    if reg: gb[1] = gb[1] + a0/1000.0
    g = np.sqrt(gb[0]**2 + gb[1]**2 + gb[2]**2); L = law(g, a0); m = L/np.maximum(g, 1e-300)
    if form == "L1":
        h = k*np.sqrt(gv[0]**2 + gv[1]**2 + gv[2]**2)/a0; return tuple(gb[i]*(m*(1 + h) - 1) for i in range(3))
    out = [gb[i]*(m - 1) for i in range(3)]
    if form == "LAW": return tuple(out)
    if form == "L2":
        sg = -1.0 if MUT else 1.0; return tuple(out[i] + sg*k*(L/a0)*gv[i] for i in range(3))
    lr, tg, tb = tabs[form]; dx = C["X"] - s; dy = C["Y"]; dz = C["Z"]; rr = np.maximum(np.sqrt(dx*dx + dy*dy + dz*dz), 0.5); q = np.log(rr)
    f = -law(np.interp(q, lr, tb), a0)*k*np.interp(q, lr, tg)/a0/rr
    return (out[0] + f*dx, out[1] + f*dy, out[2] + f*dz)
def tables(gas, star, s):
    t = {}
    for key, d in (("N1", s), ("N2", 0.0)):
        r, mg = enc_table(gas[0], gas[1], d); _, ms = enc_table(star[0], star[1], 0.0); f = G*MSUN/(r*KPC)**2
        t[key] = (np.log(r), f*mg, f*(mg + ms))
    return t
def sig_pl(D, M, a): return M*a*a/(math.pi*(D*D + a*a)**2)
ZM = np.concatenate([np.linspace(0.0, 1200.0, 61), np.geomspace(1200.0, 6000.0, 41)[1:]])
def run_pair(gas, star, s, specs, h=2.0, step=20.0):
    """specs: name -> (form, k, a0). Returns name -> (peak x, peak y, delta, dkappa, local max)"""
    w = max(0.5*s + 300.0, 500.0); xs = np.arange(0.5*s - w, 0.5*s + w + 1e-9, step); ys = np.arange(-400.0, 400.0 + 1e-9, step)
    XX, YY = np.meshgrid(xs, ys, indexing="ij"); tabs = tables(gas, star, s); res = {}
    S = {n: np.zeros_like(XX) for n in specs}
    for j0 in range(0, len(ys), 8):
        yy = ys[j0:j0 + 8]; X, Y, Z = np.meshgrid(xs, yy, ZM, indexing="ij"); div = {n: 0.0 for n in specs}
        for ax, (dx, dy, dz) in enumerate(((h, 0, 0), (0, h, 0), (0, 0, h))):
            for sgn in (1.0, -1.0):
                Xa, Ya, Za = X + sgn*dx, Y + sgn*dy, Z + sgn*dz
                C = dict(X=Xa, Y=Ya, Z=Za, g=fld(Xa, Ya, Za, (gas[0], gas[1], 0.0)), st=fld(Xa, Ya, Za, (star[0], star[1], s)))
                for n, (form, k, a0) in specs.items(): div[n] = div[n] + sgn*extra(form, k, a0, gas, star, s, C, tabs)[ax]
        for n in specs: S[n][:, j0:j0 + 8] = 2.0*np.trapz(-div[n]/(2*h)/(4*math.pi*G)*KPC**2/MSUN, ZM, axis=2)
    base = sig_pl(np.hypot(XX, YY), gas[0], gas[1]) + sig_pl(np.hypot(XX - s, YY), star[0], star[1])
    dq = np.hypot(XX, YY) <= 100.0; dg = np.hypot(XX - s, YY) <= 100.0
    for n in specs:
        T = S[n] + base; i, j = np.unravel_index(int(np.argmax(T)), T.shape); px, py = xs[i], ys[j]
        res[n] = dict(peak=[float(px), float(py)], delta=float(np.hypot(px, py)/s), dkappa=float((T[dg].mean() - T[dq].mean())/SIG_CRIT))
    return res, (XX, YY, S, base, dq, dg)

say("=" * 90); say("MG1_merger_sample" + ("  [MUTATE]" if MUT else "")); say("=" * 90); say(f"k fit {KFIT}; pi^2 {PI2:.4f}. Table numbers PROVISIONAL.")
# K3 label controls
ctl = [(10, 50, 300, 50, "GAL"), (300, 50, 10, 50, "GAS"), (150, 50, 150, 50, "BETWEEN"), (20, 50, 20, 50, "UNRESOLVED")]
got = [label(*(c[2:4] + c[:2]) if MUT else c[:4])[0] for c in ctl]
check("K3", got == [c[4] for c in ctl], f"label controls {got}")
# K2 concentric reduction, regulator off
a = A0F["canonical"]; k = 10.0; gas = (1e14, 400.0); star = (1e13, 100.0); rt = np.array([20.0, 100.0, 300.0, 1000.0, 3000.0]); z0 = np.zeros(5)
C = dict(X=rt, Y=z0, Z=z0, g=fld(rt, z0, z0, (gas[0], gas[1], 0.0)), st=fld(rt, z0, z0, (star[0], star[1], 0.0))); tb = tables(gas, star, 0.0)
gg = np.abs(C["g"][0]); gb = gg + np.abs(C["st"][0]); want = law(gb, a)*(1 + k*gg/a); dev = {}
for f in ("L1", "L2", "N1", "N2"):
    e = extra(f, k, a, gas, star, 0.0, C, tb, reg=False); dev[f] = float(np.max(np.abs((gb + np.abs(e[0]))/want - 1)))
check("K2", max(dev.values()) <= 1e-3, f"concentric vs law x (1 + k g_gas/a0), max rel dev {dev}")
# K4
bad = [r["system"] for r in rows if not r["ref"].strip()]
check("K4", not bad, f"every row has a reference; rows {len(rows)}; all tagged PROVISIONAL in this output")
# model rows
FORMS = ("LAW", "L1", "L2", "N1", "N2"); MODEL = {}
def specs_for(foot, keys=("fit", "pi2")):
    d = {}
    for f in FORMS:
        for kl in keys:
            if f == "LAW" and kl != keys[0]: continue
            d[f"{f}|{foot}|{kl}"] = (f, 0.0 if f == "LAW" else (KFIT[foot] if kl == "fit" else PI2), A0F[foot])
    return d
ALL = {}
for f in FEET: ALL.update(specs_for(f))
HALF = {}
for f in FEET: HALF.update({n: v for n, v in specs_for(f, keys=("fit",)).items() if not n.startswith("LAW")})
K6 = {}
for i, r in enumerate(rows):
    tag = f"{r['system']} {r['sub']}"; g0 = (r["M_gas"], r["a_gas"]); st = (r["M_star"], r["a_star"]); s = r["s"]
    res, ctx = run_pair(g0, st, s, ALL if not MUT else {n: v for n, v in ALL.items() if n.startswith("LAW")})
    if not MUT:
        for fac in (0.5, 2.0):
            r2, _ = run_pair((fac*g0[0], g0[1]), st, s, HALF)
            for n, v in r2.items(): res[f"{n}|gas{fac}"] = v
    MODEL[tag] = res
    if i == 0:
        XX, YY, S, base, dq, dg = ctx; n = "LAW|canonical|fit"; T = S[n] + base; a_ = 150.0; M = 3e14
        for lab, cen in (("on_gal", s), ("on_gas", 0.0)):
            if MUT and lab == "on_gal": cen = 0.0
            Tc = T + sig_pl(np.hypot(XX - cen, YY), M, a_); K6[lab] = float((Tc[dg].mean() - Tc[dq].mean())/SIG_CRIT)
check("K6", K6["on_gal"] > 0 and K6["on_gas"] < 0, f"Bullet main: mass on galaxies dkappa {K6['on_gal']:+.3f}, same on gas {K6['on_gas']:+.3f}")
if not MUT:
    bm = [MODEL[f"Bullet {x}"] for x in ("main", "sub")]; ok = all(m[f"L1|{f}|fit"]["dkappa"] < 0 and m[f"N2|{f}|fit"]["dkappa"] > 0 for m in bm for f in FEET)
    check("K1", ok, "Bullet pair control sign, L1 < 0, N2 > 0, k fit both footings; " + str({f"{x} {f}": (round(MODEL[f'Bullet {x}'][f'L1|{f}|fit']['dkappa'], 3), round(MODEL[f'Bullet {x}'][f'N2|{f}|fit']['dkappa'], 3)) for x in ("main", "sub") for f in FEET}) + "; UX6 full model L1 -0.212 -1.158, N2 +0.069 +0.422")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9
check("K5", rss < 4.0, "RSS under 4 GB")
print(f"RSS {rss:.2f} GB", file=sys.stderr)

if MUT:
    need = ("K2", "K3", "K6")
    say("MUTATE required failures: " + ", ".join(f"{k} {'FAILED' if not CHECKS[k] else 'passed (BAD)'}" for k in need))
    json.dump(dict(checks=CHECKS), open(os.path.join(HERE, "mg1_results_MUTATE.json"), "w"), indent=1); OUT.close(); sys.exit(1)

# ---------- observed labels
say("\n=== observed rows, PROVISIONAL. d in kpc, Z = d/sigma ===")
say("row | d_gal +- | d_gas +- | s | Z_gal Z_gas | label | at 1 sigma | assumed x2 | sym errors | s/sig row | s/own sig | flags")
OBS = {}
for r in rows:
    t = f"{r['system']} {r['sub']}"; dg, eg, dq, eq = r["d_lens_gal"], r["e_lens_gal"], r["d_lens_gas"], r["e_lens_gas"]
    L, zg, zq = label(dg, eg, dq, eq); L1 = label(dg, eg, dq, eq, th=1.0)[0]
    eg2 = eg*2 if r["gal_err_kind"] == "ASSUMED" else eg; eq2 = eq*2 if r["gas_err_kind"] == "ASSUMED" else eq; Lx2 = label(dg, eg2, dq, eq2)[0]
    sg = float(r["alt_sym_e_gal"]) if r["alt_sym_e_gal"] else eg; sq = float(r["alt_sym_e_gas"]) if r["alt_sym_e_gas"] else eq; Ls = label(dg, sg, dq, sq)[0]
    Lb = label(float(r["alt_d_lens_gal"]), float(r["alt_e_lens_gal"]), dq, eq)[0] if r["alt_d_lens_gal"] else None
    OBS[t] = dict(system=r["system"], counted=r["counted"] == "yes", label=L, label_1s=L1, label_assumedx2=Lx2, label_sym=Ls, label_bcg=Lb, Z_gal=zg, Z_gas=zq, s=r["s"], s_over_row=r["s"]/eq, s_over_own=r["s"]/r["e_s"], assumed=(r["gal_err_kind"] == "ASSUMED" or r["gas_err_kind"] == "ASSUMED"))
    say(f"{t:18s} {dg:6.0f} {eg:4.0f} | {dq:5.0f} {eq:4.0f} | {r['s']:5.0f} | {zg:5.2f} {zq:5.2f} | {L:10s} | {L1:10s} | {Lx2:10s} | {Ls:10s} | {r['s']/eq:5.2f} | {r['s']/r['e_s']:6.1f} | BCG alt {Lb} | {r['flags']}")
def tally(pred, key="label"):
    t = {}
    for n, o in OBS.items():
        if pred(n, o): t[o[key]] = t.get(o[key], 0) + 1
    return t
say("\n=== counts, by subcluster ===")
C_lit = lambda n, o: o["counted"] and o["s_over_row"] > 2
C_own = lambda n, o: o["counted"] and o["s_over_own"] > 2
C_all = lambda n, o: o["counted"]
C_pub = lambda n, o: o["counted"] and o["s_over_row"] > 2 and not o["assumed"]
C_in = lambda n, o: o["s_over_row"] > 2
TAL = dict(all_counted=tally(C_all), resolved_literal_PRIMARY=tally(C_lit), resolved_own_sigma=tally(C_own), resolved_published_errors_only=tally(C_pub), resolved_with_bullet=tally(C_in), primary_at_1sigma=tally(C_lit, "label_1s"), primary_assumed_x2=tally(C_lit, "label_assumedx2"), primary_sym=tally(C_lit, "label_sym"), own_sigma_at_1sigma=tally(C_own, "label_1s"))
for k, v in TAL.items(): say(f"  {k}: {v}, of {sum(v.values())}")
sysres = {}
for n, o in OBS.items():
    if C_lit(n, o): sysres.setdefault(o["system"], []).append(o["label"])
say("  systems, primary:", sysres)
def verdict_n2(t):
    N = sum(t.values()); g = t.get("GAL", 0)
    if N == 0: return "NONE"
    if g/N < 2/3: return "SIGN FAILS"
    return "SIGN HOLDS" if t.get("GAS", 0) == 0 else "SIGN HOLDS WITH EXCEPTIONS"
say("\n=== model, position and sign. PROVISIONAL inputs; isolated pair; no mass grade ===")
say("row | form: dkappa (delta) at k fit canonical, alt | pi^2 canonical, alt | gas x0.5, x2 canonical dkappa")
for t in MODEL:
    m = MODEL[t]
    for f in FORMS:
        if f == "LAW": say(f"{t:18s} LAW {m['LAW|canonical|fit']['dkappa']:+.3f} ({m['LAW|canonical|fit']['delta']:.2f}) {m['LAW|alt|fit']['dkappa']:+.3f} ({m['LAW|alt|fit']['delta']:.2f})"); continue
        a_, b_, c_, d_ = (m[f"{f}|{x}"] for x in ("canonical|fit", "alt|fit", "canonical|pi2", "alt|pi2"))
        say(f"{t:18s} {f}  {a_['dkappa']:+.3f} ({a_['delta']:.2f}) {b_['dkappa']:+.3f} ({b_['delta']:.2f}) | {c_['dkappa']:+.3f} ({c_['delta']:.2f}) {d_['dkappa']:+.3f} ({d_['delta']:.2f}) | {m[f'{f}|canonical|fit|gas0.5']['dkappa']:+.3f} {m[f'{f}|canonical|fit|gas2.0']['dkappa']:+.3f}")
say("\n=== verdicts ===")
VER = {}
for foot in FEET:
    for f in ("L1", "L2", "N1"):
        for kl in ("fit", "pi2"):
            hit = {n: MODEL[n][f"{f}|{foot}|{kl}"]["dkappa"] for n, o in OBS.items() if C_lit(n, o)}
            bad = [n for n, d in hit.items() if OBS[n]["label"] == "GAL" and d <= 0]; ss = {OBS[n]["system"] for n in bad}; N = len(hit)
            v = "INSUFFICIENT" if len({OBS[n]["system"] for n in hit}) < 3 else ("DEAD IN GENERAL" if len(ss) >= 3 and len(bad)/N >= 2/3 else "NOT GENERALISED")
            VER[f"{f}|{foot}|{kl}"] = dict(verdict=v, n_gal_wrong=len(bad), n=N, systems=sorted(ss)); say(f"  {f} {foot} {kl}: {v}; GAL with model dkappa <= 0: {len(bad)} of {N} in {len(ss)} systems; model dkappa > 0 on {[n for n, d in hit.items() if d > 0]}")
    hitn = {n: MODEL[n][f"N2|{foot}|fit"] for n, o in OBS.items() if C_lit(n, o)}
    say(f"  N2 model sign {foot}, k fit: dkappa > 0 at {sum(v['dkappa'] > 0 for v in hitn.values())} of {len(hitn)}; delta > 0.5 at {sum(v['delta'] > 0.5 for v in hitn.values())}; negative at {[n for n, v in hitn.items() if v['dkappa'] <= 0]}")
    VER[f"N2_model_pos|{foot}"] = dict(dk_pos=sum(v['dkappa'] > 0 for v in hitn.values()), delta_gt=sum(v['delta'] > 0.5 for v in hitn.values()), n=len(hitn))
for lab, c in (("primary", C_lit), ("own sigma", C_own), ("published errors only", C_pub), ("assumed x2", None)):
    t = tally(C_lit, "label_assumedx2") if c is None else tally(c)
    v = verdict_n2(t); VER[f"N2 carried|{lab}"] = dict(verdict=v, tally=t); say(f"  N2 carried memory, {lab}: {v} {t}")
need = ("K1", "K2", "K3", "K6")
json.dump(dict(checks=CHECKS, obs=OBS, tallies=TAL, verdicts=VER, model=MODEL, k6=K6), open(os.path.join(HERE, "mg1_results.json"), "w"), indent=1, default=float, sort_keys=True)
say(f"\nVerdict allowed: {all(CHECKS.get(k, False) for k in need)}; failed checks: {[k for k, v in CHECKS.items() if not v]}"); OUT.close()
