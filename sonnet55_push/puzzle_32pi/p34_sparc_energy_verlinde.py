"""p34: SPARC test of field-energy-additive Verlinde (p33) against the framework law.
  framework:  g^2 = g_N^2 + a g_N
  energy-V:   g^2 = g_N^2 + a g_N (3 + s),   s = dln g_N/dln r along the curve  [spherical-equivalent mass M(<r) = r V_bar^2/G; 4 pi G rho r = 2 g_N + r g_N';
              M' >= 0 enforced: (3 + s) clipped at >= 1 ... no: clipped at >= 0 only where 2 + s < 0 would mean negative dM/dr -> set 3 + s = 1 there (no local term)]
Both fitted the same way (lane V machinery: v_common loader, log-g_obs chi^2, sigma_int fixed, a profiled): (i) Upsilon fixed 0.5 / bulge 0.7, MLS16 cuts (Q <= 2, i >= 30),
sigma_int 0.11 dex; (ii) Upsilon free per galaxy (0.05-3), all galaxies, sigma_int 0.0808 dex (lane V). Delta chi^2 is on independent points; lane V's crude clustering
deflation (~x18) is quoted. Also: framework residuals vs the local term log10((3+s)) (the energy-V signature) -- a correlation would favour energy-V.
Run: python3 p34_sparc_energy_verlinde.py  |  MUTATE=1: energy-V with s replaced by -2 everywhere (it must then equal the framework: check M fails if not identical)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)

def prep(g, ug):
    gobs = (g["Vobs"] * 1e3) ** 2 / g["Rm"]
    Vb2 = (np.sign(g["Vgas"]) * g["Vgas"]**2)[None, :] + ug[:, None] * g["Vdisk"][None, :]**2 + 1.4 * ug[:, None] * g["Vbul"][None, :]**2
    gb = Vb2 * 1e6 / g["Rm"][None, :]
    lr = np.log(g["Rm"])
    with np.errstate(all="ignore"):
        lg = np.log(np.where(gb > 0, gb, np.nan))
        s = np.gradient(lg, lr, axis=1) if len(lr) >= 3 else np.full_like(lg, -2.0)
    fac = 3 + s
    fac = np.where(np.isfinite(fac) & (2 + s >= 0), fac, 1.0)          # negative dM/dr (gas dips) or undefined -> no local term
    if MUTATE: fac = np.ones_like(fac)
    sig = (g["eV"] / g["Vobs"]) * 2.0 / math.log(10)
    return gobs, gb, fac, sig

def chi2(pre, a, sint, model):
    tot, n = 0.0, 0
    for gobs, gb, fac, sig in pre:
        ok = (gb > 0) & np.isfinite(gb)
        with np.errstate(all="ignore"):
            gbs = np.where(ok, gb, 1.0)
            pred = np.sqrt(gbs**2 + a * gbs * (fac if model == "E" else 1.0))
            r = np.log10(gobs)[None, :] - np.log10(pred)
            v = np.where(ok, r * r / (sig[None, :]**2 + sint**2), 0.0)
        ss = v.sum(axis=1); k = int(np.argmin(np.where(ok.sum(axis=1) > 0, ss, np.inf)))
        tot += ss[k]; n += int(ok[k].sum())
    return tot, n

gals = V.load_sparc()
A = np.exp(np.linspace(math.log(0.4e-10), math.log(3e-10), 61))
out = {}
for lab, sel, ug, sint in (("fixed Upsilon 0.5, MLS16 cuts", [g for g in gals if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30], np.array([0.5]), 0.11),
                           ("Upsilon free 0.05-3, all", gals, V.UGRID, 0.0808)):
    pre = [prep(g, ug) for g in sel]
    row = {}
    for model in ("F", "E"):
        ch = np.array([chi2(pre, a, sint, model)[0] for a in A]); i = int(np.argmin(ch))
        ahat, _ = V.parabola_min(A, ch, k=6)
        row[model] = (ahat, ch[i], chi2(pre, A[i], sint, model)[1])
    d = row["E"][1] - row["F"][1]
    out[lab] = (row, d)
    print(f"   {lab:32s} ({len(sel)} galaxies, {row['F'][2]} points): framework a = {row['F'][0]:.3e}, chi2 {row['F'][1]:.1f};  energy-V a = {row['E'][0]:.3e}, chi2 {row['E'][1]:.1f};"
          f"  Delta chi2 (E - F) = {d:+.1f}  (/18 clustering ~ {d/18:+.1f})")
# residual signature at the framework's best fit, fixed-Upsilon sample
lab = "fixed Upsilon 0.5, MLS16 cuts"; sel = [g for g in gals if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
pre = [prep(g, np.array([0.5])) for g in sel]; aF = out[lab][0]["F"][0]
R, X = [], []
for gobs, gb, fac, sig in pre:
    ok = (gb[0] > 0) & np.isfinite(gb[0])
    pred = np.sqrt(gb[0][ok]**2 + aF * gb[0][ok])
    R += list(np.log10(gobs[ok]) - np.log10(pred)); X += list(np.log10(fac[0][ok]))
R, X = np.array(R), np.array(X)
rho = np.corrcoef(X, R)[0, 1]
slope = np.polyfit(X, R, 1)[0]
print(f"   framework residuals vs log10(3 + s): Pearson r = {rho:+.3f}, slope {slope:+.3f} (energy-V predicts a positive slope ~ +0.5 in the deep regime, less where Newtonian)")
if MUTATE:
    check("M with s = -2 everywhere energy-V must equal the framework exactly", all(abs(v[1]) < 1e-9 for v in out.values()))
else:
    check("M (control) the two models differ on SPARC (|Delta chi2| > 1 in both treatments)", all(abs(v[1]) > 1 for v in out.values()))
dF = out["fixed Upsilon 0.5, MLS16 cuts"][1]; dU = out["Upsilon free 0.05-3, all"][1]
verdict = "FAVOURS THE FRAMEWORK" if (dF > 0 and dU > 0) else ("FAVOURS ENERGY-V" if (dF < 0 and dU < 0) else "MIXED")
print(f"   verdict on SPARC: {verdict}")
check("V the verdict is the same in both Upsilon treatments (not MIXED)", verdict != "MIXED")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
