"""CFG775 -- black holes, cold energy, dark energy and the horizon.

Criteria: FROZEN_CRITERIA.md (committed alone first, d5c63f856).
A  geometric identity table through q = a0/(c H_inf) = kappa sqrt(3/8pi).
B1 amount: cosmologically coupled BHs (k = 3) as dark energy's source, from the Madau & Dickinson (2014) SFRD.
B2 shape F(z) = rho_DE(z)/rho_DE0 vs the record's F-DESI branch (CFG571 r_desi).
B3 sealed ALMA predictions under the BH branch (CFG571 predict, imported read-only).
Run: python3 cfg775.py   (CFG775_MUTATE=1 for the teeth).  Seconds.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np
from scipy import integrate

MUT = os.environ.get("CFG775_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"cfg775{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


RES = {"lane": "CFG775", "mutate": MUT, "checks": {}, "numbers": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


c, G = 2.99792458e8, 6.67430e-11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5
q = KAPPA * math.sqrt(3 / (8 * math.pi))
P("CFG775  black holes / cold energy / dark energy / horizon" + ("  [MUTATE]" if MUT else ""))

# ======================================================================== A geometry
P(f"\nA  every relation through q = a0/(c H_inf) = kappa sqrt(3/8pi) = {q:.6f}")
A = {}
okA = True
for f, a0 in A0.items():
    H = a0 / (q * c)                                   # framework's H_inf on this footing
    RH = c / H
    M = 1.989e30 * 1e10                                # any mass: the ratios below are mass-free
    rs, rM = 2 * G * M / c ** 2, math.sqrt(G * M / a0)
    MH = c ** 3 / (2 * G * H)                          # vacuum mass inside R_H (its Schwarzschild radius is R_H)
    rows = {
        "r_M / sqrt(r_s R_H)": (rM / math.sqrt(rs * RH), 1 / math.sqrt(2 * q)),
        "capacity a0/(pi G) / [M_H/(4 pi R_H^2)]": ((a0 / (math.pi * G)) / (MH / (4 * math.pi * RH ** 2)), 8 * q),
        "capacity / [M_H/(pi R_H^2)] (projected)": ((a0 / (math.pi * G)) / (MH / (math.pi * RH ** 2)), 2 * q),
        "M(BH surface gravity = a0) / M_H": ((c ** 4 / (4 * G * a0)) / MH, 1 / (2 * q)),
        "a0 / (dS horizon surface gravity c H)": (a0 / (c * H), q),
        "Nariai mass / M_H": ((c ** 3 / (3 * math.sqrt(3) * G * H)) / MH, 2 / (3 * math.sqrt(3))),
        "r_M(M_H) / R_H": (math.sqrt(G * MH / a0) / RH, 1 / math.sqrt(2 * q)),
    }
    for k, (direct, fromq) in rows.items():
        okA &= abs(direct / fromq - 1) < 1e-12
    A[f] = {k: v[0] for k, v in rows.items()}
    A[f]["H_inf_kms_Mpc"] = H * 3.0857e19
    P(f"  {f}: H_inf = {H * 3.0857e19:.2f} km/s/Mpc")
    for k, (d, fq) in rows.items():
        P(f"    {k:44s} = {d:.6f}  (from q: {fq:.6f})")
check("K1 every relation is a fixed function of q alone", okA, "direct SI numbers = q-formulas to 1e-12; no independent constant -> ONE COINCIDENCE (a0 ∝ c H_inf)")
P("  Cold energy's amount (Omega_c/Omega_b = 5.364): no relation to q or to any horizon quantity is on the record (no 5.364 formula); none constructed here.")
RES["numbers"]["A"] = A

# ======================================================================== B the coupled-BH dark-energy history
h, OM = 0.70, 0.308
H0 = 100 * h / 3.0857e19 * 3.156e7                     # 1/yr
RHO_CRIT = 2.775e11 * h ** 2                            # Msun/Mpc^3
RHO_DE0 = (1 - OM) * RHO_CRIT
K = 0 if MUT else 3
EPS_SCALE = 1.0


def psi(z):                                            # Madau & Dickinson 2014 eq. 15, Msun/yr/Mpc^3 (Salpeter)
    return 0.015 * (1 + z) ** 2.7 / (1 + ((1 + z) / 2.9) ** 5.6)


def dtdz(z):
    return 1.0 / ((1 + z) * H0 * math.sqrt(OM * (1 + z) ** 3 + 1 - OM))


def I_of(z, zmax, k=K, popIII=False):
    v = integrate.quad(lambda x: psi(x) * (1 + x) ** k * dtdz(x), z, zmax, limit=400, epsrel=1e-11)[0]
    if popIII:
        lo = max(z, 10.0)
        if lo < 30.0:
            v += (0.5 / 1.0) * integrate.quad(lambda x: 1e-3 * (1 + x) ** k * dtdz(x), lo, 30.0, limit=400, epsrel=1e-11)[0]  # eps_III/eps folded below
    return v


P(f"\nB1  amount: rho_DE0 = {RHO_DE0:.3e} Msun/Mpc^3 (h {h}, Omega_m {OM}); k = {K}")
B1 = {}
for zmax in (8.0, 15.0, 30.0):
    I0 = I_of(0.0, zmax)
    eps_req = RHO_DE0 / I0
    B1[str(zmax)] = dict(I0=I0, eps_req=eps_req)
    P(f"  z_max {zmax:4.0f}: int psi (1+z)^{K} dt = {I0:.3e} Msun/Mpc^3 -> eps_req = {eps_req:.3f}  "
      f"({'EXCLUDED for stellar remnants (> 0.05)' if eps_req > 0.05 else 'allowed'})")
# Pop III: rho from popIII with eps_III = 0.5 directly
rIII = 0.5 * integrate.quad(lambda x: 1e-3 * (1 + x) ** K * dtdz(x), 10.0, 30.0, limit=400)[0]
P(f"  Pop III bracket (psi_III 1e-3 over z 10-30, eps_III 0.5): rho = {rIII:.3e} = {rIII / RHO_DE0:.3f} of rho_DE0")
allx = all(v["eps_req"] > 0.05 for v in B1.values())
if not MUT:
    check("B1 class", True, ("EXCLUDED: stellar-remnant BHs cannot source dark energy (eps_req > 0.05 at every z_max)" if allx else
                             "NOT EXCLUDED by amount") + f"; eps_req = " + ", ".join(f"{v['eps_req']:.2f}" for v in B1.values()))
RES["numbers"]["B1"] = B1
RES["numbers"]["popIII_fraction"] = rIII / RHO_DE0

P("\nB2  shape: F(z) = rho_DE(z)/rho_DE0 (eps-free); a0(z)/a0(0) = sqrt(F); vs the record's F-DESI (CPL w0 -0.838, wa -0.62)")
W0, WA = -0.838, -0.62
r_desi = lambda z: math.sqrt((1 / (1 + z)) ** (-3 * (1 + W0 + WA)) * math.exp(-3 * WA * (1 - 1 / (1 + z))))
ZG = np.linspace(0, 2.5, 26)
B2 = {}
for zmax in (8.0, 15.0, 30.0):
    I0 = I_of(0.0, zmax) * EPS_SCALE
    F = np.array([I_of(z, zmax) * EPS_SCALE / I0 for z in ZG])
    rb = np.sqrt(F)
    rd = np.array([r_desi(z) for z in ZG])
    dlog = np.log10(rb) - np.log10(rd)
    B2[str(zmax)] = dict(r_BH={f"{z:.1f}": float(v) for z, v in zip(ZG, rb)}, max_dlog=float(np.max(np.abs(dlog))),
                         dlog_at_2=float(dlog[20]))
    P(f"  z_max {zmax:4.0f}: a0 ratio sqrt(F) at z 0.5/1/1.5/2/2.5 = " + "/".join(f"{rb[i]:.3f}" for i in (5, 10, 15, 20, 25))
      + f"  | DESI " + "/".join(f"{rd[i]:.3f}" for i in (5, 10, 15, 20, 25)) + f"  | max |dlog| {np.max(np.abs(dlog)):.3f}")
# M2 (run in every mode): eps x 10 leaves F unchanged
Fa = np.array([I_of(z, 8.0) for z in ZG]) / I_of(0.0, 8.0)
Fb = np.array([10 * I_of(z, 8.0) for z in ZG]) / (10 * I_of(0.0, 8.0))
check("M2 shape is eps-free", np.max(np.abs(Fa - Fb)) < 1e-12, f"max |dF| {np.max(np.abs(Fa - Fb)):.1e}")
if not MUT:
    mx = B2["8.0"]["max_dlog"]
    lab = "MATCHES DESI" if mx <= 0.02 else "DIFFERS"
    check("B2 class (primary z_max 8)", True, f"{lab}: max |dlog10 r| {mx:.3f}; at z 2 BH {B2['8.0']['r_BH']['2.0']:.3f} vs DESI {r_desi(2.0):.3f}")
    RES["B2_class"] = lab
RES["numbers"]["B2"] = B2

# ======================================================================== B3 sealed ALMA (CFG571 predict, read-only)
if not MUT:
    P("\nB3  sealed required gas under the BH branch (CFG571 predict; a0 x r_BH(z), z_max 8 primary)")
    src = open(os.path.join(HERE, "..", "CFG571_prereg_proprietary_alma", "cfg571_prereg.py")).read()
    head = src.split("# ---- controls ----")[0]
    ns = {"__file__": os.path.join(HERE, "..", "CFG571_prereg_proprietary_alma", "cfg571_prereg.py"), "__name__": "cfg571_import"}
    argv0 = sys.argv
    sys.argv = [argv0[0]]
    exec(compile(head, "cfg571_head", "exec"), ns)
    sys.argv = argv0
    zz = np.linspace(0, 2.5, 251)
    Fz = np.array([I_of(z, 8.0) for z in zz]) / I_of(0.0, 8.0)
    r_bh = lambda z: float(np.sqrt(np.interp(z, zz, Fz)))
    ns["MODELS"] = {"BH-k3": r_bh, "F-DESI": ns["r_desi"], "F-flat": lambda z: 1.0}
    pred = ns["predict"]
    SEAL = {"r_BH": {"1.41933": r_bh(1.41933), "1.997": r_bh(1.997)}, "GS4_24110": {}, "U4_27928": {}}
    for lm in (10.89, 10.76):
        pr = pred(7.39, 206.0, 1.997, 10 ** lm, 7.39 / 1.678)
        SEAL["GS4_24110"][str(lm)] = {f"{a}|{b}": {k: (None if v is None else (round(v, 4) if isinstance(v, float) else v)) for k, v in d.items()} for (a, b), d in pr.items()}
        for fn in ns["FOOT"]:
            P(f"  GS4_24110 logM* {lm} {fn}: " + "; ".join(
                f"{m} Mgas,req {ns['fmt'](pr[(fn, m)]['logMgas_Rg=Rd'])}" for m in ns["MODELS"]))
    z = 1.41933
    from scipy.integrate import quad
    dc = 2.99792458e5 / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0] * 1e3
    Re = 0.49 / 206264.806 * dc / (1 + z)
    for Vc in (150, 175, 200, 225, 250, 275, 300):
        pr = pred(2 * Re, float(Vc), z, 10 ** 10.74, Re / 1.678)
        SEAL["U4_27928"][str(Vc)] = {f"{a}|{b}": {k: (None if v is None else (round(v, 4) if isinstance(v, float) else v)) for k, v in d.items()} for (a, b), d in pr.items()}
        P(f"  U4_27928 V_c {Vc}: " + "; ".join(f"{m} {ns['fmt'](pr[('canon 9.36e-11', m)]['logMgas_Rg=Rd'])}/{ns['fmt'](pr[('alt 1.13e-10', m)]['logMgas_Rg=Rd'])}" for m in ns["MODELS"]))
    blob = json.dumps(SEAL, sort_keys=True, default=str).encode()
    sha = hashlib.sha256(blob).hexdigest()
    open(os.path.join(HERE, "SEALED_BH_BRANCH.json"), "wb").write(blob)
    RES["sealed_sha256"] = sha
    P(f"  r_BH(1.419) = {r_bh(1.41933):.4f}, r_BH(1.997) = {r_bh(1.997):.4f};  SEALED_BH_BRANCH.json sha256 = {sha}")
else:
    m1 = B2["8.0"]["r_BH"]["2.0"]
    P(f"\nM1 (k = 0): r_BH(2) = {m1:.4f}; eps_req(z_max 8) = {B1['8.0']['eps_req']:.3f}; compare main run")
    FAILS.append("MUTATE (designed)")

RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"cfg775_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUTF.close()
sys.exit(1 if FAILS else 0)
