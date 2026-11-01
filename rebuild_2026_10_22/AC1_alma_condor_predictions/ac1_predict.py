#!/usr/bin/env python3
"""AC1: pre-data predictions for the ALMA release of 2026-11-06 (FROZEN_CRITERIA.md, 57d3ac6b64). Nothing fetched; no pixel of the MOUS read.
    python3 ac1_predict.py            # writes ac1_predict.out, ac1_results.json; exit 1 on any K failure
    python3 ac1_predict.py --mutate   # R31 x 10 in the L' conversion; writes _MUTATE outputs; exit 1 if K7 bites
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; one disc excludes no model; not theory closed."""
import csv, hashlib, json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); ROOT = os.path.dirname(REB); CFGD = os.path.join(ROOT, "campaign_fresh_gravity")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; R31 = 18.0 if MUT else 1.8
OUT = []; CHK = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(n, ok, x=""): CHK.append((n, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {n} {x}")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

# ---- CFG571's head, read-only ----
src = open(os.path.join(CFGD, "CFG571_prereg_proprietary_alma", "cfg571_prereg.py")).read(); head = src[:src.index("# ---- controls ----")]
ns = {"__file__": os.path.join(CFGD, "CFG571_prereg_proprietary_alma", "cfg571_prereg.py"), "__name__": "cfg571_head"}
_a = sys.argv; sys.argv = [_a[0]]; exec(compile(head, "cfg571_head", "exec"), ns); sys.argv = _a
G, U, FOOT, MODELS = ns["G"], ns["U"], ns["FOOT"], ns["MODELS"]; v2_exp, m_from_v2 = ns["v2_exp"], ns["m_from_v2"]
NU_MONO = ns["NU"]; nu1 = lambda y: (1 + np.sqrt(1 + 4 / np.asarray(y, float))) / 2; nu2 = lambda y: np.sqrt(1 + 1 / np.asarray(y, float)); nuN = lambda y: np.ones_like(np.asarray(y, float))
KERN = {"n=1": nu1, "nu_mono": NU_MONO, "n=2": nu2}

# ---- K3, seals ----
SEALS = {"CFG571": (os.path.join(CFGD, "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json"), "be27457d"), "AG4e": (os.path.join(ROOT, "argon_push", "AG4e_n1_alma_seal", "SEALED_N1.json"), "9802de0d"),
         "AG4d": (os.path.join(ROOT, "argon_push", "AG4d_n2_alma_seal", "SEALED_N2.json"), "d64727b5"), "S3": (os.path.join(REB, "S3_v3_mw_seals", "SEALED_V3_ALMA_AQUAL.json"), "b5d65a5e")}
check("K3 seal hashes", all(sha(p).startswith(h) for p, h in SEALS.values()), str({k: sha(p)[:8] for k, (p, _) in SEALS.items()}))

# ---- background (B_cfg886_bg), distances ----
H, OM = 0.6856427, 0.2976016; W0, WA = ns["W0"], ns["WA"]
E_L = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
E_D = lambda z: math.sqrt(OM * (1 + z) ** 3 + (1 - OM) * (1 + z) ** (3 * (1 + W0 + WA)) * math.exp(-3 * WA * z / (1 + z)))
def dc(z, E=E_L): return 2.99792458e5 / (100 * H) * quad(lambda x: 1 / E(x), 0, z)[0]   # Mpc
def scale(z, E=E_L): return dc(z, E) / (1 + z) * 1e3 / 206264.806                         # kpc per arcsec
def Lp(F, nu, z, E=E_L): return 3.25e7 * F / nu ** 2 * (dc(z, E) * (1 + z)) ** 2 / (1 + z) ** 3

# ---- K1, identity (archive, 2026-11-01) ----
PC = (34.422382000017684, -5.181044500002704); cat = {r["ID"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data_assembly", "kmos3d_phibss", "kmos3d_catalog.csv")))}
sep = lambda r: math.hypot((float(r["RA"]) - PC[0]) * math.cos(math.radians(PC[1])), float(r["DEC"]) - PC[1]) * 3600
s84, s79 = sep(cat["U4_28473"]), sep(cat["U4_27928"]); ZA, ZB = float(cat["U4_27928"]["Z"]), float(cat["U4_28473"]["Z"])
nuA, nuB = 230.538 / (1 + ZA), 345.796 / (1 + ZB); SIG = {"A": 0.4393, "B": 0.4342}; BEAM = 0.06569852291410361
check("K1 identity", abs(s84) < 0.1 and abs(s79 - 7.36) < 0.05 and 94.79 < nuA < 96.67 and 97.60 < nuB < 98.62, f"U4_28473 {s84:.3f}\", U4_27928 {s79:.3f}\"; CO(2-1) {nuA:.3f} GHz, CO(3-2) {nuB:.3f} GHz")
FWHM = 1.13 * 299792458 / (nuA * 1e9) / 12 * 206264.806; PB = math.exp(-4 * math.log(2) * (s79 / FWHM) ** 2); O_B = 1.133 * BEAM ** 2
P(f"primary beam FWHM {FWHM:.1f}\", response at U4_27928 {PB:.3f}; beam {BEAM:.4f}\" ({BEAM * scale(ZB):.3f} kpc at z {ZB}, {BEAM * scale(ZA):.3f} kpc at z {ZA})")
RES = dict(frozen="57d3ac6b64", mutate=MUT, identity=dict(sep_U4_28473=s84, sep_U4_27928=s79, nu_CO21_U4_27928=nuA, nu_CO32_U4_28473=nuB, pb=PB, fwhm=FWHM, beam=BEAM, kpc_as_A=scale(ZA), kpc_as_B=scale(ZB)))

# ---- route N ----
GE, MS, PCM, KPC = 6.6743e-11, 1.98847e30, 3.0857e16, 3.0857e19
ND = json.load(open(os.path.join(REB, "ND1_native_dwarfs", "nd1_ab_results.json"))); ETA, FC, R10, R11 = ND["eta_A4"], ND["f_c"], ND["rho10"], ND["rho11"]
SCT = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))["sigma_coll_table"].items())
SL, SV = np.array([a for a, _ in SCT]), np.array([b for _, b in SCT])
def sigma_coll(M):
    l = math.log10(M)
    if l < SL[0]: return 10 ** (SV[0] + (SV[1] - SV[0]) / (SL[1] - SL[0]) * (l - SL[0]))
    if l > SL[-1]: return 10 ** (SV[-1] + (SV[-1] - SV[-2]) / (SL[-1] - SL[-2]) * (l - SL[-1]))
    return 10 ** float(np.interp(l, SL, SV))
def S_N(M):   # Msun/pc^2
    Mt = M / FC; lg = math.log10(Mt)
    return FC * float(np.interp(lg, [12, 13, 14], ETA)) * 10 ** float(np.interp(lg, [10.0, 11.0, 12.0], [math.log10(R10), math.log10(R11), 0.0])) * sigma_coll(Mt)
Bk = lambda x: np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def v2_core(M, z, R):
    """(km/s)^2 of the Burkert cold core at R kpc, M200 M Msun, at redshift z."""
    rc = 3 * (100 * H * 1e3 / (1e3 * KPC) * E_L(z)) ** 2 / (8 * math.pi * GE); R2 = (3 * M * MS / (4 * math.pi * 200 * rc)) ** (1 / 3); Sg = S_N(M) * MS / PCM ** 2
    lm = lambda lr: math.log(math.pi * Sg * math.exp(2 * lr) * float(Bk(R2 / math.exp(lr))))
    lpk = float(minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(R2 * 1e-6), math.log(R2 * 1e3)), method="bounded", options={"xatol": 1e-10}).x)
    r0 = math.exp(lpk) if lm(lpk) < math.log(M * MS) else math.exp(brentq(lambda lr: lm(lr) - math.log(M * MS), math.log(R2 * 1e-7), lpk, xtol=1e-14))
    Rm = R * KPC; return GE * math.pi * Sg * r0 ** 2 * float(Bk(Rm / r0)) / Rm / 1e6, r0 / KPC, Sg / (MS / PCM ** 2)
