"""IB1 graded run: hypothesis HG, the cluster total mass = the gas's isothermal hydrostatic mass (FROZEN_CRITERIA.md, 0669ca3fc9).

M_tot(r) = 3 beta sigma^2 r^3 / (G (r^2 + r_c^2)), beta 2/3, r_c 0.15 R500 (record gas shape), sigma^2 = kT/(0.6 m_p) (KT
clusters) or OS1's sigma fill; held constant beyond r_t (3 Mpc graded); floor M_b. Newtonian route-E lensing through OS1's
pipeline (IC1's loader). No q, c_f, M_fair. Groups and SPARC are NOT A TEST (criteria section 1).
kappa = 1/2 FITTED; not theory closed.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ib1_hse_halo.py [--mutate]
"""
import os, sys, json, math, time, resource
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "IC1_inner_cluster_band"))
import numpy as np
import ic1b_lib as L

MUTATE = "--mutate" in sys.argv; TAG = "_MUTATE" if MUTATE else ""
NX = L.NX; G, MPC, MSUN = NX["G"], NX["MPC"], NX["MSUN"]; RG, RM = NX["RG"], NX["RM"]; GAS = NX["gas"]
MP, KEV, BETA = 1.67262192e-27, 1.602176634e-16, 2 / 3
T0 = time.time(); OUT = []; RES = dict(frozen="0669ca3fc9", mutate=MUTATE, footings={}); checks = []
def P(s): OUT.append(s); print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30   # macOS: bytes

def sig2(i):
    return L.KT[i] * KEV / (0.6 * MP) if L.OKK[i] else (L.SIG_C[i] * 1e3) ** 2
def m_hg(i, foot, hk, rt="3", s2fac=1.0):
    pp = L.prep(i, foot, hk); rc = 0.15 * pp["R500"]
    rcut = {"3": 3.0, "rta": pp["rta"] / MPC, "2.2R500": 2.2 * pp["R500"]}[rt]
    r = np.minimum(RG, rcut) * MPC; M = 3 * BETA * s2fac * sig2(i) * r ** 3 / (G * (r ** 2 + (rc * MPC) ** 2))
    fl = M < pp["Mb"]; return np.where(fl, pp["Mb"], M), bool(fl[RG <= 3.0].any())

def vectors(foot, hk, **kw):
    V = np.zeros_like(L.DC[(foot, hk)]); nfl = 0
    for i in L.ALLI:
        i = int(i); M, fl = m_hg(i, foot, hk, **kw); nfl += fl; V[i] = L.dvecN(i, foot, hk, M)
    L.PREP.clear(); return V, nfl

P("IB1 HG (gas-equilibrium hydrostatic cluster halo)" + (" [MUTATE: K1 analytic side at 2 kT]" if MUTATE else "")
  + "; kappa = 1/2 FITTED; not theory closed")

# ---- K1: analytic M_HSE vs -(sigma^2 r/G) dln rho_g/dln r of the record's gas(.., "P"), beta-model part
kti = np.where(L.OKK)[0]; kts = L.KT[kti]; k1 = True; foot0, hk0 = "canonical", "h0672"
for pc in (1, 25, 50, 75, 99):
    i = int(kti[np.argmin(np.abs(kts - np.percentile(kts, pc)))]); pp = L.prep(i, foot0, hk0)
    cl = NX["CL"][i]; h = NX["HV"][hk0]; qd = (float(NX["DM"](cl["z"], h)) / (1 + cl["z"])) / NX["DA_lcdm"](cl["z"])
    _, rho = GAS(cl["Mgas500"] * qd ** 2.5, pp["R500"], "P")
    sel = (RG >= 0.05) & (RG <= min(2.0 * pp["R500"], 2.9)); lr = np.log(RG); dl = np.gradient(np.log(rho), lr)   # A1: inside the gas cut
    num = -(sig2(i) * RG * MPC / G) * dl
    ana = m_hg(i, foot0, hk0, s2fac=2.0 if MUTATE else 1.0)[0]
    rel = float(np.max(np.abs(ana[sel] / num[sel] - 1))); k1 &= rel < 1e-5
    P(f"  K1 cluster KT p{pc} (kT {L.KT[i]:.2f} keV): max rel |analytic/numeric - 1| {rel:.1e}")
