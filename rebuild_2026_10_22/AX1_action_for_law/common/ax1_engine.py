#!/usr/bin/env python3
"""AX1 engine: static-limit gates for the AX1 action classes. See common/FROZEN_CRITERIA.md and <class>/FROZEN_CRITERIA.md.

    OMP_NUM_THREADS=1 python3 -I ax1_engine.py CLASS [--mutate] [--tag TAG]

CLASS in BIMOND, AeST, khronon, nonlocal, v3s. Writes <class>/ax1_<class><TAG>[_MUTATE].{json,out}.
kappa = 1/2 FITTED; footings never pooled; not theory closed. Literature entries are PROVISIONAL."""
import json, math, os, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
np.seterr(all="ignore")  # macOS Accelerate matmul emits spurious FP warnings; K1-K3 guard the numbers
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANE = os.path.dirname(HERE); ROOT = os.path.normpath(os.path.join(LANE, "../.."))
CLS = sys.argv[1]; MUT = "--mutate" in sys.argv
TAG = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""
OUT, RES, FAILS = [], {"class": CLS, "mutate": MUT}, []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = bool(ok)
    if not ok: FAILS.append(name)

GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT_D7C = {"canonical": 9.36e-11, "alt": 1.13e-10}
HEES, PARK, SAT_BOUND, A_SAT = 9.0e-27, 5.2e-27, 7.0e-15, 9.5826 * AU
GNE_E0, GE_KIN = 6.913e-11, {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}
YT = 66.3803; BETAS = [2.5, 3.0, 4.0, 5.0, 6.0]
def J(p): return json.load(open(os.path.join(ROOT, p)))
D7C = J("doors_push_2026_10_22/D7c_q2_rar_gate/d7c_q2_rar_gate_results.json")
E2 = J("doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json")

# A = nu - 1, written stably
def A_law(y): y = np.maximum(np.asarray(y, float), 1e-300); return (2.0 / y) / (np.sqrt(1.0 + 4.0 / y) + 1.0)
def A_fix(y): y = np.maximum(np.asarray(y, float), 1e-300); return A_law(y) / (1.0 + (y / YT) ** 2)
def A_beta(b): return lambda y: np.expm1(np.log1p(np.maximum(np.asarray(y, float), 1e-300) ** (-b)) / (2.0 * b))
CANDS = {"law": A_law, "law+turnoff": A_fix, **{f"beta={b:g}": A_beta(b) for b in BETAS}}
D7KEY = {"law": "L", **{f"beta={b:g}": f"beta={b:g}" for b in BETAS}}
if MUT: CANDS = {k: (lambda y: np.zeros_like(np.asarray(y, float))) for k in CANDS}

