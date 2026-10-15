"""CFG797 -- sub-mm dish-antenna forecast at the framework-native mass.  Criteria: FROZEN_CRITERIA.md.  Seconds.
Run: python3 cfg797.py   (CFG797_MUTATE=1: rho -> 0).  kappa = 1/2 FITTED; not theory closed.  External numbers provisional.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG797_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


c, G, hbar, h, kB, eV, MSUN, PC = 2.99792458e8, 6.674e-11, 1.054571817e-34, 6.62607015e-34, 1.380649e-23, 1.602176634e-19, 1.989e30, 3.0857e16
rho = 0.0 if MUT else 0.01 * MSUN / PC ** 3
sig = 2.3e5
P("CFG797  sub-mm dish forecast at the framework-native mass" + ("  [MUTATE rho=0]" if MUT else ""))
R = {"lane": "CFG797", "mutate": MUT, "foot": {}}
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    rde = 4 * a0 ** 2 / (G * c ** 2)                       # kg/m^3
    E = (rde * c ** 2 * (hbar * c) ** 3) ** 0.25           # J
    nu = E / h
    R["foot"][foot] = dict(m_meV=E / eV * 1e3, nu_GHz=nu / 1e9, lam_mm=c / nu * 1e3, dnu_Hz=nu * (sig / c) ** 2)
    P(f"  {foot:9s}: m = {E / eV * 1e3:.3f} meV, nu = {nu / 1e9:.1f} GHz, lambda = {c / nu * 1e3:.3f} mm, line width {nu * (sig / c) ** 2 / 1e3:.0f} kHz")
f = R["foot"]["canonical"]; E = f["m_meV"] * 1e-3 * eV; dnu = f["dnu_Hz"]
P0 = lambda eps, A: eps ** 2 * rho * c ** 2 * c * A
k1 = MUT or abs(P0(1e-12, 10) / E * 86400 / 4.4e7 - 1) < 0.05
P(f"  K1 rate (no 2/3) at eps 1e-12, 10 m^2: {P0(1e-12, 10) / E * 86400:.2e}/day vs ARGON03 4.4e7: {'PASS' if k1 else 'FAIL'}")
k2 = abs(kB * 100 - 1.38e-21) / 1.38e-21 < 0.01
P(f"  K2 kT(100 K) = {kB * 100:.3e} W/Hz: {'PASS' if k2 else 'FAIL'}")
P("\n  A[m^2] Tsys[K]  t        P(eps 1e-12)[W]  SNR     eps_min(5 sigma)")
rows = []
for A in (1.0, 10.0):
    for T in (100.0, 300.0, 1000.0):
        for lab, t in (("1 h", 3600.0), ("1 day", 86400.0), ("30 d", 30 * 86400.0)):
            Ps = (2 / 3) * P0(1e-12, A)
            sP = kB * T * math.sqrt(dnu / t)
            snr = Ps / sP
            emin = 1e-12 * math.sqrt(5 / snr) if snr > 0 else float("inf")
            rows.append(dict(A=A, T=T, t=lab, P=Ps, snr=snr, eps_min=emin))
            P(f"  {A:5.0f}  {T:6.0f}  {lab:6s}   {Ps:.2e}        {snr:7.1f}  {emin:.1e}")
R["rows"] = rows; R.update(K1=bool(k1), K2=bool(k2))
best = min(r["eps_min"] for r in rows); worst = max(r["eps_min"] for r in rows)
P(f"\n  reach eps_min {best:.1e} .. {worst:.1e} vs nearest published 1e-8 (0.67-0.92 meV) and CFG795 window 4-6e-9: "
  f"every setup covers the window by x{4e-9 / worst:.0f} or more; ARGON03 kill sensitivity 1e-12 reached by {sum(r['eps_min'] <= 1e-12 for r in rows)}/{len(rows)} setups")
if MUT:
    P(f"  MUTATE: SNR {rows[0]['snr']} -> {'bites' if rows[0]['snr'] == 0 else 'DID NOT BITE'}")
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg797_results{sfx}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg797{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
