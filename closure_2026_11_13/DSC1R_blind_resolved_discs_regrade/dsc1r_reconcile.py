#!/usr/bin/env python3
"""DSC1R reconcile (after blindness ended; grades nothing, relabels neither lane). Starts from DSC1R's A1 build and swaps in
DSC1's ingredients one at a time, then all together, reporting the above group's A with its 95 % interval and the below
group's chi^2 (law, baryons alone, free halo and the halo at A = 1), both footings.
  (a) pressure term   (b) baryon model and normalisation   (c) halo construction   (d) error / correlation / interval rule
  (e) point cut       (f) other: A grid 0-6 (f1), Lelli kpc/arcsec 8.69 (f2), the record's glaw kernel (f3)
DSC1R's dsc1r.py (with --A1) is executed up to its "run" marker; SRJ2's srj2_rc.py up to "json.dump(RES" (read-only, as
DSC1 and SRJ3 do).  python3 -I -B dsc1r_reconcile.py -> dsc1r_reconcile.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, io, json, math, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# ---- DSC1R A1 machinery
src = open(os.path.join(HERE, "dsc1r.py")).read()
sys.argv = ["dsc1r.py", "--A1"]
M = {"__file__": os.path.join(HERE, "dsc1r.py"), "__name__": "dsc1r_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------ run")], os.path.join(HERE, "dsc1r.py"), "exec"), M)
assert M["A1"]
# ---- SRJ2 / FRZ1 halo and the record's law kernel
SJ = os.path.join(REPO, "closure_2026_11_12", "SRJ2_regime_split_joint"); SRC = os.path.join(SJ, "srj2_rc.py"); code = open(SRC).read()
NS = {"__file__": SRC, "__name__": "srj2_rc_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("json.dump(RES")], SRC, "exec"), NS)
FR, S, zstate = NS["FR"], NS["S"], NS["zstate"]
XTAB_R, FB_R, hh_R, MPC_R = S["XTAB"], S["FB"], S["hh"], 1e3 * S["KPC"]; glaw_R = S["glaw"]; m_nfw_R = FR["m_nfw"]
from scipy.optimize import brentq
_HR = {}
def CR_record(Rm, Mb, X, z):                                    # DSC1's CR(), same code path
    key = (X, round(math.log10(Mb), 8), round(z, 6))
    if key not in _HR:
        conc, dta, omz = zstate(z); Mta = X * Mb * hh_R / (1 - FB_R); hbz = FR["halo_basics_z"]
        lM = brentq(lambda l: hbz(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
        hb = hbz(10 ** lM, conc, dta, omz); a = MPC_R / hh_R / (1 + z)
        _HR[key] = (hb["rs"] * a, hb["rta"] * a, hb["rta"] / hb["rs"])
    rs, rta, cta = _HR[key]; r = np.minimum(Rm, rta)
    return X * Mb * S["MS"] * np.array([m_nfw_R(x) for x in np.atleast_1d(r / rs)]) / m_nfw_R(cta)

G, MS, KPC, A0, T1 = M["G"], M["MS"], M["KPC"], M["A0"], M["T1"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ---- DSC1's baryons
def g_cfg401(R, g, Mb):
    z, kpa, inc, Rh, s0, bt, vc, ms, mb = T1[g]; fgas = 1 - ms / mb; Rd = Rh / 1.678; st = 1 - fgas
    gs = M["g_disc"](R, Rd, Mb * st * (1 - bt)) + G * MS * Mb * st * bt * R ** 2 / (R + 1 / 1.8153) ** 2 / (R * KPC) ** 2
    return gs + M["g_disc"](R, 2 * Rd, Mb * fgas)
L488_DSC1 = dict(Ms=5.2e10, fbul=0.63, Rbul=0.35 * 8.69, Rdisc=0.88 * 8.69, Mg=8.4e10)

def lelli488(kpa, Re_drift):
    rows = [r for r in M["LROWS"] if r["galaxy"] == "zC-488879"]
    R = np.array([float(r["radius_arcsec"]) for r in rows]) * kpa; V = np.array([float(r["vrot_kms"]) for r in rows])
    eV = np.array([0.5 * (float(r["err_lo_kms"]) + float(r["err_hi_kms"])) for r in rows])
    Vc2 = V ** 2 + 3.36 * 15.0 ** 2 * (R / Re_drift)
    return R, np.log10(Vc2 * 1e6 / (R * KPC)), M["sig_log"](V, eV, Vc2), len(R)

def build(ft, sw):
    M["CUR"]["ft"] = ft
    D = []
    for g in T1:
        d = M["build_genzel"](g, "BEAM" if "e" in sw else "MAIN")
        if "b" in sw or "b1" in sw: d["gN"] = g_cfg401(d["R"], g, d["Mb"])
        else: d["gN"] = M["gN_of"](d["comp"], d["R"])
        D.append(d)
    kpa = 8.69 if "f2" in sw else M["DA_kpc_per_arcsec"](M["LZ"]["zC-488879"])
    Re_dr = 0.88 * 8.69 if "a" in sw else 0.88 * kpa                 # (a): DSC1's drift radius
    R, lg, sg, n = lelli488(kpa, Re_dr)
    if "b" in sw or "b2" in sw:
        L = L488_DSC1; Mb = L["Ms"] + L["Mg"]
        gN = (M["g_hern"](R, L["Rbul"] / 1.8153, L["Ms"] * L["fbul"]) + M["g_disc"](R, L["Rdisc"] / 1.678, L["Ms"] * (1 - L["fbul"]))
              + M["g_disc"](R, L["Rdisc"] / 1.678, L["Mg"]))
    else:
        comp = M["lelli_baryons"]("MAIN"); comp["Rd"] = 0.88 * kpa / 1.678; comp["Rgas"] = comp["Rd"]; Mb = comp["Mb"]; gN = M["gN_of"](comp, R)
    D.append(dict(name="zC-488879", z=M["LZ"]["zC-488879"], R=R, lg=lg, sig=sg, n=n, neff=n / 2.0, c=2.0, Mb=Mb, gN=gN))
    for d in D:
        if "c" in sw:
            Rm = d["R"] * KPC; X = XTAB_R[ft]["z0.0"] if d["z"] < 1 else XTAB_R[ft]["z1.0"]
            d["gref"] = G * CR_record(Rm, d["Mb"], X, d["z"]) / Rm ** 2
        else:
            d["gref"] = M["g_ref"](d["R"], d["Mb"], d["z"])
        d["gL"] = np.asarray(glaw_R(d["gN"], A0[ft]), float) if "f3" in sw else M["law"](d["gN"], A0[ft])
        if "d" in sw: d["c"] = 1.0; d["neff"] = float(d["n"])
        if "g" in sw: d["c"] = 2.0; d["neff"] = d["n"] / 2.0
    return D

def chi(D, A): return sum(float(np.sum(((d["lg"] - np.log10(d["gN"] + A * d["gref"])) / d["sig"]) ** 2)) / d["c"] for d in D)
def chiL(D): return sum(float(np.sum(((d["lg"] - np.log10(d["gL"])) / d["sig"]) ** 2)) / d["c"] for d in D)
def grid(sw): return np.round(np.arange(0.0, 6.0 + 1e-9, 0.005), 3) if "f1" in sw else M["AG"]
def evaluate(ft, sw):
    D = build(ft, sw); ab = [d for d in D if M["member"](d, ft)]; be = [d for d in D if not M["member"](d, ft)]
    AG = grid(sw); out = {}
    ch = np.array([chi(ab, A) if all(np.all(d["gN"] + A * d["gref"] > 0) for d in ab) else np.inf for A in AG]); i = int(np.argmin(ch))
    if "d" in sw: dof = max(sum(d["n"] for d in ab) - 1, 1); lvl = 4.0
    else: dof = max(sum(d["neff"] for d in ab) - 1, 1.0); lvl = 3.84
    s2 = max(1.0, ch[i] / dof); ok = ch <= ch[i] + lvl * s2
    out["above"] = dict(names=[d["name"] for d in ab], A=float(AG[i]), lo=float(AG[ok].min()), hi=float(AG[ok].max()), s2=float(s2),
                        chi2_A0=chi(ab, 0.0), chi2_A1=chi(ab, 1.0), chi2_L=chiL(ab), chi2_min=float(ch[i]))
    AGp = AG[AG >= 0]; chb = np.array([chi(be, A) for A in AGp]); j = int(np.argmin(chb))
    out["below"] = dict(names=[d["name"] for d in be], chi2_L=chiL(be), chi2_N=chi(be, 0.0), chi2_H=float(chb[j]), A_H=float(AGp[j]), chi2_H1=chi(be, 1.0))
    return out

RUNS = [("A1 base (DSC1R)", set()), ("(a) pressure", {"a"}), ("(b) baryons", {"b"}), ("(b1) Genzel bulge = B/T x M* (CFG401)", {"b1"}), ("(b2) zC-488879 baryons (alpha 4.3)", {"b2"}), ("(c) halo", {"c"}), ("(d) errors / correlation / interval", {"d"}),
        ("(e) cut 0.6\"", {"e"}), ("(f1) A grid 0-6", {"f1"}), ("(f2) Lelli kpc 8.69", {"f2"}), ("(f3) glaw kernel", {"f3"}),
        ("(b)+(e)", {"b", "e"}), ("(b)+(d)", {"b", "d"}), ("(d)+(e)", {"d", "e"}), ("(b)+(d)+(e)", {"b", "d", "e"}),
        ("all swapped", {"a", "b", "c", "d", "e", "f1", "f2", "f3"}),
        ("(g) c = 2 per point (Nyquist), reported", {"g"}), ("(b)+(e)+(g), reported", {"b", "e", "g"})]
DSC1_TARGET = {"canonical": dict(A=0.670, lo=0.250, hi=1.175, chi2_A0=241.2, chi2_A1=169.5, chi2_L=156.2, b_A0=942.9, b_A1=224.1, b_L=281.2, b_AH=1.415),
               "alt": dict(A=0.120, lo=0.000, hi=0.640, chi2_A0=72.9, chi2_A1=126.7, chi2_L=98.3, b_A0=1111.2, b_A1=266.9, b_L=303.1, b_AH=1.390)}
P("DSC1R reconcile: DSC1R A1 build -> DSC1's ingredients one at a time. Grades nothing; relabels neither lane. kappa = 1/2 FITTED; not theory closed.")
RES = dict(lane="DSC1R reconcile", base="A1 (f70457d798)", runs={}, target=DSC1_TARGET)
for name, sw in RUNS:
    RES["runs"][name] = {}
    for ft in M["FOOTS"]:
        r = evaluate(ft, sw); RES["runs"][name][ft] = r; a, b = r["above"], r["below"]
        P(f"[{ft}] {name:40s} ABOVE A {a['A']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}] s2 {a['s2']:.2f} chi2 A0/A1/L {a['chi2_A0']:.1f}/{a['chi2_A1']:.1f}/{a['chi2_L']:.1f} | "
          f"BELOW chi2 L {b['chi2_L']:.1f} N {b['chi2_N']:.1f} H {b['chi2_H']:.1f} (A {b['A_H']:.3f}) H1 {b['chi2_H1']:.1f}")
# halo agreement check (A1 halo vs record halo, same disc)
hc = {}
for ft in M["FOOTS"]:
    M["CUR"]["ft"] = ft; R = np.array([3.0, 8.0, 15.0]); z = 2.242; Mb = 2.5e11
    a = M["g_ref"](R, Mb, z); X = XTAB_R[ft]["z1.0"]; b = G * CR_record(R * KPC, Mb, X, z) / (R * KPC) ** 2
    hc[ft] = float(np.max(np.abs(a / b - 1)))
P(f"halo check (zC 400569 at 3, 8, 15 kpc): A1 halo / record halo - 1, max {hc['canonical']:.1e} / {hc['alt']:.1e}")
RES["halo_check_maxrel"] = hc
for ft in M["FOOTS"]:
    a = RES["runs"]["all swapped"][ft]["above"]; b = RES["runs"]["all swapped"][ft]["below"]; t = DSC1_TARGET[ft]
    ok = (abs(a["A"] - t["A"]) <= 0.005 and abs(a["lo"] - t["lo"]) <= 0.005 and abs(a["hi"] - t["hi"]) <= 0.005 and abs(a["chi2_A1"] - t["chi2_A1"]) <= 0.1
          and abs(a["chi2_L"] - t["chi2_L"]) <= 0.1 and abs(a["chi2_A0"] - t["chi2_A0"]) <= 0.1 and abs(b["chi2_N"] - t["b_A0"]) <= 0.1 and abs(b["chi2_H1"] - t["b_A1"]) <= 0.1
          and abs(b["chi2_L"] - t["b_L"]) <= 0.1 and abs(b["A_H"] - t["b_AH"]) <= 0.005)
    RES.setdefault("reproduces_DSC1", {})[ft] = bool(ok)
    P(f"[{ft}] all swapped reproduces DSC1's numbers (A, interval, chi2 A0/A1/law above; chi2 A0/A1/law and best A below): {ok}")
json.dump(RES, open(os.path.join(HERE, "dsc1r_reconcile.json"), "w"), indent=1)
open(os.path.join(HERE, "dsc1r_reconcile.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
