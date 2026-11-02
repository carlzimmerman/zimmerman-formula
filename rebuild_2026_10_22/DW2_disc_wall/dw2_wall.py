#!/usr/bin/env python3
"""DW2 part (a): K checks, A2 U_open grid, stretch, A1 total-error draws, A3 gates x profiles. nice -n 19, one thread. DW2_MUTATE=1: a0 x 1.5, share x 0.5; K1, K2 must fail, exit 1. kappa = 1/2 FITTED; not theory closed."""
import sys, io, contextlib
from dw2_core import *
OUT = []; RES = {}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(n, ok, t): CHK.append((n, bool(ok))); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}")
GAL = load(); BY = [[g for g in GAL if binof(g) == i] for i in range(6)]; ALL = load(True)
FLIST = (0.0, 0.54, 0.753, FQ, 0.946, 1.07); MASS = ("em1", "share"); DRAWS = 300; SEED = 20261102
# ---- K checks
mc1 = json.load(open(os.path.join(RB, "MC1_minimal_cold_requirement", "mc1_results.json")))["footings"]
PAIR = {}
def pair(g, U, mass):
    k = (g["name"], round(U, 3), mass)
    if k not in PAIR: PAIR[k] = cold_pair(g, U, mass)
    return PAIR[k]
for ft in FEET:
    d = 0
    for i, gs in enumerate(BY):
        q = psi_bin([item(g, 0.5, *pair(g, 0.5, "em1"), FQ) for g in gs], A0[ft], "N"); r = mc1[ft]["room"]["U0.5|f0.872|N"][BN[i]]["psi"]; d = max(d, abs(q["psi"] - r))
    check(f"K1 {ft}", d <= 0.002, f"psi N f_Q U 0.5 against MC1, max |diff| {d:.4f}")
def fixedU_rms(gals, a0, pred, U=0.5, clipV=True):
    wr2, ws = 0.0, 0.0
    for g in gals:
        gO = g["V"] ** 2 * KMS2 / g["R"]; gb = gbar(g, U); ok = (gb > 0) & (g["V"] > 0); W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["V"], 1)) ** 2; p = pred(g, np.maximum(gb, 1e-30), a0); r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.) / p), 0.); wr2 += float((W * r * r * ok).sum()); ws += float((W * ok).sum())
    return math.sqrt(wr2 / ws)
