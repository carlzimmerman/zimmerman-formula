#!/usr/bin/env python3
"""CFG493: combined kappa measurement from independent M/L-insensitive routes (criteria FROZEN_CRITERIA.md, adffc0550).

Routes: P1 SPARC gas-dominated points on ladder distances (CFG449 verdict sample, re-fitted here);
        P2 MeerKAT MIGHTEE-HI rest-frame width chain (CFG309/CFG306 committed numbers) on the single-dish flux scale (CFG304);
        P3 WALLABY DR2 gas points (p43 method re-implemented; kernel nu_mono; Hubble-flow distances at H0 = 67.4).
Shared systematics (gas scale, stellar scale, Hubble-flow distance scale) modelled explicitly; GLS on log10 a0.
kappa = 1/2 is FITTED; kappa is MEASURED here, never derived. Both footings. On-disk data only.
Run: python3 cfg493_kappa_combined.py [--mutate]
"""
import os, sys, io, csv, json, math, contextlib
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import ellipk, i0, i1, k0, k1
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []; CHECKS = []; RES = {"lane": "CFG493", "criteria": "adffc0550", "mutate": MUT}
def P(s=""): print(s); OUT.append(str(s))
def check(name, ok, lb=True):
    CHECKS.append(dict(name=name, ok=bool(ok), load_bearing=lb)); P(f"  [{'PASS' if ok else 'FAIL'}{'' if lb else ', reported'}] {name}")
def jl(path): return json.load(open(os.path.join(REPO, path)))
LN10 = math.log(10)

# ------------------------------------------------------------------ footings (K1)
c = 2.99792458e8; Gn = 6.67430e-11; Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc; OL = 0.685
den_L = c * H0 * math.sqrt(3 * OL / (8 * math.pi))         # c sqrt(G rho_Lambda)
den_c = c * H0 * math.sqrt(3 / (8 * math.pi))              # c sqrt(G rho_crit)
A_HALF_L, A_HALF_C = 9.3603e-11, 1.1312e-10                # the record's footing values
DEN_L, DEN_C = 2 * A_HALF_L, 2 * A_HALF_C
P("CFG493 combined kappa" + ("  [MUTATE RUN]" if MUT else ""))
P("K1 footing identities")
check(f"K1a c sqrt(G rho_Lambda) = {den_L:.5e} vs 2 x 9.3603e-11 (rel {den_L / DEN_L - 1:+.2e}, tol 1e-3)", abs(den_L / DEN_L - 1) < 1e-3)
check(f"K1b kappa_crit/kappa_Lambda = {DEN_L / DEN_C:.5f} vs sqrt(Omega_Lambda) {math.sqrt(OL):.5f} (tol 2e-3; record values rounded)", abs(DEN_L / DEN_C - math.sqrt(OL)) < 2e-3)
check(f"K1c exact: den_L/den_c = {den_L / den_c:.12f} = sqrt(0.685) {math.sqrt(OL):.12f}", abs(den_L / den_c - math.sqrt(OL)) < 1e-12)
a_mil = c * H0 / (2 * math.pi); a_hor = a_mil * math.sqrt(OL)
CAND = {"canonical": [("1/2", 0.5 * DEN_L), ("1/sqrt(pi)", DEN_L / math.sqrt(math.pi)), ("0.6", 0.6 * DEN_L),
                      ("cH0/2pi (Milgrom)", a_mil), ("cH_Lambda/2pi", a_hor)],
        "alt": [("1/2", 0.5 * DEN_C), ("1/sqrt(pi)", DEN_C / math.sqrt(math.pi)), ("0.6", 0.6 * DEN_C), ("cH0/2pi (Milgrom)", a_mil)]}
for f, lst in CAND.items():
    P(f"  {f:9s} candidates: " + "; ".join(f"{n} a0 {a:.4e} (kappa {a / (DEN_L if f == 'canonical' else DEN_C):.4f})" for n, a in lst))
RES["candidates"] = {f: {n: a for n, a in lst} for f, lst in CAND.items()}

# ------------------------------------------------------------------ P1: SPARC gas-dominated points (CFG449 machinery, mask frozen at nominal)
KPC = 3.0857e19
def nu_quad(y): return np.sqrt(1 + 1 / np.asarray(y, float))
def sel_points(g):
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return (vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)
def arrays(gs, U, gscale=1.0):
    out = []
    for g in gs:
        m = sel_points(g); R = g["R"][m] * KPC; vg = g["Vgas"][m]
        b = (gscale * np.sign(vg) * vg ** 2 + U * g["Vdisk"][m] ** 2 + 1.4 * U * g["Vbul"][m] ** 2) * 1e6 / R
        o = (g["Vobs"][m] * 1e3) ** 2 / R
        w = 1 / (np.clip(g["eV"][m], 1, None) / np.clip(g["Vobs"][m], 1, None)) ** 2
        ok = (b > 0) & (o > 0)
        out.append((b[ok], o[ok], w[ok]))
    return out
def fit1(parts, kern=None):
    kern = kern or C.nu_mono
    gb = np.concatenate([p[0] for p in parts]); go = np.concatenate([p[1] for p in parts]); w = np.concatenate([p[2] for p in parts])
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(kern(gb / 10 ** la))) ** 2)
    return minimize_scalar(f, bounds=(-10.8, -9.3), method="bounded", options={"xatol": 1e-5}).x
def boot1(parts, kern=None):
    rng = np.random.default_rng(7)
    return float(np.std([fit1([parts[i] for i in rng.integers(0, len(parts), len(parts))], kern) for _ in range(500)]))