def q_int(A, eta, nr=20000, nm=200, rmin=1e-7, rmax=1e5):
    u = np.linspace(math.log(rmin), math.log(rmax), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm)
    g = (1.0 / r ** 2)[:, None]; M = mu[None, :]
    a = A(np.sqrt(eta * eta + g * g + 2 * eta * g * M))
    f = (a * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w
    return 1.5 * float(np.trapz(f / r, u))
def eta_of(A, a0, E):
    if E == "E0": return GNE_E0 / a0
    t = GE_KIN[E] / a0; return brentq(lambda x: x * (1.0 + float(A(np.array([x]))[0])) - t, 1e-8, t)
def Q2(A, a0, E, **kw):
    rM = math.sqrt(GM / a0); return abs(q_int(A, eta_of(A, a0, E), **kw)) * 1.5 * a0 / rM
EFS = ["E0", "E1", "E2", "E3"]

# ---- checks
P(f"AX1 engine, class {CLS}{' MUTATE' if MUT else ''}. kappa = 1/2 FITTED; footings never pooled.")
rel = []
for foot, a0 in FOOT_D7C.items():
    for E in EFS:
        ref = D7C["Q2"]["L"][foot]["Q2"][E]; v = Q2(CANDS["law"], a0, E); rel.append(abs(v / ref - 1))
check("K1", max(rel) <= 1e-2, f"law QUMOND Q2 vs D7c 'L' (PAPER58 QUMOND), 8 cells, max rel {max(rel):.2e} (<= 1e-2)")
rel2 = []
for b in BETAS:
    k = f"beta={b:g}"
    for foot, a0 in FOOT_D7C.items():
        for E in EFS:
            ref = D7C["Q2"][k][foot]["Q2"][E]; rel2.append(abs(Q2(CANDS[k], a0, E) / ref - 1))
check("K2", max(rel2) <= 1e-2, f"beta members vs D7c, 40 cells, max rel {max(rel2):.2e} (<= 1e-2)")
if not MUT:
    k3 = max(abs(Q2(A_law, FOOT["canonical"], E, nr=40000, nm=400) / Q2(A_law, FOOT["canonical"], E) - 1) for E in ("E0", "E3"))
    check("K3", k3 <= 1e-3, f"grid doubling, law canonical E0/E3, max change {k3:.2e} (<= 1e-3)")
    gN = GM / A_SAT ** 2; a0 = FOOT["canonical"]; k4 = abs(gN * (1 + float(A_law(np.array([gN / a0]))[0])) / (gN / 2 + math.sqrt(gN * gN / 4 + a0 * gN)) - 1)
    check("K4", k4 <= 1e-12, f"spherical identity at Saturn, rel {k4:.1e} (<= 1e-12)")
RES["K1_max_rel"], RES["K2_max_rel"] = max(rel), max(rel2)

# ---- static grades for every candidate, both footings
STAT = {}
for foot, a0 in FOOT.items():
    for name, A in CANDS.items():
        qs = {E: Q2(A, a0, E) for E in EFS}; gN = GM / A_SAT ** 2; dg = gN * float(A(np.array([gN / a0]))[0])
        if name in D7KEY and D7KEY[name] != "L":
            s = D7C["SPARC"][foot][D7KEY[name]]; g1 = dict(z_vs_law=s["vs"]["L"]["z"], pass_=s["vs"]["L"]["z"] >= -2, d7c_label=s["SPARC"], d7c_worst_z=s["worst_z"], S1=s["S1_reading"])
        else: g1 = dict(z_vs_law=None, pass_=True, note="identity: the class's static function is the law (turn-off acts at y > 60)")
        aq = None
        if name == "law": aq = E2["R1"][f"{foot}|none"]["over_Hees"]
        elif name == "law+turnoff": aq = E2["R1"][f"{foot}|66.3803"]["over_Hees"]
        elif name in E2["R3"]: aq = E2["R3"][name][foot]["over_Hees"]
        STAT[f"{foot}|{name}"] = dict(Q2_QUMOND=qs, over_Hees_QUMOND=[qs[E] / HEES for E in EFS], over_Park_QUMOND=[qs[E] / PARK for E in EFS],
            pass_Q2_QUMOND=all(qs[E] <= HEES for E in EFS), over_Hees_AQUAL_E2=aq, pass_Q2_AQUAL=(None if aq is None else all(x <= 1 for x in aq)),
            Saturn_dg=dg, Saturn_over_bound=dg / SAT_BOUND, pass_mono=dg <= SAT_BOUND, G1=g1)
RES["static"] = STAT

def fmt(xs): return "[" + ", ".join(f"{x:.3f}" for x in xs) + "]"
P("\nStatic grades (Q2 / Hees 2-sigma at E0..E3; Saturn monopole / 7.0e-15; G1 = D7c z vs the law)")
for k, s in STAT.items():
    aq = "n/a" if s["over_Hees_AQUAL_E2"] is None else fmt(s["over_Hees_AQUAL_E2"])
    z = s["G1"]["z_vs_law"]; P(f"  {k:24s} QUMOND {fmt(s['over_Hees_QUMOND'])} {'P' if s['pass_Q2_QUMOND'] else 'F'} | AQUAL(E2) {aq} | Saturn {s['Saturn_over_bound']:.3g}x {'P' if s['pass_mono'] else 'F'} | G1 {'identity' if z is None else f'{z:+.2f}'} {'P' if s['G1']['pass_'] else 'F'}")

# ---- class entries (PROVISIONAL literature, record lanes), fixed in each class's FROZEN_CRITERIA
CLASSES = {
 "BIMOND": dict(type="QUMOND", G2c=("P", "gamma = 1, alpha1 = alpha2 = 0 at high acceleration [PROVISIONAL, memory; not derived]"),
                G3=("P", "one metric for matter and light, Phi = Psi [PROVISIONAL, memory]"),
                G4=("F", "Chesler & Loeb 2017, arXiv:1704.05116: BIMOND 'in its present form is not an acceptable theory' [PROVISIONAL, web snippet, argument not read]")),
 "AeST": dict(type="AQUAL", G2c=("F", "record AS3 (9581518967/6770f2d8ad): with a sound speed the static branch is real, alpha1 = -22/5, alpha2 = 11/2 (bounds 1e-4, 2.4e-7); with none, a moving source gives alpha1 = alpha2 = 0 but the law is lost for moving systems"),
              G3=("P", "Skordis & Zlosnik 2021: lensing as GR with the MOND potential [PROVISIONAL, memory]"),
              G4=("O", "c_T = c by construction [PROVISIONAL, memory]; record X6 (fd303cac8b/fbcce8f612) lists 'AeST's sector fails ... health (H1)', scope not re-read here")),
 "khronon": dict(type="AQUAL", G2c=("O", "PPN = GR except alpha1, alpha2 (Bonetti & Barausse 2015, arXiv:1502.05554) [PROVISIONAL]; record X15 (87867a70a4/11f2dceb59): static unscreened branch alpha1 = -4 eta = -8, alpha2 8.7e3-1.5e7, reported as not PPN; A22 script: alpha1 = alpha2 = 0 at beta = 0 (moving source). Branches conflict; not settled"),
                 G3=("P", "Blanchet & Marsat 2011, arXiv:1107.5264: same lensing as GR [PROVISIONAL, snippet]"),
                 G4=("O", "khronometric c_T^2 = 1/(1 - beta_kh), beta_kh = 0 allowed [PROVISIONAL, memory]; record C5 (f002ce909a/f3e7d4d661): conditionally healthy only in C4's literal form; H4 saddle growth in the literal form")),
 "nonlocal": dict(type="both", G2c=("P", "GR 'in the solar-system regime' by construction (Deffayet, Esposito-Farese & Woodard 2011, arXiv:1106.4984) [PROVISIONAL, snippet]"),
                  G3=("P", "built to give enough lensing (DEW 2011) [PROVISIONAL, snippet]"),
                  G4=("O", "no GW170817 or ghost analysis found (web search 2026-11-04) [PROVISIONAL]")),
 "v3s": dict(type="screened", G2c=("P", "record X15 / A22: alpha1 = alpha2 = 0 at beta = 0; gamma = 1 (X15)"),
             G3=("P", "record V3S verdict: lensing bound S4 mu_K < 0.1 /Mpc holds isolated-galaxy lensing at the law"),
             G4=("P", "record C8 (f2399aaf5e/aa113a5e96): c_T = c, Dv/c <= 6e-32; C5 conditionally healthy; X3 switched stiffness well-posed. Caustics generic (X14) are a structural gap, not a ghost or gradient instability")),
}
C = CLASSES[CLS]; RES["entries"] = {k: C[k] for k in ("type", "G2c", "G3", "G4")}
P(f"\nClass {CLS}: static type {C['type']}. G2c {C['G2c'][0]}: {C['G2c'][1]}\n  G3 {C['G3'][0]}: {C['G3'][1]}\n  G4 {C['G4'][0]}: {C['G4'][1]}")

EXTRA = {}
if CLS == "BIMOND" and not MUT:
    import sympy as sp
    al, be = sp.symbols("alpha beta", positive=True); A_ = al / (al + be); B_ = A_ - 1
    cross = sp.simplify(be * A_ + al * B_); kd = sp.simplify(be * A_ ** 2 + al * B_ ** 2)
    tot = sp.simplify(1 / (al + be) + A_ ** 2 / kd); share = sp.simplify((A_ ** 2 / kd) / tot)
    check("B1", cross == 0 and sp.simplify(tot - 1 / be) == 0 and sp.simplify(share - al / (al + be)) == 0, f"flat split: cross {cross}, k_delta {kd}, h response {tot}, delta share {share}")
    c = 2.99792458e8; gw = {"GW150914": (1e-21, 150.0), "GW170817": (1e-22, 300.0)}
    EXTRA["gw_gradient_over_a0"] = {k: {f: 2 * math.pi * fr * h * c / a0 for f, a0 in FOOT.items()} for k, (h, fr) in gw.items()}
    P("  ARGUED (reported): wave gradient acceleration 2 pi f h c / a0: " + "; ".join(f"{k} {v['canonical']:.2f} / {v['alt']:.2f}" for k, v in EXTRA["gw_gradient_over_a0"].items()))
if CLS == "AeST" and not MUT:
    for muK in (0.1, 1.0):
        EXTRA[f"(muK r_M)^2 at muK {muK}/Mpc"] = {f: (muK / (1e6 * PC) * math.sqrt(GM / a0)) ** 2 for f, a0 in FOOT.items()}
    EXTRA["capture/MOND radius = (v_f/w)^2"] = {f"v_f {vf}, w {w}": (vf / w) ** 2 for vf in (50, 100, 200) for w in (300, 370)}
    P("  mass-term screening at r_M, (mu_K r_M)^2: " + str({k: {f: f"{x:.1e}" for f, x in v.items()} for k, v in EXTRA.items() if k.startswith("(")}))
    P("  AS3 capture radius GM/w^2 over the MOND radius sqrt(GM/a0) = (v_flat/w)^2: " + str({k: round(v, 3) for k, v in EXTRA["capture/MOND radius = (v_f/w)^2"].items()}))
if CLS == "v3s" and not MUT:
    C6 = J("covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini_results.json")
    rp = {k: v for k, v in C6["R1_physical"].items()}; EXTRA["C6_R1_margin"] = C6["R1_margin"]
    bounds = {"Earth": 8.7e-15, "Mars": 1.4e-15, "Saturn": 7.0e-15}; hh = {}
    for L in (24, 50, 90):
        a = GM / (L * PC) ** 2; hh[L] = {p: a / b for p, b in bounds.items()}
    EXTRA["hedgehog_GM_over_Lstar2_over_bound"] = hh
    rel = abs(hh[24]["Mars"] / 0.173 - 1)
    check("V1", rel <= 0.02, f"hedgehog GM/L*^2 at 24 pc: Mars {hh[24]['Mars']:.3f} of bound vs C6's 0.173, rel {rel:.2e} (<= 2e-2)")
    q2max = max(v["Q2"] if isinstance(v, dict) and "Q2" in v else 0 for v in rp.values()) if all(isinstance(v, dict) for v in rp.values()) else None
    EXTRA["C6_Q2_max"] = q2max
    P(f"  C6 screened Q2 (read): margins {C6['R1_margin']}; max Q2 over 24 cells {q2max}; C6 verdict line: {str(C6['verdict'])[:160]}")
    P("  hedgehog GM/L*^2 / bound: " + "; ".join(f"{L} pc " + ", ".join(f"{p} {x:.3f}" for p, x in v.items()) for L, v in hh.items()))
RES["extra"] = EXTRA

# ---- labels per footing
def lab(foot):
    surv, why = [], {}
    for name in CANDS:
        s = STAT[f"{foot}|{name}"]
        if C["type"] == "screened":
            m = EXTRA.get("C6_R1_margin", {}); ok2a = bool(m) and m.get("Hees_min", 0) > 1
            ok2b = all(x <= 1 for v in EXTRA.get("hedgehog_GM_over_Lstar2_over_bound", {}).values() for x in v.values())
            g = dict(G1=s["G1"]["pass_"], G2a=ok2a, G2b=ok2b)
        elif C["type"] == "both":  # static form not fixed by the published reduction: survives if it passes under either form
            g = dict(G1=s["G1"]["pass_"], G2a=s["pass_Q2_QUMOND"] or bool(s["pass_Q2_AQUAL"]), G2b=s["pass_mono"])
        else:
            g = dict(G1=s["G1"]["pass_"], G2a=s["pass_Q2_QUMOND"] if C["type"] == "QUMOND" else bool(s["pass_Q2_AQUAL"]), G2b=s["pass_mono"])
        g["G2c"] = C["G2c"][0] != "F"
        bad = [k for k, v in g.items() if not v]; why[name] = bad
        if not bad: surv.append(name)
        if C["type"] == "screened": break
    ent = {k: C[k][0] for k in ("G3", "G4")}
    if not surv: return "FAIL [" + ", ".join(sorted({x for v in why.values() for x in v})) + " for every candidate]", surv, why
    if "F" in ent.values(): return "FAIL [" + ", ".join(k for k, v in ent.items() if v == "F") + "]", surv, why
    if "O" in ent.values(): return "OPEN [" + ", ".join(k for k, v in ent.items() if v == "O") + "]", surv, why
    return "PASS", surv, why
P("\nLabels")
RES["labels"] = {}
for foot in FOOT:
    L, surv, why = lab(foot); RES["labels"][foot] = dict(label=L, survivors=surv, fails=why)
    P(f"  {foot}: {L}; candidates surviving G1-G2: {surv or 'none'}; per-candidate failed gates: " + "; ".join(f"{k} {v}" for k, v in why.items() if v))
if MUT: check("M1", "K1" in FAILS and all(all(x == 0 for x in s["Q2_QUMOND"].values()) for s in STAT.values()), "MUTATE bites: K1 fails and every Q2 is 0")
RES["failed_checks"] = FAILS
sfx = TAG + ("_MUTATE" if MUT else "")
od = os.path.join(LANE, CLS); open(os.path.join(od, f"ax1_{CLS}{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(od, f"ax1_{CLS}{sfx}.json"), "w"), indent=1, sort_keys=True, default=str)
sys.exit(1 if MUT or FAILS else 0)
