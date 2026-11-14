"""AGB1R comparison helper (written after RESULT_BLIND.md was committed and AGB1's README was opened).
Reference median-age templates with the delay-time cutoff handled exactly (T_W: integration starts at 40 Myr; T_S:
fine grid through t_p), cosmic time by adaptive quadrature, many grid points; compared with this build's tables and
AGB1's (agb1_template.py, executed from its committed file). Writes agb1r_compare_templates.json / .out."""
import os, sys, json, importlib.util
import numpy as np
from scipy.integrate import quad, cumulative_simpson
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from agb1r_common import (build_template, sfh_behroozi, sfh_md14, dtd_childress, E2, GYR_PER_INVH0, BG_T)
spec = importlib.util.spec_from_file_location("agb1_template_other",
                                              os.path.join(HERE, "..", "AGB1_progenitor_age_bias", "agb1_template.py"))
T1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(T1)
H0, Om, w0, wa = BG_T["H0"], BG_T["Om"], BG_T["w0"], BG_T["wa"]
tH = GYR_PER_INVH0/H0

def t_of_z(z):
    f = lambda x: 1/np.sqrt(E2(np.expm1(x), Om, w0, wa))
    return tH*(quad(f, np.log1p(z), np.log1p(1e5), limit=500, epsabs=1e-13, epsrel=1e-12)[0]
               + (2/3)/np.sqrt(Om)*(1 + 1e5)**-1.5)

# fine z(t) inversion table
xs = np.linspace(0, np.log1p(1e4), 400001); zs = np.expm1(xs)
Hinv = tH/np.sqrt(E2(zs, Om, w0, wa))
ts = cumulative_simpson(Hinv[::-1], dx=xs[1] - xs[0], initial=0.0)[::-1] + (2/3)*tH/np.sqrt(Om)*np.exp(-1.5*xs[-1])
assert abs(ts[0] - t_of_z(0.0)) < 1e-9 and abs(np.interp(1.0, zs, ts) - t_of_z(1.0)) < 1e-7

def median_ref(z, kind, n=400001):
    T = t_of_z(z)
    if kind == "W":
        lo = np.log(0.04); dtd = lambda tau: tau**-1.13; sfh = sfh_md14
    else:
        lo = np.log(1e-5); dtd = dtd_childress; sfh = sfh_behroozi
    lt = np.linspace(lo, np.log(T*(1 - 1e-12)), n); tau = np.exp(lt)
    zf = np.interp(T - tau, ts[::-1], zs[::-1])
    w = sfh(zf)*dtd(tau)*tau
    c = cumulative_simpson(w, dx=lt[1] - lt[0], initial=0.0); c /= c[-1]
    return float(np.exp(np.interp(0.5, c, lt)))

zz = [0.01, 0.02, 0.03, 0.055, 0.1, 0.3, 0.5, 1.0, 1.14]
out = {}
lines = []
for kind in ("W", "S"):
    a0 = median_ref(0.0, kind)
    ref = np.array([0.030*(a0 - median_ref(z, kind)) for z in zz])
    mine = build_template(kind)["spline"](zz); theirs = np.asarray(T1.T(np.array(zz), kind))
    out[kind] = dict(z=zz, ref=ref.tolist(), mine=mine.tolist(), agb1=theirs.tolist(), age0_ref=a0)
    lines.append(f"T_{kind}: reference median age at z 0 = {a0:.5f} Gyr")
    lines.append("   z       reference   AGB1R (diff)          AGB1 (diff)")
    for i, z in enumerate(zz):
        lines.append(f"  {z:5.3f}   {ref[i]:.6f}   {mine[i]:.6f} ({mine[i] - ref[i]:+.1e})   {theirs[i]:.6f} ({theirs[i] - ref[i]:+.1e})")
    lines.append(f"  max |AGB1R - ref| {np.abs(mine - ref).max():.1e} mag;  max |AGB1 - ref| {np.abs(theirs - ref).max():.1e} mag")
# refit the T_W profile ends on `full` with each build's T_W (this build's fitter)
from agb1r_common import load_des, sample_keep, SN, BAO, PartA, fit_A
D = load_des(); keep = sample_keep(D, "full"); zk = D["zhd"][keep]
for lab, T in (("AGB1R T_W", build_template("W")["spline"](zk)), ("AGB1 T_W", np.asarray(T1.T(zk, "W")))):
    m = PartA(SN(D, keep, T), BAO("all")); r = fit_A(m, None, "free"); r0 = fit_A(m, 0.0, "free")
    out["refit_" + lab.split()[0]] = dict(A=r["A"], chi2=r["chi2"], dchi2_A0=r0["chi2"] - r["chi2"])
    lines.append(f"{lab} in this build's fitter (`full`): A_W free {r['A']:.4f}, chi2 {r['chi2']:.4f}, "
                 f"dchi2(A_W = 0) {r0['chi2'] - r['chi2']:.4f}")
print("\n".join(lines))
open(os.path.join(HERE, "agb1r_compare_templates.out"), "w").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, "agb1r_compare_templates.json"), "w"), indent=1)