s11 = ND["native"]["B_cfg886_bg"]["S_at"]["11"]; s11A = ND["native"]["A_c2b_refit"]["S_at"]["11"]
check("K5 route N S at lg M200 11 within 1% of ND1's record", min(abs(S_N(1e11) / s11 - 1), abs(S_N(1e11) / s11A - 1)) < 0.01, f"{S_N(1e11):.2f} against {s11A:.2f} / {s11:.2f}")
LM200 = (12.0, 12.5, 13.0)

# ---- generic inverse ----
def gbar_req(gobs, a0, nu):
    A = a0 / U; f = lambda gb: float(nu(gb / A)) * gb - gobs
    return brentq(f, gobs * 1e-8, gobs * (1 + 1e-12), xtol=gobs * 1e-12, rtol=1e-12)
def mgas_req(R, Vc, Ms, Rd, Rg, a0, nu):
    vg2 = gbar_req(Vc ** 2 / R, a0, nu) * R - v2_exp(Ms, Rd, R)
    return math.log10(m_from_v2(vg2, Rg, R)) if vg2 > 0 else None
def mgas_N(R, Vc, Ms, Rd, Rg, lm, z):
    vg2 = Vc ** 2 - v2_exp(Ms, Rd, R) - v2_core(10 ** lm, z, R)[0]
    return math.log10(m_from_v2(vg2, Rg, R)) if vg2 > 0 else None