L0 = {ft: fixedU_rms(GAL, A0[ft], lambda g, gb, a: law(gb, a)) for ft in FEET}; want = dict(canonical=0.1114, alt=0.1016)
check("K2", max(abs(L0[f] - want[f]) for f in FEET) <= 0.001, f"law weighted fixed-U rms {L0}, MC1 {want}")
rg = np.geomspace(1e19, 1e23, 300); M0_ = Mc_native(1e12, rg); Mz = contract(rg, 0 * rg, M0_, 0.0)[0]; check("K6", np.max(np.abs(Mz / M0_ - 1)[5:-5]) < 1e-3, f"contract zero baryons {np.max(np.abs(Mz / M0_ - 1)[5:-5]):.1e}")
rx = 0.1197 * 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G) * 1091 ** 3; check("K7", abs(rx / 2.92e-18 - 1) < 0.005, f"rho_x(1090) {rx:.4e}")
if MUT:
    RES["checks"] = CHK; json.dump(RES, open(os.path.join(HERE, f"dw2_wall_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True); open(os.path.join(HERE, f"dw2_wall{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if all(c[1] for c in CHK) else 1)
# fast contraction against X39
dmax = 0
for ft in FEET[:1]:
    for i, gs in enumerate(BY):
        q = psi_bin([item(g, 0.5, *pair(g, 0.5, "em1"), FQ) for g in gs], A0[ft], "N"); q2 = psi_bin([item(g, 0.5, *cold_pair(g, 0.5, "em1", fast=True), FQ) for g in gs], A0[ft], "N"); dmax = max(dmax, abs(q["psi"] - q2["psi"]))
P(f"fast contraction (120 pts, 40 iter, draws only) against X39 path, psi max diff {dmax:.4f}")
RES["fast_diff"] = dmax
# ---- A2 U grid
UG = np.round(np.arange(0.05, 0.8001, 0.05), 2); RES["A2"] = {}
P("\n-- A2: psi by bin against U, reading N; U_open = largest U with psi >= 1; U_fill = U where median d at psi 1 crosses 0")
for ft in FEET:
    a0 = A0[ft]; RES["A2"][ft] = {}
    for mass in MASS:
        for f in FLIST:
            for rd in ("N", "S"):
                tab = {}
                for u in UG:
                    tab[float(u)] = [psi_bin([item(g, float(u), *pair(g, float(u), mass), f) for g in gs], a0, rd) for gs in BY]
                Uo = []; Uf = []
                for i in range(6):
                    op = [float(u) for u in UG if tab[float(u)][i]["psi"] >= 1.0]; Uo.append(max(op) if op else 0.0)
                    ds = np.array([tab[float(u)][i]["d1"] for u in UG]); j = [k for k in range(len(UG) - 1) if ds[k] >= 0 > ds[k + 1]]; Uf.append(float(UG[j[-1]] + (UG[j[-1] + 1] - UG[j[-1]]) * ds[j[-1]] / (ds[j[-1]] - ds[j[-1] + 1])) if j else (float(UG[0]) if ds[0] < 0 else float(UG[-1])))
                b5 = sorted(Uo[:5]); U4 = b5[1]
                k = f"{mass}|f{f}|{rd}"; RES["A2"][ft][k] = dict(U_open=Uo, U_open_4of5=U4, U_fill=Uf, psi={str(float(u)): [t["psi"] for t in tab[float(u)]] for u in UG})
                P(f"  {ft:9s} {k:18s} U_open {' '.join(f'{a:.2f}' for a in Uo)} | 4of5 {U4:.2f} | U_fill {' '.join(f'{a:.2f}' for a in Uf)} | psi@.5 {' '.join(f'{t:.2f}' for t in [x['psi'] for x in tab[0.5]])}")
# ---- stretch at U 0.5
P("\n-- A2 stretch s at U 0.5 for psi = 1, bin by bin (UL1 seed range s 0.83-1.28); s capped at 30"); RES["stretch"] = {}
for ft in FEET:
    RES["stretch"][ft] = {}
    for mass in MASS:
        for f in (0.0, FQ):
            row = []
            for gs in BY:
                def ok(s): return psi_bin([item(g, 0.5, *cold_pair(g, 0.5, mass, s=s, fast=True), f) for g in gs], A0[ft], "N", sigma=None)["psi"] >= 1.0
                if ok(1.0): row.append(1.0); continue
                if not ok(30.0): row.append(99.0); continue
                lo, hi = 1.0, 30.0
                for _ in range(8):
                    c = math.sqrt(lo * hi); lo, hi = (lo, c) if ok(c) else (c, hi)
                row.append(hi)
            RES["stretch"][ft][f"{mass}|f{f}"] = row; P(f"  {ft:9s} {mass:6s} f {f:5.3f}  " + " ".join(f"{a:.2f}" for a in row))
# ---- U scenarios
EST = json.load(open(os.path.join(RB, "UL1_measured_upsilon_test", "ul1_est.json")))["primary"]
S576 = os.path.join(REPO, "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); n = {"__file__": os.path.abspath(S576), "__name__": "h"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S576).read().split('P("=" * 100)')[0], "h", "exec"), n)
gal_, terms, K_V, Gn = n["gal"], n["galaxy_terms"], n["K_VERT"], n["G"]
def impl(c, B):
    y = []
    for g in gal_.values():
        Rr = 1.5 * g["hR"]; t = terms(g, Rr); Sg = n["sexp"](Rr, t["Ma"], 2 * t["hR"]) + n["sexp"](Rr, t["Mm"], t["hR"]); y.append(((t["smeas"] * c) ** 2 / (math.pi * Gn * K_V * t["hz"] * B) - Sg) / (t["I0"] * math.exp(-Rr / t["hR"])))
    return float(np.median(y))
def od1(c):
    v = [impl(c, 1.0), impl(c, 1.0) / 1.3, impl(c, 1.1), impl(c, 1.1) / 1.3]; lo, hi = min(v), max(v); return math.sqrt(lo * hi), max(0.5 * math.log10(hi / lo), 0.04)
SCEN = {"S1 flat 0.50": ("flat", 0.5, 0.04)}
for nm, c in (("S4 OD1 c 1.00", 1.0), ("S5 OD1 c 1.24", 1.24), ("S6 OD1 c 1.43", 1.431), ("S7 OD1 c 1.88", 1.88)): m_, e_ = od1(c); SCEN[nm] = ("flat", m_, e_)
for nm, x in (("S2 GSWLC", "GSWLC"), ("S3 Taylor", "Taylor")): SCEN[nm] = ("bin", x, None)
SCEN = dict(sorted(SCEN.items())); RES["scenarios"] = {}
P("\n-- U scenarios")
def U_of(sc, ibin, g, offs):
    kind, a, b = SCEN[sc]
    if kind == "flat": return a * 10 ** offs
    return EST[BN[ibin]][a]["mu"] / g["TOT"] * 10 ** offs
def h_of(sc, ibin):
    kind, a, b = SCEN[sc]
    if kind == "flat": return b
    return math.sqrt((1.25 * EST[BN[ibin]][a]["sig"] / math.sqrt(len(BY[ibin]))) ** 2 + 0.04 ** 2)
for s_ in SCEN:
    kind, a, b = SCEN[s_]; RES["scenarios"][s_] = dict(U=[a] * 6 if kind == "flat" else [EST[x][a]["mu"] for x in BN], h=[h_of(s_, i) for i in range(6)]); P(f"  {s_:14s} U(tot) " + " ".join(f"{u:.3f}" for u in RES["scenarios"][s_]["U"]) + " | h dex " + " ".join(f"{u:.3f}" for u in RES["scenarios"][s_]["h"]))
# ---- A1 draws
def tp(rng, mode, lo, hi, z):  # two-piece normal, lo/hi are z-sigma edges
    x = rng.standard_normal(); return mode + x * ((hi - mode) / z if x > 0 else (mode - lo) / z)
RES["A1"] = {}
P(f"\n-- A1: {DRAWS} draws, R = 1 - psi, median [16, 84], P(R > 0) by bin; reading N primary, S reported")
for ft in FEET:
    RES["A1"][ft] = {}
    for mass in MASS:
        for sc in SCEN:
            rng = np.random.default_rng(SEED); Rn = np.zeros((DRAWS, 6)); Rs = np.zeros((DRAWS, 6)); sig_n = {}; sig_s = {}
            for i, gs in enumerate(BY):  # base sigma at mode
                its = [item(g, U_of(sc, i, g, 0.0), *cold_pair(g, U_of(sc, i, g, 0.0), mass, fast=True), FQ) for g in gs]; sig_n[i] = psi_bin(its, A0[ft], "N")["s"]; sig_s[i] = psi_bin(its, A0[ft], "S")["s"]
            for dr in range(DRAWS):
                f = tp(rng, FQ, 0.54, 1.07, 1.96); a = 11.18 + (0.06 * rng.standard_normal() if mass == "em1" else 0.0); c = tp(rng, 8.0, 6.25, 9.63, 1.0); s = 8.0 / max(c, 1.0); D = 1 + 0.05 * rng.standard_normal(); gs_ = 1 + 0.10 * rng.standard_normal(); offs = [h_of(sc, i) * rng.standard_normal() for i in range(6)]
                for i, gs in enumerate(BY):
                    idx = rng.integers(0, len(gs), len(gs)); its = []
                    for j in idx:
                        g = scaled(gs[j], D, gs_); U = U_of(sc, i, gs[j], offs[i]); its.append(item(g, U, *cold_pair(g, U, mass, s=s, a=a, fast=True), f))
                    Rn[dr, i] = 1 - psi_bin(its, A0[ft], "N", sigma=sig_n[i])["psi"]; Rs[dr, i] = 1 - psi_bin(its, A0[ft], "S", sigma=sig_s[i])["psi"]
            def lab(Rr):
                pp = (Rr > 0).mean(0)[:5]; return "WALL HOLDS" if (pp >= 0.95).sum() >= 4 else "WALL OPENS" if (pp < 0.5).sum() >= 4 else "NOT DECIDED"
            RES["A1"][ft][f"{mass}|{sc}"] = dict(N=dict(med=np.median(Rn, 0).tolist(), lo=np.percentile(Rn, 16, axis=0).tolist(), hi=np.percentile(Rn, 84, axis=0).tolist(), P=(Rn > 0).mean(0).tolist(), label=lab(Rn)), S=dict(med=np.median(Rs, 0).tolist(), P=(Rs > 0).mean(0).tolist(), label=lab(Rs)))
            q = RES["A1"][ft][f"{mass}|{sc}"]; P(f"  {ft:9s} {mass:6s} {sc:14s} N R " + " ".join(f"{a:.2f}[{b:.2f},{c:.2f}]" for a, b, c in zip(q["N"]["med"], q["N"]["lo"], q["N"]["hi"])) + " P " + " ".join(f"{a:.2f}" for a in q["N"]["P"]) + f" {q['N']['label']} | S {q['S']['label']}")
# ---- A3 gates x profiles
P("\n-- A3 gates x profiles at U 0.50/0.70")
hI, obI, omI = 0.674, 0.0493, 6.364 * 0.0493; rmI = omI * 3 * (hI * 1e5 / MPC) ** 2 / (8 * math.pi * G)
def x22(g, U=0.5, f=1.0):
    r = g["R"]; vb2 = gbar(g, U) * r / KMS2; mb = max(vb2[-1], 0) * 1e6 * r[-1] / G; rta = (3 * (omI / obI) * mb / (4 * math.pi * 5.55 * rmI)) ** (1 / 3) if mb > 0 else 1.0
    return G * f * (omI / obI - 1) * mb * np.minimum(r / rta, 1) / r ** 2, rta
def witness(ft):
    return fixedU_rms(ALL, A0[ft], lambda g, gb, a: law(gb + x22(g)[0], a))
wit = {ft: witness(ft) for ft in FEET}; wnt = dict(canonical=0.103471, alt=0.103889); check("K3", max(abs(wit[f] - wnt[f]) for f in FEET) <= 1e-3, f"M6 witness {wit}, record {wnt}")
def prof(g, nm):
    if nm == "X22": return x22(g)[0]
    return pair(g, 0.5, "em1" if nm == "native EM1" else "share")[0]
RES["A3"] = {}
for ft in FEET:
    a0 = A0[ft]; RES["A3"][ft] = {}
    for nm in ("X22", "native share", "native EM1"):
        G_ = np.array([]); 
        ratio = [float(np.median([(prof(g, nm)[outer(g)].mean() * g["R"][-1] ** 2 / G / MS) / max(Mbtot(g, .5), 1) for g in gs])) for gs in BY]
        r_ = {}
        for rd in "NS":
            T2 = [psi_bin([(lambda gO, gb, gc: (gO, gb, gc))(*item(g, .5, prof(g, nm), prof(g, nm), 0.0)) for g in gs], a0, rd)["psi"] for gs in BY]
            fx = lambda psi, sample=GAL: fixedU_rms(sample, a0, (lambda g, gb, a: law(gb, a) + psi * prof(g, nm) if rd == "N" else law(gb + psi * prof(g, nm), a)))
            p1, p175 = fx(1.0), fx(1.0, ALL); pm = [fx(x) for x in (0.5, 2.0, 4.0)]
            r_[rd] = dict(T2=T2, rms_143=p1, rms_175=p175, rms_psi=dict(zip(("0.5", "2", "4"), pm))); P(f"  {ft:9s} {nm:13s} {rd} T2 psi " + " ".join(f"{a:.2f}" for a in T2) + f" | fixed-U rms psi 1 Q<=2 {p1:.4f}, all {p175:.4f}; psi .5,2,4 {pm[0]:.4f} {pm[1]:.4f} {pm[2]:.4f}")
        RES["A3"][ft][nm] = dict(Gamma_Rlast=ratio, **r_); P(f"     M_x(R_last)/M_b by bin " + " ".join(f"{a:.2f}" for a in ratio))
    pw = {}
    for lab, fn in (("law", lambda g, gb, a: law(gb, a)), ("law x 10^-0.1", lambda g, gb, a: law(gb, a) * 10 ** -0.1), ("law x 10^-0.2", lambda g, gb, a: law(gb, a) * 10 ** -0.2), ("law x 10^+0.1", lambda g, gb, a: law(gb, a) * 10 ** 0.1), ("law at U x 2", None)):
        if fn is None: pw[lab] = (fixedU_rms(GAL, a0, lambda g, gb, a: law(gb, a), U=1.0), fixedU_rms(ALL, a0, lambda g, gb, a: law(gb, a), U=1.0))
        else: pw[lab] = (fixedU_rms(GAL, a0, fn), fixedU_rms(ALL, a0, fn))
    RES["A3"][ft]["power"] = pw; P(f"  gate power {ft}: " + "; ".join(f"{k} {v[0]:.4f}/{v[1]:.4f}" for k, v in pw.items()) + " (Q<=2 / all 175); line 0.110")
RES["checks"] = CHK; json.dump(RES, open(os.path.join(HERE, f"dw2_wall_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True); open(os.path.join(HERE, f"dw2_wall{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(c[1] for c in CHK) else 1)
