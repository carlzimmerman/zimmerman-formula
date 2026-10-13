#!/usr/bin/env python3
"""CFG666 (FROZEN_CRITERIA.md, 9dc52f46b): the dark-energy clock.  a_true = c H_Lambda, settled fraction f = 1 - exp(-H_Lambda t_b),
nu_eff = 1 + f [nu_mono(g_N/a_true) - 1], with f fixed per footing by the measured a0 (no free parameter): a knob-free SHAPE test
on raw SPARC (the record's CFG4 harness, Upsilon = 0.61).
kappa is fitted on the record; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg666.py     (CFG666_MUTATE=1 -> _MUTATE outputs, exit 1 iff both teeth bite)"""
import os, sys, io, json, math, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
    import CFG7_common as C7
MUT = os.environ.get("CFG666_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
FOOTS = ("canonical", "alt")
C = 2.99792458e8; G = 6.67430e-11; MPC = 3.0857e22; GYR = 3.15576e16
H0 = 67.4e3 / MPC; OL = 0.685
HL = H0 * math.sqrt(OL)
A_TRUE = C * HL
RHO_DE = 3 * H0 ** 2 * OL / (8 * math.pi * G)
OUT, RES = [], {"lane": "CFG666", "criteria": "9dc52f46b", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


nu = lambda y: np.asarray(C7.nu_mono(np.asarray(y, float)), float)
P("CFG666: the dark-energy clock" + (" [MUTATE]" if MUT else ""))
k_true = A_TRUE / (C * math.sqrt(G * RHO_DE))
P(f"a_true = c H_Lambda = {A_TRUE:.4e} m/s^2;  kappa_true = {k_true:.4f} (sqrt(8pi/3) = {math.sqrt(8 * math.pi / 3):.4f});  1/H_Lambda = {1 / HL / GYR:.3f} Gyr")
F, C1 = {}, {}
for foot in FOOTS:
    a0 = C7.A0_SI[foot]
    keff = a0 / (C * math.sqrt(G * RHO_DE))
    f = math.sqrt(a0 / A_TRUE)
    tb = -math.log(1 - f) / HL / GYR
    F[foot] = f
    C1[foot] = dict(a0=a0, kappa_eff=keff, f=f, t_b_Gyr=tb)
    P(f"C1 [{foot}] a0 {a0:.4e}  kappa_eff {keff:.4f}  f = sqrt(a0/a_true) = {f:.4f}  implied t_b = {tb:.2f} Gyr")
RES["C1"] = C1

with contextlib.redirect_stdout(io.StringIO()):
    g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
iu = int(np.argmin(np.abs(g4["UPS"] - 0.61)))
gb4, go4, ok4, ww4, GI, GAL = g4["GB"][:, iu], g4["GO"][:, iu], g4["OK"][:, iu], g4["WW"][:, iu], g4["GI"], g4["GAL"]
Tt = np.array([(GAL[i].get("meta") or {}).get("T", np.nan) for i in GI], float)
m = ok4 & (gb4 > 0)
w = ww4[m]; lo = np.log10(go4[m]); gb = gb4[m]


def stats(pred, mask=None):
    mm = np.ones(gb.size, bool) if mask is None else mask
    r = lo[mm] - np.log10(pred[mm]); ww = w[mm]
    return float(np.sqrt(np.sum(ww * r ** 2) / ww.sum())), float(np.sum(ww * r) / ww.sum()), int(mm.sum())


D1 = {}
for foot in FOOTS:
    a0 = C7.A0_SI[foot]
    f = F[foot] * (2.0 if (MUT and os.environ.get("CFG666_M") == "M2") else 1.0)
    if MUT and os.environ.get("CFG666_M") == "M1":
        f = 1.0
    law = nu(gb / a0) * gb
    clk = (1 + f * (nu(gb / A_TRUE) - 1)) * gb
    rl, bl, n = stats(law); rc, bc, _ = stats(clk)
    bins = {}
    for lab, (a, b) in {"g_bar > 1e-10": (1e-10, 1), "1e-11..1e-10": (1e-11, 1e-10), "< 1e-11": (0, 1e-11)}.items():
        mm = (gb > a) & (gb <= b)
        bins[lab] = dict(zip(("rms_law", "bias_law", "n"), stats(law, mm))) | dict(zip(("rms_clock", "bias_clock"), stats(clk, mm)[:2]))
    # D2: early (T <= 2) vs late (T >= 7), outer points, residual vs the law
    Tm = Tt[m]; outer = gb < 1e-11
    d2 = {}
    for lab, cond in (("early T<=2", Tm <= 2), ("late T>=7", Tm >= 7)):
        mm = outer & cond
        d2[lab] = dict(n=int(mm.sum()), n_gal=int(len(np.unique(GI[m][mm]))), mean_resid_law=stats(law, mm)[1] if mm.sum() else None)
    D1[foot] = dict(rms_law=rl, bias_law=bl, rms_clock=rc, bias_clock=bc, d=rc - rl, n=n, bins=bins, D2=d2, f=f)
    P(f"\nD1 [{foot}] {n} points: rms law {rl:.4f} (bias {bl:+.4f})   clock {rc:.4f} (bias {bc:+.4f})   d {rc - rl:+.4f}")
    for k, v in bins.items():
        P(f"   g_bar {k:13s} n {v['n']:4d}: law {v['rms_law']:.3f} ({v['bias_law']:+.3f})  clock {v['rms_clock']:.3f} ({v['bias_clock']:+.3f})")
    P(f"   D2 outer residual vs the law: early {d2['early T<=2']}  late {d2['late T>=7']}")

if all(D1[f]["d"] <= 0.01 and abs(D1[f]["bias_clock"]) <= 0.03 for f in FOOTS):
    lab = "SHAPE ALLOWED"
elif any(D1[f]["d"] >= 0.03 or abs(D1[f]["bias_clock"]) > 0.06 for f in FOOTS):
    lab = "SHAPE DISFAVOURED"
else:
    lab = "SHAPE TENSION"
RES["D1"] = D1
C2 = {f"tau_ff {t} Gyr": HL * t * GYR for t in (0.1, 0.3, 0.5)}
RES["C2"] = dict(alpha_eff=C2, below_first_excluded_node_0p1=all(v < 0.1 for v in C2.values()))
P(f"\nC2 mergers: alpha_eff = H_Lambda tau_ff = " + ", ".join(f"{k}: {v:.4f}" for k, v in C2.items()) + " (CFG623 allowed {0}; first excluded 0.1)")
rc_ = 0
if MUT:
    J = json.load(open(os.path.join(HERE, "cfg666_results.json")))
    mode = os.environ.get("CFG666_M", "")
    if mode == "M1":
        bite = D1["canonical"]["rms_clock"] - J["D1"]["canonical"]["rms_clock"] >= 0.1
    else:
        bite = abs(D1["canonical"]["bias_clock"] - J["D1"]["canonical"]["bias_clock"]) >= 0.1
    RES["tooth"] = dict(mode=mode, bites=bool(bite)); P(f"MUTATE {mode}: bites {bite}")
    rc_ = 1 if bite else 0
else:
    RES["label"] = lab; P(f"\nLANE LABEL (shape): {lab}")
json.dump(RES, open(os.path.join(HERE, f"cfg666_results{TAG}{os.environ.get('CFG666_M', '')}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg666{TAG}{os.environ.get('CFG666_M', '')}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc_)