fm = lambda x: "FLOOR" if x is None else f"{x:5.2f}"

# ---- K2, K4 ----
AG = {"n=1": json.load(open(SEALS["AG4e"][0]))["U4_27928"], "n=2": json.load(open(SEALS["AG4d"][0]))["U4_27928"], "nu_mono": json.load(open(SEALS["CFG571"][0]))["results"]["U4_27928"]}
Re = 0.49 / 206264.806 * (2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, ZA)[0] * 1e3) / (1 + ZA); RA_, RdA = 2 * Re, Re / 1.678
d2 = 0.0; n2_ = 0; nf_ = 0; fl_ = 0
for kn, nu in KERN.items():
    ns["NU"] = nu
    for vs, sd in AG[kn].items():
        pr = ns["predict"](RA_, float(vs), ZA, 10 ** 10.74, RdA)
        for (fn, mn), c in pr.items():
            key = f"{fn}|{mn}"
            if key in sd:
                nf_ += 1; fl_ += str(sd[key].get("floor")) != str(c["floor"])
            if key in sd and sd[key]["logMgas_Rg=Rd"] is not None and c["logMgas_Rg=Rd"] is not None:
                d2 = max(d2, abs(c["logMgas_Rg=Rd"] - sd[key]["logMgas_Rg=Rd"])); n2_ += 1
ns["NU"] = NU_MONO
check("K2 reproduces CFG571, AG4e, AG4d U4 grids", d2 <= 1e-12 and n2_ > 0 and fl_ == 0, f"max |d| {d2:.1e} dex over {n2_} non-FLOOR cells; FLOOR flags differ in {fl_} of {nf_} cells")
vb = math.sqrt(gbar_req(150.0 ** 2 / 9.0, 1.13e-10, nuN) * 9.0); check("K4 Newtonian round trip", abs(vb / 150 - 1) < 1e-6)

