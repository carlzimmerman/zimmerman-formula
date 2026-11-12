#!/usr/bin/env python3
"""
RCF1 -- refit the Milky Way rotation curves (Ou 2024, Eilers 2019) under the framework with the stellar
mass as the free quantity; cold gas and hot gas fixed; e_N free in [0, 0.03]; both footings.
Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt).   Usage: python3 rcf1.py
Writes rcf1.out, rcf1_results.json, rcf1_mut.out next to this file.
Functions copied from hunt_2026/h34_h35_h38_milky_way.py (item 35) and closure_2026_11_12/MWI1_inner_baryons/mwi1.py.
Published masses are MWI1's look-ups and are PROVISIONAL. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math
import numpy as np
from scipy.special import j0 as J0, j1 as J1, i0, i1, k0, k1
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "real_research", "data")
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
def nu(y):
    y = np.maximum(np.asarray(y, dtype=float), 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

OUT = open(os.path.join(HERE, "rcf1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 110); say(t); say("=" * 110)
FAIL = []
def ka(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         ({detail})")
    if not ok: FAIL.append(name)

# ------------------------------------------------------------------ data and item 35's error treatments
def load_tsv(fname):
    lines = [l.rstrip("\n") for l in open(os.path.join(DATA, fname)) if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t"); d = np.array([[float(x) for x in l.split("\t")] for l in lines[1:]])
    return {h: d[:, i] for i, h in enumerate(hdr)}
CURVES = {}
d = load_tsv("mw_rc_ou2024_table1.tsv")
CURVES["Ou2024"] = (d["R_kpc"], d["vc_kms"] * 1e3, 0.5 * (d["sig_plus"] + d["sig_minus"]) * 1e3, np.where(d["R_kpc"] < 22, 0.04, 0.15))
d = load_tsv("mw_rc_eilers2019_table1.tsv")
CURVES["Eilers2019"] = (d["R_kpc"], d["vc_kms"] * 1e3, 0.5 * (d["sig_plus"] + d["sig_minus"]) * 1e3, np.full(len(d["R_kpc"]), 0.035))
def errs(c, kind):
    R, v, st, f = CURVES[c]; return st if kind == "stat" else np.sqrt(st ** 2 + (f * v) ** 2)

# ------------------------------------------------------------------ item 35's Ou census, ported verbatim (z = 0 forces)
OU = dict(disc=dict(M=3.65e10 * MSUN, Rd=2.35 * KPC, zd=0.14 * KPC), HI=dict(M=8.20e9 * MSUN, Rd=18.24 * KPC, zd=0.52 * KPC),
          H2=dict(M=1.30e9 * MSUN, Rd=2.57 * KPC, zd=0.08 * KPC), dustc=dict(M=7.00e7 * MSUN, Rd=5.00 * KPC, zd=0.10 * KPC),
          dustw=dict(M=2.20e5 * MSUN, Rd=3.30 * KPC, zd=0.09 * KPC))
OU_BULGE_M, OU_BULGE_A = 1.55e10 * MSUN, 0.70 * KPC
KMAX35 = 100.0 / KPC
KG35 = np.linspace(1e-6 * KMAX35, KMAX35, 60000)
KC35 = np.geomspace(1e-5 / KPC, KMAX35, 700)
def sig35(c, R):
    R = np.maximum(np.asarray(R, float), 1e-4 * KPC); return c["S0"] * np.exp(-R / c["Rd"])
def zeta35(c, n=3001):
    zd = c["zd"]; zg = np.linspace(-18 * zd, 18 * zd, n); z = np.exp(-np.abs(zg) / zd) / (2 * zd); return zg, z / TRAPZ(z, zg)
def gR35_grid(c, NG):
    Rg = np.geomspace(1e-4 * KPC, 400 * KPC, 5000); Sg = sig35(c, Rg)
    S = np.interp(KG35, KC35, TRAPZ(Sg[None, :] * J0(KC35[:, None] * Rg[None, :]) * Rg[None, :], Rg, axis=1))
    zg, zz = zeta35(c); V = np.interp(KG35, KC35, TRAPZ(zz[None, :] * np.exp(-KC35[:, None] * np.abs(zg)[None, :]), zg, axis=1))
    out = np.empty(len(NG))
    for i0_, r in enumerate(NG):                       # row by row (same numbers, less memory than item 35's matrix)
        out[i0_] = 2 * math.pi * G * TRAPZ(KG35 * J1(KG35 * r) * S * V, KG35)
    return out
NG35 = np.geomspace(0.5 * KPC, 300 * KPC, 420)
RG35 = np.geomspace(3 * KPC, 60 * KPC, 300)
OUG = {}
for k, v in OU.items():
    c = dict(S0=v["M"] / (2 * math.pi * v["Rd"] ** 2), Rd=v["Rd"], zd=v["zd"])
    OUG[k] = np.interp(RG35, NG35, gR35_grid(c, NG35))          # item 35: DiscField grid, then RG grid
OUG["bulge"] = G * OU_BULGE_M * RG35 ** 2 / (RG35 + OU_BULGE_A) ** 2 / RG35 ** 2
OU_MB = (sum(v["M"] for v in OU.values()) + OU_BULGE_M) / MSUN / 1e10
def g_ou(R_kpc, comps):
    return sum(np.interp(R_kpc * KPC, RG35, OUG[k]) for k in comps)

# ------------------------------------------------------------------ McMillan 2017 census, as ported in MWI1
MC = dict(thin=dict(S0=896.0 * MSUN_PC2, Rd=2.50 * KPC, zd=0.300 * KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0 * MSUN_PC2, Rd=3.02 * KPC, zd=0.900 * KPC, Rm=0.0, vert="exp"),
          HI=dict(Sfid=10.0 * MSUN_PC2, Rfid=8.33 * KPC, Rd=7.00 * KPC, zd=0.085 * KPC, Rm=4.0 * KPC, vert="sech2"),
          H2=dict(Sfid=2.0 * MSUN_PC2, Rfid=8.33 * KPC, Rd=1.50 * KPC, zd=0.045 * KPC, Rm=12.0 * KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c): return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC); return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def disc_mass(c):
    Rg = np.geomspace(1e-5 * KPC, 600 * KPC, 20000); return float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg), Rg))
def zprofile(c, n=1201):
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp" else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    return zg, zz
KMAX = 100.0 / KPC
KGRID = np.linspace(1e-6 * KMAX, KMAX, 30000)
KCO = np.geomspace(1e-5 / KPC, KMAX, 600)
def SV_of(c):
    Rg = np.geomspace(1e-4 * KPC, 400 * KPC, 5000); Sg = sigma_of_R(c, Rg)
    S = np.interp(KGRID, KCO, TRAPZ(Sg[None, :] * J0(KCO[:, None] * Rg[None, :]) * Rg[None, :], Rg, axis=1))
    zg, zz = zprofile(c)
    V = np.interp(KGRID, KCO, TRAPZ(zz[None, :] * np.exp(-KCO[:, None] * np.abs(zg)[None, :]), zg, axis=1))
    return S * V
SV = {k: SV_of(c) for k, c in MC.items()}
def g_disc(R_kpc, sv):
    R = np.atleast_1d(R_kpc) * KPC
    return np.array([2 * math.pi * G * TRAPZ(KGRID * J1(KGRID * r) * sv, KGRID) for r in R])
def g_bulge(R_kpc):
    R = np.atleast_1d(R_kpc) * KPC; return G * MBULGE / (R + ABULGE) ** 2
MASS = {k: disc_mass(c) / MSUN / 1e10 for k, c in MC.items()}
STARS = MASS["thin"] + MASS["thick"] + MBULGE / MSUN / 1e10; COLD = MASS["HI"] + MASS["H2"]

# ------------------------------------------------------------------ hot gas (MWG1's MB15)
def m_hot(r_kpc, fac=1.0): return fac * 4.3e10 * (np.asarray(r_kpc, float) / 250.0) ** 1.5
def g_hot(R_kpc, fac=1.0): return G * m_hot(R_kpc, fac) * MSUN / (np.asarray(R_kpc, float) * KPC) ** 2

# ------------------------------------------------------------------ the fit
S_GRID = np.round(np.arange(0.5, 2.5 + 1e-9, 0.0005), 6)
E_GRID = np.round(np.arange(0.0, 0.03 + 1e-9, 0.0002), 6)
def chi2_surface(R_kpc, v, sig, gs, gf, a0, sgrid=S_GRID, egrid=E_GRID, kernel=True):
    R = R_kpc * KPC; gN = sgrid[:, None] * gs[None, :] + gf[None, :]
    out = np.empty((len(sgrid), len(egrid)))
    for j, e in enumerate(egrid):
        vm = np.sqrt((nu((gN + e * a0) / a0) if kernel else 1.0) * gN * R[None, :])
        out[:, j] = np.sum(((vm - v[None, :]) / sig[None, :]) ** 2, axis=1)
    return out
def summarize(chi2, sgrid=S_GRID, egrid=E_GRID, mstar=None):
    i, j = np.unravel_index(np.argmin(chi2), chi2.shape); cmin = chi2[i, j]
    ps = chi2.min(axis=1); ok = ps <= cmin + 1.0; slo, shi = sgrid[ok].min(), sgrid[ok].max()
    pe = chi2.min(axis=0); eok = egrid[pe <= cmin + 1.0]; ehi = eok.max()
    edge = (slo <= sgrid[0] + 1e-9) or (shi >= sgrid[-1] - 1e-9) or (sgrid[i] in (sgrid[0], sgrid[-1]))
    r = dict(s=float(sgrid[i]), slo=float(slo), shi=float(shi), e=float(egrid[j]), ehi=float(ehi),
             ehi_bound=bool(ehi >= egrid[-1] - 1e-9), chi2=float(cmin), s_edge=bool(edge))
    if mstar is not None:
        r.update(M=r["s"] * mstar, Mlo=r["slo"] * mstar, Mhi=r["shi"] * mstar,
                 dlo=(r["s"] - r["slo"]) * mstar, dhi=(r["shi"] - r["s"]) * mstar)
    return r

INV = [("LN15", "Licquia and Newman 2015", 6.08, 1.14), ("McM17", "McMillan 2017", 5.43, 0.57),
       ("C20", "Cautun et al. 2020", 5.04, 0.43), ("I25", "Imig et al. 2025 disc + bulge", 6.18, 0.21),
       ("L25", "Lian et al. 2025", 2.607, 0.363)]
MWI1_CLS = {"canonical": dict(LN15="SUPPLIED", McM17="NOT SUPPLIED", C20="NOT SUPPLIED", I25="NOT SUPPLIED", L25="NOT SUPPLIED"),
            "alt": dict(LN15="SUPPLIED", McM17="WITHIN 2 SIGMA", C20="NOT SUPPLIED", I25="SUPPLIED", L25="NOT SUPPLIED")}
MWI1_NEED = {"canonical": (7.05, 7.41), "alt": (6.36, 6.73)}
def cls(z): return "SUPPLIED" if z <= 1 else ("WITHIN 2 SIGMA" if z <= 2 else "NOT SUPPLIED")

sec("RCF1  Milky Way rotation curves refitted with the stellar mass free (criteria: FROZEN_CRITERIA.md, sha256 in FREEZE_STAMP.txt)")
sec("KNOWN-ANSWER CHECKS")
# KA1: item 35 reproduced
GA35 = np.geomspace(0.5, 6.0, 120); GE35 = np.concatenate([[0.0], np.geomspace(0.002, 5.0, 120)])
OU_ALL = list(OU) + ["bulge"]
ka35 = {}
for c in CURVES:
    R, v, _, _ = CURVES[c]; sig = errs(c, "stat+sys"); g1 = g_ou(R, OU_ALL)
    for f, a0 in A0.items():
        ch = chi2_surface(R, v, sig, g1, np.zeros_like(g1), a0, GA35, GE35)
        i, j = np.unravel_index(np.argmin(ch), ch.shape); prof = ch.min(axis=0)
        ka35[(c, f)] = dict(A=float(GA35[i]), Mb=float(GA35[i] * OU_MB), ehi=float(GE35[prof <= prof.min() + 1].max()), chi2N=float(ch[i, j] / len(R)))
ok = abs(OU_MB / 6.16 - 1) <= 0.005
ok &= abs(ka35[("Ou2024", "canonical")]["Mb"] - 8.75) <= 0.10 and abs(ka35[("Eilers2019", "canonical")]["Mb"] - 8.39) <= 0.10
ok &= abs(ka35[("Ou2024", "alt")]["A"] - 1.31) <= 0.02 and abs(ka35[("Eilers2019", "alt")]["A"] - 1.25) <= 0.02
for (c, f), t in ((("Ou2024", "canonical"), 0.008), (("Eilers2019", "canonical"), 0.006), (("Ou2024", "alt"), 0.015), (("Eilers2019", "alt"), 0.008)):
    ok &= abs(ka35[(c, f)]["ehi"] - t) <= 0.002
ka("KA1 item 35 reproduced on Ou's census (6.16e10), all baryons scaled, no hot gas, its own grids, stat+sys",
   ok, f"Ou census total {OU_MB:.4f}e10; " + "; ".join(f"{c} {f}: A {r['A']:.3f}, M_b {r['Mb']:.3f}e10, e_N <= {r['ehi']:.4f}, chi2/N {r['chi2N']:.2f}" for (c, f), r in ka35.items()))
# KA2: McMillan census and MWI1 force ratios
MBTOT = (STARS + COLD) * 1e10 * MSUN
gtot = lambda R: sum(g_disc(R, SV[k]) for k in MC) + g_bulge(R)
fr = {R: float(gtot(R)[0] * (R * KPC) ** 2 / (G * MBTOT)) for R in (20.0, 25.0, 30.0)}
ka("KA2 McMillan census (stars 5.490, cold gas 1.191, within 0.2 per cent) and MWI1's force ratios (1.0599, 1.0614, 1.0586 within 0.003)",
   abs(STARS / 5.490 - 1) <= 2e-3 and abs(COLD / 1.191 - 1) <= 2e-3 and all(abs(fr[R] - t) <= 0.003 for R, t in ((20.0, 1.0599), (25.0, 1.0614), (30.0, 1.0586))),
   f"stars {STARS:.4f}, cold gas {COLD:.4f}; ratios " + ", ".join(f"{R:.0f} kpc {v:.4f}" for R, v in fr.items()))
# KA3: Freeman razor-thin check, SI
Mt, Rdt = 3.5e10 * MSUN, 2.5 * KPC
ct = dict(S0=Mt / (2 * math.pi * Rdt ** 2), Rd=Rdt, zd=0.01 * KPC, Rm=0.0, vert="exp")
Rt = np.array([4.0, 8.0, 16.0, 24.0]); gnum = g_disc(Rt, SV_of(ct))
y = Rt * KPC / (2 * Rdt); v2 = 4 * math.pi * G * ct["S0"] * Rdt * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)); gan = v2 / (Rt * KPC)
rel = gnum / gan - 1
ka("KA3 razor-thin exponential disc vs Freeman's analytic force, each within 0.5 per cent (SI)",
   bool(np.all(np.abs(rel) <= 5e-3)), ", ".join(f"{R:.0f} kpc {r:+.2e} (v_an {math.sqrt(g*R*KPC)/1e3:.1f} km/s)" for R, r, g in zip(Rt, rel, gan)))
# KA4: hot gas
ka("KA4 MB15 hot gas inside 27 kpc = 0.153e10 within 1 per cent", abs(m_hot(27.0) / 1.53e9 - 1) <= 0.01, f"{m_hot(27.0)/1e10:.4f}e10")
# primary component forces at the data radii
COMP = {}
for c in CURVES:
    R = CURVES[c][0]
    COMP[c] = dict(stars=g_disc(R, SV["thin"]) + g_disc(R, SV["thick"]) + g_bulge(R), cold=g_disc(R, SV["HI"]) + g_disc(R, SV["H2"]), hot=g_hot(R))
# KA5: mock recovery
R, v, _, _ = CURVES["Ou2024"]; sig = errs("Ou2024", "stat+sys"); a0 = A0["canonical"]
gNm = 1.30 * COMP["Ou2024"]["stars"] + COMP["Ou2024"]["cold"] + COMP["Ou2024"]["hot"]
vmock = np.sqrt(nu((gNm + 0.005 * a0) / a0) * gNm * R * KPC)
km = summarize(chi2_surface(R, vmock, sig, COMP["Ou2024"]["stars"], COMP["Ou2024"]["cold"] + COMP["Ou2024"]["hot"], a0))
ka("KA5 noiseless mock at s = 1.30, e_N = 0.005 recovered: s within 0.002, chi2 < 1e-3", abs(km["s"] - 1.30) <= 0.002 and km["chi2"] < 1e-3,
   f"s = {km['s']:.4f}, e_N = {km['e']:.4f}, chi2 = {km['chi2']:.2e}")
if FAIL:
    say("\nSTOPPED: known-answer check failed -> no label.")
    json.dump(dict(lane="RCF1", label="NO LABEL", failed=FAIL, ka1={f"{c}|{f}": r for (c, f), r in ka35.items()}), open(os.path.join(HERE, "rcf1_results.json"), "w"), indent=1)
    sys.exit(0)

# ------------------------------------------------------------------ primary fits
sec("PRIMARY FITS  McMillan census; stars (thin + thick + bulge = %.3fe10) x s; cold gas %.3fe10 fixed; stat+sys errors" % (STARS, COLD))
say("  model: v^2 / R = nu((g_N + e_N a0) / a0) g_N, g_N = s g_stars + g_cold + g_hot; e_N in [0, 0.03]; 68 per cent = profile Delta chi2 <= 1")
FITS = {}
for hot in ("MB15", "none"):
    for c in CURVES:
        R, v, _, _ = CURVES[c]; sig = errs(c, "stat+sys"); gf = COMP[c]["cold"] + (COMP[c]["hot"] if hot == "MB15" else 0.0)
        for f, a0 in A0.items():
            r = summarize(chi2_surface(R, v, sig, COMP[c]["stars"], gf, a0), mstar=STARS); r["chi2N"] = r["chi2"] / len(R); r["N"] = len(R)
            FITS[(hot, c, f)] = r
            say(f"  hot {hot:4s} {c:10s} {f:9s}  M* = {r['M']:.3f} [{r['Mlo']:.3f}, {r['Mhi']:.3f}] e10  (-{r['dlo']:.3f} / +{r['dhi']:.3f}),"
                f"  s = {r['s']:.4f},  e_N best {r['e']:.4f}, upper {'>= 0.03 (bound)' if r['ehi_bound'] else format(r['ehi'], '.4f')},"
                f"  chi2/N = {r['chi2N']:.3f} (N = {r['N']}){'  S GRID EDGE' if r['s_edge'] else ''}")

# ------------------------------------------------------------------ mutations
MUT = open(os.path.join(HERE, "rcf1_mut.out"), "w")
MUT.write("RCF1 mutations (criteria FROZEN_CRITERIA.md). M1 must bite on every footing and data set; M2 reported.\n")
bite = True; MUTRES = {}
SG_N = np.round(np.arange(0.5, 8.0 + 1e-9, 0.002), 6)
for c in CURVES:
    R, v, _, _ = CURVES[c]; sig = errs(c, "stat+sys"); gf = COMP[c]["cold"] + COMP[c]["hot"]
    for f, a0 in A0.items():
        p = FITS[("MB15", c, f)]
        m1 = summarize(chi2_surface(R, v, sig, COMP[c]["stars"], gf, a0, SG_N, np.array([0.0]), kernel=False), SG_N, np.array([0.0]), STARS)
        m1["chi2N"] = m1["chi2"] / len(R)
        b = (m1["M"] - p["M"] > 3 * p["dhi"]) or (m1["chi2N"] >= 2 * p["chi2N"]); bite &= b
        m2 = summarize(chi2_surface(R, v, sig, COMP[c]["stars"], COMP[c]["cold"] + 10 * COMP[c]["hot"], a0), mstar=STARS)
        MUTRES[f"{c}|{f}"] = dict(M1=m1, M2=m2)
        MUT.write(f"{c} {f}: M1 kernel off: M* {m1['M']:.3f}e10 (primary {p['M']:.3f} +{p['dhi']:.3f}), chi2/N {m1['chi2N']:.3f} (primary {p['chi2N']:.3f})"
                  f"{' S GRID EDGE' if m1['s_edge'] else ''}  [{'bites' if b else 'DOES NOT BITE'}];  M2 hot gas x10: M* {m2['M']:.3f}e10 (falls by {p['M']-m2['M']:.3f})\n")
MUT.close()
sec("MUTATIONS"); say(open(os.path.join(HERE, "rcf1_mut.out")).read().rstrip())
if not bite:
    say("\nSTOPPED: M1 does not bite -> no label."); sys.exit(0)

# ------------------------------------------------------------------ grading
sec("GRADING  z = (M* best - published) / sqrt(published upward error^2 + fit lower error^2)")
GRADE = {}
for hot in ("MB15", "none"):
    for c in CURVES:
        for f in A0:
            r = FITS[(hot, c, f)]; rows = []; sup = []
            for i, name, m, e in INV:
                z = (r["M"] - m) / math.hypot(e, r["dlo"]); k = cls(z); rows.append(dict(id=i, mass=m, err=e, z=z, cls=k, ratio=r["M"] / m))
                if k == "SUPPLIED": sup.append(i)
            lab = f"SUPPLIED BY {len(sup)} OF 5" + (f" ({', '.join(sup)})" if sup else "") + f"; AT McM17 {[x['cls'] for x in rows if x['id'] == 'McM17'][0]}"
            lo, hi = MWI1_NEED[f]
            mv = "HOLDS" if lo - 0.20 <= r["M"] <= hi + 0.20 else ("MOVES UP" if r["M"] > hi + 0.20 else "MOVES DOWN")
            nch = sum(x["cls"] != MWI1_CLS[f][x["id"]] for x in rows)
            GRADE[(hot, c, f)] = dict(label=lab, rows=rows, need=mv, changed=nch, changed_ids=[x["id"] for x in rows if x["cls"] != MWI1_CLS[f][x["id"]]])
            say(f"\n  hot {hot}, {c}, {f}: M* = {r['M']:.3f} -{r['dlo']:.3f} / +{r['dhi']:.3f} e10")
            for x in rows:
                say(f"     {x['id']:6s} {x['mass']:6.3f} + {x['err']:5.3f}   z = {x['z']:+6.2f}   M*/published {x['ratio']:4.2f}   {x['cls']}"
                    f"{'' if x['cls'] == MWI1_CLS[f][x['id']] else '   (MWI1: ' + MWI1_CLS[f][x['id']] + ')'}")
            say(f"     LABEL: {lab}")
            if hot == "MB15":
                say(f"     MWI1 need ({lo}-{hi}): {mv}; classes changed vs MWI1: {nch} {GRADE[(hot, c, f)]['changed_ids']} -> {'CLASSES CHANGE' if nch else 'CLASSES UNCHANGED'}")

# ------------------------------------------------------------------ reported, not graded
sec("REPORTED, NOT GRADED")
REP = {}
for c in CURVES:
    R, v, _, _ = CURVES[c]
    for f, a0 in A0.items():
        gf = COMP[c]["cold"] + COMP[c]["hot"]
        st = summarize(chi2_surface(R, v, errs(c, "stat"), COMP[c]["stars"], gf, a0), mstar=STARS); st["chi2N"] = st["chi2"] / len(R)
        m = R >= 12.0
        o12 = summarize(chi2_surface(R[m], v[m], errs(c, "stat+sys")[m], COMP[c]["stars"][m], gf[m], a0), mstar=STARS); o12["chi2N"] = o12["chi2"] / m.sum(); o12["N"] = int(m.sum())
        ous = 3.65 + 1.55
        gs_ou = g_ou(R, ["disc", "bulge"]); gf_ou = g_ou(R, ["HI", "H2", "dustc", "dustw"]) + COMP[c]["hot"]
        ouv = summarize(chi2_surface(R, v, errs(c, "stat+sys"), gs_ou, gf_ou, a0), mstar=ous); ouv["chi2N"] = ouv["chi2"] / len(R)
        REP[f"{c}|{f}"] = dict(stat_only=st, R_ge_12=o12, ou_census=ouv)
        say(f"  {c:10s} {f:9s} stat-only: M* {st['M']:.3f} [{st['Mlo']:.3f}, {st['Mhi']:.3f}], e_N <= {st['ehi']:.4f}, chi2/N {st['chi2N']:.1f}{' S EDGE' if st['s_edge'] else ''}")
        say(f"  {'':10s} {'':9s} R >= 12 kpc ({o12['N']} pts): M* {o12['M']:.3f} [{o12['Mlo']:.3f}, {o12['Mhi']:.3f}], e_N <= {'>= 0.03 (bound)' if o12['ehi_bound'] else format(o12['ehi'], '.4f')}, chi2/N {o12['chi2N']:.3f}{' S EDGE' if o12['s_edge'] else ''}")
        say(f"  {'':10s} {'':9s} Ou census (stars 5.20 x s, Ou gas fixed, MB15): M* {ouv['M']:.3f} [{ouv['Mlo']:.3f}, {ouv['Mhi']:.3f}], e_N <= {ouv['ehi']:.4f}, chi2/N {ouv['chi2N']:.3f}{' S EDGE' if ouv['s_edge'] else ''}")

sec("LABELS (hot gas MB15 headline; no-hot-gas beside it)")
for c in CURVES:
    for f in A0:
        g = GRADE[("MB15", c, f)]; gn = GRADE[("none", c, f)]
        say(f"  {c:10s} {f:9s}: {g['label']}  |  need {g['need']}, {'CLASSES CHANGE' if g['changed'] else 'CLASSES UNCHANGED'} {g['changed_ids']}  |  no hot gas: {gn['label']}")
key = lambda t: "|".join(t)
json.dump(dict(lane="RCF1", date="2026-11-12", stars_census=STARS, cold_gas=COLD,
               ka1={key(k): v for k, v in ka35.items()}, ka2_ratios=fr, ka3_rel=rel.tolist(), ka5=km,
               fits={key(k): v for k, v in FITS.items()}, grades={key(k): v for k, v in GRADE.items()},
               mutations=MUTRES, reported=REP), open(os.path.join(HERE, "rcf1_results.json"), "w"), indent=1, default=float)
say("\nRCF1 COMPLETE. Published masses are PROVISIONAL look-ups (MWI1). kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
