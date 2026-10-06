"""p44: (1) the sample-size theorem and (3) Bayes factors, from SPARC's Upsilon-free gas points (p41b selection: gas > 80% of g_bar; 19 galaxies, MLS16 cuts).
(1) Per-galaxy a0 on the gas points (framework kernel, sigma_int 0.11) -> scatter s of ln a0 across galaxies. To separate two hypotheses whose a0 differ by Delta (in ln)
    at z sigma (one-sided), N = (z s / Delta)^2 galaxies, IF the shared systematic floor f is below Delta/z (otherwise no N suffices).
(3) Point hypotheses for a0 (c = 299792.458 km/s, H0 = 67.4, Omega_L = 0.685; H_L = H0 sqrt(Omega_L)):
    kappa = 1/2 on rho_Lambda (c H_L/Z, Z = sqrt(32 pi/3)) = 9.3603e-11; the same on rho_total (alt footing) c H0/Z = 1.1312e-10;
    Milgrom c H/2 pi on both; Verlinde c H/6 on both; p40's 32 pi turn-off 1.061e-10.
    Data: a0 = 9.00e-11 (p41b) with ln-error sqrt(stat^2 + kernel 0.03^2 + distance 0.085^2) (distance: lane V, 5% in D -> 8.5% in a0). Gaussian in ln a0; BF vs kappa = 1/2.
Run: python3 p44_samplesize_and_bayes.py  |  MUTATE=1: data a0 replaced by 1.13e-10 (the BF ordering must change: check B fails)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
def sub(g, m):
    h = dict(g)
    for k in ("Rm", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"): h[k] = g[k][m]
    return h
GP = []
for g in gals:
    vb2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2
    fg = np.where(vb2 > 0, np.sign(g["Vgas"]) * g["Vgas"]**2 / np.where(vb2 > 0, vb2, 1), 0)
    m = fg > 0.8
    if m.sum() >= 2: GP.append(sub(g, m))
A = np.exp(np.linspace(math.log(0.15e-10), math.log(6e-10), 161))
per = [V.parabola_min(A, V.Profile([g], V.IF_alpha1, ufixed=0.5).scan(A, 0.11), k=6)[0] for g in GP]
la = np.log(per); s = float(np.std(la, ddof=1)); s_rob = float(1.4826 * np.median(np.abs(la - np.median(la))))
pooled = V.parabola_min(A, V.Profile(GP, V.IF_alpha1, ufixed=0.5).scan(A, 0.11), k=6)[0]
print(f"   (1) {len(GP)} galaxies: per-galaxy a0 median {np.exp(np.median(la)):.3e}; scatter s = {s:.3f} (robust {s_rob:.3f}) in ln a0;  pooled {pooled:.3e};  s/sqrt(N) = {s/math.sqrt(len(GP)):.3f}")
c, H0, OL = 299792.458, 67.4, 0.685
Hs = H0 / 3.0857e19; HL = Hs * math.sqrt(OL); Z = math.sqrt(32 * math.pi / 3); cm = c * 1e3
H = {"kappa=1/2, rho_Lambda (9.36e-11)": cm * HL / Z, "kappa=1/2, rho_total (alt)": cm * Hs / Z, "Milgrom 2pi, rho_Lambda": cm * HL / (2 * math.pi),
     "Milgrom 2pi, rho_total": cm * Hs / (2 * math.pi), "Verlinde 6, rho_Lambda": cm * HL / 6, "Verlinde 6, rho_total": cm * Hs / 6, "32pi turn-off (p40)": 1.061e-10}
ref = H["kappa=1/2, rho_Lambda (9.36e-11)"]
floor = math.hypot(0.03, 0.085)
print(f"   shared systematic floor f = sqrt(kernel 0.03^2 + distance 0.085^2) = {floor:.3f}")
print(f"   {'rival vs kappa=1/2 (rho_Lambda)':34s} {'Delta ln':>9s} {'N at 2 sigma':>13s} {'N at 3 sigma':>13s}   needs floor < Delta/z")
Ns = {}
for k, v in H.items():
    if v == ref: continue
    d = abs(math.log(v / ref))
    n2, n3 = (2 * s / d)**2, (3 * s / d)**2
    Ns[k] = (d, n3)
    print(f"   {k:34s} {d:9.3f} {n2:13.0f} {n3:13.0f}   2s: {'ok' if floor < d/2 else 'NO'}  3s: {'ok' if floor < d/3 else 'NO'}")
check("N the per-galaxy scatter is large (s > 0.3): deciding the coefficient against its nearest rivals needs hundreds to thousands of gas-dominated galaxies",
      s > 0.3 and min(n for d, n in Ns.values()) > 100)
check("F the distance systematic (8.5%) must also fall: at the present floor no N separates rivals closer than 2 x 9% at 2 sigma", any(floor > d / 2 for d, n in Ns.values()))
a_dat = 1.13e-10 if MUTATE else 9.00e-11
sig = math.hypot(0.11, floor)
print(f"   (3) data a0 = {a_dat:.3e}, sigma_ln = sqrt(0.11^2 + {floor:.3f}^2) = {sig:.3f}")
L = {k: math.exp(-0.5 * (math.log(a_dat / v) / sig)**2) for k, v in H.items()}
for k in sorted(L, key=L.get, reverse=True):
    print(f"     {k:34s} a0 {H[k]:.3e}  pull {math.log(a_dat/H[k])/sig:+.2f}  BF(kappa=1/2 rho_L : this) = {L['kappa=1/2, rho_Lambda (9.36e-11)']/L[k]:.2f}")
top = max(L, key=L.get)
check("B the best-supported hypotheses are the rho_Lambda ones (kappa = 1/2, Verlinde 6, Milgrom 2pi), with no BF > 3 among them: the data favour the rho_Lambda FOOTING, not the coefficient",
      "rho_Lambda" in top and max(L[k] for k in L if "rho_Lambda" in k) / min(L[k] for k in L if "rho_Lambda" in k) < 3)
check("R the rho_total (alt) kappa = 1/2 footing is disfavoured relative to the rho_Lambda one by BF > 2", L["kappa=1/2, rho_Lambda (9.36e-11)"] / L["kappa=1/2, rho_total (alt)"] > 2)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