# ---- Part A: U4_27928 at the H-alpha prior ----
row = next(r for r in csv.DictReader(open(os.path.join(CFGD, "CFG99_kmos3d_outer_rc", "cfg89_per_object.csv"))) if r["ID"] == "U4_27928")
vr, s0, rd99, mu = float(row["vrot"]), float(row["sigma0"]), float(row["Rd_kpc"]), float(row["mu_gas"]); lmsA = float(row["LMSTAR"])
vc2 = lambda v: math.sqrt(v * v + 2 * s0 * s0 * RA_ / RdA)
CASES = {"a P0": vr, "b P0 /0.72": vr / 0.72, "c P-B": vc2(vr), "d P-B /0.72": vc2(vr / 0.72)}
P(f"\n=== Part A, U4_27928: Halpha vrot {vr:.1f}, sigma0 {s0:.1f}, R {RA_:.2f} kpc; empirical log M_gas {lmsA + math.log10(mu):.2f} (CFG99 mu_gas {mu:.3f}) ===")
A = dict(cases=CASES, empirical_logMgas=lmsA + math.log10(mu), req={})
for cs, Vc in CASES.items():
    A["req"][cs] = {}
    for kn, nu in KERN.items():
        ns["NU"] = nu; pr = ns["predict"](RA_, Vc, ZA, 10 ** lmsA, RdA); A["req"][cs][kn] = {f"{a}|{b}": {k: c[k] for k in ("logMgas_Rg=Rd", "logMgas_Rg=1.5Rd", "floor")} for (a, b), c in pr.items()}
        P(f"{cs:12s} V_c {Vc:5.1f} {kn:8s}: " + " | ".join(f"{m} {fm(pr[('canon 9.36e-11', m)]['logMgas_Rg=Rd'])}/{fm(pr[('alt 1.13e-10', m)]['logMgas_Rg=Rd'])}" for m in ("F-DESI", "F-flat", "R-H", "L-fb(RAR-eq)")))
    A["req"][cs]["route N (added after criteria, information)"] = {str(l): mgas_N(RA_, Vc, 10 ** lmsA, RdA, RdA, l, ZA) for l in LM200}
    P(f"{cs:12s} route N (added, information) lg M200 12/12.5/13: " + " / ".join(fm(mgas_N(RA_, Vc, 10 ** lmsA, RdA, RdA, l, ZA)) for l in LM200))
ns["NU"] = NU_MONO
LA = Lp(1.0, nuA, ZA)
def fc_A(lmg, alpha=4.36, r21=0.77, dv=1000.0):
    F = 10 ** lmg / alpha * r21 / LA; rap = 0.98; x = rap * scale(ZA) / RdA; fr = 1 - (1 + x) * math.exp(-x)
    nb = math.pi * rap ** 2 / O_B; sg = SIG["A"] / PB * 10 * math.sqrt(dv / 10) * math.sqrt(nb) / 1e3
    return F, fr * F / sg, sg / fr
fA = {str(l): dict(zip(("F", "SN_1000", "sig_F"), fc_A(l))) for l in (10.0, 10.42, 10.51, 10.86, 11.0)}
sg = fc_A(10.5)[2]; UL = math.log10(3 * sg * LA * 4.36 / 0.77); UL1 = math.log10(3 * fc_A(10.5, 1.0)[2] * LA * 1.0 / 0.77)
A["forecast"] = dict(per_mass=fA, UL3sig_alpha436=UL, UL3sig_alpha1=UL1, SN_600=fc_A(10.51, dv=600.0)[1])
P(f"detection forecast (2R_e aperture, +-500 km/s, PB corrected): " + "; ".join(f"log M_gas {k}: F {v['F']:.3f} Jy km/s, S/N {v['SN_1000']:.2f}" for k, v in fA.items()) + f"; 3 sigma limit log M_gas {UL:.2f} (alpha 4.36), {UL1:.2f} (alpha 1)")
RES["A"] = A

