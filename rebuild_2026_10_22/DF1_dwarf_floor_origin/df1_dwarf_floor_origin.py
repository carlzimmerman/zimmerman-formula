#!/usr/bin/env python3
"""DF1_dwarf_floor_origin: named-physics origins of the faint-dwarf extra, graded on X1's 82 dwarfs.

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (3ef24ec383, committed alone; POST-HOC disclosed). Reads X1's
per-system CSV, X24/X28's JSON and CFG257's binary table, read-only. One thread, minutes.

    python3 df1_dwarf_floor_origin.py                 -> .out, _results.json
    DF1_MUTATE=1 python3 df1_dwarf_floor_origin.py    -> r12 permuted in the g_x term (K0 must fail), _MUTATE outputs
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize_scalar, minimize, brentq

T0 = time.time()
MUTATE = os.environ.get("DF1_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

G, PC, MSUN = 6.674e-11, 3.0857e16, 1.989e30
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
H = ("MW ultra-faint", "bright M31", "M31 others")
GRADED = H + ("MW classical",)
REPORT = ("indiv:Crater II", "indiv:Antlia II")
SEED, NBOOT = 20261024, 10000
K0_N = {"canonical": (0.78, 0.73, 0.83), "alt": (0.80, 0.75, 0.85)}
CAND = {  # name: (n, m, label)
    "P0": (0.0, 0.0, "Gamma=0 Chaplygin/logatrope (Burgers form)"),
    "P1": (1.0, 0.0, "Gamma=1 isothermal (X24 floor form)"),
    "P4/3": (2.0, 0.0, "Gamma=4/3"),
    "P5/3": (5.0, 0.0, "Gamma=5/3 adiabatic"),
    "TK": (1.0 / 3.0, 0.0, "Kolmogorov cascade"),
    "SI": (1.25, 0.75, "secondary infall on the baryon seed"),
}
X24 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X24_dwarf_velocity_floor", "x24_dwarf_velocity_floor_results.json")))
X28 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "X28_dwarf_floor_form", "x28_dwarf_floor_form_results.json")))
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping",
                                            "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))

def s_of_nu(nu):                       # local slope d ln g_law / d ln g_bar of the simple nu, at the y where nu(y) = nu
    if nu <= 1.0 + 1e-9:
        return 1.0
    y = 1.0 / (nu * (nu - 1.0))
    return 1.0 - 1.0 / (2.0 * y * nu * (nu - 0.5))

def load(foot, classes):               # X28's load(), plus M*, the law boost and the slope s
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in classes:
            continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; E = float(r["Delta[iso AQUAL L*0]"])
        siso = sc * 10 ** (-E / 2); r12 = 4.0 / 3.0 * float(r["rh_pc"]) * PC
        nu = 10 ** (float(r["Delta[Newton]"]) - E)
        out.append(dict(name=r["name"], cls=r["cls"], E=E, s=float(r["sdMC[iso AQUAL L*0]"]), r12=r12, r12x=r12,
                        giso=3 * (siso * 1e3) ** 2 / r12, Ms=10 ** float(r["logMstar"]), nu=nu, sl=s_of_nu(nu)))
    return out

def arr(R, k):
    return np.array([q[k] for q in R])
def ep_pl(R, logA, n, m, a0):          # power-law candidate, g_x = A a0 (r/100pc)^-n (M*/1e5)^m
    gx = 10 ** logA * a0 * (arr(R, "r12x") / (100 * PC)) ** (-n) * (arr(R, "Ms") / 1e5) ** m
    return np.log10(1 + gx / arr(R, "giso"))
def ep_imf(R, F):
    return arr(R, "sl") * np.log10(F)
def chi2(R, ep):
    return float(np.sum(((arr(R, "E") - ep) / arr(R, "s")) ** 2))
def fit_pl(R, n, m, a0):
    r = minimize_scalar(lambda la: chi2(R, ep_pl(R, la, n, m, a0)), bounds=(-12.0, 6.0), method="bounded",
                        options={"xatol": 1e-5})
    return float(r.x), float(r.fun)
def fit_imf(R):
    r = minimize_scalar(lambda F: chi2(R, ep_imf(R, F)), bounds=(1.0, 1000.0), method="bounded", options={"xatol": 1e-6})
    return float(r.x), float(r.fun)
def boot_med(x, s, rng):
    N = len(x); ix = rng.integers(0, N, (NBOOT, N))
    return float(np.median(x)), float(np.std(np.median(x[ix] + s[ix] * rng.standard_normal((NBOOT, N)), axis=1)))

def x28_k0(R, a0):                     # X28's own m = 0 power-law method, verbatim in substance
    def ep_n(amp, n):
        return np.log10(1 + amp * a0 * (arr(R, "r12x") / (100 * PC)) ** (-n) / arr(R, "giso"))
    ns = np.linspace(-0.5, 1.5, 201)
    prof = np.array([minimize_scalar(lambda A: chi2(R, ep_n(A, n)), bounds=(0.0, 5.0), method="bounded").fun for n in ns])
    inside = ns[prof - prof.min() <= 1.0]
    return float(ns[np.argmin(prof)]), float(inside.min()), float(inside.max())

def t1_reference(R, a0):
    ns = np.arange(-1.0, 6.0 + 1e-9, 0.02); ms = np.arange(-1.0, 1.5 + 1e-9, 0.02)
    best = (1e99, None)
    prof_m0 = []
    for n in ns:
        for m in ms:
            la, c = fit_pl(R, n, m, a0)
            if c < best[0]:
                best = (c, (n, m, la))
        prof_m0.append(fit_pl(R, n, 0.0, a0)[1])
    n0, m0, la0 = best[1]
    pol = minimize(lambda p: chi2(R, ep_pl(R, p[2], p[0], p[1], a0)), [n0, m0, la0], method="Nelder-Mead",
                   options={"xatol": 1e-5, "fatol": 1e-7, "maxiter": 4000})
    cref = min(best[0], float(pol.fun)); nb, mb, lab = (pol.x if pol.fun < best[0] else best[1])
    prof_m0 = np.array(prof_m0); pm = prof_m0.min()
    i1 = ns[prof_m0 - pm <= 1.0]; i4 = ns[prof_m0 - pm <= 4.0]
    return dict(chi2_ref=cref, n_best=float(nb), m_best=float(mb), logA_best=float(lab),
                m0=dict(n=float(ns[np.argmin(prof_m0)]), n68=[float(i1.min()), float(i1.max())],
                        n95=[float(i4.min()), float(i4.max())], chi2=float(pm)))

def sparc_points(a0):
    pts = []
    for V, Rk in ((30.0, 2.0), (100.0, 10.0)):
        gobs = (V * 1e3) ** 2 / (Rk * 1e3 * PC); x = gobs / a0; y = x * x / (1 + x)
        nu = 0.5 + math.sqrt(0.25 + 1 / y)
        pts.append(dict(V=V, R=Rk * 1e3 * PC, gobs=gobs, M=(V * 1e3) ** 4 / (G * a0) / MSUN, sl=s_of_nu(nu)))
    return pts

P(f"DF1_dwarf_floor_origin  {'MUTATE run (r12 permuted in the g_x term)' if MUTATE else 'normal run'}  [POST-HOC, disclosed]")
P("kappa = 1/2 FITTED; footings never pooled; shapes fixed by named physics, one normalization calibrated on LG field; "
  "no DM particle; not theory closed")
RES = dict(frozen="3ef24ec383", mutate=MUTATE, footings={}); checks = []
for f in FOOTS:
    a0 = A0[f]; rng = np.random.default_rng(SEED)
    FLD = load(f, ("LG field",)); GR = load(f, GRADED); ALL = GR + FLD; RH = [q for q in GR if q["cls"] in H]
    REP = load(f, REPORT)
    if MUTATE:
        perm = np.random.default_rng(20261025).permutation(len(ALL)); rx = [ALL[i]["r12"] for i in perm]
        for q, v in zip(ALL, rx):
            q["r12x"] = v
    FR = RES["footings"][f] = dict(N_all=len(ALL), N_field=len(FLD), N_H=len(RH))
    P(f"\n=== [{f}]  a0 {a0:.4e}   N: field {len(FLD)}, H {len(RH)}, ALL {len(ALL)}")
    # K0
    nk = x28_k0(ALL, a0); la1, _ = fit_pl(FLD, 1.0, 0.0, a0)
    c0 = math.sqrt(10 ** la1 * a0 * 100 * PC / 3) / 1e3; c0x = X24["footings"][f]["B"]["c0"]
    k0 = all(abs(a - b) <= 0.011 for a, b in zip(nk, K0_N[f])) and abs(c0 - c0x) < 0.01
    P(f"  K0 X28 m=0 method: n {nk[0]:.2f} [{nk[1]:.2f}, {nk[2]:.2f}] vs {K0_N[f]};  P1 field c0 {c0:.3f} vs X24 {c0x:.3f}: "
      f"{'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{f}]", k0))
    # T1 reference
    ref = t1_reference(ALL, a0); FR["T1_reference"] = ref
    P(f"  T1 reference (free n, m on ALL): chi2 {ref['chi2_ref']:.2f} at n {ref['n_best']:+.3f}, m {ref['m_best']:+.3f}; "
      f"m=0: n {ref['m0']['n']:.2f}, 68% {ref['m0']['n68']}, 95% {ref['m0']['n95']}")
    gd = [2 * v / (1 + v) for v in (ref["m0"]["n"],) + tuple(ref["m0"]["n95"])]
    P(f"  Gamma_data = 2n/(1+n) (m = 0): {gd[0]:.3f}, 95% [{gd[1]:.3f}, {gd[2]:.3f}]  (named EOS: 0, 1, 4/3, 5/3)")
    FR["Gamma_data"] = gd
    law_H = chi2(RH, np.zeros(len(RH)))
    sp = sparc_points(a0)
    FR["cands"] = {}
    k3 = True
    for name in list(CAND) + ["IMF"]:
        C = FR["cands"][name] = {}
        if name == "IMF":
            Fa, cc = fit_imf(ALL); Ff, _ = fit_imf(FLD)
            epf = lambda R: ep_imf(R, Ff); C["F_all"], C["F_field"] = Fa, Ff; lab = "remnant-loaded IMF"
        else:
            n, m, lab = CAND[name]
            _, cc = fit_pl(ALL, n, m, a0); laf, _ = fit_pl(FLD, n, m, a0)
            epf = (lambda la, n, m: (lambda R: ep_pl(R, la, n, m, a0)))(laf, n, m); C["logA_field"] = laf
            k3 = k3 and ref["chi2_ref"] <= cc + 1e-6
        dsh = cc - ref["chi2_ref"]; t1 = dsh <= 5.99
        C.update(label=lab, chi2_all=cc, dchi2_shape=dsh, T1=t1)
        # T2
        cls = {}
        for c in GRADED:
            Rc = [q for q in GR if q["cls"] == c]; res = arr(Rc, "E") - epf(Rc); md, sd = boot_med(res, arr(Rc, "s"), rng)
            cls[c] = dict(N=len(Rc), median=md, sd=sd, Z=md / sd)
        chH = chi2(RH, epf(RH)); t2 = all(abs(cls[c]["Z"]) < 2 for c in H) and chH < law_H
        C.update(classes=cls, chi2_H=chH, T2=t2)
        # T3
        t3 = "NA"; t3info = ""
        if name == "P0":
            gx = 10 ** C["logA_field"] * a0; Cc = gx ** 2 / (6 * math.pi * G)
            h = 0.6856; rho_c = 0.3085 * 5.364 / 6.364 * 1.8785e-26 * h * h * (1 + 3) ** 3 * 10
            cs = math.sqrt(Cc / rho_c) / 1e3; t3 = "VIOLATED" if cs > 13.0 else "PASS"
            t3info = f"g_x {gx:.3e} m/s^2 = {gx / a0:.4f} a0; forest c_s(z=3, delta=10) = {cs:.1f} km/s vs gate 13"
            C["cs_forest"] = cs
        elif name in ("P1", "P4/3", "P5/3"):
            t3 = "PASS"
            if name == "P1":
                cf = math.sqrt(10 ** C["logA_field"] * a0 * 100 * PC / 3) / 1e3
                t3info = f"c0 {cf:.2f} km/s vs forest gate 6-13 (Gamma >= 1: c_s at forest <= dwarf value)"
            else:
                t3info = "Gamma > 1: c_s at forest densities below its dwarf value"
        elif name == "IMF":
            fq = {}
            viol = False
            for c in H:
                Rc = [q for q in GR if q["cls"] == c]; Fr = 10 ** (arr(Rc, "E") / arr(Rc, "sl"))
                ix = rng.integers(0, len(Rc), (NBOOT, len(Rc)))
                Eb = arr(Rc, "E")[ix] + arr(Rc, "s")[ix] * rng.standard_normal((NBOOT, len(Rc)))
                bd = np.median(10 ** (Eb / arr(Rc, "sl")[ix]), axis=1)
                fq[c] = dict(median=float(np.median(Fr)), sd=float(np.std(bd)), s_med=float(np.median(arr(Rc, "sl"))))
                viol = viol or (fq[c]["median"] - 2.0 > 2 * fq[c]["sd"])
            t3 = "VIOLATED" if viol else "PASS"; C["F_req"] = fq
            t3info = "F_req median (sd): " + "; ".join(f"{c} {v['median']:.2f} ({v['sd']:.2f}), s {v['s_med']:.2f}" for c, v in fq.items()) + " vs bound 2"
        elif name == "TK":
            sx2 = 10 ** C["logA_field"] * a0 * 100 * PC / 3; eps = sx2 ** 1.5 / (100 * PC)
            t3info = f"implied eps = sigma_x^3/r at 100 pc: {eps:.3e} W/kg (reported only)"
        elif name == "SI":
            mx = 10 ** C["logA_field"] * a0 * (100 * PC) ** 2 / G / MSUN
            t3info = f"implied M_x(<100 pc) for M* = 1e5: {mx:.3e} Msun (reported only)"
        C.update(T3=t3, T3_info=t3info)
        # T4
        dEs = []
        for p in sp:
            if name == "IMF":
                dEs.append(p["sl"] * math.log10(Ff))
            else:
                gx = 10 ** C["logA_field"] * a0 * (p["R"] / (100 * PC)) ** (-n) * (p["M"] / 1e5) ** m
                dEs.append(math.log10(1 + gx / p["gobs"]))
        t4 = max(dEs) <= 0.10; tag = max(dEs) > 0.05
        C.update(T4_dE=dEs, T4=t4, sparc_cost_tag=tag)
        # reported individuals
        C["report"] = {q["name"]: dict(E=q["E"], E_pred=float(epf([q])[0])) for q in REP}
        if t3 == "VIOLATED" or not t1:
            v = "RULED OUT"
        elif t1 and t2 and t4 and t3 in ("PASS", "NA"):
            v = "SURVIVES"
        else:
            v = "PARTIAL"
        C["verdict"] = v
        P(f"\n  [{name}] {lab}" + ("" if name == "IMF" else f"  (n {CAND[name][0]:.3f}, m {CAND[name][1]:.2f})"))
        P(f"    T1 chi2_all {cc:.2f}, dchi2_shape {dsh:+.2f} -> {'PASS' if t1 else 'FAIL'}")
        P("    T2 " + "; ".join(f"{c} {v_['median']:+.3f}+-{v_['sd']:.3f} (Z {v_['Z']:+.2f})" for c, v_ in cls.items())
          + f"; chi2_H {chH:.1f} (law {law_H:.1f}) -> {'PASS' if t2 else 'FAIL'}")
        P(f"    T3 {t3}: {t3info}")
        P(f"    T4 dE SPARC (30 km/s @ 2 kpc, 100 km/s @ 10 kpc) {dEs[0]:.3f} / {dEs[1]:.3f} -> {'PASS' if t4 else 'FAIL'}"
          f"{' [SPARC-COST]' if tag else ''}")
        P("    reported: " + "; ".join(f"{k} E {d['E']:+.2f} pred {d['E_pred']:+.2f}" for k, d in C["report"].items()))
        P(f"    VERDICT [{f}] {name}: {v}")
    checks.append((f"K1[{f}]", abs(FR["cands"]["P1"]["chi2_H"] - X28["footings"][f]["forms"]["F_v"]["chi2_H"]) < 0.1))
    checks.append((f"K3[{f}]", k3))
    # K2 positive control: synthetic E from TK at its ALL-calibrated amplitude
    laT, _ = fit_pl(ALL, 1.0 / 3.0, 0.0, a0); epT = ep_pl(ALL, laT, 1.0 / 3.0, 0.0, a0)
    syn = [dict(q) for q in ALL]; rs = np.random.default_rng(SEED + 7)
    for q, e in zip(syn, epT):
        q["E"] = float(e) + q["s"] * rs.standard_normal()
    rs_ref = t1_reference(syn, a0)
    dTK = fit_pl(syn, 1.0 / 3.0, 0.0, a0)[1] - rs_ref["chi2_ref"]; dP1 = fit_pl(syn, 1.0, 0.0, a0)[1] - rs_ref["chi2_ref"]
    k2 = dTK <= 5.99
    P(f"\n  K2 synthetic TK: dchi2_shape TK {dTK:+.2f} ({'PASS' if k2 else 'FAIL'}); power: P1 on the same data {dP1:+.2f} "
      f"({'rejected' if dP1 > 5.99 else 'not rejected'})")
    checks.append((f"K2[{f}]", k2)); FR["K2"] = dict(dchi2_TK=dTK, dchi2_P1=dP1)

V = {}
for name in list(CAND) + ["IMF"]:
    a, b = RES["footings"]["canonical"]["cands"][name]["verdict"], RES["footings"]["alt"]["cands"][name]["verdict"]
    V[name] = a if a == b else f"UNDECIDED (canonical {a}, alt {b})"
RES["verdicts"] = V
surv = [k for k, v in V.items() if v == "SURVIVES"]
RES["lane"] = ("SURVIVOR(S): " + ", ".join(surv)) if surv else "NONE SURVIVE"
P("\n=== VERDICTS (both footings)")
for k, v in V.items():
    P(f"  {k:5s} {v}")
P(f"=== LANE: {RES['lane']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K4", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; nok = sum(ok for _, ok in checks)
P(f"\nchecks {nok}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"df1_dwarf_floor_origin{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"df1_dwarf_floor_origin_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if nok == len(checks) else 1)
