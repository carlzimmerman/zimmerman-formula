#!/usr/bin/env python3
"""BI1 A2 correction (post-result, disclosed): the reaction force of carrier (iii)-explicit from the local identity
a_extra = (dL/df) |grad f| / rho_chi = g_b g_chi |df/dr| / (4 pi G rho_chi) with dL/df = g_b g_chi / (4 pi G), evaluated with an ACTUAL
Helmholtz-smoothed Xi = Psi_kin profile (spherical Yukawa convolution of s = rho_chi sigma^2 / (rho_ref v_stiff^2)) around the group
(M_b 5e12) and the L* galaxy, for R_W x 0.5 / 1 / 2. It replaces A2's window-diluted proxy (dXi/drho x l^2/2R_W^2 / R_W), which is withdrawn.
    python3 bi1_a2b.py   -> bi1_a2b.json / bi1_a2b.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"))
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
sys.argv = _a
G, MS, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; VST = {"canonical": 265.8, "alt": 288.1}
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
def fsw(Xi, pc=1.0): return (Xi * Xi / (1 + Xi * Xi)) * (1 / math.sqrt(2) + (1 - 1 / math.sqrt(2)) / (1 + pc * pc))
L = []; RES = dict(note="post-result correction, disclosed; TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
def P(s): print(s, flush=True); L.append(str(s))
for foot, a0 in A0.items():
    th = Q15["footings"][foot]["main"]["theta"]; h = float(Q15["footings"][foot]["main"]["h"]); OB, OD = th["omega_b"], th["omega_d"]; R = OD / OB; Om = (OB + OD) / h ** 2
    H0 = 100 * h * 1e3 / MPC; rhoc = 3 * H0 ** 2 / (8 * math.pi * G); rref = 200 * (OD / h ** 2) * rhoc; rbar = (OD / h ** 2) * rhoc; RW0 = VST[foot] * 1e3 / (2 * H0); RES[foot] = {}
    for name, Mb, rks in (("group 5e12", 5e12, (102.0, 400.0)), ("L* 8e10", 8e10, (100.0, 250.0, 1000.0))):
        H = C.halo(Mb, R, h, Om, z=0.0); R2 = H["R200"] * KPC; v = math.sqrt(4.3009172706e-6 * H["M200"] / H["R200"]) * 1e3; sig2 = v * v / 2
        rg = np.geomspace(1e-3 * MPC, 30 * MPC, 6000)
        rho = np.where(rg < R2, H["fchi"] * H["M200"] * MS / (4 * math.pi * R2 * rg ** 2), rbar)
        s = rho * np.where(rg < R2, sig2, (60e3) ** 2) / (rref * (VST[foot] * 1e3) ** 2)          # field dispersion outside the halo: 60 km/s (stated)
        Mchi = np.cumsum(4 * math.pi * rg ** 2 * rho * np.gradient(rg)); Mbr = Mb * MS * np.minimum(rg / R2, 1.0)        # baryons SIS-like inside R200 (stated)
        rows = {}
        for mult in (0.5, 1.0, 2.0):
            RW = RW0 * mult; Psi = np.empty_like(rg)
            for i, r in enumerate(rg):
                k = (np.exp(-np.abs(r - rg) / RW) - np.exp(-(r + rg) / RW)); Psi[i] = np.trapz(s * rg * k, rg) / (2 * RW * r)
            f = np.array([fsw(x) for x in Psi]); dfdr = np.gradient(f, rg)
            for rk in rks:
                r = rk * KPC; gb = G * float(np.interp(r, rg, Mbr)) / r ** 2; gc = G * float(np.interp(r, rg, Mchi)) / r ** 2; rr = float(np.interp(r, rg, rho))
                a = gb * gc * abs(float(np.interp(r, rg, dfdr))) / (4 * math.pi * G * rr); glaw = 0.5 * gb + math.sqrt(0.25 * gb * gb + a0 * gb)
                rows[f"R_W x{mult} r {rk:g} kpc"] = dict(Xi=float(np.interp(r, rg, Psi)), f=float(np.interp(r, rg, f)), a_extra=a, over_a0=a / a0, over_law=a / glaw)
        RES[foot][name] = rows
        for k_, v_ in rows.items(): P(f"[{foot}] {name} {k_}: Xi {v_['Xi']:.3g}, f {v_['f']:.3g}, a_extra {v_['a_extra']:.2e} m/s^2 = {v_['over_a0']:.3g} a0 = {v_['over_law']:.3g} of the law's g")
    worst = max(v_["over_law"] for n in RES[foot] for v_ in RES[foot][n].values() if "x1.0" in str([k for k in RES[foot][n] if RES[foot][n][k] is v_]))
    RES[foot]["worst_over_law_RW1"] = max(v_["over_law"] for n in RES[foot] if isinstance(RES[foot][n], dict) for k, v_ in RES[foot][n].items() if "x1.0" in k)
    RES[foot]["B0_iii_explicit_local"] = "FAIL" if RES[foot]["worst_over_law_RW1"] > 1e-3 else "PASS"
    P(f"[{foot}] local-identity B0(iii)-explicit: worst {RES[foot]['worst_over_law_RW1']:.3g} of the law's g at R_W x1 (line 1e-3) -> {RES[foot]['B0_iii_explicit_local']}")
json.dump(RES, open(os.path.join(HERE, "bi1_a2b.json"), "w"), indent=1); open(os.path.join(HERE, "bi1_a2b.out"), "w").write("\n".join(L) + "\n")