# ---- Part B: U4_28473 ----
Z = ZB; F32, eF = 0.79, 0.08; LP32 = Lp(F32, nuB, Z); LP10 = R31 * LP32; LP10_D = R31 * Lp(F32, nuB, Z, E_D)
check("K7 log M_gas from the flux, alpha 4.36, equals the hand value 11.3 +- 0.1", abs(math.log10(4.36 * LP10) - 11.3) < 0.1, f"{math.log10(4.36 * LP10):.3f}; L'(1-0) {LP10:.3e}, CPL distance {LP10_D:.3e}")
AL = (4.36, 1.0); LMS = (11.31, 11.35, 11.11, 11.15); RE = {"S1": 1.37, "S2": 0.383 * scale(Z)}; Rg0 = 1.56 / 1.678
RF = {"F-flat": 1.0, "F-DESI": ns["r_desi"](Z), "band low 0.325": 0.325, "band high 1.212": 1.212, "R-H": ns["r_H"](Z), "L-fb(RAR-eq)": ns["r_fb"](Z)}
P(f"\n=== Part B, U4_28473, z {Z}: L'(1-0) {LP10:.3e}; log M_gas {math.log10(4.36 * LP10):.2f} (alpha 4.36), {math.log10(LP10):.2f} (alpha 1); shapes R_e* {RE['S1']:.2f}, {RE['S2']:.2f} kpc, R_e,gas 1.56 kpc; a0 ratios " + ", ".join(f"{k} {v:.3f}" for k, v in RF.items()) + " ===")
B = dict(z=Z, Lp10=LP10, Lp10_CPL=LP10_D, logMgas={str(a): math.log10(a * LP10) for a in AL}, a0_ratio=RF, shapes=RE, forward={}, inverse={}, core={})
RG = (1, 2, 3, 4, 6, 8)
for l in LM200:
    B["core"][str(l)] = dict(S=v2_core(10 ** l, Z, 3.0)[2], r0=v2_core(10 ** l, Z, 3.0)[1], V=[math.sqrt(v2_core(10 ** l, Z, r)[0]) for r in RG])
P("route N core, extrapolation: " + "; ".join(f"lg M200 {k}: S {v['S']:.0f} Msun/pc2, r0 {v['r0']:.1f} kpc, V_core(R 1..8) " + "/".join(f"{x:.0f}" for x in v["V"]) for k, v in B["core"].items()))
def vbar2(R, lms, sh, a, lmg=None):
    return v2_exp(10 ** lms, RE[sh] / 1.678, R) + v2_exp(a * LP10 if lmg is None else 10 ** lmg, Rg0, R)
def vfw(R, lms, sh, a, nu, a0):
    vb2 = vbar2(R, lms, sh, a); g = vb2 / R; return math.sqrt(float(nu(g / (a0 / U))) * vb2)
P("\nForward V_c(R 1,2,3,4,6,8 kpc) [km/s]")
for lms in LMS:
    for sh in RE:
        for a in AL:
            k = f"lgM*{lms}|{sh}|alpha{a}"; B["forward"][k] = {"Newton": [math.sqrt(vbar2(r, lms, sh, a)) for r in RG]}
            for kn, nu in KERN.items():
                for fn, a00 in FOOT.items():
                    for mn, rf in RF.items():
                        B["forward"][k][f"{kn}|{fn}|{mn}"] = [vfw(r, lms, sh, a, nu, a00 * rf) for r in RG]
            for l in LM200:
                B["forward"][k][f"route N|{l}"] = [math.sqrt(vbar2(r, lms, sh, a) + v2_core(10 ** l, Z, r)[0]) for r in RG]
            if lms in (11.31, 11.11):
                row_ = B["forward"][k]; fmt = lambda v: "/".join(f"{x:.0f}" for x in v)
                P(f"{k:24s} Newton {fmt(row_['Newton'])} | n=1 canon F-flat {fmt(row_['n=1|canon 9.36e-11|F-flat'])} | F-DESI {fmt(row_['n=1|canon 9.36e-11|F-DESI'])} | R-H {fmt(row_['n=1|canon 9.36e-11|R-H'])} | N 12.5 {fmt(row_['route N|12.5'])}")
k4 = all(min(v[i] for kk, v in d.items()) >= d["Newton"][i] - 1e-9 for d in B["forward"].values() for i in range(len(RG)))
check("K4b every reading >= Newton at every R", k4)
P("\nInverse: alpha_CO,req at the measured V_c (canonical, S1, lg M* 11.31 unless stated; FLOOR = stars alone exceed); kernels n=1")
VG = (300, 350, 400, 450, 500, 550, 600); RI = (2, 3, 4)
def alpha_of(x): return None if x is None else 10 ** x / LP10
for lms in LMS:
    for sh in RE:
        kk = f"lgM*{lms}|{sh}"; B["inverse"][kk] = {}
        for R in RI:
            for V in VG:
                c = {}
                for kn, nu in list(KERN.items()) + [("Newton", nuN)]:
                    for fn, a00 in FOOT.items():
                        for mn, rf in RF.items():
                            x = mgas_req(float(R), float(V), 10 ** lms, RE[sh] / 1.678, Rg0, a00 * rf, nu); c[f"{kn}|{fn}|{mn}"] = dict(logMgas=x, alpha=alpha_of(x))
                for l in LM200:
                    x = mgas_N(float(R), float(V), 10 ** lms, RE[sh] / 1.678, Rg0, l, Z); c[f"route N|{l}"] = dict(logMgas=x, alpha=alpha_of(x))
                B["inverse"][kk][f"{R}|{V}"] = c