def rescale(g, f):
    h = dict(g); h["R"] = g["R"] * f; s = math.sqrt(f)
    for k in ("Vgas", "Vdisk", "Vbul"): h[k] = g[k] * s
    return h
SP = [dict(name=g["name"], R=np.asarray(g["R"], float), Vobs=np.asarray(g["Vobs"], float), eV=np.asarray(g["eV"], float),
           Vgas=np.asarray(g["Vgas"], float), Vdisk=np.asarray(g["Vdisk"], float), Vbul=np.asarray(g["Vbul"], float), meta=g["meta"])
      for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
SPd = {g["name"]: g for g in SP}
J449 = jl("campaign_fresh_gravity/CFG449_a0_rung_iorio_edd/cfg449_rung_results.json")
names = J449["fits"]["S0+SR"]["names"]; srD = {r[0]: (r[1], r[2]) for r in J449["sr_log"] if r[2] is not None}
P1g = [rescale(SPd[n], srD[n][1] / srD[n][0]) if n in srD else SPd[n] for n in names]
S0g = [SPd[n] for n in J449["fits"]["S0 (CFG397 anchor)"]["names"]]
parts = arrays(P1g, 0.5); L1_nom = float(fit1(parts)); sd1 = boot1(parts)
P("\nP1 SPARC gas-dominated points, ladder distances (CFG449 S0+SR, 12 galaxies)")
check(f"K2a P1 reproduces CFG449: log a0 {L1_nom:+.5f} vs {J449['fits']['S0+SR']['log_a0']:+.5f} (tol 1e-4); boot SD {sd1:.4f} vs {J449['fits']['S0+SR']['sd']:.4f} (tol 2e-3)",
      abs(L1_nom - J449["fits"]["S0+SR"]["log_a0"]) < 1e-4 and abs(sd1 - J449["fits"]["S0+SR"]["sd"]) < 2e-3)
lev1_gas = (fit1(arrays(P1g, 0.5, 1.1)) - L1_nom) / math.log10(1.1)
lev1_star = (fit1(arrays(P1g, 0.7)) - L1_nom) / math.log10(1.4)
lev1_D = (fit1(arrays([rescale(g, 10 ** 0.01) for g in P1g], 0.5)) - L1_nom) / 0.01
TIE1 = -0.052739247391679456                       # CFG306 P6: SPARC M_HI minus ALFALFA, median over 35 (dex)
J306 = jl("campaign_fresh_gravity/CFG306_paper40_referee/cfg306_physics_checks_results.json")["numbers"]
check(f"K2b P1 flux-tie input read from CFG306 P6 = {J306['P6_sparc_alfalfa']['median_dlogMHI_all']:.6f}", abs(J306["P6_sparc_alfalfa"]["median_dlogMHI_all"] - (-TIE1)) < 1e-12)
L1_tie = float(fit1(arrays(P1g, 0.5, 10 ** TIE1)))
L1 = L1_tie
P(f"  nominal log a0 {L1_nom:+.4f} +- {sd1:.4f}; on the ALFALFA flux scale (M_gas x 10^{TIE1:+.4f}): {L1:+.4f} (shift {L1 - L1_nom:+.4f})")
P(f"  levers: gas {lev1_gas:+.3f}, stellar {lev1_star:+.3f}, distance {lev1_D:+.3f} (dex a0 per dex)")
RC_RED = ((0.196 + 0.16) / 2) / 2
U1 = {"statistics": sd1, "P1 RC reduction": RC_RED, "ladder zero point": abs(lev1_D) * 0.01, "flux-tie transfer": abs(L1 - L1_nom) / 2}

# ------------------------------------------------------------------ P2: MeerKAT MIGHTEE-HI (committed CFG306 / CFG304 numbers)
P("\nP2 MeerKAT MIGHTEE-HI rest-frame width chain (CFG309 k = 0; CFG306 numbers; CFG304 flux offset)")
a2_k0 = J306["P1_frame"]["k0"]["a0"]; a2_h67 = J306["P7_h2_h0"]["k=0 H0=67.4"]
fx = J306["P3_flux_frame"]["C1 code-1 (CFG304 primary) | k=0"]; R304 = fx["R"]; a2_gasR = fx["a0_gas"]
J304 = jl("campaign_fresh_gravity/CFG304_mightee_flux_scale_alfalfa/cfg304_flux_scale_alfalfa_results.json")["numbers"]["results"]["cat"]["C1"]["OPT"]
check(f"K2c P2 inputs: a0(k0) {a2_k0:.5e}, a0(k0, H0 67.4) {a2_h67:.5e}, a0_gas(R {R304:+.4f}) {a2_gasR:.5e} vs 1.3111e-10 / 1.2078e-10 / 9.0133e-11 (tol 1e-3); R equals CFG304 median {J304['median']:+.5f}",
      abs(a2_k0 / 1.3111e-10 - 1) < 1e-3 and abs(a2_h67 / 1.2078e-10 - 1) < 1e-3 and abs(a2_gasR / 9.0133e-11 - 1) < 1e-3 and abs(R304 - J304["median"]) < 1e-12)
lev2_gas = math.log10(a2_gasR / a2_k0) / (-R304)            # per dex of M_HI increase (catalogue -> ALFALFA raises M_HI by -R)
rec = J306["P1_frame"]["k0_recipe"]
lev2_star = -rec["mstar"] / 0.25
lev2_HF = math.log10(a2_k0 / a2_h67) / math.log10(70 / 67.4)
L2_base = math.log10(a2_h67); L2 = L2_base + lev2_gas * (-R304)
ci304 = (J304["p84"] - J304["p16"]) / 2
U2 = {"statistics": J306["P1_frame"]["k0_boot"]["sd_dex"], "P2 width recipe": math.hypot(rec["delta"], rec["dhi"]),
      "flux-tie transfer": abs(lev2_gas) * math.hypot(-R304 / 2, ci304)}
P(f"  base (H0 67.4, catalogue flux) log a0 {L2_base:+.4f}; on the ALFALFA scale {L2:+.4f} (a0 {10 ** L2:.4e})")
P(f"  levers: gas {lev2_gas:+.3f}, stellar {lev2_star:+.3f}, Hubble-flow distance scale {lev2_HF:+.3f}; CFG304 68% half-width {ci304:.4f} dex")

# ------------------------------------------------------------------ P3: WALLABY DR2 gas points (p43 re-implemented)
P("\nP3 WALLABY DR2 gas points (p43 method; kernel switch; H0 switch)")
DD = os.path.join(os.path.dirname(REPO), "_external_data", "wallaby_dr2")
GW = 4.30091e-6; KMS2KPC = 1e6 / 3.0857e19
def v2_disc(R_eval, r_prof, sig_prof, rmax_fac=1.5, nring=600):
    rlast = r_prof[-1]; rr = np.linspace(0, rmax_fac * rlast, nring + 1); a = 0.5 * (rr[1:] + rr[:-1]); da = np.diff(rr)
    sig = np.interp(a, r_prof, sig_prof)
    if len(r_prof) >= 3 and sig_prof[-1] > 0 and sig_prof[-2] > sig_prof[-1]:
        h = (r_prof[-1] - r_prof[-2]) / math.log(sig_prof[-2] / sig_prof[-1])
        out = a > rlast; sig[out] = sig_prof[-1] * np.exp(-(a[out] - rlast) / h)
    else:
        sig[a > rlast] = 0.0
    m = 2 * math.pi * a * da * sig
    v2 = np.zeros_like(R_eval, dtype=float)
    for j, R in enumerate(R_eval):
        def phi(Rx):
            k2 = 4 * a * Rx / (a + Rx) ** 2
            return np.sum(-2 * GW * m / math.pi * ellipk(np.minimum(k2, 1 - 1e-12)) / (a + Rx))
        dR = 1e-3 * R
        v2[j] = R * (phi(R + dR) - phi(R - dR)) / (2 * dR)
    return v2
kin = list(csv.DictReader(open(os.path.join(DD, "wallaby_dr2_kinematic_catalogue.csv"))))
src = {r["name"]: r for r in csv.DictReader(open(os.path.join(DD, "wallaby_dr2_source_catalogue.csv")))}
wise = {r["wallaby_name"]: r for r in csv.DictReader(open(os.path.join(DD, "allwise_wallaby_dr2.csv")))}
GX = {("WALLABY " + r["name"]): r for r in csv.DictReader(l for l in open(os.path.join(REPO, "prep_2026", "wallaby_firing", "gext_wallaby_237.csv")) if not l.startswith("#"))}
arr = lambda s: np.array([float(x) for x in s.split(",")]) if s else np.array([])
best = {}
for r in kin:
    if r["QFlag_model"] not in ("0.0", "0"): continue
    n = len(arr(r["Rad"]))
    if r["name"] not in best or n > len(arr(best[r["name"]]["Rad"])): best[r["name"]] = r
def flt(x):
    try: return float(x)
    except Exception: return float("nan")
_cache = {}
def build(H0w=73.0, rdfac=1.0, fluxcorr=True, sig_ad=0.0, dist="hubble"):
    key = (H0w, rdfac, fluxcorr, sig_ad, dist)
    if key in _cache: return _cache[key]
    gals = []
    for nm, r in best.items():
        s, w = src.get(nm), wise.get(nm)
        if s is None or w is None: continue
        D = flt(s["dist_h"]) * 70.0 / H0w
        gx = GX.get(nm)
        if dist == "cmb" and gx is not None: D = flt(gx["D_mpc"]) * 73.0 / H0w
        if flt(r["Inc_model"]) < 30: continue
        fc = 10 ** (flt(s["log_m_hi_corr"]) - flt(s["log_m_hi"])) if fluxcorr and np.isfinite(flt(s.get("log_m_hi_corr", "nan"))) else 1.0
        m1 = flt(w["w1gmag"]) if np.isfinite(flt(w["w1gmag"])) else flt(w["w1mpro"])
        if not (np.isfinite(D) and D > 0 and np.isfinite(m1)): continue
        kpc_as = D * 1e3 / 206264.806
        R = arr(r["Rad"]) * kpc_as; V = arr(r["Vrot_model"]); eV = np.maximum(arr(r["e_Vrot_model"]), 2.0)
        rS = arr(r["Rad_SD"]) * kpc_as; S = arr(r["SD_FO_model"]) * 1e6 * 1.33 * fc
        if len(R) < 3 or len(rS) < 3: continue
        Mstar = 0.6 * 10 ** (-0.4 * (m1 - 5 * math.log10(D * 1e6) + 5 - 3.24))
        r2 = flt(w["r_2mass"])
        Rd = (r2 * kpc_as / 3.5) if (np.isfinite(r2) and r2 > 0) else 10 ** (0.33 * (math.log10(Mstar) - 10) + 0.45)
        Rd *= rdfac
        ok = (R > 0) & (V > 0)
        R, V, eV = R[ok], V[ok], eV[ok]
        if sig_ad > 0: V = np.sqrt(V ** 2 + sig_ad ** 2 * R / (rS[-1] / 3.5))
        vg2 = v2_disc(R, rS, S)
        yy = R / (2 * Rd)
        vs2 = 4 * math.pi * GW * (Mstar / (2 * math.pi * Rd ** 2)) * Rd * yy ** 2 * (i0(yy) * k0(yy) - i1(yy) * k1(yy))
        gals.append(dict(name=nm, R=R, V=V, eV=eV, vg2=vg2, vs2=vs2, D=D))
    _cache[key] = gals
    return gals
def gas_points(gals, ups_scale=1.0, gas_scale=1.0, fcut=0.8):
    Pp = []
    for g in gals:
        vb2 = g["vg2"] + g["vs2"]
        fg = np.where(vb2 > 0, g["vg2"] / np.where(vb2 > 0, vb2, 1), 0)
        m = (fg > fcut) & (g["vg2"] > 0)                       # mask at nominal (frozen for the lever runs)
        if m.sum() >= 2:
            gb = (gas_scale * g["vg2"][m] + ups_scale * g["vs2"][m]) / g["R"][m] * KMS2KPC
            go = g["V"][m] ** 2 / g["R"][m] * KMS2KPC
            sg = (2 * g["eV"][m] / g["V"][m]) / math.log(10)
            Pp.append((g["name"], gb, go, sg))
    return Pp
AG = np.exp(np.linspace(math.log(0.3e-10), math.log(3.0e-10), 121))
def fit3(Pp, kern="mono", sint=0.11):
    ch = np.zeros_like(AG)
    for _, gb, go, sg in Pp:
        for i, a in enumerate(AG):
            pred = gb * (C.nu_mono(gb / a) if kern == "mono" else np.sqrt(1 + a / gb))
            ch[i] += np.sum((np.log10(go) - np.log10(pred)) ** 2 / (sg ** 2 + sint ** 2))
    i = int(np.argmin(ch)); lo, hi = max(0, i - 6), min(len(AG), i + 7)
    p = np.polyfit(np.log(AG[lo:hi]) - math.log(AG[i]), ch[lo:hi], 2)
    return math.exp(math.log(AG[i]) - p[1] / (2 * p[0]))
def boot3(Pp, kern="mono"):
    rng = np.random.default_rng(43); B = [fit3([Pp[i] for i in rng.integers(0, len(Pp), len(Pp))], kern) for _ in range(200)]
    lo, hi = np.percentile(B, [16, 84]); return (math.log10(hi) - math.log10(lo)) / 2, lo, hi
a3_ctl = fit3(gas_points(build(73.0)), "quad"); a3_ctl70 = fit3(gas_points(build(70.0)), "quad")
check(f"K2d P3 control (quadrature, H0 73) a0 {a3_ctl:.4e} vs p43 7.282e-11 (rel {a3_ctl / 7.282e-11 - 1:+.4f}, tol 0.005); H0 70 {a3_ctl70:.4e} vs 6.667e-11 (rel {a3_ctl70 / 6.667e-11 - 1:+.4f})",
      abs(a3_ctl / 7.282e-11 - 1) < 0.005 and abs(a3_ctl70 / 6.667e-11 - 1) < 0.005)
G67 = build(67.4); P3p = gas_points(G67)
a3 = fit3(P3p); L3 = math.log10(a3); sd3, lo3, hi3 = boot3(P3p)
npts3 = sum(len(p[1]) for p in P3p)
ymed3 = float(np.median(np.concatenate([p[1] for p in P3p]) / a3))
Dmin3 = min(g["D"] for g in G67 if g["name"] in {p[0] for p in P3p})
lev3_gas = (math.log10(fit3(gas_points(G67, gas_scale=1.1))) - L3) / math.log10(1.1)
lev3_star = (math.log10(fit3(gas_points(G67, ups_scale=1.4))) - L3) / math.log10(1.4)
a3_70 = fit3(gas_points(build(70.0))); lev3_HF = (math.log10(a3_70) - L3) / math.log10(70 / 67.4)
a3_cmb = fit3(gas_points(build(67.4, dist="cmb"))); a3_ad = fit3(gas_points(build(67.4, sig_ad=8.0)))
a3_rd = [fit3(gas_points(build(67.4, rdfac=f))) for f in (0.5, 2.0)]; a3_nofc = fit3(gas_points(build(67.4, fluxcorr=False)))
U3 = {"statistics": sd3, "P3 distance frame": abs(math.log10(a3_cmb / a3)) / 2,
      "P3 AD/Rd/EFE": math.sqrt(math.log10(a3_ad / a3) ** 2 + max(abs(math.log10(x / a3)) for x in a3_rd) ** 2 + (0.5 * math.log10(1.085)) ** 2),
      "flux-tie transfer": abs(math.log10(a3 / a3_nofc)) / 2}
P(f"  {len(P3p)} galaxies, {npts3} gas points, median y {ymed3:.3f}, nearest D {Dmin3:.1f} Mpc; nu_mono at H0 67.4: a0 {a3:.4e} (log {L3:+.4f}; boot 68% {lo3:.3e}-{hi3:.3e}, +-{sd3:.4f} dex)")
P(f"  levers: gas {lev3_gas:+.3f}, stellar {lev3_star:+.3f}, Hubble-flow {lev3_HF:+.3f}; CMB-frame {a3_cmb:.3e}, AD8 {a3_ad:.3e}, Rd x0.5/x2 {a3_rd[0]:.3e}/{a3_rd[1]:.3e}, no flux corr {a3_nofc:.3e}")

# ------------------------------------------------------------------ the combination machinery
SH = {"S_gas": 0.0473, "S_star": 0.068, "S_HF": 0.0174}
def route(name, L, U, lev): return dict(name=name, L=float(L), U={k: float(v) for k, v in U.items()}, lev={k: float(v) for k, v in lev.items()})
R1 = route("P1 SPARC gas points (ladder)", L1, U1, {"S_gas": lev1_gas, "S_star": lev1_star, "S_HF": 0.0})
R2 = route("P2 MeerKAT MIGHTEE-HI widths", L2, U2, {"S_gas": lev2_gas, "S_star": lev2_star, "S_HF": lev2_HF})
R3 = route("P3 WALLABY DR2 gas points", L3, U3, {"S_gas": lev3_gas, "S_star": lev3_star, "S_HF": lev3_HF})
PRIM = [R1, R2, R3]
def cov(routes, sh=SH, drop=None, uscale=1.0):
    n = len(routes); Cm = np.zeros((n, n))
    for i, r in enumerate(routes):
        Cm[i, i] += sum((0 if k == drop else v * uscale) ** 2 for k, v in r["U"].items())
    keys = sorted(set(k for r in routes for k in r["lev"]))
    for k in keys:
        if k == drop: continue
        l = np.array([r["lev"].get(k, 0.0) for r in routes]); Cm += np.outer(l, l) * sh.get(k, 0.0) ** 2
    return Cm
def combine(routes, sh=SH, drop=None, Lvec=None):
    Lv = np.array([r["L"] for r in routes]) if Lvec is None else np.asarray(Lvec)
    Cm = cov(routes, sh, drop); Ci = np.linalg.inv(Cm); one = np.ones(len(routes))
    w = Ci @ one / (one @ Ci @ one); Lh = float(w @ Lv); s = float(1 / math.sqrt(one @ Ci @ one))
    res = Lv - Lh; q = float(res @ Ci @ res); dof = len(routes) - 1
    return dict(L=Lh, sigma=s, w=w.tolist(), chi2=q, dof=dof, p=float(CHI2.sf(q, dof)) if dof > 0 else float("nan"))
def verdict(Lh, s, foot, scale=1.0):
    lst = [(n, a * scale) for n, a in CAND[foot]]
    pulls = {n: abs(Lh - math.log10(a)) / s for n, a in lst}
    if pulls["1/2"] >= 2: v = "INCONSISTENT WITH 1/2"
    elif all(pulls[n] >= 2 for n in pulls if n != "1/2"): v = "CONSISTENT WITH 1/2 & DISCRIMINATING"
    else: v = "CONSISTENT BUT NOT DISCRIMINATING"
    return v, pulls
def kap(L, foot, scale=1.0): return 10 ** L / ((DEN_L if foot == "canonical" else DEN_C) * scale)

# ------------------------------------------------------------------ I2 and per-route budgets
P("\nI2 M/L-insensitivity (|lever_star| x 0.068 <= 0.05 dex)")
for r in PRIM: check(f"I2 {r['name']}: {abs(r['lev']['S_star']) * 0.068:.4f} dex", abs(r["lev"]["S_star"]) * 0.068 <= 0.05)
P("\nPER-ROUTE BUDGET (dex in log a0; shared terms = |lever| x prior sigma)")
RES["routes"] = {}
for r in PRIM:
    sh_terms = {k: abs(r["lev"][k]) * SH[k] for k in SH}
    tot = math.sqrt(sum(v ** 2 for v in r["U"].values()) + sum(v ** 2 for v in sh_terms.values()))
    r["total"] = tot
    P(f"  {r['name']}: log a0 {r['L']:+.4f} +- {tot:.4f}  (a0 {10 ** r['L']:.3e}; kappa_Lambda {kap(r['L'], 'canonical'):.3f} +- {kap(r['L'], 'canonical') * tot * LN10:.3f}; kappa_crit {kap(r['L'], 'alt'):.3f} +- {kap(r['L'], 'alt') * tot * LN10:.3f})")
    P("     " + ", ".join(f"{k} {v:.4f}" for k, v in list(r["U"].items()) + list(sh_terms.items())))
    RES["routes"][r["name"]] = dict(L=r["L"], a0=10 ** r["L"], total_sigma_dex=tot, unique=r["U"], shared_terms=sh_terms, levers=r["lev"],
                                    kappa_L=kap(r["L"], "canonical"), kappa_c=kap(r["L"], "alt"))

# ------------------------------------------------------------------ K4, power label, K3
P("\nK4 GLS sanity")
cb = combine(PRIM)
same = combine(PRIM, Lvec=[-10.0, -10.0, -10.0])
check(f"K4 weights sum {sum(cb['w']):.15f}; identical inputs -10 return {same['L']:+.12f}", abs(sum(cb["w"]) - 1) < 1e-12 and abs(same["L"] + 10) < 1e-12)
# shared-only floor: unique terms zero; the shared covariance is rank-deficient, so take the minimum-variance weights limit numerically
Csh = cov(PRIM, uscale=1e-6); one = np.ones(3); floor_s = float(1 / math.sqrt(one @ np.linalg.inv(Csh) @ one))
lab = "POSSIBLE" if cb["sigma"] <= 0.0178 else ("PARTIAL" if cb["sigma"] <= 0.0261 else "NOT POSSIBLE")
P(f"\nPOWER LABEL (error model only): sigma_hat {cb['sigma']:.4f} dex ({100 * (10 ** cb['sigma'] - 1):.1f}% in kappa) -> {lab}")
P(f"  shared-systematic floor (all route-unique terms -> 0): {floor_s:.4f} dex ({100 * (10 ** floor_s - 1):.1f}%) vs the 2-3% goal (0.0087-0.0128 dex): {'below' if floor_s <= 0.0128 else 'ABOVE'} the goal")
P("\nK3 coverage (4000 mocks from N(L_1/2, C))")
rng = np.random.default_rng(493); Cm = cov(PRIM); Lhalf = math.log10(A_HALF_L)
mocks = rng.multivariate_normal(np.full(3, Lhalf), Cm, size=4000)
Ci = np.linalg.inv(Cm); wv = Ci @ one / (one @ Ci @ one)
pl = (mocks @ wv - Lhalf) / cb["sigma"]; resm = mocks - (mocks @ wv)[:, None]
pv = CHI2.sf(np.einsum("ij,jk,ik->i", resm, Ci, resm), 2)
check(f"K3 mean pull {pl.mean():+.4f} (|.|<=0.05), SD {pl.std():.4f} (0.95-1.05), P(p<0.05) {np.mean(pv < 0.05):.4f} (0.035-0.065)",
      abs(pl.mean()) <= 0.05 and 0.95 <= pl.std() <= 1.05 and 0.035 <= np.mean(pv < 0.05) <= 0.065)
RES["power"] = dict(sigma_hat=cb["sigma"], label=lab, floor=floor_s)

# ------------------------------------------------------------------ MUTATE injection
mut_info = None
if MUT:
    imax = int(np.argmax(np.abs(cb["w"]))); before = cb["L"]
    PRIM[imax]["L"] += 0.04139; cbm = combine(PRIM)
    mut_info = dict(route=PRIM[imax]["name"], w=cb["w"][imax], dL=cbm["L"] - before)
    P(f"\nMUTATE: +0.04139 dex (+10%) injected into {PRIM[imax]['name']} (GLS weight {cb['w'][imax]:.4f})")
    check(f"M1 L_hat moved {cbm['L'] - before:+.10f} = w x 0.04139 = {cb['w'][imax] * 0.04139:+.10f} (tol 1e-9)", abs(cbm["L"] - before - cb["w"][imax] * 0.04139) < 1e-9)
    others = [r for j, r in enumerate(PRIM) if j != imax]; co = combine(others)
    pull_r = (PRIM[imax]["L"] - co["L"]) / math.sqrt(co["sigma"] ** 2 + PRIM[imax]["total"] ** 2)  # ignores the shared correlation: reported only
    P(f"  M2 (reported) real errors: consistency chi2 {cbm['chi2']:.3f} (p {cbm['p']:.3f}) -> TENSION {'FLAGGED' if cbm['p'] < 0.05 else 'NOT flagged'}; route vs the others {pull_r:+.2f} sigma (shared terms ignored)")
    def precise(rs):
        out = []
        for r in rs:
            u = dict(r["U"]); tot = math.sqrt(sum(v ** 2 for v in u.values())); u = {k: v * 0.0107 / tot for k, v in u.items()}
            out.append(route(r["name"], r["L"], u, r["lev"]))
        return out
    shp = {k: 0.005 for k in SH}; PR = precise(PRIM); cpm = combine(PR, shp)
    PRIM[imax]["L"] -= 0.04139; cp0 = combine(precise(PRIM), shp); PRIM[imax]["L"] += 0.04139
    # precision world centred on the real values would carry the real route spread; M3 is defined on a world where the routes agree before the injection
    agree = [route(r["name"], cb["L"], r["U"], r["lev"]) for r in PRIM]; agree_m = [dict(x) for x in agree]; agree_m[imax] = dict(agree_m[imax]); agree_m[imax]["L"] = cb["L"] + 0.04139
    c_in = combine(precise(agree_m), shp); c_no = combine(precise(agree), shp)
    check(f"M3 precision world (unique 2.5%, shared 0.005 dex): with the injection p {c_in['p']:.4g} (< 0.05 required), without p {c_no['p']:.4g} (>= 0.05 required)", c_in["p"] < 0.05 and c_no["p"] >= 0.05)
    P(f"  (also reported: precision errors on the REAL route values: p {cp0['p']:.3g} before, {cpm['p']:.3g} after the injection)")
    # POST-HOC (added after M3 failed as frozen; print-only, never a check): the frozen 0.005 dex shared sigma is multiplied by levers up to
    # ~2.3 (S_HF acts on P2/P3 but not P1), so the realised differential shared term is ~0.011 dex, not 0.005.
    shq = {k: 0.005 / max(abs(r["lev"][k]) for r in PRIM) for k in SH}; c_q = combine(precise(agree_m), shq)
    c_z = combine(precise(agree_m), {k: 0.0 for k in SH})
    P(f"  POST-HOC (print-only): shared sigma scaled so |lever| x sigma <= 0.005 dex: p {c_q['p']:.4g}; shared terms off: p {c_z['p']:.4g}")
    mut_info.update(posthoc_scaled_shared_p=c_q["p"], posthoc_no_shared_p=c_z["p"])
    cb = cbm
    mut_info.update(M2_p=cbm["p"], M3_p_in=c_in["p"], M3_p_no=c_no["p"], real_precision_p=cp0["p"])
    RES["mutate"] = mut_info

# ------------------------------------------------------------------ RESULT
P("\nCOMBINED (GLS, primary routes)")
P("  weights: " + ", ".join(f"{r['name'].split()[0]} {w:+.3f}" for r, w in zip(PRIM, cb["w"])))
P(f"  log a0 = {cb['L']:+.4f} +- {cb['sigma']:.4f}  ->  a0 = {10 ** cb['L']:.4e} m s^-2 (68% {10 ** (cb['L'] - cb['sigma']):.3e}-{10 ** (cb['L'] + cb['sigma']):.3e})")
P(f"  consistency chi2 {cb['chi2']:.3f} / {cb['dof']} dof, p {cb['p']:.3f} -> {'ROUTES IN TENSION' if cb['p'] < 0.05 else 'routes mutually consistent'}")
RES["combined"] = dict(cb, a0=10 ** cb["L"])
for foot in ("canonical", "alt"):
    k = kap(cb["L"], foot); v, pulls = verdict(cb["L"], cb["sigma"], foot)
    P(f"  {foot:9s} footing: kappa = {k:.4f} +- {k * cb['sigma'] * LN10:.4f} ({'rho_Lambda' if foot == 'canonical' else 'rho_crit'})")
    P("     pulls: " + "; ".join(f"{n} {s:.2f} sigma" for n, s in pulls.items()))
    P(f"     VERDICT ({foot}): {v}")
    RES["combined"][foot] = dict(kappa=k, sigma=k * cb["sigma"] * LN10, pulls=pulls, verdict=v)
fp = abs(math.log10(A_HALF_C / A_HALF_L)) / cb["sigma"]
P(f"  the two footings' 1/2 values (9.36e-11 vs 1.131e-10) differ by {math.log10(A_HALF_C / A_HALF_L):.4f} dex = {fp:.2f} sigma_hat; canonical-1/2 pull {abs(cb['L'] - math.log10(A_HALF_L)) / cb['sigma']:.2f}, alt-1/2 pull {abs(cb['L'] - math.log10(A_HALF_C)) / cb['sigma']:.2f}")
RES["combined"]["footing_separation_sigma"] = fp
P("  per-route pulls against the combination (diagonal, shared terms included): " + "; ".join(
    f"{r['name'].split()[0]} {(r['L'] - cb['L']) / math.sqrt(max(cov(PRIM)[i, i] - cb['sigma'] ** 2, 1e-12)):+.2f}" for i, r in enumerate(PRIM)))

# ------------------------------------------------------------------ dominant systematic
P("\nDOMINANT SYSTEMATIC (sigma_hat with one group removed)")
groups = ["statistics", "S_gas", "S_star", "S_HF", "ladder zero point", "flux-tie transfer", "P1 RC reduction", "P2 width recipe", "P3 distance frame", "P3 AD/Rd/EFE"]
dom = {}
for gname in groups:
    s = combine(PRIM, drop=gname)["sigma"]; dom[gname] = s; P(f"  without {gname:20s}: sigma_hat {s:.4f} (reduction {cb['sigma'] - s:.4f})")
dmax = min(dom, key=dom.get); P(f"  -> dominant group: {dmax}")
RES["dominant"] = dict(by_group=dom, dominant=dmax)

# ------------------------------------------------------------------ variants (never the verdict)
P("\nVARIANTS (reported; never the verdict)")
VAR = {}
def show(lab_, routes, sh=SH, scale=1.0):
    r = combine(routes, sh); vc, _ = verdict(r["L"], r["sigma"], "canonical", scale); va, _ = verdict(r["L"], r["sigma"], "alt", scale)
    P(f"  {lab_:58s} log a0 {r['L']:+.4f} +- {r['sigma']:.4f}; kappa_L {kap(r['L'], 'canonical', scale):.3f}, kappa_c {kap(r['L'], 'alt', scale):.3f}; p {r['p']:.3f}; {vc} / {va}")
    VAR[lab_] = dict(r, kappa_L=kap(r["L"], "canonical", scale), kappa_c=kap(r["L"], "alt", scale), verdict_canonical=vc, verdict_alt=va)
JMN = jl("qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.json")
kC, sC = JMN["S3_C"]["kappa"], JMN["S3_C"]["sigma"]; kA, sA = JMN["S3"]["box_A"]["R1"], 0.073
RC_ = route("SPARC estimator C", math.log10(kC * DEN_L), {"committed total": sC / kC / LN10}, {})
RA_ = route("SPARC estimator A", math.log10(kA * DEN_L), {"committed total": sA / kA / LN10}, {})
show("V1 SPARC = estimator C", [RC_, R2, R3]); show("V2 SPARC = estimator A", [RA_, R2, R3])
L1q = float(fit1(arrays(P1g, 0.5, 10 ** TIE1), nu_quad)); a3q = fit3(P3p, "quad")
kern2 = math.log10(J306["P2_kernels"]["rows"]["framework closed form sqrt(1+1/y)"]["a0_k0"] / a2_k0)
show("V3 kernel = quadrature sqrt(1+1/y) (all routes)", [dict(R1, L=L1q), dict(R2, L=L2 + kern2), dict(R3, L=math.log10(a3q))])
P(f"     kernel shifts: P1 {L1q - L1:+.4f}, P2 {kern2:+.4f}, P3 {math.log10(a3q) - L3:+.4f} dex")
u1n = dict(U1); u1n.pop("flux-tie transfer"); u2n = dict(U2); u2n.pop("flux-tie transfer"); u3n = dict(U3); u3n.pop("flux-tie transfer")
show("V4 no flux tie (own flux scales)", [dict(R1, L=L1_nom, U=u1n), dict(R2, L=L2_base, U=u2n), dict(R3, L=math.log10(a3_nofc), U=u3n)])
a2_087 = J306["P3_flux_frame"]["CFG306 S2: code-1 trend in z extrapolated to the 47 | k=0"]["a0_gas"]
show("V5 P2 flux offset -0.087 (S2 z-trend)", [R1, dict(R2, L=L2_base + math.log10(a2_087 / a2_k0)), R3])
a3_73 = fit3(gas_points(build(73.04))); dl2_73 = lev2_HF * math.log10(73.04 / 67.4)
show("V6 HF distances at H0 73.04, rho_Lambda at 67.4", [R1, dict(R2, L=L2 + dl2_73), dict(R3, L=math.log10(a3_73))])
show("V7 footing rebuilt at H0 73.04 (Omega_Lambda fixed)", [R1, dict(R2, L=L2 + dl2_73), dict(R3, L=math.log10(a3_73))], scale=73.04 / 67.4)
J261 = jl("campaign_fresh_gravity/CFG261_kids_absolute_a0_zthirds/cfg261_stageB_results.json")["numbers"]["rows"]
kr = [route(f"KiDS {k}", J261[k]["ls"] + math.log10(A_HALF_L), {"statistics": J261[k]["jsd"]}, {"S_kids": 1.0}) for k in ("T-late-LO", "T-late-HI")]
show("V8 + KiDS late-type rows (M* band 0.17 shared)", [R1, R2, R3] + kr, sh=dict(SH, S_kids=0.17))
show("V9 no P1 rotation-curve reduction term", [dict(R1, U={k: v for k, v in U1.items() if k != "P1 RC reduction"}), R2, R3])
def unif(U): return {k: (v / math.sqrt(3) if k in ("P2 width recipe", "flux-tie transfer") else v) for k, v in U.items()}
show("V10 recipe and transfer half-widths uniform (/sqrt 3)", [dict(R1, U=unif(U1)), dict(R2, U=unif(U2)), dict(R3, U=unif(U3))])
p0 = arrays(S0g, 0.5, 10 ** TIE1); L1s0 = float(fit1(p0)); sds0 = boot1(arrays(S0g, 0.5))
show("V11 P1 = CFG397 10-galaxy anchor", [dict(R1, L=L1s0, U=dict(U1, statistics=sds0)), R2, R3])
RES["variants"] = VAR

# ------------------------------------------------------------------ report-only rows
P("\nREPORT-ONLY ROUTES (not combined; reason in the criteria)")
J397 = jl("campaign_fresh_gravity/CFG397_gas_only_a0_rung/cfg397_gas_rung_results.json")["res"]["C Hubble flow"]
J43 = jl("qwen_claude_field_theory/papers_2026/PAPER43_figures_numbers.json")
ro = [("SPARC estimator A (Planck-consistent)", math.log10(kA * DEN_L), sA / kA / LN10),
      ("SPARC estimator B (shape only)", math.log10(JMN["S2"]["kappa_B"] * DEN_L), JMN["S2"]["sigma_B"] / JMN["S2"]["kappa_B"] / LN10),
      ("SPARC estimator C (profile likelihood)", math.log10(kC * DEN_L), sC / kC / LN10),
      ("SPARC Hubble-flow gas points (tabulated H0 73)", J397["log_a0"], J397["sd"]),
      ("SPARC Hubble-flow gas points moved to H0 67.4 (x(67.4/73)^2)", J397["log_a0"] + 2 * math.log10(67.4 / 73), J397["sd"]),
      ("KiDS late, z 0.20 (stat only; M* band +-0.17)", J261["T-late-LO"]["ls"] + math.log10(A_HALF_L), J261["T-late-LO"]["jsd"]),
      ("KiDS late, z 0.40", J261["T-late-HI"]["ls"] + math.log10(A_HALF_L), J261["T-late-HI"]["jsd"]),
      ("PAPER43 pool (quadrature kernel, mixed H0)", math.log10(J43["pool"][0]), J43["pool"][1] / LN10),
      ("Desmond 2023 (literature, SPARC, free M/L)", math.log10(1.19e-10), 0.10 / 1.19 / LN10)]
for n, L, s in ro:
    if not np.isfinite(L): continue
    P(f"  {n:58s} log a0 {L:+.4f} +- {s:.4f}: kappa_L {kap(L, 'canonical'):.3f}, kappa_c {kap(L, 'alt'):.3f}")
early = [k for k in J261 if "early" in k.lower()]
for k in early: P(f"  KiDS {k:52s} log a0 {J261[k]['ls'] + math.log10(A_HALF_L):+.4f} +- {J261[k]['jsd']:.4f}: kappa_L {kap(J261[k]['ls'] + math.log10(A_HALF_L), 'canonical'):.3f} (class-inconsistent with late)")
RES["report_only"] = {n: dict(L=L, sigma=s) for n, L, s in ro if np.isfinite(L)}

# ------------------------------------------------------------------ finish
lb_fail = [c_["name"] for c_ in CHECKS if not c_["ok"] and c_["load_bearing"]]
P(f"\n{sum(c_['ok'] for c_ in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {len(lb_fail)}")
RES["checks"] = CHECKS
json.dump(RES, open(os.path.join(HERE, f"cfg493_kappa_combined{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg493_kappa_combined{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if lb_fail else 0)