L.PREP.clear()
P(f"K1 {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))

classes = {}
for foot in L.FEET:
    o1 = L.OS1J["footings"][foot]; o1c, o1ok = o1["clusters"]["cells"], o1["clusters"]["ok"]; R = {}
    if not MUTATE:   # K0: IC1's loader reproduces OS1 (G-IN-Mall preds at q_f, SPARC A rms)
        cb, _, _ = L.grade(foot, o1["q_f"]); dpr = max(abs(cb[h]["G-IN-Mall"]["pred"] - o1c[h]["G-IN-Mall"]["pred"]) for h in L.HK)
        sb = L.sparc(foot, L.BGS["A_c2b_refit"], o1["q_f"]); k0 = dpr < 1e-9 and abs(sb["rms"] - o1["sparc_A"]["rms"]) < 1e-9
        P(f"\n=== [{foot}] K0: OS1 G-IN-Mall |dpred| {dpr:.1e}; SPARC A rms {sb['rms']:.6f} (OS1 {o1['sparc_A']['rms']:.6f}): "
          f"{'PASS' if k0 else 'FAIL'}   [{time.time() - T0:.0f} s]"); checks.append((f"K0[{foot}]", k0))
    else:
        P(f"\n=== [{foot}] MUTATE")
    def run(**kw):
        cells, nf = {}, 0
        for hk in L.HK:
            V, n = vectors(foot, hk, **kw); nf += n; cells[hk] = L.cells_from(foot, hk, V)[0]
        ok = {k: all(abs(cells[h][k]["Z"]) <= 2 for h in L.HK) for k in cells["h0672"]}
        return cells, ok, nf
    cells, ok, nfl = run()
    zin = max(abs(cells[h]["G-IN-Mall"]["Z"]) for h in L.HK); zin1 = max(abs(o1c[h]["G-IN-Mall"]["Z"]) for h in L.HK)
    newfail = [k for k in ok if o1ok[k] and not ok[k]]
    if all(ok.values()): cls = "PASS"
    elif zin < zin1 and not newfail: cls = "IMPROVES"
    elif (ok["G-IN-Mall"] or zin < zin1) and newfail: cls = "TRADES"
    else: cls = "FAILS"
    classes[foot] = cls
    P(f"  cells (h 0.672 | h 0.686): meas, pred, Z; floor binds in {nfl} cluster-cells")
    for k in cells["h0672"]:
        a, b = cells["h0672"][k], cells["h0686"][k]
        P(f"   {k:10s} {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f} | Z {b['Z']:+.2f}   "
          f"{'pass' if ok[k] else 'FAIL'}   (OS1 Z {o1c['h0672'][k]['Z']:+.2f}{'' if o1ok[k] else ' FAIL'})")
    P(f"  G-IN-Mall max|Z| {zin:.2f} (OS1 {zin1:.2f}); OS1-passing cells now failing: {newfail or 'none'}")
    P(f"  CLASS [{foot}]: {cls}")
    rep = {}
    for lab, kw in (("r_t = r_ta", dict(rt="rta")), ("r_t = 2.2 R500", dict(rt="2.2R500")), ("sigma^2 x 1.15 (non-thermal, context)", dict(s2fac=1.15))):
        c2, ok2, _ = run(**kw); fl2 = [k for k in ok2 if not ok2[k]]
        rep[lab] = dict(fails=fl2, zin=[c2[h]["G-IN-Mall"]["Z"] for h in L.HK])
        P(f"  (reported) {lab}: fails {fl2 or 'none'}; G-IN-Mall Z {c2['h0672']['G-IN-Mall']['Z']:+.2f} / {c2['h0686']['G-IN-Mall']['Z']:+.2f}   [{time.time() - T0:.0f} s]")
    # reported: implied core surface density vs OS1's core law (106 KT)
    rat = []
    for i in kti:
        i = int(i); pp = L.prep(i, foot, "h0672"); rc = 0.15 * pp["R500"] * MPC
        s_hg = 9 * BETA * sig2(i) / (4 * math.pi * G * rc); s_os = L.SIG[foot] * (L.SIG_C[i] / L.SREF) ** o1["q_f"]; rat.append(s_hg / s_os)
    L.PREP.clear()
    P(f"  (reported) Sigma_HG / Sigma_OS1 (106 KT): median {np.median(rat):.2f} [16-84% {np.percentile(rat, 16):.2f}-{np.percentile(rat, 84):.2f}]")
    rep["Sigma_HG_over_OS1"] = [float(np.median(rat)), float(np.percentile(rat, 16)), float(np.percentile(rat, 84))]
    # reported: per-bin pred/meas (all 326, h 0.672)
    hk = "h0672"; d = L.DAT[hk]; WB = d["W"] * d["B"][None, :]; nb = (WB * (d["D"] - NX["MY"]["leakP"][:, NX["HXI"][hk], 0])).sum(0)
    V, _ = vectors(foot, hk); dC = L.DC[(foot, hk)].sum(0); pm = (V.sum(0) / dC) / (nb / dC)
    P("  (reported) per-bin pred/meas, bins 0-7: " + " ".join(f"{x:.2f}" for x in pm)); rep["bin_pred_over_meas"] = pm.tolist()
    RES["footings"][foot] = dict(cells=cells, ok=ok, cls=cls, zin=zin, zin_os1=zin1, new_fail=newfail, n_floor=nfl, reported=rep)

GR1J = json.load(open(os.path.join(REB, "GR1_core_law_groups_ellipticals", "gr1_groups_ellipticals_results.json")))
P("\nNOT A TEST (quoted): groups keep the core law, GR1 class " + ", ".join(f"{f} {GR1J['footings'][f]['groups']['cls']}" for f in L.FEET)
  + "; SPARC keeps OS1's core law (K0 re-run only).")
k2 = rss() < 2.0; checks.append(("K2", k2)); P(f"K2 peak RSS {rss():.2f} GB: {'PASS' if k2 else 'FAIL'}")
v = classes["canonical"] if classes["canonical"] == classes["alt"] else "UNDECIDED"
P(f"\n=== VERDICT (both footings): HG {v}   [{time.time() - T0:.0f} s]; checks " + ", ".join(f"{k} {'PASS' if x else 'FAIL'}" for k, x in checks))
RES.update(verdict=v, classes=classes, checks=dict(checks))
json.dump(RES, open(os.path.join(HERE, f"ib1_hse_halo_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"ib1_hse_halo{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(x for _, x in checks) else 1)