sa = lambda a: "FLOOR" if a is None else f"{a:.2f}"
for lms, sh in ((11.31, "S1"), (11.11, "S1"), (11.31, "S2"), (11.11, "S2")):
    P(f"-- lg M* {lms}, {sh}: R | V | n=1 canon F-flat, F-DESI, R-H | Newton | route N 12.5")
    for R in RI:
        for V in VG:
            c = B["inverse"][f"lgM*{lms}|{sh}"][f"{R}|{V}"]
            P(f"{R} {V} | {sa(c['n=1|canon 9.36e-11|F-flat']['alpha'])} {sa(c['n=1|canon 9.36e-11|F-DESI']['alpha'])} {sa(c['n=1|canon 9.36e-11|R-H']['alpha'])} | {sa(c['Newton|canon 9.36e-11|F-flat']['alpha'])} | {sa(c['route N|12.5']['alpha'])}")

# ---- detection forecast, U4_28473 ----
kps = scale(Z); Rdg = Rg0 / kps; q = 0.55; sg1 = lambda dv: SIG["B"] * 10 * math.sqrt(dv / 10) / 1e3
Ib = lambda R: F32 * O_B / (2 * math.pi * Rdg ** 2 * q) * math.exp(-R / Rg0); beamk = BEAM * kps
DF = {}
for R in (0.5, 1, 1.5, 2, 3, 4, 5, 6):
    nr = max(1.0, 2 * math.pi * R / beamk); fr_ring = 1.0
    DF[str(R)] = dict(SN_beam_100=Ib(R) / sg1(100), SN_ring_100=Ib(R) / sg1(100) * math.sqrt(nr))
Rmax = Rg0 * math.log(Ib(0) / (3 * sg1(100))); Rring = brentq(lambda R: Ib(R) / sg1(100) * math.sqrt(max(1.0, 2 * math.pi * R / beamk)) - 3, 0.1, 30)
nb = math.pi * 1.0 ** 2 / O_B; SNint = F32 / (sg1(800) * math.sqrt(nb))
B["forecast"] = dict(per_R=DF, Rmax_beam=Rmax, Rmax_ring=Rring, SN_1as_aperture_800=SNint, beam_kpc=beamk, peak_SN_100=Ib(0) / sg1(100))
P(f"\nForecast U4_28473, CO(3-2), exponential R_e 1.56 kpc, q {q}: beam {beamk:.2f} kpc; peak S/N per beam per 100 km/s {Ib(0) / sg1(100):.1f}; 3 sigma per beam to R {Rmax:.2f} kpc; 3 sigma azimuthal ring to R {Rring:.2f} kpc; 1\" radius aperture over 800 km/s S/N {SNint:.1f}")
P("  " + "; ".join(f"R {k}: beam {v['SN_beam_100']:.2f}, ring {v['SN_ring_100']:.2f}" for k, v in DF.items()))
SCAN = {}
for rap in (0.10, 0.15, 0.25, 0.50, 1.00):
    x = rap * kps / Rg0; SCAN[str(rap)] = (1 - (1 + x) * math.exp(-x)) * F32 / (sg1(1000) * math.sqrt(max(1.0, math.pi * rap ** 2 / O_B)))
