"""AGB1R comparison helper (written after RESULT_BLIND.md was committed and AGB1's README was opened).
Evaluates this build's Part C model at AGB1's committed Part C points (fork fits on `full` and `des_only`, and the far end
of the `full` A profile), with this build's exact CAMB distances and with AGB1's linear interpolation of D_M on its
601-point ln(1+z) grid (agb1_run.py), to tell minimiser differences from model differences. Executes the model section
of agb1r_partC.py unchanged (log path swapped). Writes agb1r_compare_points.json / .out."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OTHER = os.path.join(HERE, "..", "AGB1_progenitor_age_bias")
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "agb1r_partC.py")).read()
head = src.split("out = dict(mode=MODE)")[0]
old = 'logf = open(os.path.join(HERE, f"agb1r_C_{MODE}.out"), "w")'
assert old in head
ZSN_AGB1 = np.expm1(np.linspace(0, np.log(2.2), 601))
lines = []; out = {}

def model_for(sample):
    h = head.replace(old, 'logf = open(os.devnull, "w")')
    sys.argv = ["agb1r_partC.py", sample]
    ns = {"__name__": "agb1r_partC_model", "__file__": os.path.join(HERE, "agb1r_partC.py")}
    exec(compile(h, os.path.join(HERE, "agb1r_partC.py"), "exec"), ns)
    return ns

def sn_interp(ns, p, A):
    camb, sn = ns["camb"], ns["sn"]; h, ob, obc, w0, wa = p
    P = camb.CAMBparams(); P.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    P.set_cosmology(H0=100*h, ombh2=ob, omch2=obc - ob, mnu=0.06, num_massive_neutrinos=1, nnu=3.044, omk=0)
    P.WantTransfer = False; P.WantCls = False
    R = camb.get_background(P); d = R.comoving_radial_distance(ZSN_AGB1); d[0] = 0.0
    dm = np.interp(sn.z, ZSN_AGB1, d); dx = R.comoving_radial_distance(sn.z)
    return sn.chi2(5*np.log10((1 + sn.zhel)*dm) + 25, A)[0], float(np.max(np.abs(5*np.log10(dm/dx))))

def one(ns, label, t, A, my_fit):
    p = (t["h"], t["omega_b"], t["omega_bc"], t["w0"], t["wa"])
    r = ns["evaluate"](p, A); mq = ns["minq_p"](p)[0]; ci, dmu = sn_interp(ns, p, A)
    rec = dict(agb1_chi2=t["chi2"], my_model_at_agb1_point=r["chi2"], my_fit=my_fit, agb1_sn=t["chi2_sn"],
               my_sn=r["chi2_sn"], my_sn_with_agb1_interp=ci, agb1_bao=t["chi2_bao"], my_bao=r["chi2_bao"],
               agb1_prior=t["chi2_prior"], my_prior=r["chi2_prior"], minq_at_agb1_point=mq, max_abs_dmu_interp=dmu)
    out[label] = rec
    lines.append(f"{label:24s} AGB1 {t['chi2']:.4f} | my model at AGB1 point {r['chi2']:.4f} | my fit {my_fit:.4f} | "
                 f"SN: AGB1 {t['chi2_sn']:.4f}, mine {r['chi2_sn']:.4f}, mine with AGB1 interpolation {ci:.4f} | "
                 f"BAO diff {r['chi2_bao'] - t['chi2_bao']:+.1e}, prior diff {r['chi2_prior'] - t['chi2_prior']:+.1e} | "
                 f"min q {mq:+.1e} | max |dmu| interp {dmu:.1e}")

for sample in ("full", "des_only"):
    ns = model_for(sample)
    theirs = json.load(open(os.path.join(OTHER, f"agb1_C_{sample}.json")))
    mine = json.load(open(os.path.join(HERE, f"agb1r_C_{sample}.json")))
    for lab, A in (("A0", 0.0), ("A1", 1.0), ("Afree", None)):
        for k_t, k_m in (("base", "best"), ("today", "q0zero"), ("never", "never")):
            one(ns, f"{sample} {lab} {k_m}", theirs["forks"][lab][k_t], A, mine["forks"][lab][k_m]["chi2"])
    if sample == "full":
        for a in ("2.75", "3.00"):
            ka = next(k for k in theirs["profile"] if abs(float(k) - float(a)) < 1e-9)
            km = next(k for k in mine["profile"] if abs(float(k) - float(a)) < 1e-9)
            one(ns, f"full profile A {a}", theirs["profile"][ka], float(a), mine["profile"][km]["chi2"])
# Part A bao_overlap, A free, never-accelerated (both fits on the Om = 0.05 floor)
from agb1r_common import load_des, sample_keep, SN, BAO, PartA, build_template, minq
D = load_des(); keep = sample_keep(D, "full")
mA = PartA(SN(D, keep, build_template("S")["spline"](D["zhd"][keep])), BAO("overlap"))
t = json.load(open(os.path.join(OTHER, "agb1_A_bao_overlap.json")))["forks"]["Afree"]["never"]
mi = json.load(open(os.path.join(HERE, "agb1r_A_bao_overlap.json")))["forks"]["Afree"]["never"]
rA = mA.eval(t["Om"], t["w0"], t["wa"], None)
out["A bao_overlap Afree never"] = dict(agb1_chi2=t["chi2"], my_model_at_agb1_point=rA["chi2"], my_fit=mi["chi2"],
                                        minq_at_agb1_point=minq(t["Om"], t["w0"], t["wa"])[0], my_minq=mi["minq"])
lines.append(f"Part A bao_overlap Afree never: AGB1 point Om {t['Om']:.4f} w0 {t['w0']:+.4f} wa {t['wa']:+.4f}, AGB1 chi2 "
             f"{t['chi2']:.4f}, my model there {rA['chi2']:.4f} (min q {minq(t['Om'], t['w0'], t['wa'])[0]:+.1e}); my fit "
             f"{mi['chi2']:.4f} at Om {mi['Om']:.4f} w0 {mi['w0']:+.4f} wa {mi['wa']:+.4f} (min q {mi['minq']:+.1e})")
print("\n".join(lines))
open(os.path.join(HERE, "agb1r_compare_points.out"), "w").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, "agb1r_compare_points.json"), "w"), indent=1, default=float)