S3D = math.sqrt(sum((Ib(r) / sg1(100)) ** 2 * 2 * math.pi * r * 0.05 / (1.133 * beamk ** 2) * q for r in np.arange(0.025, 12, 0.05)))
B["forecast"].update(moment0_aperture_SN_1000=SCAN, matched_3D_SN=S3D)
P("moment-0 aperture S/N, +-500 km/s window, radius [arcsec]: " + "; ".join(f"{k}: {v:.2f}" for k, v in SCAN.items()) + f"; rotation-matched 3D S/N (100 km/s per beam) {S3D:.1f}")
HA = {}
for lms in LMS:
    for sh in RE:
        HA[f"lgM*{lms}|{sh}"] = {f"{kn}|{mn}": sa(alpha_of(mgas_req(3.0, 430.0, 10 ** lms, RE[sh] / 1.678, Rg0, FOOT["canon 9.36e-11"] * RF[mn], nu))) for kn, nu in (("n=1", nu1), ("Newton", nuN)) for mn in ("F-flat", "F-DESI", "R-H")}
B["halpha_430_at_3kpc_information"] = HA
P("information, added after criteria: alpha_CO,req at V_c 430 (repo's low-S/N Halpha fit), R 3 kpc, canon, n=1 F-flat: " + "; ".join(f"{k} {v['n=1|F-flat']}" for k, v in HA.items()))
RES["B"] = B

# ---- v3 AQUAL disc ----
sys.path.insert(0, os.path.join(REB, "S3_v3_mw_seals")); import s3_alma as SA; S3 = SA.S
seal = json.load(open(SEALS["S3"][0])); cell = seal["U4_27928"]["250"]["canon 9.36e-11|F-DESI"]
Dt = SA.Disc(RdA); lmgt = cell["logMgas_Rg=Rd"]; Ct, _ = Dt.C_at(RA_, 10 ** 10.74, 10 ** lmgt, RdA, FOOT["canon 9.36e-11"] * ns["r_desi"](ZA)); Csl = cell["C_final"]["Rg=Rd"]
check("K6 S3 solver reproduces a sealed U4 C within 1e-3", abs(Ct - Csl) < 1e-3, f"{Ct:.5f} against {Csl:.5f}")
AQ = {}; Dq = SA.Disc(RE["S1"] / 1.678)
for fn, a00 in FOOT.items():
    for mn in ("F-flat", "F-DESI", "R-H"):
        for a in AL:
            a0 = a00 * RF[mn]; rho = 10 ** 11.31 * Dq.rs1 + a * LP10 * Dq.gas_rho(Rg0); g = Dq.g; M = S3.total_mass(g, rho); A0_ = a0 / U
            PBN = S3.bc_newton(g, M); PhiN = g.newton(rho, PBN); Phi, _ = g.aqual(rho, A0_, S3.bc_aqual_iso(g, M, A0_), Phi_init_N=PhiN, PB_N=PBN)
            rr = np.array(RG, float); gA = g.gR_plane(Phi, rr); gN = g.gR_plane(PhiN, rr)
            AQ[f"{fn}|{mn}|alpha{a}"] = dict(V=[float(math.sqrt(x * r)) for x, r in zip(gA, rr)], C=[float(x / (float(nu1(y / A0_)) * y)) for x, y in zip(gA, gN)], VN_grid=[float(math.sqrt(x * r)) for x, r in zip(gN, rr)])
            P(f"AQUAL lg M* 11.31 S1 {fn} {mn} alpha {a}: V " + "/".join(f"{x:.0f}" for x in AQ[f"{fn}|{mn}|alpha{a}"]["V"]) + "  C " + "/".join(f"{x:.3f}" for x in AQ[f"{fn}|{mn}|alpha{a}"]["C"]))
RES["B"]["aqual"] = AQ

RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, f"ac1{TAG}_results.json"), "w"), indent=0, default=str)
P("\nchecks: " + ", ".join(f"{n.split()[0]} {'PASS' if o else 'FAIL'}" for n, o in CHK))
open(os.path.join(HERE, f"ac1_predict{TAG}.out"), "w").write("\n".join(OUT) + "\n")
bad = [n for n, o in CHK if not o]
if MUT:
    bit = any(n.startswith("K7") for n in bad); P(f"MUTATE R31 x 10: K7 {'bites (exit 1)' if bit else 'DOES NOT BITE'}"); open(os.path.join(HERE, f"ac1_predict{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if bit else 0)
sys.exit(1 if bad else 0)
